"""
LM06 Right of Way Engine - Semantic Normalization
==================================================
Domain-specific term normalization, abbreviation expansion, synonym resolution,
and entity recognition for pipeline ROW acquisition terminology.

Covers: ROW types, pipeline entities, legal instruments, federal/state agencies,
crossing types, compensation terms, condemnation vocabulary, engineering specs.
"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Set, Tuple

from loguru import logger


# ============================================================================
# SEMANTIC MAPS
# ============================================================================

SEMANTIC_MAP: Dict[str, Set[str]] = {
    # ROW types
    "right_of_way": {"row", "r-o-w", "r.o.w.", "easement corridor", "pipeline corridor", "transmission corridor"},
    "easement": {"servitude", "right of ingress egress", "pipeline easement", "utility easement", "perpetual easement"},
    "fee_simple": {"fee", "fee title", "fee simple absolute", "complete ownership", "full title"},
    "temporary_easement": {"temp easement", "construction easement", "temporary workspace", "temp row"},
    "permanent_easement": {"permanent row", "perpetual easement", "permanent corridor"},

    # Pipeline types
    "transmission_pipeline": {"transmission line", "interstate pipeline", "trunk line", "mainline pipeline"},
    "gathering_pipeline": {"gathering line", "gathering system", "field gathering"},
    "distribution_pipeline": {"distribution line", "distribution system", "local distribution"},

    # Common carriers & operators
    "common_carrier": {"common carrier pipeline", "public service pipeline", "certificated carrier"},
    "energy_transfer": {"et", "energy transfer partners", "etp", "sunoco"},
    "enterprise_products": {"enterprise", "epp", "epd"},
    "kinder_morgan": {"kmi", "kinder", "km"},
    "plains_all_american": {"paa", "plains", "plains pipeline"},

    # Legal instruments
    "pipeline_easement": {"row agreement", "easement agreement", "pipeline right-of-way deed"},
    "surface_use_agreement": {"sua", "surface agreement", "surface damage agreement"},
    "crossing_agreement": {"utility crossing", "railroad crossing", "highway crossing"},

    # Federal/State agencies
    "ferc": {"federal energy regulatory commission", "federal power commission"},
    "rrc": {"railroad commission", "texas railroad commission", "tx rrc"},
    "txdot": {"texas department of transportation", "tx dot"},
    "usace": {"army corps of engineers", "corps", "usace"},

    # Condemnation terms
    "eminent_domain": {"condemnation", "taking", "compulsory purchase", "expropriation"},
    "just_compensation": {"fair market value", "fmv", "adequate compensation", "damages"},
    "special_commissioners": {"condemnation commissioners", "appraisal commissioners"},

    # Compensation types
    "easement_value": {"row value", "easement compensation", "perpetual easement payment"},
    "surface_damage": {"construction damage", "crop loss", "restoration costs", "temporary damage"},
    "severance_damages": {"damages to remainder", "consequential damages", "diminution in value"},

    # ROW dimensions
    "row_width": {"easement width", "corridor width", "strip width"},
    "pipeline_depth": {"depth of cover", "burial depth", "depth below surface"},

    # Construction methods
    "open_trench": {"open cut", "conventional construction", "trenching"},
    "hdd": {"horizontal directional drilling", "directional bore", "subsurface drilling"},
    "boring": {"auger boring", "jack and bore", "bore crossing"},

    # Crossing types
    "railroad_crossing": {"rail crossing", "rr crossing", "railway crossing"},
    "highway_crossing": {"road crossing", "txdot crossing", "state highway crossing"},
    "river_crossing": {"waterway crossing", "stream crossing", "creek crossing"},
    "pipeline_crossing": {"utility crossing", "existing pipeline crossing"},

    # Engineering standards
    "asme_b31_4": {"b31.4", "liquid petroleum pipeline code", "asme liquid code"},
    "asme_b31_8": {"b31.8", "gas transmission pipeline code", "asme gas code"},
    "nesc": {"national electrical safety code", "overhead line standards"},

    # Regulatory compliance
    "49_cfr_192": {"part 192", "gas pipeline safety regulations", "dot gas rules"},
    "49_cfr_195": {"part 195", "liquid pipeline safety regulations", "dot liquid rules"},

    # Property concepts
    "dominant_estate": {"easement holder", "pipeline operator estate", "superior estate"},
    "servient_estate": {"burdened estate", "underlying landowner", "surface estate"},
    "accommodation_doctrine": {"getty oil doctrine", "reasonable accommodation"},

    # Restoration terms
    "topsoil_replacement": {"topsoil restoration", "soil layer restoration", "segregated topsoil"},
    "compaction_relief": {"subsoil ripping", "deep tillage", "decompaction"},
    "reseeding": {"revegetation", "pasture restoration", "grass replanting"},
}


# ============================================================================
# ABBREVIATION MAP
# ============================================================================

ABBREVIATION_MAP: Dict[str, str] = {
    # ROW
    "row": "right of way",
    "r-o-w": "right of way",
    "r.o.w.": "right of way",
    "r/w": "right of way",

    # Federal agencies
    "ferc": "federal energy regulatory commission",
    "rrc": "railroad commission of texas",
    "txdot": "texas department of transportation",
    "usace": "us army corps of engineers",
    "epa": "environmental protection agency",
    "blm": "bureau of land management",

    # Legal
    "fmv": "fair market value",
    "sua": "surface use agreement",
    "hb": "house bill",
    "sb": "senate bill",

    # Engineering
    "hdd": "horizontal directional drilling",
    "od": "outer diameter",
    "id": "inner diameter",
    "psi": "pounds per square inch",
    "bpd": "barrels per day",
    "mcf": "thousand cubic feet",
    "mmcf": "million cubic feet",

    # Standards
    "asme": "american society of mechanical engineers",
    "api": "american petroleum institute",
    "nesc": "national electrical safety code",
    "nfpa": "national fire protection association",

    # Companies
    "et": "energy transfer",
    "etp": "energy transfer partners",
    "kmi": "kinder morgan",
    "paa": "plains all american",
    "epp": "enterprise products partners",

    # Railroad
    "bnsf": "burlington northern santa fe",
    "up": "union pacific",
    "kcs": "kansas city southern",
    "cn": "canadian national",

    # Legal citations
    "usc": "united states code",
    "cfr": "code of federal regulations",
    "tx": "texas",
    "nrc": "natural resources code",
    "cprc": "civil practice and remedies code",

    # Construction
    "cip": "cast iron pipe",
    "pvc": "polyvinyl chloride",
    "hdpe": "high density polyethylene",
    "frp": "fiberglass reinforced plastic",
}


# ============================================================================
# OPERATOR ALIAS MAP
# ============================================================================

OPERATOR_ALIAS_MAP: Dict[str, str] = {
    # Energy Transfer
    "energy transfer": "energy_transfer",
    "et": "energy_transfer",
    "etp": "energy_transfer",
    "energy transfer partners": "energy_transfer",
    "sunoco": "energy_transfer",
    "sunoco logistics": "energy_transfer",

    # Enterprise Products
    "enterprise": "enterprise_products",
    "enterprise products": "enterprise_products",
    "epp": "enterprise_products",
    "epd": "enterprise_products",

    # Kinder Morgan
    "kinder morgan": "kinder_morgan",
    "kmi": "kinder_morgan",
    "kinder": "kinder_morgan",

    # Plains All American
    "plains": "plains_all_american",
    "plains all american": "plains_all_american",
    "paa": "plains_all_american",
    "plains pipeline": "plains_all_american",

    # Williams Companies
    "williams": "williams_companies",
    "williams companies": "williams_companies",
    "williams partners": "williams_companies",

    # ONEOK
    "oneok": "oneok",
    "oneok partners": "oneok",

    # Magellan Midstream
    "magellan": "magellan_midstream",
    "magellan midstream": "magellan_midstream",
    "mmp": "magellan_midstream",

    # Targa Resources
    "targa": "targa_resources",
    "targa resources": "targa_resources",

    # DCP Midstream
    "dcp": "dcp_midstream",
    "dcp midstream": "dcp_midstream",

    # Western Midstream
    "western": "western_midstream",
    "western midstream": "western_midstream",
    "wes": "western_midstream",
}


# ============================================================================
# INSTRUMENT TYPE MAP
# ============================================================================

INSTRUMENT_TYPE_MAP: Dict[str, str] = {
    # Easement types
    "pipeline easement": "easement",
    "easement agreement": "easement",
    "right of way deed": "easement",
    "perpetual easement": "easement",
    "temporary easement": "temporary_easement",
    "construction easement": "temporary_easement",

    # Fee simple
    "warranty deed": "deed",
    "special warranty deed": "deed",
    "quitclaim deed": "deed",
    "fee simple deed": "deed",

    # Agreements
    "surface use agreement": "surface_agreement",
    "crossing agreement": "crossing_agreement",
    "railroad crossing agreement": "crossing_agreement",
    "highway crossing agreement": "crossing_agreement",

    # Condemnation
    "condemnation petition": "condemnation",
    "eminent domain proceeding": "condemnation",
    "commissioners award": "condemnation_award",

    # Amendments
    "easement amendment": "amendment",
    "supplemental easement": "amendment",
    "easement modification": "amendment",
}


# ============================================================================
# TEXAS PERMIAN COUNTIES
# ============================================================================

TEXAS_PERMIAN_COUNTIES: Set[str] = {
    "andrews", "borden", "crane", "crockett", "dawson", "ector",
    "gaines", "glasscock", "howard", "irion", "lea", "loving",
    "martin", "midland", "mitchell", "pecos", "reagan", "reeves",
    "scurry", "sterling", "terrell", "upton", "ward", "winkler", "yoakum",
}


# ============================================================================
# ROW ENGINEERING TERMS
# ============================================================================

ROW_ENGINEERING_TERMS: Dict[str, str] = {
    # Depth terms
    "depth of cover": "vertical distance from surface to top of pipe",
    "minimum depth": "regulatory minimum burial depth (36-48 inches typical)",
    "depth below rail": "depth below lowest railroad rail (6-10 feet minimum)",

    # Width terms
    "easement width": "horizontal width of ROW corridor",
    "construction corridor": "temporary workspace width during construction",
    "permanent row": "post-construction easement width",

    # Crossing terms
    "perpendicular crossing": "90-degree angle crossing (preferred)",
    "oblique crossing": "non-perpendicular crossing (<90 degrees)",
    "bore path": "subsurface drill path for HDD/boring",

    # Safety terms
    "setback": "minimum distance from structure/building to pipeline",
    "clearance": "minimum vertical distance from overhead line to ground",
    "buffer zone": "area around pipeline with restricted activities",
}


# ============================================================================
# NORMALIZATION FUNCTIONS
# ============================================================================

def normalize_query(query: str) -> str:
    """
    Normalize query string: lowercase, expand abbreviations, resolve synonyms.

    Args:
        query: Raw query string

    Returns:
        Normalized query string
    """
    query_lower = query.lower().strip()

    # Expand abbreviations
    query_expanded = expand_abbreviations(query_lower)

    # Resolve synonyms (replace with canonical terms)
    query_normalized = resolve_synonyms(query_expanded)

    return query_normalized


def expand_abbreviations(text: str) -> str:
    """
    Expand known abbreviations to full terms.

    Args:
        text: Input text with abbreviations

    Returns:
        Text with abbreviations expanded
    """
    # Sort by length descending (expand longer abbreviations first)
    abbrevs = sorted(ABBREVIATION_MAP.items(), key=lambda x: len(x[0]), reverse=True)

    result = text
    for abbrev, full_term in abbrevs:
        # Word boundary matching (avoid partial matches)
        pattern = r'\b' + re.escape(abbrev) + r'\b'
        result = re.sub(pattern, full_term, result, flags=re.IGNORECASE)

    return result


def resolve_synonyms(text: str) -> str:
    """
    Replace synonyms with canonical terms.

    Args:
        text: Input text with potential synonyms

    Returns:
        Text with synonyms resolved to canonical terms
    """
    result = text

    for canonical, synonyms in SEMANTIC_MAP.items():
        for synonym in synonyms:
            # Word boundary matching
            pattern = r'\b' + re.escape(synonym) + r'\b'
            result = re.sub(pattern, canonical, result, flags=re.IGNORECASE)

    return result


def resolve_operator(operator_name: str) -> str:
    """
    Resolve operator name/alias to canonical operator ID.

    Args:
        operator_name: Operator name or alias

    Returns:
        Canonical operator ID (or original if not found)
    """
    operator_lower = operator_name.lower().strip()
    return OPERATOR_ALIAS_MAP.get(operator_lower, operator_name)


def classify_instrument_type(instrument_desc: str) -> str:
    """
    Classify instrument description to standard type.

    Args:
        instrument_desc: Instrument description (e.g., "Pipeline Easement Agreement")

    Returns:
        Standard instrument type (e.g., "easement")
    """
    desc_lower = instrument_desc.lower().strip()

    for pattern, inst_type in INSTRUMENT_TYPE_MAP.items():
        if pattern in desc_lower:
            return inst_type

    # Default: return original
    return instrument_desc


def extract_row_dimensions(text: str) -> Dict[str, Any]:
    """
    Extract ROW dimensions (width, depth) from text.

    Args:
        text: Text containing ROW dimensions

    Returns:
        Dict with extracted dimensions
    """
    dimensions = {}

    # Width patterns
    width_patterns = [
        r'(\d+)\s*(?:foot|ft|feet|\')\s*(?:wide|width)',
        r'width\s*(?:of\s*)?(\d+)\s*(?:foot|ft|feet|\')',
        r'(\d+)\s*(?:foot|ft|feet|\')\s*row',
        r'(\d+)\s*(?:foot|ft|feet|\')\s*easement',
    ]

    for pattern in width_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            dimensions['width_feet'] = int(match.group(1))
            break

    # Depth patterns
    depth_patterns = [
        r'(\d+)\s*(?:inch|in|inches|")\s*(?:deep|depth)',
        r'depth\s*(?:of\s*)?(\d+)\s*(?:inch|in|inches|")',
        r'minimum\s*depth\s*(\d+)\s*(?:inch|in|inches|")',
        r'(\d+)\s*(?:foot|ft|feet|\')\s*(?:below|depth)',
    ]

    for pattern in depth_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = int(match.group(1))
            # Detect if feet or inches based on pattern
            if 'foot' in pattern or 'ft' in pattern or "'" in pattern:
                dimensions['depth_feet'] = value
                dimensions['depth_inches'] = value * 12
            else:
                dimensions['depth_inches'] = value
                dimensions['depth_feet'] = value / 12
            break

    return dimensions


def extract_compensation_amount(text: str) -> Dict[str, Any]:
    """
    Extract compensation amounts from text.

    Args:
        text: Text containing compensation amounts

    Returns:
        Dict with extracted amounts
    """
    compensation = {}

    # Dollar amount patterns
    amount_patterns = [
        r'\$\s*([\d,]+(?:\.\d{2})?)',
        r'([\d,]+(?:\.\d{2})?)\s*dollars?',
    ]

    for pattern in amount_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            # Convert to float, remove commas
            amounts = [float(m.replace(',', '')) for m in matches]
            compensation['amounts'] = amounts
            compensation['total'] = sum(amounts)
            break

    # Per-acre patterns
    per_acre_patterns = [
        r'\$\s*([\d,]+(?:\.\d{2})?)\s*(?:per|/)?\s*acre',
        r'([\d,]+(?:\.\d{2})?)\s*dollars?\s*(?:per|/)?\s*acre',
    ]

    for pattern in per_acre_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            compensation['per_acre'] = float(match.group(1).replace(',', ''))
            break

    return compensation


def extract_pipeline_specs(text: str) -> Dict[str, Any]:
    """
    Extract pipeline specifications (diameter, material, pressure) from text.

    Args:
        text: Text containing pipeline specs

    Returns:
        Dict with extracted specs
    """
    specs = {}

    # Diameter patterns
    diameter_patterns = [
        r'(\d+)\s*(?:inch|in|")\s*(?:diameter|pipe|pipeline)',
        r'(\d+)"',
        r'diameter\s*(?:of\s*)?(\d+)\s*(?:inch|in|")',
    ]

    for pattern in diameter_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            specs['diameter_inches'] = int(match.group(1))
            break

    # Pressure patterns
    pressure_patterns = [
        r'(\d+)\s*psi',
        r'(\d+)\s*pounds\s*per\s*square\s*inch',
        r'pressure\s*(?:of\s*)?(\d+)\s*psi',
    ]

    for pattern in pressure_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            specs['pressure_psi'] = int(match.group(1))
            break

    # Material patterns
    material_keywords = {
        'steel': 'steel',
        'carbon steel': 'carbon_steel',
        'stainless steel': 'stainless_steel',
        'pvc': 'pvc',
        'hdpe': 'hdpe',
        'fiberglass': 'frp',
        'cast iron': 'cast_iron',
    }

    text_lower = text.lower()
    for keyword, material in material_keywords.items():
        if keyword in text_lower:
            specs['material'] = material
            break

    return specs


def is_permian_county(county: str) -> bool:
    """
    Check if county is in Texas Permian Basin.

    Args:
        county: County name

    Returns:
        True if Permian county, False otherwise
    """
    return county.lower().strip() in TEXAS_PERMIAN_COUNTIES


def get_all_canonical_terms() -> List[str]:
    """Get list of all canonical terms."""
    return list(SEMANTIC_MAP.keys())


def semantic_health() -> Dict[str, Any]:
    """Get semantic normalization health statistics."""
    return {
        "semantic_map_terms": len(SEMANTIC_MAP),
        "total_synonyms": sum(len(syns) for syns in SEMANTIC_MAP.values()),
        "abbreviations": len(ABBREVIATION_MAP),
        "operators": len(set(OPERATOR_ALIAS_MAP.values())),
        "instrument_types": len(set(INSTRUMENT_TYPE_MAP.values())),
        "permian_counties": len(TEXAS_PERMIAN_COUNTIES),
        "engineering_terms": len(ROW_ENGINEERING_TERMS),
    }


# ============================================================================
# EXPORT FOR TESTING
# ============================================================================

if __name__ == "__main__":
    # Test normalization
    test_queries = [
        "FERC certificate for ET pipeline",
        "ROW width 75 ft with HDD crossing",
        "Common carrier eminent domain in Reeves County",
        "Surface damage $2000/acre for temp easement",
    ]

    print("=== Semantic Normalization Test ===\n")
    for query in test_queries:
        normalized = normalize_query(query)
        print(f"Original: {query}")
        print(f"Normalized: {normalized}\n")

    print(f"\n=== Health Stats ===")
    import json
    print(json.dumps(semantic_health(), indent=2))
