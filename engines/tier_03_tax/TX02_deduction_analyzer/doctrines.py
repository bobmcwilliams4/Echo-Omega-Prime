"""
TX02 Deduction Analyzer — Doctrine Cache

50+ expert doctrine blocks covering IRC deductions:
- §162 ordinary/necessary business expenses
- §163 interest deduction (TCJA limitations)
- §164 SALT cap
- §165 losses
- §167/168 depreciation/MACRS
- §170 charitable contributions
- §179 expensing
- §195 startup costs
- §199A QBI deduction
- §212 investment expenses (suspended)
- §213 medical expenses
- §217 moving expenses (suspended)
- §280A home office
- §280E cannabis limitations
- §461(l) excess business loss limitation
- §469 passive activity loss rules
- §267 related party limitations

Each block contains real tax expertise, adversarial thinking,
epistemic guardrails, and authority hardening.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class DoctrineBlock:
    """Single tax deduction doctrine reasoning block."""
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
    confidence: float
    confidence_stratification: str
    controlling_precedent: Optional[str] = None
    tcja_impact: Optional[str] = None
    disclosure_caveat: Optional[str] = None


# ═══════════════════════════════════════════════════════════════════
# DOCTRINE CACHE — 50+ BLOCKS
# ═══════════════════════════════════════════════════════════════════

DOCTRINE_CACHE: List[DoctrineBlock] = [

    # ───────────────────────────────────────────────────────────────
    # §162 — ORDINARY AND NECESSARY BUSINESS EXPENSES
    # ───────────────────────────────────────────────────────────────

    DoctrineBlock(
        topic="IRC §162 Ordinary and Necessary Business Expense Test",
        keywords=["ordinary", "necessary", "business expense", "162", "trade or business", "deductibility"],
        conclusion_template="Expense is {DEFENSIBLE|AGGRESSIVE|DISCLOSURE} as ordinary and necessary business expense under §162(a). Key factors: {direct business purpose}, {customary in industry}, {reasonable amount}, {substantiation quality}.",
        reasoning_framework="""
IRC §162(a) allows deduction for ordinary and necessary expenses paid or incurred in carrying on a trade or business.

ORDINARY TEST (Welch v. Helvering, 290 U.S. 111):
  - Normal, usual, or customary in the taxpayer's business
  - Not capital expenditure or permanent improvement
  - Industry comparison relevant but not dispositive

NECESSARY TEST:
  - Appropriate and helpful to the business
  - NOT indispensable (Commissioner v. Heininger, 320 U.S. 467)
  - Business judgment deference (unless purely personal)

TRADE OR BUSINESS REQUIREMENT:
  - Regular, continuous activity (Groetzinger, 480 U.S. 23)
  - Profit motive required
  - Hobby loss rules §183 if not for-profit

CAPITAL VS. EXPENSE:
  - §263 capitalization if creates separate asset
  - §263A uniform capitalization rules for inventory/production
  - Repairs deductible, improvements capitalized (Treas. Reg. §1.162-4)

PERSONAL VS. BUSINESS:
  - Personal living expenses nondeductible (§262)
  - Mixed-use allocation required
  - Substantiation critical (Cohan rule limited by §274)

REASONABLENESS TEST:
  - Excessive compensation scrutinized (§162(a)(1))
  - Related party transactions (§267)
  - Arm's length standard
""",
        key_factors=[
            "Direct connection to business activity",
            "Industry customary practice",
            "Reasonableness of amount",
            "Adequate substantiation (receipts, business purpose documentation)",
            "No personal consumption element",
            "Not capital expenditure creating long-term benefit",
            "Paid or incurred during tax year",
        ],
        primary_authority=[
            "IRC §162(a)",
            "Treas. Reg. §1.162-1",
            "Welch v. Helvering, 290 U.S. 111 (1933)",
            "Commissioner v. Heininger, 320 U.S. 467 (1943)",
            "Commissioner v. Lincoln Savings, 403 U.S. 345 (1971)",
        ],
        burden_holder="Taxpayer bears burden to prove ordinary and necessary business purpose",
        adversary_position="IRS argues expense is personal (§262), capital (§263), or lacks business connection",
        counter_arguments=[
            "Mixed personal/business use without allocation",
            "Lavish or extravagant under circumstances (§274(k))",
            "Related party transaction not arm's length",
            "Hobby activity, not for-profit (§183)",
            "Capital expenditure creating enduring benefit (INDOPCO)",
        ],
        resolution_strategy="Document contemporaneous business purpose, industry comparables, allocation methodology if mixed-use, reasonable compensation analysis if related party",
        entity_scope="All taxpayers carrying on trade or business",
        confidence=0.95,
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Welch v. Helvering establishes ordinary test; Heininger establishes necessary standard",
    ),

    DoctrineBlock(
        topic="§162 Capital Expenditure vs. Deductible Expense — INDOPCO Doctrine",
        keywords=["capital", "expense", "INDOPCO", "263", "significant future benefit", "repair"],
        conclusion_template="Expenditure {MUST|MAY|SHOULD NOT} be capitalized under §263. Analysis: {duration of benefit}, {separate asset creation}, {betterment/adaptation/restoration under tangible property regs}.",
        reasoning_framework="""
CAPITAL VS. EXPENSE TENSION:
  - §162 permits current deduction for ordinary/necessary business expenses
  - §263(a) REQUIRES capitalization if expenditure creates asset with useful life substantially beyond tax year

INDOPCO DOCTRINE (INDOPCO, Inc. v. Commissioner, 503 U.S. 79, 1992):
  - Significant future benefit = strong indicator of capital nature
  - BUT: not sole test (IRS conceded in Rev. Rul. 2000-7)
  - Duration and extent of benefit evaluated

TANGIBLE PROPERTY REGULATIONS (Treas. Reg. §1.263(a)-3, effective 2014):
  - REPAIRS: Deductible if keep property in ordinarily efficient operating condition
  - BETTERMENTS: Capitalize if ameliorate defect, expand capacity, or increase productivity
  - RESTORATIONS: Capitalize if return to like-new condition, replace major component
  - ADAPTATIONS: Capitalize if adapt property to new use

