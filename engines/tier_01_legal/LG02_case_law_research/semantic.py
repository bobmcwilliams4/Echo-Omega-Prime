"""
LG02 CASE LAW RESEARCH ENGINE - SEMANTIC NORMALIZATION DICTIONARY
=================================================================

GOVERNANCE PROTOCOL
-------------------
Authority: 11.0 SOVEREIGN | Commander: Bobby Don McWilliams II
Engine: LG02 - Case Law Research & Legal Precedent Analysis
Version: 2.0.0 | Release Date: 2026-02-10
Classification: CANONICAL | Status: PRODUCTION
Port: 8392

ARCHITECTURE POSITION
---------------------
    RAW QUERY
        |
        v
    SEMANTIC NORMALIZATION (this layer - deterministic)
        |
        v
    CITATION PARSING (extract structured citations)
        |
        v
    HASH COMPUTATION
        |
        v
    DOCTRINE MATCH / SEARCH

Normalization MUST occur BEFORE hashing. Never after.
Citation normalization is a sub-stage of semantic normalization.

IMMUTABILITY MANDATE
--------------------
1. This dictionary is FROZEN at runtime
2. No modifications permitted after module load
3. No auto-learning. Ever.
4. No probabilistic inference
5. No external API calls for updates
6. Changes require version increment + governance approval

CHANGELOG
---------
v2.0.0 | 2026-02-10 | Full rebuild with 200+ legal normalization entries
                       Covers courts, reporters, procedures, evidence,
                       constitutional law, litigation, corporate law, IP,
                       criminal law, remedies, citation formats

Author: ECHO OMEGA PRIME
"""

import hashlib
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, FrozenSet, List, Optional, Tuple

from loguru import logger


# ============================================================================
# GOVERNANCE METADATA
# ============================================================================

SEMANTIC_MAP_VERSION: str = "2.0.0"
SEMANTIC_MAP_RELEASE_DATE: str = "2026-02-10"
SEMANTIC_MAP_AUTHOR: str = "ECHO OMEGA PRIME - LG02 Engine"

_EXPECTED_ENTRY_COUNT: int = 209
_GOVERNANCE_LOCKED: bool = False


# ============================================================================
# FROZEN SEMANTIC MAP - 210+ LEGAL TERM ENTRIES
# ============================================================================
# SORT ORDER: Applied by phrase length descending to prevent partial-token
# replacement bugs (e.g., "comp" rewriting inside "compensation")
# ============================================================================

