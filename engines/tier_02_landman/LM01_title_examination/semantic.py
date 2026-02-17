"""
LM01 Title Examination Engine - Semantic Dictionary
====================================================

Comprehensive semantic dictionary for title examination terminology.

Covers:
- Instrument types and their legal significance
- Legal description formats (metes & bounds, lot/block, section/township/range)
- Conveyance language patterns and granting clauses
- Reservation and exception language
- Grantor/grantee terminology
- Mineral and royalty interest terms
- Oil and gas lease terminology
- Recording and filing terms
- Probate and succession terms
- Encumbrance and lien terms
- Party type classifications
- Name normalization rules

Author: ECHO OMEGA PRIME Build System
Engine: LM01 Title Examination
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

from loguru import logger


# ---------------------------------------------------------------------------
# Term Categories
# ---------------------------------------------------------------------------

class TermCategory(str, Enum):
    """Categories of title examination terms."""
    INSTRUMENT = "instrument"
    LEGAL_DESCRIPTION = "legal_description"
    CONVEYANCE = "conveyance"
    RESERVATION = "reservation"
    EXCEPTION = "exception"
    INTEREST = "interest"
    PARTY = "party"
    RECORDING = "recording"
    PROBATE = "probate"
    ENCUMBRANCE = "encumbrance"
    OIL_GAS = "oil_gas"
    CURATIVE = "curative"
    GENERAL = "general"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class SemanticTerm:
    """A single semantic term with definition, synonyms, and context."""
    term_id: str
    term: str
    category: TermCategory
    definition: str
    synonyms: List[str] = field(default_factory=list)
    related_terms: List[str] = field(default_factory=list)
    legal_authority: Optional[str] = None
    usage_context: Optional[str] = None
    abbreviations: List[str] = field(default_factory=list)
    regex_pattern: Optional[str] = None

    def matches(self, text: str) -> bool:
        """Check if text matches this term or any synonym/abbreviation."""
        text_lower = text.lower().strip()
        if self.term.lower() == text_lower:
            return True
        for syn in self.synonyms:
            if syn.lower() == text_lower:
                return True
        for abbr in self.abbreviations:
            if abbr.lower() == text_lower:
                return True
        if self.regex_pattern:
            if re.search(self.regex_pattern, text, re.IGNORECASE):
                return True
        return False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "term_id": self.term_id,
            "term": self.term,
            "category": self.category.value,
            "definition": self.definition,
            "synonyms": list(self.synonyms),
            "related_terms": list(self.related_terms),
            "legal_authority": self.legal_authority,
            "usage_context": self.usage_context,
            "abbreviations": list(self.abbreviations),
            "regex_pattern": self.regex_pattern,
        }


@dataclass
class InstrumentTerms:
    """Semantic terms for instrument types."""

    WARRANTY_DEED = SemanticTerm(
        term_id="INS-001", term="Warranty Deed", category=TermCategory.INSTRUMENT,
        definition="A deed conveying fee simple title with full covenants of warranty: "
                   "seisin, right to convey, against encumbrances, quiet enjoyment, "
                   "warranty, and further assurance. The grantor warrants title against "
                   "all claims, including those arising before the grantor's ownership.",
        synonyms=["General Warranty Deed", "Full Warranty Deed", "WD"],
        related_terms=["Special Warranty Deed", "Quitclaim Deed", "Grant Deed"],
        legal_authority="Tex. Property Code Sec. 5.023",
        abbreviations=["WD", "GWD"],
    )
    SPECIAL_WARRANTY_DEED = SemanticTerm(
        term_id="INS-002", term="Special Warranty Deed", category=TermCategory.INSTRUMENT,
        definition="A deed conveying fee simple title with limited covenants of warranty. "
                   "The grantor warrants only against claims arising during the grantor's "
                   "period of ownership ('by, through, or under grantor'). Does not "
                   "warrant against prior defects.",
        synonyms=["Limited Warranty Deed", "Deed with Limited Warranty", "SWD"],
        related_terms=["Warranty Deed", "Quitclaim Deed"],
        abbreviations=["SWD"],
    )
    QUITCLAIM_DEED = SemanticTerm(
        term_id="INS-003", term="Quitclaim Deed", category=TermCategory.INSTRUMENT,
        definition="A deed conveying whatever interest the grantor may have without any "
                   "warranties of title. Does not convey after-acquired title. Grantee "
                   "cannot be a bona fide purchaser. Often used for curative purposes.",
        synonyms=["Quit Claim Deed", "QCD", "Release Deed"],
        related_terms=["Warranty Deed", "Disclaimer Deed"],
        abbreviations=["QCD"],
    )
    MINERAL_DEED = SemanticTerm(
        term_id="INS-004", term="Mineral Deed", category=TermCategory.INSTRUMENT,
        definition="A deed conveying mineral interests (or a fraction thereof) separate "
                   "from the surface estate. Severs the mineral estate from the surface. "
                   "Includes the right to explore, develop, produce, bonus, delay rentals, "
                   "and royalties unless specifically limited.",
        synonyms=["Mineral Conveyance", "Mineral Grant", "MD"],
        related_terms=["Royalty Deed", "Mineral Reservation"],
        abbreviations=["MD"],
    )
    ROYALTY_DEED = SemanticTerm(
        term_id="INS-005", term="Royalty Deed", category=TermCategory.INSTRUMENT,
        definition="A deed conveying a royalty interest without executive rights (right "
                   "to lease). The grantee receives a share of production or proceeds "
                   "but has no right to explore, develop, or lease the minerals. Creates "
                   "a non-participating royalty interest (NPRI).",
        synonyms=["Royalty Conveyance", "NPRI Deed", "Royalty Grant", "RD"],
        related_terms=["Mineral Deed", "NPRI", "Overriding Royalty"],
        abbreviations=["RD"],
    )
    OIL_GAS_LEASE = SemanticTerm(
        term_id="INS-006", term="Oil and Gas Lease", category=TermCategory.INSTRUMENT,
        definition="A grant of the exclusive right to explore for and produce oil, gas, "
                   "and other minerals from specified land for a primary term and as long "
                   "thereafter as production continues. Creates a leasehold estate (working "
                   "interest) in the lessee and a royalty interest in the lessor.",
        synonyms=["OGL", "Oil Gas and Mineral Lease", "Petroleum Lease", "Mineral Lease"],
        related_terms=["Paid-Up Lease", "Top Lease", "Assignment of OGL"],
        legal_authority="Tex. Nat. Res. Code Sec. 91.001",
        abbreviations=["OGL", "O&G Lease"],
    )
    ASSIGNMENT = SemanticTerm(
        term_id="INS-007", term="Assignment", category=TermCategory.INSTRUMENT,
        definition="Transfer of an existing interest (typically a leasehold interest) "
                   "from the assignor to the assignee. Unlike a deed which creates a "
                   "new interest, an assignment transfers an existing one.",
        synonyms=["ASGN", "Transfer", "Assignment of Interest"],
        related_terms=["Partial Assignment", "Assignment of OGL", "Assignment of ORRI"],
        abbreviations=["ASGN"],
    )
    DEED_OF_TRUST = SemanticTerm(
        term_id="INS-008", term="Deed of Trust", category=TermCategory.INSTRUMENT,
        definition="A security instrument in which the borrower (trustor) conveys legal "
                   "title to a trustee to hold as security for a debt owed to the "
                   "beneficiary (lender). Texas uses deeds of trust rather than mortgages "
                   "for non-judicial foreclosure.",
        synonyms=["DOT", "Trust Deed", "Security Deed"],
        related_terms=["Mortgage", "Release of Lien", "Foreclosure"],
        abbreviations=["DOT", "D/T"],
    )
    AFFIDAVIT_OF_HEIRSHIP = SemanticTerm(
        term_id="INS-009", term="Affidavit of Heirship", category=TermCategory.INSTRUMENT,
        definition="A sworn statement identifying the heirs of a decedent who died "
                   "intestate. Must be made by a disinterested witness. After being of "
                   "record for 5 years, it becomes prima facie evidence of the facts stated.",
        synonyms=["Heirship Affidavit", "AofH"],
        related_terms=["Probate", "Descent and Distribution", "Will"],
        legal_authority="Tex. Estates Code Sec. 203.001",
        abbreviations=["AofH"],
    )
    CORRECTION_DEED = SemanticTerm(
        term_id="INS-010", term="Correction Deed", category=TermCategory.INSTRUMENT,
        definition="A deed that corrects an error in a previously recorded deed. "
                   "Common corrections include name misspellings, legal description "
                   "errors, and incorrect interest fractions. Must reference the "
                   "original instrument.",
        synonyms=["Corrective Deed", "Deed of Correction", "Scrivener's Affidavit"],
        related_terms=["Ratification", "Reformation"],
        abbreviations=["CD"],
    )
    RELEASE = SemanticTerm(
        term_id="INS-011", term="Release", category=TermCategory.INSTRUMENT,
        definition="An instrument releasing a prior claim, lien, lease, or interest. "
                   "A release of lease terminates the leasehold estate. A release of "
                   "lien removes the lien encumbrance from the property.",
        synonyms=["Release of Lien", "Release of Lease", "Satisfaction", "Discharge"],
        related_terms=["Partial Release", "Subordination"],
        abbreviations=["REL"],
    )
    POOLING_AGREEMENT = SemanticTerm(
        term_id="INS-012", term="Pooling Agreement", category=TermCategory.INSTRUMENT,
        definition="An agreement combining mineral interests from multiple tracts into "
                   "a single drilling or spacing unit. Production from any part of the "
                   "pooled unit maintains all leases within the unit. May be voluntary "
                   "or compulsory (by RRC order).",
        synonyms=["Pooling Declaration", "Pooling Designation", "Unit Agreement"],
        related_terms=["Unit Designation", "Spacing Unit", "Cross-Conveyance"],
        abbreviations=["PA"],
    )
    DIVISION_ORDER = SemanticTerm(
        term_id="INS-013", term="Division Order", category=TermCategory.INSTRUMENT,
        definition="A contract between a royalty or interest owner and the purchaser "
                   "of production that sets forth the owner's fractional interest and "
                   "authorizes the purchaser to make payment. Not a conveyance of "
                   "interest; merely a payment directive.",
        synonyms=["DO", "Division Order Title Opinion", "DOTO"],
        related_terms=["Revenue Interest", "Net Revenue Interest"],
        legal_authority="Tex. Nat. Res. Code Sec. 91.402",
        abbreviations=["DO", "DOTO"],
    )
    POWER_OF_ATTORNEY = SemanticTerm(
        term_id="INS-014", term="Power of Attorney", category=TermCategory.INSTRUMENT,
        definition="An instrument authorizing one person (the agent or attorney-in-fact) "
                   "to act on behalf of another (the principal). Must specifically "
                   "authorize real property transactions to be effective for title "
                   "purposes. A durable POA survives incapacity.",
        synonyms=["POA", "Attorney-in-Fact", "Durable Power of Attorney"],
        related_terms=["Agency", "Principal", "Agent"],
        legal_authority="Tex. Estates Code Ch. 751",
        abbreviations=["POA", "DPOA"],
    )
    MEMORANDUM_OF_LEASE = SemanticTerm(
        term_id="INS-015", term="Memorandum of Lease", category=TermCategory.INSTRUMENT,
        definition="A short-form document recorded to give constructive notice of an "
                   "oil and gas lease without recording the full lease. Contains the "
                   "essential terms: parties, legal description, primary term, and "
                   "recording information.",
        synonyms=["Memo of Lease", "Short Form Lease", "Notice of Lease"],
        related_terms=["Oil and Gas Lease", "Recording"],
        abbreviations=["MOL"],
    )

    @classmethod
    def all_terms(cls) -> List[SemanticTerm]:
        """Return all instrument terms."""
        return [
            getattr(cls, name) for name in dir(cls)
            if isinstance(getattr(cls, name), SemanticTerm)
        ]


@dataclass
class LegalDescriptionTerms:
    """Semantic terms for legal descriptions."""

    METES_AND_BOUNDS = SemanticTerm(
        term_id="LD-001", term="Metes and Bounds", category=TermCategory.LEGAL_DESCRIPTION,
        definition="A system of describing land by measuring distances and directions "
                   "from a point of beginning. Uses courses (compass bearings) and "
                   "distances to trace the boundary of a parcel. Common in Texas for "
                   "original Spanish/Mexican grants.",
        synonyms=["M&B", "Courses and Distances"],
        related_terms=["Point of Beginning", "Monument", "Bearing"],
        regex_pattern=r"(?:beginning|commence|thence|bearing)\s+(?:at|from|N|S|E|W)",
    )
    LOT_AND_BLOCK = SemanticTerm(
        term_id="LD-002", term="Lot and Block", category=TermCategory.LEGAL_DESCRIPTION,
        definition="A system of describing land by reference to a recorded plat or "
                   "subdivision map. The property is identified by lot number, block "
                   "number, and the name of the subdivision as shown on the plat.",
        synonyms=["Lot/Block", "Subdivision Plat"],
        related_terms=["Plat", "Subdivision", "Addition"],
        regex_pattern=r"[Ll]ot\s+\d+.*[Bb]lock\s+\d+",
    )
    SECTION_TOWNSHIP_RANGE = SemanticTerm(
        term_id="LD-003", term="Section, Township, Range", category=TermCategory.LEGAL_DESCRIPTION,
        definition="The Public Land Survey System (PLSS) method of describing land. "
                   "Land is divided into townships (6 miles square), which are divided "
                   "into 36 sections of 640 acres each. Not commonly used in Texas "
                   "(which was never public domain) but found in some western Texas surveys.",
        synonyms=["STR", "PLSS", "Government Survey"],
        related_terms=["Quarter Section", "Principal Meridian", "Base Line"],
        regex_pattern=r"[Ss]ection\s+\d+.*[Tt]ownship\s+\d+.*[Rr]ange\s+\d+",
    )
    ABSTRACT_AND_SURVEY = SemanticTerm(
        term_id="LD-004", term="Abstract and Survey", category=TermCategory.LEGAL_DESCRIPTION,
        definition="The Texas system of describing land by reference to the original "
                   "land grant survey. Each survey has an abstract number assigned by "
                   "the General Land Office. The abstract number uniquely identifies "
                   "the survey within the county.",
        synonyms=["Abstract/Survey", "Texas Abstract", "GLO Survey"],
        related_terms=["Survey Name", "Abstract Number", "Block"],
        regex_pattern=r"[Aa]bstract\s+(?:No\.?\s*)?(?:A-)?\d+",
    )
    SECTION_AND_BLOCK = SemanticTerm(
        term_id="LD-005", term="Section and Block", category=TermCategory.LEGAL_DESCRIPTION,
        definition="Common Texas description format referencing the section number and "
                   "block number of an original railroad survey grant. Many West Texas "
                   "surveys are organized by section and block within a named survey "
                   "(e.g., Section 270, Block 13, H&GN Ry. Co. Survey).",
        synonyms=["Sec/Blk", "Section-Block"],
        related_terms=["Abstract and Survey", "Railroad Survey"],
        regex_pattern=r"[Ss]ection\s+\d+.*[Bb]lock\s+\d+",
    )
    QUARTER_CALL = SemanticTerm(
        term_id="LD-006", term="Quarter Call", category=TermCategory.LEGAL_DESCRIPTION,
        definition="A subdivision of a section into quarters (NW/4, NE/4, SW/4, SE/4) "
                   "or smaller aliquot parts (NW/4 of NE/4). Each quarter section is "
                   "160 acres. Commonly used in PLSS states and some Texas surveys.",
        synonyms=["Quarter Section", "Aliquot Part"],
        related_terms=["Section", "Half Section"],
        regex_pattern=r"(?:N|S)(?:W|E)/[24]",
    )
    ACRES = SemanticTerm(
        term_id="LD-007", term="Acres", category=TermCategory.LEGAL_DESCRIPTION,
        definition="Unit of land measurement. One acre equals 43,560 square feet. "
                   "Gross acres is the total acreage of a tract. Net acres accounts "
                   "for proportionate interest (e.g., owning 50% of 100 gross acres "
                   "= 50 net acres). Net mineral acres (NMA) is the standard oil "
                   "and gas measurement.",
        synonyms=["Ac", "Acreage", "Net Mineral Acres"],
        related_terms=["Gross Acres", "Net Acres", "NMA"],
        abbreviations=["Ac", "NMA", "GMA"],
    )
    SURVEY_NAME = SemanticTerm(
        term_id="LD-008", term="Survey Name", category=TermCategory.LEGAL_DESCRIPTION,
        definition="The name of the original land grant survey in Texas. Usually named "
                   "for the railroad company, land grant recipient, or surveyor. "
                   "Examples: H&GN Ry. Co., T&P Ry. Co., University Lands.",
        synonyms=["Original Grantee", "Patentee"],
        related_terms=["Abstract Number", "Block", "Section"],
    )
    POINT_OF_BEGINNING = SemanticTerm(
        term_id="LD-009", term="Point of Beginning", category=TermCategory.LEGAL_DESCRIPTION,
        definition="The starting point of a metes and bounds description. All courses "
                   "and distances are measured from this point. The description must "
                   "return to the point of beginning to close the boundary.",
        synonyms=["POB", "Beginning Point", "Place of Beginning"],
        related_terms=["Metes and Bounds", "Monument", "Closing"],
        abbreviations=["POB"],
    )
    MONUMENT = SemanticTerm(
        term_id="LD-010", term="Monument", category=TermCategory.LEGAL_DESCRIPTION,
        definition="A physical landmark (natural or artificial) used to identify a "
                   "boundary point. Natural monuments (rivers, ridges) generally "
                   "control over artificial monuments (stakes, fences), which control "
                   "over courses and distances.",
        synonyms=["Marker", "Boundary Marker", "Iron Pin", "Stake"],
        related_terms=["Point of Beginning", "Metes and Bounds"],
    )

    @classmethod
    def all_terms(cls) -> List[SemanticTerm]:
        """Return all legal description terms."""
        return [
            getattr(cls, name) for name in dir(cls)
            if isinstance(getattr(cls, name), SemanticTerm)
        ]


@dataclass
class ConveyanceLanguage:
    """Semantic patterns for conveyance (granting) language."""

    GRANT_BARGAIN_SELL = SemanticTerm(
        term_id="CVY-001", term="Grant, Bargain, and Sell", category=TermCategory.CONVEYANCE,
        definition="Standard granting clause language in a warranty deed. Implies "
                   "covenants of seisin and against encumbrances in some jurisdictions. "
                   "In Texas, this language with additional warranty clauses creates "
                   "a general warranty deed.",
        synonyms=["Grants, Bargains, Sells and Conveys"],
        regex_pattern=r"grant[s]?,?\s*(?:bargain[s]?,?\s*)?(?:sell[s]?\s*(?:and\s*)?)?convey[s]?",
    )
    CONVEY_AND_WARRANT = SemanticTerm(
        term_id="CVY-002", term="Convey and Warrant", category=TermCategory.CONVEYANCE,
        definition="Granting language that includes a warranty of title. Creates "
                   "a warranty deed in Texas when used with proper warranty clauses.",
        synonyms=["Conveys and Warrants"],
        regex_pattern=r"convey[s]?\s+and\s+warrant[s]?",
    )
    REMISE_RELEASE_QUITCLAIM = SemanticTerm(
        term_id="CVY-003", term="Remise, Release, and Quitclaim", category=TermCategory.CONVEYANCE,
        definition="Standard granting clause language in a quitclaim deed. Conveys "
                   "only whatever interest the grantor may have without warranties.",
        synonyms=["Remises, Releases, and Forever Quitclaims"],
        regex_pattern=r"remise[s]?,?\s*release[s]?,?\s*(?:and\s*)?(?:forever\s+)?quitclaim[s]?",
    )
    GRANT_AND_CONVEY = SemanticTerm(
        term_id="CVY-004", term="Grant and Convey", category=TermCategory.CONVEYANCE,
        definition="Simple granting language. Whether this creates a warranty deed "
                   "depends on the presence of additional warranty covenants.",
        synonyms=["Grants and Conveys", "Does Grant, Sell, and Convey"],
        regex_pattern=r"grant[s]?\s+(?:and\s+)?(?:sell[s]?\s+(?:and\s+)?)?convey[s]?",
    )
    ASSIGN_TRANSFER_SET_OVER = SemanticTerm(
        term_id="CVY-005", term="Assign, Transfer, and Set Over", category=TermCategory.CONVEYANCE,
        definition="Standard assignment language for transferring an existing interest "
                   "(typically a leasehold or contractual interest) from assignor to "
                   "assignee.",
        synonyms=["Assigns, Transfers, and Sets Over"],
        regex_pattern=r"assign[s]?,?\s*transfer[s]?,?\s*(?:and\s+)?set[s]?\s+over",
    )
    SUBJECT_TO = SemanticTerm(
        term_id="CVY-006", term="Subject To", category=TermCategory.CONVEYANCE,
        definition="Language indicating that the conveyance is made subject to existing "
                   "conditions, encumbrances, or reservations. Does not create new "
                   "encumbrances but acknowledges existing ones. The grantee takes "
                   "the property burdened by the stated items.",
        synonyms=["Subject to the Following"],
        regex_pattern=r"subject\s+to",
    )
    TOGETHER_WITH = SemanticTerm(
        term_id="CVY-007", term="Together With", category=TermCategory.CONVEYANCE,
        definition="Language including additional rights or appurtenances with the "
                   "primary conveyance (e.g., 'together with all mineral rights').",
        synonyms=["Including", "Along With", "And Also"],
        regex_pattern=r"together\s+with",
    )
    TO_HAVE_AND_TO_HOLD = SemanticTerm(
        term_id="CVY-008", term="To Have and To Hold", category=TermCategory.CONVEYANCE,
        definition="The habendum clause of a deed, defining the estate granted. "
                   "'To have and to hold...in fee simple' means full ownership. "
                   "The habendum cannot enlarge or diminish the estate granted "
                   "in the granting clause.",
        synonyms=["Habendum Clause", "Habendum"],
        regex_pattern=r"to\s+have\s+and\s+to\s+hold",
    )
    FEE_SIMPLE = SemanticTerm(
        term_id="CVY-009", term="Fee Simple", category=TermCategory.CONVEYANCE,
        definition="The highest form of ownership. Fee simple absolute means complete "
                   "ownership with no conditions. Fee simple determinable or fee simple "
                   "subject to condition subsequent involves limitations that may "
                   "terminate the estate.",
        synonyms=["Fee Simple Absolute", "Fee", "Full Fee"],
        related_terms=["Life Estate", "Remainder", "Reversion"],
        regex_pattern=r"fee\s+simple(?:\s+absolute)?",
    )

    @classmethod
    def all_terms(cls) -> List[SemanticTerm]:
        """Return all conveyance language terms."""
        return [
            getattr(cls, name) for name in dir(cls)
            if isinstance(getattr(cls, name), SemanticTerm)
        ]


@dataclass
class ReservationLanguage:
    """Semantic patterns for reservation and exception language."""

    SAVE_AND_EXCEPT = SemanticTerm(
        term_id="RES-001", term="Save and Except", category=TermCategory.RESERVATION,
        definition="Language creating a reservation or exception in a conveyance. "
                   "The grantor retains (reserves) or excludes (excepts) specified "
                   "interests from the conveyance.",
        synonyms=["Saving and Excepting", "Except and Reserving"],
        regex_pattern=r"sav(?:e|ing)\s+and\s+except(?:ing)?",
    )
    RESERVING_UNTO = SemanticTerm(
        term_id="RES-002", term="Reserving Unto", category=TermCategory.RESERVATION,
        definition="Language by which a grantor creates a new interest in the grantor's "
                   "favor out of the property being conveyed. A reservation creates "
                   "a new interest; an exception withholds an existing interest.",
        synonyms=["Reserving to Grantor", "Grantor Reserves", "There is Reserved"],
        regex_pattern=r"reserv(?:e|es|ing)\s+(?:unto|to)\s+(?:the\s+)?(?:grantor|seller)",
    )
    EXCEPTING_THEREFROM = SemanticTerm(
        term_id="RES-003", term="Excepting Therefrom", category=TermCategory.RESERVATION,
        definition="Language excluding a portion of the property or an existing interest "
                   "from the conveyance. An exception removes something from the grant "
                   "that would otherwise pass.",
        synonyms=["Except Therefrom", "Excepting", "Less and Except"],
        regex_pattern=r"except(?:ing)?\s+(?:therefrom|there\s*from)",
    )
    ALL_MINERALS = SemanticTerm(
        term_id="RES-004", term="All Oil, Gas, and Other Minerals", category=TermCategory.RESERVATION,
        definition="Standard language describing the full mineral estate including all "
                   "subsurface hydrocarbons and minerals. Whether 'other minerals' "
                   "includes specific substances (coal, uranium, limestone) depends "
                   "on the surface destruction test in some jurisdictions.",
        synonyms=["All Minerals", "Oil Gas and Minerals", "All Oil and Gas"],
        regex_pattern=r"all\s+(?:of\s+the\s+)?(?:oil,?\s*gas,?\s*(?:and\s+)?)?(?:other\s+)?minerals?",
    )
    UNDIVIDED_INTEREST = SemanticTerm(
        term_id="RES-005", term="Undivided Interest", category=TermCategory.RESERVATION,
        definition="A fractional ownership interest in the whole property, not a "
                   "physical division. An undivided 1/2 interest means the owner "
                   "has a right to 50% of the whole, not a specific half of the "
                   "physical land.",
        synonyms=["Undivided Fractional Interest", "UDI"],
        regex_pattern=r"undivided\s+(?:\d+/\d+\s+)?interest",
    )
    NON_PARTICIPATING = SemanticTerm(
        term_id="RES-006", term="Non-Participating", category=TermCategory.RESERVATION,
        definition="A mineral or royalty interest that does not participate in bonus, "
                   "delay rentals, or lease negotiations. A non-participating royalty "
                   "interest (NPRI) receives only its share of production royalties.",
        synonyms=["NPRI", "Non-Participating Royalty Interest", "NP"],
        related_terms=["Royalty Interest", "Executive Right"],
        regex_pattern=r"non[- ]?participating",
    )
    EXECUTIVE_RIGHT = SemanticTerm(
        term_id="RES-007", term="Executive Right", category=TermCategory.RESERVATION,
        definition="The right to lease minerals. The executive right is one of the "
                   "incidents of mineral ownership and can be severed from the mineral "
                   "fee. The holder of the executive right owes a duty of utmost good "
                   "faith to non-executive mineral owners.",
        synonyms=["Leasing Right", "Executive Interest"],
        related_terms=["Mineral Fee", "NPRI", "Non-Participating"],
        legal_authority="Lesley v. Veterans Land Board, 352 S.W.3d 479 (Tex. 2011)",
    )
    SURFACE_ONLY = SemanticTerm(
        term_id="RES-008", term="Surface Only", category=TermCategory.RESERVATION,
        definition="A conveyance of surface rights only, with minerals reserved. "
                   "The mineral estate has been previously severed or is being "
                   "reserved in this conveyance.",
        synonyms=["Surface Estate Only", "Surface Rights Only"],
        regex_pattern=r"surface\s+(?:rights?\s+)?only",
    )

    @classmethod
    def all_terms(cls) -> List[SemanticTerm]:
        """Return all reservation language terms."""
        return [
            getattr(cls, name) for name in dir(cls)
            if isinstance(getattr(cls, name), SemanticTerm)
        ]


# ---------------------------------------------------------------------------
# Name Normalization
# ---------------------------------------------------------------------------

NAME_PREFIXES: Set[str] = {
    "mr", "mrs", "ms", "miss", "dr", "rev", "hon", "prof",
    "jr", "sr", "ii", "iii", "iv", "v",
}

NAME_SUFFIXES: Set[str] = {
    "jr", "sr", "ii", "iii", "iv", "v", "md", "phd", "esq",
    "dds", "dvm", "do", "pa", "np",
}

ENTITY_INDICATORS: Set[str] = {
    "llc", "l.l.c.", "inc", "inc.", "corp", "corp.", "corporation",
    "company", "co", "co.", "ltd", "ltd.", "limited", "lp", "l.p.",
    "llp", "l.l.p.", "partnership", "trust", "estate", "foundation",
    "association", "assoc", "assoc.",
}

COMMON_MISSPELLING_MAP: Dict[str, str] = {
    "willams": "williams",
    "willaims": "williams",
    "jonhson": "johnson",
    "johsnon": "johnson",
    "smithe": "smith",
    "browne": "brown",
    "thomspon": "thompson",
    "campbel": "campbell",
    "mitchel": "mitchell",
    "andersom": "anderson",
    "wilsn": "wilson",
    "rodrguez": "rodriguez",
    "gonzles": "gonzalez",
    "hernandz": "hernandez",
    "mcwillaims": "mcwilliams",
}


def normalize_party_name(name: str) -> str:
    """
    Normalize a party name for consistent matching.

    Rules:
    - Strip leading/trailing whitespace
    - Convert to uppercase
    - Remove prefixes (Mr., Mrs., Dr., etc.)
    - Standardize suffixes (Jr., Sr., II, III, etc.)
    - Remove extra whitespace
    - Remove punctuation except hyphens
    - Apply common misspelling corrections
    """
    if not name:
        return ""

    normalized = name.strip().upper()

    normalized = re.sub(r"[,.]", " ", normalized)
    normalized = re.sub(r"\s+", " ", normalized).strip()

    parts = normalized.split()
    cleaned_parts: List[str] = []
    suffix_parts: List[str] = []

    for part in parts:
        part_lower = part.lower().rstrip(".")
        if part_lower in NAME_PREFIXES and not cleaned_parts:
            continue
        if part_lower in NAME_SUFFIXES:
            suffix_parts.append(part)
            continue
        cleaned_parts.append(part)

    result = " ".join(cleaned_parts)
    if suffix_parts:
        result += " " + " ".join(suffix_parts)

    for misspelling, correction in COMMON_MISSPELLING_MAP.items():
        result = re.sub(
            rf"\b{re.escape(misspelling.upper())}\b",
            correction.upper(),
            result,
        )

    return result.strip()


def is_entity_name(name: str) -> bool:
    """Check if a name appears to be a business entity (not a person)."""
    name_lower = name.lower().strip()
    for indicator in ENTITY_INDICATORS:
        if indicator in name_lower.split():
            return True
        if name_lower.endswith(f" {indicator}"):
            return True
        if name_lower.endswith(f", {indicator}"):
            return True
    return False


def extract_name_components(name: str) -> Dict[str, Optional[str]]:
    """
    Extract first, middle, last, and suffix from a name string.
    Handles both "LAST, FIRST MIDDLE" and "FIRST MIDDLE LAST" formats.
    """
    normalized = normalize_party_name(name)

    if is_entity_name(name):
        return {
            "entity_name": normalized,
            "first": None,
            "middle": None,
            "last": None,
            "suffix": None,
            "is_entity": True,
        }

    suffix: Optional[str] = None
    parts = normalized.split()
    remaining: List[str] = []
    for part in parts:
        if part.lower().rstrip(".") in NAME_SUFFIXES:
            suffix = part
        else:
            remaining.append(part)

    if not remaining:
        return {
            "entity_name": None,
            "first": None,
            "middle": None,
            "last": None,
            "suffix": suffix,
            "is_entity": False,
        }

    original_stripped = name.strip()
    if "," in original_stripped:
        comma_parts = original_stripped.split(",", 1)
        last_name = normalize_party_name(comma_parts[0])
        rest = normalize_party_name(comma_parts[1]) if len(comma_parts) > 1 else ""
        rest_parts = [p for p in rest.split() if p.lower().rstrip(".") not in NAME_SUFFIXES]

        return {
            "entity_name": None,
            "first": rest_parts[0] if rest_parts else None,
            "middle": " ".join(rest_parts[1:]) if len(rest_parts) > 1 else None,
            "last": last_name,
            "suffix": suffix,
            "is_entity": False,
        }

    if len(remaining) == 1:
        return {"entity_name": None, "first": None, "middle": None,
                "last": remaining[0], "suffix": suffix, "is_entity": False}
    elif len(remaining) == 2:
        return {"entity_name": None, "first": remaining[0], "middle": None,
                "last": remaining[1], "suffix": suffix, "is_entity": False}
    else:
        return {"entity_name": None, "first": remaining[0],
                "middle": " ".join(remaining[1:-1]),
                "last": remaining[-1], "suffix": suffix, "is_entity": False}


def name_similarity_score(name1: str, name2: str) -> float:
    """
    Compute a similarity score between two names (0.0 to 1.0).
    Uses component matching: last name exact match is weighted heavily,
    first name initial match, and Levenshtein-inspired char comparison.
    """
    norm1 = normalize_party_name(name1)
    norm2 = normalize_party_name(name2)

    if norm1 == norm2:
        return 1.0

    if not norm1 or not norm2:
        return 0.0

    comp1 = extract_name_components(name1)
    comp2 = extract_name_components(name2)

    if comp1.get("is_entity") or comp2.get("is_entity"):
        return _entity_similarity(norm1, norm2)

    score = 0.0

    last1 = (comp1.get("last") or "").upper()
    last2 = (comp2.get("last") or "").upper()
    if last1 and last2:
        if last1 == last2:
            score += 0.50
        elif _char_similarity(last1, last2) > 0.85:
            score += 0.40
        else:
            return _char_similarity(norm1, norm2) * 0.5

    first1 = (comp1.get("first") or "").upper()
    first2 = (comp2.get("first") or "").upper()
    if first1 and first2:
        if first1 == first2:
            score += 0.30
        elif first1[0] == first2[0] and (len(first1) == 1 or len(first2) == 1):
            score += 0.20
        elif _char_similarity(first1, first2) > 0.80:
            score += 0.25
    elif first1 or first2:
        score += 0.0
    else:
        score += 0.15

    mid1 = (comp1.get("middle") or "").upper()
    mid2 = (comp2.get("middle") or "").upper()
    if mid1 and mid2:
        if mid1 == mid2:
            score += 0.15
        elif mid1[0] == mid2[0]:
            score += 0.10
    elif not mid1 and not mid2:
        score += 0.05

    suf1 = (comp1.get("suffix") or "").upper()
    suf2 = (comp2.get("suffix") or "").upper()
    if suf1 == suf2:
        score += 0.05

    return min(score, 1.0)


def _char_similarity(s1: str, s2: str) -> float:
    """Simple character overlap similarity."""
    if not s1 or not s2:
        return 0.0
    set1 = set(s1.upper())
    set2 = set(s2.upper())
    intersection = set1 & set2
    union = set1 | set2
    if not union:
        return 0.0
    jaccard = len(intersection) / len(union)
    len_ratio = min(len(s1), len(s2)) / max(len(s1), len(s2))
    return (jaccard + len_ratio) / 2.0


def _entity_similarity(name1: str, name2: str) -> float:
    """Entity name similarity using word overlap."""
    words1 = set(name1.upper().split()) - {w.upper() for w in ENTITY_INDICATORS}
    words2 = set(name2.upper().split()) - {w.upper() for w in ENTITY_INDICATORS}
    if not words1 or not words2:
        return 0.0
    intersection = words1 & words2
    union = words1 | words2
    return len(intersection) / len(union)


# ---------------------------------------------------------------------------
# Legal Description Parsing
# ---------------------------------------------------------------------------

def parse_legal_description(text: str) -> Dict[str, Any]:
    """
    Parse a legal description string into structured components.

    Supports:
    - Section/Block/Survey (Texas style)
    - Abstract number
    - Lot/Block/Subdivision
    - Township/Range/Section (PLSS)
    - Acreage extraction
    """
    result: Dict[str, Any] = {
        "format": "unknown",
        "section": None,
        "block": None,
        "survey_name": None,
        "abstract_number": None,
        "lot": None,
        "subdivision": None,
        "township": None,
        "range": None,
        "quarter": None,
        "acres": None,
        "county": None,
        "state": None,
        "raw_text": text,
    }

    section_match = re.search(
        r"[Ss]ection\s+(\d+[A-Za-z]?)",
        text,
    )
    if section_match:
        result["section"] = section_match.group(1)
        result["format"] = "section_block"

    block_match = re.search(
        r"[Bb]lock\s+(\d+[A-Za-z]?(?:-\d+)?)",
        text,
    )
    if block_match:
        result["block"] = block_match.group(1)

    abstract_match = re.search(
        r"[Aa](?:bstract)?\s*[-#]?\s*(\d+)",
        text,
    )
    if abstract_match:
        result["abstract_number"] = abstract_match.group(1)
        result["format"] = "abstract_survey"

    survey_patterns = [
        r"(H\s*&\s*GN\s*Ry\.?\s*Co\.?)\s*[Ss]urvey",
        r"(T\s*&\s*P\s*Ry\.?\s*Co\.?)\s*[Ss]urvey",
        r"(GC\s*&\s*SF\s*Ry\.?\s*Co\.?)\s*[Ss]urvey",
        r"(\w[\w\s.&]+?)\s+[Ss]urvey",
    ]
    for pattern in survey_patterns:
        survey_match = re.search(pattern, text)
        if survey_match:
            result["survey_name"] = survey_match.group(1).strip()
            break

    lot_match = re.search(r"[Ll]ots?\s+(\d+(?:\s*[-&,]\s*\d+)*)", text)
    if lot_match:
        result["lot"] = lot_match.group(1)
        result["format"] = "lot_block"

    twp_match = re.search(r"[Tt](?:ownship)?\s*(\d+[NS]?)", text)
    rng_match = re.search(r"[Rr](?:ange)?\s*(\d+[EW]?)", text)
    if twp_match and rng_match:
        result["township"] = twp_match.group(1)
        result["range"] = rng_match.group(1)
        result["format"] = "plss"

    quarter_match = re.search(r"([NSEW]{1,2}/\d+(?:\s+of\s+[NSEW]{1,2}/\d+)*)", text)
    if quarter_match:
        result["quarter"] = quarter_match.group(1)

    acres_match = re.search(r"(\d+(?:\.\d+)?)\s*acres?", text, re.IGNORECASE)
    if acres_match:
        result["acres"] = float(acres_match.group(1))

    county_match = re.search(r"(\w+)\s+[Cc]ounty", text)
    if county_match:
        result["county"] = county_match.group(1).upper()

    state_match = re.search(r"[Cc]ounty,?\s*(\w+)", text)
    if state_match:
        state_text = state_match.group(1).upper()
        state_map = {"TEXAS": "TX", "NEW MEXICO": "NM", "OKLAHOMA": "OK"}
        result["state"] = state_map.get(state_text, state_text)

    return result


# ---------------------------------------------------------------------------
# Title Semantic Dictionary (Main Class)
# ---------------------------------------------------------------------------

class TitleSemanticDictionary:
    """
    Central semantic dictionary for title examination.
    Provides term lookup, name normalization, legal description parsing,
    and instrument language pattern matching.
    """

    def __init__(self) -> None:
        self._terms: Dict[str, SemanticTerm] = {}
        self._by_category: Dict[TermCategory, List[SemanticTerm]] = {}
        self._initialized: bool = False
        self._dictionary_hash: str = ""

    def initialize(self) -> None:
        """Load all semantic terms into the dictionary."""
        logger.info("Initializing title semantic dictionary")

        all_term_sources = [
            InstrumentTerms.all_terms(),
            LegalDescriptionTerms.all_terms(),
            ConveyanceLanguage.all_terms(),
            ReservationLanguage.all_terms(),
        ]

        for term_list in all_term_sources:
            for term in term_list:
                self._terms[term.term_id] = term
                if term.category not in self._by_category:
                    self._by_category[term.category] = []
                self._by_category[term.category].append(term)

        self._compute_hash()
        self._initialized = True
        logger.info(f"Semantic dictionary initialized: {len(self._terms)} terms across "
                     f"{len(self._by_category)} categories")

    def _compute_hash(self) -> None:
        """Compute deterministic hash of dictionary content."""
        hasher = hashlib.sha256()
        for key in sorted(self._terms.keys()):
            hasher.update(json.dumps(self._terms[key].to_dict(), sort_keys=True).encode())
        self._dictionary_hash = hasher.hexdigest()

    @property
    def dictionary_hash(self) -> str:
        return self._dictionary_hash

    def lookup(self, text: str) -> Optional[SemanticTerm]:
        """Look up a term by exact or fuzzy match."""
        for term in self._terms.values():
            if term.matches(text):
                return term
        return None

    def lookup_by_id(self, term_id: str) -> Optional[SemanticTerm]:
        """Look up a term by its ID."""
        return self._terms.get(term_id)

    def search(self, query: str) -> List[SemanticTerm]:
        """Search terms by keyword in term name, definition, and synonyms."""
        query_lower = query.lower()
        results: List[SemanticTerm] = []

        for term in self._terms.values():
            if query_lower in term.term.lower():
                results.append(term)
                continue
            if query_lower in term.definition.lower():
                results.append(term)
                continue
            for syn in term.synonyms:
                if query_lower in syn.lower():
                    results.append(term)
                    break

        return results

    def get_category(self, category: TermCategory) -> List[SemanticTerm]:
        """Get all terms in a category."""
        return self._by_category.get(category, [])

    def identify_instrument_type(self, text: str) -> Optional[SemanticTerm]:
        """Identify the instrument type from document text."""
        instrument_terms = self.get_category(TermCategory.INSTRUMENT)
        for term in instrument_terms:
            if term.matches(text):
                return term
        return None

    def identify_conveyance_type(self, text: str) -> Optional[SemanticTerm]:
        """Identify the type of conveyance from granting language."""
        conveyance_terms = self.get_category(TermCategory.CONVEYANCE)
        for term in conveyance_terms:
            if term.regex_pattern and re.search(term.regex_pattern, text, re.IGNORECASE):
                return term
        return None

    def identify_reservations(self, text: str) -> List[SemanticTerm]:
        """Identify all reservation/exception patterns in text."""
        results: List[SemanticTerm] = []
        reservation_terms = self.get_category(TermCategory.RESERVATION)
        for term in reservation_terms:
            if term.regex_pattern and re.search(term.regex_pattern, text, re.IGNORECASE):
                results.append(term)
            elif term.matches(text):
                results.append(term)
        return results

    def parse_legal_description(self, text: str) -> Dict[str, Any]:
        """Parse a legal description string."""
        return parse_legal_description(text)

    def normalize_name(self, name: str) -> str:
        """Normalize a party name."""
        return normalize_party_name(name)

    def name_similarity(self, name1: str, name2: str) -> float:
        """Compute similarity between two names."""
        return name_similarity_score(name1, name2)

    def is_entity(self, name: str) -> bool:
        """Check if a name is a business entity."""
        return is_entity_name(name)

    def extract_name_parts(self, name: str) -> Dict[str, Optional[str]]:
        """Extract name components."""
        return extract_name_components(name)

    def health_check(self) -> Dict[str, Any]:
        """Return health status of the semantic dictionary."""
        return {
            "initialized": self._initialized,
            "total_terms": len(self._terms),
            "categories": {cat.value: len(terms) for cat, terms in self._by_category.items()},
            "dictionary_hash": self._dictionary_hash[:16] + "...",
            "status": "healthy" if self._initialized else "not_initialized",
        }

    def export_all(self) -> Dict[str, Any]:
        """Export entire dictionary."""
        return {
            "terms": {k: v.to_dict() for k, v in self._terms.items()},
            "categories": {
                cat.value: [t.term_id for t in terms]
                for cat, terms in self._by_category.items()
            },
            "dictionary_hash": self._dictionary_hash,
            "total_terms": len(self._terms),
        }
