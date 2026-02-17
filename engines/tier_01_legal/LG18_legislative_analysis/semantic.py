"""
LG18 Legislative Analysis Engine - Semantic Normalization Module
==================================================================
Normalizes legislative-specific terminology, maps synonyms, handles
statutory construction terms, congressional procedure vocabulary,
regulatory rulemaking terminology, preemption concepts, and Texas
legislative process terms.

Components:
    - SemanticMap: Core term normalization dictionary
    - normalize_query(): Main entry point for query normalization
    - BillAnalyzer: Bill drafting and analysis class
    - StatutoryConstructionEngine: Canon application and interpretation
    - PreemptionAnalyzer: Express, field, and conflict preemption analysis
    - RegulatoryTracker: APA rulemaking tracking and analysis
    - Citation Patterns: Legislative statute/case citation extraction

Version: 2.0.0
Engine: LG18 Legislative Analysis
"""

from __future__ import annotations

import hashlib
import json
import re
import time
from dataclasses import dataclass, field as dc_field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, ClassVar, Dict, List, Optional, Set, Tuple

from loguru import logger


# ============================================================================
# SEMANTIC MAP - LEGISLATIVE TERMINOLOGY NORMALIZATION
# ============================================================================

SEMANTIC_MAP: Dict[str, Dict[str, Any]] = {
    # ---- STATUTORY CONSTRUCTION ----
    "plain_meaning": {
        "canonical": "plain_meaning_rule",
        "synonyms": ["plain text", "ordinary meaning", "textual meaning", "literal meaning",
                      "clear text", "unambiguous text", "facial meaning"],
        "category": "statutory_construction",
        "weight": 1.0,
    },
    "textualism": {
        "canonical": "textualism",
        "synonyms": ["textual interpretation", "textual analysis", "text-based interpretation",
                      "original public meaning", "semantic meaning"],
        "category": "statutory_construction",
        "weight": 1.0,
    },
    "purposivism": {
        "canonical": "purposivism",
        "synonyms": ["purpose-based interpretation", "purposive interpretation", "legislative purpose",
                      "remedial purpose", "statutory purpose", "intent of congress"],
        "category": "statutory_construction",
        "weight": 0.9,
    },
    "ejusdem_generis": {
        "canonical": "ejusdem_generis",
        "synonyms": ["of the same kind", "same class", "general following specific",
                      "catch-all limitation", "genus restriction"],
        "category": "statutory_construction",
        "weight": 0.9,
    },
    "noscitur_a_sociis": {
        "canonical": "noscitur_a_sociis",
        "synonyms": ["known by associates", "associated words canon", "contextual meaning",
                      "words known by company", "neighbor words"],
        "category": "statutory_construction",
        "weight": 0.9,
    },
    "expressio_unius": {
        "canonical": "expressio_unius",
        "synonyms": ["expression of one excludes other", "negative implication", "inclusion exclusion",
                      "expressed excludes implied", "enumeration implies exclusion"],
        "category": "statutory_construction",
        "weight": 0.9,
    },
    "rule_of_lenity": {
        "canonical": "rule_of_lenity",
        "synonyms": ["lenity", "strict construction criminal", "ambiguity favors defendant",
                      "narrow construction penal", "criminal statute ambiguity"],
        "category": "statutory_construction",
        "weight": 0.9,
    },
    "avoidance_canon": {
        "canonical": "avoidance_canon",
        "synonyms": ["constitutional avoidance", "avoid constitutional questions", "serious doubts canon",
                      "ashwander principles", "constitutional doubt"],
        "category": "statutory_construction",
        "weight": 0.9,
    },
    "surplusage": {
        "canonical": "presumption_against_surplusage",
        "synonyms": ["no surplusage", "every word has meaning", "anti-surplusage",
                      "no redundancy", "no superfluous words"],
        "category": "statutory_construction",
        "weight": 0.8,
    },
    "whole_act": {
        "canonical": "whole_act_rule",
        "synonyms": ["whole act rule", "whole statute rule", "read in context",
                      "harmonize provisions", "statutory structure"],
        "category": "statutory_construction",
        "weight": 0.9,
    },
    "legislative_history": {
        "canonical": "legislative_history",
        "synonyms": ["leg history", "committee reports", "floor debate", "conference report",
                      "committee hearing testimony", "sponsor statements", "drafting history"],
        "category": "statutory_construction",
        "weight": 0.8,
    },
    # ---- CONGRESSIONAL PROCEDURE ----
    "filibuster": {
        "canonical": "filibuster",
        "synonyms": ["senate filibuster", "unlimited debate", "60 vote threshold",
                      "supermajority requirement", "extended debate"],
        "category": "congressional_procedure",
        "weight": 1.0,
    },
    "cloture": {
        "canonical": "cloture",
        "synonyms": ["cloture vote", "invoke cloture", "end debate", "rule xxii",
                      "three-fifths vote", "60 vote cloture"],
        "category": "congressional_procedure",
        "weight": 1.0,
    },
    "reconciliation": {
        "canonical": "budget_reconciliation",
        "synonyms": ["budget reconciliation", "reconciliation bill", "reconciliation process",
                      "simple majority budget", "filibuster-proof budget"],
        "category": "congressional_procedure",
        "weight": 1.0,
    },
    "byrd_rule": {
        "canonical": "byrd_rule",
        "synonyms": ["byrd rule", "extraneous provision", "reconciliation limitation",
                      "section 313", "budget act section 313"],
        "category": "congressional_procedure",
        "weight": 0.9,
    },
    "conference_committee": {
        "canonical": "conference_committee",
        "synonyms": ["conference", "conference report", "reconcile differences",
                      "bicameral negotiation", "joint conference"],
        "category": "congressional_procedure",
        "weight": 0.9,
    },
    "markup": {
        "canonical": "committee_markup",
        "synonyms": ["markup session", "bill markup", "amend in committee",
                      "committee consideration", "section by section"],
        "category": "congressional_procedure",
        "weight": 0.8,
    },
    "unanimous_consent": {
        "canonical": "unanimous_consent",
        "synonyms": ["uc agreement", "unanimous consent agreement", "uca",
                      "consent of the senate", "without objection"],
        "category": "congressional_procedure",
        "weight": 0.8,
    },
    "nuclear_option": {
        "canonical": "nuclear_option",
        "synonyms": ["constitutional option", "reid rule", "change senate rules by majority",
                      "lower cloture threshold"],
        "category": "congressional_procedure",
        "weight": 0.8,
    },
    # ---- REGULATORY RULEMAKING ----
    "notice_and_comment": {
        "canonical": "apa_notice_and_comment",
        "synonyms": ["notice and comment", "informal rulemaking", "section 553",
                      "nprm", "proposed rulemaking", "apa rulemaking"],
        "category": "regulatory_rulemaking",
        "weight": 1.0,
    },
    "chevron_deference": {
        "canonical": "chevron_deference",
        "synonyms": ["chevron", "two step deference", "agency deference",
                      "reasonable interpretation", "permissible construction"],
        "category": "regulatory_rulemaking",
        "weight": 1.0,
    },
    "loper_bright": {
        "canonical": "loper_bright",
        "synonyms": ["loper bright", "overruled chevron", "end of chevron",
                      "independent judgment", "no more chevron deference"],
        "category": "regulatory_rulemaking",
        "weight": 1.0,
    },
    "skidmore": {
        "canonical": "skidmore_deference",
        "synonyms": ["skidmore deference", "skidmore weight", "persuasive deference",
                      "persuasive weight", "agency persuasiveness"],
        "category": "regulatory_rulemaking",
        "weight": 0.9,
    },
    "major_questions": {
        "canonical": "major_questions_doctrine",
        "synonyms": ["major questions doctrine", "mqd", "vast economic significance",
                      "clear congressional authorization", "west virginia v epa doctrine"],
        "category": "regulatory_rulemaking",
        "weight": 1.0,
    },
    "arbitrary_capricious": {
        "canonical": "arbitrary_and_capricious",
        "synonyms": ["arbitrary and capricious", "hard look review", "state farm review",
                      "reasoned decisionmaking", "706 review", "apa review"],
        "category": "regulatory_rulemaking",
        "weight": 0.9,
    },
    "executive_order": {
        "canonical": "executive_order",
        "synonyms": ["EO", "presidential executive order", "presidential directive",
                      "presidential proclamation", "presidential memorandum"],
        "category": "regulatory_rulemaking",
        "weight": 0.8,
    },
    # ---- PREEMPTION ----
    "preemption": {
        "canonical": "preemption",
        "synonyms": ["federal preemption", "preempt state law", "supremacy clause preemption",
                      "state law displaced", "federal override"],
        "category": "preemption",
        "weight": 1.0,
    },
    "express_preemption": {
        "canonical": "preemption_express",
        "synonyms": ["express preemption", "explicit preemption", "preemption clause",
                      "statutory preemption", "preemption provision"],
        "category": "preemption",
        "weight": 1.0,
    },
    "field_preemption": {
        "canonical": "preemption_field",
        "synonyms": ["field preemption", "occupied field", "pervasive regulation",
                      "comprehensive federal scheme", "complete occupation"],
        "category": "preemption",
        "weight": 0.9,
    },
    "conflict_preemption": {
        "canonical": "preemption_conflict",
        "synonyms": ["conflict preemption", "impossibility preemption", "obstacle preemption",
                      "direct conflict", "cannot comply with both"],
        "category": "preemption",
        "weight": 0.9,
    },
    # ---- LEGISLATIVE PROCESS ----
    "bill": {
        "canonical": "bill",
        "synonyms": ["legislation", "proposed law", "measure", "act",
                      "house bill", "senate bill", "HR", "S."],
        "category": "legislative_process",
        "weight": 1.0,
    },
    "veto": {
        "canonical": "veto",
        "synonyms": ["presidential veto", "veto message", "return without approval",
                      "pocket veto", "veto override"],
        "category": "legislative_process",
        "weight": 1.0,
    },
    "signing_statement": {
        "canonical": "signing_statement",
        "synonyms": ["presidential signing statement", "statement on signing",
                      "signing interpretation", "executive interpretation at signing"],
        "category": "legislative_process",
        "weight": 0.7,
    },
    "enrolled_bill": {
        "canonical": "enrolled_bill_doctrine",
        "synonyms": ["enrolled bill", "enrolled bill doctrine", "conclusive evidence of passage",
                      "authenticated bill", "engrossed bill"],
        "category": "legislative_process",
        "weight": 0.8,
    },
    # ---- DELEGATION ----
    "nondelegation": {
        "canonical": "delegation_doctrine",
        "synonyms": ["nondelegation doctrine", "nondelegation", "intelligible principle",
                      "delegation of legislative power", "excessive delegation"],
        "category": "delegation",
        "weight": 1.0,
    },
    # ---- LOBBYING ----
    "lobbying": {
        "canonical": "lobbying_disclosure_act",
        "synonyms": ["lobbying disclosure", "LDA", "lobbyist registration",
                      "lobbying regulation", "government affairs"],
        "category": "lobbying_regulation",
        "weight": 0.9,
    },
    "fara": {
        "canonical": "foreign_agents_registration",
        "synonyms": ["FARA", "foreign agents registration act", "foreign agent",
                      "foreign principal", "foreign lobbying"],
        "category": "lobbying_regulation",
        "weight": 0.9,
    },
    # ---- REDISTRICTING ----
    "redistricting": {
        "canonical": "redistricting_legal_framework",
        "synonyms": ["redistricting", "reapportionment", "gerrymandering",
                      "drawing districts", "district lines", "one person one vote"],
        "category": "redistricting",
        "weight": 1.0,
    },
    "gerrymandering": {
        "canonical": "gerrymandering",
        "synonyms": ["partisan gerrymandering", "racial gerrymandering",
                      "packing and cracking", "malapportionment", "vote dilution"],
        "category": "redistricting",
        "weight": 0.9,
    },
    # ---- CONSTITUTIONAL AMENDMENT ----
    "constitutional_amendment": {
        "canonical": "constitutional_amendment_process",
        "synonyms": ["article v", "amendment process", "ratification",
                      "propose amendment", "amend constitution", "convention of states"],
        "category": "constitutional_process",
        "weight": 1.0,
    },
    # ---- TEXAS LEGISLATURE ----
    "texas_legislature": {
        "canonical": "texas_legislative_process",
        "synonyms": ["texas legislature", "texas house", "texas senate",
                      "biennial session", "140 day session", "texas leg"],
        "category": "state_legislative_process",
        "weight": 0.9,
    },
    "sunset_review": {
        "canonical": "sunset_review",
        "synonyms": ["sunset advisory commission", "sunset commission", "agency sunset",
                      "12 year review", "continuation or abolition"],
        "category": "state_legislative_process",
        "weight": 0.8,
    },
    # ---- CONGRESSIONAL OVERSIGHT ----
    "congressional_oversight": {
        "canonical": "congressional_oversight",
        "synonyms": ["oversight hearing", "congressional investigation", "subpoena power",
                      "government accountability", "inspector general", "GAO"],
        "category": "congressional_oversight",
        "weight": 0.9,
    },
    "cra": {
        "canonical": "congressional_review_act",
        "synonyms": ["CRA", "congressional review act", "disapproval resolution",
                      "rule disapproval", "joint resolution of disapproval"],
        "category": "congressional_oversight",
        "weight": 0.9,
    },
    # ---- APPROPRIATIONS ----
    "appropriations": {
        "canonical": "appropriations",
        "synonyms": ["appropriations bill", "spending bill", "funding bill",
                      "continuing resolution", "CR", "omnibus"],
        "category": "budget_process",
        "weight": 0.9,
    },
    "debt_ceiling": {
        "canonical": "debt_ceiling",
        "synonyms": ["debt limit", "debt ceiling", "statutory debt limit",
                      "borrowing authority", "31 usc 3101"],
        "category": "budget_process",
        "weight": 0.8,
    },
    # ---- SPEECH OR DEBATE ----
    "speech_debate": {
        "canonical": "legislative_privilege_speech_debate",
        "synonyms": ["speech or debate clause", "legislative immunity", "congressional immunity",
                      "article i section 6", "legislative privilege"],
        "category": "legislative_privilege",
        "weight": 0.9,
    },
    # ---- BALLOT INITIATIVES ----
    "ballot_initiative": {
        "canonical": "ballot_initiative",
        "synonyms": ["initiative", "ballot measure", "proposition", "referendum",
                      "direct democracy", "citizen initiative"],
        "category": "direct_democracy",
        "weight": 0.8,
    },
}

