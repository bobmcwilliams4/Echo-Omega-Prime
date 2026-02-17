"""
LM20 Indian Land Engine — Doctrine Cache
TIE Gold Standard doctrine blocks for Indian/tribal land oil & gas operations.

15+ domain-expert doctrine blocks covering:
- Trust vs fee status determination
- 25 CFR Part 212 BIA mineral leasing approval
- Allotted vs tribal mineral interests
- Indian Mineral Development Act (IMDA)
- Indian Mineral Leasing Act (IMLA)
- Fractionation and AIPRA buy-back program
- HEARTH Act (tribal self-governance leasing)
- Sovereign immunity in mineral disputes
- Checkerboard ownership (allotted + fee + tribal)
- 25 CFR Part 169 right-of-way on Indian land
- Split estate on Indian land
- Cobell settlement implications
- Indian Land Consolidation Act (ILCA)
- Tribal environmental review
- ONRR royalty reporting for Indian leases
- Historical allotment and General Allotment Act (Dawes Act)

Author: ECHO OMEGA PRIME
Engine: LM20
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum


class ConfidenceLevel(str, Enum):
    """Confidence stratification."""
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"


class IssueCategory(str, Enum):
    """Indian land issue categories."""
    LEASING = "LEASING"
    TITLE = "TITLE"
    ROYALTY = "ROYALTY"
    ALLOTMENT = "ALLOTMENT"
    TRUST_STATUS = "TRUST_STATUS"
    ENVIRONMENTAL = "ENVIRONMENTAL"
    JURISDICTIONAL = "JURISDICTIONAL"
    FRACTIONATION = "FRACTIONATION"
    UNITIZATION = "UNITIZATION"
    ASSIGNMENT = "ASSIGNMENT"
    SELF_DETERMINATION = "SELF_DETERMINATION"
    CULTURAL_RESOURCE = "CULTURAL_RESOURCE"


@dataclass
class DoctrineBlock:
    """Single doctrine block — expert pre-compiled reasoning."""
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
    confidence: float
    confidence_stratification: ConfidenceLevel
    controlling_precedent: Optional[str] = None
    issue_category: IssueCategory = IssueCategory.LEASING
    disclosure_caveat: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


# ==============================================================================
# DOCTRINE BLOCKS — 15+ DOMAIN-EXPERT BLOCKS
# ==============================================================================

DOCTRINE_TRUST_STATUS = DoctrineBlock(
    topic="Trust vs Fee Status Determination for Indian Minerals",
    keywords=["trust", "restricted", "fee", "status", "land patent", "alienation", "BIA approval", "25 USC 177"],
    conclusion_template=[
        "Indian trust or restricted land cannot be alienated or encumbered without federal approval under 25 USC 177.",
        "Trust status is confirmed by reviewing land patent, historical records, and BIA tract records.",
        "Fee status on formerly allotted land requires documented fee patent issuance or removal from trust."
    ],
    reasoning_framework="""
TRUST STATUS DETERMINATION FRAMEWORK:

1. LEGAL BASIS:
   - 25 USC 177 (Nonintercourse Act): No purchase, grant, lease, or alienation of Indian lands without federal approval
   - 25 USC 2 (Commissioner authority over Indian lands)
   - 25 CFR Part 152 (Trust and Restricted Land)
   - 25 CFR Part 700 (Allotment Regulations)

2. STATUS CATEGORIES:
   a) TRUST LAND: Held by United States in trust for tribe or individual Indian
      - Cannot be alienated without Secretarial approval
      - Exempt from state/local taxation
      - Subject to BIA mineral leasing approval (25 CFR 211/212)

   b) RESTRICTED LAND: Owned by Indian subject to federal restrictions on alienation
      - Similar protections as trust land
      - Cannot be sold/leased without BIA approval
      - Inalienable without federal consent

   c) FEE LAND: No federal restrictions on alienation
      - Subject to state/local law
      - Taxable
      - Can be freely conveyed

3. DETERMINATION PROCESS:
   Step 1: Obtain land patent from BLM records or BIA realty office
   Step 2: Review patent language for trust/restricted designation
   Step 3: Check for subsequent fee patent issuance
   Step 4: Verify current status with BIA Land Title and Records Office (LTRO)
   Step 5: Confirm no removal from trust under 25 USC 5108

4. COMMON ISSUES:
   - Allotted land presumed restricted unless fee patent issued
   - Fee patent may have been issued in error (can be challenged)
   - Mixed ownership: some tracts trust, some fee (checkerboard)
   - State law irrelevant to trust/restricted status determination

5. EVIDENTIARY REQUIREMENTS:
   - Original land patent or certified copy
   - BIA land status records
   - Title opinion from BIA or qualified landman
   - No reliance on county records for trust status
""",
    key_factors=[
        "Land patent language (trust/restricted designation)",
        "BIA Land Title and Records Office (LTRO) verification",
        "Historical allotment records and fee patent issuance",
        "25 USC 177 federal approval requirement",
        "Exemption from state/local taxation",
        "Inalienability without Secretarial consent",
        "Distinction between trust vs restricted vs fee status"
    ],
    primary_authority=[
        "25 USC 177 (Nonintercourse Act)",
        "25 USC 2 (Commissioner authority)",
        "25 CFR Part 152 (Trust and Restricted Land)",
        "25 CFR Part 700 (Allotment Regulations)",
        "United States v. Celestine, 215 U.S. 278 (1909) (restricted land inalienable)"
    ],
    burden_holder="Party claiming fee status bears burden to prove removal from trust",
    adversary_position="County records show fee ownership; state law governs",
    counter_arguments=[
        "County tax records unreliable for trust status — Indian land exempt from taxation",
        "State law irrelevant — federal law controls trust/restricted status",
        "Fee patent required to remove land from trust — mere passage of time insufficient",
        "BIA Land Title and Records Office is authoritative source",
        "United States v. Celestine: restricted land cannot be alienated without federal approval"
    ],
    resolution_strategy="Obtain certified land status from BIA LTRO; rely on federal records, not county records; cite 25 USC 177 Nonintercourse Act.",
    entity_scope="Indian allottees, tribes, oil and gas lessees, title examiners",
    confidence=0.92,
    confidence_stratification=ConfidenceLevel.DEFENSIBLE,
    controlling_precedent="United States v. Celestine, 215 U.S. 278 (1909)",
    issue_category=IssueCategory.TRUST_STATUS,
    disclosure_caveat=None
)


DOCTRINE_BIA_APPROVAL = DoctrineBlock(
    topic="25 CFR Part 212 BIA Mineral Leasing Approval Process",
    keywords=["BIA", "approval", "25 CFR 212", "allotted", "consent", "Secretary", "leasing"],
    conclusion_template=[
        "Oil and gas leases on allotted Indian land require BIA approval under 25 CFR Part 212.",
        "Lessee must obtain landowner consent, environmental clearance, and Secretarial approval before lease is valid.",
        "Lease without BIA approval is void ab initio and provides no legal rights to lessee."
    ],
    reasoning_framework="""
BIA MINERAL LEASING APPROVAL FRAMEWORK (25 CFR PART 212):

1. STATUTORY/REGULATORY BASIS:
   - 25 USC 396a-396g (Indian Mineral Leasing Act of 1938)
   - 25 CFR Part 212 (Leasing of Allotted Lands for Mineral Development)
   - 25 CFR 212.20 (Approval of leases)
   - 25 CFR 212.22 (Consent requirements)

2. APPROVAL REQUIREMENTS:
   a) LANDOWNER CONSENT:
      - Individual allottee: written consent required
      - Multiple owners: majority-in-interest consent (more than 50% undivided interest)
      - Fractionated ownership: BIA may approve with less than 100% consent if in best interest

   b) LEASE TERMS:
      - Must meet minimum standards: 25 CFR 212.7 (bonuses, royalties, terms)
      - Minimum royalty: 16.67% (1/6) of production
      - Primary term: typically 10 years
      - Competitive vs negotiated leasing

   c) ENVIRONMENTAL REVIEW:
      - NEPA compliance (EA or EIS)
      - Cultural resource survey (NHPA Section 106)
      - Tribal environmental review if applicable

   d) SECRETARIAL APPROVAL:
      - BIA Superintendent or Regional Director
      - Discretionary: BIA can reject even with landowner consent if not in best interest
      - Final approval constitutes federal agency action

3. APPROVAL PROCESS TIMELINE:
   Step 1: Lessee negotiates with landowners → consent documents
   Step 2: Submit lease package to BIA Superintendent
   Step 3: BIA reviews title, environmental, compliance → 30-90 days
   Step 4: BIA issues approval decision
   Step 5: Lease recorded with BIA Land Title and Records Office

4. CONSEQUENCES OF LACK OF APPROVAL:
   - Lease void ab initio (from the beginning)
   - No legal right to enter or develop
   - Trespass liability if operations conducted
   - Cannot record lease without BIA approval

5. COMMON PITFALLS:
   - Lessee assumes lease valid upon signing → NO, requires BIA approval
   - County recording of lease does not validate unapproved lease
   - Fractionated ownership: lessee must obtain majority-in-interest consent
   - BIA can reject lease even with 100% landowner consent if terms inadequate
""",
    key_factors=[
        "25 CFR 212.20 Secretarial approval requirement",
        "Landowner consent (majority-in-interest for fractionated tracts)",
        "Minimum lease terms (16.67% royalty, bonus, term)",
        "NEPA and cultural resource clearance",
        "BIA discretion to reject lease",
        "Lease void without approval",
        "Recording with BIA LTRO required"
    ],
    primary_authority=[
        "25 USC 396a (Indian Mineral Leasing Act)",
        "25 CFR 212.20 (Approval of leases)",
        "25 CFR 212.22 (Consent requirements)",
        "25 CFR 212.7 (Lease terms)",
        "Solicitor's Opinion M-37029 (BIA discretion)"
    ],
    burden_holder="Lessee bears burden to obtain BIA approval before commencing operations",
    adversary_position="Lease valid upon signing by landowner; BIA approval ministerial",
    counter_arguments=[
        "25 CFR 212.20 makes approval mandatory, not ministerial",
        "BIA has discretion to reject lease even with landowner consent",
        "Lease without approval is void ab initio — no legal rights",
        "Recording with county does not validate unapproved lease",
        "Trespass liability if operations conducted without BIA approval"
    ],
    resolution_strategy="Always verify BIA approval before relying on lease; obtain certified copy of approved lease from BIA LTRO; never assume county-recorded lease is valid.",
    entity_scope="Oil and gas lessees, landmen, title examiners, Indian landowners",
    confidence=0.95,
    confidence_stratification=ConfidenceLevel.DEFENSIBLE,
    controlling_precedent="Cramer v. United States, 261 U.S. 219 (1923) (Secretarial approval required)",
    issue_category=IssueCategory.LEASING,
    disclosure_caveat=None
)


DOCTRINE_ALLOTTED_VS_TRIBAL = DoctrineBlock(
    topic="Allotted vs Tribal Mineral Interests Distinction",
    keywords=["allotted", "tribal", "individual", "communal", "reservation", "ownership"],
    conclusion_template=[
        "Allotted minerals are owned by individual Indians or their heirs; tribal minerals are owned by the tribe collectively.",
        "Leasing allotted minerals requires BIA approval under 25 CFR Part 212; tribal minerals under 25 CFR Part 211.",
        "Title search must distinguish allotted vs tribal ownership to determine applicable regulatory framework."
    ],
    reasoning_framework="""
