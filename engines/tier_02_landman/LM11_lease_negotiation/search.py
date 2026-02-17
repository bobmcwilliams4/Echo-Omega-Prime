"""
LM11 Lease Negotiation Engine — Vector Search Module
Semantic retrieval fallback when doctrine cache misses.

Architecture:
    Layer 2 of the three-layer response system.
    Uses TF-IDF style scoring over doctrine blocks for fast retrieval
    without external vector DB dependency.

Author: ECHO OMEGA PRIME
Engine: LM11 Lease Negotiation
Version: 1.0.0
"""

from __future__ import annotations

import hashlib
import math
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple

from loguru import logger

# ==============================================================================
# CONSTANTS
# ==============================================================================

ENGINE_ID = "LM11"
SEARCH_VERSION = "1.0.0"
DEFAULT_TOP_K = 5
MIN_RELEVANCE_SCORE = 0.15
IDF_SMOOTHING = 1.0

# Stopwords for lease negotiation domain
STOPWORDS: Set[str] = {
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "shall", "can", "must", "need", "dare",
    "to", "of", "in", "for", "on", "with", "at", "by", "from", "as",
    "into", "through", "during", "before", "after", "above", "below",
    "between", "under", "over", "about", "against", "among",
    "and", "or", "but", "nor", "not", "so", "yet", "both", "either",
    "neither", "each", "every", "all", "any", "few", "more", "most",
    "other", "some", "such", "no", "only", "own", "same", "than",
    "too", "very", "just", "because", "if", "when", "while", "where",
    "how", "what", "which", "who", "whom", "this", "that", "these",
    "those", "it", "its", "they", "them", "their", "we", "us", "our",
    "he", "him", "his", "she", "her", "i", "me", "my", "you", "your",
}

# High-value domain terms with IDF boost
DOMAIN_BOOST_TERMS: Dict[str, float] = {
    "royalty": 2.0,
    "pugh": 3.0,
    "habendum": 3.0,
    "pooling": 2.5,
    "unitization": 2.5,
    "shut-in": 2.5,
    "cessation": 2.5,
    "indemnification": 2.0,
    "continuous": 1.8,
    "drilling": 1.5,
    "depth": 2.0,
    "severance": 2.5,
    "cost-free": 3.0,
    "proceeds": 2.0,
    "market value": 2.5,
    "bonus": 1.8,
    "delay rental": 2.5,
    "paid-up": 2.5,
    "surface damage": 2.0,
    "top lease": 3.0,
    "force pooling": 3.0,
    "assignment": 1.8,
    "accommodation": 2.5,
    "savings clause": 2.5,
    "commencement": 2.0,
    "operations clause": 2.5,
    "market enhancement": 2.5,
    "audit rights": 2.0,
    "environmental": 1.8,
    "lessor": 1.5,
    "lessee": 1.5,
    "mineral owner": 2.0,
}


# ==============================================================================
# SEARCH RESULT
# ==============================================================================

@dataclass
class SearchResult:
    """A single search result from vector/semantic search."""
    topic: str
    score: float
    keywords_matched: List[str]
    conclusion_preview: str
    confidence: str
    entity_scope: str
    source_layer: str = "semantic_retrieval"
    match_hash: str = ""

    def __post_init__(self) -> None:
        content = f"{self.topic}|{self.score:.4f}|{'|'.join(self.keywords_matched)}"
        self.match_hash = hashlib.sha256(content.encode()).hexdigest()[:12]

    def to_dict(self) -> Dict[str, Any]:
        """Serialize result."""
        return {
            "topic": self.topic,
            "score": round(self.score, 4),
            "keywords_matched": self.keywords_matched,
            "conclusion_preview": self.conclusion_preview[:300],
            "confidence": self.confidence,
            "entity_scope": self.entity_scope,
            "source_layer": self.source_layer,
            "match_hash": self.match_hash,
        }


@dataclass
class SearchResponse:
    """Complete search response with metadata."""
    query: str
    results: List[SearchResult]
    total_candidates: int
    search_time_ms: float
    index_size: int
    query_tokens: List[str]
    domain_boosts_applied: int

    def to_dict(self) -> Dict[str, Any]:
        """Serialize response."""
        return {
            "query": self.query[:200],
            "result_count": len(self.results),
            "total_candidates": self.total_candidates,
            "search_time_ms": round(self.search_time_ms, 2),
            "index_size": self.index_size,
            "query_tokens": self.query_tokens,
            "domain_boosts_applied": self.domain_boosts_applied,
            "results": [r.to_dict() for r in self.results],
        }


# ==============================================================================
# DOCUMENT INDEX ENTRY
# ==============================================================================

@dataclass
class IndexEntry:
    """Indexed document entry for search."""
    topic: str
    keywords: List[str]
    conclusion_template: str
    confidence: str
    entity_scope: str
    term_frequencies: Dict[str, float] = field(default_factory=dict)
    token_set: Set[str] = field(default_factory=set)
    doc_length: int = 0

    def compute_tf(self) -> None:
        """Compute term frequencies for this document."""
        all_tokens = self._tokenize(
            f"{self.topic} {' '.join(self.keywords)} {self.conclusion_template}"
        )
        self.doc_length = len(all_tokens)
        counts = Counter(all_tokens)
        max_count = max(counts.values()) if counts else 1
        self.term_frequencies = {
            term: 0.5 + 0.5 * (count / max_count)
            for term, count in counts.items()
        }
        self.token_set = set(all_tokens)

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        """Tokenize text into searchable terms."""
        text = text.lower()
        text = re.sub(r"[^\w\s/-]", " ", text)
        tokens = text.split()
        return [t for t in tokens if t not in STOPWORDS and len(t) > 1]


# ==============================================================================
# SEARCH ENGINE
# ==============================================================================

