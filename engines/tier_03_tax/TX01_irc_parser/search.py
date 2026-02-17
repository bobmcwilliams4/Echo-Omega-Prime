"""
TX01 IRC Parser Engine - Search Module
Vector-based semantic search fallback for doctrine retrieval
"""

from typing import List, Dict, Optional, Tuple
import numpy as np
from dataclasses import dataclass
import hashlib


@dataclass
class SearchResult:
    """Represents a search result with relevance score"""
    doctrine_topic: str
    relevance_score: float
    matched_keywords: List[str]
    snippet: str


class VectorSearchEngine:
    """Simplified vector search for doctrine retrieval"""

    def __init__(self, doctrines: List):
        self.doctrines = doctrines
        self.keyword_index = self._build_keyword_index()
        self.topic_index = self._build_topic_index()

    def _build_keyword_index(self) -> Dict[str, List[int]]:
        """Build inverted index of keywords to doctrine indices"""
        index = {}
        for i, doctrine in enumerate(self.doctrines):
            for keyword in doctrine.keywords:
                keyword_lower = keyword.lower()
                if keyword_lower not in index:
                    index[keyword_lower] = []
                index[keyword_lower].append(i)
        return index

    def _build_topic_index(self) -> Dict[str, int]:
        """Build index of topics to doctrine indices"""
        return {
            doctrine.topic: i
            for i, doctrine in enumerate(self.doctrines)
        }

    def search_by_keywords(self, query: str, top_k: int = 5) -> List[SearchResult]:
        """Search doctrines by keyword matching"""
        query_terms = query.lower().split()
        scores = {}

        # Score each doctrine based on keyword matches
        for term in query_terms:
            # Exact matches
            if term in self.keyword_index:
                for doc_idx in self.keyword_index[term]:
                    scores[doc_idx] = scores.get(doc_idx, 0.0) + 1.0

            # Partial matches
            for keyword, doc_indices in self.keyword_index.items():
                if term in keyword or keyword in term:
                    for doc_idx in doc_indices:
                        scores[doc_idx] = scores.get(doc_idx, 0.0) + 0.5

        # Convert to SearchResults
        results = []
        for doc_idx, score in sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]:
            doctrine = self.doctrines[doc_idx]
            matched_kw = [kw for kw in doctrine.keywords if any(term in kw.lower() for term in query_terms)]
            results.append(SearchResult(
                doctrine_topic=doctrine.topic,
                relevance_score=score,
                matched_keywords=matched_kw,
                snippet=doctrine.conclusion_template[0] if doctrine.conclusion_template else ""
            ))

        return results

    def search_by_topic(self, topic: str) -> Optional[SearchResult]:
        """Exact topic search"""
        if topic in self.topic_index:
            idx = self.topic_index[topic]
            doctrine = self.doctrines[idx]
            return SearchResult(
                doctrine_topic=doctrine.topic,
                relevance_score=1.0,
                matched_keywords=doctrine.keywords,
                snippet=doctrine.conclusion_template[0] if doctrine.conclusion_template else ""
            )
        return None

    def semantic_search(self, query: str, top_k: int = 3) -> List[SearchResult]:
        """
        Semantic search using simple embedding similarity
        (In production, would use actual embeddings from Cognition Cloud)
        """
        # Simple bag-of-words similarity for now
        query_lower = query.lower()
        similarities = []

        for i, doctrine in enumerate(self.doctrines):
            # Create document representation
            doc_text = " ".join([
                doctrine.topic,
                " ".join(doctrine.keywords),
                " ".join(doctrine.conclusion_template),
                doctrine.reasoning_framework[:500]  # First 500 chars
            ]).lower()

            # Calculate overlap similarity
            query_tokens = set(query_lower.split())
            doc_tokens = set(doc_text.split())
            intersection = query_tokens.intersection(doc_tokens)
            union = query_tokens.union(doc_tokens)

            similarity = len(intersection) / len(union) if union else 0.0
            similarities.append((i, similarity))

        # Sort by similarity and return top_k
        similarities.sort(key=lambda x: x[1], reverse=True)
        results = []

        for idx, sim in similarities[:top_k]:
            if sim > 0.0:  # Only return non-zero matches
                doctrine = self.doctrines[idx]
                results.append(SearchResult(
                    doctrine_topic=doctrine.topic,
                    relevance_score=sim,
                    matched_keywords=doctrine.keywords[:3],
                    snippet=doctrine.conclusion_template[0] if doctrine.conclusion_template else ""
                ))

        return results

    def multi_mode_search(self, query: str, top_k: int = 5) -> Dict[str, List[SearchResult]]:
        """Execute multiple search strategies and combine results"""
        return {
            "keyword_search": self.search_by_keywords(query, top_k),
            "semantic_search": self.semantic_search(query, top_k)
        }

    def get_related_doctrines(self, doctrine_topic: str, max_related: int = 3) -> List[SearchResult]:
        """Find doctrines related to given doctrine"""
        if doctrine_topic not in self.topic_index:
            return []

        source_idx = self.topic_index[doctrine_topic]
        source_doctrine = self.doctrines[source_idx]

        # Find doctrines with overlapping keywords
        keyword_overlap = {}
        for i, doctrine in enumerate(self.doctrines):
            if i == source_idx:
                continue

            overlap = set(source_doctrine.keywords).intersection(set(doctrine.keywords))
            if overlap:
                keyword_overlap[i] = len(overlap)

        # Sort by overlap and return top results
        related = sorted(keyword_overlap.items(), key=lambda x: x[1], reverse=True)[:max_related]
        results = []

        for idx, overlap_count in related:
            doctrine = self.doctrines[idx]
            results.append(SearchResult(
                doctrine_topic=doctrine.topic,
                relevance_score=float(overlap_count) / len(source_doctrine.keywords),
                matched_keywords=list(set(source_doctrine.keywords).intersection(set(doctrine.keywords))),
                snippet=doctrine.conclusion_template[0] if doctrine.conclusion_template else ""
            ))

        return results