ALLOTTED VS TRIBAL MINERAL INTERESTS:

1. HISTORICAL CONTEXT:
   - General Allotment Act of 1887 (Dawes Act): divided communal tribal lands into individual allotments
   - Burke Act of 1906: extended trust period for allotments
   - Indian Reorganization Act of 1934 (IRA): ended allotment policy, allowed tribes to reorganize
   - Many reservations have mixed ownership: allotted + tribal + fee land (checkerboard)

2. OWNERSHIP TYPES:
   a) ALLOTTED MINERALS:
      - Original allotment: 40-160 acres to individual Indian
      - Ownership passes to heirs through probate (25 CFR Part 15)
      - Often fractionated: hundreds of co-owners per tract
      - Individual owners can consent to lease or withhold consent

   b) TRIBAL MINERALS:
      - Owned by tribe collectively
      - Tribal council/business committee controls leasing decisions
      - No individual ownership interests
      - May be located on reservation or former reservation land

3. LEASING FRAMEWORKS:
   a) ALLOTTED MINERALS: 25 CFR Part 212 (Leasing of Allotted Lands)
      - Requires individual landowner consent
      - BIA Superintendent approval
      - Fractionation issues: majority-in-interest required

   b) TRIBAL MINERALS: 25 CFR Part 211 (Leasing of Tribal Lands)
      - Requires tribal council resolution
      - BIA Regional Director approval (higher level than allotted)
      - Tribe has more autonomy under IMDA/HEARTH Act

4. IDENTIFICATION PROCESS:
   Step 1: Obtain BIA tract ownership records
   Step 2: Identify tract type: allotted (individual) vs tribal (communal)
   Step 3: If allotted: obtain ownership interest report from BIA (shows all co-owners and percentages)
   Step 4: If tribal: obtain tribal council resolution authorizing lease
   Step 5: Apply correct regulatory framework (Part 211 vs 212)

5. COMMON ISSUES:
   - Mixed tracts: some allotted, some tribal within same section
   - Heirship complexity: allotted land may have 50+ co-owners
   - Tribal land easier to lease (single decision-maker: tribal council)
   - Allotted land requires consent from majority-in-interest (can be difficult)
   - Fee land interspersed with trust land (checkerboard ownership)
""",
    key_factors=[
        "General Allotment Act of 1887 (Dawes Act) created individual allotments",
        "Allotted land = individual ownership; tribal land = communal ownership",
        "25 CFR Part 212 for allotted; 25 CFR Part 211 for tribal",
        "BIA tract records show allotted vs tribal designation",
        "Heirship complicates allotted land leasing",
        "Tribal leasing more streamlined (tribal council decision)",
        "Checkerboard ownership common on many reservations"
    ],
    primary_authority=[
        "General Allotment Act of 1887, 24 Stat. 388 (Dawes Act)",
        "25 USC 331-334 (Allotment statutes)",
        "25 CFR Part 211 (Leasing of Tribal Lands)",
        "25 CFR Part 212 (Leasing of Allotted Lands)",
        "Indian Reorganization Act of 1934, 25 USC 5101-5129"
    ],
    burden_holder="Lessee bears burden to determine allotted vs tribal ownership and apply correct regulatory framework",
    adversary_position="All Indian land can be leased the same way; no distinction needed",
    counter_arguments=[
        "25 CFR Parts 211 and 212 establish distinct regulatory frameworks",
        "Allotted land requires individual landowner consent; tribal land requires tribal council resolution",
        "BIA approval level differs: Superintendent (allotted) vs Regional Director (tribal)",
        "Leasing wrong type of land voids lease",
        "Title search must identify ownership type from BIA records"
    ],
    resolution_strategy="Always obtain BIA tract ownership records; distinguish allotted vs tribal; apply correct regulatory framework; never assume all Indian land is the same.",
    entity_scope="Landmen, title examiners, oil and gas operators, Indian landowners, tribal governments",
    confidence=0.94,
    confidence_stratification=ConfidenceLevel.DEFENSIBLE,
    controlling_precedent="County of Yakima v. Confederated Tribes and Bands of Yakima Indian Nation, 502 U.S. 251 (1992)",
    issue_category=IssueCategory.ALLOTMENT,
    disclosure_caveat=None
)


DOCTRINE_IMDA = DoctrineBlock(
    topic="Indian Mineral Development Act (IMDA) Alternative Agreements",
    keywords=["IMDA", "25 USC 2101", "alternative agreement", "joint venture", "partnership", "25 CFR 225"],
    conclusion_template=[
        "IMDA (25 USC 2101-2108) allows tribes and allottees to enter alternative mineral agreements beyond traditional leases.",
        "IMDA agreements can be joint ventures, partnerships, or production-sharing agreements with more favorable terms than IMLA leases.",
        "IMDA requires Secretarial approval under 25 CFR Part 225 but offers greater flexibility and potentially higher returns."
    ],
    reasoning_framework="""
INDIAN MINERAL DEVELOPMENT ACT (IMDA) FRAMEWORK:

1. STATUTORY BASIS:
   - 25 USC 2101-2108 (Indian Mineral Development Act of 1982)
   - 25 CFR Part 225 (Mineral Agreements for Developing Indian Mineral Resources)
   - Enacted to overcome limitations of IMLA traditional lease structure

2. KEY FEATURES:
   a) ALTERNATIVE AGREEMENT TYPES:
      - Joint ventures: tribe/allottee as equity partner
      - Production-sharing agreements: tribe receives share of production
      - Service agreements: operator paid fee, tribe keeps minerals
      - Hybrid agreements: combination of structures

   b) ADVANTAGES OVER IMLA LEASES:
      - Higher economic returns: equity participation vs fixed royalty
      - Greater tribal control: approval rights, work program input
      - Risk sharing: operator and tribe share development risk
      - Flexibility: not limited to lease template

   c) APPROVAL PROCESS:
      - Tribal council resolution (for tribal minerals)
      - Individual consent (for allotted minerals)
      - Secretarial approval required (25 CFR 225.20)
      - Must be in best interest of Indian mineral owner

3. COMPARISON: IMLA VS IMDA:

   IMLA (Traditional Lease):
   - Fixed royalty (typically 16.67%)
   - Lessee takes all risk and reward
   - Limited tribal involvement
   - Well-established regulatory framework

   IMDA (Alternative Agreement):
   - Variable returns based on production/profits
   - Shared risk and reward
   - Greater tribal participation and control
   - More complex negotiation and approval

4. APPROVAL REQUIREMENTS (25 CFR 225.20):
   - Agreement must maximize economic benefit
   - Environmental compliance (NEPA, cultural resources)
   - Bonding/financial assurance required
   - Work program and milestones
   - Audit rights for Indian mineral owner

5. COMMON APPLICATIONS:
   - Large-scale tribal mineral development projects
   - Complex multi-phase developments
   - Situations where tribe wants operational control
   - Projects requiring significant capital investment

6. RISKS AND CONSIDERATIONS:
   - More complex than traditional lease
   - Requires sophisticated financial and legal analysis
   - Potential for disputes over profit-sharing calculations
   - BIA approval can take longer than traditional lease
""",
    key_factors=[
        "25 USC 2101-2108 authorizes alternative mineral agreements",
        "Joint ventures and production-sharing allowed",
        "Greater economic returns and tribal control vs IMLA",
        "Secretarial approval required under 25 CFR Part 225",
        "Must maximize economic benefit to Indian mineral owner",
        "More complex negotiation and approval process",
        "Best suited for large-scale or complex developments"
    ],
    primary_authority=[
        "25 USC 2101-2108 (IMDA)",
        "25 CFR Part 225 (IMDA Agreements)",
        "25 USC 396a-396g (IMLA — comparison)",
        "Solicitor's Opinion M-37029 (IMDA approval standards)",
        "H.R. Rep. No. 97-746 (1982) (IMDA legislative history)"
    ],
    burden_holder="Tribe/allottee and operator bear joint burden to demonstrate agreement in best interest and complies with 25 CFR 225",
    adversary_position="Traditional IMLA lease simpler and less risky; IMDA unnecessary complexity",
    counter_arguments=[
        "IMDA offers significantly higher economic returns through equity participation",
        "Greater tribal control over development decisions",
        "25 USC 2101 explicitly authorizes alternative agreements",
        "BIA must approve IMDA if in best interest — cannot arbitrarily reject",
        "Complexity justified by potential for greater value and self-determination"
    ],
    resolution_strategy="For large-scale or complex projects, analyze IMDA vs IMLA economics; prepare detailed agreement with financial projections; obtain tribal/allottee approval; submit to BIA with supporting analysis.",
    entity_scope="Tribes, allottees, oil and gas operators, financial advisors, tribal attorneys",
    confidence=0.88,
    confidence_stratification=ConfidenceLevel.AGGRESSIVE,
    controlling_precedent=None,
    issue_category=IssueCategory.LEASING,
    disclosure_caveat="IMDA agreements more complex; require sophisticated financial and legal analysis; approval timeline may be longer than traditional lease."
)


DOCTRINE_FRACTIONATION = DoctrineBlock(
    topic="Fractionation and AIPRA Buy-Back Program",
    keywords=["fractionation", "heirship", "AIPRA", "buy-back", "probate", "undivided interest", "consolidation"],
    conclusion_template=[
        "Fractionation occurs when allotted land is divided among multiple heirs through probate, creating undivided interests.",
        "Extreme fractionation can result in hundreds of co-owners per tract, making leasing difficult.",
        "AIPRA (25 USC 2201) and the Land Buy-Back Program seek to consolidate fractionated interests."
    ],
    reasoning_framework="""
FRACTIONATION AND CONSOLIDATION FRAMEWORK:

