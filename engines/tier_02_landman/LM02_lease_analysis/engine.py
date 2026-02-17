"""
ECHO LM02 LEASE ANALYSIS ENGINE - Production Architecture
Professional-grade oil and gas lease analysis engine for the Permian Basin.

Architecture:
    Layer 1: Doctrine Cache (0-200ms) - Pre-compiled lease reasoning
    Layer 2: Semantic Retrieval (200-700ms) - Term normalization, legal desc parsing
    Layer 3: Deep Analysis (on-demand) - Multi-clause synthesis, NRI calc, comparison

Response Modes:
    FAST:     Doctrine-driven, minimal citations, sub-2 seconds
    STANDARD: Balanced analysis with clause references
    DEEP:     Full lease audit with all clauses, comparisons, risk flags

Engine ID: LM02
Tier: T2_LANDMAN
Mode: DET (Deterministic)
Port: 8402
Author: ECHO OMEGA PRIME
Authority: 11.0 SOVEREIGN
"""

from __future__ import annotations

import hashlib
import json
import sys
import time
import traceback
import uuid
from collections import defaultdict
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal, ROUND_HALF_UP
from enum import Enum
from fractions import Fraction
from pathlib import Path
from typing import Any, ClassVar, Dict, List, Literal, Optional, Set, Tuple, Union, Deque
from collections import deque

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import BaseModel, Field, field_validator

# ============================================================================
# LOCAL IMPORTS
# ============================================================================

ENGINE_DIR = Path(__file__).parent
if str(ENGINE_DIR) not in sys.path:
    sys.path.insert(0, str(ENGINE_DIR))

_SHARED_DIR = str(Path(__file__).resolve().parent.parent / "_shared")
if _SHARED_DIR not in sys.path:
    sys.path.insert(0, _SHARED_DIR)

try:
    from cloud_retriever import retrieve_cloud_knowledge
    _CLOUD_AVAILABLE = True
except ImportError:
    _CLOUD_AVAILABLE = False

from doctrines import (
    DOCTRINE_CACHE,
    DOCTRINE_CACHE_VERSION,
    ClauseRiskLevel,
    DoctrineCategory,
    LeaseDoctrineBlock,
    LeaseTermType,
    PoolingType,
    PughClauseType,
    RoyaltyType,
    get_applicable_doctrines,
    get_doctrine,
    get_doctrine_summary,
    list_doctrine_keys,
    match_doctrine,
    verify_cache_integrity,
)
from search import (
    ExpirationAlertResult,
    ExpirationWindow,
    LeaseIndexEntry,
    LeaseSearchIndex,
    LeaseSearchQuery,
    LeaseSearchResult,
    LeaseStatus,
    SearchResponse,
    SortDirection,
    SortField,
    generate_expiration_alerts,
    get_search_index,
    search_by_document,
    search_by_legal_description,
    search_by_lessor_lessee,
    search_expiring_leases,
    search_leases,
)
from semantic import (
    COMMON_ROYALTY_FRACTIONS,
    COUNTY_TO_RRC_DISTRICT,
    FORMATION_ALIASES,
    LEASE_TERM_GLOSSARY,
    OPERATOR_ALIASES,
    DepthInterval,
    FormationType,
    InterestType,
    LeaseClauseType,
    LegalDescription,
    NormalizationResult,
    ParsedFraction,
    PartyRole,
    get_glossary_definition,
    get_rrc_district,
    identify_clause_types,
    normalize_formation_name,
    normalize_lease_term,
    normalize_operator_name,
    parse_depth_interval,
    parse_legal_description,
    parse_royalty_fraction,
    verify_semantic_map_integrity,
)
from telemetry import (
    AuditEntry,
    ErrorDomain,
    ErrorSeverity,
    MetricsCollector,
    MutationOrigin,
    MutationType,
    QueryType,
    ResponseLayer,
    TelemetryManager,
    complete_trace,
    fail_trace,
    get_telemetry,
    log_error,
    record_doctrine_mutation,
    trace_query,
)

# ============================================================================
# CONFIGURATION
# ============================================================================

ENGINE_ID = "LM02"
ENGINE_NAME = "Lease Analysis Engine"
ENGINE_VERSION = "1.1.0"
ENGINE_TIER = "T2_LANDMAN"
ENGINE_MODE = "DET"
ENGINE_PORT = 8402

LOG_DIR = Path("O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/LM02_lease_analysis/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

logger.add(
    LOG_DIR / "lm02_engine_{time}.log",
    rotation="50 MB",
    retention="30 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {module}:{function}:{line} | {message}",
)

_ENGINE_START_TIME: float = time.time()

# Load config
CONFIG_PATH = ENGINE_DIR / "config.json"
ENGINE_CONFIG: Dict[str, Any] = {}
if CONFIG_PATH.exists():
    ENGINE_CONFIG = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    logger.info(f"LM02 config loaded from {CONFIG_PATH}")
else:
    logger.warning(f"LM02 config not found at {CONFIG_PATH}, using defaults")


# ============================================================================
# PYDANTIC MODELS - REQUEST/RESPONSE
# ============================================================================


class ResponseMode(str, Enum):
    """Analysis response depth mode."""
    FAST = "FAST"
    STANDARD = "STANDARD"
    DEEP = "DEEP"


class ConfidenceStratification(str, Enum):
    """Confidence stratification zones for lease analysis."""
    DEFENSIBLE = "DEFENSIBLE"  # High confidence, audit-defensible, backed by statute/case law
    AGGRESSIVE = "AGGRESSIVE"  # Favorable interpretation, industry practice, not guaranteed
    DISCLOSURE = "DISCLOSURE"  # Material risk, requires disclosure, uncertain outcome
    HIGH_RISK = "HIGH_RISK"  # Speculative, adverse precedent, litigation risk


class AnalysisZone(str, Enum):
    """Analysis zones - never blur position zones."""
    PLANNING = "PLANNING"  # Strategic lease acquisition, portfolio planning
    REPORTING = "REPORTING"  # Asset reporting, reserves booking, investor disclosure
    AUDIT = "AUDIT"  # Compliance verification, title opinion, audit defense


class AuthorityLevel(str, Enum):
    """Hierarchical authority levels for doctrine sources."""
    CONSTITUTIONAL = "CONSTITUTIONAL"  # TX Constitution, US Constitution
    STATUTORY = "STATUTORY"  # TX Natural Resources Code, TX Property Code, federal statutes
    REGULATORY = "REGULATORY"  # Railroad Commission rules, BLM regs
    CASE_LAW = "CASE_LAW"  # TX Supreme Court, TX Courts of Appeals, federal courts
    INDUSTRY_STANDARD = "INDUSTRY_STANDARD"  # AAPL forms, common practice
    EXPERT_OPINION = "EXPERT_OPINION"  # Landman/attorney interpretation


AUTHORITY_WEIGHTS: Dict[AuthorityLevel, float] = {
    AuthorityLevel.CONSTITUTIONAL: 1.0,
    AuthorityLevel.STATUTORY: 0.95,
    AuthorityLevel.REGULATORY: 0.85,
    AuthorityLevel.CASE_LAW: 0.80,
    AuthorityLevel.INDUSTRY_STANDARD: 0.60,
    AuthorityLevel.EXPERT_OPINION: 0.40,
}


class IssueCategory(str, Enum):
    """Issue categories for multi-doctrine decomposition."""
    TERM_STATUS = "TERM_STATUS"  # Habendum, HBP, expiration, extension
    ROYALTY_BURDEN = "ROYALTY_BURDEN"  # Royalty, ORRI, NRI, cost-free language
    ACREAGE_RETENTION = "ACREAGE_RETENTION"  # Pugh, pooling, retained acreage
    DEPTH_RIGHTS = "DEPTH_RIGHTS"  # Depth limitations, Pugh depth, formation rights
    OPERATIONAL_OBLIGATIONS = "OPERATIONAL_OBLIGATIONS"  # Continuous drilling, offset wells, shut-in
    ASSIGNMENT_TRANSFER = "ASSIGNMENT_TRANSFER"  # ROFR, preferential rights, consent to assign
    SURFACE_RIGHTS = "SURFACE_RIGHTS"  # Surface use, restoration, surface damage payments
    FORCE_MAJEURE = "FORCE_MAJEURE"  # Force majeure, impossibility, market disruption
    TERMINATION = "TERMINATION"  # Surrender, release, cessation of production
    DISPUTE_RESOLUTION = "DISPUTE_RESOLUTION"  # Arbitration, venue, choice of law


class IssueStratum(str, Enum):
    """Issue stratification layers."""
    THRESHOLD = "THRESHOLD"  # Does clause exist? Is it triggered?
    QUANTITATIVE = "QUANTITATIVE"  # Acreage, dates, rates, intervals
    INTERPRETIVE = "INTERPRETIVE"  # Ambiguous language, conflicting clauses
    ADVERSARIAL = "ADVERSARIAL"  # Lessor vs lessee interpretation, litigation posture


# ─── Lease Record Model ───

class LeaseParty(BaseModel):
    """A party to the lease transaction."""
    name: str = Field(..., description="Party name")
    role: str = Field(..., description="Role: lessor, lessee, assignor, assignee")
    address: Optional[str] = Field(None, description="Address if available")
    entity_type: Optional[str] = Field(None, description="Individual, LLC, Corporation, Trust, Estate")
    interest_fraction: Optional[str] = Field(None, description="Interest fraction if specified")
    interest_decimal: Optional[float] = Field(None, description="Interest as decimal")


class LeaseClauseInfo(BaseModel):
    """Information about a specific lease clause."""
    clause_type: str = Field(..., description="Clause type identifier")
    clause_text: Optional[str] = Field(None, description="Original clause text")
    summary: str = Field("", description="Plain-language summary")
    risk_level: str = Field("moderate", description="Risk assessment: low, moderate, high, critical")
    notes: List[str] = Field(default_factory=list, description="Analysis notes")


class LeaseRecord(BaseModel):
    """Complete oil and gas lease record."""
    lease_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:16], description="Unique lease ID")
    document_number: Optional[str] = Field(None, description="County document number")
    volume: Optional[str] = Field(None, description="Recording volume")
    page: Optional[str] = Field(None, description="Recording page")
    county: Optional[str] = Field(None, description="County name")
    state: str = Field("Texas", description="State")
    instrument_type: str = Field("OGL", description="Instrument type code")

    # Parties
    lessor: Optional[LeaseParty] = Field(None, description="Lessor (mineral owner)")
    lessee: Optional[LeaseParty] = Field(None, description="Lessee (operator)")
    additional_parties: List[LeaseParty] = Field(default_factory=list)

    # Legal description
    legal_description_text: Optional[str] = Field(None, description="Raw legal description")
    parsed_legal: Optional[Dict[str, Any]] = Field(None, description="Parsed legal description components")
    acres: Optional[float] = Field(None, description="Total acres")

    # Dates and terms
    lease_date: Optional[date] = Field(None, description="Lease execution date")
    recording_date: Optional[date] = Field(None, description="County recording date")
    effective_date: Optional[date] = Field(None, description="Effective date if different from lease date")
    primary_term_years: Optional[int] = Field(None, description="Primary term duration in years")
    primary_term_expiration: Optional[date] = Field(None, description="Calculated primary term end date")

    # Financial terms
    bonus_per_acre: Optional[float] = Field(None, description="Bonus consideration per acre")
    total_bonus: Optional[float] = Field(None, description="Total bonus amount")
    delay_rental_per_acre: Optional[float] = Field(None, description="Annual delay rental per acre")
    royalty_fraction: Optional[str] = Field(None, description="Royalty fraction (e.g., '1/4')")
    royalty_rate: Optional[float] = Field(None, description="Royalty rate as decimal")
    paid_up: bool = Field(False, description="Paid-up lease (no annual delay rental)")

    # Clause flags
    has_pugh_clause: bool = Field(False)
    pugh_type: Optional[str] = Field(None, description="vertical, horizontal, depth, combined")
    has_depth_limitation: bool = Field(False)
    depth_limitation_text: Optional[str] = Field(None)
    has_continuous_development: bool = Field(False)
    continuous_dev_gap_days: Optional[int] = Field(None)
    has_force_majeure: bool = Field(False)
    has_shut_in: bool = Field(False)
    shut_in_max_months: Optional[int] = Field(None)
    has_pooling: bool = Field(False)
    pooling_max_acres_oil: Optional[float] = Field(None)
    pooling_max_acres_gas: Optional[float] = Field(None)
    has_surface_restrictions: bool = Field(False)
    has_mother_hubbard: bool = Field(False)
    has_preferential_right: bool = Field(False)
    has_surrender_clause: bool = Field(False)

    # Status
    current_status: str = Field("unknown", description="Current lease status")
    held_by_production: bool = Field(False)
    producing_wells: List[str] = Field(default_factory=list, description="RRC well API numbers")
    target_formations: List[str] = Field(default_factory=list, description="Target formations")

    # Metadata
    source: str = Field("manual", description="Data source: manual, encore, shadowglass, r2")
    clauses: List[LeaseClauseInfo] = Field(default_factory=list, description="Identified clauses")
    notes: List[str] = Field(default_factory=list, description="Analysis notes")
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ─── Analysis Request/Response Models ───

class LeaseAnalysisRequest(BaseModel):
    """Request for lease analysis."""
    lease: Optional[LeaseRecord] = Field(None, description="Full lease record to analyze")
    lease_id: Optional[str] = Field(None, description="Existing lease ID to analyze")
    lease_text: Optional[str] = Field(None, description="Raw lease text to parse and analyze")
    analysis_type: str = Field("full", description="full, term, royalty, clause, expiration, pugh")
    response_mode: ResponseMode = Field(ResponseMode.STANDARD, description="Response depth")
    include_doctrine: bool = Field(True, description="Include doctrine references")
    include_risk_assessment: bool = Field(True, description="Include risk assessment")


class TermAnalysis(BaseModel):
    """Analysis of lease term status."""
    current_term: str = Field(..., description="primary, secondary, hbp, expired, etc.")
    primary_term_start: Optional[date] = None
    primary_term_end: Optional[date] = None
    primary_term_years: Optional[int] = None
    days_remaining_primary: Optional[int] = None
    is_hbp: bool = False
    hbp_since: Optional[date] = None
    is_expired: bool = False
    expiration_date: Optional[date] = None
    days_until_expiration: Optional[int] = None
    saving_clauses: List[str] = Field(default_factory=list, description="Active saving clauses")
    risk_level: str = Field("moderate")
    analysis_notes: List[str] = Field(default_factory=list)
    doctrine_references: List[str] = Field(default_factory=list)


