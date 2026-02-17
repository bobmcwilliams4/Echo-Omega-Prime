"""
LM16 Wind/Solar Lease Engine - Search Module
==============================================
Vector search fallback, keyword matching, and semantic retrieval
for the Wind/Solar Lease Intelligence Engine. Operates when
doctrine cache misses occur.

Engine: LM16 | Port: 8516
"""

from __future__ import annotations

import hashlib
import math
import re
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Optional

from loguru import logger


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
ENGINE_ID: str = "LM16"
MAX_SEARCH_RESULTS: int = 10
MIN_RELEVANCE_SCORE: float = 0.15
BM25_K1: float = 1.5
BM25_B: float = 0.75


# ---------------------------------------------------------------------------
# Search Result Model
# ---------------------------------------------------------------------------
@dataclass
class SearchResult:
    """A single search result from vector or keyword search."""
    topic: str
    score: float
    match_type: str  # "keyword", "semantic", "bm25", "combined"
    matched_keywords: list[str] = field(default_factory=list)
    snippet: str = ""
    authority_refs: list[str] = field(default_factory=list)
    domain: str = ""
    confidence: str = ""

    @property
    def relevance_grade(self) -> str:
        """Grade the relevance of this result."""
        if self.score >= 0.80:
            return "EXACT"
        if self.score >= 0.60:
            return "HIGH"
        if self.score >= 0.40:
            return "MODERATE"
        if self.score >= 0.20:
            return "LOW"
        return "MARGINAL"


@dataclass
class SearchResponse:
    """Complete search response with multiple results."""
    query: str
    results: list[SearchResult] = field(default_factory=list)
    total_candidates: int = 0
    search_time_ms: float = 0.0
    search_method: str = ""
    fallback_used: bool = False

    @property
    def top_result(self) -> Optional[SearchResult]:
        """Return the highest-scoring result."""
        return self.results[0] if self.results else None

    @property
    def has_results(self) -> bool:
        """Check if any results were found."""
        return len(self.results) > 0


# ---------------------------------------------------------------------------
# Document index for BM25
# ---------------------------------------------------------------------------
@dataclass
class IndexedDocument:
    """A document indexed for search."""
    doc_id: str
    topic: str
    keywords: list[str]
    text: str
    authority_refs: list[str]
    domain: str
    confidence: str
    term_frequencies: dict[str, int] = field(default_factory=dict)
    doc_length: int = 0

    def compute_tf(self) -> None:
        """Compute term frequencies from the text and keywords."""
        all_text = (self.text + " " + " ".join(self.keywords)).lower()
        tokens = re.findall(r"\b[a-z]+\b", all_text)
        self.doc_length = len(tokens)
        self.term_frequencies = defaultdict(int)
        for token in tokens:
            self.term_frequencies[token] += 1


