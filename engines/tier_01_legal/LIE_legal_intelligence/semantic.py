"""
LIE Semantic Normalization — Legal term normalization and query preprocessing.

Normalizes legal terminology, expands abbreviations, standardizes citations,
and preprocesses queries for consistent routing and retrieval.

Commander: Bobby Don McWilliams II | Authority: 11.0 SOVEREIGN
"""

from __future__ import annotations

import re
from typing import Dict, List, Tuple

from loguru import logger


# ═══════════════════════════════════════════════════════════════════
# LEGAL ABBREVIATION EXPANSION
# ═══════════════════════════════════════════════════════════════════

LEGAL_ABBREVIATIONS: Dict[str, str] = {
    # Courts
    "scotus": "supreme court of the united states",
    "ussc": "united states supreme court",
    "d.c. cir.": "district of columbia circuit",
    "1st cir.": "first circuit",
    "2nd cir.": "second circuit",
    "3rd cir.": "third circuit",
    "4th cir.": "fourth circuit",
    "5th cir.": "fifth circuit",
    "6th cir.": "sixth circuit",
    "7th cir.": "seventh circuit",
    "8th cir.": "eighth circuit",
    "9th cir.": "ninth circuit",
    "10th cir.": "tenth circuit",
    "11th cir.": "eleventh circuit",
    "fed. cir.": "federal circuit",

    # Statutes and codes
    "usc": "united states code",
    "cfr": "code of federal regulations",
    "u.s.c.": "united states code",
    "c.f.r.": "code of federal regulations",
    "frcp": "federal rules of civil procedure",
    "frcp": "federal rules of criminal procedure",
    "fre": "federal rules of evidence",
    "frap": "federal rules of appellate procedure",
    "aba": "american bar association",

    # Legal concepts
    "p&a": "pleadings and practice",
    "msa": "marital settlement agreement",
    "psa": "property settlement agreement",
    "quitclaim": "quitclaim deed",
    "w/d": "warranty deed",
    "lod": "letters of administration",
    "lot": "letters testamentary",
    "moj": "memorandum of judgment",
    "noa": "notice of appeal",
    "nod": "notice of default",
    "noe": "notice of entry",
    "mot": "motion",
    "mtd": "motion to dismiss",
    "msj": "motion for summary judgment",
    "mij": "motion in limine",
    "rog": "interrogatories",
    "rfp": "request for production",
    "rfa": "request for admission",

    # Employment law
    "flsa": "fair labor standards act",
    "osha": "occupational safety and health act",
    "fmla": "family and medical leave act",
    "ada": "americans with disabilities act",
    "adea": "age discrimination in employment act",
    "nlra": "national labor relations act",
    "nlrb": "national labor relations board",
    "eeoc": "equal employment opportunity commission",
    "erisa": "employee retirement income security act",

    # Environmental law
    "epa": "environmental protection agency",
    "nepa": "national environmental policy act",
    "cercla": "comprehensive environmental response compensation and liability act",
    "rcra": "resource conservation and recovery act",
    "cwa": "clean water act",
    "caa": "clean air act",
    "esa": "endangered species act",

    # Healthcare law
    "hipaa": "health insurance portability and accountability act",
    "fda": "food and drug administration",
    "cms": "centers for medicare and medicaid services",
    "aca": "affordable care act",
    "ppaca": "patient protection and affordable care act",
    "emtala": "emergency medical treatment and labor act",

    # Immigration law
    "uscis": "united states citizenship and immigration services",
    "ice": "immigration and customs enforcement",
    "cbp": "customs and border protection",
    "ina": "immigration and nationality act",
    "eoir": "executive office for immigration review",
    "bia": "board of immigration appeals",

    # Intellectual property
    "uspto": "united states patent and trademark office",
    "ptab": "patent trial and appeal board",
    "ttab": "trademark trial and appeal board",
    "dmca": "digital millennium copyright act",
    "wipo": "world intellectual property organization",

    # Bankruptcy
    "bk": "bankruptcy",
    "ch. 7": "chapter 7",
    "ch. 11": "chapter 11",
    "ch. 13": "chapter 13",

    # Criminal law
    "acca": "armed career criminal act",
    "cipa": "classified information procedures act",
    "fisa": "foreign intelligence surveillance act",
    "rico": "racketeer influenced and corrupt organizations act",

    # Regulatory
    "sec": "securities and exchange commission",
    "ftc": "federal trade commission",
    "fcc": "federal communications commission",
    "ferc": "federal energy regulatory commission",
    "doj": "department of justice",
    "ag": "attorney general",

    # International
    "wto": "world trade organization",
    "icc": "international criminal court",
    "icj": "international court of justice",
    "uncitral": "united nations commission on international trade law",

    # ADR
    "aaa": "american arbitration association",
    "jams": "judicial arbitration and mediation services",
    "nasd": "national association of securities dealers",
    "finra": "financial industry regulatory authority",

    # General legal
    "atty": "attorney",
    "corp": "corporation",
    "inc": "incorporated",
    "llc": "limited liability company",
    "lp": "limited partnership",
    "llp": "limited liability partnership",
    "dba": "doing business as",
    "aka": "also known as",
    "fka": "formerly known as",
    "nka": "now known as",
    "et al": "and others",
    "et seq": "and following",
    "ibid": "in the same place",
    "id": "the same",
    "supra": "above",
    "infra": "below",
    "cf": "compare",
    "e.g.": "for example",
    "i.e.": "that is",
    "viz": "namely",
    "v.": "versus",
    "ex rel": "on relation of",
    "ex parte": "on behalf of one party",
    "in re": "in the matter of",
    "per curiam": "by the court",
    "amicus curiae": "friend of the court",
}


