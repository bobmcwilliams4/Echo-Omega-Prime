"""
LM09 Runsheet Generator — Doctrine Definitions Module
Engine ID: LM09 | Port: 8509
Pre-compiled expert reasoning blocks for oil & gas title examination,
run sheet generation, chain of title analysis, and interest computation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class IssueCategory(str, Enum):
    """Top-level issue categories for run sheet generation."""
    CHAIN_OF_TITLE = "CHAIN_OF_TITLE"
    INTEREST_COMPUTATION = "INTEREST_COMPUTATION"
    LEGAL_DESCRIPTION = "LEGAL_DESCRIPTION"
    LEASE_ANALYSIS = "LEASE_ANALYSIS"
    MINERAL_RIGHTS = "MINERAL_RIGHTS"
    PROBATE_HEIRSHIP = "PROBATE_HEIRSHIP"
    RESERVATION_EXCEPTION = "RESERVATION_EXCEPTION"
    GAP_DETECTION = "GAP_DETECTION"
    RUNSHEET_FORMAT = "RUNSHEET_FORMAT"
    TITLE_STANDARDS = "TITLE_STANDARDS"


class ConfidenceLevel(str, Enum):
    """Confidence stratification for title opinions."""
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"


@dataclass
class DoctrineBlock:
    """A pre-compiled expert reasoning block for run sheet generation."""
    topic: str
    keywords: list[str]
    conclusion_template: str
    reasoning_framework: str
    key_factors: list[str]
    primary_authority: list[str]
    burden_holder: str
    adversary_position: str
    counter_arguments: list[str]
    resolution_strategy: str
    entity_scope: str
    confidence: float
    confidence_stratification: ConfidenceLevel
    controlling_precedent: str
    issue_category: IssueCategory
    interaction_edges: list[str] = field(default_factory=list)


def build_doctrine_cache() -> dict[str, DoctrineBlock]:
    """Build and return the complete doctrine cache for LM09."""
    doctrines: dict[str, DoctrineBlock] = {}

    # ─── DOCTRINE 1: WARRANTY DEED CHAIN ANALYSIS ─────────────────────
    doctrines["warranty_deed_chain_analysis"] = DoctrineBlock(
        topic="Warranty Deed Chain of Title Analysis",
        keywords=["warranty deed", "chain of title", "grantor", "grantee", "conveyance", "general warranty", "special warranty"],
        conclusion_template=(
            "A warranty deed conveys fee simple title with covenants of seisin, right to convey, "
            "against encumbrances, quiet enjoyment, warranty, and further assurances. The chain "
            "must show an unbroken succession from sovereignty or common source to present owner. "
            "Any gap triggers a curative requirement before the run sheet can certify marketable title."
        ),
        reasoning_framework=(
            "STEP 1: Identify the grantor and verify they are the record title holder at the date of conveyance. "
            "Cross-reference the grantor-grantee index to confirm the grantor acquired title via a prior instrument. "
            "STEP 2: Verify the legal description matches the tract under examination. Compare section, block, "
            "survey, and abstract numbers against the parent tract description. Account for aliquot parts and "
            "metes-and-bounds calls. STEP 3: Check for reservations and exceptions in the granting clause and "
            "habendum. A general warranty deed with mineral reservation severs the mineral estate from surface. "
            "STEP 4: Examine the warranty clause type. General warranty covers all prior defects; special warranty "
            "covers only defects arising under the grantor. STEP 5: Verify proper execution — grantor signature, "
            "acknowledgment, delivery, and recording. Texas Property Code Sec. 13.001 requires recording in the "
            "county where land is situated. STEP 6: Check for after-acquired title doctrine applicability — if "
            "grantor had no title at conveyance but later acquired it, a warranty deed's estoppel passes that "
            "title automatically. STEP 7: Document the conveyance on the run sheet with date, volume/page or "
            "clerk's file number, grantor, grantee, legal description, consideration, and any reservations."
        ),
        key_factors=[
            "Grantor must hold record title at time of conveyance",
            "Legal description must match or be contained within parent tract",
            "Warranty type determines scope of title protection",
            "Reservations and exceptions must be tracked separately",
            "Recording in proper county is essential for constructive notice",
            "After-acquired title doctrine applies to warranty deeds only",
        ],
        primary_authority=[
            "Texas Property Code Sec. 5.021-5.023 (Conveyance requirements)",
            "Texas Property Code Sec. 13.001 (Recording statute)",
            "Duhig v. Peavy-Moore Lumber Co., 135 Tex. 503 (1940)",
            "Westland Oil Dev. Corp. v. Gulf Oil Corp., 637 S.W.2d 903 (Tex. 1982)",
        ],
        burden_holder="Grantee claiming under warranty deed",
        adversary_position="Third party claiming superior title or challenging chain continuity",
        counter_arguments=[
            "Grantor lacked capacity or authority to convey",
            "Legal description is ambiguous or does not cover the tract",
            "Deed was not properly acknowledged or delivered",
            "Forged or fraudulent deed breaks the chain",
            "Prior unrecorded instrument takes priority under certain conditions",
        ],
        resolution_strategy=(
            "Trace chain backward from present owner to sovereignty or common source. "
            "Each link must show a recorded instrument with matching legal descriptions. "
            "Flag any gap, wild deed, or break for curative action."
        ),
        entity_scope="All parties in chain — individuals, entities, estates, trusts",
        confidence=0.92,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Duhig v. Peavy-Moore Lumber Co., 135 Tex. 503 (1940)",
        issue_category=IssueCategory.CHAIN_OF_TITLE,
        interaction_edges=["mineral_reservation_tracking", "gap_detection_methodology", "after_acquired_title"],
    )

    # ─── DOCTRINE 2: MINERAL DEED CONVEYANCE ─────────────────────────
    doctrines["mineral_deed_conveyance"] = DoctrineBlock(
        topic="Mineral Deed Conveyance and Severance",
        keywords=["mineral deed", "mineral interest", "severance", "mineral estate", "fee mineral", "undivided interest"],
        conclusion_template=(
            "A mineral deed conveys ownership of subsurface minerals separately from the surface estate, "
            "creating a severed mineral interest. The run sheet must track the mineral estate separately "
            "once severance occurs, following the mineral chain distinct from the surface chain. "
            "Fractional interests require precise computation of undivided shares."
        ),
        reasoning_framework=(
            "STEP 1: Identify whether the instrument creates a new severance or conveys an already-severed "
            "mineral interest. If the surface and minerals are unified, this deed severs them. If already "
            "severed, trace the mineral chain only. STEP 2: Parse the fractional interest conveyed — 'an "
            "undivided 1/2 of the minerals' vs 'an undivided 1/2 of grantor's mineral interest' yield "
            "different results. The former conveys half the minerals absolutely; the latter conveys half "
            "of whatever fraction the grantor owns. STEP 3: Apply the 'minerals' vs 'royalty' distinction. "
            "Texas follows the two-grant theory: minerals = executive rights + bonus + delay rentals + "
            "royalty; royalty = only the royalty stream. Moser v. U.S. Steel Corp. controls. STEP 4: Check "
            "for depth limitations or formation-specific conveyances. STEP 5: Track the severed mineral "
            "interest through subsequent conveyances, maintaining a separate column on the run sheet. "
            "STEP 6: Compute net mineral acres (NMA) = gross acres x mineral interest fraction. "
            "STEP 7: Cross-reference any outstanding leases affecting the mineral interest."
        ),
        key_factors=[
            "Severance creates separate mineral estate with independent chain",
            "Fractional interest language must be parsed precisely",
            "Minerals vs royalty distinction affects bundle of rights conveyed",
            "Depth limitations restrict the vertical scope of the conveyance",
            "NMA computation requires tracking fractional interests through chain",
            "Executive rights remain with mineral interest owner unless separately conveyed",
        ],
        primary_authority=[
            "Moser v. U.S. Steel Corp., 676 S.W.2d 99 (Tex. 1984)",
            "Altman v. Blake, 712 S.W.2d 117 (Tex. 1986)",
            "French v. Chevron U.S.A., Inc., 896 S.W.2d 795 (Tex. 1995)",
            "Texas Natural Resources Code Ch. 91-92",
        ],
        burden_holder="Mineral interest claimant",
        adversary_position="Surface owner or competing mineral claimant",
        counter_arguments=[
            "Instrument conveyed royalty interest, not mineral interest",
            "Grantor did not own minerals at time of severance deed",
            "Fractional interest language is ambiguous — 'of' vs 'in'",
            "Depth limitation or formation restriction applies",
            "Prior mineral conveyance already severed the estate",
        ],
        resolution_strategy=(
            "Establish whether minerals were unified or already severed at time of deed. "
            "Parse the granting clause to determine exact fraction conveyed. Apply Moser "
            "mineral/royalty distinction. Compute NMA and track separately on run sheet."
        ),
        entity_scope="Mineral interest owners, surface owners, lessees",
        confidence=0.90,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Moser v. U.S. Steel Corp., 676 S.W.2d 99 (Tex. 1984)",
        issue_category=IssueCategory.MINERAL_RIGHTS,
        interaction_edges=["nri_nma_calculation", "royalty_deed_analysis", "lease_status_tracking"],
    )

    # ─── DOCTRINE 3: OIL AND GAS LEASE ABSTRACTION ───────────────────
    doctrines["oil_gas_lease_abstraction"] = DoctrineBlock(
        topic="Oil and Gas Lease Abstraction for Run Sheet",
        keywords=["oil and gas lease", "OGL", "primary term", "royalty", "lessee", "lessor", "habendum", "granting clause"],
        conclusion_template=(
            "An oil and gas lease must be abstracted with all material terms including primary term, "
            "royalty fraction, bonus consideration, delay rental, depth clause, pooling authority, "
            "Pugh clause, shut-in provisions, and continuous drilling obligations. The run sheet "
            "must reflect current lease status — active, expired, HBP, or terminated."
        ),
        reasoning_framework=(
            "STEP 1: Identify the lessor and confirm they hold the mineral interest being leased. "
            "If the lessor owns a fractional mineral interest, the lease covers only that fraction. "
            "STEP 2: Record the primary term (typically 3-5 years) and the commencement date. "
            "Calculate the expiration date of the primary term. STEP 3: Parse the habendum clause "
            "for 'and so long thereafter as oil, gas, or other minerals are produced' or similar "
            "secondary term language. STEP 4: Note the royalty fraction — Texas standard was 1/8, "
            "modern leases typically 1/4 or 3/16. STEP 5: Check for Pugh clause (horizontal and "
            "vertical). A Pugh clause limits the secondary term to only those depths or portions "
            "actually being produced or included in a producing unit. STEP 6: Abstract pooling "
            "authority — whether the lease grants broad or limited pooling rights and any acreage "
            "limitations. STEP 7: Note shut-in royalty provisions, cessation of production clauses, "
            "force majeure provisions, and continuous drilling obligations. STEP 8: Check for "
            "assignments — partial or full — that affect the lessee's interest. STEP 9: Determine "
            "current lease status: primary term active, HBP, shut-in, or expired/terminated."
        ),
        key_factors=[
            "Lessor must own the mineral interest being leased",
            "Primary term dates and expiration are critical",
            "Royalty fraction determines NRI calculation",
            "Pugh clause limits HBP to producing depths/units",
            "Pooling authority scope affects unit participation",
            "Shut-in provisions may maintain lease beyond production cessation",
            "Assignments transfer all or part of lessee's working interest",
        ],
        primary_authority=[
            "Texas Natural Resources Code Sec. 91.001 et seq.",
            "Anadarko Petroleum Corp. v. Thompson, 94 S.W.3d 550 (Tex. 2002)",
            "Wagner & Brown, Ltd. v. Horwood, 58 S.W.3d 732 (Tex. 2001)",
            "BP America Production Co. v. Red Deer Resources, LLC, 526 S.W.3d 389 (Tex. 2017)",
        ],
        burden_holder="Lessee or assignee claiming lease is still in effect",
        adversary_position="Lessor or top-lease claimant asserting lease has expired",
        counter_arguments=[
            "Primary term has expired without production or operations",
            "Cessation of production exceeded savings clause period",
            "Shut-in royalty not timely paid",
            "Pugh clause released non-producing depths/acreage",
            "Pooling was invalid or exceeded authority",
        ],
        resolution_strategy=(
            "Abstract all material lease terms. Verify lessor's mineral ownership. "
            "Calculate primary term expiration. Determine current status (active/HBP/expired). "
            "Note all assignments and their effect on working interest allocation."
        ),
        entity_scope="Lessors, lessees, assignees, overriding royalty owners",
        confidence=0.93,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Anadarko Petroleum Corp. v. Thompson, 94 S.W.3d 550 (Tex. 2002)",
        issue_category=IssueCategory.LEASE_ANALYSIS,
        interaction_edges=["nri_nma_calculation", "pooling_unit_analysis", "assignment_tracking"],
    )

    # ─── DOCTRINE 4: NRI / NMA CALCULATION ────────────────────────────
    doctrines["nri_nma_calculation"] = DoctrineBlock(
        topic="Net Revenue Interest and Net Mineral Acres Calculation",
        keywords=["NRI", "NMA", "net revenue interest", "net mineral acres", "working interest", "royalty burden", "decimal interest"],
        conclusion_template=(
            "NRI is computed as the working interest minus all royalty burdens (lessor royalty, ORRI, NPRI). "
            "NMA equals gross acres multiplied by the undivided mineral interest fraction. Accurate NRI/NMA "
            "computation requires tracing every conveyance, reservation, and lease through the entire chain."
        ),
        reasoning_framework=(
            "STEP 1: Establish gross acreage from the legal description. For aliquot parts, compute: "
            "Section = 640 acres, Quarter = 160 acres, Half = 320 acres. For metes and bounds, use "
            "the acreage stated in the deed or compute from survey data. STEP 2: Trace mineral ownership "
            "fractions. Start with 100% (8/8) and apply each conveyance: if A owns 8/8 and conveys 1/2 "
            "minerals to B, then A = 4/8, B = 4/8. STEP 3: Apply Duhig rule if applicable — when a "
            "grantor warrants title but has previously conveyed a fraction, the warranty may estop the "
            "grantor from claiming the reserved interest. STEP 4: Compute NMA = Gross Acres x Mineral "
            "Interest Fraction. Example: 640 acres x 1/4 mineral interest = 160 NMA. STEP 5: Layer "
            "in lease terms. Working Interest (WI) starts at 100% of the leasehold. The lessor's royalty "
            "(e.g., 1/4) reduces WI to 75%. STEP 6: Subtract overriding royalty interests (ORRI) — "
            "typically carved from working interest by assignment. STEP 7: NRI = WI - all burdens. "
            "Example: 100% WI - 25% lessor royalty - 3% ORRI = 72% NRI (0.720000 decimal). "
            "STEP 8: For multiple tracts in a pooled unit, compute NRI per tract, then weight by "
            "tract's proportionate share of unit acreage."
        ),
        key_factors=[
            "Gross acreage must be accurately determined from legal description",
            "Each mineral conveyance changes the fractional ownership",
            "Duhig rule can redistribute interests when warranty exceeds ownership",
            "Lease royalty rate directly affects NRI",
            "ORRI and NPRI are additional burdens subtracted from WI",
            "Pooled unit participation is proportional to tract acreage",
            "Decimal interest must carry at least 6 decimal places",
        ],
        primary_authority=[
            "Duhig v. Peavy-Moore Lumber Co., 135 Tex. 503 (1940)",
            "Concord Oil Co. v. Pennzoil Exploration & Production Co., 966 S.W.2d 451 (Tex. 1998)",
            "AAPL Title Examination Standards",
            "Texas Land Title Association Standards",
        ],
        burden_holder="Party claiming revenue interest",
        adversary_position="Competing interest holder or operator disputing decimal allocation",
        counter_arguments=[
            "Fractional interest computation chain has an error",
            "Duhig rule application is disputed",
            "ORRI was not properly carved from working interest",
            "Pooled unit proportions are calculated incorrectly",
            "Outstanding NPRI was not accounted for",
        ],
        resolution_strategy=(
            "Build interest computation spreadsheet tracing every conveyance from sovereignty "
            "to present. Apply Duhig where warranty exceeds ownership. Layer in lease burdens. "
            "Cross-check NRI against division order decimal."
        ),
        entity_scope="All mineral interest owners, lessees, ORRI holders, NPRI holders",
        confidence=0.91,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Duhig v. Peavy-Moore Lumber Co., 135 Tex. 503 (1940)",
        issue_category=IssueCategory.INTEREST_COMPUTATION,
        interaction_edges=["warranty_deed_chain_analysis", "mineral_deed_conveyance", "oil_gas_lease_abstraction"],
    )

    # ─── DOCTRINE 5: GAP DETECTION ────────────────────────────────────
    doctrines["gap_detection_methodology"] = DoctrineBlock(
        topic="Gap Detection in Chain of Title",
        keywords=["gap", "break", "chain of title", "missing link", "wild deed", "curative", "title defect"],
        conclusion_template=(
            "A gap in the chain of title exists when no recorded instrument connects one owner to the "
            "next. Gaps can result from unrecorded conveyances, probate failures, missing heirship "
            "proceedings, or clerical errors. Each gap must be flagged as a title requirement on the "
            "run sheet with a specific curative recommendation."
        ),
        reasoning_framework=(
            "STEP 1: Build the complete chain of title from sovereignty or common source to present. "
            "For each link, the grantee of instrument N must be the grantor of instrument N+1. "
            "STEP 2: When a grantor appears who was never a grantee in a prior recorded instrument, "
            "a gap exists. STEP 3: Classify the gap type: (a) Unrecorded deed — the conveyance happened "
            "but was never recorded; (b) Probate gap — owner died and no probate or heirship affidavit "
            "was filed; (c) Name variance — grantor name doesn't exactly match prior grantee name; "
            "(d) Entity succession — corporate merger, name change, or dissolution not documented; "
            "(e) Tax sale — property sold for delinquent taxes, breaking normal chain. STEP 4: For each "
            "gap, determine the curative requirement: affidavit of heirship, muniment of title, "
            "correction deed, ratification, quitclaim from missing party, or quiet title suit. "
            "STEP 5: Assess gap severity — a gap in the mineral chain vs surface chain has different "
            "risk profiles. A gap within the last 25 years is more critical than a gap cured by "
            "limitation. STEP 6: Note all gaps on the run sheet in the requirements section with "
            "specific curative instructions."
        ),
        key_factors=[
            "Every grantee must appear as grantor in the next link",
            "Name variances are common and may not indicate a true gap",
            "Probate gaps are the most frequent type in older chains",
            "Texas 25-year statute of limitations can cure ancient gaps",
            "Tax sales create new chains independent of prior ownership",
            "Wild deeds are recorded but outside the chain — not constructive notice",
        ],
        primary_authority=[
            "Texas Property Code Sec. 13.001-13.002 (Recording)",
            "Texas Civil Practice & Remedies Code Sec. 16.021-16.030 (Limitations)",
            "Tex. Prop. Code Sec. 5.023 (Validating acts)",
            "TLTA Title Standard 1.10 (Gap in chain)",
        ],
        burden_holder="Title examiner identifying the gap",
        adversary_position="Party claiming title through the gap without curative",
        counter_arguments=[
            "25-year statute of limitations cures the gap",
            "Possession under recorded deed provides constructive notice",
            "Name variance is explained by marriage, divorce, or alias",
            "Entity succession is documented in Secretary of State records",
            "Tax records show continuous payment supporting ownership",
        ],
        resolution_strategy=(
            "Systematically walk the chain checking each link. Flag gaps by type and severity. "
            "Recommend specific curative instruments for each gap. Distinguish between gaps that "
            "can be cured by affidavit versus those requiring judicial action."
        ),
        entity_scope="All parties in chain, heirs, successors, entities",
        confidence=0.94,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="TLTA Title Standard 1.10",
        issue_category=IssueCategory.GAP_DETECTION,
        interaction_edges=["warranty_deed_chain_analysis", "probate_heirship_tracking", "name_variance_resolution"],
    )

    # ─── DOCTRINE 6: LEGAL DESCRIPTION PARSING ───────────────────────
    doctrines["legal_description_parsing"] = DoctrineBlock(
        topic="Legal Description Parsing and Validation",
        keywords=["legal description", "metes and bounds", "section block survey", "aliquot parts", "abstract number", "tract"],
        conclusion_template=(
            "Every instrument on the run sheet must have its legal description validated against the "
            "parent tract. Descriptions using Texas public land survey system (section-block-survey-abstract) "
            "must be cross-referenced. Metes and bounds descriptions require closure calculation. "
            "Partial tract conveyances must be identified and acreage verified."
        ),
        reasoning_framework=(
            "STEP 1: Identify the description system — Texas primarily uses the public land survey "
            "system (Section, Block, Township, Survey, Abstract Number). Some areas use lot-and-block "
            "from platted subdivisions. Rural tracts may use metes and bounds. STEP 2: For public land "
            "survey descriptions, extract and normalize: Section number, Block designation, Survey name "
            "(the original grantee), and Abstract number (county-assigned). STEP 3: Verify the abstract "
            "number matches county records. The abstract number is the key cross-reference in Texas "
            "county clerk records. STEP 4: For partial tract descriptions (e.g., 'the N/2 of Section 10'), "
            "compute the acreage. A standard section is 640 acres, but Texas sections vary. STEP 5: For "
            "metes and bounds, verify the description closes — the final call must return to the point "
            "of beginning. Non-closure indicates a drafting error requiring correction. STEP 6: When "
            "descriptions change between instruments (e.g., one uses abstract number, another uses "
            "section-block), confirm they describe the same tract by cross-referencing county records. "
            "STEP 7: Flag any ambiguous, conflicting, or incomplete legal descriptions as title "
            "requirements on the run sheet."
        ),
        key_factors=[
            "Abstract number is the primary cross-reference in Texas counties",
            "Section sizes in Texas are not uniform — verify actual acreage",
            "Metes and bounds must close to be valid",
            "Survey name refers to the original land grant recipient",
            "Description changes between instruments must be reconciled",
            "Partial tract conveyances require acreage computation",
        ],
        primary_authority=[
            "Texas General Land Office records and maps",
            "Texas Property Code Sec. 5.021 (Conveyance requirements)",
            "Sandel v. State, 115 S.W.2d 601 (Tex. 1938)",
            "AAPL Title Standards — Legal Description Requirements",
        ],
        burden_holder="Title examiner validating descriptions",
        adversary_position="Party claiming description covers different tract",
        counter_arguments=[
            "Ambiguous description can be resolved by extrinsic evidence",
            "Acreage discrepancy is within de minimis range",
            "Description references a recorded plat that controls",
            "Correction deed has been filed to cure description error",
            "Long-standing boundary by acquiescence controls",
        ],
        resolution_strategy=(
            "Extract all description components from each instrument. Cross-reference against "
            "county abstract records. Compute acreage for partial tracts. Flag ambiguities and "
            "recommend curative correction deeds where needed."
        ),
        entity_scope="All instruments in chain",
        confidence=0.89,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Sandel v. State, 115 S.W.2d 601 (Tex. 1938)",
        issue_category=IssueCategory.LEGAL_DESCRIPTION,
        interaction_edges=["warranty_deed_chain_analysis", "acreage_calculation_methods"],
    )

    # ─── DOCTRINE 7: RESERVATION AND EXCEPTION TRACKING ──────────────
    doctrines["reservation_exception_tracking"] = DoctrineBlock(
        topic="Reservation and Exception Tracking in Conveyance Chain",
        keywords=["reservation", "exception", "save and except", "mineral reservation", "royalty reservation", "life estate"],
        conclusion_template=(
            "Reservations create new interests retained by the grantor; exceptions exclude existing "
            "outstanding interests from the warranty. Both must be tracked on the run sheet as they "
            "affect the quantum of title conveyed and the interest computation for NRI/NMA."
        ),
        reasoning_framework=(
            "STEP 1: Distinguish between reservations and exceptions. A reservation is a new interest "
            "created by the grantor in the act of conveyance (e.g., 'grantor reserves 1/2 mineral interest'). "
            "An exception acknowledges an existing outstanding interest not being conveyed (e.g., "
            "'save and except that certain mineral deed recorded in Vol. 100, Pg. 50'). STEP 2: Parse "
            "the exact language of the reservation. Common forms: (a) Fractional mineral reservation — "
            "'an undivided 1/2 of all oil, gas, and other minerals'; (b) Term mineral reservation — "
            "'for a period of 20 years and so long thereafter as minerals are produced'; (c) Life estate "
            "reservation — 'for the life of grantor'; (d) Royalty reservation — 'an undivided 1/16 royalty "
            "interest'. STEP 3: Apply the Duhig rule: if a warranty deed grantor reserves minerals but "
            "does not own the full mineral estate (due to a prior outstanding mineral interest), the "
            "warranty may estop the grantor's reservation. STEP 4: Track each reservation as a separate "
            "line item on the run sheet. For mineral reservations, maintain a separate mineral ownership "
            "column showing the reserved interest. STEP 5: For exceptions, verify the referenced "
            "outstanding interest actually exists in the records. STEP 6: Determine whether a term "
            "mineral reservation has expired by checking the stated term and any production savings clause."
        ),
        key_factors=[
            "Reservations create new interests; exceptions recognize existing ones",
            "Duhig rule can eliminate a reservation when warranty conflicts",
            "Term mineral reservations may have expired",
            "Life estate reservations terminate at grantor's death",
            "Royalty reservations are distinct from mineral reservations",
            "Every reservation/exception modifies the interest computation",
        ],
        primary_authority=[
            "Duhig v. Peavy-Moore Lumber Co., 135 Tex. 503 (1940)",
            "Luckel v. White, 819 S.W.2d 459 (Tex. 1991)",
            "Estate of Tengg v. Boswell, 554 S.W.3d 35 (Tex. App. 2018)",
            "Texas Property Code Sec. 5.001 (Reservations in conveyances)",
        ],
        burden_holder="Party relying on reservation or claiming under exception",
        adversary_position="Grantee claiming full title unencumbered by reservation",
        counter_arguments=[
            "Reservation language is ambiguous — mineral vs royalty",
            "Duhig rule eliminates the reservation",
            "Term reservation has expired",
            "Life estate reservation terminated at death",
            "Exception references non-existent instrument",
        ],
        resolution_strategy=(
            "Catalog every reservation and exception in the chain. Track their effect on "
            "mineral ownership fractions. Apply Duhig analysis where warranties conflict "
            "with reservations. Verify term expirations and life estate terminations."
        ),
        entity_scope="Grantors making reservations, outstanding interest holders",
        confidence=0.91,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Duhig v. Peavy-Moore Lumber Co., 135 Tex. 503 (1940)",
        issue_category=IssueCategory.RESERVATION_EXCEPTION,
        interaction_edges=["nri_nma_calculation", "mineral_deed_conveyance", "warranty_deed_chain_analysis"],
    )

    # ─── DOCTRINE 8: PROBATE AND HEIRSHIP TRACKING ───────────────────
    doctrines["probate_heirship_tracking"] = DoctrineBlock(
        topic="Probate and Heirship Tracking in Title Chain",
        keywords=["probate", "heirship", "affidavit of heirship", "will", "intestate", "muniment of title", "heirs"],
        conclusion_template=(
            "When a record owner dies, title passes to heirs (intestate) or devisees (testate). "
            "The run sheet must document the method of title transfer — probate proceeding, "
            "muniment of title, affidavit of heirship, or determination of heirship. Each method "
            "has different evidentiary weight and may create title requirements."
        ),
        reasoning_framework=(
            "STEP 1: Identify the deceased record owner and the date of death. If death occurred "
            "before the next recorded conveyance, a probate gap exists. STEP 2: Search county "
            "probate records and deed records for: (a) Will and order admitting will to probate; "
            "(b) Muniment of title (simplified probate with no administration); (c) Independent "
            "or dependent administration letters; (d) Affidavit of heirship. STEP 3: For testate "
            "succession — read the will to determine who receives the mineral interests. Specific "
            "devises control over general devises. A residuary clause catches property not "
            "specifically devised. STEP 4: For intestate succession — apply Texas Estates Code "
            "Chapter 201. Surviving spouse takes 1/3 of personal property and life estate in 1/3 "
            "of land (if children); if no children, spouse takes all community property and 1/2 "
            "separate property. STEP 5: An affidavit of heirship is NOT a probate proceeding — it "
            "is a sworn statement by a disinterested party. It becomes prima facie evidence of "
            "heirship after 5 years of recording. STEP 6: Verify that all heirs or devisees are "
            "accounted for. If one heir is missing, the title has a defect. STEP 7: Track the "
            "fractional interests of each heir/devisee on the run sheet."
        ),
        key_factors=[
            "Death of record owner creates probate gap requiring documentation",
            "Testate vs intestate succession follows different rules",
            "Affidavit of heirship is prima facie after 5 years but not conclusive",
            "Muniment of title is preferred simplified Texas probate method",
            "All heirs must be identified to avoid fractional interest gaps",
            "Community property vs separate property affects inheritance shares",
        ],
        primary_authority=[
            "Texas Estates Code Ch. 201 (Intestate succession)",
            "Texas Estates Code Ch. 256-258 (Probate of wills)",
            "Texas Estates Code Sec. 203.001 (Determination of heirship)",
            "Texas Estates Code Sec. 257.001 (Muniment of title)",
        ],
        burden_holder="Heir or devisee claiming through deceased owner",
        adversary_position="Competing claimant or unknown heir",
        counter_arguments=[
            "Unknown heirs may exist who were not identified",
            "Will may have been contested or revoked",
            "Affidavit of heirship contains errors or omissions",
            "Community property characterization is disputed",
            "Adopted or illegitimate children have inheritance rights",
        ],
        resolution_strategy=(
            "Search probate and deed records for any heirship documentation. Verify all heirs "
            "identified. Compute fractional interests per Texas Estates Code. Flag missing "
            "heirs or inadequate documentation as title requirements."
        ),
        entity_scope="Decedents, heirs, devisees, administrators, executors",
        confidence=0.90,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Texas Estates Code Ch. 201",
        issue_category=IssueCategory.PROBATE_HEIRSHIP,
        interaction_edges=["gap_detection_methodology", "nri_nma_calculation", "dormant_mineral_identification"],
    )

    # ─── DOCTRINE 9: ASSIGNMENT TRACKING ──────────────────────────────
    doctrines["assignment_tracking"] = DoctrineBlock(
        topic="Lease Assignment and Working Interest Tracking",
        keywords=["assignment", "partial assignment", "ORRI", "working interest", "farmout", "sublease", "overriding royalty"],
        conclusion_template=(
            "Assignments transfer all or part of the lessee's working interest to an assignee. "
            "Partial assignments may cover specific depths, formations, or acreage. ORRI is "
            "typically carved from working interest upon assignment. The run sheet must track "
            "each assignment and its effect on working interest and royalty burden allocation."
        ),
        reasoning_framework=(
            "STEP 1: Determine whether the assignment is full or partial. A full assignment "
            "transfers the entire leasehold interest; a partial assignment transfers a specified "
            "portion (by depth, formation, acreage, or fractional interest). STEP 2: Identify "
            "any ORRI retained by the assignor. ORRI is carved from working interest and burdens "
            "the assigned interest. STEP 3: For farmout agreements, the farmee earns an interest "
            "by drilling — the assignment is triggered upon completion of obligations. STEP 4: "
            "Track the chain of assignments: Lessee A assigns to B, B assigns to C — each must "
            "be recorded. STEP 5: Verify that the assignor had authority to assign (check for "
            "consent-to-assign clauses in the underlying lease). STEP 6: Compute the working "
            "interest and NRI for each party after each assignment. STEP 7: Note any depth "
            "severance created by partial assignment — the assignor may retain interests below "
            "or above the assigned formation."
        ),
        key_factors=[
            "Full vs partial assignment affects scope of interest transferred",
            "ORRI carved from working interest burdens the leasehold",
            "Consent-to-assign clauses may restrict assignment rights",
            "Farmout agreements create conditional assignments",
            "Depth-limited assignments create vertically severed interests",
            "Each assignment modifies NRI computation",
        ],
        primary_authority=[
            "Texas Natural Resources Code Sec. 91.001",
            "Hlavinka v. Hancock, 116 S.W.3d 412 (Tex. App. 2003)",
            "Sunac Petroleum Corp. v. Parkes, 416 S.W.2d 798 (Tex. 1967)",
            "AAPL Form 610-1989 (Model Form Operating Agreement)",
        ],
        burden_holder="Assignee claiming working interest",
        adversary_position="Assignor or lessor disputing assignment validity",
        counter_arguments=[
            "Assignment violated consent-to-assign clause",
            "Farmout conditions were not fully satisfied",
            "ORRI burden exceeds 5% industry standard",
            "Partial assignment description is ambiguous",
            "Assignor did not own the interest purportedly assigned",
        ],
        resolution_strategy=(
            "Track every assignment in chronological order. Compute WI and ORRI at each step. "
            "Verify assignor had authority and interest to assign. Note depth or formation "
            "limitations. Update NRI computation after each assignment."
        ),
        entity_scope="Lessees, assignors, assignees, ORRI holders, farmees",
        confidence=0.89,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Sunac Petroleum Corp. v. Parkes, 416 S.W.2d 798 (Tex. 1967)",
        issue_category=IssueCategory.LEASE_ANALYSIS,
        interaction_edges=["oil_gas_lease_abstraction", "nri_nma_calculation"],
    )

    # ─── DOCTRINE 10: POOLING AND UNITIZATION ─────────────────────────
    doctrines["pooling_unit_analysis"] = DoctrineBlock(
        topic="Pooling and Unitization Effects on Run Sheet",
        keywords=["pooling", "unitization", "pooled unit", "DPU", "unit designation", "proration", "allocation"],
        conclusion_template=(
            "Pooling combines multiple tracts or interests into a single unit for drilling and "
            "production purposes. The run sheet must identify all pooled unit designations, "
            "verify pooling authority in each lease, and compute each tract's proportionate "
            "share of unit production based on acreage participation."
        ),
        reasoning_framework=(
            "STEP 1: Identify all Designation of Pooled Unit (DPU) instruments affecting the tract. "
            "Record the unit name, effective date, total unit acreage, and the tract's acreage within "
            "the unit. STEP 2: Verify that each lease within the unit grants pooling authority. Check "
            "for acreage limitations in pooling clauses (e.g., '640 acres plus 10% tolerance'). "
            "STEP 3: Compute the tract's participation factor: Tract NMA / Total Unit NMA. This "
            "determines the proportion of unit production allocated to the tract. STEP 4: Check for "
            "Pugh clause implications — if a lease has a Pugh clause, only the pooled acreage is "
            "held by production in the secondary term. STEP 5: For force pooling (Railroad Commission "
            "orders), verify the RRC order and its terms. STEP 6: Track unit amendments — acreage "
            "additions, reductions, or reformation of unit boundaries. STEP 7: Compute NRI within "
            "the unit context: Tract NRI x Tract Participation Factor = Effective Unit NRI."
        ),
        key_factors=[
            "Pooling authority must exist in each affected lease",
            "Acreage limitations in pooling clauses must be respected",
            "Participation factor = Tract NMA / Unit NMA",
            "Pugh clause limits HBP to pooled acreage only",
            "Force pooling by RRC order has specific regulatory requirements",
            "Unit amendments must be tracked and reflected on run sheet",
        ],
        primary_authority=[
            "Texas Natural Resources Code Sec. 102.001 et seq. (Mineral Interest Pooling Act)",
            "Texaco, Inc. v. Lettermann, 343 S.W.3d 726 (Tex. 2011)",
            "Jones v. Killingsworth, 403 S.W.2d 325 (Tex. 1966)",
            "Railroad Commission Statewide Rule 37 and 38",
        ],
        burden_holder="Operator claiming valid pooling",
        adversary_position="Mineral owner challenging pooling validity or participation share",
        counter_arguments=[
            "Lease pooling clause does not authorize the pool size created",
            "Pugh clause released the tract from the unit",
            "Force pooling order was improperly granted",
            "Unit was amended without consent of all interest holders",
            "Participation factor computation contains errors",
        ],
        resolution_strategy=(
            "Identify all DPU instruments. Verify pooling authority in each lease. Compute "
            "participation factors. Check Pugh clause effects. Track unit amendments. "
            "Reflect unit participation in NRI computation."
        ),
        entity_scope="Operators, lessees, lessors, mineral owners within unit",
        confidence=0.88,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Texas Natural Resources Code Sec. 102.001",
        issue_category=IssueCategory.LEASE_ANALYSIS,
        interaction_edges=["oil_gas_lease_abstraction", "nri_nma_calculation"],
    )

    # ─── DOCTRINE 11: RUN SHEET FORMAT STANDARDS ──────────────────────
    doctrines["runsheet_format_standards"] = DoctrineBlock(
        topic="Run Sheet Formatting Standards and Best Practices",
        keywords=["run sheet", "format", "columns", "abstract", "title report", "entry", "remarks"],
        conclusion_template=(
            "A properly formatted run sheet presents the chain of title in chronological order with "
            "standardized columns: Entry Number, Date, Recording Reference (Vol/Pg or CFN), Grantor, "
            "Grantee, Instrument Type, Legal Description, Consideration, and Remarks. The remarks "
            "column captures reservations, exceptions, and other material terms."
        ),
        reasoning_framework=(
            "STEP 1: Establish the header block — County, State, Legal Description of the tract being "
            "examined, Effective Date, Prepared By, Client, and Scope of Examination. STEP 2: Each "
            "run sheet entry follows a standard format: sequential entry number, instrument date, "
            "recording reference (Volume/Page for older instruments, Clerk's File Number for newer), "
            "grantor(s), grantee(s), instrument type, legal description as it appears in the instrument, "
            "consideration, and a remarks field. STEP 3: The remarks field captures critical information: "
            "mineral reservations with exact language, exception references, Duhig issues, warranty "
            "limitations, lease terms, and other material provisions. STEP 4: Separate the run sheet "
            "into sections: (a) Chain of Title — conveyances, (b) Mineral Interests — severed minerals, "
            "(c) Leases — current and expired, (d) Encumbrances — liens, judgments, lis pendens, "
            "(e) Requirements — gaps, curative items. STEP 5: Use consistent date format (MM/DD/YYYY). "
            "STEP 6: Cross-reference related instruments by entry number. STEP 7: The interest "
            "computation summary follows the chain, showing current ownership fractions."
        ),
        key_factors=[
            "Chronological order is essential for chain readability",
            "Recording reference must be exact for verification",
            "Remarks column captures the substantive analysis",
            "Separate sections for surface, mineral, leases, encumbrances",
            "Interest computation summary derives from the chain entries",
            "Header must identify scope and effective date",
        ],
        primary_authority=[
            "AAPL Form 56 (Run Sheet form)",
            "AAPL Title Examination Standards",
            "TLTA Title Standards",
            "Industry standard practice (Permian Basin custom)",
        ],
        burden_holder="Landman preparing the run sheet",
        adversary_position="Reviewing attorney or client finding deficiencies",
        counter_arguments=[
            "Alternative format is acceptable if all data is present",
            "Electronic run sheets may differ from paper format",
            "Custom format per client requirements may vary",
            "Summary format may be acceptable for preliminary review",
            "Stand-up examination uses abbreviated format",
        ],
        resolution_strategy=(
            "Follow AAPL Form 56 structure. Ensure all material information is captured. "
            "Use consistent formatting throughout. Cross-reference related entries. "
            "Provide clear interest computation summary."
        ),
        entity_scope="Landmen, title examiners, attorneys, clients",
        confidence=0.95,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="AAPL Form 56",
        issue_category=IssueCategory.RUNSHEET_FORMAT,
        interaction_edges=["warranty_deed_chain_analysis", "nri_nma_calculation"],
    )

    # ─── DOCTRINE 12: AFTER-ACQUIRED TITLE / ESTOPPEL BY DEED ────────
    doctrines["after_acquired_title"] = DoctrineBlock(
        topic="After-Acquired Title and Estoppel by Deed",
        keywords=["after-acquired title", "estoppel by deed", "warranty", "estoppel", "feed the estoppel"],
        conclusion_template=(
            "Under the after-acquired title doctrine (estoppel by deed), when a grantor conveys "
            "by warranty deed property they do not own, and later acquires that title, the subsequently "
            "acquired title automatically inures to the benefit of the grantee. This doctrine is critical "
            "in run sheet analysis when grantor conveyed before receiving title."
        ),
        reasoning_framework=(
            "STEP 1: Identify the warranty deed that conveyed title the grantor did not yet own. "
            "STEP 2: Verify the grantor subsequently acquired the title (by deed, probate, or otherwise). "
            "STEP 3: Under Texas law, the warranty in the deed creates an estoppel — the grantor is "
            "estopped from claiming the after-acquired title against the grantee. STEP 4: The doctrine "
            "applies ONLY to warranty deeds (general or special), NOT to quitclaim deeds. A quitclaim "
            "conveys only what the grantor owns at that moment. STEP 5: If the grantor conveyed 100% "
            "minerals by warranty but only owned 50%, and later acquires the other 50%, the after-acquired "
            "50% feeds through to the grantee. STEP 6: This interacts with the Duhig rule — both involve "
            "warranty overreach. STEP 7: Document on the run sheet that title passed via estoppel, "
            "referencing both the warranty deed and the subsequent acquisition."
        ),
        key_factors=[
            "Only warranty deeds trigger after-acquired title doctrine",
            "Quitclaim deeds do not carry estoppel",
            "Title automatically passes without new instrument needed",
            "Interacts with Duhig rule in mineral conveyance context",
            "Must document the estoppel chain on run sheet",
            "BFP protection may complicate the analysis",
        ],
        primary_authority=[
            "Duhig v. Peavy-Moore Lumber Co., 135 Tex. 503 (1940)",
            "York v. Hutcheson, 15 S.W. 806 (Tex. 1891)",
            "Houston Oil Co. of Texas v. Kimball, 122 Tex. 560 (1932)",
        ],
        burden_holder="Grantee claiming after-acquired title",
        adversary_position="Grantor or subsequent purchaser from grantor",
        counter_arguments=[
            "Deed was a quitclaim, not a warranty deed",
            "Grantor never actually acquired the after-title",
            "Third party BFP intervened before estoppel could attach",
            "Statute of limitations bars the estoppel claim",
        ],
        resolution_strategy=(
            "Identify warranty deeds where grantor conveyed more than owned. Trace grantor's "
            "subsequent acquisition. Apply after-acquired title doctrine. Document estoppel "
            "passage on run sheet with cross-references."
        ),
        entity_scope="Warranty deed grantors and grantees",
        confidence=0.87,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Duhig v. Peavy-Moore Lumber Co., 135 Tex. 503 (1940)",
        issue_category=IssueCategory.CHAIN_OF_TITLE,
        interaction_edges=["warranty_deed_chain_analysis", "reservation_exception_tracking"],
    )

    # ─── DOCTRINE 13: DORMANT MINERAL INTEREST IDENTIFICATION ────────
    doctrines["dormant_mineral_identification"] = DoctrineBlock(
        topic="Dormant Mineral Interest Identification",
        keywords=["dormant mineral", "abandoned mineral", "unused mineral", "mineral interest act", "lapsed mineral"],
        conclusion_template=(
            "Texas adopted the Texas Mineral Interest Pooling Act but has NOT enacted a dormant "
            "mineral interest act like some other states. Old mineral reservations, even if unused "
            "for decades, remain valid in Texas. The run sheet must identify all outstanding mineral "
            "interests regardless of age and note any potential marketability issues."
        ),
        reasoning_framework=(
            "STEP 1: Texas does NOT have a dormant mineral interest statute. Unlike states with "
            "mineral lapse statutes, severed mineral interests in Texas persist indefinitely unless "
            "abandoned by affirmative act. STEP 2: Identify all mineral reservations and mineral "
            "deeds in the chain, regardless of age. A 1920 mineral reservation is as valid as a "
            "2024 reservation. STEP 3: Check whether any term mineral reservations have expired. "
            "A reservation 'for 20 years' expires at the end of the term unless saved by production "
            "or a savings clause. STEP 4: Trace the mineral interest through heirship. If the original "
            "mineral reservation holder died intestate, their fractional interest may now be split among "
            "dozens of heirs. STEP 5: Flag all outstanding mineral interests on the run sheet. Even "
            "if they appear 'dormant' (no activity for decades), they remain valid. STEP 6: For "
            "leasing purposes, outstanding mineral interests must be addressed — either leased from "
            "the current owner or excepted from the lease obligations."
        ),
        key_factors=[
            "Texas has no dormant mineral interest statute",
            "Severed mineral interests persist indefinitely in Texas",
            "Term reservations may expire but perpetual reservations do not",
            "Heirship fractionation multiplies outstanding interests over generations",
            "All outstanding interests must be identified for accurate NRI",
            "Unleased outstanding minerals create title requirements",
        ],
        primary_authority=[
            "Texas Property Code (no mineral lapse provision)",
            "Bagby v. Bredthauer, 627 S.W.2d 190 (Tex. App. 1981)",
            "Natural Gas Pipeline Co. of America v. Pool, 124 S.W.3d 188 (Tex. 2003)",
        ],
        burden_holder="Party asserting mineral interest has lapsed",
        adversary_position="Mineral interest holder claiming perpetual ownership",
        counter_arguments=[
            "Other states' dormant mineral acts do not apply in Texas",
            "Adverse possession of minerals requires actual production",
            "Tax payment alone does not establish mineral ownership",
            "Limitation period has not run absent ouster or repudiation",
        ],
        resolution_strategy=(
            "Identify every outstanding mineral interest in the chain regardless of age. "
            "Trace through heirship for deceased holders. Flag all as active interests "
            "on the run sheet. Recommend leasing or curative as appropriate."
        ),
        entity_scope="Mineral interest holders, their heirs, surface owners",
        confidence=0.88,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Natural Gas Pipeline Co. v. Pool, 124 S.W.3d 188 (Tex. 2003)",
        issue_category=IssueCategory.MINERAL_RIGHTS,
        interaction_edges=["probate_heirship_tracking", "reservation_exception_tracking", "nri_nma_calculation"],
    )

    # ─── DOCTRINE 14: ROYALTY DEED ANALYSIS ───────────────────────────
    doctrines["royalty_deed_analysis"] = DoctrineBlock(
        topic="Royalty Deed and Non-Participating Royalty Interest Analysis",
        keywords=["royalty deed", "NPRI", "royalty interest", "non-participating", "participating royalty", "royalty burden"],
        conclusion_template=(
            "A royalty deed conveys only the right to receive royalties from production, not the "
            "executive rights to lease. An NPRI holder cannot execute leases or receive bonus/delay "
            "rentals. The run sheet must distinguish between mineral interests (full bundle) and "
            "royalty interests (royalty stream only) to correctly compute NRI."
        ),
        reasoning_framework=(
            "STEP 1: Determine whether the instrument conveys a mineral interest or royalty interest. "
            "The language 'an undivided 1/16 royalty interest' conveys royalty only; 'an undivided 1/16 "
            "of the minerals' conveys the full mineral bundle. STEP 2: Apply Moser v. U.S. Steel — "
            "the mineral estate consists of five attributes: (a) right to develop (executive rights), "
            "(b) right to lease (executive), (c) right to receive bonus, (d) right to receive delay "
            "rentals, (e) right to receive royalty. A royalty interest includes only (e). STEP 3: "
            "Determine if the royalty interest is participating (PRI) or non-participating (NPRI). "
            "PRI holders share in lease bonus proportionate to their interest; NPRI holders do not. "
            "STEP 4: Compute the NPRI burden. An NPRI of 1/16 under a lease with 1/4 royalty means "
            "the NPRI holder receives 1/16 of production, and the mineral owner's royalty is reduced "
            "to 3/16 (1/4 minus 1/16). STEP 5: The 'double fraction' issue: does '1/2 of 1/8 royalty' "
            "mean 1/16 of production or 1/2 of whatever royalty the lease provides? Texas courts have "
            "struggled with this. STEP 6: Track all royalty interests on the run sheet in a separate "
            "section from mineral interests. Show the burden on NRI."
        ),
        key_factors=[
            "Mineral interest includes full bundle of rights; royalty is only the royalty stream",
            "NPRI holders cannot lease or receive bonus/rentals",
            "NPRI burdens the mineral owner's royalty, not the working interest",
            "Double fraction problem requires careful language analysis",
            "PRI vs NPRI distinction affects lease bonus allocation",
            "All royalty interests reduce the mineral owner's effective royalty",
        ],
        primary_authority=[
            "Moser v. U.S. Steel Corp., 676 S.W.2d 99 (Tex. 1984)",
            "Lesley v. Veterans Land Board, 352 S.W.3d 479 (Tex. 2011)",
            "Hysaw v. Dawkins, 483 S.W.3d 1 (Tex. 2016)",
            "Plainsman Trading Co. v. Crews, 898 S.W.2d 786 (Tex. 1995)",
        ],
        burden_holder="Royalty interest claimant",
        adversary_position="Mineral owner disputing extent of royalty burden",
        counter_arguments=[
            "Instrument actually conveyed a mineral interest, not just royalty",
            "Double fraction language is ambiguous requiring extrinsic evidence",
            "NPRI has been extinguished by merger or reconveyance",
            "NPRI fraction exceeds the lease royalty rate",
        ],
        resolution_strategy=(
            "Classify each royalty conveyance as mineral vs royalty using Moser factors. "
            "Determine PRI vs NPRI. Compute burden on NRI. Track separately on run sheet. "
            "Address double fraction issues with applicable case law."
        ),
        entity_scope="Royalty interest holders, mineral owners, lessees",
        confidence=0.88,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Moser v. U.S. Steel Corp., 676 S.W.2d 99 (Tex. 1984)",
        issue_category=IssueCategory.MINERAL_RIGHTS,
        interaction_edges=["mineral_deed_conveyance", "nri_nma_calculation", "oil_gas_lease_abstraction"],
    )

    # ─── DOCTRINE 15: SURFACE/MINERAL ESTATE SEPARATION ──────────────
    doctrines["surface_mineral_separation"] = DoctrineBlock(
        topic="Surface and Mineral Estate Separation Tracing",
        keywords=["surface estate", "mineral estate", "severed estate", "dominant estate", "accommodation doctrine", "surface use"],
        conclusion_template=(
            "Once the mineral estate is severed from the surface, two independent chains of title "
            "exist. The run sheet must maintain parallel chains after severance. The mineral estate "
            "is dominant — the mineral owner has the right to use the surface reasonably necessary "
            "for mineral development, subject to the accommodation doctrine."
        ),
        reasoning_framework=(
            "STEP 1: Identify the severance instrument — the first deed that separated minerals "
            "from surface. This creates two chains that must be tracked independently on the run "
            "sheet. STEP 2: After severance, surface conveyances do not affect the mineral chain "
            "and vice versa. A warranty deed conveying 'the surface only' or 'subject to outstanding "
            "mineral interests' continues the surface chain. STEP 3: Apply the dominant estate "
            "doctrine — the mineral estate is dominant over the surface estate. The mineral owner "
            "or lessee has an implied easement to use the surface for mineral development. "
            "STEP 4: Apply the accommodation doctrine (Getty Oil Co. v. Jones) — when the mineral "
            "owner has reasonable alternatives that allow both surface and mineral use, the mineral "
            "owner must accommodate existing surface use. STEP 5: Track any surface use agreements, "
            "surface damage agreements, or surface waivers that modify the default relationship. "
            "STEP 6: If minerals and surface later reunify under one owner, note the merger on the "
            "run sheet. A subsequent conveyance without reservation keeps them unified."
        ),
        key_factors=[
            "Severance creates two independent chains of title",
            "Mineral estate is dominant over surface estate",
            "Accommodation doctrine limits mineral owner's surface use in some cases",
            "Surface use agreements may modify default rights",
            "Reunification occurs when one owner holds both estates",
            "Subsequent conveyance without reservation maintains unified estate",
        ],
        primary_authority=[
            "Getty Oil Co. v. Jones, 470 S.W.2d 618 (Tex. 1971)",
            "Coyote Lake Ranch, LLC v. City of Lubbock, 498 S.W.3d 53 (Tex. 2016)",
            "Texas Natural Resources Code Sec. 92.001",
        ],
        burden_holder="Party claiming surface or mineral rights",
        adversary_position="Opposing estate owner contesting use rights",
        counter_arguments=[
            "Surface use was not reasonably necessary for mineral operations",
            "Accommodation doctrine requires mineral owner to use alternatives",
            "Surface use agreement limits mineral owner's access",
            "Estates have been reunified by common ownership",
        ],
        resolution_strategy=(
            "Identify the severance point in the chain. Maintain parallel chains from that "
            "point forward. Note the dominant estate doctrine. Track surface use agreements. "
            "Document any reunification events."
        ),
        entity_scope="Surface owners, mineral owners, lessees, operators",
        confidence=0.90,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Getty Oil Co. v. Jones, 470 S.W.2d 618 (Tex. 1971)",
        issue_category=IssueCategory.MINERAL_RIGHTS,
        interaction_edges=["mineral_deed_conveyance", "reservation_exception_tracking"],
    )

    # ─── DOCTRINES 16-45: Additional domain coverage ─────────────────

    doctrines["name_variance_resolution"] = DoctrineBlock(
        topic="Name Variance and Identity Resolution in Chain",
        keywords=["name variance", "aka", "fka", "identity", "same person", "idem sonans"],
        conclusion_template="Name variances between instruments must be resolved to maintain chain continuity. Minor variances may be addressed by affidavit; material variances require curative action.",
        reasoning_framework="STEP 1: Compare grantor name in current instrument with grantee name in prior instrument. STEP 2: Apply idem sonans doctrine — names that sound alike are treated as the same. STEP 3: Check for recorded name affidavits, marriage certificates, or divorce decrees explaining the variance. STEP 4: Common variances include: middle name/initial variations, maiden vs married names, Sr/Jr designations, misspellings. STEP 5: If variance cannot be explained by available records, flag as curative requirement — request affidavit of identity or correction deed.",
        key_factors=["Idem sonans treats sound-alike names as equivalent", "Marriage/divorce name changes are common variances", "Affidavit of identity can cure most name variances", "Material name differences require correction deeds"],
        primary_authority=["TLTA Title Standard 1.20 (Name variances)", "Texas Property Code Sec. 13.001"],
        burden_holder="Party asserting identity of differently-named individuals",
        adversary_position="Party claiming they are different persons",
        counter_arguments=["Names are too dissimilar for idem sonans", "No supporting documentation exists", "Two different persons share similar names"],
        resolution_strategy="Apply idem sonans. Check supporting records. Request affidavit of identity or correction deed for unresolved variances.",
        entity_scope="All parties in chain with name discrepancies",
        confidence=0.88,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="TLTA Title Standard 1.20",
        issue_category=IssueCategory.GAP_DETECTION,
        interaction_edges=["gap_detection_methodology", "warranty_deed_chain_analysis"],
    )

    doctrines["tax_lien_verification"] = DoctrineBlock(
        topic="Tax Lien and Tax Sale Verification",
        keywords=["tax lien", "tax sale", "delinquent taxes", "tax deed", "redemption", "tax foreclosure"],
        conclusion_template="Ad valorem tax liens are superior to all other liens. Tax sales can break the chain of title. The run sheet must verify tax payment status and identify any tax sales in the chain.",
        reasoning_framework="STEP 1: Texas Property Tax Code creates an automatic statutory lien for ad valorem taxes that is superior to all other liens. STEP 2: If taxes are delinquent, a tax suit and foreclosure can result in a tax sale deed that creates a new chain of title. STEP 3: The tax sale deed must be examined for compliance with procedural requirements — proper notice, service, and right of redemption. STEP 4: Texas allows a 2-year redemption period for homestead and agricultural property, 180 days for all other property. STEP 5: Verify current tax status — any delinquency is a title requirement.",
        key_factors=["Tax liens are superior to all other liens", "Tax sales create new chains of title", "Redemption periods must be verified", "Procedural defects can void tax sales", "Current tax status must be verified"],
        primary_authority=["Texas Tax Code Ch. 32-34", "City of Houston v. Guthrie, 332 S.W.3d 578 (Tex. App. 2009)"],
        burden_holder="Tax sale purchaser",
        adversary_position="Former owner claiming procedural defects",
        counter_arguments=["Notice requirements not met", "Redemption period not expired", "Tax amount calculation was incorrect", "Property was exempt"],
        resolution_strategy="Verify tax payment status. Examine any tax sale deeds for compliance. Check redemption period expiration. Flag delinquencies as requirements.",
        entity_scope="Property owners, taxing authorities, tax sale purchasers",
        confidence=0.87,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Texas Tax Code Ch. 32",
        issue_category=IssueCategory.CHAIN_OF_TITLE,
        interaction_edges=["gap_detection_methodology"],
    )

    doctrines["acreage_calculation_methods"] = DoctrineBlock(
        topic="Acreage Calculation Methods for Run Sheet",
        keywords=["acreage", "gross acres", "net acres", "aliquot parts", "section", "survey", "vara"],
        conclusion_template="Acreage must be accurately calculated from legal descriptions using aliquot parts, survey records, or metes-and-bounds computation. Texas sections are not uniform — actual acreage must be verified against GLO records.",
        reasoning_framework="STEP 1: For aliquot part descriptions, compute from the parent tract acreage. Standard section = 640 acres, but Texas survey sections vary. STEP 2: For metes and bounds, compute area from bearing-distance calls using coordinate geometry. STEP 3: The vara (33.33 inches) is the traditional Texas unit of measure. 1 vara = 2.778 feet. A league = 4,428 acres. A labor = 177.1 acres. STEP 4: Verify section acreage against Texas General Land Office (GLO) records — many Texas sections are irregular. STEP 5: For partial tracts, compute proportional acreage. STEP 6: Cross-check computed acreage against acreage stated in the deed.",
        key_factors=["Texas sections are not uniformly 640 acres", "GLO records provide definitive survey data", "Vara is the traditional Texas measurement unit", "Metes and bounds require coordinate geometry", "Stated acreage may differ from computed acreage"],
        primary_authority=["Texas General Land Office records", "Texas Natural Resources Code Sec. 21.001"],
        burden_holder="Party computing acreage for interest calculations",
        adversary_position="Party disputing acreage computation",
        counter_arguments=["GLO records show different acreage than deed states", "Survey was inaccurate", "Overlap with adjacent survey exists"],
        resolution_strategy="Use GLO records as primary source. Compute aliquot parts from actual survey acreage. Verify metes and bounds closure. Note discrepancies on run sheet.",
        entity_scope="All parties affected by acreage computation",
        confidence=0.89,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Texas General Land Office survey records",
        issue_category=IssueCategory.LEGAL_DESCRIPTION,
        interaction_edges=["legal_description_parsing", "nri_nma_calculation"],
    )

    doctrines["quitclaim_deed_effect"] = DoctrineBlock(
        topic="Quitclaim Deed Effect on Chain of Title",
        keywords=["quitclaim", "quitclaim deed", "no warranty", "as-is", "release"],
        conclusion_template="A quitclaim deed conveys only the interest the grantor owns at the time of execution, with no warranty of title. It does not trigger after-acquired title doctrine and may not provide constructive notice under Texas recording statutes.",
        reasoning_framework="STEP 1: A quitclaim deed conveys whatever interest the grantor has, if any. It provides no warranty against defects. STEP 2: Under Texas law, a quitclaim deed may not impart constructive notice to subsequent purchasers — it puts purchasers on inquiry notice only. STEP 3: Quitclaims are commonly used for curative purposes — clearing up clouds on title, releasing claims, or correcting chain issues. STEP 4: The after-acquired title doctrine does NOT apply to quitclaim deeds. If the grantor later acquires title, it does not pass to the grantee. STEP 5: On the run sheet, note that the instrument is a quitclaim and flag the absence of warranty protection.",
        key_factors=["No warranty protection for grantee", "No after-acquired title doctrine applies", "May not provide constructive notice in Texas", "Commonly used for curative purposes", "Conveys only interest owned at execution"],
        primary_authority=["Texas Property Code Sec. 5.023", "Geodyne Resources, Ltd. v. Newton Corp., 349 S.W.3d 2 (Tex. App. 2011)"],
        burden_holder="Grantee under quitclaim deed",
        adversary_position="Third party with competing claim",
        counter_arguments=["Grantor owned no interest at time of quitclaim", "Quitclaim does not provide constructive notice", "Subsequent BFP takes priority"],
        resolution_strategy="Verify grantor's interest at time of quitclaim. Note absence of warranty on run sheet. Assess whether additional title protection is needed.",
        entity_scope="Quitclaim grantors and grantees",
        confidence=0.88,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Texas Property Code Sec. 5.023",
        issue_category=IssueCategory.CHAIN_OF_TITLE,
        interaction_edges=["warranty_deed_chain_analysis", "after_acquired_title"],
    )

    doctrines["correction_deed_handling"] = DoctrineBlock(
        topic="Correction Deed and Scrivener's Error Resolution",
        keywords=["correction deed", "corrective deed", "scrivener's error", "reformation", "nunc pro tunc"],
        conclusion_template="Correction deeds cure errors in original instruments — misspelled names, incorrect legal descriptions, wrong recording references. The run sheet must show both the original and corrective instrument, cross-referenced.",
        reasoning_framework="STEP 1: Identify the error in the original instrument. STEP 2: Verify the correction deed references the original instrument and specifically identifies the error being corrected. STEP 3: A correction deed relates back to the date of the original instrument for chain of title purposes. STEP 4: Only scrivener's (clerical) errors can be corrected — not substantive changes to the transaction. STEP 5: Both parties to the original instrument should execute the correction deed. STEP 6: Record both instruments on the run sheet with cross-references.",
        key_factors=["Correction relates back to original instrument date", "Only clerical errors, not substantive changes", "Both original parties should execute", "Must reference the original instrument", "Run sheet shows both with cross-reference"],
        primary_authority=["Texas Property Code Sec. 5.028-5.030", "TLTA Title Standard 2.10"],
        burden_holder="Party relying on correction deed",
        adversary_position="Party claiming correction exceeds scrivener's error scope",
        counter_arguments=["Change is substantive, not clerical", "Only one party executed the correction", "Original instrument was not referenced"],
        resolution_strategy="Verify error is clerical. Confirm both parties executed. Cross-reference on run sheet. Flag substantive corrections as potential issues.",
        entity_scope="Parties to original and correction instruments",
        confidence=0.90,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Texas Property Code Sec. 5.028",
        issue_category=IssueCategory.CHAIN_OF_TITLE,
        interaction_edges=["warranty_deed_chain_analysis", "legal_description_parsing"],
    )

    doctrines["lease_expiration_analysis"] = DoctrineBlock(
        topic="Lease Expiration and Termination Analysis",
        keywords=["lease expiration", "primary term", "HBP", "cessation", "termination", "shut-in", "top lease"],
        conclusion_template="Lease status determination requires analysis of primary term, production status, savings clauses, and operations. An expired lease removes the leasehold burden and returns full mineral rights to the lessor.",
        reasoning_framework="STEP 1: Calculate primary term expiration from commencement date. STEP 2: If primary term expired, check for production — 'held by production' extends the lease into secondary term. STEP 3: If production ceased, check cessation of production clause — typically allows 60-90 days to resume. STEP 4: Check for shut-in royalty payments if well is capable but not producing. STEP 5: Check for continuous drilling clause — operations must commence within specified period. STEP 6: If lease has expired, it is no longer a burden on the mineral estate and should be noted as 'EXPIRED' on the run sheet.",
        key_factors=["Primary term dates must be precisely calculated", "HBP requires actual production in paying quantities", "Cessation clause provides limited grace period", "Shut-in provisions have specific payment requirements", "Expired leases remove leasehold burden"],
        primary_authority=["Anadarko Petroleum Corp. v. Thompson, 94 S.W.3d 550 (Tex. 2002)", "HECI Exploration Co. v. Neel, 982 S.W.2d 881 (Tex. 1998)"],
        burden_holder="Lessee claiming lease is still in effect",
        adversary_position="Lessor claiming lease has expired",
        counter_arguments=["Operations clause extends beyond primary term", "Shut-in royalty preserves the lease", "Force majeure tolled the term", "Cessation was within savings clause period"],
        resolution_strategy="Calculate primary term expiration. Verify production or operations status. Apply savings clauses. Determine current lease status definitively.",
        entity_scope="Lessors, lessees, top-lease holders",
        confidence=0.92,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Anadarko Petroleum Corp. v. Thompson, 94 S.W.3d 550 (Tex. 2002)",
        issue_category=IssueCategory.LEASE_ANALYSIS,
        interaction_edges=["oil_gas_lease_abstraction", "nri_nma_calculation"],
    )

    doctrines["lien_judgment_tracking"] = DoctrineBlock(
        topic="Lien and Judgment Tracking on Run Sheet",
        keywords=["lien", "judgment", "lis pendens", "mechanic's lien", "federal tax lien", "mortgage", "deed of trust"],
        conclusion_template="All liens and judgments affecting the tract must be identified on the run sheet. Mineral interests can be subject to judgment liens, federal tax liens, and other encumbrances that affect marketability.",
        reasoning_framework="STEP 1: Search for judgment liens in the county where the property is located. STEP 2: Search for federal tax liens filed against record owners. STEP 3: Check for mechanic's and materialman's liens. STEP 4: Check for deeds of trust or mortgages. STEP 5: Verify whether liens have been released or expired. STEP 6: Note all unreleased liens as title requirements on the run sheet.",
        key_factors=["Judgment liens attach to all real property in the county", "Federal tax liens attach to all property of the taxpayer", "Mechanic's liens have strict filing deadlines", "Mineral interests are subject to liens", "Released liens should be documented"],
        primary_authority=["Texas Property Code Ch. 52 (Judgment liens)", "Internal Revenue Code Sec. 6321-6323 (Federal tax liens)", "Texas Property Code Ch. 53 (Mechanic's liens)"],
        burden_holder="Lien creditor",
        adversary_position="Property owner claiming lien is invalid or released",
        counter_arguments=["Lien has expired under statute of limitations", "Lien was improperly filed", "Release was recorded", "Lien does not attach to mineral interests"],
        resolution_strategy="Search all lien records. Verify current status. Note unreleased liens as requirements. Distinguish between liens on surface vs mineral estate.",
        entity_scope="Property owners, lien creditors, judgment creditors",
        confidence=0.87,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Texas Property Code Ch. 52",
        issue_category=IssueCategory.CHAIN_OF_TITLE,
        interaction_edges=["gap_detection_methodology"],
    )

    doctrines["tlta_standards_compliance"] = DoctrineBlock(
        topic="TLTA Title Standards Compliance",
        keywords=["TLTA", "title standards", "Texas Land Title Association", "examination standard", "curative standard"],
        conclusion_template="TLTA Title Examination Standards provide authoritative guidance on common title issues in Texas. The run sheet should be prepared in compliance with TLTA standards, and title requirements should reference applicable standards.",
        reasoning_framework="STEP 1: TLTA standards address common title issues including gaps in chain, name variances, marital status, entity authority, probate, and ancient instruments. STEP 2: Each standard provides a recommended approach for the examiner. STEP 3: Standards are advisory, not binding, but represent industry consensus on Texas title practice. STEP 4: Reference applicable TLTA standards in run sheet remarks and requirements. STEP 5: When the examiner's opinion differs from TLTA standards, document the reasoning.",
        key_factors=["TLTA standards are advisory but widely followed", "Standards address most common title issues", "Reference applicable standards in requirements", "Standards evolve with law changes", "Document departures from standards with reasoning"],
        primary_authority=["TLTA Title Examination Standards (current edition)", "Texas State Bar Real Property Section"],
        burden_holder="Title examiner applying standards",
        adversary_position="Party arguing standard does not apply",
        counter_arguments=["TLTA standards are advisory, not mandatory", "Specific facts may require deviation from standard", "Standard has not been updated for recent case law"],
        resolution_strategy="Apply TLTA standards as primary guidance. Document any deviations with reasoning. Reference specific standard numbers in requirements.",
        entity_scope="Title examiners, attorneys, landmen",
        confidence=0.93,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="TLTA Title Examination Standards",
        issue_category=IssueCategory.TITLE_STANDARDS,
        interaction_edges=["runsheet_format_standards", "gap_detection_methodology"],
    )

    doctrines["stand_up_examination"] = DoctrineBlock(
        topic="Stand-Up Title Examination Methodology",
        keywords=["stand-up", "courthouse", "county records", "grantor-grantee index", "tract index", "examination"],
        conclusion_template="A stand-up examination is conducted at the county courthouse using grantor-grantee indexes and tract indexes to build the chain of title. The landman searches backward from the present owner to the common source, then forward to verify completeness.",
        reasoning_framework="STEP 1: Begin at the county clerk's office. Identify the current record owner using the tract index or tax records. STEP 2: Search the grantee index backward — find the instrument that conveyed title to the current owner, then to the prior owner, continuing backward to sovereignty or common source. STEP 3: Search the grantor index forward — verify that each owner in the chain did not make additional conveyances (fractional mineral deeds, leases, assignments) affecting the tract. STEP 4: Search the lis pendens, judgment, and lien indexes for each record owner. STEP 5: Check probate records for any deceased owner in the chain. STEP 6: Compile findings onto the run sheet in chronological order. STEP 7: Perform the stand-up in systematic order: (a) sovereignty to present, (b) mineral chain, (c) lease chain, (d) liens/judgments, (e) tax status.",
        key_factors=["Grantee index searched backward in time", "Grantor index searched forward to catch additional conveyances", "Both indexes must be searched for complete examination", "Lis pendens and judgment indexes are separate searches", "Probate records may be in a different court"],
        primary_authority=["AAPL Title Examination Standards", "Texas Property Code Sec. 12.001 (County clerk duties)", "Industry standard practice"],
        burden_holder="Landman performing examination",
        adversary_position="Party claiming examination missed an instrument",
        counter_arguments=["County index has errors", "Instrument was misfiled", "Name variance caused index miss", "Online records are incomplete"],
        resolution_strategy="Follow systematic examination protocol. Search both grantor and grantee indexes. Cross-reference tract index where available. Document search methodology on run sheet.",
        entity_scope="Landmen, title examiners, county clerks",
        confidence=0.91,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="AAPL Title Examination Standards",
        issue_category=IssueCategory.TITLE_STANDARDS,
        interaction_edges=["runsheet_format_standards", "gap_detection_methodology", "warranty_deed_chain_analysis"],
    )

    doctrines["abstract_vs_runsheet"] = DoctrineBlock(
        topic="Abstract of Title vs Run Sheet Distinction",
        keywords=["abstract", "abstract of title", "run sheet", "title opinion", "chain of title", "title report"],
        conclusion_template="An abstract of title is a comprehensive summary of every recorded instrument, while a run sheet is a landman's working document focusing on the chain of title and current ownership. Title opinions are attorney work product based on abstracts or run sheets.",
        reasoning_framework="STEP 1: An abstract of title is prepared by a licensed abstractor and includes a complete summary of every recorded instrument affecting the property — deeds, mortgages, judgments, tax records, plats, and more. STEP 2: A run sheet is prepared by a landman and focuses on the chain of title, mineral ownership, and lease status. It is less comprehensive but more focused on the information needed for oil and gas operations. STEP 3: A title opinion is prepared by an attorney who examines the abstract or run sheet and renders an opinion on the state of title, listing requirements for curing defects. STEP 4: In practice, run sheets are used more frequently in the Permian Basin due to speed and cost considerations. STEP 5: The scope of examination should be clearly stated on the run sheet — stand-up examination, full abstract, or update only.",
        key_factors=["Abstract is comprehensive, run sheet is focused", "Title opinion is attorney work product", "Run sheets are standard for oil and gas title work", "Scope of examination must be stated", "Run sheets are faster and less expensive than full abstracts"],
        primary_authority=["AAPL Title Examination Standards", "Texas Insurance Code (title insurance)", "Industry standard practice"],
        burden_holder="Examiner determining scope of work",
        adversary_position="Client expecting more comprehensive examination",
        counter_arguments=["Run sheet may miss instruments an abstract would catch", "Abstract provides more comprehensive coverage", "Title insurance may require full abstract"],
        resolution_strategy="Clearly state the scope of examination. Use run sheet for standard oil and gas work. Recommend full abstract when comprehensive examination is needed.",
        entity_scope="Landmen, abstractors, attorneys, clients",
        confidence=0.92,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="AAPL Title Examination Standards",
        issue_category=IssueCategory.RUNSHEET_FORMAT,
        interaction_edges=["runsheet_format_standards", "stand_up_examination"],
    )

    doctrines["multi_tract_handling"] = DoctrineBlock(
        topic="Multiple Tract and Unit Run Sheet Handling",
        keywords=["multiple tracts", "unit", "spacing unit", "proration unit", "tract-by-tract", "combined run sheet"],
        conclusion_template="When a well or unit involves multiple tracts, the run sheet must present each tract's chain of title separately, then combine the interest computations to show each owner's proportionate share of unit production.",
        reasoning_framework="STEP 1: Identify all tracts within the unit or spacing area. STEP 2: Prepare a separate chain of title for each tract. STEP 3: Compute the mineral ownership for each tract independently. STEP 4: Determine each tract's proportionate acreage within the unit. STEP 5: Combine the interest computations: Owner's NRI = (Tract NMA / Total Unit NMA) x Tract NRI. STEP 6: Present the combined interest summary showing all owners and their unit-level decimal interests.",
        key_factors=["Each tract needs separate chain of title", "Acreage proportions determine unit participation", "Interest computation must account for all tracts", "Fractional interests may differ between tracts", "Combined summary shows total unit ownership"],
        primary_authority=["Railroad Commission spacing rules", "AAPL Division Order standards", "Texas Natural Resources Code Sec. 102.001"],
        burden_holder="Operator computing division of interest",
        adversary_position="Interest owner disputing unit participation",
        counter_arguments=["Acreage computation is incorrect", "Tract should not be included in unit", "Pooling authority was exceeded", "Interest computation chain has error"],
        resolution_strategy="Examine each tract independently. Compute acreage proportions. Combine interest computations. Verify against division orders.",
        entity_scope="All mineral owners across unit tracts, operator",
        confidence=0.89,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Railroad Commission spacing rules",
        issue_category=IssueCategory.INTEREST_COMPUTATION,
        interaction_edges=["nri_nma_calculation", "pooling_unit_analysis", "acreage_calculation_methods"],
    )

    doctrines["release_instrument_analysis"] = DoctrineBlock(
        topic="Release Instrument Analysis",
        keywords=["release", "partial release", "release of lien", "release of lease", "satisfaction", "discharge"],
        conclusion_template="Release instruments remove encumbrances from the title. The run sheet must verify that releases match the original instruments and that the releasing party had authority to release.",
        reasoning_framework="STEP 1: Identify the original instrument being released — lease, deed of trust, lien, or other encumbrance. STEP 2: Verify the release references the correct original instrument by recording data. STEP 3: Confirm the releasing party is the current holder of the interest or their authorized agent. STEP 4: For partial releases, verify the legal description of the released portion. STEP 5: Check whether the release is full or partial — partial releases leave the remaining portion encumbered. STEP 6: Note the release on the run sheet with cross-reference to the original instrument.",
        key_factors=["Release must reference original instrument", "Releasing party must be current holder", "Partial releases require specific legal descriptions", "Unauthorized releases may be ineffective", "Run sheet cross-references original and release"],
        primary_authority=["Texas Property Code Sec. 12.014 (Release requirements)", "Texas Business & Commerce Code Sec. 9.513 (UCC release)"],
        burden_holder="Party relying on the release",
        adversary_position="Interest holder claiming release is ineffective",
        counter_arguments=["Releasing party lacked authority", "Release referenced wrong instrument", "Partial release description is incorrect", "Release was forged or unauthorized"],
        resolution_strategy="Verify release matches original. Confirm authority of releasing party. Note on run sheet. Flag questionable releases as requirements.",
        entity_scope="Lienholders, lessees, releasing parties, property owners",
        confidence=0.89,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Texas Property Code Sec. 12.014",
        issue_category=IssueCategory.CHAIN_OF_TITLE,
        interaction_edges=["oil_gas_lease_abstraction", "lien_judgment_tracking"],
    )

    doctrines["entity_authority_verification"] = DoctrineBlock(
        topic="Entity Authority and Capacity Verification",
        keywords=["entity", "LLC", "corporation", "partnership", "authority", "capacity", "good standing", "authorized signatory"],
        conclusion_template="When an entity (LLC, corporation, LP, trust) is a party to a conveyance, the run sheet must verify entity existence, good standing, and the signatory's authority to act on behalf of the entity.",
        reasoning_framework="STEP 1: Identify the entity type — LLC, corporation, LP, general partnership, trust. STEP 2: Verify entity existence with the Texas Secretary of State. STEP 3: Confirm good standing (not forfeited or terminated). STEP 4: Verify the signatory's authority — officers for corporations, managers/members for LLCs, general partners for LPs, trustees for trusts. STEP 5: For trusts, verify the trust instrument grants authority to convey real property. STEP 6: For out-of-state entities, verify they are registered to do business in Texas. STEP 7: Flag any authority issues as title requirements.",
        key_factors=["Entity must exist and be in good standing", "Signatory must have authority per governing documents", "Texas SOS records verify entity status", "Trust authority comes from trust instrument", "Out-of-state entities must be registered in Texas"],
        primary_authority=["Texas Business Organizations Code", "Texas Secretary of State records", "TLTA Title Standard 3.10"],
        burden_holder="Party claiming under entity conveyance",
        adversary_position="Party challenging entity's authority or capacity",
        counter_arguments=["Entity was forfeited at time of conveyance", "Signatory lacked authority", "Trust instrument did not authorize conveyance", "Entity was not registered in Texas"],
        resolution_strategy="Verify entity status with SOS. Confirm signatory authority. Check trust instruments. Flag deficiencies as requirements.",
        entity_scope="Entities acting as grantors/grantees, signatories",
        confidence=0.88,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Texas Business Organizations Code",
        issue_category=IssueCategory.TITLE_STANDARDS,
        interaction_edges=["warranty_deed_chain_analysis", "gap_detection_methodology"],
    )

    doctrines["marital_property_considerations"] = DoctrineBlock(
        topic="Marital Property and Community Property Considerations",
        keywords=["community property", "separate property", "marital", "spouse", "homestead", "joinder"],
        conclusion_template="Texas is a community property state. Conveyances of community real property require joinder of both spouses. The run sheet must identify marital status and verify proper joinder to avoid title defects.",
        reasoning_framework="STEP 1: Texas is a community property state — property acquired during marriage is presumed community. STEP 2: Both spouses must join in conveying community real property. STEP 3: Separate property (owned before marriage, inherited, or received by gift) can be conveyed by the owning spouse alone. STEP 4: Homestead property requires joinder of both spouses regardless of separate/community characterization. STEP 5: Check for separate property affidavits or partition agreements. STEP 6: If a deed lacks spousal joinder and the property is community, the non-joining spouse's interest was not conveyed — creating a title defect.",
        key_factors=["Community property requires spousal joinder", "Separate property can be conveyed by owner alone", "Homestead requires joinder regardless", "Characterization may require supporting documents", "Missing joinder creates title defect"],
        primary_authority=["Texas Family Code Sec. 3.001-3.003 (Community property)", "Texas Family Code Sec. 5.001 (Joinder requirements)", "Texas Constitution Art. XVI Sec. 50 (Homestead)"],
        burden_holder="Grantee claiming valid conveyance",
        adversary_position="Non-joining spouse claiming community interest",
        counter_arguments=["Property was grantor's separate property", "Partition agreement exists", "Separate property affidavit filed", "Statute of limitations bars claim"],
        resolution_strategy="Identify marital status of each grantor. Verify joinder where required. Check for separate property documentation. Flag missing joinder as curative requirement.",
        entity_scope="Married grantors, spouses, grantees",
        confidence=0.90,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Texas Family Code Sec. 5.001",
        issue_category=IssueCategory.TITLE_STANDARDS,
        interaction_edges=["warranty_deed_chain_analysis", "probate_heirship_tracking"],
    )

    doctrines["grantor_grantee_index_methodology"] = DoctrineBlock(
        topic="Grantor-Grantee Index Search Methodology",
        keywords=["grantor index", "grantee index", "index search", "county records", "direct index", "inverse index"],
        conclusion_template="The grantor-grantee index is the primary search tool for building a chain of title. The grantee index is searched backward (present to past) and the grantor index is searched forward (past to present) for each owner in the chain.",
        reasoning_framework="STEP 1: The grantee index (inverse index) lists instruments alphabetically by grantee name. Search backward from present owner to find how each owner acquired title. STEP 2: The grantor index (direct index) lists instruments alphabetically by grantor name. Search forward from each owner to find all instruments they executed — deeds, leases, assignments, mortgages. STEP 3: Both indexes must be searched for every name in the chain, covering the period of ownership. STEP 4: Search for name variations — middle names, initials, Jr/Sr, maiden/married names. STEP 5: In counties with tract indexes, use the tract index as a cross-check. STEP 6: Online county records may be incomplete — courthouse records are definitive.",
        key_factors=["Grantee index searched backward builds the chain", "Grantor index searched forward catches all conveyances", "Both must be searched for completeness", "Name variations must be checked", "Tract index is supplementary cross-reference"],
        primary_authority=["Texas Property Code Sec. 12.001-12.003", "AAPL Title Examination Standards"],
        burden_holder="Examiner building chain of title",
        adversary_position="Party claiming instrument was missed",
        counter_arguments=["Index error caused instrument to be missed", "Name variance prevented finding", "Online index was incomplete"],
        resolution_strategy="Systematically search both indexes for every name. Check name variations. Cross-reference tract index. Document search period and methodology.",
        entity_scope="All record owners, county clerks, examiners",
        confidence=0.93,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Texas Property Code Sec. 12.001",
        issue_category=IssueCategory.TITLE_STANDARDS,
        interaction_edges=["stand_up_examination", "gap_detection_methodology"],
    )

    doctrines["sovereignty_to_common_source"] = DoctrineBlock(
        topic="Sovereignty to Common Source Chain Establishment",
        keywords=["sovereignty", "patent", "common source", "original grant", "Republic of Texas", "GLO", "headright"],
        conclusion_template="The chain of title begins at sovereignty — the original grant from the Republic of Texas, State of Texas, or Spanish/Mexican government. A common source is an accepted starting point where all parties agree on ownership, often a patent or early deed.",
        reasoning_framework="STEP 1: Texas land titles derive from original grants by: (a) Spanish Crown, (b) Mexican Government, (c) Republic of Texas, (d) State of Texas. STEP 2: The General Land Office (GLO) maintains records of all original patents and grants. STEP 3: A patent is the government's deed to the original grantee — headright grants, pre-emption claims, bounty warrants, railroad grants. STEP 4: For practical title examination, a common source is often used instead of tracing all the way to sovereignty. A common source is a point where all competing chains converge on an agreed owner. STEP 5: The common source must be supported by sufficient chain history and tax payment records. STEP 6: Document the sovereignty/common source as the first entry on the run sheet.",
        key_factors=["All Texas titles trace to sovereignty", "GLO records provide original patent/grant data", "Common source is a practical starting point", "Multiple grant systems exist in Texas", "Patent is the first link in every chain"],
        primary_authority=["Texas General Land Office records", "Texas Natural Resources Code Sec. 21.001", "Republic of Texas land grants"],
        burden_holder="Party establishing chain from sovereignty",
        adversary_position="Party claiming through different sovereignty grant",
        counter_arguments=["Competing Spanish/Mexican grant exists", "Patent boundaries overlap", "GLO records are incomplete for area"],
        resolution_strategy="Research GLO records for original patent. Establish common source where appropriate. Document on run sheet. Verify patent boundaries match current survey.",
        entity_scope="Original patentees, State of Texas, all subsequent owners",
        confidence=0.91,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Texas General Land Office records",
        issue_category=IssueCategory.CHAIN_OF_TITLE,
        interaction_edges=["warranty_deed_chain_analysis", "legal_description_parsing"],
    )

    doctrines["depth_severance_analysis"] = DoctrineBlock(
        topic="Depth Severance and Formation-Specific Interest Analysis",
        keywords=["depth severance", "formation", "depth clause", "horizontal severance", "strata", "above", "below"],
        conclusion_template="Depth severance divides the mineral estate horizontally, creating separate ownership at different depths or formations. The run sheet must track depth-severed interests separately, similar to surface/mineral severance.",
        reasoning_framework="STEP 1: Identify instruments that sever by depth — 'all minerals above 10,000 feet' or 'the Wolfcamp formation only.' STEP 2: After depth severance, separate chains exist for each depth stratum. STEP 3: Leases with depth clauses (Pugh vertical) may release deep or shallow rights upon termination. STEP 4: Depth-specific assignments create additional complexity in interest tracking. STEP 5: Formation names must be consistent — cross-reference with Railroad Commission well records for formation depths. STEP 6: Track each depth stratum on the run sheet with separate columns or sections.",
        key_factors=["Depth severance creates separate mineral estates at different strata", "Formation-specific conveyances require geologic verification", "Lease depth clauses may release certain depths", "Each depth stratum needs independent chain tracking", "Formation depths vary by location"],
        primary_authority=["Greer v. Stanolind Oil & Gas Co., 200 F.2d 920 (5th Cir. 1952)", "Reed v. Wylie, 597 S.W.2d 743 (Tex. 1980)"],
        burden_holder="Party claiming depth-specific interest",
        adversary_position="Party claiming full-depth ownership",
        counter_arguments=["Depth limitation language is ambiguous", "Formation identification is disputed", "Depth clause in lease released the interest"],
        resolution_strategy="Identify depth severance instruments. Establish depth-specific chains. Cross-reference formation data with RRC records. Track separately on run sheet.",
        entity_scope="Depth-specific mineral owners, operators, lessees",
        confidence=0.86,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Reed v. Wylie, 597 S.W.2d 743 (Tex. 1980)",
        issue_category=IssueCategory.MINERAL_RIGHTS,
        interaction_edges=["mineral_deed_conveyance", "oil_gas_lease_abstraction", "nri_nma_calculation"],
    )

    doctrines["division_order_reconciliation"] = DoctrineBlock(
        topic="Division Order Reconciliation with Run Sheet",
        keywords=["division order", "decimal interest", "revenue distribution", "operator", "suspense", "reconciliation"],
        conclusion_template="Division orders allocate revenue based on computed decimal interests. The run sheet's interest computation must reconcile with division order decimals. Discrepancies indicate chain errors or unresolved title issues.",
        reasoning_framework="STEP 1: Division orders are prepared by the operator based on the title examination and run sheet. STEP 2: Each interest owner's decimal interest is calculated to six decimal places. STEP 3: All decimal interests should total to 1.000000 (or less if interests are in suspense). STEP 4: Reconcile the run sheet's interest computation with the division order decimals. STEP 5: Discrepancies may indicate: computational errors, missing instruments, unresolved title issues, or different interpretation of ambiguous instruments. STEP 6: Suspended interests are held in escrow pending resolution of title issues.",
        key_factors=["Decimal interests must total 1.000000", "Six decimal place precision is standard", "Suspended interests indicate unresolved issues", "Division order derives from run sheet/title opinion", "Reconciliation catches computational errors"],
        primary_authority=["Texas Natural Resources Code Sec. 91.402 (Division order statute)", "AAPL Division Order form"],
        burden_holder="Operator computing division of interest",
        adversary_position="Interest owner disputing decimal allocation",
        counter_arguments=["Computational error in chain", "Instrument was misinterpreted", "Additional instruments were not considered", "Fractional interests were incorrectly computed"],
        resolution_strategy="Compare run sheet interests with division order decimals. Identify discrepancies. Trace errors back to specific instruments. Correct and recompute.",
        entity_scope="Operators, interest owners, title examiners",
        confidence=0.90,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Texas Natural Resources Code Sec. 91.402",
        issue_category=IssueCategory.INTEREST_COMPUTATION,
        interaction_edges=["nri_nma_calculation", "runsheet_format_standards"],
    )

    doctrines["heir_fractionation_tracking"] = DoctrineBlock(
        topic="Heir Fractionation and Multi-Generational Interest Tracking",
        keywords=["heir", "fractionation", "fractional interest", "multi-generational", "intestate", "partition"],
        conclusion_template="When mineral interests pass through multiple generations of intestate succession, the number of interest holders grows exponentially and individual shares become extremely small. The run sheet must trace each line of descent and compute the resulting fractional interests.",
        reasoning_framework="STEP 1: Identify the original mineral interest holder and their fractional share. STEP 2: When the holder dies intestate, apply Texas Estates Code Ch. 201 to distribute among heirs. STEP 3: Each heir's share may further fractionate at their death. STEP 4: After 3-4 generations, a single 1/4 mineral interest can be held by 50+ individuals. STEP 5: Track each line of descent on the run sheet. STEP 6: Some heirs may have conveyed their interests, adding more complexity. STEP 7: Partition actions may consolidate fractional interests. STEP 8: For leasing purposes, all fractional mineral owners must be identified and leased from.",
        key_factors=["Intestate succession fractionates interests exponentially", "Each generation multiplies the number of holders", "All fractional owners must be identified for leasing", "Partition can consolidate interests", "Heirship affidavits may miss some heirs"],
        primary_authority=["Texas Estates Code Ch. 201", "Texas Estates Code Sec. 203.001"],
        burden_holder="Party tracing fractional interests",
        adversary_position="Unknown heir claiming overlooked interest",
        counter_arguments=["Heirship determination was incomplete", "Unknown or omitted heirs exist", "Adoption or legitimation changes inheritance rights", "Community property characterization affects distribution"],
        resolution_strategy="Build family tree for each deceased owner. Apply intestate succession rules at each generation. Track all heirs and their fractional shares. Flag unknown heirs as requirements.",
        entity_scope="Deceased mineral owners, all heirs, devisees",
        confidence=0.85,
        confidence_stratification=ConfidenceLevel.DISCLOSURE,
        controlling_precedent="Texas Estates Code Ch. 201",
        issue_category=IssueCategory.PROBATE_HEIRSHIP,
        interaction_edges=["probate_heirship_tracking", "nri_nma_calculation", "dormant_mineral_identification"],
    )

    doctrines["lis_pendens_effect"] = DoctrineBlock(
        topic="Lis Pendens Effect on Title Examination",
        keywords=["lis pendens", "pending litigation", "notice of suit", "constructive notice", "lawsuit"],
        conclusion_template="A recorded lis pendens provides constructive notice that litigation is pending affecting the described property. Any purchaser during the pendency of the suit takes subject to the outcome. The run sheet must identify all lis pendens and determine whether they have been released or the suit resolved.",
        reasoning_framework="STEP 1: Search for lis pendens notices filed against the tract or any owner in the chain. STEP 2: A lis pendens is effective from the date of recording — any subsequent purchaser is bound by the judgment. STEP 3: Verify whether the underlying suit has been resolved. Obtain certified copy of judgment or order of dismissal. STEP 4: Check whether a release of lis pendens has been recorded. STEP 5: If the lis pendens is unreleased and the suit unresolved, this is a title requirement. STEP 6: The suit must actually affect title to real property — not all lawsuits support a lis pendens. STEP 7: Flag on the run sheet with cause number, court, parties, and property description.",
        key_factors=["Lis pendens provides constructive notice from recording date", "Subsequent purchasers take subject to suit outcome", "Must verify resolution or release", "Only suits affecting real property support lis pendens", "Unreleased lis pendens is a title requirement"],
        primary_authority=["Texas Property Code Sec. 12.007 (Lis pendens)", "Texas Civil Practice & Remedies Code Sec. 12.001"],
        burden_holder="Party relying on lis pendens",
        adversary_position="Purchaser claiming no notice of pending suit",
        counter_arguments=["Suit does not affect real property title", "Lis pendens was improperly filed", "Suit has been dismissed", "Release was recorded"],
        resolution_strategy="Search for lis pendens. Verify suit status. Obtain release or evidence of resolution. Flag unreleased as requirements.",
        entity_scope="Litigants, property owners, subsequent purchasers",
        confidence=0.88,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Texas Property Code Sec. 12.007",
        issue_category=IssueCategory.CHAIN_OF_TITLE,
        interaction_edges=["lien_judgment_tracking", "gap_detection_methodology"],
    )

    doctrines["adverse_possession_minerals"] = DoctrineBlock(
        topic="Adverse Possession of Mineral Interests",
        keywords=["adverse possession", "limitation", "statute of limitations", "prescriptive rights", "mineral adverse possession"],
        conclusion_template="Adverse possession of severed mineral interests in Texas requires actual production of minerals under claim of right for the statutory period. Mere surface possession does not ripen into mineral ownership. The run sheet must identify any adverse possession claims and assess their validity.",
        reasoning_framework="STEP 1: Surface adverse possession does NOT confer mineral rights when the estates are severed. Texas courts consistently hold this position. STEP 2: To adversely possess severed minerals, claimant must actually produce minerals openly, notoriously, continuously, exclusively, and under claim of right for the statutory period. STEP 3: The statutory period is 10 years under Texas Civil Practice & Remedies Code Sec. 16.026 (improvements in good faith) or 25 years under the general statute. STEP 4: Peaceable possession for 25 years under recorded deed may cure mineral title defects under Tex. Civ. Prac. & Rem. Code Sec. 16.028. STEP 5: Tax payment alone does not establish adverse possession of minerals. STEP 6: Flag any adverse possession claims on the run sheet as title requirements pending verification.",
        key_factors=["Surface possession does not confer mineral rights", "Actual mineral production is required for adverse possession", "25-year statute may cure defects under recorded deed", "Tax payment alone is insufficient", "Claim of right must be open and notorious"],
        primary_authority=["Texas Civil Practice & Remedies Code Sec. 16.021-16.030", "Natural Gas Pipeline Co. v. Pool, 124 S.W.3d 188 (Tex. 2003)", "Cosgrove v. Cade, 468 S.W.3d 32 (Tex. 2015)"],
        burden_holder="Adverse possession claimant",
        adversary_position="Record title holder of mineral interest",
        counter_arguments=["No actual mineral production by claimant", "Possession was not exclusive or continuous", "Record owner did not receive notice", "Statutory period has not been met"],
        resolution_strategy="Verify production records for adverse possession period. Check recorded deeds and tax payment history. Assess whether statutory elements are met. Flag as requirement if unresolved.",
        entity_scope="Mineral interest claimants, record owners, surface owners",
        confidence=0.84,
        confidence_stratification=ConfidenceLevel.DISCLOSURE,
        controlling_precedent="Natural Gas Pipeline Co. v. Pool, 124 S.W.3d 188 (Tex. 2003)",
        issue_category=IssueCategory.MINERAL_RIGHTS,
        interaction_edges=["dormant_mineral_identification", "gap_detection_methodology"],
    )

    doctrines["power_of_attorney_conveyance"] = DoctrineBlock(
        topic="Power of Attorney in Title Conveyances",
        keywords=["power of attorney", "POA", "attorney-in-fact", "agency", "durable power", "statutory POA"],
        conclusion_template="Conveyances executed by an attorney-in-fact under power of attorney must be verified for authority, scope, and validity. The POA must be recorded, must grant specific real property authority, and must not have been revoked at the time of execution.",
        reasoning_framework="STEP 1: Identify the recorded power of attorney. Texas Property Code Sec. 12.001 requires recording for real property transactions. STEP 2: Verify the POA grants specific authority for real property conveyances — general powers may not suffice. STEP 3: Check whether the POA is durable (survives incapacity) or non-durable. STEP 4: Verify the POA was not revoked before the conveyance — check for recorded revocations. STEP 5: Confirm the principal was alive at the time of conveyance (non-durable POA terminates at death; durable POA also terminates at death unless coupled with interest). STEP 6: Texas Estates Code Ch. 751 governs statutory durable powers of attorney. STEP 7: Note the POA and its scope on the run sheet for the affected conveyance.",
        key_factors=["POA must be recorded for real property transactions", "Must grant specific real property authority", "Must verify POA was not revoked", "Durable vs non-durable affects survival of authority", "POA terminates at principal's death"],
        primary_authority=["Texas Estates Code Ch. 751 (Durable Power of Attorney)", "Texas Property Code Sec. 12.001", "TLTA Title Standard 3.40"],
        burden_holder="Grantee claiming under POA conveyance",
        adversary_position="Principal or heirs challenging POA authority",
        counter_arguments=["POA did not authorize real property conveyance", "POA was revoked before conveyance", "Principal was deceased at time of conveyance", "Agent exceeded scope of authority"],
        resolution_strategy="Locate and verify recorded POA. Confirm scope includes real property. Check for revocation. Verify principal was alive. Note on run sheet.",
        entity_scope="Principals, attorneys-in-fact, grantees",
        confidence=0.87,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Texas Estates Code Ch. 751",
        issue_category=IssueCategory.TITLE_STANDARDS,
        interaction_edges=["entity_authority_verification", "warranty_deed_chain_analysis"],
    )

    doctrines["water_rights_intersection"] = DoctrineBlock(
        topic="Water Rights Intersection with Mineral Title",
        keywords=["water rights", "groundwater", "Rule of Capture", "surface water", "water well", "water mineral"],
        conclusion_template="In Texas, groundwater is owned by the surface owner under the Rule of Capture as modified by the Edwards Aquifer Authority and groundwater conservation districts. Water rights may intersect with mineral operations and should be noted on the run sheet when relevant to the tract.",
        reasoning_framework="STEP 1: Texas follows the Rule of Capture for groundwater — the surface owner can pump without liability to neighbors, subject to groundwater district regulations. STEP 2: When minerals and surface are severed, the mineral lessee's right to use groundwater for operations depends on the lease terms and accommodation doctrine. STEP 3: Some mineral leases specifically address water rights and disposal. STEP 4: Surface water is governed by the prior appropriation doctrine under the Texas Water Code. STEP 5: Note any water rights agreements, permits, or restrictions on the run sheet. STEP 6: Groundwater conservation district rules may affect mineral operations.",
        key_factors=["Rule of Capture governs groundwater in Texas", "Surface owner generally controls groundwater", "Mineral lessee may use water reasonably necessary for operations", "Groundwater districts may impose restrictions", "Water disposal agreements affect operations"],
        primary_authority=["Edwards Aquifer Authority v. Day, 369 S.W.3d 814 (Tex. 2012)", "Texas Water Code Ch. 36 (Groundwater districts)", "Coyote Lake Ranch v. City of Lubbock, 498 S.W.3d 53 (Tex. 2016)"],
        burden_holder="Party claiming water rights",
        adversary_position="Competing user of water resources",
        counter_arguments=["Groundwater district restricts use", "Lease does not authorize water use", "Surface owner did not consent to water disposal", "Environmental regulations apply"],
        resolution_strategy="Identify any water rights agreements or permits. Note groundwater district rules. Check lease terms for water provisions. Flag water-related issues on run sheet.",
        entity_scope="Surface owners, mineral lessees, groundwater districts, operators",
        confidence=0.82,
        confidence_stratification=ConfidenceLevel.DISCLOSURE,
        controlling_precedent="Edwards Aquifer Authority v. Day, 369 S.W.3d 814 (Tex. 2012)",
        issue_category=IssueCategory.MINERAL_RIGHTS,
        interaction_edges=["surface_mineral_separation", "oil_gas_lease_abstraction"],
    )

    doctrines["ratification_instrument_analysis"] = DoctrineBlock(
        topic="Ratification Instrument Analysis",
        keywords=["ratification", "ratification of lease", "affirmation", "confirmation", "ratification deed"],
        conclusion_template="A ratification confirms and makes effective an instrument that may have been defective in execution or authority. Common in oil and gas title work to cure execution defects in leases. The run sheet must note ratifications and the defects they cure.",
        reasoning_framework="STEP 1: Identify the original instrument being ratified and the specific defect. STEP 2: Common ratification scenarios: (a) Spouse ratifies lease signed only by one spouse; (b) Heir ratifies lease that did not include all mineral owners; (c) Entity officer ratifies conveyance with questionable authority; (d) Co-owner ratifies lease that did not include all co-owners. STEP 3: Ratification relates back to the date of the original instrument. STEP 4: Verify the ratifying party had interest to ratify. STEP 5: Record both the original instrument and ratification on the run sheet with cross-references. STEP 6: If ratification is missing for a known defect, flag as a title requirement.",
        key_factors=["Ratification cures execution defects", "Relates back to original instrument date", "Ratifying party must have interest to ratify", "Common for spousal joinder issues", "Cross-reference on run sheet is essential"],
        primary_authority=["Texas Property Code Sec. 5.023", "TLTA Title Standards", "Industry practice"],
        burden_holder="Party relying on ratification",
        adversary_position="Party claiming ratification is ineffective",
        counter_arguments=["Defect was too fundamental for ratification", "Ratifying party lacked interest", "Ratification was obtained under duress", "Original instrument was void, not merely voidable"],
        resolution_strategy="Identify the defect in the original instrument. Verify ratification cures the specific defect. Confirm ratifying party's authority. Cross-reference on run sheet.",
        entity_scope="Parties to original instrument, ratifying parties",
        confidence=0.89,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Texas Property Code Sec. 5.023",
        issue_category=IssueCategory.CHAIN_OF_TITLE,
        interaction_edges=["marital_property_considerations", "oil_gas_lease_abstraction"],
    )

    doctrines["bankruptcy_effect_on_title"] = DoctrineBlock(
        topic="Bankruptcy Effect on Real Property Title",
        keywords=["bankruptcy", "trustee", "bankruptcy estate", "automatic stay", "adversary proceeding", "discharge"],
        conclusion_template="A bankruptcy filing creates an automatic stay and transfers property to the bankruptcy estate. Conveyances during bankruptcy may be voidable. The run sheet must identify any bankruptcy filings affecting record owners and verify proper authority for any transactions during bankruptcy.",
        reasoning_framework="STEP 1: Search federal bankruptcy court records for filings by any record owner. STEP 2: A bankruptcy filing creates an automatic stay under 11 USC Sec. 362 — no property can be conveyed without court approval. STEP 3: Property becomes part of the bankruptcy estate under 11 USC Sec. 541. STEP 4: The bankruptcy trustee has authority to sell estate property with court approval. STEP 5: Verify that any conveyance during bankruptcy was authorized by the bankruptcy court. STEP 6: Check for discharge orders that release the debtor from further liability. STEP 7: Flag any unauthorized transfers during bankruptcy as potential voidable conveyances.",
        key_factors=["Automatic stay prevents unauthorized transfers", "Bankruptcy trustee controls estate property", "Court authorization required for sales", "Voidable preference actions may affect prior transfers", "Discharge does not transfer property"],
        primary_authority=["11 USC Sec. 362 (Automatic stay)", "11 USC Sec. 541 (Property of the estate)", "11 USC Sec. 363 (Sale of estate property)"],
        burden_holder="Purchaser from bankruptcy estate",
        adversary_position="Trustee or creditor challenging unauthorized transfer",
        counter_arguments=["Transfer occurred before bankruptcy filing", "Court authorized the sale", "Property was abandoned by the estate", "Transfer was for fair value"],
        resolution_strategy="Search bankruptcy records for all owners. Verify any transfers during bankruptcy were court-authorized. Flag unauthorized transfers. Obtain court orders confirming sales.",
        entity_scope="Debtors, bankruptcy trustees, purchasers, creditors",
        confidence=0.86,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="11 USC Sec. 362",
        issue_category=IssueCategory.CHAIN_OF_TITLE,
        interaction_edges=["lien_judgment_tracking", "gap_detection_methodology"],
    )

    doctrines["mineral_classification_dispute"] = DoctrineBlock(
        topic="Mineral Classification Disputes — What Constitutes a Mineral",
        keywords=["mineral classification", "what is a mineral", "surface destruction", "mineral definition", "Moser test"],
        conclusion_template="Texas defines 'minerals' through the surface-destruction test established in Reed v. Wylie and refined in Moser. Substances that can be extracted without destroying the surface (like sand, gravel, limestone) may not be classified as minerals even under a general mineral reservation. The run sheet should note any ambiguity in mineral definitions when recording reservations.",
        reasoning_framework="STEP 1: Under the surface-destruction test, a substance is a 'mineral' under a general reservation only if it can be extracted from beneath the surface without consuming or destroying the surface. STEP 2: Oil and gas are always minerals under Texas law. STEP 3: Hard minerals (coal, metals, ore) are generally minerals. STEP 4: Surface-mineable substances (sand, gravel, limestone, caliche) are generally NOT minerals under a reservation using the word 'minerals' without specific inclusion. STEP 5: If the reservation specifically names the substance (e.g., 'all oil, gas, and other minerals including sand and gravel'), the named substance is included regardless of the surface-destruction test. STEP 6: Note any mineral classification ambiguity on the run sheet when abstracting reservations.",
        key_factors=["Surface-destruction test controls for unnamed minerals", "Oil and gas are always minerals", "Surface-mineable substances may not be minerals under general reservation", "Specific naming overrides the test", "Ambiguity in reservations creates title uncertainty"],
        primary_authority=["Reed v. Wylie, 597 S.W.2d 743 (Tex. 1980)", "Moser v. U.S. Steel Corp., 676 S.W.2d 99 (Tex. 1984)", "Friedman v. Texaco, Inc., 691 S.W.2d 586 (Tex. 1985)"],
        burden_holder="Party claiming substance is a mineral under reservation",
        adversary_position="Surface owner claiming substance belongs to surface estate",
        counter_arguments=["Substance can be extracted without surface destruction", "Reservation used general language without specific inclusion", "Surface owner has right to use surface substances", "Industry practice treats substance as surface material"],
        resolution_strategy="Apply surface-destruction test to determine classification. Check reservation language for specific substance inclusion. Note ambiguity on run sheet. Recommend curative language if needed.",
        entity_scope="Mineral owners, surface owners, lessees",
        confidence=0.85,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Reed v. Wylie, 597 S.W.2d 743 (Tex. 1980)",
        issue_category=IssueCategory.MINERAL_RIGHTS,
        interaction_edges=["reservation_exception_tracking", "surface_mineral_separation"],
    )

    doctrines["recording_statute_analysis"] = DoctrineBlock(
        topic="Texas Recording Statute and Notice Analysis",
        keywords=["recording", "constructive notice", "actual notice", "BFP", "bona fide purchaser", "race-notice"],
        conclusion_template="Texas is a race-notice jurisdiction. A subsequent purchaser for value without notice who records first takes priority over a prior unrecorded instrument. The run sheet must consider recording dates and potential unrecorded interests.",
        reasoning_framework="STEP 1: Texas Property Code Sec. 13.001 provides that recorded instruments constitute constructive notice. STEP 2: An unrecorded instrument is void as to a subsequent purchaser for value without notice who records first. STEP 3: 'Without notice' means without actual or constructive notice. Possession constitutes inquiry notice. STEP 4: The recording date (not the execution date) determines priority. STEP 5: Late-recorded instruments are effective between the parties but not against BFPs. STEP 6: Note the recording date on the run sheet and flag any gaps between execution and recording.",
        key_factors=["Texas is a race-notice recording jurisdiction", "Recording provides constructive notice", "BFP without notice who records first prevails", "Possession constitutes inquiry notice", "Recording date determines priority, not execution date"],
        primary_authority=["Texas Property Code Sec. 13.001", "Madison v. Gordon, 39 S.W.3d 604 (Tex. 2001)"],
        burden_holder="Party claiming under recorded instrument",
        adversary_position="Prior unrecorded interest holder",
        counter_arguments=["Subsequent purchaser had actual notice", "Possession put purchaser on inquiry notice", "Instrument was not properly acknowledged", "Recording was defective"],
        resolution_strategy="Record both execution and recording dates on run sheet. Flag late recordings. Consider possession as inquiry notice. Apply race-notice priority rules.",
        entity_scope="All parties in chain, subsequent purchasers",
        confidence=0.92,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Texas Property Code Sec. 13.001",
        issue_category=IssueCategory.CHAIN_OF_TITLE,
        interaction_edges=["warranty_deed_chain_analysis", "gap_detection_methodology"],
    )

    return doctrines


def get_all_doctrine_topics() -> list[str]:
    """Return a list of all doctrine topic keys."""
    return list(build_doctrine_cache().keys())


def get_doctrines_by_category(category: IssueCategory) -> list[DoctrineBlock]:
    """Return all doctrines matching a specific issue category."""
    cache = build_doctrine_cache()
    return [d for d in cache.values() if d.issue_category == category]


def get_doctrine_interaction_graph() -> dict[str, list[str]]:
    """Return the interaction graph showing doctrine dependencies."""
    cache = build_doctrine_cache()
    return {topic: block.interaction_edges for topic, block in cache.items()}