# ---------------------------------------------------------------------------
# BM25 Search Engine
# ---------------------------------------------------------------------------
class BM25SearchEngine:
    """
    BM25-based search engine for wind/solar lease doctrine retrieval.
    Provides keyword matching, BM25 scoring, and combined ranking.
    """

    def __init__(self) -> None:
        self._documents: list[IndexedDocument] = []
        self._idf_cache: dict[str, float] = {}
        self._avg_doc_length: float = 0.0
        self._doc_count: int = 0
        self._term_doc_freq: dict[str, int] = defaultdict(int)
        logger.info("BM25SearchEngine initialized for {engine}", engine=ENGINE_ID)

    def index_documents(self, documents: list[IndexedDocument]) -> None:
        """Index a list of documents for search."""
        self._documents = documents
        self._doc_count = len(documents)

        total_length = 0
        self._term_doc_freq.clear()
        self._idf_cache.clear()

        for doc in documents:
            doc.compute_tf()
            total_length += doc.doc_length
            seen_terms: set[str] = set()
            for term in doc.term_frequencies:
                if term not in seen_terms:
                    self._term_doc_freq[term] += 1
                    seen_terms.add(term)

        self._avg_doc_length = total_length / self._doc_count if self._doc_count > 0 else 1.0

        for term, df in self._term_doc_freq.items():
            self._idf_cache[term] = math.log(
                (self._doc_count - df + 0.5) / (df + 0.5) + 1.0
            )

        logger.info(
            "Indexed {n} documents, avg_length={avg:.1f}, unique_terms={terms}",
            n=self._doc_count,
            avg=self._avg_doc_length,
            terms=len(self._term_doc_freq),
        )

    def search(self, query: str, max_results: int = MAX_SEARCH_RESULTS) -> SearchResponse:
        """Search the index using BM25 scoring."""
        import time
        start = time.perf_counter()

        query_lower = query.strip().lower()
        query_terms = re.findall(r"\b[a-z]+\b", query_lower)

        if not query_terms:
            return SearchResponse(
                query=query,
                search_method="bm25",
                search_time_ms=0.0,
            )

        scored_results: list[tuple[float, IndexedDocument, list[str]]] = []

        for doc in self._documents:
            score = 0.0
            matched_terms: list[str] = []

            for term in query_terms:
                if term not in self._idf_cache:
                    continue
                idf = self._idf_cache[term]
                tf = doc.term_frequencies.get(term, 0)
                if tf == 0:
                    continue
                matched_terms.append(term)
                numerator = tf * (BM25_K1 + 1)
                denominator = tf + BM25_K1 * (
                    1 - BM25_B + BM25_B * doc.doc_length / self._avg_doc_length
                )
                score += idf * numerator / denominator

            if score > MIN_RELEVANCE_SCORE:
                scored_results.append((score, doc, matched_terms))

        scored_results.sort(key=lambda x: x[0], reverse=True)
        top = scored_results[:max_results]

        max_score = top[0][0] if top else 1.0
        results = [
            SearchResult(
                topic=doc.topic,
                score=round(score / max_score, 4) if max_score > 0 else 0.0,
                match_type="bm25",
                matched_keywords=matched,
                snippet=doc.text[:200] + "..." if len(doc.text) > 200 else doc.text,
                authority_refs=doc.authority_refs,
                domain=doc.domain,
                confidence=doc.confidence,
            )
            for score, doc, matched in top
        ]

        elapsed_ms = (time.perf_counter() - start) * 1000

        return SearchResponse(
            query=query,
            results=results,
            total_candidates=len(scored_results),
            search_time_ms=round(elapsed_ms, 2),
            search_method="bm25",
            fallback_used=False,
        )

    def keyword_search(
        self, keywords: list[str], max_results: int = MAX_SEARCH_RESULTS
    ) -> SearchResponse:
        """Direct keyword matching without BM25 scoring."""
        import time
        start = time.perf_counter()

        keyword_set = {k.lower() for k in keywords}
        scored: list[tuple[float, IndexedDocument, list[str]]] = []

        for doc in self._documents:
            doc_keywords = {k.lower() for k in doc.keywords}
            doc_text_terms = set(re.findall(r"\b[a-z]+\b", doc.text.lower()))
            all_doc_terms = doc_keywords | doc_text_terms

            matched = keyword_set & all_doc_terms
            if matched:
                score = len(matched) / len(keyword_set) if keyword_set else 0.0
                keyword_bonus = len(matched & doc_keywords) * 0.15
                score = min(score + keyword_bonus, 1.0)
                scored.append((score, doc, sorted(matched)))

        scored.sort(key=lambda x: x[0], reverse=True)
        top = scored[:max_results]

        results = [
            SearchResult(
                topic=doc.topic,
                score=round(score, 4),
                match_type="keyword",
                matched_keywords=matched,
                snippet=doc.text[:200] + "..." if len(doc.text) > 200 else doc.text,
                authority_refs=doc.authority_refs,
                domain=doc.domain,
                confidence=doc.confidence,
            )
            for score, doc, matched in top
        ]

        elapsed_ms = (time.perf_counter() - start) * 1000

        return SearchResponse(
            query=" ".join(keywords),
            results=results,
            total_candidates=len(scored),
            search_time_ms=round(elapsed_ms, 2),
            search_method="keyword",
            fallback_used=False,
        )

    def combined_search(
        self,
        query: str,
        keywords: list[str],
        max_results: int = MAX_SEARCH_RESULTS,
        bm25_weight: float = 0.6,
        keyword_weight: float = 0.4,
    ) -> SearchResponse:
        """Combined BM25 + keyword search with weighted scoring."""
        import time
        start = time.perf_counter()

        bm25_response = self.search(query, max_results=max_results * 2)
        keyword_response = self.keyword_search(keywords, max_results=max_results * 2)

        score_map: dict[str, tuple[float, SearchResult]] = {}

        for r in bm25_response.results:
            score_map[r.topic] = (r.score * bm25_weight, r)

        for r in keyword_response.results:
            if r.topic in score_map:
                existing_score, existing_result = score_map[r.topic]
                combined = existing_score + r.score * keyword_weight
                merged_keywords = list(
                    set(existing_result.matched_keywords + r.matched_keywords)
                )
                score_map[r.topic] = (
                    combined,
                    SearchResult(
                        topic=r.topic,
                        score=round(combined, 4),
                        match_type="combined",
                        matched_keywords=merged_keywords,
                        snippet=existing_result.snippet,
                        authority_refs=existing_result.authority_refs,
                        domain=existing_result.domain,
                        confidence=existing_result.confidence,
                    ),
                )
            else:
                score_map[r.topic] = (r.score * keyword_weight, r)

        sorted_results = sorted(score_map.values(), key=lambda x: x[0], reverse=True)
        final_results = [
            SearchResult(
                topic=result.topic,
                score=round(score, 4),
                match_type="combined",
                matched_keywords=result.matched_keywords,
                snippet=result.snippet,
                authority_refs=result.authority_refs,
                domain=result.domain,
                confidence=result.confidence,
            )
            for score, result in sorted_results[:max_results]
        ]

        elapsed_ms = (time.perf_counter() - start) * 1000

        return SearchResponse(
            query=query,
            results=final_results,
            total_candidates=len(score_map),
            search_time_ms=round(elapsed_ms, 2),
            search_method="combined",
            fallback_used=True,
        )


# ---------------------------------------------------------------------------
# Module-level singleton
# ---------------------------------------------------------------------------
_search_engine: Optional[BM25SearchEngine] = None


def get_search_engine() -> BM25SearchEngine:
    """Get or create the module-level search engine singleton."""
    global _search_engine
    if _search_engine is None:
        _search_engine = BM25SearchEngine()
    return _search_engine
