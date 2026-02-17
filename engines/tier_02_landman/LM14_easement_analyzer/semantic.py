"""
LM14 Easement Analyzer Engine - Semantic Normalization Module
================================================================
Provides canonical terminology mapping, synonym resolution, abbreviation
expansion, and semantic normalization for easement, right-of-way, surface
use, pipeline, and eminent domain queries in the oil and gas landman context.

Components:
    - SEMANTIC_MAP: Master dictionary mapping canonical terms to synonyms
    - ABBREVIATION_MAP: Abbreviation expansion table
    - INSTRUMENT_TYPE_MAP: Recording instrument classification
    - OPERATOR_ALIAS_MAP: Pipeline operator name normalization
    - normalize_query(): Normalize free-text query for search
    - expand_abbreviations(): Expand known abbreviations in text
    - resolve_synonyms(): Map synonyms back to canonical terms
    - classify_instrument_type(): Classify a document by instrument type
    - extract_easement_terms(): Extract easement-related terms from text

Version: 1.0.0
Engine: LM14 Easement Analyzer
"""

from __future__ import annotations

import re
from collections import defaultdict
from typing import Any, Dict, List, Optional, Set, Tuple

from loguru import logger


# ============================================================================
# SEMANTIC MAP - CANONICAL TERMS TO SYNONYMS
# ============================================================================