SEMANTIC_MAP: Dict[str, str] = {
    # =========================================================================
    # COURT NAME ABBREVIATIONS (25 entries)
    # =========================================================================
    "scotus": "supreme court of the united states",
    "supreme ct": "supreme court",
    "sup ct": "supreme court",
    "s ct": "supreme court",
    "united states supreme court": "supreme court of the united states",
    "us supreme court": "supreme court of the united states",
    "circuit ct": "circuit court",
    "cir ct": "circuit court",
    "ct of appeals": "court of appeals",
    "ct app": "court of appeals",
    "appellate ct": "appellate court",
    "appeals ct": "court of appeals",
    "dist ct": "district court",
    "district ct": "district court",
    "d ct": "district court",
    "bankruptcy ct": "bankruptcy court",
    "bankr ct": "bankruptcy court",
    "tax ct": "tax court",
    "fed cl": "court of federal claims",
    "ct fed cl": "court of federal claims",
    "ct intl trade": "court of international trade",
    "cafc": "court of appeals for the federal circuit",
    "bta": "board of tax appeals",
    "nlrb": "national labor relations board",
    "ftc": "federal trade commission",

    # =========================================================================
    # REPORTER ABBREVIATIONS (30 entries)
    # =========================================================================
    "f.3d": "F.3d",
    "f.2d": "F.2d",
    "f.4th": "F.4th",
    "f. supp.": "F. Supp.",
    "f. supp. 2d": "F. Supp. 2d",
    "f. supp. 3d": "F. Supp. 3d",
    "f supp 3d": "F. Supp. 3d",
    "f supp 2d": "F. Supp. 2d",
    "f supp": "F. Supp.",
    "f3d": "F.3d",
    "f2d": "F.2d",
    "f4th": "F.4th",
    "f app'x": "F. App'x",
    "f appx": "F. App'x",
    "s. ct.": "S. Ct.",
    "s ct": "S. Ct.",
    "l. ed.": "L. Ed.",
    "l. ed. 2d": "L. Ed. 2d",
    "l ed 2d": "L. Ed. 2d",
    "u.s.": "U.S.",
    "b.r.": "B.R.",
    "t.c.": "T.C.",
    "t.c.m.": "T.C.M.",
    "t c memo": "T.C. Memo.",
    "a.2d": "A.2d",
    "a.3d": "A.3d",
    "n.e.2d": "N.E.2d",
    "n.e.3d": "N.E.3d",
    "n.w.2d": "N.W.2d",
    "p.3d": "P.3d",

    # =========================================================================
    # PROCEDURAL TERMS (30 entries)
    # =========================================================================
    "msj": "motion for summary judgment",
    "summary judgment": "motion for summary judgment",
    "sum judg": "motion for summary judgment",
    "summ j": "motion for summary judgment",
    "mtd": "motion to dismiss",
    "motion to dismiss for failure to state a claim": "12(b)(6) motion to dismiss",
    "12b6": "12(b)(6) motion to dismiss",
    "12 b 6": "12(b)(6) motion to dismiss",
    "mtn to compel": "motion to compel",
    "mot compel": "motion to compel",
    "mot in limine": "motion in limine",
    "mil": "motion in limine",
    "mtn limine": "motion in limine",
    "preliminary injunction": "motion for preliminary injunction",
    "pi": "motion for preliminary injunction",
    "tro": "temporary restraining order",
    "temp restraining order": "temporary restraining order",
    "class cert": "class certification",
    "class action cert": "class certification",
    "cert denied": "certiorari denied",
    "cert granted": "certiorari granted",
    "cert petition": "petition for certiorari",
    "pet for cert": "petition for certiorari",
    "writ of cert": "writ of certiorari",
    "interlocutory appeal": "interlocutory appeal under 28 USC 1292",
    "mandamus": "writ of mandamus",
    "habeas corpus": "petition for writ of habeas corpus",
    "habeas": "petition for writ of habeas corpus",
    "default j": "default judgment",
    "j on the pleadings": "judgment on the pleadings",

    # =========================================================================
    # EVIDENCE TERMS (20 entries)
    # =========================================================================
    "fre": "federal rules of evidence",
    "fed r evid": "federal rules of evidence",
    "hearsay exception": "hearsay exception under FRE 803/804",
    "hearsay rule": "hearsay rule under FRE 802",
    "business records exception": "business records exception under FRE 803(6)",
    "excited utterance": "excited utterance under FRE 803(2)",
    "present sense impression": "present sense impression under FRE 803(1)",
    "daubert": "daubert standard for expert testimony",
    "daubert standard": "daubert standard for expert testimony",
    "frye standard": "frye general acceptance test",
    "frye test": "frye general acceptance test",
    "best evidence rule": "best evidence rule under FRE 1002",
    "original document rule": "best evidence rule under FRE 1002",
    "attorney client priv": "attorney-client privilege",
    "atty client privilege": "attorney-client privilege",
    "work product doctrine": "work product doctrine under FRCP 26(b)(3)",
    "work product": "work product doctrine under FRCP 26(b)(3)",
    "spoliation": "spoliation of evidence",
    "chain of custody": "chain of custody for physical evidence",
    "expert witness": "expert witness testimony under FRE 702",

    # =========================================================================
    # CONSTITUTIONAL LAW (20 entries)
    # =========================================================================
    "1st amendment": "first amendment",
    "1a": "first amendment",
    "free speech": "first amendment free speech",
    "freedom of speech": "first amendment free speech",
    "establishment clause": "first amendment establishment clause",
    "free exercise clause": "first amendment free exercise clause",
    "2nd amendment": "second amendment",
    "2a": "second amendment",
    "right to bear arms": "second amendment right to bear arms",
    "4th amendment": "fourth amendment",
    "4a": "fourth amendment",
    "search and seizure": "fourth amendment search and seizure",
    "unreasonable search": "fourth amendment unreasonable search",
    "5th amendment": "fifth amendment",
    "5a": "fifth amendment",
    "due process": "fifth amendment due process",
    "taking clause": "fifth amendment takings clause",
    "14th amendment": "fourteenth amendment",
    "equal protection": "fourteenth amendment equal protection",
    "substantive due process": "fourteenth amendment substantive due process",

    # =========================================================================
    # LITIGATION TERMS (25 entries)
    # =========================================================================
    "standing": "article iii standing",
    "standing requirement": "article iii standing",
    "case or controversy": "article iii case or controversy requirement",
    "mootness": "mootness doctrine",
    "ripeness": "ripeness doctrine",
    "political question": "political question doctrine",
    "stare decisis": "stare decisis",
    "res judicata": "res judicata (claim preclusion)",
    "claim preclusion": "res judicata (claim preclusion)",
    "collateral estoppel": "collateral estoppel (issue preclusion)",
    "issue preclusion": "collateral estoppel (issue preclusion)",
    "statute of limitations": "statute of limitations",
    "sol": "statute of limitations",
    "statute of repose": "statute of repose",
    "discovery rule": "discovery rule for statute of limitations",
    "laches": "doctrine of laches",
    "unclean hands": "doctrine of unclean hands",
    "judicial estoppel": "judicial estoppel",
    "equitable estoppel": "equitable estoppel",
    "promissory estoppel": "promissory estoppel",
    "accord and satisfaction": "accord and satisfaction",
    "forum non conveniens": "forum non conveniens",
    "forum selection": "forum selection clause",
    "choice of law": "choice of law analysis",
    "erie doctrine": "erie doctrine (federal courts applying state law)",

    # =========================================================================
    # CORPORATE AND BUSINESS LAW (20 entries)
    # =========================================================================
    "business judgment rule": "business judgment rule",
    "bjr": "business judgment rule",
    "piercing the corporate veil": "veil piercing",
    "pierce the veil": "veil piercing",
    "alter ego": "alter ego doctrine for veil piercing",
    "fiduciary duty": "fiduciary duty",
    "duty of care": "fiduciary duty of care",
    "duty of loyalty": "fiduciary duty of loyalty",
    "duty of good faith": "fiduciary duty of good faith",
    "entire fairness": "entire fairness standard of review",
    "enhanced scrutiny": "enhanced scrutiny (revlon/unocal)",
    "revlon duties": "revlon enhanced scrutiny for sale of company",
    "unocal": "unocal enhanced scrutiny for defensive measures",
    "demand futility": "demand futility under derivative action",
    "derivative action": "shareholder derivative action",
    "direct vs derivative": "direct versus derivative claim distinction",
    "appraisal rights": "statutory appraisal rights",
    "controlling shareholder": "controlling shareholder fiduciary duties",
    "mjd doctrine": "majority of the minority approval",
    "books and records": "books and records inspection under DGCL 220",

    # =========================================================================
    # INTELLECTUAL PROPERTY (15 entries)
    # =========================================================================
    "fair use": "copyright fair use under 17 USC 107",
    "fair use defense": "copyright fair use under 17 USC 107",
    "transformative use": "transformative fair use analysis",
    "dmca": "digital millennium copyright act",
    "dmca takedown": "dmca takedown notice under 17 USC 512",
    "trade secret": "trade secret misappropriation",
    "trade dress": "trade dress protection under lanham act",
    "trademark dilution": "trademark dilution under 15 USC 1125(c)",
    "likelihood of confusion": "trademark likelihood of confusion test",
    "patent infringement": "patent infringement under 35 USC 271",
    "claim construction": "patent claim construction (markman)",
    "markman hearing": "patent claim construction hearing",
    "obviousness": "patent obviousness under 35 USC 103",
    "alice test": "alice/mayo patent eligibility test under 35 USC 101",
    "patent eligible": "patent eligibility under 35 USC 101",

    # =========================================================================
    # CRIMINAL LAW (15 entries)
    # =========================================================================
    "miranda": "miranda warning requirements",
    "miranda rights": "miranda warning requirements",
    "miranda warning": "miranda warning requirements",
    "probable cause": "probable cause for arrest or search warrant",
    "reasonable suspicion": "reasonable suspicion for terry stop",
    "terry stop": "terry stop under terry v ohio",
    "exclusionary rule": "exclusionary rule for illegally obtained evidence",
    "fruit of the poisonous tree": "fruit of the poisonous tree doctrine",
    "inevitable discovery": "inevitable discovery exception",
    "good faith exception": "good faith exception to exclusionary rule",
    "qualified immunity": "qualified immunity for government officials",
    "qi": "qualified immunity for government officials",
    "brady material": "brady disclosure obligations",
    "brady violation": "brady disclosure obligations",
    "ineffective assistance": "ineffective assistance of counsel under strickland",

    # =========================================================================
    # ADMINISTRATIVE / REGULATORY (10 entries)
    # =========================================================================
    "chevron deference": "chevron deference to agency interpretation",
    "chevron": "chevron deference to agency interpretation",
    "auer deference": "auer deference to agency regulation interpretation",
    "skidmore deference": "skidmore persuasive deference",
    "arbitrary and capricious": "arbitrary and capricious standard under apa",
    "apa review": "judicial review under administrative procedure act",
    "major questions doctrine": "major questions doctrine",
    "nondelegation": "nondelegation doctrine",
    "exhaustion of admin remedies": "exhaustion of administrative remedies",
    "ripeness admin": "administrative ripeness doctrine",
}