# ============================================================================
# JURISDICTION MAP
# ============================================================================

JURISDICTION_MAP: Dict[str, Dict[str, Any]] = {
    "federal": {
        "label": "Federal",
        "constitution": "U.S. Constitution",
        "legislature": "U.S. Congress",
        "statutory_code": "United States Code (USC)",
        "regulatory_code": "Code of Federal Regulations (CFR)",
        "highest_court": "U.S. Supreme Court",
    },
    "texas": {
        "label": "Texas",
        "constitution": "Texas Constitution",
        "legislature": "Texas Legislature",
        "statutory_code": "Texas Statutes (Vernon's)",
        "regulatory_code": "Texas Administrative Code (TAC)",
        "highest_court": "Texas Supreme Court (civil) / Texas Court of Criminal Appeals (criminal)",
    },
}


# ============================================================================
# CITATION PATTERNS
# ============================================================================

CITATION_PATTERNS: Dict[str, re.Pattern[str]] = {
    "usc": re.compile(r"\b(\d+)\s*U\.?S\.?C\.?\s*(?:\xA7|[Ss](?:ec(?:tion)?\.?)?)?\s*(\d+[\w-]*)", re.IGNORECASE),
    "cfr": re.compile(r"\b(\d+)\s*C\.?F\.?R\.?\s*(?:\xA7|[Ss](?:ec(?:tion)?\.?)?)?\s*([\d.]+)", re.IGNORECASE),
    "us_reports": re.compile(r"\b(\d+)\s*U\.?S\.?\s+(\d+)", re.IGNORECASE),
    "supreme_ct": re.compile(r"\b(\d+)\s*S\.?\s*Ct\.?\s+(\d+)", re.IGNORECASE),
    "federal_reporter": re.compile(r"\b(\d+)\s*F\.?\s*(?:2d|3d|4th)?\s+(\d+)", re.IGNORECASE),
    "texas_statute": re.compile(r"Tex\.?\s*(\w+(?:\.\s*&\s*\w+)?)\s*Code\s*(?:\xA7|[Ss]ec\.?)?\s*([\d.]+)", re.IGNORECASE),
    "public_law": re.compile(r"(?:Pub\.?\s*L\.?|P\.?L\.?)\s*(?:No\.?)?\s*(\d+)-(\d+)", re.IGNORECASE),
    "executive_order": re.compile(r"(?:E\.?O\.?|Executive\s*Order)\s*(?:No\.?)?\s*(\d+)", re.IGNORECASE),
    "house_bill": re.compile(r"H\.?R\.?\s*(\d+)", re.IGNORECASE),
    "senate_bill": re.compile(r"S\.?\s*(\d+)(?!\s*(?:Ct|U\.S))", re.IGNORECASE),
}


