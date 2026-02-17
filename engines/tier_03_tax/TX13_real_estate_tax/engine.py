"""
TX13 REAL ESTATE TAX INTELLIGENCE ENGINE — Production Architecture
Professional-grade real estate tax doctrine system for CPAs, attorneys,
real estate investors, developers, and audit teams.

Architecture:
    Layer 1: Doctrine Cache (0-200ms) - Pre-compiled expert reasoning
    Layer 2: Semantic Retrieval (200-700ms) - Fast search on cache miss
    Layer 3: Deep Analysis (on-demand) - Multi-source synthesis

Response Modes:
    FAST: Doctrine-driven, minimal citations, sub-2 seconds
    DEFENSE: Structured reasoning, audit-ready, burden analysis
    MEMO: Long-form, citation-heavy, firm documentation

TIE-20 Components:
    1.  three_layer_response
    2.  response_modes (FAST, DEFENSE, MEMO)
    3.  doctrine_cache (25+ blocks)
    4.  authority_hardening
    5.  confidence_stratification
    6.  semantic_normalization
    7.  vector_search
    8.  telemetry
    9.  drift_watcher
    10. coverage_map
    11. metrics_collector
    12. health_endpoint
    13. zoned_analysis
    14. fact_fragility_scoring
    15. audit_trail_jsonl
    16. determinism_hash_sha256
    17. fastapi_server
    18. loguru_logging
    19. multi_doctrine_decomposition
    20. deep_analysis_mode

Author: ECHO OMEGA PRIME
Authority: 11.0 SOVEREIGN
Engine: TX13 Real Estate Tax
Port: 8463
Version: 1.0.0
"""

from __future__ import annotations

import hashlib
import json
import time
import uuid
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, ClassVar, Dict, List, Literal, Optional, Set, Tuple

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Local module imports
# ---------------------------------------------------------------------------
import sys
ENGINE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ENGINE_DIR))
sys.path.insert(0, str(ENGINE_DIR.parent / "_shared"))

from telemetry import (
    ErrorDomain,
    MutationOrigin,
    MutationType,
    ResponseLayer,
    complete_trace,
    get_telemetry,
    log_error,
    record_doctrine_mutation,
    trace_query,
)
from semantic import (
    NormalizationResult,
    compute_topic_relevance,
    detect_question_type,
    extract_keywords,
    normalize_semantics,
)
import sys

# Ensure sibling modules are importable
ENGINE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ENGINE_DIR))
from doctrines import (
    DOCTRINE_BLOCKS,
    DoctrineBlock,
    get_all_doctrines,
    get_doctrine,
    get_doctrine_stats,
    get_doctrine_topics,
    get_doctrines_by_confidence,
    get_doctrines_by_irc_section,
    search_doctrines_by_keyword,
)
from search import RealEstateSearchEngine, SearchContext, SearchResult

# ===========================================================================
# CONSTANTS
# ===========================================================================

ENGINE_ID: str = "TX13"
ENGINE_NAME: str = "Real Estate Tax Intelligence Engine"
ENGINE_VERSION: str = "1.0.0"
ENGINE_PORT: int = 8463
ENGINE_MODE: str = "EF"

