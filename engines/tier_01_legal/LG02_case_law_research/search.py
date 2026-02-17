"""
LG02 Case Law Research Engine - Search Layer
==============================================
Authority: 11.0 SOVEREIGN | Echo Omega Prime
Version: 2.0.0 | Port: 8392

Provides fast semantic search over doctrine blocks using an inverted index
with TF-IDF scoring, plus Shepardize-style citation verification, precedent
chain tracking, and court hierarchy weight calculations.

Architecture Position:
    QUERY NORMALIZATION
        |
        v
    DOCTRINE CACHE (exact/keyword match)
        |  miss
        v
    TF-IDF SEARCH (this layer) -- ranked results with relevance scores
        |  miss
        v
    CITATION ANALYSIS -- parsing, Shepardize, precedent chains
        |  miss
        v
    DEEP ANALYSIS (full synthesis)

Author: ECHO OMEGA PRIME
"""

from __future__ import annotations

import hashlib
import math
import re
import time
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, FrozenSet, List, Optional, Set, Tuple

from loguru import logger


# ============================================================================
# CONSTANTS
# ============================================================================

DEFAULT_TOP_K: int = 5
SCORE_THRESHOLD: float = 0.3
MIN_TOKEN_LENGTH: int = 2
MAX_TOKEN_LENGTH: int = 50

# Legal stopwords
LEGAL_STOPWORDS: FrozenSet[str] = frozenset({
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "are", "was", "were", "be", "been",
    "being", "have", "has", "had", "do", "does", "did", "will", "would",
    "could", "should", "may", "might", "shall", "can", "must", "need",
    "this", "that", "these", "those", "it", "its", "they", "them", "their",
    "we", "our", "you", "your", "he", "she", "his", "her", "not", "no",
    "if", "then", "than", "when", "where", "which", "who", "whom", "what",
    "how", "all", "each", "every", "any", "some", "such", "more", "most",
    "other", "into", "over", "under", "between", "through", "about",
    "also", "very", "just", "only", "still", "even", "so", "as", "up",
    "out", "there", "here", "own", "same", "both", "either", "neither",
    "nor", "whether", "while", "until", "after", "before", "during",
    "above", "below", "upon", "within", "without", "against",
})

# Legal term boosts -- weight tokens that are highly discriminative
LEGAL_TERM_BOOST: Dict[str, float] = {
    "stare": 2.0, "decisis": 2.0, "precedent": 1.8,
    "standing": 1.5, "jurisdiction": 1.6, "certiorari": 2.0,
    "injunction": 1.7, "summary": 1.5, "judgment": 1.3,
    "dismiss": 1.5, "hearsay": 1.8, "daubert": 2.0,
    "miranda": 2.0, "chevron": 2.0, "erie": 2.0,
    "negligence": 1.5, "fiduciary": 1.7, "breach": 1.3,
    "estoppel": 1.8, "preclusion": 1.8, "res": 1.5,
    "judicata": 2.0, "collateral": 1.5, "qualified": 1.3,
    "immunity": 1.5, "amendment": 1.3, "constitutional": 1.5,
    "arbitration": 1.6, "securities": 1.5, "fraud": 1.3,
    "bankruptcy": 1.6, "stay": 1.3, "copyright": 1.5,
    "fair": 1.2, "use": 1.0, "patent": 1.5,
    "trademark": 1.5, "infringement": 1.5, "deference": 1.7,
    "tort": 1.5, "contract": 1.3, "formation": 1.3,
    "probable": 1.5, "cause": 1.2, "warrant": 1.5,
    "exclusionary": 1.7, "suppression": 1.5, "class": 1.3,
    "certification": 1.5, "numerosity": 2.0, "commonality": 2.0,
    "typicality": 2.0, "adequacy": 1.5, "predominance": 1.8,
    "superiority": 1.5, "scienter": 2.0, "materiality": 1.7,
    "reliance": 1.5, "causation": 1.5, "mootness": 2.0,
    "ripeness": 2.0, "political": 1.3, "question": 1.0,
    "overruled": 2.0, "reversed": 1.8, "vacated": 1.8,
    "affirmed": 1.5, "remanded": 1.5, "distinguished": 1.7,
    "shepardize": 2.5, "keycite": 2.5, "bluebook": 2.0,
    "pinpoint": 1.8, "citation": 1.5, "reporter": 1.5,
}

# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass(frozen=True)
class SearchResult:
    """A single search result with relevance scoring."""
    doctrine_key: str
    topic: str
    score: float
    matched_terms: Tuple[str, ...]
    snippet: str
    court_level: str = ""
    authority_weight: int = 75

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "doctrine_key": self.doctrine_key,
            "topic": self.topic,
            "score": round(self.score, 4),
            "matched_terms": list(self.matched_terms),
            "snippet": self.snippet[:300],
            "court_level": self.court_level,
            "authority_weight": self.authority_weight,
        }


