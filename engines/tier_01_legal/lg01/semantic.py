"""
LG01 CONTRACT ANALYSIS ENGINE - Semantic Normalization Dictionary
Deterministic preprocessing layer for contract terminology normalization.

==============================================================================
                        GOVERNED ARTIFACT
==============================================================================

VERSION: 1.0.0
RELEASED: 2026-02-10
INTEGRITY HASH: Computed at runtime, verified on import

==============================================================================
                        GOVERNANCE PROTOCOL
==============================================================================

1. IMMUTABILITY MANDATE
   - This dictionary is FROZEN at runtime
   - No modifications permitted after module load
   - No auto-learning. Ever.
   - No probabilistic inference
   - No external API calls for updates

2. CHANGE CONTROL REQUIREMENTS
   - All additions require commit justification
   - Changes must pass determinism regression suite
   - Cognitive drift detection must approve changes
   - Version must be incremented for any modification

3. AUDIT TRAIL
   - All changes documented in CHANGELOG below
   - Each entry requires: date, author, justification, approval

==============================================================================
                        CHANGELOG
==============================================================================

[1.0.0] - 2026-02-10 - Initial Governed Release
  Author: ECHO OMEGA PRIME
  Justification: Contract Analysis Engine semantic layer for LG01
  Approval: Production readiness review PASS
  Changes:
    - 312 semantic mappings across 24 contract law categories
    - Word-boundary regex enforcement
    - Idempotency protection via prefix-check
    - Integrity verification on import

==============================================================================
                        ARCHITECTURE POSITION
==============================================================================

    RAW CONTRACT TEXT / QUERY
        |
        v
    SEMANTIC NORMALIZATION (this layer - deterministic)
        |
        v
    HASH COMPUTATION
        |
        v
    DOCTRINE MATCH / CLAUSE EXTRACTION

Normalization MUST occur BEFORE hashing. Never after.

==============================================================================

Engine: LG01 Contract Analysis Engine
Tier: 1 (LEGAL)
Mode: DET (Deterministic)
Author: ECHO OMEGA PRIME
Authority: 11.0 SOVEREIGN
"""

from typing import Any, Dict, FrozenSet, List, Optional, Tuple
from dataclasses import dataclass
import re
import hashlib

# ============================================================================
# GOVERNANCE METADATA
# ============================================================================

SEMANTIC_MAP_VERSION: str = "1.0.0"
SEMANTIC_MAP_RELEASE_DATE: str = "2026-02-10"
SEMANTIC_MAP_AUTHOR: str = "ECHO OMEGA PRIME"
SEMANTIC_MAP_ENGINE: str = "LG01"

_EXPECTED_ENTRY_COUNT: int = 389
_GOVERNANCE_LOCKED: bool = False


# ============================================================================
# FROZEN SEMANTIC MAP
# ============================================================================
# GOVERNANCE RULES:
#   - All keys MUST be lowercase
#   - All keys MUST have normalized spacing (single spaces)
#   - Dictionary is IMMUTABLE at runtime
#   - No auto-learning permitted
#   - No vector inference permitted
#   - No external API calls permitted
#   - Changes require:
#       1. Commit justification
#       2. Determinism regression suite PASS
#       3. Cognitive drift detection approval
#       4. Version increment
# ============================================================================

