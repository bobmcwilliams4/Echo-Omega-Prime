"""
LM11 Lease Negotiation Engine — Doctrine Cache
Pre-compiled expert reasoning blocks for oil and gas lease negotiation.

Each DoctrineBlock contains real domain content:
- Conclusion template with actionable guidance
- Reasoning framework with multi-step analysis
- Key factors for evaluation
- Primary authority citations
- Adversary positions and counter-arguments
- Resolution strategies

Author: ECHO OMEGA PRIME
Engine: LM11 Lease Negotiation
Version: 1.0.0
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from loguru import logger

ENGINE_ID = "LM11"
DOCTRINE_VERSION = "1.0.0"


@dataclass
class DoctrineBlock:
    """A single pre-compiled doctrine reasoning block."""
    topic: str
    keywords: List[str]
    conclusion_template: str
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    burden_holder: str
    adversary_position: str
    counter_arguments: List[str]
    resolution_strategy: str
    entity_scope: str
    confidence: str
    confidence_stratification: str
    controlling_precedent: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "topic": self.topic,
            "keywords": self.keywords,
            "conclusion_template": self.conclusion_template,
            "key_factors": self.key_factors,
            "primary_authority": self.primary_authority,
            "confidence": self.confidence,
            "confidence_stratification": self.confidence_stratification,
            "entity_scope": self.entity_scope,
            "burden_holder": self.burden_holder,
        }


def build_doctrine_cache() -> Dict[str, DoctrineBlock]:
    """Build and return the complete doctrine cache for lease negotiation."""
    blocks: Dict[str, DoctrineBlock] = {}

    # =========================================================================
    # BLOCK 1: ROYALTY RATE NEGOTIATION
    # =========================================================================
    blocks["royalty_rate_negotiation"] = DoctrineBlock(
        topic="royalty_rate_negotiation",
        keywords=["royalty", "rate", "fraction", "one-eighth", "one-fifth", "one-fourth", "percentage", "mineral owner"],
        conclusion_template=(
            "Royalty rates in modern oil and gas leases vary significantly by basin, market conditions, "
            "and lessor bargaining power. The historical 1/8 royalty is now considered below-market in most "
            "active basins. Permian Basin lessors routinely negotiate 1/4 (25%) royalties, while 3/16 to 1/5 "
            "is common in less competitive areas. The royalty fraction directly impacts the lessor's revenue "
            "stream for the life of the lease and should be the primary negotiation focus."
        ),
        reasoning_framework=(
            "Step 1: Assess current market royalty rates for the specific basin and county. "
            "Permian Basin (Midland/Delaware) commands 22-25%; Eagle Ford 22-25%; Haynesville 20-25%; "
            "Bakken 18-20%; Appalachian 15-18%. "
            "Step 2: Evaluate lessor bargaining position — mineral acreage size, location relative to "
            "active drilling, number of competing operators, existing production on offsetting tracts. "
            "Step 3: Consider the royalty fraction in conjunction with bonus consideration — higher "
            "royalty may justify lower bonus and vice versa. "
            "Step 4: Determine whether the royalty should be a fraction of gross production or a "
            "percentage of value. Fraction-based language (e.g., 1/4 of all oil produced) provides "
            "stronger protection than percentage-based. "
            "Step 5: Analyze interaction with post-production cost deductions — a 25% royalty with "
            "post-production deductions may net less than a 20% cost-free royalty. "
            "Step 6: Consider escalation clauses — royalty increases after payout or after initial "
            "production period. Common structure: 1/5 for first 3 years, 1/4 thereafter. "
            "Step 7: Review state-specific minimum royalty requirements. Texas has no statutory minimum "
            "for private leases; Oklahoma requires minimum 1/8 for force-pooled interests. "
            "Step 8: Document the negotiated rate clearly in the lease with no ambiguity."
        ),
        key_factors=[
            "Basin and county market rates for comparable leases",
            "Mineral acreage size and contiguity",
            "Proximity to active horizontal drilling programs",
            "Number of competing operators seeking leases in the area",
            "Whether royalty is cost-free or subject to post-production deductions",
            "Interaction between royalty rate and bonus consideration",
            "State regulatory minimums for pooled/unitized interests",
            "Lessor sophistication and willingness to negotiate",
        ],
        primary_authority=[
            "Texas Natural Resources Code Ch. 91 — general lease provisions",
            "Chesapeake Exploration v. Hyder, 483 S.W.3d 870 (Tex. 2016) — royalty valuation",
            "Burlington Resources Oil & Gas Co. v. Texas Crude Energy, 573 S.W.3d 198 (Tex. 2019)",
            "Heritage Resources v. NationsBank, 939 S.W.2d 118 (Tex. 1996) — royalty obligations",
            "AAPL Form 610-2015 Model Form Operating Agreement",
        ],
        burden_holder="Lessor bears burden of negotiating above-market royalty rate",
        adversary_position=(
            "Lessee will argue that higher royalty rates reduce working interest economics, "
            "potentially making marginal wells uneconomic and discouraging development. Lessee "
            "may offer higher bonus in exchange for lower royalty."
        ),
        counter_arguments=[
            "Modern horizontal wells in active basins generate sufficient revenue to support 25% royalties",
            "Competing operators are offering 1/4 royalty as standard in this area",
            "The royalty rate persists for the life of the lease; bonus is a one-time payment",
            "Post-production cost deductions effectively reduce the stated royalty percentage",
            "Lessor has no obligation to subsidize lessee's marginal economics",
            "Higher royalty aligns lessor and lessee interests in maximizing production value",
        ],
        resolution_strategy=(
            "Negotiate royalty rate first as the highest-impact economic term. Use comparable "
            "lease data from county clerk records to establish market rate. If lessee resists "
            "top-tier royalty, negotiate cost-free language to protect the effective rate. "
            "Consider tiered royalty structures as a compromise."
        ),
        entity_scope="lessor_lessee",
        confidence="DEFENSIBLE",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Chesapeake v. Hyder (Tex. 2016)",
    )

    # =========================================================================
    # BLOCK 2: COST-FREE ROYALTY
    # =========================================================================
    blocks["cost_free_royalty"] = DoctrineBlock(
        topic="cost_free_royalty",
        keywords=["cost-free", "free of cost", "post-production", "deductions", "gathering", "transportation", "compression", "processing"],
        conclusion_template=(
            "Cost-free royalty language eliminates the operator's ability to deduct post-production "
            "costs (gathering, compression, dehydration, transportation, processing, marketing) from "
            "the lessor's royalty. Without cost-free language, operators in Texas may deduct these costs "
            "under Heritage Resources v. NationsBank. A cost-free royalty at 20% may net more than a "
            "25% royalty subject to deductions, making this the single most important protective clause."
        ),
        reasoning_framework=(
            "Step 1: Identify all potential post-production cost categories: gathering fees ($0.15-0.50/Mcf), "
            "compression ($0.10-0.30/Mcf), dehydration ($0.05-0.15/Mcf), transportation ($0.20-1.00/Mcf), "
            "processing ($0.30-0.80/Mcf for NGLs), marketing fees (1-3% of value). "
            "Step 2: Calculate aggregate deduction impact — in the Permian, total post-production costs "
            "can reach $1.50-3.00/Mcf for gas, effectively reducing a 25% royalty to 15-18% net. "
            "Step 3: Draft cost-free language that is comprehensive and unambiguous: 'Lessor's royalty "
            "shall be free and clear of all costs, expenses, and charges of every kind incurred after "
            "severance from the soil, including but not limited to costs of gathering, compression, "
            "dehydration, transportation, treating, processing, and marketing.' "
            "Step 4: Address the valuation point — cost-free royalty should be calculated at the point "
            "of sale, not at the wellhead. This captures the full market value. "
            "Step 5: Include anti-affiliate language to prevent operator from charging above-market "
            "rates through affiliated midstream companies."
        ),
        key_factors=[
            "Total aggregate post-production costs in the specific basin",
            "Whether operator owns affiliated midstream infrastructure",
            "Gas vs. oil production mix — gas production has higher post-production cost exposure",
            "Length and complexity of gathering and processing chain",
            "State law default on cost allocation (Heritage Resources in TX)",
            "Interaction with royalty rate — cost-free may justify slightly lower fraction",
        ],
        primary_authority=[
            "Heritage Resources v. NationsBank, 939 S.W.2d 118 (Tex. 1996) — costs deductible absent contrary language",
            "Chesapeake Exploration v. Hyder, 483 S.W.3d 870 (Tex. 2016) — royalty valuation at point of sale",
            "Burlington Resources v. Texas Crude Energy, 573 S.W.3d 198 (Tex. 2019)",
            "Potts v. Chesapeake Exploration, 760 F.3d 470 (5th Cir. 2014)",
        ],
        burden_holder="Lessor must affirmatively negotiate cost-free language into the lease",
        adversary_position=(
            "Lessee argues that royalty should be valued at the wellhead and that post-production "
            "costs are necessary to make the product marketable. Lessee may claim cost-free royalty "
            "creates a windfall for the lessor."
        ),
        counter_arguments=[
            "Heritage Resources allows deductions only absent contrary lease language — include cost-free provisions",
            "Post-production costs can consume 30-50% of gas royalty value without protection",
            "Operator controls the midstream contracts and can inflate costs through affiliates",
            "The implied covenant to market requires operator to obtain best available price",
            "Cost-free language is now standard in sophisticated mineral owner leases",
        ],
        resolution_strategy=(
            "Insist on comprehensive cost-free language covering all post-production cost categories. "
            "If lessee resists blanket cost-free, negotiate caps on deductible costs or require "
            "arm's-length pricing for affiliated midstream services."
        ),
        entity_scope="lessor_lessee",
        confidence="DEFENSIBLE",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Heritage Resources v. NationsBank (Tex. 1996)",
    )

    # =========================================================================
    # BLOCK 3: BONUS CONSIDERATION STRATEGY
    # =========================================================================
    blocks["bonus_consideration"] = DoctrineBlock(
        topic="bonus_consideration",
        keywords=["bonus", "per acre", "signing", "consideration", "cash", "delay rental", "paid-up"],
        conclusion_template=(
            "Lease bonus is the upfront cash payment per net mineral acre for executing the lease. "
            "Permian Basin bonuses range from $5,000 to $75,000+ per acre depending on location. "
            "Bonus is a one-time payment and should be negotiated in balance with royalty rate and "
            "other economic terms. A paid-up lease eliminates delay rental obligations but removes "
            "the annual payment leverage that encourages timely development."
        ),
        reasoning_framework=(
            "Step 1: Research comparable bonus payments in the specific county and area using recent "
            "lease filings at the county clerk's office. "
            "Step 2: Assess the mineral acreage's strategic value: proximity to active wells, geologic "
            "quality, operator competition level, and unleased acreage scarcity. "
            "Step 3: Evaluate the trade-off between bonus and royalty rate — a lessor may accept lower "
            "bonus for higher royalty if they believe production is likely. "
            "Step 4: Determine whether paid-up lease or delay rental structure is preferred. "
            "Delay rentals ($X/acre/year) create annual touchpoints and leverage. "
            "Paid-up eliminates that leverage but provides certainty. "
            "Step 5: Negotiate bonus payment structure — lump sum at execution vs. installments. "
            "Lump sum is strongly preferred. "
            "Step 6: Ensure bonus is payable per net mineral acre, not gross acre. "
            "Step 7: Address bonus for lease extension or renewal separately."
        ),
        key_factors=[
            "Recent comparable lease bonus payments in the area",
            "Number of competing operators seeking leases",
            "Geologic prospectivity and proximity to production",
            "Mineral acreage size and contiguity",
            "Whether the area is HBP or open for new leasing",
            "Primary term length — longer terms justify higher bonus",
            "Paid-up vs. delay rental structure preference",
        ],
        primary_authority=[
            "Texas Property Code — consideration requirements for valid lease",
            "Anadarko Petroleum Corp. v. Thompson, 94 S.W.3d 550 (Tex. 2002)",
            "AAPL Landman's Legal Handbook, Ch. 4 — Lease Acquisition",
            "Rogers v. Ricane Enterprises, 772 S.W.2d 76 (Tex. 1989)",
        ],
        burden_holder="Lessor must establish market value of bonus through comparable data",
        adversary_position=(
            "Lessee will argue that high bonus payments must be offset by lower royalty rates "
            "to maintain economic viability. Lessee may offer installment payments or delay "
            "rental structure to reduce upfront cash outlay."
        ),
        counter_arguments=[
            "County records show comparable leases at $X/acre — this offer is below market",
            "Multiple operators are competing for acreage in this area",
            "Bonus is a one-time cost; royalty obligations persist for decades",
            "Paid-up lease removes lessor's annual leverage over operator development timing",
            "Installment payments create credit risk — lump sum is industry standard",
        ],
        resolution_strategy=(
            "Gather comparable lease data from county records. Present market evidence to "
            "support bonus demand. Negotiate bonus and royalty as a package — be willing "
            "to trade modest bonus reduction for stronger royalty and protective clauses."
        ),
        entity_scope="lessor_lessee",
        confidence="DEFENSIBLE",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Anadarko v. Thompson (Tex. 2002)",
    )

    # =========================================================================
    # BLOCK 4: PRIMARY TERM SELECTION
    # =========================================================================
    blocks["primary_term_selection"] = DoctrineBlock(
        topic="primary_term_selection",
        keywords=["primary term", "years", "three year", "five year", "ten year", "exploration", "initial term"],
        conclusion_template=(
            "The primary term defines the exploration period during which the lessee must commence "
            "operations or the lease expires. Shorter primary terms (3 years) favor the lessor by "
            "forcing faster development. Longer terms (5-10 years) favor the lessee. In active "
            "basins like the Permian, 3-year terms are standard. Lessors should resist terms "
            "exceeding 5 years unless compensated with higher bonus or continuous drilling obligations."
        ),
        reasoning_framework=(
            "Step 1: Assess operator's likely development timeline for the area. If the operator "
            "has active rigs nearby, a 3-year term is reasonable. If the area is exploratory, the "
            "operator may legitimately need 5 years. "
            "Step 2: Evaluate the relationship between primary term and bonus — longer terms justify "
            "higher bonus because the lessor's minerals are tied up longer. "
            "Step 3: Consider pairing longer terms with continuous drilling obligations that require "
            "the operator to drill within the first 2 years or release acreage. "
            "Step 4: Analyze extension provisions — some leases allow term extensions for additional "
            "consideration. These should be limited and require meaningful payment. "
            "Step 5: Ensure the lease clearly defines the primary term start date (execution vs. "
            "recording date). "
            "Step 6: Coordinate with Pugh clause to ensure undrilled acreage releases at end of "
            "primary term regardless of production on drilled portions."
        ),
        key_factors=[
            "Basin activity level and operator's development pace",
            "Bonus premium for longer terms",
            "Continuous drilling obligations that mitigate long-term risk",
            "Extension provisions and their cost",
            "Pugh clause interaction with primary term expiration",
            "Market competition for the specific acreage",
        ],
        primary_authority=[
            "Texas Natural Resources Code — lease term provisions",
            "Hydrocarbon Management Inc. v. Tracker Exploration, 861 S.W.2d 427 (Tex. App. 1993)",
            "AAPL Form 610 — primary term standards",
            "Samson Exploration v. T.S. Reed Props., 521 S.W.3d 766 (Tex. 2017)",
        ],
        burden_holder="Lessee must justify need for primary term exceeding 3 years",
        adversary_position=(
            "Lessee argues longer primary term is needed for proper geologic evaluation, "
            "permitting, and scheduling rig availability. Lessee may claim shorter terms "
            "create development pressure that leads to suboptimal well placement."
        ),
        counter_arguments=[
            "Active basin operators are drilling wells within 12-18 months of lease execution",
            "A 3-year term provides ample time for evaluation and permitting",
            "Longer terms without drilling obligations allow speculative lease holding",
            "Lessor's minerals are unproductive and generating no revenue during primary term",
            "Continuous drilling clause eliminates need for extended primary term",
        ],
        resolution_strategy=(
            "Default to 3-year primary term in active basins. Accept 5-year only with "
            "continuous drilling/development clause and enhanced bonus. Never accept 10-year "
            "terms in active play areas without extraordinary compensation."
        ),
        entity_scope="lessor_lessee",
        confidence="DEFENSIBLE",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Samson Exploration v. T.S. Reed (Tex. 2017)",
    )

    # =========================================================================
    # BLOCK 5: HABENDUM CLAUSE
    # =========================================================================
    blocks["habendum_clause"] = DoctrineBlock(
        topic="habendum_clause",
        keywords=["habendum", "so long thereafter", "production", "held by production", "hbp", "secondary term"],
        conclusion_template=(
            "The habendum clause creates the two-part lease duration: a fixed primary term and an "
            "indefinite secondary term lasting 'so long thereafter as oil or gas is produced.' The "
            "critical issue is defining what constitutes 'production' sufficient to maintain the lease. "
            "Modern practice requires clarifying whether marginal production, shut-in wells, or mere "
            "capability of production extends the lease. Lessors should insist on language requiring "
            "production in paying quantities to hold the lease."
        ),
        reasoning_framework=(
            "Step 1: Review the habendum language for the 'production' trigger. Traditional language "
            "('produced') requires actual physical production. 'Capable of producing' language is "
            "broader and less protective of the lessor. "
            "Step 2: Define 'paying quantities' — production sufficient to yield a profit to the "
            "operator over operating expenses, even though the drilling costs may never be recovered. "
            "Clifton v. Koontz standard in Texas. "
            "Step 3: Address the interaction between habendum and shut-in royalty clause — a shut-in "
            "well should not hold the entire lease indefinitely. "
            "Step 4: Consider adding minimum production thresholds to prevent holding by trivial "
            "production (e.g., one barrel per day on a 640-acre lease). "
            "Step 5: Clarify whether pooled production from off-lease wells can hold unpooled acreage. "
            "This is the function of the Pugh clause. "
            "Step 6: Ensure the habendum clause works in conjunction with the cessation of production "
            "clause and continuous drilling clause."
        ),
        key_factors=[
            "Definition of 'production' — actual vs. capable of producing",
            "Paying quantities standard (Clifton v. Koontz)",
            "Shut-in royalty clause interaction",
            "Minimum production thresholds",
            "Pooled production holding unpooled acreage (Pugh clause)",
            "Cessation of production savings clause interaction",
        ],
        primary_authority=[
            "Clifton v. Koontz, 160 Tex. 82, 325 S.W.2d 684 (1959) — paying quantities defined",
            "Hydrocarbon Management v. Tracker Exploration, 861 S.W.2d 427 (Tex. App. 1993)",
            "Anadarko v. Thompson, 94 S.W.3d 550 (Tex. 2002) — production requirements",
            "Garcia v. King, 139 Tex. 578, 164 S.W.2d 509 (1942)",
        ],
        burden_holder="Lessee bears burden of demonstrating production in paying quantities",
        adversary_position=(
            "Lessee argues that 'capable of producing' language is necessary to protect against "
            "temporary market conditions and that strict production requirements would cause "
            "premature lease termination."
        ),
        counter_arguments=[
            "Paying quantities is well-established Texas law — not onerous for active operators",
            "Capable of producing language allows indefinite holding without revenue to lessor",
            "Shut-in and cessation clauses provide adequate protection for temporary interruptions",
            "Minimum production thresholds prevent holding leases with trivial production",
            "Lessor receives no benefit from a lease held by non-productive operations",
        ],
        resolution_strategy=(
            "Insist on 'produced in paying quantities' language. Add minimum production "
            "thresholds where appropriate. Coordinate habendum with Pugh, shut-in, and "
            "cessation clauses for comprehensive protection."
        ),
        entity_scope="lessor_lessee",
        confidence="DEFENSIBLE",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Clifton v. Koontz (Tex. 1959)",
    )

    # =========================================================================
    # BLOCK 6: CONTINUOUS DRILLING CLAUSE
    # =========================================================================
    blocks["continuous_drilling_clause"] = DoctrineBlock(
        topic="continuous_drilling_clause",
        keywords=["continuous drilling", "continuous development", "drill or release", "development obligation", "cdc"],
        conclusion_template=(
            "Continuous drilling clauses require the operator to maintain an ongoing drilling program "
            "or release undrilled acreage. These clauses are critical for lessors with large acreage "
            "positions to prevent operators from holding acreage without development. A well-drafted "
            "CDC specifies: maximum gap between wells (90-180 days), minimum number of wells per year, "
            "acreage release for non-compliance, and clear commencement/completion definitions."
        ),
        reasoning_framework=(
            "Step 1: Determine the appropriate drilling cadence for the acreage size and geologic "
            "potential. Standard: one well per 640-acre section per year, or one well every 120-180 days. "
            "Step 2: Define 'continuous' with specificity — maximum number of days between rig release "
            "on one well and spudding the next. Industry standard: 120-180 days. "
            "Step 3: Specify consequences of non-compliance — partial release of undrilled acreage, "
            "not merely a right to extend by paying additional consideration. "
            "Step 4: Define what counts as 'drilling operations' — spudding, actual drilling, "
            "completion, not merely permitting or site preparation. "
            "Step 5: Address force majeure exceptions narrowly — weather, regulatory delays, equipment "
            "failure are legitimate; low commodity prices and corporate budget decisions are not. "
            "Step 6: Include anti-gaming provisions — operator cannot satisfy CDC by drilling shallow "
            "test wells or partial completions."
        ),
        key_factors=[
            "Acreage size and number of potential drilling locations",
            "Maximum gap between drilling operations (days)",
            "Consequence of non-compliance (acreage release vs. penalty)",
            "Definition of drilling operations",
            "Force majeure exceptions scope",
            "Anti-gaming provisions against shallow or sham wells",
        ],
        primary_authority=[
            "Hydrocarbon Management v. Tracker Exploration (Tex. App. 1993)",
            "Samson Exploration v. T.S. Reed Properties (Tex. 2017)",
            "ConocoPhillips Co. v. Koopmann, 547 S.W.3d 858 (Tex. 2018)",
            "AAPL Form 610 — development obligations",
        ],
        burden_holder="Lessee must demonstrate compliance with continuous drilling obligations",
        adversary_position=(
            "Lessee argues rigid drilling schedules prevent optimal well placement and may force "
            "uneconomic drilling during commodity price downturns."
        ),
        counter_arguments=[
            "CDC ensures the lessor's minerals are actively developed, not warehoused",
            "180-day gaps provide ample flexibility for scheduling and weather",
            "Acreage release for non-compliance is fair — operator keeps drilled acreage",
            "Without CDC, operators can hold thousands of acres with a single well",
            "Lessors cannot market undrilled acreage held under an undeveloped lease",
        ],
        resolution_strategy=(
            "Insist on CDC for any lease exceeding 640 acres. Set drilling gap at 120-180 days. "
            "Require automatic acreage release for non-compliance. Limit force majeure to genuine "
            "operational interruptions, not economic decisions."
        ),
        entity_scope="lessor_lessee",
        confidence="DEFENSIBLE",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="ConocoPhillips v. Koopmann (Tex. 2018)",
    )

    # =========================================================================
    # BLOCK 7: PUGH CLAUSE (VERTICAL AND HORIZONTAL)
    # =========================================================================
    blocks["pugh_clause"] = DoctrineBlock(
        topic="pugh_clause",
        keywords=["pugh", "pugh clause", "vertical pugh", "horizontal pugh", "depth severance", "acreage release", "freestone rider"],
        conclusion_template=(
            "The Pugh clause prevents production from one well or one depth from holding the entire "
            "lease. Horizontal Pugh releases undrilled surface acreage at the end of the primary term; "
            "vertical Pugh releases unproduced depths. Both are essential in horizontal drilling areas "
            "where a single well in one zone could otherwise hold rights to all depths across the "
            "entire lease. Named after Lawrence Pugh of Shreveport, this is the most important "
            "acreage-protection provision a lessor can negotiate."
        ),
        reasoning_framework=(
            "Step 1: Draft horizontal Pugh to release all surface acreage not included in a producing "
            "unit at the expiration of the primary term. Key: the release is automatic, not discretionary. "
            "Step 2: Draft vertical Pugh to release all depths not being produced at primary term "
            "expiration. In the Permian, this separates Wolfcamp A/B from Spraberry, Bone Spring, etc. "
            "Step 3: Define the depth limitation precisely — typically 100 feet below the deepest "
            "perforations in a producing well. "
            "Step 4: Address interaction with pooling — production from a pooled unit should only hold "
            "the pooled acreage, not unpooled portions of the lease. "
            "Step 5: Specify that acreage releases under Pugh are permanent and the released acreage "
            "reverts to the lessor free of the lease. "
            "Step 6: Include both vertical AND horizontal Pugh — many operators will accept one but "
            "resist the other. Both are necessary for complete protection."
        ),
        key_factors=[
            "Horizontal Pugh: releases undrilled surface acreage",
            "Vertical Pugh: releases unproduced depths",
            "Automatic vs. discretionary release mechanism",
            "Depth buffer below deepest perforations (100 ft standard)",
            "Interaction with pooling declarations",
            "Permanence of released acreage",
            "Application to both primary term expiration and HBP operations",
        ],
        primary_authority=[
            "Pugh v. Wm. Cameron & Co., referenced in LA jurisprudence",
            "ConocoPhillips v. Koopmann, 547 S.W.3d 858 (Tex. 2018)",
            "AAPL Form 610 — Pugh clause provisions",
            "Samson Exploration v. T.S. Reed (Tex. 2017)",
            "Morrison v. Oil States Energy, 360 S.W.3d 153 (Tex. App. 2012)",
        ],
        burden_holder="Lessor must affirmatively include Pugh language; most printed forms omit it",
        adversary_position=(
            "Lessee resists Pugh clauses because they limit the ability to hold large acreage "
            "blocks with minimal production. Lessee argues that exploration requires holding "
            "multiple horizons and contiguous acreage."
        ),
        counter_arguments=[
            "Without Pugh, a single Wolfcamp well can hold Spraberry, Bone Spring, and all other depths",
            "Horizontal drilling means one wellbore affects only a narrow strip of the total acreage",
            "Released acreage can be re-leased, giving the lessor new bonus and better terms",
            "Operators have no legitimate need to hold undrilled depths indefinitely",
            "Both vertical and horizontal Pugh are now standard in sophisticated mineral owner leases",
        ],
        resolution_strategy=(
            "Non-negotiable for any lease over 160 acres. Include both vertical and horizontal "
            "Pugh. Ensure automatic release, not operator-discretionary. Define depth buffer "
            "at 100 feet below deepest perforations."
        ),
        entity_scope="lessor_lessee",
        confidence="DEFENSIBLE",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="ConocoPhillips v. Koopmann (Tex. 2018)",
    )

    # =========================================================================
    # BLOCK 8: SURFACE USE PROVISIONS
    # =========================================================================
    blocks["surface_use_provisions"] = DoctrineBlock(
        topic="surface_use_provisions",
        keywords=["surface", "surface use", "surface damage", "restoration", "location", "accommodation", "surface owner"],
        conclusion_template=(
            "Surface use provisions balance the mineral estate's dominant right to use the surface "
            "for mineral development against the surface owner's right to continued use and enjoyment. "
            "Key provisions include surface damage payments, location approval rights, restoration "
            "obligations, water use restrictions, and road maintenance. The accommodation doctrine "
            "requires mineral developers to accommodate existing surface uses where alternative "
            "methods are available at reasonable cost."
        ),
        reasoning_framework=(
            "Step 1: Determine surface ownership — is the lessor also the surface owner? If mineral "
            "and surface are severed, surface protections benefit a different party. "
            "Step 2: Negotiate surface damage payment schedule: per-acre compensation for pad sites, "
            "road construction, pipeline easements, water well damages. "
            "Step 3: Include location approval provision — operator must present proposed well pad "
            "location for surface owner approval with 30-day review period. "
            "Step 4: Require restoration obligations — operator must restore surface to original "
            "contour and vegetation within specified time after operations cease. "
            "Step 5: Address water use — operator must not use surface water sources or groundwater "
            "from surface owner's wells without separate agreement. "
            "Step 6: Include setback requirements from residences, barns, livestock facilities. "
            "Step 7: Require operator to maintain access roads and gates."
        ),
        key_factors=[
            "Surface and mineral ownership alignment",
            "Surface damage payment schedule and amounts",
            "Location approval rights and review period",
            "Restoration obligations and timeline",
            "Water use restrictions",
            "Setback requirements from improvements",
            "Road and fence maintenance obligations",
            "Insurance and indemnification requirements",
        ],
        primary_authority=[
            "Getty Oil Co. v. Jones, 470 S.W.2d 618 (Tex. 1971) — accommodation doctrine",
            "Texas Natural Resources Code §§ 91.401-91.455 — surface owner protections",
            "Merriman v. XTO Energy, 407 S.W.3d 244 (Tex. 2013)",
            "Lightning Oil Co. v. Anadarko E&P Onshore, 520 S.W.3d 39 (Tex. 2017)",
        ],
        burden_holder="Mineral developer must accommodate existing surface uses where feasible",
        adversary_position=(
            "Lessee argues that the mineral estate is dominant and surface restrictions impede "
            "efficient mineral development, increasing costs passed through to the lessor."
        ),
        counter_arguments=[
            "Accommodation doctrine is settled Texas law — operators must accommodate surface uses",
            "Modern directional drilling allows flexible well pad placement",
            "Surface damage payments are a standard cost of doing business",
            "Unrestored sites create long-term liability for both parties",
            "Surface protections encourage cooperative lessor-operator relationships",
        ],
        resolution_strategy=(
            "Include comprehensive surface use addendum with specific payment schedules, "
            "location approval rights, restoration obligations, and water use restrictions. "
            "Reference the accommodation doctrine as baseline protection."
        ),
        entity_scope="surface_owner_operator",
        confidence="DEFENSIBLE",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Getty Oil v. Jones (Tex. 1971) — accommodation doctrine",
    )

    # =========================================================================
    # BLOCK 9: POOLING AND UNITIZATION
    # =========================================================================
    blocks["pooling_unitization"] = DoctrineBlock(
        topic="pooling_unitization",
        keywords=["pooling", "unitization", "force pooling", "voluntary", "community lease", "spacing", "proration unit"],
        conclusion_template=(
            "Pooling and unitization clauses authorize the operator to combine the leased acreage "
            "with other tracts for drilling and regulatory purposes. Unrestricted pooling authority "
            "is dangerous for lessors because the operator can dilute the lessor's interest by "
            "creating oversized units. Lessors should limit maximum pooling unit size, require "
            "notice and consent, and ensure proportionate royalty allocation."
        ),
        reasoning_framework=(
            "Step 1: Distinguish pooling (combining tracts for a single well) from unitization "
            "(combining tracts for enhanced recovery or field-wide operations). "
            "Step 2: Limit maximum unit size — for horizontal wells in Texas, 640 acres for oil "
            "and 640 acres for gas is standard RRC spacing. Prohibit units exceeding state spacing "
            "requirements plus a reasonable buffer (e.g., 640 acres + 10%). "
            "Step 3: Require advance written notice of pooling declarations — 30 days minimum. "
            "Step 4: Negotiate right to exclude acreage from pooling (Pugh clause integration). "
            "Step 5: Address force pooling risk — in Texas, the RRC can force-pool uncommitted "
            "interests under Tex. Nat. Res. Code §102.012. Ensure lease pooling terms are at least "
            "as favorable as statutory terms. "
            "Step 6: Require that pooling declarations be recorded in county deed records. "
            "Step 7: Include anti-gerrymandering provisions — units must be reasonably configured."
        ),
        key_factors=[
            "Maximum unit size limitations",
            "Notice and consent requirements",
            "Pugh clause interaction with pooled vs. unpooled acreage",
            "Force pooling risk under state law",
            "Proportionate royalty allocation method",
            "Unit configuration anti-gerrymandering",
            "Recording requirements for pooling declarations",
        ],
        primary_authority=[
            "Texas Natural Resources Code §102.012 — force pooling",
            "Jones v. Killingsworth, 403 S.W.2d 325 (Tex. 1966)",
            "AAPL Form 610 — pooling provisions",
            "Wagner & Brown v. Sheppard, 282 S.W.3d 419 (Tex. 2008)",
        ],
        burden_holder="Lessee must justify pooling unit configuration and size",
        adversary_position=(
            "Lessee needs pooling flexibility to create efficient drilling units and comply "
            "with RRC spacing rules. Restrictions on pooling may prevent optimal well placement."
        ),
        counter_arguments=[
            "Unrestricted pooling allows operators to dilute lessor royalty across oversized units",
            "Limiting unit size to RRC spacing requirements is reasonable",
            "Notice requirements allow lessor to verify proper pooling allocation",
            "Pugh clause ensures unpooled acreage is not held by pooled production",
            "Anti-gerrymandering prevents cherry-picking the most productive acreage into units",
        ],
        resolution_strategy=(
            "Limit pooling to state spacing requirements plus 10% buffer. Require 30-day "
            "advance notice. Include Pugh clause for unpooled acreage. Prohibit unitization "
            "without lessor consent."
        ),
        entity_scope="lessor_lessee",
        confidence="DEFENSIBLE",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Wagner & Brown v. Sheppard (Tex. 2008)",
    )

    # =========================================================================
    # BLOCK 10: SHUT-IN ROYALTY
    # =========================================================================
    blocks["shut_in_royalty"] = DoctrineBlock(
        topic="shut_in_royalty",
        keywords=["shut-in", "shut in royalty", "capable of producing", "no market", "gas well"],
        conclusion_template=(
            "Shut-in royalty clauses allow operators to maintain the lease when a well is capable "
            "of production but is shut-in due to lack of market, pipeline connection, or operational "
            "necessity. Without this clause, the lease would terminate if production ceased. Lessors "
            "should limit shut-in duration (maximum 2 years cumulative), require meaningful shut-in "
            "payments ($X/acre/year), and restrict the clause to genuinely unmarketable gas wells."
        ),
        reasoning_framework=(
            "Step 1: Define the triggering condition narrowly — shut-in royalty should only apply "
            "when a well is capable of producing in paying quantities but cannot be produced due to "
            "lack of pipeline connection or market. Economic shut-ins (low prices) should not qualify. "
            "Step 2: Set meaningful shut-in royalty payments — at minimum, equal to the delay rental "
            "amount per acre per year. This creates economic incentive to restore production. "
            "Step 3: Limit cumulative shut-in duration — 2 years maximum. If the well remains shut-in "
            "beyond this period, the lease terminates as to that well. "
            "Step 4: Require operator to provide written notice of shut-in status and reason. "
            "Step 5: Limit the scope — shut-in royalty should only hold the acreage within the "
            "producing unit, not the entire lease (Pugh clause coordination). "
            "Step 6: Specify payment timing — shut-in royalty must be paid on or before the shut-in "
            "anniversary date; failure to pay timely terminates the lease."
        ),
        key_factors=[
            "Triggering conditions — narrow vs. broad shut-in definition",
            "Shut-in royalty payment amount and timing",
            "Maximum cumulative shut-in duration",
            "Notice requirements",
            "Scope of acreage held by shut-in payments",
            "Economic shut-in exclusion",
            "Payment deadline enforcement",
        ],
        primary_authority=[
            "Freeman v. Magnolia Petroleum Co., 141 Tex. 274, 171 S.W.2d 339 (1943)",
            "Hydrocarbon Management v. Tracker Exploration (Tex. App. 1993)",
            "Anadarko v. Thompson, 94 S.W.3d 550 (Tex. 2002)",
            "Pack v. Santa Fe Minerals, 869 P.2d 323 (Okla. 1994)",
        ],
        burden_holder="Lessee must demonstrate well is capable of producing and shut-in is justified",
        adversary_position=(
            "Lessee needs shut-in flexibility to manage wells during pipeline construction, "
            "market disruptions, and temporary operational issues without lease termination risk."
        ),
        counter_arguments=[
            "Unlimited shut-in allows operators to hold leases indefinitely without production",
            "Meaningful shut-in payments incentivize returning wells to production",
            "2-year cumulative limit is ample time to arrange pipeline connection or market",
            "Economic shut-ins are business decisions, not force majeure events",
            "Narrow triggering conditions prevent abuse of the clause",
        ],
        resolution_strategy=(
            "Accept shut-in royalty clause only with: (1) narrow triggering conditions, "
            "(2) meaningful payment amounts, (3) 2-year cumulative maximum, (4) written "
            "notice requirement, and (5) Pugh clause coordination."
        ),
        entity_scope="lessor_lessee",
        confidence="DEFENSIBLE",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Freeman v. Magnolia Petroleum (Tex. 1943)",
    )

    # =========================================================================
    # BLOCK 11: CESSATION OF PRODUCTION
    # =========================================================================
    blocks["cessation_of_production"] = DoctrineBlock(
        topic="cessation_of_production",
        keywords=["cessation", "temporary cessation", "savings clause", "sixty-day", "ninety-day", "production interruption"],
        conclusion_template=(
            "Cessation of production clauses define what happens when production stops after the "
            "primary term. Without a savings clause, even brief cessation could terminate the lease "
            "under strict habendum interpretation. Most leases include a 60 or 90-day cessation "
            "clause allowing the operator to resume operations. Lessors should limit cessation "
            "periods, require active remediation, and cap the number of cessation events."
        ),
        reasoning_framework=(
            "Step 1: Define cessation trigger — total cessation of all production from all wells "
            "on the lease, not merely reduction in production rates. "
            "Step 2: Set the savings period — 60 days is lessor-favorable; 90 days is standard; "
            "180 days is operator-favorable. 60-90 days is recommended. "
            "Step 3: Require the operator to commence reworking or drilling operations within the "
            "savings period, not merely express intent to do so. "
            "Step 4: Define what constitutes resumption — actual production, not merely workover "
            "operations that do not result in production. "
            "Step 5: Limit the number of cessation events — a well that repeatedly ceases and "
            "resumes marginal production is not serving the lessor's interests. Cap at 2-3 events. "
            "Step 6: Coordinate with shut-in royalty clause — if a well is shut-in, the shut-in "
            "clause governs; if production ceases entirely, the cessation clause governs."
        ),
        key_factors=[
            "Length of savings period (60-180 days)",
            "Definition of operations required to save the lease",
            "Distinction between total cessation and production decline",
            "Maximum number of cessation events",
            "Interaction with shut-in royalty clause",
            "Requirement for actual production resumption vs. mere operations",
        ],
        primary_authority=[
            "Watson v. Rochmill, 137 Tex. 565, 155 S.W.2d 783 (1941)",
            "Midwest Oil Corp. v. Winsauer, 159 Tex. 560, 323 S.W.2d 944 (1959)",
            "Anadarko v. Thompson, 94 S.W.3d 550 (Tex. 2002)",
            "Garcia v. King, 139 Tex. 578, 164 S.W.2d 509 (1942)",
        ],
        burden_holder="Lessee must commence operations within the savings period or lease terminates",
        adversary_position=(
            "Lessee needs reasonable cessation periods to handle equipment failures, "
            "weather events, and market disruptions without lease termination."
        ),
        counter_arguments=[
            "90-day cessation period is ample for any legitimate operational interruption",
            "Repeated cessations indicate a marginal well that should be released",
            "Operations must result in actual production, not perpetual reworking",
            "Lessor receives no revenue during cessation periods",
            "Shorter cessation periods incentivize prompt attention to production issues",
        ],
        resolution_strategy=(
            "Set cessation savings period at 60-90 days. Require commencement of actual "
            "drilling or reworking operations. Cap cessation events at 3 per well. "
            "Ensure lease terminates if operations do not result in production."
        ),
        entity_scope="lessor_lessee",
        confidence="DEFENSIBLE",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Watson v. Rochmill (Tex. 1941)",
    )

    # =========================================================================
    # BLOCK 12: DEPTH LIMITATION
    # =========================================================================
    blocks["depth_limitation"] = DoctrineBlock(
        topic="depth_limitation",
        keywords=["depth", "depth limitation", "shallow rights", "deep rights", "depth severance", "retained acreage"],
        conclusion_template=(
            "Depth limitation clauses restrict the lease to specific geological formations or depth "
            "ranges. This allows the lessor to retain deep rights for separate leasing and prevents "
            "operators from holding formations they have no intention of developing. In the Permian "
            "Basin, depth limitations are critical because multiple productive horizons (Wolfcamp, "
            "Spraberry, Bone Spring, Cline, Devonian, Ellenburger) exist at different depths."
        ),
        reasoning_framework=(
            "Step 1: Identify the target formations for the operator's drilling program. Most Permian "
            "operators target Wolfcamp A/B and Spraberry. "
            "Step 2: Set the depth limitation at a specific footage below the deepest target formation "
            "or below the deepest perforations in any well drilled. Standard: 100 feet below deepest "
            "completed interval. "
            "Step 3: Alternatively, specify formations by name: 'This lease covers the Wolfcamp and "
            "Spraberry formations only.' Formation-specific language is clearer but may miss intervals. "
            "Step 4: Coordinate with vertical Pugh clause — unproduced depths should release at "
            "primary term expiration even if the shallow depths are producing. "
            "Step 5: Address wellbore rights — does the operator retain the right to use the wellbore "
            "through released depths for production from retained depths? Usually yes, with restrictions. "
            "Step 6: Ensure depth limitation applies to both primary and secondary term."
        ),
        key_factors=[
            "Target formations and depth ranges",
            "Footage-based vs. formation-based depth limitation",
            "Vertical Pugh clause coordination",
            "Wellbore access rights through released depths",
            "Multiple horizon development potential",
            "Application in primary and secondary term",
        ],
        primary_authority=[
            "French v. Chevron, 896 S.W.2d 795 (Tex. App. 1995)",
            "ConocoPhillips v. Koopmann, 547 S.W.3d 858 (Tex. 2018)",
            "AAPL Form 610 — depth limitation provisions",
            "Samson Exploration v. T.S. Reed (Tex. 2017)",
        ],
        burden_holder="Lessor must negotiate depth limitation; default lease language covers all depths",
        adversary_position=(
            "Lessee wants access to all depths for future development potential and argues "
            "that depth restrictions fragment the mineral estate and complicate operations."
        ),
        counter_arguments=[
            "Operators typically target 1-2 formations; holding all depths is speculative",
            "Released deep rights can be separately leased at current market rates",
            "Depth limitations are standard in sophisticated mineral owner negotiations",
            "Vertical Pugh achieves similar result but depth limitation is more precise",
            "Operators have no legitimate need to hold formations they won't develop",
        ],
        resolution_strategy=(
            "Include depth limitation at 100 feet below the deepest target formation. "
            "Pair with vertical Pugh clause for redundant protection. Allow wellbore "
            "access through released depths for retained formation production."
        ),
        entity_scope="lessor_lessee",
        confidence="DEFENSIBLE",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="French v. Chevron (Tex. App. 1995)",
    )

    # =========================================================================
    # BLOCKS 13-22: ADDITIONAL DOCTRINE BLOCKS
    # =========================================================================

    blocks["release_provisions"] = DoctrineBlock(
        topic="release_provisions",
        keywords=["release", "partial release", "surrender", "termination", "expiration", "retained acreage"],
        conclusion_template=(
            "Release provisions define how the lease terminates and what acreage reverts to the "
            "lessor. A well-drafted release provision requires the operator to promptly execute "
            "and record a release of any acreage no longer held by production, operations, or "
            "other lease terms. Lessors should include automatic release language for acreage "
            "not held at primary term expiration and require operator to pay recording fees."
        ),
        reasoning_framework=(
            "Step 1: Include automatic release of unproductive acreage at primary term expiration. "
            "Step 2: Require operator to execute and record a partial release within 60 days of "
            "acreage becoming unencumbered. Step 3: If operator fails to record release, lessor "
            "should have right to execute an affidavit of lease termination. Step 4: Operator pays "
            "all recording fees. Step 5: Coordinate with Pugh clause releases."
        ),
        key_factors=[
            "Automatic vs. discretionary release mechanism",
            "Timeline for recording releases (60-day standard)",
            "Lessor's right to record affidavit of termination",
            "Recording fee responsibility",
            "Pugh clause release coordination",
        ],
        primary_authority=[
            "Texas Property Code §5.001 — recording requirements",
            "Wagner & Brown v. Sheppard, 282 S.W.3d 419 (Tex. 2008)",
            "ConocoPhillips v. Koopmann (Tex. 2018)",
        ],
        burden_holder="Operator must promptly execute and record releases",
        adversary_position="Lessee may resist automatic releases claiming administrative complexity.",
        counter_arguments=[
            "Unreleased leases cloud title and prevent lessor from re-leasing",
            "60-day recording deadline is commercially reasonable",
            "Automatic release eliminates disputes over lease termination",
            "Lessor affidavit right provides self-help remedy",
            "Recording fees are minimal and appropriate lessee expense",
        ],
        resolution_strategy="Include automatic release with 60-day recording deadline and lessor affidavit right.",
        entity_scope="lessor_lessee",
        confidence="DEFENSIBLE",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Wagner & Brown v. Sheppard (Tex. 2008)",
    )

    blocks["assignment_restrictions"] = DoctrineBlock(
        topic="assignment_restrictions",
        keywords=["assignment", "transfer", "consent", "rofr", "right of first refusal", "change of operator"],
        conclusion_template=(
            "Assignment restrictions protect the lessor against the lease being transferred to "
            "less capable or less creditworthy operators. While absolute assignment prohibitions "
            "are generally unenforceable, reasonable restrictions such as notice requirements, "
            "consent-not-unreasonably-withheld provisions, and financial qualification standards "
            "are common and enforceable."
        ),
        reasoning_framework=(
            "Step 1: Require advance written notice (30 days) of any assignment. Step 2: Include "
            "consent-not-unreasonably-withheld provision for operating interest assignments. "
            "Step 3: Define reasonable grounds for withholding consent: financial inadequacy, "
            "environmental violations, poor operational track record. Step 4: Consider right of "
            "first refusal on proposed sales. Step 5: Require assignee to assume all lease obligations."
        ),
        key_factors=[
            "Notice requirements for assignments",
            "Consent standard (not unreasonably withheld)",
            "Financial qualification criteria",
            "Environmental and operational track record",
            "ROFR on proposed sales",
            "Assignee assumption of obligations",
        ],
        primary_authority=[
            "Texas Property Code — assignment restrictions",
            "In re El Paso Refinery, LP, 302 F.3d 343 (5th Cir. 2002)",
            "AAPL Form 610 — assignment provisions",
        ],
        burden_holder="Lessor must include assignment restrictions affirmatively",
        adversary_position="Lessee needs assignment flexibility for farmouts, corporate transactions, and capital recycling.",
        counter_arguments=[
            "Notice and consent provisions are standard in commercial leases",
            "Financial qualification prevents lease transfer to undercapitalized operators",
            "ROFR gives lessor opportunity to reacquire favorable lease position",
            "Assignee assumption of obligations protects lessor from orphaned wells",
            "Reasonable restrictions do not prevent legitimate assignments",
        ],
        resolution_strategy="Include notice + consent-not-unreasonably-withheld + financial qualifications + ROFR.",
        entity_scope="lessor_lessee",
        confidence="DEFENSIBLE",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="In re El Paso Refinery (5th Cir. 2002)",
    )

    blocks["environmental_indemnification"] = DoctrineBlock(
        topic="environmental_indemnification",
        keywords=["environmental", "indemnification", "liability", "remediation", "plugging", "contamination"],
        conclusion_template=(
            "Environmental indemnification clauses allocate liability for environmental contamination "
            "caused by lease operations. The operator should indemnify the lessor against all "
            "environmental claims arising from the operator's activities, including well plugging, "
            "site remediation, produced water disposal, and tank battery spills. This protection is "
            "critical as environmental cleanup costs can exceed the value of the mineral estate."
        ),
        reasoning_framework=(
            "Step 1: Require operator indemnification for all environmental claims arising from "
            "operations. Step 2: Include plugging obligation with specific timeline. Step 3: Require "
            "operator to maintain environmental insurance. Step 4: Address produced water disposal "
            "and saltwater contamination. Step 5: Include post-termination cleanup obligations."
        ),
        key_factors=[
            "Scope of indemnification (operations-related contamination)",
            "Well plugging timeline and financial assurance",
            "Environmental insurance requirements",
            "Produced water disposal compliance",
            "Post-termination cleanup obligations",
            "Survival of indemnification after lease termination",
        ],
        primary_authority=[
            "Texas Natural Resources Code §89.001 et seq. — well plugging requirements",
            "CERCLA 42 U.S.C. §9601 et seq. — federal environmental liability",
            "Texas Water Code Ch. 26 — water pollution control",
            "Railroad Commission of Texas Statewide Rule 14(b)(2)",
        ],
        burden_holder="Operator bears responsibility for environmental compliance and remediation",
        adversary_position="Lessee may seek to limit indemnification to gross negligence or willful misconduct.",
        counter_arguments=[
            "Strict liability applies to environmental contamination regardless of fault",
            "Operator controls all operations and is best positioned to prevent contamination",
            "Environmental cleanup costs can be catastrophic for mineral owners",
            "Insurance is available and a reasonable cost of operations",
            "Indemnification must survive lease termination for post-operations contamination",
        ],
        resolution_strategy="Require comprehensive environmental indemnification surviving lease termination with insurance requirements.",
        entity_scope="lessor_lessee",
        confidence="DEFENSIBLE",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="CERCLA 42 U.S.C. §9601 — strict environmental liability",
    )

    blocks["audit_rights"] = DoctrineBlock(
        topic="audit_rights",
        keywords=["audit", "records", "books", "inspection", "accounting", "royalty verification"],
        conclusion_template=(
            "Audit rights provisions give the lessor access to the operator's production records, "
            "sales contracts, and royalty calculations to verify that royalties are being properly "
            "computed and paid. Without audit rights, the lessor has no ability to detect underpayment. "
            "Audit provisions should include the right to inspect records at reasonable times, copy "
            "relevant documents, and recover audit costs if underpayment exceeds a threshold."
        ),
        reasoning_framework=(
            "Step 1: Include express right to audit operator's books and records relating to "
            "production volumes, sales prices, and royalty calculations. Step 2: Allow audit by "
            "lessor's designated representative (CPA, petroleum engineer). Step 3: Require operator "
            "to retain records for minimum 5 years. Step 4: If audit reveals underpayment exceeding "
            "5%, operator pays audit costs and interest on underpayment. Step 5: Include right to "
            "access gas purchase contracts and midstream agreements."
        ),
        key_factors=[
            "Express audit right in lease language",
            "Scope of records access",
            "Record retention period (5+ years)",
            "Audit cost recovery threshold",
            "Interest on underpayments",
            "Access to third-party contracts",
        ],
        primary_authority=[
            "Texas Natural Resources Code — royalty reporting requirements",
            "Chesapeake Exploration v. Hyder (Tex. 2016)",
            "AAPL Form 610 — accounting provisions",
        ],
        burden_holder="Lessor must include audit rights affirmatively in the lease",
        adversary_position="Lessee resists audit rights citing administrative burden and confidential contract terms.",
        counter_arguments=[
            "Lessor cannot verify royalty accuracy without records access",
            "Industry audits routinely discover 5-15% underpayment",
            "5-year record retention is standard business practice",
            "Audit cost recovery creates incentive for accurate royalty payment",
            "Confidentiality agreements can protect sensitive contract terms",
        ],
        resolution_strategy="Include comprehensive audit rights with cost recovery for underpayments exceeding 5%.",
        entity_scope="lessor_lessee",
        confidence="DEFENSIBLE",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Chesapeake v. Hyder (Tex. 2016)",
    )

    blocks["commencement_of_drilling"] = DoctrineBlock(
        topic="commencement_of_drilling",
        keywords=["commencement", "drilling operations", "spud", "spudding", "operations definition"],
        conclusion_template=(
            "The definition of 'commencement of drilling operations' determines when the lease is "
            "saved from expiration at the end of the primary term. Strict definition requires actual "
            "spudding of a well. Liberal definition may include site preparation, road building, or "
            "even obtaining permits. Lessors should insist on a strict definition requiring actual "
            "penetration of the surface with a drilling bit."
        ),
        reasoning_framework=(
            "Step 1: Define commencement as actual drilling — penetration of the surface with a bit "
            "affixed to a drilling rig. Step 2: Exclude preparatory activities: surveying, staking, "
            "road building, pad construction, permitting. Step 3: Require commencement within the "
            "primary term, not merely before expiration. Step 4: Set minimum drilling progress "
            "requirement (e.g., reach X depth within 90 days of commencement). Step 5: Address "
            "the scenario where drilling commences but well is not completed."
        ),
        key_factors=[
            "Strict vs. liberal definition of commencement",
            "Exclusion of preparatory activities",
            "Minimum drilling progress requirements",
            "Completion requirements after commencement",
            "Good faith drilling obligation",
        ],
        primary_authority=[
            "Hydrocarbon Management v. Tracker Exploration (Tex. App. 1993)",
            "Skelly Oil Co. v. Archer County, 356 S.W.2d 774 (Tex. 1961)",
            "Rogers v. Ricane Enterprises, 772 S.W.2d 76 (Tex. 1989)",
        ],
        burden_holder="Lessee must demonstrate actual commencement of drilling operations",
        adversary_position="Lessee wants broad commencement definition to include preparatory work.",
        counter_arguments=[
            "Only actual drilling demonstrates genuine intent to develop",
            "Preparatory activities can be commenced and abandoned without meaningful commitment",
            "Strict commencement definition is standard in negotiated leases",
            "Lessor should not have lease term extended by road building alone",
            "Good faith requirement prevents sham commencement near primary term expiration",
        ],
        resolution_strategy="Define commencement as actual spudding. Require continuous drilling to completion.",
        entity_scope="lessor_lessee",
        confidence="DEFENSIBLE",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Skelly Oil v. Archer County (Tex. 1961)",
    )

    blocks["operations_clause"] = DoctrineBlock(
        topic="operations_clause",
        keywords=["operations", "operations clause", "substitute", "reworking", "workover", "recompleting"],
        conclusion_template=(
            "The operations clause defines activities that substitute for actual production to "
            "maintain the lease. These include reworking, deepening, plugging back, sidetracking, "
            "or conducting other operations. Lessors should require operations to be conducted in "
            "good faith with reasonable prospect of restoring or obtaining production, and should "
            "limit the duration of non-productive operations."
        ),
        reasoning_framework=(
            "Step 1: Define permissible substitute operations: reworking, deepening, recompleting, "
            "plugging back, sidetracking. Step 2: Require good faith pursuit of production — "
            "operations must have reasonable prospect of obtaining or restoring production. "
            "Step 3: Limit continuous non-productive operations to 180 days. Step 4: Require operator "
            "to give notice of substitute operations. Step 5: Exclude mere maintenance or monitoring."
        ),
        key_factors=[
            "Types of permissible substitute operations",
            "Good faith requirement",
            "Maximum duration of non-productive operations",
            "Notice requirements",
            "Exclusion of maintenance activities",
        ],
        primary_authority=[
            "Midwest Oil Corp. v. Winsauer, 323 S.W.2d 944 (Tex. 1959)",
            "Rogers v. Ricane Enterprises (Tex. 1989)",
            "Garcia v. King, 164 S.W.2d 509 (Tex. 1942)",
        ],
        burden_holder="Lessee must conduct operations in good faith with production prospects",
        adversary_position="Lessee wants broad operations definition to maintain maximum flexibility.",
        counter_arguments=[
            "Perpetual non-productive operations are not beneficial to the lessor",
            "Good faith requirement is a reasonable standard",
            "180-day limit provides ample time for legitimate operations",
            "Notice allows lessor to monitor operator's activities",
            "Maintenance alone should not extend the lease indefinitely",
        ],
        resolution_strategy="Accept operations clause with good faith requirement, 180-day limit, and notice.",
        entity_scope="lessor_lessee",
        confidence="DEFENSIBLE",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Midwest Oil v. Winsauer (Tex. 1959)",
    )

    blocks["top_lease_strategy"] = DoctrineBlock(
        topic="top_lease_strategy",
        keywords=["top lease", "top leasing", "expiring lease", "renewal", "replacement", "future interest"],
        conclusion_template=(
            "Top leasing is the practice of executing a new lease that takes effect upon expiration "
            "or termination of an existing lease. This strategy allows mineral owners to lock in "
            "improved terms before the existing lease expires and creates competitive pressure on "
            "the current lessee. Top leases are valid future interests in Texas but carry risks "
            "including tortious interference claims and title complexity."
        ),
        reasoning_framework=(
            "Step 1: Verify that the existing lease is approaching expiration or has termination "
            "risks (e.g., production declining below paying quantities). Step 2: Negotiate top "
            "lease terms that are superior to the existing lease — higher royalty, cost-free "
            "language, Pugh clause, shorter term. Step 3: Address the commencement trigger — top "
            "lease commences 'upon expiration or termination of the existing lease.' Step 4: "
            "Consider partial top leases covering only depths or acreage not held by the existing "
            "lease. Step 5: Assess tortious interference risk if current lessee discovers top lease."
        ),
        key_factors=[
            "Status of existing lease (approaching expiration, production decline)",
            "Terms improvement over existing lease",
            "Commencement trigger language",
            "Partial vs. full top lease",
            "Tortious interference risk",
            "Title complexity and marketability impact",
        ],
        primary_authority=[
            "Morriss v. First National Bank of Mission, 249 S.W.2d 240 (Tex. App. 1952)",
            "Top leasing treatise: 8 Williams & Meyers, Oil and Gas Law §881",
            "Strata-G Corp. v. Zr Energy, 237 S.W.3d 429 (Tex. App. 2007)",
        ],
        burden_holder="Top lessee accepts risk that bottom lease may not terminate",
        adversary_position="Current lessee may claim tortious interference or assert lease remains valid.",
        counter_arguments=[
            "Top leasing is a recognized and legal practice in Texas",
            "Mineral owner has right to plan for lease expiration",
            "Top lease only takes effect upon bottom lease termination",
            "Competition from top lease creates incentive for current lessee to develop",
            "Mineral owner is not obligated to renew or extend existing lease",
        ],
        resolution_strategy="Execute top lease with superior terms when existing lease is within 12-18 months of expiration.",
        entity_scope="lessor_multiple_lessees",
        confidence="AGGRESSIVE",
        confidence_stratification="AGGRESSIVE",
        controlling_precedent="Morriss v. First National Bank (Tex. App. 1952)",
    )

    blocks["lease_amendment_extension"] = DoctrineBlock(
        topic="lease_amendment_extension",
        keywords=["amendment", "extension", "ratification", "renewal", "modification", "addendum"],
        conclusion_template=(
            "Lease amendments and extensions allow parties to modify existing lease terms without "
            "executing a new lease. Extensions are commonly requested by operators approaching "
            "primary term expiration without drilling. Lessors should treat extension requests as "
            "renegotiation opportunities — demanding improved terms (higher royalty, Pugh clause, "
            "cost-free language) as the price of extension."
        ),
        reasoning_framework=(
            "Step 1: Evaluate operator's request — is this a simple term extension, modification "
            "of specific clauses, or comprehensive lease update? Step 2: Treat every amendment "
            "as a negotiation opportunity. If operator wants extension, lessor wants improved terms. "
            "Step 3: Negotiate new bonus payment for extension period. Step 4: Update all clauses "
            "to current market standards. Step 5: Ensure the amendment is properly recorded."
        ),
        key_factors=[
            "Type of amendment requested",
            "Operator's leverage (expiration proximity, competing offers)",
            "Additional consideration for extension",
            "Clause updates to current market standards",
            "Recording requirements",
        ],
        primary_authority=[
            "Texas Property Code — amendment and modification requirements",
            "AAPL Form 610 — lease modification provisions",
            "Rogers v. Ricane Enterprises (Tex. 1989)",
        ],
        burden_holder="Operator requesting amendment bears burden of providing consideration",
        adversary_position="Lessee wants simple extension without reopening other terms.",
        counter_arguments=[
            "Extension is a new agreement requiring new consideration",
            "Original lease terms may be below current market",
            "Lessor has no obligation to extend — operator needs the minerals",
            "Amendment is the ideal time to add Pugh, cost-free, and other protections",
            "Each year of extension has quantifiable value that should be compensated",
        ],
        resolution_strategy="Treat amendments as full renegotiation. Demand bonus + improved terms + current market protections.",
        entity_scope="lessor_lessee",
        confidence="DEFENSIBLE",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Rogers v. Ricane Enterprises (Tex. 1989)",
    )

    blocks["mineral_vs_surface_interests"] = DoctrineBlock(
        topic="mineral_vs_surface_interests",
        keywords=["mineral owner", "surface owner", "severed estate", "dominant estate", "surface damage", "accommodation"],
        conclusion_template=(
            "When mineral and surface estates are severed, the mineral estate is dominant — meaning "
            "the mineral owner (and their lessee) has the right to use as much of the surface as "
            "reasonably necessary for mineral development. However, this right is not unlimited. "
            "The accommodation doctrine (Getty Oil v. Jones) requires the mineral developer to "
            "accommodate existing surface uses if alternative methods exist at reasonable cost."
        ),
        reasoning_framework=(
            "Step 1: Determine if mineral and surface estates are severed or unified. Step 2: If "
            "severed, identify surface owner and their existing land uses. Step 3: Negotiate surface "
            "use agreement separate from mineral lease if possible. Step 4: Apply accommodation "
            "doctrine — operator must use existing roads, minimize pad count, directional drill to "
            "reduce surface footprint. Step 5: Address competing irrigation, ranching, or farming."
        ),
        key_factors=[
            "Mineral/surface estate status (unified vs. severed)",
            "Existing surface uses (ranching, farming, residential)",
            "Accommodation doctrine applicability",
            "Surface use agreement negotiation",
            "Directional drilling to minimize surface impact",
            "Water resource competition",
        ],
        primary_authority=[
            "Getty Oil Co. v. Jones, 470 S.W.2d 618 (Tex. 1971)",
            "Merriman v. XTO Energy, 407 S.W.3d 244 (Tex. 2013)",
            "Lightning Oil v. Anadarko, 520 S.W.3d 39 (Tex. 2017)",
            "TN. Res. Code §91.402 — surface owner protections",
        ],
        burden_holder="Mineral developer must accommodate existing surface uses where alternatives exist",
        adversary_position="Operator argues mineral estate dominance gives broad surface use rights.",
        counter_arguments=[
            "Accommodation doctrine limits dominant estate rights since Getty v. Jones (1971)",
            "Directional drilling technology makes surface accommodation feasible",
            "Surface damage payments are industry standard",
            "Environmental liability for surface contamination is substantial",
            "Cooperative relationships produce better long-term outcomes",
        ],
        resolution_strategy="Negotiate surface use agreement with specific provisions for accommodation, damage payments, and restoration.",
        entity_scope="surface_owner_mineral_owner",
        confidence="DEFENSIBLE",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Getty Oil v. Jones (Tex. 1971)",
    )

    blocks["market_enhancement_clause"] = DoctrineBlock(
        topic="market_enhancement_clause",
        keywords=["market enhancement", "marketing", "best price", "arm's length", "affiliate", "gas balancing"],
        conclusion_template=(
            "Market enhancement clauses require the operator to obtain the best available market "
            "price for production and prohibit sales to affiliates at below-market rates. These "
            "clauses protect the lessor against operators who own affiliated midstream and marketing "
            "companies and might otherwise sell production at below-market prices to capture the "
            "margin in their affiliated entities."
        ),
        reasoning_framework=(
            "Step 1: Require operator to sell production at arm's-length market prices. "
            "Step 2: If operator sells to affiliated entity, require price to equal or exceed "
            "published index or arm's-length third-party offers. Step 3: Include audit rights "
            "specific to marketing arrangements. Step 4: Address gas balancing if multiple "
            "working interest owners take gas in kind. Step 5: Prohibit long-term below-market "
            "sales contracts that disadvantage the royalty owner."
        ),
        key_factors=[
            "Arm's-length pricing requirement",
            "Affiliated entity sales restrictions",
            "Published index price benchmarking",
            "Marketing audit rights",
            "Gas balancing provisions",
            "Long-term contract restrictions",
        ],
        primary_authority=[
            "Chesapeake v. Hyder, 483 S.W.3d 870 (Tex. 2016) — at-the-well valuation",
            "Heritage Resources v. NationsBank (Tex. 1996)",
            "Burlington Resources v. Texas Crude Energy (Tex. 2019)",
        ],
        burden_holder="Operator must demonstrate arm's-length pricing for royalty calculation",
        adversary_position="Lessee argues integrated operations create efficiencies that benefit all parties.",
        counter_arguments=[
            "Affiliated transactions are inherently suspect without arm's-length verification",
            "Index pricing provides objective market benchmark",
            "Lessor has no visibility into operator's marketing arrangements without audit rights",
            "Below-market affiliate sales directly reduce lessor royalty revenue",
            "Market enhancement is consistent with implied covenant to market",
        ],
        resolution_strategy="Require arm's-length pricing, index benchmarking for affiliate sales, and marketing-specific audit rights.",
        entity_scope="lessor_lessee",
        confidence="DEFENSIBLE",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Chesapeake v. Hyder (Tex. 2016)",
    )

    # =========================================================================
    # BLOCKS 23-42: ADDITIONAL SPECIALIZED DOCTRINES
    # =========================================================================

    blocks["lessor_protective_provisions"] = DoctrineBlock(
        topic="lessor_protective_provisions",
        keywords=["lessor", "protective", "addendum", "rider", "mineral owner protections", "lease addendum"],
        conclusion_template=(
            "Lessor protective provisions are addenda or riders attached to standard lease forms "
            "that modify or supplement printed form language in the mineral owner's favor. "
            "Standard printed lease forms (Producers 88, AAPL 610) are drafted to favor the "
            "lessee. A comprehensive lessor addendum should address royalty rate, cost-free "
            "language, Pugh clause, surface protections, pooling limits, assignment restrictions, "
            "audit rights, and environmental indemnification."
        ),
        reasoning_framework=(
            "Step 1: Never sign a printed form lease without a lessor addendum. Step 2: Include all "
            "critical protective provisions. Step 3: Ensure addendum language controls over "
            "conflicting printed form language. Step 4: Have addendum reviewed by oil and gas attorney. "
            "Step 5: Negotiate as a package — prioritize royalty rate and cost-free above all else."
        ),
        key_factors=[
            "Standard form deficiencies identification",
            "Addendum controls over printed form language",
            "Priority ranking of protective provisions",
            "Attorney review requirement",
            "Package negotiation strategy",
        ],
        primary_authority=[
            "AAPL Form 610 — standard lease provisions",
            "Producers 88 — printed form lease analysis",
            "Texas Property Code — lease interpretation principles",
        ],
        burden_holder="Lessor must proactively negotiate protective provisions",
        adversary_position="Lessee prefers standard printed form without modifications.",
        counter_arguments=[
            "Printed forms are drafted by industry groups favorable to operators",
            "Lessor addenda are standard practice in all active basins",
            "Attorney review is a reasonable and expected part of lease negotiation",
            "Failure to negotiate protections is irreversible for the lease term",
            "Sophisticated mineral owners always use comprehensive addenda",
        ],
        resolution_strategy="Prepare comprehensive lessor addendum covering all 12+ critical protections. Never sign printed form without modifications.",
        entity_scope="lessor",
        confidence="DEFENSIBLE",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Texas lease interpretation — four corners rule + addendum supremacy",
    )

    blocks["market_value_vs_proceeds"] = DoctrineBlock(
        topic="market_value_vs_proceeds",
        keywords=["market value", "proceeds", "amount realized", "valuation", "royalty calculation", "sales price"],
        conclusion_template=(
            "The royalty valuation method — market value vs. proceeds — fundamentally affects how "
            "royalties are calculated. Market value royalties are based on what the production is "
            "worth at the point of sale regardless of what the operator actually receives. Proceeds "
            "royalties are based on the operator's actual sales receipts. Market value is generally "
            "more favorable for lessors when operators sell below market through affiliates."
        ),
        reasoning_framework=(
            "Step 1: Identify the royalty valuation language in the lease. Step 2: 'Market value' "
            "requires valuation at fair market value regardless of actual sales price. Step 3: "
            "'Proceeds' or 'amount realized' ties royalty to actual sales receipts. Step 4: In Texas, "
            "Chesapeake v. Hyder established that market-value royalties should be valued at the "
            "point of sale. Step 5: Prefer market value language with cost-free provisions."
        ),
        key_factors=[
            "Market value vs. proceeds language identification",
            "Point of valuation (wellhead vs. point of sale)",
            "Affiliate sales impact on royalty calculation",
            "State law default rules",
            "Interaction with cost-free provisions",
        ],
        primary_authority=[
            "Chesapeake v. Hyder, 483 S.W.3d 870 (Tex. 2016)",
            "Heritage Resources v. NationsBank (Tex. 1996)",
            "Yzaguirre v. KCS Resources, 53 S.W.3d 368 (Tex. 2001)",
        ],
        burden_holder="Lessor should negotiate market value language",
        adversary_position="Lessee prefers proceeds language to avoid valuation disputes.",
        counter_arguments=[
            "Market value protects lessor from below-market affiliate sales",
            "Proceeds language allows operator to manipulate royalty through contract terms",
            "Market value is objective and verifiable through published indices",
            "Cost-free + market value provides the strongest royalty protection",
            "Chesapeake v. Hyder supports market value at point of sale",
        ],
        resolution_strategy="Negotiate market value royalty language with cost-free provisions and point-of-sale valuation.",
        entity_scope="lessor_lessee",
        confidence="DEFENSIBLE",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Chesapeake v. Hyder (Tex. 2016)",
    )

    blocks["force_pooling_defense"] = DoctrineBlock(
        topic="force_pooling_defense",
        keywords=["force pooling", "compulsory pooling", "involuntary pooling", "rrc", "railroad commission"],
        conclusion_template=(
            "Force pooling occurs when a regulatory body (Texas Railroad Commission, Oklahoma "
            "Corporation Commission) compels an uncommitted mineral interest to be included in a "
            "drilling unit. In Texas, force pooling is limited to specific circumstances under "
            "Tex. Nat. Res. Code §102.012. Lessors can protect against unfavorable force pooling "
            "by including lease pooling terms that are at least as favorable as statutory terms."
        ),
        reasoning_framework=(
            "Step 1: Understand state-specific force pooling statutes. Texas §102.012 is narrow; "
            "Oklahoma is broader. Step 2: Negotiate voluntary pooling terms in the lease that "
            "provide better protection than statutory defaults. Step 3: Limit operator's pooling "
            "authority to prevent preemptive pooling that moots force pooling protections. "
            "Step 4: Monitor RRC pooling applications and participate in hearings."
        ),
        key_factors=[
            "State-specific force pooling statutes",
            "Voluntary pooling terms vs. statutory defaults",
            "Lease pooling authority limitations",
            "RRC hearing participation rights",
            "Royalty rate protection under force pooling",
        ],
        primary_authority=[
            "Texas Natural Resources Code §102.012",
            "Oklahoma Corporation Commission pooling rules",
            "Jones v. Killingsworth, 403 S.W.2d 325 (Tex. 1966)",
        ],
        burden_holder="Operator seeking force pooling must demonstrate statutory compliance",
        adversary_position="Operator argues force pooling is necessary for efficient development.",
        counter_arguments=[
            "Voluntary leasing at market terms is preferable to forced pooling",
            "Lease pooling terms should match or exceed statutory minimums",
            "Mineral owners have right to participate in pooling hearings",
            "Force pooling should not be used to circumvent market-rate lease negotiations",
            "Operator must demonstrate inability to acquire lease at reasonable terms",
        ],
        resolution_strategy="Include lease pooling terms matching statutory minimums. Monitor force pooling applications.",
        entity_scope="lessor_regulatory",
        confidence="DEFENSIBLE",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Jones v. Killingsworth (Tex. 1966)",
    )

    blocks["paid_up_vs_delay_rental"] = DoctrineBlock(
        topic="paid_up_vs_delay_rental",
        keywords=["paid-up", "paid up", "delay rental", "annual rental", "rental payment", "lease maintenance"],
        conclusion_template=(
            "A paid-up lease requires no annual delay rental payments — the entire consideration "
            "is included in the initial bonus. A delay rental lease requires annual per-acre "
            "payments to maintain the lease during the primary term if no drilling occurs. "
            "Delay rentals create annual leverage but paid-up eliminates missed-payment termination "
            "risk. Most modern leases are paid-up; delay rental structures are less common."
        ),
        reasoning_framework=(
            "Step 1: Evaluate paid-up vs. delay rental preferences. Step 2: Paid-up advantages: "
            "no annual payment tracking, no termination risk from missed payment, simpler "
            "administration. Step 3: Delay rental advantages: annual cash flow, regular review "
            "opportunity, operator maintains engagement. Step 4: If delay rental, ensure automatic "
            "termination for non-payment with no cure period."
        ),
        key_factors=[
            "Total economic comparison (bonus + rentals vs. paid-up bonus)",
            "Administrative simplicity preference",
            "Termination risk from missed delay rental payment",
            "Annual engagement and review opportunity",
            "Operator's preference and standard practice",
        ],
        primary_authority=[
            "Anadarko v. Thompson (Tex. 2002)",
            "Rogers v. Ricane Enterprises (Tex. 1989)",
            "AAPL Form 610 — delay rental provisions",
        ],
        burden_holder="Lessee must pay delay rentals timely or lease terminates",
        adversary_position="Lessee prefers paid-up to eliminate annual payment obligation.",
        counter_arguments=[
            "Paid-up lease eliminates annual leverage over operator development timing",
            "Delay rental structure creates annual financial engagement",
            "Missed delay rental payment automatically terminates the lease",
            "Paid-up bonus should be higher to compensate for lost annual payments",
            "Delay rentals provide ongoing income during non-development periods",
        ],
        resolution_strategy="Accept paid-up lease with appropriately higher bonus. If delay rental, require strict timely payment.",
        entity_scope="lessor_lessee",
        confidence="DEFENSIBLE",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Anadarko v. Thompson (Tex. 2002)",
    )

    blocks["no_surface_operations"] = DoctrineBlock(
        topic="no_surface_operations",
        keywords=["no surface", "surface waiver", "directional drilling", "off-site drilling", "subsurface only"],
        conclusion_template=(
            "A no-surface-operations clause prohibits the operator from conducting any operations "
            "on the leased surface while retaining the right to access minerals from adjacent or "
            "off-site locations using directional or horizontal drilling. This is critical for "
            "residential, commercial, or agricultural surface use where any surface disturbance "
            "is unacceptable. Modern horizontal drilling makes this technically feasible."
        ),
        reasoning_framework=(
            "Step 1: Draft language prohibiting all surface entry, including seismic, surveying, "
            "road construction, pipeline, and pad construction. Step 2: Reserve operator's right "
            "to access minerals via directional drilling from off-site locations. Step 3: Address "
            "subsurface-only rights — operator may cross beneath the surface. Step 4: Ensure "
            "restriction applies to operator and all assigns, contractors, and agents."
        ),
        key_factors=[
            "Complete surface entry prohibition",
            "Directional drilling feasibility from adjacent tracts",
            "Subsurface crossing rights",
            "Binding on assigns and contractors",
            "Impact on bonus and royalty negotiation",
        ],
        primary_authority=[
            "Lightning Oil v. Anadarko, 520 S.W.3d 39 (Tex. 2017)",
            "Getty Oil v. Jones (Tex. 1971)",
            "Coyote Lake Ranch v. City of Lubbock, 498 S.W.3d 53 (Tex. 2016)",
        ],
        burden_holder="Lessor must include express no-surface-operations language",
        adversary_position="Operator argues surface access is necessary for efficient operations.",
        counter_arguments=[
            "Horizontal drilling from adjacent pads is technically proven",
            "Surface disturbance is incompatible with residential or agricultural use",
            "No-surface leases are common in urban and suburban mineral development",
            "Operator can access minerals without entering the leased surface",
            "Subsurface-only rights preserve surface integrity completely",
        ],
        resolution_strategy="Include comprehensive no-surface-operations clause for residential, commercial, or sensitive surface uses.",
        entity_scope="lessor_surface_owner",
        confidence="DEFENSIBLE",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Lightning Oil v. Anadarko (Tex. 2017)",
    )

    blocks["gas_royalty_valuation"] = DoctrineBlock(
        topic="gas_royalty_valuation",
        keywords=["gas royalty", "gas valuation", "mcf", "mmbtu", "residue gas", "ngl", "plant products", "gas processing"],
        conclusion_template=(
            "Gas royalty valuation is more complex than oil royalty because natural gas undergoes "
            "processing that separates residue gas from natural gas liquids (NGLs). The lessor's "
            "royalty must cover both residue gas and NGL products. Valuation should be at the "
            "point of sale, not the wellhead, and royalty should be calculated on the full value "
            "of all products extracted from the gas stream."
        ),
        reasoning_framework=(
            "Step 1: Identify all revenue streams from gas production: residue gas, ethane, "
            "propane, butane, natural gasoline, condensate. Step 2: Ensure royalty covers all "
            "products, not just residue gas. Step 3: Specify valuation at the point of sale or "
            "first arm's-length transaction. Step 4: Address processing plant shrinkage — the "
            "volume reduction during processing. Step 5: Require reporting of all product volumes "
            "and prices."
        ),
        key_factors=[
            "Coverage of all gas stream products (residue + NGLs)",
            "Valuation point (wellhead vs. point of sale)",
            "Processing shrinkage allocation",
            "Product-by-product reporting requirement",
            "Cost-free language applicability to gas processing",
        ],
        primary_authority=[
            "Chesapeake v. Hyder (Tex. 2016)",
            "Heritage Resources v. NationsBank (Tex. 1996)",
            "Burlington Resources v. Texas Crude Energy (Tex. 2019)",
        ],
        burden_holder="Operator must account for all products and provide transparent reporting",
        adversary_position="Operator argues gas processing creates value and costs should be shared.",
        counter_arguments=[
            "All gas stream products belong to the mineral owner in proportion to royalty",
            "Processing is a cost of making gas marketable — covered by cost-free language",
            "Point-of-sale valuation captures full product value",
            "Product-by-product reporting enables lessor verification",
            "Shrinkage allocation must be transparent and auditable",
        ],
        resolution_strategy="Ensure royalty covers all gas products at point of sale with cost-free provisions and detailed reporting.",
        entity_scope="lessor_lessee",
        confidence="DEFENSIBLE",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Burlington Resources v. Texas Crude Energy (Tex. 2019)",
    )

    blocks["horizontal_well_considerations"] = DoctrineBlock(
        topic="horizontal_well_considerations",
        keywords=["horizontal", "horizontal well", "lateral", "lateral length", "horizontal drilling", "multi-well pad"],
        conclusion_template=(
            "Horizontal drilling has fundamentally changed lease negotiation. A single horizontal "
            "well with a 2-mile lateral can drain minerals from multiple tracts and multiple "
            "sections. This makes Pugh clauses, pooling limitations, and depth restrictions more "
            "critical than ever. Lease terms must address lateral length, wellbore location within "
            "the unit, allocation of production across tracts, and multi-well pad operations."
        ),
        reasoning_framework=(
            "Step 1: Address lateral length — ensure lease allows horizontal wells of industry "
            "standard length (7,500-15,000 feet). Step 2: Require wellbore to physically penetrate "
            "the leased acreage (not merely pooled). Step 3: Specify production allocation method — "
            "proportionate share based on lateral feet within the unit. Step 4: Address multi-well "
            "pad development — how production from multiple wells in different formations is allocated."
        ),
        key_factors=[
            "Lateral length allowance and restrictions",
            "Wellbore penetration requirement",
            "Production allocation method (proportionate feet)",
            "Multi-well pad considerations",
            "Pugh clause interaction with horizontal wells",
        ],
        primary_authority=[
            "ConocoPhillips v. Koopmann (Tex. 2018)",
            "Texas Railroad Commission Statewide Rule 86",
            "AAPL Form 610 — horizontal drilling provisions",
        ],
        burden_holder="Operator must allocate production fairly across tracts",
        adversary_position="Operator wants maximum flexibility in well placement and allocation.",
        counter_arguments=[
            "Proportionate allocation based on lateral length is the industry standard",
            "Wellbore must physically penetrate leased acreage to hold the lease",
            "Multi-well pads require transparent allocation by formation and lateral",
            "Pugh clause prevents a single horizontal well from holding all depths",
            "RRC Rule 86 provides regulatory framework for horizontal well allocation",
        ],
        resolution_strategy="Require proportionate allocation, wellbore penetration, and Pugh clause for horizontal well leases.",
        entity_scope="lessor_lessee",
        confidence="DEFENSIBLE",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="ConocoPhillips v. Koopmann (Tex. 2018)",
    )

    blocks["water_rights_protection"] = DoctrineBlock(
        topic="water_rights_protection",
        keywords=["water", "water rights", "groundwater", "fresh water", "produced water", "disposal", "water well"],
        conclusion_template=(
            "Water rights protection in oil and gas leases is increasingly critical as hydraulic "
            "fracturing operations consume millions of gallons per well. Lease provisions should "
            "protect the lessor's surface and groundwater resources, prohibit use of the lessor's "
            "water wells without separate agreement, restrict produced water disposal on the leased "
            "premises, and address freshwater source protection."
        ),
        reasoning_framework=(
            "Step 1: Prohibit operator from using lessor's water wells, stock tanks, or irrigation "
            "systems without separate written agreement. Step 2: Restrict saltwater disposal wells "
            "on the leased premises. Step 3: Require operator to use recycled produced water or "
            "purchased water for frac operations. Step 4: Protect freshwater aquifers with casing "
            "program requirements. Step 5: Address seismic risk from produced water injection."
        ),
        key_factors=[
            "Prohibition on lessor water source use",
            "Saltwater disposal restrictions",
            "Frac water sourcing requirements",
            "Freshwater aquifer protection",
            "Seismic risk from injection wells",
            "Separate water use agreement requirement",
        ],
        primary_authority=[
            "Texas Water Code Ch. 26 — water pollution control",
            "Texas Natural Resources Code §122 — groundwater protection",
            "Edwards Aquifer Authority v. Day, 369 S.W.3d 814 (Tex. 2012)",
            "RRC Statewide Rule 13 — casing requirements",
        ],
        burden_holder="Operator must protect water resources and obtain separate water use agreement",
        adversary_position="Operator argues water access is necessary and included in surface use rights.",
        counter_arguments=[
            "Water is a separate valuable resource from minerals",
            "Frac operations consume 5-15 million gallons per well — catastrophic for ranching",
            "Produced water disposal creates seismic risk and contamination potential",
            "Separate water use agreement provides lessor compensation and control",
            "Freshwater protection is required by RRC casing rules",
        ],
        resolution_strategy="Include comprehensive water protection provisions with separate water use agreement requirement.",
        entity_scope="lessor_surface_owner",
        confidence="DEFENSIBLE",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Edwards Aquifer Authority v. Day (Tex. 2012)",
    )

    blocks["implied_covenants"] = DoctrineBlock(
        topic="implied_covenants",
        keywords=["implied covenant", "reasonable development", "further exploration", "market", "protect against drainage"],
        conclusion_template=(
            "Implied covenants are obligations imposed on the lessee by law even if not expressly "
            "stated in the lease. The five traditional implied covenants are: (1) to reasonably "
            "develop the leased premises, (2) to further explore after initial discovery, (3) to "
            "protect against drainage by offsetting wells, (4) to market production diligently, "
            "and (5) to conduct operations as a reasonably prudent operator."
        ),
        reasoning_framework=(
            "Step 1: Understand each implied covenant and its practical impact. Step 2: Make "
            "implied covenants express in the lease for enforceability. Step 3: The implied "
            "covenant to develop is the most commonly litigated. Step 4: The implied covenant to "
            "protect against drainage requires offsetting competitor wells. Step 5: Express "
            "language strengthens lessor's enforcement position."
        ),
        key_factors=[
            "Five traditional implied covenants",
            "Express vs. implied enforcement strength",
            "Reasonable prudent operator standard",
            "Drainage protection obligations",
            "Development pace requirements",
        ],
        primary_authority=[
            "Clifton v. Koontz, 325 S.W.2d 684 (Tex. 1959)",
            "Amoco Production Co. v. Alexander, 622 S.W.2d 563 (Tex. 1981)",
            "Rogers v. Ricane Enterprises (Tex. 1989)",
            "5 Williams & Meyers, Oil and Gas Law §§801-861",
        ],
        burden_holder="Lessor must demonstrate lessee failed to act as reasonably prudent operator",
        adversary_position="Lessee argues business judgment dictates development pace and marketing decisions.",
        counter_arguments=[
            "Implied covenants are established Texas law — not discretionary",
            "Reasonably prudent operator standard is objective, not subjective",
            "Express lease language eliminates ambiguity about obligations",
            "Drainage protection is measurable through production data",
            "Failure to develop denies lessor the benefit of the lease bargain",
        ],
        resolution_strategy="Make implied covenants express with specific performance standards and remedies.",
        entity_scope="lessor_lessee",
        confidence="DEFENSIBLE",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Amoco Production v. Alexander (Tex. 1981)",
    )

    blocks["lease_broker_engagement"] = DoctrineBlock(
        topic="lease_broker_engagement",
        keywords=["lease broker", "landman", "agent", "negotiation representative", "mineral manager", "fiduciary"],
        conclusion_template=(
            "Engaging a lease broker or professional landman to represent the mineral owner in "
            "lease negotiations can significantly improve terms. However, the mineral owner must "
            "understand the broker's compensation structure, conflicts of interest, and scope of "
            "authority. Brokers typically earn a percentage of the bonus or an override, which can "
            "create incentives to close deals quickly rather than negotiate optimal terms."
        ),
        reasoning_framework=(
            "Step 1: Select a broker or landman who represents mineral owners, not operators. "
            "Step 2: Define scope of authority in writing — broker can negotiate but not execute. "
            "Step 3: Understand compensation — flat fee is more aligned than percentage of bonus. "
            "Step 4: Require broker to present all offers and competing terms. Step 5: Retain "
            "oil and gas attorney for final lease review regardless of broker involvement."
        ),
        key_factors=[
            "Broker selection — mineral owner representative vs. operator agent",
            "Scope of authority definition",
            "Compensation structure alignment",
            "Disclosure of all offers requirement",
            "Attorney review of final lease",
        ],
        primary_authority=[
            "Texas Occupations Code — broker licensing requirements",
            "AAPL Standards of Practice for landmen",
            "Common law agency and fiduciary principles",
        ],
        burden_holder="Broker must act in mineral owner's best interest under agency principles",
        adversary_position="Broker may prioritize deal closing speed over optimal terms.",
        counter_arguments=[
            "Flat fee compensation aligns broker interest with mineral owner",
            "Written scope of authority prevents unauthorized commitments",
            "Attorney review provides independent protection",
            "Full disclosure of all offers ensures informed decision-making",
            "Professional landmen add value through market knowledge and negotiation experience",
        ],
        resolution_strategy="Engage mineral owner broker with flat fee, written authority limits, and independent attorney review.",
        entity_scope="lessor",
        confidence="DEFENSIBLE",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Common law agency — fiduciary duty to principal",
    )

    logger.info(f"Doctrine cache built: {len(blocks)} blocks for engine {ENGINE_ID}")
    return blocks
