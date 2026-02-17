"""
LM08 Due Diligence Engine - Search Module
===========================================
Vector search and semantic retrieval for due diligence doctrine cache misses.
Provides fallback when doctrine cache does not contain a direct hit.
"""

from __future__ import annotations

import hashlib
import math
import re
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from loguru import logger


@dataclass
class SearchResult:
    """Single search result with relevance scoring."""
    doc_id: str
    title: str
    content: str
    score: float
    domain: str
    keywords_matched: List[str] = field(default_factory=list)
    source: str = "vector_search"
    latency_ms: float = 0.0
    determinism_hash: str = ""

    def __post_init__(self) -> None:
        raw = f"{self.doc_id}|{self.title}|{self.score}"
        self.determinism_hash = hashlib.sha256(raw.encode()).hexdigest()[:16]


@dataclass
class SearchQuery:
    """Structured search query with filters."""
    text: str
    domain_filter: Optional[str] = None
    min_score: float = 0.3
    max_results: int = 10
    include_metadata: bool = True


class TFIDFIndex:
    """Simple TF-IDF index for doctrine search when vector DB not available."""

    def __init__(self) -> None:
        self._documents: Dict[str, Dict[str, Any]] = {}
        self._idf_cache: Dict[str, float] = {}
        self._term_doc_count: Dict[str, int] = {}
        self._total_docs: int = 0
        logger.info("TFIDFIndex initialized")

    def add_document(self, doc_id: str, title: str, content: str, domain: str, metadata: Optional[Dict] = None) -> None:
        """Index a document for search."""
        tokens = self._tokenize(f"{title} {content}")
        tf: Dict[str, float] = {}
        for token in tokens:
            tf[token] = tf.get(token, 0) + 1
        total_terms = len(tokens)
        if total_terms > 0:
            for token in tf:
                tf[token] /= total_terms

        unique_tokens = set(tokens)
        for token in unique_tokens:
            self._term_doc_count[token] = self._term_doc_count.get(token, 0) + 1

        self._documents[doc_id] = {
            "title": title,
            "content": content,
            "domain": domain,
            "tokens": tokens,
            "tf": tf,
            "unique_tokens": unique_tokens,
            "metadata": metadata or {},
        }
        self._total_docs += 1
        self._idf_cache.clear()

    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text into normalized terms."""
        text = text.lower()
        text = re.sub(r"[^a-z0-9\s]", " ", text)
        tokens = text.split()
        stopwords = {
            "the", "a", "an", "is", "are", "was", "were", "be", "been",
            "being", "have", "has", "had", "do", "does", "did", "will",
            "would", "could", "should", "may", "might", "shall", "can",
            "of", "in", "to", "for", "with", "on", "at", "by", "from",
            "as", "into", "through", "during", "before", "after", "and",
            "but", "or", "nor", "not", "so", "yet", "both", "either",
            "neither", "each", "every", "all", "any", "few", "more",
            "most", "other", "some", "such", "no", "only", "own",
            "same", "than", "too", "very", "just", "because", "if",
            "when", "where", "how", "what", "which", "who", "whom",
            "this", "that", "these", "those", "it", "its",
        }
        return [t for t in tokens if t not in stopwords and len(t) > 1]

    def _compute_idf(self, term: str) -> float:
        """Compute inverse document frequency for a term."""
        if term in self._idf_cache:
            return self._idf_cache[term]
        doc_count = self._term_doc_count.get(term, 0)
        if doc_count == 0:
            idf = 0.0
        else:
            idf = math.log(self._total_docs / doc_count) + 1.0
        self._idf_cache[term] = idf
        return idf

    def search(self, query: SearchQuery) -> List[SearchResult]:
        """Search the index using TF-IDF scoring."""
        start = time.perf_counter()
        query_tokens = self._tokenize(query.text)
        if not query_tokens:
            return []

        results: List[SearchResult] = []
        for doc_id, doc in self._documents.items():
            if query.domain_filter and doc["domain"] != query.domain_filter:
                continue

            score = 0.0
            matched_keywords: List[str] = []
            for token in query_tokens:
                tf = doc["tf"].get(token, 0.0)
                idf = self._compute_idf(token)
                token_score = tf * idf
                if token_score > 0:
                    score += token_score
                    matched_keywords.append(token)

            if score >= query.min_score and matched_keywords:
                latency = (time.perf_counter() - start) * 1000
                results.append(SearchResult(
                    doc_id=doc_id,
                    title=doc["title"],
                    content=doc["content"][:500],
                    score=round(score, 4),
                    domain=doc["domain"],
                    keywords_matched=matched_keywords,
                    latency_ms=round(latency, 2),
                ))

        results.sort(key=lambda r: r.score, reverse=True)
        return results[:query.max_results]

    def get_stats(self) -> Dict[str, Any]:
        """Return index statistics."""
        domain_counts: Dict[str, int] = {}
        for doc in self._documents.values():
            d = doc["domain"]
            domain_counts[d] = domain_counts.get(d, 0) + 1
        return {
            "total_documents": self._total_docs,
            "unique_terms": len(self._term_doc_count),
            "domains": domain_counts,
        }


class DueDiligenceSearchEngine:
    """Search engine for due diligence doctrine retrieval."""

    def __init__(self) -> None:
        self._index = TFIDFIndex()
        self._query_count = 0
        self._total_latency_ms = 0.0
        self._cache_hits = 0
        self._result_cache: Dict[str, List[SearchResult]] = {}
        logger.info("DueDiligenceSearchEngine initialized")

    def index_doctrine(self, doc_id: str, title: str, content: str, domain: str, metadata: Optional[Dict] = None) -> None:
        """Add a doctrine block to the search index."""
        self._index.add_document(doc_id, title, content, domain, metadata)
        self._result_cache.clear()

    def search(self, query_text: str, domain: Optional[str] = None, max_results: int = 10, min_score: float = 0.3) -> List[SearchResult]:
        """Search for relevant doctrine blocks."""
        cache_key = f"{query_text}|{domain}|{max_results}|{min_score}"
        if cache_key in self._result_cache:
            self._cache_hits += 1
            return self._result_cache[cache_key]

        self._query_count += 1
        sq = SearchQuery(
            text=query_text,
            domain_filter=domain,
            min_score=min_score,
            max_results=max_results,
        )
        results = self._index.search(sq)
        total_latency = sum(r.latency_ms for r in results) if results else 0.0
        self._total_latency_ms += total_latency
        self._result_cache[cache_key] = results

        logger.debug(
            "Search completed | query='{}' | results={} | latency={:.2f}ms",
            query_text[:60], len(results), total_latency,
        )
        return results

    def bulk_index(self, documents: List[Dict[str, str]]) -> int:
        """Index multiple documents at once."""
        count = 0
        for doc in documents:
            self._index.add_document(
                doc_id=doc.get("doc_id", f"doc_{count}"),
                title=doc.get("title", ""),
                content=doc.get("content", ""),
                domain=doc.get("domain", "general"),
                metadata=doc.get("metadata"),
            )
            count += 1
        self._result_cache.clear()
        logger.info("Bulk indexed {} documents", count)
        return count

    def get_metrics(self) -> Dict[str, Any]:
        """Return search engine metrics."""
        avg_latency = (self._total_latency_ms / self._query_count) if self._query_count > 0 else 0.0
        return {
            "total_queries": self._query_count,
            "cache_hits": self._cache_hits,
            "cache_hit_rate": round(self._cache_hits / max(self._query_count, 1), 3),
            "average_latency_ms": round(avg_latency, 2),
            "index_stats": self._index.get_stats(),
        }

    def clear_cache(self) -> None:
        """Clear the result cache."""
        self._result_cache.clear()
        logger.info("Search cache cleared")
