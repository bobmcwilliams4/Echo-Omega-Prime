"""
LM20 Indian Land Engine — Semantic Normalization
Domain-specific term normalization for Indian/tribal land oil & gas operations.

Ensures consistent terminology across queries:
- Trust vs restricted vs fee land
- Allotted vs tribal ownership
- BIA vs Bureau of Indian Affairs
- IMLA vs IMDA vs HEARTH Act
- Fractionation vs heirship
- Secretarial approval vs BIA approval
- ROW vs right-of-way

Author: ECHO OMEGA PRIME
Engine: LM20
"""

from dataclasses import dataclass
from typing import List, Dict, Set, Optional
import re


@dataclass
class NormalizationResult:
    """Result of semantic normalization."""
    original_query: str
    normalized_query: str
    applied_rules: List[str]
    canonical_terms: List[str]
    domain: str = "indian_land"


# ==============================================================================
# NORMALIZATION RULES — INDIAN LAND DOMAIN
# ==============================================================================

# Synonym mappings: variant → canonical
SYNONYM_MAP = {
    # Trust status terminology
    "trust land": "trust_land",
    "trust status": "trust_status",
    "restricted land": "restricted_land",
    "restricted status": "restricted_status",
    "fee land": "fee_land",
    "fee patent": "fee_patent",
    "fee simple": "fee_land",
    "in trust": "trust_status",
    "held in trust": "trust_status",

    # Allotment terminology
    "allotted land": "allotted_land",
    "allotment": "allotment",
    "allottee": "allottee",
    "individual indian": "individual_indian",
    "tribal land": "tribal_land",
    "tribal ownership": "tribal_ownership",
    "communal land": "tribal_land",
    "reservation land": "reservation_land",

    # BIA terminology
    "bia": "bia",
    "bureau of indian affairs": "bia",
    "bureau": "bia",
    "doi": "doi",
    "department of interior": "doi",
    "secretary": "secretary",
    "secretarial approval": "secretarial_approval",
    "bia approval": "bia_approval",
    "superintendent": "superintendent",
    "regional director": "regional_director",

    # Leasing frameworks
    "imla": "imla",
    "indian mineral leasing act": "imla",
    "imda": "imda",
    "indian mineral development act": "imda",
    "hearth act": "hearth_act",
    "hearth": "hearth_act",
    "self-governance": "self_governance",
    "self governance": "self_governance",
    "self-determination": "self_determination",
    "self determination": "self_determination",

    # Regulations
    "25 cfr 211": "25_cfr_211",
    "25 cfr part 211": "25_cfr_211",
    "part 211": "25_cfr_211",
    "25 cfr 212": "25_cfr_212",
    "25 cfr part 212": "25_cfr_212",
    "part 212": "25_cfr_212",
    "25 cfr 225": "25_cfr_225",
    "25 cfr part 225": "25_cfr_225",
    "part 225": "25_cfr_225",
    "25 cfr 169": "25_cfr_169",
    "25 cfr part 169": "25_cfr_169",
    "part 169": "25_cfr_169",
    "30 cfr 1206": "30_cfr_1206",

    # Fractionation
    "fractionation": "fractionation",
    "fractionated": "fractionated",
    "heirship": "heirship",
    "heirs": "heirs",
    "probate": "probate",
    "undivided interest": "undivided_interest",
    "co-owner": "co_owner",
    "co owner": "co_owner",
    "majority in interest": "majority_in_interest",
    "majority-in-interest": "majority_in_interest",

    # Land consolidation
    "ilca": "ilca",
    "indian land consolidation act": "ilca",
    "aipra": "aipra",
    "american indian probate reform act": "aipra",
    "cobell": "cobell",
    "cobell settlement": "cobell_settlement",
    "buy-back program": "buyback_program",
    "buy back program": "buyback_program",
    "buyback": "buyback_program",

    # Ownership patterns
    "checkerboard": "checkerboard",
    "checkerboard ownership": "checkerboard",
    "mixed ownership": "mixed_ownership",
    "interspersed": "interspersed",
    "split estate": "split_estate",
    "surface rights": "surface_rights",
    "mineral rights": "mineral_rights",

    # Rights-of-way
    "row": "row",
    "right-of-way": "row",
    "right of way": "row",
    "easement": "easement",
    "pipeline": "pipeline",
    "access": "access",

    # Sovereign immunity
    "sovereign immunity": "sovereign_immunity",
    "immunity": "sovereign_immunity",
    "waiver": "immunity_waiver",
    "sue tribe": "tribal_lawsuit",
    "tribal court": "tribal_court",

    # Environmental
    "nepa": "nepa",
    "environmental assessment": "environmental_assessment",
    "ea": "environmental_assessment",
    "eis": "environmental_impact_statement",
    "environmental impact statement": "environmental_impact_statement",
    "nhpa": "nhpa",
    "section 106": "nhpa_section_106",
    "cultural resources": "cultural_resources",
    "nagpra": "nagpra",
    "tas": "treatment_as_state",
    "treatment as state": "treatment_as_state",

    # Royalties
    "onrr": "onrr",
    "office of natural resources revenue": "onrr",
    "iim": "iim",
    "individual indian money": "iim",
    "iim account": "iim_account",
    "royalty": "royalty",
    "royalties": "royalty",
    "valuation": "valuation",
    "fogrma": "fogrma",

    # Historical
    "dawes act": "dawes_act",
    "general allotment act": "dawes_act",
    "burke act": "burke_act",
    "ira": "ira",
    "indian reorganization act": "ira",
    "nonintercourse act": "nonintercourse_act",
    "25 usc 177": "nonintercourse_act",

    # Jurisdiction
    "montana doctrine": "montana_doctrine",
    "montana test": "montana_doctrine",
    "tribal jurisdiction": "tribal_jurisdiction",
    "federal jurisdiction": "federal_jurisdiction",
    "state jurisdiction": "state_jurisdiction",
}


