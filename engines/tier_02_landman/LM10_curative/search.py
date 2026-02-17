"""
LM10 Curative Engine — Search Module
======================================
Vector search and semantic retrieval fallback for curative title queries.
Uses sentence-transformers for embedding generation and cosine similarity
for matching against the indexed doctrine corpus.

Engine: LM10 | Port: 8510 | Domain: title_curative
"""

from __future__ import annotations

import hashlib
import json
import math
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

from loguru import logger
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
ENGINE_ID = "LM10"
DEFAULT_SIMILARITY_THRESHOLD = 0.72
MAX_RESULTS = 10
EMBEDDING_DIM = 384  # all-MiniLM-L6-v2 output dimension
INDEX_PATH = Path(__file__).parent / "vector_index"


# ---------------------------------------------------------------------------
# Pydantic Models
# ---------------------------------------------------------------------------
class SearchDocument(BaseModel):
    """A document indexed for vector search."""
    doc_id: str
    topic: str
    content: str
    category: str = ""
    authority_sources: list[str] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)
    embedding: list[float] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class SearchResult(BaseModel):
    """A single search result with similarity score."""
    doc_id: str
    topic: str
    content: str
    category: str = ""
    similarity: float = 0.0
    authority_sources: list[str] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class SearchResponse(BaseModel):
    """Response from a vector search query."""
    query: str
    query_hash: str
    results: list[SearchResult] = Field(default_factory=list)
    total_candidates: int = 0
    search_time_ms: float = 0.0
    threshold_used: float = DEFAULT_SIMILARITY_THRESHOLD
    embedding_time_ms: float = 0.0


# ---------------------------------------------------------------------------
# Cosine Similarity (pure Python — no numpy dependency required)
# ---------------------------------------------------------------------------
def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    """Compute cosine similarity between two vectors."""
    if len(vec_a) != len(vec_b) or len(vec_a) == 0:
        return 0.0
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    magnitude_a = math.sqrt(sum(a * a for a in vec_a))
    magnitude_b = math.sqrt(sum(b * b for b in vec_b))
    if magnitude_a == 0.0 or magnitude_b == 0.0:
        return 0.0
    return dot_product / (magnitude_a * magnitude_b)


def normalize_vector(vec: list[float]) -> list[float]:
    """L2-normalize a vector."""
    magnitude = math.sqrt(sum(v * v for v in vec))
    if magnitude == 0.0:
        return vec
    return [v / magnitude for v in vec]