1. FRACTIONATION PROBLEM:
   a) ORIGIN:
      - Allotted land passes through probate to heirs
      - Each generation divides ownership further
      - No partition allowed (land remains undivided)
      - Result: hundreds of co-owners each owning tiny percentages

   b) CONSEQUENCES:
      - Administrative burden: BIA must track thousands of owners
      - Leasing difficulty: majority-in-interest consent required
      - Small payments: individual owners may receive cents per year
      - Economic inefficiency: transaction costs exceed value
      - Example: 40-acre tract with 200 co-owners, largest interest 2.5%

2. LEGAL FRAMEWORK:
   a) PROBATE RULES (25 CFR Part 15):
      - Indian land probate governed by federal law, not state law
      - Heirs inherit undivided interests
      - No forced partition of trust/restricted land
      - BIA must approve any inter vivos transfers

   b) INDIAN LAND CONSOLIDATION ACT (ILCA), 25 USC 2201-2219:
      - Enacted 1983, amended 2000, 2004
      - Prevents further fractionation through escheat rules
      - Authorizes consolidation through purchase, exchange, gift
      - Buy-Back Program funded by Cobell settlement

3. AMERICAN INDIAN PROBATE REFORM ACT (AIPRA), 25 USC 2201:
   - 2004 amendments to ILCA
   - Single-heir rule: certain small interests pass to single heir
   - Prevents creation of new small fractional interests
   - Applies to deaths after June 20, 2006

4. COBELL SETTLEMENT AND BUY-BACK PROGRAM:
   a) COBELL V. SALAZAR:
      - Class action settled 2009 for $3.4 billion
      - $1.9 billion for Land Buy-Back Program
      - DOI purchases fractionated interests from willing sellers

   b) BUY-BACK PROCESS:
      - DOI makes offers to fractionated interest owners
      - Voluntary sales: owner accepts fair market value
      - Purchased interests consolidated into tribal ownership
      - Reduces fractionation and administrative burden

5. LEASING IMPLICATIONS:
   a) MAJORITY-IN-INTEREST REQUIRED:
      - 25 CFR 212.22: need >50% undivided interest consent
      - Fractionated tracts: may need consent from 100+ owners
      - BIA can approve with less than majority if in best interest

   b) STRATEGIES:
      - Target less fractionated tracts
      - Work with tribes to obtain consolidated leases
      - Use IMDA joint ventures to bypass consent issues
      - Wait for Buy-Back Program to consolidate ownership

6. CURRENT STATUS:
   - Fractionation remains major problem on many reservations
   - Buy-Back Program ongoing but slow
   - Tribal land acquisition programs supplement federal efforts
""",
    key_factors=[
        "Probate divides allotted land among heirs (undivided interests)",
        "No partition allowed — land remains undivided",
        "Fractionation creates hundreds of co-owners per tract",
        "Majority-in-interest consent required for leasing (>50%)",
        "AIPRA (25 USC 2201) limits creation of new small interests",
        "Cobell Buy-Back Program consolidates fractionated interests",
        "Leasing highly fractionated tracts extremely difficult"
    ],
    primary_authority=[
        "25 USC 2201-2219 (Indian Land Consolidation Act)",
        "25 USC 2206 (AIPRA single-heir rule)",
        "25 CFR Part 15 (Probate of Indian Estates)",
        "25 CFR 212.22 (Consent requirements for fractionated land)",
        "Cobell v. Salazar Settlement Agreement (2009)"
    ],
    burden_holder="Lessee bears burden to obtain majority-in-interest consent for fractionated tracts",
    adversary_position="Small fractionated interests have no value; owners should be forced to sell",
    counter_arguments=[
        "Trust responsibility: United States must protect individual Indian property rights",
        "No forced partition of trust/restricted land — well-settled law",
        "Buy-Back Program voluntary: cannot force sales",
        "AIPRA prevents future fractionation without eliminating existing interests",
        "Leasing remains possible with majority-in-interest consent"
    ],
    resolution_strategy="For fractionated tracts: obtain BIA ownership interest report; target larger interest owners; seek majority-in-interest consent; consider tribal consolidated lease or IMDA agreement.",
    entity_scope="Landmen, title examiners, fractionated interest owners, tribes, BIA realty officers",
    confidence=0.91,
    confidence_stratification=ConfidenceLevel.DEFENSIBLE,
    controlling_precedent="Hodel v. Irving, 481 U.S. 704 (1987) (invalidated escheat without compensation)",
    issue_category=IssueCategory.FRACTIONATION,
    disclosure_caveat=None
)


DOCTRINE_HEARTH_ACT = DoctrineBlock(
    topic="HEARTH Act Tribal Self-Governance Leasing",
    keywords=["HEARTH", "self-governance", "tribal regulation", "25 USC 415", "waiver", "BIA approval"],
    conclusion_template=[
        "HEARTH Act (25 USC 415(h)) allows tribes to regulate leasing of tribal land without BIA approval.",
        "Tribe must obtain Secretarial approval of tribal leasing regulations; once approved, leases need only tribal approval.",
        "HEARTH Act applies only to tribal land, not allotted land — allotted land still requires BIA approval under 25 CFR Part 212."
    ],
    reasoning_framework="""
HEARTH ACT SELF-GOVERNANCE LEASING FRAMEWORK:

1. STATUTORY BASIS:
   - 25 USC 415(h) (Helping Expedite and Advance Responsible Tribal Homeownership Act of 2012)
   - 25 CFR Part 162 (Leases and Permits)
   - Enacted to promote tribal self-determination and reduce BIA approval delays

2. KEY PROVISIONS:
   a) TRIBAL LEASING REGULATIONS:
      - Tribe adopts leasing regulations for business, residential, or renewable energy leases
      - Submit regulations to Secretary for approval
      - Must meet minimum standards (environmental, cultural, financial)

   b) WAIVER OF SECRETARIAL APPROVAL:
      - Once tribal regulations approved, individual leases need only tribal approval
      - No BIA Superintendent or Regional Director approval required
      - Tribe assumes responsibility for lease compliance

   c) TYPES OF LEASES COVERED:
      - Business leases (including oil and gas)
      - Residential leases
      - Wind and solar energy leases
      - Agricultural leases (if included in tribal regulations)

3. APPROVAL PROCESS:
   Step 1: Tribe develops leasing regulations meeting 25 USC 415(h) standards
   Step 2: Tribal council adopts regulations by resolution
   Step 3: Submit to Secretary (BIA) for review and approval
   Step 4: BIA reviews (must approve or disapprove within 120 days)
   Step 5: Once approved, tribe can approve leases without further BIA involvement

4. ADVANTAGES:
   - Faster lease approval (no BIA bottleneck)
   - Greater tribal control and self-determination
   - Streamlined process encourages economic development
   - Tribe can tailor regulations to local needs

5. LIMITATIONS:
   a) TRIBAL LAND ONLY:
      - Applies only to tribal trust land (communal ownership)
      - Does NOT apply to allotted land (individual Indian ownership)
      - Allotted land still requires BIA approval under 25 CFR Part 212

   b) REGULATORY APPROVAL REQUIRED:
      - Tribe cannot bypass BIA approval without first obtaining approval of tribal regulations
      - BIA retains oversight: can withdraw approval if tribe violates standards

   c) COMPLIANCE RESPONSIBILITY:
      - Tribe assumes liability for environmental/cultural compliance
      - Tribe must have capacity to administer leasing program

6. CURRENT STATUS:
   - Many large tribes have obtained HEARTH Act approval
   - Smaller tribes may lack resources to develop regulations
   - Not universally adopted — traditional BIA approval still common
""",
    key_factors=[
        "25 USC 415(h) authorizes tribal leasing regulations",
        "Waives Secretarial approval for individual leases once tribal regs approved",
        "Applies only to tribal land, not allotted land",
        "Tribe must meet minimum standards (environmental, cultural, financial)",
        "Faster lease approval and greater tribal self-determination",
        "BIA retains oversight and can withdraw approval",
        "Not all tribes have adopted HEARTH Act regulations"
    ],
    primary_authority=[
        "25 USC 415(h) (HEARTH Act)",
        "25 CFR Part 162 (Leases and Permits)",
        "25 CFR 162.013 (HEARTH Act leases)",
        "Pub. L. 112-151 (HEARTH Act legislative history)",
        "BIA guidance on HEARTH Act implementation"
    ],
    burden_holder="Lessee must verify whether tribe has HEARTH Act-approved regulations before relying on tribal approval alone",
    adversary_position="HEARTH Act eliminates all BIA oversight; any tribal approval sufficient",
    counter_arguments=[
        "HEARTH Act requires initial Secretarial approval of tribal regulations",
        "BIA retains oversight: can withdraw approval for non-compliance",
        "Applies only to tribal land — allotted land still requires BIA approval",
        "Not all tribes have adopted HEARTH Act regulations",
        "Lessee must verify tribal regulations approved before relying on tribal approval alone"
    ],
    resolution_strategy="Before relying on tribal approval: (1) verify tribe has HEARTH Act-approved regulations, (2) confirm lease type covered by approved regulations, (3) ensure land is tribal, not allotted, (4) obtain tribal approval documentation.",
    entity_scope="Tribes, lessees, landmen, title examiners, BIA realty officers",
    confidence=0.89,
    confidence_stratification=ConfidenceLevel.AGGRESSIVE,
    controlling_precedent=None,
    issue_category=IssueCategory.SELF_DETERMINATION,
    disclosure_caveat="HEARTH Act adoption varies by tribe; verify tribal regulations approved before assuming BIA approval waived; allotted land never covered by HEARTH Act."
)


DOCTRINE_SOVEREIGN_IMMUNITY = DoctrineBlock(
    topic="Sovereign Immunity in Indian Mineral Disputes",
    keywords=["sovereign immunity", "waiver", "sue", "tribal court", "federal court", "jurisdiction"],
    conclusion_template=[
        "Indian tribes possess sovereign immunity from suit absent express waiver or congressional abrogation.",
        "Sovereign immunity bars lawsuits against tribes in state or federal court without tribal consent.",
        "Limited exceptions: suits against tribal officials for injunctive relief, or where tribe has waived immunity in contract."
    ],
    reasoning_framework="""
TRIBAL SOVEREIGN IMMUNITY FRAMEWORK:

1. LEGAL BASIS:
   - Inherent sovereignty: tribes possess sovereign attributes predating Constitution
   - Doctrine codified in case law: Santa Clara Pueblo v. Martinez, Kiowa Tribe v. Manufacturing Technologies
   - Immunity extends to tribes, tribal entities, and tribal officials (in official capacity)

