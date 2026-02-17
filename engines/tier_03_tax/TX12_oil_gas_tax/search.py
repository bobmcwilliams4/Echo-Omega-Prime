"""
TX12 Oil & Gas Tax Engine — Vector Search Module
Semantic retrieval fallback for when doctrine cache misses.

This module provides keyword-weighted scoring as the primary search
mechanism, with vector similarity as a secondary fallback. The search
operates over the doctrine cache and supplementary knowledge fragments.

Author: ECHO OMEGA PRIME
Engine: TX12 Oil & Gas Tax
Version: 1.0.0
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple
import hashlib
import re
import time

from loguru import logger


# ==============================================================================
# SEARCH RESULT TYPES
# ==============================================================================

@dataclass
class SearchResult:
    """A single search result with scoring metadata."""
    topic_key: str
    topic_name: str
    score: float
    match_type: str  # "keyword", "semantic", "hybrid"
    matched_terms: List[str]
    snippet: str
    authority_weight: int = 0
    confidence_tier: str = "moderate"

    def to_dict(self) -> Dict[str, Any]:
        """Serialize for API response."""
        return {
            "topic_key": self.topic_key,
            "topic_name": self.topic_name,
            "score": round(self.score, 4),
            "match_type": self.match_type,
            "matched_terms": self.matched_terms,
            "snippet": self.snippet[:300],
            "authority_weight": self.authority_weight,
            "confidence_tier": self.confidence_tier
        }


@dataclass
class SearchResponse:
    """Complete search response with metadata."""
    query: str
    results: List[SearchResult]
    total_candidates: int
    search_time_ms: float
    search_type: str  # "keyword", "semantic", "hybrid"
    determinism_hash: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Serialize for API response."""
        return {
            "query": self.query[:200],
            "results": [r.to_dict() for r in self.results],
            "total_candidates": self.total_candidates,
            "search_time_ms": round(self.search_time_ms, 2),
            "search_type": self.search_type,
            "determinism_hash": self.determinism_hash
        }


# ==============================================================================
# KNOWLEDGE FRAGMENTS — Supplementary Search Corpus
# ==============================================================================

@dataclass
class KnowledgeFragment:
    """A searchable knowledge fragment outside the doctrine cache."""
    fragment_id: str
    topic: str
    content: str
    keywords: List[str]
    authority_source: str
    relevance_weight: float = 1.0

    def keyword_set(self) -> Set[str]:
        """Return keywords as lowercase set for matching."""
        return {k.lower() for k in self.keywords}


