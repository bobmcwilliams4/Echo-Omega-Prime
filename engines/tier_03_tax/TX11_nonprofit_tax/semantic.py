"""
TX11 Nonprofit Tax — Semantic Normalization
Domain-specific term normalization and abbreviation expansion for nonprofit tax.

Deterministic normalization ensures consistent doctrine matching.
Synonym groups collapse variations to canonical forms.

Author: ECHO OMEGA PRIME
Engine: TX11 Nonprofit Tax
"""

from dataclasses import dataclass
from typing import Dict, List, Set
import re


@dataclass
class NormalizationResult:
    """Result of semantic normalization."""
    original_query: str
    normalized_query: str
    expansions_applied: List[str]
    synonyms_replaced: int
    canonical_terms: List[str]


# =============================================================================
# ABBREVIATION EXPANSIONS
# =============================================================================

ABBREVIATION_EXPANSIONS: Dict[str, str] = {
    # IRC Sections
    r"\b501\(c\)\(3\)\b": "internal revenue code section 501(c)(3)",
    r"\b501\(c\)\(4\)\b": "internal revenue code section 501(c)(4)",
    r"\b501\(h\)\b": "internal revenue code section 501(h)",
    r"\b509\(a\)\b": "internal revenue code section 509(a)",
    r"\b509\(a\)\(1\)\b": "internal revenue code section 509(a)(1)",
    r"\b509\(a\)\(2\)\b": "internal revenue code section 509(a)(2)",
    r"\b509\(a\)\(3\)\b": "internal revenue code section 509(a)(3)",
    r"\b170\b": "internal revenue code section 170",
    r"\b4940\b": "internal revenue code section 4940",
    r"\b4941\b": "internal revenue code section 4941",
    r"\b4942\b": "internal revenue code section 4942",
    r"\b4943\b": "internal revenue code section 4943",
    r"\b4944\b": "internal revenue code section 4944",
    r"\b4945\b": "internal revenue code section 4945",
    r"\b4958\b": "internal revenue code section 4958",
    r"\b4966\b": "internal revenue code section 4966",
    r"\b4967\b": "internal revenue code section 4967",
    r"\b511\b": "internal revenue code section 511",
    r"\b512\b": "internal revenue code section 512",
    r"\b513\b": "internal revenue code section 513",
    r"\b514\b": "internal revenue code section 514",
    r"\b4911\b": "internal revenue code section 4911",

    # Common acronyms
    r"\bIRC\b": "internal revenue code",
    r"\bUBIT\b": "unrelated business income tax",
    r"\bUBTI\b": "unrelated business taxable income",
    r"\bDAF\b": "donor-advised fund",
    r"\bPF\b": "private foundation",
    r"\bPC\b": "public charity",
    r"\bEO\b": "exempt organization",
    r"\bNFP\b": "not-for-profit",
    r"\bNPO\b": "nonprofit organization",
    r"\bCRF\b": "community foundation",
    r"\bDQP\b": "disqualified person",
    r"\bEBT\b": "excess benefit transaction",
    r"\bFMV\b": "fair market value",

    # Forms
    r"\b990\b": "form 990",
    r"\b990-PF\b": "form 990-pf",
    r"\b990-T\b": "form 990-t",
    r"\b990-EZ\b": "form 990-ez",
    r"\b990-N\b": "form 990-n",
    r"\b1023\b": "form 1023",
    r"\b1024\b": "form 1024",

    # Organizations
    r"\bIRS\b": "internal revenue service",
    r"\bTE/GE\b": "tax exempt and government entities",

    # Technical terms
    r"\bNOL\b": "net operating loss",
    r"\bAOC\b": "articles of incorporation",
    r"\bCOI\b": "conflict of interest",
}


# =============================================================================
# SYNONYM GROUPS — Canonical form first, then synonyms
# =============================================================================