2. SCOPE OF IMMUNITY:
   a) GENERAL RULE:
      - Tribes immune from suit in federal, state, or tribal court without consent
      - Immunity applies to commercial and governmental activities
      - Immunity exists even for off-reservation commercial activities

   b) EXTENT:
      - Bars damage suits
      - Bars suits for specific performance
      - Bars suits for declaratory relief
      - Bars attachment of tribal property

3. EXCEPTIONS TO IMMUNITY:
   a) EXPRESS WAIVER:
      - Tribe explicitly waives immunity in contract, ordinance, or resolution
      - Waiver must be clear and unambiguous
      - Example: lease states "Tribe waives sovereign immunity for disputes arising under this lease"

   b) CONGRESSIONAL ABROGATION:
      - Congress can abrogate tribal immunity by clear statement
      - Rare: few statutes abrogate immunity
      - Example: certain environmental statutes

   c) EX PARTE YOUNG DOCTRINE:
      - Suits against tribal officials for prospective injunctive relief
      - Official must be acting beyond authority or violating federal law
      - Does not apply to damage suits or suits for money from tribal treasury

4. IMPLICATIONS FOR MINERAL LEASING:
   a) CONTRACT DISPUTES:
      - Without waiver, lessee cannot sue tribe for breach of oil and gas lease
      - Lessee should negotiate explicit waiver in lease agreement
      - Waiver should specify forum (federal court, state court, tribal court, arbitration)

   b) WAIVER LANGUAGE:
      - Effective: "Tribe waives sovereign immunity for all disputes arising under this lease and consents to jurisdiction in U.S. District Court for [District]."
      - Ineffective: "Tribe agrees to comply with all laws" (not express waiver)

   c) ENFORCEMENT:
      - Without waiver, lessee's only remedy may be administrative (BIA)
      - BIA can cancel lease for tribal breach
      - Lessee cannot sue tribe directly

5. TRIBAL COURT JURISDICTION:
   - Tribes have jurisdiction over non-Indians conducting business on Indian land (Montana exceptions)
   - Tribal court may be exclusive forum unless tribe waives immunity and consents to external forum
   - Exhaustion doctrine: must exhaust tribal court remedies before federal court

6. RISK MITIGATION FOR LESSEES:
   - Negotiate explicit waiver of sovereign immunity in lease
   - Specify forum and remedies
   - Consider arbitration clause as alternative to litigation
   - Obtain BIA approval of waiver (BIA may require waiver to approve lease)
""",
    key_factors=[
        "Tribes possess sovereign immunity from suit",
        "Immunity applies in federal, state, and tribal courts",
        "Immunity extends to commercial activities and off-reservation conduct",
        "Waiver must be express and unambiguous",
        "Congress can abrogate immunity by clear statement",
        "Ex parte Young: suits against officials for injunctive relief",
        "Lessees should negotiate immunity waiver in lease agreements"
    ],
    primary_authority=[
        "Kiowa Tribe of Oklahoma v. Manufacturing Technologies, Inc., 523 U.S. 751 (1998)",
        "Santa Clara Pueblo v. Martinez, 436 U.S. 49 (1978)",
        "Oklahoma Tax Comm'n v. Citizen Band Potawatomi Indian Tribe, 498 U.S. 505 (1991)",
        "Michigan v. Bay Mills Indian Community, 572 U.S. 782 (2014)",
        "C & L Enterprises, Inc. v. Citizen Band Potawatomi Tribe, 532 U.S. 411 (2001)"
    ],
    burden_holder="Party seeking to sue tribe bears burden to demonstrate waiver or exception to sovereign immunity",
    adversary_position="Tribe engaged in commercial activity; immunity should not apply to business disputes",
    counter_arguments=[
        "Kiowa Tribe: immunity applies to commercial and governmental activities",
        "Immunity bars suits even for off-reservation commercial conduct",
        "Waiver must be express — cannot be implied from commercial activity",
        "Congress has not abrogated immunity for contract disputes",
        "Lessee's remedy: negotiate waiver before entering lease"
    ],
    resolution_strategy="For mineral leases: always negotiate express waiver of sovereign immunity; specify forum (federal court, arbitration); obtain BIA approval of waiver clause; never assume tribe can be sued without waiver.",
    entity_scope="Oil and gas lessees, landmen, attorneys, tribes, BIA officials",
    confidence=0.93,
    confidence_stratification=ConfidenceLevel.DEFENSIBLE,
    controlling_precedent="Kiowa Tribe of Oklahoma v. Manufacturing Technologies, Inc., 523 U.S. 751 (1998)",
    issue_category=IssueCategory.JURISDICTIONAL,
    disclosure_caveat=None
)


DOCTRINE_CHECKERBOARD = DoctrineBlock(
    topic="Checkerboard Ownership Pattern on Indian Reservations",
    keywords=["checkerboard", "allotted", "fee", "tribal", "mixed", "interspersed", "jurisdiction"],
    conclusion_template=[
        "Checkerboard ownership refers to interspersed trust, restricted, and fee land within reservation boundaries.",
        "Title search on reservations must identify each tract's status: tribal trust, allotted trust, restricted, or fee.",
        "Jurisdiction and regulatory framework vary by land status: federal law for trust/restricted, state law for fee."
    ],
    reasoning_framework="""
CHECKERBOARD OWNERSHIP FRAMEWORK:

1. ORIGIN:
   - General Allotment Act of 1887: divided reservations into individual allotments
   - Surplus land sold to non-Indians as fee land
   - Some allotments later patented in fee (removed from trust)
   - Result: patchwork of trust and fee land within reservation boundaries

2. OWNERSHIP CATEGORIES WITHIN RESERVATIONS:
   a) TRIBAL TRUST LAND:
      - Held by United States in trust for tribe
      - Communal ownership by tribe
      - Subject to federal law and tribal law
      - Exempt from state/local taxation

   b) ALLOTTED TRUST/RESTRICTED LAND:
      - Individual Indian ownership in trust or restricted status
      - Subject to federal law
      - Cannot be alienated without BIA approval
      - Exempt from state/local taxation

   c) FEE LAND (INDIAN-OWNED):
      - Owned in fee by Indian individual
      - Subject to state law
      - Taxable
      - Can be freely conveyed

   d) FEE LAND (NON-INDIAN-OWNED):
      - Owned in fee by non-Indian
      - Subject to state law
      - Taxable
      - Can be freely conveyed

3. JURISDICTIONAL IMPLICATIONS:
   a) MINERAL LEASING:
      - Trust/restricted: BIA approval required (25 CFR 211/212)
      - Fee: state law applies, no BIA approval

   b) TAXATION:
      - Trust/restricted: exempt from state/local taxation
      - Fee: subject to state/local property and severance taxes

   c) ENVIRONMENTAL REGULATION:
      - Trust/restricted: federal and tribal law (NEPA, tribal environmental code)
      - Fee: state environmental law

   d) CULTURAL RESOURCES:
      - Trust/restricted: NHPA Section 106, NAGPRA
      - Fee: state historic preservation law

4. TITLE SEARCH REQUIREMENTS:
   Step 1: Obtain BIA reservation map showing trust vs fee land
   Step 2: For each tract: verify status (tribal trust, allotted trust, restricted, fee)
   Step 3: Identify applicable regulatory framework based on status
   Step 4: If fee land: standard title search from county records
   Step 5: If trust/restricted: BIA land title records, not county records

5. COMMON ISSUES:
   - Leases may cross multiple tracts with different statuses
   - Unitization complicated by mixed trust/fee ownership
   - Right-of-way may cross trust land (requires BIA permit under 25 CFR 169)
   - Surface access agreements needed if surface is different owner than minerals
   - State law applies to fee land even within reservation boundaries

6. MONTANA DOCTRINE (JURISDICTION OVER NON-INDIANS):
   - General rule: tribes lack civil jurisdiction over non-Indians on fee land within reservation
   - Exceptions: (1) consensual relationships (contracts), (2) conduct threatening tribal integrity
   - Affects ability to regulate non-Indian activities on fee land
""",
    key_factors=[
        "Checkerboard: interspersed trust and fee land within reservation",
        "Each tract must be individually identified as tribal, allotted, or fee",
        "Trust/restricted: BIA approval, federal law, tax-exempt",
        "Fee: state law, taxable, no BIA approval",
        "BIA reservation maps and land status records essential",
        "Unitization and right-of-way complicated by mixed ownership",
        "Montana doctrine: limited tribal jurisdiction over non-Indians on fee land"
    ],
    primary_authority=[
        "General Allotment Act of 1887, 24 Stat. 388",
        "Montana v. United States, 450 U.S. 544 (1981) (tribal jurisdiction limits)",
        "County of Yakima v. Confederated Tribes, 502 U.S. 251 (1992) (taxation)",
        "25 CFR Part 152 (Trust and Restricted Land)",
        "25 CFR Part 169 (Rights-of-Way on Indian Land)"
    ],
    burden_holder="Lessee/operator bears burden to identify land status for each tract and comply with applicable law",
    adversary_position="All land within reservation subject to tribal jurisdiction; BIA approval required for all operations",
    counter_arguments=[
        "Montana v. United States: tribes lack general civil jurisdiction over non-Indians on fee land",
        "Fee land subject to state law even within reservation boundaries",
        "Trust vs fee status determined by federal law, not tribal assertion",
        "BIA land records are authoritative source for land status",
        "Operator must comply with applicable law based on land status"
    ],
    resolution_strategy="Obtain BIA reservation map and land status records; identify each tract as tribal, allotted, or fee; apply correct regulatory framework; for fee land within reservation, rely on state law; for trust/restricted, obtain BIA approval.",
    entity_scope="Landmen, title examiners, oil and gas operators, tribes, BIA realty officers",
    confidence=0.90,
    confidence_stratification=ConfidenceLevel.DEFENSIBLE,
    controlling_precedent="Montana v. United States, 450 U.S. 544 (1981)",
    issue_category=IssueCategory.JURISDICTIONAL,
    disclosure_caveat=None
)


DOCTRINE_RIGHT_OF_WAY = DoctrineBlock(
    topic="25 CFR Part 169 Rights-of-Way on Indian Land",
    keywords=["right-of-way", "ROW", "easement", "pipeline", "25 CFR 169", "BIA grant", "access"],
    conclusion_template=[
        "Rights-of-way across Indian trust/restricted land require BIA grant under 25 CFR Part 169.",
        "ROW needed for pipelines, roads, utilities, and other linear facilities crossing Indian land.",
        "BIA grant requires landowner consent, environmental review, and Secretarial approval; unauthorized entry is trespass."
    ],
    reasoning_framework="""
