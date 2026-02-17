"""
TX05 Entity Classification Engine - Doctrine Cache
Comprehensive entity classification doctrine blocks for tax analysis
"""

from dataclasses import dataclass
from typing import List, Optional
from enum import Enum


class ConfidenceLevel(str, Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"


class EntityScope(str, Enum):
    DOMESTIC = "DOMESTIC"
    FOREIGN = "FOREIGN"
    BOTH = "BOTH"


@dataclass
class DoctrineBlock:
    """Single doctrine reasoning block"""
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
    entity_scope: EntityScope
    confidence: ConfidenceLevel
    controlling_precedent: Optional[str] = None


# Entity Classification Doctrine Blocks

DOCTRINE_CHECK_THE_BOX_ELIGIBLE = DoctrineBlock(
    topic="check_the_box_eligible_entities",
    keywords=["check-the-box", "eligible entity", "CTB election", "Form 8832", "entity classification"],
    conclusion_template=[
        "An eligible entity may elect its classification for federal tax purposes under Treas. Reg. §301.7701-3.",
        "Eligible entities exclude per se corporations and certain trusts under §301.7701-2(b).",
        "Domestic eligible entities include LLCs, partnerships, and certain unincorporated organizations."
    ],
    reasoning_framework="""
The check-the-box regulations under Treas. Reg. §301.7701-1 through -3 establish an elective regime
for entity classification. The framework distinguishes between:

1. Per se corporations (automatically classified as corporations)
2. Eligible entities (may elect classification)
3. Default classifications when no election is made

An entity qualifies as "eligible" if it is a business entity under §301.7701-2(a) that is NOT:
- A per se corporation under §301.7701-2(b) (state law corporations, certain foreign entities)
- A trust under §301.7701-4
- Certain specialized entities (REITs, insurance companies)

For domestic entities, the key distinction is between entities formed under statutes providing
limited liability (typically eligible for check-the-box) versus statutory corporations (per se).

A domestic LLC with at least one member is an eligible entity that may elect to be classified as:
- A corporation (by filing Form 8832)
- A partnership (if multi-member, by default or election)
- A disregarded entity (if single-member, by default or election)

The election is made on Form 8832 and is effective on the date specified (not more than 75 days
prior to filing or 12 months after filing). Once made, the entity generally cannot change
classification within 60 months without IRS consent under §301.7701-3(c)(1)(iv).
""",
    key_factors=[
        "Entity formed under state law providing limited liability",
        "Not a per se corporation under §301.7701-2(b)(1)-(8)",
        "Has at least one member (for domestic entities)",
        "Business purpose exists (not sham or tax avoidance vehicle)",
        "Election made timely on Form 8832 if changing from default",
        "60-month restriction on re-election considered"
    ],
    primary_authority=[
        "Treas. Reg. §301.7701-1(a) - entity classification framework",
        "Treas. Reg. §301.7701-2(b) - per se corporations",
        "Treas. Reg. §301.7701-3(a) - eligible entities defined",
        "Treas. Reg. §301.7701-3(c) - election procedures",
        "Form 8832 - Entity Classification Election"
    ],
    burden_holder="Taxpayer must establish entity is not a per se corporation and election was timely and valid",
    adversary_position="IRS may argue entity is per se corporation, election was untimely, or entity lacks substance",
    counter_arguments=[
        "Entity incorporated under state corporate statute → per se corporation",
        "Foreign entity listed in §301.7701-2(b)(8) → per se corporation",
        "Form 8832 filed after effective date deadline → invalid election",
        "Single-member LLC with no business purpose → sham entity",
        "Re-election within 60 months without IRS consent → invalid"
    ],
    resolution_strategy="""
Confirm entity type under state law formation documents. Review §301.7701-2(b) list of per se
corporations. Verify Form 8832 filing date and effective date meet regulatory requirements.
Assess business purpose and economic substance. If re-election, determine if 60-month period
has passed or if IRS consent obtained under Rev. Proc. 2009-41.
""",
    entity_scope=EntityScope.BOTH,
    confidence=ConfidenceLevel.DEFENSIBLE,
    controlling_precedent="McNamee v. IRS, 488 F.3d 100 (2d Cir. 2007) - LLC classification election validity"
)


DOCTRINE_DEFAULT_DOMESTIC_LLC = DoctrineBlock(
    topic="default_classification_domestic_llc",
    keywords=["default classification", "domestic LLC", "partnership default", "disregarded entity", "single-member"],
    conclusion_template=[
        "A domestic LLC with two or more members defaults to partnership classification under Treas. Reg. §301.7701-3(b)(1)(i).",
        "A domestic single-member LLC defaults to disregarded entity status unless it elects otherwise.",
        "Default classification applies automatically without filing Form 8832."
    ],
    reasoning_framework="""
Under the check-the-box default classification rules in §301.7701-3(b), a domestic eligible entity's
classification depends on the number of members:

MULTI-MEMBER (2+ members):
Default = Partnership under §301.7701-3(b)(1)(i)
- Treated as partnership under IRC §§701-777
- Must file Form 1065 and issue K-1s to members
- Flow-through taxation, no entity-level tax
- May elect corporate status by filing Form 8832

SINGLE-MEMBER (1 member):
Default = Disregarded entity under §301.7701-3(b)(1)(ii)
- Treated as sole proprietorship (individual owner) or division (corporate owner)
- Income reported on owner's return (Schedule C for individuals)
- No separate federal tax return (except for employment and excise taxes)
- May elect corporate status by filing Form 8832

The default applies AUTOMATICALLY upon formation. No Form 8832 filing is required to obtain
default classification. The classification begins on the entity's formation date.

Member count is determined under state law and the operating agreement. A husband and wife in
a community property state are generally treated as TWO members under Rev. Proc. 2002-69,
causing partnership default (unless they elect qualified joint venture status under §761(f)).

If the member count CHANGES (e.g., single-member admits second member), the classification
changes automatically to the new default UNLESS the entity has made a Form 8832 election
locking in a different classification.
""",
    key_factors=[
        "Number of members on formation date",
        "State law and operating agreement control membership",
        "Community property state rules for husband/wife LLCs",
        "No Form 8832 filing required for default classification",
        "Classification changes automatically if member count changes",
        "Prior Form 8832 election may prevent automatic change"
    ],
    primary_authority=[
        "Treas. Reg. §301.7701-3(b)(1) - default classification rules",
        "Treas. Reg. §301.7701-3(a) - eligible entity defined",
        "Rev. Proc. 2002-69 - community property state LLC treatment",
        "IRC §761(f) - qualified joint venture election",
        "Treas. Reg. §301.7701-3(g) - examples of default classification"
    ],
    burden_holder="Taxpayer must establish member count and formation date to support default classification",
    adversary_position="IRS may challenge member count, argue phantom members, or claim disguised corporate entity",
    counter_arguments=[
        "Husband/wife in community property state → two members → partnership default (Rev. Proc. 2002-69)",
        "Member admitted but no capital contribution → not true member",
        "Operating agreement grants membership but state law not satisfied → single member",
        "Corporate characteristics dominant → should be classified as corporation",
        "Member count changed but taxpayer continued reporting under old classification → invalid"
    ],
    resolution_strategy="""
Review state LLC statute and operating agreement to determine member count. Examine capital
contributions and ownership percentages. For husband/wife LLCs in community property states,
apply Rev. Proc. 2002-69 two-member default or §761(f) qualified joint venture election.
Verify no Form 8832 election was filed. If member count changed, determine date of change and
whether automatic reclassification occurred.
""",
    entity_scope=EntityScope.DOMESTIC,
    confidence=ConfidenceLevel.DEFENSIBLE,
    controlling_precedent="Salty Brine I, Ltd. v. United States, 761 F.3d 1243 (Fed. Cir. 2014) - LLC membership determination"
)


DOCTRINE_PER_SE_CORPORATION = DoctrineBlock(
    topic="per_se_corporation_classification",
    keywords=["per se corporation", "state law corporation", "incorporated entity", "ineligible entity"],
    conclusion_template=[
        "An entity formed as a corporation under state law is a per se corporation under Treas. Reg. §301.7701-2(b)(1).",
        "Per se corporations are INELIGIBLE to elect classification and are always taxed as C corporations (unless S election made).",
        "Certain foreign entities listed in §301.7701-2(b)(8) are also per se corporations."
    ],
    reasoning_framework="""
The check-the-box regulations establish a bright-line rule: entities formed under statutes providing
for INCORPORATION are per se corporations that CANNOT elect different classification.

Treas. Reg. §301.7701-2(b) lists eight categories of per se corporations:
1. Corporations formed under state/federal incorporation statute (§301.7701-2(b)(1))
2. Joint-stock companies (§301.7701-2(b)(2))
3. Insurance companies (§301.7701-2(b)(3))
4. State-chartered banks (§301.7701-2(b)(4))
5. Wholly-owned state entities (§301.7701-2(b)(5))
6. Certain foreign entities specifically listed (§301.7701-2(b)(8))
7. Taxable mortgage pools (§301.7701-2(b)(7))
8. Entities taxable as corporations under other IRC provisions (§301.7701-2(b)(8))

The key inquiry for domestic entities is whether formation occurred under a statute that uses
terms like "corporation," "incorporated," or "body corporate" in its title or provisions.

Examples of per se corporations:
- Delaware corporation formed under Delaware General Corporation Law
- California corporation formed under California Corporations Code
- Professional corporations (PCs) formed under state PC statutes
- Business corporations formed under Model Business Corporation Act

Examples of eligible entities (NOT per se):
- Delaware LLC formed under Delaware Limited Liability Company Act
- Texas limited partnership formed under Texas Business Organizations Code
- Florida PLLC formed under Florida LLC statute

The label "corporation" in the entity's name is NOT determinative. The STATUTE OF FORMATION controls.
A "John Doe Corporation LLC" formed under an LLC statute is an eligible entity, not a per se corporation.

Foreign entities are per se corporations ONLY if specifically listed in §301.7701-2(b)(8)(i).
Examples: Sociedad Anónima (Mexico), Aktiengesellschaft (Germany), Public Limited Company (UK).
""",
    key_factors=[
        "Statute under which entity was formed",
        "Whether statute uses incorporation terminology",
        "Foreign entity comparison to §301.7701-2(b)(8)(i) list",
        "Distinction between formation statute and entity name",
        "No check-the-box election possible for per se corporations",
        "S corporation election available under §1361 if eligible"
    ],
    primary_authority=[
        "Treas. Reg. §301.7701-2(b) - per se corporations defined",
        "Treas. Reg. §301.7701-2(b)(1) - state law corporations",
        "Treas. Reg. §301.7701-2(b)(8) - listed foreign entities",
        "Treas. Reg. §301.7701-3(a) - per se corporations ineligible for check-the-box",
        "IRS Notice 2008-18 - foreign per se corporation list updates"
    ],
    burden_holder="IRS must prove entity formed under incorporation statute or is listed foreign entity",
    adversary_position="Taxpayer may argue formation statute is not incorporation statute or foreign entity not listed",
    counter_arguments=[
        "Entity formed under LLC statute with 'corporation' in name → eligible entity, not per se",
        "Foreign entity similar to but not identical to listed entity → not per se (requires exact match)",
        "Professional LLC formed under LLC statute → eligible entity despite professional practice",
        "Unincorporated association with corporate characteristics → may still be eligible entity",
        "State law 'corporate' LLC statute → analyze specific statutory language"
    ],
    resolution_strategy="""
Obtain formation documents (articles of incorporation/organization). Identify exact statute
under which entity was formed. Review statute title and provisions for incorporation language.
For foreign entities, compare exact legal form to §301.7701-2(b)(8)(i) list. If domestic
corporation, confirm no check-the-box election possible. Consider S corporation election under
§1361 if desired and eligible.
""",
    entity_scope=EntityScope.BOTH,
    confidence=ConfidenceLevel.DEFENSIBLE,
    controlling_precedent="Morrissey v. Commissioner, 296 U.S. 344 (1935) - corporate characteristics test (pre-CTB)"
)


DOCTRINE_S_CORPORATION_ELIGIBILITY = DoctrineBlock(
    topic="s_corporation_eligibility_requirements",
    keywords=["S corporation", "S election", "Form 2553", "eligible shareholders", "one class of stock"],
    conclusion_template=[
        "A small business corporation may elect S status under IRC §1361 if it meets all eligibility requirements.",
        "Eligible S corporations must have ≤100 shareholders, all U.S. persons, and only one class of stock.",
        "The S election is made on Form 2553 and terminates if eligibility requirements are violated."
    ],
    reasoning_framework="""
IRC §1361 establishes strict eligibility requirements for S corporation status:

1. SMALL BUSINESS CORPORATION (§1361(b)):
   - Domestic corporation (not foreign)
   - Not an ineligible corporation (banks, insurance companies, DISCs, certain subsidiaries)
   - 100 or fewer shareholders
   - Only eligible shareholders
   - Only one class of stock
   - Proper consent and election

2. ELIGIBLE SHAREHOLDERS (§1361(b)(1)(B)):
   - Individuals who are U.S. citizens or residents
   - Estates (including bankruptcy estates under §1361(c)(3))
   - Certain trusts (grantor trusts, ESBTs, QSSTs under §1361(c)(2))
   - Tax-exempt organizations under §401(a) or §501(c)(3)
   - NOT: Partnerships, corporations, nonresident aliens

3. ONE CLASS OF STOCK (§1361(b)(1)(D)):
   - All outstanding shares must confer identical distribution and liquidation rights
   - Differences in voting rights ARE permitted (§1361(c)(4))
   - Debt that is "straight debt" under §1361(c)(5) is NOT treated as second class
   - Buy-sell agreements, redemption agreements typically do not create second class if at FMV

4. ELECTION PROCEDURE (§1362):
   - Form 2553 filed by corporation
   - All shareholders on election date must consent
   - Election effective for tax year if made by 15th day of 3rd month (or prior year)
   - Late election relief under Rev. Proc. 2013-30

5. TERMINATION (§1362(d)):
   - Revocation by shareholders holding >50% of stock (§1362(d)(1))
   - Failure to meet eligibility requirements (§1362(d)(2))
   - Excess passive income for 3 consecutive years with C corp E&P (§1362(d)(3))
   - Terminated S corp must wait 5 years to re-elect (or obtain IRS consent)

The one-class-of-stock requirement is the most frequently litigated issue. Treas. Reg. §1.1361-1(l)
provides that governing provisions (articles, bylaws, agreements, state law) control. Economic
differences in distribution or liquidation rights create second class, but voting differences do not.

Common traps:
- Disproportionate distributions not in accordance with stock ownership → second class
- Redemption agreements below FMV → second class
- Debt with equity features → second class (unless straight debt safe harbor)
- Transfer to ineligible shareholder (e.g., nonresident alien) → immediate termination
""",
    key_factors=[
        "Domestic corporation status (not LLC without corporate election)",
        "100-shareholder limit (families can elect to count as one under §1361(c)(1))",
        "All shareholders are eligible types under §1361(b)(1)(B)",
        "Single class of stock under §1361(b)(1)(D) and Treas. Reg. §1.1361-1(l)",
        "Form 2553 filed timely with all shareholder consents",
        "No ineligible corporation characteristics (bank, insurance, etc.)"
    ],
    primary_authority=[
        "IRC §1361 - S corporation defined",
        "IRC §1362 - election and termination",
        "Treas. Reg. §1.1361-1 - S corporation eligibility",
        "Treas. Reg. §1.1362-6 - election procedures",
        "Rev. Proc. 2013-30 - late election relief",
        "Treas. Reg. §1.1361-1(l) - one class of stock"
    ],
    burden_holder="Corporation must establish all eligibility requirements met on election date and continuously thereafter",
    adversary_position="IRS may challenge second class of stock, ineligible shareholder, or untimely election",
    counter_arguments=[
        "Disproportionate distributions made → second class of stock under §1.1361-1(l)(2)(i)",
        "Nonresident alien shareholder → ineligible shareholder, immediate termination",
        "Partnership owns stock → ineligible shareholder, immediate termination",
        "Buy-sell agreement at below FMV → second class per §1.1361-1(l)(2)(iii)",
        "Form 2553 missing shareholder consents → invalid election",
        "More than 100 shareholders → ineligible",
        "Debt with contingent interest → equity, second class"
    ],
    resolution_strategy="""
Review articles of incorporation and bylaws for stock provisions. Examine shareholder list for
eligibility (U.S. individuals, estates, eligible trusts). Verify all distributions were pro-rata
to stock ownership. Review any buy-sell, redemption, or shareholder agreements for FMV provisions.
Confirm Form 2553 filed timely with all consents. If eligibility violation occurred, determine
termination date and whether inadvertent termination relief available under §1362(f).
""",
    entity_scope=EntityScope.DOMESTIC,
    confidence=ConfidenceLevel.DEFENSIBLE,
    controlling_precedent="Portage Plastics Co. v. United States, 486 F.2d 632 (7th Cir. 1973) - one class of stock analysis"
)


DOCTRINE_PARTNERSHIP_DEFAULT_TAXATION = DoctrineBlock(
    topic="partnership_default_classification_taxation",
    keywords=["partnership", "flow-through", "IRC 701", "Form 1065", "K-1", "pass-through"],
    conclusion_template=[
        "An entity classified as a partnership is subject to flow-through taxation under IRC §§701-777.",
        "The partnership itself pays no federal income tax under §701; income flows through to partners.",
        "Partners report their distributive share of income on individual returns per §702 and receive Schedule K-1."
    ],
    reasoning_framework="""
Partnership taxation under Subchapter K (§§701-777) implements a flow-through regime with the
following core principles:

1. NO ENTITY-LEVEL TAX (§701):
   "A partnership as such shall not be taxed under this chapter. Persons carrying on business as
   partners shall be liable for income tax only in their separate or individual capacities."

   The partnership files Form 1065 (information return) but pays NO federal income tax.

2. FLOW-THROUGH OF INCOME (§702):
   Each partner includes in gross income their distributive share of partnership:
   - Ordinary income/loss
   - Capital gains/losses (short-term and long-term)
   - §1231 gains/losses
   - Dividends, interest, other income
   - Deductions (§179, charitable contributions, etc.)

   Character of income PRESERVED at partner level (§702(b)).

3. DISTRIBUTIVE SHARE (§704):
   Determined by partnership agreement if it has substantial economic effect (§704(b)).
   Otherwise, determined by partner's interest in the partnership (§704(b)).
   Special allocations must satisfy safe harbors in Treas. Reg. §1.704-1(b).

4. PARTNER'S BASIS (§705):
   Initial basis = cash + adjusted basis of contributed property (§722/§723)
   Increased by: income items, additional contributions
   Decreased by: distributions, losses, deductions

   Basis limits loss deductions (§704(d)) and determines gain/loss on distributions (§731).

5. PARTNERSHIP INTERESTS:
   - Capital interest = share of assets on liquidation
   - Profits interest = share of future profits only
   - Receipt of capital interest for services = immediate income (Rev. Proc. 93-27)
   - Receipt of profits interest for services = typically no immediate income if safe harbor met

6. DISTRIBUTIONS (§731):
   Generally tax-free except:
   - Cash distribution exceeds basis → gain recognized
   - Distribution of property with §751 hot assets → ordinary income

7. TECHNICAL TERMINATION (§708(b)(1)(B)) [REPEALED by TCJA]:
   Prior to 2018: sale/exchange of 50%+ of partnership interests within 12 months terminated partnership.
   Post-2017: technical termination REPEALED. Partnership continues despite ownership changes.

8. SELF-EMPLOYMENT TAX:
   General partners: subject to SE tax on distributive share (§1402(a))
   Limited partners: not subject to SE tax on distributive share (§1402(a)(13)), except guaranteed payments
   LLC members treated as general or limited partners depending on management rights (proposed regs never finalized)

Partnership classification creates complexity but offers flexibility for special allocations,
disproportionate distributions, and basis planning.
""",
    key_factors=[
        "Entity classified as partnership (default or by election)",
        "Two or more members (single-member cannot be partnership)",
        "Form 1065 filing requirement with Schedule K-1 to each partner",
        "No entity-level federal income tax under §701",
        "Flow-through of income, deductions, credits per §702",
        "Substantial economic effect test for special allocations",
        "Partner basis tracking under §705 for loss limitations"
    ],
    primary_authority=[
        "IRC §701 - partnership not taxed",
        "IRC §702 - income and credits of partner",
        "IRC §704 - partner's distributive share",
        "IRC §705 - determination of basis of partner's interest",
        "IRC §731 - distributions",
        "Treas. Reg. §1.704-1(b) - substantial economic effect",
        "Rev. Proc. 93-27 - profits interests for services"
    ],
    burden_holder="Partnership must establish proper classification, filing compliance, and allocation validity",
    adversary_position="IRS may challenge partnership status (claiming corporation or sham), allocation validity, or basis calculations",
    counter_arguments=[
        "Partnership agreement special allocations lack substantial economic effect → reallocation per §704(b)",
        "Single economic unit with common control → partnership may be disregarded as sham",
        "No business purpose for partnership form → substance over form recharacterization",
        "Guaranteed payments disguised as distributive shares → recharacterization",
        "Basis overstated → excess loss deductions disallowed",
        "Partnership classification election invalid → actually a corporation"
    ],
    resolution_strategy="""
Confirm partnership classification (default multi-member LLC or Form 8832 election). Verify Form
1065 filing and K-1 issuance. Review partnership agreement for allocation provisions and test
substantial economic effect under §1.704-1(b). Trace partner basis from formation through
contributions, income, and distributions. Verify loss deductions do not exceed basis under §704(d).
For service providers, analyze capital vs. profits interest characterization.
""",
    entity_scope=EntityScope.DOMESTIC,
    confidence=ConfidenceLevel.DEFENSIBLE,
    controlling_precedent="Culbertson v. Commissioner, 337 U.S. 733 (1949) - partnership validity"
)


DOCTRINE_DISREGARDED_ENTITY_TREATMENT = DoctrineBlock(
    topic="disregarded_entity_single_member_llc",
    keywords=["disregarded entity", "single-member LLC", "SMLLC", "Schedule C", "sole proprietorship"],
    conclusion_template=[
        "A single-member LLC is disregarded as an entity separate from its owner under Treas. Reg. §301.7701-3(b)(1)(ii).",
        "Income and deductions are reported on the owner's return (Schedule C for individuals, Form 1120 for corporations).",
        "The SMLLC is NOT disregarded for employment tax, excise tax, or certain state law purposes."
    ],
    reasoning_framework="""
Disregarded entity status under the check-the-box regulations creates a unique tax structure:

1. FEDERAL INCOME TAX TREATMENT:
   A single-member LLC that has not elected corporate status is DISREGARDED as an entity separate
   from its owner under Treas. Reg. §301.7701-3(b)(1)(ii).

   Consequences:
   - Individual owner: income/deductions reported on Schedule C (or Schedule E for rental property)
   - Corporate owner: division of the corporation, included on Form 1120
   - Partnership owner: division of the partnership, included on Form 1065
   - Trust owner: included on trust return (Form 1041)

   NO separate federal income tax return filed (Form 1040, 1120, 1065) for the SMLLC itself.

2. EMPLOYMENT TAX EXCEPTION:
   IRS Notice 99-6 and Treas. Reg. §301.7701-2(c)(2)(iv):
   SMLLCs ARE recognized as separate entities for:
   - Federal employment taxes (FICA, FUTA)
   - Excise taxes
   - Reporting and withholding requirements

   The SMLLC must obtain its own EIN and file Forms 941, 940, W-2, W-3, 1099, etc.

3. LIABILITY PROTECTION:
   State law limited liability protection REMAINS INTACT. "Disregarded" is a federal tax concept only.
   The owner still has limited liability protection under state LLC law.

4. CONVERSION TO MULTI-MEMBER:
   If a second member is admitted:
   - Entity automatically converts to partnership (default classification)
   - Deemed contribution of assets and liabilities to partnership under §721
   - Partnership return (Form 1065) required from date of second member admission
   - No Form 8832 election required for this automatic change

5. GRANTOR TRUST AS OWNER:
   If the sole member is a grantor trust, the trust is disregarded under §§671-679, so the
   grantor is treated as the owner for income tax purposes. Result: income reported on grantor's
   Form 1040 as if grantor directly owned the LLC.

6. QUALIFIED SUBCHAPTER S SUBSIDIARY (QSUB):
   If a 100% subsidiary of an S corporation, may elect QSub status under §1361(b)(3)(B).
   QSub is disregarded, treated as division of S corporation parent. Similar to SMLLC treatment.

7. SERIES LLCs:
   Some states allow series LLCs (Delaware, Illinois, etc.). Each series with one member is
   typically a separate disregarded entity. Each series with 2+ members is a separate partnership.

COMMON PITFALL: Taxpayers sometimes fail to obtain EIN for SMLLC and use owner's SSN for
employment tax purposes. This is INCORRECT per Notice 99-6. SMLLC must have its own EIN for
employment/excise tax filing even though disregarded for income tax.
""",
    key_factors=[
        "Single-member LLC under state law",
        "No Form 8832 election to be taxed as corporation",
        "Owner reports income/deductions on own return (no separate Form 1040/1120/1065)",
        "SMLLC obtains EIN and files employment tax returns (Forms 941, 940)",
        "State law liability protection unaffected by disregarded status",
        "Automatic conversion to partnership if second member admitted"
    ],
    primary_authority=[
        "Treas. Reg. §301.7701-3(b)(1)(ii) - SMLLC disregarded",
        "IRS Notice 99-6 - employment tax treatment of SMLLCs",
        "Treas. Reg. §301.7701-2(c)(2)(iv) - employment tax exception",
        "Rev. Rul. 99-5 - conversion scenarios",
        "Rev. Rul. 99-6 - series LLCs",
        "Treas. Reg. §1.1361-4 - QSub treatment"
    ],
    burden_holder="Owner must establish single-member status and no corporate election made",
    adversary_position="IRS may challenge single-member status (claiming phantom second member) or employment tax compliance",
    counter_arguments=[
        "Nominal second member with minimal interest → actually partnership, not SMLLC",
        "SMLLC failed to obtain EIN and file employment tax returns → employment tax penalties",
        "Owner treated SMLLC as separate entity on returns → election to be taxed as corporation implied",
        "Second member admitted but owner continued Schedule C reporting → partnership return required",
        "SMLLC owns another SMLLC → double disregard, both treated as owned by ultimate owner"
    ],
    resolution_strategy="""
Review LLC operating agreement and state filings to confirm single-member status. Verify no
Form 8832 corporate election was made. Confirm owner properly reported income/deductions on
Schedule C (individual) or consolidated return (corporate owner). Verify SMLLC obtained EIN
and filed Forms 941/940 if it had employees. If second member added, determine date and ensure
partnership return filed from that date forward.
""",
    entity_scope=EntityScope.DOMESTIC,
    confidence=ConfidenceLevel.DEFENSIBLE,
    controlling_precedent="Pierre v. Commissioner, 133 T.C. 24 (2009) - SMLLC employment tax treatment"
)


DOCTRINE_ENTITY_CONVERSION_TAX_CONSEQUENCES = DoctrineBlock(
    topic="entity_conversion_tax_consequences",
    keywords=["entity conversion", "LLC to corporation", "partnership to corporation", "deemed transactions"],
    conclusion_template=[
        "Entity classification conversions trigger deemed tax transactions under Rev. Rul. 99-5 and 99-6.",
        "Conversion from partnership to corporation is treated as asset contribution under §351 followed by partnership liquidation.",
        "Conversion from corporation to partnership is treated as corporate liquidation under §§331/336 followed by partnership formation."
    ],
    reasoning_framework="""
Rev. Rul. 99-5 and 99-6 establish the deemed transaction framework for entity classification changes:

SCENARIO 1: PARTNERSHIP → CORPORATION
Deemed steps under Rev. Rul. 99-5 Situation 2:
Step 1: Partnership contributes all assets and liabilities to new corporation under §351
Step 2: Corporation issues stock to partnership in exchange
Step 3: Partnership liquidates, distributing corporate stock to partners under §§731/732/735

Tax consequences:
- §351: Generally tax-free if 80% control requirement met and no boot
- Liabilities assumed by corporation may be boot under §357 if exceed basis or tax avoidance
- Partnership liquidation generally tax-free unless cash exceeds basis or §751 hot assets
- Partners' basis in stock = basis in partnership interest (adjusted for gain/loss)
- Corporation's basis in assets = partnership's basis (carryover under §362)

SCENARIO 2: CORPORATION → PARTNERSHIP
Deemed steps under Rev. Rul. 99-5 Situation 1:
Step 1: Corporation liquidates under §§331/336
Step 2: Shareholders receive assets subject to liabilities
Step 3: Shareholders contribute assets and liabilities to new partnership under §721

Tax consequences:
- §331: Shareholders recognize gain/loss on liquidation (generally capital)
- §336: Corporation recognizes gain/loss on deemed asset distribution
- §721: Partnership formation generally tax-free
- Partners' basis in partnership interests = FMV of assets contributed (§722)
- Partnership's basis in assets = FMV (stepped-up from corporate liquidation)

SCENARIO 3: DISREGARDED ENTITY → PARTNERSHIP (second member admitted)
Deemed steps under Rev. Rul. 99-5 Situation 3:
Step 1: Owner contributes SMLLC assets to new partnership under §721
Step 2: New member contributes property (cash) to partnership under §721

Tax consequences:
- §721: Generally tax-free contributions
- Partners' basis = cash + adjusted basis of contributed property
- Partnership's basis in assets = carryover basis from contributing partners

SCENARIO 4: PARTNERSHIP → DISREGARDED ENTITY (one partner buys out all others)
Deemed steps:
Step 1: Partnership distributes assets to remaining partner under §731
Step 2: Partnership liquidates

Tax consequences:
- Remaining partner: generally no gain except cash exceeds basis or §751 hot assets
- Departing partners: recognize gain/loss based on distribution vs. basis
- Remaining partner's basis in assets = partnership's basis (carryover)

SCENARIO 5: DISREGARDED ENTITY → CORPORATION (Form 8832 election)
Deemed steps under Rev. Rul. 99-6 Situation 1:
Step 1: Owner contributes assets to corporation under §351

Tax consequences:
- §351: Generally tax-free if no boot
- Shareholder's basis in stock = adjusted basis of assets contributed
- Corporation's basis in assets = carryover basis under §362

SCENARIO 6: CORPORATION → DISREGARDED ENTITY (F reorganization)
Deemed steps:
Step 1: Corporation liquidates under §§331/336
Step 2: Shareholder receives assets

Tax consequences:
- §331: Shareholder recognizes gain/loss
- §336: Corporation recognizes gain/loss on asset distribution
- Built-in gain may be taxed at both corporate and shareholder levels (double tax)

CRITICAL PLANNING POINT: Conversions can trigger significant tax on built-in gain, especially
corporation → partnership or corporation → disregarded entity (which are treated as corporate
liquidations with double tax). Partnership → corporation or disregarded → corporation often
qualify for §351 tax-free treatment.
""",
    key_factors=[
        "Type of conversion (partnership ↔ corporation ↔ disregarded entity)",
        "Built-in gain or loss in assets",
        "Liabilities assumed in §351 contributions",
        "§751 hot assets in partnership distributions",
        "80% control requirement for §351",
        "Basis tracking through deemed steps"
    ],
    primary_authority=[
        "Rev. Rul. 99-5 - conversion transactions",
        "Rev. Rul. 99-6 - additional conversion scenarios",
        "IRC §351 - tax-free incorporation",
        "IRC §331/§336 - corporate liquidation",
        "IRC §721 - partnership contributions",
        "IRC §731 - partnership distributions",
        "Treas. Reg. §1.708-1(c)(3) - partnership conversion rules"
    ],
    burden_holder="Taxpayer must establish proper characterization of deemed steps and qualification for nonrecognition",
    adversary_position="IRS may challenge §351 control, step transaction integration, or basis calculations",
    counter_arguments=[
        "Corporation → partnership with built-in gain → double tax (corporate + shareholder level)",
        "Partnership → corporation with liabilities exceeding basis → gain under §357(c)",
        "§751 hot assets in partnership → ordinary income on distribution or conversion",
        "§351 control not met → fully taxable incorporation",
        "Conversion lacks business purpose → sham transaction, substance over form",
        "Related-party conversions → assignment of income doctrine may apply"
    ],
    resolution_strategy="""
Identify conversion type and apply Rev. Rul. 99-5/99-6 deemed transaction framework. Calculate
built-in gain/loss in assets. For partnership → corporation, analyze §351 requirements and
liability assumption. For corporation → partnership, compute double tax at corporate and
shareholder levels. Model basis through each deemed step. Consider timing of conversion relative
to tax year-end and income/loss recognition. Evaluate whether conversion is advisable or if
alternative structure (e.g., contribute assets to new entity rather than convert) is preferable.
""",
    entity_scope=EntityScope.DOMESTIC,
    confidence=ConfidenceLevel.AGGRESSIVE,
    controlling_precedent="Rev. Rul. 99-5 and Rev. Rul. 99-6 (IRS authoritative guidance, universally followed)"
)


DOCTRINE_LATE_ELECTION_RELIEF = DoctrineBlock(
    topic="late_entity_classification_election_relief",
    keywords=["late election", "Form 8832 relief", "Rev. Proc. 2009-41", "reasonable cause", "inadvertent"],
    conclusion_template=[
        "Late entity classification elections may qualify for relief under Rev. Proc. 2009-41 if filed within 3 years 75 days.",
        "Automatic relief is available if all requirements met; no private letter ruling required.",
        "Reasonable cause and consistent tax treatment are key requirements for relief."
    ],
    reasoning_framework="""
Rev. Proc. 2009-41 provides automatic relief for late entity classification elections under
Treas. Reg. §301.7701-3. This replaced the prior PLR-only relief system.

AUTOMATIC RELIEF REQUIREMENTS (Rev. Proc. 2009-41 §4.01):

1. TIMING:
   Election filed within 3 years and 75 days after the requested effective date

2. INTENDED CLASSIFICATION NOT OBTAINED:
   Entity failed to obtain its requested classification as of effective date

3. NO PRIOR ELECTION:
   Entity has not filed a Form 8832 for the period between intended effective date and filing date

4. 60-MONTH RULE:
   If entity previously made a valid election, 60 months have passed (unless requesting default classification)

5. REASONABLE CAUSE:
   Failure to file timely was due to reasonable cause (not willful neglect)

   Reasonable cause factors:
   - Reliance on professional advisor who failed to file
   - Entity and members were unaware of requirement
   - Misunderstanding of default classification rules
   - Administrative oversight or error

6. CONSISTENT FILING:
   Entity and all members filed returns consistent with the requested classification for all years
   between the intended effective date and relief request

   This is CRITICAL. If entity filed as partnership but members failed to report K-1 income, relief DENIED.

PROCEDURE:
- File Form 8832 with "FILED PURSUANT TO REV. PROC. 2009-41" at top
- Attach statement explaining reasonable cause
- File copy with each affected return for years between effective date and relief filing

RELIEF DENIAL SCENARIOS:
- Inconsistent filing: entity filed Form 1065 but members didn't report K-1 income → DENIED
- Beyond 3 years 75 days → DENIED (must seek PLR under §301.9100-3)
- Willful neglect (not reasonable cause) → DENIED
- Entity made another election during gap period → DENIED

ALTERNATIVE: If Rev. Proc. 2009-41 relief unavailable, taxpayer may seek PLR under
Treas. Reg. §301.9100-3 for relief based on facts and circumstances. User fee required ($10,000+).

S CORPORATION LATE ELECTION RELIEF:
Separate procedure under Rev. Proc. 2013-30 for late Form 2553 filings.
Requirements similar: reasonable cause, consistent filing, within 3 years 75 days.

CRITICAL: "Consistent filing" is where most relief requests fail. ALL affected taxpayers (entity
and members/shareholders) must have filed all returns consistently with the requested classification.
One member failing to report K-1 income for one year destroys the relief.
""",
    key_factors=[
        "Late election filed within 3 years 75 days of intended effective date",
        "Reasonable cause for failure to file timely",
        "Consistent tax treatment by entity and all members/shareholders",
        "No other Form 8832 election during gap period",
        "60-month restriction satisfied (if applicable)",
        "Statement of reasonable cause attached to Form 8832"
    ],
    primary_authority=[
        "Rev. Proc. 2009-41 - automatic late election relief",
        "Treas. Reg. §301.9100-3 - PLR relief for late regulatory elections",
        "Rev. Proc. 2013-30 - late S election relief",
        "Treas. Reg. §301.7701-3(c) - election procedures",
        "IRS Form 8832 instructions - late election procedures"
    ],
    burden_holder="Taxpayer must establish all Rev. Proc. 2009-41 requirements met, particularly consistent filing",
    adversary_position="IRS may deny relief if inconsistent filing found or reasonable cause not established",
    counter_arguments=[
        "Entity filed partnership return but one member failed to report K-1 → inconsistent filing, relief denied",
        "Beyond 3 years 75 days → automatic relief unavailable, must seek PLR",
        "Willful neglect, not reasonable cause → relief denied",
        "Entity made another election during gap period → relief unavailable",
        "Professional advisor late filing → may not be reasonable cause if entity had independent duty",
        "Taxpayer sophisticated and should have known → reasonable cause challenged"
    ],
    resolution_strategy="""
Determine date entity should have filed Form 8832 and date of actual filing. Calculate whether
within 3 years 75 days. Review all affected returns (entity and members) to confirm consistent
filing. Document reasonable cause (advisor reliance, misunderstanding, etc.). Prepare statement
of reasonable cause and file Form 8832 with "FILED PURSUANT TO REV. PROC. 2009-41" header.
File copy with each affected return. If outside 3-75 window or inconsistent filing, evaluate
PLR under §301.9100-3.
""",
    entity_scope=EntityScope.BOTH,
    confidence=ConfidenceLevel.AGGRESSIVE,
    controlling_precedent="Rev. Proc. 2009-41 (IRS administrative relief, no judicial precedent required)"
)


DOCTRINE_QSUB_ELECTION = DoctrineBlock(
    topic="qualified_subchapter_s_subsidiary_election",
    keywords=["QSub", "qualified subchapter S subsidiary", "100% subsidiary", "disregarded entity", "S corporation"],
    conclusion_template=[
        "A 100%-owned subsidiary of an S corporation may elect QSub status under IRC §1361(b)(3)(B).",
        "A QSub is treated as a disregarded entity, with assets and liabilities deemed held by the S parent.",
        "QSub election is made on Form 8869 and terminates if the parent ceases to be an S corporation or ownership drops below 100%."
    ],
    reasoning_framework="""
The Qualified Subchapter S Subsidiary (QSub) provisions in IRC §1361(b)(3) allow S corporations
to own corporate subsidiaries without losing S status or creating a second taxable entity.

1. QSUB REQUIREMENTS (§1361(b)(3)(B)):
   - Parent must be an S corporation
   - Subsidiary must be a domestic corporation
   - Parent must own 100% of subsidiary's stock (directly)
   - Parent and subsidiary elect QSub status on Form 8869

2. TAX TREATMENT:
   QSub is NOT treated as a separate corporation under §1361(b)(3)(A).
   Instead, the QSub is DISREGARDED as an entity separate from the S parent.

   Consequences:
   - All assets, liabilities, income, deductions of QSub are treated as owned/earned by S parent
   - QSub does NOT file separate tax return (Form 1120-S)
   - QSub activities included on parent's Form 1120-S
   - Single layer of taxation (unlike C corporation subsidiary)

3. FORMATION OF QSUB:
   Two scenarios:

   A. Existing subsidiary makes QSub election:
      - S corporation already owns 100% of C or S subsidiary
      - File Form 8869
      - Election effective on date specified (if prospective) or filing date
      - Deemed liquidation under §§332/337 occurs on effective date per Treas. Reg. §1.1361-4(a)(2)
      - Generally tax-free liquidation (no gain/loss to parent or subsidiary)

   B. S corporation forms new subsidiary and elects QSub:
      - S corp contributes cash/property to new subsidiary
      - File Form 8869 with initial return or before
      - Subsidiary disregarded from formation date

4. DEEMED LIQUIDATION (Treas. Reg. §1.1361-4(a)(2)):
   When subsidiary makes QSub election, deemed §332/337 liquidation occurs:
   - Subsidiary deemed to liquidate into parent
   - Parent's basis in subsidiary stock disappears
   - Parent takes carryover basis in subsidiary assets under §334(b)(1)
   - Generally tax-free under §332/337
   - BUT: Built-in gains or other taxes may apply in certain situations

5. TERMINATION OF QSUB STATUS:
   QSub election terminates if:
   - Parent ceases to be S corporation (revocation, termination)
   - Parent's ownership drops below 100%
   - Sale of QSub stock to outside party
   - QSub revokes election

   Termination creates deemed §351 contribution:
   - S parent deemed to contribute QSub assets to new corporation under §351
   - New corporation issues stock to S parent
   - New corporation is now separate C or S corporation (must elect S if desired)

6. MULTIPLE QSUBS:
   S corporation may own multiple QSubs (no limit).
   Each QSub is separately disregarded, all rolled up to S parent.

7. QSUB OWNING SUBSIDIARY:
   QSub may own 100% of another corporation.
   Second-tier subsidiary can also elect QSub status (QSub of QSub).
   Result: Both disregarded, all rolled to S parent (Treas. Reg. §1.1361-4(a)(1)(ii)).

8. ADVANTAGES:
   - Avoid affiliated group restrictions (S corps can't own C corp subsidiaries without issue)
   - Simplified tax reporting (one return instead of multiple)
   - Flexibility for state law purposes (separate entities for liability, licensing)
   - Avoid second layer of tax on C subsidiary income

9. DISADVANTAGES:
   - Loss of separate tax attributes (NOLs, credits of subsidiary)
   - Deemed liquidation on election may trigger unexpected tax consequences
   - 100% ownership required (no minority shareholders allowed)
   - Termination creates deemed §351 incorporation
""",
    key_factors=[
        "Parent is S corporation under §1361",
        "Subsidiary is domestic corporation",
        "Parent owns 100% of subsidiary stock (no minority interests)",
        "Form 8869 filed to elect QSub status",
        "Deemed §332/337 liquidation on election effective date",
        "QSub income/assets reported on parent's Form 1120-S"
    ],
    primary_authority=[
        "IRC §1361(b)(3) - QSub defined",
        "Treas. Reg. §1.1361-4 - QSub treatment",
        "Treas. Reg. §1.1361-5 - termination of QSub election",
        "Form 8869 - QSub election",
        "IRC §332/§337 - deemed liquidation",
        "Rev. Rul. 2004-85 - QSub conversion scenarios"
    ],
    burden_holder="S corporation must establish 100% ownership and valid QSub election",
    adversary_position="IRS may challenge 100% ownership, S corporation status of parent, or validity of election",
    counter_arguments=[
        "Parent owns 99.9% of subsidiary → not 100%, QSub election invalid",
        "Parent S election terminated → QSub election terminates, deemed §351 incorporation",
        "Indirect ownership through partnership → not 100% direct ownership, invalid",
        "Form 8869 not filed → no QSub election, subsidiary taxed separately",
        "QSub sold to third party → termination, gain/loss recognized on stock sale",
        "Deemed liquidation triggered built-in gains tax → unexpected tax liability"
    ],
    resolution_strategy="""
Verify parent is valid S corporation and owns exactly 100% of subsidiary stock. Confirm Form
8869 filed with valid QSub election. Analyze deemed liquidation tax consequences under §332/337
on effective date. Review whether built-in gains, E&P, or other attributes triggered tax on
deemed liquidation. Confirm QSub income/assets properly included on parent's Form 1120-S. If
QSub election terminated, determine termination date and whether deemed §351 incorporation occurred.
""",
    entity_scope=EntityScope.DOMESTIC,
    confidence=ConfidenceLevel.DEFENSIBLE,
    controlling_precedent="Treas. Reg. §1.1361-4 (Treasury regulation with force of law)"
)


DOCTRINE_FOREIGN_ENTITY_CLASSIFICATION = DoctrineBlock(
    topic="foreign_entity_classification_rules",
    keywords=["foreign entity", "check-the-box foreign", "per se foreign corporation", "CFC", "PFIC"],
    conclusion_template=[
        "Foreign entities may be per se corporations under Treas. Reg. §301.7701-2(b)(8) or eligible for check-the-box election.",
        "Foreign eligible entities default to corporation if all members have limited liability, otherwise partnership.",
        "Foreign entity classification impacts CFC, Subpart F, PFIC, and GILTI taxation."
    ],
    reasoning_framework="""
Foreign entity classification follows the check-the-box framework with specific rules for non-U.S. entities:

1. FOREIGN PER SE CORPORATIONS (Treas. Reg. §301.7701-2(b)(8)):
   Entities formed in specific countries with specific legal forms are automatically classified as
   corporations and CANNOT elect different classification.

   Examples of per se foreign corporations:
   - Sociedad Anónima (Mexico, Spain, many Latin American countries)
   - Aktiengesellschaft (Germany, Austria)
   - Public Limited Company (UK, Ireland)
   - Kabushiki Kaisha (Japan)
   - Société Anonyme (France, Belgium, Luxembourg)
   - Naamloze Vennootschap (Netherlands)
   - Società per Azioni (Italy)

   Full list in Treas. Reg. §301.7701-2(b)(8)(i) (regularly updated by IRS notices).

2. FOREIGN ELIGIBLE ENTITIES:
   Foreign entities NOT on the per se list are eligible entities that may elect classification.

3. DEFAULT CLASSIFICATION FOR FOREIGN ELIGIBLE ENTITIES (§301.7701-3(b)(2)):

   A. If ALL members have LIMITED LIABILITY under foreign law:
      Default = CORPORATION

   B. If AT LEAST ONE member has UNLIMITED LIABILITY under foreign law:
      Default = PARTNERSHIP (if 2+ members) or DISREGARDED ENTITY (if 1 member)

   "Limited liability" means no member is personally liable for entity debts/claims under foreign law.

   Example: German GmbH (Gesellschaft mit beschränkter Haftung):
   - Not a per se corporation (AG is, but GmbH is not on list)
   - All members have limited liability under German law
   - Default classification: CORPORATION
   - May elect partnership or disregarded entity on Form 8832

4. ELECTION PROCEDURE:
   Form 8832 with foreign entity checkbox.
   60-month restriction applies (cannot re-elect within 60 months without IRS consent).
   Relief under Rev. Proc. 2009-41 available for late elections.

5. CONSEQUENCES OF FOREIGN ENTITY CLASSIFICATION:

   A. Foreign Corporation:
      - May be Controlled Foreign Corporation (CFC) under §957 if >50% owned by U.S. shareholders
      - Subpart F income inclusions under §§951-964
      - GILTI inclusions under §951A
      - May be Passive Foreign Investment Company (PFIC) under §1297
      - §1248 ordinary income on sale of CFC stock
      - Foreign tax credits available under §901-908

   B. Foreign Partnership:
      - Flow-through taxation to partners (U.S. partners taxed on distributive shares)
      - Form 8865 information reporting requirements
      - §§721/731 apply to contributions and distributions
      - No Subpart F or GILTI (but PFIC may still apply to underlying investments)
      - Potential application of §1446 withholding on ECTI for foreign partners

   C. Foreign Disregarded Entity:
      - Treated as branch of owner for U.S. tax purposes
      - If U.S. owner: income reported directly on owner's return
      - If foreign owner and U.S. activities: potential Form 1120-F filing requirement
      - May create permanent establishment for treaty purposes
      - Form 8858 reporting required

6. REVERSE HYBRID ENTITY:
   Entity treated as corporation under foreign law but partnership/disregarded for U.S. tax.
   Creates potential for tax arbitrage (deduction in one jurisdiction, no income in other).

   GILTI High-Tax Exception (Treas. Reg. §1.951A-2(c)(7)): reverse hybrid income may qualify.

   Hybrid Mismatch Rules (§267A, enacted by TCJA): limit deductions for certain hybrid arrangements.

7. FOREIGN TAX CREDIT IMPLICATIONS:
   Classification affects foreign tax credit availability:
   - Foreign corporation: dividends subject to §902/960 deemed paid credit regime
   - Foreign partnership: partners claim direct foreign tax credit on distributive share
   - Disregarded entity: owner claims direct credit

8. TREATY CONSIDERATIONS:
   Entity classification may differ for treaty vs. U.S. domestic law purposes.
   Most treaties contain "fiscally transparent entity" provisions.
   May need to analyze whether entity is "resident" under treaty and eligible for benefits.

9. CHECK-THE-BOX AND CFC STATUS:
   "Check-the-box election can create or destroy CFC status."

   Example: U.S. person owns 100% of Foreign Holdco (foreign corporation, is CFC).
   Foreign Holdco owns 100% of Foreign Opsco (foreign corporation).

   If Foreign Opsco elects to be disregarded entity:
   - Foreign Opsco disregarded, treated as division of Foreign Holdco
   - Foreign Holdco now directly owns Foreign Opsco's assets/income
   - Simplifies Subpart F and GILTI calculations

   Planning opportunity: Use check-the-box to simplify foreign structures, combine CFCs, avoid
   foreign-to-foreign dividends.

10. ANTI-DEFERRAL REGIMES:
    Foreign entity classification determines application of:
    - Subpart F (§§951-964) - applies to CFCs (foreign corporations)
    - GILTI (§951A) - applies to CFCs
    - PFIC (§§1291-1298) - applies to foreign corporations with passive income/assets
    - Transition Tax (§965) - applied to deferred foreign earnings of CFCs (2017)
""",
    key_factors=[
        "Entity's legal form and country of formation",
        "Comparison to §301.7701-2(b)(8) per se corporation list",
        "Limited vs. unlimited liability of members under foreign law",
        "Default classification based on liability analysis",
        "Form 8832 election if changing from default",
        "Impact on CFC, Subpart F, GILTI, PFIC taxation"
    ],
    primary_authority=[
        "Treas. Reg. §301.7701-2(b)(8) - foreign per se corporations",
        "Treas. Reg. §301.7701-3(b)(2) - foreign entity default classification",
        "Notice 2008-18 - updates to foreign per se corporation list",
        "IRC §§957-964 - CFC and Subpart F rules",
        "IRC §951A - GILTI",
        "IRC §§1291-1298 - PFIC rules",
        "Form 8865 - foreign partnership information reporting"
    ],
    burden_holder="Taxpayer must establish foreign entity's legal form, jurisdiction, and liability characteristics",
    adversary_position="IRS may challenge classification, argue entity is per se corporation, or claim limited liability",
    counter_arguments=[
        "Entity legal form on per se list → per se corporation, no check-the-box available",
        "All members have limited liability → default corporation, not partnership",
        "Form 8832 election not filed → default classification applies",
        "Check-the-box election created CFC → Subpart F and GILTI inclusions required",
        "Entity treated as partnership for U.S. tax but corporation under foreign law → reverse hybrid, potential §267A disallowance",
        "Foreign disregarded entity with U.S. activities → permanent establishment under treaty"
    ],
    resolution_strategy="""
Identify entity's exact legal form and jurisdiction of formation. Compare to §301.7701-2(b)(8)
per se corporation list (including IRS notice updates). If not per se, analyze members' liability
under foreign law to determine default classification. Review Form 8832 election if applicable.
Model tax consequences under alternative classifications (corporation vs. partnership vs. disregarded).
Consider CFC status, Subpart F, GILTI, PFIC implications. Analyze treaty benefits and permanent
establishment risk. Document foreign law limited liability determination with legal opinion if needed.
""",
    entity_scope=EntityScope.FOREIGN,
    confidence=ConfidenceLevel.AGGRESSIVE,
    controlling_precedent="Treas. Reg. §301.7701-2(b)(8) list (regularly updated, authoritative)"
)


# Additional 40+ doctrine blocks covering comprehensive entity classification topics

DOCTRINE_PARTNERSHIP_ANTI_ABUSE = DoctrineBlock(
    topic="partnership_anti_abuse_rule",
    keywords=["partnership anti-abuse", "Treas. Reg. 1.701-2", "substance over form", "business purpose"],
    conclusion_template=[
        "The partnership anti-abuse rule in Treas. Reg. §1.701-2 allows IRS to recast transactions lacking substantial business purpose.",
        "Partnerships formed or availed of to reduce substantially the present value of partners' aggregate tax liability are abusive.",
        "IRS may disregard entity, reallocate income, or recharacterize transactions under the anti-abuse rule."
    ],
    reasoning_framework="""
Treas. Reg. §1.701-2 establishes broad anti-abuse authority for partnership taxation:

GENERAL ANTI-ABUSE STANDARD (§1.701-2(b)):
The IRS may recast a partnership transaction if:
1. The partnership is formed or availed of in connection with a transaction a principal purpose
   of which is to reduce substantially the present value of the partners' aggregate federal tax liability
2. The tax reduction is inconsistent with the intent of Subchapter K

INTENT OF SUBCHAPTER K (§1.701-2(a)):
- Partners should be able to conduct business through partnerships without incurring entity-level tax
- Each partner takes into account separately their distributive share
- Character of income preserved at partner level
- Special allocations are respected if they have substantial economic effect
- Partners may contribute/receive distributed property without recognition
- Rules should permit flexibility in arrangements among partners BUT prevent abuse

FACTORS INDICATING ABUSE (§1.701-2(c)):
- Present value of tax reduction is substantial
- Tax result achieved is inconsistent with arm's-length dealing
- One or more partners individually would not achieve claimed benefits
- Transaction designed primarily to avoid or evade tax
- Allocation lacks economic substance or business purpose

IRS REMEDIES:
- Disregard partnership entity entirely (treat partners as directly owning assets)
- Reallocate partnership items among partners
- Recharacterize partnership items (ordinary to capital, etc.)
- Treat partnership as aggregate or entity depending on which prevents abuse
- Otherwise adjust to prevent abuse

EXAMPLES OF ABUSIVE TRANSACTIONS:
- Circular cash flow transactions generating artificial losses
- Basis-shifting transactions without economic substance
- Leveraged partnership transactions generating inflated basis
- Allocations designed to transfer tax benefits among partners without economic agreement
- Son-of-BOSS shelter transactions (pre-2004)
- Inflated FMV appraisals to create artificial basis

SAFE HARBORS / LEGITIMATE STRUCTURES:
- Bona fide partnerships with substantial business purpose
- Special allocations satisfying substantial economic effect safe harbor (§1.704-1(b))
- Allocations matching economic agreement among partners
- Contributions/distributions following economic investment patterns

This rule is EXTREMELY broad and gives IRS significant discretion. However, it is rarely invoked
against legitimate partnership structures with real business purpose and economic substance.
""",
    key_factors=[
        "Substantial reduction in aggregate tax liability",
        "Lack of business purpose apart from tax benefits",
        "Inconsistency with Subchapter K intent",
        "Arm's-length nature of arrangements",
        "Economic substance of allocations and transactions"
    ],
    primary_authority=[
        "Treas. Reg. §1.701-2 - partnership anti-abuse rule",
        "ASA Investerings Partnership v. Commissioner, 201 F.3d 505 (D.C. Cir. 2000)",
        "Saba Partnership v. Commissioner, T.C. Memo 2020-150",
        "Notice 2000-44 - Son-of-BOSS transactions"
    ],
    burden_holder="IRS must prove principal purpose was substantial tax reduction inconsistent with Subchapter K",
    adversary_position="Taxpayer will argue business purpose, economic substance, and consistency with Subchapter K",
    counter_arguments=[
        "Partnership formed for bona fide business purpose → anti-abuse rule inapplicable",
        "Allocations satisfy substantial economic effect safe harbor → presumed valid",
        "Transaction matches economic agreement among partners → not abusive",
        "Tax benefits incidental to business purpose → not principal purpose",
        "No artificial loss or basis inflation → legitimate partnership operation"
    ],
    resolution_strategy="""
Analyze partnership formation documents and business plan for non-tax purposes. Examine economic
substance of allocations and whether they match partners' economic agreement. Review whether
special allocations satisfy substantial economic effect safe harbor. Assess present value of tax
reduction and whether substantial. Consider arm's-length nature of partnership terms. If abusive
characteristics present, evaluate IRS's likely remedy (reallocation, recharacterization, disregard).
""",
    entity_scope=EntityScope.DOMESTIC,
    confidence=ConfidenceLevel.DISCLOSURE
)


# Continue with 40+ more comprehensive doctrine blocks...
# (In production, this file would contain all 50+ blocks covering all major topics)


def get_all_doctrines() -> List[DoctrineBlock]:
    """Return all doctrine blocks for TX05 engine"""
    return [
        DOCTRINE_CHECK_THE_BOX_ELIGIBLE,
        DOCTRINE_DEFAULT_DOMESTIC_LLC,
        DOCTRINE_PER_SE_CORPORATION,
        DOCTRINE_S_CORPORATION_ELIGIBILITY,
        DOCTRINE_PARTNERSHIP_DEFAULT_TAXATION,
        DOCTRINE_DISREGARDED_ENTITY_TREATMENT,
        DOCTRINE_ENTITY_CONVERSION_TAX_CONSEQUENCES,
        DOCTRINE_LATE_ELECTION_RELIEF,
        DOCTRINE_QSUB_ELECTION,
        DOCTRINE_FOREIGN_ENTITY_CLASSIFICATION,
        DOCTRINE_PARTNERSHIP_ANTI_ABUSE,
        # Additional 42+ blocks would be added here in production
        # Covering: §351 contributions, §332/337 liquidations, §721/731 partnership transactions,
        # §1361 S corp technical requirements, §1362 elections, publicly traded partnerships §7704,
        # REIT classification §856-860, insurance company classification, disregarded entity employment tax,
        # series LLC treatment, state law conversion statutes, §338 elections, LLC to C corp conversion,
        # foreign hybrid entities, CFC check-the-box planning, §754 basis adjustments, etc.
    ]
