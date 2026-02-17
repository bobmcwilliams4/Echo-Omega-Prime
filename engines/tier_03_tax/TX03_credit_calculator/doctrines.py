"""
TX03 Credit Calculator Engine - Doctrine Cache
Comprehensive tax credit calculation doctrines covering IRC §21-§179D
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum


class IssueCategory(Enum):
    """Tax credit issue categorization"""
    INDIVIDUAL_CREDITS = "individual_credits"
    BUSINESS_CREDITS = "business_credits"
    REFUNDABLE_CREDITS = "refundable_credits"
    NONREFUNDABLE_CREDITS = "nonrefundable_credits"
    ENERGY_CREDITS = "energy_credits"
    EDUCATION_CREDITS = "education_credits"
    EMPLOYMENT_CREDITS = "employment_credits"
    INVESTMENT_CREDITS = "investment_credits"
    CREDIT_CARRYOVERS = "credit_carryovers"
    CREDIT_ORDERING = "credit_ordering"
    CREDIT_LIMITATIONS = "credit_limitations"
    CREDIT_RECAPTURE = "credit_recapture"


class ConfidenceStratification(Enum):
    """Confidence stratification levels"""
    DEFENSIBLE = "defensible"
    AGGRESSIVE = "aggressive"
    DISCLOSURE = "disclosure"
    HIGH_RISK = "high_risk"


@dataclass
class DoctrineBlock:
    """Single doctrine block with full reasoning framework"""
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
    entity_scope: List[str]
    confidence: float
    confidence_stratification: ConfidenceStratification
    controlling_precedent: Optional[str] = None
    issue_category: IssueCategory = IssueCategory.INDIVIDUAL_CREDITS
    credit_type: str = "nonrefundable"
    recapture_risk: bool = False
    carryover_allowed: bool = False
    ordering_priority: int = 50


# 65 Doctrine Blocks for Tax Credit Calculation

DOCTRINE_CACHE: List[DoctrineBlock] = [
    # CHILD AND DEPENDENT CARE CREDIT - IRC §21
    DoctrineBlock(
        topic="child_dependent_care_credit_eligibility",
        keywords=["IRC_21", "dependent_care", "child_care_credit", "employment_related_expenses", "qualifying_individual"],
        conclusion_template=[
            "The child and dependent care credit under IRC §21 allows a credit for employment-related expenses paid for the care of qualifying individuals.",
            "The credit percentage ranges from 20% to 35% based on AGI, applied to up to $3,000 (one qualifying individual) or $6,000 (two or more).",
            "Qualifying individuals include children under 13, disabled spouse, or disabled dependent incapable of self-care."
        ],
        reasoning_framework="""
IRC §21 provides a credit for employment-related expenses incurred to enable the taxpayer to be gainfully employed.

QUALIFICATION REQUIREMENTS:
1. QUALIFYING INDIVIDUAL: Child under 13, disabled spouse, or disabled dependent who:
   - Lives with taxpayer for more than half the year
   - Is incapable of self-care (if disabled)
   - Qualifies as taxpayer's dependent (or would but for exemption amount)

2. EMPLOYMENT-RELATED EXPENSES:
   - Must be incurred to enable taxpayer to work or look for work
   - Both spouses must work (if married filing jointly)
   - Payments cannot be to dependent or child under 19
   - Must identify care provider (name, address, TIN)

3. CREDIT CALCULATION:
   - Applicable percentage: 35% (AGI ≤ $15,000), reducing by 1% for each $2,000 over $15,000, minimum 20%
   - Maximum expenses: $3,000 (one qualifying individual) or $6,000 (two or more)
   - Credit = applicable percentage × lesser of (expenses or limit)

4. EARNED INCOME LIMITATION:
   - Credit limited to earned income of lesser-earning spouse
   - Student/disabled spouse deemed to have $250/month (one child) or $500/month (two or more)

5. EMPLOYMENT STATUS:
   - Taxpayer must have earned income during the year
   - If married, both spouses must work (or one full-time student/disabled)
        """,
        key_factors=[
            "Age of qualifying individual (under 13 for children)",
            "Disability status (if over 13)",
            "Taxpayer's employment status and earned income",
            "Proper identification of care provider",
            "AGI level determines applicable percentage",
            "Coordination with dependent care FSA reduces allowable expenses"
        ],
        primary_authority=[
            "IRC §21 - Child and dependent care credit",
            "Treas. Reg. §1.21-1 - Expenses for household and dependent care services",
            "IRS Pub. 503 - Child and Dependent Care Expenses"
        ],
        burden_holder="Taxpayer must substantiate qualifying individual status, employment-related nature of expenses, and care provider identification.",
        adversary_position="IRS may challenge that expenses were not employment-related, care provider was a dependent, or individual did not qualify.",
        counter_arguments=[
            "Expenses were for education rather than care (tuition vs. daycare)",
            "Taxpayer was not gainfully employed during expense period",
            "Care provider identification insufficient (missing TIN)",
            "Individual did not live with taxpayer for required period",
            "Expenses reimbursed by dependent care FSA were included"
        ],
        resolution_strategy="Maintain detailed records of care provider information, employment status, and expense receipts. Coordinate with employer-provided dependent care benefits (Form 2441).",
        entity_scope=["Individual", "Married_Filing_Jointly"],
        confidence=0.95,
        confidence_stratification=ConfidenceStratification.DEFENSIBLE,
        issue_category=IssueCategory.INDIVIDUAL_CREDITS,
        credit_type="nonrefundable",
        recapture_risk=False,
        carryover_allowed=False,
        ordering_priority=30
    ),

    # CHILD TAX CREDIT - IRC §24
    DoctrineBlock(
        topic="child_tax_credit_eligibility",
        keywords=["IRC_24", "CTC", "child_tax_credit", "qualifying_child", "ACTC", "additional_child_tax_credit"],
        conclusion_template=[
            "The child tax credit under IRC §24 provides up to $2,000 per qualifying child under age 17.",
            "The credit phases out for higher-income taxpayers beginning at $200,000 (single) or $400,000 (joint).",
            "Up to $1,600 may be refundable as the additional child tax credit (ACTC) based on earned income."
        ],
        reasoning_framework="""
IRC §24 allows a credit for each qualifying child, with both nonrefundable and refundable components.

QUALIFYING CHILD REQUIREMENTS (IRC §24(c)):
1. AGE: Under age 17 at end of taxable year
2. RELATIONSHIP: Son, daughter, stepchild, foster child, sibling, step-sibling, or descendant
3. SUPPORT: Did not provide over half of own support
4. RESIDENCY: Lived with taxpayer for more than half of year
5. DEPENDENT: Must be claimed as dependent (not just eligible)
6. CITIZENSHIP: U.S. citizen, national, or resident alien
7. IDENTIFICATION: Must have valid SSN issued before due date of return

CREDIT AMOUNT (IRC §24(a), (h)):
- Base credit: $2,000 per qualifying child
- Nonrefundable portion: Limited by tax liability, reduced by other nonrefundable credits
- Refundable portion (ACTC): Lesser of $1,600 or 15% × (earned income − $2,500)

PHASE-OUT (IRC §24(b)):
- Threshold: $200,000 (single), $400,000 (married filing jointly)
- Reduction: $50 for each $1,000 (or fraction) above threshold
- Applies to total credit (nonrefundable + refundable)

CREDIT FOR OTHER DEPENDENTS (IRC §24(h)(6)):
- $500 credit for dependents who don't qualify for CTC
- Nonrefundable only, same phase-out thresholds
        """,
        key_factors=[
            "Child's age on December 31 (must be under 17)",
            "Valid SSN issued before return due date",
            "U.S. citizenship or residency status",
            "Earned income amount (affects refundable portion)",
            "Modified AGI relative to phase-out thresholds",
            "Proper dependent claiming (can't be claimed by another taxpayer)"
        ],
        primary_authority=[
            "IRC §24 - Child tax credit",
            "IRC §24(h) - Additional child tax credit (refundable)",
            "Treas. Reg. §1.24-1 - Child tax credit",
            "IRS Pub. 972 - Child Tax Credit"
        ],
        burden_holder="Taxpayer must prove child meets all qualifying child requirements and has valid SSN.",
        adversary_position="IRS may challenge qualifying child status, residency period, SSN validity, or that child was claimed by another taxpayer.",
        counter_arguments=[
            "Child turned 17 during the tax year",
            "SSN was ITIN or applied for after return due date",
            "Child did not live with taxpayer for more than half year",
            "Child provided over half of own support",
            "Child was claimed as dependent by another taxpayer (tiebreaker rules apply)"
        ],
        resolution_strategy="Maintain birth certificates, SSN documentation, residency records (school, medical). Apply tiebreaker rules (IRC §152(c)(4)) if multiple taxpayers could claim. File Form 8812 for ACTC calculation.",
        entity_scope=["Individual", "Married_Filing_Jointly"],
        confidence=0.96,
        confidence_stratification=ConfidenceStratification.DEFENSIBLE,
        issue_category=IssueCategory.INDIVIDUAL_CREDITS,
        credit_type="partially_refundable",
        recapture_risk=False,
        carryover_allowed=False,
        ordering_priority=20
    ),

    # EARNED INCOME TAX CREDIT - IRC §32
    DoctrineBlock(
        topic="earned_income_tax_credit_calculation",
        keywords=["EITC", "EIC", "IRC_32", "earned_income_credit", "refundable_credit", "qualifying_child_EITC"],
        conclusion_template=[
            "The earned income tax credit under IRC §32 is a refundable credit for low-to-moderate income workers.",
            "Credit amount depends on earned income, number of qualifying children (0, 1, 2, or 3+), and filing status.",
            "Investment income cannot exceed $11,000 (2024) and AGI must be below phase-out thresholds."
        ],
        reasoning_framework="""
IRC §32 provides a refundable credit to supplement wages for low-income workers, with larger credits for those with qualifying children.

ELIGIBILITY REQUIREMENTS (IRC §32(c)):
1. EARNED INCOME: Wages, self-employment income, or certain disability payments
2. AGI/EARNED INCOME LIMITS: Must be below threshold for filing status and children count
3. INVESTMENT INCOME: Cannot exceed $11,000 (indexed annually)
4. FILING STATUS: Cannot be married filing separately
5. U.S. RESIDENCY: Must be U.S. citizen or resident alien all year
6. NO FOREIGN EARNED INCOME EXCLUSION: Cannot claim IRC §911
7. VALID SSN: Must have valid SSN by return due date (including extensions)

QUALIFYING CHILD REQUIREMENTS (IRC §32(c)(3)):
- Same relationship, age, residency, and support tests as CTC
- Age limits: Under 19 (24 if full-time student, no limit if permanently disabled)
- Must have valid SSN
- Cannot be qualifying child of another taxpayer

CREDIT CALCULATION (IRC §32(b)):
PHASE-IN: Credit % × earned income (up to maximum earned income)
MAXIMUM: Flat credit amount in plateau range
PHASE-OUT: Reduced by phase-out % × (AGI or earned income, whichever greater − threshold)

2024 PARAMETERS (0, 1, 2, 3+ children):
- Credit %: 7.65%, 34%, 40%, 45%
- Max credit: $632, $4,213, $6,960, $7,830
- Phase-out begins: $10,330/$17,640 (single/joint for 0 children)
- Phase-out %: 7.65%, 15.98%, 21.06%, 21.06%

DUE DILIGENCE REQUIREMENTS (IRC §32(k)):
Paid preparers must meet due diligence requirements or face $600 penalty per failure.
        """,
        key_factors=[
            "Earned income amount and source (W-2, Schedule C, Schedule F)",
            "Investment income limitation ($11,000 threshold)",
            "Number of qualifying children (0-3+)",
            "Filing status (MFS ineligible)",
            "AGI and earned income for phase-out calculation",
            "Valid SSN for taxpayer, spouse, and qualifying children",
            "No foreign earned income exclusion claimed"
        ],
        primary_authority=[
            "IRC §32 - Earned income tax credit",
            "Treas. Reg. §1.32-2 - Earned income",
            "IRS Pub. 596 - Earned Income Credit",
            "Rev. Proc. 2023-34 - Inflation adjustments"
        ],
        burden_holder="Taxpayer must substantiate earned income, qualifying child status, and investment income limitations.",
        adversary_position="IRS heavily audits EITC claims; may challenge qualifying child status, earned income amounts, or investment income calculation.",
        counter_arguments=[
            "Self-employment income not properly reported or substantiated",
            "Investment income exceeded $11,000 threshold",
            "Qualifying child claimed by another taxpayer",
            "Child did not live with taxpayer for more than half year",
            "Filing status was married filing separately",
            "Taxpayer claimed foreign earned income exclusion"
        ],
        resolution_strategy="Maintain meticulous records of earned income (pay stubs, 1099-NEC, business records), residency proof for qualifying children, and investment income statements. Apply tiebreaker rules if necessary. File Form 8862 if previously disallowed.",
        entity_scope=["Individual", "Married_Filing_Jointly", "Head_of_Household"],
        confidence=0.94,
        confidence_stratification=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="Heavily regulated; strict documentation requirements",
        issue_category=IssueCategory.REFUNDABLE_CREDITS,
        credit_type="refundable",
        recapture_risk=False,
        carryover_allowed=False,
        ordering_priority=10
    ),

    # AMERICAN OPPORTUNITY TAX CREDIT - IRC §25A(i)
    DoctrineBlock(
        topic="american_opportunity_tax_credit_requirements",
        keywords=["AOTC", "IRC_25A_i", "Hope_credit", "education_credit", "qualified_education_expenses", "eligible_student"],
        conclusion_template=[
            "The American Opportunity Tax Credit under IRC §25A(i) provides up to $2,500 per eligible student for first four years of post-secondary education.",
            "40% of the credit ($1,000) is refundable even if taxpayer has no tax liability.",
            "Student must be pursuing degree, enrolled at least half-time, and have no felony drug conviction."
        ],
        reasoning_framework="""
IRC §25A(i) allows a partially refundable credit for qualified tuition and related expenses for the first four years of post-secondary education.

ELIGIBLE STUDENT REQUIREMENTS (IRC §25A(i)(3)):
1. DEGREE PROGRAM: Enrolled in program leading to degree, certificate, or recognized credential
2. ENROLLMENT STATUS: At least half-time for at least one academic period during tax year
3. YEAR LIMITATION: Has not completed first four years of post-secondary education before tax year
4. NO PRIOR AOTC/HOPE: Has not claimed AOTC (or Hope) for more than four tax years
5. NO FELONY DRUG CONVICTION: No federal or state felony drug conviction as of end of tax year
6. IDENTIFICATION: Must have valid TIN (SSN, ITIN, or ATIN)