# ═══════════════════════════════════════════════════════════════════
# LEGAL TERM SYNONYMS (for semantic expansion)
# ═══════════════════════════════════════════════════════════════════

LEGAL_SYNONYMS: Dict[str, List[str]] = {
    "contract": ["agreement", "compact", "covenant", "undertaking"],
    "plaintiff": ["claimant", "petitioner", "complainant"],
    "defendant": ["respondent", "appellee"],
    "lawsuit": ["action", "suit", "litigation", "proceeding"],
    "damages": ["compensation", "recovery", "award"],
    "negligence": ["carelessness", "neglect", "dereliction"],
    "breach": ["violation", "infringement", "default"],
    "fraud": ["misrepresentation", "deceit", "false pretense"],
    "injury": ["harm", "damage", "wrong"],
    "liability": ["responsibility", "culpability", "accountability"],
    "precedent": ["authority", "case law", "decision"],
    "statute": ["law", "legislation", "act", "code"],
    "regulation": ["rule", "directive", "ordinance"],
    "judgment": ["decree", "order", "ruling", "decision"],
    "appeal": ["review", "reconsideration"],
    "evidence": ["proof", "testimony", "exhibit"],
    "witness": ["deponent", "declarant", "testifier"],
    "trial": ["hearing", "proceeding", "adjudication"],
    "settlement": ["resolution", "compromise", "accord"],
    "injunction": ["restraining order", "prohibition", "stay"],
}


# ═══════════════════════════════════════════════════════════════════
# CITATION NORMALIZATION PATTERNS
# ═══════════════════════════════════════════════════════════════════

CITATION_NORMALIZATIONS: List[Tuple[str, str]] = [
    # Normalize spacing in citations
    (r'(\d+)\s*U\s*\.\s*S\s*\.\s*(\d+)', r'\1 U.S. \2'),
    (r'(\d+)\s*F\s*\.\s*(\d)d\s*(\d+)', r'\1 F.\2d \3'),
    (r'(\d+)\s*S\s*\.\s*Ct\s*\.\s*(\d+)', r'\1 S.Ct. \2'),
    (r'(\d+)\s*U\s*\.\s*S\s*\.\s*C\s*\.\s*§?\s*(\d+)', r'\1 U.S.C. § \2'),
    (r'(\d+)\s*C\s*\.\s*F\s*\.\s*R\s*\.\s*§?\s*(\d+)', r'\1 C.F.R. § \2'),

    # Normalize "v." vs "vs" vs "versus"
    (r'\s+vs\.?\s+', ' v. '),
    (r'\s+versus\s+', ' v. '),
]


# ═══════════════════════════════════════════════════════════════════
# LEGAL STOP WORDS (domain-specific)
# ═══════════════════════════════════════════════════════════════════

LEGAL_STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "as", "is", "was", "are", "were", "be",
    "been", "being", "have", "has", "had", "do", "does", "did", "will",
    "would", "should", "could", "may", "might", "must", "can",
}