RIGHTS-OF-WAY ON INDIAN LAND FRAMEWORK (25 CFR PART 169):

1. STATUTORY/REGULATORY BASIS:
   - 25 USC 323-328 (Rights-of-Way for Various Purposes)
   - 25 CFR Part 169 (Rights-of-Way Over Indian Land)
   - Revised regulations effective 2016 (replaced 25 CFR Part 169 (2001))

2. WHEN ROW REQUIRED:
   a) ACTIVITIES REQUIRING ROW:
      - Pipelines (oil, gas, water)
      - Roads and highways
      - Utilities (electric, telephone, fiber optic)
      - Railroads
      - Canals and ditches
      - Any linear facility crossing Indian land

   b) DISTINCTION FROM LEASE:
      - Lease: right to use surface for production activities
      - ROW: right to cross land for transportation/transmission
      - Oil and gas lease may not include ROW for pipeline to adjacent land

3. APPROVAL PROCESS (25 CFR 169.107):
   Step 1: Applicant negotiates with Indian landowners
   Step 2: Obtain landowner consent (tribe or individual allottees)
   Step 3: Submit ROW application to BIA
   Step 4: BIA reviews: title, environmental (NEPA), cultural resources (NHPA)
   Step 5: BIA issues ROW grant (or denies application)
   Step 6: ROW recorded with BIA Land Title and Records Office

4. CONSENT REQUIREMENTS:
   a) TRIBAL LAND:
      - Tribal council resolution
      - Tribe may grant ROW without BIA approval if HEARTH Act regulations approved

   b) ALLOTTED LAND:
      - Individual landowner consent
      - Fractionated ownership: majority-in-interest required (>50%)
      - BIA may grant ROW with less than majority if in best interest

5. ROW TERMS:
   a) DURATION:
      - Up to 50 years (can be renewed)
      - Perpetual ROW generally not allowed

   b) COMPENSATION:
      - Fair market value required
      - Appraisal may be required
      - One-time payment or annual rent

   c) BONDING:
      - Performance bond required
      - Amount sufficient to cover restoration/removal costs

6. ENVIRONMENTAL/CULTURAL REVIEW:
   - NEPA compliance (EA or EIS)
   - NHPA Section 106 cultural resource survey
   - Tribal environmental review if applicable
   - Endangered species consultation if applicable

7. OPERATIONAL REQUIREMENTS:
   - Compliance with ROW terms and conditions
   - Restoration of surface after construction
   - Bonding for abandonment/removal
   - Annual reporting may be required

8. CONSEQUENCES OF UNAUTHORIZED ENTRY:
   - Trespass: criminal and civil liability
   - Damages for lost use
   - Injunction to remove facilities
   - No legal right to operate without BIA-granted ROW

9. COMMON ISSUES:
   - Pipeline ROW across multiple allotments: need consent from each tract
   - Existing ROW may have expired: verify current status
   - County-recorded easements on Indian land invalid without BIA grant
   - Surface owner ≠ mineral owner: separate ROW may be needed
""",
    key_factors=[
        "25 CFR Part 169 governs rights-of-way on Indian land",
        "BIA grant required for pipelines, roads, utilities crossing trust/restricted land",
        "Landowner consent (tribal or individual) required",
        "Environmental and cultural review (NEPA, NHPA)",
        "Fair market value compensation required",
        "Unauthorized entry is trespass",
        "County-recorded easements invalid without BIA grant"
    ],
    primary_authority=[
        "25 USC 323-328 (Rights-of-Way statutes)",
        "25 CFR Part 169 (Rights-of-Way regulations)",
        "25 CFR 169.107 (Approval process)",
        "25 CFR 169.3 (Consent requirements)",
        "Bowen v. United States, 570 F.3d 818 (7th Cir. 2009) (trespass damages)"
    ],
    burden_holder="ROW applicant bears burden to obtain BIA grant before entering Indian land",
    adversary_position="Existing pipeline/road constitutes prescriptive easement; no BIA grant needed",
    counter_arguments=[
        "No adverse possession or prescriptive easement against United States (trust land)",
        "25 CFR Part 169 requires BIA grant for all ROW on Indian land",
        "Unauthorized entry is trespass regardless of prior use",
        "County-recorded easement invalid without BIA approval",
        "Trust responsibility: BIA must protect Indian landowner rights"
    ],
    resolution_strategy="Before constructing pipeline or facility crossing Indian land: (1) verify land status (trust vs fee), (2) if trust/restricted, apply for BIA ROW grant under 25 CFR Part 169, (3) obtain landowner consent, (4) complete environmental review, (5) obtain BIA grant before entry.",
    entity_scope="Pipeline operators, utility companies, oil and gas operators, Indian landowners, BIA realty officers",
    confidence=0.92,
    confidence_stratification=ConfidenceLevel.DEFENSIBLE,
    controlling_precedent="Bowen v. United States, 570 F.3d 818 (7th Cir. 2009)",
    issue_category=IssueCategory.LEASING,
    disclosure_caveat=None
)


DOCTRINE_SPLIT_ESTATE = DoctrineBlock(
    topic="Split Estate on Indian Land (Surface vs Mineral Ownership)",
    keywords=["split estate", "surface", "minerals", "accommodation", "dominant estate", "servient"],
    conclusion_template=[
        "Split estate occurs when surface and mineral estates are owned by different parties.",
        "On Indian land, mineral estate is dominant; surface owner must accommodate reasonable mineral development.",
        "Surface access agreement often needed; BIA may require compensation to surface owner even though minerals dominant."
    ],
    reasoning_framework="""
SPLIT ESTATE ON INDIAN LAND FRAMEWORK:

1. SPLIT ESTATE DEFINED:
   - Surface estate: right to use surface of land
   - Mineral estate: right to extract minerals beneath surface
   - Split estate: different owners hold surface vs mineral rights

2. COMMON SCENARIOS ON INDIAN LAND:
   a) TRIBAL MINERALS, ALLOTTED SURFACE:
      - Tribe owns minerals; individual Indian owns surface
      - Common where mineral estate reserved to tribe during allotment

   b) ALLOTTED MINERALS, TRIBAL SURFACE:
      - Individual Indian owns minerals; tribe owns surface
      - Less common but occurs

   c) INDIAN MINERALS, NON-INDIAN SURFACE:
      - Indian trust minerals beneath fee surface
      - Occurs where surface patented in fee but minerals reserved

   d) NON-INDIAN MINERALS, INDIAN SURFACE:
      - Fee minerals beneath Indian trust surface
      - Occurs where minerals severed from surface

3. DOMINANT VS SERVIENT ESTATE:
   a) GENERAL RULE:
      - Mineral estate is dominant estate
      - Surface estate is servient (must accommodate mineral development)
      - Mineral owner has implied right of surface access

   b) ACCOMMODATION DOCTRINE:
      - Mineral owner must use surface reasonably
      - Minimize surface damage
      - Restore surface after operations
      - Compensate surface owner for damages

4. INDIAN LAND SPECIFIC RULES:
   a) BIA TRUST RESPONSIBILITY:
      - BIA must protect both surface and mineral owners
      - BIA may require surface access agreement before approving mineral lease
      - BIA may condition mineral lease on compensation to surface owner

   b) SURFACE DAMAGE PAYMENTS:
      - Even though minerals dominant, BIA often requires compensation to surface owner
      - Payment for lost use, damage to improvements, restoration costs
      - Negotiated between mineral lessee and surface owner, or imposed by BIA

5. APPROVAL PROCESS FOR SPLIT ESTATE DEVELOPMENT:
   Step 1: Mineral lessee obtains mineral lease (25 CFR 211/212)
   Step 2: Negotiate surface access agreement with surface owner
   Step 3: Submit surface agreement to BIA for approval
   Step 4: BIA reviews for fairness and adequacy of compensation
   Step 5: BIA approves mineral lease conditioned on surface agreement
   Step 6: Record both mineral lease and surface agreement with BIA

6. SURFACE ACCESS AGREEMENT TERMS:
   - Compensation for surface use (annual rent or one-time payment)
   - Compensation for crop/improvement damage
   - Restoration requirements
   - Surface use limitations (seasonal restrictions, setbacks, etc.)
   - Indemnification for surface damages
   - Bonding for restoration

7. COMMON DISPUTES:
   - Surface owner refuses access → mineral owner seeks BIA intervention
   - Excessive surface damage → surface owner seeks damages
   - Competing uses → BIA must balance interests
   - Cultural/religious sites on surface → may limit mineral operations

8. RISK MITIGATION:
   - Mineral lessee should negotiate surface access early
   - Include surface compensation in project economics
   - Obtain BIA approval of surface agreement
   - Never assume dominant estate = no compensation required
""",
    key_factors=[
        "Split estate: surface and minerals owned by different parties",
        "Mineral estate dominant; surface must accommodate development",
        "BIA trust responsibility requires protection of both owners",
        "Surface access agreement often required even though minerals dominant",
        "Compensation to surface owner for damages and lost use",
        "BIA may condition mineral lease approval on surface agreement",
        "Accommodation doctrine: reasonable use, minimize damage, restore surface"
    ],
    primary_authority=[
        "25 USC 323 (Rights-of-way for mineral development)",
        "25 CFR 211.7 / 212.7 (Surface protection requirements)",
        "Getty Oil Co. v. Jones, 470 S.W.2d 618 (Tex. 1971) (accommodation doctrine — non-Indian law but persuasive)",
        "Sun Oil Co. v. Whitraker, 483 S.W.2d 808 (Tex. 1972) (accommodation doctrine)",
        "BIA guidance on split estate management"
    ],
    burden_holder="Mineral lessee bears burden to negotiate surface access and obtain BIA approval",
    adversary_position="Minerals are dominant; no surface compensation required",
    counter_arguments=[
        "BIA trust responsibility requires protection of surface owner interests",
        "BIA may condition mineral lease approval on surface agreement",
        "Accommodation doctrine requires reasonable use and surface restoration",
        "Indian land: higher standard of protection than non-Indian split estates",
        "Surface owner cannot unreasonably refuse access, but entitled to compensation"
    ],
    resolution_strategy="For split estate: identify surface and mineral owners; negotiate surface access agreement; compensate surface owner fairly; obtain BIA approval of both mineral lease and surface agreement; never assume dominant estate = no compensation.",
    entity_scope="Oil and gas operators, mineral lessees, surface owners, tribes, BIA realty officers",
    confidence=0.88,
    confidence_stratification=ConfidenceLevel.AGGRESSIVE,
    controlling_precedent="Getty Oil Co. v. Jones, 470 S.W.2d 618 (Tex. 1971) (non-Indian law, persuasive)",
    issue_category=IssueCategory.TITLE,
    disclosure_caveat="BIA practices vary by region; some offices more protective of surface owners than others; surface agreement negotiation can delay mineral development."
)


DOCTRINE_COBELL = DoctrineBlock(
    topic="Cobell Settlement and Implications for Indian Mineral Leasing",
    keywords=["Cobell", "settlement", "accounting", "IIM", "trust mismanagement", "buy-back"],
    conclusion_template=[
        "Cobell v. Salazar class action challenged century of federal mismanagement of Individual Indian Money (IIM) accounts.",
        "2009 settlement: $3.4 billion, including $1.9 billion for Land Buy-Back Program to consolidate fractionated interests.",
        "Settlement improved trust accounting and land records, but structural problems remain."
    ],
    reasoning_framework="""
