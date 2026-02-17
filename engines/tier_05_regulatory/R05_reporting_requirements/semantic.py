"""
R05 SEMANTIC NORMALIZATION LAYER

Deterministic preprocessing for reporting requirements queries.
No vector inference. No embeddings. No auto-learning.
Pure rule-based keyword extraction and normalization.
"""

from dataclasses import dataclass
from typing import List
import re


@dataclass
class NormalizationResult:
    """Result of semantic normalization."""
    original_text: str
    normalized_text: str
    keywords: List[str]
    detected_entities: List[str]


# Domain-specific term mappings for O&G reporting
TERM_MAPPINGS = {
    "p4": "p-4",
    "p 4": "p-4",
    "form p4": "p-4",
    "w2": "w-2",
    "w 2": "w-2",
    "form w2": "w-2",
    "h10": "h-10",
    "h 10": "h-10",
    "form h10": "h-10",
    "p5": "p-5",
    "p 5": "p-5",
    "form p5": "p-5",
    "rrc": "railroad commission",
    "trc": "railroad commission",
    "texas railroad commission": "railroad commission",
    "tceq": "environmental quality",
    "epa": "environmental protection",
    "onrr": "federal reporting",
    "mms": "federal reporting",
    "glo": "state land",
    "general land office": "state land",
    "completion report": "w-2",
    "drilling permit": "w-1",
    "plugging report": "h-10",
    "production report": "p-4",
    "monthly production": "p-4",
    "organization report": "p-5",
    "change of operator": "p-5",
    "severance tax": "production tax",
    "royalty payment": "royalty",
    "tier 2": "tier ii",
    "tier two": "tier ii",
    "chemical inventory": "tier ii",
    "mechanical integrity": "mit",
    "integrity test": "mit",
    "injection well": "injection",
    "disposal well": "disposal",
    "salt water disposal": "disposal",
    "swd": "disposal",
    "enhanced recovery": "injection",
    "flaring": "gas flaring",
    "venting": "gas flaring",
}

# Keywords that indicate specific report types
REPORT_TYPE_KEYWORDS = {
    "p-4": ["p-4", "p4", "monthly production", "production report"],
    "w-2": ["w-2", "w2", "completion", "completion report"],
    "h-10": ["h-10", "h10", "plugging", "plug report"],
    "p-5": ["p-5", "p5", "organization", "change of operator"],
    "flaring": ["flaring", "venting", "flared gas"],
    "severance_tax": ["severance tax", "production tax", "comptroller"],
    "royalty": ["royalty", "royalty payment", "division order"],
    "federal": ["onrr", "federal lease", "federal reporting", "mms"],
    "state_land": ["glo", "state land", "general land office"],
    "tier_ii": ["tier ii", "tier 2", "chemical inventory", "tceq"],
    "mit": ["mechanical integrity", "integrity test", "mit"],
}


def normalize_semantics(text: str) -> NormalizationResult:
    """
    Normalize query text for consistent doctrine matching.

    Args:
        text: Raw query text

    Returns:
        NormalizationResult with normalized text and extracted keywords
    """
    # Lowercase for processing
    normalized = text.lower()

    # Apply term mappings
    for original, replacement in TERM_MAPPINGS.items():
        normalized = re.sub(r'\b' + re.escape(original) + r'\b', replacement, normalized)

    # Extract keywords (words 3+ chars, excluding stopwords)
    stopwords = {
        'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'her', 'was',
        'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'man', 'new',
        'now', 'old', 'see', 'two', 'way', 'who', 'boy', 'did', 'its', 'let', 'put',
        'say', 'she', 'too', 'use', 'what', 'when', 'which', 'have', 'from', 'they',
        'this', 'that', 'with', 'your', 'about', 'would', 'there', 'their'
    }

    words = re.findall(r'\b\w+\b', normalized)
    keywords = [w for w in words if len(w) >= 3 and w not in stopwords]

    # Detect specific entities (report types, jurisdictions, etc.)
    detected_entities = []

    # Detect report types
    for report_type, indicators in REPORT_TYPE_KEYWORDS.items():
        for indicator in indicators:
            if indicator in normalized:
                detected_entities.append(f"report_type:{report_type}")
                break

    # Detect jurisdictions
    if any(j in normalized for j in ["texas", "tx"]):
        detected_entities.append("jurisdiction:texas")
    if any(j in normalized for j in ["federal", "onrr", "blm"]):
        detected_entities.append("jurisdiction:federal")

    # Detect operator types
    if "operator" in normalized:
        detected_entities.append("entity:operator")
    if "producer" in normalized:
        detected_entities.append("entity:producer")
    if "royalty" in normalized:
        detected_entities.append("entity:royalty_owner")

    # Remove duplicates while preserving order
    keywords_unique = []
    seen = set()
    for kw in keywords:
        if kw not in seen:
            keywords_unique.append(kw)
            seen.add(kw)

    return NormalizationResult(
        original_text=text,
        normalized_text=normalized,
        keywords=keywords_unique,
        detected_entities=list(set(detected_entities))
    )


def extract_report_type(text: str) -> str:
    """
    Extract likely report type from query text.

    Returns:
        Report type identifier or "unknown"
    """
    text_lower = text.lower()

    for report_type, indicators in REPORT_TYPE_KEYWORDS.items():
        for indicator in indicators:
            if indicator in text_lower:
                return report_type

    return "unknown"


def extract_jurisdiction(text: str) -> str:
    """
    Extract jurisdiction from query text.

    Returns:
        Jurisdiction identifier (texas, federal, etc.) or "texas" as default
    """
    text_lower = text.lower()

    if any(j in text_lower for j in ["federal", "onrr", "blm", "mms"]):
        return "federal"

    if any(j in text_lower for j in ["glo", "state land"]):
        return "state_land"

    # Default to Texas for most O&G queries
    return "texas"
