"""
TX11 Nonprofit Tax — Search Engine
Keyword, category, and authority-based search for doctrine blocks.

Author: ECHO OMEGA PRIME
Engine: TX11 Nonprofit Tax
"""

from dataclasses import dataclass, field as dc_field
from typing import List, Dict, Optional, Set
from collections import defaultdict

from doctrines import DoctrineBlock, get_all_doctrines, get_doctrine_topics


@dataclass
class SearchResult:
    """Single doctrine search result."""
    doctrine_topic: str
    score: float
    matched_keywords: List[str]
    match_type: str  # "keyword", "category", "authority"


@dataclass
class SearchStats:
    """Search engine statistics."""
    total_searches: int = 0
    keyword_searches: int = 0
    category_searches: int = 0
    authority_searches: int = 0
    avg_results_per_search: float = 0.0
    cache_hits: int = 0


class DoctrineSearchEngine:
    """Search engine for nonprofit tax doctrine blocks."""

    def __init__(self):
        self.doctrines = get_all_doctrines()
        self.stats = SearchStats()
        self._keyword_index: Dict[str, List[str]] = {}
        self._category_index: Dict[str, List[str]] = {}
        self._authority_index: Dict[str, List[str]] = {}
        self._build_indexes()

    def _build_indexes(self):
        """Build inverted indexes for fast lookup."""
        # Keyword index
        for doctrine in self.doctrines:
            for keyword in doctrine.keywords:
                keyword_lower = keyword.lower()
                if keyword_lower not in self._keyword_index:
                    self._keyword_index[keyword_lower] = []
                self._keyword_index[keyword_lower].append(doctrine.topic)

            # Also index words from topic
            topic_words = doctrine.topic.replace("_", " ").split()
            for word in topic_words:
                word_lower = word.lower()
                if word_lower not in self._keyword_index:
                    self._keyword_index[word_lower] = []
                if doctrine.topic not in self._keyword_index[word_lower]:
                    self._keyword_index[word_lower].append(doctrine.topic)

        # Authority index
        for doctrine in self.doctrines:
            for auth in doctrine.primary_authority:
                auth_lower = auth.lower()
                if auth_lower not in self._authority_index:
                    self._authority_index[auth_lower] = []
                self._authority_index[auth_lower].append(doctrine.topic)

    def search_by_keyword(self, query: str, top_k: int = 5) -> List[SearchResult]:
        """Search doctrines by keyword matching."""
        query_lower = query.lower()
        query_words = query_lower.split()

        # Score each doctrine by keyword matches
        scores: Dict[str, float] = defaultdict(float)
        matches: Dict[str, Set[str]] = defaultdict(set)

        for word in query_words:
            for indexed_keyword, topics in self._keyword_index.items():
                if word in indexed_keyword or indexed_keyword in word:
                    for topic in topics:
                        scores[topic] += 1.0
                        matches[topic].add(indexed_keyword)

        # Also check full keyword phrases
        for doctrine in self.doctrines:
            for keyword in doctrine.keywords:
                if keyword.lower() in query_lower:
                    scores[doctrine.topic] += 2.0  # Phrase match worth more
                    matches[doctrine.topic].add(keyword)

        # Convert to SearchResult objects
        results = []
        for topic, score in sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]:
            results.append(SearchResult(
                doctrine_topic=topic,
                score=score,
                matched_keywords=list(matches[topic]),
                match_type="keyword"
            ))

        self.stats.keyword_searches += 1
        return results

    def search_by_authority(self, authority: str, top_k: int = 5) -> List[SearchResult]:
        """Search doctrines by authority citation."""
        authority_lower = authority.lower()
        results = []

        for doctrine in self.doctrines:
            for auth in doctrine.primary_authority:
                if authority_lower in auth.lower():
                    results.append(SearchResult(
                        doctrine_topic=doctrine.topic,
                        score=1.0,
                        matched_keywords=[auth],
                        match_type="authority"
                    ))
                    break  # Only count once per doctrine

        self.stats.authority_searches += 1
        return results[:top_k]

    def search_by_category(self, category: str, top_k: int = 5) -> List[SearchResult]:
        """Search doctrines by issue category."""
        category_lower = category.lower()
        results = []

        # Category mapping (simplified - could be extended)
        category_keywords = {
            "exempt_status": ["501(c)(3)", "qualification", "organizational", "operational"],
            "ubit": ["unrelated business", "512", "513", "514"],
            "public_charity": ["509(a)", "public support", "public charity"],
            "private_foundation": ["private foundation", "4940", "4941", "4942", "4943", "4944", "4945"],
            "political": ["political", "campaign", "lobbying", "501(h)", "4911"],
            "excess_benefit": ["4958", "excess benefit", "disqualified person"],
            "daf": ["donor-advised", "4966", "4967"],
        }

        # Find matching keywords for category
        matching_keywords = []
        for cat, keywords in category_keywords.items():
            if cat in category_lower:
                matching_keywords.extend(keywords)

        # Search using those keywords
        if matching_keywords:
            combined_query = " ".join(matching_keywords)
            results = self.search_by_keyword(combined_query, top_k=top_k)
            for result in results:
                result.match_type = "category"

        self.stats.category_searches += 1
        return results

    def search(self, query: str, top_k: int = 5) -> List[SearchResult]:
        """
        Main search method — tries keyword search.
        For vector search, use semantic embeddings (not implemented in this minimal version).
        """
        self.stats.total_searches += 1

        results = self.search_by_keyword(query, top_k=top_k)

        if results:
            self.stats.cache_hits += 1

        # Update average results per search
        if self.stats.total_searches > 0:
            self.stats.avg_results_per_search = (
                self.stats.avg_results_per_search * (self.stats.total_searches - 1) +
                len(results)
            ) / self.stats.total_searches

        return results


# =============================================================================
# MODULE-LEVEL SINGLETON
# =============================================================================

_SEARCH_ENGINE: Optional[DoctrineSearchEngine] = None


def get_search_engine() -> DoctrineSearchEngine:
    """Get or create the singleton search engine."""
    global _SEARCH_ENGINE
    if _SEARCH_ENGINE is None:
        _SEARCH_ENGINE = DoctrineSearchEngine()
    return _SEARCH_ENGINE


def search_doctrines(query: str, top_k: int = 5) -> List[SearchResult]:
    """Module-level search function."""
    engine = get_search_engine()
    return engine.search(query, top_k=top_k)


def get_search_stats() -> Dict[str, any]:
    """Get search engine statistics."""
    engine = get_search_engine()
    return {
        "total_searches": engine.stats.total_searches,
        "keyword_searches": engine.stats.keyword_searches,
        "category_searches": engine.stats.category_searches,
        "authority_searches": engine.stats.authority_searches,
        "avg_results_per_search": engine.stats.avg_results_per_search,
        "cache_hits": engine.stats.cache_hits,
        "cache_hit_rate": engine.stats.cache_hits / engine.stats.total_searches if engine.stats.total_searches > 0 else 0.0,
    }
