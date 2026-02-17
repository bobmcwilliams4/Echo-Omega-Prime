"""
P01 Heirship Determiner — Vector Search Fallback
Semantic retrieval when doctrine cache misses
"""

from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import json
from pathlib import Path


@dataclass
class SearchResult:
    """Search result with relevance scoring"""
    content: str
    source: str
    relevance_score: float
    metadata: Dict


class VectorSearchEngine:
    """Fallback vector search for doctrine retrieval"""

    def __init__(self, cloud_retriever=None):
        self.cloud_retriever = cloud_retriever
        self.local_fallback_enabled = True

    def search(self, query: str, top_k: int = 5, threshold: float = 0.75) -> List[SearchResult]:
        """
        Search for relevant probate content

        Args:
            query: Search query text
            top_k: Number of results to return
            threshold: Minimum relevance score

        Returns:
            List of SearchResult objects
        """
        results = []

        # Try cloud retrieval first
        if self.cloud_retriever:
            try:
                cloud_results = self.cloud_retriever.search(query, limit=top_k)
                for item in cloud_results:
                    if item.get('score', 0) >= threshold:
                        results.append(SearchResult(
                            content=item.get('content', ''),
                            source=item.get('source', 'cognition_cloud'),
                            relevance_score=item.get('score', 0.0),
                            metadata=item.get('metadata', {})
                        ))
            except Exception:
                pass  # Fall through to local fallback

        # Local fallback if cloud unavailable or insufficient results
        if len(results) < top_k and self.local_fallback_enabled:
            local_results = self._local_search(query, top_k - len(results))
            results.extend(local_results)

        return results[:top_k]

    def _local_search(self, query: str, limit: int) -> List[SearchResult]:
        """Local keyword-based fallback search"""
        # Simplified local search for demonstration
        # In production, would use local vector DB or keyword index

        probate_knowledge_base = [
            {
                "content": "Texas Estates Code §201.001 governs distribution of separate property when decedent dies intestate with surviving spouse and children.",
                "keywords": ["separate property", "spouse", "children", "intestate", "§201.001"],
                "source": "estates_code_201.001"
            },
            {
                "content": "Texas Estates Code §201.002 provides that all community property passes to surviving spouse if decedent dies intestate.",
                "keywords": ["community property", "surviving spouse", "intestate", "§201.002"],
                "source": "estates_code_201.002"
            },
            {
                "content": "Per stirpes distribution under §201.101 divides estate at first generational level, then subdivides deceased heir's share among descendants.",
                "keywords": ["per stirpes", "distribution", "descendants", "§201.101"],
                "source": "estates_code_201.101"
            },
            {
                "content": "Affidavit of heirship under §203.001 requires two disinterested witnesses with personal knowledge, creates prima facie evidence of heirship.",
                "keywords": ["affidavit", "heirship", "witnesses", "§203.001"],
                "source": "estates_code_203.001"
            },
            {
                "content": "Homestead passes to surviving spouse as life estate under §102.002, with remainder to descendants.",
                "keywords": ["homestead", "life estate", "spouse", "§102.002"],
                "source": "estates_code_102.002"
            }
        ]

        query_lower = query.lower()
        scored_results = []

        for item in probate_knowledge_base:
            score = self._calculate_keyword_score(query_lower, item["keywords"])
            if score > 0:
                scored_results.append((score, item))

        scored_results.sort(reverse=True, key=lambda x: x[0])

        results = []
        for score, item in scored_results[:limit]:
            results.append(SearchResult(
                content=item["content"],
                source=item["source"],
                relevance_score=score,
                metadata={"keywords": item["keywords"]}
            ))

        return results

    def _calculate_keyword_score(self, query: str, keywords: List[str]) -> float:
        """Simple keyword matching score"""
        matches = sum(1 for kw in keywords if kw.lower() in query)
        if not keywords:
            return 0.0
        return matches / len(keywords)

    def multi_query_search(self, queries: List[str], top_k: int = 3) -> Dict[str, List[SearchResult]]:
        """Execute multiple searches and aggregate results"""
        results = {}
        for query in queries:
            results[query] = self.search(query, top_k=top_k)
        return results


class CitationExtractor:
    """Extract and format legal citations from search results"""

    @staticmethod
    def extract_statutes(text: str) -> List[str]:
        """Extract statute citations from text"""
        import re
        pattern = r'§\s*\d+\.\d+'
        return re.findall(pattern, text)

    @staticmethod
    def extract_cases(text: str) -> List[str]:
        """Extract case citations from text"""
        import re
        # Simplified case citation pattern
        pattern = r'\b[A-Z][a-z]+\s+v\.\s+[A-Z][a-z]+,\s+\d+\s+[A-Z.]+\d+\s+\d+'
        return re.findall(pattern, text)

    @staticmethod
    def format_bluebook(citation: str, citation_type: str) -> str:
        """Format citation in Bluebook style"""
        # Simplified Bluebook formatting
        if citation_type == "statute":
            return f"TEX. EST. CODE ANN. {citation}"
        elif citation_type == "case":
            return citation  # Already in case format
        return citation


__all__ = ['VectorSearchEngine', 'SearchResult', 'CitationExtractor']
