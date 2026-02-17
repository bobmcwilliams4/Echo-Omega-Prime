"""
LM22 Coal/Mineral Specific — High-Performance Search Module
Vector search fallback and keyword search for doctrine retrieval.

Author: ECHO OMEGA PRIME
Engine: LM22 Coal/Mineral Specific
"""

import math
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from loguru import logger

from doctrines import DoctrineBlock, ALL_DOCTRINES, get_all_doctrines


# ==============================================================================
# SEARCH RESULT MODEL
# ==============================================================================

@dataclass
class SearchResult:
    """A ranked search result from doctrine retrieval."""
    doctrine: DoctrineBlock
    relevance_score: float
    match_source: str  # "keyword", "topic", "conclusion", "authority", "framework"
    matched_terms: List[str] = field(default_factory=list)
    latency_ms: float = 0.0


# ==============================================================================
# TF-IDF LIGHTWEIGHT VECTOR SEARCH
# ==============================================================================

class DoctrineSearchEngine:
    """
    Lightweight search engine for coal/mineral doctrine retrieval.
    Uses TF-IDF-like scoring without external dependencies.
    Falls back to keyword matching when vector search is unavailable.
    """

    def __init__(self) -> None:
        self._doctrines: List[DoctrineBlock] = get_all_doctrines()
        self._index: Dict[str, Dict[int, float]] = {}  # term -> {doc_idx -> tf-idf}
        self._doc_count: int = len(self._doctrines)
        self._query_count: int = 0
        self._total_latency_ms: float = 0.0
        self._build_index()

    def _tokenize(self, text: str) -> List[str]:
        """Simple whitespace + punctuation tokenizer."""
        clean = text.lower()
        for ch in ".,;:!?()[]{}\"'/\\-—–_":
            clean = clean.replace(ch, " ")
        tokens = [t.strip() for t in clean.split() if len(t.strip()) >= 2]
        return tokens

    def _build_index(self) -> None:
        """Build inverted index with TF-IDF scores."""
        start = time.perf_counter()
        doc_freq: Dict[str, int] = {}  # term -> number of docs containing term
        doc_term_freq: List[Dict[str, int]] = []  # per-doc term frequencies

        for doctrine in self._doctrines:
            # Combine all searchable text fields with weights
            text_parts = [
                doctrine.topic * 3,  # Weight topic heavily
                " ".join(doctrine.keywords) * 2,  # Weight keywords
                doctrine.conclusion_template,
                doctrine.reasoning_framework,
                " ".join(doctrine.key_factors),
                " ".join(doctrine.primary_authority),
                doctrine.adversary_position,
                " ".join(doctrine.counter_arguments),
                doctrine.resolution_strategy,
            ]
            full_text = " ".join(text_parts)
            tokens = self._tokenize(full_text)

            term_freq: Dict[str, int] = {}
            for token in tokens:
                term_freq[token] = term_freq.get(token, 0) + 1

            doc_term_freq.append(term_freq)
            for term in set(tokens):
                doc_freq[term] = doc_freq.get(term, 0) + 1

        # Calculate TF-IDF scores
        for doc_idx, tf_map in enumerate(doc_term_freq):
            max_tf = max(tf_map.values()) if tf_map else 1
            for term, freq in tf_map.items():
                tf = 0.5 + 0.5 * (freq / max_tf)  # Augmented TF
                idf = math.log((self._doc_count + 1) / (doc_freq.get(term, 0) + 1)) + 1
                tfidf = tf * idf
                if term not in self._index:
                    self._index[term] = {}
                self._index[term][doc_idx] = tfidf

        elapsed = (time.perf_counter() - start) * 1000
        logger.info(f"Search index built: {len(self._index)} terms, {self._doc_count} docs, {elapsed:.1f}ms")

    def search(self, query: str, top_k: int = 5, min_score: float = 0.1) -> List[SearchResult]:
        """
        Search doctrines using TF-IDF similarity scoring.
        Returns top_k results above min_score threshold.
        """
        start = time.perf_counter()
        query_tokens = self._tokenize(query)

        if not query_tokens:
            return []

        # Score each document
        doc_scores: Dict[int, float] = {}
        matched_terms_per_doc: Dict[int, List[str]] = {}

        for token in query_tokens:
            if token in self._index:
                for doc_idx, tfidf in self._index[token].items():
                    doc_scores[doc_idx] = doc_scores.get(doc_idx, 0.0) + tfidf
                    if doc_idx not in matched_terms_per_doc:
                        matched_terms_per_doc[doc_idx] = []
                    if token not in matched_terms_per_doc[doc_idx]:
                        matched_terms_per_doc[doc_idx].append(token)

        # Also do direct keyword matching against doctrine keywords list
        for idx, doctrine in enumerate(self._doctrines):
            keyword_bonus = 0.0
            for kw in doctrine.keywords:
                kw_lower = kw.lower()
                for qt in query_tokens:
                    if qt in kw_lower or kw_lower in query.lower():
                        keyword_bonus += 2.0
                        if idx not in matched_terms_per_doc:
                            matched_terms_per_doc[idx] = []
                        if kw not in matched_terms_per_doc[idx]:
                            matched_terms_per_doc[idx].append(kw)
            if keyword_bonus > 0:
                doc_scores[idx] = doc_scores.get(idx, 0.0) + keyword_bonus

        # Topic exact match bonus
        for idx, doctrine in enumerate(self._doctrines):
            topic_lower = doctrine.topic.lower().replace("_", " ")
            if any(qt in topic_lower for qt in query_tokens):
                doc_scores[idx] = doc_scores.get(idx, 0.0) + 5.0

        # Sort by score descending
        ranked = sorted(doc_scores.items(), key=lambda x: -x[1])

        # Normalize scores to 0-1 range
        max_score = ranked[0][1] if ranked else 1.0
        if max_score == 0:
            max_score = 1.0

        results: List[SearchResult] = []
        for doc_idx, raw_score in ranked[:top_k]:
            normalized = round(raw_score / max_score, 4)
            if normalized < min_score:
                break

            doctrine = self._doctrines[doc_idx]
            match_source = self._determine_match_source(query_tokens, doctrine)

            results.append(SearchResult(
                doctrine=doctrine,
                relevance_score=normalized,
                match_source=match_source,
                matched_terms=matched_terms_per_doc.get(doc_idx, []),
                latency_ms=0.0,  # Set below
            ))

        elapsed = (time.perf_counter() - start) * 1000
        self._query_count += 1
        self._total_latency_ms += elapsed

        for r in results:
            r.latency_ms = round(elapsed, 2)

        logger.debug(f"Search '{query}' → {len(results)} results in {elapsed:.1f}ms")
        return results

    def _determine_match_source(self, query_tokens: List[str], doctrine: DoctrineBlock) -> str:
        """Determine primary match source for a doctrine result."""
        topic_lower = doctrine.topic.lower().replace("_", " ")
        if any(qt in topic_lower for qt in query_tokens):
            return "topic"

        for kw in doctrine.keywords:
            if any(qt in kw.lower() for qt in query_tokens):
                return "keyword"

        conclusion_lower = doctrine.conclusion_template.lower()
        if any(qt in conclusion_lower for qt in query_tokens):
            return "conclusion"

        authority_text = " ".join(doctrine.primary_authority).lower()
        if any(qt in authority_text for qt in query_tokens):
            return "authority"

        return "framework"

    def get_stats(self) -> Dict[str, float]:
        """Return search engine statistics."""
        avg_latency = (self._total_latency_ms / max(self._query_count, 1))
        return {
            "index_terms": len(self._index),
            "indexed_docs": self._doc_count,
            "queries_served": self._query_count,
            "avg_latency_ms": round(avg_latency, 2),
            "total_latency_ms": round(self._total_latency_ms, 2),
        }


# ==============================================================================
# MODULE-LEVEL SEARCH ENGINE INSTANCE
# ==============================================================================

_search_engine: Optional[DoctrineSearchEngine] = None


def get_search_engine() -> DoctrineSearchEngine:
    """Get or create the singleton search engine instance."""
    global _search_engine
    if _search_engine is None:
        _search_engine = DoctrineSearchEngine()
    return _search_engine


def search_doctrines(query: str, top_k: int = 5) -> List[SearchResult]:
    """Convenience function: search doctrines using the singleton engine."""
    engine = get_search_engine()
    return engine.search(query, top_k=top_k)


def get_search_stats() -> Dict[str, float]:
    """Convenience function: get search engine stats."""
    engine = get_search_engine()
    return engine.get_stats()