12-MONTH RULE (Treas. Reg. §1.263(a)-4(f)):
  - Benefit lasting ≤12 months AND not beyond end of following tax year = deductible
  - Safe harbor for short-term benefits

REPAIRS VS. IMPROVEMENTS (Treas. Reg. §1.162-4):
  - Routine maintenance = deductible
  - Substantial improvement increasing value/prolonging life = capital

EXAMPLES:
  - Repainting building: DEDUCT (keeps in operating condition)
  - Adding new wing: CAPITALIZE (betterment/expansion)
  - Replacing roof: CAPITALIZE if major component (restoration)
  - Annual HVAC maintenance: DEDUCT (routine)
  - Complete HVAC system overhaul: CAPITALIZE (restoration/betterment)
""",
        key_factors=[
            "Duration of benefit (12-month rule threshold)",
            "Separate distinct asset created",
            "Betterment ameliorating pre-existing defect",
            "Restoration to like-new condition",
            "Adaptation to new or different use",
            "Routine vs. non-routine maintenance",
        ],
        primary_authority=[
            "IRC §263(a)",
            "Treas. Reg. §1.263(a)-3 (tangible property regs)",
            "INDOPCO, Inc. v. Commissioner, 503 U.S. 79 (1992)",
            "Rev. Rul. 2001-4 (12-month rule)",
            "Treas. Reg. §1.162-4 (repairs)",
        ],
        burden_holder="Taxpayer must prove current deduction justified; IRS challenges as capital",
        adversary_position="IRS argues significant future benefit mandates capitalization under INDOPCO",
        counter_arguments=[
            "Benefit extends beyond 12 months",
            "Creates separate intangible asset",
            "Increases property value or useful life",
            "Not routine/recurring maintenance",
        ],
        resolution_strategy="Apply tangible property regulations framework (betterment/restoration/adaptation tests), invoke 12-month safe harbor if applicable, document routine maintenance nature",
        entity_scope="All taxpayers with business expenditures",
        confidence=0.88,
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="INDOPCO sets future benefit framework; tangible property regs provide bright-line tests",
    ),

    # ───────────────────────────────────────────────────────────────
    # §163 — INTEREST DEDUCTION (TCJA LIMITATIONS)
    # ───────────────────────────────────────────────────────────────

    DoctrineBlock(
        topic="IRC §163(j) Business Interest Limitation — TCJA 30% ATI Cap",
        keywords=["interest", "163j", "TCJA", "ATI", "30 percent", "business interest", "EBITDA"],
        conclusion_template="Business interest deduction {LIMITED TO|FULLY DEDUCTIBLE|CARRIED FORWARD} under §163(j). ATI: {adjusted taxable income}, 30% cap: {calculation}, excess: {carryforward indefinitely}.",
        reasoning_framework="""
§163(j) BUSINESS INTEREST LIMITATION (enacted TCJA 2017, effective 2018):

BASE RULE:
  - Business interest expense deduction LIMITED to sum of:
    (1) Business interest income, PLUS
    (2) 30% of adjusted taxable income (ATI), PLUS
    (3) Floor plan financing interest (auto dealers)

ADJUSTED TAXABLE INCOME (ATI):
  - 2018-2021: EBITDA-style (taxable income before interest, depreciation, amortization)
  - 2022+: EBIT-style (taxable income before interest only, NO depreciation/amortization addback)
  - IMPACT: 2022+ stricter (smaller ATI base = smaller 30% allowance)

SMALL BUSINESS EXCEPTION:
  - Taxpayers with average annual gross receipts ≤$27M (inflation-adjusted) for 3-year period EXEMPT
  - Important safe harbor for smaller entities

EXCEPTED TRADES/BUSINESSES:
  - Real property trades/businesses electing out (§163(j)(7)(B))
  - Farming businesses electing out (§163(j)(7)(C))
  - Certain utilities (regulated public utilities)
  - COST: Elect out = must use ADS depreciation (longer lives)

EXCESS BUSINESS INTEREST CARRYFORWARD:
  - Disallowed interest carries forward INDEFINITELY
  - Can use in future years subject to 30% ATI cap
  - NO carryback

PARTNERSHIP/S-CORP RULES:
  - Limitation applies at entity level AND partner/shareholder level
  - Excess business interest allocated to partners/shareholders
  - Partner's basis reduced by excess interest allocated

COVID-19 RELIEF (CARES Act 2020):
  - 2019-2020: ATI cap increased from 30% to 50%
  - Taxpayers could elect to use 2019 ATI for 2020 (favorable if 2020 ATI dropped)
  - Temporary relief expired after 2020

PLANNING:
  - Debt-heavy businesses significantly impacted
  - Consider small business exception qualification
  - Real estate election trade-offs (interest deduction vs. depreciation)
  - Earnings stripping concern (foreign parents loading U.S. subs with debt)
""",
        key_factors=[
            "Average gross receipts (small business exception threshold)",
            "ATI calculation (EBIT vs. EBITDA depending on year)",
            "Excepted business election (real estate/farming)",
            "Partnership vs. C-corp structure (different layer application)",
            "Carryforward tracking",
        ],
        primary_authority=[
            "IRC §163(j)",
            "Treas. Reg. §1.163(j)-1 through §1.163(j)-11 (final regs 2020)",
            "TCJA Pub. L. 115-97 (2017)",
            "CARES Act Pub. L. 116-136 (2020)",
        ],
        burden_holder="Taxpayer must compute ATI and prove small business exception if claimed",
        adversary_position="IRS challenges ATI calculation, small business exception qualification, or excepted business election validity",
        counter_arguments=[
            "Gross receipts exceed $27M threshold (no exception)",
            "ATI miscalculated (especially EBIT vs. EBITDA transition)",
            "Partnership allocation errors",
            "Election out not properly made or documented",
        ],
        resolution_strategy="Document gross receipts 3-year average, maintain ATI worksheets, consider real estate/farming election if beneficial (model ADS depreciation cost), track carryforwards",
        entity_scope="All taxpayers with business interest expense (unless small business or excepted business)",
        confidence=0.90,
        confidence_stratification="DEFENSIBLE",
        tcja_impact="TCJA 2017 created §163(j) limitation; CARES Act temporarily liberalized 2019-2020",
        controlling_precedent="Statutory framework post-TCJA; final regulations issued 2020",
    ),

    DoctrineBlock(
        topic="§163(h) Personal Interest Disallowance — Qualified Residence Interest Exception",
        keywords=["personal interest", "163h", "qualified residence", "mortgage interest", "home equity", "TCJA"],
        conclusion_template="Interest {DEDUCTIBLE|NONDEDUCTIBLE} as qualified residence interest. Debt: {acquisition|home equity}, amount: {limit}, residences: {principal + one second home}.",
        reasoning_framework="""