# Domain-specific patterns
DOMAIN_PATTERNS = {
    "indian_land": [
        "trust", "restricted", "allot", "tribal", "bia", "secretar",
        "imla", "imda", "hearth", "fraction", "probate", "sovereign",
        "nepa", "onrr", "iim", "dawes", "checkerboard", "row"
    ],
    "leasing": [
        "lease", "consent", "approval", "imla", "imda", "hearth",
        "25 cfr 211", "25 cfr 212", "bonus", "royalty"
    ],
    "title": [
        "trust", "fee", "patent", "allot", "tribal", "ownership",
        "undivided interest", "fraction", "title"
    ],
    "environmental": [
        "nepa", "ea", "eis", "nhpa", "section 106", "cultural",
        "nagpra", "tas", "tribal environmental"
    ],
    "royalty": [
        "onrr", "royalty", "iim", "valuation", "30 cfr 1206",
        "fogrma", "reporting"
    ],
}


# Abbreviation expansions
ABBREVIATIONS = {
    "BIA": "Bureau of Indian Affairs",
    "DOI": "Department of Interior",
    "IMLA": "Indian Mineral Leasing Act",
    "IMDA": "Indian Mineral Development Act",
    "HEARTH": "Helping Expedite and Advance Responsible Tribal Homeownership Act",
    "ILCA": "Indian Land Consolidation Act",
    "AIPRA": "American Indian Probate Reform Act",
    "ROW": "right-of-way",
    "NEPA": "National Environmental Policy Act",
    "NHPA": "National Historic Preservation Act",
    "NAGPRA": "Native American Graves Protection and Repatriation Act",
    "TAS": "Treatment as State",
    "ONRR": "Office of Natural Resources Revenue",
    "IIM": "Individual Indian Money",
    "FOGRMA": "Federal Oil and Gas Royalty Management Act",
    "IRA": "Indian Reorganization Act",
    "CFR": "Code of Federal Regulations",
    "USC": "United States Code",
}


# Common misspellings and variants
SPELLING_VARIANTS = {
    "alloted": "allotted",
    "allottment": "allotment",
    "tribal soveriegnty": "tribal sovereignty",
    "sovreign": "sovereign",
    "fractional": "fractionated",
    "right of ways": "right-of-way",
    "rights of way": "right-of-way",
    "LTRO": "Land Title and Records Office",
}


# ==============================================================================
# NORMALIZATION FUNCTIONS
# ==============================================================================

def normalize_semantics(query: str) -> NormalizationResult:
    """
    Normalize query using Indian land domain semantics.

    Steps:
    1. Lowercase and clean whitespace
    2. Expand abbreviations
    3. Fix common misspellings
    4. Apply synonym mapping
    5. Identify domain
    6. Extract canonical terms
    """
    original = query
    applied_rules = []

    # Step 1: Clean
    normalized = query.lower().strip()
    normalized = re.sub(r'\s+', ' ', normalized)

    # Step 2: Expand abbreviations (case-insensitive)
    for abbr, expansion in ABBREVIATIONS.items():
        pattern = r'\b' + re.escape(abbr) + r'\b'
        if re.search(pattern, query, re.IGNORECASE):
            normalized = re.sub(pattern, expansion.lower(), normalized, flags=re.IGNORECASE)
            applied_rules.append(f"Expanded {abbr} → {expansion}")

    # Step 3: Fix misspellings
    for variant, correct in SPELLING_VARIANTS.items():
        if variant.lower() in normalized:
            normalized = normalized.replace(variant.lower(), correct.lower())
            applied_rules.append(f"Corrected {variant} → {correct}")

    # Step 4: Apply synonym mapping
    canonical_terms = []
    for synonym, canonical in SYNONYM_MAP.items():
        if synonym in normalized:
            # Replace phrase with canonical term
            normalized = normalized.replace(synonym, canonical)
            canonical_terms.append(canonical)
            applied_rules.append(f"Mapped {synonym} → {canonical}")

    # Step 5: Identify domain
    domain = identify_domain(normalized)

    # Step 6: Deduplicate canonical terms
    canonical_terms = sorted(set(canonical_terms))

    return NormalizationResult(
        original_query=original,
        normalized_query=normalized,
        applied_rules=applied_rules,
        canonical_terms=canonical_terms,
        domain=domain
    )


