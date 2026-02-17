"""
LM08 Due Diligence Engine - Doctrine Cache Module
====================================================
Pre-compiled expert reasoning blocks for oil & gas acquisition due diligence.
Each block contains real domain content: conclusion templates, reasoning frameworks,
key factors, primary authorities, adversary positions, and counter-arguments.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class IssueCategory(str, Enum):
    """Due diligence issue categories."""
    TITLE_DUE_DILIGENCE = "TITLE_DUE_DILIGENCE"
    ENVIRONMENTAL_COMPLIANCE = "ENVIRONMENTAL_COMPLIANCE"
    REGULATORY_AUDIT = "REGULATORY_AUDIT"
    PRODUCTION_ANALYSIS = "PRODUCTION_ANALYSIS"
    RESERVE_ESTIMATION = "RESERVE_ESTIMATION"
    LEASE_STATUS = "LEASE_STATUS"
    LIEN_ENCUMBRANCE = "LIEN_ENCUMBRANCE"
    LITIGATION_REVIEW = "LITIGATION_REVIEW"
    PREFERENTIAL_RIGHTS = "PREFERENTIAL_RIGHTS"
    CONSENT_ASSIGN = "CONSENT_ASSIGN"
    CHANGE_OF_CONTROL = "CHANGE_OF_CONTROL"
    AMI_AGREEMENTS = "AMI_AGREEMENTS"
    DEFICIENCY_CURE = "DEFICIENCY_CURE"
    PSA_REVIEW = "PSA_REVIEW"
    REPS_WARRANTIES = "REPS_WARRANTIES"
    INDEMNIFICATION = "INDEMNIFICATION"
    NRI_WI_VERIFICATION = "NRI_WI_VERIFICATION"
    SUSPENSE_ANALYSIS = "SUSPENSE_ANALYSIS"
    OPERATOR_QUALIFICATION = "OPERATOR_QUALIFICATION"


class ConfidenceLevel(str, Enum):
    """Confidence stratification levels."""
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"


class PositionZone(str, Enum):
    """Position zones — never blur buyer vs. seller perspective."""
    BUYER = "BUYER"
    SELLER = "SELLER"
    NEUTRAL = "NEUTRAL"


@dataclass
class DoctrineBlock:
    """A pre-compiled doctrine reasoning block."""
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
    confidence: ConfidenceLevel
    confidence_stratification: str
    controlling_precedent: str
    issue_category: IssueCategory
    position_zone: PositionZone = PositionZone.NEUTRAL
    interaction_edges: List[str] = field(default_factory=list)


# =============================================================================
# DOCTRINE CACHE — 45 BLOCKS OF REAL DOMAIN EXPERTISE
# =============================================================================

DOCTRINE_CACHE: Dict[str, DoctrineBlock] = {}


def _register(block: DoctrineBlock) -> None:
    """Register a doctrine block in the cache."""
    DOCTRINE_CACHE[block.topic] = block


# ─────────────────────────────────────────────────────────────────────────────
# 1. TITLE DUE DILIGENCE
# ─────────────────────────────────────────────────────────────────────────────

_register(DoctrineBlock(
    topic="title_opinion_standard_of_review",
    keywords=["title opinion", "standard of review", "marketable title", "examination", "division order"],
    conclusion_template=(
        "The applicable standard of title review in an acquisition context is the "
        "'marketable title' standard unless the PSA specifies a different standard such as "
        "'defensible title' or 'good and indefeasible title.' The acquiring party should "
        "clearly define the title standard in the PSA to avoid disputes during the defect "
        "assertion period."
    ),
    reasoning_framework=(
        "Title opinions in oil and gas acquisitions serve a fundamentally different purpose "
        "than drilling title opinions. An acquisition title opinion must evaluate the entire "
        "chain of title from sovereign to current owner, identify all burdens (royalties, "
        "overriding royalties, production payments, net profits interests), confirm the "
        "seller's working interest and net revenue interest, and identify all title defects "
        "that could affect the buyer's enjoyment of the acquired assets. The standard of "
        "review determines which issues constitute 'defects' versus mere 'requirements.' "
        "Under a 'marketable title' standard, the title must be free from reasonable doubt "
        "and a reasonably prudent person would accept it. Under a 'defensible title' standard, "
        "which is less stringent, the title need only be defensible against challenge — there "
        "may be open questions that have not been and likely will not be challenged. The PSA "
        "typically specifies the standard, and the title examiner's opinion should apply that "
        "standard consistently across all evaluated properties. AAPL Title Examination Standards "
        "provide baseline guidance but specific PSA language controls."
    ),
    key_factors=[
        "PSA-defined title standard (marketable vs. defensible vs. good and indefeasible)",
        "Scope of examination period (from sovereign vs. from base abstract date)",
        "Treatment of uncured title requirements vs. title defects",
        "Allocation of curative responsibility between buyer and seller",
        "Materiality threshold for title defect assertion (NRI variance)",
        "Time period for defect assertion and cure",
    ],
    primary_authority=[
        "AAPL Title Examination Standards (2020 rev.)",
        "State-specific title standards (e.g., Texas Title Examination Standards)",
        "Restatement (Third) of Property: Servitudes",
        "Williams & Meyers, Oil and Gas Law, Ch. 3",
    ],
    burden_holder="Buyer bears burden of identifying defects within assertion period; seller bears burden of cure.",
    adversary_position=(
        "Seller will argue that 'defensible title' standard should apply to limit defect "
        "assertions, and that any defect not raised within the assertion period is waived."
    ),
    counter_arguments=[
        "Buyer should insist on 'marketable title' standard for higher-value acquisitions to ensure clean title.",
        "Title defects discovered post-closing should be covered by seller's representations and indemnification.",
        "The examination standard should be explicitly defined to avoid ambiguity in defect classification.",
        "Known defects accepted at closing should be reflected in purchase price adjustments.",
        "Supplemental title opinions may be required for properties with complex title chains.",
    ],
    resolution_strategy=(
        "Define the title standard explicitly in the PSA. Set clear materiality thresholds "
        "(e.g., NRI variance of 0.01 or more constitutes a defect). Establish reasonable "
        "assertion and cure periods (typically 30-45 days for assertion, 90-120 days for cure). "
        "Include a dispute resolution mechanism for contested defects."
    ),
    entity_scope="All acquisition targets",
    confidence=ConfidenceLevel.DEFENSIBLE,
    confidence_stratification="Well-established industry practice with strong AAPL guidance.",
    controlling_precedent="AAPL Title Examination Standards; state-specific title standards",
    issue_category=IssueCategory.TITLE_DUE_DILIGENCE,
    position_zone=PositionZone.BUYER,
    interaction_edges=["deficiency_identification_and_cure", "nri_working_interest_verification"],
))

_register(DoctrineBlock(
    topic="chain_of_title_gap_analysis",
    keywords=["chain of title", "gap", "missing link", "wild deed", "break in chain", "ownership"],
    conclusion_template=(
        "Gaps in the chain of title — whether caused by missing instruments, unrecorded "
        "conveyances, intestate successions without probate, or 'wild deeds' recorded outside "
        "the chain — constitute title defects requiring curative action. The severity depends "
        "on whether the gap affects the current owner's ability to convey marketable title."
    ),
    reasoning_framework=(
        "A complete chain of title traces ownership from the sovereign (state or federal "
        "government) through each successive conveyance to the current owner. Any break in "
        "this chain creates uncertainty about the current owner's right to convey. Common "
        "causes of gaps include: (1) instruments never recorded, (2) instruments recorded "
        "outside the direct chain (wild deeds), (3) deaths without probate proceedings, "
        "(4) corporate dissolutions without proper conveyance, (5) tax sales with defective "
        "notice, (6) foreclosure proceedings with jurisdictional defects. For oil and gas "
        "interests, the analysis is complicated by the severable nature of the mineral estate "
        "— a gap affecting only the surface estate may not affect the mineral title, and vice "
        "versa. Constructive notice doctrine means that a properly recorded instrument in the "
        "chain provides notice to all subsequent purchasers, but instruments outside the chain "
        "(wild deeds) do not provide constructive notice. Curative options include: affidavits "
        "of heirship, quiet title actions, tax title curative, ratification instruments, and "
        "corrective deeds. Title insurance may be available to insure over certain gaps."
    ),
    key_factors=[
        "Location and nature of the gap in the chain",
        "Whether the gap affects mineral or surface estate or both",
        "Duration of possession following the gap (adverse possession/limitations)",
        "Availability of curative instruments (affidavits, ratifications, quiet title)",
        "State-specific recording act type (race, notice, race-notice)",
        "Whether title insurance is available and at what cost",
    ],
    primary_authority=[
        "State recording statutes (e.g., Tex. Prop. Code Chapter 13)",
        "State adverse possession statutes (e.g., Tex. Civ. Prac. & Rem. Code Ch. 16)",
        "Luthi v. Evans, 233 Kan. 1060 (1983) — constructive notice in chain",
        "Williams & Meyers, Oil and Gas Law, Chapter 2",
    ],
    burden_holder="Buyer to identify gaps; seller to provide curative or accept price adjustment.",
    adversary_position=(
        "Seller argues that long-standing gaps not challenged constitute defensible title "
        "under limitations doctrines and that buyer should accept title insurance as cure."
    ),
    counter_arguments=[
        "Title insurance is not equivalent to clear title — it merely shifts risk to insurer.",
        "Limitations periods may not have run if possession was interrupted or disputed.",
        "Federal mineral interests (BLM leases) have different recording requirements.",
        "Wild deeds may have been recorded in other counties or under variant spellings.",
        "Some gaps require judicial action (quiet title) that cannot be completed during diligence period.",
    ],
    resolution_strategy=(
        "Map every gap chronologically. Assess whether limitations have cured the gap. "
        "Obtain affidavits of heirship for intestate successions. File corrective instruments "
        "where possible. Pursue quiet title only for material gaps. Accept title insurance "
        "for minor gaps below the materiality threshold."
    ),
    entity_scope="All mineral and leasehold interests",
    confidence=ConfidenceLevel.DEFENSIBLE,
    confidence_stratification="Standard title examination methodology with well-developed case law.",
    controlling_precedent="State recording acts; state limitations statutes",
    issue_category=IssueCategory.TITLE_DUE_DILIGENCE,
    position_zone=PositionZone.BUYER,
    interaction_edges=["title_opinion_standard_of_review", "deficiency_identification_and_cure"],
))

_register(DoctrineBlock(
    topic="mineral_severance_analysis",
    keywords=["mineral severance", "mineral reservation", "surface vs mineral", "severed estate", "outstanding mineral"],
    conclusion_template=(
        "When the mineral estate has been severed from the surface estate, due diligence must "
        "independently trace each estate's chain of title. Outstanding mineral reservations, "
        "if not properly identified, can result in the buyer acquiring less mineral interest "
        "than expected, directly impacting NRI and purchase price."
    ),
    reasoning_framework=(
        "The dominant estate doctrine in most oil and gas states provides that the mineral "
        "estate is dominant, meaning the mineral owner has an implied right of reasonable "
        "surface use for exploration and production. However, this doctrine has been "
        "significantly limited by surface damage statutes and accommodation doctrine in "
        "many states. When evaluating severed mineral interests for acquisition: (1) Trace "
        "the severance instrument to determine the exact quantum of minerals reserved or "
        "conveyed. (2) Determine whether the severance included 'minerals' broadly or was "
        "limited to specific substances. (3) Evaluate whether the reservation language "
        "includes executive rights, bonus, delay rental, and royalty or only a bare mineral "
        "interest. (4) Check for Duhig-type issues where a grantor's warranty may have "
        "conveyed interests the grantor did not own. (5) Assess whether any outstanding "
        "mineral interests may have terminated by operation of law (dormant mineral acts, "
        "marketable title acts, or abandonment)."
    ),
    key_factors=[
        "Language of the severance instrument — 'minerals' definition varies by state",
        "Executive rights: who holds the right to lease the severed minerals",
        "Duhig analysis: did a prior grantor's warranty convey more than intended",
        "Dormant mineral act applicability (e.g., Indiana, Ohio, Michigan statutes)",
        "Surface damage obligations and accommodation doctrine",
        "Whether the severed interest includes development rights or only production rights",
    ],
    primary_authority=[
        "Moser v. U.S. Steel Corp., 676 S.W.2d 99 (Tex. 1984) — surface destruction test",
        "Duhig v. Peavy-Moore Lumber Co., 135 Tex. 503 (1940) — warranty conveyance",
        "Getty Oil Co. v. Jones, 470 S.W.2d 618 (Tex. 1971) — accommodation doctrine",
        "State dormant mineral acts (e.g., Ohio R.C. 5301.56)",
    ],
    burden_holder="Buyer to verify mineral ownership independently from surface records.",
    adversary_position=(
        "Seller may represent that minerals are 'intact' when in fact prior reservations "
        "exist. Seller may argue that Duhig analysis is speculative."
    ),
    counter_arguments=[
        "Mineral severances may not appear in tract indices that index only by grantor-grantee.",
        "Historical mineral reservations often use ambiguous language that varies by state interpretation.",
        "Duhig doctrine may not apply in all states or may be limited to warranty deed context.",
        "Dormant mineral acts have varying requirements and may not be self-executing.",
        "Outstanding mineral owners may surface post-closing to assert rights.",
    ],
    resolution_strategy=(
        "Run independent mineral chain of title. Check county records for all severance "
        "instruments. Apply state-specific mineral definition to each reservation. Perform "
        "Duhig analysis on all warranty conveyances in the chain. Verify executive rights "
        "allocation. Calculate true NRI accounting for all outstanding mineral interests."
    ),
    entity_scope="All mineral acquisitions",
    confidence=ConfidenceLevel.DEFENSIBLE,
    confidence_stratification="Well-developed case law but highly state-specific interpretation.",
    controlling_precedent="State-specific mineral ownership statutes and case law",
    issue_category=IssueCategory.TITLE_DUE_DILIGENCE,
    position_zone=PositionZone.BUYER,
    interaction_edges=["nri_working_interest_verification", "chain_of_title_gap_analysis"],
))

# ─────────────────────────────────────────────────────────────────────────────
# 2. ENVIRONMENTAL COMPLIANCE
# ─────────────────────────────────────────────────────────────────────────────

_register(DoctrineBlock(
    topic="phase_i_esa_scope_and_limitations",
    keywords=["phase i", "esa", "environmental site assessment", "ASTM E1527", "recognized environmental condition", "all appropriate inquiries"],
    conclusion_template=(
        "A Phase I ESA conducted in conformance with ASTM E1527-21 is the baseline environmental "
        "due diligence for oil and gas acquisitions. It establishes the 'innocent landowner' or "
        "'bona fide prospective purchaser' defense under CERCLA but has significant limitations "
        "for upstream oil and gas properties."
    ),
    reasoning_framework=(
        "The Phase I ESA evaluates the presence or likely presence of hazardous substances "
        "or petroleum products at a property through records review, site reconnaissance, "
        "interviews, and historical research. For oil and gas properties, the Phase I scope "
        "must be expanded beyond standard commercial real estate practice to include: "
        "(1) Review of state oil and gas commission records (well files, violation notices, "
        "spill reports). (2) Evaluation of NORM (Naturally Occurring Radioactive Material) "
        "risks, especially in Marcellus/Utica and Bakken formations. (3) Assessment of produced "
        "water disposal practices and injection well compliance. (4) Review of pipeline and "
        "gathering system integrity. (5) Identification of orphan wells and historical drilling "
        "locations. (6) Evaluation of pit closure compliance (drill cuttings, produced water "
        "pits). The Phase I will identify RECs (Recognized Environmental Conditions), HRECs "
        "(Historical RECs), and CRECs (Controlled RECs). Any identified REC typically triggers "
        "a recommendation for Phase II investigation. Cost allocation for environmental "
        "remediation should be addressed in the PSA through specific environmental "
        "representations, indemnification provisions, and potentially environmental escrow."
    ),
    key_factors=[
        "ASTM E1527-21 standard compliance (updated from E1527-13)",
        "Expansion of scope for oil and gas operational considerations",
        "NORM assessment requirements (state-specific regulations)",
        "Produced water disposal compliance (UIC permits, Class II wells)",
        "Orphan well and historical drilling site identification",
        "Environmental insurance (pollution legal liability) availability",
        "State voluntary cleanup program applicability",
    ],
    primary_authority=[
        "ASTM E1527-21 Standard Practice for Environmental Site Assessments",
        "CERCLA Section 101(40) — bona fide prospective purchaser defense",
        "40 CFR Part 312 — All Appropriate Inquiries",
        "State environmental statutes (e.g., TCEQ regulations in Texas)",
    ],
    burden_holder="Buyer to conduct Phase I ESA; environmental consultant liability for errors.",
    adversary_position=(
        "Seller argues that operational oil and gas activities are exempt from CERCLA "
        "petroleum exclusion and that existing NORM levels are within regulatory limits."
    ),
    counter_arguments=[
        "CERCLA petroleum exclusion does not cover all oilfield wastes (e.g., tank bottoms with heavy metals).",
        "NORM regulations vary significantly by state and may impose strict disposal requirements.",
        "Phase I ESA shelf life is 180 days — must be refreshed if closing is delayed.",
        "Environmental consultant qualifications vary — require EP (Environmental Professional) designation.",
        "State voluntary cleanup programs may provide liability protection but require enrollment and completion.",
    ],
    resolution_strategy=(
        "Conduct Phase I ESA per ASTM E1527-21 with oil and gas scope expansion. If RECs "
        "identified, proceed to Phase II. Quantify remediation costs and negotiate purchase "
        "price adjustment or environmental escrow. Evaluate pollution legal liability insurance. "
        "Include specific environmental representations in PSA covering known conditions."
    ),
    entity_scope="All surface and subsurface assets in acquisition",
    confidence=ConfidenceLevel.DEFENSIBLE,
    confidence_stratification="Standard environmental due diligence with well-defined regulatory framework.",
    controlling_precedent="ASTM E1527-21; CERCLA; state environmental regulations",
    issue_category=IssueCategory.ENVIRONMENTAL_COMPLIANCE,
    position_zone=PositionZone.BUYER,
    interaction_edges=["plugging_abandonment_liability", "regulatory_compliance_audit"],
))

_register(DoctrineBlock(
    topic="plugging_abandonment_liability",
    keywords=["plugging", "abandonment", "P&A", "ARO", "asset retirement obligation", "decommissioning", "well plugging"],
    conclusion_template=(
        "Plugging and abandonment (P&A) liability is a critical component of acquisition due "
        "diligence. The buyer assumes the obligation to plug all acquired wells, remove "
        "equipment, and restore surface. P&A costs must be estimated and factored into the "
        "purchase price or addressed through indemnification provisions."
    ),
    reasoning_framework=(
        "P&A obligations attach to the current operator and working interest owners. Upon "
        "acquisition, the buyer assumes these obligations unless the PSA specifically allocates "
        "them otherwise. Due diligence must evaluate: (1) Total well count including active, "
        "inactive, temporarily abandoned, and shut-in wells. (2) State regulatory requirements "
        "for plugging (cement volumes, plug placement, surface restoration). (3) Historical "
        "P&A costs in the relevant field and formation. (4) Supplemental bonding requirements "
        "— many states are tightening bonding rules. (5) Federal wells on BLM/Forest Service "
        "land have separate and often more stringent P&A requirements. (6) Environmental "
        "remediation costs associated with P&A (pit closures, soil remediation, produced "
        "water spills). (7) Idle well policies — many states now require operators to plug "
        "or return to production within specified timeframes (e.g., California's AB 1057, "
        "New Mexico idle well rules). (8) SEC ASC 410-20 Asset Retirement Obligations require "
        "public companies to accrue P&A costs on financial statements. These accrued amounts "
        "should be compared to actual estimated costs. Underaccrual of ARO is a common "
        "acquisition risk. P&A cost estimation should use recent comparable plugging operations "
        "in the same area and formation, adjusted for well depth, casing condition, and "
        "accessibility. Offshore P&A costs are substantially higher due to platform removal "
        "and subsea well plugging requirements."
    ),
    key_factors=[
        "Total well count by status (active, inactive, shut-in, temporarily abandoned)",
        "Average P&A cost per well in the relevant basin/formation",
        "Bonding requirements (individual well bonds, blanket bonds, statewide bonds)",
        "Idle well regulatory compliance status",
        "Surface owner agreements and restoration requirements",
        "Federal vs. state well P&A requirements",
        "Seller's ARO accrual vs. actual estimated P&A costs",
        "Environmental remediation costs associated with well sites",
    ],
    primary_authority=[
        "State plugging regulations (e.g., 16 TAC Chapter 3, Statewide Rule 14 in Texas)",
        "BLM Onshore Order No. 2 (federal well abandonment)",
        "ASC 410-20 Asset Retirement Obligations",
        "State bonding requirements (e.g., Tex. Nat. Res. Code Section 91.104)",
    ],
    burden_holder="Buyer assumes P&A liability upon closing unless PSA allocates to seller.",
    adversary_position=(
        "Seller may understate P&A liability by using outdated cost estimates or excluding "
        "inactive wells from the count. Seller may argue that ARO accrual is adequate."
    ),
    counter_arguments=[
        "Historical P&A costs in many basins have escalated 30-50% in recent years due to contractor scarcity.",
        "State regulatory agencies are increasingly enforcing idle well plugging requirements.",
        "ARO accruals on financial statements often significantly underestimate actual P&A costs.",
        "Surface restoration costs are frequently excluded from P&A estimates.",
        "Bonding requirements are increasing — blanket bonds may be insufficient post-acquisition.",
    ],
    resolution_strategy=(
        "Obtain complete well list with status codes. Estimate P&A cost per well using recent "
        "comparable operations. Compare seller's ARO to independent estimate. Negotiate "
        "purchase price adjustment for P&A excess. Evaluate escrow or holdback for P&A on "
        "inactive/shut-in wells. Verify bonding compliance and transfer."
    ),
    entity_scope="All wells and facilities in acquisition",
    confidence=ConfidenceLevel.DEFENSIBLE,
    confidence_stratification="Well-established regulatory framework; cost estimation has inherent uncertainty.",
    controlling_precedent="State plugging regulations; ASC 410-20; BLM Onshore Orders",
    issue_category=IssueCategory.ENVIRONMENTAL_COMPLIANCE,
    position_zone=PositionZone.BUYER,
    interaction_edges=["phase_i_esa_scope_and_limitations", "closing_adjustments_methodology"],
))

# ─────────────────────────────────────────────────────────────────────────────
# 3. REGULATORY AUDIT
# ─────────────────────────────────────────────────────────────────────────────

_register(DoctrineBlock(
    topic="regulatory_compliance_audit",
    keywords=["regulatory", "compliance", "RRC", "BLM", "EPA", "violation", "notice", "permit"],
    conclusion_template=(
        "A comprehensive regulatory compliance audit must cover all applicable federal, state, "
        "and local regulatory requirements. Outstanding violations, pending enforcement actions, "
        "and compliance gaps should be identified and quantified as potential liabilities."
    ),
    reasoning_framework=(
        "Oil and gas operations are subject to overlapping federal, state, and local regulations. "
        "Due diligence must verify compliance across all jurisdictions: (1) State oil and gas "
        "commission — drilling permits, completion reports, production reports, well tests, "
        "spacing orders, allowables, flaring permits, H2S plans. (2) State environmental "
        "agency — air permits, water discharge permits, waste disposal permits, spill reports. "
        "(3) Federal agencies if applicable — BLM (federal leases), EPA (air/water), OSHA "
        "(safety), PHMSA (pipelines), BSEE (offshore). (4) Local permits — road use agreements, "
        "county permits, zoning compliance. Key regulatory risks include: outstanding violations "
        "with pending penalties, expired permits not renewed, required reports not filed, "
        "non-compliant equipment (tank battery emissions, flaring without permit), and "
        "undisclosed spills or releases. The regulatory compliance status directly affects "
        "operability — non-compliant properties may face shut-in orders, production curtailment, "
        "or denial of new permit applications. Many states now maintain online databases of "
        "violations and enforcement actions that should be checked during diligence."
    ),
    key_factors=[
        "Outstanding violations and pending enforcement actions",
        "Permit compliance status (drilling, environmental, pipeline)",
        "Required report filing status (production, injection, emissions)",
        "Flaring compliance and methane emissions regulations",
        "Financial assurance (bonds, letters of credit) adequacy",
        "Operator qualification and P-4/P-5 filing status (Texas)",
        "Federal lease compliance (APD, sundry notices, royalty reporting)",
    ],
    primary_authority=[
        "State oil and gas conservation statutes and regulations",
        "Clean Air Act / Clean Water Act (federal environmental)",
        "BLM regulations (43 CFR Part 3160 et seq.)",
        "OSHA 29 CFR 1910 (general industry safety)",
    ],
    burden_holder="Buyer to identify regulatory risks; seller to disclose known violations.",
    adversary_position=(
        "Seller may characterize minor violations as routine operational matters and argue "
        "that regulatory compliance is the responsibility of the post-closing operator."
    ),
    counter_arguments=[
        "Outstanding violations may result in successor liability for the buyer.",
        "Regulatory agencies may impose conditions on operator transfer that delay closing.",
        "Non-compliant operations may face shut-in orders that eliminate cash flow.",
        "Undisclosed environmental releases may trigger CERCLA or state cleanup liability.",
        "Federal lease compliance issues can result in lease cancellation.",
    ],
    resolution_strategy=(
        "Search state and federal databases for violations and enforcement actions. Request "
        "seller's compliance correspondence files. Verify permit status for all operations. "
        "Quantify potential penalties for outstanding violations. Include regulatory compliance "
        "representations in PSA. Negotiate escrow for unresolved violations."
    ),
    entity_scope="All regulated operations in acquisition",
    confidence=ConfidenceLevel.DEFENSIBLE,
    confidence_stratification="Regulatory records are publicly available; compliance status verifiable.",
    controlling_precedent="State and federal regulatory statutes and enforcement precedent",
    issue_category=IssueCategory.REGULATORY_AUDIT,
    position_zone=PositionZone.BUYER,
    interaction_edges=["phase_i_esa_scope_and_limitations", "operator_qualification_review"],
))

# ─────────────────────────────────────────────────────────────────────────────
# 4. PRODUCTION ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────

_register(DoctrineBlock(
    topic="production_decline_curve_review",
    keywords=["decline curve", "DCA", "production forecast", "Arps", "b-factor", "EUR", "type curve"],
    conclusion_template=(
        "Decline curve analysis is the primary method for forecasting future production and "
        "estimating remaining reserves. The buyer should independently verify the seller's "
        "decline assumptions and compare with offset wells to validate EUR estimates."
    ),
    reasoning_framework=(
        "Arps decline curve equations (exponential, hyperbolic, harmonic) remain the standard "
        "methodology for conventional wells. For unconventional wells (horizontal multi-stage "
        "fracs), modified hyperbolic decline with a terminal decline rate switch is standard. "
        "Key analysis steps: (1) Obtain monthly production data from state regulatory agency "
        "(independent of seller's data). (2) Normalize production for downtime, workovers, "
        "and artificial lift changes. (3) Fit decline parameters (qi, Di, b-factor) to "
        "historical data. (4) Compare fitted parameters to offset well performance. (5) For "
        "wells on artificial lift, evaluate pump efficiency and sustainability. (6) For gas "
        "wells, evaluate condensate yield trends and water production. (7) Consider operational "
        "upside — recompletions, artificial lift optimization, infill drilling. (8) Identify "
        "anomalous production — sudden rate increases may indicate cross-flow or mechanical "
        "issues. (9) Gas-to-oil ratio trends may indicate reservoir depletion stage. (10) Water "
        "cut trends inform remaining economic life and lifting cost trajectory. The buyer's "
        "independent engineer should provide reserve estimates using SEC or PRMS definitions "
        "appropriate for the transaction."
    ),
    key_factors=[
        "Accuracy of decline curve fit to historical production",
        "Comparison of seller's EUR estimates to independent analysis",
        "Offset well performance benchmarking",
        "Gas-to-oil ratio and water cut trends",
        "Artificial lift efficiency and sustainability",
        "Operational upside opportunities (recompletions, infill)",
        "Price assumptions underlying economic analysis",
    ],
    primary_authority=[
        "Arps, J.J. (1945) 'Analysis of Decline Curves' AIME Trans. 160:228-247",
        "SPE/WPC/AAPG PRMS (Petroleum Resources Management System)",
        "SEC Regulation S-X Rule 4-10 (reserve definitions for public companies)",
        "State production records (e.g., RRC production database in Texas)",
    ],
    burden_holder="Buyer should independently verify production data and decline assumptions.",
    adversary_position=(
        "Seller will use optimistic decline assumptions (lower b-factor, lower terminal "
        "decline) to maximize EUR and justify higher purchase price."
    ),
    counter_arguments=[
        "Seller's decline assumptions may not account for recent well performance deterioration.",
        "Type curves for new completions may not reflect actual well results in heterogeneous reservoirs.",
        "Artificial lift changes can mask true decline rate.",
        "Commingled production makes individual well analysis unreliable without allocation methodology.",
        "Price assumptions significantly impact economic reserves and NPV.",
    ],
    resolution_strategy=(
        "Obtain independent production data from state regulatory database. Perform independent "
        "DCA using standard methodology. Compare results to seller's reserve report. Identify "
        "and quantify differences. Adjust purchase price for any material variance in EUR."
    ),
    entity_scope="All producing properties",
    confidence=ConfidenceLevel.DEFENSIBLE,
    confidence_stratification="Standard engineering methodology; subject to technical judgment.",
    controlling_precedent="SPE/WPC PRMS guidelines; SEC reserve definitions",
    issue_category=IssueCategory.PRODUCTION_ANALYSIS,
    position_zone=PositionZone.BUYER,
    interaction_edges=["reserve_estimation_methodology", "held_by_production_analysis"],
))

# ─────────────────────────────────────────────────────────────────────────────
# 5. RESERVE ESTIMATION
# ─────────────────────────────────────────────────────────────────────────────

_register(DoctrineBlock(
    topic="reserve_estimation_methodology",
    keywords=["reserves", "SEC", "PRMS", "proved", "probable", "PDP", "PUD", "reserve report"],
    conclusion_template=(
        "Reserve estimation for acquisition due diligence should use consistent methodology "
        "across all evaluated properties. The buyer should engage an independent reserve "
        "engineer and reconcile differences between their estimates and the seller's reserve "
        "report before finalizing the purchase price."
    ),
    reasoning_framework=(
        "Reserve classification follows either SEC rules (for public company reporting) or "
        "PRMS (for commercial transactions). Key distinctions: (1) Proved Developed Producing "
        "(PDP) — the lowest-risk category, based on existing wells with established production "
        "history. PDP reserves carry the least uncertainty and highest value per BOE. (2) Proved "
        "Developed Non-Producing (PDNP) — behind-pipe or shut-in zones that require minimal "
        "capital to bring on production. (3) Proved Undeveloped (PUD) — locations with reasonable "
        "certainty of recovery that require significant capital (drilling and completion). SEC "
        "rules require that PUDs be developed within 5 years. (4) Probable — reserves that are "
        "less certain than proved, typically P50 estimates. (5) Possible — low-confidence estimates, "
        "typically P10. For acquisition pricing, the buyer should heavily weight PDP reserves "
        "(typically 80-100% of PDP PV-10) and discount PUD reserves (typically 0-30% of PUD "
        "PV-10) because PUD development requires future capital and carries execution risk. The "
        "reserve engineer's assumptions about commodity prices, operating costs, capital costs, "
        "and discount rates must be clearly stated and evaluated."
    ),
    key_factors=[
        "Reserve classification (PDP/PDNP/PUD/Probable/Possible)",
        "Commodity price assumptions (SEC pricing vs. strip pricing vs. flat pricing)",
        "Operating cost assumptions and trends",
        "Capital cost assumptions for PUD development",
        "Discount rate applied (SEC uses 10%; commercial transactions may vary)",
        "Reserve-to-production ratio comparison with peers",
        "Reconciliation between seller's and buyer's reserve estimates",
    ],
    primary_authority=[
        "SEC Regulation S-X Rule 4-10 (reserve definitions)",
        "SPE/WPC/AAPG/SPEE PRMS (2018 edition)",
        "SEC Staff Accounting Bulletin Topic 12",
        "SPEE Recommended Evaluation Practices",
    ],
    burden_holder="Buyer should independently estimate reserves; differences negotiated pre-closing.",
    adversary_position=(
        "Seller will present reserves using the most favorable assumptions to maximize valuation."
    ),
    counter_arguments=[
        "SEC pricing (12-month average) may differ significantly from current strip pricing.",
        "PUD locations may not meet SEC's 5-year development requirement.",
        "Operating cost assumptions may not reflect current inflation in oilfield services.",
        "Type curves applied to PUD locations may overstate expected performance.",
        "Reserve engineers may have conflicts of interest if engaged by seller.",
    ],
    resolution_strategy=(
        "Engage independent reserve engineer. Use consistent assumptions for all properties. "
        "Compare results to seller's report. Focus valuation on PDP and risk-adjust PUD. "
        "Use current strip pricing for commercial valuation. Include reserve contingency "
        "in purchase price negotiation."
    ),
    entity_scope="All producing and undeveloped properties",
    confidence=ConfidenceLevel.DEFENSIBLE,
    confidence_stratification="Standard industry methodology; uncertainty quantifiable by category.",
    controlling_precedent="SEC reserve rules; PRMS; SPEE recommended practices",
    issue_category=IssueCategory.RESERVE_ESTIMATION,
    position_zone=PositionZone.BUYER,
    interaction_edges=["production_decline_curve_review", "closing_adjustments_methodology"],
))

# ─────────────────────────────────────────────────────────────────────────────
# 6. LEASE STATUS
# ─────────────────────────────────────────────────────────────────────────────

_register(DoctrineBlock(
    topic="held_by_production_analysis",
    keywords=["HBP", "held by production", "paying quantities", "habendum", "primary term", "cessation"],
    conclusion_template=(
        "Verification of held-by-production (HBP) status is critical because a lease that has "
        "terminated for failure to produce in paying quantities reverts to the lessor, and the "
        "buyer would acquire nothing. Production in paying quantities is determined by whether "
        "revenues exceed operating costs, excluding the cost of drilling."
    ),
    reasoning_framework=(
        "The habendum clause of an oil and gas lease grants the lease for a primary term and "
        "'so long thereafter as oil, gas, or other minerals are produced in paying quantities.' "
        "After expiration of the primary term, continued lease validity depends on continuous "
        "production in paying quantities. Key considerations: (1) 'Paying quantities' means "
        "revenue from production exceeds direct lifting costs — a marginal well test, not a "
        "return-on-investment test. (2) The test is applied over a reasonable period, not on a "
        "month-to-month basis. Seasonal fluctuations and temporary operational issues do not "
        "terminate a lease. (3) Temporary cessation of production may be excused if the lessee "
        "exercised due diligence to restore production within a reasonable time. Many leases "
        "now include specific cessation clauses (60 or 90 days). (4) Shut-in royalty clauses "
        "maintain leases when wells are shut in and capable of production but not marketed. "
        "(5) Continuous development clauses may require ongoing drilling to maintain leases. "
        "(6) Pooling and unitization may affect the production threshold for HBP. (7) For "
        "acquisitions, every lease beyond its primary term must be evaluated for HBP status. "
        "If a lease has marginal production, the buyer should assess the risk of lease "
        "termination and potential lessor challenge."
    ),
    key_factors=[
        "Current production volumes and revenue vs. direct lifting costs",
        "Duration and consistency of production history",
        "Any cessation of production periods and compliance with cessation clauses",
        "Shut-in royalty payment compliance for non-producing wells",
        "Continuous development clause requirements",
        "Lessor correspondence or challenges to HBP status",
        "Pooling/unitization compliance for multi-lease units",
    ],
    primary_authority=[
        "Clifton v. Koontz, 160 Tex. 82 (1959) — paying quantities standard",
        "Hydrocarbon Mgmt. v. Tracker Exploration, 861 S.W.2d 427 (Tex. App. 1993)",
        "State-specific lease termination statutes",
        "Williams & Meyers, Oil and Gas Law, Chapter 6",
    ],
    burden_holder="Lessee (seller/buyer post-closing) bears burden of proving HBP status.",
    adversary_position=(
        "Lessor may argue that marginal production does not constitute paying quantities and "
        "seek judicial declaration of lease termination."
    ),
    counter_arguments=[
        "The paying quantities test considers a reasonable time period, not isolated months of loss.",
        "Temporary cessation is excused if lessee acts diligently to restore production.",
        "Shut-in royalty payments must be timely and in the correct amount — late payment may not cure.",
        "Some courts apply a subjective 'reasonably prudent operator' test in addition to the economic test.",
        "Pooling may satisfy HBP if any well in the pooled unit produces in paying quantities.",
    ],
    resolution_strategy=(
        "Obtain production records for all leases beyond primary term. Calculate revenue vs. "
        "lifting costs for each lease. Identify any cessation periods and evaluate compliance "
        "with cessation clauses. Verify shut-in royalty payments. Flag marginal leases for "
        "further analysis. Obtain estoppel certificates from lessors where possible."
    ),
    entity_scope="All leases beyond primary term",
    confidence=ConfidenceLevel.DEFENSIBLE,
    confidence_stratification="Well-established case law; factual analysis of production records.",
    controlling_precedent="Clifton v. Koontz; state-specific lease termination law",
    issue_category=IssueCategory.LEASE_STATUS,
    position_zone=PositionZone.BUYER,
    interaction_edges=["production_decline_curve_review", "nri_working_interest_verification"],
))

_register(DoctrineBlock(
    topic="lease_expiration_risk",
    keywords=["lease expiration", "primary term", "extension", "continuous drilling", "top lease", "pooling deadline"],
    conclusion_template=(
        "Leases approaching primary term expiration represent both risk and opportunity. The "
        "buyer must verify whether extension provisions have been properly exercised and whether "
        "the seller has complied with all conditions for maintaining the lease."
    ),
    reasoning_framework=(
        "Leases within their primary term will expire at the end of that term unless extended "
        "by: (1) Commencement or completion of drilling operations. (2) Production in paying "
        "quantities. (3) Exercise of an option to extend. (4) Payment of shut-in royalties. "
        "(5) Continuous drilling obligations. Each extension mechanism has specific requirements "
        "that must be strictly complied with. For example, 'commencement of drilling operations' "
        "may require actual spudding of a well versus mere site preparation, depending on lease "
        "language and state law. Due diligence for expiring leases must verify: (a) Exact "
        "primary term expiration date. (b) Whether any extension provisions have been properly "
        "exercised. (c) Whether delay rental payments are current. (d) Whether continuous "
        "drilling clauses have been satisfied. (e) Whether the lease has been pooled and whether "
        "the pooling was effective. (f) Whether top leases have been filed by competitors. "
        "Leases expiring during the diligence period or shortly after closing require immediate "
        "action — either drilling, extension, or acceptance of expiration risk."
    ),
    key_factors=[
        "Exact primary term expiration date and extension options",
        "Delay rental payment history and compliance",
        "Continuous drilling obligation compliance",
        "Pooling designation timing and validity",
        "Existence of top leases filed by competitors",
        "Planned drilling schedule relative to expiration dates",
        "Cost of re-leasing if lease expires (current bonus rates)",
    ],
    primary_authority=[
        "State-specific lease interpretation statutes",
        "Rogers v. Osborn, 152 Tex. 540 (1953) — lease commencement",
        "AAPL Form 675 lease provisions",
        "Williams & Meyers, Oil and Gas Law, Chapter 6",
    ],
    burden_holder="Lessee (seller) to demonstrate compliance with extension requirements.",
    adversary_position=(
        "Lessor and top-lessee may argue that extension requirements were not strictly "
        "satisfied and that the lease has terminated."
    ),
    counter_arguments=[
        "Courts strictly construe lease termination provisions in most jurisdictions.",
        "Minor irregularities in delay rental payments may not terminate the lease if promptly corrected.",
        "Pooling after primary term expiration may not save a lease that had already terminated.",
        "Continuous drilling obligations must be precisely analyzed against actual drilling timelines.",
        "Top leases create contingent interests that become effective only upon original lease termination.",
    ],
    resolution_strategy=(
        "Create a lease expiration schedule for all leases in the acquisition. Verify extension "
        "compliance for each lease. Identify leases requiring immediate drilling to maintain. "
        "Assess re-leasing costs for expiring leases. Include lease maintenance representations "
        "in PSA. Require seller to maintain all leases through closing."
    ),
    entity_scope="All leases within or approaching primary term expiration",
    confidence=ConfidenceLevel.DEFENSIBLE,
    confidence_stratification="Lease interpretation is fact-specific but guided by established precedent.",
    controlling_precedent="State lease termination law; Rogers v. Osborn",
    issue_category=IssueCategory.LEASE_STATUS,
    position_zone=PositionZone.BUYER,
    interaction_edges=["held_by_production_analysis", "pooling_unitization_compliance"],
))

_register(DoctrineBlock(
    topic="pooling_unitization_compliance",
    keywords=["pooling", "unitization", "unit", "spacing", "compulsory pooling", "force pooling", "PA designation"],
    conclusion_template=(
        "Pooling and unitization designations must be verified for regulatory compliance, proper "
        "authority, and correct allocation of production. Invalid pooling can affect lease status, "
        "NRI calculations, and regulatory standing."
    ),
    reasoning_framework=(
        "Pooling combines multiple tracts or leases into a single drilling or spacing unit. "
        "Unitization combines multiple leases for secondary or tertiary recovery operations. "
        "Due diligence must verify: (1) Whether pooling was voluntary (per lease authority) or "
        "compulsory (by state order). (2) Whether the lease granting pooling authority has been "
        "properly exercised within any time or size limitations. (3) Whether the pooled unit "
        "conforms to state spacing requirements. (4) Whether production from any well in the "
        "pooled unit maintains all leases included in the pool. (5) Whether pooling was "
        "exercised in good faith (Amoco v. Thompson doctrine in Texas — pooling must not be "
        "done in bad faith to maintain a lease without intent to develop). (6) Whether "
        "compulsory pooling orders are final and non-appealable. (7) For unitization, whether "
        "the unit agreement has been properly ratified by the required percentage of interest "
        "owners. (8) Participating area designations within units — only wells within the PA "
        "contribute to production allocation. (9) Unit operating agreement terms — overhead "
        "charges, voting requirements, surrender provisions."
    ),
    key_factors=[
        "Lease pooling authority — size limitations, timing restrictions",
        "State spacing requirements for the formation",
        "Good faith exercise of pooling authority",
        "Compulsory pooling order finality",
        "Unit ratification percentage achieved",
        "Participating area designations and allocation methodology",
        "Cross-unit well considerations",
    ],
    primary_authority=[
        "Amoco Prod. Co. v. Thompson, 516 S.W.2d 396 (Tex. 1974) — good faith pooling",
        "State spacing and pooling statutes (e.g., Tex. Nat. Res. Code Ch. 102)",
        "State compulsory pooling statutes (e.g., OCC pooling orders in Oklahoma)",
        "Model Form Unit Operating Agreement (AAPL/COPAS)",
    ],
    burden_holder="Lessee to demonstrate valid pooling; regulatory agency for compulsory orders.",
    adversary_position=(
        "Non-pooled interest owners or lessors may challenge pooling as invalid due to "
        "bad faith, exceeding lease authority, or procedural defect."
    ),
    counter_arguments=[
        "Pooling designations filed of record are presumed valid until challenged.",
        "Compulsory pooling orders may be challenged on procedural or constitutional grounds.",
        "Bad faith pooling can result in lease termination — high-risk issue.",
        "Cross-unit wells create complex allocation issues that must be separately analyzed.",
        "Participating area changes can significantly affect allocation of production.",
    ],
    resolution_strategy=(
        "Review all pooling designations and unit agreements. Verify lease authority for "
        "voluntary pooling. Check spacing orders and PA designations. Confirm production "
        "allocation methodology. Flag any pooling challenges or disputes."
    ),
    entity_scope="All pooled and unitized interests",
    confidence=ConfidenceLevel.DEFENSIBLE,
    confidence_stratification="Well-established regulatory framework; fact-specific analysis required.",
    controlling_precedent="Amoco v. Thompson; state spacing and pooling statutes",
    issue_category=IssueCategory.LEASE_STATUS,
    position_zone=PositionZone.NEUTRAL,
    interaction_edges=["held_by_production_analysis", "nri_working_interest_verification"],
))

# ─────────────────────────────────────────────────────────────────────────────
# 7. LIEN & ENCUMBRANCE
# ─────────────────────────────────────────────────────────────────────────────

_register(DoctrineBlock(
    topic="lien_encumbrance_search",
    keywords=["lien", "UCC", "security interest", "mortgage", "deed of trust", "judgment", "tax lien", "financing statement"],
    conclusion_template=(
        "A comprehensive lien and encumbrance search must cover county real property records, "
        "UCC filings at both state and county levels, federal and state tax liens, judgment "
        "liens, and any other encumbrances that could affect the buyer's acquired interest."
    ),
    reasoning_framework=(
        "Oil and gas assets are commonly subject to multiple layers of encumbrances: "
        "(1) Mortgages and deeds of trust securing reserve-based lending facilities. "
        "(2) UCC-1 financing statements covering personal property (equipment, accounts, "
        "production proceeds). (3) Federal tax liens filed by the IRS. (4) State tax liens "
        "for severance, production, or ad valorem taxes. (5) Mechanics' and materialmen's "
        "liens from service providers. (6) Judgment liens from litigation. (7) Production "
        "payment liens (volumetric or dollar-denominated). (8) Net profits interests that "
        "may have priority characteristics. Due diligence must search all relevant filing "
        "locations — UCC filings at the state level (Secretary of State) and real property "
        "liens at the county level. For multi-state acquisitions, searches must cover every "
        "state and county where assets are located. The PSA typically requires seller to "
        "deliver assets free and clear of all liens (other than permitted encumbrances). "
        "Permitted encumbrances must be clearly defined and limited. Seller's lender must "
        "provide lien releases at or before closing."
    ),
    key_factors=[
        "Reserve-based lending facility lien release timing",
        "UCC-1 filing currency (continuation statements filed timely)",
        "Federal and state tax lien status",
        "Mechanics' lien potential from recent service work",
        "Judgment lien search in all relevant jurisdictions",
        "Production payment and net profits interest priority",
        "Cross-collateralization across multiple asset packages",
    ],
    primary_authority=[
        "UCC Article 9 (secured transactions)",
        "State recording statutes for real property liens",
        "IRC Section 6321-6323 (federal tax liens)",
        "State mechanics' lien statutes",
    ],
    burden_holder="Seller to deliver title free of liens; buyer to verify through independent search.",
    adversary_position=(
        "Seller may claim all liens will be released at closing without providing evidence "
        "of lender consent or payoff arrangements."
    ),
    counter_arguments=[
        "Lien releases may not be obtained before closing — escrow or holdback may be needed.",
        "UCC continuation statements may create perpetual liens if not properly terminated.",
        "Federal tax liens have special priority rules that override normal recording acts.",
        "Mechanics' liens may be filed after closing for work performed pre-closing.",
        "Cross-collateralization provisions may prevent release of individual assets.",
    ],
    resolution_strategy=(
        "Conduct UCC searches at state SOS level and county recorder level. Search federal "
        "and state tax lien records. Obtain judgment lien search. Require seller to provide "
        "payoff letters and lien release commitments before closing. Hold back from purchase "
        "price sufficient funds to ensure lien release."
    ),
    entity_scope="All assets in acquisition",
    confidence=ConfidenceLevel.DEFENSIBLE,
    confidence_stratification="Lien searches are factual and verifiable; priority rules well-established.",
    controlling_precedent="UCC Article 9; state recording acts; IRC lien priority",
    issue_category=IssueCategory.LIEN_ENCUMBRANCE,
    position_zone=PositionZone.BUYER,
    interaction_edges=["title_opinion_standard_of_review", "closing_adjustments_methodology"],
))

# ─────────────────────────────────────────────────────────────────────────────
# 8. LITIGATION REVIEW
# ─────────────────────────────────────────────────────────────────────────────

_register(DoctrineBlock(
    topic="pending_litigation_review",
    keywords=["litigation", "lawsuit", "pending claims", "demand letter", "class action", "royalty dispute"],
    conclusion_template=(
        "All pending, threatened, or reasonably anticipated litigation involving the assets "
        "or the seller must be identified and evaluated. Litigation liability allocation between "
        "buyer and seller should be clearly addressed in the PSA."
    ),
    reasoning_framework=(
        "Litigation review in oil and gas acquisitions covers: (1) Pending lawsuits involving "
        "the assets — title suits, royalty disputes, surface damage claims, environmental "
        "claims, personal injury, contractual disputes. (2) Threatened litigation — demand "
        "letters, regulatory enforcement notices, audit findings. (3) Anticipated litigation — "
        "known disputes that have not yet resulted in formal claims. (4) Class actions — "
        "royalty class actions are increasingly common, particularly regarding deductions from "
        "royalty payments, gas quality adjustments, and marketing fees. (5) Qui tam / False "
        "Claims Act — for federal lease royalty underpayment. Due diligence should include: "
        "search of court records in all relevant jurisdictions (state and federal), review of "
        "seller's litigation files and correspondence with counsel, inquiry about insurance "
        "coverage for pending claims, and assessment of potential exposure. The PSA typically "
        "allocates pre-effective date litigation to seller and post-effective date litigation "
        "to buyer, with specific provisions for straddling claims."
    ),
    key_factors=[
        "Material pending lawsuits and their current status",
        "Demand letters and threatened claims",
        "Royalty class action exposure",
        "Environmental enforcement actions",
        "Insurance coverage for pending claims",
        "Settlement history and outstanding settlement obligations",
        "Litigation reserve adequacy",
    ],
    primary_authority=[
        "Federal Rules of Civil Procedure (federal court litigation)",
        "State civil procedure rules",
        "State royalty payment statutes (e.g., Tex. Nat. Res. Code Section 91.402)",
        "CERCLA cost recovery actions (42 U.S.C. Section 9607)",
    ],
    burden_holder="Seller to disclose known litigation; buyer to conduct independent search.",
    adversary_position=(
        "Seller may characterize pending claims as frivolous or routine, and may resist "
        "disclosure of threatened litigation based on attorney-client privilege."
    ),
    counter_arguments=[
        "Seller's characterization of claims as 'frivolous' should not be accepted without independent evaluation.",
        "Attorney-client privilege does not excuse disclosure of the existence of pending claims.",
        "Insurance coverage must be verified independently — carrier may deny coverage.",
        "Class action exposure may not be apparent from individual case review.",
        "Successor liability may apply to buyer for pre-closing environmental and safety claims.",
    ],
    resolution_strategy=(
        "Search federal (PACER) and state court records. Request seller's litigation log "
        "and demand letter files. Interview seller's counsel regarding outstanding claims. "
        "Evaluate insurance coverage. Quantify potential exposure for each material claim. "
        "Negotiate indemnification and escrow for pre-effective date claims."
    ),
    entity_scope="All litigation involving acquired assets or seller entity",
    confidence=ConfidenceLevel.DEFENSIBLE,
    confidence_stratification="Court records are public; litigation evaluation involves judgment.",
    controlling_precedent="Federal and state civil procedure; successor liability doctrine",
    issue_category=IssueCategory.LITIGATION_REVIEW,
    position_zone=PositionZone.BUYER,
    interaction_edges=["indemnification_provisions", "reps_and_warranties_analysis"],
))

# ─────────────────────────────────────────────────────────────────────────────
# 9. PREFERENTIAL RIGHTS
# ─────────────────────────────────────────────────────────────────────────────

_register(DoctrineBlock(
    topic="rofr_preferential_purchase_rights",
    keywords=["ROFR", "right of first refusal", "preferential purchase", "PPR", "preemptive right", "tag-along"],
    conclusion_template=(
        "Preferential purchase rights (PPR/ROFR) attached to oil and gas assets can significantly "
        "delay closing, reduce the asset package available for sale, and create valuation disputes. "
        "PPR obligations must be identified early and the election/waiver process managed proactively."
    ),
    reasoning_framework=(
        "PPRs are commonly found in joint operating agreements (JOAs), partnership agreements, "
        "farmout agreements, and some oil and gas leases. When a working interest owner proposes "
        "to sell, the PPR holder has the right to purchase the interest on the same terms as "
        "the proposed sale to a third party. Key issues: (1) Scope of the PPR — does it cover "
        "all transfers or only voluntary sales? (2) Package vs. piecemeal — can the PPR holder "
        "cherry-pick specific assets from a package deal? (3) Valuation — if the sale is a "
        "package, how is value allocated to the PPR-encumbered asset? (4) Notice requirements — "
        "what information must be provided to the PPR holder? (5) Election period — typically "
        "30 days from notice. (6) Waiver — PPR holders who do not respond within the election "
        "period are deemed to have waived. (7) Impact on closing timeline — PPR elections may "
        "extend closing. (8) Exercise — if a PPR is exercised, the asset is excluded from the "
        "sale and the purchase price is adjusted. The PSA should address: PPR identification "
        "responsibility, notice process, value allocation methodology, closing condition "
        "regarding PPR waivers, and price adjustment for exercised PPRs."
    ),
    key_factors=[
        "Number and scope of PPRs across the asset package",
        "PPR holder identity and likelihood of exercise",
        "Value allocation methodology for package deals",
        "Notice requirements and election periods",
        "Impact on purchase price and asset package integrity",
        "Whether PPR applies to entity-level transactions",
        "Historical PPR exercise patterns by same holder",
    ],
    primary_authority=[
        "AAPL Form 610 Model Operating Agreement (Article VIII.F)",
        "State partnership and LLC statutes (right of first offer/refusal)",
        "Contractual PPR provisions in specific JOAs",
        "Mountain Gathering LLC v. EQT Prod. Co., 392 F.Supp.3d 638 (S.D.W.Va. 2019)",
    ],
    burden_holder="Seller to identify PPRs and deliver proper notice; PPR holder to elect or waive.",
    adversary_position=(
        "PPR holder may demand additional information or argue that notice was inadequate to "
        "delay the election period and gain negotiating leverage."
    ),
    counter_arguments=[
        "Package deal valuation methodology may be disputed — PPR holder wants low allocation.",
        "Entity-level transactions may not trigger PPRs even though economic effect is same as asset sale.",
        "PPR provisions vary significantly between contracts — no standard language.",
        "Late or defective notice may restart the election period.",
        "PPR holder exercise at allocated value may cherry-pick the best assets.",
    ],
    resolution_strategy=(
        "Compile complete PPR inventory from all contracts. Develop consistent value allocation "
        "methodology defensible under each contract. Prepare PPR notices early in the process. "
        "Track election periods and responses. Adjust purchase price for any exercised PPRs. "
        "Include closing condition that aggregate PPR exercises do not exceed a materiality "
        "threshold."
    ),
    entity_scope="All interests subject to PPR/ROFR provisions",
    confidence=ConfidenceLevel.DEFENSIBLE,
    confidence_stratification="Contract-specific analysis; well-established legal principles.",
    controlling_precedent="Specific contract language; AAPL Form 610 Article VIII.F",
    issue_category=IssueCategory.PREFERENTIAL_RIGHTS,
    position_zone=PositionZone.SELLER,
    interaction_edges=["consent_to_assign_requirements", "closing_adjustments_methodology"],
))

# ─────────────────────────────────────────────────────────────────────────────
# 10. CONSENT TO ASSIGN
# ─────────────────────────────────────────────────────────────────────────────

_register(DoctrineBlock(
    topic="consent_to_assign_requirements",
    keywords=["consent", "assign", "assignment", "transfer restriction", "operator approval", "landlord consent"],
    conclusion_template=(
        "Consent-to-assign requirements in leases, JOAs, and other contracts can block or delay "
        "the transfer of assets. Due diligence must identify all consent requirements and "
        "assess the likelihood and timeline for obtaining required consents."
    ),
    reasoning_framework=(
        "Consent requirements arise from: (1) Lease provisions requiring lessor consent for "
        "assignment — some leases require consent only for sublease while permitting assignment. "
        "(2) JOA provisions requiring operator consent or governing body approval for transfers "
        "to non-qualified parties. (3) Federal lease requirements — BLM requires qualification "
        "of transferee and processing of assignment applications. (4) State lease requirements — "
        "some state leases require agency approval. (5) Pipeline and gathering agreements with "
        "assignment restrictions. (6) Surface use agreements with landowner consent requirements. "
        "(7) Partnership or LLC operating agreements with consent provisions. The distinction "
        "between 'consent not to be unreasonably withheld' and absolute consent requirements "
        "is critical. Unreasonable withholding of consent may be challenged, but absolute "
        "consent provisions give the counterparty a veto. Many assignment provisions include "
        "exceptions for affiliates, and the structure of the acquisition may be designed to "
        "utilize affiliate exceptions."
    ),
    key_factors=[
        "Number and type of consents required",
        "Standard of consent — absolute vs. reasonableness",
        "Timeline for obtaining consents relative to closing schedule",
        "Consequences of failing to obtain consent — void transfer vs. breach of covenant",
        "Affiliate transfer exceptions that may eliminate consent requirement",
        "Federal and state agency processing times for assignment applications",
        "Whether consent provisions apply to entity-level transactions",
    ],
    primary_authority=[
        "Lease-specific consent provisions",
        "AAPL Form 610 Article VIII.B (assignment provisions)",
        "43 CFR Part 3106 (BLM lease assignment regulations)",
        "State oil and gas lease assignment regulations",
    ],
    burden_holder="Seller to obtain required consents; buyer to qualify as acceptable transferee.",
    adversary_position=(
        "Consent holders may withhold consent to extract concessions or delay closing."
    ),
    counter_arguments=[
        "Unreasonable withholding of consent may be actionable under contract or equity.",
        "Some assignments are effective without consent under state law even if prohibited by contract.",
        "Entity-level transactions may avoid consent triggers depending on contract language.",
        "Federal agency processing delays are common — build into closing timeline.",
        "Failure to obtain consent for non-material contracts may be accepted as a closing condition carve-out.",
    ],
    resolution_strategy=(
        "Inventory all consent requirements by contract. Categorize as absolute vs. reasonableness. "
        "Initiate consent process early. Identify affiliate exceptions. Structure transaction "
        "to minimize consent requirements. Include consent as a closing condition with "
        "materiality threshold."
    ),
    entity_scope="All contracts with assignment restrictions",
    confidence=ConfidenceLevel.DEFENSIBLE,
    confidence_stratification="Contract interpretation is fact-specific; consent process is procedural.",
    controlling_precedent="Specific contract language; state assignment law",
    issue_category=IssueCategory.CONSENT_ASSIGN,
    position_zone=PositionZone.NEUTRAL,
    interaction_edges=["rofr_preferential_purchase_rights", "change_of_control_provisions"],
))

# ─────────────────────────────────────────────────────────────────────────────
# 11. CHANGE OF CONTROL
# ─────────────────────────────────────────────────────────────────────────────

_register(DoctrineBlock(
    topic="change_of_control_provisions",
    keywords=["change of control", "COC", "deemed assignment", "indirect transfer", "stock sale", "entity transaction"],
    conclusion_template=(
        "Change of control provisions can be triggered by entity-level transactions even when "
        "no direct asset assignment occurs. Due diligence must identify all contracts with COC "
        "provisions and assess whether the proposed transaction triggers them."
    ),
    reasoning_framework=(
        "An entity-level acquisition (stock purchase, membership interest purchase, merger) "
        "does not involve a direct assignment of assets but may trigger change-of-control "
        "provisions in underlying contracts. COC provisions are common in: (1) JOAs — may "
        "trigger consent requirements or preferential purchase rights. (2) Oil and gas leases — "
        "some leases restrict 'change in the beneficial ownership' of the lessee. (3) Pipeline "
        "and gathering agreements — COC may trigger renegotiation or termination rights. "
        "(4) Surface use agreements — landowners may have COC protections. (5) Credit facilities — "
        "borrowing base redetermination may be triggered. (6) Key employee agreements — change "
        "of control may trigger severance payments. The buyer's counsel must review every "
        "material contract for COC provisions. Structuring considerations may include: "
        "acquiring less than 50% to avoid triggering COC thresholds, using a merger "
        "structure that may not constitute a 'transfer,' or negotiating COC waivers "
        "pre-closing."
    ),
    key_factors=[
        "Contracts containing COC provisions and their trigger thresholds",
        "Whether transaction structure (asset vs. entity) triggers COC",
        "Consequences of triggering COC (consent, ROFR, termination, renegotiation)",
        "Ability to obtain COC waivers before closing",
        "Credit facility implications of COC",
        "Employee/management COC provisions (change of control payments)",
        "Multi-tier entity structures and indirect COC triggers",
    ],
    primary_authority=[
        "Specific contract COC provisions",
        "State corporate and LLC statutes (merger/conversion effects on contracts)",
        "UCC anti-assignment provisions vs. free transferability of property",
        "Federal lease assignment regulations (entity-level considerations)",
    ],
    burden_holder="Buyer to identify COC triggers; seller to obtain waivers where required.",
    adversary_position=(
        "Counterparties may argue that any change in ultimate beneficial ownership triggers COC, "
        "regardless of the transaction structure or ownership percentage change."
    ),
    counter_arguments=[
        "Many COC provisions require a specific percentage change (e.g., 50% or more).",
        "Mergers may not constitute 'assignments' under some contract interpretations.",
        "Anti-assignment provisions may be unenforceable under certain state laws.",
        "COC waivers may be obtainable with appropriate operator qualification assurances.",
        "Multi-tier ownership changes may not trigger COC if intermediate entities remain in place.",
    ],
    resolution_strategy=(
        "Review all material contracts for COC provisions. Map trigger thresholds against "
        "proposed transaction structure. Identify contracts requiring COC waiver. Initiate "
        "waiver process early. Consider alternative transaction structures to avoid triggers. "
        "Include COC waiver as a closing condition for material contracts."
    ),
    entity_scope="All contracts with COC provisions",
    confidence=ConfidenceLevel.DEFENSIBLE,
    confidence_stratification="Contract interpretation; structuring analysis is well-established.",
    controlling_precedent="Specific contract language; state entity law",
    issue_category=IssueCategory.CHANGE_OF_CONTROL,
    position_zone=PositionZone.BUYER,
    interaction_edges=["consent_to_assign_requirements", "rofr_preferential_purchase_rights"],
))

# ─────────────────────────────────────────────────────────────────────────────
# 12. AMI AGREEMENTS
# ─────────────────────────────────────────────────────────────────────────────

_register(DoctrineBlock(
    topic="ami_agreement_obligations",
    keywords=["AMI", "area of mutual interest", "acquisition notification", "after-acquired", "joint acquisition"],
    conclusion_template=(
        "AMI agreements obligate parties to offer jointly any interest acquired within a defined "
        "geographic area. Due diligence must identify all AMI obligations that may encumber "
        "the acquired assets or obligate the buyer post-closing."
    ),
    reasoning_framework=(
        "AMI provisions are common in exploration joint ventures, JOAs, and farmout agreements. "
        "The AMI obligates each party to offer the other a proportional interest in any "
        "acquisition within the defined area. Key analysis points: (1) Geographic scope — the "
        "AMI boundary must be precisely mapped. (2) Subject interest — does the AMI cover only "
        "working interests or also minerals, royalties, and overrides? (3) Duration — is the "
        "AMI perpetual, co-terminus with the JOA, or time-limited? (4) Notification requirements — "
        "what information and timing for offering interests? (5) Election period — time to "
        "accept or decline. (6) Cost allocation — does the electing party pay pro-rata of "
        "acquisition cost? (7) Exceptions — inter-company transfers, de minimis acquisitions, "
        "defensive leasing. For the buyer of AMI-encumbered assets: (a) the buyer may be "
        "obligated to offer interests in future acquisitions within the AMI area, and (b) the "
        "buyer may be entitled to participate in other parties' future acquisitions."
    ),
    key_factors=[
        "AMI geographic boundary definition and mapping",
        "Duration and termination provisions",
        "Types of interests covered (WI, MI, RI, ORRI)",
        "Notification and election mechanics",
        "Cost allocation for joint acquisitions",
        "Exceptions to AMI obligation",
        "Whether AMI runs with the land or is personal",
        "Number of AMI counterparties",
    ],
    primary_authority=[
        "Specific AMI agreement provisions",
        "JOA AMI articles (AAPL Form 610 may include AMI provisions)",
        "State partnership and JV law",
        "Williams & Meyers, Oil and Gas Law (AMI discussion)",
    ],
    burden_holder="Both parties obligated to comply with AMI provisions.",
    adversary_position=(
        "AMI counterparty may argue that the acquisition itself triggers AMI notification "
        "obligation, requiring offer of proportional interest."
    ),
    counter_arguments=[
        "Whether the acquisition triggers AMI depends on the specific AMI language and acquisition structure.",
        "Entity-level acquisitions may not trigger asset-level AMI provisions.",
        "AMI obligations may have been terminated by prior notice or passage of time.",
        "Exceptions for inter-company transfers may apply to the acquisition.",
        "AMI counterparty may lack financial capacity to participate.",
    ],
    resolution_strategy=(
        "Identify and map all AMI boundaries. Determine whether acquisition triggers AMI. "
        "Quantify exposure if AMI counterparties elect to participate. Include AMI "
        "representations in PSA. If material, provide AMI notices pre-closing."
    ),
    entity_scope="All interests within AMI boundaries",
    confidence=ConfidenceLevel.DEFENSIBLE,
    confidence_stratification="Contract-specific; AMI jurisprudence is limited but principles are clear.",
    controlling_precedent="Specific AMI agreement provisions; JV law",
    issue_category=IssueCategory.AMI_AGREEMENTS,
    position_zone=PositionZone.NEUTRAL,
    interaction_edges=["rofr_preferential_purchase_rights", "consent_to_assign_requirements"],
))

# ─────────────────────────────────────────────────────────────────────────────
# 13. DEFICIENCY & CURE
# ─────────────────────────────────────────────────────────────────────────────

_register(DoctrineBlock(
    topic="deficiency_identification_and_cure",
    keywords=["deficiency", "title defect", "curative", "cure period", "title requirement", "assertion period"],
    conclusion_template=(
        "The deficiency identification and cure process is the central mechanism for resolving "
        "title issues discovered during due diligence. The PSA defines the assertion period, "
        "cure period, materiality threshold, and remedies for uncured defects."
    ),
    reasoning_framework=(
        "The typical deficiency process: (1) Buyer conducts title examination during the "
        "diligence period. (2) Buyer asserts specific title defects before the defect "
        "assertion deadline, with each assertion describing the nature of the defect, the "
        "affected property, and the alleged impact on buyer's interest. (3) Seller has a "
        "cure period (typically 90-120 days) to cure defects. (4) Uncured defects are resolved "
        "by: (a) purchase price adjustment based on the defect value, (b) exclusion of the "
        "affected property, (c) indemnification by seller, or (d) mutual agreement. "
        "(5) Defect valuation methodology must be specified in the PSA — common approaches "
        "include: allocated value times NRI shortfall percentage, or present value of the "
        "lost interest stream. (6) Materiality threshold — defects below a per-property "
        "threshold (e.g., $50,000) or aggregate threshold (e.g., 5% of purchase price) may "
        "not be asserted. (7) Title benefits — the PSA should also address title benefits "
        "(where buyer's NRI exceeds scheduled NRI), which offset defect deductions."
    ),
    key_factors=[
        "Defect assertion deadline (typically 30-45 days before closing)",
        "Required content of defect notices",
        "Cure period duration and cure standard",
        "Defect valuation methodology",
        "Individual and aggregate materiality thresholds",
        "Title benefit offset provisions",
        "Remedies for uncured defects (price adjustment, exclusion, indemnification)",
        "Dispute resolution for contested defects",
    ],
    primary_authority=[
        "PSA defect provisions (Article-specific)",
        "AAPL Title Examination Standards",
        "State title standards",
        "Industry custom and practice",
    ],
    burden_holder="Buyer to assert defects timely; seller to cure within cure period.",
    adversary_position=(
        "Seller will challenge defect assertions as immaterial, incorrect, or waived "
        "due to untimely assertion."
    ),
    counter_arguments=[
        "Defect assertion must be specific — generic assertions may be rejected.",
        "Cure may not be possible for some defects (e.g., missing heirs, untraceable grantors).",
        "Title benefits should not be used to offset defects affecting different properties.",
        "Materiality thresholds must be applied consistently.",
        "Post-closing defect discovery should be covered by seller's representations.",
    ],
    resolution_strategy=(
        "Begin title examination early to maximize assertion period. Prepare detailed defect "
        "notices with supporting documentation. Track cure progress. Quantify defect values "
        "using PSA methodology. Negotiate in good faith on contested defects. Use dispute "
        "resolution mechanism for unresolved defects."
    ),
    entity_scope="All properties with title defects",
    confidence=ConfidenceLevel.DEFENSIBLE,
    confidence_stratification="Well-established industry process with clear contractual framework.",
    controlling_precedent="PSA provisions; AAPL Title Standards; state title law",
    issue_category=IssueCategory.DEFICIENCY_CURE,
    position_zone=PositionZone.BUYER,
    interaction_edges=["title_opinion_standard_of_review", "chain_of_title_gap_analysis", "nri_working_interest_verification"],
))

# ─────────────────────────────────────────────────────────────────────────────
# 14. PSA REVIEW
# ─────────────────────────────────────────────────────────────────────────────

_register(DoctrineBlock(
    topic="psa_structure_and_key_provisions",
    keywords=["PSA", "purchase agreement", "asset purchase", "closing conditions", "termination", "effective date"],
    conclusion_template=(
        "The PSA is the governing document for the acquisition. Due diligence must verify that "
        "the PSA adequately addresses all identified risks, properly allocates liability between "
        "buyer and seller, and includes appropriate conditions, representations, and remedies."
    ),
    reasoning_framework=(
        "Key PSA provisions for oil and gas acquisitions: (1) Effective Date vs. Closing Date — "
        "the effective date is when economic ownership transfers; the closing date is when legal "
        "title transfers. Revenue and expenses between effective and closing dates are adjusted "
        "through the settlement process. (2) Purchase Price and adjustments — upward adjustments "
        "(revenue received by seller post-effective date, capital expenditures by seller) and "
        "downward adjustments (operating expenses paid by seller, defect deductions, PPR "
        "exclusions). (3) Conditions to closing — regulatory approvals, PPR/consent waivers, "
        "no material adverse change, accuracy of representations. (4) Termination rights — "
        "aggregate defect threshold, failure to satisfy closing conditions, outside date. "
        "(5) Interim operations — seller's obligations between signing and closing (operate "
        "in ordinary course, maintain leases, not create new encumbrances). (6) Excluded "
        "assets — clearly define what is NOT being acquired. (7) Assumed obligations vs. "
        "retained obligations — post-effective date obligations assumed by buyer; pre-effective "
        "date obligations retained by seller (typically)."
    ),
    key_factors=[
        "Effective date and closing date relationship",
        "Purchase price adjustment mechanics",
        "Closing conditions and satisfaction timeline",
        "Termination triggers and termination fee",
        "Interim operations covenants",
        "Excluded assets and retained obligations",
        "Post-closing adjustment process and timeline",
        "Dispute resolution provisions (arbitration vs. litigation)",
    ],
    primary_authority=[
        "Industry-standard PSA forms (typically customized)",
        "State contract law (choice of law provision)",
        "UCC Article 2 (if applicable to equipment portion)",
        "M&A case law regarding material adverse effect and closing conditions",
    ],
    burden_holder="Both parties to satisfy their respective closing conditions.",
    adversary_position=(
        "Each party will negotiate PSA provisions to minimize their risk exposure and maximize "
        "flexibility to terminate or adjust."
    ),
    counter_arguments=[
        "Effective date selection significantly impacts settlement economics — earlier date favors buyer in rising price environment.",
        "Closing conditions should be objective and verifiable — subjective conditions create dispute risk.",
        "Termination fees must be reasonable — excessive fees may not be enforceable.",
        "Interim operations covenants must balance seller's operational flexibility with buyer's protection.",
        "Post-closing adjustment period should be sufficient to verify all adjustments (typically 90-180 days).",
    ],
    resolution_strategy=(
        "Review PSA with experienced oil and gas transaction counsel. Verify consistency "
        "between PSA provisions and due diligence findings. Ensure all identified risks are "
        "addressed through representations, indemnification, or closing conditions. Negotiate "
        "balanced provisions that protect buyer while giving seller reasonable assurance of closing."
    ),
    entity_scope="The acquisition transaction as a whole",
    confidence=ConfidenceLevel.DEFENSIBLE,
    confidence_stratification="Standard transactional practice; highly customized per deal.",
    controlling_precedent="State contract law; oil and gas M&A precedent",
    issue_category=IssueCategory.PSA_REVIEW,
    position_zone=PositionZone.NEUTRAL,
    interaction_edges=["closing_adjustments_methodology", "reps_and_warranties_analysis", "indemnification_provisions"],
))

_register(DoctrineBlock(
    topic="closing_adjustments_methodology",
    keywords=["closing adjustment", "settlement statement", "proration", "purchase price adjustment", "true-up", "PSS", "FSS"],
    conclusion_template=(
        "Closing adjustments reconcile economic ownership (effective date) with legal transfer "
        "(closing date). The preliminary settlement statement (PSS) establishes the closing "
        "payment; the final settlement statement (FSS) trues up within the post-closing "
        "adjustment period."
    ),
    reasoning_framework=(
        "The settlement process adjusts the base purchase price: UPWARD for: (a) revenue "
        "received by seller attributable to production after the effective date, (b) capital "
        "expenditures incurred by seller after the effective date per approved AFEs, (c) "
        "prepaid expenses extending past the effective date. DOWNWARD for: (a) operating "
        "expenses incurred and paid by seller for operations after the effective date, (b) "
        "proceeds from asset dispositions after the effective date, (c) title defect "
        "deductions, (d) environmental defect deductions, (e) PPR exclusion adjustments. "
        "The PSS is prepared by seller shortly before closing and verified by buyer. The "
        "closing amount = base price +/- PSS adjustments. Post-closing, buyer prepares (or "
        "seller prepares) the FSS using actual data (which may not be available at closing). "
        "Disagreements on the FSS are resolved per the PSA dispute resolution process. "
        "Timing considerations: JIB (joint interest billing) reconciliation, royalty suspense "
        "assumption, property tax proration, ad valorem tax proration, income tax deposits, "
        "and insurance premium allocation all require careful treatment."
    ),
    key_factors=[
        "Effective date to closing date time gap (longer = more adjustment complexity)",
        "Revenue proration methodology (entitlement vs. cash basis)",
        "Capital expenditure approval process during interim period",
        "Property and ad valorem tax proration",
        "Suspense account assumption and responsibility",
        "FSS preparation timeline and dispute resolution",
        "Interest on adjustment amounts",
        "Escrow for disputed adjustments",
    ],
    primary_authority=[
        "PSA settlement provisions (Article-specific)",
        "Industry practice (monthly proration from effective date)",
        "State ad valorem tax statutes",
        "Generally accepted accounting principles (GAAP)",
    ],
    burden_holder="Seller prepares PSS; buyer verifies; both parties agree on FSS.",
    adversary_position=(
        "Each party will calculate adjustments favorably — seller maximizes upward adjustments; "
        "buyer maximizes downward adjustments."
    ),
    counter_arguments=[
        "Revenue proration methodology (entitlement vs. cash) can produce materially different results.",
        "Capital expenditure adjustments should only include AFEs approved or consented to by buyer.",
        "Tax prorations must be based on actual assessments, not estimates.",
        "Suspense account assumptions should be clearly defined in the PSA.",
        "Post-closing adjustment period should be at least 120 days to allow for data verification.",
    ],
    resolution_strategy=(
        "Agree on detailed settlement methodology in PSA before signing. Build settlement "
        "model early in diligence to estimate closing adjustments. Prepare detailed PSS with "
        "supporting documentation. Verify seller's PSS calculations independently. Reserve "
        "rights for FSS adjustments on all items lacking final data."
    ),
    entity_scope="All financial aspects of the acquisition closing",
    confidence=ConfidenceLevel.DEFENSIBLE,
    confidence_stratification="Standard transactional process; methodology well-established.",
    controlling_precedent="PSA provisions; industry practice; GAAP",
    issue_category=IssueCategory.PSA_REVIEW,
    position_zone=PositionZone.NEUTRAL,
    interaction_edges=["psa_structure_and_key_provisions", "suspense_account_analysis"],
))

# ─────────────────────────────────────────────────────────────────────────────
# 15. REPS & WARRANTIES
# ─────────────────────────────────────────────────────────────────────────────

_register(DoctrineBlock(
    topic="reps_and_warranties_analysis",
    keywords=["representations", "warranties", "reps", "material adverse effect", "MAE", "disclosure schedule"],
    conclusion_template=(
        "Seller's representations and warranties provide contractual assurances about the "
        "condition of the assets, compliance with laws, and accuracy of information provided. "
        "These serve as both a diligence tool (through disclosure schedules) and a remedy "
        "mechanism (through indemnification for breaches)."
    ),
    reasoning_framework=(
        "Oil and gas acquisition reps fall into categories: (1) Fundamental reps — organization, "
        "authority, enforceability, no conflicts. These typically survive indefinitely. (2) Title "
        "reps — seller's ownership interest, no undisclosed encumbrances (may be qualified as "
        "'to seller's knowledge'). (3) Environmental reps — compliance with environmental laws, "
        "no undisclosed contamination, adequacy of P&A accruals. (4) Regulatory reps — compliance "
        "with oil and gas regulations, no outstanding violations, permits current. (5) Operational "
        "reps — wells drilled in compliance with permits, equipment in working condition, contracts "
        "current. (6) Tax reps — ad valorem and severance taxes paid, no audits. (7) Litigation "
        "reps — no pending or threatened litigation. (8) Financial reps — accuracy of production "
        "data and financial information provided. Knowledge qualifiers ('to seller's knowledge') "
        "significantly limit the scope of reps — buyer should negotiate for actual knowledge of "
        "named individuals, not just entity knowledge. Materiality qualifiers ('material', "
        "'Material Adverse Effect') also narrow the scope and should be clearly defined."
    ),
    key_factors=[
        "Scope of seller's knowledge qualifier (constructive vs. actual; named individuals)",
        "Materiality and MAE definition",
        "Disclosure schedule completeness and accuracy",
        "Survival periods for different categories of reps",
        "Fundamental vs. non-fundamental rep distinction",
        "Sandbagging vs. anti-sandbagging provisions",
        "Bring-down condition at closing",
    ],
    primary_authority=[
        "PSA representations articles",
        "Restatement (Second) of Contracts (warranty and representation doctrines)",
        "State fraud and misrepresentation statutes",
        "Acquisition Agreement case law (MAE jurisprudence)",
    ],
    burden_holder="Seller bears risk of inaccurate representations; buyer to diligence and verify.",
    adversary_position=(
        "Seller will seek to narrow reps with knowledge qualifiers, materiality thresholds, "
        "and short survival periods to limit post-closing exposure."
    ),
    counter_arguments=[
        "Knowledge qualifiers should include constructive knowledge to prevent willful ignorance.",
        "MAE definition should have specific carve-outs (commodity price changes, general industry conditions).",
        "Disclosure schedules must be complete — omissions may constitute breach.",
        "Survival periods should be sufficient for buyer to discover latent issues (minimum 12-18 months).",
        "Anti-sandbagging clause protects buyer who discovers rep breach during diligence but closes anyway.",
    ],
    resolution_strategy=(
        "Negotiate for broadest practicable reps. Push for actual knowledge of named senior "
        "officers. Define MAE clearly. Require complete disclosure schedules. Set survival "
        "periods matched to risk discovery timeline. Include sandbagging protection. Link "
        "rep breaches to indemnification provisions."
    ),
    entity_scope="All seller representations regarding acquired assets",
    confidence=ConfidenceLevel.DEFENSIBLE,
    confidence_stratification="Standard M&A practice; extensive jurisprudence.",
    controlling_precedent="State contract and fraud law; MAE case law (Akorn v. Fresenius)",
    issue_category=IssueCategory.REPS_WARRANTIES,
    position_zone=PositionZone.BUYER,
    interaction_edges=["indemnification_provisions", "psa_structure_and_key_provisions"],
))

# ─────────────────────────────────────────────────────────────────────────────
# 16. INDEMNIFICATION
# ─────────────────────────────────────────────────────────────────────────────

_register(DoctrineBlock(
    topic="indemnification_provisions",
    keywords=["indemnification", "indemnity", "hold harmless", "cap", "basket", "deductible", "escrow", "survival"],
    conclusion_template=(
        "Indemnification provisions allocate risk between buyer and seller for pre-closing "
        "liabilities and breaches of representations. The structure of caps, baskets, and "
        "survival periods determines the practical value of the indemnity."
    ),
    reasoning_framework=(
        "Indemnification in oil and gas acquisitions typically follows this structure: "
        "(1) Seller indemnifies buyer for: breaches of representations, pre-effective date "
        "obligations (including retained environmental liabilities), third-party claims arising "
        "from pre-closing operations, and specific identified liabilities. (2) Buyer indemnifies "
        "seller for: post-effective date obligations (assumed obligations), buyer's breaches "
        "of representations, and third-party claims arising from post-closing operations. "
        "(3) Limitations on indemnification: (a) Basket/deductible — claims must exceed a "
        "minimum threshold (typically 0.5-1.5% of purchase price) before indemnification kicks "
        "in. First-dollar vs. tipping basket distinction. (b) Cap — maximum aggregate "
        "indemnification (typically 10-20% of purchase price for non-fundamental reps; higher "
        "or uncapped for fundamental reps and fraud). (c) Survival — time period during which "
        "claims can be asserted (typically 12-24 months for non-fundamental reps; longer for "
        "fundamental, tax, and environmental reps). (d) Exclusions — consequential damages "
        "waiver, punitive damages waiver, materiality scrape for calculating damages. "
        "(4) Escrow/holdback — a portion of purchase price held in escrow to satisfy "
        "indemnification claims (common range: 5-15% of purchase price). (5) Special "
        "indemnities — identified liabilities with specific dollar caps or no cap."
    ),
    key_factors=[
        "Basket type (first-dollar/tipping vs. true deductible) and amount",
        "Cap amount (percentage of purchase price) and what is included/excluded",
        "Survival periods by rep category",
        "Consequential damages waiver scope",
        "Escrow amount, term, and release conditions",
        "Special indemnities for identified risks",
        "Indemnification claim process and timing requirements",
        "Insurance recovery offset provisions",
    ],
    primary_authority=[
        "PSA indemnification article",
        "Restatement (Third) of Torts: Apportionment of Liability",
        "State indemnification statutes (e.g., anti-indemnity statutes in oil and gas)",
        "UCC warranty and remedy provisions",
    ],
    burden_holder="Indemnified party to prove breach and damages; indemnifying party to cure or pay.",
    adversary_position=(
        "Seller seeks low cap, high basket, short survival, broad exclusions. Buyer seeks "
        "high cap, low basket, long survival, narrow exclusions."
    ),
    counter_arguments=[
        "Basket amount should reflect the deal size — too high eliminates practical remedy.",
        "Cap should be sufficient to cover reasonably anticipated claims — 10% minimum for most deals.",
        "Survival periods should align with the time needed to discover latent issues.",
        "Anti-indemnity statutes in some oil and gas states may limit indemnification scope.",
        "Escrow is critical for buyer protection when seller creditworthiness is uncertain.",
    ],
    resolution_strategy=(
        "Negotiate indemnification structure matched to deal risk profile. Set basket at "
        "0.5-1% of purchase price (tipping). Set cap at 15-20% for non-fundamental, higher "
        "for environmental. Survival 18-24 months minimum. Require escrow of 10% with 12-month "
        "release. Include special indemnities for identified high-risk items. Require "
        "representations and warranties insurance consideration."
    ),
    entity_scope="All post-closing liability allocation",
    confidence=ConfidenceLevel.DEFENSIBLE,
    confidence_stratification="Well-established M&A practice; quantifiable financial analysis.",
    controlling_precedent="PSA provisions; state indemnification law; anti-indemnity statutes",
    issue_category=IssueCategory.INDEMNIFICATION,
    position_zone=PositionZone.BUYER,
    interaction_edges=["reps_and_warranties_analysis", "psa_structure_and_key_provisions"],
))

# ─────────────────────────────────────────────────────────────────────────────
# 17. NRI/WI VERIFICATION
# ─────────────────────────────────────────────────────────────────────────────

_register(DoctrineBlock(
    topic="nri_working_interest_verification",
    keywords=["NRI", "net revenue interest", "working interest", "WI", "decimal interest", "division order"],
    conclusion_template=(
        "Verification of net revenue interest (NRI) and working interest (WI) is foundational "
        "to acquisition valuation. The scheduled NRI in the PSA must be reconciled against "
        "division orders, title opinions, and actual payment records."
    ),
    reasoning_framework=(
        "NRI verification involves: (1) Obtain the seller's schedule of NRI and WI for each "
        "well/unit. (2) Reconcile scheduled NRI against: (a) Current division orders on file "
        "with purchasers and operators. (b) Title opinions (if available). (c) Actual revenue "
        "payment records. (d) State production tax allocation records. (3) Calculate expected "
        "NRI from WI less all burdens: NRI = WI × (1 - Royalty - ORRI - Other Burdens). "
        "(4) Identify variances between scheduled, calculated, and paid NRI. (5) Variances "
        "exceeding the defect threshold (typically 0.01 or 0.005 NRI) are asserted as title "
        "defects. (6) NRI verification must be performed on a well-by-well basis, not in "
        "aggregate, because averaging can mask material defects in individual wells. (7) For "
        "units, verify allocation among tracts within the unit and compliance with the unit "
        "operating agreement. (8) Verify that division orders reflect the most recent title "
        "opinion and that no interim conveyances have changed the interest since the last "
        "title opinion."
    ),
    key_factors=[
        "Scheduled NRI accuracy by well/unit",
        "Division order vs. title opinion reconciliation",
        "Actual payment records vs. division orders",
        "Variance threshold for defect assertion",
        "Treatment of underpayment and overpayment",
        "Impact of NRI variance on property valuation",
        "Suspense amounts related to NRI disputes",
    ],
    primary_authority=[
        "Division order statutes (e.g., Tex. Nat. Res. Code Section 91.402)",
        "Title opinions underlying current division orders",
        "PSA NRI schedules and defect provisions",
        "AAPL Division Order Form 15",
    ],
    burden_holder="Buyer to verify NRI; seller to substantiate scheduled NRI.",
    adversary_position=(
        "Seller may argue that division orders are conclusive evidence of NRI and that "
        "title examination is unnecessary for properties with established division orders."
    ),
    counter_arguments=[
        "Division orders are not conclusive evidence of title in most states — they are merely a payment directive.",
        "Division orders may be outdated and not reflect interim conveyances.",
        "Payment records may include suspense amounts that distort actual NRI analysis.",
        "Operator-calculated NRI may contain errors, especially in complex units.",
        "Underpayment of NRI creates a revenue claim; overpayment creates a potential liability to adjust.",
    ],
    resolution_strategy=(
        "Compile NRI schedule from PSA exhibits. Obtain division orders from operators and "
        "purchasers. Compare scheduled NRI to division order NRI. Verify against revenue "
        "payment records. Run independent NRI calculation from title data. Assert defects for "
        "variances exceeding threshold. Quantify defect values using PSA methodology."
    ),
    entity_scope="All wells and units in acquisition",
    confidence=ConfidenceLevel.DEFENSIBLE,
    confidence_stratification="Arithmetic verification; factual reconciliation.",
    controlling_precedent="Division order statutes; PSA NRI provisions; title opinions",
    issue_category=IssueCategory.NRI_WI_VERIFICATION,
    position_zone=PositionZone.BUYER,
    interaction_edges=["title_opinion_standard_of_review", "deficiency_identification_and_cure", "suspense_account_analysis"],
))

# ─────────────────────────────────────────────────────────────────────────────
# 18. SUSPENSE ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────

_register(DoctrineBlock(
    topic="suspense_account_analysis",
    keywords=["suspense", "suspended funds", "unclaimed revenue", "division order suspense", "title suspense"],
    conclusion_template=(
        "Suspense accounts represent revenue held pending resolution of title, payment, or "
        "administrative issues. Due diligence must quantify suspense balances, determine the "
        "cause, and allocate responsibility for resolution between buyer and seller."
    ),
    reasoning_framework=(
        "Revenue is held in suspense when the operator or purchaser cannot distribute it to "
        "the rightful owner. Common causes: (1) Title suspense — division orders not in place "
        "due to unresolved title questions, pending probate, or ownership disputes. (2) Address "
        "unknown — royalty or interest owner cannot be located. (3) Minimum check amount — "
        "accumulated revenue below distribution threshold. (4) Tax ID missing — inability to "
        "report payments without taxpayer identification number. (5) Dispute — ownership "
        "percentage contested between parties. For acquisitions: (a) Buyer typically assumes "
        "the obligation to distribute suspended funds once title is cleared. (b) The PSA "
        "should address whether suspense funds transfer with the sale (increasing the purchase "
        "price) or are retained by seller for resolution. (c) State escheat/unclaimed property "
        "laws may require reporting of aged suspense to the state — buyer must evaluate "
        "compliance. (d) Large suspense balances may indicate unresolved title problems that "
        "affect NRI. (e) Some suspense may be offset against amounts owed to buyer/seller for "
        "production imbalances."
    ),
    key_factors=[
        "Total suspense balance by cause category",
        "Age of suspense — exposure to escheat reporting",
        "PSA treatment of suspense (transfer vs. retention)",
        "Suspense related to NRI disputes vs. administrative issues",
        "State escheat/unclaimed property law compliance",
        "Suspense resolution timeline and cost",
        "Connection between suspense and title defects",
    ],
    primary_authority=[
        "State unclaimed property/escheat statutes",
        "Division order statutes (distribution obligations)",
        "PSA suspense provisions",
        "COPAS accounting procedures (suspense treatment)",
    ],
    burden_holder="Operator to distribute suspense when cause is resolved; acquirer assumes obligation post-closing.",
    adversary_position=(
        "Seller may minimize suspense disclosure or argue that suspense is merely "
        "administrative and will be resolved without cost."
    ),
    counter_arguments=[
        "Large title suspense balances indicate material unresolved title issues.",
        "Aged suspense may require escheat reporting, creating regulatory compliance risk.",
        "Resolution of suspense requires curative work (title examination, affidavits, quiet title).",
        "Suspense reduces cash flow available to buyer and creates ongoing administrative burden.",
        "Suspense funds transferred at closing should be reflected in purchase price adjustments.",
    ],
    resolution_strategy=(
        "Obtain detailed suspense report by well, cause, and age. Evaluate title suspense "
        "for connection to NRI defects. Assess escheat compliance status. Negotiate PSA "
        "provisions for suspense assumption/retention. Quantify cost of suspense resolution. "
        "Include suspense representations in PSA."
    ),
    entity_scope="All operator and purchaser suspense accounts",
    confidence=ConfidenceLevel.DEFENSIBLE,
    confidence_stratification="Factual analysis of financial records; regulatory framework clear.",
    controlling_precedent="State unclaimed property statutes; division order law",
    issue_category=IssueCategory.SUSPENSE_ANALYSIS,
    position_zone=PositionZone.BUYER,
    interaction_edges=["nri_working_interest_verification", "closing_adjustments_methodology"],
))

# ─────────────────────────────────────────────────────────────────────────────
# 19. OPERATOR QUALIFICATION
# ─────────────────────────────────────────────────────────────────────────────

_register(DoctrineBlock(
    topic="operator_qualification_review",
    keywords=["operator", "qualification", "JOA", "operating agreement", "COPAS", "AFE", "operator transfer"],
    conclusion_template=(
        "Operator qualification review evaluates whether the buyer (or continuing operator) "
        "has the regulatory standing, financial capacity, technical expertise, and contractual "
        "authority to operate the acquired assets safely and in compliance with all regulations."
    ),
    reasoning_framework=(
        "Operator review encompasses: (1) Regulatory qualification — the buyer must be "
        "qualified as an operator with the relevant state oil and gas commission (e.g., Form "
        "P-4 Organization Report in Texas, operator registration in Oklahoma/NM). (2) Financial "
        "capacity — bonding requirements, letters of credit, financial assurance for plugging "
        "and environmental obligations. (3) JOA provisions — the existing JOA governs operator "
        "rights and obligations. Review Article V (operator selection), Article VI (operator "
        "obligations), and Article VII (operator resignation and removal). (4) COPAS accounting "
        "procedure — governs overhead charges, direct charges, and accounting methodology. "
        "Verify which COPAS version applies and whether amendments have been adopted. (5) AFE "
        "process — authority for expenditure approval requirements, non-consent provisions, "
        "and penalty provisions. (6) Insurance requirements — operator's insurance obligations "
        "under the JOA and applicable law. (7) Operator transition — if the buyer is becoming "
        "operator, the transition process must be planned (data transfer, regulatory filings, "
        "employee transitions, system migrations, vendor contract assignments). (8) Non-operator "
        "rights — if the buyer is a non-operator, review the JOA for non-consent penalties, "
        "information rights, audit rights, and operator removal provisions."
    ),
    key_factors=[
        "Regulatory operator registration status",
        "Financial assurance (bonding, insurance) requirements",
        "JOA operator selection and removal provisions",
        "COPAS version and amendments in effect",
        "AFE authority limits and non-consent provisions",
        "Operator transition plan and timeline",
        "Key employee retention during transition",
        "Historical operator performance and compliance record",
    ],
    primary_authority=[
        "AAPL Form 610 Model Operating Agreement (Articles V-VII)",
        "COPAS Accounting Procedures (2005 or 2019 version)",
        "State operator registration requirements",
        "State bonding and financial assurance regulations",
    ],
    burden_holder="Buyer to qualify as operator; non-ops to consent per JOA terms.",
    adversary_position=(
        "Non-operating interest owners may challenge buyer's qualification and resist "
        "operator transition to a less-experienced operator."
    ),
    counter_arguments=[
        "Regulatory qualification is a threshold requirement — must be completed before operating.",
        "JOA operator removal provisions may be triggered by non-operator objections post-closing.",
        "COPAS overhead rates may need renegotiation after operator change.",
        "Operator transition risks include data loss, compliance gaps, and employee departures.",
        "Non-consent penalties may significantly dilute non-participating interest owners' returns.",
    ],
    resolution_strategy=(
        "Begin regulatory operator qualification process early. Review all JOAs for operator "
        "provisions. Plan transition timeline and resource requirements. Negotiate operator "
        "designation in PSA if assuming operatorship. Ensure bonding and insurance are in "
        "place before assuming operations. Communicate with non-operators about transition plan."
    ),
    entity_scope="All operated and non-operated interests",
    confidence=ConfidenceLevel.DEFENSIBLE,
    confidence_stratification="Regulatory requirements are clear; JOA interpretation is contract-specific.",
    controlling_precedent="AAPL Form 610; COPAS; state operator regulations",
    issue_category=IssueCategory.OPERATOR_QUALIFICATION,
    position_zone=PositionZone.BUYER,
    interaction_edges=["regulatory_compliance_audit", "consent_to_assign_requirements"],
))


# ─────────────────────────────────────────────────────────────────────────────
# 20. ADDITIONAL DUE DILIGENCE DOCTRINES
# ─────────────────────────────────────────────────────────────────────────────

_register(DoctrineBlock(
    topic="surface_use_agreement_review",
    keywords=["surface use", "surface damage", "surface owner", "accommodation", "surface agreement", "SUA"],
    conclusion_template=(
        "Surface use agreements (SUAs) govern the relationship between the mineral operator and "
        "the surface owner. Due diligence must identify all SUAs, evaluate compliance, and assess "
        "ongoing surface damage obligations that transfer to the buyer."
    ),
    reasoning_framework=(
        "The mineral estate is dominant, granting the mineral owner an implied easement for "
        "reasonable surface use necessary for exploration and production. However, this right "
        "is limited by: (1) Surface damage acts in states like Texas (Tex. Nat. Res. Code "
        "Chapter 92), North Dakota (NDCC 38-11.1), and Oklahoma, which require compensation "
        "for surface damage. (2) The accommodation doctrine (Getty Oil v. Jones, 1971), which "
        "requires the mineral owner to accommodate the surface owner's existing use when "
        "alternative methods are available. (3) Contractual surface use agreements that may "
        "impose specific obligations beyond statutory requirements. (4) Landowner consent "
        "requirements for certain activities (salt water disposal, pipeline construction). "
        "Due diligence should: (a) Identify all SUAs and surface damage payments. (b) Review "
        "pending or threatened surface damage claims. (c) Evaluate compliance with state "
        "surface damage statutes. (d) Assess future surface restoration obligations, including "
        "road maintenance, site reclamation, and equipment removal. (e) Determine whether "
        "surface consents are required for future development plans. SUAs may contain "
        "assignment restrictions, annual payment obligations, and performance standards "
        "that survive transfer."
    ),
    key_factors=[
        "Number and scope of existing surface use agreements",
        "State surface damage statute requirements",
        "Pending or threatened surface damage claims",
        "Future surface restoration obligations and estimated costs",
        "Surface consent requirements for planned development",
        "Annual surface use fee obligations",
        "Road use and maintenance agreements with landowners",
        "Water sourcing agreements for completion operations",
    ],
    primary_authority=[
        "Tex. Nat. Res. Code Chapter 92 (Texas surface damage act)",
        "NDCC 38-11.1 (North Dakota surface damage statute)",
        "Getty Oil Co. v. Jones, 470 S.W.2d 618 (Tex. 1971) — accommodation doctrine",
        "State-specific surface damage statutes",
    ],
    burden_holder="Operator to comply with surface damage statutes; surface owner to document damages.",
    adversary_position=(
        "Surface owners may assert that operator has exceeded reasonable use and demand "
        "additional compensation or restrict access to future development locations."
    ),
    counter_arguments=[
        "The dominant estate doctrine protects the mineral owner's right of reasonable surface use.",
        "Accommodation doctrine only applies when the mineral owner has reasonable alternatives.",
        "Surface damage statutes vary significantly by state in scope and remedy.",
        "SUAs may be renegotiable if original terms were below current market rates.",
        "Surface consents for pipeline ROWs may be separately negotiable from lease surface use.",
    ],
    resolution_strategy=(
        "Compile inventory of all SUAs and surface payments. Review compliance with state "
        "surface damage acts. Assess pending claims. Estimate future surface obligations for "
        "planned development. Include surface use representations in PSA. Budget for surface "
        "damage payments in operating cost projections."
    ),
    entity_scope="All surface operations",
    confidence=ConfidenceLevel.DEFENSIBLE,
    confidence_stratification="State statutes are clear; accommodation doctrine is fact-specific.",
    controlling_precedent="Getty Oil v. Jones; state surface damage statutes",
    issue_category=IssueCategory.REGULATORY_AUDIT,
    position_zone=PositionZone.BUYER,
    interaction_edges=["regulatory_compliance_audit", "plugging_abandonment_liability"],
))

_register(DoctrineBlock(
    topic="water_rights_disposal_compliance",
    keywords=["water rights", "produced water", "disposal", "injection well", "SWD", "Class II", "UIC"],
    conclusion_template=(
        "Produced water management — including disposal well compliance, water sourcing rights, "
        "and injection well permits — is an increasingly critical due diligence item. Regulatory "
        "tightening around induced seismicity and water quality has elevated disposal risks."
    ),
    reasoning_framework=(
        "Oil and gas operations generate significant produced water volumes requiring proper "
        "management and disposal. Due diligence must evaluate: (1) Disposal capacity — does "
        "the seller have sufficient permitted saltwater disposal (SWD) capacity for current "
        "and planned production? (2) UIC (Underground Injection Control) permit compliance — "
        "Class II injection well permits under the Safe Drinking Water Act. (3) Induced "
        "seismicity risk — regulatory agencies in Oklahoma, Texas, Kansas, and other states "
        "have imposed disposal restrictions in seismically active areas. The Texas Railroad "
        "Commission and Oklahoma Corporation Commission have seismicity response protocols "
        "that can reduce permitted injection volumes or require well shut-in. (4) Water "
        "sourcing for completions — rights to source fresh or brackish water, recycling "
        "facilities, water transfer agreements. (5) Third-party disposal agreements — "
        "commercial disposal contracts with midstream companies, pricing terms, and minimum "
        "volume commitments. (6) Produced water recycling infrastructure and economics. "
        "(7) Surface water discharge permits (NPDES) where applicable. (8) State-specific "
        "water quality standards and monitoring requirements."
    ),
    key_factors=[
        "Permitted SWD capacity vs. current and projected disposal needs",
        "UIC permit compliance and renewal status",
        "Induced seismicity risk classification for disposal wells",
        "Third-party disposal contracts and pricing",
        "Water sourcing rights and agreements for completions",
        "Produced water recycling infrastructure",
        "Regulatory restrictions on injection volumes or pressures",
        "NPDES surface discharge permit status (if applicable)",
    ],
    primary_authority=[
        "Safe Drinking Water Act (42 U.S.C. Section 300h) — UIC program",
        "40 CFR Part 144-148 (EPA UIC regulations)",
        "State oil and gas commission disposal well regulations",
        "State seismicity response protocols (e.g., RRC Disposal Well Monitoring)",
    ],
    burden_holder="Operator to maintain disposal permits and comply with injection limits.",
    adversary_position=(
        "Seller may argue that disposal capacity is adequate without disclosing recent "
        "regulatory restrictions or seismicity concerns affecting permitted volumes."
    ),
    counter_arguments=[
        "Induced seismicity regulations can materially reduce disposal capacity with limited notice.",
        "Disposal costs have increased significantly in constrained basins.",
        "Water sourcing rights may be contested during drought conditions.",
        "Third-party disposal contracts may have termination clauses or price escalators.",
        "Regulatory trend toward tighter disposal restrictions is accelerating.",
    ],
    resolution_strategy=(
        "Audit all UIC permits and compliance history. Assess induced seismicity risk for "
        "disposal wells. Review third-party disposal contracts. Evaluate water sourcing "
        "agreements and sufficiency. Model disposal cost projections under various regulatory "
        "scenarios. Include water management representations in PSA."
    ),
    entity_scope="All water disposal and sourcing operations",
    confidence=ConfidenceLevel.DEFENSIBLE,
    confidence_stratification="Regulatory framework is clear; seismicity risk involves uncertainty.",
    controlling_precedent="SDWA; state UIC regulations; seismicity response protocols",
    issue_category=IssueCategory.ENVIRONMENTAL_COMPLIANCE,
    position_zone=PositionZone.BUYER,
    interaction_edges=["phase_i_esa_scope_and_limitations", "regulatory_compliance_audit"],
))

_register(DoctrineBlock(
    topic="midstream_contract_review",
    keywords=["midstream", "gathering", "processing", "transportation", "pipeline", "MVC", "dedication", "acreage dedication"],
    conclusion_template=(
        "Midstream contracts (gathering, processing, and transportation agreements) are critical "
        "due diligence items because they establish the terms under which production reaches "
        "market. Unfavorable midstream terms can materially impair asset value."
    ),
    reasoning_framework=(
        "Midstream agreements determine the cost and availability of bringing production to "
        "market. Key analysis: (1) Acreage dedication — most midstream contracts require "
        "dedication of all production from defined acreage to the midstream provider. This "
        "creates a covenant running with the land that binds successors. (2) Minimum volume "
        "commitments (MVCs) — require the producer to deliver a minimum volume or pay a "
        "deficiency fee. MVCs can create significant liabilities if production declines. "
        "(3) Fee structure — percentage-of-proceeds (POP), keep-whole, fee-based, or hybrid. "
        "The fee structure determines how commodity price risk is allocated. (4) Quality "
        "specifications — BTU content, H2S levels, CO2 content. Off-spec penalties. "
        "(5) Term — many midstream contracts are 10-20 years with acreage dedication. "
        "Early termination may not be available. (6) Assignment provisions — the midstream "
        "contract may restrict assignment or require midstream provider consent. (7) "
        "Operational control — system curtailment rights, force majeure provisions, "
        "maintenance windows. (8) Rate escalators and renegotiation provisions. (9) "
        "Capacity constraints — insufficient midstream capacity can curtail production. "
        "(10) Regulatory considerations — pipeline safety (PHMSA), right-of-way, and "
        "FERC jurisdiction for interstate transportation."
    ),
    key_factors=[
        "Acreage dedication scope and exclusions",
        "MVC levels vs. current and projected production",
        "Fee structure and comparison to market rates",
        "Contract term and renewal/termination provisions",
        "Assignment and change of control provisions",
        "Quality specifications and off-spec penalties",
        "System capacity relative to current and planned production",
        "Rate escalators and renegotiation triggers",
        "Force majeure and curtailment provisions",
    ],
    primary_authority=[
        "Specific midstream agreement provisions",
        "State real property law (covenants running with the land)",
        "PHMSA pipeline safety regulations (49 CFR Parts 191-199)",
        "FERC jurisdiction (if interstate transportation)",
    ],
    burden_holder="Buyer to evaluate midstream economics; dedication runs with the land regardless.",
    adversary_position=(
        "Midstream provider will enforce dedication and MVC provisions regardless of "
        "change in upstream ownership. Unfavorable terms are not renegotiable without leverage."
    ),
    counter_arguments=[
        "MVC shortfalls create ongoing liabilities that reduce asset value.",
        "Acreage dedications may cover more acreage than the seller currently operates.",
        "Below-market gathering rates may be offset by higher processing deductions.",
        "Assignment restrictions may delay or complicate closing.",
        "Capacity constraints can force production curtailment with no recourse.",
    ],
    resolution_strategy=(
        "Review all midstream contracts in detail. Model MVC exposure under various production "
        "scenarios. Compare fee structures to current market rates. Evaluate assignment "
        "provisions and consent requirements. Assess capacity adequacy for development plans. "
        "Negotiate midstream representations in PSA covering material terms."
    ),
    entity_scope="All gathering, processing, and transportation agreements",
    confidence=ConfidenceLevel.DEFENSIBLE,
    confidence_stratification="Contract analysis is deterministic; market comparison provides benchmark.",
    controlling_precedent="Specific contract terms; state real property law",
    issue_category=IssueCategory.PSA_REVIEW,
    position_zone=PositionZone.BUYER,
    interaction_edges=["psa_structure_and_key_provisions", "production_decline_curve_review"],
))

_register(DoctrineBlock(
    topic="tax_due_diligence_considerations",
    keywords=["tax", "ad valorem", "severance tax", "income tax", "transfer tax", "tax audit", "property tax"],
    conclusion_template=(
        "Tax due diligence for oil and gas acquisitions must cover ad valorem property taxes, "
        "severance/production taxes, federal and state income tax implications of the "
        "transaction structure, and any pending tax audits or disputes."
    ),
    reasoning_framework=(
        "Tax considerations in oil and gas acquisitions: (1) Ad valorem/property taxes — "
        "mineral interests are subject to property tax in most states. Due diligence must "
        "verify that all property taxes are current, identify any tax protests in progress, "
        "and prorate taxes between buyer and seller. In Texas, mineral properties are assessed "
        "based on discounted cash flow of remaining reserves, making the appraised value "
        "directly tied to production and reserves. (2) Severance/production taxes — verify "
        "that all production taxes have been paid and that any available exemptions or "
        "incentives (stripper well, enhanced recovery, high-cost gas) have been properly "
        "claimed. (3) Transaction structure tax implications — an asset purchase allows the "
        "buyer to step up basis to purchase price, allocating value under Section 1060 cost "
        "allocation rules. An entity purchase provides no basis step-up unless a Section 338(h)(10) "
        "election is available (S corporations). (4) Percentage depletion vs. cost depletion — "
        "independent producers may claim percentage depletion on up to 1,000 BOE/day. (5) "
        "Intangible drilling costs (IDC) deduction availability for planned development. "
        "(6) State income tax considerations vary — Texas has no income tax but has franchise "
        "tax; Oklahoma, New Mexico, and other states have income tax. (7) Transfer taxes — "
        "some jurisdictions impose transfer taxes on real property conveyances."
    ),
    key_factors=[
        "Ad valorem tax payment status and pending protests",
        "Severance tax compliance and exemption verification",
        "Transaction structure (asset vs. entity) tax implications",
        "Section 1060 purchase price allocation methodology",
        "Available depletion and IDC deductions for buyer",
        "Pending tax audits or disputes",
        "State-specific transfer tax applicability",
        "Tax representation and indemnification in PSA",
    ],
    primary_authority=[
        "IRC Section 1060 (applicable asset acquisition)",
        "IRC Section 611-613A (depletion)",
        "IRC Section 263(c) (intangible drilling costs)",
        "State ad valorem tax statutes",
        "State severance tax statutes",
    ],
    burden_holder="Seller to deliver tax records; buyer to evaluate tax implications of structure.",
    adversary_position=(
        "Seller may prefer entity-level sale to avoid gain recognition and depreciation "
        "recapture, which conflicts with buyer's preference for asset purchase with basis step-up."
    ),
    counter_arguments=[
        "Entity purchase without 338(h)(10) election provides no basis step-up for buyer.",
        "Ad valorem tax protests may be resolved unfavorably after closing.",
        "Severance tax exemptions may not survive change of operator.",
        "Purchase price allocation methodology affects both parties' tax outcomes.",
        "State franchise/income tax nexus may be created for buyer in new jurisdictions.",
    ],
    resolution_strategy=(
        "Verify all tax payments are current. Review pending protests and tax audit status. "
        "Evaluate transaction structure for optimal tax efficiency. Model Section 1060 "
        "purchase price allocation. Include tax representations and indemnification in PSA. "
        "Prorate ad valorem taxes in closing adjustments."
    ),
    entity_scope="All tax aspects of the acquisition",
    confidence=ConfidenceLevel.DEFENSIBLE,
    confidence_stratification="Tax law is well-defined; specific application depends on structure and jurisdiction.",
    controlling_precedent="IRC; state tax statutes; Section 1060 allocation rules",
    issue_category=IssueCategory.PSA_REVIEW,
    position_zone=PositionZone.NEUTRAL,
    interaction_edges=["psa_structure_and_key_provisions", "closing_adjustments_methodology"],
))

_register(DoctrineBlock(
    topic="insurance_coverage_review",
    keywords=["insurance", "coverage", "liability", "pollution", "well control", "umbrella", "excess"],
    conclusion_template=(
        "Insurance coverage review verifies that the acquired operations have adequate insurance "
        "protection and identifies any gaps, exclusions, or coverage disputes that could create "
        "uninsured liability for the buyer."
    ),
    reasoning_framework=(
        "Oil and gas operations require multiple layers of insurance coverage: (1) Commercial "
        "general liability (CGL) — bodily injury, property damage, personal injury. Standard "
        "CGL policies contain a pollution exclusion, requiring separate pollution coverage. "
        "(2) Operator's extra expense / well control — covers costs of regaining control of "
        "a wild well, including blowout, crater, seepage, and pollution from well events. "
        "This is critical and unique to oil and gas. (3) Pollution legal liability (PLL) — "
        "covers gradual pollution, pre-existing contamination (if insured), and third-party "
        "bodily injury/property damage from pollution events. (4) Excess/umbrella liability — "
        "excess limits over CGL and auto. (5) Workers' compensation and employer's liability. "
        "(6) Property/inland marine — covers owned equipment, drilling rigs, production "
        "facilities. (7) Business interruption / loss of production income. (8) Directors "
        "and officers (D&O) liability — if acquiring an entity. (9) Due diligence should: "
        "(a) Review all insurance policies for adequacy. (b) Identify pending claims and "
        "available coverage. (c) Evaluate tail coverage needs if seller's policies are "
        "occurrence-based vs. claims-made. (d) Determine whether JOA insurance requirements "
        "are satisfied. (e) Budget for buyer's insurance costs post-closing."
    ),
    key_factors=[
        "CGL coverage limits and pollution exclusion applicability",
        "Well control / operator's extra expense policy adequacy",
        "Pollution legal liability coverage scope and limits",
        "Pending insurance claims and coverage disputes",
        "Claims-made vs. occurrence-based policy implications",
        "JOA minimum insurance requirements",
        "Insurance cost projections for buyer post-closing",
        "Representations and warranties insurance (R&W insurance) for the transaction",
    ],
    primary_authority=[
        "JOA insurance provisions (AAPL Form 610 Article XIII)",
        "State insurance regulations",
        "ISO CGL policy forms and endorsements",
        "AIPN Model Joint Operating Agreement insurance article",
    ],
    burden_holder="Seller to maintain adequate insurance through closing; buyer to arrange post-closing coverage.",
    adversary_position=(
        "Seller may have minimal insurance coverage or pending claims that reduce available "
        "limits. Seller may argue that insurance costs are buyer's responsibility post-closing."
    ),
    counter_arguments=[
        "Inadequate historical insurance may leave uninsured legacy liabilities for buyer.",
        "Claims-made policies provide no coverage for pre-closing events reported after closing.",
        "Well control insurance limits may be inadequate for high-pressure deepwater or HPHT wells.",
        "Pollution exclusions in CGL policies are broadly interpreted by courts.",
        "R&W insurance may be cost-effective alternative to expanded seller indemnification.",
    ],
    resolution_strategy=(
        "Obtain certificates of insurance and policy summaries. Review pending claims and "
        "coverage history. Evaluate tail coverage needs. Verify JOA insurance compliance. "
        "Budget post-closing insurance costs. Consider R&W insurance for the transaction. "
        "Include insurance representations in PSA."
    ),
    entity_scope="All insurance policies and pending claims",
    confidence=ConfidenceLevel.DEFENSIBLE,
    confidence_stratification="Insurance review is factual; coverage interpretation involves policy analysis.",
    controlling_precedent="Insurance policy terms; state insurance law; JOA requirements",
    issue_category=IssueCategory.REPS_WARRANTIES,
    position_zone=PositionZone.BUYER,
    interaction_edges=["indemnification_provisions", "reps_and_warranties_analysis"],
))

_register(DoctrineBlock(
    topic="employee_and_labor_considerations",
    keywords=["employee", "labor", "WARN Act", "severance", "retention", "benefits", "pension", "key man"],
    conclusion_template=(
        "For acquisitions involving operated properties or entity-level transactions, employee "
        "and labor considerations can significantly impact transition costs, operational "
        "continuity, and regulatory compliance."
    ),
    reasoning_framework=(
        "Employee due diligence covers: (1) Employee census — number, roles, compensation, "
        "tenure, location. (2) Key personnel identification — field supervisors, engineers, "
        "landmen, and compliance personnel essential for operations. (3) Employment agreements — "
        "severance provisions, non-compete covenants, change of control payments. (4) Benefits — "
        "health insurance, retirement plans (401k, pension, ESOP), equity compensation. (5) WARN "
        "Act compliance — the Worker Adjustment and Retraining Notification Act requires 60 days "
        "notice for plant closings or mass layoffs. Asset acquisitions may trigger WARN if buyer "
        "does not offer employment. (6) Collective bargaining agreements — union contracts, "
        "grievances, and successor employer obligations. (7) OSHA compliance — safety records, "
        "citations, pending investigations. (8) Worker classification — independent contractor "
        "vs. employee analysis (IRS 20-factor test, state-specific tests). Misclassification "
        "creates back tax and benefits liability. (9) Pending employment litigation — "
        "discrimination, wage and hour, wrongful termination claims."
    ),
    key_factors=[
        "Key personnel identification and retention planning",
        "Change of control payment obligations",
        "WARN Act applicability and compliance timing",
        "Benefit plan transition or termination costs",
        "Independent contractor classification risk",
        "Collective bargaining agreement successor obligations",
        "OSHA compliance and safety record",
        "Pending employment claims or investigations",
    ],
    primary_authority=[
        "WARN Act (29 U.S.C. Section 2101 et seq.)",
        "ERISA (29 U.S.C. Section 1001 et seq.) — benefit plan requirements",
        "OSHA (29 U.S.C. Section 651 et seq.) — workplace safety",
        "State employment laws (at-will, non-compete, wage payment)",
    ],
    burden_holder="Buyer to evaluate workforce needs; seller to disclose employment obligations.",
    adversary_position=(
        "Seller may not disclose the full scope of employment liabilities, including unfunded "
        "benefit obligations, pending claims, or contractor classification risks."
    ),
    counter_arguments=[
        "Change of control payments can be significant and should be factored into purchase price.",
        "WARN Act penalties for non-compliance include back pay and benefits for 60 days.",
        "Successor employer doctrine may impose CBA obligations on buyer.",
        "Contractor reclassification can create back-tax and penalty exposure.",
        "Key personnel departures post-closing can impair operational capability.",
    ],
    resolution_strategy=(
        "Obtain employee census and compensation data. Identify key personnel and negotiate "
        "retention agreements. Evaluate COC payment obligations. Assess WARN Act timing. "
        "Review benefit plans and transition costs. Check OSHA compliance. Include employment "
        "representations in PSA."
    ),
    entity_scope="All personnel and employment matters",
    confidence=ConfidenceLevel.DEFENSIBLE,
    confidence_stratification="Employment law is well-defined; fact-specific application required.",
    controlling_precedent="WARN Act; ERISA; OSHA; state employment statutes",
    issue_category=IssueCategory.PSA_REVIEW,
    position_zone=PositionZone.BUYER,
    interaction_edges=["psa_structure_and_key_provisions", "operator_qualification_review"],
))

_register(DoctrineBlock(
    topic="data_room_and_information_management",
    keywords=["data room", "virtual data room", "VDR", "information request", "due diligence checklist", "document management"],
    conclusion_template=(
        "Systematic management of the data room and information request process is essential "
        "for efficient due diligence. A structured approach ensures completeness, tracks "
        "outstanding requests, and preserves the evidentiary record."
    ),
    reasoning_framework=(
        "Due diligence data management: (1) Virtual data room (VDR) structure — the seller's "
        "data room should be organized by asset type, geography, and document category (title, "
        "environmental, regulatory, contracts, financial). Industry-standard data room indices "
        "follow the AAPL/EnergyNet convention. (2) Buyer's due diligence checklist — a "
        "comprehensive request list covering all 19 issue categories. The checklist should be "
        "issued promptly after PSA execution to maximize the diligence period. (3) Information "
        "tracking — every document request should be tracked for: date requested, date "
        "received, reviewer assigned, review status, and follow-up items identified. (4) "
        "Management presentations — structured sessions with seller's technical, operational, "
        "and financial personnel. Questions should be prepared in advance and responses "
        "documented. (5) Site visits — physical inspection of key properties, facilities, "
        "and equipment. Site visit protocols should include environmental screening, equipment "
        "condition assessment, and compliance verification. (6) Data quality assessment — "
        "evaluate the completeness and accuracy of data provided. Missing or incomplete data "
        "may indicate seller's lack of organization or intentional omission. (7) "
        "Confidentiality — all data room access should be logged and controlled per the "
        "confidentiality agreement (CA/NDA). (8) Privilege preservation — mark privileged "
        "documents appropriately; inadvertent disclosure may waive privilege."
    ),
    key_factors=[
        "Data room organization and completeness",
        "Due diligence checklist coverage of all 19 issue categories",
        "Information request tracking and follow-up process",
        "Management presentation scheduling and documentation",
        "Site visit planning and reporting",
        "Data quality and completeness assessment",
        "Confidentiality agreement compliance",
        "Privilege preservation for sensitive documents",
    ],
    primary_authority=[
        "AAPL Due Diligence Standards and Checklists",
        "Industry-standard VDR organization protocols",
        "Confidentiality agreement provisions",
        "Federal Rules of Evidence 502 (privilege waiver)",
    ],
    burden_holder="Seller to populate data room; buyer to systematically review and track.",
    adversary_position=(
        "Seller may provide voluminous but incomplete data, making it difficult for buyer "
        "to identify gaps within the diligence period."
    ),
    counter_arguments=[
        "Incomplete data room population may constitute breach of seller's cooperation covenant.",
        "Failure to provide requested information creates negative inference for defect valuation.",
        "Data room access logs establish what buyer knew and when (relevant for sandbagging).",
        "Management representations during presentations may supplement or contradict written disclosures.",
        "Site visit findings may reveal conditions not disclosed in data room documents.",
    ],
    resolution_strategy=(
        "Issue comprehensive due diligence checklist immediately after PSA execution. "
        "Assign dedicated team to track all information requests. Schedule management "
        "presentations early in diligence period. Plan site visits for material properties. "
        "Document all findings systematically. Escalate data gaps through formal channels."
    ),
    entity_scope="All due diligence information management",
    confidence=ConfidenceLevel.DEFENSIBLE,
    confidence_stratification="Process-oriented; well-established industry practice.",
    controlling_precedent="AAPL standards; CA/NDA provisions; PSA cooperation covenants",
    issue_category=IssueCategory.TITLE_DUE_DILIGENCE,
    position_zone=PositionZone.NEUTRAL,
    interaction_edges=["psa_structure_and_key_provisions", "reps_and_warranties_analysis"],
))

_register(DoctrineBlock(
    topic="federal_lease_due_diligence",
    keywords=["federal lease", "BLM", "ONRR", "federal royalty", "APD", "sundry notice", "unit PA"],
    conclusion_template=(
        "Federal oil and gas leases carry unique due diligence requirements beyond state lease "
        "analysis, including BLM compliance verification, ONRR royalty audit exposure, federal "
        "unit participating area analysis, and transferee qualification."
    ),
    reasoning_framework=(
        "Federal leases are governed by the Mineral Leasing Act (30 U.S.C. Section 181 et seq.) "
        "and BLM regulations (43 CFR Part 3100). Due diligence considerations: (1) Lease status "
        "— verify that the lease is in good standing with BLM. Check for compliance orders, "
        "notices of noncompliance, or pending lease cancellation proceedings. (2) Royalty "
        "compliance — federal royalty rates (currently 16.67% for new competitive leases, "
        "12.5% for older leases) must be verified. ONRR (Office of Natural Resources Revenue) "
        "conducts royalty audits with a 7-year lookback period. Underpayment exposure can be "
        "substantial. (3) APD (Application for Permit to Drill) compliance — verify that all "
        "wells were drilled under approved APDs with proper conditions of approval. (4) Sundry "
        "notices — verify compliance with all BLM sundry notice requirements (well tests, "
        "equipment installations, production reporting). (5) Federal unit compliance — for "
        "unitized federal leases, verify participating area designations, unit contraction "
        "status, and compensatory royalty obligations. (6) Assignment processing — BLM must "
        "approve all lease assignments. The transferee must be qualified as a lessee (citizens, "
        "associations of citizens, or corporations organized under US or state law). Processing "
        "time is typically 60-120 days. (7) NEPA compliance — the National Environmental Policy "
        "Act requires environmental review for federal lease activities. Verify that EAs or EISs "
        "have been completed for all active operations. (8) Endangered Species Act — biological "
        "opinions and take permits for operations in sensitive habitats."
    ),
    key_factors=[
        "BLM lease compliance status and outstanding violations",
        "ONRR royalty audit history and exposure",
        "APD and sundry notice compliance for all federal wells",
        "Federal unit participating area designations",
        "BLM assignment processing timeline",
        "Transferee qualification requirements",
        "NEPA compliance for active operations",
        "ESA/biological opinion requirements",
    ],
    primary_authority=[
        "Mineral Leasing Act (30 U.S.C. Section 181 et seq.)",
        "43 CFR Part 3100 (BLM oil and gas lease regulations)",
        "30 CFR Part 1202-1228 (ONRR royalty regulations)",
        "NEPA (42 U.S.C. Section 4321 et seq.)",
    ],
    burden_holder="Buyer must qualify as BLM lessee; BLM must approve assignment.",
    adversary_position=(
        "BLM may delay assignment approval or impose conditions. ONRR may initiate royalty "
        "audit during due diligence period."
    ),
    counter_arguments=[
        "BLM assignment processing delays can significantly impact closing timeline.",
        "ONRR royalty audits have 7-year lookback — exposure may be substantial.",
        "Federal unit contraction can eliminate lease coverage for marginal areas.",
        "NEPA requirements for new development may impose significant delays and costs.",
        "Compensatory royalty obligations for off-lease drainage may not be immediately apparent.",
    ],
    resolution_strategy=(
        "Request BLM lease status reports for all federal leases. Verify ONRR royalty payment "
        "history. Review APD compliance for all federal wells. Analyze unit participating areas "
        "and contraction risk. Begin BLM assignment qualification early. Evaluate NEPA status "
        "for planned development. Include federal lease representations in PSA."
    ),
    entity_scope="All federal oil and gas leases in acquisition",
    confidence=ConfidenceLevel.DEFENSIBLE,
    confidence_stratification="Federal regulatory framework is well-defined; BLM processing is procedural.",
    controlling_precedent="Mineral Leasing Act; BLM regulations; ONRR audit authority",
    issue_category=IssueCategory.REGULATORY_AUDIT,
    position_zone=PositionZone.BUYER,
    interaction_edges=["regulatory_compliance_audit", "held_by_production_analysis"],
))

_register(DoctrineBlock(
    topic="gas_balancing_and_imbalances",
    keywords=["gas balancing", "imbalance", "overproduction", "underproduction", "make-up rights", "cash balancing"],
    conclusion_template=(
        "Gas balancing issues arise when co-owners take production in different proportions "
        "than their ownership interests. Outstanding gas imbalances transfer with the assets "
        "and must be quantified and allocated in the PSA."
    ),
    reasoning_framework=(
        "In joint operations, working interest owners may take gas in-kind or elect to have "
        "the operator sell on their behalf. When one owner takes more than their proportionate "
        "share (overproduction), or less (underproduction), a gas imbalance is created. The "
        "methods for resolving imbalances vary: (1) In-kind balancing — the underproduced "
        "party takes excess production until balanced. (2) Cash balancing — the overproduced "
        "party pays the underproduced party for the value of the gas taken. (3) Make-up rights — "
        "contractual right to take excess production in the future. (4) JOA balancing provisions — "
        "the operating agreement may specify the balancing methodology. (5) Regulatory "
        "considerations — some states have gas balancing regulations. In Texas, the 'take-or-pay' "
        "litigation era established that the overproduced party may be liable for conversion "
        "if taking without authority. Due diligence must: (a) Obtain gas balancing statements "
        "for all properties. (b) Quantify net imbalance position (over or under). (c) Determine "
        "applicable balancing methodology per JOA and applicable law. (d) Allocate imbalance "
        "liability/benefit in PSA settlement adjustments."
    ),
    key_factors=[
        "Net gas imbalance position (MMcf and dollar value)",
        "Applicable balancing methodology (in-kind vs. cash)",
        "JOA gas balancing provisions",
        "State-specific gas balancing regulations",
        "Make-up rights value and exercisability",
        "Impact on NRI and revenue allocation",
        "Gas processor imbalance positions",
        "Historical balancing dispute resolution",
    ],
    primary_authority=[
        "JOA gas balancing provisions (AAPL Form 610)",
        "State gas balancing regulations (if applicable)",
        "Anderson Living Trust v. ConocoPhillips, 952 F.3d 166 (5th Cir. 2020)",
        "COPAS accounting procedures for gas imbalances",
    ],
    burden_holder="Both parties to verify imbalance position; PSA allocates responsibility.",
    adversary_position=(
        "Overproduced party may dispute the magnitude of the imbalance or the valuation "
        "methodology used for cash balancing."
    ),
    counter_arguments=[
        "Gas balancing statements from different parties may not reconcile.",
        "Historical imbalances may be difficult to reconstruct if records are incomplete.",
        "The value of make-up rights depends on remaining reserves and production capability.",
        "Gas processor imbalances are separate from wellhead imbalances.",
        "Cash balancing methodology (posted price vs. actual sales price) affects valuation.",
    ],
    resolution_strategy=(
        "Obtain gas balancing statements from all parties and the operator. Reconcile "
        "differences. Quantify net imbalance position at a fair valuation. Include gas "
        "balancing provisions in PSA settlement adjustments. Specify the methodology for "
        "post-closing imbalance resolution."
    ),
    entity_scope="All gas production with multiple working interest owners",
    confidence=ConfidenceLevel.DEFENSIBLE,
    confidence_stratification="Gas balancing is factual; methodology varies by contract and jurisdiction.",
    controlling_precedent="JOA provisions; state gas balancing law",
    issue_category=IssueCategory.PRODUCTION_ANALYSIS,
    position_zone=PositionZone.NEUTRAL,
    interaction_edges=["nri_working_interest_verification", "closing_adjustments_methodology"],
))

_register(DoctrineBlock(
    topic="hedging_and_derivative_positions",
    keywords=["hedging", "derivatives", "swap", "collar", "put option", "commodity hedge", "hedge book"],
    conclusion_template=(
        "Commodity hedging positions may transfer with the assets or be retained by the seller. "
        "Due diligence must identify all hedging positions, evaluate their value (or liability), "
        "and determine the PSA treatment for hedge transfer or termination."
    ),
    reasoning_framework=(
        "Oil and gas producers commonly hedge commodity price risk through derivatives: "
        "(1) Swaps — fix the price for a defined volume and period. Positive value if swap "
        "price exceeds market; negative value if market exceeds swap price. (2) Collars — "
        "establish a price floor (put) and ceiling (call) for a defined volume. (3) Put options — "
        "provide a price floor without capping upside. (4) Basis swaps — hedge the differential "
        "between a local price and a benchmark price. Due diligence considerations: (a) Identify "
        "all outstanding hedging positions by type, volume, price, and counterparty. (b) "
        "Calculate mark-to-market value of each position. (c) Determine whether hedges are "
        "assignable to buyer or must be terminated at closing. (d) If terminated, evaluate "
        "termination costs and allocate in PSA. (e) If transferred, negotiate value adjustment "
        "to purchase price. (f) ISDA Master Agreement provisions governing assignment and "
        "termination. (g) Credit support requirements — letters of credit or margin deposits. "
        "(h) Hedge accounting treatment under ASC 815 (if applicable). (i) Whether hedges "
        "are designated as cash flow hedges or fair value hedges affects accounting on "
        "transfer."
    ),
    key_factors=[
        "Outstanding hedge positions by instrument type",
        "Mark-to-market value of each position",
        "ISDA assignment and termination provisions",
        "Counterparty credit quality and credit support requirements",
        "PSA treatment of hedge transfer or termination",
        "Hedge accounting designation and transfer implications",
        "Hedge volume relative to acquisition production",
        "Termination cost allocation",
    ],
    primary_authority=[
        "ISDA Master Agreement provisions",
        "Dodd-Frank Title VII (derivative regulation)",
        "ASC 815 (hedge accounting, if applicable)",
        "PSA hedge transfer/termination provisions",
    ],
    burden_holder="Seller to disclose all hedging positions; buyer to evaluate transfer or termination.",
    adversary_position=(
        "Seller may seek to retain profitable hedge positions while transferring out-of-the-money "
        "hedges, or may argue that hedge value is already reflected in the purchase price."
    ),
    counter_arguments=[
        "Out-of-the-money hedges represent a real liability that should reduce purchase price.",
        "ISDA counterparty may not consent to assignment, forcing termination.",
        "Termination costs may be significant in a volatile commodity price environment.",
        "Hedge accounting designation may be lost on transfer, creating earnings volatility.",
        "Credit support requirements may change upon assignment to a different credit profile.",
    ],
    resolution_strategy=(
        "Obtain complete hedge book from seller. Calculate MTM for all positions. Determine "
        "transferability per ISDA terms. Negotiate PSA treatment — transfer with value "
        "adjustment or terminate with cost allocation. Evaluate buyer's own hedging needs "
        "post-closing."
    ),
    entity_scope="All commodity derivative positions",
    confidence=ConfidenceLevel.DEFENSIBLE,
    confidence_stratification="MTM valuation is deterministic; transfer mechanics depend on ISDA terms.",
    controlling_precedent="ISDA Master Agreement; PSA provisions; ASC 815",
    issue_category=IssueCategory.PSA_REVIEW,
    position_zone=PositionZone.NEUTRAL,
    interaction_edges=["psa_structure_and_key_provisions", "closing_adjustments_methodology"],
))

_register(DoctrineBlock(
    topic="antitrust_and_regulatory_approvals",
    keywords=["antitrust", "HSR", "Hart-Scott-Rodino", "FTC", "DOJ", "regulatory approval", "closing condition"],
    conclusion_template=(
        "For acquisitions above the Hart-Scott-Rodino threshold, HSR filing and antitrust "
        "clearance is a mandatory closing condition. Additional regulatory approvals may be "
        "required depending on the nature and location of the assets."
    ),
    reasoning_framework=(
        "Antitrust considerations: (1) Hart-Scott-Rodino Act (HSR) — transactions exceeding "
        "the current size-of-transaction threshold (adjusted annually; $119.5 million in 2024) "
        "generally require pre-merger notification to the FTC and DOJ. The standard waiting "
        "period is 30 days from filing (15 days for cash tender offers). (2) Second request — "
        "if the reviewing agency issues a second request, the waiting period is extended until "
        "substantial compliance. Second requests in energy transactions are uncommon but "
        "possible for acquisitions creating significant market concentration. (3) Market "
        "definition — relevant markets for oil and gas may include production basin, product "
        "(crude oil, natural gas, NGLs), midstream gathering systems, and processing plants. "
        "(4) Remedies — if antitrust concerns exist, parties may propose divestitures or "
        "behavioral remedies. (5) State regulatory approvals — some states require notice or "
        "approval for operator changes, lease assignments, or utility acquisitions. (6) CFIUS — "
        "Committee on Foreign Investment in the United States review is required if the buyer "
        "is a foreign person and the acquisition involves US energy assets near military "
        "installations or critical infrastructure."
    ),
    key_factors=[
        "HSR filing threshold applicability",
        "Market concentration analysis for relevant markets",
        "Second request risk assessment",
        "State regulatory approval requirements",
        "CFIUS applicability (if foreign buyer)",
        "Timeline for obtaining all regulatory approvals",
        "Reverse termination fee if regulatory approval fails",
        "Interim operating restrictions during regulatory review",
    ],
    primary_authority=[
        "Hart-Scott-Rodino Antitrust Improvements Act (15 U.S.C. Section 18a)",
        "FTC/DOJ Horizontal Merger Guidelines",
        "50 U.S.C. Section 4565 (CFIUS)",
        "State regulatory statutes (operator transfer, utility regulation)",
    ],
    burden_holder="Both parties jointly responsible for HSR filing; buyer for CFIUS if applicable.",
    adversary_position=(
        "If the transaction creates market concentration concerns, competitors may lobby the "
        "reviewing agency to challenge the deal."
    ),
    counter_arguments=[
        "HSR filing fees can be substantial (up to $2.25 million at highest tier).",
        "Second request timing is unpredictable and can significantly delay closing.",
        "State regulatory approvals in multiple jurisdictions create parallel timelines.",
        "CFIUS review can result in deal prohibition or forced divestitures.",
        "Regulatory risk should be allocated via reverse termination fees.",
    ],
    resolution_strategy=(
        "Determine HSR applicability based on current thresholds. Prepare HSR filings "
        "concurrently with PSA negotiation. Assess market concentration to evaluate second "
        "request risk. Identify all state regulatory approvals required. Evaluate CFIUS "
        "applicability. Include regulatory approval as a closing condition with outside "
        "date. Negotiate reverse termination fee allocation."
    ),
    entity_scope="Transaction-level regulatory compliance",
    confidence=ConfidenceLevel.DEFENSIBLE,
    confidence_stratification="Regulatory requirements are well-defined; antitrust analysis involves judgment.",
    controlling_precedent="HSR Act; FTC/DOJ merger guidelines; CFIUS",
    issue_category=IssueCategory.REGULATORY_AUDIT,
    position_zone=PositionZone.NEUTRAL,
    interaction_edges=["psa_structure_and_key_provisions", "change_of_control_provisions"],
))


def get_doctrine_cache() -> Dict[str, DoctrineBlock]:
    """Return the complete doctrine cache."""
    return DOCTRINE_CACHE


def get_doctrine_by_topic(topic: str) -> DoctrineBlock | None:
    """Retrieve a specific doctrine block by topic."""
    return DOCTRINE_CACHE.get(topic)


def get_doctrines_by_category(category: IssueCategory) -> list[DoctrineBlock]:
    """Retrieve all doctrine blocks for a specific issue category."""
    return [d for d in DOCTRINE_CACHE.values() if d.issue_category == category]


def get_doctrine_topics() -> list[str]:
    """Return all doctrine topic names."""
    return list(DOCTRINE_CACHE.keys())


def search_doctrines(keywords: list[str]) -> list[DoctrineBlock]:
    """Search doctrine cache by keywords. Returns blocks matching any keyword."""
    results: list[DoctrineBlock] = []
    for block in DOCTRINE_CACHE.values():
        for kw in keywords:
            kw_lower = kw.lower()
            if any(kw_lower in bkw.lower() for bkw in block.keywords):
                results.append(block)
                break
            if kw_lower in block.topic.lower():
                results.append(block)
                break
    return results


def get_interaction_graph() -> dict[str, list[str]]:
    """Return the full interaction graph between doctrines."""
    graph: dict[str, list[str]] = {}
    for topic, block in DOCTRINE_CACHE.items():
        graph[topic] = block.interaction_edges
    return graph


def get_doctrine_summary() -> dict[str, Any]:
    """Return a summary of the doctrine cache for dashboards."""
    from typing import Any
    category_stats: dict[str, dict[str, Any]] = {}
    for block in DOCTRINE_CACHE.values():
        cat = block.issue_category.value
        if cat not in category_stats:
            category_stats[cat] = {
                "count": 0,
                "confidence_distribution": {},
                "position_zones": {},
                "total_key_factors": 0,
                "total_authorities": 0,
                "total_counter_arguments": 0,
            }
        stats = category_stats[cat]
        stats["count"] += 1
        conf = block.confidence.value
        stats["confidence_distribution"][conf] = stats["confidence_distribution"].get(conf, 0) + 1
        pz = block.position_zone.value
        stats["position_zones"][pz] = stats["position_zones"].get(pz, 0) + 1
        stats["total_key_factors"] += len(block.key_factors)
        stats["total_authorities"] += len(block.primary_authority)
        stats["total_counter_arguments"] += len(block.counter_arguments)

    return {
        "total_doctrines": len(DOCTRINE_CACHE),
        "total_categories": len(category_stats),
        "categories": category_stats,
        "topics": list(DOCTRINE_CACHE.keys()),
    }
