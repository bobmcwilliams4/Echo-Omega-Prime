"""
ECHO LG03 REGULATORY COMPLIANCE ENGINE - Production Architecture
Professional-grade regulatory compliance system for compliance officers,
attorneys, and risk management teams.

Architecture:
    Layer 1: Doctrine Cache (0-200ms) - Pre-compiled regulatory reasoning
    Layer 2: Semantic Retrieval (200-700ms) - CFR/FR search on cache miss
    Layer 3: Deep Analysis (on-demand) - Multi-agency synthesis

Response Modes:
    FAST:   Doctrine-driven, minimal citations, sub-2 seconds
    AUDIT:  Structured compliance check, audit-ready, gap analysis
    REPORT: Long-form, citation-heavy, regulatory filing documentation

Engine ID: LG03
Tier: T1_LEGAL
Mode: DET (Deterministic)
Port: 8393
Author: ECHO OMEGA PRIME
Authority: 11.0 SOVEREIGN
"""

from __future__ import annotations

import hashlib
import json
import sys
import time
import uuid
from collections import defaultdict
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from enum import Enum
from pathlib import Path
from typing import Any, ClassVar, Dict, List, Literal, Optional, Tuple

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import BaseModel, Field

# ============================================================================
# LOCAL IMPORTS
# ============================================================================

# Add engine directory to path for local imports
ENGINE_DIR = Path(__file__).parent
if str(ENGINE_DIR) not in sys.path:
    sys.path.insert(0, str(ENGINE_DIR))

from doctrines import (
    AGENCY_PROFILES,
    COMPLIANCE_OBLIGATIONS,
    DOCTRINE_CACHE,
    DOCTRINE_CACHE_VERSION,
    ENFORCEMENT_ACTIONS,
    INDUSTRY_REGULATION_MAP,
    PREEMPTION_RULES,
    AgencyLevel,
    AgencyProfile,
    AuthorityType,
    ComplianceObligation,
    ComplianceStatus,
    EnforcementAction,
    EnforcementSeverity,
    PreemptionRule,
    PreemptionType,
    RegulatoryDoctrineBlock,
    RiskLevel,
    RuleStatus,
    compute_doctrine_match_score,
    get_applicable_doctrines,
    get_doctrine,
    get_doctrine_summary,
    list_doctrine_keys,
    match_doctrine,
)
from search import (
    ComplianceDeadline,
    ComplianceGapResult,
    EnforcementSearchResult,
    PreemptionAnalysisResult,
    RegulationSearchResult,
    SearchResponse,
    analyze_compliance_gaps,
    analyze_preemption,
    compute_risk_score,
    generate_compliance_checklist,
    search_agency,
    search_by_cfr,
    search_deadlines,
    search_enforcement_actions,
    search_regulations,
)
from semantic import (
    CFR_TITLE_NAMES,
    CFR_TITLE_TO_AGENCY,
    CFRCitation,
    FederalRegisterCitation,
    NormalizationResult,
    PublicLawCitation,
    USCCitation,
    normalize_agency,
    normalize_semantics,
    parse_cfr_citation,
    parse_executive_order,
    parse_fr_citation,
    parse_public_law,
    parse_usc_citation,
    verify_semantic_map_integrity,
)
from telemetry import (
    AuditEntry,
    ErrorDomain,
    MetricsCollector,
    MutationOrigin,
    MutationType,
    QueryType,
    ResponseLayer,
    TelemetryManager,
    complete_trace,
    get_telemetry,
    log_error,
    record_doctrine_mutation,
    trace_query,
)

# ============================================================================
# CONFIGURATION
# ============================================================================

ENGINE_ID = "LG03"
ENGINE_NAME = "Regulatory Compliance Engine"
ENGINE_VERSION = "1.0.0"
ENGINE_TIER = "T1_LEGAL"
ENGINE_MODE = "DET"
ENGINE_PORT = 8393