def identify_domain(normalized_query: str) -> str:
    """Identify most relevant domain for query."""
    scores = {}
    for domain_name, patterns in DOMAIN_PATTERNS.items():
        score = sum(1 for pattern in patterns if pattern in normalized_query)
        if score > 0:
            scores[domain_name] = score

    if not scores:
        return "indian_land"  # default

    return max(scores, key=scores.get)


def get_all_domains() -> List[str]:
    """Return list of all domain names."""
    return list(DOMAIN_PATTERNS.keys())


def get_synonym_count() -> int:
    """Return total number of synonym mappings."""
    return len(SYNONYM_MAP)


def get_canonical_count() -> int:
    """Return number of unique canonical terms."""
    return len(set(SYNONYM_MAP.values()))


def get_synonyms_for_canonical(canonical: str) -> List[str]:
    """Return all synonyms that map to a canonical term."""
    return [syn for syn, can in SYNONYM_MAP.items() if can == canonical]


def expand_abbreviation(abbr: str) -> Optional[str]:
    """Expand abbreviation if known."""
    return ABBREVIATIONS.get(abbr.upper())


# ==============================================================================
# DOMAIN-SPECIFIC QUERY ENHANCEMENT
# ==============================================================================

def enhance_query(query: str) -> str:
    """
    Enhance query with domain-specific expansions.

    Example:
    - "BIA approval" → "Bureau of Indian Affairs approval secretarial approval"
    - "IMDA" → "Indian Mineral Development Act joint venture"
    """
    enhanced = query

    # Add expansions for key concepts
    enhancements = {
        "trust status": "trust status restricted status inalienable secretarial approval",
        "allotted": "allotted individual indian fractionated undivided interest",
        "tribal": "tribal communal tribal council resolution",
        "bia approval": "BIA approval secretarial approval superintendent regional director",
        "imda": "IMDA Indian Mineral Development Act joint venture alternative agreement",
        "imla": "IMLA Indian Mineral Leasing Act traditional lease",
        "hearth": "HEARTH Act self-governance tribal regulations waiver",
        "fractionation": "fractionation heirship probate undivided interest co-owners",
        "row": "right-of-way easement pipeline access 25 CFR 169",
    }

    for trigger, expansion in enhancements.items():
        if trigger.lower() in query.lower():
            enhanced += f" {expansion}"

    return enhanced


def extract_key_entities(query: str) -> Dict[str, List[str]]:
    """
    Extract key entities from query.

    Returns:
        dict with keys: regulations, statutes, concepts, actions
    """
    entities = {
        "regulations": [],
        "statutes": [],
        "concepts": [],
        "actions": []
    }

    # Extract CFR citations
    cfr_pattern = r'\b(\d+)\s+CFR\s+(Part\s+)?(\d+)\b'
    for match in re.finditer(cfr_pattern, query, re.IGNORECASE):
        entities["regulations"].append(f"{match.group(1)} CFR {match.group(3)}")

    # Extract USC citations
    usc_pattern = r'\b(\d+)\s+U\.?S\.?C\.?\s+(\d+[a-z]?)\b'
    for match in re.finditer(usc_pattern, query, re.IGNORECASE):
        entities["statutes"].append(f"{match.group(1)} USC {match.group(2)}")

    # Extract concepts
    concept_keywords = [
        "trust", "restricted", "fee", "allotted", "tribal", "fractionation",
        "sovereign immunity", "right-of-way", "split estate", "checkerboard"
    ]
    for concept in concept_keywords:
        if concept in query.lower():
            entities["concepts"].append(concept)

    # Extract actions
    action_keywords = [
        "lease", "approval", "consent", "waiver", "permit", "grant", "valuation"
    ]
    for action in action_keywords:
        if action in query.lower():
            entities["actions"].append(action)

    return entities