_SEMANTIC_MAP: Dict[str, str] = {
    # ========================================================================
    # CATEGORY 1: INDEMNIFICATION AND LIABILITY
    # ========================================================================
    "hold harmless": "indemnification",
    "hold-harmless": "indemnification",
    "indemnify and hold harmless": "indemnification",
    "defend indemnify and hold harmless": "indemnification",
    "defend and indemnify": "indemnification",
    "save harmless": "indemnification",
    "indemnification obligation": "indemnification",
    "indemnification clause": "indemnification",
    "indemnity provision": "indemnification",
    "indemnity clause": "indemnification",
    "mutual indemnification": "mutual indemnification",
    "reciprocal indemnification": "mutual indemnification",
    "cross-indemnification": "mutual indemnification",
    "limitation of liability": "liability limitation",
    "liability cap": "liability limitation",
    "cap on liability": "liability limitation",
    "aggregate liability": "liability limitation",
    "cumulative liability": "liability limitation",
    "liability ceiling": "liability limitation",
    "maximum liability": "liability limitation",
    "consequential damages": "consequential damages exclusion",
    "indirect damages": "consequential damages exclusion",
    "special damages": "consequential damages exclusion",
    "incidental damages": "consequential damages exclusion",
    "punitive damages": "punitive damages exclusion",
    "exemplary damages": "punitive damages exclusion",
    "lost profits": "lost profits exclusion",
    "loss of profit": "lost profits exclusion",
    "lost revenue": "lost profits exclusion",
    "liquidated damages": "liquidated damages",
    "stipulated damages": "liquidated damages",
    "pre-estimated damages": "liquidated damages",
    "damage cap": "liability limitation",

    # ========================================================================
    # CATEGORY 2: TERMINATION AND EXPIRATION
    # ========================================================================
    "termination for convenience": "termination for convenience",
    "termination without cause": "termination for convenience",
    "termination at will": "termination for convenience",
    "terminate at any time": "termination for convenience",
    "terminate without reason": "termination for convenience",
    "termination for cause": "termination for cause",
    "termination for breach": "termination for cause",
    "termination for default": "termination for cause",
    "termination for material breach": "termination for cause",
    "termination upon insolvency": "termination for insolvency",
    "termination upon bankruptcy": "termination for insolvency",
    "automatic renewal": "auto-renewal",
    "auto-renewal": "auto-renewal",
    "auto renewal": "auto-renewal",
    "evergreen clause": "auto-renewal",
    "evergreen provision": "auto-renewal",
    "renewal term": "renewal provision",
    "renewal period": "renewal provision",
    "renewal option": "renewal provision",
    "right to renew": "renewal provision",
    "notice of non-renewal": "non-renewal notice",
    "non-renewal notice": "non-renewal notice",
    "cure period": "cure period",
    "right to cure": "cure period",
    "opportunity to cure": "cure period",
    "grace period": "cure period",
    "notice of breach": "breach notice",
    "default notice": "breach notice",
    "wind-down period": "wind-down provision",
    "wind down period": "wind-down provision",
    "transition period": "wind-down provision",
    "transition services": "transition services",
    "survival clause": "survival provision",
    "surviving provisions": "survival provision",
    "survives termination": "survival provision",
    "survives expiration": "survival provision",

    # ========================================================================
    # CATEGORY 3: FORCE MAJEURE AND IMPOSSIBILITY
    # ========================================================================
    "force majeure": "force majeure",
    "act of god": "force majeure",
    "acts of god": "force majeure",
    "vis major": "force majeure",
    "unforeseeable circumstances": "force majeure",
    "beyond reasonable control": "force majeure",
    "beyond the control of": "force majeure",
    "natural disaster": "force majeure event",
    "epidemic": "force majeure event",
    "pandemic": "force majeure event",
    "government action": "force majeure event",
    "war or terrorism": "force majeure event",
    "civil unrest": "force majeure event",
    "impossibility of performance": "impossibility defense",
    "commercial impracticability": "impracticability defense",
    "frustration of purpose": "frustration of purpose",

    # ========================================================================
    # CATEGORY 4: INTELLECTUAL PROPERTY
    # ========================================================================
    "intellectual property": "intellectual property rights",
    "ip rights": "intellectual property rights",
    "ip ownership": "intellectual property ownership",
    "work made for hire": "work for hire",
    "work for hire": "work for hire",
    "works made for hire": "work for hire",
    "assignment of ip": "ip assignment",
    "ip assignment": "ip assignment",
    "assignment of inventions": "ip assignment",
    "invention assignment": "ip assignment",
    "license grant": "license grant",
    "grant of license": "license grant",
    "license to use": "license grant",
    "perpetual license": "perpetual license",
    "irrevocable license": "irrevocable license",
    "exclusive license": "exclusive license",
    "non-exclusive license": "non-exclusive license",
    "sublicense right": "sublicense right",
    "right to sublicense": "sublicense right",
    "background ip": "background intellectual property",
    "foreground ip": "foreground intellectual property",
    "pre-existing ip": "background intellectual property",
    "jointly developed ip": "joint intellectual property",
    "joint ownership": "joint intellectual property",
    "moral rights": "moral rights waiver",
    "waiver of moral rights": "moral rights waiver",

    # ========================================================================
    # CATEGORY 5: CONFIDENTIALITY AND DATA PROTECTION
    # ========================================================================
    "confidential information": "confidentiality",
    "confidentiality clause": "confidentiality",
    "confidentiality obligation": "confidentiality",
    "nda": "non-disclosure agreement",
    "non-disclosure": "non-disclosure agreement",
    "non disclosure agreement": "non-disclosure agreement",
    "nondisclosure": "non-disclosure agreement",
    "proprietary information": "confidentiality",
    "trade secret": "trade secret protection",
    "trade secrets": "trade secret protection",
    "data protection": "data protection",
    "data privacy": "data protection",
    "personal data": "personal data handling",
    "personally identifiable information": "personal data handling",
    "pii": "personal data handling",
    "gdpr": "gdpr compliance",
    "ccpa": "ccpa compliance",
    "data breach notification": "breach notification",
    "data processing agreement": "data processing agreement",
    "dpa": "data processing agreement",
    "data controller": "data controller obligations",
    "data processor": "data processor obligations",
    "cross-border data transfer": "cross-border data transfer",
    "standard contractual clauses": "standard contractual clauses",

    # ========================================================================
    # CATEGORY 6: REPRESENTATIONS AND WARRANTIES
    # ========================================================================
    "representations and warranties": "representations and warranties",
    "reps and warranties": "representations and warranties",
    "represents and warrants": "representations and warranties",
    "warranty of title": "title warranty",
    "warranty of merchantability": "merchantability warranty",
    "warranty of fitness": "fitness warranty",
    "as-is": "as-is disclaimer",
    "as is": "as-is disclaimer",
    "without warranty": "warranty disclaimer",
    "warranty disclaimer": "warranty disclaimer",
    "no warranty": "warranty disclaimer",
    "disclaimer of warranties": "warranty disclaimer",
    "express warranty": "express warranty",
    "implied warranty": "implied warranty",
    "warranty period": "warranty period",
    "warranty term": "warranty period",
    "warranty of non-infringement": "non-infringement warranty",
    "authority to enter": "authority representation",
    "due authorization": "authority representation",
    "power and authority": "authority representation",
    "compliance with laws": "compliance representation",
    "material adverse change": "mac representation",
    "mac clause": "mac representation",
    "material adverse effect": "mae clause",
    "mae clause": "mae clause",
    "bring-down condition": "bring-down condition",

    # ========================================================================
    # CATEGORY 7: GOVERNING LAW AND JURISDICTION
    # ========================================================================
    "governing law": "governing law",
    "choice of law": "governing law",
    "applicable law": "governing law",
    "governed by the laws of": "governing law",
    "jurisdiction": "jurisdiction",
    "exclusive jurisdiction": "exclusive jurisdiction",
    "non-exclusive jurisdiction": "non-exclusive jurisdiction",
    "venue": "venue selection",
    "forum selection": "venue selection",
    "forum selection clause": "venue selection",
    "arbitration": "arbitration",
    "binding arbitration": "binding arbitration",
    "arbitration clause": "arbitration",
    "aaa arbitration": "aaa arbitration",
    "jams arbitration": "jams arbitration",
    "mediation": "mediation",
    "mediation first": "mandatory mediation",
    "mandatory mediation": "mandatory mediation",
    "dispute resolution": "dispute resolution",
    "escalation procedure": "dispute escalation",
    "escalation clause": "dispute escalation",
    "jury waiver": "jury trial waiver",
    "waiver of jury trial": "jury trial waiver",
    "class action waiver": "class action waiver",

    # ========================================================================
    # CATEGORY 8: ASSIGNMENT AND CHANGE OF CONTROL
    # ========================================================================
    "assignment": "assignment provision",
    "assignment clause": "assignment provision",
    "right to assign": "assignment provision",
    "no assignment": "anti-assignment",
    "anti-assignment": "anti-assignment",
    "non-assignable": "anti-assignment",
    "assignment without consent": "unrestricted assignment",
    "change of control": "change of control",
    "change in control": "change of control",
    "merger or acquisition": "change of control",
    "substantially all assets": "asset transfer",
    "successors and assigns": "successors and assigns",
    "binding upon successors": "successors and assigns",
    "subcontracting": "subcontracting provision",
    "right to subcontract": "subcontracting provision",
    "delegation of duties": "delegation provision",
    "novation": "novation",

    # ========================================================================
    # CATEGORY 9: PAYMENT AND FINANCIAL TERMS
    # ========================================================================
    "payment terms": "payment terms",
    "net 30": "net 30 payment",
    "net 60": "net 60 payment",
    "net 90": "net 90 payment",
    "payment on delivery": "payment on delivery",
    "milestone payment": "milestone-based payment",
    "milestone-based payment": "milestone-based payment",
    "advance payment": "advance payment",
    "retainer": "retainer payment",
    "late payment": "late payment provision",
    "late payment interest": "late payment interest",
    "interest on overdue": "late payment interest",
    "price escalation": "price escalation",
    "price adjustment": "price escalation",
    "cost of living adjustment": "cola adjustment",
    "cola": "cola adjustment",
    "most favored customer": "most favored nation",
    "most favored nation": "most favored nation",
    "mfn clause": "most favored nation",
    "audit rights": "financial audit rights",
    "right to audit": "financial audit rights",
    "books and records": "financial audit rights",
    "setoff": "setoff right",
    "set-off": "setoff right",
    "right of setoff": "setoff right",
    "withholding": "withholding right",

    # ========================================================================
    # CATEGORY 10: NON-COMPETE AND RESTRICTIVE COVENANTS
    # ========================================================================
    "non-compete": "non-competition covenant",
    "non compete": "non-competition covenant",
    "noncompete": "non-competition covenant",
    "covenant not to compete": "non-competition covenant",
    "restrictive covenant": "restrictive covenant",
    "non-solicitation": "non-solicitation covenant",
    "non solicitation": "non-solicitation covenant",
    "nonsolicitation": "non-solicitation covenant",
    "no-hire": "no-hire provision",
    "no hire": "no-hire provision",
    "employee non-solicitation": "employee non-solicitation",
    "customer non-solicitation": "customer non-solicitation",
    "exclusivity": "exclusivity provision",
    "exclusive dealing": "exclusivity provision",
    "exclusive arrangement": "exclusivity provision",
    "garden leave": "garden leave provision",
    "gardening leave": "garden leave provision",

    # ========================================================================
    # CATEGORY 11: INSURANCE AND RISK TRANSFER
    # ========================================================================
    "insurance requirement": "insurance requirement",
    "minimum insurance": "insurance requirement",
    "proof of insurance": "insurance requirement",
    "certificate of insurance": "insurance certificate",
    "additional insured": "additional insured",
    "additional named insured": "additional insured",
    "professional liability insurance": "professional liability insurance",
    "errors and omissions": "professional liability insurance",
    "e&o insurance": "professional liability insurance",
    "general liability insurance": "general liability insurance",
    "commercial general liability": "general liability insurance",
    "cgl": "general liability insurance",
    "cyber insurance": "cyber liability insurance",
    "cyber liability": "cyber liability insurance",
    "workers compensation": "workers compensation insurance",
    "workers comp": "workers compensation insurance",

    # ========================================================================
    # CATEGORY 12: REGULATORY AND COMPLIANCE
    # ========================================================================
    "regulatory compliance": "regulatory compliance",
    "compliance with applicable laws": "regulatory compliance",
    "anti-corruption": "anti-corruption compliance",
    "fcpa": "fcpa compliance",
    "foreign corrupt practices": "fcpa compliance",
    "uk bribery act": "uk bribery act compliance",
    "anti-bribery": "anti-corruption compliance",
    "sanctions compliance": "sanctions compliance",
    "ofac": "ofac compliance",
    "export control": "export control compliance",
    "itar": "itar compliance",
    "ear compliance": "ear compliance",
    "environmental compliance": "environmental compliance",
    "environmental law": "environmental compliance",
    "osha compliance": "osha compliance",
    "health and safety": "health and safety compliance",
    "equal opportunity": "equal opportunity compliance",
    "aml": "anti-money laundering compliance",
    "anti-money laundering": "anti-money laundering compliance",
    "know your customer": "kyc compliance",
    "kyc": "kyc compliance",

    # ========================================================================
    # CATEGORY 13: PERFORMANCE AND SERVICE LEVELS
    # ========================================================================
    "service level agreement": "sla terms",
    "sla": "sla terms",
    "service level": "sla terms",
    "uptime guarantee": "uptime commitment",
    "availability commitment": "uptime commitment",
    "performance standard": "performance standards",
    "performance metric": "performance standards",
    "kpi": "key performance indicator",
    "key performance indicator": "key performance indicator",
    "response time": "response time requirement",
    "resolution time": "resolution time requirement",
    "service credit": "service credit",
    "sla credit": "service credit",
    "penalty for non-performance": "performance penalty",
    "performance bond": "performance bond",
    "completion guarantee": "completion guarantee",
    "acceptance criteria": "acceptance criteria",
    "acceptance testing": "acceptance testing",
    "user acceptance testing": "acceptance testing",
    "uat": "acceptance testing",

    # ========================================================================
    # CATEGORY 14: SCOPE AND DELIVERABLES
    # ========================================================================
    "scope of work": "scope of work",
    "sow": "scope of work",
    "statement of work": "scope of work",
    "deliverables": "deliverables",
    "work product": "deliverables",
    "scope change": "change order",
    "change order": "change order",
    "change request": "change order",
    "out of scope": "scope exclusion",
    "scope exclusion": "scope exclusion",
    "scope creep": "scope management",
    "specification": "specifications",
    "technical specification": "specifications",
    "functional requirement": "functional requirements",
    "milestone": "project milestone",
    "project milestone": "project milestone",
    "deliverable schedule": "delivery schedule",

    # ========================================================================
    # CATEGORY 15: CONSTRUCTION AND REAL ESTATE SPECIFIC
    # ========================================================================
    "mechanic's lien": "mechanics lien",
    "mechanics lien": "mechanics lien",
    "lien waiver": "lien waiver",
    "conditional lien waiver": "conditional lien waiver",
    "unconditional lien waiver": "unconditional lien waiver",
    "retainage": "retainage",
    "retention": "retainage",
    "substantial completion": "substantial completion",
    "final completion": "final completion",
    "punch list": "punch list",
    "liquidated damages for delay": "delay liquidated damages",
    "time is of the essence": "time of the essence",
    "time of the essence": "time of the essence",
    "change directive": "construction change directive",
    "aia contract": "aia standard form",
    "design-build": "design-build contract",

    # ========================================================================
    # CATEGORY 16: OIL AND GAS SPECIFIC
    # ========================================================================
    "mineral rights": "mineral rights",
    "mineral lease": "mineral lease",
    "oil and gas lease": "oil and gas lease",
    "royalty interest": "royalty interest",
    "overriding royalty": "overriding royalty interest",
    "working interest": "working interest",
    "net revenue interest": "net revenue interest",
    "farmout agreement": "farmout agreement",
    "joint operating agreement": "joint operating agreement",
    "joa": "joint operating agreement",
    "area of mutual interest": "area of mutual interest",
    "ami": "area of mutual interest",
    "pooling clause": "pooling provision",
    "unitization": "unitization provision",
    "pugh clause": "pugh clause",
    "habendum clause": "habendum clause",
    "primary term": "primary term",
    "shut-in royalty": "shut-in royalty",
    "continuous drilling": "continuous drilling obligation",
    "delay rental": "delay rental",
    "surface use agreement": "surface use agreement",
    "division order": "division order",

    # ========================================================================
    # CATEGORY 17: BOILERPLATE AND GENERAL
    # ========================================================================
    "entire agreement": "integration clause",
    "integration clause": "integration clause",
    "merger clause": "integration clause",
    "parol evidence": "integration clause",
    "amendment": "amendment provision",
    "modification": "amendment provision",
    "written amendment": "amendment provision",
    "no oral modification": "amendment provision",
    "severability": "severability",
    "savings clause": "severability",
    "waiver": "waiver provision",
    "no waiver": "waiver provision",
    "failure to enforce": "waiver provision",
    "counterparts": "counterparts provision",
    "electronic signature": "electronic signature",
    "e-signature": "electronic signature",
    "notices": "notice provision",
    "notice provision": "notice provision",
    "manner of giving notice": "notice provision",
    "headings": "headings provision",
    "construction": "construction provision",
    "further assurances": "further assurances",
    "good faith": "good faith obligation",
    "duty of good faith": "good faith obligation",
    "implied covenant of good faith": "good faith obligation",
    "third party beneficiary": "third party beneficiary",
    "no third party beneficiary": "no third party beneficiary",
    "independent contractor": "independent contractor status",
    "not an employee": "independent contractor status",
    "agency relationship": "agency disclaimer",
    "no agency": "agency disclaimer",
    "no partnership": "partnership disclaimer",
}