class RoyaltyCalculation(BaseModel):
    """Detailed royalty calculation result."""
    royalty_fraction: str = Field(..., description="Royalty fraction (e.g., '1/4')")
    royalty_decimal: float = Field(..., description="Royalty as decimal")
    gross_royalty_factor: float = Field(..., description="Gross royalty factor before deductions")
    post_production_deductions: Dict[str, float] = Field(default_factory=dict)
    net_royalty_factor: float = Field(0.0)
    overriding_royalties: List[Dict[str, Any]] = Field(default_factory=list)
    total_burden: float = Field(0.0, description="Total burden on working interest")
    working_interest: float = Field(0.0, description="Working interest after royalty")
    net_revenue_interest: float = Field(0.0, description="NRI after all burdens")
    pooling_factor: Optional[float] = Field(None, description="Unit participation factor")
    pooled_nri: Optional[float] = Field(None, description="NRI adjusted for pooling")
    severance_tax_rate: Optional[float] = Field(None, description="Applicable severance tax rate")
    calculation_steps: List[str] = Field(default_factory=list, description="Step-by-step calculation")
    warnings: List[str] = Field(default_factory=list)


class PughClauseAnalysis(BaseModel):
    """Pugh clause impact analysis."""
    has_pugh: bool = False
    pugh_type: Optional[str] = None
    total_lease_acres: Optional[float] = None
    pooled_acres: Optional[float] = None
    retained_acres: Optional[float] = None
    released_acres: Optional[float] = None
    retained_percentage: Optional[float] = None
    released_percentage: Optional[float] = None
    trigger_date: Optional[date] = None
    days_until_trigger: Optional[int] = None
    depth_retained: Optional[str] = None
    depth_released: Optional[str] = None
    formations_retained: List[str] = Field(default_factory=list)
    formations_released: List[str] = Field(default_factory=list)
    impact_assessment: str = Field("")
    risk_level: str = Field("moderate")
    recommendations: List[str] = Field(default_factory=list)
    doctrine_references: List[str] = Field(default_factory=list)


class LeaseExpirationAlert(BaseModel):
    """Lease expiration alert."""
    lease_id: str
    alert_level: str = Field("info", description="critical, warning, info")
    days_until_expiration: int
    expiration_date: date
    lessor_name: Optional[str] = None
    lessee_name: Optional[str] = None
    county: Optional[str] = None
    legal_description: Optional[str] = None
    acres: Optional[float] = None
    royalty_rate: Optional[float] = None
    saving_clauses: List[str] = Field(default_factory=list)
    recommended_actions: List[str] = Field(default_factory=list)


class LeaseAnalysisResponse(BaseModel):
    """Full lease analysis response."""
    lease_id: str
    analysis_type: str
    response_mode: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    lease: Optional[LeaseRecord] = None
    term_analysis: Optional[TermAnalysis] = None
    royalty_calculation: Optional[RoyaltyCalculation] = None
    pugh_analysis: Optional[PughClauseAnalysis] = None
    identified_clauses: List[LeaseClauseInfo] = Field(default_factory=list)
    expiration_alerts: List[LeaseExpirationAlert] = Field(default_factory=list)
    risk_summary: Dict[str, Any] = Field(default_factory=dict)
    doctrine_references: List[Dict[str, str]] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    trace_id: str = Field("")
    processing_time_ms: float = Field(0.0)
    determinism_hash: str = Field("")


class LeaseComparisonRequest(BaseModel):
    """Request to compare two or more leases."""
    lease_ids: List[str] = Field(default_factory=list, description="Lease IDs to compare")
    leases: List[LeaseRecord] = Field(default_factory=list, description="Lease records to compare")
    comparison_aspects: List[str] = Field(
        default_factory=lambda: ["royalty", "term", "pooling", "pugh", "surface_use"],
        description="Aspects to compare",
    )
    response_mode: ResponseMode = Field(ResponseMode.STANDARD)


class LeaseComparisonResponse(BaseModel):
    """Lease comparison result."""
    leases_compared: int
    comparison_aspects: List[str]
    comparisons: Dict[str, List[Dict[str, Any]]] = Field(default_factory=dict)
    best_for_lessor: Optional[str] = Field(None, description="Lease ID best for lessor")
    best_for_lessee: Optional[str] = Field(None, description="Lease ID best for lessee")
    summary: str = Field("")
    recommendations: List[str] = Field(default_factory=list)
    trace_id: str = Field("")
    processing_time_ms: float = Field(0.0)
    determinism_hash: str = Field("")


class NRICalculationRequest(BaseModel):
    """Request for NRI calculation."""
    mineral_interest: float = Field(1.0, ge=0.0, le=1.0, description="Mineral interest fraction")
    royalty_rate: float = Field(0.25, ge=0.0, le=1.0, description="Royalty rate (decimal)")
    overriding_royalties: List[Dict[str, float]] = Field(
        default_factory=list,
        description="List of {name: str, rate: float} for ORRIs",
    )
    other_burdens: List[Dict[str, float]] = Field(
        default_factory=list,
        description="Other burdens (production payments, NPIs, etc.)",
    )
    pooling_factor: Optional[float] = Field(None, ge=0.0, le=1.0, description="Unit participation factor")
    product_type: str = Field("oil", description="oil or gas")


class NRICalculationResponse(BaseModel):
    """NRI calculation result."""
    mineral_interest: float
    royalty_rate: float
    gross_working_interest: float
    total_orri_burden: float
    total_other_burdens: float
    total_burden: float
    net_revenue_interest: float
    pooling_factor: Optional[float]
    pooled_nri: Optional[float]
    severance_tax_rate: float
    after_tax_nri: float
    calculation_steps: List[str]
    warnings: List[str] = Field(default_factory=list)
    determinism_hash: str = Field("")


# ============================================================================
# TIE-20 COMPONENT: AUTHORITY HARDENING
# ============================================================================


@dataclass
class AuthoritySource:
    """A single authority source with hierarchical weighting."""
    citation: str
    authority_level: AuthorityLevel
    weight: float
    summary: str
    url: Optional[str] = None

    def __post_init__(self):
        """Set weight from authority level if not provided."""
        if self.weight == 0.0:
            self.weight = AUTHORITY_WEIGHTS.get(self.authority_level, 0.5)


class AuthorityHardeningEngine:
    """Hierarchical authority resolution with conflict detection."""

    def __init__(self):
        """Initialize authority engine."""
        self._authority_index: Dict[str, List[AuthoritySource]] = defaultdict(list)
        logger.info("Authority hardening engine initialized")

    def add_authority(self, topic: str, source: AuthoritySource) -> None:
        """Add an authority source for a topic."""
        self._authority_index[topic].append(source)
        logger.debug(f"Added {source.authority_level.value} authority for {topic}: {source.citation}")

    def resolve_authority(self, topic: str) -> Optional[AuthoritySource]:
        """Resolve the highest authority source for a topic."""
        sources = self._authority_index.get(topic, [])
        if not sources:
            return None
        # Sort by weight (descending), then alphabetically by citation
        sorted_sources = sorted(sources, key=lambda s: (-s.weight, s.citation))
        return sorted_sources[0]

    def detect_conflicts(self, topic: str) -> List[Tuple[AuthoritySource, AuthoritySource]]:
        """Detect conflicting authority sources on the same topic."""
        sources = self._authority_index.get(topic, [])
        conflicts: List[Tuple[AuthoritySource, AuthoritySource]] = []

        for i, source_a in enumerate(sources):
            for source_b in sources[i+1:]:
                # Conflict if summaries differ and authority levels are close
                if source_a.summary != source_b.summary:
                    weight_diff = abs(source_a.weight - source_b.weight)
                    if weight_diff < 0.2:  # Within 0.2 weight points = conflict
                        conflicts.append((source_a, source_b))

        return conflicts

    def get_all_authorities(self, topic: str) -> List[AuthoritySource]:
        """Get all authority sources for a topic, sorted by weight."""
        sources = self._authority_index.get(topic, [])
        return sorted(sources, key=lambda s: -s.weight)


# ============================================================================
# TIE-20 COMPONENT: DRIFT WATCHER
# ============================================================================


@dataclass
class DriftObservation:
    """Single observation of doctrine drift."""
    timestamp: datetime
    doctrine_key: str
    expected_conclusion: str
    observed_conclusion: str
    drift_magnitude: float  # 0.0 to 1.0
    query_hash: str
    context_summary: str


class DriftWatcher:
    """Detect doctrine drift over time by comparing expected vs observed conclusions."""

    MAX_OBSERVATIONS = 1000

    def __init__(self):
        """Initialize drift watcher."""
        self._observations: Deque[DriftObservation] = deque(maxlen=self.MAX_OBSERVATIONS)
        self._drift_by_doctrine: Dict[str, List[DriftObservation]] = defaultdict(list)
        logger.info("Drift watcher initialized")

    def record_observation(self, obs: DriftObservation) -> None:
        """Record a drift observation."""
        self._observations.append(obs)
        self._drift_by_doctrine[obs.doctrine_key].append(obs)

        if obs.drift_magnitude > 0.3:
            logger.warning(
                f"DRIFT DETECTED: {obs.doctrine_key} | "
                f"Expected: {obs.expected_conclusion[:60]} | "
                f"Observed: {obs.observed_conclusion[:60]} | "
                f"Magnitude: {obs.drift_magnitude:.2f}"
            )

    def get_drift_summary(self, doctrine_key: Optional[str] = None) -> Dict[str, Any]:
        """Get drift summary for a specific doctrine or all doctrines."""
        if doctrine_key:
            obs_list = self._drift_by_doctrine.get(doctrine_key, [])
        else:
            obs_list = list(self._observations)

        if not obs_list:
            return {"total_observations": 0, "drift_detected": False}

        total = len(obs_list)
        drifted = sum(1 for o in obs_list if o.drift_magnitude > 0.2)
        avg_magnitude = sum(o.drift_magnitude for o in obs_list) / total

        return {
            "total_observations": total,
            "drift_detected": drifted > 0,
            "drift_count": drifted,
            "drift_rate": round(drifted / total, 3),
            "avg_drift_magnitude": round(avg_magnitude, 3),
            "max_drift": round(max((o.drift_magnitude for o in obs_list), default=0.0), 3),
            "recent_drifts": [
                {
                    "timestamp": o.timestamp.isoformat(),
                    "doctrine_key": o.doctrine_key,
                    "magnitude": round(o.drift_magnitude, 3),
                    "context": o.context_summary[:100],
                }
                for o in sorted(obs_list, key=lambda x: -x.drift_magnitude)[:5]
            ],
        }


# ============================================================================
# TIE-20 COMPONENT: COVERAGE MAP
# ============================================================================


@dataclass
class DoctrineInvocation:
    """Record of a doctrine being triggered (or not)."""
    timestamp: datetime
    query_hash: str
    doctrine_key: str
    triggered: bool
    confidence_score: float
    query_summary: str


class CoverageTracker:
    """Track triggered vs missed doctrines and detect epistemic gaps."""

    MAX_INVOCATIONS = 5000

    def __init__(self, total_doctrines: int = 0):
        """Initialize coverage tracker."""
        self._total_doctrines = total_doctrines
        self._invocations: Deque[DoctrineInvocation] = deque(maxlen=self.MAX_INVOCATIONS)
        self._triggered_count: Dict[str, int] = defaultdict(int)
        self._missed_count: Dict[str, int] = defaultdict(int)
        logger.info(f"Coverage tracker initialized with {total_doctrines} doctrines")

    def record_invocation(self, inv: DoctrineInvocation) -> None:
        """Record a doctrine invocation."""
        self._invocations.append(inv)
        if inv.triggered:
            self._triggered_count[inv.doctrine_key] += 1
        else:
            self._missed_count[inv.doctrine_key] += 1

    def get_coverage_map(self) -> Dict[str, Any]:
        """Get full coverage statistics."""
        all_keys = set(self._triggered_count.keys()) | set(self._missed_count.keys())
        triggered = set(self._triggered_count.keys())
        never_triggered = {k for k in all_keys if self._triggered_count[k] == 0}

        # Epistemic gaps: doctrines that exist but are never triggered
        epistemic_gaps = list(never_triggered)

        # Coverage rate
        coverage_rate = len(triggered) / self._total_doctrines if self._total_doctrines > 0 else 0.0

        # Top triggered doctrines
        top_triggered = sorted(
            self._triggered_count.items(),
            key=lambda x: -x[1]
        )[:10]

        return {
            "total_doctrines": self._total_doctrines,
            "doctrines_triggered": len(triggered),
            "doctrines_never_triggered": len(never_triggered),
            "coverage_rate": round(coverage_rate, 3),
            "total_invocations": len(self._invocations),
            "epistemic_gaps": epistemic_gaps[:20],  # First 20 gaps
            "top_triggered": [
                {"doctrine_key": k, "count": c} for k, c in top_triggered
            ],
            "recent_invocations": [
                {
                    "doctrine_key": inv.doctrine_key,
                    "triggered": inv.triggered,
                    "confidence": round(inv.confidence_score, 3),
                    "query": inv.query_summary[:80],
                }
                for inv in list(self._invocations)[-10:]
            ],
        }


# ============================================================================
# TIE-20 COMPONENT: FACT FRAGILITY SCORING
# ============================================================================


@dataclass
class FactFragilityScore:
    """Fragility assessment for a specific fact in lease analysis."""
    fact_description: str
    verifiability: float  # 0.0 = unverifiable, 1.0 = objective/verifiable
    recharacterization_risk: float  # 0.0 = no risk, 1.0 = high risk of reinterpretation
    testimony_dependence: float  # 0.0 = documentary, 1.0 = relies on witness testimony
    adversary_position: Optional[str] = None
    confidence_zone: ConfidenceStratification = ConfidenceStratification.DEFENSIBLE

    @property
    def fragility_index(self) -> float:
        """Composite fragility score (higher = more fragile)."""
        return round(
            (1.0 - self.verifiability) * 0.4 +
            self.recharacterization_risk * 0.4 +
            self.testimony_dependence * 0.2,
            3
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "fact": self.fact_description,
            "verifiability": round(self.verifiability, 3),
            "recharacterization_risk": round(self.recharacterization_risk, 3),
            "testimony_dependence": round(self.testimony_dependence, 3),
            "fragility_index": self.fragility_index,
            "confidence_zone": self.confidence_zone.value,
            "adversary_position": self.adversary_position,
        }


