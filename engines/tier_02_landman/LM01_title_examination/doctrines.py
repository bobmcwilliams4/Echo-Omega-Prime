"""
LM01 Title Examination Engine - Doctrines Module
=================================================

Texas title examination doctrines, standards, and legal rules.

Covers:
- Chain of title rules and requirements
- Curative standards for common defects
- Title defect classifications with severity
- Texas Title Standards (State Bar of Texas)
- Marketable vs insurable title distinctions
- After-acquired title doctrine
- Estoppel by deed
- Shelter rule
- Bona fide purchaser protections
- Recording act priorities (race-notice)
- Wild deeds and chain break analysis
- Forgery and fraud rules
- Adverse possession and limitations
- Probate requirements for succession
- Community property rules
- Mineral estate dominance doctrine
- Executive right severance

Author: ECHO OMEGA PRIME Build System
Engine: LM01 Title Examination
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import date, timedelta
from decimal import Decimal
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from loguru import logger


# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------

class DefectSeverity(str, Enum):
    """Severity levels for title defects."""
    CRITICAL = "critical"
    MAJOR = "major"
    MINOR = "minor"
    INFORMATIONAL = "informational"


class DefectCategory(str, Enum):
    """Categories of title defects."""
    CHAIN_BREAK = "chain_break"
    WILD_DEED = "wild_deed"
    FORGERY = "forgery"
    FRAUD = "fraud"
    MISSING_HEIR = "missing_heir"
    DOUBLE_GRANT = "double_grant"
    OVERLAPPING_INTEREST = "overlapping_interest"
    UNRELEASED_MORTGAGE = "unreleased_mortgage"
    EXPIRED_LIEN = "expired_lien"
    TAX_DELINQUENCY = "tax_delinquency"
    MISSING_MARITAL = "missing_marital_acknowledgment"
    DEFECTIVE_ACKNOWLEDGMENT = "defective_acknowledgment"
    MISSING_PROBATE = "missing_probate"
    GAP_IN_CHAIN = "gap_in_chain"
    NAME_VARIANCE = "name_variance"
    RECORDING_GAP = "recording_gap"
    MISSING_LEGAL = "missing_legal_description"
    CONSIDERATION_MISSING = "consideration_recital_missing"
    SCRIVENERS_ERROR = "scriveners_error"
    IMPROPER_VENUE = "improper_venue"
    LATE_RECORDING = "late_recording"
    ADVERSE_POSSESSION = "adverse_possession"
    TAX_SALE_DEFECT = "tax_sale_defect"
    MINERAL_RESERVATION_AMBIGUITY = "mineral_reservation_ambiguity"
    COMMUNITY_PROPERTY_ISSUE = "community_property_issue"
    ENTITY_AUTHORITY_DEFECT = "entity_authority_defect"
    POWER_OF_ATTORNEY_DEFECT = "power_of_attorney_defect"
    UNDIVIDED_INTEREST_ERROR = "undivided_interest_error"


class CurativeAction(str, Enum):
    """Types of curative actions."""
    CORRECTION_DEED = "correction_deed"
    AFFIDAVIT_OF_HEIRSHIP = "affidavit_of_heirship"
    AFFIDAVIT_OF_IDENTITY = "affidavit_of_identity"
    AFFIDAVIT_OF_NON_PRODUCTION = "affidavit_of_non_production"
    RATIFICATION = "ratification"
    RELEASE_OF_LIEN = "release_of_lien"
    QUIET_TITLE_ACTION = "quiet_title_action"
    PROBATE_PROCEEDING = "probate_proceeding"
    STIPULATION_OF_INTEREST = "stipulation_of_interest"
    QUITCLAIM_DEED = "quitclaim_deed"
    TAX_CERTIFICATE = "tax_certificate"
    TITLE_INSURANCE = "title_insurance"
    COURT_ORDER = "court_order"
    AFFIDAVIT_OF_FACTS = "affidavit_of_facts"
    SUBORDINATION_AGREEMENT = "subordination_agreement"
    ESTOPPEL_LETTER = "estoppel_letter"
    JOINDER = "joinder"
    DISCLAIMER = "disclaimer"


class TitleType(str, Enum):
    """Types of title quality."""
    MARKETABLE = "marketable"
    INSURABLE = "insurable"
    RECORD = "record"
    GOOD_AND_INDEFEASIBLE = "good_and_indefeasible"
    DOUBTFUL = "doubtful"
    DEFECTIVE = "defective"
    UNMARKETABLE = "unmarketable"


class RecordingActType(str, Enum):
    """Types of recording act systems."""
    RACE = "race"
    NOTICE = "notice"
    RACE_NOTICE = "race_notice"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class TexasTitleStandard:
    """
    A Texas Title Standard as published by the State Bar of Texas
    Title Standards Committee.
    """
    standard_number: str
    title: str
    category: str
    text: str
    applies_to: List[str]
    effective_date: str
    supersedes: Optional[str] = None
    notes: List[str] = field(default_factory=list)

    def matches_defect(self, defect_category: DefectCategory) -> bool:
        """Check if this standard addresses a specific defect category."""
        category_str = defect_category.value.lower()
        text_lower = self.text.lower()
        title_lower = self.title.lower()
        return category_str in text_lower or category_str in title_lower

    def to_dict(self) -> Dict[str, Any]:
        return {
            "standard_number": self.standard_number,
            "title": self.title,
            "category": self.category,
            "text": self.text,
            "applies_to": self.applies_to,
            "effective_date": self.effective_date,
            "supersedes": self.supersedes,
            "notes": list(self.notes),
        }


@dataclass(frozen=True)
class DefectClassification:
    """
    Classification of a title defect with severity, cure path,
    and legal authority.
    """
    defect_id: str
    category: DefectCategory
    severity: DefectSeverity
    name: str
    description: str
    legal_authority: str
    cure_actions: List[CurativeAction]
    cure_priority: int
    affects_marketability: bool
    affects_insurability: bool
    statute_of_limitations_years: Optional[int] = None
    auto_curable: bool = False
    notes: List[str] = field(default_factory=list)

    def is_critical(self) -> bool:
        """Return True if defect is critical severity."""
        return self.severity == DefectSeverity.CRITICAL

    def blocks_title(self) -> bool:
        """Return True if defect blocks both marketability and insurability."""
        return self.affects_marketability and self.affects_insurability

    def primary_cure(self) -> Optional[CurativeAction]:
        """Return the primary (first) curative action."""
        if self.cure_actions:
            return self.cure_actions[0]
        return None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "defect_id": self.defect_id,
            "category": self.category.value,
            "severity": self.severity.value,
            "name": self.name,
            "description": self.description,
            "legal_authority": self.legal_authority,
            "cure_actions": [c.value for c in self.cure_actions],
            "cure_priority": self.cure_priority,
            "affects_marketability": self.affects_marketability,
            "affects_insurability": self.affects_insurability,
            "statute_of_limitations_years": self.statute_of_limitations_years,
            "auto_curable": self.auto_curable,
            "notes": list(self.notes),
        }


@dataclass(frozen=True)
class CurativeStandard:
    """
    A curative standard defining how to remedy a specific defect type.
    """
    standard_id: str
    action: CurativeAction
    target_defect: DefectCategory
    description: str
    requirements: List[str]
    typical_cost_range: str
    typical_time_days: int
    legal_authority: str
    recording_required: bool
    notarization_required: bool
    witness_count: int
    acceptance_criteria: List[str]

    def meets_criteria(self, provided_items: List[str]) -> bool:
        """Check if provided items meet all acceptance criteria."""
        provided_set = {item.lower().strip() for item in provided_items}
        for criterion in self.acceptance_criteria:
            if criterion.lower().strip() not in provided_set:
                return False
        return True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "standard_id": self.standard_id,
            "action": self.action.value,
            "target_defect": self.target_defect.value,
            "description": self.description,
            "requirements": list(self.requirements),
            "typical_cost_range": self.typical_cost_range,
            "typical_time_days": self.typical_time_days,
            "legal_authority": self.legal_authority,
            "recording_required": self.recording_required,
            "notarization_required": self.notarization_required,
            "witness_count": self.witness_count,
            "acceptance_criteria": list(self.acceptance_criteria),
        }


@dataclass(frozen=True)
class RecordingActRule:
    """
    Recording act rule for a specific jurisdiction.
    """
    jurisdiction: str
    act_type: RecordingActType
    statute_citation: str
    description: str
    bfp_requirements: List[str]
    shelter_rule_applies: bool
    after_acquired_title: bool
    wild_deed_void: bool
    constructive_notice_from_recording: bool
    priority_rules: List[str]

    def is_bona_fide_purchaser(
        self,
        paid_valuable_consideration: bool,
        without_notice: bool,
        recorded_first: bool,
    ) -> bool:
        """Determine if a party qualifies as a bona fide purchaser."""
        if self.act_type == RecordingActType.RACE:
            return recorded_first
        elif self.act_type == RecordingActType.NOTICE:
            return paid_valuable_consideration and without_notice
        elif self.act_type == RecordingActType.RACE_NOTICE:
            return paid_valuable_consideration and without_notice and recorded_first
        return False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "jurisdiction": self.jurisdiction,
            "act_type": self.act_type.value,
            "statute_citation": self.statute_citation,
            "description": self.description,
            "bfp_requirements": list(self.bfp_requirements),
            "shelter_rule_applies": self.shelter_rule_applies,
            "after_acquired_title": self.after_acquired_title,
            "wild_deed_void": self.wild_deed_void,
            "constructive_notice_from_recording": self.constructive_notice_from_recording,
            "priority_rules": list(self.priority_rules),
        }


# ---------------------------------------------------------------------------
# Texas Title Standards
# ---------------------------------------------------------------------------

TEXAS_TITLE_STANDARDS: List[TexasTitleStandard] = [
    TexasTitleStandard(
        standard_number="1.10",
        title="Period of Search",
        category="general",
        text="Title should be searched from sovereignty of the soil. In the absence of"
             " special circumstances, a search of the records for a period of at least"
             " 60 years is sufficient to establish marketable record title. Where the"
             " abstract reflects a connected chain of title from sovereignty, a shorter"
             " search period may be acceptable depending on the circumstances.",
        applies_to=["all"],
        effective_date="1998-01-01",
        notes=[
            "Most title companies require 40-year minimum search",
            "Oil and gas title typically requires sovereignty search",
            "60-year standard for general real property",
        ],
    ),
    TexasTitleStandard(
        standard_number="1.20",
        title="Marketable Title",
        category="general",
        text="Marketable title is a title free from reasonable doubt as to matters of"
             " law and fact; such title as a reasonably prudent person, familiar with"
             " the facts and their legal significance, would accept. It need not be a"
             " perfect title, but must be one that is free from plausible or reasonable"
             " objections. A marketable title is one which is free from liens,"
             " encumbrances, and defects other than those waived by the purchaser.",
        applies_to=["all"],
        effective_date="1998-01-01",
    ),
    TexasTitleStandard(
        standard_number="1.30",
        title="Insurable Title",
        category="general",
        text="Insurable title is title that a reputable title insurance company would"
             " be willing to insure at standard rates without special exceptions."
             " Insurable title may include defects that do not affect marketability"
             " but which a title company will insure over with appropriate exceptions"
             " or endorsements. Insurable title is generally a lesser standard than"
             " marketable title.",
        applies_to=["all"],
        effective_date="1998-01-01",
        notes=["Title insurance does not cure defects, only insures against loss"],
    ),
    TexasTitleStandard(
        standard_number="2.10",
        title="Recitals of Consideration",
        category="conveyances",
        text="A recital of consideration in a deed is not essential to its validity"
             " as a conveyance. Under Texas law, a deed without recital of"
             " consideration is valid as between the parties and as to subsequent"
             " purchasers with notice. However, lack of consideration may affect"
             " the grantee's status as a bona fide purchaser for value.",
        applies_to=["warranty_deed", "special_warranty_deed", "quitclaim_deed"],
        effective_date="1998-01-01",
    ),
    TexasTitleStandard(
        standard_number="2.20",
        title="After-Acquired Title (Estoppel by Deed)",
        category="conveyances",
        text="Under Texas law, if a grantor conveys land by warranty deed to which"
             " the grantor has no title or defective title, and the grantor subsequently"
             " acquires the title, the after-acquired title inures to the benefit of"
             " the grantee by way of estoppel by deed. This doctrine applies only to"
             " warranty deeds and deeds that contain covenants of warranty or purport"
             " to convey the fee simple. It does not apply to quitclaim deeds.",
        applies_to=["warranty_deed", "special_warranty_deed"],
        effective_date="1998-01-01",
        notes=[
            "Tex. Prop. Code Sec. 5.023",
            "Does not apply to quitclaim deeds",
            "May apply to mineral deeds with warranty covenants",
        ],
    ),
    TexasTitleStandard(
        standard_number="2.30",
        title="Quitclaim Deeds",
        category="conveyances",
        text="A quitclaim deed conveys only such interest as the grantor may have at"
             " the time of the conveyance. It does not convey after-acquired title."
             " A grantee under a quitclaim deed cannot be a bona fide purchaser without"
             " notice because the quitclaim deed itself provides constructive notice"
             " that the grantor may not own the property. However, the grantee of a"
             " quitclaim deed is protected by the shelter rule if the grantee's"
             " predecessor in title was a bona fide purchaser.",
        applies_to=["quitclaim_deed"],
        effective_date="1998-01-01",
    ),
    TexasTitleStandard(
        standard_number="3.10",
        title="Community Property Presumption",
        category="marital_rights",
        text="In Texas, property acquired during marriage is presumed to be community"
             " property regardless of which spouse's name appears on the title. Both"
             " spouses must join in a conveyance of homestead property and in a"
             " conveyance of community real property. A conveyance by only one spouse"
             " of community property may be voidable at the election of the non-joining"
             " spouse. Separate property may be conveyed by the owning spouse alone"
             " unless it is the homestead.",
        applies_to=["all"],
        effective_date="1998-01-01",
        notes=[
            "Tex. Family Code Sec. 3.002 (community property presumption)",
            "Tex. Const. Art. XVI Sec. 50 (homestead)",
            "Mineral interests are real property subject to community property rules",
        ],
    ),
    TexasTitleStandard(
        standard_number="3.20",
        title="Homestead Protections",
        category="marital_rights",
        text="No conveyance, mortgage, or other encumbrance of the homestead is valid"
             " unless both spouses join in the execution. A conveyance of the homestead"
             " by one spouse without the joinder of the other is void, not merely"
             " voidable, and may not be ratified. The homestead designation attaches"
             " automatically to the urban or rural property used as the family home.",
        applies_to=["all"],
        effective_date="1998-01-01",
    ),
    TexasTitleStandard(
        standard_number="4.10",
        title="Acknowledgment Requirements",
        category="execution",
        text="A deed must be acknowledged before a notary public or other authorized"
             " officer to be eligible for recording. A defective acknowledgment does"
             " not invalidate the deed as between the parties but prevents the deed"
             " from imparting constructive notice. An instrument with a defective"
             " acknowledgment is not entitled to be recorded and does not give"
             " constructive notice to subsequent purchasers.",
        applies_to=["all"],
        effective_date="1998-01-01",
        notes=[
            "Tex. Civ. Prac. & Rem. Code Sec. 121.001",
            "Tex. Property Code Sec. 12.001",
        ],
    ),
    TexasTitleStandard(
        standard_number="4.20",
        title="Delivery Requirements",
        category="execution",
        text="A deed must be delivered by the grantor and accepted by the grantee to"
             " be effective. Recording creates a presumption of delivery. A deed that"
             " is not delivered is void and conveys no interest. Delivery may be"
             " actual (physical handing over) or constructive (recorded, placed"
             " beyond grantor's control, or acknowledged to grantee).",
        applies_to=["all"],
        effective_date="1998-01-01",
    ),
    TexasTitleStandard(
        standard_number="5.10",
        title="Recording Act - Race-Notice",
        category="recording",
        text="Texas is a race-notice jurisdiction. To prevail over an unrecorded"
             " instrument, a subsequent purchaser must: (1) pay valuable consideration,"
             " (2) take without actual or constructive notice of the prior instrument,"
             " and (3) record first. If the subsequent purchaser fails to meet all"
             " three requirements, the prior unrecorded instrument prevails.",
        applies_to=["all"],
        effective_date="1998-01-01",
        notes=[
            "Tex. Property Code Sec. 13.001",
            "Constructive notice arises from properly recorded instruments",
            "Actual notice includes knowledge or facts sufficient to put on inquiry",
        ],
    ),
    TexasTitleStandard(
        standard_number="5.20",
        title="Shelter Rule",
        category="recording",
        text="A person who acquires property from a bona fide purchaser (BFP) takes"
             " shelter under the BFP's superior title, even if the subsequent grantee"
             " has notice of the prior unrecorded interest. The shelter rule protects"
             " the transferee of a BFP and allows the BFP's title to be freely"
             " transferable. Exception: the shelter rule does not protect the original"
             " grantor who created the problem by conveying twice.",
        applies_to=["all"],
        effective_date="1998-01-01",
    ),
    TexasTitleStandard(
        standard_number="5.30",
        title="Wild Deeds",
        category="recording",
        text="A wild deed is a recorded instrument that is not connected to the chain"
             " of title because a prior instrument in the chain was not recorded. A"
             " wild deed does not impart constructive notice because a title searcher"
             " would have no reason to search under the name of a grantor who does not"
             " appear in the chain of record title. However, actual notice of a wild"
             " deed defeats the subsequent purchaser's BFP status.",
        applies_to=["all"],
        effective_date="1998-01-01",
    ),
    TexasTitleStandard(
        standard_number="6.10",
        title="Mineral Estate Severance",
        category="minerals",
        text="The mineral estate may be severed from the surface estate by grant or"
             " reservation. Once severed, the mineral estate and surface estate are"
             " treated as separate tracts of land. The mineral estate is the dominant"
             " estate and has the implied right to use so much of the surface as is"
             " reasonably necessary to explore, develop, and produce the minerals."
             " This right exists regardless of surface ownership changes.",
        applies_to=["mineral_deed", "warranty_deed", "royalty_deed"],
        effective_date="1998-01-01",
        notes=[
            "Dominant mineral estate - Acker v. Guinn (1979)",
            "Accommodation doctrine - Getty Oil Co. v. Jones (1971)",
        ],
    ),
    TexasTitleStandard(
        standard_number="6.20",
        title="Mineral vs Royalty Interest",
        category="minerals",
        text="A mineral interest includes the right to explore, develop, and produce"
             " minerals, plus the right to receive bonus, delay rentals, and royalties."
             " A royalty interest is a right to receive a share of production or"
             " proceeds without the right to explore or develop. The distinction is"
             " critical because mineral interest owners have executive rights (right"
             " to lease) while royalty interest owners generally do not.",
        applies_to=["mineral_deed", "royalty_deed"],
        effective_date="1998-01-01",
        notes=[
            "Executive right may be severed from mineral fee",
            "Non-participating royalty interest (NPRI) has no right to lease",
        ],
    ),
    TexasTitleStandard(
        standard_number="6.30",
        title="Fraction/Mineral Deed Construction",
        category="minerals",
        text="When a mineral deed conveys a fraction of minerals, courts must determine"
             " whether the fraction applies to the grantor's interest (a fractional"
             " mineral interest) or to the total mineral estate (a fixed mineral"
             " interest). The two-grant doctrine and the estate misconception"
             " doctrine have been abrogated in favor of the four corners approach."
             " Texas courts now look to the entire instrument to determine intent.",
        applies_to=["mineral_deed"],
        effective_date="1998-01-01",
        notes=[
            "Hysaw v. Dawkins (2013) - abrogated two-grant doctrine",
            "Look to four corners of instrument for intent",
        ],
    ),
    TexasTitleStandard(
        standard_number="7.10",
        title="Adverse Possession - 5 Year Statute",
        category="adverse_possession",
        text="A person who cultivates, uses, or enjoys real property for 5 continuous"
             " years under a duly registered deed or other memorandum of title that"
             " fixes the boundaries and pays all taxes, acquires title by limitations."
             " This applies to both surface and mineral estates. The claimant must"
             " prove actual, visible, continuous, notorious, distinct, hostile, and"
             " exclusive possession.",
        applies_to=["all"],
        effective_date="1998-01-01",
        notes=[
            "Tex. Civ. Prac. & Rem. Code Sec. 16.025",
            "Rarely applies to mineral interests (difficult to prove possession)",
        ],
    ),
    TexasTitleStandard(
        standard_number="7.20",
        title="Adverse Possession - 10 Year Statute",
        category="adverse_possession",
        text="A person who uses or enjoys real property for 10 continuous years"
             " acquires title by limitations without requirement of a registered"
             " deed or tax payment. The claimant must still prove the essential"
             " elements of adverse possession. This is the most commonly invoked"
             " statute of limitations for title disputes.",
        applies_to=["all"],
        effective_date="1998-01-01",
        notes=["Tex. Civ. Prac. & Rem. Code Sec. 16.026"],
    ),
    TexasTitleStandard(
        standard_number="7.30",
        title="Adverse Possession - 25 Year Statute",
        category="adverse_possession",
        text="A person who holds real property under a claim of right for 25 years"
             " acquires title by limitations. This statute applies regardless of"
             " disability and requires no deed, tax payment, or good faith. It is"
             " the broadest of the adverse possession statutes and is often used"
             " to quiet title to long-held property.",
        applies_to=["all"],
        effective_date="1998-01-01",
        notes=["Tex. Civ. Prac. & Rem. Code Sec. 16.028"],
    ),
    TexasTitleStandard(
        standard_number="8.10",
        title="Descent and Distribution",
        category="probate",
        text="When a person dies intestate (without a will), their property passes"
             " according to the Texas Estates Code descent and distribution rules."
             " Community property passes to the surviving spouse if all children are"
             " also children of the surviving spouse. Separate property follows a"
             " different distribution. An heirship proceeding or affidavit of heirship"
             " is necessary to establish the chain of title through an intestate"
             " decedent.",
        applies_to=["all"],
        effective_date="1998-01-01",
        notes=[
            "Tex. Estates Code Ch. 201 (intestate succession)",
            "Affidavit of heirship - Tex. Estates Code Sec. 203.001",
            "Must wait 4 years after death for affidavit to become prima facie evidence",
        ],
    ),
    TexasTitleStandard(
        standard_number="8.20",
        title="Probate of Wills",
        category="probate",
        text="A will must be admitted to probate within 4 years of the testator's"
             " death to be effective as a muniment of title. After 4 years, the will"
             " may be admitted as a muniment of title if the applicant was not in"
             " default in failing to present it for probate. An independent"
             " administration is preferred in Texas and allows the executor to act"
             " without court supervision for most transactions.",
        applies_to=["all"],
        effective_date="1998-01-01",
        notes=[
            "Tex. Estates Code Sec. 256.003 (4-year limitation)",
            "Muniment of title - Tex. Estates Code Sec. 257.001",
        ],
    ),
    TexasTitleStandard(
        standard_number="9.10",
        title="Entity Authority - Corporations",
        category="entities",
        text="A deed from a corporation must be executed by an authorized officer."
             " The title examiner should verify the corporation is in good standing"
             " with the Texas Secretary of State. A deed from a dissolved corporation"
             " may be void. Corporate authority is typically established by a"
             " resolution of the board of directors authorizing the transaction.",
        applies_to=["all"],
        effective_date="1998-01-01",
    ),
    TexasTitleStandard(
        standard_number="9.20",
        title="Entity Authority - LLCs and Partnerships",
        category="entities",
        text="For LLCs, the company agreement governs authority to convey property."
             " A manager-managed LLC requires the manager's signature; a member-managed"
             " LLC may require all members. For partnerships, all partners must join"
             " unless the partnership agreement authorizes a specific partner to act."
             " Limited partnerships require the general partner's signature.",
        applies_to=["all"],
        effective_date="1998-01-01",
    ),
    TexasTitleStandard(
        standard_number="9.30",
        title="Entity Authority - Trusts",
        category="entities",
        text="A deed from a trust must be executed by the trustee. The title examiner"
             " should verify the trustee's authority under the trust instrument. The"
             " trust instrument should be reviewed for restrictions on the trustee's"
             " power to convey real property. If the trust is not recorded, the"
             " examiner may require a certificate of trust under Tex. Property Code"
             " Sec. 114.086.",
        applies_to=["all"],
        effective_date="1998-01-01",
    ),
    TexasTitleStandard(
        standard_number="10.10",
        title="Tax Sales",
        category="tax_liens",
        text="A tax sale deed conveys only the interest of the person assessed."
             " The owner has a right of redemption: 2 years for homestead and"
             " agricultural property, 180 days for other property. A tax sale may be"
             " voided if proper notice was not given. After expiration of the"
             " redemption period, a tax deed creates a presumption of valid title.",
        applies_to=["tax_deed"],
        effective_date="1998-01-01",
        notes=[
            "Tex. Tax Code Sec. 34.21 (right of redemption)",
            "Tax lien is superior to all other liens except federal tax lien",
        ],
    ),
    TexasTitleStandard(
        standard_number="10.20",
        title="Federal Tax Liens",
        category="tax_liens",
        text="A federal tax lien attaches to all property of the taxpayer. It is"
             " effective from the date of assessment but is not valid against certain"
             " purchasers, holders of security interests, mechanic's lienors, or"
             " judgment lien creditors until a notice of federal tax lien is filed."
             " The lien expires 10 years from the date of assessment unless renewed.",
        applies_to=["all"],
        effective_date="1998-01-01",
    ),
    TexasTitleStandard(
        standard_number="11.10",
        title="Oil and Gas Lease Requirements",
        category="oil_gas",
        text="An oil and gas lease must be in writing and must contain: identification"
             " of lessor and lessee, adequate legal description, granting clause,"
             " habendum clause (primary term), royalty clause, and delay rental"
             " clause (or paid-up provision). The lease must be signed by all mineral"
             " owners (or their proportionate share) and acknowledged for recording.",
        applies_to=["oil_gas_lease"],
        effective_date="1998-01-01",
    ),
    TexasTitleStandard(
        standard_number="11.20",
        title="Held by Production",
        category="oil_gas",
        text="An oil and gas lease is maintained beyond the primary term by production"
             " in paying quantities. Production in paying quantities means production"
             " that yields a profit over operating costs, even if the revenue does not"
             " fully repay the drilling costs. A shut-in royalty clause may maintain"
             " the lease in the absence of actual production if gas is capable of"
             " being produced but there is no available market.",
        applies_to=["oil_gas_lease"],
        effective_date="1998-01-01",
    ),
    TexasTitleStandard(
        standard_number="11.30",
        title="Pooling and Unitization",
        category="oil_gas",
        text="A pooling clause in an oil and gas lease authorizes the lessee to combine"
             " the leased premises with other lands to form a drilling or spacing unit."
             " Production from any part of the pooled unit maintains the lease as to"
             " the entire leased premises. Unitization may be voluntary (contractual)"
             " or compulsory (Railroad Commission order). Cross-conveyance theory"
             " applies in Texas: each working interest owner conveys an undivided"
             " interest to every other working interest owner.",
        applies_to=["oil_gas_lease", "pooling_agreement", "unit_designation"],
        effective_date="1998-01-01",
    ),
    TexasTitleStandard(
        standard_number="12.10",
        title="Power of Attorney",
        category="agency",
        text="A power of attorney authorizing the agent to convey real property must"
             " be in writing, signed by the principal, and acknowledged for recording."
             " A durable power of attorney survives the principal's incapacity."
             " The title examiner should verify that the power of attorney was in"
             " effect at the time of the conveyance and that the agent acted within"
             " the scope of authority granted.",
        applies_to=["all"],
        effective_date="1998-01-01",
    ),
    TexasTitleStandard(
        standard_number="13.10",
        title="Forgery and Void vs Voidable",
        category="fraud",
        text="A forged instrument is void ab initio and conveys no interest, even to"
             " a bona fide purchaser. This is the critical distinction between forgery"
             " (void) and fraud (voidable). A deed obtained by fraud is voidable and"
             " passes title that may be ratified or that a bona fide purchaser for"
             " value without notice may acquire good title under. A forged deed can"
             " never pass good title regardless of the purchaser's innocence.",
        applies_to=["all"],
        effective_date="1998-01-01",
        notes=[
            "No statute of limitations on forgery",
            "Fraud has 4-year statute of limitations",
            "BFP protection available for fraud but NOT forgery",
        ],
    ),
    TexasTitleStandard(
        standard_number="14.10",
        title="Name Variances",
        category="curative",
        text="Minor variations in a party's name between instruments do not break"
             " the chain of title if the identity of the party can be reasonably"
             " established. Common acceptable variances include: use of initials vs."
             " full name, misspellings that are phonetically similar, use of maiden"
             " vs. married name with supporting evidence. An affidavit of identity"
             " may be used to cure a name variance.",
        applies_to=["all"],
        effective_date="1998-01-01",
    ),
]


# ---------------------------------------------------------------------------
# Defect Classifications
# ---------------------------------------------------------------------------

DEFECT_CLASSIFICATIONS: List[DefectClassification] = [
    DefectClassification(
        defect_id="DEF-001",
        category=DefectCategory.CHAIN_BREAK,
        severity=DefectSeverity.CRITICAL,
        name="Break in Chain of Title",
        description="A conveyance gap exists where a grantor conveyed property without "
                    "having received title from a prior grantee in the chain. No recorded "
                    "instrument connects the current grantor to the chain of title.",
        legal_authority="Tex. Property Code Sec. 13.001; common law chain of title doctrine",
        cure_actions=[CurativeAction.QUIET_TITLE_ACTION, CurativeAction.QUITCLAIM_DEED,
                      CurativeAction.AFFIDAVIT_OF_FACTS],
        cure_priority=1,
        affects_marketability=True,
        affects_insurability=True,
    ),
    DefectClassification(
        defect_id="DEF-002",
        category=DefectCategory.WILD_DEED,
        severity=DefectSeverity.CRITICAL,
        name="Wild Deed",
        description="A recorded deed from a grantor who does not appear in the chain of "
                    "record title. The deed cannot impart constructive notice because a "
                    "title searcher would not discover it through a normal grantor-grantee "
                    "index search.",
        legal_authority="Common law; Luthi v. Evans, 576 P.2d 1064 (Kan. 1978)",
        cure_actions=[CurativeAction.QUIET_TITLE_ACTION, CurativeAction.QUITCLAIM_DEED],
        cure_priority=1,
        affects_marketability=True,
        affects_insurability=True,
    ),
    DefectClassification(
        defect_id="DEF-003",
        category=DefectCategory.FORGERY,
        severity=DefectSeverity.CRITICAL,
        name="Forgery",
        description="An instrument bearing a forged signature is void ab initio. No title "
                    "passes through a forged instrument, and even a bona fide purchaser "
                    "cannot acquire good title through a forged deed.",
        legal_authority="Common law; Tex. Penal Code Sec. 32.21",
        cure_actions=[CurativeAction.QUIET_TITLE_ACTION, CurativeAction.COURT_ORDER],
        cure_priority=1,
        affects_marketability=True,
        affects_insurability=True,
        statute_of_limitations_years=None,
        notes=["No statute of limitations - forgery is void forever"],
    ),
    DefectClassification(
        defect_id="DEF-004",
        category=DefectCategory.FRAUD,
        severity=DefectSeverity.CRITICAL,
        name="Fraud in Execution",
        description="A deed obtained through fraud is voidable (not void). The defrauded "
                    "party may set aside the deed, but a bona fide purchaser for value "
                    "without notice acquires good title.",
        legal_authority="Tex. Bus. & Com. Code Sec. 27.01; 4-year limitations",
        cure_actions=[CurativeAction.COURT_ORDER, CurativeAction.RATIFICATION,
                      CurativeAction.TITLE_INSURANCE],
        cure_priority=2,
        affects_marketability=True,
        affects_insurability=False,
        statute_of_limitations_years=4,
    ),
    DefectClassification(
        defect_id="DEF-005",
        category=DefectCategory.MISSING_HEIR,
        severity=DefectSeverity.CRITICAL,
        name="Missing or Unknown Heir",
        description="A decedent's interest was not properly conveyed through probate or "
                    "heirship proceedings. One or more heirs may have undisclosed or "
                    "undivested interest in the property.",
        legal_authority="Tex. Estates Code Ch. 201-202; Tex. Estates Code Sec. 203.001",
        cure_actions=[CurativeAction.AFFIDAVIT_OF_HEIRSHIP, CurativeAction.PROBATE_PROCEEDING,
                      CurativeAction.QUIET_TITLE_ACTION],
        cure_priority=1,
        affects_marketability=True,
        affects_insurability=True,
    ),
    DefectClassification(
        defect_id="DEF-006",
        category=DefectCategory.DOUBLE_GRANT,
        severity=DefectSeverity.CRITICAL,
        name="Double Grant / Double Conveyance",
        description="The same interest was conveyed to two or more different grantees. "
                    "Priority between competing grantees is determined by the recording "
                    "act (race-notice in Texas).",
        legal_authority="Tex. Property Code Sec. 13.001 (race-notice statute)",
        cure_actions=[CurativeAction.QUIET_TITLE_ACTION, CurativeAction.QUITCLAIM_DEED],
        cure_priority=1,
        affects_marketability=True,
        affects_insurability=True,
    ),
    DefectClassification(
        defect_id="DEF-007",
        category=DefectCategory.OVERLAPPING_INTEREST,
        severity=DefectSeverity.CRITICAL,
        name="Overlapping Interest (Exceeds 100%)",
        description="The total interests conveyed exceed the whole estate. This typically "
                    "results from a double grant, calculation error, or failure to account "
                    "for prior reservations.",
        legal_authority="Common law; mathematical impossibility doctrine",
        cure_actions=[CurativeAction.STIPULATION_OF_INTEREST, CurativeAction.COURT_ORDER,
                      CurativeAction.QUIET_TITLE_ACTION],
        cure_priority=1,
        affects_marketability=True,
        affects_insurability=True,
    ),
    DefectClassification(
        defect_id="DEF-008",
        category=DefectCategory.UNRELEASED_MORTGAGE,
        severity=DefectSeverity.MAJOR,
        name="Unreleased Mortgage / Deed of Trust",
        description="A mortgage or deed of trust appears of record with no corresponding "
                    "release or satisfaction. The lien remains a cloud on title until "
                    "properly released.",
        legal_authority="Tex. Property Code Sec. 12.014; Tex. Civ. Prac. & Rem. Code Sec. 16.035",
        cure_actions=[CurativeAction.RELEASE_OF_LIEN, CurativeAction.AFFIDAVIT_OF_FACTS,
                      CurativeAction.COURT_ORDER],
        cure_priority=2,
        affects_marketability=True,
        affects_insurability=False,
        statute_of_limitations_years=4,
        notes=["Deed of trust lien becomes barred 4 years after maturity date"],
    ),
    DefectClassification(
        defect_id="DEF-009",
        category=DefectCategory.EXPIRED_LIEN,
        severity=DefectSeverity.MAJOR,
        name="Expired but Unreleased Lien",
        description="A lien that has expired by operation of law but remains of record "
                    "without a release. While not enforceable, it constitutes a cloud "
                    "on title.",
        legal_authority="Tex. Civ. Prac. & Rem. Code Sec. 16.035; Tex. Property Code Sec. 16.037",
        cure_actions=[CurativeAction.RELEASE_OF_LIEN, CurativeAction.AFFIDAVIT_OF_FACTS],
        cure_priority=3,
        affects_marketability=False,
        affects_insurability=False,
        auto_curable=True,
        notes=["May be cured by affidavit showing lien is barred by limitations"],
    ),
    DefectClassification(
        defect_id="DEF-010",
        category=DefectCategory.TAX_DELINQUENCY,
        severity=DefectSeverity.MAJOR,
        name="Tax Delinquency",
        description="Ad valorem taxes are delinquent on the property. Tax liens are "
                    "superior to all other liens. Continued delinquency may result "
                    "in tax sale.",
        legal_authority="Tex. Tax Code Sec. 32.01 (tax lien priority); Sec. 33.01 (delinquency)",
        cure_actions=[CurativeAction.TAX_CERTIFICATE],
        cure_priority=2,
        affects_marketability=True,
        affects_insurability=True,
    ),
    DefectClassification(
        defect_id="DEF-011",
        category=DefectCategory.MISSING_MARITAL,
        severity=DefectSeverity.MAJOR,
        name="Missing Marital Joinder / Acknowledgment",
        description="A conveyance of homestead or community property without joinder of "
                    "both spouses. Homestead conveyances without spousal joinder are "
                    "void; community property conveyances are voidable.",
        legal_authority="Tex. Const. Art. XVI Sec. 50; Tex. Family Code Sec. 5.001",
        cure_actions=[CurativeAction.RATIFICATION, CurativeAction.JOINDER,
                      CurativeAction.QUITCLAIM_DEED],
        cure_priority=2,
        affects_marketability=True,
        affects_insurability=True,
        notes=["Homestead: VOID without joinder; Community: VOIDABLE"],
    ),
    DefectClassification(
        defect_id="DEF-012",
        category=DefectCategory.DEFECTIVE_ACKNOWLEDGMENT,
        severity=DefectSeverity.MAJOR,
        name="Defective Acknowledgment",
        description="The instrument's acknowledgment is defective (wrong venue, missing "
                    "elements, expired notary commission). The instrument is valid between "
                    "the parties but does not impart constructive notice.",
        legal_authority="Tex. Civ. Prac. & Rem. Code Sec. 121.001",
        cure_actions=[CurativeAction.CORRECTION_DEED, CurativeAction.RATIFICATION],
        cure_priority=3,
        affects_marketability=True,
        affects_insurability=False,
    ),
    DefectClassification(
        defect_id="DEF-013",
        category=DefectCategory.MISSING_PROBATE,
        severity=DefectSeverity.MAJOR,
        name="Missing Probate / Heirship Proceeding",
        description="A decedent appears in the chain of title but no probate, heirship "
                    "proceeding, or affidavit of heirship has been recorded to establish "
                    "the succession of title.",
        legal_authority="Tex. Estates Code Ch. 201, 256, 257",
        cure_actions=[CurativeAction.AFFIDAVIT_OF_HEIRSHIP, CurativeAction.PROBATE_PROCEEDING],
        cure_priority=2,
        affects_marketability=True,
        affects_insurability=True,
    ),
    DefectClassification(
        defect_id="DEF-014",
        category=DefectCategory.GAP_IN_CHAIN,
        severity=DefectSeverity.MAJOR,
        name="Gap in Chain of Title",
        description="A time period exists where no instrument connects successive owners. "
                    "Unlike a chain break, a gap may involve the same party but with a "
                    "missing connecting instrument (e.g., missing probate between decedent "
                    "and heir).",
        legal_authority="Common law chain of title doctrine",
        cure_actions=[CurativeAction.AFFIDAVIT_OF_FACTS, CurativeAction.QUITCLAIM_DEED,
                      CurativeAction.QUIET_TITLE_ACTION],
        cure_priority=2,
        affects_marketability=True,
        affects_insurability=False,
    ),
    DefectClassification(
        defect_id="DEF-015",
        category=DefectCategory.NAME_VARIANCE,
        severity=DefectSeverity.MINOR,
        name="Name Variance",
        description="A party's name differs between instruments (e.g., 'John A. Smith' vs "
                    "'J.A. Smith' vs 'John Smith'). Minor variances do not break the chain "
                    "but should be documented.",
        legal_authority="Texas Title Standard 14.10",
        cure_actions=[CurativeAction.AFFIDAVIT_OF_IDENTITY],
        cure_priority=4,
        affects_marketability=False,
        affects_insurability=False,
        auto_curable=True,
    ),
    DefectClassification(
        defect_id="DEF-016",
        category=DefectCategory.RECORDING_GAP,
        severity=DefectSeverity.MINOR,
        name="Late or Gap in Recording",
        description="An instrument was recorded substantially after execution, creating "
                    "a period where the instrument was not of record. During the gap, "
                    "subsequent purchasers may have taken without constructive notice.",
        legal_authority="Tex. Property Code Sec. 13.001",
        cure_actions=[CurativeAction.AFFIDAVIT_OF_FACTS],
        cure_priority=4,
        affects_marketability=False,
        affects_insurability=False,
        auto_curable=True,
    ),
    DefectClassification(
        defect_id="DEF-017",
        category=DefectCategory.MISSING_LEGAL,
        severity=DefectSeverity.MINOR,
        name="Missing or Defective Legal Description",
        description="The instrument's legal description is missing, incomplete, or "
                    "ambiguous. The property cannot be positively identified from the "
                    "instrument alone.",
        legal_authority="Tex. Property Code Sec. 5.021; Statute of Frauds",
        cure_actions=[CurativeAction.CORRECTION_DEED],
        cure_priority=3,
        affects_marketability=True,
        affects_insurability=False,
    ),
    DefectClassification(
        defect_id="DEF-018",
        category=DefectCategory.CONSIDERATION_MISSING,
        severity=DefectSeverity.MINOR,
        name="Missing Consideration Recital",
        description="The instrument does not recite consideration. While not fatal to the "
                    "deed's validity, lack of consideration may affect BFP status.",
        legal_authority="Texas Title Standard 2.10",
        cure_actions=[],
        cure_priority=5,
        affects_marketability=False,
        affects_insurability=False,
        auto_curable=True,
        notes=["No curative action required per Title Standard 2.10"],
    ),
    DefectClassification(
        defect_id="DEF-019",
        category=DefectCategory.MINERAL_RESERVATION_AMBIGUITY,
        severity=DefectSeverity.MAJOR,
        name="Ambiguous Mineral Reservation",
        description="A mineral reservation in a deed is ambiguous as to the fraction or "
                    "type of interest reserved. Common ambiguity: 'an undivided 1/2 of "
                    "1/8' could mean 1/16 of minerals or 1/2 of a 1/8 royalty.",
        legal_authority="Texas Title Standard 6.30; Hysaw v. Dawkins (2013)",
        cure_actions=[CurativeAction.STIPULATION_OF_INTEREST, CurativeAction.COURT_ORDER],
        cure_priority=2,
        affects_marketability=True,
        affects_insurability=True,
    ),
    DefectClassification(
        defect_id="DEF-020",
        category=DefectCategory.COMMUNITY_PROPERTY_ISSUE,
        severity=DefectSeverity.MAJOR,
        name="Community Property Issue",
        description="Property acquired during marriage conveyed by one spouse without "
                    "the other's joinder. The non-joining spouse may have a community "
                    "property claim.",
        legal_authority="Tex. Family Code Sec. 3.002; Tex. Const. Art. XVI Sec. 15",
        cure_actions=[CurativeAction.JOINDER, CurativeAction.RATIFICATION,
                      CurativeAction.QUITCLAIM_DEED],
        cure_priority=2,
        affects_marketability=True,
        affects_insurability=True,
    ),
    DefectClassification(
        defect_id="DEF-021",
        category=DefectCategory.ENTITY_AUTHORITY_DEFECT,
        severity=DefectSeverity.MAJOR,
        name="Entity Authority Defect",
        description="A conveyance by a corporation, LLC, partnership, or trust without "
                    "evidence of proper authority. The entity may have been dissolved, "
                    "or the signatory may not have been authorized to act.",
        legal_authority="Texas Title Standards 9.10-9.30; Tex. Bus. Orgs. Code",
        cure_actions=[CurativeAction.RATIFICATION, CurativeAction.COURT_ORDER,
                      CurativeAction.AFFIDAVIT_OF_FACTS],
        cure_priority=2,
        affects_marketability=True,
        affects_insurability=True,
    ),
    DefectClassification(
        defect_id="DEF-022",
        category=DefectCategory.ADVERSE_POSSESSION,
        severity=DefectSeverity.MAJOR,
        name="Potential Adverse Possession Claim",
        description="Evidence suggests a third party may have acquired title through "
                    "adverse possession. Continuous, hostile, visible possession for "
                    "the statutory period may vest title in the possessor.",
        legal_authority="Tex. Civ. Prac. & Rem. Code Secs. 16.025-16.028",
        cure_actions=[CurativeAction.QUIET_TITLE_ACTION, CurativeAction.QUITCLAIM_DEED],
        cure_priority=2,
        affects_marketability=True,
        affects_insurability=True,
    ),
    DefectClassification(
        defect_id="DEF-023",
        category=DefectCategory.TAX_SALE_DEFECT,
        severity=DefectSeverity.MAJOR,
        name="Tax Sale Defect",
        description="A tax sale in the chain of title may have procedural defects "
                    "(insufficient notice, premature sale, redemption rights outstanding).",
        legal_authority="Tex. Tax Code Ch. 33-34",
        cure_actions=[CurativeAction.QUIET_TITLE_ACTION, CurativeAction.TAX_CERTIFICATE],
        cure_priority=2,
        affects_marketability=True,
        affects_insurability=True,
    ),
    DefectClassification(
        defect_id="DEF-024",
        category=DefectCategory.POWER_OF_ATTORNEY_DEFECT,
        severity=DefectSeverity.MAJOR,
        name="Power of Attorney Defect",
        description="A conveyance executed under power of attorney where the POA is "
                    "expired, revoked, not recorded, or does not specifically authorize "
                    "real property transactions.",
        legal_authority="Texas Title Standard 12.10; Tex. Estates Code Ch. 751",
        cure_actions=[CurativeAction.RATIFICATION, CurativeAction.CORRECTION_DEED],
        cure_priority=2,
        affects_marketability=True,
        affects_insurability=True,
    ),
    DefectClassification(
        defect_id="DEF-025",
        category=DefectCategory.UNDIVIDED_INTEREST_ERROR,
        severity=DefectSeverity.MAJOR,
        name="Undivided Interest Does Not Total 100%",
        description="The sum of all undivided interests in a particular estate (mineral, "
                    "surface, royalty) does not equal 100%. Missing interest may indicate "
                    "an unrecorded conveyance or heir.",
        legal_authority="Common law; mathematical consistency requirement",
        cure_actions=[CurativeAction.STIPULATION_OF_INTEREST, CurativeAction.AFFIDAVIT_OF_FACTS,
                      CurativeAction.QUIET_TITLE_ACTION],
        cure_priority=2,
        affects_marketability=True,
        affects_insurability=True,
    ),
]


# ---------------------------------------------------------------------------
# Curative Standards
# ---------------------------------------------------------------------------

CURATIVE_STANDARDS: List[CurativeStandard] = [
    CurativeStandard(
        standard_id="CUR-001",
        action=CurativeAction.CORRECTION_DEED,
        target_defect=DefectCategory.SCRIVENERS_ERROR,
        description="A correction deed corrects a scrivener's error in a prior deed "
                    "such as misspelled name, incorrect legal description, or wrong "
                    "interest fraction. The correction deed must reference the original "
                    "deed and clearly state the correction.",
        requirements=[
            "Original grantor and grantee must execute (or their successors)",
            "Reference to original deed by volume/page or document number",
            "Clear statement of the error and correction",
            "New acknowledgment",
            "Recording in county of property",
        ],
        typical_cost_range="$200-$500",
        typical_time_days=30,
        legal_authority="Tex. Property Code Sec. 5.028",
        recording_required=True,
        notarization_required=True,
        witness_count=0,
        acceptance_criteria=[
            "References original instrument",
            "Identifies error and correction",
            "Executed by original parties or successors",
            "Properly acknowledged",
            "Recorded in county records",
        ],
    ),
    CurativeStandard(
        standard_id="CUR-002",
        action=CurativeAction.AFFIDAVIT_OF_HEIRSHIP,
        target_defect=DefectCategory.MISSING_HEIR,
        description="An affidavit of heirship establishes the heirs of a decedent who "
                    "died intestate. Must be executed by a disinterested party who knew "
                    "the decedent and the family. After recording for 5 years, it becomes "
                    "prima facie evidence of the facts stated.",
        requirements=[
            "Affiant must be disinterested (not an heir or beneficiary)",
            "Affiant must have personal knowledge of decedent's family",
            "Statement of decedent's marital history",
            "List of all children (including deceased children and their issue)",
            "Statement regarding existence or non-existence of will",
            "Two disinterested witnesses in addition to affiant",
            "Acknowledgment before notary",
        ],
        typical_cost_range="$500-$2,000",
        typical_time_days=45,
        legal_authority="Tex. Estates Code Sec. 203.001-203.002",
        recording_required=True,
        notarization_required=True,
        witness_count=2,
        acceptance_criteria=[
            "Disinterested affiant",
            "Complete family history",
            "All heirs identified",
            "Two additional witnesses",
            "Properly acknowledged",
            "Filed of record for 5+ years (for prima facie status)",
        ],
    ),
    CurativeStandard(
        standard_id="CUR-003",
        action=CurativeAction.AFFIDAVIT_OF_IDENTITY,
        target_defect=DefectCategory.NAME_VARIANCE,
        description="An affidavit of identity confirms that a person known by different "
                    "names in the chain of title is the same individual. Typically used "
                    "for maiden name/married name variances, misspellings, or use of "
                    "initials versus full names.",
        requirements=[
            "Executed by the person whose identity is in question (if living)",
            "Or by a person with knowledge of the identity",
            "States all name variations",
            "Identifies relevant instruments",
            "Acknowledgment",
        ],
        typical_cost_range="$100-$300",
        typical_time_days=14,
        legal_authority="Common law; Texas Title Standard 14.10",
        recording_required=True,
        notarization_required=True,
        witness_count=0,
        acceptance_criteria=[
            "All name variations listed",
            "Connection to relevant instruments",
            "Properly acknowledged",
            "Recorded in county records",
        ],
    ),
    CurativeStandard(
        standard_id="CUR-004",
        action=CurativeAction.RELEASE_OF_LIEN,
        target_defect=DefectCategory.UNRELEASED_MORTGAGE,
        description="A release of lien removes an existing lien from the property records. "
                    "Must be executed by the lienholder or their successor. For expired "
                    "liens, an affidavit showing the lien is barred by limitations may "
                    "substitute.",
        requirements=[
            "Executed by lienholder or successor",
            "Reference to original lien instrument",
            "Legal description of property",
            "Statement that lien is satisfied or released",
            "Acknowledgment",
        ],
        typical_cost_range="$100-$500",
        typical_time_days=30,
        legal_authority="Tex. Property Code Sec. 12.014",
        recording_required=True,
        notarization_required=True,
        witness_count=0,
        acceptance_criteria=[
            "Executed by proper party",
            "References original lien",
            "Contains legal description",
            "Properly acknowledged",
            "Recorded in county records",
        ],
    ),
    CurativeStandard(
        standard_id="CUR-005",
        action=CurativeAction.QUIET_TITLE_ACTION,
        target_defect=DefectCategory.CHAIN_BREAK,
        description="A judicial proceeding to establish title to real property by requiring "
                    "all adverse claimants to come forward and establish their claims or be "
                    "forever barred. This is the most comprehensive curative action and is "
                    "used for serious defects that cannot be cured by affidavit or deed.",
        requirements=[
            "File suit in district court of county where property is located",
            "Join all known adverse claimants as defendants",
            "Publish citation for unknown claimants",
            "Prove title by preponderance of evidence",
            "Obtain judgment quieting title",
        ],
        typical_cost_range="$5,000-$25,000",
        typical_time_days=180,
        legal_authority="Tex. Civ. Prac. & Rem. Code Sec. 37.001 (Declaratory Judgments)",
        recording_required=True,
        notarization_required=False,
        witness_count=0,
        acceptance_criteria=[
            "Final judgment from court of competent jurisdiction",
            "All adverse claimants joined or defaulted",
            "Certified copy of judgment recorded in county records",
        ],
    ),
    CurativeStandard(
        standard_id="CUR-006",
        action=CurativeAction.RATIFICATION,
        target_defect=DefectCategory.DEFECTIVE_ACKNOWLEDGMENT,
        description="A ratification confirms a prior instrument that had a defect in "
                    "execution (defective acknowledgment, missing signature, etc.). "
                    "The ratifying party confirms the prior conveyance and cures the "
                    "execution defect.",
        requirements=[
            "Executed by the party whose signature was missing or defective",
            "Reference to the original instrument",
            "Statement ratifying the prior conveyance",
            "Proper acknowledgment",
        ],
        typical_cost_range="$200-$500",
        typical_time_days=30,
        legal_authority="Common law ratification doctrine",
        recording_required=True,
        notarization_required=True,
        witness_count=0,
        acceptance_criteria=[
            "Executed by proper party",
            "References original instrument",
            "Contains ratification language",
            "Properly acknowledged",
            "Recorded in county records",
        ],
    ),
    CurativeStandard(
        standard_id="CUR-007",
        action=CurativeAction.PROBATE_PROCEEDING,
        target_defect=DefectCategory.MISSING_PROBATE,
        description="A probate proceeding establishes the validity of a will or the "
                    "identity of heirs for an intestate decedent. Must be filed in the "
                    "county of the decedent's domicile. Texas allows probate as muniment "
                    "of title for simple estates.",
        requirements=[
            "Application for probate filed in county court",
            "Original will (if testate) or proof of death (if intestate)",
            "Citation to all interested parties",
            "Proof of heirship (if intestate)",
            "Court order admitting will or determining heirship",
        ],
        typical_cost_range="$2,000-$10,000",
        typical_time_days=120,
        legal_authority="Tex. Estates Code Ch. 256-257",
        recording_required=True,
        notarization_required=False,
        witness_count=0,
        acceptance_criteria=[
            "Court order from county with jurisdiction",
            "All heirs/beneficiaries identified",
            "Order recorded in county of property location",
        ],
    ),
    CurativeStandard(
        standard_id="CUR-008",
        action=CurativeAction.STIPULATION_OF_INTEREST,
        target_defect=DefectCategory.MINERAL_RESERVATION_AMBIGUITY,
        description="A stipulation of interest is an agreement among all interest owners "
                    "confirming their respective interests. Used to resolve ambiguities "
                    "in fractional mineral or royalty conveyances.",
        requirements=[
            "Executed by all parties claiming an interest",
            "Clear statement of each party's interest fraction",
            "Reference to original instruments creating ambiguity",
            "Acknowledgment by all parties",
        ],
        typical_cost_range="$500-$3,000",
        typical_time_days=60,
        legal_authority="Common law agreement; binding on signatories",
        recording_required=True,
        notarization_required=True,
        witness_count=0,
        acceptance_criteria=[
            "All interest owners are signatories",
            "Interests clearly stated and total 100%",
            "References ambiguous instruments",
            "Properly acknowledged by all parties",
            "Recorded in county records",
        ],
    ),
    CurativeStandard(
        standard_id="CUR-009",
        action=CurativeAction.TAX_CERTIFICATE,
        target_defect=DefectCategory.TAX_DELINQUENCY,
        description="A tax certificate from the county tax assessor-collector showing "
                    "all taxes are current. Required to clear tax delinquency defects "
                    "and to confirm no outstanding tax liens.",
        requirements=[
            "Request from county tax assessor-collector",
            "Payment of all delinquent taxes, penalties, and interest",
            "Obtain certificate showing no outstanding taxes",
        ],
        typical_cost_range="$25-$200",
        typical_time_days=14,
        legal_authority="Tex. Tax Code Sec. 31.08",
        recording_required=False,
        notarization_required=False,
        witness_count=0,
        acceptance_criteria=[
            "Certificate from county tax office",
            "Shows all taxes paid through current year",
            "No outstanding liens",
        ],
    ),
    CurativeStandard(
        standard_id="CUR-010",
        action=CurativeAction.AFFIDAVIT_OF_NON_PRODUCTION,
        target_defect=DefectCategory.GAP_IN_CHAIN,
        description="An affidavit of non-production is used to establish that an oil and "
                    "gas lease has terminated due to cessation of production and no "
                    "operations are being conducted. This clears the lease from the "
                    "chain of title.",
        requirements=[
            "Executed by the mineral owner or their agent",
            "Statement that no production exists",
            "Statement that no drilling operations are being conducted",
            "Legal description of property",
            "Reference to the lease being cleared",
        ],
        typical_cost_range="$200-$500",
        typical_time_days=14,
        legal_authority="Common law; lease termination doctrine",
        recording_required=True,
        notarization_required=True,
        witness_count=0,
        acceptance_criteria=[
            "Factual statement of non-production",
            "References specific lease",
            "Contains legal description",
            "Properly acknowledged",
            "Recorded in county records",
        ],
    ),
]


# ---------------------------------------------------------------------------
# Doctrine Cache
# ---------------------------------------------------------------------------

class TitleDoctrineCache:
    """
    In-memory cache for title examination doctrines, standards,
    defect classifications, and curative standards.

    Provides fast lookup by category, severity, and defect type.
    Includes deterministic hashing for integrity verification.
    """

    def __init__(self) -> None:
        self._title_standards: Dict[str, TexasTitleStandard] = {}
        self._defect_classifications: Dict[str, DefectClassification] = {}
        self._curative_standards: Dict[str, CurativeStandard] = {}
        self._recording_rules: Dict[str, RecordingActRule] = {}
        self._initialized: bool = False
        self._doctrine_hash: str = ""

    def initialize(self) -> None:
        """Load all doctrines into cache."""
        logger.info("Initializing title doctrine cache")

        for std in TEXAS_TITLE_STANDARDS:
            self._title_standards[std.standard_number] = std

        for defect in DEFECT_CLASSIFICATIONS:
            self._defect_classifications[defect.defect_id] = defect

        for curative in CURATIVE_STANDARDS:
            self._curative_standards[curative.standard_id] = curative

        self._load_recording_rules()
        self._compute_doctrine_hash()
        self._initialized = True

        logger.info(
            f"Doctrine cache initialized: {len(self._title_standards)} standards, "
            f"{len(self._defect_classifications)} defect classes, "
            f"{len(self._curative_standards)} curative standards, "
            f"{len(self._recording_rules)} recording rules"
        )

    def _load_recording_rules(self) -> None:
        """Load recording act rules for supported jurisdictions."""
        self._recording_rules["TX"] = RecordingActRule(
            jurisdiction="TX",
            act_type=RecordingActType.RACE_NOTICE,
            statute_citation="Tex. Property Code Sec. 13.001",
            description="Texas is a race-notice jurisdiction. A subsequent purchaser for "
                        "valuable consideration without notice who records first prevails "
                        "over a prior unrecorded conveyance.",
            bfp_requirements=[
                "Paid valuable consideration",
                "Without actual or constructive notice of prior interest",
                "Recorded before prior instrument was recorded",
            ],
            shelter_rule_applies=True,
            after_acquired_title=True,
            wild_deed_void=True,
            constructive_notice_from_recording=True,
            priority_rules=[
                "First in time, first in right (absent BFP protection)",
                "Recorded instrument gives constructive notice",
                "Wild deed does not give constructive notice",
                "Quitclaim grantee cannot be BFP",
                "Lis pendens gives constructive notice of pending suit",
                "Tax lien superior to all except prior federal tax lien",
            ],
        )

        self._recording_rules["NM"] = RecordingActRule(
            jurisdiction="NM",
            act_type=RecordingActType.RACE_NOTICE,
            statute_citation="NMSA 1978 Sec. 14-9-3",
            description="New Mexico is a race-notice jurisdiction similar to Texas.",
            bfp_requirements=[
                "Paid valuable consideration",
                "Without notice of prior interest",
                "Recorded first",
            ],
            shelter_rule_applies=True,
            after_acquired_title=True,
            wild_deed_void=True,
            constructive_notice_from_recording=True,
            priority_rules=[
                "First to record without notice prevails",
                "Constructive notice from recording",
            ],
        )

        self._recording_rules["OK"] = RecordingActRule(
            jurisdiction="OK",
            act_type=RecordingActType.RACE_NOTICE,
            statute_citation="16 O.S. Sec. 15",
            description="Oklahoma is a race-notice jurisdiction.",
            bfp_requirements=[
                "Paid valuable consideration",
                "Without notice",
                "Recorded first",
            ],
            shelter_rule_applies=True,
            after_acquired_title=True,
            wild_deed_void=True,
            constructive_notice_from_recording=True,
            priority_rules=[
                "Race-notice priority system",
                "Constructive notice from recording",
            ],
        )

    def _compute_doctrine_hash(self) -> None:
        """Compute deterministic hash of all doctrine content."""
        hasher = hashlib.sha256()

        for key in sorted(self._title_standards.keys()):
            std = self._title_standards[key]
            hasher.update(json.dumps(std.to_dict(), sort_keys=True).encode())

        for key in sorted(self._defect_classifications.keys()):
            defect = self._defect_classifications[key]
            hasher.update(json.dumps(defect.to_dict(), sort_keys=True).encode())

        for key in sorted(self._curative_standards.keys()):
            curative = self._curative_standards[key]
            hasher.update(json.dumps(curative.to_dict(), sort_keys=True).encode())

        for key in sorted(self._recording_rules.keys()):
            rule = self._recording_rules[key]
            hasher.update(json.dumps(rule.to_dict(), sort_keys=True).encode())

        self._doctrine_hash = hasher.hexdigest()

    @property
    def doctrine_hash(self) -> str:
        """Return the deterministic hash of all doctrine content."""
        return self._doctrine_hash

    def get_title_standard(self, standard_number: str) -> Optional[TexasTitleStandard]:
        """Look up a title standard by number."""
        return self._title_standards.get(standard_number)

    def get_standards_for_category(self, category: str) -> List[TexasTitleStandard]:
        """Get all standards for a category (e.g., 'minerals', 'recording')."""
        return [
            s for s in self._title_standards.values()
            if s.category == category
        ]

    def get_standards_for_defect(self, defect_category: DefectCategory) -> List[TexasTitleStandard]:
        """Get all standards that address a specific defect category."""
        return [
            s for s in self._title_standards.values()
            if s.matches_defect(defect_category)
        ]

    def get_defect_classification(self, defect_id: str) -> Optional[DefectClassification]:
        """Look up a defect classification by ID."""
        return self._defect_classifications.get(defect_id)

    def get_defects_by_severity(self, severity: DefectSeverity) -> List[DefectClassification]:
        """Get all defect classifications with a specific severity."""
        return [
            d for d in self._defect_classifications.values()
            if d.severity == severity
        ]

    def get_defects_by_category(self, category: DefectCategory) -> List[DefectClassification]:
        """Get all defect classifications in a category."""
        return [
            d for d in self._defect_classifications.values()
            if d.category == category
        ]

    def get_critical_defects(self) -> List[DefectClassification]:
        """Get all critical defect classifications."""
        return self.get_defects_by_severity(DefectSeverity.CRITICAL)

    def get_curative_standard(self, standard_id: str) -> Optional[CurativeStandard]:
        """Look up a curative standard by ID."""
        return self._curative_standards.get(standard_id)

    def get_curative_for_defect(self, defect_category: DefectCategory) -> List[CurativeStandard]:
        """Get all curative standards that address a specific defect."""
        return [
            c for c in self._curative_standards.values()
            if c.target_defect == defect_category
        ]

    def get_recording_rule(self, state: str) -> Optional[RecordingActRule]:
        """Get the recording act rule for a state."""
        return self._recording_rules.get(state.upper())

    def classify_defect(
        self,
        category: DefectCategory,
    ) -> Optional[DefectClassification]:
        """Find the defect classification for a given category."""
        for defect in self._defect_classifications.values():
            if defect.category == category:
                return defect
        return None

    def get_cure_path(
        self,
        defect_category: DefectCategory,
    ) -> List[Tuple[DefectClassification, List[CurativeStandard]]]:
        """
        Get the full cure path for a defect category.
        Returns the defect classification paired with applicable curative standards.
        """
        results: List[Tuple[DefectClassification, List[CurativeStandard]]] = []
        defects = self.get_defects_by_category(defect_category)

        for defect in defects:
            curatives = self.get_curative_for_defect(defect.category)
            results.append((defect, curatives))

        return results

    def is_marketable_title(
        self,
        defects: List[DefectCategory],
    ) -> Tuple[bool, List[str]]:
        """
        Determine if title is marketable given a list of defect categories.
        Returns (is_marketable, list of blocking defect descriptions).
        """
        blocking: List[str] = []

        for defect_cat in defects:
            classification = self.classify_defect(defect_cat)
            if classification and classification.affects_marketability:
                blocking.append(f"{classification.name}: {classification.description[:100]}")

        return (len(blocking) == 0, blocking)

    def is_insurable_title(
        self,
        defects: List[DefectCategory],
    ) -> Tuple[bool, List[str]]:
        """
        Determine if title is insurable given a list of defect categories.
        Returns (is_insurable, list of blocking defect descriptions).
        """
        blocking: List[str] = []

        for defect_cat in defects:
            classification = self.classify_defect(defect_cat)
            if classification and classification.affects_insurability:
                blocking.append(f"{classification.name}: {classification.description[:100]}")

        return (len(blocking) == 0, blocking)

    def determine_title_quality(
        self,
        defects: List[DefectCategory],
    ) -> TitleType:
        """
        Determine the overall title quality based on detected defects.
        """
        if not defects:
            return TitleType.GOOD_AND_INDEFEASIBLE

        marketable, _ = self.is_marketable_title(defects)
        insurable, _ = self.is_insurable_title(defects)

        if not insurable and not marketable:
            has_critical = any(
                self.classify_defect(d) and self.classify_defect(d).is_critical()
                for d in defects
            )
            if has_critical:
                return TitleType.DEFECTIVE
            return TitleType.UNMARKETABLE

        if not marketable and insurable:
            return TitleType.INSURABLE

        if marketable and not insurable:
            return TitleType.DOUBTFUL

        return TitleType.MARKETABLE

    def export_all(self) -> Dict[str, Any]:
        """Export all doctrines as a dictionary."""
        return {
            "title_standards": {k: v.to_dict() for k, v in self._title_standards.items()},
            "defect_classifications": {k: v.to_dict() for k, v in self._defect_classifications.items()},
            "curative_standards": {k: v.to_dict() for k, v in self._curative_standards.items()},
            "recording_rules": {k: v.to_dict() for k, v in self._recording_rules.items()},
            "doctrine_hash": self._doctrine_hash,
            "total_standards": len(self._title_standards),
            "total_defect_classes": len(self._defect_classifications),
            "total_curative_standards": len(self._curative_standards),
            "total_recording_rules": len(self._recording_rules),
        }

    def health_check(self) -> Dict[str, Any]:
        """Return health status of the doctrine cache."""
        return {
            "initialized": self._initialized,
            "title_standards_count": len(self._title_standards),
            "defect_classifications_count": len(self._defect_classifications),
            "curative_standards_count": len(self._curative_standards),
            "recording_rules_count": len(self._recording_rules),
            "doctrine_hash": self._doctrine_hash[:16] + "...",
            "status": "healthy" if self._initialized else "not_initialized",
        }