LOG_DIR = Path("O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/LG03_regulatory_compliance/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

logger.add(
    LOG_DIR / "lg03_engine_{time}.log",
    rotation="50 MB",
    retention="30 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {module}:{function}:{line} | {message}",
)

# ============================================================================
# STARTUP TIME TRACKING
# ============================================================================

_ENGINE_START_TIME: float = time.time()


# ============================================================================
# ENUMS
# ============================================================================

class ResponseMode(str, Enum):
    """Response depth mode."""
    FAST = "fast"
    AUDIT = "audit"
    REPORT = "report"


class Complexity(str, Enum):
    """Query complexity level."""
    STANDARD = "standard"
    ADVANCED = "advanced"


# ============================================================================
# PYDANTIC REQUEST/RESPONSE MODELS
# ============================================================================

class ComplianceQuery(BaseModel):
    """Regulatory compliance query request."""
    question: str = Field(..., min_length=5, description="Compliance question or regulation reference")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response depth mode")
    agency: Optional[str] = Field(default=None, description="Filter to specific agency (e.g., SEC, EPA, OSHA)")
    naics_code: Optional[str] = Field(default=None, description="NAICS code for industry filtering")
    jurisdiction: str = Field(default="federal", description="Jurisdiction (federal, or state code)")
    include_enforcement: bool = Field(default=True, description="Include enforcement action information")
    include_deadlines: bool = Field(default=True, description="Include deadline information")
    include_trace: bool = Field(default=False, description="Include reasoning trace")


class RiskAssessmentQuery(BaseModel):
    """Risk assessment request."""
    regulation: str = Field(..., description="Regulation or regulatory area to assess")
    severity: int = Field(..., ge=1, le=10, description="Severity score (1-10)")
    likelihood: int = Field(..., ge=1, le=10, description="Likelihood score (1-10)")
    detectability: int = Field(..., ge=1, le=10, description="Detectability score (1-10)")
    context: Optional[str] = Field(default=None, description="Additional context for assessment")
    agency: Optional[str] = Field(default=None, description="Relevant agency")


class GapAnalysisQuery(BaseModel):
    """Compliance gap analysis request."""
    entity_name: str = Field(..., description="Name of entity being analyzed")
    naics_code: str = Field(..., min_length=2, description="NAICS code for the entity")
    current_compliance: Dict[str, str] = Field(
        default_factory=dict,
        description="Dict mapping doctrine_key -> compliance status"
    )


class PreemptionQuery(BaseModel):
    """Preemption analysis request."""
    federal_area: str = Field(..., description="Federal regulatory area (e.g., erisa, securities, osha)")
    state_law_description: str = Field(..., description="Description of the state/local law in question")


class ChecklistQuery(BaseModel):
    """Compliance checklist generation request."""
    naics_code: str = Field(..., min_length=2, description="NAICS code for the industry")
    jurisdiction: str = Field(default="federal", description="Jurisdiction")


class CFRLookupQuery(BaseModel):
    """CFR cross-reference lookup request."""
    cfr_citation: str = Field(..., description="CFR citation to look up (e.g., '40 CFR 261')")


class AgencySearchQuery(BaseModel):
    """Agency information search request."""
    query: str = Field(..., description="Agency name, code, or jurisdiction keyword")


class NormalizationQuery(BaseModel):
    """Semantic normalization request (diagnostic)."""
    text: str = Field(..., description="Text to normalize")


class Citation(BaseModel):
    """Structured regulatory citation."""
    authority: str
    reference: str
    relevance: str


class ReasoningStep(BaseModel):
    """Structured reasoning component."""
    step: int
    analysis: str
    authority: Optional[str] = None


class ComplianceResponse(BaseModel):
    """Regulatory compliance response."""
    # Core
    query_id: str
    question: str
    mode: ResponseMode

    # Primary answer
    conclusion: str
    reasoning: str

    # Structured components
    key_factors: List[str]
    citations: List[Citation]

    # Regulatory specifics
    agency: Optional[str] = None
    cfr_references: List[str] = Field(default_factory=list)
    usc_references: List[str] = Field(default_factory=list)
    risk_level: Optional[str] = None
    risk_score: Optional[int] = None
    penalty_range: Optional[str] = None
    criminal_exposure: Optional[bool] = None

    # Compliance actions
    required_actions: List[str] = Field(default_factory=list)
    documentation_required: List[str] = Field(default_factory=list)
    reporting_frequency: Optional[str] = None

    # Enforcement info
    enforcement_actions: Optional[List[Dict[str, Any]]] = None

    # Deadline info
    deadlines: Optional[List[Dict[str, Any]]] = None

    # Preemption
    preemption_type: Optional[str] = None
    state_variations: List[str] = Field(default_factory=list)

    # Industry
    applicable_industries: List[str] = Field(default_factory=list)

    # Metadata
    doctrine_match: bool
    confidence_tier: Literal["high", "moderate", "requires_review"]
    response_layer: str
    latency_ms: float
    determinism_hash: str

    # Trace (optional)
    reasoning_trace: Optional[List[ReasoningStep]] = None

    # Search metadata
    agencies_detected: List[str] = Field(default_factory=list)
    cfr_citations_parsed: List[Dict[str, Any]] = Field(default_factory=list)
    normalization_applied: Optional[Dict[str, Any]] = None

    # Limitations
    limitations: List[str] = Field(default_factory=list)

    # Audit
    timestamp: str
    version: str = ENGINE_VERSION


class HealthResponse(BaseModel):
    """Engine health check response."""
    status: Literal["healthy", "degraded", "unhealthy"]
    engine_id: str
    engine_name: str
    version: str
    tier: str
    mode: str
    port: int
    uptime_seconds: float

    # Components
    doctrine_cache: Dict[str, Any]
    semantic_map: Dict[str, Any]

    # Metrics
    api_latency: Dict[str, float]
    active_queries: int
    queries_last_hour: int
    error_rate: Dict[str, Any]
    doctrine_hit_rate: float
    risk_distribution: Dict[str, Any]
    agency_distribution: Dict[str, int]

    # Audit
    audit_trail: Dict[str, Any]

    # Memory
    memory_mb: Dict[str, float]


class RiskAssessmentResponse(BaseModel):
    """Risk assessment response."""
    query_id: str
    regulation: str
    severity: int
    likelihood: int
    detectability: int
    composite_score: int
    max_possible: int
    risk_level: str
    recommended_action: str
    context_analysis: Optional[str] = None
    related_doctrine: Optional[Dict[str, Any]] = None
    determinism_hash: str
    timestamp: str


# ============================================================================
# APPLICATION LIFECYCLE
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown lifecycle."""
    logger.info(f"LG03 Regulatory Compliance Engine v{ENGINE_VERSION} starting on port {ENGINE_PORT}")
    logger.info(f"Doctrine cache: {len(DOCTRINE_CACHE)} doctrines loaded")
    logger.info(f"Agency profiles: {len(AGENCY_PROFILES)} agencies")
    logger.info(f"Enforcement actions: {len(ENFORCEMENT_ACTIONS)} templates")
    logger.info(f"Compliance obligations: {len(COMPLIANCE_OBLIGATIONS)} obligations")
    logger.info(f"Preemption rules: {len(PREEMPTION_RULES)} rules")

    # Verify semantic map integrity
    integrity = verify_semantic_map_integrity()
    logger.info(f"Semantic map integrity: {integrity}")

    # Record startup in audit trail
    telemetry = get_telemetry()
    telemetry.audit.record(
        action="engine_startup",
        actor="LG03_ENGINE",
        resource="system",
        details={
            "version": ENGINE_VERSION,
            "doctrine_count": len(DOCTRINE_CACHE),
            "agency_count": len(AGENCY_PROFILES),
            "enforcement_count": len(ENFORCEMENT_ACTIONS),
            "obligation_count": len(COMPLIANCE_OBLIGATIONS),
            "semantic_integrity": integrity,
        },
    )

    yield

    # Shutdown
    logger.info("LG03 Regulatory Compliance Engine shutting down")
    telemetry.audit.record(
        action="engine_shutdown",
        actor="LG03_ENGINE",
        resource="system",
        details={"uptime_seconds": telemetry.uptime_seconds},
    )


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(
    title="LG03 Regulatory Compliance Engine",
    description="Professional-grade regulatory compliance system for compliance officers, "
                "attorneys, and risk management teams. Covers SEC, EPA, OSHA, IRS, FTC, "
                "FINCEN, HHS, EEOC, OFAC, and more.",
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
# CORE QUERY PROCESSING
# ============================================================================

def _generate_query_id() -> str:
    """Generate a unique query identifier."""
    return f"LG03-{uuid.uuid4().hex[:12]}"


def _compute_determinism_hash(query: str, result_summary: str) -> str:
    """Compute SHA-256 determinism hash for response verification."""
    content = f"{query}:{result_summary}:{ENGINE_VERSION}"
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def _build_reasoning_trace(norm_result: NormalizationResult,
                           match_result: Optional[Dict[str, Any]],
                           doctrine: Optional[RegulatoryDoctrineBlock],
                           search_result: Optional[SearchResponse]) -> List[ReasoningStep]:
    """Build structured reasoning trace for the query."""
    steps: List[ReasoningStep] = []
    step_num = 1

    # Step 1: Semantic normalization
    changes = norm_result.changes_applied
    steps.append(ReasoningStep(
        step=step_num,
        analysis=f"Normalized query: {len(changes)} semantic mappings applied. "
                 f"Agencies detected: {', '.join(norm_result.agencies_detected) or 'none'}. "
                 f"CFR citations parsed: {len(norm_result.cfr_citations)}.",
    ))
    step_num += 1

    # Step 2: Citation extraction
    if norm_result.cfr_citations or norm_result.usc_citations:
        cit_details = []
        for c in norm_result.cfr_citations:
            cit_details.append(f"CFR: {c.canonical}")
        for c in norm_result.usc_citations:
            cit_details.append(f"USC: {c.canonical}")
        steps.append(ReasoningStep(
            step=step_num,
            analysis=f"Citations extracted: {'; '.join(cit_details)}",
            authority=cit_details[0] if cit_details else None,
        ))
        step_num += 1

    # Step 3: Doctrine matching
    if match_result:
        steps.append(ReasoningStep(
            step=step_num,
            analysis=f"Doctrine matched: {match_result['topic']} (score: {match_result['score']}). "
                     f"Agency: {match_result['agency']}. "
                     f"Total candidates evaluated: {len(match_result.get('all_candidates', []))}.",
        ))
        step_num += 1

    # Step 4: Doctrine analysis
    if doctrine:
        steps.append(ReasoningStep(
            step=step_num,
            analysis=f"Applying {doctrine.topic} compliance framework. "
                     f"Risk level: {doctrine.risk_level.value}. "
                     f"Criminal exposure: {doctrine.criminal_exposure}. "
                     f"Key requirements: {len(doctrine.key_requirements)}.",
            authority=doctrine.cfr_references[0] if doctrine.cfr_references else None,
        ))
        step_num += 1

    # Step 5: Risk assessment
    if doctrine:
        steps.append(ReasoningStep(
            step=step_num,
            analysis=f"Risk score: {doctrine.composite_risk_score}/1000 "
                     f"(S={doctrine.severity_score} x L={doctrine.likelihood_score} "
                     f"x D={doctrine.detectability_score}). "
                     f"Penalty range: {doctrine.penalty_range}.",
        ))
        step_num += 1

    # Step 6: Search results
    if search_result:
        steps.append(ReasoningStep(
            step=step_num,
            analysis=f"Search returned {search_result.total_results} total results: "
                     f"{len(search_result.regulation_results)} regulations, "
                     f"{len(search_result.enforcement_results)} enforcement actions, "
                     f"{len(search_result.deadline_results)} deadlines.",
        ))
        step_num += 1

    # Step 7: Preemption
    if doctrine and doctrine.preemption_type != PreemptionType.NONE:
        steps.append(ReasoningStep(
            step=step_num,
            analysis=f"Preemption: {doctrine.preemption_type.value}. "
                     f"State variations: {len(doctrine.state_variations)} noted.",
        ))
        step_num += 1

    # Step 8: Conclusion
    steps.append(ReasoningStep(
        step=step_num,
        analysis="Analysis complete. Determinism hash computed on full response.",
    ))

    return steps


def _determine_confidence_tier(doctrine_match: bool, risk_level: Optional[str],
                                mode: ResponseMode) -> Literal["high", "moderate", "requires_review"]:
    """Determine confidence tier for the response."""
    if not doctrine_match:
        return "requires_review"
    if risk_level in ("critical", "high"):
        if mode == ResponseMode.FAST:
            return "moderate"
        return "high"
    return "high"


def _build_conclusion(doctrine: Optional[RegulatoryDoctrineBlock],
                      norm_result: NormalizationResult,
                      mode: ResponseMode) -> str:
    """Build the conclusion text based on doctrine and query analysis."""
    if doctrine is None:
        agencies = ", ".join(norm_result.agencies_detected) or "multiple agencies"
        return (
            f"The query touches regulatory areas potentially governed by {agencies}. "
            f"No specific pre-compiled doctrine was matched with sufficient confidence. "
            f"A detailed review of applicable regulations is recommended, focusing on "
            f"the specific industry sector, entity size, and jurisdictional requirements."
        )

    conclusion_parts: List[str] = []

    # Primary compliance framework summary
    framework_lines = doctrine.compliance_framework.strip().split("\n")
    # Get first substantive paragraph
    for line in framework_lines:
        stripped = line.strip()
        if stripped and not stripped.startswith(("=", "-", "#")) and len(stripped) > 20:
            conclusion_parts.append(stripped)
            break

    # Risk assessment
    conclusion_parts.append(
        f"Risk assessment: {doctrine.risk_level.value.upper()} "
        f"(composite score {doctrine.composite_risk_score}/1000). "
    )

    # Enforcement posture
    if doctrine.criminal_exposure:
        conclusion_parts.append(
            f"Criminal exposure exists. Penalties: {doctrine.penalty_range}."
        )
    else:
        conclusion_parts.append(f"Penalties: {doctrine.penalty_range}.")

    # Key requirements count
    conclusion_parts.append(
        f"There are {len(doctrine.key_requirements)} primary compliance requirements "
        f"under {doctrine.agency} jurisdiction."
    )

    if mode == ResponseMode.REPORT:
        # Add preemption info for report mode
        if doctrine.preemption_type != PreemptionType.NONE:
            conclusion_parts.append(
                f"Federal preemption: {doctrine.preemption_type.value}. "
                f"State variations exist in {len(doctrine.state_variations)} areas."
            )

    return " ".join(conclusion_parts)


def _build_reasoning(doctrine: Optional[RegulatoryDoctrineBlock],
                     norm_result: NormalizationResult,
                     mode: ResponseMode) -> str:
    """Build detailed reasoning text."""
    if doctrine is None:
        return (
            "No matching regulatory doctrine was found in the pre-compiled cache. "
            "This may indicate a novel regulatory question, a cross-jurisdictional issue, "
            "or a query that spans multiple regulatory domains without a clear primary "
            "agency nexus. Recommend consulting with specialized regulatory counsel "
            "for the specific area of concern."
        )

    parts: List[str] = [doctrine.compliance_framework.strip()]

    if mode in (ResponseMode.AUDIT, ResponseMode.REPORT):
        parts.append(f"\nENFORCEMENT POSTURE:\n{doctrine.enforcement_history}")
        parts.append(f"\nREPORTING REQUIREMENTS:\nFrequency: {doctrine.reporting_frequency}")

        if doctrine.state_variations:
            parts.append("\nSTATE VARIATIONS:")
            for variation in doctrine.state_variations:
                parts.append(f"  - {variation}")

    return "\n".join(parts)


def _build_citations(doctrine: Optional[RegulatoryDoctrineBlock],
                     norm_result: NormalizationResult) -> List[Citation]:
    """Build structured citation list."""
    citations: List[Citation] = []

    if doctrine:
        for ref in doctrine.cfr_references:
            citations.append(Citation(
                authority="CFR",
                reference=ref,
                relevance=f"Primary regulatory authority for {doctrine.topic}",
            ))
        for ref in doctrine.usc_references:
            citations.append(Citation(
                authority="USC",
                reference=ref,
                relevance=f"Statutory basis for {doctrine.topic}",
            ))

    # Add parsed citations from query
    for cfr in norm_result.cfr_citations:
        already = any(c.reference == cfr.canonical for c in citations)
        if not already:
            citations.append(Citation(
                authority="CFR",
                reference=cfr.canonical,
                relevance=f"Cited in query ({cfr.title_name})",
            ))

    for usc in norm_result.usc_citations:
        already = any(c.reference == usc.canonical for c in citations)
        if not already:
            citations.append(Citation(
                authority="USC",
                reference=usc.canonical,
                relevance="Cited in query",
            ))

    return citations


# ============================================================================
# EPISTEMIC GUARDRAILS
# ============================================================================

BANNED_PHRASES: List[str] = [
    "definitely compliant",
    "guaranteed safe",
    "no risk",
    "zero liability",
    "impossible to violate",
    "absolutely no penalties",
    "always legal",
    "never illegal",
    "completely protected",
    "100% compliant",
]

DISCLOSURE_CAVEAT: str = (
    "This analysis is provided for informational purposes and does not constitute "
    "legal advice. Regulatory compliance determinations require review by qualified "
    "legal counsel familiar with the specific facts and applicable jurisdiction. "
    "Regulations change frequently; verify current requirements with the relevant "
    "regulatory agency."
)


def apply_epistemic_guardrails(text: str) -> str:
    """Ensure response does not contain overconfident or misleading language.

    Args:
        text: Response text to validate.

    Returns:
        Validated text with any banned phrases replaced.
    """
    result = text
    for phrase in BANNED_PHRASES:
        if phrase.lower() in result.lower():
            result = result.replace(phrase, "[claim requires qualification]")
            result = result.replace(phrase.capitalize(), "[claim requires qualification]")
            result = result.replace(phrase.upper(), "[CLAIM REQUIRES QUALIFICATION]")
    return result


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Comprehensive engine health check."""
    import psutil

    telemetry = get_telemetry()
    metrics = telemetry.metrics
    process = psutil.Process()
    mem_info = process.memory_info()

    doctrine_summary = get_doctrine_summary()
    semantic_integrity = verify_semantic_map_integrity()
    audit_status = telemetry.audit.verify_chain()

    # Determine overall status
    status: Literal["healthy", "degraded", "unhealthy"] = "healthy"
    error_stats = metrics.get_error_stats()
    if error_stats["last_hour"] > 10:
        status = "degraded"
    if error_stats["last_hour"] > 50:
        status = "unhealthy"
    if not semantic_integrity.get("count_match", True):
        status = "degraded"

    return HealthResponse(
        status=status,
        engine_id=ENGINE_ID,
        engine_name=ENGINE_NAME,
        version=ENGINE_VERSION,
        tier=ENGINE_TIER,
        mode=ENGINE_MODE,
        port=ENGINE_PORT,
        uptime_seconds=round(time.time() - _ENGINE_START_TIME, 2),
        doctrine_cache={
            "status": "loaded",
            "version": DOCTRINE_CACHE_VERSION,
            "doctrines": doctrine_summary["total_doctrines"],
            "agencies": doctrine_summary["total_agencies"],
            "enforcement_actions": doctrine_summary["total_enforcement_actions"],
            "obligations": doctrine_summary["total_obligations"],
            "preemption_rules": doctrine_summary["total_preemption_rules"],
            "hit_rate": metrics.get_doctrine_hit_rate(),
        },
        semantic_map=semantic_integrity,
        api_latency=metrics.get_latency_stats(),
        active_queries=metrics.active_queries,
        queries_last_hour=metrics.queries_last_hour(),
        error_rate=error_stats,
        doctrine_hit_rate=metrics.get_doctrine_hit_rate(),
        risk_distribution=metrics.get_risk_distribution(),
        agency_distribution=metrics.get_agency_distribution(),
        audit_trail={
            "entries": telemetry.audit.entry_count,
            "chain_integrity": audit_status,
        },
        memory_mb={
            "rss_mb": round(mem_info.rss / 1024 / 1024, 2),
            "vms_mb": round(mem_info.vms / 1024 / 1024, 2),
        },
    )


@app.post("/query", response_model=ComplianceResponse)
async def compliance_query(query: ComplianceQuery) -> ComplianceResponse:
    """Primary compliance query endpoint.

    Performs full regulatory compliance analysis including:
        - Semantic normalization and citation extraction
        - Doctrine matching and compliance framework application
        - Risk assessment
        - Enforcement action cross-referencing
        - Deadline identification
        - Preemption analysis
    """
    query_id = _generate_query_id()
    start_time = time.time()
    telemetry = get_telemetry()

    # Determine query type
    query_type = QueryType.COMPLIANCE_CHECK
    q_lower = query.question.lower()
    if any(kw in q_lower for kw in ["risk", "penalty", "fine", "enforcement"]):
        query_type = QueryType.RISK_ASSESSMENT
    elif any(kw in q_lower for kw in ["deadline", "filing", "due", "report", "when"]):
        query_type = QueryType.DEADLINE_QUERY
    elif any(kw in q_lower for kw in ["gap", "deficiency", "missing", "lacking"]):
        query_type = QueryType.GAP_ANALYSIS
    elif any(kw in q_lower for kw in ["preempt", "state law", "federal vs state"]):
        query_type = QueryType.PREEMPTION_CHECK
    elif any(kw in q_lower for kw in ["search", "find", "what regulation", "which rule"]):
        query_type = QueryType.REGULATION_SEARCH

    trace_id = trace_query(query_id, query_type)

    try:
        # Step 1: Semantic normalization
        norm_result = normalize_semantics(query.question)
        logger.info(f"[{query_id}] Normalized: {len(norm_result.changes_applied)} changes, "
                     f"{len(norm_result.agencies_detected)} agencies, "
                     f"{len(norm_result.cfr_citations)} CFR citations")

        # Step 2: Doctrine matching
        match_result = match_doctrine(norm_result.normalized)
        doctrine: Optional[RegulatoryDoctrineBlock] = None
        doctrine_hit = False

        if match_result:
            doctrine = get_doctrine(match_result["matched_doctrine"])
            doctrine_hit = True
            logger.info(f"[{query_id}] Doctrine matched: {match_result['topic']} "
                         f"(score: {match_result['score']})")

        # Step 3: Search (for AUDIT and REPORT modes, or if no doctrine match)
        search_result: Optional[SearchResponse] = None
        if query.mode in (ResponseMode.AUDIT, ResponseMode.REPORT) or not doctrine_hit:
            search_result = search_regulations(
                query.question,
                max_results=10,
                agency_filter=query.agency,
                naics_filter=query.naics_code,
            )

        # Step 4: Build response
        conclusion = _build_conclusion(doctrine, norm_result, query.mode)
        conclusion = apply_epistemic_guardrails(conclusion)

        reasoning = _build_reasoning(doctrine, norm_result, query.mode)
        reasoning = apply_epistemic_guardrails(reasoning)

        citations = _build_citations(doctrine, norm_result)

        key_factors = doctrine.key_factors if doctrine else [
            "Specific regulatory area must be identified",
            "Industry sector determines applicable regulations",
            "Entity size may affect compliance thresholds",
            "Jurisdictional analysis needed (federal vs. state)",
        ]

        # Enforcement actions
        enforcement_data: Optional[List[Dict[str, Any]]] = None
        if query.include_enforcement and doctrine_hit:
            enforcement_results = search_enforcement_actions(
                norm_result.normalized.lower(),
                agency_filter=query.agency or (doctrine.agency if doctrine else None),
            )
            if enforcement_results:
                enforcement_data = [r.to_dict() for r in enforcement_results]

        # Deadlines
        deadline_data: Optional[List[Dict[str, Any]]] = None
        if query.include_deadlines:
            deadline_results = search_deadlines(
                norm_result.normalized.lower(),
                agency_filter=query.agency,
                naics_filter=query.naics_code,
            )
            if deadline_results:
                deadline_data = [r.to_dict() for r in deadline_results]

        # Reasoning trace
        trace_steps: Optional[List[ReasoningStep]] = None
        if query.include_trace:
            trace_steps = _build_reasoning_trace(norm_result, match_result, doctrine, search_result)

        # Determine response layer
        if doctrine_hit:
            response_layer = ResponseLayer.DOCTRINE.value
        elif search_result and search_result.total_results > 0:
            response_layer = ResponseLayer.RETRIEVAL.value
        else:
            response_layer = ResponseLayer.DEEP_ANALYSIS.value

        # Confidence tier
        confidence = _determine_confidence_tier(
            doctrine_hit,
            doctrine.risk_level.value if doctrine else None,
            query.mode,
        )

        # Compute latency
        latency_ms = round((time.time() - start_time) * 1000, 2)

        # Determinism hash
        hash_summary = f"{doctrine_hit}:{match_result['matched_doctrine'] if match_result else 'none'}"
        determinism_hash = _compute_determinism_hash(query.question, hash_summary)

        # Limitations
        limitations: List[str] = [DISCLOSURE_CAVEAT]
        if not doctrine_hit:
            limitations.append(
                "No exact doctrine match found. Analysis is based on general regulatory "
                "principles and may not capture all applicable requirements."
            )
        if query.jurisdiction != "federal":
            limitations.append(
                f"State-specific analysis for {query.jurisdiction} may require "
                f"additional review of state regulatory codes."
            )

        # Complete telemetry trace
        complete_trace(
            trace_id,
            layer=ResponseLayer.DOCTRINE if doctrine_hit else ResponseLayer.RETRIEVAL,
            doctrine_hit=doctrine_hit,
            agency=doctrine.agency if doctrine else None,
            risk_score=float(doctrine.composite_risk_score) if doctrine else None,
        )

        # Record audit entry
        telemetry.record_compliance_determination(
            query_id=query_id,
            regulation=doctrine.topic if doctrine else "unmatched",
            determination=conclusion[:200],
            risk_score=float(doctrine.composite_risk_score) if doctrine else 0.0,
            determinism_hash=determinism_hash,
            details={
                "mode": query.mode.value,
                "doctrine_hit": doctrine_hit,
                "agency": doctrine.agency if doctrine else None,
                "query_type": query_type.value,
            },
        )

        return ComplianceResponse(
            query_id=query_id,
            question=query.question,
            mode=query.mode,
            conclusion=conclusion,
            reasoning=reasoning,
            key_factors=key_factors,
            citations=[Citation(authority=c.authority, reference=c.reference,
                                relevance=c.relevance) for c in citations],
            agency=doctrine.agency if doctrine else None,
            cfr_references=doctrine.cfr_references if doctrine else [],
            usc_references=doctrine.usc_references if doctrine else [],
            risk_level=doctrine.risk_level.value if doctrine else None,
            risk_score=doctrine.composite_risk_score if doctrine else None,
            penalty_range=doctrine.penalty_range if doctrine else None,
            criminal_exposure=doctrine.criminal_exposure if doctrine else None,
            required_actions=doctrine.required_actions if doctrine else [],
            documentation_required=doctrine.documentation_required if doctrine else [],
            reporting_frequency=doctrine.reporting_frequency if doctrine else None,
            enforcement_actions=enforcement_data,
            deadlines=deadline_data,
            preemption_type=doctrine.preemption_type.value if doctrine else None,
            state_variations=doctrine.state_variations if doctrine else [],
            applicable_industries=doctrine.applicable_naics if doctrine else [],
            doctrine_match=doctrine_hit,
            confidence_tier=confidence,
            response_layer=response_layer,
            latency_ms=latency_ms,
            determinism_hash=determinism_hash,
            reasoning_trace=trace_steps,
            agencies_detected=norm_result.agencies_detected,
            cfr_citations_parsed=[c.to_dict() for c in norm_result.cfr_citations],
            normalization_applied=norm_result.to_dict() if query.include_trace else None,
            limitations=limitations,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

    except Exception as exc:
        log_error(trace_id, str(exc), ErrorDomain.UNKNOWN,
                  {"query_id": query_id, "question": query.question[:200]})
        logger.exception(f"[{query_id}] Query processing failed: {exc}")
        raise HTTPException(status_code=500, detail=f"Query processing error: {str(exc)}")


@app.post("/risk-assessment", response_model=RiskAssessmentResponse)
async def risk_assessment(query: RiskAssessmentQuery) -> RiskAssessmentResponse:
    """Compute risk score for a regulatory area."""
    query_id = _generate_query_id()
    trace_id = trace_query(query_id, QueryType.RISK_ASSESSMENT)

    try:
        risk_result = compute_risk_score(query.severity, query.likelihood, query.detectability)

        # Try to find related doctrine
        related: Optional[Dict[str, Any]] = None
        norm = normalize_semantics(query.regulation)
        match_result = match_doctrine(norm.normalized)
        if match_result:
            doctrine = get_doctrine(match_result["matched_doctrine"])
            if doctrine:
                related = {
                    "doctrine_key": match_result["matched_doctrine"],
                    "topic": doctrine.topic,
                    "agency": doctrine.agency,
                    "doctrine_risk_score": doctrine.composite_risk_score,
                    "penalty_range": doctrine.penalty_range,
                    "criminal_exposure": doctrine.criminal_exposure,
                }

        # Context analysis
        context_analysis: Optional[str] = None
        if query.context:
            context_analysis = (
                f"Context considered: {query.context}. "
                f"Risk assessment: {risk_result['risk_level']} level. "
                f"Recommended action: {risk_result['recommended_action']}."
            )

        complete_trace(trace_id, ResponseLayer.RISK_ASSESSMENT, doctrine_hit=bool(match_result),
                       risk_score=float(risk_result["composite_score"]))

        return RiskAssessmentResponse(
            query_id=query_id,
            regulation=query.regulation,
            severity=risk_result["severity"],
            likelihood=risk_result["likelihood"],
            detectability=risk_result["detectability"],
            composite_score=risk_result["composite_score"],
            max_possible=risk_result["max_possible"],
            risk_level=risk_result["risk_level"],
            recommended_action=risk_result["recommended_action"],
            context_analysis=context_analysis,
            related_doctrine=related,
            determinism_hash=risk_result["determinism_hash"],
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

    except Exception as exc:
        log_error(trace_id, str(exc), ErrorDomain.RISK_SCORING)
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/gap-analysis")
async def gap_analysis(query: GapAnalysisQuery) -> Dict[str, Any]:
    """Analyze compliance gaps for an entity."""
    query_id = _generate_query_id()
    trace_id = trace_query(query_id, QueryType.GAP_ANALYSIS)

    try:
        result = analyze_compliance_gaps(
            entity_name=query.entity_name,
            naics_code=query.naics_code,
            current_compliance=query.current_compliance,
        )

        telemetry = get_telemetry()
        telemetry.record_gap_analysis(
            query_id=query_id,
            entity=query.entity_name,
            gap_score=result.gap_score,
            gaps=[g.get("doctrine_key", "") for g in result.gaps],
            determinism_hash=result.determinism_hash,
        )

        complete_trace(trace_id, ResponseLayer.GAP_ANALYSIS, doctrine_hit=True,
                       risk_score=result.gap_score * 1000)

        response = result.to_dict()
        response["query_id"] = query_id
        response["timestamp"] = datetime.now(timezone.utc).isoformat()
        return response

    except Exception as exc:
        log_error(trace_id, str(exc), ErrorDomain.COMPLIANCE_GAP)
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/preemption-analysis")
async def preemption_analysis(query: PreemptionQuery) -> Dict[str, Any]:
    """Analyze federal preemption of state/local law."""
    query_id = _generate_query_id()
    trace_id = trace_query(query_id, QueryType.PREEMPTION_CHECK)

    try:
        result = analyze_preemption(
            federal_area=query.federal_area,
            state_law_description=query.state_law_description,
        )

        complete_trace(trace_id, ResponseLayer.DEEP_ANALYSIS, doctrine_hit=True)

        response = result.to_dict()
        response["query_id"] = query_id
        response["timestamp"] = datetime.now(timezone.utc).isoformat()
        return response

    except Exception as exc:
        log_error(trace_id, str(exc), ErrorDomain.PREEMPTION_ANALYSIS)
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/checklist")
async def compliance_checklist(query: ChecklistQuery) -> Dict[str, Any]:
    """Generate a compliance checklist for an industry."""
    query_id = _generate_query_id()
    trace_id = trace_query(query_id, QueryType.COMPLIANCE_CHECK)

    try:
        result = generate_compliance_checklist(
            naics_code=query.naics_code,
            jurisdiction=query.jurisdiction,
        )

        complete_trace(trace_id, ResponseLayer.COMPLIANCE_CHECK, doctrine_hit=True)

        result["query_id"] = query_id
        result["timestamp"] = datetime.now(timezone.utc).isoformat()
        return result

    except Exception as exc:
        log_error(trace_id, str(exc), ErrorDomain.INDUSTRY_CLASSIFY)
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/search")
async def regulation_search(
    question: str = Query(..., description="Search query"),
    agency: Optional[str] = Query(None, description="Agency filter"),
    naics_code: Optional[str] = Query(None, description="NAICS filter"),
    risk_level: Optional[str] = Query(None, description="Risk level filter"),
    max_results: int = Query(20, ge=1, le=100, description="Max results"),
) -> Dict[str, Any]:
    """Search the regulatory doctrine database."""
    query_id = _generate_query_id()
    trace_id = trace_query(query_id, QueryType.REGULATION_SEARCH)

    try:
        result = search_regulations(
            query=question,
            max_results=max_results,
            agency_filter=agency,
            naics_filter=naics_code,
            risk_level_filter=risk_level,
        )

        complete_trace(trace_id, ResponseLayer.RETRIEVAL,
                       doctrine_hit=len(result.regulation_results) > 0)

        response = result.to_dict()
        response["query_id"] = query_id
        response["timestamp"] = datetime.now(timezone.utc).isoformat()
        return response

    except Exception as exc:
        log_error(trace_id, str(exc), ErrorDomain.SEARCH)
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/cfr-lookup")
async def cfr_lookup(query: CFRLookupQuery) -> Dict[str, Any]:
    """Look up doctrines by CFR citation."""
    query_id = _generate_query_id()
    trace_id = trace_query(query_id, QueryType.REGULATION_SEARCH)

    try:
        results = search_by_cfr(query.cfr_citation)
        citations = parse_cfr_citation(query.cfr_citation)

        complete_trace(trace_id, ResponseLayer.RETRIEVAL, doctrine_hit=len(results) > 0)

        return {
            "query_id": query_id,
            "cfr_citation": query.cfr_citation,
            "parsed_citations": [c.to_dict() for c in citations],
            "matching_doctrines": results,
            "total_matches": len(results),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as exc:
        log_error(trace_id, str(exc), ErrorDomain.CFR_PARSE)
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/agency-search")
async def agency_search(query: AgencySearchQuery) -> Dict[str, Any]:
    """Search agency profiles."""
    query_id = _generate_query_id()

    results = search_agency(query.query)
    return {
        "query_id": query_id,
        "query": query.query,
        "results": results,
        "total_matches": len(results),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.post("/normalize")
async def normalize_text(query: NormalizationQuery) -> Dict[str, Any]:
    """Diagnostic endpoint: semantic normalization analysis."""
    query_id = _generate_query_id()
    result = normalize_semantics(query.text)
    integrity = verify_semantic_map_integrity()

    return {
        "query_id": query_id,
        "normalization": result.to_dict(),
        "semantic_map_integrity": integrity,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ============================================================================
# ENFORCEMENT ENDPOINTS
# ============================================================================

@app.get("/enforcement/actions")
async def list_enforcement_actions(
    agency: Optional[str] = Query(None, description="Filter by agency"),
) -> Dict[str, Any]:
    """List all enforcement action templates."""
    results: List[Dict[str, Any]] = []
    for key, action in ENFORCEMENT_ACTIONS.items():
        if agency and action.agency != normalize_agency(agency):
            continue
        data = action.to_dict()
        data["action_key"] = key
        results.append(data)

    return {
        "total": len(results),
        "enforcement_actions": results,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/enforcement/{action_key}")
async def get_enforcement_action(action_key: str) -> Dict[str, Any]:
    """Get a specific enforcement action template."""
    action = ENFORCEMENT_ACTIONS.get(action_key)
    if not action:
        raise HTTPException(status_code=404, detail=f"Enforcement action not found: {action_key}")
    data = action.to_dict()
    data["action_key"] = action_key
    return data


# ============================================================================
# DOCTRINE ENDPOINTS
# ============================================================================

@app.get("/doctrines")
async def list_doctrines() -> Dict[str, Any]:
    """List all regulatory doctrines with summary info."""
    summary = get_doctrine_summary()
    doctrines: List[Dict[str, str]] = []
    for key, doctrine in DOCTRINE_CACHE.items():
        doctrines.append({
            "key": key,
            "topic": doctrine.topic,
            "agency": doctrine.agency,
            "risk_level": doctrine.risk_level.value,
            "composite_risk_score": str(doctrine.composite_risk_score),
        })
    summary["doctrines"] = doctrines
    return summary


@app.get("/doctrines/{doctrine_key}")
async def get_doctrine_detail(doctrine_key: str) -> Dict[str, Any]:
    """Get full detail for a specific doctrine."""
    doctrine = get_doctrine(doctrine_key)
    if not doctrine:
        raise HTTPException(status_code=404, detail=f"Doctrine not found: {doctrine_key}")
    return doctrine.to_dict()


# ============================================================================
# AGENCY ENDPOINTS
# ============================================================================

@app.get("/agencies")
async def list_agencies() -> Dict[str, Any]:
    """List all agency profiles."""
    agencies = [p.to_dict() for p in AGENCY_PROFILES.values()]
    return {
        "total": len(agencies),
        "agencies": agencies,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/agencies/{agency_code}")
async def get_agency_detail(agency_code: str) -> Dict[str, Any]:
    """Get detailed agency profile."""
    code = normalize_agency(agency_code)
    profile = AGENCY_PROFILES.get(code)
    if not profile:
        raise HTTPException(status_code=404, detail=f"Agency not found: {agency_code}")
    return profile.to_dict()


# ============================================================================
# PREEMPTION ENDPOINTS
# ============================================================================

@app.get("/preemption-rules")
async def list_preemption_rules() -> Dict[str, Any]:
    """List all federal preemption rules."""
    rules: List[Dict[str, Any]] = []
    for key, rule in PREEMPTION_RULES.items():
        data = rule.to_dict()
        data["rule_key"] = key
        rules.append(data)
    return {
        "total": len(rules),
        "preemption_rules": rules,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ============================================================================
# OBLIGATION ENDPOINTS
# ============================================================================

@app.get("/obligations")
async def list_obligations(
    agency: Optional[str] = Query(None, description="Filter by agency"),
    naics_code: Optional[str] = Query(None, description="Filter by NAICS sector"),
) -> Dict[str, Any]:
    """List compliance obligations with optional filtering."""
    results: List[Dict[str, Any]] = []
    for key, obligation in COMPLIANCE_OBLIGATIONS.items():
        if agency and obligation.agency != normalize_agency(agency):
            continue
        if naics_code:
            sector = naics_code[:2]
            if sector not in obligation.applicable_industries and \
                    "All sectors" not in obligation.applicable_industries:
                continue
        data = obligation.to_dict()
        data["obligation_key"] = key
        results.append(data)

    return {
        "total": len(results),
        "obligations": results,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ============================================================================
# AUDIT TRAIL ENDPOINTS
# ============================================================================

@app.get("/audit-trail")
async def get_audit_trail(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    action: Optional[str] = Query(None, description="Filter by action type"),
    query_id: Optional[str] = Query(None, description="Filter by query ID"),
) -> Dict[str, Any]:
    """Retrieve audit trail entries."""
    telemetry = get_telemetry()
    entries = telemetry.audit.get_entries(
        limit=limit,
        offset=offset,
        action_filter=action,
        query_id_filter=query_id,
    )

    return {
        "total_entries": telemetry.audit.entry_count,
        "returned": len(entries),
        "offset": offset,
        "entries": entries,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/audit-trail/verify")
async def verify_audit_chain() -> Dict[str, Any]:
    """Verify audit trail hash chain integrity."""
    telemetry = get_telemetry()
    result = telemetry.audit.verify_chain()
    result["timestamp"] = datetime.now(timezone.utc).isoformat()
    return result


# ============================================================================
# METRICS ENDPOINT
# ============================================================================

@app.get("/metrics")
async def get_metrics() -> Dict[str, Any]:
    """Get full telemetry metrics."""
    telemetry = get_telemetry()
    metrics = telemetry.metrics.get_full_metrics()
    metrics["uptime_seconds"] = telemetry.uptime_seconds
    metrics["engine_id"] = ENGINE_ID
    metrics["version"] = ENGINE_VERSION
    metrics["timestamp"] = datetime.now(timezone.utc).isoformat()
    return metrics


# ============================================================================
# INDUSTRY CLASSIFICATION ENDPOINTS
# ============================================================================

@app.get("/industries/{naics_code}/regulations")
async def get_industry_regulations(naics_code: str) -> Dict[str, Any]:
    """Get applicable regulations for a NAICS code."""
    from semantic import NAICS_SECTOR_NAMES, get_naics_sector

    sector_name = get_naics_sector(naics_code)
    applicable = get_applicable_doctrines(naics_code)

    doctrines_detail: List[Dict[str, Any]] = []
    for key in applicable:
        doctrine = get_doctrine(key)
        if doctrine:
            doctrines_detail.append({
                "doctrine_key": key,
                "topic": doctrine.topic,
                "agency": doctrine.agency,
                "risk_level": doctrine.risk_level.value,
                "composite_risk_score": doctrine.composite_risk_score,
                "penalty_range": doctrine.penalty_range,
                "criminal_exposure": doctrine.criminal_exposure,
                "reporting_frequency": doctrine.reporting_frequency,
            })

    return {
        "naics_code": naics_code,
        "sector_name": sector_name or f"Unknown sector for {naics_code}",
        "applicable_doctrines": len(doctrines_detail),
        "doctrines": doctrines_detail,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/cfr-titles")
async def list_cfr_titles() -> Dict[str, Any]:
    """List all CFR titles with names and primary agencies."""
    titles: List[Dict[str, Any]] = []
    for title_num, title_name in sorted(CFR_TITLE_NAMES.items()):
        agency = CFR_TITLE_TO_AGENCY.get(title_num, "Various")
        titles.append({
            "title": title_num,
            "name": title_name,
            "primary_agency": agency,
        })
    return {
        "total": len(titles),
        "cfr_titles": titles,
    }


# ============================================================================
# RISK CALCULATOR ENDPOINT
# ============================================================================

@app.post("/risk-calculator")
async def risk_calculator(
    severity: int = Query(..., ge=1, le=10),
    likelihood: int = Query(..., ge=1, le=10),
    detectability: int = Query(..., ge=1, le=10),
) -> Dict[str, Any]:
    """Quick risk score calculator."""
    result = compute_risk_score(severity, likelihood, detectability)
    result["timestamp"] = datetime.now(timezone.utc).isoformat()
    return result


# ============================================================================
# MULTI-REGULATION COMPLIANCE CHECK
# ============================================================================

class MultiRegulationQuery(BaseModel):
    """Check compliance across multiple regulations simultaneously."""
    entity_name: str = Field(..., description="Entity being checked")
    naics_code: str = Field(..., min_length=2, description="NAICS code")
    regulations: List[str] = Field(..., description="List of regulation keywords or CFR refs")
    jurisdiction: str = Field(default="federal", description="Jurisdiction")
    entity_size: Optional[str] = Field(default=None, description="Entity size descriptor")


@app.post("/multi-check")
async def multi_regulation_check(query: MultiRegulationQuery) -> Dict[str, Any]:
    """Check compliance posture across multiple regulations simultaneously.

    For each regulation specified, performs doctrine matching, risk assessment,
    and returns a consolidated compliance matrix.
    """
    query_id = _generate_query_id()
    trace_id = trace_query(query_id, QueryType.COMPLIANCE_CHECK)
    start_time = time.time()

    results: List[Dict[str, Any]] = []
    total_risk_score = 0
    highest_risk: Optional[Dict[str, Any]] = None
    agencies_involved: set = set()
    criminal_exposure_count = 0

    for regulation in query.regulations:
        norm = normalize_semantics(regulation)
        match_result = match_doctrine(norm.normalized)

        result_entry: Dict[str, Any] = {
            "regulation_query": regulation,
            "normalized": norm.normalized,
            "agencies_detected": norm.agencies_detected,
        }

        if match_result:
            doctrine = get_doctrine(match_result["matched_doctrine"])
            if doctrine:
                result_entry.update({
                    "matched": True,
                    "doctrine_key": match_result["matched_doctrine"],
                    "topic": doctrine.topic,
                    "agency": doctrine.agency,
                    "risk_level": doctrine.risk_level.value,
                    "composite_risk_score": doctrine.composite_risk_score,
                    "penalty_range": doctrine.penalty_range,
                    "criminal_exposure": doctrine.criminal_exposure,
                    "key_requirements": doctrine.key_requirements,
                    "reporting_frequency": doctrine.reporting_frequency,
                    "preemption_type": doctrine.preemption_type.value,
                })
                total_risk_score += doctrine.composite_risk_score
                agencies_involved.add(doctrine.agency)
                if doctrine.criminal_exposure:
                    criminal_exposure_count += 1
                if highest_risk is None or doctrine.composite_risk_score > highest_risk.get("composite_risk_score", 0):
                    highest_risk = result_entry
        else:
            result_entry.update({
                "matched": False,
                "doctrine_key": None,
                "topic": f"No doctrine match for: {regulation}",
                "agency": None,
                "risk_level": "unknown",
                "composite_risk_score": 0,
            })

        results.append(result_entry)

    avg_risk = total_risk_score / len(query.regulations) if query.regulations else 0

    # Overall risk classification
    if avg_risk >= 500:
        overall_risk = "high"
    elif avg_risk >= 200:
        overall_risk = "medium"
    else:
        overall_risk = "low"

    latency_ms = round((time.time() - start_time) * 1000, 2)
    hash_input = f"{query.entity_name}:{query.naics_code}:{len(results)}:{total_risk_score}"
    determinism_hash = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()

    complete_trace(trace_id, ResponseLayer.COMPLIANCE_CHECK, doctrine_hit=True,
                   risk_score=float(avg_risk))

    return {
        "query_id": query_id,
        "entity_name": query.entity_name,
        "naics_code": query.naics_code,
        "jurisdiction": query.jurisdiction,
        "regulations_checked": len(query.regulations),
        "regulations_matched": sum(1 for r in results if r.get("matched")),
        "overall_risk_level": overall_risk,
        "average_risk_score": round(avg_risk, 1),
        "total_risk_score": total_risk_score,
        "agencies_involved": sorted(agencies_involved),
        "criminal_exposure_count": criminal_exposure_count,
        "highest_risk_regulation": highest_risk,
        "results": results,
        "latency_ms": latency_ms,
        "determinism_hash": determinism_hash,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ============================================================================
# REGULATORY TIMELINE TRACKER
# ============================================================================

class RegulatoryTimelineEntry(BaseModel):
    """Entry in a regulatory timeline."""
    regulation: str
    event_type: str  # "proposed_rule", "comment_period", "final_rule", "effective_date", "amendment"
    description: str
    date_str: Optional[str] = None
    agency: str
    fr_citation: Optional[str] = None
    status: str  # "completed", "pending", "upcoming"


class TimelineQuery(BaseModel):
    """Query for regulatory timeline."""
    regulation: str = Field(..., description="Regulation or regulatory area")
    agency: Optional[str] = Field(default=None, description="Agency filter")


@app.post("/timeline")
async def regulatory_timeline(query: TimelineQuery) -> Dict[str, Any]:
    """Generate a regulatory timeline for a regulation or area.

    Returns the typical lifecycle stages of a federal regulation:
    ANPRM -> NPRM -> Comment Period -> Final Rule -> Effective Date -> Amendments
    """
    query_id = _generate_query_id()
    trace_id = trace_query(query_id, QueryType.REGULATION_SEARCH)

    norm = normalize_semantics(query.regulation)
    match_result = match_doctrine(norm.normalized)

    timeline: List[Dict[str, Any]] = []
    doctrine_info: Optional[Dict[str, Any]] = None

    if match_result:
        doctrine = get_doctrine(match_result["matched_doctrine"])
        if doctrine:
            doctrine_info = {
                "doctrine_key": match_result["matched_doctrine"],
                "topic": doctrine.topic,
                "agency": doctrine.agency,
            }

            # Build standard regulatory lifecycle timeline
            timeline = [
                {
                    "stage": 1,
                    "event_type": "enabling_statute",
                    "description": f"Enabling statute enacted: {', '.join(doctrine.usc_references[:3])}",
                    "agency": doctrine.agency,
                    "status": "completed",
                },
                {
                    "stage": 2,
                    "event_type": "initial_rulemaking",
                    "description": f"Initial regulations promulgated: {', '.join(doctrine.cfr_references[:3])}",
                    "agency": doctrine.agency,
                    "status": "completed",
                },
                {
                    "stage": 3,
                    "event_type": "current_enforcement",
                    "description": f"Current enforcement posture: {doctrine.enforcement_history[:200]}",
                    "agency": doctrine.agency,
                    "status": "active",
                },
                {
                    "stage": 4,
                    "event_type": "compliance_requirements",
                    "description": f"Ongoing compliance: {doctrine.reporting_frequency}",
                    "agency": doctrine.agency,
                    "status": "active",
                },
            ]

            # Add preemption info if relevant
            if doctrine.preemption_type != PreemptionType.NONE:
                timeline.append({
                    "stage": 5,
                    "event_type": "preemption_status",
                    "description": f"Federal preemption: {doctrine.preemption_type.value}. "
                                   f"{len(doctrine.state_variations)} state variations noted.",
                    "agency": doctrine.agency,
                    "status": "active",
                })

    # Standard rulemaking process template
    rulemaking_process = [
        {
            "phase": "ANPRM",
            "full_name": "Advance Notice of Proposed Rulemaking",
            "description": "Agency solicits input on whether rulemaking is needed",
            "typical_duration": "30-90 days comment period",
        },
        {
            "phase": "NPRM",
            "full_name": "Notice of Proposed Rulemaking",
            "description": "Proposed rule published in Federal Register for public comment",
            "typical_duration": "60-120 days comment period",
        },
        {
            "phase": "Comment_Analysis",
            "full_name": "Comment Analysis Period",
            "description": "Agency reviews and responds to public comments",
            "typical_duration": "6-24 months",
        },
        {
            "phase": "Final_Rule",
            "full_name": "Final Rule Publication",
            "description": "Final rule published in Federal Register",
            "typical_duration": "Published with effective date",
        },
        {
            "phase": "Effective_Date",
            "full_name": "Rule Effective Date",
            "description": "Rule becomes legally binding, typically 30-180 days after publication",
            "typical_duration": "30-180 days after publication",
        },
        {
            "phase": "Compliance_Date",
            "full_name": "Compliance Deadline",
            "description": "Date by which regulated entities must achieve full compliance",
            "typical_duration": "Varies; may be same as effective date or phased",
        },
        {
            "phase": "Enforcement",
            "full_name": "Active Enforcement",
            "description": "Agency begins enforcement actions for non-compliance",
            "typical_duration": "Ongoing",
        },
    ]

    complete_trace(trace_id, ResponseLayer.RETRIEVAL, doctrine_hit=bool(match_result))

    hash_input = f"{query.regulation}:{len(timeline)}:{bool(match_result)}"
    determinism_hash = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()

    return {
        "query_id": query_id,
        "regulation": query.regulation,
        "doctrine_info": doctrine_info,
        "specific_timeline": timeline,
        "standard_rulemaking_process": rulemaking_process,
        "determinism_hash": determinism_hash,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ============================================================================
# PENALTY CALCULATOR
# ============================================================================

class PenaltyCalculationQuery(BaseModel):
    """Penalty estimation request."""
    agency: str = Field(..., description="Agency code (e.g., EPA, OSHA, SEC)")
    violation_type: str = Field(..., description="Type of violation")
    violation_count: int = Field(default=1, ge=1, description="Number of violations")
    days_of_violation: int = Field(default=1, ge=1, description="Duration in days")
    willful: bool = Field(default=False, description="Whether violation was willful")
    prior_violations: int = Field(default=0, ge=0, description="Number of prior violations")
    cooperation: bool = Field(default=True, description="Whether entity cooperated")
    self_reported: bool = Field(default=False, description="Whether entity self-reported")


@app.post("/penalty-calculator")
async def calculate_penalty(query: PenaltyCalculationQuery) -> Dict[str, Any]:
    """Estimate potential penalties for a regulatory violation.

    Uses enforcement action database, violation parameters, and
    mitigating/aggravating factors to compute a penalty range estimate.
    """
    query_id = _generate_query_id()
    agency_code = normalize_agency(query.agency)

    # Find matching enforcement action
    matching_action: Optional[EnforcementAction] = None
    matching_key: str = ""
    query_lower = query.violation_type.lower()

    for key, action in ENFORCEMENT_ACTIONS.items():
        if action.agency == agency_code:
            cat_lower = action.violation_category.lower()
            if any(word in cat_lower for word in query_lower.split() if len(word) > 3):
                matching_action = action
                matching_key = key
                break
        # Also check by description
        if action.agency == agency_code and not matching_action:
            desc_lower = action.description.lower()
            if any(word in desc_lower for word in query_lower.split() if len(word) > 3):
                matching_action = action
                matching_key = key

    if not matching_action:
        # Use generic penalty estimation
        base_penalty = 10000.0
        penalty_low = base_penalty * query.violation_count
        penalty_high = base_penalty * query.violation_count * 5
        if query.willful:
            penalty_low *= 3
            penalty_high *= 10
        if query.days_of_violation > 1 and penalty_high < 1_000_000:
            penalty_high *= min(query.days_of_violation, 30)

        hash_input = f"{agency_code}:{query.violation_type}:{penalty_low}:{penalty_high}"
        determinism_hash = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()

        return {
            "query_id": query_id,
            "agency": agency_code,
            "violation_type": query.violation_type,
            "matched_enforcement_template": None,
            "penalty_estimate_low": round(penalty_low, 2),
            "penalty_estimate_high": round(penalty_high, 2),
            "criminal_exposure": False,
            "methodology": "generic_estimation",
            "note": f"No specific enforcement template found for {agency_code} - "
                    f"{query.violation_type}. Estimate is approximate.",
            "determinism_hash": determinism_hash,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    # Calculate penalty range based on enforcement template
    base_low = matching_action.penalty_min or 0.0
    base_high = matching_action.penalty_max or 100_000.0

    # Per-violation calculation
    if matching_action.penalty_per_violation:
        per_violation_total = matching_action.penalty_per_violation * query.violation_count
        base_high = max(base_high, per_violation_total)

    # Per-day calculation
    if matching_action.penalty_per_day and query.days_of_violation > 1:
        per_day_total = matching_action.penalty_per_day * query.days_of_violation
        base_high = max(base_high, per_day_total)

    # Apply multipliers
    penalty_low = base_low * query.violation_count
    penalty_high = base_high * query.violation_count

    # Willful multiplier
    if query.willful:
        penalty_low *= 2.0
        penalty_high *= 5.0

    # Prior violations multiplier
    if query.prior_violations > 0:
        repeat_mult = 1.0 + (0.5 * min(query.prior_violations, 5))
        penalty_low *= repeat_mult
        penalty_high *= repeat_mult

    # Mitigation factors (reduce low end)
    mitigation_factors_applied: List[str] = []
    if query.cooperation:
        penalty_low *= 0.7
        mitigation_factors_applied.append("Cooperation with investigation (-30% low estimate)")
    if query.self_reported:
        penalty_low *= 0.5
        penalty_high *= 0.75
        mitigation_factors_applied.append("Self-reporting (-50% low / -25% high estimate)")

    # Criminal exposure assessment
    criminal_risk = matching_action.criminal_exposure and query.willful
    imprisonment_risk: Optional[str] = None
    if criminal_risk and matching_action.max_imprisonment_years:
        imprisonment_risk = f"Up to {matching_action.max_imprisonment_years} years per violation"

    hash_input = f"{agency_code}:{matching_key}:{penalty_low:.2f}:{penalty_high:.2f}"
    determinism_hash = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()

    return {
        "query_id": query_id,
        "agency": agency_code,
        "violation_type": query.violation_type,
        "matched_enforcement_template": {
            "action_key": matching_key,
            "violation_category": matching_action.violation_category,
            "statute_basis": matching_action.statute_basis,
        },
        "parameters": {
            "violation_count": query.violation_count,
            "days_of_violation": query.days_of_violation,
            "willful": query.willful,
            "prior_violations": query.prior_violations,
            "cooperation": query.cooperation,
            "self_reported": query.self_reported,
        },
        "penalty_estimate_low": round(penalty_low, 2),
        "penalty_estimate_high": round(penalty_high, 2),
        "criminal_exposure": criminal_risk,
        "imprisonment_risk": imprisonment_risk,
        "mitigation_factors_applied": mitigation_factors_applied,
        "aggravating_factors": matching_action.aggravating_factors,
        "methodology": "enforcement_template_calculation",
        "disclaimer": "Penalty estimates are approximate and based on statutory maximums. "
                      "Actual penalties depend on specific facts, agency discretion, and "
                      "negotiation. Consult legal counsel for specific matters.",
        "determinism_hash": determinism_hash,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ============================================================================
# CROSS-AGENCY REGULATION MAPPER
# ============================================================================

@app.get("/cross-agency/{topic}")
async def cross_agency_map(topic: str) -> Dict[str, Any]:
    """Map a regulatory topic across all agencies that have jurisdiction.

    Shows which agencies regulate what aspects of a given topic,
    identifying potential overlaps and coordination requirements.
    """
    query_id = _generate_query_id()
    topic_lower = topic.lower()

    agency_coverage: Dict[str, Dict[str, Any]] = {}

    for key, doctrine in DOCTRINE_CACHE.items():
        score = compute_doctrine_match_score(topic_lower, doctrine)
        if score >= 15:
            agency = doctrine.agency
            if agency not in agency_coverage:
                agency_coverage[agency] = {
                    "agency_code": agency,
                    "agency_name": AGENCY_PROFILES[agency].full_name if agency in AGENCY_PROFILES else agency,
                    "doctrines": [],
                    "total_relevance_score": 0,
                    "max_risk_score": 0,
                    "cfr_titles": set(),
                }
            agency_coverage[agency]["doctrines"].append({
                "doctrine_key": key,
                "topic": doctrine.topic,
                "relevance_score": score,
                "risk_level": doctrine.risk_level.value,
                "composite_risk_score": doctrine.composite_risk_score,
            })
            agency_coverage[agency]["total_relevance_score"] += score
            agency_coverage[agency]["max_risk_score"] = max(
                agency_coverage[agency]["max_risk_score"],
                doctrine.composite_risk_score,
            )
            for ref in doctrine.cfr_references:
                import re as _re
                title_match = _re.match(r"(\d+)\s+CFR", ref)
                if title_match:
                    agency_coverage[agency]["cfr_titles"].add(int(title_match.group(1)))

    # Convert sets to lists for JSON serialization
    for data in agency_coverage.values():
        data["cfr_titles"] = sorted(data["cfr_titles"])

    # Sort by relevance
    sorted_agencies = sorted(
        agency_coverage.values(),
        key=lambda x: x["total_relevance_score"],
        reverse=True,
    )

    # Identify potential jurisdiction overlaps
    overlaps: List[Dict[str, Any]] = []
    agency_list = list(agency_coverage.keys())
    for i in range(len(agency_list)):
        for j in range(i + 1, len(agency_list)):
            a1 = agency_list[i]
            a2 = agency_list[j]
            d1_keys = {d["doctrine_key"] for d in agency_coverage[a1]["doctrines"]}
            d2_keys = {d["doctrine_key"] for d in agency_coverage[a2]["doctrines"]}
            # Check if they cover similar areas via keyword overlap
            d1_topics = " ".join(d["topic"].lower() for d in agency_coverage[a1]["doctrines"])
            d2_topics = " ".join(d["topic"].lower() for d in agency_coverage[a2]["doctrines"])
            common_words = set(d1_topics.split()) & set(d2_topics.split()) - {"and", "the", "of", "for", "in", "or"}
            if len(common_words) >= 3:
                overlaps.append({
                    "agencies": [a1, a2],
                    "overlap_indicator": len(common_words),
                    "common_terms": sorted(common_words)[:10],
                    "recommendation": f"Coordinate compliance efforts between {a1} and {a2}",
                })

    hash_input = f"{topic}:{len(sorted_agencies)}:{sum(a['total_relevance_score'] for a in sorted_agencies)}"
    determinism_hash = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()

    return {
        "query_id": query_id,
        "topic": topic,
        "agencies_with_jurisdiction": len(sorted_agencies),
        "agency_map": sorted_agencies,
        "jurisdiction_overlaps": overlaps,
        "determinism_hash": determinism_hash,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ============================================================================
# COMPLIANCE SUMMARY DASHBOARD
# ============================================================================

@app.get("/dashboard/{naics_code}")
async def compliance_dashboard(naics_code: str) -> Dict[str, Any]:
    """Generate a compliance dashboard summary for an industry sector.

    Provides an at-a-glance view of:
    - Total applicable regulations
    - Risk distribution
    - Agency involvement
    - Key deadlines
    - Criminal exposure areas
    """
    from semantic import get_naics_sector

    query_id = _generate_query_id()
    sector_name = get_naics_sector(naics_code) or f"NAICS {naics_code}"
    applicable = get_applicable_doctrines(naics_code)

    risk_distribution: Dict[str, int] = defaultdict(int)
    agencies: Dict[str, int] = defaultdict(int)
    criminal_exposure_areas: List[Dict[str, str]] = []
    total_risk_score = 0
    max_risk_score = 0

    for key in applicable:
        doctrine = get_doctrine(key)
        if doctrine:
            risk_distribution[doctrine.risk_level.value] += 1
            agencies[doctrine.agency] += 1
            total_risk_score += doctrine.composite_risk_score
            max_risk_score = max(max_risk_score, doctrine.composite_risk_score)
            if doctrine.criminal_exposure:
                criminal_exposure_areas.append({
                    "doctrine_key": key,
                    "topic": doctrine.topic,
                    "agency": doctrine.agency,
                    "penalty_range": doctrine.penalty_range,
                })

    avg_risk = total_risk_score / len(applicable) if applicable else 0

    # Key obligations for this industry
    key_obligations: List[Dict[str, Any]] = []
    for obl_key, obligation in COMPLIANCE_OBLIGATIONS.items():
        sector = naics_code[:2]
        if sector in obligation.applicable_industries or "All sectors" in obligation.applicable_industries:
            key_obligations.append({
                "obligation_id": obligation.obligation_id,
                "description": obligation.description,
                "agency": obligation.agency,
                "frequency": obligation.frequency,
                "deadline": obligation.deadline_type,
            })

    hash_input = f"{naics_code}:{len(applicable)}:{total_risk_score}"
    determinism_hash = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()

    return {
        "query_id": query_id,
        "naics_code": naics_code,
        "industry": sector_name,
        "total_applicable_regulations": len(applicable),
        "risk_summary": {
            "average_risk_score": round(avg_risk, 1),
            "max_risk_score": max_risk_score,
            "distribution": dict(risk_distribution),
        },
        "agency_involvement": dict(sorted(agencies.items(), key=lambda x: x[1], reverse=True)),
        "criminal_exposure_areas": criminal_exposure_areas,
        "key_obligations": key_obligations,
        "determinism_hash": determinism_hash,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ============================================================================
# ERROR HANDLER
# ============================================================================

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Global exception handler with telemetry logging."""
    log_error(None, str(exc), ErrorDomain.UNKNOWN, {"path": str(request.url)})
    logger.exception(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc)[:500],
            "engine": ENGINE_ID,
            "version": ENGINE_VERSION,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )


# ============================================================================
# ENTRYPOINT
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting {ENGINE_NAME} v{ENGINE_VERSION} on port {ENGINE_PORT}")
    uvicorn.run(
        "engine:app",
        host="0.0.0.0",
        port=ENGINE_PORT,
        reload=False,
        log_level="info",
    )
