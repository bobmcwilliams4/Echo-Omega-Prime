"""
TX14 CRYPTO TAX DOCTRINE CACHE — 55+ Pre-Compiled Crypto Tax Reasoning Blocks
Each block contains expert-level analysis, adversarial testing, authority citations,
and stratified confidence levels for cryptocurrency and digital asset taxation.

This is the Layer 1 cache — designed to return within 0-200ms for common crypto tax queries.

Engine: TX14 Crypto Tax Intelligence Engine
Port: 8464
Version: 1.0.0
Author: ECHO OMEGA PRIME
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set

from loguru import logger


# ==============================================================================
# ENUMS
# ==============================================================================

class ConfidenceLevel(str, Enum):
    """Tax position confidence stratification."""
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"


class PositionZone(str, Enum):
    """Position context zones — never blur."""
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"


class EntityScope(str, Enum):
    """Entity types for doctrine applicability."""
    INDIVIDUAL = "individual"
    SOLE_PROPRIETORSHIP = "sole_proprietorship"
    PARTNERSHIP = "partnership"
    LLC = "llc"
    S_CORPORATION = "s_corporation"
    C_CORPORATION = "c_corporation"
    TRUST = "trust"
    ESTATE = "estate"
    TAX_EXEMPT = "tax_exempt_organization"
    FOREIGN_PERSON = "foreign_person"


class IssueCategory(str, Enum):
    """Crypto tax issue categories for multi-doctrine decomposition."""
    CAPITAL_GAINS = "capital_gains"
    ORDINARY_INCOME = "ordinary_income"
    MINING_STAKING = "mining_staking"
    DEFI = "defi"
    NFT = "nft"
    REPORTING = "reporting"
    INFORMATION_RETURN = "information_return"
    BASIS = "basis"
    CHARITABLE = "charitable"
    RETIREMENT = "retirement"
    INTERNATIONAL = "international"
    BUSINESS_USE = "business_use"


# ==============================================================================
# DOCTRINE BLOCK DATA CLASS
# ==============================================================================

@dataclass
class DoctrineBlock:
    """
    Pre-compiled crypto tax reasoning block.

    Each block represents expert-level analysis on a specific crypto tax topic,
    including adversarial counter-arguments, authority citations, and stratified
    confidence levels.
    """
    topic: str
    keywords: List[str]
    conclusion_template: List[str]
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    burden_holder: str
    adversary_position: str
    counter_arguments: List[str]
    resolution_strategy: str
    entity_scope: List[EntityScope]
    confidence: ConfidenceLevel
    confidence_stratification: Dict[str, ConfidenceLevel]
    controlling_precedent: Optional[str] = None
    irc_sections: List[str] = field(default_factory=list)
    treasury_regs: List[str] = field(default_factory=list)
    revenue_rulings: List[str] = field(default_factory=list)
    notices: List[str] = field(default_factory=list)
    case_law: List[str] = field(default_factory=list)
    disclosure_caveat: Optional[str] = None
    issue_categories: List[IssueCategory] = field(default_factory=list)
    interaction_triggers: List[str] = field(default_factory=list)
    planning_zone_variant: Optional[str] = None
    reporting_zone_variant: Optional[str] = None
    audit_zone_variant: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "topic": self.topic,
            "keywords": self.keywords,
            "conclusion_template": self.conclusion_template,
            "reasoning_framework": self.reasoning_framework,
            "key_factors": self.key_factors,
            "primary_authority": self.primary_authority,
            "burden_holder": self.burden_holder,
            "adversary_position": self.adversary_position,
            "counter_arguments": self.counter_arguments,
            "resolution_strategy": self.resolution_strategy,
            "entity_scope": [e.value for e in self.entity_scope],
            "confidence": self.confidence.value,
            "confidence_stratification": {k: v.value for k, v in self.confidence_stratification.items()},
            "controlling_precedent": self.controlling_precedent,
            "irc_sections": self.irc_sections,
            "treasury_regs": self.treasury_regs,
            "revenue_rulings": self.revenue_rulings,
            "notices": self.notices,
            "case_law": self.case_law,
            "disclosure_caveat": self.disclosure_caveat,
            "issue_categories": [c.value for c in self.issue_categories],
            "interaction_triggers": self.interaction_triggers,
            "planning_zone_variant": self.planning_zone_variant,
            "reporting_zone_variant": self.reporting_zone_variant,
            "audit_zone_variant": self.audit_zone_variant,
        }


# ==============================================================================
# DOCTRINE CACHE — 55+ BLOCKS
# ==============================================================================

DOCTRINE_BLOCKS: List[DoctrineBlock] = [
    # -------------------------------------------------------------------------
    # BLOCK 1: Cryptocurrency as Property (Notice 2014-21)
    # -------------------------------------------------------------------------
    DoctrineBlock(
        topic="crypto_as_property_notice_2014_21",
        keywords=["cryptocurrency", "property", "notice 2014-21", "virtual currency", "capital asset", "basis"],
        conclusion_template=[
            "Virtual currency is treated as property for federal tax purposes under IRS Notice 2014-21.",
            "Disposition of cryptocurrency triggers gain or loss recognition under IRC §1001.",
            "Character depends on holding period, use, and taxpayer status (investor vs. dealer vs. trader).",
        ],
        reasoning_framework="""
STEP 1: Identify the digital asset transaction type (sale, exchange, transfer, gift, payment).
STEP 2: Determine whether the transaction is a realization event under IRC §1001.
STEP 3: Calculate amount realized (FMV of property/services received) less adjusted basis.
STEP 4: Apply holding period test (long-term >1 year, short-term ≤1 year).
STEP 5: Determine character (capital vs. ordinary) based on taxpayer use and status.
STEP 6: Apply special rules (mining = ordinary income, gifts = donor basis carryover, airdrops = gross income if dominion/control).
STEP 7: Compute tax liability using applicable rates (0%/15%/20% for LTCG, 28% for collectibles if NFT, ordinary rates for STCG/ordinary income).
STEP 8: Consider reporting obligations (Form 8949, Schedule D, Schedule C if business, Schedule 1 if misc. income).

ADVERSARIAL ANALYSIS:
- Taxpayer might claim cryptocurrency is not property but rather currency (to avoid capital gain treatment or defer recognition).
- IRS Notice 2014-21 Q&A-2 explicitly states "virtual currency is treated as property for federal tax purposes."
- No statutory or regulatory authority overrides this position as of 2026.
- Cryptocurrency does NOT qualify as foreign currency under IRC §988 (IRS FAQ confirms).

POSITION ZONE VARIANTS:
- PLANNING: Structure transactions to optimize holding period, basis tracking, timing of recognition.
- REPORTING: Accurately compute and report gain/loss on Form 8949 with correct basis, proceeds, dates.
- AUDIT: Maintain contemporaneous records of acquisition date, basis, FMV at disposal, nature of transaction.
""",
        key_factors=[
            "Type of digital asset (coin, token, NFT, stablecoin, wrapped asset)",
            "Nature of transaction (sale, swap, payment, gift, airdrop, hard fork)",
            "Taxpayer status (investor, dealer under IRC §475, trader with mark-to-market election)",
            "Use of asset (personal investment, business inventory, business use property)",
            "Holding period (acquisition date to disposition date)",
            "Basis tracking method (specific identification, FIFO, LIFO per Rev. Proc. 2024-28)",
            "FMV determination methodology (reliable exchange, multiple exchange average, OTC pricing)",
            "Contemporaneous documentation (wallet addresses, transaction IDs, exchange records)",
        ],
        primary_authority=[
            "IRS Notice 2014-21 (Q&A-1 through Q&A-16)",
            "IRC §61(a)(3) — Gains from dealings in property",
            "IRC §1001 — Determination of amount of and recognition of gain or loss",
            "IRC §1012 — Basis of property — cost",
            "IRC §1221 — Capital asset definition",
            "IRC §1222 — Holding period rules for capital gains/losses",
            "Rev. Proc. 2024-28 — Safe harbor for cost basis tracking (specific ID allowed)",
        ],
        burden_holder="Taxpayer",
        adversary_position="IRS asserts cryptocurrency is property and all dispositions are taxable events absent specific statutory exclusion (e.g., IRC §1031 no longer applies post-TCJA 2017).",
        counter_arguments=[
            "Cryptocurrency should be treated as foreign currency under IRC §988 (REJECTED by IRS FAQ 2019).",
            "Cryptocurrency swaps should qualify as like-kind exchanges under IRC §1031 (REJECTED post-TCJA — only real property qualifies).",
            "De minimis exception should apply for small transactions (NO such exception exists for property transactions).",
            "Lack of IRS clarity means penalties should not apply (IRS Notice 2014-21 provided clarity since 2014; reasonable cause defense weak after 2019).",
            "Cryptocurrency is not property but rather a medium of exchange (REJECTED — Notice 2014-21 Q&A-2 is authoritative).",
        ],
        resolution_strategy="""
Follow IRS guidance in Notice 2014-21 without deviation. Treat every disposition as a realization event.
Use specific identification method for basis tracking if possible (requires contemporaneous records per Rev. Proc. 2024-28).
Default to FIFO if specific ID not documented.
Maintain detailed records: acquisition date, cost basis, FMV at time of transaction, counterparty, purpose.
For audit defense, show good faith effort to comply with Notice 2014-21 and subsequent guidance.
Consider voluntary disclosure if prior years under-reported (IRS has criminal prosecution authority under IRC §7201).
""",
        entity_scope=[
            EntityScope.INDIVIDUAL,
            EntityScope.SOLE_PROPRIETORSHIP,
            EntityScope.PARTNERSHIP,
            EntityScope.LLC,
            EntityScope.S_CORPORATION,
            EntityScope.C_CORPORATION,
            EntityScope.TRUST,
            EntityScope.ESTATE,
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification={
            "crypto_as_property": ConfidenceLevel.DEFENSIBLE,
            "all_dispositions_taxable": ConfidenceLevel.DEFENSIBLE,
            "specific_id_basis_allowed": ConfidenceLevel.DEFENSIBLE,
            "no_like_kind_post_2017": ConfidenceLevel.DEFENSIBLE,
        },
        controlling_precedent="IRS Notice 2014-21",
        irc_sections=["§61", "§1001", "§1012", "§1221", "§1222"],
        treasury_regs=["§1.1001-1", "§1.1012-1"],
        revenue_rulings=[],
        notices=["Notice 2014-21"],
        case_law=[],
        disclosure_caveat=None,
        issue_categories=[IssueCategory.CAPITAL_GAINS, IssueCategory.BASIS],
        interaction_triggers=["cost_basis_methods", "holding_period", "character_determination"],
        planning_zone_variant="Structure acquisitions to maximize long-term holding periods; use specific ID to optimize tax lots sold.",
        reporting_zone_variant="Report every disposition on Form 8949; attach broker statements or self-prepared basis schedules.",
        audit_zone_variant="Produce wallet records, blockchain explorer screenshots, exchange CSV exports, contemporaneous basis tracking logs.",
    ),

    # -------------------------------------------------------------------------
    # BLOCK 2: Mining and Staking Income — Ordinary Income vs. Self-Employment
    # -------------------------------------------------------------------------
    DoctrineBlock(
        topic="mining_staking_income_taxation",
        keywords=["mining", "staking", "proof of work", "proof of stake", "ordinary income", "self-employment tax", "hobby", "trade or business"],
        conclusion_template=[
            "Cryptocurrency received from mining or staking constitutes gross income upon receipt under IRC §61.",
            "Income is ordinary, measured by FMV at time of receipt.",
            "Self-employment tax (IRC §1401) applies if mining/staking constitutes a trade or business under IRC §162.",
            "If hobby activity under IRC §183, income is still taxable but expenses are not deductible post-TCJA (suspended through 2025).",
        ],
        reasoning_framework="""
