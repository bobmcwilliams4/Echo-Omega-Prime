"""
P08 Probate Procedure Engine - Vector Search Fallback
Semantic retrieval when doctrine cache misses.
"""

from typing import List, Dict, Any, Optional
import sys
from pathlib import Path

# Import shared cloud retriever
sys.path.insert(0, str(Path(__file__).parent.parent / "_shared"))

try:
    from cloud_retriever import CloudRetriever, SearchResult
    CLOUD_AVAILABLE = True
except ImportError:
    CLOUD_AVAILABLE = False
    CloudRetriever = None
    SearchResult = None


class VectorSearchFallback:
    """Semantic search fallback for probate procedure queries."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.enabled = config.get("vector_fallback_enabled", True) and CLOUD_AVAILABLE
        self.retriever: Optional[CloudRetriever] = None

        if self.enabled and CloudRetriever:
            try:
                self.retriever = CloudRetriever(
                    namespace="probate_procedure",
                    index_name="probate-procedure-index"
                )
            except Exception:
                self.enabled = False

    async def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Perform semantic search for probate procedure content.

        Args:
            query: Search query
            top_k: Number of results to return

        Returns:
            List of search results with metadata
        """
        if not self.enabled or not self.retriever:
            return []

        try:
            results = await self.retriever.search(query, top_k=top_k)
            return [self._format_result(r) for r in results]
        except Exception as e:
            # Log error but don't fail
            return []

    def _format_result(self, result: 'SearchResult') -> Dict[str, Any]:
        """Format search result for consumption."""
        return {
            "content": result.text,
            "score": result.score,
            "metadata": result.metadata,
            "source": result.metadata.get("source", "unknown"),
            "authority": result.metadata.get("authority", []),
            "confidence": result.score
        }

    async def hybrid_search(
        self,
        query: str,
        cache_results: List[Dict[str, Any]],
        top_k: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Combine cache results with vector search results.

        Args:
            query: Search query
            cache_results: Results from doctrine cache
            top_k: Number of vector results to add

        Returns:
            Combined and deduplicated results
        """
        vector_results = await self.search(query, top_k=top_k)

        # Merge results, preferring cache
        combined = cache_results.copy()
        cache_topics = {r.get("topic", "") for r in cache_results}

        for vr in vector_results:
            topic = vr.get("metadata", {}).get("topic", "")
            if topic not in cache_topics:
                combined.append(vr)

        return combined


class ProcedureKnowledgeBase:
    """Local knowledge base for probate procedure references."""

    def __init__(self):
        self.procedure_guides = self._load_procedure_guides()
        self.statutory_references = self._load_statutory_references()

    def _load_procedure_guides(self) -> Dict[str, str]:
        """Load procedure step-by-step guides."""
        return {
            "independent_administration": """
                INDEPENDENT ADMINISTRATION PROCEDURE:
                1. Verify will authorizes independent administration OR obtain beneficiary consent
                2. File application with probate court in domicile county
                3. Include death certificate, original will, list of heirs/beneficiaries
                4. Serve citation to interested parties
                5. Attend hearing (if contested) or submit on written approval
                6. Obtain court order admitting will and appointing independent executor
                7. Take oath and receive letters testamentary
                8. File inventory within 90 days
                9. Notify creditors and beneficiaries
                10. Administer estate (pay debts, distribute assets) without court approval
                11. File closing affidavit when complete
            """,

            "muniment_of_title": """
                MUNIMENT OF TITLE PROCEDURE:
                1. Verify estate has no unpaid debts (except real estate liens)
                2. File application with probate court in domicile county
                3. Include death certificate, original will, affidavit of no debts
                4. Serve citation to interested parties
                5. Attend hearing
                6. Court reviews will validity and debt affidavit
                7. Obtain court order admitting will as muniment of title
                8. Record certified copy with county clerk
                9. Use court order to transfer assets to beneficiaries
                10. No ongoing administration or inventory required
            """,

            "small_estate_affidavit": """
                SMALL ESTATE AFFIDAVIT PROCEDURE:
                1. Wait 30 days after death
                2. Verify estate value ≤ $75,000 (excluding homestead/exempt property)
                3. Prepare affidavit listing: decedent info, assets, debts, distributees
                4. Two disinterested witnesses sign affidavit
                5. File with county clerk (not probate court)
                6. Pay $15 filing fee
                7. Use affidavit to collect assets from holders
                8. Distribute to entitled parties
            """,

            "determination_of_heirship": """
                DETERMINATION OF HEIRSHIP PROCEDURE:
                1. File application with probate court
                2. List all known heirs with addresses and relationships
                3. Court appoints attorney ad litem for unknown heirs
                4. Serve citation to all known heirs
                5. Post/publish notice for unknown heirs
                6. Ad litem investigates and files report
                7. Hearing with evidence: birth/death certificates, witness testimony
                8. Court declares heirs and their shares
                9. Judgment serves as muniment of title or combine with administration
            """,

            "foreign_will": """
                FOREIGN WILL PROCEDURE:
                1. Obtain authenticated/exemplified copy of foreign probate order
                2. File with Texas probate court (county where Texas property located)
                3. Include affidavit from foreign executor/attorney
                4. Court admits foreign will (generally ministerial)
                5. If executor authority needed: file application for ancillary administration
                6. Court appoints Texas executor
                7. Texas executor administers Texas property only
            """,
        }

    def _load_statutory_references(self) -> Dict[str, List[str]]:
        """Load key statutory citations by topic."""
        return {
            "independent_administration": [
                "Texas Estates Code §401 (Authorization)",
                "Texas Estates Code §402 (Powers)",
                "Texas Estates Code §404 (Accounting)",
                "Texas Estates Code §309 (Inventory)"
            ],
            "muniment_of_title": [
                "Texas Estates Code §257.051 (Requirements)",
                "Texas Estates Code §257.101 (Effect)"
            ],
            "small_estate_affidavit": [
                "Texas Estates Code §205.001 (Eligibility)",
                "Texas Estates Code §205.002 (Procedure)",
                "Texas Estates Code §205.003 (Effect)"
            ],
            "determination_of_heirship": [
                "Texas Estates Code §202.005 (Procedure)",
                "Texas Estates Code §202.009 (Ad Litem)",
                "Texas Estates Code §202.201 (Judgment)"
            ],
            "foreign_will": [
                "Texas Estates Code §501.002 (Filing)",
                "Texas Estates Code §501.006 (Effect)"
            ],
            "venue": [
                "Texas Estates Code §33.001 (Domicile)",
                "Texas Estates Code §33.002 (Non-resident)",
                "Texas Estates Code §33.003 (Transfer)"
            ],
            "four_year_limitation": [
                "Texas Estates Code §256.003 (4-year limit)"
            ],
            "standing": [
                "Texas Estates Code §22.018 (Interested person)",
                "Texas Estates Code §256.204 (Contest period)"
            ],
        }

    def get_procedure_guide(self, procedure: str) -> Optional[str]:
        """Retrieve step-by-step guide for procedure."""
        return self.procedure_guides.get(procedure)

    def get_statutory_references(self, topic: str) -> List[str]:
        """Retrieve statutory citations for topic."""
        return self.statutory_references.get(topic, [])


# Singleton instance
_knowledge_base = ProcedureKnowledgeBase()


def get_procedure_guide(procedure: str) -> Optional[str]:
    """Public API: get procedure guide."""
    return _knowledge_base.get_procedure_guide(procedure)


def get_statutory_references(topic: str) -> List[str]:
    """Public API: get statutory references."""
    return _knowledge_base.get_statutory_references(topic)