SEMANTIC_MAP: Dict[str, List[str]] = {
    # --- Easement Types ---
    "express_easement": [
        "express easement", "granted easement", "deeded easement",
        "written easement", "express grant", "easement deed",
        "easement by grant", "conveyed easement", "easement conveyance",
    ],
    "implied_easement": [
        "implied easement", "easement by implication", "quasi-easement",
        "implied grant", "implied reservation", "easement implied by law",
    ],
    "easement_by_necessity": [
        "easement by necessity", "necessity easement", "landlocked easement",
        "way of necessity", "access by necessity", "strict necessity easement",
        "easement of necessity", "landlocked access",
    ],
    "prescriptive_easement": [
        "prescriptive easement", "adverse use easement", "prescriptive right",
        "easement by prescription", "adverse easement", "prescriptive use",
        "prescriptive access", "long use easement",
    ],
    "easement_appurtenant": [
        "appurtenant easement", "easement appurtenant", "runs with land",
        "running with the land", "appurtenant right", "land-based easement",
        "dominant servient easement",
    ],
    "easement_in_gross": [
        "easement in gross", "personal easement", "commercial easement in gross",
        "in gross easement", "easement to person", "non-appurtenant easement",
        "corporate easement", "utility easement in gross",
    ],
    "conservation_easement": [
        "conservation easement", "conservation restriction", "scenic easement",
        "agricultural easement", "preservation easement", "open space easement",
        "land trust easement", "environmental easement",
    ],
    "flowage_easement": [
        "flowage easement", "drainage easement", "flood easement",
        "water flow easement", "stormwater easement", "runoff easement",
        "discharge easement",
    ],

    # --- Right-of-Way ---
    "right_of_way": [
        "right-of-way", "right of way", "ROW", "R/W", "R.O.W.",
        "row", "r/w", "r.o.w.", "pipeline row", "pipeline right-of-way",
        "pipeline right of way", "easement corridor", "corridor",
    ],
    "pipeline_row": [
        "pipeline right-of-way", "pipeline row", "pipeline easement",
        "pipe right of way", "transmission row", "gathering row",
        "flowline easement", "line easement", "pipeline corridor",
    ],
    "road_easement": [
        "road easement", "access easement", "ingress and egress",
        "ingress/egress", "road right-of-way", "road row",
        "access road", "private road easement", "county road easement",
        "oilfield road", "lease road", "well access road",
    ],
    "utility_easement": [
        "utility easement", "electric easement", "power line easement",
        "telephone easement", "communication easement", "water line easement",
        "sewer easement", "fiber optic easement", "transmission line easement",
        "distribution line easement", "overhead line easement",
    ],
    "railroad_row": [
        "railroad right-of-way", "railroad row", "rail easement",
        "railway right-of-way", "railroad corridor", "rail line easement",
    ],

    # --- Surface Use ---
    "surface_use_agreement": [
        "surface use agreement", "sua", "SUA", "surface agreement",
        "surface lease", "surface access agreement", "surface occupancy",
        "surface damage agreement", "surface compensation agreement",
    ],
    "surface_damage": [
        "surface damage", "surface impact", "surface disturbance",
        "crop damage", "land damage", "grazing damage", "soil compaction",
        "restoration", "reclamation", "surface restoration",
    ],
    "accommodation_doctrine": [
        "accommodation doctrine", "getty oil doctrine", "getty oil v jones",
        "surface accommodation", "mineral accommodation", "due regard",
        "alternative methods", "coexistence doctrine",
    ],
    "dominant_estate": [
        "dominant estate", "dominant tenement", "benefited estate",
        "dominant parcel", "easement beneficiary", "mineral estate dominant",
    ],
    "servient_estate": [
        "servient estate", "servient tenement", "burdened estate",
        "burdened parcel", "subject property", "encumbered estate",
    ],

    # --- Pipeline ---
    "pipeline": [
        "pipeline", "pipe line", "pipe-line", "line", "flowline",
        "flow line", "gathering line", "transmission line", "trunk line",
        "product line", "produced water line", "salt water disposal line",
        "swd line", "injection line",
    ],
    "gathering_line": [
        "gathering line", "gathering system", "gathering pipeline",
        "field gathering", "lease gathering", "low pressure line",
    ],
    "transmission_line": [
        "transmission line", "transmission pipeline", "high pressure line",
        "interstate pipeline", "trunk line", "mainline", "main line",
    ],
    "cathodic_protection": [
        "cathodic protection", "cp", "corrosion protection", "anode",
        "sacrificial anode", "impressed current", "pipeline protection",
    ],
    "horizontal_directional_drill": [
        "horizontal directional drill", "HDD", "hdd", "directional bore",
        "directional drill", "horizontal bore", "trenchless", "bore",
    ],

    # --- Eminent Domain ---
    "eminent_domain": [
        "eminent domain", "condemnation", "condemn", "taking",
        "government taking", "compulsory acquisition", "expropriation",
        "pipeline condemnation", "utility condemnation",
    ],
    "just_compensation": [
        "just compensation", "fair compensation", "compensation",
        "damages", "condemnation award", "taking payment",
        "fair market value", "fmv", "severance damages",
    ],
    "common_carrier": [
        "common carrier", "common carrier pipeline", "carrier",
        "public carrier", "for-hire carrier", "common carrier status",
    ],

    # --- Abandonment ---
    "abandonment": [
        "abandonment", "abandoned easement", "easement abandonment",
        "non-use", "discontinued use", "ceased operations",
        "pipeline abandonment", "abandoned pipeline", "orphan pipeline",
    ],
    "extinguishment": [
        "extinguishment", "termination", "expiration", "release",
        "merger", "cancellation", "surrender", "vacate", "vacated",
        "revocation", "forfeiture",
    ],
    "overburdening": [
        "overburdening", "overburden", "excess use", "misuse",
        "exceed scope", "unauthorized use", "expanded use",
        "additional burden", "surcharge",
    ],

    # --- Legal Description ---
    "metes_and_bounds": [
        "metes and bounds", "metes & bounds", "m&b", "survey description",
        "bearing and distance", "courses and distances",
    ],
    "plss": [
        "PLSS", "plss", "public land survey system", "section township range",
        "quarter section", "aliquot part",
    ],
    "lot_block": [
        "lot and block", "lot/block", "platted", "subdivision",
        "addition", "recorded plat",
    ],

    # --- RRC / Regulatory ---
    "t4_permit": [
        "T-4 permit", "T4 permit", "t-4", "t4", "pipeline permit",
        "rrc pipeline permit", "construction permit",
    ],
    "rrc": [
        "RRC", "rrc", "Railroad Commission", "railroad commission",
        "Texas Railroad Commission", "TRRC",
    ],
    "txdot": [
        "TxDOT", "txdot", "Texas Department of Transportation",
        "texas dot", "highway department", "TXDOT",
    ],
    "phmsa": [
        "PHMSA", "phmsa", "Pipeline and Hazardous Materials Safety Administration",
        "DOT pipeline safety", "federal pipeline safety",
    ],

    # --- Depth and Width ---
    "depth_of_cover": [
        "depth of cover", "cover depth", "burial depth", "depth of burial",
        "minimum depth", "pipe depth", "pipeline depth",
    ],
    "row_width": [
        "ROW width", "right-of-way width", "easement width", "corridor width",
        "permanent width", "construction width", "workspace width",
    ],
    "temporary_workspace": [
        "temporary workspace", "temp workspace", "construction workspace",
        "additional workspace", "extra workspace", "working space",
    ],

    # --- Valuation ---
    "severance_damage": [
        "severance damage", "severance damages", "remainder damage",
        "damage to remainder", "diminution in value", "residual damage",
    ],
    "cost_to_cure": [
        "cost to cure", "cure cost", "mitigation cost", "remediation cost",
        "fix cost", "repair cost",
    ],
    "before_and_after": [
        "before and after", "before-and-after", "before after method",
        "diminution method", "valuation method",
    ],
}