COBELL SETTLEMENT FRAMEWORK:

1. BACKGROUND:
   - Cobell v. Babbitt filed 1996 by Elouise Cobell (Blackfeet)
   - Alleged federal mismanagement of Individual Indian Money (IIM) accounts
   - IIM accounts: hold royalties, lease payments for individual Indian trust beneficiaries
   - Claims: century of lost records, missing funds, no accounting

2. CLAIMS:
   a) TRUST ACCOUNTING FAILURE:
      - United States as trustee failed to provide accountings
      - IIM account balances inaccurate
      - Records lost or destroyed
      - Billions in royalties unaccounted for

   b) TRUST MISMANAGEMENT:
      - Inadequate systems for tracking funds
      - Commingling of accounts
      - Failure to invest funds
      - Failure to collect royalties owed

3. SETTLEMENT TERMS (2009, approved 2011):
   a) TOTAL: $3.4 billion
      - $1.5 billion for IIM account holders (historical accounting settlement)
      - $1.9 billion for Land Buy-Back Program

   b) HISTORICAL ACCOUNTING SETTLEMENT:
      - Individual payments to IIM account holders
      - Based on account activity
      - No full historical accounting (deemed impossible)

   c) LAND BUY-BACK PROGRAM:
      - DOI purchases fractionated interests from willing sellers
      - Fair market value payments
      - Purchased interests consolidated into tribal ownership
      - Goal: reduce fractionation and administrative burden

4. LAND BUY-BACK PROGRAM DETAILS:
   a) PROCESS:
      - DOI appraises fractionated tracts
      - Offers made to interest owners
      - Voluntary sales: owner accepts or declines
      - Purchased interests transferred to tribe in trust

   b) STATUS (ongoing):
      - Hundreds of thousands of interests purchased
      - Significant reduction in fractionation on some reservations
      - Program continues as funding allows

   c) LEASING IMPLICATIONS:
      - As fractionated interests consolidated, leasing easier
      - Tribal ownership = tribal council decision (vs individual consent)
      - Reduces transaction costs for operators

5. TRUST REFORM:
   a) IMPROVED ACCOUNTING:
      - New IIM account systems
      - Regular account statements
      - Better record-keeping

   b) IMPROVED LAND RECORDS:
      - BIA Land Title and Records Office modernization
      - Better tracking of ownership interests
      - Digitization of historical records

6. ONGOING ISSUES:
   - Fractionation still major problem despite Buy-Back Program
   - Some IIM accounts still have discrepancies
   - Trust management improvements ongoing
   - Structural issues remain (probate, fractionation, underfunding)

7. IMPLICATIONS FOR OIL AND GAS LEASING:
   a) ROYALTY PAYMENTS:
      - Operators pay royalties to ONRR (Office of Natural Resources Revenue)
      - ONRR distributes to IIM accounts
      - Improved accounting = better tracking of payments

   b) LEASING:
      - Buy-Back Program reduces fractionation → easier to obtain consent
      - Tribal ownership post-buyback → tribal council approval (simpler)
      - Operators benefit from reduced fractionation
""",
    key_factors=[
        "Cobell v. Salazar: $3.4 billion settlement for IIM account mismanagement",
        "$1.9 billion Land Buy-Back Program to consolidate fractionated interests",
        "Voluntary purchase of fractionated interests from willing sellers",
        "Purchased interests transferred to tribal ownership",
        "Improved trust accounting and land records systems",
        "Ongoing fractionation reduction improves leasing efficiency",
        "Structural problems remain despite settlement"
    ],
    primary_authority=[
        "Cobell v. Salazar, 679 F.3d 909 (D.C. Cir. 2012) (settlement approval)",
        "Cobell Settlement Agreement (2009)",
        "25 USC 162a (IIM accounts)",
        "Claims Resolution Act of 2010, Pub. L. 111-291 (Cobell settlement)",
        "DOI Land Buy-Back Program guidance"
    ],
    burden_holder="United States (as trustee) bears burden to manage IIM accounts and land records properly",
    adversary_position="Cobell settlement resolved all issues; no ongoing trust mismanagement",
    counter_arguments=[
        "Settlement was compromise, not full remedy for century of mismanagement",
        "Structural problems remain: fractionation, probate, underfunding",
        "Buy-Back Program voluntary: cannot force consolidation",
        "Some IIM accounts still have discrepancies",
        "Trust reform ongoing: not complete"
    ],
    resolution_strategy="For operators: benefit from Buy-Back Program consolidation; work with tribes on post-buyback leasing; verify IIM account accuracy for royalty distributions; recognize improved land records from BIA LTRO.",
    entity_scope="Indian landowners, tribes, oil and gas operators, ONRR, BIA trust officers",
    confidence=0.87,
    confidence_stratification=ConfidenceLevel.AGGRESSIVE,
    controlling_precedent="Cobell v. Salazar, 679 F.3d 909 (D.C. Cir. 2012)",
    issue_category=IssueCategory.TITLE,
    disclosure_caveat="Buy-Back Program ongoing but slow; fractionation remains major issue on many reservations; operators should not assume all fractionation resolved."
)


DOCTRINE_ILCA = DoctrineBlock(
    topic="Indian Land Consolidation Act (ILCA) Anti-Fractionation Rules",
    keywords=["ILCA", "25 USC 2201", "escheat", "single heir", "anti-fractionation", "probate"],
    conclusion_template=[
        "ILCA (25 USC 2201-2219) seeks to prevent further fractionation of allotted land through probate rules.",
        "AIPRA amendments (2004) impose single-heir rule for small interests: prevents creation of new fractional interests below threshold.",
        "Applies to deaths after June 20, 2006; does not eliminate existing fractionation."
    ],
    reasoning_framework="""
INDIAN LAND CONSOLIDATION ACT (ILCA) FRAMEWORK:

1. STATUTORY HISTORY:
   - ILCA enacted 1983 (Pub. L. 97-459)
   - Amended 2000 (Indian Land Consolidation Act Amendments)
   - Amended 2004 (American Indian Probate Reform Act — AIPRA)
   - Purpose: reduce fractionation of allotted Indian land

2. FRACTIONATION PROBLEM (see DOCTRINE_FRACTIONATION):
   - Allotted land passes to multiple heirs through probate
   - Each generation divides ownership further
   - Result: hundreds of co-owners per tract, administrative nightmare

3. ILCA ANTI-FRACTIONATION MECHANISMS:
   a) ESCHEAT PROVISIONS (original 1983 Act):
      - Small interests (<2% and earning <$100/year) escheated to tribe on death
      - HELD UNCONSTITUTIONAL: Hodel v. Irving (1987) — taking without compensation
      - Revised in 2000 amendments

   b) PURCHASE AT PROBATE (2000 amendments):
      - Tribe or co-owners have right to purchase small interests at probate
      - Voluntary: heirs can accept or reject purchase offer
      - Prevents further division if purchase accepted

   c) SINGLE-HEIR RULE (AIPRA 2004):
      - 25 USC 2206: interests below threshold pass to single heir
      - Threshold: <5% of entire tract and earning <$1000/year
      - Applies to deaths after June 20, 2006
      - Prevents creation of new small fractional interests

4. AIPRA SINGLE-HEIR RULE DETAILS:
   a) APPLICABILITY:
      - Applies to individual Indian dying after June 20, 2006
      - Only for interests meeting threshold (<5% and <$1000/year)
      - Does not apply to larger interests (still divided among heirs)

   b) SINGLE-HEIR DETERMINATION:
      - Decedent's will: can name single heir for small interest
      - No will: single heir determined by BIA under 25 CFR Part 15
      - Preference: spouse, then children, then other heirs

   c) EFFECT:
      - Small interest passes undivided to single heir
      - Prevents creation of new fractional interests below threshold
      - Over time, reduces number of very small interests

5. LIMITATIONS:
   - Does not eliminate existing fractionation (only prevents new fractionation)
   - Applies only to small interests (larger interests still divided)
   - Voluntary purchase provisions rarely used
   - Fractionation remains major problem despite ILCA

6. COORDINATION WITH BUY-BACK PROGRAM:
   - Cobell settlement funded Buy-Back Program (see DOCTRINE_COBELL)
   - Buy-Back Program more effective than ILCA at reducing existing fractionation
   - ILCA prevents new fractionation; Buy-Back consolidates existing fractionation

7. LEASING IMPLICATIONS:
   a) FUTURE FRACTIONATION:
      - AIPRA single-heir rule reduces future fractionation
      - Long-term: easier to lease as fractionation reduced

   b) CURRENT FRACTIONATION:
      - ILCA does not help with existing fractionated tracts
      - Lessee still must obtain majority-in-interest consent
      - Buy-Back Program more relevant for current leasing
