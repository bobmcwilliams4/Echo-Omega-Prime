"""
LMIE Semantic Normalization — Landman domain term normalization.

Provides deterministic term normalization, abbreviation expansion,
and legal description parsing for landman queries.

Commander: Bobby Don McWilliams II | Authority: 11.0 SOVEREIGN
"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Tuple

from loguru import logger


# ═══════════════════════════════════════════════════════════════════
# ABBREVIATION EXPANSIONS
# ═══════════════════════════════════════════════════════════════════

ABBREVIATIONS: Dict[str, str] = {
    # General landman
    "nri": "net revenue interest",
    "wi": "working interest",
    "orri": "overriding royalty interest",
    "nma": "net mineral acre",
    "gma": "gross mineral acre",
    "nsa": "net surface acre",
    "doi": "division of interest",
    "do": "division order",
    "joa": "joint operating agreement",
    "psa": "purchase and sale agreement",
    "afe": "authority for expenditure",
    "afd": "authority for expenditure",
    "hbp": "held by production",
    "pbq": "paying quantities",
    "ogml": "oil gas and mineral lease",
    "row": "right of way",
    "swd": "saltwater disposal well",
    "apd": "application for permit to drill",
    "npri": "non-participating royalty interest",
    "npmi": "non-participating mineral interest",

    # Regulatory
    "rrc": "railroad commission of texas",
    "tceq": "texas commission on environmental quality",
    "blm": "bureau of land management",
    "glo": "texas general land office",
    "bia": "bureau of indian affairs",
    "nepa": "national environmental policy act",
    "ferc": "federal energy regulatory commission",
    "phmsa": "pipeline and hazardous materials safety administration",
    "epa": "environmental protection agency",
    "osha": "occupational safety and health administration",

    # Legal
    "tpc": "texas property code",
    "tnrc": "texas natural resources code",
    "twc": "texas water code",
    "tec": "texas estates code",
    "smcra": "surface mining control and reclamation act",
    "ilca": "indian land consolidation act",
    "imda": "indian mineral development act",
    "imla": "indian mineral leasing act",

    # Geographic/Survey
    "h&gn": "houston and great northern railroad survey",
    "t&p": "texas and pacific railroad survey",
    "sp": "southern pacific railroad survey",
    "gc&sf": "gulf colorado and santa fe railroad survey",
    "blk": "block",
    "sec": "section",
    "twp": "township",
    "rng": "range",
    "abs": "abstract",
    "pmt": "patent",
    "surv": "survey",
    "cert": "certificate",

    # Instrument types
    "wd": "warranty deed",
    "qcd": "quitclaim deed",
    "md": "mineral deed",
    "rod": "release of deed of trust",
    "dot": "deed of trust",
    "aoh": "affidavit of heirship",
    "mot": "muniment of title",
    "cd": "correction deed",
    "mol": "memorandum of lease",
    "rol": "release of oil and gas lease",
}


# ═══════════════════════════════════════════════════════════════════
# LEGAL DESCRIPTION PATTERNS
# ═══════════════════════════════════════════════════════════════════

LEGAL_DESC_PATTERNS = [
    # Section/Block/Survey
    re.compile(
        r"(?:section|sec\.?)\s*(\d+),?\s*(?:block|blk\.?)\s*([\w-]+),?\s*(.+?)(?:survey|surv\.?)",
        re.IGNORECASE,
    ),
    # Abstract number
    re.compile(r"(?:abstract|abs\.?)\s*(?:no\.?\s*)?(\d+)", re.IGNORECASE),
    # Township/Range (federal)
    re.compile(
        r"(?:township|twp\.?)\s*(\d+[NS]),?\s*(?:range|rng\.?)\s*(\d+[EW])",
        re.IGNORECASE,
    ),
    # Lot/Block (platted)
    re.compile(r"(?:lot|lt\.?)\s*(\d+),?\s*(?:block|blk\.?)\s*([\w-]+)", re.IGNORECASE),
]


def parse_legal_description(text: str) -> Optional[Dict[str, str]]:
    """Extract structured legal description from free text."""
    for pattern in LEGAL_DESC_PATTERNS:
        match = pattern.search(text)
        if match:
            groups = match.groups()
            if len(groups) >= 3:
                return {
                    "section": groups[0],
                    "block": groups[1],
                    "survey": groups[2].strip().rstrip(","),
                    "raw": match.group(0),
                }
            elif len(groups) == 2:
                return {"primary": groups[0], "secondary": groups[1], "raw": match.group(0)}
            elif len(groups) == 1:
                return {"abstract": groups[0], "raw": match.group(0)}
    return None


# ═══════════════════════════════════════════════════════════════════
# COUNTY NORMALIZATION
# ═══════════════════════════════════════════════════════════════════

TX_COUNTY_ALIASES: Dict[str, str] = {
    "reeves": "Reeves",
    "ector": "Ector",
    "midland": "Midland",
    "martin": "Martin",
    "howard": "Howard",
    "glasscock": "Glasscock",
    "upton": "Upton",
    "crane": "Crane",
    "ward": "Ward",
    "winkler": "Winkler",
    "loving": "Loving",
    "culberson": "Culberson",
    "pecos": "Pecos",
    "jeff davis": "Jeff Davis",
    "presidio": "Presidio",
    "brewster": "Brewster",
    "terrell": "Terrell",
    "val verde": "Val Verde",
    "crockett": "Crockett",
    "irion": "Irion",
    "reagan": "Reagan",
    "sterling": "Sterling",
    "tom green": "Tom Green",
    "andrews": "Andrews",
    "gaines": "Gaines",
    "dawson": "Dawson",
    "borden": "Borden",
    "scurry": "Scurry",
    "fisher": "Fisher",
    "nolan": "Nolan",
    "mitchell": "Mitchell",
    "lea": "Lea",  # NM Permian
    "eddy": "Eddy",  # NM Permian
    "chaves": "Chaves",  # NM
    "roosevelt": "Roosevelt",  # NM
}


def normalize_county(county: str) -> Optional[str]:
    """Normalize county name to canonical form."""
    return TX_COUNTY_ALIASES.get(county.lower().strip())


# ═══════════════════════════════════════════════════════════════════
# QUERY NORMALIZATION
# ═══════════════════════════════════════════════════════════════════

def expand_abbreviations(text: str) -> str:
    """Expand landman abbreviations in text."""
    words = text.split()
    expanded = []
    for word in words:
        clean = word.lower().strip(".,;:()")
        if clean in ABBREVIATIONS:
            expanded.append(ABBREVIATIONS[clean])
        else:
            expanded.append(word)
    return " ".join(expanded)


def normalize_query(query: str) -> Dict[str, Any]:
    """Full semantic normalization of a landman query."""
    expanded = expand_abbreviations(query)
    legal_desc = parse_legal_description(query)
    county = None
    for alias in TX_COUNTY_ALIASES:
        if alias in query.lower():
            county = normalize_county(alias)
            break

    return {
        "original": query,
        "expanded": expanded,
        "legal_description": legal_desc,
        "county": county,
        "abbreviations_found": [
            w.lower().strip(".,;:()")
            for w in query.split()
            if w.lower().strip(".,;:()") in ABBREVIATIONS
        ],
    }


logger.info(
    "LMIE semantic module loaded: {} abbreviations, {} county aliases",
    len(ABBREVIATIONS),
    len(TX_COUNTY_ALIASES),
)
