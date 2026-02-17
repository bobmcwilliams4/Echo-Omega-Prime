"""
TX03 Credit Calculator Engine - Search Module
Vector and semantic search for credit doctrines
"""

from typing import List, Dict, Optional, Tuple
from pathlib import Path
import json
from loguru import logger

try:
    from doctrines import DOCTRINE_CACHE, DoctrineBlock, IssueCategory
except ImportError:
    from .doctrines import DOCTRINE_CACHE, DoctrineBlock, IssueCategory


class CreditSearchEngine:
    """Search engine for credit calculator doctrines"""

    def __init__(self, config_path: Path):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)

        self.doctrine_cache = DOCTRINE_CACHE
        self.min_similarity = self.config.get('vector_search', {}).get('min_similarity', 0.75)
        self.max_results = self.config.get('vector_search', {}).get('max_results', 10)

        logger.info(f"CreditSearchEngine initialized with {len(self.doctrine_cache)} doctrines")

    def keyword_search(self, query: str) -> List[DoctrineBlock]:
        """Search doctrines by keyword matching"""
        query_lower = query.lower()
        query_terms = set(query_lower.split())

        results = []
        for doctrine in self.doctrine_cache:
            # Check if any keyword matches query terms
            keyword_matches = sum(1 for kw in doctrine.keywords if kw.lower() in query_lower)
            topic_match = any(term in doctrine.topic.lower() for term in query_terms)

            if keyword_matches > 0 or topic_match:
                results.append((doctrine, keyword_matches))

        # Sort by number of keyword matches (descending)
        results.sort(key=lambda x: x[1], reverse=True)

        return [doctrine for doctrine, _ in results[:self.max_results]]

    def search_by_irc_section(self, irc_section: str) -> List[DoctrineBlock]:
        """Search doctrines by IRC section"""
        section_normalized = irc_section.strip().upper()
        if not section_normalized.startswith('IRC_'):
            section_normalized = f"IRC_{section_normalized}"

        results = []
        for doctrine in self.doctrine_cache:
            if any(section_normalized in kw.upper() for kw in doctrine.keywords):
                results.append(doctrine)

        return results

    def search_by_category(self, category: IssueCategory) -> List[DoctrineBlock]:
        """Search doctrines by issue category"""
        return [d for d in self.doctrine_cache if d.issue_category == category]

    def search_by_credit_type(self, credit_type: str) -> List[DoctrineBlock]:
        """Search doctrines by credit type (refundable, nonrefundable, etc.)"""
        credit_type_lower = credit_type.lower()
        return [d for d in self.doctrine_cache if credit_type_lower in d.credit_type.lower()]

    def semantic_similarity(self, query: str, doctrine: DoctrineBlock) -> float:
        """Calculate semantic similarity score (simple term overlap)"""
        query_terms = set(query.lower().split())
        doctrine_terms = set()

        # Collect doctrine terms from various fields
        doctrine_terms.update(doctrine.topic.lower().split('_'))
        for kw in doctrine.keywords:
            doctrine_terms.update(kw.lower().split('_'))
        doctrine_terms.update(doctrine.reasoning_framework.lower().split())

        if not query_terms or not doctrine_terms:
            return 0.0

        # Calculate Jaccard similarity
        intersection = query_terms.intersection(doctrine_terms)
        union = query_terms.union(doctrine_terms)

        return len(intersection) / len(union) if union else 0.0

    def semantic_search(self, query: str) -> List[Tuple[DoctrineBlock, float]]:
        """Search doctrines by semantic similarity"""
        results = []
        for doctrine in self.doctrine_cache:
            score = self.semantic_similarity(query, doctrine)
            if score >= self.min_similarity:
                results.append((doctrine, score))

        # Sort by similarity score (descending)
        results.sort(key=lambda x: x[1], reverse=True)

        return results[:self.max_results]

    def hybrid_search(self, query: str, boost_keywords: float = 0.6, boost_semantic: float = 0.4) -> List[Tuple[DoctrineBlock, float]]:
        """Hybrid search combining keyword and semantic approaches"""
        # Keyword search
        keyword_results = self.keyword_search(query)
        keyword_scores = {id(d): 1.0 / (i + 1) for i, d in enumerate(keyword_results)}  # Rank-based scoring

        # Semantic search
        semantic_results = self.semantic_search(query)
        semantic_scores = {id(d): score for d, score in semantic_results}

        # Combine scores (use dict to deduplicate by id)
        all_doctrines_dict = {}
        for d in keyword_results:
            all_doctrines_dict[id(d)] = d
        for d, _ in semantic_results:
            all_doctrines_dict[id(d)] = d

        combined_results = []

        for doctrine in all_doctrines_dict.values():
            doctrine_id = id(doctrine)
            keyword_score = keyword_scores.get(doctrine_id, 0.0)
            semantic_score = semantic_scores.get(doctrine_id, 0.0)

            # Weighted combination
            combined_score = (boost_keywords * keyword_score) + (boost_semantic * semantic_score)
            combined_results.append((doctrine, combined_score))

        # Sort by combined score
        combined_results.sort(key=lambda x: x[1], reverse=True)

        return combined_results[:self.max_results]

    def search_by_confidence(self, min_confidence: float) -> List[DoctrineBlock]:
        """Search doctrines meeting minimum confidence threshold"""
        return [d for d in self.doctrine_cache if d.confidence >= min_confidence]

    def search_carryover_credits(self) -> List[DoctrineBlock]:
        """Find credits that allow carryover"""
        return [d for d in self.doctrine_cache if d.carryover_allowed]

    def search_recapture_credits(self) -> List[DoctrineBlock]:
        """Find credits with recapture risk"""
        return [d for d in self.doctrine_cache if d.recapture_risk]

    def get_credit_ordering(self) -> List[DoctrineBlock]:
        """Get credits in ordering priority"""
        return sorted(self.doctrine_cache, key=lambda x: x.ordering_priority)

    def search_by_entity_scope(self, entity_type: str) -> List[DoctrineBlock]:
        """Search credits applicable to entity type"""
        return [d for d in self.doctrine_cache if entity_type in d.entity_scope]

    def multi_filter_search(
        self,
        query: Optional[str] = None,
        category: Optional[IssueCategory] = None,
        credit_type: Optional[str] = None,
        min_confidence: Optional[float] = None,
        entity_type: Optional[str] = None,
        carryover_only: bool = False,
        recapture_only: bool = False
    ) -> List[DoctrineBlock]:
        """Advanced multi-criteria search"""
        results = self.doctrine_cache.copy()

        # Apply filters sequentially
        if query:
            query_results = self.hybrid_search(query)
            query_doctrines = {id(d) for d, _ in query_results}
            results = [d for d in results if id(d) in query_doctrines]

        if category:
            results = [d for d in results if d.issue_category == category]

        if credit_type:
            credit_type_lower = credit_type.lower()
            results = [d for d in results if credit_type_lower in d.credit_type.lower()]

        if min_confidence is not None:
            results = [d for d in results if d.confidence >= min_confidence]

        if entity_type:
            results = [d for d in results if entity_type in d.entity_scope]

        if carryover_only:
            results = [d for d in results if d.carryover_allowed]

        if recapture_only:
            results = [d for d in results if d.recapture_risk]

        return results

    def get_related_credits(self, topic: str, max_results: int = 5) -> List[DoctrineBlock]:
        """Find credits related to a given topic"""
        # Find the source doctrine
        source_doctrine = None
        for d in self.doctrine_cache:
            if d.topic == topic:
                source_doctrine = d
                break

        if not source_doctrine:
            return []

        # Find related by shared keywords or category
        related = []
        for doctrine in self.doctrine_cache:
            if doctrine.topic == topic:
                continue  # Skip self

            # Count shared keywords
            shared_keywords = set(source_doctrine.keywords).intersection(set(doctrine.keywords))

            # Same category bonus
            category_match = doctrine.issue_category == source_doctrine.issue_category

            if shared_keywords or category_match:
                score = len(shared_keywords) + (2 if category_match else 0)
                related.append((doctrine, score))

        # Sort by relevance
        related.sort(key=lambda x: x[1], reverse=True)

        return [d for d, _ in related[:max_results]]

    def get_statistics(self) -> Dict[str, any]:
        """Get search engine statistics"""
        return {
            'total_doctrines': len(self.doctrine_cache),
            'by_category': {
                cat.value: len([d for d in self.doctrine_cache if d.issue_category == cat])
                for cat in IssueCategory
            },
            'by_credit_type': {
                'refundable': len([d for d in self.doctrine_cache if 'refundable' in d.credit_type]),
                'nonrefundable': len([d for d in self.doctrine_cache if d.credit_type == 'nonrefundable']),
                'partially_refundable': len([d for d in self.doctrine_cache if 'partially' in d.credit_type])
            },
            'carryover_allowed': len([d for d in self.doctrine_cache if d.carryover_allowed]),
            'recapture_risk': len([d for d in self.doctrine_cache if d.recapture_risk]),
            'avg_confidence': sum(d.confidence for d in self.doctrine_cache) / len(self.doctrine_cache)
        }