""",
    key_factors=[
        "ILCA (25 USC 2201-2219) seeks to reduce fractionation",
        "AIPRA single-heir rule (2004): small interests pass to single heir",
        "Threshold: <5% of tract and <$1000/year",
        "Applies to deaths after June 20, 2006",
        "Does not eliminate existing fractionation",
        "Prevents creation of new small fractional interests",
        "Limited impact on current leasing (focuses on future fractionation)"
    ],
    primary_authority=[
        "25 USC 2201-2219 (ILCA)",
        "25 USC 2206 (AIPRA single-heir rule)",
        "Hodel v. Irving, 481 U.S. 704 (1987) (escheat unconstitutional)",
        "Babbitt v. Youpee, 519 U.S. 234 (1997) (revised escheat also unconstitutional)",
        "25 CFR Part 15 (Probate of Indian Estates)"
    ],
    burden_holder="United States (BIA) bears burden to administer AIPRA single-heir rule in probate proceedings",
    adversary_position="ILCA solves fractionation; no further action needed",
    counter_arguments=[
        "ILCA prevents new fractionation but does not eliminate existing fractionation",
        "Existing fractionation remains major problem",
        "Buy-Back Program more effective at consolidating fractionated interests",
        "AIPRA single-heir rule limited to small interests",
        "Leasing fractionated tracts still requires majority-in-interest consent"
    ],
    resolution_strategy="For current leasing: ILCA has limited impact; rely on Buy-Back Program consolidation; obtain majority-in-interest consent for fractionated tracts; AIPRA single-heir rule reduces future fractionation but not immediate concern.",
    entity_scope="Indian landowners, heirs, probate attorneys, BIA realty officers, landmen",
    confidence=0.86,
    confidence_stratification=ConfidenceLevel.AGGRESSIVE,
    controlling_precedent="Hodel v. Irving, 481 U.S. 704 (1987)",
    issue_category=IssueCategory.FRACTIONATION,
    disclosure_caveat="AIPRA single-heir rule applies only to deaths after June 20, 2006 and small interests; existing fractionation unaffected; limited immediate impact on leasing."
)


DOCTRINE_TRIBAL_ENVIRONMENTAL = DoctrineBlock(
    topic="Tribal Environmental Review (Not NEPA) on Indian Land",
    keywords=["tribal environmental", "NEPA", "tribal code", "EPA", "approval", "TAS", "treatment as state"],
    conclusion_template=[
        "NEPA applies to federal actions (BIA mineral lease approval) on Indian land, but tribes may also impose tribal environmental review.",
        "Tribes with Treatment as State (TAS) status under EPA can administer Clean Air Act, Clean Water Act, and other environmental laws.",
        "Operators must comply with both federal (NEPA) and tribal environmental requirements."
    ],
    reasoning_framework="""
TRIBAL ENVIRONMENTAL REVIEW FRAMEWORK:

1. DUAL REGULATORY FRAMEWORK:
   a) FEDERAL ENVIRONMENTAL LAW:
      - NEPA (42 USC 4321): applies to federal agency actions (BIA lease approval)
      - BIA prepares Environmental Assessment (EA) or Environmental Impact Statement (EIS)
      - Clean Air Act, Clean Water Act: EPA authority unless delegated to tribe

   b) TRIBAL ENVIRONMENTAL LAW:
      - Tribes have inherent authority to regulate on-reservation activities
      - Tribal environmental codes govern air, water, waste, cultural resources
      - Tribal permitting and compliance requirements
      - Enforcement through tribal courts or administrative processes

2. NEPA ON INDIAN LAND:
   a) APPLICABILITY:
      - BIA approval of oil and gas lease = federal action
      - Triggers NEPA review (EA or EIS)
      - BIA responsible for NEPA compliance

   b) SCOPE:
      - Environmental Assessment (EA) for routine leases
      - Environmental Impact Statement (EIS) for major actions
      - Cultural resource survey (NHPA Section 106)
      - Tribal consultation required

   c) LIMITATIONS:
      - NEPA does not apply to tribal actions (only federal actions)
      - If tribe approves lease under HEARTH Act (no BIA approval), NEPA does not apply
      - Tribal environmental review may still be required

3. TREATMENT AS STATE (TAS) STATUS:
   a) AUTHORITY:
      - Clean Air Act: 42 USC 7601(d)(2)
      - Clean Water Act: 33 USC 1377(e)
      - Safe Drinking Water Act: 42 USC 300j-11
      - Tribes can apply to EPA for TAS status

   b) EFFECT:
      - Tribe administers federal environmental programs on reservation
      - Tribal permits required (air, water, waste)
      - Tribe enforces federal environmental standards
      - EPA oversight but tribe has primary authority

   c) EXAMPLES:
      - Air quality permits for oil and gas facilities
      - Water discharge permits (NPDES)
      - Underground injection control (Class II wells)

4. TRIBAL ENVIRONMENTAL CODES:
   a) COMMON PROVISIONS:
      - Air quality standards
      - Water quality standards
      - Waste management
      - Cultural resource protection
      - Endangered species protection (tribal analog to ESA)
      - Tribal permitting requirements

   b) ENFORCEMENT:
      - Tribal environmental agency reviews permit applications
      - Compliance inspections
      - Penalties for violations
      - Tribal court jurisdiction

5. OPERATOR COMPLIANCE REQUIREMENTS:
   Step 1: Determine if tribe has TAS status (check with EPA)
   Step 2: Review tribal environmental code (obtain from tribe)
   Step 3: Apply for tribal environmental permits (air, water, waste)
   Step 4: Comply with BIA NEPA review (federal requirement)
   Step 5: Comply with tribal environmental standards (tribal requirement)
   Step 6: Obtain all permits before commencing operations

6. COMMON ISSUES:
   - Dual permitting: federal and tribal permits both required
   - Tribal standards may be more stringent than federal standards
   - Tribes may have unique cultural resource requirements
   - Operators must consult with tribal environmental agency early

7. CULTURAL RESOURCES:
   a) FEDERAL LAW:
      - NHPA Section 106 (54 USC 306108): applies to federal actions
      - NAGPRA (25 USC 3001-3013): applies to human remains, cultural items
      - ARPA (16 USC 470aa): applies to archaeological resources

   b) TRIBAL LAW:
      - Tribal historic preservation codes
      - Tribal cultural resource review
      - May be more protective than federal law
      - Tribal religious sites, sacred areas, traditional cultural properties
""",
    key_factors=[
        "NEPA applies to federal actions (BIA lease approval)",
        "Tribes have inherent environmental regulatory authority",
        "Treatment as State (TAS): tribes administer federal environmental programs",
        "Dual permitting: federal (NEPA, EPA) and tribal (environmental code)",
        "Tribal environmental standards may be more stringent than federal",
        "Cultural resource review: NHPA, NAGPRA, tribal codes",
        "Early consultation with tribal environmental agency essential"
    ],
    primary_authority=[
        "42 USC 4321 (NEPA)",
        "42 USC 7601(d)(2) (Clean Air Act TAS)",
        "33 USC 1377(e) (Clean Water Act TAS)",
        "54 USC 306108 (NHPA Section 106)",
        "25 USC 3001-3013 (NAGPRA)",
        "EPA guidance on TAS status"
    ],
    burden_holder="Operator bears burden to comply with both federal (NEPA) and tribal environmental requirements",
    adversary_position="NEPA compliance sufficient; tribal environmental review unnecessary",
    counter_arguments=[
        "Tribes have inherent authority to regulate on-reservation activities",
        "TAS status: tribes administer federal environmental programs",
        "Tribal environmental codes enforceable in tribal court",
        "Operators must comply with tribal law in addition to federal law",
        "Failure to obtain tribal permits = violation, potential shutdown"
    ],
    resolution_strategy="Before operations: (1) check if tribe has TAS status, (2) obtain tribal environmental code, (3) apply for tribal permits, (4) coordinate with BIA NEPA review, (5) complete cultural resource survey, (6) obtain all federal and tribal approvals.",
    entity_scope="Oil and gas operators, environmental consultants, tribes, BIA, EPA",
    confidence=0.89,
    confidence_stratification=ConfidenceLevel.AGGRESSIVE,
    controlling_precedent="Montana v. United States, 450 U.S. 544 (1981) (tribal regulatory authority)",
    issue_category=IssueCategory.ENVIRONMENTAL,
    disclosure_caveat="Tribal environmental requirements vary by tribe; some tribes have sophisticated environmental programs, others minimal; early consultation essential."
)


DOCTRINE_ONRR_ROYALTY = DoctrineBlock(
    topic="ONRR Royalty Reporting for Indian Oil and Gas Leases",
    keywords=["ONRR", "royalty", "valuation", "reporting", "IIM", "30 CFR 1206", "FOGRMA"],
    conclusion_template=[
        "Oil and gas lessees on Indian land must report production and pay royalties to ONRR (Office of Natural Resources Revenue).",
        "ONRR distributes royalties to Individual Indian Money (IIM) accounts or tribal accounts.",
        "Royalty valuation follows 30 CFR Part 1206; reporting errors can result in penalties and interest."
    ],
    reasoning_framework="""
ONRR ROYALTY REPORTING FRAMEWORK:

1. STATUTORY/REGULATORY BASIS:
   - 30 USC 1701-1757 (Federal Oil and Gas Royalty Management Act — FOGRMA)
   - 30 CFR Part 1210 (Forms and Reports)
   - 30 CFR Part 1206 (Product Valuation)
   - 30 CFR Part 1241 (Penalties)

2. ONRR ROLE:
   - Collects royalties from oil and gas lessees (federal and Indian leases)
   - Audits production and royalty reports
   - Distributes royalties to Indian landowners (via IIM accounts) or tribes
   - Enforces compliance with FOGRMA

3. REPORTING REQUIREMENTS:
   a) MONTHLY REPORTING:
      - Form ONRR-2014 (Oil and Gas Operations Report — OGOR)
      - Due by end of month following production month
      - Reports volumes, disposition, purchaser

   b) ROYALTY PAYMENT:
      - Due by end of month following production month
      - Electronic payment via Pay.gov
      - Late payment = interest and penalties

   c) LESSEE IDENTIFICATION:
      - Payor code: unique identifier for lessee
      - Agreement number: identifies specific lease
      - BIA lease number cross-referenced

4. ROYALTY VALUATION (30 CFR PART 1206):
   a) OIL VALUATION (30 CFR 1206.50-1206.62):
      - Gross proceeds: actual sales price
      - Major portion: higher of gross proceeds or index price
      - Deductions: limited transportation and processing costs

   b) GAS VALUATION (30 CFR 1206.150-1206.178):
      - Gross proceeds or index price
      - Deductions: transportation, processing
      - Complex rules for gas plant products

   c) INDIAN LEASES SPECIFIC:
      - 30 CFR 1206.50(a)(2): Indian oil valuation
      - 30 CFR 1206.150(a)(2): Indian gas valuation
      - May differ from federal lease valuation

5. ROYALTY RATE:
   - Minimum 16.67% (1/6) for Indian leases (25 CFR 212.7)
   - Tribal leases may have higher rates
   - Applies to production value (gross proceeds or index)

6. DISTRIBUTION:
   a) INDIVIDUAL ALLOTTEES:
      - Royalties deposited to IIM accounts
      - ONRR distributes based on ownership percentages
      - IIM account statements show royalty deposits

   b) TRIBAL LEASES:
      - Royalties deposited to tribal account
      - Tribe receives full payment
      - Tribe distributes to tribal members (if applicable)

