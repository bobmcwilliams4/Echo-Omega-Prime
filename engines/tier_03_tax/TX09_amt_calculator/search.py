"""
TX09 AMT CALCULATOR — VECTOR SEARCH
Semantic retrieval fallback for AMT knowledge.

Author: ECHO OMEGA PRIME
Version: 1.0.0
"""

from typing import List, Dict, Any, Optional
from pathlib import Path
import json
import hashlib


class AMTVectorSearch:
    """
    Lightweight vector search for AMT documentation.

    In production, this would integrate with:
    - Cloudflare Vectorize
    - Pinecone
    - ChromaDB
    - FAISS

    For now, implements simple keyword matching fallback.
    """

    def __init__(self):
        self.knowledge_base: List[Dict[str, Any]] = []
        self._load_knowledge_base()

    def _load_knowledge_base(self):
        """Load AMT knowledge base from local storage."""
        # In production, load from R2 or vectorize
        # For now, create in-memory knowledge base

        self.knowledge_base = [
            {
                "id": "amt_001",
                "text": "IRC Section 55 imposes alternative minimum tax equal to excess of tentative minimum tax over regular tax. "
                       "Tentative minimum tax calculated by applying AMT rates to AMTI less exemption amount. "
                       "2024 exemption amounts: $85,700 single, $133,300 married filing jointly.",
                "keywords": ["section 55", "amt calculation", "exemption", "tentative minimum tax"],
                "section": "55",
                "category": "calculation"
            },
            {
                "id": "amt_002",
                "text": "IRC Section 56 AMT adjustments include depreciation recalculation using ADS, mining exploration costs "
                       "capitalized over 10 years, long-term contracts using percentage-of-completion method, "
                       "and installment sales of dealer property. TCJA eliminated depreciation adjustment for post-2017 property.",
                "keywords": ["section 56", "adjustments", "depreciation", "mining", "long-term contracts"],
                "section": "56",
                "category": "adjustments"
            },
            {
                "id": "amt_003",
                "text": "IRC Section 57 tax preference items include private activity bond interest, excess percentage depletion, "
                       "and excess intangible drilling costs. Private activity bond interest exempt for regular tax but "
                       "included in AMTI, creating major AMT exposure for high-income taxpayers.",
                "keywords": ["section 57", "preferences", "private activity bonds", "depletion", "idc"],
                "section": "57",
                "category": "preferences"
            },
            {
                "id": "amt_004",
                "text": "IRC Section 55(d) AMT exemption phases out at 25% rate starting at $609,350 single, $1,218,700 married "
                       "filing jointly for 2024. Phase-out creates effective marginal rate increase of 6.5% or 7% in the "
                       "phase-out range. Exemption fully phases out at threshold plus 4x exemption amount.",
                "keywords": ["exemption", "phase-out", "phaseout", "section 55"],
                "section": "55",
                "category": "exemption"
            },
            {
                "id": "amt_005",
                "text": "IRC Section 53 minimum tax credit allows credit for prior-year AMT attributable to deferral preferences. "
                       "Credit limited to excess of regular tax over tentative minimum tax. Exclusion preferences like "
                       "private activity bond interest do not generate creditable AMT. Unlimited carryforward period.",
                "keywords": ["section 53", "minimum tax credit", "mtc", "amt credit"],
                "section": "53",
                "category": "credits"
            },
            {
                "id": "amt_006",
                "text": "IRC Section 56(b)(3) requires AMT adjustment for incentive stock option exercise spread equal to "
                       "FMV minus exercise price. No regular tax income at exercise but full spread included in AMTI. "
                       "Same-year disposition eliminates AMT adjustment. Creates major AMT trap if stock price declines post-exercise.",
                "keywords": ["iso", "incentive stock options", "section 56", "stock options"],
                "section": "56",
                "category": "adjustments"
            },
            {
                "id": "amt_007",
                "text": "TCJA Section 164(b)(6) imposed $10,000 SALT cap for regular tax. AMT continues to disallow SALT entirely, "
                       "but AMT adjustment now limited to $10K for taxpayers with SALT exceeding cap. Paradoxically reduced "
                       "AMT incidence by narrowing regular/AMT differential. PTET workarounds may avoid SALT cap and AMT adjustment.",
                "keywords": ["salt", "state and local tax", "tcja", "salt cap"],
                "section": "164",
                "category": "adjustments"
            },
            {
                "id": "amt_008",
                "text": "IRC Section 56(d) limits AMT NOL deduction to 90% of AMTI before NOL deduction, ensuring minimum 10% tax base. "
                       "ATNOL calculated separately from regular tax NOL with AMT adjustments. Indefinite carryforward period post-TCJA.",
                "keywords": ["nol", "net operating loss", "atnol", "section 56"],
                "section": "56",
                "category": "adjustments"
            },
            {
                "id": "amt_009",
                "text": "Inflation Reduction Act 2022 enacted 15% corporate alternative minimum tax on adjusted financial statement income "
                       "for corporations with average annual AFSI exceeding $1 billion. CAMT based on book income, not taxable income, "
                       "creating new book-tax conformity pressure. Effective for tax years beginning after December 31, 2022.",
                "keywords": ["corporate amt", "camt", "afsi", "inflation reduction act"],
                "section": "55",
                "category": "corporate"
            },
            {
                "id": "amt_010",
                "text": "AMT rates under IRC Section 55(b): 26% on first $220,700 of AMT base, 28% on excess. Thresholds apply to "
                       "singles and married filing jointly ($110,350 for married filing separately). Capital gains taxed at "
                       "preferential rates for both regular tax and AMT.",
                "keywords": ["amt rates", "26 percent", "28 percent", "section 55"],
                "section": "55",
                "category": "calculation"
            },
            {
                "id": "amt_011",
                "text": "AMT planning strategies: defer income into AMT years, accelerate deductions into non-AMT years, manage ISO "
                       "exercise timing, consider PTET elections, evaluate private activity bond holdings, coordinate Roth conversions "
                       "with AMT years, and model multi-year tax scenarios.",
                "keywords": ["amt planning", "strategies", "minimize amt", "avoid amt"],
                "section": "planning",
                "category": "planning"
            },
            {
                "id": "amt_012",
                "text": "Form 6251 required to calculate and report AMT liability. Part I calculates AMTI, Part II applies exemption "
                       "and rates to determine tentative minimum tax, Part III calculates tax. Form 8801 tracks AMT credit generation "
                       "and utilization across years.",
                "keywords": ["form 6251", "form 8801", "amt forms"],
                "section": "compliance",
                "category": "compliance"
            },
        ]

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search AMT knowledge base.

        Args:
            query: Search query
            top_k: Number of results to return

        Returns:
            List of search results with scores
        """
        query_lower = query.lower()
        results = []

        for doc in self.knowledge_base:
            # Simple keyword matching score
            score = 0.0

            # Check if query keywords match document keywords
            for keyword in doc["keywords"]:
                if keyword.lower() in query_lower:
                    score += 0.2

            # Check if query words appear in document text
            query_words = set(query_lower.split())
            doc_words = set(doc["text"].lower().split())
            overlap = len(query_words & doc_words)
            score += overlap * 0.01

            # Section number matching
            if doc.get("section") and doc["section"] in query:
                score += 0.3

            if score > 0:
                results.append({
                    "id": doc["id"],
                    "text": doc["text"],
                    "score": score,
                    "category": doc.get("category", "general"),
                    "section": doc.get("section", "")
                })

        # Sort by score descending
        results.sort(key=lambda x: x["score"], reverse=True)

        return results[:top_k]

    def document_count(self) -> int:
        """Return number of documents in knowledge base."""
        return len(self.knowledge_base)

    def add_document(self, text: str, keywords: List[str], section: str = "",
                    category: str = "general") -> str:
        """
        Add document to knowledge base.

        Args:
            text: Document text
            keywords: Associated keywords
            section: IRC section number
            category: Document category

        Returns:
            Document ID
        """
        doc_id = f"amt_{hashlib.md5(text.encode()).hexdigest()[:8]}"

        doc = {
            "id": doc_id,
            "text": text,
            "keywords": keywords,
            "section": section,
            "category": category
        }

        self.knowledge_base.append(doc)
        return doc_id

    def get_by_section(self, section: str) -> List[Dict[str, Any]]:
        """Get all documents for a specific IRC section."""
        return [
            doc for doc in self.knowledge_base
            if doc.get("section") == section
        ]

    def get_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get all documents for a specific category."""
        return [
            doc for doc in self.knowledge_base
            if doc.get("category") == category
        ]

    def semantic_search_enhanced(self, query: str, filters: Optional[Dict[str, Any]] = None,
                                 top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Enhanced semantic search with filtering.

        Args:
            query: Search query
            filters: Optional filters (section, category, etc.)
            top_k: Number of results

        Returns:
            Filtered and ranked results
        """
        # Start with basic search
        results = self.search(query, top_k=top_k * 2)

        # Apply filters if provided
        if filters:
            if "section" in filters:
                results = [r for r in results if r.get("section") == filters["section"]]

            if "category" in filters:
                results = [r for r in results if r.get("category") == filters["category"]]

            if "min_score" in filters:
                results = [r for r in results if r["score"] >= filters["min_score"]]

        return results[:top_k]


# ============================================================================
# KNOWLEDGE BASE UTILITIES
# ============================================================================

def initialize_amt_knowledge_base() -> AMTVectorSearch:
    """Initialize AMT knowledge base with core documentation."""
    search = AMTVectorSearch()

    # Knowledge base already initialized in __init__
    # This function can be extended to load from external sources

    return search


def sync_to_cloudflare_vectorize(search: AMTVectorSearch, account_id: str,
                                  database_id: str, api_token: str):
    """
    Sync local knowledge base to Cloudflare Vectorize.

    Args:
        search: AMTVectorSearch instance
        account_id: Cloudflare account ID
        database_id: Vectorize database ID
        api_token: Cloudflare API token
    """
    # Production implementation would use Cloudflare Vectorize API
    # https://developers.cloudflare.com/vectorize/

    # Placeholder for production sync logic
    pass


def load_from_r2(bucket_name: str, key: str) -> List[Dict[str, Any]]:
    """
    Load knowledge base from R2 storage.

    Args:
        bucket_name: R2 bucket name
        key: Object key

    Returns:
        List of documents
    """
    # Production implementation would use boto3 or Cloudflare R2 API
    # For now, return empty list
    return []