# ============================================================================
# NORMALIZATION RESULT
# ============================================================================

@dataclass
class NormalizationResult:
    """Result of normalizing a query through the semantic dictionary."""
    original_query: str
    normalized_query: str
    matched_terms: List[Dict[str, Any]]
    detected_categories: List[str]
    detected_citations: List[Dict[str, str]]
    detected_jurisdiction: Optional[str]
    normalization_time_ms: float
    semantic_map_version: str
    confidence: float

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "original_query": self.original_query,
            "normalized_query": self.normalized_query,
            "matched_terms": self.matched_terms,
            "detected_categories": self.detected_categories,
            "detected_citations": self.detected_citations,
            "detected_jurisdiction": self.detected_jurisdiction,
            "normalization_time_ms": round(self.normalization_time_ms, 3),
            "semantic_map_version": self.semantic_map_version,
            "confidence": round(self.confidence, 4),
        }


# ============================================================================
# SEMANTIC MAP METADATA
# ============================================================================

_SEMANTIC_MAP_VERSION: str = "2.0.0"
_SEMANTIC_MAP_HASH: Optional[str] = None


def _compute_semantic_map_hash() -> str:
    """Compute SHA-256 hash of the semantic map."""
    global _SEMANTIC_MAP_HASH
    if _SEMANTIC_MAP_HASH is None:
        content = json.dumps(SEMANTIC_MAP, sort_keys=True)
        _SEMANTIC_MAP_HASH = hashlib.sha256(content.encode("utf-8")).hexdigest()
    return _SEMANTIC_MAP_HASH


