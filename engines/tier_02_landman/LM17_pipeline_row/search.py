"""
LM17 Pipeline ROW Engine - Search Module
==========================================
Vector-less semantic search fallback for doctrine retrieval when the
doctrine cache misses. Uses keyword overlap, TF-IDF-like scoring,
and domain-weighted relevance ranking.

Engine ID: LM17 | Port: 8517
TIE Gold Standard Search Implementation
"""

from __future__ import annotations

import hashlib
import math
import re
from collections import Counter, defaultdict
from typing import Any, Optional

from loguru import logger
from pydantic import BaseModel, Field


# ============================================================================
# CONSTANTS
# ============================================================================

ENGINE_ID: str = "LM17"
DEFAULT_TOP_K: int = 5
MIN_RELEVANCE_THRESHOLD: float = 0.10

DOMAIN_BOOST_TERMS: dict[str, float] = {
    "right-of-way": 2.5,
    "easement": 2.5,
    "pipeline": 2.0,
    "ferc": 2.5,
    "eminent domain": 3.0,
    "condemnation": 2.5,
    "common carrier": 2.5,
    "crossing": 1.8,
    "hdd": 2.0,
    "horizontal directional drilling": 2.0,
    "phmsa": 2.5,
    "section 7": 2.5,
    "section 404": 2.0,
    "section 106": 2.0,
    "environmental": 1.5,
    "wetland": 2.0,
    "endangered species": 2.5,
    "cathodic protection": 2.0,
    "abandonment": 2.0,
    "surface damage": 2.0,
    "crop damage": 2.0,
    "temporary workspace": 1.8,
    "encroachment": 2.0,
    "transmission": 1.5,
    "gathering": 1.5,
    "restoration": 1.5,
    "railroad crossing": 2.0,
    "highway crossing": 2.0,
    "natural gas act": 2.5,
    "certificate": 1.8,
    "negotiation": 1.5,
    "compensation": 1.8,
    "permit": 1.5,
    "regulatory": 1.5,
}


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class SearchDocument(BaseModel):
    """A searchable document in the corpus."""
    doc_id: str
    topic: str
    category: str
    content: str
    keywords: list[str] = Field(default_factory=list)
    authority_sources: list[str] = Field(default_factory=list)
    weight: float = 1.0
    metadata: dict[str, Any] = Field(default_factory=dict)


class SearchResult(BaseModel):
    """A search result with relevance scoring."""
    doc_id: str
    topic: str
    category: str
    relevance_score: float
    matched_terms: list[str] = Field(default_factory=list)
    domain_boost_applied: float = 1.0
    snippet: str = ""
    authority_sources: list[str] = Field(default_factory=list)


class SearchResponse(BaseModel):
    """Full search response with results and metadata."""
    query: str
    query_hash: str
    total_documents: int
    results_returned: int
    results: list[SearchResult] = Field(default_factory=list)
    search_time_ms: float = 0.0


# ============================================================================
# SEARCH ENGINE
# ============================================================================