@dataclass
class ParsedCitation:
    """A fully parsed legal citation with all components."""
    raw: str
    volume: int = 0
    reporter: str = ""
    page: int = 0
    pinpoint_page: int = 0
    court: str = ""
    year: int = 0
    party_v_party: str = ""
    citation_type: str = "case"  # case, statute, regulation, rule
    reporter_series: str = ""
    court_level: str = ""
    court_weight: int = 50
    jurisdiction: str = ""
    is_valid: bool = False
    parse_confidence: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "raw": self.raw,
            "volume": self.volume,
            "reporter": self.reporter,
            "page": self.page,
            "pinpoint_page": self.pinpoint_page,
            "court": self.court,
            "year": self.year,
            "party_v_party": self.party_v_party,
            "citation_type": self.citation_type,
            "reporter_series": self.reporter_series,
            "court_level": self.court_level,
            "court_weight": self.court_weight,
            "jurisdiction": self.jurisdiction,
            "is_valid": self.is_valid,
            "parse_confidence": round(self.parse_confidence, 3),
        }


@dataclass
class ShepardizeResult:
    """Result of Shepardizing a citation."""
    citation: str
    signal: str  # green, yellow, red, blue
    signal_label: str  # Good Law, Caution, Negative Treatment, Neutral/Cited
    is_good_law: bool
    treatments: List[Dict[str, str]]  # list of {case, treatment, year}
    citing_count: int = 0
    positive_count: int = 0
    negative_count: int = 0
    neutral_count: int = 0
    warning_count: int = 0
    overruled_by: Optional[str] = None
    distinguished_by: List[str] = field(default_factory=list)
    followed_by: List[str] = field(default_factory=list)
    questioned_by: List[str] = field(default_factory=list)
    last_checked: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "citation": self.citation,
            "signal": self.signal,
            "signal_label": self.signal_label,
            "is_good_law": self.is_good_law,
            "treatments": self.treatments,
            "citing_count": self.citing_count,
            "positive_count": self.positive_count,
            "negative_count": self.negative_count,
            "neutral_count": self.neutral_count,
            "warning_count": self.warning_count,
            "overruled_by": self.overruled_by,
            "distinguished_by": self.distinguished_by[:10],
            "followed_by": self.followed_by[:10],
            "questioned_by": self.questioned_by[:10],
            "last_checked": self.last_checked,
        }


@dataclass
class PrecedentChainNode:
    """A node in a precedent chain (citation graph)."""
    citation: str
    court: str
    year: int
    court_weight: int
    treatment: str  # how this case treated the prior case
    depth: int  # distance from the root citation
    children: List[str] = field(default_factory=list)
    parents: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "citation": self.citation,
            "court": self.court,
            "year": self.year,
            "court_weight": self.court_weight,
            "treatment": self.treatment,
            "depth": self.depth,
            "children": self.children[:20],
            "parents": self.parents[:20],
        }


@dataclass
class PrecedentChainResult:
    """Full precedent chain analysis."""
    root_citation: str
    chain_depth: int
    total_nodes: int
    nodes: List[PrecedentChainNode]
    strongest_path: List[str]
    weakest_link: Optional[str]
    circuit_split_detected: bool
    overruled_in_chain: List[str]

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "root_citation": self.root_citation,
            "chain_depth": self.chain_depth,
            "total_nodes": self.total_nodes,
            "nodes": [n.to_dict() for n in self.nodes],
            "strongest_path": self.strongest_path,
            "weakest_link": self.weakest_link,
            "circuit_split_detected": self.circuit_split_detected,
            "overruled_in_chain": self.overruled_in_chain,
        }


# ============================================================================
# REPORTER METADATA
# ============================================================================

REPORTER_COURT_MAP: Dict[str, Dict[str, Any]] = {
    "U.S.": {"court": "us_supreme_court", "level": "supreme", "weight": 100},
    "S. Ct.": {"court": "us_supreme_court", "level": "supreme", "weight": 100},
    "L. Ed.": {"court": "us_supreme_court", "level": "supreme", "weight": 100},
    "L. Ed. 2d": {"court": "us_supreme_court", "level": "supreme", "weight": 100},
    "F.": {"court": "federal_circuit_court", "level": "appellate", "weight": 85},
    "F.2d": {"court": "federal_circuit_court", "level": "appellate", "weight": 85},
    "F.3d": {"court": "federal_circuit_court", "level": "appellate", "weight": 85},
    "F.4th": {"court": "federal_circuit_court", "level": "appellate", "weight": 85},
    "F. App'x": {"court": "federal_circuit_court", "level": "appellate", "weight": 70},
    "F. Supp.": {"court": "federal_district_court", "level": "trial", "weight": 70},
    "F. Supp. 2d": {"court": "federal_district_court", "level": "trial", "weight": 70},
    "F. Supp. 3d": {"court": "federal_district_court", "level": "trial", "weight": 70},
    "B.R.": {"court": "federal_bankruptcy_court", "level": "trial", "weight": 60},
    "T.C.": {"court": "tax_court", "level": "trial", "weight": 72},
    "T.C.M.": {"court": "tax_court", "level": "trial", "weight": 65},
    "T.C. Memo.": {"court": "tax_court", "level": "trial", "weight": 65},
    "Fed. Cl.": {"court": "court_of_federal_claims", "level": "trial", "weight": 70},
    "A.2d": {"court": "state_court", "level": "varies", "weight": 65},
    "A.3d": {"court": "state_court", "level": "varies", "weight": 65},
    "N.E.2d": {"court": "state_court", "level": "varies", "weight": 65},
    "N.E.3d": {"court": "state_court", "level": "varies", "weight": 65},
    "N.W.2d": {"court": "state_court", "level": "varies", "weight": 65},
    "P.2d": {"court": "state_court", "level": "varies", "weight": 65},
    "P.3d": {"court": "state_court", "level": "varies", "weight": 65},
    "S.E.2d": {"court": "state_court", "level": "varies", "weight": 65},
    "So. 2d": {"court": "state_court", "level": "varies", "weight": 65},
    "So. 3d": {"court": "state_court", "level": "varies", "weight": 65},
    "S.W.2d": {"court": "state_court", "level": "varies", "weight": 65},
    "S.W.3d": {"court": "state_court", "level": "varies", "weight": 65},
}

