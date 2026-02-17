"""
Search Module
R03 Compliance Checker Engine

Fallback search capabilities (semantic retrieval not primary for rule-based engine)
"""

from typing import List, Dict, Optional
import sys
from pathlib import Path

# Add shared module path
shared_path = Path(__file__).parent.parent / "_shared"
if str(shared_path) not in sys.path:
    sys.path.insert(0, str(shared_path))

try:
    from cloud_retriever import CloudRetriever
    CLOUD_AVAILABLE = True
except ImportError:
    CLOUD_AVAILABLE = False


class ComplianceSearchEngine:
    """
    Search engine for regulatory compliance information.

    Primary reliance on doctrine cache (rule-based).
    Cloud retrieval used only for novel/complex queries not in cache.
    """

    def __init__(self, config: Dict):
        self.config = config
        self.cloud_retriever = None

        if CLOUD_AVAILABLE and config.get("semantic_fallback_enabled", True):
            try:
                self.cloud_retriever = CloudRetriever(
                    bucket_name="echo-prime-knowledge",
                    collection_prefix="compliance"
                )
            except Exception:
                self.cloud_retriever = None

    def search_regulations(
        self,
        query: str,
        authorities: Optional[List[str]] = None,
        top_k: int = 5
    ) -> List[Dict]:
        """
        Search regulatory information via cloud retrieval.

        Args:
            query: Search query (normalized)
            authorities: Filter by regulatory authorities (RRC, TCEQ, EPA, etc.)
            top_k: Number of results to return

        Returns:
            List of search results with text, source, and score
        """
        if not self.cloud_retriever:
            return []

        try:
            # Build filter based on authorities
            filter_dict = {}
            if authorities:
                filter_dict["authority"] = {"$in": authorities}

            results = self.cloud_retriever.search(
                query_text=query,
                top_k=top_k,
                filter_dict=filter_dict if filter_dict else None
            )

            return [
                {
                    "text": r.get("text", ""),
                    "source": r.get("metadata", {}).get("source", "Unknown"),
                    "authority": r.get("metadata", {}).get("authority", "Unknown"),
                    "rule_citation": r.get("metadata", {}).get("rule_citation", ""),
                    "score": r.get("score", 0.0),
                }
                for r in results
            ]
        except Exception as e:
            # Log error but don't fail - return empty results
            return []

    def search_similar_violations(
        self,
        violation_description: str,
        top_k: int = 3
    ) -> List[Dict]:
        """
        Search for similar violation cases and enforcement actions.

        Args:
            violation_description: Description of the violation scenario
            top_k: Number of similar cases to return

        Returns:
            List of similar violation cases with outcomes
        """
        if not self.cloud_retriever:
            return []

        # Prefix query to focus on enforcement/violation documents
        enforcement_query = f"enforcement action violation penalty: {violation_description}"

        try:
            results = self.cloud_retriever.search(
                query_text=enforcement_query,
                top_k=top_k,
                filter_dict={"document_type": "enforcement"}
            )

            return [
                {
                    "case_summary": r.get("text", ""),
                    "violation_type": r.get("metadata", {}).get("violation_type", ""),
                    "penalty_amount": r.get("metadata", {}).get("penalty_amount", ""),
                    "authority": r.get("metadata", {}).get("authority", ""),
                    "outcome": r.get("metadata", {}).get("outcome", ""),
                    "score": r.get("score", 0.0),
                }
                for r in results
            ]
        except Exception:
            return []

    def search_guidance_documents(
        self,
        topic: str,
        authority: Optional[str] = None,
        top_k: int = 3
    ) -> List[Dict]:
        """
        Search for regulatory guidance documents and interpretations.

        Args:
            topic: Topic or subject matter
            authority: Specific regulatory authority (RRC, TCEQ, EPA)
            top_k: Number of guidance documents to return

        Returns:
            List of guidance documents
        """
        if not self.cloud_retriever:
            return []

        try:
            filter_dict = {"document_type": "guidance"}
            if authority:
                filter_dict["authority"] = authority

            results = self.cloud_retriever.search(
                query_text=topic,
                top_k=top_k,
                filter_dict=filter_dict
            )

            return [
                {
                    "title": r.get("metadata", {}).get("title", ""),
                    "summary": r.get("text", ""),
                    "authority": r.get("metadata", {}).get("authority", ""),
                    "publication_date": r.get("metadata", {}).get("publication_date", ""),
                    "url": r.get("metadata", {}).get("url", ""),
                    "score": r.get("score", 0.0),
                }
                for r in results
            ]
        except Exception:
            return []

    def search_compliance_checklists(
        self,
        operation_type: str,
        top_k: int = 2
    ) -> List[Dict]:
        """
        Search for compliance checklists for specific operation types.

        Args:
            operation_type: Type of operation (drilling, production, plugging, etc.)
            top_k: Number of checklists to return

        Returns:
            List of compliance checklists
        """
        if not self.cloud_retriever:
            return []

        checklist_query = f"compliance checklist requirements for {operation_type}"

        try:
            results = self.cloud_retriever.search(
                query_text=checklist_query,
                top_k=top_k,
                filter_dict={"document_type": "checklist"}
            )

            return [
                {
                    "checklist_name": r.get("metadata", {}).get("title", ""),
                    "items": r.get("text", "").split("\n"),
                    "operation_type": r.get("metadata", {}).get("operation_type", ""),
                    "last_updated": r.get("metadata", {}).get("last_updated", ""),
                    "score": r.get("score", 0.0),
                }
                for r in results
            ]
        except Exception:
            return []

    def is_available(self) -> bool:
        """Check if cloud search is available."""
        return self.cloud_retriever is not None


def get_search_engine(config: Dict) -> ComplianceSearchEngine:
    """Factory function to create search engine instance."""
    return ComplianceSearchEngine(config)
