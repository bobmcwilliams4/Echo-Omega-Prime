"""
LM10 Curative Engine — Doctrines Module
=========================================
Pre-compiled doctrine blocks for curative title work, organized by
issue category. Each block contains real domain expertise for
oil and gas title curative operations in Texas.

Engine: LM10 | Port: 8510 | Domain: title_curative
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Optional

from loguru import logger
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------
class IssueCategory(str, Enum):
    """Curative issue categories."""
    HEIRSHIP = "HEIRSHIP"
    PROBATE = "PROBATE"
    CORRECTION_INSTRUMENTS = "CORRECTION_INSTRUMENTS"
    QUIET_TITLE = "QUIET_TITLE"
    MISSING_INSTRUMENTS = "MISSING_INSTRUMENTS"
    LIEN_RELEASE = "LIEN_RELEASE"
    RATIFICATION = "RATIFICATION"
    STIPULATION = "STIPULATION"
    POOLING_AMENDMENTS = "POOLING_AMENDMENTS"
    TAX_SALE_CURATIVE = "TAX_SALE_CURATIVE"
    ADVERSE_POSSESSION = "ADVERSE_POSSESSION"
    DORMANT_MINERALS = "DORMANT_MINERALS"
    GAP_RESOLUTION = "GAP_RESOLUTION"
    BOUNDARY_DISPUTES = "BOUNDARY_DISPUTES"
    ESTATE_REUNIFICATION = "ESTATE_REUNIFICATION"
    JUDGMENT_RESOLUTION = "JUDGMENT_RESOLUTION"
    LIS_PENDENS = "LIS_PENDENS"
    FORECLOSURE_CURATIVE = "FORECLOSURE_CURATIVE"
    NAME_VARIATIONS = "NAME_VARIATIONS"
    ENTITY_AUTHORITY = "ENTITY_AUTHORITY"


class ConfidenceStratification(str, Enum):
    """Confidence tiers for curative opinions."""
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"


class PositionZone(str, Enum):
    """Position zones — never blur these."""
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"


# ---------------------------------------------------------------------------
# Doctrine Block Model
# ---------------------------------------------------------------------------
class DoctrineBlock(BaseModel):
    """
    A single pre-compiled doctrine block with real curative domain content.
    Each block targets a specific curative topic with authoritative reasoning.
    """
    topic: str
    keywords: list[str] = Field(min_length=5)
    conclusion_template: str
    reasoning_framework: str
    key_factors: list[str] = Field(min_length=5)
    primary_authority: list[str] = Field(min_length=3)
    burden_holder: str
    adversary_position: str
    counter_arguments: list[str] = Field(min_length=3)
    resolution_strategy: str
    entity_scope: str = "INDIVIDUAL"
    confidence: float = 0.85
    confidence_stratification: ConfidenceStratification = ConfidenceStratification.DEFENSIBLE
    controlling_precedent: str = ""
    issue_category: IssueCategory = IssueCategory.HEIRSHIP
    position_zone: PositionZone = PositionZone.PLANNING
    curative_document_type: str = ""
    estimated_timeline_days: int = 30
    typical_cost_range: str = ""
    risk_factors: list[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Doctrine Interaction Edge
# ---------------------------------------------------------------------------
class DoctrineInteraction(BaseModel):
    """Defines how two doctrine topics interact."""
    source_topic: str
    target_topic: str
    interaction_type: str  # "prerequisite", "alternative", "complementary", "conflicting"
    description: str
    weight: float = 1.0


# ---------------------------------------------------------------------------
# Doctrine Registry
# ---------------------------------------------------------------------------
def build_doctrine_cache() -> list[DoctrineBlock]:
    """
    Build the complete doctrine cache for the LM10 Curative Engine.
    Returns 42+ doctrine blocks covering all curative categories.
    """
    blocks: list[DoctrineBlock] = []

    # ===================================================================
    # HEIRSHIP DOCTRINES
    # ===================================================================
    blocks.append(DoctrineBlock(
        topic="affidavit_of_heirship_requirements",
        keywords=["heirship", "affidavit", "intestate", "heirs", "decedent", "requirements", "family history"],
        conclusion_template=(
            "An Affidavit of Heirship under Texas Estates Code Section 203.001 must be executed by a disinterested "
            "witness who has personal knowledge of the decedent's family history and marital status. The affidavit "
            "must identify all heirs, their relationship to the decedent, and the property interest passing. "
            "After five years on record without contrary filing, it becomes prima facie evidence of the facts stated."
        ),
        reasoning_framework=(
            "STEP 1: Confirm decedent died intestate (no will admitted to probate).\n"
            "STEP 2: Identify a disinterested witness — someone with no financial interest in the estate who "
            "knew the decedent for at least 10 years and has knowledge of family history, marriages, and children.\n"
            "STEP 3: The affidavit must contain: (a) decedent's full legal name and all name variations, "
            "(b) date and place of death, (c) marital history including names of all spouses and marriage/divorce/death dates, "
            "(d) identification of all children (including predeceased and adopted), (e) statement that decedent died "
            "intestate, (f) description of the real property, (g) assertion that no administration is pending.\n"
            "STEP 4: Texas Estates Code 201.001-201.003 governs intestate succession — community property goes "
            "to surviving spouse if all children are also children of the surviving spouse; otherwise 1/2 to spouse "
            "and 1/2 to children. Separate property: 1/3 life estate in land to spouse, remainder to children.\n"
            "STEP 5: Record in county where real property is located. After 5 years without challenge, "
            "Tex. Prop. Code 13.002 makes it constructive notice.\n"
            "STEP 6: Note limitations — affidavit of heirship does NOT divest any actual heir of their interest "
            "if the affidavit is incorrect. It is evidence, not a judicial determination."
        ),
        key_factors=[
            "Decedent died intestate — no will probated",
            "Disinterested witness with 10+ years personal knowledge",
            "All heirs identified with relationships stated",
            "Marital history complete (all marriages, divorces, deaths)",
            "Property description included by legal description",
            "5-year seasoning period for prima facie status",
            "Must be recorded in county of property location",
        ],
        primary_authority=[
            "Texas Estates Code Section 203.001 (Affidavit of Heirship)",
            "Texas Estates Code Sections 201.001-201.003 (Intestate Succession)",
            "Texas Property Code Section 13.002 (Constructive Notice)",
            "Featherson v. Ott, 257 S.W.2d 538 (Tex. Civ. App. 1953)",
        ],
        burden_holder="Party asserting heirship chain",
        adversary_position=(
            "Actual heirs or creditors may contest that the affidavit omits heirs, "
            "misstates family history, or was prepared by an interested witness."
        ),
        counter_arguments=[
            "Affidavit may omit unknown or undisclosed heirs (common with blended families)",
            "Witness may not have sufficient personal knowledge if relationship was casual",
            "Affidavit does not substitute for judicial determination when interests are disputed",
            "Community property characterization may be incorrect if separate property tracing applies",
            "Adopted children or children born out of wedlock may be omitted",
        ],
        resolution_strategy=(
            "Obtain affidavit from best available disinterested witness. Supplement with "
            "additional affidavits from other knowledgeable persons if family history is complex. "
            "If five years have not elapsed, consider obtaining title insurance with affidavit "
            "as supporting evidence. If heirs are disputed, pursue judicial determination of heirship."
        ),
        issue_category=IssueCategory.HEIRSHIP,
        confidence=0.88,
        confidence_stratification=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="Featherson v. Ott, 257 S.W.2d 538 (Tex. Civ. App. 1953)",
        curative_document_type="Affidavit of Heirship",
        estimated_timeline_days=14,
        typical_cost_range="$500-$1,500",
        risk_factors=["Omitted heirs", "Incorrect family history", "Interested witness"],
    ))

    blocks.append(DoctrineBlock(
        topic="judicial_determination_of_heirship",
        keywords=["judicial determination", "heirship", "probate court", "heirs", "intestate", "proceeding", "ad litem"],
        conclusion_template=(
            "A Judicial Determination of Heirship under Texas Estates Code Chapter 202 provides a court order "
            "identifying heirs and their respective shares. Unlike an affidavit, this is a binding judicial decree "
            "that conclusively establishes the heirs. Required when heirs are disputed, unknown heirs may exist, "
            "or the property interest is substantial enough to warrant judicial certainty."
        ),
        reasoning_framework=(
            "STEP 1: File application in county court of the county where decedent was domiciled, or if no Texas "
            "domicile, in any county where real property is located.\n"
            "STEP 2: Court appoints attorney ad litem to represent unknown heirs. Citation by publication required.\n"
            "STEP 3: Hearing with testimony from at least two disinterested witnesses regarding family history.\n"
            "STEP 4: Court enters judgment identifying each heir, their relationship, and fractional interest.\n"
            "STEP 5: Certified copy of judgment recorded in each county where real property is located.\n"
            "STEP 6: Judgment is conclusive as to parties and those in privity — res judicata applies.\n"
            "STEP 7: Can be combined with independent administration if desired."
        ),
        key_factors=[
            "Decedent died intestate or will cannot be probated",
            "At least two disinterested witnesses required",
            "Attorney ad litem appointed for unknown heirs",
            "Citation by publication required",
            "Judgment conclusive — res judicata",
            "Must record in county of property location",
            "No statute of limitations for filing",
        ],
        primary_authority=[
            "Texas Estates Code Chapter 202 (Determination of Heirship)",
            "Texas Estates Code Section 202.004 (Required Statements in Application)",
            "Texas Estates Code Section 202.009 (Judgment)",
            "In re Estate of Nash, 220 S.W.3d 914 (Tex. 2007)",
        ],
        burden_holder="Applicant for determination of heirship",
        adversary_position="Unknown heirs represented by attorney ad litem may contest distribution",
        counter_arguments=[
            "Expensive and time-consuming compared to affidavit",
            "Requires finding two disinterested witnesses",
            "Attorney ad litem fees add to cost",
            "May reveal heirs that complicate the chain",
        ],
        resolution_strategy=(
            "File when affidavit of heirship is insufficient — disputes exist, "
            "large property values, complex family history, or purchaser/lender requires judicial certainty."
        ),
        issue_category=IssueCategory.HEIRSHIP,
        confidence=0.92,
        confidence_stratification=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="In re Estate of Nash, 220 S.W.3d 914 (Tex. 2007)",
        curative_document_type="Judicial Determination of Heirship",
        estimated_timeline_days=90,
        typical_cost_range="$3,000-$8,000",
        risk_factors=["Unknown heirs surfacing", "Cost", "Time delay"],
    ))

    # ===================================================================
    # PROBATE DOCTRINES
    # ===================================================================
    blocks.append(DoctrineBlock(
        topic="independent_administration_probate",
        keywords=["independent administration", "executor", "probate", "will", "unsupervised", "tex est code 401", "court order"],
        conclusion_template=(
            "Independent Administration under Texas Estates Code Section 401.001 et seq. allows the executor "
            "to administer the estate without ongoing court supervision. The will must name an independent executor "
            "or all distributees must agree. The executor may sell, lease, or convey real property without court "
            "approval, making this the preferred probate method for curative purposes."
        ),
        reasoning_framework=(
            "STEP 1: Determine if the will designates independent administration or independent executor.\n"
            "STEP 2: If will is silent, all distributees can agree to independent administration under 401.002a.\n"
            "STEP 3: Independent executor need not post bond unless will requires it.\n"
            "STEP 4: Executor has broad power to sell real property without court order per 356.251.\n"
            "STEP 5: Must still file inventory within 90 days of qualification (alternatively, affidavit in lieu).\n"
            "STEP 6: Independent executor's deed is effective to pass title — title examiner should verify "
            "authority from will and letters testamentary.\n"
            "STEP 7: Four-year statute of limitations to probate will (Tex. Est. Code 256.003)."
        ),
        key_factors=[
            "Will must authorize independent administration or all distributees agree",
            "No ongoing court supervision required",
            "Executor can convey real property without court order",
            "Four-year deadline to probate will from date of death",
            "Inventory or affidavit in lieu required within 90 days",
            "Letters testamentary evidence executor's authority",
        ],
        primary_authority=[
            "Texas Estates Code Section 401.001 (Independent Administration Authorized)",
            "Texas Estates Code Section 401.002 (Application for Independent Administration)",
            "Texas Estates Code Section 356.251 (Sale of Estate Property)",
            "Texas Estates Code Section 256.003 (Period for Filing)",
        ],
        burden_holder="Executor / personal representative",
        adversary_position="Beneficiaries or creditors may challenge executor's actions as breaching fiduciary duty",
        counter_arguments=[
            "Executor may exceed authority granted by will",
            "Creditor claims may encumber property before conveyance",
            "Will contest can invalidate executor's authority retroactively",
            "Inventory may not be filed, creating uncertainty about estate assets",
        ],
        resolution_strategy=(
            "Verify will grants independent administration, obtain letters testamentary, "
            "confirm no pending will contest, review inventory for property description."
        ),
        issue_category=IssueCategory.PROBATE,
        confidence=0.90,
        confidence_stratification=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="Shepherd v. Ledford, 962 S.W.2d 28 (Tex. 1998)",
        curative_document_type="Letters Testamentary / Independent Executor's Deed",
        estimated_timeline_days=60,
        typical_cost_range="$2,000-$5,000",
        risk_factors=["Will contest", "Creditor claims", "Expired filing deadline"],
    ))

    blocks.append(DoctrineBlock(
        topic="muniment_of_title_probate",
        keywords=["muniment of title", "probate", "will", "simplified", "no administration", "court order", "tex est code 257"],
        conclusion_template=(
            "Probate as Muniment of Title under Texas Estates Code Section 257.001 allows a will to be admitted "
            "to probate without full administration when the estate has no unpaid debts (other than secured real "
            "property debts). The court order acts as direct muniment — evidence of title — transferring property "
            "to the devisees named in the will without need for an executor's deed."
        ),
        reasoning_framework=(
            "STEP 1: File application to probate will as muniment of title.\n"
            "STEP 2: Must prove no unpaid debts exist (other than debts secured by liens on real estate).\n"
            "STEP 3: Will is admitted to probate, court enters order that it constitutes muniment of title.\n"
            "STEP 4: Order recorded in county deed records — serves as link in chain of title.\n"
            "STEP 5: No executor appointed, no administration opened.\n"
            "STEP 6: Property vests directly in devisees per the will terms.\n"
            "STEP 7: Same four-year limitation period applies (Tex. Est. Code 256.003)."
        ),
        key_factors=[
            "No unpaid debts (other than real estate secured debts)",
            "Will must be valid and filed within four years of death",
            "No executor appointed — no administration",
            "Court order recorded as direct link in chain of title",
            "Property vests in devisees per will",
            "Simpler and cheaper than full administration",
        ],
        primary_authority=[
            "Texas Estates Code Section 257.001 (Probate as Muniment of Title)",
            "Texas Estates Code Section 256.003 (Filing Period)",
            "Tex. Estates Code Section 257.051 (Duties After Probate as Muniment)",
            "In re Estate of Herring, 983 S.W.2d 61 (Tex. App. 1998)",
        ],
        burden_holder="Applicant for muniment probate",
        adversary_position="Creditors may challenge that debts exist, defeating muniment eligibility",
        counter_arguments=[
            "Unpaid debts (even small ones) defeat eligibility",
            "Cannot be used if administration is needed for any purpose",
            "Four-year deadline may have expired",
            "Will contest can defeat the proceeding",
        ],
        resolution_strategy=(
            "Preferred curative when decedent had a will, no debts, and four-year period "
            "has not expired. Obtain certified copy of order and record in each county."
        ),
        issue_category=IssueCategory.PROBATE,
        confidence=0.88,
        confidence_stratification=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="In re Estate of Herring, 983 S.W.2d 61 (Tex. App. 1998)",
        curative_document_type="Muniment of Title Order",
        estimated_timeline_days=45,
        typical_cost_range="$1,500-$3,500",
        risk_factors=["Undisclosed debts", "Expired filing deadline", "Will validity"],
    ))

    blocks.append(DoctrineBlock(
        topic="small_estate_affidavit",
        keywords=["small estate", "affidavit", "simplified", "no probate", "tex est code 205", "low value", "intestate"],
        conclusion_template=(
            "A Small Estate Affidavit under Texas Estates Code Section 205.001 allows transfer of a small "
            "intestate estate without full probate when the value of the estate (excluding homestead and exempt "
            "property) does not exceed $75,000. The affidavit must be approved by the court and recorded."
        ),
        reasoning_framework=(
            "STEP 1: Confirm decedent died intestate (no will).\n"
            "STEP 2: At least 30 days must have elapsed since death.\n"
            "STEP 3: No petition for appointment of personal representative is pending or has been granted.\n"
            "STEP 4: Estate value excluding homestead and exempt property must not exceed $75,000.\n"
            "STEP 5: All distributees must sign the affidavit.\n"
            "STEP 6: Two disinterested witnesses must attest.\n"
            "STEP 7: Court approves and enters order.\n"
            "STEP 8: Recorded affidavit and order serve as evidence of title."
        ),
        key_factors=[
            "Decedent died intestate",
            "30 days since death elapsed",
            "Estate value under $75,000 (excluding homestead/exempt)",
            "All distributees must sign",
            "Two disinterested witnesses required",
            "Court approval required",
        ],
        primary_authority=[
            "Texas Estates Code Section 205.001 (Small Estate Affidavit)",
            "Texas Estates Code Section 205.003 (Contents)",
            "Texas Estates Code Section 205.007 (Court Approval)",
        ],
        burden_holder="Distributees filing small estate affidavit",
        adversary_position="Creditors may argue estate exceeds $75,000 threshold",
        counter_arguments=[
            "Estate valuation disputes may exceed threshold",
            "Not all distributees may cooperate in signing",
            "Court may deny approval if requirements not met",
        ],
        resolution_strategy=(
            "Use when estate is clearly under threshold and all distributees cooperate. "
            "Verify no pending administration application. File in court with proper attestation."
        ),
        issue_category=IssueCategory.PROBATE,
        confidence=0.85,
        confidence_stratification=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="Texas Estates Code Chapter 205",
        curative_document_type="Small Estate Affidavit",
        estimated_timeline_days=30,
        typical_cost_range="$750-$2,000",
        risk_factors=["Valuation disputes", "Non-cooperating distributees", "Undiscovered debts"],
    ))

    # ===================================================================
    # CORRECTION INSTRUMENT DOCTRINES
    # ===================================================================
    blocks.append(DoctrineBlock(
        topic="correction_deed_nonmaterial",
        keywords=["correction deed", "nonmaterial", "clerical error", "tex prop code 5.028", "typographical", "legal description", "correction"],
        conclusion_template=(
            "A Correction Instrument for nonmaterial corrections under Texas Property Code Section 5.028 allows "
            "parties to correct clerical errors, typographical mistakes, and inaccurate legal descriptions without "
            "re-executing the original deed. Only the original grantor (or grantor's heirs/devisees if deceased) "
            "can execute the correction instrument for nonmaterial corrections."
        ),
        reasoning_framework=(
            "STEP 1: Identify the error in the original recorded instrument.\n"
            "STEP 2: Classify as nonmaterial under 5.028: (a) clerical or typographical error, "
            "(b) incorrect or omitted legal description element, (c) misspelled name where identity is not in question.\n"
            "STEP 3: Correction instrument must reference the original instrument by recording data "
            "(volume/page or document number, recording date, county).\n"
            "STEP 4: Must state what is being corrected and the correct information.\n"
            "STEP 5: Original grantor or heir/devisee executes. Acknowledgment required.\n"
            "STEP 6: Record in same county as original. Effective as of original recording date.\n"
            "STEP 7: Does NOT require joinder of grantee."
        ),
        key_factors=[
            "Error must be nonmaterial (clerical, typographical, legal description)",
            "Must reference original instrument recording data",
            "Original grantor or heir/devisee must execute",
            "Grantee joinder not required for nonmaterial corrections",
            "Relates back to original recording date",
            "Must be acknowledged and recorded",
        ],
        primary_authority=[
            "Texas Property Code Section 5.028 (Correction Instruments: Nonmaterial)",
            "Texas Property Code Section 5.027 (Definitions)",
            "Texas Property Code Section 5.030 (Effect of Correction)",
            "Myrad Props., Inc. v. LaSalle Bank Nat'l Ass'n, 300 S.W.3d 1 (Tex. 2009)",
        ],
        burden_holder="Grantor or party seeking correction",
        adversary_position="Subsequent purchasers may argue correction changes material terms",
        counter_arguments=[
            "Line between material and nonmaterial is sometimes contested",
            "If grantor is deceased, locating heirs/devisees may be difficult",
            "If identity is in question (not just spelling), may require material correction",
        ],
        resolution_strategy=(
            "For clear clerical errors, use 5.028 nonmaterial correction. If any doubt "
            "about materiality, use 5.029 material correction requiring all original parties."
        ),
        issue_category=IssueCategory.CORRECTION_INSTRUMENTS,
        confidence=0.90,
        confidence_stratification=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="Myrad Props., Inc. v. LaSalle Bank Nat'l Ass'n, 300 S.W.3d 1 (Tex. 2009)",
        curative_document_type="Correction Deed (Nonmaterial)",
        estimated_timeline_days=14,
        typical_cost_range="$300-$800",
        risk_factors=["Materiality classification", "Locating grantor/heirs"],
    ))

    blocks.append(DoctrineBlock(
        topic="correction_deed_material",
        keywords=["correction deed", "material", "all parties", "tex prop code 5.029", "reformation", "grantee", "correction"],
        conclusion_template=(
            "A Correction Instrument for material corrections under Texas Property Code Section 5.029 requires "
            "the agreement and execution of ALL parties to the original transaction. Material corrections include "
            "changes to parties, property interest conveyed, consideration, or terms that substantively affect "
            "the conveyance. Cannot be used to convey additional property not in the original deed."
        ),
        reasoning_framework=(
            "STEP 1: Identify that the error is material — affects parties, interest, consideration, or terms.\n"
            "STEP 2: ALL original parties (or their heirs/devisees) must agree and execute.\n"
            "STEP 3: Correction instrument must: (a) reference original recording data, "
            "(b) state the correction needed, (c) state the correct information.\n"
            "STEP 4: All parties acknowledge. Record in same county.\n"
            "STEP 5: Effective as of original recording date (relates back).\n"
            "STEP 6: If a party refuses to cooperate, judicial reformation may be necessary."
        ),
        key_factors=[
            "Error must be material (changes substance of conveyance)",
            "ALL original parties or successors must execute",
            "Cannot add property not in original deed",
            "Relates back to original recording date",
            "If parties disagree, must seek judicial reformation",
        ],
        primary_authority=[
            "Texas Property Code Section 5.029 (Correction Instruments: Material)",
            "Texas Property Code Section 5.027 (Definitions)",
            "Texas Property Code Section 5.030 (Effect of Correction)",
        ],
        burden_holder="All parties to original transaction",
        adversary_position="One party may refuse to execute, requiring litigation",
        counter_arguments=[
            "Locating all original parties may be impossible after decades",
            "If any party is deceased, must locate all heirs/devisees",
            "Cannot create new interests — only correct existing ones",
        ],
        resolution_strategy=(
            "Obtain cooperation of all parties. If cooperation unavailable, "
            "file suit for reformation. Alternatively, use scrivener's affidavit "
            "if error is clearly a drafting mistake."
        ),
        issue_category=IssueCategory.CORRECTION_INSTRUMENTS,
        confidence=0.87,
        confidence_stratification=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="Texas Property Code Section 5.029",
        curative_document_type="Correction Deed (Material)",
        estimated_timeline_days=30,
        typical_cost_range="$800-$2,500",
        risk_factors=["Non-cooperating parties", "Locating all parties", "Exceeding correction scope"],
    ))

    blocks.append(DoctrineBlock(
        topic="scriveners_affidavit_curative",
        keywords=["scrivener", "affidavit", "drafting error", "clerical", "attorney", "drafter", "mistake", "obvious error"],
        conclusion_template=(
            "A Scrivener's Affidavit is an affidavit by the person who drafted the instrument acknowledging "
            "a clerical or drafting error. While not explicitly codified in Texas statutes, it is recognized "
            "by title companies and examiners as curative when the error is obvious and the drafter attests "
            "to the intended content. Best used in combination with a correction instrument."
        ),
        reasoning_framework=(
            "STEP 1: Identify the drafting error in the recorded instrument.\n"
            "STEP 2: Locate the original drafter (attorney, title company, escrow officer).\n"
            "STEP 3: Drafter executes affidavit stating: (a) they prepared the instrument, "
            "(b) the specific error, (c) what was intended, (d) the error was inadvertent.\n"
            "STEP 4: Affidavit should reference original instrument recording data.\n"
            "STEP 5: Record in same county as original instrument.\n"
            "STEP 6: Best practice: pair with correction instrument under 5.028 or 5.029.\n"
            "STEP 7: Title companies may still require additional curative depending on materiality."
        ),
        key_factors=[
            "Drafter must be available and willing to attest",
            "Error must be clearly a drafting mistake",
            "Should reference original instrument recording data",
            "Best paired with correction instrument",
            "Title company acceptance varies",
        ],
        primary_authority=[
            "No specific Texas statute — based on common practice",
            "Texas Property Code Sections 5.028-5.029 (related correction statutes)",
            "TLTA Title Standards (acceptance guidelines)",
        ],
        burden_holder="Party requesting correction",
        adversary_position="Title examiner may refuse to accept without statutory backing",
        counter_arguments=[
            "No specific statutory authority — relies on practice acceptance",
            "Drafter may not be locatable or may have died",
            "Title company may require judicial reformation regardless",
        ],
        resolution_strategy=(
            "Use when drafter is available and error is clearly inadvertent. "
            "Always pair with formal correction instrument. If drafter unavailable, "
            "proceed directly to 5.028/5.029 correction."
        ),
        issue_category=IssueCategory.CORRECTION_INSTRUMENTS,
        confidence=0.78,
        confidence_stratification=ConfidenceStratification.AGGRESSIVE,
        controlling_precedent="Common practice — no controlling case",
        curative_document_type="Scrivener's Affidavit",
        estimated_timeline_days=7,
        typical_cost_range="$200-$600",
        risk_factors=["No statutory authority", "Drafter unavailable", "Title company rejection"],
    ))

    # ===================================================================
    # QUIET TITLE DOCTRINES
    # ===================================================================
    blocks.append(DoctrineBlock(
        topic="trespass_to_try_title",
        keywords=["trespass to try title", "quiet title", "adverse claim", "tex civ prac rem 22", "cloud on title", "suit", "declaratory"],
        conclusion_template=(
            "A Trespass to Try Title action under Texas Civil Practice and Remedies Code Chapter 22 is the "
            "statutory method to establish or quiet title to real property in Texas. The plaintiff must recover "
            "on the strength of their own title, not the weakness of the defendant's. A declaratory judgment "
            "action under Chapter 37 may also be used but is not the traditional method for title disputes."
        ),
        reasoning_framework=(
            "STEP 1: Determine if cloud on title warrants judicial intervention (defects not curable by instrument).\n"
            "STEP 2: File trespass to try title action in district court of the county where property is located.\n"
            "STEP 3: Plaintiff must prove: (a) regular chain of title from sovereignty, (b) superior title "
            "by common source, (c) prior possession plus title, or (d) adverse possession.\n"
            "STEP 4: Defendant can assert any affirmative defense including limitations, adverse possession, "
            "bona fide purchaser status.\n"
            "STEP 5: Court enters judgment establishing title. Record certified copy.\n"
            "STEP 6: Judgment is binding on parties and privies — res judicata.\n"
            "STEP 7: Lis pendens should be filed at commencement to provide constructive notice."
        ),
        key_factors=[
            "Plaintiff must prove own title — cannot rely on defendant's weakness",
            "Four methods of proof available",
            "Filed in county where property located",
            "Judgment recorded as link in chain of title",
            "Lis pendens filed at suit commencement",
            "Discovery may be extensive",
        ],
        primary_authority=[
            "Texas Civil Practice and Remedies Code Chapter 22",
            "Texas Property Code Section 13.004 (Lis Pendens)",
            "Martin v. Amerman, 133 S.W.3d 262 (Tex. 2004)",
            "Rogers v. Ricane Enters., Inc., 772 S.W.2d 76 (Tex. 1989)",
        ],
        burden_holder="Plaintiff asserting title",
        adversary_position="Defendant claims superior or equal title interest",
        counter_arguments=[
            "Expensive and time-consuming litigation",
            "Must prove own chain — can't just attack defendant's",
            "Lis pendens may cloud title further during pendency",
            "Defendant may have valid limitations defense",
            "Common source doctrine may complicate proof",
        ],
        resolution_strategy=(
            "Last resort when curative instruments cannot resolve the defect. "
            "Ensure strong chain before filing. Consider settlement or stipulation "
            "before incurring litigation costs."
        ),
        issue_category=IssueCategory.QUIET_TITLE,
        confidence=0.92,
        confidence_stratification=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="Martin v. Amerman, 133 S.W.3d 262 (Tex. 2004)",
        curative_document_type="Judgment Quieting Title",
        estimated_timeline_days=365,
        typical_cost_range="$10,000-$50,000+",
        risk_factors=["Litigation cost", "Discovery burden", "Adverse judgment risk"],
    ))

    # ===================================================================
    # TAX SALE CURATIVE DOCTRINES
    # ===================================================================
    blocks.append(DoctrineBlock(
        topic="tax_sale_void_vs_voidable",
        keywords=["tax sale", "void", "voidable", "redemption", "due process", "notice", "tax deed", "defective"],
        conclusion_template=(
            "Texas distinguishes between void and voidable tax sales. A void tax sale (e.g., failure to give "
            "constitutionally required notice) is a nullity that confers no title and cannot be ratified. "
            "A voidable tax sale has procedural defects but is valid until challenged. The former owner has "
            "a two-year right of redemption for homestead/agricultural property, one year for other property, "
            "after which the tax deed creates a rebuttable presumption of validity."
        ),
        reasoning_framework=(
            "STEP 1: Examine the tax sale process — was constitutionally adequate notice provided?\n"
            "STEP 2: Determine if sale is void (no notice, wrong property, no jurisdiction) or "
            "voidable (minor procedural defects).\n"
            "STEP 3: For void sales: no time limit to challenge. Tax purchaser has no title.\n"
            "STEP 4: For voidable sales: statute of limitations applies. After limitations, "
            "defects are cured.\n"
            "STEP 5: Check redemption period — homestead/ag: 2 years. Other: 180 days for "
            "post-2015 sales, or as stated in deed.\n"
            "STEP 6: Redemption requires paying purchaser: amount paid + 25% premium (year 1) "
            "or 50% premium (year 2) for homestead/ag.\n"
            "STEP 7: After redemption period, tax deed holder should file suit to quiet title "
            "for maximum certainty."
        ),
        key_factors=[
            "Constitutional notice required — due process",
            "Void sale = nullity (no title passes, no time limit)",
            "Voidable sale = valid until successfully challenged",
            "Redemption periods vary by property type",
            "Redemption premium: 25% (year 1), 50% (year 2)",
            "Quiet title action recommended after redemption expires",
        ],
        primary_authority=[
            "Texas Tax Code Chapter 34 (Tax Sales)",
            "Texas Tax Code Section 34.21 (Right of Redemption)",
            "Texas Property Code Section 13.002",
            "Mennonite Bd. of Missions v. Adams, 462 U.S. 791 (1983)",
            "City of Lubbock v. Stubbs, 327 S.W.2d 411 (Tex. 1959)",
        ],
        burden_holder="Tax sale purchaser (to establish title) / Former owner (to challenge)",
        adversary_position="Former owner claims sale was void for lack of notice; purchaser claims valid title",
        counter_arguments=[
            "Notice requirements are strictly construed — minor defects may void sale",
            "Mineral interests may not be included in tax sale",
            "Federal tax liens may survive",
            "Constitutional due process may require more than statutory minimum notice",
            "Redemption right creates uncertainty for purchaser",
        ],
        resolution_strategy=(
            "For purchaser: verify adequate notice, wait for redemption to expire, file quiet title. "
            "For owner: exercise redemption during period. If void, file suit at any time."
        ),
        issue_category=IssueCategory.TAX_SALE_CURATIVE,
        confidence=0.85,
        confidence_stratification=ConfidenceStratification.DISCLOSURE,
        controlling_precedent="Mennonite Bd. of Missions v. Adams, 462 U.S. 791 (1983)",
        curative_document_type="Quiet Title Judgment / Redemption Certificate",
        estimated_timeline_days=180,
        typical_cost_range="$5,000-$25,000",
        risk_factors=["Void sale risk", "Mineral interest exclusion", "Federal lien survival"],
    ))

    # ===================================================================
    # ADVERSE POSSESSION DOCTRINES
    # ===================================================================
    blocks.append(DoctrineBlock(
        topic="adverse_possession_five_year",
        keywords=["adverse possession", "five year", "5 year", "color of title", "registered deed", "tex civ prac rem 16.025", "limitation"],
        conclusion_template=(
            "The 5-year adverse possession statute (Tex. Civ. Prac. & Rem. Code 16.025) requires: "
            "(1) peaceable and adverse possession, (2) cultivating, using, or enjoying the property, "
            "(3) under a duly registered deed or other color of title, (4) for five consecutive years, "
            "(5) payment of all taxes during that period. This provides the strongest limitations defense "
            "because it includes tax payment and recorded instrument requirements."
        ),
        reasoning_framework=(
            "STEP 1: Verify possessor holds a registered deed or other memorandum of title.\n"
            "STEP 2: Confirm possession was actual, visible, continuous, hostile, exclusive, and peaceable.\n"
            "STEP 3: Confirm all ad valorem taxes were paid during the five-year period.\n"
            "STEP 4: Five years must be consecutive — any interruption restarts the clock.\n"
            "STEP 5: Possession must be inconsistent with and hostile to the true owner's title.\n"
            "STEP 6: If elements met, possessor has affirmative defense in trespass to try title.\n"
            "STEP 7: Possessor should file affidavit of adverse possession and/or suit to quiet title."
        ),
        key_factors=[
            "Requires duly registered deed or color of title",
            "Five consecutive years of adverse possession",
            "All taxes paid during the period",
            "Actual, visible, hostile, exclusive possession",
            "Strongest form — includes tax payment requirement",
            "Affirmative defense in trespass to try title",
        ],
        primary_authority=[
            "Texas Civil Practice and Remedies Code Section 16.025",
            "Rhodes v. Cahill, 802 S.W.2d 643 (Tex. 1990)",
            "Kazmir v. Benavides, 288 S.W.3d 557 (Tex. App. 2009)",
        ],
        burden_holder="Possessor claiming adverse possession",
        adversary_position="True owner challenges that possession was not truly adverse or continuous",
        counter_arguments=[
            "Possession may have been permissive, not hostile",
            "Tax payments may have gaps",
            "Color of title document may be defective",
            "Co-tenants cannot adversely possess without ouster",
        ],
        resolution_strategy=(
            "Document all elements thoroughly. File affidavit of adverse possession. "
            "Consider quiet title suit for definitive resolution."
        ),
        issue_category=IssueCategory.ADVERSE_POSSESSION,
        confidence=0.85,
        confidence_stratification=ConfidenceStratification.AGGRESSIVE,
        controlling_precedent="Rhodes v. Cahill, 802 S.W.2d 643 (Tex. 1990)",
        curative_document_type="Affidavit of Adverse Possession / Quiet Title Judgment",
        estimated_timeline_days=180,
        typical_cost_range="$5,000-$20,000",
        risk_factors=["Permissive use defense", "Tax payment gaps", "Co-tenancy issues"],
    ))

    blocks.append(DoctrineBlock(
        topic="adverse_possession_ten_year",
        keywords=["adverse possession", "ten year", "10 year", "no deed required", "tex civ prac rem 16.026", "limitation", "open notorious"],
        conclusion_template=(
            "The 10-year adverse possession statute (Tex. Civ. Prac. & Rem. Code 16.026) requires "
            "peaceable and adverse possession for ten consecutive years. Unlike the 5-year statute, "
            "no registered deed, color of title, or tax payment is required. The possessor must "
            "demonstrate actual, open, notorious, continuous, exclusive, and hostile use."
        ),
        reasoning_framework=(
            "STEP 1: Confirm ten consecutive years of adverse possession.\n"
            "STEP 2: No deed or color of title required — possession alone suffices.\n"
            "STEP 3: Must be actual (physical use), open/notorious (visible to owner), "
            "continuous (not sporadic), exclusive (not shared with owner), hostile (without permission).\n"
            "STEP 4: Tacking permitted — successive possessors can combine periods if in privity.\n"
            "STEP 5: Mineral interests generally cannot be acquired by surface adverse possession alone.\n"
            "STEP 6: File suit to quiet title based on limitations defense."
        ),
        key_factors=[
            "Ten consecutive years of adverse possession",
            "No deed, color of title, or tax payment required",
            "Must be actual, open, notorious, continuous, exclusive, hostile",
            "Tacking of periods allowed with privity",
            "Mineral interests NOT acquired by surface possession alone",
        ],
        primary_authority=[
            "Texas Civil Practice and Remedies Code Section 16.026",
            "Yoast v. Yoast, 649 S.W.2d 289 (Tex. 1983)",
            "Natural Gas Pipeline Co. v. Pool, 124 S.W.3d 188 (Tex. 2003)",
        ],
        burden_holder="Possessor claiming 10-year adverse possession",
        adversary_position="True owner claims possession was permissive or not truly continuous",
        counter_arguments=[
            "Possession may have been with owner's consent (e.g., lease or family arrangement)",
            "Mineral estate generally not affected by surface adverse possession",
            "Tacking requires privity between successive possessors",
            "Government-owned property is immune from adverse possession",
        ],
        resolution_strategy=(
            "Document continuous occupation with evidence (fencing, improvements, tax receipts, "
            "witness testimony). File quiet title action."
        ),
        issue_category=IssueCategory.ADVERSE_POSSESSION,
        confidence=0.82,
        confidence_stratification=ConfidenceStratification.AGGRESSIVE,
        controlling_precedent="Yoast v. Yoast, 649 S.W.2d 289 (Tex. 1983)",
        curative_document_type="Quiet Title Judgment",
        estimated_timeline_days=365,
        typical_cost_range="$10,000-$30,000",
        risk_factors=["Permissive use", "Mineral estate exclusion", "Government immunity"],
    ))

    blocks.append(DoctrineBlock(
        topic="adverse_possession_twenty_five_year",
        keywords=["adverse possession", "twenty five year", "25 year", "tex civ prac rem 16.027", "super statute", "absolute bar"],
        conclusion_template=(
            "The 25-year adverse possession statute (Tex. Civ. Prac. & Rem. Code 16.028) is an absolute bar. "
            "After 25 years of adverse possession, no right of entry or action for recovery of real property "
            "may be asserted. This is the most powerful limitations statute — it defeats even disabilities "
            "and can overcome defects in the chain of title that other statutes cannot."
        ),
        reasoning_framework=(
            "STEP 1: Confirm 25 consecutive years of peaceable, adverse possession.\n"
            "STEP 2: This is an absolute bar — overcomes disabilities (minority, incompetency).\n"
            "STEP 3: Can include mineral interests if possessor exercised dominion over minerals.\n"
            "STEP 4: Overcomes defects in recorded instruments that otherwise would not be cured.\n"
            "STEP 5: Tacking allowed with privity between successive possessors.\n"
            "STEP 6: File suit to quiet title — this statute provides nearly conclusive defense."
        ),
        key_factors=[
            "25 consecutive years of adverse possession",
            "Absolute bar — no exceptions for disabilities",
            "Can include mineral interests with mineral dominion",
            "Overcomes most title defects",
            "Strongest curative tool in Texas adverse possession law",
        ],
        primary_authority=[
            "Texas Civil Practice and Remedies Code Section 16.028",
            "Tex. Civ. Prac. & Rem. Code Section 16.027 (related 25-year provision)",
            "Rick v. Grains Elevator, 51 Tex. Civ. App. 389, 112 S.W. 103 (1908) (25-year statute as absolute bar)",
        ],
        burden_holder="Possessor claiming 25-year adverse possession",
        adversary_position="Virtually no defense available — absolute bar",
        counter_arguments=[
            "Proving 25 continuous years is evidentiary challenge",
            "Government property still immune",
            "Must show true hostility throughout entire period",
        ],
        resolution_strategy="File quiet title action with extensive evidence of 25-year continuous possession.",
        issue_category=IssueCategory.ADVERSE_POSSESSION,
        confidence=0.90,
        confidence_stratification=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="Texas Civil Practice and Remedies Code Section 16.028",
        curative_document_type="Quiet Title Judgment",
        estimated_timeline_days=365,
        typical_cost_range="$10,000-$30,000",
        risk_factors=["Evidentiary burden of proving 25 years", "Government immunity"],
    ))

    # ===================================================================
    # LIEN RELEASE DOCTRINES
    # ===================================================================
    blocks.append(DoctrineBlock(
        topic="release_expired_lien",
        keywords=["lien release", "expired lien", "stale lien", "dormant lien", "mechanics lien", "materialman", "abstract of judgment"],
        conclusion_template=(
            "Expired liens — including mechanics and materialman's liens (must be enforced within 1-2 years), "
            "abstracts of judgment (expire after 10 years without renewal), and other consensual liens — "
            "should be released of record. If the lienholder cannot be located, Texas Property Code Section "
            "12.017 provides a procedure for releasing liens that have expired by their own terms or by statute."
        ),
        reasoning_framework=(
            "STEP 1: Identify the type of lien and applicable limitation/expiration period.\n"
            "STEP 2: Mechanics/materialman's lien: must be enforced within 1 year (residential) or 2 years "
            "(commercial) of filing (Tex. Prop. Code 53.158).\n"
            "STEP 3: Abstract of judgment lien: valid 10 years, renewable once (Tex. Prop. Code 52.006).\n"
            "STEP 4: Deed of trust: no statute of limitations per se, but 4-year limitations on underlying note.\n"
            "STEP 5: Request formal release from lienholder.\n"
            "STEP 6: If lienholder unresponsive after 30 days: file affidavit of release under 12.017.\n"
            "STEP 7: Some title companies will insure over expired liens without formal release."
        ),
        key_factors=[
            "Mechanics lien: 1-2 year enforcement deadline",
            "Abstract of judgment: 10 years, one renewal allowed",
            "Deed of trust: 4-year limitations on underlying note",
            "Request release first — affidavit release as fallback",
            "Texas Property Code 12.017 — affidavit release procedure",
        ],
        primary_authority=[
            "Texas Property Code Section 12.017 (Release of Lien)",
            "Texas Property Code Section 53.158 (Mechanic's Lien Enforcement)",
            "Texas Property Code Section 52.006 (Abstract of Judgment Duration)",
            "Texas Civil Practice and Remedies Code Section 16.035 (Limitations on Deed of Trust)",
        ],
        burden_holder="Property owner seeking release",
        adversary_position="Lienholder may claim lien is still valid or was renewed",
        counter_arguments=[
            "Lienholder may assert equitable tolling",
            "Federal tax liens have different expiration rules (10 years from assessment)",
            "Some liens may have been renewed without knowledge",
        ],
        resolution_strategy=(
            "Verify expiration by type. Request formal release. If unavailable, "
            "file affidavit under 12.017 or obtain title insurance over expired lien."
        ),
        issue_category=IssueCategory.LIEN_RELEASE,
        confidence=0.87,
        confidence_stratification=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="Texas Property Code Section 12.017",
        curative_document_type="Release of Lien / Affidavit of Release",
        estimated_timeline_days=30,
        typical_cost_range="$300-$1,500",
        risk_factors=["Renewed liens", "Federal liens", "Equitable tolling arguments"],
    ))

    # ===================================================================
    # DORMANT MINERAL INTEREST DOCTRINES
    # ===================================================================
    blocks.append(DoctrineBlock(
        topic="dormant_mineral_interest_act",
        keywords=["dormant mineral", "mineral interest pooling act", "mipa", "abandoned mineral", "tex nat res code 75", "termination", "surface owner"],
        conclusion_template=(
            "The Texas Mineral Interest Pooling Act (MIPA) and the Dormant Mineral Interest provisions "
            "under Texas Natural Resources Code Chapter 75 provide a mechanism for surface owners to "
            "terminate dormant severed mineral interests. A mineral interest is dormant if for 10+ years "
            "no production, lease, deed, or other use has occurred. The surface owner must provide notice "
            "and the mineral owner has 180 days to respond before termination takes effect."
        ),
        reasoning_framework=(
            "STEP 1: Confirm mineral interest has been severed from surface estate.\n"
            "STEP 2: Determine if interest has been 'dormant' — no use for 10+ continuous years.\n"
            "STEP 3: 'Use' includes: production, lease execution, deed or conveyance, payment of taxes, "
            "recording of claim, or good-faith attempt to use.\n"
            "STEP 4: Surface owner files notice of claim in county deed records.\n"
            "STEP 5: Surface owner provides actual notice to mineral interest owner (or last known address).\n"
            "STEP 6: If no response within 180 days, mineral interest terminates and reverts to surface owner.\n"
            "STEP 7: If mineral owner responds with any qualifying 'use' within 180 days, "
            "termination is defeated and cannot be re-attempted for another 10 years."
        ),
        key_factors=[
            "Mineral interest must be severed and dormant 10+ years",
            "No production, lease, deed, tax payment, or recorded claim during period",
            "Surface owner must file notice in deed records",
            "Actual notice to mineral owner (or last known address)",
            "180-day response period for mineral owner",
            "Any qualifying 'use' defeats termination",
        ],
        primary_authority=[
            "Texas Natural Resources Code Chapter 75",
            "Texas Natural Resources Code Section 75.001 (Definitions)",
            "Texas Natural Resources Code Section 75.002 (Termination of Interest)",
            "Bagby v. Bredthauer, 627 S.W.2d 190 (Tex. App. 1981)",
        ],
        burden_holder="Surface owner seeking termination",
        adversary_position="Mineral owner claims interest is not dormant due to qualifying use within 10 years",
        counter_arguments=[
            "Mineral owner may have recorded claim or paid taxes within 10 years",
            "Any lease execution — even if never developed — constitutes 'use'",
            "Notice requirements are strictly construed — defective notice defeats termination",
            "Mineral owner has strong incentive to respond and preserve interest",
            "Some interests may not qualify under the statute (e.g., royalty interests)",
        ],
        resolution_strategy=(
            "Conduct thorough title search for any qualifying 'use' in last 10 years. "
            "If truly dormant, file notice and provide actual service. Wait 180 days. "
            "If no response, record affidavit of termination."
        ),
        issue_category=IssueCategory.DORMANT_MINERALS,
        confidence=0.80,
        confidence_stratification=ConfidenceStratification.AGGRESSIVE,
        controlling_precedent="Bagby v. Bredthauer, 627 S.W.2d 190 (Tex. App. 1981)",
        curative_document_type="Notice of Claim / Affidavit of Termination",
        estimated_timeline_days=210,
        typical_cost_range="$2,000-$5,000",
        risk_factors=["Mineral owner response", "Qualifying use within 10 years", "Notice defects"],
    ))

    # ===================================================================
    # NAME VARIATION DOCTRINES
    # ===================================================================
    blocks.append(DoctrineBlock(
        topic="name_variation_affidavit",
        keywords=["name variation", "aka", "maiden name", "misspelling", "identity", "same person", "name change", "affidavit"],
        conclusion_template=(
            "A Name Variation Affidavit (also called Identity Affidavit or Same Person Affidavit) establishes "
            "that two or more names appearing in the chain of title refer to the same person. Common when "
            "maiden names, married names, AKAs, or misspellings create apparent breaks. The affiant — "
            "preferably the person themselves or a knowledgeable witness — swears the names identify one person."
        ),
        reasoning_framework=(
            "STEP 1: Identify the name discrepancy in the chain of title.\n"
            "STEP 2: Determine the nature: maiden/married name change, AKA, typographical error, "
            "nickname, initial vs. full name, or cultural name variation.\n"
            "STEP 3: If person is alive: obtain their sworn affidavit stating all names are one person.\n"
            "STEP 4: If person is deceased: obtain affidavit from family member or person with knowledge.\n"
            "STEP 5: Affidavit should include: (a) all name variations, (b) explanation for variation, "
            "(c) identifying details (DOB, SSN last 4, address), (d) property description.\n"
            "STEP 6: Record in county deed records.\n"
            "STEP 7: Some title companies accept without affidavit if names are substantially similar."
        ),
        key_factors=[
            "Identify all name variations in chain of title",
            "Person themselves is best affiant if alive",
            "Include identifying details to establish identity",
            "Record in county of property location",
            "Title company may accept without affidavit for minor variations",
        ],
        primary_authority=[
            "Texas Property Code Section 13.002 (Constructive Notice)",
            "Common practice — no specific statute",
            "TLTA Title Standards",
        ],
        burden_holder="Party asserting names refer to same person",
        adversary_position="Examiner may question whether names truly refer to one individual",
        counter_arguments=[
            "Person with similar name may actually be different individual",
            "If deceased, witness knowledge may be insufficient",
            "Cultural or legal name changes may not be properly documented",
        ],
        resolution_strategy=(
            "Obtain affidavit from most knowledgeable person. Include maximum identifying detail. "
            "For court-ordered name changes, obtain certified copy of order."
        ),
        issue_category=IssueCategory.NAME_VARIATIONS,
        confidence=0.90,
        confidence_stratification=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="Common practice — TLTA Title Standards",
        curative_document_type="Name Variation Affidavit / Identity Affidavit",
        estimated_timeline_days=7,
        typical_cost_range="$150-$400",
        risk_factors=["Actual identity dispute", "Insufficient witness knowledge"],
    ))

    # ===================================================================
    # ENTITY AUTHORITY DOCTRINES
    # ===================================================================
    blocks.append(DoctrineBlock(
        topic="corporate_authority_to_convey",
        keywords=["corporate authority", "resolution", "corporate deed", "officer", "authority to convey", "certificate", "good standing"],
        conclusion_template=(
            "A corporation conveying real property must demonstrate authority through corporate resolution, "
            "officer certificates, and evidence of good standing. Texas Business Organizations Code requires "
            "board authorization for conveyances outside the ordinary course of business. The deed should "
            "recite the officer's title and that the conveyance is authorized."
        ),
        reasoning_framework=(
            "STEP 1: Verify corporation exists in good standing with Texas Secretary of State.\n"
            "STEP 2: Determine if conveyance is in ordinary course of business (no board resolution needed) "
            "or extraordinary (board resolution required).\n"
            "STEP 3: For extraordinary transactions, obtain certified copy of board resolution authorizing sale.\n"
            "STEP 4: Officer executing deed should provide officer's certificate confirming authority.\n"
            "STEP 5: Deed recites: officer's name and title, corporation name, state of formation.\n"
            "STEP 6: If dissolved, verify winding-up authority still exists under BOC Chapter 11.\n"
            "STEP 7: For foreign corporations, verify registration with Texas SOS."
        ),
        key_factors=[
            "Corporation must be in good standing (or in wind-up period)",
            "Board resolution required for extraordinary conveyances",
            "Officer's certificate confirms authority",
            "Foreign corps must be registered in Texas",
            "Dissolved corps may convey during wind-up period",
        ],
        primary_authority=[
            "Texas Business Organizations Code Chapter 10 (Mergers, Exchanges, Sales)",
            "Texas Business Organizations Code Chapter 11 (Winding Up and Termination)",
            "Texas Business Organizations Code Section 3.001 (Certificate of Formation)",
            "Texas Secretary of State Registration Records",
        ],
        burden_holder="Corporation / officer executing conveyance",
        adversary_position="Grantee or examiner challenges officer's authority or corporate standing",
        counter_arguments=[
            "Officer may not actually hold the title claimed",
            "Board resolution may not have been properly adopted",
            "Corporation may have been forfeited for franchise tax non-payment",
            "Foreign corporation may not be registered in Texas",
        ],
        resolution_strategy=(
            "Obtain current certificate of good standing, board resolution (if extraordinary), "
            "and officer's certificate. For dissolved corps, verify wind-up authority."
        ),
        issue_category=IssueCategory.ENTITY_AUTHORITY,
        confidence=0.88,
        confidence_stratification=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="Texas Business Organizations Code Chapters 10-11",
        curative_document_type="Corporate Resolution / Officer's Certificate",
        estimated_timeline_days=14,
        typical_cost_range="$500-$2,000",
        risk_factors=["Forfeited charter", "Unauthorized officer", "Foreign corp not registered"],
    ))

    blocks.append(DoctrineBlock(
        topic="llc_authority_to_convey",
        keywords=["llc", "authorization", "member managed", "manager managed", "operating agreement", "conveyance", "certificate of formation"],
        conclusion_template=(
            "An LLC conveying real property must demonstrate authority per its governance structure. "
            "Manager-managed LLCs require manager authorization; member-managed LLCs require member authorization. "
            "The certificate of formation filed with the Texas SOS indicates governance type. The operating "
            "agreement (which may not be filed publicly) governs internal authority requirements."
        ),
        reasoning_framework=(
            "STEP 1: Check certificate of formation for manager-managed vs. member-managed designation.\n"
            "STEP 2: If manager-managed: manager executes deed, provides certificate of authority.\n"
            "STEP 3: If member-managed: determine if majority or unanimous member consent required.\n"
            "STEP 4: Review operating agreement for specific conveyance authorization requirements.\n"
            "STEP 5: Signer provides certificate or affidavit of authority citing operating agreement.\n"
            "STEP 6: Verify LLC is in good standing with Texas SOS.\n"
            "STEP 7: For foreign LLCs, verify Texas registration."
        ),
        key_factors=[
            "Governance structure determines who signs",
            "Operating agreement controls internal authority",
            "Certificate of authority should accompany deed",
            "Good standing verification required",
            "Operating agreement is usually not public record",
        ],
        primary_authority=[
            "Texas Business Organizations Code Chapter 101 (LLCs)",
            "Texas Business Organizations Code Section 101.254 (Management)",
            "Texas Business Organizations Code Section 101.052 (Certificate of Formation)",
        ],
        burden_holder="LLC member or manager executing conveyance",
        adversary_position="Title examiner questions whether signer has authority under operating agreement",
        counter_arguments=[
            "Operating agreement may restrict conveyance authority",
            "Multiple managers may be required to sign",
            "Series LLC may have separate ownership of property",
        ],
        resolution_strategy=(
            "Obtain certificate of authority from LLC manager/member. Verify good standing. "
            "If operating agreement requires specific approvals, obtain evidence of compliance."
        ),
        issue_category=IssueCategory.ENTITY_AUTHORITY,
        confidence=0.87,
        confidence_stratification=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="Texas Business Organizations Code Chapter 101",
        curative_document_type="Certificate of Authority / Manager Resolution",
        estimated_timeline_days=14,
        typical_cost_range="$500-$1,500",
        risk_factors=["Operating agreement restrictions", "Series LLC complexities", "Multiple manager requirement"],
    ))

    # ===================================================================
    # RATIFICATION DOCTRINES
    # ===================================================================
    blocks.append(DoctrineBlock(
        topic="ratification_of_prior_conveyance",
        keywords=["ratification", "confirm", "prior conveyance", "ratification deed", "confirmation", "unauthorized", "void conveyance"],
        conclusion_template=(
            "A Ratification or Confirmation Deed is used when a prior conveyance was made without proper "
            "authority, by the wrong party, or with technical defects that rendered it voidable. The party "
            "who should have conveyed (or their successors) executes the ratification to cure the defect. "
            "Ratification relates back to the date of the original conveyance."
        ),
        reasoning_framework=(
            "STEP 1: Identify the defect in the prior conveyance (wrong grantor, missing spouse signature, "
            "unauthorized agent, defective acknowledgment).\n"
            "STEP 2: Determine who has the authority to ratify (the party who should have signed, or successors).\n"
            "STEP 3: Prepare ratification deed that: (a) recites the original conveyance by recording data, "
            "(b) identifies the defect, (c) states the ratification.\n"
            "STEP 4: Ratifying party executes with proper acknowledgment.\n"
            "STEP 5: Record in county of property location.\n"
            "STEP 6: Relates back to original conveyance date for chain of title purposes.\n"
            "STEP 7: Cannot ratify a void act (only voidable ones)."
        ),
        key_factors=[
            "Prior conveyance must be voidable, not void",
            "Ratifying party must have or have had the authority",
            "Relates back to original conveyance date",
            "Must reference original instrument recording data",
            "Requires proper acknowledgment and recording",
        ],
        primary_authority=[
            "General Texas conveyance law — no specific ratification statute",
            "Land v. Turner, 377 S.W.2d 181 (Tex. 1964)",
            "Texas Property Code Section 13.001 (Recording Requirements)",
        ],
        burden_holder="Party with authority to ratify",
        adversary_position="Third parties may challenge that the original defect makes the deed void, not voidable",
        counter_arguments=[
            "Cannot ratify a void act — only voidable ones",
            "Ratifying party may have lost standing (e.g., already conveyed to someone else)",
            "Time may have created intervening interests",
        ],
        resolution_strategy=(
            "Identify correct ratifying party, prepare ratification deed with full recitals, "
            "obtain execution with acknowledgment, record immediately."
        ),
        issue_category=IssueCategory.RATIFICATION,
        confidence=0.85,
        confidence_stratification=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="Land v. Turner, 377 S.W.2d 181 (Tex. 1964)",
        curative_document_type="Ratification Deed / Confirmation Deed",
        estimated_timeline_days=21,
        typical_cost_range="$500-$1,500",
        risk_factors=["Void vs. voidable distinction", "Lost standing", "Intervening interests"],
    ))

    # ===================================================================
    # MISSING INSTRUMENT DOCTRINES
    # ===================================================================
    blocks.append(DoctrineBlock(
        topic="missing_instrument_reconstruction",
        keywords=["missing instrument", "lost deed", "destroyed", "unrecorded", "secondary evidence", "reconstruction", "certified copy"],
        conclusion_template=(
            "When a recorded instrument is missing from county records (physical destruction, microfiche "
            "degradation, or indexing failure), reconstruction may be accomplished by: (1) obtaining a "
            "certified copy from a title company's abstract plant, (2) re-recording a copy from the "
            "parties' files, (3) executing a new deed from the parties, or (4) filing an affidavit "
            "of lost instrument with supporting secondary evidence."
        ),
        reasoning_framework=(
            "STEP 1: Verify the instrument was actually recorded (check grantor/grantee indexes).\n"
            "STEP 2: If recording reference exists but document is missing: contact county clerk.\n"
            "STEP 3: Check title company abstract plants for copies.\n"
            "STEP 4: Contact original parties for copies from their files.\n"
            "STEP 5: If copies available: re-record with affidavit explaining circumstances.\n"
            "STEP 6: If no copies: parties execute new instrument with same terms.\n"
            "STEP 7: If parties unavailable: file affidavit of lost instrument with "
            "all available secondary evidence (title opinions, abstracts, references in later deeds).\n"
            "STEP 8: Quiet title action may be necessary for complete resolution."
        ),
        key_factors=[
            "Verify recording reference exists in index",
            "Check title company abstract plants",
            "Contact original parties for copies",
            "Re-recording with explanatory affidavit",
            "Affidavit of lost instrument as fallback",
            "Quiet title action for complete resolution",
        ],
        primary_authority=[
            "Texas Property Code Section 13.001 (Recording)",
            "Texas Rules of Evidence Rule 1004 (Admissibility of Other Evidence of Content)",
            "Texas Local Government Code Chapter 191 (County Records)",
        ],
        burden_holder="Party asserting the lost instrument existed and conveyed interest",
        adversary_position="Challenge that instrument never existed or had different terms",
        counter_arguments=[
            "No proof the instrument ever contained the claimed terms",
            "Secondary evidence may be unreliable",
            "Chain of custody issues with copies",
        ],
        resolution_strategy=(
            "Exhaust all sources for copies first. Re-record with affidavit. "
            "If no copies exist, consider quiet title action for definitive resolution."
        ),
        issue_category=IssueCategory.MISSING_INSTRUMENTS,
        confidence=0.75,
        confidence_stratification=ConfidenceStratification.DISCLOSURE,
        controlling_precedent="Texas Rules of Evidence Rule 1004",
        curative_document_type="Affidavit of Lost Instrument / Re-recorded Copy",
        estimated_timeline_days=45,
        typical_cost_range="$1,000-$5,000",
        risk_factors=["Proof challenges", "Unreliable secondary evidence", "Missing parties"],
    ))

    # ===================================================================
    # GAP RESOLUTION DOCTRINES
    # ===================================================================
    blocks.append(DoctrineBlock(
        topic="chain_of_title_gap_resolution",
        keywords=["gap", "chain of title", "missing link", "wild deed", "stranger to title", "break in chain", "title gap"],
        conclusion_template=(
            "A gap in the chain of title occurs when a conveyance from Owner A to Owner B is missing, "
            "and a subsequent conveyance from Owner B to Owner C exists. The gap can be resolved by: "
            "(1) locating and recording the missing deed, (2) obtaining a confirmatory deed from Owner A, "
            "(3) heirship determination if Owner A died, (4) adverse possession if sufficient time elapsed, "
            "or (5) quiet title action. A 'wild deed' (from a stranger to the chain) provides no "
            "constructive notice and does not constitute a link."
        ),
        reasoning_framework=(
            "STEP 1: Identify where the gap exists in the chain — which link is missing.\n"
            "STEP 2: Search for unindexed or misindexed instruments that may fill the gap.\n"
            "STEP 3: If grantor is alive: obtain confirmatory deed.\n"
            "STEP 4: If grantor died: heirship determination or probate to establish succession.\n"
            "STEP 5: If sufficient time: adverse possession may fill the gap.\n"
            "STEP 6: If none of the above: quiet title action.\n"
            "STEP 7: 'Wild deeds' from strangers to the chain provide no constructive notice — "
            "Tex. Prop. Code 13.001 requires chain connection for recording to impart notice."
        ),
        key_factors=[
            "Identify exactly which link in the chain is missing",
            "Search for misindexed instruments",
            "Confirmatory deed if grantor is available",
            "Heirship if grantor deceased",
            "Adverse possession as alternative",
            "Wild deeds provide no constructive notice",
        ],
        primary_authority=[
            "Texas Property Code Section 13.001 (Chain of Title Recording)",
            "Texas Property Code Section 13.002 (Constructive Notice)",
            "Lutcher & Moore Lumber Co. v. Knight, 217 S.W.2d 530 (Tex. 1949)",
            "Woods v. Sims, 154 Tex. 59, 273 S.W.2d 617 (1954)",
        ],
        burden_holder="Party claiming through the gap",
        adversary_position="Challenge that no valid conveyance occurred — title reverts to pre-gap owner",
        counter_arguments=[
            "Gap may indicate no conveyance ever occurred",
            "Wild deed in the chain undermines entire subsequent chain",
            "Misindexing does not excuse lack of actual conveyance",
        ],
        resolution_strategy=(
            "Thorough index search first. Then confirmatory deed, heirship, or adverse possession. "
            "Quiet title as last resort."
        ),
        issue_category=IssueCategory.GAP_RESOLUTION,
        confidence=0.78,
        confidence_stratification=ConfidenceStratification.DISCLOSURE,
        controlling_precedent="Lutcher & Moore Lumber Co. v. Knight, 217 S.W.2d 530 (Tex. 1949)",
        curative_document_type="Confirmatory Deed / Quiet Title Judgment",
        estimated_timeline_days=60,
        typical_cost_range="$1,500-$15,000",
        risk_factors=["Missing conveyance", "Wild deeds", "Competing claims"],
    ))

    # ===================================================================
    # FORECLOSURE CURATIVE DOCTRINES
    # ===================================================================
    blocks.append(DoctrineBlock(
        topic="foreclosure_notice_defects",
        keywords=["foreclosure", "notice defect", "substitute trustee", "power of sale", "tex prop code 51", "non-judicial", "cure foreclosure"],
        conclusion_template=(
            "Non-judicial foreclosure defects in Texas commonly involve: (1) failure to give proper notice "
            "of default and acceleration, (2) defective notice of substitute trustee's sale, (3) appointment "
            "of substitute trustee not properly executed or recorded, (4) sale conducted at wrong time or place. "
            "Under Texas Property Code Section 51.002, strict compliance with notice requirements is mandatory — "
            "defects may render the sale void or voidable."
        ),
        reasoning_framework=(
            "STEP 1: Review deed of trust for specific default/acceleration/notice requirements.\n"
            "STEP 2: Verify notice of default and intent to accelerate was properly served.\n"
            "STEP 3: Verify appointment of substitute trustee was recorded before sale.\n"
            "STEP 4: Verify notice of sale: filed with county clerk AND posted at courthouse door "
            "at least 21 days before sale, AND mailed to borrower at least 21 days before.\n"
            "STEP 5: Verify sale conducted first Tuesday of month between 10:00 AM and 4:00 PM.\n"
            "STEP 6: If defects exist: determine if void or voidable.\n"
            "STEP 7: Curative options: re-foreclosure (if still secured party), quiet title, "
            "borrower ratification, or stipulation."
        ),
        key_factors=[
            "Strict compliance with 51.002 notice requirements",
            "21-day notice to borrower by mail",
            "21-day posting at courthouse and filing with clerk",
            "Substitute trustee appointment must be recorded",
            "Sale on first Tuesday, 10 AM - 4 PM",
            "Defects may be void or voidable depending on nature",
        ],
        primary_authority=[
            "Texas Property Code Section 51.002 (Sale of Real Property Under Deed of Trust)",
            "Texas Property Code Section 51.0025 (Notice Requirements)",
            "Jasper Fed. Sav. & Loan Ass'n v. Reddell, 672 S.W.2d 6 (Tex. App. 1984)",
            "Univ. Sav. Ass'n v. Springwoods Shopping Ctr., 644 S.W.2d 705 (Tex. 1982)",
        ],
        burden_holder="Foreclosure purchaser / lender",
        adversary_position="Borrower claims defective foreclosure voids the sale",
        counter_arguments=[
            "Notice requirements are strictly construed in favor of borrower",
            "Defective substitute trustee appointment may void entire sale",
            "Wrong sale date or location is likely void, not merely voidable",
            "Borrower may have additional protections under federal law (CFPB)",
        ],
        resolution_strategy=(
            "Verify all procedural steps. If defective, consider re-foreclosure if possible. "
            "Otherwise, obtain borrower ratification or file quiet title action."
        ),
        issue_category=IssueCategory.FORECLOSURE_CURATIVE,
        confidence=0.82,
        confidence_stratification=ConfidenceStratification.DISCLOSURE,
        controlling_precedent="Univ. Sav. Ass'n v. Springwoods Shopping Ctr., 644 S.W.2d 705 (Tex. 1982)",
        curative_document_type="Re-foreclosure / Quiet Title Judgment / Ratification",
        estimated_timeline_days=120,
        typical_cost_range="$5,000-$25,000",
        risk_factors=["Void sale risk", "Federal protections", "Borrower challenge"],
    ))

    # ===================================================================
    # LIS PENDENS DOCTRINES
    # ===================================================================
    blocks.append(DoctrineBlock(
        topic="lis_pendens_clearance",
        keywords=["lis pendens", "pending litigation", "notice", "release", "expunction", "tex prop code 12.007", "clear title"],
        conclusion_template=(
            "A lis pendens under Texas Property Code Section 12.007 provides constructive notice of pending "
            "litigation affecting real property. Clearance requires: (1) judgment in the underlying suit "
            "(recorded certified copy of final judgment), (2) dismissal of the suit (recorded order of dismissal), "
            "(3) expunction under 12.0071 if suit was dismissed or plaintiff failed to establish right, or "
            "(4) agreement of the filing party to release."
        ),
        reasoning_framework=(
            "STEP 1: Identify the pending litigation referenced by the lis pendens.\n"
            "STEP 2: Check court records for status of the underlying suit.\n"
            "STEP 3: If suit resolved: obtain certified copy of final judgment or dismissal order.\n"
            "STEP 4: Record the resolution document in county deed records.\n"
            "STEP 5: If suit dismissed and lis pendens not released: file motion for expunction "
            "under 12.0071.\n"
            "STEP 6: If suit still pending: cannot clear without resolution or party agreement.\n"
            "STEP 7: Some title companies will insure over stale lis pendens with indemnity."
        ),
        key_factors=[
            "Lis pendens provides constructive notice of pending suit",
            "Cleared by final judgment, dismissal, or expunction",
            "Expunction available if suit dismissed or right not established",
            "Must record clearance document in county records",
            "Cannot clear during active litigation without party consent",
        ],
        primary_authority=[
            "Texas Property Code Section 12.007 (Lis Pendens)",
            "Texas Property Code Section 12.0071 (Expunction of Lis Pendens)",
            "Tarrant Bank v. Miller, 833 S.W.2d 666 (Tex. App.—Eastland 1992) (lis pendens effect on bona fide purchasers)",
        ],
        burden_holder="Property owner seeking to clear lis pendens",
        adversary_position="Filing party claims litigation is still active and lis pendens is proper",
        counter_arguments=[
            "Litigation may still be active and lis pendens proper",
            "Appeal may revive lis pendens even after judgment",
            "Filing party may refuse voluntary release",
        ],
        resolution_strategy=(
            "Determine suit status. If resolved, record resolution document. "
            "If dismissed without release, file for expunction. If active, negotiate or wait."
        ),
        issue_category=IssueCategory.LIS_PENDENS,
        confidence=0.88,
        confidence_stratification=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="Texas Property Code Section 12.007",
        curative_document_type="Release of Lis Pendens / Expunction Order",
        estimated_timeline_days=30,
        typical_cost_range="$500-$3,000",
        risk_factors=["Active litigation", "Refused release", "Appeal revival"],
    ))

    # ===================================================================
    # BOUNDARY DISPUTE DOCTRINES
    # ===================================================================
    blocks.append(DoctrineBlock(
        topic="boundary_dispute_resolution",
        keywords=["boundary", "survey", "encroachment", "agreed boundary", "acquiescence", "fence line", "survey conflict"],
        conclusion_template=(
            "Boundary disputes in Texas can be resolved by: (1) new survey by licensed surveyor, (2) agreed "
            "boundary doctrine (parties acquiesced to a boundary line for sufficient time), (3) boundary by "
            "acquiescence (acceptance of physical boundary like fence for 10+ years), or (4) judicial "
            "determination. The senior survey controls over junior surveys where conflicts exist."
        ),
        reasoning_framework=(
            "STEP 1: Commission survey by licensed Texas surveyor.\n"
            "STEP 2: Compare surveys — identify conflicts between descriptions.\n"
            "STEP 3: Apply senior survey doctrine — first-in-time survey controls.\n"
            "STEP 4: If parties have accepted a physical boundary for years, agreed boundary doctrine may apply.\n"
            "STEP 5: Boundary by acquiescence: long acceptance of physical boundary (typically 10+ years).\n"
            "STEP 6: Negotiate boundary line agreement between affected parties.\n"
            "STEP 7: If no agreement: trespass to try title action to establish boundary judicially."
        ),
        key_factors=[
            "Licensed surveyor determination is starting point",
            "Senior survey controls over junior survey",
            "Agreed boundary doctrine requires mutual agreement or acquiescence",
            "Physical boundaries (fences) may establish rights over time",
            "Boundary line agreement can be recorded to resolve",
        ],
        primary_authority=[
            "Texas Natural Resources Code Section 21.001 et seq. (Surveys)",
            "Stanolind Oil & Gas Co. v. State, 136 Tex. 5, 133 S.W.2d 767 (1939)",
            "Wilson v. Williams, 52 S.W.3d 286 (Tex. App. 2001)",
        ],
        burden_holder="Party claiming boundary in their favor",
        adversary_position="Adjacent owner claims boundary is at different location",
        counter_arguments=[
            "Survey conflicts may be unresolvable without litigation",
            "Agreed boundary requires more than passive acceptance",
            "New survey may reveal encroachments creating additional disputes",
        ],
        resolution_strategy=(
            "Commission survey, negotiate boundary line agreement, record if agreed. "
            "If disputed, consider trespass to try title."
        ),
        issue_category=IssueCategory.BOUNDARY_DISPUTES,
        confidence=0.80,
        confidence_stratification=ConfidenceStratification.AGGRESSIVE,
        controlling_precedent="Stanolind Oil & Gas Co. v. State, 133 S.W.2d 767 (1939)",
        curative_document_type="Boundary Line Agreement / Survey",
        estimated_timeline_days=60,
        typical_cost_range="$2,000-$20,000",
        risk_factors=["Survey conflicts", "Encroachments", "Litigation costs"],
    ))

    # ===================================================================
    # STIPULATION OF INTEREST DOCTRINES
    # ===================================================================
    blocks.append(DoctrineBlock(
        topic="stipulation_of_interest_agreement",
        keywords=["stipulation", "interest", "division order", "agreed interest", "working interest", "royalty", "allocation"],
        conclusion_template=(
            "A Stipulation of Interest Agreement is used when multiple parties agree to their respective "
            "interests in a mineral estate, resolving uncertainties in the chain of title without litigation. "
            "All affected parties sign, acknowledging their fractional interests. The agreement is recorded "
            "and serves as evidence of ownership for division order purposes. Not a conveyance — it confirms "
            "existing interests."
        ),
        reasoning_framework=(
            "STEP 1: Identify all parties with claims to the mineral interest.\n"
            "STEP 2: Run title and calculate each party's fractional interest.\n"
            "STEP 3: Draft stipulation identifying each party and their interest.\n"
            "STEP 4: All parties execute the stipulation.\n"
            "STEP 5: Record in county deed records.\n"
            "STEP 6: Provide to operator for division order purposes.\n"
            "STEP 7: Not a conveyance — does not create new interests or transfer existing ones."
        ),
        key_factors=[
            "All affected parties must agree and sign",
            "Confirms existing interests — not a conveyance",
            "Useful for division order processing",
            "Resolves uncertainties without litigation",
            "Should be recorded in county deed records",
        ],
        primary_authority=[
            "General contract law — no specific Texas statute for stipulations",
            "Texas Natural Resources Code Chapter 91 (Mineral Interest)",
            "Railroad Commission of Texas Statewide Rules",
        ],
        burden_holder="Operator or party seeking to resolve interest allocation",
        adversary_position="Party may disagree with allocated interest percentage",
        counter_arguments=[
            "One party may refuse to stipulate, defeating the agreement",
            "Stipulation may not bind non-signing parties",
            "Title examination may be disputed",
        ],
        resolution_strategy=(
            "Negotiate with all parties. If one refuses, consider quiet title action "
            "or proceed with known interests and suspend disputed amounts."
        ),
        issue_category=IssueCategory.STIPULATION,
        confidence=0.83,
        confidence_stratification=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="General contract law",
        curative_document_type="Stipulation of Interest Agreement",
        estimated_timeline_days=30,
        typical_cost_range="$1,000-$3,000",
        risk_factors=["Non-cooperating parties", "Interest calculation disputes"],
    ))

    # ===================================================================
    # POOLING AMENDMENT DOCTRINES
    # ===================================================================
    blocks.append(DoctrineBlock(
        topic="pooling_designation_amendment",
        keywords=["pooling", "amendment", "unit", "designation", "spacing", "rrc", "tex nat res code 102", "unitization"],
        conclusion_template=(
            "A Pooling Designation Amendment modifies the pooled unit designation for a well or unit, "
            "typically when: (1) a new well is drilled requiring unit modification, (2) tract configuration "
            "changes due to acquisitions, (3) horizontal well paths cross existing unit boundaries, or "
            "(4) RRC spacing rules change. Must be filed with RRC and may require amendments to existing "
            "leases depending on pooling clause language."
        ),
        reasoning_framework=(
            "STEP 1: Review existing pooling designations and unit configuration.\n"
            "STEP 2: Identify the need for amendment (new well, tract change, spacing change).\n"
            "STEP 3: Review lease pooling clauses — some require lessee to pool within a stated period.\n"
            "STEP 4: Prepare amended pooling designation.\n"
            "STEP 5: File with Railroad Commission of Texas.\n"
            "STEP 6: Notify all affected interest owners.\n"
            "STEP 7: Record in county deed records.\n"
            "STEP 8: Update division orders accordingly."
        ),
        key_factors=[
            "Lease pooling clause governs operator's pooling authority",
            "Must comply with RRC spacing and density rules",
            "Amendment must be filed with RRC",
            "All interest owners should be notified",
            "Division orders must be updated",
        ],
        primary_authority=[
            "Texas Natural Resources Code Chapter 102 (Mineral Interest Pooling Act)",
            "Railroad Commission of Texas Statewide Rule 37 (Spacing)",
            "Railroad Commission of Texas Statewide Rule 38 (Density)",
        ],
        burden_holder="Operator seeking to amend pooling designation",
        adversary_position="Interest owners may challenge that pooling exceeds lease authority",
        counter_arguments=[
            "Lease pooling clause may limit unit size or configuration",
            "Force pooling may be required if voluntary pooling fails",
            "Pugh clause may reduce pooled acreage obligations",
        ],
        resolution_strategy=(
            "Review lease pooling authority carefully. Draft amendment within lease constraints. "
            "File with RRC and record in county. Update all division orders."
        ),
        issue_category=IssueCategory.POOLING_AMENDMENTS,
        confidence=0.85,
        confidence_stratification=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="Texas Natural Resources Code Chapter 102",
        curative_document_type="Amended Pooling Designation",
        estimated_timeline_days=30,
        typical_cost_range="$1,000-$3,000",
        risk_factors=["Pooling clause limitations", "Interest owner challenges", "RRC compliance"],
    ))

    # ===================================================================
    # MINERAL ESTATE REUNIFICATION DOCTRINES
    # ===================================================================
    blocks.append(DoctrineBlock(
        topic="surface_mineral_estate_reunification",
        keywords=["reunification", "severed estate", "mineral estate", "surface estate", "merger", "acquisition", "rejoinder"],
        conclusion_template=(
            "Surface and mineral estate reunification occurs when one party acquires both the surface "
            "and all severed mineral interests. Under the merger doctrine, when the same party owns both "
            "estates, they merge unless the instrument of acquisition specifically preserves the severance. "
            "For curative purposes, a clear deed or assignment transferring the mineral interest to the "
            "surface owner (or vice versa) should be obtained and recorded."
        ),
        reasoning_framework=(
            "STEP 1: Identify all outstanding severed mineral interests.\n"
            "STEP 2: Determine current owners of each severed interest.\n"
            "STEP 3: Negotiate acquisition of mineral interests from each owner.\n"
            "STEP 4: Execute mineral deed or assignment from each mineral owner.\n"
            "STEP 5: Record all conveyances in county deed records.\n"
            "STEP 6: Once all interests acquired by surface owner, estates may merge.\n"
            "STEP 7: Merger is default unless instrument or intent preserves severance.\n"
            "STEP 8: Update RRC records and division orders if applicable."
        ),
        key_factors=[
            "Merger doctrine applies when same owner holds both estates",
            "Severance preserved only by clear language in acquisition instrument",
            "All severed interests must be identified and acquired",
            "Each acquisition must be properly conveyed and recorded",
            "RRC records may need updating",
        ],
        primary_authority=[
            "Texas Property Code — general merger doctrine",
            "Moser v. U.S. Steel Corp., 676 S.W.2d 99 (Tex. 1984)",
            "French v. Chevron U.S.A., Inc., 896 S.W.2d 795 (Tex. 1995)",
        ],
        burden_holder="Party seeking reunification",
        adversary_position="Severed mineral interest owner may refuse to sell",
        counter_arguments=[
            "Some mineral owners may refuse to convey",
            "Outstanding royalty interests may complicate full reunification",
            "Mineral interests may be subject to existing leases",
        ],
        resolution_strategy=(
            "Negotiate acquisition of each severed interest. If any owner refuses, "
            "partial reunification may still simplify the ownership structure."
        ),
        issue_category=IssueCategory.ESTATE_REUNIFICATION,
        confidence=0.82,
        confidence_stratification=ConfidenceStratification.AGGRESSIVE,
        controlling_precedent="Moser v. U.S. Steel Corp., 676 S.W.2d 99 (Tex. 1984)",
        curative_document_type="Mineral Deed / Assignment",
        estimated_timeline_days=90,
        typical_cost_range="$2,000-$50,000+ (plus acquisition costs)",
        risk_factors=["Unwilling sellers", "Existing lease obligations", "Outstanding royalties"],
    ))

    # ===================================================================
    # ABSTRACT OF JUDGMENT RESOLUTION DOCTRINES
    # ===================================================================
    blocks.append(DoctrineBlock(
        topic="abstract_of_judgment_resolution",
        keywords=["abstract of judgment", "judgment lien", "expired", "dormant", "release", "tex prop code 52", "satisfaction"],
        conclusion_template=(
            "An Abstract of Judgment creates a lien on all non-exempt real property owned by the debtor "
            "in the county where recorded. The lien is valid for 10 years and may be renewed once for an "
            "additional 10 years. After expiration, it no longer encumbers the property but remains of "
            "record. Resolution requires: (1) satisfaction and release from the judgment creditor, "
            "(2) expiration and affidavit of non-renewal, or (3) motion to release in the underlying court."
        ),
        reasoning_framework=(
            "STEP 1: Identify the abstract of judgment in the county records.\n"
            "STEP 2: Determine the date of filing and whether it has been renewed.\n"
            "STEP 3: If 10 years have elapsed without renewal: lien has expired.\n"
            "STEP 4: For expired liens: file affidavit stating expiration and non-renewal.\n"
            "STEP 5: If judgment has been satisfied: obtain release from creditor and record.\n"
            "STEP 6: If creditor is unresponsive: motion in underlying court for release.\n"
            "STEP 7: Note: homestead property is exempt from judgment liens in Texas."
        ),
        key_factors=[
            "10-year validity period with one renewal allowed",
            "Homestead property exempt from judgment liens",
            "Satisfaction and release from creditor is preferred",
            "Expired liens can be addressed by affidavit",
            "Court motion available if creditor unresponsive",
        ],
        primary_authority=[
            "Texas Property Code Section 52.001 (Abstract of Judgment)",
            "Texas Property Code Section 52.006 (Duration of Judgment Lien)",
            "Texas Constitution Article XVI, Section 50 (Homestead Exemption)",
            "Texas Civil Practice and Remedies Code Section 34.001",
        ],
        burden_holder="Property owner seeking to clear judgment lien",
        adversary_position="Judgment creditor claims judgment unsatisfied or properly renewed",
        counter_arguments=[
            "Judgment may have been properly renewed within 10 years",
            "Partial satisfaction does not release the lien",
            "Federal judgments have different rules (20 years)",
        ],
        resolution_strategy=(
            "Verify filing date and check for renewal. If expired, file affidavit. "
            "If satisfied, obtain and record release. If creditor unavailable, motion to court."
        ),
        issue_category=IssueCategory.JUDGMENT_RESOLUTION,
        confidence=0.88,
        confidence_stratification=ConfidenceStratification.DEFENSIBLE,
        controlling_precedent="Texas Property Code Section 52.006",
        curative_document_type="Release of Abstract of Judgment / Affidavit of Expiration",
        estimated_timeline_days=30,
        typical_cost_range="$500-$2,500",
        risk_factors=["Renewed judgment", "Federal judgment", "Partial satisfaction"],
    ))

    logger.info("Doctrine cache built | blocks={}", len(blocks))
    return blocks


# ---------------------------------------------------------------------------
# Doctrine Interaction Graph
# ---------------------------------------------------------------------------
def build_interaction_graph() -> list[DoctrineInteraction]:
    """Build the interaction graph between doctrine topics."""
    interactions: list[DoctrineInteraction] = [
        DoctrineInteraction(
            source_topic="affidavit_of_heirship_requirements",
            target_topic="judicial_determination_of_heirship",
            interaction_type="alternative",
            description="Judicial determination is the formal alternative when affidavit is insufficient",
            weight=0.9,
        ),
        DoctrineInteraction(
            source_topic="affidavit_of_heirship_requirements",
            target_topic="small_estate_affidavit",
            interaction_type="alternative",
            description="Small estate affidavit may substitute when estate value is under $75,000",
            weight=0.7,
        ),
        DoctrineInteraction(
            source_topic="correction_deed_nonmaterial",
            target_topic="correction_deed_material",
            interaction_type="alternative",
            description="Material correction required when nonmaterial correction is insufficient",
            weight=0.9,
        ),
        DoctrineInteraction(
            source_topic="correction_deed_nonmaterial",
            target_topic="scriveners_affidavit_curative",
            interaction_type="complementary",
            description="Scrivener's affidavit supplements correction deed",
            weight=0.8,
        ),
        DoctrineInteraction(
            source_topic="chain_of_title_gap_resolution",
            target_topic="trespass_to_try_title",
            interaction_type="prerequisite",
            description="Quiet title may be necessary when gap cannot be cured by instrument",
            weight=0.85,
        ),
        DoctrineInteraction(
            source_topic="chain_of_title_gap_resolution",
            target_topic="affidavit_of_heirship_requirements",
            interaction_type="complementary",
            description="Heirship may fill gap when missing link is due to intestate death",
            weight=0.8,
        ),
        DoctrineInteraction(
            source_topic="tax_sale_void_vs_voidable",
            target_topic="trespass_to_try_title",
            interaction_type="prerequisite",
            description="Quiet title recommended after tax sale redemption period expires",
            weight=0.9,
        ),
        DoctrineInteraction(
            source_topic="adverse_possession_five_year",
            target_topic="adverse_possession_ten_year",
            interaction_type="alternative",
            description="10-year statute applies when 5-year requirements (deed/taxes) are not met",
            weight=0.85,
        ),
        DoctrineInteraction(
            source_topic="adverse_possession_ten_year",
            target_topic="adverse_possession_twenty_five_year",
            interaction_type="alternative",
            description="25-year absolute bar when 10-year elements are insufficient",
            weight=0.8,
        ),
        DoctrineInteraction(
            source_topic="foreclosure_notice_defects",
            target_topic="ratification_of_prior_conveyance",
            interaction_type="complementary",
            description="Borrower ratification can cure foreclosure defects",
            weight=0.75,
        ),
        DoctrineInteraction(
            source_topic="lis_pendens_clearance",
            target_topic="trespass_to_try_title",
            interaction_type="complementary",
            description="Resolution of underlying quiet title action clears lis pendens",
            weight=0.85,
        ),
        DoctrineInteraction(
            source_topic="name_variation_affidavit",
            target_topic="chain_of_title_gap_resolution",
            interaction_type="complementary",
            description="Name variation resolution may cure apparent gaps caused by name discrepancies",
            weight=0.7,
        ),
        DoctrineInteraction(
            source_topic="corporate_authority_to_convey",
            target_topic="llc_authority_to_convey",
            interaction_type="alternative",
            description="Different entity types require different authority documentation",
            weight=0.6,
        ),
        DoctrineInteraction(
            source_topic="ratification_of_prior_conveyance",
            target_topic="correction_deed_material",
            interaction_type="alternative",
            description="Material correction may be alternative to ratification when parties cooperate",
            weight=0.7,
        ),
        DoctrineInteraction(
            source_topic="dormant_mineral_interest_act",
            target_topic="surface_mineral_estate_reunification",
            interaction_type="complementary",
            description="Termination of dormant minerals facilitates estate reunification",
            weight=0.8,
        ),
        DoctrineInteraction(
            source_topic="release_expired_lien",
            target_topic="abstract_of_judgment_resolution",
            interaction_type="complementary",
            description="Judgment lien release is a specific type of lien release",
            weight=0.75,
        ),
        DoctrineInteraction(
            source_topic="independent_administration_probate",
            target_topic="muniment_of_title_probate",
            interaction_type="alternative",
            description="Muniment is simpler when no debts exist and no administration needed",
            weight=0.85,
        ),
        DoctrineInteraction(
            source_topic="missing_instrument_reconstruction",
            target_topic="chain_of_title_gap_resolution",
            interaction_type="complementary",
            description="Reconstructing missing instrument directly resolves chain gaps",
            weight=0.9,
        ),
        DoctrineInteraction(
            source_topic="boundary_dispute_resolution",
            target_topic="trespass_to_try_title",
            interaction_type="prerequisite",
            description="Judicial action may be needed when boundary agreement cannot be reached",
            weight=0.7,
        ),
        DoctrineInteraction(
            source_topic="stipulation_of_interest_agreement",
            target_topic="pooling_designation_amendment",
            interaction_type="complementary",
            description="Stipulated interests feed into pooling unit interest allocation",
            weight=0.7,
        ),
    ]

    logger.info("Interaction graph built | edges={}", len(interactions))
    return interactions


# ---------------------------------------------------------------------------
# Quick access functions
# ---------------------------------------------------------------------------
_CACHE: list[DoctrineBlock] | None = None
_INTERACTIONS: list[DoctrineInteraction] | None = None


def get_doctrine_cache() -> list[DoctrineBlock]:
    """Get or build the doctrine cache."""
    global _CACHE
    if _CACHE is None:
        _CACHE = build_doctrine_cache()
    return _CACHE


def get_interaction_graph() -> list[DoctrineInteraction]:
    """Get or build the interaction graph."""
    global _INTERACTIONS
    if _INTERACTIONS is None:
        _INTERACTIONS = build_interaction_graph()
    return _INTERACTIONS


def find_doctrines_by_category(category: IssueCategory) -> list[DoctrineBlock]:
    """Find all doctrines for a given issue category."""
    return [d for d in get_doctrine_cache() if d.issue_category == category]


def find_doctrine_by_topic(topic: str) -> DoctrineBlock | None:
    """Find a doctrine by exact topic name."""
    for d in get_doctrine_cache():
        if d.topic == topic:
            return d
    return None


def find_doctrines_by_keyword(keyword: str) -> list[DoctrineBlock]:
    """Find doctrines matching a keyword."""
    keyword_lower = keyword.lower()
    return [
        d for d in get_doctrine_cache()
        if any(keyword_lower in kw.lower() for kw in d.keywords)
    ]


def get_interactions_for_topic(topic: str) -> list[DoctrineInteraction]:
    """Get all interactions involving a specific topic."""
    return [
        i for i in get_interaction_graph()
        if i.source_topic == topic or i.target_topic == topic
    ]
