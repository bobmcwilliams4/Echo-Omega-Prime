"""
TX13 Real Estate Tax Engine - Semantic Normalization Layer
Deterministic preprocessing for real estate tax terminology.

This module normalizes user queries into canonical forms before
doctrine lookup. It is purely deterministic — no probabilistic
models, no embeddings, no auto-learning at this stage.

Author: ECHO OMEGA PRIME
Engine: TX13 Real Estate Tax
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple

from loguru import logger


# =============================================================================
# NORMALIZATION RESULT
# =============================================================================

@dataclass
class NormalizationResult:
    """Result of semantic normalization on a query."""
    original: str
    normalized: str
    extracted_irc_sections: List[str] = field(default_factory=list)
    extracted_entities: List[str] = field(default_factory=list)
    detected_topics: List[str] = field(default_factory=list)
    confidence: float = 1.0
    transformations_applied: List[str] = field(default_factory=list)
    dollar_amounts: List[float] = field(default_factory=list)
    time_periods: List[str] = field(default_factory=list)
    property_types: List[str] = field(default_factory=list)


# =============================================================================
# CANONICAL TERM MAPS
# =============================================================================

TERM_SYNONYMS: Dict[str, str] = {
    # 1031 Exchange terms
    "like kind exchange": "like-kind exchange",
    "like-kind": "like-kind exchange",
    "1031 exchange": "like-kind exchange",
    "section 1031": "like-kind exchange",
    "starker exchange": "like-kind exchange",
    "starker trust": "like-kind exchange",
    "deferred exchange": "like-kind exchange",
    "delayed exchange": "like-kind exchange",
    "tax free exchange": "like-kind exchange",
    "tax-free exchange": "like-kind exchange",
    "qualified intermediary": "qualified intermediary",
    "qi": "qualified intermediary",
    "accommodator": "qualified intermediary",
    "exchange accommodator": "qualified intermediary",
    "reverse exchange": "reverse 1031 exchange",
    "reverse 1031": "reverse 1031 exchange",
    "improvement exchange": "improvement 1031 exchange",
    "build to suit exchange": "improvement 1031 exchange",
    "construction exchange": "improvement 1031 exchange",
    "exchange accommodation titleholder": "exchange accommodation titleholder",
    "eat": "exchange accommodation titleholder",
    # Depreciation terms
    "macrs": "macrs depreciation",
    "modified accelerated cost recovery": "macrs depreciation",
    "cost seg": "cost segregation",
    "cost segregation study": "cost segregation",
    "component depreciation": "cost segregation",
    "bonus depreciation": "bonus depreciation section 168k",
    "100% bonus": "bonus depreciation section 168k",
    "168(k)": "bonus depreciation section 168k",
    "section 168k": "bonus depreciation section 168k",
    "27.5 year": "residential rental depreciation",
    "27.5 years": "residential rental depreciation",
    "39 year": "commercial depreciation",
    "39 years": "commercial depreciation",
    "straight line depreciation": "straight-line depreciation",
    "sl depreciation": "straight-line depreciation",
    "ads depreciation": "alternative depreciation system",
    "alternative depreciation": "alternative depreciation system",
    # Passive activity
    "passive activity": "passive activity rules 469",
    "passive loss": "passive activity rules 469",
    "pal rules": "passive activity rules 469",
    "passive activity loss": "passive activity rules 469",
    "real estate professional": "real estate professional status",
    "rep status": "real estate professional status",
    "re professional": "real estate professional status",
    "750 hour test": "real estate professional status",
    "750 hours": "real estate professional status",
    "material participation": "material participation tests",
    "$25,000 allowance": "rental loss allowance 25k",
    "$25k allowance": "rental loss allowance 25k",
    "25000 allowance": "rental loss allowance 25k",
    "rental loss allowance": "rental loss allowance 25k",
    "active participation": "rental loss allowance 25k",
    # Section 199A / QBI
    "qbi": "section 199a qbi deduction",
    "qualified business income": "section 199a qbi deduction",
    "199a": "section 199a qbi deduction",
    "section 199a": "section 199a qbi deduction",
    "pass-through deduction": "section 199a qbi deduction",
    "20% deduction": "section 199a qbi deduction",
    "safe harbor rental": "section 199a rental safe harbor",
    "rev proc 2019-38": "section 199a rental safe harbor",
    "triple net lease": "triple net lease nnn",
    "nnn lease": "triple net lease nnn",
    # Opportunity Zones
    "opportunity zone": "opportunity zone 1400z",
    "oz fund": "opportunity zone 1400z",
    "qof": "qualified opportunity fund",
    "qualified opportunity fund": "qualified opportunity fund",
    "qoz": "qualified opportunity zone",
    "qozb": "qualified opportunity zone business",
    "qualified opportunity zone business": "qualified opportunity zone business",
    "180 day rule": "opportunity zone 180 day investment",
    "step up in basis": "opportunity zone basis step-up",
    "10 year hold": "opportunity zone 10 year hold",
    # Installment Sales
    "installment sale": "installment sale 453",
    "installment method": "installment sale 453",
    "section 453": "installment sale 453",
    "dealer exclusion": "installment sale dealer exclusion",
    "related party installment": "installment sale related party",
    "453(e)": "installment sale related party",
    "453(g)": "installment sale related party",
    # Depreciation Recapture
    "depreciation recapture": "depreciation recapture 1250",
    "section 1250": "depreciation recapture 1250",
    "unrecaptured 1250 gain": "unrecaptured section 1250 gain",
    "unrecaptured section 1250": "unrecaptured section 1250 gain",
    "25% rate": "unrecaptured section 1250 gain",
    # Primary Residence
    "primary residence exclusion": "primary residence exclusion 121",
    "home sale exclusion": "primary residence exclusion 121",
    "section 121": "primary residence exclusion 121",
    "$250,000 exclusion": "primary residence exclusion 121",
    "$500,000 exclusion": "primary residence exclusion 121",
    "250k exclusion": "primary residence exclusion 121",
    "500k exclusion": "primary residence exclusion 121",
    "ownership and use test": "primary residence exclusion 121",
    # REITs
    "reit": "real estate investment trust 856",
    "real estate investment trust": "real estate investment trust 856",
    "section 856": "real estate investment trust 856",
    "95% distribution": "reit distribution requirement",
    "reit distribution": "reit distribution requirement",
    "taxable reit subsidiary": "taxable reit subsidiary",
    "trs": "taxable reit subsidiary",
    # LIHTC
    "lihtc": "low income housing tax credit 42",
    "low income housing credit": "low income housing tax credit 42",
    "section 42": "low income housing tax credit 42",
    "4% credit": "lihtc 4 percent credit",
    "9% credit": "lihtc 9 percent credit",
    "qualified basis": "lihtc qualified basis",
    "compliance period": "lihtc compliance period",
    # Historic Rehab
    "historic tax credit": "historic rehabilitation credit 47",
    "htc": "historic rehabilitation credit 47",
    "section 47": "historic rehabilitation credit 47",
    "rehabilitation credit": "historic rehabilitation credit 47",
    # 179D
    "179d": "section 179d energy deduction",
    "section 179d": "section 179d energy deduction",
    "energy efficient building": "section 179d energy deduction",
    "commercial building deduction": "section 179d energy deduction",
    # At-Risk
    "at risk": "at-risk rules 465",
    "at-risk rules": "at-risk rules 465",
    "section 465": "at-risk rules 465",
    "qualified nonrecourse": "qualified nonrecourse financing",
    "nonrecourse financing": "qualified nonrecourse financing",
    # REMIC
    "remic": "real estate mortgage conduit 860a",
    "real estate mortgage conduit": "real estate mortgage conduit 860a",
    "section 860a": "real estate mortgage conduit 860a",
    # Construction Interest
    "263a": "construction interest capitalization 263a",
    "section 263a": "construction interest capitalization 263a",
    "unicap": "construction interest capitalization 263a",
    "uniform capitalization": "construction interest capitalization 263a",
    "construction period interest": "construction interest capitalization 263a",
    # Demolition
    "280b": "demolition costs 280b",
    "section 280b": "demolition costs 280b",
    "demolition costs": "demolition costs 280b",
    "demolition expense": "demolition costs 280b",
    # Involuntary Conversion
    "involuntary conversion": "involuntary conversion 1033",
    "section 1033": "involuntary conversion 1033",
    "condemnation": "involuntary conversion 1033",
    "eminent domain": "involuntary conversion 1033",
    "casualty loss": "involuntary conversion 1033",
    # Tenant Improvements
    "tenant improvement": "tenant improvements qip",
    "leasehold improvement": "tenant improvements qip",
    "qualified improvement property": "tenant improvements qip",
    "qip": "tenant improvements qip",
    # Ground Lease
    "ground lease": "ground lease taxation 110",
    "section 110": "ground lease taxation 110",
    # Other
    "163j": "business interest limitation 163j",
    "section 163j": "business interest limitation 163j",
    "business interest limitation": "business interest limitation 163j",
    "interest expense limitation": "business interest limitation 163j",
    "partnership basis": "partnership basis 754",
    "754 election": "partnership basis 754",
    "section 754": "partnership basis 754",
    "704c": "contributed property 704c",
    "section 704c": "contributed property 704c",
    "contributed property": "contributed property 704c",
    "environmental remediation": "environmental remediation 198",
    "brownfield": "environmental remediation 198",
    "section 198": "environmental remediation 198",
}

IRC_SECTION_PATTERNS: List[Tuple[str, str]] = [
    (r"\b(?:irc|IRC|I\.R\.C\.)\s*(?:section|sec\.?|[Ss])\s*(\d+[a-zA-Z]?(?:\([a-z0-9]+\))*)", "IRC {}"),
    (r"\bsection\s+(\d{2,4}[a-zA-Z]?(?:\([a-z0-9]+\))*)\b", "IRC {}"),
    (r"\b(\d{3,4})\s*(?:exchange|deduction|exclusion|credit|recapture)\b", "IRC {}"),
    (r"\bsec(?:tion)?\.?\s*(\d{3,4}[a-zA-Z]?)\b", "IRC {}"),
]

PROPERTY_TYPE_PATTERNS: Dict[str, str] = {
    r"\bresidential\s+rental\b": "residential_rental",
    r"\bcommercial\s+(?:property|building|real estate)\b": "commercial",
    r"\bindustrial\b": "industrial",
    r"\boffice\s+building\b": "office",
    r"\bretail\b": "retail",
    r"\bmulti-?family\b": "multifamily",
    r"\bapartment\b": "multifamily",
    r"\bsingle.?family\b": "single_family",
    r"\braw\s+land\b": "raw_land",
    r"\bvacant\s+land\b": "raw_land",
    r"\bhotel\b": "hospitality",
    r"\bmotel\b": "hospitality",
    r"\bself.?storage\b": "self_storage",
    r"\bwarehouse\b": "warehouse",
    r"\bmixed.?use\b": "mixed_use",
    r"\bmobile\s+home\b": "mobile_home",
    r"\bmanufactured\s+home\b": "mobile_home",
    r"\bfarm(?:land)?\b": "agricultural",
    r"\branch\b": "agricultural",
    r"\btimber\b": "timber",
    r"\bparking\s+(?:lot|garage|structure)\b": "parking",
}

DOLLAR_PATTERN = re.compile(r"\$[\d,]+(?:\.\d{2})?|\b\d{1,3}(?:,\d{3})+\b")
TIME_PATTERN = re.compile(
    r"\b(\d+)\s*(?:year|yr|month|mo|day|week)s?\b", re.IGNORECASE
)


# =============================================================================
# NORMALIZATION FUNCTIONS
# =============================================================================

def normalize_semantics(query: str) -> NormalizationResult:
    """
    Normalize a real estate tax query into canonical form.

    This is purely deterministic. No ML, no embeddings, no probability.
    Steps:
      1. Lowercase and strip
      2. Extract IRC section references
      3. Extract dollar amounts
      4. Extract time periods
      5. Detect property types
      6. Apply synonym map
      7. Detect topic areas
    """
    if not query or not query.strip():
        return NormalizationResult(original=query, normalized="", confidence=0.0)

    original = query.strip()
    working = original.lower().strip()
    transformations: List[str] = []
    irc_sections: List[str] = []
    dollar_amounts: List[float] = []
    time_periods: List[str] = []
    property_types: List[str] = []
    detected_topics: List[str] = []

    # Step 1: Extract IRC sections
    for pattern, fmt in IRC_SECTION_PATTERNS:
        for match in re.finditer(pattern, working, re.IGNORECASE):
            section = fmt.format(match.group(1))
            if section not in irc_sections:
                irc_sections.append(section)
                transformations.append(f"extracted_irc:{section}")

    # Step 2: Extract dollar amounts
    for match in DOLLAR_PATTERN.finditer(working):
        raw = match.group().replace("$", "").replace(",", "")
        try:
            val = float(raw)
            if val > 0:
                dollar_amounts.append(val)
                transformations.append(f"extracted_amount:${val:,.2f}")
        except ValueError:
            pass

    # Step 3: Extract time periods
    for match in TIME_PATTERN.finditer(working):
        period_str = match.group()
        time_periods.append(period_str)
        transformations.append(f"extracted_period:{period_str}")

    # Step 4: Detect property types
    for pattern_str, prop_type in PROPERTY_TYPE_PATTERNS.items():
        if re.search(pattern_str, working, re.IGNORECASE):
            if prop_type not in property_types:
                property_types.append(prop_type)
                transformations.append(f"detected_property:{prop_type}")

    # Step 5: Apply synonym normalization (longest match first)
    normalized = working
    sorted_synonyms = sorted(TERM_SYNONYMS.keys(), key=len, reverse=True)
    applied_synonyms: Set[str] = set()

    for term in sorted_synonyms:
        pattern = re.compile(re.escape(term), re.IGNORECASE)
        if pattern.search(normalized):
            canonical = TERM_SYNONYMS[term]
            if canonical not in applied_synonyms:
                detected_topics.append(canonical)
                applied_synonyms.add(canonical)
                transformations.append(f"synonym:{term}->{canonical}")

    # Step 6: Build final normalized form
    if detected_topics:
        normalized = " | ".join(detected_topics) + " | " + normalized
        transformations.append("prepended_topics")

    # Step 7: Confidence scoring
    confidence = 1.0
    if not irc_sections and not detected_topics:
        confidence = 0.5
    elif irc_sections and detected_topics:
        confidence = 1.0
    elif irc_sections or detected_topics:
        confidence = 0.8

    result = NormalizationResult(
        original=original,
        normalized=normalized,
        extracted_irc_sections=irc_sections,
        extracted_entities=[],
        detected_topics=detected_topics,
        confidence=confidence,
        transformations_applied=transformations,
        dollar_amounts=dollar_amounts,
        time_periods=time_periods,
        property_types=property_types,
    )

    logger.debug(
        "Normalized query | topics={} irc={} confidence={:.2f} transforms={}",
        len(detected_topics), len(irc_sections), confidence, len(transformations),
    )

    return result


def extract_keywords(query: str) -> List[str]:
    """Extract meaningful keywords from a query for doctrine matching."""
    stop_words = {
        "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
        "have", "has", "had", "do", "does", "did", "will", "would", "could",
        "should", "may", "might", "shall", "can", "need", "must", "to", "of",
        "in", "for", "on", "with", "at", "by", "from", "as", "into", "about",
        "between", "through", "during", "before", "after", "above", "below",
        "and", "but", "or", "not", "no", "if", "when", "where", "how", "what",
        "which", "who", "whom", "this", "that", "these", "those", "my", "your",
        "his", "her", "its", "our", "their", "i", "me", "we", "us", "you",
        "he", "she", "it", "they", "them", "am", "than", "also", "very",
        "just", "so", "too", "each", "every", "all", "any", "both",
    }
    words = re.findall(r"\b[a-zA-Z]{2,}\b", query.lower())
    return [w for w in words if w not in stop_words]


def detect_question_type(query: str) -> str:
    """Detect what type of question is being asked."""
    q = query.lower().strip()

    if any(q.startswith(w) for w in ["can i", "am i able", "is it possible"]):
        return "eligibility"
    if any(w in q for w in ["how much", "what amount", "calculate", "computation"]):
        return "calculation"
    if any(w in q for w in ["deadline", "due date", "time limit", "when must"]):
        return "timing"
    if any(w in q for w in ["requirement", "qualify", "eligible", "meet the test"]):
        return "requirements"
    if any(w in q for w in ["risk", "audit", "penalty", "irs position"]):
        return "risk_assessment"
    if any(w in q for w in ["compare", "difference", "versus", "vs", "better"]):
        return "comparison"
    if any(w in q for w in ["strategy", "plan", "optimize", "minimize", "structure"]):
        return "planning"
    if any(w in q for w in ["report", "form", "file", "disclosure", "return"]):
        return "compliance"
    if any(w in q for w in ["what happens if", "consequence", "failure to"]):
        return "consequence"
    if any(w in q for w in ["explain", "what is", "define", "overview"]):
        return "educational"

    return "general"


def compute_topic_relevance(query: str, doctrine_keywords: List[str]) -> float:
    """Compute relevance score between query and doctrine keywords."""
    query_words = set(extract_keywords(query))
    doctrine_set = set(k.lower() for k in doctrine_keywords)

    if not query_words or not doctrine_set:
        return 0.0

    intersection = query_words & doctrine_set
    union = query_words | doctrine_set

    jaccard = len(intersection) / len(union) if union else 0.0
    keyword_coverage = len(intersection) / len(doctrine_set) if doctrine_set else 0.0

    return round(0.4 * jaccard + 0.6 * keyword_coverage, 4)
