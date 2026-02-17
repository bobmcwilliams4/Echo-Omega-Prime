"""
LM11 LEASE NEGOTIATION ENGINE — Production Architecture
TIE Gold Standard engine for oil and gas lease negotiation strategy and clause analysis.

Architecture:
    Layer 1: Doctrine Cache (0-200ms) - Pre-compiled expert reasoning on lease clauses
    Layer 2: Semantic Retrieval (200-700ms) - Fast search on cache miss
    Layer 3: Deep Analysis (on-demand) - Multi-source synthesis for complex scenarios

Response Modes:
    FAST: Doctrine-driven, minimal citations, sub-2 seconds
    DEFENSE: Structured reasoning, audit-ready, burden analysis
    MEMO: Long-form, citation-heavy, firm documentation

Domain Coverage:
    Royalty clauses, bonus negotiation, primary term, habendum, continuous drilling,
    Pugh clause, surface use, pooling/unitization, shut-in royalty, cessation of
    production, depth limitations, release provisions, assignment restrictions,
    environmental indemnification, audit rights, top lease strategy, lease amendments,
    mineral vs surface interests, market enhancement, lessor protections.

Author: ECHO OMEGA PRIME
Engine: LM11 Lease Negotiation
Port: 8511
Version: 1.0.0
"""

from __future__ import annotations

import hashlib
import json
import sys
import time
import traceback
import uuid
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, ClassVar, Dict, List, Literal, Optional

# Ensure _shared is on path for cloud_retriever
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_shared"))

# Ensure sibling modules are importable
ENGINE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ENGINE_DIR))

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import BaseModel, Field