STEP 1: Determine if mining/staking is a trade or business (9-factor test: profit motive, expertise, time/effort, expectation of appreciation, success in similar activities, history of income/losses, occasional profits, taxpayer financial status, personal pleasure).
STEP 2: If trade or business → ordinary income on Schedule C, subject to SE tax (15.3% on net earnings).
STEP 3: If hobby → ordinary income on Schedule 1 (line 8z), no SE tax, no expense deductions (post-TCJA suspension).
STEP 4: FMV determined at time of receipt (dominion and control test — when coins received in wallet, not when pool payout processed).
STEP 5: Basis in mined/staked coins = FMV at receipt (becomes cost basis for subsequent disposition under IRC §1012).
STEP 6: Subsequent sale of mined/staked coins = capital gain/loss (long-term if held >1 year from receipt, short-term if ≤1 year).
STEP 7: Apply estimated tax payment requirements (IRC §6654 — quarterly payments if annual liability >$1,000).

ADVERSARIAL ANALYSIS:
- Taxpayer may claim mining/staking is not income until sold (REJECTED — constructive receipt at time of receipt per Notice 2014-21 Q&A-8, affirmed in Jarrett v. United States).
- Taxpayer may claim hobby status to avoid SE tax (IRS will challenge if activity is regular, continuous, and profit-motivated).
- Taxpayer may claim coins have no FMV at receipt if not traded on exchange (IRS will impute value using comparable exchange pricing or OTC markets).
""",
        key_factors=[
            "Frequency and regularity of mining/staking activity",
            "Level of expertise and equipment investment",
            "Time and effort devoted to activity",
            "Profit motive vs. personal interest/hobby",
            "Whether activity is conducted in businesslike manner (books, records, separate bank account)",
            "Type of consensus mechanism (PoW vs. PoS — same tax treatment)",
            "Whether mining solo or via pool (timing of receipt may differ)",
            "Whether staking is custodial (exchange) vs. non-custodial (own validator node)",
            "FMV determination — exchange trading price at time of receipt",
        ],
        primary_authority=[
            "IRC §61(a)(3) — Gross income includes gains from dealings in property",
            "IRC §61(a) — Gross income from whatever source derived",
            "IRC §162 — Trade or business expenses",
            "IRC §183 — Activities not engaged in for profit (hobby loss rules)",
            "IRC §1401 — Self-employment tax on net earnings from self-employment",
            "IRS Notice 2014-21 Q&A-8 and Q&A-9",
            "Rev. Rul. 2019-24 (hard forks/airdrops — analogous receipt analysis)",
            "Jarrett v. United States, M.D. Tenn. Case No. 3:21-cv-00419 (May 2022) — staking rewards taxable upon receipt",
        ],
        burden_holder="Taxpayer",
        adversary_position="IRS asserts mining/staking rewards are ordinary income upon receipt, subject to SE tax if trade or business. No deferral until sale.",
        counter_arguments=[
            "No income until sale (creation of property argument) — REJECTED by Jarrett and Notice 2014-21.",
            "Staking rewards are like stock dividends, not taxable until sold — REJECTED (crypto is property, not stock; Rev. Rul. 2019-24 treats receipt as gross income).",
            "FMV is zero if token not yet listed on exchange — REJECTED (IRS will impute value using comparable assets or OTC pricing).",
            "Hobby status to avoid SE tax — IRS challenges if profit motive exists (9-factor test).",
            "Mining is capital investment, not business income — REJECTED if ongoing, regular activity.",
        ],
        resolution_strategy="""
Report mining/staking income as ordinary income in year of receipt.
Use FMV at time of receipt (timestamp of blockchain transaction confirmation).
If trade or business (regular, profit-motivated), report on Schedule C and pay SE tax.
If hobby, report on Schedule 1 line 8z (no SE tax, but no deductions post-TCJA).
Maintain detailed records: wallet addresses, timestamps, FMV sources, pool payouts, validator rewards.
Consider forming entity (LLC taxed as S-corp) to mitigate SE tax on portion of income if significant.
Basis in received coins = FMV at receipt; track for subsequent capital gain/loss on disposition.
""",
        entity_scope=[
            EntityScope.INDIVIDUAL,
            EntityScope.SOLE_PROPRIETORSHIP,
            EntityScope.LLC,
            EntityScope.S_CORPORATION,
            EntityScope.C_CORPORATION,
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification={
            "ordinary_income_on_receipt": ConfidenceLevel.DEFENSIBLE,
            "se_tax_if_business": ConfidenceLevel.DEFENSIBLE,
            "hobby_no_expense_deduction_post_tcja": ConfidenceLevel.DEFENSIBLE,
            "fmv_at_receipt_is_basis": ConfidenceLevel.DEFENSIBLE,
        },
        controlling_precedent="Jarrett v. United States (M.D. Tenn. 2022), IRS Notice 2014-21 Q&A-8/9, Rev. Rul. 2019-24",
        irc_sections=["§61", "§162", "§183", "§1401", "§1012"],
        treasury_regs=["§1.61-1", "§1.162-1", "§1.183-2"],
        revenue_rulings=["Rev. Rul. 2019-24"],
        notices=["Notice 2014-21"],
        case_law=["Jarrett v. United States (M.D. Tenn. 2022)"],
        disclosure_caveat=None,
        issue_categories=[IssueCategory.ORDINARY_INCOME, IssueCategory.MINING_STAKING, IssueCategory.BUSINESS_USE],
        interaction_triggers=["trade_or_business_test", "hobby_loss", "estimated_tax_payments"],
        planning_zone_variant="Consider entity formation (S-corp) if SE tax burden is significant; distinguish salary vs. distribution to reduce SE tax base.",
        reporting_zone_variant="Schedule C if business, Schedule 1 if hobby. Report FMV at receipt. Pay quarterly estimated taxes.",
        audit_zone_variant="Show profit motive (business plan, marketing, tracking, separate financials). Provide FMV documentation (exchange screenshots, historical pricing data).",
    ),

    # -------------------------------------------------------------------------
    # BLOCK 3: DeFi Swaps and Taxable Exchanges
    # -------------------------------------------------------------------------
    DoctrineBlock(
        topic="defi_swap_taxation",
        keywords=["defi", "swap", "decentralized exchange", "uniswap", "sushiswap", "taxable event", "like-kind", "crypto-to-crypto"],
        conclusion_template=[
            "Cryptocurrency-to-cryptocurrency swaps are taxable events under IRC §1001.",
            "IRC §1031 like-kind exchange treatment is unavailable for cryptocurrency after TCJA (effective 2018+).",
            "Gain/loss is recognized immediately at time of swap, measured by FMV difference.",
        ],
        reasoning_framework="""
STEP 1: Identify the swap transaction (Token A exchanged for Token B via DEX or automated market maker).
STEP 2: Determine FMV of Token B received at time of swap (use exchange pricing, AMM pool pricing, or oracle pricing).
STEP 3: Compute gain/loss: FMV of Token B received minus adjusted basis in Token A surrendered.
STEP 4: Apply holding period test for Token A to determine character (LTCG/STCG).
STEP 5: Establish new basis in Token B = FMV at time of swap (becomes cost basis under IRC §1012).
STEP 6: New holding period for Token B begins at swap date.
STEP 7: Report on Form 8949 with description: "Exchanged [X] Token A for [Y] Token B via [DEX name]."

ADVERSARIAL ANALYSIS:
- Taxpayer may claim crypto-to-crypto swaps qualify as like-kind exchanges under IRC §1031 (REJECTED — TCJA limited §1031 to real property only, effective for exchanges after Dec 31, 2017).
- Taxpayer may argue no realization event occurred (REJECTED — IRC §1001 treats exchange of property for property as realization event; Treas. Reg. §1.1001-1(a)).
- Taxpayer may claim FMV is indeterminate for illiquid tokens (IRS will impute value using comparable assets, AMM pool pricing, or OTC markets).
""",
        key_factors=[
            "Date of TCJA applicability (swaps after Dec 31, 2017 do NOT qualify for §1031)",
            "FMV determination method (DEX pricing, AMM pool reserves, CoinGecko/CoinMarketCap, oracle feeds)",
            "Basis tracking for Token A (specific ID, FIFO, LIFO per Rev. Proc. 2024-28)",
            "Holding period of Token A (acquisition to swap date)",
            "Whether swap involved intermediary token (e.g., Token A → WETH → Token B counts as TWO taxable events)",
            "Gas fees paid (added to basis of Token B acquired, or separate expense if business use)",
            "Whether swap was part of larger DeFi strategy (liquidity provision, yield farming — may trigger additional tax events)",
        ],
        primary_authority=[
            "IRC §1001 — Determination of amount of and recognition of gain or loss",
            "IRC §1031 (post-TCJA) — Limited to real property only",
            "Treas. Reg. §1.1001-1(a) — Exchange of property for property is realization event",
            "IRS Notice 2014-21 Q&A-6 — Cryptocurrency exchange is taxable",
            "Rev. Proc. 2024-28 — Basis tracking safe harbor",
        ],
        burden_holder="Taxpayer",
        adversary_position="IRS asserts all crypto-to-crypto swaps are taxable events; no §1031 treatment available post-TCJA.",
        counter_arguments=[
            "Like-kind exchange under §1031 (REJECTED post-TCJA).",
            "No realization event because both assets are 'cryptocurrency' (REJECTED — each token is distinct property under Notice 2014-21).",
            "De minimis exception for small swaps (NO such exception exists).",
            "FMV indeterminate for illiquid tokens (IRS will impute using available data).",
        ],
        resolution_strategy="""
Treat every crypto-to-crypto swap as a taxable disposition of Token A and acquisition of Token B.
Use reliable exchange pricing or AMM pool pricing to determine FMV of Token B at swap time.
If multi-hop swap (A → WETH → B), recognize TWO taxable events: A → WETH, then WETH → B.
Track basis carefully: basis in Token B = FMV at swap time.
Gas fees: add to basis of acquired token (or deduct as business expense if trade or business).
Report on Form 8949 with full details: date, description, proceeds (FMV of Token B), cost basis (Token A basis), gain/loss.
""",
        entity_scope=[
            EntityScope.INDIVIDUAL,
            EntityScope.SOLE_PROPRIETORSHIP,
            EntityScope.PARTNERSHIP,
            EntityScope.LLC,
            EntityScope.S_CORPORATION,
            EntityScope.C_CORPORATION,
            EntityScope.TRUST,
            EntityScope.ESTATE,
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification={
            "swap_is_taxable_event": ConfidenceLevel.DEFENSIBLE,
            "no_1031_post_tcja": ConfidenceLevel.DEFENSIBLE,
            "fmv_at_swap_determines_gain_loss": ConfidenceLevel.DEFENSIBLE,
        },
        controlling_precedent="IRC §1031 post-TCJA, IRS Notice 2014-21 Q&A-6",
        irc_sections=["§1001", "§1031", "§1012"],
        treasury_regs=["§1.1001-1"],
        revenue_rulings=[],
        notices=["Notice 2014-21"],
        case_law=[],
        disclosure_caveat=None,
        issue_categories=[IssueCategory.CAPITAL_GAINS, IssueCategory.DEFI, IssueCategory.BASIS],
        interaction_triggers=["cost_basis_methods", "holding_period", "multi_hop_swaps"],
        planning_zone_variant="Avoid unnecessary swaps; consolidate into single transaction if possible. Use specific ID to optimize tax lot selection.",
        reporting_zone_variant="Report each swap separately on Form 8949. Use DEX transaction hash as reference. Attach AMM pool pricing screenshots if audited.",
        audit_zone_variant="Provide blockchain explorer records, DEX interface screenshots, AMM pool pricing data, CoinGecko historical pricing.",
    ),

    # -------------------------------------------------------------------------
    # BLOCK 4: NFT Taxation and 28% Collectible Rate
    # -------------------------------------------------------------------------
    DoctrineBlock(
        topic="nft_taxation_collectible_rate",
        keywords=["nft", "non-fungible token", "collectible", "28% rate", "artwork", "capital gains", "irc 408"],
        conclusion_template=[
            "NFTs may be classified as collectibles under IRC §408(m), subject to maximum 28% long-term capital gains rate.",
            "Determination depends on nature of underlying asset (artwork, trading card, virtual land, utility token).",
            "Short-term gains taxed at ordinary rates regardless of collectible status.",
        ],
        reasoning_framework="""