# ---------------------------------------------------------------------------
# Lightweight Keyword Embedding (fallback when sentence-transformers unavailable)
# ---------------------------------------------------------------------------
class KeywordEmbedder:
    """
    Deterministic keyword-based embedding fallback.
    Uses term frequency hashing to produce a fixed-dimension pseudo-embedding.
    This ensures the engine can operate without GPU or sentence-transformers.
    """

    def __init__(self, dim: int = EMBEDDING_DIM) -> None:
        self._dim = dim

    def embed(self, text: str) -> list[float]:
        """Generate a deterministic pseudo-embedding from text."""
        tokens = text.lower().split()
        vec = [0.0] * self._dim
        for token in tokens:
            token_hash = int(hashlib.md5(token.encode()).hexdigest(), 16)
            idx = token_hash % self._dim
            sign = 1.0 if (token_hash // self._dim) % 2 == 0 else -1.0
            vec[idx] += sign
        return normalize_vector(vec)

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Embed multiple texts."""
        return [self.embed(t) for t in texts]


# ---------------------------------------------------------------------------
# Embedding Provider
# ---------------------------------------------------------------------------
class EmbeddingProvider:
    """
    Manages embedding generation. Attempts to use sentence-transformers
    if available, otherwise falls back to KeywordEmbedder.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2") -> None:
        self._model_name = model_name
        self._model: Any = None
        self._fallback = KeywordEmbedder(dim=EMBEDDING_DIM)
        self._using_transformers = False
        self._load_model()

    def _load_model(self) -> None:
        """Attempt to load sentence-transformers model."""
        try:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer(self._model_name)
            self._using_transformers = True
            logger.info("Loaded sentence-transformers model: {}", self._model_name)
        except ImportError:
            logger.warning(
                "sentence-transformers not available, using KeywordEmbedder fallback"
            )
            self._using_transformers = False
        except Exception as exc:
            logger.warning(
                "Failed to load sentence-transformers ({}), using fallback",
                exc,
            )
            self._using_transformers = False

    def embed(self, text: str) -> list[float]:
        """Generate embedding for a single text."""
        if self._using_transformers and self._model is not None:
            embedding = self._model.encode(text, normalize_embeddings=True)
            return embedding.tolist()
        return self._fallback.embed(text)

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple texts."""
        if self._using_transformers and self._model is not None:
            embeddings = self._model.encode(texts, normalize_embeddings=True)
            return embeddings.tolist()
        return self._fallback.embed_batch(texts)

    @property
    def is_using_transformers(self) -> bool:
        """Whether real sentence-transformers are active."""
        return self._using_transformers


# ---------------------------------------------------------------------------
# Vector Index
# ---------------------------------------------------------------------------
class VectorIndex:
    """
    In-memory vector index for curative doctrine search.
    Supports add, search, persist, and load operations.
    """

    def __init__(self, embedding_provider: Optional[EmbeddingProvider] = None) -> None:
        self._embedder = embedding_provider or EmbeddingProvider()
        self._documents: dict[str, SearchDocument] = {}
        self._index_path = INDEX_PATH
        self._index_path.mkdir(parents=True, exist_ok=True)

    def add_document(self, doc: SearchDocument) -> None:
        """Add a document to the index, generating embedding if missing."""
        if not doc.embedding:
            combined_text = f"{doc.topic} {doc.content} {' '.join(doc.keywords)}"
            doc.embedding = self._embedder.embed(combined_text)
        self._documents[doc.doc_id] = doc

    def add_documents(self, docs: list[SearchDocument]) -> int:
        """Add multiple documents, returning count added."""
        for doc in docs:
            self.add_document(doc)
        return len(docs)

    def search(
        self,
        query: str,
        threshold: float = DEFAULT_SIMILARITY_THRESHOLD,
        max_results: int = MAX_RESULTS,
        category_filter: Optional[str] = None,
    ) -> SearchResponse:
        """Search the index for documents similar to the query."""
        start_time = time.time()
        query_hash = hashlib.sha256(query.encode()).hexdigest()[:16]

        embed_start = time.time()
        query_embedding = self._embedder.embed(query)
        embedding_time_ms = (time.time() - embed_start) * 1000.0

        candidates: list[tuple[float, SearchDocument]] = []
        for doc in self._documents.values():
            if category_filter and doc.category != category_filter:
                continue
            if not doc.embedding:
                continue
            sim = cosine_similarity(query_embedding, doc.embedding)
            if sim >= threshold:
                candidates.append((sim, doc))

        candidates.sort(key=lambda x: x[0], reverse=True)
        top_results = candidates[:max_results]

        results = [
            SearchResult(
                doc_id=doc.doc_id,
                topic=doc.topic,
                content=doc.content,
                category=doc.category,
                similarity=round(sim, 4),
                authority_sources=doc.authority_sources,
                keywords=doc.keywords,
                metadata=doc.metadata,
            )
            for sim, doc in top_results
        ]

        search_time_ms = (time.time() - start_time) * 1000.0

        logger.debug(
            "Vector search | query_hash={} | candidates={}/{} | results={} | time={:.1f}ms",
            query_hash,
            len(candidates),
            len(self._documents),
            len(results),
            search_time_ms,
        )

        return SearchResponse(
            query=query[:200],
            query_hash=query_hash,
            results=results,
            total_candidates=len(candidates),
            search_time_ms=round(search_time_ms, 2),
            threshold_used=threshold,
            embedding_time_ms=round(embedding_time_ms, 2),
        )

    def save_index(self, path: Optional[Path] = None) -> Path:
        """Persist the index to disk."""
        save_path = path or (self._index_path / "index.json")
        data = {
            doc_id: doc.model_dump()
            for doc_id, doc in self._documents.items()
        }
        save_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        logger.info("Vector index saved | docs={} | path={}", len(data), save_path)
        return save_path

    def load_index(self, path: Optional[Path] = None) -> int:
        """Load index from disk, returning count loaded."""
        load_path = path or (self._index_path / "index.json")
        if not load_path.exists():
            logger.warning("No index file found at {}", load_path)
            return 0
        try:
            data = json.loads(load_path.read_text(encoding="utf-8"))
            for doc_id, doc_data in data.items():
                self._documents[doc_id] = SearchDocument(**doc_data)
            logger.info("Vector index loaded | docs={} | path={}", len(data), load_path)
            return len(data)
        except Exception as exc:
            logger.error("Failed to load vector index: {}", exc)
            return 0

    @property
    def document_count(self) -> int:
        """Number of documents in the index."""
        return len(self._documents)

    def get_stats(self) -> dict[str, Any]:
        """Get index statistics."""
        categories: dict[str, int] = {}
        for doc in self._documents.values():
            cat = doc.category or "uncategorized"
            categories[cat] = categories.get(cat, 0) + 1
        return {
            "total_documents": len(self._documents),
            "using_transformers": self._embedder.is_using_transformers,
            "embedding_dim": EMBEDDING_DIM,
            "categories": categories,
        }


# ---------------------------------------------------------------------------
# Module-level factory
# ---------------------------------------------------------------------------
_index: Optional[VectorIndex] = None


def get_vector_index() -> VectorIndex:
    """Get or create the singleton vector index."""
    global _index
    if _index is None:
        _index = VectorIndex()
    return _index


def reset_vector_index() -> None:
    """Reset the singleton (for testing)."""
    global _index
    _index = None
