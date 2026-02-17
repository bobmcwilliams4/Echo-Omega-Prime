"""
LG09 Criminal Law Engine - Vector Search Module
=================================================
ChromaDB-based semantic search for criminal law doctrine retrieval.

Architecture:
    - In-memory ChromaDB collection for fast similarity search
    - Sentence-transformer embeddings (all-MiniLM-L6-v2)
    - Fallback to keyword search if vector DB unavailable
    - Pre-populated with doctrine cache entries on init
    - Thread-safe query interface

Author: ECHO OMEGA PRIME
Engine: LG09 Criminal Law
"""

from __future__ import annotations

import hashlib
import json
import re
import threading
import time
import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from loguru import logger
from pydantic import BaseModel, Field


# =============================================================================
# SEARCH RESULT MODELS
# =============================================================================

class SearchResult(BaseModel):
    """A single search result from vector or keyword search."""
    doc_id: str = Field(description="Document identifier")
    doctrine_key: str = Field(description="Doctrine cache key")
    text: str = Field(description="Matched text content")
    score: float = Field(description="Similarity score 0.0-1.0")
    metadata: Dict[str, Any] = Field(default_factory=dict)
    search_method: str = Field(default="vector", description="vector or keyword")

    class Config:
        json_schema_extra = {
            "example": {
                "doc_id": "doc_001",
                "doctrine_key": "homicide.felony_murder",
                "text": "The felony murder rule imputes malice...",
                "score": 0.87,
                "metadata": {"jurisdiction": "federal", "category": "homicide"},
                "search_method": "vector",
            }
        }


class SearchResponse(BaseModel):
    """Response from a search operation."""
    query: str
    results: List[SearchResult]
    total_results: int
    search_method: str
    latency_ms: float
    collection_size: int

    class Config:
        json_schema_extra = {
            "example": {
                "query": "felony murder rule",
                "results": [],
                "total_results": 0,
                "search_method": "vector",
                "latency_ms": 15.3,
                "collection_size": 500,
            }
        }


# =============================================================================
# KEYWORD INDEX (FALLBACK)
# =============================================================================