LOG_DIR: Path = Path("O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/TX13_real_estate_tax/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
AUDIT_LOG: Path = LOG_DIR / "audit_trail.jsonl"

logger.add(
    LOG_DIR / "tx13_engine_{time}.log",
    rotation="50 MB",
    retention="30 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {module}:{function}:{line} | {message}",
)

# ===========================================================================
# BANNED PHRASES — Epistemic Guardrails
# ===========================================================================

BANNED_PHRASES: List[str] = [
    "you should always",
    "the irs always",
    "this is definitely",
    "there is no risk",
    "guaranteed to work",
    "the irs never",
    "absolutely no penalty",
    "100% safe",
    "no audit risk",
    "always deductible",
    "never taxable",
    "no chance of",
    "completely risk-free",
    "the law is clear that",
    "there is no question",
    "universally accepted",
    "beyond any doubt",
]


# ===========================================================================
# ENUMS
# ===========================================================================

class ResponseMode(str, Enum):
    """Response detail levels."""
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"


class ConfidenceLevel(str, Enum):
    """Confidence stratification tiers."""
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"


class PositionZone(str, Enum):
    """Zoned analysis — never blur the zones."""
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"


class IssueCategory(str, Enum):
    """Real estate tax issue categories for multi-doctrine decomposition."""
    EXCHANGE = "exchange"
    DEPRECIATION = "depreciation"
    PASSIVE_ACTIVITY = "passive_activity"
    QBI_DEDUCTION = "qbi_deduction"
    OPPORTUNITY_ZONE = "opportunity_zone"
    INSTALLMENT_SALE = "installment_sale"
    RECAPTURE = "recapture"
    RESIDENCE = "residence"
    REIT = "reit"
    CREDITS = "credits"
    INTEREST = "interest"
    CAPITALIZATION = "capitalization"
    PARTNERSHIP = "partnership"
    ENTITY_STRUCTURE = "entity_structure"
    COMPLIANCE = "compliance"


# ===========================================================================
# PYDANTIC MODELS — All I/O
# ===========================================================================

class QueryRequest(BaseModel):
    """Incoming query to the engine."""
    query: str = Field(..., min_length=3, max_length=5000)
    mode: ResponseMode = ResponseMode.FAST
    zone: PositionZone = PositionZone.PLANNING
    context: Optional[Dict[str, Any]] = None
    entity_type: Optional[str] = None
    property_type: Optional[str] = None
    include_deep_analysis: bool = False
    max_doctrines: int = Field(default=5, ge=1, le=20)


class AuthorityReference(BaseModel):
    """A legal authority citation."""
    citation: str
    weight: float = Field(default=1.0, ge=0.0, le=1.0)
    authority_type: str = "primary"
    description: str = ""


class DoctrineResult(BaseModel):
    """Result from a single doctrine block."""
    topic: str
    confidence: str
    confidence_stratification: str
    conclusion: str
    reasoning: str
    key_factors: List[str]
    authorities: List[AuthorityReference]
    burden_holder: str
    adversary_position: str
    counter_arguments: List[str]
    resolution_strategy: str
    irc_sections: List[str]
    related_doctrines: List[str]
    entity_scope: List[str]
    controlling_precedent: str
    match_score: float = 0.0


class FragilityScore(BaseModel):
    """Fact fragility assessment."""
    verifiability: float = Field(default=0.5, ge=0.0, le=1.0)
    recharacterization_risk: float = Field(default=0.3, ge=0.0, le=1.0)
    testimony_dependence: float = Field(default=0.3, ge=0.0, le=1.0)
    documentary_support: float = Field(default=0.5, ge=0.0, le=1.0)
    overall_fragility: float = Field(default=0.3, ge=0.0, le=1.0)
    assessment: str = ""


class DeepAnalysisResult(BaseModel):
    """Result from deep analysis mode."""
    synthesis: str
    multi_doctrine_interactions: List[Dict[str, Any]]
    risk_factors: List[str]
    planning_opportunities: List[str]
    compliance_requirements: List[str]
    recommended_actions: List[str]
    additional_research: List[str]


class CoverageGap(BaseModel):
    """An identified epistemic coverage gap."""
    topic: str
    description: str
    severity: str = "medium"
    suggested_research: str = ""


class QueryResponse(BaseModel):
    """Full response from the engine."""
    engine_id: str = ENGINE_ID
    engine_version: str = ENGINE_VERSION
    trace_id: str
    timestamp: str
    query: str
    normalized_query: str
    mode: str
    zone: str
    question_type: str
    layer_hit: str
    latency_ms: float
    doctrines: List[DoctrineResult]
    deep_analysis: Optional[DeepAnalysisResult] = None
    fragility: Optional[FragilityScore] = None
    coverage_gaps: List[CoverageGap] = Field(default_factory=list)
    issue_categories: List[str] = Field(default_factory=list)
    irc_sections_referenced: List[str] = Field(default_factory=list)
    disclosure_caveat: str = ""
    epistemic_guardrails_applied: bool = True
    determinism_hash: str = ""


class HealthResponse(BaseModel):
    """Health check response."""
    engine_id: str = ENGINE_ID
    engine_name: str = ENGINE_NAME
    engine_version: str = ENGINE_VERSION
    status: str = "healthy"
    port: int = ENGINE_PORT
    mode: str = ENGINE_MODE
    uptime_seconds: float = 0.0
    total_queries: int = 0
    total_errors: int = 0
    error_rate: float = 0.0
    doctrine_count: int = 0
    doctrine_hit_rate: float = 0.0
    avg_latency_ms: float = 0.0
    p95_latency_ms: float = 0.0
    search_index_built: bool = False
    coverage_map_topics: int = 0
    drift_mutations: int = 0
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ===========================================================================
# METRICS COLLECTOR (TIE Component 11)
# ===========================================================================

class MetricsCollector:
    """Lightweight metrics for operational awareness."""

    def __init__(self) -> None:
        self.latencies: List[float] = []
        self.errors: List[float] = []
        self.queries: List[float] = []
        self.doctrine_hits: int = 0
        self.doctrine_misses: int = 0
        self.last_error: Optional[str] = None
        self.active_queries: int = 0
        self._max_latencies: int = 200

    def record_query(self, latency_ms: float, doctrine_hit: bool) -> None:
        """Record a completed query."""
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
        """Record an error."""
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
            return {"avg_ms": 0.0, "p95_ms": 0.0, "last_ms": 0.0}
        sorted_lat = sorted(self.latencies)
        p95_idx = int(len(sorted_lat) * 0.95)
        return {
            "avg_ms": round(sum(self.latencies) / len(self.latencies), 2),
            "p95_ms": round(sorted_lat[min(p95_idx, len(sorted_lat) - 1)], 2),
            "last_ms": round(self.latencies[-1], 2),
        }

    def get_error_stats(self) -> Dict[str, Any]:
        now = time.time()
        last_hour = sum(1 for t in self.errors if t > now - 3600)
        return {"last_hour": last_hour, "last_24h": len(self.errors), "last_error": self.last_error}

    def get_doctrine_hit_rate(self) -> float:
        total = self.doctrine_hits + self.doctrine_misses
        if total == 0:
            return 0.0
        return round(self.doctrine_hits / total * 100.0, 2)


# ===========================================================================
# AUTHORITY HARDENING (TIE Component 4)
# ===========================================================================

AUTHORITY_WEIGHTS: Dict[str, float] = {
    "internal_revenue_code": 1.00,
    "treasury_regulation_final": 0.95,
    "treasury_regulation_proposed": 0.70,
    "treasury_regulation_temporary": 0.85,
    "revenue_ruling": 0.85,
    "revenue_procedure": 0.85,
    "supreme_court": 1.00,
    "circuit_court": 0.90,
    "tax_court_regular": 0.85,
    "tax_court_memo": 0.75,
    "district_court": 0.75,
    "court_of_claims": 0.80,
    "private_letter_ruling": 0.50,
    "technical_advice_memo": 0.55,
    "chief_counsel_advice": 0.60,
    "irs_notice": 0.75,
    "irs_announcement": 0.65,
    "irs_publication": 0.40,
    "irs_audit_technique_guide": 0.45,
    "legislative_history": 0.70,
    "joint_committee_report": 0.75,
    "secondary_source_treatise": 0.30,
    "secondary_source_article": 0.25,
}


def classify_authority(citation: str) -> Tuple[str, float]:
    """Classify an authority citation and return its type and weight."""
    cite_lower = citation.lower()

    if "irc" in cite_lower or "internal revenue code" in cite_lower or cite_lower.startswith("section"):
        return "internal_revenue_code", AUTHORITY_WEIGHTS["internal_revenue_code"]
    if "reg." in cite_lower or "regulation" in cite_lower:
        if "proposed" in cite_lower:
            return "treasury_regulation_proposed", AUTHORITY_WEIGHTS["treasury_regulation_proposed"]
        if "temporary" in cite_lower or "temp" in cite_lower:
            return "treasury_regulation_temporary", AUTHORITY_WEIGHTS["treasury_regulation_temporary"]
        return "treasury_regulation_final", AUTHORITY_WEIGHTS["treasury_regulation_final"]
    if "rev. rul." in cite_lower or "revenue ruling" in cite_lower:
        return "revenue_ruling", AUTHORITY_WEIGHTS["revenue_ruling"]
    if "rev. proc." in cite_lower or "revenue procedure" in cite_lower:
        return "revenue_procedure", AUTHORITY_WEIGHTS["revenue_procedure"]
    if "supreme court" in cite_lower or "u.s." in cite_lower:
        return "supreme_court", AUTHORITY_WEIGHTS["supreme_court"]
    if "cir." in cite_lower or "circuit" in cite_lower:
        return "circuit_court", AUTHORITY_WEIGHTS["circuit_court"]
    if "t.c." in cite_lower and "memo" not in cite_lower:
        return "tax_court_regular", AUTHORITY_WEIGHTS["tax_court_regular"]
    if "t.c. memo" in cite_lower or "tc memo" in cite_lower:
        return "tax_court_memo", AUTHORITY_WEIGHTS["tax_court_memo"]
    if "plr" in cite_lower or "private letter" in cite_lower:
        return "private_letter_ruling", AUTHORITY_WEIGHTS["private_letter_ruling"]
    if "notice" in cite_lower:
        return "irs_notice", AUTHORITY_WEIGHTS["irs_notice"]
    if "audit technique" in cite_lower or "atg" in cite_lower:
        return "irs_audit_technique_guide", AUTHORITY_WEIGHTS["irs_audit_technique_guide"]
    if "tcja" in cite_lower or "cares act" in cite_lower or "ira" in cite_lower:
        return "legislative_history", AUTHORITY_WEIGHTS["legislative_history"]

    return "secondary_source_treatise", AUTHORITY_WEIGHTS["secondary_source_treatise"]


def build_authority_chain(doctrine: DoctrineBlock) -> List[AuthorityReference]:
    """Build a weighted authority chain from a doctrine block."""
    authorities: List[AuthorityReference] = []
    for citation in doctrine.primary_authority:
        auth_type, weight = classify_authority(citation)
        authorities.append(AuthorityReference(
            citation=citation,
            weight=weight,
            authority_type=auth_type,
        ))
    authorities.sort(key=lambda a: a.weight, reverse=True)
    return authorities


def resolve_authority_conflicts(
    authorities_a: List[AuthorityReference],
    authorities_b: List[AuthorityReference],
) -> List[AuthorityReference]:
    """Resolve conflicts between two authority chains by weight."""
    combined = authorities_a + authorities_b
    seen: Set[str] = set()
    deduped: List[AuthorityReference] = []
    for auth in sorted(combined, key=lambda a: a.weight, reverse=True):
        if auth.citation not in seen:
            seen.add(auth.citation)
            deduped.append(auth)
    return deduped


# ===========================================================================
# CONFIDENCE STRATIFICATION (TIE Component 5)
# ===========================================================================

def stratify_confidence(
    doctrine: DoctrineBlock,
    authority_chain: List[AuthorityReference],
    question_type: str,
    zone: PositionZone,
) -> ConfidenceLevel:
    """
    Determine confidence stratification based on doctrine, authority,
    question type, and position zone.
    """
    base_confidence = doctrine.confidence_stratification

    if not authority_chain:
        return ConfidenceLevel.HIGH_RISK

    avg_weight = sum(a.weight for a in authority_chain) / len(authority_chain)

    if zone == PositionZone.AUDIT:
        if avg_weight < 0.7:
            return ConfidenceLevel.DISCLOSURE
        if base_confidence == "AGGRESSIVE":
            return ConfidenceLevel.DISCLOSURE

    if zone == PositionZone.REPORTING:
        if base_confidence == "HIGH_RISK":
            return ConfidenceLevel.DISCLOSURE

    if avg_weight >= 0.85 and base_confidence == "DEFENSIBLE":
        return ConfidenceLevel.DEFENSIBLE
    if avg_weight >= 0.70 and base_confidence in ("DEFENSIBLE", "AGGRESSIVE"):
        return ConfidenceLevel(base_confidence)

    if base_confidence == "AGGRESSIVE" and avg_weight < 0.60:
        return ConfidenceLevel.DISCLOSURE

    try:
        return ConfidenceLevel(base_confidence)
    except ValueError:
        return ConfidenceLevel.DISCLOSURE


# ===========================================================================
# FACT FRAGILITY SCORING (TIE Component 14)
# ===========================================================================

def score_fact_fragility(
    doctrine: DoctrineBlock,
    question_type: str,
    zone: PositionZone,
) -> FragilityScore:
    """
    Score the fragility of the factual basis underlying a position.
    Higher fragility = more vulnerable to IRS challenge.
    """
    verifiability = 0.7
    rechar_risk = 0.3
    testimony_dep = 0.2
    documentary = 0.7

    topic = doctrine.topic.lower()
    if "professional_status" in topic or "material_participation" in topic:
        testimony_dep = 0.8
        documentary = 0.3
        verifiability = 0.4
        rechar_risk = 0.5
    elif "dealer" in doctrine.adversary_position.lower():
        rechar_risk = 0.7
        verifiability = 0.5
    elif "cost_segregation" in topic:
        documentary = 0.8
        testimony_dep = 0.2
        verifiability = 0.7
    elif "opportunity_zone" in topic:
        documentary = 0.6
        rechar_risk = 0.4
    elif "installment" in topic:
        rechar_risk = 0.5
        documentary = 0.6
    elif "reit" in topic:
        documentary = 0.8
        verifiability = 0.8
    elif "lihtc" in topic:
        documentary = 0.7
        testimony_dep = 0.3

    if zone == PositionZone.AUDIT:
        rechar_risk *= 1.2
        testimony_dep *= 1.1

    if question_type == "risk_assessment":
        rechar_risk *= 1.1

    verifiability = min(verifiability, 1.0)
    rechar_risk = min(rechar_risk, 1.0)
    testimony_dep = min(testimony_dep, 1.0)
    documentary = min(documentary, 1.0)

    overall = round(
        0.25 * (1.0 - verifiability)
        + 0.30 * rechar_risk
        + 0.25 * testimony_dep
        + 0.20 * (1.0 - documentary),
        3,
    )

    if overall < 0.25:
        assessment = "Low fragility — position is well-supported by documentary evidence"
    elif overall < 0.45:
        assessment = "Moderate fragility — position has some fact-dependent elements"
    elif overall < 0.65:
        assessment = "Elevated fragility — position relies significantly on taxpayer testimony"
    else:
        assessment = "High fragility — position is highly dependent on subjective facts and vulnerable to challenge"

    return FragilityScore(
        verifiability=round(verifiability, 3),
        recharacterization_risk=round(rechar_risk, 3),
        testimony_dependence=round(testimony_dep, 3),
        documentary_support=round(documentary, 3),
        overall_fragility=overall,
        assessment=assessment,
    )


# ===========================================================================
# EPISTEMIC GUARDRAILS
# ===========================================================================

def apply_epistemic_guardrails(text: str) -> Tuple[str, bool]:
    """
    Screen text for banned absolute phrases. Return cleaned text
    and whether any guardrails were applied.
    """
    applied = False
    result = text
    for phrase in BANNED_PHRASES:
        if phrase.lower() in result.lower():
            result = result.replace(phrase, "[EPISTEMIC GUARDRAIL: absolute removed]")
            applied = True
    return result, applied


def generate_disclosure_caveat(
    confidence: ConfidenceLevel,
    zone: PositionZone,
    fragility: FragilityScore,
) -> str:
    """Generate appropriate disclosure caveat based on confidence and zone."""
    caveats: List[str] = []

    if confidence in (ConfidenceLevel.AGGRESSIVE, ConfidenceLevel.DISCLOSURE, ConfidenceLevel.HIGH_RISK):
        caveats.append(
            "This position involves tax authority that is not fully settled. "
            "The IRS may take a contrary position on audit."
        )

    if confidence == ConfidenceLevel.DISCLOSURE:
        caveats.append(
            "Disclosure on Form 8275 or 8275-R may be advisable to avoid "
            "accuracy-related penalties under IRC 6662."
        )

    if confidence == ConfidenceLevel.HIGH_RISK:
        caveats.append(
            "WARNING: This position carries significant audit risk and "
            "potential penalties. Substantial authority or reasonable basis "
            "may be difficult to establish."
        )

    if fragility.overall_fragility > 0.5:
        caveats.append(
            "The factual basis for this position has elevated fragility. "
            "Documentary evidence should be strengthened before relying on "
            "this analysis."
        )

    if zone == PositionZone.AUDIT:
        caveats.append(
            "AUDIT ZONE: This analysis is for audit defense purposes. "
            "All representations should be supported by contemporaneous "
            "documentation."
        )

    if not caveats:
        return "Standard analysis applies. No special disclosure requirements identified."

    return " ".join(caveats)


# ===========================================================================
# ZONED ANALYSIS (TIE Component 13)
# ===========================================================================

def apply_zone_framing(
    text: str,
    zone: PositionZone,
    confidence: ConfidenceLevel,
) -> str:
    """Frame analysis text according to the position zone."""
    if zone == PositionZone.PLANNING:
        prefix = "PLANNING ANALYSIS: "
        suffix = " This analysis is for tax planning purposes and assumes the described facts."
    elif zone == PositionZone.REPORTING:
        prefix = "REPORTING POSITION: "
        suffix = " This analysis supports the reported position on the tax return."
    elif zone == PositionZone.AUDIT:
        prefix = "AUDIT DEFENSE: "
        suffix = " This analysis is prepared for audit defense and should be reviewed by counsel."
    else:
        prefix = ""
        suffix = ""

    return f"{prefix}{text}{suffix}"


# ===========================================================================
# COVERAGE MAP (TIE Component 10)
# ===========================================================================

class CoverageMap:
    """Track which doctrines have been triggered and identify gaps."""

    def __init__(self) -> None:
        self._triggered: Dict[str, int] = {}
        self._missed: Dict[str, List[str]] = {}
        self._gap_reports: List[CoverageGap] = []

    def record_hit(self, topic: str) -> None:
        self._triggered[topic] = self._triggered.get(topic, 0) + 1

    def record_miss(self, query: str, searched_topics: List[str]) -> None:
        key = query[:100]
        self._missed[key] = searched_topics

    def detect_gaps(self, all_topics: List[str]) -> List[CoverageGap]:
        """Detect topics that have never been triggered."""
        never_triggered = [t for t in all_topics if t not in self._triggered]
        gaps: List[CoverageGap] = []
        for topic in never_triggered:
            gaps.append(CoverageGap(
                topic=topic,
                description=f"Doctrine '{topic}' has never been triggered by any query",
                severity="low",
                suggested_research=f"Review keyword coverage for {topic}",
            ))
        self._gap_reports = gaps
        return gaps

    def get_stats(self) -> Dict[str, Any]:
        return {
            "triggered_topics": len(self._triggered),
            "total_triggers": sum(self._triggered.values()),
            "missed_queries": len(self._missed),
            "top_topics": sorted(
                self._triggered.items(), key=lambda x: x[1], reverse=True
            )[:10],
        }


# ===========================================================================
# DRIFT WATCHER (TIE Component 9)
# ===========================================================================

class DriftWatcher:
    """Monitor doctrine stability and detect drift over time."""

    def __init__(self) -> None:
        self._baseline_hashes: Dict[str, str] = {}
        self._mutations: List[Dict[str, Any]] = []
        self._initialized: bool = False

    def initialize_baseline(self, doctrines: Dict[str, DoctrineBlock]) -> None:
        """Snapshot current doctrine state as baseline."""
        for topic, block in doctrines.items():
            content = (
                block.conclusion_template
                + block.reasoning_framework
                + str(block.key_factors)
                + str(block.primary_authority)
            )
            self._baseline_hashes[topic] = hashlib.sha256(content.encode()).hexdigest()
        self._initialized = True
        logger.info("DriftWatcher baseline initialized | topics={}", len(self._baseline_hashes))

    def check_drift(self, doctrines: Dict[str, DoctrineBlock]) -> List[Dict[str, Any]]:
        """Check for drift from baseline."""
        if not self._initialized:
            return []

        drifted: List[Dict[str, Any]] = []
        for topic, block in doctrines.items():
            content = (
                block.conclusion_template
                + block.reasoning_framework
                + str(block.key_factors)
                + str(block.primary_authority)
            )
            current_hash = hashlib.sha256(content.encode()).hexdigest()
            baseline = self._baseline_hashes.get(topic)

            if baseline and current_hash != baseline:
                drift_entry = {
                    "topic": topic,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "baseline_hash": baseline[:16],
                    "current_hash": current_hash[:16],
                }
                drifted.append(drift_entry)
                self._mutations.append(drift_entry)

        return drifted

    def get_mutation_count(self) -> int:
        return len(self._mutations)

    def get_mutations(self) -> List[Dict[str, Any]]:
        return list(self._mutations)


# ===========================================================================
# MULTI-DOCTRINE DECOMPOSITION (TIE Component 19)
# ===========================================================================

ISSUE_CATEGORY_MAP: Dict[str, List[IssueCategory]] = {
    "like_kind_exchange_1031": [IssueCategory.EXCHANGE, IssueCategory.RECAPTURE],
    "reverse_1031_exchange": [IssueCategory.EXCHANGE],
    "improvement_exchange_1031": [IssueCategory.EXCHANGE],
    "cost_segregation": [IssueCategory.DEPRECIATION, IssueCategory.RECAPTURE],
    "bonus_depreciation_168k": [IssueCategory.DEPRECIATION],
    "passive_activity_469": [IssueCategory.PASSIVE_ACTIVITY],
    "real_estate_professional_status": [IssueCategory.PASSIVE_ACTIVITY],
    "rental_loss_allowance_25k": [IssueCategory.PASSIVE_ACTIVITY],
    "section_199a_real_estate": [IssueCategory.QBI_DEDUCTION],
    "opportunity_zone_investment": [IssueCategory.OPPORTUNITY_ZONE],
    "installment_sale_453": [IssueCategory.INSTALLMENT_SALE, IssueCategory.RECAPTURE],
    "depreciation_recapture_1250": [IssueCategory.RECAPTURE, IssueCategory.DEPRECIATION],
    "primary_residence_121": [IssueCategory.RESIDENCE],
    "reit_taxation_856": [IssueCategory.REIT, IssueCategory.ENTITY_STRUCTURE],
    "lihtc_42": [IssueCategory.CREDITS],
    "section_179d_energy": [IssueCategory.CREDITS, IssueCategory.DEPRECIATION],
    "at_risk_real_estate_465": [IssueCategory.PASSIVE_ACTIVITY],
    "construction_interest_263a": [IssueCategory.CAPITALIZATION],
    "demolition_280b": [IssueCategory.CAPITALIZATION],
    "tenant_improvements_qip": [IssueCategory.DEPRECIATION],
    "ground_lease_taxation": [IssueCategory.ENTITY_STRUCTURE],
    "involuntary_conversion_1033": [IssueCategory.EXCHANGE],
    "historic_rehabilitation_credit_47": [IssueCategory.CREDITS],
    "business_interest_limitation_163j": [IssueCategory.INTEREST, IssueCategory.DEPRECIATION],
    "partnership_basis_754": [IssueCategory.PARTNERSHIP],
}

INTERACTION_EDGES: List[Tuple[str, str, str]] = [
    ("cost_segregation", "bonus_depreciation_168k", "Cost seg reclassifies components eligible for bonus depreciation"),
    ("cost_segregation", "depreciation_recapture_1250", "Reclassified 1245 property has full ordinary recapture"),
    ("like_kind_exchange_1031", "depreciation_recapture_1250", "Exchange defers recapture into replacement property basis"),
    ("passive_activity_469", "real_estate_professional_status", "RE professional exempts rental losses from PAL"),
    ("passive_activity_469", "rental_loss_allowance_25k", "$25K allowance is limited passive loss exception"),
    ("passive_activity_469", "at_risk_real_estate_465", "At-risk rules apply before passive activity rules"),
    ("section_199a_real_estate", "passive_activity_469", "QBI requires trade or business, interacts with PAL"),
    ("bonus_depreciation_168k", "business_interest_limitation_163j", "163(j) election eliminates bonus depreciation"),
    ("bonus_depreciation_168k", "tenant_improvements_qip", "QIP eligible for bonus depreciation at 15-year recovery"),
    ("installment_sale_453", "depreciation_recapture_1250", "1250 recapture accelerated in year of installment sale"),
    ("like_kind_exchange_1031", "opportunity_zone_investment", "Both are gain deferral strategies — choose one"),
    ("cost_segregation", "section_179d_energy", "Energy deduction complements cost seg for commercial properties"),
    ("partnership_basis_754", "like_kind_exchange_1031", "754 adjustment affects partner basis in exchanged property"),
    ("construction_interest_263a", "cost_segregation", "Capitalized interest becomes part of depreciable basis"),
    ("reit_taxation_856", "section_199a_real_estate", "REIT dividends eligible for 199A deduction"),
    ("primary_residence_121", "depreciation_recapture_1250", "Home office depreciation not excludable under 121"),
    ("lihtc_42", "passive_activity_469", "LIHTC credits subject to passive activity credit rules"),
    ("historic_rehabilitation_credit_47", "cost_segregation", "HTC and cost seg can be combined on same property"),
    ("demolition_280b", "construction_interest_263a", "Demolition costs capitalized before new construction begins"),
    ("involuntary_conversion_1033", "like_kind_exchange_1031", "Similar deferral mechanisms, different triggering events"),
    ("ground_lease_taxation", "tenant_improvements_qip", "Ground lease lessee improvements may qualify as QIP"),
    ("at_risk_real_estate_465", "partnership_basis_754", "Partner at-risk includes share of qualified nonrecourse debt"),
    ("business_interest_limitation_163j", "cost_segregation", "ADS requirement from 163(j) changes cost seg recovery periods"),
]


def identify_issue_categories(doctrines: List[str]) -> List[IssueCategory]:
    """Identify all issue categories touched by a set of doctrines."""
    categories: Set[IssueCategory] = set()
    for topic in doctrines:
        cats = ISSUE_CATEGORY_MAP.get(topic, [])
        categories.update(cats)
    return sorted(categories, key=lambda c: c.value)


def find_doctrine_interactions(doctrines: List[str]) -> List[Dict[str, str]]:
    """Find interaction edges between triggered doctrines."""
    interactions: List[Dict[str, str]] = []
    doc_set = set(doctrines)
    for source, target, description in INTERACTION_EDGES:
        if source in doc_set and target in doc_set:
            interactions.append({
                "source": source,
                "target": target,
                "interaction": description,
            })
        elif source in doc_set or target in doc_set:
            interactions.append({
                "source": source,
                "target": target,
                "interaction": description,
                "note": "One side triggered — consider related doctrine",
            })
    return interactions


# ===========================================================================
# DEEP ANALYSIS MODE (TIE Component 20)
# ===========================================================================

def perform_deep_analysis(
    query: str,
    doctrines: List[DoctrineResult],
    zone: PositionZone,
    question_type: str,
    entity_type: Optional[str] = None,
) -> DeepAnalysisResult:
    """
    Multi-source synthesis producing comprehensive analysis.
    Combines all matched doctrines into a unified assessment.
    """
    topics = [d.topic for d in doctrines]
    interactions = find_doctrine_interactions(topics)
    categories = identify_issue_categories(topics)

    synthesis_parts: List[str] = []
    risk_factors: List[str] = []
    planning_opps: List[str] = []
    compliance_reqs: List[str] = []
    actions: List[str] = []
    research: List[str] = []

    for doc in doctrines:
        synthesis_parts.append(
            f"[{doc.topic}] (Confidence: {doc.confidence}) — {doc.conclusion[:200]}"
        )

        if doc.confidence in ("AGGRESSIVE", "DISCLOSURE", "HIGH_RISK"):
            risk_factors.append(
                f"{doc.topic}: {doc.adversary_position[:150]}"
            )

        if zone == PositionZone.PLANNING:
            planning_opps.append(f"{doc.topic}: {doc.resolution_strategy[:150]}")

        for irc in doc.irc_sections:
            compliance_reqs.append(f"Compliance with IRC {irc} requirements")

        actions.append(f"Review {doc.topic} — {doc.resolution_strategy[:100]}")

    for interaction in interactions:
        synthesis_parts.append(
            f"INTERACTION: {interaction['source']} <-> {interaction['target']}: "
            f"{interaction['interaction']}"
        )

    for cat in categories:
        research.append(f"Review all {cat.value} implications for the transaction")

    if entity_type:
        research.append(f"Confirm entity-specific rules for {entity_type}")

    synthesis = "\n".join(synthesis_parts)
    compliance_reqs = list(set(compliance_reqs))

    return DeepAnalysisResult(
        synthesis=synthesis,
        multi_doctrine_interactions=interactions,
        risk_factors=risk_factors,
        planning_opportunities=planning_opps,
        compliance_requirements=compliance_reqs,
        recommended_actions=actions,
        additional_research=research,
    )


# ===========================================================================
# DETERMINISM HASH (TIE Component 16)
# ===========================================================================

def compute_determinism_hash(
    query: str,
    mode: str,
    zone: str,
    doctrines: List[DoctrineResult],
) -> str:
    """Compute SHA-256 determinism hash for reproducibility."""
    content = json.dumps({
        "query": query,
        "mode": mode,
        "zone": zone,
        "doctrines": [d.topic for d in doctrines],
        "engine_version": ENGINE_VERSION,
    }, sort_keys=True)
    return hashlib.sha256(content.encode()).hexdigest()


# ===========================================================================
# AUDIT TRAIL (TIE Component 15)
# ===========================================================================

def write_audit_trail(
    trace_id: str,
    query: str,
    mode: str,
    zone: str,
    doctrines: List[str],
    confidence: str,
    latency_ms: float,
    determinism_hash: str,
    client_ip: Optional[str] = None,
) -> None:
    """Write an append-only audit trail entry."""
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "engine_id": ENGINE_ID,
        "trace_id": trace_id,
        "query": query[:500],
        "mode": mode,
        "zone": zone,
        "doctrines_matched": doctrines,
        "confidence": confidence,
        "latency_ms": round(latency_ms, 2),
        "determinism_hash": determinism_hash,
        "client_ip": client_ip,
    }
    try:
        with open(AUDIT_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, default=str) + "\n")
    except OSError as e:
        logger.warning("Audit trail write failed | error={}", str(e))