# ============================================================================
# ABBREVIATION MAP
# ============================================================================

ABBREVIATION_MAP: Dict[str, str] = {
    "ROW": "right-of-way",
    "R/W": "right-of-way",
    "R.O.W.": "right-of-way",
    "SUA": "surface use agreement",
    "HDD": "horizontal directional drill",
    "CP": "cathodic protection",
    "FMV": "fair market value",
    "BFP": "bona fide purchaser",
    "PLSS": "public land survey system",
    "M&B": "metes and bounds",
    "RRC": "Railroad Commission of Texas",
    "TRRC": "Texas Railroad Commission",
    "TxDOT": "Texas Department of Transportation",
    "PHMSA": "Pipeline and Hazardous Materials Safety Administration",
    "TNRC": "Texas Natural Resources Code",
    "NRC": "Natural Resources Code",
    "TPC": "Texas Property Code",
    "SWD": "salt water disposal",
    "UIC": "underground injection control",
    "NPDES": "National Pollutant Discharge Elimination System",
    "NESC": "National Electrical Safety Code",
    "CFR": "Code of Federal Regulations",
    "TAC": "Texas Administrative Code",
    "IRC": "Internal Revenue Code",
    "IRS": "Internal Revenue Service",
    "BLM": "Bureau of Land Management",
    "GLO": "Texas General Land Office",
    "DOT": "Department of Transportation",
    "EPA": "Environmental Protection Agency",
    "TCEQ": "Texas Commission on Environmental Quality",
    "NMA": "net mineral acres",
    "WI": "working interest",
    "RI": "royalty interest",
    "ORRI": "overriding royalty interest",
    "NRI": "net revenue interest",
    "OGL": "oil and gas lease",
    "PSA": "purchase and sale agreement",
    "JOA": "joint operating agreement",
    "AFE": "authority for expenditure",
    "DO": "division order",
    "MOD": "memorandum of division order",
    "MOGM": "memorandum of oil and gas lease",
    "OGL": "oil and gas lease",
    "DT": "deed of trust",
    "MML": "mechanic's and materialman's lien",
    "UCC": "Uniform Commercial Code",
    "QCD": "quit claim deed",
    "WD": "warranty deed",
    "SPTWD": "special warranty deed",
    "CD": "correction deed",
    "AMD": "amendment",
    "ASGN": "assignment",
    "CONV": "conveyance",
    "REL": "release",
    "SUBORD": "subordination",
}


# ============================================================================
# INSTRUMENT TYPE MAP
# ============================================================================