def get_semantic_map() -> Dict[str, Dict[str, Any]]:
    """Return the semantic map dictionary."""
    return SEMANTIC_MAP


def get_semantic_map_version() -> str:
    """Return the semantic map version string."""
    return _SEMANTIC_MAP_VERSION


def get_semantic_map_hash() -> str:
    """Return the SHA-256 hash of the semantic map."""
    return _compute_semantic_map_hash()


def get_jurisdiction_map() -> Dict[str, Dict[str, Any]]:
    """Return the jurisdiction map."""
    return JURISDICTION_MAP


def verify_dictionary_integrity() -> Dict[str, Any]:
    """Verify the integrity of the semantic dictionary."""
    issues: List[str] = []
    seen_canonicals: Set[str] = set()
    all_synonyms: List[str] = []
    for key, entry in SEMANTIC_MAP.items():
        if "canonical" not in entry:
            issues.append(f"Missing canonical for key: {key}")
        if "synonyms" not in entry:
            issues.append(f"Missing synonyms for key: {key}")
        if "category" not in entry:
            issues.append(f"Missing category for key: {key}")
        canonical = entry.get("canonical", "")
        if canonical in seen_canonicals:
            issues.append(f"Duplicate canonical: {canonical}")
        seen_canonicals.add(canonical)
        all_synonyms.extend(entry.get("synonyms", []))
    dup_synonyms = [s for s in all_synonyms if all_synonyms.count(s) > 1]
    if dup_synonyms:
        issues.append(f"Duplicate synonyms found: {set(dup_synonyms)}")
    return {
        "valid": len(issues) == 0,
        "total_entries": len(SEMANTIC_MAP),
        "total_synonyms": len(all_synonyms),
        "total_categories": len(set(e.get("category", "") for e in SEMANTIC_MAP.values())),
        "issues": issues,
        "hash": get_semantic_map_hash(),
        "version": _SEMANTIC_MAP_VERSION,
    }


# ============================================================================
# QUERY NORMALIZATION
# ============================================================================

