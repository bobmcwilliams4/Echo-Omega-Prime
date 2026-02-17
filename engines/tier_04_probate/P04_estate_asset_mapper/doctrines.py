"""
P04 Estate Asset Mapper - Doctrine Cache
50+ pre-compiled expert reasoning blocks for estate asset classification and valuation.
Each block = 40-80 lines of REAL domain expertise.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum


class IssueCategory(str, Enum):
    """Estate asset mapping issue categories."""
    PROPERTY_CLASSIFICATION = "PROPERTY_CLASSIFICATION"
    INCLUSION_EXCLUSION = "INCLUSION_EXCLUSION"
    VALUATION_METHOD = "VALUATION_METHOD"
    DISCOUNT_APPLICABILITY = "DISCOUNT_APPLICABILITY"
    COMMUNITY_PROPERTY = "COMMUNITY_PROPERTY"
    RETAINED_INTERESTS = "RETAINED_INTERESTS"
    TRANSFER_TIMING = "TRANSFER_TIMING"
    SPECIAL_VALUATION = "SPECIAL_VALUATION"
    JOINT_OWNERSHIP = "JOINT_OWNERSHIP"
    LIFE_INSURANCE = "LIFE_INSURANCE"
    BUSINESS_INTERESTS = "BUSINESS_INTERESTS"
    MINERAL_RIGHTS = "MINERAL_RIGHTS"


class ConfidenceStratification(str, Enum):
    """Confidence levels for estate tax positions."""
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"


@dataclass
class DoctrineBlock:
    """Pre-compiled expert reasoning for estate asset mapping issues."""
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
    issue_category: IssueCategory = IssueCategory.PROPERTY_CLASSIFICATION
    fact_fragility_score: float = 0.5
    disclosure_caveat: Optional[str] = None


# ═══════════════════════════════════════════════════════════════════════════
# DOCTRINE CACHE - 50+ BLOCKS OF REAL DOMAIN EXPERTISE
# ═══════════════════════════════════════════════════════════════════════════

DOCTRINE_CACHE: List[DoctrineBlock] = [
    # ──────────────────────────────────────────────────────────────────────
    # IRC §2031 - GROSS ESTATE DEFINITION
    # ──────────────────────────────────────────────────────────────────────
    DoctrineBlock(
        topic="irc_2031_gross_estate_scope",
        keywords=["gross estate", "irc 2031", "inclusion", "fair market value", "date of death"],
        conclusion_template=[
            "IRC §2031(a) defines gross estate as the value of all property to the extent of the decedent's interest at death.",
            "Fair market value is the price at which property would change hands between willing buyer and seller, neither under compulsion.",
            "Valuation date is generally date of death unless alternate valuation elected under §2032."
        ],
        reasoning_framework="""
IRC §2031 establishes the fundamental scope of the gross estate:

STATUTORY FRAMEWORK:
- §2031(a): Value of gross estate = all property, real or personal, tangible or intangible
- Valuation standard: Fair market value (FMV) at date of death
- Geographic scope: Wherever situated (for U.S. citizens/residents)
- Interest extent: To extent of decedent's interest

FAIR MARKET VALUE STANDARD (Treas. Reg. §20.2031-1(b)):
1. Willing buyer / willing seller test
2. Neither compelled to buy/sell
3. Both having reasonable knowledge of relevant facts
4. Hypothetical transaction in open market
5. Highest and best use assumption

PROPERTY TYPES INCLUDED:
- Real property (land, buildings, mineral interests)
- Tangible personal property (vehicles, jewelry, art, collectibles)
- Intangible property (stocks, bonds, bank accounts, intellectual property)
- Business interests (corporations, partnerships, LLCs, sole proprietorships)
- Beneficial interests (trusts, estates, annuities)
- Claims and rights (contract rights, causes of action, royalties)

INCLUSION PRINCIPLES:
- Property OWNED at death (§2033)
- Property TRANSFERRED with retained interests (§2036-§2038)
- Property subject to general power of appointment (§2041)
- Life insurance on decedent's life (§2042)
- QTIP property from prior spouse's estate (§2044)
- Certain transfers within 3 years of death (§2035)

VALUATION MECHANICS:
- Snapshot at single moment: date of death (or alternate date if elected)
- Post-death events generally irrelevant (except for wasting assets, stock dividends declared pre-death)
- Blockage discounts apply for large blocks of publicly traded securities
- Fractional interest discounts for undivided interests in property
- Lack of marketability/control discounts for closely held business interests

TEXAS-SPECIFIC CONSIDERATIONS:
- Community property: Only 50% included in decedent's estate (other 50% belongs to surviving spouse)
- Separate property: 100% included if owned by decedent
- Inception of title rule: Character at acquisition controls
        """,
        key_factors=[
            "Property ownership at date of death (legal title, beneficial interest)",
            "Fair market value determination (appraisal, comparable sales, income approach)",
            "Community vs. separate property classification (Texas marital property)",
            "Retained interests or powers over transferred property",
            "Valuation date selection (date of death vs. alternate valuation)",
            "Discount applicability (fractional, marketability, control)",
            "Special valuation elections (§2032A for farms/ranches)"
        ],
        primary_authority=[
            "IRC §2031(a) (Gross Estate Definition)",
            "Treas. Reg. §20.2031-1(b) (Fair Market Value Standard)",
            "Estate of Bright v. United States, 658 F.2d 999 (5th Cir. 1981) (FMV Willing Buyer/Seller)",
            "United States v. Cartwright, 411 U.S. 546 (1973) (Community Property 50% Inclusion)",
            "Texas Family Code §3.001 (Separate vs. Community Property)"
        ],
        burden_holder="Executor bears burden to establish values reported on Form 706",
        adversary_position="IRS challenges low valuations, argues for inclusion of transferred property, contests discount applicability",
        counter_arguments=[
            "Post-death events show true FMV was higher (rejected: valuation is snapshot at death)",
            "Appraisal not needed for publicly traded securities (correct: use mean of high/low on date of death)",
            "Community property includes only probate assets (wrong: includes all community property regardless of probate)",
            "Discounts not available because decedent controlled entity (wrong: FMV assumes hypothetical willing buyer)",
            "Special use valuation is automatic for farms (wrong: requires election and strict qualifications)"
        ],
        resolution_strategy="""
STEP 1: Identify all property interests at date of death
- Legal title holdings (real property deeds, stock certificates, account statements)
- Beneficial interests (trust beneficiary, life estate, remainder interests)
- Contractual rights (employment agreements, royalty contracts, options)

STEP 2: Classify property character (Texas)
- Separate property: Acquired before marriage, by gift, inheritance, or personal injury recovery
- Community property: Acquired during marriage, presumed community absent clear evidence
- Commingled: Trace funds to establish character (clear and convincing evidence)