INSTRUMENT_TYPE_MAP: Dict[str, Dict[str, Any]] = {
    "easement_grant": {
        "canonical": "Easement Grant",
        "keywords": [
            "grant of easement", "easement grant", "right-of-way grant",
            "row grant", "grant of right-of-way", "pipeline easement",
            "grants unto", "grant and convey an easement",
        ],
        "category": "easement",
    },
    "surface_use_agreement": {
        "canonical": "Surface Use Agreement",
        "keywords": [
            "surface use agreement", "surface agreement", "sua",
            "surface damage agreement", "surface occupancy agreement",
        ],
        "category": "agreement",
    },
    "pipeline_row_agreement": {
        "canonical": "Pipeline Right-of-Way Agreement",
        "keywords": [
            "pipeline right-of-way", "pipeline row", "pipeline easement agreement",
            "right-of-way agreement", "row agreement", "pipe line easement",
        ],
        "category": "easement",
    },
    "road_easement_grant": {
        "canonical": "Road Easement Grant",
        "keywords": [
            "road easement", "access easement", "ingress and egress",
            "road right-of-way", "road row", "private road easement",
        ],
        "category": "easement",
    },
    "utility_easement_grant": {
        "canonical": "Utility Easement Grant",
        "keywords": [
            "utility easement", "electric easement", "power line easement",
            "telephone easement", "water line easement", "sewer easement",
        ],
        "category": "easement",
    },
    "conservation_easement": {
        "canonical": "Conservation Easement",
        "keywords": [
            "conservation easement", "conservation restriction",
            "preservation easement", "scenic easement",
        ],
        "category": "easement",
    },
    "easement_release": {
        "canonical": "Easement Release",
        "keywords": [
            "release of easement", "easement release", "termination of easement",
            "abandonment of easement", "surrender of easement", "vacate easement",
        ],
        "category": "release",
    },
    "easement_assignment": {
        "canonical": "Easement Assignment",
        "keywords": [
            "assignment of easement", "easement assignment", "transfer of easement",
            "assignment of right-of-way", "row assignment",
        ],
        "category": "assignment",
    },
    "condemnation_petition": {
        "canonical": "Condemnation Petition",
        "keywords": [
            "condemnation petition", "eminent domain petition",
            "condemnation proceeding", "petition for condemnation",
            "petition to condemn",
        ],
        "category": "litigation",
    },
    "crossing_agreement": {
        "canonical": "Crossing Agreement",
        "keywords": [
            "crossing agreement", "pipeline crossing", "utility crossing",
            "road crossing agreement", "railroad crossing agreement",
        ],
        "category": "agreement",
    },
    "amendment_to_easement": {
        "canonical": "Amendment to Easement",
        "keywords": [
            "amendment to easement", "easement amendment", "modification of easement",
            "amended easement", "supplemental easement",
        ],
        "category": "amendment",
    },
    "subordination_agreement": {
        "canonical": "Subordination Agreement",
        "keywords": [
            "subordination agreement", "subordination of easement",
            "subordination of lien to easement", "lien subordination",
        ],
        "category": "agreement",
    },
}


# ============================================================================
# OPERATOR ALIAS MAP - Common Pipeline Operators and Aliases
# ============================================================================

OPERATOR_ALIAS_MAP: Dict[str, List[str]] = {
    "Enterprise Products Partners": [
        "enterprise products", "enterprise", "epd", "EPPL",
        "enterprise products partners", "enterprise products operating",
    ],
    "Energy Transfer Partners": [
        "energy transfer", "etp", "energy transfer partners",
        "energy transfer operating", "energy transfer equity",
        "sunoco logistics", "sunoco pipeline",
    ],
    "Plains All American Pipeline": [
        "plains all american", "plains pipeline", "paa",
        "plains all american pipeline", "plains marketing",
    ],
    "Kinder Morgan": [
        "kinder morgan", "kmi", "kinder morgan texas pipeline",
        "kinder morgan operating", "kmep", "natural gas pipeline company of america",
        "ngpl", "el paso natural gas", "colorado interstate gas",
    ],
    "Williams Companies": [
        "williams", "williams companies", "wmb", "transco",
        "transcontinental gas pipeline", "williams partners",
    ],
    "ONEOK": [
        "oneok", "oneok partners", "oke", "oneok inc",
    ],
    "Targa Resources": [
        "targa", "targa resources", "trgp", "targa pipeline",
    ],
    "DCP Midstream": [
        "dcp midstream", "dcp", "dcp midstream partners",
    ],
    "Crestwood Equity Partners": [
        "crestwood", "crestwood equity", "crestwood midstream",
    ],
    "Western Gas Partners": [
        "western gas", "western gas partners", "wes",
    ],
    "Summit Midstream Partners": [
        "summit midstream", "summit", "smlp",
    ],
    "Enbridge": [
        "enbridge", "enb", "enbridge pipelines", "enbridge energy",
        "enbridge inc", "spectra energy",
    ],
    "TC Energy": [
        "tc energy", "transcanada", "trp", "tc energy corporation",
    ],
    "Permian Highway Pipeline": [
        "permian highway", "php", "permian highway pipeline",
    ],
    "Gulf Coast Express Pipeline": [
        "gulf coast express", "gce", "gcx",
    ],
    "EPIC Pipeline": [
        "epic", "epic pipeline", "epic crude pipeline",
        "epic y-grade pipeline",
    ],
    "Medallion Midstream": [
        "medallion", "medallion midstream", "medallion gathering",
        "medallion pipeline",
    ],
    "Lucid Energy": [
        "lucid energy", "lucid", "lucid energy group",
    ],
    "Fasken Oil and Ranch": [
        "fasken", "fasken oil", "fasken oil and ranch",
    ],
}