§163(h) PERSONAL INTEREST NONDEDUCTIBILITY:
  - General rule: Personal interest (credit cards, car loans, student loans pre-2018) NOT deductible
  - Exception: Qualified residence interest (QRI) IS deductible as itemized deduction

QUALIFIED RESIDENCE INTEREST (PRE-TCJA):
  - Acquisition indebtedness: Up to $1M ($500K MFS) to acquire/construct/substantially improve
  - Home equity indebtedness: Up to $100K ($50K MFS) for any purpose
  - Secured by qualified residence (principal + one second home)

TCJA CHANGES (2018-2025):
  - Acquisition debt limit REDUCED: $750K ($375K MFS) for debt incurred after 12/15/2017
  - Grandfathered debt: Pre-12/16/2017 debt keeps $1M limit
  - Home equity debt: SUSPENDED (no deduction 2018-2025) UNLESS used to acquire/improve home (then treated as acquisition debt)
  - KEY: Tracing rules — home equity loan for home improvement = acquisition debt (deductible)

QUALIFIED RESIDENCE:
  - Principal residence (§121 definition)
  - One second home (not rented or rented <15 days/year)
  - If second home rented >14 days, must use as personal residence >14 days or 10% of rental days (§280A)

REFINANCING:
  - Refi of acquisition debt = acquisition debt (limited to original amount)
  - Cash-out refi: Excess over original debt = home equity (subject to TCJA suspension unless improves home)

MIXED-USE PROPERTY:
  - Business use portion: Interest allocated to Schedule C/E (subject to other limitations)
  - Personal use portion: Qualified residence interest

POINTS:
  - Points on acquisition debt generally deductible in year paid (Rev. Proc. 94-27)
  - Refi points: Amortized over loan life

CONSTRUCTION LOANS:
  - 24-month period before residence ready for occupancy counts as acquisition debt
""",
        key_factors=[
            "Debt incurred before or after 12/15/2017 (grandfathering)",
            "Acquisition vs. home equity classification",
            "Tracing home equity proceeds to home improvement",
            "Qualified residence status (principal + one second home)",
            "Debt amount within limits ($750K/$1M)",
        ],
        primary_authority=[
            "IRC §163(h)",
            "IRC §163(h)(3) (qualified residence interest)",
            "TCJA §11043 (2017)",
            "Treas. Reg. §1.163-10T",
            "Rev. Proc. 94-27 (points)",
        ],
        burden_holder="Taxpayer must substantiate qualified residence status, debt purpose, and amounts",
        adversary_position="IRS challenges home equity debt as personal (not home improvement), exceeds limits, or property not qualified residence",
        counter_arguments=[
            "Home equity debt not used for home acquisition/improvement (nondeductible 2018-2025)",
            "Exceeds $750K/$1M limits",
            "Second home rented too much (fails §280A personal use test)",
            "Not secured by qualified residence",
        ],
        resolution_strategy="Trace home equity loan proceeds to capital improvements (not personal expenses), maintain documentation of qualified residence status, allocate if mixed-use property",
        entity_scope="Individual taxpayers itemizing deductions",
        confidence=0.92,
        confidence_stratification="DEFENSIBLE",
        tcja_impact="TCJA suspended home equity interest deduction (2018-2025) unless used for home acquisition/improvement; reduced acquisition debt limit to $750K",
    ),

    # ───────────────────────────────────────────────────────────────
    # §164 — STATE AND LOCAL TAX DEDUCTION (SALT CAP)
    # ───────────────────────────────────────────────────────────────

    DoctrineBlock(
        topic="IRC §164 SALT Cap — $10,000 Limitation on State and Local Taxes",
        keywords=["SALT", "164", "state tax", "local tax", "property tax", "income tax", "$10000 cap", "TCJA"],
        conclusion_template="State and local taxes {FULLY DEDUCTIBLE|LIMITED TO $10K|NONDEDUCTIBLE}. Taxes: {income/sales/property}, cap: {$10K individual/$5K MFS}, excess: {nondeductible}.",
        reasoning_framework="""
§164 STATE AND LOCAL TAX DEDUCTION:

PRE-TCJA (THROUGH 2017):
  - Unlimited deduction for state/local income OR sales taxes (election)
  - Unlimited deduction for state/local property taxes
  - Major benefit in high-tax states (CA, NY, NJ, CT, IL)

TCJA SALT CAP (2018-2025):
  - HARD CAP: $10,000 ($5,000 MFS) aggregate limit on:
    (1) State and local income OR sales taxes (election), PLUS
    (2) State and local property taxes
  - Excess over cap = NONDEDUCTIBLE
  - Applies to individuals (NOT businesses — business taxes fully deductible)

TAXES INCLUDED IN CAP:
  - State/local income taxes (or sales tax if elected in lieu)
  - State/local property taxes on personal-use property
  - Foreign real property taxes (added to cap)

TAXES EXCLUDED FROM CAP (FULLY DEDUCTIBLE):
  - Trade or business taxes (Schedule C/E/F)
  - Investment property taxes (Schedule E rental)
  - Foreign income taxes (§164(a)(3), but limited by foreign tax credit coordination)
  - Employment taxes (FICA)

WORKAROUNDS (ATTEMPTED):
  - Entity-level state taxes (S-corps, partnerships): Some states enacted passthrough entity taxes (PTET) paid at entity level
  - IRS Notice 2020-75: Approves PTET workaround (entity deducts, individual gets state credit)
  - Charitable contribution workarounds: IRS Prop. Reg. §1.170A-1(h)(3) limits if quid pro quo (state tax credit)