# ============================================================================
# CITATION FORMAT PATTERNS
# ============================================================================

# Bluebook citation regex patterns for parsing
CITATION_PATTERNS: Dict[str, str] = {
    # Volume Reporter Page (Court Year) — standard case citation
    "standard_case": r"(\d+)\s+([A-Za-z][A-Za-z\.\s\']+\d*[a-z]*)\s+(\d+)\s*(?:\(([^)]+)\))?\s*(?:\((\d{4})\))?",
    # Pinpoint citation: 123 F.3d 456, 460
    "pinpoint": r"(\d+)\s+([A-Za-z][A-Za-z\.\s\']+\d*[a-z]*)\s+(\d+),\s*(\d+)",
    # Party v. Party style: Smith v. Jones, 123 F.3d 456 (5th Cir. 1999)
    "party_style": r"([A-Z][a-zA-Z\.\s]+)\s+v\.\s+([A-Z][a-zA-Z\.\s]+),\s*(\d+)\s+([A-Za-z][A-Za-z\.\s\']+\d*[a-z]*)\s+(\d+)\s*\(([^)]+)\)",
    # Statute citation: 26 U.S.C. Section 162
    "usc_statute": r"(\d+)\s+U\.?S\.?C\.?\s*(?:\xA7|[Ss]ec(?:tion)?\.?)\s*(\d+[a-zA-Z]*(?:\([a-zA-Z0-9]+\))*)",
    # CFR citation: 26 C.F.R. Section 1.162-1
    "cfr_regulation": r"(\d+)\s+C\.?F\.?R\.?\s*(?:\xA7|[Ss]ec(?:tion)?\.?)\s*([\d]+(?:\.[\d\w\-]+)*)",
    # IRC section: IRC Section 162(a)
    "irc_section": r"I\.?R\.?C\.?\s*(?:\xA7|[Ss]ec(?:tion)?\.?)\s*(\d+[a-zA-Z]*(?:\([a-zA-Z0-9]+\))*)",
    # Restatement citation
    "restatement": r"Restatement\s+\((?:Second|Third|Fourth)\)\s+of\s+([A-Za-z\s]+)\s*(?:\xA7|[Ss]ec\.?)\s*(\d+)",
    # Federal Rules of Civil Procedure
    "frcp": r"Fed\.\s*R\.\s*Civ\.\s*P\.\s*(\d+)(?:\(([a-zA-Z0-9]+)\))?",
    # Federal Rules of Evidence
    "fre": r"Fed\.\s*R\.\s*Evid\.\s*(\d+)(?:\(([a-zA-Z0-9]+)\))?",
    # Federal Rules of Appellate Procedure
    "frap": r"Fed\.\s*R\.\s*App\.\s*P\.\s*(\d+)",
    # Federal Rules of Criminal Procedure
    "frcrp": r"Fed\.\s*R\.\s*Crim\.\s*P\.\s*(\d+)",
}