def normalize_query(query: str) -> NormalizationResult:
    """Normalize a legislative query through the semantic dictionary.

    Matches query tokens against the semantic map, detects categories,
    extracts citations, and identifies jurisdiction.
    """
    start = time.perf_counter()
    query_lower = query.lower().strip()
    matched_terms: List[Dict[str, Any]] = []
    detected_categories: Set[str] = set()
    normalized_tokens: List[str] = query_lower.split()

    for key, entry in SEMANTIC_MAP.items():
        canonical = entry.get("canonical", key)
        synonyms = entry.get("synonyms", [])
        category = entry.get("category", "")
        weight = entry.get("weight", 1.0)
        all_terms = [key] + synonyms
        for term in all_terms:
            if term.lower() in query_lower:
                matched_terms.append({
                    "input_term": term,
                    "canonical": canonical,
                    "category": category,
                    "weight": weight,
                })
                detected_categories.add(category)
                break

    detected_citations: List[Dict[str, str]] = []
    for pattern_name, pattern in CITATION_PATTERNS.items():
        for match in pattern.finditer(query):
            detected_citations.append({
                "type": pattern_name,
                "match": match.group(0),
                "groups": str(match.groups()),
            })

    detected_jurisdiction: Optional[str] = None
    if "texas" in query_lower or "tex." in query_lower or "tx " in query_lower:
        detected_jurisdiction = "texas"
    elif "federal" in query_lower or "congress" in query_lower or "u.s.c." in query_lower:
        detected_jurisdiction = "federal"

    if matched_terms:
        for mt in matched_terms:
            canonical = mt["canonical"]
            for i, token in enumerate(normalized_tokens):
                if token in mt.get("input_term", "").lower().split():
                    normalized_tokens[i] = canonical
                    break

    normalized_query = " ".join(normalized_tokens)
    confidence = min(1.0, 0.5 + 0.1 * len(matched_terms) + 0.05 * len(detected_citations))

    elapsed_ms = (time.perf_counter() - start) * 1000
    logger.debug(
        "Normalized query in {:.1f}ms: {} matched terms, {} citations",
        elapsed_ms,
        len(matched_terms),
        len(detected_citations),
    )

    return NormalizationResult(
        original_query=query,
        normalized_query=normalized_query,
        matched_terms=matched_terms,
        detected_categories=sorted(detected_categories),
        detected_citations=detected_citations,
        detected_jurisdiction=detected_jurisdiction,
        normalization_time_ms=elapsed_ms,
        semantic_map_version=_SEMANTIC_MAP_VERSION,
        confidence=confidence,
    )


# ============================================================================
# BILL ANALYZER
# ============================================================================

class BillAnalyzer:
    """Analyzes bill drafting and structure."""

    REQUIRED_SECTIONS: ClassVar[List[str]] = [
        "short_title",
        "findings_and_purpose",
        "definitions",
        "substantive_provisions",
        "enforcement",
        "effective_date",
        "severability",
    ]

    DRAFTING_ISSUES: ClassVar[Dict[str, str]] = {
        "vague_delegation": "Provision delegates broad authority without intelligible principle; may face nondelegation challenge",
        "preemption_ambiguity": "Preemption clause is unclear; may generate costly litigation over scope",
        "sunset_missing": "No sunset provision; consider adding for periodic reassessment",
        "funding_mechanism_absent": "Authorizes programs but does not appropriate funds; requires separate appropriation",
        "definitional_gap": "Key terms used but not defined; may cause interpretive disputes",
        "retroactivity_risk": "Provisions may be construed as retroactive without clear statement; Due Process concerns",
        "severability_absent": "No severability clause; invalidation of one provision may affect entire statute",
        "enforcement_gap": "Creates obligations without enforcement mechanism or penalty provisions",
    }

    def analyze_bill_structure(self, bill_text: str) -> Dict[str, Any]:
        """Analyze a bill's structural completeness and drafting quality."""
        text_lower = bill_text.lower()
        found_sections: List[str] = []
        missing_sections: List[str] = []
        for section in self.REQUIRED_SECTIONS:
            readable = section.replace("_", " ")
            if readable in text_lower or section in text_lower:
                found_sections.append(section)
            else:
                missing_sections.append(section)

        drafting_issues: List[Dict[str, str]] = []
        for issue_key, issue_desc in self.DRAFTING_ISSUES.items():
            readable = issue_key.replace("_", " ")
            if readable in text_lower:
                drafting_issues.append({"issue": issue_key, "description": issue_desc})

        if "shall" in text_lower and "as the secretary determines" in text_lower:
            drafting_issues.append({
                "issue": "vague_delegation",
                "description": self.DRAFTING_ISSUES["vague_delegation"],
            })
        if "preempt" in text_lower and "saving" not in text_lower:
            drafting_issues.append({
                "issue": "preemption_ambiguity",
                "description": "Preemption clause present without savings clause; may preempt state law more broadly than intended",
            })

        completeness = len(found_sections) / max(len(self.REQUIRED_SECTIONS), 1)

        return {
            "found_sections": found_sections,
            "missing_sections": missing_sections,
            "completeness_score": round(completeness, 4),
            "drafting_issues": drafting_issues,
            "word_count": len(bill_text.split()),
            "analyzed_at": datetime.now(timezone.utc).isoformat(),
        }

    def identify_committees(self, subject_areas: List[str]) -> List[Dict[str, Any]]:
        """Identify likely committee referrals based on subject areas."""
        committee_map: Dict[str, List[str]] = {
            "tax": ["House Ways and Means", "Senate Finance"],
            "appropriation": ["House Appropriations", "Senate Appropriations"],
            "defense": ["House Armed Services", "Senate Armed Services"],
            "judiciary": ["House Judiciary", "Senate Judiciary"],
            "energy": ["House Energy and Commerce", "Senate Energy and Natural Resources"],
            "environment": ["House Natural Resources", "Senate Environment and Public Works"],
            "banking": ["House Financial Services", "Senate Banking"],
            "agriculture": ["House Agriculture", "Senate Agriculture"],
            "education": ["House Education and the Workforce", "Senate HELP"],
            "foreign_affairs": ["House Foreign Affairs", "Senate Foreign Relations"],
            "homeland_security": ["House Homeland Security", "Senate Homeland Security"],
            "transportation": ["House Transportation and Infrastructure", "Senate Commerce, Science, and Transportation"],
            "veterans": ["House Veterans' Affairs", "Senate Veterans' Affairs"],
            "small_business": ["House Small Business", "Senate Small Business"],
        }

        referrals: List[Dict[str, Any]] = []
        for area in subject_areas:
            area_lower = area.lower()
            for key, committees in committee_map.items():
                if key in area_lower:
                    referrals.append({
                        "subject_area": area,
                        "likely_committees": committees,
                        "primary": committees[0] if committees else "Unknown",
                    })
                    break
        return referrals


