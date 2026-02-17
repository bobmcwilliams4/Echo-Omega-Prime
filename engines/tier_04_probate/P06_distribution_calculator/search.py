"""
P06_distribution_calculator - Search Module
TIE-20 Component 7: Vector search fallback (when implemented with vector DB).
Currently provides keyword-based search over doctrines.
"""

from typing import List, Dict, Optional, Tuple
import re
from collections import defaultdict

from doctrines import DOCTRINE_BLOCKS, DoctrineBlock, search_doctrines_by_keyword


class DistributionSearchEngine:
    """Search engine for estate distribution doctrines and precedents."""

    def __init__(self):
        self.doctrine_index = self._build_doctrine_index()
        self.keyword_index = self._build_keyword_index()

    def _build_doctrine_index(self) -> Dict[str, DoctrineBlock]:
        """Build fast lookup index by doctrine topic."""
        return {block.topic: block for block in DOCTRINE_BLOCKS}

    def _build_keyword_index(self) -> Dict[str, List[str]]:
        """Build inverted index: keyword -> list of doctrine topics."""
        index = defaultdict(list)
        for block in DOCTRINE_BLOCKS:
            for keyword in block.keywords:
                index[keyword.lower()].append(block.topic)
            # Also index words from topic itself
            topic_words = re.findall(r'\w+', block.topic.lower())
            for word in topic_words:
                if word not in index[word]:
                    index[word].append(block.topic)
        return dict(index)

    def search_by_keyword(self, query: str, max_results: int = 10) -> List[DoctrineBlock]:
        """
        Search doctrines by keyword.
        Returns ranked list of relevant doctrine blocks.
        """
        query_lower = query.lower()
        query_words = set(re.findall(r'\w+', query_lower))

        # Score each doctrine by keyword matches
        scores = defaultdict(int)
        for word in query_words:
            if word in self.keyword_index:
                for topic in self.keyword_index[word]:
                    scores[topic] += 1

        # Sort by score descending
        ranked_topics = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:max_results]

        # Return doctrine blocks
        return [self.doctrine_index[topic] for topic, _ in ranked_topics if topic in self.doctrine_index]

    def search_by_issue(self, issue_description: str) -> List[DoctrineBlock]:
        """
        Search for doctrines relevant to a specific distribution issue.
        Uses enhanced keyword matching with domain-specific patterns.
        """
        issue_lower = issue_description.lower()

        # Issue pattern matching
        patterns = {
            "abatement": ["abate", "insufficient", "shortage", "not enough"],
            "ademption": ["ademption", "property gone", "no longer own", "sold before death"],
            "intestacy": ["intestate", "no will", "died without", "statutory"],
            "community_property": ["community", "marital property", "texas", "spouse"],
            "per_stirpes": ["per stirpes", "by representation", "roots", "stocks"],
            "executor_fees": ["executor", "commission", "compensation", "fees"],
            "estate_tax": ["estate tax", "706", "2001", "exemption"],
            "marital_deduction": ["marital deduction", "2056", "QTIP", "spouse"],
            "dni": ["DNI", "distributable net income", "661", "662"],
            "643e": ["643(e)", "in-kind", "distribution", "recognition"]
        }

        matching_topics = []
        for topic_key, keywords in patterns.items():
            if any(kw in issue_lower for kw in keywords):
                # Find doctrines with this topic_key in their name
                for block in DOCTRINE_BLOCKS:
                    if topic_key in block.topic.lower() and block not in matching_topics:
                        matching_topics.append(block)

        # Fallback to keyword search if pattern matching finds nothing
        if not matching_topics:
            matching_topics = self.search_by_keyword(issue_description, max_results=5)

        return matching_topics

    def search_by_statute(self, statute_cite: str) -> List[DoctrineBlock]:
        """Search for doctrines citing specific statute."""
        cite_lower = statute_cite.lower()
        results = []

        for block in DOCTRINE_BLOCKS:
            # Search in primary_authority list
            for authority in block.primary_authority:
                if cite_lower in authority.lower():
                    results.append(block)
                    break

        return results

    def search_by_confidence(self, min_confidence: str) -> List[DoctrineBlock]:
        """Search doctrines by minimum confidence level."""
        confidence_order = {
            "DEFENSIBLE": 4,
            "AGGRESSIVE": 3,
            "DISCLOSURE": 2,
            "HIGH_RISK": 1
        }

        min_level = confidence_order.get(min_confidence.upper(), 1)
        results = [
            block for block in DOCTRINE_BLOCKS
            if confidence_order.get(block.confidence.value, 1) >= min_level
        ]

        return results

    def find_related_doctrines(self, topic: str, max_results: int = 5) -> List[DoctrineBlock]:
        """
        Find doctrines related to a given topic.
        Uses keyword overlap and topic similarity.
        """
        if topic not in self.doctrine_index:
            return []

        base_block = self.doctrine_index[topic]
        base_keywords = set(kw.lower() for kw in base_block.keywords)

        # Score other doctrines by keyword overlap
        scores = {}
        for other_topic, other_block in self.doctrine_index.items():
            if other_topic == topic:
                continue

            other_keywords = set(kw.lower() for kw in other_block.keywords)
            overlap = len(base_keywords & other_keywords)
            if overlap > 0:
                scores[other_topic] = overlap

        # Sort by overlap descending
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:max_results]

        return [self.doctrine_index[t] for t, _ in ranked]

    def search_counter_arguments(self, position: str) -> List[Tuple[DoctrineBlock, List[str]]]:
        """
        Find doctrines with counter-arguments relevant to a given position.
        Returns list of (doctrine, relevant_counter_arguments).
        """
        position_lower = position.lower()
        results = []

        for block in DOCTRINE_BLOCKS:
            relevant_counters = [
                counter for counter in block.counter_arguments
                if any(word in counter.lower() for word in position_lower.split())
            ]
            if relevant_counters:
                results.append((block, relevant_counters))

        return results

    def search_by_beneficiary_type(self, beneficiary_type: str) -> List[DoctrineBlock]:
        """Search doctrines relevant to specific beneficiary type (spouse, child, charity, etc.)."""
        type_lower = beneficiary_type.lower()

        type_keywords = {
            "spouse": ["spouse", "marital", "surviving spouse", "widow"],
            "child": ["child", "descendant", "issue", "offspring"],
            "charity": ["charitable", "charity", "501(c)(3)", "exempt"],
            "trust": ["trust", "trustee", "beneficiary"]
        }

        search_terms = type_keywords.get(type_lower, [type_lower])
        results = []

        for block in DOCTRINE_BLOCKS:
            block_text = f"{block.topic} {' '.join(block.keywords)} {block.reasoning_framework}".lower()
            if any(term in block_text for term in search_terms):
                results.append(block)

        return results

    def get_all_authorities(self) -> List[str]:
        """Get unique list of all authorities cited across all doctrines."""
        authorities = set()
        for block in DOCTRINE_BLOCKS:
            authorities.update(block.primary_authority)
        return sorted(authorities)

    def get_doctrine_stats(self) -> Dict[str, any]:
        """Get statistics about doctrine coverage."""
        total = len(DOCTRINE_BLOCKS)
        by_confidence = defaultdict(int)
        by_authority_level = defaultdict(int)

        for block in DOCTRINE_BLOCKS:
            by_confidence[block.confidence.value] += 1
            by_authority_level[block.authority_level.value] += 1

        return {
            "total_doctrines": total,
            "by_confidence": dict(by_confidence),
            "by_authority_level": dict(by_authority_level),
            "avg_keywords_per_doctrine": sum(len(b.keywords) for b in DOCTRINE_BLOCKS) / total,
            "avg_authorities_per_doctrine": sum(len(b.primary_authority) for b in DOCTRINE_BLOCKS) / total,
            "unique_authorities": len(self.get_all_authorities())
        }

    def build_dependency_graph(self) -> Dict[str, List[str]]:
        """
        Build dependency graph showing which doctrines reference or relate to others.
        Returns adjacency list representation.
        """
        graph = defaultdict(list)

        for block in DOCTRINE_BLOCKS:
            # Find references to other doctrines in reasoning framework
            for other_block in DOCTRINE_BLOCKS:
                if other_block.topic == block.topic:
                    continue

                # Check if other doctrine's topic mentioned in this doctrine's reasoning
                if other_block.topic.replace("_", " ") in block.reasoning_framework.lower():
                    graph[block.topic].append(other_block.topic)

                # Check keyword overlap (strong overlap suggests dependency)
                overlap = len(set(block.keywords) & set(other_block.keywords))
                if overlap >= 3:  # Threshold for dependency
                    if other_block.topic not in graph[block.topic]:
                        graph[block.topic].append(other_block.topic)

        return dict(graph)
