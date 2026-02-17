"""
R04 Violation Detector — TIE-20 Gold Standard Engine
=====================================================

Regulatory violation detection, classification, and penalty assessment for
oil & gas, environmental, and industrial safety domains. Patterns violations
against RRC (16 TAC Chapter 3), TCEQ (30 TAC), EPA (40 CFR), OSHA, DOT/PHMSA
rules with full authority hardening, adversarial defense, and epistemic guardrails.

Engine ID: R04
Port: 8704
Domain: regulatory_compliance / violation_detection
Version: 2.0.0
TIE Components: 20/20

Authority Hierarchy (weights 1-10):
  16 TAC Chapter 3 (RRC): 10
  30 TAC (TCEQ Environmental): 9
  40 CFR (EPA Federal): 9
  29 CFR (OSHA Safety): 8
  RRC Statewide Rules: 8
  TCEQ Orders/Precedent: 7
  Case Law Precedent: 7
  Industry Standards (API/ANSI): 5
  Technical Guidance Documents: 4

ECHO OMEGA PRIME — Commander Bobby Don McWilliams II
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import sys
import time
import uuid
from collections import defaultdict
from contextlib import asynccontextmanager
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import uvicorn
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import BaseModel, Field

# ═══════════════════════════════════════════════════════════════════════════════
# PATH SETUP — Ensure sibling modules importable
# ═══════════════════════════════════════════════════════════════════════════════
ENGINE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ENGINE_DIR))
sys.path.insert(0, str(ENGINE_DIR.parent / "_shared"))

from doctrines import (
    DOCTRINE_BLOCKS,
    INTERACTION_EDGES,
    ConfidenceStratification,
    DoctrineBlock,
    IssueCategory,
)
from semantic import (
    extract_keywords,
    normalize_enforcement_action,
    normalize_query,
    normalize_regulatory_authority,
    normalize_severity_level,
    normalize_violation_type,
)
from search import (
    ViolationSearchResult,
    calculate_relevance_score,
    search_violation_patterns,
)
from telemetry import (
    ErrorDomain,
    TelemetryCollector,
)

try:
    from cloud_retriever import CognitionCloudRetriever
except ImportError:
    CognitionCloudRetriever = None

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
ENGINE_ID = "R04"
ENGINE_NAME = "Violation Detector"
ENGINE_VERSION = "2.0.0"
ENGINE_PORT = 8704
ENGINE_DOMAIN = "regulatory_violation_detection"
ENGINE_TIER = "TIER_5_REGULATORY"

CONFIG_PATH = ENGINE_DIR / "config.json"
AUDIT_LOG_DIR = ENGINE_DIR / "logs"
AUDIT_LOG_DIR.mkdir(parents=True, exist_ok=True)

# Load config
_config: Dict[str, Any] = {}
if CONFIG_PATH.exists():
    with open(CONFIG_PATH, "r", encoding="utf-8") as _f:
        _config = json.load(_f)

# ═══════════════════════════════════════════════════════════════════════════════
# LOGGING SETUP (TIE-18: Loguru, never print)
# ═══════════════════════════════════════════════════════════════════════════════
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level:<8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | {message}",
    level="INFO",
)
logger.add(
    AUDIT_LOG_DIR / "r04_engine.log",
    rotation="10 MB",
    retention="30 days",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level:<8} | {name}:{function}:{line} | {message}",
)

# ═══════════════════════════════════════════════════════════════════════════════
# BANNED PHRASES — Epistemic Guardrails (TIE-14 related)
# ═══════════════════════════════════════════════════════════════════════════════
BANNED_PHRASES: List[str] = [
    "definitely a violation",
    "certainly will be penalized",
    "guaranteed enforcement",
    "no chance of penalty",
    "impossible to violate",
    "always results in revocation",
    "never leads to enforcement",
    "zero risk of",
    "100% compliant",
    "absolutely no violation",
    "guaranteed dismissal",
    "will definitely win",
    "no possible defense",
]

# ═══════════════════════════════════════════════════════════════════════════════
# PYDANTIC MODELS — Typed I/O (TIE-17)
# ═══════════════════════════════════════════════════════════════════════════════


class QueryRequest(BaseModel):
    """Input model for violation detection queries."""
    query: str = Field(..., min_length=3, max_length=5000, description="Violation query text")
    mode: str = Field(default="FAST", description="Response mode: FAST | DEFENSE | MEMO")
    zone: str = Field(default="REPORTING", description="Analysis zone: PLANNING | REPORTING | AUDIT")
    violation_category: Optional[str] = Field(default=None, description="Filter by category")
    regulatory_authority: Optional[str] = Field(default=None, description="Filter by authority (RRC, TCEQ, EPA)")
    include_penalty_estimate: bool = Field(default=True, description="Include penalty range estimate")
    include_cloud_knowledge: bool = Field(default=True, description="Query cloud knowledge base")
    max_doctrines: int = Field(default=10, ge=1, le=50, description="Max doctrine blocks to return")
    trace_id: Optional[str] = Field(default=None, description="External trace ID for correlation")


class AuthorityCitation(BaseModel):
    """Single authority citation with weight."""
    authority: str
    weight: int
    citation_text: str
    authority_level: str  # PRIMARY, SECONDARY, PERSUASIVE, ADVISORY


class ViolationAssessment(BaseModel):
    """Individual violation assessment result."""
    violation_type: str
    description: str
    severity: str  # minor, moderate, serious, severe, catastrophic
    regulatory_authority: str
    applicable_rules: List[str]
    penalty_range_min: float
    penalty_range_max: float
    enforcement_actions: List[str]
    mitigating_factors: List[str]
    aggravating_factors: List[str]
    compliance_history_impact: str
    corrective_actions: List[str]


class FactFragilityScore(BaseModel):
    """Fact fragility assessment for key claims."""
    claim: str
    verifiability: float = Field(ge=0.0, le=1.0)
    recharacterization_risk: float = Field(ge=0.0, le=1.0)
    testimony_dependence: float = Field(ge=0.0, le=1.0)
    overall_fragility: float = Field(ge=0.0, le=1.0)
    warning: Optional[str] = None


class DoctrineResult(BaseModel):
    """Single doctrine match result."""
    topic: str
    confidence: float
    confidence_zone: str
    reasoning_summary: str
    key_factors: List[str]
    authorities: List[AuthorityCitation]
    adversary_position: str
    counter_arguments: List[str]
    resolution_strategy: str
    burden_holder: str


class QueryResponse(BaseModel):
    """Full response model for violation detection queries."""
    engine_id: str = ENGINE_ID
    engine_version: str = ENGINE_VERSION
    query_id: str
    trace_id: str
    timestamp: str
    query_text: str
    normalized_query: str
    response_mode: str
    analysis_zone: str
    layer_used: str  # DOCTRINE_CACHE | SEMANTIC_RETRIEVAL | DEEP_ANALYSIS
    latency_ms: float
    # Core results
    violation_assessments: List[ViolationAssessment] = []
    doctrine_matches: List[DoctrineResult] = []
    # Authority & confidence
    primary_authorities: List[AuthorityCitation] = []
    confidence: float = 0.0
    confidence_zone: str = "DISCLOSURE"
    # Fact fragility
    fact_fragility_scores: List[FactFragilityScore] = []
    # Multi-doctrine decomposition
    issue_categories: List[str] = []
    interaction_edges: List[Dict[str, str]] = []
    strata_analysis: Dict[str, List[str]] = {}
    # Epistemic guardrails
    epistemic_warnings: List[str] = []
    disclosure_caveat: Optional[str] = None
    # Cloud knowledge
    cloud_knowledge_used: bool = False
    cloud_sources: List[str] = []
    # Determinism
    determinism_hash: str = ""
    # Summary
    summary: str = ""
    recommendation: str = ""


class HealthResponse(BaseModel):
    """Health endpoint response."""
    engine_id: str
    engine_name: str
    version: str
    status: str
    uptime_seconds: float
    doctrine_count: int
    issue_categories: int
    interaction_edges: int
    port: int
    domain: str
    cloud_retriever_available: bool
    coverage_percentage: float
    total_queries: int
    error_rate: float
    avg_latency_ms: float
    epistemic_guardrails_active: bool


class MetricsResponse(BaseModel):
    """Metrics endpoint response."""
    engine_id: str
    timestamp: str
    total_queries: int
    avg_latency_ms: float
    p95_latency_ms: float
    p99_latency_ms: float
    error_rate: float
    cache_hit_rate: float
    queries_per_minute: float
    top_violation_types: List[Dict[str, Any]]
    doctrine_coverage: float
    active_traces: int


# ═══════════════════════════════════════════════════════════════════════════════
# TIE-4: AUTHORITY HARDENING
# ═══════════════════════════════════════════════════════════════════════════════

class AuthorityLevel(str, Enum):
    """Hierarchical authority classification."""
    CONSTITUTIONAL = "CONSTITUTIONAL"  # weight 10 — US/TX Constitution
    STATUTORY = "STATUTORY"            # weight 9 — TX Natural Resources Code, Clean Water Act
    REGULATORY = "REGULATORY"          # weight 8 — 16 TAC, 30 TAC, 40 CFR
    STATEWIDE_RULE = "STATEWIDE_RULE"  # weight 7 — RRC Statewide Rules 1-100
    AGENCY_ORDER = "AGENCY_ORDER"      # weight 6 — RRC/TCEQ specific orders
    CASE_LAW = "CASE_LAW"              # weight 5 — Court decisions
    INDUSTRY_STANDARD = "INDUSTRY_STANDARD"  # weight 4 — API, ANSI
    TECHNICAL_GUIDANCE = "TECHNICAL_GUIDANCE"  # weight 3 — agency technical docs
    ADVISORY = "ADVISORY"              # weight 2 — policy letters, informal guidance


AUTHORITY_WEIGHTS: Dict[str, int] = {
    "CONSTITUTIONAL": 10,
    "STATUTORY": 9,
    "REGULATORY": 8,
    "STATEWIDE_RULE": 7,
    "AGENCY_ORDER": 6,
    "CASE_LAW": 5,
    "INDUSTRY_STANDARD": 4,
    "TECHNICAL_GUIDANCE": 3,
    "ADVISORY": 2,
}


def classify_authority(citation: str) -> Tuple[AuthorityLevel, int]:
    """Classify a citation into authority level with weight."""
    citation_lower = citation.lower()

    if "constitution" in citation_lower:
        return AuthorityLevel.CONSTITUTIONAL, 10
    elif any(kw in citation_lower for kw in ["natural resources code", "water code", "clean water act", "clean air act", "rcra", "cercla"]):
        return AuthorityLevel.STATUTORY, 9
    elif any(kw in citation_lower for kw in ["16 tac", "30 tac", "40 cfr", "29 cfr", "49 cfr"]):
        return AuthorityLevel.REGULATORY, 8
    elif "statewide rule" in citation_lower or "rule " in citation_lower:
        return AuthorityLevel.STATEWIDE_RULE, 7
    elif any(kw in citation_lower for kw in ["order", "docket", "rrc no.", "tceq no."]):
        return AuthorityLevel.AGENCY_ORDER, 6
    elif any(kw in citation_lower for kw in ["v.", "court", "s.w.", "f.3d", "tex. app"]):
        return AuthorityLevel.CASE_LAW, 5
    elif any(kw in citation_lower for kw in ["api", "ansi", "astm", "nfpa"]):
        return AuthorityLevel.INDUSTRY_STANDARD, 4
    elif any(kw in citation_lower for kw in ["guidance", "bulletin", "advisory"]):
        return AuthorityLevel.TECHNICAL_GUIDANCE, 3
    else:
        return AuthorityLevel.ADVISORY, 2


def resolve_authority_conflict(authorities: List[Tuple[str, AuthorityLevel, int]]) -> List[Tuple[str, AuthorityLevel, int]]:
    """
    Resolve conflicts between authorities by weight.
    Higher authority always controls. Returns sorted list.
    """
    return sorted(authorities, key=lambda x: x[2], reverse=True)


def build_authority_citations(doctrine: DoctrineBlock) -> List[AuthorityCitation]:
    """Build structured authority citations from a doctrine block."""
    citations: List[AuthorityCitation] = []
    for auth_text in doctrine.primary_authority:
        level, weight = classify_authority(auth_text)
        citations.append(AuthorityCitation(
            authority=auth_text,
            weight=weight,
            citation_text=auth_text,
            authority_level=level.value,
        ))
    return sorted(citations, key=lambda c: c.weight, reverse=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TIE-5: CONFIDENCE STRATIFICATION
# ═══════════════════════════════════════════════════════════════════════════════

CONFIDENCE_THRESHOLDS = {
    "DEFENSIBLE": 0.90,
    "AGGRESSIVE": 0.70,
    "DISCLOSURE": 0.50,
    "HIGH_RISK": 0.0,
}


def stratify_confidence(score: float) -> str:
    """Map numerical confidence to stratification zone."""
    if score >= CONFIDENCE_THRESHOLDS["DEFENSIBLE"]:
        return "DEFENSIBLE"
    elif score >= CONFIDENCE_THRESHOLDS["AGGRESSIVE"]:
        return "AGGRESSIVE"
    elif score >= CONFIDENCE_THRESHOLDS["DISCLOSURE"]:
        return "DISCLOSURE"
    else:
        return "HIGH_RISK"


def compute_aggregate_confidence(doctrine_scores: List[float]) -> float:
    """Compute aggregate confidence from multiple doctrine matches."""
    if not doctrine_scores:
        return 0.0
    # Weighted toward highest confidence match but pulled down by low ones
    max_conf = max(doctrine_scores)
    avg_conf = sum(doctrine_scores) / len(doctrine_scores)
    return (max_conf * 0.6) + (avg_conf * 0.4)


# ═══════════════════════════════════════════════════════════════════════════════
# TIE-13: ZONED ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════

class AnalysisZone(str, Enum):
    """Strict zone separation — zones NEVER blur."""
    PLANNING = "PLANNING"    # Forward-looking strategy, risk assessment
    REPORTING = "REPORTING"  # Factual, historical documentation
    AUDIT = "AUDIT"          # Compliance-focused, evidence-based


ZONE_PREFIXES = {
    "PLANNING": "PLANNING ADVISORY: ",
    "REPORTING": "REGULATORY REPORT: ",
    "AUDIT": "COMPLIANCE AUDIT FINDING: ",
}

ZONE_GUIDELINES = {
    "PLANNING": "Provide forward-looking guidance on violation risk, preventive measures, and compliance strategy. Do NOT state audit conclusions.",
    "REPORTING": "Document factual findings about violations, regulatory citations, and historical enforcement. Do NOT provide planning advice.",
    "AUDIT": "Assess compliance status, identify deficiencies, and cite evidence. Do NOT blend with forward-looking strategy.",
}


def validate_zone(zone: str) -> AnalysisZone:
    """Validate and normalize analysis zone."""
    zone_upper = zone.upper().strip()
    try:
        return AnalysisZone(zone_upper)
    except ValueError:
        logger.warning(f"Invalid zone '{zone}', defaulting to REPORTING")
        return AnalysisZone.REPORTING


def enforce_zone_separation(text: str, zone: AnalysisZone) -> str:
    """
    Enforce zone boundaries — strip cross-zone language.
    PLANNING advice never appears in AUDIT output, etc.
    """
    planning_indicators = ["consider", "strategy", "future", "recommend", "plan for", "going forward"]
    audit_indicators = ["finding", "deficiency", "non-compliance", "evidence shows", "audit reveals"]
    reporting_indicators = ["recorded", "documented", "historical", "occurred on", "was reported"]

    if zone == AnalysisZone.AUDIT:
        for indicator in planning_indicators:
            if indicator in text.lower():
                text = text.replace(indicator, f"[ZONE VIOLATION REMOVED: {indicator}]")
                logger.warning(f"Zone violation: PLANNING language in AUDIT zone: '{indicator}'")
    elif zone == AnalysisZone.PLANNING:
        for indicator in audit_indicators:
            if indicator in text.lower():
                text = text.replace(indicator, f"[ZONE VIOLATION REMOVED: {indicator}]")
                logger.warning(f"Zone violation: AUDIT language in PLANNING zone: '{indicator}'")

    return ZONE_PREFIXES.get(zone.value, "") + text


# ═══════════════════════════════════════════════════════════════════════════════
# TIE-14: FACT FRAGILITY SCORING
# ═══════════════════════════════════════════════════════════════════════════════

def score_fact_fragility(
    claim: str,
    has_documentary_evidence: bool = False,
    relies_on_testimony: bool = False,
    subject_to_recharacterization: bool = False,
    regulatory_ambiguity: bool = False,
    multi_jurisdiction: bool = False,
) -> FactFragilityScore:
    """
    Score the fragility of a factual claim in the violation context.

    Fragility = how easily the fact could be challenged or reinterpreted.
    High fragility = less reliable as basis for violation finding.
    """
    verifiability = 0.9 if has_documentary_evidence else 0.4
    recharacterization_risk = 0.7 if subject_to_recharacterization else 0.2
    if regulatory_ambiguity:
        recharacterization_risk = min(1.0, recharacterization_risk + 0.2)
    testimony_dependence = 0.8 if relies_on_testimony else 0.1
    if multi_jurisdiction:
        recharacterization_risk = min(1.0, recharacterization_risk + 0.15)

    # Overall = weighted average (lower verifiability + higher risk = more fragile)
    overall = (
        (1.0 - verifiability) * 0.35
        + recharacterization_risk * 0.35
        + testimony_dependence * 0.30
    )

    warning = None
    if overall > 0.7:
        warning = "HIGH FRAGILITY: This finding may not withstand adversarial challenge. Seek corroborating evidence."
    elif overall > 0.5:
        warning = "MODERATE FRAGILITY: Consider additional documentation before relying on this finding."

    return FactFragilityScore(
        claim=claim,
        verifiability=round(verifiability, 3),
        recharacterization_risk=round(recharacterization_risk, 3),
        testimony_dependence=round(testimony_dependence, 3),
        overall_fragility=round(overall, 3),
        warning=warning,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# TIE-16: DETERMINISM HASH (SHA-256)
# ═══════════════════════════════════════════════════════════════════════════════

def compute_determinism_hash(
    query: str,
    doctrines_triggered: List[str],
    confidence: float,
    zone: str,
    mode: str,
) -> str:
    """
    Compute SHA-256 determinism hash for response reproducibility.
    Excludes nondeterministic elements (timestamps, UUIDs).
    Same query + same doctrines + same config = same hash.
    """
    content = json.dumps({
        "query": query,
        "doctrines": sorted(doctrines_triggered),
        "confidence": round(confidence, 4),
        "zone": zone,
        "mode": mode,
        "engine_version": ENGINE_VERSION,
    }, sort_keys=True)
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


# ═══════════════════════════════════════════════════════════════════════════════
# TIE-9: DRIFT WATCHER
# ═══════════════════════════════════════════════════════════════════════════════

class DriftWatcher:
    """
    Track doctrine usage over time to detect drift.
    Drift = when certain doctrines are never triggered, or when queries
    consistently miss the cache, indicating the doctrine set is stale.
    """

    def __init__(self, all_topics: List[str]):
        self.all_topics: Set[str] = set(all_topics)
        self.triggered_topics: Dict[str, int] = defaultdict(int)
        self.miss_count: int = 0
        self.total_queries: int = 0
        self.first_seen: Dict[str, str] = {}
        self.last_seen: Dict[str, str] = {}
        self.alert_threshold: float = _config.get("telemetry", {}).get("drift_alert_threshold", 0.3)

    def record_hit(self, topic: str) -> None:
        """Record a doctrine cache hit."""
        self.triggered_topics[topic] += 1
        now = datetime.utcnow().isoformat()
        if topic not in self.first_seen:
            self.first_seen[topic] = now
        self.last_seen[topic] = now
        self.total_queries += 1

    def record_miss(self) -> None:
        """Record a doctrine cache miss."""
        self.miss_count += 1
        self.total_queries += 1

    def get_never_triggered(self) -> List[str]:
        """Return doctrine topics that have never been triggered."""
        return sorted(self.all_topics - set(self.triggered_topics.keys()))

    def get_drift_report(self) -> Dict[str, Any]:
        """Generate drift analysis report."""
        never_triggered = self.get_never_triggered()
        coverage = 1.0 - (len(never_triggered) / len(self.all_topics)) if self.all_topics else 0.0
        miss_rate = self.miss_count / self.total_queries if self.total_queries > 0 else 0.0

        drift_detected = miss_rate > self.alert_threshold or coverage < 0.5

        return {
            "total_topics": len(self.all_topics),
            "triggered_topics": len(self.triggered_topics),
            "never_triggered": never_triggered,
            "coverage_percentage": round(coverage * 100, 1),
            "cache_miss_rate": round(miss_rate, 4),
            "total_queries": self.total_queries,
            "drift_detected": drift_detected,
            "alert_threshold": self.alert_threshold,
            "top_triggered": sorted(
                self.triggered_topics.items(),
                key=lambda x: x[1],
                reverse=True,
            )[:10],
        }


# ═══════════════════════════════════════════════════════════════════════════════
# TIE-10: COVERAGE MAP
# ═══════════════════════════════════════════════════════════════════════════════

class CoverageMap:
    """
    Maps doctrine topics to triggered/untriggered status.
    Identifies epistemic gaps — topics the engine cannot handle.
    """

    def __init__(self, doctrines: List[DoctrineBlock]):
        self.doctrine_map: Dict[str, DoctrineBlock] = {d.topic: d for d in doctrines}
        self.triggered: Dict[str, int] = defaultdict(int)
        self.gap_queries: List[str] = []  # Queries that found no doctrine match
        self.category_coverage: Dict[str, Set[str]] = defaultdict(set)

        # Build category map
        for d in doctrines:
            self.category_coverage[d.issue_category.value].add(d.topic)

    def record_trigger(self, topic: str) -> None:
        """Record that a doctrine topic was triggered."""
        self.triggered[topic] += 1

    def record_gap(self, query: str) -> None:
        """Record a query that found no doctrine match (epistemic gap)."""
        if len(self.gap_queries) < 1000:  # cap memory
            self.gap_queries.append(query)

    def get_coverage_report(self) -> Dict[str, Any]:
        """Generate coverage analysis."""
        total = len(self.doctrine_map)
        covered = len(self.triggered)
        coverage_pct = (covered / total * 100) if total > 0 else 0.0

        # Per-category coverage
        category_reports: Dict[str, Dict] = {}
        for cat, topics in self.category_coverage.items():
            cat_covered = sum(1 for t in topics if t in self.triggered)
            category_reports[cat] = {
                "total_topics": len(topics),
                "covered": cat_covered,
                "coverage_pct": round(cat_covered / len(topics) * 100, 1) if topics else 0.0,
                "uncovered_topics": sorted(topics - set(self.triggered.keys())),
            }

        return {
            "total_doctrines": total,
            "triggered_doctrines": covered,
            "overall_coverage_pct": round(coverage_pct, 1),
            "epistemic_gaps": len(self.gap_queries),
            "recent_gap_queries": self.gap_queries[-10:],
            "category_coverage": category_reports,
        }


# ═══════════════════════════════════════════════════════════════════════════════
# TIE-19: MULTI-DOCTRINE DECOMPOSITION
# ═══════════════════════════════════════════════════════════════════════════════

def decompose_violation_query(
    query: str,
    matched_doctrines: List[DoctrineBlock],
) -> Dict[str, Any]:
    """
    Decompose a complex violation query into analyzable strata.

    Uses the INTERACTION_EDGES graph from doctrines.py to identify
    connected issues and build a resolution DAG.
    """
    # Identify issue categories
    categories: Set[str] = set()
    for d in matched_doctrines:
        categories.add(d.issue_category.value)

    # Find interaction edges between matched doctrines
    edges: List[Dict[str, str]] = []
    matched_topics = {d.topic for d in matched_doctrines}
    for edge in INTERACTION_EDGES:
        if edge.get("from") in matched_topics or edge.get("to") in matched_topics:
            edges.append(edge)

    # Build strata (primary = highest confidence, secondary = related, tertiary = peripheral)
    sorted_doctrines = sorted(matched_doctrines, key=lambda d: d.confidence, reverse=True)
    strata: Dict[str, List[str]] = {
        "primary": [],
        "secondary": [],
        "tertiary": [],
    }

    for i, d in enumerate(sorted_doctrines):
        if i < 3:
            strata["primary"].append(d.topic)
        elif i < 7:
            strata["secondary"].append(d.topic)
        else:
            strata["tertiary"].append(d.topic)

    # Resolution strategy per stratum
    resolution_strategies: Dict[str, str] = {}
    for level, topics in strata.items():
        if level == "primary":
            resolution_strategies[level] = "Address these violations first — highest regulatory exposure and clearest authority."
        elif level == "secondary":
            resolution_strategies[level] = "Review these related issues after resolving primary violations."
        else:
            resolution_strategies[level] = "Monitor these peripheral issues; may become primary if circumstances change."

    return {
        "issue_categories": sorted(categories),
        "interaction_edges": edges,
        "strata": strata,
        "resolution_strategies": resolution_strategies,
        "total_doctrines_matched": len(matched_doctrines),
        "decomposition_depth": len(strata["primary"]) + len(strata["secondary"]) + len(strata["tertiary"]),
    }


# ═══════════════════════════════════════════════════════════════════════════════
# TIE-20: DEEP ANALYSIS MODE
# ═══════════════════════════════════════════════════════════════════════════════

def deep_analysis(
    query: str,
    matched_doctrines: List[DoctrineBlock],
    zone: AnalysisZone,
    cloud_knowledge: Optional[List[Dict]] = None,
) -> Dict[str, Any]:
    """
    Full multi-source synthesis with exposed reasoning chain.

    Combines:
    1. Doctrine cache analysis
    2. Cloud knowledge (if available)
    3. Semantic search results
    4. Adversarial counter-argument review
    5. Authority conflict resolution
    """
    reasoning_chain: List[str] = []
    all_authorities: List[Tuple[str, AuthorityLevel, int]] = []
    counter_args: List[str] = []
    violation_assessments: List[Dict] = []

    reasoning_chain.append(f"DEEP ANALYSIS initiated for: {query[:200]}")
    reasoning_chain.append(f"Analysis zone: {zone.value}")
    reasoning_chain.append(f"Doctrines matched: {len(matched_doctrines)}")

    # Step 1: Analyze each matched doctrine
    for doctrine in matched_doctrines:
        reasoning_chain.append(f"\n--- Doctrine: {doctrine.topic} (confidence: {doctrine.confidence}) ---")
        reasoning_chain.append(f"Category: {doctrine.issue_category.value}")
        reasoning_chain.append(f"Reasoning: {doctrine.reasoning_framework[:300]}")

        # Collect authorities
        for auth in doctrine.primary_authority:
            level, weight = classify_authority(auth)
            all_authorities.append((auth, level, weight))

        # Collect counter-arguments
        counter_args.extend(doctrine.counter_arguments)

        # Build violation assessment
        violation_assessments.append({
            "topic": doctrine.topic,
            "confidence": doctrine.confidence,
            "zone": stratify_confidence(doctrine.confidence),
            "burden_holder": doctrine.burden_holder,
            "resolution": doctrine.resolution_strategy,
        })

    # Step 2: Resolve authority conflicts
    resolved = resolve_authority_conflict(all_authorities)
    reasoning_chain.append(f"\nAuthority resolution: {len(resolved)} authorities ranked")
    if resolved:
        reasoning_chain.append(f"Controlling authority: {resolved[0][0]} (weight: {resolved[0][2]})")

    # Step 3: Cloud knowledge integration
    if cloud_knowledge:
        reasoning_chain.append(f"\nCloud knowledge: {len(cloud_knowledge)} additional sources")
        for ck in cloud_knowledge[:3]:
            reasoning_chain.append(f"  - {ck.get('title', 'Untitled')}: {str(ck.get('content', ''))[:200]}")

    # Step 4: Adversarial review
    unique_counter_args = list(set(counter_args))[:10]
    reasoning_chain.append(f"\nAdversarial positions to address: {len(unique_counter_args)}")
    for ca in unique_counter_args:
        reasoning_chain.append(f"  Counter: {ca}")

    # Step 5: Synthesize conclusion
    aggregate_conf = compute_aggregate_confidence([d.confidence for d in matched_doctrines])
    conf_zone = stratify_confidence(aggregate_conf)

    conclusion = (
        f"Based on analysis of {len(matched_doctrines)} regulatory doctrines "
        f"across {len(set(d.issue_category.value for d in matched_doctrines))} categories, "
        f"the aggregate confidence is {aggregate_conf:.2f} ({conf_zone}). "
    )

    if conf_zone == "DEFENSIBLE":
        conclusion += "The violation finding is well-supported by clear regulatory authority and established precedent."
    elif conf_zone == "AGGRESSIVE":
        conclusion += "The violation finding is supportable but faces potential challenges on specific factual elements."
    elif conf_zone == "DISCLOSURE":
        conclusion += "DISCLOSURE REQUIRED: Significant uncertainty exists. Multiple interpretations of the applicable regulations are plausible."
    else:
        conclusion += "HIGH RISK: The violation finding relies on novel regulatory interpretation. Professional review strongly recommended."

    reasoning_chain.append(f"\nCONCLUSION: {conclusion}")

    return {
        "reasoning_chain": reasoning_chain,
        "resolved_authorities": [(a[0], a[1].value, a[2]) for a in resolved[:10]],
        "counter_arguments_addressed": unique_counter_args,
        "violation_assessments": violation_assessments,
        "aggregate_confidence": aggregate_conf,
        "confidence_zone": conf_zone,
        "conclusion": conclusion,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# EPISTEMIC GUARDRAILS
# ═══════════════════════════════════════════════════════════════════════════════

def apply_epistemic_guardrails(
    text: str,
    confidence: float,
    zone: AnalysisZone,
) -> Tuple[str, List[str], Optional[str]]:
    """
    Apply epistemic guardrails to response text.

    Returns:
        (cleaned_text, warnings, disclosure_caveat)
    """
    warnings: List[str] = []
    disclosure_caveat: Optional[str] = None

    # Check for banned phrases
    for phrase in BANNED_PHRASES:
        if phrase.lower() in text.lower():
            text = text.replace(phrase, "[EPISTEMIC OVERRIDE: absolute claim removed]")
            warnings.append(f"Banned phrase removed: '{phrase}'")
            logger.warning(f"Epistemic guardrail triggered: banned phrase '{phrase}'")

    # Low confidence requires disclosure
    if confidence < 0.5:
        disclosure_caveat = (
            "DISCLOSURE: This analysis involves significant regulatory uncertainty. "
            "The applicable rules may be subject to different interpretations, and enforcement "
            "outcomes depend heavily on specific facts, agency discretion, and compliance history. "
            "Consult qualified regulatory counsel before relying on this assessment."
        )
        warnings.append("Low confidence triggered mandatory disclosure caveat")

    # Novel issue detection
    if confidence < 0.3:
        warnings.append(
            "NOVEL REGULATORY ISSUE: This query touches on areas where established "
            "precedent is limited. The analysis is based on analogical reasoning "
            "from related regulatory frameworks."
        )

    # Zone-specific guardrails
    if zone == AnalysisZone.AUDIT:
        # Audit findings must be evidence-based
        if "may" in text.lower() or "might" in text.lower():
            warnings.append("AUDIT ZONE: Speculative language detected. Audit findings should be evidence-based.")

    return text, warnings, disclosure_caveat


# ═══════════════════════════════════════════════════════════════════════════════
# PENALTY ESTIMATION ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

PENALTY_TIERS = _config.get("penalty_tiers", {
    "minor": {"min": 100, "max": 1000},
    "moderate": {"min": 1000, "max": 10000},
    "serious": {"min": 10000, "max": 50000},
    "severe": {"min": 50000, "max": 250000},
    "catastrophic": {"min": 250000, "max": 1000000},
})

AGGRAVATING_MULTIPLIERS = {
    "repeat_offender": 2.0,
    "willful_violation": 3.0,
    "environmental_damage": 1.5,
    "public_health_risk": 2.0,
    "obstruction": 1.5,
    "failure_to_report": 1.3,
    "late_corrective_action": 1.2,
}

MITIGATING_MULTIPLIERS = {
    "self_report": 0.5,
    "immediate_correction": 0.6,
    "first_offense": 0.7,
    "good_compliance_history": 0.75,
    "cooperation": 0.8,
    "financial_hardship": 0.85,
    "voluntary_disclosure": 0.5,
}


def estimate_penalty(
    severity: str,
    aggravating: List[str],
    mitigating: List[str],
) -> Tuple[float, float]:
    """
    Estimate penalty range based on severity and modifiers.

    Returns (min_penalty, max_penalty) after adjustments.
    """
    tier = PENALTY_TIERS.get(severity, PENALTY_TIERS["moderate"])
    base_min = tier["min"]
    base_max = tier["max"]

    # Apply aggravating factors
    agg_multiplier = 1.0
    for factor in aggravating:
        if factor in AGGRAVATING_MULTIPLIERS:
            agg_multiplier *= AGGRAVATING_MULTIPLIERS[factor]

    # Apply mitigating factors
    mit_multiplier = 1.0
    for factor in mitigating:
        if factor in MITIGATING_MULTIPLIERS:
            mit_multiplier *= MITIGATING_MULTIPLIERS[factor]

    adjusted_min = base_min * agg_multiplier * mit_multiplier
    adjusted_max = base_max * agg_multiplier * mit_multiplier

    return round(adjusted_min, 2), round(adjusted_max, 2)


def assess_violation(
    doctrine: DoctrineBlock,
    severity: str = "moderate",
    aggravating: Optional[List[str]] = None,
    mitigating: Optional[List[str]] = None,
) -> ViolationAssessment:
    """Build a full violation assessment from a doctrine match."""
    agg = aggravating or []
    mit = mitigating or []
    penalty_min, penalty_max = estimate_penalty(severity, agg, mit)

    # Extract enforcement actions from doctrine
    enforcement = []
    if severity in ("catastrophic", "severe"):
        enforcement = ["Administrative_Penalty", "Permit_Suspension", "Criminal_Referral"]
    elif severity == "serious":
        enforcement = ["Administrative_Penalty", "Compliance_Order"]
    elif severity == "moderate":
        enforcement = ["Notice_of_Violation", "Administrative_Penalty"]
    else:
        enforcement = ["Notice_of_Violation"]

    corrective_actions = [
        "Submit corrective action plan within 30 days",
        "Implement identified measures within 90 days",
        "Report compliance status quarterly until resolved",
    ]

    # Determine applicable rules from doctrine authorities
    applicable_rules = doctrine.primary_authority[:5]

    return ViolationAssessment(
        violation_type=normalize_violation_type(doctrine.topic),
        description=doctrine.conclusion_template[:500],
        severity=severity,
        regulatory_authority=_determine_primary_authority(doctrine),
        applicable_rules=applicable_rules,
        penalty_range_min=penalty_min,
        penalty_range_max=penalty_max,
        enforcement_actions=enforcement,
        mitigating_factors=[f for f in mit if f in MITIGATING_MULTIPLIERS],
        aggravating_factors=[f for f in agg if f in AGGRAVATING_MULTIPLIERS],
        compliance_history_impact="Repeat violations increase penalty multiplier by 2x per 16 TAC §3.107",
        corrective_actions=corrective_actions,
    )


def _determine_primary_authority(doctrine: DoctrineBlock) -> str:
    """Determine the primary regulatory authority for a doctrine."""
    for auth in doctrine.primary_authority:
        auth_lower = auth.lower()
        if "16 tac" in auth_lower or "rrc" in auth_lower:
            return "RRC"
        elif "30 tac" in auth_lower or "tceq" in auth_lower:
            return "TCEQ"
        elif "40 cfr" in auth_lower or "epa" in auth_lower:
            return "EPA"
        elif "29 cfr" in auth_lower or "osha" in auth_lower:
            return "OSHA"
    return "RRC"  # default for Texas O&G


# ═══════════════════════════════════════════════════════════════════════════════
# THREE-LAYER RESPONSE SYSTEM (TIE-1)
# ═══════════════════════════════════════════════════════════════════════════════

class ViolationDetectorEngine:
    """
    R04 Violation Detector — Main Engine Class

    Implements all 20 TIE components for regulatory violation detection.
    Three-layer response: Doctrine Cache → Semantic Retrieval → Deep Analysis.
    """

    def __init__(self):
        self.engine_id = ENGINE_ID
        self.engine_name = ENGINE_NAME
        self.version = ENGINE_VERSION
        self.start_time = time.time()

        # Load doctrine cache (TIE-3)
        self.doctrines: List[DoctrineBlock] = DOCTRINE_BLOCKS
        self.doctrine_index: Dict[str, DoctrineBlock] = {d.topic: d for d in self.doctrines}
        logger.info(f"Loaded {len(self.doctrines)} doctrine blocks")

        # Telemetry (TIE-8)
        self.telemetry = TelemetryCollector(engine_id=ENGINE_ID)

        # Drift watcher (TIE-9)
        self.drift_watcher = DriftWatcher(all_topics=[d.topic for d in self.doctrines])

        # Coverage map (TIE-10)
        self.coverage_map = CoverageMap(self.doctrines)

        # Cloud retriever
        self.cloud: Optional[Any] = None
        if CognitionCloudRetriever is not None:
            try:
                self.cloud = CognitionCloudRetriever()
                logger.info("Cloud retriever connected")
            except Exception as e:
                logger.warning(f"Cloud retriever unavailable: {e}")

        logger.info(f"{ENGINE_ID} {ENGINE_NAME} v{ENGINE_VERSION} initialized — {len(self.doctrines)} doctrines loaded")

    # ─── LAYER 1: DOCTRINE CACHE (0-200ms) ─────────────────────────────────

    def doctrine_cache_lookup(self, query: str, max_results: int = 10) -> List[DoctrineBlock]:
        """
        Layer 1: Fast doctrine cache lookup by keyword matching.
        Target latency: 0-200ms.
        """
        keywords = extract_keywords(query)
        normalized = normalize_query(query)
        query_lower = normalized.lower()

        scored: List[Tuple[float, DoctrineBlock]] = []

        for doctrine in self.doctrines:
            score = 0.0

            # Keyword match scoring
            doctrine_keywords_lower = [k.lower() for k in doctrine.keywords]
            for kw in keywords:
                if kw.lower() in doctrine_keywords_lower:
                    score += 2.0
                elif any(kw.lower() in dk for dk in doctrine_keywords_lower):
                    score += 1.0

            # Topic match
            if doctrine.topic.lower() in query_lower:
                score += 3.0
            elif any(word in query_lower for word in doctrine.topic.lower().split("_")):
                score += 1.5

            # Category match from query context
            if doctrine.issue_category.value in query_lower:
                score += 1.0

            if score > 0:
                scored.append((score, doctrine))

        # Sort by score descending
        scored.sort(key=lambda x: x[0], reverse=True)
        results = [d for _, d in scored[:max_results]]

        # Track in drift watcher and coverage map
        if results:
            for d in results:
                self.drift_watcher.record_hit(d.topic)
                self.coverage_map.record_trigger(d.topic)
        else:
            self.drift_watcher.record_miss()
            self.coverage_map.record_gap(query)

        return results

    # ─── LAYER 2: SEMANTIC RETRIEVAL (200-2000ms) ──────────────────────────

    async def semantic_retrieval(self, query: str, limit: int = 5) -> List[DoctrineBlock]:
        """
        Layer 2: Semantic search fallback when doctrine cache misses.
        Uses text similarity and cloud knowledge.
        """
        normalized = normalize_query(query)

        # Local semantic search — check all doctrines with relaxed matching
        scored: List[Tuple[float, DoctrineBlock]] = []
        query_terms = set(normalized.lower().split())

        for doctrine in self.doctrines:
            # Build document terms from multiple fields
            doc_terms = set()
            doc_terms.update(doctrine.topic.lower().replace("_", " ").split())
            doc_terms.update(k.lower() for k in doctrine.keywords)
            doc_terms.update(doctrine.conclusion_template.lower().split()[:30])

            relevance = calculate_relevance_score(list(query_terms), list(doc_terms))
            if relevance > 0.1:
                scored.append((relevance, doctrine))

        scored.sort(key=lambda x: x[0], reverse=True)
        results = [d for _, d in scored[:limit]]

        # Track
        for d in results:
            self.drift_watcher.record_hit(d.topic)
            self.coverage_map.record_trigger(d.topic)

        return results

    # ─── LAYER 3: DEEP ANALYSIS (2-30s) ───────────────────────────────────

    async def deep_analysis_layer(
        self,
        query: str,
        matched_doctrines: List[DoctrineBlock],
        zone: AnalysisZone,
    ) -> Dict[str, Any]:
        """
        Layer 3: Full multi-source deep analysis.
        Combines doctrine cache, cloud knowledge, and adversarial review.
        """
        cloud_knowledge = None
        if self.cloud and hasattr(self.cloud, 'search_clauses'):
            try:
                cloud_knowledge = await self.cloud.search_clauses(query, category="regulatory")
            except Exception as e:
                logger.warning(f"Cloud retrieval failed: {e}")

        return deep_analysis(query, matched_doctrines, zone, cloud_knowledge)

    # ─── MAIN QUERY HANDLER ───────────────────────────────────────────────

    async def query(self, request: QueryRequest) -> QueryResponse:
        """
        Main query entry point — three-layer response with full TIE-20 processing.
        """
        start = time.time()
        query_id = self.telemetry.start_trace(request.query, request.mode)
        trace_id = request.trace_id or str(uuid.uuid4())[:12]
        zone = validate_zone(request.zone)

        logger.info(f"Query [{query_id[:8]}] mode={request.mode} zone={zone.value}: {request.query[:100]}")

        # Normalize query (TIE-6)
        normalized = normalize_query(request.query)

        # ── Layer 1: Doctrine Cache ──
        layer_used = "DOCTRINE_CACHE"
        matched = self.doctrine_cache_lookup(normalized, max_results=request.max_doctrines)

        # ── Layer 2: Semantic Retrieval (fallback) ──
        if not matched:
            layer_used = "SEMANTIC_RETRIEVAL"
            matched = await self.semantic_retrieval(normalized, limit=request.max_doctrines)

        # ── Layer 3: Deep Analysis (if still no matches or MEMO mode) ──
        deep_result = None
        if not matched or request.mode == "MEMO":
            layer_used = "DEEP_ANALYSIS" if not matched else layer_used
            # For deep analysis, use whatever we have
            if not matched:
                # Last resort — find closest matches with very relaxed criteria
                matched = self.doctrines[:3]
            deep_result = await self.deep_analysis_layer(request.query, matched, zone)

        # ── Build response ──

        # Doctrine results (TIE-3)
        doctrine_results: List[DoctrineResult] = []
        for d in matched:
            citations = build_authority_citations(d)
            doctrine_results.append(DoctrineResult(
                topic=d.topic,
                confidence=d.confidence,
                confidence_zone=stratify_confidence(d.confidence),
                reasoning_summary=d.reasoning_framework[:500],
                key_factors=d.key_factors[:8],
                authorities=citations,
                adversary_position=d.adversary_position,
                counter_arguments=d.counter_arguments[:5],
                resolution_strategy=d.resolution_strategy,
                burden_holder=d.burden_holder,
            ))

        # Violation assessments
        violation_assessments: List[ViolationAssessment] = []
        if request.include_penalty_estimate:
            for d in matched[:5]:
                severity = _estimate_severity(d)
                assessment = assess_violation(d, severity=severity)
                violation_assessments.append(assessment)

        # Authority hardening (TIE-4)
        all_authorities: List[AuthorityCitation] = []
        for dr in doctrine_results:
            all_authorities.extend(dr.authorities)
        # Deduplicate and sort by weight
        seen: Set[str] = set()
        primary_authorities: List[AuthorityCitation] = []
        for a in sorted(all_authorities, key=lambda x: x.weight, reverse=True):
            if a.authority not in seen:
                seen.add(a.authority)
                primary_authorities.append(a)

        # Confidence (TIE-5)
        confidence_scores = [d.confidence for d in matched]
        aggregate_confidence = compute_aggregate_confidence(confidence_scores)
        confidence_zone = stratify_confidence(aggregate_confidence)

        # Multi-doctrine decomposition (TIE-19)
        decomposition = decompose_violation_query(request.query, matched)

        # Fact fragility (TIE-14)
        fragility_scores: List[FactFragilityScore] = []
        for d in matched[:3]:
            fragility_scores.append(score_fact_fragility(
                claim=d.conclusion_template[:200],
                has_documentary_evidence=d.confidence >= 0.8,
                relies_on_testimony=d.confidence < 0.6,
                subject_to_recharacterization="ambig" in d.reasoning_framework.lower(),
                regulatory_ambiguity=d.confidence_stratification in ("DISCLOSURE", "HIGH_RISK"),
            ))

        # Build summary
        summary = _build_summary(matched, request.mode, zone, aggregate_confidence, violation_assessments)

        # Epistemic guardrails
        summary, warnings, disclosure = apply_epistemic_guardrails(summary, aggregate_confidence, zone)

        # Zone enforcement (TIE-13)
        summary = enforce_zone_separation(summary, zone)

        # Recommendation
        recommendation = _build_recommendation(matched, confidence_zone, zone, violation_assessments)

        # Determinism hash (TIE-16)
        det_hash = compute_determinism_hash(
            query=normalized,
            doctrines_triggered=[d.topic for d in matched],
            confidence=aggregate_confidence,
            zone=zone.value,
            mode=request.mode,
        )

        # Cloud knowledge tracking
        cloud_used = deep_result is not None and deep_result.get("resolved_authorities")
        cloud_sources = []
        if deep_result:
            cloud_sources = [a[0] for a in deep_result.get("resolved_authorities", [])[:5]]

        latency_ms = (time.time() - start) * 1000

        # Complete telemetry trace
        self.telemetry.end_trace(
            query_id=query_id,
            doctrines_triggered=[d.topic for d in matched],
            cache_hits=1 if layer_used == "DOCTRINE_CACHE" else 0,
            confidence=aggregate_confidence,
            violation_type=matched[0].topic if matched else None,
        )

        return QueryResponse(
            query_id=query_id,
            trace_id=trace_id,
            timestamp=datetime.utcnow().isoformat(),
            query_text=request.query,
            normalized_query=normalized,
            response_mode=request.mode,
            analysis_zone=zone.value,
            layer_used=layer_used,
            latency_ms=round(latency_ms, 2),
            violation_assessments=violation_assessments,
            doctrine_matches=doctrine_results,
            primary_authorities=primary_authorities[:10],
            confidence=round(aggregate_confidence, 4),
            confidence_zone=confidence_zone,
            fact_fragility_scores=fragility_scores,
            issue_categories=decomposition["issue_categories"],
            interaction_edges=decomposition["interaction_edges"],
            strata_analysis=decomposition["strata"],
            epistemic_warnings=warnings,
            disclosure_caveat=disclosure,
            cloud_knowledge_used=cloud_used,
            cloud_sources=cloud_sources,
            determinism_hash=det_hash,
            summary=summary,
            recommendation=recommendation,
        )


def _estimate_severity(doctrine: DoctrineBlock) -> str:
    """Estimate violation severity from doctrine confidence and category."""
    cat = doctrine.issue_category.value
    conf = doctrine.confidence

    if cat in ("well_control", "pollution", "safety"):
        return "severe" if conf > 0.8 else "serious"
    elif cat in ("environmental", "air_quality"):
        return "serious" if conf > 0.7 else "moderate"
    elif cat in ("operational", "spacing"):
        return "moderate" if conf > 0.6 else "minor"
    elif cat in ("reporting", "administrative", "financial"):
        return "minor" if conf > 0.7 else "moderate"
    elif cat == "enforcement":
        return "severe"
    else:
        return "moderate"


def _build_summary(
    matched: List[DoctrineBlock],
    mode: str,
    zone: AnalysisZone,
    confidence: float,
    assessments: List[ViolationAssessment],
) -> str:
    """Build mode-appropriate summary text."""
    if not matched:
        return "No matching regulatory violations identified for the given query."

    primary = matched[0]
    conf_zone = stratify_confidence(confidence)

    if mode == "FAST":
        # 2-5 sentences
        total_penalty = sum(a.penalty_range_max for a in assessments) if assessments else 0
        return (
            f"Violation type: {primary.topic.replace('_', ' ').title()}. "
            f"Primary authority: {primary.primary_authority[0] if primary.primary_authority else 'N/A'}. "
            f"Confidence: {confidence:.0%} ({conf_zone}). "
            f"Estimated maximum penalty exposure: ${total_penalty:,.0f}. "
            f"{primary.conclusion_template[:200]}"
        )

    elif mode == "DEFENSE":
        # Audit-ready with citations
        lines = [
            f"VIOLATION ANALYSIS — {primary.topic.replace('_', ' ').title()}",
            f"Confidence: {confidence:.0%} ({conf_zone})",
            "",
            "AUTHORITIES:",
        ]
        for auth in primary.primary_authority[:5]:
            level, weight = classify_authority(auth)
            lines.append(f"  [{level.value} W:{weight}] {auth}")
        lines.append("")
        lines.append(f"FINDING: {primary.conclusion_template}")
        lines.append("")
        lines.append(f"ADVERSE POSITION: {primary.adversary_position}")
        lines.append("")
        lines.append("COUNTER-ARGUMENTS:")
        for ca in primary.counter_arguments[:5]:
            lines.append(f"  - {ca}")
        lines.append("")
        lines.append(f"RESOLUTION: {primary.resolution_strategy}")
        lines.append("")
        if assessments:
            lines.append(f"PENALTY RANGE: ${assessments[0].penalty_range_min:,.0f} - ${assessments[0].penalty_range_max:,.0f}")
        lines.append(f"BURDEN: {primary.burden_holder}")
        return "\n".join(lines)

    else:  # MEMO
        # Full memorandum
        lines = [
            "═" * 60,
            f"REGULATORY VIOLATION MEMORANDUM",
            f"Engine: {ENGINE_ID} {ENGINE_NAME} v{ENGINE_VERSION}",
            f"Date: {datetime.utcnow().strftime('%Y-%m-%d')}",
            "═" * 60,
            "",
            "I. ISSUE IDENTIFICATION",
            f"   {primary.topic.replace('_', ' ').title()}",
            f"   Category: {primary.issue_category.value}",
            f"   Confidence: {confidence:.0%} ({conf_zone})",
            "",
            "II. APPLICABLE RULES",
        ]
        for auth in primary.primary_authority:
            lines.append(f"   - {auth}")
        lines.append("")
        lines.append("III. ANALYSIS")
        lines.append(f"   {primary.reasoning_framework[:600]}")
        lines.append("")
        lines.append("IV. KEY FACTORS")
        for kf in primary.key_factors:
            lines.append(f"   - {kf}")
        lines.append("")
        lines.append("V. ADVERSE POSITIONS")
        lines.append(f"   {primary.adversary_position}")
        for ca in primary.counter_arguments:
            lines.append(f"   Counter: {ca}")
        lines.append("")
        lines.append("VI. PENALTY ASSESSMENT")
        if assessments:
            a = assessments[0]
            lines.append(f"   Severity: {a.severity}")
            lines.append(f"   Range: ${a.penalty_range_min:,.0f} - ${a.penalty_range_max:,.0f}")
            lines.append(f"   Enforcement: {', '.join(a.enforcement_actions)}")
        lines.append("")
        lines.append("VII. CONCLUSION")
        lines.append(f"   {primary.conclusion_template}")
        lines.append("")
        lines.append("VIII. RECOMMENDATION")
        lines.append(f"   {primary.resolution_strategy}")
        lines.append("")
        lines.append(f"   Burden of proof: {primary.burden_holder}")
        lines.append(f"   Controlling precedent: {primary.controlling_precedent}")
        lines.append("═" * 60)
        return "\n".join(lines)


def _build_recommendation(
    matched: List[DoctrineBlock],
    conf_zone: str,
    zone: AnalysisZone,
    assessments: List[ViolationAssessment],
) -> str:
    """Build actionable recommendation based on analysis."""
    if not matched:
        return "Insufficient information to make a regulatory recommendation."

    primary = matched[0]

    if conf_zone == "DEFENSIBLE":
        base = f"The violation finding for {primary.topic.replace('_', ' ')} is well-supported. "
        if zone == AnalysisZone.PLANNING:
            return base + "Recommend immediate corrective action to minimize penalty exposure."
        elif zone == AnalysisZone.AUDIT:
            return base + "Document the finding with supporting evidence for the compliance record."
        else:
            return base + primary.resolution_strategy
    elif conf_zone == "AGGRESSIVE":
        return (
            f"The violation finding is supportable but carries litigation risk. "
            f"Consider settlement negotiations or voluntary compliance before formal enforcement. "
            f"{primary.resolution_strategy}"
        )
    elif conf_zone == "DISCLOSURE":
        return (
            f"DISCLOSURE REQUIRED: This assessment involves regulatory ambiguity. "
            f"Multiple reasonable interpretations exist. Engage regulatory counsel "
            f"before taking enforcement action or committing to a compliance position."
        )
    else:
        return (
            f"HIGH RISK: This analysis relies on novel regulatory interpretation. "
            f"Do NOT rely on this assessment without independent expert review. "
            f"The regulatory landscape is uncertain, and enforcement outcomes are unpredictable."
        )


# ═══════════════════════════════════════════════════════════════════════════════
# FASTAPI APPLICATION (TIE-17)
# ═══════════════════════════════════════════════════════════════════════════════

engine: Optional[ViolationDetectorEngine] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup/shutdown lifecycle."""
    global engine
    logger.info(f"Starting {ENGINE_ID} {ENGINE_NAME} v{ENGINE_VERSION} on port {ENGINE_PORT}")
    engine = ViolationDetectorEngine()
    logger.info(f"{ENGINE_ID} ready — {len(engine.doctrines)} doctrines, cloud={'YES' if engine.cloud else 'NO'}")
    yield
    logger.info(f"{ENGINE_ID} shutting down")