# Court hierarchy for conflict resolution
COURT_WEIGHT_MAP: Dict[str, int] = {
    "us_supreme_court": 100,
    "federal_circuit_court": 85,
    "federal_district_court": 70,
    "tax_court": 72,
    "court_of_federal_claims": 70,
    "federal_bankruptcy_court": 60,
    "state_supreme_court": 75,
    "state_appellate_court": 60,
    "state_trial_court": 45,
    "state_court": 65,
    "administrative_agency": 55,
}


# ============================================================================
# CITATION PARSER
# ============================================================================

class CitationParser:
    """
    Parses Bluebook-format legal citations into structured components.

    Handles:
    - Standard case citations: 123 F.3d 456 (5th Cir. 1999)
    - Party-style citations: Smith v. Jones, 123 F.3d 456 (5th Cir. 1999)
    - Pinpoint citations: 123 F.3d 456, 460
    - Statute citations: 26 U.S.C. 162
    - Regulation citations: 26 C.F.R. 1.162-1
    - Rule citations: Fed. R. Civ. P. 56
    """

    # Pre-compiled patterns for maximum performance
    _PARTY_PATTERN = re.compile(
        r"([A-Z][a-zA-Z\.\s&,']+?)\s+v\.\s+([A-Z][a-zA-Z\.\s&,']+?),\s*"
        r"(\d+)\s+([A-Za-z][A-Za-z\.\s']+?\d*[a-z]*)\s+(\d+)"
        r"(?:,\s*(\d+))?"
        r"\s*\(([^)]+)\)",
        re.MULTILINE,
    )

    _STANDARD_PATTERN = re.compile(
        r"(\d+)\s+([A-Za-z][A-Za-z\.\s']+?\d*[a-z]*)\s+(\d+)"
        r"(?:,\s*(\d+))?"
        r"\s*\(([^)]+)\)",
    )

    _COURT_YEAR_PATTERN = re.compile(
        r"(?:(\d+)(?:st|nd|rd|th)\s+Cir\.\s*)?(\d{4})",
        re.IGNORECASE,
    )

    _USC_PATTERN = re.compile(
        r"(\d+)\s+U\.?S\.?C\.?\s*(?:\xa7|[Ss]ec(?:tion)?\.?)\s*"
        r"(\d+[a-zA-Z]*(?:\([a-zA-Z0-9]+\))*)",
    )

    _CFR_PATTERN = re.compile(
        r"(\d+)\s+C\.?F\.?R\.?\s*(?:\xa7|[Ss]ec(?:tion)?\.?)\s*"
        r"([\d]+(?:\.[\d\w\-]+)*)",
    )

    _IRC_PATTERN = re.compile(
        r"I\.?R\.?C\.?\s*(?:\xa7|[Ss]ec(?:tion)?\.?)\s*"
        r"(\d+[a-zA-Z]*(?:\([a-zA-Z0-9]+\))*)",
    )

    _FRCP_PATTERN = re.compile(
        r"Fed\.\s*R\.\s*Civ\.\s*P\.\s*(\d+)(?:\(([a-zA-Z0-9]+)\))?",
        re.IGNORECASE,
    )

    _FRE_PATTERN = re.compile(
        r"Fed\.\s*R\.\s*Evid\.\s*(\d+)(?:\(([a-zA-Z0-9]+)\))?",
        re.IGNORECASE,
    )

    def __init__(self) -> None:
        self._parse_count: int = 0
        self._success_count: int = 0
        self._fail_count: int = 0

    def parse(self, raw_citation: str) -> ParsedCitation:
        """Parse a raw citation string into structured components."""
        self._parse_count += 1
        raw = raw_citation.strip()

        if not raw:
            self._fail_count += 1
            return ParsedCitation(raw=raw, is_valid=False, parse_confidence=0.0)

        # Try party-style citation first (most specific case format)
        result = self._try_party_style(raw)
        if result and result.is_valid:
            self._success_count += 1
            return result

        # Try statute citations BEFORE standard case pattern
        # because "26 U.S.C. Sec. 162" falsely matches vol-reporter-page
        result = self._try_statute(raw)
        if result and result.is_valid:
            self._success_count += 1
            return result

        # Try rule citations before standard case pattern
        result = self._try_rule(raw)
        if result and result.is_valid:
            self._success_count += 1
            return result

        # Try standard volume-reporter-page (least specific, checked last)
        result = self._try_standard(raw)
        if result and result.is_valid:
            self._success_count += 1
            return result

        self._fail_count += 1
        return ParsedCitation(raw=raw, is_valid=False, parse_confidence=0.1)

    def _try_party_style(self, raw: str) -> Optional[ParsedCitation]:
        """Try to parse as Party v. Party, Vol Reporter Page (Court Year)."""
        match = self._PARTY_PATTERN.search(raw)
        if not match:
            return None

        plaintiff = match.group(1).strip()
        defendant = match.group(2).strip()
        volume = int(match.group(3))
        reporter = match.group(4).strip()
        page = int(match.group(5))
        pinpoint = int(match.group(6)) if match.group(6) else 0
        court_year = match.group(7).strip()

        court, year = self._parse_court_year(court_year)
        reporter_meta = self._identify_reporter(reporter)

        return ParsedCitation(
            raw=raw,
            volume=volume,
            reporter=reporter,
            page=page,
            pinpoint_page=pinpoint,
            court=court or reporter_meta.get("court", ""),
            year=year,
            party_v_party=f"{plaintiff} v. {defendant}",
            citation_type="case",
            reporter_series=reporter,
            court_level=reporter_meta.get("level", ""),
            court_weight=reporter_meta.get("weight", 50),
            jurisdiction=self._infer_jurisdiction(court),
            is_valid=True,
            parse_confidence=0.95,
        )

    def _try_standard(self, raw: str) -> Optional[ParsedCitation]:
        """Try to parse as Vol Reporter Page (Court Year)."""
        match = self._STANDARD_PATTERN.search(raw)
        if not match:
            return None

        volume = int(match.group(1))
        reporter = match.group(2).strip()
        page = int(match.group(3))
        pinpoint = int(match.group(4)) if match.group(4) else 0
        court_year = match.group(5).strip()

        court, year = self._parse_court_year(court_year)
        reporter_meta = self._identify_reporter(reporter)

        return ParsedCitation(
            raw=raw,
            volume=volume,
            reporter=reporter,
            page=page,
            pinpoint_page=pinpoint,
            court=court or reporter_meta.get("court", ""),
            year=year,
            citation_type="case",
            reporter_series=reporter,
            court_level=reporter_meta.get("level", ""),
            court_weight=reporter_meta.get("weight", 50),
            jurisdiction=self._infer_jurisdiction(court),
            is_valid=True,
            parse_confidence=0.85,
        )

    def _try_statute(self, raw: str) -> Optional[ParsedCitation]:
        """Try to parse as a statutory citation."""
        # USC
        match = self._USC_PATTERN.search(raw)
        if match:
            title = int(match.group(1))
            section = match.group(2)
            return ParsedCitation(
                raw=raw,
                volume=title,
                reporter="U.S.C.",
                page=0,
                court="congress",
                citation_type="statute",
                court_level="legislative",
                court_weight=95,
                jurisdiction="federal",
                is_valid=True,
                parse_confidence=0.90,
                party_v_party=f"{title} U.S.C. {section}",
            )

        # CFR
        match = self._CFR_PATTERN.search(raw)
        if match:
            title = int(match.group(1))
            section = match.group(2)
            return ParsedCitation(
                raw=raw,
                volume=title,
                reporter="C.F.R.",
                page=0,
                court="executive_agency",
                citation_type="regulation",
                court_level="administrative",
                court_weight=75,
                jurisdiction="federal",
                is_valid=True,
                parse_confidence=0.90,
                party_v_party=f"{title} C.F.R. {section}",
            )

        # IRC
        match = self._IRC_PATTERN.search(raw)
        if match:
            section = match.group(1)
            return ParsedCitation(
                raw=raw,
                volume=26,
                reporter="I.R.C.",
                page=0,
                court="congress",
                citation_type="statute",
                court_level="legislative",
                court_weight=95,
                jurisdiction="federal",
                is_valid=True,
                parse_confidence=0.90,
                party_v_party=f"I.R.C. {section}",
            )

        return None

    def _try_rule(self, raw: str) -> Optional[ParsedCitation]:
        """Try to parse as a procedural rule citation."""
        # FRCP
        match = self._FRCP_PATTERN.search(raw)
        if match:
            rule_num = match.group(1)
            subsection = match.group(2) or ""
            return ParsedCitation(
                raw=raw,
                reporter="Fed. R. Civ. P.",
                citation_type="rule",
                court_level="procedural",
                court_weight=90,
                jurisdiction="federal",
                is_valid=True,
                parse_confidence=0.90,
                party_v_party=f"Fed. R. Civ. P. {rule_num}" + (f"({subsection})" if subsection else ""),
            )

        # FRE
        match = self._FRE_PATTERN.search(raw)
        if match:
            rule_num = match.group(1)
            subsection = match.group(2) or ""
            return ParsedCitation(
                raw=raw,
                reporter="Fed. R. Evid.",
                citation_type="rule",
                court_level="procedural",
                court_weight=90,
                jurisdiction="federal",
                is_valid=True,
                parse_confidence=0.90,
                party_v_party=f"Fed. R. Evid. {rule_num}" + (f"({subsection})" if subsection else ""),
            )

        return None

    def _parse_court_year(self, court_year_str: str) -> Tuple[str, int]:
        """Extract court name and year from parenthetical."""
        year = 0
        court = ""

        # Extract year (last 4-digit number)
        year_match = re.search(r"(\d{4})", court_year_str)
        if year_match:
            year = int(year_match.group(1))

        # Extract court (everything except the year)
        court = re.sub(r"\d{4}", "", court_year_str).strip().strip(",").strip()
        if not court:
            court = "unknown"

        return court, year

    def _identify_reporter(self, reporter: str) -> Dict[str, Any]:
        """Identify court metadata from reporter abbreviation."""
        reporter_normalized = reporter.strip()

        # Direct lookup
        if reporter_normalized in REPORTER_COURT_MAP:
            return REPORTER_COURT_MAP[reporter_normalized]

        # Fuzzy match: try stripping trailing dots/spaces
        for key, meta in REPORTER_COURT_MAP.items():
            if reporter_normalized.replace(".", "").replace(" ", "").lower() == key.replace(".", "").replace(" ", "").lower():
                return meta

        return {"court": "unknown", "level": "unknown", "weight": 50}

    def _infer_jurisdiction(self, court: str) -> str:
        """Infer the jurisdiction from a court identifier."""
        court_lower = court.lower()
        if any(term in court_lower for term in ["supreme", "u.s.", "scotus"]):
            return "federal_national"
        if "cir" in court_lower:
            return "federal_circuit"
        if any(term in court_lower for term in ["d.", "dist", "s.d.", "n.d.", "e.d.", "w.d.", "c.d.", "m.d."]):
            return "federal_district"
        if any(term in court_lower for term in ["bankr", "b.r."]):
            return "federal_bankruptcy"
        if "tax" in court_lower or "t.c." in court_lower:
            return "federal_tax"
        if any(term in court_lower for term in ["cal", "tex", "fla", "n.y.", "ill", "ohio", "pa", "ga"]):
            return "state"
        return "unknown"

    def get_stats(self) -> Dict[str, Any]:
        """Get citation parse statistics."""
        return {
            "total_parses": self._parse_count,
            "successful": self._success_count,
            "failed": self._fail_count,
            "success_rate": round(
                self._success_count / max(self._parse_count, 1), 4
            ),
        }