QUALIFIED EDUCATION EXPENSES (IRC §25A(f)):
- Tuition and fees required for enrollment or attendance
- Course materials required for course (books, supplies, equipment)
- EXCLUDES: Room and board, insurance, medical, transportation, non-required fees

CREDIT CALCULATION (IRC §25A(i)(1)):
- 100% of first $2,000 of qualified expenses
- 25% of next $2,000 of qualified expenses
- Maximum credit: $2,500 per eligible student

REFUNDABLE PORTION (IRC §25A(i)(5)):
- 40% of credit (max $1,000) is refundable
- Refundable portion not allowed if student under 24 and IRC §152(c) applies (kiddie tax rules)

PHASE-OUT (IRC §25A(i)(4)):
- Begins: $80,000 MAGI (single), $160,000 (joint)
- Completely phased out: $90,000 (single), $180,000 (joint)
- MAGI = AGI + foreign earned income exclusion + foreign housing exclusion

COORDINATION WITH OTHER BENEFITS:
- Cannot claim AOTC and Lifetime Learning Credit for same student in same year
- Qualified expenses reduced by tax-free educational assistance (Pell grants, scholarships, 529 distributions)
- Form 1098-T reporting required from eligible educational institution
        """,
        key_factors=[
            "Student enrolled at least half-time in degree program",
            "Not more than four years of AOTC/Hope claimed",
            "No felony drug conviction",
            "Valid TIN for student",
            "MAGI within phase-out limits",
            "Qualified expenses properly reduced by tax-free aid",
            "Form 1098-T received from institution"
        ],
        primary_authority=[
            "IRC §25A(i) - American Opportunity Tax Credit",
            "IRC §25A(f) - Qualified tuition and related expenses",
            "Treas. Reg. §1.25A-1 - Denial of double benefit",
            "IRS Pub. 970 - Tax Benefits for Education",
            "Form 8863 - Education Credits"
        ],
        burden_holder="Taxpayer must substantiate student eligibility, qualified expenses, and coordination with other educational benefits.",
        adversary_position="IRS may challenge half-time enrollment status, year count, expense qualification, or reduction for tax-free aid.",
        counter_arguments=[
            "Student was not enrolled at least half-time for any academic period",
            "AOTC already claimed for four prior years",
            "Felony drug conviction exists but not disclosed",
            "Expenses claimed include non-qualified items (room and board)",
            "Expenses not reduced by scholarship or 529 distribution",
            "Form 1098-T shows different expense amounts"
        ],
        resolution_strategy="Obtain Form 1098-T from institution, enrollment verification, payment receipts for required course materials, and documentation of scholarships/grants. Track years of AOTC claimed. File Form 8863 with return.",
        entity_scope=["Individual", "Married_Filing_Jointly", "Head_of_Household"],
        confidence=0.93,
        confidence_stratification=ConfidenceStratification.DEFENSIBLE,
        issue_category=IssueCategory.EDUCATION_CREDITS,
        credit_type="partially_refundable",
        recapture_risk=False,
        carryover_allowed=False,
        ordering_priority=25
    ),

    # LIFETIME LEARNING CREDIT - IRC §25A(c)
    DoctrineBlock(
        topic="lifetime_learning_credit_calculation",
        keywords=["LLC", "IRC_25A_c", "lifetime_learning", "education_credit", "qualified_tuition", "post_secondary"],
        conclusion_template=[
            "The Lifetime Learning Credit under IRC §25A(c) provides 20% of up to $10,000 in qualified education expenses ($2,000 max credit per return).",
            "Unlike AOTC, LLC has no year limit, no degree requirement, and covers graduate courses.",
            "LLC is nonrefundable and has lower phase-out thresholds than AOTC."
        ],
        reasoning_framework="""
IRC §25A(c) allows a nonrefundable credit for qualified tuition and related expenses for post-secondary education without year or degree limitations.

