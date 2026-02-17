"""
TX13 Real Estate Tax Engine - Search Module
Vector-based semantic retrieval fallback for cache misses.

When the doctrine cache does not produce a direct hit, this module
performs semantic search across all doctrine blocks to find the
best-matching content for the query.

Author: ECHO OMEGA PRIME
Engine: TX13 Real Estate Tax
"""

from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from loguru import logger


# =============================================================================
# SEARCH RESULT MODEL
# =============================================================================

@dataclass
class SearchResult:
    """A ranked search result from semantic retrieval."""
    doctrine_topic: str
    score: float
    matched_keywords: List[str] = field(default_factory=list)
    irc_sections: List[str] = field(default_factory=list)
    confidence_tier: str = "DEFENSIBLE"
    snippet: str = ""
    reasoning_preview: str = ""


@dataclass
class SearchContext:
    """Context for a search operation."""
    query: str
    normalized_query: str = ""
    detected_topics: List[str] = field(default_factory=list)
    extracted_irc: List[str] = field(default_factory=list)
    property_types: List[str] = field(default_factory=list)
    question_type: str = "general"
    max_results: int = 5
    min_score: float = 0.1


# =============================================================================
# TF-IDF VECTOR SEARCH ENGINE
# =============================================================================

class RealEstateSearchEngine:
    """
    Lightweight TF-IDF based search engine for doctrine retrieval.

    No external dependencies (no numpy, no sklearn). Pure Python
    implementation optimized for the ~55 doctrine block corpus.
    Fast enough for real-time retrieval on small corpora.
    """

    def __init__(self) -> None:
        self._documents: Dict[str, Dict[str, Any]] = {}
        self._idf_cache: Dict[str, float] = {}
        self._doc_vectors: Dict[str, Dict[str, float]] = {}
        self._total_docs: int = 0
        self._vocabulary: set = set()
        self._built: bool = False
        logger.info("TX13 SearchEngine initialized")

    def index_doctrine(
        self,
        topic: str,
        keywords: List[str],
        conclusion_template: str,
        reasoning_framework: str,
        irc_sections: List[str],
        confidence_tier: str = "DEFENSIBLE",
        additional_text: str = "",
    ) -> None:
        """Index a doctrine block for search."""
        combined_text = " ".join([
            topic.replace("_", " "),
            " ".join(keywords),
            conclusion_template,
            reasoning_framework[:500],
            additional_text,
            " ".join(irc_sections),
        ]).lower()

        tokens = self._tokenize(combined_text)
        tf = Counter(tokens)
        total_tokens = len(tokens) if tokens else 1

        self._documents[topic] = {
            "keywords": keywords,
            "tokens": tokens,
            "tf": {t: c / total_tokens for t, c in tf.items()},
            "irc_sections": irc_sections,
            "confidence_tier": confidence_tier,
            "conclusion_preview": conclusion_template[:200],
            "reasoning_preview": reasoning_framework[:200],
        }
        self._vocabulary.update(tokens)
        self._total_docs += 1
        self._built = False

    def build_index(self) -> None:
        """Build IDF values and document vectors. Call after all indexing."""
        if self._total_docs == 0:
            logger.warning("No documents indexed, cannot build search index")
            return

        self._idf_cache = {}
        for term in self._vocabulary:
            doc_freq = sum(
                1 for doc in self._documents.values()
                if term in doc["tf"]
            )
            self._idf_cache[term] = math.log(
                (self._total_docs + 1) / (doc_freq + 1)
            ) + 1.0

        self._doc_vectors = {}
        for topic, doc in self._documents.items():
            vector: Dict[str, float] = {}
            for term, tf_val in doc["tf"].items():
                idf_val = self._idf_cache.get(term, 1.0)
                vector[term] = tf_val * idf_val
            self._doc_vectors[topic] = vector

        self._built = True
        logger.info(
            "Search index built | docs={} vocabulary={}",
            self._total_docs, len(self._vocabulary),
        )

    def search(self, context: SearchContext) -> List[SearchResult]:
        """Search for relevant doctrine blocks."""
        if not self._built:
            self.build_index()

        if not self._documents:
            return []

        query_text = f"{context.normalized_query} {context.query}".lower()
        query_tokens = self._tokenize(query_text)

        if context.detected_topics:
            for topic in context.detected_topics:
                query_tokens.extend(self._tokenize(topic.replace("_", " ")))

        if context.extracted_irc:
            for irc in context.extracted_irc:
                query_tokens.extend(self._tokenize(irc))

        query_tf = Counter(query_tokens)
        total_q = len(query_tokens) if query_tokens else 1
        query_vector: Dict[str, float] = {}
        for term, count in query_tf.items():
            tf_val = count / total_q
            idf_val = self._idf_cache.get(term, 1.0)
            query_vector[term] = tf_val * idf_val

        results: List[SearchResult] = []
        for topic, doc_vector in self._doc_vectors.items():
            score = self._cosine_similarity(query_vector, doc_vector)

            irc_boost = self._irc_boost(context.extracted_irc, self._documents[topic]["irc_sections"])
            score += irc_boost

            keyword_matches = [
                kw for kw in self._documents[topic]["keywords"]
                if kw.lower() in query_text
            ]
            if keyword_matches:
                score += 0.1 * len(keyword_matches)

            if context.property_types:
                doc_text = " ".join(self._documents[topic]["tokens"])
                for pt in context.property_types:
                    if pt.replace("_", " ") in doc_text:
                        score += 0.05

            if score >= context.min_score:
                results.append(SearchResult(
                    doctrine_topic=topic,
                    score=round(score, 4),
                    matched_keywords=keyword_matches,
                    irc_sections=self._documents[topic]["irc_sections"],
                    confidence_tier=self._documents[topic]["confidence_tier"],
                    snippet=self._documents[topic]["conclusion_preview"],
                    reasoning_preview=self._documents[topic]["reasoning_preview"],
                ))

        results.sort(key=lambda r: r.score, reverse=True)
        results = results[:context.max_results]

        logger.debug(
            "Search completed | query_tokens={} results={} top_score={}",
            len(query_tokens),
            len(results),
            results[0].score if results else 0.0,
        )

        return results

    # -------------------------------------------------------------------------
    # INTERNAL HELPERS
    # -------------------------------------------------------------------------

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        """Tokenize text into lowercase words, filtering noise."""
        stop_words = {
            "the", "a", "an", "is", "are", "was", "were", "be", "been",
            "have", "has", "had", "do", "does", "did", "will", "would",
            "could", "should", "may", "might", "shall", "can", "to", "of",
            "in", "for", "on", "with", "at", "by", "from", "as", "and",
            "but", "or", "not", "if", "this", "that", "it", "its",
        }
        words = re.findall(r"\b[a-z0-9]{2,}\b", text.lower())
        return [w for w in words if w not in stop_words]

    @staticmethod
    def _cosine_similarity(
        vec_a: Dict[str, float], vec_b: Dict[str, float]
    ) -> float:
        """Compute cosine similarity between two sparse vectors."""
        if not vec_a or not vec_b:
            return 0.0

        common_keys = set(vec_a.keys()) & set(vec_b.keys())
        if not common_keys:
            return 0.0

        dot = sum(vec_a[k] * vec_b[k] for k in common_keys)
        mag_a = math.sqrt(sum(v * v for v in vec_a.values()))
        mag_b = math.sqrt(sum(v * v for v in vec_b.values()))

        if mag_a == 0 or mag_b == 0:
            return 0.0

        return dot / (mag_a * mag_b)

    @staticmethod
    def _irc_boost(
        query_irc: List[str], doc_irc: List[str]
    ) -> float:
        """Boost score if IRC sections match between query and document."""
        if not query_irc or not doc_irc:
            return 0.0

        q_nums = set()
        for s in query_irc:
            nums = re.findall(r"\d+", s)
            q_nums.update(nums)

        d_nums = set()
        for s in doc_irc:
            nums = re.findall(r"\d+", s)
            d_nums.update(nums)

        overlap = q_nums & d_nums
        if overlap:
            return 0.3 * len(overlap)
        return 0.0

    def get_index_stats(self) -> Dict[str, Any]:
        """Return statistics about the search index."""
        return {
            "total_documents": self._total_docs,
            "vocabulary_size": len(self._vocabulary),
            "index_built": self._built,
            "document_topics": list(self._documents.keys()),
        }