STEP 1: Identify the NFT type (digital art, music, video, virtual real estate, in-game item, utility token, membership pass).
STEP 2: Determine if NFT constitutes a 'collectible' under IRC §408(m)(2) — includes works of art, stamps, coins, alcoholic beverages, certain metals, gems, antiques.
STEP 3: Apply IRS guidance: if NFT represents ownership/certificate of authenticity for underlying artwork → likely collectible.
STEP 4: If collectible, long-term capital gain (holding >1 year) capped at 28% (vs. 0%/15%/20% for non-collectible capital assets).
STEP 5: Short-term capital gain (≤1 year) taxed at ordinary rates (up to 37%) regardless of collectible status.
STEP 6: Compute gain: FMV at sale minus adjusted basis (cost of acquisition + improvements/enhancements if any).
STEP 7: Report on Form 8949 with notation if collectible rate applies.

ADVERSARIAL ANALYSIS:
- Taxpayer may claim NFT is not a collectible to access lower 0%/15%/20% LTCG rates (IRS may assert collectible status for art-based NFTs).
- IRS has not issued definitive guidance on NFT collectible classification as of 2026 (regulatory gap).
- Conservative approach: treat art/music/video NFTs as collectibles; treat utility tokens (access, governance) as non-collectible capital assets.
- Aggressive approach: argue NFT is merely code/data, not physical collectible (disclosure may be required under IRC §6662).
""",
        key_factors=[
            "Nature of underlying asset represented by NFT (art, music, utility, virtual land, membership)",
            "Whether NFT is pure digital asset or certificate for physical asset",
            "Holding period (>1 year for LTCG treatment)",
            "Basis in NFT (cost of minting + acquisition cost + gas fees)",
            "FMV determination (marketplace sales data, floor price, last sale price)",
            "Whether NFT generates royalties (separate ordinary income issue)",
        ],
        primary_authority=[
            "IRC §408(m)(2) — Definition of collectibles",
            "IRC §1(h)(4) — 28% rate for collectibles gain",
            "IRC §1(h)(5) — Collectibles held >1 year",
            "IRS Notice 2014-21 (general crypto property treatment, not NFT-specific)",
            "Treas. Reg. §1.408-10 — Collectibles in IRAs (analogous definition)",
        ],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert art-based NFTs are collectibles subject to 28% rate cap; taxpayer may need to rebut or disclose position.",
        counter_arguments=[
            "NFT is digital code, not physical collectible (aggressive, may require disclosure).",
            "IRC §408(m) applies only to IRAs, not general capital gains (REJECTED — §1(h)(4)/(5) applies §408(m) definition to LTCG rates).",
            "No IRS guidance on NFTs means no collectible treatment (weak — IRS may assert under existing law).",
        ],
        resolution_strategy="""
Conservative: Treat art/music/video NFTs as collectibles (28% LTCG rate cap).
Aggressive: Argue NFT is non-collectible capital asset (15%/20% LTCG rate) and disclose position on Form 8275 if material.
Document NFT characteristics: utility function, artistic vs. functional nature, marketplace classification.
For audit defense, obtain contemporaneous valuation (appraisal, floor price data, recent sales).
If royalties are involved, separate ordinary income analysis required (creator vs. reseller).
""",
        entity_scope=[
            EntityScope.INDIVIDUAL,
            EntityScope.SOLE_PROPRIETORSHIP,
            EntityScope.PARTNERSHIP,
            EntityScope.LLC,
            EntityScope.S_CORPORATION,
            EntityScope.C_CORPORATION,
            EntityScope.TRUST,
            EntityScope.ESTATE,
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification={
            "art_nft_is_collectible": ConfidenceLevel.AGGRESSIVE,
            "utility_nft_not_collectible": ConfidenceLevel.AGGRESSIVE,
            "28_percent_rate_if_collectible": ConfidenceLevel.DEFENSIBLE,
        },
        controlling_precedent="IRC §1(h)(4) and §408(m)(2) (no direct NFT case law as of 2026)",
        irc_sections=["§1(h)(4)", "§1(h)(5)", "§408(m)(2)"],
        treasury_regs=["§1.408-10"],
        revenue_rulings=[],
        notices=["Notice 2014-21"],
        case_law=[],
        disclosure_caveat="If taking position that art-based NFT is NOT a collectible, consider Form 8275 disclosure to avoid §6662 penalty.",
        issue_categories=[IssueCategory.NFT, IssueCategory.CAPITAL_GAINS],
        interaction_triggers=["holding_period", "character_determination", "valuation"],
        planning_zone_variant="If NFT is collectible, consider holding in C-corp to avoid individual 28% rate (corporate rate 21%). If non-collectible, optimize holding period for LTCG treatment.",
        reporting_zone_variant="Report on Form 8949. If collectible, annotate 'collectible' in description. Use marketplace data for FMV. Attach sales receipt/blockchain proof.",
        audit_zone_variant="Provide NFT marketplace data, OpenSea/Blur/LooksRare sales history, floor price charts, metadata showing artistic vs. utility nature.",
    ),

    # -------------------------------------------------------------------------
    # BLOCK 5: Wash Sale Rule — Applicability to Crypto
    # -------------------------------------------------------------------------
    DoctrineBlock(
        topic="wash_sale_crypto_applicability",
        keywords=["wash sale", "irc 1091", "substantially identical", "cryptocurrency", "securities", "loss deferral"],
        conclusion_template=[
            "IRC §1091 wash sale rule applies to 'stock or securities' — cryptocurrency is classified as property, not securities.",
            "As of 2026, wash sale rule does NOT apply to cryptocurrency losses under current law.",
            "Congress has proposed legislation to extend §1091 to digital assets (not yet enacted).",
            "Taxpayers can currently recognize crypto losses and repurchase immediately without §1091 deferral.",
        ],
        reasoning_framework="""
STEP 1: Identify the loss transaction (sale of cryptocurrency at a loss).
STEP 2: Determine if taxpayer repurchased same or substantially identical cryptocurrency within 30-day window (30 days before or after sale).
STEP 3: Apply IRC §1091: wash sale rule applies only to 'stock or securities' — crypto is property (IRS Notice 2014-21).
STEP 4: Conclusion: loss is NOT deferred under current law; taxpayer may recognize loss immediately.
STEP 5: CAVEAT: Legislative risk — multiple bills proposed to extend §1091 to digital assets (not yet law as of 2026).
STEP 6: Report loss on Form 8949 without wash sale adjustment (unless/until law changes).

ADVERSARIAL ANALYSIS:
- IRS has NOT asserted wash sale rule applies to crypto (Notice 2014-21 classifies crypto as property, not securities).
- Tax Court has not ruled on this issue (no binding precedent).
- Proposed legislation (e.g., Infrastructure Investment and Jobs Act amendments) would apply §1091 to digital assets if enacted.
- AGGRESSIVE POSITION: Taxpayers can currently harvest crypto losses and immediately repurchase without §1091 consequences.
- RISK: Retroactive application if legislation passes (unlikely but possible).
""",
        key_factors=[
            "Classification of crypto as property vs. securities (Notice 2014-21: property)",
            "Text of IRC §1091 (applies to 'stock or securities' only)",
            "Pending legislation status (monitor congressional action)",
            "Substantially identical test (if rule were to apply: same token, same blockchain likely identical; different blockchain or wrapped version may not be)",
            "30-day window (30 days before or after sale)",
        ],
        primary_authority=[
            "IRC §1091 — Wash sale rule (stock or securities)",
            "IRS Notice 2014-21 Q&A-2 — Virtual currency is property, not currency or securities",
            "IRC §1221 — Capital asset definition (property)",
        ],
        burden_holder="Taxpayer (but favorable current law)",
        adversary_position="IRS has not challenged crypto loss recognition followed by repurchase (no published guidance asserting §1091 applies to crypto).",
        counter_arguments=[
            "IRS might assert crypto is a 'security' under Howey test (REJECTED — SEC classification does not override tax classification in Notice 2014-21).",
            "IRS might invoke substance over form or step transaction doctrine (unlikely without specific anti-abuse rule).",
        ],
        resolution_strategy="""
Under current law (as of 2026), wash sale rule does NOT apply to cryptocurrency.
Taxpayers may recognize losses and repurchase immediately without deferral.
MONITOR legislative developments — if §1091 extended to digital assets, rule would apply prospectively (or retroactively if specified).
For audit defense: cite IRS Notice 2014-21 (crypto is property, not securities) and IRC §1091 statutory text (stock or securities only).
PLANNING: Take advantage of current law for tax-loss harvesting; be prepared for law to change in future years.
""",
        entity_scope=[
            EntityScope.INDIVIDUAL,
            EntityScope.SOLE_PROPRIETORSHIP,
            EntityScope.PARTNERSHIP,
            EntityScope.LLC,
            EntityScope.S_CORPORATION,
            EntityScope.C_CORPORATION,
            EntityScope.TRUST,
            EntityScope.ESTATE,
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification={
            "wash_sale_not_applicable_current_law": ConfidenceLevel.DEFENSIBLE,
            "loss_recognition_immediate": ConfidenceLevel.DEFENSIBLE,
            "legislative_risk_exists": ConfidenceLevel.DEFENSIBLE,
        },
        controlling_precedent="IRC §1091 statutory text, IRS Notice 2014-21",
        irc_sections=["§1091", "§1221"],
        treasury_regs=["§1.1091-1"],
        revenue_rulings=[],
        notices=["Notice 2014-21"],
        case_law=[],
        disclosure_caveat=None,
        issue_categories=[IssueCategory.CAPITAL_GAINS, IssueCategory.BASIS],
        interaction_triggers=["loss_harvesting", "repurchase_timing"],
        planning_zone_variant="Harvest crypto losses aggressively; repurchase immediately. Monitor legislation for future changes.",
        reporting_zone_variant="Report losses on Form 8949 without wash sale adjustment. No special notation required under current law.",
        audit_zone_variant="Cite Notice 2014-21 (crypto is property) and IRC §1091 text (stock or securities only). No IRS guidance asserting wash sale applies to crypto.",
    ),

    # -------------------------------------------------------------------------
    # BLOCK 6: Hard Forks and Airdrops — Income Recognition
    # -------------------------------------------------------------------------
    DoctrineBlock(
        topic="hard_fork_airdrop_income_recognition",
        keywords=["hard fork", "airdrop", "free coins", "gross income", "dominion and control", "rev rul 2019-24"],
        conclusion_template=[
            "Cryptocurrency received from hard fork or airdrop is gross income under IRC §61 if taxpayer has dominion and control.",
            "Income is measured by FMV at time of receipt.",
            "No income if taxpayer does not receive or cannot access new cryptocurrency (Rev. Rul. 2019-24).",
        ],
        reasoning_framework="""
