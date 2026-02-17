"""
TX10 State Nexus Engine - Doctrine Cache
50+ pre-compiled expert nexus reasoning blocks
"""

from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum


class IssueCategory(str, Enum):
    CONSTITUTIONAL_NEXUS = "constitutional_nexus"
    ECONOMIC_NEXUS = "economic_nexus"
    PL_86_272_PROTECTION = "pl_86_272_protection"
    ATTRIBUTION_NEXUS = "attribution_nexus"
    APPORTIONMENT = "apportionment"
    SOURCING_RULES = "sourcing_rules"
    COMBINED_REPORTING = "combined_reporting"
    MARKETPLACE_FACILITATOR = "marketplace_facilitator"
    TEXAS_FRANCHISE_TAX = "texas_franchise_tax"
    SALT_CAP_PLANNING = "salt_cap_planning"
    DORMANT_COMMERCE_CLAUSE = "dormant_commerce_clause"
    FACTOR_PRESENCE = "factor_presence"


class ConfidenceLevel(str, Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"


@dataclass
class DoctrineBlock:
    topic: str
    category: IssueCategory
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
    confidence: ConfidenceLevel
    controlling_precedent: Optional[str] = None
    state_specific_notes: Optional[str] = None
    effective_date: Optional[str] = None


DOCTRINE_CACHE: List[DoctrineBlock] = [

    DoctrineBlock(
        topic="complete_auto_four_prong_test",
        category=IssueCategory.CONSTITUTIONAL_NEXUS,
        keywords=["complete auto", "substantial nexus", "commerce clause", "fair apportionment", "discrimination", "fair relation"],
        conclusion_template=[
            "A state tax satisfies constitutional requirements under Complete Auto Transit if it (1) applies to an activity with substantial nexus with the taxing state, (2) is fairly apportioned, (3) does not discriminate against interstate commerce, and (4) is fairly related to services provided by the state.",
            "Physical presence is no longer required for substantial nexus after Wayfair, but the tax must still satisfy all four Complete Auto prongs.",
            "The taxpayer bears the burden of proving constitutional invalidity under any of the four prongs."
        ],
        reasoning_framework="""
Complete Auto Transit, Inc. v. Brady, 430 U.S. 274 (1977) established the foundational four-part test for state tax constitutionality under the Commerce Clause:

PRONG 1 - SUBSTANTIAL NEXUS:
Originally interpreted to require physical presence (Quill Corp. v. North Dakota, 504 U.S. 298 (1992)), but Wayfair overruled Quill's physical presence requirement. Substantial nexus now assessed based on economic and virtual contacts. The state must demonstrate purposeful direction of business activities toward the state, sufficient to invoke the benefits and protections of state law.

PRONG 2 - FAIR APPORTIONMENT:
Two components: (a) internal consistency (tax structure, if applied by every state, would not result in multiple taxation of same income), and (b) external consistency (apportionment formula actually reflects reasonable sense of how income is generated). Container Corp. v. Franchise Tax Board, 463 U.S. 159 (1983).

PRONG 3 - NO DISCRIMINATION:
Tax cannot facially discriminate against interstate commerce or be discriminatory in effect. Differential treatment of in-state vs out-of-state commerce is subject to strict scrutiny. Comptroller of Treasury v. Wynne, 575 U.S. 542 (2015) (internal consistency test for discrimination).

PRONG 4 - FAIR RELATION TO STATE SERVICES:
Tax must be reasonably related to the extent of taxpayer's contact with the state and the benefits received. This prong has rarely invalidated taxes in modern jurisprudence.

POST-WAYFAIR ANALYSIS:
South Dakota v. Wayfair, 138 S. Ct. 2080 (2018) specifically upheld South Dakota's economic nexus statute because it:
- Had safe harbor ($100K sales OR 200 transactions)
- Was not retroactive
- South Dakota is member of Streamlined Sales Tax Agreement
- No obligation to remit tax on past sales

Courts now analyze the "quantity and quality" of contacts, considering:
- Dollar volume of sales
- Number of transactions
- Purposeful availment of state markets
- Systematic and continuous contacts
- Use of state infrastructure (delivery systems, payment processors)
""",
        key_factors=[
            "Physical presence no longer required after Wayfair (2018)",
            "Economic nexus thresholds vary by state ($100K-$500K common)",
            "Transaction count thresholds (100-200 transactions common)",
            "Fair apportionment requires internal and external consistency",
            "Discrimination analysis includes facial and effect-based review",
            "Retroactive application of economic nexus may violate Due Process",
            "Safe harbor provisions weigh in favor of constitutionality",
            "Marketplace facilitator collection reduces compliance burden"
        ],
        primary_authority=[
            "Complete Auto Transit, Inc. v. Brady, 430 U.S. 274 (1977)",
            "South Dakota v. Wayfair, Inc., 138 S. Ct. 2080 (2018)",
            "Quill Corp. v. North Dakota, 504 U.S. 298 (1992) [overruled on Commerce Clause]",
            "Container Corp. v. Franchise Tax Board, 463 U.S. 159 (1983)",
            "Comptroller of Treasury v. Wynne, 575 U.S. 542 (2015)",
            "National Bellas Hess, Inc. v. Department of Revenue, 386 U.S. 753 (1967)"
        ],
        burden_holder="Taxpayer challenging constitutionality",
        adversary_position="State will argue economic contacts are substantial, tax is fairly apportioned under internal/external consistency tests, no discrimination exists, and safe harbors demonstrate reasonableness",
        counter_arguments=[
            "Physical presence should still matter for non-sales taxes (income/franchise)",
            "De minimis contacts should not establish nexus",
            "Compliance burden on small businesses is discriminatory effect",
            "Economic nexus may violate Due Process for lack of minimum contacts",
            "Retroactive application violates fair notice requirements"
        ],
        resolution_strategy="Apply Complete Auto test sequentially. For substantial nexus post-Wayfair, assess economic contacts (sales volume, transaction count, systematic solicitation). For fair apportionment, apply internal consistency test (would formula if universally applied result in multiple taxation?) and external consistency (does formula reasonably reflect income generation?). Discrimination analysis examines facial classifications and disparate effects. Document state safe harbors and prospective-only application.",
        entity_scope="All entities subject to state taxation",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="South Dakota v. Wayfair, Inc., 138 S. Ct. 2080 (2018)"
    ),

    DoctrineBlock(
        topic="wayfair_economic_nexus_standards",
        category=IssueCategory.ECONOMIC_NEXUS,
        keywords=["wayfair", "economic nexus", "sales threshold", "transaction threshold", "$100k", "200 transactions", "remote seller"],
        conclusion_template=[
            "After Wayfair (2018), states may impose sales/use tax collection obligations on remote sellers without physical presence if economic contacts exceed statutory thresholds.",
            "Most states adopted thresholds of $100,000 in sales OR 200+ transactions annually; some states use higher thresholds or sales-only tests.",
            "Economic nexus statutes prospectively applied with safe harbors are more likely to withstand constitutional challenge."
        ],
        reasoning_framework="""
WAYFAIR HOLDING:
South Dakota v. Wayfair, Inc., 138 S. Ct. 2080 (2018) overruled Quill's physical presence requirement for sales tax nexus. The Court held:
1. Physical presence rule is "unsound and incorrect" - creates "arbitrary, formalistic distinction"
2. Modern e-commerce has "magnified the revenue shortfall" from physical presence rule
3. South Dakota's law is constitutional because it includes protections against undue burden

SOUTH DAKOTA SAFE HARBORS (SD Codified Laws § 10-64-2):
- Safe harbor: no obligation unless $100,000 in sales OR 200+ separate transactions
- No retroactive application
- Streamlined Sales Tax Agreement member (uniform definitions, central registration, simplified filing)

STATE-BY-STATE ECONOMIC NEXUS THRESHOLDS (as of 2024):
$100,000 sales threshold: 28 states
$100,000 OR 200 transactions: 18 states (original Wayfair model)
$500,000 sales threshold: California, New York, Texas (sales tax)
Sales-only test (no transaction count): Trending approach to reduce compliance burden

CONSTITUTIONAL ANALYSIS POST-WAYFAIR:
SUBSTANTIAL NEXUS: Economic presence through purposeful direction of business toward state market satisfies Commerce Clause. Courts examine:
- Systematic and continuous solicitation
- Volume of sales (dollar and transaction counts)
- Use of state infrastructure (delivery, payment processing, state-facilitated marketplaces)
- Targeting of state residents through advertising/marketing

DUE PROCESS: Economic nexus also satisfies Due Process "minimum contacts" if:
- Purposeful availment of state market
- Fair warning that conduct may subject seller to state's jurisdiction
- Reasonable relationship between contacts and tax obligation
- Prospective-only application (retroactive may violate fair notice)

MARKETPLACE FACILITATOR RULES:
45 states enacted marketplace facilitator laws shifting collection obligation from third-party sellers to platforms (Amazon, eBay, Etsy). This:
- Reduces compliance burden on small sellers
- Increases collection efficiency
- Addresses "loophole" of platform sales
- Generally withstands constitutional challenge due to reduced burden

INCOME TAX ECONOMIC NEXUS:
Post-Wayfair, many states adopted economic nexus for income/franchise tax:
- Factor presence nexus: sales, property, or payroll exceeding threshold
- Bright-line tests: $50K-$500K in sales, $50K in property, $50K in payroll
- P.L. 86-272 still protects solicitation of tangible personal property sales (does NOT apply to services, rentals, sales of intangibles)
""",
        key_factors=[
            "Wayfair overruled Quill's physical presence requirement (2018)",
            "$100K sales OR 200 transactions is most common threshold",
            "Some states use sales-only thresholds ($500K in CA, NY, TX for sales tax)",
            "Prospective application reduces constitutional risk",
            "Safe harbors and SST membership supported in Wayfair",
            "Marketplace facilitator laws shift burden from sellers to platforms",
            "P.L. 86-272 does NOT apply to sales tax (only income tax on TPP sales)",
            "Economic nexus for income tax spreading (factor presence statutes)"
        ],
        primary_authority=[
            "South Dakota v. Wayfair, Inc., 138 S. Ct. 2080 (2018)",
            "SD Codified Laws § 10-64-2 (economic nexus statute)",
            "Quill Corp. v. North Dakota, 504 U.S. 298 (1992) [overruled]",
            "MTC Model Notice and Reporting Statute (alternative to collection)",
            "Streamlined Sales and Use Tax Agreement",
            "State economic nexus statutes (45+ states post-Wayfair)"
        ],
        burden_holder="Taxpayer challenging economic nexus statute",
        adversary_position="State will argue economic contacts are substantial and purposeful, safe harbor thresholds are reasonable, prospective application satisfies due process, and marketplace facilitator collection reduces burden",
        counter_arguments=[
            "Small businesses face disproportionate compliance costs",
            "Transaction count threshold (200) is arbitrary and burdensome",
            "Lack of uniform thresholds creates patchwork compliance nightmare",
            "Retroactive application violates due process fair notice",
            "Economic presence is insufficient for tax jurisdiction (due process argument)"
        ],
        resolution_strategy="Determine if taxpayer exceeds state's economic nexus threshold (sales and/or transactions). If yes, assess whether prospective-only application and safe harbors make statute constitutional under Wayfair. Consider marketplace facilitator rules if sales through platforms. For income tax, analyze factor presence thresholds and P.L. 86-272 applicability. Document compliance with economic nexus registration and filing requirements.",
        entity_scope="Remote sellers, marketplace facilitators, online retailers",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="South Dakota v. Wayfair, Inc., 138 S. Ct. 2080 (2018)",
        effective_date="2018-06-21"
    ),

    DoctrineBlock(
        topic="pl_86_272_safe_harbor_scope",
        category=IssueCategory.PL_86_272_PROTECTION,
        keywords=["pl 86-272", "p.l. 86-272", "solicitation", "tangible personal property", "safe harbor", "15 usc 381"],
        conclusion_template=[
            "P.L. 86-272 prohibits states from imposing net income tax on out-of-state sellers whose only activity is solicitation of orders for tangible personal property (TPP) that are approved and filled from outside the state.",
            "Protection does NOT extend to: (1) services, (2) sales of intangibles, (3) rentals/leases, (4) activities beyond mere solicitation, (5) gross receipts taxes, or (6) sales/use taxes.",
            "MTC revised guidance (2021) narrowly interprets 'solicitation' and provides detailed lists of protected vs. unprotected activities."
        ],
        reasoning_framework="""
P.L. 86-272 STATUTORY TEXT (15 U.S.C. §§ 381-384):
Section 381 prohibits a state from imposing a "net income tax" on income derived from interstate commerce if:
1. The only business activity in the state is solicitation of orders
2. Orders are for sales of tangible personal property
3. Orders are sent outside the state for approval or rejection
4. Orders are filled by shipment or delivery from outside the state

CRITICAL LIMITATIONS:
ONLY APPLIES TO NET INCOME TAX:
- Does NOT protect against gross receipts taxes (Washington B&O, Ohio CAT, Texas franchise tax margin)
- Does NOT protect against sales/use tax collection obligations
- Does NOT protect against franchise tax measured by capital

ONLY APPLIES TO SALES OF TPP:
- Services NOT protected (Wisconsin Dept. of Revenue v. William Wrigley, Jr., Co., 505 U.S. 214 (1992))
- Sales of intangibles NOT protected (licenses, royalties, digital goods in many states)
- Rentals and leases NOT protected
- Mixed transactions: MTC guidance requires separation of TPP sales from non-protected activities

SOLICITATION DEFINED (MTC GUIDANCE, revised 2021):
PROTECTED solicitation activities:
- Soliciting orders through employees, independent contractors, or by mail/phone/internet
- Conducting meetings with customers/prospects to solicit orders
- Maintaining sales office used exclusively for solicitation
- Maintaining free samples for display/distribution
- Furnishing and setting up display racks
- Providing automobiles to salespersons for solicitation
- Passing inquiries/complaints to home office
- Missionary sales activities (educating customers about products)
- Coordinating shipment/delivery WITHOUT control over delivery (tracking only)

UNPROTECTED activities beyond solicitation:
- Accepting/approving orders in-state
- Maintaining inventory in state (even if for display)
- Repairing/servicing products in state (except warranty repairs under contract with home office)
- Collecting current or delinquent accounts
- Conducting training for customer employees (beyond product use)
- Providing engineering/technical assistance
- Investigating credit-worthiness in-state
- Installation activities
- Maintaining office for non-solicitation purposes
- Consignment sales (inventory ownership in-state)
- Making repairs or providing maintenance under service contracts

DE MINIMIS EXCEPTION:
15 U.S.C. § 381(a)(3) provides that "solicitation" includes "ancillary activities" if de minimis. MTC interprets de minimis VERY narrowly - activities must be trivial and entirely secondary to solicitation.

STATE-SPECIFIC INTERPRETATIONS:
- California FTB: strict application, no protection for intangibles/services
- New York: follows MTC guidance closely
- Texas: P.L. 86-272 does NOT apply to franchise tax (gross receipts-based margin tax)
- Illinois: P.L. 86-272 does NOT apply to personal property replacement tax (gross receipts)

SERVICES EXCLUSION - WRIGLEY CASE:
Wisconsin Dept. of Revenue v. William Wrigley, Jr., Co., 505 U.S. 214 (1992):
Wrigley's employees provided in-state services (market research, shelf space consultation, checking stock). Court held these activities were NOT "ancillary to solicitation" even if they promoted TPP sales. Services are NOT protected by P.L. 86-272.

DIGITAL GOODS:
State treatment varies:
- Some states classify digital goods as intangibles (NOT protected)
- Some states classify specific digital goods as TPP by statute
- Cloud-based software (SaaS) generally treated as service (NOT protected)
- Downloaded software: state-specific (some TPP, some intangible)
""",
        key_factors=[
            "Protects only solicitation of orders for tangible personal property sales",
            "Does NOT protect services, intangibles, rentals, or leases",
            "Does NOT apply to gross receipts taxes or sales tax",
            "Applies only to net income tax",
            "Orders must be approved outside state and filled from outside state",
            "Activities beyond solicitation destroy protection (Wrigley case)",
            "De minimis exception is very narrow per MTC guidance",
            "MTC revised guidance (2021) provides detailed activity lists",
            "Digital goods treatment varies by state",
            "Independent contractor activities count as taxpayer activities"
        ],
        primary_authority=[
            "P.L. 86-272, 15 U.S.C. §§ 381-384",
            "Wisconsin Dept. of Revenue v. William Wrigley, Jr., Co., 505 U.S. 214 (1992)",
            "MTC Statement of Information Concerning Practices (revised 2021)",
            "MTC Proposed Amendments re: Digital Economy (ongoing)",
            "State administrative guidance (CA FTB, NY TSB, etc.)"
        ],
        burden_holder="State asserting activities exceed protected solicitation",
        adversary_position="State will argue taxpayer's in-state activities go beyond mere solicitation (installation, training, repairs, credit investigation, inventory maintenance), or that sales involve services/intangibles not protected by P.L. 86-272",
        counter_arguments=[
            "Activities are de minimis and ancillary to solicitation",
            "Digital goods should be treated as TPP for P.L. 86-272 purposes",
            "Services are incidental to TPP sale and should be protected",
            "Independent contractor activities should not be attributed to principal"
        ],
        resolution_strategy="Determine if tax is net income tax (P.L. 86-272 does not apply to gross receipts taxes). Confirm sales are of tangible personal property (not services, intangibles, rentals). Analyze in-state activities using MTC guidance lists - if ANY unprotected activity occurs in state, P.L. 86-272 protection is lost. Consider separating protected TPP sales from unprotected activities for apportionment purposes. Document that orders are approved/filled from outside state.",
        entity_scope="Out-of-state sellers with in-state solicitation activities",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Wisconsin Dept. of Revenue v. William Wrigley, Jr., Co., 505 U.S. 214 (1992)",
        effective_date="1959-09-14"
    ),

    DoctrineBlock(
        topic="texas_franchise_tax_nexus",
        category=IssueCategory.TEXAS_FRANCHISE_TAX,
        keywords=["texas franchise tax", "margin tax", "nexus", "texas receipts", "tmi", "taxable margin", "70% rule"],
        conclusion_template=[
            "Texas franchise tax is imposed on entities doing business in Texas, defined as either (1) being organized in Texas, or (2) having nexus with Texas through receipts sourced to Texas.",
            "Texas follows economic nexus standard post-Wayfair; $500,000 Texas receipts threshold for nexus.",
            "Franchise tax is a privilege tax measured by 'taxable margin' (NOT net income), so P.L. 86-272 does NOT apply."
        ],
        reasoning_framework="""
TEXAS FRANCHISE TAX STRUCTURE (Tax Code Chapter 171):

TAXPAYERS SUBJECT TO TAX:
- Each taxable entity formed in Texas
- Each taxable entity doing business in Texas (nexus standard)

TAXABLE ENTITY DEFINED (§171.0002):
- Corporation, LLC, partnership (unless wholly owned by natural persons - exemption for many partnerships)
- Professional associations, business trusts, REITs (if not exempt)
- Exemptions: sole proprietorships, general partnerships (if no entity owners), most passive entities

NEXUS STANDARD (§171.0001, §171.1011):
PRE-WAYFAIR: Required physical presence (office, employee, agent, property)
POST-WAYFAIR (2019+): Economic nexus - $500,000 Texas receipts in preceding 12 months

TEXAS RECEIPTS SOURCING (§171.103, §171.106):
- Receipts from sale of TPP: sourced to Texas if shipped to Texas buyer
- Services: sourced to Texas if performed in Texas OR if customer/payor located in Texas (market-based)
- Rentals: sourced to Texas if property located in Texas
- Intangibles: sourced to Texas if used in Texas (market-based)

TAXABLE MARGIN COMPUTATION (§171.101):
Margin = lesser of:
1. Total revenue minus cost of goods sold (COGS)
2. Total revenue minus compensation
3. Total revenue × 70%
4. Total revenue (if no subtraction elected)

THEN: Margin × apportionment percentage × tax rate

TAX RATES (§171.002):
- Most entities: 0.375% (retail/wholesale) or 0.75% (other)
- Rate applied to apportioned margin
- $1.23 million exemption threshold (no tax if total revenue < threshold)

APPORTIONMENT (§171.106):
Single receipts factor: Texas receipts / total receipts everywhere

NO P.L. 86-272 PROTECTION:
Texas franchise tax is NOT a net income tax. It is a privilege tax measured by margin (gross receipts-based). P.L. 86-272 explicitly protects only "net income tax." Texas Comptroller and courts confirm P.L. 86-272 does not apply.

COGS ELECTION (§171.1012):
COGS includes:
- Cost to acquire or produce TPP sold
- Direct labor and materials
- Overhead (if Texas Admin Code requires)
- NOT services (service businesses cannot use COGS subtraction)

COMPENSATION ELECTION (§171.1013):
Total wage/salary compensation paid to employees and officers, capped at $350,000 per person

70% GROSS RECEIPTS ELECTION:
No documentation required, automatic 30% reduction as proxy for margin

FILING REQUIREMENTS:
- Annual report due May 15
- Franchise tax year = federal tax year or calendar year
- Combined reporting NOT required (each entity files separately unless affiliated group election)

CONSTITUTIONAL CHALLENGES:
Texas franchise tax has withstood Commerce Clause challenges because:
- Single receipts factor apportionment is internally and externally consistent
- No discrimination against interstate commerce
- Fairly related to state services (courts, infrastructure, legal system)
""",
        key_factors=[
            "$500,000 Texas receipts creates economic nexus (post-Wayfair)",
            "Franchise tax is privilege tax, NOT net income tax (P.L. 86-272 does not apply)",
            "Taxable margin = lesser of (revenue-COGS, revenue-comp, revenue×70%, revenue)",
            "Single receipts factor apportionment (Texas receipts / total receipts)",
            "Market-based sourcing for services and intangibles",
            "LLCs and partnerships can be taxable entities (not all are exempt)",
            "$1.23 million no-tax-due threshold",
            "Combined reporting NOT mandatory (entity-by-entity default)",
            "Tax rates: 0.375% or 0.75% depending on NAICS code"
        ],
        primary_authority=[
            "Texas Tax Code Chapter 171 (Franchise Tax)",
            "Texas Admin. Code Title 34, Part 1, Chapter 3, Rule 3.591 (Nexus)",
            "34 TAC § 3.584 (Margin computation)",
            "34 TAC § 3.586 (Apportionment)",
            "Texas Comptroller Rule 3.591 (Doing Business in Texas)",
            "Texas Comptroller Publication 96-576 (Franchise Tax Guidelines)"
        ],
        burden_holder="Taxpayer challenging nexus or margin computation",
        adversary_position="Texas Comptroller will assert economic nexus based on $500K Texas receipts, argue P.L. 86-272 does not apply to margin-based tax, and enforce strict COGS/compensation subtraction rules",
        counter_arguments=[
            "Economic nexus violates substantial nexus prong of Complete Auto",
            "Market-based sourcing creates nexus where no activities occur",
            "Margin tax is effectively an income tax and P.L. 86-272 should apply",
            "Single receipts factor apportionment overstates Texas activity"
        ],
        resolution_strategy="Calculate Texas-sourced receipts using market-based sourcing rules. If exceeds $500K, nexus exists. Determine entity type and exemptions. Compute taxable margin using four methods and select lowest. Apply apportionment percentage (Texas receipts / total receipts). Compare to $1.23M exemption threshold. File annual franchise tax report by May 15. P.L. 86-272 argument will fail.",
        entity_scope="Corporations, LLCs, partnerships (with entity partners), doing business in Texas",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Texas Tax Code Chapter 171",
        state_specific_notes="Texas has unique margin-based tax structure. COGS subtraction favors manufacturers/resellers. Service businesses typically use compensation or 70% methods.",
        effective_date="2008-01-01 (margin tax effective date)"
    ),

    DoctrineBlock(
        topic="factor_presence_nexus_income_tax",
        category=IssueCategory.FACTOR_PRESENCE,
        keywords=["factor presence", "bright-line nexus", "sales factor", "property factor", "payroll factor", "apportionment factor"],
        conclusion_template=[
            "Factor presence nexus statutes establish income tax nexus based on exceeding quantitative thresholds for property, payroll, or sales within a state.",
            "Common thresholds: $50,000-$500,000 in sales, $50,000 in property, $50,000 in payroll, or 25% of total apportionment factors.",
            "Factor presence nexus is constitutional post-Wayfair and not protected by P.L. 86-272 for services or intangibles."
        ],
        reasoning_framework="""
FACTOR PRESENCE NEXUS STATUTES:

CONCEPT:
Factor presence statutes create income/franchise tax nexus when a taxpayer's apportionment factors (sales, property, payroll) exceed statutory thresholds in a state, even without physical presence.

COMMON THRESHOLDS (state-by-state variation):

SALES FACTOR:
- $50,000: Michigan, Pennsylvania
- $250,000: California (prior to 2011 amendment to $500K)
- $500,000: California (current), Colorado, Connecticut, New York, Ohio, Tennessee
- $1,000,000: Alabama, Oklahoma

PROPERTY FACTOR:
- $50,000: California, Colorado, Michigan, Pennsylvania, Tennessee
- $100,000: Oklahoma

PAYROLL FACTOR:
- $50,000: California, Colorado, Michigan, Pennsylvania, Tennessee
- $100,000: Oklahoma

PERCENTAGE TEST:
- 25% of total property, payroll, or sales: California (alternative to dollar thresholds)

REPRESENTATIVE STATES:

CALIFORNIA (Cal. Rev. & Tax. Code § 23101):
Doing business includes:
- Sales in California exceed lesser of $500,000 or 25% of total sales
- Property in California exceeds lesser of $50,000 or 25% of total property
- Payroll in California exceeds lesser of $50,000 or 25% of total payroll

NEW YORK (N.Y. Tax Law § 209.1):
Nexus if:
- $1,000,000 in receipts (prior law: $500,000)
- Bright-line presence test for corporate franchise tax

COLORADO (Colo. Rev. Stat. § 39-22-301.3):
$50,000 in property, $50,000 in payroll, or $500,000 in sales

CONSTITUTIONAL BASIS POST-WAYFAIR:
Factor presence nexus satisfies:
1. SUBSTANTIAL NEXUS: Economic contacts through sales, property, or payroll demonstrate purposeful direction toward state
2. DUE PROCESS: Exceeding factor thresholds shows minimum contacts sufficient for jurisdiction
3. FAIR APPORTIONMENT: Nexus tied to apportionment factors ensures internal/external consistency
4. NO DISCRIMINATION: Applied equally to in-state and out-of-state taxpayers

P.L. 86-272 INTERACTION:
- P.L. 86-272 can protect sales of TPP even if factor presence nexus exists
- BUT: services, intangibles, rentals NOT protected
- AND: activities beyond solicitation destroy protection
- RESULT: Factor presence often captures taxpayers P.L. 86-272 does not protect

PLANNING CONSIDERATIONS:
- De minimis thresholds: some taxpayers intentionally stay below nexus thresholds
- Separate entity structures: isolate activities in no-nexus subsidiaries
- Drop-shipment strategies: avoid property factor nexus
- Independent contractor vs. employee: payroll factor planning (but employee characterization laws limit this)
- Trailing nexus: factor presence in Year 1 may create filing obligation in Year 2

NOTICE AND REPORTING STATUTES (alternative to nexus):
Some states adopted notice/reporting statutes as alternative to economic nexus for remote sellers:
- Colorado's notice statute (struck down in Direct Marketing Ass'n v. Brohl, but later versions upheld)
- Requires non-collecting retailers to notify Colorado purchasers of use tax obligation
- Does NOT create income tax nexus, but creates sales tax reporting obligation
""",
        key_factors=[
            "Factor presence creates income tax nexus without physical presence",
            "Common thresholds: $500K sales, $50K property/payroll",
            "P.L. 86-272 may still protect TPP sales even with factor nexus",
            "Services and intangibles NOT protected by P.L. 86-272",
            "Factor presence is constitutional under Wayfair reasoning",
            "Percentage tests (25% of total factor) are alternative to dollar thresholds",
            "States vary significantly in threshold amounts",
            "Trailing nexus: prior year factors may trigger current year filing"
        ],
        primary_authority=[
            "Cal. Rev. & Tax. Code § 23101 (factor presence nexus)",
            "Colo. Rev. Stat. § 39-22-301.3 (factor presence)",
            "N.Y. Tax Law § 209.1 (nexus standards)",
            "Mich. Comp. Laws § 206.621 (nexus)",
            "MTC Model Factor Presence Nexus Statute",
            "South Dakota v. Wayfair, Inc., 138 S. Ct. 2080 (2018) (constitutional basis)"
        ],
        burden_holder="Taxpayer challenging factor presence nexus statute",
        adversary_position="State will argue factor presence thresholds demonstrate substantial economic nexus, satisfy Due Process minimum contacts, and are constitutional under Wayfair; P.L. 86-272 does not apply to services/intangibles",
        counter_arguments=[
            "Factor presence without physical presence violates substantial nexus",
            "Thresholds are arbitrary and lack rational basis",
            "Compliance burden on small businesses is discriminatory",
            "Lack of physical presence means state provides no benefits to justify tax"
        ],
        resolution_strategy="Calculate taxpayer's property, payroll, and sales in each factor presence nexus state. Compare to statutory thresholds. If exceeded, nexus exists for income/franchise tax. Assess P.L. 86-272 protection for TPP sales (if applicable). For services/intangibles, factor presence nexus cannot be avoided with P.L. 86-272. Consider filing obligations, estimated tax payments, and apportionment implications. Plan to stay below thresholds if economically feasible.",
        entity_scope="Corporations, pass-through entities with multistate operations",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="South Dakota v. Wayfair, Inc., 138 S. Ct. 2080 (2018)"
    ),

    DoctrineBlock(
        topic="affiliate_nexus_attribution",
        category=IssueCategory.ATTRIBUTION_NEXUS,
        keywords=["affiliate nexus", "attribution", "agency nexus", "subsidiary nexus", "interbrand competition", "related party"],
        conclusion_template=[
            "Affiliate nexus (or attribution nexus) imputes physical presence of in-state affiliates to out-of-state sellers based on common ownership, control, or business integration.",
            "Key cases: Geoffrey (trademark licensing), Borders Online (agency relationship), KFC (interbrand competition test).",
            "Constitutional challenges often fail if affiliate performs services substantially benefiting out-of-state seller or exercises control over seller's operations."
        ],
        reasoning_framework="""
AFFILIATE NEXUS THEORIES:

1. AGENCY NEXUS:
Out-of-state principal has nexus through in-state agent if agent:
- Regularly solicits orders on behalf of principal
- Has authority to bind principal
- Maintains inventory or office for principal's benefit
- Performs services that create physical presence

STANDARD: Whether agent's activities are "significantly associated with" the taxpayer's ability to establish and maintain a market in the state.

Scripto, Inc. v. Carson, 362 U.S. 207 (1960): Independent contractors soliciting orders created nexus for principal.

Tyler Pipe Industries, Inc. v. Washington Dept. of Revenue, 483 U.S. 232 (1987): Independent sales representative's activities attributed to out-of-state principal.

2. INTANGIBLE PROPERTY NEXUS (GEOFFREY DOCTRINE):
Geoffrey, Inc. v. South Carolina Tax Comm'n, 437 S.E.2d 13 (S.C. 1993):
Delaware holding company licensed trademarks to affiliate Toys "R" Us stores in South Carolina. Court held:
- Trademarks have "commercial domicile" where they are exploited
- Licensing intangibles to in-state affiliate creates nexus
- Physical presence of affiliate (licensee) establishes nexus for licensor

GEOFFREY APPROACH ADOPTED BY: Alabama, California, Connecticut, Mississippi, North Carolina, others
REJECTED BY: Delaware (home state), Wisconsin (no physical presence from intangibles alone)

POST-WAYFAIR: Geoffrey nexus is economic nexus (intangible exploitation), strengthened by Wayfair's rejection of physical presence requirement.

3. INTERBRAND COMPETITION TEST (KFC):
KFC Corp. v. Iowa Dept. of Revenue, 792 N.W.2d 308 (Iowa 2010):
Out-of-state franchisor (KFC) had nexus through franchisee operations because:
- Franchisor and franchisee are NOT in interbrand competition (they sell same brand)
- Franchisee's activities substantially benefit franchisor
- Franchisor exercises control over franchisee operations (quality standards, operations manual)

INTERBRAND COMPETITION: If in-state affiliate competes with out-of-state seller (different brands), no attribution nexus. If same brand/integrated operations, nexus exists.

4. CONSOLIDATED/UNITARY BUSINESS NEXUS:
If in-state and out-of-state entities are part of unitary business:
- Nexus of one member can establish nexus for entire unitary group
- Combined reporting states may require inclusion of all unitary members
- Apportionment based on combined group's factors

5. BORDERS ONLINE NEXUS:
Borders Online, LLC v. State Bd. of Equalization, 29 Cal. Rptr. 3d 176 (Ct. App. 2005):
Online retailer (Borders Online) had nexus through affiliate (Borders brick-and-mortar stores) because:
- Common branding
- In-store returns accepted for online purchases
- Shared advertising and customer data
- Affiliate performed services benefiting online seller

MODERN VARIATION: Amazon and other online retailers avoid this by operating through separate legal entities and avoiding in-state services by affiliates.

STATUTORY AFFILIATE NEXUS (CLICK-THROUGH NEXUS):
New York Tax Law § 1101(b)(8)(vi) ("Amazon Law"):
Creates nexus if:
- Out-of-state seller pays commission to in-state residents for referrals
- Gross receipts from NY referrals exceed $10,000 annually
- Creates rebuttable presumption of nexus

CONSTITUTIONAL CHALLENGES:
- Amazon.com, LLC v. New York State Dept. of Taxation & Finance, 913 N.Y.S.2d 129 (App. Div. 2010): UPHELD click-through nexus statute
- Presumption is rebuttable (seller can show referrers do not solicit sales)

PLANNING TO AVOID AFFILIATE NEXUS:
- Separate legal entities with distinct operations
- Avoid shared branding, customer lists, advertising
- No in-state services by affiliate for benefit of out-of-state seller
- Independent contractor agreements (but Scripto limits effectiveness)
- Ensure interbrand competition (different brands, different markets)
- Avoid in-state inventory ownership or bailment
""",
        key_factors=[
            "Agency relationship can create nexus through agent's physical presence",
            "Geoffrey doctrine: intangibles exploited in-state create nexus (post-Wayfair strengthened)",
            "Interbrand competition test: no competition = nexus; competition = no nexus (KFC)",
            "Click-through nexus: commissions to in-state referrers create presumption",
            "Common ownership alone is insufficient; operational integration required",
            "Borders Online: in-store returns and shared services created nexus",
            "Separate entities with distinct operations can avoid attribution",
            "Unitary business doctrine can require combined reporting and attribution"
        ],
        primary_authority=[
            "Geoffrey, Inc. v. South Carolina Tax Comm'n, 437 S.E.2d 13 (S.C. 1993)",
            "KFC Corp. v. Iowa Dept. of Revenue, 792 N.W.2d 308 (Iowa 2010)",
            "Borders Online, LLC v. State Bd. of Equalization, 29 Cal. Rptr. 3d 176 (Ct. App. 2005)",
            "Scripto, Inc. v. Carson, 362 U.S. 207 (1960)",
            "Tyler Pipe Industries, Inc. v. Washington Dept. of Revenue, 483 U.S. 232 (1987)",
            "Amazon.com, LLC v. New York State Dept. of Taxation & Finance, 913 N.Y.S.2d 129 (App. Div. 2010)",
            "N.Y. Tax Law § 1101(b)(8)(vi) (click-through nexus)"
        ],
        burden_holder="Taxpayer challenging attribution/affiliate nexus",
        adversary_position="State will argue affiliate's physical presence or activities benefit out-of-state seller, common branding creates integrated operations, intangibles are exploited in-state (Geoffrey), or agency relationship exists (Scripto/Tyler Pipe)",
        counter_arguments=[
            "Separate legal entities should be respected",
            "No control over affiliate's operations",
            "Interbrand competition exists (KFC test not met)",
            "Arm's length transactions with affiliate",
            "Intangibles do not have physical presence (pre-Wayfair argument, weakened)"
        ],
        resolution_strategy="Analyze relationship between out-of-state seller and in-state affiliate: (1) common ownership/control, (2) shared branding/operations, (3) in-state services benefiting out-of-state seller, (4) interbrand competition or integration, (5) unitary business factors. If affiliate nexus asserted, examine whether separate entities with distinct operations. Post-Wayfair, even intangible exploitation (Geoffrey) likely creates nexus. Consider restructuring to eliminate in-state affiliate services, shared branding, or inventory.",
        entity_scope="Out-of-state sellers with in-state affiliates, franchisors, IP holding companies",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Geoffrey, Inc. v. South Carolina Tax Comm'n, 437 S.E.2d 13 (S.C. 1993); KFC Corp. v. Iowa Dept. of Revenue, 792 N.W.2d 308 (Iowa 2010)"
    ),

    DoctrineBlock(
        topic="marketplace_facilitator_collection",
        category=IssueCategory.MARKETPLACE_FACILITATOR,
        keywords=["marketplace facilitator", "amazon fba", "ebay", "etsy", "platform seller", "third party seller"],
        conclusion_template=[
            "Marketplace facilitator laws require platforms (Amazon, eBay, Etsy) to collect and remit sales tax on behalf of third-party sellers.",
            "44+ states enacted marketplace facilitator laws post-Wayfair, effective 2019-2020.",
            "Third-party sellers are generally relieved of collection obligation when facilitator collects; reduces compliance burden and increases state revenue."
        ],
        reasoning_framework="""
MARKETPLACE FACILITATOR STATUTES:

DEFINITION (typical statutory language):
"Marketplace facilitator" = person who:
1. Contracts with sellers to facilitate sales through physical or electronic marketplace
2. Collects payment from customer and transmits to seller
3. Through terms and conditions, agreement, or arrangement, collects sales tax or use tax on behalf of seller

EXAMPLES: Amazon (including FBA), eBay, Etsy, Walmart Marketplace, Facebook Marketplace (commercial), Uber Eats, DoorDash (food delivery), Airbnb (lodging)

COLLECTION OBLIGATION:
Marketplace facilitator must collect/remit sales tax on:
- Facilitator's own sales
- Third-party seller sales facilitated through the marketplace

RELIEF FOR THIRD-PARTY SELLERS:
When marketplace facilitator collects, third-party seller is generally NOT required to:
- Register for sales tax permit
- Collect tax on marketplace sales
- File sales tax returns for those sales

BUT: Third-party seller MUST still collect on direct sales (non-marketplace)

STATE ADOPTION (44+ states):
EFFECTIVE DATES:
- 2019: Alabama, Connecticut, Iowa, Minnesota, New Jersey, Oklahoma, Pennsylvania, Washington, others
- 2020: California, Florida, Illinois, New York, Texas, others
- 2023: Missouri (last major state to adopt)

THRESHOLDS (vary by state):
Most states: Same economic nexus threshold as remote sellers ($100K sales or 200 transactions)
Some states: No threshold (all marketplace facilitators must collect)

RELIABILITIZATION OF MARKETPLACE:
Facilitator statutes include "hold harmless" provisions:
- Third-party seller is not liable for tax if facilitator fails to collect
- Facilitator is solely liable to state
- Exception: Seller provided incorrect information to facilitator

CONSTITUTIONAL BASIS:
Marketplace facilitator laws withstand Commerce Clause scrutiny because:
1. Reduces compliance burden (fewer collectors)
2. Increases efficiency of tax collection
3. Addresses "loophole" of platform sales
4. Mentioned favorably in Wayfair dicta

WAYFAIR DICTA:
"States may have reasonable options that allow them to collect the tax from those who make sales through such mechanisms [marketplace facilitators]."

AMAZON FBA (FULFILLMENT BY AMAZON):
- Amazon stores seller's inventory in Amazon warehouses
- Amazon ships products to customers
- Amazon is marketplace facilitator for FBA transactions
- Amazon collects and remits sales tax
- Seller has NO collection obligation for FBA sales
- BUT: Seller may have income tax nexus due to inventory in Amazon's in-state warehouses (physical presence)

INCOME TAX IMPLICATIONS:
- Marketplace facilitator collection is ONLY for sales tax
- Third-party sellers still have income tax nexus if:
  * Economic nexus thresholds exceeded
  * Inventory stored in-state (FBA warehouses)
  * Factor presence nexus standards met
- P.L. 86-272 may protect TPP sales (income tax), but not sales tax

EXEMPTION CERTIFICATES:
- Marketplace facilitators must honor valid exemption certificates
- Seller is responsible for providing certificate to facilitator
- If seller fails to provide, facilitator must collect tax

REPORTING OBLIGATIONS:
Some states require marketplace facilitators to:
- Report sales by third-party sellers (even if tax collected)
- Provide annual 1099-K forms to sellers (IRS requirement: $600+ threshold as of 2023)

PLANNING CONSIDERATIONS:
- Ensure facilitator is collecting tax (verify on invoices)
- Maintain records showing facilitator collected
- File direct sales separately (non-marketplace sales)
- Monitor income tax nexus from inventory in facilitator warehouses
- Consider economic nexus for income tax even if sales tax covered by facilitator
""",
        key_factors=[
            "44+ states have marketplace facilitator laws (effective 2019-2020)",
            "Facilitator collects sales tax on behalf of third-party sellers",
            "Third-party sellers relieved of sales tax collection on marketplace sales",
            "Sellers still responsible for direct sales (non-marketplace)",
            "Amazon FBA, eBay, Etsy are common facilitators",
            "Hold harmless provisions protect sellers from facilitator non-compliance",
            "Income tax nexus still possible (inventory in FBA warehouses, economic nexus)",
            "Thresholds typically match economic nexus thresholds ($100K sales)"
        ],
        primary_authority=[
            "State marketplace facilitator statutes (44+ states)",
            "South Dakota v. Wayfair, Inc., 138 S. Ct. 2080 (2018) (dicta on facilitators)",
            "Streamlined Sales and Use Tax Agreement (facilitator provisions)",
            "Amazon.com Services LLC marketplace agreements",
            "State administrative guidance (CA, NY, TX, etc.)"
        ],
        burden_holder="Marketplace facilitator for sales tax collection; state for enforcement",
        adversary_position="State will argue marketplace facilitator statutes reduce compliance burden, increase efficiency, and are constitutional under Wayfair; third-party sellers should not have double collection obligation",
        counter_arguments=[
            "Facilitators lack information to determine exemptions",
            "Hold harmless creates moral hazard for facilitators to under-collect",
            "Income tax nexus still exists separate from sales tax collection",
            "Sellers lose control over tax compliance"
        ],
        resolution_strategy="Determine if sales are made through marketplace facilitator. If yes, verify facilitator is collecting sales tax (check invoices, agreements). Seller has NO sales tax collection obligation for marketplace sales. BUT: Assess income tax nexus separately (inventory in facilitator warehouses, economic nexus from sales volume). Maintain records of marketplace vs. direct sales. File income tax returns if nexus exists, even if sales tax collected by facilitator.",
        entity_scope="Third-party sellers on Amazon, eBay, Etsy, and other marketplaces",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="South Dakota v. Wayfair, Inc., 138 S. Ct. 2080 (2018); state marketplace facilitator statutes"
    ),

    # Adding 43 more doctrine blocks to reach 50+ total...

    DoctrineBlock(
        topic="uditpa_apportionment_framework",
        category=IssueCategory.APPORTIONMENT,
        keywords=["uditpa", "uniform division of income", "three factor formula", "equally weighted", "property payroll sales"],
        conclusion_template=[
            "UDITPA (Uniform Division of Income for Tax Purposes Act) provides model three-factor apportionment formula: equally weighted property, payroll, and sales factors.",
            "Business income is apportioned; non-business income is allocated to specific states.",
            "Most states have adopted UDITPA or variations, with trend toward single sales factor weighting."
        ],
        reasoning_framework="""
UDITPA FRAMEWORK:

BUSINESS INCOME VS. NON-BUSINESS INCOME:
BUSINESS INCOME: Income arising from transactions in regular course of taxpayer's trade or business; apportioned
NON-BUSINESS INCOME: All other income (investment income, sale of assets not inventory); allocated to specific states

APPORTIONMENT FORMULA (UDITPA § 9):
Apportionment percentage = (Property factor + Payroll factor + Sales factor) / 3

PROPERTY FACTOR (UDITPA § 10-11):
Numerator: Average value of real and tangible personal property owned or rented in state
Denominator: Average value of ALL property everywhere
- Real property: valued at original cost
- Tangible personal property: valued at original cost
- Rented property: capitalized at 8× annual rent

PAYROLL FACTOR (UDITPA § 13-14):
Numerator: Total compensation paid in state
Denominator: Total compensation paid everywhere
- Compensation: wages, salaries, commissions, bonuses
- Assigned to state where services performed
- If services in multiple states: base of operations, direction/control state, or residence (hierarchy)

SALES FACTOR (UDITPA § 15-17):
Numerator: Total sales in state
Denominator: Total sales everywhere
- TPP sales: destination (where shipped to)
- Services: where performed (cost-of-performance method under UDITPA)
- Intangibles: varies by type

STATE VARIATIONS FROM UDITPA:
DOUBLE-WEIGHTED SALES: Some states double sales factor (4-factor formula): (Prop + Pay + 2×Sales) / 4
SINGLE SALES FACTOR: 19+ states use 100% sales factor (no property/payroll): Sales in state / Total sales
MARKET-BASED SOURCING: Modern trend - sales factor based on customer/market location, NOT cost-of-performance

JOYCE METHOD VS. FINNIGAN METHOD (COMBINED REPORTING):
JOYCE (minority): Only group members with nexus in state are included in numerator
FINNIGAN (majority): All group members' in-state factors included in numerator, regardless of individual nexus
""",
        key_factors=[
            "UDITPA: equally weighted three-factor formula (property, payroll, sales)",
            "Business income apportioned; non-business income allocated",
            "Property factor: owned property at cost + rented property capitalized at 8×",
            "Payroll factor: compensation where services performed",
            "Sales factor: destination for TPP, cost-of-performance for services (UDITPA)",
            "Trend: single sales factor (19+ states) and market-based sourcing",
            "MTC model regulations provide detailed guidance"
        ],
        primary_authority=[
            "Uniform Division of Income for Tax Purposes Act (UDITPA)",
            "MTC Model General Allocation and Apportionment Regulations",
            "Moorman Mfg. Co. v. Bair, 437 U.S. 267 (1978) (Iowa single sales factor upheld)",
            "MeadWestvaco Corp. v. Illinois Dept. of Revenue, 553 U.S. 16 (2008) (business vs. non-business income)"
        ],
        burden_holder="Taxpayer to prove apportionment formula is unconstitutional",
        adversary_position="State will defend apportionment formula as fairly representing in-state activity and generating income reasonably attributed to state",
        counter_arguments=[
            "Single sales factor overstates income in market states",
            "Double-weighted sales creates disparate treatment",
            "Cost-of-performance does not reflect where income earned"
        ],
        resolution_strategy="Classify income as business or non-business. Apportion business income using state's formula. Calculate property factor (owned + rented), payroll factor (where services performed), sales factor (destination or market-based). Apply state's weighting. Allocate non-business income to specific states per UDITPA rules.",
        entity_scope="Multistate corporations, pass-through entities",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="market_based_sourcing_services",
        category=IssueCategory.SOURCING_RULES,
        keywords=["market-based sourcing", "service receipts", "customer location", "cascading rules", "hierarchy"],
        conclusion_template=[
            "Market-based sourcing assigns service receipts to the state where the customer receives the benefit of the service, rather than where the service is performed.",
            "Adopted by 30+ states to ensure sales factor reflects customer market, not cost-of-performance location.",
            "Cascading hierarchy rules determine sourcing when customer location is ambiguous or spans multiple states."
        ],
        reasoning_framework="""
MARKET-BASED SOURCING (MBS):

TRADITIONAL COST-OF-PERFORMANCE (COP):
UDITPA § 17: Service receipts assigned to state where "income-producing activity" is performed
PROBLEM: Incentivizes moving service employees to low-tax states; does not reflect customer market

MARKET-BASED SOURCING (MBS):
Service receipts assigned to state where customer receives benefit of service
PURPOSE: Reflect where revenue is economically generated (customer's market state)

MTC MODEL REGULATION (2014, revised 2018):
Tier 1: Assign to state where customer received benefit of service
Tier 2: If benefit received in multiple states, assign based on reasonable approximation
Tier 3: If cannot reasonably approximate, assign to customer's billing address
Tier 4: If billing address not in state with nexus, assign to customer's commercial domicile
Tier 5: If customer location cannot be determined, exclude from sales factor denominator (nowhere income)

STATE ADOPTION:
30+ states adopted MBS for services:
- California: market assignment (Cal. Rev. & Tax. Code § 25136)
- New York: market sourcing (N.Y. Tax Law § 210-A)
- Illinois, Massachusetts, Ohio, Pennsylvania, Texas, others

CALIFORNIA CASCADING RULES (Cal. Code Regs. tit. 18, § 25136-2):
1. Assign to state where benefit of service received by customer
2. If multiple states, assign to state where customer makes predominant use
3. If predominant use cannot be determined, assign in proportion to customer's use
4. If proportional assignment not reasonable, assign to customer's billing address
5. If billing address does not reasonably reflect benefit, assign to customer's principal place of business

EXAMPLES:
LEGAL SERVICES: Client receives benefit where legal matter arises or client is located
ACCOUNTING SERVICES: Client receives benefit at client's principal place of business
CONSULTING SERVICES: Client receives benefit where recommendations implemented or client's decision-makers located
CLOUD SERVICES (SaaS): Customer receives benefit where users access service

DIGITAL GOODS AND SERVICES:
State treatment varies:
- Some states: digital goods are TPP (destination sourcing)
- Some states: digital services are services (market-based sourcing)
- Some states: separate rules for electronically delivered products

APPORTIONMENT IMPACT:
MBS shifts sales factor from service-performance states to customer-market states
EXAMPLE: California consulting firm with clients nationwide - under COP, 100% sales in CA; under MBS, sales assigned to client states

THROWOUT RULE INTERACTION:
If customer is in state where taxpayer has no nexus, receipts may be "thrown out" (excluded from denominator) or "thrown back" (included in numerator of taxpayer's state)
THROWOUT: Reduces denominator (increases apportionment to other states)
THROWBACK: Increases numerator in taxpayer's home state (increases home state apportionment)
""",
        key_factors=[
            "Market-based sourcing assigns service receipts to customer's market state",
            "Replaces cost-of-performance (where service performed)",
            "30+ states adopted MBS for apportionment",
            "Cascading hierarchy rules: benefit received → approximation → billing address → domicile",
            "Shifts sales factor from service-performance states to customer states",
            "Throwout/throwback rules apply if customer in no-nexus state"
        ],
        primary_authority=[
            "MTC Model Regulation IV.17 (Market-based Sourcing, 2014/2018)",
            "Cal. Rev. & Tax. Code § 25136 (market assignment)",
            "Cal. Code Regs. tit. 18, § 25136-2 (cascading rules)",
            "N.Y. Tax Law § 210-A (market sourcing)",
            "Mass. Gen. Laws ch. 63, § 38 (market-based sourcing)"
        ],
        burden_holder="Taxpayer to demonstrate proper sourcing under state's hierarchy",
        adversary_position="State will argue MBS reflects economic reality of where income generated (customer market), not arbitrary cost-of-performance location",
        counter_arguments=[
            "Difficult to determine where customer receives benefit",
            "Increases compliance burden (tracking customer locations)",
            "May create nexus in customer states where no physical presence",
            "Cascading rules are ambiguous and subject to dispute"
        ],
        resolution_strategy="Identify customer location for each service transaction. Apply state's cascading rules: (1) where benefit received, (2) predominant use or proportional assignment, (3) billing address, (4) commercial domicile. Document reasonable approximation methodology. Consider throwout/throwback if customer in no-nexus state. MBS increases apportionment to customer-market states.",
        entity_scope="Service providers, SaaS companies, consulting firms",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="combined_reporting_unitary_business",
        category=IssueCategory.COMBINED_REPORTING,
        keywords=["combined reporting", "unitary business", "water's edge", "worldwide", "contribution", "dependency"],
        conclusion_template=[
            "Combined reporting requires affiliated corporations in a unitary business to file a single return apportioning combined income.",
            "Unitary business test: three unities (ownership, operation, use) or contribution/dependency.",
            "28 states require or allow combined reporting; prevents income shifting to low-tax jurisdictions."
        ],
        reasoning_framework="""
COMBINED REPORTING:

CONCEPT:
Instead of each corporation filing separately, all corporations in a unitary business combine income and apportion as single entity.

PURPOSE:
- Prevent income shifting to affiliates in low/no-tax states
- Fairly reflect economic reality of integrated operations
- Simplify enforcement (harder to manipulate transfer pricing)

UNITARY BUSINESS TEST:
THREE UNITIES (Mobil Oil test):
1. Unity of OWNERSHIP: Common control (>50% ownership typical threshold)
2. Unity of OPERATION: Centralized management, economies of scale, functional integration
3. Unity of USE: Centralized departments (purchasing, advertising, accounting, legal, HR)

CONTRIBUTION/DEPENDENCY TEST (alternative):
- Do business activities of separate corporations contribute to or depend upon each other?
- Flow of value between entities (IP, management services, supply chain)

CONTAINER CORP. V. FRANCHISE TAX BOARD, 463 U.S. 159 (1983):
Upheld California's worldwide combined reporting. Unitary business exists if operations are part of integrated system.

ALLIED-SIGNAL V. DIRECTOR, DIV. OF TAXATION, 504 U.S. 768 (1992):
Dividend income from subsidiary can be business income if payor and payee are unitary.

WATER'S EDGE ELECTION:
Limits combined group to U.S. corporations only (excludes foreign affiliates)
- Reduces compliance burden (foreign income/apportionment data)
- Available in most combined reporting states
- May require election and fee

WORLDWIDE COMBINED REPORTING:
Includes foreign affiliates in combined group
- California allowed (now water's edge default with election)
- Constitutional per Container Corp. but extremely burdensome
- Rare in practice due to water's edge elections

JOYCE VS. FINNIGAN:
JOYCE METHOD (minority): Only group members with nexus in state included in numerator
FINNIGAN METHOD (majority): All group members' in-state activities included in numerator

EXAMPLE (Finnigan):
- Parent Corp (CA) owns 100% of Sub Corp (NV)
- Sub has nexus in CA (sales, no physical presence)
- Under Finnigan: Sub's CA sales included in combined CA sales factor numerator, even though Sub has no physical presence

STATES REQUIRING COMBINED REPORTING (28 states):
Alaska, Arizona, California, Colorado, Connecticut, Hawaii, Idaho, Illinois, Kansas, Maine, Massachusetts, Michigan, Minnesota, Montana, Nebraska, New Hampshire, New York, North Dakota, Oregon, Rhode Island, Texas (limited), Utah, Vermont, West Virginia, Wisconsin

SEPARATE ENTITY STATES:
Allow separate filing per entity (but may require combined if distortion)

TRANSFER PRICING:
Separate entity states: enforce arm's length pricing (IRC § 482 analogue)
Combined reporting states: transfer pricing less relevant (income combined anyway)

INTERCOMPANY ELIMINATIONS:
Combined reporting eliminates intercompany transactions:
- Intercompany sales eliminated
- Intercompany royalties/interest eliminated
- Only third-party income/expenses remain

APPORTIONMENT:
Combined group's apportionment factors are sum of all unitary members' factors
Sales factor = Total in-state sales of all members / Total worldwide sales of all members

PLANNING:
- Separate entity states: Shift income to low-tax subsidiaries (subject to § 482/arm's length)
- Combined reporting states: Income shifting ineffective (all combined)
- Consider breaking unitary relationship (requires true economic separation)
""",
        key_factors=[
            "28 states require combined reporting for unitary businesses",
            "Unitary business: three unities (ownership, operation, use) or contribution/dependency",
            "Water's edge election limits to U.S. corporations",
            "Joyce vs. Finnigan: treatment of nexus in apportionment numerator",
            "Intercompany transactions eliminated in combined reporting",
            "Transfer pricing less relevant in combined states",
            "Prevents income shifting to low-tax affiliates"
        ],
        primary_authority=[
            "Container Corp. v. Franchise Tax Board, 463 U.S. 159 (1983)",
            "Mobil Oil Corp. v. Commissioner of Taxes, 445 U.S. 425 (1980)",
            "Allied-Signal, Inc. v. Director, Div. of Taxation, 504 U.S. 768 (1992)",
            "MTC Model Combined Reporting Regulations",
            "Cal. Rev. & Tax. Code §§ 25101-25141 (combined reporting)",
            "State combined reporting statutes (28 states)"
        ],
        burden_holder="Taxpayer to prove entities are not unitary or combined reporting is unconstitutional",
        adversary_position="State will argue entities are unitary (three unities or contribution/dependency), combined reporting prevents income shifting, and fairly reflects integrated operations",
        counter_arguments=[
            "Entities operate independently (no centralized management)",
            "No functional integration or economies of scale",
            "Worldwide combined reporting is overly burdensome",
            "Separate legal entities should be respected"
        ],
        resolution_strategy="Determine if state requires combined reporting. Assess if entities are unitary: (1) common ownership >50%, (2) centralized management/operations, (3) shared services (purchasing, HR, legal), (4) contribution/dependency. If unitary, file combined return with water's edge election if available. Eliminate intercompany transactions. Sum apportionment factors across all unitary members. Consider breaking unitary relationship through true economic separation.",
        entity_scope="Affiliated corporations with common ownership and integrated operations",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Container Corp. v. Franchise Tax Board, 463 U.S. 159 (1983)"
    ),

    DoctrineBlock(
        topic="throwback_throwout_rules",
        category=IssueCategory.APPORTIONMENT,
        keywords=["throwback rule", "throwout rule", "nowhere income", "pl 86-272 protection", "sales factor adjustment"],
        conclusion_template=[
            "Throwback rules assign sales to the seller's state if the customer is in a state where the seller is not taxable (no nexus or P.L. 86-272 protection).",
            "Throwout rules exclude such sales from the sales factor denominator entirely.",
            "Approximately 18 states have throwback rules; fewer have throwout rules; designed to prevent 'nowhere income.'"
        ],
        reasoning_framework="""
THROWBACK VS. THROWOUT:

NOWHERE INCOME PROBLEM:
If seller has nexus in State A but not State B, and ships goods to State B:
- State B cannot tax (no nexus)
- State A apportions based on destination → sales assigned to State B (not in numerator)
- Result: income escapes taxation ("nowhere income")

THROWBACK RULE (solution 1):
If seller is not taxable in destination state, "throw back" sales to state of origin (seller's state)
- Increases numerator in seller's state
- Sales included in both numerator and denominator

THROWOUT RULE (solution 2):
If seller is not taxable in destination state, "throw out" sales (exclude from denominator)
- Decreases denominator
- Increases apportionment percentage to other states

STATES WITH THROWBACK (18 states):
Alabama, Arkansas, California, Connecticut, Hawaii, Idaho, Illinois, Kansas, Maine, Mississippi, Montana, Nebraska, New Jersey, New Mexico, North Dakota, Oklahoma, Utah, West Virginia

STATES WITH THROWOUT (fewer):
Georgia, Iowa, Oregon, Pennsylvania (in certain circumstances)

CALIFORNIA THROWBACK (Cal. Rev. & Tax. Code § 25135):
Sales of TPP shipped from California to another state are assigned to California if:
1. Purchaser is U.S. government, or
2. Seller is not taxable in destination state

"NOT TAXABLE" DEFINED:
- No nexus in destination state, OR
- Protected by P.L. 86-272 in destination state

JOYCE V. FINNIGAN IMPACT:
JOYCE (minority): Throwback only if individual entity not taxable
FINNIGAN (majority): Throwback if combined group not taxable (any member's nexus counts)

P.L. 86-272 INTERACTION:
If seller has P.L. 86-272 protection in destination state (solicitation of TPP sales only):
- Seller is "not taxable" in destination state
- Throwback rule applies (sales thrown back to seller's state)
- Increases seller's state apportionment

EXAMPLE (California throwback):
- California Corp sells TPP to customers nationwide
- In State X, Corp only solicits orders (P.L. 86-272 protection)
- State X cannot impose income tax on Corp
- California throwback: sales to State X are thrown back to California (included in CA numerator)
- Increases California apportionment percentage

DOUBLE TAXATION RISK:
If destination state later asserts nexus (economic nexus, factor presence):
- Destination state taxes income attributed to its sales
- Origin state already taxed via throwback
- Result: double taxation (no federal mechanism to prevent state double taxation)

CREDITS FOR TAXES PAID TO OTHER STATES:
Some states provide credit for taxes paid to other states, reducing double taxation
BUT: Credit often limited to resident state's tax rate (does not eliminate double tax if other state's rate higher)

POLICY DEBATE:
PRO-THROWBACK: Prevents nowhere income, ensures fair taxation
ANTI-THROWBACK: Creates complexity, double taxation risk, penalizes in-state businesses

MODERN TREND:
- Economic nexus post-Wayfair reduces nowhere income (more states can tax remote sellers)
- Throwback rules less necessary but still applied
- Some states repealing throwback (e.g., Michigan repealed)
""",
        key_factors=[
            "Throwback: sales assigned to seller's state if not taxable in destination state",
            "Throwout: sales excluded from denominator if not taxable in destination",
            "18 states have throwback rules; fewer have throwout",
            "P.L. 86-272 protection triggers throwback (seller 'not taxable')",
            "Economic nexus post-Wayfair reduces nowhere income",
            "Double taxation risk if destination state later asserts nexus",
            "Joyce vs. Finnigan affects combined reporting throwback"
        ],
        primary_authority=[
            "Cal. Rev. & Tax. Code § 25135 (throwback rule)",
            "MTC Model Regulation IV.18 (throwback/throwout)",
            "State throwback statutes (18 states)",
            "P.L. 86-272, 15 U.S.C. §§ 381-384 (interaction with throwback)"
        ],
        burden_holder="Taxpayer to prove sales should not be thrown back/out",
        adversary_position="State will argue throwback prevents nowhere income and fairly taxes income attributable to in-state activities; P.L. 86-272 protection in destination state makes seller 'not taxable'",
        counter_arguments=[
            "Economic nexus eliminates nowhere income (throwback obsolete)",
            "Double taxation violates Commerce Clause fair apportionment",
            "Throwback penalizes in-state businesses vs. out-of-state competitors",
            "P.L. 86-272 'not taxable' definition is ambiguous"
        ],
        resolution_strategy="Determine if seller's state has throwback/throwout rule. For each sale, assess if seller is taxable in destination state (nexus exists and no P.L. 86-272 protection). If not taxable, apply throwback (include in numerator) or throwout (exclude from denominator). Post-Wayfair, economic nexus may eliminate throwback in many states. Document nexus analysis for each destination state. Consider double taxation risk if multiple states assert nexus.",
        entity_scope="Multistate sellers of tangible personal property",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="salt_deduction_cap_164b6",
        category=IssueCategory.SALT_CAP_PLANNING,
        keywords=["salt cap", "10000 limit", "164(b)(6)", "pass-through entity tax", "workaround", "ptet"],
        conclusion_template=[
            "IRC § 164(b)(6) caps state and local tax (SALT) deduction at $10,000 ($5,000 if married filing separately) for tax years 2018-2025.",
            "Pass-through entity (PTE) SALT workarounds allow entity-level state tax deduction, avoiding individual cap.",
            "IRS Notice 2020-75 blessed PTE workarounds; 30+ states enacted PTET legislation."
        ],
        reasoning_framework="""
SALT DEDUCTION CAP (IRC § 164(b)(6)):

STATUTORY TEXT:
"In the case of an individual, the aggregate amount of taxes described in paragraph (1) [state/local property and income taxes] which may be taken into account shall not exceed $10,000 ($5,000 in the case of a married individual filing a separate return)."

EFFECTIVE: Tax years 2018-2025 (sunsets 12/31/2025 under TCJA)

IMPACT:
High-tax states (CA, NY, NJ, CT, IL) - many taxpayers exceed $10K cap
- State income tax + property tax often >$10K
- Deduction limited to $10K, creating effective tax increase

PASS-THROUGH ENTITY (PTE) SALT WORKAROUND:

CONCEPT:
Entity-level state tax imposed on pass-through entity (S corp, partnership, LLC)
- Entity pays state tax and deducts as business expense (IRC § 162)
- Not subject to § 164(b)(6) cap (entity deduction, not individual)
- Owners get credit on individual state returns for entity-level tax paid
- Net result: full federal deduction for state tax via entity, avoiding individual cap

IRS NOTICE 2020-75 (11/9/2020):
IRS clarified that PTET workarounds are PERMISSIBLE:
- Entity-level state tax is deductible by entity under § 164(a)
- Owners who receive credit against individual state liability do NOT have income inclusion under tax benefit rule
- Blessing: states can implement PTET workarounds without federal challenge

STATE ADOPTION (30+ states):
Alabama, Arizona, Arkansas, California, Colorado, Connecticut, Georgia, Idaho, Illinois, Kansas, Louisiana, Maryland, Massachusetts, Michigan, Minnesota, Mississippi, New Jersey, New Mexico, New York, North Carolina, Ohio, Oklahoma, Oregon, Rhode Island, South Carolina, Utah, Virginia, Wisconsin

EXAMPLE (New York Pass-Through Entity Tax, N.Y. Tax Law § 860):
- S corp elects PTET
- Entity pays NY tax on entity income (6.85% rate)
- Entity deducts NY tax as business expense (federal deduction)
- Owners receive credit on individual NY returns for entity-level tax paid
- Owners' federal AGI reduced by entity's deduction (flows through to individual K-1 as reduction in income)

MECHANICS:
1. Entity elects into PTET (annual election in most states)
2. Entity calculates tax on entity income
3. Entity pays estimated taxes quarterly
4. Entity deducts tax as ordinary business expense
5. Owners receive K-1 showing reduced income (after entity-level tax deduction)
6. Owners report on individual federal return (lower pass-through income)
7. Owners file state return and claim credit for entity-level tax paid
8. Net: federal deduction achieved, state liability unchanged

LIMITATIONS:
- Not all states have enacted PTET
- Election requirements vary (annual, irrevocable, deadline)
- Some states impose entity-level tax as mandatory (not elective)
- Credits on individual state returns may not fully offset (rate differentials)

MULTI-STATE PLANNING:
- Entity with income in multiple states: some PTET states, some not
- Must track state-by-state PTET elections and credits
- Composite returns vs. PTET (different mechanisms)

CONSTITUTIONAL CHALLENGES:
Some states filed lawsuits claiming SALT cap is unconstitutional (NY, NJ, CT, MD)
- Argued cap violates state sovereignty, equal protection
- Dismissed: New York v. Mnuchin, 2021 (SALT cap is constitutional)

SUNSET (12/31/2025):
SALT cap expires after 2025 unless extended
- PTET workarounds may become obsolete if cap expires
- States may retain PTET as alternative tax structure
""",
        key_factors=[
            "IRC § 164(b)(6) caps SALT deduction at $10,000 (individuals) for 2018-2025",
            "PTET workarounds: entity-level state tax deductible as business expense",
            "IRS Notice 2020-75 approved PTET workarounds",
            "30+ states enacted PTET legislation",
            "Owners receive credit on state returns for entity-level tax paid",
            "Federal deduction achieved, state liability unchanged",
            "Annual election required in most states",
            "SALT cap sunsets 12/31/2025"
        ],
        primary_authority=[
            "IRC § 164(b)(6) (SALT deduction cap)",
            "IRS Notice 2020-75 (PTET workaround blessing)",
            "N.Y. Tax Law § 860 (NY PTET)",
            "Cal. Rev. & Tax. Code § 19900 (CA elective tax for pass-throughs)",
            "State PTET statutes (30+ states)",
            "New York v. Mnuchin, 2021 (SALT cap constitutional)"
        ],
        burden_holder="Taxpayer to elect PTET and comply with state requirements",
        adversary_position="IRS and states support PTET workarounds as permissible method to mitigate SALT cap impact",
        counter_arguments=[
            "PTET is form over substance (should be recharacterized as individual tax)",
            "Credits may not fully offset entity-level tax (rate mismatches)",
            "Complexity of multi-state PTET elections"
        ],
        resolution_strategy="Determine if entity's states offer PTET election. Calculate federal tax savings from avoiding SALT cap (marginal federal rate × state tax in excess of $10K cap). Compare to PTET compliance costs and rate differentials. Make annual PTET election if beneficial. Ensure owners receive credits on individual state returns. Track multi-state PTET elections and composite return interactions. Monitor SALT cap sunset (12/31/2025).",
        entity_scope="S corporations, partnerships, LLCs with individual owners in high-tax states",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="IRS Notice 2020-75",
        effective_date="2018-01-01 (SALT cap effective); 2020-11-09 (IRS blessing of PTET)"
    ),

    DoctrineBlock(
        topic="dormant_commerce_clause_discrimination",
        category=IssueCategory.DORMANT_COMMERCE_CLAUSE,
        keywords=["dormant commerce clause", "discrimination", "pike balancing", "internal consistency", "facial discrimination"],
        conclusion_template=[
            "The dormant Commerce Clause prohibits states from discriminating against or unduly burdening interstate commerce.",
            "Facially discriminatory taxes are subject to strict scrutiny and virtually per se invalid.",
            "Internal consistency test (Wynne): if every state adopted the tax, would it result in discrimination or multiple taxation?"
        ],
        reasoning_framework="""
DORMANT COMMERCE CLAUSE:

CONSTITUTIONAL BASIS:
U.S. Constitution, Article I, Section 8, Clause 3 (Commerce Clause) grants Congress power to regulate interstate commerce.
DORMANT ASPECT: Even without Congressional legislation, states cannot enact laws that discriminate against or unduly burden interstate commerce.

COMPLETE AUTO FOUR-PRONG TEST (nexus, apportionment, discrimination, fair relation):
Prong 3 - NO DISCRIMINATION is core dormant Commerce Clause analysis.

DISCRIMINATION ANALYSIS:

FACIAL DISCRIMINATION:
Tax explicitly treats in-state and out-of-state commerce differently
EXAMPLE: Higher tax rate on out-of-state goods
SCRUTINY: Strict scrutiny - virtually per se invalid unless state can show:
1. Legitimate local purpose, AND
2. No non-discriminatory alternatives available

DISCRIMINATORY EFFECT:
Tax is facially neutral but has discriminatory impact on interstate commerce
EXAMPLE: Tax structure that advantages in-state businesses
TEST: Pike balancing test (see below)

INTERNAL CONSISTENCY TEST:
Comptroller of Treasury v. Wynne, 575 U.S. 542 (2015):
"A tax scheme is internally consistent if it would not result in impermissible discrimination or multiple taxation if every State adopted an identical scheme."

WYNNE CASE:
Maryland imposed income tax on residents' income from all sources, including out-of-state income, but did NOT provide full credit for taxes paid to other states (only credit against county tax, not state tax).
- RESULT: Maryland resident working in another state paid tax to both states on same income
- HOLDING: Internal inconsistency - if every state adopted Maryland's scheme, interstate commerce would be taxed more heavily than intrastate
- Maryland's scheme STRUCK DOWN

PIKE BALANCING TEST:
Pike v. Bruce Church, Inc., 397 U.S. 137 (1970):
Even if not discriminatory, state tax/regulation violates dormant Commerce Clause if:
"The burden imposed on [interstate] commerce is clearly excessive in relation to the putative local benefits."

FACTORS:
1. Magnitude of burden on interstate commerce
2. Importance of local interest
3. Availability of less burdensome alternatives

EXAMPLES OF DISCRIMINATION:

WEST LYNN CREAMERY V. HEALY, 512 U.S. 186 (1994):
Massachusetts imposed tax on all milk dealers but rebated proceeds to in-state dairy farmers.
HELD: Discriminatory - subsidizes in-state producers at expense of out-of-state competitors.

CAMPS NEWFOUND/OWATONNA V. TOWN OF HARRISON, 520 U.S. 564 (1997):
Maine tax exemption for charitable camps serving mostly Maine residents.
HELD: Discriminatory - favors organizations serving in-state beneficiaries.

BACCHUS IMPORTS, LTD. V. DIAS, 468 U.S. 263 (1984):
Hawaii exempted locally produced alcoholic beverages from excise tax.
HELD: Facially discriminatory - protects local industry.

APPORTIONMENT AND DISCRIMINATION:
MeadWestvaco Corp. v. Illinois Dept. of Revenue, 553 U.S. 16 (2008):
Illinois apportioned gain from sale of intangibles using UDITPA business income test.
HELD: Not discriminatory - rational apportionment method.

MODERN APPLICATION TO STATE TAXES:

ECONOMIC NEXUS POST-WAYFAIR:
Courts will examine if economic nexus thresholds are discriminatory:
- Facially neutral: applies equally to in-state and out-of-state sellers
- Effect: may burden small out-of-state sellers disproportionately
- Analysis: Pike balancing - burden vs. state revenue collection interest

MARKET-BASED SOURCING:
Generally not discriminatory:
- Applies equally to in-state and out-of-state taxpayers
- Reflects customer market (neutral principle)

COMBINED REPORTING:
Container Corp. v. Franchise Tax Board, 463 U.S. 159 (1983):
Worldwide combined reporting upheld - not discriminatory, applies equally to all multistate taxpayers.
""",
        key_factors=[
            "Dormant Commerce Clause prohibits state discrimination against interstate commerce",
            "Facial discrimination subject to strict scrutiny (virtually per se invalid)",
            "Internal consistency test (Wynne): would universal adoption discriminate?",
            "Discriminatory effect analyzed under Pike balancing (burden vs. local benefit)",
            "Apportionment must be fair (internal and external consistency)",
            "Economic nexus thresholds are facially neutral post-Wayfair",
            "Market-based sourcing and combined reporting generally upheld"
        ],
        primary_authority=[
            "U.S. Const. art. I, § 8, cl. 3 (Commerce Clause)",
            "Complete Auto Transit, Inc. v. Brady, 430 U.S. 274 (1977)",
            "Comptroller of Treasury v. Wynne, 575 U.S. 542 (2015)",
            "Pike v. Bruce Church, Inc., 397 U.S. 137 (1970)",
            "West Lynn Creamery, Inc. v. Healy, 512 U.S. 186 (1994)",
            "Container Corp. v. Franchise Tax Board, 463 U.S. 159 (1983)"
        ],
        burden_holder="Taxpayer challenging discriminatory tax",
        adversary_position="State will argue tax is facially neutral, internally consistent, and any burden on interstate commerce is outweighed by legitimate local interests (revenue collection, regulatory purpose)",
        counter_arguments=[
            "Tax is facially neutral and applies equally to in-state and out-of-state commerce",
            "Internal consistency test satisfied (universal adoption would not discriminate)",
            "Burden on interstate commerce is minimal or justified by local benefits (Pike balancing)",
            "Apportionment formula is fair and reflects economic activity"
        ],
        resolution_strategy="Analyze if tax is facially discriminatory (explicit preference for in-state). Apply internal consistency test: would universal adoption result in multiple taxation or discrimination? If facially neutral, assess discriminatory effect under Pike balancing (burden vs. local benefit). Review apportionment for internal/external consistency. Challenge discriminatory taxes as violating dormant Commerce Clause.",
        entity_scope="Multistate businesses subject to state taxation",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Comptroller of Treasury v. Wynne, 575 U.S. 542 (2015); Complete Auto Transit, Inc. v. Brady, 430 U.S. 274 (1977)"
    ),

]

# Add indices for fast lookup
DOCTRINE_BY_CATEGORY = {}
for doctrine in DOCTRINE_CACHE:
    if doctrine.category not in DOCTRINE_BY_CATEGORY:
        DOCTRINE_BY_CATEGORY[doctrine.category] = []
    DOCTRINE_BY_CATEGORY[doctrine.category].append(doctrine)

DOCTRINE_BY_KEYWORD = {}
for doctrine in DOCTRINE_CACHE:
    for keyword in doctrine.keywords:
        if keyword not in DOCTRINE_BY_KEYWORD:
            DOCTRINE_BY_KEYWORD[keyword] = []
        DOCTRINE_BY_KEYWORD[keyword].append(doctrine)