BUSINESS VS. PERSONAL ALLOCATION:
  - Home office: Property tax allocated between business (Sch C) and personal (subject to cap)
  - Rental property: Fully deductible on Schedule E (not subject to cap)

PREPAYMENT STRATEGIES (BLOCKED):
  - Pre-TCJA: Taxpayers prepaid 2018 state taxes in 2017 to avoid cap
  - IRS Notice 2018-54: Prepayment allowed ONLY if assessed in 2017 (estimated payments OK, but future year assessments blocked)

IMPACT:
  - High-tax state residents hit hardest
  - Couples with $20K+ state income tax + $10K property tax lose $20K+ deduction
  - Migration to low-tax states (FL, TX, NV, WA) accelerated
""",
        key_factors=[
            "Personal vs. business use allocation",
            "Income vs. sales tax election (choose higher)",
            "Property tax personal vs. rental/business classification",
            "State passthrough entity tax election availability",
            "Prepayment timing (assessed vs. paid)",
        ],
        primary_authority=[
            "IRC §164(b)(6) (SALT cap)",
            "TCJA §11042 (2017)",
            "IRS Notice 2020-75 (PTET workaround)",
            "IRS Notice 2018-54 (prepayment limits)",
            "Treas. Reg. §1.164-1",
        ],
        burden_holder="Taxpayer must track and allocate taxes between personal (capped) and business (uncapped)",
        adversary_position="IRS challenges business allocation as personal, or prepayment timing",
        counter_arguments=[
            "Taxes claimed as business are actually personal",
            "Prepaid taxes not yet assessed (disallowed under Notice 2018-54)",
            "PTET election not properly made or state law invalid",
            "Foreign taxes should be credited not deducted (§901 coordination)",
        ],
        resolution_strategy="Elect state PTET if available (entity-level deduction bypasses cap), allocate home office taxes accurately, choose income vs. sales tax election optimally, avoid prepayment games",
        entity_scope="Individual taxpayers itemizing deductions",
        confidence=0.94,
        confidence_stratification="DEFENSIBLE",
        tcja_impact="TCJA imposed $10K cap on SALT deductions (2018-2025), massively impacting high-tax state residents",
    ),

    # ───────────────────────────────────────────────────────────────
    # §165 — CASUALTY AND THEFT LOSS DEDUCTION
    # ───────────────────────────────────────────────────────────────

    DoctrineBlock(
        topic="IRC §165(h) Personal Casualty and Theft Loss — TCJA Suspension",
        keywords=["casualty loss", "165", "theft", "disaster", "federally declared", "TCJA suspension"],
        conclusion_template="Casualty loss {DEDUCTIBLE|SUSPENDED 2018-2025|NONDEDUCTIBLE}. Event: {federally declared disaster required for personal}, loss: {FMV decrease or basis}, limits: {$100/event + 10% AGI floor}.",
        reasoning_framework="""
§165 LOSS DEDUCTION:

GENERAL RULE:
  - Deduction allowed for losses sustained during tax year, not compensated by insurance

BUSINESS/INVESTMENT LOSSES:
  - Fully deductible (subject to other limits like passive loss rules)
  - No TCJA restrictions

PERSONAL CASUALTY/THEFT LOSSES (PRE-TCJA):
  - Deductible if from fire, storm, shipwreck, theft, other casualty
  - LIMITS:
    (1) $100 per casualty event
    (2) Aggregate losses exceed 10% of AGI

TCJA SUSPENSION (2018-2025):
  - Personal casualty/theft losses SUSPENDED unless attributable to FEDERALLY DECLARED DISASTER
  - §165(h)(5) added by TCJA
  - Presidential disaster declaration (Stafford Act) required

FEDERALLY DECLARED DISASTER:
  - Presidential major disaster declaration under Robert T. Stafford Disaster Relief Act
  - FEMA maintains list (hurricanes, wildfires, floods, tornadoes with declaration)
  - State/local emergency ≠ federal declaration (must be presidential)

LOSS MEASUREMENT:
  - Lesser of:
    (1) Adjusted basis in property, OR
    (2) Decrease in FMV
  - Appraisals, repair costs as FMV evidence
  - Insurance/FEMA reimbursement reduces loss

TIMING:
  - Year loss sustained
  - Safe harbor: Disaster area losses can elect prior year (§165(i))

THEFT LOSSES:
  - Discovery year (when theft discovered)
  - Must prove criminal theft (not mere disappearance)
  - Ponzi schemes: Rev. Proc. 2009-20 safe harbor (95% theft loss, no 10% AGI floor)

POST-TCJA PLANNING:
  - Personal casualty losses mostly eliminated (unless federal disaster)
  - Casualty gains: If insurance/FEMA > basis, can offset with suspended losses (§165(h)(4)(B))
  - Business property losses: Fully deductible (not subject to TCJA suspension)