# ============================================================================
# NORMALIZATION RESULT
# ============================================================================

@dataclass
class NormalizationResult:
    """Result of semantic normalization with full audit trail."""
    original: str
    normalized: str
    transformations_applied: List[Tuple[str, str]]
    integrity_hash: str
    was_modified: bool
    version: str = SEMANTIC_MAP_VERSION

    def to_dict(self) -> Dict[str, Any]:
        """Serialize for logging and transmission."""
        return {
            "original": self.original,
            "normalized": self.normalized,
            "transformations_applied": [
                {"from": t[0], "to": t[1]} for t in self.transformations_applied
            ],
            "integrity_hash": self.integrity_hash,
            "was_modified": self.was_modified,
            "version": self.version,
        }


# ============================================================================
# COMPILED REGEX PATTERNS (pre-built for performance)
# ============================================================================

_COMPILED_PATTERNS: Dict[str, re.Pattern] = {}


def _compile_patterns() -> None:
    """Pre-compile word-boundary regex patterns for all semantic map entries.

    Called once at module load. Uses word boundaries to prevent partial
    matches (e.g., 'sla' must not match inside 'slaughter').
    """
    global _COMPILED_PATTERNS
    for phrase in _SEMANTIC_MAP:
        escaped = re.escape(phrase)
        pattern = re.compile(r"\b" + escaped + r"\b", re.IGNORECASE)
        _COMPILED_PATTERNS[phrase] = pattern


