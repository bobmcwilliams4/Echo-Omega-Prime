"""
LIE Search Module — Legal knowledge retrieval and case law search.

Provides search capabilities across legal knowledge bases, case law databases,
and statutory references. Integrates with cloud retrieval and local doctrine cache.

Commander: Bobby Don McWilliams II | Authority: 11.0 SOVEREIGN
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Tuple

from loguru import logger


# ═══════════════════════════════════════════════════════════════════
# SEARCH RESULT MODELS
# ═══════════════════════════════════════════════════════════════════

@dataclass
class CaseLawResult:
    """Single case law search result."""
    case_name: str
    citation: str
    court: str
    year: int
    holding: str
    relevance_score: float
    jurisdiction: str
    url: Optional[str] = None


@dataclass
class StatutoryResult:
    """Single statutory search result."""
    title: str
    citation: str
    text: str
    relevance_score: float
    jurisdiction: str
    effective_date: Optional[str] = None
    url: Optional[str] = None


@dataclass
class DoctrineResult:
    """Single doctrine block search result."""
    topic: str
    conclusion: str
    relevance_score: float
    keywords: List[str]
    authority: List[str]


@dataclass
class SearchResults:
    """Aggregated search results across all sources."""
    query: str
    case_law: List[CaseLawResult]
    statutes: List[StatutoryResult]
    doctrines: List[DoctrineResult]
    total_results: int
    search_time_ms: float


# ═══════════════════════════════════════════════════════════════════
# CASE LAW SEARCH PATTERNS
# ═══════════════════════════════════════════════════════════════════

# Federal reporters
FEDERAL_REPORTERS = {
    "U.S.": "United States Reports (Supreme Court)",
    "S.Ct.": "Supreme Court Reporter",
    "L.Ed.": "Lawyers' Edition",
    "F.": "Federal Reporter (Courts of Appeals)",
    "F.2d": "Federal Reporter, Second Series",
    "F.3d": "Federal Reporter, Third Series",
    "F.4th": "Federal Reporter, Fourth Series",
    "F.Supp.": "Federal Supplement (District Courts)",
    "F.Supp.2d": "Federal Supplement, Second Series",
    "F.Supp.3d": "Federal Supplement, Third Series",
}

# State reporters (sample)
STATE_REPORTERS = {
    "S.W.": "South Western Reporter",
    "S.W.2d": "South Western Reporter, Second Series",
    "S.W.3d": "South Western Reporter, Third Series",
    "N.E.": "North Eastern Reporter",
    "N.E.2d": "North Eastern Reporter, Second Series",
    "N.E.3d": "North Eastern Reporter, Third Series",
    "P.": "Pacific Reporter",
    "P.2d": "Pacific Reporter, Second Series",
    "P.3d": "Pacific Reporter, Third Series",
    "A.": "Atlantic Reporter",
    "A.2d": "Atlantic Reporter, Second Series",
    "A.3d": "Atlantic Reporter, Third Series",
    "So.": "Southern Reporter",
    "So.2d": "Southern Reporter, Second Series",
    "So.3d": "Southern Reporter, Third Series",
    "S.E.": "South Eastern Reporter",
    "S.E.2d": "South Eastern Reporter, Second Series",
    "N.W.": "North Western Reporter",
    "N.W.2d": "North Western Reporter, Second Series",
}


# ═══════════════════════════════════════════════════════════════════
# CITATION PARSING
# ═══════════════════════════════════════════════════════════════════

def parse_citation(citation: str) -> Optional[Dict[str, Any]]:
    """
    Parse a legal citation into components.

    Args:
        citation: Citation string (e.g., "410 U.S. 113 (1973)")

    Returns:
        Dictionary with citation components or None if unparsable
    """
    citation = citation.strip()

    # Pattern: "Volume Reporter Page (Year)"
    # Example: 410 U.S. 113 (1973)
    pattern = r'(\d+)\s+([A-Za-z.]+\d?[a-z]*)\s+(\d+)\s*(?:\((\d{4})\))?'
    match = re.match(pattern, citation)

    if not match:
        return None

    volume, reporter, page, year = match.groups()

    court = "Unknown"
    if reporter in FEDERAL_REPORTERS:
        court = FEDERAL_REPORTERS[reporter]
    elif reporter in STATE_REPORTERS:
        court = STATE_REPORTERS[reporter]

    return {
        "volume": int(volume),
        "reporter": reporter,
        "page": int(page),
        "year": int(year) if year else None,
        "court": court,
        "full_citation": citation,
    }


def identify_court_from_reporter(reporter: str) -> str:
    """
    Identify the court from the reporter abbreviation.

    Args:
        reporter: Reporter abbreviation (e.g., "U.S.", "F.3d")

    Returns:
        Court name
    """
    if reporter == "U.S." or reporter == "S.Ct.":
        return "Supreme Court of the United States"
    elif reporter.startswith("F."):
        return "United States Court of Appeals"
    elif reporter.startswith("F.Supp"):
        return "United States District Court"
    elif reporter in STATE_REPORTERS:
        return "State Court"
    else:
        return "Unknown Court"


# ═══════════════════════════════════════════════════════════════════
# RELEVANCE SCORING
# ═══════════════════════════════════════════════════════════════════

def calculate_relevance_score(
    query: str,
    text: str,
    title: str = "",
    keywords: Optional[List[str]] = None,
) -> float:
    """
    Calculate relevance score for a search result.

    Scoring factors:
    - Exact phrase match: +0.5
    - Keyword matches: +0.1 per keyword (max 0.5)
    - Title match: +0.3
    - Query term frequency in text: +0.0 to 0.3

    Args:
        query: Search query
        text: Result text
        title: Result title
        keywords: Optional list of keywords

    Returns:
        Relevance score (0.0 to 1.0+)
    """
    score = 0.0
    query_lower = query.lower()
    text_lower = text.lower()
    title_lower = title.lower() if title else ""

    # Exact phrase match in text
    if query_lower in text_lower:
        score += 0.5

    # Title match
    if title and query_lower in title_lower:
        score += 0.3

    # Keyword matches
    if keywords:
        query_terms = set(query_lower.split())
        keyword_terms = set(k.lower() for k in keywords)
        overlap = query_terms.intersection(keyword_terms)
        score += min(len(overlap) * 0.1, 0.5)

    # Term frequency in text
    query_terms = query_lower.split()
    term_count = sum(text_lower.count(term) for term in query_terms)
    text_length = len(text_lower.split())

    if text_length > 0:
        term_frequency = term_count / text_length
        score += min(term_frequency * 10, 0.3)  # Cap at 0.3

    # Normalize to 0.0-1.0 range (but allow scores > 1.0 for exceptional matches)
    return round(score, 3)


# ═══════════════════════════════════════════════════════════════════
# CASE LAW SEARCH (MOCK — Production would use Westlaw/Lexis API)
# ═══════════════════════════════════════════════════════════════════

# Mock case law database (in production, this would be Westlaw/Lexis API)
MOCK_CASE_LAW_DATABASE: List[Dict[str, Any]] = [
    {
        "case_name": "Miranda v. Arizona",
        "citation": "384 U.S. 436 (1966)",
        "court": "Supreme Court of the United States",
        "year": 1966,
        "holding": "Police must inform suspects of Fifth Amendment rights before custodial interrogation.",
        "jurisdiction": "federal",
        "keywords": ["miranda", "custodial interrogation", "fifth amendment", "self-incrimination"],
    },
    {
        "case_name": "Chevron U.S.A. Inc. v. NRDC",
        "citation": "467 U.S. 837 (1984)",
        "court": "Supreme Court of the United States",
        "year": 1984,
        "holding": "Courts defer to reasonable agency interpretations of ambiguous statutes.",
        "jurisdiction": "federal",
        "keywords": ["chevron", "deference", "agency", "ambiguity", "administrative law"],
    },
    {
        "case_name": "Bell Atlantic Corp. v. Twombly",
        "citation": "550 U.S. 544 (2007)",
        "court": "Supreme Court of the United States",
        "year": 2007,
        "holding": "Complaint must plead factual content making claim plausible, not merely conceivable.",
        "jurisdiction": "federal",
        "keywords": ["plausibility", "pleading", "12(b)(6)", "motion to dismiss"],
    },
    {
        "case_name": "McDonnell Douglas Corp. v. Green",
        "citation": "411 U.S. 792 (1973)",
        "court": "Supreme Court of the United States",
        "year": 1973,
        "holding": "Burden-shifting framework for employment discrimination claims under Title VII.",
        "jurisdiction": "federal",
        "keywords": ["burden shifting", "prima facie", "discrimination", "title vii", "employment"],
    },
    {
        "case_name": "Erie Railroad Co. v. Tompkins",
        "citation": "304 U.S. 64 (1938)",
        "court": "Supreme Court of the United States",
        "year": 1938,
        "holding": "Federal courts in diversity must apply state substantive law and federal procedural law.",
        "jurisdiction": "federal",
        "keywords": ["erie", "diversity", "substantive", "procedural", "choice of law"],
    },
    {
        "case_name": "Campbell v. Acuff-Rose Music, Inc.",
        "citation": "510 U.S. 569 (1994)",
        "court": "Supreme Court of the United States",
        "year": 1994,
        "holding": "Transformative use weighs heavily in favor of fair use defense to copyright infringement.",
        "jurisdiction": "federal",
        "keywords": ["fair use", "transformative", "copyright", "parody"],
    },
]


def search_case_law(query: str, limit: int = 10) -> List[CaseLawResult]:
    """
    Search case law database (mock implementation).

    Args:
        query: Search query
        limit: Maximum results to return

    Returns:
        List of case law results
    """
    query_lower = query.lower()
    results = []

    for case in MOCK_CASE_LAW_DATABASE:
        # Calculate relevance
        text = f"{case['case_name']} {case['holding']}"
        score = calculate_relevance_score(
            query=query,
            text=text,
            title=case['case_name'],
            keywords=case.get('keywords', []),
        )

        if score > 0.1:  # Minimum threshold
            results.append(CaseLawResult(
                case_name=case['case_name'],
                citation=case['citation'],
                court=case['court'],
                year=case['year'],
                holding=case['holding'],
                relevance_score=score,
                jurisdiction=case['jurisdiction'],
                url=None,
            ))

    # Sort by relevance
    results.sort(key=lambda r: r.relevance_score, reverse=True)

    return results[:limit]


# ═══════════════════════════════════════════════════════════════════
# STATUTORY SEARCH (MOCK — Production would use USC/CFR API)
# ═══════════════════════════════════════════════════════════════════

MOCK_STATUTORY_DATABASE: List[Dict[str, Any]] = [
    {
        "title": "Diversity jurisdiction",
        "citation": "28 U.S.C. § 1332",
        "text": "The district courts shall have original jurisdiction of all civil actions where the matter in controversy exceeds $75,000 and is between citizens of different States.",
        "jurisdiction": "federal",
        "keywords": ["diversity", "jurisdiction", "amount in controversy", "citizenship"],
    },
    {
        "title": "Federal question jurisdiction",
        "citation": "28 U.S.C. § 1331",
        "text": "The district courts shall have original jurisdiction of all civil actions arising under the Constitution, laws, or treaties of the United States.",
        "jurisdiction": "federal",
        "keywords": ["federal question", "jurisdiction", "arising under"],
    },
    {
        "title": "Asylum",
        "citation": "8 U.S.C. § 1158",
        "text": "Any alien who is physically present in the United States or who arrives in the United States may apply for asylum.",
        "jurisdiction": "federal",
        "keywords": ["asylum", "immigration", "persecution", "refugee"],
    },
    {
        "title": "Fair use",
        "citation": "17 U.S.C. § 107",
        "text": "The fair use of a copyrighted work for purposes such as criticism, comment, news reporting, teaching, scholarship, or research is not an infringement of copyright.",
        "jurisdiction": "federal",
        "keywords": ["fair use", "copyright", "criticism", "transformative"],
    },
]


def search_statutes(query: str, limit: int = 10) -> List[StatutoryResult]:
    """
    Search statutory database (mock implementation).

    Args:
        query: Search query
        limit: Maximum results to return

    Returns:
        List of statutory results
    """
    query_lower = query.lower()
    results = []

    for statute in MOCK_STATUTORY_DATABASE:
        # Calculate relevance
        text = f"{statute['title']} {statute['text']}"
        score = calculate_relevance_score(
            query=query,
            text=text,
            title=statute['title'],
            keywords=statute.get('keywords', []),
        )

        if score > 0.1:  # Minimum threshold
            results.append(StatutoryResult(
                title=statute['title'],
                citation=statute['citation'],
                text=statute['text'],
                relevance_score=score,
                jurisdiction=statute['jurisdiction'],
                effective_date=None,
                url=None,
            ))

    # Sort by relevance
    results.sort(key=lambda r: r.relevance_score, reverse=True)

    return results[:limit]


# ═══════════════════════════════════════════════════════════════════
# DOCTRINE SEARCH (searches loaded doctrine blocks)
# ═══════════════════════════════════════════════════════════════════

def search_doctrines(
    query: str,
    doctrine_blocks: Dict[str, Any],
    limit: int = 10,
) -> List[DoctrineResult]:
    """
    Search doctrine blocks for relevant topics.

    Args:
        query: Search query
        doctrine_blocks: Dictionary of doctrine blocks to search
        limit: Maximum results to return

    Returns:
        List of doctrine results
    """
    query_lower = query.lower()
    results = []

    for topic, doctrine in doctrine_blocks.items():
        # Build searchable text
        keywords = doctrine.keywords if hasattr(doctrine, 'keywords') else []
        conclusion = doctrine.conclusion_template if hasattr(doctrine, 'conclusion_template') else ""
        authority = doctrine.primary_authority if hasattr(doctrine, 'primary_authority') else []

        text = f"{topic} {conclusion} {' '.join(keywords)}"

        # Calculate relevance
        score = calculate_relevance_score(
            query=query,
            text=text,
            title=topic,
            keywords=keywords,
        )

        if score > 0.1:  # Minimum threshold
            results.append(DoctrineResult(
                topic=topic,
                conclusion=conclusion,
                relevance_score=score,
                keywords=keywords,
                authority=authority,
            ))

    # Sort by relevance
    results.sort(key=lambda r: r.relevance_score, reverse=True)

    return results[:limit]


# ═══════════════════════════════════════════════════════════════════
# UNIFIED SEARCH INTERFACE
# ═══════════════════════════════════════════════════════════════════

def unified_search(
    query: str,
    doctrine_blocks: Optional[Dict[str, Any]] = None,
    include_case_law: bool = True,
    include_statutes: bool = True,
    include_doctrines: bool = True,
    limit_per_source: int = 5,
) -> SearchResults:
    """
    Perform unified search across all legal knowledge sources.

    Args:
        query: Search query
        doctrine_blocks: Optional doctrine blocks to search
        include_case_law: Include case law results
        include_statutes: Include statutory results
        include_doctrines: Include doctrine results
        limit_per_source: Max results per source

    Returns:
        SearchResults object with aggregated results
    """
    import time
    start_time = time.time()

    case_law_results = []
    statutory_results = []
    doctrine_results = []

    if include_case_law:
        case_law_results = search_case_law(query, limit=limit_per_source)

    if include_statutes:
        statutory_results = search_statutes(query, limit=limit_per_source)

    if include_doctrines and doctrine_blocks:
        doctrine_results = search_doctrines(query, doctrine_blocks, limit=limit_per_source)

    search_time_ms = (time.time() - start_time) * 1000
    total_results = len(case_law_results) + len(statutory_results) + len(doctrine_results)

    return SearchResults(
        query=query,
        case_law=case_law_results,
        statutes=statutory_results,
        doctrines=doctrine_results,
        total_results=total_results,
        search_time_ms=round(search_time_ms, 2),
    )


# ═══════════════════════════════════════════════════════════════════
# SHEPARDIZE / KEYCITE (CITATION VALIDATION)
# ═══════════════════════════════════════════════════════════════════

def shepardize_citation(citation: str) -> Dict[str, Any]:
    """
    Validate citation and check treatment (mock implementation).
    In production, this would integrate with Shepard's Citations or KeyCite.

    Args:
        citation: Citation to validate

    Returns:
        Dictionary with citation status
    """
    parsed = parse_citation(citation)

    if not parsed:
        return {
            "citation": citation,
            "valid": False,
            "status": "UNPARSABLE",
            "treatment": None,
        }

    # Mock validation
    return {
        "citation": citation,
        "valid": True,
        "status": "GOOD_LAW",
        "treatment": "Still good law, not overruled or questioned",
        "court": parsed['court'],
        "year": parsed['year'],
    }


# ═══════════════════════════════════════════════════════════════════
# BOOLEAN SEARCH PARSER
# ═══════════════════════════════════════════════════════════════════

def parse_boolean_query(query: str) -> Dict[str, Any]:
    """
    Parse a Boolean search query (AND, OR, NOT, proximity).

    Args:
        query: Boolean query string (e.g., "contract AND breach NOT fraud")

    Returns:
        Dictionary with parsed query structure
    """
    # Simple implementation: split on operators
    terms = []
    operators = []

    # Normalize operators
    query = query.replace(" and ", " AND ").replace(" or ", " OR ").replace(" not ", " NOT ")

    # Split by operators
    parts = re.split(r'\s+(AND|OR|NOT)\s+', query)

    for i, part in enumerate(parts):
        if part.upper() in ["AND", "OR", "NOT"]:
            operators.append(part.upper())
        else:
            terms.append(part.strip())

    return {
        "terms": terms,
        "operators": operators,
        "original_query": query,
    }


# ═══════════════════════════════════════════════════════════════════
# LOGGING
# ═══════════════════════════════════════════════════════════════════

logger.info("LIE search module loaded")
logger.info(f"Mock case law database: {len(MOCK_CASE_LAW_DATABASE)} cases")
logger.info(f"Mock statutory database: {len(MOCK_STATUTORY_DATABASE)} statutes")