# Oil & Gas tax knowledge fragments for search fallback
OIL_GAS_FRAGMENTS: List[KnowledgeFragment] = [
    KnowledgeFragment(
        fragment_id="frag_idc_election",
        topic="IDC Election Mechanics",
        content="Under IRC 263(c) and Treas. Reg. 1.612-4, operators may elect to currently "
                "expense intangible drilling and development costs or capitalize and amortize "
                "them over 60 months. The election is made on the first return on which IDC "
                "is claimed and is binding for all subsequent wells. The election applies to "
                "all IDC incurred during the tax year, not on a well-by-well basis. For "
                "integrated oil companies, 30% of IDC must be capitalized and amortized "
                "over 60 months under IRC 291(b).",
        keywords=["idc", "election", "263c", "capitalize", "expense", "intangible",
                  "drilling", "integrated", "291b", "amortize"],
        authority_source="IRC 263(c), Treas. Reg. 1.612-4"
    ),
    KnowledgeFragment(
        fragment_id="frag_depletion_limits",
        topic="Depletion Limitation Rules",
        content="Percentage depletion is limited to the greater of (a) 65% of taxpayer's "
                "taxable income computed without regard to depletion, or (b) the taxpayer's "
                "adjusted basis in the property. Cost depletion cannot exceed the adjusted "
                "basis of the property. The 1,000 barrel per day equivalent limit for small "
                "producers under IRC 613A applies to average daily production, allocated "
                "proportionally across all properties. Transferred properties carry the "
                "transferor's depletion history for purposes of the limit.",
        keywords=["depletion", "limitation", "65%", "basis", "1000 barrel", "small producer",
                  "613a", "taxable income", "adjusted basis"],
        authority_source="IRC 613A(c), (d)"
    ),
    KnowledgeFragment(
        fragment_id="frag_economic_interest",
        topic="Economic Interest Doctrine",
        content="The economic interest doctrine, established in Palmer v. Bender (287 U.S. 551, "
                "1933), requires that to claim depletion a taxpayer must have (1) acquired by "
                "investment any interest in mineral in place, (2) secured by legal relationship "
                "income derived from extraction of the mineral, to which the taxpayer must look "
                "for a return of capital. This is the foundational test for all depletion claims "
                "and determines who is entitled to depletion — working interest owners, royalty "
                "owners, and ORRI holders all satisfy this test if they have a right to share in "
                "production or proceeds from production.",
        keywords=["economic interest", "palmer", "bender", "depletion", "mineral in place",
                  "return of capital", "extraction", "investment"],
        authority_source="Palmer v. Bender, 287 U.S. 551 (1933)"
    ),
    KnowledgeFragment(
        fragment_id="frag_pool_of_capital",
        topic="Pool of Capital Doctrine for Farmouts",
        content="Under the pool of capital doctrine, a farmout transaction is treated as a "
                "sharing arrangement in the exploration of mineral property, not as a sale or "
                "exchange. The farmor contributes the lease; the farmee contributes drilling "
                "services. Neither recognizes gain or loss. The farmee takes a zero basis in "
                "the earned interest and deducts drilling costs as IDC. The farmor retains "
                "a royalty or ORRI, which has a carved-out basis from the original lease cost. "
                "Rev. Rul. 77-176 confirms this treatment. The doctrine was established in "
                "United States v. Frazell, 335 F.2d 487 (5th Cir. 1964).",
        keywords=["pool of capital", "farmout", "frazell", "sharing arrangement",
                  "farmee", "farmor", "no gain", "no loss", "rev rul 77-176"],
        authority_source="Rev. Rul. 77-176; United States v. Frazell, 335 F.2d 487 (5th Cir. 1964)"
    ),
    KnowledgeFragment(
        fragment_id="frag_carved_out_payment",
        topic="Carved-Out vs Retained Production Payments",
        content="IRC 636(a) treats a carved-out production payment as a mortgage loan on the "
                "mineral property. The recipient treats the payment as loan proceeds, not as "
                "income from the sale of an economic interest. IRC 636(b) treats a retained "
                "production payment in a sale as a purchase money mortgage — the seller recognizes "
                "gain at closing, not as production occurs. A retained production payment in a "
                "lease is treated as a bonus. The classification as carved-out vs retained depends "
                "on whether the grantor retains an interest in the property after the grant.",
        keywords=["636", "carved out", "retained", "production payment", "mortgage loan",
                  "purchase money", "bonus", "economic interest"],
        authority_source="IRC 636(a), (b)"
    ),
    KnowledgeFragment(
        fragment_id="frag_working_interest_se_tax",
        topic="Working Interest Self-Employment Tax Exception",
        content="Under IRC 1402(a)(1), a working interest in an oil or gas well is excluded "
                "from the definition of rental income from real estate that would otherwise be "
                "excluded from self-employment income — meaning working interest income IS "
                "subject to self-employment tax UNLESS the taxpayer's liability is limited. "
                "Limited partners holding working interests are NOT subject to SE tax because "
                "they hold through a limited partnership. However, LLC members who hold working "
                "interests may or may not be subject depending on their level of participation "
                "and whether the LLC provides liability limitation.",
        keywords=["working interest", "self-employment", "se tax", "1402", "limited partner",
                  "llc", "liability", "net earnings", "rental exclusion"],
        authority_source="IRC 1402(a)(1); Treas. Reg. 1.1402(a)-1"
    ),
    KnowledgeFragment(
        fragment_id="frag_texas_franchise_tax",
        topic="Texas Franchise Tax for Oil & Gas Producers",
        content="Texas franchise (margin) tax applies to oil and gas companies at a rate of "
                "0.375% for entities primarily engaged in retail or wholesale trade, 0.75% for "
                "all others. O&G producers may calculate the tax base using the cost of goods "
                "sold (COGS) method, which allows deduction of direct costs of production "
                "including lease operating expenses, depletion, IDC, and depreciation of "
                "tangible equipment. The COGS deduction makes the franchise tax significantly "
                "lower for capital-intensive E&P companies. The no-tax-due threshold is "
                "$2.47 million in total revenue (2024). The EZ computation rate is 0.331%.",
        keywords=["texas franchise tax", "margin tax", "cogs", "cost of goods sold",
                  "0.375%", "0.75%", "production", "operating expense", "threshold"],
        authority_source="Texas Tax Code Chapter 171"
    ),
    KnowledgeFragment(
        fragment_id="frag_passive_activity_og",
        topic="Passive Activity Rules for Oil & Gas Working Interests",
        content="IRC 469(c)(3) provides a critical exception for working interests in oil and "
                "gas properties. A working interest in an oil or gas property is NOT treated as "
                "a passive activity if the taxpayer holds it directly or through an entity that "
                "does not limit the taxpayer's liability. This means net losses from working "
                "interests held by general partners or sole proprietors can offset active income "
                "without regard to material participation. However, if the working interest is "
                "held through an LLC, S-Corp, or limited partnership that limits liability, the "
                "passive activity rules DO apply, and the taxpayer must materially participate "
                "to deduct losses against active income.",
        keywords=["passive activity", "469", "working interest exception", "material participation",
                  "limited liability", "general partner", "active income", "net losses"],
        authority_source="IRC 469(c)(3); Treas. Reg. 1.469-1T(e)(4)"
    ),
    KnowledgeFragment(
        fragment_id="frag_amt_oil_gas",
        topic="Alternative Minimum Tax — Oil & Gas Preferences",
        content="For AMT purposes, excess IDC is a tax preference item under IRC 57(a)(2). "
                "Excess IDC is the amount by which IDC deducted under IRC 263(c) exceeds the "
                "amount that would have been deductible had IDC been capitalized and amortized "
                "over 10 years. Percentage depletion in excess of the adjusted basis of the "
                "property is also a preference item under IRC 57(a)(1). However, independent "
                "producers and royalty owners who compute percentage depletion under IRC 613A "
                "may claim depletion as a preference only to the extent it exceeds the adjusted "
                "basis. The IRC 59(e) election allows taxpayers to capitalize IDC and amortize "
                "over 60 months to avoid the AMT preference.",
        keywords=["amt", "alternative minimum tax", "preference", "57", "excess idc",
                  "percentage depletion", "59e", "capitalize", "amortize", "10 year"],
        authority_source="IRC 57(a)(1), (2); IRC 59(e)"
    ),
    KnowledgeFragment(
        fragment_id="frag_section_1254",
        topic="IRC 1254 IDC Recapture",
        content="When a taxpayer disposes of oil, gas, or geothermal property, IRC 1254 "
                "requires recapture of previously deducted IDC and depletion as ordinary income. "
                "The recapture amount is the lesser of (1) the amount realized over the adjusted "
                "basis, or (2) the total IDC deducted plus depletion claimed that reduced basis "
                "below what it would have been under cost depletion. This recapture applies to "
                "sales, exchanges, and certain involuntary conversions. It does not apply to "
                "transfers at death (stepped-up basis eliminates the recapture), gifts (donee "
                "inherits the recapture potential), or tax-free reorganizations.",
        keywords=["1254", "recapture", "idc", "depletion", "ordinary income", "disposition",
                  "sale", "adjusted basis", "death", "gift", "reorganization"],
        authority_source="IRC 1254"
    ),
    KnowledgeFragment(
        fragment_id="frag_199a_oil_gas",
        topic="Section 199A QBI Deduction for Oil & Gas",
        content="Oil and gas operating companies generally qualify for the IRC 199A 20% QBI "
                "deduction when conducted through pass-through entities. The key question is "
                "whether an O&G activity constitutes a specified service trade or business (SSTB). "
                "E&P operations (exploration, drilling, production) are generally NOT SSTBs. "
                "However, O&G consulting, engineering services, geological advisory services, "
                "and brokerage may constitute SSTBs depending on facts. Royalty income from "
                "mineral interests generally qualifies for QBI if the underlying activity is a "
                "trade or business (not merely investment). The W-2/UBIA limitation applies "
                "above the income threshold ($191,950 single / $383,900 MFJ for 2024).",
        keywords=["199a", "qbi", "qualified business income", "sstb", "oil gas",
                  "pass-through", "20%", "deduction", "w-2", "ubia", "trade or business"],
        authority_source="IRC 199A; Treas. Reg. 1.199A-5"
    ),
]