# ============================================================================
# COMPILED PATTERNS (precompiled for performance)
# ============================================================================

_COMPILED_CITATION_PATTERNS: Dict[str, re.Pattern] = {
    name: re.compile(pattern, re.IGNORECASE)
    for name, pattern in CITATION_PATTERNS.items()
}


# ============================================================================
# COURT IDENTIFIER PATTERNS
# ============================================================================

COURT_ABBREVIATIONS: Dict[str, str] = {
    "1st cir": "First Circuit",
    "2d cir": "Second Circuit",
    "2nd cir": "Second Circuit",
    "3d cir": "Third Circuit",
    "3rd cir": "Third Circuit",
    "4th cir": "Fourth Circuit",
    "5th cir": "Fifth Circuit",
    "6th cir": "Sixth Circuit",
    "7th cir": "Seventh Circuit",
    "8th cir": "Eighth Circuit",
    "9th cir": "Ninth Circuit",
    "10th cir": "Tenth Circuit",
    "11th cir": "Eleventh Circuit",
    "d.c. cir": "D.C. Circuit",
    "dc cir": "D.C. Circuit",
    "fed. cir": "Federal Circuit",
    "fed cir": "Federal Circuit",
    "d. del": "District of Delaware",
    "s.d.n.y": "Southern District of New York",
    "sdny": "Southern District of New York",
    "e.d.n.y": "Eastern District of New York",
    "edny": "Eastern District of New York",
    "n.d. cal": "Northern District of California",
    "c.d. cal": "Central District of California",
    "s.d. cal": "Southern District of California",
    "e.d. tex": "Eastern District of Texas",
    "w.d. tex": "Western District of Texas",
    "n.d. tex": "Northern District of Texas",
    "s.d. tex": "Southern District of Texas",
    "d. mass": "District of Massachusetts",
    "e.d. pa": "Eastern District of Pennsylvania",
    "n.d. ill": "Northern District of Illinois",
    "d.d.c": "District of Columbia",
    "d. md": "District of Maryland",
    "w.d. wash": "Western District of Washington",
    "d.n.j": "District of New Jersey",
    "m.d. fla": "Middle District of Florida",
    "s.d. fla": "Southern District of Florida",
    "n.d. ga": "Northern District of Georgia",
    "w.d. va": "Western District of Virginia",
}