7. AUDITS AND COMPLIANCE:
   a) ONRR AUDITS:
      - Periodic audits of production and royalty reports
      - Review sales contracts, production records, payment calculations
      - Identify underpayments, reporting errors

   b) PENALTIES:
      - Late payment: interest at Treasury rate + 2%
      - False reporting: civil penalties up to $10,000/day
      - Intentional violations: criminal penalties

   c) ADJUSTMENTS:
      - Amended reports: correct errors
      - Refunds: if overpaid
      - Assessments: if underpaid + interest

8. COMMON ISSUES:
   - Incorrect valuation (using wrong index or gross proceeds)
   - Deductions exceeding allowed amounts
   - Late reporting or payment
   - Failure to report production
   - Ownership percentage errors (fractionated tracts)

9. OPERATOR RESPONSIBILITIES:
   Step 1: Obtain payor code from ONRR
   Step 2: Report production monthly (Form ONRR-2014)
   Step 3: Calculate royalty based on 30 CFR 1206 valuation rules
   Step 4: Pay royalty electronically by deadline
   Step 5: Maintain records for 7 years (audit support)
   Step 6: Respond to ONRR audit requests promptly
""",
    key_factors=[
        "ONRR collects royalties from lessees on Indian leases",
        "Monthly reporting and payment required (Form ONRR-2014)",
        "Royalty valuation follows 30 CFR Part 1206",
        "Minimum royalty 16.67% (1/6) for Indian leases",
        "ONRR distributes to IIM accounts (allotted) or tribal accounts (tribal)",
        "Audits common; penalties for late payment or false reporting",
        "Records must be maintained 7 years"
    ],
    primary_authority=[
        "30 USC 1701-1757 (FOGRMA)",
        "30 CFR Part 1206 (Product Valuation)",
        "30 CFR Part 1210 (Forms and Reports)",
        "30 CFR Part 1241 (Penalties)",
        "25 CFR 212.7 (Minimum royalty for Indian leases)"
    ],
    burden_holder="Lessee bears burden to accurately report production and pay royalties on time",
    adversary_position="Royalty calculation complex; minor errors should be excused",
    counter_arguments=[
        "FOGRMA imposes strict liability for royalty underpayment",
        "Interest accrues on late or underpaid royalties",
        "Penalties up to $10,000/day for false reporting",
        "ONRR audits identify errors years after production",
        "Lessee must maintain accurate records and comply with 30 CFR 1206"
    ],
    resolution_strategy="Ensure accurate royalty reporting: (1) understand 30 CFR 1206 valuation rules, (2) report production monthly on time, (3) pay royalties electronically by deadline, (4) maintain detailed records, (5) respond promptly to ONRR audits, (6) correct errors immediately via amended reports.",
    entity_scope="Oil and gas operators, royalty accountants, ONRR, Indian landowners, tribes",
    confidence=0.91,
    confidence_stratification=ConfidenceLevel.DEFENSIBLE,
    controlling_precedent=None,
    issue_category=IssueCategory.ROYALTY,
    disclosure_caveat=None
)


DOCTRINE_DAWES_ACT = DoctrineBlock(
    topic="Historical Allotment Under General Allotment Act (Dawes Act)",
    keywords=["Dawes Act", "General Allotment Act", "1887", "allotment", "fee patent", "trust period", "Burke Act"],
    conclusion_template=[
        "General Allotment Act of 1887 (Dawes Act) divided tribal lands into individual allotments of 40-160 acres.",
        "Allotments held in trust for 25 years, after which fee patent could be issued removing land from trust.",
        "Many allotments remain in trust today; title search must verify current status (trust vs fee)."
    ],
    reasoning_framework="""
GENERAL ALLOTMENT ACT (DAWES ACT) FRAMEWORK:

1. STATUTORY BASIS:
   - Act of February 8, 1887, 24 Stat. 388 (General Allotment Act)
   - Also known as Dawes Act (after sponsor Sen. Henry Dawes)
   - Codified at 25 USC 331-334

2. PURPOSE (historical):
   - Assimilate Indians into American society
   - Divide communal tribal lands into individual farms
   - "Surplus" land sold to non-Indians for settlement
   - Intended to make Indians self-sufficient farmers

3. ALLOTMENT PROCESS:
   a) ACREAGE:
      - 160 acres to heads of households
      - 80 acres to single adults
      - 40 acres to minors
      - Doubled for grazing land in arid regions

   b) TRUST PERIOD:
      - Land held in trust by United States for 25 years
      - During trust period: inalienable, tax-exempt
      - After 25 years: fee patent issued, land became alienable and taxable

   c) CITIZENSHIP:
      - Allottees became U.S. citizens upon receiving allotment
      - Renounced tribal citizenship (original intent)

4. BURKE ACT OF 1906:
   - Extended trust period beyond 25 years at Secretarial discretion
   - Allowed competency hearings to issue fee patents early
   - Many allottees lost land after receiving premature fee patents

5. CONSEQUENCES:
   a) LAND LOSS:
      - 90+ million acres of Indian land lost between 1887-1934
      - "Surplus" land sold to non-Indians
      - Fee-patented allotments sold for taxes or debts
      - Checkerboard ownership pattern created

   b) FRACTIONATION:
      - Allotted land passed to heirs through probate
      - Each generation divided ownership further
      - Modern fractionation crisis (see DOCTRINE_FRACTIONATION)

   c) CULTURAL DESTRUCTION:
      - Communal land base destroyed
      - Traditional governance disrupted
      - Assimilation policy failed but caused immense harm

6. END OF ALLOTMENT:
   - Indian Reorganization Act of 1934 (IRA) ended allotment policy
   - Remaining tribal lands retained in tribal ownership
   - Allotted lands remained in allotted status (not returned to tribe)
   - IRA allowed tribes to reorganize and adopt constitutions

7. MODERN IMPLICATIONS:
   a) TRUST STATUS:
      - Many allotments still in trust or restricted status
      - Trust period extended indefinitely by Burke Act and subsequent legislation
      - Allotted land remains inalienable without BIA approval

   b) FEE PATENTS:
      - Some allotments received fee patents and left trust
      - Fee-patented land became alienable and taxable
      - Often sold to non-Indians, creating checkerboard ownership

   c) TITLE SEARCH:
      - Must determine if allotted land still in trust or fee-patented
      - BIA land title records are authoritative
      - County records unreliable for trust status

8. VERIFICATION PROCESS:
   Step 1: Identify original allotment from land patent
   Step 2: Check for fee patent issuance (removal from trust)
   Step 3: Verify current status with BIA Land Title and Records Office
   Step 4: If trust/restricted: BIA approval required for lease
   Step 5: If fee: state law applies, no BIA approval

9. HISTORICAL CONTEXT FOR TITLE EXAMINERS:
   - Allotment occurred 1887-1934
   - Trust period originally 25 years
   - Many allotments extended indefinitely in trust
   - Some fee-patented (check BIA records)
   - Probate created fractionated ownership
""",
    key_factors=[
        "Dawes Act (1887) divided tribal lands into individual allotments",
        "40-160 acres per allottee, held in trust for 25 years",
        "Burke Act (1906) extended trust period indefinitely",
        "Many allotments remain in trust today",
        "Fee patents removed some allotments from trust",
        "Checkerboard ownership pattern created",
        "Title search must verify current status (trust vs fee)"
    ],
    primary_authority=[
        "General Allotment Act of 1887, 24 Stat. 388",
        "25 USC 331-334 (Dawes Act codified)",
        "Burke Act of 1906, 34 Stat. 182",
        "Indian Reorganization Act of 1934, 25 USC 5101-5129",
        "Lone Wolf v. Hitchcock, 187 U.S. 553 (1903) (allotment upheld)"
    ],
    burden_holder="Party claiming fee status bears burden to prove fee patent issued",
    adversary_position="Allotment ended in 1934; all allotted land now fee",
    counter_arguments=[
        "Burke Act extended trust period indefinitely for many allotments",
        "Many allotments still in trust or restricted status today",
        "Fee patent required to remove land from trust",
        "BIA land title records show current status",
        "Presumption: allotted land remains in trust unless fee patent proven"
    ],
    resolution_strategy="For allotted land: (1) obtain original allotment patent from BLM or BIA, (2) check for fee patent issuance, (3) verify current status with BIA Land Title and Records Office, (4) if trust, obtain BIA approval for lease; if fee, proceed under state law.",
    entity_scope="Landmen, title examiners, historians, Indian landowners, tribes, BIA realty officers",
    confidence=0.93,
    confidence_stratification=ConfidenceLevel.DEFENSIBLE,
    controlling_precedent="Lone Wolf v. Hitchcock, 187 U.S. 553 (1903)",
    issue_category=IssueCategory.ALLOTMENT,
    disclosure_caveat=None
)


# ==============================================================================
# DOCTRINE COLLECTION
# ==============================================================================

ALL_DOCTRINES: List[DoctrineBlock] = [
    DOCTRINE_TRUST_STATUS,
    DOCTRINE_BIA_APPROVAL,
    DOCTRINE_ALLOTTED_VS_TRIBAL,
    DOCTRINE_IMDA,
    DOCTRINE_FRACTIONATION,
    DOCTRINE_HEARTH_ACT,
    DOCTRINE_SOVEREIGN_IMMUNITY,
    DOCTRINE_CHECKERBOARD,
    DOCTRINE_RIGHT_OF_WAY,
    DOCTRINE_SPLIT_ESTATE,
    DOCTRINE_COBELL,
    DOCTRINE_ILCA,
    DOCTRINE_TRIBAL_ENVIRONMENTAL,
    DOCTRINE_ONRR_ROYALTY,
    DOCTRINE_DAWES_ACT,
]


# ==============================================================================
# UTILITY FUNCTIONS
# ==============================================================================

def get_all_doctrines() -> List[DoctrineBlock]:
    """Return all doctrine blocks."""
    return ALL_DOCTRINES


def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    """Get doctrine block by exact topic match."""
    for doctrine in ALL_DOCTRINES:
        if doctrine.topic.lower() == topic.lower():
            return doctrine
    return None


def search_doctrines(query: str) -> List[DoctrineBlock]:
    """Keyword search across doctrine topics and keywords."""
    query_lower = query.lower()
    results = []
    for doctrine in ALL_DOCTRINES:
        if query_lower in doctrine.topic.lower():
            results.append(doctrine)
            continue
        if any(query_lower in kw.lower() for kw in doctrine.keywords):
            results.append(doctrine)
    return results


def get_doctrine_topics() -> List[str]:
    """Return list of all doctrine topics."""
    return [d.topic for d in ALL_DOCTRINES]


def get_doctrine_count() -> int:
    """Return total number of doctrine blocks."""
    return len(ALL_DOCTRINES)