SYNONYM_GROUPS: Dict[str, List[str]] = {
    # Exempt status
    "exempt status": ["tax-exempt status", "exemption", "501(c)(3) status", "charitable status"],
    "exempt organization": ["tax-exempt organization", "nonprofit", "charity", "exempt entity"],

    # Public charity vs private foundation
    "public charity": ["publicly supported charity", "public charity organization", "509(a)(1) organization"],
    "private foundation": ["non-operating foundation", "family foundation", "pf"],
    "supporting organization": ["509(a)(3) organization", "type i supporting organization", "type ii supporting organization", "type iii supporting organization"],

    # Qualification tests
    "organizational test": ["organizational requirement", "articles test"],
    "operational test": ["operational requirement", "activities test"],
    "public support test": ["one-third support test", "33 1/3 percent test", "public support requirement"],

    # Private benefit/inurement
    "private benefit": ["impermissible private benefit", "non-incidental private benefit"],
    "private inurement": ["inurement", "insider benefit", "distribution to insiders"],
    "excess benefit transaction": ["excess benefit", "ebt", "intermediate sanction transaction"],
    "disqualified person": ["insider", "substantial contributor", "person with substantial influence"],

    # UBIT
    "unrelated business income": ["ubi", "unrelated income", "business income"],
    "unrelated business taxable income": ["ubti", "taxable ubi"],
    "unrelated trade or business": ["unrelated business", "ub", "unrelated business activity"],
    "substantially related": ["substantially related activity", "related activity", "exempt function activity"],
    "regularly carried on": ["regular activity", "continuous activity"],

    # Lobbying and political
    "lobbying": ["legislative activity", "lobbying activity", "influencing legislation"],
    "political campaign intervention": ["political activity", "campaign intervention", "electioneering", "political campaign activity"],
    "candidate": ["candidate for public office", "political candidate", "office seeker"],

    # Donor-advised funds
    "donor-advised fund": ["daf", "donor advised fund", "advised fund"],
    "sponsoring organization": ["daf sponsor", "fund sponsor", "sponsoring charity"],
    "advisory privileges": ["advisory rights", "recommendation privileges"],

    # Governance
    "governing board": ["board of directors", "board of trustees", "board"],
    "independent board member": ["independent director", "outside director", "non-interested director"],
    "conflict of interest": ["coi", "conflicted transaction"],

    # Charitable purpose
    "charitable purpose": ["exempt purpose", "501(c)(3) purpose", "charitable mission"],
    "religious purpose": ["religious activity", "advancement of religion"],
    "educational purpose": ["educational activity", "instruction of the public"],

    # Contributions
    "charitable contribution": ["donation", "gift", "charitable gift", "contribution"],
    "contribution deduction": ["charitable deduction", "donation deduction", "170 deduction"],
    "substantiation": ["contribution substantiation", "donor acknowledgment", "written acknowledgment"],

    # Forms and compliance
    "annual information return": ["form 990", "990 return", "information return"],
    "determination letter": ["exemption letter", "501(c)(3) determination", "irs determination"],
    "public disclosure": ["990 disclosure", "public inspection", "transparency requirement"],

    # Excise taxes
    "excise tax": ["intermediate sanction", "penalty tax", "section 4958 tax"],
    "self-dealing": ["prohibited transaction", "4941 transaction"],
    "jeopardizing investment": ["risky investment", "imprudent investment", "4944 investment"],
    "taxable expenditure": ["prohibited expenditure", "4945 expenditure"],

    # Distribution requirements
    "minimum distribution requirement": ["5% distribution", "payout requirement", "4942 requirement"],
    "qualifying distribution": ["charitable distribution", "exempt purpose distribution"],

    # Revenue sources
    "program service revenue": ["earned income", "fee for service", "program income"],
    "contribution revenue": ["donation revenue", "gift revenue", "contribution income"],
    "investment income": ["passive income", "portfolio income", "dividends and interest"],

    # Special entities
    "church": ["religious organization", "house of worship", "religious congregation"],
    "school": ["educational institution", "501(c)(3) school", "exempt school"],
    "hospital": ["healthcare organization", "medical facility", "exempt hospital"],
}


# =============================================================================
# CANONICAL TERMS — Domain-specific vocabulary
# =============================================================================

