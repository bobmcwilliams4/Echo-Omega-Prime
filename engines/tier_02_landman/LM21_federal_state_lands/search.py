"""
LM21 Federal/State Lands Engine - Vector Search Module
========================================================
Semantic retrieval fallback for queries that miss the doctrine cache.
Uses lightweight embedding similarity with TF-IDF weighted cosine
distance over the doctrine corpus.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from loguru import logger
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

class SearchResult(BaseModel):
    """A single search result from the vector store."""
    doc_id: str
    topic: str
    score: float = Field(ge=0.0, le=1.0)
    snippet: str = ""
    authority: str = ""
    metadata: Dict[str, Any] = Field(default_factory=dict)


class SearchResponse(BaseModel):
    """Container for search results."""
    query: str
    normalized_query: str = ""
    results: List[SearchResult] = Field(default_factory=list)
    total_candidates: int = 0
    search_time_ms: float = 0.0
    search_hash: str = ""


class DocumentRecord(BaseModel):
    """A document stored in the vector index."""
    doc_id: str
    topic: str
    content: str
    authority: str = ""
    keywords: List[str] = Field(default_factory=list)
    category: str = ""
    weight: float = 1.0
    token_counts: Dict[str, int] = Field(default_factory=dict)
    norm: float = 0.0


# ---------------------------------------------------------------------------
# TF-IDF Vector Search Engine
# ---------------------------------------------------------------------------

class FederalLandsSearchEngine:
    """
    Lightweight vector search using TF-IDF cosine similarity.
    Designed for fast fallback when the doctrine cache misses.
    No external dependencies beyond stdlib + pydantic.
    """

    def __init__(self, data_dir: Optional[Path] = None) -> None:
        self._documents: Dict[str, DocumentRecord] = {}
        self._idf: Dict[str, float] = {}
        self._vocab: set[str] = set()
        self._doc_count: int = 0
        self._df: Dict[str, int] = defaultdict(int)
        self._data_dir = data_dir or Path("data")
        self._indexed = False
        logger.info("FederalLandsSearchEngine initialized")

    def add_document(
        self,
        doc_id: str,
        topic: str,
        content: str,
        authority: str = "",
        keywords: Optional[List[str]] = None,
        category: str = "",
        weight: float = 1.0,
    ) -> None:
        """Add a document to the search index."""
        tokens = self._tokenize(content + " " + topic + " " + " ".join(keywords or []))
        token_counts = Counter(tokens)
        self._documents[doc_id] = DocumentRecord(
            doc_id=doc_id,
            topic=topic,
            content=content,
            authority=authority,
            keywords=keywords or [],
            category=category,
            weight=weight,
            token_counts=dict(token_counts),
        )
        for token in set(tokens):
            self._df[token] += 1
            self._vocab.add(token)
        self._doc_count += 1
        self._indexed = False

    def build_index(self) -> None:
        """Compute IDF values and document norms for cosine similarity."""
        if self._doc_count == 0:
            logger.warning("No documents to index")
            return

        self._idf = {}
        for token, df in self._df.items():
            self._idf[token] = math.log((self._doc_count + 1) / (df + 1)) + 1.0

        for doc in self._documents.values():
            norm_sq = 0.0
            for token, count in doc.token_counts.items():
                tf = 1 + math.log(count) if count > 0 else 0
                tfidf = tf * self._idf.get(token, 1.0)
                norm_sq += tfidf * tfidf
            doc.norm = math.sqrt(norm_sq) if norm_sq > 0 else 1.0

        self._indexed = True
        logger.info(
            f"Search index built | docs={self._doc_count} | "
            f"vocab={len(self._vocab)}"
        )

    def search(
        self,
        query: str,
        top_k: int = 5,
        min_score: float = 0.05,
        category_filter: Optional[str] = None,
    ) -> SearchResponse:
        """
        Search the document index using TF-IDF cosine similarity.

        Args:
            query: The search query string.
            top_k: Maximum number of results to return.
            min_score: Minimum similarity score threshold.
            category_filter: Optional category to filter results.

        Returns:
            SearchResponse with ranked results.
        """
        import time
        start = time.perf_counter()

        if not self._indexed:
            self.build_index()

        query_tokens = self._tokenize(query)
        query_counts = Counter(query_tokens)

        query_vec: Dict[str, float] = {}
        query_norm_sq = 0.0
        for token, count in query_counts.items():
            tf = 1 + math.log(count) if count > 0 else 0
            idf = self._idf.get(token, 1.0)
            tfidf = tf * idf
            query_vec[token] = tfidf
            query_norm_sq += tfidf * tfidf
        query_norm = math.sqrt(query_norm_sq) if query_norm_sq > 0 else 1.0

        scores: List[Tuple[str, float]] = []
        candidates = 0
        for doc_id, doc in self._documents.items():
            if category_filter and doc.category != category_filter:
                continue
            candidates += 1

            dot_product = 0.0
            for token, q_val in query_vec.items():
                if token in doc.token_counts:
                    d_count = doc.token_counts[token]
                    d_tf = 1 + math.log(d_count) if d_count > 0 else 0
                    d_tfidf = d_tf * self._idf.get(token, 1.0)
                    dot_product += q_val * d_tfidf

            similarity = dot_product / (query_norm * doc.norm) if doc.norm > 0 else 0.0
            similarity *= doc.weight

            if similarity >= min_score:
                scores.append((doc_id, similarity))

        scores.sort(key=lambda x: x[1], reverse=True)
        top_results = scores[:top_k]

        results: List[SearchResult] = []
        for doc_id, score in top_results:
            doc = self._documents[doc_id]
            snippet = doc.content[:300].strip()
            if len(doc.content) > 300:
                snippet += "..."
            results.append(SearchResult(
                doc_id=doc_id,
                topic=doc.topic,
                score=round(score, 6),
                snippet=snippet,
                authority=doc.authority,
                metadata={
                    "category": doc.category,
                    "keywords": doc.keywords,
                    "weight": doc.weight,
                },
            ))

        elapsed_ms = (time.perf_counter() - start) * 1000
        search_hash = hashlib.sha256(
            json.dumps([r.doc_id for r in results]).encode()
        ).hexdigest()

        return SearchResponse(
            query=query,
            normalized_query=" ".join(query_tokens),
            results=results,
            total_candidates=candidates,
            search_time_ms=round(elapsed_ms, 3),
            search_hash=search_hash,
        )

    def get_document(self, doc_id: str) -> Optional[DocumentRecord]:
        """Retrieve a document by ID."""
        return self._documents.get(doc_id)

    def list_categories(self) -> List[str]:
        """List all unique document categories."""
        return sorted({d.category for d in self._documents.values() if d.category})

    def document_count(self) -> int:
        """Return total number of indexed documents."""
        return self._doc_count

    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text into lowercase words, removing stop words."""
        stop_words = frozenset({
            "the", "a", "an", "is", "are", "was", "were", "be", "been",
            "being", "have", "has", "had", "do", "does", "did", "will",
            "would", "could", "should", "may", "might", "shall", "can",
            "of", "in", "to", "for", "with", "on", "at", "from", "by",
            "about", "as", "into", "through", "during", "before", "after",
            "and", "but", "or", "not", "no", "if", "then", "than", "so",
            "this", "that", "these", "those", "it", "its", "he", "she",
        })
        words = re.findall(r"[a-zA-Z0-9]+", text.lower())
        return [w for w in words if w not in stop_words and len(w) > 1]

    def save_index(self, path: Optional[Path] = None) -> None:
        """Persist the search index to disk."""
        target = path or (self._data_dir / "lm21_search_index.json")
        target.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "doc_count": self._doc_count,
            "documents": {
                doc_id: {
                    "topic": doc.topic,
                    "content": doc.content[:500],
                    "authority": doc.authority,
                    "keywords": doc.keywords,
                    "category": doc.category,
                    "weight": doc.weight,
                }
                for doc_id, doc in self._documents.items()
            },
        }
        target.write_text(json.dumps(data, indent=2), encoding="utf-8")
        logger.info(f"Search index saved to {target} | docs={self._doc_count}")

    def load_index(self, path: Optional[Path] = None) -> int:
        """Load the search index from disk. Returns count of loaded docs."""
        target = path or (self._data_dir / "lm21_search_index.json")
        if not target.exists():
            logger.warning(f"Index file not found: {target}")
            return 0

        data = json.loads(target.read_text(encoding="utf-8"))
        loaded = 0
        for doc_id, doc_data in data.get("documents", {}).items():
            self.add_document(
                doc_id=doc_id,
                topic=doc_data["topic"],
                content=doc_data["content"],
                authority=doc_data.get("authority", ""),
                keywords=doc_data.get("keywords", []),
                category=doc_data.get("category", ""),
                weight=doc_data.get("weight", 1.0),
            )
            loaded += 1

        self.build_index()
        logger.info(f"Search index loaded from {target} | docs={loaded}")
        return loaded
