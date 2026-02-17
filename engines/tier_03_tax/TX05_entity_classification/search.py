"""
TX05 Entity Classification Engine - Search Module
Vector and semantic search capabilities for entity classification
"""

from typing import List, Dict, Optional
from pathlib import Path
import json
from loguru import logger


class EntityClassificationSearch:
    """Search functionality for entity classification knowledge"""

    def __init__(self, cloud_retriever=None):
        """
        Initialize search module

        Args:
            cloud_retriever: Optional cloud-based retrieval service
        """
        self.cloud_retriever = cloud_retriever
        self.search_cache = {}

    def semantic_search(
        self,
        query: str,
        top_k: int = 5,
        filters: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Perform semantic search for entity classification content

        Args:
            query: Search query
            top_k: Number of results to return
            filters: Optional filters (entity_type, jurisdiction, etc.)

        Returns:
            List of search results with content and metadata
        """
        cache_key = f"{query}:{top_k}:{str(filters)}"

        if cache_key in self.search_cache:
            logger.debug(f"Cache hit for query: {query[:50]}")
            return self.search_cache[cache_key]

        if self.cloud_retriever:
            try:
                results = self.cloud_retriever.search(
                    query=query,
                    domain="entity_classification",
                    top_k=top_k,
                    filters=filters
                )
                self.search_cache[cache_key] = results
                return results
            except Exception as e:
                logger.warning(f"Cloud retrieval failed: {e}, using fallback")

        # Fallback to local search
        results = self._local_semantic_search(query, top_k, filters)
        self.search_cache[cache_key] = results
        return results

    def _local_semantic_search(
        self,
        query: str,
        top_k: int,
        filters: Optional[Dict]
    ) -> List[Dict]:
        """
        Local fallback semantic search

        Args:
            query: Search query
            top_k: Number of results
            filters: Optional filters

        Returns:
            List of search results
        """
        # This would integrate with local vector DB or keyword matching
        # For now, return empty list (cloud retriever handles actual search)
        logger.info(f"Local semantic search for: {query[:50]}")
        return []

    def search_by_entity_type(self, entity_type: str, top_k: int = 10) -> List[Dict]:
        """
        Search for content by entity type

        Args:
            entity_type: Entity type (LLC, corporation, partnership, etc.)
            top_k: Number of results

        Returns:
            List of relevant content
        """
        return self.semantic_search(
            query=f"entity classification {entity_type}",
            top_k=top_k,
            filters={'entity_type': entity_type}
        )

    def search_by_authority(
        self,
        authority_type: str,
        citation: Optional[str] = None,
        top_k: int = 10
    ) -> List[Dict]:
        """
        Search for content by authority type

        Args:
            authority_type: Type of authority (IRC, Treasury Regulation, case law, etc.)
            citation: Specific citation (e.g., "301.7701-3")
            top_k: Number of results

        Returns:
            List of relevant content
        """
        query = f"{authority_type}"
        if citation:
            query += f" {citation}"

        return self.semantic_search(
            query=query,
            top_k=top_k,
            filters={'authority_type': authority_type}
        )

    def search_conversion_scenarios(
        self,
        from_type: str,
        to_type: str,
        top_k: int = 5
    ) -> List[Dict]:
        """
        Search for entity conversion scenarios

        Args:
            from_type: Current entity classification
            to_type: Target entity classification
            top_k: Number of results

        Returns:
            List of conversion guidance
        """
        query = f"conversion from {from_type} to {to_type} tax consequences"
        return self.semantic_search(
            query=query,
            top_k=top_k,
            filters={'scenario_type': 'conversion'}
        )

    def search_election_procedures(
        self,
        election_type: str,
        top_k: int = 5
    ) -> List[Dict]:
        """
        Search for election procedures

        Args:
            election_type: Type of election (check-the-box, S corp, QSub, etc.)
            top_k: Number of results

        Returns:
            List of election guidance
        """
        query = f"{election_type} election procedure requirements"
        return self.semantic_search(
            query=query,
            top_k=top_k,
            filters={'topic': 'elections'}
        )

    def search_foreign_entity_guidance(
        self,
        country: Optional[str] = None,
        entity_form: Optional[str] = None,
        top_k: int = 5
    ) -> List[Dict]:
        """
        Search for foreign entity classification guidance

        Args:
            country: Country of formation
            entity_form: Foreign entity legal form
            top_k: Number of results

        Returns:
            List of foreign entity guidance
        """
        query = "foreign entity classification"
        if country:
            query += f" {country}"
        if entity_form:
            query += f" {entity_form}"

        return self.semantic_search(
            query=query,
            top_k=top_k,
            filters={'jurisdiction': 'foreign'}
        )

    def clear_cache(self):
        """Clear search cache"""
        self.search_cache = {}
        logger.info("Search cache cleared")


def create_search_engine(cloud_retriever=None) -> EntityClassificationSearch:
    """
    Factory function to create search engine

    Args:
        cloud_retriever: Optional cloud retrieval service

    Returns:
        Configured search engine
    """
    return EntityClassificationSearch(cloud_retriever=cloud_retriever)