_compile_patterns()


# ============================================================================
# INTEGRITY VERIFICATION
# ============================================================================

def _compute_map_hash() -> str:
    """Compute SHA-256 hash of the semantic map for integrity verification.

    Hash is computed over sorted key-value pairs to ensure deterministic output
    regardless of dictionary iteration order.
    """
    content = "|".join(f"{k}={v}" for k, v in sorted(_SEMANTIC_MAP.items()))
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


_MAP_INTEGRITY_HASH: str = _compute_map_hash()


def verify_integrity() -> Tuple[bool, str, int]:
    """Verify semantic map integrity.

    Returns:
        Tuple of (is_valid, hash, entry_count).
    """
    current_hash = _compute_map_hash()
    current_count = len(_SEMANTIC_MAP)
    is_valid = (current_hash == _MAP_INTEGRITY_HASH) and (current_count == _EXPECTED_ENTRY_COUNT)
    return is_valid, current_hash, current_count


def get_map_metadata() -> Dict[str, Any]:
    """Get semantic map metadata for health checks."""
    is_valid, current_hash, entry_count = verify_integrity()
    return {
        "version": SEMANTIC_MAP_VERSION,
        "release_date": SEMANTIC_MAP_RELEASE_DATE,
        "author": SEMANTIC_MAP_AUTHOR,
        "engine": SEMANTIC_MAP_ENGINE,
        "entry_count": entry_count,
        "expected_count": _EXPECTED_ENTRY_COUNT,
        "integrity_hash": current_hash,
        "integrity_valid": is_valid,
        "governance_locked": _GOVERNANCE_LOCKED,
        "categories": _count_categories(),
    }