# ============================================================================
# STATUTORY CONSTRUCTION ENGINE
# ============================================================================

class StatutoryConstructionEngine:
    """Engine for applying canons of statutory construction."""

    CANON_PRIORITY: ClassVar[List[str]] = [
        "plain_meaning_rule",
        "whole_act_rule",
        "presumption_against_surplusage",
        "noscitur_a_sociis",
        "ejusdem_generis",
        "expressio_unius",
        "avoidance_canon",
        "rule_of_lenity",
        "purposivism",
    ]

    CANON_DESCRIPTIONS: ClassVar[Dict[str, str]] = {
        "plain_meaning_rule": "Apply the statute according to its plain text when unambiguous",
        "whole_act_rule": "Read each provision in the context of the entire statute",
        "presumption_against_surplusage": "Presume every word in the statute has independent meaning",
        "noscitur_a_sociis": "Interpret ambiguous words by reference to their statutory neighbors",
        "ejusdem_generis": "Limit general terms following specific lists to the same class",
        "expressio_unius": "The expression of one thing implies the exclusion of others",
        "avoidance_canon": "Choose the interpretation that avoids serious constitutional questions",
        "rule_of_lenity": "Resolve ambiguity in criminal statutes in favor of the defendant",
        "purposivism": "Interpret in light of the statute's remedial purpose",
    }

    def identify_applicable_canons(self, query: str) -> List[Dict[str, Any]]:
        """Identify which canons of construction are applicable to a query."""
        query_lower = query.lower()
        applicable: List[Dict[str, Any]] = []

        for canon in self.CANON_PRIORITY:
            relevance = 0.0
            canon_readable = canon.replace("_", " ")
            if canon_readable in query_lower:
                relevance = 1.0
            elif any(kw in query_lower for kw in canon_readable.split()):
                relevance = 0.5

            if "ambiguous" in query_lower or "unclear" in query_lower:
                if canon in ("noscitur_a_sociis", "ejusdem_generis", "whole_act_rule"):
                    relevance = max(relevance, 0.7)
            if "criminal" in query_lower or "penalty" in query_lower:
                if canon == "rule_of_lenity":
                    relevance = max(relevance, 0.8)
            if "constitutional" in query_lower or "unconstitutional" in query_lower:
                if canon == "avoidance_canon":
                    relevance = max(relevance, 0.8)
            if "list" in query_lower or "enumerat" in query_lower:
                if canon in ("ejusdem_generis", "expressio_unius"):
                    relevance = max(relevance, 0.7)
            if "purpose" in query_lower or "intent" in query_lower:
                if canon == "purposivism":
                    relevance = max(relevance, 0.7)
            if "plain" in query_lower or "text" in query_lower or "literal" in query_lower:
                if canon == "plain_meaning_rule":
                    relevance = max(relevance, 0.8)

            if relevance > 0.0:
                applicable.append({
                    "canon": canon,
                    "description": self.CANON_DESCRIPTIONS.get(canon, ""),
                    "relevance": round(relevance, 4),
                    "priority_rank": self.CANON_PRIORITY.index(canon) + 1,
                })

        if not applicable:
            applicable.append({
                "canon": "plain_meaning_rule",
                "description": self.CANON_DESCRIPTIONS["plain_meaning_rule"],
                "relevance": 0.5,
                "priority_rank": 1,
            })

        applicable.sort(key=lambda x: (-x["relevance"], x["priority_rank"]))
        return applicable

    def apply_canon(self, canon: str, statutory_text: str, context: str) -> Dict[str, Any]:
        """Apply a specific canon to a statutory text with context."""
        analysis_steps: List[str] = []

        if canon == "plain_meaning_rule":
            analysis_steps = [
                "Step 1: Examine the statutory text as written",
                "Step 2: Determine the ordinary public meaning of the key terms",
                "Step 3: If the text is clear and unambiguous, apply it as written",
                "Step 4: Check for absurdity (narrow exception to plain meaning)",
                "Step 5: If ambiguous, proceed to other canons and contextual analysis",
            ]
        elif canon == "ejusdem_generis":
            analysis_steps = [
                "Step 1: Identify the list of specific items",
                "Step 2: Identify the general catch-all term",
                "Step 3: Determine the common characteristic (genus) of the specific items",
                "Step 4: Limit the general term to items sharing that common characteristic",
                "Step 5: Verify the specific items actually share a discernible genus",
            ]
        elif canon == "noscitur_a_sociis":
            analysis_steps = [
                "Step 1: Identify the ambiguous word in its statutory context",
                "Step 2: Examine the surrounding words in the grouping",
                "Step 3: Determine the common quality shared by the neighboring terms",
                "Step 4: Interpret the ambiguous word to share that quality",
                "Step 5: Verify consistency with the statute's overall scheme",
            ]
        elif canon == "expressio_unius":
            analysis_steps = [
                "Step 1: Identify the items explicitly mentioned in the statute",
                "Step 2: Determine whether the list appears exhaustive or illustrative",
                "Step 3: If exhaustive, infer the intentional exclusion of omitted items",
                "Step 4: Check for contrary indicators (e.g., 'including but not limited to')",
                "Step 5: Consider whether the omission was deliberate or inadvertent",
            ]
        elif canon == "avoidance_canon":
            analysis_steps = [
                "Step 1: Identify the competing interpretations of the statute",
                "Step 2: Determine whether one interpretation raises serious constitutional questions",
                "Step 3: Assess whether the alternative interpretation is 'fairly possible' from the text",
                "Step 4: If so, adopt the constitutionally permissible interpretation",
                "Step 5: Identify the specific constitutional provision at issue",
            ]
        elif canon == "rule_of_lenity":
            analysis_steps = [
                "Step 1: Confirm the statute is criminal or quasi-criminal",
                "Step 2: Apply all other tools of statutory construction",
                "Step 3: Determine whether genuine ('grievous') ambiguity remains",
                "Step 4: If so, resolve the ambiguity in favor of the defendant",
                "Step 5: Adopt the narrower reading of the criminal prohibition",
            ]
        elif canon == "whole_act_rule":
            analysis_steps = [
                "Step 1: Map all uses of the key term throughout the statute",
                "Step 2: Check the definitions section for defined terms",
                "Step 3: Compare parallel provisions for consistent usage",
                "Step 4: Ensure no provision is rendered superfluous",
                "Step 5: Harmonize the provision with the statute's overall structure",
            ]
        elif canon == "purposivism":
            analysis_steps = [
                "Step 1: Identify the mischief or evil Congress intended to address",
                "Step 2: Examine legislative history (committee reports, floor statements)",
                "Step 3: Determine the remedy Congress chose",
                "Step 4: Interpret the ambiguous provision in light of the remedial purpose",
                "Step 5: Consider whether the reading serves the statute's overarching goal",
            ]
        else:
            analysis_steps = [
                "Step 1: Identify the applicable canon",
                "Step 2: Apply the canon to the statutory text",
                "Step 3: Assess the result against the statutory structure",
                "Step 4: Consider counter-arguments under competing canons",
                "Step 5: Reach a conclusion with appropriate confidence level",
            ]

        return {
            "canon": canon,
            "description": self.CANON_DESCRIPTIONS.get(canon, ""),
            "statutory_text_excerpt": statutory_text[:500],
            "context_excerpt": context[:500],
            "analysis_steps": analysis_steps,
            "applied_at": datetime.now(timezone.utc).isoformat(),
        }


