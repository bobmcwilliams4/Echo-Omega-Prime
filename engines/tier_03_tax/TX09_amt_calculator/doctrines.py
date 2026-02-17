"""
TX09 AMT CALCULATOR — DOCTRINE CACHE
Pre-compiled expert reasoning blocks for Alternative Minimum Tax analysis.

Domain: IRC §55-59 Alternative Minimum Tax framework
Authority: 11.0 SOVEREIGN
Version: 1.0.0
"""

from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum


class IssueCategory(str, Enum):
    """Issue categories for AMT analysis."""
    CALCULATION = "calculation"
    ADJUSTMENTS = "adjustments"
    PREFERENCES = "preferences"
    EXEMPTION = "exemption"
    CREDITS = "credits"
    PLANNING = "planning"
    COMPLIANCE = "compliance"
    ENTITIES = "entities"


class Stratification(str, Enum):
    """Confidence stratification tiers."""
    DEFENSIBLE = "defensible"
    AGGRESSIVE_SUPPORTABLE = "aggressive_supportable"
    DISCLOSURE_RECOMMENDED = "disclosure_recommended"
    HIGH_AUDIT_RISK = "high_audit_risk"


class ConfidenceStratification(str, Enum):
    """Alias for Stratification to match TIE pattern."""
    DEFENSIBLE = "defensible"
    AGGRESSIVE_SUPPORTABLE = "aggressive_supportable"
    DISCLOSURE_RECOMMENDED = "disclosure_recommended"
    HIGH_AUDIT_RISK = "high_audit_risk"


@dataclass
class DoctrineBlock:
    """Pre-compiled expert reasoning block for AMT analysis."""
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
    category: Optional[IssueCategory] = None
    related_doctrines: List[str] = field(default_factory=list)


# ============================================================================
# DOCTRINE CACHE — 50+ AMT EXPERTISE BLOCKS
# ============================================================================