# ============================================================================
# PRECEDENT WEIGHT CALCULATOR
# ============================================================================

class PrecedentWeightCalculator:
    """
    Calculates the authority weight of a legal precedent based on multiple factors:
    - Court level in the hierarchy
    - Age of the decision (recency bonus)
    - Number of citations (influence)
    - Treatment history (positive/negative)
    - Jurisdiction relevance
    - Whether the case has been overruled
    """

    COURT_BASE_WEIGHTS: Dict[str, int] = {
        "us_supreme_court": 100,
        "federal_circuit_court": 85,
        "federal_district_court": 70,
        "tax_court": 72,
        "court_of_federal_claims": 70,
        "federal_bankruptcy_court": 60,
        "state_supreme_court": 75,
        "state_appellate_court": 60,
        "state_trial_court": 45,
        "administrative_agency": 55,
    }

    def calculate_weight(
        self,
        court_level: str,
        year: int,
        citation_count: int = 0,
        positive_treatments: int = 0,
        negative_treatments: int = 0,
        overruled: bool = False,
        same_jurisdiction: bool = True,
        opinion_type: str = "majority",
    ) -> Dict[str, Any]:
        """
        Calculate the composite authority weight of a citation.

        Returns a dictionary with the total weight and component breakdown.
        """
        current_year = datetime.now(timezone.utc).year

        # Base court weight
        base_weight = self.COURT_BASE_WEIGHTS.get(court_level, 50)

        # Age factor: recent cases get a bonus, very old cases get penalized
        age = max(current_year - year, 0)
        if age <= 5:
            age_modifier = 1.10  # 10% bonus for cases < 5 years old
        elif age <= 15:
            age_modifier = 1.0   # No modifier
        elif age <= 30:
            age_modifier = 0.95  # 5% reduction
        elif age <= 50:
            age_modifier = 0.85  # 15% reduction
        else:
            age_modifier = 0.70  # 30% reduction for very old cases

        # Citation influence: logarithmic scaling of citation count
        if citation_count > 0:
            citation_modifier = 1.0 + min(0.15, math.log10(citation_count) * 0.05)
        else:
            citation_modifier = 1.0

        # Treatment modifier
        total_treatments = positive_treatments + negative_treatments
        if total_treatments > 0:
            positive_ratio = positive_treatments / total_treatments
            treatment_modifier = 0.7 + (positive_ratio * 0.3)
        else:
            treatment_modifier = 1.0

        # Overruled: dramatic weight reduction
        if overruled:
            overruled_modifier = 0.05  # 95% weight loss
        else:
            overruled_modifier = 1.0

        # Jurisdiction relevance
        jurisdiction_modifier = 1.0 if same_jurisdiction else 0.7

        # Opinion type modifier
        opinion_modifiers = {
            "majority": 1.0,
            "per_curiam": 0.9,
            "plurality": 0.7,
            "concurrence": 0.4,
            "concurrence_in_judgment": 0.3,
            "dissent": 0.2,
            "syllabus": 0.3,
        }
        opinion_modifier = opinion_modifiers.get(opinion_type, 0.5)

        # Composite weight
        composite = (
            base_weight
            * age_modifier
            * citation_modifier
            * treatment_modifier
            * overruled_modifier
            * jurisdiction_modifier
            * opinion_modifier
        )

        return {
            "total_weight": round(min(composite, 100), 2),
            "base_weight": base_weight,
            "age_modifier": round(age_modifier, 3),
            "age_years": age,
            "citation_modifier": round(citation_modifier, 3),
            "citation_count": citation_count,
            "treatment_modifier": round(treatment_modifier, 3),
            "overruled_modifier": round(overruled_modifier, 3),
            "jurisdiction_modifier": round(jurisdiction_modifier, 3),
            "opinion_modifier": round(opinion_modifier, 3),
            "court_level": court_level,
            "year": year,
            "opinion_type": opinion_type,
            "overruled": overruled,
            "same_jurisdiction": same_jurisdiction,
        }


