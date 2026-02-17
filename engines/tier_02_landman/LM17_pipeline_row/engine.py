"""
LM17 Pipeline ROW Engine
==========================
Pipeline right-of-way acquisition, routing, easement negotiation,
FERC compliance, eminent domain, environmental permitting, pipeline
safety, and landowner dispute resolution intelligence engine.

Engine ID: LM17 | Port: 8517 | Version: 1.0.0
TIE-20 Gold Standard Implementation

Components:
  1.  three_layer_response
  2.  response_modes (FAST / DEFENSE / MEMO)
  3.  doctrine_cache (45 blocks)
  4.  authority_hardening
  5.  confidence_stratification
  6.  semantic_normalization
  7.  vector_search (keyword-based fallback)
  8.  telemetry
  9.  drift_watcher
  10. coverage_map
  11. metrics_collector
  12. health_endpoint
  13. zoned_analysis (PLANNING / REPORTING / AUDIT)
  14. fact_fragility_scoring
  15. audit_trail_jsonl
  16. determinism_hash_sha256
  17. fastapi_server
  18. loguru_logging
  19. multi_doctrine_decomposition
  20. deep_analysis_mode
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import sys
import time
import traceback
import uuid
from collections import defaultdict
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Optional

# Ensure _shared is in path for cloud_retriever
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_shared"))

import uvicorn
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Local imports
# ---------------------------------------------------------------------------

# Ensure sibling modules are importable
ENGINE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ENGINE_DIR))
from doctrines import (
    DOCTRINE_CACHE,
    BurdenHolder,
    ConfidenceLevel,
    DoctrineBlock,
    IssueCategory,
    PositionZone,
    get_all_categories,
    get_all_topics,
    get_doctrine_by_topic,
    get_doctrine_cache,
    get_doctrine_topic_keyword_map,
    get_doctrines_by_category,
)
from search import PipelineROWSearchEngine, SearchDocument, SearchResponse
from semantic import NormalizationMode, NormalizationResult, PipelineROWNormalizer
from telemetry import (
    ENGINE_ID,
    ENGINE_NAME,
    ENGINE_VERSION,
    ErrorDomain,
    MetricsCollector,
    QueryPhase,
    ResponseTier,
    TraceContext,
)

# Cloud retriever integration
try:
    from cloud_retriever import CognitionCloudRetriever, CloudKnowledge, retrieve_cloud_knowledge
    _CLOUD_AVAILABLE = True
except ImportError:
    _CLOUD_AVAILABLE = False
    logger.warning("cloud_retriever not available — running without cloud knowledge")

# ============================================================================
# CONSTANTS
# ============================================================================

PORT: int = 8517
HOST: str = "0.0.0.0"
LOG_DIR: Path = Path(__file__).parent / "logs"
AUDIT_DIR: Path = Path(__file__).parent / "audit_logs"

BANNED_PHRASES: list[str] = [
    "this is not legal advice",
    "consult an attorney",
    "i am not a lawyer",
    "this is for informational purposes only",
    "you should seek professional",
    "i cannot provide legal advice",
    "disclaimer",
]

# ============================================================================
# LOGGING SETUP
# ============================================================================

LOG_DIR.mkdir(parents=True, exist_ok=True)
AUDIT_DIR.mkdir(parents=True, exist_ok=True)

logger.remove()
logger.add(
    sys.stderr,
    level="INFO",
    format="<green>{time:HH:mm:ss}</green> | <level>{level:<8}</level> | <cyan>{module}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | {message}",
)
logger.add(
    str(LOG_DIR / "lm17_engine_{time:YYYY-MM-DD}.log"),
    level="DEBUG",
    rotation="50 MB",
    retention="30 days",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level:<8} | {module}:{function}:{line} | {message}",
)

# ============================================================================
# ENUMS
# ============================================================================


class ResponseMode(str, Enum):
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"


class AnalysisZone(str, Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"


# ============================================================================
# PYDANTIC MODELS - REQUEST / RESPONSE
# ============================================================================


class QueryRequest(BaseModel):
    """Incoming query request."""
    query: str
    mode: ResponseMode = ResponseMode.FAST
    zone: AnalysisZone = AnalysisZone.PLANNING
    category_filter: Optional[str] = None
    include_authority: bool = True
    include_counter_arguments: bool = False
    max_doctrines: int = Field(default=5, ge=1, le=20)
    session_id: Optional[str] = None


class AuthorityReference(BaseModel):
    """A single authority citation."""
    source: str
    weight: float = 1.0
    binding: bool = True


class CounterArgument(BaseModel):
    """A counter-argument with rebuttal."""
    argument: str
    rebuttal: str
    risk_level: str = "medium"


class FragilityScore(BaseModel):
    """Fact fragility assessment."""
    overall_score: float = Field(ge=0.0, le=1.0)
    verifiability: float = Field(ge=0.0, le=1.0)
    recharacterization_risk: float = Field(ge=0.0, le=1.0)
    testimony_dependence: float = Field(ge=0.0, le=1.0)
    regulatory_change_risk: float = Field(ge=0.0, le=1.0)
    factors: list[str] = Field(default_factory=list)


class DoctrineResult(BaseModel):
    """A single matched doctrine in the response."""
    topic: str
    category: str
    conclusion: str
    confidence: str
    confidence_stratification: str
    authority_sources: list[str] = Field(default_factory=list)
    match_score: float = 0.0
    burden_holder: str = ""
    adversary_position: str = ""
    resolution_strategy: str = ""
    fragility: Optional[FragilityScore] = None
    position_zone: str = "PLANNING"
    disclosure_caveat: Optional[str] = None


class DecompositionNode(BaseModel):
    """A node in the multi-doctrine decomposition graph."""
    issue_category: str
    doctrines: list[str]
    interactions: list[str] = Field(default_factory=list)
    resolution_order: int = 0


class QueryResponse(BaseModel):
    """Full query response."""
    engine_id: str = ENGINE_ID
    engine_name: str = ENGINE_NAME
    engine_version: str = ENGINE_VERSION
    query_id: str
    query: str
    query_hash: str
    mode: ResponseMode
    zone: AnalysisZone
    response_tier: str
    timestamp_utc: str
    elapsed_ms: float
    normalization: Optional[NormalizationResult] = None
    doctrines_matched: list[DoctrineResult] = Field(default_factory=list)
    decomposition: list[DecompositionNode] = Field(default_factory=list)
    deep_analysis: Optional[str] = None
    determinism_hash: str = ""
    confidence_summary: str = ""
    epistemic_disclosure: str = ""
    authority_chain: list[AuthorityReference] = Field(default_factory=list)
    counter_arguments: list[CounterArgument] = Field(default_factory=list)
    coverage_gaps: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    cloud_knowledge: dict[str, Any] = Field(default_factory=dict)
    cloud_citations: list[str] = Field(default_factory=list)


class HealthResponse(BaseModel):
    """Health check response."""
    engine_id: str = ENGINE_ID
    engine_name: str = ENGINE_NAME
    engine_version: str = ENGINE_VERSION
    status: str = "operational"
    timestamp_utc: str = ""
    uptime_seconds: float = 0.0
    doctrine_count: int = 0
    category_count: int = 0
    total_queries: int = 0
    error_rate: float = 0.0
    avg_latency_ms: float = 0.0
    cache_hit_rate: float = 0.0
    search_index_size: int = 0
    components: dict[str, str] = Field(default_factory=dict)


class CoverageReport(BaseModel):
    """Doctrine coverage report."""
    total_doctrines: int
    triggered_doctrines: list[str]
    untriggered_doctrines: list[str]
    trigger_counts: dict[str, int]
    category_coverage: dict[str, dict[str, int]]
    coverage_percentage: float
    epistemic_gaps: list[str]


# ============================================================================
# AUTHORITY HARDENING
# ============================================================================

AUTHORITY_HIERARCHY: dict[str, float] = {
    "federal_statute": 1.0,
    "federal_regulation": 0.95,
    "us_supreme_court": 0.98,
    "federal_circuit_court": 0.90,
    "federal_district_court": 0.80,
    "ferc_order": 0.92,
    "ferc_policy_statement": 0.85,
    "ferc_guidance": 0.75,
    "state_statute": 0.88,
    "state_regulation": 0.82,
    "state_supreme_court": 0.87,
    "state_appellate_court": 0.78,
    "state_trial_court": 0.65,
    "rrc_rule": 0.80,
    "rrc_order": 0.75,
    "phmsa_advisory_bulletin": 0.70,
    "phmsa_interpretation": 0.68,
    "industry_standard": 0.60,
    "api_recommended_practice": 0.58,
    "industry_practice": 0.50,
    "treatise": 0.45,
    "law_review": 0.40,
}


def classify_authority(source: str) -> tuple[str, float]:
    """Classify an authority source and return its weight."""
    source_lower = source.lower()
    if "usc" in source_lower or "united states code" in source_lower:
        return "federal_statute", AUTHORITY_HIERARCHY["federal_statute"]
    if "cfr" in source_lower or "code of federal regulations" in source_lower:
        return "federal_regulation", AUTHORITY_HIERARCHY["federal_regulation"]
    if "ferc" in source_lower and "policy statement" in source_lower:
        return "ferc_policy_statement", AUTHORITY_HIERARCHY["ferc_policy_statement"]
    if "ferc" in source_lower and ("order" in source_lower or "docket" in source_lower):
        return "ferc_order", AUTHORITY_HIERARCHY["ferc_order"]
    if "ferc" in source_lower:
        return "ferc_guidance", AUTHORITY_HIERARCHY["ferc_guidance"]
    if "tex." in source_lower or "texas" in source_lower:
        if "code" in source_lower:
            return "state_statute", AUTHORITY_HIERARCHY["state_statute"]
        if "s.w." in source_lower or "supreme" in source_lower:
            return "state_supreme_court", AUTHORITY_HIERARCHY["state_supreme_court"]
        return "state_regulation", AUTHORITY_HIERARCHY["state_regulation"]
    if "railroad commission" in source_lower or "rrc" in source_lower:
        return "rrc_rule", AUTHORITY_HIERARCHY["rrc_rule"]
    if "phmsa" in source_lower:
        return "phmsa_advisory_bulletin", AUTHORITY_HIERARCHY["phmsa_advisory_bulletin"]
    if "api" in source_lower:
        return "api_recommended_practice", AUTHORITY_HIERARCHY["api_recommended_practice"]
    if "49 cfr" in source_lower:
        return "federal_regulation", AUTHORITY_HIERARCHY["federal_regulation"]
    return "industry_practice", AUTHORITY_HIERARCHY["industry_practice"]


def harden_authorities(sources: list[str]) -> list[AuthorityReference]:
    """Convert raw authority sources into hardened, weighted references."""
    refs: list[AuthorityReference] = []
    for src in sources:
        auth_type, weight = classify_authority(src)
        refs.append(AuthorityReference(
            source=src,
            weight=round(weight, 2),
            binding=weight >= 0.80,
        ))
    refs.sort(key=lambda r: r.weight, reverse=True)
    return refs


# ============================================================================
# CONFIDENCE STRATIFICATION
# ============================================================================

CONFIDENCE_DESCRIPTIONS: dict[str, str] = {
    "DEFENSIBLE": (
        "Position supported by clear statutory authority, binding regulations, or controlling precedent. "
        "Low risk of adverse outcome if challenged."
    ),
    "AGGRESSIVE": (
        "Position supported by persuasive authority, favorable industry practice, or analogous precedent. "
        "Reasonable risk of adverse challenge."
    ),
    "DISCLOSURE": (
        "Material uncertainty exists requiring explicit disclosure to stakeholders. Multiple reasonable "
        "interpretations of applicable authority."
    ),
    "HIGH_RISK": (
        "Novel position with limited or adverse authority. Substantial risk of regulatory enforcement "
        "or litigation loss. Proceed with caution and explicit risk acceptance."
    ),
}


def get_confidence_description(level: ConfidenceLevel) -> str:
    """Return the description for a confidence level."""
    return CONFIDENCE_DESCRIPTIONS.get(level.value, "Unknown confidence level")


# ============================================================================
# FACT FRAGILITY SCORING (TIE-14)
# ============================================================================


def compute_fragility(doctrine: DoctrineBlock) -> FragilityScore:
    """Compute fact fragility score for a doctrine block."""
    verifiability = 0.8 if len(doctrine.primary_authority) >= 3 else 0.5
    rechar_risk = 0.6 if doctrine.confidence == ConfidenceLevel.DISCLOSURE else 0.3
    testimony_dep = 0.4 if doctrine.burden_holder == BurdenHolder.SHARED else 0.2
    reg_change_risk = 0.5 if "regulation" in " ".join(doctrine.primary_authority).lower() else 0.3

    overall = round(
        verifiability * 0.30
        + rechar_risk * 0.25
        + testimony_dep * 0.20
        + reg_change_risk * 0.25,
        3,
    )

    factors: list[str] = []
    if verifiability < 0.6:
        factors.append("Limited primary authority citations")
    if rechar_risk > 0.5:
        factors.append("Position subject to material recharacterization risk")
    if testimony_dep > 0.3:
        factors.append("Resolution depends on shared burden factual determinations")
    if reg_change_risk > 0.4:
        factors.append("Regulatory authority subject to change or reinterpretation")

    return FragilityScore(
        overall_score=overall,
        verifiability=verifiability,
        recharacterization_risk=rechar_risk,
        testimony_dependence=testimony_dep,
        regulatory_change_risk=reg_change_risk,
        factors=factors,
    )


# ============================================================================
# EPISTEMIC GUARDRAILS
# ============================================================================


def apply_epistemic_guardrails(text: str) -> str:
    """Strip banned phrases and apply epistemic integrity to response text."""
    result = text
    for phrase in BANNED_PHRASES:
        lower_result = result.lower()
        idx = lower_result.find(phrase)
        while idx != -1:
            result = result[:idx] + result[idx + len(phrase):]
            lower_result = result.lower()
            idx = lower_result.find(phrase)
    result = result.replace("  ", " ").strip()
    return result


# ============================================================================
# DRIFT WATCHER (TIE-9)
# ============================================================================


class DriftWatcher:
    """Monitor doctrine usage patterns to detect drift over time."""

    def __init__(self) -> None:
        self._topic_timestamps: defaultdict[str, list[float]] = defaultdict(list)
        self._confidence_shifts: list[dict[str, Any]] = []
        self._drift_alerts: list[dict[str, Any]] = []
        logger.info("DriftWatcher initialized")

    def record_usage(self, topic: str, confidence: str) -> None:
        """Record a doctrine usage event."""
        now = time.time()
        self._topic_timestamps[topic].append(now)
        if len(self._topic_timestamps[topic]) > 1000:
            self._topic_timestamps[topic] = self._topic_timestamps[topic][-500:]

    def check_drift(self) -> list[dict[str, Any]]:
        """Check for doctrine drift patterns."""
        alerts: list[dict[str, Any]] = []
        now = time.time()
        one_hour_ago = now - 3600
        for topic, timestamps in self._topic_timestamps.items():
            recent = [t for t in timestamps if t > one_hour_ago]
            if len(recent) > 50:
                alerts.append({
                    "type": "high_frequency",
                    "topic": topic,
                    "count_last_hour": len(recent),
                    "message": f"Doctrine '{topic}' triggered {len(recent)} times in the last hour",
                })
        self._drift_alerts.extend(alerts)
        return alerts

    def get_alerts(self) -> list[dict[str, Any]]:
        """Return all drift alerts."""
        return list(self._drift_alerts)


# ============================================================================
# COVERAGE MAP (TIE-10)
# ============================================================================


class CoverageMap:
    """Track which doctrines are triggered and identify epistemic gaps."""

    def __init__(self, all_topics: list[str]) -> None:
        self._all_topics = set(all_topics)
        self._trigger_counts: defaultdict[str, int] = defaultdict(int)
        self._category_triggers: defaultdict[str, defaultdict[str, int]] = defaultdict(lambda: defaultdict(int))
        logger.info("CoverageMap initialized with {} topics", len(self._all_topics))

    def record_trigger(self, topic: str, category: str) -> None:
        """Record that a doctrine was triggered."""
        self._trigger_counts[topic] += 1
        self._category_triggers[category][topic] += 1

    def get_report(self) -> CoverageReport:
        """Generate a coverage report."""
        triggered = [t for t in self._all_topics if self._trigger_counts.get(t, 0) > 0]
        untriggered = [t for t in self._all_topics if self._trigger_counts.get(t, 0) == 0]
        coverage_pct = (len(triggered) / len(self._all_topics) * 100.0) if self._all_topics else 0.0

        gaps: list[str] = []
        for cat_name, topics in self._category_triggers.items():
            if len(topics) < 2:
                gaps.append(f"Category '{cat_name}' has limited doctrine coverage ({len(topics)} triggered)")

        category_cov: dict[str, dict[str, int]] = {}
        for cat, topics in self._category_triggers.items():
            category_cov[cat] = dict(topics)

        return CoverageReport(
            total_doctrines=len(self._all_topics),
            triggered_doctrines=sorted(triggered),
            untriggered_doctrines=sorted(untriggered),
            trigger_counts=dict(self._trigger_counts),
            category_coverage=category_cov,
            coverage_percentage=round(coverage_pct, 1),
            epistemic_gaps=gaps,
        )


# ============================================================================
# MULTI-DOCTRINE DECOMPOSITION (TIE-19)
# ============================================================================

INTERACTION_EDGES: list[tuple[str, str, str]] = [
    ("ROW_ACQUISITION", "EASEMENT_NEGOTIATION", "Acquisition requires negotiated easement terms"),
    ("ROW_ACQUISITION", "EMINENT_DOMAIN", "Voluntary acquisition failure triggers condemnation"),
    ("ROW_ACQUISITION", "ENVIRONMENTAL_PERMITTING", "Route selection constrained by environmental permits"),
    ("EASEMENT_NEGOTIATION", "TEMPORARY_WORKSPACE", "Temporary workspace negotiated alongside permanent easement"),
    ("EASEMENT_NEGOTIATION", "SURFACE_DAMAGE", "Surface damage provisions included in easement"),
    ("FERC_COMPLIANCE", "EMINENT_DOMAIN", "FERC certificate enables federal eminent domain"),
    ("FERC_COMPLIANCE", "ENVIRONMENTAL_PERMITTING", "FERC certificate requires NEPA review"),
    ("EMINENT_DOMAIN", "DISPUTE_RESOLUTION", "Condemnation compensation disputes"),
    ("CROSSING_PERMITS", "ENVIRONMENTAL_PERMITTING", "Waterway crossings require Section 404 permits"),
    ("ENVIRONMENTAL_PERMITTING", "SURFACE_DAMAGE", "Environmental restoration overlaps surface damage"),
    ("PIPELINE_SAFETY", "ENCROACHMENT", "Safety regulations require encroachment monitoring"),
    ("PIPELINE_SAFETY", "ABANDONMENT", "Safety regulations govern abandonment procedures"),
    ("ABANDONMENT", "DISPUTE_RESOLUTION", "Abandonment may trigger landowner disputes"),
    ("ENCROACHMENT", "DISPUTE_RESOLUTION", "Encroachment enforcement may require dispute resolution"),
    ("SURFACE_DAMAGE", "DISPUTE_RESOLUTION", "Surface damage claims are common dispute source"),
]


def decompose_query(matched_categories: list[str]) -> list[DecompositionNode]:
    """Decompose a multi-doctrine query into an interaction graph."""
    if not matched_categories:
        return []

    category_set = set(matched_categories)
    nodes: dict[str, DecompositionNode] = {}

    for cat in matched_categories:
        doctrines_in_cat = [d.topic for d in DOCTRINE_CACHE if d.category.value == cat]
        interactions: list[str] = []
        for src, tgt, desc in INTERACTION_EDGES:
            if src == cat and tgt in category_set:
                interactions.append(f"{tgt}: {desc}")
            elif tgt == cat and src in category_set:
                interactions.append(f"{src}: {desc}")
        nodes[cat] = DecompositionNode(
            issue_category=cat,
            doctrines=doctrines_in_cat,
            interactions=interactions,
            resolution_order=0,
        )

    resolution_order = [
        "FERC_COMPLIANCE", "ENVIRONMENTAL_PERMITTING", "ROW_ACQUISITION",
        "EASEMENT_NEGOTIATION", "EMINENT_DOMAIN", "CROSSING_PERMITS",
        "TEMPORARY_WORKSPACE", "SURFACE_DAMAGE", "PIPELINE_SAFETY",
        "ENCROACHMENT", "ABANDONMENT", "DISPUTE_RESOLUTION",
    ]
    for idx, cat in enumerate(resolution_order):
        if cat in nodes:
            nodes[cat].resolution_order = idx

    return sorted(nodes.values(), key=lambda n: n.resolution_order)


# ============================================================================
# ZONED ANALYSIS (TIE-13)
# ============================================================================


def apply_zone_filter(doctrine: DoctrineBlock, zone: AnalysisZone) -> DoctrineBlock:
    """Apply position zone filtering to a doctrine block."""
    if zone == AnalysisZone.PLANNING:
        return doctrine
    if zone == AnalysisZone.REPORTING:
        if doctrine.confidence == ConfidenceLevel.HIGH_RISK:
            modified = doctrine.model_copy()
            modified.disclosure_caveat = (
                f"REPORTING ZONE DISCLOSURE: This position carries HIGH_RISK confidence. "
                f"Original stratification: {doctrine.confidence_stratification}. "
                f"Report should include full risk analysis."
            )
            return modified
    if zone == AnalysisZone.AUDIT:
        modified = doctrine.model_copy()
        modified.disclosure_caveat = (
            f"AUDIT ZONE: Full authority chain and counter-arguments must be disclosed. "
            f"Confidence: {doctrine.confidence.value}. "
            f"Controlling precedent: {doctrine.controlling_precedent}"
        )
        return modified
    return doctrine


# ============================================================================
# DEEP ANALYSIS MODE (TIE-20)
# ============================================================================


def generate_deep_analysis(
    query: str,
    matched_doctrines: list[DoctrineBlock],
    normalization: NormalizationResult,
    zone: AnalysisZone,
) -> str:
    """Generate deep multi-source synthesis analysis."""
    if not matched_doctrines:
        return "No doctrines matched for deep analysis."

    sections: list[str] = []
    sections.append(f"DEEP ANALYSIS: Pipeline ROW Intelligence Assessment")
    sections.append(f"Query: {query}")
    sections.append(f"Analysis Zone: {zone.value}")
    sections.append(f"Doctrines Analyzed: {len(matched_doctrines)}")
    sections.append("")

    sections.append("--- ISSUE IDENTIFICATION ---")
    categories_seen: set[str] = set()
    for d in matched_doctrines:
        if d.category.value not in categories_seen:
            categories_seen.add(d.category.value)
            sections.append(f"  Category: {d.category.value}")
            cat_doctrines = [x for x in matched_doctrines if x.category == d.category]
            for cd in cat_doctrines:
                sections.append(f"    - {cd.topic}: {cd.confidence.value} confidence")
    sections.append("")

    sections.append("--- AUTHORITY CHAIN ---")
    all_authorities: list[tuple[str, float]] = []
    for d in matched_doctrines:
        for src in d.primary_authority:
            _, weight = classify_authority(src)
            all_authorities.append((src, weight))
    all_authorities.sort(key=lambda x: x[1], reverse=True)
    for src, weight in all_authorities[:10]:
        binding = "BINDING" if weight >= 0.80 else "PERSUASIVE"
        sections.append(f"  [{binding} w={weight:.2f}] {src}")
    sections.append("")

    sections.append("--- REASONING SYNTHESIS ---")
    for d in matched_doctrines:
        sections.append(f"  Topic: {d.topic}")
        sections.append(f"  Conclusion: {d.conclusion_template[:200]}...")
        sections.append(f"  Burden: {d.burden_holder.value}")
        sections.append(f"  Confidence: {d.confidence.value} - {d.confidence_stratification}")
        sections.append("")

    sections.append("--- ADVERSARIAL ANALYSIS ---")
    for d in matched_doctrines:
        if d.adversary_position:
            sections.append(f"  [{d.topic}] Adversary: {d.adversary_position[:150]}...")
            if d.counter_arguments:
                for ca in d.counter_arguments[:2]:
                    sections.append(f"    Counter: {ca}")
            sections.append("")

    sections.append("--- INTERACTION ANALYSIS ---")
    matched_cats = list(categories_seen)
    for src, tgt, desc in INTERACTION_EDGES:
        if src in matched_cats and tgt in matched_cats:
            sections.append(f"  {src} <-> {tgt}: {desc}")
    sections.append("")

    if any(d.disclosure_caveat for d in matched_doctrines):
        sections.append("--- DISCLOSURE REQUIREMENTS ---")
        for d in matched_doctrines:
            if d.disclosure_caveat:
                sections.append(f"  [{d.topic}] {d.disclosure_caveat}")
        sections.append("")

    sections.append("--- RESOLUTION PATHWAY ---")
    for d in matched_doctrines:
        sections.append(f"  [{d.topic}] {d.resolution_strategy[:150]}...")
    sections.append("")

    if normalization.statutes_identified:
        sections.append("--- STATUTES IDENTIFIED ---")
        for s in normalization.statutes_identified:
            sections.append(f"  - {s}")

    return "\n".join(sections)


# ============================================================================
# DETERMINISM HASH (TIE-16)
# ============================================================================


def compute_determinism_hash(
    query: str,
    mode: str,
    zone: str,
    matched_topics: list[str],
    tier: str,
) -> str:
    """Compute SHA-256 determinism hash for reproducibility."""
    payload = json.dumps({
        "query": query.strip().lower(),
        "mode": mode,
        "zone": zone,
        "topics": sorted(matched_topics),
        "tier": tier,
        "engine_version": ENGINE_VERSION,
    }, sort_keys=True)
    return hashlib.sha256(payload.encode()).hexdigest()


# ============================================================================
# CORE ENGINE CLASS
# ============================================================================


class PipelineROWEngine:
    """
    Core LM17 Pipeline ROW intelligence engine implementing TIE-20 standard.
    Three-layer response architecture: doctrine cache -> semantic search -> deep analysis.
    """

    def __init__(self) -> None:
        self._start_time: float = time.time()
        self._normalizer = PipelineROWNormalizer(NormalizationMode.STANDARD)
        self._metrics = MetricsCollector()
        self._search_engine = PipelineROWSearchEngine()
        self._drift_watcher = DriftWatcher()
        self._coverage_map = CoverageMap(get_all_topics())
        self._doctrine_cache: list[DoctrineBlock] = get_doctrine_cache()
        self._topic_keyword_map: dict[str, list[str]] = get_doctrine_topic_keyword_map()

        self._index_doctrines()
        logger.info(
            "PipelineROWEngine initialized | doctrines={} categories={} port={}",
            len(self._doctrine_cache), len(get_all_categories()), PORT,
        )

    def _index_doctrines(self) -> None:
        """Index all doctrines into the search engine."""
        docs: list[SearchDocument] = []
        for doctrine in self._doctrine_cache:
            content = (
                f"{doctrine.topic} {doctrine.conclusion_template} "
                f"{doctrine.reasoning_framework} "
                f"{' '.join(doctrine.key_factors)} "
                f"{doctrine.adversary_position} "
                f"{' '.join(doctrine.counter_arguments)} "
                f"{doctrine.resolution_strategy}"
            )
            docs.append(SearchDocument(
                doc_id=doctrine.topic,
                topic=doctrine.topic,
                category=doctrine.category.value,
                content=content,
                keywords=doctrine.keywords,
                authority_sources=doctrine.primary_authority,
                weight=1.2 if doctrine.confidence == ConfidenceLevel.DEFENSIBLE else 1.0,
            ))
        self._search_engine.add_documents(docs)
        logger.info("Indexed {} doctrines into search engine", len(docs))

    def process_query(self, request: QueryRequest) -> QueryResponse:
        """Process a query through the three-layer response architecture."""
        query_id = str(uuid.uuid4())
        trace = self._metrics.create_trace(request.query, query_id)

        # Cloud knowledge retrieval
        cloud_data = {}
        cloud_citations = []
        if _CLOUD_AVAILABLE:
            try:
                cloud = asyncio.run(retrieve_cloud_knowledge(request.query, category="pipeline_row"))
                cloud_data = {
                    "records": len(cloud.clauses) + len(cloud.graph_nodes) + len(cloud.crystals),
                    "merged_context": cloud.merged_text(3000),
                    "sources_succeeded": cloud.sources_succeeded,
                    "retrieval_time_ms": cloud.retrieval_time_ms,
                }
                cloud_citations = cloud.citation_list()
            except Exception as e:
                logger.warning(f"Cloud retrieval failed: {e}")

        try:
            # --- Layer 0: Normalization ---
            trace.add_event(QueryPhase.NORMALIZED)
            normalization = self._normalizer.normalize(request.query)
            trace.add_event(QueryPhase.VALIDATED, {"keywords": len(normalization.keyword_tokens)})

            # --- Layer 1: Doctrine Cache Lookup ---
            trace.add_event(QueryPhase.CACHE_LOOKUP)
            cache_matches = self._normalizer.match_query_to_topics(
                request.query, self._topic_keyword_map, threshold=0.18,
            )

            matched_doctrines: list[tuple[DoctrineBlock, float]] = []
            if cache_matches:
                trace.add_event(QueryPhase.CACHE_HIT, {"matches": len(cache_matches)})
                for match in cache_matches[:request.max_doctrines]:
                    doctrine = get_doctrine_by_topic(match.topic)
                    if doctrine:
                        if request.category_filter and doctrine.category.value != request.category_filter:
                            continue
                        doctrine = apply_zone_filter(doctrine, request.zone)
                        matched_doctrines.append((doctrine, match.match_score))
                        self._coverage_map.record_trigger(doctrine.topic, doctrine.category.value)
                        self._drift_watcher.record_usage(doctrine.topic, doctrine.confidence.value)

            # --- Layer 2: Semantic Search Fallback ---
            response_tier = ResponseTier.DOCTRINE_CACHE
            if not matched_doctrines:
                trace.add_event(QueryPhase.CACHE_MISS)
                trace.add_event(QueryPhase.SEMANTIC_SEARCH)
                search_result: SearchResponse = self._search_engine.search(
                    request.query,
                    top_k=request.max_doctrines,
                    category_filter=request.category_filter,
                )
                response_tier = ResponseTier.SEMANTIC_RETRIEVAL
                for sr in search_result.results:
                    doctrine = get_doctrine_by_topic(sr.topic)
                    if doctrine:
                        doctrine = apply_zone_filter(doctrine, request.zone)
                        matched_doctrines.append((doctrine, sr.relevance_score))
                        self._coverage_map.record_trigger(doctrine.topic, doctrine.category.value)
                        self._drift_watcher.record_usage(doctrine.topic, doctrine.confidence.value)

            # --- Layer 3: Deep Analysis (DEFENSE / MEMO modes, or when no matches) ---
            deep_analysis_text: Optional[str] = None
            if request.mode in (ResponseMode.DEFENSE, ResponseMode.MEMO) or not matched_doctrines:
                trace.add_event(QueryPhase.DEEP_ANALYSIS)
                if not matched_doctrines:
                    response_tier = ResponseTier.DEEP_ANALYSIS
                raw_doctrines = [d for d, _ in matched_doctrines]
                deep_analysis_text = generate_deep_analysis(
                    request.query, raw_doctrines, normalization, request.zone,
                )

            # --- Authority Hardening ---
            trace.add_event(QueryPhase.AUTHORITY_HARDENING)
            all_authority_sources: list[str] = []
            for d, _ in matched_doctrines:
                all_authority_sources.extend(d.primary_authority)
            authority_chain = harden_authorities(list(set(all_authority_sources)))

            # --- Confidence Scoring ---
            trace.add_event(QueryPhase.CONFIDENCE_SCORING)
            confidence_levels = [d.confidence.value for d, _ in matched_doctrines]
            if confidence_levels:
                if "HIGH_RISK" in confidence_levels:
                    confidence_summary = "HIGH_RISK - At least one matched position carries substantial adverse authority risk"
                elif "DISCLOSURE" in confidence_levels:
                    confidence_summary = "DISCLOSURE - Material uncertainty present requiring stakeholder notification"
                elif "AGGRESSIVE" in confidence_levels:
                    confidence_summary = "AGGRESSIVE - Positions supported by persuasive but non-binding authority"
                else:
                    confidence_summary = "DEFENSIBLE - All matched positions supported by clear authority"
            else:
                confidence_summary = "NO_MATCH - No doctrine positions matched; general analysis provided"

            # --- Fragility Scoring ---
            trace.add_event(QueryPhase.FRAGILITY_SCORING)

            # --- Build Doctrine Results ---
            doctrine_results: list[DoctrineResult] = []
            for doctrine, score in matched_doctrines:
                fragility = compute_fragility(doctrine)
                conclusion = apply_epistemic_guardrails(doctrine.conclusion_template)
                dr = DoctrineResult(
                    topic=doctrine.topic,
                    category=doctrine.category.value,
                    conclusion=conclusion,
                    confidence=doctrine.confidence.value,
                    confidence_stratification=doctrine.confidence_stratification,
                    authority_sources=doctrine.primary_authority if request.include_authority else [],
                    match_score=round(score, 4),
                    burden_holder=doctrine.burden_holder.value,
                    adversary_position=doctrine.adversary_position if request.include_counter_arguments else "",
                    resolution_strategy=doctrine.resolution_strategy,
                    fragility=fragility,
                    position_zone=doctrine.position_zone.value,
                    disclosure_caveat=doctrine.disclosure_caveat,
                )
                doctrine_results.append(dr)

            # --- Counter Arguments ---
            counter_args: list[CounterArgument] = []
            if request.include_counter_arguments:
                for doctrine, _ in matched_doctrines:
                    for i, ca in enumerate(doctrine.counter_arguments):
                        counter_args.append(CounterArgument(
                            argument=doctrine.adversary_position if i == 0 else f"Counter-point {i + 1}",
                            rebuttal=ca,
                            risk_level="high" if doctrine.confidence == ConfidenceLevel.HIGH_RISK else "medium",
                        ))

            # --- Multi-Doctrine Decomposition ---
            matched_categories = list(set(d.category.value for d, _ in matched_doctrines))
            decomposition = decompose_query(matched_categories)

            # --- Epistemic Disclosure ---
            disclosures: list[str] = []
            for d, _ in matched_doctrines:
                if d.disclosure_caveat:
                    disclosures.append(d.disclosure_caveat)
            epistemic_disclosure = "; ".join(disclosures) if disclosures else ""

            # --- Coverage Gaps ---
            coverage_gaps: list[str] = []
            for cat in get_all_categories():
                if cat not in matched_categories:
                    cat_doctrines = get_doctrines_by_category(IssueCategory(cat))
                    for cd in cat_doctrines:
                        for kw in cd.keywords:
                            if kw.lower() in request.query.lower() and cat not in [g.split(":")[0] for g in coverage_gaps]:
                                coverage_gaps.append(f"{cat}: Keyword '{kw}' present but category not matched")
                                break

            # --- Determinism Hash ---
            matched_topics = [d.topic for d, _ in matched_doctrines]
            det_hash = compute_determinism_hash(
                request.query, request.mode.value, request.zone.value,
                matched_topics, response_tier.value,
            )

            # --- Assemble Response ---
            trace.add_event(QueryPhase.RESPONSE_ASSEMBLY)
            query_hash = hashlib.sha256(request.query.encode()).hexdigest()[:16]

            query_trace = trace.complete(
                response_tier=response_tier,
                doctrine_topics=matched_topics,
                issue_categories=matched_categories,
                confidence_level=confidence_summary.split(" - ")[0] if confidence_summary else None,
                determinism_hash=det_hash,
            )

            return QueryResponse(
                query_id=query_id,
                query=request.query,
                query_hash=query_hash,
                mode=request.mode,
                zone=request.zone,
                response_tier=response_tier.value,
                timestamp_utc=datetime.now(timezone.utc).isoformat(),
                elapsed_ms=query_trace.total_elapsed_ms,
                normalization=normalization,
                doctrines_matched=doctrine_results,
                decomposition=decomposition,
                deep_analysis=deep_analysis_text,
                determinism_hash=det_hash,
                confidence_summary=confidence_summary,
                epistemic_disclosure=epistemic_disclosure,
                authority_chain=authority_chain,
                counter_arguments=counter_args if request.include_counter_arguments else [],
                coverage_gaps=coverage_gaps,
                cloud_knowledge=cloud_data,
                cloud_citations=cloud_citations,
                metadata={
                    "trace_id": query_trace.trace_id,
                    "doctrine_count": len(doctrine_results),
                    "category_count": len(matched_categories),
                    "search_fallback": response_tier != ResponseTier.DOCTRINE_CACHE,
                },
            )

        except Exception as exc:
            error_trace = trace.fail(ErrorDomain.UNKNOWN, str(exc))
            logger.exception("Query processing failed | query_id={}", query_id)
            raise HTTPException(
                status_code=500,
                detail={
                    "error": str(exc),
                    "trace_id": error_trace.trace_id,
                    "query_id": query_id,
                    "stack": traceback.format_exc(),
                },
            ) from exc

    def get_health(self) -> HealthResponse:
        """Generate comprehensive health check response."""
        telemetry = self._metrics.get_health_telemetry()
        index_stats = self._search_engine.get_index_stats()
        uptime = time.time() - self._start_time
        return HealthResponse(
            status=telemetry.status,
            timestamp_utc=datetime.now(timezone.utc).isoformat(),
            uptime_seconds=round(uptime, 1),
            doctrine_count=len(self._doctrine_cache),
            category_count=len(get_all_categories()),
            total_queries=telemetry.total_queries_processed,
            error_rate=telemetry.error_rate_percent,
            avg_latency_ms=telemetry.avg_response_ms,
            cache_hit_rate=telemetry.cache_hit_rate_percent,
            search_index_size=index_stats["total_documents"],
            components={
                "doctrine_cache": "operational",
                "semantic_normalizer": "operational",
                "search_engine": "operational",
                "telemetry": telemetry.status,
                "drift_watcher": "operational",
                "coverage_map": "operational",
                "authority_hardening": "operational",
                "fragility_scoring": "operational",
                "audit_trail": "operational",
                "determinism_hash": "operational",
                "zoned_analysis": "operational",
                "deep_analysis": "operational",
                "decomposition": "operational",
                "epistemic_guardrails": "operational",
            },
        )

    def get_metrics(self) -> dict[str, Any]:
        """Get current metrics snapshot."""
        return self._metrics.get_snapshot().model_dump()

    def get_coverage(self) -> CoverageReport:
        """Get doctrine coverage report."""
        return self._coverage_map.get_report()

    def get_drift_alerts(self) -> list[dict[str, Any]]:
        """Get drift watcher alerts."""
        return self._drift_watcher.check_drift()


# ============================================================================
# FASTAPI APPLICATION (TIE-17)
# ============================================================================

engine: Optional[PipelineROWEngine] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    global engine
    logger.info("Starting LM17 Pipeline ROW Engine v{} on port {}", ENGINE_VERSION, PORT)
    engine = PipelineROWEngine()
    logger.info("Engine initialized successfully | doctrines={}", len(DOCTRINE_CACHE))
    yield
    logger.info("Shutting down LM17 Pipeline ROW Engine")
    if _CLOUD_AVAILABLE:
        try:
            from cloud_retriever import cleanup_cloud_resources
            await cleanup_cloud_resources()
            logger.info("Cloud resources cleaned up")
        except Exception as e:
            logger.warning(f"Cloud cleanup failed: {e}")


app = FastAPI(
    title=f"LM17 Pipeline ROW Intelligence Engine",
    description=(
        "Pipeline right-of-way acquisition, routing, easement negotiation, "
        "FERC compliance, eminent domain, environmental permitting, and "
        "landowner dispute resolution intelligence engine."
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


# ============================================================================
# ENDPOINTS
# ============================================================================


@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest) -> QueryResponse:
    """Process a pipeline ROW intelligence query."""
    if engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    return engine.process_query(request)


@app.get("/health", response_model=HealthResponse)
async def health_endpoint() -> HealthResponse:
    """Comprehensive health check."""
    if engine is None:
        return HealthResponse(status="initializing", timestamp_utc=datetime.now(timezone.utc).isoformat())
    return engine.get_health()


@app.get("/metrics")
async def metrics_endpoint() -> dict[str, Any]:
    """Performance metrics snapshot."""
    if engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    return engine.get_metrics()


@app.get("/coverage", response_model=CoverageReport)
async def coverage_endpoint() -> CoverageReport:
    """Doctrine coverage report."""
    if engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    return engine.get_coverage()


@app.get("/doctrines")
async def doctrines_endpoint(
    category: Optional[str] = Query(None, description="Filter by issue category"),
) -> dict[str, Any]:
    """List all doctrines or filter by category."""
    doctrines = get_doctrine_cache()
    if category:
        try:
            cat_enum = IssueCategory(category)
            doctrines = get_doctrines_by_category(cat_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid category: {category}")
    return {
        "engine_id": ENGINE_ID,
        "total": len(doctrines),
        "categories": get_all_categories(),
        "doctrines": [
            {
                "topic": d.topic,
                "category": d.category.value,
                "confidence": d.confidence.value,
                "keywords": d.keywords,
                "burden_holder": d.burden_holder.value,
                "authority_count": len(d.primary_authority),
                "counter_arguments_count": len(d.counter_arguments),
            }
            for d in doctrines
        ],
    }


@app.get("/drift")
async def drift_endpoint() -> dict[str, Any]:
    """Drift watcher alerts."""
    if engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    alerts = engine.get_drift_alerts()
    return {"engine_id": ENGINE_ID, "alerts": alerts, "alert_count": len(alerts)}


@app.get("/categories")
async def categories_endpoint() -> dict[str, Any]:
    """List all issue categories with doctrine counts."""
    categories: dict[str, int] = {}
    for doctrine in DOCTRINE_CACHE:
        cat = doctrine.category.value
        categories[cat] = categories.get(cat, 0) + 1
    return {
        "engine_id": ENGINE_ID,
        "total_categories": len(categories),
        "categories": categories,
    }


@app.get("/")
async def root_endpoint() -> dict[str, Any]:
    """Root endpoint with engine information."""
    return {
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "engine_version": ENGINE_VERSION,
        "port": PORT,
        "status": "operational" if engine else "initializing",
        "tie_standard": "TIE-20 GOLD",
        "domain": "pipeline_right_of_way",
        "endpoints": ["/query", "/health", "/metrics", "/coverage", "/doctrines", "/drift", "/categories"],
    }


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    logger.info("Launching LM17 Pipeline ROW Engine on port {}", PORT)
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    uvicorn.run(
        "engine:app",
        host=HOST,
        port=PORT,
        reload=False,
        log_level="info",
        access_log=True,
    )