# ============================================================================
# NORMALIZATION RESULT
# ============================================================================

@dataclass
class NormalizationResult:
    """Result of semantic normalization including metadata."""
    original: str
    normalized: str
    substitutions: List[Tuple[str, str]]
    citations_found: List[str]
    courts_identified: List[str]
    hash_before: str
    hash_after: str
    was_modified: bool
    normalization_version: str = SEMANTIC_MAP_VERSION

    def to_dict(self) -> Dict:
        """Serialize to dictionary."""
        return {
            "original": self.original,
            "normalized": self.normalized,
            "substitutions": self.substitutions,
            "citations_found": self.citations_found,
            "courts_identified": self.courts_identified,
            "hash_before": self.hash_before,
            "hash_after": self.hash_after,
            "was_modified": self.was_modified,
            "normalization_version": self.normalization_version,
        }


# ============================================================================
# SORTING — Longest match first to prevent partial replacement
# ============================================================================

_SORTED_ENTRIES: List[Tuple[str, str]] = sorted(
    SEMANTIC_MAP.items(),
    key=lambda item: len(item[0]),
    reverse=True,
)

# Pre-compile word-boundary patterns for each entry
_COMPILED_REPLACEMENTS: List[Tuple[re.Pattern, str]] = [
    (re.compile(r"\b" + re.escape(key) + r"\b", re.IGNORECASE), value)
    for key, value in _SORTED_ENTRIES
]


# ============================================================================
# INTEGRITY VERIFICATION
# ============================================================================

def _compute_map_hash() -> str:
    """Compute SHA-256 integrity hash of the semantic map."""
    serialized = "|".join(f"{k}={v}" for k, v in sorted(SEMANTIC_MAP.items()))
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


_MAP_INTEGRITY_HASH: str = _compute_map_hash()


def verify_dictionary_integrity() -> Dict[str, Any]:
    """Verify the semantic map has not been tampered with at runtime."""
    current_hash = _compute_map_hash()
    entry_count = len(SEMANTIC_MAP)
    matches = current_hash == _MAP_INTEGRITY_HASH
    count_ok = entry_count >= _EXPECTED_ENTRY_COUNT

    return {
        "integrity_hash": current_hash,
        "stored_hash": _MAP_INTEGRITY_HASH,
        "hashes_match": matches,
        "entry_count": entry_count,
        "expected_minimum": _EXPECTED_ENTRY_COUNT,
        "count_valid": count_ok,
        "overall_integrity": matches and count_ok,
        "version": SEMANTIC_MAP_VERSION,
        "release_date": SEMANTIC_MAP_RELEASE_DATE,
    }


# ============================================================================
# CORE NORMALIZATION FUNCTION
# ============================================================================