class FactFragilityAnalyzer:
    """Analyze fact fragility in lease analysis conclusions."""

    def __init__(self):
        """Initialize fact fragility analyzer."""
        logger.info("Fact fragility analyzer initialized")

    def assess_lease_fact(
        self,
        fact: str,
        source: str,
        lease: Optional[Any] = None
    ) -> FactFragilityScore:
        """Assess fragility of a lease analysis fact.

        Args:
            fact: The factual assertion being made.
            source: Source of the fact (e.g., "recorded_lease_text", "RRC_production", "operator_statement").
            lease: Optional lease context for deeper analysis.

        Returns:
            FactFragilityScore with fragility metrics.
        """
        # Default scores
        verifiability = 0.8
        recharacterization_risk = 0.2
        testimony_dependence = 0.1
        adversary_position = None
        confidence_zone = ConfidenceStratification.DEFENSIBLE

        # Adjust based on source
        if source in ("recorded_lease_text", "county_records", "rrc_p4_form"):
            verifiability = 0.95
            recharacterization_risk = 0.1
            testimony_dependence = 0.0
            confidence_zone = ConfidenceStratification.DEFENSIBLE
        elif source in ("operator_statement", "email_correspondence"):
            verifiability = 0.6
            recharacterization_risk = 0.4
            testimony_dependence = 0.7
            adversary_position = "Operator may later claim different intent or understanding"
            confidence_zone = ConfidenceStratification.AGGRESSIVE
        elif source in ("industry_practice", "expert_opinion"):
            verifiability = 0.5
            recharacterization_risk = 0.6
            testimony_dependence = 0.8
            adversary_position = "Other experts may have differing opinions"
            confidence_zone = ConfidenceStratification.DISCLOSURE
        elif source in ("unrecorded_amendment", "oral_agreement"):
            verifiability = 0.3
            recharacterization_risk = 0.9
            testimony_dependence = 1.0
            adversary_position = "Opposing party may deny existence or terms"
            confidence_zone = ConfidenceStratification.HIGH_RISK

        # Lease-specific adjustments
        if lease and hasattr(lease, "has_preferential_right") and lease.has_preferential_right:
            if "assignment" in fact.lower() or "transfer" in fact.lower():
                recharacterization_risk += 0.2
                adversary_position = "Lessor may claim ROFR was triggered and violated"

        return FactFragilityScore(
            fact_description=fact,
            verifiability=min(verifiability, 1.0),
            recharacterization_risk=min(recharacterization_risk, 1.0),
            testimony_dependence=min(testimony_dependence, 1.0),
            adversary_position=adversary_position,
            confidence_zone=confidence_zone,
        )


# ============================================================================
# TIE-20 COMPONENT: MULTI-DOCTRINE DECOMPOSITION
# ============================================================================


@dataclass
class DoctrineEdge:
    """Edge in the doctrine interaction graph."""
    from_doctrine: str
    to_doctrine: str
    interaction_type: str  # "requires", "conflicts_with", "modifies", "supersedes"
    weight: float = 1.0


class MultiDoctrineDecomposer:
    """Decompose complex lease issues into interacting doctrine networks."""

    def __init__(self):
        """Initialize multi-doctrine decomposer."""
        self._interaction_graph: List[DoctrineEdge] = []
        self._build_lease_interaction_graph()
        logger.info("Multi-doctrine decomposer initialized with interaction graph")

    def _build_lease_interaction_graph(self) -> None:
        """Build the doctrine interaction graph for oil & gas leases."""
        # Habendum interactions
        self._interaction_graph.extend([
            DoctrineEdge("habendum_primary_term", "hbp_status", "requires", 1.0),
            DoctrineEdge("habendum_secondary_term", "production_paying_quantities", "requires", 1.0),
            DoctrineEdge("shut_in_royalty", "hbp_status", "modifies", 0.8),
            DoctrineEdge("force_majeure", "habendum_primary_term", "modifies", 0.7),
            DoctrineEdge("continuous_development", "habendum_primary_term", "modifies", 0.9),
        ])

        # Pugh clause interactions
        self._interaction_graph.extend([
            DoctrineEdge("pugh_vertical", "pooling_authority", "requires", 1.0),
            DoctrineEdge("pugh_horizontal", "depth_limitation", "requires", 0.9),
            DoctrineEdge("pugh_depth", "formation_definition", "requires", 1.0),
            DoctrineEdge("pugh_vertical", "retained_acreage", "modifies", 1.0),
        ])

        # Royalty interactions
        self._interaction_graph.extend([
            DoctrineEdge("royalty_cost_free", "post_production_costs", "conflicts_with", 1.0),
            DoctrineEdge("overriding_royalty", "net_revenue_interest", "modifies", 1.0),
            DoctrineEdge("royalty_suspension", "shut_in_royalty", "modifies", 0.8),
        ])

        # Assignment interactions
        self._interaction_graph.extend([
            DoctrineEdge("preferential_right_to_purchase", "assignment_clause", "requires", 1.0),
            DoctrineEdge("consent_to_assign", "assignment_clause", "modifies", 0.9),
        ])

        # Pooling interactions
        self._interaction_graph.extend([
            DoctrineEdge("pooling_authority", "nri_calculation", "modifies", 1.0),
            DoctrineEdge("pooling_authority", "pugh_vertical", "requires", 0.9),
        ])

    def decompose_issue(
        self,
        issue_description: str,
        primary_category: IssueCategory
    ) -> Dict[str, Any]:
        """Decompose a complex issue into constituent doctrines and their interactions.

        Args:
            issue_description: Natural language description of the issue.
            primary_category: The primary issue category.

        Returns:
            Dictionary with decomposition analysis.
        """
        # Identify relevant doctrines by keyword matching
        keywords_by_category = {
            IssueCategory.TERM_STATUS: ["habendum", "primary term", "hbp", "expiration", "production"],
            IssueCategory.ROYALTY_BURDEN: ["royalty", "orri", "nri", "cost free", "burden"],
            IssueCategory.ACREAGE_RETENTION: ["pugh", "pooling", "retained", "released", "acreage"],
            IssueCategory.DEPTH_RIGHTS: ["depth", "formation", "vertical", "horizontal", "zone"],
            IssueCategory.OPERATIONAL_OBLIGATIONS: ["continuous", "drilling", "offset", "shut-in"],
            IssueCategory.ASSIGNMENT_TRANSFER: ["assignment", "transfer", "rofr", "preferential"],
            IssueCategory.SURFACE_RIGHTS: ["surface", "damage", "restoration", "access"],
            IssueCategory.FORCE_MAJEURE: ["force majeure", "impossibility", "act of god"],
            IssueCategory.TERMINATION: ["surrender", "release", "termination", "cessation"],
            IssueCategory.DISPUTE_RESOLUTION: ["arbitration", "venue", "jurisdiction", "choice of law"],
        }

        keywords = keywords_by_category.get(primary_category, [])
        matched_doctrines = []
        issue_lower = issue_description.lower()

        # Match doctrines from interaction graph
        doctrine_keys = set()
        for edge in self._interaction_graph:
            doctrine_keys.add(edge.from_doctrine)
            doctrine_keys.add(edge.to_doctrine)

        for doctrine_key in doctrine_keys:
            for keyword in keywords:
                if keyword in issue_lower or keyword.replace(" ", "_") in doctrine_key:
                    if doctrine_key not in matched_doctrines:
                        matched_doctrines.append(doctrine_key)

        # Find interactions between matched doctrines
        interactions = []
        for edge in self._interaction_graph:
            if edge.from_doctrine in matched_doctrines and edge.to_doctrine in matched_doctrines:
                interactions.append({
                    "from": edge.from_doctrine,
                    "to": edge.to_doctrine,
                    "type": edge.interaction_type,
                    "weight": edge.weight,
                })

        # Stratify the issue
        strata = self._stratify_issue(issue_description, matched_doctrines)

        return {
            "issue": issue_description,
            "primary_category": primary_category.value,
            "matched_doctrines": matched_doctrines,
            "doctrine_interactions": interactions,
            "issue_strata": strata,
            "complexity_score": round(len(matched_doctrines) * 0.3 + len(interactions) * 0.7, 2),
        }

    def _stratify_issue(self, issue: str, doctrines: List[str]) -> Dict[str, List[str]]:
        """Stratify issue into layers."""
        strata = {
            IssueStratum.THRESHOLD.value: [],
            IssueStratum.QUANTITATIVE.value: [],
            IssueStratum.INTERPRETIVE.value: [],
            IssueStratum.ADVERSARIAL.value: [],
        }

        # Simple keyword-based stratification
        if any(word in issue.lower() for word in ["does", "exists", "present", "included"]):
            strata[IssueStratum.THRESHOLD.value].extend(doctrines[:2])

        if any(word in issue.lower() for word in ["how much", "how many", "acres", "rate", "days"]):
            strata[IssueStratum.QUANTITATIVE.value].extend(doctrines[:3])

        if any(word in issue.lower() for word in ["ambiguous", "unclear", "interpret", "mean"]):
            strata[IssueStratum.INTERPRETIVE.value].extend(doctrines)

        if any(word in issue.lower() for word in ["dispute", "lessor", "lessee", "claim", "argue"]):
            strata[IssueStratum.ADVERSARIAL.value].extend(doctrines)

        return strata


# ============================================================================
# TIE-20 COMPONENT: ZONED ANALYSIS
# ============================================================================


class ZonedAnalysisEngine:
    """Enforce strict separation between PLANNING, REPORTING, and AUDIT analysis zones."""

    def __init__(self):
        """Initialize zoned analysis engine."""
        self._current_zone: Optional[AnalysisZone] = None
        self._zone_stack: List[AnalysisZone] = []
        logger.info("Zoned analysis engine initialized")

    def enter_zone(self, zone: AnalysisZone) -> None:
        """Enter an analysis zone."""
        if self._current_zone:
            self._zone_stack.append(self._current_zone)
        self._current_zone = zone
        logger.debug(f"Entered {zone.value} analysis zone")

    def exit_zone(self) -> None:
        """Exit the current analysis zone."""
        if self._zone_stack:
            self._current_zone = self._zone_stack.pop()
        else:
            self._current_zone = None
        logger.debug(f"Exited analysis zone, now in {self._current_zone.value if self._current_zone else 'none'}")

    def assert_zone(self, required_zone: AnalysisZone) -> None:
        """Assert that we're in the required zone (raise error if not)."""
        if self._current_zone != required_zone:
            raise ValueError(
                f"Analysis zone violation: required {required_zone.value}, "
                f"currently in {self._current_zone.value if self._current_zone else 'none'}"
            )

    def get_zone_guidance(self, zone: AnalysisZone) -> str:
        """Get guidance text for a specific analysis zone."""
        guidance = {
            AnalysisZone.PLANNING: (
                "PLANNING ZONE: Strategic lease acquisition. Focus on upside potential, "
                "competitive positioning, acreage value. Aggressive interpretations acceptable. "
                "Risk disclosure NOT required unless material to investment decision."
            ),
            AnalysisZone.REPORTING: (
                "REPORTING ZONE: Asset reporting, reserves booking, investor disclosure. "
                "Use DEFENSIBLE interpretations only. Material risks MUST be disclosed. "
                "Follow SEC guidance for proved reserves. Be conservative."
            ),
            AnalysisZone.AUDIT: (
                "AUDIT ZONE: Compliance verification, title opinion defense, audit response. "
                "Cite statutes and case law. Document all assumptions. Flag all ambiguities. "
                "Adversarial posture — assume hostile examiner."
            ),
        }
        return guidance.get(zone, "No specific guidance for this zone.")


# ============================================================================
# TIE-20 COMPONENT: DEEP ANALYSIS MODE (VECTOR SEARCH INTEGRATION)
# ============================================================================


class DeepAnalysisEngine:
    """Multi-source synthesis for deep analysis queries using cloud knowledge and doctrine cache."""

    def __init__(self, cloud_retriever_available: bool = False):
        """Initialize deep analysis engine."""
        self._cloud_available = cloud_retriever_available
        logger.info(f"Deep analysis engine initialized (cloud available: {cloud_retriever_available})")

    async def deep_analyze(
        self,
        query: str,
        lease_context: Optional[Dict[str, Any]] = None,
        response_mode: ResponseMode = ResponseMode.DEEP,
    ) -> Dict[str, Any]:
        """Perform deep multi-source analysis.

        Args:
            query: The analysis query.
            lease_context: Optional lease context dictionary.
            response_mode: Response depth mode.

        Returns:
            Dictionary with deep analysis results.
        """
        start_time = time.monotonic()
        sources_used = []

        # Layer 1: Doctrine cache
        doctrine_matches = match_doctrine(query, top_k=5)
        doctrine_analysis = {
            "source": "doctrine_cache",
            "matches": len(doctrine_matches),
            "top_doctrines": [
                {"key": key, "score": score, "title": block.title}
                for key, score, block in doctrine_matches[:3]
            ],
        }
        sources_used.append("doctrine_cache")

        # Layer 2: Cloud knowledge (if available)
        cloud_analysis = {}
        if self._cloud_available:
            try:
                from cloud_retriever import retrieve_cloud_knowledge
                cloud = await retrieve_cloud_knowledge(query, category="lease_analysis")
                cloud_analysis = {
                    "source": "cognition_cloud",
                    "records": cloud.total_records,
                    "context_summary": cloud.merged_text(1000),
                    "sources_succeeded": cloud.sources_succeeded,
                    "retrieval_time_ms": cloud.retrieval_time_ms,
                }
                sources_used.append("cognition_cloud")
            except Exception as e:
                logger.warning(f"Cloud retrieval failed in deep analysis: {e}")
                cloud_analysis = {"error": str(e)}

        # Layer 3: Lease-specific context
        lease_specific = {}
        if lease_context:
            lease_specific = {
                "source": "lease_record",
                "lease_id": lease_context.get("lease_id"),
                "county": lease_context.get("county"),
                "status": lease_context.get("current_status"),
                "has_pugh": lease_context.get("has_pugh_clause", False),
                "royalty_rate": lease_context.get("royalty_rate"),
            }
            sources_used.append("lease_record")

        # Synthesize reasoning chain
        reasoning_chain = self._synthesize_reasoning(
            query, doctrine_matches, cloud_analysis, lease_specific
        )

        elapsed_ms = (time.monotonic() - start_time) * 1000

        return {
            "query": query,
            "mode": response_mode.value,
            "sources_used": sources_used,
            "doctrine_analysis": doctrine_analysis,
            "cloud_analysis": cloud_analysis,
            "lease_specific_analysis": lease_specific,
            "reasoning_chain": reasoning_chain,
            "synthesis_confidence": self._compute_synthesis_confidence(sources_used),
            "processing_time_ms": round(elapsed_ms, 2),
        }

    def _synthesize_reasoning(
        self,
        query: str,
        doctrine_matches: List[Tuple[str, float, Any]],
        cloud_analysis: Dict[str, Any],
        lease_specific: Dict[str, Any],
    ) -> List[str]:
        """Synthesize a reasoning chain from multiple sources."""
        chain = []

        # Step 1: Doctrine foundation
        if doctrine_matches:
            top_doctrine = doctrine_matches[0]
            chain.append(
                f"1. Doctrine Foundation: {top_doctrine[2].title} ({top_doctrine[0]}) "
                f"provides the legal framework."
            )

        # Step 2: Cloud context
        if "context_summary" in cloud_analysis:
            summary = cloud_analysis["context_summary"][:150]
            chain.append(
                f"2. Industry Context: Cloud knowledge retrieval found {cloud_analysis.get('records', 0)} "
                f"relevant records. Key insight: {summary}..."
            )

        # Step 3: Lease-specific application
        if lease_specific:
            chain.append(
                f"3. Lease Application: For lease {lease_specific.get('lease_id', 'unknown')} in "
                f"{lease_specific.get('county', 'unknown')} County, current status: "
                f"{lease_specific.get('status', 'unknown')}."
            )

        # Step 4: Conclusion
        chain.append(
            "4. Conclusion: Multi-source synthesis complete. Confidence weighted by "
            "authority hierarchy and source reliability."
        )

        return chain

    def _compute_synthesis_confidence(self, sources: List[str]) -> float:
        """Compute confidence score based on sources used."""
        base = 0.5
        if "doctrine_cache" in sources:
            base += 0.2
        if "cognition_cloud" in sources:
            base += 0.15
        if "lease_record" in sources:
            base += 0.15
        return min(base, 1.0)


