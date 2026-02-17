"""
P04 Estate Asset Mapper - Vector Search Fallback
Cloud retriever integration for semantic search when doctrine cache misses.
"""

from typing import List, Dict, Any, Optional
from pathlib import Path
import sys

# Add parent directory to path for cloud_retriever import
sys.path.insert(0, str(Path(__file__).parent.parent / "_shared"))

try:
    from cloud_retriever import CloudRetriever
    CLOUD_RETRIEVER_AVAILABLE = True
except ImportError:
    CLOUD_RETRIEVER_AVAILABLE = False


class EstateAssetVectorSearch:
    """
    Vector search fallback for estate asset mapping queries.
    Integrates with cloud knowledge base when doctrine cache insufficient.
    """

    def __init__(self, retriever: Optional[Any] = None):
        """
        Initialize vector search with cloud retriever.

        Args:
            retriever: CloudRetriever instance (optional, will create if None)
        """
        self.retriever = retriever
        if self.retriever is None and CLOUD_RETRIEVER_AVAILABLE:
            try:
                self.retriever = CloudRetriever(
                    namespace="estate_planning",
                    embedding_model="text-embedding-3-small"
                )
            except Exception:
                self.retriever = None

    def search(
        self,
        query: str,
        top_k: int = 5,
        min_score: float = 0.7,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Semantic search for estate planning knowledge.

        Args:
            query: Natural language query
            top_k: Number of results to return
            min_score: Minimum similarity score (0-1)
            filters: Optional metadata filters

        Returns:
            List of search results with content, metadata, score
        """
        if not self.retriever:
            return []

        try:
            results = self.retriever.search(
                query=query,
                top_k=top_k,
                min_score=min_score,
                filters=filters
            )
            return results
        except Exception:
            return []

    def search_by_irc_section(
        self,
        irc_section: str,
        query: str,
        top_k: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Search for content related to specific IRC section.

        Args:
            irc_section: IRC section (e.g., "2031", "2036", "2040")
            query: Additional context query
            top_k: Number of results

        Returns:
            List of results filtered to IRC section
        """
        filters = {"irc_section": irc_section}
        return self.search(query=query, top_k=top_k, filters=filters)

    def search_valuation_methods(
        self,
        asset_type: str,
        top_k: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Search for valuation methods for specific asset type.

        Args:
            asset_type: Asset type (e.g., "real_property", "closely_held_business")
            top_k: Number of results

        Returns:
            Valuation guidance for asset type
        """
        query = f"valuation method for {asset_type}"
        filters = {"topic": "valuation"}
        return self.search(query=query, top_k=top_k, filters=filters)

    def search_discount_guidance(
        self,
        discount_type: str,
        top_k: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Search for discount applicability guidance.

        Args:
            discount_type: Type of discount (e.g., "dlom", "dloc", "fractional_interest")
            top_k: Number of results

        Returns:
            Discount guidance and case law
        """
        query = f"{discount_type} discount estate tax"
        filters = {"topic": "discounts"}
        return self.search(query=query, top_k=top_k, filters=filters)

    def search_case_law(
        self,
        issue: str,
        jurisdiction: Optional[str] = None,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search for relevant case law.

        Args:
            issue: Legal issue (e.g., "FLP inclusion", "fractional interest discount")
            jurisdiction: Optional jurisdiction filter (e.g., "5th Circuit", "Tax Court")
            top_k: Number of results

        Returns:
            Relevant case law
        """
        query = f"{issue} case law estate tax"
        filters = {"content_type": "case_law"}
        if jurisdiction:
            filters["jurisdiction"] = jurisdiction
        return self.search(query=query, top_k=top_k, filters=filters)

    def search_texas_law(
        self,
        topic: str,
        top_k: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Search for Texas-specific law (community property, partition, etc.).

        Args:
            topic: Texas law topic
            top_k: Number of results

        Returns:
            Texas law guidance
        """
        query = f"Texas {topic}"
        filters = {"jurisdiction": "Texas"}
        return self.search(query=query, top_k=top_k, filters=filters)

    def search_form_706_guidance(
        self,
        schedule: str,
        top_k: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Search for Form 706 reporting guidance.

        Args:
            schedule: Form 706 schedule (e.g., "Schedule A", "Schedule D")
            top_k: Number of results

        Returns:
            Form 706 reporting instructions
        """
        query = f"Form 706 {schedule} reporting instructions"
        filters = {"content_type": "form_instructions"}
        return self.search(query=query, top_k=top_k, filters=filters)

    def multi_source_search(
        self,
        query: str,
        search_strategies: List[str],
        top_k_per_strategy: int = 2
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Execute multiple search strategies and combine results.

        Args:
            query: Base query
            search_strategies: List of strategy names (e.g., ["irc", "case_law", "valuation"])
            top_k_per_strategy: Results per strategy

        Returns:
            Dict mapping strategy name to results
        """
        results = {}

        if "irc" in search_strategies:
            results["irc"] = self.search(
                query=query,
                top_k=top_k_per_strategy,
                filters={"content_type": "statute"}
            )

        if "case_law" in search_strategies:
            results["case_law"] = self.search_case_law(
                issue=query,
                top_k=top_k_per_strategy
            )

        if "valuation" in search_strategies:
            results["valuation"] = self.search(
                query=query,
                top_k=top_k_per_strategy,
                filters={"topic": "valuation"}
            )

        if "discounts" in search_strategies:
            results["discounts"] = self.search(
                query=query,
                top_k=top_k_per_strategy,
                filters={"topic": "discounts"}
            )

        if "texas" in search_strategies:
            results["texas"] = self.search_texas_law(
                topic=query,
                top_k=top_k_per_strategy
            )

        return results

    def is_available(self) -> bool:
        """Check if cloud retriever is available and functional."""
        return self.retriever is not None and CLOUD_RETRIEVER_AVAILABLE


# ═══════════════════════════════════════════════════════════════════════════
# MODULE-LEVEL SINGLETON
# ═══════════════════════════════════════════════════════════════════════════

_search_instance = None


def get_vector_search() -> EstateAssetVectorSearch:
    """Get singleton vector search instance."""
    global _search_instance
    if _search_instance is None:
        _search_instance = EstateAssetVectorSearch()
    return _search_instance