# ═══════════════════════════════════════════════════════════════════
# JURISDICTION STANDARDIZATION
# ═══════════════════════════════════════════════════════════════════

JURISDICTION_ALIASES: Dict[str, str] = {
    "tx": "texas",
    "ca": "california",
    "ny": "new york",
    "fl": "florida",
    "il": "illinois",
    "pa": "pennsylvania",
    "oh": "ohio",
    "ga": "georgia",
    "nc": "north carolina",
    "mi": "michigan",
    "nj": "new jersey",
    "va": "virginia",
    "wa": "washington",
    "az": "arizona",
    "ma": "massachusetts",
    "tn": "tennessee",
    "in": "indiana",
    "mo": "missouri",
    "md": "maryland",
    "wi": "wisconsin",
    "co": "colorado",
    "mn": "minnesota",
    "sc": "south carolina",
    "al": "alabama",
    "la": "louisiana",
    "ky": "kentucky",
    "or": "oregon",
    "ok": "oklahoma",
    "ct": "connecticut",
    "ut": "utah",
    "ia": "iowa",
    "nv": "nevada",
    "ar": "arkansas",
    "ms": "mississippi",
    "ks": "kansas",
    "nm": "new mexico",
    "ne": "nebraska",
    "wv": "west virginia",
    "id": "idaho",
    "hi": "hawaii",
    "nh": "new hampshire",
    "me": "maine",
    "ri": "rhode island",
    "mt": "montana",
    "de": "delaware",
    "sd": "south dakota",
    "nd": "north dakota",
    "ak": "alaska",
    "vt": "vermont",
    "wy": "wyoming",
    "d.c.": "district of columbia",
    "dc": "district of columbia",
}


# ═══════════════════════════════════════════════════════════════════
# QUERY NORMALIZATION FUNCTION
# ═══════════════════════════════════════════════════════════════════

def normalize_legal_query(query: str) -> str:
    """
    Normalize a legal query through multiple passes:
    1. Expand abbreviations
    2. Normalize citations
    3. Standardize jurisdictions
    4. Lowercase and trim

    Args:
        query: Raw legal query text

    Returns:
        Normalized query string
    """
    if not query or not query.strip():
        return ""

    normalized = query.strip()

    # Pass 1: Expand legal abbreviations
    normalized_lower = normalized.lower()
    for abbrev, expansion in LEGAL_ABBREVIATIONS.items():
        # Use word boundaries to avoid partial matches
        pattern = r'\b' + re.escape(abbrev.lower()) + r'\b'
        normalized_lower = re.sub(pattern, expansion, normalized_lower)

    normalized = normalized_lower

    # Pass 2: Normalize citations (preserve case for this pass)
    for pattern, replacement in CITATION_NORMALIZATIONS:
        normalized = re.sub(pattern, replacement, normalized, flags=re.IGNORECASE)

    # Pass 3: Standardize jurisdictions
    for alias, full_name in JURISDICTION_ALIASES.items():
        pattern = r'\b' + re.escape(alias) + r'\b'
        normalized = re.sub(pattern, full_name, normalized, flags=re.IGNORECASE)

    # Pass 4: Collapse multiple spaces
    normalized = re.sub(r'\s+', ' ', normalized)

    # Pass 5: Trim
    normalized = normalized.strip()

    return normalized


def expand_synonyms(term: str) -> List[str]:
    """
    Expand a legal term to include synonyms.

    Args:
        term: Legal term

    Returns:
        List of synonyms (including original term)
    """
    term_lower = term.lower().strip()

    if term_lower in LEGAL_SYNONYMS:
        return [term_lower] + LEGAL_SYNONYMS[term_lower]

    return [term_lower]


def extract_party_names(query: str) -> List[str]:
    """
    Extract party names from case citations (e.g., "Smith v. Jones").

    Args:
        query: Legal query text

    Returns:
        List of party names
    """
    # Pattern: "Party1 v. Party2" or "Party1 vs. Party2"
    pattern = r'\b([A-Z][a-zA-Z\s&.,-]+?)\s+v\.?\s+([A-Z][a-zA-Z\s&.,-]+?)\b'
    matches = re.findall(pattern, query)

    parties = []
    for match in matches:
        parties.extend([p.strip() for p in match if p.strip()])

    return parties