# Local imports
from telemetry import (
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
from semantic import NormalizationResult, normalize_semantics, get_normalizer
from search import LeaseNegotiationSearchEngine, SearchResult, get_search_engine

from doctrines import DoctrineBlock, build_doctrine_cache

# Cloud knowledge integration
try:
    from cloud_retriever import CognitionCloudRetriever, CloudKnowledge, retrieve_cloud_knowledge
    _CLOUD_AVAILABLE = True
except ImportError:
    _CLOUD_AVAILABLE = False
    logger.warning("cloud_retriever not available — running without cloud knowledge")

# ==============================================================================
# CONSTANTS
# ==============================================================================

ENGINE_ID = "LM11"
ENGINE_NAME = "Lease Negotiation Engine"
ENGINE_VERSION = "1.0.0"
ENGINE_PORT = 8511
ENGINE_DOMAIN = "oil_gas_lease_negotiation"

LOG_DIR = Path("O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/LM11_lease_negotiation/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

AUDIT_LOG = LOG_DIR / "audit_trail.jsonl"

logger.add(
    LOG_DIR / "engine_{time}.log",
    rotation="50 MB",
    retention="30 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {message}",
)

# Banned phrases that indicate uncertainty masquerading as authority
BANNED_PHRASES: List[str] = [
    "it depends",
    "consult a lawyer",
    "this is not legal advice",
    "every situation is different",
    "you should seek professional advice",
    "results may vary",
    "this is general information only",
    "we cannot guarantee",
    "in my opinion",
    "i think",
    "i believe",
    "probably",
    "maybe",
    "might be",
    "could possibly",
]


# ==============================================================================
# ENUMS
# ==============================================================================

class ResponseMode(str, Enum):
    """Response detail level."""
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"


class AnalysisZone(str, Enum):
    """Position zone for analysis — never blur these boundaries."""
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"


class ConfidenceLevel(str, Enum):
    """Confidence stratification for conclusions."""
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"


class IssueCategory(str, Enum):
    """Lease negotiation issue categories for multi-doctrine decomposition."""
    ROYALTY = "royalty"
    BONUS = "bonus"
    TERM = "term"
    HABENDUM = "habendum"
    DRILLING_OBLIGATIONS = "drilling_obligations"
    PUGH = "pugh"
    SURFACE_USE = "surface_use"
    POOLING = "pooling"
    SHUT_IN = "shut_in"
    CESSATION = "cessation"
    DEPTH = "depth"
    RELEASE = "release"
    ASSIGNMENT = "assignment"
    ENVIRONMENTAL = "environmental"
    AUDIT_RIGHTS = "audit_rights"
    TOP_LEASE = "top_lease"
    AMENDMENT = "amendment"
    MINERAL_SURFACE = "mineral_surface"
    MARKET_ENHANCEMENT = "market_enhancement"
    WATER_RIGHTS = "water_rights"
    IMPLIED_COVENANTS = "implied_covenants"
    GENERAL = "general"


# ==============================================================================
# PYDANTIC MODELS
# ==============================================================================

class QueryRequest(BaseModel):
    """Inbound query request."""
    query: str = Field(..., min_length=3, max_length=5000, description="The lease negotiation question")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response detail level")
    zone: AnalysisZone = Field(default=AnalysisZone.PLANNING, description="Analysis zone")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")
    session_id: Optional[str] = Field(default=None, description="Session tracking ID")
    basin: Optional[str] = Field(default=None, description="Basin context override")
    party_role: Optional[str] = Field(default=None, description="Party role perspective")


class AuthorityReference(BaseModel):
    """A single authority citation."""
    source: str
    weight: float = Field(ge=0.0, le=1.0)
    jurisdiction: str = "Texas"
    year: Optional[int] = None


class DoctrineResult(BaseModel):
    """Result from doctrine cache lookup."""
    topic: str
    conclusion: str
    confidence: str
    confidence_stratification: str
    key_factors: List[str]
    authorities: List[str]
    burden_holder: str
    adversary_position: str
    counter_arguments: List[str]
    resolution_strategy: str
    entity_scope: str


class FragilityScore(BaseModel):
    """Fact fragility assessment."""
    verifiability: float = Field(ge=0.0, le=1.0, description="How verifiable is this conclusion")
    recharacterization_risk: float = Field(ge=0.0, le=1.0, description="Risk of adversary recharacterizing facts")
    testimony_dependence: float = Field(ge=0.0, le=1.0, description="Dependence on testimony vs documentary evidence")
    overall_fragility: float = Field(ge=0.0, le=1.0, description="Composite fragility score")
    assessment: str = ""


class QueryResponse(BaseModel):
    """Complete query response."""
    engine_id: str = ENGINE_ID
    engine_version: str = ENGINE_VERSION
    query: str
    response_mode: str
    analysis_zone: str
    conclusion: str
    reasoning: str
    confidence: str
    confidence_stratification: str
    key_factors: List[str]
    authorities: List[str]
    counter_arguments: List[str]
    resolution_strategy: str
    fragility: FragilityScore
    issue_categories: List[str]
    basin_context: Optional[str] = None
    party_role: Optional[str] = None
    doctrine_hit: bool = False
    doctrine_topic: Optional[str] = None
    response_layer: str = ""
    latency_ms: float = 0.0
    determinism_hash: str = ""
    trace_id: str = ""
    timestamp: str = ""
    # Cloud knowledge enrichment
    cloud_knowledge: Optional[Dict[str, Any]] = None
    cloud_citations: Optional[List[str]] = None
    disclosure_caveat: str = ""


class HealthResponse(BaseModel):
    """Health check response."""
    engine_id: str = ENGINE_ID
    engine_name: str = ENGINE_NAME
    version: str = ENGINE_VERSION
    status: str = "healthy"
    uptime_seconds: float = 0.0
    doctrine_count: int = 0
    search_index_size: int = 0
    total_queries: int = 0
    doctrine_hit_rate_pct: float = 0.0
    metrics: Dict[str, Any] = {}
    normalizer_stats: Dict[str, Any] = {}
    search_stats: Dict[str, Any] = {}
    timestamp: str = ""


# ==============================================================================
# METRICS COLLECTOR
# ==============================================================================

class MetricsCollector:
    """Lightweight operational metrics for the lease negotiation engine."""

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
        """Record an error event."""
        self.errors.append(time.time())
        self.last_error = f"{datetime.now(timezone.utc).isoformat()}: {error_msg[:200]}"
        cutoff = time.time() - 86400
        self.errors = [t for t in self.errors if t > cutoff]

    def get_stats(self) -> Dict[str, Any]:
        """Return current metrics."""
        total = self.doctrine_hits + self.doctrine_misses
        hit_rate = (self.doctrine_hits / total * 100) if total > 0 else 0.0
        avg_latency = (sum(self.latencies) / len(self.latencies)) if self.latencies else 0.0
        return {
            "total_queries": total,
            "doctrine_hits": self.doctrine_hits,
            "doctrine_misses": self.doctrine_misses,
            "hit_rate_pct": round(hit_rate, 2),
            "avg_latency_ms": round(avg_latency, 2),
            "queries_last_hour": len(self.queries),
            "errors_last_24h": len(self.errors),
            "last_error": self.last_error,
        }


# ==============================================================================
# DOCTRINE DRIFT WATCHER
# ==============================================================================

class DoctrineDriftWatcher:
    """Monitor doctrine cache for content drift over time."""

    def __init__(self) -> None:
        self._baseline_hashes: Dict[str, str] = {}
        self._drift_events: List[Dict[str, Any]] = []
        self._initialized: bool = False

    def initialize(self, cache: Dict[str, DoctrineBlock]) -> None:
        """Capture baseline hashes for all doctrine blocks."""
        for topic, block in cache.items():
            content = f"{block.conclusion_template}|{block.reasoning_framework}"
            self._baseline_hashes[topic] = hashlib.sha256(content.encode()).hexdigest()
        self._initialized = True
        logger.info(f"Drift watcher initialized with {len(self._baseline_hashes)} baselines")

    def check_drift(self, cache: Dict[str, DoctrineBlock]) -> List[Dict[str, Any]]:
        """Check current cache against baseline for drift."""
        if not self._initialized:
            return []
        drifted: List[Dict[str, Any]] = []
        for topic, block in cache.items():
            content = f"{block.conclusion_template}|{block.reasoning_framework}"
            current_hash = hashlib.sha256(content.encode()).hexdigest()
            baseline = self._baseline_hashes.get(topic)
            if baseline and current_hash != baseline:
                event = {
                    "topic": topic,
                    "baseline_hash": baseline[:12],
                    "current_hash": current_hash[:12],
                    "detected_at": datetime.now(timezone.utc).isoformat(),
                }
                drifted.append(event)
                self._drift_events.append(event)
        return drifted

    def get_drift_history(self) -> List[Dict[str, Any]]:
        """Return all drift events."""
        return list(self._drift_events)

    def get_stats(self) -> Dict[str, Any]:
        """Return drift watcher statistics."""
        return {
            "initialized": self._initialized,
            "baseline_count": len(self._baseline_hashes),
            "total_drift_events": len(self._drift_events),
        }


# ==============================================================================
# DOCTRINE COVERAGE MAP
# ==============================================================================

class DoctrineCoverageMap:
    """Track which doctrines are triggered and identify epistemic gaps."""

    def __init__(self) -> None:
        self._hits: Dict[str, int] = {}
        self._misses: List[str] = []
        self._total_queries: int = 0

    def record_hit(self, topic: str) -> None:
        """Record a doctrine cache hit."""
        self._hits[topic] = self._hits.get(topic, 0) + 1
        self._total_queries += 1

    def record_miss(self, query: str) -> None:
        """Record a doctrine cache miss with the query that missed."""
        self._misses.append(query[:200])
        if len(self._misses) > 200:
            self._misses = self._misses[-200:]
        self._total_queries += 1

    def get_coverage_report(self, total_doctrines: int) -> Dict[str, Any]:
        """Generate coverage report."""
        triggered = len(self._hits)
        coverage_pct = (triggered / total_doctrines * 100) if total_doctrines > 0 else 0.0
        sorted_hits = sorted(self._hits.items(), key=lambda x: x[1], reverse=True)
        return {
            "total_doctrines": total_doctrines,
            "triggered_doctrines": triggered,
            "untriggered_doctrines": total_doctrines - triggered,
            "coverage_pct": round(coverage_pct, 2),
            "total_queries": self._total_queries,
            "top_doctrines": sorted_hits[:10],
            "recent_misses": self._misses[-10:],
            "epistemic_gaps": self._identify_gaps(total_doctrines),
        }

    def _identify_gaps(self, total_doctrines: int) -> List[str]:
        """Identify potential epistemic gaps from miss patterns."""
        if len(self._misses) < 5:
            return []
        # Simple frequency analysis of miss keywords
        word_counts: Dict[str, int] = {}
        for miss in self._misses:
            for word in miss.lower().split():
                if len(word) > 3:
                    word_counts[word] = word_counts.get(word, 0) + 1
        sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
        return [w for w, c in sorted_words[:5] if c >= 3]


# ==============================================================================
# AUTHORITY HARDENING
# ==============================================================================

class AuthorityResolver:
    """Resolve and weight authority citations for lease negotiation conclusions."""

    AUTHORITY_WEIGHTS: ClassVar[Dict[str, float]] = {
        "texas_supreme_court": 1.0,
        "texas_appeals_court": 0.85,
        "fifth_circuit": 0.90,
        "texas_statute": 0.95,
        "rrc_rule": 0.80,
        "aapl_standard": 0.70,
        "treatise": 0.65,
        "secondary_source": 0.50,
        "industry_practice": 0.40,
    }

    def classify_authority(self, citation: str) -> str:
        """Classify an authority citation by type."""
        citation_lower = citation.lower()
        if "tex." in citation_lower and ("s.w." in citation_lower or "supreme" in citation_lower):
            if "app." in citation_lower:
                return "texas_appeals_court"
            return "texas_supreme_court"
        if "f.3d" in citation_lower or "f.2d" in citation_lower or "cir." in citation_lower:
            return "fifth_circuit"
        if "code" in citation_lower or "§" in citation_lower or "u.s.c." in citation_lower:
            return "texas_statute"
        if "rrc" in citation_lower or "railroad commission" in citation_lower or "statewide rule" in citation_lower:
            return "rrc_rule"
        if "aapl" in citation_lower:
            return "aapl_standard"
        if "williams" in citation_lower or "treatise" in citation_lower or "handbook" in citation_lower:
            return "treatise"
        return "secondary_source"

    def resolve_authorities(self, citations: List[str]) -> List[Dict[str, Any]]:
        """Resolve and weight a list of authority citations."""
        resolved: List[Dict[str, Any]] = []
        for cite in citations:
            auth_type = self.classify_authority(cite)
            weight = self.AUTHORITY_WEIGHTS.get(auth_type, 0.30)
            resolved.append({
                "citation": cite,
                "type": auth_type,
                "weight": weight,
            })
        resolved.sort(key=lambda x: x["weight"], reverse=True)
        return resolved

    def compute_authority_strength(self, citations: List[str]) -> float:
        """Compute aggregate authority strength score (0-1)."""
        if not citations:
            return 0.0
        resolved = self.resolve_authorities(citations)
        weights = [r["weight"] for r in resolved]
        return round(max(weights) * 0.6 + (sum(weights) / len(weights)) * 0.4, 3)


# ==============================================================================
# FACT FRAGILITY SCORING
# ==============================================================================

class FragilityAssessor:
    """Assess the fragility of factual conclusions in lease negotiation."""

    def assess(
        self,
        conclusion: str,
        authorities: List[str],
        confidence: str,
        has_statutory_basis: bool = False,
        has_case_law: bool = False,
        depends_on_testimony: bool = False,
    ) -> FragilityScore:
        """Compute fragility score for a conclusion."""
        # Verifiability: higher if statutory or case law basis
        verifiability = 0.5
        if has_statutory_basis:
            verifiability += 0.3
        if has_case_law:
            verifiability += 0.2
        verifiability = min(verifiability, 1.0)

        # Recharacterization risk: based on confidence level
        rechar_map = {
            "DEFENSIBLE": 0.2,
            "AGGRESSIVE": 0.5,
            "DISCLOSURE": 0.6,
            "HIGH_RISK": 0.8,
        }
        recharacterization_risk = rechar_map.get(confidence, 0.5)

        # Testimony dependence
        testimony_dependence = 0.7 if depends_on_testimony else 0.2

        # Overall fragility: weighted composite
        overall = (
            (1.0 - verifiability) * 0.4
            + recharacterization_risk * 0.35
            + testimony_dependence * 0.25
        )

        # Assessment text
        if overall < 0.3:
            assessment = "LOW FRAGILITY — conclusion is well-supported by authority and documentary evidence"
        elif overall < 0.5:
            assessment = "MODERATE FRAGILITY — conclusion has supporting authority but some elements are contestable"
        elif overall < 0.7:
            assessment = "ELEVATED FRAGILITY — conclusion depends on interpretation and may face challenge"
        else:
            assessment = "HIGH FRAGILITY — conclusion is aggressive and depends on favorable fact characterization"

        return FragilityScore(
            verifiability=round(verifiability, 3),
            recharacterization_risk=round(recharacterization_risk, 3),
            testimony_dependence=round(testimony_dependence, 3),
            overall_fragility=round(overall, 3),
            assessment=assessment,
        )


# ==============================================================================
# MULTI-DOCTRINE DECOMPOSITION
# ==============================================================================

class IssueDecomposer:
    """Decompose complex lease queries into issue categories and doctrine interactions."""

    ISSUE_KEYWORDS: ClassVar[Dict[IssueCategory, List[str]]] = {
        IssueCategory.ROYALTY: ["royalty", "fraction", "1/4", "1/5", "1/8", "cost-free", "proceeds", "market value"],
        IssueCategory.BONUS: ["bonus", "per acre", "consideration", "signing", "delay rental", "paid-up"],
        IssueCategory.TERM: ["primary term", "years", "three year", "five year", "ten year"],
        IssueCategory.HABENDUM: ["habendum", "so long thereafter", "held by production", "hbp"],
        IssueCategory.DRILLING_OBLIGATIONS: ["continuous drilling", "development", "cdc", "drill or release"],
        IssueCategory.PUGH: ["pugh", "depth severance", "vertical pugh", "horizontal pugh", "acreage release"],
        IssueCategory.SURFACE_USE: ["surface", "damage", "restoration", "accommodation", "location"],
        IssueCategory.POOLING: ["pooling", "unitization", "force pooling", "community lease", "spacing"],
        IssueCategory.SHUT_IN: ["shut-in", "shut in", "capable of producing"],
        IssueCategory.CESSATION: ["cessation", "temporary cessation", "savings clause", "sixty-day"],
        IssueCategory.DEPTH: ["depth limitation", "shallow rights", "deep rights", "depth clause"],
        IssueCategory.RELEASE: ["release", "partial release", "surrender", "termination"],
        IssueCategory.ASSIGNMENT: ["assignment", "transfer", "consent", "rofr"],
        IssueCategory.ENVIRONMENTAL: ["environmental", "indemnification", "plugging", "remediation"],
        IssueCategory.AUDIT_RIGHTS: ["audit", "records", "books", "inspection", "accounting"],
        IssueCategory.TOP_LEASE: ["top lease", "top leasing", "replacement lease"],
        IssueCategory.AMENDMENT: ["amendment", "extension", "ratification", "renewal"],
        IssueCategory.MINERAL_SURFACE: ["mineral owner", "surface owner", "severed estate", "dominant estate"],
        IssueCategory.MARKET_ENHANCEMENT: ["market enhancement", "marketing", "affiliate", "arm's length"],
        IssueCategory.WATER_RIGHTS: ["water", "groundwater", "fresh water", "produced water"],
        IssueCategory.IMPLIED_COVENANTS: ["implied covenant", "reasonable development", "drainage", "prudent operator"],
    }

    INTERACTION_EDGES: ClassVar[List[tuple]] = [
        (IssueCategory.ROYALTY, IssueCategory.BONUS, "inverse_economic_tradeoff"),
        (IssueCategory.ROYALTY, IssueCategory.MARKET_ENHANCEMENT, "valuation_dependency"),
        (IssueCategory.PUGH, IssueCategory.POOLING, "acreage_scope_interaction"),
        (IssueCategory.PUGH, IssueCategory.DEPTH, "vertical_horizontal_coordination"),
        (IssueCategory.HABENDUM, IssueCategory.CESSATION, "lease_maintenance_chain"),
        (IssueCategory.HABENDUM, IssueCategory.SHUT_IN, "production_substitute_chain"),
        (IssueCategory.TERM, IssueCategory.DRILLING_OBLIGATIONS, "development_timeline"),
        (IssueCategory.TERM, IssueCategory.PUGH, "expiration_release_coordination"),
        (IssueCategory.SURFACE_USE, IssueCategory.MINERAL_SURFACE, "estate_rights_allocation"),
        (IssueCategory.SURFACE_USE, IssueCategory.WATER_RIGHTS, "resource_competition"),
        (IssueCategory.POOLING, IssueCategory.DEPTH, "unit_depth_interaction"),
        (IssueCategory.ASSIGNMENT, IssueCategory.ENVIRONMENTAL, "liability_transfer"),
        (IssueCategory.CESSATION, IssueCategory.SHUT_IN, "production_interruption_coverage"),
        (IssueCategory.RELEASE, IssueCategory.PUGH, "release_mechanism_coordination"),
        (IssueCategory.DRILLING_OBLIGATIONS, IssueCategory.RELEASE, "drill_or_release_obligation"),
        (IssueCategory.AUDIT_RIGHTS, IssueCategory.ROYALTY, "verification_dependency"),
        (IssueCategory.TOP_LEASE, IssueCategory.AMENDMENT, "lease_succession_strategy"),
        (IssueCategory.IMPLIED_COVENANTS, IssueCategory.DRILLING_OBLIGATIONS, "development_obligation_overlap"),
    ]

    def decompose(self, query: str) -> Dict[str, Any]:
        """Decompose a query into issue categories and interactions."""
        query_lower = query.lower()
        detected_issues: List[IssueCategory] = []
        issue_scores: Dict[str, int] = {}

        for category, keywords in self.ISSUE_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in query_lower)
            if score > 0:
                detected_issues.append(category)
                issue_scores[category.value] = score

        if not detected_issues:
            detected_issues = [IssueCategory.GENERAL]
            issue_scores["general"] = 1

        # Find relevant interaction edges
        interactions: List[Dict[str, str]] = []
        for cat_a, cat_b, relationship in self.INTERACTION_EDGES:
            if cat_a in detected_issues and cat_b in detected_issues:
                interactions.append({
                    "issue_a": cat_a.value,
                    "issue_b": cat_b.value,
                    "relationship": relationship,
                })

        # Sort by score
        sorted_issues = sorted(issue_scores.items(), key=lambda x: x[1], reverse=True)

        return {
            "primary_issue": sorted_issues[0][0] if sorted_issues else "general",
            "all_issues": [cat.value for cat in detected_issues],
            "issue_scores": issue_scores,
            "interactions": interactions,
            "complexity": len(detected_issues),
            "multi_doctrine": len(detected_issues) > 1,
        }


# ==============================================================================
# EPISTEMIC GUARDRAILS
# ==============================================================================

def apply_epistemic_guardrails(text: str) -> str:
    """Remove banned phrases and apply epistemic discipline to response text."""
    result = text
    for phrase in BANNED_PHRASES:
        while phrase.lower() in result.lower():
            idx = result.lower().index(phrase.lower())
            result = result[:idx] + result[idx + len(phrase):]
    # Clean up double spaces
    while "  " in result:
        result = result.replace("  ", " ")
    return result.strip()


def generate_disclosure_caveat(confidence: str, zone: str) -> str:
    """Generate appropriate disclosure caveat based on confidence and zone."""
    if confidence == "DEFENSIBLE" and zone == "PLANNING":
        return (
            "This analysis reflects established lease negotiation principles supported by "
            "Texas case law and industry practice. Specific lease language should be reviewed "
            "by qualified oil and gas counsel before execution."
        )
    if confidence == "AGGRESSIVE":
        return (
            "This position takes an aggressive interpretation that may face challenge. "
            "The analysis is informed by case law trends but the specific outcome depends "
            "on lease language, jurisdiction, and court interpretation."
        )
    if confidence == "DISCLOSURE":
        return (
            "This area involves evolving legal standards or split authority. Multiple "
            "defensible positions exist. The recommended approach should be evaluated "
            "against current jurisdictional trends."
        )
    if confidence == "HIGH_RISK":
        return (
            "This position carries elevated risk. While supported by some authority, "
            "contrary authority exists and the outcome is uncertain. Consider alternative "
            "strategies that achieve similar objectives with lower risk."
        )
    return (
        "Analysis based on established lease negotiation principles and Texas oil and gas law. "
        "Specific application depends on lease language and factual circumstances."
    )


# ==============================================================================
# LEASE NEGOTIATION ENGINE — CORE
# ==============================================================================

class LeaseNegotiationEngine:
    """
    Core engine implementing TIE-20 standard for oil and gas lease negotiation.

    Components:
    1.  three_layer_response
    2.  response_modes (FAST/DEFENSE/MEMO)
    3.  doctrine_cache (26+ pre-compiled blocks)
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
    """

    def __init__(self) -> None:
        self._start_time: float = time.time()
        self._doctrine_cache: Dict[str, DoctrineBlock] = {}
        self._search_engine: LeaseNegotiationSearchEngine = get_search_engine()
        self._telemetry: TelemetryCollector = get_telemetry()
        self._metrics: MetricsCollector = MetricsCollector()
        self._drift_watcher: DoctrineDriftWatcher = DoctrineDriftWatcher()
        self._coverage_map: DoctrineCoverageMap = DoctrineCoverageMap()
        self._authority_resolver: AuthorityResolver = AuthorityResolver()
        self._fragility_assessor: FragilityAssessor = FragilityAssessor()
        self._issue_decomposer: IssueDecomposer = IssueDecomposer()
        self._initialized: bool = False
        logger.info(f"LeaseNegotiationEngine created: {ENGINE_ID} v{ENGINE_VERSION}")

    def initialize(self) -> None:
        """Initialize all engine subsystems."""
        logger.info("Initializing Lease Negotiation Engine...")

        # Build doctrine cache
        self._doctrine_cache = build_doctrine_cache()
        logger.info(f"Doctrine cache loaded: {len(self._doctrine_cache)} blocks")

        # Index doctrines for search
        for topic, block in self._doctrine_cache.items():
            self._search_engine.index_doctrine_block(
                topic=block.topic,
                keywords=block.keywords,
                conclusion_template=block.conclusion_template,
                confidence=block.confidence,
                entity_scope=block.entity_scope,
            )
        self._search_engine.build_index()
        logger.info(f"Search index built: {self._search_engine.get_stats()['document_count']} documents")

        # Initialize drift watcher
        self._drift_watcher.initialize(self._doctrine_cache)

        self._initialized = True
        logger.info(f"Engine {ENGINE_ID} fully initialized")

    # --------------------------------------------------------------------------
    # LAYER 1: DOCTRINE CACHE LOOKUP
    # --------------------------------------------------------------------------

    def _doctrine_lookup(self, query: str, norm_result: NormalizationResult) -> Optional[DoctrineBlock]:
        """Attempt doctrine cache lookup using normalized terms."""
        # Direct topic match
        for canonical in norm_result.canonical_terms:
            if canonical in self._doctrine_cache:
                return self._doctrine_cache[canonical]

        # Keyword-based search across doctrine blocks
        query_lower = query.lower()
        best_match: Optional[DoctrineBlock] = None
        best_score: int = 0

        for topic, block in self._doctrine_cache.items():
            score = sum(1 for kw in block.keywords if kw.lower() in query_lower)
            # Boost for canonical term match
            for canonical in norm_result.canonical_terms:
                if canonical == topic:
                    score += 10
                elif canonical in [kw.lower() for kw in block.keywords]:
                    score += 3

            if score > best_score:
                best_score = score
                best_match = block

        if best_score >= 2:
            return best_match
        return None

    # --------------------------------------------------------------------------
    # LAYER 2: SEMANTIC RETRIEVAL
    # --------------------------------------------------------------------------

    def _semantic_retrieval(self, query: str, top_k: int = 3) -> List[SearchResult]:
        """Perform semantic search when doctrine cache misses."""
        response = self._search_engine.search(query, top_k=top_k)
        return response.results

    # --------------------------------------------------------------------------
    # LAYER 3: DEEP ANALYSIS
    # --------------------------------------------------------------------------

    def _deep_analysis(
        self,
        query: str,
        norm_result: NormalizationResult,
        decomposition: Dict[str, Any],
        search_results: List[SearchResult],
    ) -> Dict[str, Any]:
        """
        Multi-source synthesis for complex queries that span multiple doctrines.
        Combines search results, decomposition, and cross-doctrine reasoning.
        """
        # Gather all relevant doctrine blocks
        relevant_blocks: List[DoctrineBlock] = []
        for issue in decomposition.get("all_issues", []):
            for topic, block in self._doctrine_cache.items():
                if issue in topic or any(issue in kw.lower() for kw in block.keywords):
                    if block not in relevant_blocks:
                        relevant_blocks.append(block)

        # Add blocks from search results
        for sr in search_results:
            if sr.topic in self._doctrine_cache:
                block = self._doctrine_cache[sr.topic]
                if block not in relevant_blocks:
                    relevant_blocks.append(block)

        # Synthesize conclusion from multiple blocks
        conclusions: List[str] = []
        all_factors: List[str] = []
        all_authorities: List[str] = []
        all_counter_args: List[str] = []
        all_strategies: List[str] = []

        for block in relevant_blocks[:5]:
            conclusions.append(block.conclusion_template)
            all_factors.extend(block.key_factors)
            all_authorities.extend(block.primary_authority)
            all_counter_args.extend(block.counter_arguments)
            all_strategies.append(block.resolution_strategy)

        # Deduplicate
        all_factors = list(dict.fromkeys(all_factors))
        all_authorities = list(dict.fromkeys(all_authorities))
        all_counter_args = list(dict.fromkeys(all_counter_args))

        # Build interaction analysis
        interaction_analysis = ""
        for interaction in decomposition.get("interactions", []):
            interaction_analysis += (
                f"Interaction between {interaction['issue_a']} and {interaction['issue_b']}: "
                f"{interaction['relationship']}. "
            )

        # Synthesized conclusion
        synthesized = " ".join(conclusions[:3])
        if interaction_analysis:
            synthesized += f" Key interactions: {interaction_analysis}"

        # Determine overall confidence — lowest confidence of any contributing block
        confidence_priority = ["HIGH_RISK", "DISCLOSURE", "AGGRESSIVE", "DEFENSIBLE"]
        overall_confidence = "DEFENSIBLE"
        for block in relevant_blocks:
            if confidence_priority.index(block.confidence) < confidence_priority.index(overall_confidence):
                overall_confidence = block.confidence

        return {
            "conclusion": synthesized,
            "key_factors": all_factors[:10],
            "authorities": all_authorities[:8],
            "counter_arguments": all_counter_args[:8],
            "resolution_strategy": " ".join(all_strategies[:3]),
            "confidence": overall_confidence,
            "blocks_consulted": len(relevant_blocks),
            "interactions": decomposition.get("interactions", []),
        }

    # --------------------------------------------------------------------------
    # THREE-LAYER RESPONSE
    # --------------------------------------------------------------------------

    def process_query(self, request: QueryRequest) -> QueryResponse:
        """
        Process a lease negotiation query through the three-layer response system.

        Layer 1: Doctrine Cache (0-200ms) — instant if we have a pre-compiled block
        Layer 2: Semantic Retrieval (200-700ms) — search when cache misses
        Layer 3: Deep Analysis (on-demand) — multi-doctrine synthesis
        """
        start_time = time.time()
        trace = trace_query(
            request.query,
            session_id=request.session_id,
            response_mode=request.mode.value,
            analysis_zone=request.zone.value,
        )

        try:
            # Semantic normalization
            span_norm = trace.add_span("semantic_normalization")
            norm_result = normalize_semantics(request.query)
            span_norm.complete({"canonical_terms": norm_result.canonical_terms})

            # Issue decomposition
            span_decomp = trace.add_span("issue_decomposition")
            decomposition = self._issue_decomposer.decompose(request.query)
            span_decomp.complete({"issues": decomposition["all_issues"]})

            # Basin and role detection
            basin = request.basin or norm_result.basin_context
            party_role = request.party_role or norm_result.party_role

            # Layer 1: Doctrine Cache
            span_doctrine = trace.add_span("doctrine_cache_lookup", ResponseLayer.DOCTRINE_CACHE)
            doctrine = self._doctrine_lookup(request.query, norm_result)
            span_doctrine.complete({"hit": doctrine is not None})

            response_layer = ResponseLayer.DOCTRINE_CACHE
            doctrine_hit = False
            doctrine_topic: Optional[str] = None

            if doctrine:
                doctrine_hit = True
                doctrine_topic = doctrine.topic
                self._coverage_map.record_hit(doctrine.topic)

                conclusion = doctrine.conclusion_template
                reasoning = doctrine.reasoning_framework
                key_factors = doctrine.key_factors
                authorities = doctrine.primary_authority
                counter_args = doctrine.counter_arguments
                resolution = doctrine.resolution_strategy
                confidence = doctrine.confidence
                confidence_strat = doctrine.confidence_stratification
                burden = doctrine.burden_holder
                entity_scope = doctrine.entity_scope
            else:
                self._coverage_map.record_miss(request.query)

                # Layer 2: Semantic Retrieval
                span_search = trace.add_span("semantic_retrieval", ResponseLayer.SEMANTIC_RETRIEVAL)
                search_results = self._semantic_retrieval(request.query)
                span_search.complete({"result_count": len(search_results)})
                response_layer = ResponseLayer.SEMANTIC_RETRIEVAL

                if search_results:
                    top = search_results[0]
                    if top.topic in self._doctrine_cache:
                        block = self._doctrine_cache[top.topic]
                        conclusion = block.conclusion_template
                        reasoning = block.reasoning_framework
                        key_factors = block.key_factors
                        authorities = block.primary_authority
                        counter_args = block.counter_arguments
                        resolution = block.resolution_strategy
                        confidence = block.confidence
                        confidence_strat = block.confidence_stratification
                        burden = block.burden_holder
                        entity_scope = block.entity_scope
                        doctrine_topic = top.topic
                    else:
                        conclusion = top.conclusion_preview
                        reasoning = f"Retrieved via semantic search (score: {top.score:.3f})"
                        key_factors = top.keywords_matched
                        authorities = []
                        counter_args = []
                        resolution = "Further analysis recommended based on specific lease language."
                        confidence = top.confidence
                        confidence_strat = "DISCLOSURE"
                        burden = "requires_analysis"
                        entity_scope = top.entity_scope
                else:
                    # Layer 3: Deep Analysis
                    span_deep = trace.add_span("deep_analysis", ResponseLayer.DEEP_ANALYSIS)
                    deep_result = self._deep_analysis(
                        request.query, norm_result, decomposition, search_results
                    )
                    span_deep.complete({"blocks_consulted": deep_result["blocks_consulted"]})
                    response_layer = ResponseLayer.DEEP_ANALYSIS

                    conclusion = deep_result["conclusion"]
                    reasoning = f"Multi-doctrine synthesis across {deep_result['blocks_consulted']} doctrine blocks."
                    key_factors = deep_result["key_factors"]
                    authorities = deep_result["authorities"]
                    counter_args = deep_result["counter_arguments"]
                    resolution = deep_result["resolution_strategy"]
                    confidence = deep_result["confidence"]
                    confidence_strat = confidence
                    burden = "multi_party_analysis"
                    entity_scope = "multi_scope"

            # Also run deep analysis for DEFENSE and MEMO modes even on cache hit
            if doctrine_hit and request.mode in (ResponseMode.DEFENSE, ResponseMode.MEMO):
                span_deep_enhance = trace.add_span("deep_analysis_enhancement", ResponseLayer.DEEP_ANALYSIS)
                deep_result = self._deep_analysis(
                    request.query, norm_result, decomposition, []
                )
                span_deep_enhance.complete()
                # Enhance with additional factors and authorities
                for factor in deep_result.get("key_factors", []):
                    if factor not in key_factors:
                        key_factors.append(factor)
                for auth in deep_result.get("authorities", []):
                    if auth not in authorities:
                        authorities.append(auth)

            # Apply response mode formatting
            if request.mode == ResponseMode.FAST:
                conclusion = conclusion[:500]
                reasoning = reasoning[:300] if reasoning else ""
                key_factors = key_factors[:5]
                authorities = authorities[:3]
                counter_args = counter_args[:3]
            elif request.mode == ResponseMode.MEMO:
                # MEMO mode: full detail, no truncation
                pass

            # Epistemic guardrails
            conclusion = apply_epistemic_guardrails(conclusion)
            if reasoning:
                reasoning = apply_epistemic_guardrails(reasoning)

            # Fragility assessment
            has_statutory = any("code" in a.lower() or "§" in a for a in authorities)
            has_case_law = any("s.w." in a.lower() or "f.3d" in a.lower() for a in authorities)
            fragility = self._fragility_assessor.assess(
                conclusion=conclusion,
                authorities=authorities,
                confidence=confidence,
                has_statutory_basis=has_statutory,
                has_case_law=has_case_law,
            )

            # Disclosure caveat
            disclosure = generate_disclosure_caveat(confidence, request.zone.value)

            # Determinism hash
            hash_content = f"{request.query}|{conclusion}|{confidence}|{request.mode.value}"
            determinism_hash = hashlib.sha256(hash_content.encode()).hexdigest()

            # Calculate latency
            latency_ms = (time.time() - start_time) * 1000

            # Complete telemetry trace
            complete_trace(
                trace,
                final_layer=response_layer,
                doctrine_hit=doctrine_hit,
                doctrine_topic=doctrine_topic,
                confidence_level=confidence,
                determinism_hash=determinism_hash,
            )

            # Record metrics
            self._metrics.record_query(latency_ms, doctrine_hit)

            # Write audit trail
            self._write_audit(request, conclusion, confidence, latency_ms, determinism_hash, trace.trace_id)

            return QueryResponse(
                query=request.query,
                response_mode=request.mode.value,
                analysis_zone=request.zone.value,
                conclusion=conclusion,
                reasoning=reasoning,
                confidence=confidence,
                confidence_stratification=confidence_strat,
                key_factors=key_factors,
                authorities=authorities,
                counter_arguments=counter_args,
                resolution_strategy=resolution,
                fragility=fragility,
                issue_categories=decomposition["all_issues"],
                basin_context=basin,
                party_role=party_role,
                doctrine_hit=doctrine_hit,
                doctrine_topic=doctrine_topic,
                response_layer=response_layer.value,
                latency_ms=round(latency_ms, 2),
                determinism_hash=determinism_hash,
                trace_id=trace.trace_id,
                timestamp=datetime.now(timezone.utc).isoformat(),
                disclosure_caveat=disclosure,
            )

        except Exception as exc:
            latency_ms = (time.time() - start_time) * 1000
            error_msg = str(exc)
            trace.error = error_msg
            self._metrics.record_error(error_msg)
            log_error(
                ErrorDomain.UNKNOWN,
                error_msg,
                trace_id=trace.trace_id,
                stack_trace=traceback.format_exc(),
                query_context=request.query,
            )
            logger.error(f"Query processing failed: {error_msg}")
            raise HTTPException(status_code=500, detail=f"Engine error: {error_msg}")

    def _write_audit(
        self,
        request: QueryRequest,
        conclusion: str,
        confidence: str,
        latency_ms: float,
        determinism_hash: str,
        trace_id: str,
    ) -> None:
        """Write audit trail entry to JSONL file."""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "engine_id": ENGINE_ID,
            "trace_id": trace_id,
            "query": request.query[:200],
            "mode": request.mode.value,
            "zone": request.zone.value,
            "conclusion_preview": conclusion[:200],
            "confidence": confidence,
            "latency_ms": round(latency_ms, 2),
            "hash": determinism_hash,
        }
        try:
            with open(AUDIT_LOG, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as exc:
            logger.warning(f"Failed to write audit trail: {exc}")

    # --------------------------------------------------------------------------
    # HEALTH AND DIAGNOSTICS
    # --------------------------------------------------------------------------

    def get_health(self) -> HealthResponse:
        """Return comprehensive health check."""
        uptime = time.time() - self._start_time
        metrics = self._metrics.get_stats()
        normalizer_stats = get_normalizer().get_stats()
        search_stats = self._search_engine.get_stats()

        return HealthResponse(
            status="healthy" if self._initialized else "initializing",
            uptime_seconds=round(uptime, 1),
            doctrine_count=len(self._doctrine_cache),
            search_index_size=search_stats.get("document_count", 0),
            total_queries=metrics.get("total_queries", 0),
            doctrine_hit_rate_pct=metrics.get("hit_rate_pct", 0.0),
            metrics=metrics,
            normalizer_stats=normalizer_stats,
            search_stats=search_stats,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )


# ==============================================================================
# FASTAPI APPLICATION
# ==============================================================================

engine = LeaseNegotiationEngine()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    logger.info(f"Starting {ENGINE_NAME} v{ENGINE_VERSION} on port {ENGINE_PORT}")
    engine.initialize()
    logger.info(f"Engine {ENGINE_ID} ready — {len(engine._doctrine_cache)} doctrines loaded")

    if _CLOUD_AVAILABLE:
        logger.info("Cloud knowledge integration: ENABLED")
    else:
        logger.info("Cloud knowledge integration: DISABLED (cloud_retriever not found)")

    yield

    logger.info(f"Shutting down {ENGINE_NAME}")
    get_telemetry().flush()

    # Cleanup cloud retriever if available
    if _CLOUD_AVAILABLE:
        try:
            # Cloud retriever cleanup happens automatically via context manager
            logger.info("Cloud knowledge cleanup complete")
        except Exception as e:
            logger.warning(f"Cloud cleanup error: {e}")


app = FastAPI(
    title=ENGINE_NAME,
    description=(
        "TIE Gold Standard engine for oil and gas lease negotiation strategy. "
        "Covers royalty clauses, bonus negotiation, primary term selection, habendum, "
        "continuous drilling, Pugh clause, surface use, pooling/unitization, shut-in "
        "royalty, cessation of production, depth limitations, and 15+ additional "
        "negotiation domains."
    ),
    version=ENGINE_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------------------------------
# API ENDPOINTS
# --------------------------------------------------------------------------

@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Comprehensive health check endpoint."""
    return engine.get_health()


@app.get("/")
async def root() -> Dict[str, Any]:
    """Root endpoint with engine info."""
    return {
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "version": ENGINE_VERSION,
        "port": ENGINE_PORT,
        "domain": ENGINE_DOMAIN,
        "status": "operational",
        "endpoints": [
            "/health", "/query", "/doctrines", "/search",
            "/metrics", "/coverage", "/drift", "/decompose",
        ],
    }


@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest) -> QueryResponse:
    """
    Primary query endpoint — three-layer response system.

    Modes:
    - FAST: Quick doctrine-driven response (<200ms target)
    - DEFENSE: Audit-ready with full authority chain
    - MEMO: Long-form documentation-grade output
    """
    result = engine.process_query(request)

    # Cloud knowledge enrichment
    if _CLOUD_AVAILABLE:
        try:
            cloud = await retrieve_cloud_knowledge(
                request.query,
                category="lease_negotiation",
                top_k=3
            )

            # Enrich result with cloud data
            result_dict = result.model_dump()
            result_dict["cloud_knowledge"] = {
                "total_sources": cloud.total_sources,
                "ekm_matches": len(cloud.ekm_results),
                "crystal_matches": len(cloud.crystal_results),
                "graph_nodes": len(cloud.graph_results),
                "combined_summary": cloud.combined_summary if hasattr(cloud, 'combined_summary') else None
            }
            result_dict["cloud_citations"] = cloud.citation_list()

            # Convert back to QueryResponse
            result = QueryResponse(**result_dict)

            logger.info(f"Cloud enrichment: {cloud.total_sources} sources, {len(cloud.citation_list())} citations")
        except Exception as e:
            logger.warning(f"Cloud retrieval failed: {e}")

    return result


@app.get("/doctrines")
async def list_doctrines() -> Dict[str, Any]:
    """List all available doctrine blocks."""
    return {
        "engine_id": ENGINE_ID,
        "doctrine_count": len(engine._doctrine_cache),
        "doctrines": [
            {
                "topic": block.topic,
                "keywords": block.keywords,
                "confidence": block.confidence,
                "entity_scope": block.entity_scope,
                "controlling_precedent": block.controlling_precedent,
            }
            for block in engine._doctrine_cache.values()
        ],
    }


@app.get("/doctrines/{topic}")
async def get_doctrine(topic: str) -> Dict[str, Any]:
    """Get a specific doctrine block by topic."""
    block = engine._doctrine_cache.get(topic)
    if not block:
        raise HTTPException(status_code=404, detail=f"Doctrine not found: {topic}")
    return {
        "engine_id": ENGINE_ID,
        "doctrine": block.to_dict(),
        "full_reasoning": block.reasoning_framework,
        "adversary_position": block.adversary_position,
        "counter_arguments": block.counter_arguments,
        "resolution_strategy": block.resolution_strategy,
        "controlling_precedent": block.controlling_precedent,
    }


@app.post("/search")
async def search_doctrines(query: str, top_k: int = 5) -> Dict[str, Any]:
    """Search doctrine blocks by semantic similarity."""
    response = engine._search_engine.search(query, top_k=top_k)
    return response.to_dict()


@app.get("/metrics")
async def get_metrics() -> Dict[str, Any]:
    """Return operational metrics."""
    return {
        "engine_id": ENGINE_ID,
        "engine_metrics": engine._metrics.get_stats(),
        "telemetry_metrics": get_telemetry().get_metrics(),
        "search_stats": engine._search_engine.get_stats(),
        "normalizer_stats": get_normalizer().get_stats(),
    }


@app.get("/coverage")
async def get_coverage() -> Dict[str, Any]:
    """Return doctrine coverage report."""
    return {
        "engine_id": ENGINE_ID,
        "coverage": engine._coverage_map.get_coverage_report(len(engine._doctrine_cache)),
    }


@app.get("/drift")
async def check_drift() -> Dict[str, Any]:
    """Check for doctrine drift."""
    drift_events = engine._drift_watcher.check_drift(engine._doctrine_cache)
    return {
        "engine_id": ENGINE_ID,
        "drift_detected": len(drift_events) > 0,
        "events": drift_events,
        "history": engine._drift_watcher.get_drift_history(),
        "stats": engine._drift_watcher.get_stats(),
    }


@app.post("/decompose")
async def decompose_query(query: str) -> Dict[str, Any]:
    """Decompose a query into issue categories and interactions."""
    return {
        "engine_id": ENGINE_ID,
        "query": query,
        "decomposition": engine._issue_decomposer.decompose(query),
    }


@app.get("/traces")
async def get_traces(limit: int = 20) -> Dict[str, Any]:
    """Return recent query traces."""
    return {
        "engine_id": ENGINE_ID,
        "traces": get_telemetry().get_recent_traces(limit),
    }


@app.get("/errors")
async def get_errors(limit: int = 20) -> Dict[str, Any]:
    """Return recent errors."""
    return {
        "engine_id": ENGINE_ID,
        "errors": get_telemetry().get_recent_errors(limit),
    }


@app.get("/mutations")
async def get_mutations(limit: int = 50) -> Dict[str, Any]:
    """Return doctrine mutation history."""
    return {
        "engine_id": ENGINE_ID,
        "mutations": get_telemetry().get_mutation_history(limit),
    }


@app.get("/authority/{topic}")
async def resolve_authority(topic: str) -> Dict[str, Any]:
    """Resolve authority citations for a specific doctrine topic."""
    block = engine._doctrine_cache.get(topic)
    if not block:
        raise HTTPException(status_code=404, detail=f"Doctrine not found: {topic}")
    resolved = engine._authority_resolver.resolve_authorities(block.primary_authority)
    strength = engine._authority_resolver.compute_authority_strength(block.primary_authority)
    return {
        "engine_id": ENGINE_ID,
        "topic": topic,
        "authorities": resolved,
        "aggregate_strength": strength,
    }


@app.get("/fragility/{topic}")
async def assess_fragility(topic: str) -> Dict[str, Any]:
    """Assess fact fragility for a specific doctrine topic."""
    block = engine._doctrine_cache.get(topic)
    if not block:
        raise HTTPException(status_code=404, detail=f"Doctrine not found: {topic}")
    has_statutory = any("code" in a.lower() or "§" in a for a in block.primary_authority)
    has_case_law = any("s.w." in a.lower() or "f.3d" in a.lower() for a in block.primary_authority)
    score = engine._fragility_assessor.assess(
        conclusion=block.conclusion_template,
        authorities=block.primary_authority,
        confidence=block.confidence,
        has_statutory_basis=has_statutory,
        has_case_law=has_case_law,
    )
    return {
        "engine_id": ENGINE_ID,
        "topic": topic,
        "fragility": score.model_dump(),
    }


# ==============================================================================
# BATCH QUERY SUPPORT
# ==============================================================================

class BatchQueryRequest(BaseModel):
    """Batch query request for multiple lease negotiation questions."""
    queries: List[QueryRequest] = Field(..., min_length=1, max_length=20)
    session_id: Optional[str] = Field(default=None, description="Shared session ID for the batch")


class BatchQueryResponse(BaseModel):
    """Batch query response."""
    engine_id: str = ENGINE_ID
    batch_size: int = 0
    total_latency_ms: float = 0.0
    avg_latency_ms: float = 0.0
    doctrine_hit_rate_pct: float = 0.0
    responses: List[QueryResponse] = []
    timestamp: str = ""


@app.post("/batch", response_model=BatchQueryResponse)
async def batch_query(request: BatchQueryRequest) -> BatchQueryResponse:
    """Process multiple lease negotiation queries in a single request."""
    start = time.time()
    responses: List[QueryResponse] = []
    hits = 0
    total = 0

    for q in request.queries:
        if request.session_id and not q.session_id:
            q.session_id = request.session_id
        try:
            resp = engine.process_query(q)
            responses.append(resp)
            total += 1
            if resp.doctrine_hit:
                hits += 1
        except HTTPException:
            total += 1

    total_ms = (time.time() - start) * 1000
    avg_ms = total_ms / max(total, 1)
    hit_pct = (hits / max(total, 1)) * 100

    return BatchQueryResponse(
        batch_size=total,
        total_latency_ms=round(total_ms, 2),
        avg_latency_ms=round(avg_ms, 2),
        doctrine_hit_rate_pct=round(hit_pct, 2),
        responses=responses,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


# ==============================================================================
# LEASE COMPARISON ENDPOINT
# ==============================================================================

class LeaseClauseInput(BaseModel):
    """Input for a single lease clause to analyze."""
    clause_name: str = Field(..., description="Name of the clause (e.g., royalty, pugh, pooling)")
    clause_text: str = Field(..., description="Actual clause language from the lease")
    lease_id: Optional[str] = Field(default=None, description="Identifier for the lease")


class ClauseAnalysis(BaseModel):
    """Analysis of a single lease clause."""
    clause_name: str
    doctrine_topic: Optional[str] = None
    assessment: str = ""
    strengths: List[str] = []
    weaknesses: List[str] = []
    missing_protections: List[str] = []
    recommended_modifications: List[str] = []
    confidence: str = "DEFENSIBLE"
    authority_references: List[str] = []
    overall_grade: str = ""


class LeaseAnalysisRequest(BaseModel):
    """Request to analyze lease clauses."""
    clauses: List[LeaseClauseInput] = Field(..., min_length=1, max_length=30)
    perspective: str = Field(default="lessor", description="lessor or lessee perspective")
    basin: Optional[str] = Field(default=None, description="Basin context")


class LeaseAnalysisResponse(BaseModel):
    """Complete lease analysis response."""
    engine_id: str = ENGINE_ID
    clause_count: int = 0
    perspective: str = ""
    overall_grade: str = ""
    clause_analyses: List[ClauseAnalysis] = []
    missing_clauses: List[str] = []
    priority_recommendations: List[str] = []
    timestamp: str = ""


# Clause analysis grading rubric
CLAUSE_GRADING_RUBRIC: Dict[str, Dict[str, Any]] = {
    "royalty": {
        "strong_indicators": ["1/4", "25%", "one-fourth", "cost-free", "free of cost", "market value"],
        "weak_indicators": ["1/8", "12.5%", "one-eighth", "proceeds", "at the well", "wellhead"],
        "essential_elements": ["royalty fraction specified", "valuation method", "cost allocation"],
        "missing_protection": "cost-free royalty language",
    },
    "pugh": {
        "strong_indicators": ["vertical", "horizontal", "automatic release", "depths", "unpooled"],
        "weak_indicators": ["at lessee's option", "may release", "discretion"],
        "essential_elements": ["vertical severance", "horizontal severance", "automatic release"],
        "missing_protection": "both vertical and horizontal Pugh clause",
    },
    "pooling": {
        "strong_indicators": ["maximum acreage", "640 acres", "notice", "consent", "rrc spacing"],
        "weak_indicators": ["unlimited", "sole discretion", "any size", "without restriction"],
        "essential_elements": ["size limitation", "notice requirement", "proportionate allocation"],
        "missing_protection": "pooling unit size limitation",
    },
    "surface_use": {
        "strong_indicators": ["surface damage", "restoration", "location approval", "setback", "water"],
        "weak_indicators": ["reasonable use", "necessary operations", "sole discretion"],
        "essential_elements": ["damage payments", "restoration obligation", "location consent"],
        "missing_protection": "surface use protections and damage payments",
    },
    "cessation": {
        "strong_indicators": ["60 days", "90 days", "commence operations", "actual production"],
        "weak_indicators": ["180 days", "one year", "12 months", "good faith efforts"],
        "essential_elements": ["time limit", "operations requirement", "production resumption"],
        "missing_protection": "cessation of production savings clause with defined time limit",
    },
    "shut_in": {
        "strong_indicators": ["2 years", "annual payment", "cumulative limit", "narrow trigger"],
        "weak_indicators": ["indefinite", "no limit", "capable of producing in any quantity"],
        "essential_elements": ["payment amount", "duration limit", "triggering condition"],
        "missing_protection": "shut-in royalty clause with duration limits",
    },
    "assignment": {
        "strong_indicators": ["consent", "notice", "financial qualification", "assume obligations"],
        "weak_indicators": ["free to assign", "without restriction", "without consent"],
        "essential_elements": ["notice requirement", "consent standard", "obligation assumption"],
        "missing_protection": "assignment restrictions with consent requirement",
    },
    "environmental": {
        "strong_indicators": ["indemnify", "remediation", "insurance", "plugging", "survive termination"],
        "weak_indicators": ["gross negligence only", "limited liability", "cap on damages"],
        "essential_elements": ["indemnification", "plugging obligation", "survival clause"],
        "missing_protection": "environmental indemnification surviving lease termination",
    },
    "audit_rights": {
        "strong_indicators": ["inspect records", "5 years", "audit costs", "underpayment"],
        "weak_indicators": ["upon request only", "reasonable access", "operator discretion"],
        "essential_elements": ["right to audit", "record retention", "cost recovery"],
        "missing_protection": "audit rights with cost recovery for underpayments",
    },
    "depth_limitation": {
        "strong_indicators": ["100 feet below", "specific formation", "deepest perforations"],
        "weak_indicators": ["all depths", "surface to center of earth", "without limitation"],
        "essential_elements": ["depth boundary", "formation specification", "release mechanism"],
        "missing_protection": "depth limitation clause for unproduced formations",
    },
    "continuous_drilling": {
        "strong_indicators": ["120 days", "180 days", "automatic release", "well per year"],
        "weak_indicators": ["no drilling obligation", "sole discretion", "good faith"],
        "essential_elements": ["drilling cadence", "gap maximum", "release for non-compliance"],
        "missing_protection": "continuous drilling obligation for large acreage positions",
    },
    "market_enhancement": {
        "strong_indicators": ["arm's length", "index price", "affiliate restriction", "best price"],
        "weak_indicators": ["operator discretion", "reasonable efforts", "commercially reasonable"],
        "essential_elements": ["arm's length requirement", "affiliate disclosure", "marketing audit"],
        "missing_protection": "market enhancement clause preventing below-market affiliate sales",
    },
}

# Essential clauses that every lease should contain
ESSENTIAL_LEASE_CLAUSES: List[str] = [
    "royalty", "pugh", "pooling", "surface_use", "cessation",
    "shut_in", "assignment", "environmental", "audit_rights",
    "depth_limitation", "continuous_drilling", "market_enhancement",
]


def _analyze_clause(clause: LeaseClauseInput, perspective: str) -> ClauseAnalysis:
    """Analyze a single lease clause against the grading rubric."""
    clause_key = clause.clause_name.lower().replace(" ", "_").replace("-", "_")
    clause_text_lower = clause.clause_text.lower()

    rubric = CLAUSE_GRADING_RUBRIC.get(clause_key)

    # Find matching doctrine
    doctrine_topic: Optional[str] = None
    for topic, block in engine._doctrine_cache.items():
        if clause_key in topic or any(clause_key in kw.lower() for kw in block.keywords):
            doctrine_topic = topic
            break

    if not rubric:
        return ClauseAnalysis(
            clause_name=clause.clause_name,
            doctrine_topic=doctrine_topic,
            assessment=f"No grading rubric available for clause type: {clause.clause_name}. Manual review recommended.",
            strengths=[],
            weaknesses=[],
            missing_protections=[],
            recommended_modifications=[],
            confidence="DISCLOSURE",
            authority_references=[],
            overall_grade="UNGRADED",
        )

    # Score strengths and weaknesses
    strengths: List[str] = []
    for indicator in rubric["strong_indicators"]:
        if indicator in clause_text_lower:
            strengths.append(f"Contains strong language: '{indicator}'")

    weaknesses: List[str] = []
    for indicator in rubric["weak_indicators"]:
        if indicator in clause_text_lower:
            weaknesses.append(f"Contains weak/unfavorable language: '{indicator}'")

    # Check essential elements
    missing_protections: List[str] = []
    for element in rubric["essential_elements"]:
        element_keywords = element.lower().split()
        found = any(kw in clause_text_lower for kw in element_keywords)
        if not found:
            missing_protections.append(f"Missing essential element: {element}")

    # Generate recommendations
    recommendations: List[str] = []
    if weaknesses:
        recommendations.append(f"Negotiate to remove weak language: {', '.join(w.split(': ')[1] for w in weaknesses[:3])}")
    if missing_protections:
        recommendations.append(f"Add missing protection: {rubric['missing_protection']}")
    if not strengths:
        recommendations.append(f"Strengthen clause with industry-standard protections for {clause.clause_name}")

    # Get authority references from doctrine
    authorities: List[str] = []
    if doctrine_topic and doctrine_topic in engine._doctrine_cache:
        block = engine._doctrine_cache[doctrine_topic]
        authorities = block.primary_authority[:3]

    # Overall grade
    strength_score = len(strengths)
    weakness_score = len(weaknesses)
    missing_score = len(missing_protections)

    if strength_score >= 3 and weakness_score == 0 and missing_score == 0:
        grade = "A"
        assessment = f"Excellent {clause.clause_name} clause with strong protections."
    elif strength_score >= 2 and weakness_score <= 1 and missing_score <= 1:
        grade = "B"
        assessment = f"Good {clause.clause_name} clause with minor improvements available."
    elif strength_score >= 1 and weakness_score <= 2:
        grade = "C"
        assessment = f"Acceptable {clause.clause_name} clause but significant improvements recommended."
    elif weakness_score >= 2 or missing_score >= 2:
        grade = "D"
        assessment = f"Weak {clause.clause_name} clause requiring substantial renegotiation."
    else:
        grade = "C"
        assessment = f"Average {clause.clause_name} clause — standard improvements recommended."

    # Adjust for perspective
    if perspective == "lessee":
        # Invert the grading — strong lessor protections are weak for lessee
        strengths, weaknesses = weaknesses, strengths
        if grade == "A":
            grade = "D"
        elif grade == "D":
            grade = "A"
        elif grade == "B":
            grade = "C"
        elif grade == "C":
            grade = "B"

    return ClauseAnalysis(
        clause_name=clause.clause_name,
        doctrine_topic=doctrine_topic,
        assessment=assessment,
        strengths=strengths,
        weaknesses=weaknesses,
        missing_protections=missing_protections,
        recommended_modifications=recommendations,
        confidence="DEFENSIBLE",
        authority_references=authorities,
        overall_grade=grade,
    )


@app.post("/analyze-lease", response_model=LeaseAnalysisResponse)
async def analyze_lease(request: LeaseAnalysisRequest) -> LeaseAnalysisResponse:
    """
    Analyze lease clauses against the TIE doctrine standard.

    Grades each clause A-D based on:
    - Presence of strong protective language
    - Absence of weak/unfavorable language
    - Essential elements coverage
    - Authority support

    Identifies missing clauses that every lease should contain.
    """
    analyses: List[ClauseAnalysis] = []
    for clause in request.clauses:
        analysis = _analyze_clause(clause, request.perspective)
        analyses.append(analysis)

    # Identify missing essential clauses
    provided_clause_names = {c.clause_name.lower().replace(" ", "_").replace("-", "_") for c in request.clauses}
    missing = [
        CLAUSE_GRADING_RUBRIC.get(c, {}).get("missing_protection", c)
        for c in ESSENTIAL_LEASE_CLAUSES
        if c not in provided_clause_names
    ]

    # Overall grade
    grades = [a.overall_grade for a in analyses if a.overall_grade != "UNGRADED"]
    grade_values = {"A": 4, "B": 3, "C": 2, "D": 1}
    if grades:
        avg = sum(grade_values.get(g, 2) for g in grades) / len(grades)
        if avg >= 3.5:
            overall = "A"
        elif avg >= 2.5:
            overall = "B"
        elif avg >= 1.5:
            overall = "C"
        else:
            overall = "D"
    else:
        overall = "UNGRADED"

    # Priority recommendations
    priority_recs: List[str] = []
    d_clauses = [a for a in analyses if a.overall_grade == "D"]
    if d_clauses:
        priority_recs.append(f"CRITICAL: Renegotiate {len(d_clauses)} clause(s) graded D: {', '.join(a.clause_name for a in d_clauses)}")
    if missing:
        priority_recs.append(f"ADD MISSING: {len(missing)} essential clause(s) not found in lease")
        for m in missing[:5]:
            priority_recs.append(f"  - Add {m}")

    return LeaseAnalysisResponse(
        clause_count=len(analyses),
        perspective=request.perspective,
        overall_grade=overall,
        clause_analyses=analyses,
        missing_clauses=missing,
        priority_recommendations=priority_recs,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


# ==============================================================================
# NEGOTIATION STRATEGY GENERATOR
# ==============================================================================

class NegotiationScenario(BaseModel):
    """Input for a negotiation strategy request."""
    mineral_acres: float = Field(..., gt=0, description="Net mineral acres under negotiation")
    basin: str = Field(default="permian_midland", description="Basin context")
    current_offers: Optional[List[Dict[str, Any]]] = Field(default=None, description="Current offers on the table")
    lessor_priorities: List[str] = Field(default_factory=lambda: ["royalty", "cost-free", "pugh"], description="Lessor's priority ranking")
    existing_production: bool = Field(default=False, description="Whether there is existing production nearby")
    competing_operators: int = Field(default=1, ge=1, description="Number of competing operators")
    surface_sensitivity: str = Field(default="low", description="Surface use sensitivity: low/medium/high")


class NegotiationStrategy(BaseModel):
    """Generated negotiation strategy."""
    engine_id: str = ENGINE_ID
    scenario_summary: str = ""
    leverage_assessment: str = ""
    leverage_score: float = Field(ge=0.0, le=10.0, default=5.0)
    recommended_terms: Dict[str, str] = {}
    opening_positions: Dict[str, str] = {}
    fallback_positions: Dict[str, str] = {}
    deal_breakers: List[str] = []
    trading_points: List[Dict[str, str]] = []
    estimated_bonus_range: Dict[str, float] = {}
    recommended_royalty: str = ""
    priority_clauses: List[str] = []
    warnings: List[str] = []
    timestamp: str = ""


# Basin-specific bonus ranges (per net mineral acre)
BASIN_BONUS_RANGES: Dict[str, Dict[str, float]] = {
    "permian_midland": {"low": 15000, "mid": 35000, "high": 75000},
    "permian_delaware": {"low": 10000, "mid": 25000, "high": 60000},
    "eagle_ford": {"low": 5000, "mid": 15000, "high": 40000},
    "haynesville": {"low": 3000, "mid": 10000, "high": 25000},
    "marcellus": {"low": 2000, "mid": 8000, "high": 20000},
    "bakken": {"low": 1000, "mid": 5000, "high": 15000},
    "scoop_stack": {"low": 2000, "mid": 8000, "high": 20000},
}

# Basin-specific royalty expectations
BASIN_ROYALTY_TARGETS: Dict[str, str] = {
    "permian_midland": "1/4 (25%)",
    "permian_delaware": "1/4 (25%)",
    "eagle_ford": "1/4 (25%)",
    "haynesville": "1/4 (25%)",
    "marcellus": "1/5 (20%)",
    "bakken": "3/16 (18.75%)",
    "scoop_stack": "1/5 (20%)",
}


def _generate_strategy(scenario: NegotiationScenario) -> NegotiationStrategy:
    """Generate a comprehensive negotiation strategy based on the scenario."""
    basin = scenario.basin
    acres = scenario.mineral_acres

    # Leverage assessment
    leverage_factors: List[str] = []
    leverage_score = 5.0

    if scenario.competing_operators > 2:
        leverage_factors.append(f"{scenario.competing_operators} competing operators create strong bidding environment")
        leverage_score += 1.5
    elif scenario.competing_operators == 1:
        leverage_factors.append("Single operator limits competitive leverage")
        leverage_score -= 1.0

    if acres >= 640:
        leverage_factors.append(f"Large acreage position ({acres} NMA) is highly attractive to operators")
        leverage_score += 1.0
    elif acres < 40:
        leverage_factors.append(f"Small acreage position ({acres} NMA) limits individual negotiation leverage")
        leverage_score -= 1.0

    if scenario.existing_production:
        leverage_factors.append("Existing nearby production proves geologic prospectivity")
        leverage_score += 1.0

    if basin in ("permian_midland", "permian_delaware"):
        leverage_factors.append("Permian Basin is the most active US play — strong lessor market")
        leverage_score += 0.5

    leverage_score = max(1.0, min(10.0, leverage_score))

    if leverage_score >= 7:
        leverage_assessment = "STRONG LEVERAGE — Lessor is in a commanding negotiation position"
    elif leverage_score >= 5:
        leverage_assessment = "MODERATE LEVERAGE — Balanced negotiation with room for favorable terms"
    else:
        leverage_assessment = "LIMITED LEVERAGE — Focus on essential protections over premium economics"

    # Bonus range
    bonus_range = BASIN_BONUS_RANGES.get(basin, {"low": 2000, "mid": 10000, "high": 30000})
    if leverage_score >= 7:
        estimated_bonus = {"low": bonus_range["mid"], "high": bonus_range["high"]}
    elif leverage_score >= 5:
        estimated_bonus = {"low": bonus_range["low"], "high": bonus_range["mid"]}
    else:
        estimated_bonus = {"low": bonus_range["low"] * 0.7, "high": bonus_range["low"] * 1.5}

    # Recommended royalty
    target_royalty = BASIN_ROYALTY_TARGETS.get(basin, "1/5 (20%)")

    # Recommended terms
    recommended: Dict[str, str] = {
        "royalty_rate": f"{target_royalty} cost-free royalty",
        "primary_term": "3 years" if basin in ("permian_midland", "permian_delaware") else "5 years",
        "pugh_clause": "Both vertical and horizontal Pugh with automatic release",
        "pooling_limit": "640 acres maximum or RRC spacing plus 10%",
        "surface_protection": "Full surface damage payments, location approval, and restoration" if scenario.surface_sensitivity != "low" else "Standard surface damage payments",
        "cessation_clause": "60-day cessation period with operations requirement",
        "shut_in_limit": "2-year cumulative maximum with annual payments",
        "assignment_restriction": "30-day notice, consent not unreasonably withheld",
        "environmental_indemnity": "Comprehensive indemnification surviving lease termination",
        "audit_rights": "Annual audit right with cost recovery for underpayments exceeding 5%",
        "depth_limitation": "100 feet below deepest target formation",
        "continuous_drilling": "One well per 640 acres per year, 180-day maximum gap" if acres >= 640 else "N/A for small tracts",
    }

    # Opening positions (aspirational)
    opening: Dict[str, str] = {
        "royalty_rate": "1/4 cost-free at point of sale",
        "bonus": f"${estimated_bonus['high']:,.0f}/NMA",
        "primary_term": "3 years",
        "pugh": "Full vertical and horizontal Pugh",
    }

    # Fallback positions (minimum acceptable)
    fallback: Dict[str, str] = {
        "royalty_rate": "3/16 cost-free" if leverage_score < 5 else "1/5 cost-free",
        "bonus": f"${estimated_bonus['low']:,.0f}/NMA",
        "primary_term": "5 years with continuous drilling clause",
    }

    # Deal breakers
    deal_breakers: List[str] = [
        "No cost-free royalty language",
        "Royalty below 1/8 (12.5%)",
        "No Pugh clause on large acreage positions",
        "Unlimited pooling authority",
        "Primary term exceeding 10 years without continuous drilling",
    ]

    # Trading points
    trading_points: List[Dict[str, str]] = [
        {"give": "Accept 3/16 royalty instead of 1/4", "get": "Comprehensive cost-free language"},
        {"give": "Accept 5-year primary term", "get": "Continuous drilling clause with annual well commitment"},
        {"give": "Allow pooling up to 640 acres", "get": "Full Pugh clause with automatic release"},
        {"give": "Lower bonus per acre", "get": "Higher royalty rate (royalty > bonus for long-term value)"},
        {"give": "Accept shut-in clause", "get": "2-year cumulative limit with meaningful annual payment"},
    ]

    # Priority clauses from lessor priorities
    priority_clauses: List[str] = []
    for p in scenario.lessor_priorities:
        if p in engine._doctrine_cache or any(p in k for k in engine._doctrine_cache.keys()):
            priority_clauses.append(p)
    if not priority_clauses:
        priority_clauses = ["royalty_rate_negotiation", "cost_free_royalty", "pugh_clause"]

    # Warnings
    warnings: List[str] = []
    if scenario.surface_sensitivity == "high":
        warnings.append("High surface sensitivity — negotiate no-surface-operations clause or comprehensive surface protections")
    if acres >= 1280 and "continuous_drilling" not in scenario.lessor_priorities:
        warnings.append("Large acreage without continuous drilling priority — risk of operator warehousing acreage")
    if scenario.competing_operators <= 1:
        warnings.append("Single operator — limited competitive leverage; focus on protective clauses over premium economics")

    return NegotiationStrategy(
        scenario_summary=(
            f"Negotiation for {acres:.1f} NMA in {basin.replace('_', ' ').title()}. "
            f"{scenario.competing_operators} competing operator(s). "
            f"{'Existing' if scenario.existing_production else 'No'} nearby production. "
            f"Surface sensitivity: {scenario.surface_sensitivity}."
        ),
        leverage_assessment=leverage_assessment,
        leverage_score=round(leverage_score, 1),
        recommended_terms=recommended,
        opening_positions=opening,
        fallback_positions=fallback,
        deal_breakers=deal_breakers,
        trading_points=trading_points,
        estimated_bonus_range=estimated_bonus,
        recommended_royalty=target_royalty,
        priority_clauses=priority_clauses,
        warnings=warnings,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


@app.post("/strategy", response_model=NegotiationStrategy)
async def generate_negotiation_strategy(scenario: NegotiationScenario) -> NegotiationStrategy:
    """
    Generate a comprehensive lease negotiation strategy.

    Takes mineral acreage, basin, competition level, and priorities
    to produce recommended terms, opening/fallback positions,
    deal breakers, and trading points.
    """
    return _generate_strategy(scenario)


# ==============================================================================
# CLAUSE COMPARISON ENDPOINT
# ==============================================================================

class ClauseComparisonRequest(BaseModel):
    """Compare two versions of a lease clause."""
    clause_name: str
    version_a: str = Field(..., description="First version of the clause")
    version_b: str = Field(..., description="Second version of the clause")
    perspective: str = Field(default="lessor", description="lessor or lessee")


class ClauseComparisonResponse(BaseModel):
    """Clause comparison result."""
    engine_id: str = ENGINE_ID
    clause_name: str
    version_a_grade: str = ""
    version_b_grade: str = ""
    preferred_version: str = ""
    differences: List[str] = []
    version_a_analysis: ClauseAnalysis = ClauseAnalysis(clause_name="")
    version_b_analysis: ClauseAnalysis = ClauseAnalysis(clause_name="")
    recommendation: str = ""
    timestamp: str = ""


@app.post("/compare-clauses", response_model=ClauseComparisonResponse)
async def compare_clauses(request: ClauseComparisonRequest) -> ClauseComparisonResponse:
    """Compare two versions of a lease clause and recommend the stronger version."""
    clause_a = LeaseClauseInput(clause_name=request.clause_name, clause_text=request.version_a)
    clause_b = LeaseClauseInput(clause_name=request.clause_name, clause_text=request.version_b)

    analysis_a = _analyze_clause(clause_a, request.perspective)
    analysis_b = _analyze_clause(clause_b, request.perspective)

    # Determine preferred version
    grade_values = {"A": 4, "B": 3, "C": 2, "D": 1, "UNGRADED": 0}
    score_a = grade_values.get(analysis_a.overall_grade, 0)
    score_b = grade_values.get(analysis_b.overall_grade, 0)

    if score_a > score_b:
        preferred = "version_a"
        recommendation = f"Version A is preferred ({analysis_a.overall_grade} vs {analysis_b.overall_grade}). "
    elif score_b > score_a:
        preferred = "version_b"
        recommendation = f"Version B is preferred ({analysis_b.overall_grade} vs {analysis_a.overall_grade}). "
    else:
        # Equal grades — prefer the one with more strengths
        if len(analysis_a.strengths) > len(analysis_b.strengths):
            preferred = "version_a"
            recommendation = "Both versions grade equally but Version A has more protective language. "
        elif len(analysis_b.strengths) > len(analysis_a.strengths):
            preferred = "version_b"
            recommendation = "Both versions grade equally but Version B has more protective language. "
        else:
            preferred = "either"
            recommendation = "Both versions are substantially equivalent. "

    # Identify differences
    differences: List[str] = []
    a_strengths = set(s for s in analysis_a.strengths)
    b_strengths = set(s for s in analysis_b.strengths)
    only_a = a_strengths - b_strengths
    only_b = b_strengths - a_strengths
    if only_a:
        differences.append(f"Version A exclusively contains: {', '.join(list(only_a)[:3])}")
    if only_b:
        differences.append(f"Version B exclusively contains: {', '.join(list(only_b)[:3])}")
    a_weak = set(w for w in analysis_a.weaknesses)
    b_weak = set(w for w in analysis_b.weaknesses)
    if a_weak - b_weak:
        differences.append(f"Version A has weaknesses not in B: {', '.join(list(a_weak - b_weak)[:3])}")
    if b_weak - a_weak:
        differences.append(f"Version B has weaknesses not in A: {', '.join(list(b_weak - a_weak)[:3])}")

    recommendation += f"Key differences: {len(differences)} identified."

    return ClauseComparisonResponse(
        clause_name=request.clause_name,
        version_a_grade=analysis_a.overall_grade,
        version_b_grade=analysis_b.overall_grade,
        preferred_version=preferred,
        differences=differences,
        version_a_analysis=analysis_a,
        version_b_analysis=analysis_b,
        recommendation=recommendation,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


# ==============================================================================
# ROYALTY CALCULATOR
# ==============================================================================

class RoyaltyCalculationRequest(BaseModel):
    """Royalty calculation input."""
    monthly_oil_bbls: float = Field(default=0.0, ge=0, description="Monthly oil production in barrels")
    monthly_gas_mcf: float = Field(default=0.0, ge=0, description="Monthly gas production in MCF")
    monthly_ngl_bbls: float = Field(default=0.0, ge=0, description="Monthly NGL production in barrels")
    oil_price_per_bbl: float = Field(default=70.0, gt=0, description="Oil price per barrel")
    gas_price_per_mcf: float = Field(default=3.0, gt=0, description="Gas price per MCF")
    ngl_price_per_bbl: float = Field(default=25.0, gt=0, description="NGL price per barrel")
    royalty_fraction: float = Field(default=0.25, gt=0, le=1.0, description="Royalty fraction (e.g., 0.25 for 1/4)")
    net_mineral_acres: float = Field(default=640.0, gt=0, description="Net mineral acres in the unit")
    unit_acres: float = Field(default=640.0, gt=0, description="Total unit acres")
    post_production_costs_per_mcf: float = Field(default=0.0, ge=0, description="Post-production cost deductions per MCF (0 if cost-free)")
    post_production_costs_per_bbl: float = Field(default=0.0, ge=0, description="Post-production cost deductions per barrel oil")


class RoyaltyCalculationResponse(BaseModel):
    """Royalty calculation result."""
    engine_id: str = ENGINE_ID
    mineral_interest_fraction: float = 0.0
    gross_oil_revenue: float = 0.0
    gross_gas_revenue: float = 0.0
    gross_ngl_revenue: float = 0.0
    total_gross_revenue: float = 0.0
    post_production_deductions_oil: float = 0.0
    post_production_deductions_gas: float = 0.0
    net_revenue_after_deductions: float = 0.0
    royalty_fraction: float = 0.0
    mineral_interest_royalty: float = 0.0
    monthly_royalty: float = 0.0
    annual_royalty_estimate: float = 0.0
    cost_free_vs_deducted_delta: float = 0.0
    effective_royalty_rate: float = 0.0
    notes: List[str] = []
    timestamp: str = ""


@app.post("/calculate-royalty", response_model=RoyaltyCalculationResponse)
async def calculate_royalty(request: RoyaltyCalculationRequest) -> RoyaltyCalculationResponse:
    """
    Calculate monthly and annual royalty payments with and without post-production deductions.
    Demonstrates the financial impact of cost-free vs. proceeds-based royalty language.
    """
    mi_fraction = request.net_mineral_acres / request.unit_acres

    gross_oil = request.monthly_oil_bbls * request.oil_price_per_bbl
    gross_gas = request.monthly_gas_mcf * request.gas_price_per_mcf
    gross_ngl = request.monthly_ngl_bbls * request.ngl_price_per_bbl
    total_gross = gross_oil + gross_gas + gross_ngl

    deductions_oil = request.monthly_oil_bbls * request.post_production_costs_per_bbl
    deductions_gas = request.monthly_gas_mcf * request.post_production_costs_per_mcf
    total_deductions = deductions_oil + deductions_gas

    net_revenue = total_gross - total_deductions

    # Royalty on net (after deductions)
    royalty_on_net = net_revenue * request.royalty_fraction * mi_fraction

    # Royalty on gross (cost-free)
    royalty_on_gross = total_gross * request.royalty_fraction * mi_fraction

    # Delta shows value of cost-free language
    cost_free_delta = royalty_on_gross - royalty_on_net

    # Effective royalty rate after deductions
    effective_rate = (royalty_on_net / total_gross * 100) if total_gross > 0 else 0.0

    notes: List[str] = []
    if cost_free_delta > 0:
        pct_impact = (cost_free_delta / royalty_on_gross * 100) if royalty_on_gross > 0 else 0
        notes.append(
            f"Cost-free royalty language would save ${cost_free_delta:,.2f}/month "
            f"({pct_impact:.1f}% royalty value protection)"
        )
        notes.append(
            f"Annual impact of cost-free language: ${cost_free_delta * 12:,.2f}/year"
        )
    if effective_rate < request.royalty_fraction * 100 * 0.8:
        notes.append(
            f"WARNING: Effective royalty rate ({effective_rate:.1f}%) is significantly below "
            f"stated rate ({request.royalty_fraction * 100:.1f}%) due to post-production deductions"
        )
    if request.post_production_costs_per_mcf == 0 and request.post_production_costs_per_bbl == 0:
        notes.append("Cost-free royalty: no post-production deductions applied")

    return RoyaltyCalculationResponse(
        mineral_interest_fraction=round(mi_fraction, 6),
        gross_oil_revenue=round(gross_oil, 2),
        gross_gas_revenue=round(gross_gas, 2),
        gross_ngl_revenue=round(gross_ngl, 2),
        total_gross_revenue=round(total_gross, 2),
        post_production_deductions_oil=round(deductions_oil, 2),
        post_production_deductions_gas=round(deductions_gas, 2),
        net_revenue_after_deductions=round(net_revenue, 2),
        royalty_fraction=request.royalty_fraction,
        mineral_interest_royalty=round(royalty_on_net, 2),
        monthly_royalty=round(royalty_on_net, 2),
        annual_royalty_estimate=round(royalty_on_net * 12, 2),
        cost_free_vs_deducted_delta=round(cost_free_delta, 2),
        effective_royalty_rate=round(effective_rate, 2),
        notes=notes,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


# ==============================================================================
# LEASE TERM TIMELINE ENDPOINT
# ==============================================================================

class LeaseTimelineRequest(BaseModel):
    """Input for lease term timeline visualization."""
    execution_date: str = Field(..., description="Lease execution date (YYYY-MM-DD)")
    primary_term_years: int = Field(default=3, ge=1, le=20)
    has_extension_option: bool = Field(default=False)
    extension_years: int = Field(default=0, ge=0, le=10)
    has_continuous_drilling: bool = Field(default=False)
    drilling_gap_days: int = Field(default=180, ge=30, le=365)
    has_cessation_clause: bool = Field(default=True)
    cessation_days: int = Field(default=90, ge=30, le=365)
    has_shut_in: bool = Field(default=True)
    shut_in_max_years: int = Field(default=2, ge=1, le=5)


class TimelineEvent(BaseModel):
    """A single event on the lease timeline."""
    date: str
    event: str
    description: str
    action_required: str
    critical: bool = False


@app.post("/timeline")
async def generate_timeline(request: LeaseTimelineRequest) -> Dict[str, Any]:
    """Generate a lease term timeline with critical dates and action items."""
    from datetime import timedelta

    try:
        exec_date = datetime.strptime(request.execution_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    events: List[Dict[str, Any]] = []

    # Execution date
    events.append({
        "date": exec_date.strftime("%Y-%m-%d"),
        "event": "Lease Execution",
        "description": "Lease signed and primary term begins.",
        "action_required": "Record lease at county clerk's office.",
        "critical": True,
    })

    # Primary term milestones
    pt_end = exec_date + timedelta(days=request.primary_term_years * 365)

    # Annual anniversaries
    for year in range(1, request.primary_term_years + 1):
        anniversary = exec_date + timedelta(days=year * 365)
        events.append({
            "date": anniversary.strftime("%Y-%m-%d"),
            "event": f"Year {year} Anniversary",
            "description": f"Primary term year {year} of {request.primary_term_years}.",
            "action_required": "Review development status and operator compliance.",
            "critical": year == request.primary_term_years,
        })

    # 6-month warning before primary term expiration
    warning_date = pt_end - timedelta(days=180)
    events.append({
        "date": warning_date.strftime("%Y-%m-%d"),
        "event": "6-Month Primary Term Warning",
        "description": "Primary term expires in 6 months.",
        "action_required": "Evaluate operator development status. Consider top lease if no activity.",
        "critical": True,
    })

    # Primary term expiration
    events.append({
        "date": pt_end.strftime("%Y-%m-%d"),
        "event": "Primary Term Expiration",
        "description": "Lease expires unless held by production, operations, or extension.",
        "action_required": "Verify lease status — producing, operating, or expired. Record release if expired.",
        "critical": True,
    })

    # Extension option
    if request.has_extension_option and request.extension_years > 0:
        ext_end = pt_end + timedelta(days=request.extension_years * 365)
        events.append({
            "date": pt_end.strftime("%Y-%m-%d"),
            "event": "Extension Option Deadline",
            "description": f"Operator may extend for {request.extension_years} year(s) with additional consideration.",
            "action_required": "Negotiate extension terms — demand improved royalty and protective clauses.",
            "critical": True,
        })

    # Continuous drilling milestones
    if request.has_continuous_drilling:
        gap_days = request.drilling_gap_days
        for i in range(1, min(request.primary_term_years * 2, 10)):
            drill_deadline = exec_date + timedelta(days=i * gap_days)
            if drill_deadline > pt_end:
                break
            events.append({
                "date": drill_deadline.strftime("%Y-%m-%d"),
                "event": f"Continuous Drilling Deadline #{i}",
                "description": f"Next well must spud within {gap_days} days of previous completion.",
                "action_required": "Monitor operator drilling activity. Release acreage if non-compliant.",
                "critical": False,
            })

    # Sort by date
    events.sort(key=lambda x: x["date"])

    return {
        "engine_id": ENGINE_ID,
        "execution_date": request.execution_date,
        "primary_term_expiration": pt_end.strftime("%Y-%m-%d"),
        "total_events": len(events),
        "critical_events": sum(1 for e in events if e["critical"]),
        "timeline": events,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ==============================================================================
# LEASE CHECKLIST GENERATOR
# ==============================================================================

class ChecklistRequest(BaseModel):
    """Request for a lease negotiation checklist."""
    acreage_type: str = Field(default="private", description="private, state, federal")
    basin: str = Field(default="permian_midland")
    perspective: str = Field(default="lessor", description="lessor or lessee")
    surface_sensitivity: str = Field(default="medium", description="low, medium, high")
    acreage_size: str = Field(default="medium", description="small (<80 NMA), medium (80-640), large (640+)")


class ChecklistItem(BaseModel):
    """Single checklist item."""
    category: str
    item: str
    priority: str = "HIGH"
    doctrine_reference: Optional[str] = None
    notes: str = ""
    completed: bool = False


CHECKLIST_TEMPLATES: Dict[str, List[Dict[str, Any]]] = {
    "pre_negotiation": [
        {"item": "Obtain current ownership report / title opinion", "priority": "CRITICAL", "notes": "Confirm mineral ownership chain and net mineral acres"},
        {"item": "Research comparable lease terms in the county", "priority": "CRITICAL", "notes": "County clerk records, recent bonus and royalty data"},
        {"item": "Identify all competing operators seeking leases", "priority": "HIGH", "notes": "Multiple offers create leverage"},
        {"item": "Verify surface ownership and any existing surface use agreements", "priority": "HIGH", "notes": "Critical if mineral and surface are severed"},
        {"item": "Review any existing leases or top leases on the property", "priority": "HIGH", "notes": "Check for unexpired prior leases"},
        {"item": "Consult oil and gas attorney for lease review", "priority": "CRITICAL", "notes": "Never sign without attorney review"},
        {"item": "Determine priority ranking of negotiation objectives", "priority": "HIGH", "notes": "Royalty > cost-free > Pugh > surface > other"},
        {"item": "Review operator financial strength and operational track record", "priority": "MEDIUM", "notes": "Publicly available data, RRC records"},
        {"item": "Assess geologic prospectivity from public well data", "priority": "MEDIUM", "notes": "RRC completion reports, DrillingInfo/Enverus"},
        {"item": "Prepare lessor addendum with all protective provisions", "priority": "CRITICAL", "notes": "Never rely on printed form lease alone"},
    ],
    "economic_terms": [
        {"item": "Negotiate royalty rate at or above basin market rate", "priority": "CRITICAL", "doctrine": "royalty_rate_negotiation"},
        {"item": "Include comprehensive cost-free royalty language", "priority": "CRITICAL", "doctrine": "cost_free_royalty"},
        {"item": "Negotiate bonus at or above comparable market rate", "priority": "HIGH", "doctrine": "bonus_consideration"},
        {"item": "Specify market value valuation (not proceeds)", "priority": "HIGH", "doctrine": "market_value_vs_proceeds"},
        {"item": "Include market enhancement clause for affiliate sales", "priority": "HIGH", "doctrine": "market_enhancement_clause"},
        {"item": "Ensure royalty covers all gas products (residue + NGLs)", "priority": "HIGH", "doctrine": "gas_royalty_valuation"},
        {"item": "Negotiate audit rights with cost recovery", "priority": "MEDIUM", "doctrine": "audit_rights"},
    ],
    "term_and_development": [
        {"item": "Set primary term at 3 years (or 5 max with CDC)", "priority": "HIGH", "doctrine": "primary_term_selection"},
        {"item": "Strengthen habendum with paying quantities requirement", "priority": "HIGH", "doctrine": "habendum_clause"},
        {"item": "Include continuous drilling clause for large acreage", "priority": "HIGH", "doctrine": "continuous_drilling_clause"},
        {"item": "Define commencement of drilling strictly (actual spudding)", "priority": "MEDIUM", "doctrine": "commencement_of_drilling"},
        {"item": "Include operations clause with good faith requirement", "priority": "MEDIUM", "doctrine": "operations_clause"},
        {"item": "Limit cessation of production savings period to 60-90 days", "priority": "HIGH", "doctrine": "cessation_of_production"},
        {"item": "Limit shut-in royalty to 2-year cumulative maximum", "priority": "HIGH", "doctrine": "shut_in_royalty"},
    ],
    "acreage_protection": [
        {"item": "Include horizontal Pugh clause with automatic release", "priority": "CRITICAL", "doctrine": "pugh_clause"},
        {"item": "Include vertical Pugh clause for depth severance", "priority": "CRITICAL", "doctrine": "pugh_clause"},
        {"item": "Add depth limitation for unproduced formations", "priority": "HIGH", "doctrine": "depth_limitation"},
        {"item": "Limit pooling unit size to RRC spacing plus 10%", "priority": "HIGH", "doctrine": "pooling_unitization"},
        {"item": "Include automatic release provisions with recording deadline", "priority": "HIGH", "doctrine": "release_provisions"},
        {"item": "Address horizontal well production allocation", "priority": "MEDIUM", "doctrine": "horizontal_well_considerations"},
    ],
    "surface_and_environmental": [
        {"item": "Negotiate surface damage payment schedule", "priority": "HIGH", "doctrine": "surface_use_provisions"},
        {"item": "Include location approval rights for well pads", "priority": "HIGH", "doctrine": "surface_use_provisions"},
        {"item": "Require surface restoration obligations", "priority": "HIGH", "doctrine": "surface_use_provisions"},
        {"item": "Include environmental indemnification surviving termination", "priority": "HIGH", "doctrine": "environmental_indemnification"},
        {"item": "Protect water rights with separate use agreement", "priority": "HIGH", "doctrine": "water_rights_protection"},
        {"item": "Include setback requirements from improvements", "priority": "MEDIUM", "doctrine": "surface_use_provisions"},
    ],
    "legal_protections": [
        {"item": "Add assignment restrictions with consent requirement", "priority": "HIGH", "doctrine": "assignment_restrictions"},
        {"item": "Consider ROFR on proposed lease assignments", "priority": "MEDIUM", "doctrine": "assignment_restrictions"},
        {"item": "Make implied covenants express in the lease", "priority": "MEDIUM", "doctrine": "implied_covenants"},
        {"item": "Evaluate top lease opportunities for expiring leases", "priority": "MEDIUM", "doctrine": "top_lease_strategy"},
        {"item": "Address force pooling protection with lease pooling terms", "priority": "MEDIUM", "doctrine": "force_pooling_defense"},
    ],
    "post_execution": [
        {"item": "Record lease at county clerk's office", "priority": "CRITICAL", "notes": "Unrecorded leases are not constructive notice to third parties"},
        {"item": "Set calendar reminders for all critical dates", "priority": "HIGH", "notes": "Primary term expiration, annual anniversaries, CDC deadlines"},
        {"item": "Monitor operator activity through RRC filings", "priority": "MEDIUM", "notes": "Drilling permits, completion reports, production data"},
        {"item": "Verify first royalty payment and check calculation", "priority": "HIGH", "notes": "Compare against lease terms and current prices"},
        {"item": "Schedule annual audit of royalty payments", "priority": "MEDIUM", "notes": "Exercise audit rights per lease terms"},
        {"item": "Monitor for lease expiration and demand release recording", "priority": "HIGH", "notes": "Operator must record release within 60 days"},
    ],
}


@app.post("/checklist")
async def generate_checklist(request: ChecklistRequest) -> Dict[str, Any]:
    """
    Generate a comprehensive lease negotiation checklist customized for the scenario.
    Covers pre-negotiation, economic terms, term/development, acreage protection,
    surface/environmental, legal protections, and post-execution steps.
    """
    categories_output: Dict[str, List[Dict[str, Any]]] = {}
    total_items = 0
    critical_count = 0

    for category, items in CHECKLIST_TEMPLATES.items():
        category_items: List[Dict[str, Any]] = []
        for item_data in items:
            checklist_item = {
                "item": item_data["item"],
                "priority": item_data.get("priority", "MEDIUM"),
                "doctrine_reference": item_data.get("doctrine"),
                "notes": item_data.get("notes", ""),
                "completed": False,
            }

            # Adjust for acreage size
            if request.acreage_size == "small" and "large acreage" in item_data["item"].lower():
                checklist_item["priority"] = "LOW"
                checklist_item["notes"] += " (less critical for small tracts)"

            # Adjust for surface sensitivity
            if request.surface_sensitivity == "high" and category == "surface_and_environmental":
                if checklist_item["priority"] == "MEDIUM":
                    checklist_item["priority"] = "HIGH"

            # Adjust for federal/state leases
            if request.acreage_type in ("federal", "state"):
                if "bonus" in item_data["item"].lower() or "royalty rate" in item_data["item"].lower():
                    checklist_item["notes"] += f" ({request.acreage_type} leases have fixed terms — limited negotiation)"

            category_items.append(checklist_item)
            total_items += 1
            if checklist_item["priority"] == "CRITICAL":
                critical_count += 1

        categories_output[category] = category_items

    return {
        "engine_id": ENGINE_ID,
        "checklist_type": f"{request.perspective}_{request.acreage_type}_lease",
        "basin": request.basin,
        "perspective": request.perspective,
        "total_items": total_items,
        "critical_items": critical_count,
        "categories": categories_output,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


# ==============================================================================
# DOCTRINE INTERACTION GRAPH
# ==============================================================================

@app.get("/interaction-graph")
async def get_interaction_graph() -> Dict[str, Any]:
    """
    Return the full doctrine interaction graph showing how lease negotiation
    issues interconnect and influence each other.
    """
    nodes: List[Dict[str, Any]] = []
    for category in IssueCategory:
        if category == IssueCategory.GENERAL:
            continue
        # Find matching doctrine blocks
        matching_blocks = [
            topic for topic in engine._doctrine_cache.keys()
            if category.value in topic
        ]
        nodes.append({
            "id": category.value,
            "label": category.value.replace("_", " ").title(),
            "doctrine_count": len(matching_blocks),
            "doctrines": matching_blocks,
        })

    edges: List[Dict[str, Any]] = []
    for cat_a, cat_b, relationship in IssueDecomposer.INTERACTION_EDGES:
        edges.append({
            "source": cat_a.value,
            "target": cat_b.value,
            "relationship": relationship,
            "label": relationship.replace("_", " ").title(),
        })

    return {
        "engine_id": ENGINE_ID,
        "node_count": len(nodes),
        "edge_count": len(edges),
        "nodes": nodes,
        "edges": edges,
        "description": (
            "Doctrine interaction graph showing how lease negotiation issues "
            "interconnect. Edges represent cross-doctrine dependencies that must "
            "be considered during holistic lease review."
        ),
    }


# ==============================================================================
# BASIN MARKET DATA ENDPOINT
# ==============================================================================

BASIN_MARKET_DATA: Dict[str, Dict[str, Any]] = {
    "permian_midland": {
        "basin_name": "Permian Basin - Midland",
        "state": "Texas",
        "typical_royalty": "22-25%",
        "typical_bonus_per_nma": "$15,000-$75,000",
        "typical_primary_term": "3 years",
        "key_formations": ["Wolfcamp A", "Wolfcamp B", "Spraberry", "Cline"],
        "key_counties": ["Midland", "Martin", "Howard", "Reagan", "Upton", "Glasscock"],
        "active_operators": ["Pioneer", "Diamondback", "ConocoPhillips", "Chevron", "Exxon"],
        "development_pace": "Very Active — multiple rigs per operator",
        "cost_free_prevalence": "Standard in negotiated leases",
        "pugh_clause_prevalence": "Expected in all negotiated leases",
        "notes": "Most competitive leasing market in the US. Lessor leverage is strong.",
    },
    "permian_delaware": {
        "basin_name": "Permian Basin - Delaware",
        "state": "Texas/New Mexico",
        "typical_royalty": "22-25%",
        "typical_bonus_per_nma": "$10,000-$60,000",
        "typical_primary_term": "3 years",
        "key_formations": ["Wolfcamp", "Bone Spring", "Avalon"],
        "key_counties": ["Reeves", "Loving", "Ward", "Pecos", "Culberson", "Lea (NM)", "Eddy (NM)"],
        "active_operators": ["Oxy", "Devon", "Apache", "Chevron", "ConocoPhillips"],
        "development_pace": "Very Active",
        "cost_free_prevalence": "Standard",
        "pugh_clause_prevalence": "Expected",
        "notes": "Thick pay zones and stacked targets make depth limitations critical.",
    },
    "eagle_ford": {
        "basin_name": "Eagle Ford Shale",
        "state": "Texas",
        "typical_royalty": "22-25%",
        "typical_bonus_per_nma": "$5,000-$40,000",
        "typical_primary_term": "3-5 years",
        "key_formations": ["Eagle Ford", "Austin Chalk"],
        "key_counties": ["Dimmit", "La Salle", "Webb", "Karnes", "DeWitt", "McMullen"],
        "active_operators": ["EOG", "Marathon", "ConocoPhillips", "SM Energy"],
        "development_pace": "Active — focus on infill drilling",
        "cost_free_prevalence": "Common",
        "pugh_clause_prevalence": "Common",
        "notes": "Mature play with established market rates. Oil window commands premium.",
    },
    "haynesville": {
        "basin_name": "Haynesville Shale",
        "state": "Louisiana/Texas",
        "typical_royalty": "20-25%",
        "typical_bonus_per_nma": "$3,000-$25,000",
        "typical_primary_term": "3-5 years",
        "key_formations": ["Haynesville", "Bossier"],
        "key_counties": ["Caddo Parish", "DeSoto Parish", "Red River Parish", "Harrison Co. (TX)"],
        "active_operators": ["Chesapeake", "Southwestern Energy", "Comstock", "Aethon"],
        "development_pace": "Active — driven by LNG export demand",
        "cost_free_prevalence": "Growing — Louisiana courts less favorable than Texas",
        "pugh_clause_prevalence": "Named after Louisiana practice — very common",
        "notes": "Dry gas play; economics tied to gas prices and LNG demand.",
    },
    "marcellus": {
        "basin_name": "Marcellus Shale",
        "state": "Pennsylvania/West Virginia",
        "typical_royalty": "15-20%",
        "typical_bonus_per_nma": "$2,000-$20,000",
        "typical_primary_term": "5 years",
        "key_formations": ["Marcellus", "Utica"],
        "key_counties": ["Susquehanna", "Bradford", "Greene", "Washington"],
        "active_operators": ["EQT", "Range Resources", "Coterra", "CNX"],
        "development_pace": "Moderate — constrained by pipeline capacity",
        "cost_free_prevalence": "Less common — PA law more operator-friendly",
        "pugh_clause_prevalence": "Less common — negotiate explicitly",
        "notes": "Pipeline takeaway constraints affect development timing.",
    },
    "bakken": {
        "basin_name": "Bakken/Three Forks",
        "state": "North Dakota/Montana",
        "typical_royalty": "18-20%",
        "typical_bonus_per_nma": "$1,000-$15,000",
        "typical_primary_term": "5 years",
        "key_formations": ["Bakken", "Three Forks"],
        "key_counties": ["McKenzie", "Williams", "Mountrail", "Dunn"],
        "active_operators": ["Hess", "Continental", "Whiting", "Marathon"],
        "development_pace": "Moderate — rebound from 2020 downturn",
        "cost_free_prevalence": "Varies — negotiate explicitly",
        "pugh_clause_prevalence": "Less common — important to include",
        "notes": "ND has statutory 1/6 minimum for force-pooled interests.",
    },
    "scoop_stack": {
        "basin_name": "SCOOP/STACK/Merge",
        "state": "Oklahoma",
        "typical_royalty": "20-22%",
        "typical_bonus_per_nma": "$2,000-$20,000",
        "typical_primary_term": "3-5 years",
        "key_formations": ["Woodford", "Meramec", "Osage"],
        "key_counties": ["Blaine", "Canadian", "Grady", "Kingfisher"],
        "active_operators": ["Continental", "Devon", "Marathon", "Ovintiv"],
        "development_pace": "Moderate",
        "cost_free_prevalence": "Growing",
        "pugh_clause_prevalence": "Common",
        "notes": "Oklahoma has strong force pooling statute — lease terms should match or exceed statutory minimums.",
    },
}


@app.get("/market-data/{basin}")
async def get_basin_market_data(basin: str) -> Dict[str, Any]:
    """
    Return current market data for a specific basin including typical
    royalty rates, bonus ranges, and lease term expectations.
    """
    data = BASIN_MARKET_DATA.get(basin)
    if not data:
        available = list(BASIN_MARKET_DATA.keys())
        raise HTTPException(
            status_code=404,
            detail=f"Basin not found: {basin}. Available: {', '.join(available)}",
        )
    return {
        "engine_id": ENGINE_ID,
        "basin": basin,
        "market_data": data,
        "disclaimer": (
            "Market data represents typical ranges based on industry knowledge. "
            "Actual terms vary by specific location, acreage quality, and market conditions. "
            "Always verify with current comparable lease data from county records."
        ),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/market-data")
async def list_basin_market_data() -> Dict[str, Any]:
    """List all available basin market data."""
    summary: List[Dict[str, str]] = []
    for basin_key, data in BASIN_MARKET_DATA.items():
        summary.append({
            "basin_id": basin_key,
            "basin_name": data["basin_name"],
            "state": data["state"],
            "typical_royalty": data["typical_royalty"],
            "typical_bonus": data["typical_bonus_per_nma"],
        })
    return {
        "engine_id": ENGINE_ID,
        "basin_count": len(summary),
        "basins": summary,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ==============================================================================
# MAIN ENTRYPOINT
# ==============================================================================

if __name__ == "__main__":
    import uvicorn
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    uvicorn.run(
        "engine:app",
        host="0.0.0.0",
        port=ENGINE_PORT,
        log_level="info",
        reload=False,
    )
