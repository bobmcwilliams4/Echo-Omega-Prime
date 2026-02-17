"""
TX09 AMT CALCULATOR — SEMANTIC NORMALIZATION
Deterministic query preprocessing for AMT domain.

No LLM. No embeddings. No probabilistic models.
Pure rule-based normalization.

Author: ECHO OMEGA PRIME
Version: 1.0.0
"""

from dataclasses import dataclass
from typing import List, Optional, Set
import re


@dataclass
class NormalizationResult:
    """Result of semantic normalization."""
    original_query: str
    normalized_query: str
    detected_keywords: List[str]
    entity_type: Optional[str]
    tax_year: Optional[int]
    detected_amounts: List[float]
    detected_sections: List[str]


# ============================================================================
# AMT SEMANTIC DICTIONARY
# ============================================================================

AMT_SYNONYM_MAP = {
    # Core AMT terms
    "alternative minimum tax": ["amt", "minimum tax", "parallel tax"],
    "tentative minimum tax": ["tmt", "tentative amt"],
    "alternative minimum taxable income": ["amti", "amt income", "amt base"],
    "amt exemption": ["exemption amount", "amt deduction"],
    "amt adjustment": ["adjustments", "amt modifications"],
    "tax preference": ["preferences", "preference items", "tax preferences"],

    # IRC sections
    "section 55": ["§55", "irc 55", "code section 55"],
    "section 56": ["§56", "irc 56", "code section 56"],
    "section 57": ["§57", "irc 57", "code section 57"],
    "section 53": ["§53", "irc 53", "code section 53"],
    "section 59": ["§59", "irc 59", "code section 59"],

    # Adjustments
    "depreciation": ["depreciation adjustment", "ads depreciation", "amt depreciation"],
    "mining exploration": ["mining costs", "mine development", "exploration costs"],
    "long-term contract": ["percentage of completion", "completed contract"],
    "pollution control": ["pollution control facility", "environmental depreciation"],
    "installment sale": ["installment method", "dealer installment sales"],

    # Preferences
    "private activity bond": ["pab", "private activity bonds", "tax-exempt interest"],
    "percentage depletion": ["depletion preference", "excess depletion"],
    "intangible drilling cost": ["idc", "intangible drilling costs", "drilling preferences"],
    "accelerated depreciation": ["pre-1987 depreciation", "pre-1987 property"],

    # Credits
    "minimum tax credit": ["mtc", "amt credit", "section 53 credit"],

    # Stock options
    "incentive stock option": ["iso", "qualified stock option"],
    "exercise spread": ["bargain element", "iso spread"],

    # Entities
    "individual": ["personal", "person", "taxpayer"],
    "corporation": ["c corp", "c corporation", "corporate"],
    "partnership": ["partners", "partnership interest"],
    "s corporation": ["s corp", "subchapter s"],
    "estate": ["decedent estate", "estate tax"],
    "trust": ["fiduciary", "trustee"],

    # Filing status
    "single": ["unmarried", "filing single"],
    "married filing jointly": ["mfj", "joint return", "married joint"],
    "married filing separately": ["mfs", "married separate"],
    "head of household": ["hoh", "head-of-household"],

    # TCJA and recent changes
    "tax cuts and jobs act": ["tcja", "tax reform"],
    "inflation reduction act": ["ira", "ira 2022"],
    "corporate amt": ["camt", "corporate minimum tax"],
    "adjusted financial statement income": ["afsi", "book income"],

    # SALT
    "state and local tax": ["salt", "state tax", "local tax"],
    "salt cap": ["salt limitation", "$10000 cap", "10k cap"],

    # NOL
    "net operating loss": ["nol", "loss carryforward"],
    "alternative tax nol": ["atnol", "amt nol"],
}

# Keywords that indicate specific AMT topics
AMT_TOPIC_KEYWORDS = {
    "calculation": ["calculate", "computation", "compute", "determine amt", "how much"],
    "exemption": ["exemption", "phase-out", "phaseout", "exempt amount"],
    "adjustments": ["adjustment", "§56", "section 56", "modifications"],
    "preferences": ["preference", "§57", "section 57"],
    "credits": ["credit", "§53", "section 53", "mtc"],
    "iso": ["iso", "incentive stock", "stock option", "exercise"],
    "depreciation": ["depreciation", "ads", "accelerated"],
    "pab": ["private activity", "pab", "municipal bond", "tax-exempt interest"],
    "planning": ["planning", "strategy", "minimize", "avoid", "reduce"],
    "corporate": ["corporation", "corporate", "c corp", "camt"],
    "salt": ["salt", "state tax", "local tax"],
    "nol": ["nol", "net operating loss", "loss"],
}

# Entity detection patterns
ENTITY_PATTERNS = {
    "individual": r"\b(individual|person|taxpayer|filing)\b",
    "c_corporation": r"\b(c corp|c-corp|corporation|corporate)\b",
    "s_corporation": r"\b(s corp|s-corp|subchapter s)\b",
    "partnership": r"\b(partnership|partners|partner)\b",
    "estate": r"\b(estate|decedent)\b",
    "trust": r"\b(trust|fiduciary|trustee)\b",
}

# Section number patterns
SECTION_PATTERN = r"(?:§|section|sec\.?|irc)\s*(\d+)"

# Amount patterns
AMOUNT_PATTERN = r"\$?\d{1,3}(?:,\d{3})*(?:\.\d{2})?"


# ============================================================================
# NORMALIZATION FUNCTIONS
# ============================================================================

