"""
LM18 Title Insurance Engine — Doctrine Cache
=============================================
Title insurance doctrine blocks covering underwriting, policy coverage,
commitment review, endorsements, claims, rate regulation, and curative requirements.

Engine: LM18 | Port: 8518 | Domain: title_insurance
Version: 1.0.0 | TIE Gold Standard Component 3
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# ===================================================================
# TIE COMPONENT 3: Doctrine Cache — Issue Categories
# ===================================================================
class IssueCategory(str, Enum):
    """Issue categories for title insurance analysis."""
    POLICY_COVERAGE = "POLICY_COVERAGE"
    COMMITMENT_REVIEW = "COMMITMENT_REVIEW"
    ENDORSEMENT_ANALYSIS = "ENDORSEMENT_ANALYSIS"
    UNDERWRITING_RISK = "UNDERWRITING_RISK"
    MINERAL_EXCLUSION = "MINERAL_EXCLUSION"
    CLAIMS_LOSS = "CLAIMS_LOSS"
    RATE_REGULATION = "RATE_REGULATION"
    SURVEY_EXCEPTION = "SURVEY_EXCEPTION"
    LIEN_ANALYSIS = "LIEN_ANALYSIS"
    GAP_COVERAGE = "GAP_COVERAGE"
    CURATIVE_REQUIREMENTS = "CURATIVE_REQUIREMENTS"
    CLOSING_PROTECTION = "CLOSING_PROTECTION"


class ConfidenceStratification(str, Enum):
    """Confidence tiers for title insurance opinions."""
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"


class PositionZone(str, Enum):
    """Analysis zones — PLANNING, REPORTING, AUDIT. Never blur."""
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"


@dataclass(frozen=True)
class DoctrineBlock:
    """A single doctrine block with complete reasoning framework."""
    topic: str
    keywords: list[str]
    conclusion_templates: list[str]
    reasoning_framework: str
    key_factors: list[str]
    primary_authority: list[str]
    burden_holder: str
    adversary_position: str
    counter_arguments: list[str]
    resolution_strategy: str
    category: IssueCategory
    confidence: ConfidenceStratification
    controlling_precedent: Optional[str] = None
    disclosure_caveat: Optional[str] = None


@dataclass
class DoctrineInteraction:
    """Represents interaction between two doctrine topics."""
    topic_a: str
    topic_b: str
    interaction_type: str  # conflicts, reinforces, modifies, depends_on
    resolution_rule: str
    priority: int = 0


# ===================================================================
# Doctrine Cache — 15+ Title Insurance Doctrine Blocks
# ===================================================================

# Doctrine 1: Title Commitment Review Process
DOCTRINE_COMMITMENT_REVIEW = DoctrineBlock(
    topic="title_commitment_review_process",
    keywords=["commitment", "preliminary report", "pro forma policy", "Schedule A", "Schedule B", "effective date", "insured amount"],
    conclusion_templates=[
        "The title commitment dated {date} shows insurable title subject to the Schedule B exceptions.",
        "Schedule A identifies the proposed insured as {party}, with policy amount of {amount}, effective as of {effective_date}.",
        "All standard pre-printed exceptions in Schedule B-I must be satisfied or removed prior to closing."
    ],
    reasoning_framework="""
Title commitment review follows systematic examination:

1. **Schedule A Analysis** — Verify proposed insured, estate/interest insured, policy amount, effective date
2. **Schedule B-I Requirements** — Identify curative requirements (payoffs, releases, affidavits, surveys)
3. **Schedule B-II Exceptions** — Evaluate exceptions to coverage (easements, liens, restrictions, minerals)
4. **Commitment vs Policy** — Understand commitment is NOT insurance; coverage begins at closing
5. **Effective Date** — Coverage applies only to matters of record as of effective date (gap issues)
6. **Insured Amount** — Confirm policy amount matches purchase price or loan amount
7. **Proposed Insured** — Verify correct legal entity or individual name

Key Questions:
- Are all requirements in Schedule B-I satisfiable before closing?
- Do Schedule B-II exceptions impair the intended use (drilling, pipeline, development)?
- Are mineral interests excepted? If so, surface-only coverage or full mineral estate?
- Are survey exceptions acceptable or is ALTA 9.0 Restrictions/Encroachments endorsement needed?
- Is gap coverage required for the period between effective date and recording?
""",
    key_factors=[
        "Effective date of commitment and recording date gap",
        "Proposed insured matches buyer/borrower legal name",
        "Policy amount matches transaction value",
        "Requirements in Schedule B-I are satisfiable",
        "Exceptions in Schedule B-II do not materially impair use",
        "Mineral interests excepted or insured",
        "Survey exception vs survey-related endorsements",
        "Standard exceptions vs special exceptions",
    ],
    primary_authority=[
        "Texas Insurance Code Title 11 (Title Insurance)",
        "28 TAC §9.4 (Commitment for Title Insurance)",
        "ALTA Commitment for Title Insurance (2016 Form)",
        "Stewart Title Guaranty Company v. Aiello, 941 S.W.2d 68 (Tex. 1997) — commitment is not insurance",
    ],
    burden_holder="Title company must identify all matters affecting title; buyer must identify unacceptable exceptions",
    adversary_position="Buyer may argue undisclosed defects create liability; title company asserts commitment is preliminary only",
    counter_arguments=[
        "Commitment expressly states it is not insurance and coverage begins at closing",
        "Schedule B exceptions are identified for buyer's review and objection",
        "Requirements must be satisfied; failure to close means no coverage",
        "Buyer has opportunity to review and object to exceptions before closing",
        "Gap coverage available via ALTA 3.1 Zoning endorsement or extended coverage",
    ],
    resolution_strategy="Review commitment systematically: Schedule A for accuracy, Schedule B-I for curative requirements, Schedule B-II for acceptable exceptions. Negotiate removal of unacceptable exceptions or obtain endorsements.",
    category=IssueCategory.COMMITMENT_REVIEW,
    confidence=ConfidenceStratification.DEFENSIBLE,
    controlling_precedent="Stewart Title Guaranty v. Aiello — commitment is not insurance policy",
    disclosure_caveat="Commitment review must occur before closing deadline; exceptions not objected to are deemed accepted"
)

# Doctrine 2: Schedule A Requirements
DOCTRINE_SCHEDULE_A = DoctrineBlock(
    topic="schedule_a_requirements",
    keywords=["Schedule A", "proposed insured", "estate insured", "policy amount", "effective date", "land description"],
    conclusion_templates=[
        "Schedule A must accurately identify the proposed insured, estate/interest insured, and land description.",
        "Policy amount of {amount} should match purchase price for owner's policy or loan amount for lender's policy.",
        "Effective date establishes the search cutoff; matters recorded after this date are not covered unless gap endorsement issued."
    ],
    reasoning_framework="""
Schedule A is the core identification section of the title commitment:

1. **Effective Date** — Date/time as of which title search was conducted; later recordings not covered
2. **Proposed Insured** — Must match exactly the name of buyer (owner's policy) or lender (loan policy)
3. **Policy Amount** — Owner's policy = purchase price; loan policy = loan amount (not combined)
4. **Estate/Interest** — Fee simple, leasehold, easement, mineral estate, etc.
5. **Land Description** — Legal description from deed or survey; must match exactly
6. **Vesting** — How title will vest (individual, joint tenants, community property, LLC, etc.)

Common Defects:
- Proposed insured name misspelled or incorrect entity type (LLC vs Corporation)
- Policy amount insufficient (purchase price increased after commitment issued)
- Land description does not match deed or includes wrong survey
- Estate insured unclear (surface only? minerals included?)
- Effective date too old (gap between effective date and closing creates uninsured period)

Underwriting Rule: Schedule A must be 100% accurate; errors void coverage.
""",
    key_factors=[
        "Proposed insured name matches buyer/borrower exactly",
        "Estate/interest insured is correctly identified (fee simple, mineral, surface, leasehold)",
        "Land description matches deed and survey",
        "Policy amount matches transaction value",
        "Effective date is recent (within 30 days of closing preferred)",
        "Vesting matches buyer's intent (LLC vs personal, joint vs tenants in common)",
    ],
    primary_authority=[
        "28 TAC §9.4(b) — Schedule A content requirements",
        "ALTA Commitment Form (2016) — Schedule A format",
        "Texas Insurance Code §2703.151 — policy must accurately describe land",
    ],
    burden_holder="Title company must ensure Schedule A accuracy; proposed insured must provide correct entity information",
    adversary_position="Insured may claim Schedule A error voids coverage; title company asserts substantial compliance",
    counter_arguments=[
        "Minor typographical errors that do not affect identification are immaterial",
        "Proposed insured had opportunity to review commitment before closing",
        "Policy amount can be increased via endorsement if purchase price increases",
        "Land description errors discovered post-closing may be corrected by reformation",
    ],
    resolution_strategy="Verify every field in Schedule A before closing: proposed insured spelling, entity type, land description against survey, policy amount against HUD-1/Closing Disclosure, effective date recency.",
    category=IssueCategory.COMMITMENT_REVIEW,
    confidence=ConfidenceStratification.DEFENSIBLE,
    controlling_precedent="Hare v. Wendler, 949 S.W.2d 125 (Tex. App. 1997) — incorrect legal description in policy"
)

# Doctrine 3: Schedule B-I Requirements
DOCTRINE_SCHEDULE_B1 = DoctrineBlock(
    topic="schedule_b1_requirements",
    keywords=["Schedule B-I", "requirements", "curative", "payoff", "release", "affidavit", "survey", "closing conditions"],
    conclusion_templates=[
        "Schedule B-I identifies {count} requirements that must be satisfied before the policy will be issued.",
        "Requirements include payoffs of existing liens totaling {amount}, delivery of recorded instruments, and affidavits.",
        "All Schedule B-I requirements must be completed; failure to satisfy any requirement means no policy issues."
    ],
    reasoning_framework="""
Schedule B-I lists pre-closing requirements that MUST be satisfied for policy issuance:

**Common Requirements:**
1. **Lien Payoffs** — Mortgages, deeds of trust, mechanic's liens, tax liens to be paid at closing
2. **Releases** — Recorded releases of satisfied liens, easements, restrictions
3. **Affidavits** — Non-foreign affidavit, marital status, ownership and gap, identity
4. **Surveys** — Current ALTA/NSPS survey showing improvements, easements, encroachments
5. **Probate Documents** — Death certificates, probate orders, heirship affidavits
6. **Entity Documents** — LLC resolutions, corporate resolutions, authority to sell/buy
7. **Curative Instruments** — Corrective deeds, ratifications, amendments to clear title defects
8. **Estoppel Certificates** — HOA, lease, mortgage estoppels confirming no defaults

**Satisfaction Process:**
- Each requirement numbered and described in detail
- Title company verifies satisfaction before closing
- Recording of releases, deeds, assignments occurs at closing
- Policy issues ONLY after all requirements met

**Failure to Satisfy = No Policy:**
If even one requirement is not satisfied, the commitment expires and no coverage attaches.
This is an absolute condition precedent to coverage.
""",
    key_factors=[
        "All requirements are satisfiable within closing timeline",
        "Payoff amounts are accurate and include per diem interest",
        "Releases will be recorded simultaneously with new deed/deed of trust",
        "Affidavits are properly executed and notarized",
        "Survey is acceptable to title company and shows no defects",
        "Entity authority documents are valid and current",
        "Curative instruments effectively cure the identified defects",
    ],
    primary_authority=[
        "28 TAC §9.4(c) — Schedule B-I requirements",
        "ALTA Commitment Form (2016) — Requirements section",
        "Texas Insurance Code §2703.052 — conditions precedent to policy issuance",
    ],
    burden_holder="Seller/borrower must satisfy requirements; title company verifies satisfaction",
    adversary_position="Buyer may argue requirement was substantially satisfied; title company asserts strict compliance required",
    counter_arguments=[
        "Commitment expressly conditions policy issuance on satisfaction of all requirements",
        "Partial satisfaction does not trigger coverage; all-or-nothing rule applies",
        "Title company has no duty to issue policy if requirements not met",
        "Buyer accepted commitment with requirements listed and had opportunity to object",
    ],
    resolution_strategy="Systematically address each requirement: obtain payoff statements, coordinate recordings, prepare affidavits, order survey, collect entity documents. Verify satisfaction before closing.",
    category=IssueCategory.COMMITMENT_REVIEW,
    confidence=ConfidenceStratification.DEFENSIBLE,
    controlling_precedent="Forbau v. Aetna Life Ins. Co., 876 S.W.2d 132 (Tex. 1994) — failure to satisfy requirement = no coverage"
)

# Doctrine 4: Schedule B-II Exceptions
DOCTRINE_SCHEDULE_B2 = DoctrineBlock(
    topic="schedule_b2_exceptions",
    keywords=["Schedule B-II", "exceptions", "easements", "restrictions", "liens", "minerals reserved", "survey exception", "gap"],
    conclusion_templates=[
        "Schedule B-II lists {count} exceptions that will NOT be covered by the policy.",
        "Exception {number} for {description} is acceptable for the intended use of {use}.",
        "Mineral reservation in Exception {number} excludes coverage for subsurface rights; surface estate only insured."
    ],
    reasoning_framework="""
Schedule B-II exceptions are matters EXCLUDED from coverage:

**Standard Exceptions:**
1. **Taxes** — Current year taxes not yet due and payable
2. **Mineral Reservations** — Prior severances of mineral estate
3. **Easements** — Utility, access, pipeline, drainage easements of record
4. **Restrictions** — Subdivision, HOA, use restrictions
5. **Survey Defects** — "Shortages in area, encroachments, overlaps, boundary disputes as would be disclosed by survey"
6. **Unrecorded Liens** — Mechanic's liens, tax liens not yet filed
7. **Rights of Parties in Possession** — Tenants, adverse possessors not shown by record

**Special Exceptions:**
- Specific recorded instruments (deeds, easements, liens, UCC filings)
- Litigation (lis pendens, bankruptcy, foreclosure)
- Judgments and federal tax liens against prior owners

**Evaluating Exceptions:**
- Do exceptions impair intended use? (Drilling, building, selling, financing)
- Are mineral interests excepted? (Critical for oil/gas transactions)
- Are survey exceptions acceptable or must ALTA 9 endorsement be obtained?
- Can exceptions be removed via curative action or negotiation?

**Negotiation Strategy:**
Buyer may object to unacceptable exceptions and require seller to cure or remove.
If not curable, buyer may terminate or accept with reduced price.
""",
    key_factors=[
        "Impact of exceptions on intended use (drilling, development, financing)",
        "Mineral estate excepted vs surface-only coverage",
        "Survey exception vs ALTA 9 endorsement",
        "Utility easements location and interference with improvements",
        "Restrictive covenants compatibility with intended use",
        "Outstanding liens that must be paid/released",
        "Gap coverage for period between effective date and recording",
    ],
    primary_authority=[
        "28 TAC §9.4(d) — Schedule B-II exceptions",
        "ALTA Owner's Policy (2006) — Covered Risks vs Exclusions",
        "Texas Insurance Code §2703.151(b) — exceptions to coverage",
    ],
    burden_holder="Title company lists exceptions; buyer evaluates acceptability and objects if necessary",
    adversary_position="Buyer argues exception was not disclosed or impairs marketability; title company asserts proper disclosure",
    counter_arguments=[
        "All exceptions were listed in commitment and buyer had opportunity to object",
        "Exceptions are matters of public record; buyer had constructive notice",
        "Policy expressly excepts listed matters; no coverage for excepted items",
        "Buyer can obtain endorsements to delete or modify exceptions (for additional premium)",
    ],
    resolution_strategy="Review each exception for impact on use; object to unacceptable exceptions; negotiate removal, obtain endorsements (ALTA 9, 8.1, 19), or accept with price adjustment.",
    category=IssueCategory.COMMITMENT_REVIEW,
    confidence=ConfidenceStratification.DEFENSIBLE,
    controlling_precedent="Stonewall Ins. Co. v. Self, 849 S.W.2d 534 (Tex. App. 1993) — excepted matters not covered"
)

# Doctrine 5: Owner's vs Lender's Policy
DOCTRINE_OWNERS_VS_LENDERS = DoctrineBlock(
    topic="owners_vs_lenders_policy",
    keywords=["owner's policy", "lender's policy", "loan policy", "simultaneous issue", "coverage differences", "insured parties"],
    conclusion_templates=[
        "Owner's policy insures {buyer} against title defects; coverage amount {purchase_price}.",
        "Lender's policy insures {lender} against loss on the loan; coverage amount {loan_amount}.",
        "Simultaneous issue discount applies when both policies issued at same closing."
    ],
    reasoning_framework="""
Owner's vs Lender's Policy — Critical Differences:

**Owner's Policy:**
- **Insured:** Buyer of property (individual, LLC, corporation, etc.)
- **Coverage Amount:** Purchase price (not market value; static amount)
- **Duration:** Permanent; covers insured and heirs/successors as long as they hold interest
- **Covered Risks:** Defects in title, liens, encumbrances, unmarketability, lack of access
- **Enhanced Coverage:** ALTA Homeowner's Policy (residential) adds additional coverages
- **Premium:** One-time premium at closing based on purchase price

**Lender's Policy:**
- **Insured:** Mortgage lender (bank, credit union, private lender)
- **Coverage Amount:** Loan amount (decreases as loan paid down? No, static at issuance amount)
- **Duration:** Until loan paid off or foreclosed; does NOT continue after payoff
- **Covered Risks:** Same as owner's policy but protects lender's security interest
- **Assignment:** Transfers to subsequent holders of the loan (MERS, servicers, investors)
- **Premium:** Based on loan amount; simultaneous issue discount if owner's policy also issued

**Simultaneous Issue Discount:**
When both policies issued at same closing, lender's policy receives ~60% discount.
Buyer typically pays for both policies in residential; commercial varies by negotiation.

**Rate Regulation (Texas):**
Promulgated rates by Texas Department of Insurance; no deviation allowed.
Basic Rate Manual sets premium tables; liability coverage and simultaneous issue discounts.

**Key Question:** Who pays for each policy?
- Owner's policy: Buyer pays (residential custom); commercial negotiable
- Lender's policy: Buyer pays (required by lender as loan condition)
""",
    key_factors=[
        "Owner's policy insures buyer; lender's policy insures lender",
        "Owner's policy permanent; lender's policy expires at loan payoff",
        "Simultaneous issue discount reduces lender's policy premium",
        "Rates are promulgated by TDI; no negotiation allowed",
        "Enhanced coverage available for residential (ALTA Homeowner's Policy)",
        "Buyer typically pays both premiums in residential transactions",
    ],
    primary_authority=[
        "Texas Insurance Code §2703.051 — title insurance policies",
        "28 TAC §9.1 — promulgated rates for title insurance",
        "ALTA Owner's Policy (2006) vs ALTA Loan Policy (2006)",
        "TDI Basic Rate Manual — premium calculation tables",
    ],
    burden_holder="Lender requires loan policy as condition of financing; buyer elects whether to purchase owner's policy",
    adversary_position="Buyer may argue lender should pay for lender's policy; lender asserts buyer pays per custom",
    counter_arguments=[
        "Loan policy protects lender's interest, not buyer's personal interest",
        "Owner's policy is optional but highly recommended for buyer's protection",
        "Simultaneous issue discount incentivizes buyer to purchase both policies",
        "Custom and practice in residential transactions is buyer pays both premiums",
    ],
    resolution_strategy="Explain coverage differences to buyer; recommend owner's policy for permanent protection; negotiate who pays in commercial transactions; apply simultaneous issue discount.",
    category=IssueCategory.POLICY_COVERAGE,
    confidence=ConfidenceStratification.DEFENSIBLE,
    controlling_precedent="Mortgage Elec. Registration Sys. v. Southwest Homes, 301 S.W.3d 1 (Tex. 2009) — MERS as nominee"
)

# Doctrine 6: ALTA Endorsements (8.1, 9, 19)
DOCTRINE_ALTA_ENDORSEMENTS = DoctrineBlock(
    topic="alta_endorsements",
    keywords=["ALTA endorsement", "8.1 environmental", "9 restrictions", "19 contiguity", "coverage modification", "additional premium"],
    conclusion_templates=[
        "ALTA 8.1 Environmental Protection endorsement adds coverage for environmental liens and cleanup costs.",
        "ALTA 9 Restrictions/Encroachments/Minerals endorsement deletes standard survey exception and insures improvements location.",
        "ALTA 19 Contiguity endorsement insures that described parcels are contiguous with no gaps."
    ],
    reasoning_framework="""
ALTA Endorsements — Enhanced Coverage Modifications:

**ALTA 8.1 Environmental Protection Lien:**
- Insures against loss from environmental liens (CERCLA, state Superfund liens)
- Covers cleanup costs imposed due to prior contamination
- Does NOT cover contamination by insured; only pre-existing contamination
- Critical for commercial/industrial properties with contamination risk

**ALTA 9 Comprehensive (or Short Form 9.x):**
- Deletes standard survey exception from Schedule B-II
- Insures improvements are located on land (no encroachments off land)
- Insures no encroachments onto land that violate restrictions or building lines
- Insures no violations of recorded subdivision restrictions/building setbacks
- Requires current ALTA/NSPS survey acceptable to title company
- Sub-types: 9.1 (no survey), 9.2 (with survey), 9.5 (minerals), 9.11 (single tax lot)

**ALTA 19 Contiguity:**
- Insures that described parcels are contiguous (no gaps, no strips between)
- Critical for ranch/farm assemblages, large commercial tracts, pipeline routes
- Requires survey showing contiguity or acceptable legal descriptions
- Often combined with ALTA 19.1 (location and contiguity)

**Other Common Endorsements:**
- ALTA 2 (Access) — insures physical and legal access to public street
- ALTA 3.1 (Zoning) — insures current zoning classification and compliance
- ALTA 4.1 (Condominium) — special coverage for condo units
- ALTA 5.1 (Planned Unit Development) — PUD coverage
- ALTA 6.2 (Variable Rate Mortgage) — insures changing loan amounts
- ALTA 7 (Manufactured Housing) — mobile home unit coverage
- ALTA 22 (Location) — insures street address matches legal description

**Premium Calculation:**
Most endorsements add 5-10% to basic premium; some flat fee.
Promulgated by TDI; no negotiation.

**Underwriting Requirements:**
Each endorsement has specific underwriting criteria (survey, affidavits, inspection, search depth).
Title company may decline endorsement if risk not acceptable.
""",
    key_factors=[
        "ALTA 8.1 requires environmental search and Phase I ESA review",
        "ALTA 9 requires current ALTA/NSPS survey showing improvements and easements",
        "ALTA 19 requires survey or legal description analysis confirming contiguity",
        "Endorsements add premium (5-25% of basic premium depending on type)",
        "Title company may decline endorsement if underwriting risk too high",
        "Oil & gas transactions frequently require ALTA 9.5 (minerals), 19 (contiguity), 8.1 (environmental)",
    ],
    primary_authority=[
        "28 TAC §9.8 — endorsements to title insurance policies",
        "ALTA Endorsement Forms (2006, 2016, 2021 versions)",
        "TDI Rate Manual — endorsement premium schedules",
    ],
    burden_holder="Insured requests endorsement; title company underwrites and approves or declines",
    adversary_position="Insured may argue endorsement should be included without additional premium; title company asserts promulgated rate",
    counter_arguments=[
        "Endorsements modify coverage beyond standard policy; additional premium justified",
        "Underwriting requirements (survey, environmental search) add cost and risk",
        "Promulgated rates set by TDI; title company cannot waive or discount",
        "Insured can decline endorsement if cost not justified by risk",
    ],
    resolution_strategy="Identify endorsements needed for transaction type (commercial, residential, oil/gas); obtain survey and environmental reports; calculate total premium; obtain title company approval.",
    category=IssueCategory.ENDORSEMENT_ANALYSIS,
    confidence=ConfidenceStratification.DEFENSIBLE,
    controlling_precedent="28 TAC §9.8 mandates promulgated endorsement forms and rates"
)

# Doctrine 7: Title Plant and Abstract Search
DOCTRINE_TITLE_PLANT_SEARCH = DoctrineBlock(
    topic="title_plant_abstract_search",
    keywords=["title plant", "abstract", "chain of title", "search period", "root of title", "starter update", "full certification"],
    conclusion_templates=[
        "Title search conducted for {years} years back from effective date using {company} title plant.",
        "Abstract of title certified by {abstractor} shows chain of title from {root_year} to present.",
        "No defects or encumbrances found except those listed in Schedule B-II."
    ],
    reasoning_framework="""
Title Plant and Abstract Search — Chain of Title Examination:

**Title Plant:**
- Geographically-indexed database of all recorded instruments affecting land in a county
- Maintained by title company or abstract company (private, not public record)
- Updated daily from county recorder's office
- Provides faster search than county records
- Texas law requires title plants for certain underwriting (28 TAC §9.3)

**Abstract of Title:**
- Written summary of all recorded instruments affecting a property
- Chronological listing: deeds, mortgages, releases, judgments, liens, easements
- Prepared by licensed abstractor or title company
- "Certified abstract" = abstractor certifies completeness and accuracy
- Used as basis for attorney's title opinion or title insurance commitment

**Search Period:**
- Standard: 50+ years (establishes marketable root of title)
- Texas: 50 years for mineral title, 30+ years for surface title
- Commercial: 30-50 years or to root of title (whichever is deeper)
- Residential: 30 years or to prior owner's policy (starter/update)

**Root of Title:**
- Transaction establishing clear starting point (federal patent, prior owner's policy, marketable deed)
- All subsequent conveyances must chain back to root without gaps or defects

**Starter vs Update:**
- **Starter:** Search from root of title (50+ years) — full examination
- **Update:** Search from date of prior title policy to present — faster, cheaper
- Update relies on prior title company's search; only examines gap period

**Defect Identification:**
- Gaps in chain (missing conveyances, wild deeds)
- Defective conveyances (lack of authority, forgery, improper execution)
- Outstanding liens (mortgages, tax liens, judgment liens, UCC filings)
- Easements and restrictions affecting use
- Mineral reservations and royalty interests
- Probate issues (deaths without probate, heirship questions)
""",
    key_factors=[
        "Title plant current and complete (updated daily from county records)",
        "Search depth adequate for transaction type (50 years minerals, 30 years surface)",
        "Root of title established (federal patent, prior policy, marketable deed 50+ years ago)",
        "All conveyances chain properly with no gaps or wild deeds",
        "All liens and encumbrances identified and listed in Schedule B",
        "Mineral and royalty interests accounted for",
        "Probate and heirship issues resolved",
    ],
    primary_authority=[
        "28 TAC §9.3 — title plant requirements for title insurance",
        "Texas Property Code §13.001 — marketable title (50-year root for minerals)",
        "Texas Standards for Attorney's Title Examination — search standards",
    ],
    burden_holder="Title company conducts search and identifies defects; buyer evaluates whether title is acceptable",
    adversary_position="Buyer may argue search was inadequate and missed defects; title company asserts search met standards",
    counter_arguments=[
        "Title plant maintained according to TDI regulations and updated daily",
        "Search period met industry standards for transaction type",
        "All recorded instruments affecting title were examined and listed",
        "Unrecorded matters (fraud, forgery, unrecorded easements) covered by policy if not excepted",
    ],
    resolution_strategy="Use title plant for efficient search; abstract of title for complex transactions; search to root of title or 50 years for minerals; identify and list all defects in Schedule B.",
    category=IssueCategory.UNDERWRITING_RISK,
    confidence=ConfidenceStratification.DEFENSIBLE,
    controlling_precedent="Texas Property Code §13.001 — 50-year root of title for minerals"
)

# Doctrine 8: Chain of Title Examination for Underwriting
DOCTRINE_CHAIN_OF_TITLE_UNDERWRITING = DoctrineBlock(
    topic="chain_of_title_examination_underwriting",
    keywords=["chain of title", "underwriting", "wild deed", "gap in title", "defective conveyance", "marketable title", "root"],
    conclusion_templates=[
        "Chain of title is complete and unbroken from {root_year} root deed to present vesting in {current_owner}.",
        "Gap in chain identified: Deed from {grantor} to {grantee} dated {date} not recorded until {record_date}, creating {days}-day gap.",
        "Wild deed detected: {deed_description} does not connect to main chain; curative required."
    ],
    reasoning_framework="""
Chain of Title Examination — Underwriting Analysis:

**Perfect Chain:**
1. Each conveyance out of prior owner is recorded before next conveyance
2. No gaps between conveyances (every grantee becomes next grantor)
3. All conveyances properly executed, acknowledged, and delivered
4. All necessary parties join in conveyances (spouses, co-owners, entities)
5. Conveyances are valid (no fraud, duress, incompetence, lack of authority)

**Common Chain Defects:**

**Wild Deed:**
- Deed from someone who doesn't appear in chain (stranger to title)
- Cannot be found by searching grantor-grantee index from root forward
- Example: A→B→C→D, then X→D (X is wild; where did X get title?)
- Cure: Obtain quit claim from X or establish X had no interest

**Gap in Title:**
- Missing conveyance in chain (A→B→D, missing B→C)
- Gap period creates uncertainty about ownership
- Cure: Locate missing deed or obtain curative affidavit/quit claim

**Defective Conveyance:**
- Deed not properly acknowledged (no notary or defective acknowledgment)
- Grantor lacked capacity (minor, mentally incompetent, deceased)
- Deed not delivered (intent to convey not shown)
- Forged signatures
- Cure: Obtain corrective deed, probate order, or ratification

**Heirship Issues:**
- Prior owner died; no probate or defective probate
- Heirs not identified or consent not obtained
- Cure: File probate, obtain heirship affidavit, or quiet title

**Entity Authority:**
- LLC/corporation sold property; no resolution or authority shown
- Partnership sold property; all partners did not join
- Cure: Obtain entity resolutions, affidavits of authority, or ratification

**Underwriting Decision:**
Title company evaluates severity of defect and likelihood of adverse claim.
- Minor defects: Insure over with exception or affidavit
- Material defects: Require curative before issuing policy
- Fatal defects: Decline to insure until resolved
""",
    key_factors=[
        "Each link in chain properly executes and connects to next",
        "No gaps or missing conveyances",
        "No wild deeds from strangers to title",
        "All necessary parties joined in conveyances (spouses, co-owners)",
        "Probate completed for deceased owners",
        "Entity authority shown for LLC/corporate conveyances",
        "Conveyances properly acknowledged and recorded",
    ],
    primary_authority=[
        "Texas Property Code §5.022 — deed requirements (writing, signature, delivery)",
        "Texas Estates Code Title 2 — probate requirements for heirship",
        "Wiley v. Spilman, 100 S.W.2d 585 (Tex. 1937) — wild deed not in chain",
    ],
    burden_holder="Title company examines chain; seller must cure defects for marketable title",
    adversary_position="Buyer may claim defect renders title unmarketable; seller argues defect is minor or cured",
    counter_arguments=[
        "Minor defects that do not affect marketability are acceptable",
        "Curative instruments (corrective deeds, affidavits) effectively cure many defects",
        "Adverse possession may cure gaps if possession meets statutory requirements",
        "Title insurance covers many defects even if not cured (forgery, lack of capacity, etc.)",
    ],
    resolution_strategy="Examine each link in chain for proper execution, acknowledgment, and connection; identify gaps, wild deeds, and defective conveyances; require curative action or except from coverage.",
    category=IssueCategory.UNDERWRITING_RISK,
    confidence=ConfidenceStratification.DEFENSIBLE,
    controlling_precedent="Wiley v. Spilman — wild deed doctrine; deed from stranger not in chain is void"
)

# Doctrine 9: Title Defect Types
DOCTRINE_TITLE_DEFECT_TYPES = DoctrineBlock(
    topic="title_defect_types",
    keywords=["wild deed", "forged deed", "gap in title", "heirship defect", "entity authority", "improper acknowledgment"],
    conclusion_templates=[
        "Defect type: {defect_type}. Severity: {severity}. Curative action required: {curative}.",
        "Wild deed from {grantor} creates cloud on title; quit claim or quiet title action necessary.",
        "Forged deed is void ab initio; title never passed; all subsequent conveyances are void."
    ],
    reasoning_framework="""
Title Defect Classification — Underwriting Risk Assessment:

**Class 1: Fatal Defects (Cannot Insure Until Cured):**

1. **Forged Deed** — Signature forged; deed is void from inception; title never passed
   - All subsequent conveyances are also void (built on false foundation)
   - Cure: Quiet title action; obtain deed from true owner; title insurance may cover loss

2. **Undisclosed Federal Tax Lien** — IRS lien not discovered in search; takes priority over subsequent purchasers
   - Federal tax liens have 30-year life; relate back to assessment date
   - Cure: Payoff or release from IRS; subordination agreement

3. **Missing Probate** — Prior owner died intestate; no probate or administration
   - Title passed to heirs by operation of law but identities uncertain
   - Cure: Probate estate or heirship affidavit with title insurance

**Class 2: Material Defects (Require Curative or Exception):**

4. **Wild Deed** — Conveyance from stranger to title; not connected to chain
   - Cannot be found by grantor-grantee search from root
   - Cure: Quit claim from wild grantor; establish wild grantor had no interest

5. **Gap in Title** — Missing link in chain (A→B→D, no B→C deed)
   - Ownership uncertain during gap period
   - Cure: Locate missing deed; affidavit of no interest; title insurance over gap

6. **Improper Acknowledgment** — Notary defect; acknowledgment missing or defective
   - Deed may be valid between parties but not recordable or effective against purchasers
   - Cure: Corrective deed with proper acknowledgment

7. **Lack of Entity Authority** — LLC/corporation conveyed without resolution or authority
   - Deed voidable by entity or members/shareholders
   - Cure: Ratification by entity; affidavit of authority; title insurance over defect

8. **Spouse Not Joined** — Community property or homestead; spouse did not sign
   - Spouse has interest that was not conveyed
   - Cure: Spouse joins in ratification deed; affidavit of separate property

**Class 3: Minor Defects (Insure Over or Accept):**

9. **Name Variance** — Grantor/grantee name spelled differently in successive deeds
   - John Smith vs John A. Smith vs J.A. Smith
   - Cure: Affidavit of identity (same person); title company insures over

10. **Scrivener's Error** — Typographical error in legal description or date
    - Obvious error that can be corrected by reformation
    - Cure: Corrective deed; scrivener's affidavit

**Underwriting Evaluation:**
- Likelihood of adverse claim arising from defect
- Cost to cure vs cost to insure over defect
- Policy exclusions/exceptions vs full coverage
""",
    key_factors=[
        "Severity of defect (fatal, material, minor)",
        "Likelihood of adverse claim",
        "Curability (can defect be fixed pre-closing?)",
        "Cost to cure vs insuring over",
        "Age of defect (statute of limitations may bar claims)",
        "Policy coverage for defect type (forged deed covered, undisclosed lien covered)",
    ],
    primary_authority=[
        "Texas Property Code §5.022 — deed requirements",
        "Texas Estates Code §201.001 — intestate succession requires probate or affidavit",
        "26 USC §6323 — federal tax lien priority",
        "Stone v. Clements, 991 S.W.2d 793 (Tex. App. 1999) — forged deed void",
    ],
    burden_holder="Title company identifies defects; seller cures or buyer accepts with title insurance",
    adversary_position="Buyer may demand cure of all defects; seller argues minor defects acceptable with insurance",
    counter_arguments=[
        "Title insurance covers most defects even if not cured (forged deed, missing probate, etc.)",
        "Minor defects that do not affect marketability need not be cured",
        "Cost to cure may exceed risk; insurance more economical",
        "Statute of limitations bars many old claims",
    ],
    resolution_strategy="Classify defect by severity; evaluate curability and cost; require cure for fatal defects, insure over material defects, accept minor defects.",
    category=IssueCategory.UNDERWRITING_RISK,
    confidence=ConfidenceStratification.DEFENSIBLE,
    controlling_precedent="Stone v. Clements — forged deed is void ab initio; title never passed"
)

# Doctrine 10: Lien Priority Rules
DOCTRINE_LIEN_PRIORITY = DoctrineBlock(
    topic="lien_priority_rules",
    keywords=["lien priority", "first in time", "deed of trust", "mechanic's lien", "judgment lien", "tax lien", "subordination"],
    conclusion_templates=[
        "First lien position: {lien_description} recorded {date}. All junior liens subordinate.",
        "Mechanic's lien relates back to inception of work on {date}, taking priority over deed of trust recorded {later_date}.",
        "Federal tax lien filed {date} takes priority over all subsequent interests including recorded mortgages."
    ],
    reasoning_framework="""
Lien Priority — Order of Payment in Foreclosure or Sale:

**General Rule: First in Time, First in Right**
Liens recorded earlier have priority over later-recorded liens.
Exception: Statutory liens may have priority based on relation-back or super-priority.

**Lien Priority Hierarchy (Texas):**

1. **Property Tax Liens** — First priority by statute; take precedence over all other liens
   - Relate back to January 1 of tax year
   - Cannot be subordinated or avoided (except in bankruptcy)

2. **Special Assessment Liens** — HOA assessments, MUD bonds, road district assessments
   - Often have super-priority over mortgages (check declaration/statute)

3. **Mechanic's & Materialman's Liens** — Relate back to inception of work or delivery of materials
   - Texas Property Code §53.124 — affidavit must be filed within strict deadlines
   - Priority from inception date, even if recorded after mortgage (if timely filed)

4. **Judgment Liens** — Abstract of judgment filed in county where property located
   - Priority from date abstract filed (not date of judgment)
   - Last 10 years from date of judgment; renewable

5. **Mortgage/Deed of Trust Liens** — Priority from recording date
   - First lien, second lien, third lien based on recording order
   - Refinances may lose priority unless subordination agreements obtained

6. **Federal Tax Liens** — IRS Notice of Federal Tax Lien (NFTL)
   - Priority from filing date but 45-day purchaser protection period
   - 30-year duration from assessment; can be catastrophic if missed

7. **HOA Liens** — Relate back to date assessment becomes due
   - May have super-priority over first mortgage (limited to 6 months in Texas)

**Subordination Agreements:**
Junior lien holder agrees to subordinate to new senior lien (e.g., refinance).
Without subordination, refinance drops to junior position behind original second mortgage.

**Foreclosure and Priority:**
Foreclosing lien holder wipes out junior liens but not senior liens.
Purchaser at foreclosure takes subject to senior liens.

**Title Insurance Impact:**
Policy insures lien priority as shown in Schedule B-II.
If undisclosed senior lien exists, policy covers loss.
""",
    key_factors=[
        "Recording date establishes priority (first in time, first in right)",
        "Property tax liens have automatic first priority",
        "Mechanic's liens relate back to inception of work (may jump ahead of mortgage)",
        "Federal tax liens have 30-year life and take priority from filing",
        "Subordination agreements preserve priority in refinances",
        "Foreclosure wipes out junior liens but not senior liens",
    ],
    primary_authority=[
        "Texas Property Code §53.001 et seq. — mechanic's lien priority and relation-back",
        "26 USC §6323 — federal tax lien priority rules",
        "Texas Property Code §52.006 — judgment lien creation and priority",
        "Texas Tax Code §32.05 — property tax lien priority (first and superior)",
    ],
    burden_holder="Senior lien holder has priority; junior must wait until senior satisfied",
    adversary_position="Junior lien holder may argue equitable priority or relation-back; senior asserts recording date controls",
    counter_arguments=[
        "Race-notice statute in Texas: first to record with no notice of prior unrecorded lien wins",
        "Mechanic's lien relation-back is statutory exception to first-in-time rule",
        "Federal tax liens have special priority rules under federal law (preempt state law)",
        "HOA super-priority limited by statute to 6 months assessments in Texas",
    ],
    resolution_strategy="Verify recording dates for all liens; identify statutory priority (tax, mechanic's, HOA); obtain subordination agreements for refinances; list in Schedule B-II in priority order.",
    category=IssueCategory.LIEN_ANALYSIS,
    confidence=ConfidenceStratification.DEFENSIBLE,
    controlling_precedent="Texas Tax Code §32.05 — property tax liens superior to all other liens"
)

# Doctrine 11: Mechanic's Lien vs Deed of Trust Priority
DOCTRINE_MECHANICS_LIEN_PRIORITY = DoctrineBlock(
    topic="mechanics_lien_vs_deed_of_trust",
    keywords=["mechanic's lien", "materialman's lien", "construction lien", "relation back", "inception of work", "deed of trust priority"],
    conclusion_templates=[
        "Mechanic's lien relates back to {inception_date}, predating deed of trust recorded {deed_date}, giving lien priority.",
        "Mechanic's lien affidavit filed {days} days after completion; missed 4-month deadline; lien invalid.",
        "Original contractor mechanic's lien has priority over subcontractor lien; both relate back to same inception date."
    ],
    reasoning_framework="""
Mechanic's Lien Priority — Relation-Back Doctrine:

**Relation-Back Rule (Texas Property Code §53.124):**
Mechanic's lien relates back to "inception of the work" or first delivery of material.
Even if lien affidavit filed months after work completed, priority dates to inception.

**Why This Matters:**
Mortgage recorded AFTER work started but BEFORE lien filed may be subordinate to mechanic's lien.

**Example Timeline:**
- March 1: Construction begins (inception of work)
- April 15: Deed of trust recorded (construction loan)
- July 1: Construction completed
- August 15: Mechanic's lien affidavit filed (within 4 months of completion)

**Result:** Mechanic's lien has priority over deed of trust (March 1 vs April 15).

**Mechanic's Lien Requirements:**
1. **Claimants:** Original contractor, subcontractor, supplier, laborer, architect, engineer
2. **Property:** Residential or commercial real property improvements
3. **Notice:** Preliminary notice required for subcontractors (Texas Property Code §53.056)
4. **Affidavit:** Must be filed within 4 months of completion (original contractor) or last work (sub)
5. **Enforcement:** Must file suit to foreclose within 2 years of completion or 1 year from filing affidavit

**Inception of Work Defined:**
- First physical work on site (excavation, surveying, material delivery to site)
- NOT contract signing or mobilization off-site
- Relates to entire project (all trades), not individual contractor's start date

**Defeating Mechanic's Lien:**
- Payment in full to contractor (removes lien even if sub unpaid if contractor was paid)
- Bond posted by owner or contractor (bond replaces lien on property)
- Untimely filing (affidavit filed after 4-month deadline)
- Notice defects (sub failed to send preliminary notice)

**Title Insurance Implications:**
Title company searches for mechanic's lien affidavits before closing.
If construction loan, title company may require contractor/sub waivers of lien.
Policy may except mechanic's liens for work performed before effective date.

**Lender Protection:**
Construction lenders require:
- Contractors to provide lien waivers at each draw
- Title company to insure no mechanic's liens have priority over deed of trust
- Payment directly to contractors/subs (joint checks)
""",
    key_factors=[
        "Inception of work date determines priority (not filing date)",
        "Mechanic's lien may have priority over deed of trust recorded after inception",
        "Affidavit must be filed within 4 months of completion (original contractor)",
        "Subcontractors must send preliminary notice to owner/lender within strict deadlines",
        "Suit to foreclose must be filed within 2 years of completion",
        "Payment to contractor removes lien even if subcontractor unpaid",
    ],
    primary_authority=[
        "Texas Property Code §53.124 — relation-back to inception of work",
        "Texas Property Code §53.056 — preliminary notice requirements for subs",
        "Texas Property Code §53.052 — affidavit filing deadlines",
        "Texas Property Code §53.158 — foreclosure suit deadline (2 years)",
    ],
    burden_holder="Mechanic's lien claimant must perfect lien by timely filing affidavit and giving notice",
    adversary_position="Lender argues lien not timely filed or notice defective; contractor asserts relation-back priority",
    counter_arguments=[
        "Relation-back is statutory exception to first-in-time recording rule",
        "Mechanic's lien protects those who improve property and add value",
        "Lender can protect itself by requiring lien waivers at each draw",
        "Bonding the lien removes cloud on title and allows closing",
    ],
    resolution_strategy="Determine inception date and deed of trust recording date; verify affidavit timely filed; obtain lien waivers from contractors/subs; require bond if lien claimed.",
    category=IssueCategory.LIEN_ANALYSIS,
    confidence=ConfidenceStratification.DEFENSIBLE,
    controlling_precedent="Texas Property Code §53.124 — mechanic's lien relates back to inception of work"
)

# Doctrine 12: Title Insurance Claims Handling
DOCTRINE_CLAIMS_HANDLING = DoctrineBlock(
    topic="claims_handling_process",
    keywords=["title insurance claim", "notice of claim", "defense duty", "indemnity", "loss payment", "exclusions", "exceptions"],
    conclusion_templates=[
        "Claim filed for {loss_type}; covered risk under Policy Section {section}; estimated loss ${amount}.",
        "Claim denied: loss falls within Policy Exclusion {exclusion} for {reason}.",
        "Title company has duty to defend against {claim_type} and duty to indemnify up to policy amount of ${limit}."
    ],
    reasoning_framework="""
Title Insurance Claims — Coverage, Defense, and Payment:

**Covered Risks (ALTA Owner's Policy 2006):**
1. Title vested other than as stated in policy (wrong owner)
2. Any defect, lien, encumbrance on title at policy date (missed in search)
3. Unmarketability of title (cannot sell or mortgage)
4. Lack of access to land (landlocked)
5. Encroachments onto land by improvements on adjoining land
6. Forced removal of improvements due to encroachment onto adjoining land or easement
7. Forgery, fraud, duress, incompetency, incapacity, impersonation affecting title
8. Defective execution of documents (lack of capacity, authority, or signature)
9. Restrictive covenant violations existing at policy date

**Exclusions (What's NOT Covered):**
1. **Governmental Action** — Eminent domain, police power, zoning changes (unless endorsement)
2. **Created by Insured** — Defects created, assumed, or agreed to by insured after policy date
3. **Known Defects** — Matters known to insured but not disclosed to title company
4. **Environmental Hazards** — Contamination, EPA liens (unless ALTA 8.1 endorsement)
5. **Native American Claims** — Indian land claims (rarely applicable)
6. **Future Matters** — Recorded after policy date (unless gap coverage endorsement)

**Exceptions (Listed in Schedule B):**
Any matter listed in Schedule B-II is excepted from coverage.
No claim coverage for excepted matters even if otherwise a covered risk.

**Claim Process:**
1. **Notice of Claim** — Insured must notify title company promptly in writing
2. **Claim Investigation** — Title company investigates validity and coverage
3. **Defense Duty** — If claim covered, title company must defend in litigation
4. **Settlement Authority** — Title company may settle claim without insured's consent
5. **Indemnity Payment** — If loss incurred, title company pays up to policy amount

**Duty to Defend vs Duty to Indemnify:**
- **Duty to Defend:** Title company hires attorney and pays defense costs (no deductible, no limit)
- **Duty to Indemnify:** Title company pays actual loss up to policy amount (including legal fees if no duty to defend)

**Claim Valuation:**
Loss measured by:
- Diminution in value of estate or interest insured
- Costs to cure defect or remove encumbrance
- Cost to defend title (legal fees if duty to defend not triggered)
- Policy limits apply; no coverage beyond policy amount

**Common Claims:**
- Forged deed in chain (prior owner's signature forged)
- Missing heir (deceased owner's heir not joined in conveyance)
- Undisclosed mortgage or tax lien (not found in search)
- Boundary dispute (encroachment, adverse possession)
- Access issue (landlocked property or prescriptive easement dispute)
- Survey defect (encroachment missed, shortage in area)

**Bad Faith Claims:**
Texas Insurance Code §541 prohibits unfair claims practices.
Title company must investigate promptly, communicate, and pay valid claims.
Failure may result in bad faith damages, attorney fees, and penalties.
""",
    key_factors=[
        "Loss must be a covered risk under policy (not excluded, not excepted)",
        "Defect must have existed at or before policy date (not created after)",
        "Insured must give prompt written notice of claim",
        "Title company has duty to defend if claim potentially covered",
        "Loss valuation: diminution in value or cost to cure",
        "Policy limits apply (no coverage beyond insured amount)",
    ],
    primary_authority=[
        "ALTA Owner's Policy (2006) — Covered Risks, Exclusions, Conditions",
        "Texas Insurance Code §541.060 — unfair claim settlement practices",
        "28 TAC §9.1 et seq. — title insurance policy forms and endorsements",
    ],
    burden_holder="Title company must investigate and pay valid claims; insured must give notice and cooperate",
    adversary_position="Insured argues claim is covered; title company asserts exclusion or exception applies",
    counter_arguments=[
        "Policy expressly excludes governmental action, environmental hazards, and created defects",
        "Matters listed in Schedule B are excepted; insured accepted commitment with exceptions",
        "Insured failed to give timely notice; prejudiced title company's ability to defend",
        "Loss is speculative or not yet incurred (must be actual loss, not potential)",
    ],
    resolution_strategy="Review policy for coverage (covered risk vs exclusion vs exception); investigate claim validity; determine duty to defend; evaluate loss and settle or litigate.",
    category=IssueCategory.CLAIMS_LOSS,
    confidence=ConfidenceStratification.DEFENSIBLE,
    controlling_precedent="Lawyers Title Ins. Corp. v. Doubletree Partners, 739 F.3d 848 (5th Cir. 2014) — duty to defend"
)

# Doctrine 13: Rate Regulation in Texas
DOCTRINE_RATE_REGULATION = DoctrineBlock(
    topic="rate_regulation_texas",
    keywords=["promulgated rates", "TDI", "basic premium", "simultaneous issue", "reissue credit", "rate deviation", "rebate prohibited"],
    conclusion_templates=[
        "Title insurance premium calculated per TDI Basic Rate Manual: ${amount} for policy amount of ${coverage}.",
        "Simultaneous issue discount applies: owner's policy ${owner_premium}, lender's policy ${lender_premium} (60% discount).",
        "Reissue credit of ${credit} applies based on prior policy dated {prior_date} (within 20 years)."
    ],
    reasoning_framework="""
Title Insurance Rate Regulation — Texas Promulgated Rates:

**Regulatory Framework:**
Texas Insurance Code Title 11 and 28 TAC Chapter 9 require promulgated rates.
Texas Department of Insurance (TDI) sets all title insurance rates.
NO deviation, discount, rebate, or inducement allowed (except as promulgated).

**Basic Premium Calculation:**
TDI Basic Rate Manual provides premium tables based on policy amount:
- $0 - $100,000: Tiered rate per $1,000
- $100,001 - $1,000,000: Reduced rate per $1,000
- $1,000,001+: Further reduced rate per $1,000

**Simultaneous Issue Discount:**
When owner's policy and lender's policy issued at same closing:
- Owner's policy charged at full basic premium
- Lender's policy charged at ~40% of basic premium (60% discount)
- Both policies must be issued by same title company

**Reissue Credit:**
If property insured within past 20 years and prior policy provided to title company:
- Reissue credit applied to basic premium (reduces premium)
- Credit amount varies by age of prior policy (higher credit if more recent)
- Does NOT apply to refinances (only purchases)

**Endorsement Premiums:**
Each endorsement has promulgated premium:
- Some are flat fees ($50, $100, $250)
- Some are percentage of basic premium (5%, 10%, 25%)
- ALTA 9 Comprehensive: typically $250-$500 depending on policy amount
- ALTA 8.1 Environmental: 10% of basic premium

**Prohibited Practices:**
- Premium rebates or kickbacks to buyer, seller, lender, or real estate agent
- Free services as inducement (free closings, surveys, appraisals)
- Rate deviations (charging more or less than promulgated rate)
- Splitting premium with non-title entities (except licensed escrow officers)

**Enforcement:**
TDI audits title companies for rate compliance.
Violations result in fines, license suspension, and criminal penalties.
Competitors may sue for unfair competition if rebates given.

**Comparison to Other States:**
Texas is one of few states with promulgated rates (Florida, New Mexico also).
Most states allow file-and-use or negotiated rates.
Texas system ensures uniform pricing but eliminates price competition.

**Title Plant Credit:**
Title companies that maintain title plants may charge lower search fees.
But basic premium remains same (promulgated rate applies to all).
""",
    key_factors=[
        "All premiums promulgated by TDI; no deviation allowed",
        "Simultaneous issue discount applies when owner + lender policies at same closing",
        "Reissue credit applies if prior policy within 20 years (purchase only, not refi)",
        "Endorsement premiums vary (flat fee or percentage)",
        "Rebates, kickbacks, and inducements prohibited",
        "Violations subject to fines, license suspension, criminal prosecution",
    ],
    primary_authority=[
        "Texas Insurance Code §2703.151 — promulgated rate requirement",
        "28 TAC §9.1 — Basic Premium Rate Manual",
        "28 TAC §9.4 — simultaneous issue and reissue credits",
        "Texas Insurance Code §2703.152 — prohibited rebates and inducements",
    ],
    burden_holder="Title company must charge promulgated rates; no discretion to discount or negotiate",
    adversary_position="Buyer may argue excessive premium or request discount; title company asserts TDI sets rates",
    counter_arguments=[
        "Promulgated rates ensure uniform pricing and prevent anti-competitive behavior",
        "TDI rate-setting process considers actuarial data and loss experience",
        "Rebates harm competition and lead to race-to-bottom pricing",
        "Buyer can shop for ancillary services (escrow, closing fees) but not basic premium",
    ],
    resolution_strategy="Calculate premium per TDI Basic Rate Manual; apply simultaneous issue discount if applicable; apply reissue credit if prior policy available; charge endorsement premiums per promulgated schedule.",
    category=IssueCategory.RATE_REGULATION,
    confidence=ConfidenceStratification.DEFENSIBLE,
    controlling_precedent="Texas Insurance Code §2703.151 — all rates must be promulgated by TDI"
)

# Doctrine 14: Mineral Reservation Exceptions
DOCTRINE_MINERAL_RESERVATION = DoctrineBlock(
    topic="mineral_reservation_exceptions",
    keywords=["mineral reservation", "surface estate", "mineral estate", "executive rights", "royalty", "NPRI", "exception to coverage"],
    conclusion_templates=[
        "Mineral estate reserved in deed dated {date} from {grantor}; surface estate only insured by policy.",
        "Exception {number}: Mineral interests as reserved in prior conveyances; policy does not cover subsurface rights.",
        "Title company will not insure mineral estate without full mineral title search (50+ years)."
    ],
    reasoning_framework="""
Mineral Reservation Exceptions — Surface vs Mineral Estate:

**Estate in Land Doctrine:**
Texas recognizes separate ownership of surface and mineral estates.
Mineral estate is "dominant" — holder can use surface as reasonably necessary for extraction.

**Common Exception Language:**
"Reservations or exceptions of minerals, mineral rights, royalties, and related rights
as reserved in prior conveyances of record."

**What This Means:**
- Policy insures surface estate ONLY
- Mineral estate ownership NOT insured (excepted from coverage)
- If mineral owner drills and damages surface, policy does NOT cover
- If claim arises from mineral title defect, policy does NOT cover

**Why Mineral Exceptions Are Standard:**
Mineral title search requires 50+ years (Texas Property Code §13.001).
Surface title search typically 30 years.
Title companies except minerals to avoid liability for deep mineral title defects.

**When Minerals ARE Insured:**
- Buyer requests mineral coverage and pays additional premium
- Title company performs full 50-year mineral title search
- Separate mineral title commitment issued
- Often seen in oil & gas acquisitions

**Mineral Rights Components:**
1. **Executive Rights** — Right to lease minerals (can be separated from mineral ownership)
2. **Mineral Interest** — Ownership of minerals in place (1/2, 1/4, 1/8, etc.)
3. **Royalty Interest** — Right to production revenue without leasing rights (NPRI = non-participating)
4. **Surface Rights** — Ownership of surface and right to exclude (subordinate to mineral estate)

**Impact on Surface Owner:**
Surface owner insured under policy has NO protection if:
- Mineral owner drills and damages surface (accommodation doctrine may help but not insured)
- Mineral title defect leads to adverse claim against surface
- Royalty owner claims surface use interferes with production

**Oil & Gas Transactions:**
Mineral title insurance essential for E&P companies buying mineral rights.
Requires exhaustive 50-year search, runsheet, chain of title analysis.
ALTA 19 (Contiguity), 9.5 (Minerals), and custom endorsements common.
""",
    key_factors=[
        "Mineral estate often reserved in prior deeds (especially pre-1980s)",
        "Standard title policy insures surface only (minerals excepted)",
        "Mineral title search requires 50+ years per Texas Property Code",
        "Buyer can request mineral coverage for additional premium",
        "Mineral estate is dominant; surface owner must accommodate mineral use",
        "Oil & gas transactions require separate mineral title commitment",
    ],
    primary_authority=[
        "Texas Property Code §13.001 — 50-year marketable title for minerals",
        "Texas Natural Resources Code §91.402 — mineral estate dominant",
        "Altman v. Blake, 712 S.W.2d 117 (Tex. 1986) — accommodation doctrine",
    ],
    burden_holder="Buyer must request mineral coverage; title company conducts 50-year search if requested",
    adversary_position="Surface owner argues mineral exception too broad; title company asserts standard exception",
    counter_arguments=[
        "Mineral exception is standard in Texas due to separate estate doctrine",
        "Full mineral title search is expensive and time-consuming (50+ years required)",
        "Buyer can purchase mineral coverage for additional premium if needed",
        "Surface-only policy is adequate for residential and most commercial transactions",
    ],
    resolution_strategy="Identify whether minerals are needed for transaction; if yes, request mineral coverage and 50-year search; if no, accept standard mineral exception.",
    category=IssueCategory.MINERAL_EXCLUSION,
    confidence=ConfidenceStratification.DEFENSIBLE,
    controlling_precedent="Texas Property Code §13.001 — 50-year root of title for minerals"
)

# Doctrine 15: Curative Requirements for Title Insurance
DOCTRINE_CURATIVE_REQUIREMENTS = DoctrineBlock(
    topic="curative_requirements_title_insurance",
    keywords=["curative", "title defect cure", "corrective deed", "affidavit of heirship", "quiet title", "ratification"],
    conclusion_templates=[
        "Curative requirement: {defect_type}. Recommended cure: {curative_instrument}. Estimated timeline: {timeline}.",
        "Heirship affidavit required for {deceased_owner} to establish heirs and vest title.",
        "Quiet title action necessary to cure wild deed from {grantor}; alternative: obtain quit claim and insure over."
    ],
    reasoning_framework="""
Curative Requirements for Title Insurance — Defect Resolution:

**Common Curative Instruments:**

1. **Corrective Deed (Deed of Correction):**
   - Fixes scrivener's errors in prior deed (misspelling, wrong legal description, wrong date)
   - Must be executed by original grantor
   - Relates back to original deed date for priority purposes
   - Fast and inexpensive cure

2. **Affidavit of Heirship:**
   - Establishes heirs of deceased owner when no probate filed
   - Requires two disinterested witnesses with knowledge of family
   - Must include detailed family tree, marriage/death dates, heirs' names
   - Filed of record and combined with title insurance for marketability

3. **Ratification Deed:**
   - Cures lack of authority (entity sold without resolution)
   - Cures spousal consent issue (community property or homestead)
   - Confirms and ratifies prior conveyance

4. **Affidavit of Identity:**
   - Establishes that John Smith = John A. Smith = J.A. Smith (same person)
   - Cures name variance in chain
   - Requires detailed identifying information (SSN, DOB, addresses, employment)

5. **Quiet Title Action:**
   - Judicial proceeding to clear title cloud (wild deed, adverse possession claim, lien dispute)
   - Notice to all interested parties; court order vests title
   - Expensive and time-consuming (6-12 months minimum)
   - Last resort when other curative instruments insufficient

6. **Release of Lien:**
   - Paid-off mortgage, judgment lien, tax lien released and recorded
   - Must be obtained from lien holder; if defunct, substituted release or quiet title

7. **Probate or Determination of Heirship:**
   - Court proceeding to identify heirs and vest title when informal affidavit not sufficient
   - Required if estate >$75,000 in Texas or real property involved
   - 6-12 month process; generates court order that clears title

**Title Company Evaluation:**
Title company determines:
- Severity of defect (fatal, material, minor)
- Curative instrument sufficient to render title marketable/insurable
- Cost and timeline for cure
- Whether to insure over defect with affidavit or require judicial action

**Schedule B-I Requirements:**
Curative requirements listed in Schedule B-I of commitment.
ALL must be satisfied before policy issues.
Failure to cure any requirement = no coverage.

**Alternative to Cure:**
If defect minor and risk acceptable, title company may:
- Insure over defect with affidavit and exception
- Accept curative affidavit in lieu of judicial action
- Charge higher premium or limit coverage
""",
    key_factors=[
        "Type of defect determines curative instrument needed",
        "Cost and timeline for cure (corrective deed = fast, quiet title = slow)",
        "Title company acceptance of curative instrument",
        "All Schedule B-I curative requirements must be satisfied",
        "Alternative: insure over defect with affidavit and exception",
        "Quiet title is last resort for complex or contested defects",
    ],
    primary_authority=[
        "Texas Estates Code §202.001 — affidavit of heirship requirements",
        "Texas Property Code §5.028 — corrective deed/deed of correction",
        "Texas Civil Practice & Remedies Code §16.0265 — quiet title suits",
    ],
    burden_holder="Seller must cure defects to deliver marketable title; buyer may accept with title insurance",
    adversary_position="Seller argues curative affidavit sufficient; buyer demands judicial action for certainty",
    counter_arguments=[
        "Affidavits combined with title insurance provide marketable title without court action",
        "Cost and delay of quiet title often exceed risk of title defect",
        "Title insurance covers defect even if curative imperfect (forged affidavit, etc.)",
        "Industry custom accepts affidavits for heirship, identity, and minor defects",
    ],
    resolution_strategy="Identify defect type; select appropriate curative instrument (deed, affidavit, release, probate, quiet title); estimate cost and timeline; obtain title company approval.",
    category=IssueCategory.CURATIVE_REQUIREMENTS,
    confidence=ConfidenceStratification.DEFENSIBLE,
    controlling_precedent="Texas Estates Code §202.001 — affidavit of heirship accepted with title insurance"
)


# ===================================================================
# Doctrine Interaction Graph
# ===================================================================

_DOCTRINE_INTERACTIONS = [
    DoctrineInteraction(
        topic_a="schedule_b1_requirements",
        topic_b="curative_requirements_title_insurance",
        interaction_type="depends_on",
        resolution_rule="Schedule B-I requirements identify curative actions needed; use curative doctrines to resolve",
        priority=1
    ),
    DoctrineInteraction(
        topic_a="schedule_b2_exceptions",
        topic_b="alta_endorsements",
        interaction_type="modifies",
        resolution_rule="ALTA endorsements can delete or modify Schedule B-II exceptions for additional premium",
        priority=1
    ),
    DoctrineInteraction(
        topic_a="lien_priority_rules",
        topic_b="mechanics_lien_vs_deed_of_trust",
        interaction_type="reinforces",
        resolution_rule="Mechanic's lien relation-back is exception to general first-in-time lien priority rule",
        priority=2
    ),
    DoctrineInteraction(
        topic_a="owners_vs_lenders_policy",
        topic_b="rate_regulation_texas",
        interaction_type="depends_on",
        resolution_rule="Premium calculation for owner's and lender's policies governed by TDI promulgated rates",
        priority=1
    ),
    DoctrineInteraction(
        topic_a="title_commitment_review_process",
        topic_b="schedule_a_requirements",
        interaction_type="depends_on",
        resolution_rule="Schedule A is critical component of commitment review; accuracy essential",
        priority=1
    ),
    DoctrineInteraction(
        topic_a="chain_of_title_examination_underwriting",
        topic_b="title_defect_types",
        interaction_type="reinforces",
        resolution_rule="Chain of title examination identifies defects; defect classification determines underwriting decision",
        priority=1
    ),
    DoctrineInteraction(
        topic_a="mineral_reservation_exceptions",
        topic_b="schedule_b2_exceptions",
        interaction_type="reinforces",
        resolution_rule="Mineral reservations typically listed in Schedule B-II as standard exception",
        priority=2
    ),
    DoctrineInteraction(
        topic_a="claims_handling_process",
        topic_b="schedule_b2_exceptions",
        interaction_type="conflicts",
        resolution_rule="Excepted matters in Schedule B-II are NOT covered; claims for excepted matters denied",
        priority=1
    ),
]


# ===================================================================
# Global Doctrine Cache and Interaction Graph
# ===================================================================

_DOCTRINE_CACHE: list[DoctrineBlock] = []
_INTERACTION_GRAPH: list[DoctrineInteraction] = []


def build_doctrine_cache() -> list[DoctrineBlock]:
    """Build and return the complete doctrine cache."""
    global _DOCTRINE_CACHE
    if not _DOCTRINE_CACHE:
        _DOCTRINE_CACHE = [
            DOCTRINE_COMMITMENT_REVIEW,
            DOCTRINE_SCHEDULE_A,
            DOCTRINE_SCHEDULE_B1,
            DOCTRINE_SCHEDULE_B2,
            DOCTRINE_OWNERS_VS_LENDERS,
            DOCTRINE_ALTA_ENDORSEMENTS,
            DOCTRINE_TITLE_PLANT_SEARCH,
            DOCTRINE_CHAIN_OF_TITLE_UNDERWRITING,
            DOCTRINE_TITLE_DEFECT_TYPES,
            DOCTRINE_LIEN_PRIORITY,
            DOCTRINE_MECHANICS_LIEN_PRIORITY,
            DOCTRINE_CLAIMS_HANDLING,
            DOCTRINE_RATE_REGULATION,
            DOCTRINE_MINERAL_RESERVATION,
            DOCTRINE_CURATIVE_REQUIREMENTS,
        ]
    return _DOCTRINE_CACHE


def build_interaction_graph() -> list[DoctrineInteraction]:
    """Build and return the doctrine interaction graph."""
    global _INTERACTION_GRAPH
    if not _INTERACTION_GRAPH:
        _INTERACTION_GRAPH = _DOCTRINE_INTERACTIONS
    return _INTERACTION_GRAPH


def get_doctrine_cache() -> list[DoctrineBlock]:
    """Get doctrine cache (builds if not already built)."""
    if not _DOCTRINE_CACHE:
        build_doctrine_cache()
    return _DOCTRINE_CACHE


def get_interaction_graph() -> list[DoctrineInteraction]:
    """Get interaction graph (builds if not already built)."""
    if not _INTERACTION_GRAPH:
        build_interaction_graph()
    return _INTERACTION_GRAPH


def find_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    """Find doctrine block by exact topic match."""
    cache = get_doctrine_cache()
    for doctrine in cache:
        if doctrine.topic == topic:
            return doctrine
    return None


def find_doctrines_by_keyword(keyword: str) -> list[DoctrineBlock]:
    """Find all doctrines containing keyword (case-insensitive)."""
    cache = get_doctrine_cache()
    keyword_lower = keyword.lower()
    matches = []
    for doctrine in cache:
        if any(keyword_lower in kw.lower() for kw in doctrine.keywords):
            matches.append(doctrine)
    return matches


def find_doctrines_by_category(category: IssueCategory) -> list[DoctrineBlock]:
    """Find all doctrines in a specific category."""
    cache = get_doctrine_cache()
    return [d for d in cache if d.category == category]


def get_interactions_for_topic(topic: str) -> list[DoctrineInteraction]:
    """Get all interactions involving a specific topic."""
    graph = get_interaction_graph()
    return [i for i in graph if topic in (i.topic_a, i.topic_b)]