def normalize_query(text: str) -> NormalizationResult:
    """
    Normalize a legal query using the frozen semantic map.

    Process:
        1. Lowercase the input
        2. Collapse whitespace
        3. Compute pre-normalization hash
        4. Apply semantic substitutions (longest-match-first)
        5. Extract embedded citations
        6. Identify courts mentioned
        7. Compute post-normalization hash

    Args:
        text: Raw legal query text

    Returns:
        NormalizationResult with full metadata
    """
    if not text or not text.strip():
        empty_hash = hashlib.sha256(b"").hexdigest()
        return NormalizationResult(
            original=text,
            normalized="",
            substitutions=[],
            citations_found=[],
            courts_identified=[],
            hash_before=empty_hash,
            hash_after=empty_hash,
            was_modified=False,
        )

    original = text.strip()
    working = original.lower()

    # Collapse multiple whitespace to single space
    working = re.sub(r"\s+", " ", working).strip()

    # Compute hash before normalization
    hash_before = hashlib.sha256(working.encode("utf-8")).hexdigest()

    # Apply semantic substitutions
    substitutions: List[Tuple[str, str]] = []
    for pattern, replacement in _COMPILED_REPLACEMENTS:
        match = pattern.search(working)
        if match:
            found = match.group(0)
            # Idempotency check: don't replace if already normalized
            if found.lower() != replacement.lower():
                working = pattern.sub(replacement, working)
                substitutions.append((found, replacement))

    # Extract citations found in the query
    citations_found: List[str] = []
    for pattern_name, compiled in _COMPILED_CITATION_PATTERNS.items():
        for match in compiled.finditer(original):
            citations_found.append(match.group(0).strip())

    # Identify courts mentioned
    courts_identified: List[str] = []
    lower_working = working.lower()
    for abbrev, full_name in COURT_ABBREVIATIONS.items():
        if abbrev.lower() in lower_working:
            if full_name not in courts_identified:
                courts_identified.append(full_name)

    # Also check for circuit numbers
    circuit_pattern = re.compile(r"(\d+)(?:st|nd|rd|th)\s+cir", re.IGNORECASE)
    for match in circuit_pattern.finditer(working):
        circuit_num = match.group(1)
        circuit_names = {
            "1": "First Circuit", "2": "Second Circuit", "3": "Third Circuit",
            "4": "Fourth Circuit", "5": "Fifth Circuit", "6": "Sixth Circuit",
            "7": "Seventh Circuit", "8": "Eighth Circuit", "9": "Ninth Circuit",
            "10": "Tenth Circuit", "11": "Eleventh Circuit",
        }
        name = circuit_names.get(circuit_num, f"{circuit_num}th Circuit")
        if name not in courts_identified:
            courts_identified.append(name)

    # Compute hash after normalization
    hash_after = hashlib.sha256(working.encode("utf-8")).hexdigest()

    return NormalizationResult(
        original=original,
        normalized=working,
        substitutions=substitutions,
        citations_found=citations_found,
        courts_identified=courts_identified,
        hash_before=hash_before,
        hash_after=hash_after,
        was_modified=hash_before != hash_after,
    )


# ============================================================================
# ACCESSOR FUNCTIONS
# ============================================================================

def get_semantic_map() -> Dict[str, str]:
    """Get a read-only copy of the semantic map."""
    return dict(SEMANTIC_MAP)


def get_governance_metadata() -> Dict[str, str]:
    """Get governance metadata for the semantic map."""
    return {
        "version": SEMANTIC_MAP_VERSION,
        "release_date": SEMANTIC_MAP_RELEASE_DATE,
        "author": SEMANTIC_MAP_AUTHOR,
        "entry_count": str(len(SEMANTIC_MAP)),
        "integrity_hash": _MAP_INTEGRITY_HASH,
        "governance_locked": str(_GOVERNANCE_LOCKED),
    }


def get_semantic_map_version() -> str:
    """Get the version of the semantic map."""
    return SEMANTIC_MAP_VERSION


def get_semantic_map_hash() -> str:
    """Get the integrity hash of the semantic map."""
    return _MAP_INTEGRITY_HASH


def get_citation_patterns() -> Dict[str, str]:
    """Get the raw citation patterns dictionary."""
    return dict(CITATION_PATTERNS)


def get_court_abbreviations() -> Dict[str, str]:
    """Get the court abbreviations dictionary."""
    return dict(COURT_ABBREVIATIONS)