# ==============================================================================
# SEARCH ENGINE
# ==============================================================================

class OilGasTaxSearch:
    """Keyword and semantic search engine for oil & gas tax doctrine.

    Operates in three modes:
        1. keyword — exact and partial keyword matching with TF-IDF-like scoring
        2. semantic — conceptual similarity (simplified without vector DB)
        3. hybrid — combined keyword + semantic scoring

    The search engine operates over both the doctrine cache (passed in at
    query time) and the supplementary knowledge fragments defined above.
    """

    def __init__(self) -> None:
        """Initialize search engine with knowledge fragments."""
        self._fragments: List[KnowledgeFragment] = list(OIL_GAS_FRAGMENTS)
        self._query_count: int = 0
        self._total_search_ms: float = 0.0
        logger.info(f"OilGasTaxSearch initialized with {len(self._fragments)} knowledge fragments")

    def search(self, query: str, doctrine_cache: Dict[str, Any],
               max_results: int = 10, search_type: str = "hybrid") -> SearchResponse:
        """Execute a search across doctrine cache and knowledge fragments.

        Args:
            query: The search query text.
            doctrine_cache: Dict of topic_key -> DoctrineBlock from the engine.
            max_results: Maximum number of results to return.
            search_type: One of "keyword", "semantic", "hybrid".

        Returns:
            SearchResponse with ranked results.
        """
        start_time = time.time()
        query_lower = query.lower()
        query_terms = self._tokenize(query_lower)
        results: List[SearchResult] = []

        # Search doctrine cache
        for topic_key, doctrine in doctrine_cache.items():
            score = self._score_doctrine(query_terms, query_lower, doctrine, search_type)
            if score > 0.1:
                matched_terms = self._find_matched_terms(query_terms, doctrine)
                results.append(SearchResult(
                    topic_key=topic_key,
                    topic_name=getattr(doctrine, "topic", topic_key),
                    score=score,
                    match_type=search_type,
                    matched_terms=matched_terms,
                    snippet=getattr(doctrine, "conclusion_template", "")[:300],
                    authority_weight=doctrine.get_authority_weight() if hasattr(doctrine, "get_authority_weight") else 0,
                    confidence_tier=getattr(doctrine, "confidence", "moderate")
                ))

        # Search knowledge fragments
        for fragment in self._fragments:
            score = self._score_fragment(query_terms, query_lower, fragment, search_type)
            if score > 0.1:
                matched_terms = [t for t in query_terms if t in fragment.keyword_set()]
                results.append(SearchResult(
                    topic_key=fragment.fragment_id,
                    topic_name=fragment.topic,
                    score=score * fragment.relevance_weight,
                    match_type=search_type,
                    matched_terms=matched_terms,
                    snippet=fragment.content[:300],
                    authority_weight=0,
                    confidence_tier="moderate"
                ))

        # Sort by score descending
        results.sort(key=lambda r: r.score, reverse=True)
        total_candidates = len(results)
        results = results[:max_results]

        search_time_ms = (time.time() - start_time) * 1000

        # Determinism hash
        hash_input = query + "|" + "|".join(r.topic_key for r in results)
        det_hash = hashlib.sha256(hash_input.encode()).hexdigest()[:16]

        self._query_count += 1
        self._total_search_ms += search_time_ms

        return SearchResponse(
            query=query,
            results=results,
            total_candidates=total_candidates,
            search_time_ms=search_time_ms,
            search_type=search_type,
            determinism_hash=det_hash
        )

    def _tokenize(self, text: str) -> Set[str]:
        """Tokenize text into lowercase terms, removing stopwords."""
        stopwords = {"the", "a", "an", "is", "are", "was", "were", "be", "been",
                     "being", "have", "has", "had", "do", "does", "did", "will",
                     "would", "could", "should", "may", "might", "can", "shall",
                     "to", "of", "in", "for", "on", "with", "at", "by", "from",
                     "as", "into", "through", "during", "before", "after", "above",
                     "below", "between", "and", "or", "not", "no", "but", "if",
                     "then", "than", "that", "this", "these", "those", "it", "its",
                     "how", "what", "when", "where", "which", "who", "whom", "why"}
        tokens = set(re.findall(r'\b[a-z0-9]+\b', text))
        return tokens - stopwords

    def _score_doctrine(self, query_terms: Set[str], query_lower: str,
                        doctrine: Any, search_type: str) -> float:
        """Score a doctrine block against query terms."""
        score = 0.0
        keywords = [k.lower() for k in getattr(doctrine, "keywords", [])]
        keyword_set = set(keywords)
        topic_lower = getattr(doctrine, "topic", "").lower()
        conclusion = getattr(doctrine, "conclusion_template", "").lower()
        reasoning = getattr(doctrine, "reasoning_framework", "").lower()

        # Keyword matching (weighted)
        if search_type in ("keyword", "hybrid"):
            # Direct keyword match — highest signal
            keyword_matches = query_terms & keyword_set
            score += len(keyword_matches) * 3.0

            # Phrase matching in keywords
            for kw in keywords:
                if kw in query_lower:
                    score += 4.0

            # Topic name matching
            topic_terms = self._tokenize(topic_lower)
            topic_matches = query_terms & topic_terms
            score += len(topic_matches) * 2.0

            # Partial content matching
            conclusion_terms = self._tokenize(conclusion)
            content_matches = query_terms & conclusion_terms
            score += len(content_matches) * 0.5

        # Semantic matching (simplified)
        if search_type in ("semantic", "hybrid"):
            # Check for conceptual overlap via reasoning framework
            reasoning_terms = self._tokenize(reasoning)
            semantic_matches = query_terms & reasoning_terms
            score += len(semantic_matches) * 1.0

            # Check for IRC section references
            irc_refs = re.findall(r'\b(?:irc\s*)?(?:section\s*)?\d{2,4}[a-z]?\b', query_lower)
            for ref in irc_refs:
                ref_num = re.findall(r'\d+', ref)
                if ref_num:
                    for kw in keywords:
                        if ref_num[0] in kw:
                            score += 5.0
                            break

        # Normalize score to 0-1 range approximately
        return min(score / 20.0, 1.0)

    def _score_fragment(self, query_terms: Set[str], query_lower: str,
                        fragment: KnowledgeFragment, search_type: str) -> float:
        """Score a knowledge fragment against query terms."""
        score = 0.0
        kw_set = fragment.keyword_set()

        # Keyword matching
        keyword_matches = query_terms & kw_set
        score += len(keyword_matches) * 3.0

        # Phrase matching
        for kw in fragment.keywords:
            if kw.lower() in query_lower:
                score += 4.0

        # Content matching
        content_terms = self._tokenize(fragment.content.lower())
        content_matches = query_terms & content_terms
        score += len(content_matches) * 0.3

        return min(score / 20.0, 1.0)

    def _find_matched_terms(self, query_terms: Set[str], doctrine: Any) -> List[str]:
        """Find which query terms matched a doctrine."""
        keywords = {k.lower() for k in getattr(doctrine, "keywords", [])}
        return list(query_terms & keywords)

    def get_stats(self) -> Dict[str, Any]:
        """Return search engine statistics."""
        return {
            "total_queries": self._query_count,
            "total_search_ms": round(self._total_search_ms, 2),
            "avg_search_ms": round(self._total_search_ms / max(self._query_count, 1), 2),
            "fragment_count": len(self._fragments)
        }
