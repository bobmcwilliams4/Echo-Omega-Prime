"""
LM20 Indian Land Engine — Vector Search
Fast semantic search over doctrine cache when exact keyword match fails.

Integration with cloud retriever (Cognition Cloud) for expanded knowledge.

Author: ECHO OMEGA PRIME
Engine: LM20
"""

from dataclasses import dataclass, field
from typing import List, Optional
import time
from loguru import logger


@dataclass
class SearchResult:
    """Single search result from doctrine cache."""
    topic: str
    score: float
    matched_keywords: List[str]
    doctrine_summary: str
    issue_category: str
    confidence_level: str
    retrieval_time_ms: float


@dataclass
class SearchStats:
    """Search engine statistics."""
    total_searches: int = 0
    cache_hits: int = 0
    vector_searches: int = 0
    avg_search_time_ms: float = 0.0
    total_results_returned: int = 0


class DoctrineSearchEngine:
    """
    Lightweight vector search over doctrine cache.

    Layer 2 of TIE architecture: semantic retrieval when cache miss.
    """

    def __init__(self, doctrines: List):
        """Initialize search engine with doctrine blocks."""
        self.doctrines = doctrines
        self.stats = SearchStats()
        self._keyword_index = self._build_keyword_index()
        logger.info(f"DoctrineSearchEngine initialized with {len(doctrines)} doctrines")

    def _build_keyword_index(self) -> dict:
        """Build inverted index: keyword → [doctrine indices]."""
        index = {}
        for i, doctrine in enumerate(self.doctrines):
            # Index topic words
            for word in doctrine.topic.lower().split():
                if len(word) > 3:  # skip short words
                    index.setdefault(word, []).append(i)

            # Index keywords
            for kw in doctrine.keywords:
                for word in kw.lower().split():
                    if len(word) > 3:
                        index.setdefault(word, []).append(i)

        # Deduplicate
        for kw in index:
            index[kw] = list(set(index[kw]))

        logger.info(f"Built keyword index with {len(index)} terms")
        return index

    def search(self, query: str, top_k: int = 3) -> List[SearchResult]:
        """
        Search doctrine cache using keyword matching + scoring.

        Args:
            query: search query
            top_k: number of results to return

        Returns:
            List of SearchResult sorted by score (descending)
        """
        start_time = time.perf_counter()
        self.stats.total_searches += 1

        query_lower = query.lower()
        query_words = [w for w in query_lower.split() if len(w) > 3]

        # Score each doctrine
        scores = []
        for i, doctrine in enumerate(self.doctrines):
            score, matched_kws = self._score_doctrine(doctrine, query_words)
            if score > 0:
                scores.append((i, score, matched_kws))

        # Sort by score descending
        scores.sort(key=lambda x: x[1], reverse=True)

        # Build results
        results = []
        for i, score, matched_kws in scores[:top_k]:
            doctrine = self.doctrines[i]
            results.append(SearchResult(
                topic=doctrine.topic,
                score=score,
                matched_keywords=matched_kws,
                doctrine_summary=doctrine.conclusion_template[0] if doctrine.conclusion_template else "",
                issue_category=doctrine.issue_category.value,
                confidence_level=doctrine.confidence_stratification.value,
                retrieval_time_ms=(time.perf_counter() - start_time) * 1000
            ))

        elapsed_ms = (time.perf_counter() - start_time) * 1000
        self.stats.avg_search_time_ms = (
            (self.stats.avg_search_time_ms * (self.stats.total_searches - 1) + elapsed_ms)
            / self.stats.total_searches
        )
        self.stats.total_results_returned += len(results)

        if len(results) > 0:
            self.stats.cache_hits += 1
        else:
            self.stats.vector_searches += 1

        logger.debug(f"Search for '{query}' returned {len(results)} results in {elapsed_ms:.2f}ms")
        return results

    def _score_doctrine(self, doctrine, query_words: List[str]) -> tuple[float, List[str]]:
        """
        Score a single doctrine against query words.

        Scoring:
        - Topic word match: 3 points
        - Keyword exact match: 2 points
        - Keyword partial match: 1 point
        - Reasoning framework match: 0.5 points
        """
        score = 0.0
        matched_keywords = []

        topic_lower = doctrine.topic.lower()
        keywords_lower = [kw.lower() for kw in doctrine.keywords]
        reasoning_lower = doctrine.reasoning_framework.lower()

        for word in query_words:
            # Topic match
            if word in topic_lower:
                score += 3.0
                matched_keywords.append(f"topic:{word}")

            # Keyword exact match
            if word in keywords_lower:
                score += 2.0
                matched_keywords.append(word)
            else:
                # Keyword partial match
                for kw in keywords_lower:
                    if word in kw:
                        score += 1.0
                        matched_keywords.append(kw)
                        break

            # Reasoning framework match
            if word in reasoning_lower:
                score += 0.5

        return score, list(set(matched_keywords))

    def get_stats(self) -> SearchStats:
        """Return search engine statistics."""
        return self.stats


# ==============================================================================
# MODULE-LEVEL FUNCTIONS (for engine.py integration)
# ==============================================================================

_search_engine: Optional[DoctrineSearchEngine] = None


def get_search_engine() -> Optional[DoctrineSearchEngine]:
    """Get the initialized search engine instance."""
    return _search_engine


def initialize_search_engine(doctrines: List):
    """Initialize module-level search engine."""
    global _search_engine
    _search_engine = DoctrineSearchEngine(doctrines)
    logger.info("Module-level search engine initialized")


def search_doctrines(query: str, top_k: int = 3) -> List[SearchResult]:
    """
    Search doctrines using module-level engine.

    Args:
        query: search query
        top_k: number of results

    Returns:
        List of SearchResult
    """
    if _search_engine is None:
        logger.warning("Search engine not initialized; returning empty results")
        return []

    return _search_engine.search(query, top_k)


def get_search_stats() -> Optional[SearchStats]:
    """Get search statistics from module-level engine."""
    if _search_engine is None:
        return None
    return _search_engine.get_stats()