class LeaseNegotiationSearchEngine:
    """
    TF-IDF style search engine for doctrine blocks.

    Responsibilities:
    - Index doctrine blocks by topic, keywords, and content
    - Score queries against indexed documents
    - Apply domain-specific term boosting
    - Return ranked results with match metadata
    - Operate without external vector DB dependency
    """

    def __init__(self) -> None:
        self._index: List[IndexEntry] = []
        self._idf_cache: Dict[str, float] = {}
        self._doc_count: int = 0
        self._indexed: bool = False
        logger.info("LeaseNegotiationSearchEngine initialized")

    def index_doctrine_block(
        self,
        topic: str,
        keywords: List[str],
        conclusion_template: str,
        confidence: str = "DEFENSIBLE",
        entity_scope: str = "general",
    ) -> None:
        """Add a doctrine block to the search index."""
        entry = IndexEntry(
            topic=topic,
            keywords=keywords,
            conclusion_template=conclusion_template,
            confidence=confidence,
            entity_scope=entity_scope,
        )
        entry.compute_tf()
        self._index.append(entry)
        self._doc_count = len(self._index)
        self._indexed = False

    def build_index(self) -> None:
        """Rebuild IDF cache after all documents are indexed."""
        if not self._index:
            logger.warning("No documents to index")
            return

        doc_freq: Dict[str, int] = defaultdict(int)
        for entry in self._index:
            for token in entry.token_set:
                doc_freq[token] += 1

        self._idf_cache = {
            term: math.log((self._doc_count + IDF_SMOOTHING) / (df + IDF_SMOOTHING))
            for term, df in doc_freq.items()
        }
        self._indexed = True
        logger.info(
            f"Search index built: {self._doc_count} documents, "
            f"{len(self._idf_cache)} unique terms"
        )

    def search(
        self,
        query: str,
        top_k: int = DEFAULT_TOP_K,
        min_score: float = MIN_RELEVANCE_SCORE,
        confidence_filter: Optional[str] = None,
        entity_scope_filter: Optional[str] = None,
    ) -> SearchResponse:
        """
        Search indexed doctrine blocks for relevant results.

        Scoring:
        1. TF-IDF cosine similarity base score
        2. Domain boost for high-value terms
        3. Keyword exact match bonus
        4. Optional confidence and scope filtering
        """
        import time
        start = time.time()

        if not self._indexed:
            self.build_index()

        query_tokens = IndexEntry._tokenize(query)
        if not query_tokens:
            return SearchResponse(
                query=query, results=[], total_candidates=0,
                search_time_ms=0.0, index_size=self._doc_count,
                query_tokens=[], domain_boosts_applied=0,
            )

        # Score each document
        scored: List[Tuple[float, IndexEntry, List[str]]] = []
        domain_boosts = 0

        for entry in self._index:
            if confidence_filter and entry.confidence != confidence_filter:
                continue
            if entity_scope_filter and entry.entity_scope != entity_scope_filter:
                continue

            score = 0.0
            matched_keywords: List[str] = []

            for token in query_tokens:
                if token in entry.term_frequencies:
                    tf = entry.term_frequencies[token]
                    idf = self._idf_cache.get(token, 1.0)
                    token_score = tf * idf

                    # Apply domain boost
                    if token in DOMAIN_BOOST_TERMS:
                        token_score *= DOMAIN_BOOST_TERMS[token]
                        domain_boosts += 1

                    score += token_score

                    if token in [kw.lower() for kw in entry.keywords]:
                        matched_keywords.append(token)
                        score += 0.5  # Keyword exact match bonus

            # Normalize by document length
            if entry.doc_length > 0:
                score /= math.sqrt(entry.doc_length)

            # Topic match bonus
            topic_tokens = set(IndexEntry._tokenize(entry.topic))
            topic_overlap = len(set(query_tokens) & topic_tokens)
            if topic_overlap > 0:
                score += topic_overlap * 0.3

            if score >= min_score:
                scored.append((score, entry, matched_keywords))

        # Sort by score descending
        scored.sort(key=lambda x: x[0], reverse=True)
        top_results = scored[:top_k]

        results = [
            SearchResult(
                topic=entry.topic,
                score=score,
                keywords_matched=matched_kws,
                conclusion_preview=entry.conclusion_template[:300],
                confidence=entry.confidence,
                entity_scope=entry.entity_scope,
            )
            for score, entry, matched_kws in top_results
        ]

        elapsed_ms = (time.time() - start) * 1000

        logger.debug(
            f"Search complete: query='{query[:60]}' | "
            f"results={len(results)}/{len(scored)} | "
            f"time={elapsed_ms:.1f}ms"
        )

        return SearchResponse(
            query=query,
            results=results,
            total_candidates=len(scored),
            search_time_ms=elapsed_ms,
            index_size=self._doc_count,
            query_tokens=query_tokens,
            domain_boosts_applied=domain_boosts,
        )

    def get_stats(self) -> Dict[str, Any]:
        """Return search engine statistics."""
        return {
            "engine_id": ENGINE_ID,
            "version": SEARCH_VERSION,
            "document_count": self._doc_count,
            "unique_terms": len(self._idf_cache),
            "indexed": self._indexed,
            "domain_boost_terms": len(DOMAIN_BOOST_TERMS),
            "stopwords": len(STOPWORDS),
        }


# ==============================================================================
# MODULE-LEVEL SINGLETON
# ==============================================================================

_search_engine: Optional[LeaseNegotiationSearchEngine] = None


def get_search_engine() -> LeaseNegotiationSearchEngine:
    """Get or create the search engine singleton."""
    global _search_engine
    if _search_engine is None:
        _search_engine = LeaseNegotiationSearchEngine()
    return _search_engine