STEP 3: Determine includible percentage
- Separate property: 100% of decedent's interest
- Community property: 50% (decedent's half)
- Joint tenancy with right of survivorship: Apply §2040 rules
- Tenancy in common: Decedent's fractional share

STEP 4: Value each asset at FMV
- Real property: Appraisal using comparable sales, income approach, or cost approach
- Publicly traded securities: Mean of high/low on date of death (or nearest trading day)
- Closely held business: Revenue Ruling 59-60 factors, apply appropriate discounts
- Mineral interests: Discounted cash flow of proven reserves, comparable sales

STEP 5: Apply discounts where supported
- Fractional interests in real property: 20-40% typical range
- Lack of marketability (closely held): 25-45% supported by restricted stock studies
- Lack of control (minority interest): 15-35% for non-controlling interests
- Blockage (large blocks of stock): Case-by-case based on market absorption

STEP 6: Consider special elections
- Alternate valuation (§2032): If estate value and tax both decrease
- Special use valuation (§2032A): Farms/ranches, up to $1.39M reduction (2025), strict requirements
        """,
        entity_scope="Decedent's gross estate for federal estate tax purposes",
        confidence=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="IRC §2031(a) + Treas. Reg. §20.2031-1(b)",
        issue_category=IssueCategory.PROPERTY_CLASSIFICATION,
        fact_fragility_score=0.3
    ),

    # ──────────────────────────────────────────────────────────────────────
    # IRC §2033 - PROPERTY OWNED AT DEATH
    # ──────────────────────────────────────────────────────────────────────
    DoctrineBlock(
        topic="irc_2033_property_owned_at_death",
        keywords=["property owned", "irc 2033", "beneficial interest", "legal title", "date of death"],
        conclusion_template=[
            "IRC §2033 includes in the gross estate all property owned by the decedent at death to the extent of the decedent's interest.",
            "Ownership includes both legal title and beneficial interests in property.",
            "The key inquiry is what property rights the decedent held at the moment of death."
        ],
        reasoning_framework="""
IRC §2033 is the baseline inclusion provision for estate tax:

SCOPE OF §2033:
- Includes property decedent actually owned at death
- Both legal and equitable ownership counted
- No lookback period (unlike §2035-§2038)
- Applies to all property types (real, personal, tangible, intangible)

OWNERSHIP CONCEPTS:
1. Legal Title: Record ownership (deed, title certificate, account registration)
2. Beneficial Ownership: Right to enjoy property benefits (trust beneficiary, life tenant with power to invade)
3. Undivided Interests: Tenancy in common, fractional mineral interests
4. Contingent Interests: Valued at FMV even if contingent (e.g., lawsuit pending at death)

TEXAS COMMUNITY PROPERTY INTERSECTION:
- Community property: Decedent owns 50% undivided interest (other 50% is spouse's)
- Separate property: Decedent owns 100% (or stated fractional share)
- Mixed character: Allocate based on tracing (inception of title, separate funds used, etc.)

EXAMPLE SCENARIOS:
A. Decedent owns home as separate property → 100% FMV included
B. Decedent owns home as community property → 50% FMV included
C. Decedent owns 25% undivided interest in ranch → 25% FMV included (apply fractional interest discount)
D. Decedent is life tenant with power to invade principal → Full trust corpus included (§2036 overlap)
E. Decedent owns stock options vested at death → Include spread value (FMV of stock minus exercise price)

WHAT §2033 DOES NOT COVER:
- Property transferred before death with retained interests (§2036-§2038 apply)
- Life insurance where decedent had no incidents of ownership (§2042 issue)
- Property passing by operation of law (joint tenancy → §2040; annuities → §2039)
- Property over which decedent held power of appointment but did not own (§2041)

VALUATION UNDER §2033:
- Date of death FMV snapshot
- Apply discounts for fractional interests, lack of marketability/control
- Consider highest and best use for real property
- Use comparable sales, income approach, or asset-based approach as appropriate
        """,
        key_factors=[
            "Legal or beneficial ownership at death",
            "Community vs. separate property character",
            "Fractional or undivided interest percentage",
            "Existence of restrictions on transferability",
            "Fair market value with applicable discounts"
        ],
        primary_authority=[
            "IRC §2033",
            "Treas. Reg. §20.2033-1(a)",
            "Estate of Dillingham v. Commissioner, 88 T.C. 1569 (1987) (Beneficial Ownership)",
            "Texas Family Code §3.002 (Community Property Presumption)"
        ],
        burden_holder="Executor to establish ownership and value; IRS challenges low values or excluded property",
        adversary_position="IRS argues property was owned even if not in decedent's name (beneficial ownership, community property)",
        counter_arguments=[
            "Property titled in spouse's name is excluded (wrong if community property)",
            "Contingent interests not valued until resolved (wrong: include at FMV of contingent right)",
            "Discounts not applicable to §2033 property (wrong: apply if fractional or restricted)"
        ],
        resolution_strategy="""
ANALYSIS FRAMEWORK:
1. Identify property in decedent's name (deeds, accounts, certificates)
2. Identify beneficial interests (trusts, life estates, partnership interests)
3. Classify Texas marital property character (separate vs. community)
4. Determine includible percentage (100% separate, 50% community, fractional share if co-owned)
5. Value at FMV with applicable discounts
6. Cross-check against §2036-§2044 for overlap (e.g., life estate with power to invade)
        """,
        entity_scope="All property owned at death",
        confidence=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="IRC §2033 + Treas. Reg. §20.2033-1",
        issue_category=IssueCategory.PROPERTY_CLASSIFICATION,
        fact_fragility_score=0.2
    ),

    # ──────────────────────────────────────────────────────────────────────
    # IRC §2036 - RETAINED LIFE ESTATE
    # ──────────────────────────────────────────────────────────────────────
    DoctrineBlock(
        topic="irc_2036_retained_life_estate",
        keywords=["retained life estate", "irc 2036", "power to designate", "enjoyment", "possession", "income"],
        conclusion_template=[
            "IRC §2036(a) includes in the gross estate property transferred during life if the decedent retained the right to income, possession, enjoyment, or the power to designate who shall enjoy the property.",
            "The retention must be for life, for a period not ascertainable without reference to death, or for a period that does not in fact end before death.",
            "§2036 recapture applies even if transfer was complete gift for gift tax purposes."
        ],
        reasoning_framework="""
IRC §2036 is the primary anti-avoidance provision for lifetime transfers with retained interests:

STATUTORY ELEMENTS (§2036(a)):
1. Decedent made a transfer during life (not at death)
2. Transfer was of property (real, personal, tangible, intangible)
3. Decedent retained one of the following:
   a. Right to income from property (§2036(a)(1)), OR
   b. Possession or enjoyment of property (§2036(a)(1)), OR
   c. Right to designate who shall possess or enjoy property or income (§2036(a)(2))
4. Retention was for:
   a. Decedent's life, OR
   b. Period not ascertainable without reference to decedent's death, OR
   c. Period that does not in fact end before death

SCOPE OF INCLUSION:
- Full FMV of transferred property included in gross estate at date of death
- Not just the value of retained interest
- Applies even if transfer was completed gift (gift tax paid)
- Common in family limited partnerships (FLP) with retained management rights

COMMON §2036 TRIGGERS:
A. EXPLICIT RETAINED RIGHTS:
   - Life estate in trust with remainder to children
   - Transfer to FLP, decedent continues as general partner with management powers
   - Transfer of home to children, decedent continues living there rent-free
   - Transfer of stock to irrevocable trust, decedent retains voting rights

B. IMPLIED RETAINED RIGHTS (based on facts):
   - Decedent transfers property but continues using it without paying rent
   - Decedent transfers to family entity but controls distributions
   - Decedent transfers property but retains ability to direct investments

§2036(a)(1) - RETAINED INCOME/POSSESSION/ENJOYMENT:
- Income: Dividends, interest, rents, royalties from transferred property
- Possession: Physical occupancy, custody, control of tangible property
- Enjoyment: Economic benefit (e.g., rent-free use of home, personal use of assets)
- Case Law: "Enjoyment" is broader than legal ownership (Byrum factors)

§2036(a)(2) - POWER TO DESIGNATE:
- Right to determine who receives income or property
- Includes power to change beneficial interests
- Trustee powers may trigger if decedent is trustee
- "Fiduciary" label does not shield if effectively controls enjoyment

BONA FIDE SALE EXCEPTION (§2036(a) flush language):
- Transfer for adequate and full consideration in money or money's worth
- Must be bona fide sale (not disguised gift)
- Common defense for FLPs if legitimate business purpose and proportionate value received

FLP CASES - §2036 BATTLEGROUND:
- Estate of Strangi v. Commissioner, 293 F.3d 279 (5th Cir. 2002): FLP inclusion, no bona fide sale
- Estate of Bongard v. Commissioner, 124 T.C. 95 (2005): Inclusion where decedent retained enjoyment
- Estate of Stone v. Commissioner, T.C. Memo 2012-48: Inclusion, implied agreement for continued enjoyment
- Kimbell v. United States, 371 F.3d 257 (5th Cir. 2004): Exclusion, legitimate business purpose and proportionate capital

TEXAS APPLICATIONS:
- Ranch transferred to LLC, decedent continues operating → §2036(a)(1) possession/enjoyment
- Mineral interests transferred to trust, decedent retains royalty income → §2036(a)(1) income
- Oil & gas working interests in FLP, decedent is GP → §2036(a)(2) power to designate distributions
        """,
        key_factors=[
            "Whether decedent transferred property during life",
            "Whether decedent retained income, possession, enjoyment, or designating power",
            "Duration of retention (for life, or period ending at death)",
            "Whether transfer was bona fide sale for full consideration",
            "Express vs. implied agreement for retained rights",
            "Legitimate business purpose for entity (FLP defense)",
            "Proportionality of interests received vs. property transferred"
        ],
        primary_authority=[
            "IRC §2036(a)(1) and (a)(2)",
            "Treas. Reg. §20.2036-1",
            "United States v. Byrum, 408 U.S. 125 (1972) (Enjoyment Standard)",
            "Estate of Strangi v. Commissioner, 293 F.3d 279 (5th Cir. 2002) (FLP Inclusion)",
            "Kimbell v. United States, 371 F.3d 257 (5th Cir. 2004) (FLP Exclusion - Bona Fide Sale)"
        ],
        burden_holder="IRS bears burden to prove §2036 applies; executor defends bona fide sale exception",
        adversary_position="IRS argues FLPs are testamentary substitutes with no business purpose, implied retained enjoyment",
        counter_arguments=[
            "Gift tax paid means no estate inclusion (wrong: §2036 applies despite completed gift)",
            "Decedent had no legal right to income (wrong: economic benefit/enjoyment sufficient)",
            "Proportionate partnership interest proves bona fide sale (not alone: need business purpose)",
            "Fiduciary powers not retained rights (wrong: if decedent controls enjoyment, §2036(a)(2) applies)",
            "Post-death distributions show no retained control (irrelevant: focus on rights at transfer)"
        ],
        resolution_strategy="""
DEFENSIVE STRATEGY FOR FLPs:
1. Establish legitimate business purpose (asset protection, centralized management, succession planning)
2. Document proportionate capital contributions (not disproportionate)
3. Ensure entity respected (separate books, bank accounts, no commingling)
4. Decedent receives FMV for property transferred (appraisal)
5. Avoid retained GP powers if decedent's health declining (use independent GP or LP only)
6. Pay rent if decedent uses entity property personally
7. Distributions consistent with partnership agreement (not de facto controlled by decedent)

ANALYSIS CHECKLIST:
□ Was property transferred during life? (Yes → continue; No → §2036 not applicable)
□ Did decedent retain income from property? (Yes → §2036(a)(1) presumption)
□ Did decedent retain possession/enjoyment? (Explicit or implied → §2036(a)(1))
□ Did decedent retain power to designate enjoyment? (Trustee/GP powers → §2036(a)(2))
□ Was retention for life, or period ending at death? (Yes → inclusion; No → exclusion)
□ Was transfer bona fide sale for full consideration? (Yes → exclusion defense; No → inclusion)
□ Does evidence support legitimate business purpose? (Yes → strengthens defense; No → weak)
        """,
        entity_scope="Property transferred during life with retained life estate or control",
        confidence=ConfidenceStratification.AGGRESSIVE,
        controlling_precedent="IRC §2036 + Strangi (5th Cir.) + Kimbell (5th Cir.)",
        issue_category=IssueCategory.RETAINED_INTERESTS,
        fact_fragility_score=0.7,
        disclosure_caveat="FLP structures heavily scrutinized; document business purpose and proportionate contributions"
    ),

    # ──────────────────────────────────────────────────────────────────────
    # IRC §2038 - REVOCABLE TRANSFERS
    # ──────────────────────────────────────────────────────────────────────
    DoctrineBlock(
        topic="irc_2038_revocable_transfers",
        keywords=["revocable transfer", "irc 2038", "power to alter", "amend", "revoke", "terminate"],
        conclusion_template=[
            "IRC §2038(a) includes in the gross estate property transferred during life if the decedent retained the power to alter, amend, revoke, or terminate the transfer.",
            "The power must exist at death or have been relinquished within 3 years of death.",
            "§2038 applies even if the power was never exercised and even if consent of adverse party required."
        ],
        reasoning_framework="""
IRC §2038 targets revocable transfers where decedent maintains control:

STATUTORY ELEMENTS:
1. Decedent made a transfer during life
2. Decedent retained power to:
   - Alter (change beneficial interests)
   - Amend (modify trust terms)
   - Revoke (cancel transfer and reclaim property)
   - Terminate (end trust and distribute property)
3. Power existed at death OR was relinquished within 3 years of death (§2035(a) clawback)

SCOPE:
- Power exercisable alone OR with non-adverse party (e.g., co-trustee)
- Power exercisable in any capacity (individual, trustee, agent)
- Does NOT apply if power requires consent of adverse party (person with substantial beneficial interest)

REVOCABLE TRUSTS - AUTOMATIC INCLUSION:
- Settlor retains power to revoke → entire trust corpus included
- Common estate planning tool (avoids probate, but no estate tax benefit)
- Form 706 reporting: Include full FMV of trust assets at date of death

IRREVOCABLE TRUSTS - §2038 ANALYSIS:
- Generally excluded if truly irrevocable
- BUT: Retained trustee powers may trigger §2038
  * Power to sprinkle income among beneficiaries → §2038(a) (power to alter)
  * Power to invade principal for beneficiaries → §2038(a) (power to alter)
  * Power to add or remove beneficiaries → §2038(a) (power to alter/amend)
- Safe Harbor: Independent trustee with no retained powers → exclusion

POWER TO ALTER vs. ADMINISTRATIVE POWERS:
- Altering beneficial enjoyment → §2038 inclusion
- Administrative/investment powers (Byrum factors) → generally excluded unless control enjoyment

EXAMPLE SCENARIOS:
A. Decedent creates revocable trust, dies with power to revoke intact → 100% inclusion
B. Decedent creates irrevocable trust, retains trustee power to distribute principal among children → §2038 inclusion (power to alter beneficial interests)
C. Decedent creates irrevocable trust, independent trustee has all powers → No §2038 inclusion
D. Decedent creates irrevocable trust, relinquishes trustee powers 2 years before death → §2035 clawback, included
E. Decedent creates irrevocable trust, power to revoke only with consent of all beneficiaries (adverse parties) → No §2038 inclusion

§2038 vs. §2036 OVERLAP:
- §2038: Focuses on power to change beneficial interests
- §2036: Focuses on retained right to income/enjoyment
- Often both apply (e.g., revocable trust → §2038 power to revoke + §2036 retained enjoyment)
- Inclusion under either = full FMV of property

3-YEAR CLAWBACK (IRC §2035(a)):
- If decedent relinquishes §2038 power within 3 years of death → still included
- Purpose: Prevent deathbed gifts of powers to avoid estate tax
- Example: Decedent resigns as trustee 1 year before death → trust corpus still included
        """,
        key_factors=[
            "Existence of power to alter, amend, revoke, or terminate",
            "Whether power exercisable alone or with non-adverse party",
            "Whether power existed at death or relinquished within 3 years",
            "Revocable vs. irrevocable trust characterization",
            "Trustee powers vs. beneficial ownership powers"
        ],
        primary_authority=[
            "IRC §2038(a)(1)",
            "IRC §2035(a) (3-Year Clawback)",
            "Treas. Reg. §20.2038-1",
            "Lober v. United States, 346 U.S. 335 (1953) (Power to Alter)",
            "Estate of Paxton v. Commissioner, 86 T.C. 785 (1986) (Trustee Powers)"
        ],
        burden_holder="Executor to establish powers relinquished >3 years before death; IRS challenges retained powers",
        adversary_position="IRS argues trustee powers = power to alter beneficial interests, consent requirements ineffective",
        counter_arguments=[
            "Irrevocable trust excludes from estate (wrong if retained trustee powers to alter)",
            "Power never exercised so no inclusion (wrong: existence of power sufficient)",
            "Independent co-trustee consent required (not sufficient if co-trustee non-adverse)",
            "Administrative powers not §2038 powers (correct if truly ministerial; wrong if affect enjoyment)"
        ],
        resolution_strategy="""
DEFENSIVE PLANNING:
1. Use independent trustee (no family member, no subordinate employee)
2. Eliminate or severely limit distribution discretion
3. Remove decedent as trustee >3 years before anticipated death (if health declining)
4. Require consent of adverse party for any changes (all beneficiaries with substantial interests)
5. Use defined distribution standards (health, education, support) vs. discretionary

ANALYSIS FRAMEWORK:
STEP 1: Identify transferred property during life
STEP 2: Determine if decedent retained any powers over transfer
STEP 3: Classify power:
   - Alter beneficial interests? → §2038 trigger
   - Administrative/investment only? → Byrum analysis (likely excluded)
   - Revoke entirely? → §2038 automatic inclusion
STEP 4: Check if power existed at death
STEP 5: If relinquished, check if within 3 years of death (§2035 clawback)
STEP 6: Calculate inclusion amount (full FMV of transferred property at date of death)
        """,
        entity_scope="Property transferred with retained power to alter, amend, revoke, or terminate",
        confidence=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="IRC §2038(a) + Treas. Reg. §20.2038-1",
        issue_category=IssueCategory.RETAINED_INTERESTS,
        fact_fragility_score=0.4
    ),

    # ──────────────────────────────────────────────────────────────────────
    # IRC §2040 - JOINT INTERESTS
    # ──────────────────────────────────────────────────────────────────────
    DoctrineBlock(
        topic="irc_2040_joint_tenancy_survivorship",
        keywords=["joint tenancy", "right of survivorship", "irc 2040", "consideration furnished", "spousal exception"],
        conclusion_template=[
            "IRC §2040 governs inclusion of jointly held property with right of survivorship.",
            "General rule: Include proportionate share based on consideration furnished by decedent, unless surviving joint tenant can prove their contribution.",
            "Spousal exception (§2040(b)): Only 50% included if joint tenants are spouses, regardless of contribution."
        ],
        reasoning_framework="""
IRC §2040 addresses property held jointly with right of survivorship:

JOINT TENANCY CHARACTERISTICS:
- Multiple owners hold undivided interests
- Right of survivorship: At death, decedent's interest passes automatically to surviving joint tenant(s)
- Not subject to probate
- Common for real estate, bank accounts, brokerage accounts

IRC §2040(a) - GENERAL RULE (Non-Spousal):
- Include in gross estate the portion attributable to consideration furnished by decedent
- Presumption: 100% inclusion unless survivor proves contribution
- Burden on executor to show survivor's contribution

CALCULATION:
  Includible Amount = (FMV at Death) × (Decedent's Contribution / Total Contributions)

EXAMPLE - Non-Spousal Joint Tenancy:
- Father and son own ranch as joint tenants
- Father contributed $500K, son contributed $300K (total $800K)
- Ranch worth $2M at father's death
- Includible in father's estate: $2M × ($500K / $800K) = $1,250,000

IRC §2040(b) - SPOUSAL EXCEPTION (Qualified Joint Interest):
- If joint tenants are spouses (and only spouses), include only 50%
- Regardless of which spouse furnished consideration
- Simplified rule: Always 50/50 for spousal joint tenancy

QUALIFIED JOINT INTEREST REQUIREMENTS:
1. Only spouses are joint tenants
2. Property held as joint tenants with right of survivorship (or tenants by entirety)
3. Both spouses are U.S. citizens (if non-citizen spouse, different rules apply)

EXAMPLE - Spousal Joint Tenancy:
- Husband and wife own home as joint tenants with right of survivorship
- Husband paid entire $800K purchase price
- Home worth $1.5M at husband's death
- Includible in husband's estate: $1.5M × 50% = $750,000
- (Ignore contribution; automatic 50/50 split under §2040(b))

TENANCY IN COMMON vs. JOINT TENANCY:
- Tenancy in Common: No right of survivorship, decedent's share passes via will/intestacy
  * Include only decedent's fractional share (e.g., 50%, 25%) under §2033
  * Not a §2040 issue (no survivorship)
- Joint Tenancy: Right of survivorship, passes automatically to survivor
  * §2040 rules apply

TEXAS CONSIDERATIONS:
- Texas recognizes joint tenancy if clearly expressed in deed ("with right of survivorship")
- Otherwise, presumption is tenancy in common
- Spousal property presumed community unless clearly separate
- Community property with right of survivorship: Hybrid form, §2040(b) applies (50% inclusion)

PROVING CONTRIBUTION (Non-Spousal Cases):
- Direct payment from decedent's separate funds
- Gift from decedent to joint tenant (treated as decedent's contribution)
- Income from property originally furnished by decedent
- Burden on executor to establish survivor's contribution (bank records, gift tax returns, tracing)

SECTION 2040 INTERPLAY WITH OTHER SECTIONS:
- If joint property also subject to §2036 (retained life estate), §2036 controls (full inclusion)
- If decedent transferred property to joint tenancy within 3 years of death, §2035 may apply
- If property is community property, §2033 applies (not §2040), only 50% included
        """,
        key_factors=[
            "Joint tenancy with right of survivorship vs. tenancy in common",
            "Spousal vs. non-spousal joint tenancy",
            "Consideration furnished by each joint tenant",
            "Evidence of survivor's contribution (tracing, bank records)",
            "Community property characterization (Texas)"
        ],
        primary_authority=[
            "IRC §2040(a) (General Rule)",
            "IRC §2040(b) (Spousal Exception)",
            "Treas. Reg. §20.2040-1",
            "Estate of Goldsborough v. Commissioner, 70 T.C. 1077 (1978) (Contribution Tracing)",
            "Texas Estates Code §111.001 (Right of Survivorship)"
        ],
        burden_holder="Executor bears burden to prove survivor's contribution (non-spousal); automatic 50/50 for spousal",
        adversary_position="IRS presumes 100% inclusion in non-spousal joint tenancy unless executor proves otherwise",
        counter_arguments=[
            "Joint tenancy always 50/50 (wrong: only for spousal under §2040(b))",
            "Survivor's name on title proves contribution (wrong: must show actual payment)",
            "Community property subject to §2040 (wrong: §2033 controls, 50% inclusion regardless of survivorship)"
        ],
        resolution_strategy="""
ANALYSIS CHECKLIST:
STEP 1: Identify type of co-ownership
  - Joint tenancy with right of survivorship? → Continue to STEP 2
  - Tenancy in common? → §2033 applies (decedent's fractional share only)
  - Community property? → §2033 applies (50% of community property)

STEP 2: Spousal or non-spousal joint tenancy?
  - Both joint tenants are spouses? → §2040(b) applies: Include 50% of FMV, regardless of contribution
  - Non-spousal (parent-child, siblings, friends)? → Continue to STEP 3

STEP 3: Determine consideration furnished (non-spousal)
  - Trace contributions: Who paid purchase price? Who made improvements?
  - Obtain bank records, cancelled checks, gift tax returns
  - Calculate: Includible % = Decedent's Contribution / Total Contributions

STEP 4: Value property at date of death
  - FMV at date of death (appraisal for real property, account balance for financial accounts)

STEP 5: Calculate includible amount
  - Spousal: FMV × 50%
  - Non-Spousal: FMV × (Decedent's Contribution %)

DEFENSIVE TACTICS (Estate Planning):
  - Convert non-spousal joint tenancy to tenancy in common to limit inclusion
  - Document contributions contemporaneously (avoid tracing disputes)
  - For spousal property, consider community property with right of survivorship (automatic 50%, plus step-up for survivor's half under §1014(b)(6))
        """,
        entity_scope="Property held jointly with right of survivorship",
        confidence=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="IRC §2040 + Treas. Reg. §20.2040-1",
        issue_category=IssueCategory.JOINT_OWNERSHIP,
        fact_fragility_score=0.4
    ),

    # ──────────────────────────────────────────────────────────────────────
    # IRC §2042 - LIFE INSURANCE
    # ──────────────────────────────────────────────────────────────────────
    DoctrineBlock(
        topic="irc_2042_life_insurance_inclusion",
        keywords=["life insurance", "irc 2042", "incidents of ownership", "payable to estate", "beneficiary designation"],
        conclusion_template=[
            "IRC §2042 includes life insurance proceeds in gross estate if (1) payable to the estate or (2) decedent possessed incidents of ownership at death.",
            "Incidents of ownership include the power to change beneficiaries, borrow against policy, surrender or cancel policy, or assign policy.",
            "Transfer of policy within 3 years of death results in inclusion under §2035."
        ],
        reasoning_framework="""
IRC §2042 is the exclusive provision for life insurance inclusion:

TWO INDEPENDENT INCLUSION TESTS:

§2042(1) - PAYABLE TO ESTATE:
- Proceeds payable to executor or estate (directly or indirectly)
- Includes proceeds used to pay estate debts or expenses
- Beneficiary designation controls (not intention)
- If estate is named beneficiary → 100% of proceeds included

§2042(2) - INCIDENTS OF OWNERSHIP:
- Decedent possessed any incidents of ownership at death
- Ownership in any capacity (individual, fiduciary, trustee)
- Includes economic benefits AND powers over policy

INCIDENTS OF OWNERSHIP DEFINED (Treas. Reg. §20.2042-1(c)(2)):
- Right to change beneficiary
- Right to surrender or cancel policy
- Right to assign policy or revoke assignment
- Right to pledge policy for loan
- Right to borrow against cash value
- Reversionary interest exceeding 5% of policy value immediately before death

COMMON SCENARIOS:

A. DECEDENT OWNS POLICY ON OWN LIFE:
   - Decedent pays premiums, controls policy → Incidents of ownership
   - Beneficiary: Spouse or children (not estate) → Still included under §2042(2)
   - Death benefit: $1M → $1M included in gross estate

B. IRREVOCABLE LIFE INSURANCE TRUST (ILIT):
   - Decedent transfers policy to ILIT >3 years before death → Excluded (no incidents, not payable to estate)
   - Decedent transfers policy to ILIT <3 years before death → Included under §2035 (3-year clawback)
   - Decedent creates ILIT, ILIT buys new policy → Excluded (decedent never owned)

C. GROUP TERM LIFE INSURANCE (Employer-Provided):
   - Decedent has right to convert to individual policy → Incidents of ownership
   - Decedent can change beneficiary → Incidents of ownership
   - Typically included unless assigned to ILIT >3 years before death

D. COMMUNITY PROPERTY STATE (TEXAS):
   - Policy purchased with community funds → 50% owned by each spouse
   - At decedent spouse's death → 50% of proceeds included (decedent's community share)
   - Separate property policy → 100% of proceeds included if decedent owned

REVERSIONARY INTEREST:
- If decedent has >5% chance of policy reverting to estate, included
- Example: Decedent creates ILIT, trust terminates if beneficiary predeceases decedent → Reversionary interest
- Actuarial calculation: If >5% probability → included

3-YEAR CLAWBACK (IRC §2035(a)):
- Decedent transfers life insurance policy within 3 years of death → Proceeds included
- Applies to §2042 policies (life insurance) but not most other property transfers
- Purpose: Prevent deathbed gifts of life insurance to avoid estate tax
- Example: Decedent transfers $2M policy to ILIT 2 years before death → $2M proceeds included

PLANNING STRATEGIES TO EXCLUDE LIFE INSURANCE:

1. IRREVOCABLE LIFE INSURANCE TRUST (ILIT):
   - Create ILIT, trustee buys policy (decedent never owns) → Excluded
   - OR transfer existing policy >3 years before death → Excluded after 3 years
   - Beneficiaries receive proceeds estate-tax-free
   - Crummey powers for annual exclusion gifts to pay premiums

2. CROSS-PURCHASE AGREEMENT:
   - Business partners own policies on each other
   - At death, survivor buys decedent's business interest with proceeds
   - Proceeds not included in decedent's estate (no incidents of ownership)

3. COMMUNITY PROPERTY ALLOCATION:
   - If policy purchased with community funds, only 50% included
   - Separate property policy → 100% included
   - Conversion to separate property via partition agreement (pre-death planning)

FORM 706 REPORTING:
- Schedule D: List all life insurance policies (owned or incidents)
- Include: Policy number, company, face amount, beneficiary, incidents of ownership
- Attach: Form 712 (Life Insurance Statement) from each insurer
        """,
        key_factors=[
            "Beneficiary designation (estate vs. named beneficiary)",
            "Incidents of ownership at death (power to change, borrow, assign)",
            "Date of transfer (if transferred, was it >3 years before death?)",
            "Community vs. separate property (Texas)",
            "Reversionary interest exceeding 5%",
            "ILIT ownership vs. individual ownership"
        ],
        primary_authority=[
            "IRC §2042(1) (Payable to Estate)",
            "IRC §2042(2) (Incidents of Ownership)",
            "IRC §2035(a) (3-Year Clawback)",
            "Treas. Reg. §20.2042-1(c) (Incidents of Ownership Defined)",
            "Estate of Noel v. Commissioner, 380 U.S. 678 (1965) (Community Property 50% Inclusion)"
        ],
        burden_holder="Executor to establish no incidents of ownership; IRS challenges retained powers or transfers <3 years",
        adversary_position="IRS argues decedent retained incidents through informal arrangements, ILIT not respected",
        counter_arguments=[
            "Beneficiary is not estate, so excluded (wrong: §2042(2) includes if incidents of ownership)",
            "Policy in ILIT name, not decedent's (irrelevant if transferred <3 years or decedent has incidents)",
            "Decedent paid premiums but didn't own policy (not sufficient: must show no incidents of ownership)",
            "Community property policy, so 100% excluded (wrong: 50% included for decedent's share)"
        ],
        resolution_strategy="""
INCLUSION ANALYSIS:
STEP 1: Identify all life insurance on decedent's life
STEP 2: Check beneficiary designation
   - Payable to estate or executor? → §2042(1) inclusion (100% of proceeds)
   - Payable to named beneficiary? → Continue to STEP 3
STEP 3: Check incidents of ownership at death
   - Could decedent change beneficiary, borrow, surrender, assign? → §2042(2) inclusion
   - Policy in ILIT, decedent has no powers? → Continue to STEP 4
STEP 4: Check 3-year clawback
   - Was policy transferred within 3 years of death? → §2035 inclusion (100% of proceeds)
   - Transferred >3 years before death? → Excluded
STEP 5: Community property allocation (Texas)
   - Policy purchased with community funds? → Only 50% of proceeds included
   - Separate property policy? → 100% of proceeds included (if §2042 applies)

DEFENSIVE PLANNING:
- Transfer existing policies to ILIT immediately (3-year clock starts)
- Create new ILIT to purchase new policies (no 3-year issue)
- Remove all incidents of ownership (no retained beneficiary change rights)
- Use independent trustee (not decedent, not decedent's controlled entity)
- Document ILIT formalities (separate EIN, bank account, trust agreement, Crummey notices)
        """,
        entity_scope="Life insurance proceeds on decedent's life",
        confidence=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="IRC §2042 + Treas. Reg. §20.2042-1",
        issue_category=IssueCategory.LIFE_INSURANCE,
        fact_fragility_score=0.3
    ),

    # ──────────────────────────────────────────────────────────────────────
    # COMMUNITY PROPERTY - TEXAS
    # ──────────────────────────────────────────────────────────────────────
    DoctrineBlock(
        topic="texas_community_property_classification",
        keywords=["community property", "separate property", "texas", "inception of title", "commingling", "tracing"],
        conclusion_template=[
            "Texas Family Code §3.001-§3.003 establishes community property system: Property acquired during marriage is presumed community unless proven separate.",
            "Separate property includes property owned before marriage, acquired by gift, devise, or descent, and recovery for personal injuries (except lost wages).",
            "For estate tax, only 50% of community property is included in decedent spouse's gross estate; 100% of separate property is included."
        ],
        reasoning_framework="""
TEXAS COMMUNITY PROPERTY SYSTEM:

FUNDAMENTAL RULE (Texas Family Code §3.002):
- Community property = property acquired by either spouse during marriage OTHER THAN separate property
- Presumption: Property possessed during or on dissolution of marriage is community property

SEPARATE PROPERTY (Texas Family Code §3.001):
1. Property owned or claimed before marriage
2. Property acquired during marriage by gift, devise, or descent (inheritance)
3. Recovery for personal injuries sustained during marriage (EXCEPT recovery for loss of earning capacity)

INCEPTION OF TITLE DOCTRINE:
- Character determined at acquisition, not when paid off
- Example: Spouse buys property during marriage with earnest money (separate) but mortgage (community) → Community property
- Example: Spouse owns property before marriage, marries, pays off mortgage with community funds → Separate property (with possible reimbursement claim)

TRACING REQUIREMENTS:
- Spouse claiming separate property bears burden: Clear and convincing evidence
- Tracing methods: Records, testimony, circumstantial evidence
- Commingled accounts: Must trace separate funds through each transaction

COMMON SCENARIOS:

A. HOME PURCHASED DURING MARRIAGE:
   - Presumed community property
   - Even if titled in one spouse's name → Community property (Texas is not title state)
   - At death: 50% of FMV included in decedent's estate (other 50% belongs to surviving spouse)

B. HOME OWNED BEFORE MARRIAGE:
   - Separate property of owning spouse
   - Mortgage payments during marriage with community funds → Reimbursement claim (but character remains separate)
   - At death: 100% of FMV included if decedent spouse owned as separate property

C. INHERITANCE DURING MARRIAGE:
   - Separate property of inheriting spouse
   - Income/rents from inheritance → Community property (unless will/trust specifies otherwise)
   - At death: 100% of inherited property included in decedent's estate (separate property)

D. COMMINGLED BANK ACCOUNT:
   - Separate funds deposited into joint account with community funds → Commingled
   - Burden on separate property claimant to trace separate funds (bank records, deposit slips)
   - If tracing impossible → Presumed community property

E. BUSINESS STARTED DURING MARRIAGE:
   - Presumed community property (both spouses own 50%)
   - At death: 50% of business FMV included in decedent's estate
   - Exception: If business purchased with separate funds and properly traced → Separate property

ESTATE TAX IMPLICATIONS:

COMMUNITY PROPERTY:
- Only 50% included in decedent's gross estate
- Surviving spouse already owns other 50% (not passing from decedent)
- Step-up in basis: BOTH halves get step-up under IRC §1014(b)(6) (major tax benefit)

SEPARATE PROPERTY:
- 100% included in decedent's gross estate (if decedent owned)
- Step-up in basis: Only decedent's property gets step-up

PLANNING ADVANTAGE OF COMMUNITY PROPERTY:
- Double step-up in basis at first spouse's death (both halves)
- Example: Spouses buy stock for $100K (community property), worth $1M at death
  * Decedent's estate: Include $500K (50%)
  * Surviving spouse's basis: $1M (both halves stepped up)
  * If sold immediately: Zero capital gain

PARTITION AND EXCHANGE AGREEMENTS:
- Spouses can agree to convert community property to separate property (or vice versa)
- Must be in writing, fair, and voluntary
- Estate planning use: Convert appreciating assets to separate property of younger spouse (if expect to predecease)
- IRS scrutiny: Must have legitimate non-tax purpose

MINERAL INTERESTS (TEXAS-SPECIFIC):
- If mineral rights acquired during marriage → Community property (50% inclusion)
- Royalty income from separate property mineral interest → Community income (if received during marriage)
- Lease bonus, delay rentals → Follow character of underlying mineral interest

FORM 706 REPORTING (TEXAS ESTATES):
- Schedule E: List ALL community property (even though only 50% included)
- Indicate "Community Property" in description
- Value: Report full FMV, then show 50% includible in Part 5 Recapitulation
        """,
        key_factors=[
            "Timing of acquisition (before or during marriage)",
            "Source of acquisition (purchase, gift, inheritance, personal injury)",
            "Commingling and tracing evidence",
            "Partition or exchange agreements",
            "Inception of title vs. payment source",
            "Income from separate property (community vs. separate)"
        ],
        primary_authority=[
            "Texas Family Code §3.001 (Separate Property Defined)",
            "Texas Family Code §3.002 (Community Property Defined)",
            "Texas Family Code §3.003 (Presumption)",
            "IRC §1014(b)(6) (Basis Step-Up for Community Property)",
            "United States v. Cartwright, 411 U.S. 546 (1973) (50% Inclusion Rule)"
        ],
        burden_holder="Spouse claiming separate property bears burden of proof by clear and convincing evidence",
        adversary_position="IRS presumes community property unless executor provides clear tracing to separate source",
        counter_arguments=[
            "Title in one spouse's name makes it separate property (wrong: Texas not title state, presumption is community)",
            "Mortgage paid with community funds converts to community property (wrong: inception of title controls)",
            "Income from separate property is separate (wrong: income is community unless specific exception)",
            "Commingled account is all community (often true if no tracing, but not absolute rule)"
        ],
        resolution_strategy="""
CLASSIFICATION ANALYSIS:
STEP 1: Determine date of acquisition
   - Before marriage? → Separate property (of acquiring spouse)
   - During marriage? → Presumed community (continue to STEP 2)

STEP 2: Identify source of acquisition
   - Purchase with earned income? → Community property
   - Gift or inheritance? → Separate property (of recipient spouse)
   - Personal injury recovery? → Separate property (except lost wages)

STEP 3: Trace commingled funds (if applicable)
   - Separate funds deposited into joint account? → Trace with bank records
   - Cannot trace? → Presumed community property

STEP 4: Check for partition/exchange agreement
   - Written agreement converting character? → Respect if fair and voluntary

STEP 5: Calculate estate tax inclusion
   - Community property: 50% of FMV
   - Separate property: 100% of FMV (if decedent owned)

EVIDENCE FOR SEPARATE PROPERTY CLAIM:
□ Pre-marital title documents (deed dated before marriage)
□ Gift letters from donor (if acquired by gift)
□ Will or trust showing inheritance (if acquired by devise/descent)
□ Personal injury settlement agreement allocating recovery (exclude lost wages portion)
□ Tracing records (bank statements showing separate fund deposits, withdrawals, balances)
□ Partition agreement (if character converted)

DEFENSIVE STRATEGY:
- Document separate property contemporaneously (maintain separate accounts)
- Avoid commingling (do not deposit separate funds into joint community account)
- Execute partition agreements for estate planning (convert character if beneficial)
        """,
        entity_scope="All property acquired during marriage or before marriage (Texas)",
        confidence=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="Texas Family Code §3.001-§3.003 + Cartwright (U.S. Supreme Court)",
        issue_category=IssueCategory.COMMUNITY_PROPERTY,
        fact_fragility_score=0.5
    ),

    # ──────────────────────────────────────────────────────────────────────
    # VALUATION - FAIR MARKET VALUE
    # ──────────────────────────────────────────────────────────────────────
    DoctrineBlock(
        topic="fair_market_value_standard",
        keywords=["fair market value", "fmv", "willing buyer", "willing seller", "valuation", "appraisal"],
        conclusion_template=[
            "Fair market value is the price at which property would change hands between a willing buyer and willing seller, neither being under compulsion to buy or sell, and both having reasonable knowledge of relevant facts.",
            "Valuation is as of a specific date (date of death or alternate valuation date).",
            "Hypothetical transaction assumes arms-length negotiation in the open market."
        ],
        reasoning_framework="""
FAIR MARKET VALUE (FMV) STANDARD - Treas. Reg. §20.2031-1(b):

DEFINITION COMPONENTS:
1. Willing Buyer: Hypothetical purchaser, ready and able to buy
2. Willing Seller: Hypothetical seller, ready and able to sell
3. Neither Compelled: No distress sale, no forced purchase
4. Reasonable Knowledge: Both parties have relevant facts about property
5. Open Market: Transaction occurs in public market (not private negotiation)

KEY PRINCIPLES:

A. SNAPSHOT AT VALUATION DATE:
   - Valuation as of specific moment in time (date of death, or alternate date)
   - Post-death events generally ignored (except for wasting assets, dividends declared pre-death but paid post-death)
   - Cannot use hindsight (e.g., property sold for $X six months later does not establish date-of-death FMV)

B. HIGHEST AND BEST USE:
   - Property valued at its highest and best use (most profitable legal use)
   - Example: Land zoned commercial but used as parking lot → Value as commercial development site, not parking lot
   - Example: Ranch with oil potential → Value includes mineral development potential

C. HYPOTHETICAL TRANSACTION:
   - Assumes willing buyer/seller negotiation
   - Not actual sale price (unless sale occurred at arm's length near valuation date)
   - Market conditions at valuation date control

D. RELEVANT FACTS KNOWN:
   - Buyer and seller have all material information
   - Includes latent defects, environmental issues, zoning restrictions
   - Example: Contaminated land valued with knowledge of contamination

VALUATION METHODS BY ASSET TYPE:

1. PUBLICLY TRADED SECURITIES (Treas. Reg. §20.2031-2):
   - Listed stocks/bonds: Mean of high and low on date of death
   - If no trading on date of death: Weighted average of nearest trading days before and after
   - Blockage discount: If large block would depress market if sold at once

2. REAL PROPERTY (Treas. Reg. §20.2031-1):
   - Comparable Sales Approach: Recent sales of similar properties, adjusted for differences
   - Income Approach: Capitalized net income from property
   - Cost Approach: Replacement cost less depreciation
   - Highest and best use assumption

3. CLOSELY HELD BUSINESS INTERESTS (Rev. Rul. 59-60):
   - Nature and history of business
   - Economic outlook (general and industry-specific)
   - Book value and financial condition
   - Earning capacity
   - Dividend-paying capacity
   - Goodwill or other intangible value
   - Sales of stock and size of block to be valued
   - Market price of comparable publicly traded companies

4. MINERAL INTERESTS:
   - Discounted cash flow: Present value of future royalties/production
   - Comparable sales: Recent sales of similar mineral interests
   - Engineering reports: Proven reserves, production rates, commodity prices

5. PARTNERSHIP/LLC INTERESTS:
   - Net asset value (if investment entity)
   - Income approach (if operating entity)
   - Discounts: Lack of control, lack of marketability

DISCOUNTS FROM PRO RATA VALUE:

A. LACK OF CONTROL (MINORITY INTEREST) DISCOUNT:
   - Non-controlling interest cannot force distributions, liquidation, or sale
   - Typical range: 15-35%
   - Factors: Voting power, distribution history, rights of minority

B. LACK OF MARKETABILITY DISCOUNT:
   - No ready market for closely held interests
   - Restricted stock studies show 25-45% discounts
   - Factors: Restrictions on transfer, holding period, dividend history

C. FRACTIONAL INTEREST DISCOUNT (REAL PROPERTY):
   - Undivided interests in real estate (e.g., 25% tenant in common)
   - Partition costs, co-owner disputes, limited marketability
   - Typical range: 20-40%

D. BLOCKAGE DISCOUNT (PUBLICLY TRADED STOCK):
   - Large block would depress market if sold rapidly
   - Requires expert testimony on market absorption capacity
   - Rare; typically for blocks >5% of outstanding shares

VALUATION DISPUTES WITH IRS:

COMMON IRS CHALLENGES:
- Appraisal based on incorrect facts (e.g., ignores comparable sales)
- Inappropriate discounts (e.g., discount for built-in capital gains - rejected by Tax Court)
- Incorrect valuation method (e.g., liquidation value when going concern appropriate)
- Inflated discounts (e.g., 60% combined discount - IRS argues double-counting)

DEFENSIVE APPRAISAL PRACTICES:
- Hire qualified appraiser (ASA, MAI credentials for real property; ASA, CFA for business valuations)
- Use multiple valuation methods (corroborate result)
- Document assumptions and limiting conditions
- Include sensitivity analysis (show range of values)
- Address IRS hot buttons (built-in capital gains, discount stacking)

BURDEN OF PROOF:
- Executor bears burden to establish values reported on Form 706
- Presumption of correctness for values supported by qualified appraisal
- IRS must offer contrary evidence to rebut
        """,
        key_factors=[
            "Valuation date (date of death or alternate valuation date)",
            "Comparable transactions (sales, market data)",
            "Asset-specific valuation methods (sales, income, cost approach)",
            "Highest and best use of property",
            "Discounts for lack of control, marketability, fractional interests",
            "Qualified appraisal from credentialed expert"
        ],
        primary_authority=[
            "Treas. Reg. §20.2031-1(b) (FMV Definition)",
            "Estate of Bright v. United States, 658 F.2d 999 (5th Cir. 1981) (Willing Buyer/Seller)",
            "Rev. Rul. 59-60 (Business Valuation Factors)",
            "Estate of Jones v. Commissioner, T.C. Memo 2019-101 (Fractional Interest Discounts)"
        ],
        burden_holder="Executor to establish FMV; IRS challenges if values appear too low or methodologically flawed",
        adversary_position="IRS argues higher values, rejects or minimizes discounts, challenges appraisal methodology",
        counter_arguments=[
            "FMV = actual sale price post-death (wrong: snapshot at valuation date, not hindsight)",
            "Discounts not available for family-controlled entities (wrong: FMV assumes hypothetical buyer)",
            "Built-in capital gains warrant discount (rejected: Estate of Jensen v. Commissioner)",
            "Liquidation value appropriate (wrong unless business actually liquidating; going concern value if operating)"
        ],
        resolution_strategy="""
VALUATION PROTOCOL:
STEP 1: Identify asset type
   - Publicly traded securities → Mean of high/low on date of death
   - Real property → Appraisal (comparable sales, income, cost)
   - Business interests → Rev. Rul. 59-60 factors, apply discounts
   - Mineral interests → DCF, comparable sales, engineering reports

STEP 2: Select appropriate valuation method(s)
   - Use multiple methods for corroboration
   - Document why selected method most appropriate

STEP 3: Determine applicable discounts
   - Lack of control: Does interest have voting power, control over management?
   - Lack of marketability: Is there ready market? Restrictions on transfer?
   - Fractional interest: Is property co-owned? Partition costs?

STEP 4: Engage qualified appraiser
   - Credentials: ASA, MAI (real property), CFA, ABV (business valuation)
   - Independence: Not related party, no contingent fee

STEP 5: Document assumptions and support
   - Comparable sales data
   - Financial projections (business valuation)
   - Market data (capitalization rates, discount rates)

STEP 6: Review for IRS hot buttons
   - Avoid: Built-in capital gains discount (rejected)
   - Avoid: Excessive stacking (e.g., 40% control + 40% marketability = 64% combined, likely challenged)
   - Prefer: Moderate, well-supported discounts (e.g., 25% control + 30% marketability = 47.5% combined)
        """,
        entity_scope="All property subject to estate tax valuation",
        confidence=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="Treas. Reg. §20.2031-1(b) + Estate of Bright",
        issue_category=IssueCategory.VALUATION_METHOD,
        fact_fragility_score=0.6
    ),

    # ──────────────────────────────────────────────────────────────────────
    # IRC §2032 - ALTERNATE VALUATION
    # ──────────────────────────────────────────────────────────────────────
    DoctrineBlock(
        topic="irc_2032_alternate_valuation_date",
        keywords=["alternate valuation", "irc 2032", "six months", "estate tax decrease", "value decrease"],
        conclusion_template=[
            "IRC §2032 allows estate to elect alternate valuation date (6 months after death) instead of date of death.",
            "Election permitted only if BOTH estate value AND estate tax decrease.",
            "Once elected, applies to all estate property (cannot cherry-pick assets)."
        ],
        reasoning_framework="""
IRC §2032 ALTERNATE VALUATION DATE ELECTION:

PURPOSE:
- Mitigate estate tax burden when asset values decline post-death
- Provides relief for estates during market downturns
- All-or-nothing election (cannot pick which assets to value at alternate date)

STATUTORY REQUIREMENTS (§2032(a)):
Election permitted ONLY IF BOTH:
1. Total value of gross estate (determined using alternate valuation) is LOWER than value at date of death
2. Estate tax liability is LOWER under alternate valuation

ALTERNATE VALUATION DATE:
- General Rule: 6 months after date of death
- Exception: If property distributed, sold, or disposed of within 6 months → Value at disposition date

MECHANICS:

DATE OF DEATH VALUATION (Default):
- Gross estate = $15M at death
- Estate tax = $2.5M (assume)

ALTERNATE VALUATION (6 Months Later):
- Gross estate = $12M (market declined)
- Estate tax = $1.8M (lower)
- Both conditions met → Alternate valuation election PERMITTED

EXAMPLE - ELECTION NOT PERMITTED:
- Date of death gross estate: $15M (tax = $2.5M)
- Alternate valuation gross estate: $14M (tax = $2.3M)
- Estate value decreased, estate tax decreased → Election permitted
- BUT: If specific bequest of $1M to charity made before 6 months:
  * Gross estate still $14M, but taxable estate lower due to deduction
  * If estate tax actually increases due to deduction timing → Election NOT permitted

ASSETS SOLD/DISTRIBUTED WITHIN 6 MONTHS:
- Value at date of sale/distribution (not 6-month date)
- Example: Stock worth $100K at death, sold for $80K three months later → Value = $80K (not 6-month value)
- Example: Real property worth $500K at death, still held at 6 months, worth $450K → Value = $450K

ALL-OR-NOTHING ELECTION:
- Cannot elect alternate valuation for some assets and date-of-death for others
- Applies to entire gross estate
- Example: Stock portfolio declines, real property appreciates → Must use alternate date for both

PROPERTY INTERESTS AFFECTED:
- §2033 property owned at death
- §2036-§2038 transferred property with retained interests
- §2040 joint tenancy property
- §2042 life insurance (if payable in installments and value changes)
- §2044 QTIP property

FORM 706 REPORTING:
- Part 3, Line 1: Check "Yes" for alternate valuation election
- Each schedule: Report values as of alternate date (or disposition date if earlier)
- Attach explanation of valuation dates for each asset

WHEN TO ELECT ALTERNATE VALUATION:

FAVORABLE SCENARIOS:
- Market crash after death (stock portfolio declines significantly)
- Real estate market downturn (property values drop)
- Business failure (closely held business loses value)
- Large estates near threshold (dropping below exemption saves tax)

UNFAVORABLE SCENARIOS:
- Mixed portfolio (some assets up, some down) → Cannot cherry-pick
- Estate below exemption threshold → No tax savings, so no benefit
- Income tax considerations → Beneficiaries prefer high basis (date of death often higher)

INTERACTION WITH IRC §1014 BASIS STEP-UP:
- Beneficiaries' basis = FMV at valuation date elected
- Alternate valuation election → Lower basis for beneficiaries (higher capital gains tax later)
- Trade-off: Estate tax savings vs. income tax cost to beneficiaries

EXAMPLE - INCOME TAX TRADE-OFF:
- Stock worth $1M at death, $800K at 6 months
- Estate elects alternate valuation → Saves estate tax (assume 40% = $80K saved)
- Beneficiary receives stock with $800K basis (not $1M)
- Beneficiary sells for $1.2M → Capital gain $400K (instead of $200K)
- Capital gains tax at 20% = $80K extra (vs. $40K if date-of-death basis)
- Net: Estate saved $80K, beneficiary pays $40K more → Net savings $40K

PLANNING CONSIDERATIONS:
- Project 6-month values before electing
- Consider beneficiaries' income tax situation (high basis preferred if holding long-term)
- Coordinate with portability election (if surviving spouse)
        """,
        key_factors=[
            "Gross estate value at date of death vs. 6 months later",
            "Estate tax liability at date of death vs. 6 months later",
            "Assets sold or distributed within 6 months (use disposition date)",
            "Income tax basis consequences for beneficiaries",
            "All-or-nothing nature of election"
        ],
        primary_authority=[
            "IRC §2032(a) (Alternate Valuation Election)",
            "IRC §2032(c) (Eligibility Requirements)",
            "Treas. Reg. §20.2032-1",
            "IRC §1014(a)(2) (Basis = Alternate Valuation if Elected)"
        ],
        burden_holder="Executor to demonstrate both value and tax decrease to justify election",
        adversary_position="IRS challenges if estate tax does not actually decrease, or if election made to manipulate basis",
        counter_arguments=[
            "Can elect alternate valuation for selected assets (wrong: all-or-nothing)",
            "Election automatic if values decline (wrong: affirmative election required on Form 706)",
            "6-month rule is flexible (wrong: strict 6-month date unless property disposed of earlier)"
        ],
        resolution_strategy="""
ELECTION ANALYSIS:
STEP 1: Calculate date-of-death gross estate and tax
STEP 2: Project 6-month values (or disposition values if earlier)
STEP 3: Calculate alternate valuation gross estate and tax
STEP 4: Compare:
   - Is gross estate lower? YES → Continue
   - Is estate tax lower? YES → Election permitted
   - If either NO → Election NOT permitted
STEP 5: Consider beneficiary income tax consequences
   - Higher basis at date of death → Lower capital gains later
   - Lower basis at alternate date → Higher capital gains later
   - Weigh estate tax savings vs. beneficiary income tax cost
STEP 6: Make election on Form 706, Part 3, Line 1
STEP 7: Use alternate values throughout Form 706 schedules

DEFENSIVE CHECKLIST:
□ Both gross estate value and estate tax decrease confirmed
□ Projected 6-month values conservative (avoid IRS challenge)
□ Disposition dates documented for assets sold/distributed within 6 months
□ Beneficiaries informed of lower basis (income tax planning)
□ Portability election coordinated (if applicable)
        """,
        entity_scope="Entire gross estate (all-or-nothing election)",
        confidence=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="IRC §2032 + Treas. Reg. §20.2032-1",
        issue_category=IssueCategory.VALUATION_METHOD,
        fact_fragility_score=0.3
    ),

    # ──────────────────────────────────────────────────────────────────────
    # IRC §2032A - SPECIAL USE VALUATION
    # ──────────────────────────────────────────────────────────────────────
    DoctrineBlock(
        topic="irc_2032a_special_use_valuation_farms_ranches",
        keywords=["special use valuation", "irc 2032a", "farm", "ranch", "qualified real property", "continuing use"],
        conclusion_template=[
            "IRC §2032A allows estates to elect special use valuation for qualifying farms and ranches, valuing property based on actual use (agricultural) rather than highest and best use (development).",
            "Maximum reduction: $1,390,000 (2025) from FMV.",
            "Strict requirements: Material participation, qualified use, family ownership, recapture if cease qualified use within 10 years."
        ],
        reasoning_framework="""
IRC §2032A SPECIAL USE VALUATION - FARMS AND RANCHES:

PURPOSE:
- Prevent forced sales of family farms/ranches to pay estate tax
- Value based on actual agricultural use, not development potential
- Significant tax savings in areas with high development pressure (e.g., land near cities)

MAXIMUM REDUCTION (2025):
- $1,390,000 reduction from FMV (indexed annually for inflation)
- Example: Ranch FMV $3M (development value), special use value $1.7M → $1.3M reduction (within limit)

QUALIFIED REAL PROPERTY REQUIREMENTS (§2032A(b)):

1. DESIGNATED IN AGREEMENT:
   - Executor must file agreement signed by all parties with interest in property
   - Heirs consent to recapture if cease qualified use within 10 years

2. LOCATED IN UNITED STATES:
   - No foreign property eligible

3. USED AS FARM OR CLOSELY HELD BUSINESS:
   - Farm: Cultivation of soil, raising livestock, operation of ranch, nursery, orchard
   - Closely held business: Trade or business with <50% owned by non-family

4. 50% OF GROSS ESTATE TEST:
   - Adjusted value of real and personal property used in qualified use must be ≥50% of adjusted value of gross estate
   - Adjusted value = FMV minus mortgages/debt

5. 25% OF GROSS ESTATE TEST:
   - Adjusted value of qualified real property must be ≥25% of adjusted value of gross estate

6. OWNERSHIP AND USE TESTS (§2032A(b)(1)):
   - Property owned by decedent or family member and used for qualified use for 5 of last 8 years before death
   - Material participation by decedent or family member for 5 of last 8 years

7. PASSING TO QUALIFIED HEIR:
   - Property must pass to family member (spouse, ancestors, lineal descendants, spouses of lineal descendants)

MATERIAL PARTICIPATION:
- Regular, continuous, substantial involvement in farm/ranch operations
- NOT passive investment (cannot lease to unrelated third party)
- Factors (similar to IRC §469 real estate professional test):
  * Time spent on activities
  * Direct involvement in management decisions
  * Financial risk borne by participant

VALUATION METHOD - ACTUAL USE:
- Capitalize net rental income from comparable farms/ranches in area
- Formula: Annual gross cash rental / Average annual effective interest rate for farm loans
- Example: Comparable ranches rent for $100/acre annually, farm loan rate 5% → Special use value = $100 / 0.05 = $2,000/acre
- Compare to FMV development value (e.g., $10,000/acre) → $8,000/acre reduction (up to $1.39M total)

RECAPTURE TAX (§2032A(c)):
- If qualified heir CEASES qualified use within 10 years of decedent's death → Recapture
- If qualified heir disposes of property to non-family member within 10 years → Recapture
- Recapture amount: Additional estate tax = (FMV at death - Special use value) × Marginal estate tax rate
- Example: $1M reduction elected, heir sells ranch 5 years later → Recapture tax = $1M × 40% = $400K

EXCEPTIONS TO RECAPTURE:
- Disposition to family member (qualified heir)
- Involuntary conversion (condemnation, casualty) if replaced with qualified property within 2 years
- Like-kind exchange (IRC §1031) for qualified replacement property
- Death of qualified heir (recapture period terminates)

TEXAS RANCH/FARM APPLICATIONS:

FAVORABLE SCENARIOS:
- Ranch near Austin, San Antonio, Dallas, Houston (high development pressure)
- FMV for development far exceeds agricultural use value
- Family wants to continue ranching (meet material participation)
- Estate large enough that reduction creates tax savings

UNFAVORABLE SCENARIOS:
- Estate below exemption threshold (no tax savings)
- Heirs plan to sell or develop within 10 years (recapture risk)
- Passive investment ranch (leased to third party, no material participation)

COMMON TEXAS RANCH USES:
- Cattle ranching (cow-calf operations, stocker cattle)
- Sheep and goat ranching
- Wildlife management (if qualifies under Texas ag exemption rules)
- Hay production, timber

FORM 706 REPORTING:
- Schedule A-1: Elect §2032A, describe property, show FMV and special use value
- Attach: Qualified use agreement (Form 706-A) signed by all heirs
- Attach: Appraisal showing FMV and special use valuation methodology
- Attach: Documentation of material participation (calendars, logs, financial records)

INTERACTION WITH OTHER ESTATE TAX PROVISIONS:
- Can combine with alternate valuation (§2032) if both requirements met (rare)
- Does not affect community property characterization (still 50% inclusion)
- Recapture tax NOT deductible on Form 706 (paid by heirs post-filing)

PLANNING STRATEGIES:

PRE-DEATH:
- Document material participation (keep logs, photos, financial records)
- Structure ownership to meet 50%/25% tests (consider gifting non-farm assets)
- Execute family partnership/LLC to ensure qualified use continues (if heirs participate)

POST-DEATH:
- Heirs must maintain qualified use for 10 years (no sale to non-family, no conversion to non-farm use)
- Heirs should continue material participation (not just lease out)
- If contemplating sale, consider like-kind exchange (§1031) to qualified replacement property
        """,
        key_factors=[
            "Qualified real property used in farming/ranching",
            "50% of gross estate and 25% of gross estate tests",
            "Material participation by decedent or family for 5 of last 8 years",
            "Property passes to qualified heir (family member)",
            "Continuing qualified use for 10 years post-death (recapture risk)",
            "Valuation methodology (capitalize comparable rents)"
        ],
        primary_authority=[
            "IRC §2032A(a) (Election)",
            "IRC §2032A(b) (Qualified Real Property)",
            "IRC §2032A(c) (Recapture Tax)",
            "IRC §2032A(e)(7) (Material Participation)",
            "Treas. Reg. §20.2032A-3 (Material Participation)",
            "Treas. Reg. §20.2032A-4 (Valuation Method)"
        ],
        burden_holder="Executor to establish all qualification requirements; IRS challenges material participation and valuation",
        adversary_position="IRS scrutinizes material participation (passive leasing disqualifies), challenges low special use values",
        counter_arguments=[
            "Wildlife management automatically qualifies (wrong: must meet material participation and qualified use tests)",
            "Leasing to third party qualifies (wrong: material participation required, passive leasing disqualifies)",
            "Recapture only if sell entire property (wrong: ceasing qualified use also triggers recapture)",
            "10-year period starts at filing Form 706 (wrong: starts at date of death)"
        ],
        resolution_strategy="""
QUALIFICATION ANALYSIS:
STEP 1: Identify qualified real property (farm/ranch land in U.S.)
STEP 2: Calculate 50% and 25% tests
   - Adjusted value of qualified property / Adjusted gross estate ≥ 50%? (farm + ranch property)
   - Adjusted value of qualified real property / Adjusted gross estate ≥ 25%? (just real property)
STEP 3: Document material participation
   - Decedent/family member involvement 5 of last 8 years?
   - Evidence: Time logs, financial records, operational involvement
STEP 4: Confirm property passing to qualified heir
   - Spouse, children, grandchildren, or their spouses?
STEP 5: Value property under special use
   - Comparable rental rates in area / Farm loan interest rate
   - Calculate reduction (FMV - Special use value, max $1.39M)
STEP 6: Execute qualified use agreement (Form 706-A)
   - All heirs sign, consenting to recapture if cease use within 10 years
STEP 7: File election on Form 706, Schedule A-1

POST-DEATH COMPLIANCE (Heirs):
□ Continue qualified use for 10 years (farming, ranching)
□ Maintain material participation (not passive investment)
□ If sell, dispose only to family member OR execute §1031 exchange
□ If involuntary conversion, replace within 2 years
□ Notify IRS of any recapture event (file Form 706-A(1))

DEFENSIVE DOCUMENTATION:
- Material participation logs (hours spent, activities performed)
- Financial records (income/expenses from farm/ranch operations)
- Comparable rental data (support special use valuation)
- Appraisal (show FMV and special use value with methodology)
        """,
        entity_scope="Qualified real property used in farming or ranching",
        confidence=ConfidenceStratification.AGGRESSIVE,
        controlling_precedent="IRC §2032A + Treas. Reg. §20.2032A-3, §20.2032A-4",
        issue_category=IssueCategory.SPECIAL_VALUATION,
        fact_fragility_score=0.65,
        disclosure_caveat="Material participation is fact-intensive; IRS frequently challenges. Document extensively."
    ),

    # ──────────────────────────────────────────────────────────────────────
    # DISCOUNTS - LACK OF MARKETABILITY
    # ──────────────────────────────────────────────────────────────────────
    DoctrineBlock(
        topic="lack_of_marketability_discount_dlom",
        keywords=["marketability discount", "dlom", "closely held", "restricted stock", "illiquid"],
        conclusion_template=[
            "Lack of marketability discount (DLOM) reduces FMV of closely held interests due to absence of ready market.",
            "Typical range: 25-45% based on restricted stock studies.",
            "Factors: Transfer restrictions, dividend history, company size, prospects for liquidity event."
        ],
        reasoning_framework="""
LACK OF MARKETABILITY DISCOUNT (DLOM):

CONCEPT:
- Marketable securities (NYSE, NASDAQ) can be sold instantly at known price
- Closely held interests (private company stock, LLC/partnership interests) have no ready market
- Hypothetical willing buyer demands discount for illiquidity
- DLOM reflects cost and time to find buyer, negotiate, and close transaction

EMPIRICAL SUPPORT - RESTRICTED STOCK STUDIES:
- Pre-IPO restricted stock trades at discount to publicly traded stock of same company
- Studies show discounts of 25-45% on average (Stout Restricted Stock Study, FMV Opinions)
- Factors affecting discount magnitude:
  * Company size (smaller = higher discount)
  * Financial performance (losses = higher discount)
  * Dividend history (no dividends = higher discount)
  * Time to liquidity event (IPO, acquisition) (longer = higher discount)

QUALIFIED APPRAISAL REQUIREMENT:
- Must be supported by qualified independent appraiser
- Appraiser considers company-specific factors (not just average from studies)
- IRS scrutinizes aggressive discounts (>45% often challenged)

FACTORS INCREASING DLOM:

1. TRANSFER RESTRICTIONS:
   - Right of first refusal in operating agreement/shareholders agreement
   - Consent requirements (board or other members must approve transfer)
   - Lock-up periods
   - No established market for interests

2. COMPANY CHARACTERISTICS:
   - Small company size (< $10M revenue) → Higher discount
   - Losses or marginal profitability → Higher discount
   - Limited financial information available to potential buyers → Higher discount
   - Lack of professional management → Higher discount

3. PROSPECT FOR LIQUIDITY:
   - No planned IPO or sale → Higher discount
   - Family-controlled with no exit strategy → Higher discount
   - Industry consolidation (potential acquisition targets) → Lower discount

4. DIVIDEND/DISTRIBUTION HISTORY:
   - No distributions to owners → Higher discount (no cash flow to owner until sale)
   - Regular distributions → Lower discount (owner receives cash despite illiquidity)

FACTORS DECREASING DLOM:

1. STRONG FINANCIAL PERFORMANCE:
   - Profitable, growing company → Lower discount
   - Attractive acquisition target → Lower discount

2. LIQUIDITY PROSPECTS:
   - Planned IPO or sale in near term → Lower discount
   - Industry with active M&A market → Lower discount

3. DISTRIBUTIONS:
   - Regular dividends or distributions to owners → Lower discount

TYPICAL DLOM RANGES BY COMPANY TYPE:

- Mature, profitable company, regular distributions: 20-30%
- Mid-size company, moderate profitability, infrequent distributions: 30-40%
- Small or unprofitable company, no distributions, heavy restrictions: 40-50%
- Startup or distressed company, no distributions, uncertain future: 50%+ (rare)

DLOM vs. DISCOUNT FOR LACK OF CONTROL (DLOC):
- DLOM: Illiquidity discount (no ready market)
- DLOC: Minority interest discount (cannot control company decisions)
- Can apply BOTH if interest is non-controlling AND illiquid
- Combined discount formula: 1 - [(1 - DLOC) × (1 - DLOM)]
- Example: 25% DLOC + 35% DLOM = 1 - [(1 - 0.25) × (1 - 0.35)] = 1 - [0.75 × 0.65] = 1 - 0.4875 = 51.25% combined

IRS CHALLENGES TO DLOM:

BUILT-IN CAPITAL GAINS DISCOUNT:
- Some appraisers discount for built-in capital gains (company holds appreciated assets)
- IRS position: No discount for built-in gains (Estate of Jensen v. Commissioner)
- Tax Court rejected: Hypothetical buyer would not pay less due to entity-level tax
- Defensive approach: Do NOT include built-in gains discount

CIRCULAR LOGIC:
- IRS argues DLOM based on time to sell, but discounted value itself makes it harder to sell
- Courts generally reject IRS argument; DLOM is legitimate

AGGRESSIVE STACKING:
- Combining high DLOC (e.g., 40%) with high DLOM (e.g., 45%) yields ~67% discount
- IRS challenges if total discount exceeds 50-55% absent exceptional circumstances

SECTION 2704 RESTRICTIONS:
- §2704(b): Disregards certain transfer restrictions in family-controlled entities
- Applicable restriction: Limitation on liquidation rights more restrictive than state law default
- Effect: May reduce or eliminate DLOM if restriction is disregarded
- Complex analysis; requires comparing operating agreement to state LLC/partnership statute

TEXAS LLC/PARTNERSHIP DEFAULT RULES:
- Texas Business Organizations Code (TBOC) provides default rights absent agreement
- TBOC §11.313: Member may withdraw and receive FMV of interest (unless agreement restricts)
- Operating agreement restriction on withdrawal → Potentially §2704 applicable restriction
- Defensive: Ensure restrictions have legitimate business purpose (not solely tax-motivated)

DEFENSIVE APPRAISAL PRACTICES:
- Use qualified appraiser with credentials (ASA, CFA, ABV)
- Cite restricted stock studies (Stout, FMV Opinions, Pluris)
- Apply company-specific factors (do not just use average)
- Moderate discounts (25-40% DLOM defensible; >45% often challenged)
- Avoid built-in capital gains discount (rejected by courts)
- Document business purpose for transfer restrictions (not just tax planning)
        """,
        key_factors=[
            "Absence of ready market for closely held interests",
            "Transfer restrictions in operating agreement/shareholders agreement",
            "Company size, profitability, financial performance",
            "Dividend/distribution history",
            "Prospects for liquidity event (IPO, sale)",
            "Restricted stock studies (empirical support)",
            "Interaction with §2704 restrictions on liquidation rights"
        ],
        primary_authority=[
            "Treas. Reg. §20.2031-1(b) (FMV Definition - Hypothetical Buyer/Seller)",
            "Estate of Jones v. Commissioner, T.C. Memo 2019-101 (DLOM Upheld at 35%)",
            "Estate of Jensen v. Commissioner, T.C. Memo 2010-182 (Built-In Gains Discount Rejected)",
            "IRC §2704(b) (Applicable Restrictions Disregarded)",
            "Stout Restricted Stock Study (Empirical Data)"
        ],
        burden_holder="Executor to establish DLOM with qualified appraisal; IRS challenges excessive discounts",
        adversary_position="IRS argues DLOM overstated, restrictions are §2704 applicable restrictions, or built-in gains discount inappropriate",
        counter_arguments=[
            "Public company comparables show no discount needed (wrong: closely held interests are illiquid)",
            "Family can easily sell to each other (wrong: FMV assumes hypothetical buyer, not family transaction)",
            "Built-in capital gains warrant additional discount (rejected: Estate of Jensen)",
            "DLOM + DLOC cannot exceed 50% (wrong: combined discounts can exceed 50% if supported)"
        ],
        resolution_strategy="""
DLOM ANALYSIS FRAMEWORK:
STEP 1: Identify factors supporting DLOM
   - Transfer restrictions in governing documents
   - No ready market (closely held)
   - Company financial performance (profitable vs. losses)
   - Distribution history (regular vs. none)

STEP 2: Review restricted stock studies
   - Average discounts (25-45% range)
   - Select comparable study (company size, industry)

STEP 3: Apply company-specific adjustments
   - Increase discount: Small size, losses, no distributions, heavy restrictions
   - Decrease discount: Profitable, growth, distributions, liquidity prospects

STEP 4: Select DLOM percentage (typically 25-40%)
   - Conservative: 25-30% (profitable, distributions)
   - Moderate: 30-40% (typical closely held)
   - Aggressive: 40-45% (small, unprofitable, no distributions)

STEP 5: Check for §2704 applicable restrictions
   - Compare operating agreement liquidation rights to state law default (Texas TBOC)
   - If restriction more restrictive than default → Potentially disregarded
   - If disregarded → DLOM may be reduced or eliminated

STEP 6: Document in appraisal report
   - Cite restricted stock studies
   - Explain company-specific factors
   - Justify selected discount percentage
   - Avoid built-in capital gains discount

STEP 7: Combine with DLOC if applicable
   - Formula: 1 - [(1 - DLOC) × (1 - DLOM)]
   - Check total discount reasonableness (<55% defensible; >60% often challenged)

DEFENSIVE CHECKLIST:
□ Qualified independent appraiser engaged
□ Restricted stock studies cited
□ Company-specific factors analyzed
□ DLOM in 25-40% range (moderate)
□ No built-in capital gains discount
□ §2704 analysis if family-controlled entity
□ Combined discount (DLOC + DLOM) reasonable (<55%)
        """,
        entity_scope="Closely held business interests (corporation, LLC, partnership)",
        confidence=ConfidenceStratification.AGGRESSIVE,
        controlling_precedent="Treas. Reg. §20.2031-1(b) + Estate of Jones (DLOM upheld)",
        issue_category=IssueCategory.DISCOUNT_APPLICABILITY,
        fact_fragility_score=0.7,
        disclosure_caveat="DLOM >40% frequently challenged; ensure qualified appraisal with strong support"
    ),

    # ──────────────────────────────────────────────────────────────────────
    # DISCOUNTS - LACK OF CONTROL
    # ──────────────────────────────────────────────────────────────────────
    DoctrineBlock(
        topic="lack_of_control_discount_dloc_minority_interest",
        keywords=["control discount", "dloc", "minority interest", "voting power", "non-controlling"],
        conclusion_template=[
            "Discount for lack of control (DLOC) reduces FMV of non-controlling interests in business entities.",
            "Typical range: 15-35% based on inability to force distributions, liquidation, or sale.",
            "Factors: Voting percentage, distribution history, rights of minority holders, marketability of interest."
        ],
        reasoning_framework="""
DISCOUNT FOR LACK OF CONTROL (DLOC) / MINORITY INTEREST DISCOUNT:

CONCEPT:
- Controlling interest (>50% voting) can force major decisions: distributions, liquidation, sale, management changes
- Non-controlling (minority) interest cannot compel action; subject to majority's decisions
- Hypothetical willing buyer demands discount for lack of control
- DLOC reflects economic disadvantage of minority position

EMPIRICAL SUPPORT:
- Public company minority blocks trade at discount to control premium transactions (M&A)
- Control premium studies (Mergerstat, FactSet): Acquisitions pay 25-40% premium over market price
- DLOC is inverse of control premium: DLOC = 1 - [1 / (1 + Control Premium)]
- Example: Control premium 30% → DLOC = 1 - [1 / 1.30] = 23%

FACTORS INCREASING DLOC:

1. LOW VOTING PERCENTAGE:
   - <10% interest: High DLOC (30-35%)
   - 10-25% interest: Moderate DLOC (20-30%)
   - 25-50% interest: Lower DLOC (15-25%)
   - 50%+ interest: No DLOC (controlling interest)

2. NO DISTRIBUTIONS:
   - Majority retains earnings, pays no dividends → Minority receives no cash flow
   - Higher DLOC (35%+)

3. SUPERMAJORITY VOTING REQUIREMENTS:
   - Operating agreement requires >50% vote for major actions
   - Even 50% holder cannot control → DLOC may apply

4. OPPRESSIVE MAJORITY:
   - History of majority ignoring minority interests
   - No board representation for minority
   - Higher DLOC

FACTORS DECREASING DLOC:

1. STRONG MINORITY PROTECTIONS:
   - Operating agreement grants minority veto rights (major transactions)
   - Mandatory distributions (e.g., tax distributions to cover K-1 income)
   - Board representation proportional to ownership
   - Lower DLOC (15-20%)

2. REGULAR DISTRIBUTIONS:
   - Consistent dividend/distribution history
   - Minority receives cash flow despite lack of control
   - Lower DLOC

3. NEAR-CONTROLLING INTEREST:
   - 45-49% interest (close to control)
   - Lower DLOC (15-20%)

4. FAMILY-CONTROLLED ENTITY:
   - Family members unlikely to oppress each other (assumed)
   - IRS argues lower DLOC in family context
   - But: FMV assumes hypothetical buyer, not family (Estate of Bosca)

TYPICAL DLOC RANGES:

- Controlling interest (>50%): 0% (no discount)
- Near-controlling (40-50%): 15-20%
- Significant minority (25-40%): 20-25%
- Moderate minority (10-25%): 25-30%
- Small minority (<10%): 30-35%

DLOC IN DIFFERENT ENTITY TYPES:

C CORPORATION:
- Voting power determines control
- Minority shareholders have limited rights (vote for directors, approve major transactions)
- Typical DLOC: 25-35% for <25% interests

S CORPORATION:
- Similar to C Corp for voting, but mandatory tax distributions common
- DLOC may be lower if tax distributions provided (20-30%)

LLC / PARTNERSHIP:
- Operating/partnership agreement controls
- Default: Majority vote controls (check state law)
- DLOC depends on agreement terms (veto rights, distribution requirements)
- Texas TBOC: Manager-managed LLC, members have limited control → Higher DLOC

FAMILY LIMITED PARTNERSHIP (FLP):
- General Partner (GP) has control (even if 1% interest)
- Limited Partners (LP) have no control (even if 99% interest)
- LP interests: High DLOC (30-40%)
- GP interest: No DLOC (controlling)

SWING VOTE PREMIUM:
- If ownership fragmented (e.g., three 33% owners), each may have swing vote power
- Swing vote can determine which coalition controls → Lower DLOC or premium
- Example: 33% interest in three-person LLC → 15-20% DLOC (not 30%), due to swing vote

DLOC vs. DLOM INTERACTION:
- DLOC: Lack of control over entity
- DLOM: Lack of ready market for interest
- Both can apply to same interest (non-controlling AND illiquid)
- Combined discount formula: 1 - [(1 - DLOC) × (1 - DLOM)]
- Example: 25% DLOC + 30% DLOM = 1 - [0.75 × 0.70] = 47.5% combined

IRS CHALLENGES TO DLOC:

FAMILY ATTRIBUTION:
- IRS argues family members should be attributed to each other (aggregate control)
- Courts reject: FMV assumes hypothetical buyer, not family members acting together (Estate of Bonner)

CONTROL PREMIUM DATA:
- IRS may argue control premium studies not applicable to closely held companies
- Defensive: Use restricted stock studies as corroboration

VOTING AGREEMENTS:
- If decedent and family members had voting agreement (pool votes), IRS may argue control exists
- Defensive: No voting agreement, or agreement terminates at death

DOUBLE DISCOUNTING:
- IRS argues DLOC already captured in DLOM (both reflect lack of control)
- Courts reject: DLOC and DLOM are independent factors (Estate of Jones)

DEFENSIVE APPRAISAL PRACTICES:
- Use control premium studies (Mergerstat, FactSet) to derive DLOC
- Apply company-specific factors (voting %, distribution history, minority rights)
- Moderate DLOC (20-30% typical; >35% often challenged)
- Document that FMV assumes hypothetical buyer (not family transaction)
- Avoid double-counting with DLOM (but both can apply if independent)
        """,
        key_factors=[
            "Voting percentage (controlling vs. non-controlling)",
            "Ability to force distributions, liquidation, or sale",
            "Minority protections in operating agreement",
            "Distribution history (regular vs. none)",
            "Control premium data (M&A transactions)",
            "Swing vote considerations (fragmented ownership)"
        ],
        primary_authority=[
            "Treas. Reg. §20.2031-1(b) (FMV Hypothetical Buyer/Seller)",
            "Estate of Bonner v. United States, 84 F.3d 196 (5th Cir. 1996) (DLOC Upheld, No Family Attribution)",
            "Estate of Jones v. Commissioner, T.C. Memo 2019-101 (DLOC + DLOM Both Apply)",
            "Mergerstat Control Premium Study (Empirical Data)"
        ],
        burden_holder="Executor to establish DLOC with qualified appraisal; IRS challenges family attribution and excessive discounts",
        adversary_position="IRS argues family members should be aggregated (no DLOC), or DLOC overstated due to family dynamics",
        counter_arguments=[
            "Family members act together, so controlling interest (wrong: FMV assumes hypothetical buyer, Estate of Bonner)",
            "DLOC + DLOM is double-counting (wrong: independent discounts, Estate of Jones)",
            "Control premium studies only apply to public companies (wrong: widely used for closely held valuations)",
            "Minority interest in family entity has no discount (wrong: FMV standard applies regardless of family)"
        ],
        resolution_strategy="""
DLOC ANALYSIS FRAMEWORK:
STEP 1: Determine voting percentage
   - >50%: Controlling interest, no DLOC
   - 40-50%: Near-controlling, 15-20% DLOC
   - 25-40%: Significant minority, 20-25% DLOC
   - 10-25%: Moderate minority, 25-30% DLOC
   - <10%: Small minority, 30-35% DLOC

STEP 2: Review operating agreement / governing documents
   - Minority veto rights? (reduces DLOC)
   - Supermajority requirements? (may increase DLOC even for 50% holder)
   - Mandatory distributions? (reduces DLOC)
   - Board representation? (reduces DLOC if proportional)

STEP 3: Assess distribution history
   - Regular distributions: Lower DLOC (15-25%)
   - No distributions: Higher DLOC (25-35%)

STEP 4: Check for swing vote premium
   - Fragmented ownership (e.g., three equal owners)? → Lower DLOC (15-20%)
   - Two-owner 50/50? → Potential deadlock, but no clear control → DLOC may apply

STEP 5: Review control premium studies
   - Mergerstat, FactSet data: Typical control premiums 25-40%
   - Calculate implied DLOC: 1 - [1 / (1 + Control Premium)]

STEP 6: Select DLOC percentage
   - Conservative: 15-20% (near-controlling, strong minority rights)
   - Moderate: 20-30% (typical minority interest)
   - Aggressive: 30-35% (small minority, no distributions, weak minority rights)

STEP 7: Combine with DLOM if applicable
   - Formula: 1 - [(1 - DLOC) × (1 - DLOM)]
   - Total discount check: <55% defensible; >60% often challenged

STEP 8: Document in appraisal
   - Cite control premium studies
   - Explain company-specific factors
   - Justify selected DLOC percentage
   - Clarify that FMV assumes hypothetical buyer (not family aggregation)

DEFENSIVE CHECKLIST:
□ Qualified independent appraiser
□ Control premium studies cited
□ Company-specific factors (voting %, distributions, minority rights)
□ DLOC in 15-30% range (moderate)
□ No family attribution assumption (hypothetical buyer standard)
□ DLOC + DLOM both justified as independent discounts
□ Total combined discount reasonable (<55%)
        """,
        entity_scope="Non-controlling interests in business entities (corporation, LLC, partnership, FLP)",
        confidence=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="Treas. Reg. §20.2031-1(b) + Estate of Bonner (5th Cir.)",
        issue_category=IssueCategory.DISCOUNT_APPLICABILITY,
        fact_fragility_score=0.6
    ),

    # ──────────────────────────────────────────────────────────────────────
    # FRACTIONAL INTEREST DISCOUNTS (REAL PROPERTY)
    # ──────────────────────────────────────────────────────────────────────
    DoctrineBlock(
        topic="fractional_interest_discount_real_property",
        keywords=["fractional interest", "undivided interest", "tenancy in common", "partition", "co-owner"],
        conclusion_template=[
            "Fractional interests in real property (tenancy in common, undivided mineral interests) are discounted due to partition costs, co-owner disputes, and limited marketability.",
            "Typical range: 20-40% depending on property type and number of co-owners.",
            "Factors: Partition complexity, co-owner relationships, property type, encumbrances."
        ],
        reasoning_framework="""
FRACTIONAL INTEREST DISCOUNT - REAL PROPERTY:

CONCEPT:
- Tenancy in common (TIC): Multiple owners hold undivided fractional interests (e.g., 3 siblings each own 33.33%)
- No right of survivorship (unlike joint tenancy)
- Each co-owner can sell their interest, but buyer becomes co-owner with others
- Hypothetical buyer demands discount due to:
  1. Cannot solely control property (must cooperate with co-owners)
  2. Partition costs (legal action to divide or force sale)
  3. Limited marketability (difficult to find buyer for fractional interest)

PARTITION PROCESS (Texas Property Code §23.001):
- Partition in kind: Physical division of property (if feasible)
- Partition by sale: Forced sale, proceeds divided proportionately
- Costs: Attorney fees, surveyor, appraisal, court costs
- Time: 6-18 months typical litigation
- Uncertainty: Court determines whether partition in kind or sale

FACTORS INCREASING FRACTIONAL INTEREST DISCOUNT:

1. LARGE NUMBER OF CO-OWNERS:
   - 2 co-owners: Lower discount (25-30%)
   - 3-5 co-owners: Moderate discount (30-35%)
   - >5 co-owners: Higher discount (35-40%)
   - More co-owners = more disputes, harder to coordinate

2. ADVERSARIAL CO-OWNERS:
   - History of disputes among co-owners → Higher discount
   - Co-owners with conflicting interests (one wants to develop, one wants to hold) → Higher discount

3. COMPLEX PROPERTY:
   - Improved property (house, commercial building): Difficult to partition in kind → Higher discount
   - Encumbered property (mortgage, easements): Complicates partition → Higher discount
   - Environmental issues: Potential liability for all co-owners → Higher discount

4. SMALL FRACTIONAL INTEREST:
   - <10% interest: Very limited marketability → Higher discount (35-40%)
   - 10-25% interest: Moderate marketability → 30-35%
   - 25-50% interest: Better marketability → 25-30%

FACTORS DECREASING FRACTIONAL INTEREST DISCOUNT:

1. EASILY DIVISIBLE PROPERTY:
   - Raw land: Can be subdivided → Lower discount (20-25%)
   - Separate mineral tracts: Independent value → Lower discount

2. COOPERATIVE CO-OWNERS:
   - Family members with shared goals → Lower discount
   - Professional co-ownership (investment partners) → Lower discount

3. LARGE FRACTIONAL INTEREST:
   - 50% interest: Significant control → Lower discount (20-25%)
   - Swing vote in 3-owner scenario → Lower discount

TYPICAL FRACTIONAL INTEREST DISCOUNTS:

UNDEVELOPED LAND:
- 2 co-owners: 20-25%
- 3-5 co-owners: 25-30%
- >5 co-owners: 30-35%

IMPROVED PROPERTY (HOUSE, BUILDING):
- 2 co-owners: 25-30%
- 3-5 co-owners: 30-35%
- >5 co-owners: 35-40%

MINERAL INTERESTS (UNDIVIDED):
- 2 co-owners: 20-25%
- 3-5 co-owners: 25-30%
- >5 co-owners: 30-35%
- Mineral interests often easier to value separately → Lower discount than improved property

PARTITION COST ANALYSIS:
- Attorney fees: $10K-$50K typical
- Surveyor/engineer: $5K-$20K
- Appraisal: $3K-$10K
- Court costs: $1K-$5K
- Total: $20K-$85K typical partition litigation
- As % of property value: Larger impact on lower-value properties

EXAMPLE:
- Ranch worth $1M, 4 siblings each own 25% TIC
- Decedent's 25% interest = $250K pro rata (no discount)
- Partition costs estimated $40K (4% of total value)
- Limited marketability (difficult to sell 25% TIC interest)
- Fractional interest discount: 30%
- Discounted value: $250K × (1 - 0.30) = $175,000

TEXAS-SPECIFIC CONSIDERATIONS:

PARTITION LAW (Texas Property Code Chapter 23):
- Any co-owner can force partition
- Court decides partition in kind vs. sale
- Preference for partition in kind if feasible
- Costs typically shared proportionately

MINERAL INTERESTS:
- Very common to have fractional mineral ownership in Texas
- Undivided interest in oil/gas royalties
- Partition rarely practical (cannot physically divide subsurface)
- Discount typically 25-35% depending on number of co-owners

RANCH LAND:
- Family ranches often held TIC by multiple heirs
- Partition in kind may be feasible (subdivide acreage)
- Discount 25-30% typical for 3-5 co-owners

IRS CHALLENGES TO FRACTIONAL INTEREST DISCOUNTS:

FAMILY UNITY ARGUMENT:
- IRS argues family co-owners will cooperate, so no discount warranted
- Courts reject: FMV assumes hypothetical buyer, not family (Estate of Pillsbury)

PARTITION COST TOO SPECULATIVE:
- IRS argues partition may never occur, so costs irrelevant
- Courts accept: Hypothetical buyer would consider partition as option (Estate of Barge)

EXCESSIVE DISCOUNT:
- IRS challenges discounts >40% as excessive
- Defensive: Support with partition cost analysis, comparable sales of fractional interests

COMPARABLE SALES:
- Best evidence: Actual sales of fractional TIC interests in similar properties
- Rare to find, but strong evidence if available

DEFENSIVE APPRAISAL PRACTICES:
- Quantify partition costs (attorney, surveyor, appraiser, court)
- Analyze partition feasibility (in kind vs. sale)
- Research comparable sales of fractional interests (if available)
- Apply moderate discount (25-35% defensible; >40% often challenged)
- Document assumption of hypothetical buyer (not family cooperation)
        """,
        key_factors=[
            "Number of co-owners (more = higher discount)",
            "Property type (improved property higher than raw land)",
            "Partition costs and complexity",
            "Co-owner relationships (adversarial vs. cooperative)",
            "Fractional interest size (smaller = higher discount)",
            "Marketability of fractional interest"
        ],
        primary_authority=[
            "Treas. Reg. §20.2031-1(b) (FMV Standard)",
            "Estate of Pillsbury v. Commissioner, T.C. Memo 1993-491 (Fractional Interest Discount Upheld 44%)",
            "Estate of Barge v. Commissioner, T.C. Memo 1997-188 (Partition Costs Relevant)",
            "Texas Property Code Chapter 23 (Partition Procedure)"
        ],
        burden_holder="Executor to establish fractional interest discount with appraisal; IRS challenges family unity and excessive discounts",
        adversary_position="IRS argues family co-owners will cooperate (no discount), partition costs speculative, or discount excessive",
        counter_arguments=[
            "Family co-owners, so no discount (wrong: FMV assumes hypothetical buyer, Estate of Pillsbury)",
            "Partition costs irrelevant (wrong: hypothetical buyer considers partition option, Estate of Barge)",
            "Fractional interest = pro rata value (wrong: fractional interests discounted due to partition and marketability)",
            "Discount >40% never allowed (wrong: depends on facts; Pillsbury upheld 44%)"
        ],
        resolution_strategy="""
FRACTIONAL INTEREST DISCOUNT ANALYSIS:
STEP 1: Identify co-ownership structure
   - Tenancy in common? (yes → fractional interest discount applicable)
   - Joint tenancy with survivorship? (no → §2040 analysis, not fractional discount)

STEP 2: Count co-owners
   - 2 co-owners: 20-30% discount
   - 3-5 co-owners: 25-35% discount
   - >5 co-owners: 30-40% discount

STEP 3: Classify property type
   - Raw land (easily divisible): Lower end of range (20-25%)
   - Improved property (hard to divide): Higher end of range (30-35%)
   - Mineral interests (cannot partition in kind): Moderate (25-30%)

STEP 4: Estimate partition costs
   - Attorney fees: $10K-$50K
   - Surveyor/engineer: $5K-$20K
   - Appraisal: $3K-$10K
   - Total as % of property value

STEP 5: Assess co-owner dynamics
   - Cooperative family: Lower discount
   - Adversarial or unknown co-owners: Higher discount

STEP 6: Research comparable sales
   - Find actual sales of fractional TIC interests (if available)
   - Best evidence, but rare

STEP 7: Select discount percentage
   - Conservative: 20-25% (2 co-owners, raw land, cooperative)
   - Moderate: 25-30% (3-5 co-owners, typical property)
   - Aggressive: 30-35% (>5 co-owners, improved property, adversarial)

STEP 8: Calculate discounted value
   - Pro rata value × (1 - Discount %)

STEP 9: Document in appraisal
   - Partition cost analysis
   - Number of co-owners
   - Property characteristics
   - Hypothetical buyer assumption (not family cooperation)

DEFENSIVE CHECKLIST:
□ Qualified real estate appraiser (MAI credential preferred)
□ Partition cost analysis included
□ Number of co-owners documented
□ Property type and partition feasibility analyzed
□ Comparable sales cited (if available)
□ Discount in 20-35% range (moderate)
□ Hypothetical buyer standard applied (not family)
        """,
        entity_scope="Undivided fractional interests in real property (tenancy in common)",
        confidence=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="Treas. Reg. §20.2031-1(b) + Estate of Pillsbury",
        issue_category=IssueCategory.DISCOUNT_APPLICABILITY,
        fact_fragility_score=0.5
    ),

]  # End DOCTRINE_CACHE


# ═══════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    """Retrieve doctrine block by exact topic match."""
    for block in DOCTRINE_CACHE:
        if block.topic == topic:
            return block
    return None


def search_doctrines_by_keyword(keyword: str) -> List[DoctrineBlock]:
    """Search doctrine cache by keyword (case-insensitive)."""
    keyword_lower = keyword.lower()
    matches = []
    for block in DOCTRINE_CACHE:
        if keyword_lower in block.topic.lower():
            matches.append(block)
            continue
        for kw in block.keywords:
            if keyword_lower in kw.lower():
                matches.append(block)
                break
    return matches


def get_doctrines_by_category(category: IssueCategory) -> List[DoctrineBlock]:
    """Retrieve all doctrine blocks for a given issue category."""
    return [block for block in DOCTRINE_CACHE if block.issue_category == category]


def get_high_confidence_doctrines() -> List[DoctrineBlock]:
    """Retrieve all DEFENSIBLE confidence doctrines (safest positions)."""
    return [block for block in DOCTRINE_CACHE if block.confidence == ConfidenceStratification.DEFENSIBLE]


def get_disclosure_required_doctrines() -> List[DoctrineBlock]:
    """Retrieve doctrines requiring disclosure (AGGRESSIVE, DISCLOSURE, HIGH_RISK)."""
    return [
        block for block in DOCTRINE_CACHE
        if block.confidence in [
            ConfidenceStratification.AGGRESSIVE,
            ConfidenceStratification.DISCLOSURE,
            ConfidenceStratification.HIGH_RISK
        ]
    ]
