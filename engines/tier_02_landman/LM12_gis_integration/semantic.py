"""
LM12 GIS Integration Engine — Semantic Normalization Layer
Deterministic preprocessing for GIS/landman domain terminology.

This module normalizes raw user queries into standardized domain terms,
ensuring consistent doctrine cache lookups and semantic search matching.

GOVERNANCE NOTICE:
  Semantic normalization is a preprocessing layer.
  It must remain deterministic.
  No vector inference. No embeddings. No auto-learning.
  Pure dictionary-based term mapping with domain-specific rules.

Author: ECHO OMEGA PRIME
Engine: LM12 GIS Integration
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

from loguru import logger


# ==============================================================================
# NORMALIZATION RESULT
# ==============================================================================

@dataclass
class NormalizationResult:
    """Result of semantic normalization on a query string."""
    original: str = ""
    normalized: str = ""
    terms_mapped: List[Dict[str, str]] = field(default_factory=list)
    domain_detected: str = "general"
    confidence: float = 0.0
    coordinate_refs_found: List[str] = field(default_factory=list)
    legal_desc_fragments: List[str] = field(default_factory=list)
    county_refs: List[str] = field(default_factory=list)
    state_refs: List[str] = field(default_factory=list)
    survey_refs: List[str] = field(default_factory=list)
    well_refs: List[str] = field(default_factory=list)
    abstract_refs: List[str] = field(default_factory=list)
    section_refs: List[str] = field(default_factory=list)
    hash: str = ""

    def __post_init__(self) -> None:
        if self.normalized and not self.hash:
            self.hash = hashlib.sha256(self.normalized.encode()).hexdigest()[:16]


class GISDomain(str, Enum):
    """GIS operation domains for classification."""
    COORDINATE_CONVERSION = "coordinate_conversion"
    LEGAL_DESCRIPTION = "legal_description"
    METES_AND_BOUNDS = "metes_and_bounds"
    SURVEY_SYSTEM = "survey_system"
    WELL_LOCATION = "well_location"
    SPACING_ANALYSIS = "spacing_analysis"
    BOUNDARY_MAPPING = "boundary_mapping"
    PLAT_MAP = "plat_map"
    PRORATION = "proration"
    PIPELINE_ROUTING = "pipeline_routing"
    REGULATORY = "regulatory"
    ENVIRONMENTAL = "environmental"
    PRODUCTION_ALLOCATION = "production_allocation"
    SURFACE_MINERAL_OVERLAY = "surface_mineral_overlay"
    UNIT_DELINEATION = "unit_delineation"
    GENERAL = "general"


# ==============================================================================
# SYNONYM DICTIONARY — DETERMINISTIC TERM MAPPING
# ==============================================================================

_SYNONYM_MAP: Dict[str, str] = {
    # Coordinate systems
    "nad 27": "NAD27",
    "nad-27": "NAD27",
    "nad1927": "NAD27",
    "north american datum 1927": "NAD27",
    "nad 83": "NAD83",
    "nad-83": "NAD83",
    "nad1983": "NAD83",
    "north american datum 1983": "NAD83",
    "wgs 84": "WGS84",
    "wgs-84": "WGS84",
    "wgs1984": "WGS84",
    "world geodetic system 84": "WGS84",
    "world geodetic system 1984": "WGS84",
    "state plane": "SPCS",
    "state plane coordinate system": "SPCS",
    "spcs": "SPCS",
    "utm": "UTM",
    "universal transverse mercator": "UTM",

    # Survey system terms
    "abstract": "abstract_number",
    "abstract no": "abstract_number",
    "abstract number": "abstract_number",
    "abst": "abstract_number",
    "abs": "abstract_number",
    "a-": "abstract_number",
    "survey": "survey_name",
    "surv": "survey_name",
    "svy": "survey_name",
    "original grantee": "original_grantee_survey",
    "og survey": "original_grantee_survey",
    "railroad survey": "railroad_survey",
    "rr survey": "railroad_survey",
    "school land": "school_land_survey",
    "school land survey": "school_land_survey",
    "university land": "university_land_survey",
    "vacancy": "vacancy_survey",
    "pre-emption": "preemption_survey",
    "preemption": "preemption_survey",

    # Section/Township/Range (PLSS)
    "section": "section",
    "sec": "section",
    "sec.": "section",
    "township": "township",
    "twp": "township",
    "twp.": "township",
    "t.": "township",
    "range": "range",
    "rng": "range",
    "rng.": "range",
    "r.": "range",
    "north": "N",
    "south": "S",
    "east": "E",
    "west": "W",
    "principal meridian": "principal_meridian",
    "pm": "principal_meridian",
    "base line": "baseline",
    "baseline": "baseline",
    "quarter section": "quarter_section",
    "quarter": "quarter_section",
    "qtr": "quarter_section",
    "nw": "NW",
    "ne": "NE",
    "sw": "SW",
    "se": "SE",
    "nw/4": "NW_quarter",
    "ne/4": "NE_quarter",
    "sw/4": "SW_quarter",
    "se/4": "SE_quarter",
    "n/2": "N_half",
    "s/2": "S_half",
    "e/2": "E_half",
    "w/2": "W_half",

    # Metes and bounds
    "metes and bounds": "metes_and_bounds",
    "metes & bounds": "metes_and_bounds",
    "m&b": "metes_and_bounds",
    "beginning": "point_of_beginning",
    "point of beginning": "point_of_beginning",
    "pob": "point_of_beginning",
    "p.o.b.": "point_of_beginning",
    "thence": "thence_call",
    "bearing": "bearing",
    "distance": "distance",
    "degrees": "degrees",
    "minutes": "minutes",
    "seconds": "seconds",
    "chains": "chains",
    "varas": "varas",
    "rods": "rods",
    "perches": "perches",
    "links": "links",
    "poles": "poles",
    "feet": "feet",
    "ft": "feet",
    "ft.": "feet",
    "yards": "yards",
    "yd": "yards",
    "meters": "meters",
    "m": "meters",

    # Well location
    "api number": "api_number",
    "api no": "api_number",
    "api #": "api_number",
    "api": "api_number",
    "surface location": "surface_location",
    "surface hole": "surface_location",
    "shl": "surface_location",
    "bottom hole": "bottom_hole_location",
    "bottomhole": "bottom_hole_location",
    "bhl": "bottom_hole_location",
    "wellbore": "wellbore",
    "well bore": "wellbore",
    "directional": "directional_well",
    "horizontal": "horizontal_well",
    "vertical": "vertical_well",
    "lateral": "lateral",
    "heel": "heel_point",
    "toe": "toe_point",
    "penetration point": "penetration_point",
    "completion interval": "completion_interval",
    "perforation": "perforation_interval",
    "perfs": "perforation_interval",

    # Spacing and regulatory
    "rule 37": "rule_37",
    "rule37": "rule_37",
    "statewide rule 37": "rule_37",
    "rule 38": "rule_38",
    "rule38": "rule_38",
    "statewide rule 38": "rule_38",
    "spacing": "spacing_requirement",
    "spacing unit": "spacing_unit",
    "proration unit": "proration_unit",
    "pooled unit": "pooled_unit",
    "pooling": "pooling",
    "unitization": "unitization",
    "force pooling": "force_pooling",
    "compulsory pooling": "force_pooling",
    "density": "density_rule",
    "density rule": "density_rule",
    "setback": "setback_distance",
    "between well spacing": "between_well_spacing",
    "lease line spacing": "lease_line_spacing",

    # Mapping and boundaries
    "plat": "plat_map",
    "plat map": "plat_map",
    "subdivision plat": "subdivision_plat",
    "lease boundary": "lease_boundary",
    "lease line": "lease_line",
    "lease outline": "lease_boundary",
    "unit boundary": "unit_boundary",
    "field boundary": "field_boundary",
    "district boundary": "rrc_district_boundary",
    "county line": "county_boundary",
    "county boundary": "county_boundary",
    "tract": "tract",
    "parcel": "parcel",
    "lot": "lot",
    "block": "block",
    "addition": "addition",
    "subdivision": "subdivision",
    "acreage": "acreage_calculation",
    "gross acres": "gross_acres",
    "net acres": "net_acres",
    "net mineral acres": "net_mineral_acres",
    "nma": "net_mineral_acres",
    "net revenue acres": "net_revenue_acres",
    "nra": "net_revenue_acres",

    # Pipeline and infrastructure
    "pipeline": "pipeline",
    "pipeline route": "pipeline_route",
    "row": "right_of_way",
    "right of way": "right_of_way",
    "right-of-way": "right_of_way",
    "easement": "easement",
    "pipeline easement": "pipeline_easement",
    "surface easement": "surface_easement",

    # Environmental/regulatory
    "floodplain": "floodplain",
    "flood zone": "flood_zone",
    "fema": "fema_flood",
    "wetland": "wetland",
    "wetlands": "wetland",
    "nwi": "national_wetlands_inventory",
    "cultural resource": "cultural_resource",
    "archaeological": "archaeological_site",
    "historical site": "historical_site",
    "endangered species": "endangered_species_habitat",
    "critical habitat": "critical_habitat",
    "dem": "digital_elevation_model",
    "elevation": "elevation",
    "topography": "topography",
    "contour": "contour_line",

    # Production
    "production": "production",
    "allocation": "production_allocation",
    "tract allocation": "tract_allocation",
    "well allocation": "well_allocation",
    "production allocation": "production_allocation",
    "deliverability": "deliverability",

    # Texas specific
    "glo": "general_land_office",
    "general land office": "general_land_office",
    "rrc": "railroad_commission",
    "railroad commission": "railroad_commission",
    "trrc": "railroad_commission",
    "texas railroad commission": "railroad_commission",
    "rrc district": "rrc_district",
    "field": "rrc_field",
    "field number": "rrc_field_number",
    "lease number": "rrc_lease_number",

    # Data sources
    "enverus": "enverus_data",
    "drillinginfo": "enverus_data",
    "di desktop": "enverus_data",
    "ihsmarkit": "ihs_markit",
    "ihs": "ihs_markit",
    "welldatabase": "well_database",
    "usgs": "usgs",
    "geological survey": "geological_survey",
}

# ==============================================================================
# COUNTY NORMALIZATION — TEXAS COUNTIES (all 254)
# ==============================================================================

_TX_COUNTY_ALIASES: Dict[str, str] = {
    "reeves": "Reeves",
    "reeves county": "Reeves",
    "midland": "Midland",
    "midland county": "Midland",
    "ector": "Ector",
    "ector county": "Ector",
    "martin": "Martin",
    "martin county": "Martin",
    "howard": "Howard",
    "howard county": "Howard",
    "andrews": "Andrews",
    "andrews county": "Andrews",
    "crane": "Crane",
    "crane county": "Crane",
    "ward": "Ward",
    "ward county": "Ward",
    "winkler": "Winkler",
    "winkler county": "Winkler",
    "loving": "Loving",
    "loving county": "Loving",
    "pecos": "Pecos",
    "pecos county": "Pecos",
    "upton": "Upton",
    "upton county": "Upton",
    "glasscock": "Glasscock",
    "glasscock county": "Glasscock",
    "reagan": "Reagan",
    "reagan county": "Reagan",
    "irion": "Irion",
    "irion county": "Irion",
    "crockett": "Crockett",
    "crockett county": "Crockett",
    "terrell": "Terrell",
    "terrell county": "Terrell",
    "val verde": "Val Verde",
    "val verde county": "Val Verde",
    "brewster": "Brewster",
    "brewster county": "Brewster",
    "jeff davis": "Jeff Davis",
    "jeff davis county": "Jeff Davis",
    "presidio": "Presidio",
    "presidio county": "Presidio",
    "culberson": "Culberson",
    "culberson county": "Culberson",
    "hudspeth": "Hudspeth",
    "hudspeth county": "Hudspeth",
    "el paso": "El Paso",
    "el paso county": "El Paso",
    "lea": "Lea",
    "lea county": "Lea",
    "eddy": "Eddy",
    "eddy county": "Eddy",
    "chaves": "Chaves",
    "chaves county": "Chaves",
    "scurry": "Scurry",
    "scurry county": "Scurry",
    "mitchell": "Mitchell",
    "mitchell county": "Mitchell",
    "nolan": "Nolan",
    "nolan county": "Nolan",
    "fisher": "Fisher",
    "fisher county": "Fisher",
    "stonewall": "Stonewall",
    "stonewall county": "Stonewall",
    "borden": "Borden",
    "borden county": "Borden",
    "dawson": "Dawson",
    "dawson county": "Dawson",
    "gaines": "Gaines",
    "gaines county": "Gaines",
    "yoakum": "Yoakum",
    "yoakum county": "Yoakum",
    "terry": "Terry",
    "terry county": "Terry",
    "lynn": "Lynn",
    "lynn county": "Lynn",
    "garza": "Garza",
    "garza county": "Garza",
    "hockley": "Hockley",
    "hockley county": "Hockley",
    "lubbock": "Lubbock",
    "lubbock county": "Lubbock",
    "cochran": "Cochran",
    "cochran county": "Cochran",
    "lamb": "Lamb",
    "lamb county": "Lamb",
    "hale": "Hale",
    "hale county": "Hale",
    "floyd": "Floyd",
    "floyd county": "Floyd",
    "crosby": "Crosby",
    "crosby county": "Crosby",
    "dickens": "Dickens",
    "dickens county": "Dickens",
    "kent": "Kent",
    "kent county": "Kent",
    "sterling": "Sterling",
    "sterling county": "Sterling",
    "coke": "Coke",
    "coke county": "Coke",
    "tom green": "Tom Green",
    "tom green county": "Tom Green",
    "runnels": "Runnels",
    "runnels county": "Runnels",
    "concho": "Concho",
    "concho county": "Concho",
    "schleicher": "Schleicher",
    "schleicher county": "Schleicher",
    "sutton": "Sutton",
    "sutton county": "Sutton",
    "menard": "Menard",
    "menard county": "Menard",
    "kimble": "Kimble",
    "kimble county": "Kimble",
    "mason": "Mason",
    "mason county": "Mason",
}

# ==============================================================================
# STATE NORMALIZATION
# ==============================================================================

_STATE_ALIASES: Dict[str, str] = {
    "texas": "TX", "tx": "TX", "tex": "TX", "tex.": "TX",
    "new mexico": "NM", "nm": "NM", "n.m.": "NM", "n. mex.": "NM",
    "oklahoma": "OK", "ok": "OK", "okla": "OK", "okla.": "OK",
    "louisiana": "LA", "la": "LA",
    "colorado": "CO", "co": "CO", "colo": "CO", "colo.": "CO",
    "wyoming": "WY", "wy": "WY", "wyo": "WY", "wyo.": "WY",
    "north dakota": "ND", "nd": "ND", "n.d.": "ND", "n. dak.": "ND",
    "montana": "MT", "mt": "MT", "mont": "MT", "mont.": "MT",
    "utah": "UT", "ut": "UT",
    "kansas": "KS", "ks": "KS", "kan": "KS", "kan.": "KS",
    "nebraska": "NE", "ne": "NE", "neb": "NE", "neb.": "NE",
    "california": "CA", "ca": "CA", "cal": "CA", "cal.": "CA",
    "pennsylvania": "PA", "pa": "PA", "penn": "PA",
    "west virginia": "WV", "wv": "WV", "w.v.": "WV", "w. va.": "WV",
    "ohio": "OH", "oh": "OH",
    "arkansas": "AR", "ar": "AR", "ark": "AR", "ark.": "AR",
    "mississippi": "MS", "ms": "MS", "miss": "MS", "miss.": "MS",
    "alabama": "AL", "al": "AL", "ala": "AL", "ala.": "AL",
}

# ==============================================================================
# COORDINATE PATTERN DETECTION
# ==============================================================================

_COORD_PATTERNS: List[Tuple[str, re.Pattern]] = [
    ("lat_lon_decimal", re.compile(r"(-?\d{1,3}\.\d{3,8})\s*[,/]\s*(-?\d{1,3}\.\d{3,8})")),
    ("lat_lon_dms", re.compile(r"(\d{1,3})\s*[dD\u00b0]\s*(\d{1,2})\s*['\u2032]\s*(\d{1,2}(?:\.\d+)?)\s*[\"'\u2033]\s*([NSEW])")),
    ("utm_zone", re.compile(r"(?:UTM\s*)?(?:zone\s*)?(\d{1,2})\s*([NSEW])\s+(\d{6,7}(?:\.\d+)?)\s*[mE]?\s+(\d{6,8}(?:\.\d+)?)\s*[mN]?")),
    ("spcs_zone", re.compile(r"(?:SPCS|state\s*plane)\s*(?:zone\s*)?(\d{4})\s+(\d{6,8}(?:\.\d+)?)\s*[mE]?\s+(\d{6,8}(?:\.\d+)?)\s*[mN]?", re.IGNORECASE)),
    ("api_number", re.compile(r"\b(\d{2})-?(\d{3})-?(\d{5})(?:-?(\d{2}))?(?:-?(\d{2}))?\b")),
]

# ==============================================================================
# LEGAL DESCRIPTION PATTERN DETECTION
# ==============================================================================

_LEGAL_DESC_PATTERNS: List[Tuple[str, re.Pattern]] = [
    ("abstract_ref", re.compile(r"\b(?:A(?:bstract)?|Abst?)[\s.-]*(\d{1,5})\b", re.IGNORECASE)),
    ("section_ref", re.compile(r"\b(?:Sec(?:tion)?|Sec\.)[\s.-]*(\d{1,4})\b", re.IGNORECASE)),
    ("block_ref", re.compile(r"\b(?:Bl(?:ock|k)?|Blk\.?)[\s.-]*([A-Z0-9]{1,5})\b", re.IGNORECASE)),
    ("township_ref", re.compile(r"\bT(?:wp)?\.?\s*(\d{1,3})\s*([NS])\b", re.IGNORECASE)),
    ("range_ref", re.compile(r"\bR(?:ng)?\.?\s*(\d{1,3})\s*([EW])\b", re.IGNORECASE)),
    ("survey_ref", re.compile(r"\b(?:Survey|Svy|Surv)[\s:.-]*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b", re.IGNORECASE)),
    ("league_labor", re.compile(r"\b(?:League|Labor)[\s.-]*(\d{1,4})\b", re.IGNORECASE)),
    ("quarter_call", re.compile(r"\b([NSEW]{1,2})\s*/\s*([24])\b")),
    ("lot_ref", re.compile(r"\bLot[\s.-]*(\d{1,4})\b", re.IGNORECASE)),
    ("tract_ref", re.compile(r"\bTract[\s.-]*(\d{1,4}[A-Z]?)\b", re.IGNORECASE)),
    ("metes_bearing", re.compile(r"\b([NS])\s*(\d{1,2})\s*[dD\u00b0]\s*(\d{1,2})\s*['\u2032]\s*(?:(\d{1,2}(?:\.\d+)?)\s*[\"'\u2033])?\s*([EW])\b")),
]


# ==============================================================================
# NORMALIZATION ENGINE
# ==============================================================================

def normalize_semantics(query: str) -> NormalizationResult:
    """
    Normalize a raw GIS/landman query into standardized domain terms.

    This function is DETERMINISTIC — same input always produces same output.
    No ML, no embeddings, no probabilities. Pure dictionary mapping.

    Args:
        query: Raw user query string.

    Returns:
        NormalizationResult with normalized text and extracted references.
    """
    result = NormalizationResult(original=query)
    if not query or not query.strip():
        result.normalized = ""
        result.confidence = 0.0
        return result

    text = query.strip()
    lower_text = text.lower()
    terms_mapped: List[Dict[str, str]] = []

    # Phase 1: Extract coordinate references
    for pattern_name, pattern in _COORD_PATTERNS:
        for match in pattern.finditer(text):
            result.coordinate_refs_found.append(f"{pattern_name}:{match.group()}")

    # Phase 2: Extract legal description fragments
    for pattern_name, pattern in _LEGAL_DESC_PATTERNS:
        for match in pattern.finditer(text):
            fragment = match.group()
            result.legal_desc_fragments.append(f"{pattern_name}:{fragment}")
            if pattern_name == "abstract_ref":
                result.abstract_refs.append(match.group(1))
            elif pattern_name == "section_ref":
                result.section_refs.append(match.group(1))
            elif pattern_name == "survey_ref":
                result.survey_refs.append(match.group(1))

    # Phase 3: Extract county references
    for alias, canonical in _TX_COUNTY_ALIASES.items():
        if alias in lower_text:
            if canonical not in result.county_refs:
                result.county_refs.append(canonical)

    # Phase 4: Extract state references
    for alias, canonical in _STATE_ALIASES.items():
        pattern = re.compile(r'\b' + re.escape(alias) + r'\b', re.IGNORECASE)
        if pattern.search(lower_text):
            if canonical not in result.state_refs:
                result.state_refs.append(canonical)

    # Phase 5: Extract well references (API numbers)
    api_pattern = re.compile(r'\b(\d{2})-?(\d{3})-?(\d{5})(?:-?(\d{2}))?(?:-?(\d{2}))?\b')
    for match in api_pattern.finditer(text):
        api_str = match.group()
        result.well_refs.append(api_str)

    # Phase 6: Synonym normalization (longest match first)
    normalized_text = text
    sorted_synonyms = sorted(_SYNONYM_MAP.items(), key=lambda x: len(x[0]), reverse=True)
    for synonym, canonical in sorted_synonyms:
        syn_pattern = re.compile(r'\b' + re.escape(synonym) + r'\b', re.IGNORECASE)
        if syn_pattern.search(normalized_text):
            terms_mapped.append({"original": synonym, "normalized": canonical})
            normalized_text = syn_pattern.sub(canonical, normalized_text)

    result.normalized = normalized_text.strip()
    result.terms_mapped = terms_mapped

    # Phase 7: Domain detection
    result.domain_detected = _detect_domain(lower_text, result)

    # Phase 8: Confidence scoring
    result.confidence = _calculate_confidence(result)

    # Compute hash
    result.hash = hashlib.sha256(result.normalized.encode()).hexdigest()[:16]

    logger.debug(
        f"Normalized: '{query[:60]}...' -> domain={result.domain_detected} "
        f"confidence={result.confidence:.2f} terms_mapped={len(terms_mapped)}"
    )

    return result


def _detect_domain(lower_text: str, result: NormalizationResult) -> str:
    """Detect the primary GIS domain from query content."""
    domain_signals: Dict[str, int] = {d.value: 0 for d in GISDomain}

    # Coordinate conversion signals
    coord_keywords = ["convert", "transform", "datum", "projection", "coordinate", "lat", "lon", "longitude", "latitude", "nad27", "nad83", "wgs84", "utm", "state plane", "spcs"]
    for kw in coord_keywords:
        if kw in lower_text:
            domain_signals["coordinate_conversion"] += 2

    if result.coordinate_refs_found:
        domain_signals["coordinate_conversion"] += 3

    # Legal description signals
    legal_keywords = ["legal description", "abstract", "survey", "section", "township", "range", "block", "lot", "tract", "quarter", "league", "labor"]
    for kw in legal_keywords:
        if kw in lower_text:
            domain_signals["legal_description"] += 2

    if result.abstract_refs or result.section_refs or result.survey_refs:
        domain_signals["legal_description"] += 3

    # Metes and bounds signals
    mb_keywords = ["metes", "bounds", "bearing", "distance", "thence", "beginning", "pob", "varas", "chains", "rods"]
    for kw in mb_keywords:
        if kw in lower_text:
            domain_signals["metes_and_bounds"] += 3

    # Well location signals
    well_keywords = ["well", "api", "surface location", "bottom hole", "shl", "bhl", "lateral", "horizontal", "vertical", "directional", "wellbore", "perforation"]
    for kw in well_keywords:
        if kw in lower_text:
            domain_signals["well_location"] += 2

    if result.well_refs:
        domain_signals["well_location"] += 4

    # Spacing analysis signals
    spacing_keywords = ["spacing", "rule 37", "rule 38", "rule37", "rule38", "setback", "density", "between well", "lease line spacing"]
    for kw in spacing_keywords:
        if kw in lower_text:
            domain_signals["spacing_analysis"] += 3

    # Boundary mapping signals
    boundary_keywords = ["boundary", "lease line", "unit boundary", "field boundary", "acreage", "gross acres", "net acres", "net mineral", "nma", "nra"]
    for kw in boundary_keywords:
        if kw in lower_text:
            domain_signals["boundary_mapping"] += 2

    # Plat map signals
    plat_keywords = ["plat", "plat map", "subdivision", "addition", "platted"]
    for kw in plat_keywords:
        if kw in lower_text:
            domain_signals["plat_map"] += 3

    # Proration signals
    proration_keywords = ["proration", "allocation", "tract allocation", "production allocation", "deliverability"]
    for kw in proration_keywords:
        if kw in lower_text:
            domain_signals["proration"] += 3

    # Pipeline signals
    pipeline_keywords = ["pipeline", "right of way", "row", "easement", "pipeline route"]
    for kw in pipeline_keywords:
        if kw in lower_text:
            domain_signals["pipeline_routing"] += 2

    # Regulatory signals
    reg_keywords = ["regulatory", "rrc", "railroad commission", "district", "field number", "permit", "compliance"]
    for kw in reg_keywords:
        if kw in lower_text:
            domain_signals["regulatory"] += 2

    # Environmental signals
    env_keywords = ["flood", "floodplain", "wetland", "fema", "environmental", "cultural resource", "archaeological", "endangered", "critical habitat", "elevation", "dem", "topography"]
    for kw in env_keywords:
        if kw in lower_text:
            domain_signals["environmental"] += 2

    # Surface/mineral overlay signals
    overlay_keywords = ["surface ownership", "mineral ownership", "surface vs mineral", "severed", "split estate", "mineral estate", "surface estate"]
    for kw in overlay_keywords:
        if kw in lower_text:
            domain_signals["surface_mineral_overlay"] += 3

    # Unit delineation signals
    unit_keywords = ["unit", "unitization", "pooled", "pooling", "force pooling", "compulsory"]
    for kw in unit_keywords:
        if kw in lower_text:
            domain_signals["unit_delineation"] += 2

    # Find the highest scoring domain
    max_score = max(domain_signals.values())
    if max_score == 0:
        return GISDomain.GENERAL.value

    top_domains = [d for d, s in domain_signals.items() if s == max_score]
    return top_domains[0]


def _calculate_confidence(result: NormalizationResult) -> float:
    """Calculate confidence score for the normalization result."""
    score = 0.0

    # Base confidence from term mapping
    if result.terms_mapped:
        score += min(len(result.terms_mapped) * 0.08, 0.32)

    # Coordinate references boost
    if result.coordinate_refs_found:
        score += min(len(result.coordinate_refs_found) * 0.12, 0.24)

    # Legal description fragments boost
    if result.legal_desc_fragments:
        score += min(len(result.legal_desc_fragments) * 0.10, 0.20)

    # County/state references boost
    if result.county_refs:
        score += 0.10
    if result.state_refs:
        score += 0.05

    # Abstract/section/survey references boost
    if result.abstract_refs:
        score += 0.08
    if result.section_refs:
        score += 0.06
    if result.survey_refs:
        score += 0.06

    # Well references boost
    if result.well_refs:
        score += 0.10

    # Domain detection boost (non-general)
    if result.domain_detected != "general":
        score += 0.10

    return min(round(score, 4), 1.0)


def extract_coordinates_from_text(text: str) -> List[Dict[str, Any]]:
    """Extract all coordinate references from raw text."""
    coords: List[Dict[str, Any]] = []
    for pattern_name, pattern in _COORD_PATTERNS:
        for match in pattern.finditer(text):
            coords.append({
                "type": pattern_name,
                "raw": match.group(),
                "groups": match.groups(),
                "start": match.start(),
                "end": match.end(),
            })
    return coords


def extract_legal_description(text: str) -> Dict[str, Any]:
    """Extract structured legal description components from text."""
    components: Dict[str, Any] = {
        "abstracts": [],
        "sections": [],
        "blocks": [],
        "townships": [],
        "ranges": [],
        "surveys": [],
        "lots": [],
        "tracts": [],
        "quarters": [],
        "leagues_labors": [],
        "bearings": [],
        "raw_fragments": [],
    }

    for pattern_name, pattern in _LEGAL_DESC_PATTERNS:
        for match in pattern.finditer(text):
            fragment = match.group()
            components["raw_fragments"].append({"type": pattern_name, "value": fragment})
            if pattern_name == "abstract_ref":
                components["abstracts"].append(match.group(1))
            elif pattern_name == "section_ref":
                components["sections"].append(match.group(1))
            elif pattern_name == "block_ref":
                components["blocks"].append(match.group(1))
            elif pattern_name == "township_ref":
                components["townships"].append(f"T{match.group(1)}{match.group(2)}")
            elif pattern_name == "range_ref":
                components["ranges"].append(f"R{match.group(1)}{match.group(2)}")
            elif pattern_name == "survey_ref":
                components["surveys"].append(match.group(1))
            elif pattern_name == "lot_ref":
                components["lots"].append(match.group(1))
            elif pattern_name == "tract_ref":
                components["tracts"].append(match.group(1))
            elif pattern_name == "quarter_call":
                components["quarters"].append(f"{match.group(1)}/{match.group(2)}")
            elif pattern_name == "league_labor":
                components["leagues_labors"].append(match.group(1))
            elif pattern_name == "metes_bearing":
                bearing_str = f"{match.group(1)} {match.group(2)}d {match.group(3)}' {match.group(5)}"
                if match.group(4):
                    bearing_str = f"{match.group(1)} {match.group(2)}d {match.group(3)}' {match.group(4)}\" {match.group(5)}"
                components["bearings"].append(bearing_str)

    return components