# ============================================================================
# REVERSE INDEX (built at import time for O(1) synonym resolution)
# ============================================================================

_REVERSE_SYNONYM_INDEX: Dict[str, str] = {}
_REVERSE_OPERATOR_INDEX: Dict[str, str] = {}


def _build_reverse_indices() -> None:
    """Build reverse lookup indices for synonym and operator resolution."""
    global _REVERSE_SYNONYM_INDEX, _REVERSE_OPERATOR_INDEX

    for canonical, synonyms in SEMANTIC_MAP.items():
        for syn in synonyms:
            _REVERSE_SYNONYM_INDEX[syn.lower().strip()] = canonical

    for canonical, aliases in OPERATOR_ALIAS_MAP.items():
        for alias in aliases:
            _REVERSE_OPERATOR_INDEX[alias.lower().strip()] = canonical

    logger.debug(
        f"Reverse indices built: {len(_REVERSE_SYNONYM_INDEX)} synonyms, "
        f"{len(_REVERSE_OPERATOR_INDEX)} operator aliases"
    )


_build_reverse_indices()


# ============================================================================
# NORMALIZATION FUNCTIONS
# ============================================================================

def normalize_query(query: str) -> str:
    """
    Normalize a free-text query by expanding abbreviations, lowercasing,
    normalizing whitespace, and stripping punctuation noise.

    Args:
        query: Raw user query string.

    Returns:
        Normalized query string suitable for search.
    """
    if not query or not query.strip():
        return ""

    normalized = query.strip()

    # Expand known abbreviations (case-sensitive first pass)
    for abbr, expansion in ABBREVIATION_MAP.items():
        pattern = re.compile(r'\b' + re.escape(abbr) + r'\b')
        normalized = pattern.sub(expansion, normalized)

    # Lowercase
    normalized = normalized.lower()

    # Normalize whitespace
    normalized = re.sub(r'\s+', ' ', normalized).strip()

    # Remove excessive punctuation but keep hyphens in compound terms
    normalized = re.sub(r'[^\w\s\-/.]', '', normalized)

    # Normalize common variants
    normalized = normalized.replace("right-of-way", "right of way")
    normalized = re.sub(r'\brow\b', 'right of way', normalized)
    normalized = re.sub(r'\br/w\b', 'right of way', normalized)

    return normalized


def expand_abbreviations(text: str) -> str:
    """
    Expand known abbreviations in text to their full forms.

    Args:
        text: Input text potentially containing abbreviations.

    Returns:
        Text with abbreviations expanded.
    """
    if not text:
        return ""

    expanded = text
    for abbr, expansion in sorted(ABBREVIATION_MAP.items(), key=lambda x: -len(x[0])):
        pattern = re.compile(r'\b' + re.escape(abbr) + r'\b')
        expanded = pattern.sub(f"{expansion} ({abbr})", expanded, count=1)

    return expanded


def resolve_synonyms(text: str) -> Dict[str, List[str]]:
    """
    Identify canonical terms present in text via synonym matching.

    Args:
        text: Input text to analyze.

    Returns:
        Dict mapping canonical terms to the matching synonyms found in text.
    """
    if not text:
        return {}

    text_lower = text.lower()
    found: Dict[str, List[str]] = defaultdict(list)

    for synonym, canonical in _REVERSE_SYNONYM_INDEX.items():
        if synonym in text_lower:
            if synonym not in found[canonical]:
                found[canonical].append(synonym)

    return dict(found)


def resolve_operator(name: str) -> Optional[str]:
    """
    Resolve a pipeline operator name or alias to the canonical name.

    Args:
        name: Operator name or alias.

    Returns:
        Canonical operator name, or None if not found.
    """
    if not name:
        return None
    return _REVERSE_OPERATOR_INDEX.get(name.lower().strip())


