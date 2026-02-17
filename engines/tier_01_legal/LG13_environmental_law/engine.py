"""
LG13 Environmental Law Engine - Main FastAPI Engine
======================================================
Production-grade environmental law analysis engine implementing all 20 TIE
components for NEPA, CAA, CWA, RCRA, CERCLA/Superfund, TSCA, ESA, FIFRA,
SDWA, OPA, EPCRA, environmental impact assessment, air/water discharge
permits, hazardous waste, brownfield redevelopment, Phase I/II ESA, USTs,
TCEQ, RRC environmental authority, Permian Basin environmental issues,
carbon credits, climate regulation, environmental justice, citizen suits,
toxic tort, and environmental insurance analysis.

TIE-20 Components:
    1.  three_layer_response
    2.  response_modes (fast, analysis, memo, permit_review, compliance_check)
    3.  doctrine_cache
    4.  authority_hardening
    5.  confidence_stratification
    6.  semantic_normalization
    7.  vector_search_chromadb (TF-IDF inverted index implementation)
    8.  telemetry_module
    9.  doctrine_drift_watcher
    10. doctrine_coverage_map
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

Port: 8403
Engine: LG13 Environmental Law
Version: 1.0.0
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import os
import sys
import time
import uuid
from collections import Counter, defaultdict
from contextlib import asynccontextmanager
from dataclasses import dataclass, field as dc_field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, ClassVar, Dict, List, Optional, Set, Tuple, Union

from loguru import logger

# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------
from pydantic import BaseModel, Field, field_validator

# ---------------------------------------------------------------------------
# FastAPI
# ---------------------------------------------------------------------------
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# ---------------------------------------------------------------------------
# Sibling module imports
# ---------------------------------------------------------------------------

# Ensure sibling modules are importable
ENGINE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ENGINE_DIR))
from doctrines import (
    DOCTRINE_BLOCKS,
    DoctrineCacheBlock,
    DoctrineCacheIndex,
    build_doctrine_cache,
    get_all_doctrine_categories,
    get_all_doctrine_topics,
    get_coverage_map,
    get_doctrine_block,
    get_doctrine_cache,
    get_doctrine_cache_hash,
    get_doctrine_cache_stats,
    get_stale_doctrines,
    search_doctrines,
    verify_doctrine_integrity,
)
from search import (
    CERCLAPRPAnalyzer,
    ComplianceChecker,
    ComplianceCheckResult,
    DoctrineSearchIndex,
    PRPCategory,
    PRPLiabilityAssessment,
    PenaltyCalculator,
    PenaltyEstimate,
    PermitAnalyzer,
    PermitAnalysisResult,
    PhaseIESAWorkflow,
    PhaseIESAResult,
    RemediationSelector,
    RemediationOption,
    SearchResult,
    build_search_index,
    compute_query_hash,
)
from semantic import (
    NormalizationResult,
    normalize_semantics,
    get_normalizer,
)
from telemetry import (
    AlertSeverity,
    DoctrineMutation,
    ErrorDomain,
    MutationOrigin,
    MutationType,
    QueryTrace,
    ResponseLayer,
    TelemetryCollector,
    complete_trace,
    get_telemetry,
    log_error,
    record_doctrine_mutation,
    trace_query,
)


# ============================================================================
# CONFIGURATION
# ============================================================================

ENGINE_ID = "LG13"
ENGINE_NAME = "Environmental Law Engine"
ENGINE_VERSION = "1.0.0"
ENGINE_PORT = 8403
ENGINE_DOMAIN = "environmental_law"

ENGINE_DIR = Path(__file__).parent
CONFIG_PATH = ENGINE_DIR / "config.json"
LOG_DIR = ENGINE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logger.add(
    LOG_DIR / "lg13_engine_{time}.log",
    rotation="50 MB",
    retention="30 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level:<8} | {name}:{function}:{line} | {message}",
)


def load_config() -> Dict[str, Any]:
    """Load engine configuration from config.json."""
    if CONFIG_PATH.exists():
        with CONFIG_PATH.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    logger.warning(f"Config not found at {CONFIG_PATH}, using defaults")
    return {}


CONFIG = load_config()


# ============================================================================
# TIE COMPONENT 2: RESPONSE MODES
# ============================================================================

class ResponseMode(str, Enum):
    """Response mode determines output depth and format."""
    FAST = "FAST"
    ANALYSIS = "ANALYSIS"
    MEMO = "MEMO"
    PERMIT_REVIEW = "PERMIT_REVIEW"
    COMPLIANCE_CHECK = "COMPLIANCE_CHECK"


class AnalysisLayer(str, Enum):
    """Analysis depth layer."""
    QUICK = "QUICK"
    STANDARD = "STANDARD"
    DEEP = "DEEP"


# ============================================================================
# TIE COMPONENT 5: CONFIDENCE STRATIFICATION
# ============================================================================

class ConfidenceLevel(str, Enum):
    """Confidence level classification."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNCERTAIN = "uncertain"


CONFIDENCE_THRESHOLDS = CONFIG.get("confidence_thresholds", {
    "high": 0.85,
    "medium": 0.65,
    "low": 0.40,
    "uncertain": 0.20,
})


def classify_confidence(score: float) -> ConfidenceLevel:
    """Classify a confidence score into a level."""
    if score >= CONFIDENCE_THRESHOLDS["high"]:
        return ConfidenceLevel.HIGH
    elif score >= CONFIDENCE_THRESHOLDS["medium"]:
        return ConfidenceLevel.MEDIUM
    elif score >= CONFIDENCE_THRESHOLDS["low"]:
        return ConfidenceLevel.LOW
    return ConfidenceLevel.UNCERTAIN


# ============================================================================
# TIE COMPONENT 4: AUTHORITY HARDENING
# ============================================================================

BANNED_PHRASES: List[str] = [
    "i think",
    "i believe",
    "probably",
    "it seems like",
    "in my opinion",
    "you should consider",
    "it might be",
    "it could be",
    "this might",
    "maybe",
    "perhaps",
    "i would guess",
    "it appears that",
    "one could argue",
    "it is possible that",
    "you might want to",
    "i suggest",
]

DISCLOSURE_CAVEATS: Dict[str, str] = {
    "general": "This analysis is for informational purposes only and does not constitute legal advice. Consult qualified environmental counsel for site-specific guidance.",
    "permit": "Permit requirements vary by jurisdiction, facility characteristics, and activity type. This analysis identifies likely requirements but a comprehensive permit review by qualified counsel is recommended.",
    "cercla": "CERCLA liability analysis is highly fact-specific. The defenses and allocations discussed are general frameworks; actual liability depends on the specific facts, evidence, and judicial district.",
    "penalty": "Penalty estimates are based on published penalty policies and statutory maxima. Actual penalties are determined through negotiation or litigation and may differ substantially.",
    "compliance": "Compliance requirements change frequently. Verify current regulations and permit conditions with the applicable regulatory agency before relying on this analysis.",
    "texas": "Texas environmental regulation involves split jurisdiction between TCEQ and RRC. Confirm the correct regulatory authority for your specific activity and location.",
}


def apply_authority_hardening(text: str) -> str:
    """Remove soft language from analysis text."""
    result = text
    for phrase in BANNED_PHRASES:
        lower_result = result.lower()
        idx = lower_result.find(phrase)
        while idx != -1:
            end = idx + len(phrase)
            replacement = ""
            if phrase in ("probably", "perhaps", "maybe"):
                replacement = ""
            result = result[:idx] + replacement + result[end:]
            lower_result = result.lower()
            idx = lower_result.find(phrase)
    result = " ".join(result.split())
    return result


# ============================================================================
# PYDANTIC MODELS - REQUEST / RESPONSE
# ============================================================================

class EnvironmentalQueryRequest(BaseModel):
    """Incoming query request."""
    query: str = Field(..., min_length=3, max_length=10000, description="The environmental law question")
    response_mode: ResponseMode = Field(default=ResponseMode.ANALYSIS, description="Response depth mode")
    analysis_layer: AnalysisLayer = Field(default=AnalysisLayer.STANDARD, description="Analysis depth")
    jurisdiction: str = Field(default="TX", description="Primary jurisdiction")
    include_texas_notes: bool = Field(default=True, description="Include Texas-specific annotations")
    include_permian_context: bool = Field(default=False, description="Include Permian Basin context")
    include_penalty_estimate: bool = Field(default=False, description="Include penalty estimate if applicable")
    max_results: int = Field(default=10, ge=1, le=50, description="Maximum search results")

    @field_validator("query")
    @classmethod
    def validate_query(cls, v: str) -> str:
        stripped = v.strip()
        if len(stripped) < 3:
            raise ValueError("Query must be at least 3 characters")
        return stripped


class EnvironmentalQueryResponse(BaseModel):
    """Response to an environmental law query."""
    engine_id: str = ENGINE_ID
    engine_version: str = ENGINE_VERSION
    query: str
    normalized_query: str
    response_mode: str
    analysis_layer: str
    jurisdiction: str
    # TIE Component 1: Three-layer response
    doctrine_response: Optional[Dict[str, Any]] = None
    search_response: Optional[Dict[str, Any]] = None
    deep_response: Optional[Dict[str, Any]] = None
    # Core analysis
    primary_analysis: str
    statutes_applicable: List[str]
    agencies_involved: List[str]
    permits_relevant: List[str]
    contaminants_identified: List[str]
    environmental_domains: List[str]
    # TIE Components
    confidence: float
    confidence_level: str
    citations: List[str]
    practice_tips: List[str]
    texas_notes: Optional[str] = None
    permian_context: Optional[str] = None
    penalty_estimate: Optional[Dict[str, Any]] = None
    disclosure_caveat: str
    # Metadata
    normalization_info: Dict[str, Any]
    search_results_count: int
    doctrine_blocks_matched: int
    response_layer: str
    determinism_hash: str
    trace_id: str
    latency_ms: float
    timestamp: str


class PermitAnalysisRequest(BaseModel):
    """Request for permit requirement analysis."""
    activity: str = Field(..., min_length=5, description="Description of proposed activity")
    jurisdiction: str = Field(default="TX")
    keywords: List[str] = Field(default_factory=list)


class PRPAssessmentRequest(BaseModel):
    """Request for CERCLA PRP liability assessment."""
    party_name: str = Field(..., min_length=2)
    category: str = Field(..., description="current_owner_operator|past_owner_operator|arranger|transporter")
    facts: Dict[str, Any] = Field(default_factory=dict)


class ComplianceCheckRequest(BaseModel):
    """Request for facility compliance check."""
    facility_type: str = Field(..., min_length=3)
    activities: List[str] = Field(..., min_length=1)
    jurisdiction: str = Field(default="TX")


class PhaseIRequest(BaseModel):
    """Request for Phase I ESA workflow."""
    property_address: str = Field(..., min_length=5)
    jurisdiction: str = Field(default="TX")
    findings: List[Dict[str, Any]] = Field(default_factory=list)


class PenaltyRequest(BaseModel):
    """Request for penalty estimate."""
    statute: str = Field(..., min_length=2)
    violation_type: str = Field(..., min_length=3)
    days_of_violation: int = Field(default=1, ge=1)
    gravity: str = Field(default="moderate")
    economic_benefit: float = Field(default=0.0, ge=0)
    mitigating: List[str] = Field(default_factory=list)
    aggravating: List[str] = Field(default_factory=list)


class RemediationRequest(BaseModel):
    """Request for remediation technology recommendation."""
    contaminants: List[str] = Field(..., min_length=1)
    media: List[str] = Field(..., min_length=1)
    site_factors: Dict[str, Any] = Field(default_factory=dict)


class HealthResponse(BaseModel):
    """Health endpoint response."""
    engine_id: str
    engine_name: str
    version: str
    status: str
    port: int
    uptime_seconds: float
    domain: str
    tie_components: int
    doctrine_blocks: int
    doctrine_categories: int
    search_index_docs: int
    search_index_terms: int
    telemetry_summary: Dict[str, Any]
    doctrine_integrity: bool
    timestamp: str


# ============================================================================
# TIE COMPONENT 14: FACT FRAGILITY SCORING
# ============================================================================

class FactFragilityScorer:
    """Score the fragility of facts in an environmental analysis."""

    FRAGILE_INDICATORS: ClassVar[List[str]] = [
        "regulation may change",
        "proposed rule",
        "pending litigation",
        "circuit split",
        "under review",
        "stay pending",
        "interim final",
        "emergency rule",
        "voluntary program",
        "guidance document",
        "enforcement discretion",
        "case by case",
        "fact specific",
        "evolving standard",
        "no binding precedent",
        "administrative interpretation",
        "unsettled law",
        "recent amendment",
        "state varies",
        "jurisdiction specific",
    ]

    STABLE_INDICATORS: ClassVar[List[str]] = [
        "supreme court held",
        "statutory requirement",
        "mandatory",
        "shall",
        "no exception",
        "absolute prohibition",
        "self-executing",
        "clear statutory text",
        "well established",
        "long standing",
        "uniform across jurisdictions",
        "black letter law",
        "codified",
        "final rule",
    ]

    def score(self, analysis_text: str, topic: str = "") -> Dict[str, Any]:
        """Score the fragility of an analysis."""
        lowered = analysis_text.lower()
        fragile_count = sum(1 for ind in self.FRAGILE_INDICATORS if ind in lowered)
        stable_count = sum(1 for ind in self.STABLE_INDICATORS if ind in lowered)
        total = fragile_count + stable_count
        if total == 0:
            fragility_score = 0.50
        else:
            fragility_score = fragile_count / total
        fragile_items = [ind for ind in self.FRAGILE_INDICATORS if ind in lowered]
        stable_items = [ind for ind in self.STABLE_INDICATORS if ind in lowered]
        if fragility_score > 0.70:
            risk_label = "HIGHLY_FRAGILE"
        elif fragility_score > 0.40:
            risk_label = "MODERATELY_FRAGILE"
        else:
            risk_label = "STABLE"
        return {
            "fragility_score": round(fragility_score, 3),
            "risk_label": risk_label,
            "fragile_indicators_found": fragile_items,
            "stable_indicators_found": stable_items,
            "recommendation": self._recommendation(risk_label),
        }

    def _recommendation(self, risk_label: str) -> str:
        """Generate recommendation based on risk label."""
        if risk_label == "HIGHLY_FRAGILE":
            return "High fragility — verify current regulatory status; consider regulatory counsel; monitor for changes"
        elif risk_label == "MODERATELY_FRAGILE":
            return "Moderate fragility — some elements may shift; revalidate before relying on this analysis for major decisions"
        return "Stable analysis — grounded in established law and binding precedent"