ELIGIBLE STUDENT REQUIREMENTS (IRC §25A(c)):
1. ENROLLMENT: Taking one or more courses at eligible educational institution
2. NO DEGREE REQUIREMENT: Course can be for degree, credential, or job skills
3. NO YEAR LIMITATION: Can claim indefinitely (unlike AOTC's four-year limit)
4. NO HALF-TIME REQUIREMENT: Even one course qualifies
5. GRADUATE COURSES: Allowed (AOTC only covers undergraduate)

QUALIFIED EDUCATION EXPENSES (IRC §25A(f)):
- Tuition and fees required for enrollment or attendance
- EXCLUDES: Books, supplies, equipment (unless required to be paid to institution)
- EXCLUDES: Room and board, insurance, medical, transportation

CREDIT CALCULATION (IRC §25A(c)(1)):
- 20% of qualified education expenses
- Maximum expenses: $10,000 per return (not per student)
- Maximum credit: $2,000 per return

NONREFUNDABLE STATUS:
- Credit limited to tax liability
- No refundable portion (unlike AOTC)
- Excess credit lost (no carryover)

PHASE-OUT (IRC §25A(d)):
- Begins: $80,000 MAGI (single), $160,000 (joint)
- Completely phased out: $90,000 (single), $180,000 (joint)
- Same phase-out as AOTC

COORDINATION RULES:
- Cannot claim LLC and AOTC for same student in same year
- Can claim AOTC for one student and LLC for another student
- Expenses reduced by tax-free educational assistance
- Per-return limit means multiple students share $10,000 cap
        """,
        key_factors=[
            "No year limitation (can claim indefinitely)",
            "Graduate and professional courses eligible",
            "Per-return limit ($10,000 expenses, $2,000 credit)",
            "Nonrefundable only (no refund if no tax liability)",
            "Same phase-out thresholds as AOTC",
            "Coordination with AOTC (cannot claim both for same student)"
        ],
        primary_authority=[
            "IRC §25A(c) - Lifetime Learning Credit",
            "IRC §25A(f) - Qualified tuition and related expenses",
            "Treas. Reg. §1.25A-2 - Lifetime Learning Credit",
            "IRS Pub. 970 - Tax Benefits for Education"
        ],
        burden_holder="Taxpayer must substantiate enrollment, qualified expenses, and that AOTC not claimed for same student.",
        adversary_position="IRS may challenge that expenses were for courses at eligible institution or that expenses were reduced by tax-free aid.",
        counter_arguments=[
            "Institution not eligible educational institution (not Title IV eligible)",
            "Expenses include books/supplies not paid to institution",
            "AOTC claimed for same student in same year",
            "Expenses not reduced by employer reimbursement or scholarship"
        ],
        resolution_strategy="Obtain Form 1098-T, enrollment verification, and payment records. Choose between AOTC and LLC based on maximum benefit. File Form 8863.",
        entity_scope=["Individual", "Married_Filing_Jointly", "Head_of_Household"],
        confidence=0.94,
        confidence_stratification=ConfidenceStratification.DEFENSIBLE,
        issue_category=IssueCategory.EDUCATION_CREDITS,
        credit_type="nonrefundable",
        recapture_risk=False,
        carryover_allowed=False,
        ordering_priority=35
    ),

    # GENERAL BUSINESS CREDIT - IRC §38
    DoctrineBlock(
        topic="general_business_credit_structure",
        keywords=["IRC_38", "GBC", "general_business_credit", "credit_carryback", "credit_carryforward", "business_credit_components"],
        conclusion_template=[
            "The general business credit under IRC §38 is an umbrella credit comprising multiple component credits.",
            "GBC is limited to net income tax minus the greater of (1) tentative minimum tax or (2) 25% of net regular tax over $25,000.",
            "Unused credits can be carried back 1 year and forward 20 years."
        ],
        reasoning_framework="""
IRC §38 aggregates multiple business credits into a single general business credit with unified limitation and carryover rules.

COMPONENT CREDITS (IRC §38(b)):
Includes 30+ credits, most common:
- IRC §41 - Research credit
- IRC §42 - Low-income housing credit
- IRC §45 - Renewable electricity production credit
- IRC §45F - Employer-provided child care credit
- IRC §51 - Work opportunity credit
- IRC §46 - Investment credit (rehabilitation, energy, reforestation)
- IRC §47 - Rehabilitation credit

CREDIT LIMITATION (IRC §38(c)):
GBC limited to EXCESS of:
1. Net income tax (regular tax - nonrefundable credits), OVER
2. GREATER of:
   (a) Tentative minimum tax, OR
   (b) 25% × (net regular tax liability − $25,000)

NET REGULAR TAX LIABILITY = regular tax − nonrefundable personal credits

ORDERING RULES (IRC §38(d)):
Credits used in this order:
1. Carryforwards from earliest year first
2. Current year credits
3. Carrybacks from latest year

CARRYBACK/CARRYFORWARD (IRC §39):
- CARRYBACK: 1 year (except ESOP credits and specified credits)
- CARRYFORWARD: 20 years (21 years for credits arising after 2017)
- Specified liability loss credits: 10-year carryback, indefinite carryforward
- Election to forgo carryback period (IRC §39(a)(4))

AT-RISK RULES (IRC §49):
Investment credit component subject to at-risk limitations.

PASSIVE ACTIVITY RULES (IRC §469):
Credits from passive activities limited to tax attributable to passive income.
        """,
        key_factors=[
            "Current year net income tax amount",
            "Tentative minimum tax (AMT calculation)",
            "Total component credits from all sources",
            "Existence of credit carryforwards from prior years",
            "Passive activity status of credit-generating activities",
            "At-risk limitations on investment credits"
        ],
        primary_authority=[
            "IRC §38 - General business credit",
            "IRC §39 - Carryback and carryforward of unused credits",
            "IRC §38(c) - Limitation based on tax liability",
            "Treas. Reg. §1.38-1 - General business credit",
            "Form 3800 - General Business Credit"
        ],
        burden_holder="Taxpayer must track component credits, apply limitation formula, and maintain carryover schedules.",
        adversary_position="IRS may challenge underlying component credit calculations, limitation computation, or passive activity restrictions.",
        counter_arguments=[
            "Tentative minimum tax calculation incorrect",
            "Component credit not properly calculated (e.g., research credit)",
            "Passive activity limitations not applied",
            "At-risk limitations ignored for investment credits",
            "Carryforward period expired (20-year limit)"
        ],
        resolution_strategy="Use Form 3800 to aggregate credits and calculate limitation. Maintain detailed records of component credit computations. Track carryover schedules carefully. Consider timing of income to maximize credit utilization.",
        entity_scope=["C_Corporation", "S_Corporation", "Partnership", "Individual_Business"],
        confidence=0.92,
        confidence_stratification=ConfidenceStratification.DEFENSIBLE,
        issue_category=IssueCategory.BUSINESS_CREDITS,
        credit_type="nonrefundable",
        recapture_risk=True,
        carryover_allowed=True,
        ordering_priority=60
    ),

    # RESEARCH CREDIT - IRC §41
    DoctrineBlock(
        topic="research_credit_qualified_research",
        keywords=["IRC_41", "R&D_credit", "research_development", "qualified_research_expenses", "four_part_test", "QRE"],
        conclusion_template=[
            "The research credit under IRC §41 provides a credit for increasing qualified research expenses.",
            "Research must satisfy four-part test: technological in nature, eliminate uncertainty, process of experimentation, qualified purpose.",
            "Credit is generally 20% of QREs above a base amount, or 14% reduced rate for alternative simplified credit."
        ],
        reasoning_framework="""
IRC §41 incentivizes domestic research and development through a credit based on incremental qualified research expenses.

FOUR-PART TEST (IRC §41(d)(1)):
Research qualifies only if ALL four requirements met:
1. TECHNOLOGICAL IN NATURE: Relies on hard sciences (engineering, physics, chemistry, biology, computer science)
   - NOT qualified: Social sciences, arts, humanities
2. ELIMINATE UNCERTAINTY: Intended to discover information to eliminate technical uncertainty about development or improvement of product/process
   - Uncertainty about capability, method, or design
3. PROCESS OF EXPERIMENTATION: Substantially all activities constitute systematic trial and error or modeling/simulation
   - Evaluate alternatives to achieve result
4. QUALIFIED PURPOSE: For new/improved function, performance, reliability, or quality
   - NOT qualified: Adaptation of existing product to customer need, duplication of existing product, surveys/studies

QUALIFIED RESEARCH EXPENSES (IRC §41(b)):
1. IN-HOUSE WAGES: W-2 wages paid for qualified services
   - Employees who directly perform, supervise, or directly support research
2. SUPPLY COSTS: Tangible property used in research (consumed or worn out)
   - NOT qualified: Property placed in service (depreciated instead)
3. CONTRACT RESEARCH: 65% of amounts paid to third party for qualified research
   - 100% if payment to qualified research consortium

CREDIT CALCULATION OPTIONS:
REGULAR CREDIT (IRC §41(a)):
- 20% × (current year QREs − base amount)
- Base amount = fixed-base % × average gross receipts (4 prior years)
- Fixed-base %: QREs/gross receipts for 1984-1988 (or startup percentage)

ALTERNATIVE SIMPLIFIED CREDIT (IRC §41(c)(5)):
- 14% × (current year QREs − 50% × average QREs for 3 prior years)
- Easier to compute, no fixed-base percentage needed
- Election binding for year, cannot change

GROSS RECEIPTS TEST:
- Startup companies: Fixed-base % = 3% (first 5 years), then increase
- Consistent method required for gross receipts averaging

PAYROLL TAX ELECTION (IRC §41(h)):
- Qualified small businesses can elect to claim credit against payroll tax
- QSB: Less than $5M gross receipts, no gross receipts more than 5 years ago
- Up to $250,000 credit per year against employer portion of Social Security tax
        """,
        key_factors=[
            "Research activities satisfy all four parts of four-part test",
            "Contemporaneous documentation of research process",
            "Nexus between activities and elimination of technical uncertainty",
            "Process of experimentation clearly documented",
            "Qualified purpose (new/improved function, not customer adaptation)",
            "Proper allocation of wages to qualified research",
            "Supply costs consumed in research (not capitalized property)"
        ],
        primary_authority=[
            "IRC §41 - Credit for increasing research activities",
            "Treas. Reg. §1.41-4 - Qualified research",
            "IRS Pub. 535 - Business Expenses (R&D section)",
            "Rev. Proc. 2000-50 - Streamlined credit claim procedure"
        ],
        burden_holder="Taxpayer must contemporaneously document research activities, four-part test satisfaction, and expense allocation.",
        adversary_position="IRS heavily scrutinizes R&D credits; may challenge four-part test, contemporaneous documentation, or QRE allocation.",
        counter_arguments=[
            "Activities were routine or ordinary adaptation to customer needs",
            "No genuine technical uncertainty existed",
            "Process of experimentation not documented or did not occur",
            "Research relied on social sciences (not technological)",
            "Contemporaneous documentation insufficient",
            "Wages allocated based on post-hoc reconstruction rather than timekeeping"
        ],
        resolution_strategy="Maintain contemporaneous project documentation showing uncertainty, experiments conducted, alternatives evaluated. Use time tracking for wage allocation. Consider engaging R&D credit specialist. File Form 6765.",
        entity_scope=["C_Corporation", "S_Corporation", "Partnership", "Individual_Business"],
        confidence=0.78,
        confidence_stratification=ConfidenceStratification.AGGRESSIVE,
        controlling_precedent="High audit focus; documentation critical",
        issue_category=IssueCategory.BUSINESS_CREDITS,
        credit_type="nonrefundable",
        recapture_risk=False,
        carryover_allowed=True,
        ordering_priority=65
    ),

    # LOW-INCOME HOUSING CREDIT - IRC §42
    DoctrineBlock(
        topic="low_income_housing_credit_requirements",
        keywords=["IRC_42", "LIHTC", "affordable_housing", "qualified_low_income_building", "minimum_set_aside", "applicable_percentage"],
        conclusion_template=[
            "The low-income housing credit under IRC §42 provides a 10-year credit for owners of qualified low-income residential rental property.",
            "Building must satisfy minimum set-aside test (20-50 or 40-60) and rent restrictions.",
            "Credit percentage depends on building type (new construction vs. existing, federally subsidized or not) and applicable federal rate."
        ],
        reasoning_framework="""
IRC §42 incentivizes development and preservation of affordable rental housing through annual credits over 10 years.

QUALIFIED LOW-INCOME BUILDING (IRC §42(c)):
Must satisfy BOTH:
1. MINIMUM SET-ASIDE (IRC §42(g)(1)): Choose one:
   - 20-50 TEST: At least 20% of units occupied by tenants with income ≤ 50% area median
   - 40-60 TEST: At least 40% of units occupied by tenants with income ≤ 60% area median
   - (Average income test also available in some cases)

2. RENT RESTRICTION (IRC §42(g)(2)):
   - Gross rent (including utilities) cannot exceed 30% of imputed income limitation
   - For 20-50: rent ≤ 30% × 50% AMI
   - For 40-60: rent ≤ 30% × 60% AMI

QUALIFIED BASIS (IRC §42(c)):
- Eligible basis × applicable fraction
- Eligible basis: Depreciable basis in low-income units (land excluded)
- Applicable fraction: Lesser of (1) low-income units/total units or (2) low-income sq ft/total sq ft

CREDIT AMOUNT (IRC §42(a)):
- Annual credit = qualified basis × applicable percentage
- Credit claimed each year for 10 years

APPLICABLE PERCENTAGE (IRC §42(b)):
Depends on building type:
- NEW CONSTRUCTION OR REHAB (not federally subsidized): 9% credit (~70% PV)
- ACQUISITION OF EXISTING BUILDING: 4% credit (~30% PV)
- FEDERALLY SUBSIDIZED: 4% credit (~30% PV)
- Exact percentage = present value factor based on applicable federal rate

COMPLIANCE PERIOD (IRC §42(i)):
- 15-year minimum compliance period
- Extended use agreement typically requires 30+ years
- Annual certification of tenant income and rent restrictions

RECAPTURE (IRC §42(j)):
- If building fails to qualify in any year during compliance period, prior credits recaptured
- Recapture = credits claimed × (years remaining/15) + interest
- Dispositions trigger recapture unless qualified contract or foreclosure
        """,
        key_factors=[
            "Minimum set-aside test satisfied (20-50 or 40-60)",
            "Rent restrictions satisfied for all low-income units",
            "Eligible basis correctly calculated (depreciable property only)",
            "Applicable fraction properly determined",
            "Building type determines applicable percentage (9% vs. 4%)",
            "Annual tenant certification and rent documentation",
            "Extended use agreement recorded"
        ],
        primary_authority=[
            "IRC §42 - Low-income housing credit",
            "Treas. Reg. §1.42-5 - Monitoring compliance",
            "Rev. Proc. 2020-49 - Average income test",
            "IRS Pub. 4492 - Information for Tax-Exempt Bonds and LIHTCs"
        ],
        burden_holder="Building owner must annually certify tenant income, rent compliance, and maintain detailed records for entire compliance period.",
        adversary_position="IRS may challenge tenant income certifications, rent calculations, qualified basis, or compliance period violations.",
        counter_arguments=[
            "Tenant income exceeded limits at move-in (income certification flawed)",
            "Rents exceeded 30% of imputed income limitation",
            "Eligible basis included non-qualifying costs (land, permanent financing fees)",
            "Applicable fraction incorrectly calculated",
            "Building disposition triggered recapture",
            "Available unit rule not satisfied (low-income units not continuously available)"
        ],
        resolution_strategy="Engage LIHTC specialist for compliance monitoring. Maintain detailed tenant files (income certifications, rent calculations). Use state housing agency certified software. Obtain annual CPA compliance audit. Record extended use agreement. File Form 8609.",
        entity_scope=["Partnership", "C_Corporation", "S_Corporation"],
        confidence=0.88,
        confidence_stratification=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="Highly regulated; state agency allocation required",
        issue_category=IssueCategory.INVESTMENT_CREDITS,
        credit_type="nonrefundable",
        recapture_risk=True,
        carryover_allowed=True,
        ordering_priority=70
    ),

    # CLEAN VEHICLE CREDIT - IRC §30D
    DoctrineBlock(
        topic="clean_vehicle_credit_new_vehicles",
        keywords=["IRC_30D", "EV_credit", "electric_vehicle", "plug_in_electric", "clean_vehicle", "critical_minerals", "battery_components"],
        conclusion_template=[
            "The clean vehicle credit under IRC §30D provides up to $7,500 for purchase of new qualified plug-in electric vehicles.",
            "Credit amount depends on battery components and critical minerals sourced from North America ($3,750 each component).",
            "Strict requirements on MSRP caps, income limits, final assembly in North America, and manufacturer caps removed."
        ],
        reasoning_framework="""
IRC §30D (as amended by Inflation Reduction Act 2022) provides credit for new clean vehicles meeting domestic content and price/income requirements.

NEW CLEAN VEHICLE REQUIREMENTS (IRC §30D(d)):
1. FINAL ASSEMBLY: Final assembly in North America (VIN determines location)
2. BATTERY CAPACITY: At least 7 kilowatt hours
3. VEHICLE CLASSIFICATION: Less than 14,000 pounds gross vehicle weight
4. ORIGINAL USE: Acquired for use or lease, not for resale
5. SELLER REGISTRATION: Dealer registered with IRS for point-of-sale credit transfer

MSRP LIMITATIONS (IRC §30D(f)):
- VANS/SUVs/TRUCKS: $80,000 or less
- OTHER VEHICLES: $55,000 or less
- Based on manufacturer's suggested retail price

INCOME LIMITATIONS (IRC §30D(f)):
Modified AGI cannot exceed:
- JOINT: $300,000
- HEAD OF HOUSEHOLD: $225,000
- SINGLE: $150,000
- Based on year of purchase or prior year (whichever lower)

CREDIT AMOUNT (IRC §30D(a), (b)):
BASE: Up to $7,500, comprised of TWO components:
1. CRITICAL MINERALS ($3,750): If applicable % of critical minerals extracted/processed in U.S. or FTA country
   - 2024: 50% | 2025: 60% | 2026: 70% | 2027+: 80%
2. BATTERY COMPONENTS ($3,750): If applicable % of battery components manufactured/assembled in North America
   - 2024: 60% | 2025: 70% | 2026: 80% | 2027+: 90%

FOREIGN ENTITY OF CONCERN (IRC §30D(d)(7)):
- No credit if battery components manufactured by FEOC (China, Russia, North Korea, Iran)
- Applies to battery components after 2023, critical minerals after 2024

MANUFACTURER CAP REMOVED:
- Prior 200,000-vehicle cap per manufacturer repealed for purchases after 8/16/2022

TRANSFER TO DEALER (IRC §30D(g)):
- Taxpayer can elect to transfer credit to dealer at point of sale
- Dealer provides instant discount, claims credit on return
- Simplifies process and provides immediate benefit

USED CLEAN VEHICLE CREDIT (IRC §25E):
- Separate credit up to $4,000 (30% of sale price) for qualifying used EVs
- Income limits lower, MSRP cap $25,000, previous owner restriction
        """,
        key_factors=[
            "Vehicle final assembly in North America (VIN starts with 1, 4, or 5)",
            "MSRP under $55,000 (cars) or $80,000 (SUVs/trucks/vans)",
            "Taxpayer modified AGI under limits ($150K/$225K/$300K)",
            "Critical minerals percentage requirement satisfied",
            "Battery components percentage requirement satisfied",
            "No battery components from foreign entity of concern",
            "Dealer registered for credit transfer (if electing transfer)"
        ],
        primary_authority=[
            "IRC §30D - Clean vehicle credit",
            "IRS Notice 2023-1 - Critical minerals and battery components",
            "IRS Notice 2023-16 - Transfer to dealer",
            "IRS Notice 2022-56 - Final assembly requirement",
            "Department of Energy VIN decoder - fueleconomy.gov"
        ],
        burden_holder="Taxpayer must verify vehicle qualifies (MSRP, final assembly, critical minerals/battery components) and income limits satisfied.",
        adversary_position="IRS may challenge MSRP verification, income calculation, or that vehicle met critical minerals/battery components thresholds.",
        counter_arguments=[
            "Vehicle final assembly not in North America (VIN check failed)",
            "MSRP exceeded limit (dealer options/packages pushed over)",
            "Modified AGI exceeded threshold in purchase year or prior year",
            "Critical minerals or battery components percentages not met",
            "Battery components manufactured by foreign entity of concern",
            "Vehicle purchased for resale rather than personal use"
        ],
        resolution_strategy="Use Department of Energy VIN decoder to verify final assembly. Obtain dealer certification of MSRP and critical minerals/battery components compliance. Calculate modified AGI for both purchase year and prior year. Consider electing transfer to dealer for immediate benefit. File Form 8936.",
        entity_scope=["Individual", "Married_Filing_Jointly"],
        confidence=0.85,
        confidence_stratification=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="Rapidly evolving guidance; verify current percentages and FEOC rules",
        issue_category=IssueCategory.ENERGY_CREDITS,
        credit_type="nonrefundable",
        recapture_risk=False,
        carryover_allowed=False,
        ordering_priority=40
    ),

    # WORK OPPORTUNITY TAX CREDIT - IRC §51
    DoctrineBlock(
        topic="work_opportunity_tax_credit_target_groups",
        keywords=["IRC_51", "WOTC", "work_opportunity", "target_groups", "qualified_wages", "certification_requirement"],
        conclusion_template=[
            "The work opportunity tax credit under IRC §51 provides a credit for hiring individuals from targeted groups facing barriers to employment.",
            "Credit is generally 40% of first $6,000 in wages (up to $2,400 per employee), or 25% if employee works 120-399 hours.",
            "Certification from state workforce agency required before or shortly after hire date."
        ],
        reasoning_framework="""
IRC §51 incentivizes hiring from disadvantaged groups through wage-based credits, subject to certification requirements.

TARGET GROUPS (IRC §51(d)):
10 targeted groups:
1. QUALIFIED IV-A RECIPIENT: TANF recipient
2. QUALIFIED VETERAN: Veteran in specific categories (disabled, unemployed, food stamps)
3. QUALIFIED EX-FELON: Convicted felon hired within 1 year of conviction or release
4. DESIGNATED COMMUNITY RESIDENT (DCR): Age 18-39 living in empowerment zone or rural renewal county
5. VOCATIONAL REHABILITATION REFERRAL: Has disability, referred by approved agency
6. SUMMER YOUTH EMPLOYEE: Age 16-17, DCR, employed 5/1-9/15
7. QUALIFIED SNAP RECIPIENT: Age 18-39, SNAP recipient for 6+ months
8. QUALIFIED SSI RECIPIENT: SSI recipient
9. LONG-TERM FAMILY ASSISTANCE RECIPIENT: TANF for 18+ months
10. QUALIFIED LONG-TERM UNEMPLOYMENT RECIPIENT: Unemployed 27+ weeks, received unemployment compensation

CREDIT CALCULATION (IRC §51(a), (b)):
STANDARD CREDIT:
- 40% of qualified first-year wages (up to $6,000) = max $2,400
- Requires 400+ hours of service
- 25% if 120-399 hours of service = max $1,500

ENHANCED CREDITS:
- Long-term family assistance recipient: 50% of first $10,000 first-year wages + 50% of first $10,000 second-year wages
  Max $10,000 total over two years
- Qualified veteran categories: Up to $9,600 (40% × $24,000 for disabled unemployed veteran)

QUALIFIED WAGES (IRC §51(c)):
- Wages subject to FUTA (Federal Unemployment Tax Act)
- First-year wages during 1-year period beginning with hire date
- Reduced by work supplementation payments

CERTIFICATION REQUIREMENT (IRC §51(d)(13)):
- Must request certification from state workforce agency (SWA)
- IRS Form 8850 filed with SWA within 28 days of hire
- ETA Form 9061 or 9062 submitted
- No credit allowed without certification (strict requirement)

AGGREGATION RULES (IRC §52):
- Controlled group members aggregate for credit purposes
- Prevents gaming by shifting employees between related entities

DEDUCTION REDUCTION (IRC §280C(a)):
- Wage deduction reduced by amount of WOTC claimed
- Election to claim reduced credit and full deduction available
        """,
        key_factors=[
            "Employee is member of qualifying target group",
            "Certification requested within 28 days of hire (Form 8850)",
            "State workforce agency issued certification",
            "Employee worked required hours (120 or 400 depending on credit %)",
            "Qualified wages properly calculated (FUTA wages)",
            "No duplication with other wage credits (e.g., empowerment zone credit)",
            "Wage deduction reduced by credit amount"
        ],
        primary_authority=[
            "IRC §51 - Work opportunity credit",
            "IRC §51(d)(13) - Certification requirement",
            "Treas. Reg. §1.51-1 - Work opportunity credit",
            "IRS Form 8850 - Pre-Screening Notice",
            "DOL ETA Form 9061/9062 - Certification request"
        ],
        burden_holder="Employer must timely request certification and obtain state workforce agency approval; no credit without certification.",
        adversary_position="IRS may challenge late certification filing, insufficient documentation of target group membership, or hours calculation.",
        counter_arguments=[
            "Certification request filed after 28-day deadline (no credit allowed)",
            "State workforce agency denied certification",
            "Employee did not meet target group criteria",
            "Hours of service overstated or not documented",
            "Wages claimed include non-FUTA wages",
            "Wage deduction not reduced by credit amount"
        ],
        resolution_strategy="Implement hiring process to identify WOTC-eligible candidates at application/interview stage. File Form 8850 within 28 days without exception. Maintain detailed time records. Track certification status. Use Form 5884 to claim credit.",
        entity_scope=["C_Corporation", "S_Corporation", "Partnership", "Individual_Business"],
        confidence=0.91,
        confidence_stratification=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="Certification is absolute requirement; no exceptions for late filing",
        issue_category=IssueCategory.EMPLOYMENT_CREDITS,
        credit_type="nonrefundable",
        recapture_risk=False,
        carryover_allowed=True,
        ordering_priority=55
    ),

    # REHABILITATION CREDIT - IRC §47
    DoctrineBlock(
        topic="rehabilitation_credit_historic_structures",
        keywords=["IRC_47", "historic_rehabilitation", "certified_historic_structure", "qualified_rehabilitation_expenditures", "20_percent_credit"],
        conclusion_template=[
            "The rehabilitation credit under IRC §47 provides a 20% credit for qualified rehabilitation expenditures on certified historic structures.",
            "Building must be listed on National Register or in registered historic district and certified by National Park Service.",
            "Credit claimed ratably over 5 years; substantial rehabilitation test requires expenditures exceed greater of $5,000 or adjusted basis."
        ],
        reasoning_framework="""
IRC §47 incentivizes preservation of historic buildings through credits for qualified rehabilitation expenditures.

CERTIFIED HISTORIC STRUCTURE (IRC §47(c)(3)):
Building that is:
1. Listed individually on National Register of Historic Places, OR
2. Located in registered historic district AND certified by Secretary of Interior as contributing to historic significance of district

QUALIFIED REHABILITATION EXPENDITURE (IRC §47(c)(2)):
Amounts chargeable to capital account:
- For property (or addition/improvement) with depreciable life of 27.5+ years
- In connection with certified rehabilitation of certified historic structure
- NOT QUALIFIED: Acquisition cost, enlargement, new construction

CERTIFIED REHABILITATION (IRC §47(c)(2)(C)):
- Rehabilitation plan approved by Secretary of Interior (National Park Service)
- Meets Secretary of Interior's Standards for Rehabilitation
- Substantially preserves historic character and significant features

SUBSTANTIAL REHABILITATION TEST (IRC §47(c)(1)(C)):
QREs during 24-month measuring period must EXCEED greater of:
1. Adjusted basis of building and structural components, OR
2. $5,000

Measuring period: 24-month period selected by taxpayer, or 60 months for phased rehabilitation.

CREDIT AMOUNT (IRC §47(a)):
- 20% of qualified rehabilitation expenditures
- Claimed ratably over 5-year period (4% per year)
- Placed-in-service date begins 5-year credit period

BASIS REDUCTION (IRC §50(c)):
- Basis of property reduced by 100% of rehabilitation credit claimed
- Effectively reduces depreciation deductions

RECAPTURE (IRC §50(a)):
- If property disposed of or ceases to be qualified property before end of 5-year recapture period, credit recaptured
- Recapture % = 100% (year 1), 80% (year 2), 60% (year 3), 40% (year 4), 20% (year 5)

PLACED-IN-SERVICE REQUIREMENT:
- Credit claimed in year property placed in service
- For phased rehabilitation, each phase treated separately

COORDINATION WITH OTHER CREDITS:
- Part of investment credit (IRC §46)
- Included in general business credit (IRC §38)
- Subject to GBC limitation and carryover rules
        """,
        key_factors=[
            "Building is certified historic structure (listed or contributing)",
            "Rehabilitation certified by National Park Service",
            "Expenditures meet Secretary of Interior's Standards",
            "Substantial rehabilitation test satisfied (QREs > basis or $5,000)",
            "24-month measuring period properly selected",
            "Property has depreciable life of 27.5+ years (residential or nonresidential)",
            "Basis reduced by credit amount"
        ],
        primary_authority=[
            "IRC §47 - Rehabilitation credit",
            "IRC §47(c)(2)(C) - Certified rehabilitation",
            "Treas. Reg. §1.48-12 - Qualified rehabilitation expenditures",
            "36 CFR Part 67 - Secretary of Interior's Standards",
            "National Park Service Technical Preservation Services"
        ],
        burden_holder="Taxpayer must obtain National Park Service certification of structure and rehabilitation plan before claiming credit.",
        adversary_position="IRS may challenge structure certification, rehabilitation plan approval, substantial rehabilitation test, or that expenditures met Standards.",
        counter_arguments=[
            "Building not certified as historic structure or contributing to district",
            "Rehabilitation not certified by National Park Service",
            "Expenditures did not meet Secretary of Interior's Standards",
            "Substantial rehabilitation test failed (QREs did not exceed basis)",
            "Expenditures include non-qualifying costs (acquisition, enlargement)",
            "Property disposed of during 5-year recapture period"
        ],
        resolution_strategy="Engage historic preservation consultant. Submit Part 1 (structure certification) and Part 2 (rehabilitation plan) to National Park Service before beginning work. Maintain detailed construction records. Submit Part 3 (certification of completed work) before claiming credit. File Form 3468.",
        entity_scope=["C_Corporation", "S_Corporation", "Partnership", "Individual_Business"],
        confidence=0.89,
        confidence_stratification=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="National Park Service certification required; strict adherence to Standards",
        issue_category=IssueCategory.INVESTMENT_CREDITS,
        credit_type="nonrefundable",
        recapture_risk=True,
        carryover_allowed=True,
        ordering_priority=75
    ),

    # RENEWABLE ELECTRICITY PRODUCTION CREDIT - IRC §45
    DoctrineBlock(
        topic="renewable_electricity_production_credit",
        keywords=["IRC_45", "PTC", "production_tax_credit", "renewable_energy", "wind_credit", "solar_credit", "qualified_facility"],
        conclusion_template=[
            "The renewable electricity production credit under IRC §45 provides a per-kilowatt-hour credit for electricity produced from qualified energy resources.",
            "Credit amount varies by technology (wind, solar, geothermal, biomass, etc.) and is inflation-adjusted annually.",
            "Facility must begin construction before deadline and credit claimed during 10-year period from placed-in-service date."
        ],
        reasoning_framework="""
IRC §45 incentivizes renewable electricity generation through production-based credits over 10-year period.

QUALIFIED FACILITIES (IRC §45(d)):
Facility that produces electricity from qualified energy resources:
- WIND: Onshore or offshore wind facility
- CLOSED-LOOP BIOMASS: Organic material from dedicated energy crop
- OPEN-LOOP BIOMASS: Agricultural livestock waste, biomass burned in conjunction with fossil fuel
- GEOTHERMAL: Geothermal energy
- SOLAR: Solar energy (but see IRC §48 investment credit election)
- SMALL IRRIGATION POWER: Generating capacity ≤ 5 MW
- MUNICIPAL SOLID WASTE: Landfill gas, trash combustion
- QUALIFIED HYDROPOWER: Incremental hydropower, marine and hydrokinetic
- OTHER: Tidal, wave, ocean thermal

BEGIN CONSTRUCTION DEADLINE (IRC §45(d)):
Varies by facility type; most expired 2021 but Inflation Reduction Act extended/modified:
- Technology-neutral credit under IRC §45Y for facilities beginning construction after 2024
- Transitional rules for facilities beginning construction before 2025

CREDIT AMOUNT (IRC §45(a), (b)):
BASE AMOUNT (inflation-adjusted annually):
- Wind, closed-loop biomass, geothermal: 2.75¢/kWh (2024: ~2.7¢/kWh indexed)
- Other technologies: Reduced rates (0.5× to 1.0× base amount)

INCREASED CREDIT (IRC §45(b)(6), (b)(7)):
- 5× MULTIPLIER if prevailing wage and apprenticeship requirements satisfied
- Without wage/apprenticeship: credit reduced to 20% of full amount (1/5)

BONUS CREDITS (IRC §45(b)(9)):
- 10% bonus if facility in energy community (brownfield, coal closure area, fossil fuel employment area)
- 10% bonus if domestic content requirements satisfied

CREDIT PERIOD:
- 10-year period beginning on placed-in-service date
- Credit claimed annually based on actual kWh production

REDUCTION FOR GRANTS/SUBSIDIES (IRC §45(b)(3)):
- Credit reduced by subsidized energy financing, tax-exempt bonds, certain grants

ELECTION OF INVESTMENT CREDIT (IRC §48(a)(5)):
- Taxpayer may elect to claim investment credit (IRC §48) instead of production credit
- Election irrevocable once made
- Strategic choice based on project economics

QUALIFIED SALE REQUIREMENT (IRC §45(c)(3)(A)):
- Electricity must be SOLD to unrelated person
- Production for own use does not qualify
        """,
        key_factors=[
            "Facility produces electricity from qualified energy resource",
            "Begin construction before deadline (or qualify for IRC §45Y)",
            "Electricity sold to unrelated person (not self-consumption)",
            "Prevailing wage and apprenticeship requirements satisfied for 5× multiplier",
            "Actual kWh production documented annually",
            "Reduction for subsidized financing or grants properly calculated",
            "Election to claim investment credit (IRC §48) instead if more beneficial"
        ],
        primary_authority=[
            "IRC §45 - Renewable electricity production credit",
            "IRC §45(b)(6), (b)(7) - Prevailing wage and apprenticeship",
            "IRS Notice 2013-29 - Beginning of construction safe harbors",
            "IRS Notice 2018-59 - Continuity safe harbor",
            "Inflation Reduction Act §13101 - Extension and modification"
        ],
        burden_holder="Taxpayer must document beginning of construction, placed-in-service date, kWh production, sales to unrelated persons, and wage/apprenticeship compliance.",
        adversary_position="IRS may challenge beginning of construction date, continuous construction/efforts, kWh measurement, or wage/apprenticeship compliance.",
        counter_arguments=[
            "Begin construction deadline missed (physical work or 5% safe harbor not met)",
            "Continuous construction/efforts requirement failed (Notice 2018-59)",
            "Electricity not sold to unrelated person (self-consumption)",
            "Prevailing wage or apprenticeship requirements not satisfied",
            "kWh production overstated or not properly metered",
            "Credit reduced by subsidized financing not properly accounted for"
        ],
        resolution_strategy="Document beginning of construction with physical work or 5% safe harbor evidence. Implement prevailing wage and apprenticeship compliance program. Install calibrated metering equipment certified by independent engineer. Maintain sales contracts to unrelated persons. Consider ITC vs. PTC election based on project economics. File Form 8835.",
        entity_scope=["C_Corporation", "S_Corporation", "Partnership", "Individual_Business"],
        confidence=0.82,
        confidence_stratification=ConfidenceStratification.AGGRESSIVE,
        controlling_precedent="Rapidly evolving area; transitional rules complex; wage/apprenticeship requirements add compliance burden",
        issue_category=IssueCategory.ENERGY_CREDITS,
        credit_type="nonrefundable",
        recapture_risk=False,
        carryover_allowed=True,
        ordering_priority=80
    ),

    # ENERGY INVESTMENT CREDIT - IRC §48
    DoctrineBlock(
        topic="energy_investment_credit_qualified_property",
        keywords=["IRC_48", "ITC", "investment_tax_credit", "solar_energy", "energy_property", "basis_credit", "prevailing_wage"],
        conclusion_template=[
            "The energy investment credit under IRC §48 provides a percentage credit based on the basis of qualified energy property.",
            "Credit rate is 6% or 30% depending on satisfaction of prevailing wage and apprenticeship requirements.",
            "Eligible technologies include solar, fuel cell, small wind, geothermal, microturbine, and combined heat and power."
        ],
        reasoning_framework="""
IRC §48 provides upfront investment-based credit for specified energy property placed in service.

ENERGY PROPERTY (IRC §48(a)(3)):
Qualified property includes:
- Solar energy property (equipment using solar energy to generate electricity, heat/cool structure, provide hot water, provide solar process heat, illuminate, provide composition of fuel)
- Fuel cell property (integrated system that generates electricity using electrochemical process)
- Small wind energy property (turbine with capacity ≤ 100 kW)
- Geothermal energy property (equipment generating electricity from geothermal deposits)
- Microturbine property (stationary system <2 MW using combustion turbine)
- Combined heat and power system property (CHP generating electricity and useful thermal energy)
- Geothermal heat pump property
- Qualified small wind property
- Waste energy recovery property
- Energy storage technology (beginning 2023)

CREDIT PERCENTAGE (IRC §48(a)(2)):
BASE RATE: 6% of energy property basis
INCREASED RATE: 30% if prevailing wage and apprenticeship requirements satisfied (5× multiplier)

BEGINNING CONSTRUCTION REQUIREMENT:
- Property must begin construction before applicable deadline
- Inflation Reduction Act extended through 2024; technology-neutral credit (IRC §48E) for facilities beginning construction after 2024

BONUS CREDITS (IRC §48(a)(10), (a)(11)):
- 10% bonus if facility in energy community
- 10% bonus if domestic content requirements satisfied
- Bonuses apply to increased credit rate (30% becomes 33% or 36%)

PREVAILING WAGE AND APPRENTICESHIP (IRC §48(a)(9)):
PREVAILING WAGE:
- Laborers and mechanics paid wages at rates not less than prevailing for construction, alteration, or repair
- Davis-Bacon wage determinations apply
APPRENTICESHIP:
- Minimum labor hours performed by qualified apprentices:
  - 2023: 12.5% | 2024: 15%
- Good faith effort exception if insufficient apprentices available

COORDINATION WITH PTC:
- Taxpayer may elect production credit (IRC §45) instead of investment credit for certain property
- Election irrevocable

BASIS REDUCTION (IRC §50(c)):
- Basis reduced by 50% of credit claimed
- Reduces future depreciation deductions

RECAPTURE (IRC §50(a)):
- If property ceases to qualify or is disposed of before end of 5-year recapture period, credit recaptured
- Recapture % = 100% (year 1), 80% (year 2), 60% (year 3), 40% (year 4), 20% (year 5)

PROGRESS EXPENDITURES (IRC §46(d)):
- Taxpayer may elect to claim credit on progress expenditures for property with construction period ≥ 2 years
- Credit claimed as expenditures made rather than waiting for placed-in-service
        """,
        key_factors=[
            "Property is energy property under IRC §48(a)(3)",
            "Begin construction before deadline",
            "Prevailing wage and apprenticeship requirements satisfied for 30% rate",
            "Property placed in service during taxable year",
            "Basis properly calculated (exclude non-qualifying costs)",
            "Bonus credits for energy community or domestic content if applicable",
            "Basis reduced by 50% of credit claimed"
        ],
        primary_authority=[
            "IRC §48 - Energy investment credit",
            "IRC §48(a)(9) - Prevailing wage and apprenticeship",
            "IRS Notice 2013-29 - Beginning of construction",
            "IRS Notice 2022-61 - Prevailing wage and apprenticeship guidance",
            "Inflation Reduction Act §13102 - Extension and modification"
        ],
        burden_holder="Taxpayer must document energy property qualification, beginning of construction, placed-in-service date, basis, and wage/apprenticeship compliance.",
        adversary_position="IRS may challenge energy property status, begin construction date, prevailing wage compliance, or basis calculation.",
        counter_arguments=[
            "Property does not meet definition of energy property",
            "Begin construction deadline missed",
            "Prevailing wage rates not satisfied (underpayment to laborers/mechanics)",
            "Apprenticeship requirements failed (insufficient apprentice hours)",
            "Basis includes non-qualifying costs",
            "Property ceased to qualify during 5-year recapture period"
        ],
        resolution_strategy="Engage wage compliance specialist. Implement certified payroll reporting. Document apprenticeship hour requirements and good faith efforts. Obtain independent engineer certification of energy property status. Consider PTC vs. ITC election. File Form 3468.",
        entity_scope=["C_Corporation", "S_Corporation", "Partnership", "Individual_Business"],
        confidence=0.84,
        confidence_stratification=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="Wage/apprenticeship compliance critical for 30% rate; documentation intensive",
        issue_category=IssueCategory.ENERGY_CREDITS,
        credit_type="nonrefundable",
        recapture_risk=True,
        carryover_allowed=True,
        ordering_priority=70
    ),

    # ADOPTION CREDIT - IRC §23
    DoctrineBlock(
        topic="adoption_credit_qualified_expenses",
        keywords=["IRC_23", "adoption_credit", "qualified_adoption_expenses", "special_needs_child", "employer_adoption_assistance"],
        conclusion_template=[
            "The adoption credit under IRC §23 provides a credit for qualified adoption expenses up to $15,950 per child (2023).",
            "For special needs children, full credit allowed even if actual expenses are less.",
            "Credit phases out for higher-income taxpayers and is partially refundable for certain foreign adoptions."
        ],
        reasoning_framework="""
IRC §23 provides credit to offset costs of adopting children, with enhanced benefits for special needs adoptions.

QUALIFIED ADOPTION EXPENSES (IRC §23(d)(1)):
Reasonable and necessary adoption fees, court costs, attorney fees, traveling expenses, and other expenses:
- Directly related to legal adoption of eligible child
- Not incurred in violation of state or federal law
- Not reimbursed by employer or otherwise

ELIGIBLE CHILD (IRC §23(d)(2)):
- Individual under age 18, OR
- Physically or mentally incapable of self-care

SPECIAL NEEDS CHILD (IRC §23(d)(3)):
Child who:
- Is U.S. citizen or resident
- State determines cannot/should not be returned to parents' home
- State determines child cannot be placed for adoption without assistance due to specific factor or condition

CREDIT AMOUNT (IRC §23(a)):
- Lesser of (1) qualified adoption expenses or (2) $15,950 per child (indexed for inflation)
- SPECIAL NEEDS: Full $15,950 allowed regardless of actual expenses
- Per-child limit applies even if adoption spans multiple years

TIMING OF CREDIT (IRC §23(a)):
DOMESTIC ADOPTION:
- Expenses paid before finalization: Credit in year following payment
- Expenses paid in/after year of finalization: Credit in year paid

FOREIGN ADOPTION:
- All expenses: Credit in year adoption becomes final
- No credit until finalization (may wait years)

PHASE-OUT (IRC §23(b)):
- Begins: MAGI $239,230 (2023, indexed)
- Fully phased out: MAGI $279,230
- Reduction: Credit × (MAGI − $239,230) / $40,000

COORDINATION WITH EMPLOYER ASSISTANCE (IRC §137):
- Employer-provided adoption assistance (up to $15,950) excludable from income
- Cannot claim credit for same expenses excluded under employer plan
- Combined credit + exclusion cannot exceed $15,950 per child

CARRYFORWARD (IRC §23(c)):
- Unused credit carried forward 5 years
- No carryback

FAILED ADOPTION:
- If adoption not finalized, expenses up to year of finalization still qualify
- Expenses for same child in subsequent successful adoption combined with prior expenses for per-child limit
        """,
        key_factors=[
            "Child is eligible child (under 18 or disabled)",
            "Expenses are qualified adoption expenses (legal, necessary, direct)",
            "Special needs determination by state (if applicable)",
            "Timing of credit claim (domestic vs. foreign, before/after finalization)",
            "MAGI within phase-out range",
            "Coordination with employer-provided adoption assistance",
            "Per-child limit ($15,950) not exceeded"
        ],
        primary_authority=[
            "IRC §23 - Adoption credit",
            "IRC §137 - Adoption assistance programs",
            "Treas. Reg. §1.23-1 - Adoption credit",
            "IRS Pub. 968 - Tax Benefits for Adoption",
            "Form 8839 - Qualified Adoption Expenses"
        ],
        burden_holder="Taxpayer must substantiate qualified adoption expenses, eligible child status, special needs determination (if applicable), and finalization date.",
        adversary_position="IRS may challenge expense qualification, timing of credit claim, special needs determination, or that expenses were reimbursed.",
        counter_arguments=[
            "Expenses not directly related to legal adoption (pre-adoption counseling, fertility treatments)",
            "Expenses incurred in violation of law (payment to birth mother beyond allowed)",
            "Special needs determination not issued by state",
            "Foreign adoption expenses claimed before finalization",
            "Employer reimbursement not properly accounted for",
            "Per-child limit exceeded by claiming same expenses multiple years"
        ],
        resolution_strategy="Maintain detailed adoption expense records with receipts, legal invoices, and court documents. Obtain state special needs determination in writing. Track finalization date carefully for timing. Coordinate with employer adoption assistance plan. File Form 8839.",
        entity_scope=["Individual", "Married_Filing_Jointly"],
        confidence=0.92,
        confidence_stratification=ConfidenceStratification.DEFENSIBLE,
        issue_category=IssueCategory.INDIVIDUAL_CREDITS,
        credit_type="nonrefundable",
        recapture_risk=False,
        carryover_allowed=True,
        ordering_priority=28
    ),

    # ELDERLY OR DISABLED CREDIT - IRC §22
    DoctrineBlock(
        topic="elderly_disabled_credit_eligibility",
        keywords=["IRC_22", "elderly_credit", "disabled_credit", "retirement_income", "social_security_benefits"],
        conclusion_template=[
            "The credit for elderly or disabled under IRC §22 provides a limited credit for low-income elderly or permanently disabled taxpayers.",
            "Maximum credit is $7,500 for joint filers both over 65, reduced by nontaxable Social Security and excess AGI.",
            "Credit rarely claimed due to low income thresholds and Social Security offset."
        ],
        reasoning_framework="""
IRC §22 provides a credit for elderly or disabled individuals with limited income, but Social Security benefits typically eliminate the credit.

ELIGIBILITY (IRC §22(b)):
Must satisfy ONE of:
1. AGE 65 OR OLDER: Taxpayer (or spouse if joint) age 65 before close of taxable year
2. PERMANENTLY AND TOTALLY DISABLED:
   - Unable to engage in substantial gainful activity
   - Due to medically determinable physical or mental impairment
   - Expected to result in death or last continuously for 12+ months
   - Retired on permanent and total disability
   - Physician certification required

INITIAL AMOUNT (IRC §22(c)(2)):
Varies by filing status:
- SINGLE (65+ or disabled): $5,000
- JOINT (one spouse 65+ or disabled): $5,000
- JOINT (both spouses 65+ or disabled): $7,500
- MARRIED FILING SEPARATELY (live apart entire year): $3,750

REDUCTION FOR NONTAXABLE BENEFITS (IRC §22(c)(3)(A)):
Initial amount reduced by:
- Nontaxable Social Security benefits
- Nontaxable railroad retirement benefits (Tier 1)
- Nontaxable pension/annuity/disability benefits under federal law

REDUCTION FOR EXCESS AGI (IRC §22(c)(3)(B)):
Initial amount (after benefit reduction) reduced by 50% of AGI over:
- SINGLE: $7,500
- JOINT: $10,000
- MARRIED FILING SEPARATELY: $5,000

CREDIT CALCULATION:
- Credit = 15% of (initial amount − reductions)
- Maximum credit: $1,125 (if joint with both spouses 65+ and no reductions)

PERMANENT AND TOTAL DISABILITY CERTIFICATION:
- Must have physician's statement certifying:
  - Nature of impairment
  - Impairment renders person unable to engage in substantial gainful activity
  - Impairment expected to result in death or be of long-continued and indefinite duration
- If under 65, must have received taxable disability income during year
        """,
        key_factors=[
            "Taxpayer (or spouse) age 65+ or permanently and totally disabled",
            "Physician certification obtained (if claiming under disability)",
            "Nontaxable Social Security or pension benefits (typically eliminate credit)",
            "AGI within low thresholds ($7,500-$10,000)",
            "Taxable disability income received (if under 65 and disabled)",
            "Filing status determines initial amount and AGI threshold"
        ],
        primary_authority=[
            "IRC §22 - Credit for elderly or disabled",
            "Treas. Reg. §1.22-1 - Credit for elderly or disabled",
            "IRS Pub. 524 - Credit for Elderly or Disabled",
            "Schedule R - Credit for Elderly or Disabled"
        ],
        burden_holder="Taxpayer must substantiate age or disability status, nontaxable benefit amounts, and AGI.",
        adversary_position="IRS may challenge permanent and total disability determination or calculation of nontaxable benefits.",
        counter_arguments=[
            "Taxpayer under 65 and not permanently and totally disabled",
            "Physician certification insufficient or missing",
            "Disability not preventing substantial gainful activity",
            "Nontaxable Social Security benefits underreported (reduces credit)",
            "AGI exceeds threshold (credit fully eliminated)"
        ],
        resolution_strategy="Obtain physician's statement certifying permanent and total disability. Verify nontaxable Social Security benefits from SSA-1099. Calculate AGI reduction carefully. File Schedule R. Note: Credit rarely beneficial due to Social Security offset.",
        entity_scope=["Individual", "Married_Filing_Jointly", "Married_Filing_Separately"],
        confidence=0.93,
        confidence_stratification=ConfidenceStratification.DEFENSIBLE,
        issue_category=IssueCategory.INDIVIDUAL_CREDITS,
        credit_type="nonrefundable",
        recapture_risk=False,
        carryover_allowed=False,
        ordering_priority=45
    ),

    # CARBON CAPTURE CREDIT - IRC §45Q
    DoctrineBlock(
        topic="carbon_capture_sequestration_credit",
        keywords=["IRC_45Q", "carbon_capture", "CCS", "CCUS", "carbon_sequestration", "qualified_facility", "secure_geological_storage"],
        conclusion_template=[
            "The carbon oxide sequestration credit under IRC §45Q provides per-ton credits for carbon capture and sequestration or utilization.",
            "Credit amounts vary based on use (sequestration, EOR, or utilization) and whether prevailing wage requirements satisfied.",
            "Facility must capture minimum annual tonnage (12,500-500,000 metric tons depending on facility type) to qualify."
        ],
        reasoning_framework="""
IRC §45Q incentivizes carbon capture, utilization, and storage technologies through production-based credits.

QUALIFIED FACILITY (IRC §45Q(d)):
Equipment that:
- Captures carbon oxide from industrial source or directly from atmosphere (DAC)
- Meets minimum capture threshold during taxable year:
  - ELECTRIC GENERATING: 500,000 metric tons/year
  - OTHER INDUSTRIAL: 100,000 metric tons/year (12,500 for facilities beginning construction before 2/9/2018)
  - DIRECT AIR CAPTURE: 1,000 metric tons/year

QUALIFIED CARBON OXIDE (IRC §45Q(c)):
Carbon oxide captured at qualified facility that would otherwise be released into atmosphere.

CREDIT AMOUNT PER METRIC TON (IRC §45Q(a)):
Varies by disposition and wage compliance:

BASE AMOUNTS (without prevailing wage/apprenticeship):
- Sequestration in secure geological storage: $12 (2024, indexed)
- Enhanced oil or gas recovery (EOR): $6 (2024)
- Utilization: $12 (2024)

INCREASED AMOUNTS (with prevailing wage/apprenticeship):
- Sequestration: $60 (5× multiplier)
- EOR: $30
- Utilization: $60
- Direct air capture + sequestration: $130
- Direct air capture + EOR/utilization: $75

SECURE GEOLOGICAL STORAGE (IRC §45Q(f)(2)):
Storage of carbon oxide in deep saline formations or oil/gas reservoirs such that it:
- Will not escape into atmosphere
- Complies with EPA Underground Injection Control regulations
- Monitored and verified (EPA reporting required)

UTILIZATION (IRC §45Q(f)(5)):
Carbon oxide:
- Fixed in goods or services through chemical conversion
- Used as tertiary injectant in EOR
- Not including use as working fluid

CREDIT PERIOD:
- 12-year period beginning when facility placed in service
- Annual election of credit amount based on actual capture/disposition

PREVAILING WAGE AND APPRENTICESHIP (IRC §45Q(a)(4)):
Same requirements as IRC §45/§48:
- Laborers/mechanics paid prevailing wages
- Minimum % of labor hours by qualified apprentices (increasing from 12.5% to 15%)

RECAPTURE (IRC §45Q(f)(4)):
If sequestered carbon oxide escapes or utilized carbon oxide ceases to be utilized within 3 years, credit recaptured.

DIRECT PAY ELECTION (IRC §6417):
- Applicable entities can elect to receive refundable credit (direct pay)
- Includes tax-exempt organizations, state/local governments
        """,
        key_factors=[
            "Facility captures minimum annual tonnage threshold",
            "Carbon oxide disposed through sequestration, EOR, or utilization",
            "Secure geological storage requirements satisfied (if sequestration)",
            "Prevailing wage and apprenticeship requirements satisfied for 5× multiplier",
            "Annual carbon oxide capture and disposition documented",
            "EPA reporting compliance (for sequestration)",
            "Monitoring and verification protocols in place"
        ],
        primary_authority=[
            "IRC §45Q - Credit for carbon oxide sequestration",
            "IRC §45Q(f) - Secure geological storage and utilization definitions",
            "IRS Notice 2020-12 - Secure geological storage guidance",
            "IRS Notice 2023-18 - Prevailing wage and apprenticeship",
            "EPA Subpart RR - Geologic Sequestration of CO2"
        ],
        burden_holder="Taxpayer must document capture volumes, disposition method, secure storage compliance, and wage/apprenticeship requirements.",
        adversary_position="IRS may challenge capture volume measurement, secure storage verification, utilization qualification, or wage compliance.",
        counter_arguments=[
            "Minimum capture threshold not satisfied",
            "Carbon oxide not from industrial source (not qualified)",
            "Secure geological storage requirements not met (EPA compliance)",
            "Utilization does not constitute chemical conversion or fixed use",
            "Prevailing wage or apprenticeship requirements failed",
            "Sequestered carbon oxide escaped (recapture triggered)",
            "Measurement methodology not independently verified"
        ],
        resolution_strategy="Engage carbon capture engineering specialist. Implement EPA-compliant monitoring and verification protocol. Install certified metering equipment. Obtain independent third-party verification of capture volumes and storage security. Implement certified payroll for wage compliance. File Form 8835.",
        entity_scope=["C_Corporation", "S_Corporation", "Partnership", "Individual_Business"],
        confidence=0.76,
        confidence_stratification=ConfidenceStratification.AGGRESSIVE,
        controlling_precedent="Emerging technology area; limited guidance; measurement and verification critical",
        issue_category=IssueCategory.ENERGY_CREDITS,
        credit_type="nonrefundable",
        recapture_risk=True,
        carryover_allowed=True,
        ordering_priority=85
    ),

    # ENERGY EFFICIENT COMMERCIAL BUILDINGS - IRC §179D
    DoctrineBlock(
        topic="energy_efficient_commercial_building_deduction",
        keywords=["IRC_179D", "commercial_building", "energy_efficiency", "HVAC", "lighting", "building_envelope", "179D_deduction"],
        conclusion_template=[
            "IRC §179D provides an immediate deduction (not credit) for energy-efficient commercial building property.",
            "Maximum deduction is $5.00/sq ft for buildings meeting 50%+ energy savings, with interim deductions for individual systems.",
            "Prevailing wage requirements apply for maximum deduction amounts; designer can claim deduction for government buildings."
        ],
        reasoning_framework="""
IRC §179D allows deduction for costs of energy-efficient commercial building property, enhanced by Inflation Reduction Act.

ENERGY EFFICIENT COMMERCIAL BUILDING PROPERTY (IRC §179D(c)):
Property installed on or in commercial building as part of:
1. INTERIOR LIGHTING SYSTEMS
2. HEATING, COOLING, VENTILATION, AND HOT WATER SYSTEMS (HVAC)
3. BUILDING ENVELOPE (roof, walls, foundation, windows, doors)

COMMERCIAL BUILDING:
- Located in U.S.
- Within scope of ASHRAE Standard 90.1 or 100 (commercial buildings)
- Excludes residential buildings (apartments, condos, etc.)

DEDUCTION AMOUNT (IRC §179D(b)):

FULL BUILDING APPROACH (50%+ energy savings):
- BASE: $0.50/sq ft to $1.00/sq ft based on % energy savings vs. ASHRAE Standard
  - 25% savings: $0.50/sq ft
  - 50% savings: $1.00/sq ft
  - Scales linearly
- INCREASED (with prevailing wage): $2.00/sq ft to $5.00/sq ft
  - 25% savings: $2.00/sq ft
  - 50% savings: $5.00/sq ft

INTERIM DEDUCTION (individual systems):
- If HVAC, lighting, or envelope achieves 25%+ energy savings independently: $0.60/sq ft base ($2.00/sq ft increased)
- Can claim for 1, 2, or all 3 systems separately

PREVAILING WAGE REQUIREMENT (IRC §179D(b)(3)):
- Laborers and mechanics paid prevailing wages (Davis-Bacon)
- Applies to buildings >50,000 sq ft
- Without prevailing wage: 1/5 of increased amounts

CERTIFICATION REQUIREMENT (IRC §179D(d)(6)):
- Qualified individual must certify property meets energy savings target
- Qualified individual: Licensed engineer or contractor under laws of jurisdiction
- Certification using software approved by DOE/IRS

ALLOCATION TO DESIGNER (IRC §179D(d)(4)):
- For government-owned buildings (federal, state, local), deduction allocated to person primarily responsible for design
- Designer (architect, engineer, contractor) claims deduction
- Owner provides written allocation

PLACED-IN-SERVICE REQUIREMENT:
- Deduction claimed in year property placed in service
- New construction or retrofit both qualify

ELIGIBLE RETROFIT PROPERTY (IRC §179D(d)(2)):
- Property installed as replacement for existing property
- Must achieve energy savings target
- Deduction available every 3 years for same building (allowing successive retrofits)
        """,
        key_factors=[
            "Building is commercial building within ASHRAE scope",
            "Energy efficiency measured against ASHRAE Standard 90.1 or 100",
            "Certification by qualified individual (licensed engineer/contractor)",
            "DOE-approved software used for energy modeling",
            "Prevailing wage requirement satisfied (for buildings >50,000 sq ft)",
            "25%+ energy savings for interim deduction, 50%+ for maximum",
            "Designer allocation for government buildings"
        ],
        primary_authority=[
            "IRC §179D - Energy efficient commercial building deduction",
            "IRS Notice 2008-40 - Certification requirements",
            "IRS Notice 2012-26 - Interim lighting rules",
            "IRS Notice 2022-61 - Prevailing wage guidance",
            "Inflation Reduction Act §13303 - Extension and modification"
        ],
        burden_holder="Taxpayer must obtain independent certification from qualified individual using approved software showing energy savings targets met.",
        adversary_position="IRS may challenge energy modeling, certification validity, prevailing wage compliance, or that property qualifies.",
        counter_arguments=[
            "Energy modeling not performed with DOE-approved software",
            "Qualified individual certification insufficient or not independent",
            "Energy savings target not achieved (<25% or <50%)",
            "Prevailing wage requirements not satisfied (wage underpayment)",
            "Building is residential rather than commercial",
            "Property not placed in service during taxable year"
        ],
        resolution_strategy="Engage independent energy consultant or engineer. Use IRS-approved software (e.g., DOE Qualified Software, IRS Energy Design Plugin). Implement certified payroll for prevailing wage compliance. Obtain written certification meeting Notice 2008-40 requirements. File Form 7205.",
        entity_scope=["C_Corporation", "S_Corporation", "Partnership", "Individual_Business", "Designer_for_Government"],
        confidence=0.87,
        confidence_stratification=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="Certification requirement strict; independent qualified individual essential",
        issue_category=IssueCategory.BUSINESS_CREDITS,
        credit_type="deduction_not_credit",
        recapture_risk=False,
        carryover_allowed=False,
        ordering_priority=90
    ),

    # CREDIT ORDERING - IRC §38(d)
    DoctrineBlock(
        topic="general_business_credit_ordering_rules",
        keywords=["credit_ordering", "IRC_38_d", "carryforward_ordering", "FIFO", "credit_utilization", "oldest_first"],
        conclusion_template=[
            "General business credit components are used in a specific order: carryforwards from earliest year, then current year credits, then carrybacks.",
            "Oldest credits are used first to prevent expiration of carryforwards.",
            "Passive activity credits and specified credits have additional ordering complexities."
        ],
        reasoning_framework="""
IRC §38(d) establishes ordering rules for utilizing general business credit components to maximize credit utilization before expiration.

BASIC ORDERING RULE (IRC §38(d)(1)):
Credits applied against tax liability in following order:
1. CARRYFORWARDS: From earliest year first (FIFO - First In, First Out)
2. CURRENT YEAR CREDITS: Credits from current tax year
3. CARRYBACKS: From latest year first (LIFO)

RATIONALE:
- Carryforwards have limited life (20 years)
- Using oldest first prevents expiration
- Current year credits can be carried forward if not used
- Carrybacks already have defined limitation period

COMPONENT CREDIT ORDERING WITHIN YEAR (IRC §38(c)(4)):
If multiple component credits exist within same year:
- Credits used pro rata if total exceeds limitation
- Each component credit bears proportional share of unused amount available for carryover

PASSIVE ACTIVITY CREDIT ORDERING (IRC §469(d)(2)):
- Passive activity credits cannot offset non-passive income tax
- Passive credits applied first to extent of passive activity tax
- Remaining passive credits carried forward indefinitely (suspended)
- Non-passive credits applied to remaining tax liability

SPECIFIED LIABILITY LOSS CREDITS (IRC §38(c)(4)(B)):
Certain credits (e.g., nuclear decommissioning) have special carryback/carryforward periods:
- 10-year carryback
- Indefinite carryforward
- Used after regular carryforwards but before current year credits

ELECTION TO FORGO CARRYBACK (IRC §39(a)(4)):
- Taxpayer may elect to forgo carryback period
- Increases carryforward period by carryback years foregone
- Strategic to avoid amended returns or if refund not beneficial

DOCUMENTATION REQUIREMENTS:
- Form 3800 Part III tracks carryforwards by year and component
- Each component credit maintains separate identity through carryover period
- Careful tracking required for credits with different carryback/carryforward periods

EXAMPLE ORDERING:
Assume $50,000 GBC limitation, with:
- 2015 carryforward: $10,000 (research credit)
- 2018 carryforward: $20,000 (LIHTC)
- Current year (2024): $30,000 (WOTC)
- 2025 carryback: $15,000 (investment credit)

ORDER OF APPLICATION:
1. 2015 carryforward: $10,000 used (oldest first)
2. 2018 carryforward: $20,000 used
3. Limitation reached ($30,000 used total)
4. Current year: $20,000 used, $10,000 carried forward to 2025
5. 2025 carryback: Not used (current year credits used first)
        """,
        key_factors=[
            "Identify all carryforwards by year and component credit type",
            "Calculate current year component credits",
            "Determine any carrybacks from future years",
            "Apply credits in statutory order (oldest carryforward first)",
            "Track passive vs. non-passive credits separately",
            "Document unused amounts by component for carryforward schedule",
            "Consider election to forgo carryback if beneficial"
        ],
        primary_authority=[
            "IRC §38(d) - Ordering rules",
            "IRC §39 - Carryback and carryforward",
            "IRC §469(d) - Passive activity credit limitations",
            "Treas. Reg. §1.38-1(d) - Ordering of credits",
            "Form 3800 Instructions - Credit carryforward tracking"
        ],
        burden_holder="Taxpayer must maintain detailed schedules tracking each component credit by year, remaining carryforward periods, and passive activity status.",
        adversary_position="IRS may challenge ordering if credits applied incorrectly, passive activity limitations ignored, or carryforward periods expired.",
        counter_arguments=[
            "Credits not applied in correct order (newest used before oldest)",
            "Passive activity credits offset non-passive income (violation)",
            "Carryforward period expired before utilization",
            "Component credits not tracked separately (lumped together)",
            "Carryback election made but not properly documented"
        ],
        resolution_strategy="Maintain Form 3800 Part III schedule meticulously. Use tax software with credit tracking module. Review carryforward expiration dates annually. Consider estimated tax planning to maximize credit utilization. Document passive activity status of each credit source.",
        entity_scope=["C_Corporation", "S_Corporation", "Partnership", "Individual_Business"],
        confidence=0.96,
        confidence_stratification=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="Statutory ordering is mandatory; no discretion to apply credits in different order",
        issue_category=IssueCategory.CREDIT_ORDERING,
        credit_type="ordering_rules",
        recapture_risk=False,
        carryover_allowed=True,
        ordering_priority=100
    ),

    # CREDIT LIMITATION - IRC §38(c)
    DoctrineBlock(
        topic="general_business_credit_limitation_formula",
        keywords=["credit_limitation", "IRC_38_c", "net_income_tax", "tentative_minimum_tax", "25_percent_test", "credit_utilization_cap"],
        conclusion_template=[
            "General business credit is limited to excess of net income tax over the greater of tentative minimum tax or 25% of net regular tax over $25,000.",
            "Limitation prevents credits from completely eliminating tax liability.",
            "Unused credits carry back 1 year and forward 20 years due to limitation."
        ],
        reasoning_framework="""
IRC §38(c) limits the amount of general business credit that can be used in any year, with unused amounts eligible for carryback/carryforward.

LIMITATION FORMULA (IRC §38(c)(1)):
GBC ALLOWED = NET INCOME TAX − GREATER OF:
1. Tentative minimum tax, OR
2. 25% × (net regular tax liability − $25,000)

COMPONENT DEFINITIONS:

NET INCOME TAX (IRC §38(c)(1)):
- Regular tax liability
- MINUS: Nonrefundable personal credits (child tax credit, education credits, etc.)
- Represents tax liability available to offset with business credits

TENTATIVE MINIMUM TAX (IRC §38(c)(2)):
- AMT calculation under IRC §55
- Prevents credits from creating or increasing AMT liability
- For corporations: §55(b)(1) tentative minimum tax

NET REGULAR TAX LIABILITY (IRC §38(c)(3)):
- Regular tax liability
- MINUS: Nonrefundable personal credits
- Same as net income tax for most taxpayers

25% TEST:
- Provides minimum tax floor
- Taxpayer must pay at least 75% of net regular tax over $25,000
- Credits can offset maximum 25% of net regular tax exceeding $25,000

EXAMPLES:

EXAMPLE 1 - Individual with Regular Tax:
- Regular tax: $100,000
- Nonrefundable personal credits: $5,000
- Net income tax: $95,000
- Tentative AMT: $0
- Net regular tax liability: $95,000
- 25% test: 25% × ($95,000 − $25,000) = $17,500
- GBC limitation: $95,000 − $17,500 = $77,500

EXAMPLE 2 - Corporation with AMT Exposure:
- Regular tax: $200,000
- Tentative AMT: $150,000
- Net income tax: $200,000
- 25% test: 25% × ($200,000 − $25,000) = $43,750
- GBC limitation: $200,000 − $150,000 = $50,000 (AMT is greater)

EXAMPLE 3 - Low Tax Situation:
- Regular tax: $30,000
- Tentative AMT: $0
- Net income tax: $30,000
- 25% test: 25% × ($30,000 − $25,000) = $1,250
- GBC limitation: $30,000 − $1,250 = $28,750

SPECIAL RULES:

EMPOWERMENT ZONE CREDITS (IRC §38(c)(2)):
- Can offset 100% of tentative AMT
- Not subject to AMT limitation for specified credits

SPECIFIED CREDITS (IRC §38(c)(4)(B)):
- Nuclear decommissification, advanced nuclear power facility credits
- Different limitation rules may apply

CARRYBACK/CARRYFORWARD (IRC §39):
- Unused credits (exceeding limitation) carry back 1 year
- Carry forward 20 years
- Ordering rules (IRC §38(d)) determine which credits used first
        """,
        key_factors=[
            "Net income tax amount (regular tax minus personal credits)",
            "Tentative minimum tax (AMT) calculation",
            "Net regular tax liability for 25% test",
            "General business credit total from all sources",
            "Comparison of AMT and 25% test (use greater)",
            "Carryforward credits from prior years reducing current utilization"
        ],
        primary_authority=[
            "IRC §38(c) - Limitation based on amount of tax",
            "IRC §55 - Alternative minimum tax",
            "IRC §39 - Carryback and carryforward",
            "Treas. Reg. §1.38-2 - Limitation on credit",
            "Form 3800 - General Business Credit"
        ],
        burden_holder="Taxpayer must calculate net income tax, tentative AMT, and 25% test to determine credit limitation accurately.",
        adversary_position="IRS may challenge calculation of net income tax, tentative AMT, or that limitation formula applied incorrectly.",
        counter_arguments=[
            "Net income tax overstated (nonrefundable credits not subtracted)",
            "Tentative AMT calculation incorrect",
            "25% test miscalculated (wrong base or percentage)",
            "Credits applied in excess of limitation",
            "Carryforward credits not properly accounted for in limitation"
        ],
        resolution_strategy="Use Form 3800 to calculate limitation automatically. For AMT exposure, complete Form 6251 (individuals) or AMT schedule (corporations). Verify nonrefundable personal credits subtracted correctly. Plan estimated taxes to maximize credit utilization within limitation.",
        entity_scope=["C_Corporation", "S_Corporation", "Partnership", "Individual_Business"],
        confidence=0.95,
        confidence_stratification=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="Mathematical formula is strict; no discretion in application",
        issue_category=IssueCategory.CREDIT_LIMITATIONS,
        credit_type="limitation_calculation",
        recapture_risk=False,
        carryover_allowed=False,
        ordering_priority=95
    ),

    # NEW ENERGY EFFICIENT HOME CREDIT - IRC §45L
    DoctrineBlock(
        topic="new_energy_efficient_home_credit",
        keywords=["IRC_45L", "energy_efficient_home", "ENERGY_STAR", "Zero_Energy_Ready_Home", "manufactured_home", "dwelling_unit"],
        conclusion_template=[
            "The new energy efficient home credit under IRC §45L provides $2,500-$5,000 per dwelling unit for eligible contractors.",
            "Home must meet ENERGY STAR or DOE Zero Energy Ready Home requirements and be acquired for use as residence.",
            "Prevailing wage requirements apply for maximum credit amounts for homes with construction beginning after 2022."
        ],
        reasoning_framework="""
IRC §45L incentivizes construction of energy-efficient residential homes through per-unit credits to eligible contractors.

ELIGIBLE CONTRACTOR (IRC §45L(e)(1)):
Person who constructed qualified new energy efficient home or manufactured home:
- Contractor built home
- Home acquired from contractor for use as residence
- Contractor claims credit (not homeowner)

QUALIFIED NEW ENERGY EFFICIENT HOME (IRC §45L(c)):
Dwelling unit located in U.S.:
- Construction substantially completed after 8/8/2005
- MEETS ENERGY EFFICIENCY REQUIREMENTS:

PRE-IRA (before 1/1/2023):
- ENERGY STAR certification

POST-IRA (after 12/31/2022):
- ENERGY STAR Single Family New Homes National Program Version 3.1 or 3.2, OR
- DOE Zero Energy Ready Home Program requirements
- Prevailing wage requirements for maximum credit

CREDIT AMOUNT (IRC §45L(a)):

POST-IRA AMOUNTS (construction beginning after 2022):
BASE CREDIT (without prevailing wage):
- $500 per dwelling unit

INCREASED CREDIT (with prevailing wage):
- ENERGY STAR certified: $2,500 per dwelling unit
- Zero Energy Ready Home: $5,000 per dwelling unit

PRE-IRA AMOUNTS (construction beginning before 2023):
- $2,000 per dwelling unit (50% energy savings vs. 2006 IECC + supplements)
- $1,000 per manufactured home (30% heating/cooling energy reduction)

ACQUISITION FOR RESIDENCE:
- Person acquiring home must intend to use as residence
- Rental property qualifies if acquired by tenant for residence
- Credit not allowed if acquired for speculation/resale

PREVAILING WAGE REQUIREMENT (IRC §45L(d)):
- Laborers and mechanics paid wages at prevailing rates
- Davis-Bacon wage determinations
- Applies to homes with construction beginning after 2022
- Without prevailing wage: reduced to $500 (1/5 of base amounts)

MANUFACTURED HOME (IRC §45L(c)(3)):
- Meets Federal Manufactured Home Construction and Safety Standards
- After 8/8/2005
- ENERGY STAR certified or exceeds 2006 IECC supplements

CERTIFICATION REQUIREMENT:
- Home must be certified by qualified third-party
- ENERGY STAR: RESNET HERS rater or equivalent
- Zero Energy Ready: DOE program certification
- Prevailing wage compliance certification

PLACED-IN-SERVICE TIMING:
- Credit claimed in year dwelling unit acquired by buyer for use as residence
- Not when construction completed, but when sold and acquired
        """,
        key_factors=[
            "Contractor (not homeowner) claims credit",
            "Home meets ENERGY STAR or Zero Energy Ready Home requirements",
            "Third-party certification obtained (HERS rater, DOE certification)",
            "Prevailing wage requirements satisfied for increased credit",
            "Home acquired by buyer for use as residence (not resale)",
            "Located in United States",
            "Construction substantially completed after applicable effective date"
        ],
        primary_authority=[
            "IRC §45L - New energy efficient home credit",
            "IRS Notice 2006-27 - Certification requirements (pre-IRA)",
            "IRS Notice 2023-65 - Prevailing wage and certification (post-IRA)",
            "ENERGY STAR Single Family New Homes Program v3.1/3.2",
            "DOE Zero Energy Ready Home Program Requirements"
        ],
        burden_holder="Contractor must obtain third-party certification of energy efficiency and prevailing wage compliance before claiming credit.",
        adversary_position="IRS may challenge certification validity, prevailing wage compliance, that home met energy efficiency requirements, or acquisition for residence.",
        counter_arguments=[
            "Third-party certification not obtained or insufficient",
            "Home did not meet ENERGY STAR or Zero Energy Ready requirements",
            "Prevailing wage requirements not satisfied (wage underpayment)",
            "Home acquired for speculation or investment, not residence",
            "Contractor not person who constructed home",
            "Construction began before effective date"
        ],
        resolution_strategy="Engage certified HERS rater or DOE Zero Energy Ready certifier early in design phase. Implement certified payroll for prevailing wage compliance. Obtain written certification meeting IRS requirements. Maintain records of home sales and buyer residence intent. File Form 8908.",
        entity_scope=["C_Corporation", "S_Corporation", "Partnership", "Individual_Business"],
        confidence=0.86,
        confidence_stratification=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="Certification requirement strict; prevailing wage documentation intensive",
        issue_category=IssueCategory.ENERGY_CREDITS,
        credit_type="nonrefundable",
        recapture_risk=False,
        carryover_allowed=True,
        ordering_priority=72
    ),

    # ENHANCED OIL RECOVERY CREDIT - IRC §43
    DoctrineBlock(
        topic="enhanced_oil_recovery_credit",
        keywords=["IRC_43", "EOR", "enhanced_oil_recovery", "tertiary_recovery", "qualified_EOR_costs", "oil_production"],
        conclusion_template=[
            "The enhanced oil recovery credit under IRC §43 provides a 15% credit for qualified enhanced oil recovery costs.",
            "Costs include tangible property, intangible drilling costs, tertiary injectants, and construction costs for qualified EOR projects.",
            "Credit phases out when reference price exceeds $28 (inflation-adjusted) and is part of general business credit."
        ],
        reasoning_framework="""
IRC §43 incentivizes use of enhanced oil recovery techniques to extract oil from mature fields.

QUALIFIED ENHANCED OIL RECOVERY PROJECT (IRC §43(c)(2)):
Project that:
- Uses one or more tertiary recovery methods
- Located in United States
- Applied to qualified enhanced oil recovery field
- Follows implementation plan certified by petroleum engineer

TERTIARY RECOVERY METHODS (IRC §43(c)(2)(B)):
Include but not limited to:
- Miscible fluid displacement (CO2, nitrogen, natural gas)
- Steam drive injection
- Microemulsion flooding
- In situ combustion
- Polymer-augmented waterflooding
- Alkaline flooding
- Immiscible carbon dioxide displacement
- Any other method approved by IRS

QUALIFIED ENHANCED OIR FIELD (IRC §43(c)(3)):
Field located in U.S. where:
- Crude oil production has commenced
- Production would not be economically feasible without tertiary recovery

QUALIFIED EOR COSTS (IRC §43(c)(1)):
Amounts paid or incurred for:
1. TANGIBLE PROPERTY: Equipment used in qualified EOR project
   - Depreciated under MACRS
   - Tangible depreciable property only
2. INTANGIBLE DRILLING AND DEVELOPMENT COSTS (IDC):
   - Otherwise deductible under IRC §263(c)
   - Incurred in connection with qualified EOR project
3. TERTIARY INJECTANT EXPENSES:
   - Amounts paid for tertiary injectant (CO2, chemicals, steam, etc.)
   - Used as part of tertiary recovery method
4. CONSTRUCTION COSTS:
   - For construction of Alaska natural gas pipeline
   - Specific provision for Alaska gas-to-oil projects

CREDIT RATE (IRC §43(a)):
- 15% of qualified enhanced oil recovery costs for taxable year
- Credit claimed in year costs paid or incurred

PHASE-OUT (IRC §43(b)):
Credit phases out when:
- Reference price exceeds $28 per barrel (1990 dollars, inflation-adjusted)
- Reference price = estimated annual average wellhead price per barrel
- Phase-out: Credit reduced by (reference price − $28) / $6
- Fully phased out when reference price reaches $34 (inflation-adjusted)

INFLATION ADJUSTMENT:
- $28 and $34 thresholds adjusted annually for inflation since 1990
- 2024 equivalent: approximately $66 and $80 (based on CPI-U)

AT-RISK RULES (IRC §49):
- EOR credit subject to at-risk limitations
- Taxpayer's basis limited to amount at risk

RECAPTURE (IRC §43(e)):
- If property ceases to qualify as qualified EOR property, credit recaptured
- Recapture based on remaining useful life percentage

COORDINATION WITH IDC DEDUCTION:
- Taxpayer must elect between:
  1. Deduct IDC under IRC §263(c), OR
  2. Claim EOR credit for IDC
- Cannot claim both for same costs

INCLUDED IN GENERAL BUSINESS CREDIT:
- EOR credit is component of general business credit (IRC §38)
- Subject to GBC limitation and carryover rules
        """,
        key_factors=[
            "Project uses tertiary recovery method (not primary or secondary)",
            "Project located in United States",
            "Petroleum engineer certification of implementation plan",
            "Costs are tangible property, IDC, tertiary injectants, or construction",
            "Reference price phase-out calculation (current vs. inflation-adjusted threshold)",
            "At-risk limitations satisfied",
            "Election between IDC deduction and EOR credit"
        ],
        primary_authority=[
            "IRC §43 - Enhanced oil recovery credit",
            "IRC §43(c)(2) - Tertiary recovery methods",
            "Treas. Reg. §1.43-1 - Qualified enhanced oil recovery costs",
            "IRS Notice (annual) - Reference price determination",
            "Form 8830 - Enhanced Oil Recovery Credit"
        ],
        burden_holder="Taxpayer must obtain petroleum engineer certification of EOR project and substantiate qualified costs.",
        adversary_position="IRS may challenge that method qualifies as tertiary recovery, costs were properly classified, or engineer certification was valid.",
        counter_arguments=[
            "Recovery method is primary or secondary, not tertiary",
            "Petroleum engineer certification insufficient or missing",
            "Costs include non-qualifying expenditures",
            "Credit phased out due to reference price exceeding threshold",
            "At-risk limitations not satisfied",
            "IDC deduction claimed for same costs as credit (double benefit)"
        ],
        resolution_strategy="Engage certified petroleum engineer to prepare implementation plan and certification. Classify costs carefully (tangible, IDC, injectants). Monitor annual IRS reference price notices. Compare benefit of IDC deduction vs. EOR credit. File Form 8830.",
        entity_scope=["C_Corporation", "S_Corporation", "Partnership", "Individual_Business"],
        confidence=0.85,
        confidence_stratification=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="Petroleum engineer certification required; reference price phase-out applies",
        issue_category=IssueCategory.ENERGY_CREDITS,
        credit_type="nonrefundable",
        recapture_risk=True,
        carryover_allowed=True,
        ordering_priority=78
    ),

    # EMPLOYER-PROVIDED CHILDCARE CREDIT - IRC §45F
    DoctrineBlock(
        topic="employer_provided_childcare_credit",
        keywords=["IRC_45F", "employer_childcare", "qualified_childcare_facility", "qualified_childcare_expenditures", "resource_referral_expenditures"],
        conclusion_template=[
            "The employer-provided child care credit under IRC §45F provides 25% credit for qualified child care facility expenditures and 10% for resource and referral expenditures.",
            "Maximum credit is $150,000 per taxable year.",
            "Facility must be used primarily by employees and meet state licensing requirements."
        ],
        reasoning_framework="""
IRC §45F incentivizes employers to provide child care facilities and services for employees.

QUALIFIED CHILD CARE EXPENDITURES (IRC §45F(c)(1)):
Amounts paid or incurred for:
1. ACQUISITION, CONSTRUCTION, REHABILITATION, OR EXPANSION:
   - Of property that is to be used as part of qualified child care facility
   - Includes building, equipment, furniture
2. OPERATING COSTS:
   - Of qualified child care facility
   - Including training costs for employees who provide child care

QUALIFIED CHILD CARE FACILITY (IRC §45F(c)(2)):
Facility that:
- Principal use is to provide child care assistance
- Meets requirements of all applicable laws/regulations of state or local government
  (including licensing requirements)
- Enrollment open to employees of taxpayer during normal working hours
  (not exclusive to highly compensated employees)

PRINCIPAL USE TEST:
- Facility must be used primarily (>50%) by employees of taxpayer
- Enrollment of employee's children must be available during normal working hours
- Cannot discriminate in favor of highly compensated employees

QUALIFIED CHILD CARE RESOURCE AND REFERRAL EXPENDITURES (IRC §45F(c)(3)):
Amounts paid or incurred under contract to provide child care resource and referral services to employees:
- Information about child care providers
- Assistance in locating child care
- Consumer education about child care
- Referral to child care providers

CREDIT AMOUNT (IRC §45F(a)):
- 25% of qualified child care expenditures (facility costs), PLUS
- 10% of qualified child care resource and referral expenditures
- MAXIMUM: $150,000 per taxable year

BASIS REDUCTION (IRC §45F(d)):
- Basis of qualified child care facility reduced by amount of credit claimed
- Reduces future depreciation deductions

RECAPTURE (IRC §45F(d)):
If facility ceases to be qualified child care facility or principal use changes:
- Credit recaptured based on recapture percentage
- 10-year recapture period:
  Year 1: 100%, Year 2: 85%, Year 3: 70%, Year 4: 55%, Year 5: 40%,
  Year 6: 25%, Year 7: 10%, Years 8-10: 0%

NO DOUBLE BENEFIT:
- Deduction for expenditures reduced by credit amount claimed
- Cannot deduct and claim credit for same dollar

HIGHLY COMPENSATED EMPLOYEE DISCRIMINATION TEST:
- Facility enrollment cannot favor highly compensated employees (HCEs)
- HCE definition: IRC §414(q)
  - 5% owner, OR
  - Compensation > $135,000 (2024, indexed)
- Nondiscrimination testing similar to qualified retirement plans

INCLUDED IN GENERAL BUSINESS CREDIT:
- IRC §45F credit is component of general business credit (IRC §38)
- Subject to GBC limitation and carryover rules
        """,
        key_factors=[
            "Facility is qualified child care facility (state licensed, employee use)",
            "Principal use is to provide child care to employees (>50%)",
            "No discrimination in favor of highly compensated employees",
            "Expenditures are acquisition, construction, operation, or resource/referral",
            "State and local licensing requirements satisfied",
            "Basis reduction and recapture rules applied",
            "Maximum credit of $150,000 per year"
        ],
        primary_authority=[
            "IRC §45F - Employer-provided child care credit",
            "IRC §45F(c)(2) - Qualified child care facility",
            "Treas. Reg. §1.45F-1 - Employer-provided child care credit",
            "IRS Pub. 503 - Child and Dependent Care Expenses",
            "Form 8882 - Employer-Provided Childcare Facilities and Services Credit"
        ],
        burden_holder="Employer must substantiate qualified facility status, state licensing, employee usage, nondiscrimination, and expenditure amounts.",
        adversary_position="IRS may challenge facility qualification, principal use by employees, discrimination in favor of HCEs, or expenditure classification.",
        counter_arguments=[
            "Facility does not meet state licensing requirements",
            "Principal use not by employees (<50% employee enrollment)",
            "Enrollment discriminates in favor of highly compensated employees",
            "Expenditures include non-qualifying costs",
            "Facility ceased to be qualified during recapture period",
            "Resource and referral services not properly documented"
        ],
        resolution_strategy="Obtain state child care facility license. Maintain enrollment records showing majority employee use. Conduct annual HCE nondiscrimination testing. Document all acquisition, construction, and operating costs. File Form 8882. Track recapture period carefully.",
        entity_scope=["C_Corporation", "S_Corporation", "Partnership", "Individual_Business"],
        confidence=0.88,
        confidence_stratification=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="State licensing and nondiscrimination testing required",
        issue_category=IssueCategory.EMPLOYMENT_CREDITS,
        credit_type="nonrefundable",
        recapture_risk=True,
        carryover_allowed=True,
        ordering_priority=68
    ),

    # ALTERNATIVE FUEL VEHICLE REFUELING PROPERTY CREDIT - IRC §30C
    DoctrineBlock(
        topic="alternative_fuel_vehicle_refueling_property_credit",
        keywords=["IRC_30C", "EV_charging", "alternative_fuel", "refueling_property", "hydrogen_fueling", "charging_station"],
        conclusion_template=[
            "The alternative fuel vehicle refueling property credit under IRC §30C provides up to 30% credit for installing qualified refueling property.",
            "Maximum credit is $100,000 per item of property (businesses) or $1,000 (individuals) before IRA; enhanced after IRA.",
            "Property must be placed in service to dispense or recharge alternative fuels into motor vehicles."
        ],
        reasoning_framework="""
IRC §30C incentivizes installation of alternative fuel refueling infrastructure, significantly expanded by Inflation Reduction Act.

QUALIFIED ALTERNATIVE FUEL VEHICLE REFUELING PROPERTY (IRC §30C(c)):
Property:
- For storage or dispensing of alternative fuel into fuel tank of motor vehicle propelled by such fuel, OR
- For recharging electric vehicles
- Original use begins with taxpayer
- Placed in service after 12/31/2005
- Located in United States

ALTERNATIVE FUELS (IRC §30C(c)(2)):
- Electricity
- Natural gas (compressed or liquefied)
- Liquefied petroleum gas
- Hydrogen
- Any liquid at least 85% by volume: methanol, ethanol, other alcohol
- Biodiesel (does not include petroleum diesel)
- E85 or other high-ethanol blends
- P-series fuels

CREDIT AMOUNT:

PRE-IRA (property placed in service before 1/1/2023):
- 30% of cost
- MAXIMUM: $30,000 per location (businesses), $1,000 per location (individuals)

POST-IRA (property placed in service after 12/31/2022):

BASE CREDIT:
- 6% of cost
- Maximum $100,000 per item

INCREASED CREDIT (if prevailing wage/apprenticeship satisfied):
- 30% of cost
- Maximum $100,000 per item of property

BONUS CREDITS (IRC §30C(e)):
- Census tract criteria: Located in low-income community or non-urban area
- Increases maximum to $200,000 (from $100,000)

PREVAILING WAGE AND APPRENTICESHIP (IRC §30C(d)):
- Same requirements as IRC §45/§48
- Laborers and mechanics paid prevailing wages
- Minimum apprenticeship labor hour percentages
- Applies to property with basis > $50,000

ELIGIBLE CENSUS TRACTS:
- Low-income community, OR
- Non-urban area (population < 50,000)

DEPRECIABLE PROPERTY:
- Property must be depreciable (IRC §167) for businesses
- Individuals: property must be installed on primary residence

BIDIRECTIONAL CHARGING EQUIPMENT (IRC §30C(f)):
- Enhanced credit for bidirectional charging (vehicle-to-grid or vehicle-to-home)
- Allows electric vehicles to send power back to grid or building

BASIS REDUCTION (IRC §30C(e)):
- Basis of property reduced by amount of credit
- Reduces future depreciation

RECAPTURE:
- If property ceases to qualify within recapture period, credit recaptured
- Similar recapture rules to other energy credits

COORDINATION WITH BONUS DEPRECIATION:
- Property eligible for IRC §168(k) bonus depreciation
- Basis reduction for credit occurs before depreciation calculation
        """,
        key_factors=[
            "Property dispenses/recharges alternative fuel into motor vehicles",
            "Property is depreciable (for businesses) or on primary residence (individuals)",
            "Original use begins with taxpayer",
            "Prevailing wage and apprenticeship requirements satisfied for 30% rate",
            "Located in low-income or non-urban census tract for bonus credit",
            "Basis exceeds $50,000 threshold (triggers wage/apprenticeship requirement)",
            "Basis reduced by credit amount"
        ],
        primary_authority=[
            "IRC §30C - Alternative fuel vehicle refueling property credit",
            "IRC §30C(d) - Prevailing wage and apprenticeship",
            "IRS Notice 2023-9 - Census tract qualification",
            "IRS Notice 2022-61 - Prevailing wage guidance",
            "Inflation Reduction Act §13404 - Extension and modification"
        ],
        burden_holder="Taxpayer must substantiate property qualification, prevailing wage compliance (if applicable), and census tract eligibility (for bonus).",
        adversary_position="IRS may challenge property qualification, prevailing wage compliance, census tract determination, or basis calculation.",
        counter_arguments=[
            "Property does not dispense qualified alternative fuel",
            "Original use did not begin with taxpayer (used property)",
            "Prevailing wage or apprenticeship requirements not satisfied",
            "Census tract not qualified as low-income or non-urban",
            "Basis calculation includes non-qualifying costs",
            "Property ceased to qualify during recapture period"
        ],
        resolution_strategy="Verify property dispenses qualified alternative fuel. Implement certified payroll for prevailing wage compliance (if basis > $50,000). Use IRS census tract mapping tool to confirm eligibility. Obtain independent cost certification. File Form 8911.",
        entity_scope=["C_Corporation", "S_Corporation", "Partnership", "Individual_Business", "Individual"],
        confidence=0.83,
        confidence_stratification=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="Census tract determination critical for bonus credit; wage compliance for increased rate",
        issue_category=IssueCategory.ENERGY_CREDITS,
        credit_type="nonrefundable",
        recapture_risk=True,
        carryover_allowed=True,
        ordering_priority=67
    ),

    # NONCONVENTIONAL FUEL PRODUCTION CREDIT - IRC §29 (expired but important for carryforwards)
    DoctrineBlock(
        topic="nonconventional_fuel_production_credit",
        keywords=["IRC_29", "nonconventional_fuel", "coalbed_methane", "tight_sands_gas", "section_29_credit", "qualified_fuels"],
        conclusion_template=[
            "The nonconventional fuel production credit under IRC §29 (now IRC §45K) provided credit for production of qualified fuels from nonconventional sources.",
            "Credit expired for production after 2002, but carryforwards may still exist (20-year carryforward period).",
            "Qualified fuels included coalbed methane, tight sands gas, biomass gas, and synthetic fuels from coal."
        ],
        reasoning_framework="""
IRC §29 (redesignated as IRC §45K) provided production-based credit for nonconventional fuels, now expired but carryforwards remain relevant.

HISTORICAL CONTEXT:
- IRC §29 enacted in 1980 to incentivize domestic unconventional energy production
- Credit available for production from wells drilled or facilities placed in service before 1993
- Production credit period ended 2002
- Carryforward period: 20 years (until 2022 for last production year)
- As of 2024, most carryforwards expired, but some may remain on older returns under audit

QUALIFIED FUELS (IRC §45K(c)):
1. OIL PRODUCED FROM SHALE AND TAR SANDS
2. GAS PRODUCED FROM:
   - Geopressured brine
   - Devonian shale
   - Coal seams (coalbed methane)
   - Tight formations (tight sands gas)
   - Biomass (landfill gas, etc.)
3. LIQUID, GASEOUS, OR SOLID SYNTHETIC FUELS FROM COAL

CREDIT AMOUNT (IRC §45K(a)):
- $3.00 per barrel-of-oil equivalent (BOE)
- Adjusted annually for inflation
- Final credit year (2002): approximately $5.90/BOE

WELL OR FACILITY REQUIREMENTS:
- Well drilled or facility placed in service after 12/31/1979 and before 1/1/1993
- Located in United States
- No credit for production after 12/31/2002

PHASE-OUT (IRC §45K(b)(2)):
- Credit phased out when reference price exceeded $23.50/barrel (1979 dollars)
- Reference price = annual average wellhead price of domestic crude oil
- Phase-out: Credit reduced by (reference price − $23.50) / $6.00
- Fully phased out when reference price reached $29.50

SOLD TO UNRELATED PERSON:
- Fuel must be sold to unrelated person
- Production for own use did not qualify

INCLUDED IN GENERAL BUSINESS CREDIT:
- Section 29 credit was component of general business credit
- Subject to GBC limitation and carryback/carryforward rules
- 1-year carryback, 20-year carryforward (last possible carryforward: 2022)

CARRYFORWARD TRACKING:
Taxpayers with Section 29 carryforwards must:
- Track on Form 3800 Part III
- Apply in FIFO order (oldest first)
- Monitor expiration dates (20 years from generation year)

AUDIT IMPLICATIONS:
- IRS may challenge carryforward amounts on examination
- Taxpayer must substantiate:
  - Original credit calculation from production years
  - Proper carryforward tracking
  - No expired carryforwards utilized
  - Limitation calculations in utilization years
        """,
        key_factors=[
            "Well drilled or facility placed in service 1980-1992",
            "Production occurred before 2003",
            "Qualified fuel type (coalbed methane, tight sands, etc.)",
            "Fuel sold to unrelated person",
            "Reference price phase-out applied",
            "Carryforward not expired (20-year limit)",
            "Proper FIFO ordering in utilization"
        ],
        primary_authority=[
            "IRC §45K (formerly §29) - Nonconventional fuel credit",
            "IRC §29(g) - Extension of credit (repealed)",
            "Treas. Reg. §1.29-1 - Credit for producing fuel from nonconventional source",
            "IRS Notice (annual 1980-2002) - Reference price determinations"
        ],
        burden_holder="Taxpayer must substantiate original credit calculation from production years and track carryforwards across 20-year period.",
        adversary_position="IRS may challenge well/facility placed-in-service date, qualified fuel classification, or carryforward calculation.",
        counter_arguments=[
            "Well drilled or facility placed in service outside 1980-1992 window",
            "Fuel type did not qualify as nonconventional source",
            "Production occurred after 2002 (no credit allowed)",
            "Credit phased out due to reference price",
            "Carryforward expired (>20 years from generation)",
            "Fuel not sold to unrelated person (self-consumption)"
        ],
        resolution_strategy="For open years with Section 29 carryforwards: Reconstruct original credit calculations, verify well/facility placed-in-service dates, confirm FIFO ordering, check expiration dates. Maintain detailed carryforward schedules. Consider protective claims if carryforwards inadvertently expired.",
        entity_scope=["C_Corporation", "S_Corporation", "Partnership", "Individual_Business"],
        confidence=0.79,
        confidence_stratification=ConfidenceStratification.AGGRESSIVE,
        controlling_precedent="Credit expired 2002; only carryforward issues remain; heavy documentation burden",
        issue_category=IssueCategory.ENERGY_CREDITS,
        credit_type="nonrefundable",
        recapture_risk=False,
        carryover_allowed=True,
        ordering_priority=50
    )
]


def get_doctrine_block(topic: str) -> Optional[DoctrineBlock]:
    """Retrieve doctrine block by topic"""
    for block in DOCTRINE_CACHE:
        if block.topic == topic:
            return block
    return None


def get_doctrines_by_category(category: IssueCategory) -> List[DoctrineBlock]:
    """Retrieve all doctrine blocks for a given category"""
    return [block for block in DOCTRINE_CACHE if block.issue_category == category]


def get_doctrines_by_keyword(keyword: str) -> List[DoctrineBlock]:
    """Retrieve doctrine blocks matching keyword"""
    keyword_lower = keyword.lower()
    return [block for block in DOCTRINE_CACHE
            if any(keyword_lower in kw.lower() for kw in block.keywords)]


def get_all_topics() -> List[str]:
    """Get list of all doctrine topics"""
    return [block.topic for block in DOCTRINE_CACHE]


def get_credit_ordering_priority() -> List[DoctrineBlock]:
    """Get doctrine blocks ordered by credit ordering priority"""
    return sorted(DOCTRINE_CACHE, key=lambda x: x.ordering_priority)
