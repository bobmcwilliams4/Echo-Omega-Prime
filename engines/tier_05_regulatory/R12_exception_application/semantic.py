"""
R09 - Semantic Processing Module
Query normalization and keyword extraction for plugging analysis
"""

from typing import List, Set
import re


# ═══════════════════════════════════════════════════════════════════════════
# DOMAIN-SPECIFIC TERM MAPPINGS
# ═══════════════════════════════════════════════════════════════════════════

PLUGGING_SYNONYMS = {
    "plug": ["plug", "plugging", "plugged", "cement plug", "plug back", "p&a", "abandon"],
    "cement": ["cement", "cementing", "cemented", "cement slurry", "grout"],
    "surface_casing": ["surface casing", "surface pipe", "conductor", "conductor pipe"],
    "production_casing": ["production casing", "production string", "long string", "production pipe"],
    "abandonment": ["abandonment", "abandoned", "plug and abandon", "p&a", "decommission"],
    "notification": ["notification", "notice", "notify", "filing", "report"],
    "h10": ["h10", "h-10", "plugging report", "plugging form", "form h-10"],
    "bond": ["bond", "surety", "financial security", "letter of credit", "financial assurance"],
    "orphan": ["orphan well", "inactive well", "abandoned well", "orphan"],
    "injection": ["injection well", "disposal well", "injection", "saltwater disposal", "swd"],
    "bay": ["bay", "estuary", "offshore", "state waters", "coastal waters"],
    "surface_owner": ["surface owner", "landowner", "surface estate", "fee owner"],
    "operator": ["operator", "operator of record", "designated operator", "working interest owner"],
    "verification": ["verification", "verification test", "pressure test", "cement bond log"],
    "restoration": ["restoration", "reclamation", "cleanup", "site restoration", "surface restoration"],
}

STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "as", "is", "was", "are", "were", "be",
    "been", "being", "have", "has", "had", "do", "does", "did", "will",
    "would", "could", "should", "may", "might", "must", "can", "what",
    "when", "where", "who", "which", "how", "why"
}


def normalize_query(query: str) -> str:
    """
    Normalize query to canonical forms

    Args:
        query: Raw user query

    Returns:
        Normalized query string
    """
    normalized = query.lower().strip()

    # Replace synonyms with canonical terms
    for canonical, variants in PLUGGING_SYNONYMS.items():
        for variant in variants:
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(variant) + r'\b'
            normalized = re.sub(pattern, canonical, normalized)

    # Normalize whitespace
    normalized = re.sub(r'\s+', ' ', normalized)

    return normalized


def extract_keywords(query: str) -> List[str]:
    """
    Extract meaningful keywords from query

    Args:
        query: Normalized query string

    Returns:
        List of keywords
    """
    # Split on whitespace and punctuation
    tokens = re.findall(r'\b\w+\b', query.lower())

    # Remove stop words
    keywords = [t for t in tokens if t not in STOP_WORDS and len(t) > 2]

    # Remove duplicates while preserving order
    seen: Set[str] = set()
    unique_keywords = []
    for kw in keywords:
        if kw not in seen:
            seen.add(kw)
            unique_keywords.append(kw)

    return unique_keywords


def extract_numeric_values(query: str) -> dict:
    """
    Extract numeric values from query (depths, costs, etc.)

    Args:
        query: Query string

    Returns:
        Dictionary of extracted values
    """
    values = {}

    # Extract depths (feet)
    depth_patterns = [
        r'(\d+(?:,\d{3})*(?:\.\d+)?)\s*(?:ft|feet|foot)',
        r'(\d+(?:,\d{3})*(?:\.\d+)?)\s*(?:\')',
        r'depth\s+(?:of\s+)?(\d+(?:,\d{3})*)',
    ]

    for pattern in depth_patterns:
        match = re.search(pattern, query, re.IGNORECASE)
        if match:
            depth_str = match.group(1).replace(',', '')
            values['depth'] = float(depth_str)
            break

    # Extract costs (dollars)
    cost_patterns = [
        r'\$\s*(\d+(?:,\d{3})*(?:\.\d{2})?)',
        r'(\d+(?:,\d{3})*(?:\.\d{2})?)\s*(?:dollars|usd)',
    ]

    for pattern in cost_patterns:
        match = re.search(pattern, query, re.IGNORECASE)
        if match:
            cost_str = match.group(1).replace(',', '')
            values['cost'] = float(cost_str)
            break

    # Extract time periods (days)
    time_patterns = [
        r'(\d+)\s*(?:days?|day)',
        r'(\d+)\s*(?:weeks?)',  # Convert to days
    ]

    for pattern in time_patterns:
        match = re.search(pattern, query, re.IGNORECASE)
        if match:
            if 'week' in match.group(0).lower():
                values['days'] = int(match.group(1)) * 7
            else:
                values['days'] = int(match.group(1))
            break

    return values


def identify_well_type(query: str) -> str | None:
    """
    Identify well type from query text

    Args:
        query: Query string

    Returns:
        Well type or None
    """
    query_lower = query.lower()

    # Explicit well type mentions
    if any(term in query_lower for term in ['injection well', 'injection', 'disposal well', 'swd']):
        return 'injection'
    if any(term in query_lower for term in ['oil well', 'oil and gas', 'oil & gas']):
        return 'oil'
    if any(term in query_lower for term in ['gas well', 'natural gas']):
        return 'gas'
    if any(term in query_lower for term in ['water well', 'water supply']):
        return 'water_supply'
    if any(term in query_lower for term in ['horizontal', 'horizontal well']):
        return 'horizontal'
    if any(term in query_lower for term in ['dual completion', 'multiple completion']):
        return 'multiple_completion'

    return None


def identify_regulatory_forms(query: str) -> List[str]:
    """
    Identify mentioned regulatory forms

    Args:
        query: Query string

    Returns:
        List of form identifiers
    """
    forms = []

    form_patterns = [
        (r'\bh-?10\b', 'H-10'),
        (r'\bw-?3a?\b', 'W-3A'),
        (r'\bp-?4\b', 'P-4'),
        (r'\bw-?1\b', 'W-1'),
        (r'\bg-?1\b', 'G-1'),
    ]

    query_lower = query.lower()
    for pattern, form_id in form_patterns:
        if re.search(pattern, query_lower):
            forms.append(form_id)

    return forms


def calculate_semantic_similarity(query1: str, query2: str) -> float:
    """
    Calculate simple semantic similarity between queries

    Args:
        query1: First query
        query2: Second query

    Returns:
        Similarity score 0.0-1.0
    """
    kw1 = set(extract_keywords(normalize_query(query1)))
    kw2 = set(extract_keywords(normalize_query(query2)))

    if not kw1 or not kw2:
        return 0.0

    # Jaccard similarity
    intersection = len(kw1 & kw2)
    union = len(kw1 | kw2)

    return intersection / union if union > 0 else 0.0


def expand_query_with_synonyms(query: str) -> str:
    """
    Expand query with synonyms for broader matching

    Args:
        query: Original query

    Returns:
        Expanded query string
    """
    keywords = extract_keywords(query.lower())
    expanded_terms = []

    for kw in keywords:
        # Add original keyword
        expanded_terms.append(kw)

        # Add synonyms if available
        for canonical, variants in PLUGGING_SYNONYMS.items():
            if kw in variants or kw == canonical:
                expanded_terms.extend(variants[:3])  # Limit synonyms
                break

    # Remove duplicates
    expanded_terms = list(dict.fromkeys(expanded_terms))

    return ' '.join(expanded_terms)
