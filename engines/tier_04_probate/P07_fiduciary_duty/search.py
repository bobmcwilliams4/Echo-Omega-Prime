"""
P07 Fiduciary Duty Engine - Vector Search
Semantic retrieval fallback when doctrine cache misses
"""

from typing import List, Dict, Any, Optional
from pathlib import Path
import sys

# Add shared directory to path
shared_path = Path(__file__).parent.parent.parent / "APPS" / "_SHARED"
sys.path.insert(0, str(shared_path))

try:
    from cloud_retriever import CloudKnowledgeRetriever
    CLOUD_AVAILABLE = True
except ImportError:
    CLOUD_AVAILABLE = False
    print("Warning: CloudKnowledgeRetriever not available, using fallback")


class FiduciaryVectorSearch:
    """Vector-based semantic search for fiduciary duty knowledge"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.cloud_retriever = None

        if CLOUD_AVAILABLE:
            try:
                self.cloud_retriever = CloudKnowledgeRetriever(
                    domain="fiduciary_law",
                    jurisdiction="texas"
                )
            except Exception as e:
                print(f"Cloud retriever initialization failed: {e}")

    def search(
        self,
        query: str,
        top_k: int = 5,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Perform semantic search for fiduciary duty knowledge

        Args:
            query: Search query
            top_k: Number of results to return
            filters: Optional filters (issue_category, confidence_level, etc.)

        Returns:
            List of search results with relevance scores
        """
        if self.cloud_retriever:
            return self._cloud_search(query, top_k, filters)
        else:
            return self._fallback_search(query, top_k, filters)

    def _cloud_search(
        self,
        query: str,
        top_k: int,
        filters: Optional[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Search using cloud vector database"""
        try:
            # Build filter dict for cloud retriever
            search_filters = {}
            if filters:
                if "issue_category" in filters:
                    search_filters["category"] = filters["issue_category"]
                if "confidence_level" in filters:
                    search_filters["confidence"] = filters["confidence_level"]

            results = self.cloud_retriever.search(
                query=query,
                top_k=top_k,
                filters=search_filters
            )

            # Transform results to engine format
            formatted_results = []
            for result in results:
                formatted_results.append({
                    "content": result.get("text", ""),
                    "source": result.get("source", "Cloud Knowledge Base"),
                    "relevance_score": result.get("score", 0.0),
                    "metadata": result.get("metadata", {}),
                    "citations": result.get("citations", [])
                })

            return formatted_results

        except Exception as e:
            print(f"Cloud search failed: {e}, falling back to local search")
            return self._fallback_search(query, top_k, filters)

    def _fallback_search(
        self,
        query: str,
        top_k: int,
        filters: Optional[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Fallback search using keyword matching
        Used when cloud retriever unavailable
        """
        # Load local knowledge snippets
        local_knowledge = self._load_local_knowledge()

        # Score results by keyword overlap
        scored_results = []
        query_terms = set(query.lower().split())

        for snippet in local_knowledge:
            # Skip if filters don't match
            if filters:
                if "issue_category" in filters and snippet.get("category") != filters["issue_category"]:
                    continue
                if "confidence_level" in filters and snippet.get("confidence") != filters["confidence_level"]:
                    continue

            # Calculate keyword overlap score
            snippet_terms = set(snippet["content"].lower().split())
            overlap = len(query_terms & snippet_terms)
            score = overlap / max(len(query_terms), 1)

            if score > 0:
                scored_results.append({
                    "content": snippet["content"],
                    "source": snippet.get("source", "Local Knowledge"),
                    "relevance_score": score,
                    "metadata": snippet.get("metadata", {}),
                    "citations": snippet.get("citations", [])
                })

        # Sort by score and return top_k
        scored_results.sort(key=lambda x: x["relevance_score"], reverse=True)
        return scored_results[:top_k]

    def _load_local_knowledge(self) -> List[Dict[str, Any]]:
        """Load local fiduciary duty knowledge snippets"""
        return [
            {
                "content": "TX Estates Code §351.101 imposes comprehensive fiduciary duties on executors including loyalty, care, impartiality, and accounting. Independent executor status grants broader powers but identical duty standards.",
                "source": "TX Estates Code §351.101",
                "category": "EXECUTOR_DUTIES",
                "confidence": "DEFENSIBLE",
                "citations": ["TX Estates Code §351.101"],
                "metadata": {"statute": True}
            },
            {
                "content": "The duty of loyalty requires fiduciary to act solely in beneficiaries' interest. Self-dealing transactions voidable per se under 'no further inquiry' rule established in Slay v. Burnett Trust.",
                "source": "Slay v. Burnett Trust, 187 S.W.2d 377 (Tex. 1945)",
                "category": "SELF_DEALING",
                "confidence": "DEFENSIBLE",
                "citations": ["Slay v. Burnett Trust, 187 S.W.2d 377 (Tex. 1945)"],
                "metadata": {"case_law": True}
            },
            {
                "content": "TX Property Code Chapter 117 adopted Uniform Prudent Investor Act. Investments evaluated based on total portfolio approach, not isolation. Diversification presumed prudent unless special circumstances justify concentration.",
                "source": "TX Property Code §117.004",
                "category": "INVESTMENT_PRUDENCE",
                "confidence": "DEFENSIBLE",
                "citations": ["TX Property Code §117.004", "TX Property Code §117.005"],
                "metadata": {"statute": True}
            },
            {
                "content": "Surcharge remedy requires fiduciary to restore estate/trust to position it would occupy absent breach. Calculation methods include direct loss, lost profits, profit disgorgement, or appreciation in value.",
                "source": "Humane Society v. Austin National Bank, 531 S.W.2d 574 (Tex. 1975)",
                "category": "SURCHARGE_LIABILITY",
                "confidence": "AGGRESSIVE",
                "citations": ["Humane Society v. Austin National Bank, 531 S.W.2d 574 (Tex. 1975)", "TX Property Code §114.008"],
                "metadata": {"case_law": True}
            },
            {
                "content": "TX Property Code §114.007 limits exculpatory clauses. Cannot excuse bad faith, reckless indifference, or intentional failure to act impartially. Clause drafted by trustee invalid unless proves fairness and adequate communication.",
                "source": "TX Property Code §114.007",
                "category": "EXCULPATORY_CLAUSES",
                "confidence": "AGGRESSIVE",
                "citations": ["TX Property Code §114.007"],
                "metadata": {"statute": True}
            },
            {
                "content": "Executors must file inventory and appraisement within 90 days under §309.051. Annual accountings required for dependent administration. Failure to account extends statute of limitations per Huie v. DeShazo.",
                "source": "TX Estates Code §309.051",
                "category": "ACCOUNTING_DISCLOSURE",
                "confidence": "DEFENSIBLE",
                "citations": ["TX Estates Code §309.051", "Huie v. DeShazo, 922 S.W.2d 920 (Tex. 1996)"],
                "metadata": {"statute": True}
            },
            {
                "content": "Corporate and professional fiduciaries held to higher standard under §114.006(b). Must exercise special skills and expertise. Industry standards and best practices relevant to standard of care.",
                "source": "TX Property Code §114.006(b)",
                "category": "CORPORATE_FIDUCIARY",
                "confidence": "DEFENSIBLE",
                "citations": ["TX Property Code §114.006(b)", "Montgomery v. Kennedy, 669 S.W.2d 309 (Tex. 1984)"],
                "metadata": {"statute": True}
            },
            {
                "content": "Guardian of person makes personal care decisions; guardian of estate manages financial affairs. TX Estates Code Chapter 1151 establishes distinct duties for each guardian type.",
                "source": "TX Estates Code Chapter 1151",
                "category": "GUARDIAN_DUTIES",
                "confidence": "DEFENSIBLE",
                "citations": ["TX Estates Code §1151.051", "TX Estates Code §1151.151"],
                "metadata": {"statute": True}
            },
            {
                "content": "Co-trustees must act unanimously unless trust authorizes majority rule. Each co-trustee has duty to monitor and prevent co-trustee's breach. Liability joint and several for breaches participated in or failed to prevent.",
                "source": "TX Property Code §113.085",
                "category": "TRUSTEE_DUTIES",
                "confidence": "DEFENSIBLE",
                "citations": ["TX Property Code §113.085"],
                "metadata": {"statute": True}
            },
            {
                "content": "Delegation permitted under §117.011 but fiduciary must prudently select, instruct, and monitor agents. Cannot delegate ultimate responsibility or discretionary decisions reserved to fiduciary.",
                "source": "TX Property Code §117.011",
                "category": "TRUSTEE_DUTIES",
                "confidence": "AGGRESSIVE",
                "citations": ["TX Property Code §117.011", "TX Property Code §114.0031"],
                "metadata": {"statute": True}
            },
            {
                "content": "Court may remove fiduciary for material breach under §404.003 but removal discretionary. Must find statutory ground exists AND removal in best interests of estate/trust.",
                "source": "TX Estates Code §404.003",
                "category": "REMOVAL_GROUNDS",
                "confidence": "AGGRESSIVE",
                "citations": ["TX Estates Code §404.003", "Pool v. Pool, 290 S.W.3d 564 (Tex. App. 2009)"],
                "metadata": {"statute": True}
            },
            {
                "content": "Trustee entitled to reasonable compensation under §114.061. Factors include time/effort, skill required, trust size, results obtained, and customary fees. Court may reduce if unreasonable or breach occurred.",
                "source": "TX Property Code §114.061",
                "category": "TRUSTEE_DUTIES",
                "confidence": "AGGRESSIVE",
                "citations": ["TX Property Code §114.061"],
                "metadata": {"statute": True}
            }
        ]

    def search_by_citation(self, citation: str) -> List[Dict[str, Any]]:
        """Search for knowledge by statutory or case citation"""
        local_knowledge = self._load_local_knowledge()

        results = []
        citation_lower = citation.lower()

        for snippet in local_knowledge:
            snippet_citations = [c.lower() for c in snippet.get("citations", [])]
            if any(citation_lower in sc for sc in snippet_citations):
                results.append({
                    "content": snippet["content"],
                    "source": snippet.get("source", ""),
                    "relevance_score": 1.0,
                    "metadata": snippet.get("metadata", {}),
                    "citations": snippet.get("citations", [])
                })

        return results

    def search_by_category(self, category: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """Search for knowledge by issue category"""
        return self.search(
            query=category.lower().replace("_", " "),
            top_k=top_k,
            filters={"issue_category": category}
        )

    def hybrid_search(
        self,
        query: str,
        keywords: List[str],
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Hybrid search combining semantic and keyword approaches

        Args:
            query: Semantic search query
            keywords: Specific keywords to boost
            top_k: Number of results

        Returns:
            Combined and deduplicated results
        """
        # Get semantic results
        semantic_results = self.search(query, top_k=top_k * 2)

        # Get keyword results
        keyword_query = " ".join(keywords)
        keyword_results = self._fallback_search(keyword_query, top_k=top_k, filters=None)

        # Combine and deduplicate
        seen_content = set()
        combined = []

        for result in semantic_results + keyword_results:
            content_hash = hash(result["content"][:100])  # Hash first 100 chars
            if content_hash not in seen_content:
                seen_content.add(content_hash)
                combined.append(result)

        # Re-sort by relevance
        combined.sort(key=lambda x: x["relevance_score"], reverse=True)
        return combined[:top_k]
