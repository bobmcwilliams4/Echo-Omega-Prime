"""
LG03 REGULATORY COMPLIANCE ENGINE - SEMANTIC NORMALIZATION MODULE
Deterministic regulatory terminology normalization and CFR citation parsing.

Provides:
    - Regulatory term normalization (agency names, regulation references)
    - CFR citation parser with full structural decomposition
    - Federal Register citation parser
    - USC citation parser
    - Public Law citation parser
    - Executive Order reference parser
    - Agency abbreviation resolution
    - Industry code normalization (SIC <-> NAICS)
    - Regulation status terminology standardization

Architecture:
    This module is a DETERMINISTIC preprocessing layer.
    It must remain deterministic. No probabilistic models.
    No vector inference. No embeddings. No auto-learning.
    Normalization occurs BEFORE hashing. Never after.

Author: ECHO OMEGA PRIME
Authority: 11.0 SOVEREIGN
Engine: LG03 Regulatory Compliance
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from typing import Any, Dict, FrozenSet, List, Optional, Tuple

from loguru import logger

# ============================================================================
# GOVERNANCE METADATA
# ============================================================================

SEMANTIC_MAP_VERSION: str = "1.0.0"
SEMANTIC_MAP_RELEASE_DATE: str = "2026-02-10"
SEMANTIC_MAP_AUTHOR: str = "ECHO OMEGA PRIME"
_EXPECTED_ENTRY_COUNT: int = 198
_GOVERNANCE_LOCKED: bool = False


# ============================================================================
# CFR CITATION PARSER
# ============================================================================

@dataclass
class CFRCitation:
    """Parsed Code of Federal Regulations citation.

    Examples:
        40 CFR 261.3(a)(2)
        29 CFR Part 1910.1200
        17 CFR 240.10b-5
        26 CFR 1.61-1(a)
    """
    title: int
    part: Optional[int] = None
    section: Optional[str] = None
    subsection: Optional[str] = None
    paragraph: Optional[str] = None
    subparagraph: Optional[str] = None
    raw_text: str = ""
    is_valid: bool = True
    agency_hint: Optional[str] = None

    @property
    def canonical(self) -> str:
        """Produce canonical citation string."""
        parts = [f"{self.title} CFR"]
        if self.part is not None:
            parts.append(f"\u00a7 {self.part}")
        if self.section:
            parts[-1] += f".{self.section}"
        if self.subsection:
            parts[-1] += f"({self.subsection})"
        if self.paragraph:
            parts[-1] += f"({self.paragraph})"
        if self.subparagraph:
            parts[-1] += f"({self.subparagraph})"
        return " ".join(parts)

    @property
    def title_name(self) -> str:
        """Return the name of the CFR title."""
        return CFR_TITLE_NAMES.get(self.title, f"Title {self.title}")

    def to_dict(self) -> Dict[str, Any]:
        """Serialize for API response."""
        return {
            "title": self.title,
            "part": self.part,
            "section": self.section,
            "subsection": self.subsection,
            "paragraph": self.paragraph,
            "subparagraph": self.subparagraph,
            "canonical": self.canonical,
            "title_name": self.title_name,
            "raw_text": self.raw_text,
            "is_valid": self.is_valid,
            "agency_hint": self.agency_hint,
        }


# CFR title numbers to names
CFR_TITLE_NAMES: Dict[int, str] = {
    1: "General Provisions",
    2: "Grants and Agreements",
    3: "The President",
    4: "Accounts",
    5: "Administrative Personnel",
    6: "Domestic Security",
    7: "Agriculture",
    8: "Aliens and Nationality",
    9: "Animals and Animal Products",
    10: "Energy",
    11: "Federal Elections",
    12: "Banks and Banking",
    13: "Business Credit and Assistance",
    14: "Aeronautics and Space",
    15: "Commerce and Foreign Trade",
    16: "Commercial Practices",
    17: "Commodity and Securities Exchanges",
    18: "Conservation of Power and Water Resources",
    19: "Customs Duties",
    20: "Employees Benefits",
    21: "Food and Drugs",
    22: "Foreign Relations",
    23: "Highways",
    24: "Housing and Urban Development",
    25: "Indians",
    26: "Internal Revenue",
    27: "Alcohol, Tobacco Products and Firearms",
    28: "Judicial Administration",
    29: "Labor",
    30: "Mineral Resources",
    31: "Money and Finance: Treasury",
    32: "National Defense",
    33: "Navigation and Navigable Waters",
    34: "Education",
    36: "Parks, Forests, and Public Property",
    37: "Patents, Trademarks, and Copyrights",
    38: "Pensions, Bonuses, and Veterans Relief",
    39: "Postal Service",
    40: "Protection of Environment",
    41: "Public Contracts and Property Management",
    42: "Public Health",
    43: "Public Lands: Interior",
    44: "Emergency Management and Assistance",
    45: "Public Welfare",
    46: "Shipping",
    47: "Telecommunication",
    48: "Federal Acquisition Regulations System",
    49: "Transportation",
    50: "Wildlife and Fisheries",
}

# CFR title to primary agency mapping
CFR_TITLE_TO_AGENCY: Dict[int, str] = {
    7: "USDA",
    10: "NRC/DOE",
    12: "OCC/FDIC/FRB",
    14: "FAA/NASA",
    16: "FTC",
    17: "SEC/CFTC",
    20: "DOL/SSA",
    21: "FDA",
    26: "IRS",
    27: "ATF/TTB",
    29: "DOL/OSHA",
    30: "MSHA/OSMRE",
    33: "USACE/USCG",
    40: "EPA",
    42: "HHS/CMS",
    47: "FCC",
    48: "GSA/DOD",
    49: "DOT/FMCSA/NHTSA",
}


# Pattern for CFR citations: "XX CFR [Part ]YYY.ZZZ(a)(1)(i)"
_CFR_PATTERN = re.compile(
    r"(\d{1,2})\s*(?:C\.?F\.?R\.?|CFR)\s*"
    r"(?:(?:Part|Pt\.?|part)\s*)?"
    r"(?:\xa7\s*)?"
    r"(\d{1,4})"
    r"(?:\.(\d{1,6}[a-zA-Z]?(?:-\d+[a-zA-Z]?)?))"
    r"?"
    r"(?:\(([a-zA-Z0-9]+)\))?"
    r"(?:\(([a-zA-Z0-9]+)\))?"
    r"(?:\(([a-zA-Z0-9]+)\))?",
    re.IGNORECASE,
)


def parse_cfr_citation(text: str) -> List[CFRCitation]:
    """Parse all CFR citations from a text string.

    Handles formats:
        40 CFR 261.3(a)(2)
        29 CFR Part 1910.1200
        17 C.F.R. 240.10b-5
        26 CFR 1.61-1(a)
        40 CFR \u00a7 261.3(a)(2)

    Args:
        text: Input text that may contain CFR citations.

    Returns:
        List of parsed CFRCitation objects.
    """
    citations: List[CFRCitation] = []
    for match in _CFR_PATTERN.finditer(text):
        title = int(match.group(1))
        part_num = int(match.group(2)) if match.group(2) else None
        section = match.group(3) if match.group(3) else None
        subsection = match.group(4) if match.group(4) else None
        paragraph = match.group(5) if match.group(5) else None
        subparagraph = match.group(6) if match.group(6) else None

        is_valid = 1 <= title <= 50
        agency_hint = CFR_TITLE_TO_AGENCY.get(title)

        citation = CFRCitation(
            title=title,
            part=part_num,
            section=section,
            subsection=subsection,
            paragraph=paragraph,
            subparagraph=subparagraph,
            raw_text=match.group(0).strip(),
            is_valid=is_valid,
            agency_hint=agency_hint,
        )
        citations.append(citation)

    return citations


# ============================================================================
# USC CITATION PARSER
# ============================================================================

@dataclass
class USCCitation:
    """Parsed United States Code citation.

    Examples:
        42 U.S.C. 7401
        15 USC 78j(b)
        26 U.S.C. 61(a)
    """
    title: int
    section: str
    subsection: Optional[str] = None
    raw_text: str = ""
    is_valid: bool = True

    @property
    def canonical(self) -> str:
        """Produce canonical citation string."""
        result = f"{self.title} U.S.C. \u00a7 {self.section}"
        if self.subsection:
            result += f"({self.subsection})"
        return result

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "section": self.section,
            "subsection": self.subsection,
            "canonical": self.canonical,
            "raw_text": self.raw_text,
            "is_valid": self.is_valid,
        }


_USC_PATTERN = re.compile(
    r"(\d{1,2})\s*(?:U\.?S\.?C\.?|USC)\s*"
    r"(?:\xa7\s*)?"
    r"(\d{1,6}[a-zA-Z]?(?:-\d+[a-zA-Z]?)?)"
    r"(?:\(([a-zA-Z0-9]+)\))?"
    r"(?:\(([a-zA-Z0-9]+)\))?",
    re.IGNORECASE,
)


def parse_usc_citation(text: str) -> List[USCCitation]:
    """Parse all USC citations from text."""
    citations: List[USCCitation] = []
    for match in _USC_PATTERN.finditer(text):
        title = int(match.group(1))
        section = match.group(2)
        subsection = match.group(3)
        citations.append(USCCitation(
            title=title,
            section=section,
            subsection=subsection,
            raw_text=match.group(0).strip(),
            is_valid=1 <= title <= 54,
        ))
    return citations


# ============================================================================
# FEDERAL REGISTER CITATION PARSER
# ============================================================================

@dataclass
class FederalRegisterCitation:
    """Parsed Federal Register citation.

    Examples:
        88 FR 12345
        89 Fed. Reg. 45678
    """
    volume: int
    page: int
    raw_text: str = ""

    @property
    def canonical(self) -> str:
        return f"{self.volume} FR {self.page}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "volume": self.volume,
            "page": self.page,
            "canonical": self.canonical,
            "raw_text": self.raw_text,
        }


_FR_PATTERN = re.compile(
    r"(\d{2,3})\s*(?:FR|Fed\.?\s*Reg\.?)\s+(\d{3,6})",
    re.IGNORECASE,
)


def parse_fr_citation(text: str) -> List[FederalRegisterCitation]:
    """Parse all Federal Register citations from text."""
    citations: List[FederalRegisterCitation] = []
    for match in _FR_PATTERN.finditer(text):
        citations.append(FederalRegisterCitation(
            volume=int(match.group(1)),
            page=int(match.group(2)),
            raw_text=match.group(0).strip(),
        ))
    return citations


# ============================================================================
# PUBLIC LAW AND EXECUTIVE ORDER PARSERS
# ============================================================================

@dataclass
class PublicLawCitation:
    """Parsed Public Law citation. E.g., Pub. L. 107-204 (Sarbanes-Oxley)."""
    congress: int
    law_number: int
    raw_text: str = ""

    @property
    def canonical(self) -> str:
        return f"Pub. L. {self.congress}-{self.law_number}"

    def to_dict(self) -> Dict[str, Any]:
        return {"congress": self.congress, "law_number": self.law_number,
                "canonical": self.canonical, "raw_text": self.raw_text}


_PUB_LAW_PATTERN = re.compile(
    r"(?:Pub(?:lic)?\.?\s*(?:L(?:aw)?\.?|Law))\s*(\d{2,3})\s*[-\u2013]\s*(\d{1,4})",
    re.IGNORECASE,
)


def parse_public_law(text: str) -> List[PublicLawCitation]:
    """Parse Public Law citations from text."""
    citations: List[PublicLawCitation] = []
    for match in _PUB_LAW_PATTERN.finditer(text):
        citations.append(PublicLawCitation(
            congress=int(match.group(1)),
            law_number=int(match.group(2)),
            raw_text=match.group(0).strip(),
        ))
    return citations


@dataclass
class ExecutiveOrderCitation:
    """Parsed Executive Order reference. E.g., E.O. 13990."""
    number: int
    raw_text: str = ""

    @property
    def canonical(self) -> str:
        return f"E.O. {self.number}"

    def to_dict(self) -> Dict[str, Any]:
        return {"number": self.number, "canonical": self.canonical,
                "raw_text": self.raw_text}


_EO_PATTERN = re.compile(
    r"(?:E\.?O\.?|Executive\s+Order)\s*(?:No\.?\s*)?(\d{4,5})",
    re.IGNORECASE,
)


def parse_executive_order(text: str) -> List[ExecutiveOrderCitation]:
    """Parse Executive Order references from text."""
    citations: List[ExecutiveOrderCitation] = []
    for match in _EO_PATTERN.finditer(text):
        citations.append(ExecutiveOrderCitation(
            number=int(match.group(1)),
            raw_text=match.group(0).strip(),
        ))
    return citations


# ============================================================================
# AGENCY NAME NORMALIZATION
# ============================================================================

AGENCY_ALIASES: Dict[str, str] = {
    # Securities and Exchange Commission
    "sec": "SEC",
    "securities and exchange commission": "SEC",
    "securities & exchange commission": "SEC",
    "s.e.c.": "SEC",
    "s.e.c": "SEC",
    # Environmental Protection Agency
    "epa": "EPA",
    "environmental protection agency": "EPA",
    "e.p.a.": "EPA",
    "e.p.a": "EPA",
    "us epa": "EPA",
    # Occupational Safety and Health Administration
    "osha": "OSHA",
    "occupational safety and health administration": "OSHA",
    "occupational safety": "OSHA",
    "o.s.h.a.": "OSHA",
    # Internal Revenue Service
    "irs": "IRS",
    "internal revenue service": "IRS",
    "i.r.s.": "IRS",
    "i.r.s": "IRS",
    "internal revenue": "IRS",
    # Federal Trade Commission
    "ftc": "FTC",
    "federal trade commission": "FTC",
    "f.t.c.": "FTC",
    # Food and Drug Administration
    "fda": "FDA",
    "food and drug administration": "FDA",
    "f.d.a.": "FDA",
    "food & drug administration": "FDA",
    # Department of Labor
    "dol": "DOL",
    "department of labor": "DOL",
    "dept of labor": "DOL",
    "dept. of labor": "DOL",
    "labor department": "DOL",
    # Department of Justice
    "doj": "DOJ",
    "department of justice": "DOJ",
    "dept of justice": "DOJ",
    "justice department": "DOJ",
    # Consumer Financial Protection Bureau
    "cfpb": "CFPB",
    "consumer financial protection bureau": "CFPB",
    "consumer financial protection": "CFPB",
    # Financial Industry Regulatory Authority
    "finra": "FINRA",
    "financial industry regulatory authority": "FINRA",
    # Office of the Comptroller of the Currency
    "occ": "OCC",
    "comptroller of the currency": "OCC",
    "office of the comptroller": "OCC",
    # Federal Deposit Insurance Corporation
    "fdic": "FDIC",
    "federal deposit insurance": "FDIC",
    "federal deposit insurance corporation": "FDIC",
    # Federal Reserve Board
    "frb": "FRB",
    "federal reserve": "FRB",
    "federal reserve board": "FRB",
    "the fed": "FRB",
    "fed reserve": "FRB",
    # Commodity Futures Trading Commission
    "cftc": "CFTC",
    "commodity futures trading commission": "CFTC",
    # Equal Employment Opportunity Commission
    "eeoc": "EEOC",
    "equal employment opportunity commission": "EEOC",
    "equal employment opportunity": "EEOC",
    # Department of Health and Human Services
    "hhs": "HHS",
    "health and human services": "HHS",
    "department of health and human services": "HHS",
    # Centers for Medicare and Medicaid Services
    "cms": "CMS",
    "centers for medicare and medicaid": "CMS",
    "centers for medicare & medicaid": "CMS",
    "medicare": "CMS",
    # National Highway Traffic Safety Administration
    "nhtsa": "NHTSA",
    "national highway traffic safety": "NHTSA",
    # Federal Aviation Administration
    "faa": "FAA",
    "federal aviation administration": "FAA",
    # Federal Communications Commission
    "fcc": "FCC",
    "federal communications commission": "FCC",
    # Federal Energy Regulatory Commission
    "ferc": "FERC",
    "federal energy regulatory commission": "FERC",
    # Nuclear Regulatory Commission
    "nrc": "NRC",
    "nuclear regulatory commission": "NRC",
    # Bureau of Alcohol, Tobacco, Firearms and Explosives
    "atf": "ATF",
    "alcohol tobacco firearms": "ATF",
    "bureau of alcohol tobacco firearms": "ATF",
    # Drug Enforcement Administration
    "dea": "DEA",
    "drug enforcement administration": "DEA",
    # Customs and Border Protection
    "cbp": "CBP",
    "customs and border protection": "CBP",
    "customs & border protection": "CBP",
    # Financial Crimes Enforcement Network
    "fincen": "FINCEN",
    "financial crimes enforcement network": "FINCEN",
    "financial crimes enforcement": "FINCEN",
    # Office of Foreign Assets Control
    "ofac": "OFAC",
    "office of foreign assets control": "OFAC",
    "foreign assets control": "OFAC",
    # Small Business Administration
    "sba": "SBA",
    "small business administration": "SBA",
    # Pension Benefit Guaranty Corporation
    "pbgc": "PBGC",
    "pension benefit guaranty": "PBGC",
    "pension benefit guaranty corporation": "PBGC",
    # Mine Safety and Health Administration
    "msha": "MSHA",
    "mine safety and health administration": "MSHA",
    "mine safety": "MSHA",
    # Consumer Product Safety Commission
    "cpsc": "CPSC",
    "consumer product safety commission": "CPSC",
    "consumer product safety": "CPSC",
    # Public Company Accounting Oversight Board
    "pcaob": "PCAOB",
    "public company accounting oversight board": "PCAOB",
    # Pipeline and Hazardous Materials Safety Administration
    "phmsa": "PHMSA",
    "pipeline and hazardous materials safety": "PHMSA",
}


def normalize_agency(text: str) -> str:
    """Normalize an agency name or abbreviation to its canonical form.

    Args:
        text: Raw agency name or abbreviation.

    Returns:
        Canonical agency abbreviation (e.g., "SEC", "EPA").
        Returns original text (uppercased) if no match found.
    """
    cleaned = text.strip().lower()
    if cleaned in AGENCY_ALIASES:
        return AGENCY_ALIASES[cleaned]
    return text.strip().upper()


# ============================================================================
# REGULATORY SEMANTIC MAP
# ============================================================================

REGULATORY_SEMANTIC_MAP: Dict[str, str] = {
    # Compliance terminology
    "in compliance": "compliant",
    "out of compliance": "non-compliant",
    "not in compliance": "non-compliant",
    "non compliant": "non-compliant",
    "noncompliant": "non-compliant",
    "noncompliance": "non-compliance",
    "non compliance": "non-compliance",
    # Regulatory action types
    "notice of proposed rulemaking": "NPRM",
    "proposed rulemaking": "NPRM",
    "advance notice of proposed rulemaking": "ANPRM",
    "advance notice": "ANPRM",
    "final rule": "final_rule",
    "interim final rule": "interim_final_rule",
    "direct final rule": "direct_final_rule",
    "emergency rule": "emergency_rule",
    # Enforcement terminology
    "consent decree": "consent_decree",
    "consent order": "consent_order",
    "cease and desist": "cease_and_desist",
    "cease-and-desist": "cease_and_desist",
    "c&d": "cease_and_desist",
    "warning letter": "warning_letter",
    "no-action letter": "no_action_letter",
    "no action letter": "no_action_letter",
    "enforcement action": "enforcement_action",
    "corrective action": "corrective_action",
    "corrective action plan": "corrective_action_plan",
    "cap": "corrective_action_plan",
    "civil monetary penalty": "civil_penalty",
    "civil money penalty": "civil_penalty",
    "cmp": "civil_penalty",
    "administrative penalty": "administrative_penalty",
    # Filing types
    "annual report": "annual_filing",
    "quarterly report": "quarterly_filing",
    "10-k": "annual_filing_sec",
    "10-q": "quarterly_filing_sec",
    "10k": "annual_filing_sec",
    "10q": "quarterly_filing_sec",
    "form 8-k": "current_report_sec",
    "8-k": "current_report_sec",
    "schedule 13d": "beneficial_ownership_filing",
    "13d": "beneficial_ownership_filing",
    # Risk terminology
    "high risk": "high_risk",
    "low risk": "low_risk",
    "medium risk": "medium_risk",
    "moderate risk": "medium_risk",
    "elevated risk": "high_risk",
    "minimal risk": "low_risk",
    "negligible risk": "low_risk",
    "significant risk": "high_risk",
    "material risk": "high_risk",
    # Regulatory status
    "effective date": "effective_date",
    "compliance date": "compliance_deadline",
    "compliance deadline": "compliance_deadline",
    "sunset date": "expiration_date",
    "sunset provision": "sunset_clause",
    "grandfather clause": "grandfathering_provision",
    "grandfathered": "grandfathering_provision",
    "safe harbor": "safe_harbor",
    "safe harbour": "safe_harbor",
    # Preemption
    "federal preemption": "federal_preemption",
    "preempted by federal law": "federal_preemption",
    "preempts state law": "federal_preemption",
    "state preemption": "state_preemption",
    "field preemption": "field_preemption",
    "conflict preemption": "conflict_preemption",
    "express preemption": "express_preemption",
    "implied preemption": "implied_preemption",
    # Industry terms
    "naics code": "naics",
    "naics": "naics",
    "sic code": "sic",
    "sic": "sic",
    "north american industry classification": "naics",
    "standard industrial classification": "sic",
    # Environmental
    "rcra": "RCRA",
    "resource conservation and recovery act": "RCRA",
    "cercla": "CERCLA",
    "superfund": "CERCLA",
    "comprehensive environmental response": "CERCLA",
    "clean air act": "CAA",
    "caa": "CAA",
    "clean water act": "CWA",
    "cwa": "CWA",
    "national environmental policy act": "NEPA",
    "nepa": "NEPA",
    "toxic substances control act": "TSCA",
    "tsca": "TSCA",
    # Financial
    "sarbanes-oxley": "SOX",
    "sarbanes oxley": "SOX",
    "sox": "SOX",
    "sarbox": "SOX",
    "dodd-frank": "DODD_FRANK",
    "dodd frank": "DODD_FRANK",
    "dodd-frank act": "DODD_FRANK",
    "bank secrecy act": "BSA",
    "bsa": "BSA",
    "anti-money laundering": "AML",
    "anti money laundering": "AML",
    "aml": "AML",
    "know your customer": "KYC",
    "kyc": "KYC",
    # Healthcare
    "hipaa": "HIPAA",
    "health insurance portability": "HIPAA",
    "health insurance portability and accountability": "HIPAA",
    "hitech": "HITECH",
    "health information technology": "HITECH",
    "stark law": "STARK",
    "physician self-referral": "STARK",
    "anti-kickback": "AKS",
    "anti-kickback statute": "AKS",
    "false claims act": "FCA",
    "fca": "FCA",
    # Labor/Employment
    "fair labor standards act": "FLSA",
    "flsa": "FLSA",
    "family and medical leave act": "FMLA",
    "fmla": "FMLA",
    "americans with disabilities act": "ADA",
    "ada": "ADA",
    "title vii": "TITLE_VII",
    "title 7": "TITLE_VII",
    "civil rights act": "CRA",
    "age discrimination in employment act": "ADEA",
    "adea": "ADEA",
    "worker adjustment and retraining notification": "WARN",
    "warn act": "WARN",
    # Privacy/Data
    "general data protection regulation": "GDPR",
    "gdpr": "GDPR",
    "california consumer privacy act": "CCPA",
    "ccpa": "CCPA",
    "california privacy rights act": "CPRA",
    "cpra": "CPRA",
    "children's online privacy protection act": "COPPA",
    "coppa": "COPPA",
    "gramm-leach-bliley": "GLBA",
    "gramm leach bliley": "GLBA",
    "glba": "GLBA",
    "ferpa": "FERPA",
    "family educational rights and privacy act": "FERPA",
}


# ============================================================================
# NAICS / SIC CODE MAPPINGS
# ============================================================================

NAICS_TO_SIC_MAP: Dict[str, List[str]] = {
    "11": ["01", "02", "07", "08", "09"],
    "21": ["10", "12", "13", "14"],
    "22": ["49"],
    "23": ["15", "16", "17"],
    "31": ["20", "21", "22", "23"],
    "32": ["24", "25", "26", "27", "28", "29", "30", "31", "32"],
    "33": ["33", "34", "35", "36", "37", "38", "39"],
    "42": ["50", "51"],
    "44": ["52", "53", "55", "56", "57"],
    "45": ["54", "58", "59"],
    "48": ["40", "41", "42", "43", "44", "45", "46", "47"],
    "49": ["40", "41", "42", "43", "44", "45", "46", "47", "49"],
    "51": ["27", "48"],
    "52": ["60", "61", "62", "63", "64", "65", "67"],
    "53": ["65"],
    "54": ["73", "81", "87", "89"],
    "55": ["67"],
    "56": ["73", "76"],
    "61": ["82"],
    "62": ["80"],
    "71": ["78", "79", "84"],
    "72": ["58", "70"],
    "81": ["72", "75", "76", "83", "86", "88"],
    "92": ["91", "92", "93", "94", "95", "96", "97"],
}

NAICS_SECTOR_NAMES: Dict[str, str] = {
    "11": "Agriculture, Forestry, Fishing and Hunting",
    "21": "Mining, Quarrying, and Oil and Gas Extraction",
    "22": "Utilities",
    "23": "Construction",
    "31": "Manufacturing",
    "32": "Manufacturing",
    "33": "Manufacturing",
    "42": "Wholesale Trade",
    "44": "Retail Trade",
    "45": "Retail Trade",
    "48": "Transportation and Warehousing",
    "49": "Transportation and Warehousing",
    "51": "Information",
    "52": "Finance and Insurance",
    "53": "Real Estate and Rental and Leasing",
    "54": "Professional, Scientific, and Technical Services",
    "55": "Management of Companies and Enterprises",
    "56": "Administrative and Support and Waste Management",
    "61": "Educational Services",
    "62": "Health Care and Social Assistance",
    "71": "Arts, Entertainment, and Recreation",
    "72": "Accommodation and Food Services",
    "81": "Other Services (except Public Administration)",
    "92": "Public Administration",
}


def get_naics_sector(code: str) -> Optional[str]:
    """Get NAICS sector name from a NAICS code (2-6 digits)."""
    prefix = code[:2]
    return NAICS_SECTOR_NAMES.get(prefix)


def naics_to_sic(naics_code: str) -> List[str]:
    """Convert NAICS sector code to approximate SIC division codes."""
    prefix = naics_code[:2]
    return NAICS_TO_SIC_MAP.get(prefix, [])


# ============================================================================
# NORMALIZATION RESULT
# ============================================================================

@dataclass
class NormalizationResult:
    """Result of semantic normalization, preserving original for audit."""
    original: str
    normalized: str
    changes_applied: List[Tuple[str, str]]
    cfr_citations: List[CFRCitation]
    usc_citations: List[USCCitation]
    fr_citations: List[FederalRegisterCitation]
    public_law_citations: List[PublicLawCitation]
    executive_orders: List[ExecutiveOrderCitation]
    agencies_detected: List[str]
    determinism_hash: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "original": self.original,
            "normalized": self.normalized,
            "changes_applied": [{"from": f, "to": t} for f, t in self.changes_applied],
            "cfr_citations": [c.to_dict() for c in self.cfr_citations],
            "usc_citations": [c.to_dict() for c in self.usc_citations],
            "fr_citations": [c.to_dict() for c in self.fr_citations],
            "public_law_citations": [c.to_dict() for c in self.public_law_citations],
            "executive_orders": [c.to_dict() for c in self.executive_orders],
            "agencies_detected": self.agencies_detected,
            "determinism_hash": self.determinism_hash,
        }


# ============================================================================
# MAIN NORMALIZATION FUNCTION
# ============================================================================

# Build sorted keys for longest-match-first replacement
_SORTED_SEMANTIC_KEYS: List[str] = sorted(
    REGULATORY_SEMANTIC_MAP.keys(),
    key=len,
    reverse=True,
)


def normalize_semantics(raw_query: str) -> NormalizationResult:
    """Normalize regulatory terminology in a query string.

    Deterministic normalization pipeline:
        1. Lowercase and strip
        2. Apply semantic map (longest match first, word-boundary enforced)
        3. Parse CFR citations
        4. Parse USC citations
        5. Parse Federal Register citations
        6. Parse Public Law citations
        7. Parse Executive Order references
        8. Detect agency names
        9. Compute determinism hash

    Args:
        raw_query: Raw user query text.

    Returns:
        NormalizationResult with all parsed entities and normalized text.
    """
    if not raw_query or not raw_query.strip():
        empty_hash = hashlib.sha256(b"").hexdigest()
        return NormalizationResult(
            original="",
            normalized="",
            changes_applied=[],
            cfr_citations=[],
            usc_citations=[],
            fr_citations=[],
            public_law_citations=[],
            executive_orders=[],
            agencies_detected=[],
            determinism_hash=empty_hash,
        )

    original = raw_query.strip()
    text = original.lower()
    changes: List[Tuple[str, str]] = []

    # Apply semantic map with word-boundary matching, longest first
    for key in _SORTED_SEMANTIC_KEYS:
        pattern = re.compile(r"\b" + re.escape(key) + r"\b", re.IGNORECASE)
        replacement = REGULATORY_SEMANTIC_MAP[key]
        # Check if already normalized (idempotency)
        if replacement.lower() in text and key not in text:
            continue
        new_text = pattern.sub(replacement, text)
        if new_text != text:
            changes.append((key, replacement))
            text = new_text

    # Parse citations from ORIGINAL text (preserve case for citation parsing)
    cfr_citations = parse_cfr_citation(original)
    usc_citations = parse_usc_citation(original)
    fr_citations = parse_fr_citation(original)
    pub_law_citations = parse_public_law(original)
    exec_orders = parse_executive_order(original)

    # Detect agency names from normalized text
    agencies_detected: List[str] = []
    seen_agencies: set = set()
    for alias, canonical in AGENCY_ALIASES.items():
        if canonical not in seen_agencies:
            pattern = re.compile(r"\b" + re.escape(alias) + r"\b", re.IGNORECASE)
            if pattern.search(text):
                agencies_detected.append(canonical)
                seen_agencies.add(canonical)

    # Also detect from CFR title mappings
    for cit in cfr_citations:
        if cit.agency_hint and cit.agency_hint not in seen_agencies:
            agencies_detected.append(cit.agency_hint)
            seen_agencies.add(cit.agency_hint)

    # Compute determinism hash on normalized text
    determinism_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()

    return NormalizationResult(
        original=original,
        normalized=text,
        changes_applied=changes,
        cfr_citations=cfr_citations,
        usc_citations=usc_citations,
        fr_citations=fr_citations,
        public_law_citations=pub_law_citations,
        executive_orders=exec_orders,
        agencies_detected=sorted(agencies_detected),
        determinism_hash=determinism_hash,
    )


# ============================================================================
# INTEGRITY VERIFICATION
# ============================================================================

def verify_semantic_map_integrity() -> Dict[str, Any]:
    """Verify the semantic map has not been tampered with at runtime."""
    actual_count = len(REGULATORY_SEMANTIC_MAP)
    all_keys_lower = all(k == k.lower() for k in REGULATORY_SEMANTIC_MAP.keys())

    content_hash = hashlib.sha256(
        json.dumps(dict(sorted(REGULATORY_SEMANTIC_MAP.items())), sort_keys=True).encode("utf-8")
    ).hexdigest()

    return {
        "version": SEMANTIC_MAP_VERSION,
        "expected_entries": _EXPECTED_ENTRY_COUNT,
        "actual_entries": actual_count,
        "count_match": actual_count == _EXPECTED_ENTRY_COUNT,
        "all_keys_lowercase": all_keys_lower,
        "content_hash": content_hash,
        "governance_locked": _GOVERNANCE_LOCKED,
    }


# Need json for verify function
import json