def classify_instrument_type(text: str) -> Optional[Dict[str, Any]]:
    """
    Classify a document/instrument by type based on keyword matching
    against the INSTRUMENT_TYPE_MAP.

    Args:
        text: Instrument title, description, or content snippet.

    Returns:
        Dict with canonical type, category, and confidence score, or None.
    """
    if not text:
        return None

    text_lower = text.lower()
    best_match: Optional[str] = None
    best_score: float = 0.0

    for type_key, type_info in INSTRUMENT_TYPE_MAP.items():
        keyword_hits = sum(1 for kw in type_info["keywords"] if kw.lower() in text_lower)
        if keyword_hits > 0:
            score = keyword_hits / len(type_info["keywords"])
            if score > best_score:
                best_score = score
                best_match = type_key

    if best_match and best_score > 0.0:
        info = INSTRUMENT_TYPE_MAP[best_match]
        return {
            "instrument_type": best_match,
            "canonical_name": info["canonical"],
            "category": info["category"],
            "confidence": round(min(best_score * 2.0, 1.0), 3),
        }

    return None


def extract_easement_terms(text: str) -> List[Dict[str, Any]]:
    """
    Extract easement-related terms from text, returning canonical term,
    matched synonym, and position in text.

    Args:
        text: Input text to analyze.

    Returns:
        List of dicts with canonical_term, matched_synonym, and position.
    """
    if not text:
        return []

    text_lower = text.lower()
    results: List[Dict[str, Any]] = []
    seen_positions: Set[int] = set()

    for synonym, canonical in sorted(
        _REVERSE_SYNONYM_INDEX.items(),
        key=lambda x: -len(x[0])
    ):
        start = 0
        while True:
            pos = text_lower.find(synonym, start)
            if pos == -1:
                break
            if pos not in seen_positions:
                seen_positions.add(pos)
                results.append({
                    "canonical_term": canonical,
                    "matched_synonym": synonym,
                    "position": pos,
                    "length": len(synonym),
                })
            start = pos + 1

    results.sort(key=lambda x: x["position"])
    return results


def get_all_canonical_terms() -> List[str]:
    """Return sorted list of all canonical terms in the semantic map."""
    return sorted(SEMANTIC_MAP.keys())


def get_synonyms_for_term(canonical_term: str) -> List[str]:
    """Return all synonyms for a given canonical term."""
    return SEMANTIC_MAP.get(canonical_term, [])


def get_all_abbreviations() -> Dict[str, str]:
    """Return the complete abbreviation map."""
    return dict(ABBREVIATION_MAP)


def get_operator_canonical_names() -> List[str]:
    """Return sorted list of all canonical pipeline operator names."""
    return sorted(OPERATOR_ALIAS_MAP.keys())


def get_instrument_types() -> List[str]:
    """Return sorted list of all recognized instrument type keys."""
    return sorted(INSTRUMENT_TYPE_MAP.keys())


def normalize_party_name(name: str) -> str:
    """
    Normalize a grantor/grantee party name for matching.
    Strips common suffixes (LLC, LP, Inc, etc.), normalizes whitespace,
    and applies consistent casing.

    Args:
        name: Raw party name from instrument.

    Returns:
        Normalized party name.
    """
    if not name:
        return ""

    normalized = name.strip()

    # Remove common entity suffixes for matching
    suffixes = [
        r'\b(LLC|L\.L\.C\.)\b',
        r'\b(LP|L\.P\.)\b',
        r'\b(Inc\.?|Incorporated)\b',
        r'\b(Corp\.?|Corporation)\b',
        r'\b(Ltd\.?|Limited)\b',
        r'\b(Co\.?|Company)\b',
        r'\b(LLP|L\.L\.P\.)\b',
        r'\b(PC|P\.C\.)\b',
        r'\b(PLLC|P\.L\.L\.C\.)\b',
        r'\b(d/b/a|DBA|dba)\b',
        r'\b(et\s+al\.?)\b',
        r'\b(et\s+ux\.?)\b',
        r'\b(et\s+vir\.?)\b',
        r'\b(a/k/a|AKA|aka)\b',
        r'\b(f/k/a|FKA|fka)\b',
        r'\b(n/k/a|NKA|nka)\b',
        r'\b(as\s+trustee)\b',
        r'\b(individually\s+and\s+as)\b',
        r',?\s*(a\s+Texas\s+limited\s+partnership)\b',
        r',?\s*(a\s+Texas\s+corporation)\b',
        r',?\s*(a\s+Texas\s+limited\s+liability\s+company)\b',
        r',?\s*(a\s+Delaware\s+limited\s+partnership)\b',
        r',?\s*(a\s+Delaware\s+corporation)\b',
    ]

    for suffix_pattern in suffixes:
        normalized = re.sub(suffix_pattern, '', normalized, flags=re.IGNORECASE)

    # Normalize whitespace and punctuation
    normalized = re.sub(r'\s+', ' ', normalized).strip()
    normalized = re.sub(r'\s*,\s*$', '', normalized).strip()
    normalized = re.sub(r'\s*;\s*$', '', normalized).strip()

    return normalized


