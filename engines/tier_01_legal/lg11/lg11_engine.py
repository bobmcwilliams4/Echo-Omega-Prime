"""
LG11 — Immigration Law Intelligence Engine
Professional-grade immigration law doctrine system for attorneys, accredited representatives,
and DOJ-recognized organizations.

Architecture:
    Layer 1: Doctrine Cache (0-200ms) — Pre-compiled expert reasoning from INA, BIA, CFR
    Layer 2: Semantic Retrieval (200-700ms) — TF-IDF vector search on cache miss
    Layer 3: Deep Analysis (on-demand) — Multi-doctrine synthesis, fragility, risk assessment

Response Modes:
    FAST: Doctrine-driven, minimal citations, sub-2 seconds
    STANDARD: Doctrine + retrieval, moderate citations, thorough analysis
    DEEP: Full multi-doctrine analysis with counter-arguments
    DEFENSE: Court-defensible, maximum citation density, fragility scoring

Analysis Zones:
    PETITION: Prospective — visa category selection, eligibility pathways, strategy
    COMPLIANCE: Regulatory — status maintenance, employment authorization, conditions
    DEFENSE: Removal defense — what will survive immigration court proceedings
    NATURALIZATION: Citizenship pathway — eligibility, bars, good moral character

Author: ECHO OMEGA PRIME
Engine: LG11 Immigration Law
Authority: 5.0 (Tier 1 LEGAL)
Port: 8500
Version: 1.0.0
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
import time
import uuid
from collections import Counter, defaultdict
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, ClassVar, Dict, List, Literal, Optional, Tuple

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import BaseModel, Field

from lg11_telemetry import (
    ErrorDomain,
    MutationOrigin,
    MutationType,
    ResponseLayer,
    TelemetryCollector,
    complete_trace,
    get_telemetry,
    log_error,
    record_doctrine_mutation,
    trace_query,
)

# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================

ENGINE_DIR = Path(__file__).parent
LOG_DIR = ENGINE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logger.add(
    LOG_DIR / "lg11_engine_{time}.log",
    rotation="10 MB",
    retention="7 days",
    level="DEBUG",
    compression="gz",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level:<8} | {message}",
)
logger.add(
    LOG_DIR / "lg11_audit.log",
    rotation="10 MB",
    retention="30 days",
    level="INFO",
    compression="gz",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | AUDIT | {message}",
    filter=lambda record: "AUDIT" in record["message"],
)

AUDIT_LOG = LOG_DIR / "audit_trail.jsonl"
ENGINE_VERSION = "1.0.0"
ENGINE_ID = "LG11"
ENGINE_PORT = 8500
_START_TIME = time.time()


# =============================================================================
# ENUMS AND CONSTANTS
# =============================================================================

class ResponseMode(str, Enum):
    FAST = "fast"
    STANDARD = "standard"
    DEEP = "deep"
    DEFENSE = "defense"


class AnalysisZone(str, Enum):
    """Immigration law analysis zones — each conclusion pinned to exactly one zone."""
    PETITION = "petition"
    COMPLIANCE = "compliance"
    DEFENSE = "defense"
    NATURALIZATION = "naturalization"


class AuthorityLevel(str, Enum):
    """Hierarchical authority weighting for immigration law sources."""
    INA = "ina"
    CFR = "cfr"
    COURT_CASE = "court_case"
    AGENCY_GUIDANCE = "agency_guidance"
    COMMENTARY = "commentary"

    @property
    def weight(self) -> int:
        weights = {
            "ina": 100,
            "cfr": 80,
            "court_case": 60,
            "agency_guidance": 40,
            "commentary": 20,
        }
        return weights.get(self.value, 10)


class ConfidenceBand(str, Enum):
    """Confidence stratification for immigration conclusions."""
    DEFENSIBLE = "defensible"
    SUPPORTABLE = "supportable"
    DISCLOSURE = "disclosure_recommended"
    HIGH_RISK = "high_risk"


class RiskLevel(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class IssueCategory(str, Enum):
    """Issue categories for pre-doctrine decomposition."""
    VISA_CLASSIFICATION = "visa_classification"
    ADMISSIBILITY = "admissibility"
    DEPORTABILITY = "deportability"
    RELIEF_FROM_REMOVAL = "relief_from_removal"
    CITIZENSHIP = "citizenship"
    EMPLOYMENT_AUTHORIZATION = "employment_authorization"
    FAMILY_UNITY = "family_unity"
    HUMANITARIAN_PROTECTION = "humanitarian_protection"
    CRIMINAL_CONSEQUENCES = "criminal_consequences"
    UNLAWFUL_PRESENCE = "unlawful_presence"
    CONSULAR_PROCESSING = "consular_processing"
    ADJUSTMENT_OF_STATUS = "adjustment_of_status"


class DoctrineStratum(str, Enum):
    """Doctrine classification in multi-doctrine analysis."""
    PRIMARY = "primary"
    SECONDARY = "secondary"
    TERTIARY = "tertiary"


# =============================================================================
# SEMANTIC NORMALIZATION — 100+ immigration law domain synonyms
# =============================================================================

IMMIGRATION_SYNONYMS: Dict[str, str] = {
    "green card": "lawful permanent residence",
    "gc": "lawful permanent residence",
    "lpr": "lawful permanent resident",
    "permanent resident": "lawful permanent resident",
    "permanent residency": "lawful permanent residence",
    "deportation": "removal",
    "deport": "remove",
    "deported": "removed",
    "illegal alien": "undocumented noncitizen",
    "illegal immigrant": "undocumented noncitizen",
    "alien": "noncitizen",
    "usc": "united states citizen",
    "us citizen": "united states citizen",
    "american citizen": "united states citizen",
    "citizen": "united states citizen",
    "naturalized citizen": "naturalized united states citizen",
    "ina": "immigration and nationality act",
    "immigration act": "immigration and nationality act",
    "cimt": "crime involving moral turpitude",
    "moral turpitude": "crime involving moral turpitude",
    "af": "aggravated felony",
    "aggravated felony conviction": "aggravated felony",
    "aos": "adjustment of status",
    "adjust status": "adjustment of status",
    "green card application": "adjustment of status",
    "nta": "notice to appear",
    "removal proceedings": "removal proceedings",
    "immigration court": "immigration court proceedings",
    "eoir": "executive office for immigration review",
    "bia": "board of immigration appeals",
    "immigration appeal": "board of immigration appeals",
    "aao": "administrative appeals office",
    "uscis": "united states citizenship and immigration services",
    "cis": "united states citizenship and immigration services",
    "ice": "immigration and customs enforcement",
    "cbp": "customs and border protection",
    "dhs": "department of homeland security",
    "dos": "department of state",
    "dol": "department of labor",
    "h1b": "h-1b specialty occupation",
    "h-1b": "h-1b specialty occupation",
    "h1-b": "h-1b specialty occupation",
    "h1b visa": "h-1b specialty occupation",
    "h-1b visa": "h-1b specialty occupation",
    "l1": "l-1 intracompany transferee",
    "l-1": "l-1 intracompany transferee",
    "l1a": "l-1a manager executive",
    "l1b": "l-1b specialized knowledge",
    "o1": "o-1 extraordinary ability",
    "o-1": "o-1 extraordinary ability",
    "eb1": "eb-1 priority worker",
    "eb-1": "eb-1 priority worker",
    "eb1a": "eb-1a extraordinary ability",
    "eb-1a": "eb-1a extraordinary ability",
    "eb2": "eb-2 advanced degree",
    "eb-2": "eb-2 advanced degree",
    "niw": "national interest waiver",
    "eb3": "eb-3 skilled worker",
    "eb-3": "eb-3 skilled worker",
    "eb5": "eb-5 immigrant investor",
    "eb-5": "eb-5 immigrant investor",
    "perm": "labor certification perm",
    "labor cert": "labor certification perm",
    "labor certification": "labor certification perm",
    "tps": "temporary protected status",
    "daca": "deferred action for childhood arrivals",
    "dreamer": "deferred action for childhood arrivals",
    "dreamers": "deferred action for childhood arrivals",
    "asylum seeker": "asylum applicant",
    "asylee": "asylum grantee",
    "refugee": "refugee admission",
    "withholding": "withholding of removal",
    "cat": "convention against torture",
    "torture convention": "convention against torture",
    "vawa": "violence against women act self-petition",
    "u visa": "u nonimmigrant status crime victim",
    "u-visa": "u nonimmigrant status crime victim",
    "t visa": "t nonimmigrant status trafficking victim",
    "t-visa": "t nonimmigrant status trafficking victim",
    "sij": "special immigrant juvenile",
    "sijs": "special immigrant juvenile status",
    "i-130": "petition for alien relative",
    "i130": "petition for alien relative",
    "i-140": "immigrant petition for alien worker",
    "i140": "immigrant petition for alien worker",
    "i-485": "application to register permanent residence",
    "i485": "application to register permanent residence",
    "i-751": "petition to remove conditions",
    "i751": "petition to remove conditions",
    "i-589": "application for asylum",
    "i-601": "application for waiver of inadmissibility",
    "i-601a": "provisional unlawful presence waiver",
    "i-212": "application for permission to reapply",
    "i-765": "application for employment authorization",
    "ead": "employment authorization document",
    "work permit": "employment authorization document",
    "work authorization": "employment authorization",
    "combo card": "employment authorization and advance parole card",
    "advance parole": "advance parole travel document",
    "ap": "advance parole travel document",
    "i-131": "application for travel document",
    "n-400": "application for naturalization",
    "oath ceremony": "naturalization oath ceremony",
    "citizenship test": "naturalization civics and english examination",
    "unlawful presence": "unlawful presence accrual",
    "overstay": "unlawful presence visa overstay",
    "out of status": "failure to maintain nonimmigrant status",
    "visa overstay": "unlawful presence visa overstay",
    "3 year bar": "three-year inadmissibility bar",
    "10 year bar": "ten-year inadmissibility bar",
    "3/10 bar": "unlawful presence bars",
    "three year bar": "three-year inadmissibility bar",
    "ten year bar": "ten-year inadmissibility bar",
    "permanent bar": "permanent inadmissibility bar",
    "expedited removal": "expedited removal proceedings",
    "credible fear": "credible fear of persecution interview",
    "reasonable fear": "reasonable fear of persecution interview",
    "bond": "immigration bond custody determination",
    "ice hold": "immigration detainer",
    "detainer": "immigration detainer",
    "voluntary departure": "voluntary departure in lieu of removal",
    "vd": "voluntary departure in lieu of removal",
    "cancellation": "cancellation of removal",
    "42a": "cancellation of removal for lawful permanent residents",
    "42b": "cancellation of removal for non-permanent residents",
    "registry": "registry under ina section 249",
    "private bill": "private immigration legislation",
    "consular processing": "immigrant visa consular processing",
    "cp": "immigrant visa consular processing",
    "nvc": "national visa center",
    "visa bulletin": "department of state visa bulletin",
    "priority date": "immigrant visa priority date",
    "current": "visa number immediately available",
    "retrogression": "visa bulletin retrogression",
    "backlog": "immigrant visa category backlog",
    "per country limit": "per-country numerical limitation",
    "cspa": "child status protection act",
    "aging out": "child aging out of eligibility",
    "marriage fraud": "marriage fraud determination ina 204(c)",
    "sham marriage": "fraudulent marriage for immigration benefit",
    "bona fide marriage": "good faith marriage determination",
    "extreme hardship": "extreme hardship to qualifying relative",
    "exceptional hardship": "exceptional and extremely unusual hardship",
    "gmc": "good moral character",
    "good moral character": "good moral character under ina 101(f)",
    "categorical approach": "categorical approach to criminal convictions",
    "modified categorical": "modified categorical approach",
    "padilla": "padilla v kentucky sixth amendment duty",
    "hranka": "matter of hranka waiver factors",
    "dhanasar": "matter of dhanasar niw framework",
    "kazarian": "kazarian two-step evidentiary analysis",
    "lozada": "matter of lozada ineffective assistance requirements",
    "pereira": "pereira v sessions nta requirements",
    "public charge": "public charge inadmissibility",
    "i-864": "affidavit of support",
    "sponsor": "immigration financial sponsor",
    "joint sponsor": "joint financial sponsor",
    "ac21": "american competitiveness twenty-first century act",
    "portability": "employment-based job portability",
    "pip": "parole in place",
    "parole in place": "parole in place program",
}


class NormalizationResult:
    """Result of semantic normalization on a query."""

    def __init__(self, original: str, normalized: str, substitutions: List[Dict[str, str]]):
        self.original = original
        self.normalized = normalized
        self.substitutions = substitutions

    def to_dict(self) -> Dict[str, Any]:
        return {
            "original": self.original,
            "normalized": self.normalized,
            "substitutions_count": len(self.substitutions),
            "substitutions": self.substitutions,
        }


def normalize_query(text: str) -> NormalizationResult:
    """Apply semantic normalization to an immigration law query.

    Deterministic preprocessing — no probabilistic models, no inference.
    Maps domain jargon, abbreviations, and slang to canonical forms.
    """
    original = text
    normalized = text.lower().strip()
    substitutions: List[Dict[str, str]] = []

    sorted_synonyms = sorted(IMMIGRATION_SYNONYMS.items(), key=lambda x: -len(x[0]))

    for term, canonical in sorted_synonyms:
        pattern = r"\b" + re.escape(term) + r"\b"
        if re.search(pattern, normalized, re.IGNORECASE):
            normalized = re.sub(pattern, canonical, normalized, flags=re.IGNORECASE)
            substitutions.append({"from": term, "to": canonical})

    return NormalizationResult(original=original, normalized=normalized, substitutions=substitutions)


# =============================================================================
# METRICS COLLECTOR
# =============================================================================

class MetricsCollector:
    """Lightweight operational metrics. No external dependencies."""

    def __init__(self) -> None:
        self.latencies: List[float] = []
        self.errors: List[float] = []
        self.queries: List[float] = []
        self.doctrine_hits: int = 0
        self.doctrine_misses: int = 0
        self.last_error: Optional[str] = None
        self.active_queries: int = 0
        self._max_latencies: int = 100

    def record_query(self, latency_ms: float, doctrine_hit: bool) -> None:
        now = time.time()
        self.latencies.append(latency_ms)
        if len(self.latencies) > self._max_latencies:
            self.latencies.pop(0)
        self.queries.append(now)
        cutoff = now - 3600
        self.queries = [t for t in self.queries if t > cutoff]
        if doctrine_hit:
            self.doctrine_hits += 1
        else:
            self.doctrine_misses += 1

    def record_error(self, error_msg: str) -> None:
        self.errors.append(time.time())
        self.last_error = f"{datetime.now(timezone.utc).isoformat()}: {error_msg[:200]}"
        cutoff = time.time() - 86400
        self.errors = [t for t in self.errors if t > cutoff]

    def query_start(self) -> None:
        self.active_queries += 1

    def query_end(self) -> None:
        self.active_queries = max(0, self.active_queries - 1)

    def get_latency_stats(self) -> Dict[str, float]:
        if not self.latencies:
            return {"avg_ms": 0.0, "p50_ms": 0.0, "p95_ms": 0.0, "p99_ms": 0.0, "last_ms": 0.0}
        s = sorted(self.latencies)
        n = len(s)
        return {
            "avg_ms": round(sum(s) / n, 2),
            "p50_ms": round(s[int(n * 0.50)], 2),
            "p95_ms": round(s[min(int(n * 0.95), n - 1)], 2),
            "p99_ms": round(s[min(int(n * 0.99), n - 1)], 2),
            "last_ms": round(s[-1], 2),
        }

    def get_error_stats(self) -> Dict[str, Any]:
        now = time.time()
        return {
            "last_hour": sum(1 for t in self.errors if t > now - 3600),
            "last_24h": len(self.errors),
            "last_error": self.last_error,
        }

    def get_cache_hit_rate(self) -> float:
        total = self.doctrine_hits + self.doctrine_misses
        return round(self.doctrine_hits / max(total, 1), 4)

    def queries_last_hour(self) -> int:
        cutoff = time.time() - 3600
        return sum(1 for t in self.queries if t > cutoff)


_metrics = MetricsCollector()


def get_metrics() -> MetricsCollector:
    return _metrics


# =============================================================================
# PYDANTIC REQUEST / RESPONSE MODELS
# =============================================================================

class ImmigrationQuery(BaseModel):
    """Professional immigration law query request."""
    question: str = Field(..., min_length=10, description="Immigration law question requiring analysis")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response depth mode")
    jurisdiction: str = Field(default="US", description="Jurisdiction context")
    visa_category: Optional[str] = Field(default=None, description="Specific visa category if known")
    alien_status: Optional[str] = Field(default=None, description="Current immigration status")
    include_trace: bool = Field(default=False, description="Include reasoning trace in response")


class Citation(BaseModel):
    """Structured legal citation."""
    authority: str
    reference: str
    relevance: str


class ReasoningStep(BaseModel):
    """Single step in structured reasoning chain."""
    step: int
    analysis: str
    authority: Optional[str] = None


class ZonedConclusion(BaseModel):
    """Conclusion pinned to a specific analysis zone."""
    zone: str
    conclusion: str
    confidence: float
    caveats: List[str] = Field(default_factory=list)
    action_items: List[str] = Field(default_factory=list)


class FactFragility(BaseModel):
    """Fragility assessment for a factual conclusion."""
    fact: str
    fragility_score: float
    fragility_tier: str
    single_source: bool
    source_count: int
    fragility_factors: List[str] = Field(default_factory=list)
    narrative: str = ""


class ImmigrationResponse(BaseModel):
    """Professional immigration law intelligence response."""
    query_id: str
    question: str
    mode: ResponseMode
    conclusion: str
    reasoning: str
    key_factors: List[str]
    citations: List[Citation]
    risk_level: str = "medium"
    risk_narrative: str = ""
    doctrine_match: bool
    confidence_band: str
    confidence_score: float
    response_layer: str
    latency_ms: float
    conflict_detected: bool = False
    conflict_resolution: Optional[Dict[str, Any]] = None
    authority_weight: Optional[int] = None
    determinism_hash: Optional[str] = None
    zoned_analysis: Optional[List[Dict[str, Any]]] = None
    fact_fragility: Optional[List[Dict[str, Any]]] = None
    coverage_report: Optional[Dict[str, Any]] = None
    counter_arguments: Optional[List[str]] = None
    practice_tips: Optional[List[str]] = None
    reasoning_trace: Optional[List[ReasoningStep]] = None
    limitations: List[str] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    version: str = ENGINE_VERSION
    engine_id: str = ENGINE_ID


class HealthResponse(BaseModel):
    """Comprehensive system health check."""
    status: Literal["healthy", "degraded", "unhealthy"]
    engine: str
    engine_id: str
    version: str
    uptime_seconds: float
    api_latency: Dict[str, float]
    doctrine_cache: Dict[str, Any]
    memory_mb: Dict[str, float]
    active_queries: int
    queries_last_hour: int
    error_rate: Dict[str, Any]
    doctrine_freshness: Dict[str, Any]
    cache_hit_rate: float
    telemetry: Dict[str, Any]


class BatchQuery(BaseModel):
    """Batch query request."""
    queries: List[ImmigrationQuery] = Field(..., min_length=1, max_length=10)


class ExplainRequest(BaseModel):
    """Request explanation of a prior query."""
    query_id: str


# =============================================================================
# DOCTRINE BLOCK — Pre-compiled expert reasoning
# =============================================================================

@dataclass
class DoctrineBlock:
    """Pre-compiled immigration law expert reasoning block with authority hardening."""
    topic_key: str
    topic: str
    keywords: List[str]
    conclusion_template: str
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[Dict[str, str]]
    counter_arguments: List[str]
    applicability_test: str
    confidence_stratification: str = "DEFENSIBLE"
    risk_level: str = "MEDIUM"
    related_doctrines: List[str] = field(default_factory=list)
    last_updated: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def get_authority_weight(self) -> int:
        """Calculate weighted authority score for this doctrine."""
        if not self.primary_authority:
            return 0
        total = 0
        for auth in self.primary_authority:
            auth_type = auth.get("authority", "").lower()
            ref = auth.get("reference", "").lower()
            if "ina" in auth_type or "8 usc" in ref:
                total += AuthorityLevel.INA.weight
            elif "cfr" in auth_type or "8 cfr" in ref or "20 cfr" in ref or "22 cfr" in ref:
                total += AuthorityLevel.CFR.weight
            elif any(x in auth_type for x in ["case", "court", "v.", "vs"]):
                total += AuthorityLevel.COURT_CASE.weight
            elif any(x in auth_type for x in ["uscis", "bia", "aao", "bia", "memo", "policy"]):
                total += AuthorityLevel.AGENCY_GUIDANCE.weight
            else:
                total += AuthorityLevel.COMMENTARY.weight
        return total


# =============================================================================
# DOCTRINE CACHE — Load from doctrines JSON
# =============================================================================

def _load_doctrine_cache() -> Dict[str, DoctrineBlock]:
    """Load doctrine blocks from lg11_doctrines.json."""
    doctrines_path = ENGINE_DIR / "lg11_doctrines.json"
    cache: Dict[str, DoctrineBlock] = {}

    if not doctrines_path.exists():
        logger.warning("Doctrine file not found: {}", doctrines_path)
        return cache

    try:
        raw = json.loads(doctrines_path.read_text(encoding="utf-8"))
        blocks = raw.get("doctrines", [])
        for block_data in blocks:
            topic_key = block_data.get("topic_key", "")
            if not topic_key:
                continue
            cache[topic_key] = DoctrineBlock(
                topic_key=topic_key,
                topic=block_data.get("topic", ""),
                keywords=block_data.get("keywords", []),
                conclusion_template=block_data.get("conclusion_template", ""),
                reasoning_framework=block_data.get("reasoning_framework", ""),
                key_factors=block_data.get("key_factors", []),
                primary_authority=block_data.get("primary_authority", []),
                counter_arguments=block_data.get("counter_arguments", []),
                applicability_test=block_data.get("applicability_test", ""),
                confidence_stratification=block_data.get("confidence_stratification", "SUPPORTABLE"),
                risk_level=block_data.get("risk_level", "MEDIUM"),
            )
        logger.info("Loaded {} doctrine blocks from {}", len(cache), doctrines_path)
    except Exception as exc:
        logger.error("Failed to load doctrines: {}", exc)

    return cache


DOCTRINE_CACHE: Dict[str, DoctrineBlock] = _load_doctrine_cache()


# =============================================================================
# DOCTRINE MATCHING ENGINE
# =============================================================================

@dataclass
class MatchResult:
    """Result of doctrine matching with conflict resolution metadata."""
    doctrine: Optional[DoctrineBlock]
    topic_key: Optional[str]
    match_score: int
    authority_weight: int
    conflict_detected: bool
    conflict_resolution: Optional[Dict[str, Any]]
    all_candidates: List[Dict[str, Any]]
    determinism_hash: str

    @property
    def is_match(self) -> bool:
        return self.doctrine is not None


@dataclass
class ConflictResolution:
    """Explicit resolution when multiple doctrines apply."""
    competing_doctrines: List[str]
    resolution_rationale: str
    authority_basis: str
    rejected_alternatives: List[Dict[str, str]]


def _score_doctrine(query_lower: str, doctrine: DoctrineBlock) -> int:
    """Score how well a doctrine matches a query via keyword overlap."""
    score = 0
    query_words = set(query_lower.split())
    for kw in doctrine.keywords:
        kw_lower = kw.lower()
        if kw_lower in query_lower:
            word_count = len(kw_lower.split())
            score += word_count * 10
        else:
            kw_words = set(kw_lower.split())
            overlap = query_words & kw_words
            score += len(overlap) * 3

    if doctrine.topic.lower() in query_lower:
        score += 25

    applicability_lower = doctrine.applicability_test.lower()
    app_words = set(applicability_lower.split())
    overlap = query_words & app_words
    score += len(overlap) * 2

    return score


def match_doctrine(query: str) -> MatchResult:
    """Match a normalized query against the doctrine cache.

    Resolution protocol when multiple doctrines match:
        1. Highest keyword match score
        2. Highest authority weight (tiebreaker)
        3. Most recent update (second tiebreaker)
    """
    query_lower = query.lower()
    candidates: List[Dict[str, Any]] = []

    for key, doctrine in DOCTRINE_CACHE.items():
        score = _score_doctrine(query_lower, doctrine)
        if score > 0:
            candidates.append({
                "topic_key": key,
                "score": score,
                "authority_weight": doctrine.get_authority_weight(),
                "confidence": doctrine.confidence_stratification,
            })

    candidates.sort(key=lambda c: (c["score"], c["authority_weight"]), reverse=True)

    hash_input = f"{query_lower}|{ENGINE_VERSION}|{len(DOCTRINE_CACHE)}"
    det_hash = hashlib.sha256(hash_input.encode()).hexdigest()[:16]

    if not candidates:
        return MatchResult(
            doctrine=None, topic_key=None, match_score=0, authority_weight=0,
            conflict_detected=False, conflict_resolution=None,
            all_candidates=[], determinism_hash=det_hash,
        )

    top = candidates[0]
    conflict_detected = len(candidates) > 1 and candidates[1]["score"] >= top["score"] * 0.8
    conflict_res = None

    if conflict_detected and len(candidates) >= 2:
        conflict_res = {
            "competing_doctrines": [c["topic_key"] for c in candidates[:3]],
            "resolution_rationale": f"Selected '{top['topic_key']}' with score {top['score']} and authority weight {top['authority_weight']}. "
                                   f"Runner-up '{candidates[1]['topic_key']}' scored {candidates[1]['score']}.",
            "authority_basis": f"Authority weight: {top['authority_weight']}",
            "rejected_alternatives": [
                {"topic": c["topic_key"], "reason": f"Lower combined score ({c['score']}) and authority ({c['authority_weight']})"}
                for c in candidates[1:3]
            ],
        }

    matched_doctrine = DOCTRINE_CACHE.get(top["topic_key"])
    return MatchResult(
        doctrine=matched_doctrine,
        topic_key=top["topic_key"],
        match_score=top["score"],
        authority_weight=top["authority_weight"],
        conflict_detected=conflict_detected,
        conflict_resolution=conflict_res,
        all_candidates=candidates[:10],
        determinism_hash=det_hash,
    )


# =============================================================================
# MULTI-DOCTRINE ANALYSIS — Issue Decomposition and Stratification
# =============================================================================

ISSUE_KEYWORDS: Dict[IssueCategory, List[str]] = {
    IssueCategory.VISA_CLASSIFICATION: [
        "visa", "h-1b", "l-1", "o-1", "eb-1", "eb-2", "eb-3", "eb-5", "f-1", "j-1",
        "b-1", "b-2", "k-1", "r-1", "e-2", "tn", "visa category", "classification",
    ],
    IssueCategory.ADMISSIBILITY: [
        "inadmissible", "inadmissibility", "212(a)", "public charge", "health ground",
        "criminal ground", "fraud", "misrepresentation", "documentation",
    ],
    IssueCategory.DEPORTABILITY: [
        "deportable", "deportability", "237(a)", "removable", "removal ground",
        "aggravated felony", "crime", "conviction", "criminal",
    ],
    IssueCategory.RELIEF_FROM_REMOVAL: [
        "relief", "cancellation", "asylum", "withholding", "cat", "voluntary departure",
        "waiver", "212(h)", "212(i)", "601", "601a",
    ],
    IssueCategory.CITIZENSHIP: [
        "naturalization", "citizenship", "n-400", "oath", "civics", "derivative citizenship",
        "acquisition", "good moral character",
    ],
    IssueCategory.EMPLOYMENT_AUTHORIZATION: [
        "ead", "work permit", "employment authorization", "i-765", "work authorization",
        "unauthorized employment",
    ],
    IssueCategory.FAMILY_UNITY: [
        "family", "spouse", "child", "parent", "sibling", "i-130", "immediate relative",
        "preference category", "family petition",
    ],
    IssueCategory.HUMANITARIAN_PROTECTION: [
        "asylum", "refugee", "persecution", "tps", "daca", "vawa", "u visa", "t visa",
        "trafficking", "humanitarian", "sij",
    ],
    IssueCategory.CRIMINAL_CONSEQUENCES: [
        "criminal", "conviction", "cimt", "aggravated felony", "drug", "dui", "domestic violence",
        "categorical approach", "padilla",
    ],
    IssueCategory.UNLAWFUL_PRESENCE: [
        "unlawful presence", "overstay", "3 year bar", "10 year bar", "out of status",
        "accrual", "tolling",
    ],
    IssueCategory.CONSULAR_PROCESSING: [
        "consular", "embassy", "ds-260", "nvc", "visa interview", "221(g)", "consulate",
    ],
    IssueCategory.ADJUSTMENT_OF_STATUS: [
        "adjustment", "i-485", "245", "245(i)", "concurrent filing", "ead/ap",
    ],
}


def decompose_query(query: str) -> List[IssueCategory]:
    """Decompose a query into issue categories based on keyword analysis."""
    query_lower = query.lower()
    detected: List[Tuple[IssueCategory, int]] = []

    for category, keywords in ISSUE_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in query_lower)
        if score > 0:
            detected.append((category, score))

    detected.sort(key=lambda x: x[1], reverse=True)
    return [cat for cat, _ in detected]


@dataclass
class StratifiedMatch:
    """Result of multi-doctrine stratified matching."""
    issues_detected: List[IssueCategory]
    primary: Optional[MatchResult]
    secondary: List[MatchResult]
    tertiary: List[MatchResult]
    resolution_hierarchy: List[Dict[str, Any]]
    total_doctrines_matched: int
    determinism_hash: str
    coverage_report: Optional[Dict[str, Any]] = None

    @property
    def is_multi_doctrine(self) -> bool:
        has_primary = self.primary is not None and self.primary.is_match
        has_secondary = any(m.is_match for m in self.secondary)
        has_tertiary = any(m.is_match for m in self.tertiary)
        return sum([has_primary, has_secondary, has_tertiary]) > 1

    @property
    def all_matched_topics(self) -> List[str]:
        topics: List[str] = []
        if self.primary and self.primary.topic_key:
            topics.append(self.primary.topic_key)
        for m in self.secondary:
            if m.topic_key:
                topics.append(m.topic_key)
        for m in self.tertiary:
            if m.topic_key:
                topics.append(m.topic_key)
        return topics


def stratified_match(query: str) -> StratifiedMatch:
    """Perform multi-doctrine stratified matching.

    Decomposes the query into issue categories, then matches doctrines
    at primary (classification), secondary (constraints), and tertiary
    (waivers/exceptions) strata.
    """
    issues = decompose_query(query)
    query_lower = query.lower()

    all_scored: List[Tuple[str, DoctrineBlock, int]] = []
    for key, doctrine in DOCTRINE_CACHE.items():
        score = _score_doctrine(query_lower, doctrine)
        if score > 5:
            all_scored.append((key, doctrine, score))

    all_scored.sort(key=lambda x: x[2], reverse=True)

    primary_match: Optional[MatchResult] = None
    secondary_matches: List[MatchResult] = []
    tertiary_matches: List[MatchResult] = []
    used_keys: set = set()

    hash_parts: List[str] = [query_lower, ENGINE_VERSION]

    if all_scored:
        top_key, top_doc, top_score = all_scored[0]
        used_keys.add(top_key)
        primary_match = MatchResult(
            doctrine=top_doc, topic_key=top_key, match_score=top_score,
            authority_weight=top_doc.get_authority_weight(),
            conflict_detected=False, conflict_resolution=None,
            all_candidates=[], determinism_hash="",
        )
        hash_parts.append(top_key)

    for key, doc, score in all_scored[1:4]:
        if key not in used_keys:
            used_keys.add(key)
            secondary_matches.append(MatchResult(
                doctrine=doc, topic_key=key, match_score=score,
                authority_weight=doc.get_authority_weight(),
                conflict_detected=False, conflict_resolution=None,
                all_candidates=[], determinism_hash="",
            ))
            hash_parts.append(key)

    for key, doc, score in all_scored[4:7]:
        if key not in used_keys:
            used_keys.add(key)
            tertiary_matches.append(MatchResult(
                doctrine=doc, topic_key=key, match_score=score,
                authority_weight=doc.get_authority_weight(),
                conflict_detected=False, conflict_resolution=None,
                all_candidates=[], determinism_hash="",
            ))
            hash_parts.append(key)

    resolution_hierarchy: List[Dict[str, Any]] = []
    if primary_match and primary_match.is_match:
        resolution_hierarchy.append({
            "stratum": "primary",
            "topic": primary_match.topic_key,
            "score": primary_match.match_score,
            "role": "Classification / eligibility determination",
        })
    for m in secondary_matches:
        if m.is_match:
            resolution_hierarchy.append({
                "stratum": "secondary",
                "topic": m.topic_key,
                "score": m.match_score,
                "role": "Constraint / bar / condition",
            })
    for m in tertiary_matches:
        if m.is_match:
            resolution_hierarchy.append({
                "stratum": "tertiary",
                "topic": m.topic_key,
                "score": m.match_score,
                "role": "Waiver / exception / discretionary relief",
            })

    det_hash = hashlib.sha256("|".join(hash_parts).encode()).hexdigest()[:16]
    total_matched = (
        (1 if primary_match and primary_match.is_match else 0) +
        sum(1 for m in secondary_matches if m.is_match) +
        sum(1 for m in tertiary_matches if m.is_match)
    )

    return StratifiedMatch(
        issues_detected=issues,
        primary=primary_match,
        secondary=secondary_matches,
        tertiary=tertiary_matches,
        resolution_hierarchy=resolution_hierarchy,
        total_doctrines_matched=total_matched,
        determinism_hash=det_hash,
    )
