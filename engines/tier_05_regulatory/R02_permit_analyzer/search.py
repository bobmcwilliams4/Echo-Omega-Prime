"""
R02 Permit Analyzer - Vector Search Module
Semantic retrieval fallback for doctrine cache misses.

Author: ECHO OMEGA PRIME
Authority: 11.0 SOVEREIGN
"""

from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from pathlib import Path
import sys

# Import cloud retriever from shared
SHARED_PATH = Path(__file__).parent.parent / "_shared"
if str(SHARED_PATH) not in sys.path:
    sys.path.insert(0, str(SHARED_PATH))

try:
    from cloud_retriever import CloudRetriever, RetrievalResult
    CLOUD_RETRIEVER_AVAILABLE = True
except ImportError:
    CLOUD_RETRIEVER_AVAILABLE = False

from loguru import logger


# ==============================================================================
# SEARCH RESULT STRUCTURES
# ==============================================================================

@dataclass
class PermitSearchResult:
    """Single search result from vector retrieval."""
    permit_type: str
    requirement_text: str
    authority_source: str
    confidence_score: float
    regulatory_body: str
    metadata: Dict[str, Any]


@dataclass
class SearchResults:
    """Collection of search results with metadata."""
    query: str
    results: List[PermitSearchResult]
    total_results: int
    search_latency_ms: float
    retrieval_method: str


# ==============================================================================
# VECTOR SEARCH ENGINE
# ==============================================================================

class PermitVectorSearch:
    """
    Semantic search over permit knowledge base.
    Fallback layer when doctrine cache misses.
    """

    def __init__(self, engine_id: str = "R02_permit_analyzer"):
        self.engine_id = engine_id
        self.cloud_retriever: Optional[CloudRetriever] = None

        if CLOUD_RETRIEVER_AVAILABLE:
            try:
                self.cloud_retriever = CloudRetriever(engine_id=engine_id)
                logger.info("Cloud retriever initialized for vector search")
            except Exception as e:
                logger.warning(f"Cloud retriever unavailable: {e}")
                self.cloud_retriever = None
        else:
            logger.warning("Cloud retriever module not found - search disabled")

    def search(
        self,
        query: str,
        permit_types: Optional[List[str]] = None,
        top_k: int = 5
    ) -> SearchResults:
        """
        Execute semantic search over permit knowledge.

        Args:
            query: Normalized query text
            permit_types: Filter by specific permit types
            top_k: Number of results to return

        Returns:
            SearchResults with ranked permit requirements
        """
        import time
        start_time = time.time()

        results = []

        if self.cloud_retriever:
            # Use cloud-based vector retrieval
            try:
                retrieval_results = self.cloud_retriever.search(
                    query=query,
                    namespace=f"permits_{self.engine_id}",
                    top_k=top_k,
                    filters={"permit_types": permit_types} if permit_types else None
                )

                for res in retrieval_results.results:
                    results.append(PermitSearchResult(
                        permit_type=res.metadata.get("permit_type", "unknown"),
                        requirement_text=res.text,
                        authority_source=res.metadata.get("authority_source", ""),
                        confidence_score=res.score,
                        regulatory_body=res.metadata.get("regulatory_body", "RRC"),
                        metadata=res.metadata
                    ))

                method = "cloud_vector_search"
            except Exception as e:
                logger.error(f"Cloud retrieval failed: {e}")
                method = "fallback_empty"
        else:
            # Fallback: return empty results
            logger.warning("No search backend available")
            method = "no_backend"

        latency_ms = (time.time() - start_time) * 1000

        return SearchResults(
            query=query,
            results=results,
            total_results=len(results),
            search_latency_ms=latency_ms,
            retrieval_method=method
        )

    def search_by_permit_type(
        self,
        permit_type: str,
        operation_context: Optional[str] = None,
        top_k: int = 10
    ) -> List[PermitSearchResult]:
        """
        Search for requirements specific to a permit type.

        Args:
            permit_type: Specific permit type to search
            operation_context: Additional context (e.g., "horizontal drilling")
            top_k: Max results

        Returns:
            List of relevant permit requirements
        """
        query = permit_type
        if operation_context:
            query = f"{permit_type} {operation_context}"

        search_results = self.search(
            query=query,
            permit_types=[permit_type],
            top_k=top_k
        )

        return search_results.results

    def multi_permit_search(
        self,
        permit_types: List[str],
        query: str,
        top_k_per_permit: int = 3
    ) -> Dict[str, List[PermitSearchResult]]:
        """
        Search across multiple permit types simultaneously.

        Args:
            permit_types: List of permit types to search
            query: Query text
            top_k_per_permit: Results per permit type

        Returns:
            Dict mapping permit_type -> results
        """
        results_by_type = {}

        for permit_type in permit_types:
            permit_results = self.search_by_permit_type(
                permit_type=permit_type,
                operation_context=query,
                top_k=top_k_per_permit
            )
            results_by_type[permit_type] = permit_results

        return results_by_type


# ==============================================================================
# PUBLIC API
# ==============================================================================

_search_instance: Optional[PermitVectorSearch] = None


def get_search_engine(engine_id: str = "R02_permit_analyzer") -> PermitVectorSearch:
    """Get global vector search instance."""
    global _search_instance
    if _search_instance is None:
        _search_instance = PermitVectorSearch(engine_id=engine_id)
    return _search_instance


def search_permits(
    query: str,
    permit_types: Optional[List[str]] = None,
    top_k: int = 5
) -> SearchResults:
    """Execute permit search (convenience function)."""
    return get_search_engine().search(query, permit_types, top_k)