# ============================================================================
# LEASE ANALYSIS ENGINE CORE
# ============================================================================


class LM02LeaseAnalysisEngine:
    """Core lease analysis engine with multi-layer architecture.

    Layer 1: Doctrine Cache - instant answers from pre-compiled reasoning blocks
    Layer 2: Semantic Retrieval - term normalization, legal desc parsing
    Layer 3: Deep Analysis - multi-clause synthesis, NRI calc, comparison
    """

    def __init__(self) -> None:
        """Initialize the engine with all subsystems."""
        self._search_index = get_search_index()
        self._telemetry = get_telemetry()
        self._lease_store: Dict[str, LeaseRecord] = {}
        self._start_time = time.time()

        # TIE-20 Component Initialization
        self._authority_engine = AuthorityHardeningEngine()
        self._drift_watcher = DriftWatcher()
        self._coverage_tracker = CoverageTracker(total_doctrines=len(DOCTRINE_CACHE))
        self._fragility_analyzer = FactFragilityAnalyzer()
        self._doctrine_decomposer = MultiDoctrineDecomposer()
        self._zoned_analysis = ZonedAnalysisEngine()
        self._deep_analysis = DeepAnalysisEngine(cloud_retriever_available=_CLOUD_AVAILABLE)

        # Load authority sources for key lease topics
        self._load_authority_sources()

        logger.info(
            f"LM02 Lease Analysis Engine v{ENGINE_VERSION} initialized. "
            f"Doctrines: {len(DOCTRINE_CACHE)}, "
            f"Index entries: {self._search_index.total_entries}, "
            f"TIE-20 components: ACTIVE"
        )

    def _load_authority_sources(self) -> None:
        """Load authority sources for common lease topics."""
        # Habendum clause authorities
        self._authority_engine.add_authority(
            "habendum_primary_term",
            AuthoritySource(
                citation="TX NAT. RES. CODE § 91.001",
                authority_level=AuthorityLevel.STATUTORY,
                weight=0.95,
                summary="Statutory recognition of habendum clause in Texas oil and gas leases",
                url="https://statutes.capitol.texas.gov/Docs/NR/htm/NR.91.htm"
            )
        )
        self._authority_engine.add_authority(
            "hbp_status",
            AuthoritySource(
                citation="Clifton v. Koontz, 160 Tex. 82, 325 S.W.2d 684 (1959)",
                authority_level=AuthorityLevel.CASE_LAW,
                weight=0.80,
                summary="Production in paying quantities standard for HBP determination",
            )
        )

        # Pugh clause authorities
        self._authority_engine.add_authority(
            "pugh_vertical",
            AuthoritySource(
                citation="Endeavor Energy Resources, L.P. v. Discovery Operating, Inc., 554 S.W.3d 586 (Tex. 2018)",
                authority_level=AuthorityLevel.CASE_LAW,
                weight=0.80,
                summary="Pugh clause interpretation and retained acreage calculation",
            )
        )
        self._authority_engine.add_authority(
            "pugh_horizontal",
            AuthoritySource(
                citation="Industry practice - horizontal Pugh clause",
                authority_level=AuthorityLevel.INDUSTRY_STANDARD,
                weight=0.60,
                summary="Horizontal Pugh releases acreage outside producing unit laterals",
            )
        )

        # Royalty authorities
        self._authority_engine.add_authority(
            "royalty_cost_free",
            AuthoritySource(
                citation="Heritage Resources, Inc. v. NationsBank, 939 S.W.2d 118 (Tex. 1996)",
                authority_level=AuthorityLevel.CASE_LAW,
                weight=0.80,
                summary="Cost-free royalty interpretation, post-production cost allocation",
            )
        )
        self._authority_engine.add_authority(
            "shut_in_royalty",
            AuthoritySource(
                citation="TX NAT. RES. CODE § 91.402",
                authority_level=AuthorityLevel.STATUTORY,
                weight=0.95,
                summary="Shut-in royalty payment requirements for gas wells",
            )
        )

        # Pooling authorities
        self._authority_engine.add_authority(
            "pooling_authority",
            AuthoritySource(
                citation="TX NAT. RES. CODE § 85.201-85.206",
                authority_level=AuthorityLevel.STATUTORY,
                weight=0.95,
                summary="Voluntary pooling provisions in Texas",
            )
        )

        # Assignment authorities
        self._authority_engine.add_authority(
            "preferential_right_to_purchase",
            AuthoritySource(
                citation="Texas common law - ROFR enforceability",
                authority_level=AuthorityLevel.CASE_LAW,
                weight=0.75,
                summary="Right of first refusal is enforceable property right",
            )
        )

        logger.info(f"Loaded {len(self._authority_engine._authority_index)} authority topics")

    # ────────────────────────────────────────────────────────────────────
    # LEASE MANAGEMENT
    # ────────────────────────────────────────────────────────────────────

    def add_lease(self, lease: LeaseRecord) -> str:
        """Add or update a lease record in the engine.

        Args:
            lease: The lease record to add.

        Returns:
            The lease ID.
        """
        # Auto-compute primary term expiration if not set
        if lease.primary_term_expiration is None and lease.lease_date and lease.primary_term_years:
            try:
                exp_year = lease.lease_date.year + lease.primary_term_years
                lease.primary_term_expiration = lease.lease_date.replace(year=exp_year)
            except ValueError:
                # Handle Feb 29 -> non-leap year
                lease.primary_term_expiration = lease.lease_date.replace(
                    year=lease.lease_date.year + lease.primary_term_years,
                    day=28,
                )

        # Parse legal description if raw text provided
        if lease.legal_description_text and not lease.parsed_legal:
            parsed = parse_legal_description(lease.legal_description_text)
            lease.parsed_legal = parsed.to_dict()
            if parsed.county and not lease.county:
                lease.county = parsed.county
            if parsed.acres and not lease.acres:
                lease.acres = parsed.acres

        # Parse royalty if fraction provided but no decimal
        if lease.royalty_fraction and not lease.royalty_rate:
            parsed_frac = parse_royalty_fraction(lease.royalty_fraction)
            if parsed_frac.is_valid:
                lease.royalty_rate = parsed_frac.decimal_value

        # Determine current status
        if lease.current_status == "unknown":
            lease.current_status = self._determine_lease_status(lease)

        # Update timestamp
        lease.updated_at = datetime.now(timezone.utc).isoformat()

        # Store in memory
        self._lease_store[lease.lease_id] = lease

        # Index for search
        self._index_lease(lease)

        # Audit
        self._telemetry.record_audit(
            mutation_type=MutationType.LEASE_ADDED,
            mutation_origin=MutationOrigin.API_CALL,
            entity_type="lease",
            entity_id=lease.lease_id,
            description=f"Added lease: {lease.lessor.name if lease.lessor else 'unknown'} to "
                        f"{lease.lessee.name if lease.lessee else 'unknown'}, "
                        f"{lease.county or 'unknown'} County",
        )

        logger.info(f"Lease {lease.lease_id} added/updated in engine")
        return lease.lease_id

    def get_lease(self, lease_id: str) -> Optional[LeaseRecord]:
        """Retrieve a lease by ID."""
        return self._lease_store.get(lease_id)

    def remove_lease(self, lease_id: str) -> bool:
        """Remove a lease from the engine."""
        if lease_id in self._lease_store:
            del self._lease_store[lease_id]
            self._search_index.remove_entry(lease_id)
            self._telemetry.record_audit(
                mutation_type=MutationType.LEASE_DELETED,
                mutation_origin=MutationOrigin.API_CALL,
                entity_type="lease",
                entity_id=lease_id,
                description=f"Removed lease {lease_id}",
            )
            return True
        return False

    def _index_lease(self, lease: LeaseRecord) -> None:
        """Index a lease record for search."""
        parsed = lease.parsed_legal or {}
        entry = LeaseIndexEntry(
            lease_id=lease.lease_id,
            lessor_name=lease.lessor.name if lease.lessor else "",
            lessee_name=lease.lessee.name if lease.lessee else "",
            operator_name=lease.lessee.name if lease.lessee else "",
            lease_date=lease.lease_date,
            recording_date=lease.recording_date,
            expiration_date=lease.primary_term_expiration,
            status=LeaseStatus(lease.current_status) if lease.current_status in [s.value for s in LeaseStatus] else LeaseStatus.UNKNOWN,
            county=lease.county or "",
            legal_description=lease.legal_description_text or "",
            section=parsed.get("section", "") or "",
            block=parsed.get("block", "") or "",
            survey=parsed.get("survey_name", "") or "",
            abstract_number=parsed.get("abstract_number", "") or "",
            acres=lease.acres,
            royalty_rate=lease.royalty_rate,
            royalty_fraction=lease.royalty_fraction or "",
            primary_term_years=lease.primary_term_years,
            has_pugh_clause=lease.has_pugh_clause,
            has_depth_limitation=lease.has_depth_limitation,
            has_continuous_development=lease.has_continuous_development,
            document_number=lease.document_number or "",
            volume=lease.volume or "",
            page=lease.page or "",
            instrument_type=lease.instrument_type,
            formations=lease.target_formations,
            source=lease.source,
        )
        self._search_index.add_entry(entry)

    def _determine_lease_status(self, lease: LeaseRecord) -> str:
        """Determine the current status of a lease."""
        today = date.today()

        if lease.held_by_production:
            return LeaseStatus.HELD_BY_PRODUCTION.value

        if lease.primary_term_expiration:
            days_until = (lease.primary_term_expiration - today).days
            if days_until < 0:
                if lease.producing_wells:
                    return LeaseStatus.HELD_BY_PRODUCTION.value
                return LeaseStatus.EXPIRED.value
            elif days_until <= 30:
                return LeaseStatus.PENDING_EXPIRATION.value
            else:
                return LeaseStatus.ACTIVE_PRIMARY.value

        if lease.lease_date and lease.primary_term_years:
            try:
                exp = lease.lease_date.replace(year=lease.lease_date.year + lease.primary_term_years)
                days_until = (exp - today).days
                if days_until < 0:
                    return LeaseStatus.EXPIRED.value
                elif days_until <= 30:
                    return LeaseStatus.PENDING_EXPIRATION.value
                return LeaseStatus.ACTIVE_PRIMARY.value
            except ValueError:
                pass

        return LeaseStatus.UNKNOWN.value

    # ────────────────────────────────────────────────────────────────────
    # LEASE ANALYSIS
    # ────────────────────────────────────────────────────────────────────

    def analyze_lease(self, request: LeaseAnalysisRequest) -> LeaseAnalysisResponse:
        """Perform comprehensive lease analysis.

        Args:
            request: The analysis request with lease data and parameters.

        Returns:
            LeaseAnalysisResponse with full analysis results.
        """
        trace_id = trace_query(
            QueryType.LEASE_ANALYSIS,
            input_summary=f"type={request.analysis_type}, mode={request.response_mode.value}",
        )
        start_time = time.monotonic()

        try:
            # Resolve lease record
            lease = self._resolve_lease(request)
            if lease is None:
                fail_trace(trace_id, "No lease data provided", ErrorDomain.VALIDATION)
                raise HTTPException(status_code=400, detail="Provide a lease record, lease_id, or lease_text")

            # Build response
            response = LeaseAnalysisResponse(
                lease_id=lease.lease_id,
                analysis_type=request.analysis_type,
                response_mode=request.response_mode.value,
                lease=lease,
                trace_id=trace_id,
            )

            # Run analysis based on type
            if request.analysis_type in ("full", "term"):
                response.term_analysis = self._analyze_term(lease, request.response_mode)

            if request.analysis_type in ("full", "royalty"):
                response.royalty_calculation = self._calculate_royalty(lease)

            if request.analysis_type in ("full", "pugh"):
                response.pugh_analysis = self._analyze_pugh(lease)

            if request.analysis_type in ("full", "clause"):
                response.identified_clauses = self._identify_clauses(lease)

            if request.analysis_type in ("full", "expiration"):
                response.expiration_alerts = self._check_expiration(lease)

            # Risk summary
            if request.include_risk_assessment:
                response.risk_summary = self._compute_risk_summary(
                    lease, response.term_analysis, response.pugh_analysis
                )

            # Doctrine references
            if request.include_doctrine:
                response.doctrine_references = self._gather_doctrine_references(
                    request.analysis_type, lease
                )

            # Recommendations
            response.recommendations = self._generate_recommendations(lease, response)

            # Determinism hash
            elapsed = (time.monotonic() - start_time) * 1000
            response.processing_time_ms = round(elapsed, 2)
            hash_content = json.dumps({
                "lease_id": lease.lease_id,
                "analysis_type": request.analysis_type,
                "timestamp": response.timestamp,
            }, sort_keys=True)
            response.determinism_hash = hashlib.sha256(hash_content.encode()).hexdigest()

            complete_trace(trace_id, ResponseLayer.DEEP_ANALYSIS, f"analysis complete in {elapsed:.0f}ms")
            return response

        except HTTPException:
            raise
        except Exception as e:
            fail_trace(trace_id, str(e), ErrorDomain.CALCULATION, ErrorSeverity.HIGH)
            logger.error(f"Lease analysis failed: {e}\n{traceback.format_exc()}")
            raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

    def _resolve_lease(self, request: LeaseAnalysisRequest) -> Optional[LeaseRecord]:
        """Resolve the lease record from the request."""
        if request.lease:
            self.add_lease(request.lease)
            return request.lease
        if request.lease_id:
            return self._lease_store.get(request.lease_id)
        if request.lease_text:
            return self._parse_lease_text(request.lease_text)
        return None

    def _parse_lease_text(self, text: str) -> LeaseRecord:
        """Parse raw lease text into a LeaseRecord.

        This extracts clause types, legal description, parties, and terms
        from unstructured lease text.
        """
        trace_id = trace_query(QueryType.LEASE_ANALYSIS, input_summary=f"parsing {len(text)} chars of lease text")

        lease = LeaseRecord(source="parsed_text")

        # Identify clause types
        clauses_found = identify_clause_types(text)
        for clause_type, confidence, matched in clauses_found:
            if confidence > 0.3:
                lease.clauses.append(LeaseClauseInfo(
                    clause_type=clause_type.value,
                    summary=f"Identified with {confidence:.0%} confidence",
                    risk_level="moderate",
                    notes=[f"Matched indicators: {', '.join(matched)}"],
                ))

                # Set clause flags based on identified types
                if clause_type == LeaseClauseType.PUGH:
                    lease.has_pugh_clause = True
                elif clause_type == LeaseClauseType.DEPTH_LIMITATION:
                    lease.has_depth_limitation = True
                elif clause_type == LeaseClauseType.CONTINUOUS_DEVELOPMENT:
                    lease.has_continuous_development = True
                elif clause_type == LeaseClauseType.FORCE_MAJEURE:
                    lease.has_force_majeure = True
                elif clause_type == LeaseClauseType.SHUT_IN:
                    lease.has_shut_in = True
                elif clause_type == LeaseClauseType.POOLING:
                    lease.has_pooling = True
                elif clause_type == LeaseClauseType.SURFACE_USE:
                    lease.has_surface_restrictions = True
                elif clause_type == LeaseClauseType.MOTHER_HUBBARD:
                    lease.has_mother_hubbard = True
                elif clause_type == LeaseClauseType.PREFERENTIAL_RIGHT:
                    lease.has_preferential_right = True
                elif clause_type == LeaseClauseType.SURRENDER:
                    lease.has_surrender_clause = True

        # Try to parse legal description from the text
        legal = parse_legal_description(text)
        if legal.confidence > 0.2:
            lease.legal_description_text = text[:500]
            lease.parsed_legal = legal.to_dict()
            if legal.county:
                lease.county = legal.county
            if legal.acres:
                lease.acres = legal.acres

        # Try to find royalty fraction
        import re
        royalty_match = re.search(r"royalty\s+(?:of\s+)?(\d+/\d+)", text, re.IGNORECASE)
        if royalty_match:
            parsed_frac = parse_royalty_fraction(royalty_match.group(1))
            if parsed_frac.is_valid:
                lease.royalty_fraction = parsed_frac.fraction_str
                lease.royalty_rate = parsed_frac.decimal_value

        # Try to find primary term
        term_match = re.search(r"(?:term\s+of|for)\s+(\d+)\s+years", text, re.IGNORECASE)
        if term_match:
            lease.primary_term_years = int(term_match.group(1))

        self.add_lease(lease)
        complete_trace(trace_id, ResponseLayer.SEMANTIC_RETRIEVAL, f"parsed lease with {len(clauses_found)} clauses identified")
        return lease

    # ────────────────────────────────────────────────────────────────────
    # TERM ANALYSIS
    # ────────────────────────────────────────────────────────────────────

    def _analyze_term(self, lease: LeaseRecord, mode: ResponseMode) -> TermAnalysis:
        """Analyze the current term status of a lease."""
        trace_id = trace_query(QueryType.TERM_ANALYSIS, input_summary=f"lease={lease.lease_id}")
        today = date.today()

        analysis = TermAnalysis(
            current_term="unknown",
            primary_term_start=lease.lease_date or lease.effective_date,
            primary_term_years=lease.primary_term_years,
        )

        # Calculate primary term end
        start_date = lease.effective_date or lease.lease_date
        if start_date and lease.primary_term_years:
            try:
                analysis.primary_term_end = start_date.replace(year=start_date.year + lease.primary_term_years)
            except ValueError:
                analysis.primary_term_end = start_date.replace(
                    year=start_date.year + lease.primary_term_years, day=28
                )
            lease.primary_term_expiration = analysis.primary_term_end

        # Determine current term
        if lease.held_by_production or lease.producing_wells:
            analysis.current_term = "secondary_hbp"
            analysis.is_hbp = True
            analysis.risk_level = "low"
            analysis.analysis_notes.append("Lease is held by production in the secondary term.")
            analysis.saving_clauses.append("Production in paying quantities")
        elif analysis.primary_term_end:
            days_remaining = (analysis.primary_term_end - today).days
            analysis.days_remaining_primary = days_remaining
            analysis.expiration_date = analysis.primary_term_end
            analysis.days_until_expiration = days_remaining

            if days_remaining < 0:
                analysis.current_term = "expired"
                analysis.is_expired = True
                analysis.risk_level = "critical"
                analysis.analysis_notes.append(
                    f"Primary term expired {abs(days_remaining)} days ago on {analysis.primary_term_end}."
                )
            elif days_remaining <= 30:
                analysis.current_term = "primary_expiring"
                analysis.risk_level = "critical"
                analysis.analysis_notes.append(
                    f"CRITICAL: Primary term expires in {days_remaining} days on {analysis.primary_term_end}."
                )
            elif days_remaining <= 90:
                analysis.current_term = "primary_warning"
                analysis.risk_level = "high"
                analysis.analysis_notes.append(
                    f"WARNING: Primary term expires in {days_remaining} days on {analysis.primary_term_end}."
                )
            elif days_remaining <= 365:
                analysis.current_term = "primary_active"
                analysis.risk_level = "moderate"
                analysis.analysis_notes.append(
                    f"Primary term active. {days_remaining} days remaining until {analysis.primary_term_end}."
                )
            else:
                analysis.current_term = "primary_active"
                analysis.risk_level = "low"
                analysis.analysis_notes.append(
                    f"Primary term active with {days_remaining} days remaining."
                )
        else:
            analysis.current_term = "unknown"
            analysis.risk_level = "high"
            analysis.analysis_notes.append(
                "Cannot determine term status — missing lease date or primary term duration."
            )

        # Identify saving clauses
        if lease.has_shut_in:
            analysis.saving_clauses.append("Shut-in royalty clause")
        if lease.has_force_majeure:
            analysis.saving_clauses.append("Force majeure clause")
        if lease.has_continuous_development:
            analysis.saving_clauses.append("Continuous development clause")
        if lease.paid_up:
            analysis.analysis_notes.append("Paid-up lease — no annual delay rental obligation.")

        # Doctrine references
        if mode in (ResponseMode.STANDARD, ResponseMode.DEEP):
            analysis.doctrine_references = ["habendum_primary_term", "habendum_secondary_term", "hbp_status"]
            if lease.has_shut_in:
                analysis.doctrine_references.append("shut_in_royalty")
            if lease.has_force_majeure:
                analysis.doctrine_references.append("force_majeure")

        complete_trace(trace_id, ResponseLayer.COMPUTED, f"term={analysis.current_term}, risk={analysis.risk_level}")
        return analysis

    # ────────────────────────────────────────────────────────────────────
    # ROYALTY CALCULATION
    # ────────────────────────────────────────────────────────────────────

    def _calculate_royalty(self, lease: LeaseRecord) -> RoyaltyCalculation:
        """Calculate royalty and NRI for a lease."""
        trace_id = trace_query(QueryType.ROYALTY_CALCULATION, input_summary=f"lease={lease.lease_id}")

        royalty_fraction = lease.royalty_fraction or "1/4"
        royalty_decimal = lease.royalty_rate or 0.25

        steps: List[str] = []
        warnings: List[str] = []

        # Step 1: Gross royalty
        steps.append(f"1. Royalty fraction: {royalty_fraction} = {royalty_decimal:.6f}")

        # Step 2: Working interest
        wi = 1.0 - royalty_decimal
        steps.append(f"2. Working interest: 1.0 - {royalty_decimal:.6f} = {wi:.6f}")

        # Step 3: Overriding royalties (none stored on lease record, but support)
        total_orri = 0.0
        orri_list: List[Dict[str, Any]] = []
        steps.append(f"3. Overriding royalties: {total_orri:.6f} (none recorded)")

        # Step 4: Total burden
        total_burden = royalty_decimal + total_orri
        steps.append(f"4. Total burden: {royalty_decimal:.6f} + {total_orri:.6f} = {total_burden:.6f}")

        # Step 5: NRI
        nri = wi - total_orri
        steps.append(f"5. Net Revenue Interest: {wi:.6f} - {total_orri:.6f} = {nri:.6f}")

        # Step 6: Pooling adjustment
        pooled_nri = None
        pooling_factor = None
        if lease.acres and lease.pooling_max_acres_oil:
            pooling_factor = lease.acres / lease.pooling_max_acres_oil
            if pooling_factor > 1.0:
                pooling_factor = 1.0
                warnings.append("Lease acres exceed pooling max — capped at 1.0")
            pooled_nri = nri * pooling_factor
            steps.append(
                f"6. Pooling factor: {lease.acres:.2f} / {lease.pooling_max_acres_oil:.2f} = {pooling_factor:.6f}"
            )
            steps.append(f"   Pooled NRI: {nri:.6f} x {pooling_factor:.6f} = {pooled_nri:.6f}")
        else:
            steps.append("6. No pooling adjustment (no unit acreage data)")

        # Step 7: Severance tax
        tx_config = ENGINE_CONFIG.get("nri_calculation", {}).get("texas_severance_tax", {})
        sev_tax = tx_config.get("oil_rate", 0.046)
        steps.append(f"7. Texas severance tax rate: {sev_tax:.4f} (oil)")

        if total_burden > 0.99:
            warnings.append(f"CRITICAL: Total burden ({total_burden:.6f}) approaches or exceeds 100%")

        calc = RoyaltyCalculation(
            royalty_fraction=royalty_fraction,
            royalty_decimal=royalty_decimal,
            gross_royalty_factor=royalty_decimal,
            net_royalty_factor=royalty_decimal,
            overriding_royalties=orri_list,
            total_burden=total_burden,
            working_interest=wi,
            net_revenue_interest=nri,
            pooling_factor=pooling_factor,
            pooled_nri=pooled_nri,
            severance_tax_rate=sev_tax,
            calculation_steps=steps,
            warnings=warnings,
        )

        complete_trace(trace_id, ResponseLayer.COMPUTED, f"NRI={nri:.6f}")
        return calc

    # ────────────────────────────────────────────────────────────────────
    # PUGH CLAUSE ANALYSIS
    # ────────────────────────────────────────────────────────────────────

    def _analyze_pugh(self, lease: LeaseRecord) -> PughClauseAnalysis:
        """Analyze the impact of Pugh clause on the lease."""
        trace_id = trace_query(QueryType.PUGH_ANALYSIS, input_summary=f"lease={lease.lease_id}")

        analysis = PughClauseAnalysis(
            has_pugh=lease.has_pugh_clause,
            pugh_type=lease.pugh_type,
            total_lease_acres=lease.acres,
        )

        if not lease.has_pugh_clause:
            analysis.impact_assessment = (
                "No Pugh clause present. Production from any pooled unit will hold the entire lease, "
                "including all non-pooled acreage and all depths. This favors the lessee."
            )
            analysis.risk_level = "high" if lease.acres and lease.acres > 160 else "moderate"
            analysis.recommendations = [
                "Consider requesting Pugh clause in any lease amendment or renewal",
                "Monitor pooling declarations to ensure lease is not held by minimal production",
                "If negotiating new lease, include combined vertical and horizontal Pugh clause",
            ]
            analysis.doctrine_references = ["pugh_vertical", "pugh_horizontal", "pugh_depth"]
            complete_trace(trace_id, ResponseLayer.DOCTRINE_CACHE, "no Pugh clause")
            return analysis

        # Pugh clause present — analyze impact
        if lease.primary_term_expiration:
            today = date.today()
            analysis.trigger_date = lease.primary_term_expiration
            analysis.days_until_trigger = (lease.primary_term_expiration - today).days

        # Estimate acreage impact
        if lease.acres and lease.pooling_max_acres_oil:
            pooled = min(lease.pooling_max_acres_oil, lease.acres)
            analysis.pooled_acres = pooled
            analysis.retained_acres = pooled
            analysis.released_acres = max(0, lease.acres - pooled)
            analysis.retained_percentage = round((pooled / lease.acres) * 100, 2)
            analysis.released_percentage = round((analysis.released_acres / lease.acres) * 100, 2)
        elif lease.acres:
            # Estimate based on typical unit sizes
            est_unit = 640.0  # Typical horizontal well unit
            pooled = min(est_unit, lease.acres)
            analysis.pooled_acres = pooled
            analysis.retained_acres = pooled
            analysis.released_acres = max(0, lease.acres - pooled)
            analysis.retained_percentage = round((pooled / lease.acres) * 100, 2)
            analysis.released_percentage = round((analysis.released_acres / lease.acres) * 100, 2)

        # Depth analysis for horizontal Pugh
        if lease.pugh_type in ("horizontal", "depth", "combined"):
            if lease.target_formations:
                analysis.formations_retained = lease.target_formations
            analysis.depth_retained = lease.depth_limitation_text or "Producing zone(s) only"
            analysis.depth_released = "All depths below producing zone(s)"

        # Impact assessment
        if analysis.released_percentage and analysis.released_percentage > 50:
            analysis.risk_level = "high"
            analysis.impact_assessment = (
                f"Pugh clause will release {analysis.released_percentage:.1f}% of lease acreage "
                f"({analysis.released_acres:.1f} of {lease.acres:.1f} acres) at the end of the "
                f"primary term. This is a significant acreage release that creates re-leasing opportunity."
            )
        elif analysis.released_percentage and analysis.released_percentage > 20:
            analysis.risk_level = "moderate"
            analysis.impact_assessment = (
                f"Pugh clause will release {analysis.released_percentage:.1f}% of lease acreage "
                f"({analysis.released_acres:.1f} acres). Moderate impact — some acreage available "
                f"for new lease."
            )
        else:
            analysis.risk_level = "low"
            analysis.impact_assessment = (
                f"Pugh clause releases minimal acreage ({analysis.released_percentage or 0:.1f}%). "
                "Most of the lease is within the producing unit."
            )

        # Recommendations
        if analysis.days_until_trigger is not None and 0 < analysis.days_until_trigger <= 180:
            analysis.recommendations.append(
                f"Pugh clause triggers in {analysis.days_until_trigger} days — review acreage "
                f"retention strategy immediately"
            )
        if analysis.released_acres and analysis.released_acres > 0:
            analysis.recommendations.append(
                "Identify released acreage on a plat and evaluate for new lease or top lease"
            )
            analysis.recommendations.append(
                "Check for continuous development obligation on released acreage"
            )
        if lease.pugh_type == "vertical" and not lease.has_depth_limitation:
            analysis.recommendations.append(
                "Vertical Pugh only releases surface acreage — consider depth Pugh to release deeper zones"
            )

        analysis.doctrine_references = ["pugh_vertical", "pugh_horizontal", "pugh_depth", "retained_acreage"]

        complete_trace(
            trace_id, ResponseLayer.COMPUTED,
            f"pugh_type={lease.pugh_type}, released={analysis.released_percentage or 0:.1f}%"
        )
        return analysis

    # ────────────────────────────────────────────────────────────────────
    # CLAUSE IDENTIFICATION
    # ────────────────────────────────────────────────────────────────────

    def _identify_clauses(self, lease: LeaseRecord) -> List[LeaseClauseInfo]:
        """Identify and assess all clauses in a lease."""
        trace_id = trace_query(QueryType.CLAUSE_IDENTIFICATION, input_summary=f"lease={lease.lease_id}")

        clauses: List[LeaseClauseInfo] = []

        # Check each clause flag and generate info
        clause_checks = [
            (lease.has_pugh_clause, "pugh_clause", "Pugh Clause", self._assess_pugh_risk(lease)),
            (lease.has_depth_limitation, "depth_limitation", "Depth Limitation", ("moderate", ["Review depth boundary for formation accuracy"])),
            (lease.has_continuous_development, "continuous_development", "Continuous Development",
             ("high" if lease.continuous_dev_gap_days and lease.continuous_dev_gap_days < 120 else "moderate",
              [f"Gap period: {lease.continuous_dev_gap_days or 'unspecified'} days"])),
            (lease.has_force_majeure, "force_majeure", "Force Majeure", ("low", ["Standard provision"])),
            (lease.has_shut_in, "shut_in", "Shut-In Royalty",
             ("moderate" if lease.shut_in_max_months and lease.shut_in_max_months > 24 else "low",
              [f"Max shut-in: {lease.shut_in_max_months or 'unspecified'} months"])),
            (lease.has_pooling, "pooling", "Pooling Authority",
             ("high" if not lease.has_pugh_clause else "moderate",
              [f"Oil max: {lease.pooling_max_acres_oil or 'unspecified'} ac, Gas max: {lease.pooling_max_acres_gas or 'unspecified'} ac"])),
            (lease.has_surface_restrictions, "surface_use", "Surface Use Restrictions", ("low", ["Lease contains surface restrictions"])),
            (lease.has_mother_hubbard, "mother_hubbard", "Mother Hubbard Clause", ("low", ["Covers adjacent strips and gores"])),
            (lease.has_preferential_right, "preferential_right", "Preferential Right / ROFR",
             ("high", ["Must be honored in any assignment or sale"])),
            (lease.has_surrender_clause, "surrender", "Surrender Clause", ("low", ["Lessee right to release"])),
            (lease.paid_up, "paid_up", "Paid-Up Lease", ("low", ["No annual delay rental obligation"])),
        ]

        for present, clause_type, title, (risk, notes) in clause_checks:
            if present:
                clauses.append(LeaseClauseInfo(
                    clause_type=clause_type,
                    summary=title,
                    risk_level=risk,
                    notes=notes,
                ))

        # Always include habendum and royalty
        clauses.insert(0, LeaseClauseInfo(
            clause_type="habendum",
            summary=f"Habendum: {lease.primary_term_years or '?'} year primary term",
            risk_level=self._assess_term_risk(lease),
            notes=[f"Status: {lease.current_status}"],
        ))
        clauses.insert(1, LeaseClauseInfo(
            clause_type="royalty",
            summary=f"Royalty: {lease.royalty_fraction or lease.royalty_rate or 'unspecified'}",
            risk_level="low" if lease.royalty_rate and lease.royalty_rate >= 0.25 else "moderate",
            notes=[f"Rate: {lease.royalty_rate or 'unknown'}"],
        ))

        # Add from pre-parsed clauses
        for existing_clause in lease.clauses:
            if not any(c.clause_type == existing_clause.clause_type for c in clauses):
                clauses.append(existing_clause)

        complete_trace(trace_id, ResponseLayer.COMPUTED, f"{len(clauses)} clauses identified")
        return clauses

    def _assess_pugh_risk(self, lease: LeaseRecord) -> Tuple[str, List[str]]:
        """Assess risk level for Pugh clause."""
        if not lease.has_pugh_clause:
            return ("high", ["No Pugh clause — large acreage can be held by small pooled unit"])
        if lease.pugh_type == "combined":
            return ("low", ["Combined Pugh provides best protection for lessor"])
        if lease.pugh_type == "vertical":
            return ("moderate", ["Vertical Pugh only — deep rights may still be held"])
        return ("moderate", [f"Pugh type: {lease.pugh_type or 'unspecified'}"])

    def _assess_term_risk(self, lease: LeaseRecord) -> str:
        """Assess term risk level."""
        if lease.current_status == LeaseStatus.EXPIRED.value:
            return "critical"
        if lease.current_status == LeaseStatus.PENDING_EXPIRATION.value:
            return "critical"
        if lease.current_status == LeaseStatus.HELD_BY_PRODUCTION.value:
            return "low"
        if lease.primary_term_expiration:
            days = (lease.primary_term_expiration - date.today()).days
            if days <= 90:
                return "high"
            if days <= 365:
                return "moderate"
        return "moderate"

    # ────────────────────────────────────────────────────────────────────
    # EXPIRATION TRACKING
    # ────────────────────────────────────────────────────────────────────

    def _check_expiration(self, lease: LeaseRecord) -> List[LeaseExpirationAlert]:
        """Check lease for expiration and generate alerts."""
        trace_id = trace_query(QueryType.EXPIRATION_CHECK, input_summary=f"lease={lease.lease_id}")
        alerts: List[LeaseExpirationAlert] = []
        today = date.today()

        exp_date = lease.primary_term_expiration
        if not exp_date:
            complete_trace(trace_id, ResponseLayer.COMPUTED, "no expiration date")
            return alerts

        days_until = (exp_date - today).days

        # Generate alert based on threshold
        thresholds = ENGINE_CONFIG.get("alert_thresholds", {}).get("lease_expiration_warning_days", [30, 60, 90, 180, 365])

        for threshold in sorted(thresholds):
            if days_until <= threshold:
                if days_until < 0:
                    alert_level = "critical"
                    actions = [
                        "Lease has EXPIRED — verify no saving clause applies",
                        "Check for production in paying quantities",
                        "Review shut-in, force majeure, and continuous operations clauses",
                        "If expired, prepare top lease or new lease",
                    ]
                elif days_until <= 30:
                    alert_level = "critical"
                    actions = [
                        f"CRITICAL: Lease expires in {days_until} days",
                        "Verify drilling operations are underway or production has commenced",
                        "Confirm delay rental is current (if not paid-up)",
                        "Review all saving clauses for applicability",
                        "If no activity, prepare top lease strategy",
                    ]
                elif days_until <= 90:
                    alert_level = "warning"
                    actions = [
                        f"Lease expires in {days_until} days — action required",
                        "Contact operator to confirm development plans",
                        "Review saving clauses and continuous development obligations",
                        "Begin negotiating extension if warranted",
                    ]
                else:
                    alert_level = "info"
                    actions = [
                        f"Lease expires in {days_until} days",
                        "Monitor development activity",
                        "Calendar review 90 days before expiration",
                    ]

                saving_clauses = []
                if lease.has_shut_in:
                    saving_clauses.append("Shut-in royalty")
                if lease.has_force_majeure:
                    saving_clauses.append("Force majeure")
                if lease.has_continuous_development:
                    saving_clauses.append("Continuous development")
                if lease.producing_wells:
                    saving_clauses.append(f"Production ({len(lease.producing_wells)} well(s))")

                alerts.append(LeaseExpirationAlert(
                    lease_id=lease.lease_id,
                    alert_level=alert_level,
                    days_until_expiration=days_until,
                    expiration_date=exp_date,
                    lessor_name=lease.lessor.name if lease.lessor else None,
                    lessee_name=lease.lessee.name if lease.lessee else None,
                    county=lease.county,
                    legal_description=lease.legal_description_text,
                    acres=lease.acres,
                    royalty_rate=lease.royalty_rate,
                    saving_clauses=saving_clauses,
                    recommended_actions=actions,
                ))
                break  # Only generate alert for the tightest matching threshold

        complete_trace(trace_id, ResponseLayer.COMPUTED, f"{len(alerts)} alerts generated")
        return alerts

    # ────────────────────────────────────────────────────────────────────
    # NRI CALCULATION (STANDALONE)
    # ────────────────────────────────────────────────────────────────────

    def calculate_nri(self, request: NRICalculationRequest) -> NRICalculationResponse:
        """Calculate Net Revenue Interest from components.

        Args:
            request: NRI calculation parameters.

        Returns:
            NRICalculationResponse with detailed calculation.
        """
        trace_id = trace_query(
            QueryType.NRI_CALCULATION,
            input_summary=f"MI={request.mineral_interest}, royalty={request.royalty_rate}",
        )

        steps: List[str] = []
        warnings: List[str] = []

        # Step 1: Mineral interest
        mi = request.mineral_interest
        steps.append(f"1. Mineral Interest: {mi:.6f}")

        # Step 2: Royalty rate
        royalty = request.royalty_rate
        steps.append(f"2. Royalty Rate: {royalty:.6f}")

        # Step 3: Gross working interest
        gwi = mi * (1.0 - royalty)
        steps.append(f"3. Gross Working Interest: {mi:.6f} x (1 - {royalty:.6f}) = {gwi:.6f}")

        # Step 4: ORRI burden
        total_orri = 0.0
        for i, orri in enumerate(request.overriding_royalties):
            rate = orri.get("rate", 0.0)
            name = orri.get("name", f"ORRI_{i+1}")
            total_orri += rate
            steps.append(f"4.{i+1}. ORRI '{name}': {rate:.6f}")

        if total_orri > 0:
            steps.append(f"4. Total ORRI burden: {total_orri:.6f}")
        else:
            steps.append("4. No overriding royalties")

        # Step 5: Other burdens
        total_other = 0.0
        for i, burden in enumerate(request.other_burdens):
            rate = burden.get("rate", 0.0)
            name = burden.get("name", f"Burden_{i+1}")
            total_other += rate
            steps.append(f"5.{i+1}. Other burden '{name}': {rate:.6f}")

        if total_other > 0:
            steps.append(f"5. Total other burdens: {total_other:.6f}")
        else:
            steps.append("5. No other burdens")

        # Step 6: Total burden
        total_burden = royalty + total_orri + total_other
        steps.append(f"6. Total burden: {royalty:.6f} + {total_orri:.6f} + {total_other:.6f} = {total_burden:.6f}")

        if total_burden >= 1.0:
            warnings.append(f"CRITICAL: Total burden ({total_burden:.6f}) >= 100%. NRI calculation invalid.")

        # Step 7: NRI
        nri = mi * (1.0 - total_burden)
        nri = max(nri, 0.0)
        steps.append(f"7. NRI: {mi:.6f} x (1 - {total_burden:.6f}) = {nri:.6f}")

        # Step 8: Pooling factor
        pooled_nri = None
        if request.pooling_factor is not None:
            pooled_nri = nri * request.pooling_factor
            steps.append(
                f"8. Pooling factor: {request.pooling_factor:.6f}, Pooled NRI: {nri:.6f} x {request.pooling_factor:.6f} = {pooled_nri:.6f}"
            )
        else:
            steps.append("8. No pooling adjustment")

        # Step 9: Severance tax
        tx_config = ENGINE_CONFIG.get("nri_calculation", {}).get("texas_severance_tax", {})
        if request.product_type == "gas":
            sev_rate = tx_config.get("gas_rate", 0.075)
        else:
            sev_rate = tx_config.get("oil_rate", 0.046)

        effective_nri = pooled_nri if pooled_nri is not None else nri
        after_tax = effective_nri * (1.0 - sev_rate)
        steps.append(f"9. Severance tax ({request.product_type}): {sev_rate:.4f}")
        steps.append(f"   After-tax NRI: {effective_nri:.6f} x (1 - {sev_rate:.4f}) = {after_tax:.6f}")

        # Determinism hash
        hash_content = json.dumps({
            "mi": mi, "royalty": royalty, "orri": total_orri,
            "other": total_other, "pooling": request.pooling_factor,
        }, sort_keys=True)
        det_hash = hashlib.sha256(hash_content.encode()).hexdigest()

        response = NRICalculationResponse(
            mineral_interest=mi,
            royalty_rate=royalty,
            gross_working_interest=gwi,
            total_orri_burden=total_orri,
            total_other_burdens=total_other,
            total_burden=total_burden,
            net_revenue_interest=round(nri, 6),
            pooling_factor=request.pooling_factor,
            pooled_nri=round(pooled_nri, 6) if pooled_nri is not None else None,
            severance_tax_rate=sev_rate,
            after_tax_nri=round(after_tax, 6),
            calculation_steps=steps,
            warnings=warnings,
            determinism_hash=det_hash,
        )

        complete_trace(trace_id, ResponseLayer.COMPUTED, f"NRI={nri:.6f}, after_tax={after_tax:.6f}")
        return response

    # ────────────────────────────────────────────────────────────────────
    # LEASE COMPARISON
    # ────────────────────────────────────────────────────────────────────

    def compare_leases(self, request: LeaseComparisonRequest) -> LeaseComparisonResponse:
        """Compare two or more leases side by side.

        Args:
            request: Comparison request with lease IDs or records.

        Returns:
            LeaseComparisonResponse with comparison data.
        """
        trace_id = trace_query(
            QueryType.LEASE_COMPARISON,
            input_summary=f"{len(request.lease_ids) + len(request.leases)} leases, aspects={request.comparison_aspects}",
        )
        start_time = time.monotonic()

        # Collect leases
        leases: List[LeaseRecord] = list(request.leases)
        for lid in request.lease_ids:
            lease = self._lease_store.get(lid)
            if lease:
                leases.append(lease)

        if len(leases) < 2:
            fail_trace(trace_id, "Need at least 2 leases to compare", ErrorDomain.VALIDATION)
            raise HTTPException(status_code=400, detail="Need at least 2 leases for comparison")

        comparisons: Dict[str, List[Dict[str, Any]]] = {}

        for aspect in request.comparison_aspects:
            if aspect == "royalty":
                comparisons["royalty"] = self._compare_royalty(leases)
            elif aspect == "term":
                comparisons["term"] = self._compare_terms(leases)
            elif aspect == "pooling":
                comparisons["pooling"] = self._compare_pooling(leases)
            elif aspect == "pugh":
                comparisons["pugh"] = self._compare_pugh(leases)
            elif aspect == "surface_use":
                comparisons["surface_use"] = self._compare_surface(leases)

        # Determine best for each party
        best_lessor = self._determine_best_for_lessor(leases)
        best_lessee = self._determine_best_for_lessee(leases)

        # Summary
        summary = self._generate_comparison_summary(leases, comparisons)

        elapsed = (time.monotonic() - start_time) * 1000
        hash_content = json.dumps([l.lease_id for l in leases], sort_keys=True)

        response = LeaseComparisonResponse(
            leases_compared=len(leases),
            comparison_aspects=request.comparison_aspects,
            comparisons=comparisons,
            best_for_lessor=best_lessor,
            best_for_lessee=best_lessee,
            summary=summary,
            recommendations=self._comparison_recommendations(leases, comparisons),
            trace_id=trace_id,
            processing_time_ms=round(elapsed, 2),
            determinism_hash=hashlib.sha256(hash_content.encode()).hexdigest(),
        )

        complete_trace(trace_id, ResponseLayer.COMPUTED, f"compared {len(leases)} leases in {elapsed:.0f}ms")
        return response

    def _compare_royalty(self, leases: List[LeaseRecord]) -> List[Dict[str, Any]]:
        """Compare royalty provisions across leases."""
        result = []
        for lease in leases:
            result.append({
                "lease_id": lease.lease_id,
                "lessor": lease.lessor.name if lease.lessor else "unknown",
                "lessee": lease.lessee.name if lease.lessee else "unknown",
                "royalty_fraction": lease.royalty_fraction or "unknown",
                "royalty_rate": lease.royalty_rate,
                "paid_up": lease.paid_up,
                "delay_rental_per_acre": lease.delay_rental_per_acre,
                "bonus_per_acre": lease.bonus_per_acre,
            })
        return result

    def _compare_terms(self, leases: List[LeaseRecord]) -> List[Dict[str, Any]]:
        """Compare term provisions across leases."""
        result = []
        for lease in leases:
            result.append({
                "lease_id": lease.lease_id,
                "primary_term_years": lease.primary_term_years,
                "lease_date": str(lease.lease_date) if lease.lease_date else None,
                "expiration_date": str(lease.primary_term_expiration) if lease.primary_term_expiration else None,
                "current_status": lease.current_status,
                "has_continuous_development": lease.has_continuous_development,
                "continuous_dev_gap_days": lease.continuous_dev_gap_days,
                "has_force_majeure": lease.has_force_majeure,
                "has_shut_in": lease.has_shut_in,
            })
        return result

    def _compare_pooling(self, leases: List[LeaseRecord]) -> List[Dict[str, Any]]:
        """Compare pooling provisions across leases."""
        result = []
        for lease in leases:
            result.append({
                "lease_id": lease.lease_id,
                "has_pooling": lease.has_pooling,
                "pooling_max_acres_oil": lease.pooling_max_acres_oil,
                "pooling_max_acres_gas": lease.pooling_max_acres_gas,
                "has_pugh_clause": lease.has_pugh_clause,
                "pugh_type": lease.pugh_type,
            })
        return result

    def _compare_pugh(self, leases: List[LeaseRecord]) -> List[Dict[str, Any]]:
        """Compare Pugh clause provisions across leases."""
        result = []
        for lease in leases:
            result.append({
                "lease_id": lease.lease_id,
                "has_pugh": lease.has_pugh_clause,
                "pugh_type": lease.pugh_type,
                "has_depth_limitation": lease.has_depth_limitation,
                "depth_limitation": lease.depth_limitation_text,
                "has_retained_acreage": True if lease.has_pugh_clause else False,
                "total_acres": lease.acres,
            })
        return result

    def _compare_surface(self, leases: List[LeaseRecord]) -> List[Dict[str, Any]]:
        """Compare surface use provisions across leases."""
        result = []
        for lease in leases:
            result.append({
                "lease_id": lease.lease_id,
                "has_surface_restrictions": lease.has_surface_restrictions,
                "has_mother_hubbard": lease.has_mother_hubbard,
            })
        return result

    def _determine_best_for_lessor(self, leases: List[LeaseRecord]) -> Optional[str]:
        """Determine which lease is best for the lessor."""
        best_id = None
        best_score = -1.0

        for lease in leases:
            score = 0.0
            if lease.royalty_rate:
                score += lease.royalty_rate * 100  # Higher royalty = better
            if lease.has_pugh_clause:
                score += 20  # Pugh clause protects lessor
            if lease.pugh_type == "combined":
                score += 10
            if lease.has_continuous_development:
                score += 5
            if lease.primary_term_years:
                score -= lease.primary_term_years * 2  # Shorter term = better for lessor
            if lease.has_surface_restrictions:
                score += 5

            if score > best_score:
                best_score = score
                best_id = lease.lease_id

        return best_id

    def _determine_best_for_lessee(self, leases: List[LeaseRecord]) -> Optional[str]:
        """Determine which lease is best for the lessee."""
        best_id = None
        best_score = -1.0

        for lease in leases:
            score = 0.0
            if lease.royalty_rate:
                score += (1.0 - lease.royalty_rate) * 100  # Lower royalty = better
            if not lease.has_pugh_clause:
                score += 20  # No Pugh = more flexibility
            if lease.primary_term_years:
                score += lease.primary_term_years * 3  # Longer term = better for lessee
            if lease.has_pooling:
                score += 10  # Pooling authority
            if not lease.has_continuous_development:
                score += 5
            if lease.paid_up:
                score += 5  # No annual rental payments

            if score > best_score:
                best_score = score
                best_id = lease.lease_id

        return best_id

    def _generate_comparison_summary(
        self, leases: List[LeaseRecord], comparisons: Dict[str, List[Dict[str, Any]]]
    ) -> str:
        """Generate a human-readable comparison summary."""
        parts: List[str] = []
        parts.append(f"Compared {len(leases)} leases.")

        # Royalty comparison
        if "royalty" in comparisons:
            rates = [l.royalty_rate for l in leases if l.royalty_rate]
            if rates:
                parts.append(
                    f"Royalty rates range from {min(rates):.4f} ({min(rates)*100:.2f}%) "
                    f"to {max(rates):.4f} ({max(rates)*100:.2f}%)."
                )

        # Term comparison
        if "term" in comparisons:
            terms = [l.primary_term_years for l in leases if l.primary_term_years]
            if terms:
                parts.append(f"Primary terms range from {min(terms)} to {max(terms)} years.")

        # Pugh comparison
        pugh_count = sum(1 for l in leases if l.has_pugh_clause)
        parts.append(f"{pugh_count} of {len(leases)} leases contain a Pugh clause.")

        return " ".join(parts)

    def _comparison_recommendations(
        self, leases: List[LeaseRecord], comparisons: Dict[str, List[Dict[str, Any]]]
    ) -> List[str]:
        """Generate recommendations from comparison."""
        recs: List[str] = []

        # Royalty
        rates = [l.royalty_rate for l in leases if l.royalty_rate]
        if rates and max(rates) - min(rates) > 0.05:
            recs.append(
                "Significant royalty rate variation between leases — consider negotiating "
                "standardized rate for future leases in the area"
            )

        # Pugh
        no_pugh = [l for l in leases if not l.has_pugh_clause]
        if no_pugh:
            recs.append(
                f"{len(no_pugh)} lease(s) lack Pugh clause — recommend adding Pugh provision "
                f"in any amendment or renewal"
            )

        # Term
        long_terms = [l for l in leases if l.primary_term_years and l.primary_term_years >= 5]
        if long_terms:
            recs.append(
                f"{len(long_terms)} lease(s) have 5+ year primary terms — "
                "consider requesting shorter terms with extension options"
            )

        return recs

    # ────────────────────────────────────────────────────────────────────
    # RISK ASSESSMENT
    # ────────────────────────────────────────────────────────────────────

    def _compute_risk_summary(
        self,
        lease: LeaseRecord,
        term_analysis: Optional[TermAnalysis],
        pugh_analysis: Optional[PughClauseAnalysis],
    ) -> Dict[str, Any]:
        """Compute a risk summary for the lease."""
        risks: Dict[str, str] = {}
        overall_risk = "low"
        risk_scores: List[int] = []

        # Term risk
        if term_analysis:
            risks["term"] = term_analysis.risk_level
            risk_scores.append({"low": 1, "moderate": 2, "high": 3, "critical": 4}.get(term_analysis.risk_level, 2))

        # Pugh risk
        if pugh_analysis:
            risks["pugh"] = pugh_analysis.risk_level
            risk_scores.append({"low": 1, "moderate": 2, "high": 3, "critical": 4}.get(pugh_analysis.risk_level, 2))

        # Royalty risk
        if lease.royalty_rate:
            if lease.royalty_rate < 0.1875:
                risks["royalty"] = "high"
                risk_scores.append(3)
            elif lease.royalty_rate < 0.25:
                risks["royalty"] = "moderate"
                risk_scores.append(2)
            else:
                risks["royalty"] = "low"
                risk_scores.append(1)

        # Pooling risk
        if lease.has_pooling and not lease.has_pugh_clause:
            risks["pooling"] = "high"
            risk_scores.append(3)
        elif lease.has_pooling:
            risks["pooling"] = "moderate"
            risk_scores.append(2)
        else:
            risks["pooling"] = "low"
            risk_scores.append(1)

        # Continuous development risk
        if lease.has_continuous_development and lease.continuous_dev_gap_days:
            if lease.continuous_dev_gap_days < 90:
                risks["continuous_dev"] = "high"
                risk_scores.append(3)
            else:
                risks["continuous_dev"] = "moderate"
                risk_scores.append(2)

        # Depth risk
        if lease.has_depth_limitation:
            risks["depth"] = "moderate"
            risk_scores.append(2)

        # Overall risk
        if risk_scores:
            avg_risk = sum(risk_scores) / len(risk_scores)
            if avg_risk >= 3.5:
                overall_risk = "critical"
            elif avg_risk >= 2.5:
                overall_risk = "high"
            elif avg_risk >= 1.5:
                overall_risk = "moderate"
            else:
                overall_risk = "low"

        return {
            "overall_risk": overall_risk,
            "risk_by_category": risks,
            "risk_score": round(sum(risk_scores) / max(len(risk_scores), 1), 2),
            "max_risk_category": max(risks, key=lambda k: {"low": 1, "moderate": 2, "high": 3, "critical": 4}.get(risks[k], 0)) if risks else None,
        }

    # ────────────────────────────────────────────────────────────────────
    # DOCTRINE AND RECOMMENDATION HELPERS
    # ────────────────────────────────────────────────────────────────────

    def _gather_doctrine_references(self, analysis_type: str, lease: LeaseRecord) -> List[Dict[str, str]]:
        """Gather relevant doctrine references for the analysis."""
        relevant_keys: List[str] = []

        if analysis_type in ("full", "term"):
            relevant_keys.extend(["habendum_primary_term", "habendum_secondary_term", "hbp_status"])
        if analysis_type in ("full", "royalty"):
            relevant_keys.extend(["royalty_calculation", "overriding_royalty", "nri_calculation"])
        if analysis_type in ("full", "pugh"):
            relevant_keys.extend(["pugh_vertical", "pugh_horizontal", "pugh_depth"])
        if analysis_type in ("full", "clause"):
            relevant_keys.extend(["drilling_clause", "delay_rental_unless", "implied_covenants"])
        if analysis_type in ("full", "expiration"):
            relevant_keys.extend(["cessation_of_production", "shut_in_royalty"])

        # Add lease-specific doctrines
        if lease.has_force_majeure:
            relevant_keys.append("force_majeure")
        if lease.has_continuous_development:
            relevant_keys.append("continuous_development")
        if lease.has_pooling:
            relevant_keys.append("pooling_voluntary")
        if lease.has_depth_limitation:
            relevant_keys.append("depth_limitation")

        # Deduplicate
        seen: Set[str] = set()
        refs: List[Dict[str, str]] = []
        for key in relevant_keys:
            if key in seen:
                continue
            seen.add(key)
            doctrine = get_doctrine(key)
            if doctrine:
                refs.append({
                    "key": key,
                    "title": doctrine.title,
                    "category": doctrine.category.value,
                    "summary": doctrine.summary[:200] + "..." if len(doctrine.summary) > 200 else doctrine.summary,
                })
        return refs

    def _generate_recommendations(self, lease: LeaseRecord, response: LeaseAnalysisResponse) -> List[str]:
        """Generate actionable recommendations from the analysis."""
        recs: List[str] = []

        # Term recommendations
        if response.term_analysis:
            ta = response.term_analysis
            if ta.is_expired:
                recs.append("EXPIRED: Verify no saving clause applies. If expired, pursue new lease or top lease immediately.")
            elif ta.current_term in ("primary_expiring", "primary_warning"):
                recs.append(
                    f"EXPIRING: Lease expires in {ta.days_remaining_primary} days. "
                    "Confirm operator has commenced operations or production."
                )
            if not ta.saving_clauses:
                recs.append("No saving clauses identified — lease will terminate at end of primary term without production.")

        # Royalty recommendations
        if lease.royalty_rate and lease.royalty_rate < 0.25:
            recs.append(
                f"Below-market royalty rate ({lease.royalty_rate:.4f}). "
                "Current Permian Basin standard is 1/4 (0.2500). Negotiate higher rate on renewal."
            )

        # Pugh recommendations
        if not lease.has_pugh_clause and lease.acres and lease.acres > 160:
            recs.append(
                "No Pugh clause on a large acreage lease. Production from a single pooled unit "
                "will hold all acreage and depths. Strongly recommend Pugh clause in any amendment."
            )

        # Depth recommendations
        if not lease.has_depth_limitation and lease.target_formations:
            recs.append(
                "No depth limitation. Lease covers all depths. Consider requesting depth "
                "limitation to release non-target formations."
            )

        # Continuous development
        if not lease.has_continuous_development and lease.acres and lease.acres > 320:
            recs.append(
                "No continuous development clause. Operator has no obligation to drill "
                "additional wells after holding the lease with one well."
            )

        # Preferential right
        if lease.has_preferential_right:
            recs.append(
                "ROFR/Preferential right exists — must be honored in any assignment or sale. "
                "Build ROFR compliance into any transaction timeline."
            )

        return recs

    # ────────────────────────────────────────────────────────────────────
    # HEALTH AND METADATA
    # ────────────────────────────────────────────────────────────────────

    def get_health(self) -> Dict[str, Any]:
        """Get engine health status."""
        uptime = time.time() - self._start_time
        telemetry_health = self._telemetry.get_health()

        return {
            "engine_id": ENGINE_ID,
            "engine_name": ENGINE_NAME,
            "engine_version": ENGINE_VERSION,
            "engine_tier": ENGINE_TIER,
            "engine_mode": ENGINE_MODE,
            "engine_port": ENGINE_PORT,
            "status": telemetry_health.get("status", "healthy"),
            "uptime_seconds": round(uptime, 1),
            "leases_in_memory": len(self._lease_store),
            "search_index_entries": self._search_index.total_entries,
            "doctrine_cache_blocks": len(DOCTRINE_CACHE),
            "doctrine_cache_version": DOCTRINE_CACHE_VERSION,
            "doctrine_integrity": verify_cache_integrity(),
            "telemetry": telemetry_health,
            "tie20_components": {
                "authority_hardening": {
                    "active": True,
                    "topics_loaded": len(self._authority_engine._authority_index),
                },
                "drift_watcher": {
                    "active": True,
                    "observations": len(self._drift_watcher._observations),
                },
                "coverage_tracker": {
                    "active": True,
                    "total_doctrines": self._coverage_tracker._total_doctrines,
                    "coverage_rate": round(
                        len(set(self._coverage_tracker._triggered_count.keys())) /
                        max(self._coverage_tracker._total_doctrines, 1), 3
                    ),
                },
                "fragility_analyzer": {"active": True},
                "doctrine_decomposer": {
                    "active": True,
                    "interaction_edges": len(self._doctrine_decomposer._interaction_graph),
                },
                "zoned_analysis": {
                    "active": True,
                    "current_zone": self._zoned_analysis._current_zone.value if self._zoned_analysis._current_zone else None,
                },
                "deep_analysis": {
                    "active": True,
                    "cloud_available": self._deep_analysis._cloud_available,
                },
            },
        }

    def get_statistics(self) -> Dict[str, Any]:
        """Get engine statistics."""
        return {
            "engine_id": ENGINE_ID,
            "leases_stored": len(self._lease_store),
            "search_index": self._search_index.get_statistics(),
            "doctrine_summary": get_doctrine_summary(),
            "semantic_integrity": verify_semantic_map_integrity(),
            "metrics": self._telemetry.get_metrics(),
        }