def normalize_amt_semantics(query: str) -> NormalizationResult:
    """
    Normalize AMT query using deterministic rules.

    Args:
        query: Raw query string

    Returns:
        NormalizationResult with normalized query and metadata
    """
    original = query
    normalized = query.lower().strip()

    # Apply synonym normalization
    for canonical, synonyms in AMT_SYNONYM_MAP.items():
        for synonym in synonyms:
            pattern = r'\b' + re.escape(synonym) + r'\b'
            normalized = re.sub(pattern, canonical, normalized, flags=re.IGNORECASE)

    # Detect keywords
    detected_keywords = []
    for topic, keywords in AMT_TOPIC_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in normalized:
                detected_keywords.append(topic)
                break

    # Remove duplicates
    detected_keywords = list(set(detected_keywords))

    # Detect entity type
    entity_type = None
    for entity, pattern in ENTITY_PATTERNS.items():
        if re.search(pattern, normalized, re.IGNORECASE):
            entity_type = entity
            break

    # Detect tax year
    tax_year = None
    year_match = re.search(r'\b(20\d{2})\b', normalized)
    if year_match:
        tax_year = int(year_match.group(1))

    # Detect amounts
    amounts = []
    for match in re.finditer(AMOUNT_PATTERN, normalized):
        amount_str = match.group(0).replace('$', '').replace(',', '')
        try:
            amounts.append(float(amount_str))
        except ValueError:
            pass

    # Detect IRC sections
    sections = []
    for match in re.finditer(SECTION_PATTERN, normalized, re.IGNORECASE):
        sections.append(f"§{match.group(1)}")

    return NormalizationResult(
        original_query=original,
        normalized_query=normalized,
        detected_keywords=detected_keywords,
        entity_type=entity_type,
        tax_year=tax_year,
        detected_amounts=amounts,
        detected_sections=list(set(sections))
    )


def extract_filing_status(query: str) -> Optional[str]:
    """Extract filing status from query."""
    query_lower = query.lower()

    if any(term in query_lower for term in ["married filing jointly", "mfj", "joint"]):
        return "married_joint"
    elif any(term in query_lower for term in ["married filing separately", "mfs", "married separate"]):
        return "married_separate"
    elif any(term in query_lower for term in ["head of household", "hoh"]):
        return "head_household"
    elif "single" in query_lower:
        return "single"
    elif any(term in query_lower for term in ["estate", "trust"]):
        return "estate_trust"

    return None


def extract_numeric_inputs(query: str) -> dict:
    """Extract numeric inputs for AMT calculation."""
    result = {
        "regular_income": None,
        "adjustments": {},
        "preferences": {},
    }

    # Look for income amounts
    income_pattern = r"(?:income|taxable income|regular income).*?\$?([\d,]+)"
    income_match = re.search(income_pattern, query, re.IGNORECASE)
    if income_match:
        try:
            result["regular_income"] = float(income_match.group(1).replace(',', ''))
        except ValueError:
            pass

    # Look for specific adjustments
    adj_patterns = {
        "depreciation": r"depreciation.*?\$?([\d,]+)",
        "mining": r"mining.*?\$?([\d,]+)",
        "iso": r"(?:iso|stock option).*?\$?([\d,]+)",
    }

    for adj_type, pattern in adj_patterns.items():
        match = re.search(pattern, query, re.IGNORECASE)
        if match:
            try:
                result["adjustments"][adj_type] = float(match.group(1).replace(',', ''))
            except ValueError:
                pass

    # Look for preferences
    pref_patterns = {
        "pab_interest": r"(?:private activity|pab).*?\$?([\d,]+)",
        "depletion": r"depletion.*?\$?([\d,]+)",
        "idc": r"(?:idc|drilling).*?\$?([\d,]+)",
    }

    for pref_type, pattern in pref_patterns.items():
        match = re.search(pattern, query, re.IGNORECASE)
        if match:
            try:
                result["preferences"][pref_type] = float(match.group(1).replace(',', ''))
            except ValueError:
                pass

    return result


def identify_amt_scenario(query: str) -> str:
    """Identify the specific AMT scenario being asked about."""
    query_lower = query.lower()

    # Calculation request
    if any(term in query_lower for term in ["calculate", "compute", "how much amt", "what is amt"]):
        return "calculation"

    # ISO-specific
    if any(term in query_lower for term in ["iso", "incentive stock option", "exercise"]):
        return "iso_exercise"

    # Exemption
    if any(term in query_lower for term in ["exemption", "phase-out", "phaseout"]):
        return "exemption_calculation"

    # Credits
    if any(term in query_lower for term in ["credit", "mtc", "minimum tax credit"]):
        return "credit_analysis"

    # Planning
    if any(term in query_lower for term in ["planning", "strategy", "avoid", "minimize"]):
        return "planning_strategy"

    # Corporate CAMT
    if any(term in query_lower for term in ["corporate amt", "camt", "adjusted financial statement"]):
        return "corporate_camt"

    # SALT
    if any(term in query_lower for term in ["salt", "state tax", "local tax"]):
        return "salt_analysis"

    # General
    return "general_amt"


# ============================================================================
# CONFIDENCE SCORING
# ============================================================================

def calculate_semantic_confidence(norm_result: NormalizationResult) -> float:
    """
    Calculate confidence score based on normalization quality.

    Returns: Float 0.0-1.0
    """
    score = 0.5  # Base score

    # Keywords detected (+0.1 per keyword, max +0.3)
    if norm_result.detected_keywords:
        score += min(len(norm_result.detected_keywords) * 0.1, 0.3)

    # Entity type detected (+0.1)
    if norm_result.entity_type:
        score += 0.1

    # IRC sections detected (+0.05 per section, max +0.15)
    if norm_result.detected_sections:
        score += min(len(norm_result.detected_sections) * 0.05, 0.15)

    # Amounts detected (+0.1)
    if norm_result.detected_amounts:
        score += 0.1

    # Cap at 1.0
    return min(score, 1.0)