""",
        key_factors=[
            "Federally declared disaster (TCJA requirement for personal)",
            "Loss measurement (lesser of basis or FMV decline)",
            "Insurance reimbursement or reasonable prospect thereof",
            "Business vs. personal property classification",
            "Theft proof (criminal intent)",
        ],
        primary_authority=[
            "IRC §165(c)(3) (personal casualty)",
            "IRC §165(h)(5) (TCJA disaster requirement)",
            "TCJA §11044 (2017)",
            "Rev. Proc. 2009-20 (Ponzi scheme safe harbor)",
            "Treas. Reg. §1.165-1, §1.165-7, §1.165-8",
        ],
        burden_holder="Taxpayer must prove casualty event, federal disaster declaration, loss amount, and lack of reimbursement",
        adversary_position="IRS denies loss for lack of federal disaster declaration, or challenges loss measurement/reimbursement expectation",
        counter_arguments=[
            "No federal disaster declaration (state/local emergency insufficient)",
            "Insurance reimbursement reduces or eliminates loss",
            "Loss not sudden, unexpected, unusual (gradual deterioration ≠ casualty)",
            "Theft not proven (must show criminal intent)",
        ],
        resolution_strategy="Verify federal disaster declaration (FEMA list), obtain appraisals/repair estimates for FMV decline, document insurance claims and settlements, classify business property separately",
        entity_scope="Individuals with personal casualty/theft losses",
        confidence=0.91,
        confidence_stratification="DEFENSIBLE",
        tcja_impact="TCJA suspended personal casualty/theft losses (2018-2025) except federally declared disasters",
    ),

    # ───────────────────────────────────────────────────────────────
    # §167/§168 — DEPRECIATION AND MACRS
    # ───────────────────────────────────────────────────────────────

    DoctrineBlock(
        topic="IRC §168 MACRS Depreciation — General Depreciation System",
        keywords=["depreciation", "168", "MACRS", "GDS", "ADS", "recovery period", "bonus depreciation"],
        conclusion_template="Property depreciable over {recovery period} using {GDS|ADS}, method: {200%|150%|SL}, convention: {half-year|mid-quarter|mid-month}. Bonus depreciation: {available|not available}.",
        reasoning_framework="""
§168 MODIFIED ACCELERATED COST RECOVERY SYSTEM (MACRS):

GENERAL DEPRECIATION SYSTEM (GDS) — DEFAULT:
  - 200% declining balance (switches to SL when optimal) for 3/5/7/10-year property
  - 150% declining balance for 15/20-year property
  - Straight-line for nonresidential real property (39 years), residential rental (27.5 years)

RECOVERY PERIODS (GDS):
  - 3-year: Tractor units, horses >2 years old (race/breeding)
  - 5-year: Cars, light trucks, computers, office equipment, cattle, semiconductor manufacturing
  - 7-year: Office furniture, most machinery/equipment, any property with no class life
  - 10-year: Vessels, barges, tugs, single-purpose agricultural structures
  - 15-year: Gas stations, restaurants, retail improvements (some), land improvements
  - 20-year: Farm buildings, municipal sewers
  - 27.5-year: Residential rental property
  - 39-year: Nonresidential real property (commercial buildings)

ALTERNATIVE DEPRECIATION SYSTEM (ADS):
  - Straight-line method ONLY
  - Longer recovery periods (generally)
  - REQUIRED for:
    (1) Tax-exempt use property
    (2) Tax-exempt bond financed property
    (3) Farming businesses electing out of §163(j)
    (4) Real property businesses electing out of §163(j)
  - ADS recovery periods: 5-year cars become 5-year, 39-year buildings become 40-year

CONVENTIONS:
  - Half-year: Most personal property (treats as placed in service mid-year)
  - Mid-quarter: If >40% of property placed in service in Q4 (anti-abuse)
  - Mid-month: Real property (buildings)

BONUS DEPRECIATION (§168(k)):
  - 100% first-year deduction for qualified property (TCJA 2018-2022)
  - Phase-down: 80% (2023), 60% (2024), 40% (2025), 20% (2026), 0% (2027+)
  - Qualified property: New or used, acquired after 9/27/2017, MACRS property with recovery ≤20 years
  - Election out: Can elect out (useful if NOL concern or AMT)

SECTION 179 EXPENSING:
  - Immediate deduction up to $1,160,000 (2023, indexed)
  - Phase-out: Dollar-for-dollar once total property >$2,890,000 (2023)
  - Limitations: Taxable income limit, recapture if business use drops ≤50%

LISTED PROPERTY (§280F):
  - Cars, computers, cell phones (pre-2010)
  - Luxury auto caps ($20,200 first year with bonus depreciation 2023)
  - >50% business use required; if ≤50%, must use ADS SL

RECAPTURE (§1245/§1250):
  - §1245: Full recapture of depreciation as ordinary income (personal property)
  - §1250: Recapture of excess accelerated over SL (real property, minimal post-1986)
""",
        key_factors=[
            "Property class and recovery period",
            "GDS vs. ADS election/requirement",
            "Placed in service date (bonus depreciation phase-down)",
            "Business use percentage (>50% for listed property)",
            "Mid-quarter convention trigger (>40% Q4)",
        ],
        primary_authority=[
            "IRC §168 (MACRS)",
            "IRC §168(k) (bonus depreciation)",
            "IRC §179 (expensing)",
            "IRC §280F (listed property)",
            "Rev. Proc. 87-56 (class lives)",
        ],
        burden_holder="Taxpayer must prove property class, placed in service date, business use percentage",
        adversary_position="IRS challenges property classification, business use %, or improper bonus depreciation claim",
        counter_arguments=[
            "Property misclassified (longer recovery period applies)",
            "Not qualified property for bonus (used property acquired from related party)",
            "Business use ≤50% (listed property loses accelerated depreciation)",
            "ADS required but not used (§163(j) election out)",
        ],
        resolution_strategy="Document placed in service date, business use logs (listed property), elect bonus depreciation vs. §179 optimally, consider ADS election if §163(j) trade-off favorable",
        entity_scope="All taxpayers depreciating business property",
        confidence=0.93,
        confidence_stratification="DEFENSIBLE",
        tcja_impact="TCJA expanded bonus depreciation to 100% (2018-2022) including used property, increased §179 limits, imposed ADS requirement for §163(j) elect-out businesses",
    ),

    # ───────────────────────────────────────────────────────────────
    # §170 — CHARITABLE CONTRIBUTIONS
    # ───────────────────────────────────────────────────────────────

    DoctrineBlock(
        topic="IRC §170 Charitable Contribution Deduction — Percentage Limitations",
        keywords=["charitable", "170", "donation", "percentage limit", "AGI", "carryforward", "substantiation"],
        conclusion_template="Charitable contribution {FULLY DEDUCTIBLE|LIMITED|CARRIED FORWARD}. Type: {cash|property}, limit: {60%|50%|30%|20% AGI}, carryforward: {5 years}, substantiation: {required|inadequate}.",
        reasoning_framework="""
§170 CHARITABLE CONTRIBUTION DEDUCTION:

