"""
LM18 Title Insurance Engine — Vector Search
===========================================
Semantic search and vector indexing for title insurance knowledge retrieval.

Engine: LM18 | Port: 8518 | Domain: title_insurance
Version: 1.0.0 | TIE Gold Standard Component 7
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

from loguru import logger


@dataclass
class SearchDocument:
    """A searchable document with vector embedding."""
    doc_id: str
    content: str
    metadata: dict[str, Any]
    embedding: Optional[list[float]] = None
    category: str = "general"
    authority_level: int = 5


@dataclass
class SearchResponse:
    """Response from vector search."""
    query: str
    results: list[SearchDocument]
    scores: list[float]
    total_results: int
    search_time_ms: float


class VectorIndex:
    """Vector search index for title insurance knowledge."""

    def __init__(self, embedding_model: str = "all-MiniLM-L6-v2"):
        """
        Initialize vector index.

        Args:
            embedding_model: Name of sentence-transformer model to use
        """
        self.embedding_model = embedding_model
        self.documents: list[SearchDocument] = []
        self.index_built = False

        # Try to import sentence-transformers
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(embedding_model)
            self.model_available = True
            logger.info(f"Loaded embedding model: {embedding_model}")
        except (ImportError, OSError, Exception) as exc:
            logger.warning(f"Embedding model unavailable ({type(exc).__name__}: {exc}); vector search disabled — falling back to keyword search")
            self.model = None
            self.model_available = False

    def add_document(self, doc_id: str, content: str, metadata: dict[str, Any], category: str = "general", authority_level: int = 5) -> None:
        """
        Add document to index.

        Args:
            doc_id: Unique document identifier
            content: Document text content
            metadata: Document metadata
            category: Document category
            authority_level: Authority level (1=highest, 8=lowest)
        """
        doc = SearchDocument(
            doc_id=doc_id,
            content=content,
            metadata=metadata,
            category=category,
            authority_level=authority_level
        )

        # Generate embedding if model available
        if self.model_available and self.model is not None:
            doc.embedding = self.model.encode(content).tolist()

        self.documents.append(doc)
        logger.debug(f"Added document {doc_id} to index (category: {category}, authority: {authority_level})")

    def build_index(self) -> None:
        """Build or rebuild the vector index."""
        if not self.model_available:
            logger.warning("Cannot build index: embedding model not available")
            return

        logger.info(f"Building vector index with {len(self.documents)} documents")

        # Re-embed all documents
        if self.model is not None:
            for doc in self.documents:
                if doc.embedding is None:
                    doc.embedding = self.model.encode(doc.content).tolist()

        self.index_built = True
        logger.info("Vector index built successfully")

    def search(
        self,
        query: str,
        top_k: int = 10,
        similarity_threshold: float = 0.72,
        category_filter: Optional[str] = None,
        authority_max: int = 8
    ) -> SearchResponse:
        """
        Search index for documents matching query.

        Args:
            query: Search query text
            top_k: Maximum results to return
            similarity_threshold: Minimum cosine similarity (0-1)
            category_filter: Filter by category if provided
            authority_max: Maximum authority level to include (1=highest, 8=lowest)

        Returns:
            SearchResponse with matching documents and scores
        """
        import time
        start_time = time.time()

        if not self.model_available or self.model is None:
            logger.warning("Vector search unavailable; returning empty results")
            return SearchResponse(
                query=query,
                results=[],
                scores=[],
                total_results=0,
                search_time_ms=0.0
            )

        # Generate query embedding
        query_embedding = self.model.encode(query)

        # Calculate similarities
        results_with_scores = []
        for doc in self.documents:
            # Apply filters
            if category_filter and doc.category != category_filter:
                continue
            if doc.authority_level > authority_max:
                continue
            if doc.embedding is None:
                continue

            # Calculate cosine similarity
            similarity = self._cosine_similarity(query_embedding, doc.embedding)

            if similarity >= similarity_threshold:
                results_with_scores.append((doc, similarity))

        # Sort by similarity descending, then authority ascending
        results_with_scores.sort(key=lambda x: (-x[1], x[0].authority_level))

        # Take top K
        top_results = results_with_scores[:top_k]
        results = [r[0] for r in top_results]
        scores = [r[1] for r in top_results]

        search_time_ms = (time.time() - start_time) * 1000

        return SearchResponse(
            query=query,
            results=results,
            scores=scores,
            total_results=len(results_with_scores),
            search_time_ms=search_time_ms
        )

    def _cosine_similarity(self, vec1: Any, vec2: list[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        import numpy as np
        vec1_np = np.array(vec1)
        vec2_np = np.array(vec2)

        dot_product = np.dot(vec1_np, vec2_np)
        norm1 = np.linalg.norm(vec1_np)
        norm2 = np.linalg.norm(vec2_np)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return float(dot_product / (norm1 * norm2))

    def get_document_by_id(self, doc_id: str) -> Optional[SearchDocument]:
        """Retrieve document by ID."""
        for doc in self.documents:
            if doc.doc_id == doc_id:
                return doc
        return None

    def get_documents_by_category(self, category: str) -> list[SearchDocument]:
        """Get all documents in a category."""
        return [doc for doc in self.documents if doc.category == category]

    def get_document_count(self) -> int:
        """Get total number of indexed documents."""
        return len(self.documents)


# ===================================================================
# Global Vector Index
# ===================================================================

_VECTOR_INDEX: Optional[VectorIndex] = None


def get_vector_index(embedding_model: str = "all-MiniLM-L6-v2") -> VectorIndex:
    """Get global vector index instance (singleton)."""
    global _VECTOR_INDEX
    if _VECTOR_INDEX is None:
        _VECTOR_INDEX = VectorIndex(embedding_model=embedding_model)
    return _VECTOR_INDEX


def initialize_index_from_doctrines(doctrines: list[Any]) -> None:
    """
    Initialize vector index from doctrine blocks.

    Args:
        doctrines: List of DoctrineBlock objects
    """
    index = get_vector_index()

    for doctrine in doctrines:
        # Generate document ID from topic
        doc_id = hashlib.md5(doctrine.topic.encode()).hexdigest()[:16]

        # Build searchable content from doctrine
        content_parts = [
            doctrine.topic.replace("_", " "),
            " ".join(doctrine.keywords),
            " ".join(doctrine.conclusion_templates),
            doctrine.reasoning_framework[:500],  # First 500 chars
            " ".join(doctrine.key_factors),
        ]
        content = " ".join(content_parts)

        # Extract authority level from primary_authority
        authority_level = 3  # Default mid-level
        if any("Texas Insurance Code" in auth for auth in doctrine.primary_authority):
            authority_level = 1
        elif any("TAC" in auth or "TDI" in auth for auth in doctrine.primary_authority):
            authority_level = 2
        elif any("ALTA" in auth for auth in doctrine.primary_authority):
            authority_level = 3

        # Add to index
        index.add_document(
            doc_id=doc_id,
            content=content,
            metadata={
                "topic": doctrine.topic,
                "category": doctrine.category.value,
                "confidence": doctrine.confidence.value,
                "primary_authority": doctrine.primary_authority,
            },
            category=doctrine.category.value,
            authority_level=authority_level
        )

    # Build the index
    index.build_index()
    logger.info(f"Vector index initialized with {index.get_document_count()} doctrine documents")


def search_doctrines(
    query: str,
    top_k: int = 5,
    similarity_threshold: float = 0.72,
    category_filter: Optional[str] = None
) -> SearchResponse:
    """
    Search doctrines using vector similarity.

    Args:
        query: Search query
        top_k: Max results
        similarity_threshold: Min similarity score
        category_filter: Optional category filter

    Returns:
        SearchResponse with matching doctrines
    """
    index = get_vector_index()
    return index.search(
        query=query,
        top_k=top_k,
        similarity_threshold=similarity_threshold,
        category_filter=category_filter
    )