# ============================================================================
# PREEMPTION ANALYZER
# ============================================================================

class PreemptionAnalyzer:
    """Analyzes preemption issues across express, field, and conflict types."""

    PREEMPTION_FACTORS: ClassVar[Dict[str, List[str]]] = {
        "express": [
            "Does the federal statute contain an explicit preemption clause?",
            "What is the scope of the preemption clause as written?",
            "Is there a savings clause preserving any state authority?",
            "Does the presumption against preemption apply?",
            "How have courts interpreted this preemption clause?",
        ],
        "field": [
            "Is the federal regulatory scheme pervasive and comprehensive?",
            "Has Congress manifested an intent to occupy the field?",
            "Is the federal interest dominant in this area?",
            "Does the subject matter require national uniformity?",
            "Is this an area of traditional state regulation?",
        ],
        "conflict": [
            "Is compliance with both federal and state law physically impossible?",
            "Does the state law stand as an obstacle to federal objectives?",
            "Does federal law establish a floor or a ceiling?",
            "What are the specific purposes of the federal statute?",
            "Can the regulated entity comply with both laws simultaneously?",
        ],
    }

    def analyze_preemption(
        self, federal_statute: str, state_law: str, preemption_type: str
    ) -> Dict[str, Any]:
        """Analyze a preemption issue."""
        p_type = preemption_type.lower()
        if p_type not in self.PREEMPTION_FACTORS:
            p_type = "express"

        factors = self.PREEMPTION_FACTORS[p_type]

        analysis: Dict[str, Any] = {
            "preemption_type": p_type,
            "federal_statute": federal_statute,
            "state_law": state_law,
            "analysis_factors": factors,
            "presumption_against_preemption": True,
            "traditional_state_regulation": "Assess whether the area is one of traditional state regulation",
            "framework": f"Apply {p_type} preemption analysis under the Supremacy Clause (Art. VI, Cl. 2)",
            "key_cases": self._get_key_cases(p_type),
            "analyzed_at": datetime.now(timezone.utc).isoformat(),
        }
        return analysis

    def _get_key_cases(self, preemption_type: str) -> List[str]:
        """Return key cases for the specified preemption type."""
        cases_map: Dict[str, List[str]] = {
            "express": [
                "Cipollone v. Liggett Group, 505 U.S. 504 (1992)",
                "Medtronic v. Lohr, 518 U.S. 470 (1996)",
                "Riegel v. Medtronic, 552 U.S. 312 (2008)",
            ],
            "field": [
                "Arizona v. United States, 567 U.S. 387 (2012)",
                "Pacific Gas & Electric Co. v. State Energy Resources, 461 U.S. 190 (1983)",
                "Gade v. National Solid Wastes, 505 U.S. 88 (1992)",
            ],
            "conflict": [
                "Wyeth v. Levine, 555 U.S. 555 (2009)",
                "Geier v. American Honda, 529 U.S. 861 (2000)",
                "PLIVA v. Mensing, 564 U.S. 604 (2011)",
            ],
        }
        return cases_map.get(preemption_type, [])