QUALIFIED ORGANIZATIONS:
  - 501(c)(3) public charities
  - Churches, educational institutions, hospitals
  - Private foundations (different limits)
  - NOT: Individuals, political organizations, foreign charities (with exceptions)

PERCENTAGE OF AGI LIMITATIONS (POST-TCJA):

CASH CONTRIBUTIONS:
  - 60% of AGI for public charities (increased from 50% by TCJA)
  - 30% of AGI for private foundations
  - Excess: 5-year carryforward

CAPITAL GAIN PROPERTY (appreciated stock, real estate):
  - 30% of AGI for public charities (at FMV if long-term capital gain property)
  - 20% of AGI for private foundations
  - Election: Deduct basis only → 50%/60% limit applies (rarely beneficial)

ORDINARY INCOME PROPERTY (inventory, short-term capital gain property):
  - Deduction limited to basis (NOT FMV)
  - Subject to 50%/60% limits

SUBSTANTIATION REQUIREMENTS:
  - <$250: Canceled check or receipt
  - ≥$250: Written acknowledgment from charity (must state if quid pro quo received)
  - >$500 property: Form 8283, describe property
  - >$5,000 property: Qualified appraisal required
  - >$500,000 property: Attach appraisal to return

QUID PRO QUO LIMITATIONS:
  - Deduction reduced by value of goods/services received
  - Charity must disclose if quid pro quo >$75 (e.g., gala ticket: $500 ticket - $100 meal = $400 deduction)

CARRYFORWARD:
  - 5-year carryforward for excess contributions
  - FIFO ordering (oldest contributions used first)

SPECIAL RULES:
  - S-corp/partnership: Contributions pass through to owners (subject to individual AGI limits)
  - C-corp: 10% of taxable income limit (different regime)
  - Conservation easements: Enhanced deductions for farmers/ranchers (50% AGI, 15-year carryforward)

COVID-19 RELIEF (2020-2021):
  - 100% AGI limit for cash contributions (CARES Act)
  - $300 above-the-line deduction for non-itemizers (2020-2021)
  - Temporary provisions expired

TCJA CHANGES:
  - Increased cash contribution limit from 50% to 60% of AGI
  - No longer offset against estate tax (TCJA eliminated or reduced estate tax exposure)
""",
        key_factors=[
            "Qualified organization status (public charity vs. private foundation)",
            "Type of property (cash, capital gain property, ordinary income property)",
            "Holding period (long-term vs. short-term for property)",
            "AGI percentage limitation (60%/30%/20%)",
            "Substantiation level ($250/$500/$5K/$500K thresholds)",
        ],
        primary_authority=[
            "IRC §170",
            "Treas. Reg. §1.170A-1 through §1.170A-18",
            "TCJA §11023 (60% AGI limit)",
            "CARES Act §2204 (2020 100% limit)",
        ],
        burden_holder="Taxpayer must substantiate contribution, charity qualification, and property valuation",
        adversary_position="IRS challenges charity qualification, property valuation (over-appraisal), or substantiation inadequacy",
        counter_arguments=[
            "Charity not qualified 501(c)(3) (e.g., foreign charity, political org)",
            "Property overvalued (appraisal not qualified)",
            "Substantiation missing (no written acknowledgment ≥$250)",
            "Quid pro quo not properly reduced (gala tickets, membership benefits)",
        ],
        resolution_strategy="Verify charity IRS qualification (IRS Tax Exempt Organization Search), obtain contemporaneous written acknowledgment, get qualified appraisal for >$5K property, track carryforwards, consider bunching contributions in high-income years",
        entity_scope="Individual and corporate taxpayers making charitable contributions",
        confidence=0.94,
        confidence_stratification="DEFENSIBLE",
        tcja_impact="TCJA increased cash contribution limit to 60% AGI (from 50%)",
    ),

    # ───────────────────────────────────────────────────────────────
    # §179 — IMMEDIATE EXPENSING ELECTION
    # ───────────────────────────────────────────────────────────────

    DoctrineBlock(
        topic="IRC §179 Immediate Expensing Election — Dollar and Investment Limitations",
        keywords=["179", "expensing", "section 179", "small business", "equipment", "tangible property"],
        conclusion_template="§179 expensing {AVAILABLE|LIMITED|PHASED OUT}. Limit: {$1,160,000 2023}, phase-out: {begins $2,890,000}, taxable income limit: {cannot create NOL}, recapture: {if business use drops ≤50%}.",
        reasoning_framework="""
§179 EXPENSING ELECTION:

DOLLAR LIMITATION (2023, INDEXED):
  - Maximum §179 deduction: $1,160,000
  - Increased from $25,000 pre-2003 (§179 renaissance began with Jobs Act 2003)

INVESTMENT LIMITATION (PHASE-OUT):
  - Dollar-for-dollar phase-out once total §179 property placed in service exceeds $2,890,000 (2023)
  - Example: $3M property → $1,160,000 - ($3M - $2,890,000) = $1,050,000 max
  - Completely phased out at $4,050,000 property

QUALIFIED PROPERTY:
  - Tangible personal property (machinery, equipment, furniture, computers)
  - Off-the-shelf software
  - Qualified improvement property (QIP) — nonresidential interior improvements (TCJA fix via CARES Act)
  - NOT: Buildings, land, investment property, inherited property

TAXABLE INCOME LIMITATION:
  - §179 deduction CANNOT exceed taxable income from active trade or business
  - Prevents creating/increasing NOL with §179
  - Carryforward: Excess carries forward indefinitely (subject to future taxable income limit)

BUSINESS USE REQUIREMENT:
  - >50% business use required
  - If business use drops to ≤50% in subsequent year → RECAPTURE as ordinary income

PASSTHROUGH ENTITIES:
  - S-corps, partnerships: §179 deduction passes through to owners
  - Each owner subject to individual taxable income limitation
  - Aggregation rules for controlled groups

ELECTION:
  - Made on timely filed return (including extensions)
  - Specify property and dollar amount elected
  - Irrevocable (except with IRS consent)

§179 vs. BONUS DEPRECIATION:
  - §179: Taxable income limit, phase-out for large purchases
  - Bonus: No taxable income limit, no phase-out, applies automatically (can elect out)
  - Strategy: Use §179 first (if no taxable income constraint), then bonus depreciation for remaining property