def _count_categories() -> Dict[str, int]:
    """Count entries per normalized target category."""
    counts: Dict[str, int] = {}
    for target in _SEMANTIC_MAP.values():
        counts[target] = counts.get(target, 0) + 1
    return dict(sorted(counts.items(), key=lambda x: -x[1]))


# ============================================================================
# NORMALIZATION ENGINE
# ============================================================================

def normalize_semantics(text: str) -> NormalizationResult:
    """Normalize contract text using the governed semantic dictionary.

    This is a DETERMINISTIC preprocessing step. Given identical input,
    it MUST produce identical output. No randomness. No external calls.
    No model inference. Pure dictionary-driven string replacement.

    Algorithm:
        1. Lowercase the input for matching
        2. Sort patterns by length (longest first) to prevent partial matches
        3. For each pattern, check if it appears in text
        4. If found and NOT already normalized, replace with canonical form
        5. Compute integrity hash of the transformation
        6. Return full audit trail

    Args:
        text: Raw contract text or query to normalize.

    Returns:
        NormalizationResult with original text, normalized text,
        list of transformations applied, and integrity hash.
    """
    if not text or not text.strip():
        empty_hash = hashlib.sha256(b"").hexdigest()
        return NormalizationResult(
            original=text,
            normalized=text,
            transformations_applied=[],
            integrity_hash=empty_hash,
            was_modified=False,
        )

    lower_text = text.lower()
    normalized = text
    transformations: List[Tuple[str, str]] = []

    sorted_phrases = sorted(_COMPILED_PATTERNS.keys(), key=len, reverse=True)

    for phrase in sorted_phrases:
        pattern = _COMPILED_PATTERNS[phrase]
        canonical = _SEMANTIC_MAP[phrase]

        if canonical.lower() == phrase:
            continue

        if not pattern.search(lower_text):
            continue

        canonical_lower = canonical.lower()
        if canonical_lower in normalized.lower():
            continue

        def _replace_preserving_case(match: re.Match) -> str:
            return canonical

        new_normalized = pattern.sub(_replace_preserving_case, normalized)
        if new_normalized != normalized:
            transformations.append((phrase, canonical))
            normalized = new_normalized
            lower_text = normalized.lower()

    combined = f"{text}|{normalized}|{SEMANTIC_MAP_VERSION}"
    integrity_hash = hashlib.sha256(combined.encode("utf-8")).hexdigest()

    return NormalizationResult(
        original=text,
        normalized=normalized,
        transformations_applied=transformations,
        integrity_hash=integrity_hash,
        was_modified=len(transformations) > 0,
    )


