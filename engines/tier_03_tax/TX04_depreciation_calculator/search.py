"""
TX04 Depreciation Calculator - Vector Search Fallback
Semantic retrieval when doctrine cache misses.
"""

from typing import List, Dict, Any, Optional
import sys
from pathlib import Path

# Import shared cloud retriever
sys.path.insert(0, str(Path(__file__).parent.parent / "_shared"))

try:
    from cloud_retriever import CloudflareVectorSearch
except ImportError:
    CloudflareVectorSearch = None


class DepreciationVectorSearch:
    """Vector search for depreciation knowledge retrieval."""

    def __init__(self, vectorize_index: str = "depreciation-knowledge"):
        """
        Initialize vector search.

        Args:
            vectorize_index: Cloudflare Vectorize index name
        """
        self.vectorize_index = vectorize_index
        self.cloud_search = None

        if CloudflareVectorSearch:
            try:
                self.cloud_search = CloudflareVectorSearch(
                    account_id="your_account_id",  # Replace with actual account ID
                    index_name=vectorize_index
                )
            except Exception:
                # Fallback: vector search unavailable
                pass

    async def search(
        self,
        query: str,
        top_k: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search depreciation knowledge base.

        Args:
            query: Search query
            top_k: Number of results to return
            filter_metadata: Optional metadata filters

        Returns:
            List of search results with scores
        """
        if not self.cloud_search:
            return []

        try:
            results = await self.cloud_search.search(
                query=query,
                top_k=top_k,
                filter_metadata=filter_metadata
            )
            return results
        except Exception:
            return []

    async def search_by_section(self, section: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search by IRC section.

        Args:
            section: IRC section (e.g., "168", "179", "1245")
            top_k: Number of results

        Returns:
            List of results for that section
        """
        filter_metadata = {"irc_section": section}
        return await self.search(
            query=f"IRC Section {section}",
            top_k=top_k,
            filter_metadata=filter_metadata
        )

    async def search_by_property_type(
        self,
        property_type: str,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search by property type.

        Args:
            property_type: 'personal', 'real', 'intangible'
            top_k: Number of results

        Returns:
            List of results for property type
        """
        filter_metadata = {"property_type": property_type}
        return await self.search(
            query=f"{property_type} property depreciation",
            top_k=top_k,
            filter_metadata=filter_metadata
        )

    async def search_by_recovery_period(
        self,
        recovery_period: str,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search by MACRS recovery period.

        Args:
            recovery_period: '3', '5', '7', '10', '15', '20', '27.5', '39'
            top_k: Number of results

        Returns:
            List of results for recovery period
        """
        filter_metadata = {"recovery_period": recovery_period}
        return await self.search(
            query=f"{recovery_period} year MACRS depreciation",
            top_k=top_k,
            filter_metadata=filter_metadata
        )

    def format_results(self, results: List[Dict[str, Any]]) -> str:
        """
        Format search results for display.

        Args:
            results: List of search results

        Returns:
            Formatted text
        """
        if not results:
            return "No relevant results found in knowledge base."

        formatted = ["Vector Search Results:\n"]
        for i, result in enumerate(results, 1):
            score = result.get("score", 0.0)
            text = result.get("text", "")
            metadata = result.get("metadata", {})

            formatted.append(f"{i}. [Score: {score:.3f}]")
            if metadata:
                formatted.append(f"   Metadata: {metadata}")
            formatted.append(f"   {text[:200]}...")
            formatted.append("")

        return "\n".join(formatted)


class LocalDepreciationSearch:
    """Local fallback search using keyword matching."""

    def __init__(self):
        """Initialize local search with depreciation knowledge snippets."""
        self.knowledge_snippets = [
            {
                "text": "MACRS recovery periods: 3-year (race horses), 5-year (computers, cars), "
                        "7-year (furniture, equipment), 15-year (land improvements), "
                        "27.5-year (residential rental), 39-year (commercial buildings)",
                "keywords": ["macrs", "recovery period", "class life"],
                "section": "168"
            },
            {
                "text": "Section 179 expensing: $1,160,000 limit (2024), phases out at $2,890,000. "
                        "Limited to taxable income from active business. Excess carries forward.",
                "keywords": ["179", "expensing", "dollar limit"],
                "section": "179"
            },
            {
                "text": "Bonus depreciation: 60% for 2024, phases to 40% (2025), 20% (2026), 0% (2027+). "
                        "Applies to new and used property with 20-year or less recovery period.",
                "keywords": ["bonus", "168k", "first year"],
                "section": "168k"
            },
            {
                "text": "Luxury auto limits (2024): $12,200 first year (no bonus), $20,200 (with bonus), "
                        "$19,600 second year, $11,800 third year, $7,160 thereafter. "
                        "Vehicles over 6,000 lbs GVWR exempt.",
                "keywords": ["luxury auto", "280f", "automobile", "vehicle"],
                "section": "280F"
            },
            {
                "text": "Section 1245 recapture: All depreciation recaptured as ordinary income on sale "
                        "of personal property, limited to gain realized.",
                "keywords": ["1245", "recapture", "personal property"],
                "section": "1245"
            },
            {
                "text": "Section 1250 recapture: Excess accelerated over straight-line for real property. "
                        "Post-1986 MACRS property has no recapture, but unrecaptured §1250 gain "
                        "taxed at 25% maximum.",
                "keywords": ["1250", "recapture", "real property", "25%"],
                "section": "1250"
            },
            {
                "text": "Mid-quarter convention applies if >40% of personal property placed in service "
                        "in Q4. Significantly reduces first-year depreciation for Q4 assets (12.5% vs 50%).",
                "keywords": ["mid-quarter", "40%", "convention", "q4"],
                "section": "168d"
            },
            {
                "text": "Qualified Improvement Property (QIP): Interior improvements to nonresidential buildings. "
                        "15-year recovery period, eligible for bonus depreciation post-TCJA.",
                "keywords": ["qip", "qualified improvement", "leasehold"],
                "section": "168"
            },
            {
                "text": "Alternative Depreciation System (ADS): Required for tax-exempt use property, "
                        "farming with election, certain imported property. Uses straight-line method "
                        "with longer recovery periods.",
                "keywords": ["ads", "alternative", "straight-line"],
                "section": "168g"
            },
            {
                "text": "Section 197 intangibles: Goodwill, customer lists, covenants not to compete, "
                        "franchises amortized straight-line over 15 years. No other method allowed.",
                "keywords": ["197", "intangible", "goodwill", "amortization"],
                "section": "197"
            }
        ]

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Local keyword search.

        Args:
            query: Search query
            top_k: Number of results

        Returns:
            List of matching snippets with scores
        """
        query_lower = query.lower()
        results = []

        for snippet in self.knowledge_snippets:
            score = 0.0

            # Keyword matching
            for keyword in snippet["keywords"]:
                if keyword in query_lower:
                    score += 1.0

            # Section matching
            if snippet["section"].lower() in query_lower:
                score += 2.0

            if score > 0:
                results.append({
                    "text": snippet["text"],
                    "score": score,
                    "metadata": {"section": snippet["section"]}
                })

        # Sort by score descending
        results.sort(key=lambda x: x["score"], reverse=True)

        return results[:top_k]