CANONICAL_TERMS: Set[str] = {
    # Core concepts
    "exempt status", "exempt organization", "501(c)(3)", "public charity", "private foundation",
    "organizational test", "operational test", "private benefit", "private inurement",
    "unrelated business income", "ubit", "substantially related", "regularly carried on",
    "lobbying", "political campaign intervention", "excess benefit transaction", "disqualified person",
    "donor-advised fund", "sponsoring organization", "charitable purpose", "exempt purpose",

    # Statutory terms
    "exclusively", "primarily", "substantial", "incidental", "insubstantial",
    "commensurate", "reasonable", "fair market value", "arm's-length",

    # Tests and standards
    "public support test", "one-third test", "facts and circumstances test",
    "commensurate test", "rebuttable presumption", "comparability data",

    # Compliance
    "form 990", "form 1023", "determination letter", "public disclosure",
    "annual information return", "substantiation", "contemporaneous documentation",

    # Excise taxes
    "self-dealing", "excess business holdings", "jeopardizing investment", "taxable expenditure",
    "minimum distribution requirement", "intermediate sanction",

    # Revenue and support
    "public support", "contribution", "grant", "program service revenue",
    "investment income", "unrelated business income", "gross receipts",

    # Governance
    "governing board", "independent director", "conflict of interest",
    "substantial influence", "insider", "related party",
}


# =============================================================================
# NORMALIZATION FUNCTIONS
# =============================================================================

def expand_abbreviations(text: str) -> tuple[str, List[str]]:
    """Expand common nonprofit tax abbreviations to full terms."""
    expanded_text = text
    applied_expansions = []

    for pattern, expansion in ABBREVIATION_EXPANSIONS.items():
        if re.search(pattern, expanded_text, re.IGNORECASE):
            expanded_text = re.sub(pattern, expansion, expanded_text, flags=re.IGNORECASE)
            applied_expansions.append(f"{pattern} -> {expansion}")

    return expanded_text, applied_expansions


def normalize_synonyms(text: str) -> tuple[str, int]:
    """Replace synonyms with canonical forms."""
    normalized_text = text.lower()
    replacement_count = 0

    for canonical, synonyms in SYNONYM_GROUPS.items():
        for synonym in synonyms:
            pattern = r'\b' + re.escape(synonym.lower()) + r'\b'
            if re.search(pattern, normalized_text):
                normalized_text = re.sub(pattern, canonical, normalized_text)
                replacement_count += 1

    return normalized_text, replacement_count


def extract_canonical_terms(text: str) -> List[str]:
    """Extract canonical terms present in the text."""
    text_lower = text.lower()
    found_terms = []

    for term in CANONICAL_TERMS:
        if term.lower() in text_lower:
            found_terms.append(term)

    return found_terms


def normalize_semantics(query: str) -> NormalizationResult:
    """
    Apply full semantic normalization pipeline:
    1. Expand abbreviations
    2. Normalize synonyms to canonical forms
    3. Extract canonical terms
    """
    # Step 1: Expand abbreviations
    expanded_text, expansions_applied = expand_abbreviations(query)

    # Step 2: Normalize synonyms
    normalized_text, synonyms_replaced = normalize_synonyms(expanded_text)

    # Step 3: Extract canonical terms
    canonical_terms = extract_canonical_terms(normalized_text)

    return NormalizationResult(
        original_query=query,
        normalized_query=normalized_text,
        expansions_applied=expansions_applied,
        synonyms_replaced=synonyms_replaced,
        canonical_terms=canonical_terms,
    )


def get_all_domains() -> List[str]:
    """Return list of all semantic domains."""
    return [
        "exempt_status",
        "public_charity_classification",
        "private_foundation_rules",
        "unrelated_business_income",
        "political_lobbying",
        "excess_benefits",
        "donor_advised_funds",
        "governance_compliance",
        "charitable_contributions",
        "excise_taxes",
    ]


def get_synonym_count() -> int:
    """Return total number of synonym groups."""
    return len(SYNONYM_GROUPS)


def get_canonical_count() -> int:
    """Return total number of canonical terms."""
    return len(CANONICAL_TERMS)