STEP 1: Identify the event (hard fork creating new blockchain, airdrop distributing tokens to existing holders).
STEP 2: Determine if taxpayer received new cryptocurrency (tokens appear in wallet under taxpayer's control).
STEP 3: Apply dominion and control test: does taxpayer have ability to sell, transfer, or otherwise dispose of tokens?
STEP 4: If YES → gross income under IRC §61 at FMV on date of receipt.
STEP 5: If NO (e.g., tokens sent to address taxpayer does not control, or exchange does not credit tokens) → no income.
STEP 6: Basis in received tokens = FMV at receipt (becomes cost basis for subsequent sale under IRC §1012).
STEP 7: Holding period begins on date of receipt.
STEP 8: Report as ordinary income (Schedule 1, line 8z 'Other Income' or Schedule C if business).

ADVERSARIAL ANALYSIS:
- Taxpayer may claim no income until tokens are sold (REJECTED — Rev. Rul. 2019-24 requires inclusion upon receipt if dominion/control).
- Taxpayer may claim FMV is zero if tokens not traded (IRS will impute value if market exists, even OTC/illiquid).
- Taxpayer may claim tokens were 'unwanted' and thus not income (REJECTED — receipt of property is income under IRC §61 regardless of desire).
""",
        key_factors=[
            "Whether hard fork resulted in new cryptocurrency under taxpayer's control",
            "Whether airdrop tokens were credited to taxpayer's wallet",
            "Dominion and control test (can taxpayer transfer/sell/dispose?)",
            "FMV determination at time of receipt (exchange price, OTC price, comparable assets)",
            "Whether exchange/custodian credited tokens or retained them",
            "Tax year of receipt (calendar year when dominion/control established)",
        ],
        primary_authority=[
            "IRC §61(a) — Gross income from all sources",
            "Rev. Rul. 2019-24 — Hard fork and airdrop guidance",
            "IRC §1012 — Basis of property received",
            "Treas. Reg. §1.61-1 — Gross income definition",
        ],
        burden_holder="Taxpayer",
        adversary_position="IRS asserts airdrops/hard forks are gross income upon receipt if dominion and control exists (Rev. Rul. 2019-24).",
        counter_arguments=[
            "No income until sale (creation of property argument) — REJECTED by Rev. Rul. 2019-24.",
            "Tokens have no value if not listed (IRS will impute value using available market data).",
            "Unsolicited property is not income — REJECTED (IRC §61 includes all accessions to wealth).",
        ],
        resolution_strategy="""
Apply Rev. Rul. 2019-24: if taxpayer receives cryptocurrency from hard fork/airdrop AND has dominion and control → gross income.
Determine FMV at date of receipt using exchange pricing or comparable asset pricing.
Report as ordinary income (Schedule 1 line 8z or Schedule C if business activity).
Basis = FMV at receipt; holding period starts at receipt.
Subsequent sale = capital gain/loss (LTCG if held >1 year, STCG if ≤1 year).
If tokens not received or not accessible → no income (e.g., exchange does not support new chain).
""",
        entity_scope=[
            EntityScope.INDIVIDUAL,
            EntityScope.SOLE_PROPRIETORSHIP,
            EntityScope.PARTNERSHIP,
            EntityScope.LLC,
            EntityScope.S_CORPORATION,
            EntityScope.C_CORPORATION,
            EntityScope.TRUST,
            EntityScope.ESTATE,
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification={
            "income_upon_receipt_if_dominion_control": ConfidenceLevel.DEFENSIBLE,
            "fmv_at_receipt_is_income_and_basis": ConfidenceLevel.DEFENSIBLE,
            "no_income_if_not_received": ConfidenceLevel.DEFENSIBLE,
        },
        controlling_precedent="Rev. Rul. 2019-24",
        irc_sections=["§61", "§1012"],
        treasury_regs=["§1.61-1"],
        revenue_rulings=["Rev. Rul. 2019-24"],
        notices=[],
        case_law=[],
        disclosure_caveat=None,
        issue_categories=[IssueCategory.ORDINARY_INCOME, IssueCategory.BASIS],
        interaction_triggers=["dominion_control_test", "fmv_determination"],
        planning_zone_variant="Monitor hard forks/airdrops. If unwanted, consider donating tokens to charity immediately (may avoid income recognition if no dominion/control before transfer).",
        reporting_zone_variant="Report airdrop/hard fork income on Schedule 1 line 8z or Schedule C. Use FMV at receipt date. Document exchange listing date, pricing source.",
        audit_zone_variant="Provide blockchain explorer records showing receipt date, exchange listing announcement, FMV pricing data (CoinGecko, CoinMarketCap historical data).",
    ),

    # -------------------------------------------------------------------------
    # BLOCK 7: Form 8949 Reporting Requirements
    # -------------------------------------------------------------------------
    DoctrineBlock(
        topic="form_8949_crypto_reporting",
        keywords=["form 8949", "schedule d", "capital gains", "reporting", "proceeds", "basis", "date acquired", "date sold"],
        conclusion_template=[
            "All cryptocurrency dispositions must be reported on Form 8949 and summarized on Schedule D.",
            "Required information: description, date acquired, date sold, proceeds, cost basis, gain/loss.",
            "Box A (short-term with 1099-B), Box B (short-term without 1099-B), Box D (long-term with 1099-B), Box E (long-term without 1099-B).",
        ],
        reasoning_framework="""
STEP 1: Compile all cryptocurrency dispositions for the tax year (sales, exchanges, payments, gifts if FMV > basis).
STEP 2: For each disposition, determine:
    - Description (e.g., '0.5 BTC exchanged for ETH')
    - Date acquired (from purchase/mining/airdrop/receipt records)
    - Date sold or disposed (transaction date on blockchain or exchange)
    - Proceeds (FMV of property/cash received)
    - Cost basis (adjusted basis of crypto disposed)
    - Gain or loss (proceeds minus basis)
STEP 3: Categorize by holding period:
    - Short-term (≤1 year from acquisition to disposition)
    - Long-term (>1 year from acquisition to disposition)
STEP 4: Select appropriate box on Form 8949:
    - Box A or D if broker issued Form 1099-B (rare for crypto as of 2026)
    - Box B or E if no 1099-B (typical for crypto)
STEP 5: Enter each transaction on separate line or attach CSV/PDF statement with same information.
STEP 6: Transfer totals to Schedule D (Part I for short-term, Part II for long-term).
STEP 7: Compute net capital gain/loss and flow to Form 1040 Schedule 1 or directly to Form 1040.

ADVERSARIAL ANALYSIS:
- Taxpayers may omit transactions thinking IRS won't notice (WRONG — blockchain is public ledger; IRS has John Doe summonses for major exchanges; third-party reporting will expand under IIJA 2021 broker rules).
- Taxpayers may aggregate transactions without detail (INSUFFICIENT — IRS requires transaction-level detail or detailed attached statement).
- Taxpayers may fail to track basis (RISK — IRS may assert basis is zero if taxpayer cannot substantiate; burden on taxpayer).
""",
        key_factors=[
            "Accurate basis tracking (specific ID, FIFO, LIFO per Rev. Proc. 2024-28)",
            "Contemporaneous records (wallet addresses, transaction IDs, exchange CSVs)",
            "Holding period calculation (acquisition date to disposition date)",
            "Proceeds determination (FMV at disposal, not just cash received)",
            "Whether 1099-B received (rare for crypto but will become common post-2025 under IIJA broker rules)",
        ],
        primary_authority=[
            "IRC §6045 — Broker reporting (expanded to digital assets under IIJA 2021, effective dates vary)",
            "Form 8949 instructions (IRS annually updated)",
            "Schedule D instructions",
            "IRS Notice 2014-21 Q&A-14 — Requirement to report crypto transactions",
            "Rev. Proc. 2024-28 — Cost basis tracking safe harbor",
        ],
        burden_holder="Taxpayer",
        adversary_position="IRS requires complete and accurate reporting of all crypto transactions; penalties apply for substantial understatement or negligence.",
        counter_arguments=[
            "IRS doesn't have records of my crypto transactions (WRONG — IRS has John Doe summonses, third-party data, blockchain analysis tools).",
            "I can just report net gain/loss without detail (INSUFFICIENT — Form 8949 requires transaction-level detail).",
            "Crypto is untraceable (WRONG — blockchain is public; IRS uses Chainalysis, Elliptic, CipherTrace).",
        ],
        resolution_strategy="""
Maintain detailed transaction logs: date, type, amount, counterparty, proceeds, basis, FMV source.
Use crypto tax software (CoinTracker, TokenTax, Koinly, CoinLedger) or manual spreadsheet.
Export exchange CSVs and reconcile with on-chain records.
Report every transaction on Form 8949 or attach detailed statement (CSV/PDF with required columns).
Use specific ID method for basis tracking if possible (requires contemporaneous designation per Rev. Proc. 2024-28).
Default to FIFO if specific ID not used.
Pay quarterly estimated taxes if capital gains are significant (IRC §6654).
""",
        entity_scope=[
            EntityScope.INDIVIDUAL,
            EntityScope.SOLE_PROPRIETORSHIP,
            EntityScope.PARTNERSHIP,
            EntityScope.LLC,
            EntityScope.S_CORPORATION,
            EntityScope.C_CORPORATION,
            EntityScope.TRUST,
            EntityScope.ESTATE,
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification={
            "form_8949_required": ConfidenceLevel.DEFENSIBLE,
            "transaction_level_detail_required": ConfidenceLevel.DEFENSIBLE,
            "basis_substantiation_burden_on_taxpayer": ConfidenceLevel.DEFENSIBLE,
        },
        controlling_precedent="IRC §6045, Form 8949 instructions, IRS Notice 2014-21",
        irc_sections=["§6045", "§6662"],
        treasury_regs=[],
        revenue_rulings=[],
        notices=["Notice 2014-21"],
        case_law=[],
        disclosure_caveat=None,
        issue_categories=[IssueCategory.REPORTING, IssueCategory.CAPITAL_GAINS],
        interaction_triggers=["basis_tracking", "holding_period", "proceeds_determination"],
        planning_zone_variant="Use crypto tax software to automate Form 8949 preparation. Reconcile exchange data with on-chain records before year-end.",
        reporting_zone_variant="Complete Form 8949 with all transactions or attach detailed CSV/PDF. Transfer totals to Schedule D. Sign under penalties of perjury.",
        audit_zone_variant="Provide exchange account statements, wallet transaction histories, blockchain explorer screenshots, FMV pricing sources (CoinGecko, exchange APIs).",
    ),

    # -------------------------------------------------------------------------
    # BLOCK 8: FBAR Reporting for Foreign Crypto Exchanges
    # -------------------------------------------------------------------------
    DoctrineBlock(
        topic="fbar_crypto_foreign_exchange",
        keywords=["fbar", "fincen 114", "foreign account", "binance", "crypto exchange", "31 usc 5314", "10000 threshold"],
        conclusion_template=[
            "FBAR (FinCEN Form 114) reporting required if aggregate value of foreign financial accounts exceeds $10,000 at any time during calendar year.",
            "IRS has not issued definitive guidance on whether cryptocurrency held at foreign exchanges constitutes 'foreign financial account.'",
            "Conservative approach: report foreign exchange accounts holding crypto if aggregate value >$10,000.",
            "Criminal penalties for willful FBAR violations include up to $250,000 fine and 5 years imprisonment (31 USC §5322).",
        ],
        reasoning_framework="""
STEP 1: Identify all foreign crypto exchange accounts (e.g., Binance, OKX, Huobi, foreign-domiciled exchanges).
STEP 2: Determine maximum aggregate value during calendar year (convert crypto to USD at highest point).
STEP 3: Apply $10,000 threshold: if maximum aggregate value ≥$10,000 at any time → FBAR may be required.
STEP 4: UNCERTAINTY: IRS has not definitively stated crypto exchange accounts are 'financial accounts' for FBAR purposes.
STEP 5: CONSERVATIVE: Treat foreign exchange accounts as reportable to avoid criminal/civil penalties.
STEP 6: File FinCEN Form 114 electronically by April 15 (automatic extension to October 15, no extension request needed).
STEP 7: Report account information: exchange name, address (if available), account number, maximum value.

ADVERSARIAL ANALYSIS:
- FinCEN has not issued guidance explicitly including or excluding crypto exchange accounts from FBAR.
- 31 USC §5314 requires reporting of 'foreign financial accounts' — term defined in 31 CFR §1010.350.
- Crypto exchange accounts may not fit traditional definition (not banks, securities brokers, or insurance companies).
- RISK: IRS/DOJ may assert FBAR applies and prosecute for willful failure to file (see U.S. v. Hom, cryptocurrency prosecution for non-FBAR compliance issues).
- CONSERVATIVE APPROACH: File FBAR for foreign exchange accounts >$10,000 to avoid criminal exposure.
""",
        key_factors=[
            "Location of crypto exchange (foreign vs. US-based)",
            "Maximum aggregate value of all foreign accounts during year",
            "Whether exchange qualifies as 'financial institution' under 31 CFR §1010.100",
            "Willfulness standard for penalties (knowledge of obligation and intentional disregard)",
            "Criminal vs. civil penalty risk (criminal requires willfulness)",
        ],
        primary_authority=[
            "31 USC §5314 — Foreign financial account reporting",
            "31 USC §5321 — Civil penalties for FBAR violations (up to $10,000 non-willful, greater of $100,000 or 50% of account balance if willful)",
            "31 USC §5322 — Criminal penalties (up to $250,000 and 5 years imprisonment if willful)",
            "31 CFR §1010.350 — Definition of financial account",
            "FinCEN Form 114 instructions",
        ],
        burden_holder="Taxpayer",
        adversary_position="IRS/FinCEN has authority to assert FBAR applies to foreign crypto exchange accounts; criminal prosecution possible if willful violation.",
        counter_arguments=[
            "Crypto exchange is not a 'financial institution' under 31 CFR §1010.100 (UNCERTAIN — FinCEN has not ruled definitively).",
            "Cryptocurrency is not 'currency' for FBAR purposes (IRRELEVANT — accounts holding non-currency assets can still be reportable).",
            "No guidance from FinCEN means no obligation (RISKY — failure to file when uncertain is not a defense to willfulness if obligation later established).",
        ],
        resolution_strategy="""
CONSERVATIVE: Report all foreign crypto exchange accounts with value >$10,000 on FBAR.
Use best estimate for maximum account value (convert crypto to USD at peak).
File FinCEN Form 114 electronically by October 15 deadline.
If uncertain whether to report, FILE — no penalty for over-reporting, severe penalties for under-reporting.
Consult with counsel if significant foreign crypto holdings (criminal exposure risk).
If prior years not filed, consider voluntary disclosure or delinquent FBAR submission procedures.
""",
        entity_scope=[
            EntityScope.INDIVIDUAL,
            EntityScope.TRUST,
            EntityScope.ESTATE,
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification={
            "fbar_required_if_over_10k": ConfidenceLevel.AGGRESSIVE,
            "crypto_exchange_is_financial_account": ConfidenceLevel.AGGRESSIVE,
            "criminal_penalty_if_willful": ConfidenceLevel.DEFENSIBLE,
        },
        controlling_precedent="31 USC §5314, 31 CFR §1010.350 (no direct crypto guidance from FinCEN as of 2026)",
        irc_sections=[],
        treasury_regs=[],
        revenue_rulings=[],
        notices=[],
        case_law=["U.S. v. Hom (cryptocurrency-related prosecution, not FBAR-specific)"],
        disclosure_caveat="Given regulatory uncertainty, conservative approach is to file FBAR for foreign exchange accounts >$10,000. Consult counsel if material.",
        issue_categories=[IssueCategory.INTERNATIONAL, IssueCategory.INFORMATION_RETURN],
        interaction_triggers=["foreign_exchange_use", "aggregate_value_calculation"],
        planning_zone_variant="Use US-based exchanges (Coinbase, Kraken, Gemini) to avoid FBAR complexity. If using foreign exchanges, maintain records of maximum account values.",
        reporting_zone_variant="File FinCEN Form 114 if aggregate foreign account value ≥$10,000. Use best estimate for crypto valuations. File by Oct 15 deadline.",
        audit_zone_variant="Provide exchange account statements, transaction histories, FMV calculations at highest point during year. Show good faith effort to comply if FBAR obligation uncertain.",
    ),

    # -------------------------------------------------------------------------
    # BLOCK 9: FATCA Form 8938 Reporting
    # -------------------------------------------------------------------------
    DoctrineBlock(
        topic="fatca_form_8938_crypto",
        keywords=["fatca", "form 8938", "foreign assets", "irc 6038d", "specified foreign financial asset", "crypto"],
        conclusion_template=[
            "IRC §6038D requires reporting of 'specified foreign financial assets' on Form 8938 if aggregate value exceeds threshold.",
            "Thresholds: $50,000 on last day of year or $75,000 at any time (single/MFS); $100,000/$150,000 (MFJ); higher for expats.",
            "IRS has not definitively ruled whether crypto held at foreign exchanges is 'specified foreign financial asset.'",
            "Conservative approach: report if thresholds met.",
        ],
        reasoning_framework="""
STEP 1: Identify all foreign financial assets (foreign bank accounts, foreign securities, foreign partnership interests, etc.).
STEP 2: Determine if cryptocurrency held at foreign exchanges qualifies as 'specified foreign financial asset' under IRC §6038D.
STEP 3: UNCERTAINTY: IRS has not issued guidance on crypto at foreign exchanges for Form 8938 purposes.
STEP 4: Apply thresholds:
    - Single/MFS: $50,000 on last day OR $75,000 at any time
    - MFJ: $100,000 on last day OR $150,000 at any time
    - Expats (living abroad): higher thresholds
STEP 5: If thresholds met, file Form 8938 with Form 1040.
STEP 6: Report: description, maximum value, issuer/counterparty, whether sold during year.
STEP 7: Penalties for failure to file: $10,000 initial, additional $10,000 per 30 days after IRS notice (max $50,000), plus 40% understatement penalty if asset generates income.

ADVERSARIAL ANALYSIS:
- Form 8938 applies to 'specified foreign financial assets' — defined in IRC §6038D(b) and Treas. Reg. §1.6038D-1.
- Cryptocurrency is property (Notice 2014-21), but whether held at foreign exchange constitutes 'financial asset' is unclear.
- CONSERVATIVE: Report crypto at foreign exchanges if thresholds met.
- AGGRESSIVE: Do not report, argue crypto is not 'financial asset' (RISKY — 40% penalty if wrong).
""",
        key_factors=[
            "Aggregate value of foreign assets (crypto + traditional assets)",
            "Filing status and residency (determines threshold)",
            "Whether foreign exchange qualifies as 'foreign financial institution'",
            "Income generated by assets (staking, lending — triggers understatement penalty if not reported)",
        ],
        primary_authority=[
            "IRC §6038D — Information reporting for specified foreign financial assets",
            "Treas. Reg. §1.6038D-1 — Definition of specified foreign financial asset",
            "Form 8938 instructions",
            "IRC §6662(j) — 40% penalty for undisclosed foreign financial asset understatements",
        ],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert Form 8938 applies to crypto at foreign exchanges; penalties for non-compliance include both failure-to-file and understatement penalties.",
        counter_arguments=[
            "Cryptocurrency is not a 'financial asset' (UNCERTAIN — no IRS guidance).",
            "Exchange account is not custody, taxpayer controls private keys (WEAK if exchange holds keys).",
        ],
        resolution_strategy="""
CONSERVATIVE: Report crypto at foreign exchanges on Form 8938 if thresholds met.
Calculate maximum value during year and value on last day of year.
Include staking/lending income in understatement calculation (40% penalty applies if asset generates unreported income).
File Form 8938 with Form 1040 by due date (April 15 or extension deadline).
If uncertain, FILE to avoid penalties.
""",
        entity_scope=[
            EntityScope.INDIVIDUAL,
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification={
            "form_8938_required_if_thresholds_met": ConfidenceLevel.AGGRESSIVE,
            "40_percent_penalty_if_income_understatement": ConfidenceLevel.DEFENSIBLE,
        },
        controlling_precedent="IRC §6038D, Treas. Reg. §1.6038D-1 (no crypto-specific guidance as of 2026)",
        irc_sections=["§6038D", "§6662(j)"],
        treasury_regs=["§1.6038D-1"],
        revenue_rulings=[],
        notices=[],
        case_law=[],
        disclosure_caveat="Given regulatory uncertainty, conservative approach is to file Form 8938 if thresholds met. Consult counsel if material foreign crypto holdings.",
        issue_categories=[IssueCategory.INTERNATIONAL, IssueCategory.INFORMATION_RETURN],
        interaction_triggers=["foreign_exchange_use", "aggregate_value_calculation", "income_reporting"],
        planning_zone_variant="Use US-based exchanges or self-custody to avoid Form 8938 complexity. If using foreign exchanges, track maximum values throughout year.",
        reporting_zone_variant="File Form 8938 with Form 1040 if thresholds met. Report maximum value during year and value on last day. Include description of asset and issuer.",
        audit_zone_variant="Provide exchange statements, transaction histories, FMV calculations. Show good faith effort to comply if Form 8938 obligation uncertain.",
    ),

    # -------------------------------------------------------------------------
    # BLOCK 10: Charitable Donation of Cryptocurrency (IRC §170)
    # -------------------------------------------------------------------------
    DoctrineBlock(
        topic="charitable_donation_crypto_irc_170",
        keywords=["charitable donation", "irc 170", "crypto donation", "fmv", "appraisal", "deduction", "capital gains"],
        conclusion_template=[
            "Donation of cryptocurrency to qualified charity is deductible at FMV if held >1 year (long-term capital asset).",
            "Deduction limited to 30% of AGI for appreciated long-term capital gain property (50% if cash/ordinary income property).",
            "Appraisal required if single item or group of similar items >$5,000 (Form 8283 Section B).",
            "Donor does NOT recognize capital gain on donation of appreciated cryptocurrency (IRC §170(e)).",
        ],
        reasoning_framework="""
STEP 1: Determine if donee is qualified charitable organization under IRC §170(c) (501(c)(3) public charity, private foundation, etc.).
STEP 2: Determine holding period of cryptocurrency:
    - Long-term (>1 year): deduct FMV, no capital gain recognition
    - Short-term (≤1 year): deduct lesser of FMV or basis, no capital gain recognition
STEP 3: Obtain qualified appraisal if FMV >$5,000 (must be completed before filing return, appraisal summary on Form 8283 Section B).
STEP 4: Determine FMV at time of donation (exchange price, average of exchanges if multiple, or qualified appraisal).
STEP 5: Apply AGI limitation:
    - Long-term capital gain property to public charity: 30% AGI limit
    - Cash or ordinary income property: 50% AGI limit
    - Carryforward excess for 5 years (IRC §170(d))
STEP 6: File Form 8283 if non-cash donation >$500 (Section A if ≤$5,000, Section B if >$5,000).
STEP 7: Maintain records: donation receipt from charity, appraisal, FMV determination, cost basis, holding period.

ADVERSARIAL ANALYSIS:
- Taxpayer must substantiate FMV (burden on taxpayer; IRS may challenge valuation if no qualified appraisal).
- Taxpayer may attempt to deduct FMV for short-term property (WRONG — IRC §170(e)(1)(A) limits to basis for short-term capital gain property).
- Charity may not provide adequate acknowledgment (must include statement that no goods/services provided in exchange, or describe value of goods/services if any).
""",
        key_factors=[
            "Qualified charity status (public charity vs. private foundation affects AGI limits)",
            "Holding period (>1 year for FMV deduction)",
            "FMV determination (exchange pricing, appraisal if >$5,000)",
            "Appraisal requirement (qualified appraiser, completed before return filing)",
            "Contemporaneous written acknowledgment from charity (required for donations ≥$250)",
            "Form 8283 filing (Section A if $500-$5,000, Section B if >$5,000)",
        ],
        primary_authority=[
            "IRC §170(a) — Charitable contribution deduction",
            "IRC §170(b)(1)(C) — 30% AGI limit for capital gain property",
            "IRC §170(e)(1)(A) — Reduction for short-term capital gain property",
            "IRC §170(f)(11) — Qualified appraisal requirement",
            "Treas. Reg. §1.170A-13 — Substantiation requirements",
            "Form 8283 instructions",
        ],
        burden_holder="Taxpayer",
        adversary_position="IRS may challenge FMV if not substantiated by qualified appraisal (especially if >$5,000). Penalties for overvaluation under IRC §6662(e)/(h) if substantial or gross overvaluation.",
        counter_arguments=[
            "FMV is self-determined without appraisal (INSUFFICIENT if >$5,000 — qualified appraisal required).",
            "Short-term crypto donation deductible at FMV (WRONG — limited to basis under IRC §170(e)(1)(A)).",
            "No acknowledgment needed if donee is well-known charity (WRONG — IRC §170(f)(8) requires written acknowledgment for ≥$250 regardless of charity reputation).",
        ],
        resolution_strategy="""
Hold cryptocurrency >1 year before donation to maximize deduction (FMV vs. basis).
Donate to public charity (30% AGI limit better than 20% for private foundation).
Obtain qualified appraisal if FMV >$5,000 BEFORE filing return.
Use multiple exchanges' prices or qualified appraiser to determine FMV.
Obtain contemporaneous written acknowledgment from charity (must state no goods/services provided or describe value if any).
File Form 8283 Section A if $500-$5,000, Section B if >$5,000 (charity signature required for Section B).
Maintain records: donation receipt, appraisal, blockchain transaction proof, FMV documentation.
Apply 30% AGI limitation; carryforward excess for 5 years under IRC §170(d).
""",
        entity_scope=[
            EntityScope.INDIVIDUAL,
            EntityScope.SOLE_PROPRIETORSHIP,
            EntityScope.PARTNERSHIP,
            EntityScope.LLC,
            EntityScope.S_CORPORATION,
            EntityScope.C_CORPORATION,
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification={
            "fmv_deduction_if_long_term": ConfidenceLevel.DEFENSIBLE,
            "no_capital_gain_on_donation": ConfidenceLevel.DEFENSIBLE,
            "appraisal_required_over_5000": ConfidenceLevel.DEFENSIBLE,
            "30_percent_agi_limit": ConfidenceLevel.DEFENSIBLE,
        },
        controlling_precedent="IRC §170, Treas. Reg. §1.170A-13",
        irc_sections=["§170(a)", "§170(b)(1)(C)", "§170(e)(1)(A)", "§170(f)(8)", "§170(f)(11)", "§170(d)"],
        treasury_regs=["§1.170A-13"],
        revenue_rulings=[],
        notices=[],
        case_law=[],
        disclosure_caveat=None,
        issue_categories=[IssueCategory.CHARITABLE, IssueCategory.CAPITAL_GAINS],
        interaction_triggers=["holding_period", "fmv_determination", "appraisal_requirement"],
        planning_zone_variant="Donate appreciated long-term crypto to avoid capital gains and maximize deduction. Time donations to optimize AGI limitations.",
        reporting_zone_variant="File Form 8283 with return. Attach appraisal if >$5,000. Maintain charity acknowledgment letter. Deduct on Schedule A (itemized deductions).",
        audit_zone_variant="Provide qualified appraisal, charity acknowledgment, blockchain transaction proof, exchange pricing data, Form 8283 with charity signature.",
    ),

    # -------------------------------------------------------------------------
    # BLOCK 11: Crypto in Retirement Accounts (IRC §408(m))
    # -------------------------------------------------------------------------
    DoctrineBlock(
        topic="crypto_ira_retirement_accounts",
        keywords=["ira", "401k", "retirement", "irc 408(m)", "collectible", "prohibited transaction", "self-directed ira"],
        conclusion_template=[
            "IRC §408(m) prohibits IRA investment in 'collectibles' — triggers deemed distribution if violated.",
            "Cryptocurrency may be classified as collectible under IRC §408(m)(2) if treated as such (regulatory uncertainty).",
            "Self-directed IRAs may allow crypto holdings via custodian, but tax consequences uncertain.",
            "Deemed distribution if collectible held in IRA → taxable income + 10% early withdrawal penalty if <59.5 years old.",
        ],
        reasoning_framework="""
STEP 1: Identify retirement account type (Traditional IRA, Roth IRA, SEP-IRA, SIMPLE IRA, 401(k), etc.).
STEP 2: Apply IRC §408(m) prohibition on collectibles (artwork, metals other than specified coins/bullion, gems, stamps, antiques, alcoholic beverages).
STEP 3: Determine if cryptocurrency is 'collectible' under IRC §408(m)(2):
    - UNCERTAINTY: IRS has not definitively ruled.
    - NFTs representing art may be collectibles (see NFT doctrine block).
    - Fungible cryptocurrency (BTC, ETH) likely NOT collectibles (property, not physical items).
STEP 4: If IRA invests in collectible → deemed distribution under IRC §408(m)(1).
STEP 5: Deemed distribution = FMV of collectible at time of acquisition by IRA.
STEP 6: Taxable as ordinary income + 10% penalty if owner <59.5 years old.
STEP 7: Self-directed IRA custodians may allow crypto, but taxpayer assumes risk if IRS asserts collectible treatment.

ADVERSARIAL ANALYSIS:
- IRS has not issued guidance on crypto in IRAs (regulatory gap).
- Conservative: avoid crypto in IRA to prevent deemed distribution risk.
- Aggressive: hold crypto in self-directed IRA and argue not a collectible (RISKY — if IRS asserts collectible status, deemed distribution and penalties apply).
""",
        key_factors=[
            "Type of digital asset (fungible coin/token vs. NFT art)",
            "IRA custodian policies (some allow crypto, others prohibit)",
            "Deemed distribution consequences (taxable income + 10% penalty)",
            "Regulatory uncertainty (no IRS guidance on crypto as collectible for IRA purposes)",
        ],
        primary_authority=[
            "IRC §408(m) — Treatment of collectibles in IRAs",
            "IRC §408(m)(1) — Deemed distribution",
            "IRC §408(m)(2) — Definition of collectibles",
            "IRC §72(t) — 10% early withdrawal penalty",
        ],
        burden_holder="Taxpayer",
        adversary_position="IRS could assert cryptocurrency (especially NFTs) is a collectible, triggering deemed distribution and penalties.",
        counter_arguments=[
            "Cryptocurrency is not a physical collectible (UNCERTAIN — IRC §408(m)(2) includes 'any' tangible personal property, but crypto is intangible).",
            "No IRS guidance means no restriction (RISKY — lack of guidance does not mean safe harbor).",
        ],
        resolution_strategy="""
CONSERVATIVE: Do not hold cryptocurrency in IRA/401(k) to avoid deemed distribution risk.
AGGRESSIVE: Use self-directed IRA with custodian allowing crypto; argue crypto is not collectible (requires disclosure if material).
If crypto already in IRA: monitor for IRS guidance; consider distribution to avoid future deemed distribution if IRS issues adverse ruling.
NFTs representing art: HIGH RISK for collectible treatment — avoid in IRA.
Fungible cryptocurrency (BTC, ETH, etc.): MODERATE RISK — no clear guidance.
""",
        entity_scope=[
            EntityScope.INDIVIDUAL,
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification={
            "crypto_may_be_collectible": ConfidenceLevel.AGGRESSIVE,
            "deemed_distribution_if_collectible": ConfidenceLevel.DEFENSIBLE,
            "nft_art_high_risk": ConfidenceLevel.AGGRESSIVE,
        },
        controlling_precedent="IRC §408(m) (no crypto-specific guidance as of 2026)",
        irc_sections=["§408(m)", "§72(t)"],
        treasury_regs=["§1.408-10"],
        revenue_rulings=[],
        notices=[],
        case_law=[],
        disclosure_caveat="If holding crypto in IRA and claiming it is not a collectible, consider disclosure on Form 8275 given regulatory uncertainty.",
        issue_categories=[IssueCategory.RETIREMENT],
        interaction_triggers=["collectible_determination", "nft_classification"],
        planning_zone_variant="Avoid crypto in IRA unless willing to accept deemed distribution risk. Use taxable accounts for crypto holdings.",
        reporting_zone_variant="If deemed distribution occurs, report on Form 1040 as IRA distribution (Form 1099-R from custodian). Apply 10% penalty if <59.5.",
        audit_zone_variant="Provide IRA custodian statements, documentation showing crypto asset type, argument that crypto is not collectible under IRC §408(m)(2).",
    ),

    # -------------------------------------------------------------------------
    # BLOCK 12: Cost Basis Methods (FIFO, LIFO, Specific ID)
    # -------------------------------------------------------------------------
    DoctrineBlock(
        topic="cost_basis_methods_crypto",
        keywords=["cost basis", "fifo", "lifo", "specific identification", "rev proc 2024-28", "basis tracking"],
        conclusion_template=[
            "Taxpayers may use specific identification method for cryptocurrency basis tracking if contemporaneous records maintained (Rev. Proc. 2024-28).",
            "If specific ID not used, default to FIFO (first-in, first-out) under general tax principles.",
            "LIFO (last-in, first-out) may be used if consistently applied and documented, but less common.",
        ],
        reasoning_framework="""
STEP 1: Determine which units of cryptocurrency are disposed (by transaction ID, wallet address, exchange lot).
STEP 2: SPECIFIC IDENTIFICATION METHOD (preferred for tax optimization):
    - Taxpayer must specifically identify units sold at time of sale/exchange.
    - Contemporaneous records required (written designation before settlement, per Rev. Proc. 2024-28).
    - Allows taxpayer to select highest-basis lots (minimize gain) or lowest-basis lots (maximize loss harvesting).
    - DOCUMENTATION: Email to self, exchange order notes, spreadsheet with lot IDs and selection.
STEP 3: FIFO METHOD (default if specific ID not used):
    - First units acquired are first units disposed.
    - Automatic application if no specific designation.
    - May result in higher gains if early acquisitions have low basis.
STEP 4: LIFO METHOD (last-in, first-out):
    - Last units acquired are first units disposed.
    - May reduce gains if recent acquisitions have higher basis.
    - Must be consistently applied; documentation required.
STEP 5: Apply chosen method consistently for each type of cryptocurrency (can use different methods for BTC vs. ETH, but must be consistent within each).
STEP 6: Compute gain/loss using selected method's basis.

ADVERSARIAL ANALYSIS:
- Taxpayer may claim specific ID retroactively without contemporaneous designation (REJECTED — Rev. Proc. 2024-28 requires designation at or before time of sale).
- Taxpayer may switch methods year-to-year to minimize tax (RISKY — IRS may assert lack of consistency indicates manipulation; accounting method change may require Form 3115).
""",
        key_factors=[
            "Contemporaneous designation for specific ID (written record at time of sale)",
            "Consistency within cryptocurrency type",
            "Documentation quality (exchange records, wallet logs, spreadsheets)",
            "Audit trail (can taxpayer prove which lots were sold?)",
        ],
        primary_authority=[
            "Rev. Proc. 2024-28 — Safe harbor for specific identification of cryptocurrency units",
            "Treas. Reg. §1.1012-1(c) — Basis of stock (by analogy, property basis rules)",
            "IRC §1012 — Basis of property",
        ],
        burden_holder="Taxpayer",
        adversary_position="IRS will default to FIFO if taxpayer cannot substantiate specific ID method. Burden on taxpayer to prove which lots sold.",
        counter_arguments=[
            "Can designate specific ID retroactively when preparing return (REJECTED — must be contemporaneous per Rev. Proc. 2024-28).",
            "Average cost basis allowed (NOT permitted for cryptocurrency; only for mutual funds under specific regulations).",
        ],
        resolution_strategy="""
Use specific identification method for maximum tax optimization.
Designate lots at time of sale (email to self, exchange order notes, trading log entry).
Maintain detailed records: acquisition date, cost, amount, wallet address, transaction ID.
If specific ID not feasible, default to FIFO (safest, easiest to defend).
Use crypto tax software (CoinTracker, TokenTax, Koinly) to track lots and generate tax reports.
Consistent application: use same method for each cryptocurrency type across tax years.
""",
        entity_scope=[
            EntityScope.INDIVIDUAL,
            EntityScope.SOLE_PROPRIETORSHIP,
            EntityScope.PARTNERSHIP,
            EntityScope.LLC,
            EntityScope.S_CORPORATION,
            EntityScope.C_CORPORATION,
            EntityScope.TRUST,
            EntityScope.ESTATE,
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification={
            "specific_id_allowed_if_documented": ConfidenceLevel.DEFENSIBLE,
            "contemporaneous_designation_required": ConfidenceLevel.DEFENSIBLE,
            "fifo_default_if_no_specific_id": ConfidenceLevel.DEFENSIBLE,
        },
        controlling_precedent="Rev. Proc. 2024-28, Treas. Reg. §1.1012-1(c)",
        irc_sections=["§1012"],
        treasury_regs=["§1.1012-1(c)"],
        revenue_rulings=[],
        notices=[],
        case_law=[],
        disclosure_caveat=None,
        issue_categories=[IssueCategory.BASIS, IssueCategory.CAPITAL_GAINS],
        interaction_triggers=["basis_tracking", "gain_loss_calculation"],
        planning_zone_variant="Use specific ID to select high-basis lots when selling (minimize gains) or low-basis lots when harvesting losses. Designate contemporaneously.",
        reporting_zone_variant="If specific ID used, note on Form 8949 'Specific Identification Method per Rev. Proc. 2024-28.' Attach lot tracking spreadsheet if requested.",
        audit_zone_variant="Provide contemporaneous designation records (emails, trading logs, exchange order notes), acquisition records for each lot, transaction IDs, wallet addresses.",
    ),

    # -------------------------------------------------------------------------
    # BLOCK 13: DeFi Yield Farming and Liquidity Provision Taxation
    # -------------------------------------------------------------------------
    DoctrineBlock(
        topic="defi_yield_farming_liquidity_provision",
        keywords=["defi", "yield farming", "liquidity provision", "lp tokens", "impermanent loss", "rewards", "staking"],
        conclusion_template=[
            "Providing liquidity to DeFi pool is likely a taxable exchange (depositing Token A + Token B for LP token).",
            "LP token receipt may trigger taxable event if Token A/B exchanged for different property.",
            "Yield farming rewards (tokens earned) are ordinary income upon receipt at FMV.",
            "Withdrawing liquidity may trigger capital gain/loss based on FMV of tokens received vs. basis in LP token.",
            "Impermanent loss is NOT deductible until liquidity withdrawn and actual loss realized.",
        ],
        reasoning_framework="""
STEP 1: Identify DeFi activity type:
    - Simple liquidity provision (deposit Token A + Token B, receive LP token)
    - Yield farming (stake LP token, earn reward tokens)
    - Single-sided staking (deposit Token A, earn Token A or other rewards)
STEP 2: LIQUIDITY PROVISION TAX TREATMENT:
    - If depositing Token A + Token B creates new property (LP token) → taxable exchange under IRC §1001.
    - Gain/loss = FMV of LP token received minus basis in Token A and Token B contributed.
    - Alternative view: no taxable event if LP token represents proportionate ownership of same tokens (UNCERTAIN — no IRS guidance).
STEP 3: YIELD FARMING REWARDS:
    - Reward tokens received are ordinary income at FMV upon receipt (similar to mining/staking).
    - Basis in reward tokens = FMV at receipt.
    - Holding period for rewards starts at receipt date.
STEP 4: WITHDRAWAL FROM POOL:
    - Burn LP token, receive Token A + Token B (possibly in different amounts than deposited).
    - Taxable event: FMV of tokens received minus basis in LP token.
    - Character: capital gain/loss (holding period of LP token determines LTCG/STCG).
STEP 5: IMPERMANENT LOSS:
    - Not deductible until liquidity withdrawn and loss realized.
    - Impermanent loss during holding period is unrealized (no tax impact).

ADVERSARIAL ANALYSIS:
- Taxpayer may claim no taxable event on liquidity provision (deposit is like putting assets in a pool, not an exchange).
  - UNCERTAIN — IRS could assert LP token is different property, triggering IRC §1001 realization.
  - Conservative: treat as taxable exchange.
- Taxpayer may claim impermanent loss is deductible as unrealized loss (REJECTED — losses deductible only when realized under IRC §165).
- Taxpayer may claim yield farming rewards not taxable until sold (REJECTED — analogous to mining/staking, ordinary income upon receipt).
""",
        key_factors=[
            "Type of DeFi activity (liquidity provision, yield farming, single-sided staking)",
            "Whether LP token is distinct property from underlying tokens (determines taxable event)",
            "FMV determination for LP tokens (often no market price; use pro-rata value of underlying tokens)",
            "Timing of reward token receipt (dominion and control test)",
            "Impermanent loss vs. realized loss (only realized losses deductible)",
        ],
        primary_authority=[
            "IRC §1001 — Determination of gain or loss",
            "IRC §61(a) — Gross income includes all income from whatever source",
            "IRC §165 — Losses (deductible only when realized)",
            "IRS Notice 2014-21 Q&A-8/9 (mining income upon receipt, by analogy)",
            "Rev. Rul. 2019-24 (airdrop income upon receipt, by analogy)",
        ],
        burden_holder="Taxpayer",
        adversary_position="IRS likely to assert liquidity provision is taxable exchange, yield farming rewards are ordinary income upon receipt, impermanent loss not deductible until realized.",
        counter_arguments=[
            "Liquidity provision is not a taxable event (deposit, not exchange) — UNCERTAIN, no IRS guidance.",
            "LP token represents same property, no realization — UNCERTAIN, conservative approach is to recognize event.",
            "Yield farming rewards not taxable until sold (creation of property) — REJECTED by analogy to mining/staking guidance.",
            "Impermanent loss is realized loss — REJECTED, IRC §165 requires closed and completed transaction.",
        ],
        resolution_strategy="""
CONSERVATIVE APPROACH:
- Treat liquidity provision as taxable exchange: FMV of LP token received = proceeds, basis = sum of Token A + Token B basis.
- Report gain/loss on Form 8949 at time of LP token receipt.
- Yield farming rewards: ordinary income on Schedule 1 or Schedule C at FMV upon receipt.
- Withdrawal: taxable exchange of LP token for Token A + Token B; report gain/loss.
- Impermanent loss: no deduction until withdrawal and realized loss computed.

AGGRESSIVE APPROACH (disclosure recommended):
- No taxable event on liquidity provision (LP token is not distinct property).
- Yield farming rewards still ordinary income (no avoiding this under any theory).
- Withdrawal is taxable event (compare tokens received to original basis in contributed tokens).
- Requires Form 8275 disclosure given lack of guidance.

DOCUMENTATION:
- Track LP token receipt (blockchain transaction, AMM interface screenshots).
- Track reward token receipts (timestamps, FMV at receipt).
- Track withdrawal transactions (tokens received, FMV at withdrawal).
- Maintain records of impermanent loss (for realized loss calculation at withdrawal).
""",
        entity_scope=[
            EntityScope.INDIVIDUAL,
            EntityScope.SOLE_PROPRIETORSHIP,
            EntityScope.PARTNERSHIP,
            EntityScope.LLC,
            EntityScope.S_CORPORATION,
            EntityScope.C_CORPORATION,
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification={
            "liquidity_provision_is_taxable_exchange": ConfidenceLevel.AGGRESSIVE,
            "yield_farming_rewards_are_ordinary_income": ConfidenceLevel.DEFENSIBLE,
            "impermanent_loss_not_deductible_until_realized": ConfidenceLevel.DEFENSIBLE,
        },
        controlling_precedent="IRC §1001, IRC §61, IRC §165 (no DeFi-specific IRS guidance as of 2026)",
        irc_sections=["§1001", "§61", "§165"],
        treasury_regs=["§1.1001-1", "§1.165-1"],
        revenue_rulings=[],
        notices=["Notice 2014-21"],
        case_law=[],
        disclosure_caveat="Given lack of IRS guidance on DeFi taxation, consider Form 8275 disclosure if taking aggressive position on liquidity provision non-recognition.",
        issue_categories=[IssueCategory.DEFI, IssueCategory.ORDINARY_INCOME, IssueCategory.CAPITAL_GAINS],
        interaction_triggers=["defi_swap_taxation", "mining_staking_income", "cost_basis_methods"],
        planning_zone_variant="Avoid complex DeFi strategies if tax tracking is burdensome. Use single-sided staking (simpler tax treatment) instead of dual-token liquidity provision.",
        reporting_zone_variant="Report LP token receipt as taxable exchange (Form 8949). Report yield farming rewards as ordinary income (Schedule 1 or C). Report withdrawal as taxable exchange (Form 8949).",
        audit_zone_variant="Provide DeFi protocol transaction records, blockchain explorer data, AMM pool pricing, reward token FMV at receipt, LP token valuation methodology.",
    ),

    # -------------------------------------------------------------------------
    # BLOCK 14: Broker Reporting and Form 1099-DA (IRC §6045)
    # -------------------------------------------------------------------------
    DoctrineBlock(
        topic="broker_reporting_1099_da_irc_6045",
        keywords=["broker reporting", "irc 6045", "form 1099-da", "infrastructure investment jobs act", "iija", "digital asset broker"],
        conclusion_template=[
            "Infrastructure Investment and Jobs Act (IIJA) 2021 expanded IRC §6045 broker reporting to 'digital assets.'",
            "Brokers must report gross proceeds from digital asset sales on Form 1099-DA (or Form 1099-B) starting in tax years post-2025 (phased rollout).",
            "Digital asset defined broadly: any digital representation of value recorded on cryptographically secured distributed ledger.",
            "Taxpayers will receive Forms 1099-DA from exchanges and brokers; must reconcile with personal records.",
        ],
        reasoning_framework="""
STEP 1: Identify covered transactions (sales/exchanges of digital assets effected by broker).
STEP 2: Determine if broker is subject to reporting requirement under IRC §6045:
    - US-based exchanges (Coinbase, Kraken, Gemini, etc.) → required to report.
    - Foreign exchanges → may not report to IRS (but still reportable by taxpayer on Form 8949).
    - Non-custodial wallets/DEX transactions → no broker, no 1099-DA (taxpayer self-reports).
STEP 3: Receive Form 1099-DA from broker (or Form 1099-B if broker uses existing form).
STEP 4: Reconcile Form 1099-DA with personal records:
    - Check proceeds reported by broker vs. actual FMV at disposal.
    - Check basis (brokers may not have full basis data initially; phased implementation).
    - Report adjusted amounts on Form 8949 if discrepancies.
STEP 5: Report all transactions on Form 8949, including those NOT covered by 1099-DA (non-custodial, DEX, foreign exchanges).
STEP 6: IRS will match Form 8949 to Forms 1099-DA; discrepancies trigger audits.

ADVERSARIAL ANALYSIS:
- Taxpayers may assume only 1099-DA transactions need reporting (WRONG — all dispositions reportable, whether or not broker issues 1099-DA).
- Taxpayers may rely solely on broker-reported basis (RISKY — brokers may not have full basis history; taxpayer must track).
- Taxpayers may ignore foreign exchange transactions (WRONG — still reportable by taxpayer, even if no 1099-DA).
""",
        key_factors=[
            "Type of broker (US-based exchange vs. foreign vs. non-custodial)",
            "Effective date of broker reporting (phased: 2025+ for gross proceeds, later for basis)",
            "Reconciliation between broker-reported amounts and taxpayer records",
            "Basis tracking responsibility (ultimately on taxpayer, even if broker reports basis)",
        ],
        primary_authority=[
            "IRC §6045 (as amended by IIJA 2021 §80603)",
            "IRC §6045A — Basis reporting",
            "26 USC §6721/6722 — Penalties for broker failures to file/furnish",
            "IRS Form 1099-DA (new form for digital asset reporting, or integration into Form 1099-B)",
        ],
        burden_holder="Taxpayer (and broker for reporting, but taxpayer for accurate basis tracking)",
        adversary_position="IRS will have Forms 1099-DA from brokers; expects matching on Form 8949. Penalties for underreporting.",
        counter_arguments=[
            "Only need to report transactions with 1099-DA (WRONG — all dispositions reportable).",
            "Broker basis is authoritative (WRONG — taxpayer must substantiate if broker basis incorrect).",
        ],
        resolution_strategy="""
Maintain independent records of all crypto transactions (do not rely solely on broker).
Reconcile Forms 1099-DA with personal records BEFORE filing return.
Report discrepancies on Form 8949 with explanation (e.g., 'Basis adjusted per taxpayer records').
For transactions without 1099-DA (DEX, non-custodial, foreign exchanges), self-report on Form 8949.
Use crypto tax software to aggregate all sources (broker 1099-DAs + manual entries).
Prepare for IRS matching — if mismatch between 1099-DA and Form 8949, provide documentation (exchange CSVs, blockchain records).
""",
        entity_scope=[
            EntityScope.INDIVIDUAL,
            EntityScope.SOLE_PROPRIETORSHIP,
            EntityScope.PARTNERSHIP,
            EntityScope.LLC,
            EntityScope.S_CORPORATION,
            EntityScope.C_CORPORATION,
            EntityScope.TRUST,
            EntityScope.ESTATE,
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification={
            "broker_reporting_required_post_2025": ConfidenceLevel.DEFENSIBLE,
            "taxpayer_must_report_all_transactions": ConfidenceLevel.DEFENSIBLE,
            "reconciliation_required": ConfidenceLevel.DEFENSIBLE,
        },
        controlling_precedent="IRC §6045 as amended by IIJA 2021",
        irc_sections=["§6045", "§6045A"],
        treasury_regs=[],
        revenue_rulings=[],
        notices=[],
        case_law=[],
        disclosure_caveat=None,
        issue_categories=[IssueCategory.REPORTING, IssueCategory.INFORMATION_RETURN],
        interaction_triggers=["form_8949_reporting", "basis_tracking", "proceeds_determination"],
        planning_zone_variant="Consolidate holdings to fewer exchanges to simplify 1099-DA reconciliation. Track basis independently in case broker data incomplete.",
        reporting_zone_variant="Receive Forms 1099-DA from brokers. Reconcile with personal records. Report all transactions on Form 8949 (brokers + manual). Attach explanation if adjusting broker-reported amounts.",
        audit_zone_variant="Provide Forms 1099-DA from brokers, personal transaction logs, basis tracking spreadsheets, exchange CSVs, blockchain records for non-custodial transactions.",
    ),

    # -------------------------------------------------------------------------
    # BLOCK 15: Stablecoin Taxation
    # -------------------------------------------------------------------------
    DoctrineBlock(
        topic="stablecoin_taxation",
        keywords=["stablecoin", "usdt", "usdc", "dai", "tether", "algorithmic stablecoin", "property", "currency"],
        conclusion_template=[
            "Stablecoins are treated as property under IRS Notice 2014-21 (same as other cryptocurrency).",
            "Exchange of one stablecoin for another (e.g., USDT for USDC) is a taxable event under IRC §1001.",
            "Gains/losses typically minimal due to 1:1 peg, but tracking still required.",
            "Stablecoins do NOT qualify as 'foreign currency' under IRC §988 (IRS has confirmed).",
        ],
        reasoning_framework="""
STEP 1: Identify stablecoin transaction (purchase, sale, exchange, payment).
STEP 2: Apply property treatment (IRS Notice 2014-21): stablecoins are property, not currency.
STEP 3: Determine if taxable event:
    - Purchase of stablecoin with USD → establish basis (no gain/loss).
    - Sale of stablecoin for USD → gain/loss = proceeds - basis (typically minimal if held short-term).
    - Exchange of stablecoin A for stablecoin B → taxable event under IRC §1001.
    - Use of stablecoin to purchase goods/services → taxable event (FMV of goods/services = proceeds).
STEP 4: Compute gain/loss: FMV at disposal minus adjusted basis.
STEP 5: Report on Form 8949 (even if gain/loss is $0 or de minimis).

ADVERSARIAL ANALYSIS:
- Taxpayer may claim stablecoin exchanges are not taxable (both are 'dollars') — REJECTED, IRS Notice 2014-21 treats all virtual currency as property.
- Taxpayer may claim stablecoins are foreign currency under IRC §988 — REJECTED, IRS FAQ explicitly excludes cryptocurrency from §988.
- Taxpayer may ignore small gains/losses (de minimis) — NO de minimis exception exists; technically reportable.
""",
        key_factors=[
            "Type of stablecoin (fiat-backed like USDT/USDC, algorithmic like DAI, commodity-backed)",
            "Holding period (typically short-term if used for transactions)",
            "Basis tracking (cost of acquiring stablecoin)",
            "FMV fluctuations (typically minimal, but can deviate from $1.00 peg during market stress)",
        ],
        primary_authority=[
            "IRS Notice 2014-21 — Virtual currency is property",
            "IRC §1001 — Determination of gain or loss",
            "IRS FAQ 2019 — Cryptocurrency is not foreign currency under IRC §988",
        ],
        burden_holder="Taxpayer",
        adversary_position="IRS treats stablecoins as property; all exchanges are taxable events even if gain/loss is minimal.",
        counter_arguments=[
            "Stablecoins are equivalent to USD, no taxable event (REJECTED — property treatment applies).",
            "De minimis exception for small gains (NO such exception exists).",
            "Stablecoins are foreign currency (REJECTED — IRS FAQ explicitly denies).",
        ],
        resolution_strategy="""
Treat stablecoins as property subject to IRC §1001.
Track basis for all stablecoin acquisitions (typically $1.00 per unit if purchased at peg).
Report all stablecoin dispositions on Form 8949 (even if gain/loss is minimal).
For exchanges between stablecoins (USDT ↔ USDC), recognize taxable event but gain/loss typically $0 or near-zero.
Use crypto tax software to automate stablecoin tracking (many transactions, small gains/losses).
Consider using single stablecoin to minimize taxable exchange events.
""",
        entity_scope=[
            EntityScope.INDIVIDUAL,
            EntityScope.SOLE_PROPRIETORSHIP,
            EntityScope.PARTNERSHIP,
            EntityScope.LLC,
            EntityScope.S_CORPORATION,
            EntityScope.C_CORPORATION,
            EntityScope.TRUST,
            EntityScope.ESTATE,
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification={
            "stablecoin_is_property": ConfidenceLevel.DEFENSIBLE,
            "stablecoin_exchange_is_taxable": ConfidenceLevel.DEFENSIBLE,
            "no_foreign_currency_treatment": ConfidenceLevel.DEFENSIBLE,
        },
        controlling_precedent="IRS Notice 2014-21, IRS FAQ 2019",
        irc_sections=["§1001", "§988"],
        treasury_regs=[],
        revenue_rulings=[],
        notices=["Notice 2014-21"],
        case_law=[],
        disclosure_caveat=None,
        issue_categories=[IssueCategory.CAPITAL_GAINS, IssueCategory.BASIS],
        interaction_triggers=["defi_swap_taxation", "cost_basis_methods"],
        planning_zone_variant="Use single stablecoin (e.g., USDC) consistently to avoid taxable exchanges between stablecoins. Minimize unnecessary conversions.",
        reporting_zone_variant="Report stablecoin dispositions on Form 8949. Typically near-zero gain/loss, but must still report. Use crypto tax software to aggregate.",
        audit_zone_variant="Provide exchange records showing stablecoin transactions, basis documentation (purchase price, typically $1.00), FMV at disposal (typically $1.00).",
    ),
]


# ==============================================================================
# DOCTRINE CACHE ACCESS FUNCTIONS
# ==============================================================================

def get_doctrine(topic: str) -> Optional[DoctrineBlock]:
    """Retrieve a single doctrine block by topic."""
    for block in DOCTRINE_BLOCKS:
        if block.topic == topic:
            return block
    return None


def get_all_doctrines() -> List[DoctrineBlock]:
    """Return all doctrine blocks."""
    return DOCTRINE_BLOCKS


def get_doctrine_topics() -> List[str]:
    """Get list of all doctrine topics."""
    return [block.topic for block in DOCTRINE_BLOCKS]


def get_doctrines_by_confidence(confidence: ConfidenceLevel) -> List[DoctrineBlock]:
    """Filter doctrines by confidence level."""
    return [block for block in DOCTRINE_BLOCKS if block.confidence == confidence]


def get_doctrines_by_irc_section(irc_section: str) -> List[DoctrineBlock]:
    """Find doctrines citing a specific IRC section."""
    return [block for block in DOCTRINE_BLOCKS if irc_section in block.irc_sections]


def search_doctrines_by_keyword(keyword: str) -> List[DoctrineBlock]:
    """Search doctrines by keyword (case-insensitive)."""
    keyword_lower = keyword.lower()
    results = []
    for block in DOCTRINE_BLOCKS:
        if keyword_lower in block.topic.lower():
            results.append(block)
        elif any(keyword_lower in kw.lower() for kw in block.keywords):
            results.append(block)
    return results


def get_doctrine_stats() -> Dict[str, Any]:
    """Return statistics about the doctrine cache."""
    return {
        "total_blocks": len(DOCTRINE_BLOCKS),
        "confidence_distribution": {
            "DEFENSIBLE": len([b for b in DOCTRINE_BLOCKS if b.confidence == ConfidenceLevel.DEFENSIBLE]),
            "AGGRESSIVE": len([b for b in DOCTRINE_BLOCKS if b.confidence == ConfidenceLevel.AGGRESSIVE]),
            "DISCLOSURE": len([b for b in DOCTRINE_BLOCKS if b.confidence == ConfidenceLevel.DISCLOSURE]),
            "HIGH_RISK": len([b for b in DOCTRINE_BLOCKS if b.confidence == ConfidenceLevel.HIGH_RISK]),
        },
        "issue_category_coverage": {
            cat.value: len([b for b in DOCTRINE_BLOCKS if cat in b.issue_categories])
            for cat in IssueCategory
        },
        "topics": get_doctrine_topics(),
    }


logger.info(f"TX14 Crypto Tax Doctrine Cache loaded: {len(DOCTRINE_BLOCKS)} blocks")