# ============================================================================
# SHEPARDIZE ENGINE
# ============================================================================

class ShepardizeEngine:
    """
    Simulates Shepard's Citation Service / KeyCite functionality.

    Tracks citation treatment history and generates signals indicating
    whether a case is still good law.

    Note: In production, this would connect to a live citation database.
    This implementation provides the full framework and works with the
    doctrine-cache-based citation network.
    """

    # Known citation treatment database (doctrine-cache-based)
    KNOWN_TREATMENTS: Dict[str, List[Dict[str, str]]] = {
        "Chevron U.S.A., Inc. v. NRDC, 467 U.S. 837 (1984)": [
            {"case": "Loper Bright Enterprises v. Raimondo, 144 S. Ct. 2244 (2024)", "treatment": "overruled", "year": "2024"},
            {"case": "City of Arlington v. FCC, 569 U.S. 290 (2013)", "treatment": "followed", "year": "2013"},
            {"case": "King v. Burwell, 576 U.S. 473 (2015)", "treatment": "discussed", "year": "2015"},
        ],
        "Conley v. Gibson, 355 U.S. 41 (1957)": [
            {"case": "Bell Atlantic Corp. v. Twombly, 550 U.S. 544 (2007)", "treatment": "overruled", "year": "2007"},
        ],
        "Ohio v. Roberts, 448 U.S. 56 (1980)": [
            {"case": "Crawford v. Washington, 541 U.S. 36 (2004)", "treatment": "overruled", "year": "2004"},
        ],
        "Swift v. Tyson, 41 U.S. 1 (1842)": [
            {"case": "Erie Railroad Co. v. Tompkins, 304 U.S. 64 (1938)", "treatment": "overruled", "year": "1938"},
        ],
        "Payne v. Tennessee, 501 U.S. 808 (1991)": [
            {"case": "Dobbs v. Jackson Women's Health Org., 597 U.S. 215 (2022)", "treatment": "followed", "year": "2022"},
            {"case": "Janus v. AFSCME, 138 S. Ct. 2448 (2018)", "treatment": "followed", "year": "2018"},
        ],
        "Lujan v. Defenders of Wildlife, 504 U.S. 555 (1992)": [
            {"case": "TransUnion LLC v. Ramirez, 594 U.S. 413 (2021)", "treatment": "followed", "year": "2021"},
            {"case": "Spokeo, Inc. v. Robins, 578 U.S. 330 (2016)", "treatment": "followed", "year": "2016"},
            {"case": "Clapper v. Amnesty Int'l USA, 568 U.S. 398 (2013)", "treatment": "followed", "year": "2013"},
        ],
    }

    POSITIVE_TREATMENTS = {"followed", "affirmed", "approved", "adopted", "relied_upon", "cited_favorably", "harmonized"}
    NEGATIVE_TREATMENTS = {"overruled", "reversed", "vacated", "abrogated", "superseded", "criticized", "questioned", "limited"}
    WARNING_TREATMENTS = {"modified", "partially_overruled", "narrowed", "called_into_doubt", "declining_to_follow"}
    NEUTRAL_TREATMENTS = {"cited", "discussed", "mentioned", "compared", "distinguished", "explained"}

    def __init__(self) -> None:
        self._lookups: int = 0
        self._hits: int = 0
        self._misses: int = 0

    def shepardize(self, citation: str) -> ShepardizeResult:
        """
        Shepardize a citation to determine its current status.

        Returns a ShepardizeResult with signal color and treatment details.
        """
        self._lookups += 1
        citation_clean = citation.strip()

        treatments = self.KNOWN_TREATMENTS.get(citation_clean, [])

        if not treatments:
            # Check partial match
            for key, val in self.KNOWN_TREATMENTS.items():
                if citation_clean.lower() in key.lower() or key.lower() in citation_clean.lower():
                    treatments = val
                    break

        if treatments:
            self._hits += 1
        else:
            self._misses += 1

        # Classify treatments
        positive_count = sum(1 for t in treatments if t["treatment"] in self.POSITIVE_TREATMENTS)
        negative_count = sum(1 for t in treatments if t["treatment"] in self.NEGATIVE_TREATMENTS)
        neutral_count = sum(1 for t in treatments if t["treatment"] in self.NEUTRAL_TREATMENTS)
        warning_count = sum(1 for t in treatments if t["treatment"] in self.WARNING_TREATMENTS)

        # Determine overruling case
        overruled_by = None
        for t in treatments:
            if t["treatment"] in ("overruled", "reversed", "vacated", "abrogated"):
                overruled_by = t["case"]
                break

        # Extract specific treatment lists
        followed_by = [t["case"] for t in treatments if t["treatment"] in ("followed", "affirmed", "approved")]
        distinguished_by = [t["case"] for t in treatments if t["treatment"] == "distinguished"]
        questioned_by = [t["case"] for t in treatments if t["treatment"] in ("questioned", "criticized")]

        # Determine signal
        if overruled_by:
            signal = "red"
            signal_label = "Negative Treatment"
            is_good_law = False
        elif warning_count > 0 or (negative_count > 0 and negative_count < positive_count):
            signal = "yellow"
            signal_label = "Caution"
            is_good_law = True
        elif positive_count > 0 and negative_count == 0:
            signal = "green"
            signal_label = "Good Law"
            is_good_law = True
        else:
            signal = "blue"
            signal_label = "Neutral/Cited"
            is_good_law = True

        return ShepardizeResult(
            citation=citation_clean,
            signal=signal,
            signal_label=signal_label,
            is_good_law=is_good_law,
            treatments=treatments,
            citing_count=len(treatments),
            positive_count=positive_count,
            negative_count=negative_count,
            neutral_count=neutral_count,
            warning_count=warning_count,
            overruled_by=overruled_by,
            distinguished_by=distinguished_by,
            followed_by=followed_by,
            questioned_by=questioned_by,
        )

    def get_stats(self) -> Dict[str, Any]:
        """Get Shepardize operation statistics."""
        return {
            "total_lookups": self._lookups,
            "hits": self._hits,
            "misses": self._misses,
            "hit_rate": round(self._hits / max(self._lookups, 1), 4),
            "known_citations": len(self.KNOWN_TREATMENTS),
        }


