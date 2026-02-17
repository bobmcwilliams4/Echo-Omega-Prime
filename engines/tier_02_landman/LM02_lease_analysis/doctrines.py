"""
LM02 Lease Analysis Engine - Doctrine Cache
Texas Oil and Gas Lease Doctrines for the Permian Basin

Pre-compiled reasoning blocks for instant lease analysis covering:
    - Habendum clause (primary/secondary term)
    - Drilling and delay rental clauses
    - Royalty and overriding royalty provisions
    - Pooling and unitization clauses
    - Pugh clause analysis (vertical, horizontal, depth)
    - Shut-in royalty provisions
    - Force majeure clauses
    - Continuous development obligations
    - Surface use rights and accommodation doctrine
    - Depth limitations and retained acreage
    - Top lease provisions
    - Preferential rights and ROFR
    - Assignment and sublease provisions
    - Mother Hubbard clause
    - Surrender clause
    - Texas-specific statutory framework

Author: ECHO OMEGA PRIME
Authority: 11.0 SOVEREIGN
Version: 1.0.0
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from loguru import logger

# ============================================================================
# DOCTRINE CACHE METADATA
# ============================================================================

DOCTRINE_CACHE_VERSION = "1.0.0"
DOCTRINE_CACHE_BUILD_DATE = "2026-02-10"
DOCTRINE_CACHE_HASH = ""  # Computed at load time


class DoctrineCategory(str, Enum):
    """Categories of lease doctrines."""
    HABENDUM = "habendum"
    DRILLING = "drilling"
    DELAY_RENTAL = "delay_rental"
    ROYALTY = "royalty"
    OVERRIDING_ROYALTY = "overriding_royalty"
    POOLING = "pooling"
    UNITIZATION = "unitization"
    PUGH_CLAUSE = "pugh_clause"
    SHUT_IN = "shut_in"
    FORCE_MAJEURE = "force_majeure"
    CONTINUOUS_DEVELOPMENT = "continuous_development"
    SURFACE_USE = "surface_use"
    DEPTH_LIMITATION = "depth_limitation"
    RETAINED_ACREAGE = "retained_acreage"
    TOP_LEASE = "top_lease"
    PREFERENTIAL_RIGHT = "preferential_right"
    ASSIGNMENT = "assignment"
    MOTHER_HUBBARD = "mother_hubbard"
    SURRENDER = "surrender"
    HBP_STATUS = "hbp_status"
    NRI_CALCULATION = "nri_calculation"
    TEXAS_STATUTORY = "texas_statutory"


class LeaseTermType(str, Enum):
    """Types of lease terms."""
    PRIMARY = "primary"
    SECONDARY = "secondary"
    EXTENDED = "extended"
    HELD_BY_PRODUCTION = "held_by_production"
    CONTINUOUS_OPERATIONS = "continuous_operations"
    SHUT_IN = "shut_in"
    FORCE_MAJEURE = "force_majeure"
    EXPIRED = "expired"
    TERMINATED = "terminated"


class RoyaltyType(str, Enum):
    """Types of royalty interests."""
    LANDOWNER_ROYALTY = "landowner_royalty"
    OVERRIDING_ROYALTY = "overriding_royalty"
    PRODUCTION_PAYMENT = "production_payment"
    NET_PROFITS_INTEREST = "net_profits_interest"
    CARRIED_INTEREST = "carried_interest"


class PoolingType(str, Enum):
    """Types of pooling authority."""
    VOLUNTARY = "voluntary"
    FORCED = "forced"
    COMMUNITY_LEASE = "community_lease"
    FIELDWIDE_UNIT = "fieldwide_unit"


class PughClauseType(str, Enum):
    """Types of Pugh clause provisions."""
    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"
    DEPTH = "depth"
    COMBINED = "combined"


class ClauseRiskLevel(str, Enum):
    """Risk assessment for lease clauses."""
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


# ============================================================================
# DOCTRINE BLOCK STRUCTURE
# ============================================================================

@dataclass
class LeaseDoctrineBlock:
    """A single pre-compiled reasoning block for lease analysis."""
    key: str
    category: DoctrineCategory
    title: str
    summary: str
    legal_basis: str
    texas_authority: str
    analysis_template: str
    risk_factors: List[str]
    best_practices: List[str]
    common_pitfalls: List[str]
    related_doctrines: List[str]
    keywords: List[str]
    permian_specific: bool = False
    statutory_references: List[str] = field(default_factory=list)
    case_law_references: List[str] = field(default_factory=list)
    version: str = "1.0.0"
    created: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "key": self.key,
            "category": self.category.value,
            "title": self.title,
            "summary": self.summary,
            "legal_basis": self.legal_basis,
            "texas_authority": self.texas_authority,
            "analysis_template": self.analysis_template,
            "risk_factors": self.risk_factors,
            "best_practices": self.best_practices,
            "common_pitfalls": self.common_pitfalls,
            "related_doctrines": self.related_doctrines,
            "keywords": self.keywords,
            "permian_specific": self.permian_specific,
            "statutory_references": self.statutory_references,
            "case_law_references": self.case_law_references,
            "version": self.version,
            "created": self.created,
        }

    def compute_hash(self) -> str:
        """Compute SHA-256 hash of doctrine content for integrity verification."""
        content = json.dumps(self.to_dict(), sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()


# ============================================================================
# DOCTRINE CACHE - 50+ BLOCKS
# ============================================================================

DOCTRINE_CACHE: Dict[str, LeaseDoctrineBlock] = {}


def _register(block: LeaseDoctrineBlock) -> None:
    """Register a doctrine block into the cache."""
    DOCTRINE_CACHE[block.key] = block


# ─────────────────────────────────────────────────────────────────────────────
# HABENDUM CLAUSE DOCTRINES
# ─────────────────────────────────────────────────────────────────────────────

_register(LeaseDoctrineBlock(
    key="habendum_primary_term",
    category=DoctrineCategory.HABENDUM,
    title="Habendum Clause - Primary Term",
    summary=(
        "The habendum clause defines the duration of the lease grant. The primary term is the "
        "fixed period during which the lessee has the right to explore and develop without any "
        "obligation to produce. Standard Permian Basin primary terms range from 3 to 5 years, "
        "though some older leases carry 10-year terms. The lease automatically terminates at the "
        "end of the primary term unless held by production, continuous operations, shut-in royalty "
        "payments, or other saving clauses."
    ),
    legal_basis=(
        "Texas common law recognizes the habendum clause as the granting clause that defines "
        "the estate conveyed. The primary term is a determinable fee — the estate exists for "
        "the stated period and continues thereafter only upon the occurrence of stated conditions."
    ),
    texas_authority="Tex. Nat. Res. Code Ann. § 91.001 et seq.",
    analysis_template=(
        "1. Identify the primary term start date (lease effective date or recording date)\n"
        "2. Determine the primary term duration (typically 3 or 5 years)\n"
        "3. Calculate the primary term expiration date\n"
        "4. Check for extension provisions (paid-up lease, continuous operations clause)\n"
        "5. Identify all saving clauses that can extend beyond primary term\n"
        "6. Determine current lease status: active primary term, HBP, expired, or saved"
    ),
    risk_factors=[
        "Short primary term with no extension option",
        "Ambiguous commencement date language",
        "Missing or vague saving clause provisions",
        "Discrepancy between lease date and recording date",
        "Primary term expiration during permitting delays",
    ],
    best_practices=[
        "Always confirm primary term start date from the granting clause, not the execution date",
        "Calendar all key dates: primary term end, delay rental due dates, option periods",
        "Review all saving clauses in conjunction with habendum",
        "For horizontal wells, confirm that spud date vs completion date governs",
        "Track RRC permit applications as evidence of operations",
    ],
    common_pitfalls=[
        "Assuming lease date equals effective date",
        "Failing to account for leap years in term calculations",
        "Overlooking cessation-of-production clauses after HBP",
        "Not distinguishing between 'commence operations' vs 'commence drilling'",
        "Missing top lease that takes effect upon expiration",
    ],
    related_doctrines=["habendum_secondary_term", "hbp_status", "continuous_operations", "shut_in_royalty"],
    keywords=["habendum", "primary term", "lease term", "granting clause", "determinable fee"],
    permian_specific=True,
    statutory_references=["Tex. Nat. Res. Code § 91.001", "Tex. Prop. Code § 5.001"],
    case_law_references=[
        "Hydrocarbon Mgmt. v. Tracker Exploration, 861 S.W.2d 427 (Tex. App. 1993)",
        "Anadarko Petroleum v. Thompson, 94 S.W.3d 550 (Tex. 2002)",
    ],
))

_register(LeaseDoctrineBlock(
    key="habendum_secondary_term",
    category=DoctrineCategory.HABENDUM,
    title="Habendum Clause - Secondary Term",
    summary=(
        "The secondary term extends the lease beyond the primary term for 'as long thereafter "
        "as oil, gas, or other minerals are produced' or 'as long as operations continue.' "
        "The secondary term is indefinite in duration but conditional — it persists only so long "
        "as the specified condition (typically production) continues. Any cessation of the "
        "qualifying activity triggers the 60-day or 90-day cessation clause, after which the "
        "lease may automatically terminate if operations are not resumed."
    ),
    legal_basis=(
        "The secondary term creates a determinable fee subject to a special limitation. Upon "
        "cessation of the qualifying condition, the estate automatically reverts to the lessor "
        "without need for judicial action, unless a savings clause applies."
    ),
    texas_authority="Tex. Nat. Res. Code Ann. § 91.001; common law determinable fee",
    analysis_template=(
        "1. Confirm transition from primary to secondary term occurred properly\n"
        "2. Identify the specific condition maintaining the secondary term\n"
        "3. Review cessation-of-production clause and grace period\n"
        "4. Check for temporary cessation doctrine applicability\n"
        "5. Verify continuous operations clause if applicable\n"
        "6. Assess whether shut-in provisions can save the lease\n"
        "7. Determine if Pugh clause limits acreage held in secondary term"
    ),
    risk_factors=[
        "Gap in production without cessation clause protection",
        "Mechanical failure causing unexpected production stoppage",
        "Market conditions making continued production uneconomical",
        "Regulatory shutdown (environmental, safety) during secondary term",
        "Lease language requiring production 'in paying quantities'",
    ],
    best_practices=[
        "Monitor production reports monthly for any gaps",
        "Document all maintenance shutdowns with operator records",
        "Keep delay rental payments current as insurance during marginal production",
        "Review 'paying quantities' standard under Clifton v. Koontz",
        "Maintain communication with operator regarding planned workovers",
    ],
    common_pitfalls=[
        "Assuming any production holds the entire lease when Pugh clause limits acreage",
        "Failing to invoke cessation clause within the grace period",
        "Not distinguishing between 'produced' and 'capable of producing'",
        "Overlooking that de minimis production may not constitute 'paying quantities'",
    ],
    related_doctrines=["habendum_primary_term", "hbp_status", "cessation_of_production", "pugh_vertical"],
    keywords=["secondary term", "thereafter", "so long as produced", "determinable fee", "special limitation"],
    permian_specific=False,
    statutory_references=["Tex. Nat. Res. Code § 91.001"],
    case_law_references=[
        "Clifton v. Koontz, 325 S.W.2d 684 (Tex. 1959)",
        "Rogers v. Osborn, 152 Tex. 540, 261 S.W.2d 311 (1953)",
        "Skelly Oil Co. v. Archer County, 356 S.W.2d 774 (Tex. 1961)",
    ],
))

_register(LeaseDoctrineBlock(
    key="hbp_status",
    category=DoctrineCategory.HBP_STATUS,
    title="Held by Production (HBP) Analysis",
    summary=(
        "A lease is Held by Production when it has transitioned from the primary term to the "
        "secondary term by virtue of actual production of oil, gas, or other minerals in paying "
        "quantities. Under Texas law, 'paying quantities' means production sufficient to yield "
        "a profit to the lessee over operating costs, even if small, judged over a reasonable "
        "time period. The test is whether a reasonably prudent operator would continue to "
        "operate the well for profit, not merely to hold the lease."
    ),
    legal_basis=(
        "The paying quantities test was established in Clifton v. Koontz and refined in "
        "subsequent decisions. It is an objective test based on economics, not the subjective "
        "intent of the operator."
    ),
    texas_authority="Clifton v. Koontz, 325 S.W.2d 684 (Tex. 1959)",
    analysis_template=(
        "1. Confirm that production commenced during or before the end of the primary term\n"
        "2. Verify production is of oil, gas, or other minerals covered by the lease\n"
        "3. Apply paying quantities test:\n"
        "   a. Calculate gross revenue from production over reasonable period (6-12 months)\n"
        "   b. Deduct direct operating costs (lifting, treating, transport)\n"
        "   c. Determine if net revenue is positive\n"
        "   d. Consider whether a prudent operator would continue operations\n"
        "4. Check if Pugh clause limits HBP to specific tracts or depths\n"
        "5. Verify production reports with RRC or operator\n"
        "6. Assess any production gaps under cessation-of-production clause"
    ),
    risk_factors=[
        "Marginal wells producing at or near the paying quantities threshold",
        "Seasonal fluctuations in commodity prices affecting paying quantities analysis",
        "Operator intentionally maintaining minimal production to hold lease",
        "Production from pooled unit where leased acreage is a small fraction",
        "Multiple formations — production from one zone may not hold all depths",
    ],
    best_practices=[
        "Obtain monthly production data from RRC public records or operator",
        "Run paying quantities analysis quarterly using 12-month rolling average",
        "Document commodity prices used in paying quantities calculation",
        "If marginal, consider requesting operator to release non-producing acreage",
        "Track all wells on lease — abandonment of last producing well terminates HBP",
    ],
    common_pitfalls=[
        "Assuming any production, however minimal, constitutes paying quantities",
        "Not accounting for all operating costs in paying quantities analysis",
        "Overlooking that production from a pooled unit may hold only the pooled acreage",
        "Failing to distinguish between gross production and paying quantities",
    ],
    related_doctrines=["habendum_secondary_term", "cessation_of_production", "pugh_vertical", "royalty_calculation"],
    keywords=["HBP", "held by production", "paying quantities", "prudent operator", "Clifton v. Koontz"],
    permian_specific=True,
    statutory_references=["Tex. Nat. Res. Code § 91.001"],
    case_law_references=[
        "Clifton v. Koontz, 325 S.W.2d 684 (Tex. 1959)",
        "Garcia v. King, 164 S.W.2d 509 (Tex. 1942)",
        "Hydrocarbon Mgmt. v. Tracker, 861 S.W.2d 427 (Tex. App. 1993)",
    ],
))

# ─────────────────────────────────────────────────────────────────────────────
# DRILLING AND DELAY RENTAL DOCTRINES
# ─────────────────────────────────────────────────────────────────────────────

_register(LeaseDoctrineBlock(
    key="drilling_clause",
    category=DoctrineCategory.DRILLING,
    title="Drilling Clause - Commencement of Operations",
    summary=(
        "The drilling clause defines what constitutes the beginning of drilling operations "
        "sufficient to satisfy lease obligations or extend the primary term. Modern Permian "
        "Basin leases typically require actual spudding of a well, not merely preparatory "
        "activities. Some leases use broader language such as 'commence operations' which may "
        "include building access roads, constructing the pad, or moving equipment onto the lease. "
        "The distinction is critical when the primary term is about to expire."
    ),
    legal_basis=(
        "Under Texas law, the phrase 'commence drilling' requires actual drilling, while "
        "'commence operations' may be satisfied by preparatory activities done in good faith "
        "with intent to drill. The lessee must act as a reasonably prudent operator."
    ),
    texas_authority="Tex. Nat. Res. Code § 91.001; common law reasonably prudent operator standard",
    analysis_template=(
        "1. Identify the specific drilling obligation language in the lease\n"
        "2. Distinguish between 'commence drilling' vs 'commence operations' vs 'spud'\n"
        "3. Determine the deadline for commencement (end of primary term or earlier)\n"
        "4. Verify what activities qualify under the specific lease language\n"
        "5. Check for continuous drilling obligation after commencement\n"
        "6. Assess whether preparatory activities satisfy the clause\n"
        "7. Review any depth commitment associated with drilling obligation"
    ),
    risk_factors=[
        "Narrow drilling clause requiring actual spud vs broader operations language",
        "Permitting delays preventing timely commencement",
        "Equipment or contractor unavailability near term expiration",
        "Ambiguous definition of 'operations' in older lease forms",
        "Weather or environmental conditions preventing access to location",
    ],
    best_practices=[
        "Begin permitting and site preparation well before deadline",
        "Document all preparatory activities with dates and photographs",
        "Obtain RRC drilling permit as evidence of intent to drill",
        "Coordinate with operator on specific timeline and milestones",
        "If commencement is marginal, request affidavit from operator",
    ],
    common_pitfalls=[
        "Relying on preparatory activities when lease requires actual spud",
        "Assuming drilling permit alone constitutes commencement",
        "Not documenting the chain of operations leading to spud",
        "Overlooking that completion of the well may also be required",
    ],
    related_doctrines=["delay_rental_unless", "habendum_primary_term", "continuous_development"],
    keywords=["drilling clause", "commence operations", "spud", "drilling obligation", "commencement"],
    permian_specific=True,
    statutory_references=["Tex. Nat. Res. Code § 89.001"],
    case_law_references=[
        "Riddle v. Bolin, 342 S.W.2d 192 (Tex. Civ. App. 1961)",
        "Shell Oil Co. v. Goodroe, 197 S.W.2d 395 (Tex. Civ. App. 1946)",
    ],
))

_register(LeaseDoctrineBlock(
    key="delay_rental_unless",
    category=DoctrineCategory.DELAY_RENTAL,
    title="Delay Rental - Unless Clause",
    summary=(
        "The 'unless' lease is the modern standard in Texas. Under the unless clause, the lease "
        "automatically terminates if delay rentals are not paid by the anniversary date, unless "
        "drilling operations have commenced. No notice or demand is required — failure to pay "
        "creates an automatic forfeiture. The unless clause is a special limitation, not a "
        "condition subsequent, meaning the lessor need not take any action to reclaim the lease. "
        "Most modern Permian Basin leases are paid-up leases where the bonus includes all "
        "delay rentals, eliminating this risk."
    ),
    legal_basis=(
        "The unless clause creates a determinable fee in the lessee. The estate automatically "
        "terminates upon failure to pay delay rental by the due date. Unlike an 'or' clause, "
        "no action by the lessor is required to terminate the lease."
    ),
    texas_authority="Tex. Prop. Code § 5.001; common law determinable fee",
    analysis_template=(
        "1. Determine whether the lease contains an 'unless' or 'or' clause\n"
        "2. If unless clause, identify the delay rental amount and due date\n"
        "3. Verify all rental payments were made timely\n"
        "4. Check for paid-up lease provision that eliminates rental obligations\n"
        "5. If rental was missed, confirm automatic termination\n"
        "6. Check for any equitable relief provisions in the lease\n"
        "7. Verify correct payee — assignment may change the rental obligee"
    ),
    risk_factors=[
        "Missed delay rental payment causing automatic lease termination",
        "Payment sent to wrong party after lease assignment",
        "Incorrect rental amount after partial release of acreage",
        "Banking errors or postal delays causing late payment",
        "Failure to account for leap year in anniversary date calculation",
    ],
    best_practices=[
        "Set up automatic payment reminders 30 and 60 days before due date",
        "Confirm payee identity before each payment (check for assignments)",
        "Send payments via certified mail or wire with confirmation",
        "Maintain copies of all rental payment receipts and confirmations",
        "If doubt about paid-up status, pay the rental as insurance",
    ],
    common_pitfalls=[
        "Confusing 'unless' clause with 'or' clause — different consequences",
        "Assuming grace period exists when none is stated in the lease",
        "Sending payment to original lessor after mineral conveyance to new owner",
        "Not adjusting rental amount after partial surrender of acreage",
    ],
    related_doctrines=["delay_rental_or", "habendum_primary_term", "drilling_clause"],
    keywords=["delay rental", "unless clause", "paid-up lease", "automatic termination", "anniversary date"],
    permian_specific=True,
    statutory_references=["Tex. Prop. Code § 5.001"],
    case_law_references=[
        "Sword v. Rains, 575 F.2d 810 (10th Cir. 1978)",
        "Sun Oil Co. v. Burns, 125 Tex. 549, 84 S.W.2d 442 (1935)",
    ],
))

_register(LeaseDoctrineBlock(
    key="delay_rental_or",
    category=DoctrineCategory.DELAY_RENTAL,
    title="Delay Rental - Or Clause",
    summary=(
        "The 'or' lease gives the lessee a choice: either pay delay rental or commence drilling "
        "operations. Failure to do either does not automatically terminate the lease; instead, "
        "it creates a breach of covenant that gives the lessor a cause of action for damages or "
        "forfeiture. The lessor must take affirmative action (typically filing suit) to terminate "
        "the lease. This is the older form, now rarely used in the Permian Basin, but still "
        "found in legacy leases that remain HBP from prior decades."
    ),
    legal_basis=(
        "The or clause creates a covenant, not a special limitation. Breach gives the lessor "
        "a right of action but does not automatically terminate the estate. The lessor must "
        "pursue equitable relief to cancel the lease."
    ),
    texas_authority="Common law covenant analysis; equity jurisdiction",
    analysis_template=(
        "1. Confirm the lease uses 'or' language rather than 'unless'\n"
        "2. Identify the rental amount and payment schedule\n"
        "3. Determine if any rentals were missed\n"
        "4. If missed, assess whether lessor took action to terminate\n"
        "5. Check for waiver or estoppel by lessor accepting late payments\n"
        "6. Determine current status: active, breached-but-not-terminated, or judicially cancelled"
    ),
    risk_factors=[
        "Ambiguous language that could be construed as either 'or' or 'unless'",
        "Lessor accepting late payments creating waiver argument",
        "Long period between breach and lessor action — laches defense",
        "Lessee reliance on the lease during breach period — estoppel",
    ],
    best_practices=[
        "Treat 'or' clause leases with same urgency as 'unless' clause leases",
        "Document any late payments and lessor's response",
        "Obtain written confirmation from lessor acknowledging payment acceptance",
        "If uncertain about clause type, consult the full lease text",
    ],
    common_pitfalls=[
        "Assuming an 'or' lease automatically terminates like an 'unless' lease",
        "Lessor failing to act promptly after breach, creating waiver issues",
        "Not recognizing that some courts construe ambiguous language as 'unless'",
    ],
    related_doctrines=["delay_rental_unless", "habendum_primary_term"],
    keywords=["or clause", "covenant", "breach", "forfeiture", "equitable relief"],
    permian_specific=False,
    statutory_references=[],
    case_law_references=[
        "Magnolia Petroleum Co. v. Connellee, 11 S.W.2d 158 (Tex. Comm'n App. 1928)",
    ],
))

# ─────────────────────────────────────────────────────────────────────────────
# ROYALTY DOCTRINES
# ─────────────────────────────────────────────────────────────────────────────

_register(LeaseDoctrineBlock(
    key="royalty_calculation",
    category=DoctrineCategory.ROYALTY,
    title="Royalty Calculation - Landowner Royalty",
    summary=(
        "The landowner royalty is the lessor's share of production, free of the costs of "
        "production. Under Texas law, the royalty is a cost-free interest — the lessor bears "
        "no share of drilling, completing, equipping, or operating costs. The standard royalty "
        "has evolved from 1/8 (12.5%) historically to 1/4 (25%) as the modern Permian Basin "
        "standard. The royalty is calculated on the market value of production at the wellhead, "
        "unless the lease specifies a different valuation point (such as 'at the well' vs "
        "'amount realized' vs 'market value at the point of sale')."
    ),
    legal_basis=(
        "Texas Supreme Court in Heritage Resources v. NationsBank held that the royalty owner "
        "bears a proportionate share of post-production costs unless the lease provides otherwise. "
        "However, many modern leases contain 'no deduction' or 'cost-free' royalty clauses that "
        "shift all post-production costs to the lessee."
    ),
    texas_authority="Heritage Resources v. NationsBank, 939 S.W.2d 118 (Tex. 1996)",
    analysis_template=(
        "1. Identify the royalty fraction stated in the lease\n"
        "2. Determine the valuation point: wellhead, point of sale, or market value\n"
        "3. Check for cost-free or no-deduction language\n"
        "4. Identify allowable deductions (if any): severance tax, gathering, transport, processing\n"
        "5. Calculate gross royalty: Production Volume x Price x Royalty Fraction\n"
        "6. Apply permitted deductions to arrive at net royalty\n"
        "7. If pooled, apply unit participation factor\n"
        "8. Verify royalty payments against division order"
    ),
    risk_factors=[
        "Ambiguous valuation language leading to disputes over deductions",
        "Operator deducting post-production costs from royalty without authority",
        "Price manipulation through affiliate transactions",
        "Commingling production from multiple leases with different royalty rates",
        "Gas vs oil royalty calculation differences (BTU adjustment, shrinkage)",
    ],
    best_practices=[
        "Obtain and review the division order for each producing well",
        "Compare royalty payments to RRC production reports monthly",
        "Track commodity prices to verify operator is using fair market value",
        "Audit post-production deductions annually",
        "For gas, verify BTU adjustment and shrinkage calculations",
    ],
    common_pitfalls=[
        "Assuming 'market value at the well' means no deductions",
        "Not distinguishing between oil royalty and gas royalty calculations",
        "Overlooking NGL extraction royalties in gas processing",
        "Failing to account for pooling participation factor in royalty calculation",
    ],
    related_doctrines=["overriding_royalty", "nri_calculation", "pooling_voluntary", "royalty_gas_specific"],
    keywords=["royalty", "royalty fraction", "cost-free", "market value", "Heritage Resources"],
    permian_specific=True,
    statutory_references=["Tex. Nat. Res. Code § 91.402"],
    case_law_references=[
        "Heritage Resources v. NationsBank, 939 S.W.2d 118 (Tex. 1996)",
        "Burlington Resources Oil & Gas v. Texas Crude Energy, 573 S.W.3d 198 (Tex. 2019)",
    ],
))

_register(LeaseDoctrineBlock(
    key="royalty_gas_specific",
    category=DoctrineCategory.ROYALTY,
    title="Royalty - Gas-Specific Calculation",
    summary=(
        "Gas royalty calculation differs from oil royalty in several critical ways. Gas is often "
        "sold at a point downstream from the wellhead after gathering, compression, processing, "
        "and transportation. The question of which costs are deductible from royalty depends on "
        "the lease language. Under the 'market value at the well' standard, the lessor receives "
        "the value of gas at the wellhead, which means post-production costs incurred to move "
        "gas to the market may be deductible. Gas processing yields NGLs (natural gas liquids) "
        "which have separate value — the royalty owner's share of NGLs is often a significant "
        "portion of total gas royalties in the Permian Basin."
    ),
    legal_basis=(
        "Under Heritage Resources, post-production costs are deductible unless the lease "
        "provides otherwise. For gas, this includes gathering, compression, dehydration, "
        "transportation, and processing costs."
    ),
    texas_authority="Heritage Resources v. NationsBank, 939 S.W.2d 118 (Tex. 1996)",
    analysis_template=(
        "1. Identify gas royalty clause — is it market value at well, proceeds, or amount realized?\n"
        "2. Determine if gas is sold at the wellhead or downstream\n"
        "3. Identify all post-production costs: gathering, compression, dehydration, transport, processing\n"
        "4. Check for 'no deduction' language specific to gas\n"
        "5. Calculate residue gas royalty after processing\n"
        "6. Calculate NGL royalty (separate stream)\n"
        "7. Apply BTU adjustment if applicable\n"
        "8. Account for gas shrinkage during processing\n"
        "9. Verify against division order and check stubs"
    ),
    risk_factors=[
        "Excessive gathering and transportation deductions eroding gas royalty",
        "NGL royalty not being paid or being paid at below-market prices",
        "Gas shrinkage not properly accounted for in royalty calculation",
        "Affiliate transactions between operator and midstream company",
        "Flared or vented gas not generating any royalty",
    ],
    best_practices=[
        "Review gas purchase agreement to understand pricing structure",
        "Track NGL component prices separately (ethane, propane, butane, condensate)",
        "Verify gas metering volumes against RRC production reports",
        "Audit midstream deductions against actual cost data",
        "Monitor flaring reports — excessive flaring reduces royalty revenue",
    ],
    common_pitfalls=[
        "Treating gas royalty the same as oil royalty",
        "Not claiming NGL royalties separately from residue gas",
        "Accepting division order gas price without verifying index",
        "Overlooking BTU value differences between raw and processed gas",
    ],
    related_doctrines=["royalty_calculation", "nri_calculation", "overriding_royalty"],
    keywords=["gas royalty", "NGL", "gathering", "compression", "processing", "shrinkage", "BTU"],
    permian_specific=True,
    statutory_references=["Tex. Nat. Res. Code § 91.402"],
    case_law_references=[
        "Heritage Resources v. NationsBank, 939 S.W.2d 118 (Tex. 1996)",
        "Burlington Resources Oil & Gas v. Texas Crude Energy, 573 S.W.3d 198 (Tex. 2019)",
    ],
))

_register(LeaseDoctrineBlock(
    key="overriding_royalty",
    category=DoctrineCategory.OVERRIDING_ROYALTY,
    title="Overriding Royalty Interest (ORRI)",
    summary=(
        "An overriding royalty interest (ORRI) is a non-operating, non-cost-bearing interest "
        "carved from the lessee's working interest. Unlike the landowner royalty which is part "
        "of the mineral estate, the ORRI is created by the lessee and terminates when the "
        "underlying lease terminates. ORRIs are commonly reserved by landmen, geologists, "
        "assignors, and promoters. In the Permian Basin, typical ORRIs range from 1% to 5% "
        "of 8/8ths. The ORRI reduces the lessee's net revenue interest proportionally."
    ),
    legal_basis=(
        "An ORRI is a property interest created by reservation or grant from the working interest. "
        "It runs with the lease and binds subsequent assignees. It terminates coextensively "
        "with the underlying lease."
    ),
    texas_authority="Tex. Nat. Res. Code § 91.001; common law conveyancing principles",
    analysis_template=(
        "1. Identify all ORRI reservations in the chain of assignments\n"
        "2. Calculate total ORRI burden on the working interest\n"
        "3. Verify that total burdens (royalty + ORRI) do not exceed 100%\n"
        "4. Determine whether ORRI survives pooling and unitization\n"
        "5. Check for proportionate reduction clauses affecting ORRI\n"
        "6. Assess impact of ORRI on lessee's NRI and economics\n"
        "7. Verify ORRI is properly recorded and reflected in division orders"
    ),
    risk_factors=[
        "Excessive ORRI burden making well uneconomical for operator",
        "ORRI not properly recorded or reflected in division orders",
        "ORRI termination upon lease expiration — re-leasing eliminates ORRI",
        "Dispute over whether ORRI applies to all depths or specific zones",
        "Proportionate reduction clause reducing ORRI when lease covers less than full interest",
    ],
    best_practices=[
        "Track all ORRI reservations in the assignment chain",
        "Ensure total burdens are clearly stated in each assignment",
        "Record ORRI reservations promptly in county records",
        "Include anti-washout language if ORRI should survive re-leasing",
        "Verify ORRI payment on each well's division order",
    ],
    common_pitfalls=[
        "Failing to account for cumulative ORRIs across multiple assignments",
        "Assuming ORRI survives lease termination and re-leasing",
        "Not including anti-washout provision in ORRI reservation",
        "Overlooking proportionate reduction in partial interest scenarios",
    ],
    related_doctrines=["royalty_calculation", "nri_calculation", "assignment_sublease"],
    keywords=["ORRI", "overriding royalty", "non-cost-bearing", "carved interest", "anti-washout"],
    permian_specific=True,
    statutory_references=["Tex. Nat. Res. Code § 91.001"],
    case_law_references=[
        "HECI Exploration Co. v. Neel, 982 S.W.2d 881 (Tex. 1998)",
    ],
))

# ─────────────────────────────────────────────────────────────────────────────
# POOLING AND UNITIZATION DOCTRINES
# ─────────────────────────────────────────────────────────────────────────────

_register(LeaseDoctrineBlock(
    key="pooling_voluntary",
    category=DoctrineCategory.POOLING,
    title="Pooling - Voluntary Pooling Authority",
    summary=(
        "Voluntary pooling is the combining of two or more tracts or mineral interests into a "
        "single drilling or production unit by agreement of the parties. The pooling clause in "
        "the lease grants the lessee authority to pool the leased acreage with other lands. "
        "Texas does not have compulsory pooling (forced pooling) for oil wells, making the "
        "lease pooling clause critical. The pooling declaration must be recorded and typically "
        "specifies the unit name, participating tracts, acreage, and effective date. Production "
        "anywhere on the pooled unit is deemed production on each tract within the unit."
    ),
    legal_basis=(
        "Pooling authority derives from the lease contract. Texas does not have compulsory "
        "pooling for oil, only for gas under limited circumstances (Tex. Nat. Res. Code Ch. 102). "
        "The scope of the pooling authority is strictly construed — the lessee may only pool "
        "within the parameters set by the lease."
    ),
    texas_authority="Tex. Nat. Res. Code §§ 102.001-102.051 (gas only); lease contract",
    analysis_template=(
        "1. Identify the pooling clause in the lease\n"
        "2. Determine the maximum unit size permitted by the pooling clause\n"
        "3. Check for unit size limitations by formation or well type (vertical vs horizontal)\n"
        "4. Review the pooling declaration for compliance with lease terms\n"
        "5. Verify the leased acreage's participation percentage in the pooled unit\n"
        "6. Assess whether the pooled unit is of a reasonable size\n"
        "7. Determine the effect of pooling on royalty calculation\n"
        "8. Check for Pugh clause limiting the effect of pooling on unpooled acreage"
    ),
    risk_factors=[
        "Pooling clause granting excessive authority to lessee (no size limit)",
        "Dilution of royalty through large pooled units",
        "Pooling of only a portion of the lease without Pugh clause protection",
        "Operator pooling acreage to hold the lease rather than for legitimate development",
        "Cross-unit well allocation disputes",
    ],
    best_practices=[
        "Include unit size limitations in the pooling clause",
        "Require Pugh clause to release unpooled acreage",
        "Review all pooling declarations for compliance with lease terms",
        "Calculate the royalty impact of pooling before signing",
        "Verify the participation factor in the division order",
    ],
    common_pitfalls=[
        "Assuming pooling automatically holds the entire lease — Pugh clause may limit",
        "Not reviewing the pooling declaration for compliance with lease terms",
        "Overlooking that horizontal wells may require larger units than vertical wells",
        "Failing to verify that the pooled unit is properly filed with RRC",
    ],
    related_doctrines=["pugh_vertical", "pugh_horizontal", "unitization", "nri_calculation"],
    keywords=["pooling", "pooled unit", "drilling unit", "participation factor", "voluntary pooling"],
    permian_specific=True,
    statutory_references=["Tex. Nat. Res. Code § 102.001"],
    case_law_references=[
        "Jones v. Killingsworth, 403 S.W.2d 325 (Tex. 1965)",
        "Browning Oil Co. v. Luecke, 38 S.W.3d 625 (Tex. App. 2000)",
    ],
))

_register(LeaseDoctrineBlock(
    key="unitization",
    category=DoctrineCategory.UNITIZATION,
    title="Unitization - Fieldwide and Enhanced Recovery Units",
    summary=(
        "Unitization combines multiple leases and tracts into a single operating unit, typically "
        "for secondary or enhanced recovery operations (waterflood, CO2 flood, polymer injection). "
        "Unlike pooling (which is for drilling units), unitization covers an entire field or "
        "reservoir. In Texas, unitization requires consent of at least 65% of the working interest "
        "and 65% of the royalty interest within the proposed unit area. The unit operating "
        "agreement allocates costs and production among the working interest owners based on "
        "a participation formula, typically based on surface acreage or hydrocarbon pore volume."
    ),
    legal_basis=(
        "Texas Mineral Interest Pooling Act (Tex. Nat. Res. Code Ch. 102) allows forced "
        "pooling for gas wells only. Fieldwide unitization in Texas is voluntary and requires "
        "contractual consent of the requisite percentages."
    ),
    texas_authority="Tex. Nat. Res. Code §§ 101.001-101.101; 102.001-102.051",
    analysis_template=(
        "1. Determine the type of unit: drilling unit, production unit, or enhanced recovery unit\n"
        "2. Review the unit operating agreement terms\n"
        "3. Verify consent percentages were met (65% WI + 65% RI for voluntary)\n"
        "4. Identify the participation formula (acreage, pore volume, etc.)\n"
        "5. Calculate the leased tract's participation factor\n"
        "6. Assess the impact on royalty and NRI\n"
        "7. Review cost allocation provisions\n"
        "8. Check for tract reversion rights if unit is dissolved"
    ),
    risk_factors=[
        "Participation formula undervaluing the leased acreage",
        "High unit operating costs reducing net revenue",
        "Unit dissolution leaving acreage without lease protection",
        "Operator controlled unit decisions favoring working interest over royalty",
    ],
    best_practices=[
        "Review the unit operating agreement before consenting",
        "Verify participation formula methodology",
        "Ensure unit agreement preserves all lease rights",
        "Monitor unit accounting statements regularly",
    ],
    common_pitfalls=[
        "Confusing pooling with unitization — different legal concepts",
        "Assuming unit production holds all leases within the unit",
        "Not reviewing the unit operating agreement cost allocation",
    ],
    related_doctrines=["pooling_voluntary", "nri_calculation", "royalty_calculation"],
    keywords=["unitization", "unit", "enhanced recovery", "waterflood", "CO2 flood", "participation formula"],
    permian_specific=True,
    statutory_references=["Tex. Nat. Res. Code § 101.001", "Tex. Nat. Res. Code § 102.001"],
    case_law_references=[
        "Railroad Commission of Texas v. Manziel, 361 S.W.2d 560 (Tex. 1962)",
    ],
))

# ─────────────────────────────────────────────────────────────────────────────
# PUGH CLAUSE DOCTRINES
# ─────────────────────────────────────────────────────────────────────────────

_register(LeaseDoctrineBlock(
    key="pugh_vertical",
    category=DoctrineCategory.PUGH_CLAUSE,
    title="Pugh Clause - Vertical (Surface) Pugh",
    summary=(
        "The vertical Pugh clause (also called a surface Pugh or freestone rider) provides "
        "that production from a pooled unit holds only the acreage actually included in the "
        "pooled unit, releasing all acreage outside the unit at the end of the primary term. "
        "Without a Pugh clause, production from a pooled unit is treated as production from "
        "the entire lease, holding all acreage regardless of whether it is included in the "
        "unit. The Pugh clause is one of the most important lessor protections in modern "
        "Permian Basin leases where large tracts may have only a small portion pooled."
    ),
    legal_basis=(
        "The Pugh clause modifies the common law rule that production anywhere on the lease "
        "holds the entire lease. Named after Lawrence Pugh, a Louisiana legislator who first "
        "introduced the concept in Louisiana statute form. In Texas, it exists purely as a "
        "contractual provision in the lease."
    ),
    texas_authority="Contractual provision; no statutory basis in Texas",
    analysis_template=(
        "1. Identify whether the lease contains a Pugh clause\n"
        "2. Determine the scope: does it apply to pooled units only, or all non-producing acreage?\n"
        "3. Identify the trigger date: end of primary term, or specific anniversary\n"
        "4. Calculate acreage released vs acreage retained\n"
        "5. Determine if released acreage reverts to lessor immediately or with notice\n"
        "6. Check for continuous development obligations on released acreage\n"
        "7. Assess impact on lease economics and development plans\n"
        "8. Verify that pooling declarations are consistent with Pugh clause terms"
    ),
    risk_factors=[
        "Missing Pugh clause allowing small pooled unit to hold entire large lease",
        "Ambiguous Pugh clause language creating uncertainty about released acreage",
        "Operator pooling acreage shortly before primary term expires to circumvent Pugh",
        "Pugh clause that does not address horizontal wells spanning multiple tracts",
    ],
    best_practices=[
        "Always include a Pugh clause in leases covering more than one drilling unit",
        "Specify that Pugh clause applies to both pooled and unpooled non-producing acreage",
        "Define 'retained acreage' clearly — producing unit + reasonable buffer",
        "Include anti-dilution provision preventing operator from creating oversized units",
        "Address horizontal wells that may cross unit boundaries",
    ],
    common_pitfalls=[
        "Assuming Pugh clause exists when it does not — verify the actual lease text",
        "Not accounting for horizontal wells that straddle multiple pooled units",
        "Overlooking that some Pugh clauses release acreage only at specific anniversary dates",
        "Failing to file release of lease for Pugh-released acreage in county records",
    ],
    related_doctrines=["pugh_horizontal", "pugh_depth", "pooling_voluntary", "retained_acreage"],
    keywords=["Pugh clause", "vertical Pugh", "freestone rider", "released acreage", "retained acreage"],
    permian_specific=True,
    statutory_references=[],
    case_law_references=[
        "Jones v. Killingsworth, 403 S.W.2d 325 (Tex. 1965)",
    ],
))

_register(LeaseDoctrineBlock(
    key="pugh_horizontal",
    category=DoctrineCategory.PUGH_CLAUSE,
    title="Pugh Clause - Horizontal Pugh",
    summary=(
        "The horizontal Pugh clause (also called a depth Pugh) releases all depths not currently "
        "being produced or included in a pooled unit at the end of the primary term. This "
        "prevents a shallow well from holding all depths to the center of the earth. In the "
        "Permian Basin, where stacked pay zones (Spraberry, Wolfcamp, Bone Spring, etc.) are "
        "common, the horizontal Pugh clause is critical for ensuring that deep rights are not "
        "locked up by shallow production. The released depths become available for a new lease "
        "or a deeper drilling obligation."
    ),
    legal_basis=(
        "The horizontal Pugh clause is a contractual modification of the common law rule that "
        "an oil and gas lease covers all depths. Texas courts have upheld depth limitation and "
        "depth severance provisions as valid contractual terms."
    ),
    texas_authority="Contractual provision; Tex. Nat. Res. Code § 91.001",
    analysis_template=(
        "1. Determine whether the lease contains a horizontal/depth Pugh clause\n"
        "2. Identify the depth reference: formation top, specific footage, or producing zone\n"
        "3. Determine which depths are retained by current production\n"
        "4. Calculate the depth interval released at the end of the primary term\n"
        "5. Identify target formations within the released depths\n"
        "6. Assess the commercial value of released depth intervals\n"
        "7. Check for continuous drilling obligations to retain deeper rights\n"
        "8. Determine if released depths are available for a new lease"
    ),
    risk_factors=[
        "Missing depth Pugh allowing shallow well to hold all stacked pay zones",
        "Vague depth reference creating disputes over which zones are released",
        "Operator completing well in multiple zones to circumvent depth Pugh",
        "Released depths may have different mineral owners than retained depths",
    ],
    best_practices=[
        "Define depth retention by formation name AND measured depth",
        "Include a depth buffer (e.g., 100 feet below deepest perforation) for retained zone",
        "Require separate pooling declaration for each depth interval",
        "Address dual lateral and stacked lateral completions in the Pugh clause",
    ],
    common_pitfalls=[
        "Using only footage without formation reference — formations vary across the lease",
        "Not accounting for deviated or horizontal wellbores that cross depth boundaries",
        "Failing to file depth release in county records after Pugh clause triggers",
    ],
    related_doctrines=["pugh_vertical", "depth_limitation", "retained_acreage"],
    keywords=["horizontal Pugh", "depth Pugh", "stacked pay", "depth severance", "deep rights"],
    permian_specific=True,
    statutory_references=["Tex. Nat. Res. Code § 91.001"],
    case_law_references=[
        "French v. Chevron U.S.A., 896 S.W.2d 795 (Tex. App. 1995)",
    ],
))

_register(LeaseDoctrineBlock(
    key="pugh_depth",
    category=DoctrineCategory.PUGH_CLAUSE,
    title="Pugh Clause - Combined Depth and Surface Pugh",
    summary=(
        "A combined Pugh clause releases both unpooled surface acreage AND non-producing depths "
        "at the end of the primary term. This is the most comprehensive form of Pugh protection "
        "and is the modern standard in sophisticated Permian Basin leases. The combined Pugh "
        "effectively creates a three-dimensional release: the lessee retains only the acreage "
        "within a producing unit AND only the depths being produced within that unit. All other "
        "surface acreage and all other depths revert to the lessor. This prevents the common "
        "practice of holding large tracts with minimal shallow production."
    ),
    legal_basis="Contractual provision combining vertical and horizontal Pugh concepts.",
    texas_authority="Contractual provision; no direct statutory authority",
    analysis_template=(
        "1. Confirm the lease contains both vertical and horizontal Pugh provisions\n"
        "2. Map the three-dimensional retained volume: surface acreage x depth interval\n"
        "3. Calculate the released surface acreage (outside producing units)\n"
        "4. Calculate the released depth intervals (below/above producing zones)\n"
        "5. Identify the commercial value of all released dimensions\n"
        "6. Determine if any continuous development obligations preserve released rights\n"
        "7. Check for anti-washout or renewal provisions on released rights\n"
        "8. Generate a 3D map of retained vs released rights"
    ),
    risk_factors=[
        "Complex interaction between surface and depth Pugh provisions",
        "Dispute over the exact boundary between retained and released depths",
        "Operator completing in multiple zones to maximize retention",
        "Multiple horizontal wells spanning different tracts and depths",
    ],
    best_practices=[
        "Use specific formation names and footage references for depth boundaries",
        "Include clear language that each producing unit retains only the pooled acreage",
        "Require separate designation for each producing zone/unit combination",
        "Include a reasonableness standard for unit size relative to formation",
    ],
    common_pitfalls=[
        "Assuming vertical Pugh alone provides sufficient protection",
        "Not generating a visual map of retained vs released rights",
        "Failing to coordinate Pugh releases across multiple leases from same lessor",
    ],
    related_doctrines=["pugh_vertical", "pugh_horizontal", "depth_limitation", "retained_acreage"],
    keywords=["combined Pugh", "3D release", "surface and depth", "stacked pay protection"],
    permian_specific=True,
    statutory_references=[],
    case_law_references=[],
))

# ─────────────────────────────────────────────────────────────────────────────
# SHUT-IN, FORCE MAJEURE, CONTINUOUS DEVELOPMENT
# ─────────────────────────────────────────────────────────────────────────────

_register(LeaseDoctrineBlock(
    key="shut_in_royalty",
    category=DoctrineCategory.SHUT_IN,
    title="Shut-In Royalty Provisions",
    summary=(
        "The shut-in royalty clause allows the lessee to maintain the lease by making periodic "
        "payments when a well is capable of producing but is shut in (not producing). A well "
        "may be shut in due to lack of pipeline connection, market conditions, regulatory "
        "requirements, or operational reasons. The shut-in payment is typically $1 to $25 per "
        "net mineral acre per year. The lease usually limits the shut-in period to 1-3 years. "
        "If the well is not returned to production or a new well drilled within the shut-in "
        "period, the lease terminates. The well must be genuinely capable of production — a "
        "dry hole or depleted well cannot support shut-in payments."
    ),
    legal_basis=(
        "Shut-in royalty provisions are contractual exceptions to the requirement of actual "
        "production. Texas courts construe them strictly — the well must be capable of "
        "production in commercial quantities."
    ),
    texas_authority="Tex. Nat. Res. Code § 91.001; lease contract terms",
    analysis_template=(
        "1. Verify the lease contains a shut-in royalty clause\n"
        "2. Determine the shut-in payment amount and due date\n"
        "3. Confirm the well is capable of producing in paying quantities\n"
        "4. Identify the maximum shut-in period permitted\n"
        "5. Calculate elapsed shut-in time and remaining period\n"
        "6. Verify timely payment of shut-in royalties\n"
        "7. Determine if other wells on the lease are producing (shut-in may be moot)\n"
        "8. Assess the reason for shut-in and likelihood of resuming production"
    ),
    risk_factors=[
        "Shut-in period expiring without return to production",
        "Well not genuinely capable of production — shut-in payments invalid",
        "Operator using shut-in to hold lease without intent to develop",
        "Shut-in royalty payment not made timely — lease terminates",
    ],
    best_practices=[
        "Calendar shut-in payment due dates and maximum shut-in period end date",
        "Obtain operator certification that well is capable of production",
        "Monitor RRC status reports for shut-in wells",
        "If shut-in approaches maximum period, demand operator commit to development plan",
    ],
    common_pitfalls=[
        "Assuming shut-in payment alone keeps lease alive indefinitely",
        "Not verifying that the well is actually capable of production",
        "Failing to track the cumulative shut-in period across multiple episodes",
    ],
    related_doctrines=["hbp_status", "habendum_secondary_term", "force_majeure"],
    keywords=["shut-in", "shut-in royalty", "capable of producing", "shut-in payment"],
    permian_specific=True,
    statutory_references=["Tex. Nat. Res. Code § 91.001"],
    case_law_references=[
        "Freeman v. Magnolia Petroleum Co., 171 S.W.2d 339 (Tex. 1943)",
        "Hydrocarbon Mgmt. v. Tracker Exploration, 861 S.W.2d 427 (Tex. App. 1993)",
    ],
))

_register(LeaseDoctrineBlock(
    key="force_majeure",
    category=DoctrineCategory.FORCE_MAJEURE,
    title="Force Majeure Clause",
    summary=(
        "The force majeure clause excuses the lessee's performance obligations during events "
        "beyond the lessee's reasonable control. Common force majeure events include acts of "
        "God, war, government regulation, labor disputes, equipment failure, pandemic, "
        "environmental orders, pipeline capacity limitations, and adverse market conditions. "
        "The clause typically requires the lessee to give notice within a specified period "
        "(often 30 days) and to resume operations promptly when the event ceases. Force "
        "majeure suspends but does not extend the primary term in most modern leases, unless "
        "the lease specifically provides for term extension."
    ),
    legal_basis=(
        "Force majeure clauses are contractual allocations of risk. Texas courts enforce them "
        "according to their terms but construe them narrowly. The party invoking force majeure "
        "bears the burden of proving the event qualifies and that it used reasonable diligence "
        "to overcome the obstacle."
    ),
    texas_authority="Common law contract interpretation; UCC § 2-615 by analogy",
    analysis_template=(
        "1. Identify the force majeure clause in the lease\n"
        "2. Determine what events qualify as force majeure\n"
        "3. Assess whether the claimed event falls within the enumerated categories\n"
        "4. Check for notice requirements and verify compliance\n"
        "5. Determine the maximum suspension period\n"
        "6. Assess whether the event actually prevented performance (causation)\n"
        "7. Verify that the lessee used reasonable diligence to overcome the obstacle\n"
        "8. Determine the effect on the lease term: suspension vs extension"
    ),
    risk_factors=[
        "Force majeure clause too narrow — claimed event not covered",
        "Failure to give timely notice as required by the clause",
        "Operator invoking force majeure for economic reasons when clause excludes market conditions",
        "Dispute over whether the event actually prevented (vs merely hindered) operations",
    ],
    best_practices=[
        "Review force majeure clause carefully for enumerated vs general catch-all events",
        "Give notice promptly upon occurrence of qualifying event",
        "Document the causal connection between the event and inability to perform",
        "Resume operations as soon as reasonably practicable after event ceases",
    ],
    common_pitfalls=[
        "Assuming force majeure excuses all lease obligations — it typically only excuses operations",
        "Not giving timely notice as required by the specific lease terms",
        "Invoking force majeure for economic hardship when clause covers only physical events",
        "Assuming force majeure automatically extends the primary term",
    ],
    related_doctrines=["habendum_primary_term", "drilling_clause", "continuous_development"],
    keywords=["force majeure", "act of God", "impossibility", "impracticability", "excuse"],
    permian_specific=False,
    statutory_references=[],
    case_law_references=[
        "Sun Operating v. Holt, 984 S.W.2d 277 (Tex. App. 1998)",
    ],
))

_register(LeaseDoctrineBlock(
    key="continuous_development",
    category=DoctrineCategory.CONTINUOUS_DEVELOPMENT,
    title="Continuous Development Obligation",
    summary=(
        "The continuous development clause (also called a continuous drilling clause) requires "
        "the lessee to maintain an ongoing drilling program to hold the lease after the primary "
        "term. Typically, the lessee must commence a new well within 90 to 180 days after "
        "completing the previous well. If the lessee fails to maintain continuous development, "
        "the lease terminates as to acreage not held by production. This clause is particularly "
        "important in the Permian Basin where large sections may require multiple wells across "
        "different formations to fully develop the leased acreage."
    ),
    legal_basis=(
        "Continuous development clauses are contractual provisions that modify the implied "
        "covenant to develop. They create specific, objective standards for development that "
        "replace the more subjective 'reasonably prudent operator' standard."
    ),
    texas_authority="Contractual provision; implied covenant of reasonable development",
    analysis_template=(
        "1. Identify the continuous development clause\n"
        "2. Determine the gap period allowed between wells (e.g., 90, 120, 180 days)\n"
        "3. Track all well completions and spud dates on the lease\n"
        "4. Calculate the current gap since last well completion\n"
        "5. Determine if the gap has exceeded the permitted period\n"
        "6. Identify acreage at risk of release if gap is exceeded\n"
        "7. Check for force majeure tolling of the gap period\n"
        "8. Assess the operator's development plan going forward"
    ),
    risk_factors=[
        "Equipment or crew unavailability causing gap in development",
        "Regulatory delays (permit approval) extending gap period",
        "Operator choosing not to develop marginal acreage",
        "Dispute over what constitutes 'completion' vs 'commencement' of a well",
    ],
    best_practices=[
        "Track all well spud and completion dates in a development calendar",
        "Coordinate with operator on development schedule well in advance",
        "Include reasonable gap periods (120-180 days) to account for logistics",
        "Define 'operations' broadly to include permitting, site prep, and spud",
    ],
    common_pitfalls=[
        "Not tracking the continuous development timeline",
        "Assuming completion of one well holds the entire lease forever",
        "Failing to account for force majeure tolling provisions",
    ],
    related_doctrines=["drilling_clause", "pugh_vertical", "retained_acreage", "force_majeure"],
    keywords=["continuous development", "continuous drilling", "development obligation", "gap period"],
    permian_specific=True,
    statutory_references=["Tex. Nat. Res. Code § 91.001"],
    case_law_references=[
        "Amoco Prod. Co. v. Alexander, 622 S.W.2d 563 (Tex. 1981)",
    ],
))

_register(LeaseDoctrineBlock(
    key="cessation_of_production",
    category=DoctrineCategory.HBP_STATUS,
    title="Cessation of Production - Temporary Cessation Doctrine",
    summary=(
        "The temporary cessation of production doctrine provides that a brief, good-faith "
        "interruption in production does not automatically terminate a lease held by production "
        "in the secondary term. Texas courts recognize that production may be temporarily "
        "interrupted for operational reasons (workover, equipment repair, pipeline maintenance) "
        "without forfeiting the lease, provided the cessation is temporary, in good faith, and "
        "the lessee resumes operations within a reasonable time. Many modern leases codify this "
        "with a specific cessation clause granting 60-90 days to resume production."
    ),
    legal_basis=(
        "The temporary cessation doctrine is a judicial gloss on the habendum clause, "
        "recognizing that strict literal interpretation would lead to inequitable results "
        "when production is temporarily interrupted for legitimate reasons."
    ),
    texas_authority="Watson v. Rochmill, 137 Tex. 565, 155 S.W.2d 783 (1941)",
    analysis_template=(
        "1. Determine the date production ceased\n"
        "2. Identify the cause of cessation\n"
        "3. Assess whether the cause is legitimate (operational, regulatory, market)\n"
        "4. Calculate the duration of the cessation\n"
        "5. Check for a specific cessation clause in the lease and its grace period\n"
        "6. If no specific clause, apply the common law temporary cessation doctrine\n"
        "7. Determine if the lessee acted with reasonable diligence to resume\n"
        "8. Assess whether the lease has terminated or remains viable"
    ),
    risk_factors=[
        "Extended cessation beyond the reasonable period",
        "Cessation caused by operator abandoning the well",
        "Lease language that strictly requires continuous production without cessation clause",
        "Multiple cessation events suggesting permanent decline",
    ],
    best_practices=[
        "Include a specific cessation clause with defined grace period (60-90 days)",
        "Document the cause of every production interruption",
        "Resume operations promptly and document the timeline",
        "Monitor production reports for unexpected gaps",
    ],
    common_pitfalls=[
        "Assuming any brief cessation terminates the lease",
        "Failing to invoke the cessation clause within the grace period",
        "Not documenting the good-faith effort to resume production",
    ],
    related_doctrines=["hbp_status", "habendum_secondary_term", "shut_in_royalty"],
    keywords=["cessation", "temporary cessation", "production interruption", "grace period"],
    permian_specific=False,
    statutory_references=[],
    case_law_references=[
        "Watson v. Rochmill, 137 Tex. 565, 155 S.W.2d 783 (1941)",
        "Midwest Oil Corp. v. Winsauer, 323 S.W.2d 944 (Tex. 1959)",
    ],
))

# ─────────────────────────────────────────────────────────────────────────────
# SURFACE USE AND DEPTH LIMITATION DOCTRINES
# ─────────────────────────────────────────────────────────────────────────────

_register(LeaseDoctrineBlock(
    key="surface_use_rights",
    category=DoctrineCategory.SURFACE_USE,
    title="Surface Use Rights and Accommodation Doctrine",
    summary=(
        "The mineral estate is dominant over the surface estate in Texas — the mineral owner "
        "(and by extension, the lessee) has the implied right to use as much of the surface as "
        "is reasonably necessary to develop the minerals. However, the accommodation doctrine "
        "(also called the alternative means doctrine) limits this right: if the surface owner "
        "has an existing use of the surface, and the mineral lessee can accomplish the same "
        "objective by reasonable alternative means that do not interfere with the surface use, "
        "the lessee must accommodate the surface owner. Modern leases typically include specific "
        "surface use restrictions, surface damage payment obligations, and restoration requirements."
    ),
    legal_basis=(
        "The dominant mineral estate doctrine is Texas common law. The accommodation doctrine "
        "was established in Getty Oil Co. v. Jones and limits the dominant estate when "
        "alternative means are available."
    ),
    texas_authority="Getty Oil Co. v. Jones, 470 S.W.2d 618 (Tex. 1971)",
    analysis_template=(
        "1. Determine if the mineral and surface estates are severed\n"
        "2. Review the lease for specific surface use restrictions\n"
        "3. Identify any surface damage payment obligations\n"
        "4. Assess whether the accommodation doctrine applies\n"
        "5. Check for location restrictions (setbacks, no-drill zones)\n"
        "6. Review water rights provisions\n"
        "7. Evaluate restoration obligations after drilling\n"
        "8. Determine if surface owner consent is required for any activities"
    ),
    risk_factors=[
        "Surface owner claiming accommodation doctrine limits well placement",
        "High surface damage costs in developed areas",
        "Water use disputes between lessee and surface owner",
        "Environmental contamination liability on the surface",
    ],
    best_practices=[
        "Include specific surface use provisions in the lease",
        "Negotiate surface damage payments before operations begin",
        "Photograph and document surface condition before drilling",
        "Include restoration and reclamation obligations with timeline",
    ],
    common_pitfalls=[
        "Assuming unlimited surface access under the dominant estate doctrine",
        "Not budgeting for surface damage payments",
        "Failing to obtain necessary surface use agreements before operations",
    ],
    related_doctrines=["depth_limitation", "drilling_clause"],
    keywords=["surface use", "accommodation doctrine", "dominant estate", "surface damage", "Getty v. Jones"],
    permian_specific=True,
    statutory_references=["Tex. Nat. Res. Code § 91.001", "Tex. Water Code § 36.001"],
    case_law_references=[
        "Getty Oil Co. v. Jones, 470 S.W.2d 618 (Tex. 1971)",
        "Merriman v. XTO Energy, 407 S.W.3d 244 (Tex. 2013)",
    ],
))

_register(LeaseDoctrineBlock(
    key="depth_limitation",
    category=DoctrineCategory.DEPTH_LIMITATION,
    title="Depth Limitation Clause",
    summary=(
        "A depth limitation clause restricts the lease to a specific depth interval, typically "
        "defined by formation name, measured depth, or a combination. In the Permian Basin, "
        "depth limitations are common where the mineral estate has been vertically severed — "
        "for example, one lease covering the Spraberry/Wolfcamp (shallow) and a different "
        "lease covering the Bone Spring/Delaware (deep). Depth limitations can also result "
        "from Pugh clause depth releases, depth severance deeds, or operator assignments "
        "that retain certain depths. Proper identification of depth limitations is essential "
        "for title work because a well that penetrates below the leased depth may be trespassing."
    ),
    legal_basis=(
        "Texas recognizes the mineral estate can be vertically severed, creating separate "
        "estates for different depth intervals. Each depth interval is a distinct property "
        "interest that can be separately leased, conveyed, and encumbered."
    ),
    texas_authority="Tex. Nat. Res. Code § 91.001; common law vertical severance",
    analysis_template=(
        "1. Identify any depth limitation language in the lease\n"
        "2. Determine the reference: formation name, measured depth in feet, or both\n"
        "3. Map the depth limitation against the known Permian Basin stratigraphic column\n"
        "4. Check for depth severance deeds in the chain of title\n"
        "5. Verify that proposed wellbore targets fall within the leased depths\n"
        "6. Assess whether horizontal laterals stay within the leased depth interval\n"
        "7. Identify ownership of depths above and below the leased interval\n"
        "8. Check RRC well completion reports for perforated intervals"
    ),
    risk_factors=[
        "Wellbore crossing depth limitation boundary into non-leased interval",
        "Horizontal lateral deviating into shallower or deeper formation",
        "Vague depth reference that is difficult to apply in the field",
        "Conflicting depth limitations from different documents in the chain",
    ],
    best_practices=[
        "Use both formation name AND measured depth reference for clarity",
        "Include a buffer zone (e.g., 100 feet) around the depth boundary",
        "Coordinate depth limitations across all leases in a section",
        "Obtain directional survey data to confirm wellbore stays within limits",
    ],
    common_pitfalls=[
        "Assuming lease covers all depths when a depth limitation exists",
        "Using formation names without footage — formations dip and vary",
        "Not checking for depth severance deeds in the chain of title",
    ],
    related_doctrines=["pugh_horizontal", "retained_acreage", "surface_use_rights"],
    keywords=["depth limitation", "depth severance", "vertical severance", "formation", "depth interval"],
    permian_specific=True,
    statutory_references=["Tex. Nat. Res. Code § 91.001"],
    case_law_references=[
        "French v. Chevron U.S.A., 896 S.W.2d 795 (Tex. App. 1995)",
    ],
))

_register(LeaseDoctrineBlock(
    key="retained_acreage",
    category=DoctrineCategory.RETAINED_ACREAGE,
    title="Retained Acreage Provisions",
    summary=(
        "Retained acreage provisions define exactly how much acreage the lessee keeps after "
        "the primary term expires when a Pugh clause or similar release mechanism is present. "
        "The retained acreage is typically defined as the acreage within a producing unit, "
        "plus a reasonable buffer. The buffer may be a specific number of acres around the "
        "wellbore, the governmental drilling unit size, or the pooled unit boundaries. All "
        "acreage outside the retained area reverts to the lessor. The definition of retained "
        "acreage has become more complex with horizontal drilling, where a single lateral may "
        "span 10,000+ feet and the associated unit may encompass 640+ acres."
    ),
    legal_basis="Contractual provision defining the scope of retained rights after Pugh release.",
    texas_authority="Contractual provision; lease terms",
    analysis_template=(
        "1. Identify the retained acreage definition in the lease or Pugh clause\n"
        "2. Determine the method: pooled unit, governmental unit, or buffer-based\n"
        "3. Calculate the retained acreage for each producing well or unit\n"
        "4. Calculate the released acreage (total lease acreage minus retained)\n"
        "5. Map the retained and released acreage on a plat\n"
        "6. Verify consistency with RRC unit designations\n"
        "7. Check for overlap with adjacent lease retained acreage areas\n"
        "8. Determine the value of released vs retained acreage"
    ),
    risk_factors=[
        "Vague retained acreage definition leading to disputes",
        "Retained acreage calculation may change with unit boundary amendments",
        "Released acreage may have higher development potential than retained",
        "Multiple producing units creating fragmented retained acreage patterns",
    ],
    best_practices=[
        "Define retained acreage with specific reference to unit boundaries",
        "Include provisions for unit boundary changes affecting retained acreage",
        "Map all retained and released acreage on a current survey",
        "Coordinate retained acreage patterns across adjacent leases",
    ],
    common_pitfalls=[
        "Assuming retained acreage equals the entire lease when Pugh clause applies",
        "Not mapping the retained acreage to verify it matches expectations",
        "Overlooking that horizontal well units may retain more acreage than vertical",
    ],
    related_doctrines=["pugh_vertical", "pugh_horizontal", "pooling_voluntary"],
    keywords=["retained acreage", "released acreage", "Pugh release", "unit acreage"],
    permian_specific=True,
    statutory_references=[],
    case_law_references=[],
))

# ─────────────────────────────────────────────────────────────────────────────
# TOP LEASE, PREFERENTIAL RIGHTS, ASSIGNMENT, MOTHER HUBBARD, SURRENDER
# ─────────────────────────────────────────────────────────────────────────────

_register(LeaseDoctrineBlock(
    key="top_lease",
    category=DoctrineCategory.TOP_LEASE,
    title="Top Lease Provisions",
    summary=(
        "A top lease is an oil and gas lease granted by the mineral owner to take effect upon "
        "the expiration or termination of an existing (bottom) lease covering the same lands. "
        "Top leases are common in the Permian Basin where valuable acreage is under existing "
        "leases that may soon expire. The top lease typically recites that it is subject to "
        "the existing bottom lease and becomes effective only upon the bottom lease's "
        "termination. Top leases raise complex issues regarding priority, the effect of the "
        "bottom lease's renewal or extension, and potential tortious interference with the "
        "bottom lessee's contractual rights."
    ),
    legal_basis=(
        "Top leases are valid future interests in Texas. They are not considered tortious "
        "interference per se, though aggressive top leasing of a lease clearly held by "
        "production may give rise to claims."
    ),
    texas_authority="Tex. Prop. Code § 5.001; common law future interests",
    analysis_template=(
        "1. Identify any top leases recorded against the mineral interest\n"
        "2. Determine the effective date and triggering event\n"
        "3. Assess the current status of the bottom lease\n"
        "4. Evaluate the likelihood of the bottom lease expiring or terminating\n"
        "5. Check for provisions addressing the relationship between top and bottom lease\n"
        "6. Assess tortious interference risk if the bottom lease is clearly HBP\n"
        "7. Review the top lease terms (bonus, royalty, primary term)\n"
        "8. Determine priority among multiple top leases if any"
    ),
    risk_factors=[
        "Bottom lease renewal or extension defeating the top lease",
        "Multiple top leases creating priority disputes",
        "Tortious interference claim from the bottom lessee",
        "Top lease bonus paid for a lease that never takes effect",
    ],
    best_practices=[
        "Include specific language identifying the bottom lease and triggering event",
        "Record the top lease promptly for priority protection",
        "Include a term limitation (e.g., top lease expires if not effective within 5 years)",
        "Negotiate reasonable bonus considering the contingent nature of the grant",
    ],
    common_pitfalls=[
        "Assuming the top lease automatically voids the bottom lease",
        "Not checking for extension or renewal provisions in the bottom lease",
        "Paying excessive bonus for a highly contingent future interest",
    ],
    related_doctrines=["habendum_primary_term", "hbp_status", "preferential_right"],
    keywords=["top lease", "bottom lease", "future interest", "contingent grant", "priority"],
    permian_specific=True,
    statutory_references=["Tex. Prop. Code § 5.001", "Tex. Prop. Code § 13.001"],
    case_law_references=[
        "Chesapeake Exploration v. Hyder, 483 S.W.3d 870 (Tex. 2016)",
    ],
))

_register(LeaseDoctrineBlock(
    key="preferential_right",
    category=DoctrineCategory.PREFERENTIAL_RIGHT,
    title="Preferential Right of Purchase (ROFR)",
    summary=(
        "A preferential right of purchase (also called right of first refusal or ROFR) gives "
        "the holder the right to match any bona fide third-party offer to purchase the lease "
        "or working interest. The holder must be given notice of the proposed sale terms and "
        "a specified period (typically 15-60 days) to elect to purchase on the same terms. "
        "Preferential rights are common in joint operating agreements, farmout agreements, "
        "and some leases. They can significantly complicate lease acquisitions and must be "
        "identified early in the due diligence process."
    ),
    legal_basis=(
        "Preferential rights are contractual covenants that run with the interest. Texas "
        "courts enforce them according to their terms, subject to the rule against perpetuities."
    ),
    texas_authority="Contractual provision; Tex. Prop. Code § 5.043 (rule against perpetuities)",
    analysis_template=(
        "1. Identify all preferential rights affecting the lease or working interest\n"
        "2. Determine the scope: does it apply to the proposed transaction?\n"
        "3. Identify the notice requirements and election period\n"
        "4. Determine if the proposed transaction triggers the ROFR\n"
        "5. Prepare notice compliant with the ROFR terms\n"
        "6. Allow the holder the full election period to respond\n"
        "7. Document the holder's election or waiver\n"
        "8. Assess alternatives if the ROFR holder exercises"
    ),
    risk_factors=[
        "ROFR holder exercising the right, defeating the planned transaction",
        "Failure to provide proper notice, voiding the transaction",
        "ROFR scope broader than expected (applies to partial assignments)",
        "Multiple ROFRs with overlapping coverage",
    ],
    best_practices=[
        "Identify all ROFRs during due diligence before signing purchase agreement",
        "Include ROFR compliance as a closing condition in purchase agreements",
        "Provide ROFR notice promptly and track election deadline",
        "Obtain written waiver from ROFR holder if they do not exercise",
    ],
    common_pitfalls=[
        "Overlooking a ROFR buried in a joint operating agreement",
        "Structuring a transaction to avoid ROFR — courts may treat as evasion",
        "Not complying with specific notice requirements (form, timing, content)",
    ],
    related_doctrines=["assignment_sublease", "top_lease"],
    keywords=["preferential right", "ROFR", "right of first refusal", "matching right"],
    permian_specific=False,
    statutory_references=["Tex. Prop. Code § 5.043"],
    case_law_references=[
        "Tenneco Inc. v. Enterprise Products Co., 925 S.W.2d 640 (Tex. 1996)",
    ],
))

_register(LeaseDoctrineBlock(
    key="assignment_sublease",
    category=DoctrineCategory.ASSIGNMENT,
    title="Assignment and Sublease Provisions",
    summary=(
        "The lessee's working interest under an oil and gas lease is freely assignable unless "
        "the lease restricts or prohibits assignment. Assignments may be total (the entire lease) "
        "or partial (specific depths, specific acreage, or an undivided fractional interest). "
        "The assignor typically reserves an overriding royalty interest (ORRI). A sublease "
        "differs from an assignment — in a sublease, the original lessee retains a reversionary "
        "interest, while in an assignment, the entire interest is transferred. The distinction "
        "matters for determining who is liable for lease obligations."
    ),
    legal_basis=(
        "Oil and gas lease interests are property interests freely alienable under Texas law "
        "unless restricted by the lease terms. An assignment transfers the entire interest; "
        "a sublease retains a reversion."
    ),
    texas_authority="Tex. Prop. Code § 5.001; common law conveyancing principles",
    analysis_template=(
        "1. Review the lease for assignment restrictions or consent requirements\n"
        "2. Identify all assignments in the chain of title\n"
        "3. Determine if each assignment is total or partial\n"
        "4. Check for ORRI reservations in each assignment\n"
        "5. Verify cumulative burdens (royalty + all ORRIs + other burdens)\n"
        "6. Confirm current working interest owner from most recent assignment\n"
        "7. Check for proportionate reduction clauses in partial assignments\n"
        "8. Verify proper recording in county records"
    ),
    risk_factors=[
        "Unrecorded assignment creating title disputes",
        "Assignment violating consent provision in the lease",
        "Cumulative ORRIs making the lease uneconomical",
        "Partial assignment creating fragmented working interest ownership",
    ],
    best_practices=[
        "Record all assignments promptly in county real property records",
        "Include clear description of the interest assigned (surface, depth, fraction)",
        "Track cumulative burdens with each assignment",
        "Obtain lessor consent if required by the lease",
    ],
    common_pitfalls=[
        "Failing to record the assignment — subsequent BFP may take priority",
        "Not checking for consent requirements before closing",
        "Creating fractional interests so small they become unmarketable",
    ],
    related_doctrines=["overriding_royalty", "preferential_right", "nri_calculation"],
    keywords=["assignment", "sublease", "transfer", "ORRI reservation", "partial assignment"],
    permian_specific=False,
    statutory_references=["Tex. Prop. Code § 5.001", "Tex. Prop. Code § 13.001"],
    case_law_references=[
        "Sunac Petroleum Corp. v. Parkes, 416 S.W.2d 798 (Tex. 1967)",
    ],
))

_register(LeaseDoctrineBlock(
    key="mother_hubbard",
    category=DoctrineCategory.MOTHER_HUBBARD,
    title="Mother Hubbard Clause",
    summary=(
        "The Mother Hubbard clause (also called a cover-all or after-acquired clause) extends "
        "the lease to cover small strips, gores, or fractional interests owned by the lessor "
        "that are contiguous or adjacent to the specifically described lands but were "
        "inadvertently omitted from the legal description. The clause typically reads: "
        "'This lease also covers and includes all land owned or claimed by the lessor adjacent "
        "or contiguous to the land described herein.' Texas courts strictly construe Mother "
        "Hubbard clauses — they cover only small tracts and strips, not substantial separately "
        "described parcels."
    ),
    legal_basis=(
        "Texas Supreme Court in Sharp v. Fowler held that a Mother Hubbard clause operates "
        "as a quitclaim and does not constitute constructive notice to subsequent purchasers "
        "of the undescribed tracts."
    ),
    texas_authority="Sharp v. Fowler, 151 Tex. 490, 252 S.W.2d 153 (1952)",
    analysis_template=(
        "1. Identify Mother Hubbard language in the lease\n"
        "2. Determine the scope: 'adjacent or contiguous' vs broader language\n"
        "3. Identify any tracts or strips that could be covered\n"
        "4. Assess the size of the potentially covered tracts (small strips only)\n"
        "5. Check for after-acquired interest language\n"
        "6. Evaluate constructive notice limitations\n"
        "7. Determine if any substantial tracts are improperly claimed under the clause"
    ),
    risk_factors=[
        "Mother Hubbard clause being used to claim substantial unreleased acreage",
        "Lack of constructive notice defeating the clause against BFPs",
        "Uncertainty about which tracts are actually covered",
    ],
    best_practices=[
        "Specifically describe all lands intended to be leased — do not rely on Mother Hubbard",
        "If Mother Hubbard clause is present, verify it covers only minor strips",
        "Do not rely on Mother Hubbard for constructive notice to third parties",
    ],
    common_pitfalls=[
        "Relying on Mother Hubbard to cover substantial acreage",
        "Assuming Mother Hubbard provides constructive notice",
        "Not specifically describing all intended tracts in the lease",
    ],
    related_doctrines=["habendum_primary_term"],
    keywords=["Mother Hubbard", "cover-all clause", "adjacent", "contiguous", "strips and gores"],
    permian_specific=False,
    statutory_references=["Tex. Prop. Code § 13.001"],
    case_law_references=[
        "Sharp v. Fowler, 151 Tex. 490, 252 S.W.2d 153 (1952)",
    ],
))

_register(LeaseDoctrineBlock(
    key="surrender_clause",
    category=DoctrineCategory.SURRENDER,
    title="Surrender Clause",
    summary=(
        "The surrender clause gives the lessee the right to release all or part of the leased "
        "premises at any time, thereby terminating the lease (or reducing its coverage) and "
        "extinguishing future obligations on the surrendered acreage. Partial surrender allows "
        "the lessee to release non-productive or non-prospective acreage while retaining the "
        "productive portions. The surrendering lessee typically must provide written notice to "
        "the lessor and file a release of record in the county records. Upon surrender, the "
        "lessee is usually entitled to a pro rata refund of any prepaid delay rentals "
        "attributable to the surrendered acreage."
    ),
    legal_basis=(
        "The surrender clause is a contractual right that allows the lessee to voluntarily "
        "relinquish the lease without liability for future obligations on the surrendered lands."
    ),
    texas_authority="Contractual provision; Tex. Prop. Code § 5.001",
    analysis_template=(
        "1. Identify the surrender clause in the lease\n"
        "2. Determine if partial surrender is permitted\n"
        "3. Check notice requirements (written, days before effective)\n"
        "4. Determine if rental credit or refund is available on surrendered acreage\n"
        "5. Verify the surrender was properly recorded in county records\n"
        "6. Calculate the remaining lease acreage after partial surrender\n"
        "7. Assess the impact on any continuous development obligations\n"
        "8. Determine if the surrender extinguishes all lessee obligations on the surrendered land"
    ),
    risk_factors=[
        "Surrender of acreage that later proves to be highly valuable",
        "Failure to file proper release in county records creating title cloud",
        "Partial surrender not clearly described, leading to boundary disputes",
    ],
    best_practices=[
        "File a properly recorded release or partial release in county records",
        "Clearly describe the surrendered acreage by legal description",
        "Request confirmation of receipt of surrender notice from lessor",
        "Evaluate the geological and economic value before surrendering",
    ],
    common_pitfalls=[
        "Surrendering acreage without proper evaluation of remaining potential",
        "Not filing the release of record — creates cloud on lessor's title",
        "Assuming verbal surrender is effective — must follow lease notice provisions",
    ],
    related_doctrines=["delay_rental_unless", "retained_acreage", "pugh_vertical"],
    keywords=["surrender", "release", "partial release", "relinquish", "abandon"],
    permian_specific=False,
    statutory_references=["Tex. Prop. Code § 5.001", "Tex. Prop. Code § 13.001"],
    case_law_references=[],
))

# ─────────────────────────────────────────────────────────────────────────────
# NRI CALCULATION DOCTRINE
# ─────────────────────────────────────────────────────────────────────────────

_register(LeaseDoctrineBlock(
    key="nri_calculation",
    category=DoctrineCategory.NRI_CALCULATION,
    title="Net Revenue Interest (NRI) Calculation",
    summary=(
        "The Net Revenue Interest (NRI) is the share of production revenue that a working "
        "interest owner actually receives after all burdens (royalties, overriding royalties, "
        "production payments, and other non-operating interests) are deducted. The formula is: "
        "NRI = Working Interest × (1 - Sum of All Burdens). For example, if the working interest "
        "is 75% (3/4 lease with 1/4 royalty) and there is a 3% ORRI, the NRI = 0.75 × (1 - 0.03) "
        "= 0.7275 or 72.75%. When acreage is pooled, the NRI is further adjusted by the tract's "
        "participation factor in the pooled unit. In the Permian Basin, common NRI values for a "
        "100% working interest with 1/4 royalty and no ORRI are 75% (0.750000)."
    ),
    legal_basis=(
        "NRI is a mathematical calculation derived from the lease terms, assignments, and "
        "any encumbrances on the working interest. It is verified through the division order "
        "process before first production."
    ),
    texas_authority="Tex. Nat. Res. Code § 91.402 (division orders); common law",
    analysis_template=(
        "1. Start with the full mineral interest (1.000000 or 8/8ths)\n"
        "2. Determine the lessor's royalty fraction and subtract from WI\n"
        "3. Identify all ORRIs, production payments, and other burdens\n"
        "4. Subtract all burdens from the working interest\n"
        "5. If pooled, multiply by participation factor (tract acres / unit acres)\n"
        "6. If partial mineral interest, multiply by the undivided fraction\n"
        "7. Verify the calculated NRI against the division order\n"
        "8. Cross-check with operator's revenue distribution"
    ),
    risk_factors=[
        "Cumulative burdens exceeding 100% of gross production (mathematical impossibility)",
        "Unrecorded ORRIs not reflected in NRI calculation",
        "Division order errors perpetuating incorrect NRI",
        "Partial mineral interest not properly factored",
    ],
    best_practices=[
        "Build NRI calculation from the ground up — mineral interest through all encumbrances",
        "Verify every burden in the chain of title",
        "Compare calculated NRI to division order NRI — investigate any discrepancy",
        "Track NRI changes with each assignment or encumbrance",
    ],
    common_pitfalls=[
        "Using working interest as NRI — they are different",
        "Not accounting for all ORRIs in the chain of assignments",
        "Applying pooling participation factor incorrectly",
        "Forgetting to multiply by undivided mineral interest fraction",
    ],
    related_doctrines=["royalty_calculation", "overriding_royalty", "pooling_voluntary", "assignment_sublease"],
    keywords=["NRI", "net revenue interest", "working interest", "burdens", "division order"],
    permian_specific=True,
    statutory_references=["Tex. Nat. Res. Code § 91.402"],
    case_law_references=[],
))

# ─────────────────────────────────────────────────────────────────────────────
# TEXAS STATUTORY FRAMEWORK
# ─────────────────────────────────────────────────────────────────────────────

_register(LeaseDoctrineBlock(
    key="texas_mineral_code",
    category=DoctrineCategory.TEXAS_STATUTORY,
    title="Texas Natural Resources Code - Mineral Interest Provisions",
    summary=(
        "The Texas Natural Resources Code (TNRC) governs oil and gas operations in Texas. "
        "Key chapters include: Ch. 85-86 (RRC regulatory authority), Ch. 89 (plugging and "
        "abandonment), Ch. 91 (common lessees and royalty payments), Ch. 92 (payment of "
        "royalties), Ch. 101 (unitization agreements), and Ch. 102 (mineral interest pooling). "
        "The TNRC does not codify lease interpretation — that remains common law. The RRC "
        "regulates drilling, production, and conservation but does not adjudicate lease disputes."
    ),
    legal_basis="Texas Natural Resources Code, enacted and amended by the Texas Legislature.",
    texas_authority="Tex. Nat. Res. Code Ann. §§ 85.001-102.051",
    analysis_template=(
        "1. Identify the specific TNRC provision applicable to the issue\n"
        "2. Review RRC rules implementing the statutory provision\n"
        "3. Check for recent amendments or updates\n"
        "4. Apply the statutory provision to the facts\n"
        "5. Consider federal preemption issues if applicable\n"
        "6. Cross-reference with relevant case law interpreting the statute"
    ),
    risk_factors=[
        "Statutory changes affecting existing lease obligations",
        "RRC rule changes affecting drilling and production practices",
        "Federal environmental regulations preempting state rules",
    ],
    best_practices=[
        "Stay current on TNRC amendments and RRC rulemaking",
        "Consult the RRC's Statewide Rules for operational requirements",
        "Monitor legislative sessions for proposed changes to the TNRC",
    ],
    common_pitfalls=[
        "Assuming lease terms control when TNRC imposes stricter requirements",
        "Not checking for RRC rules implementing TNRC provisions",
        "Overlooking federal preemption in environmental matters",
    ],
    related_doctrines=["royalty_calculation", "pooling_voluntary", "drilling_clause"],
    keywords=["TNRC", "Texas Natural Resources Code", "RRC", "mineral code", "statutory"],
    permian_specific=True,
    statutory_references=[
        "Tex. Nat. Res. Code § 85.001", "Tex. Nat. Res. Code § 89.001",
        "Tex. Nat. Res. Code § 91.001", "Tex. Nat. Res. Code § 92.001",
        "Tex. Nat. Res. Code § 101.001", "Tex. Nat. Res. Code § 102.001",
    ],
    case_law_references=[],
))

_register(LeaseDoctrineBlock(
    key="texas_recording_statute",
    category=DoctrineCategory.TEXAS_STATUTORY,
    title="Texas Recording Statute - Notice and Priority",
    summary=(
        "Texas is a notice jurisdiction with a race-notice recording statute (Tex. Prop. Code "
        "§ 13.001). A subsequent purchaser for value who records first and takes without notice "
        "of a prior unrecorded conveyance prevails over the prior grantee. For oil and gas "
        "leases, this means prompt recording is essential to protect against subsequent "
        "conveyances. The recording statute applies to leases, assignments, ORRIs, production "
        "payments, and all other interests in real property. Failure to record timely can result "
        "in loss of the leasehold interest to a subsequent bona fide purchaser."
    ),
    legal_basis=(
        "Texas Property Code § 13.001 — A conveyance of real property or an interest therein "
        "is void as to a subsequent purchaser for a valuable consideration without notice "
        "unless the instrument has been acknowledged, sworn to, or proved and filed for record."
    ),
    texas_authority="Tex. Prop. Code Ann. § 13.001",
    analysis_template=(
        "1. Check recording status of all instruments in the chain of title\n"
        "2. Identify any unrecorded instruments that could be at risk\n"
        "3. Determine recording dates and sequence of all conveyances\n"
        "4. Assess whether any subsequent grantees took without notice\n"
        "5. Evaluate constructive vs actual notice for each transaction\n"
        "6. Check for Mother Hubbard clause limitations on constructive notice\n"
        "7. Verify that all lease amendments and modifications are recorded"
    ),
    risk_factors=[
        "Unrecorded lease or assignment creating risk of loss to BFP",
        "Gap in recording chain creating title defect",
        "Delayed recording allowing intervening conveyances",
    ],
    best_practices=[
        "Record all instruments promptly after execution",
        "Verify recording by obtaining file-stamped copy from county clerk",
        "Maintain a recording log tracking all instruments and their recording data",
        "Run title before and after recording to confirm chain is complete",
    ],
    common_pitfalls=[
        "Delaying recording while negotiating post-closing matters",
        "Assuming execution date equals recording date",
        "Not verifying that the county clerk properly indexed the instrument",
    ],
    related_doctrines=["assignment_sublease", "top_lease", "mother_hubbard"],
    keywords=["recording statute", "notice", "priority", "BFP", "constructive notice", "race-notice"],
    permian_specific=False,
    statutory_references=["Tex. Prop. Code § 13.001"],
    case_law_references=[
        "Madison v. Gordon, 39 S.W.3d 604 (Tex. 2001)",
    ],
))

_register(LeaseDoctrineBlock(
    key="implied_covenants",
    category=DoctrineCategory.TEXAS_STATUTORY,
    title="Implied Covenants in Oil and Gas Leases",
    summary=(
        "Texas law implies several covenants in oil and gas leases even when not expressly "
        "stated: (1) Covenant to develop — the lessee must develop the lease as a reasonably "
        "prudent operator, considering geological data, market conditions, and the lessor's "
        "interests. (2) Covenant to protect against drainage — the lessee must drill offset "
        "wells when adjacent wells are draining the leased minerals. (3) Covenant to market — "
        "the lessee must market production within a reasonable time. (4) Covenant to manage "
        "and administer — the lessee must manage operations prudently. (5) Covenant to conduct "
        "further exploration — the lessee must explore undeveloped portions of the lease."
    ),
    legal_basis=(
        "Implied covenants arise from the relationship between lessor and lessee and the "
        "general duty of good faith. They supplement express lease terms but do not override "
        "them. The reasonably prudent operator standard governs all implied covenants."
    ),
    texas_authority="Amoco Prod. Co. v. Alexander, 622 S.W.2d 563 (Tex. 1981)",
    analysis_template=(
        "1. Identify the specific implied covenant at issue\n"
        "2. Determine the standard: reasonably prudent operator\n"
        "3. Gather evidence of what a prudent operator would do in similar circumstances\n"
        "4. Compare the lessee's actual conduct to the prudent operator standard\n"
        "5. Assess whether express lease terms modify or replace the implied covenant\n"
        "6. Determine remedies available for breach: damages, lease cancellation, or both\n"
        "7. Evaluate defenses: economic futility, force majeure, lease restrictions"
    ),
    risk_factors=[
        "Lessee failing to drill development wells on productive portions of the lease",
        "Adjacent operators drilling offset wells that drain leased minerals",
        "Lessee failing to market production within a reasonable time",
        "Lessor claiming breach to terminate lease or extract damages",
    ],
    best_practices=[
        "Monitor adjacent drilling activity for potential drainage",
        "Maintain communication with operator regarding development plans",
        "Document the economics supporting or opposing additional development",
        "Include express development obligations to supplement implied covenants",
    ],
    common_pitfalls=[
        "Assuming express lease terms completely displace implied covenants",
        "Failing to monitor for drainage by adjacent operators",
        "Not pursuing breach of implied covenant claims within the statute of limitations",
    ],
    related_doctrines=["continuous_development", "hbp_status", "drilling_clause"],
    keywords=["implied covenant", "reasonably prudent operator", "develop", "protect", "drainage", "market"],
    permian_specific=False,
    statutory_references=["Tex. Nat. Res. Code § 91.001"],
    case_law_references=[
        "Amoco Prod. Co. v. Alexander, 622 S.W.2d 563 (Tex. 1981)",
        "Clifton v. Koontz, 325 S.W.2d 684 (Tex. 1959)",
        "Rogers v. Osborn, 152 Tex. 540, 261 S.W.2d 311 (1953)",
    ],
))

# ============================================================================
# DOCTRINE CACHE INTEGRITY AND ACCESS FUNCTIONS
# ============================================================================

def _compute_cache_hash() -> str:
    """Compute SHA-256 hash of the entire doctrine cache for integrity verification."""
    cache_data = {k: v.to_dict() for k, v in sorted(DOCTRINE_CACHE.items())}
    content = json.dumps(cache_data, sort_keys=True)
    return hashlib.sha256(content.encode()).hexdigest()


# Compute hash on module load
DOCTRINE_CACHE_HASH = _compute_cache_hash()
logger.info(
    f"LM02 Doctrine Cache loaded: {len(DOCTRINE_CACHE)} blocks, "
    f"version={DOCTRINE_CACHE_VERSION}, hash={DOCTRINE_CACHE_HASH[:16]}..."
)


def get_doctrine(key: str) -> Optional[LeaseDoctrineBlock]:
    """Retrieve a single doctrine block by key.

    Args:
        key: The doctrine key to look up.

    Returns:
        The matching LeaseDoctrineBlock, or None if not found.
    """
    block = DOCTRINE_CACHE.get(key)
    if block is None:
        logger.warning(f"Doctrine key not found: {key}")
    return block


def list_doctrine_keys() -> List[str]:
    """Return all doctrine keys in the cache.

    Returns:
        Sorted list of all doctrine keys.
    """
    return sorted(DOCTRINE_CACHE.keys())


def list_doctrines_by_category(category: DoctrineCategory) -> List[LeaseDoctrineBlock]:
    """Return all doctrine blocks in a specific category.

    Args:
        category: The DoctrineCategory to filter by.

    Returns:
        List of matching LeaseDoctrineBlock instances.
    """
    return [b for b in DOCTRINE_CACHE.values() if b.category == category]


def match_doctrine(query: str, top_k: int = 5) -> List[Tuple[str, float, LeaseDoctrineBlock]]:
    """Match a natural language query to the most relevant doctrines.

    Uses keyword overlap scoring to rank doctrine blocks by relevance to the query.

    Args:
        query: Natural language query string.
        top_k: Maximum number of results to return.

    Returns:
        List of (key, score, block) tuples sorted by descending score.
    """
    query_lower = query.lower()
    query_tokens = set(query_lower.split())

    results: List[Tuple[str, float, LeaseDoctrineBlock]] = []

    for key, block in DOCTRINE_CACHE.items():
        score = 0.0

        # Title match (highest weight)
        title_lower = block.title.lower()
        for token in query_tokens:
            if token in title_lower:
                score += 3.0

        # Keyword match (high weight)
        for kw in block.keywords:
            kw_lower = kw.lower()
            if kw_lower in query_lower:
                score += 2.5
            for token in query_tokens:
                if token in kw_lower:
                    score += 1.0

        # Summary match (medium weight)
        summary_lower = block.summary.lower()
        for token in query_tokens:
            if len(token) >= 4 and token in summary_lower:
                score += 0.5

        # Category match
        if block.category.value in query_lower:
            score += 1.5

        # Permian Basin bonus
        if block.permian_specific and ("permian" in query_lower or "midland" in query_lower or "ector" in query_lower):
            score += 1.0

        if score > 0:
            results.append((key, score, block))

    results.sort(key=lambda x: x[1], reverse=True)
    return results[:top_k]


def get_doctrine_summary() -> Dict[str, Any]:
    """Return a summary of the doctrine cache.

    Returns:
        Dictionary with cache statistics.
    """
    categories = {}
    for block in DOCTRINE_CACHE.values():
        cat = block.category.value
        categories[cat] = categories.get(cat, 0) + 1

    return {
        "version": DOCTRINE_CACHE_VERSION,
        "build_date": DOCTRINE_CACHE_BUILD_DATE,
        "total_blocks": len(DOCTRINE_CACHE),
        "hash": DOCTRINE_CACHE_HASH,
        "categories": categories,
        "keys": list_doctrine_keys(),
        "permian_specific_count": sum(1 for b in DOCTRINE_CACHE.values() if b.permian_specific),
    }


def get_applicable_doctrines(
    clause_types: List[str],
    permian_only: bool = False,
) -> List[LeaseDoctrineBlock]:
    """Get all doctrines applicable to a set of lease clause types.

    Args:
        clause_types: List of clause type strings to match against categories.
        permian_only: If True, return only Permian Basin-specific doctrines.

    Returns:
        List of matching LeaseDoctrineBlock instances.
    """
    clause_types_lower = [ct.lower() for ct in clause_types]
    results = []

    for block in DOCTRINE_CACHE.values():
        if permian_only and not block.permian_specific:
            continue

        category_match = block.category.value.lower() in clause_types_lower
        keyword_match = any(
            any(ct in kw.lower() for ct in clause_types_lower)
            for kw in block.keywords
        )

        if category_match or keyword_match:
            results.append(block)

    return results


def verify_cache_integrity() -> bool:
    """Verify doctrine cache has not been tampered with since load.

    Returns:
        True if integrity check passes, False if cache has been modified.
    """
    current_hash = _compute_cache_hash()
    if current_hash != DOCTRINE_CACHE_HASH:
        logger.error(
            f"Doctrine cache integrity check FAILED. "
            f"Expected: {DOCTRINE_CACHE_HASH[:16]}..., Got: {current_hash[:16]}..."
        )
        return False
    logger.debug("Doctrine cache integrity check PASSED.")
    return True
