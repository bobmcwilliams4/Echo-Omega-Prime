"""
R04 Violation Detector — Semantic Normalization

Domain-specific term normalization for regulatory violation detection.
Maps variant terms, abbreviations, and synonyms to canonical forms.

Examples:
  "production exceeded allowable" → "overproduction_violation"
  "late form p-4" → "late_production_report"
  "h2s detector missing" → "h2s_equipment_violation"
"""

from __future__ import annotations

import re
from typing import Dict, List, Set


# ═══════════════════════════════════════════════════════════════════════════════
# TERM NORMALIZATION MAPS
# ═══════════════════════════════════════════════════════════════════════════════

VIOLATION_TYPE_SYNONYMS: Dict[str, str] = {
    # Operational violations
    "spacing violation": "spacing_violation",
    "well too close": "spacing_violation",
    "setback violation": "spacing_violation",
    "offset violation": "spacing_violation",
    "exceeded allowable": "overproduction_violation",
    "overproduction": "overproduction_violation",
    "over allowable": "overproduction_violation",
    "proration violation": "overproduction_violation",
    "unauthorized injection": "unauthorized_injection",
    "unpermitted injection": "unauthorized_injection",
    "injection without permit": "unauthorized_injection",
    "no uic permit": "unauthorized_injection",
    "flaring violation": "flaring_violation",
    "excess flaring": "flaring_violation",
    "unauthorized flaring": "flaring_violation",

    # Environmental violations
    "spill": "unauthorized_discharge",
    "discharge": "unauthorized_discharge",
    "release": "unauthorized_discharge",
    "leak": "unauthorized_discharge",
    "overflow": "pit_violation",
    "pit overflow": "pit_violation",
    "unlined pit": "pit_violation",
    "freeboard violation": "pit_violation",
    "tank leak": "tank_leak",
    "storage tank leak": "tank_leak",
    "containment failure": "tank_leak",

    # Safety violations
    "h2s violation": "h2s_equipment_violation",
    "hydrogen sulfide": "h2s_equipment_violation",
    "sour gas violation": "h2s_equipment_violation",
    "missing h2s detector": "h2s_equipment_violation",
    "bop failure": "bop_violation",
    "blowout preventer": "bop_violation",
    "bop not tested": "bop_violation",
    "well control violation": "bop_violation",

    # Reporting violations
    "late p-4": "late_production_report",
    "late p4": "late_production_report",
    "late form p-4": "late_production_report",
    "production report late": "late_production_report",
    "missing w-2": "missing_completion_report",
    "late w2": "missing_completion_report",
    "w-2 not filed": "missing_completion_report",
    "completion report missing": "missing_completion_report",

    # Financial violations
    "lapsed bond": "lapsed_bond",
    "expired bond": "lapsed_bond",
    "insufficient bond": "insufficient_bond_coverage",
    "bond coverage exceeded": "insufficient_bond_coverage",
    "no bond": "lapsed_bond",

    # Administrative violations
    "no permit": "unpermitted_activity",
    "permit violation": "permit_violation",
    "permit expired": "expired_permit",
    "inspection obstruction": "inspection_obstruction",
    "denied entry": "inspection_obstruction"
}


REGULATORY_AUTHORITY_SYNONYMS: Dict[str, str] = {
    "railroad commission": "RRC",
    "texas railroad commission": "RRC",
    "commission": "RRC",
    "tceq": "TCEQ",
    "texas commission on environmental quality": "TCEQ",
    "environmental quality": "TCEQ",
    "epa": "EPA",
    "environmental protection agency": "EPA",
    "federal epa": "EPA",
    "osha": "OSHA",
    "occupational safety": "OSHA",
    "dot": "DOT",
    "department of transportation": "DOT",
    "phmsa": "PHMSA",
    "pipeline safety": "PHMSA"
}


ENFORCEMENT_ACTION_SYNONYMS: Dict[str, str] = {
    "nov": "Notice_of_Violation",
    "notice of violation": "Notice_of_Violation",
    "violation notice": "Notice_of_Violation",
    "compliance order": "Compliance_Order",
    "order": "Compliance_Order",
    "penalty": "Administrative_Penalty",
    "fine": "Administrative_Penalty",
    "administrative penalty": "Administrative_Penalty",
    "cease and desist": "Cease_and_Desist",
    "stop work order": "Cease_and_Desist",
    "shutdown": "Cease_and_Desist",
    "permit suspension": "Permit_Suspension",
    "permit revocation": "Permit_Revocation",
    "criminal referral": "Criminal_Referral",
    "plugging order": "Plugging_Order",
    "bond call": "Financial_Assurance_Call"
}


SEVERITY_LEVEL_SYNONYMS: Dict[str, str] = {
    "minor": "minor",
    "small": "minor",
    "de minimis": "minor",
    "moderate": "moderate",
    "medium": "moderate",
    "serious": "serious",
    "major": "serious",
    "severe": "severe",
    "egregious": "severe",
    "catastrophic": "catastrophic",
    "willful": "catastrophic"
}