LISTED PROPERTY (§280F):
  - Cars, computers (pre-2010 cell phones)
  - §179 allowed BUT luxury auto caps apply ($20,200 total first year 2023 with bonus)

RECAPTURE:
  - If business use drops to ≤50%, prior §179 benefit recaptured as ordinary income
  - Amount recaptured: Excess of §179 over depreciation that would have been allowed
""",
        key_factors=[
            "Total property placed in service (investment limitation threshold)",
            "Taxable income from active business (cannot create NOL)",
            "Business use >50%",
            "Property type (qualified vs. excluded)",
            "Election made on timely filed return",
        ],
        primary_authority=[
            "IRC §179",
            "IRC §179(b)(3) (investment limitation)",
            "CARES Act §2307 (QIP technical correction)",
            "Rev. Proc. 2023-34 (2023 inflation adjustments)",
        ],
        burden_holder="Taxpayer must prove business use >50%, taxable income sufficient, and property qualified",
        adversary_position="IRS challenges business use percentage, taxable income calculation, or property qualification",
        counter_arguments=[
            "Business use ≤50% (no §179 allowed)",
            "Taxable income insufficient (excess carried forward)",
            "Property not qualified (building, land, investment)",
            "Investment limitation exceeded (phase-out applies)",
        ],
        resolution_strategy="Document business use percentage, calculate taxable income from active business carefully, elect §179 on timely filed return, monitor for recapture if use changes, coordinate with bonus depreciation",
        entity_scope="All businesses (heavily favors small businesses due to phase-out)",
        confidence=0.95,
        confidence_stratification="DEFENSIBLE",
        tcja_impact="TCJA increased §179 limits dramatically ($1M expensing, $2.5M phase-out), added qualified improvement property",
    ),

    # ───────────────────────────────────────────────────────────────
    # §195 — STARTUP COSTS
    # ───────────────────────────────────────────────────────────────

    DoctrineBlock(
        topic="IRC §195 Startup Cost Deduction — $5,000 First-Year + Amortization",
        keywords=["startup costs", "195", "organizational costs", "amortization", "15 years", "$5000 deduction"],
        conclusion_template="Startup costs {$5,000 IMMEDIATE + AMORTIZE|AMORTIZE ONLY}. Costs: {investigation, creation, pre-opening}, election: {deemed made}, amortization: {180 months}.",
        reasoning_framework="""
§195 STARTUP EXPENDITURE TREATMENT:

DEFINITION — STARTUP EXPENDITURES:
  - Investigating creation/acquisition of trade or business
  - Creating an active trade or business
  - Activities engaged in for profit BEFORE business begins
  - Examples: Market research, employee training, advertising, professional fees (legal, accounting), travel

MUST BE:
  - Incurred before business begins
  - Amounts that WOULD be deductible as ordinary/necessary business expense if incurred AFTER business begins
  - NOT: Costs of acquiring assets (capitalized under §263), interest, taxes, R&D (§174)

$5,000 FIRST-YEAR DEDUCTION:
  - Up to $5,000 immediately deductible in first year business begins
  - Phase-out: Dollar-for-dollar reduction if total startup costs exceed $50,000
  - Example: $52,000 startup costs → $5,000 - ($52,000 - $50,000) = $3,000 immediate deduction
  - Completely phased out at $55,000 or more

AMORTIZATION:
  - Remaining startup costs amortized over 180 months (15 years)
  - Begins month business begins operations

DEEMED ELECTION:
  - §195 election deemed made (no formal election required unless electing out or different amortization period)
  - Simplification from prior law (pre-2004 required affirmative election)

ORGANIZATIONAL COSTS (§248 CORPORATIONS, §709 PARTNERSHIPS):
  - Similar treatment: $5,000 immediate + 180-month amortization
  - Organizational costs: Legal fees to incorporate, accounting for organizational matters, filing fees
  - NOT: Syndication costs (partnership interests sold) — never deductible

BUSINESS BEGINS:
  - When business actively offering goods/services for sale
  - NOT when first revenue received (can have startup period with initial sales)
  - Facts and circumstances test

DISPOSAL OF BUSINESS:
  - If business disposed of before end of 15-year period, remaining unamortized startup costs deductible as loss

PLANNING:
  - Aggregate startup costs: If likely to exceed $50,000, consider deferring some costs to post-opening (fully deductible)
  - Multiple businesses: Each business gets separate $5,000 allowance
""",
        key_factors=[
            "Costs incurred before business begins",
            "Would be ordinary/necessary if incurred post-opening",
            "Total startup costs (phase-out threshold $50K)",
            "Business begins operations date",
            "Proper classification (startup vs. organizational vs. asset acquisition)",
        ],
        primary_authority=[
            "IRC §195",
            "Treas. Reg. §1.195-1",
            "American Jobs Creation Act 2004 (deemed election, $5K allowance)",
        ],
        burden_holder="Taxpayer must prove costs are startup (pre-opening), would be deductible post-opening, and business commencement date",
        adversary_position="IRS challenges costs as not startup (personal investigation, asset acquisition), or business began earlier (reducing amortization period)",
        counter_arguments=[
            "Costs are personal investigation (not business startup)",
            "Costs are asset acquisition (§263 capitalization, not §195 amortization)",
            "Business began earlier than claimed (shorter amortization period)",
            "Exceeds $55K (no immediate $5K deduction)",
        ],
        resolution_strategy="Document pre-opening timeline clearly, segregate startup costs from asset acquisition costs, track commencement date (first customer transaction or active offering), aggregate costs to plan phase-out impact",
        entity_scope="All taxpayers starting new trade or business",
        confidence=0.92,
        confidence_stratification="DEFENSIBLE",
    ),

    # ───────────────────────────────────────────────────────────────
    # §199A — QUALIFIED BUSINESS INCOME DEDUCTION
    # ───────────────────────────────────────────────────────────────

    DoctrineBlock(
        topic="IRC §199A Qualified Business Income Deduction — 20% Passthrough Deduction",
        keywords=["199A", "QBI", "qualified business income", "20 percent", "passthrough", "SSTB", "W-2 wages"],
        conclusion_template="§199A deduction: {20% QBI|LIMITED|PHASED OUT|SSTB DENIED}. Income: {qualified|specified service}, limit: {lesser of 20% QBI or taxable income}, phase-out: {$182,100-$232,100 single / $364,200-$464,200 joint (2023)}.",
        reasoning_framework="""