def normalize_case_citation(citation: str) -> str:
    """
    Normalize a case citation to standard format.

    Args:
        citation: Raw citation string

    Returns:
        Normalized citation
    """
    citation = citation.strip()

    # Apply citation normalization patterns
    for pattern, replacement in CITATION_NORMALIZATIONS:
        citation = re.sub(pattern, replacement, citation, flags=re.IGNORECASE)

    return citation


def remove_stop_words(text: str) -> str:
    """
    Remove legal stop words from text.

    Args:
        text: Input text

    Returns:
        Text with stop words removed
    """
    words = text.lower().split()
    filtered_words = [w for w in words if w not in LEGAL_STOP_WORDS]
    return ' '.join(filtered_words)


def extract_statutory_references(query: str) -> List[str]:
    """
    Extract statutory references (e.g., "42 U.S.C. § 1983", "28 C.F.R. § 35.130").

    Args:
        query: Legal query text

    Returns:
        List of statutory references
    """
    patterns = [
        r'\d+\s+U\.S\.C\.\s+§\s*\d+',
        r'\d+\s+C\.F\.R\.\s+§\s*\d+',
        r'Title\s+\d+',
        r'Section\s+\d+',
    ]

    references = []
    for pattern in patterns:
        matches = re.findall(pattern, query, re.IGNORECASE)
        references.extend(matches)

    return references


def identify_legal_issues(query: str) -> List[str]:
    """
    Identify key legal issues mentioned in the query.

    Args:
        query: Legal query text

    Returns:
        List of identified legal issues
    """
    query_lower = query.lower()
    issues = []

    # Check for procedural issues
    procedural_keywords = {
        "motion to dismiss": "motion_to_dismiss",
        "summary judgment": "summary_judgment",
        "discovery": "discovery",
        "jurisdiction": "subject_matter_jurisdiction",
        "venue": "venue",
        "standing": "standing",
        "statute of limitations": "statute_of_limitations",
        "res judicata": "res_judicata",
        "collateral estoppel": "collateral_estoppel",
    }

    for keyword, issue in procedural_keywords.items():
        if keyword in query_lower:
            issues.append(issue)

    # Check for substantive issues
    substantive_keywords = {
        "breach of contract": "contract_breach",
        "negligence": "negligence",
        "fraud": "fraud",
        "defamation": "defamation",
        "discrimination": "discrimination",
        "harassment": "harassment",
        "constitutional": "constitutional_law",
        "first amendment": "first_amendment",
        "fourth amendment": "fourth_amendment",
        "due process": "due_process",
        "equal protection": "equal_protection",
    }

    for keyword, issue in substantive_keywords.items():
        if keyword in query_lower:
            issues.append(issue)

    return issues


def semantic_similarity(term1: str, term2: str) -> float:
    """
    Calculate basic semantic similarity between two legal terms.
    Uses synonym matching and string similarity.

    Args:
        term1: First legal term
        term2: Second legal term

    Returns:
        Similarity score (0.0 to 1.0)
    """
    term1_lower = term1.lower().strip()
    term2_lower = term2.lower().strip()

    # Exact match
    if term1_lower == term2_lower:
        return 1.0

    # Check if one is a synonym of the other
    synonyms1 = set(expand_synonyms(term1_lower))
    synonyms2 = set(expand_synonyms(term2_lower))

    if term2_lower in synonyms1 or term1_lower in synonyms2:
        return 0.9

    # Check for partial overlap in synonyms
    overlap = synonyms1.intersection(synonyms2)
    if overlap:
        return 0.7

    # Basic string similarity (Jaccard similarity on character bigrams)
    bigrams1 = set(term1_lower[i:i+2] for i in range(len(term1_lower) - 1))
    bigrams2 = set(term2_lower[i:i+2] for i in range(len(term2_lower) - 1))

    if not bigrams1 or not bigrams2:
        return 0.0

    intersection = len(bigrams1.intersection(bigrams2))
    union = len(bigrams1.union(bigrams2))

    return intersection / union if union > 0 else 0.0


# ═══════════════════════════════════════════════════════════════════
# LOGGING
# ═══════════════════════════════════════════════════════════════════

logger.info("LIE semantic normalization module loaded")
logger.info(f"Legal abbreviations: {len(LEGAL_ABBREVIATIONS)}")
logger.info(f"Legal synonyms: {len(LEGAL_SYNONYMS)}")
logger.info(f"Jurisdiction aliases: {len(JURISDICTION_ALIASES)}")