# ============================================================================
# ENGINE SINGLETON
# ============================================================================

_ENGINE = LM02LeaseAnalysisEngine()


def get_engine() -> LM02LeaseAnalysisEngine:
    """Get the module-level engine instance."""
    return _ENGINE


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    logger.info(f"LM02 Lease Analysis Engine v{ENGINE_VERSION} starting on port {ENGINE_PORT}")
    yield
    logger.info("LM02 Lease Analysis Engine shutting down")


app = FastAPI(
    title=f"ECHO {ENGINE_ID} {ENGINE_NAME}",
    version=ENGINE_VERSION,
    description="Oil and Gas Lease Analysis Engine for the Permian Basin",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Health Endpoints ───

@app.get("/health")
async def health_endpoint():
    """Engine health check."""
    return _ENGINE.get_health()


@app.get("/statistics")
async def statistics_endpoint():
    """Engine statistics."""
    return _ENGINE.get_statistics()


@app.get("/metrics")
async def metrics_endpoint():
    """Telemetry metrics."""
    return get_telemetry().get_metrics()


@app.get("/doctrines")
async def doctrines_endpoint():
    """List all doctrine keys and summary."""
    return get_doctrine_summary()


@app.get("/doctrines/{key}")
async def doctrine_detail_endpoint(key: str):
    """Get a specific doctrine block."""
    block = get_doctrine(key)
    if block is None:
        raise HTTPException(status_code=404, detail=f"Doctrine '{key}' not found")
    return block.to_dict()


@app.get("/glossary")
async def glossary_endpoint():
    """Get the lease term glossary."""
    return LEASE_TERM_GLOSSARY


@app.get("/glossary/{term}")
async def glossary_term_endpoint(term: str):
    """Look up a glossary term."""
    definition = get_glossary_definition(term)
    if definition is None:
        raise HTTPException(status_code=404, detail=f"Term '{term}' not found in glossary")
    return {"term": term, "definition": definition}


# ─── Lease CRUD ───

@app.post("/leases")
async def add_lease_endpoint(lease: LeaseRecord):
    """Add a lease to the engine."""
    lease_id = _ENGINE.add_lease(lease)
    return {"lease_id": lease_id, "status": "added"}


@app.get("/leases/{lease_id}")
async def get_lease_endpoint(lease_id: str):
    """Get a lease by ID."""
    lease = _ENGINE.get_lease(lease_id)
    if lease is None:
        raise HTTPException(status_code=404, detail=f"Lease '{lease_id}' not found")
    return lease


@app.delete("/leases/{lease_id}")
async def delete_lease_endpoint(lease_id: str):
    """Delete a lease."""
    removed = _ENGINE.remove_lease(lease_id)
    if not removed:
        raise HTTPException(status_code=404, detail=f"Lease '{lease_id}' not found")
    return {"lease_id": lease_id, "status": "deleted"}


# ─── Analysis Endpoints ───

@app.post("/analyze")
async def analyze_lease_endpoint(request: LeaseAnalysisRequest):
    """Analyze a lease."""
    return _ENGINE.analyze_lease(request)


@app.post("/nri")
async def nri_endpoint(request: NRICalculationRequest):
    """Calculate NRI."""
    return _ENGINE.calculate_nri(request)


@app.post("/compare")
async def compare_endpoint(request: LeaseComparisonRequest):
    """Compare leases."""
    return _ENGINE.compare_leases(request)


# ─── Search Endpoints ───

@app.post("/search")
async def search_endpoint(query: LeaseSearchQuery):
    """Search leases."""
    return search_leases(query)


@app.get("/search/expiring")
async def expiring_endpoint(
    window: ExpirationWindow = ExpirationWindow.NEXT_90_DAYS,
    county: Optional[str] = None,
    operator: Optional[str] = None,
):
    """Search for expiring leases."""
    return search_expiring_leases(window, county, operator)


@app.get("/alerts/expiration")
async def expiration_alerts_endpoint(
    county: Optional[str] = None,
):
    """Generate expiration alerts."""
    return generate_expiration_alerts(county)


# ─── Semantic Endpoints ───

@app.get("/normalize/{term}")
async def normalize_endpoint(term: str):
    """Normalize a lease term."""
    return normalize_lease_term(term).to_dict()


@app.post("/parse/legal-description")
async def parse_legal_desc_endpoint(request: Dict[str, str]):
    """Parse a legal description."""
    text = request.get("text", "")
    if not text:
        raise HTTPException(status_code=400, detail="Provide 'text' field with legal description")
    return parse_legal_description(text).to_dict()


@app.post("/parse/royalty")
async def parse_royalty_endpoint(request: Dict[str, str]):
    """Parse a royalty fraction."""
    text = request.get("text", "")
    if not text:
        raise HTTPException(status_code=400, detail="Provide 'text' field with royalty fraction")
    return parse_royalty_fraction(text).to_dict()


@app.post("/identify-clauses")
async def identify_clauses_endpoint(request: Dict[str, str]):
    """Identify clause types in lease text."""
    text = request.get("text", "")
    if not text:
        raise HTTPException(status_code=400, detail="Provide 'text' field with lease text")
    results = identify_clause_types(text)
    return [
        {"clause_type": ct.value, "confidence": conf, "matched_indicators": matched}
        for ct, conf, matched in results
    ]


@app.post("/match-doctrine")
async def match_doctrine_endpoint(request: Dict[str, Any]):
    """Match a query to relevant doctrines."""
    query = request.get("query", "")
    top_k = request.get("top_k", 5)
    if not query:
        raise HTTPException(status_code=400, detail="Provide 'query' field")
    results = match_doctrine(query, top_k)
    return [
        {"key": key, "score": score, "title": block.title, "summary": block.summary[:200]}
        for key, score, block in results
    ]


# ─── Telemetry Endpoints ───

@app.get("/traces")
async def traces_endpoint(limit: int = 50, query_type: Optional[str] = None):
    """Get recent query traces."""
    qt = QueryType(query_type) if query_type else None
    return get_telemetry().get_recent_traces(limit, qt)


@app.get("/errors")
async def errors_endpoint(limit: int = 50, domain: Optional[str] = None):
    """Get recent errors."""
    d = ErrorDomain(domain) if domain else None
    return get_telemetry().get_recent_errors(limit, d)


@app.get("/audit")
async def audit_endpoint(limit: int = 100, entity_type: Optional[str] = None):
    """Get audit log."""
    return get_telemetry().get_audit_log(limit, entity_type)


# ─── TIE-20 Component Endpoints ───

@app.get("/tie20/authority/{topic}")
async def authority_resolution_endpoint(topic: str):
    """Resolve the highest authority source for a topic."""
    source = _ENGINE._authority_engine.resolve_authority(topic)
    if source is None:
        return {"topic": topic, "authority_found": False}
    return {
        "topic": topic,
        "authority_found": True,
        "citation": source.citation,
        "authority_level": source.authority_level.value,
        "weight": source.weight,
        "summary": source.summary,
        "url": source.url,
    }


@app.get("/tie20/authority/{topic}/conflicts")
async def authority_conflicts_endpoint(topic: str):
    """Detect conflicting authority sources on a topic."""
    conflicts = _ENGINE._authority_engine.detect_conflicts(topic)
    return {
        "topic": topic,
        "conflicts_detected": len(conflicts) > 0,
        "conflict_count": len(conflicts),
        "conflicts": [
            {
                "source_a": {"citation": a.citation, "level": a.authority_level.value, "weight": a.weight},
                "source_b": {"citation": b.citation, "level": b.authority_level.value, "weight": b.weight},
            }
            for a, b in conflicts
        ],
    }


@app.get("/tie20/drift")
async def drift_summary_endpoint(doctrine_key: Optional[str] = None):
    """Get drift summary for a specific doctrine or all doctrines."""
    return _ENGINE._drift_watcher.get_drift_summary(doctrine_key)


@app.get("/tie20/coverage")
async def coverage_map_endpoint():
    """Get doctrine coverage map showing triggered vs missed doctrines."""
    return _ENGINE._coverage_tracker.get_coverage_map()


@app.post("/tie20/fragility")
async def fact_fragility_endpoint(request: Dict[str, str]):
    """Assess fact fragility for a lease analysis fact."""
    fact = request.get("fact", "")
    source = request.get("source", "unknown")
    if not fact:
        raise HTTPException(status_code=400, detail="Provide 'fact' field")
    score = _ENGINE._fragility_analyzer.assess_lease_fact(fact, source)
    return score.to_dict()


@app.post("/tie20/decompose")
async def multi_doctrine_decompose_endpoint(request: Dict[str, Any]):
    """Decompose a complex issue into interacting doctrines."""
    issue = request.get("issue", "")
    category = request.get("category", IssueCategory.TERM_STATUS.value)
    if not issue:
        raise HTTPException(status_code=400, detail="Provide 'issue' field")
    try:
        cat = IssueCategory(category)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid category: {category}")
    return _ENGINE._doctrine_decomposer.decompose_issue(issue, cat)


@app.get("/tie20/zones/{zone}")
async def zone_guidance_endpoint(zone: str):
    """Get guidance for a specific analysis zone."""
    try:
        z = AnalysisZone(zone.upper())
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid zone: {zone}")
    return {
        "zone": z.value,
        "guidance": _ENGINE._zoned_analysis.get_zone_guidance(z),
    }


@app.post("/tie20/deep-analysis")
async def deep_analysis_endpoint(request: Dict[str, Any]):
    """Perform deep multi-source analysis."""
    query = request.get("query", "")
    lease_context = request.get("lease_context")
    mode_str = request.get("mode", "DEEP")
    if not query:
        raise HTTPException(status_code=400, detail="Provide 'query' field")
    try:
        mode = ResponseMode(mode_str.upper())
    except ValueError:
        mode = ResponseMode.DEEP
    return await _ENGINE._deep_analysis.deep_analyze(query, lease_context, mode)


# ============================================================================
# CLOUD-ENRICHED QUERY ENDPOINT
# ============================================================================


class _CloudQueryRequest(BaseModel):
    query: str = ""
    prompt: str = ""
    mode: str = "full"
    include_cloud: bool = True


@app.post("/query")
async def cloud_query_endpoint(request: _CloudQueryRequest):
    """Universal query endpoint with cloud knowledge retrieval."""
    import time as _time
    start = _time.monotonic()
    q = request.query or request.prompt

    # Cloud retrieval
    cloud_data = {}
    cloud_citations = []
    if _CLOUD_AVAILABLE and request.include_cloud:
        try:
            cloud = await retrieve_cloud_knowledge(q, category="lease_analysis")
            cloud_data = {
                "records": cloud.total_records,
                "merged_context": cloud.merged_text(3000),
                "sources_succeeded": cloud.sources_succeeded,
                "retrieval_time_ms": cloud.retrieval_time_ms,
            }
            cloud_citations = cloud.citation_list()
        except Exception as e:
            logger.warning(f"Cloud retrieval failed: {e}")

    # Local engine analysis
    analysis = {}
    try:
        engine = get_engine()
        doctrine_matches = engine._doctrine_cache.match_doctrines(q) if hasattr(engine, '_doctrine_cache') else []
        analysis = {
            "engine_id": ENGINE_ID,
            "query": q,
            "mode": request.mode,
            "doctrine_matches": len(doctrine_matches) if doctrine_matches else 0,
        }
    except Exception as e:
        analysis = {"error": str(e)}

    elapsed = (_time.monotonic() - start) * 1000
    return {
        "engine_id": ENGINE_ID, "engine_name": ENGINE_NAME, "query": q,
        "analysis": analysis, "cloud_knowledge": cloud_data,
        "cloud_citations": cloud_citations, "processing_time_ms": round(elapsed, 2),
        "cloud_available": _CLOUD_AVAILABLE,
    }


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    logger.info(f"Starting LM02 {ENGINE_NAME} v{ENGINE_VERSION} on port {ENGINE_PORT}")
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    uvicorn.run(
        "engine:app",
        host="0.0.0.0",
        port=ENGINE_PORT,
        reload=False,
        log_level="info",
    )