# ============================================================================
# TF-IDF SEARCH INDEX
# ============================================================================

class DoctrineSearchIndex:
    """
    TF-IDF inverted index over doctrine cache entries.

    Features:
    - Fast tokenization with legal stopword removal
    - Legal term boosting
    - Inverted index for sub-linear search
    - Relevance scoring with BM25-like characteristics
    """

    def __init__(self) -> None:
        self._documents: Dict[str, str] = {}
        self._doc_metadata: Dict[str, Dict[str, Any]] = {}
        self._term_doc_freq: Dict[str, int] = {}
        self._inverted_index: Dict[str, Set[str]] = defaultdict(set)
        self._doc_term_freq: Dict[str, Dict[str, int]] = {}
        self._doc_lengths: Dict[str, int] = {}
        self._total_docs: int = 0
        self._avg_doc_length: float = 0.0
        self._query_count: int = 0
        self._miss_queries: List[str] = []
        self._indexed: bool = False

    def add_document(
        self,
        doc_key: str,
        text: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Add a document to the index."""
        self._documents[doc_key] = text
        self._doc_metadata[doc_key] = metadata or {}

        tokens = self._tokenize(text)
        self._doc_lengths[doc_key] = len(tokens)

        term_freq: Dict[str, int] = Counter(tokens)
        self._doc_term_freq[doc_key] = dict(term_freq)

        for term in set(tokens):
            self._inverted_index[term].add(doc_key)

        self._total_docs = len(self._documents)
        if self._total_docs > 0:
            self._avg_doc_length = sum(self._doc_lengths.values()) / self._total_docs

    def build_idf(self) -> None:
        """Pre-compute IDF values."""
        self._term_doc_freq = {
            term: len(docs) for term, docs in self._inverted_index.items()
        }
        self._indexed = True
        logger.info(
            f"Search index built: {self._total_docs} docs, "
            f"{len(self._term_doc_freq)} unique terms"
        )

    def search(
        self,
        query: str,
        top_k: int = DEFAULT_TOP_K,
        threshold: float = SCORE_THRESHOLD,
    ) -> List[SearchResult]:
        """Search the index and return ranked results."""
        self._query_count += 1

        if not self._indexed:
            self.build_idf()

        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []

        # Find candidate documents via inverted index
        candidates: Set[str] = set()
        for token in query_tokens:
            candidates.update(self._inverted_index.get(token, set()))

        if not candidates:
            self._miss_queries.append(query[:200])
            if len(self._miss_queries) > 500:
                self._miss_queries = self._miss_queries[-500:]
            return []

        # Score candidates using BM25-like formula
        k1 = 1.2
        b = 0.75
        scores: List[Tuple[str, float, List[str]]] = []

        for doc_key in candidates:
            score = 0.0
            matched: List[str] = []
            doc_len = self._doc_lengths.get(doc_key, 0)
            doc_tf = self._doc_term_freq.get(doc_key, {})

            for token in query_tokens:
                if token not in doc_tf:
                    continue

                tf = doc_tf[token]
                df = self._term_doc_freq.get(token, 1)
                idf = math.log((self._total_docs - df + 0.5) / (df + 0.5) + 1)

                # BM25 term frequency normalization
                norm_tf = (tf * (k1 + 1)) / (
                    tf + k1 * (1 - b + b * doc_len / max(self._avg_doc_length, 1))
                )

                # Apply legal term boost
                boost = LEGAL_TERM_BOOST.get(token, 1.0)
                score += idf * norm_tf * boost
                matched.append(token)

            if score > threshold:
                scores.append((doc_key, score, matched))

        # Sort by score descending
        scores.sort(key=lambda x: x[1], reverse=True)

        # Build SearchResult objects
        results: List[SearchResult] = []
        for doc_key, score, matched in scores[:top_k]:
            meta = self._doc_metadata.get(doc_key, {})
            text = self._documents.get(doc_key, "")
            snippet = text[:250].replace("\n", " ")

            results.append(SearchResult(
                doctrine_key=doc_key,
                topic=meta.get("topic", doc_key),
                score=score,
                matched_terms=tuple(matched),
                snippet=snippet,
                court_level=meta.get("court_level", ""),
                authority_weight=meta.get("authority_weight", 75),
            ))

        if not results:
            self._miss_queries.append(query[:200])
            if len(self._miss_queries) > 500:
                self._miss_queries = self._miss_queries[-500:]

        return results

    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text with legal stopword removal."""
        tokens = re.findall(r"[a-zA-Z]+", text.lower())
        return [
            t for t in tokens
            if t not in LEGAL_STOPWORDS
            and MIN_TOKEN_LENGTH <= len(t) <= MAX_TOKEN_LENGTH
        ]

    def get_stats(self) -> Dict[str, Any]:
        """Get search index statistics."""
        return {
            "total_documents": self._total_docs,
            "unique_terms": len(self._term_doc_freq),
            "avg_doc_length": round(self._avg_doc_length, 1),
            "total_queries": self._query_count,
            "indexed": self._indexed,
        }

    def get_misses(self, limit: int = 20) -> List[str]:
        """Get recent search misses."""
        return self._miss_queries[-limit:]


# ============================================================================
# SINGLETONS
# ============================================================================

_search_index: Optional[DoctrineSearchIndex] = None
_citation_parser: Optional[CitationParser] = None
_weight_calculator: Optional[PrecedentWeightCalculator] = None
_shepardize_engine: Optional[ShepardizeEngine] = None


def get_search_index() -> DoctrineSearchIndex:
    """Get the global search index instance."""
    global _search_index
    if _search_index is None:
        _search_index = DoctrineSearchIndex()
    return _search_index


def get_citation_parser() -> CitationParser:
    """Get the global citation parser instance."""
    global _citation_parser
    if _citation_parser is None:
        _citation_parser = CitationParser()
    return _citation_parser


def get_weight_calculator() -> PrecedentWeightCalculator:
    """Get the global weight calculator instance."""
    global _weight_calculator
    if _weight_calculator is None:
        _weight_calculator = PrecedentWeightCalculator()
    return _weight_calculator


def get_shepardize_engine() -> ShepardizeEngine:
    """Get the global Shepardize engine instance."""
    global _shepardize_engine
    if _shepardize_engine is None:
        _shepardize_engine = ShepardizeEngine()
    return _shepardize_engine


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def compute_query_hash(query: str) -> str:
    """Compute deterministic SHA-256 hash of a query string."""
    return hashlib.sha256(query.strip().lower().encode("utf-8")).hexdigest()