# ===========================================================================
# THREE-LAYER RESPONSE ENGINE (TIE Component 1)
# ===========================================================================

class RealEstateTaxEngine:
    """
    The core TX13 Real Estate Tax Intelligence Engine.

    Three-layer architecture:
      Layer 1: Doctrine Cache — direct keyword match (0-200ms)
      Layer 2: Semantic Retrieval — TF-IDF search (200-700ms)
      Layer 3: Deep Analysis — multi-doctrine synthesis (on-demand)
    """

    def __init__(self) -> None:
        self._search_engine = RealEstateSearchEngine()
        self._metrics = MetricsCollector()
        self._coverage = CoverageMap()
        self._drift = DriftWatcher()
        self._start_time: float = time.time()
        self._initialized: bool = False
        logger.info("TX13 RealEstateTaxEngine initializing")

    def initialize(self) -> None:
        """Initialize the engine — index all doctrines for search."""
        doctrines = get_all_doctrines()

        for topic, block in doctrines.items():
            self._search_engine.index_doctrine(
                topic=topic,
                keywords=block.keywords,
                conclusion_template=block.conclusion_template,
                reasoning_framework=block.reasoning_framework,
                irc_sections=block.irc_sections,
                confidence_tier=block.confidence,
                additional_text=" ".join(block.key_factors),
            )

        self._search_engine.build_index()
        self._drift.initialize_baseline(doctrines)
        self._initialized = True
        logger.info(
            "TX13 Engine initialized | doctrines={} index_built=True",
            len(doctrines),
        )

    def process_query(self, request: QueryRequest) -> QueryResponse:
        """Process a query through the three-layer architecture."""
        start_time = time.time()
        self._metrics.query_start()
        trace_id = trace_query(request.query, request.mode.value)

        try:
            # Normalize
            norm = normalize_semantics(request.query)
            question_type = detect_question_type(request.query)

            # Layer 1: Doctrine Cache
            matched_doctrines = self._layer1_doctrine_cache(norm, request)

            layer_hit = ResponseLayer.DOCTRINE_CACHE
            if not matched_doctrines:
                # Layer 2: Semantic Retrieval
                matched_doctrines = self._layer2_semantic_retrieval(norm, request)
                layer_hit = ResponseLayer.SEMANTIC_RETRIEVAL

            if not matched_doctrines:
                self._coverage.record_miss(
                    request.query,
                    norm.detected_topics,
                )
                layer_hit = ResponseLayer.ERROR_FALLBACK

            # Build doctrine results
            doctrine_results: List[DoctrineResult] = []
            all_irc: Set[str] = set()
            top_confidence = ConfidenceLevel.DEFENSIBLE

            for topic, score in matched_doctrines[:request.max_doctrines]:
                block = get_doctrine(topic)
                if not block:
                    continue

                self._coverage.record_hit(topic)
                authorities = build_authority_chain(block)
                confidence = stratify_confidence(block, authorities, question_type, request.zone)

                if confidence.value in ("HIGH_RISK", "DISCLOSURE"):
                    top_confidence = confidence

                conclusion = block.conclusion_template
                reasoning = block.reasoning_framework

                if request.mode == ResponseMode.FAST:
                    reasoning = reasoning[:500] + "..." if len(reasoning) > 500 else reasoning
                elif request.mode == ResponseMode.MEMO:
                    conclusion = apply_zone_framing(conclusion, request.zone, confidence)

                conclusion, _ = apply_epistemic_guardrails(conclusion)
                reasoning, _ = apply_epistemic_guardrails(reasoning)

                all_irc.update(block.irc_sections)

                doctrine_results.append(DoctrineResult(
                    topic=topic,
                    confidence=confidence.value,
                    confidence_stratification=block.confidence_stratification,
                    conclusion=conclusion,
                    reasoning=reasoning,
                    key_factors=block.key_factors,
                    authorities=authorities,
                    burden_holder=block.burden_holder,
                    adversary_position=block.adversary_position,
                    counter_arguments=block.counter_arguments,
                    resolution_strategy=block.resolution_strategy,
                    irc_sections=block.irc_sections,
                    related_doctrines=block.related_doctrines,
                    entity_scope=block.entity_scope,
                    controlling_precedent=block.controlling_precedent,
                    match_score=score,
                ))

            # Fragility scoring
            fragility = None
            if doctrine_results:
                block = get_doctrine(doctrine_results[0].topic)
                if block:
                    fragility = score_fact_fragility(block, question_type, request.zone)

            # Deep analysis
            deep_analysis = None
            if request.include_deep_analysis and doctrine_results:
                deep_analysis = perform_deep_analysis(
                    request.query,
                    doctrine_results,
                    request.zone,
                    question_type,
                    request.entity_type,
                )

            # Issue categories
            doc_topics = [d.topic for d in doctrine_results]
            categories = identify_issue_categories(doc_topics)

            # Coverage gaps
            coverage_gaps = self._coverage.detect_gaps(get_doctrine_topics())

            # Disclosure caveat
            disclosure_caveat = ""
            if fragility and doctrine_results:
                disclosure_caveat = generate_disclosure_caveat(
                    top_confidence, request.zone, fragility
                )

            # Determinism hash
            det_hash = compute_determinism_hash(
                request.query, request.mode.value, request.zone.value, doctrine_results
            )

            latency_ms = (time.time() - start_time) * 1000.0
            doctrine_hit = layer_hit == ResponseLayer.DOCTRINE_CACHE
            self._metrics.record_query(latency_ms, doctrine_hit)

            # Complete telemetry trace
            complete_trace(
                trace_id=trace_id,
                layer_hit=layer_hit,
                doctrine_topic=doctrine_results[0].topic if doctrine_results else None,
                confidence=top_confidence.value,
                determinism_hash=det_hash,
                irc_sections=list(all_irc),
                authority_chain=[a.citation for d in doctrine_results for a in d.authorities[:2]],
            )

            # Audit trail
            write_audit_trail(
                trace_id=trace_id,
                query=request.query,
                mode=request.mode.value,
                zone=request.zone.value,
                doctrines=doc_topics,
                confidence=top_confidence.value,
                latency_ms=latency_ms,
                determinism_hash=det_hash,
            )

            self._metrics.query_end()

            return QueryResponse(
                trace_id=trace_id,
                timestamp=datetime.now(timezone.utc).isoformat(),
                query=request.query,
                normalized_query=norm.normalized[:500],
                mode=request.mode.value,
                zone=request.zone.value,
                question_type=question_type,
                layer_hit=layer_hit.value,
                latency_ms=round(latency_ms, 2),
                doctrines=doctrine_results,
                deep_analysis=deep_analysis,
                fragility=fragility,
                coverage_gaps=coverage_gaps[:5],
                issue_categories=[c.value for c in categories],
                irc_sections_referenced=sorted(all_irc),
                disclosure_caveat=disclosure_caveat,
                determinism_hash=det_hash,
            )

        except Exception as exc:
            latency_ms = (time.time() - start_time) * 1000.0
            self._metrics.record_error(str(exc))
            self._metrics.query_end()
            log_error(str(exc), ErrorDomain.UNKNOWN, trace_id)
            complete_trace(
                trace_id=trace_id,
                layer_hit=ResponseLayer.ERROR_FALLBACK,
                error=str(exc),
                error_domain=ErrorDomain.UNKNOWN,
            )
            logger.exception("Query processing failed | trace_id={}", trace_id)
            raise HTTPException(status_code=500, detail=f"Engine error: {str(exc)[:200]}")

    # -----------------------------------------------------------------------
    # Layer 1: Doctrine Cache
    # -----------------------------------------------------------------------

    def _layer1_doctrine_cache(
        self,
        norm: NormalizationResult,
        request: QueryRequest,
    ) -> List[Tuple[str, float]]:
        """Direct doctrine cache lookup via keyword matching."""
        matches: List[Tuple[str, float]] = []

        for detected_topic in norm.detected_topics:
            for topic, block in DOCTRINE_BLOCKS.items():
                if detected_topic.lower() in [kw.lower() for kw in block.keywords]:
                    relevance = compute_topic_relevance(request.query, block.keywords)
                    matches.append((topic, max(relevance, 0.8)))
                elif detected_topic.replace(" ", "_") == topic:
                    matches.append((topic, 0.95))

        for irc in norm.extracted_irc_sections:
            irc_doctrines = get_doctrines_by_irc_section(irc)
            for block in irc_doctrines:
                if block.topic not in [m[0] for m in matches]:
                    matches.append((block.topic, 0.7))

        query_keywords = extract_keywords(request.query)
        for topic, block in DOCTRINE_BLOCKS.items():
            if topic in [m[0] for m in matches]:
                continue
            relevance = compute_topic_relevance(request.query, block.keywords)
            if relevance >= 0.4:
                matches.append((topic, relevance))

        seen: Set[str] = set()
        deduped: List[Tuple[str, float]] = []
        for topic, score in sorted(matches, key=lambda x: x[1], reverse=True):
            if topic not in seen:
                seen.add(topic)
                deduped.append((topic, score))

        return deduped[:request.max_doctrines]

    # -----------------------------------------------------------------------
    # Layer 2: Semantic Retrieval
    # -----------------------------------------------------------------------

    def _layer2_semantic_retrieval(
        self,
        norm: NormalizationResult,
        request: QueryRequest,
    ) -> List[Tuple[str, float]]:
        """Semantic search fallback when Layer 1 misses."""
        context = SearchContext(
            query=request.query,
            normalized_query=norm.normalized,
            detected_topics=norm.detected_topics,
            extracted_irc=norm.extracted_irc_sections,
            property_types=norm.property_types,
            question_type=detect_question_type(request.query),
            max_results=request.max_doctrines,
            min_score=0.15,
        )

        results = self._search_engine.search(context)
        return [(r.doctrine_topic, r.score) for r in results]

    # -----------------------------------------------------------------------
    # Health & Metrics
    # -----------------------------------------------------------------------

    def get_health(self) -> HealthResponse:
        """Return comprehensive health check."""
        uptime = time.time() - self._start_time
        telemetry = get_telemetry()
        snap = telemetry.get_snapshot()
        latency_stats = self._metrics.get_latency_stats()

        return HealthResponse(
            status="healthy" if self._initialized else "initializing",
            uptime_seconds=round(uptime, 1),
            total_queries=snap.total_queries,
            total_errors=snap.total_errors,
            error_rate=snap.error_rate,
            doctrine_count=len(DOCTRINE_BLOCKS),
            doctrine_hit_rate=self._metrics.get_doctrine_hit_rate(),
            avg_latency_ms=latency_stats["avg_ms"],
            p95_latency_ms=latency_stats["p95_ms"],
            search_index_built=self._initialized,
            coverage_map_topics=len(self._coverage._triggered),
            drift_mutations=self._drift.get_mutation_count(),
        )

    def get_metrics(self) -> Dict[str, Any]:
        """Return operational metrics."""
        return {
            "latency": self._metrics.get_latency_stats(),
            "errors": self._metrics.get_error_stats(),
            "doctrine_hit_rate": self._metrics.get_doctrine_hit_rate(),
            "coverage": self._coverage.get_stats(),
            "drift_mutations": self._drift.get_mutation_count(),
            "search_index": self._search_engine.get_index_stats(),
        }