# ============================================================================
# TIE COMPONENT 9: DOCTRINE DRIFT WATCHER
# ============================================================================

class DoctrineDriftWatcher:
    """Monitor for drift in doctrine cache vs current law."""

    def __init__(self) -> None:
        self._drift_registry: List[Dict[str, Any]] = []
        self._last_check: float = 0.0

    def check_drift(self) -> List[Dict[str, Any]]:
        """Check for potential doctrine drift."""
        drifts: List[Dict[str, Any]] = []
        stale = get_stale_doctrines(max_age_days=180)
        for topic in stale:
            drifts.append({
                "topic": topic,
                "drift_type": "stale_content",
                "description": f"Doctrine block '{topic}' has not been updated in 180+ days",
                "severity": "MEDIUM",
                "recommendation": "Review against current regulations and case law",
            })
        # Check for known evolving areas
        evolving_topics = {
            "tsca_pfas": "PFAS regulation is rapidly evolving (MCLs, CERCLA designation, state laws)",
            "caa_nsps": "NSPS OOOOb/OOOOc methane rules — implementation timeline and compliance dates",
            "permian_seismicity": "RRC seismicity orders and SRA designations change frequently",
            "environmental_justice": "EJ requirements expanding via EOs, guidance, and proposed regulations",
            "carbon_credits": "Carbon market regulations and SEC climate disclosure rules in flux",
            "cwa_npdes": "WOTUS definition post-Sackett v. EPA still being implemented",
        }
        for topic, reason in evolving_topics.items():
            block = get_doctrine_block(topic)
            if block:
                drifts.append({
                    "topic": topic,
                    "drift_type": "evolving_area",
                    "description": reason,
                    "severity": "LOW",
                    "recommendation": "Monitor federal register and agency websites for updates",
                })
        self._drift_registry = drifts
        self._last_check = time.time()
        return drifts

    def get_registry(self) -> List[Dict[str, Any]]:
        """Get current drift registry."""
        return self._drift_registry

    def get_summary(self) -> Dict[str, Any]:
        """Get drift watcher summary."""
        return {
            "total_drifts": len(self._drift_registry),
            "last_check": self._last_check,
            "by_severity": dict(Counter(d["severity"] for d in self._drift_registry)),
            "by_type": dict(Counter(d["drift_type"] for d in self._drift_registry)),
        }


# ============================================================================
# TIE COMPONENT 10: DOCTRINE COVERAGE MAP
# ============================================================================

class DoctrineCoverageMap:
    """Map of doctrine coverage with gap identification."""

    EXPECTED_DOMAINS: ClassVar[List[str]] = [
        "nepa", "air_quality", "water_quality", "hazardous_waste", "superfund",
        "toxic_substances", "endangered_species", "pesticides", "drinking_water",
        "oil_spill", "epcra_reporting", "tceq", "rrc", "permian_basin",
        "environmental_justice", "carbon_climate", "site_assessment",
        "compliance_enforcement", "toxic_tort", "environmental_insurance",
    ]

    def generate_report(self) -> Dict[str, Any]:
        """Generate coverage report identifying gaps."""
        coverage = get_coverage_map()
        covered_domains = set(coverage.keys())
        expected = set(self.EXPECTED_DOMAINS)
        gaps = expected - covered_domains
        extra = covered_domains - expected
        thin_domains: List[str] = []
        for domain, topics in coverage.items():
            if len(topics) < 2:
                thin_domains.append(domain)
        return {
            "total_domains_expected": len(expected),
            "total_domains_covered": len(covered_domains),
            "coverage_percentage": round(len(covered_domains & expected) / max(len(expected), 1) * 100, 1),
            "gap_domains": list(gaps),
            "extra_domains": list(extra),
            "thin_domains": thin_domains,
            "domain_block_counts": {k: len(v) for k, v in coverage.items()},
            "total_blocks": sum(len(v) for v in coverage.values()),
        }


# ============================================================================
# TIE COMPONENT 11: METRICS COLLECTOR
# ============================================================================

class EngineMetricsCollector:
    """Lightweight engine-level metrics."""

    def __init__(self) -> None:
        self.total_queries: int = 0
        self.doctrine_hits: int = 0
        self.doctrine_misses: int = 0
        self.search_hits: int = 0
        self.deep_analyses: int = 0
        self.errors: int = 0
        self.latencies: List[float] = []
        self._max_latencies: int = 500

    def record_query(self, latency_ms: float, doctrine_hit: bool, search_hit: bool, deep: bool) -> None:
        """Record a query completion."""
        self.total_queries += 1
        if doctrine_hit:
            self.doctrine_hits += 1
        else:
            self.doctrine_misses += 1
        if search_hit:
            self.search_hits += 1
        if deep:
            self.deep_analyses += 1
        self.latencies.append(latency_ms)
        if len(self.latencies) > self._max_latencies:
            self.latencies.pop(0)

    def record_error(self) -> None:
        """Record an error."""
        self.errors += 1

    def get_stats(self) -> Dict[str, Any]:
        """Get engine metrics."""
        avg_latency = sum(self.latencies) / max(len(self.latencies), 1)
        return {
            "total_queries": self.total_queries,
            "doctrine_hits": self.doctrine_hits,
            "doctrine_misses": self.doctrine_misses,
            "search_hits": self.search_hits,
            "deep_analyses": self.deep_analyses,
            "errors": self.errors,
            "avg_latency_ms": round(avg_latency, 2),
            "doctrine_hit_rate": round(self.doctrine_hits / max(self.total_queries, 1), 3),
        }


# ============================================================================
# TIE COMPONENT 13: ZONED ANALYSIS
# ============================================================================

class EnvironmentalZone(str, Enum):
    """Environmental analysis zones."""
    FEDERAL_STATUTE = "federal_statute"
    STATE_REGULATION = "state_regulation"
    PERMITTING = "permitting"
    ENFORCEMENT = "enforcement"
    LIABILITY = "liability"
    REMEDIATION = "remediation"
    TRANSACTION = "transaction"
    PERMIAN_BASIN = "permian_basin"
    CLIMATE_CARBON = "climate_carbon"


def detect_zone(query: str, domains: List[str]) -> EnvironmentalZone:
    """Detect the analysis zone from query and detected domains."""
    lowered = query.lower()
    if any(d in ("permian_basin",) for d in domains) or any(k in lowered for k in ["permian", "midland", "ector", "reeves"]):
        return EnvironmentalZone.PERMIAN_BASIN
    if any(k in lowered for k in ["permit", "application", "authorization", "approval"]):
        return EnvironmentalZone.PERMITTING
    if any(k in lowered for k in ["penalty", "enforcement", "violation", "citizen suit", "compliance"]):
        return EnvironmentalZone.ENFORCEMENT
    if any(k in lowered for k in ["liability", "prp", "cercla", "superfund", "cost recovery", "contribution"]):
        return EnvironmentalZone.LIABILITY
    if any(k in lowered for k in ["cleanup", "remediation", "corrective action", "removal", "treatment"]):
        return EnvironmentalZone.REMEDIATION
    if any(k in lowered for k in ["transaction", "phase i", "due diligence", "brownfield", "acquisition"]):
        return EnvironmentalZone.TRANSACTION
    if any(k in lowered for k in ["carbon", "climate", "ghg", "cap and trade", "offset"]):
        return EnvironmentalZone.CLIMATE_CARBON
    if any(k in lowered for k in ["tceq", "rrc", "texas", "30 tac", "16 tac"]):
        return EnvironmentalZone.STATE_REGULATION
    return EnvironmentalZone.FEDERAL_STATUTE


# ============================================================================
# TIE COMPONENT 16: DETERMINISM HASH
# ============================================================================

def compute_determinism_hash(
    query: str,
    response_text: str,
    confidence: float,
    version: str = ENGINE_VERSION,
    salt: str = "LG13_ENV_v1",
) -> str:
    """Compute a deterministic SHA-256 hash of the response."""
    content = f"{salt}:{version}:{query.strip().lower()}:{response_text[:500]}:{confidence:.4f}"
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


# ============================================================================
# TIE COMPONENT 19: MULTI-DOCTRINE DECOMPOSITION
# ============================================================================

class MultiDoctrineDecomposer:
    """Decompose a complex query into sub-doctrines for comprehensive analysis."""

    def decompose(self, query: str, norm_result: NormalizationResult) -> List[Dict[str, Any]]:
        """Decompose query into doctrine components."""
        components: List[Dict[str, Any]] = []
        for statute in norm_result.statutes_detected:
            block = get_doctrine_block(statute.lower())
            if block:
                components.append({
                    "type": "statute",
                    "identifier": statute,
                    "topic": block.topic,
                    "summary": block.summary[:200],
                    "confidence": block.confidence,
                })
        for domain in norm_result.environmental_domains:
            domain_blocks = get_doctrine_cache().get_by_category(domain)
            for block in domain_blocks[:3]:
                if not any(c["topic"] == block.topic for c in components):
                    components.append({
                        "type": "domain",
                        "identifier": domain,
                        "topic": block.topic,
                        "summary": block.summary[:200],
                        "confidence": block.confidence,
                    })
        for permit in norm_result.permit_types_detected:
            components.append({
                "type": "permit",
                "identifier": permit,
                "topic": f"permit_{permit}",
                "summary": f"Permit analysis for {permit} type",
                "confidence": 0.85,
            })
        return components


# ============================================================================
# CORE ENGINE
# ============================================================================

