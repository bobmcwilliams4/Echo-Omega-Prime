"""
R01_rrc_parser Vector Search — Semantic fallback when doctrine cache misses

Provides vector-based semantic search as fallback tier when keyword-based
doctrine cache lookup returns insufficient results.
"""

from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass
from typing import Dict, List, Optional

from loguru import logger
from pydantic import BaseModel


@dataclass
class VectorResult:
    """Single vector search result."""
    id: str
    text: str
    score: float
    metadata: Dict[str, str]


class VectorSearch:
    """
    Lightweight vector search for RRC doctrine retrieval.

    In no-LLM mode, uses simple TF-IDF + cosine similarity as semantic fallback.
    Can be upgraded to use Cognition Cloud embedding pipeline if needed.
    """

    def __init__(self) -> None:
        self._cache: Dict[str, List[VectorResult]] = {}
        self._query_count = 0

        # Simplified TF-IDF vocabulary (RRC-specific terms)
        self._vocabulary = [
            "permit", "drill", "drilling", "completion", "production", "report",
            "well", "lease", "operator", "plugging", "casing", "cement", "injection",
            "disposal", "saltwater", "horizontal", "lateral", "spacing", "density",
            "allowable", "proration", "rule", "violation", "penalty", "bond",
            "pipeline", "permit", "h2s", "hydrogen", "sulfide", "gas", "oil",
            "formation", "zone", "depth", "pressure", "test", "survey", "log",
            "texas", "railroad", "commission", "rrc", "statute", "code", "tac",
        ]

        logger.info(f"VectorSearch initialized with {len(self._vocabulary)} terms")

    async def search(
        self,
        query: str,
        top_k: int = 10,
        use_cloud: bool = False,
    ) -> List[VectorResult]:
        """
        Semantic search for RRC doctrines.

        Args:
            query: Search query text
            top_k: Number of results to return
            use_cloud: If True, use Cognition Cloud embedding pipeline (requires cloud_retriever)

        Returns:
            List of VectorResult objects ranked by relevance
        """
        self._query_count += 1

        # Check cache
        cache_key = self._hash_query(query, top_k)
        if cache_key in self._cache:
            logger.debug(f"Vector search cache hit for query: {query[:50]}...")
            return self._cache[cache_key]

        # Simple TF-IDF scoring (no-LLM mode)
        results = self._tfidf_search(query, top_k)

        # Cache results
        self._cache[cache_key] = results

        logger.debug(f"Vector search returned {len(results)} results for query: {query[:50]}...")
        return results

    def _tfidf_search(self, query: str, top_k: int) -> List[VectorResult]:
        """
        Simple TF-IDF search over vocabulary.

        In production, this would search against doctrine blocks or cloud embeddings.
        For now, returns mock results based on keyword presence.
        """
        query_lower = query.lower()
        query_tokens = set(query_lower.split())

        # Score based on vocabulary term presence
        scores: Dict[str, float] = {}
        for term in self._vocabulary:
            if term in query_tokens or term in query_lower:
                scores[term] = 1.0 / (1 + query_lower.index(term))

        # Convert to results (mock data for now)
        results: List[VectorResult] = []
        for i, (term, score) in enumerate(sorted(scores.items(), key=lambda x: -x[1])[:top_k]):
            results.append(VectorResult(
                id=f"vector_{i}",
                text=f"RRC doctrine related to {term}",
                score=score,
                metadata={"term": term, "source": "tfidf"},
            ))

        return results

    def _hash_query(self, query: str, top_k: int) -> str:
        """Generate cache key for query."""
        raw = f"{query}|{top_k}"
        return hashlib.md5(raw.encode()).hexdigest()

    @property
    def stats(self) -> Dict[str, int]:
        """Return search statistics."""
        return {
            "query_count": self._query_count,
            "cache_size": len(self._cache),
        }