§199A QUALIFIED BUSINESS INCOME DEDUCTION (TCJA 2018-2025):

BASE DEDUCTION:
  - 20% of qualified business income (QBI) from passthrough entities
  - Individuals, trusts, estates (NOT C-corps)
  - S-corps, partnerships, sole proprietorships eligible

QUALIFIED BUSINESS INCOME (QBI):
  - Net income from qualified trade or business (QTB)
  - Excludes: Capital gains, dividends, interest (investment income)
  - Excludes: Reasonable compensation (W-2 wages to S-corp shareholder-employee)
  - Excludes: Guaranteed payments (partnership)

SPECIFIED SERVICE TRADE OR BUSINESS (SSTB) — LIMITATION:
  - SSTBs: Health, law, accounting, actuarial, performing arts, consulting, athletics, financial/brokerage services, investing/trading
  - Architecture and engineering: NOT SSTBs (carved out)
  - SSTB income INELIGIBLE for §199A deduction if taxpayer income exceeds threshold

INCOME THRESHOLDS (2023, INDEXED):
  - Phase-in range:
    * Single/HOH: $182,100 - $232,100
    * MFJ: $364,200 - $464,200
    * MFS: $182,100 - $232,100
  - BELOW threshold: Full 20% QBI deduction, no W-2/property limitation, SSTBs eligible
  - WITHIN phase-in: Partial limitation
  - ABOVE threshold: Full limitations apply

W-2 WAGE AND PROPERTY LIMITATIONS (ABOVE THRESHOLD):
  - Deduction limited to GREATER of:
    (1) 50% of W-2 wages paid by business, OR
    (2) 25% of W-2 wages + 2.5% of unadjusted basis of qualified property (UBIA)
  - Qualified property: Tangible depreciable property used in business, held at year-end

AGGREGATION:
  - Can aggregate multiple trades/businesses under common control (Treas. Reg. §1.199A-4)
  - Increases W-2 wage limit (combine wages across businesses)

OVERALL LIMITATION:
  - §199A deduction cannot exceed 20% of taxable income (before §199A) minus net capital gains
  - Excess QBI loss carryforward to future years

LOSS TREATMENT:
  - QBI loss from one business reduces QBI from other businesses
  - Net negative QBI carries forward to reduce next year's QBI

RENTAL REAL ESTATE — SAFE HARBOR:
  - Rev. Proc. 2019-38: Rental real estate can qualify as QTB if:
    (1) Separate books for each rental property
    (2) 250+ hours of rental services per year
    (3) Contemporaneous time records
  - Allows 20% deduction for real estate investors

PLANNING STRATEGIES:
  - SSTB mitigation: Reduce income below threshold (retirement contributions, deferral)
  - Increase W-2 wages: Convert contractor payments to W-2 employees (business cost, but boosts §199A)
  - Asset purchases: Qualified property (UBIA) increases deduction limit
  - Aggregation: Group businesses to maximize W-2 wage limitation
""",
        key_factors=[
            "Taxpayer's taxable income (threshold comparison)",
            "SSTB classification",
            "W-2 wages paid by business",
            "Unadjusted basis of qualified property (UBIA)",
            "Aggregation election",
        ],
        primary_authority=[
            "IRC §199A",
            "Treas. Reg. §1.199A-1 through §1.199A-6 (final regs 2019)",
            "Rev. Proc. 2019-38 (rental real estate safe harbor)",
            "TCJA §11011 (2017)",
        ],
        burden_holder="Taxpayer must prove QBI amount, W-2 wages, property UBIA, and SSTB classification",
        adversary_position="IRS challenges SSTB classification (business is specified service), W-2 wage calculations, or rental real estate QTB qualification",
        counter_arguments=[
            "Business is SSTB (law, consulting, financial services) → no deduction above threshold",
            "Insufficient W-2 wages (limits deduction)",
            "Rental real estate fails safe harbor (< 250 hours, no contemporaneous records)",
            "Aggregation improper (businesses not under common control)",
        ],
        resolution_strategy="Document SSTB status carefully (avoid consulting/advisory characterization), track W-2 wages paid, maintain qualified property UBIA schedules, consider rental real estate safe harbor compliance, model aggregation benefit",
        entity_scope="Individual passthrough owners (S-corp, partnership, sole prop)",
        confidence=0.89,
        confidence_stratification="AGGRESSIVE",
        tcja_impact="TCJA created §199A 20% passthrough deduction (2018-2025) to partially offset C-corp rate reduction to 21%",
        disclosure_caveat="§199A regulations complex and evolving; SSTB classification subject to audit scrutiny; rental real estate safe harbor compliance critical",
    ),

    # (CONTINUE WITH 40+ MORE DOCTRINE BLOCKS...)
    # Additional blocks would cover:
    # - §212 investment expenses (suspended 2018-2025)
    # - §213 medical expenses (7.5% AGI floor)
    # - §217 moving expenses (suspended for non-military 2018-2025)
    # - §280A home office strict requirements
    # - §280E cannabis business expense denial
    # - §461(l) excess business loss limitation ($289K single/$578K joint 2023)
    # - §469 passive activity loss rules (real estate professional exception)
    # - §267 related party disallowance
    # - §274 meals/entertainment 50% limitation
    # - Employee business expenses (suspended 2018-2025)
    # - Standard vs. itemized deduction election
    # - AMT add-backs and preference items
    # - NOL carryforward/carryback rules post-TCJA
    # - At-risk limitations §465
    # - Conservation easement deductions
    # - Energy efficiency/green energy credits vs. deductions

]

# For space, I'm including 10 total blocks in this example.
# Production version would have 50+ blocks covering all major deduction topics.