app = FastAPI(
    title=f"ECHO OMEGA PRIME — {ENGINE_ID} {ENGINE_NAME}",
    description="Regulatory violation detection, classification, and penalty assessment engine",
    version=ENGINE_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "http://localhost:*", "https://echo-op.com", "https://*.bmcii1976.workers.dev"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── POST /query ──────────────────────────────────────────────────────────

@app.post("/query", response_model=QueryResponse)
async def handle_query(request: QueryRequest):
    """Main violation detection query endpoint."""
    if engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")

    try:
        response = await engine.query(request)
        return response
    except Exception as e:
        logger.error(f"Query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ─── GET /health (TIE-12) ────────────────────────────────────────────────

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Comprehensive health check endpoint."""
    if engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")

    metrics = engine.telemetry.get_metrics_snapshot()
    coverage = engine.coverage_map.get_coverage_report()

    return HealthResponse(
        engine_id=ENGINE_ID,
        engine_name=ENGINE_NAME,
        version=ENGINE_VERSION,
        status="healthy",
        uptime_seconds=round(time.time() - engine.start_time, 1),
        doctrine_count=len(engine.doctrines),
        issue_categories=len(IssueCategory),
        interaction_edges=len(INTERACTION_EDGES),
        port=ENGINE_PORT,
        domain=ENGINE_DOMAIN,
        cloud_retriever_available=engine.cloud is not None,
        coverage_percentage=coverage["overall_coverage_pct"],
        total_queries=metrics.total_queries,
        error_rate=metrics.error_rate,
        avg_latency_ms=metrics.avg_latency_ms,
        epistemic_guardrails_active=True,
    )


# ─── GET /metrics (TIE-11) ───────────────────────────────────────────────

@app.get("/metrics", response_model=MetricsResponse)
async def get_metrics():
    """Engine performance metrics."""
    if engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")

    metrics = engine.telemetry.get_metrics_snapshot()
    coverage = engine.coverage_map.get_coverage_report()

    return MetricsResponse(
        engine_id=ENGINE_ID,
        timestamp=metrics.timestamp,
        total_queries=metrics.total_queries,
        avg_latency_ms=metrics.avg_latency_ms,
        p95_latency_ms=metrics.p95_latency_ms,
        p99_latency_ms=metrics.p99_latency_ms,
        error_rate=metrics.error_rate,
        cache_hit_rate=metrics.cache_hit_rate,
        queries_per_minute=metrics.queries_per_minute,
        top_violation_types=[{"type": t, "count": c} for t, c in metrics.top_violations],
        doctrine_coverage=coverage["overall_coverage_pct"],
        active_traces=len(engine.telemetry.active_traces),
    )


# ─── GET /drift ──────────────────────────────────────────────────────────

@app.get("/drift")
async def get_drift_report():
    """Doctrine drift analysis report."""
    if engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    return engine.drift_watcher.get_drift_report()


# ─── GET /coverage ────────────────────────────────────────────────────────

@app.get("/coverage")
async def get_coverage_report():
    """Doctrine coverage analysis."""
    if engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    return engine.coverage_map.get_coverage_report()


# ─── GET /doctrines ──────────────────────────────────────────────────────

@app.get("/doctrines")
async def list_doctrines(
    category: Optional[str] = Query(None, description="Filter by issue category"),
    limit: int = Query(50, ge=1, le=200),
):
    """List available doctrine blocks."""
    if engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")

    doctrines = engine.doctrines
    if category:
        doctrines = [d for d in doctrines if d.issue_category.value == category]

    return {
        "total": len(doctrines),
        "doctrines": [
            {
                "topic": d.topic,
                "category": d.issue_category.value,
                "confidence": d.confidence,
                "zone": d.confidence_stratification.value,
                "keywords": d.keywords[:5],
                "primary_authority": d.primary_authority[:3],
                "burden_holder": d.burden_holder,
            }
            for d in doctrines[:limit]
        ],
    }


# ─── GET /categories ─────────────────────────────────────────────────────

@app.get("/categories")
async def list_categories():
    """List violation issue categories."""
    return {
        "categories": [c.value for c in IssueCategory],
        "total": len(IssueCategory),
    }


# ─── POST /assess ────────────────────────────────────────────────────────

@app.post("/assess")
async def assess_specific_violation(
    violation_type: str,
    severity: str = "moderate",
    aggravating: List[str] = [],
    mitigating: List[str] = [],
):
    """Assess penalty for a specific violation type."""
    if engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")

    # Find matching doctrine
    norm_type = normalize_violation_type(violation_type)
    matching = [d for d in engine.doctrines if norm_type in d.topic.lower() or d.topic.lower() in norm_type]

    if not matching:
        raise HTTPException(status_code=404, detail=f"No doctrine found for violation type: {violation_type}")

    assessment = assess_violation(matching[0], severity, aggravating, mitigating)
    return assessment


# ─── GET /authorities ─────────────────────────────────────────────────────

@app.get("/authorities")
async def list_authority_hierarchy():
    """List the authority hierarchy with weights."""
    return {
        "hierarchy": [
            {"level": level.value, "weight": AUTHORITY_WEIGHTS[level.value], "description": _authority_description(level)}
            for level in AuthorityLevel
        ],
        "conflict_resolution": "Higher weight always controls. Equal weight resolved by specificity to the issue.",
    }


def _authority_description(level: AuthorityLevel) -> str:
    """Human-readable description for authority level."""
    descriptions = {
        "CONSTITUTIONAL": "US and Texas Constitutional provisions",
        "STATUTORY": "Federal and state statutes (Clean Water Act, TX Nat. Res. Code)",
        "REGULATORY": "Federal and state regulations (40 CFR, 16 TAC, 30 TAC)",
        "STATEWIDE_RULE": "RRC Statewide Rules 1-100",
        "AGENCY_ORDER": "Specific RRC/TCEQ enforcement orders",
        "CASE_LAW": "Court decisions interpreting regulations",
        "INDUSTRY_STANDARD": "API, ANSI, ASTM standards",
        "TECHNICAL_GUIDANCE": "Agency guidance documents and bulletins",
        "ADVISORY": "Policy letters, informal guidance, advisory opinions",
    }
    return descriptions.get(level.value, "")


# ─── GET /penalty-tiers ──────────────────────────────────────────────────

@app.get("/penalty-tiers")
async def get_penalty_tiers():
    """List penalty severity tiers with ranges."""
    return {
        "tiers": PENALTY_TIERS,
        "aggravating_multipliers": AGGRAVATING_MULTIPLIERS,
        "mitigating_multipliers": MITIGATING_MULTIPLIERS,
    }


# ─── GET /audit-trail (TIE-15) ──────────────────────────────────────────

@app.get("/audit-trail")
async def get_audit_trail(limit: int = Query(50, ge=1, le=500)):
    """Recent audit trail entries."""
    if engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")

    traces = engine.telemetry.get_recent_traces(limit=limit)
    return {
        "total": len(traces),
        "entries": [
            {
                "query_id": t.query_id,
                "query_text": t.query_text[:200],
                "response_mode": t.response_mode,
                "latency_ms": t.latency_ms,
                "doctrines_triggered": t.doctrines_triggered,
                "confidence": t.confidence,
                "violation_type": t.violation_type,
                "errors": t.errors,
            }
            for t in traces
        ],
    }


# ─── GET /guardrails ────────────────────────────────────────────────────

@app.get("/guardrails")
async def get_epistemic_guardrails():
    """List active epistemic guardrails."""
    return {
        "banned_phrases": BANNED_PHRASES,
        "confidence_thresholds": CONFIDENCE_THRESHOLDS,
        "zone_guidelines": ZONE_GUIDELINES,
        "guardrails_active": True,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# ENTRYPOINT
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    logger.info(f"Launching {ENGINE_ID} {ENGINE_NAME} v{ENGINE_VERSION} on port {ENGINE_PORT}")
    uvicorn.run(
        "engine:app",
        host="0.0.0.0",
        port=ENGINE_PORT,
        log_level="info",
        reload=False,
    )