class PipelineROWSearchEngine:
    """
    Keyword-based semantic search engine for pipeline ROW doctrine retrieval.
    Implements TF-IDF-like scoring with domain-specific term boosting,
    used as a fallback when the doctrine cache does not produce a direct hit.
    """

    def __init__(self) -> None:
        self._documents: dict[str, SearchDocument] = {}
        self._inverted_index: defaultdict[str, set[str]] = defaultdict(set)
        self._doc_term_freq: dict[str, Counter] = {}
        self._idf_cache: dict[str, float] = {}
        self._total_docs: int = 0
        self._dirty: bool = False
        logger.info("PipelineROWSearchEngine initialized")

    def add_document(self, doc: SearchDocument) -> None:
        """Add a document to the search index."""
        self._documents[doc.doc_id] = doc
        terms = self._tokenize(doc.content + " " + " ".join(doc.keywords))
        term_counts = Counter(terms)
        self._doc_term_freq[doc.doc_id] = term_counts
        for term in set(terms):
            self._inverted_index[term].add(doc.doc_id)
        self._total_docs = len(self._documents)
        self._dirty = True
        logger.trace("Document added | doc_id={} topic={} terms={}", doc.doc_id, doc.topic, len(terms))

    def add_documents(self, docs: list[SearchDocument]) -> None:
        """Add multiple documents to the search index."""
        for doc in docs:
            self.add_document(doc)
        self._rebuild_idf()
        logger.info("Indexed {} documents | total={}", len(docs), self._total_docs)

    def search(
        self,
        query: str,
        top_k: int = DEFAULT_TOP_K,
        category_filter: Optional[str] = None,
        min_score: float = MIN_RELEVANCE_THRESHOLD,
    ) -> SearchResponse:
        """Search the document corpus for relevant doctrine content."""
        import time
        start = time.perf_counter()

        if self._dirty:
            self._rebuild_idf()

        query_hash = hashlib.sha256(query.lower().encode()).hexdigest()[:16]
        query_terms = self._tokenize(query)

        if not query_terms:
            return SearchResponse(
                query=query,
                query_hash=query_hash,
                total_documents=self._total_docs,
                results_returned=0,
                search_time_ms=0.0,
            )

        candidate_docs: set[str] = set()
        for term in query_terms:
            if term in self._inverted_index:
                candidate_docs |= self._inverted_index[term]

        scored_results: list[SearchResult] = []
        for doc_id in candidate_docs:
            doc = self._documents[doc_id]
            if category_filter and doc.category != category_filter:
                continue

            score, matched_terms = self._compute_relevance(query_terms, doc_id)
            domain_boost = self._apply_domain_boost(query, doc)
            final_score = score * domain_boost * doc.weight

            if final_score >= min_score:
                snippet = self._extract_snippet(doc.content, matched_terms)
                scored_results.append(SearchResult(
                    doc_id=doc_id,
                    topic=doc.topic,
                    category=doc.category,
                    relevance_score=round(final_score, 4),
                    matched_terms=matched_terms,
                    domain_boost_applied=round(domain_boost, 2),
                    snippet=snippet,
                    authority_sources=doc.authority_sources,
                ))

        scored_results.sort(key=lambda r: r.relevance_score, reverse=True)
        top_results = scored_results[:top_k]
        elapsed = (time.perf_counter() - start) * 1000.0

        logger.debug(
            "Search completed | query_hash={} candidates={} results={} elapsed_ms={:.1f}",
            query_hash, len(candidate_docs), len(top_results), elapsed,
        )

        return SearchResponse(
            query=query,
            query_hash=query_hash,
            total_documents=self._total_docs,
            results_returned=len(top_results),
            results=top_results,
            search_time_ms=round(elapsed, 3),
        )

    def _tokenize(self, text: str) -> list[str]:
        """Tokenize text into lowercase terms, removing stopwords."""
        tokens = re.findall(r"[a-zA-Z][a-zA-Z0-9-]*[a-zA-Z0-9]|[a-zA-Z]", text.lower())
        stopwords = {
            "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
            "have", "has", "had", "do", "does", "did", "will", "would", "shall",
            "should", "may", "might", "can", "could", "must", "to", "of", "in",
            "for", "on", "with", "at", "by", "from", "as", "into", "through",
            "and", "or", "but", "not", "if", "then", "that", "this", "it",
            "what", "which", "who", "how", "when", "where", "why",
        }
        return [t for t in tokens if t not in stopwords and len(t) > 1]

    def _compute_relevance(self, query_terms: list[str], doc_id: str) -> tuple[float, list[str]]:
        """Compute TF-IDF-like relevance score for a document."""
        doc_tf = self._doc_term_freq.get(doc_id, Counter())
        score = 0.0
        matched: list[str] = []
        for term in query_terms:
            tf = doc_tf.get(term, 0)
            if tf > 0:
                idf = self._idf_cache.get(term, 1.0)
                term_score = (1 + math.log(tf)) * idf
                score += term_score
                if term not in matched:
                    matched.append(term)
        if query_terms:
            score /= len(query_terms)
        return score, matched

    def _apply_domain_boost(self, query: str, doc: SearchDocument) -> float:
        """Apply domain-specific term boosting."""
        boost = 1.0
        query_lower = query.lower()
        for term, multiplier in DOMAIN_BOOST_TERMS.items():
            if term in query_lower and term in doc.content.lower():
                boost = max(boost, multiplier)
        return boost

    def _extract_snippet(self, content: str, matched_terms: list[str], max_length: int = 200) -> str:
        """Extract a relevant snippet from document content around matched terms."""
        if not matched_terms or not content:
            return content[:max_length] if content else ""
        content_lower = content.lower()
        best_pos = 0
        best_density = 0
        window = max_length
        for i in range(0, len(content) - window + 1, 20):
            chunk = content_lower[i:i + window]
            density = sum(1 for t in matched_terms if t in chunk)
            if density > best_density:
                best_density = density
                best_pos = i
        start = max(0, best_pos)
        end = min(len(content), start + max_length)
        snippet = content[start:end].strip()
        if start > 0:
            snippet = "..." + snippet
        if end < len(content):
            snippet = snippet + "..."
        return snippet

    def _rebuild_idf(self) -> None:
        """Rebuild the IDF cache for all indexed terms."""
        self._idf_cache.clear()
        for term, doc_set in self._inverted_index.items():
            df = len(doc_set)
            if df > 0:
                self._idf_cache[term] = math.log(self._total_docs / df) + 1.0
        self._dirty = False
        logger.trace("IDF cache rebuilt | terms={}", len(self._idf_cache))

    def get_index_stats(self) -> dict[str, Any]:
        """Return statistics about the search index."""
        return {
            "total_documents": self._total_docs,
            "unique_terms": len(self._inverted_index),
            "avg_terms_per_doc": (
                sum(len(c) for c in self._doc_term_freq.values()) / self._total_docs
                if self._total_docs > 0 else 0
            ),
            "categories": list(set(d.category for d in self._documents.values())),
        }

    def clear(self) -> None:
        """Clear all indexed documents."""
        self._documents.clear()
        self._inverted_index.clear()
        self._doc_term_freq.clear()
        self._idf_cache.clear()
        self._total_docs = 0
        self._dirty = False
        logger.warning("Search index cleared")