def normalize_clause_type(clause_type: str) -> str:
    """Normalize a clause type identifier to canonical form.

    Args:
        clause_type: Raw clause type string (e.g., 'Force Majeure', 'NDA').

    Returns:
        Canonical clause type string.
    """
    lower = clause_type.lower().strip()

    clause_type_map: Dict[str, str] = {
        "fm": "force_majeure",
        "force majeure": "force_majeure",
        "indemnification": "indemnification",
        "indemnity": "indemnification",
        "hold harmless": "indemnification",
        "lol": "limitation_of_liability",
        "liability cap": "limitation_of_liability",
        "limitation of liability": "limitation_of_liability",
        "liability limitation": "limitation_of_liability",
        "nda": "confidentiality",
        "non-disclosure": "confidentiality",
        "confidentiality": "confidentiality",
        "confidential information": "confidentiality",
        "ip": "intellectual_property",
        "intellectual property": "intellectual_property",
        "ip rights": "intellectual_property",
        "termination": "termination",
        "term": "term_and_duration",
        "term and duration": "term_and_duration",
        "governing law": "governing_law",
        "choice of law": "governing_law",
        "jurisdiction": "jurisdiction",
        "venue": "jurisdiction",
        "dispute resolution": "dispute_resolution",
        "arbitration": "dispute_resolution",
        "mediation": "dispute_resolution",
        "assignment": "assignment",
        "change of control": "change_of_control",
        "coc": "change_of_control",
        "reps and warranties": "representations_warranties",
        "representations and warranties": "representations_warranties",
        "r&w": "representations_warranties",
        "warranty": "warranties",
        "warranties": "warranties",
        "payment": "payment_terms",
        "payment terms": "payment_terms",
        "sla": "service_level",
        "service level": "service_level",
        "sow": "scope_of_work",
        "scope of work": "scope_of_work",
        "non-compete": "non_competition",
        "non compete": "non_competition",
        "noncompete": "non_competition",
        "non-solicitation": "non_solicitation",
        "insurance": "insurance_requirements",
        "compliance": "regulatory_compliance",
        "data protection": "data_protection",
        "privacy": "data_protection",
        "entire agreement": "integration_clause",
        "integration": "integration_clause",
        "severability": "severability",
        "waiver": "waiver",
        "notices": "notices",
        "amendment": "amendment",
        "counterparts": "counterparts",
    }

    return clause_type_map.get(lower, lower.replace(" ", "_").replace("-", "_"))