class EnvironmentalLawEngine:
    """Core environmental law analysis engine with all 20 TIE components."""

    def __init__(self) -> None:
        # TIE Component 3: Doctrine Cache
        self.doctrine_cache: DoctrineCacheIndex = build_doctrine_cache()
        # TIE Component 7: Search Index
        self.search_index: DoctrineSearchIndex = build_search_index(
            [b.to_dict() for b in DOCTRINE_BLOCKS]
        )
        # TIE Component 6: Semantic Normalization
        self.normalizer = get_normalizer()
        # TIE Component 8: Telemetry
        self.telemetry: TelemetryCollector = get_telemetry()
        # TIE Component 9: Drift Watcher
        self.drift_watcher = DoctrineDriftWatcher()
        # TIE Component 10: Coverage Map
        self.coverage_map = DoctrineCoverageMap()
        # TIE Component 11: Metrics
        self.metrics = EngineMetricsCollector()
        # TIE Component 14: Fact Fragility
        self.fragility_scorer = FactFragilityScorer()
        # TIE Component 19: Decomposer
        self.decomposer = MultiDoctrineDecomposer()
        # Domain analyzers
        self.permit_analyzer = PermitAnalyzer()
        self.prp_analyzer = CERCLAPRPAnalyzer()
        self.penalty_calculator = PenaltyCalculator()
        self.phase_i_workflow = PhaseIESAWorkflow()
        self.remediation_selector = RemediationSelector()
        self.compliance_checker = ComplianceChecker()
        # Boot time
        self._boot_time = time.time()
        logger.info(f"{ENGINE_NAME} v{ENGINE_VERSION} initialized: {self.doctrine_cache.total_blocks} doctrine blocks, "
                     f"{self.search_index.document_count} search docs")

    async def analyze(self, request: EnvironmentalQueryRequest) -> EnvironmentalQueryResponse:
        """Main analysis entrypoint implementing all 20 TIE components."""
        start = time.time()
        query = request.query
        trace = trace_query(
            query_text=query,
            response_mode=request.response_mode.value,
            analysis_layer=request.analysis_layer.value,
            jurisdiction=request.jurisdiction,
        )
        try:
            # TIE Component 6: Semantic Normalization
            t0 = time.time()
            norm = normalize_semantics(query)
            trace.add_sub_trace("semantic_normalization", (time.time() - t0) * 1000)
            trace.semantic_normalized = True
            trace.normalization_mapping = {m["from"]: m["to"] for m in norm.mappings_applied}
            trace.jurisdiction = norm.jurisdiction_detected or request.jurisdiction
            # TIE Component 13: Zoned Analysis
            zone = detect_zone(query, norm.environmental_domains)
            # TIE Component 1: Three-Layer Response
            # Layer 1: Doctrine Cache
            t1 = time.time()
            doctrine_result = self._layer_doctrine(query, norm)
            trace.add_sub_trace("doctrine_cache", (time.time() - t1) * 1000)
            # Layer 2: Search
            t2 = time.time()
            search_result = self._layer_search(query, norm, request.max_results)
            trace.add_sub_trace("search_index", (time.time() - t2) * 1000)
            # Layer 3: Deep Analysis (if requested or needed)
            deep_result: Optional[Dict[str, Any]] = None
            if request.analysis_layer == AnalysisLayer.DEEP or (
                doctrine_result["confidence"] < 0.65 and search_result["total_results"] < 3
            ):
                t3 = time.time()
                deep_result = self._layer_deep(query, norm, zone, doctrine_result, search_result)
                trace.add_sub_trace("deep_analysis", (time.time() - t3) * 1000)
            # TIE Component 19: Multi-doctrine decomposition
            components = self.decomposer.decompose(query, norm)
            # Aggregate confidence
            confidence = self._aggregate_confidence(doctrine_result, search_result, deep_result, norm)
            # TIE Component 5: Confidence Stratification
            conf_level = classify_confidence(confidence)
            # TIE Component 4: Authority Hardening
            primary_analysis = self._build_primary_analysis(
                doctrine_result, search_result, deep_result, norm, zone, request
            )
            primary_analysis = apply_authority_hardening(primary_analysis)
            # TIE Component 14: Fact Fragility
            fragility = self.fragility_scorer.score(primary_analysis, doctrine_result.get("matched_topic", ""))
            # Collect citations and practice tips
            citations = self._collect_citations(doctrine_result, search_result)
            practice_tips = self._collect_practice_tips(doctrine_result)
            # Texas notes
            texas_notes_text: Optional[str] = None
            if request.include_texas_notes:
                texas_notes_text = self._collect_texas_notes(doctrine_result, search_result)
            # Permian context
            permian_text: Optional[str] = None
            if request.include_permian_context:
                permian_text = self._build_permian_context(norm)
            # Penalty estimate
            penalty_dict: Optional[Dict[str, Any]] = None
            if request.include_penalty_estimate and norm.statutes_detected:
                penalty_dict = self._estimate_penalty(norm)
            # Determine response layer
            if doctrine_result["confidence"] >= 0.80:
                response_layer = "DOCTRINE_CACHE"
            elif search_result["total_results"] > 0:
                response_layer = "SEARCH_INDEX"
            elif deep_result:
                response_layer = "DEEP_ANALYSIS"
            else:
                response_layer = "FALLBACK"
            # TIE Component 16: Determinism Hash
            det_hash = compute_determinism_hash(query, primary_analysis, confidence)
            # Disclosure caveat
            caveat_key = "general"
            if zone == EnvironmentalZone.PERMITTING:
                caveat_key = "permit"
            elif zone == EnvironmentalZone.LIABILITY:
                caveat_key = "cercla"
            elif zone == EnvironmentalZone.ENFORCEMENT:
                caveat_key = "penalty"
            disclosure = DISCLOSURE_CAVEATS.get(caveat_key, DISCLOSURE_CAVEATS["general"])
            # Complete trace
            elapsed_ms = (time.time() - start) * 1000
            trace.complete(ResponseLayer(response_layer.lower()), confidence)
            trace.doctrine_blocks_matched = doctrine_result.get("blocks_matched", 0)
            trace.search_results_count = search_result.get("total_results", 0)
            trace.environmental_domain = ",".join(norm.environmental_domains[:5])
            trace.statute_referenced = ",".join(norm.statutes_detected[:5])
            trace.permit_type = ",".join(norm.permit_types_detected[:3])
            complete_trace(trace)
            # TIE Component 11: Metrics
            self.metrics.record_query(
                latency_ms=elapsed_ms,
                doctrine_hit=doctrine_result["confidence"] >= 0.80,
                search_hit=search_result["total_results"] > 0,
                deep=deep_result is not None,
            )
            # Record domain metrics
            for statute in norm.statutes_detected:
                self.telemetry.env_metrics.record_statute_query(statute)
            for contam in norm.contaminants_detected:
                self.telemetry.env_metrics.record_contaminant(contam)
            if norm.permit_types_detected:
                self.telemetry.env_metrics.record_permit_query()
            return EnvironmentalQueryResponse(
                query=query,
                normalized_query=norm.normalized_query,
                response_mode=request.response_mode.value,
                analysis_layer=request.analysis_layer.value,
                jurisdiction=norm.jurisdiction_detected or request.jurisdiction,
                doctrine_response=doctrine_result,
                search_response=search_result,
                deep_response=deep_result,
                primary_analysis=primary_analysis,
                statutes_applicable=norm.statutes_detected,
                agencies_involved=norm.agencies_detected,
                permits_relevant=norm.permit_types_detected,
                contaminants_identified=norm.contaminants_detected,
                environmental_domains=norm.environmental_domains,
                confidence=round(confidence, 4),
                confidence_level=conf_level.value,
                citations=citations,
                practice_tips=practice_tips,
                texas_notes=texas_notes_text,
                permian_context=permian_text,
                penalty_estimate=penalty_dict,
                disclosure_caveat=disclosure,
                normalization_info={
                    "mappings": norm.mappings_applied,
                    "duration_ms": round(norm.duration_ms, 2),
                    "hash": norm.normalization_hash,
                },
                search_results_count=search_result.get("total_results", 0),
                doctrine_blocks_matched=doctrine_result.get("blocks_matched", 0),
                response_layer=response_layer,
                determinism_hash=det_hash,
                trace_id=trace.trace_id,
                latency_ms=round(elapsed_ms, 2),
                timestamp=datetime.now(timezone.utc).isoformat(),
            )
        except Exception as exc:
            self.metrics.record_error()
            log_error(ErrorDomain.SYSTEM, str(exc), trace.trace_id)
            trace.error_message = str(exc)
            trace.error_domain = ErrorDomain.SYSTEM
            trace.complete(ResponseLayer.ERROR, 0.0)
            complete_trace(trace)
            raise HTTPException(status_code=500, detail=f"Analysis failed: {str(exc)[:200]}")

    def _layer_doctrine(self, query: str, norm: NormalizationResult) -> Dict[str, Any]:
        """Layer 1: Doctrine cache lookup."""
        best_block: Optional[DoctrineCacheBlock] = None
        best_confidence = 0.0
        blocks_checked = 0
        blocks_matched = 0
        # Direct topic match from statutes detected
        for statute in norm.statutes_detected:
            topic_key = statute.lower()
            block = get_doctrine_block(topic_key)
            if block and block.confidence > best_confidence:
                best_block = block
                best_confidence = block.confidence
                blocks_matched += 1
            blocks_checked += 1
        # Keyword search in cache
        cache_results = search_doctrines(query, max_results=5)
        for block in cache_results:
            blocks_checked += 1
            if block.confidence > best_confidence:
                best_block = block
                best_confidence = block.confidence
                blocks_matched += 1
        if best_block:
            return {
                "matched_topic": best_block.topic,
                "category": best_block.category,
                "summary": best_block.summary,
                "analysis": best_block.analysis,
                "authority": best_block.authority,
                "statute": best_block.statute,
                "cfr_reference": best_block.cfr_reference,
                "confidence": best_confidence + norm.confidence_boost,
                "cross_references": best_block.cross_references,
                "practice_tips": best_block.practice_tips,
                "penalties": best_block.penalties,
                "texas_notes": best_block.texas_notes,
                "block_hash": best_block.block_hash[:16],
                "blocks_checked": blocks_checked,
                "blocks_matched": blocks_matched,
            }
        return {
            "matched_topic": "",
            "category": "",
            "summary": "",
            "analysis": "",
            "authority": "",
            "confidence": 0.0,
            "blocks_checked": blocks_checked,
            "blocks_matched": 0,
        }

    def _layer_search(self, query: str, norm: NormalizationResult, max_results: int) -> Dict[str, Any]:
        """Layer 2: TF-IDF search over doctrine blocks."""
        results = self.search_index.search(query, top_k=max_results)
        if not results and norm.normalized_query != query:
            results = self.search_index.search(norm.normalized_query, top_k=max_results)
        formatted = []
        for r in results:
            formatted.append({
                "topic": r.topic,
                "category": r.category,
                "score": r.score,
                "snippet": r.snippet[:300],
                "statute": r.statute,
                "authority": r.authority,
            })
        return {
            "total_results": len(results),
            "results": formatted,
            "index_stats": self.search_index.get_stats(),
        }

    def _layer_deep(
        self,
        query: str,
        norm: NormalizationResult,
        zone: EnvironmentalZone,
        doctrine_result: Dict[str, Any],
        search_result: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Layer 3: Deep analysis combining all available information."""
        analysis_parts: List[str] = []
        # Gather from doctrine
        if doctrine_result.get("analysis"):
            analysis_parts.append(f"Doctrine Analysis: {doctrine_result['analysis']}")
        # Gather from search results
        for sr in search_result.get("results", [])[:5]:
            analysis_parts.append(f"Related ({sr['topic']}): {sr['snippet']}")
        # Zone-specific deep analysis
        if zone == EnvironmentalZone.PERMITTING:
            analysis_parts.append("Deep Permit Analysis: Evaluate all applicable federal, state, and local permit requirements. Consider pre-application meetings, public notice requirements, and administrative appeal rights.")
        elif zone == EnvironmentalZone.LIABILITY:
            analysis_parts.append("Deep Liability Analysis: Assess all four PRP categories, evaluate available defenses, analyze contribution and cost recovery options, review insurance coverage, and consider settlement strategy.")
        elif zone == EnvironmentalZone.REMEDIATION:
            analysis_parts.append("Deep Remediation Analysis: Evaluate remedy selection criteria (nine NCP criteria for CERCLA or RBCA for state programs), assess technology feasibility, estimate costs, and consider institutional controls.")
        elif zone == EnvironmentalZone.PERMIAN_BASIN:
            analysis_parts.append("Deep Permian Basin Analysis: Consider RRC jurisdiction vs. TCEQ, produced water disposal constraints, seismicity review requirements, methane emission rules, and local community impacts.")
        elif zone == EnvironmentalZone.ENFORCEMENT:
            analysis_parts.append("Deep Enforcement Analysis: Evaluate penalty exposure under applicable statutes, assess audit privilege applicability, consider SEP opportunities, and evaluate citizen suit risk.")
        # Cross-reference analysis
        cross_refs: List[str] = []
        if doctrine_result.get("cross_references"):
            for ref in doctrine_result["cross_references"]:
                ref_block = get_doctrine_block(ref)
                if ref_block:
                    cross_refs.append(f"{ref}: {ref_block.summary[:150]}")
        if cross_refs:
            analysis_parts.append("Cross-References: " + " | ".join(cross_refs))
        fragility = self.fragility_scorer.score(" ".join(analysis_parts))
        return {
            "zone": zone.value,
            "analysis": " ".join(analysis_parts),
            "cross_references_expanded": cross_refs,
            "fragility": fragility,
            "decomposition": [c["topic"] for c in self.decomposer.decompose(query, norm)],
        }

    def _aggregate_confidence(
        self,
        doctrine: Dict[str, Any],
        search: Dict[str, Any],
        deep: Optional[Dict[str, Any]],
        norm: NormalizationResult,
    ) -> float:
        """Aggregate confidence from all layers."""
        scores: List[float] = []
        doc_conf = doctrine.get("confidence", 0.0)
        if doc_conf > 0:
            scores.append(doc_conf * 1.5)
        search_count = search.get("total_results", 0)
        if search_count > 0:
            search_conf = min(0.70 + search_count * 0.02, 0.90)
            scores.append(search_conf)
        if deep:
            scores.append(0.75)
        if not scores:
            return 0.30 + norm.confidence_boost
        avg = sum(scores) / len(scores)
        return min(avg + norm.confidence_boost, 0.99)

    def _build_primary_analysis(
        self,
        doctrine: Dict[str, Any],
        search: Dict[str, Any],
        deep: Optional[Dict[str, Any]],
        norm: NormalizationResult,
        zone: EnvironmentalZone,
        request: EnvironmentalQueryRequest,
    ) -> str:
        """Build the primary analysis text."""
        parts: List[str] = []
        if request.response_mode == ResponseMode.FAST:
            if doctrine.get("summary"):
                parts.append(doctrine["summary"])
            return " ".join(parts) if parts else "No doctrine match found for this environmental query. Broaden your search or rephrase."
        if doctrine.get("summary"):
            parts.append(f"[Doctrine] {doctrine['summary']}")
        if doctrine.get("analysis") and request.response_mode in (ResponseMode.ANALYSIS, ResponseMode.MEMO):
            parts.append(f"[Analysis] {doctrine['analysis']}")
        if doctrine.get("authority"):
            parts.append(f"[Authority] {doctrine['authority']}")
        for sr in search.get("results", [])[:3]:
            if sr["topic"] != doctrine.get("matched_topic"):
                parts.append(f"[Related: {sr['topic']}] {sr['snippet']}")
        if deep and deep.get("analysis"):
            parts.append(f"[Deep Analysis — Zone: {deep['zone']}] {deep['analysis'][:800]}")
        if request.response_mode == ResponseMode.MEMO:
            parts.append("[Disclosure] " + DISCLOSURE_CAVEATS.get("general", ""))
        if not parts:
            parts.append("Environmental analysis could not be completed with available doctrine. Consider reformulating the query with specific statute references or regulatory program names.")
        return "\n\n".join(parts)

    def _collect_citations(self, doctrine: Dict[str, Any], search: Dict[str, Any]) -> List[str]:
        """Collect all citations from analysis."""
        citations: List[str] = []
        if doctrine.get("authority"):
            citations.append(doctrine["authority"])
        if doctrine.get("statute"):
            citations.append(f"Statute: {doctrine['statute']}")
        if doctrine.get("cfr_reference"):
            citations.append(f"CFR: {doctrine['cfr_reference']}")
        for sr in search.get("results", [])[:5]:
            if sr.get("authority") and sr["authority"] not in citations:
                citations.append(sr["authority"])
        return citations

    def _collect_practice_tips(self, doctrine: Dict[str, Any]) -> List[str]:
        """Collect practice tips."""
        tips: List[str] = doctrine.get("practice_tips", [])
        if not tips:
            tips.append("Verify current regulatory status — environmental regulations change frequently")
            tips.append("Confirm correct regulatory authority (TCEQ vs. RRC for Texas oil/gas operations)")
        return tips

    def _collect_texas_notes(self, doctrine: Dict[str, Any], search: Dict[str, Any]) -> Optional[str]:
        """Collect Texas-specific notes."""
        notes: List[str] = []
        if doctrine.get("texas_notes"):
            notes.append(doctrine["texas_notes"])
        for sr in search.get("results", [])[:5]:
            block = get_doctrine_block(sr["topic"])
            if block and block.texas_notes and block.texas_notes not in notes:
                notes.append(block.texas_notes)
        return " | ".join(notes) if notes else None

    def _build_permian_context(self, norm: NormalizationResult) -> Optional[str]:
        """Build Permian Basin context."""
        permian_blocks = get_doctrine_cache().get_by_category("permian_basin")
        if not permian_blocks:
            return None
        context_parts: List[str] = []
        for block in permian_blocks[:3]:
            context_parts.append(f"{block.topic}: {block.summary[:200]}")
        return " | ".join(context_parts)

    def _estimate_penalty(self, norm: NormalizationResult) -> Optional[Dict[str, Any]]:
        """Quick penalty estimate from detected statutes."""
        if not norm.statutes_detected:
            return None
        statute = norm.statutes_detected[0]
        stat_key = statute.split("_")[0].lower() if "_" in statute else statute.lower()
        try:
            result = self.penalty_calculator.calculate(
                statute=stat_key,
                violation_type="general violation",
                days_of_violation=1,
                gravity="moderate",
            )
            return {
                "statute": result.statute,
                "base_per_day": result.base_penalty_per_day,
                "statutory_maximum": result.statutory_maximum,
                "estimated_range_low": result.total_estimated_range_low,
                "estimated_range_high": result.total_estimated_range_high,
                "notes": result.calculation_notes,
            }
        except Exception:
            return None


# ============================================================================
# FASTAPI APPLICATION (TIE Component 17)
# ============================================================================

engine_instance: Optional[EnvironmentalLawEngine] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: initialize engine on startup."""
    global engine_instance
    logger.info(f"Starting {ENGINE_NAME} v{ENGINE_VERSION} on port {ENGINE_PORT}")
    engine_instance = EnvironmentalLawEngine()
    logger.info(f"{ENGINE_NAME} ready — {engine_instance.doctrine_cache.total_blocks} doctrine blocks loaded")
    yield
    logger.info(f"{ENGINE_NAME} shutting down")


app = FastAPI(
    title=ENGINE_NAME,
    version=ENGINE_VERSION,
    description="Comprehensive environmental law analysis engine — NEPA, CAA, CWA, RCRA, CERCLA, TSCA, ESA, FIFRA, SDWA, OPA, EPCRA, TCEQ, RRC, Permian Basin, carbon/climate, environmental justice, citizen suits",
    lifespan=lifespan,
)

# TIE Component 18: Loguru logging + CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CONFIG.get("api", {}).get("cors_origins", ["*"]),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_engine() -> EnvironmentalLawEngine:
    """Get the engine instance."""
    if engine_instance is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    return engine_instance


# ============================================================================
# ROUTES
# ============================================================================

# TIE Component 12: Health Endpoint
@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    """Health check endpoint."""
    eng = get_engine()
    integrity, _ = verify_doctrine_integrity()
    return HealthResponse(
        engine_id=ENGINE_ID,
        engine_name=ENGINE_NAME,
        version=ENGINE_VERSION,
        status="operational",
        port=ENGINE_PORT,
        uptime_seconds=round(time.time() - eng._boot_time, 1),
        domain=ENGINE_DOMAIN,
        tie_components=20,
        doctrine_blocks=eng.doctrine_cache.total_blocks,
        doctrine_categories=len(eng.doctrine_cache.categories),
        search_index_docs=eng.search_index.document_count,
        search_index_terms=eng.search_index.term_count,
        telemetry_summary=eng.telemetry.get_health(),
        doctrine_integrity=integrity,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


@app.post("/analyze", response_model=EnvironmentalQueryResponse)
async def analyze(request: EnvironmentalQueryRequest) -> EnvironmentalQueryResponse:
    """Main environmental law analysis endpoint."""
    eng = get_engine()
    return await eng.analyze(request)


@app.post("/query", response_model=EnvironmentalQueryResponse)
async def query_alias(request: EnvironmentalQueryRequest) -> EnvironmentalQueryResponse:
    """Alias for /analyze."""
    eng = get_engine()
    return await eng.analyze(request)


@app.post("/permits/analyze")
async def analyze_permits(request: PermitAnalysisRequest) -> Dict[str, Any]:
    """Analyze permit requirements for a proposed activity."""
    eng = get_engine()
    result = eng.permit_analyzer.analyze_permits(
        activity=request.activity,
        jurisdiction=request.jurisdiction,
        keywords=request.keywords,
    )
    return {
        "activity": result.activity_description,
        "jurisdiction": result.jurisdiction,
        "required_permits": [
            {
                "type": p.permit_type.value,
                "statute": p.statute,
                "agency": p.regulatory_agency,
                "description": p.description,
                "timeline_days": p.typical_timeline_days,
                "cost_range": p.estimated_cost_range,
                "penalties": p.penalties_for_noncompliance,
            }
            for p in result.required_permits
        ],
        "potentially_required": [
            {"type": p.permit_type.value, "statute": p.statute, "description": p.description}
            for p in result.potentially_required
        ],
        "recommended_sequence": result.recommended_sequence,
        "total_timeline_days": result.total_estimated_timeline_days,
        "compliance_notes": result.compliance_notes,
        "result_hash": result.result_hash,
    }


@app.post("/cercla/prp-assessment")
async def assess_prp(request: PRPAssessmentRequest) -> Dict[str, Any]:
    """Assess CERCLA PRP liability."""
    eng = get_engine()
    category_map = {
        "current_owner_operator": PRPCategory.CURRENT_OWNER_OPERATOR,
        "past_owner_operator": PRPCategory.PAST_OWNER_OPERATOR,
        "arranger": PRPCategory.ARRANGER,
        "transporter": PRPCategory.TRANSPORTER,
    }
    cat = category_map.get(request.category)
    if cat is None:
        raise HTTPException(status_code=400, detail=f"Invalid PRP category: {request.category}")
    result = eng.prp_analyzer.assess_liability(
        party_name=request.party_name,
        category=cat,
        facts=request.facts,
    )
    return {
        "party_name": result.party_name,
        "prp_category": result.prp_category.value,
        "liability_basis": result.liability_basis,
        "potential_defenses": result.potential_defenses,
        "defense_viability": result.defense_viability,
        "joint_several_exposure": result.joint_several_exposure,
        "estimated_share_range": result.estimated_share_range,
        "contribution_claim_targets": result.contribution_claim_targets,
        "key_facts_needed": result.key_facts_needed,
        "settlement_considerations": result.settlement_considerations,
        "statutory_citations": result.statutory_citations,
        "risk_level": result.risk_level,
        "analysis_hash": result.analysis_hash,
    }


@app.post("/compliance/check")
async def check_compliance(request: ComplianceCheckRequest) -> Dict[str, Any]:
    """Check multi-statute environmental compliance for a facility."""
    eng = get_engine()
    result = eng.compliance_checker.check_facility(
        facility_type=request.facility_type,
        activities=request.activities,
        jurisdiction=request.jurisdiction,
    )
    return {
        "facility_type": result.facility_type,
        "jurisdiction": result.jurisdiction,
        "applicable_statutes": result.applicable_statutes,
        "compliance_items": result.compliance_items,
        "high_risk_items": result.high_risk_items,
        "permits_required": result.permits_required,
        "reporting_obligations": result.reporting_obligations,
        "inspection_frequency": result.inspection_frequency,
        "overall_risk": result.overall_risk,
        "result_hash": result.result_hash,
    }


@app.post("/phase-i/checklist")
async def phase_i_checklist(request: PhaseIRequest) -> Dict[str, Any]:
    """Generate Phase I ESA checklist."""
    eng = get_engine()
    return eng.phase_i_workflow.generate_checklist(
        property_address=request.property_address,
        jurisdiction=request.jurisdiction,
    )


@app.post("/phase-i/assess")
async def phase_i_assess(request: PhaseIRequest) -> Dict[str, Any]:
    """Assess Phase I ESA findings."""
    eng = get_engine()
    result = eng.phase_i_workflow.assess_findings(
        property_address=request.property_address,
        findings=request.findings,
    )
    return {
        "property_address": result.property_address,
        "assessment_date": result.assessment_date,
        "recs_identified": result.recs_identified,
        "crecs_identified": result.crecs_identified,
        "hrecs_identified": result.hrecs_identified,
        "de_minimis_conditions": result.de_minimis_conditions,
        "data_gaps": result.data_gaps,
        "recommendation": result.recommendation,
        "phase_ii_needed": result.phase_ii_needed,
        "standard_applied": result.standard_applied,
        "result_hash": result.result_hash,
    }


@app.post("/penalty/estimate")
async def estimate_penalty(request: PenaltyRequest) -> Dict[str, Any]:
    """Estimate environmental penalty."""
    eng = get_engine()
    result = eng.penalty_calculator.calculate(
        statute=request.statute,
        violation_type=request.violation_type,
        days_of_violation=request.days_of_violation,
        gravity=request.gravity,
        economic_benefit=request.economic_benefit,
        mitigating=request.mitigating,
        aggravating=request.aggravating,
    )
    return {
        "statute": result.statute,
        "violation_type": result.violation_type,
        "base_penalty_per_day": result.base_penalty_per_day,
        "gravity_adjustment": result.gravity_adjustment,
        "economic_benefit_component": result.economic_benefit_component,
        "days_of_violation": result.days_of_violation,
        "total_estimated_range_low": result.total_estimated_range_low,
        "total_estimated_range_high": result.total_estimated_range_high,
        "mitigating_factors": result.mitigating_factors,
        "aggravating_factors": result.aggravating_factors,
        "statutory_maximum": result.statutory_maximum,
        "calculation_notes": result.calculation_notes,
        "penalty_hash": result.penalty_hash,
    }


@app.post("/remediation/recommend")
async def recommend_remediation(request: RemediationRequest) -> Dict[str, Any]:
    """Recommend remediation technologies."""
    eng = get_engine()
    options = eng.remediation_selector.recommend(
        contaminants=request.contaminants,
        media=request.media,
        site_factors=request.site_factors,
    )
    return {
        "contaminants": request.contaminants,
        "media": request.media,
        "recommendations": [
            {
                "technology": opt.technology.value,
                "description": opt.description,
                "applicability": opt.applicability,
                "target_media": opt.target_media,
                "target_contaminants": opt.target_contaminants,
                "duration_years": opt.estimated_duration_years,
                "cost_range": opt.estimated_cost_range,
                "effectiveness": opt.effectiveness,
                "limitations": opt.limitations,
                "regulatory_acceptance": opt.regulatory_acceptance,
            }
            for opt in options
        ],
    }


@app.get("/doctrines")
async def list_doctrines(category: Optional[str] = None) -> Dict[str, Any]:
    """List doctrine blocks, optionally filtered by category."""
    eng = get_engine()
    if category:
        blocks = eng.doctrine_cache.get_by_category(category)
    else:
        blocks = [get_doctrine_block(t) for t in eng.doctrine_cache.topics]
        blocks = [b for b in blocks if b is not None]
    return {
        "total": len(blocks),
        "blocks": [
            {
                "topic": b.topic,
                "category": b.category,
                "summary": b.summary[:200],
                "statute": b.statute,
                "confidence": b.confidence,
                "jurisdiction": b.jurisdiction,
            }
            for b in blocks
        ],
    }


@app.get("/doctrines/{topic}")
async def get_doctrine(topic: str) -> Dict[str, Any]:
    """Get a specific doctrine block by topic."""
    block = get_doctrine_block(topic)
    if not block:
        raise HTTPException(status_code=404, detail=f"Doctrine block '{topic}' not found")
    return block.to_dict()


@app.get("/coverage")
async def coverage_report() -> Dict[str, Any]:
    """Get doctrine coverage map and gap analysis."""
    eng = get_engine()
    return eng.coverage_map.generate_report()


@app.get("/drift")
async def drift_report() -> Dict[str, Any]:
    """Get doctrine drift analysis."""
    eng = get_engine()
    drifts = eng.drift_watcher.check_drift()
    return {
        "summary": eng.drift_watcher.get_summary(),
        "drifts": drifts,
    }


@app.get("/metrics")
async def engine_metrics() -> Dict[str, Any]:
    """Get engine performance metrics."""
    eng = get_engine()
    return {
        "engine_metrics": eng.metrics.get_stats(),
        "telemetry_health": eng.telemetry.get_health(),
        "environmental_metrics": eng.telemetry.env_metrics.get_stats(),
    }


@app.get("/telemetry")
async def telemetry_report() -> Dict[str, Any]:
    """Get full telemetry report."""
    eng = get_engine()
    return eng.telemetry.get_health()


@app.get("/integrity")
async def integrity_check() -> Dict[str, Any]:
    """Verify doctrine cache integrity."""
    valid, errors = verify_doctrine_integrity()
    cache_hash = get_doctrine_cache_hash()
    return {
        "integrity_valid": valid,
        "errors": errors,
        "cache_hash": cache_hash[:32],
        "total_blocks": len(DOCTRINE_BLOCKS),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/search")
async def search_endpoint(
    q: str = Query(..., min_length=2, description="Search query"),
    max_results: int = Query(default=10, ge=1, le=50),
) -> Dict[str, Any]:
    """Search doctrine blocks."""
    eng = get_engine()
    results = eng.search_index.search(q, top_k=max_results)
    return {
        "query": q,
        "total_results": len(results),
        "results": [
            {
                "topic": r.topic,
                "category": r.category,
                "score": r.score,
                "snippet": r.snippet[:300],
                "statute": r.statute,
                "authority": r.authority,
            }
            for r in results
        ],
    }


@app.get("/normalize")
async def normalize_endpoint(q: str = Query(..., min_length=2)) -> Dict[str, Any]:
    """Normalize an environmental law query."""
    result = normalize_semantics(q)
    return {
        "original": result.original_query,
        "normalized": result.normalized_query,
        "statutes": result.statutes_detected,
        "agencies": result.agencies_detected,
        "contaminants": result.contaminants_detected,
        "permit_types": result.permit_types_detected,
        "domains": result.environmental_domains,
        "jurisdiction": result.jurisdiction_detected,
        "confidence_boost": result.confidence_boost,
        "mappings": result.mappings_applied,
        "duration_ms": round(result.duration_ms, 2),
        "hash": result.normalization_hash,
    }


# TIE Component 15: Audit Trail JSONL
@app.get("/audit/verify")
async def verify_audit() -> Dict[str, Any]:
    """Verify audit trail hash chain integrity."""
    eng = get_engine()
    valid, count, error = eng.telemetry.audit.verify_chain()
    return {
        "chain_valid": valid,
        "entries_verified": count,
        "error": error,
        "total_entries": eng.telemetry.audit.entry_count,
        "last_hash": eng.telemetry.audit.last_hash[:16] + "...",
    }


# ============================================================================
# ADDITIONAL DOMAIN ANALYSIS CLASSES
# ============================================================================

class PermianBasinAnalyzer:
    """Specialized analyzer for Permian Basin environmental issues."""

    PERMIAN_COUNTIES: ClassVar[List[str]] = [
        "midland", "ector", "martin", "howard", "glasscock", "reeves",
        "pecos", "ward", "crane", "upton", "andrews", "gaines", "dawson",
        "loving", "winkler", "lea", "eddy", "culberson", "jeff davis",
    ]

    PERMIAN_ISSUES: ClassVar[Dict[str, Dict[str, Any]]] = {
        "produced_water": {
            "description": "Management and disposal of produced water from oil and gas operations",
            "regulatory_authority": "RRC (Statewide Rule 9, 16 TAC 3.9)",
            "key_requirements": [
                "No discharge of produced water to surface waters",
                "Disposal via Class II injection wells (UIC permit required)",
                "Recycling and beneficial reuse gaining regulatory support",
                "Surface spill reporting required (1 barrel threshold)",
                "Financial assurance for disposal wells",
            ],
            "current_issues": [
                "Induced seismicity from high-volume injection",
                "Recycling infrastructure development",
                "PFAS contamination in produced water",
                "Interstate produced water transport regulatory gaps",
                "Emerging beneficial reuse standards",
            ],
            "statutes": ["Texas Water Code Chapter 27", "SDWA Part C (42 USC 300h)"],
        },
        "flaring": {
            "description": "Flaring and venting of associated gas from oil production",
            "regulatory_authority": "RRC (Statewide Rule 32, 16 TAC 3.32)",
            "key_requirements": [
                "Flaring permit required beyond initial completion period",
                "No routine venting of gas (safety exceptions)",
                "Gas capture plan required for new drilling permits",
                "Reporting of flared/vented volumes monthly",
                "World Bank Zero Routine Flaring by 2030 endorsement",
            ],
            "current_issues": [
                "EPA OOOOb/OOOOc methane rules overlap",
                "IRA Waste Emissions Charge financial exposure",
                "ESG investor pressure on flaring intensity",
                "Midstream infrastructure buildout constraints",
                "Satellite monitoring by EPA and third parties",
            ],
            "statutes": ["Texas Natural Resources Code Section 85", "CAA Section 111"],
        },
        "seismicity": {
            "description": "Induced seismicity from saltwater disposal and hydraulic fracturing",
            "regulatory_authority": "RRC (Seismic Response Areas, 16 TAC 3.9)",
            "key_requirements": [
                "Seismic Response Area (SRA) designation authority",
                "Injection volume reductions or well suspensions in SRAs",
                "TexNet seismic monitoring network",
                "New disposal well permits require seismicity assessment",
                "Traffic light protocol for seismic events",
            ],
            "current_issues": [
                "Magnitude 5.0+ events (November 2022 Mentone area)",
                "Expanding SRA designations in Delaware Basin",
                "Correlation between deep Ellenburger injection and seismicity",
                "Shallow disposal alternatives (non-Ellenburger zones)",
                "Federal vs. state regulatory authority conflicts",
            ],
            "statutes": ["Texas Water Code Section 27.031", "16 TAC 3.9(6)(D)"],
        },
        "groundwater_contamination": {
            "description": "Groundwater contamination from oil and gas activities",
            "regulatory_authority": "TCEQ (groundwater quality) and RRC (oil/gas related)",
            "key_requirements": [
                "RRC casing and cementing requirements (Rule 13)",
                "Surface casing set through base of USDW",
                "Mechanical integrity testing for injection wells",
                "Groundwater monitoring may be required in permit conditions",
                "Corrective action for documented contamination",
            ],
            "current_issues": [
                "Legacy well integrity (pre-regulation wells)",
                "Horizontal drilling through shallow aquifer zones",
                "Chemical storage and handling at well sites",
                "Orphan well leakage to groundwater",
                "Agricultural water supply protection in irrigated areas",
            ],
            "statutes": ["Texas Water Code Chapter 26", "SDWA Part C"],
        },
    }

    def analyze_issue(self, issue_type: str, county: str = "") -> Dict[str, Any]:
        """Analyze a specific Permian Basin environmental issue."""
        issue = self.PERMIAN_ISSUES.get(issue_type)
        if not issue:
            available = list(self.PERMIAN_ISSUES.keys())
            return {
                "issue_type": issue_type,
                "found": False,
                "message": f"Unknown Permian Basin issue type. Available: {available}",
                "available_issues": available,
            }
        county_context = ""
        if county:
            county_lower = county.lower()
            if county_lower in self.PERMIAN_COUNTIES:
                county_context = f"County '{county}' is within the Permian Basin region"
            else:
                county_context = f"County '{county}' may not be within the core Permian Basin region"
        return {
            "issue_type": issue_type,
            "found": True,
            "description": issue["description"],
            "regulatory_authority": issue["regulatory_authority"],
            "key_requirements": issue["key_requirements"],
            "current_issues": issue["current_issues"],
            "applicable_statutes": issue["statutes"],
            "county_context": county_context,
            "confidence": 0.90,
        }

    def get_all_issues(self) -> Dict[str, str]:
        """Get a summary of all Permian Basin issues tracked."""
        return {k: v["description"] for k, v in self.PERMIAN_ISSUES.items()}

    def identify_issues_from_query(self, query: str) -> List[str]:
        """Identify which Permian Basin issues are relevant to a query."""
        lowered = query.lower()
        relevant: List[str] = []
        issue_keywords = {
            "produced_water": ["produced water", "saltwater disposal", "swd", "brine", "formation water"],
            "flaring": ["flaring", "flare", "venting", "associated gas", "gas capture"],
            "seismicity": ["seismic", "earthquake", "induced seismicity", "sra", "texnet"],
            "groundwater_contamination": ["groundwater", "aquifer", "water well", "contamination", "usdw"],
        }
        for issue, keywords in issue_keywords.items():
            if any(kw in lowered for kw in keywords):
                relevant.append(issue)
        return relevant


class MultiStatutePenaltyAnalyzer:
    """Analyze penalty exposure across multiple statutes simultaneously."""

    def __init__(self, penalty_calculator: PenaltyCalculator) -> None:
        self.calculator = penalty_calculator

    def analyze_multi_statute_exposure(
        self,
        violations: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Calculate aggregate penalty exposure across multiple statute violations."""
        results: List[Dict[str, Any]] = []
        total_low = 0.0
        total_high = 0.0
        statutes_involved: List[str] = []
        for violation in violations:
            statute = violation.get("statute", "")
            vtype = violation.get("violation_type", "general violation")
            days = violation.get("days", 1)
            gravity = violation.get("gravity", "moderate")
            econ_benefit = violation.get("economic_benefit", 0.0)
            mitigating = violation.get("mitigating", [])
            aggravating = violation.get("aggravating", [])
            try:
                estimate = self.calculator.calculate(
                    statute=statute,
                    violation_type=vtype,
                    days_of_violation=days,
                    gravity=gravity,
                    economic_benefit=econ_benefit,
                    mitigating_factors=mitigating,
                    aggravating_factors=aggravating,
                )
                entry = {
                    "statute": estimate.statute,
                    "violation_type": vtype,
                    "days": days,
                    "base_per_day": estimate.base_penalty_per_day,
                    "statutory_max": estimate.statutory_maximum,
                    "range_low": estimate.total_estimated_range_low,
                    "range_high": estimate.total_estimated_range_high,
                    "notes": estimate.calculation_notes,
                }
                results.append(entry)
                total_low += estimate.total_estimated_range_low
                total_high += estimate.total_estimated_range_high
                if statute not in statutes_involved:
                    statutes_involved.append(statute)
            except Exception as exc:
                results.append({
                    "statute": statute,
                    "violation_type": vtype,
                    "error": str(exc),
                })
        return {
            "violation_count": len(violations),
            "statutes_involved": statutes_involved,
            "individual_penalties": results,
            "aggregate_range_low": round(total_low, 2),
            "aggregate_range_high": round(total_high, 2),
            "notes": [
                "Aggregate penalties represent sum of individual statute exposures",
                "Actual enforcement may result in global settlement at lower total",
                "Criminal penalties not included in civil penalty estimates",
                "EPA penalty policies may allow penalty mitigation for compliance history, ability to pay, and settlement posture",
            ],
        }


class EnvironmentalTransactionAnalyzer:
    """Analyze environmental issues in real estate and business transactions."""

    TRANSACTION_TYPES: ClassVar[Dict[str, Dict[str, Any]]] = {
        "acquisition": {
            "description": "Purchase of real property or business with potential environmental liability",
            "key_steps": [
                "Phase I Environmental Site Assessment (ASTM E1527-21)",
                "Phase II Subsurface Investigation (if RECs identified)",
                "Environmental compliance audit of target operations",
                "Regulatory file review (EPA, state agency records)",
                "Environmental insurance evaluation (PLL, cost cap)",
                "Contractual protections (indemnification, escrow, representations)",
                "Post-closing compliance integration plan",
            ],
            "liability_frameworks": [
                "CERCLA strict liability (current owner/operator)",
                "RCRA corrective action obligations",
                "State cleanup program obligations",
                "Permit transfer requirements",
                "Financial assurance assumption",
            ],
            "defenses_available": [
                "Bona fide prospective purchaser (CERCLA 107(r))",
                "Innocent landowner (CERCLA 101(35))",
                "All appropriate inquiries (40 CFR 312)",
                "State VCP liability protections",
            ],
        },
        "lending": {
            "description": "Secured lending on properties with potential environmental contamination",
            "key_steps": [
                "Phase I ESA on collateral property",
                "Environmental risk assessment for underwriting",
                "Environmental insurance evaluation for borrower/lender",
                "Loan covenant environmental compliance requirements",
                "Monitoring during loan term",
                "Foreclosure environmental due diligence protocol",
            ],
            "liability_frameworks": [
                "Secured creditor exemption (CERCLA 101(20)(E))",
                "EPA Lender Liability Rule (40 CFR 300.1100)",
                "State secured creditor protections",
                "Asset Conservation Act of 1996",
            ],
            "defenses_available": [
                "Secured creditor exemption (maintain security interest, don't participate in management)",
                "Contiguous property owner defense (if applicable)",
                "EPA Lender Liability Final Rule protections",
            ],
        },
        "merger": {
            "description": "Corporate merger or asset purchase with environmental liability allocation",
            "key_steps": [
                "Environmental due diligence on all target facilities",
                "Historical operations analysis for legacy contamination",
                "Successor liability analysis (stock vs. asset purchase)",
                "Environmental liability quantification and allocation",
                "Representations, warranties, and indemnification negotiation",
                "Environmental insurance for gap coverage",
                "Post-closing integration of environmental programs",
            ],
            "liability_frameworks": [
                "CERCLA successor liability (stock purchase = automatic)",
                "State law successor liability theories (de facto merger, mere continuation, product line)",
                "RCRA permit transfer requirements",
                "Contractual liability allocation vs. statutory liability",
            ],
            "defenses_available": [
                "Asset purchase structure (limits automatic successor liability)",
                "Contractual indemnification from seller",
                "Environmental insurance (PLL, R&W)",
                "Escrow/holdback for known environmental costs",
            ],
        },
    }

    def analyze_transaction(self, transaction_type: str, details: Dict[str, Any] = None) -> Dict[str, Any]:
        """Analyze environmental considerations for a transaction type."""
        if details is None:
            details = {}
        txn = self.TRANSACTION_TYPES.get(transaction_type)
        if not txn:
            return {
                "transaction_type": transaction_type,
                "found": False,
                "available_types": list(self.TRANSACTION_TYPES.keys()),
            }
        risk_factors: List[str] = []
        if details.get("industrial_history"):
            risk_factors.append("Industrial history increases likelihood of contamination — Phase II recommended")
        if details.get("petroleum_operations"):
            risk_factors.append("Petroleum operations — check UST/AST registry, SPCC compliance, RRC well records")
        if details.get("near_superfund"):
            risk_factors.append("Proximity to Superfund site — potential contribution claim risk")
        if details.get("pre_1980"):
            risk_factors.append("Pre-1980 operations — increased risk of unregulated waste disposal, asbestos, PCBs, lead paint")
        return {
            "transaction_type": transaction_type,
            "found": True,
            "description": txn["description"],
            "recommended_steps": txn["key_steps"],
            "liability_frameworks": txn["liability_frameworks"],
            "available_defenses": txn["defenses_available"],
            "identified_risk_factors": risk_factors,
            "confidence": 0.90,
        }


class RegulatoryTimelineTracker:
    """Track regulatory deadlines and compliance milestones."""

    UPCOMING_DEADLINES: ClassVar[List[Dict[str, Any]]] = [
        {
            "regulation": "EPA NSPS OOOOb - New Source Requirements",
            "deadline": "March 2025 (effective date for new sources)",
            "affected_sectors": ["oil_gas_production", "midstream", "gas_processing"],
            "key_actions": ["Update LDAR programs", "Install zero-emission pneumatic devices", "Implement green completions"],
        },
        {
            "regulation": "EPA NSPS OOOOc - Existing Source Guidelines",
            "deadline": "State plans due 2026, compliance by 2028",
            "affected_sectors": ["oil_gas_production", "midstream"],
            "key_actions": ["Monitor state plan development", "Inventory existing sources", "Budget for retrofits"],
        },
        {
            "regulation": "IRA Waste Emissions Charge",
            "deadline": "2024 emissions (report 2025), $900/ton; 2025 emissions, $1,200/ton; 2026+, $1,500/ton",
            "affected_sectors": ["oil_gas_production", "midstream", "gas_processing", "refining"],
            "key_actions": ["Calculate GHGRP Subpart W emissions", "Identify exemption eligibility", "Implement methane reduction projects"],
        },
        {
            "regulation": "TSCA PFAS Reporting Rule",
            "deadline": "Reporting period closed November 2024",
            "affected_sectors": ["manufacturing", "chemical_processing", "oil_gas"],
            "key_actions": ["Verify reporting compliance", "Maintain records", "Monitor EPA enforcement"],
        },
        {
            "regulation": "EPA PFAS MCLs (SDWA)",
            "deadline": "Final rule April 2024, compliance by 2029",
            "affected_sectors": ["public_water_systems", "military", "industrial"],
            "key_actions": ["Monitor source water for PFAS", "Evaluate treatment technologies", "Plan capital improvements"],
        },
        {
            "regulation": "CERCLA PFAS Hazardous Substance Designation",
            "deadline": "Final rule 2024, effective 2025",
            "affected_sectors": ["manufacturing", "fire_departments", "military", "waste_disposal"],
            "key_actions": ["Assess potential PRP liability", "Review insurance coverage", "Implement source control"],
        },
        {
            "regulation": "RRC Gas Capture Plan Requirements",
            "deadline": "Ongoing — required with new drilling permits",
            "affected_sectors": ["oil_gas_production"],
            "key_actions": ["Submit gas capture plans with APDs", "Connect wells to gathering systems", "Minimize flaring"],
        },
        {
            "regulation": "TCEQ Edwards Aquifer Protection Program Updates",
            "deadline": "Ongoing — required before construction over contributing/recharge zones",
            "affected_sectors": ["development", "construction", "oil_gas"],
            "key_actions": ["Verify project location relative to recharge zones", "Prepare Water Pollution Abatement Plans", "Implement BMPs"],
        },
    ]

    def get_upcoming_deadlines(self, sector: str = "") -> List[Dict[str, Any]]:
        """Get upcoming regulatory deadlines, optionally filtered by sector."""
        if not sector:
            return self.UPCOMING_DEADLINES
        filtered: List[Dict[str, Any]] = []
        sector_lower = sector.lower().replace(" ", "_")
        for deadline in self.UPCOMING_DEADLINES:
            if any(sector_lower in s for s in deadline["affected_sectors"]):
                filtered.append(deadline)
        return filtered

    def get_deadlines_for_facility(self, facility_type: str, activities: List[str]) -> List[Dict[str, Any]]:
        """Get regulatory deadlines relevant to a specific facility."""
        relevant: List[Dict[str, Any]] = []
        keywords = [w.lower() for w in [facility_type] + activities]
        for deadline in self.UPCOMING_DEADLINES:
            desc_lower = deadline["regulation"].lower()
            actions_text = " ".join(deadline["key_actions"]).lower()
            sectors_text = " ".join(deadline["affected_sectors"]).lower()
            combined = f"{desc_lower} {actions_text} {sectors_text}"
            if any(kw in combined for kw in keywords):
                relevant.append(deadline)
        return relevant


class EnvironmentalAuditAnalyzer:
    """Analyze environmental audit privilege and self-disclosure programs."""

    STATE_AUDIT_PROGRAMS: ClassVar[Dict[str, Dict[str, Any]]] = {
        "texas": {
            "statute": "Texas Health and Safety Code Chapter 1101 (Environmental Health and Safety Audit Privilege Act)",
            "privilege": True,
            "immunity": True,
            "key_provisions": [
                "Audit reports are privileged and not admissible in civil, criminal, or administrative proceedings",
                "Voluntary disclosure immunity from penalties (not injunctive relief) if violation disclosed within 30 days",
                "Violation corrected within reasonable time (90 days default, extension available)",
                "Privilege does not apply to documents required by law to be created",
                "Privilege waivable; crime-fraud exception applies",
                "Disclosure must be voluntary — not triggered by complaint, monitoring, or government investigation",
            ],
            "limitations": [
                "Does not protect underlying facts — only audit conclusions/recommendations",
                "Does not apply if violation results in serious environmental harm or imminent danger",
                "Repeat violations of same type within 3 years not eligible for immunity",
                "Penalty immunity only — corrective action still required",
            ],
        },
        "epa_audit_policy": {
            "statute": "EPA Audit Policy (Incentives for Self-Policing: Discovery, Disclosure, Correction and Prevention of Violations, 65 FR 19618)",
            "privilege": False,
            "immunity": False,
            "key_provisions": [
                "Gravity-based penalty elimination (up to 100% reduction) for voluntary discovery and prompt disclosure",
                "Nine conditions: systematic discovery, voluntary discovery, prompt disclosure (21 days), independent discovery (not monitoring/third party), correction within 60 days, prevent recurrence, no repeat violations, no serious environmental harm, cooperation",
                "If all 9 conditions met: no gravity-based penalties and no criminal prosecution recommendations",
                "If 8 of 9 (except systematic discovery): 75% gravity-based penalty reduction",
                "Economic benefit still due even with penalty mitigation",
            ],
            "limitations": [
                "EPA does not recognize audit privilege — documents may be requested",
                "Does not prevent third-party citizen suits",
                "Criminal prosecution still possible for non-qualifying violations",
                "Does not apply to violations found through monitoring or required sampling",
            ],
        },
    }

    def analyze_audit_applicability(
        self,
        jurisdiction: str,
        violation_type: str,
        discovery_method: str,
        days_since_discovery: int = 0,
    ) -> Dict[str, Any]:
        """Analyze whether audit privilege/immunity may apply."""
        jurisdiction_lower = jurisdiction.lower()
        program = self.STATE_AUDIT_PROGRAMS.get(jurisdiction_lower)
        if not program:
            program = self.STATE_AUDIT_PROGRAMS.get("epa_audit_policy", {})
            jurisdiction_lower = "epa_audit_policy"
        eligible = True
        issues: List[str] = []
        if "monitoring" in discovery_method.lower() or "required" in discovery_method.lower():
            eligible = False
            issues.append("Violation discovered through monitoring/required activity — not voluntary discovery")
        if days_since_discovery > 30 and jurisdiction_lower == "texas":
            eligible = False
            issues.append(f"Texas requires disclosure within 30 days; {days_since_discovery} days elapsed")
        if days_since_discovery > 21 and jurisdiction_lower == "epa_audit_policy":
            eligible = False
            issues.append(f"EPA Audit Policy requires disclosure within 21 days; {days_since_discovery} days elapsed")
        return {
            "jurisdiction": jurisdiction_lower,
            "program": program.get("statute", ""),
            "privilege_available": program.get("privilege", False),
            "immunity_available": program.get("immunity", False),
            "preliminary_eligibility": eligible,
            "eligibility_issues": issues,
            "key_provisions": program.get("key_provisions", []),
            "limitations": program.get("limitations", []),
            "recommendation": self._recommendation(eligible, jurisdiction_lower),
        }

    def _recommendation(self, eligible: bool, jurisdiction: str) -> str:
        """Generate recommendation."""
        if eligible:
            return f"Audit privilege/immunity may be available under {jurisdiction} program — consult environmental counsel immediately to preserve privilege and meet disclosure deadlines"
        return "Audit privilege/immunity may not be available based on initial assessment — consult environmental counsel to evaluate alternatives including voluntary disclosure with penalty mitigation request"


class WaterRightsAnalyzer:
    """Analyze water rights issues relevant to environmental law."""

    TEXAS_WATER_RIGHTS: ClassVar[Dict[str, Any]] = {
        "surface_water": {
            "doctrine": "Prior Appropriation — first in time, first in right",
            "regulatory_authority": "TCEQ Water Rights Division",
            "key_principles": [
                "All surface water is property of the state",
                "Appropriative right required for diversion, storage, or use",
                "Seniority system based on priority date",
                "Beneficial use is the basis, measure, and limit of the right",
                "Domestic and livestock use exempt up to 200 acre-feet/year",
                "Environmental flows — SB 3 (2007) requires consideration of environmental needs",
            ],
            "permit_types": [
                "Water use permit (permanent appropriation)",
                "Temporary water use permit (up to 10 years)",
                "Emergency authorization",
                "Contractual authorization from existing permit holder",
                "Bed and banks authorization (transport through state watercourses)",
            ],
        },
        "groundwater": {
            "doctrine": "Rule of Capture (absolute ownership doctrine, modified by GCDs)",
            "regulatory_authority": "Groundwater Conservation Districts (GCDs)",
            "key_principles": [
                "Landowner owns groundwater beneath their property",
                "May pump without liability to neighbors (rule of capture)",
                "GCDs may regulate production to prevent waste/subsidence",
                "Desired Future Conditions (DFCs) set by GCDs through joint planning process",
                "Edwards Aquifer Authority — separate statutory authority with specific pumping caps",
                "EAA permit required for Edwards Aquifer use",
            ],
            "permit_types": [
                "GCD production permit",
                "GCD drilling permit",
                "GCD transport permit (export outside district)",
                "Edwards Aquifer Authority Initial Regular Permit",
                "Edwards Aquifer Authority Term Permit",
            ],
        },
        "produced_water": {
            "doctrine": "Jurisdictionally split — RRC for oil/gas operations, TCEQ for other",
            "regulatory_authority": "RRC (production), TCEQ (if removed from oil/gas context)",
            "key_principles": [
                "Produced water is waste under RRC jurisdiction during oil/gas operations",
                "Disposal via Class II injection wells (RRC permit required)",
                "Beneficial reuse emerging — RRC and TCEQ developing regulatory framework",
                "Surface discharge generally prohibited",
                "HB 2771 (2023) clarified produced water ownership and reuse authority",
            ],
            "permit_types": [
                "RRC Class II disposal well permit",
                "RRC recycling/reuse authorization",
                "TCEQ permit if water enters surface water or groundwater system",
            ],
        },
    }

    def analyze_water_right(self, water_type: str, use_description: str = "") -> Dict[str, Any]:
        """Analyze water rights framework for a given water type."""
        water_type_lower = water_type.lower().replace(" ", "_")
        framework = self.TEXAS_WATER_RIGHTS.get(water_type_lower)
        if not framework:
            return {
                "water_type": water_type,
                "found": False,
                "available_types": list(self.TEXAS_WATER_RIGHTS.keys()),
            }
        return {
            "water_type": water_type,
            "found": True,
            "doctrine": framework["doctrine"],
            "regulatory_authority": framework["regulatory_authority"],
            "key_principles": framework["key_principles"],
            "permit_types": framework["permit_types"],
            "confidence": 0.90,
        }


class StatutoryMaximaPenaltyReference:
    """Reference table for statutory maxima across all major environmental statutes."""

    STATUTORY_MAXIMA: ClassVar[Dict[str, Dict[str, Any]]] = {
        "caa": {
            "statute": "Clean Air Act Section 113",
            "civil_per_day": 109024,
            "criminal_knowing": "$1M and/or 5 years",
            "criminal_negligent": "$100K and/or 1 year",
            "criminal_knowing_endangerment": "$1M and/or 15 years",
            "administrative_per_day": 44539,
            "notes": "IFR adjusted annually; criminal penalties per individual",
        },
        "cwa": {
            "statute": "Clean Water Act Section 309",
            "civil_per_day": 64618,
            "criminal_knowing": "$100K/day and/or 6 years (double for repeat)",
            "criminal_negligent": "$50K/day and/or 2 years",
            "administrative_class_i_per_violation": 21952,
            "administrative_class_i_max": 54884,
            "administrative_class_ii_per_day": 21952,
            "administrative_class_ii_max": 329166,
            "notes": "Oil and hazardous substance penalties under Section 311 separate",
        },
        "rcra": {
            "statute": "RCRA Section 3008",
            "civil_per_day": 70117,
            "criminal_knowing": "$50K/day and/or 5 years",
            "criminal_knowing_endangerment": "$250K and/or 15 years ($1M for org)",
            "administrative_per_day": 70117,
            "notes": "RCRA corrective action costs additional to penalties",
        },
        "cercla": {
            "statute": "CERCLA Section 109",
            "class_i_per_violation": 64618,
            "class_ii_per_day": 64618,
            "class_ii_max": 193853,
            "failure_to_notify": 70117,
            "treble_damages": "3x cleanup costs for failure to comply with EPA order without sufficient cause",
            "notes": "PRP liability for response costs uncapped; penalties separate",
        },
        "tsca": {
            "statute": "TSCA Section 16",
            "civil_per_day": 47756,
            "criminal_knowing": "$50K/day and/or 1 year",
            "notes": "PFAS-specific provisions may increase future penalties",
        },
        "sdwa": {
            "statute": "Safe Drinking Water Act Section 1414",
            "civil_per_day": 64618,
            "administrative_per_day": 21952,
            "uic_per_day": 32309,
            "notes": "UIC penalties separate from PWS penalties",
        },
        "fifra": {
            "statute": "FIFRA Section 14",
            "commercial_per_violation": 21952,
            "private_per_violation": 1300,
            "knowing_commercial": "$50K and/or 1 year",
            "notes": "Private applicator penalties significantly lower than commercial",
        },
        "epcra": {
            "statute": "EPCRA Section 325",
            "section_302_per_day": 64618,
            "section_304_per_violation": 64618,
            "section_311_312_per_day": 64618,
            "section_313_per_day": 47756,
            "notes": "Citizen suit penalties available under Section 326",
        },
    }

    def get_maxima(self, statute: str) -> Dict[str, Any]:
        """Get statutory maxima for a statute."""
        statute_lower = statute.lower()
        data = self.STATUTORY_MAXIMA.get(statute_lower)
        if not data:
            return {"statute": statute, "found": False, "available": list(self.STATUTORY_MAXIMA.keys())}
        return {"statute": statute, "found": True, **data}

    def get_all_maxima(self) -> Dict[str, Dict[str, Any]]:
        """Get all statutory maxima."""
        return self.STATUTORY_MAXIMA

    def compare_statutes(self, statutes: List[str]) -> List[Dict[str, Any]]:
        """Compare penalty maxima across multiple statutes."""
        results: List[Dict[str, Any]] = []
        for s in statutes:
            data = self.get_maxima(s)
            if data.get("found"):
                results.append(data)
        return results


class EnvironmentalDocumentGenerator:
    """Generate structured environmental analysis documents."""

    def generate_memo_header(self, subject: str, date: str, author: str = "LG13 Environmental Law Engine") -> str:
        """Generate a legal memo header."""
        return (
            f"MEMORANDUM\n"
            f"{'='*60}\n"
            f"TO:      [Client/File]\n"
            f"FROM:    {author}\n"
            f"DATE:    {date}\n"
            f"RE:      {subject}\n"
            f"{'='*60}\n\n"
            f"PRIVILEGED AND CONFIDENTIAL\n"
            f"ATTORNEY-CLIENT COMMUNICATION\n"
            f"{'='*60}\n"
        )

    def generate_compliance_matrix(
        self,
        facility_type: str,
        activities: List[str],
        compliance_results: List[ComplianceCheckResult],
    ) -> Dict[str, Any]:
        """Generate a compliance requirement matrix."""
        matrix_rows: List[Dict[str, Any]] = []
        for result in compliance_results:
            matrix_rows.append({
                "statute": result.statute,
                "program": result.program,
                "applicable": result.applicable,
                "requirements": result.requirements,
                "compliance_status": result.compliance_status if hasattr(result, "compliance_status") else "UNKNOWN",
                "priority": result.priority if hasattr(result, "priority") else "MEDIUM",
            })
        return {
            "facility_type": facility_type,
            "activities": activities,
            "matrix": matrix_rows,
            "total_programs": len(matrix_rows),
            "applicable_programs": sum(1 for r in matrix_rows if r["applicable"]),
        }

    def generate_penalty_summary(
        self,
        penalties: List[PenaltyEstimate],
    ) -> Dict[str, Any]:
        """Generate a penalty exposure summary."""
        total_low = sum(p.total_estimated_range_low for p in penalties)
        total_high = sum(p.total_estimated_range_high for p in penalties)
        return {
            "total_violations": len(penalties),
            "aggregate_exposure_low": round(total_low, 2),
            "aggregate_exposure_high": round(total_high, 2),
            "by_statute": [
                {
                    "statute": p.statute,
                    "range_low": p.total_estimated_range_low,
                    "range_high": p.total_estimated_range_high,
                    "per_day_rate": p.base_penalty_per_day,
                }
                for p in penalties
            ],
        }


class EnvironmentalDueDiligenceWorkflow:
    """Comprehensive environmental due diligence workflow for transactions."""

    WORKFLOW_STEPS: ClassVar[List[Dict[str, Any]]] = [
        {
            "phase": 1,
            "name": "Preliminary Screening",
            "duration_days": "3-5",
            "tasks": [
                "Review publicly available environmental data (EPA Envirofacts, TCEQ Central Registry, RRC GIS)",
                "Screen for proximity to known contaminated sites (NPL, state superfund, brownfield)",
                "Review historical aerial photographs for prior land use",
                "Identify potential environmental justice concerns",
                "Determine applicable regulatory framework",
            ],
        },
        {
            "phase": 2,
            "name": "Phase I Environmental Site Assessment",
            "duration_days": "15-30",
            "tasks": [
                "Engage qualified Environmental Professional (EP)",
                "Records review: federal, state, tribal, local environmental databases",
                "Historical review: Sanborn maps, city directories, chain of title",
                "Site reconnaissance: visual inspection for RECs",
                "Interviews: current/past owners, occupants, local officials",
                "User-provided information review",
                "Report preparation with findings, opinions, conclusions",
                "Identify Recognized Environmental Conditions (RECs), Controlled RECs (CRECs), Historical RECs (HRECs)",
            ],
        },
        {
            "phase": 3,
            "name": "Phase II Subsurface Investigation",
            "duration_days": "30-60",
            "tasks": [
                "Develop Sampling and Analysis Plan (SAP)",
                "Obtain access agreements and permits",
                "Soil sampling (borings, test pits, surface sampling)",
                "Groundwater sampling (monitoring wells, grab samples)",
                "Soil gas sampling (if vapor intrusion concern)",
                "Laboratory analysis for COCs identified in Phase I",
                "Data evaluation against screening levels (EPA RSLs, TCEQ PCLs)",
                "Conceptual site model development",
                "Risk characterization and cleanup cost estimation",
            ],
        },
        {
            "phase": 4,
            "name": "Risk Assessment and Liability Quantification",
            "duration_days": "15-30",
            "tasks": [
                "Human health risk assessment (residential/commercial/industrial exposure scenarios)",
                "Ecological risk assessment (if sensitive receptors present)",
                "Cleanup cost estimation (remedial alternatives analysis)",
                "Regulatory pathway selection (CERCLA, RCRA, state VCP, self-directed)",
                "Liability allocation analysis (PRP status, available defenses)",
                "Environmental insurance feasibility assessment",
                "Financial modeling of environmental costs (NPV, risk-adjusted)",
            ],
        },
        {
            "phase": 5,
            "name": "Transaction Structuring and Closure",
            "duration_days": "15-45",
            "tasks": [
                "Environmental representations and warranties drafting",
                "Indemnification provisions (scope, duration, caps, baskets)",
                "Escrow/holdback calculation for known environmental costs",
                "Environmental insurance placement (PLL, cost cap, R&W)",
                "Permit transfer applications",
                "Regulatory notification (if applicable)",
                "Post-closing compliance transition planning",
                "Environmental management system integration",
            ],
        },
    ]

    def get_workflow(self, transaction_type: str = "acquisition") -> Dict[str, Any]:
        """Get the full due diligence workflow."""
        total_tasks = sum(len(step["tasks"]) for step in self.WORKFLOW_STEPS)
        return {
            "transaction_type": transaction_type,
            "total_phases": len(self.WORKFLOW_STEPS),
            "total_tasks": total_tasks,
            "estimated_duration": "78-170 days (depending on complexity)",
            "phases": self.WORKFLOW_STEPS,
        }

    def get_phase(self, phase_number: int) -> Optional[Dict[str, Any]]:
        """Get a specific phase of the workflow."""
        for step in self.WORKFLOW_STEPS:
            if step["phase"] == phase_number:
                return step
        return None


# ============================================================================
# EXTENDED ENGINE METHODS
# ============================================================================

# Attach additional analyzers to the engine class
def _init_extended_analyzers(engine: EnvironmentalLawEngine) -> None:
    """Initialize extended analyzers on the engine instance."""
    engine.permian_analyzer = PermianBasinAnalyzer()
    engine.multi_penalty_analyzer = MultiStatutePenaltyAnalyzer(engine.penalty_calculator)
    engine.transaction_analyzer = EnvironmentalTransactionAnalyzer()
    engine.timeline_tracker = RegulatoryTimelineTracker()
    engine.audit_analyzer = EnvironmentalAuditAnalyzer()
    engine.water_rights_analyzer = WaterRightsAnalyzer()
    engine.statutory_maxima = StatutoryMaximaPenaltyReference()
    engine.doc_generator = EnvironmentalDocumentGenerator()
    engine.dd_workflow = EnvironmentalDueDiligenceWorkflow()


# Patch the engine __init__ to include extended analyzers
_original_init = EnvironmentalLawEngine.__init__


def _patched_init(self: EnvironmentalLawEngine) -> None:
    """Patched init that includes extended analyzers."""
    _original_init(self)
    _init_extended_analyzers(self)


EnvironmentalLawEngine.__init__ = _patched_init  # type: ignore[method-assign]


# ============================================================================
# EXTENDED PYDANTIC MODELS
# ============================================================================

class PermianIssueRequest(BaseModel):
    """Request for Permian Basin issue analysis."""
    issue_type: str = Field(..., min_length=2, description="Issue type: produced_water|flaring|seismicity|groundwater_contamination")
    county: str = Field(default="", description="County name for context")


class MultiPenaltyRequest(BaseModel):
    """Request for multi-statute penalty analysis."""
    violations: List[Dict[str, Any]] = Field(..., min_length=1, description="List of violations with statute, type, days, gravity")


class TransactionRequest(BaseModel):
    """Request for transaction environmental analysis."""
    transaction_type: str = Field(..., description="acquisition|lending|merger")
    details: Dict[str, Any] = Field(default_factory=dict)


class AuditPrivilegeRequest(BaseModel):
    """Request for audit privilege analysis."""
    jurisdiction: str = Field(default="texas")
    violation_type: str = Field(default="general")
    discovery_method: str = Field(..., min_length=3)
    days_since_discovery: int = Field(default=0, ge=0)


class WaterRightsRequest(BaseModel):
    """Request for water rights analysis."""
    water_type: str = Field(..., description="surface_water|groundwater|produced_water")
    use_description: str = Field(default="")


class RegulatoryTimelineRequest(BaseModel):
    """Request for regulatory timeline deadlines."""
    sector: str = Field(default="", description="Industry sector filter")
    facility_type: str = Field(default="")
    activities: List[str] = Field(default_factory=list)


class StatutoryMaximaRequest(BaseModel):
    """Request for statutory penalty maxima."""
    statutes: List[str] = Field(..., min_length=1)


class DueDiligenceRequest(BaseModel):
    """Request for due diligence workflow."""
    transaction_type: str = Field(default="acquisition")
    phase: Optional[int] = Field(default=None, ge=1, le=5)


class MemoRequest(BaseModel):
    """Request for environmental memo generation."""
    query: str = Field(..., min_length=5)
    subject: str = Field(default="Environmental Analysis")
    jurisdiction: str = Field(default="TX")
    include_penalty_analysis: bool = Field(default=False)
    include_compliance_matrix: bool = Field(default=False)
    include_permian_context: bool = Field(default=False)


class BatchQueryRequest(BaseModel):
    """Request for batch query processing."""
    queries: List[str] = Field(..., min_length=1, max_length=10)
    response_mode: ResponseMode = Field(default=ResponseMode.FAST)
    jurisdiction: str = Field(default="TX")


# ============================================================================
# EXTENDED API ENDPOINTS
# ============================================================================

@app.post("/permian/analyze")
async def analyze_permian_issue(request: PermianIssueRequest) -> Dict[str, Any]:
    """Analyze a specific Permian Basin environmental issue."""
    eng = get_engine()
    result = eng.permian_analyzer.analyze_issue(request.issue_type, request.county)
    return result


@app.get("/permian/issues")
async def get_permian_issues() -> Dict[str, Any]:
    """Get all tracked Permian Basin environmental issues."""
    eng = get_engine()
    return {
        "issues": eng.permian_analyzer.get_all_issues(),
        "counties": eng.permian_analyzer.PERMIAN_COUNTIES,
    }


@app.post("/penalty/multi-statute")
async def multi_statute_penalty(request: MultiPenaltyRequest) -> Dict[str, Any]:
    """Calculate aggregate penalty exposure across multiple statutes."""
    eng = get_engine()
    result = eng.multi_penalty_analyzer.analyze_multi_statute_exposure(request.violations)
    return result


@app.get("/penalty/maxima")
async def get_penalty_maxima(
    statute: str = Query(default="", description="Specific statute to look up"),
) -> Dict[str, Any]:
    """Get statutory penalty maxima reference."""
    eng = get_engine()
    if statute:
        return eng.statutory_maxima.get_maxima(statute)
    return {"statutes": eng.statutory_maxima.get_all_maxima()}


@app.post("/penalty/compare")
async def compare_penalty_maxima(request: StatutoryMaximaRequest) -> Dict[str, Any]:
    """Compare penalty maxima across statutes."""
    eng = get_engine()
    results = eng.statutory_maxima.compare_statutes(request.statutes)
    return {"comparison": results, "statutes_requested": request.statutes}


@app.post("/transaction/analyze")
async def analyze_transaction(request: TransactionRequest) -> Dict[str, Any]:
    """Analyze environmental considerations for a transaction."""
    eng = get_engine()
    result = eng.transaction_analyzer.analyze_transaction(request.transaction_type, request.details)
    return result


@app.post("/audit/privilege")
async def analyze_audit_privilege(request: AuditPrivilegeRequest) -> Dict[str, Any]:
    """Analyze environmental audit privilege/immunity applicability."""
    eng = get_engine()
    result = eng.audit_analyzer.analyze_audit_applicability(
        jurisdiction=request.jurisdiction,
        violation_type=request.violation_type,
        discovery_method=request.discovery_method,
        days_since_discovery=request.days_since_discovery,
    )
    return result


@app.post("/water-rights/analyze")
async def analyze_water_rights(request: WaterRightsRequest) -> Dict[str, Any]:
    """Analyze water rights framework."""
    eng = get_engine()
    result = eng.water_rights_analyzer.analyze_water_right(request.water_type, request.use_description)
    return result


@app.get("/timeline/deadlines")
async def get_regulatory_deadlines(
    sector: str = Query(default="", description="Industry sector filter"),
) -> Dict[str, Any]:
    """Get upcoming regulatory deadlines."""
    eng = get_engine()
    deadlines = eng.timeline_tracker.get_upcoming_deadlines(sector)
    return {"deadlines": deadlines, "total": len(deadlines), "sector_filter": sector or "all"}


@app.post("/timeline/facility")
async def get_facility_deadlines(request: RegulatoryTimelineRequest) -> Dict[str, Any]:
    """Get regulatory deadlines relevant to a specific facility."""
    eng = get_engine()
    deadlines = eng.timeline_tracker.get_deadlines_for_facility(request.facility_type, request.activities)
    return {"deadlines": deadlines, "total": len(deadlines)}


@app.post("/due-diligence/workflow")
async def get_due_diligence_workflow(request: DueDiligenceRequest) -> Dict[str, Any]:
    """Get environmental due diligence workflow."""
    eng = get_engine()
    if request.phase:
        phase = eng.dd_workflow.get_phase(request.phase)
        if not phase:
            raise HTTPException(status_code=404, detail=f"Phase {request.phase} not found")
        return {"phase": phase}
    return eng.dd_workflow.get_workflow(request.transaction_type)


@app.post("/memo/generate")
async def generate_memo(request: MemoRequest) -> Dict[str, Any]:
    """Generate a structured environmental analysis memo."""
    eng = get_engine()
    # Run the full analysis
    query_request = EnvironmentalQueryRequest(
        query=request.query,
        response_mode=ResponseMode.MEMO,
        analysis_layer=AnalysisLayer.DEEP,
        jurisdiction=request.jurisdiction,
        include_texas_notes=True,
        include_permian_context=request.include_permian_context,
        include_penalty_estimate=request.include_penalty_analysis,
    )
    analysis = await eng.analyze(query_request)
    # Build memo structure
    memo_date = datetime.now(timezone.utc).strftime("%B %d, %Y")
    header = eng.doc_generator.generate_memo_header(request.subject, memo_date)
    sections: List[Dict[str, str]] = [
        {"title": "I. QUESTION PRESENTED", "content": request.query},
        {"title": "II. SHORT ANSWER", "content": analysis.primary_analysis[:500] if analysis.primary_analysis else "Further analysis required."},
        {"title": "III. APPLICABLE LAW", "content": "\n".join(f"- {c}" for c in analysis.citations) if analysis.citations else "No specific statutes identified."},
        {"title": "IV. ANALYSIS", "content": analysis.primary_analysis},
    ]
    if analysis.texas_notes:
        sections.append({"title": "V. TEXAS-SPECIFIC CONSIDERATIONS", "content": analysis.texas_notes})
    if analysis.penalty_estimate:
        sections.append({"title": "VI. PENALTY EXPOSURE", "content": json.dumps(analysis.penalty_estimate, indent=2)})
    if analysis.practice_tips:
        sections.append({"title": "VII. PRACTICE TIPS", "content": "\n".join(f"- {t}" for t in analysis.practice_tips)})
    sections.append({"title": "VIII. CONCLUSION AND DISCLAIMER", "content": analysis.disclosure_caveat})
    return {
        "header": header,
        "sections": sections,
        "confidence": analysis.confidence,
        "confidence_level": analysis.confidence_level,
        "determinism_hash": analysis.determinism_hash,
        "statutes": analysis.statutes_applicable,
        "domains": analysis.environmental_domains,
        "timestamp": analysis.timestamp,
    }


@app.post("/batch/analyze")
async def batch_analyze(request: BatchQueryRequest) -> Dict[str, Any]:
    """Process multiple environmental queries in batch."""
    eng = get_engine()
    results: List[Dict[str, Any]] = []
    for query_text in request.queries:
        try:
            query_req = EnvironmentalQueryRequest(
                query=query_text,
                response_mode=request.response_mode,
                jurisdiction=request.jurisdiction,
            )
            analysis = await eng.analyze(query_req)
            results.append({
                "query": query_text,
                "success": True,
                "confidence": analysis.confidence,
                "confidence_level": analysis.confidence_level,
                "primary_analysis": analysis.primary_analysis[:500],
                "statutes": analysis.statutes_applicable,
                "domains": analysis.environmental_domains,
                "determinism_hash": analysis.determinism_hash,
            })
        except Exception as exc:
            results.append({
                "query": query_text,
                "success": False,
                "error": str(exc)[:200],
            })
    return {
        "total_queries": len(request.queries),
        "successful": sum(1 for r in results if r.get("success")),
        "failed": sum(1 for r in results if not r.get("success")),
        "results": results,
    }


@app.get("/statutes/reference")
async def get_statute_reference(
    category: str = Query(default="", description="Filter by category"),
) -> Dict[str, Any]:
    """Get environmental statute reference information."""
    eng = get_engine()
    cache = eng.doctrine_cache
    if category:
        blocks = cache.get_by_category(category)
    else:
        blocks = DOCTRINE_BLOCKS
    statutes: List[Dict[str, Any]] = []
    seen: Set[str] = set()
    for block in blocks:
        if block.statute and block.statute not in seen:
            statutes.append({
                "statute": block.statute,
                "cfr_reference": block.cfr_reference,
                "topic": block.topic,
                "category": block.category,
                "authority": block.authority,
            })
            seen.add(block.statute)
    return {
        "total_statutes": len(statutes),
        "category_filter": category or "all",
        "statutes": statutes,
    }


@app.get("/categories")
async def get_categories() -> Dict[str, Any]:
    """Get all doctrine categories with block counts."""
    eng = get_engine()
    categories = get_all_doctrine_categories()
    coverage = get_coverage_map()
    return {
        "categories": [
            {
                "name": cat,
                "block_count": len(coverage.get(cat, [])),
                "topics": coverage.get(cat, []),
            }
            for cat in sorted(categories)
        ],
        "total_categories": len(categories),
    }


@app.get("/fragility/assess")
async def assess_fragility(
    text: str = Query(..., min_length=10, description="Text to assess for fact fragility"),
    topic: str = Query(default="", description="Topic context"),
) -> Dict[str, Any]:
    """Assess fact fragility of a text."""
    eng = get_engine()
    result = eng.fragility_scorer.score(text, topic)
    return result


@app.get("/decompose")
async def decompose_query(
    query: str = Query(..., min_length=3, description="Query to decompose into sub-doctrines"),
) -> Dict[str, Any]:
    """Decompose a complex query into doctrine components."""
    eng = get_engine()
    norm = normalize_semantics(query)
    components = eng.decomposer.decompose(query, norm)
    return {
        "query": query,
        "normalized_query": norm.normalized_query,
        "components": components,
        "total_components": len(components),
        "statutes_detected": norm.statutes_detected,
        "domains_detected": norm.environmental_domains,
    }


@app.get("/zones")
async def list_analysis_zones() -> Dict[str, Any]:
    """List all environmental analysis zones."""
    return {
        "zones": [
            {"zone": z.value, "description": f"Analysis zone for {z.value.replace('_', ' ')} queries"}
            for z in EnvironmentalZone
        ],
        "total_zones": len(EnvironmentalZone),
    }


@app.get("/zone/detect")
async def detect_analysis_zone(
    query: str = Query(..., min_length=3, description="Query to detect zone for"),
) -> Dict[str, Any]:
    """Detect the analysis zone for a query."""
    norm = normalize_semantics(query)
    zone = detect_zone(query, norm.environmental_domains)
    return {
        "query": query,
        "detected_zone": zone.value,
        "domains": norm.environmental_domains,
        "statutes": norm.statutes_detected,
    }


@app.get("/config/summary")
async def get_config_summary() -> Dict[str, Any]:
    """Get engine configuration summary."""
    return {
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "version": ENGINE_VERSION,
        "port": ENGINE_PORT,
        "domain": ENGINE_DOMAIN,
        "federal_statutes": CONFIG.get("federal_statutes", []),
        "texas_agencies": list(CONFIG.get("texas_agencies", {}).keys()),
        "permit_types_count": sum(len(v) for v in CONFIG.get("permit_types", {}).values()),
        "doctrine_domains_count": len(CONFIG.get("doctrine_domains", [])),
        "confidence_thresholds": CONFIDENCE_THRESHOLDS,
    }


@app.get("/export/doctrines")
async def export_doctrines(
    format: str = Query(default="summary", description="summary|full"),
) -> Dict[str, Any]:
    """Export doctrine cache in specified format."""
    eng = get_engine()
    if format == "full":
        return {
            "total_blocks": len(DOCTRINE_BLOCKS),
            "cache_hash": get_doctrine_cache_hash(),
            "blocks": [
                {
                    "topic": b.topic,
                    "category": b.category,
                    "summary": b.summary,
                    "analysis": b.analysis,
                    "authority": b.authority,
                    "keywords": b.keywords,
                    "statute": b.statute,
                    "cfr_reference": b.cfr_reference,
                    "jurisdiction": b.jurisdiction,
                    "confidence": b.confidence,
                    "last_updated": b.last_updated,
                    "block_hash": b.block_hash[:16] + "...",
                    "cross_references": b.cross_references,
                    "practice_tips": b.practice_tips,
                    "penalties": b.penalties,
                    "texas_notes": b.texas_notes,
                }
                for b in DOCTRINE_BLOCKS
            ],
        }
    return {
        "total_blocks": len(DOCTRINE_BLOCKS),
        "cache_hash": get_doctrine_cache_hash(),
        "blocks": [
            {
                "topic": b.topic,
                "category": b.category,
                "summary": b.summary[:200],
                "confidence": b.confidence,
                "statute": b.statute,
            }
            for b in DOCTRINE_BLOCKS
        ],
    }


@app.get("/")
async def root() -> Dict[str, Any]:
    """Root endpoint."""
    return {
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "version": ENGINE_VERSION,
        "port": ENGINE_PORT,
        "domain": ENGINE_DOMAIN,
        "tie_components": 20,
        "endpoints": [
            "/health", "/analyze", "/query", "/search", "/normalize",
            "/permits/analyze", "/cercla/prp-assessment", "/compliance/check",
            "/phase-i/checklist", "/phase-i/assess", "/penalty/estimate",
            "/penalty/multi-statute", "/penalty/maxima", "/penalty/compare",
            "/remediation/recommend", "/doctrines", "/doctrines/{topic}",
            "/coverage", "/drift", "/metrics", "/telemetry", "/integrity",
            "/audit/verify", "/audit/privilege",
            "/permian/analyze", "/permian/issues",
            "/transaction/analyze", "/water-rights/analyze",
            "/timeline/deadlines", "/timeline/facility",
            "/due-diligence/workflow",
            "/memo/generate", "/batch/analyze",
            "/statutes/reference", "/categories",
            "/fragility/assess", "/decompose",
            "/zones", "/zone/detect",
            "/config/summary", "/export/doctrines",
        ],
        "status": "operational",
    }


# ============================================================================
# CONTAMINANT DATABASE
# ============================================================================

class ContaminantDatabase:
    """Reference database for common environmental contaminants."""

    CONTAMINANTS: ClassVar[Dict[str, Dict[str, Any]]] = {
        "benzene": {
            "cas_number": "71-43-2",
            "category": "VOC",
            "epa_rsl_residential": 0.0011,
            "epa_rsl_industrial": 0.0054,
            "epa_rsl_units": "mg/kg (soil)",
            "mcl": 0.005,
            "mcl_units": "mg/L (water)",
            "carcinogen": True,
            "common_sources": ["petroleum", "gasoline", "chemical manufacturing"],
            "applicable_statutes": ["RCRA", "CERCLA", "SDWA", "CAA"],
            "remediation_technologies": ["air_sparging", "SVE", "bioremediation", "activated_carbon"],
        },
        "trichloroethylene": {
            "cas_number": "79-01-6",
            "category": "VOC",
            "epa_rsl_residential": 0.0030,
            "epa_rsl_industrial": 0.015,
            "epa_rsl_units": "mg/kg (soil)",
            "mcl": 0.005,
            "mcl_units": "mg/L (water)",
            "carcinogen": True,
            "common_sources": ["degreasing", "dry cleaning", "metal fabrication"],
            "applicable_statutes": ["RCRA", "CERCLA", "SDWA"],
            "remediation_technologies": ["SVE", "ISCO", "bioremediation", "PRB", "thermal"],
        },
        "lead": {
            "cas_number": "7439-92-1",
            "category": "Metal",
            "epa_rsl_residential": 400,
            "epa_rsl_industrial": 800,
            "epa_rsl_units": "mg/kg (soil)",
            "mcl": 0.015,
            "mcl_units": "mg/L (water, action level)",
            "carcinogen": False,
            "common_sources": ["paint", "batteries", "ammunition", "smelting", "mining"],
            "applicable_statutes": ["RCRA", "CERCLA", "SDWA", "TSCA (lead paint)"],
            "remediation_technologies": ["excavation", "stabilization", "soil_washing", "phytoremediation"],
        },
        "pfos": {
            "cas_number": "1763-23-1",
            "category": "PFAS",
            "epa_rsl_residential": 0.00000058,
            "epa_rsl_industrial": 0.0000026,
            "epa_rsl_units": "mg/kg (soil)",
            "mcl": 0.000004,
            "mcl_units": "mg/L (water, 4 ppt)",
            "carcinogen": False,
            "common_sources": ["AFFF foam", "industrial processes", "consumer products"],
            "applicable_statutes": ["CERCLA (designated hazardous substance 2024)", "SDWA", "TSCA"],
            "remediation_technologies": ["activated_carbon", "ion_exchange", "PFAS_destruction", "containment"],
        },
        "pfoa": {
            "cas_number": "335-67-1",
            "category": "PFAS",
            "epa_rsl_residential": 0.00000058,
            "epa_rsl_industrial": 0.0000026,
            "epa_rsl_units": "mg/kg (soil)",
            "mcl": 0.000004,
            "mcl_units": "mg/L (water, 4 ppt)",
            "carcinogen": True,
            "common_sources": ["AFFF foam", "non-stick coatings", "industrial processes"],
            "applicable_statutes": ["CERCLA (designated hazardous substance 2024)", "SDWA", "TSCA"],
            "remediation_technologies": ["activated_carbon", "ion_exchange", "PFAS_destruction", "containment"],
        },
        "arsenic": {
            "cas_number": "7440-38-2",
            "category": "Metal",
            "epa_rsl_residential": 0.68,
            "epa_rsl_industrial": 3.0,
            "epa_rsl_units": "mg/kg (soil)",
            "mcl": 0.010,
            "mcl_units": "mg/L (water)",
            "carcinogen": True,
            "common_sources": ["mining", "smelting", "pesticides", "natural occurrence"],
            "applicable_statutes": ["RCRA", "CERCLA", "SDWA"],
            "remediation_technologies": ["excavation", "stabilization", "permeable_reactive_barrier", "phytoremediation"],
        },
        "total_petroleum_hydrocarbons": {
            "cas_number": "N/A (mixture)",
            "category": "Petroleum",
            "epa_rsl_residential": "varies by fraction",
            "epa_rsl_industrial": "varies by fraction",
            "epa_rsl_units": "mg/kg (soil)",
            "mcl": "N/A (no federal MCL)",
            "mcl_units": "N/A",
            "carcinogen": False,
            "common_sources": ["petroleum spills", "UST releases", "crude oil production", "refining"],
            "applicable_statutes": ["RCRA", "CERCLA", "OPA", "CWA Section 311"],
            "remediation_technologies": ["bioremediation", "SVE", "landfarming", "thermal_desorption", "excavation"],
        },
        "hydrogen_sulfide": {
            "cas_number": "7783-06-4",
            "category": "Gas",
            "epa_rsl_residential": "N/A (air standard)",
            "epa_rsl_industrial": "N/A",
            "epa_rsl_units": "N/A",
            "mcl": "N/A",
            "mcl_units": "N/A",
            "carcinogen": False,
            "common_sources": ["sour crude oil/gas", "wastewater treatment", "paper mills", "landfills"],
            "applicable_statutes": ["CAA (HAP)", "OSHA", "RRC (Rule 36)"],
            "remediation_technologies": ["scrubbing", "chemical_treatment", "biological_treatment", "thermal_oxidation"],
        },
    }

    def lookup(self, contaminant: str) -> Dict[str, Any]:
        """Look up a contaminant in the database."""
        key = contaminant.lower().replace(" ", "_").replace("-", "_")
        data = self.CONTAMINANTS.get(key)
        if not data:
            # Fuzzy match
            for k, v in self.CONTAMINANTS.items():
                if contaminant.lower() in k or k in contaminant.lower():
                    return {"contaminant": contaminant, "found": True, "matched_key": k, **v}
            return {"contaminant": contaminant, "found": False, "available": list(self.CONTAMINANTS.keys())}
        return {"contaminant": contaminant, "found": True, "matched_key": key, **data}

    def get_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get contaminants by category."""
        results: List[Dict[str, Any]] = []
        for key, data in self.CONTAMINANTS.items():
            if data["category"].lower() == category.lower():
                results.append({"key": key, **data})
        return results

    def get_all_categories(self) -> List[str]:
        """Get all contaminant categories."""
        categories: Set[str] = set()
        for data in self.CONTAMINANTS.values():
            categories.add(data["category"])
        return sorted(categories)


# Attach contaminant database to engine
_original_patched_init = EnvironmentalLawEngine.__init__


def _final_patched_init(self: EnvironmentalLawEngine) -> None:
    """Final patched init that includes contaminant database."""
    _original_patched_init(self)
    self.contaminant_db = ContaminantDatabase()


EnvironmentalLawEngine.__init__ = _final_patched_init  # type: ignore[method-assign]


@app.get("/contaminants/lookup")
async def lookup_contaminant(
    name: str = Query(..., min_length=2, description="Contaminant name"),
) -> Dict[str, Any]:
    """Look up contaminant information."""
    eng = get_engine()
    return eng.contaminant_db.lookup(name)


@app.get("/contaminants/categories")
async def get_contaminant_categories() -> Dict[str, Any]:
    """Get all contaminant categories."""
    eng = get_engine()
    categories = eng.contaminant_db.get_all_categories()
    return {
        "categories": categories,
        "total": len(categories),
    }


@app.get("/contaminants/by-category")
async def get_contaminants_by_category(
    category: str = Query(..., min_length=2, description="Category (VOC, Metal, PFAS, Petroleum, Gas)"),
) -> Dict[str, Any]:
    """Get contaminants by category."""
    eng = get_engine()
    results = eng.contaminant_db.get_by_category(category)
    return {"category": category, "contaminants": results, "total": len(results)}


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "engine:app",
        host="0.0.0.0",
        port=ENGINE_PORT,
        reload=False,
        log_level="info",
        workers=1,
    )
