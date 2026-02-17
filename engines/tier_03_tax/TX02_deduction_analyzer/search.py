"""
TX02 Deduction Analyzer — Search Module

Vector similarity fallback when doctrine cache misses.
Integrates with Cognition Cloud for semantic retrieval.
"""

from __future__ import annotations

import asyncio
from typing import List, Optional

from loguru import logger

from doctrines import DOCTRINE_CACHE, DoctrineBlock


# ═══════════════════════════════════════════════════════════════════
# DOCTRINE SEARCH
# ═══════════════════════════════════════════════════════════════════

class DoctrineSearcher:
    """
    Search doctrine cache by keyword matching and semantic similarity.

    Fallback chain:
        1. Exact keyword match (0-50ms)
        2. Fuzzy keyword match (50-200ms)
        3. Cloud semantic search (200-2000ms)
    """

    def __init__(self) -> None:
        self._doctrine_cache = DOCTRINE_CACHE
        self._keyword_index = self._build_keyword_index()

    def _build_keyword_index(self) -> dict:
        """Build inverted index of keywords to doctrine blocks."""
        index = {}
        for block in self._doctrine_cache:
            for keyword in block.keywords:
                keyword_lower = keyword.lower()
                if keyword_lower not in index:
                    index[keyword_lower] = []
                index[keyword_lower].append(block)
        logger.info(f"Built keyword index: {len(index)} unique keywords")
        return index

    def search_by_keywords(
        self,
        query_keywords: List[str],
        min_matches: int = 1,
    ) -> List[DoctrineBlock]:
        """
        Search doctrine cache by keyword matching.

        Args:
            query_keywords: Normalized query keywords
            min_matches: Minimum keyword matches required

        Returns:
            List of matching doctrine blocks, sorted by match count
        """
        match_counts = {}

        for keyword in query_keywords:
            keyword_lower = keyword.lower()
            if keyword_lower in self._keyword_index:
                for block in self._keyword_index[keyword_lower]:
                    match_counts[id(block)] = match_counts.get(id(block), 0) + 1

        # Filter by min_matches and sort by match count (descending)
        matched_blocks = [
            (block, count)
            for block in self._doctrine_cache
            if match_counts.get(id(block), 0) >= min_matches
        ]
        matched_blocks.sort(key=lambda x: match_counts.get(id(x[0]), 0), reverse=True)

        results = [block for block, _ in matched_blocks]
        logger.debug(f"Keyword search: {len(results)} doctrines matched")
        return results

    def search_by_topic(self, topic_substring: str) -> List[DoctrineBlock]:
        """Search by substring match in doctrine topic."""
        topic_lower = topic_substring.lower()
        matches = [
            block for block in self._doctrine_cache
            if topic_lower in block.topic.lower()
        ]
        logger.debug(f"Topic search '{topic_substring}': {len(matches)} matches")
        return matches

    def get_by_irc_section(self, section: str) -> List[DoctrineBlock]:
        """Get all doctrines related to an IRC section (e.g., '§162', '§199A')."""
        section_normalized = section.replace("§", "").replace(" ", "").lower()
        matches = []
        for block in self._doctrine_cache:
            # Check topic and keywords for IRC section
            if any(section_normalized in kw.replace("§", "").replace(" ", "").lower()
                   for kw in block.keywords + [block.topic]):
                matches.append(block)
        logger.debug(f"IRC section '{section}': {len(matches)} doctrines")
        return matches

    def get_high_confidence(self, min_confidence: float = 0.85) -> List[DoctrineBlock]:
        """Get all doctrines with confidence ≥ threshold."""
        matches = [block for block in self._doctrine_cache if block.confidence >= min_confidence]
        return matches

    def get_by_stratification(self, strat: str) -> List[DoctrineBlock]:
        """Get doctrines by confidence stratification (DEFENSIBLE, AGGRESSIVE, etc.)."""
        matches = [block for block in self._doctrine_cache if block.confidence_stratification == strat]
        return matches

    def get_tcja_impacted(self) -> List[DoctrineBlock]:
        """Get all doctrines with TCJA impact."""
        matches = [block for block in self._doctrine_cache if block.tcja_impact is not None]
        return matches


# ═══════════════════════════════════════════════════════════════════
# CLOUD SEMANTIC SEARCH FALLBACK
# ═══════════════════════════════════════════════════════════════════

async def cloud_semantic_search(
    query: str,
    top_k: int = 10,
) -> List[dict]:
    """
    Fallback to Cognition Cloud semantic search when doctrine cache misses.

    Uses CognitionCloudRetriever to fetch relevant tax knowledge from:
        - EKM (Enterprise Knowledge Management)
        - Crystal Memory
        - Knowledge Graph

    Returns:
        List of cloud knowledge records (dicts with id, content, relevance_score)
    """
    try:
        # Lazy import to avoid circular dependency and startup cost
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '_shared'))
        from cloud_retriever import CognitionCloudRetriever

        retriever = CognitionCloudRetriever()
        cloud_knowledge = await retriever.retrieve_all(
            query=query,
            category="tax_deductions",
            include_crystals=True,
            include_embeddings=False,
            ekm_limit=top_k,
            crystal_limit=5,
        )

        results = []
        for clause in cloud_knowledge.clauses:
            results.append({
                "id": clause.id,
                "title": clause.title,
                "content": clause.content,
                "relevance_score": clause.relevance_score,
                "source": "ekm",
            })

        for crystal in cloud_knowledge.crystals:
            results.append({
                "id": crystal.crystal_id,
                "title": crystal.topic,
                "content": crystal.content,
                "relevance_score": 0.8,  # Default crystal score
                "source": "crystal",
            })

        logger.info(f"Cloud semantic search: {len(results)} results from {len(cloud_knowledge.sources_succeeded)} sources")
        return results[:top_k]

    except Exception as e:
        logger.warning(f"Cloud semantic search failed: {e}")
        return []


# ═══════════════════════════════════════════════════════════════════
# MODULE SINGLETON
# ═══════════════════════════════════════════════════════════════════

_searcher: Optional[DoctrineSearcher] = None


def get_searcher() -> DoctrineSearcher:
    """Get or create module-level searcher singleton."""
    global _searcher
    if _searcher is None:
        _searcher = DoctrineSearcher()
    return _searcher