REGULATORY_CITATION_PATTERNS: List[tuple] = [
    (r"16\s*TAC\s*[§§]*\s*(\d+\.\d+)", r"16 TAC §\1"),  # 16 TAC §3.37
    (r"30\s*TAC\s*[§§]*\s*(\d+\.\d+)", r"30 TAC §\1"),  # 30 TAC §281.25
    (r"40\s*CFR\s*[§§]*\s*(\d+\.\d+)", r"40 CFR §\1"),  # 40 CFR §112.8
    (r"Rule\s*(\d+)", r"Statewide Rule \1"),  # Rule 37 → Statewide Rule 37
    (r"TWC\s*[§§]*\s*(\d+\.\d+)", r"Texas Water Code §\1"),  # TWC §26.121
    (r"TNRC\s*[§§]*\s*(\d+\.\d+)", r"Texas Natural Resources Code §\1")  # TNRC §85.046
]


# ═══════════════════════════════════════════════════════════════════════════════
# NORMALIZATION FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def normalize_violation_type(raw_text: str) -> str:
    """
    Normalize violation type description to canonical form.

    Args:
        raw_text: Raw violation description (e.g., "well too close to lease line")

    Returns:
        Canonical violation type (e.g., "spacing_violation")
    """
    text_lower = raw_text.lower().strip()

    # Direct lookup
    if text_lower in VIOLATION_TYPE_SYNONYMS:
        return VIOLATION_TYPE_SYNONYMS[text_lower]

    # Partial match (longest match wins)
    matches = []
    for synonym, canonical in VIOLATION_TYPE_SYNONYMS.items():
        if synonym in text_lower:
            matches.append((len(synonym), canonical))

    if matches:
        matches.sort(reverse=True)
        return matches[0][1]

    # No match — return cleaned original
    return text_lower.replace(" ", "_")


def normalize_regulatory_authority(raw_text: str) -> str:
    """Normalize regulatory authority to standard abbreviation."""
    text_lower = raw_text.lower().strip()

    if text_lower in REGULATORY_AUTHORITY_SYNONYMS:
        return REGULATORY_AUTHORITY_SYNONYMS[text_lower]

    # Partial match
    for synonym, canonical in REGULATORY_AUTHORITY_SYNONYMS.items():
        if synonym in text_lower:
            return canonical

    return raw_text.upper()


def normalize_enforcement_action(raw_text: str) -> str:
    """Normalize enforcement action to standard form."""
    text_lower = raw_text.lower().strip()

    if text_lower in ENFORCEMENT_ACTION_SYNONYMS:
        return ENFORCEMENT_ACTION_SYNONYMS[text_lower]

    for synonym, canonical in ENFORCEMENT_ACTION_SYNONYMS.items():
        if synonym in text_lower:
            return canonical

    return raw_text.title().replace(" ", "_")


def normalize_severity_level(raw_text: str) -> str:
    """Normalize severity level to standard tier."""
    text_lower = raw_text.lower().strip()

    if text_lower in SEVERITY_LEVEL_SYNONYMS:
        return SEVERITY_LEVEL_SYNONYMS[text_lower]

    return "moderate"  # default


def normalize_regulatory_citation(raw_citation: str) -> str:
    """
    Normalize regulatory citation to standard format.

    Examples:
        "16 tac 3.37" → "16 TAC §3.37"
        "Rule 8" → "Statewide Rule 8"
        "40cfr112" → "40 CFR §112"
    """
    citation = raw_citation.strip()

    for pattern, replacement in REGULATORY_CITATION_PATTERNS:
        citation = re.sub(pattern, replacement, citation, flags=re.IGNORECASE)

    return citation


def extract_keywords(text: str) -> List[str]:
    """
    Extract regulatory violation keywords from text.

    Returns normalized keywords for doctrine cache lookup.
    """
    keywords: Set[str] = set()
    text_lower = text.lower()

    # Extract violation types
    for synonym in VIOLATION_TYPE_SYNONYMS.keys():
        if synonym in text_lower:
            keywords.add(VIOLATION_TYPE_SYNONYMS[synonym])

    # Extract regulatory authorities
    for synonym in REGULATORY_AUTHORITY_SYNONYMS.keys():
        if synonym in text_lower:
            keywords.add(REGULATORY_AUTHORITY_SYNONYMS[synonym])

    # Extract enforcement actions
    for synonym in ENFORCEMENT_ACTION_SYNONYMS.keys():
        if synonym in text_lower:
            keywords.add(ENFORCEMENT_ACTION_SYNONYMS[synonym])

    # Common violation-related terms
    common_terms = [
        "penalty", "fine", "violation", "compliance", "enforcement",
        "permit", "bond", "report", "inspection", "safety", "environmental"
    ]
    for term in common_terms:
        if term in text_lower:
            keywords.add(term)

    return sorted(list(keywords))


def normalize_query(raw_query: str) -> str:
    """
    Normalize entire query for semantic search.

    Applies all normalization rules to produce clean, searchable text.
    """
    # Normalize regulatory citations
    query = normalize_regulatory_citation(raw_query)

    # Normalize violation types (replace in context)
    for synonym, canonical in VIOLATION_TYPE_SYNONYMS.items():
        if synonym in query.lower():
            query = re.sub(
                re.escape(synonym),
                canonical.replace("_", " "),
                query,
                flags=re.IGNORECASE
            )

    # Normalize authorities
    for synonym, canonical in REGULATORY_AUTHORITY_SYNONYMS.items():
        if synonym in query.lower():
            query = re.sub(
                re.escape(synonym),
                canonical,
                query,
                flags=re.IGNORECASE
            )

    return query.strip()
