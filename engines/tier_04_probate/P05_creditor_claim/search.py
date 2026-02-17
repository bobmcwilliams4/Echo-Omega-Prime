"""
P05 Creditor Claim Engine - Search Module
Vector search fallback for creditor claim doctrine retrieval
"""

from typing import List, Dict, Optional, Any
from dataclasses import dataclass
import sys
from pathlib import Path
from loguru import logger

# Import shared cloud retriever
sys.path.insert(0, str(Path(__file__).parent.parent / "_shared"))

try:
    from cloud_retriever import CloudKnowledgeRetriever, SearchResult
    CLOUD_AVAILABLE = True
except ImportError:
    logger.warning("Cloud retriever not available, search will be limited")
    CLOUD_AVAILABLE = False

    @dataclass
    class SearchResult:
        content: str
        score: float
        source: str
        metadata: Dict[str, Any]


class CreditorClaimSearchEngine:
    """Vector search for creditor claim knowledge base"""

    def __init__(self, engine_id: str = "P05_creditor_claim"):
        self.engine_id = engine_id
        self.cloud_retriever: Optional[Any] = None

        if CLOUD_AVAILABLE:
            try:
                self.cloud_retriever = CloudKnowledgeRetriever(
                    namespace=f"creditor_claim_{engine_id}",
                    endpoint_url="https://cognition-ekm.bmcii1976.workers.dev"
                )
                logger.info("Cloud knowledge retriever initialized for creditor claims")
            except Exception as e:
                logger.warning(f"Cloud retriever initialization failed: {e}")
                self.cloud_retriever = None

    def semantic_search(
        self,
        query: str,
        top_k: int = 5,
        threshold: float = 0.75,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[SearchResult]:
        """
        Perform semantic search for creditor claim knowledge

        Args:
            query: Search query
            top_k: Number of results to return
            threshold: Minimum similarity threshold
            filters: Optional metadata filters

        Returns:
            List of search results with scores
        """
        if not self.cloud_retriever:
            logger.warning("Cloud retriever not available, returning empty results")
            return self._fallback_search(query, top_k)

        try:
            results = self.cloud_retriever.search(
                query=query,
                top_k=top_k,
                threshold=threshold,
                filters=filters or {}
            )

            logger.info(f"Semantic search returned {len(results)} results for query: {query[:50]}")
            return results

        except Exception as e:
            logger.error(f"Semantic search failed: {e}")
            return self._fallback_search(query, top_k)

    def search_by_category(
        self,
        query: str,
        claim_category: str,
        top_k: int = 3
    ) -> List[SearchResult]:
        """Search within a specific claim category"""
        filters = {"claim_category": claim_category}
        return self.semantic_search(query, top_k=top_k, filters=filters)

    def search_by_statute(
        self,
        query: str,
        statute_cite: str,
        top_k: int = 3
    ) -> List[SearchResult]:
        """Search within a specific statute"""
        filters = {"statute": statute_cite}
        return self.semantic_search(query, top_k=top_k, filters=filters)

    def multi_category_search(
        self,
        query: str,
        categories: List[str],
        top_k: int = 10
    ) -> Dict[str, List[SearchResult]]:
        """Search across multiple claim categories"""
        results = {}

        for category in categories:
            category_results = self.search_by_category(query, category, top_k=top_k)
            if category_results:
                results[category] = category_results

        return results

    def search_exemption_law(self, query: str, top_k: int = 5) -> List[SearchResult]:
        """Search specifically for exemption law"""
        filters = {"topic": "exemptions"}
        return self.semantic_search(query, top_k=top_k, filters=filters)

    def search_priority_rules(self, query: str, top_k: int = 5) -> List[SearchResult]:
        """Search for claim priority rules"""
        filters = {"topic": "priority"}
        return self.semantic_search(query, top_k=top_k, filters=filters)

    def search_procedures(self, query: str, top_k: int = 5) -> List[SearchResult]:
        """Search for filing procedures and deadlines"""
        filters = {"topic": "procedures"}
        return self.semantic_search(query, top_k=top_k, filters=filters)

    def _fallback_search(self, query: str, top_k: int) -> List[SearchResult]:
        """Fallback search using local keyword matching"""
        # Simple keyword-based fallback
        keywords = query.lower().split()

        creditor_knowledge_base = [
            {
                "content": "Secured claims are claims backed by collateral under TEC §355.064. Secured creditors may elect to have their claim classified as a matured secured claim or as a preferred debt and lien against specific estate property.",
                "keywords": ["secured", "claim", "collateral", "lien", "mortgage", "355.064"],
                "source": "TEC_355.064",
                "category": "SECURED_CLAIMS"
            },
            {
                "content": "Notice to creditors must be published in accordance with TEC §308.053. Personal service or certified mail is required for secured creditors and creditors with claims of $500 or more. Publication notice gives general creditors 4 months from notice date.",
                "keywords": ["notice", "creditors", "publication", "308.053", "deadline", "certified mail"],
                "source": "TEC_308.053",
                "category": "PROCEDURES"
            },
            {
                "content": "Claim priority order under TEC §355.102: (1) funeral expenses, (2) expenses of last illness, (3) family allowance, (4) exempt property, (5) secured claims, (6) child support, (7) claims for personal services, (8) other claims.",
                "keywords": ["priority", "355.102", "funeral", "family allowance", "secured", "order"],
                "source": "TEC_355.102",
                "category": "PRIORITY"
            },
            {
                "content": "Homestead exemption under Texas Constitution Article XVI Section 50 protects the family homestead from forced sale for most creditor claims. Urban homestead limited to 10 acres, rural to 100 acres. Unlimited value protection.",
                "keywords": ["homestead", "exemption", "constitution", "protected", "forced sale", "urban", "rural"],
                "source": "TX_CONST_XVI_50",
                "category": "EXEMPTIONS"
            },
            {
                "content": "Family allowance under TEC §353.101 allows court to set aside property for surviving spouse and minor children for one year. This allowance takes priority over most claims except funeral and administration expenses.",
                "keywords": ["family allowance", "353.101", "surviving spouse", "minor children", "priority"],
                "source": "TEC_353.101",
                "category": "EXEMPTIONS"
            },
        ]

        # Score each item based on keyword matches
        scored_items = []
        for item in creditor_knowledge_base:
            score = sum(1 for keyword in keywords if keyword in item["keywords"]) / len(keywords)
            if score > 0:
                scored_items.append((score, item))

        # Sort by score and take top_k
        scored_items.sort(reverse=True, key=lambda x: x[0])
        top_items = scored_items[:top_k]

        results = [
            SearchResult(
                content=item["content"],
                score=score,
                source=item["source"],
                metadata={"category": item["category"]}
            )
            for score, item in top_items
        ]

        logger.info(f"Fallback search returned {len(results)} results")
        return results

    def health_check(self) -> Dict[str, Any]:
        """Check search engine health"""
        status = {
            "engine_id": self.engine_id,
            "cloud_available": CLOUD_AVAILABLE,
            "cloud_connected": self.cloud_retriever is not None
        }

        if self.cloud_retriever:
            try:
                test_results = self.semantic_search("test query", top_k=1)
                status["test_search"] = "SUCCESS"
                status["test_results_count"] = len(test_results)
            except Exception as e:
                status["test_search"] = "FAILED"
                status["error"] = str(e)
        else:
            status["mode"] = "FALLBACK_ONLY"

        return status
