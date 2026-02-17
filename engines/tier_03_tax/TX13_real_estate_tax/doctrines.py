"""
TX13 Real Estate Tax Engine - Doctrine Definitions
Pre-compiled expert reasoning blocks covering all real estate tax domains.

Each DoctrineBlock contains:
  - topic: canonical identifier
  - keywords: 5-8 trigger terms for cache matching
  - conclusion_template: 3-5 sentence authoritative conclusion
  - reasoning_framework: 20-40 lines of structured analysis
  - key_factors: 5+ decision-critical factors
  - primary_authority: 3-5 authoritative citations
  - burden_holder: who bears the burden of proof
  - adversary_position: expected IRS/counterparty position
  - counter_arguments: 5+ potential challenges
  - resolution_strategy: recommended approach
  - entity_scope: applicable entity types
  - confidence: DEFENSIBLE / AGGRESSIVE / DISCLOSURE / HIGH_RISK
  - controlling_precedent: lead case or ruling

Author: ECHO OMEGA PRIME
Engine: TX13 Real Estate Tax
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


# =============================================================================
# DOCTRINE BLOCK DATACLASS
# =============================================================================

@dataclass
class DoctrineBlock:
    """A single pre-compiled doctrine block for real estate tax analysis."""
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
    entity_scope: List[str]
    confidence: str
    confidence_stratification: str
    controlling_precedent: str
    irc_sections: List[str] = field(default_factory=list)
    related_doctrines: List[str] = field(default_factory=list)
    effective_dates: str = ""
    sunset_provision: str = ""


# =============================================================================
# DOCTRINE LIBRARY
# =============================================================================

DOCTRINE_BLOCKS: Dict[str, DoctrineBlock] = {}


def _register(block: DoctrineBlock) -> None:
    """Register a doctrine block in the global library."""
    DOCTRINE_BLOCKS[block.topic] = block


# =============================================================================
# 1. LIKE-KIND EXCHANGE - IRC 1031
# =============================================================================

_register(DoctrineBlock(
    topic="like_kind_exchange_1031",
    keywords=[
        "like-kind exchange", "1031 exchange", "deferred exchange", "starker",
        "qualified intermediary", "identification period", "exchange period",
        "boot", "debt relief",
    ],
    conclusion_template=(
        "Under IRC 1031(a), no gain or loss is recognized on the exchange of "
        "real property held for productive use in a trade or business or for "
        "investment if such property is exchanged solely for real property of "
        "like kind. The taxpayer must identify replacement property within 45 "
        "days and complete the exchange within 180 days. Boot received (cash "
        "or non-like-kind property) is taxable to the extent of realized gain."
    ),
    reasoning_framework=(
        "STEP 1: Confirm both relinquished and replacement properties are real "
        "property held for productive use or investment (not dealer property). "
        "Post-TCJA, personal property no longer qualifies.\n"
        "STEP 2: Verify the exchange structure uses a qualified intermediary "
        "(QI) under Reg. 1.1031(k)-1(g)(4) to avoid constructive receipt.\n"
        "STEP 3: Check the 45-day identification period. Taxpayer must identify "
        "replacement property in writing, signed and delivered to the QI. Three "
        "rules apply: 3-property rule, 200% rule, or 95% exception.\n"
        "STEP 4: Verify 180-day exchange period. Replacement property must be "
        "received by the earlier of 180 days or the tax return due date.\n"
        "STEP 5: Calculate boot. Debt relief netting: if debt on replacement "
        "exceeds debt on relinquished, no boot. Cash boot is recognized gain.\n"
        "STEP 6: Determine basis of replacement property: carryover basis from "
        "relinquished, decreased by boot received, increased by gain recognized.\n"
        "STEP 7: Assess related party restrictions under 1031(f). If related "
        "party disposes within 2 years, gain is accelerated.\n"
        "STEP 8: Document held-for requirement. No statutory holding period, "
        "but IRS safe harbor suggests 24 months minimum per Rev. Proc. 2008-16."
    ),
    key_factors=[
        "Property must be real property (post-TCJA, no personal property)",
        "Held for productive use in trade/business or investment",
        "45-day identification period is absolute (no extensions)",
        "180-day exchange period (or tax return due date if earlier)",
        "Qualified intermediary must hold funds to avoid constructive receipt",
        "Boot (cash or debt relief net) triggers gain recognition",
        "Related party rules under 1031(f) require 2-year hold",
        "Dealer property is categorically excluded",
    ],
    primary_authority=[
        "IRC 1031(a) - Like-Kind Exchange Nonrecognition",
        "Reg. 1.1031(k)-1 - Deferred Exchange Rules",
        "Starker v. United States, 602 F.2d 1341 (9th Cir. 1979)",
        "Rev. Proc. 2000-37 (Reverse Exchange Safe Harbor)",
        "TCJA 2017 - Limitation to Real Property Only",
    ],
    burden_holder="Taxpayer bears burden to prove like-kind qualification and compliance with timing requirements",
    adversary_position=(
        "IRS may argue: (1) property was held primarily for sale (dealer), "
        "(2) constructive receipt of funds occurred, (3) identification was "
        "defective, (4) exchange period exceeded, (5) related party abuse."
    ),
    counter_arguments=[
        "Dealer vs. investor distinction based on frequency, marketing, intent",
        "Constructive receipt if QI agreement has loopholes or taxpayer controls funds",
        "Identification letter ambiguity may invalidate the exchange",
        "Drop-and-swap transactions may be recharacterized as sale-first",
        "Partnership interest exchanges are specifically excluded by 1031(a)(2)(D)",
        "Mixed-use property requires allocation between qualifying and non-qualifying",
    ],
    resolution_strategy=(
        "Use a reputable QI with proper exchange agreement. Identify property "
        "within 45 days using the 3-property rule for simplicity. Document "
        "investment intent with contemporaneous records. Avoid related party "
        "transactions. Hold replacement property at least 24 months."
    ),
    entity_scope=["individual", "partnership", "llc", "s_corp", "c_corp", "trust"],
    confidence="DEFENSIBLE",
    confidence_stratification="DEFENSIBLE",
    controlling_precedent="Starker v. United States, 602 F.2d 1341 (9th Cir. 1979)",
    irc_sections=["1031", "1031(a)", "1031(f)", "1031(k)"],
    related_doctrines=["reverse_1031_exchange", "improvement_exchange_1031", "depreciation_recapture_1250"],
    effective_dates="Ongoing; post-TCJA limited to real property only effective 01/01/2018",
))


# =============================================================================
# 2. REVERSE 1031 EXCHANGE
# =============================================================================

_register(DoctrineBlock(
    topic="reverse_1031_exchange",
    keywords=[
        "reverse exchange", "reverse 1031", "parking arrangement",
        "exchange accommodation titleholder", "eat", "rev proc 2000-37",
        "acquire first", "reverse starker",
    ],
    conclusion_template=(
        "A reverse 1031 exchange under Rev. Proc. 2000-37 allows a taxpayer "
        "to acquire replacement property before disposing of relinquished "
        "property through a parking arrangement with an Exchange Accommodation "
        "Titleholder (EAT). The safe harbor requires the EAT to hold title "
        "and the exchange to be completed within 180 days."
    ),
    reasoning_framework=(
        "STEP 1: Determine if a reverse exchange is necessary (replacement "
        "available before buyer found for relinquished property).\n"
        "STEP 2: Engage an EAT to acquire and park the replacement property.\n"
        "STEP 3: The EAT takes title via a qualified exchange accommodation "
        "agreement (QEAA). This must be executed within 5 business days.\n"
        "STEP 4: Within 45 days, the taxpayer must identify the relinquished "
        "property to be transferred (if parking replacement) or the replacement "
        "property (if parking relinquished).\n"
        "STEP 5: Complete the exchange within 180 days of the EAT acquiring "
        "the parked property.\n"
        "STEP 6: The EAT must report as the beneficial owner. The taxpayer "
        "provides financing guarantees but does not take title.\n"
        "STEP 7: Ensure the EAT is not a disqualified person (agent, employee, "
        "attorney, accountant of taxpayer within 2-year lookback).\n"
        "STEP 8: Document all costs, financing, and timeline compliance."
    ),
    key_factors=[
        "Must use qualified Exchange Accommodation Titleholder (EAT)",
        "QEAA must be entered within 5 business days of EAT acquiring property",
        "45-day identification and 180-day exchange period apply",
        "EAT cannot be a disqualified person under Reg. 1.1031(k)-1(k)",
        "Taxpayer cannot hold both properties simultaneously outside safe harbor",
        "Financing for EAT acquisition must be carefully structured",
    ],
    primary_authority=[
        "Rev. Proc. 2000-37 - Safe Harbor for Reverse Exchanges",
        "IRC 1031 - Like-Kind Exchange",
        "Reg. 1.1031(k)-1(g)(4) - Qualified Intermediary Rules",
        "PLR 200131014 (Reverse Exchange Guidance)",
    ],
    burden_holder="Taxpayer bears burden to demonstrate compliance with Rev. Proc. 2000-37 safe harbor",
    adversary_position=(
        "IRS may argue the arrangement fails outside the safe harbor if the "
        "taxpayer exercises too much control over the parked property, the "
        "QEAA was not timely, or the EAT is a disqualified person."
    ),
    counter_arguments=[
        "EAT control vs. taxpayer control creates factual disputes",
        "Financing arrangements may indicate taxpayer is beneficial owner",
        "Improvements made during parking period may not qualify",
        "Non-safe-harbor reverse exchanges face uncertain treatment",
        "Cost and complexity make these unsuitable for smaller transactions",
    ],
    resolution_strategy=(
        "Strictly comply with Rev. Proc. 2000-37 safe harbor requirements. "
        "Use an experienced EAT. Execute QEAA within 5 business days. "
        "Maintain clear documentation of EAT's ownership role. "
        "Complete exchange within 180-day window."
    ),
    entity_scope=["individual", "partnership", "llc", "s_corp", "c_corp", "trust"],
    confidence="DEFENSIBLE",
    confidence_stratification="DEFENSIBLE",
    controlling_precedent="Rev. Proc. 2000-37",
    irc_sections=["1031"],
    related_doctrines=["like_kind_exchange_1031", "improvement_exchange_1031"],
))


# =============================================================================
# 3. IMPROVEMENT EXCHANGE 1031
# =============================================================================

_register(DoctrineBlock(
    topic="improvement_exchange_1031",
    keywords=[
        "improvement exchange", "build to suit", "construction exchange",
        "exchange last agreement", "bezdjian", "improvements on replacement",
        "build-to-suit 1031",
    ],
    conclusion_template=(
        "An improvement or build-to-suit 1031 exchange allows the taxpayer "
        "to use exchange proceeds to construct or improve replacement property "
        "before taking title. The EAT holds the property while improvements "
        "are made, and the taxpayer receives the improved property within the "
        "180-day exchange period. The value of improvements counts toward the "
        "exchange value."
    ),
    reasoning_framework=(
        "STEP 1: Identify the need for improvements on the replacement property.\n"
        "STEP 2: Structure as a reverse/improvement hybrid using EAT.\n"
        "STEP 3: EAT acquires replacement property and commissions improvements.\n"
        "STEP 4: Exchange funds are used by the EAT for construction costs.\n"
        "STEP 5: Improvements must be substantially complete within 180 days.\n"
        "STEP 6: Taxpayer receives improved property as replacement property.\n"
        "STEP 7: Only improvements completed and in place at transfer count "
        "toward the exchange value — incomplete work in progress does not.\n"
        "STEP 8: Document all construction contracts, invoices, and timelines."
    ),
    key_factors=[
        "EAT must hold title during improvement period",
        "All improvements must be completed within the 180-day exchange window",
        "Only improvements in place at time of transfer count toward value",
        "Construction delays can cause partial boot recognition",
        "Must comply with all standard 1031 identification rules",
        "Pre-existing ownership of the replacement site creates complications",
    ],
    primary_authority=[
        "Rev. Proc. 2000-37 (applied to improvement exchanges)",
        "Bezdjian v. Commissioner (improvement exchange guidance)",
        "IRC 1031 - Like-Kind Exchange",
        "Reg. 1.1031(k)-1 - Deferred Exchange Rules",
    ],
    burden_holder="Taxpayer must prove improvements were completed within exchange period and EAT had genuine title",
    adversary_position=(
        "IRS may argue: (1) taxpayer had beneficial ownership during construction, "
        "(2) improvements not substantially complete, (3) arrangement is a financing "
        "device rather than genuine exchange."
    ),
    counter_arguments=[
        "Construction delays may force recognition of boot on unspent funds",
        "Taxpayer involvement in construction decisions blurs EAT ownership",
        "Cost overruns may require additional non-exchange funds",
        "Complex accounting for partially completed improvements",
        "If EAT relationship is too close to taxpayer, structure fails",
    ],
    resolution_strategy=(
        "Engage experienced EAT early. Begin construction immediately after "
        "EAT acquisition. Use fixed-price contracts with liquidated damages "
        "for delay. Ensure all improvements are in place before day 180. "
        "Document EAT's independent decision-making authority over construction."
    ),
    entity_scope=["individual", "partnership", "llc", "s_corp", "c_corp"],
    confidence="AGGRESSIVE",
    confidence_stratification="AGGRESSIVE",
    controlling_precedent="Bezdjian v. Commissioner, TC Memo 2010-265",
    irc_sections=["1031"],
    related_doctrines=["like_kind_exchange_1031", "reverse_1031_exchange"],
))


# =============================================================================
# 4. COST SEGREGATION
# =============================================================================

_register(DoctrineBlock(
    topic="cost_segregation",
    keywords=[
        "cost segregation", "cost seg", "component depreciation",
        "audit technique guide", "engineering study", "reclassification",
        "5 year property", "7 year property", "15 year property",
    ],
    conclusion_template=(
        "Cost segregation studies reclassify building components from "
        "27.5-year (residential) or 39-year (commercial) recovery periods "
        "to shorter 5, 7, or 15-year recovery periods. This accelerates "
        "depreciation deductions and improves cash flow. The IRS Cost "
        "Segregation Audit Technique Guide sets quality standards for studies."
    ),
    reasoning_framework=(
        "STEP 1: Determine if cost segregation is beneficial — typically "
        "properties with acquisition/construction cost exceeding $1 million.\n"
        "STEP 2: Engage a qualified engineering firm to perform the study.\n"
        "STEP 3: Identify components that qualify as personal property (5/7yr) "
        "or land improvements (15yr) rather than structural components (27.5/39yr).\n"
        "STEP 4: Common reclassifications: electrical (dedicated circuits), "
        "plumbing (specialized), flooring (carpet, vinyl), site improvements "
        "(parking lots, landscaping, sidewalks), decorative finishes.\n"
        "STEP 5: Apply IRS four-factor test from Whiteco Industries: "
        "(1) capable of removal without damage, (2) not a structural component, "
        "(3) used in taxpayer's activity, (4) not permanently affixed.\n"
        "STEP 6: Tangible personal property test — inherent permanent "
        "attachment analysis per Hospital Corp. of America v. Commissioner.\n"
        "STEP 7: Apply bonus depreciation to reclassified components if "
        "placed in service in qualifying year.\n"
        "STEP 8: File Form 3115 for change in accounting method if applying "
        "to previously placed-in-service property (catch-up via 481(a) adjustment)."
    ),
    key_factors=[
        "Engineering study must meet IRS Audit Technique Guide standards",
        "Common reclassifications: site improvements, specialty systems, finishes",
        "Whiteco four-factor test for personal property classification",
        "Form 3115 required for retroactive application (accounting method change)",
        "Bonus depreciation amplifies benefit of reclassified components",
        "Alternative Depreciation System (ADS) required for some real property activities",
        "Look-back studies can recapture previously missed depreciation",
    ],
    primary_authority=[
        "IRS Cost Segregation Audit Technique Guide (2004, updated 2022)",
        "Hospital Corp. of America v. Commissioner, 109 T.C. 21 (1997)",
        "Whiteco Industries v. Commissioner, 65 T.C. 664 (1975)",
        "IRC 168 - MACRS Depreciation",
        "Rev. Proc. 2015-13 (Automatic Accounting Method Changes)",
    ],
    burden_holder="Taxpayer bears burden to substantiate reclassifications with engineering evidence",
    adversary_position=(
        "IRS challenges cost seg studies for: (1) inadequate engineering analysis, "
        "(2) blanket percentage allocations without component-level detail, "
        "(3) classifying structural components as personal property, "
        "(4) using sampling instead of detailed analysis."
    ),
    counter_arguments=[
        "IRS may disallow reclassifications lacking engineering support",
        "Sampling-based studies are weaker than detailed component analysis",
        "Structural vs. personal property boundaries are fact-intensive",
        "Recapture on sale at Section 1245 rates (ordinary income)",
        "ADS requirements for real property trades or businesses may negate benefit",
        "Audit risk is elevated for aggressive reclassification percentages",
    ],
    resolution_strategy=(
        "Use a qualified engineering firm meeting ATG standards. Perform "
        "detailed component-level analysis, not sampling. Document the "
        "four-factor test for each reclassified component. Maintain "
        "photographs, invoices, and engineering reports. File Form 3115 "
        "for look-back studies. Consider ADS implications."
    ),
    entity_scope=["individual", "partnership", "llc", "s_corp", "c_corp", "reit", "trust"],
    confidence="DEFENSIBLE",
    confidence_stratification="DEFENSIBLE",
    controlling_precedent="Hospital Corp. of America v. Commissioner, 109 T.C. 21 (1997)",
    irc_sections=["168", "167", "1245", "1250"],
    related_doctrines=["bonus_depreciation_168k", "depreciation_recapture_1250"],
))


# =============================================================================
# 5. BONUS DEPRECIATION - IRC 168(k)
# =============================================================================

_register(DoctrineBlock(
    topic="bonus_depreciation_168k",
    keywords=[
        "bonus depreciation", "168k", "100% depreciation", "first year",
        "qualified property", "phase down", "used property",
        "additional first year depreciation",
    ],
    conclusion_template=(
        "IRC 168(k) provides 100% bonus depreciation for qualified property "
        "placed in service after September 27, 2017, through December 31, 2026, "
        "with phase-down beginning in 2023 (80%), 2024 (60%), 2025 (40%), "
        "2026 (20%). Post-TCJA, used property qualifies if new to the taxpayer. "
        "Qualified improvement property (QIP) is eligible at 15-year recovery."
    ),
    reasoning_framework=(
        "STEP 1: Confirm property is qualified property under 168(k)(2) — "
        "MACRS property with recovery period of 20 years or less, computer "
        "software, water utility property, or qualified improvement property.\n"
        "STEP 2: Determine placed-in-service date to identify applicable "
        "percentage: 100% (2017-2022), 80% (2023), 60% (2024), 40% (2025), "
        "20% (2026), 0% (2027+).\n"
        "STEP 3: For used property, verify the property was not previously "
        "used by the taxpayer (new-to-taxpayer test).\n"
        "STEP 4: Check for elections out — taxpayer may elect out of bonus "
        "depreciation on a class-by-class basis per year.\n"
        "STEP 5: Assess interaction with Section 179 (separate election, "
        "$1,160,000 limit for 2023, different phase-out rules).\n"
        "STEP 6: Consider ADS implications — real property trades or "
        "businesses electing out of 163(j) must use ADS, which precludes "
        "bonus depreciation.\n"
        "STEP 7: For partnerships, consider technical termination and "
        "placed-in-service date reset issues.\n"
        "STEP 8: Document the property's cost, acquisition date, and "
        "classification for audit defense."
    ),
    key_factors=[
        "Phase-down schedule: 80% (2023), 60% (2024), 40% (2025), 20% (2026)",
        "Used property now qualifies if new to the taxpayer (post-TCJA)",
        "QIP qualifies as 15-year property eligible for bonus depreciation",
        "Election out available on class-by-class basis",
        "ADS requirement for 163(j) electing businesses eliminates bonus",
        "Interaction with cost segregation multiplies the benefit",
        "Special rules for long-production-period property",
    ],
    primary_authority=[
        "IRC 168(k) - Additional First-Year Depreciation",
        "Reg. 1.168(k)-2 (2019 Final Regulations)",
        "TCJA 2017, Section 13201 (100% Bonus)",
        "CARES Act 2020 (QIP Technical Correction to 15 years)",
        "Rev. Proc. 2020-25 (QIP Late Bonus Depreciation Election)",
    ],
    burden_holder="Taxpayer must substantiate property classification, cost basis, and placed-in-service date",
    adversary_position=(
        "IRS may challenge: (1) placed-in-service date manipulation, "
        "(2) property classification errors, (3) failure to meet new-to-taxpayer "
        "test for used property, (4) ADS requirement not properly applied."
    ),
    counter_arguments=[
        "Placed-in-service date disputes for construction/renovation projects",
        "Related party acquisitions may not meet new-to-taxpayer test",
        "ADS election under 163(j) eliminates bonus depreciation benefit",
        "Phase-down creates timing pressure for large acquisitions",
        "Recapture as ordinary income on disposition within recovery period",
    ],
    resolution_strategy=(
        "Combine cost segregation with bonus depreciation for maximum benefit. "
        "Document placed-in-service dates with certificates of occupancy. "
        "Evaluate 163(j) election implications before claiming bonus. "
        "Consider electing out if AMT or loss limitation issues exist."
    ),
    entity_scope=["individual", "partnership", "llc", "s_corp", "c_corp", "reit"],
    confidence="DEFENSIBLE",
    confidence_stratification="DEFENSIBLE",
    controlling_precedent="Reg. 1.168(k)-2 (2019 Final Regulations)",
    irc_sections=["168(k)", "168", "179", "163(j)"],
    related_doctrines=["cost_segregation", "depreciation_recapture_1250", "tenant_improvements_qip"],
    effective_dates="100% through 12/31/2022, phase-down 2023-2026, expires 2027",
))


# =============================================================================
# 6. PASSIVE ACTIVITY RULES - IRC 469
# =============================================================================

_register(DoctrineBlock(
    topic="passive_activity_469",
    keywords=[
        "passive activity", "passive loss", "section 469", "rental activity",
        "grouping election", "pal", "suspended losses", "disposition",
        "material participation",
    ],
    conclusion_template=(
        "IRC 469 limits the deductibility of passive activity losses to "
        "passive activity income. Rental activities are per se passive unless "
        "the taxpayer qualifies as a real estate professional under 469(c)(7). "
        "Suspended passive losses are allowed in full upon a fully taxable "
        "disposition of the activity to an unrelated party."
    ),
    reasoning_framework=(
        "STEP 1: Classify the activity as passive or non-passive. Rental "
        "activities are per se passive unless the RE professional exception applies.\n"
        "STEP 2: Determine if the taxpayer materially participates under "
        "Reg. 1.469-5T (seven tests, 500-hour test most common).\n"
        "STEP 3: Evaluate grouping election under Reg. 1.469-4(c). Grouping "
        "appropriate activities can satisfy material participation.\n"
        "STEP 4: If passive, determine if $25K rental loss allowance applies "
        "(active participation, AGI under $150K, individual taxpayers only).\n"
        "STEP 5: Track suspended passive losses on Form 8582. These carry "
        "forward indefinitely.\n"
        "STEP 6: On disposition, all suspended losses are released — but only "
        "if the disposition is fully taxable to an unrelated party.\n"
        "STEP 7: Gift does NOT release suspended losses (they attach to "
        "donee's basis). Death releases losses only to the extent they exceed "
        "the step-up in basis.\n"
        "STEP 8: Document hours and activities for each rental property/business."
    ),
    key_factors=[
        "Rental activities are per se passive (with RE professional exception)",
        "Seven material participation tests under Reg. 1.469-5T",
        "Grouping election allows combining related activities",
        "Suspended losses carry forward indefinitely",
        "Full disposition to unrelated party releases all suspended losses",
        "Gift does NOT release suspended losses",
        "Death releases losses only exceeding basis step-up",
        "$25K rental loss allowance for active participants (AGI phase-out)",
    ],
    primary_authority=[
        "IRC 469 - Passive Activity Loss Rules",
        "Reg. 1.469-5T - Material Participation Tests",
        "Reg. 1.469-4 - Definition of Activity / Grouping",
        "Reg. 1.469-9 - Rules for Real Estate Professionals",
        "Fransen v. United States, 191 F.3d 599 (5th Cir. 1999)",
    ],
    burden_holder="Taxpayer bears burden to prove material participation through contemporaneous records",
    adversary_position=(
        "IRS consistently challenges: (1) hour logs as self-serving, "
        "(2) grouping elections as abuse, (3) real estate professional "
        "status claims without adequate documentation."
    ),
    counter_arguments=[
        "Hour logs prepared after-the-fact are given less weight (Goshorn)",
        "Grouping election may be challenged if activities lack economic integration",
        "Real estate professional status requires strict 750-hour test documentation",
        "Conversion from passive to non-passive may trigger recapture issues",
        "S corporation shareholders cannot count entity-level hours for material participation",
    ],
    resolution_strategy=(
        "Maintain contemporaneous daily time logs. File grouping election "
        "statement with first return claiming benefit. Track hours separately "
        "for each activity. Document the nature of participation activities. "
        "Consider RE professional election if hours warrant."
    ),
    entity_scope=["individual", "partnership", "llc", "s_corp", "trust"],
    confidence="DEFENSIBLE",
    confidence_stratification="DEFENSIBLE",
    controlling_precedent="Fransen v. United States, 191 F.3d 599 (5th Cir. 1999)",
    irc_sections=["469", "469(c)(7)", "469(i)"],
    related_doctrines=["real_estate_professional_status", "rental_loss_allowance_25k"],
))


# =============================================================================
# 7. REAL ESTATE PROFESSIONAL STATUS
# =============================================================================

_register(DoctrineBlock(
    topic="real_estate_professional_status",
    keywords=[
        "real estate professional", "rep status", "750 hours",
        "material participation", "469(c)(7)", "rental aggregation",
        "qualifying taxpayer", "re professional",
    ],
    conclusion_template=(
        "A taxpayer qualifying as a real estate professional under IRC "
        "469(c)(7) may treat rental real estate activities as non-passive, "
        "allowing losses to offset ordinary income. The taxpayer must spend "
        "more than 750 hours in real property trades or businesses AND more "
        "than half of personal services in such activities. Each rental "
        "activity requires separate material participation unless an "
        "aggregation election is made."
    ),
    reasoning_framework=(
        "STEP 1: Determine if the taxpayer performs more than 750 hours of "
        "services in real property trades or businesses during the tax year.\n"
        "STEP 2: Verify that more than 50% of all personal services performed "
        "during the year are in real property trades or businesses.\n"
        "STEP 3: Real property trades or businesses include: development, "
        "redevelopment, construction, reconstruction, acquisition, conversion, "
        "rental, operation, management, leasing, brokerage.\n"
        "STEP 4: For married filing jointly, only ONE spouse must meet the "
        "tests — hours cannot be combined between spouses.\n"
        "STEP 5: Even with RE professional status, the taxpayer must still "
        "materially participate in each rental activity (separately) unless "
        "the aggregation election is made.\n"
        "STEP 6: Aggregation election (treating all rental activities as one) "
        "is made by filing a statement with the return. Once made, it applies "
        "to all future years unless revoked.\n"
        "STEP 7: Document all hours — IRS challenges are frequent and the "
        "Tax Court consistently requires contemporaneous records.\n"
        "STEP 8: W-2 employees rarely qualify due to the 50% test."
    ),
    key_factors=[
        "750+ hours in real property trades or businesses",
        "More than 50% of all personal services in real property activities",
        "Only one spouse needs to qualify (joint return)",
        "Separate material participation required for each rental unless aggregated",
        "Aggregation election is irrevocable (applies to all future years)",
        "W-2 employment hours count against the 50% test",
        "Contemporaneous time logs are critical for audit defense",
    ],
    primary_authority=[
        "IRC 469(c)(7) - Real Estate Professional Exception",
        "Reg. 1.469-9 - Real Estate Professional Rules",
        "Aragona Trust v. Commissioner, 142 T.C. 165 (2014)",
        "Moss v. Commissioner, T.C. Memo 2012-292",
        "Birdsong v. Commissioner, T.C. Memo 2018-148",
    ],
    burden_holder="Taxpayer bears burden to prove 750 hours and >50% test with contemporaneous records",
    adversary_position=(
        "IRS aggressively challenges RE professional claims, particularly "
        "for taxpayers with full-time W-2 employment. Post-hoc time logs "
        "are given minimal weight. Vague descriptions of activities rejected."
    ),
    counter_arguments=[
        "Full-time W-2 employees almost never pass the 50% test",
        "Post-hoc time reconstructions carry little evidentiary weight",
        "Travel time to/from properties may not count as qualifying hours",
        "Investor-type activities (reviewing financial statements) may not count",
        "IRS has won numerous Tax Court cases on insufficient documentation",
    ],
    resolution_strategy=(
        "Maintain contemporaneous daily log of hours with specific activity "
        "descriptions. If one spouse qualifies, ensure that spouse's hours "
        "are well-documented. Consider aggregation election to simplify "
        "material participation. Avoid W-2 employment that defeats the 50% test."
    ),
    entity_scope=["individual"],
    confidence="AGGRESSIVE",
    confidence_stratification="AGGRESSIVE",
    controlling_precedent="Aragona Trust v. Commissioner, 142 T.C. 165 (2014)",
    irc_sections=["469(c)(7)"],
    related_doctrines=["passive_activity_469", "rental_loss_allowance_25k"],
))


# =============================================================================
# 8. RENTAL LOSS ALLOWANCE $25K
# =============================================================================

_register(DoctrineBlock(
    topic="rental_loss_allowance_25k",
    keywords=[
        "rental loss allowance", "25000 allowance", "active participation",
        "agi phase out", "469(i)", "rental deduction", "150000 phase out",
        "25k allowance",
    ],
    conclusion_template=(
        "IRC 469(i) allows individual taxpayers who actively participate in "
        "rental real estate activities to deduct up to $25,000 of rental "
        "losses against non-passive income. The allowance phases out by 50% "
        "of the amount by which AGI exceeds $100,000, fully eliminating at "
        "$150,000 AGI. Active participation requires a 10% ownership interest "
        "and involvement in management decisions."
    ),
    reasoning_framework=(
        "STEP 1: Confirm the taxpayer is an individual (not a corporation, "
        "trust, or estate — though estates can claim for 2 years after death).\n"
        "STEP 2: Verify 10%+ ownership interest in the rental activity.\n"
        "STEP 3: Determine active participation — management decisions "
        "such as approving tenants, setting rental terms, approving repairs.\n"
        "STEP 4: Calculate modified AGI for phase-out purposes. Modified AGI "
        "is AGI without passive losses, IRA contributions, or taxable SS.\n"
        "STEP 5: Phase-out: $25,000 reduced by 50 cents for each dollar of "
        "modified AGI over $100,000. Fully eliminated at $150,000.\n"
        "STEP 6: The $25,000 is reduced to $12,500 for married filing separately "
        "if spouses lived together at any point during the year.\n"
        "STEP 7: Rehabilitation and low-income housing credits have a higher "
        "$25,000 equivalent offset with phase-out starting at $200,000 AGI.\n"
        "STEP 8: Losses exceeding the allowance are suspended and carry forward."
    ),
    key_factors=[
        "Individual taxpayers only (not corporations or trusts)",
        "10% ownership interest required",
        "Active participation is lower standard than material participation",
        "Phase-out: $100K-$150K modified AGI (50 cents per dollar)",
        "$12,500 limit for married filing separately (living together)",
        "Suspended losses carry forward indefinitely",
        "Does not apply to limited partners",
    ],
    primary_authority=[
        "IRC 469(i) - Special Allowance for Rental Real Estate",
        "Reg. 1.469-1T(e)(3) - Active Participation Standard",
        "IRC 469(i)(3) - Phase-Out Rules",
        "Senate Finance Committee Report, TRA 1986",
    ],
    burden_holder="Taxpayer must demonstrate active participation and AGI within phase-out range",
    adversary_position=(
        "IRS may argue: (1) taxpayer does not actively participate (pure "
        "investor), (2) modified AGI exceeds $150,000, (3) limited partner "
        "status precludes active participation."
    ),
    counter_arguments=[
        "Pure investors who delegate all management may not qualify",
        "High-income taxpayers receive zero benefit due to phase-out",
        "Limited partners generally cannot claim active participation",
        "LLC members may qualify depending on operating agreement provisions",
        "Modified AGI calculation differs from standard AGI",
    ],
    resolution_strategy=(
        "Document management involvement: tenant approval emails, repair "
        "authorizations, lease negotiations. Track modified AGI for phase-out. "
        "If AGI exceeds $150K, focus on RE professional status instead."
    ),
    entity_scope=["individual"],
    confidence="DEFENSIBLE",
    confidence_stratification="DEFENSIBLE",
    controlling_precedent="Senate Finance Committee Report, TRA 1986 (legislative history)",
    irc_sections=["469(i)", "469(i)(3)"],
    related_doctrines=["passive_activity_469", "real_estate_professional_status"],
))


# =============================================================================
# 9. SECTION 199A - QBI DEDUCTION FOR REAL ESTATE
# =============================================================================

_register(DoctrineBlock(
    topic="section_199a_real_estate",
    keywords=[
        "199a", "qbi", "qualified business income", "pass-through deduction",
        "safe harbor rental", "rev proc 2019-38", "sstb",
        "w2 wage limitation", "ubia",
    ],
    conclusion_template=(
        "Section 199A provides a deduction of up to 20% of qualified business "
        "income from pass-through entities and sole proprietorships. For real "
        "estate rental activities, Rev. Proc. 2019-38 provides a safe harbor "
        "treating rental enterprises as trades or businesses if 250 hours of "
        "rental services are performed annually. Triple net leases are "
        "excluded from the safe harbor."
    ),
    reasoning_framework=(
        "STEP 1: Determine if the rental activity is a trade or business "
        "under Section 162 or qualifies under the safe harbor.\n"
        "STEP 2: Safe harbor requirements (Rev. Proc. 2019-38): 250 hours "
        "of rental services per year, separate books, contemporaneous records, "
        "and rental services include maintenance, repairs, rent collection, "
        "tenant management, property supervision.\n"
        "STEP 3: Triple net leases are excluded from the safe harbor but may "
        "still qualify as a Section 162 trade or business on their own facts.\n"
        "STEP 4: For taxpayers above the income threshold ($182,100 single / "
        "$364,200 MFJ for 2023), the QBI deduction is limited to the greater "
        "of: (a) 50% of W-2 wages, or (b) 25% of W-2 wages plus 2.5% of "
        "the unadjusted basis immediately after acquisition (UBIA).\n"
        "STEP 5: Rental real estate is generally not a specified service trade "
        "or business (SSTB), so it is not subject to the SSTB phase-out.\n"
        "STEP 6: Aggregation election under Reg. 1.199A-4 allows combining "
        "commonly controlled trades or businesses to pool W-2 wages and UBIA.\n"
        "STEP 7: Partnership/S corp K-1 reporting of QBI, W-2 wages, and UBIA.\n"
        "STEP 8: Rental losses reduce QBI (can create negative QBI carryforward)."
    ),
    key_factors=[
        "250 hours of rental services for safe harbor (Rev. Proc. 2019-38)",
        "Triple net leases excluded from safe harbor",
        "W-2 wage and UBIA limitations for high-income taxpayers",
        "Aggregation election to pool W-2 wages and UBIA",
        "Not an SSTB (favorable for real estate)",
        "Negative QBI carries forward to reduce future deductions",
        "UBIA includes full cost basis regardless of depreciation taken",
    ],
    primary_authority=[
        "IRC 199A - Qualified Business Income Deduction",
        "Rev. Proc. 2019-38 - Rental Real Estate Safe Harbor",
        "Reg. 1.199A-1 through 1.199A-6 (Final Regulations)",
        "Reg. 1.199A-4 - Aggregation Rules",
        "Notice 2019-07 (Initial Safe Harbor Guidance)",
    ],
    burden_holder="Taxpayer must demonstrate trade or business status or safe harbor compliance",
    adversary_position=(
        "IRS may argue: (1) rental activity is not a trade or business "
        "(insufficient activity level), (2) safe harbor 250-hour test not met, "
        "(3) triple net lease exclusion applies, (4) aggregation election is "
        "improper if businesses lack common control."
    ),
    counter_arguments=[
        "Triple net leases may fail even the Section 162 trade or business test",
        "250-hour safe harbor requires contemporaneous records",
        "Passive rental with management company may lack sufficient taxpayer involvement",
        "UBIA is reduced to zero after depreciable life expires",
        "Aggregation requires 50% common ownership and other criteria",
    ],
    resolution_strategy=(
        "Document 250+ hours of rental services annually. Maintain separate "
        "books for each rental enterprise. File aggregation election with "
        "first return claiming benefit. Track UBIA for each property. "
        "Avoid triple net lease structures if 199A is important."
    ),
    entity_scope=["individual", "partnership", "llc", "s_corp", "trust"],
    confidence="DEFENSIBLE",
    confidence_stratification="DEFENSIBLE",
    controlling_precedent="Rev. Proc. 2019-38",
    irc_sections=["199A"],
    related_doctrines=["passive_activity_469", "real_estate_professional_status"],
    effective_dates="Tax years 2018-2025 (sunsets unless extended)",
    sunset_provision="Section 199A expires after December 31, 2025 unless Congress extends",
))


# =============================================================================
# 10. OPPORTUNITY ZONES - IRC 1400Z
# =============================================================================

_register(DoctrineBlock(
    topic="opportunity_zone_investment",
    keywords=[
        "opportunity zone", "qof", "qualified opportunity fund",
        "1400z", "capital gain deferral", "10 year hold",
        "basis step up", "180 day", "qozb",
    ],
    conclusion_template=(
        "IRC 1400Z-2 allows taxpayers to defer capital gains by investing "
        "in Qualified Opportunity Funds (QOFs) within 180 days of the gain "
        "event. Gains invested in a QOF are deferred until December 31, 2026, "
        "or earlier disposition. If the QOF investment is held for at least "
        "10 years, any appreciation in the QOF investment receives a permanent "
        "exclusion from income (basis step-up to fair market value)."
    ),
    reasoning_framework=(
        "STEP 1: Identify eligible capital gain (short-term or long-term, "
        "from any source — not limited to real estate gains).\n"
        "STEP 2: Invest the gain amount into a QOF within 180 days. Only the "
        "gain amount needs to be invested, not the full proceeds.\n"
        "STEP 3: The QOF must hold at least 90% of assets in qualified "
        "opportunity zone property, tested semi-annually.\n"
        "STEP 4: A Qualified Opportunity Zone Business (QOZB) must meet: "
        "70% tangible property in zone, 50% gross income from active conduct "
        "in zone, nonqualified financial property under 5%.\n"
        "STEP 5: The original basis step-ups (10% at 5 years, 15% at 7 years) "
        "expired December 31, 2026 and December 31, 2026 respectively. "
        "For investments made after 2019, only the 10-year exclusion remains.\n"
        "STEP 6: Deferred gain is recognized on December 31, 2026, or upon "
        "earlier disposition of the QOF interest.\n"
        "STEP 7: After 10 years, elect to step up basis to FMV — all "
        "appreciation in QOF investment is permanently excluded.\n"
        "STEP 8: Self-certification on Form 8996 (annual) and Form 8949 "
        "(for gain deferral election)."
    ),
    key_factors=[
        "180-day investment window from date of gain recognition",
        "Only the gain amount must be invested (not full proceeds)",
        "QOF must hold 90%+ in qualified opportunity zone property",
        "Deferred gain recognized December 31, 2026 (or earlier disposition)",
        "10-year hold provides permanent exclusion of QOF appreciation",
        "Original 5-year/7-year basis step-ups largely expired",
        "Self-certification via Form 8996 and Form 8949",
        "QOZB must conduct active business in the zone",
    ],
    primary_authority=[
        "IRC 1400Z-1 - Designation of Qualified Opportunity Zones",
        "IRC 1400Z-2 - Special Rules for Capital Gains Invested in QOFs",
        "Reg. 1.1400Z2(a)-1 through 1.1400Z2(f)-1 (Final Regulations 2020)",
        "TCJA 2017, Section 13823 (Opportunity Zone Provisions)",
        "IRS FAQ on Opportunity Zones (updated periodically)",
    ],
    burden_holder="Taxpayer/QOF must demonstrate compliance with 90% test, QOZB requirements, and holding period",
    adversary_position=(
        "IRS may challenge: (1) 180-day investment window missed, (2) QOF "
        "fails 90% asset test, (3) QOZB does not meet active conduct test, "
        "(4) nonqualified financial property exceeds 5%, (5) zone designation "
        "expired or was improper."
    ),
    counter_arguments=[
        "180-day window disputes for installment sales and partnership gains",
        "QOF compliance testing is complex and penalties apply for failure",
        "Real estate development projects may not meet substantial improvement test",
        "Working capital safe harbor has strict 31-month timeline",
        "State tax treatment of OZ gains varies significantly",
    ],
    resolution_strategy=(
        "Invest within 180 days of gain event. Structure QOF as LLC or corp "
        "with clear 90% asset testing procedures. Ensure QOZB property "
        "is substantially improved (doubles original basis in 30 months). "
        "File Form 8996 annually. Plan for 2026 gain recognition event."
    ),
    entity_scope=["individual", "partnership", "llc", "s_corp", "c_corp", "trust"],
    confidence="DEFENSIBLE",
    confidence_stratification="DEFENSIBLE",
    controlling_precedent="Reg. 1.1400Z2(a)-1 (2020 Final Regulations)",
    irc_sections=["1400Z-1", "1400Z-2"],
    related_doctrines=["like_kind_exchange_1031"],
    effective_dates="Zone designations through 2028; investment benefits vary by year",
))


# =============================================================================
# 11. INSTALLMENT SALE - IRC 453
# =============================================================================

_register(DoctrineBlock(
    topic="installment_sale_453",
    keywords=[
        "installment sale", "installment method", "section 453",
        "deferred gain", "gross profit ratio", "interest charge",
        "dealer exclusion", "related party",
    ],
    conclusion_template=(
        "IRC 453 allows sellers of real property to report gain ratably as "
        "payments are received, rather than recognizing all gain in the year "
        "of sale. The gross profit ratio (gain/contract price) determines the "
        "taxable portion of each payment. Depreciation recapture under "
        "Section 1250 must be recognized in year one regardless of payment "
        "receipt. Dealers in real property are excluded from installment reporting."
    ),
    reasoning_framework=(
        "STEP 1: Confirm eligibility — not a dealer in real property (held "
        "primarily for sale to customers in the ordinary course of business).\n"
        "STEP 2: Calculate the gross profit ratio: (Selling Price - Adjusted "
        "Basis - Selling Expenses) / Contract Price.\n"
        "STEP 3: Contract Price = Selling Price - Existing Mortgage Assumed "
        "(but not below zero; excess mortgage over basis is payment in year 1).\n"
        "STEP 4: Each payment received: Payment x Gross Profit Ratio = Gain "
        "recognized. Remainder is return of basis.\n"
        "STEP 5: Section 1250 depreciation recapture is accelerated — recognized "
        "in full in year of sale regardless of payment schedule.\n"
        "STEP 6: If selling price exceeds $150,000 and face amount of all "
        "installment obligations exceeds $5 million, IRC 453A interest charge "
        "applies on the deferred tax liability.\n"
        "STEP 7: Related party rules (453(e)): if buyer disposes within 2 years, "
        "seller recognizes remaining gain immediately.\n"
        "STEP 8: Election out available — taxpayer may elect out of installment "
        "method on a timely filed return."
    ),
    key_factors=[
        "Dealer property (held for sale to customers) is excluded",
        "Section 1250 depreciation recapture recognized in year one",
        "Gross profit ratio determines taxable portion of each payment",
        "453A interest charge for obligations exceeding $5 million",
        "Related party 2-year disposition rule accelerates gain",
        "Election out must be made on timely filed return",
        "Mortgage assumption reduces contract price",
    ],
    primary_authority=[
        "IRC 453 - Installment Method",
        "IRC 453A - Interest Charge on Deferred Tax",
        "IRC 453(e) - Related Party Rules",
        "Reg. 1.453-1 through 1.453-12",
        "Pitts v. Commissioner, 557 F.2d 531 (5th Cir. 1977)",
    ],
    burden_holder="Taxpayer must prove non-dealer status and proper gain recognition computation",
    adversary_position=(
        "IRS may argue: (1) taxpayer is a dealer, not an investor, "
        "(2) installment sale is a disguised cash sale with a loan back, "
        "(3) related party rules triggered, (4) 453A interest not properly computed."
    ),
    counter_arguments=[
        "Dealer vs. investor classification is highly fact-intensive",
        "Wraparound mortgages create complex computation issues",
        "Related party rules can trap inadvertent dispositions (foreclosure)",
        "453A interest charge can negate much of the deferral benefit",
        "Pledging installment note as collateral triggers deemed payment",
    ],
    resolution_strategy=(
        "Document investment intent (hold period, no marketing for sale). "
        "Compute gross profit ratio carefully, especially with mortgage "
        "assumptions. Recognize all Section 1250 recapture in year one. "
        "Avoid related party transactions. Monitor $5M threshold for 453A."
    ),
    entity_scope=["individual", "partnership", "llc", "s_corp", "c_corp", "trust"],
    confidence="DEFENSIBLE",
    confidence_stratification="DEFENSIBLE",
    controlling_precedent="Pitts v. Commissioner, 557 F.2d 531 (5th Cir. 1977)",
    irc_sections=["453", "453A", "453(e)", "1250"],
    related_doctrines=["depreciation_recapture_1250"],
))


# =============================================================================
# 12. DEPRECIATION RECAPTURE - SECTION 1250
# =============================================================================

_register(DoctrineBlock(
    topic="depreciation_recapture_1250",
    keywords=[
        "depreciation recapture", "section 1250", "unrecaptured gain",
        "25% rate", "1250 gain", "straight line recapture",
        "real property recapture",
    ],
    conclusion_template=(
        "Section 1250 depreciation recapture requires that gain on the sale "
        "of depreciable real property attributable to depreciation in excess "
        "of straight-line is recaptured as ordinary income. Since MACRS uses "
        "straight-line for real property, the excess recapture is typically "
        "zero. However, unrecaptured Section 1250 gain (depreciation taken "
        "at straight-line rates) is taxed at a maximum 25% rate rather than "
        "the 20% long-term capital gains rate."
    ),
    reasoning_framework=(
        "STEP 1: Calculate total depreciation taken on the property (or "
        "allowed, whichever is greater).\n"
        "STEP 2: Determine if any depreciation was in excess of straight-line "
        "(pre-1987 ACRS property or transitional property). If so, that "
        "excess is ordinary income under Section 1250(a).\n"
        "STEP 3: For post-1986 MACRS property (most current real estate), "
        "all depreciation was straight-line, so Section 1250(a) recapture is "
        "zero. However, unrecaptured Section 1250 gain applies.\n"
        "STEP 4: Unrecaptured Section 1250 gain = lesser of: (a) total "
        "depreciation taken, or (b) gain on sale. Taxed at max 25% rate.\n"
        "STEP 5: Remaining gain (above unrecaptured 1250) is taxed at "
        "normal capital gains rates (0%, 15%, or 20% plus 3.8% NIIT).\n"
        "STEP 6: For cost segregation property reclassified as Section 1245 "
        "personal property, full recapture at ordinary income rates applies.\n"
        "STEP 7: In installment sales, Section 1250 recapture is accelerated "
        "and recognized in year of sale regardless of payment timing.\n"
        "STEP 8: In like-kind exchanges, recapture is deferred (built into "
        "replacement property basis)."
    ),
    key_factors=[
        "Excess depreciation over straight-line: ordinary income (rare for post-1986 property)",
        "Unrecaptured 1250 gain: taxed at maximum 25% rate",
        "Section 1245 personal property (from cost seg): full ordinary recapture",
        "Installment sales: recapture recognized in year one",
        "Like-kind exchanges: recapture deferred into replacement property",
        "Depreciation allowed or allowable (higher of) is used",
    ],
    primary_authority=[
        "IRC 1250 - Gain from Dispositions of Certain Depreciable Realty",
        "IRC 1(h)(1)(E) - Unrecaptured Section 1250 Gain Rate",
        "IRC 1245 - Personal Property Recapture (for cost seg reclassified items)",
        "Reg. 1.1250-1 through 1.1250-5",
    ],
    burden_holder="Taxpayer must compute recapture based on depreciation allowed or allowable",
    adversary_position=(
        "IRS may assert: (1) depreciation was allowable even if not claimed, "
        "(2) cost segregation items are Section 1245 property with full recapture, "
        "(3) incorrect basis computation understates recapture."
    ),
    counter_arguments=[
        "Depreciation allowable (even if not taken) is used for recapture",
        "Cost segregation creates Section 1245 recapture at ordinary rates",
        "Basis computation errors cascade into incorrect recapture amounts",
        "Net investment income tax (3.8%) applies on top of 25% rate",
        "Partnership distributions may trigger unexpected recapture",
    ],
    resolution_strategy=(
        "Maintain detailed depreciation schedules for all properties. "
        "Separate Section 1245 and Section 1250 property in records. "
        "Compute unrecaptured 1250 gain on Form 4797 and Schedule D. "
        "Consider 1031 exchange to defer recapture on sale."
    ),
    entity_scope=["individual", "partnership", "llc", "s_corp", "c_corp", "reit", "trust"],
    confidence="DEFENSIBLE",
    confidence_stratification="DEFENSIBLE",
    controlling_precedent="IRC 1(h)(1)(E) (statutory rate provision)",
    irc_sections=["1250", "1245", "1(h)(1)(E)"],
    related_doctrines=["cost_segregation", "like_kind_exchange_1031", "installment_sale_453"],
))


# =============================================================================
# 13. PRIMARY RESIDENCE EXCLUSION - SECTION 121
# =============================================================================

_register(DoctrineBlock(
    topic="primary_residence_121",
    keywords=[
        "primary residence", "home sale exclusion", "section 121",
        "250000 exclusion", "500000 exclusion", "ownership test",
        "use test", "unforeseen circumstances",
    ],
    conclusion_template=(
        "IRC 121 excludes up to $250,000 ($500,000 for married filing jointly) "
        "of gain on the sale of a principal residence. The taxpayer must have "
        "owned and used the property as a principal residence for at least "
        "2 of the 5 years preceding the sale. A reduced exclusion is available "
        "for sales due to health, change of employment, or unforeseen circumstances."
    ),
    reasoning_framework=(
        "STEP 1: Verify ownership test — taxpayer must own the property for "
        "at least 2 of the 5 years before the date of sale.\n"
        "STEP 2: Verify use test — taxpayer must use the property as principal "
        "residence for at least 2 of the 5 years (730 days, need not be "
        "consecutive).\n"
        "STEP 3: For married filing jointly ($500K), both spouses must meet "
        "the use test, and at least one must meet the ownership test.\n"
        "STEP 4: The exclusion cannot be used more than once every 2 years.\n"
        "STEP 5: If ownership or use test not fully met, a reduced exclusion "
        "may apply if sale is due to: change of employment (50+ miles), "
        "health reasons, or unforeseen circumstances (Reg. 1.121-3).\n"
        "STEP 6: Reduced exclusion = max exclusion x (months qualifying / 24).\n"
        "STEP 7: Depreciation claimed after May 6, 1997 for home office or "
        "rental conversion is NOT excludable — taxed as Section 1250 gain.\n"
        "STEP 8: Gain beyond the exclusion is capital gain (long-term if "
        "held over 1 year). Report on Form 8949 / Schedule D."
    ),
    key_factors=[
        "$250K single / $500K MFJ exclusion amount",
        "2-year ownership test within 5-year lookback",
        "2-year use test within 5-year lookback (need not be consecutive)",
        "Cannot use more than once every 2 years",
        "Reduced exclusion for health, employment change, unforeseen circumstances",
        "Post-May 1997 depreciation (home office/rental) is not excludable",
        "Both spouses must meet use test for $500K exclusion",
    ],
    primary_authority=[
        "IRC 121 - Exclusion of Gain from Sale of Principal Residence",
        "Reg. 1.121-1 through 1.121-4",
        "Reg. 1.121-3 - Reduced Maximum Exclusion",
        "Guinan v. Commissioner, T.C. Memo 2015-61",
    ],
    burden_holder="Taxpayer must prove ownership, use, and principal residence status",
    adversary_position=(
        "IRS may argue: (1) property was not principal residence (rental or "
        "vacation use predominated), (2) ownership/use tests not met, "
        "(3) exclusion claimed within 2 years of prior use, (4) depreciation "
        "recapture not properly reported."
    ),
    counter_arguments=[
        "Multiple residence situations require facts-and-circumstances analysis",
        "Temporary absences (vacation, medical) generally count as use",
        "Military and intelligence community members get extended lookback",
        "Home office depreciation recapture is often overlooked",
        "Divorce-related transfers create complex ownership test issues",
    ],
    resolution_strategy=(
        "Document principal residence status with utility bills, voter "
        "registration, driver's license. Track 2-year ownership and use "
        "periods. Compute depreciation recapture for any home office periods. "
        "For partial exclusion, document qualifying reason."
    ),
    entity_scope=["individual"],
    confidence="DEFENSIBLE",
    confidence_stratification="DEFENSIBLE",
    controlling_precedent="Guinan v. Commissioner, T.C. Memo 2015-61",
    irc_sections=["121", "121(b)", "121(c)"],
    related_doctrines=["depreciation_recapture_1250"],
))


# =============================================================================
# 14. REIT TAXATION - IRC 856-860
# =============================================================================

_register(DoctrineBlock(
    topic="reit_taxation_856",
    keywords=[
        "reit", "real estate investment trust", "section 856",
        "distribution requirement", "asset test", "income test",
        "taxable reit subsidiary", "trs",
    ],
    conclusion_template=(
        "A Real Estate Investment Trust (REIT) under IRC 856-860 provides "
        "flow-through taxation if it distributes at least 90% of taxable "
        "income annually. REITs must meet asset tests (75% real estate assets), "
        "income tests (75% real estate income, 95% passive income), and "
        "organizational tests (100+ shareholders, not closely held). Taxable "
        "REIT subsidiaries (TRS) handle non-qualifying activities."
    ),
    reasoning_framework=(
        "STEP 1: Organizational test — at least 100 shareholders, no 5 or "
        "fewer individuals owning more than 50% (5/50 test).\n"
        "STEP 2: Asset tests (quarterly): 75% of assets must be real estate "
        "assets, cash, and government securities. No more than 25% in TRS "
        "securities. No single non-REIT/non-government issuer > 5%.\n"
        "STEP 3: Income tests (annual): 75% gross income from real property "
        "rents, mortgage interest, real property gains. 95% from 75% sources "
        "plus dividends, interest, and gains from security sales.\n"
        "STEP 4: Distribution: 90% of REIT taxable income must be distributed "
        "to avoid entity-level tax. 4% excise tax on underdistributed amounts.\n"
        "STEP 5: REIT dividends are generally ordinary income to shareholders "
        "(not qualified dividends), but the 199A 20% deduction may apply.\n"
        "STEP 6: TRS handles non-qualifying activities (hotel management, "
        "active services). TRS taxed at corporate rate.\n"
        "STEP 7: Failure to meet tests: cure provisions available for asset "
        "and income test failures (de minimis exceptions, penalty tax).\n"
        "STEP 8: Built-in gain tax applies to C-to-REIT conversions (5-year "
        "recognition period)."
    ),
    key_factors=[
        "90% distribution requirement to avoid entity-level tax",
        "75% asset test (real estate, cash, government securities)",
        "75% and 95% income tests",
        "100 shareholder test and 5/50 anti-concentration rule",
        "TRS for non-qualifying activities (limited to 20% of REIT assets)",
        "Section 199A deduction available on REIT dividends",
        "Built-in gain tax on C-to-REIT conversions (5-year period)",
    ],
    primary_authority=[
        "IRC 856-860 - REIT Provisions",
        "IRC 857(a) - Distribution Requirements",
        "IRC 856(c) - Income and Asset Tests",
        "Reg. 1.856-1 through 1.860-4",
        "Rev. Rul. 2001-29 (REIT Customary Services)",
    ],
    burden_holder="REIT bears burden to demonstrate continuous compliance with all REIT qualification tests",
    adversary_position=(
        "IRS may challenge: (1) rental income characterization (impermissible "
        "services provided), (2) asset test failures, (3) TRS exceeding 20% "
        "limit, (4) related party rental arrangements at non-arm's length."
    ),
    counter_arguments=[
        "Impermissible tenant services can disqualify rental income",
        "TRS intercompany pricing must be at arm's length (penalty tax applies)",
        "Quarterly asset testing creates ongoing compliance burden",
        "Loss of REIT status has severe consequences (entity-level tax, 5-year lockout)",
        "Closely held restrictions require ongoing shareholder monitoring",
    ],
    resolution_strategy=(
        "Monitor asset and income tests quarterly. Use TRS for non-qualifying "
        "activities. Maintain 100+ shareholder count through public offering "
        "or preferred stock. Distribute at least 90% of taxable income. "
        "Engage REIT tax counsel for complex transactions."
    ),
    entity_scope=["reit", "c_corp"],
    confidence="DEFENSIBLE",
    confidence_stratification="DEFENSIBLE",
    controlling_precedent="Rev. Rul. 2001-29 (customary services definition)",
    irc_sections=["856", "857", "858", "859", "860"],
    related_doctrines=["section_199a_real_estate"],
))


# =============================================================================
# 15. LIHTC - IRC 42
# =============================================================================

_register(DoctrineBlock(
    topic="lihtc_42",
    keywords=[
        "lihtc", "low income housing", "section 42", "tax credit",
        "qualified basis", "applicable percentage", "compliance period",
        "4 percent credit", "9 percent credit", "recapture",
    ],
    conclusion_template=(
        "The Low-Income Housing Tax Credit under IRC 42 provides dollar-for-dollar "
        "federal income tax credits for the development of affordable rental "
        "housing. The 9% credit applies to new construction without federal "
        "subsidies, while the 4% credit applies to acquisition and projects "
        "financed with tax-exempt bonds. Credits are claimed annually over "
        "a 10-year credit period, with a 15-year compliance period."
    ),
    reasoning_framework=(
        "STEP 1: Determine credit type — 9% (new construction, no federal "
        "subsidy) or 4% (acquisition, tax-exempt bond financed).\n"
        "STEP 2: Calculate qualified basis = eligible basis x applicable "
        "fraction (lesser of unit fraction or floor space fraction).\n"
        "STEP 3: Eligible basis includes depreciable costs of buildings, "
        "excluding land, but including construction, rehabilitation, and "
        "allocated development costs.\n"
        "STEP 4: Annual credit = qualified basis x applicable percentage "
        "(approximately 9% or 4% depending on program).\n"
        "STEP 5: Credits claimed over 10-year credit period beginning when "
        "the building is placed in service or beginning of the first taxable "
        "year after allocation.\n"
        "STEP 6: 15-year compliance period — project must maintain income and "
        "rent restrictions. Failure triggers recapture.\n"
        "STEP 7: Recapture (IRC 42(j)) — accelerated portion of prior credits "
        "must be repaid if compliance fails during 15-year period.\n"
        "STEP 8: State housing credit agencies allocate credits. Competitive "
        "process with qualified allocation plan (QAP)."
    ),
    key_factors=[
        "9% credit for new construction without federal subsidy",
        "4% credit for acquisition and tax-exempt bond projects",
        "10-year credit period, 15-year compliance period",
        "Qualified basis = eligible basis x applicable fraction",
        "Income and rent restrictions must be maintained throughout compliance period",
        "Recapture upon noncompliance during 15-year period",
        "State housing agencies administer allocation and monitoring",
        "30-year extended use period in most states",
    ],
    primary_authority=[
        "IRC 42 - Low-Income Housing Tax Credit",
        "IRC 42(j) - Recapture of Credit",
        "Reg. 1.42-1 through 1.42-19",
        "Rev. Rul. 2004-82 (Eligible Basis)",
        "IRS Guide for Completing Form 8609",
    ],
    burden_holder="Developer/owner must demonstrate and maintain compliance throughout the compliance period",
    adversary_position=(
        "IRS/state HFA may challenge: (1) eligible basis computation, "
        "(2) applicable fraction calculation, (3) income certification of "
        "tenants, (4) habitability standards, (5) noncompliance triggering recapture."
    ),
    counter_arguments=[
        "Noncompliance recapture creates significant financial risk",
        "Extended use period (30 years in most states) limits exit strategies",
        "Eligible basis disputes for community service facilities",
        "Related party construction contracts may inflate eligible basis",
        "Annual income recertification is administratively burdensome",
    ],
    resolution_strategy=(
        "Engage experienced LIHTC syndicator and legal counsel. Maintain "
        "rigorous tenant income certification processes. Monitor applicable "
        "fraction quarterly. Budget for 15-year compliance monitoring. "
        "Document all eligible basis components thoroughly."
    ),
    entity_scope=["partnership", "llc", "c_corp"],
    confidence="DEFENSIBLE",
    confidence_stratification="DEFENSIBLE",
    controlling_precedent="Rev. Rul. 2004-82",
    irc_sections=["42", "42(j)"],
    related_doctrines=["reit_taxation_856"],
))


# =============================================================================
# 16. SECTION 179D - ENERGY EFFICIENT COMMERCIAL BUILDINGS
# =============================================================================

_register(DoctrineBlock(
    topic="section_179d_energy",
    keywords=[
        "179d", "energy efficient", "commercial building", "deduction",
        "building envelope", "hvac", "lighting", "ira enhancement",
        "prevailing wage",
    ],
    conclusion_template=(
        "IRC 179D allows a deduction for energy efficient commercial building "
        "property. As enhanced by the Inflation Reduction Act, the maximum "
        "deduction is $5.00 per square foot for buildings meeting prevailing "
        "wage and apprenticeship requirements (or $1.00/sq ft base). The "
        "deduction applies to new construction or retrofits of envelope, "
        "HVAC, hot water, and interior lighting systems achieving energy "
        "savings thresholds."
    ),
    reasoning_framework=(
        "STEP 1: Determine if the building is commercial (or government/non-profit "
        "with designer allocation).\n"
        "STEP 2: Post-IRA (2023+): building must achieve 25%+ energy cost "
        "savings vs. ASHRAE 90.1 reference standard. Above 25%, sliding scale "
        "increases deduction.\n"
        "STEP 3: Base deduction: $0.50-$1.00/sq ft. Enhanced deduction "
        "(prevailing wage + apprenticeship): $2.50-$5.00/sq ft.\n"
        "STEP 4: Partial deductions available for individual systems "
        "(envelope, HVAC/hot water, lighting) meeting system-specific savings.\n"
        "STEP 5: Certification required by qualified third-party inspector "
        "using approved software (DOE-approved).\n"
        "STEP 6: For government/tax-exempt buildings, the deduction is "
        "allocated to the designer (architect, engineer, contractor).\n"
        "STEP 7: Post-IRA, the deduction is available annually (previously "
        "was one-time per building). Retrofit deductions available every 3-4 years.\n"
        "STEP 8: Document all energy modeling, certifications, and prevailing "
        "wage compliance records."
    ),
    key_factors=[
        "Maximum $5.00/sq ft (enhanced) or $1.00/sq ft (base) deduction",
        "25% minimum energy savings vs. ASHRAE reference standard",
        "Prevailing wage and apprenticeship requirements for enhanced amount",
        "Third-party certification required",
        "Designers can claim for government/tax-exempt buildings",
        "Post-IRA: repeating deduction available (not just one-time)",
        "Partial deductions for individual building systems",
    ],
    primary_authority=[
        "IRC 179D - Energy Efficient Commercial Buildings Deduction",
        "Inflation Reduction Act 2022, Section 13303 (179D Enhancement)",
        "Notice 2023-29 (Prevailing Wage and Apprenticeship Guidance)",
        "IRS Interim Guidance (Notice 2006-52, Notice 2008-40)",
        "ASHRAE Standard 90.1 (Reference Building Standard)",
    ],
    burden_holder="Taxpayer (or designer) must obtain third-party certification and document prevailing wage compliance",
    adversary_position=(
        "IRS may challenge: (1) energy modeling methodology, (2) certification "
        "by unqualified inspector, (3) prevailing wage noncompliance reducing "
        "to base amount, (4) improper designer allocation."
    ),
    counter_arguments=[
        "Energy modeling disputes between taxpayer and IRS engineers",
        "Prevailing wage compliance documentation is extensive",
        "ASHRAE reference standard version disputes",
        "Designer allocation for government buildings has limited guidance",
        "Retrofit deduction eligibility timing rules are complex",
    ],
    resolution_strategy=(
        "Engage a qualified 179D engineer using DOE-approved software. "
        "Document prevailing wage compliance for all construction workers. "
        "Obtain certification before claiming the deduction. "
        "Maintain energy modeling reports and compliance records."
    ),
    entity_scope=["individual", "partnership", "llc", "s_corp", "c_corp", "reit"],
    confidence="DEFENSIBLE",
    confidence_stratification="DEFENSIBLE",
    controlling_precedent="Notice 2023-29 (IRA Implementation Guidance)",
    irc_sections=["179D"],
    related_doctrines=["cost_segregation", "bonus_depreciation_168k"],
    effective_dates="Permanent (enhanced by IRA effective 2023+)",
))


# =============================================================================
# 17. AT-RISK RULES - IRC 465
# =============================================================================

_register(DoctrineBlock(
    topic="at_risk_real_estate_465",
    keywords=[
        "at risk", "at-risk rules", "section 465", "qualified nonrecourse",
        "nonrecourse financing", "amount at risk", "real estate exception",
    ],
    conclusion_template=(
        "IRC 465 limits deductions to the amount the taxpayer has at risk "
        "in an activity. For real estate, qualified nonrecourse financing "
        "from banks and government agencies counts as at-risk, providing a "
        "significant exception to the general rule that nonrecourse debt is "
        "not at-risk. The at-risk limitation applies before the passive "
        "activity loss rules."
    ),
    reasoning_framework=(
        "STEP 1: Calculate amount at risk: cash invested + adjusted basis "
        "of contributed property + qualified nonrecourse financing + recourse "
        "debt for which taxpayer is personally liable.\n"
        "STEP 2: Qualified nonrecourse financing for real estate: must be "
        "from a qualified lender (bank, savings institution, or government), "
        "secured by real property used in the activity, and no person is "
        "personally liable.\n"
        "STEP 3: Seller financing is NOT qualified nonrecourse (related party).\n"
        "STEP 4: Losses exceeding at-risk amount are suspended and carry "
        "forward to future years.\n"
        "STEP 5: At-risk amount is reduced by losses and distributions, "
        "increased by income and additional investments.\n"
        "STEP 6: At-risk applies before passive activity rules — a loss must "
        "clear both hurdles to be deductible.\n"
        "STEP 7: Partnerships report each partner's at-risk amount; partners "
        "must separately track their own at-risk basis.\n"
        "STEP 8: Conversion from recourse to nonrecourse may reduce at-risk amount."
    ),
    key_factors=[
        "Real estate has special qualified nonrecourse financing exception",
        "Qualified lender: bank, savings institution, or government agency",
        "Seller financing is NOT qualified nonrecourse",
        "At-risk applies BEFORE passive activity rules",
        "Losses exceeding at-risk amount are suspended and carry forward",
        "At-risk basis is reduced by distributions and losses",
    ],
    primary_authority=[
        "IRC 465 - At-Risk Limitations",
        "IRC 465(b)(6) - Qualified Nonrecourse Financing for Real Property",
        "Reg. 1.465-1 through 1.465-27",
        "Hubert v. Commissioner, 94 T.C. 1 (1990)",
    ],
    burden_holder="Taxpayer bears burden to prove amount at risk and qualification of nonrecourse financing",
    adversary_position=(
        "IRS may argue: (1) financing is not from a qualified lender, "
        "(2) seller financing disguised as bank financing, (3) at-risk amount "
        "reduced below zero by distributions, (4) circular financing arrangements."
    ),
    counter_arguments=[
        "Seller financing precludes qualified nonrecourse treatment",
        "Cross-collateralized loans may not qualify",
        "Guarantee arrangements can create at-risk but with personal liability",
        "Tiered partnership structures complicate at-risk tracking",
        "Refinancing may change at-risk amounts",
    ],
    resolution_strategy=(
        "Ensure real estate debt is from qualified lenders (banks, not sellers). "
        "Track at-risk basis annually for each activity. Apply at-risk "
        "limitations before passive activity rules on Form 6198. "
        "Document loan terms and lender qualifications."
    ),
    entity_scope=["individual", "partnership", "llc", "s_corp", "trust"],
    confidence="DEFENSIBLE",
    confidence_stratification="DEFENSIBLE",
    controlling_precedent="Hubert v. Commissioner, 94 T.C. 1 (1990)",
    irc_sections=["465", "465(b)(6)"],
    related_doctrines=["passive_activity_469"],
))


# =============================================================================
# 18. CONSTRUCTION INTEREST CAPITALIZATION - IRC 263A
# =============================================================================

_register(DoctrineBlock(
    topic="construction_interest_263a",
    keywords=[
        "263a", "unicap", "uniform capitalization", "construction interest",
        "production period", "capitalized interest", "self-constructed property",
    ],
    conclusion_template=(
        "IRC 263A requires capitalization of direct and allocable indirect "
        "costs (including interest) incurred during the production period "
        "of real property constructed by or for the taxpayer. Construction "
        "period interest must be capitalized into the basis of the property "
        "rather than deducted currently. The production period begins when "
        "construction starts and ends when the property is ready for its "
        "intended use."
    ),
    reasoning_framework=(
        "STEP 1: Determine if the property is self-constructed or produced "
        "under contract. Both are subject to 263A for real property.\n"
        "STEP 2: Identify the production period: begins when physical "
        "construction activity starts, ends when property placed in service.\n"
        "STEP 3: Capitalize direct costs: materials, labor, subcontractor costs.\n"
        "STEP 4: Capitalize indirect costs: interest on debt traceable to "
        "construction, insurance, taxes, overhead allocable to production.\n"
        "STEP 5: Interest capitalization uses the avoided cost method: "
        "capitalize interest on accumulated expenditures during production.\n"
        "STEP 6: Only interest on debt used or reasonably allocable to "
        "production is subject to capitalization.\n"
        "STEP 7: Pre-production costs (architectural, engineering, permits) "
        "incurred before physical construction are also capitalizable.\n"
        "STEP 8: Once placed in service, capitalized costs become part of "
        "depreciable basis and are recovered through MACRS depreciation."
    ),
    key_factors=[
        "Real property construction requires UNICAP treatment",
        "Production period: physical construction start to placed in service",
        "Interest on construction debt must be capitalized (avoided cost method)",
        "Direct and indirect costs are capitalizable",
        "Pre-production costs (design, permits) are also capitalized",
        "Capitalized costs become depreciable basis at placed in service",
    ],
    primary_authority=[
        "IRC 263A - Uniform Capitalization Rules",
        "Reg. 1.263A-1 through 1.263A-15",
        "IRC 263A(f) - Interest Capitalization",
        "Reg. 1.263A-8 through 1.263A-15 (Interest Capitalization Rules)",
    ],
    burden_holder="Taxpayer must properly identify and capitalize all required costs during the production period",
    adversary_position=(
        "IRS may argue: (1) production period started earlier than claimed, "
        "(2) indirect costs not properly allocated, (3) interest capitalization "
        "understated, (4) pre-production costs improperly deducted."
    ),
    counter_arguments=[
        "Production period start date disputes (site preparation vs. foundation)",
        "Indirect cost allocation methods are complex and fact-intensive",
        "Mixed-use financing creates interest allocation challenges",
        "Small taxpayer exceptions may apply for certain activities",
        "De minimis rules for minor costs may be disputed",
    ],
    resolution_strategy=(
        "Document construction start and completion dates precisely. "
        "Track debt draws and their use for construction. Apply avoided "
        "cost method for interest capitalization. Allocate indirect costs "
        "using a reasonable method. Maintain cost segregation-ready records."
    ),
    entity_scope=["individual", "partnership", "llc", "s_corp", "c_corp", "reit"],
    confidence="DEFENSIBLE",
    confidence_stratification="DEFENSIBLE",
    controlling_precedent="Reg. 1.263A-8 (Interest Capitalization Methodology)",
    irc_sections=["263A", "263A(f)"],
    related_doctrines=["cost_segregation", "bonus_depreciation_168k"],
))


# =============================================================================
# 19. DEMOLITION COSTS - IRC 280B
# =============================================================================

_register(DoctrineBlock(
    topic="demolition_280b",
    keywords=[
        "demolition", "280b", "section 280b", "tear down",
        "demolition costs", "razed building", "capitalization",
    ],
    conclusion_template=(
        "IRC 280B requires that the costs of demolishing a structure, plus "
        "any undepreciated basis remaining in the demolished structure, must "
        "be capitalized into the land. No current deduction is allowed for "
        "demolition costs or the remaining basis of the demolished building. "
        "These capitalized amounts increase the basis of the land."
    ),
    reasoning_framework=(
        "STEP 1: Determine if a demolition has occurred — complete removal "
        "of a structure (partial demolitions may have different treatment).\n"
        "STEP 2: Calculate the remaining undepreciated basis of the demolished "
        "structure at the time of demolition.\n"
        "STEP 3: Aggregate demolition costs: wrecking contractor fees, "
        "environmental abatement, permits, debris removal.\n"
        "STEP 4: Capitalize both the remaining basis and demolition costs "
        "into the basis of the underlying land.\n"
        "STEP 5: No loss deduction is allowed for the demolished structure "
        "(even if the building had significant remaining basis).\n"
        "STEP 6: Land basis increase is recovered only upon sale of the land "
        "(no depreciation on land).\n"
        "STEP 7: If the intent to demolish existed at acquisition, the entire "
        "building cost may be treated as land cost from the outset.\n"
        "STEP 8: Environmental remediation may qualify for separate deduction "
        "under IRC 198 (if still available)."
    ),
    key_factors=[
        "No current deduction for demolition costs",
        "Remaining basis of demolished structure capitalized to land",
        "Demolition costs capitalized to land",
        "Land is not depreciable — costs recovered only on sale",
        "Intent to demolish at acquisition may reclassify building cost as land",
        "Environmental remediation may be separately deductible under IRC 198",
    ],
    primary_authority=[
        "IRC 280B - Demolition of Structures",
        "Reg. 1.280B-1",
        "IRC 198 - Environmental Remediation (if applicable)",
    ],
    burden_holder="Taxpayer must capitalize demolition costs; IRS may challenge intent at acquisition",
    adversary_position=(
        "IRS may argue: (1) intent to demolish existed at purchase (retroactive "
        "land classification), (2) partial demolition treated as full under 280B, "
        "(3) environmental costs improperly separated from demolition."
    ),
    counter_arguments=[
        "Intent-to-demolish at acquisition creates retroactive classification risk",
        "Partial demolition vs. renovation is a facts-and-circumstances determination",
        "Environmental remediation deduction may have expired",
        "Large remaining basis in demolished building creates significant non-deductible loss",
        "Timing of demolition relative to acquisition is critical evidence",
    ],
    resolution_strategy=(
        "If acquiring property with plans to demolish, allocate purchase price "
        "heavily to land in appraisal. Separate environmental remediation "
        "costs from pure demolition costs. Document the business purpose "
        "for demolition and timeline of decision-making."
    ),
    entity_scope=["individual", "partnership", "llc", "s_corp", "c_corp", "reit"],
    confidence="DEFENSIBLE",
    confidence_stratification="DEFENSIBLE",
    controlling_precedent="Reg. 1.280B-1",
    irc_sections=["280B", "198"],
    related_doctrines=["construction_interest_263a"],
))


# =============================================================================
# 20. TENANT IMPROVEMENTS / QIP
# =============================================================================

_register(DoctrineBlock(
    topic="tenant_improvements_qip",
    keywords=[
        "tenant improvement", "leasehold improvement", "qip",
        "qualified improvement property", "15 year", "lessee",
        "lessor", "construction allowance",
    ],
    conclusion_template=(
        "Qualified Improvement Property (QIP) — interior improvements to "
        "nonresidential real property placed in service after the building "
        "was first placed in service — is depreciable over 15 years under "
        "MACRS (corrected by CARES Act 2020). QIP is eligible for bonus "
        "depreciation. Tenant construction allowances excluded from lessor "
        "income under IRC 110 if used for qualified long-term real property."
    ),
    reasoning_framework=(
        "STEP 1: Determine if the improvement is QIP: interior improvement "
        "to nonresidential real property, placed in service after the building "
        "was first placed in service.\n"
        "STEP 2: Exclusions from QIP: elevators, escalators, enlargement of "
        "the building, internal structural framework.\n"
        "STEP 3: Recovery period: 15 years straight-line (MACRS). ADS: 20 years.\n"
        "STEP 4: QIP is eligible for bonus depreciation (phasing down 2023-2026).\n"
        "STEP 5: Lessee-paid improvements: lessee depreciates over 15 years "
        "(QIP) if they retain benefit. Abandonment loss on lease termination.\n"
        "STEP 6: Lessor-paid improvements: lessor depreciates over recovery "
        "period. If tenant-specific, may be QIP.\n"
        "STEP 7: Construction allowance from lessor to lessee: excluded from "
        "lessee gross income under IRC 110 if used for qualified long-term "
        "real property and lease term is 15+ years.\n"
        "STEP 8: CARES Act technical correction: QIP was intended to be 15-year "
        "property in TCJA but was erroneously left at 39 years; corrected "
        "retroactively to 01/01/2018."
    ),
    key_factors=[
        "QIP: interior improvements to nonresidential real property",
        "15-year recovery period (CARES Act correction)",
        "Eligible for bonus depreciation",
        "Excludes elevators, escalators, enlargement, structural framework",
        "IRC 110 excludes construction allowances if lease is 15+ years",
        "Lessee gets abandonment loss if improvements left behind on termination",
        "ADS recovery period for QIP is 20 years",
    ],
    primary_authority=[
        "IRC 168(e)(6) - Qualified Improvement Property Definition",
        "CARES Act 2020, Section 2307 (QIP Technical Correction)",
        "IRC 110 - Qualified Lessee Construction Allowances",
        "Rev. Proc. 2020-25 (Late QIP Bonus Depreciation Election)",
        "Reg. 1.168(i)-8 (Retirement and Disposition of MACRS Property)",
    ],
    burden_holder="Taxpayer must substantiate that improvements qualify as QIP and are not excluded categories",
    adversary_position=(
        "IRS may argue: (1) improvements are structural framework (not QIP), "
        "(2) improvements enlarge the building (excluded), (3) construction "
        "allowance does not meet IRC 110 requirements, (4) improvements made "
        "before building placed in service (not QIP)."
    ),
    counter_arguments=[
        "Structural framework vs. interior improvement is fact-intensive",
        "Building enlargement exclusion requires careful measurement",
        "IRC 110 lease term requirement (15 years) may not be met",
        "Retroactive QIP correction requires amended returns or Form 3115",
        "ADS requirement for 163(j) electing businesses extends to 20 years",
    ],
    resolution_strategy=(
        "Classify improvements carefully — document that they are interior "
        "and not structural framework. Claim 15-year recovery period with "
        "bonus depreciation. For retroactive correction, file Form 3115 "
        "for automatic change in accounting method."
    ),
    entity_scope=["individual", "partnership", "llc", "s_corp", "c_corp", "reit"],
    confidence="DEFENSIBLE",
    confidence_stratification="DEFENSIBLE",
    controlling_precedent="CARES Act 2020, Section 2307",
    irc_sections=["168(e)(6)", "110"],
    related_doctrines=["bonus_depreciation_168k", "cost_segregation"],
    effective_dates="QIP as 15-year property retroactive to 01/01/2018",
))


# =============================================================================
# 21. GROUND LEASE TAXATION - IRC 110
# =============================================================================

_register(DoctrineBlock(
    topic="ground_lease_taxation",
    keywords=[
        "ground lease", "section 110", "construction allowance",
        "leasehold", "subordinated ground lease", "land lease",
    ],
    conclusion_template=(
        "Ground leases create unique tax issues. Under IRC 110, a lessee "
        "may exclude qualified construction allowances received from a lessor "
        "from gross income if the lease term is at least 15 years and the "
        "allowance is used for qualified long-term real property. Improvements "
        "made by the lessee on leased land are depreciable by the lessee over "
        "the applicable MACRS recovery period, not the lease term."
    ),
    reasoning_framework=(
        "STEP 1: Determine if the ground lease creates a leasehold interest "
        "or is recharacterized as a sale/financing (substance over form).\n"
        "STEP 2: Lessee improvements on ground lease: depreciable by lessee "
        "over MACRS recovery period (27.5yr residential, 39yr commercial).\n"
        "STEP 3: At lease expiration, improvements revert to lessor — lessor "
        "does NOT recognize income (IRC 109 exclusion).\n"
        "STEP 4: Construction allowances: excluded under IRC 110 if qualifying.\n"
        "STEP 5: Ground rent payments: ordinary deduction for lessee if "
        "trade or business expense. Ordinary income for lessor.\n"
        "STEP 6: Prepaid rent: capitalize and amortize over lease term.\n"
        "STEP 7: Long-term ground leases (99 years) may be treated more "
        "like fee ownership for some purposes.\n"
        "STEP 8: Lease termination payments may be capital gain to lessor "
        "or ordinary deduction to lessee depending on characterization."
    ),
    key_factors=[
        "IRC 110 excludes qualified construction allowances from lessee income",
        "Lease term must be at least 15 years for IRC 110 exclusion",
        "Lessee depreciates improvements over MACRS period (not lease term)",
        "IRC 109 excludes lessor from income on improvement reversion",
        "Substance over form may recharacterize as sale/financing",
        "Ground rent is ordinary expense/income",
    ],
    primary_authority=[
        "IRC 110 - Qualified Lessee Construction Allowances",
        "IRC 109 - Improvements by Lessee on Lessor's Property",
        "IRC 178 - Amortization of Cost of Acquiring a Lease",
        "Reg. 1.109-1",
    ],
    burden_holder="Taxpayer must demonstrate lease is genuine and construction allowance meets IRC 110 requirements",
    adversary_position=(
        "IRS may recharacterize a long-term ground lease as a purchase/sale "
        "if economic substance indicates transfer of ownership benefits."
    ),
    counter_arguments=[
        "Long-term ground leases may be recharacterized as ownership",
        "IRC 110 requirements (15-year term, qualified property) must be strictly met",
        "Lease termination payments create characterization disputes",
        "Related party ground leases face additional scrutiny",
    ],
    resolution_strategy=(
        "Structure ground leases with clear lease terms distinct from ownership. "
        "Document construction allowance compliance with IRC 110. Ensure "
        "lease term meets 15-year minimum for exclusion."
    ),
    entity_scope=["individual", "partnership", "llc", "s_corp", "c_corp", "reit"],
    confidence="DEFENSIBLE",
    confidence_stratification="DEFENSIBLE",
    controlling_precedent="IRC 110 (statutory provision)",
    irc_sections=["110", "109", "178"],
    related_doctrines=["tenant_improvements_qip"],
))


# =============================================================================
# 22. INVOLUNTARY CONVERSION - IRC 1033
# =============================================================================

_register(DoctrineBlock(
    topic="involuntary_conversion_1033",
    keywords=[
        "involuntary conversion", "section 1033", "condemnation",
        "eminent domain", "casualty", "replacement property",
        "2 year replacement", "3 year real property",
    ],
    conclusion_template=(
        "IRC 1033 allows deferral of gain when property is involuntarily "
        "converted through condemnation, casualty, or theft, and the proceeds "
        "are reinvested in similar or related-use property within the "
        "replacement period. For real property condemned by government, the "
        "replacement period is 3 years (vs. 2 years for other conversions), "
        "and the like-kind standard applies instead of similar-use."
    ),
    reasoning_framework=(
        "STEP 1: Identify the involuntary conversion event — condemnation, "
        "casualty, theft, or requisition.\n"
        "STEP 2: Determine replacement period: 2 years for casualty/theft, "
        "3 years for government condemnation of real property.\n"
        "STEP 3: Calculate gain: insurance/condemnation proceeds minus "
        "adjusted basis of converted property.\n"
        "STEP 4: Gain is deferred only to extent proceeds are reinvested "
        "in qualifying replacement property.\n"
        "STEP 5: For condemnation of real property held for business/investment, "
        "replacement property need only be like-kind (same standard as 1031).\n"
        "STEP 6: For casualty/theft, replacement must be similar or related "
        "in service or use (higher standard than like-kind).\n"
        "STEP 7: Basis of replacement property = cost of replacement minus "
        "deferred gain.\n"
        "STEP 8: Election to defer is made by not reporting gain on return "
        "and attaching a statement."
    ),
    key_factors=[
        "Government condemnation: 3-year replacement period, like-kind standard",
        "Casualty/theft: 2-year replacement period, similar-use standard",
        "Only gain (proceeds minus basis) is subject to deferral",
        "Gain deferred only to extent of reinvestment",
        "Like-kind is broader than similar-use standard",
        "Extension of replacement period available from IRS",
        "Election made by not reporting gain and attaching statement",
    ],
    primary_authority=[
        "IRC 1033 - Involuntary Conversions",
        "Reg. 1.1033(a)-1 through 1.1033(g)-1",
        "Liant Record Inc. v. Commissioner, 303 F.2d 326 (2d Cir. 1962)",
        "Rev. Rul. 64-237 (Condemnation Replacement Period)",
    ],
    burden_holder="Taxpayer must prove involuntary conversion, timely reinvestment, and qualifying replacement property",
    adversary_position=(
        "IRS may argue: (1) replacement property does not meet similar-use "
        "test, (2) replacement period expired, (3) conversion was voluntary "
        "(negotiated sale), (4) proceeds not fully reinvested."
    ),
    counter_arguments=[
        "Voluntary sale under threat of condemnation may qualify",
        "Similar-use test is stricter than like-kind for non-condemnation",
        "Replacement period extensions are discretionary with IRS",
        "Partial reinvestment triggers proportional gain recognition",
        "Insurance proceeds received over multiple years create timing issues",
    ],
    resolution_strategy=(
        "Document the involuntary nature of the conversion. Identify "
        "replacement property early within the replacement period. "
        "Request extension before deadline if needed. Reinvest full "
        "proceeds to defer all gain. Attach proper election statement."
    ),
    entity_scope=["individual", "partnership", "llc", "s_corp", "c_corp", "trust"],
    confidence="DEFENSIBLE",
    confidence_stratification="DEFENSIBLE",
    controlling_precedent="Liant Record Inc. v. Commissioner, 303 F.2d 326 (2d Cir. 1962)",
    irc_sections=["1033"],
    related_doctrines=["like_kind_exchange_1031"],
))


# =============================================================================
# 23. HISTORIC REHABILITATION TAX CREDIT - IRC 47
# =============================================================================

_register(DoctrineBlock(
    topic="historic_rehabilitation_credit_47",
    keywords=[
        "historic tax credit", "htc", "section 47", "rehabilitation",
        "certified historic structure", "national register",
        "substantial rehabilitation",
    ],
    conclusion_template=(
        "IRC 47 provides a 20% tax credit for qualified rehabilitation "
        "expenditures on certified historic structures listed on or eligible "
        "for the National Register of Historic Places. The credit must be "
        "taken ratably over 5 years. Qualified expenditures must equal or "
        "exceed the greater of the adjusted basis of the building or $5,000 "
        "(substantial rehabilitation test)."
    ),
    reasoning_framework=(
        "STEP 1: Verify the building is a certified historic structure (listed "
        "on or eligible for National Register of Historic Places).\n"
        "STEP 2: Confirm substantial rehabilitation test: qualified expenditures "
        "must exceed the greater of adjusted basis or $5,000 within 24-month "
        "(or 60-month for phased) measurement period.\n"
        "STEP 3: Calculate qualified rehabilitation expenditures — costs of "
        "rehabilitating the building, excluding land, enlargement, and site work.\n"
        "STEP 4: Credit = 20% of qualified expenditures, taken ratably over "
        "5 years beginning in the year placed in service (post-TCJA change).\n"
        "STEP 5: Rehabilitation must be certified by the Secretary of the "
        "Interior through a 3-part certification process via the National "
        "Park Service.\n"
        "STEP 6: Basis of the building is reduced by the full credit amount.\n"
        "STEP 7: Recapture if the building is disposed of or ceases to be "
        "a certified historic structure within 5 years.\n"
        "STEP 8: Credit can be used by the building owner or passed through "
        "to investors via partnership allocation."
    ),
    key_factors=[
        "20% credit for certified historic structures",
        "Credit taken ratably over 5 years (post-TCJA)",
        "Substantial rehabilitation test must be met",
        "NPS 3-part certification required",
        "Basis reduced by full credit amount",
        "5-year recapture period",
        "Enlargement costs do not qualify",
    ],
    primary_authority=[
        "IRC 47 - Rehabilitation Credit",
        "Reg. 1.47-1 through 1.47-6",
        "TCJA 2017, Section 13402 (5-Year Ratable Credit)",
        "NPS Standards for Rehabilitation (Secretary of Interior's Standards)",
    ],
    burden_holder="Taxpayer must obtain NPS certification and prove substantial rehabilitation test is met",
    adversary_position=(
        "IRS may challenge: (1) building not properly certified, (2) expenditures "
        "include non-qualifying costs, (3) substantial rehabilitation test not met, "
        "(4) recapture triggered by early disposition."
    ),
    counter_arguments=[
        "NPS certification process is lengthy and may delay credit",
        "5-year ratable credit reduces present value benefit",
        "Substantial rehabilitation test may be difficult for high-basis buildings",
        "Recapture risk during 5-year period",
        "State historic credits may have different requirements",
    ],
    resolution_strategy=(
        "Begin NPS certification early (Part 1 before acquisition). "
        "Track qualified expenditures separately from non-qualifying costs. "
        "Plan 24-month measurement period carefully. Maintain building as "
        "certified historic structure for at least 5 years."
    ),
    entity_scope=["individual", "partnership", "llc", "c_corp"],
    confidence="DEFENSIBLE",
    confidence_stratification="DEFENSIBLE",
    controlling_precedent="TCJA 2017, Section 13402",
    irc_sections=["47"],
    related_doctrines=["cost_segregation"],
))


# =============================================================================
# 24. BUSINESS INTEREST LIMITATION - IRC 163(j)
# =============================================================================

_register(DoctrineBlock(
    topic="business_interest_limitation_163j",
    keywords=[
        "163j", "business interest limitation", "interest expense",
        "ati", "adjusted taxable income", "real property election",
        "30% limitation", "floor plan financing",
    ],
    conclusion_template=(
        "IRC 163(j) limits the deduction for business interest expense to "
        "30% of adjusted taxable income (ATI) plus business interest income "
        "and floor plan financing interest. Real property trades or businesses "
        "may elect out of the limitation but must use the Alternative "
        "Depreciation System (ADS) for all real property, forfeiting bonus "
        "depreciation. Disallowed interest carries forward indefinitely."
    ),
    reasoning_framework=(
        "STEP 1: Determine if the business interest limitation applies (gross "
        "receipts over $29 million average for 3 prior years).\n"
        "STEP 2: Calculate ATI: taxable income + interest expense + depreciation "
        "(for years before 2022) + NOL deduction.\n"
        "STEP 3: Limitation: deductible interest = 30% of ATI + business "
        "interest income + floor plan financing interest.\n"
        "STEP 4: Real property trade or business election under 163(j)(7)(B): "
        "elects out of limitation. Irrevocable. Must use ADS for all real "
        "property placed in service after 12/31/2017.\n"
        "STEP 5: ADS requirement: 30-year for residential rental, 40-year "
        "for nonresidential real property, 20-year for QIP.\n"
        "STEP 6: Trade-off analysis: unlimited interest deduction vs. loss "
        "of bonus depreciation. Model both scenarios.\n"
        "STEP 7: Partnership 163(j) applies at partnership level. Excess "
        "business interest expense (EBIE) allocated to partners.\n"
        "STEP 8: Disallowed interest carries forward indefinitely (not subject "
        "to the 80% NOL limitation)."
    ),
    key_factors=[
        "30% ATI limitation on business interest deduction",
        "Real property trade or business can elect out (irrevocable)",
        "Election out requires ADS for all real property (no bonus depreciation)",
        "Disallowed interest carries forward indefinitely",
        "Small business exception: average gross receipts under $29M",
        "Partnership-level application with EBIE pass-through",
        "ATI computation changed in 2022 (no longer adds back depreciation)",
    ],
    primary_authority=[
        "IRC 163(j) - Business Interest Limitation",
        "IRC 163(j)(7)(B) - Real Property Trade or Business Election",
        "Reg. 1.163(j)-1 through 1.163(j)-11 (Final Regulations 2020)",
        "Rev. Proc. 2020-22 (Late Real Property Election)",
    ],
    burden_holder="Taxpayer must compute limitation and, if electing out, convert to ADS",
    adversary_position=(
        "IRS may argue: (1) ATI computed incorrectly, (2) election was not "
        "properly made, (3) ADS not applied to all qualifying property after "
        "election, (4) partnership EBIE tracking errors."
    ),
    counter_arguments=[
        "Election is irrevocable — cannot undo if circumstances change",
        "ADS extends depreciation periods significantly",
        "Loss of bonus depreciation may exceed interest deduction benefit",
        "Partnership EBIE tracking is complex for multi-tier structures",
        "ATI computation changes in 2022 reduce the limitation amount",
    ],
    resolution_strategy=(
        "Model both scenarios (with and without 163(j) election) before making "
        "irrevocable election. Consider time value of bonus depreciation vs. "
        "current interest deduction. Track EBIE carefully for partnership interests. "
        "Ensure ADS is applied to all qualifying property after election."
    ),
    entity_scope=["individual", "partnership", "llc", "s_corp", "c_corp", "reit"],
    confidence="DEFENSIBLE",
    confidence_stratification="DEFENSIBLE",
    controlling_precedent="Reg. 1.163(j)-1 (2020 Final Regulations)",
    irc_sections=["163(j)", "163(j)(7)(B)"],
    related_doctrines=["bonus_depreciation_168k", "cost_segregation"],
))


# =============================================================================
# 25. PARTNERSHIP BASIS - IRC 754 ELECTION
# =============================================================================

_register(DoctrineBlock(
    topic="partnership_basis_754",
    keywords=[
        "754 election", "step up", "partnership basis", "inside basis",
        "outside basis", "743b adjustment", "734b adjustment",
        "substantial built in loss",
    ],
    conclusion_template=(
        "A Section 754 election allows a partnership to adjust the inside "
        "basis of partnership property upon a transfer of a partnership "
        "interest (Section 743(b)) or a distribution of property (Section "
        "734(b)). For real estate partnerships, this is critical to avoid "
        "phantom income when a partner purchases an interest at a premium "
        "over the partner's share of inside basis."
    ),
    reasoning_framework=(
        "STEP 1: Determine if a 754 election is beneficial — typically when "
        "a partner acquires an interest at a premium (FMV > inside basis).\n"
        "STEP 2: Section 743(b) adjustment: on transfer of a partnership "
        "interest, the transferee partner gets a special basis adjustment "
        "equal to the difference between outside basis and share of inside basis.\n"
        "STEP 3: The 743(b) adjustment is personal to the transferee partner "
        "and affects only that partner's depreciation and gain/loss.\n"
        "STEP 4: Section 734(b) adjustment: on distribution of property, "
        "the partnership adjusts the basis of remaining property.\n"
        "STEP 5: The 754 election is irrevocable once made (applies to all "
        "future transfers and distributions) unless IRS grants revocation.\n"
        "STEP 6: Mandatory basis adjustment (no election needed) if there is "
        "a substantial built-in loss (>$250,000).\n"
        "STEP 7: Allocation of 743(b) adjustment among partnership assets "
        "follows Section 755 rules (ordinary income vs. capital gain property).\n"
        "STEP 8: For real estate, the adjustment typically increases "
        "depreciable basis, providing additional depreciation to the buyer."
    ),
    key_factors=[
        "754 election is irrevocable once made",
        "743(b) adjustment on partnership interest transfer",
        "734(b) adjustment on property distribution",
        "Adjustment is personal to the transferee partner",
        "Allocation under Section 755 between ordinary and capital property",
        "Mandatory adjustment for substantial built-in loss (>$250K)",
        "Critical for real estate partnerships to avoid phantom income",
    ],
    primary_authority=[
        "IRC 754 - Election to Adjust Basis",
        "IRC 743(b) - Adjustment to Basis of Partnership Property (Transfer)",
        "IRC 734(b) - Adjustment to Basis of Partnership Property (Distribution)",
        "IRC 755 - Rules for Allocating Basis Adjustments",
        "Reg. 1.754-1 through 1.755-1",
    ],
    burden_holder="Partnership must properly compute and allocate basis adjustments; election is partnership-level",
    adversary_position=(
        "IRS may argue: (1) basis adjustment incorrectly computed, "
        "(2) allocation under 755 is improper, (3) election not properly "
        "made or filed, (4) substantial built-in loss not addressed."
    ),
    counter_arguments=[
        "Irrevocability means negative adjustments also apply to future transfers",
        "Administrative burden of tracking individual partner adjustments",
        "Complex allocation under 755 for multi-asset partnerships",
        "Interaction with 704(c) creates layered basis tracking",
        "Late election is generally not available (must be on timely filed return)",
    ],
    resolution_strategy=(
        "Make 754 election when partners are acquiring interests at premiums "
        "(common in real estate). Track individual partner basis adjustments "
        "carefully. Use tax software capable of 743(b)/755 computations. "
        "Consider consequences of irrevocability for future transactions."
    ),
    entity_scope=["partnership", "llc"],
    confidence="DEFENSIBLE",
    confidence_stratification="DEFENSIBLE",
    controlling_precedent="Reg. 1.754-1 (Election Procedures)",
    irc_sections=["754", "743(b)", "734(b)", "755"],
    related_doctrines=["contributed_property_704c"],
))


# =============================================================================
# 26. CONTRIBUTED PROPERTY - IRC 704(c)
# =============================================================================

_register(DoctrineBlock(
    topic="contributed_property_704c",
    keywords=[
        "704c", "contributed property", "built-in gain", "built-in loss",
        "traditional method", "remedial method", "curative allocation",
        "partnership contribution",
    ],
    conclusion_template=(
        "IRC 704(c) requires that when property with a built-in gain or loss "
        "is contributed to a partnership, the built-in gain or loss must be "
        "allocated to the contributing partner. Three methods are available: "
        "traditional, traditional with curative allocations, and remedial. "
        "This prevents shifting of pre-contribution gains to non-contributing partners."
    ),
    reasoning_framework=(
        "STEP 1: Identify contributed property with FMV differing from basis.\n"
        "STEP 2: Calculate built-in gain (FMV > basis) or loss (basis > FMV).\n"
        "STEP 3: Select allocation method — traditional is simplest but may "
        "have ceiling rule limitations. Remedial eliminates ceiling rule.\n"
        "STEP 4: Traditional method: allocate tax items to match book items. "
        "Ceiling rule limits tax allocation to total tax item available.\n"
        "STEP 5: Remedial method: creates offsetting tax items to eliminate "
        "ceiling rule distortions. Most complete but most complex.\n"
        "STEP 6: Anti-abuse rules: 704(c)(1)(C) requires built-in loss "
        "limitation — only contributing partner takes the loss.\n"
        "STEP 7: Revaluation events (new partner admission) create reverse "
        "704(c) layers for all existing partners.\n"
        "STEP 8: 704(c) layers persist for the life of the contributed asset."
    ),
    key_factors=[
        "Built-in gain/loss allocated to contributing partner",
        "Three methods: traditional, curative, remedial",
        "Ceiling rule may cause distortions under traditional method",
        "Remedial method eliminates ceiling rule but adds complexity",
        "Built-in loss limitation under 704(c)(1)(C)",
        "Revaluations create reverse 704(c) layers",
        "Layers persist for life of contributed asset",
    ],
    primary_authority=[
        "IRC 704(c) - Contributed Property Allocations",
        "Reg. 1.704-3 - Methods of Allocation",
        "IRC 704(c)(1)(C) - Built-In Loss Limitation",
        "Reg. 1.704-3(d) - Remedial Allocation Method",
    ],
    burden_holder="Partnership must properly apply 704(c) method and allocate items to contributing partner",
    adversary_position=(
        "IRS may argue: (1) improper 704(c) method selected to shift tax, "
        "(2) ceiling rule distortions create unfair results, (3) reverse "
        "704(c) layers not properly maintained on revaluation."
    ),
    counter_arguments=[
        "Ceiling rule under traditional method can shift tax to non-contributing partners",
        "Method selection is binding and cannot be changed without IRS consent",
        "Reverse 704(c) adds significant tracking complexity",
        "Contributed property with multiple components requires layer-by-layer tracking",
        "Disposition of contributed property requires special allocation rules",
    ],
    resolution_strategy=(
        "Select 704(c) method at partnership formation and document in agreement. "
        "Use remedial method for significant built-in gain/loss to avoid ceiling "
        "rule distortions. Maintain detailed records of contribution basis, FMV, "
        "and 704(c) layers."
    ),
    entity_scope=["partnership", "llc"],
    confidence="DEFENSIBLE",
    confidence_stratification="DEFENSIBLE",
    controlling_precedent="Reg. 1.704-3",
    irc_sections=["704(c)", "704(c)(1)(C)"],
    related_doctrines=["partnership_basis_754"],
))


# =============================================================================
# 27. ENVIRONMENTAL REMEDIATION - IRC 198
# =============================================================================

_register(DoctrineBlock(
    topic="environmental_remediation_198",
    keywords=[
        "environmental remediation", "brownfield", "section 198",
        "hazardous substance", "contaminated site", "cleanup costs",
        "targeted area", "superfund",
    ],
    conclusion_template=(
        "IRC 198 allowed a current deduction for environmental remediation "
        "expenditures incurred to clean up hazardous substances at qualified "
        "contaminated sites. This provision expired after December 31, 2011, "
        "but has been periodically extended and may be reinstated. Without "
        "Section 198, remediation costs must be capitalized under general "
        "principles and recovered through depreciation or upon sale."
    ),
    reasoning_framework=(
        "STEP 1: Determine if IRC 198 is currently in effect (check for "
        "retroactive extension — Congress has extended multiple times).\n"
        "STEP 2: If 198 is available: site must be a qualified contaminated "
        "site — hazardous substance released or disposal confirmed.\n"
        "STEP 3: Expenditures must be for cleanup, not acquisition of land.\n"
        "STEP 4: If 198 is NOT available: capitalize remediation costs "
        "under IRC 263 general capitalization rules.\n"
        "STEP 5: Capitalized remediation costs added to land or building basis.\n"
        "STEP 6: If added to building basis — recoverable through MACRS.\n"
        "STEP 7: If added to land basis — recoverable only on sale.\n"
        "STEP 8: Separate from demolition costs under 280B."
    ),
    key_factors=[
        "Section 198 expired 12/31/2011 — check for retroactive extension",
        "If available: current deduction for hazardous substance cleanup",
        "If expired: capitalize under IRC 263",
        "Qualified contaminated site requires EPA/state confirmation",
        "Expenditures must be for actual remediation, not land acquisition",
        "Capitalized costs added to land or building basis",
    ],
    primary_authority=[
        "IRC 198 - Environmental Remediation Costs",
        "Reg. 1.198-1 (when in effect)",
        "IRC 263 - Capital Expenditures (fallback)",
        "Rev. Rul. 94-38 (Soil Remediation Costs)",
    ],
    burden_holder="Taxpayer must prove contamination exists and expenditures are for remediation",
    adversary_position=(
        "IRS may argue: (1) Section 198 is expired, no current deduction, "
        "(2) costs are improvements rather than remediation, (3) site does "
        "not qualify as contaminated under EPA/state standards."
    ),
    counter_arguments=[
        "Expiration of Section 198 forces capitalization (less favorable)",
        "Distinction between remediation and improvement is fact-intensive",
        "EPA certification process can be lengthy and expensive",
        "State environmental laws may differ from federal standards",
        "Rev. Rul. 94-38 provides limited authority for soil remediation as repair",
    ],
    resolution_strategy=(
        "Check current status of Section 198 for the tax year. If available, "
        "obtain EPA/state confirmation of contamination. If expired, analyze "
        "under Rev. Rul. 94-38 and general capitalization rules. Separate "
        "remediation costs from improvement costs."
    ),
    entity_scope=["individual", "partnership", "llc", "s_corp", "c_corp"],
    confidence="AGGRESSIVE",
    confidence_stratification="AGGRESSIVE",
    controlling_precedent="Rev. Rul. 94-38",
    irc_sections=["198", "263"],
    related_doctrines=["demolition_280b"],
    sunset_provision="Section 198 expired 12/31/2011 — may be retroactively extended",
))


# =============================================================================
# 28. REAL ESTATE MORTGAGE CONDUIT - IRC 860A-G
# =============================================================================

_register(DoctrineBlock(
    topic="real_estate_mortgage_conduit_860a",
    keywords=[
        "remic", "mortgage backed security", "real estate mortgage conduit",
        "regular interest", "residual interest", "section 860a",
        "excess inclusion income", "phantom income",
    ],
    conclusion_template=(
        "A Real Estate Mortgage Investment Conduit (REMIC) under IRC 860A-G "
        "is a pass-through entity holding a fixed pool of mortgages that "
        "issues multiple classes of interests (regular and residual). Regular "
        "interests are taxed like debt instruments. Residual interests bear "
        "the 'excess inclusion income' that cannot be offset by NOLs and "
        "creates phantom income issues for holders."
    ),
    reasoning_framework=(
        "STEP 1: REMIC must hold a fixed pool of real estate mortgages.\n"
        "STEP 2: Issues two types of interests: regular (debt-like, predictable "
        "cash flows) and residual (equity-like, bears excess inclusion income).\n"
        "STEP 3: REMIC entity itself is not taxed — income passes through.\n"
        "STEP 4: Regular interest holders report income as OID (original "
        "issue discount) under standard debt rules.\n"
        "STEP 5: Residual interest holders bear excess inclusion income — "
        "taxable even if no cash distribution received (phantom income).\n"
        "STEP 6: Excess inclusion income cannot be offset by NOLs, "
        "deductions, or credits — it is always taxable.\n"
        "STEP 7: Tax-exempt holders of residual interests face UBTI.\n"
        "STEP 8: Prohibited transactions (self-dealing, new mortgages after "
        "startup) result in 100% penalty tax."
    ),
    key_factors=[
        "Fixed pool of real estate mortgages",
        "Regular interests taxed as debt instruments (OID rules)",
        "Residual interests bear excess inclusion income",
        "Excess inclusion income: not offset by NOLs/deductions",
        "Phantom income for residual holders (no cash distribution)",
        "100% penalty tax on prohibited transactions",
        "Tax-exempt holders: excess inclusion = UBTI",
    ],
    primary_authority=[
        "IRC 860A-G - REMIC Provisions",
        "IRC 860E - Excess Inclusion Income",
        "Reg. 1.860A-1 through 1.860G-3",
        "IRC 860F - Prohibited Transactions",
    ],
    burden_holder="REMIC must maintain fixed pool and avoid prohibited transactions",
    adversary_position=(
        "IRS may challenge: (1) qualification as REMIC, (2) improper regular "
        "vs. residual classification, (3) prohibited transaction occurred, "
        "(4) excess inclusion income not properly reported."
    ),
    counter_arguments=[
        "Excess inclusion income creates phantom income for residual holders",
        "Prohibited transaction penalty (100% tax) is severe",
        "REMIC classification is irrevocable",
        "Tax-exempt investors face unexpected UBTI",
        "Complex OID computations for regular interests",
    ],
    resolution_strategy=(
        "Carefully structure REMIC to avoid prohibited transactions. "
        "Ensure residual holders understand excess inclusion income implications. "
        "Avoid placing residual interests with tax-exempt entities. "
        "Maintain proper REMIC election and compliance documentation."
    ),
    entity_scope=["remic", "trust"],
    confidence="DEFENSIBLE",
    confidence_stratification="DEFENSIBLE",
    controlling_precedent="IRC 860A-G (statutory framework)",
    irc_sections=["860A", "860B", "860C", "860D", "860E", "860F", "860G"],
    related_doctrines=["reit_taxation_856"],
))


# =============================================================================
# 29. MIXED-USE PROPERTY ALLOCATION
# =============================================================================

_register(DoctrineBlock(
    topic="mixed_use_property_allocation",
    keywords=[
        "mixed use", "personal use", "rental use", "allocation",
        "vacation home", "280a", "14 day rule", "personal residence rental",
    ],
    conclusion_template=(
        "Mixed-use property (used partly for personal and partly for rental/business "
        "purposes) requires allocation of expenses between personal and rental use "
        "under IRC 280A. The Bolton formula (Tax Court) or IRS approach (365-day "
        "method) determines the deductible rental portion. Properties rented fewer "
        "than 15 days per year are excluded from rental income reporting entirely."
    ),
    reasoning_framework=(
        "STEP 1: Determine personal use days vs. rental use days.\n"
        "STEP 2: If rented fewer than 15 days — no rental income reported, "
        "no rental expenses deducted (14-day rule). Only mortgage interest "
        "and taxes deductible on Schedule A.\n"
        "STEP 3: If personal use exceeds greater of 14 days or 10% of rental "
        "days — property is a 'residence' under 280A, limiting rental "
        "deductions to rental income.\n"
        "STEP 4: Allocate expenses: Bolton method (Tax Court) uses rental "
        "days / total days for interest and taxes; IRS method uses rental "
        "days / 365. Bolton is more favorable to taxpayer.\n"
        "STEP 5: Rental deductions limited to rental income if 280A applies "
        "(no rental loss). Excess carries forward.\n"
        "STEP 6: Order of deduction: (1) allocated interest/taxes, (2) operating "
        "expenses, (3) depreciation.\n"
        "STEP 7: Passive activity rules also apply to rental portion.\n"
        "STEP 8: Section 121 exclusion may apply to personal use portion on sale."
    ),
    key_factors=[
        "14-day rule: no rental income/expense if rented < 15 days",
        "280A limits rental deductions to rental income for personal residences",
        "Bolton formula vs. IRS 365-day method for expense allocation",
        "Order of deductions: interest/taxes, then operating, then depreciation",
        "Excess rental deductions carry forward (not lost)",
        "Personal use = greater of 14 days or 10% of rental days triggers 280A",
        "Section 121 may apply to personal use portion on sale",
    ],
    primary_authority=[
        "IRC 280A - Disallowance of Expenses in Connection with Certain Uses",
        "Bolton v. Commissioner, 694 F.2d 556 (9th Cir. 1982)",
        "Prop. Reg. 1.280A-3 (Allocation Methods)",
        "IRS Publication 527 (Residential Rental Property)",
    ],
    burden_holder="Taxpayer must document personal vs. rental use days and properly allocate expenses",
    adversary_position=(
        "IRS prefers 365-day allocation method which allocates more interest/taxes "
        "to rental (reducing available deductions for other rental expenses). "
        "IRS may challenge personal use day counting."
    ),
    counter_arguments=[
        "Bolton vs. IRS method creates different results — circuit split",
        "Personal use day counting rules are detailed and easy to violate",
        "280A loss limitation traps depreciation deductions",
        "Passive activity rules layer on top of 280A limitations",
        "Short-term rental platforms complicate the analysis",
    ],
    resolution_strategy=(
        "Carefully track personal and rental use days. Limit personal use to "
        "avoid 280A 'residence' classification. Use Bolton method in 9th "
        "Circuit or where favorable. Order deductions to maximize benefit."
    ),
    entity_scope=["individual"],
    confidence="DEFENSIBLE",
    confidence_stratification="DEFENSIBLE",
    controlling_precedent="Bolton v. Commissioner, 694 F.2d 556 (9th Cir. 1982)",
    irc_sections=["280A"],
    related_doctrines=["passive_activity_469", "primary_residence_121"],
))


# =============================================================================
# 30. REAL PROPERTY DEFINITION POST-TCJA
# =============================================================================

_register(DoctrineBlock(
    topic="real_property_definition_1031",
    keywords=[
        "real property", "definition", "1031 real property", "post tcja",
        "inherently permanent", "structural component", "land",
        "distinct asset",
    ],
    conclusion_template=(
        "Post-TCJA, only real property qualifies for 1031 exchanges. The "
        "2020 final regulations (Reg. 1.1031(a)-3) define real property "
        "broadly to include: land, inherently permanent structures, and "
        "structural components. Property incidental to the use of real "
        "property (e.g., parking lot striping machines) may also qualify "
        "if listed in the regulations or meeting the factors test."
    ),
    reasoning_framework=(
        "STEP 1: Determine if the asset is land (always real property).\n"
        "STEP 2: If not land, determine if it is an inherently permanent "
        "structure — a structure permanently affixed to land, including "
        "buildings, permanent outdoor structures, and similar items.\n"
        "STEP 3: Apply the factors test: (1) manner of affixation, "
        "(2) designed for permanent installation, (3) damage on removal, "
        "(4) time and expense to move, (5) nature of the structure.\n"
        "STEP 4: Structural components of inherently permanent structures "
        "also qualify (walls, floors, ceilings, plumbing, HVAC, electrical).\n"
        "STEP 5: State and local law characterization is considered but "
        "not determinative.\n"
        "STEP 6: Intangible interests in real property qualify: fee simple, "
        "life estates, remainders, leasehold interests (30+ years or with "
        "purchase option), easements.\n"
        "STEP 7: Personal property is excluded — no 1031 for equipment, "
        "vehicles, artwork, or other tangible personal property post-TCJA.\n"
        "STEP 8: Transition rule for personal property exchanges if "
        "initiated before 01/01/2018."
    ),
    key_factors=[
        "Real property = land + inherently permanent structures + structural components",
        "Five-factor test for inherent permanence",
        "Intangible real property interests qualify (30+ year leaseholds, easements)",
        "Personal property categorically excluded post-TCJA",
        "State law characterization considered but not determinative",
        "2020 final regulations provide safe harbors and examples",
    ],
    primary_authority=[
        "Reg. 1.1031(a)-3 - Definition of Real Property (2020 Final)",
        "TCJA 2017, Section 13303 (Limitation to Real Property)",
        "IRC 1031(a) - Like-Kind Exchange",
        "T.D. 9935 (2020 Final Regulations)",
    ],
    burden_holder="Taxpayer must demonstrate property qualifies as real property under the regulations",
    adversary_position=(
        "IRS may argue: (1) property is personal property disguised as real, "
        "(2) fails the factors test for inherent permanence, (3) intangible "
        "interest (e.g., short lease) does not qualify."
    ),
    counter_arguments=[
        "Borderline assets require detailed factual analysis",
        "Some fixtures may be personal property under cost segregation but real for 1031",
        "Leasehold interests under 30 years without purchase option may not qualify",
        "State law characterization differences create uncertainty",
        "Pre-TCJA personal property exchange commitments may still qualify",
    ],
    resolution_strategy=(
        "Apply the 2020 final regulations factors test to any questionable "
        "asset before including in a 1031 exchange. Obtain appraisal "
        "supporting real property classification. Document affixation, "
        "permanence, and structural integration."
    ),
    entity_scope=["individual", "partnership", "llc", "s_corp", "c_corp", "trust"],
    confidence="DEFENSIBLE",
    confidence_stratification="DEFENSIBLE",
    controlling_precedent="Reg. 1.1031(a)-3 (2020 Final Regulations)",
    irc_sections=["1031(a)"],
    related_doctrines=["like_kind_exchange_1031"],
    effective_dates="Final regulations effective 01/19/2021",
))


# =============================================================================
# 31. SHORT-TERM RENTAL TAXATION
# =============================================================================

_register(DoctrineBlock(
    topic="short_term_rental_taxation",
    keywords=[
        "short term rental", "airbnb", "vrbo", "vacation rental",
        "average rental period", "7 day rule", "significant personal services",
        "schedule c", "schedule e",
    ],
    conclusion_template=(
        "Short-term rentals (average rental period of 7 days or less) are not "
        "treated as rental activities under Reg. 1.469-1T(e)(3)(ii). This "
        "means they escape the per-se passive rental classification and may "
        "be treated as non-passive if the taxpayer materially participates. "
        "If significant personal services are provided, the activity may be "
        "reported on Schedule C rather than Schedule E."
    ),
    reasoning_framework=(
        "STEP 1: Calculate average period of customer use. If 7 days or less, "
        "the activity is NOT a rental activity for PAL purposes.\n"
        "STEP 2: If average period is 8-30 days AND significant personal "
        "services are provided, also NOT a rental activity.\n"
        "STEP 3: Non-rental classification means material participation tests "
        "apply (7 tests under Reg. 1.469-5T). If met, losses are non-passive.\n"
        "STEP 4: If significant personal services are provided (maid service, "
        "concierge, meals, entertainment), activity may be a service business "
        "on Schedule C, subject to self-employment tax.\n"
        "STEP 5: If no significant personal services, report on Schedule E "
        "as a trade or business.\n"
        "STEP 6: Cost segregation and bonus depreciation available to create "
        "large upfront deductions if activity is non-passive.\n"
        "STEP 7: Section 199A QBI deduction potentially available if trade "
        "or business.\n"
        "STEP 8: State and local STR taxes and regulations must be considered."
    ),
    key_factors=[
        "7-day average rental period removes per-se passive rental classification",
        "8-30 day average with significant personal services also non-rental",
        "Material participation tests determine passive vs. non-passive",
        "Schedule C if significant personal services (self-employment tax)",
        "Schedule E if trade or business without significant personal services",
        "Cost seg + bonus depreciation creates large non-passive deductions",
        "199A QBI deduction may apply",
    ],
    primary_authority=[
        "Reg. 1.469-1T(e)(3)(ii) - Rental Activity Definition",
        "Reg. 1.469-5T - Material Participation Tests",
        "IRC 469 - Passive Activity Limitations",
        "IRC 1402 - Self-Employment Tax",
        "IRS Chief Counsel Memo 201427016 (STR Classification)",
    ],
    burden_holder="Taxpayer must prove average rental period and material participation",
    adversary_position=(
        "IRS may argue: (1) average rental period exceeds 7 days, (2) taxpayer "
        "does not materially participate, (3) significant personal services "
        "trigger self-employment tax, (4) losses are passive despite STR "
        "classification."
    ),
    counter_arguments=[
        "Average rental period calculation methods may be disputed",
        "Property manager hours may not count toward material participation",
        "Self-employment tax exposure if significant personal services",
        "State and local regulations may restrict STR operations",
        "Grouping elections interact with STR classification",
    ],
    resolution_strategy=(
        "Track average rental period carefully — document all stays. Maintain "
        "material participation hour logs. Minimize personal services to avoid "
        "self-employment tax. Combine with cost segregation for maximum "
        "non-passive deductions."
    ),
    entity_scope=["individual", "partnership", "llc", "s_corp"],
    confidence="DEFENSIBLE",
    confidence_stratification="DEFENSIBLE",
    controlling_precedent="Reg. 1.469-1T(e)(3)(ii)",
    irc_sections=["469", "1402"],
    related_doctrines=["passive_activity_469", "cost_segregation", "section_199a_real_estate"],
))


# =============================================================================
# 32. SECTION 1060 - ASSET ACQUISITION RULES
# =============================================================================

_register(DoctrineBlock(
    topic="asset_acquisition_1060",
    keywords=[
        "1060", "asset acquisition", "purchase price allocation",
        "residual method", "class allocation", "going concern",
        "form 8594", "applicable asset acquisition",
    ],
    conclusion_template=(
        "IRC 1060 requires that when a trade or business (including real estate "
        "operations) is acquired, the purchase price must be allocated among "
        "the acquired assets using the residual method under IRC 338(b)(5). "
        "Assets are allocated across seven classes, with real property typically "
        "falling in Class V. Both buyer and seller must report consistent "
        "allocations on Form 8594."
    ),
    reasoning_framework=(
        "STEP 1: Determine if the acquisition is an applicable asset acquisition "
        "(group of assets constituting a trade or business).\n"
        "STEP 2: Apply residual method — allocate purchase price to assets "
        "in order of seven classes until fully absorbed.\n"
        "STEP 3: Class I: cash and equivalents. Class II: actively traded "
        "securities. Class III: accounts receivable, mortgages, deposits. "
        "Class IV: inventory. Class V: all other tangible and intangible "
        "assets (includes real property). Class VI: IRC 197 intangibles "
        "(except goodwill). Class VII: goodwill and going concern value.\n"
        "STEP 4: Within Class V, allocate to real property based on appraised "
        "FMV. This determines depreciable basis.\n"
        "STEP 5: Seller and buyer must file Form 8594 with consistent allocations.\n"
        "STEP 6: Buyer prefers allocation to shorter-lived assets (depreciation). "
        "Seller prefers allocation to capital gain assets.\n"
        "STEP 7: Arm's length allocation in purchase agreement is generally "
        "binding on both parties unless clearly unreasonable.\n"
        "STEP 8: Obtain appraisals supporting allocation — IRS will challenge "
        "aggressive allocations."
    ),
    key_factors=[
        "Residual method across seven asset classes",
        "Real property in Class V — allocation determines depreciable basis",
        "Form 8594 required for both buyer and seller (consistent)",
        "Contractual allocation generally binding on both parties",
        "Buyer prefers shorter-lived assets; seller prefers capital gain",
        "Independent appraisal supports defensibility",
    ],
    primary_authority=[
        "IRC 1060 - Special Allocation Rules for Applicable Asset Acquisitions",
        "IRC 338(b)(5) - Residual Method",
        "Reg. 1.1060-1",
        "Form 8594 Instructions",
    ],
    burden_holder="Both buyer and seller must justify allocation — IRS can challenge either party",
    adversary_position=(
        "IRS may argue: (1) allocation does not reflect FMV of assets, "
        "(2) parties colluded on non-arm's-length allocation, (3) insufficient "
        "appraisal support, (4) goodwill undervalued."
    ),
    counter_arguments=[
        "Buyer and seller have adverse interests in allocation (natural check)",
        "Appraisal subjectivity creates audit risk on both sides",
        "Goodwill vs. other intangibles allocation is fact-intensive",
        "Real property vs. personal property allocation affects depreciation",
        "Related party acquisitions face heightened scrutiny",
    ],
    resolution_strategy=(
        "Negotiate allocation in purchase agreement with arm's-length positions. "
        "Obtain independent appraisal supporting allocation. File Form 8594 "
        "with consistent allocations. Consider cost segregation immediately "
        "after acquisition."
    ),
    entity_scope=["individual", "partnership", "llc", "s_corp", "c_corp"],
    confidence="DEFENSIBLE",
    confidence_stratification="DEFENSIBLE",
    controlling_precedent="Reg. 1.1060-1",
    irc_sections=["1060", "338(b)(5)", "197"],
    related_doctrines=["cost_segregation"],
))


# =============================================================================
# 33. RELATED PARTY EXCHANGE RULES - IRC 1031(f)
# =============================================================================

_register(DoctrineBlock(
    topic="related_party_exchange_1031f",
    keywords=[
        "related party", "1031(f)", "related party exchange",
        "2 year hold", "related person", "constructive ownership",
        "related party disposition",
    ],
    conclusion_template=(
        "IRC 1031(f) provides that if a like-kind exchange occurs between "
        "related persons (as defined by IRC 267(b) or 707(b)(1)), and either "
        "party disposes of the property within 2 years of the exchange, "
        "the deferred gain is recognized. This anti-abuse rule prevents "
        "related parties from using exchanges to cash out at preferential "
        "rates while deferring gain."
    ),
    reasoning_framework=(
        "STEP 1: Determine if parties are related under IRC 267(b) or 707(b)(1).\n"
        "STEP 2: Related persons include: family members, >50% owned entities, "
        "trusts and beneficiaries, corporate stockholders >50%.\n"
        "STEP 3: If exchange is between related persons, 2-year holding "
        "requirement applies to both relinquished and replacement property.\n"
        "STEP 4: If either party disposes within 2 years, gain recognition "
        "is triggered for the original exchange.\n"
        "STEP 5: Exceptions: dispositions due to death, involuntary conversion, "
        "and exchanges where IRS determines no tax avoidance purpose.\n"
        "STEP 6: Constructive ownership rules under 267(c) apply — "
        "attribution through entities, family members.\n"
        "STEP 7: The 2-year period is tolled during any period when risk "
        "of loss is substantially diminished (puts, shorts, etc.).\n"
        "STEP 8: Indirect exchanges (through intermediary) with related "
        "parties also trigger 1031(f)."
    ),
    key_factors=[
        "Related persons: IRC 267(b) and 707(b)(1) definitions",
        "2-year holding period after exchange for both parties",
        "Disposition by either party within 2 years triggers gain",
        "Constructive ownership rules apply",
        "Exceptions: death, involuntary conversion, non-tax-avoidance",
        "Period tolled when risk of loss substantially diminished",
        "Applies to direct and indirect exchanges",
    ],
    primary_authority=[
        "IRC 1031(f) - Related Party Exchanges",
        "IRC 267(b) - Related Person Definition",
        "IRC 707(b)(1) - Related Partner/Partnership Definition",
        "Reg. 1.1031(k)-1(b) (general exchange rules)",
        "Teruya Brothers Ltd. v. Commissioner, 124 T.C. 45 (2005)",
    ],
    burden_holder="IRS bears burden of proving tax avoidance purpose, but taxpayer must demonstrate compliance",
    adversary_position=(
        "IRS will assert: (1) related party relationship exists through "
        "constructive ownership, (2) disposition within 2 years occurred, "
        "(3) exchange was structured to facilitate basis shifting."
    ),
    counter_arguments=[
        "Constructive ownership can create unexpected related party status",
        "2-year rule applies even to unplanned dispositions (foreclosure)",
        "Basis shifting between related parties is primary IRS concern",
        "Indirect exchanges through QI do not avoid related party rules",
        "Risk diminishment tolling is broadly interpreted by IRS",
    ],
    resolution_strategy=(
        "Check related party status (including constructive ownership) before "
        "any 1031 exchange. If related parties are involved, ensure both "
        "parties hold for at least 2 years. Document non-tax-avoidance "
        "business purpose for the exchange."
    ),
    entity_scope=["individual", "partnership", "llc", "s_corp", "c_corp", "trust"],
    confidence="DEFENSIBLE",
    confidence_stratification="DEFENSIBLE",
    controlling_precedent="Teruya Brothers Ltd. v. Commissioner, 124 T.C. 45 (2005)",
    irc_sections=["1031(f)", "267(b)", "707(b)(1)"],
    related_doctrines=["like_kind_exchange_1031"],
))


# =============================================================================
# 34. NET INVESTMENT INCOME TAX - IRC 1411
# =============================================================================

_register(DoctrineBlock(
    topic="net_investment_income_tax_1411",
    keywords=[
        "niit", "net investment income", "3.8 percent", "1411",
        "additional tax", "rental income niit", "gain on sale niit",
        "agi threshold",
    ],
    conclusion_template=(
        "IRC 1411 imposes an additional 3.8% tax on net investment income "
        "for taxpayers with modified AGI exceeding $200,000 (single) or "
        "$250,000 (MFJ). Real estate rental income and gain on sale of "
        "investment property are generally included in NII. However, income "
        "from a real property trade or business in which the taxpayer "
        "materially participates is excluded from NII."
    ),
    reasoning_framework=(
        "STEP 1: Determine if modified AGI exceeds threshold ($200K single, "
        "$250K MFJ, $125K MFS).\n"
        "STEP 2: NII includes: rental income, interest, dividends, capital "
        "gains, royalties, passive activity income.\n"
        "STEP 3: NII excludes: income from active trade or business where "
        "taxpayer materially participates (and not trading financial instruments).\n"
        "STEP 4: For rental real estate: passive rental income is NII. "
        "But if RE professional + material participation, rental income "
        "may be excluded from NII (Reg. 1.1411-4(g)).\n"
        "STEP 5: Gain on sale: passive activity disposition gain is NII. "
        "Active trade or business disposition gain may be excluded.\n"
        "STEP 6: The 3.8% applies to the LESSER of: NII or excess of "
        "MAGI over the threshold.\n"
        "STEP 7: Grouping elections for PAL purposes also apply for NIIT.\n"
        "STEP 8: Planning: managing AGI around thresholds, timing gains, "
        "qualifying as RE professional."
    ),
    key_factors=[
        "3.8% additional tax on net investment income",
        "Thresholds: $200K single, $250K MFJ, $125K MFS (not indexed)",
        "Rental income generally included in NII",
        "RE professional with material participation may exclude rental income",
        "Gain on sale of investment/passive property is NII",
        "Tax applies to lesser of NII or MAGI excess over threshold",
        "Thresholds are NOT inflation-indexed",
    ],
    primary_authority=[
        "IRC 1411 - Net Investment Income Tax",
        "Reg. 1.1411-1 through 1.1411-10 (Final Regulations 2013)",
        "Reg. 1.1411-4(g) - Exception for Active Trade or Business Income",
        "ACA 2010 (Affordable Care Act — enacting provision)",
    ],
    burden_holder="Taxpayer must demonstrate material participation for NII exclusion",
    adversary_position=(
        "IRS may argue: (1) rental income is passive NII despite RE professional "
        "claim, (2) gain on sale is NII because activity was passive, "
        "(3) grouping election improperly used to avoid NIIT."
    ),
    counter_arguments=[
        "Non-indexed thresholds capture more taxpayers over time",
        "RE professional exclusion from NIIT requires both 469(c)(7) AND material participation",
        "Grouping elections create complexity for both PAL and NIIT",
        "Installment sale gain recognition triggers NIIT in payout years",
        "Short-term rental income classification affects NIIT treatment",
    ],
    resolution_strategy=(
        "Qualify as RE professional with material participation to exclude "
        "rental income from NII. Time capital gains to manage MAGI around "
        "thresholds. Consider installment sales to spread NII over years. "
        "Evaluate grouping elections for both PAL and NIIT impact."
    ),
    entity_scope=["individual", "trust"],
    confidence="DEFENSIBLE",
    confidence_stratification="DEFENSIBLE",
    controlling_precedent="Reg. 1.1411-4(g)",
    irc_sections=["1411"],
    related_doctrines=["passive_activity_469", "real_estate_professional_status", "installment_sale_453"],
))


# =============================================================================
# 35. QUALIFIED OPPORTUNITY ZONE BUSINESS PROPERTY
# =============================================================================

_register(DoctrineBlock(
    topic="qozb_substantial_improvement",
    keywords=[
        "substantial improvement", "qozb", "qualified opportunity zone business",
        "double basis", "30 month", "original use", "working capital safe harbor",
    ],
    conclusion_template=(
        "For existing structures acquired in an Opportunity Zone, the QOF or "
        "QOZB must substantially improve the property by doubling the adjusted "
        "basis of the building (excluding land) within 30 months of acquisition. "
        "Alternatively, property with 'original use' commencing with the QOF "
        "does not require substantial improvement. A working capital safe harbor "
        "allows 31 months to deploy capital."
    ),
    reasoning_framework=(
        "STEP 1: Determine if the property has original use commencing with "
        "the QOF/QOZB. If yes, no substantial improvement needed.\n"
        "STEP 2: If existing property, must substantially improve: additions "
        "to adjusted basis of building must exceed adjusted basis at acquisition.\n"
        "STEP 3: Land is excluded from the substantial improvement test — "
        "only building basis must be doubled.\n"
        "STEP 4: 30-month improvement period begins on date of acquisition.\n"
        "STEP 5: Working capital safe harbor: 31 months to deploy capital "
        "if QOZB has a written plan, written schedule, and assets held "
        "pursuant to the plan.\n"
        "STEP 6: Original use = property first placed in service in the zone. "
        "Vacant property may qualify as original use under certain conditions.\n"
        "STEP 7: 70% tangible property test: 70% of tangible property owned "
        "or leased by QOZB must be QOZP.\n"
        "STEP 8: Nonqualified financial property (stocks, debt, options) "
        "cannot exceed 5% of QOZB assets."
    ),
    key_factors=[
        "Substantial improvement: double building basis within 30 months",
        "Land excluded from substantial improvement test",
        "Original use property: no improvement required",
        "Working capital safe harbor: 31 months with written plan",
        "70% tangible property in zone requirement",
        "5% limit on nonqualified financial property",
        "Vacant property may qualify as original use",
    ],
    primary_authority=[
        "IRC 1400Z-2(d)(2)(D) - Substantial Improvement",
        "Reg. 1.1400Z2(d)-2 - QOZB Requirements",
        "Reg. 1.1400Z2(d)-1(c)(8) - Working Capital Safe Harbor",
        "IRS FAQ on Opportunity Zones (Substantial Improvement)",
    ],
    burden_holder="QOF/QOZB must demonstrate compliance with improvement test or original use",
    adversary_position=(
        "IRS may argue: (1) improvement did not double basis within 30 months, "
        "(2) land was improperly excluded, (3) working capital safe harbor "
        "requirements not met, (4) property does not have original use."
    ),
    counter_arguments=[
        "Doubling basis requires significant capital for high-basis acquisitions",
        "30-month timeline creates construction risk",
        "Working capital safe harbor requires detailed written plans",
        "Original use determination for vacant property is factual",
        "70% tangible property test must be met at each testing date",
    ],
    resolution_strategy=(
        "Plan improvements before acquisition to ensure doubling is feasible "
        "within 30 months. Separate land from building basis in acquisition "
        "allocation. Document working capital plan if funds are not immediately "
        "deployed. Verify original use for new construction."
    ),
    entity_scope=["partnership", "llc", "c_corp"],
    confidence="DEFENSIBLE",
    confidence_stratification="DEFENSIBLE",
    controlling_precedent="Reg. 1.1400Z2(d)-2",
    irc_sections=["1400Z-2(d)"],
    related_doctrines=["opportunity_zone_investment"],
))


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def get_all_doctrines() -> Dict[str, DoctrineBlock]:
    """Return all registered doctrine blocks."""
    return dict(DOCTRINE_BLOCKS)


def get_doctrine(topic: str) -> Optional[DoctrineBlock]:
    """Get a specific doctrine block by topic."""
    return DOCTRINE_BLOCKS.get(topic)


def get_doctrine_topics() -> List[str]:
    """Return list of all doctrine topics."""
    return list(DOCTRINE_BLOCKS.keys())


def search_doctrines_by_keyword(keyword: str) -> List[DoctrineBlock]:
    """Search doctrines by keyword match."""
    keyword_lower = keyword.lower()
    results = []
    for block in DOCTRINE_BLOCKS.values():
        if any(keyword_lower in kw.lower() for kw in block.keywords):
            results.append(block)
        elif keyword_lower in block.topic.lower():
            results.append(block)
        elif keyword_lower in block.conclusion_template.lower():
            results.append(block)
    return results


def get_doctrines_by_irc_section(section: str) -> List[DoctrineBlock]:
    """Find all doctrines covering a specific IRC section."""
    section_clean = section.replace("IRC ", "").replace("Section ", "").strip()
    results = []
    for block in DOCTRINE_BLOCKS.values():
        for irc in block.irc_sections:
            if section_clean in irc:
                results.append(block)
                break
    return results


def get_doctrines_by_confidence(confidence: str) -> List[DoctrineBlock]:
    """Get all doctrines at a specific confidence level."""
    return [b for b in DOCTRINE_BLOCKS.values() if b.confidence == confidence]


def get_doctrine_stats() -> Dict[str, int]:
    """Return statistics about the doctrine library."""
    confidences = {}
    for block in DOCTRINE_BLOCKS.values():
        confidences[block.confidence] = confidences.get(block.confidence, 0) + 1
    return {
        "total_doctrines": len(DOCTRINE_BLOCKS),
        "by_confidence": confidences,
        "total_irc_sections": len(set(
            s for b in DOCTRINE_BLOCKS.values() for s in b.irc_sections
        )),
    }