class KeywordIndex:
    """
    Inverted index for keyword-based fallback search.
    Used when ChromaDB/embedding model is unavailable.
    """

    def __init__(self):
        self._index: Dict[str, Set[str]] = defaultdict(set)  # term -> doc_ids
        self._documents: Dict[str, Dict[str, Any]] = {}  # doc_id -> {text, metadata}
        self._lock = threading.Lock()

    def add_document(self, doc_id: str, text: str, metadata: Optional[Dict] = None) -> None:
        """Index a document for keyword search."""
        with self._lock:
            self._documents[doc_id] = {"text": text, "metadata": metadata or {}}
            tokens = self._tokenize(text)
            for token in tokens:
                self._index[token].add(doc_id)

    def search(self, query: str, max_results: int = 10) -> List[Tuple[str, float]]:
        """
        Search by keyword overlap. Returns (doc_id, score) pairs.
        Score is Jaccard-like overlap coefficient.
        """
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []

        doc_scores: Dict[str, float] = defaultdict(float)
        with self._lock:
            for token in query_tokens:
                matching_docs = self._index.get(token, set())
                for doc_id in matching_docs:
                    doc_scores[doc_id] += 1.0

        # Normalize scores
        max_possible = len(query_tokens)
        results = []
        for doc_id, raw_score in doc_scores.items():
            normalized = raw_score / max_possible
            results.append((doc_id, normalized))

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:max_results]

    def get_document(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a document by ID."""
        with self._lock:
            return self._documents.get(doc_id)

    @property
    def size(self) -> int:
        with self._lock:
            return len(self._documents)

    @staticmethod
    def _tokenize(text: str) -> Set[str]:
        """Tokenize text into lowercase terms, removing stopwords."""
        stopwords = {
            "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
            "have", "has", "had", "do", "does", "did", "will", "would", "could",
            "should", "may", "might", "shall", "can", "to", "of", "in", "for",
            "on", "with", "at", "by", "from", "as", "into", "through", "during",
            "before", "after", "above", "below", "between", "out", "off", "over",
            "under", "again", "further", "then", "once", "here", "there", "when",
            "where", "why", "how", "all", "each", "every", "both", "few", "more",
            "most", "other", "some", "such", "no", "nor", "not", "only", "own",
            "same", "so", "than", "too", "very", "and", "but", "or", "if", "it",
            "its", "this", "that", "what", "which", "who", "whom", "these", "those",
        }
        tokens = set(re.findall(r"\b[a-z]{2,}\b", text.lower()))
        return tokens - stopwords


# =============================================================================
# CHROMA WRAPPER
# =============================================================================

class ChromaSearchEngine:
    """
    ChromaDB-based vector search engine for criminal law doctrines.

    Falls back to keyword search if ChromaDB or embedding model
    is not available. Graceful degradation is the design principle.
    """

    def __init__(
        self,
        collection_name: str = "lg09_criminal_law",
        persist_directory: Optional[str] = None,
        similarity_threshold: float = 0.65,
        max_results: int = 10,
    ):
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        self.similarity_threshold = similarity_threshold
        self.max_results = max_results

        # State
        self._chroma_available = False
        self._collection = None
        self._client = None
        self._keyword_index = KeywordIndex()
        self._lock = threading.Lock()
        self._doc_count = 0

        # Try to initialize ChromaDB
        self._init_chromadb()

    def _init_chromadb(self) -> None:
        """Attempt to initialize ChromaDB. Falls back gracefully."""
        try:
            import chromadb
            from chromadb.config import Settings

            if self.persist_directory:
                persist_path = Path(self.persist_directory)
                persist_path.mkdir(parents=True, exist_ok=True)
                self._client = chromadb.Client(Settings(
                    chroma_db_impl="duckdb+parquet",
                    persist_directory=str(persist_path),
                    anonymized_telemetry=False,
                ))
            else:
                self._client = chromadb.Client()

            self._collection = self._client.get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"},
            )
            self._chroma_available = True
            logger.info(
                f"ChromaDB initialized: collection={self.collection_name} "
                f"existing_count={self._collection.count()}"
            )
        except ImportError:
            logger.warning("ChromaDB not installed. Using keyword fallback search.")
            self._chroma_available = False
        except Exception as e:
            logger.warning(f"ChromaDB init failed: {e}. Using keyword fallback search.")
            self._chroma_available = False

    @property
    def is_vector_enabled(self) -> bool:
        return self._chroma_available

    @property
    def collection_size(self) -> int:
        if self._chroma_available and self._collection is not None:
            try:
                return self._collection.count()
            except Exception:
                return self._doc_count
        return self._keyword_index.size

    # -------------------------------------------------------------------------
    # DOCUMENT INGESTION
    # -------------------------------------------------------------------------

    def add_doctrine(
        self,
        doctrine_key: str,
        text: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Add a doctrine entry to the search index.

        Args:
            doctrine_key: Unique doctrine identifier (e.g., "homicide.felony_murder")
            text: Full doctrine text content
            metadata: Optional metadata (jurisdiction, category, etc.)

        Returns:
            Document ID
        """
        doc_id = f"doc_{hashlib.md5(doctrine_key.encode()).hexdigest()[:12]}"
        meta = metadata or {}
        meta["doctrine_key"] = doctrine_key
        meta["indexed_at"] = datetime.now(timezone.utc).isoformat()
        meta["text_length"] = len(text)

        # Always add to keyword index (backup)
        self._keyword_index.add_document(doc_id, text, meta)

        # Add to ChromaDB if available
        if self._chroma_available and self._collection is not None:
            try:
                # ChromaDB metadata must be str/int/float/bool
                clean_meta = {k: str(v) if not isinstance(v, (int, float, bool)) else v for k, v in meta.items()}
                self._collection.upsert(
                    ids=[doc_id],
                    documents=[text],
                    metadatas=[clean_meta],
                )
            except Exception as e:
                logger.error(f"ChromaDB upsert failed for {doctrine_key}: {e}")

        self._doc_count += 1
        return doc_id

    def add_doctrines_bulk(
        self,
        entries: List[Dict[str, Any]],
    ) -> int:
        """
        Bulk add doctrine entries.

        Args:
            entries: List of dicts with keys: doctrine_key, text, metadata (optional)

        Returns:
            Number of entries added
        """
        count = 0
        for entry in entries:
            key = entry.get("doctrine_key", "")
            text = entry.get("text", "")
            meta = entry.get("metadata", {})
            if key and text:
                self.add_doctrine(key, text, meta)
                count += 1
        logger.info(f"Bulk indexed {count}/{len(entries)} doctrine entries")
        return count

    # -------------------------------------------------------------------------
    # SEARCH
    # -------------------------------------------------------------------------

    def search(
        self,
        query: str,
        max_results: Optional[int] = None,
        threshold: Optional[float] = None,
        jurisdiction_filter: Optional[str] = None,
        category_filter: Optional[str] = None,
    ) -> SearchResponse:
        """
        Search for relevant doctrines.

        Uses ChromaDB vector search if available, otherwise falls back
        to keyword search.

        Args:
            query: Search query text
            max_results: Maximum number of results (default from config)
            threshold: Minimum similarity score (default from config)
            jurisdiction_filter: Filter by jurisdiction
            category_filter: Filter by crime category

        Returns:
            SearchResponse with ranked results
        """
        start_time = time.time()
        limit = max_results or self.max_results
        min_score = threshold or self.similarity_threshold

        if self._chroma_available and self._collection is not None:
            results = self._vector_search(query, limit, min_score, jurisdiction_filter, category_filter)
            method = "vector"
        else:
            results = self._keyword_search(query, limit, min_score, jurisdiction_filter, category_filter)
            method = "keyword"

        latency = (time.time() - start_time) * 1000

        return SearchResponse(
            query=query,
            results=results,
            total_results=len(results),
            search_method=method,
            latency_ms=round(latency, 2),
            collection_size=self.collection_size,
        )

    def _vector_search(
        self,
        query: str,
        limit: int,
        threshold: float,
        jurisdiction_filter: Optional[str],
        category_filter: Optional[str],
    ) -> List[SearchResult]:
        """Perform vector similarity search via ChromaDB."""
        try:
            where_filter = None
            conditions = []
            if jurisdiction_filter:
                conditions.append({"jurisdiction": jurisdiction_filter})
            if category_filter:
                conditions.append({"category": category_filter})

            if len(conditions) == 1:
                where_filter = conditions[0]
            elif len(conditions) > 1:
                where_filter = {"$and": conditions}

            query_params = {
                "query_texts": [query],
                "n_results": limit,
            }
            if where_filter:
                query_params["where"] = where_filter

            chroma_results = self._collection.query(**query_params)

            results = []
            if chroma_results and chroma_results.get("ids"):
                ids = chroma_results["ids"][0] if chroma_results["ids"] else []
                documents = chroma_results["documents"][0] if chroma_results.get("documents") else []
                distances = chroma_results["distances"][0] if chroma_results.get("distances") else []
                metadatas = chroma_results["metadatas"][0] if chroma_results.get("metadatas") else []

                for i, doc_id in enumerate(ids):
                    # ChromaDB cosine distance: 0 = identical, 2 = opposite
                    # Convert to similarity: 1 - (distance / 2)
                    distance = distances[i] if i < len(distances) else 1.0
                    similarity = max(0.0, 1.0 - (distance / 2.0))

                    if similarity < threshold:
                        continue

                    text = documents[i] if i < len(documents) else ""
                    meta = metadatas[i] if i < len(metadatas) else {}

                    results.append(SearchResult(
                        doc_id=doc_id,
                        doctrine_key=meta.get("doctrine_key", "unknown"),
                        text=text[:2000],
                        score=round(similarity, 4),
                        metadata=meta,
                        search_method="vector",
                    ))

            return results

        except Exception as e:
            logger.error(f"Vector search failed, falling back to keyword: {e}")
            return self._keyword_search(query, limit, threshold, jurisdiction_filter, category_filter)

    def _keyword_search(
        self,
        query: str,
        limit: int,
        threshold: float,
        jurisdiction_filter: Optional[str],
        category_filter: Optional[str],
    ) -> List[SearchResult]:
        """Perform keyword-based fallback search."""
        raw_results = self._keyword_index.search(query, max_results=limit * 2)
        results = []

        for doc_id, score in raw_results:
            if score < threshold * 0.5:  # Lower threshold for keyword search
                continue

            doc = self._keyword_index.get_document(doc_id)
            if not doc:
                continue

            meta = doc.get("metadata", {})

            # Apply filters
            if jurisdiction_filter and meta.get("jurisdiction") != jurisdiction_filter:
                continue
            if category_filter and meta.get("category") != category_filter:
                continue

            results.append(SearchResult(
                doc_id=doc_id,
                doctrine_key=meta.get("doctrine_key", "unknown"),
                text=doc["text"][:2000],
                score=round(score, 4),
                metadata=meta,
                search_method="keyword",
            ))

            if len(results) >= limit:
                break

        return results

    # -------------------------------------------------------------------------
    # MANAGEMENT
    # -------------------------------------------------------------------------

    def delete_doctrine(self, doctrine_key: str) -> bool:
        """Remove a doctrine from the search index."""
        doc_id = f"doc_{hashlib.md5(doctrine_key.encode()).hexdigest()[:12]}"

        if self._chroma_available and self._collection is not None:
            try:
                self._collection.delete(ids=[doc_id])
                logger.info(f"Deleted from vector index: {doctrine_key}")
                return True
            except Exception as e:
                logger.error(f"Failed to delete from ChromaDB: {e}")
                return False

        return False

    def get_collection_stats(self) -> Dict[str, Any]:
        """Get search index statistics."""
        stats = {
            "collection_name": self.collection_name,
            "vector_enabled": self._chroma_available,
            "total_documents": self.collection_size,
            "keyword_index_size": self._keyword_index.size,
            "similarity_threshold": self.similarity_threshold,
            "max_results": self.max_results,
        }

        if self._chroma_available and self._collection is not None:
            try:
                stats["chroma_count"] = self._collection.count()
            except Exception:
                stats["chroma_count"] = -1

        return stats

    def rebuild_index(self, doctrines: Dict[str, Dict[str, Any]]) -> int:
        """
        Rebuild the entire search index from a doctrine dictionary.

        Args:
            doctrines: Dict mapping doctrine_key -> {text, metadata}

        Returns:
            Number of entries indexed
        """
        logger.info(f"Rebuilding search index with {len(doctrines)} entries...")

        # Clear existing
        if self._chroma_available and self._client is not None:
            try:
                self._client.delete_collection(self.collection_name)
                self._collection = self._client.create_collection(
                    name=self.collection_name,
                    metadata={"hnsw:space": "cosine"},
                )
            except Exception as e:
                logger.error(f"Failed to reset ChromaDB collection: {e}")

        self._keyword_index = KeywordIndex()
        self._doc_count = 0

        count = 0
        for key, data in doctrines.items():
            text = data.get("text", "")
            meta = data.get("metadata", {})
            if text:
                self.add_doctrine(key, text, meta)
                count += 1

        logger.info(f"Search index rebuilt: {count} entries indexed")
        return count

    def health_check(self) -> Dict[str, Any]:
        """Check search subsystem health."""
        status = "healthy"
        issues = []

        if not self._chroma_available:
            issues.append("ChromaDB not available, using keyword fallback")

        if self.collection_size == 0:
            issues.append("Search index is empty")
            status = "degraded"

        if self._chroma_available and self._collection is not None:
            try:
                test_results = self._collection.query(
                    query_texts=["test health check"],
                    n_results=1,
                )
                if test_results is None:
                    issues.append("ChromaDB query returned None")
                    status = "degraded"
            except Exception as e:
                issues.append(f"ChromaDB query test failed: {str(e)[:100]}")
                status = "degraded"

        return {
            "component": "vector_search",
            "status": status,
            "vector_enabled": self._chroma_available,
            "collection_size": self.collection_size,
            "issues": issues,
        }


# =============================================================================
# MULTI-FIELD SEARCH (STRUCTURED)
# =============================================================================

class StructuredSearch:
    """
    Multi-field structured search for complex criminal law queries.

    Supports filtering by:
    - Jurisdiction (federal, texas, model_penal_code)
    - Crime category (homicide, assault, property, drug, etc.)
    - Severity level (felony, misdemeanor, infraction)
    - Statutory reference (USC section, TPC section)
    - Date range (for case law references)
    """

    def __init__(self, engine: ChromaSearchEngine):
        self._engine = engine

    def search_by_statute(self, statute_ref: str, max_results: int = 5) -> SearchResponse:
        """Search for doctrines related to a specific statute."""
        normalized_ref = statute_ref.strip().upper()
        query = f"statute {normalized_ref} elements analysis"
        return self._engine.search(query, max_results=max_results)

    def search_by_elements(self, crime_type: str, element: str, max_results: int = 5) -> SearchResponse:
        """Search for specific elements of a crime."""
        query = f"{crime_type} element {element} requirement analysis"
        return self._engine.search(query, max_results=max_results)

    def search_defenses(self, crime_type: str, max_results: int = 5) -> SearchResponse:
        """Search for applicable defenses to a crime type."""
        query = f"defense {crime_type} affirmative defense justification excuse"
        return self._engine.search(query, max_results=max_results)

    def search_sentencing(self, crime_type: str, jurisdiction: str = "federal", max_results: int = 5) -> SearchResponse:
        """Search for sentencing information."""
        query = f"sentencing {crime_type} {jurisdiction} guidelines punishment range"
        return self._engine.search(query, max_results=max_results, jurisdiction_filter=jurisdiction)

    def search_constitutional_issue(self, issue: str, max_results: int = 5) -> SearchResponse:
        """Search for constitutional issues in criminal law."""
        query = f"constitutional {issue} rights protection criminal procedure"
        return self._engine.search(query, max_results=max_results, category_filter="constitutional")

    def search_case_law(self, topic: str, max_results: int = 5) -> SearchResponse:
        """Search for relevant case law on a topic."""
        query = f"case law precedent {topic} holding ruling"
        return self._engine.search(query, max_results=max_results)

    def search_procedure(self, stage: str, max_results: int = 5) -> SearchResponse:
        """Search for procedural information at a given stage."""
        query = f"criminal procedure {stage} requirements process"
        return self._engine.search(query, max_results=max_results, category_filter="procedural")

    def compare_jurisdictions(
        self, topic: str, jurisdictions: Optional[List[str]] = None, max_results: int = 5
    ) -> Dict[str, SearchResponse]:
        """Compare treatment of a topic across jurisdictions."""
        jurisdictions = jurisdictions or ["federal", "texas"]
        results = {}
        for jur in jurisdictions:
            results[jur] = self._engine.search(
                f"{topic} {jur} law",
                max_results=max_results,
                jurisdiction_filter=jur,
            )
        return results


# =============================================================================
# MODULE-LEVEL SINGLETON
# =============================================================================

_search_engine: Optional[ChromaSearchEngine] = None
_structured_search: Optional[StructuredSearch] = None


def get_search_engine(
    collection_name: str = "lg09_criminal_law",
    persist_directory: Optional[str] = None,
) -> ChromaSearchEngine:
    """Get or create the singleton search engine."""
    global _search_engine
    if _search_engine is None:
        _search_engine = ChromaSearchEngine(
            collection_name=collection_name,
            persist_directory=persist_directory,
        )
    return _search_engine


def get_structured_search() -> StructuredSearch:
    """Get or create the singleton structured search."""
    global _structured_search
    if _structured_search is None:
        _structured_search = StructuredSearch(get_search_engine())
    return _structured_search