# ============================================================================
# REGULATORY TRACKER
# ============================================================================

class RegulatoryTracker:
    """Tracks and analyzes regulatory rulemaking activities."""

    RULEMAKING_STAGES: ClassVar[List[str]] = [
        "advance_notice_of_proposed_rulemaking",
        "notice_of_proposed_rulemaking",
        "public_comment_period",
        "comment_analysis",
        "final_rule",
        "effective_date",
        "congressional_review_period",
    ]

    DEFERENCE_DOCTRINES: ClassVar[Dict[str, Dict[str, Any]]] = {
        "chevron": {
            "status": "OVERRULED by Loper Bright (2024)",
            "standard": "No longer applicable; courts exercise independent judgment",
            "cite": "Chevron U.S.A. v. NRDC, 467 U.S. 837 (1984) (OVERRULED)",
        },
        "skidmore": {
            "status": "ACTIVE",
            "standard": "Agency interpretation given persuasive weight based on thoroughness, consistency, and expertise",
            "cite": "Skidmore v. Swift & Co., 323 U.S. 134 (1944)",
        },
        "auer": {
            "status": "NARROWED",
            "standard": "Deference to agency interpretation of its own regulation, but only when regulation is genuinely ambiguous and other conditions are met",
            "cite": "Kisor v. Wilkie, 588 U.S. 558 (2019)",
        },
        "major_questions": {
            "status": "ACTIVE",
            "standard": "Agencies must have clear congressional authorization for actions of vast economic and political significance",
            "cite": "West Virginia v. EPA, 597 U.S. 697 (2022)",
        },
    }

    def assess_deference(self, doctrine: str) -> Dict[str, Any]:
        """Assess the current status of a deference doctrine."""
        doc_lower = doctrine.lower()
        for key, info in self.DEFERENCE_DOCTRINES.items():
            if key in doc_lower:
                return {
                    "doctrine": key,
                    "status": info["status"],
                    "standard": info["standard"],
                    "citation": info["cite"],
                    "post_loper_bright_note": "After Loper Bright (2024), courts exercise independent judgment on statutory interpretation. Chevron deference is no longer available.",
                    "assessed_at": datetime.now(timezone.utc).isoformat(),
                }
        return {
            "doctrine": doctrine,
            "status": "UNKNOWN",
            "standard": "Doctrine not found in tracker",
            "citation": "",
            "post_loper_bright_note": "All deference analysis must account for Loper Bright Enterprises v. Ramos (2024).",
            "assessed_at": datetime.now(timezone.utc).isoformat(),
        }

    def analyze_rulemaking_compliance(self, rule_info: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze whether a rulemaking complies with APA requirements."""
        issues: List[str] = []
        nprm_published = rule_info.get("nprm_published", False)
        comment_period_days = rule_info.get("comment_period_days", 0)
        comments_addressed = rule_info.get("comments_addressed", False)
        logical_outgrowth = rule_info.get("logical_outgrowth", True)
        basis_and_purpose = rule_info.get("basis_and_purpose", False)
        good_cause_claimed = rule_info.get("good_cause_claimed", False)

        if not nprm_published and not good_cause_claimed:
            issues.append("NPRM not published and no good cause exception claimed (5 USC 553(b))")
        if comment_period_days < 30 and not good_cause_claimed:
            issues.append(f"Comment period of {comment_period_days} days may be inadequate; E.O. 12866 recommends 60 days")
        if not comments_addressed:
            issues.append("Agency did not address significant comments; may be arbitrary and capricious (Motor Vehicle Mfrs. v. State Farm)")
        if not logical_outgrowth:
            issues.append("Final rule may not be a logical outgrowth of the NPRM; may require reproposal")
        if not basis_and_purpose:
            issues.append("Missing concise general statement of basis and purpose (5 USC 553(c))")

        compliance_score = 1.0 - (len(issues) * 0.2)
        compliance_score = max(0.0, min(1.0, compliance_score))

        return {
            "rule_info": rule_info,
            "compliance_score": round(compliance_score, 4),
            "issues": issues,
            "apa_requirements_met": len(issues) == 0,
            "vulnerable_to_challenge": len(issues) > 0,
            "recommended_actions": [f"Address: {issue}" for issue in issues],
            "analyzed_at": datetime.now(timezone.utc).isoformat(),
        }