def normalize_legal_description(text: str) -> str:
    """
    Normalize a legal description for consistent matching.
    Standardizes section/block/township/range formatting.

    Args:
        text: Raw legal description text.

    Returns:
        Normalized legal description.
    """
    if not text:
        return ""

    normalized = text.strip()

    # Standardize section references
    normalized = re.sub(r'\bSec(?:tion)?\.?\s*', 'Section ', normalized, flags=re.IGNORECASE)
    normalized = re.sub(r'\bBlk\.?\s*', 'Block ', normalized, flags=re.IGNORECASE)
    normalized = re.sub(r'\bTwp\.?\s*', 'Township ', normalized, flags=re.IGNORECASE)
    normalized = re.sub(r'\bRng\.?\s*', 'Range ', normalized, flags=re.IGNORECASE)
    normalized = re.sub(r'\bAbst?\.?\s*', 'Abstract ', normalized, flags=re.IGNORECASE)
    normalized = re.sub(r'\bSvy\.?\s*', 'Survey ', normalized, flags=re.IGNORECASE)

    # Standardize directional abbreviations
    normalized = re.sub(r'\bN\.?\s*', 'North ', normalized)
    normalized = re.sub(r'\bS\.?\s*', 'South ', normalized)
    normalized = re.sub(r'\bE\.?\s*', 'East ', normalized)
    normalized = re.sub(r'\bW\.?\s*', 'West ', normalized)

    # Normalize whitespace
    normalized = re.sub(r'\s+', ' ', normalized).strip()

    return normalized


# ============================================================================
# EASEMENT CLAUSE PATTERNS - for identifying easement grants in instrument text
# ============================================================================

EASEMENT_CLAUSE_PATTERNS: Dict[str, List[str]] = {
    "grant_language": [
        r"grants?\s+(?:and\s+conveys?\s+)?(?:unto|to)\s+.+?\s+(?:an?\s+)?easement",
        r"grant(?:s|ed|ing)?\s+(?:a\s+)?(?:permanent\s+)?(?:non-exclusive\s+)?(?:easement|right-of-way)",
        r"hereby\s+grant(?:s|ed)?\s+(?:and\s+convey(?:s|ed)?)?\s+.+?\s+(?:an?\s+)?(?:pipeline\s+)?(?:easement|right-of-way)",
        r"convey(?:s|ed|ing)?\s+(?:and\s+grant(?:s|ed)?)?\s+(?:unto|to)\s+.+?\s+(?:an?\s+)?(?:easement|right-of-way)",
    ],
    "reservation_language": [
        r"reserv(?:es?|ing|ed)\s+(?:unto\s+(?:itself|grantor)\s+)?(?:an?\s+)?easement",
        r"except(?:s|ing|ed)?\s+and\s+reserv(?:es?|ing|ed)\s+(?:an?\s+)?easement",
        r"subject\s+to\s+(?:a\s+)?reserved?\s+easement",
    ],
    "width_specification": [
        r"(\d+[\.\d]*)\s*(?:foot|ft\.?|feet|')\s*(?:wide|width|in\s+width)",
        r"width\s+of\s+(\d+[\.\d]*)\s*(?:foot|ft\.?|feet|')",
        r"(\d+[\.\d]*)\s*(?:foot|ft\.?|feet|')\s*permanent\s+(?:easement|right-of-way)",
    ],
    "depth_specification": [
        r"(?:depth|cover)\s+of\s+(?:at\s+least\s+)?(\d+[\.\d]*)\s*(?:inch(?:es)?|in\.?|foot|ft\.?|feet)",
        r"(?:buried|installed|laid)\s+(?:at\s+)?(?:a\s+)?(?:minimum\s+)?(?:depth\s+of\s+)?(\d+[\.\d]*)\s*(?:inch|in\.?|foot|ft\.?|feet)",
        r"(\d+[\.\d]*)\s*(?:inch|in\.?|foot|ft\.?|feet)\s+(?:of\s+)?cover",
    ],
    "duration_specification": [
        r"(?:for\s+a\s+)?(?:period|term)\s+of\s+(\d+)\s*years?",
        r"in\s+perpetuity",
        r"perpetual\s+(?:easement|right-of-way)",
        r"(?:so\s+long\s+as|during\s+(?:the\s+)?(?:time|period)\s+(?:that|of))",
        r"for\s+(?:the\s+)?(?:life|duration)\s+of\s+(?:the\s+)?(?:pipeline|operations?)",
    ],
    "pipeline_specification": [
        r"(\d+[\.\d]*)\s*(?:inch|in\.?|\")\s*(?:diameter\s+)?(?:pipeline|pipe\s*line|line)",
        r"(?:pipeline|pipe\s*line|line)\s+(?:not\s+to\s+exceed\s+)?(\d+[\.\d]*)\s*(?:inch|in\.?|\")\s*(?:in\s+)?(?:diameter|outside\s+diameter|OD)",
        r"(?:natural\s+gas|crude\s+oil|petroleum|produced\s+water|salt\s+water|SWD|product)\s+(?:pipeline|pipe\s*line|line)",
    ],
}