# ===========================================================================
# GLOBAL ENGINE INSTANCE
# ===========================================================================

_engine: Optional[RealEstateTaxEngine] = None


def get_engine() -> RealEstateTaxEngine:
    """Get or create the singleton engine instance."""
    global _engine
    if _engine is None:
        _engine = RealEstateTaxEngine()
        _engine.initialize()
    return _engine


# ===========================================================================
# FASTAPI APPLICATION (TIE Component 17)
# ===========================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan — initialize engine on startup."""
    logger.info("TX13 Real Estate Tax Engine starting | port={}", ENGINE_PORT)
    engine = get_engine()
    logger.info(
        "TX13 Engine ready | doctrines={} version={}",
        len(DOCTRINE_BLOCKS), ENGINE_VERSION,
    )
    yield
    logger.info("TX13 Engine shutting down")


app = FastAPI(
    title=ENGINE_NAME,
    version=ENGINE_VERSION,
    description=(
        "TX13 Real Estate Tax Intelligence Engine — Professional-grade "
        "real estate tax doctrine system covering IRC 1031, MACRS, passive "
        "activity, 199A, Opportunity Zones, installment sales, REITs, "
        "LIHTC, and 30+ additional domains."
    ),
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ===========================================================================
# API ENDPOINTS
# ===========================================================================

@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Comprehensive health check endpoint."""
    return get_engine().get_health()


@app.get("/")
async def root() -> Dict[str, Any]:
    """Root endpoint with engine info."""
    return {
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "engine_version": ENGINE_VERSION,
        "port": ENGINE_PORT,
        "mode": ENGINE_MODE,
        "doctrines": len(DOCTRINE_BLOCKS),
        "status": "operational",
        "endpoints": [
            "/health", "/query", "/doctrines", "/doctrines/{topic}",
            "/metrics", "/coverage", "/search", "/irc/{section}",
        ],
    }


@app.post("/query", response_model=QueryResponse)
async def query_engine(request: QueryRequest) -> QueryResponse:
    """
    Primary query endpoint.

    Processes a real estate tax question through the three-layer
    architecture and returns doctrine-backed analysis.
    """
    return get_engine().process_query(request)


@app.get("/doctrines")
async def list_doctrines() -> Dict[str, Any]:
    """List all doctrine topics with summary info."""
    stats = get_doctrine_stats()
    topics = []
    for topic, block in DOCTRINE_BLOCKS.items():
        topics.append({
            "topic": topic,
            "confidence": block.confidence,
            "irc_sections": block.irc_sections,
            "keyword_count": len(block.keywords),
            "authority_count": len(block.primary_authority),
            "controlling_precedent": block.controlling_precedent,
        })
    return {
        "engine_id": ENGINE_ID,
        "total_doctrines": stats["total_doctrines"],
        "by_confidence": stats["by_confidence"],
        "total_irc_sections": stats["total_irc_sections"],
        "doctrines": topics,
    }


@app.get("/doctrines/{topic}")
async def get_doctrine_detail(topic: str) -> Dict[str, Any]:
    """Get detailed information about a specific doctrine."""
    block = get_doctrine(topic)
    if not block:
        raise HTTPException(status_code=404, detail=f"Doctrine '{topic}' not found")

    authorities = build_authority_chain(block)
    categories = ISSUE_CATEGORY_MAP.get(topic, [])

    return {
        "topic": block.topic,
        "keywords": block.keywords,
        "conclusion_template": block.conclusion_template,
        "reasoning_framework": block.reasoning_framework,
        "key_factors": block.key_factors,
        "authorities": [a.model_dump() for a in authorities],
        "burden_holder": block.burden_holder,
        "adversary_position": block.adversary_position,
        "counter_arguments": block.counter_arguments,
        "resolution_strategy": block.resolution_strategy,
        "entity_scope": block.entity_scope,
        "confidence": block.confidence,
        "confidence_stratification": block.confidence_stratification,
        "controlling_precedent": block.controlling_precedent,
        "irc_sections": block.irc_sections,
        "related_doctrines": block.related_doctrines,
        "issue_categories": [c.value for c in categories],
        "effective_dates": block.effective_dates,
        "sunset_provision": block.sunset_provision,
    }


@app.get("/metrics")
async def get_metrics() -> Dict[str, Any]:
    """Return operational metrics."""
    return get_engine().get_metrics()


@app.get("/coverage")
async def get_coverage() -> Dict[str, Any]:
    """Return coverage map statistics."""
    engine = get_engine()
    stats = engine._coverage.get_stats()
    gaps = engine._coverage.detect_gaps(get_doctrine_topics())
    return {
        "stats": stats,
        "gaps": [{"topic": g.topic, "severity": g.severity} for g in gaps[:20]],
    }


@app.get("/search")
async def search_doctrines_endpoint(
    q: str,
    max_results: int = 5,
) -> Dict[str, Any]:
    """Search doctrines by keyword."""
    results = search_doctrines_by_keyword(q)
    return {
        "query": q,
        "results": [
            {
                "topic": r.topic,
                "confidence": r.confidence,
                "irc_sections": r.irc_sections,
                "keywords": r.keywords[:5],
            }
            for r in results[:max_results]
        ],
        "total_matches": len(results),
    }


@app.get("/irc/{section}")
async def get_by_irc_section(section: str) -> Dict[str, Any]:
    """Find doctrines covering a specific IRC section."""
    doctrines = get_doctrines_by_irc_section(section)
    return {
        "section": section,
        "doctrines": [
            {
                "topic": d.topic,
                "confidence": d.confidence,
                "controlling_precedent": d.controlling_precedent,
            }
            for d in doctrines
        ],
        "total": len(doctrines),
    }


@app.get("/telemetry")
async def get_telemetry_snapshot() -> Dict[str, Any]:
    """Return telemetry snapshot."""
    return get_telemetry().get_snapshot().model_dump()


@app.get("/drift")
async def get_drift_status() -> Dict[str, Any]:
    """Check for doctrine drift."""
    engine = get_engine()
    drifted = engine._drift.check_drift(get_all_doctrines())
    return {
        "total_mutations": engine._drift.get_mutation_count(),
        "current_drift": drifted,
        "baseline_topics": len(engine._drift._baseline_hashes),
    }


@app.get("/interactions")
async def get_doctrine_interactions() -> Dict[str, Any]:
    """Return all doctrine interaction edges."""
    return {
        "total_edges": len(INTERACTION_EDGES),
        "edges": [
            {"source": s, "target": t, "description": d}
            for s, t, d in INTERACTION_EDGES
        ],
    }


@app.get("/categories")
async def get_issue_categories() -> Dict[str, Any]:
    """Return issue category mappings."""
    return {
        "categories": [c.value for c in IssueCategory],
        "doctrine_mappings": {
            topic: [c.value for c in cats]
            for topic, cats in ISSUE_CATEGORY_MAP.items()
        },
    }


@app.post("/analyze/exchange")
async def analyze_exchange(request: QueryRequest) -> QueryResponse:
    """Specialized endpoint for 1031 exchange analysis."""
    request.query = f"1031 exchange analysis: {request.query}"
    request.include_deep_analysis = True
    return get_engine().process_query(request)


@app.post("/analyze/depreciation")
async def analyze_depreciation(request: QueryRequest) -> QueryResponse:
    """Specialized endpoint for depreciation strategy analysis."""
    request.query = f"depreciation strategy: {request.query}"
    request.include_deep_analysis = True
    return get_engine().process_query(request)


@app.post("/analyze/passive")
async def analyze_passive_activity(request: QueryRequest) -> QueryResponse:
    """Specialized endpoint for passive activity analysis."""
    request.query = f"passive activity rules: {request.query}"
    request.include_deep_analysis = True
    return get_engine().process_query(request)


@app.post("/analyze/opportunity-zone")
async def analyze_opportunity_zone(request: QueryRequest) -> QueryResponse:
    """Specialized endpoint for Opportunity Zone analysis."""
    request.query = f"opportunity zone: {request.query}"
    request.include_deep_analysis = True
    return get_engine().process_query(request)


@app.post("/analyze/reit")
async def analyze_reit(request: QueryRequest) -> QueryResponse:
    """Specialized endpoint for REIT compliance analysis."""
    request.query = f"REIT taxation: {request.query}"
    request.include_deep_analysis = True
    return get_engine().process_query(request)


@app.post("/analyze/installment")
async def analyze_installment_sale(request: QueryRequest) -> QueryResponse:
    """Specialized endpoint for installment sale analysis."""
    request.query = f"installment sale: {request.query}"
    request.include_deep_analysis = True
    return get_engine().process_query(request)


@app.post("/analyze/multi-doctrine")
async def analyze_multi_doctrine(request: QueryRequest) -> Dict[str, Any]:
    """
    Multi-doctrine decomposition endpoint.
    Accepts a complex real estate scenario and decomposes it into
    all applicable doctrine areas with interaction analysis.
    """
    engine = get_engine()
    response = engine.process_query(QueryRequest(
        query=request.query,
        mode=ResponseMode.DEFENSE,
        zone=request.zone,
        include_deep_analysis=True,
        max_doctrines=15,
        entity_type=request.entity_type,
        property_type=request.property_type,
    ))

    topics = [d.topic for d in response.doctrines]
    interactions = find_doctrine_interactions(topics)
    categories = identify_issue_categories(topics)

    interaction_dag: Dict[str, List[str]] = {}
    for source, target, desc in INTERACTION_EDGES:
        if source in topics:
            if source not in interaction_dag:
                interaction_dag[source] = []
            interaction_dag[source].append(target)

    strata: Dict[str, List[str]] = {}
    for cat in categories:
        strata[cat.value] = [
            t for t in topics
            if cat in ISSUE_CATEGORY_MAP.get(t, [])
        ]

    return {
        "engine_id": ENGINE_ID,
        "trace_id": response.trace_id,
        "query": request.query,
        "decomposition": {
            "total_doctrines_triggered": len(topics),
            "issue_categories": [c.value for c in categories],
            "category_strata": strata,
            "doctrine_interaction_dag": interaction_dag,
            "interaction_edges": interactions,
        },
        "doctrines": [
            {
                "topic": d.topic,
                "confidence": d.confidence,
                "irc_sections": d.irc_sections,
                "key_factors": d.key_factors[:3],
                "adversary_position": d.adversary_position[:200],
            }
            for d in response.doctrines
        ],
        "deep_analysis": response.deep_analysis.model_dump() if response.deep_analysis else None,
        "disclosure_caveat": response.disclosure_caveat,
        "determinism_hash": response.determinism_hash,
    }


@app.get("/audit-trail")
async def get_audit_trail(limit: int = 50) -> Dict[str, Any]:
    """Return recent audit trail entries."""
    entries: List[Dict[str, Any]] = []
    try:
        if AUDIT_LOG.exists():
            with open(AUDIT_LOG, "r", encoding="utf-8") as f:
                lines = f.readlines()
            for line in lines[-limit:]:
                try:
                    entries.append(json.loads(line.strip()))
                except json.JSONDecodeError:
                    continue
    except OSError as e:
        logger.warning("Failed to read audit trail | error={}", str(e))

    return {
        "engine_id": ENGINE_ID,
        "total_entries": len(entries),
        "entries": entries,
    }


@app.get("/fragility/{topic}")
async def get_fragility_for_topic(
    topic: str,
    zone: str = "PLANNING",
    question_type: str = "general",
) -> Dict[str, Any]:
    """Get fact fragility scoring for a specific doctrine topic."""
    block = get_doctrine(topic)
    if not block:
        raise HTTPException(status_code=404, detail=f"Doctrine '{topic}' not found")

    try:
        pos_zone = PositionZone(zone)
    except ValueError:
        pos_zone = PositionZone.PLANNING

    fragility = score_fact_fragility(block, question_type, pos_zone)
    return {
        "topic": topic,
        "zone": pos_zone.value,
        "question_type": question_type,
        "fragility": fragility.model_dump(),
    }


@app.post("/compare-strategies")
async def compare_strategies(
    scenario: str = "",
    strategies: List[str] = [],
) -> Dict[str, Any]:
    """
    Compare multiple tax strategies for a real estate scenario.
    Evaluates each strategy through the doctrine engine and provides
    a comparative analysis.
    """
    engine = get_engine()
    results: List[Dict[str, Any]] = []

    for strategy in strategies[:5]:
        query = f"{scenario} using strategy: {strategy}"
        response = engine.process_query(QueryRequest(
            query=query,
            mode=ResponseMode.DEFENSE,
            zone=PositionZone.PLANNING,
            include_deep_analysis=False,
            max_doctrines=5,
        ))

        top_confidence = "DEFENSIBLE"
        if response.doctrines:
            confidences = [d.confidence for d in response.doctrines]
            if "HIGH_RISK" in confidences:
                top_confidence = "HIGH_RISK"
            elif "DISCLOSURE" in confidences:
                top_confidence = "DISCLOSURE"
            elif "AGGRESSIVE" in confidences:
                top_confidence = "AGGRESSIVE"

        results.append({
            "strategy": strategy,
            "doctrines_triggered": [d.topic for d in response.doctrines],
            "overall_confidence": top_confidence,
            "irc_sections": response.irc_sections_referenced,
            "issue_categories": response.issue_categories,
            "key_risks": [
                d.adversary_position[:150]
                for d in response.doctrines
                if d.confidence in ("AGGRESSIVE", "DISCLOSURE", "HIGH_RISK")
            ],
            "disclosure_required": top_confidence in ("DISCLOSURE", "HIGH_RISK"),
        })

    return {
        "engine_id": ENGINE_ID,
        "scenario": scenario,
        "comparison": results,
        "recommendation": _select_best_strategy(results),
    }


def _select_best_strategy(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Select the best strategy from comparative analysis."""
    if not results:
        return {"strategy": "none", "reason": "No strategies provided"}

    confidence_rank = {"DEFENSIBLE": 4, "AGGRESSIVE": 3, "DISCLOSURE": 2, "HIGH_RISK": 1}
    best = max(
        results,
        key=lambda r: confidence_rank.get(r["overall_confidence"], 0),
    )
    return {
        "recommended_strategy": best["strategy"],
        "confidence": best["overall_confidence"],
        "reason": (
            f"Strategy '{best['strategy']}' has the highest confidence "
            f"level ({best['overall_confidence']}) with "
            f"{len(best['doctrines_triggered'])} supporting doctrines."
        ),
    }


# ===========================================================================
# RESPONSE FORMATTING UTILITIES
# ===========================================================================

class ResponseFormatter:
    """Format engine responses for different output modes."""

    @staticmethod
    def format_fast_response(response: QueryResponse) -> Dict[str, Any]:
        """Format a FAST mode response — concise, action-oriented."""
        primary = response.doctrines[0] if response.doctrines else None
        return {
            "answer": primary.conclusion[:300] if primary else "No matching doctrine found.",
            "confidence": primary.confidence if primary else "UNKNOWN",
            "irc_sections": response.irc_sections_referenced[:5],
            "key_action": primary.resolution_strategy[:200] if primary else "",
            "trace_id": response.trace_id,
        }

    @staticmethod
    def format_defense_response(response: QueryResponse) -> Dict[str, Any]:
        """Format a DEFENSE mode response — structured for audit defense."""
        sections: List[Dict[str, Any]] = []
        for doc in response.doctrines:
            sections.append({
                "issue": doc.topic.replace("_", " ").title(),
                "position": doc.conclusion,
                "authority": [a.citation for a in doc.authorities[:3]],
                "confidence": doc.confidence,
                "burden": doc.burden_holder,
                "irs_position": doc.adversary_position,
                "counter_arguments": doc.counter_arguments[:3],
                "resolution": doc.resolution_strategy,
            })

        return {
            "defense_brief": {
                "sections": sections,
                "disclosure_caveat": response.disclosure_caveat,
                "fragility": response.fragility.model_dump() if response.fragility else None,
            },
            "trace_id": response.trace_id,
            "determinism_hash": response.determinism_hash,
        }

    @staticmethod
    def format_memo_response(response: QueryResponse) -> Dict[str, Any]:
        """Format a MEMO mode response — full memorandum format."""
        memo_sections: List[Dict[str, Any]] = []

        memo_sections.append({
            "heading": "I. FACTS AND ISSUES",
            "content": (
                f"Query: {response.query}\n"
                f"Issue Categories: {', '.join(response.issue_categories)}\n"
                f"IRC Sections: {', '.join(response.irc_sections_referenced)}"
            ),
        })

        for i, doc in enumerate(response.doctrines, 1):
            memo_sections.append({
                "heading": f"II.{i}. {doc.topic.replace('_', ' ').upper()}",
                "content": doc.conclusion,
                "reasoning": doc.reasoning,
                "authority": [
                    f"{a.citation} (weight: {a.weight:.2f}, type: {a.authority_type})"
                    for a in doc.authorities
                ],
                "key_factors": doc.key_factors,
                "confidence": doc.confidence,
            })

        if response.deep_analysis:
            memo_sections.append({
                "heading": "III. MULTI-DOCTRINE INTERACTION ANALYSIS",
                "content": response.deep_analysis.synthesis,
                "risk_factors": response.deep_analysis.risk_factors,
                "planning_opportunities": response.deep_analysis.planning_opportunities,
            })

        memo_sections.append({
            "heading": "IV. CONCLUSION AND RECOMMENDATIONS",
            "content": response.disclosure_caveat,
            "actions": (
                response.deep_analysis.recommended_actions
                if response.deep_analysis else
                [d.resolution_strategy for d in response.doctrines[:3]]
            ),
        })

        return {
            "memorandum": {
                "title": f"TAX MEMORANDUM — {response.query[:100]}",
                "date": response.timestamp,
                "engine": f"{ENGINE_ID} v{ENGINE_VERSION}",
                "sections": memo_sections,
            },
            "trace_id": response.trace_id,
            "determinism_hash": response.determinism_hash,
        }


@app.post("/format/fast")
async def format_fast(request: QueryRequest) -> Dict[str, Any]:
    """Query with FAST response formatting."""
    request.mode = ResponseMode.FAST
    response = get_engine().process_query(request)
    return ResponseFormatter.format_fast_response(response)


@app.post("/format/defense")
async def format_defense(request: QueryRequest) -> Dict[str, Any]:
    """Query with DEFENSE brief formatting."""
    request.mode = ResponseMode.DEFENSE
    response = get_engine().process_query(request)
    return ResponseFormatter.format_defense_response(response)


@app.post("/format/memo")
async def format_memo(request: QueryRequest) -> Dict[str, Any]:
    """Query with MEMO memorandum formatting."""
    request.mode = ResponseMode.MEMO
    request.include_deep_analysis = True
    response = get_engine().process_query(request)
    return ResponseFormatter.format_memo_response(response)


# ===========================================================================
# DEPRECIATION CALCULATOR
# ===========================================================================

class DepreciationCalculator:
    """Real estate depreciation computation utilities."""

    MACRS_PERIODS: Dict[str, float] = {
        "residential_rental": 27.5,
        "commercial_nonresidential": 39.0,
        "qualified_improvement_property": 15.0,
        "land_improvement": 15.0,
        "personal_property_5yr": 5.0,
        "personal_property_7yr": 7.0,
    }

    ADS_PERIODS: Dict[str, float] = {
        "residential_rental": 30.0,
        "commercial_nonresidential": 40.0,
        "qualified_improvement_property": 20.0,
        "land_improvement": 20.0,
        "personal_property_5yr": 9.0,
        "personal_property_7yr": 12.0,
    }

    BONUS_SCHEDULE: Dict[int, float] = {
        2022: 1.00,
        2023: 0.80,
        2024: 0.60,
        2025: 0.40,
        2026: 0.20,
        2027: 0.00,
    }

    @classmethod
    def calculate_annual_depreciation(
        cls,
        cost_basis: float,
        property_type: str,
        use_ads: bool = False,
        placed_in_service_year: int = 2024,
        use_bonus: bool = True,
    ) -> Dict[str, Any]:
        """Calculate annual depreciation for a property."""
        if property_type not in cls.MACRS_PERIODS:
            return {"error": f"Unknown property type: {property_type}"}

        periods = cls.ADS_PERIODS if use_ads else cls.MACRS_PERIODS
        recovery_period = periods[property_type]

        bonus_pct = 0.0
        if use_bonus and not use_ads and property_type != "residential_rental" and property_type != "commercial_nonresidential":
            bonus_pct = cls.BONUS_SCHEDULE.get(placed_in_service_year, 0.0)

        bonus_deduction = cost_basis * bonus_pct
        remaining_basis = cost_basis - bonus_deduction
        annual_depreciation = remaining_basis / recovery_period if recovery_period > 0 else 0.0

        schedule: List[Dict[str, float]] = []
        for year in range(1, int(recovery_period) + 2):
            if year == 1:
                year_dep = bonus_deduction + (annual_depreciation * 0.5)
            elif year == int(recovery_period) + 1:
                year_dep = annual_depreciation * 0.5
            else:
                year_dep = annual_depreciation
            year_dep = min(year_dep, remaining_basis)
            remaining_basis_for_display = cost_basis - sum(s["depreciation"] for s in schedule) - year_dep
            schedule.append({
                "year": year,
                "depreciation": round(year_dep, 2),
                "cumulative": round(cost_basis - remaining_basis_for_display, 2),
            })
            if remaining_basis_for_display <= 0:
                break

        return {
            "cost_basis": cost_basis,
            "property_type": property_type,
            "recovery_period": recovery_period,
            "method": "ADS" if use_ads else "MACRS",
            "bonus_depreciation_pct": bonus_pct,
            "bonus_deduction_year1": round(bonus_deduction, 2),
            "annual_straight_line": round(annual_depreciation, 2),
            "total_depreciation": cost_basis,
            "schedule_preview": schedule[:5],
        }

    @classmethod
    def cost_segregation_estimate(
        cls,
        total_cost: float,
        property_type: str = "commercial_nonresidential",
        placed_in_service_year: int = 2024,
    ) -> Dict[str, Any]:
        """Estimate cost segregation benefit."""
        if property_type == "residential_rental":
            pct_5yr = 0.10
            pct_7yr = 0.05
            pct_15yr = 0.15
            pct_building = 0.60
            pct_land = 0.10
        else:
            pct_5yr = 0.15
            pct_7yr = 0.05
            pct_15yr = 0.15
            pct_building = 0.55
            pct_land = 0.10

        alloc_5yr = total_cost * pct_5yr
        alloc_7yr = total_cost * pct_7yr
        alloc_15yr = total_cost * pct_15yr
        alloc_building = total_cost * pct_building
        alloc_land = total_cost * pct_land

        bonus_pct = cls.BONUS_SCHEDULE.get(placed_in_service_year, 0.0)

        year1_with_seg = (
            alloc_5yr * bonus_pct
            + alloc_7yr * bonus_pct
            + alloc_15yr * bonus_pct
            + alloc_5yr * (1 - bonus_pct) / 5 * 0.5
            + alloc_7yr * (1 - bonus_pct) / 7 * 0.5
            + alloc_15yr * (1 - bonus_pct) / 15 * 0.5
            + alloc_building / (27.5 if property_type == "residential_rental" else 39.0) * 0.5
        )

        recovery = 27.5 if property_type == "residential_rental" else 39.0
        year1_without_seg = total_cost * (1 - pct_land) / recovery * 0.5

        benefit = year1_with_seg - year1_without_seg

        return {
            "total_cost": total_cost,
            "property_type": property_type,
            "bonus_depreciation_pct": bonus_pct,
            "allocation": {
                "5yr_personal_property": round(alloc_5yr, 2),
                "7yr_personal_property": round(alloc_7yr, 2),
                "15yr_land_improvements": round(alloc_15yr, 2),
                "building": round(alloc_building, 2),
                "land": round(alloc_land, 2),
            },
            "year1_depreciation_with_cost_seg": round(year1_with_seg, 2),
            "year1_depreciation_without_cost_seg": round(year1_without_seg, 2),
            "year1_benefit": round(benefit, 2),
            "estimated_tax_savings_year1_37pct": round(benefit * 0.37, 2),
            "note": (
                "Estimates based on typical cost segregation percentages. "
                "Actual results require engineering study."
            ),
        }


@app.post("/calculate/depreciation")
async def calculate_depreciation(
    cost_basis: float,
    property_type: str = "commercial_nonresidential",
    use_ads: bool = False,
    placed_in_service_year: int = 2024,
    use_bonus: bool = True,
) -> Dict[str, Any]:
    """Calculate depreciation schedule for a property."""
    return DepreciationCalculator.calculate_annual_depreciation(
        cost_basis, property_type, use_ads, placed_in_service_year, use_bonus
    )


@app.post("/calculate/cost-segregation")
async def calculate_cost_segregation(
    total_cost: float,
    property_type: str = "commercial_nonresidential",
    placed_in_service_year: int = 2024,
) -> Dict[str, Any]:
    """Estimate cost segregation benefit."""
    return DepreciationCalculator.cost_segregation_estimate(
        total_cost, property_type, placed_in_service_year
    )


# ===========================================================================
# 1031 EXCHANGE TIMELINE CALCULATOR
# ===========================================================================

class ExchangeTimelineCalculator:
    """Calculate critical dates for 1031 exchanges."""

    @staticmethod
    def calculate_dates(
        relinquished_close_date: str,
        tax_return_due_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Calculate 45-day identification and 180-day exchange deadlines."""
        try:
            close = datetime.strptime(relinquished_close_date, "%Y-%m-%d")
        except ValueError:
            return {"error": "Invalid date format. Use YYYY-MM-DD."}

        id_deadline = close + __import__("datetime").timedelta(days=45)
        exchange_deadline = close + __import__("datetime").timedelta(days=180)

        if tax_return_due_date:
            try:
                tax_due = datetime.strptime(tax_return_due_date, "%Y-%m-%d")
                if tax_due < exchange_deadline:
                    exchange_deadline = tax_due
                    exchange_note = "Exchange deadline limited by tax return due date"
                else:
                    exchange_note = "180-day rule applies (before tax return due date)"
            except ValueError:
                exchange_note = "Invalid tax return due date provided"
        else:
            exchange_note = "Verify tax return due date — may be earlier than 180 days"

        today = datetime.now()
        id_remaining = (id_deadline - today).days
        exchange_remaining = (exchange_deadline - today).days

        return {
            "relinquished_close_date": relinquished_close_date,
            "identification_deadline": id_deadline.strftime("%Y-%m-%d"),
            "identification_days_remaining": max(id_remaining, 0),
            "identification_expired": id_remaining < 0,
            "exchange_deadline": exchange_deadline.strftime("%Y-%m-%d"),
            "exchange_days_remaining": max(exchange_remaining, 0),
            "exchange_expired": exchange_remaining < 0,
            "exchange_note": exchange_note,
            "identification_rules": {
                "three_property_rule": "Identify up to 3 properties regardless of value",
                "two_hundred_percent_rule": "Identify any number, aggregate FMV <= 200% of relinquished",
                "ninety_five_percent_exception": "Identify any number if 95%+ of identified value is acquired",
            },
            "critical_reminders": [
                "Identification must be in writing, signed, and delivered to QI",
                "Identification cannot be revoked after 45-day deadline",
                "Replacement must be received by exchange deadline",
                "Use a qualified intermediary to avoid constructive receipt",
            ],
        }


@app.post("/calculate/exchange-timeline")
async def calculate_exchange_timeline(
    relinquished_close_date: str,
    tax_return_due_date: Optional[str] = None,
) -> Dict[str, Any]:
    """Calculate 1031 exchange timeline deadlines."""
    return ExchangeTimelineCalculator.calculate_dates(
        relinquished_close_date, tax_return_due_date
    )


# ===========================================================================
# INSTALLMENT SALE CALCULATOR
# ===========================================================================

class InstallmentCalculator:
    """Calculate installment sale gain recognition."""

    @staticmethod
    def calculate(
        selling_price: float,
        adjusted_basis: float,
        selling_expenses: float,
        mortgage_assumed: float,
        down_payment: float,
        annual_payment: float,
        depreciation_taken: float = 0.0,
    ) -> Dict[str, Any]:
        """Calculate installment sale gain recognition schedule."""
        realized_gain = selling_price - adjusted_basis - selling_expenses
        contract_price = selling_price - mortgage_assumed
        if contract_price <= 0:
            contract_price = realized_gain

        gross_profit_ratio = realized_gain / contract_price if contract_price > 0 else 0.0

        section_1250_recapture = min(depreciation_taken, realized_gain)

        year1_payment = down_payment
        year1_gain = year1_payment * gross_profit_ratio
        year1_total_gain = year1_gain + section_1250_recapture

        annual_gain = annual_payment * gross_profit_ratio

        total_payments = contract_price
        years_to_complete = (
            (total_payments - down_payment) / annual_payment
            if annual_payment > 0 else 0
        )

        return {
            "selling_price": selling_price,
            "adjusted_basis": adjusted_basis,
            "selling_expenses": selling_expenses,
            "mortgage_assumed": mortgage_assumed,
            "realized_gain": round(realized_gain, 2),
            "contract_price": round(contract_price, 2),
            "gross_profit_ratio": round(gross_profit_ratio, 4),
            "section_1250_recapture_year1": round(section_1250_recapture, 2),
            "year1": {
                "down_payment": down_payment,
                "installment_gain": round(year1_gain, 2),
                "section_1250_recapture": round(section_1250_recapture, 2),
                "total_recognized_gain": round(year1_total_gain, 2),
            },
            "subsequent_years": {
                "annual_payment": annual_payment,
                "gain_per_payment": round(annual_gain, 2),
                "return_of_basis_per_payment": round(annual_payment - annual_gain, 2),
            },
            "estimated_years_to_complete": round(years_to_complete, 1),
            "warnings": [
                "Section 1250 depreciation recapture is recognized in year 1 regardless of payment timing",
                "If installment obligations exceed $5M, IRC 453A interest charge may apply",
                "Related party dispositions within 2 years accelerate gain recognition",
            ],
        }


@app.post("/calculate/installment-sale")
async def calculate_installment_sale(
    selling_price: float,
    adjusted_basis: float,
    selling_expenses: float = 0.0,
    mortgage_assumed: float = 0.0,
    down_payment: float = 0.0,
    annual_payment: float = 0.0,
    depreciation_taken: float = 0.0,
) -> Dict[str, Any]:
    """Calculate installment sale gain recognition."""
    return InstallmentCalculator.calculate(
        selling_price, adjusted_basis, selling_expenses,
        mortgage_assumed, down_payment, annual_payment, depreciation_taken
    )


# ===========================================================================
# PASSIVE ACTIVITY HOUR TRACKER
# ===========================================================================

class PassiveActivityTracker:
    """Track hours for passive activity and RE professional status."""

    MATERIAL_PARTICIPATION_TESTS: Dict[str, str] = {
        "test_1_500_hours": (
            "The individual participates in the activity for more than 500 hours "
            "during the tax year."
        ),
        "test_2_substantially_all": (
            "The individual's participation constitutes substantially all of the "
            "participation in the activity for the tax year."
        ),
        "test_3_100_hours_no_other": (
            "The individual participates more than 100 hours and no other individual "
            "participates more hours."
        ),
        "test_4_significant_participation": (
            "The activity is a significant participation activity (100+ hours) and "
            "aggregate hours in all significant participation activities exceed 500."
        ),
        "test_5_5_of_10_years": (
            "The individual materially participated in the activity for any 5 of "
            "the 10 preceding tax years."
        ),
        "test_6_personal_service": (
            "The activity is a personal service activity and the individual "
            "materially participated in any 3 preceding tax years."
        ),
        "test_7_facts_and_circumstances": (
            "Based on all facts and circumstances, the individual participates on "
            "a regular, continuous, and substantial basis (minimum 100 hours)."
        ),
    }

    @classmethod
    def evaluate_re_professional(
        cls,
        real_property_hours: float,
        total_personal_service_hours: float,
        rental_hours_per_property: Dict[str, float],
        aggregation_election: bool = False,
    ) -> Dict[str, Any]:
        """Evaluate real estate professional status eligibility."""
        meets_750 = real_property_hours > 750
        meets_50_pct = (
            real_property_hours > total_personal_service_hours * 0.5
            if total_personal_service_hours > 0 else False
        )

        qualifies = meets_750 and meets_50_pct

        if aggregation_election:
            total_rental_hours = sum(rental_hours_per_property.values())
            material_participation = total_rental_hours > 500
        else:
            material_participation_per = {
                prop: hours > 500
                for prop, hours in rental_hours_per_property.items()
            }
            material_participation = all(material_participation_per.values()) if material_participation_per else False

        return {
            "re_professional_status": {
                "qualifies": qualifies,
                "750_hour_test": {
                    "met": meets_750,
                    "hours": real_property_hours,
                    "required": 750,
                },
                "50_percent_test": {
                    "met": meets_50_pct,
                    "real_property_hours": real_property_hours,
                    "total_hours": total_personal_service_hours,
                    "percentage": round(
                        real_property_hours / max(total_personal_service_hours, 1) * 100, 1
                    ),
                },
            },
            "material_participation": {
                "aggregation_election": aggregation_election,
                "meets_material_participation": material_participation,
                "per_property": rental_hours_per_property,
            },
            "result": (
                "QUALIFIES as RE Professional with material participation — rental losses are NON-PASSIVE"
                if qualifies and material_participation
                else "Does NOT qualify — rental losses remain PASSIVE"
            ),
            "recommendations": [
                "Maintain contemporaneous daily time logs" if not qualifies else "Status qualified — maintain records",
                "Consider aggregation election to simplify material participation" if not aggregation_election else "Aggregation election active",
                "Reduce W-2 hours if possible to meet 50% test" if not meets_50_pct else "50% test met",
            ],
        }


@app.post("/evaluate/re-professional")
async def evaluate_re_professional(
    real_property_hours: float,
    total_personal_service_hours: float,
    rental_hours_per_property: Dict[str, float] = {},
    aggregation_election: bool = False,
) -> Dict[str, Any]:
    """Evaluate real estate professional status eligibility."""
    return PassiveActivityTracker.evaluate_re_professional(
        real_property_hours, total_personal_service_hours,
        rental_hours_per_property, aggregation_election
    )


@app.get("/tests/material-participation")
async def list_material_participation_tests() -> Dict[str, Any]:
    """List all 7 material participation tests."""
    return {
        "tests": PassiveActivityTracker.MATERIAL_PARTICIPATION_TESTS,
        "note": "Taxpayer must meet at least ONE test to materially participate.",
    }


# ===========================================================================
# OPPORTUNITY ZONE TIMELINE
# ===========================================================================

@app.post("/calculate/oz-timeline")
async def calculate_oz_timeline(
    gain_date: str,
    gain_amount: float,
    investment_amount: Optional[float] = None,
) -> Dict[str, Any]:
    """Calculate Opportunity Zone investment timeline and benefits."""
    try:
        gain_dt = datetime.strptime(gain_date, "%Y-%m-%d")
    except ValueError:
        return {"error": "Invalid date format. Use YYYY-MM-DD."}

    invest_deadline = gain_dt + __import__("datetime").timedelta(days=180)
    invest_amount = investment_amount if investment_amount else gain_amount

    recognition_date = datetime(2026, 12, 31)

    hold_10yr = gain_dt + __import__("datetime").timedelta(days=3652)

    deferred_gain = min(invest_amount, gain_amount)
    non_deferred = max(gain_amount - invest_amount, 0)

    return {
        "gain_event_date": gain_date,
        "gain_amount": gain_amount,
        "investment_amount": invest_amount,
        "180_day_deadline": invest_deadline.strftime("%Y-%m-%d"),
        "gain_recognition_date": "2026-12-31",
        "10_year_hold_date": hold_10yr.strftime("%Y-%m-%d"),
        "deferred_gain": round(deferred_gain, 2),
        "non_deferred_gain": round(non_deferred, 2),
        "benefits": {
            "deferral": f"${deferred_gain:,.2f} deferred until 12/31/2026",
            "10yr_exclusion": (
                "If held 10+ years, ALL appreciation in QOF investment is permanently excluded"
            ),
        },
        "key_dates": [
            {"date": invest_deadline.strftime("%Y-%m-%d"), "event": "Investment deadline (180 days)"},
            {"date": "2026-12-31", "event": "Deferred gain recognition event"},
            {"date": hold_10yr.strftime("%Y-%m-%d"), "event": "10-year hold achieved — elect basis step-up"},
        ],
        "compliance": [
            "Invest in a Qualified Opportunity Fund (QOF)",
            "QOF must hold 90%+ in qualified OZ property",
            "File Form 8996 annually (QOF testing)",
            "Report deferral election on Form 8949",
        ],
    }


# ===========================================================================
# SECTION 199A QBI CALCULATOR
# ===========================================================================

@app.post("/calculate/qbi")
async def calculate_qbi_deduction(
    net_rental_income: float,
    w2_wages_paid: float = 0.0,
    ubia: float = 0.0,
    taxable_income: float = 0.0,
    filing_status: str = "mfj",
) -> Dict[str, Any]:
    """Calculate Section 199A QBI deduction for rental real estate."""
    threshold = 364200.0 if filing_status == "mfj" else 182100.0
    phase_in = 100000.0 if filing_status == "mfj" else 50000.0

    base_deduction = net_rental_income * 0.20

    if taxable_income <= threshold:
        deduction = base_deduction
        limitation_applied = "none"
    elif taxable_income <= threshold + phase_in:
        w2_limit = max(w2_wages_paid * 0.50, w2_wages_paid * 0.25 + ubia * 0.025)
        reduction_pct = (taxable_income - threshold) / phase_in
        reduced = base_deduction - (base_deduction - w2_limit) * reduction_pct
        deduction = max(reduced, 0)
        limitation_applied = "partial_phase_in"
    else:
        w2_limit = max(w2_wages_paid * 0.50, w2_wages_paid * 0.25 + ubia * 0.025)
        deduction = min(base_deduction, w2_limit)
        limitation_applied = "full_w2_ubia"

    deduction = min(deduction, taxable_income * 0.20)
    deduction = max(deduction, 0)

    return {
        "net_rental_income": net_rental_income,
        "base_qbi_deduction_20pct": round(base_deduction, 2),
        "w2_wages_paid": w2_wages_paid,
        "ubia": ubia,
        "taxable_income": taxable_income,
        "filing_status": filing_status,
        "threshold": threshold,
        "limitation_applied": limitation_applied,
        "final_deduction": round(deduction, 2),
        "tax_savings_estimate_24pct": round(deduction * 0.24, 2),
        "tax_savings_estimate_37pct": round(deduction * 0.37, 2),
        "requirements": [
            "Rental activity must be a trade or business (Section 162 or safe harbor)",
            "Rev. Proc. 2019-38 safe harbor: 250 hours of rental services",
            "Triple net leases excluded from safe harbor",
            "Maintain separate books and records",
        ],
    }


# ===========================================================================
# RECAPTURE CALCULATOR
# ===========================================================================

class RecaptureCalculator:
    """Calculate depreciation recapture on property disposition."""

    @staticmethod
    def calculate_1250_recapture(
        selling_price: float,
        adjusted_basis: float,
        total_depreciation_taken: float,
        selling_expenses: float = 0.0,
        has_section_1245_property: bool = False,
        section_1245_depreciation: float = 0.0,
    ) -> Dict[str, Any]:
        """Calculate Section 1250 and Section 1245 depreciation recapture."""
        realized_gain = selling_price - adjusted_basis - selling_expenses

        if realized_gain <= 0:
            return {
                "realized_gain": round(realized_gain, 2),
                "section_1250_recapture": 0.0,
                "unrecaptured_1250_gain": 0.0,
                "section_1245_recapture": 0.0,
                "remaining_capital_gain": 0.0,
                "note": "No gain to recapture — loss on disposition.",
            }

        section_1250_excess = 0.0

        unrecaptured_1250 = min(total_depreciation_taken, realized_gain)

        section_1245_recapture = 0.0
        if has_section_1245_property:
            section_1245_recapture = min(section_1245_depreciation, realized_gain)
            unrecaptured_1250 = min(
                total_depreciation_taken - section_1245_depreciation,
                max(realized_gain - section_1245_recapture, 0),
            )

        remaining_capital_gain = max(
            realized_gain - section_1250_excess - unrecaptured_1250 - section_1245_recapture,
            0,
        )

        tax_1245 = section_1245_recapture * 0.37
        tax_unrecaptured = unrecaptured_1250 * 0.25
        tax_capital = remaining_capital_gain * 0.20
        tax_niit = realized_gain * 0.038
        total_tax = tax_1245 + tax_unrecaptured + tax_capital + tax_niit

        effective_rate = total_tax / realized_gain if realized_gain > 0 else 0.0

        return {
            "selling_price": selling_price,
            "adjusted_basis": adjusted_basis,
            "selling_expenses": selling_expenses,
            "total_depreciation_taken": total_depreciation_taken,
            "realized_gain": round(realized_gain, 2),
            "gain_layers": {
                "section_1245_ordinary_recapture": {
                    "amount": round(section_1245_recapture, 2),
                    "rate": "37% (ordinary income)",
                    "tax": round(tax_1245, 2),
                },
                "unrecaptured_section_1250_gain": {
                    "amount": round(unrecaptured_1250, 2),
                    "rate": "25% (maximum rate)",
                    "tax": round(tax_unrecaptured, 2),
                },
                "remaining_long_term_capital_gain": {
                    "amount": round(remaining_capital_gain, 2),
                    "rate": "20% (maximum LTCG rate)",
                    "tax": round(tax_capital, 2),
                },
                "net_investment_income_tax": {
                    "amount": round(realized_gain, 2),
                    "rate": "3.8% (NIIT)",
                    "tax": round(tax_niit, 2),
                },
            },
            "total_estimated_tax": round(total_tax, 2),
            "effective_tax_rate": round(effective_rate * 100, 2),
            "deferral_options": [
                "IRC 1031 like-kind exchange — defer all gain including recapture",
                "IRC 1033 involuntary conversion — defer if qualifying event",
                "IRC 453 installment sale — defer capital gain (recapture in year 1)",
                "IRC 1400Z-2 Opportunity Zone — defer capital gain portion",
            ],
        }


@app.post("/calculate/recapture")
async def calculate_recapture(
    selling_price: float,
    adjusted_basis: float,
    total_depreciation_taken: float,
    selling_expenses: float = 0.0,
    has_section_1245_property: bool = False,
    section_1245_depreciation: float = 0.0,
) -> Dict[str, Any]:
    """Calculate depreciation recapture on property sale."""
    return RecaptureCalculator.calculate_1250_recapture(
        selling_price, adjusted_basis, total_depreciation_taken,
        selling_expenses, has_section_1245_property, section_1245_depreciation,
    )


# ===========================================================================
# ENTITY STRUCTURE ANALYZER
# ===========================================================================

class EntityStructureAnalyzer:
    """Analyze optimal entity structure for real estate holdings."""

    ENTITY_CHARACTERISTICS: Dict[str, Dict[str, Any]] = {
        "sole_proprietorship": {
            "liability_protection": False,
            "pass_through": True,
            "self_employment_tax": True,
            "section_199a": True,
            "1031_exchange": True,
            "basis_from_debt": False,
            "flexibility": "low",
            "complexity": "minimal",
            "best_for": "Single property, low risk, simplicity preferred",
        },
        "single_member_llc": {
            "liability_protection": True,
            "pass_through": True,
            "self_employment_tax": "depends on activity",
            "section_199a": True,
            "1031_exchange": True,
            "basis_from_debt": False,
            "flexibility": "high",
            "complexity": "low",
            "best_for": "Single property owner wanting liability protection",
        },
        "multi_member_llc_partnership": {
            "liability_protection": True,
            "pass_through": True,
            "self_employment_tax": "depends on member role",
            "section_199a": True,
            "1031_exchange": True,
            "basis_from_debt": True,
            "flexibility": "very high",
            "complexity": "moderate",
            "best_for": "Multiple investors, complex deal structures",
        },
        "s_corporation": {
            "liability_protection": True,
            "pass_through": True,
            "self_employment_tax": "salary only",
            "section_199a": True,
            "1031_exchange": True,
            "basis_from_debt": False,
            "flexibility": "moderate",
            "complexity": "moderate",
            "best_for": "Active businesses with payroll savings opportunity",
        },
        "c_corporation": {
            "liability_protection": True,
            "pass_through": False,
            "self_employment_tax": False,
            "section_199a": False,
            "1031_exchange": True,
            "basis_from_debt": False,
            "flexibility": "moderate",
            "complexity": "high",
            "best_for": "Rarely optimal for real estate due to double taxation",
        },
        "reit": {
            "liability_protection": True,
            "pass_through": True,
            "self_employment_tax": False,
            "section_199a": True,
            "1031_exchange": True,
            "basis_from_debt": False,
            "flexibility": "low",
            "complexity": "very high",
            "best_for": "Large portfolios, institutional investors, public markets",
        },
    }

    @classmethod
    def analyze(
        cls,
        num_properties: int,
        num_investors: int,
        anticipated_losses: bool,
        leveraged: bool,
        active_management: bool,
        annual_revenue: float,
    ) -> Dict[str, Any]:
        """Analyze and recommend entity structures for real estate."""
        recommendations: List[Dict[str, Any]] = []

        for entity, chars in cls.ENTITY_CHARACTERISTICS.items():
            score = 50

            if num_investors > 1:
                if entity in ("multi_member_llc_partnership",):
                    score += 25
                elif entity in ("sole_proprietorship", "single_member_llc"):
                    score -= 50

            if anticipated_losses:
                if chars.get("pass_through"):
                    score += 15
                if chars.get("basis_from_debt") and leveraged:
                    score += 20
                if entity == "c_corporation":
                    score -= 30

            if leveraged and entity == "multi_member_llc_partnership":
                score += 15

            if chars.get("liability_protection"):
                score += 10

            if entity == "c_corporation":
                score -= 20

            if entity == "reit" and (num_properties < 5 or annual_revenue < 1000000):
                score -= 40

            recommendations.append({
                "entity_type": entity,
                "score": max(score, 0),
                "characteristics": chars,
            })

        recommendations.sort(key=lambda r: r["score"], reverse=True)

        return {
            "scenario": {
                "num_properties": num_properties,
                "num_investors": num_investors,
                "anticipated_losses": anticipated_losses,
                "leveraged": leveraged,
                "active_management": active_management,
                "annual_revenue": annual_revenue,
            },
            "recommendations": recommendations[:3],
            "top_recommendation": recommendations[0]["entity_type"],
            "key_considerations": [
                "Partnership/LLC provides basis from debt (critical for leveraged real estate)",
                "S-Corp shareholders do NOT get basis from entity-level debt",
                "C-Corp double taxation makes it rarely optimal for real estate",
                "REIT only practical for large portfolios with 100+ shareholders",
                "Single-member LLC is a disregarded entity for tax (like sole proprietorship)",
                "Series LLC available in some states for multi-property isolation",
            ],
        }


@app.post("/analyze/entity-structure")
async def analyze_entity_structure(
    num_properties: int = 1,
    num_investors: int = 1,
    anticipated_losses: bool = True,
    leveraged: bool = True,
    active_management: bool = True,
    annual_revenue: float = 100000,
) -> Dict[str, Any]:
    """Analyze optimal entity structure for real estate holdings."""
    return EntityStructureAnalyzer.analyze(
        num_properties, num_investors, anticipated_losses,
        leveraged, active_management, annual_revenue,
    )


# ===========================================================================
# TAX PLANNING CHECKLIST GENERATOR
# ===========================================================================

ANNUAL_CHECKLIST: Dict[str, List[Dict[str, str]]] = {
    "Q1_January_March": [
        {"task": "Review prior year depreciation schedules", "irc": "168"},
        {"task": "Evaluate cost segregation for properties placed in service", "irc": "168"},
        {"task": "Assess bonus depreciation phase-down impact", "irc": "168(k)"},
        {"task": "Begin RE professional hour tracking (daily log)", "irc": "469(c)(7)"},
        {"task": "Review 163(j) election status and interest expense projections", "irc": "163(j)"},
        {"task": "Confirm REIT quarterly asset test compliance", "irc": "856"},
        {"task": "File Form 8996 for QOF annual certification", "irc": "1400Z-2"},
    ],
    "Q2_April_June": [
        {"task": "File extension if needed (preserve installment sale election)", "irc": "453"},
        {"task": "Mid-year RE professional hour check (375+ hours target)", "irc": "469(c)(7)"},
        {"task": "Review 199A safe harbor rental services (125+ hours target)", "irc": "199A"},
        {"task": "LIHTC compliance monitoring — income certifications", "irc": "42"},
        {"task": "Evaluate mid-year property acquisitions for 1031 exchanges", "irc": "1031"},
        {"task": "Review opportunity zone 90% asset test", "irc": "1400Z-2"},
    ],
    "Q3_July_September": [
        {"task": "Assess YTD passive activity income/loss by grouping", "irc": "469"},
        {"task": "Review at-risk amounts for leveraged properties", "irc": "465"},
        {"task": "Evaluate Section 179D energy deduction for new construction", "irc": "179D"},
        {"task": "Mid-year REIT income test projection", "irc": "856"},
        {"task": "Review QIP placed in service for bonus depreciation", "irc": "168(k)"},
        {"task": "Plan year-end property dispositions (recapture planning)", "irc": "1250"},
    ],
    "Q4_October_December": [
        {"task": "Final RE professional hour count (must exceed 750)", "irc": "469(c)(7)"},
        {"task": "Year-end 1031 exchange — verify 45/180 day deadlines", "irc": "1031"},
        {"task": "Maximize rental loss allowance (AGI management)", "irc": "469(i)"},
        {"task": "REIT year-end distribution (90% of taxable income)", "irc": "857"},
        {"task": "OZ gain recognition planning for 12/31/2026 event", "irc": "1400Z-2"},
        {"task": "Section 121 — verify ownership and use tests before sale", "irc": "121"},
        {"task": "Year-end entity structure review", "irc": "Multiple"},
        {"task": "199A W-2 wage and UBIA computation for QBI deduction", "irc": "199A"},
        {"task": "NIIT planning — manage AGI around $250K threshold", "irc": "1411"},
    ],
}


@app.get("/checklist/annual")
async def get_annual_checklist() -> Dict[str, Any]:
    """Get annual real estate tax planning checklist."""
    return {
        "engine_id": ENGINE_ID,
        "title": "Annual Real Estate Tax Planning Checklist",
        "quarters": ANNUAL_CHECKLIST,
        "total_items": sum(len(items) for items in ANNUAL_CHECKLIST.values()),
    }


@app.get("/checklist/{quarter}")
async def get_quarter_checklist(quarter: str) -> Dict[str, Any]:
    """Get checklist for a specific quarter."""
    matched = None
    for key, items in ANNUAL_CHECKLIST.items():
        if quarter.lower() in key.lower():
            matched = {"quarter": key, "items": items}
            break

    if not matched:
        raise HTTPException(
            status_code=404,
            detail=f"Quarter '{quarter}' not found. Use Q1, Q2, Q3, or Q4.",
        )
    return matched


# ===========================================================================
# SUNSET/EXPIRATION TRACKER
# ===========================================================================

TAX_PROVISION_EXPIRATIONS: List[Dict[str, Any]] = [
    {
        "provision": "Section 199A QBI Deduction",
        "irc_section": "199A",
        "expires": "2025-12-31",
        "impact": "20% deduction for pass-through rental income eliminated",
        "likelihood_of_extension": "moderate",
    },
    {
        "provision": "Bonus Depreciation (100%)",
        "irc_section": "168(k)",
        "expires": "Phase-down: 80%(2023), 60%(2024), 40%(2025), 20%(2026), 0%(2027)",
        "impact": "Reduced first-year depreciation for cost segregation components",
        "likelihood_of_extension": "possible",
    },
    {
        "provision": "Opportunity Zone 10-Year Exclusion",
        "irc_section": "1400Z-2",
        "expires": "Zone designations through 2028, deferral event 12/31/2026",
        "impact": "Must recognize deferred gains on 12/31/2026",
        "likelihood_of_extension": "uncertain",
    },
    {
        "provision": "Opportunity Zone 5-Year/7-Year Basis Step-Up",
        "irc_section": "1400Z-2(b)(2)(B)",
        "expires": "Already expired for most investments",
        "impact": "10%/15% basis step-up no longer available for new investments",
        "likelihood_of_extension": "unlikely",
    },
    {
        "provision": "Individual Tax Rate Reductions (TCJA)",
        "irc_section": "1",
        "expires": "2025-12-31",
        "impact": "Tax rates revert to pre-TCJA levels (potentially higher capital gains effective rate)",
        "likelihood_of_extension": "possible",
    },
    {
        "provision": "Higher Estate Tax Exemption",
        "irc_section": "2010",
        "expires": "2025-12-31",
        "impact": "$13.61M exemption halves — real estate estate planning urgency",
        "likelihood_of_extension": "uncertain",
    },
    {
        "provision": "Section 179D Energy Deduction (Enhanced IRA Amounts)",
        "irc_section": "179D",
        "expires": "Permanent (IRA made it permanent with enhanced amounts)",
        "impact": "No expiration — $5/sqft enhanced deduction continues",
        "likelihood_of_extension": "not needed (permanent)",
    },
    {
        "provision": "Section 45L Energy Efficient Home Credit",
        "irc_section": "45L",
        "expires": "2032-12-31 (IRA extension)",
        "impact": "Up to $5,000 credit per qualifying home",
        "likelihood_of_extension": "possible",
    },
]


@app.get("/expirations")
async def get_tax_expirations() -> Dict[str, Any]:
    """Get upcoming tax provision expirations affecting real estate."""
    return {
        "engine_id": ENGINE_ID,
        "provisions": TAX_PROVISION_EXPIRATIONS,
        "total": len(TAX_PROVISION_EXPIRATIONS),
        "critical_note": (
            "TCJA provisions (199A, bonus depreciation phase-down, rate reductions) "
            "are the most impactful real estate tax expirations. Planning should "
            "account for both extension and expiration scenarios."
        ),
    }


# ===========================================================================
# SECTION 121 EXCLUSION CALCULATOR
# ===========================================================================

class Section121Calculator:
    """Calculate primary residence gain exclusion under IRC 121."""

    @staticmethod
    def calculate(
        selling_price: float,
        original_cost: float,
        improvements: float,
        depreciation_claimed: float,
        selling_expenses: float,
        filing_status: str = "single",
        months_owned: int = 24,
        months_used_as_residence: int = 24,
        used_exclusion_within_2_years: bool = False,
    ) -> Dict[str, Any]:
        """Calculate Section 121 exclusion for primary residence sale."""
        adjusted_basis = original_cost + improvements - depreciation_claimed
        realized_gain = selling_price - adjusted_basis - selling_expenses

        max_exclusion = 500000.0 if filing_status == "mfj" else 250000.0

        ownership_met = months_owned >= 24
        use_met = months_used_as_residence >= 24
        prior_use_ok = not used_exclusion_within_2_years

        full_exclusion_available = ownership_met and use_met and prior_use_ok

        if full_exclusion_available:
            excludable_gain = min(max(realized_gain, 0), max_exclusion)
            non_excludable_depreciation = depreciation_claimed
            excludable_gain = max(excludable_gain - non_excludable_depreciation, 0)
        elif not prior_use_ok:
            excludable_gain = 0
            non_excludable_depreciation = depreciation_claimed
        else:
            qualifying_months = min(months_owned, months_used_as_residence)
            reduced_pct = qualifying_months / 24.0
            reduced_exclusion = max_exclusion * reduced_pct
            excludable_gain = min(max(realized_gain, 0), reduced_exclusion)
            non_excludable_depreciation = depreciation_claimed
            excludable_gain = max(excludable_gain - non_excludable_depreciation, 0)

        taxable_gain = max(realized_gain - excludable_gain, 0)
        depreciation_recapture = min(depreciation_claimed, taxable_gain)
        remaining_capital_gain = max(taxable_gain - depreciation_recapture, 0)

        tax_on_recapture = depreciation_recapture * 0.25
        tax_on_capital = remaining_capital_gain * 0.20
        tax_niit = taxable_gain * 0.038
        total_tax = tax_on_recapture + tax_on_capital + tax_niit

        return {
            "selling_price": selling_price,
            "adjusted_basis": round(adjusted_basis, 2),
            "realized_gain": round(realized_gain, 2),
            "section_121_analysis": {
                "max_exclusion": max_exclusion,
                "ownership_test_met": ownership_met,
                "use_test_met": use_met,
                "no_prior_exclusion_within_2yr": prior_use_ok,
                "full_exclusion_available": full_exclusion_available,
                "excludable_gain": round(excludable_gain, 2),
                "depreciation_not_excludable": round(non_excludable_depreciation, 2),
            },
            "taxable_gain": round(taxable_gain, 2),
            "tax_breakdown": {
                "depreciation_recapture_25pct": round(tax_on_recapture, 2),
                "capital_gain_20pct": round(tax_on_capital, 2),
                "niit_3_8pct": round(tax_niit, 2),
                "total_estimated_tax": round(total_tax, 2),
            },
            "planning_notes": [
                "Post-May 1997 home office depreciation is NOT excludable under Section 121",
                "If tests not fully met, reduced exclusion may be available for health, employment change, or unforeseen circumstances",
                "Married couples: both spouses must meet use test for $500K; only one needs ownership test",
                "Cannot use exclusion more than once every 2 years",
            ],
        }


@app.post("/calculate/section-121")
async def calculate_section_121(
    selling_price: float,
    original_cost: float,
    improvements: float = 0.0,
    depreciation_claimed: float = 0.0,
    selling_expenses: float = 0.0,
    filing_status: str = "single",
    months_owned: int = 24,
    months_used_as_residence: int = 24,
    used_exclusion_within_2_years: bool = False,
) -> Dict[str, Any]:
    """Calculate Section 121 primary residence exclusion."""
    return Section121Calculator.calculate(
        selling_price, original_cost, improvements, depreciation_claimed,
        selling_expenses, filing_status, months_owned,
        months_used_as_residence, used_exclusion_within_2_years,
    )


# ===========================================================================
# ENGINE SUMMARY / STATUS
# ===========================================================================

@app.get("/summary")
async def get_engine_summary() -> Dict[str, Any]:
    """Get a comprehensive engine summary for system status reporting."""
    engine = get_engine()
    health = engine.get_health()
    stats = get_doctrine_stats()

    return {
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "engine_version": ENGINE_VERSION,
        "port": ENGINE_PORT,
        "mode": ENGINE_MODE,
        "status": health.status,
        "uptime_seconds": health.uptime_seconds,
        "doctrine_library": {
            "total_doctrines": stats["total_doctrines"],
            "by_confidence": stats["by_confidence"],
            "irc_sections_covered": stats["total_irc_sections"],
        },
        "performance": {
            "total_queries": health.total_queries,
            "total_errors": health.total_errors,
            "error_rate": health.error_rate,
            "avg_latency_ms": health.avg_latency_ms,
            "p95_latency_ms": health.p95_latency_ms,
            "doctrine_hit_rate": health.doctrine_hit_rate,
        },
        "capabilities": {
            "three_layer_response": True,
            "response_modes": ["FAST", "DEFENSE", "MEMO"],
            "confidence_stratification": True,
            "authority_hardening": True,
            "fact_fragility_scoring": True,
            "multi_doctrine_decomposition": True,
            "deep_analysis_mode": True,
            "depreciation_calculator": True,
            "cost_segregation_estimator": True,
            "exchange_timeline_calculator": True,
            "installment_sale_calculator": True,
            "recapture_calculator": True,
            "entity_structure_analyzer": True,
            "re_professional_evaluator": True,
            "qbi_calculator": True,
            "section_121_calculator": True,
            "oz_timeline_calculator": True,
            "annual_planning_checklist": True,
            "expiration_tracker": True,
        },
        "tie_20_compliance": {
            "components_implemented": 20,
            "components_required": 20,
            "compliant": True,
        },
    }


# ===========================================================================
# ENTRY POINT
# ===========================================================================

if __name__ == "__main__":
    import uvicorn

    logger.info("Starting TX13 Real Estate Tax Engine on port {}", ENGINE_PORT)
    uvicorn.run(
        "engine:app",
        host="0.0.0.0",
        port=ENGINE_PORT,
        reload=False,
        log_level="info",
    )