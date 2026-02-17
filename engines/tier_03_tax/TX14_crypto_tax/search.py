"""
TX14 Crypto Tax Engine — Vector Search Module
Semantic retrieval fallback for doctrine cache misses.

When the doctrine cache does not contain a pre-compiled block for a query,
this module performs vector similarity search against indexed crypto tax
knowledge to find relevant passages, authorities, and reasoning patterns.

Engine: TX14 Crypto Tax Intelligence Engine
Port: 8464
Author: ECHO OMEGA PRIME
"""

from __future__ import annotations

import hashlib
import json
import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from loguru import logger


# ==============================================================================
# CONSTANTS
# ==============================================================================

ENGINE_ID: str = "TX14"
SEARCH_INDEX_DIR: Path = Path("O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/TX14_crypto_tax/search_index")
SEARCH_INDEX_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_SIMILARITY_THRESHOLD: float = 0.72
DEFAULT_MAX_RESULTS: int = 10


# ==============================================================================
# SEARCH RESULT
# ==============================================================================

@dataclass
class SearchResult:
    """A single search result from the vector index."""
    document_id: str
    title: str
    content: str
    authority_type: str  # IRC, REG, CASE_LAW, NOTICE, REV_RUL, etc.
    authority_reference: str
    relevance_score: float
    snippet: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize for response inclusion."""
        return {
            "document_id": self.document_id,
            "title": self.title,
            "content": self.content[:500],
            "authority_type": self.authority_type,
            "authority_reference": self.authority_reference,
            "relevance_score": round(self.relevance_score, 4),
            "snippet": self.snippet,
            "metadata": self.metadata,
        }


@dataclass
class SearchResponse:
    """Aggregated search results."""
    query: str
    results: List[SearchResult]
    total_found: int
    search_latency_ms: float
    threshold_used: float
    index_size: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """Serialize for response."""
        return {
            "query": self.query,
            "results": [r.to_dict() for r in self.results],
            "total_found": self.total_found,
            "search_latency_ms": round(self.search_latency_ms, 3),
            "threshold_used": self.threshold_used,
            "index_size": self.index_size,
        }


# ==============================================================================
# KNOWLEDGE DOCUMENTS (Built-in crypto tax knowledge for search)
# ==============================================================================

CRYPTO_TAX_DOCUMENTS: List[Dict[str, Any]] = [
    {
        "id": "irs_notice_2014_21",
        "title": "IRS Notice 2014-21 — Virtual Currency Guidance",
        "authority_type": "NOTICE",
        "authority_reference": "IRS Notice 2014-21",
        "content": (
            "Virtual currency is treated as property for federal tax purposes. "
            "General tax principles applicable to property transactions apply to transactions using virtual currency. "
            "A taxpayer who receives virtual currency as payment for goods or services must include the fair market value "
            "of the virtual currency in computing gross income. For purposes of computing gain or loss, the basis of "
            "virtual currency received as payment is the FMV at time of receipt. Virtual currency is not treated as "
            "currency for purposes of IRC section 988 (foreign currency transactions). A payment made using virtual "
            "currency is subject to information reporting to the same extent as any other payment in property."
        ),
        "keywords": ["property", "virtual currency", "fmv", "basis", "gross income", "notice 2014-21"],
    },
    {
        "id": "rev_rul_2019_24",
        "title": "Rev. Rul. 2019-24 — Hard Forks and Airdrops",
        "authority_type": "REV_RUL",
        "authority_reference": "Rev. Rul. 2019-24",
        "content": (
            "If a taxpayer receives new cryptocurrency through an airdrop following a hard fork, the taxpayer has "
            "ordinary income equal to the fair market value of the new cryptocurrency at the time it is received, "
            "provided the taxpayer has dominion and control over the new cryptocurrency. If a hard fork occurs but "
            "does not result in an airdrop, the taxpayer has no income. The basis of the new cryptocurrency equals "
            "the amount included in income. The holding period begins the day after receipt."
        ),
        "keywords": ["hard fork", "airdrop", "ordinary income", "dominion", "control", "rev rul 2019-24"],
    },
    {
        "id": "irc_1001_recognition",
        "title": "IRC Section 1001 — Recognition of Gain or Loss",
        "authority_type": "IRC",
        "authority_reference": "IRC §1001",
        "content": (
            "Gain from the sale or other disposition of property is the excess of the amount realized over the "
            "adjusted basis. Loss is the excess of adjusted basis over the amount realized. Every exchange of crypto "
            "for another crypto, crypto for fiat, or crypto for goods/services is a taxable disposition under §1001. "
            "The amount realized includes money received plus the FMV of property received. Since crypto is property "
            "per Notice 2014-21, every swap, trade, or exchange triggers gain/loss recognition."
        ),
        "keywords": ["gain", "loss", "disposition", "amount realized", "adjusted basis", "1001"],
    },
    {
        "id": "irc_1012_basis",
        "title": "IRC Section 1012 — Cost Basis",
        "authority_type": "IRC",
        "authority_reference": "IRC §1012",
        "content": (
            "The basis of property is its cost. For cryptocurrency, cost basis includes the purchase price plus "
            "any transaction fees (gas fees, exchange fees) paid to acquire the asset. When crypto is received as "
            "income (mining, staking, airdrops), the basis is the FMV at time of receipt — the same amount included "
            "in gross income. Cost basis methods include FIFO (default if no specific identification), LIFO, specific "
            "identification (requires adequate records), and average cost (limited applicability). "
            "Rev. Proc. 2024-28 provides a safe harbor for certain basis determinations."
        ),
        "keywords": ["cost basis", "fifo", "lifo", "specific identification", "average cost", "1012"],
    },
    {
        "id": "irc_1222_holding_period",
        "title": "IRC Section 1222 — Holding Period and Capital Gains Rates",
        "authority_type": "IRC",
        "authority_reference": "IRC §1222",
        "content": (
            "Short-term capital gain/loss: asset held one year or less. Long-term: held more than one year. "
            "Short-term gains taxed at ordinary income rates (up to 37%). Long-term gains taxed at preferential "
            "rates (0%, 15%, or 20% depending on taxable income). Additional 3.8% NIIT may apply. For NFTs "
            "classified as collectibles, long-term rate is 28%. Holding period begins day after acquisition. "
            "For hard fork/airdrop assets, holding period begins day after receipt date."
        ),
        "keywords": ["holding period", "short-term", "long-term", "capital gains rate", "1222", "NIIT"],
    },
    {
        "id": "irc_1091_wash_sales",
        "title": "IRC Section 1091 — Wash Sale Rules",
        "authority_type": "IRC",
        "authority_reference": "IRC §1091",
        "content": (
            "Section 1091 disallows losses on sales of stock or securities if substantially identical stock or "
            "securities are acquired within 30 days before or after the sale. CRITICAL: As of 2026, cryptocurrency "
            "is NOT classified as stock or securities for purposes of §1091. Therefore, the wash sale rule does NOT "
            "currently apply to cryptocurrency. Taxpayers can sell crypto at a loss and immediately repurchase the same "
            "crypto without wash sale disallowance. CAUTION: Pending legislation may extend wash sale rules to digital "
            "assets. The Build Back Better Act (2021) and subsequent proposals included crypto wash sale provisions."
        ),
        "keywords": ["wash sale", "1091", "substantially identical", "30 days", "loss disallowance", "securities"],
    },
    {
        "id": "irc_170_charitable",
        "title": "IRC Section 170 — Charitable Contributions of Crypto",
        "authority_type": "IRC",
        "authority_reference": "IRC §170",
        "content": (
            "Cryptocurrency held more than one year qualifies as long-term capital gain property for charitable "
            "deduction purposes. Deduction equals FMV at time of donation — no gain recognition on the appreciation. "
            "If held one year or less, deduction limited to cost basis. Donations exceeding $5,000 require qualified "
            "appraisal (Form 8283 Section B). Donations of $250+ require written acknowledgment from charity. "
            "AGI limitation: 30% for appreciated capital gain property to public charities, 20% to private foundations."
        ),
        "keywords": ["charitable", "donation", "170", "fmv", "appraisal", "form 8283", "agi limitation"],
    },
    {
        "id": "irc_165_losses",
        "title": "IRC Section 165 — Casualty and Theft Losses for Crypto",
        "authority_type": "IRC",
        "authority_reference": "IRC §165",
        "content": (
            "Post-TCJA (2018-2025), personal casualty and theft losses are NOT deductible unless attributable to "
            "a federally declared disaster. Lost or stolen cryptocurrency (exchange hacks, wallet compromise, scams) "
            "does NOT qualify for personal casualty loss deduction. However, business theft losses under §165(c)(1) "
            "may still be deductible if the crypto was held in a trade or business. Abandoned/worthless crypto may "
            "qualify for worthlessness deduction under §165(a) if abandonment is evidenced by identifiable event."
        ),
        "keywords": ["casualty", "theft", "lost", "stolen", "worthless", "165", "TCJA", "hack"],
    },
    {
        "id": "jarrett_v_us",
        "title": "Jarrett v. United States — Staking Rewards",
        "authority_type": "CASE_LAW",
        "authority_reference": "Jarrett v. United States, No. 3:21-cv-00419 (M.D. Tenn. 2022)",
        "content": (
            "Joshua and Jessica Jarrett argued that Tezos staking rewards constituted 'new property' created by "
            "the taxpayer and should not be taxed until sold (like crops or manufactured goods). The IRS initially "
            "offered a refund, but the Jarretts sought a precedential ruling. The court dismissed for lack of "
            "standing after the refund. The 'creation theory' — that newly created tokens through staking are not "
            "taxable until disposition — has NOT been affirmed by any court. IRS position remains that staking "
            "rewards are ordinary income at FMV when received (dominion and control)."
        ),
        "keywords": ["jarrett", "staking", "creation theory", "new property", "tezos", "dominion"],
    },
    {
        "id": "defi_swap_disposition",
        "title": "DeFi Swap as Taxable Disposition",
        "authority_type": "ANALYSIS",
        "authority_reference": "IRS Notice 2014-21 applied to DeFi",
        "content": (
            "Each token-to-token swap on a decentralized exchange (DEX) constitutes a taxable disposition under "
            "IRC §1001. Even if no fiat currency is involved, exchanging one cryptocurrency for another is an "
            "exchange of property for property, triggering gain or loss recognition. Gas fees paid for the swap "
            "transaction should be added to the basis of the acquired asset (purchase side) or reduce the amount "
            "realized (sale side). Multi-hop swaps through routing protocols are treated as a single exchange for "
            "the endpoints. Liquidity pool interactions (adding/removing) may trigger separate taxable events "
            "depending on the protocol mechanics and whether LP tokens represent a new asset."
        ),
        "keywords": ["defi", "swap", "dex", "disposition", "gas fees", "token exchange", "lp token"],
    },
    {
        "id": "mining_self_employment",
        "title": "Mining as Self-Employment Income",
        "authority_type": "ANALYSIS",
        "authority_reference": "IRS Notice 2014-21, Q&A 8-9",
        "content": (
            "If mining is conducted as a trade or business (continuity, regularity, profit motive), mining rewards "
            "are self-employment income reported on Schedule C, subject to self-employment tax (15.3% on first "
            "$168,600 for 2024). Expenses deductible: electricity, hardware depreciation (§179 or MACRS), internet, "
            "pool fees, cooling costs, facility rent. If mining is a hobby (IRC §183), income still reported but "
            "expenses not deductible post-TCJA. Mining pool participants: income recognized when pool distributes "
            "reward, not when block is mined. Fair market value determined at time of receipt."
        ),
        "keywords": ["mining", "self-employment", "schedule c", "se tax", "trade or business", "hobby"],
    },
    {
        "id": "nft_collectible_treatment",
        "title": "NFT Collectible Tax Treatment",
        "authority_type": "NOTICE",
        "authority_reference": "IRS Notice 2023-27",
        "content": (
            "The IRS announced in Notice 2023-27 that it intends to issue guidance treating certain NFTs as "
            "collectibles under IRC §408(m). NFTs that represent underlying collectible items (art, antiques, gems, "
            "stamps, coins, certain metals) would be subject to the 28% maximum long-term capital gains rate for "
            "collectibles rather than the standard 20% maximum rate. The IRS uses a 'look-through' analysis: if the "
            "NFT certifies ownership of a physical collectible, or if the associated digital file would itself be a "
            "collectible if physical, the NFT is treated as a collectible. NFTs certifying rights to non-collectible "
            "assets (event tickets, domain names) would not be subject to the collectible rate."
        ),
        "keywords": ["nft", "collectible", "28%", "notice 2023-27", "look-through", "408(m)", "digital art"],
    },
    {
        "id": "broker_reporting_iija",
        "title": "Digital Asset Broker Reporting — IIJA 2021",
        "authority_type": "IRC",
        "authority_reference": "IRC §6045 as amended by IIJA §80603",
        "content": (
            "The Infrastructure Investment and Jobs Act (2021) expanded the definition of 'broker' under IRC §6045 "
            "to include persons who effectuate transfers of digital assets. Brokers must report gross proceeds and, "
            "beginning in later years, cost basis on Form 1099-DA. The definition potentially captures DEX operators, "
            "wallet providers, and DeFi protocol operators, though Treasury regulations may narrow the scope. "
            "Effective dates: gross proceeds reporting for 2025, basis reporting for 2026. Cash transaction reporting "
            "under §6050I ($10,000+) also applies to digital asset transactions."
        ),
        "keywords": ["broker", "1099-da", "6045", "iija", "infrastructure act", "reporting", "6050I"],
    },
    {
        "id": "fbar_foreign_exchange",
        "title": "FBAR Reporting for Foreign Crypto Exchanges",
        "authority_type": "IRC",
        "authority_reference": "31 USC §5314; FinCEN 114",
        "content": (
            "U.S. persons with financial interest in or signature authority over foreign financial accounts with "
            "aggregate value exceeding $10,000 at any time during the calendar year must file FinCEN Form 114 (FBAR). "
            "FinCEN has stated that virtual currency held in foreign exchanges is reportable on FBAR. The threshold "
            "is based on aggregate value across ALL foreign accounts. Willful failure to file: up to $100,000 or 50% "
            "of account balance per violation. Non-willful: up to $10,000 per violation. Reasonable cause defense "
            "available for non-willful. Filing deadline: April 15, automatic extension to October 15."
        ),
        "keywords": ["fbar", "foreign", "fincen", "114", "$10,000", "exchange", "willful", "penalty"],
    },
    {
        "id": "wrapped_tokens_analysis",
        "title": "Wrapped Token Tax Treatment Analysis",
        "authority_type": "ANALYSIS",
        "authority_reference": "No direct IRS guidance",
        "content": (
            "No direct IRS guidance exists on whether wrapping a token (e.g., ETH to WETH) is a taxable event. "
            "Conservative position: wrapping is a taxable exchange under §1001 because WETH is a different asset "
            "with different smart contract properties. WETH is an ERC-20 token while ETH is the native asset. "
            "Aggressive position: wrapping is merely a change in form, not substance — economically equivalent, "
            "1:1 redeemable, no change in economic exposure. Analogous to exchanging physical gold for a gold "
            "warehouse receipt. The IRS has not ruled on this issue. Given the ambiguity, practitioners should "
            "consider disclosure under §6662 if taking the non-taxable position."
        ),
        "keywords": ["wrapped", "weth", "wrapping", "eth to weth", "change in form", "taxable exchange"],
    },
    {
        "id": "cross_chain_bridge_analysis",
        "title": "Cross-Chain Bridge Tax Analysis",
        "authority_type": "ANALYSIS",
        "authority_reference": "No direct IRS guidance",
        "content": (
            "Cross-chain bridges transfer assets between different blockchains. Tax treatment depends on the bridge "
            "mechanism. Lock-and-mint bridges: original asset locked, synthetic version minted on destination chain. "
            "Possible treatment as taxable exchange (different asset received) or non-taxable (mere transfer of same "
            "economic interest). Burn-and-mint bridges: original destroyed, new version created — stronger argument "
            "for taxable exchange. Liquidity pool bridges: user swaps into pool on one chain, receives from pool on "
            "another — likely taxable exchange. No IRS guidance exists. Substance-over-form doctrine suggests that if "
            "economic exposure changes (different chain, different contract), a taxable event may occur."
        ),
        "keywords": ["bridge", "cross-chain", "lock", "mint", "burn", "layer 2", "transfer"],
    },
]


# ==============================================================================
# KEYWORD SEARCH ENGINE (TF-IDF-like without ML dependencies)
# ==============================================================================

class CryptoTaxSearchEngine:
    """Deterministic keyword-based search engine for crypto tax knowledge.

    Uses TF-IDF-inspired scoring without external ML dependencies.
    This provides the Layer 2 (Semantic Retrieval) capability when
    the doctrine cache (Layer 1) misses.
    """

    def __init__(self, documents: Optional[List[Dict[str, Any]]] = None) -> None:
        self._documents: List[Dict[str, Any]] = documents or CRYPTO_TAX_DOCUMENTS
        self._index: Dict[str, List[Tuple[int, float]]] = {}
        self._build_index()
        logger.info(f"CryptoTaxSearchEngine initialized with {len(self._documents)} documents")

    def _build_index(self) -> None:
        """Build inverted index from documents."""
        import math
        doc_count = len(self._documents)
        term_doc_freq: Dict[str, int] = {}

        # First pass: count document frequency for each term
        for doc in self._documents:
            terms = self._extract_terms(doc)
            unique_terms = set(terms)
            for term in unique_terms:
                term_doc_freq[term] = term_doc_freq.get(term, 0) + 1

        # Second pass: build TF-IDF index
        for doc_idx, doc in enumerate(self._documents):
            terms = self._extract_terms(doc)
            term_counts: Dict[str, int] = {}
            for term in terms:
                term_counts[term] = term_counts.get(term, 0) + 1
            total_terms = len(terms) or 1
            for term, count in term_counts.items():
                tf = count / total_terms
                idf = math.log(doc_count / (1 + term_doc_freq.get(term, 0)))
                tfidf = tf * idf
                if term not in self._index:
                    self._index[term] = []
                self._index[term].append((doc_idx, tfidf))

    def _extract_terms(self, doc: Dict[str, Any]) -> List[str]:
        """Extract searchable terms from a document."""
        text = f"{doc.get('title', '')} {doc.get('content', '')} {' '.join(doc.get('keywords', []))}"
        text = text.lower()
        text = re.sub(r'[^\w\s§$%]', ' ', text)
        tokens = text.split()
        # Remove very short tokens and common stop words
        stop_words = {"the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
                      "have", "has", "had", "do", "does", "did", "will", "would", "shall", "should",
                      "may", "might", "can", "could", "and", "or", "but", "if", "of", "at", "by",
                      "for", "with", "about", "to", "from", "in", "on", "up", "out", "as", "it",
                      "its", "that", "this", "not", "no", "so", "such", "than", "too", "very"}
        return [t for t in tokens if len(t) > 1 and t not in stop_words]

    def search(self, query: str, max_results: int = DEFAULT_MAX_RESULTS,
               threshold: float = DEFAULT_SIMILARITY_THRESHOLD) -> SearchResponse:
        """Search the knowledge base for relevant documents."""
        start_time = time.time()
        query_terms = self._extract_terms({"title": "", "content": query, "keywords": []})

        if not query_terms:
            return SearchResponse(
                query=query, results=[], total_found=0,
                search_latency_ms=0.0, threshold_used=threshold, index_size=len(self._documents),
            )

        # Score each document
        doc_scores: Dict[int, float] = {}
        for term in query_terms:
            if term in self._index:
                for doc_idx, tfidf in self._index[term]:
                    doc_scores[doc_idx] = doc_scores.get(doc_idx, 0.0) + tfidf

        # Also boost for keyword matches
        for doc_idx, doc in enumerate(self._documents):
            keywords = [k.lower() for k in doc.get("keywords", [])]
            for term in query_terms:
                if term in keywords:
                    doc_scores[doc_idx] = doc_scores.get(doc_idx, 0.0) + 0.5

        # Normalize scores to 0-1 range
        max_score = max(doc_scores.values()) if doc_scores else 1.0
        if max_score > 0:
            for doc_idx in doc_scores:
                doc_scores[doc_idx] /= max_score

        # Filter by threshold and sort
        scored = [(idx, score) for idx, score in doc_scores.items() if score >= threshold]
        scored.sort(key=lambda x: x[1], reverse=True)
        scored = scored[:max_results]

        results: List[SearchResult] = []
        for doc_idx, score in scored:
            doc = self._documents[doc_idx]
            content = doc.get("content", "")
            snippet = content[:200] + "..." if len(content) > 200 else content
            results.append(SearchResult(
                document_id=doc["id"],
                title=doc["title"],
                content=content,
                authority_type=doc.get("authority_type", "ANALYSIS"),
                authority_reference=doc.get("authority_reference", ""),
                relevance_score=score,
                snippet=snippet,
                metadata={"keywords": doc.get("keywords", [])},
            ))

        latency = (time.time() - start_time) * 1000
        logger.debug(f"Search completed: {len(results)} results in {latency:.1f}ms for query: {query[:50]}...")

        return SearchResponse(
            query=query,
            results=results,
            total_found=len(results),
            search_latency_ms=latency,
            threshold_used=threshold,
            index_size=len(self._documents),
        )

    def get_document_by_id(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a specific document by ID."""
        for doc in self._documents:
            if doc["id"] == doc_id:
                return doc
        return None

    def get_index_stats(self) -> Dict[str, Any]:
        """Get search index statistics."""
        return {
            "document_count": len(self._documents),
            "unique_terms": len(self._index),
            "avg_terms_per_doc": round(sum(len(self._extract_terms(d)) for d in self._documents) / max(len(self._documents), 1), 1),
        }


# ==============================================================================
# SINGLETON INSTANCE
# ==============================================================================

_search_engine: Optional[CryptoTaxSearchEngine] = None


def get_search_engine() -> CryptoTaxSearchEngine:
    """Get or create the singleton search engine."""
    global _search_engine
    if _search_engine is None:
        _search_engine = CryptoTaxSearchEngine()
    return _search_engine


def search_crypto_tax(query: str, max_results: int = DEFAULT_MAX_RESULTS,
                      threshold: float = DEFAULT_SIMILARITY_THRESHOLD) -> SearchResponse:
    """Convenience: search the crypto tax knowledge base."""
    return get_search_engine().search(query, max_results, threshold)