DOCTRINE_CACHE = [
    # IRC §55 — AMT Framework
    DoctrineBlock(
        topic="AMT Calculation Framework IRC §55",
        keywords=["alternative minimum tax", "amt calculation", "tentative minimum tax", "§55", "section 55"],
        conclusion_template=[
            "Alternative minimum tax is imposed under IRC §55 when tentative minimum tax exceeds regular tax liability.",
            "Tentative minimum tax is calculated by applying AMT rates to alternative minimum taxable income (AMTI) less the AMT exemption amount.",
            "AMT liability equals the excess of tentative minimum tax over regular tax, creating a parallel tax system."
        ],
        reasoning_framework="""IRC §55(a) imposes alternative minimum tax on taxpayers equal to the excess (if any) of
tentative minimum tax over regular tax for the taxable year. This creates a parallel tax calculation system designed to
ensure minimum tax payment regardless of deductions and preferences. The tentative minimum tax calculation starts with
alternative minimum taxable income (AMTI), reduces it by the applicable exemption amount (subject to phase-out), and
applies graduated AMT rates. For 2024, AMT rates are 26% on the first $220,700 of AMT base ($110,350 for married filing
separately) and 28% on amounts above that threshold. The exemption amount for 2024 is $85,700 for singles, $133,300 for
married filing jointly, and begins phasing out at $609,350/$1,218,700 respectively at a 25% rate. Corporate AMT was
repealed by TCJA for tax years beginning after 2017, but the Inflation Reduction Act 2022 introduced a new 15% corporate
alternative minimum tax (CAMT) on adjusted financial statement income for corporations with average annual adjusted
financial statement income exceeding $1 billion. Individual AMT persists post-TCJA with increased exemption amounts.""",
        key_factors=[
            "Tentative minimum tax calculation methodology",
            "AMT rates: 26% base, 28% excess over threshold",
            "Exemption amounts and phase-out thresholds indexed for inflation",
            "AMT applies only if tentative minimum tax exceeds regular tax",
            "TCJA increased exemption amounts and phase-out thresholds",
            "Parallel calculation system requires separate tracking",
            "Form 6251 required for AMT calculation and reporting"
        ],
        primary_authority=[
            "IRC §55(a) — Imposition of AMT",
            "IRC §55(b) — AMT rates and thresholds",
            "IRC §55(d) — Exemption amount and phase-out",
            "IRC §55(c) — Regular tax defined",
            "Rev Proc 2023-34 — 2024 inflation adjustments"
        ],
        burden_holder="Taxpayer bears burden of proving AMT calculation accuracy",
        adversary_position="IRS will challenge understated AMTI or overstated exemptions",
        counter_arguments=[
            "Exemption phase-out calculation errors are common audit targets",
            "Failure to include all §56 adjustments understates AMTI",
            "Failure to include all §57 preferences understates AMTI",
            "Incorrect filing status exemption amount applied",
            "AMT credits improperly claimed or calculated"
        ],
        resolution_strategy="Document all AMT calculations with contemporaneous workpapers; maintain dual-track tax records for regular and AMT; use Form 6251 as calculation template; verify all adjustments and preferences included; confirm correct exemption amount and phase-out calculation; retain supporting documentation for all AMTI components.",
        entity_scope=["individual", "estate", "trust"],
        confidence=0.95,
        confidence_stratification=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="IRC §55(a)",
        category=IssueCategory.CALCULATION
    ),

    # IRC §56 — AMT Adjustments
    DoctrineBlock(
        topic="AMT Adjustments IRC §56 — Depreciation and Timing",
        keywords=["amt adjustments", "depreciation", "§56", "section 56", "amti adjustments", "timing differences"],
        conclusion_template=[
            "IRC §56 requires specific adjustments to taxable income to compute AMTI, primarily addressing accelerated deductions.",
            "Depreciation adjustments require recalculation using ADS for property placed in service before 1999 or AMT depreciation lives.",
            "Post-TCJA, bonus depreciation and Section 179 are generally allowed for AMT purposes, eliminating major adjustment."
        ],
        reasoning_framework="""IRC §56 mandates adjustments to regular taxable income to arrive at AMTI, targeting items that
create timing differences or permanent exclusions. Pre-TCJA, depreciation adjustments were substantial: §56(a)(1) required
150% declining balance over ADS recovery period for personal property and straight-line over ADS for real property placed
in service before 1999. TCJA eliminated most depreciation adjustments for property placed in service after 2017, allowing
bonus depreciation and Section 179 for AMT. However, property placed in service pre-1999 still requires adjustment. Mining
exploration and development costs under §56(a)(2) must be capitalized and amortized over 10 years for AMT rather than
expensed. Long-term contract income under §56(a)(3) requires percentage-of-completion method for AMT rather than completed
contract. Pollution control facilities under §56(a)(5) require ADS depreciation. Installment sales of dealer property under
§56(a)(6) cannot use installment method for AMT. Loss limitations and passive activity loss rules apply differently for AMT.""",
        key_factors=[
            "Depreciation adjustment complexity depends on property placed-in-service date",
            "TCJA eliminated depreciation adjustment for most post-2017 property",
            "Pre-1999 property still requires ADS recalculation",
            "Mining costs capitalized for AMT vs. expensed for regular tax",
            "Long-term contracts use percentage-of-completion for AMT",
            "Installment method unavailable for AMT on dealer property",
            "Passive activity loss limitations computed separately for AMT"
        ],
        primary_authority=[
            "IRC §56(a)(1) — Depreciation adjustments",
            "IRC §56(a)(2) — Mining exploration and development",
            "IRC §56(a)(3) — Long-term contract income",
            "IRC §56(a)(5) — Pollution control facilities",
            "IRC §56(a)(6) — Installment sales",
            "TCJA §13201 — Bonus depreciation AMT conformity"
        ],
        burden_holder="Taxpayer must demonstrate proper adjustment calculations with supporting depreciation schedules",
        adversary_position="IRS audits focus on depreciation adjustment errors and incomplete identification of adjustable property",
        counter_arguments=[
            "Taxpayer failed to identify all pre-1999 property requiring adjustment",
            "ADS lives incorrectly applied in depreciation recalculation",
            "Bonus depreciation improperly claimed for AMT on pre-2018 property",
            "Mining costs improperly expensed for AMT",
            "Installment method improperly used for AMT on dealer sales"
        ],
        resolution_strategy="Maintain detailed property ledgers with placed-in-service dates; prepare dual depreciation schedules (regular vs AMT) for pre-1999 property; track cumulative timing differences; document method changes post-TCJA; maintain contemporaneous election documentation; use IRS depreciation tables for ADS lives.",
        entity_scope=["individual", "c_corporation", "partnership", "s_corporation", "estate", "trust"],
        confidence=0.90,
        confidence_stratification=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="IRC §56(a)(1)",
        category=IssueCategory.ADJUSTMENTS
    ),

    # IRC §57 — Tax Preference Items
    DoctrineBlock(
        topic="AMT Tax Preference Items IRC §57",
        keywords=["tax preferences", "§57", "section 57", "private activity bonds", "percentage depletion", "idc"],
        conclusion_template=[
            "IRC §57 requires adding back specific tax preference items to compute AMTI, targeting favored tax treatments.",
            "Private activity bond interest exempt for regular tax must be included in AMTI under §57(a)(5).",
            "Excess percentage depletion over basis and excess intangible drilling costs are key preference items."
        ],
        reasoning_framework="""IRC §57 identifies specific "items of tax preference" that must be added to taxable income in
computing AMTI. These represent permanent or long-term favorable tax treatments deemed inappropriate for minimum tax
purposes. Section 57(a)(5) requires inclusion of tax-exempt interest from private activity bonds issued after August 7,
1986, a major preference for high-net-worth individuals holding municipal bonds. However, qualified housing bonds and
§501(c)(3) bonds are excluded from this preference. Section 57(a)(1) requires adding excess percentage depletion (amount
claimed over property basis) for oil, gas, and mineral properties. Section 57(a)(2) addresses accelerated depreciation on
pre-1987 real and leased personal property, though this affects fewer taxpayers post-TCJA. Intangible drilling costs under
§57(a)(2) require adding back excess IDCs (amount over 10-year amortization) with a 65% of net oil/gas income limitation.
Post-TCJA changes eliminated several preferences but retained private activity bonds and natural resource preferences.""",
        key_factors=[
            "Private activity bond interest is major individual AMT preference",
            "Housing bonds and 501(c)(3) bonds excluded from preference",
            "Percentage depletion preference equals excess over basis",
            "IDC preference calculation includes 65% net income limitation",
            "Pre-1987 accelerated depreciation still relevant for older property",
            "Preferences are permanent additions, not timing differences",
            "Form 6251 Schedule requires preference item detail"
        ],
        primary_authority=[
            "IRC §57(a)(5) — Private activity bond interest",
            "IRC §57(a)(1) — Excess percentage depletion",
            "IRC §57(a)(2) — Intangible drilling costs",
            "IRC §57(a)(7) — Accelerated depreciation (pre-1987)",
            "Treas Reg §1.57-1 — Tax preference items"
        ],
        burden_holder="Taxpayer must identify and report all preference items; failure to report creates understatement exposure",
        adversary_position="IRS targets unreported private activity bond interest and natural resource preferences in high-income audits",
        counter_arguments=[
            "Private activity bond interest unreported or misclassified",
            "Taxpayer incorrectly excluded housing bonds from preference",
            "Percentage depletion preference understated due to basis errors",
            "IDC preference calculation omitted or 65% limitation misapplied",
            "Pre-1987 property depreciation preference not identified"
        ],
        resolution_strategy="Request bond classification from brokers annually; maintain detailed natural resource property records with basis tracking; document IDC elections and calculate 65% limitation; identify pre-1987 property still on books; reconcile Form 1099-INT and broker statements to AMT preferences; maintain technical memo on preference item identification.",
        entity_scope=["individual", "estate", "trust"],
        confidence=0.92,
        confidence_stratification=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="IRC §57(a)(5)",
        category=IssueCategory.PREFERENCES
    ),

    # IRC §55(d) — Exemption Amount and Phase-Out
    DoctrineBlock(
        topic="AMT Exemption Amount and Phase-Out IRC §55(d)",
        keywords=["amt exemption", "exemption phase-out", "§55(d)", "exemption amount", "phaseout threshold"],
        conclusion_template=[
            "IRC §55(d) provides exemption amounts that reduce AMTI before applying AMT rates, subject to income-based phase-out.",
            "For 2024, exemption amounts are $85,700 (single), $133,300 (married filing jointly), with phase-out beginning at $609,350/$1,218,700.",
            "Exemption phases out at 25% rate, creating effective marginal rate increase in phase-out range."
        ],
        reasoning_framework="""IRC §55(d)(1) establishes exemption amounts that function similarly to standard deduction in
regular tax calculation, reducing AMTI before rate application. However, unlike standard deduction, AMT exemption phases
out at high income levels under §55(d)(3), creating complex rate structure. For 2024 (indexed annually for inflation per
§55(d)(4)), exemption amounts are: $85,700 for singles and heads of household, $133,300 for married filing jointly, $66,650
for married filing separately, and $29,200 for estates and trusts. Phase-out begins at $609,350 for singles ($1,218,700 for
joint filers) with exemption reduced by 25 cents for each dollar of AMTI above threshold. This creates effective marginal
rate of 32.5% (26% base rate + 6.5% from phase-out) or 35% (28% base rate + 7% from phase-out) in the phase-out range.
Exemption fully phases out when AMTI reaches threshold plus 4x exemption amount. TCJA substantially increased exemption
amounts and phase-out thresholds through 2025, reducing AMT incidence. Pre-TCJA exemptions were approximately 40% lower.""",
        key_factors=[
            "Exemption amounts indexed annually for inflation",
            "Phase-out creates effective marginal rate increase of 6.5% or 7%",
            "Full phase-out occurs at threshold plus 4x exemption amount",
            "Filing status determines both exemption amount and phase-out threshold",
            "TCJA temporary increases sunset after 2025 without extension",
            "Married filing separately exemption exactly half of joint filer amount",
            "Estate and trust exemption substantially lower than individual amounts"
        ],
        primary_authority=[
            "IRC §55(d)(1) — Exemption amounts",
            "IRC §55(d)(3) — Phase-out mechanism",
            "IRC §55(d)(4) — Inflation adjustments",
            "Rev Proc 2023-34 — 2024 inflation-adjusted amounts",
            "TCJA §12003 — Increased exemption amounts 2018-2025"
        ],
        burden_holder="Taxpayer must correctly calculate phase-out based on AMTI and filing status",
        adversary_position="IRS will challenge incorrect exemption amounts or phase-out calculations in high-income cases",
        counter_arguments=[
            "Taxpayer used wrong filing status exemption amount",
            "Phase-out threshold incorrect for filing status",
            "Phase-out calculation mathematically incorrect (should be 25% of excess)",
            "Taxpayer failed to phase out exemption when AMTI exceeded threshold",
            "Wrong year exemption amount used (failed to adjust for inflation)"
        ],
        resolution_strategy="Use current year inflation-adjusted amounts from IRS revenue procedures; verify filing status consistency across return; calculate phase-out with precision (25% of excess over threshold); document exemption calculation on Form 6251; verify phase-out threshold matches filing status; prepare for post-2025 sunset of TCJA increases.",
        entity_scope=["individual", "estate", "trust"],
        confidence=0.95,
        confidence_stratification=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="IRC §55(d)(3)",
        category=IssueCategory.EXEMPTION
    ),

    # IRC §53 — AMT Credit
    DoctrineBlock(
        topic="AMT Credit Carryforward IRC §53",
        keywords=["amt credit", "minimum tax credit", "§53", "section 53", "mtc", "credit carryforward"],
        conclusion_template=[
            "IRC §53 allows credit for prior-year AMT attributable to timing differences (deferral preferences).",
            "Credit is limited to excess of regular tax over tentative minimum tax in carryforward year.",
            "Exclusion preferences (e.g., private activity bond interest) do not generate creditable AMT."
        ],
        reasoning_framework="""IRC §53 provides minimum tax credit (MTC) mechanism to mitigate double taxation from timing
difference AMT adjustments. When AMT is paid due to deferral items (depreciation, mining costs, passive losses, etc.),
those AMT amounts generate credits usable in future years when regular tax exceeds tentative minimum tax. However, §53(d)(1)
limits credits to AMT attributable to "adjusted net minimum tax," excluding AMT from exclusion preferences like private
activity bond interest, percentage depletion excess, and certain other permanent items. Credit carryforward is unlimited in
time, but annual utilization is limited to excess of regular tax over tentative minimum tax, preventing credit from reducing
tax below AMT level. Form 8801 calculates credit generation and utilization. TCJA §12001 added special rule allowing
refundability of unused pre-2018 credits: 50% refundable in 2018-2020, remainder refundable in 2021. Post-2017 credits
continue to be carryforward-only. Estates and trusts can pass through unused credits to beneficiaries upon termination under
§53(d)(1)(B)(i).""",
        key_factors=[
            "Only deferral preference AMT generates creditable amounts",
            "Exclusion preference AMT (PAB interest, depletion) not creditable",
            "Credit utilization limited to regular tax excess over tentative minimum tax",
            "Unlimited carryforward period for credits",
            "Pre-2018 credits partially refundable under TCJA transition rule",
            "Form 8801 required for credit tracking and utilization",
            "Estates/trusts pass through unused credits to beneficiaries on termination"
        ],
        primary_authority=[
            "IRC §53(a) — Minimum tax credit allowed",
            "IRC §53(c) — Credit limitation to regular tax excess",
            "IRC §53(d) — Adjusted net minimum tax computation",
            "IRC §53(e) — Carryforward rules",
            "TCJA §12001 — Pre-2018 credit refundability"
        ],
        burden_holder="Taxpayer must track credit generation and maintain multi-year records for carryforward substantiation",
        adversary_position="IRS will challenge credit claims lacking proper substantiation or including non-creditable exclusion preferences",
        counter_arguments=[
            "Taxpayer claimed credit for exclusion preference AMT (PAB interest)",
            "Credit calculation omitted adjusted net minimum tax limitation",
            "Utilization exceeded regular tax excess over tentative minimum tax",
            "Inadequate records to substantiate credit carryforward from prior years",
            "Failed to recapture credits upon property disposition"
        ],
        resolution_strategy="Maintain Form 8801 and supporting schedules for all years with AMT or credit activity; separately track deferral vs exclusion preference AMT amounts; document adjusted net minimum tax calculation; retain property records for credit recapture tracking; calculate annual credit limitation before claiming; consider TCJA refundability for pre-2018 credits.",
        entity_scope=["individual", "c_corporation", "estate", "trust"],
        confidence=0.88,
        confidence_stratification=ConfidenceStratification.AGGRESSIVE_SUPPORTABLE,
        controlling_precedent="IRC §53(d)(1)",
        category=IssueCategory.CREDITS
    ),

    # ISO Stock Options and AMT
    DoctrineBlock(
        topic="Incentive Stock Options and AMT IRC §56(b)(3)",
        keywords=["iso", "incentive stock options", "§56(b)(3)", "stock options amt", "exercise spread"],
        conclusion_template=[
            "IRC §56(b)(3) requires AMT adjustment for spread on incentive stock option exercise (FMV minus exercise price).",
            "Regular tax has no income on ISO exercise, but AMT includes spread in AMTI, creating substantial exposure.",
            "Disposition in same year as exercise eliminates AMT adjustment; disqualifying disposition triggers regular tax."
        ],
        reasoning_framework="""IRC §56(b)(3) creates major AMT trap for employees exercising incentive stock options. Under
regular tax rules (§422), ISO exercise creates no taxable income; income recognition deferred until stock sale. However, for
AMT purposes, the spread at exercise (fair market value minus exercise price) must be included in AMTI as compensation
adjustment. This creates significant AMT liability in exercise year with no cash to pay tax. The adjustment is timing
difference that reverses on stock sale, generating AMT credit under §53. However, if stock price declines after exercise,
taxpayer may have AMT liability exceeding ultimate gain. Special rule under §56(b)(3): if stock disposed in same calendar
year as exercise, no AMT adjustment (regular tax gain/loss applies). Disqualifying disposition (sale before end of 2-year
holding from grant or 1-year from exercise) eliminates AMT benefit but triggers regular tax ordinary income, potentially
beneficial if stock price declined. Post-exercise basis for AMT purposes is exercise price plus spread included in AMTI.
Planning requires careful coordination of exercise timing, AMT exposure calculation, and disposition strategy.""",
        key_factors=[
            "AMT spread = FMV at exercise minus exercise price",
            "Regular tax has zero income at exercise; AMT has full spread inclusion",
            "Same-year disposition eliminates AMT adjustment",
            "Disqualifying disposition converts to regular tax ordinary income",
            "Stock price decline post-exercise creates AMT trap (tax on unrealized gain)",
            "AMT adjustment creates future credit under IRC §53",
            "AMT basis in stock equals exercise price plus spread included in AMTI"
        ],
        primary_authority=[
            "IRC §56(b)(3) — ISO exercise AMT adjustment",
            "IRC §422 — ISO qualification rules",
            "IRC §421(a) — Regular tax deferral on ISO exercise",
            "IRC §424(c) — Disqualifying disposition",
            "Treas Reg §1.422-1 — ISO requirements"
        ],
        burden_holder="Taxpayer must report AMT adjustment and track dual basis (regular vs AMT); burden to substantiate FMV at exercise",
        adversary_position="IRS challenges understated FMV at exercise or failure to include spread in AMTI",
        counter_arguments=[
            "Taxpayer understated FMV at exercise to reduce AMT spread",
            "Failed to include ISO spread in AMTI calculation",
            "Incorrectly excluded spread claiming same-year disposition when sold in following year",
            "Failed to establish ISO qualification, spread should be regular tax W-2 income",
            "Overstated exercise price to reduce spread"
        ],
        resolution_strategy="Obtain contemporaneous FMV appraisal or 409A valuation at exercise; document ISO grant terms and exercise dates; calculate AMT exposure before exercising; consider same-year disposition to avoid AMT; track AMT credit generation from adjustment; maintain dual basis records; model disqualifying disposition scenarios; consider cashless exercise or exercise-and-hold strategies based on AMT position.",
        entity_scope=["individual"],
        confidence=0.90,
        confidence_stratification=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="IRC §56(b)(3)",
        category=IssueCategory.ADJUSTMENTS,
        related_doctrines=["AMT Credit IRC §53"]
    ),

    # State and Local Tax (SALT) and AMT Post-TCJA
    DoctrineBlock(
        topic="SALT Deduction Limitation and AMT Post-TCJA",
        keywords=["salt", "state and local tax", "§164(b)(6)", "amt salt", "tcja salt cap"],
        conclusion_template=[
            "IRC §164(b)(6) limits state and local tax deduction to $10,000 ($5,000 MFS) for regular tax post-TCJA.",
            "AMT historically disallowed SALT deduction entirely, but TCJA $10K cap paradoxically reduced AMT differential.",
            "Taxpayers with SALT exceeding $10K have smaller regular/AMT spread post-TCJA, reducing AMT incidence."
        ],
        reasoning_framework="""Pre-TCJA, state and local taxes were fully deductible for regular tax but completely disallowed
for AMT under former §56(b)(1)(A)(ii), creating substantial AMT exposure for high-income taxpayers in high-tax states. TCJA
§11042 imposed $10,000 cap ($5,000 married filing separately) on SALT deduction for regular tax years 2018-2025. This cap
substantially reduced the differential between regular tax and AMT for SALT purposes. For taxpayers with SALT exceeding
$10,000, the AMT adjustment is now limited to $10,000 (the capped deduction amount), whereas pre-TCJA it was the entire SALT
amount. Paradoxically, TCJA SALT cap reduced AMT incidence by narrowing regular/AMT tax base gap. However, AMT still applies
§56(b)(1)(A)(ii) full disallowance, meaning the $10K regular tax deduction creates $10K AMT adjustment. Taxpayers in low-tax
states with SALT under $10K have no AMT adjustment. High-income taxpayers in high-tax states still face AMT exposure but
less than pre-TCJA. Planning involves state tax payment timing, property tax prepayment (now limited), and entity selection
for pass-through businesses (PTET workarounds).""",
        key_factors=[
            "TCJA $10K SALT cap applies to regular tax 2018-2025",
            "AMT continues to disallow SALT deduction entirely",
            "AMT adjustment limited to lesser of actual SALT or $10K cap",
            "High-tax state residents have reduced AMT differential post-TCJA",
            "Property tax prepayment strategy eliminated by TCJA for tax years after 2017",
            "PTET (pass-through entity tax) workarounds may avoid SALT cap and AMT adjustment",
            "SALT cap scheduled to sunset after 2025 absent legislative extension"
        ],
        primary_authority=[
            "IRC §164(b)(6) — SALT deduction limitation",
            "IRC §56(b)(1)(A)(ii) — AMT SALT disallowance",
            "TCJA §11042 — SALT cap enactment",
            "Notice 2020-75 — PTET guidance",
            "Rev Rul 2020-17 — Charitable contribution SALT workaround limits"
        ],
        burden_holder="Taxpayer must substantiate SALT payments and demonstrate proper limitation calculation",
        adversary_position="IRS challenges SALT cap workarounds and timing manipulations; monitors PTET compliance",
        counter_arguments=[
            "Taxpayer improperly deducted SALT exceeding $10K for regular tax",
            "Failed to add back SALT deduction in AMT calculation",
            "Prepaid property taxes claimed in violation of TCJA anti-acceleration rules",
            "PTET election not properly made or substantiated",
            "Attempted charitable contribution workaround disallowed under Rev Rul 2020-17"
        ],
        resolution_strategy="Track SALT payments and calculate $10K cap accurately; add back full SALT deduction for AMT; evaluate PTET elections for pass-through businesses where available; avoid improper prepayment strategies; document state tax payment timing; monitor TCJA sunset provisions for post-2025 planning; maintain contemporaneous records of all state/local tax payments.",
        entity_scope=["individual"],
        confidence=0.92,
        confidence_stratification=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="IRC §164(b)(6)",
        category=IssueCategory.ADJUSTMENTS,
        related_doctrines=["AMT Calculation Framework IRC §55"]
    ),

    # AMT NOL Limitation
    DoctrineBlock(
        topic="AMT Net Operating Loss Limitation IRC §56(d)",
        keywords=["amt nol", "net operating loss", "§56(d)", "90% limitation", "nol amt"],
        conclusion_template=[
            "IRC §56(d) limits AMT net operating loss deduction to 90% of AMTI (before NOL deduction).",
            "Regular tax NOL can fully offset income, but AMT NOL limited to 90%, ensuring minimum 10% tax base.",
            "AMT NOL carryforwards calculated separately from regular tax NOLs using AMT adjustments and preferences."
        ],
        reasoning_framework="""IRC §56(d)(1) imposes 90% limitation on alternative tax net operating loss (ATNOL) deduction,
preventing complete offset of AMTI. This contrasts with regular tax NOL rules which generally allow full offset (subject to
§172 limitations). The ATNOL is computed under §56(d)(2) by starting with regular tax NOL and adjusting for AMT modifications:
adding back items deductible for regular tax but not AMT, subtracting items deductible for AMT but not regular tax. The
resulting ATNOL may differ substantially from regular tax NOL. Key adjustments include depreciation timing differences, mining
costs, tax-exempt interest on private activity bonds, and other §56/§57 items. The 90% limitation under §56(d)(1)(A) means
even with large ATNOL carryforward, taxpayer pays AMT on at least 10% of AMTI. TCJA §13302 eliminated 2-year carryback and
imposed 80% limitation for regular tax NOLs arising in years after 2017, but AMT NOL retains 90% limitation. Ordering rules:
oldest ATNOL absorbed first, consistent with regular tax. Carryforward period is indefinite post-TCJA for both regular and AMT.""",
        key_factors=[
            "AMT NOL limited to 90% of AMTI before NOL deduction",
            "ATNOL calculated separately from regular tax NOL with AMT adjustments",
            "10% minimum AMTI always subject to tax even with NOL",
            "Regular tax NOL 80% limitation (post-TCJA) vs AMT 90% limitation",
            "Depreciation and other timing differences affect ATNOL calculation",
            "Indefinite carryforward period for both regular and AMT NOLs post-TCJA",
            "Separate tracking required for regular vs AMT NOL carryforwards"
        ],
        primary_authority=[
            "IRC §56(d)(1) — 90% ATNOL limitation",
            "IRC §56(d)(2) — ATNOL computation",
            "IRC §172 — Regular tax NOL rules",
            "TCJA §13302 — Regular tax NOL changes",
            "Treas Reg §1.56(d)-1 — AMT NOL regulations"
        ],
        burden_holder="Taxpayer must substantiate ATNOL calculation with separate AMT NOL schedule and carryforward tracking",
        adversary_position="IRS challenges ATNOL calculations lacking proper AMT adjustments or exceeding 90% limitation",
        counter_arguments=[
            "Taxpayer failed to adjust regular tax NOL for AMT items in ATNOL calculation",
            "ATNOL deduction exceeded 90% of AMTI",
            "Failed to separately track regular vs AMT NOL carryforwards",
            "Depreciation adjustments omitted in ATNOL computation",
            "Improperly carried back ATNOL post-TCJA (no carryback allowed)"
        ],
        resolution_strategy="Maintain separate schedules for regular tax NOL and ATNOL carryforwards; calculate ATNOL with all §56/§57 adjustments; apply 90% limitation correctly (90% of AMTI before NOL); track carryforward periods indefinitely; document NOL year AMT return showing ATNOL calculation; reconcile regular and AMT NOL differences; prepare technical memo explaining ATNOL adjustments.",
        entity_scope=["individual", "c_corporation", "estate", "trust"],
        confidence=0.87,
        confidence_stratification=ConfidenceStratification.AGGRESSIVE_SUPPORTABLE,
        controlling_precedent="IRC §56(d)(1)",
        category=IssueCategory.ADJUSTMENTS,
        related_doctrines=["AMT Calculation Framework IRC §55"]
    ),

    # Corporate AMT (CAMT) — IRA 2022
    DoctrineBlock(
        topic="Corporate Alternative Minimum Tax IRC §55/56A/59 (CAMT)",
        keywords=["corporate amt", "camt", "§59", "adjusted financial statement income", "15% corporate minimum tax"],
        conclusion_template=[
            "Inflation Reduction Act 2022 enacted 15% corporate alternative minimum tax on adjusted financial statement income.",
            "CAMT applies to corporations with average annual adjusted financial statement income exceeding $1 billion.",
            "CAMT calculated on financial statement income, not taxable income, creating new book-tax conformity pressure."
        ],
        reasoning_framework="""IRC §55(b)(2), as added by Inflation Reduction Act §10101, imposes 15% corporate alternative
minimum tax on adjusted financial statement income (AFSI) for applicable corporations. An "applicable corporation" under
§59(k) is one with average annual AFSI exceeding $1 billion for any 3-taxable-year period ending before the current year
(reduced to $100 million if foreign-parented). AFSI is net income or loss on applicable financial statement (GAAP, IFRS, or
SEC filing), adjusted for specific items under §56A. Key adjustments include: depreciation (5-year ADS for most property),
pension contributions, NOL limitation, foreign taxes, and others. CAMT creates parallel to individual AMT structure: tentative
minimum tax equals 15% of AFSI less corporate AMT foreign tax credit, and CAMT liability equals excess of tentative minimum
tax over regular corporate tax (reduced by certain credits). Unlike repealed pre-TCJA corporate AMT based on taxable income,
CAMT is based on financial statement income, creating unique planning challenges around book-tax differences. Effective for
tax years beginning after December 31, 2022. §53(e) provides general business credit refundability for CAMT-paying corporations.""",
        key_factors=[
            "$1B AFSI threshold for applicable corporation status ($100M if foreign-parented)",
            "15% rate applied to adjusted financial statement income",
            "Book income basis fundamentally different from prior corporate AMT",
            "Depreciation recalculated using 5-year ADS for most property",
            "Creates incentive to manage financial statement income for tax purposes",
            "Foreign tax credit allowed but limited for CAMT",
            "General business credits refundable for CAMT payers under §53(e)",
            "Effective for tax years beginning after 12/31/2022"
        ],
        primary_authority=[
            "IRC §55(b)(2) — CAMT imposition",
            "IRC §56A — AFSI adjustments",
            "IRC §59(k) — Applicable corporation definition",
            "IRC §53(e) — Credit refundability for CAMT payers",
            "IRA 2022 §10101 — CAMT enactment",
            "Notice 2023-7 — Initial CAMT guidance"
        ],
        burden_holder="Applicable corporation must calculate AFSI and demonstrate proper adjustments; high burden of substantiation",
        adversary_position="IRS scrutiny of AFSI adjustments, aggregation rules, and applicable corporation status",
        counter_arguments=[
            "Corporation understated AFSI to avoid applicable corporation status",
            "Depreciation adjustments under §56A calculated incorrectly",
            "Failed to aggregate related entities properly for $1B threshold",
            "Book-tax differences improperly used to manipulate AFSI",
            "Foreign tax credit limitation miscalculated for CAMT"
        ],
        resolution_strategy="Establish robust AFSI calculation and tracking system; document all §56A adjustments; maintain audited financial statements; coordinate with financial reporting team on book-tax strategy; evaluate M&A impact on aggregation threshold; model CAMT exposure annually; consider financial statement income management opportunities; track general business credit refundability eligibility; prepare for IRS examination focus on CAMT calculations.",
        entity_scope=["c_corporation"],
        confidence=0.85,
        confidence_stratification=ConfidenceStratification.AGGRESSIVE_SUPPORTABLE,
        controlling_precedent="IRC §55(b)(2)",
        category=IssueCategory.CALCULATION,
        related_doctrines=["AMT Calculation Framework IRC §55"]
    ),

    # Additional 40+ doctrine blocks would follow covering:
    # - IRC §59(e) election for IDC amortization
    # - Farm loss AMT rules
    # - Passive activity AMT computation
    # - Trust and estate AMT specifics
    # - AMT and qualified small business stock
    # - Research credit vs AMT
    # - Foreign tax credit for AMT
    # - AMT and like-kind exchanges
    # - Child tax credit AMT interaction
    # - Estate tax deduction for AMT
    # - Generation-skipping transfer tax and AMT
    # - Charitable contribution AMT planning
    # - AMT and qualified opportunity zones
    # - AMT refundable credits (ACTC, etc.)
    # - Partnership AMT allocations
    # - S corporation AMT flow-through
    # - AMT and built-in gains tax
    # - REIT dividends and AMT
    # - QSBS gain exclusion and AMT
    # - AMT and installment sales
    # - Etc. (continuing to 50+ total blocks)

    # Placeholder for remaining doctrines — production system would have 50+ full blocks
    DoctrineBlock(
        topic="AMT Planning Strategies — General Framework",
        keywords=["amt planning", "amt mitigation", "timing strategies", "amt avoidance"],
        conclusion_template=[
            "AMT planning focuses on managing timing of income/deductions and minimizing exclusion preferences.",
            "Defer income into AMT years, accelerate deductions into non-AMT years to maximize benefit.",
            "Consider entity structure, ISO exercise timing, and state tax planning to reduce AMT exposure."
        ],
        reasoning_framework="""Effective AMT planning requires multi-year tax modeling to identify AMT vs non-AMT years and
strategic timing of income and deductions. Because AMT disallows or limits certain deductions (SALT, miscellaneous itemized
pre-TCJA), accelerating deductions into non-AMT years maximizes tax benefit. Conversely, timing income into AMT years
(where marginal rate may be lower due to AMT exemption) can reduce overall liability. ISO planning is critical: avoid large
exercises creating AMT without liquidity; consider same-year disposition; model AMT credit recovery. Entity planning:
pass-throughs subject owners to AMT on flow-through items; C corps historically avoided individual AMT but now face CAMT.
State tax planning post-TCJA limited by SALT cap but PTET workarounds may help. Private activity bond holdings create
permanent AMT exposure best avoided by high-AMT-risk taxpayers. Charitable contribution bunching into non-AMT years, Roth
conversions in AMT years (lower rate), and depreciation method elections all factor into comprehensive AMT planning.""",
        key_factors=[
            "Multi-year tax projection essential for AMT planning",
            "Timing differences create planning opportunities; exclusion preferences should be avoided",
            "ISO exercise timing and same-year disposition strategy",
            "Entity selection impacts AMT exposure (pass-through vs C corp)",
            "SALT cap and PTET considerations post-TCJA",
            "Private activity bond holdings should be evaluated for AMT impact",
            "Roth conversions attractive in AMT years (lower rate)"
        ],
        primary_authority=[
            "IRC §55-59 — AMT framework",
            "General tax planning principles",
            "TCJA provisions affecting AMT incidence"
        ],
        burden_holder="Taxpayer/advisor must model multi-year scenarios and document planning rationale",
        adversary_position="IRS challenges artificial timing arrangements lacking business purpose",
        counter_arguments=[
            "Timing strategies lack economic substance",
            "Step transaction doctrine collapses multi-year plan",
            "Business purpose requirement not met for timing elections",
            "ISO exercise-and-sale documented as single transaction (loses same-year benefit)"
        ],
        resolution_strategy="Document business purpose for all timing decisions; maintain multi-year tax models; avoid purely tax-motivated transactions lacking economic substance; consult competent tax advisor for AMT planning; implement strategies over multiple years to establish pattern; coordinate with financial planning for ISO exercises and entity structure decisions.",
        entity_scope=["individual", "estate", "trust", "c_corporation"],
        confidence=0.80,
        confidence_stratification=ConfidenceStratification.AGGRESSIVE_SUPPORTABLE,
        controlling_precedent="IRC §55",
        category=IssueCategory.PLANNING
    ),

]
