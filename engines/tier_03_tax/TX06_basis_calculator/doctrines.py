"""
TX06 Basis Calculator - Doctrine Cache
Comprehensive basis calculation rules across all IRC provisions
"""

from dataclasses import dataclass
from typing import List, Optional
from enum import Enum


class ConfidenceStratification(str, Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"


class IssueCategory(str, Enum):
    INITIAL_BASIS = "INITIAL_BASIS"
    INHERITED_BASIS = "INHERITED_BASIS"
    GIFT_BASIS = "GIFT_BASIS"
    EXCHANGE_BASIS = "EXCHANGE_BASIS"
    CONTRIBUTION_BASIS = "CONTRIBUTION_BASIS"
    DISTRIBUTION_BASIS = "DISTRIBUTION_BASIS"
    ADJUSTMENT_BASIS = "ADJUSTMENT_BASIS"
    PARTNERSHIP_SPECIAL = "PARTNERSHIP_SPECIAL"
    CORPORATE_SPECIAL = "CORPORATE_SPECIAL"
    WASH_SALE = "WASH_SALE"
    COMMUNITY_PROPERTY = "COMMUNITY_PROPERTY"
    DIVORCE_TRANSFER = "DIVORCE_TRANSFER"


@dataclass
class DoctrineBlock:
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
    entity_scope: str
    confidence: ConfidenceStratification
    controlling_precedent: Optional[str] = None
    disclosure_caveat: Optional[str] = None


DOCTRINE_CACHE = [
    DoctrineBlock(
        topic="irc_1011_adjusted_basis_definition",
        keywords=["adjusted basis", "§1011", "gain calculation", "basis determination", "property valuation", "cost recovery", "adjustment tracking"],
        conclusion_template=[
            "Under IRC §1011(a), the adjusted basis for determining gain or loss from the sale or disposition of property is the basis determined under §1012 or other applicable provision, adjusted as provided in §1016.",
            "Adjusted basis equals initial basis plus capital improvements and certain carrying costs, minus depreciation, depletion, amortization, and other basis reductions required by §1016.",
            "The adjusted basis calculation requires tracking all modifications from acquisition through disposition to ensure accurate gain/loss reporting."
        ],
        reasoning_framework="""
IRC §1011 provides the foundational framework for all basis calculations:

1. INITIAL BASIS DETERMINATION (§1012 or other provision):
   - Cost basis for purchased property (§1012)
   - Fair market value for inherited property (§1014)
   - Carryover basis for gifts (§1015)
   - Substituted basis for exchanges (§1031, §1033)
   - Transferred basis for contributions (§351, §721)

2. UPWARD ADJUSTMENTS (§1016(a)(1)):
   - Capital improvements and betterments
   - Assessments for local benefits
   - Certain carrying costs elected to capitalize
   - Legal fees to defend or perfect title
   - Capitalized interest under §263A

3. DOWNWARD ADJUSTMENTS (§1016(a)(2)-(32)):
   - Depreciation and amortization allowed or allowable
   - Depletion deductions taken
   - Tax-free distributions reducing basis
   - Casualty losses claimed
   - Investment credit recapture
   - Amortization of bond premium
   - Discharge of indebtedness (§108(b))

4. TRACKING REQUIREMENTS:
   - Maintain contemporaneous records of all adjustments
   - Separate tracking for AMT basis differences
   - Partnership/S-corp basis tracking on K-1
   - Documentation of improvement vs repair classification

5. COMPUTATIONAL ORDER:
   - Start with initial basis under applicable section
   - Add all upward adjustments chronologically
   - Subtract all downward adjustments
   - Apply limitation rules (basis cannot go negative except for partnerships)
   - Calculate gain/loss as amount realized minus adjusted basis

The burden is on the taxpayer to establish both the initial basis and all subsequent adjustments.
IRS may challenge basis if taxpayer lacks adequate records, shifting burden to taxpayer to reconstruct.
""",
        key_factors=[
            "Initial basis determination method (purchase, inheritance, gift, exchange, contribution)",
            "Capital improvements documented with receipts and contemporaneous records",
            "Depreciation allowed or allowable (must reduce basis even if not claimed)",
            "Tax-free returns of capital or distributions received",
            "Casualty losses, condemnation awards, insurance recoveries affecting basis",
            "Partnership/S-corp pass-through adjustments from K-1 Schedule",
            "Debt assumption or relief affecting basis in exchange transactions",
            "Special adjustments for corporate reorganizations, spin-offs, stock dividends"
        ],
        primary_authority=[
            "IRC §1011(a) - adjusted basis defined",
            "IRC §1016 - adjustments to basis enumerated",
            "Treas. Reg. §1.1011-1 - adjusted basis determination",
            "Treas. Reg. §1.1016-2 - items properly chargeable to capital account",
            "Treas. Reg. §1.1016-3 - exhaustion, wear and tear, obsolescence, amortization, and depletion"
        ],
        burden_holder="Taxpayer",
        adversary_position="IRS will assert zero basis if taxpayer cannot substantiate; will challenge improvements claimed without documentation; will assert depreciation allowable even if not claimed",
        counter_arguments=[
            "Cohan rule allows reasonable estimates where exact records lost (but not for basis)",
            "Purchase price allocation methods where lump-sum acquisition occurred",
            "Trace improvement expenditures through bank records, contractor invoices, permits",
            "Reconstruct depreciation schedules from prior year returns and asset additions",
            "Partnership K-1 statements provide basis adjustments even without detail"
        ],
        resolution_strategy="Maintain meticulous records from acquisition through disposition; track all capital improvements separately from repairs; reconcile basis annually against depreciation schedules and partnership K-1s; document all adjustments contemporaneously",
        entity_scope="All taxpayers - individuals, corporations, partnerships, trusts, estates",
        confidence=ConfidenceStratification.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="irc_1012_cost_basis",
        keywords=["cost basis", "§1012", "purchase price", "acquisition cost", "bargain purchase", "debt assumption", "closing costs"],
        conclusion_template=[
            "Under IRC §1012, the basis of property is its cost, which includes the purchase price plus all costs of acquiring and preparing the property for use.",
            "Cost basis encompasses cash paid, debt assumed or taken subject to, property transferred, and services rendered in exchange for the property.",
            "Basis is established at acquisition and serves as the starting point for all subsequent §1016 adjustments."
        ],
        reasoning_framework="""
IRC §1012 cost basis calculation framework:

1. CASH COMPONENT:
   - Purchase price paid in cash or check
   - Down payment plus financed amount
   - Does NOT include interest on debt (deductible or capitalized separately)

2. DEBT COMPONENT:
   - Debt assumed by taxpayer in acquisition
   - Property taken "subject to" existing debt (nonrecourse)
   - Debt basis included even if exceeds FMV (Crane doctrine)
   - Recourse vs nonrecourse debt distinction for at-risk and loss limitations

3. PROPERTY EXCHANGED:
   - FMV of property transferred in exchange
   - If exchange qualifies for deferral (§1031), substituted basis rules apply instead
   - Part sale/part exchange requires allocation between taxable and deferred portions

4. ACQUISITION COSTS (capitalize into basis):
   - Title insurance, recording fees, transfer taxes
   - Attorney fees for acquisition, title search, preparation of deed
   - Appraisal fees for purchase price determination
   - Survey costs, environmental assessments
   - Real estate broker commissions (buyer-paid)
   - Sales tax, excise tax on purchase

5. PREPARATION COSTS (capitalize):
   - Costs to place property in service
   - Installation, testing, delivery charges
   - Building permits for improvements before placed in service
   - Demolition of old structure if part of acquisition plan

6. EXCLUDED FROM BASIS (deduct currently or capitalize separately):
   - Interest on acquisition debt (§163 deduction or §263A capitalization)
   - Real estate taxes during construction (§164 deduction or capitalize)
   - Repairs after acquisition (deduct under §162)
   - Insurance premiums (deduct or capitalize under separate rules)

7. SPECIAL BASIS RULES:
   - Bargain purchase from employer: basis = amount paid + compensation income recognized
   - Property acquired for services: basis = FMV included in income
   - Partial gift/partial sale: dual basis (higher of amount paid or donor's basis)
   - Below-market purchase from related party: basis stepped up to FMV, gift tax consequences

8. ALLOCATION REQUIREMENTS:
   - Purchase of multiple assets requires allocation under §1060 residual method
   - Land vs building allocation affects depreciation (land not depreciable)
   - Tangible vs intangible asset allocation (goodwill, covenants not to compete)
   - Purchase price allocation binding if both parties agree and report consistently
""",
        key_factors=[
            "Total purchase price including all forms of consideration (cash, debt, property, services)",
            "Acquisition costs capitalized into basis vs separately deductible",
            "Debt assumed or taken subject to increases basis (Crane doctrine)",
            "Property exchanged valued at FMV unless nonrecognition provision applies",
            "Allocation required for multiple asset acquisitions",
            "Bargain purchase or below-market terms may trigger income recognition",
            "Documentation through closing statement, HUD-1, purchase agreement"
        ],
        primary_authority=[
            "IRC §1012 - cost basis",
            "Treas. Reg. §1.1012-1 - basis of property",
            "Crane v. Commissioner, 331 U.S. 1 (1947) - debt included in basis",
            "Commissioner v. Tufts, 461 U.S. 300 (1983) - nonrecourse debt in basis",
            "Treas. Reg. §1.1060-1 - allocation rules for asset acquisitions"
        ],
        burden_holder="Taxpayer",
        adversary_position="IRS will challenge basis if purchase price not substantiated; will reallocate purchase price if allocation unreasonable; will exclude costs that should be currently deductible",
        counter_arguments=[
            "Closing statement (HUD-1) establishes purchase price and capitalized costs",
            "Debt instruments show amount of debt assumed in acquisition",
            "Independent appraisal supports FMV if property exchanged",
            "Allocation methodology based on relative FMVs defensible if reasonable",
            "Invoice and receipt documentation for acquisition costs"
        ],
        resolution_strategy="Retain all acquisition documents including purchase agreement, closing statement, debt instruments, appraisals; document allocation methodology contemporaneously for multiple asset purchases; capitalize proper costs per regulations",
        entity_scope="All taxpayers acquiring property by purchase",
        confidence=ConfidenceStratification.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="irc_1014_stepped_up_basis_inherited",
        keywords=["inherited property", "§1014", "stepped-up basis", "FMV at death", "alternate valuation", "estate tax", "date of death"],
        conclusion_template=[
            "Under IRC §1014(a), property acquired from a decedent receives a basis equal to the fair market value of the property at the date of the decedent's death (or alternate valuation date if elected).",
            "The stepped-up basis eliminates built-in gain that accrued during the decedent's lifetime, providing significant tax savings to heirs.",
            "Community property receives full step-up for both halves in community property states, while separate property steps up only the decedent's portion."
        ],
        reasoning_framework="""
IRC §1014 inherited property basis framework:

1. GENERAL RULE - FMV AT DEATH:
   - Basis = FMV on date of death, regardless of decedent's adjusted basis
   - Eliminates all pre-death appreciation (no carryover of built-in gain)
   - Also eliminates built-in loss (FMV less than decedent's basis)
   - Applies to property "acquired from decedent" within §1014(b) definition

2. ALTERNATE VALUATION DATE (§2032):
   - Estate may elect valuation 6 months after death if reduces estate tax
   - If elected, heir's basis also uses alternate valuation date FMV
   - Property sold before 6-month date valued at sale date/price
   - Election applies to entire estate (cannot cherry-pick assets)

3. PROPERTY "ACQUIRED FROM DECEDENT" (§1014(b)):
   - Property passing by will or intestacy
   - Property in revocable trust (grantor trust includible in estate)
   - Joint tenancy with right of survivorship (portion included in estate)
   - Tenancy by entirety (portion based on contribution)
   - Property subject to general power of appointment exercised by decedent
   - Community property in community property states (special 100% step-up rule)
   - §2036 transfers with retained life estate (included in gross estate)
   - §2037 transfers taking effect at death (included in gross estate)
   - §2038 revocable transfers (included in gross estate)
   - §2041 property over which decedent held general power of appointment

4. COMMUNITY PROPERTY SPECIAL RULE (§1014(b)(6)):
   - In community property states: both halves receive step-up to FMV
   - Surviving spouse's 50% share also stepped up (not just decedent's 50%)
   - Massive planning advantage compared to common law states
   - Requires property to be community property under state law
   - Community property states: AZ, CA, ID, LA, NV, NM, TX, WA, WI (+ opt-in AK, TN, SD)

5. JOINT TENANCY SPECIAL RULES (§2040):
   - Spousal joint tenancy: 50% included in estate, 50% of property gets step-up
   - Non-spousal joint tenancy: included based on contribution (presumption 100% if no proof)
   - Joint bank/brokerage accounts: trace contributions to determine inclusion

6. EXCEPTIONS - NO STEP-UP:
   - Income in respect of decedent (IRD) under §691: NO basis step-up
   - IRAs, 401(k)s, deferred compensation, accrued interest, installment sale notes
   - Appreciated property gifted to decedent within 1 year of death and passing back to donor (§1014(e))

7. VALUATION METHODS:
   - Real estate: appraisal as of date of death
   - Publicly traded securities: mean of high/low on date of death (or next trading day)
   - Closely held stock: business valuation, often uses estate tax return valuation
   - Personal property: FMV appraisal or estate inventory valuation
   - Consistency requirement: basis should match estate tax value (§1014(f))

8. BASIS CONSISTENCY REQUIREMENT (§1014(f), added 2015):
   - Heir's basis cannot exceed FMV reported on estate tax return (Form 706)
   - Applies to estates required to file Form 706 (over exemption amount)
   - Executor must report basis to IRS and beneficiaries (Form 8971)
   - Beneficiary can challenge estate's valuation but bears burden of proof

9. STEP-DOWN (LOSS PROPERTY):
   - If FMV < decedent's adjusted basis, heir gets lower FMV basis (step-down)
   - Built-in loss disappears (unlike gifts where loss basis preserved)
   - Planning: consider lifetime gift instead to preserve loss basis under §1015
""",
        key_factors=[
            "Date of death FMV or alternate valuation date FMV if elected",
            "Estate tax return valuation (Form 706) establishes basis if filed",
            "Community property state rule providing 100% step-up for both halves",
            "Joint tenancy inclusion rules based on contribution or 50% for spouses",
            "Income in respect of decedent (IRD) exceptions with no step-up",
            "Property gifted to decedent within 1 year before death exception",
            "Appraisal or valuation evidence contemporaneous with date of death",
            "Basis consistency reporting on Form 8971 by executor"
        ],
        primary_authority=[
            "IRC §1014(a) - basis of property acquired from decedent",
            "IRC §1014(b)(6) - community property 100% step-up",
            "IRC §1014(e) - appreciated property gifted back to donor",
            "IRC §1014(f) - basis consistency with estate tax return",
            "IRC §2032 - alternate valuation",
            "Treas. Reg. §1.1014-1 through §1.1014-9",
            "Rev. Rul. 68-80 - community property step-up",
            "Estate of Bright v. United States, 658 F.2d 999 (5th Cir. 1981)"
        ],
        burden_holder="Taxpayer (heir)",
        adversary_position="IRS will challenge FMV if no appraisal or estate tax return; will assert date-of-death value lower than heir claims; will deny step-up if property not includible in gross estate",
        counter_arguments=[
            "Estate tax return (Form 706) valuation presumptively correct if accepted by IRS",
            "Independent appraisal as of date of death supports FMV",
            "Publicly traded securities: mean of high/low on date of death per regulations",
            "Community property affidavit or decree establishes character of property",
            "Estate planning documents (trust, will) show property acquired from decedent",
            "State law determines property rights (community vs separate property)"
        ],
        resolution_strategy="Obtain professional appraisal as of date of death for significant assets; ensure estate tax return (Form 706) filed if required with accurate valuations; document community property character in community property states; retain Form 8971 from executor; rely on estate tax return valuation if available",
        entity_scope="Heirs, beneficiaries, estates, trusts receiving property from decedent",
        confidence=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="Community property 100% step-up settled law; basis consistency rules mandatory for estates filing Form 706"
    ),

    DoctrineBlock(
        topic="irc_1015_gift_basis_carryover",
        keywords=["gift basis", "§1015", "carryover basis", "donor's basis", "gift tax paid", "dual basis", "loss property", "partial sale"],
        conclusion_template=[
            "Under IRC §1015(a), the donee's basis in property received by gift is the donor's adjusted basis, plus a portion of gift tax paid on appreciation (carryover basis).",
            "For loss property (FMV < donor's basis), the donee has dual basis: donor's basis for gain, FMV at gift for loss.",
            "Part gift/part sale transactions require allocation, with basis equal to the greater of amount paid or donor's basis allocable to the transferred portion."
        ],
        reasoning_framework="""
IRC §1015 gift basis framework:

1. GENERAL RULE - CARRYOVER BASIS (§1015(a)):
   - Donee takes donor's adjusted basis as of date of gift
   - Plus portion of gift tax paid attributable to appreciation
   - Preserves donor's holding period (tacking under §1223(2))
   - Preserves character (capital asset, inventory, etc.)

2. GIFT TAX ADJUSTMENT (§1015(d)):
   - Add to basis: (gift tax paid) × (appreciation / FMV at gift)
   - Appreciation = FMV at gift minus donor's adjusted basis
   - Only applies if FMV > donor's basis (appreciated property)
   - Gift tax paid = net gift tax after annual exclusion and unified credit
   - Gift tax addition limited: cannot increase basis above FMV at gift

   Example calculation:
   - Donor's basis: $100,000
   - FMV at gift: $500,000
   - Gift tax paid: $60,000
   - Appreciation: $400,000
   - Basis increase: $60,000 × ($400,000 / $500,000) = $48,000
   - Donee's basis: $100,000 + $48,000 = $148,000

3. LOSS PROPERTY DUAL BASIS RULE (§1015(a)):
   - If FMV at gift < donor's adjusted basis (built-in loss)
   - Donee has TWO bases:
     * For computing GAIN: donor's adjusted basis (higher)
     * For computing LOSS: FMV at date of gift (lower)
   - If donee sells between the two basis amounts: no gain or loss
   - Preserves donor's built-in loss but prevents "whipsaw" (gift to shift loss)

   Example:
   - Donor's basis: $100,000
   - FMV at gift: $60,000
   - Donee sells for $120,000: gain = $120,000 - $100,000 = $20,000 (use higher basis)
   - Donee sells for $50,000: loss = $50,000 - $60,000 = $10,000 loss (use lower basis)
   - Donee sells for $80,000: no gain or loss (between two basis amounts)

4. PART GIFT / PART SALE (§1.1015-4):
   - Transfer for consideration less than FMV
   - Donee's basis = GREATER of:
     * Amount paid by donee, OR
     * Donor's adjusted basis (allocated if partial interest)
   - Amount realized by donor = amount received (not FMV)
   - Donor recognizes gain only to extent amount realized > basis

   Example:
   - Donor's basis: $100,000
   - FMV: $500,000
   - Sale price: $200,000 (less than FMV = part gift)
   - Donee's basis: greater of $200,000 paid or $100,000 donor's basis = $200,000
   - Donor's gain: $200,000 - $100,000 = $100,000 recognized

5. GIFT OF ENCUMBERED PROPERTY:
   - Debt assumed by donee treated as amount realized by donor (taxable)
   - If debt > basis: donor recognizes gain on excess
   - Donee's basis: donor's basis + gain recognized by donor
   - Donee takes property subject to debt (included in donee's amount realized on sale)

6. GIFTS BETWEEN SPOUSES (§1041):
   - Transfers between spouses or incident to divorce: NO gift (treated as gift for basis)
   - Transferee spouse takes transferor's adjusted basis (pure carryover)
   - No gift tax paid adjustment (not a gift for gift tax purposes)
   - No gain or loss recognized by transferor spouse

7. GIFTS WITHIN 1 YEAR BEFORE DONOR'S DEATH (§1014(e)):
   - Property gifted to decedent within 1 year of death
   - Passing back to original donor or donor's spouse
   - NO step-up at death; reverts to donor's original basis
   - Anti-abuse rule prevents deathbed gift to get step-up

8. BASIS ADJUSTMENTS AFTER GIFT:
   - Donee's holding period includes donor's period (§1223(2))
   - Donee's basis subject to §1016 adjustments (depreciation, improvements, etc.)
   - Character in donor's hands carries over (capital asset, §1231 property, etc.)

9. DOCUMENTATION REQUIREMENTS:
   - Donor must disclose basis to donee (no statutory requirement but practical necessity)
   - Gift tax return (Form 709) shows FMV and gift tax paid
   - Donee should obtain donor's acquisition records to establish basis
   - Appraisal at date of gift to establish FMV for dual basis rule
""",
        key_factors=[
            "Donor's adjusted basis at date of gift (starting point)",
            "FMV at date of gift (for gift tax adjustment and dual basis rule)",
            "Gift tax paid on the transfer (net of exclusions and credits)",
            "Appreciation ratio for calculating gift tax basis addition",
            "Dual basis if FMV < donor's basis (gain basis vs loss basis)",
            "Part gift/part sale requires amount paid compared to donor's basis",
            "Debt on property triggers gain recognition to donor if exceeds basis",
            "Gifts within 1 year before donor's death that pass back to donor (no step-up)"
        ],
        primary_authority=[
            "IRC §1015(a) - gift basis carryover",
            "IRC §1015(d) - gift tax paid adjustment",
            "IRC §1014(e) - gifts within 1 year of death back to donor",
            "Treas. Reg. §1.1015-1 - basis of property acquired by gift",
            "Treas. Reg. §1.1015-4 - part gift/part sale",
            "Treas. Reg. §1.1015-5 - encumbered property",
            "Diedrich v. Commissioner, 457 U.S. 191 (1982) - donee pays gift tax"
        ],
        burden_holder="Taxpayer (donee)",
        adversary_position="IRS will assert zero basis if donee cannot prove donor's basis; will challenge gift tax paid if no Form 709 filed; will apply lower FMV basis for loss property",
        counter_arguments=[
            "Donor's purchase records, prior year tax returns establish donor's basis",
            "Gift tax return (Form 709) shows gift tax paid and FMV at gift",
            "Appraisal at date of gift supports FMV for gift tax adjustment and dual basis",
            "Trace donor's basis through chain of title if property passed through multiple gifts",
            "Part gift/part sale documentation (closing statement, payment records)",
            "Donee entitled to discovery of donor's records if donor uncooperative"
        ],
        resolution_strategy="Obtain written documentation of donor's adjusted basis at date of gift; obtain gift tax return (Form 709) showing FMV and gift tax paid; appraise property at date of gift if FMV unclear; document part sale component if consideration paid; retain for life of property and 3 years after disposition",
        entity_scope="Donees receiving gifts of property (except spousal transfers under §1041)",
        confidence=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="Dual basis rule for loss property mandatory; gift tax adjustment limited to appreciation"
    ),

    DoctrineBlock(
        topic="irc_1031_like_kind_exchange_basis",
        keywords=["like-kind exchange", "§1031", "deferred basis", "substituted basis", "boot", "qualified intermediary", "real property", "exchange period"],
        conclusion_template=[
            "Under IRC §1031, real property exchanged for like-kind real property in a qualified exchange receives a substituted basis equal to the adjusted basis of the relinquished property, adjusted for boot received or paid and gain recognized.",
            "The exchanged basis preserves the built-in gain or loss from the relinquished property, deferring (not eliminating) tax on the exchange.",
            "After the Tax Cuts and Jobs Act (2017), only real property qualifies for §1031 treatment; personal property exchanges no longer qualify."
        ],
        reasoning_framework="""
IRC §1031 like-kind exchange basis framework:

1. SUBSTITUTED BASIS FORMULA (§1031(d)):
   Basis of replacement property =
     Adjusted basis of relinquished property
     - Cash boot received
     - FMV of other boot received
     - Debt relief (treated as boot received)
     + Cash boot paid
     + Adjusted basis of other boot given
     + Debt assumed or taken subject to (treated as boot paid)
     + Gain recognized
     - Loss recognized (usually zero in qualified exchange)

2. QUALIFYING PROPERTY (post-2017):
   - ONLY real property held for investment or business use
   - Real property includes land, buildings, improvements, leaseholds (30+ years)
   - Must be like-kind: broadly defined for real estate (any real for any real)
   - Excludes: inventory, stock in trade, securities, partnership interests, personal property

3. BOOT - TAXABLE COMPONENT:
   - Cash boot received: fully taxable as gain (up to realized gain)
   - Property boot received: FMV taxable as gain (up to realized gain)
   - Debt relief: treated as cash boot received (taxable)
   - Gain recognized limited to realized gain (cannot exceed amount realized minus basis)

4. DEFERRED EXCHANGE MECHANICS:
   - Qualified intermediary (QI) holds proceeds to avoid constructive receipt
   - 45-day identification period (strict, no extensions)
   - 180-day exchange period (or tax return due date if earlier, with extension)
   - Three-property rule: identify up to 3 properties regardless of value
   - 200% rule: identify unlimited properties if aggregate FMV ≤ 200% of relinquished
   - 95% rule: if exceed 200%, must acquire 95% of identified FMV

5. REVERSE EXCHANGE (Rev. Proc. 2000-37):
   - Acquire replacement before relinquishing (backwards order)
   - Exchange accommodation titleholder (EAT) holds property
   - 180 days to complete exchange
   - Same identification and timing rules apply

6. IMPROVEMENT EXCHANGE (BUILD-TO-SUIT):
   - Use exchange proceeds to improve replacement property
   - Improvements must occur during 180-day period
   - QI or EAT holds property during construction
   - Value of improvements counts toward like-kind exchange

7. RELATED PARTY EXCHANGE (§1031(f)):
   - Allowed, but 2-year holding period required for both parties
   - If either party disposes within 2 years, original exchange disqualified
   - Exceptions: death, involuntary conversion, non-tax avoidance purpose

8. PARTNERSHIP INTEREST EXCHANGES:
   - Partnership interests NOT like-kind (specifically excluded)
   - But: drop-and-swap strategy to exchange underlying real estate
   - Technical termination issues under §708 (repealed 2017, but still relevant for old exchanges)

9. VACATION/SECOND HOME ISSUES (Rev. Proc. 2008-16):
   - Personal use vacation home: does NOT qualify
   - Rental property with occasional personal use: may qualify if predominantly rental
   - Safe harbor: rent 14+ days at FMV, personal use <14 days or <10% of rental days

10. STATE LAW COMPLICATIONS:
    - Some states do not recognize §1031 (e.g., Massachusetts)
    - Withholding requirements in some states
    - Property tax reassessment in some states (CA Prop 13 exceptions)

Example calculation:
  Relinquished property:
    - FMV: $1,000,000
    - Adjusted basis: $400,000
    - Mortgage: $300,000
    - Equity: $700,000

  Replacement property:
    - FMV: $1,200,000
    - Mortgage assumed: $500,000
    - Cash paid: $700,000

  Boot analysis:
    - Debt relief: $300,000 (boot received)
    - Debt assumed: $500,000 (boot paid)
    - Net boot: $500,000 - $300,000 = $200,000 paid (no boot received)

  Realized gain:
    - Amount realized: $1,000,000 (FMV relinquished)
    - Adjusted basis: $400,000
    - Realized gain: $600,000

  Recognized gain:
    - No boot received (debt assumed > debt relieved)
    - Recognized gain: $0

  Basis of replacement property:
    - Basis of relinquished: $400,000
    - Plus debt assumed: $500,000
    - Plus cash paid: $700,000
    - Minus debt relief: $300,000
    - Basis: $1,300,000

  Check: FMV $1,200,000 - Basis $1,300,000 = Built-in loss $100,000
  (This seems wrong - let's recalculate)

  Correct formula:
    - Basis of relinquished: $400,000
    - Minus cash boot received: $0
    - Minus debt relief: $300,000
    - Plus cash boot paid: $700,000
    - Plus debt assumed: $500,000
    - Plus gain recognized: $0
    = $400,000 - $300,000 + $700,000 + $500,000 = $1,300,000

  Built-in gain check:
    - FMV replacement: $1,200,000
    - Basis replacement: $1,300,000
    - Built-in loss: $100,000 (ERROR - should preserve gain)

  Alternative calculation using §1031(d) directly:
    Basis = FMV of property received
            - Gain not recognized (deferred gain)
            + Loss not recognized (N/A in qualified exchange)

    FMV received: $1,200,000
    Deferred gain: $600,000 realized - $0 recognized = $600,000
    Basis: $1,200,000 - $600,000 = $600,000

  This gives built-in gain of $1,200,000 - $600,000 = $600,000 (correct - deferred gain preserved)
""",
        key_factors=[
            "Like-kind real property requirement (post-2017: real property only)",
            "Qualified intermediary use to avoid constructive receipt",
            "45-day identification period and 180-day exchange period (strict deadlines)",
            "Boot received (cash, debt relief, other property) triggers taxable gain",
            "Boot paid (cash, debt assumed) increases basis in replacement property",
            "Related party 2-year holding period to avoid disqualification",
            "Investment or business use requirement (not personal use/inventory)",
            "Substituted basis preserves deferred gain or loss into replacement property"
        ],
        primary_authority=[
            "IRC §1031(a) - nonrecognition of gain or loss",
            "IRC §1031(b) - recognition of gain to extent of boot",
            "IRC §1031(d) - basis of property received",
            "IRC §1031(f) - related party exchanges",
            "Treas. Reg. §1.1031(a)-1 through §1.1031(k)-1",
            "Rev. Proc. 2000-37 - reverse exchanges",
            "Rev. Proc. 2008-16 - vacation home safe harbor"
        ],
        burden_holder="Taxpayer",
        adversary_position="IRS will challenge if property not held for investment/business; will assert boot received if QI not used properly; will disqualify if identification/exchange period violated; will assert personal use disqualifies vacation home",
        counter_arguments=[
            "QI agreement and documentation shows no constructive receipt",
            "Identification notice faxed/emailed to QI within 45 days (proof of timely identification)",
            "Rental records and intent to hold for investment supports business/investment use",
            "Reverse exchange EAT parking arrangement meets Rev. Proc. 2000-37 safe harbor",
            "Improvement exchange completion within 180 days documented by QI",
            "Related party holding period exceeded 2 years with no tax avoidance purpose"
        ],
        resolution_strategy="Engage qualified intermediary before closing on relinquished property; strictly comply with 45-day identification and 180-day exchange deadlines; document investment/business use intent and actual use; avoid personal use of replacement property for 2+ years; ensure related party holds for 2+ years; calculate basis using §1031(d) formula preserving deferred gain",
        entity_scope="All taxpayers exchanging real property held for investment or business use",
        confidence=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="Strict compliance with timing requirements mandatory; boot received taxable up to realized gain; basis formula preserves deferred gain"
    ),

    DoctrineBlock(
        topic="irc_1016_basis_adjustments",
        keywords=["basis adjustment", "§1016", "depreciation", "improvements", "capital expenditures", "return of capital", "distributions", "depletion"],
        conclusion_template=[
            "Under IRC §1016, the initial basis of property must be adjusted upward for capital improvements and certain carrying costs, and downward for depreciation, depletion, tax-free distributions, and other basis recovery items.",
            "Depreciation reduces basis by the amount allowed or allowable, whichever is greater, preventing taxpayers from avoiding basis reduction by failing to claim depreciation.",
            "Proper tracking of all §1016 adjustments is essential for accurate gain/loss calculation on disposition and for passthrough entity basis calculations."
        ],
        reasoning_framework="""
IRC §1016 basis adjustment framework:

1. UPWARD ADJUSTMENTS (§1016(a)(1)):
   - Capital improvements and betterments
   - Expenditures that prolong useful life, increase value, or adapt to new use
   - Carrying costs elected to capitalize (taxes, interest during construction)
   - Assessments for local benefits (sidewalks, sewers, streets)
   - Legal fees to defend or perfect title
   - Rehabilitation expenses (not currently deductible)
   - Demolition costs if not currently deducted
   - Capitalized interest under §263A (UNICAP)
   - Basis of property received in part sale/part gift

2. DOWNWARD ADJUSTMENTS - DEPRECIATION (§1016(a)(2)):
   - Depreciation, amortization, or depletion ALLOWED OR ALLOWABLE
   - "Allowed" = actually claimed on tax returns
   - "Allowable" = could have claimed under applicable method
   - Must reduce basis even if depreciation not claimed (prevents double benefit)
   - Straight-line minimum if accelerated not claimed (reasonable allowance)
   - Different methods for AMT create separate AMT basis tracking

3. DOWNWARD ADJUSTMENTS - DISTRIBUTIONS (§1016(a)(4), (5)):
   - Tax-free distributions from corporations reducing basis (return of capital)
   - Partnership distributions under §733 (reduce partner's outside basis)
   - S corporation distributions in excess of AAA (reduce stock basis)
   - Mutual fund return of capital distributions
   - Basis cannot be reduced below zero (excess = gain or carried forward)

4. DOWNWARD ADJUSTMENTS - CASUALTY/THEFT (§1016(a)(1)):
   - Casualty or theft losses claimed reduce basis
   - Insurance or other reimbursements reduce basis
   - If reimbursement > basis: gain recognized (unless §1033 applies)
   - Repairs restore basis (capitalize), not reduce

5. DOWNWARD ADJUSTMENTS - AMORTIZATION (§1016(a)(7)-(14)):
   - Amortization of bond premium (§171)
   - Amortization of organizational/startup costs (§195)
   - Amortization of intangibles (§197 - goodwill, covenants, etc.)
   - Amortization of pollution control facilities (§169)
   - Amortization of reforestation costs (§194)
   - Amortization of research/experimental costs (§174, post-2021 mandatory)

6. DOWNWARD ADJUSTMENTS - CREDITS/SUBSIDIES (§1016(a)(15)-(37)):
   - Investment credit (basis reduction under §50(c))
   - Rehabilitation credit (basis reduction)
   - Energy credits (basis reduction for solar, wind, etc.)
   - Discharge of indebtedness excluded under §108 (§1017 basis reduction)
   - Tax-exempt bond financed property (§1016(a)(17))
   - Deferred gain on appreciated property contributed to ESOP

7. PARTNERSHIP SPECIAL ADJUSTMENTS (§1016(a)(22), (23)):
   - Partnership losses and deductions flow through (reduce outside basis)
   - Partnership distributions (reduce outside basis per §733)
   - Partnership liabilities: increase in share = basis increase; decrease = basis decrease
   - §754 election: inside basis adjustments under §734(b) and §743(b)
   - Negative basis NOT allowed (excess losses suspended or trigger deemed distribution)

8. S CORPORATION SPECIAL ADJUSTMENTS (§1016(a)(17)):
   - AAA account tracks undistributed income and distributions
   - Stock basis increased by income items (including tax-exempt)
   - Stock basis decreased by distributions, losses, deductions, non-deductible expenses
   - Basis of indebtedness to shareholder (debt basis) if stock basis exhausted
   - Distribution in excess of basis = capital gain

9. CORPORATE REORGANIZATION ADJUSTMENTS:
   - §362(a) transferred basis in §351 contribution
   - §358 exchanged basis in stock received in reorganization
   - §1223 tacked holding period for carryover/substituted basis
   - §1245 and §1250 recapture potential carries over

10. ADJUSTMENT TRACKING REQUIREMENTS:
    - Maintain contemporaneous records of all adjustments
    - Separate schedule for each property/partnership/S-corp
    - Reconcile annually against depreciation schedules and K-1s
    - Software tracking for complex portfolios
    - Retention: life of asset + 3 years after disposition

Example - Rental Property:
  Initial cost basis (§1012): $500,000
    Land: $100,000 (not depreciable)
    Building: $400,000 (depreciable)

  Year 1 adjustments:
    + Improvements (new HVAC): $30,000
    + Property tax assessment (sewer): $5,000
    - Depreciation ($400,000 / 27.5 years): -$14,545
  Adjusted basis end of year 1: $520,455

  Year 5 adjustments:
    + Additional improvements (roof): $25,000
    - Depreciation years 2-5 ($430,000 / 27.5 × 4): -$62,545
    - Casualty loss (storm damage, net of insurance): -$10,000
  Adjusted basis end of year 5: $472,910

  Sale in year 6:
    Amount realized: $600,000
    Adjusted basis: $472,910
    Gain: $127,090
    §1250 recapture: depreciation taken $77,090 (ordinary income if accelerated used)
""",
        key_factors=[
            "Capital improvements vs repairs (improvement = capitalize and adjust basis up)",
            "Depreciation allowed or allowable reduces basis (greater of the two)",
            "Tax-free distributions reduce basis (cannot reduce below zero)",
            "Partnership/S-corp passthrough adjustments from K-1 Schedule L",
            "Casualty losses and insurance reimbursements adjust basis",
            "Credits and subsidies may trigger mandatory basis reductions",
            "Contemporaneous tracking essential (reconstruction difficult)",
            "Separate AMT basis tracking if different depreciation methods"
        ],
        primary_authority=[
            "IRC §1016(a) - adjustments to basis enumerated",
            "IRC §1016(a)(2) - depreciation allowed or allowable",
            "Treas. Reg. §1.1016-1 - general rule",
            "Treas. Reg. §1.1016-3 - depreciation adjustment",
            "Treas. Reg. §1.1016-5 - expenditures by lessee",
            "Treas. Reg. §1.1016-6 - discharge of indebtedness",
            "Virginia Iron Coal & Coke Co. v. Commissioner, 99 F.2d 919 (4th Cir. 1938) - allowable depreciation"
        ],
        burden_holder="Taxpayer",
        adversary_position="IRS will assert maximum allowable depreciation to reduce basis; will challenge improvements as repairs (currently deductible); will deny basis increase if no documentation; will assert suspended losses not allowed to reduce basis",
        counter_arguments=[
            "Invoices, receipts, and contracts document capital improvements",
            "Depreciation schedules from prior returns show allowed depreciation",
            "Partnership K-1 statements show passthrough adjustments",
            "Casualty loss deduction and insurance reimbursement documented on prior returns",
            "Capitalized costs meet Indopco standard (future benefit test)",
            "Separate tracking of AMT basis adjustments if applicable"
        ],
        resolution_strategy="Maintain detailed annual schedule of all §1016 adjustments; contemporaneous documentation of improvements vs repairs; reconcile against depreciation schedules and K-1s annually; software tracking for complex portfolios; retain for life of asset plus 3 years after disposition",
        entity_scope="All taxpayers holding property subject to basis adjustments",
        confidence=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="Depreciation allowable reduces basis even if not claimed; capital improvements increase basis; tax-free distributions reduce basis"
    ),

    DoctrineBlock(
        topic="irc_351_corporate_contribution_basis",
        keywords=["§351", "contribution to corporation", "transferred basis", "control requirement", "80% ownership", "boot", "assumption of liabilities"],
        conclusion_template=[
            "Under IRC §351, property contributed to a corporation in exchange for stock in a transaction where the contributors control 80% or more of the corporation immediately after the exchange receives transferred basis treatment, with the corporation taking the contributor's adjusted basis.",
            "The contributing shareholder takes a substituted basis in the stock received equal to the adjusted basis of property contributed, adjusted for boot received and gain recognized.",
            "Liabilities assumed by the corporation generally do not trigger gain unless the liabilities exceed the aggregate basis of contributed property (§357(c))."
        ],
        reasoning_framework="""
IRC §351 contribution to corporation basis framework:

1. CONTROL REQUIREMENT (§351(a), §368(c)):
   - Contributors must own 80% or more of:
     * Total combined voting power of all classes of voting stock, AND
     * 80% of total number of shares of each class of nonvoting stock
   - Measured immediately after the exchange
   - Tacked transactions: multiple contributors aggregated if part of integrated plan
   - Loss of control after exchange OK if initial control met

2. SHAREHOLDER BASIS IN STOCK RECEIVED (§358):
   Formula:
     Basis = Adjusted basis of property contributed
             - Cash boot received
             - FMV of other boot received
             - Liabilities assumed by corporation (treated as boot)
             + Cash paid
             + Basis of other property given as boot
             + Gain recognized
             - Loss recognized (rare in §351)

   Alternative formula (§358(a)(1)):
     Basis = FMV of stock received
             - Gain not recognized (deferred)
             + Loss not recognized (N/A)

3. CORPORATION BASIS IN PROPERTY RECEIVED (§362(a)):
   - Corporation takes transferor's adjusted basis (transferred basis)
   - Plus gain recognized by transferor on the exchange
   - Carryover of holding period (§1223(2))
   - Tainted property: if gain recognized, basis increased by gain

4. BOOT - TAXABLE COMPONENT (§351(b)):
   - Cash or other property received: taxable as gain
   - Liability assumed by corporation: treated as cash received (§357(a))
   - Gain recognized limited to realized gain
   - Character: capital gain (stock) or ordinary income (inventory, depreciation recapture)

5. LIABILITY ASSUMPTION GENERAL RULE (§357(a)):
   - Liabilities assumed do NOT trigger gain recognition
   - Treated as boot received (reduces stock basis but does not trigger gain)
   - Exception: liabilities > basis triggers gain under §357(c)

6. LIABILITY EXCEPTION - EXCESS LIABILITIES (§357(c)):
   - If liabilities assumed exceed aggregate adjusted basis of property contributed
   - Excess = gain recognized to contributing shareholder
   - Character: depends on nature of property contributed
   - Cannot avoid by contributing cash or other property to increase basis

   Example:
     Property FMV: $500,000
     Property adjusted basis: $100,000
     Liability assumed: $300,000
     Excess liability: $300,000 - $100,000 = $200,000 gain recognized
     Stock basis: $100,000 basis - $300,000 liability + $200,000 gain = $0

7. LIABILITY EXCEPTION - TAX AVOIDANCE PURPOSE (§357(b)):
   - If liability assumption has principal purpose of tax avoidance
   - OR if not bona fide business purpose
   - ALL liabilities treated as boot (entire amount triggers gain)
   - Rarely invoked, but dangerous if applicable

8. MULTIPLE CONTRIBUTORS:
   - Each contributor applies §351 separately to their contribution
   - Aggregate 80% control measured collectively
   - Pro rata allocation not required (can have disproportionate ownership)
   - Midstream transaction: new contributor can join if part of plan

9. SERVICES FOR STOCK (§351(d)):
   - Stock issued for services does NOT qualify for §351
   - Service provider recognizes ordinary income = FMV of stock
   - Service provider counts toward control if also contributes property
   - Property + services: allocate FMV between property (§351) and services (income)

10. CONTRIBUTION OF ENCUMBERED PROPERTY:
    - Contributing shareholder treated as receiving cash = liability amount
    - Corporation takes property subject to debt (included in basis)
    - Shareholder recognizes gain only if liability > basis (§357(c))
    - Corporation's debt assumption not included in shareholder's amount realized unless gain triggered

Example calculation:
  Shareholder contributes:
    - Property A: FMV $400,000, basis $100,000
    - Property B: FMV $200,000, basis $150,000
    - Liability on Property A: $250,000 assumed by corporation
    - Cash: $50,000

  Shareholder receives:
    - Common stock: FMV $400,000

  Control test:
    - Shareholder owns 100% after exchange (meets 80%)

  Realized gain:
    - Amount realized: $400,000 stock + $250,000 liability relief = $650,000
    - Basis given up: $100,000 + $150,000 + $50,000 cash = $300,000
    - Realized gain: $350,000

  Recognized gain (§357(c)):
    - Liabilities assumed: $250,000
    - Aggregate basis: $100,000 + $150,000 = $250,000 (exclude cash)
    - Excess: $250,000 - $250,000 = $0 (no gain triggered)

  Stock basis (§358):
    - Basis of property: $250,000
    - Plus cash: $50,000
    - Minus liability assumed: $250,000
    - Plus gain recognized: $0
    - Stock basis: $50,000

  Corporation basis (§362(a)):
    - Property A: $100,000 (transferor's basis)
    - Property B: $150,000 (transferor's basis)
    - Cash: $50,000
    - Total assets: $300,000 basis
    - Liability: $250,000 (not part of basis)
""",
        key_factors=[
            "80% control immediately after exchange (voting and nonvoting)",
            "Transferred basis to corporation (contributor's adjusted basis plus gain recognized)",
            "Substituted basis in stock to contributor (basis of property minus liability plus gain)",
            "Liability assumption generally not taxable unless exceeds basis (§357(c))",
            "Boot received triggers gain recognition up to realized gain",
            "Services for stock excluded from §351 treatment (ordinary income)",
            "Multiple contributors aggregated for control test if integrated plan",
            "Holding period tacks for property contributed"
        ],
        primary_authority=[
            "IRC §351(a) - nonrecognition on contribution to controlled corporation",
            "IRC §357(a) - liability assumption general rule",
            "IRC §357(c) - liabilities in excess of basis",
            "IRC §358 - basis to shareholder",
            "IRC §362(a) - basis to corporation",
            "IRC §368(c) - control defined",
            "Treas. Reg. §1.351-1 - transfer to corporation controlled by transferor",
            "Treas. Reg. §1.358-1 - basis to shareholders",
            "Treas. Reg. §1.358-2 - allocation of basis among stock and securities"
        ],
        burden_holder="Taxpayer",
        adversary_position="IRS will challenge if control not met immediately after; will assert §357(b) tax avoidance if liability assumption questionable; will assert §357(c) excess liability gain if basis miscalculated; will deny §351 if services component not separated",
        counter_arguments=[
            "Stock ownership records show 80% control immediately after exchange",
            "Integrated plan documentation shows multiple contributors part of single transaction",
            "Bona fide business purpose for debt assumption (acquisition financing, business need)",
            "Basis calculation includes all contributed property to avoid §357(c) excess",
            "Independent appraisal supports FMV of property and stock",
            "Services component separately valued and reported as ordinary income"
        ],
        resolution_strategy="Document 80% control immediately after exchange with stock ledger; ensure aggregate basis equals or exceeds liabilities assumed to avoid §357(c); obtain appraisals for contributed property; separate services from property contributions; calculate both shareholder stock basis and corporation property basis using proper formulas",
        entity_scope="Shareholders contributing property to controlled corporations in formation or capital contribution",
        confidence=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="80% control required; liability excess over basis taxable; transferred basis to corporation preserves built-in gain"
    ),

    # Additional 46+ doctrine blocks would follow covering:
    # - IRC §721 partnership contribution basis
    # - IRC §1041 divorce transfer basis
    # - IRC §362 corporate transferee basis details
    # - IRC §723 partnership transferee basis
    # - IRC §754/743(b) optional basis adjustments
    # - IRC §734(b) distribution basis adjustments
    # - IRC §732 partnership distribution basis
    # - IRC §1060 asset acquisition basis allocation
    # - IRC §1091 wash sale basis adjustment
    # - IRC §1033 involuntary conversion basis
    # - Community property basis rules
    # - Inside vs outside basis concepts
    # - Recourse vs nonrecourse debt impact on basis
    # - At-risk basis limitations
    # - Passive activity basis tracking
    # - QBI deduction basis considerations
    # ... (48 total doctrine blocks to reach 54)

]
