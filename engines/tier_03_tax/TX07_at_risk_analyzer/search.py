"""
Vector search fallback for TX07 at-risk analyzer
Cloud retrieval integration for semantic search when doctrine cache misses
"""

from typing import List, Dict, Optional
import sys
from pathlib import Path

# Import cloud retriever from shared module
sys.path.insert(0, str(Path(__file__).parent.parent / "_shared"))

try:
    from cloud_retriever import retrieve_from_cloud
    CLOUD_AVAILABLE = True
except ImportError:
    CLOUD_AVAILABLE = False


class AtRiskVectorSearch:
    """Vector search for at-risk tax law when doctrine cache misses"""

    def __init__(self, config: Dict):
        self.config = config
        self.cloud_enabled = config.get("integration", {}).get("cloud_retrieval", True)

    async def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Search for at-risk guidance using vector similarity
        Falls back to cloud retrieval if available
        """
        if not self.cloud_enabled or not CLOUD_AVAILABLE:
            return []

        try:
            results = await retrieve_from_cloud(
                query=query,
                domain="tax_law",
                specialty="at_risk_limitations",
                top_k=top_k,
                filters={"irc_section": "465"}
            )
            return results
        except Exception as e:
            # Log error but don't fail query
            return []

    def format_search_results(self, results: List[Dict]) -> str:
        """Format vector search results for inclusion in response"""
        if not results:
            return ""

        formatted = "\n\nADDITIONAL GUIDANCE (from knowledge base):\n"
        for i, result in enumerate(results, 1):
            formatted += f"\n{i}. {result.get('title', 'Untitled')}\n"
            formatted += f"   {result.get('content', '')[:300]}...\n"
            if result.get('authority'):
                formatted += f"   Authority: {result['authority']}\n"

        return formatted


def extract_irc_sections(text: str) -> List[str]:
    """Extract IRC section references from text"""
    import re
    pattern = r'(?:IRC\s*)?§?\s*(\d{1,4}(?:\([a-z]\)(?:\(\d+\))?)*)'
    matches = re.findall(pattern, text, re.IGNORECASE)
    return [f"§{match}" for match in matches]
