"""
VECTOR SEARCH INTEGRATION — Cloud Retriever Fallback

When doctrine cache misses, fall back to cloud-based semantic retrieval.
Integrates with ECHO OMEGA PRIME shared cloud retriever module.
"""

from pathlib import Path
from typing import List, Dict, Any, Optional
import sys

# Add shared module path
SHARED_PATH = Path(__file__).parent.parent / "_shared"
if SHARED_PATH.exists():
    sys.path.insert(0, str(SHARED_PATH))

try:
    from cloud_retriever import CloudRetriever, RetrievalResult
    CLOUD_RETRIEVER_AVAILABLE = True
except ImportError:
    CLOUD_RETRIEVER_AVAILABLE = False
    RetrievalResult = None

from loguru import logger


class WillParserVectorSearch:
    """
    Vector search fallback for will construction queries.
    Integrates with Cognition Cloud vectorization infrastructure.
    """

    def __init__(self):
        self.retriever: Optional[Any] = None
        self.enabled = False
        self._initialize_retriever()

    def _initialize_retriever(self):
        """Initialize cloud retriever if available."""
        if not CLOUD_RETRIEVER_AVAILABLE:
            logger.warning("Cloud retriever module not available. Vector search disabled.")
            return

        try:
            self.retriever = CloudRetriever(
                engine_id="P02_will_parser",
                domain="will_construction",
                r2_bucket="echo-prime-knowledge",
                vector_index="will-construction-vectors"
            )
            self.enabled = True
            logger.info("Cloud retriever initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize cloud retriever: {e}")
            self.enabled = False

    def search(
        self,
        query: str,
        top_k: int = 5,
        min_score: float = 0.6
    ) -> List[Dict[str, Any]]:
        """
        Execute vector search against cloud knowledge base.

        Args:
            query: Normalized search query
            top_k: Number of results to return
            min_score: Minimum relevance score (0.0-1.0)

        Returns:
            List of retrieval results with content and metadata
        """
        if not self.enabled:
            logger.warning("Vector search not enabled. Returning empty results.")
            return []

        try:
            results = self.retriever.search(
                query=query,
                top_k=top_k,
                min_score=min_score,
                domain_filter="will_construction"
            )

            # Convert to dict format
            return [
                {
                    "content": r.content,
                    "score": r.score,
                    "source": r.metadata.get("source", "unknown"),
                    "authority": r.metadata.get("authority", "unknown"),
                    "section": r.metadata.get("section", ""),
                    "topic": r.metadata.get("topic", ""),
                }
                for r in results
            ]
        except Exception as e:
            logger.error(f"Vector search failed: {e}")
            return []

    def search_by_authority(
        self,
        authority: str,
        query: str,
        top_k: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Search within specific authority source.

        Args:
            authority: Authority filter (e.g., 'Texas Estates Code', 'Restatement Third')
            query: Search query
            top_k: Number of results

        Returns:
            Filtered search results
        """
        if not self.enabled:
            return []

        try:
            results = self.retriever.search(
                query=query,
                top_k=top_k * 2,  # Retrieve more to filter
                domain_filter="will_construction"
            )

            # Filter by authority
            filtered = [
                {
                    "content": r.content,
                    "score": r.score,
                    "source": r.metadata.get("source", ""),
                    "section": r.metadata.get("section", ""),
                }
                for r in results
                if authority.lower() in r.metadata.get("source", "").lower()
            ]

            return filtered[:top_k]
        except Exception as e:
            logger.error(f"Authority-filtered search failed: {e}")
            return []

    def get_related_provisions(
        self,
        statute_section: str,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Find related statute provisions based on section reference.

        Args:
            statute_section: Section reference (e.g., '§255.153')
            top_k: Number of related provisions

        Returns:
            Related provisions from same chapter or topic area
        """
        if not self.enabled:
            return []

        try:
            # Extract chapter number (e.g., '255' from '§255.153')
            import re
            match = re.search(r'§?(\d{3})', statute_section)
            if not match:
                return []

            chapter = match.group(1)
            query = f"Texas Estates Code Chapter {chapter}"

            results = self.retriever.search(
                query=query,
                top_k=top_k,
                domain_filter="will_construction"
            )

            return [
                {
                    "content": r.content,
                    "score": r.score,
                    "section": r.metadata.get("section", ""),
                    "topic": r.metadata.get("topic", ""),
                }
                for r in results
            ]
        except Exception as e:
            logger.error(f"Related provisions search failed: {e}")
            return []

    def health_check(self) -> Dict[str, Any]:
        """Check vector search system health."""
        return {
            "enabled": self.enabled,
            "cloud_retriever_available": CLOUD_RETRIEVER_AVAILABLE,
            "retriever_initialized": self.retriever is not None,
        }


# Singleton instance
_vector_search: Optional[WillParserVectorSearch] = None


def get_vector_search() -> WillParserVectorSearch:
    """Get or create vector search singleton."""
    global _vector_search
    if _vector_search is None:
        _vector_search = WillParserVectorSearch()
    return _vector_search
