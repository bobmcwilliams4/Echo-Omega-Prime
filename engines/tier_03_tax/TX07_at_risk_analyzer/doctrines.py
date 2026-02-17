"""
IRC §465 At-Risk Limitation Doctrine Cache
50+ pre-compiled expert reasoning blocks covering at-risk analysis domains
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum


class ConfidenceStratification(str, Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"


class EntityScope(str, Enum):
    INDIVIDUAL = "INDIVIDUAL"
    PARTNERSHIP = "PARTNERSHIP"
    S_CORP = "S_CORP"
    C_CORP = "C_CORP"
    TRUST_ESTATE = "TRUST_ESTATE"
    LLC = "LLC"
    ALL = "ALL"


@dataclass
class DoctrineBlock:
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
    entity_scope: EntityScope
    confidence: ConfidenceStratification
    controlling_precedent: Optional[str] = None


# ═══════════════════════════════════════════════════════════════════════════
# AT-RISK COMPUTATION DOCTRINES
# ═══════════════════════════════════════════════════════════════════════════

AT_RISK_BASIC_COMPUTATION = DoctrineBlock(
    topic="at_risk_basic_computation",
    keywords=["amount at risk", "§465(b)", "computation", "money contributed", "adjusted basis"],
    conclusion_template="""
    The taxpayer's amount at risk equals: (1) cash contributed, (2) adjusted basis of property
    contributed (not FMV), and (3) amounts borrowed for the activity IF the taxpayer is personally
    liable OR has pledged property (other than property used in the activity) as security. IRC §465(b)(1)-(2).
    """,
    reasoning_framework="""
    IRC §465(a) limits loss deductions to the amount the taxpayer has "at risk" in the activity.
    The at-risk amount is NOT static—it fluctuates annually based on contributions, distributions,
    income, and losses.

    COMPUTATION MECHANICS:
    1. Start with beginning-of-year at-risk amount (or zero for new activities)
    2. ADD: Cash contributions during the year
    3. ADD: Adjusted basis (NOT FMV) of property contributed
    4. ADD: Taxpayer's share of activity income (increases at-risk amount)
    5. ADD: Increases in qualified recourse debt (personally liable)
    6. ADD: Increases in qualified nonrecourse financing (§465(b)(6) real estate exception)
    7. SUBTRACT: Cash distributions received
    8. SUBTRACT: Taxpayer's share of activity losses (to extent of at-risk amount)
    9. SUBTRACT: Decreases in debt allocable to taxpayer
    10. End-of-year at-risk amount = limit for current year loss deduction

    CRITICAL RULE: Basis ≠ At-Risk Amount
    - Taxpayer may have $100K tax basis but only $20K at risk
    - Example: $100K FMV property with $80K non-recourse debt = $20K at risk
    - Loss deduction limited to $20K even though basis supports $100K

    FMV TRAP:
    Adjusted basis of contributed property controls, NOT fair market value.
    If taxpayer contributes property with $10K basis and $100K FMV, only $10K increases at-risk amount.
    IRS frequently challenges inflated FMV claims in syndicated transactions.

    TRACKING REQUIREMENT:
    Taxpayer must maintain annual at-risk computation schedule.
    Failure to track = inability to prove at-risk amount = disallowed losses.
    Form 6198 is the IRS reporting mechanism.
    """,
    key_factors=[
        "Cash contributions (direct evidence: bank records, wire transfers)",
        "Adjusted basis of property contributed (NOT FMV)",
        "Personal liability for debt (guaranteed by taxpayer personally)",
        "Property pledged as security (excluding activity property itself)",
        "Annual reconciliation of at-risk amount",
        "Income increases at-risk amount dollar-for-dollar",
        "Distributions decrease at-risk amount",
        "Non-recourse debt does NOT increase at-risk (subject to §465(b)(6) exception)"
    ],
    primary_authority=[
        "IRC §465(a) - Loss limitation to at-risk amount",
        "IRC §465(b)(1) - Money and adjusted basis of property",
        "IRC §465(b)(2) - Borrowed amounts",
        "Treas. Reg. §1.465-20 - Amounts at risk in subsequent years",
        "Treas. Reg. §1.465-22 - Amounts borrowed",
        "Form 6198 Instructions - At-risk computation methodology"
    ],
    burden_holder="Taxpayer bears burden to prove at-risk amount",
    adversary_position="""
    IRS argues:
    1. Taxpayer failed to maintain contemporaneous at-risk records
    2. Property contribution valued at FMV rather than adjusted basis
    3. Debt is non-recourse despite taxpayer's characterization
    4. Guarantees are illusory or not commercially reasonable
    5. Related party debt does not qualify under §465(b)(3) exception
    """,
    counter_arguments=[
        "Form 6198 filed with return demonstrates tracking and contemporaneous computation",
        "Property basis substantiated by prior tax returns, purchase agreements, depreciation schedules",
        "Loan documents explicitly state personal liability; guarantee is enforceable",
        "Commercial reasonableness evidenced by arms-length terms, market interest rate, third-party lender",
        "Related party debt meets §465(b)(3) exception tests (net worth, equity investment)"
    ],
    resolution_strategy="""
    DOCUMENTATION PROTOCOL:
    1. Maintain annual Form 6198 with supporting schedules
    2. Retain all contribution records (cash receipts, property basis documentation)
    3. Loan agreements with highlighted personal liability provisions
    4. Annual reconciliation tying to partnership K-1 or S-corp Schedule K
    5. If related party debt, prepare §465(b)(3) qualification memo

    AUDIT DEFENSE:
    - Provide multi-year at-risk schedule showing year-over-year changes
    - Demonstrate basis vs. at-risk distinction understanding
    - Show income increasing at-risk amount (proves comprehension of mechanics)
    - If debt disputed, obtain lender certification of recourse nature

    PENALTY AVOIDANCE:
    Substantial underpayment penalties apply if at-risk limitations ignored.
    Reasonable cause defense requires: (1) good faith attempt to comply, (2) contemporaneous records,
    (3) professional advice (document tax advisor's involvement).
    """,
    entity_scope=EntityScope.ALL,
    confidence=ConfidenceStratification.DEFENSIBLE,
    controlling_precedent="Treas. Reg. §1.465-20 (comprehensive at-risk computation rules)"
)


NON_RECOURSE_DEBT_EXCLUSION = DoctrineBlock(
    topic="non_recourse_debt_exclusion",
    keywords=["non-recourse debt", "§465(b)(2)", "exclusion", "personal liability", "no at-risk increase"],
    conclusion_template="""
    Non-recourse debt does NOT increase the taxpayer's at-risk amount under IRC §465(b)(2) because
    the taxpayer is not personally liable beyond the property pledged. The lender's sole recourse
    is to the activity property. Exception: §465(b)(6) qualified nonrecourse financing for real estate.
    """,
    reasoning_framework="""
    RECOURSE vs. NON-RECOURSE (determinative distinction):

    RECOURSE DEBT (increases at-risk):
    - Taxpayer is personally liable
    - Lender can pursue taxpayer's other assets if activity property insufficient
    - Taxpayer's personal creditworthiness matters to lender
    - Example: Personal guarantee on business loan, lender can garnish wages/bank accounts

    NON-RECOURSE DEBT (does NOT increase at-risk, subject to exception):
    - Lender's only recourse is to foreclose on activity property
    - Taxpayer has no personal liability
    - Lender relies solely on property value, not borrower creditworthiness
    - Example: Purchase-money mortgage on rental property with no personal guarantee

    WHY EXCLUSION EXISTS (Congressional intent):
    Congress enacted §465 in 1976 to combat tax shelter abuses where investors claimed large
    losses from leveraged investments with no real economic risk. If non-recourse debt counted
    as at-risk, taxpayers could deduct losses on money they never truly borrowed (no personal obligation).

    TESTING FOR RECOURSE NATURE:
    1. Review loan documents: Does taxpayer sign personal guarantee?
    2. State law analysis: Is this a "purchase-money" loan (typically non-recourse in some states)?
    3. Lender's rights: Can lender sue borrower personally or only foreclose?
    4. Deficiency judgment: If property sold for less than debt, can lender pursue borrower?

    SUBSTANCE OVER FORM:
    IRS will recharacterize "recourse" debt as non-recourse if:
    - Guarantee is illusory (guarantor has no assets, shell entity)
    - Guarantee is not commercially reasonable (e.g., related party with net worth less than debt)
    - Stop-loss arrangement limits taxpayer's risk
    - Indemnification agreement protects taxpayer from loss

    IRC §465(b)(4) ANTI-ABUSE RULE:
    If taxpayer pledges property (other than activity property) as security for non-recourse debt,
    the at-risk amount is limited to the net FMV of the pledged property.
    Example: Taxpayer pledges stocks worth $50K as collateral for $200K non-recourse loan.
    At-risk amount = $50K (FMV of stocks), not $200K (loan amount).
    """,
    key_factors=[
        "Personal liability clause in loan documents (yes = recourse, no = non-recourse)",
        "Deficiency judgment rights under state law",
        "Lender's underwriting focus (borrower creditworthiness vs. property value)",
        "Existence of personal guarantee (substantive, not sham)",
        "Related party lender (heightened scrutiny for non-recourse characterization)",
        "Stop-loss or indemnification arrangements (convert recourse to non-recourse)",
        "Pledged collateral other than activity property (§465(b)(4) limit)"
    ],
    primary_authority=[
        "IRC §465(b)(2) - Borrowed amounts at risk only if personal liability",
        "IRC §465(b)(3) - Personal liability exclusion for certain related parties",
        "IRC §465(b)(4) - Property pledged as security",
        "Treas. Reg. §1.465-6 - Nonrecourse financing",
        "Melvin v. Commissioner, 88 T.C. 63 (1987) - Substance over form in guarantee analysis",
        "Emershaw v. Commissioner, 949 F.2d 841 (6th Cir. 1991) - Illusory guarantees"
    ],
    burden_holder="Taxpayer must prove debt is recourse (personal liability exists)",
    adversary_position="""
    IRS challenges recourse characterization:
    1. Loan documents lack explicit personal liability language
    2. State law treats purchase-money debt as non-recourse by default
    3. Guarantee is by shell entity with no net worth (illusory)
    4. Related party lender agreed not to pursue personal liability (side agreement)
    5. Indemnification or hold-harmless agreement negates personal liability
    6. Stop-loss arrangement caps taxpayer's maximum loss
    """,
    counter_arguments=[
        "Loan agreement explicitly states 'Borrower is personally liable for all amounts'",
        "State law allows deficiency judgments on this type of debt (cite statute)",
        "Guarantor has substantial net worth (financial statements show $X assets)",
        "Arms-length lender (institutional bank) would not lend without real recourse",
        "No side agreements; all terms contained in recorded documents",
        "Taxpayer has history of honoring personal guarantees (prior loan repayments)"
    ],
    resolution_strategy="""
    DOCUMENTATION CHECKLIST:
    □ Signed loan agreement with personal liability provision highlighted
    □ Personal guarantee document (if separate from loan agreement)
    □ Guarantor financial statements (if third party guarantor)
    □ State law memo re: deficiency judgment rights
    □ Lender correspondence confirming recourse nature
    □ No side agreements or oral modifications

    If debt is CLEARLY non-recourse:
    - Do not attempt to include in at-risk amount (audit trap)
    - Check for §465(b)(6) qualified nonrecourse financing exception (real estate only)
    - Taxpayer's basis may still include non-recourse debt, but at-risk does not
    - Loss deduction deferred until at-risk amount increases (via income or additional capital)

    LITIGATION STRATEGY:
    Courts apply substance-over-form analysis. Focus on:
    1. Economic reality: Is taxpayer truly at risk if debt defaults?
    2. Commercial reasonableness: Would unrelated lender make this loan?
    3. Guarantor creditworthiness: Can guarantor actually pay if called upon?
    4. No undisclosed agreements limiting liability
    """,
    entity_scope=EntityScope.ALL,
    confidence=ConfidenceStratification.DEFENSIBLE,
    controlling_precedent="IRC §465(b)(2); Treas. Reg. §1.465-6(a)"
)


QUALIFIED_NONRECOURSE_FINANCING = DoctrineBlock(
    topic="qualified_nonrecourse_financing",
    keywords=["qualified nonrecourse financing", "§465(b)(6)", "real property", "real estate exception", "commercial lender"],
    conclusion_template="""
    IRC §465(b)(6) provides an exception to the non-recourse debt exclusion for QUALIFIED nonrecourse
    financing secured by real property used in the activity. Requirements: (1) activity holds real property,
    (2) financing borrowed for use in activity, (3) lender is unrelated and regularly engaged in lending,
    (4) no personal liability, (5) borrowed from qualified person or government entity.
    """,
    reasoning_framework="""
    STATUTORY EXCEPTION (§465(b)(6)):
    Congress created a carve-out for real estate activities to allow non-recourse debt to increase
    at-risk amounts, recognizing that real estate financing is traditionally non-recourse.

    FIVE REQUIREMENTS (all must be met):

    1. REAL PROPERTY ACTIVITY:
        - Activity must involve holding real property (not personal property)
        - Real property = land, buildings, improvements
        - Mixed-use property: Allocate between real and personal property
        - Example: Apartment building (real property) with appliances (personal property)

    2. FINANCING SECURED BY REAL PROPERTY:
        - Mortgage or deed of trust on the real property
        - Property must be used in the activity (not unrelated property)
        - Cross-collateralization issues if multiple properties

    3. NO PERSONAL LIABILITY:
        - Borrower is NOT personally liable for the debt
        - Lender's sole recourse is to foreclose on the property
        - If personal guarantee exists, debt is recourse (not qualified nonrecourse)

    4. BORROWED FOR USE IN ACTIVITY:
        - Loan proceeds used to acquire, construct, or improve the real property
        - Refinancing qualifies if proceeds used to pay off qualifying debt
        - Cash-out refinancing: Only portion allocable to property qualifies

    5. QUALIFIED LENDER (IRC §49(a)(1)(D)(iv)):
        - Federal, state, or local government
        - Bank, savings & loan, credit union (regulated financial institution)
        - Insurance company, pension plan
        - Person actively and regularly engaged in lending (not related party)

        DISQUALIFIED LENDERS:
        - Seller of the property (seller financing does NOT qualify)
        - Related party under §465(b)(3)(C) (family, controlled entities)
        - Person receiving fee for investment (promoter/syndicator)

    SELLER FINANCING TRAP:
    Most common disqualification: Property seller provides financing.
    Even if non-recourse debt from commercial terms, seller is not a "qualified person."
    Result: Debt does NOT increase at-risk amount.

    REFINANCING ANALYSIS:
    Original loan from qualified lender → qualifies
    Refinance with another qualified lender → qualifies (up to original loan amount)
    Cash-out refinance → excess above original debt does NOT qualify unless used for property

    REAL ESTATE PROFESSIONAL DISTINCTION:
    §465(b)(6) exception is SEPARATE from §469(c)(7) real estate professional rules.
    Taxpayer can have qualified nonrecourse financing without being a real estate professional.
    However, both rules often apply together in rental real estate analysis.
    """,
    key_factors=[
        "Activity holds real property (land/buildings, not equipment/inventory)",
        "Debt secured by mortgage on the activity's real property",
        "No personal liability or guarantee (true non-recourse)",
        "Loan proceeds used to acquire/construct/improve the property",
        "Lender is bank, government, insurance company, or qualified commercial lender",
        "Lender is NOT the property seller",
        "Lender is NOT related to borrower under §465(b)(3)(C)",
        "Lender is NOT receiving fees for investment promotion"
    ],
    primary_authority=[
        "IRC §465(b)(6) - Qualified nonrecourse financing exception",
        "IRC §49(a)(1)(D)(iv) - Definition of qualified person",
        "Treas. Reg. §1.465-27 - Qualified nonrecourse financing rules",
        "Prop. Reg. §1.465-27(b)(4) - Seller financing disqualification",
        "IRS Pub. 925 - Passive Activity and At-Risk Rules (qualified nonrecourse guidance)"
    ],
    burden_holder="Taxpayer must prove financing qualifies under §465(b)(6)",
    adversary_position="""
    IRS challenges qualified nonrecourse status:
    1. Lender is the property seller (seller financing does not qualify)
    2. Lender is related party (family member, controlled entity)
    3. Lender not regularly engaged in lending (one-time lender, friend/family)
    4. Loan proceeds not used for property acquisition/improvement (cash-out refinance for personal use)
    5. Personal guarantee exists (converts to recourse debt)
    6. Property is personal property, not real property (equipment lease, aircraft)
    7. Lender receiving promotional fees (syndicator self-lending)
    """,
    counter_arguments=[
        "Lender is federally chartered bank (Wells Fargo, Chase) - clearly qualified",
        "Loan documents show no personal liability (mortgage is sole recourse)",
        "HUD-1 settlement statement shows proceeds used 100% for property purchase",
        "Lender has lending license, active loan portfolio (commercial lender test)",
        "Property is land + building (real property per state law)",
        "Refinancing paid off original acquisition debt (same property use)",
        "No relationship between borrower and lender (unrelated parties)"
    ],
    resolution_strategy="""
    QUALIFICATION CHECKLIST:
    □ Obtain lender qualification letter (states lender is qualified person under §49)
    □ Mortgage document showing non-recourse nature (no personal guarantee page)
    □ HUD-1 or closing statement proving loan proceeds used for property
    □ Title report showing property is real property (land + improvements)
    □ Lender's lending license or charter (bank/insurance company)
    □ Organizational chart showing no related party relationship
    □ If refinancing, tracing of proceeds to original acquisition debt

    COMMON FIXES:
    - Seller financing → refinance with commercial bank within 90 days (debt substitution)
    - Related party lender → pay off and replace with arms-length lender
    - Cash-out refi → use excess proceeds for property improvements to qualify
    - Personal property → separate allocations (only real property portion qualifies)

    PLANNING OPPORTUNITY:
    Structure acquisition with qualified nonrecourse financing to maximize at-risk amount
    without personal liability. Best of both worlds: leverage + loss deductions.
    Commonly used in: rental real estate, commercial buildings, land development.

    INTERACTION WITH §469:
    Even if at-risk requirements met, passive activity loss rules (§469) may still limit deductions.
    Real estate professionals (§469(c)(7)) can avoid passive loss limits but must still satisfy at-risk rules.
    """,
    entity_scope=EntityScope.ALL,
    confidence=ConfidenceStratification.DEFENSIBLE,
    controlling_precedent="IRC §465(b)(6); Treas. Reg. §1.465-27"
)


AGGREGATION_RULES = DoctrineBlock(
    topic="aggregation_rules",
    keywords=["aggregation", "§465(c)", "separate activities", "similar activities", "film", "oil and gas"],
    conclusion_template="""
    IRC §465(c) requires certain activities to be treated separately for at-risk purposes (each activity
    has its own at-risk computation). Similar activities in specific categories (films, equipment leasing,
    farming, oil/gas) CAN be aggregated at taxpayer election. All other activities are aggregated by default.
    """,
    reasoning_framework="""
    DEFAULT RULE (§465(c)(3)(B)):
    All activities OTHER than those listed in §465(c)(1) are aggregated into a single at-risk pool.
    This means taxpayer can offset income from one business against losses from another.

    MANDATORY SEPARATION (§465(c)(1) - specific enumerated activities):
    The following activities MUST be tracked separately (cannot aggregate with other activities):
    1. Films or video tapes
    2. Farming (as defined in §464(e))
    3. Leasing of §1245 property (equipment leasing)
    4. Exploring for or exploiting oil and gas resources
    5. Exploring for or exploiting geothermal deposits

    WITHIN-CATEGORY AGGREGATION ELECTION:
    Taxpayer may elect to aggregate SIMILAR activities within the same category.
    Example: Taxpayer owns 5 separate equipment leasing partnerships. Can elect to aggregate
    all 5 into a single at-risk pool for leasing activities.

    BENEFIT: Income from profitable leasing activity increases at-risk amount for loss-generating activities.

    RISK: If aggregated, cannot separate later without IRS consent. Election is binding.

    OIL & GAS EXCEPTION (§465(c)(3)(A)):
    Working interests in oil and gas properties are EXEMPT from at-risk rules IF:
    - Taxpayer holds a working interest (not royalty/overriding royalty)
    - Liability is not limited by legal arrangement (not through limited partnership/LLC)

    This is a major exception: unlimited personal liability working interests escape §465 entirely.

    FILM AND VIDEO TAPE ACTIVITY RULES:
    Each film is a separate activity. Cannot aggregate multiple films unless elect to do so.
    Post-1986: Special rules under §181 (election to expense production costs) interact with §465.

    FARMING AGGREGATION:
    All farming activities can be aggregated (unless taxpayer elects to separate).
    "Farming" defined in §464(e): cultivation of land, raising livestock, poultry, fish.
    Orchard/vineyard development subject to special capitalization rules (§263A).

    PARTNERSHIP/S-CORP AGGREGATION:
    At-risk rules apply at the PARTNER/SHAREHOLDER level, not entity level.
    Each partner tracks separate at-risk amount for each partnership interest.
    Partner cannot aggregate across different partnerships absent election.
    """,
    key_factors=[
        "Activity classification under §465(c)(1) categories",
        "Films, farming, equipment leasing, oil/gas require separate tracking (unless elect to aggregate)",
        "All other activities aggregated by default",
        "Within-category aggregation requires affirmative election",
        "Election is binding and cannot be easily revoked",
        "Working interest in oil/gas exempt if unlimited personal liability",
        "Pass-through entities: at-risk determined at partner/shareholder level"
    ],
    primary_authority=[
        "IRC §465(c)(1) - Separate activity categories",
        "IRC §465(c)(3)(A) - Oil and gas working interest exception",
        "IRC §465(c)(3)(B) - Aggregation of other activities",
        "Treas. Reg. §1.465-1(c) - Aggregation rules",
        "Temp. Reg. §1.465-1T(c)(2) - Election to aggregate similar activities"
    ],
    burden_holder="Taxpayer bears burden to properly classify and aggregate activities",
    adversary_position="""
    IRS argues:
    1. Activities are in separate §465(c)(1) categories and improperly aggregated
    2. Taxpayer failed to make formal aggregation election (no election statement filed)
    3. Oil/gas working interest has limited liability (through LLC/LP structure) so no exception
    4. Farming activity is actually real estate development (not farming for §465 purposes)
    5. Equipment leasing is incidental to another business (not separate activity)
    """,
    counter_arguments=[
        "All activities are in same category (e.g., all equipment leasing) - aggregation permitted",
        "Aggregation election filed with original return (attach election statement)",
        "Oil/gas working interest held as general partner with unlimited personal liability",
        "Activity meets §464(e) definition of farming (cultivation/livestock)",
        "Equipment leasing is primary business purpose (not incidental)"
    ],
    resolution_strategy="""
    CLASSIFICATION PROTOCOL:
    Step 1: Identify all taxpayer activities
    Step 2: Classify each activity under §465(c)(1) categories or "other"
    Step 3: Determine if within-category aggregation desired (file election if yes)
    Step 4: Maintain separate at-risk schedules for each disaggregated activity
    Step 5: Aggregate all "other" activities by default

    ELECTION MECHANICS:
    - File with original return for first year aggregation desired
    - Election statement: "Taxpayer elects to aggregate the following similar activities under
      Temp. Reg. §1.465-1T(c)(2): [list activities]."
    - Once elected, binding for future years unless IRS consents to change

    OIL & GAS PLANNING:
    Structure working interests outside limited liability entities to escape §465.
    General partnership or sole proprietorship with unlimited liability = no at-risk limitation.
    Trade-off: Exposure to unlimited liability vs. loss deduction flexibility.

    AUDIT DEFENSE:
    Demonstrate activities are properly classified (activity description, primary purpose).
    If aggregation elected, produce election statement from original return.
    If not elected, show separate Form 6198 for each disaggregated activity.
    """,
    entity_scope=EntityScope.ALL,
    confidence=ConfidenceStratification.DEFENSIBLE,
    controlling_precedent="IRC §465(c); Temp. Reg. §1.465-1T(c)"
)


STOP_LOSS_AGREEMENTS = DoctrineBlock(
    topic="stop_loss_agreements",
    keywords=["stop-loss", "loss limitation", "guaranteed return", "limited risk", "§465(b)(4)"],
    conclusion_template="""
    A stop-loss agreement, guarantee of repurchase, or similar arrangement that limits the taxpayer's
    risk of loss REDUCES or ELIMINATES the amount at risk under IRC §465(b)(4). If taxpayer is protected
    against loss beyond a specific amount, at-risk amount is limited to the unprotected exposure.
    """,
    reasoning_framework="""
    ANTI-ABUSE PROVISION (§465(b)(4)):
    Congress enacted this rule to prevent taxpayers from claiming at-risk status while being
    protected from actual economic loss through side agreements.

    FORMS OF LOSS LIMITATION (all trigger §465(b)(4)):

    1. STOP-LOSS AGREEMENTS:
       - Third party agrees to cover losses exceeding $X
       - Example: Taxpayer invests $100K but promoter guarantees maximum loss of $25K
       - At-risk amount = $25K (actual exposure), not $100K (nominal investment)

    2. REPURCHASE AGREEMENTS:
       - Seller or promoter agrees to repurchase investment at minimum price
       - Example: Real estate syndicator guarantees to buy back units at 80% of investment
       - At-risk amount limited to potential 20% loss

    3. GUARANTEED RETURNS:
       - Minimum rate of return guaranteed regardless of activity performance
       - Example: Partnership promises 8% annual return regardless of actual profits
       - Reduces at-risk amount because downside risk is eliminated

    4. INDEMNIFICATION AGREEMENTS:
       - Third party agrees to indemnify taxpayer for losses
       - Example: Promoter indemnifies against environmental liabilities
       - At-risk amount reduced by indemnified exposure

    5. PUT OPTIONS:
       - Taxpayer has right to sell investment at fixed price
       - Floor on potential loss = ceiling on at-risk amount

    COMMERCIALLY REASONABLE vs. SHAM:
    Courts distinguish between:
    - LEGITIMATE BUSINESS PROTECTIONS (do not trigger §465(b)(4)):
      * Standard insurance policies (fire, liability, business interruption)
      * Warranties on equipment
      * Ordinary hedging in commodity businesses
      * Stop-loss insurance in employee benefit plans (unrelated context)

    - ABUSIVE LOSS LIMITATION ARRANGEMENTS (trigger §465(b)(4)):
      * Guarantees designed to eliminate economic risk while preserving tax losses
      * Circular financing (promoter lends money then guarantees return)
      * Related party protection arrangements
      * Non-recourse debt disguised as recourse via secret indemnity

    SUBSTANCE OVER FORM:
    IRS looks beyond formal documents to economic reality:
    - Are loss limitation agreements disclosed in offering materials?
    - Does taxpayer have real downside exposure?
    - Is arrangement commercially reasonable or tax-motivated?
    - Would unrelated parties accept these terms?

    EXAMPLE - ABUSIVE STRUCTURE:
    Taxpayer invests $100K in partnership. Promoter provides:
    1. Non-recourse loan of $400K (no personal liability)
    2. Guarantee to repurchase interest for $80K after 3 years
    3. Management agreement with guaranteed fees covering cash needs

    Analysis: Taxpayer's maximum loss is $20K ($100K investment - $80K guaranteed repurchase).
    At-risk amount = $20K, not $500K (investment + debt).
    Tax losses limited to $20K even though basis may be higher.
    """,
    key_factors=[
        "Existence of repurchase agreements or put options (limits downside)",
        "Guaranteed minimum return provisions (eliminates risk)",
        "Indemnification or hold-harmless agreements (shifts risk to third party)",
        "Related party protection arrangements (family member backstops losses)",
        "Ratio of protection to investment (full protection = zero at-risk)",
        "Commercial reasonableness (legitimate business protection vs. tax avoidance)",
        "Disclosure in offering documents (undisclosed protection = fraud indicator)"
    ],
    primary_authority=[
        "IRC §465(b)(4) - Protection against loss",
        "Treas. Reg. §1.465-6(b) - Guarantees and similar arrangements",
        "Levien v. Commissioner, 103 T.C. 120 (1994) - Stop-loss analysis",
        "Melvin v. Commissioner, 88 T.C. 63 (1987) - Substance over form in loss protection"
    ],
    burden_holder="Taxpayer must disclose and quantify any loss limitation arrangements",
    adversary_position="""
    IRS argues:
    1. Undisclosed repurchase agreement limits taxpayer's actual risk
    2. Promoter's oral promise to protect against loss (not in written documents)
    3. Related party will cover any losses (family understanding, even if not formalized)
    4. Put option or similar right to exit investment at minimum value
    5. Insurance policy is not commercially reasonable (premiums below market)
    6. Combination of protections eliminates substantially all risk
    """,
    counter_arguments=[
        "No repurchase agreement or guarantee exists (no written or oral understanding)",
        "Investment subject to full market risk (no floor on value)",
        "Insurance is commercially reasonable (compare premiums to market rates)",
        "Related party has no legal or economic obligation to cover losses",
        "Any protective arrangements are standard business practice (not tax-motivated)",
        "Taxpayer has already suffered actual economic losses (proves risk is real)"
    ],
    resolution_strategy="""
    DUE DILIGENCE (before investing):
    - Review all subscription documents for loss protection provisions
    - Question promoter about any informal understandings or side letters
    - Analyze economic substance: Is there real downside risk?
    - Compare to similar investments: Are terms commercially reasonable?

    IF LOSS PROTECTION EXISTS:
    - Quantify maximum loss exposure accurately
    - Limit at-risk amount to unprotected portion
    - Do not claim losses in excess of true economic risk
    - Disclose arrangement to tax advisor and on return

    AUDIT DEFENSE:
    - Produce all agreements (written and oral understandings)
    - Demonstrate commercial reasonableness of any protective provisions
    - Show actual economic loss suffered (proves risk was real)
    - Distinguish standard business protections from abusive tax shelters

    PENALTY AVOIDANCE:
    Accuracy-related penalties (20%) apply to underpayments from §465 violations.
    Reasonable cause defense requires: good faith, full disclosure, professional advice.
    """,
    entity_scope=EntityScope.ALL,
    confidence=ConfidenceStratification.DEFENSIBLE,
    controlling_precedent="IRC §465(b)(4); Treas. Reg. §1.465-6(b)"
)


# ═══════════════════════════════════════════════════════════════════════════
# PARTNER LOANS AND RELATED PARTY ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════

PARTNER_LOANS_AT_RISK = DoctrineBlock(
    topic="partner_loans_at_risk",
    keywords=["partner loans", "§465(b)(3)", "related party", "net worth", "equity investment"],
    conclusion_template="""
    A partner's loan to the partnership generally does NOT increase the partner's at-risk amount
    under IRC §465(b)(3) if the loan is from a related party. EXCEPTION: Loan increases at-risk
    if lender (1) has substantial net worth, or (2) has equity investment in the activity.
    """,
    reasoning_framework="""
    RELATED PARTY EXCLUSION (§465(b)(3)):
    Amounts borrowed from related parties do NOT increase at-risk amount UNLESS exception applies.

    RELATED PARTY DEFINITION (§465(b)(3)(C)):
    - Family members: spouse, ancestors, lineal descendants
    - Controlled corporations (80% ownership)
    - Partnerships where taxpayer owns >10% profits or capital interest
    - Grantor trusts
    - Attribution rules apply (constructive ownership)

    WHY EXCLUSION EXISTS:
    Related party loans can be illusory—family member lends money but has no real expectation
    of repayment or enforcement. Without this rule, taxpayers could artificially inflate
    at-risk amounts through circular lending within family.

    EXCEPTION #1: SUBSTANTIAL NET WORTH (§465(b)(3)(A)):
    Loan from related party DOES increase at-risk amount if lender has NET WORTH exceeding:
    - $1 million (inflation-adjusted), OR
    - 10x the amount loaned to taxpayer

    RATIONALE: Wealthy lender has capacity and incentive to enforce loan.

    EXAMPLE:
    Father loans son $50,000 for business investment.
    Father's net worth = $2 million.
    Result: Loan increases son's at-risk amount (net worth exceeds $1M and exceeds 10x loan).

    EXCEPTION #2: EQUITY INVESTMENT (§465(b)(3)(B)):
    Loan from related party DOES increase at-risk amount if lender has EQUITY interest in
    the activity and the interest is not acquired through non-recourse debt.

    RATIONALE: Lender with skin in the game (equity owner) has aligned interests.

    EXAMPLE:
    Partner A loans $100K to partnership. Partner A also contributed $50K equity capital.
    Result: Loan increases Partner A's at-risk amount (lender has equity investment).

    PARTNERSHIP OUTSIDE BASIS vs. AT-RISK:
    - Partner's outside basis includes share of partnership liabilities (recourse + qualified nonrecourse)
    - Partner's at-risk amount is MORE RESTRICTIVE (excludes related party loans absent exception)
    - Loss deduction requires BOTH sufficient basis AND sufficient at-risk amount
    - Whichever is lower controls the deductible loss

    COMMON TRAP:
    Partner has $200K outside basis (including $150K related party loan).
    Related party lender does not meet net worth or equity investment exception.
    At-risk amount = $50K (excludes $150K loan).
    Partner's K-1 shows $100K loss.
    Deductible loss = $50K (at-risk limit), even though basis supports $200K.
    $50K loss suspended until at-risk amount increases.
    """,
    key_factors=[
        "Lender is related party under §465(b)(3)(C) (family, controlled entity)",
        "Lender's net worth exceeds $1M or 10x loan amount (exception applies)",
        "Lender has equity investment in the activity (exception applies)",
        "Loan is bona fide (enforceable note, market interest rate, repayment terms)",
        "Loan is not circular (borrowed from third party to re-lend to related party)",
        "Partner's outside basis vs. at-risk amount (basis ≥ at-risk, but not always equal)"
    ],
    primary_authority=[
        "IRC §465(b)(3) - Related party loans exclusion and exceptions",
        "IRC §465(b)(3)(A) - Net worth exception",
        "IRC §465(b)(3)(B) - Equity investment exception",
        "IRC §465(b)(3)(C) - Related party definition",
        "Treas. Reg. §1.465-8 - Amounts borrowed from persons with interest in activity"
    ],
    burden_holder="Taxpayer must prove related party loan qualifies for exception",
    adversary_position="""
    IRS challenges related party loan at-risk treatment:
    1. Lender is related party and does not meet net worth exception
    2. Lender's net worth overstated (assets valued at FMV rather than basis, or illiquid assets)
    3. Lender has no equity investment in the activity (debt-only lender)
    4. Loan is not bona fide (no repayment, no interest, no enforcement)
    5. Circular financing (third party loaned to related party who re-lent to taxpayer)
    6. Loan forgiveness anticipated (no real creditor relationship)
    """,
    counter_arguments=[
        "Lender's financial statement shows net worth of $X (exceeds statutory threshold)",
        "Lender is also equity partner with $Y capital contribution",
        "Loan documented with promissory note, market interest rate, scheduled payments",
        "Taxpayer has made regular principal and interest payments (proves bona fide debt)",
        "No relationship between lender and third party sources (no circular financing)",
        "Lender has history of enforcing debts (prior collection actions)"
    ],
    resolution_strategy="""
    DOCUMENTATION REQUIREMENTS:
    □ Promissory note with arm's-length terms (interest rate, maturity, payment schedule)
    □ Lender's financial statement (if claiming net worth exception)
    □ Partnership agreement showing lender's equity investment (if claiming equity exception)
    □ Payment records (canceled checks, wire transfers showing actual repayment)
    □ Loan is included in partnership balance sheet as liability
    □ No side agreements or understandings regarding non-enforcement

    NET WORTH EXCEPTION SUBSTANTIATION:
    - Personal financial statement (balance sheet showing assets and liabilities)
    - Appraisals for significant assets (real estate, business interests)
    - Net worth must be computed at time of loan (not later appreciation)
    - Deduct ALL liabilities (mortgage, credit cards, other debts)
    - Use conservative valuations (IRS will challenge inflated asset values)

    EQUITY INVESTMENT EXCEPTION SUBSTANTIATION:
    - Partnership K-1 showing lender's capital account
    - Cash contribution records (not just debt contribution)
    - Lender's equity must be AT RISK (not funded with non-recourse debt)

    ALTERNATIVE PLANNING:
    If related party loan does not qualify:
    - Refinance with unrelated commercial lender (bank, credit union)
    - Related party contributes equity instead of debt (permanent capital)
    - Related party guarantees third-party loan (if guarantee is substantive)

    AUDIT STRATEGY:
    Anticipate IRS challenge to related party loans. Proactive documentation is critical.
    If loan does NOT qualify, adjust at-risk computation accordingly and avoid overstating losses.
    """,
    entity_scope=EntityScope.PARTNERSHIP,
    confidence=ConfidenceStratification.DEFENSIBLE,
    controlling_precedent="IRC §465(b)(3); Treas. Reg. §1.465-8"
)


# Additional 44 doctrine blocks covering: loss recapture, ordering rules, interaction with §469,
# interaction with §461(l), pass-through entity look-through, real estate professional exception,
# oil & gas exception, holding activity rules, S-corp shareholder at-risk basis, and more...
# [Truncated for length - production version would include all 50+ blocks]


# ═══════════════════════════════════════════════════════════════════════════
# LOSS RECAPTURE RULES
# ═══════════════════════════════════════════════════════════════════════════

LOSS_RECAPTURE_465 = DoctrineBlock(
    topic="loss_recapture_465",
    keywords=["recapture", "§465(e)", "at-risk decrease", "income recognition", "distribution"],
    conclusion_template="""
    IRC §465(e) requires RECAPTURE of previously allowed losses when the at-risk amount decreases
    below zero (through distributions, debt reduction, or guarantee elimination). Recapture amount
    is treated as income in the year at-risk goes negative, up to the amount of previously deducted losses.
    """,
    reasoning_framework="""
    RECAPTURE MECHANISM (§465(e)):
    If previously deducted losses under §465 and at-risk amount later decreases below zero,
    taxpayer must recapture (include in income) the excess.

    FORMULA:
    Recapture Income = Lesser of:
    (1) Amount by which at-risk is negative, OR
    (2) Cumulative losses previously deducted under §465

    TRIGGERING EVENTS:
    1. Cash distribution exceeding at-risk amount
    2. Reduction in partnership liabilities allocated to partner
    3. Elimination of personal guarantee (converts recourse to non-recourse)
    4. Sale of property securing qualified nonrecourse financing
    5. Conversion of activity property to personal use

    EXAMPLE:
    Year 1: Partner contributes $50K cash, borrows $150K recourse debt. At-risk = $200K.
             Partnership loses $180K. Partner deducts $180K loss. At-risk = $20K.
    Year 2: Partnership repays $100K of debt. Partner's share of debt reduction = $100K.
             At-risk = $20K - $100K = ($80K) negative.
             Recapture income = $80K (lesser of $80K negative or $180K prior losses).

    Year 2: Partner reports $80K §465(e) recapture income on tax return.
            At-risk amount resets to zero (not negative).

    RECAPTURE vs. GAIN:
    Recapture is ORDINARY INCOME under §465(e), not capital gain.
    Character is determined by original loss character (usually ordinary business loss).
    Recapture does NOT depend on sale or disposition (can occur while still owning interest).

    MULTI-YEAR TRACKING:
    Taxpayer must track cumulative §465 losses over entire holding period.
    Only losses actually DEDUCTED trigger recapture (suspended losses do not).

    INTERACTION WITH BASIS:
    Recapture income increases partner's outside basis (prevents double taxation on later sale).
    At-risk amount is separate from basis but both must be tracked.
    """,
    key_factors=[
        "At-risk amount goes negative (below zero)",
        "Prior losses were deducted under §465 (not suspended)",
        "Decrease triggered by distribution, debt reduction, or guarantee elimination",
        "Recapture limited to previously deducted losses (not total losses)",
        "Recapture is ordinary income (not capital gain)",
        "Basis adjustment for recapture income (prevents double tax)"
    ],
    primary_authority=[
        "IRC §465(e) - Recapture of losses where amount at risk is less than zero",
        "Treas. Reg. §1.465-23 - Recapture rules",
        "IRS Form 6198 Instructions - Recapture computation"
    ],
    burden_holder="Taxpayer must track and report recapture income",
    adversary_position="""
    IRS argues:
    1. Taxpayer failed to report recapture income when at-risk went negative
    2. At-risk decreased below zero in prior year (statute of limitations on assessment)
    3. Amount of recapture understated (cumulative losses higher than reported)
    4. Debt reduction triggered recapture but not reported
    """,
    counter_arguments=[
        "At-risk amount never went negative (remained at zero or positive)",
        "Losses were suspended under §465 (not deducted) so no recapture required",
        "Debt was qualified nonrecourse financing (reduction does not trigger recapture)",
        "Distribution was return of capital, not in excess of at-risk amount"
    ],
    resolution_strategy="""
    PREVENTION:
    Monitor at-risk amount annually before taking distributions.
    If distribution would cause negative at-risk, either:
    (a) Limit distribution to preserve zero or positive at-risk, OR
    (b) Recognize recapture income is required and plan for tax liability.

    COMPUTATIONAL WORKSHEET:
    Beginning at-risk amount: $____
    + Income allocated: $____
    + Additional contributions: $____
    + Debt increases: $____
    - Losses allocated: ($____)
    - Distributions: ($____)
    - Debt decreases: ($____)
    = Ending at-risk amount: $____

    If ending amount is negative: Recapture = lesser of negative amount or cumulative deducted losses.

    AUDIT DOCUMENTATION:
    □ Multi-year at-risk schedule
    □ Form 6198 for all years
    □ Partnership K-1s showing income/loss/distribution
    □ Debt agreements and repayment records
    □ Recapture computation worksheet
    """,
    entity_scope=EntityScope.ALL,
    confidence=ConfidenceStratification.DEFENSIBLE,
    controlling_precedent="IRC §465(e); Treas. Reg. §1.465-23"
)


# Doctrine registry for runtime access
DOCTRINE_REGISTRY = {
    "at_risk_basic_computation": AT_RISK_BASIC_COMPUTATION,
    "non_recourse_debt_exclusion": NON_RECOURSE_DEBT_EXCLUSION,
    "qualified_nonrecourse_financing": QUALIFIED_NONRECOURSE_FINANCING,
    "aggregation_rules": AGGREGATION_RULES,
    "stop_loss_agreements": STOP_LOSS_AGREEMENTS,
    "partner_loans_at_risk": PARTNER_LOANS_AT_RISK,
    "loss_recapture_465": LOSS_RECAPTURE_465,
    # Additional 43+ doctrines would be included in production version
}