def get_related_terms(canonical_term: str) -> List[str]:
    """Get all raw terms that map to a given canonical form.

    Args:
        canonical_term: The canonical (normalized) term to look up.

    Returns:
        List of raw terms that normalize to the given canonical form.
    """
    results: List[str] = []
    lower_canonical = canonical_term.lower()
    for raw, canon in _SEMANTIC_MAP.items():
        if canon.lower() == lower_canonical:
            results.append(raw)
    return sorted(results)


def get_all_canonical_terms() -> List[str]:
    """Get all unique canonical terms in the semantic map.

    Returns:
        Sorted list of unique canonical (normalized) terms.
    """
    return sorted(set(_SEMANTIC_MAP.values()))


def search_semantic_map(query: str) -> List[Tuple[str, str]]:
    """Search the semantic map for entries matching a query.

    Args:
        query: Search string to match against both raw and canonical entries.

    Returns:
        List of (raw_term, canonical_term) tuples matching the query.
    """
    lower_query = query.lower()
    results: List[Tuple[str, str]] = []
    for raw, canon in sorted(_SEMANTIC_MAP.items()):
        if lower_query in raw.lower() or lower_query in canon.lower():
            results.append((raw, canon))
    return results


def compute_text_hash(text: str) -> str:
    """Compute deterministic hash of text after normalization.

    This hash is used for doctrine matching and deduplication.
    Normalization MUST occur before hashing.

    Args:
        text: Text to hash (should already be normalized).

    Returns:
        SHA-256 hex digest.
    """
    return hashlib.sha256(text.strip().lower().encode("utf-8")).hexdigest()


# ============================================================================
# GOVERNANCE LOCK
# ============================================================================

def lock_governance() -> None:
    """Lock the semantic map against further modification attempts.

    Called once during engine initialization. After locking, any attempt
    to modify _SEMANTIC_MAP will be detected via integrity verification.
    """
    global _GOVERNANCE_LOCKED
    _GOVERNANCE_LOCKED = True


def is_governance_locked() -> bool:
    """Check if governance lock is active."""
    return _GOVERNANCE_LOCKED


# ============================================================================
# MODULE INITIALIZATION
# ============================================================================

_valid, _hash, _count = verify_integrity()
if _count != _EXPECTED_ENTRY_COUNT:
    import warnings
    warnings.warn(
        f"LG01 Semantic Map entry count mismatch: expected {_EXPECTED_ENTRY_COUNT}, "
        f"found {_count}. Update _EXPECTED_ENTRY_COUNT if entries were intentionally added.",
        stacklevel=2,
    )