def extract_clause_matches(text: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Extract easement clause pattern matches from instrument text.

    Args:
        text: Full instrument text to analyze.

    Returns:
        Dict mapping clause type to list of matches with position and captured groups.
    """
    if not text:
        return {}

    results: Dict[str, List[Dict[str, Any]]] = {}

    for clause_type, patterns in EASEMENT_CLAUSE_PATTERNS.items():
        matches_for_type: List[Dict[str, Any]] = []
        for pattern in patterns:
            for match in re.finditer(pattern, text, flags=re.IGNORECASE):
                match_info: Dict[str, Any] = {
                    "pattern": pattern,
                    "matched_text": match.group(0),
                    "start": match.start(),
                    "end": match.end(),
                }
                if match.groups():
                    match_info["captured_groups"] = list(match.groups())
                matches_for_type.append(match_info)

        if matches_for_type:
            results[clause_type] = matches_for_type

    return results


def extract_dimensions_from_text(text: str) -> Dict[str, Optional[float]]:
    """
    Extract width, depth, and diameter dimensions from instrument text.

    Args:
        text: Instrument text containing dimension specifications.

    Returns:
        Dict with width_ft, depth_ft/depth_inches, and diameter_inches values.
    """
    if not text:
        return {"width_ft": None, "depth_ft": None, "diameter_inches": None}

    width: Optional[float] = None
    depth: Optional[float] = None
    diameter: Optional[float] = None

    # Width extraction
    for pattern in EASEMENT_CLAUSE_PATTERNS["width_specification"]:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match and match.group(1):
            try:
                width = float(match.group(1))
                break
            except ValueError:
                pass

    # Depth extraction
    for pattern in EASEMENT_CLAUSE_PATTERNS["depth_specification"]:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match and match.group(1):
            try:
                val = float(match.group(1))
                # Determine if inches or feet based on context
                if "inch" in match.group(0).lower() or "in." in match.group(0).lower():
                    depth = val / 12.0  # convert to feet
                else:
                    depth = val
                break
            except ValueError:
                pass

    # Diameter extraction
    for pattern in EASEMENT_CLAUSE_PATTERNS["pipeline_specification"]:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            for group in match.groups():
                if group:
                    try:
                        diameter = float(group)
                        break
                    except ValueError:
                        pass
            if diameter:
                break

    return {
        "width_ft": width,
        "depth_ft": depth,
        "diameter_inches": diameter,
    }


def semantic_health() -> Dict[str, Any]:
    """Return health metrics for the semantic module."""
    total_synonyms = sum(len(v) for v in SEMANTIC_MAP.values())
    total_operator_aliases = sum(len(v) for v in OPERATOR_ALIAS_MAP.values())
    return {
        "canonical_terms": len(SEMANTIC_MAP),
        "total_synonyms": total_synonyms,
        "abbreviations": len(ABBREVIATION_MAP),
        "instrument_types": len(INSTRUMENT_TYPE_MAP),
        "operator_aliases": total_operator_aliases,
        "canonical_operators": len(OPERATOR_ALIAS_MAP),
        "reverse_synonym_index_size": len(_REVERSE_SYNONYM_INDEX),
        "reverse_operator_index_size": len(_REVERSE_OPERATOR_INDEX),
        "clause_patterns": len(EASEMENT_CLAUSE_PATTERNS),
    }
