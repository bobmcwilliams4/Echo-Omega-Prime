"""
LM14 Easement Analyzer Engine - Main FastAPI Engine
======================================================
Production-grade easement analysis engine implementing all 20 TIE
components for easement identification, ROW width/depth analysis,
surface use agreement parsing, pipeline corridor mapping, accommodation
doctrine compliance checking, surface damage calculation, eminent domain
tracking, and easement conflict detection.

TIE-20 Components:
    1.  three_layer_response
    2.  response_modes (fast, analysis, memo, row_review, condemnation_analysis)
    3.  doctrine_cache
    4.  authority_hardening
    5.  confidence_stratification
    6.  semantic_normalization
    7.  vector_search (TF-IDF inverted index implementation)
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

Port: 8434
Engine: LM14 Easement Analyzer
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
# Cloud retriever
# ---------------------------------------------------------------------------
_SHARED_DIR = str(Path(__file__).resolve().parent.parent / "_shared")
if _SHARED_DIR not in sys.path:
    sys.path.insert(0, _SHARED_DIR)
try:
    from cloud_retriever import retrieve_cloud_knowledge
    _CLOUD_AVAILABLE = True
except ImportError:
    _CLOUD_AVAILABLE = False

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
    search_doctrines,
    get_blocks_by_category,
    get_blocks_by_tag,
    doctrine_cache_health,
    export_all_doctrines,
)
from semantic import (
    SEMANTIC_MAP,
    ABBREVIATION_MAP,
    INSTRUMENT_TYPE_MAP,
    OPERATOR_ALIAS_MAP,
    normalize_query,
    expand_abbreviations,
    resolve_synonyms,
    resolve_operator,
    classify_instrument_type,
    extract_easement_terms,
    get_all_canonical_terms,
    semantic_health,
)
from search import (
    EasementRecord,
    EasementType,
    EasementStatus,
    SearchQuery,
    SearchResult,
    SearchResponse,
    SortField,
    SortOrder,
    EasementSearchIndex,
    build_search_index,
    get_search_index,
    search_easements,
    filter_by_location,
    filter_by_type,
    filter_by_operator,
    filter_by_dimensions,
    search_index_health,
)
from telemetry import (
    TelemetryCollector,
    get_telemetry,
    telemetry_health,
    telemetry_dashboard,
    reset_telemetry,
)


# ============================================================================
# CONSTANTS
# ============================================================================

ENGINE_ID = "LM14"
ENGINE_NAME = "Easement Analyzer"
ENGINE_VERSION = "1.0.0"
ENGINE_PORT = 8434
ENGINE_AUTHORITY = 7.0
ENGINE_TIER = "LANDMAN"
ENGINE_MODE = "DET"

CONFIG_PATH = Path(__file__).parent / "config.json"
AUDIT_LOG_DIR = Path(__file__).parent / "audit_logs"

TEXAS_PERMIAN_COUNTIES: Set[str] = {
    "andrews", "borden", "crane", "crockett", "dawson", "ector",
    "gaines", "glasscock", "howard", "irion", "lea", "loving",
    "martin", "midland", "mitchell", "pecos", "reagan", "reeves",
    "scurry", "sterling", "terrell", "upton", "ward", "winkler", "yoakum",
}


# ============================================================================
# RESPONSE MODE ENUM
# ============================================================================

class ResponseMode(str, Enum):
    FAST = "fast"
    ANALYSIS = "analysis"
    MEMO = "memo"
    ROW_REVIEW = "row_review"
    CONDEMNATION_ANALYSIS = "condemnation_analysis"


# ============================================================================
# CONFIDENCE LEVELS
# ============================================================================

class ConfidenceLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNCERTAIN = "uncertain"


# ============================================================================
# PYDANTIC MODELS - REQUEST / RESPONSE
# ============================================================================

class EasementQueryRequest(BaseModel):
    """Request model for easement analysis queries."""
    query: str = Field(..., min_length=1, max_length=5000, description="The easement analysis query")
    mode: ResponseMode = Field(default=ResponseMode.ANALYSIS, description="Response mode")
    county: Optional[str] = Field(default=None, description="County filter")
    state: Optional[str] = Field(default="TX", description="State filter")
    easement_type: Optional[str] = Field(default=None, description="Easement type filter")
    grantor: Optional[str] = Field(default=None, description="Grantor name filter")
    grantee: Optional[str] = Field(default=None, description="Grantee name filter")
    pipeline_operator: Optional[str] = Field(default=None, description="Pipeline operator filter")
    include_doctrines: bool = Field(default=True, description="Include matched doctrine blocks")
    include_statutes: bool = Field(default=True, description="Include statutory citations")
    session_id: Optional[str] = Field(default=None, description="Session tracking ID")
    max_results: int = Field(default=10, ge=1, le=50, description="Max results to return")


class EasementDoctrineRef(BaseModel):
    """Reference to a matched doctrine block."""
    topic: str
    summary: str
    category: str
    authority_score: float
    key_statutes: List[str]
    leading_cases: List[str]
    relevance_score: float


class EasementAnalysisLayer(BaseModel):
    """A single analysis layer result."""
    layer_name: str
    content: str
    confidence: ConfidenceLevel
    citations: List[str]
    latency_ms: float


class FactFragilityScore(BaseModel):
    """Fact fragility assessment for a specific claim or finding."""
    claim: str
    fragility_score: float = Field(ge=0.0, le=1.0, description="0=robust, 1=fragile")
    risk_factors: List[str]
    mitigation: str


class EasementIdentification(BaseModel):
    """Identified easement from an instrument or query."""
    easement_type: str
    classification_confidence: float
    dominant_estate: Optional[str] = None
    servient_estate: Optional[str] = None
    purpose: str
    width_ft: Optional[float] = None
    depth_ft: Optional[float] = None
    duration: str = "perpetual"
    recording_info: Optional[str] = None
    notes: str = ""


class ROWAnalysis(BaseModel):
    """Right-of-way width and depth analysis."""
    permanent_row_width_ft: float
    temp_workspace_ft: float
    depth_of_cover_ft: float
    pipe_diameter_inches: float = 0.0
    product_type: str = ""
    road_crossing_depth_ft: float = 48.0
    waterway_crossing_depth_ft: float = 60.0
    casing_required: bool = False
    hdd_recommended: bool = False
    rrc_permit_required: bool = True
    txdot_permit_required: bool = False
    compliance_notes: List[str] = Field(default_factory=list)


class AccommodationDoctrineCheck(BaseModel):
    """Accommodation doctrine compliance assessment."""
    existing_surface_use: str
    mineral_operations_description: str
    impairment_assessment: str
    alternative_methods_available: bool
    alternatives_description: str = ""
    compliance_status: str  # "compliant", "at_risk", "non_compliant"
    risk_factors: List[str]
    recommendations: List[str]
    confidence: ConfidenceLevel


class SurfaceDamageCalculation(BaseModel):
    """Surface damage assessment and compensation estimate."""
    damage_type: str
    acreage_affected: float
    crop_damage_estimate: float = 0.0
    fence_repair_estimate: float = 0.0
    road_damage_estimate: float = 0.0
    water_source_impact: str = ""
    restoration_cost_estimate: float = 0.0
    total_estimated_damage: float = 0.0
    notice_required: bool = True
    notice_period_days: int = 30
    statutory_basis: str = "Tex. Nat. Res. Code Ch. 52"
    notes: str = ""


class EasementConflict(BaseModel):
    """Detected conflict between easements."""
    conflict_type: str
    easement_a: str
    easement_b: str
    description: str
    severity: str  # "low", "medium", "high", "critical"
    resolution_options: List[str]
    priority_analysis: str


class CondemnationTracker(BaseModel):
    """Eminent domain / condemnation proceeding tracking."""
    condemner: str
    condemnee: str
    property_description: str
    common_carrier_status: str  # "confirmed", "disputed", "unverified"
    denbury_test_analysis: str
    just_compensation_estimate: float = 0.0
    severance_damages_estimate: float = 0.0
    proceeding_status: str
    key_dates: Dict[str, str] = Field(default_factory=dict)
    statutory_basis: List[str] = Field(default_factory=list)


class DeterminismHash(BaseModel):
    """SHA-256 determinism hash for response verification."""
    hash_value: str
    algorithm: str = "sha256"
    input_hash: str
    timestamp: str


class EasementQueryResponse(BaseModel):
    """Complete response model for easement analysis queries."""
    engine_id: str = ENGINE_ID
    engine_version: str = ENGINE_VERSION
    request_id: str
    mode: ResponseMode
    timestamp: str

    # Three-layer response
    layers: List[EasementAnalysisLayer]

    # Analysis outputs
    easement_identifications: List[EasementIdentification] = Field(default_factory=list)
    row_analysis: Optional[ROWAnalysis] = None
    accommodation_check: Optional[AccommodationDoctrineCheck] = None
    surface_damage: Optional[SurfaceDamageCalculation] = None
    conflicts: List[EasementConflict] = Field(default_factory=list)
    condemnation: Optional[CondemnationTracker] = None

    # Doctrine
    matched_doctrines: List[EasementDoctrineRef] = Field(default_factory=list)
    fact_fragility: List[FactFragilityScore] = Field(default_factory=list)

    # Metadata
    confidence: ConfidenceLevel
    determinism_hash: DeterminismHash
    total_latency_ms: float
    search_results_count: int = 0
    warnings: List[str] = Field(default_factory=list)
    disclosure_caveat: str = (
        "This analysis is provided for informational purposes only and does not "
        "constitute legal advice. Easement rights and obligations should be "
        "confirmed through review of recorded instruments by qualified legal "
        "counsel licensed in the applicable jurisdiction."
    )


class HealthResponse(BaseModel):
    """Health check response model."""
    engine_id: str = ENGINE_ID
    engine_name: str = ENGINE_NAME
    engine_version: str = ENGINE_VERSION
    status: str
    timestamp: str
    uptime_seconds: float
    doctrine_cache: Dict[str, Any]
    search_index: Dict[str, Any]
    telemetry: Dict[str, Any]
    semantic: Dict[str, Any]


class SearchRequest(BaseModel):
    """Request model for direct search."""
    query: str = ""
    easement_type: Optional[str] = None
    county: Optional[str] = None
    state: Optional[str] = None
    grantor: Optional[str] = None
    grantee: Optional[str] = None
    pipeline_operator: Optional[str] = None
    min_width_ft: Optional[float] = None
    max_width_ft: Optional[float] = None
    min_depth_ft: Optional[float] = None
    max_depth_ft: Optional[float] = None
    limit: int = Field(default=10, ge=1, le=50)
    offset: int = Field(default=0, ge=0)
    sort_by: str = "relevance"
    sort_order: str = "desc"


class InstrumentClassifyRequest(BaseModel):
    """Request model for instrument type classification."""
    text: str = Field(..., min_length=1, max_length=10000)


class EasementTermsRequest(BaseModel):
    """Request model for easement term extraction."""
    text: str = Field(..., min_length=1, max_length=50000)


class ROWReviewRequest(BaseModel):
    """Request model for pipeline ROW review."""
    pipe_diameter_inches: float = Field(gt=0)
    product_type: str = Field(..., min_length=1)
    operating_pressure_psi: float = Field(ge=0)
    length_miles: float = Field(gt=0)
    county: str = ""
    crosses_highway: bool = False
    crosses_railroad: bool = False
    crosses_waterway: bool = False
    existing_easement_width_ft: Optional[float] = None
    proposed_width_ft: Optional[float] = None


class AccommodationCheckRequest(BaseModel):
    """Request for accommodation doctrine compliance check."""
    existing_surface_use: str = Field(..., min_length=1)
    proposed_mineral_operations: str = Field(..., min_length=1)
    alternative_methods_description: str = ""
    county: str = ""
    surface_owner: str = ""
    mineral_operator: str = ""


class SurfaceDamageRequest(BaseModel):
    """Request for surface damage calculation."""
    acreage_affected: float = Field(gt=0)
    crop_type: str = ""
    existing_improvements: List[str] = Field(default_factory=list)
    operation_type: str = ""
    duration_days: int = 30
    county: str = ""
    surface_owner_is_mineral_owner: bool = False


class ConflictCheckRequest(BaseModel):
    """Request for easement conflict detection."""
    property_id: str = ""
    county: str = ""
    legal_description: str = ""
    proposed_easement_type: str = ""
    proposed_width_ft: float = 0.0
    proposed_route_description: str = ""


# ============================================================================
# CORE ANALYSIS ENGINE
# ============================================================================

class EasementAnalyzer:
    """
    Core analysis engine for LM14. Orchestrates doctrine cache lookups,
    semantic search, easement identification, ROW analysis, accommodation
    doctrine compliance, surface damage calculation, and conflict detection.
    """

    def __init__(self) -> None:
        self._config: Dict[str, Any] = {}
        self._doctrine_cache: Optional[DoctrineCacheIndex] = None
        self._search_index: Optional[EasementSearchIndex] = None
        self._telemetry: Optional[TelemetryCollector] = None
        self._start_time = time.time()
        self._request_count = 0

    def initialize(self) -> None:
        """Initialize all subsystems."""
        logger.info(f"Initializing {ENGINE_ID} {ENGINE_NAME} v{ENGINE_VERSION}")

        # Load config
        if CONFIG_PATH.exists():
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                self._config = json.load(f)
            logger.info(f"Config loaded from {CONFIG_PATH}")
        else:
            logger.warning(f"Config not found at {CONFIG_PATH}, using defaults")
            self._config = {}

        # Build doctrine cache
        self._doctrine_cache = build_doctrine_cache()
        logger.info(f"Doctrine cache: {self._doctrine_cache.size} blocks")

        # Build search index (empty initially, populated by ingestion)
        self._search_index = build_search_index()
        logger.info(f"Search index: {self._search_index.size} records")

        # Initialize telemetry
        self._telemetry = get_telemetry()
        logger.info("Telemetry collector initialized")

        logger.info(f"{ENGINE_ID} initialization complete")

    @property
    def config(self) -> Dict[str, Any]:
        return self._config

    @property
    def uptime_seconds(self) -> float:
        return time.time() - self._start_time

    # -----------------------------------------------------------------------
    # CORE ANALYSIS METHOD
    # -----------------------------------------------------------------------

    async def analyze(self, request: EasementQueryRequest) -> EasementQueryResponse:
        """
        Main analysis entry point. Routes to appropriate analysis
        depth based on response mode.
        """
        start = time.time()
        request_id = str(uuid.uuid4())
        self._request_count += 1
        session_id = request.session_id or ""
        telemetry = get_telemetry()

        logger.info(
            f"[{request_id}] Analyzing: mode={request.mode.value}, "
            f"query='{request.query[:80]}...'"
        )

        # Normalize query
        normalized_query = normalize_query(request.query)
        synonyms = resolve_synonyms(request.query)

        # Phase 1: Doctrine cache lookup
        layer1_start = time.time()
        matched_doctrines = self._doctrine_lookup(normalized_query, request.query)
        layer1_ms = (time.time() - layer1_start) * 1000

        for doc in matched_doctrines:
            telemetry.record_cache_access(doc.topic, True)

        # Phase 2: Semantic search over indexed records
        layer2_start = time.time()
        search_response = search_easements(
            query=normalized_query,
            easement_type=request.easement_type,
            county=request.county,
            state=request.state,
            grantor=request.grantor,
            grantee=request.grantee,
            pipeline_operator=request.pipeline_operator,
            limit=request.max_results,
        )
        layer2_ms = (time.time() - layer2_start) * 1000

        # Phase 3: Easement identification
        layer3_start = time.time()
        identifications = self._identify_easements(request.query, matched_doctrines)
        layer3_ms = (time.time() - layer3_start) * 1000

        # Phase 4: Deep analysis (mode-dependent)
        layer4_start = time.time()
        row_analysis = None
        accommodation_check = None
        surface_damage = None
        conflicts: List[EasementConflict] = []
        condemnation = None

        if request.mode in (ResponseMode.ANALYSIS, ResponseMode.MEMO, ResponseMode.ROW_REVIEW):
            row_analysis = self._analyze_row(request.query, identifications)

        if request.mode in (ResponseMode.ANALYSIS, ResponseMode.MEMO):
            accommodation_check = self._check_accommodation(request.query, identifications)
            conflicts = self._detect_conflicts(request.query, search_response)

        if request.mode == ResponseMode.CONDEMNATION_ANALYSIS:
            condemnation = self._analyze_condemnation(request.query, matched_doctrines)

        layer4_ms = (time.time() - layer4_start) * 1000

        # Build three-layer response
        layers = self._build_layers(
            request.mode,
            matched_doctrines,
            search_response,
            identifications,
            row_analysis,
            accommodation_check,
            conflicts,
            condemnation,
            layer1_ms,
            layer2_ms,
            layer3_ms + layer4_ms,
        )

        # Fact fragility scoring
        fact_fragility = self._score_fact_fragility(identifications, matched_doctrines)

        # Confidence stratification
        confidence = self._compute_confidence(
            matched_doctrines, search_response, identifications
        )

        # Build doctrine references
        doctrine_refs = []
        if request.include_doctrines:
            for doc in matched_doctrines:
                rel_score = doc.matches_query(normalized_query)
                doctrine_refs.append(EasementDoctrineRef(
                    topic=doc.topic,
                    summary=doc.summary[:500],
                    category=doc.category,
                    authority_score=doc.authority_score,
                    key_statutes=doc.key_statutes[:5] if request.include_statutes else [],
                    leading_cases=doc.leading_cases[:3],
                    relevance_score=rel_score,
                ))

        # Determinism hash
        total_ms = (time.time() - start) * 1000
        input_hash = hashlib.sha256(request.query.encode()).hexdigest()
        response_payload = json.dumps({
            "query": request.query,
            "mode": request.mode.value,
            "doctrine_count": len(matched_doctrines),
            "identification_count": len(identifications),
            "search_count": search_response.total_hits,
        }, sort_keys=True)
        determinism_hash = DeterminismHash(
            hash_value=hashlib.sha256(response_payload.encode()).hexdigest(),
            algorithm="sha256",
            input_hash=input_hash,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

        # Warnings
        warnings: List[str] = []
        if not matched_doctrines:
            warnings.append("No matching doctrine blocks found for this query")
        if search_response.total_hits == 0 and request.query:
            warnings.append("No indexed easement records matched the search criteria")
        if confidence == ConfidenceLevel.LOW:
            warnings.append("Low confidence analysis - recommend manual review")

        # Telemetry recording
        telemetry.record_request(
            endpoint="/analyze",
            latency_ms=total_ms,
            query=request.query,
            result_count=len(identifications),
            easement_type=request.easement_type or "",
            county=request.county or "",
            pipeline_operator=request.pipeline_operator or "",
            session_id=session_id,
        )

        # Record query pattern
        telemetry.patterns.record_query(
            query_text=request.query,
            easement_type=request.easement_type or "",
            county=request.county or "",
            pipeline_operator=request.pipeline_operator or "",
        )

        return EasementQueryResponse(
            request_id=request_id,
            mode=request.mode,
            timestamp=datetime.now(timezone.utc).isoformat(),
            layers=layers,
            easement_identifications=identifications,
            row_analysis=row_analysis,
            accommodation_check=accommodation_check,
            surface_damage=surface_damage,
            conflicts=conflicts,
            condemnation=condemnation,
            matched_doctrines=doctrine_refs,
            fact_fragility=fact_fragility,
            confidence=confidence,
            determinism_hash=determinism_hash,
            total_latency_ms=round(total_ms, 2),
            search_results_count=search_response.total_hits,
            warnings=warnings,
        )

    # -----------------------------------------------------------------------
    # DOCTRINE CACHE LOOKUP
    # -----------------------------------------------------------------------

    def _doctrine_lookup(
        self, normalized_query: str, raw_query: str
    ) -> List[DoctrineCacheBlock]:
        """Search doctrine cache for relevant blocks."""
        results = search_doctrines(normalized_query, top_k=10)

        # Also try synonym-resolved terms
        synonyms = resolve_synonyms(raw_query)
        for canonical_term in synonyms:
            block = get_doctrine_block(canonical_term)
            if block and block not in results:
                results.append(block)

        # Sort by relevance to query
        scored = [(b.matches_query(normalized_query), b) for b in results]
        scored.sort(key=lambda x: x[0], reverse=True)
        return [b for _, b in scored if _ > 0.0][:10]

    # -----------------------------------------------------------------------
    # EASEMENT IDENTIFICATION
    # -----------------------------------------------------------------------

    def _identify_easements(
        self,
        query: str,
        doctrines: List[DoctrineCacheBlock],
    ) -> List[EasementIdentification]:
        """Identify easement types and characteristics from query text."""
        identifications: List[EasementIdentification] = []
        query_lower = query.lower()

        # Check for express easement indicators
        express_indicators = [
            "grant of easement", "easement deed", "convey an easement",
            "grants unto", "right-of-way agreement", "pipeline easement",
        ]
        if any(ind in query_lower for ind in express_indicators):
            identifications.append(EasementIdentification(
                easement_type="express",
                classification_confidence=0.85,
                purpose="Express grant identified in instrument language",
                notes="Express easement created by written instrument",
            ))

        # Check for implied easement indicators
        implied_indicators = [
            "implied easement", "prior use", "quasi-easement",
            "existing at time of severance",
        ]
        if any(ind in query_lower for ind in implied_indicators):
            identifications.append(EasementIdentification(
                easement_type="implied_prior_use",
                classification_confidence=0.70,
                purpose="Implied easement by prior use indicated",
                notes="Requires apparent, continuous, reasonably necessary use at severance",
            ))

        # Check for necessity indicators
        necessity_indicators = [
            "landlocked", "no access", "necessity", "way of necessity",
            "no public road",
        ]
        if any(ind in query_lower for ind in necessity_indicators):
            identifications.append(EasementIdentification(
                easement_type="implied_necessity",
                classification_confidence=0.75,
                purpose="Access by necessity to landlocked parcel",
                notes="Requires strict necessity (no alternative access)",
            ))

        # Check for prescriptive indicators
        prescriptive_indicators = [
            "prescriptive", "adverse use", "ten years", "10 years",
            "open and notorious", "hostile use",
        ]
        if any(ind in query_lower for ind in prescriptive_indicators):
            identifications.append(EasementIdentification(
                easement_type="prescriptive",
                classification_confidence=0.65,
                purpose="Prescriptive easement by adverse use",
                notes="Requires 10 years open, notorious, hostile, continuous use in TX",
            ))

        # Check for pipeline ROW indicators
        pipeline_indicators = [
            "pipeline", "pipe line", "gathering line", "transmission line",
            "flowline", "row", "right-of-way", "pipeline easement",
        ]
        if any(ind in query_lower for ind in pipeline_indicators):
            # Determine type of pipeline
            width = 30.0  # default gathering
            depth = 36.0
            if "transmission" in query_lower or "trunk" in query_lower:
                width = 50.0
            elif "major" in query_lower or "trunk line" in query_lower:
                width = 75.0

            identifications.append(EasementIdentification(
                easement_type="pipeline_row",
                classification_confidence=0.80,
                purpose="Pipeline right-of-way for oil and gas operations",
                width_ft=width,
                depth_ft=depth,
                notes="T-4 permit required from RRC; cathodic protection required",
            ))

        # Check for road easement indicators
        road_indicators = [
            "road easement", "access road", "ingress and egress",
            "ingress/egress", "lease road", "oilfield road",
        ]
        if any(ind in query_lower for ind in road_indicators):
            identifications.append(EasementIdentification(
                easement_type="road",
                classification_confidence=0.80,
                purpose="Road access for ingress and egress",
                width_ft=30.0,
                notes="Typical oilfield road 20-40 ft; must accommodate heavy equipment",
            ))

        # Check for utility easement indicators
        utility_indicators = [
            "utility easement", "electric easement", "power line",
            "telephone", "fiber optic", "water line", "sewer",
        ]
        if any(ind in query_lower for ind in utility_indicators):
            identifications.append(EasementIdentification(
                easement_type="utility",
                classification_confidence=0.80,
                purpose="Utility infrastructure installation and maintenance",
                width_ft=20.0,
                notes="Typically easement in gross; may have condemnation authority",
            ))

        # Check for surface use agreement indicators
        sua_indicators = [
            "surface use agreement", "sua", "surface damage",
            "surface access", "surface occupancy",
        ]
        if any(ind in query_lower for ind in sua_indicators):
            identifications.append(EasementIdentification(
                easement_type="surface_use",
                classification_confidence=0.80,
                purpose="Surface use agreement governing operator's surface activities",
                notes="Governs pad sites, roads, water sources, restoration per Tex. NRC Ch. 52",
            ))

        # Check for conservation easement indicators
        conservation_indicators = [
            "conservation easement", "preservation", "scenic easement",
            "land trust",
        ]
        if any(ind in query_lower for ind in conservation_indicators):
            identifications.append(EasementIdentification(
                easement_type="conservation",
                classification_confidence=0.80,
                purpose="Conservation restriction protecting natural or agricultural values",
                duration="perpetual",
                notes="Tax benefits under IRC \xA7170(h); may conflict with mineral development",
            ))

        # Check for condemnation indicators
        condemnation_indicators = [
            "condemnation", "eminent domain", "taking", "condemn",
        ]
        if any(ind in query_lower for ind in condemnation_indicators):
            identifications.append(EasementIdentification(
                easement_type="express",
                classification_confidence=0.70,
                purpose="Easement by condemnation (eminent domain)",
                notes="Requires common carrier status (Denbury test); just compensation required",
            ))

        # If no specific type identified, check doctrines
        if not identifications and doctrines:
            top_doctrine = doctrines[0]
            identifications.append(EasementIdentification(
                easement_type="unknown",
                classification_confidence=0.40,
                purpose=f"Analysis based on doctrine: {top_doctrine.topic}",
                notes=f"Category: {top_doctrine.category}",
            ))

        return identifications

    # -----------------------------------------------------------------------
    # ROW WIDTH/DEPTH ANALYSIS
    # -----------------------------------------------------------------------

    def _analyze_row(
        self,
        query: str,
        identifications: List[EasementIdentification],
    ) -> Optional[ROWAnalysis]:
        """Analyze ROW width, depth, and engineering parameters."""
        query_lower = query.lower()

        # Determine pipeline type and parameters
        pipe_specs = self._config.get("pipeline_specifications", {})
        txdot = self._config.get("txdot_standards", {})

        # Default to gathering line parameters
        diameter = 6.0
        product = "natural_gas"
        pressure = 300.0
        perm_width = 30.0
        temp_ws = 25.0
        depth = 36.0

        if "transmission" in query_lower:
            diameter = 16.0
            perm_width = 50.0
            temp_ws = 50.0
            product = "natural_gas"
            pressure = 800.0
        elif "product" in query_lower or "crude" in query_lower or "oil" in query_lower:
            diameter = 10.0
            perm_width = 40.0
            temp_ws = 30.0
            product = "crude_oil"
            pressure = 500.0
        elif "water" in query_lower or "swd" in query_lower or "produced" in query_lower:
            diameter = 8.0
            perm_width = 25.0
            temp_ws = 25.0
            product = "produced_water"
            pressure = 200.0

        # Override with identification data
        for ident in identifications:
            if ident.width_ft and ident.width_ft > 0:
                perm_width = ident.width_ft
            if ident.depth_ft and ident.depth_ft > 0:
                depth = ident.depth_ft

        crosses_highway = "highway" in query_lower or "txdot" in query_lower
        crosses_railroad = "railroad" in query_lower or "rail" in query_lower
        crosses_waterway = "river" in query_lower or "creek" in query_lower or "waterway" in query_lower

        road_depth = txdot.get("minimum_depth_under_highway_ft", 48)
        rail_depth = txdot.get("minimum_depth_under_railroad_ft", 60)
        water_depth = 60

        compliance_notes: List[str] = [
            f"RRC T-4 permit required for intrastate pipeline construction",
            f"Minimum depth of cover: {depth} ft per 49 CFR 192.327/195.248",
            f"Pipeline markers required at crossings, fences, and every 660 ft",
            f"Cathodic protection monitoring required annually",
        ]

        if crosses_highway:
            compliance_notes.append(
                f"TxDOT Form 1082 required for highway crossing; min depth {road_depth} ft; casing required"
            )
        if crosses_railroad:
            compliance_notes.append(
                f"Railroad crossing requires minimum {rail_depth} ft depth and casing"
            )
        if crosses_waterway:
            compliance_notes.append(
                f"Waterway crossing requires minimum {water_depth} ft depth; HDD recommended"
            )

        return ROWAnalysis(
            permanent_row_width_ft=perm_width,
            temp_workspace_ft=temp_ws,
            depth_of_cover_ft=depth,
            pipe_diameter_inches=diameter,
            product_type=product,
            road_crossing_depth_ft=road_depth,
            waterway_crossing_depth_ft=water_depth,
            casing_required=crosses_highway or crosses_railroad,
            hdd_recommended=crosses_highway or crosses_waterway,
            rrc_permit_required=True,
            txdot_permit_required=crosses_highway,
            compliance_notes=compliance_notes,
        )

    # -----------------------------------------------------------------------
    # ACCOMMODATION DOCTRINE CHECK
    # -----------------------------------------------------------------------

    def _check_accommodation(
        self,
        query: str,
        identifications: List[EasementIdentification],
    ) -> Optional[AccommodationDoctrineCheck]:
        """Check accommodation doctrine compliance."""
        query_lower = query.lower()

        # Look for accommodation-related terms
        accommodation_terms = [
            "accommodation", "surface use", "surface owner",
            "alternative methods", "due regard", "existing use",
            "crop", "cattle", "ranching", "farming", "irrigation",
        ]

        if not any(term in query_lower for term in accommodation_terms):
            return None

        # Identify existing surface use
        surface_uses = []
        if "cattle" in query_lower or "ranching" in query_lower or "livestock" in query_lower:
            surface_uses.append("ranching/livestock operations")
        if "crop" in query_lower or "farming" in query_lower or "agriculture" in query_lower:
            surface_uses.append("agricultural/crop production")
        if "irrigation" in query_lower:
            surface_uses.append("irrigation systems")
        if "residence" in query_lower or "home" in query_lower:
            surface_uses.append("residential use")
        if not surface_uses:
            surface_uses.append("general surface use")

        existing_use = "; ".join(surface_uses)

        # Identify mineral operations
        mineral_ops = []
        for ident in identifications:
            if ident.easement_type in ("pipeline_row", "surface_use"):
                mineral_ops.append(ident.purpose)
        if not mineral_ops:
            mineral_ops.append("oil and gas operations (unspecified)")

        ops_description = "; ".join(mineral_ops)

        # Assess impairment
        risk_factors: List[str] = []
        recommendations: List[str] = []

        if "cattle" in query_lower and "pipeline" in query_lower:
            risk_factors.append("Pipeline construction may disrupt grazing patterns and fencing")
            recommendations.append("Install temporary fencing during construction; restore permanent fencing promptly")
            recommendations.append("Route pipeline along existing fence lines where possible")

        if "crop" in query_lower:
            risk_factors.append("Pipeline trenching will destroy crops in the construction corridor")
            recommendations.append("Schedule construction outside growing season if possible")
            recommendations.append("Compensate for crop loss per Tex. NRC Ch. 52")

        if "irrigation" in query_lower:
            risk_factors.append("Pipeline may intersect with irrigation infrastructure")
            recommendations.append("HDD under irrigation lines and ditches")
            recommendations.append("Coordinate timing with irrigation schedule")

        if "water" in query_lower or "well" in query_lower:
            risk_factors.append("Operations may affect groundwater supply (Merriman v. XTO Energy)")
            recommendations.append("Test water quality before and after operations")
            recommendations.append("Provide alternative water source if existing supply affected")

        # Determine compliance status
        alternatives_available = "alternative" in query_lower or len(recommendations) > 0
        if risk_factors and not alternatives_available:
            compliance_status = "at_risk"
            confidence = ConfidenceLevel.MEDIUM
        elif risk_factors and alternatives_available:
            compliance_status = "compliant"
            confidence = ConfidenceLevel.MEDIUM
        else:
            compliance_status = "compliant"
            confidence = ConfidenceLevel.HIGH

        risk_factors.append(
            "Getty Oil v. Jones (1971): mineral estate must accommodate existing surface uses "
            "when reasonable alternatives exist"
        )
        risk_factors.append(
            "Merriman v. XTO Energy (2013): accommodation doctrine extends to groundwater protection"
        )

        return AccommodationDoctrineCheck(
            existing_surface_use=existing_use,
            mineral_operations_description=ops_description,
            impairment_assessment=(
                f"Identified {len(risk_factors)} risk factors affecting existing surface use. "
                f"{'Alternatives available.' if alternatives_available else 'No alternatives identified.'}"
            ),
            alternative_methods_available=alternatives_available,
            alternatives_description="; ".join(recommendations[:3]) if recommendations else "",
            compliance_status=compliance_status,
            risk_factors=risk_factors,
            recommendations=recommendations,
            confidence=confidence,
        )

    # -----------------------------------------------------------------------
    # CONFLICT DETECTION
    # -----------------------------------------------------------------------

    def _detect_conflicts(
        self,
        query: str,
        search_response: SearchResponse,
    ) -> List[EasementConflict]:
        """Detect potential conflicts between easements."""
        conflicts: List[EasementConflict] = []
        query_lower = query.lower()

        # Look for explicit conflict indicators
        conflict_terms = [
            "conflict", "overlap", "interfere", "competing",
            "crossing", "intersection", "incompatible",
        ]

        if any(term in query_lower for term in conflict_terms):
            conflicts.append(EasementConflict(
                conflict_type="potential_overlap",
                easement_a="proposed easement",
                easement_b="existing easement(s) in area",
                description=(
                    "Potential conflict detected based on query context. "
                    "A full title search and easement plat review is recommended "
                    "to identify all existing encumbrances."
                ),
                severity="medium",
                resolution_options=[
                    "Conduct full title search to identify all existing easements",
                    "Prepare easement plat showing all corridors with dimensions",
                    "Negotiate crossing agreements with existing easement holders",
                    "Evaluate alternative route to avoid conflicts",
                    "Obtain subordination agreements where appropriate",
                ],
                priority_analysis=(
                    "First in time, first in right. Recorded easements take priority "
                    "over later recorded or unrecorded easements among BFPs."
                ),
            ))

        # Check for pipeline crossing conflicts
        if "pipeline" in query_lower and ("cross" in query_lower or "intersection" in query_lower):
            conflicts.append(EasementConflict(
                conflict_type="pipeline_crossing",
                easement_a="proposed pipeline",
                easement_b="existing pipeline or utility",
                description=(
                    "Pipeline crossings require crossing agreements between operators. "
                    "The crossing must maintain minimum separation distances and "
                    "depth of cover requirements."
                ),
                severity="medium",
                resolution_options=[
                    "Execute crossing agreement between pipeline operators",
                    "Install casing at crossing point",
                    "Maintain minimum 12-inch vertical separation at crossing",
                    "Notify both operators of crossing location and depth",
                    "Mark crossing with above-ground markers per RRC requirements",
                ],
                priority_analysis=(
                    "Prior pipeline has priority. Crossing pipeline must accommodate "
                    "existing pipeline and bear cost of protective measures."
                ),
            ))

        # Check for utility vs pipeline conflicts
        if ("utility" in query_lower or "electric" in query_lower or "power" in query_lower) and (
            "pipeline" in query_lower
        ):
            conflicts.append(EasementConflict(
                conflict_type="utility_pipeline_proximity",
                easement_a="utility easement",
                easement_b="pipeline easement",
                description=(
                    "Utility and pipeline easements in close proximity require "
                    "coordination to prevent interference. Cathodic protection "
                    "systems on pipelines may be affected by AC power lines."
                ),
                severity="medium",
                resolution_options=[
                    "Maintain minimum horizontal separation per NESC standards",
                    "Evaluate AC interference effects on cathodic protection",
                    "Install mitigation measures for AC interference if needed",
                    "Execute proximity agreement between utility and pipeline operator",
                ],
                priority_analysis="Per Marcus Cable v. Krohn, each easement is limited to its granted scope.",
            ))

        return conflicts

    # -----------------------------------------------------------------------
    # CONDEMNATION ANALYSIS
    # -----------------------------------------------------------------------

    def _analyze_condemnation(
        self,
        query: str,
        doctrines: List[DoctrineCacheBlock],
    ) -> Optional[CondemnationTracker]:
        """Analyze eminent domain / condemnation proceeding."""
        query_lower = query.lower()

        condemnation_terms = [
            "condemnation", "eminent domain", "condemn", "taking",
            "common carrier", "just compensation",
        ]

        if not any(term in query_lower for term in condemnation_terms):
            return None

        # Extract condemner if mentioned
        condemner = "Unknown Pipeline Company"
        for canonical, aliases in OPERATOR_ALIAS_MAP.items():
            for alias in aliases:
                if alias.lower() in query_lower:
                    condemner = canonical
                    break

        # Denbury test analysis
        denbury_analysis = (
            "Under Denbury Green Pipeline-Texas LLC v. Texas Rice Land Partners Ltd. "
            "(Tex. 2017), a pipeline company must prove it is a bona fide common carrier "
            "serving the public, not merely transporting its own product. The company "
            "must demonstrate: (1) reasonable probability that capacity will be available "
            "to third parties, (2) willingness to transport for the public at published "
            "tariffs, and (3) the pipeline is not exclusively for the company's own "
            "production. Common carrier status under Tex. NRC \xA7111.002 is necessary "
            "but not sufficient -- actual common carrier operations must be shown."
        )

        return CondemnationTracker(
            condemner=condemner,
            condemnee="Surface Owner (unspecified)",
            property_description="Pipeline right-of-way across private property",
            common_carrier_status="unverified",
            denbury_test_analysis=denbury_analysis,
            just_compensation_estimate=0.0,
            severance_damages_estimate=0.0,
            proceeding_status="analysis",
            key_dates={
                "analysis_date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            },
            statutory_basis=[
                "Tex. Nat. Res. Code \xA7111.001 et seq.",
                "Tex. Prop. Code Ch. 21",
                "U.S. Const. Amend. V",
                "Tex. Const. Art. I, \xA717",
            ],
        )

    # -----------------------------------------------------------------------
    # THREE-LAYER RESPONSE BUILDER
    # -----------------------------------------------------------------------

    def _build_layers(
        self,
        mode: ResponseMode,
        doctrines: List[DoctrineCacheBlock],
        search_response: SearchResponse,
        identifications: List[EasementIdentification],
        row_analysis: Optional[ROWAnalysis],
        accommodation_check: Optional[AccommodationDoctrineCheck],
        conflicts: List[EasementConflict],
        condemnation: Optional[CondemnationTracker],
        layer1_ms: float,
        layer2_ms: float,
        layer3_ms: float,
    ) -> List[EasementAnalysisLayer]:
        """Build the three-layer response based on mode."""
        layers: List[EasementAnalysisLayer] = []

        # Layer 1: Doctrine cache (always present)
        if doctrines:
            doc_summary = "; ".join(
                f"{d.topic}: {d.summary[:120]}" for d in doctrines[:3]
            )
            citations = []
            for d in doctrines[:5]:
                citations.extend(d.key_statutes[:2])
                citations.extend(d.leading_cases[:1])
            citations = list(dict.fromkeys(citations))[:10]  # deduplicate, limit
        else:
            doc_summary = "No directly matching doctrine blocks found."
            citations = []

        layers.append(EasementAnalysisLayer(
            layer_name="Doctrine Cache",
            content=doc_summary,
            confidence=ConfidenceLevel.HIGH if doctrines else ConfidenceLevel.LOW,
            citations=citations,
            latency_ms=round(layer1_ms, 2),
        ))

        # Layer 2: Semantic search results
        if search_response.total_hits > 0:
            search_summary = (
                f"Found {search_response.total_hits} matching easement records. "
                f"Top results span {len(search_response.facets.get('county', {}))} counties "
                f"and {len(search_response.facets.get('easement_type', {}))} easement types."
            )
        else:
            search_summary = "No indexed easement records matched the query."

        layers.append(EasementAnalysisLayer(
            layer_name="Semantic Search",
            content=search_summary,
            confidence=(
                ConfidenceLevel.HIGH if search_response.total_hits > 5
                else ConfidenceLevel.MEDIUM if search_response.total_hits > 0
                else ConfidenceLevel.LOW
            ),
            citations=[],
            latency_ms=round(layer2_ms, 2),
        ))

        # Layer 3: Analysis (varies by mode)
        if mode == ResponseMode.FAST:
            analysis_content = self._fast_analysis(identifications, doctrines)
        elif mode == ResponseMode.ANALYSIS:
            analysis_content = self._standard_analysis(
                identifications, doctrines, row_analysis, accommodation_check, conflicts
            )
        elif mode == ResponseMode.MEMO:
            analysis_content = self._memo_analysis(
                identifications, doctrines, row_analysis, accommodation_check, conflicts
            )
        elif mode == ResponseMode.ROW_REVIEW:
            analysis_content = self._row_review_analysis(identifications, row_analysis)
        elif mode == ResponseMode.CONDEMNATION_ANALYSIS:
            analysis_content = self._condemnation_layer(condemnation, doctrines)
        else:
            analysis_content = "Analysis mode not recognized."

        layers.append(EasementAnalysisLayer(
            layer_name="Deep Analysis",
            content=analysis_content,
            confidence=ConfidenceLevel.MEDIUM,
            citations=citations[:5],
            latency_ms=round(layer3_ms, 2),
        ))

        return layers

    def _fast_analysis(
        self,
        identifications: List[EasementIdentification],
        doctrines: List[DoctrineCacheBlock],
    ) -> str:
        """Build fast mode analysis content."""
        parts: List[str] = []
        if identifications:
            for ident in identifications[:3]:
                parts.append(
                    f"Identified {ident.easement_type} easement "
                    f"(confidence: {ident.classification_confidence:.0%}): "
                    f"{ident.purpose}"
                )
        if doctrines:
            parts.append(f"Top doctrine: {doctrines[0].topic} ({doctrines[0].category})")
        return " | ".join(parts) if parts else "Insufficient data for fast analysis."

    def _standard_analysis(
        self,
        identifications: List[EasementIdentification],
        doctrines: List[DoctrineCacheBlock],
        row_analysis: Optional[ROWAnalysis],
        accommodation_check: Optional[AccommodationDoctrineCheck],
        conflicts: List[EasementConflict],
    ) -> str:
        """Build standard analysis content."""
        sections: List[str] = []

        # Identification summary
        if identifications:
            ident_lines = []
            for i, ident in enumerate(identifications, 1):
                ident_lines.append(
                    f"{i}. {ident.easement_type.upper()} "
                    f"(confidence: {ident.classification_confidence:.0%}) - {ident.purpose}"
                )
                if ident.width_ft:
                    ident_lines.append(f"   Width: {ident.width_ft} ft")
                if ident.depth_ft:
                    ident_lines.append(f"   Depth: {ident.depth_ft} ft")
                if ident.notes:
                    ident_lines.append(f"   Note: {ident.notes}")
            sections.append("EASEMENT IDENTIFICATION:\n" + "\n".join(ident_lines))

        # ROW analysis
        if row_analysis:
            sections.append(
                f"ROW ANALYSIS: Permanent width {row_analysis.permanent_row_width_ft} ft, "
                f"temp workspace {row_analysis.temp_workspace_ft} ft, "
                f"depth of cover {row_analysis.depth_of_cover_ft} ft. "
                f"RRC permit: {'required' if row_analysis.rrc_permit_required else 'not required'}. "
                f"TxDOT permit: {'required' if row_analysis.txdot_permit_required else 'not required'}."
            )

        # Accommodation check
        if accommodation_check:
            sections.append(
                f"ACCOMMODATION DOCTRINE: Status={accommodation_check.compliance_status.upper()}. "
                f"Existing use: {accommodation_check.existing_surface_use}. "
                f"Risk factors: {len(accommodation_check.risk_factors)}."
            )

        # Conflicts
        if conflicts:
            conflict_lines = [
                f"- {c.conflict_type}: {c.description[:100]}" for c in conflicts[:3]
            ]
            sections.append("CONFLICTS DETECTED:\n" + "\n".join(conflict_lines))

        # Doctrines
        if doctrines:
            doc_lines = [
                f"- {d.topic} ({d.category}): {d.summary[:100]}" for d in doctrines[:5]
            ]
            sections.append("APPLICABLE DOCTRINES:\n" + "\n".join(doc_lines))

        return "\n\n".join(sections) if sections else "Insufficient data for standard analysis."

    def _memo_analysis(
        self,
        identifications: List[EasementIdentification],
        doctrines: List[DoctrineCacheBlock],
        row_analysis: Optional[ROWAnalysis],
        accommodation_check: Optional[AccommodationDoctrineCheck],
        conflicts: List[EasementConflict],
    ) -> str:
        """Build memo mode analysis (most comprehensive)."""
        standard = self._standard_analysis(
            identifications, doctrines, row_analysis, accommodation_check, conflicts
        )

        # Add detailed doctrine analysis
        doctrine_detail: List[str] = []
        for d in doctrines[:5]:
            detail = (
                f"DOCTRINE: {d.topic}\n"
                f"Category: {d.category} | Subcategory: {d.subcategory}\n"
                f"Summary: {d.summary}\n"
                f"Key Statutes: {'; '.join(d.key_statutes)}\n"
                f"Elements: {'; '.join(d.elements[:5])}\n"
                f"Defenses: {'; '.join(d.defenses[:3])}\n"
                f"Remedies: {'; '.join(d.remedies[:3])}\n"
                f"Leading Cases: {'; '.join(d.leading_cases[:3])}"
            )
            doctrine_detail.append(detail)

        full_doctrines = "\n\n".join(doctrine_detail) if doctrine_detail else ""

        return f"{standard}\n\n--- DETAILED DOCTRINE ANALYSIS ---\n\n{full_doctrines}"

    def _row_review_analysis(
        self,
        identifications: List[EasementIdentification],
        row_analysis: Optional[ROWAnalysis],
    ) -> str:
        """Build ROW review analysis."""
        if not row_analysis:
            return "Insufficient data for ROW review."

        parts = [
            f"PIPELINE ROW REVIEW",
            f"Permanent Width: {row_analysis.permanent_row_width_ft} ft",
            f"Temporary Workspace: {row_analysis.temp_workspace_ft} ft",
            f"Depth of Cover: {row_analysis.depth_of_cover_ft} ft",
            f"Pipe Diameter: {row_analysis.pipe_diameter_inches} inches",
            f"Product Type: {row_analysis.product_type}",
            f"Road Crossing Depth: {row_analysis.road_crossing_depth_ft} ft",
            f"Waterway Crossing Depth: {row_analysis.waterway_crossing_depth_ft} ft",
            f"Casing Required: {'Yes' if row_analysis.casing_required else 'No'}",
            f"HDD Recommended: {'Yes' if row_analysis.hdd_recommended else 'No'}",
            f"RRC Permit Required: {'Yes' if row_analysis.rrc_permit_required else 'No'}",
            f"TxDOT Permit Required: {'Yes' if row_analysis.txdot_permit_required else 'No'}",
            "",
            "COMPLIANCE NOTES:",
        ]
        for note in row_analysis.compliance_notes:
            parts.append(f"  - {note}")

        return "\n".join(parts)

    def _condemnation_layer(
        self,
        condemnation: Optional[CondemnationTracker],
        doctrines: List[DoctrineCacheBlock],
    ) -> str:
        """Build condemnation analysis layer."""
        if not condemnation:
            return "No condemnation indicators found in query."

        parts = [
            f"CONDEMNATION / EMINENT DOMAIN ANALYSIS",
            f"Condemner: {condemnation.condemner}",
            f"Common Carrier Status: {condemnation.common_carrier_status.upper()}",
            f"",
            f"DENBURY TEST ANALYSIS:",
            condemnation.denbury_test_analysis,
            f"",
            f"STATUTORY BASIS:",
        ]
        for statute in condemnation.statutory_basis:
            parts.append(f"  - {statute}")

        if doctrines:
            parts.append("")
            parts.append("RELEVANT DOCTRINES:")
            for d in doctrines[:5]:
                parts.append(f"  - {d.topic}: {d.summary[:120]}")

        return "\n".join(parts)

    # -----------------------------------------------------------------------
    # FACT FRAGILITY SCORING
    # -----------------------------------------------------------------------

    def _score_fact_fragility(
        self,
        identifications: List[EasementIdentification],
        doctrines: List[DoctrineCacheBlock],
    ) -> List[FactFragilityScore]:
        """Score fragility of key findings."""
        scores: List[FactFragilityScore] = []

        for ident in identifications:
            risk_factors: List[str] = []
            fragility = 1.0 - ident.classification_confidence

            if ident.easement_type == "prescriptive":
                risk_factors.append("Prescriptive easement claims require extensive factual proof")
                risk_factors.append("Permissive use defense can defeat prescriptive claim entirely")
                fragility = max(fragility, 0.6)

            if ident.easement_type in ("implied_prior_use", "implied_necessity"):
                risk_factors.append("Implied easements depend on factual circumstances at severance")
                risk_factors.append("Express deed language may negate implied easement")
                fragility = max(fragility, 0.5)

            if ident.easement_type == "express":
                risk_factors.append("Express easement validity depends on compliance with Statute of Frauds")
                if ident.classification_confidence >= 0.8:
                    fragility = min(fragility, 0.3)

            if not risk_factors:
                risk_factors.append("Classification based on keyword analysis; instrument review required")

            scores.append(FactFragilityScore(
                claim=f"{ident.easement_type} easement: {ident.purpose[:80]}",
                fragility_score=round(fragility, 2),
                risk_factors=risk_factors,
                mitigation=(
                    "Verify classification against actual recorded instrument language "
                    "and applicable deed records."
                ),
            ))

        return scores

    # -----------------------------------------------------------------------
    # CONFIDENCE STRATIFICATION
    # -----------------------------------------------------------------------

    def _compute_confidence(
        self,
        doctrines: List[DoctrineCacheBlock],
        search_response: SearchResponse,
        identifications: List[EasementIdentification],
    ) -> ConfidenceLevel:
        """Compute overall confidence level for the analysis."""
        signals: List[float] = []

        # Doctrine match quality
        if doctrines:
            avg_authority = sum(d.authority_score for d in doctrines) / len(doctrines)
            signals.append(avg_authority)
        else:
            signals.append(0.2)

        # Search result quality
        if search_response.total_hits > 10:
            signals.append(0.9)
        elif search_response.total_hits > 3:
            signals.append(0.7)
        elif search_response.total_hits > 0:
            signals.append(0.5)
        else:
            signals.append(0.2)

        # Identification confidence
        if identifications:
            avg_conf = sum(i.classification_confidence for i in identifications) / len(identifications)
            signals.append(avg_conf)
        else:
            signals.append(0.2)

        overall = sum(signals) / len(signals)

        if overall >= 0.75:
            return ConfidenceLevel.HIGH
        elif overall >= 0.50:
            return ConfidenceLevel.MEDIUM
        elif overall >= 0.30:
            return ConfidenceLevel.LOW
        else:
            return ConfidenceLevel.UNCERTAIN

    # -----------------------------------------------------------------------
    # SURFACE DAMAGE CALCULATION
    # -----------------------------------------------------------------------

    def calculate_surface_damage(self, request: SurfaceDamageRequest) -> SurfaceDamageCalculation:
        """Calculate surface damage compensation estimate."""
        # Texas ranges: $500-2000/acre for crop damage, $15-50/ft for fence
        crop_damage = 0.0
        if request.crop_type:
            # Estimate based on Permian Basin crop values
            crop_rates = {
                "cotton": 800.0,
                "hay": 400.0,
                "wheat": 500.0,
                "sorghum": 450.0,
                "pecans": 1500.0,
                "improved_pasture": 300.0,
                "native_grass": 150.0,
            }
            rate = crop_rates.get(request.crop_type.lower(), 500.0)
            crop_damage = request.acreage_affected * rate

        fence_repair = 0.0
        road_damage = 0.0
        for improvement in request.existing_improvements:
            imp_lower = improvement.lower()
            if "fence" in imp_lower:
                # Estimate 660 ft per acre of perimeter
                fence_repair += request.acreage_affected * 660 * 25  # $25/ft replacement
            if "road" in imp_lower:
                road_damage += request.acreage_affected * 5000  # $5000/acre for road repair
            if "well" in imp_lower or "water" in imp_lower:
                road_damage += 15000  # Water well replacement estimate

        # Restoration cost
        restoration = request.acreage_affected * 2000  # $2000/acre restoration estimate

        total = crop_damage + fence_repair + road_damage + restoration

        notice_required = not request.surface_owner_is_mineral_owner

        return SurfaceDamageCalculation(
            damage_type=request.operation_type or "oil and gas operations",
            acreage_affected=request.acreage_affected,
            crop_damage_estimate=round(crop_damage, 2),
            fence_repair_estimate=round(fence_repair, 2),
            road_damage_estimate=round(road_damage, 2),
            water_source_impact="Assess impact on groundwater wells within 1/4 mile radius",
            restoration_cost_estimate=round(restoration, 2),
            total_estimated_damage=round(total, 2),
            notice_required=notice_required,
            notice_period_days=30 if notice_required else 0,
            statutory_basis="Tex. Nat. Res. Code Ch. 52" if notice_required else "N/A (common ownership)",
            notes=(
                f"Estimates based on Permian Basin averages. Actual damages should be "
                f"determined by qualified appraiser. Duration: {request.duration_days} days."
            ),
        )

    # -----------------------------------------------------------------------
    # ROW REVIEW (STANDALONE)
    # -----------------------------------------------------------------------

    def review_row(self, request: ROWReviewRequest) -> ROWAnalysis:
        """Standalone ROW review from structured parameters."""
        # Determine width based on diameter and product
        if request.pipe_diameter_inches <= 12:
            perm_width = request.proposed_width_ft or 30.0
            temp_ws = 25.0
        elif request.pipe_diameter_inches <= 24:
            perm_width = request.proposed_width_ft or 50.0
            temp_ws = 40.0
        else:
            perm_width = request.proposed_width_ft or 75.0
            temp_ws = 50.0

        if request.existing_easement_width_ft and request.existing_easement_width_ft > 0:
            if request.existing_easement_width_ft < perm_width:
                logger.warning(
                    f"Existing easement width ({request.existing_easement_width_ft} ft) "
                    f"is less than recommended ({perm_width} ft)"
                )

        depth = 36.0
        road_depth = 48.0
        rail_depth = 60.0
        water_depth = 60.0

        compliance_notes: List[str] = [
            f"Pipeline: {request.pipe_diameter_inches} inch {request.product_type} "
            f"at {request.operating_pressure_psi} psi",
            f"Length: {request.length_miles} miles",
            f"Permanent ROW: {perm_width} ft; Temp workspace: {temp_ws} ft",
            f"Minimum depth of cover: {depth} ft",
            "RRC T-4 permit required before construction",
            "Cathodic protection required",
            "Pipeline markers at all crossings and every 660 ft",
        ]

        if request.crosses_highway:
            compliance_notes.append(f"TxDOT Form 1082 for highway crossing; min {road_depth} ft depth; casing required")
        if request.crosses_railroad:
            compliance_notes.append(f"Railroad crossing: min {rail_depth} ft depth; casing required; railroad agreement needed")
        if request.crosses_waterway:
            compliance_notes.append(f"Waterway crossing: min {water_depth} ft depth; HDD recommended; USACE 404 permit may be required")

        if request.county:
            is_permian = request.county.lower() in TEXAS_PERMIAN_COUNTIES
            if is_permian:
                compliance_notes.append(f"Permian Basin county ({request.county}): high density pipeline corridor")

        return ROWAnalysis(
            permanent_row_width_ft=perm_width,
            temp_workspace_ft=temp_ws,
            depth_of_cover_ft=depth,
            pipe_diameter_inches=request.pipe_diameter_inches,
            product_type=request.product_type,
            road_crossing_depth_ft=road_depth,
            waterway_crossing_depth_ft=water_depth,
            casing_required=request.crosses_highway or request.crosses_railroad,
            hdd_recommended=request.crosses_highway or request.crosses_waterway,
            rrc_permit_required=True,
            txdot_permit_required=request.crosses_highway,
            compliance_notes=compliance_notes,
        )


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

analyzer = EasementAnalyzer()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown lifecycle."""
    logger.info(f"Starting {ENGINE_ID} {ENGINE_NAME} v{ENGINE_VERSION} on port {ENGINE_PORT}")
    analyzer.initialize()
    yield
    logger.info(f"Shutting down {ENGINE_ID}")
    telemetry_inst = get_telemetry()
    telemetry_inst.flush()


app = FastAPI(
    title=f"ECHO OMEGA PRIME - {ENGINE_ID} {ENGINE_NAME}",
    description=(
        "Production-grade easement analysis engine for oil and gas operations. "
        "Analyzes easements, rights-of-way, surface use agreements, pipeline corridors, "
        "accommodation doctrine compliance, surface damage, and eminent domain."
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

@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint (TIE component 12)."""
    return HealthResponse(
        status="operational",
        timestamp=datetime.now(timezone.utc).isoformat(),
        uptime_seconds=round(analyzer.uptime_seconds, 1),
        doctrine_cache=doctrine_cache_health(),
        search_index=search_index_health(),
        telemetry=telemetry_health(),
        semantic=semantic_health(),
    )


@app.post("/analyze", response_model=EasementQueryResponse)
async def analyze_easement(request: EasementQueryRequest) -> EasementQueryResponse:
    """
    Main analysis endpoint. Accepts a free-text query about easements,
    ROW, surface use, or condemnation and returns a structured analysis.
    """
    try:
        return await analyzer.analyze(request)
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        telemetry_inst = get_telemetry()
        telemetry_inst.errors.record_error(type(e).__name__, str(e), "/analyze")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/search")
async def search_endpoint(request: SearchRequest) -> Dict[str, Any]:
    """Direct search endpoint over indexed easement records."""
    start = time.time()
    try:
        sort_field = SortField(request.sort_by)
    except ValueError:
        sort_field = SortField.RELEVANCE
    try:
        sort_order = SortOrder(request.sort_order)
    except ValueError:
        sort_order = SortOrder.DESC

    etype = None
    if request.easement_type:
        try:
            etype = EasementType(request.easement_type)
        except ValueError:
            pass

    sq = SearchQuery(
        query=request.query,
        easement_type=etype,
        county=request.county,
        state=request.state,
        grantor=request.grantor,
        grantee=request.grantee,
        pipeline_operator=request.pipeline_operator,
        min_width_ft=request.min_width_ft,
        max_width_ft=request.max_width_ft,
        min_depth_ft=request.min_depth_ft,
        max_depth_ft=request.max_depth_ft,
        limit=request.limit,
        offset=request.offset,
        sort_by=sort_field,
        sort_order=sort_order,
    )

    response = get_search_index().search(sq)
    elapsed = (time.time() - start) * 1000
    get_telemetry().record_request("/search", elapsed, request.query, response.total_hits)
    return response.to_dict()


@app.post("/row-review")
async def row_review_endpoint(request: ROWReviewRequest) -> Dict[str, Any]:
    """Pipeline ROW review with engineering parameters."""
    start = time.time()
    result = analyzer.review_row(request)
    elapsed = (time.time() - start) * 1000
    get_telemetry().record_request("/row-review", elapsed)
    return result.model_dump()


@app.post("/accommodation-check")
async def accommodation_check_endpoint(request: AccommodationCheckRequest) -> Dict[str, Any]:
    """Accommodation doctrine compliance check."""
    start = time.time()

    # Build a query to feed through the analyzer
    query = (
        f"Accommodation doctrine analysis: {request.existing_surface_use} vs "
        f"{request.proposed_mineral_operations}"
    )
    eq = EasementQueryRequest(
        query=query,
        mode=ResponseMode.ANALYSIS,
        county=request.county or None,
    )
    response = await analyzer.analyze(eq)
    elapsed = (time.time() - start) * 1000
    get_telemetry().record_request("/accommodation-check", elapsed)

    result = response.accommodation_check
    if result:
        return result.model_dump()
    return {"status": "no_accommodation_issues_detected", "confidence": "low"}


@app.post("/surface-damage")
async def surface_damage_endpoint(request: SurfaceDamageRequest) -> Dict[str, Any]:
    """Surface damage calculation."""
    start = time.time()
    result = analyzer.calculate_surface_damage(request)
    elapsed = (time.time() - start) * 1000
    get_telemetry().record_request("/surface-damage", elapsed)
    return result.model_dump()


@app.post("/conflict-check")
async def conflict_check_endpoint(request: ConflictCheckRequest) -> Dict[str, Any]:
    """Easement conflict detection."""
    start = time.time()
    query = f"Easement conflict check: {request.proposed_easement_type} {request.proposed_route_description}"
    eq = EasementQueryRequest(
        query=query,
        mode=ResponseMode.ANALYSIS,
        county=request.county or None,
    )
    response = await analyzer.analyze(eq)
    elapsed = (time.time() - start) * 1000
    get_telemetry().record_request("/conflict-check", elapsed)
    return {
        "conflicts": [c.model_dump() for c in response.conflicts],
        "total_conflicts": len(response.conflicts),
    }


@app.post("/classify-instrument")
async def classify_instrument_endpoint(request: InstrumentClassifyRequest) -> Dict[str, Any]:
    """Classify an instrument by type."""
    result = classify_instrument_type(request.text)
    if result:
        return result
    return {"instrument_type": "unknown", "confidence": 0.0}


@app.post("/extract-terms")
async def extract_terms_endpoint(request: EasementTermsRequest) -> Dict[str, Any]:
    """Extract easement-related terms from text."""
    terms = extract_easement_terms(request.text)
    return {
        "terms": terms,
        "total_found": len(terms),
    }


@app.get("/doctrines")
async def list_doctrines(
    category: Optional[str] = Query(None),
    tag: Optional[str] = Query(None),
) -> Dict[str, Any]:
    """List all doctrine blocks, optionally filtered by category or tag."""
    if category:
        blocks = get_blocks_by_category(category)
    elif tag:
        blocks = get_blocks_by_tag(tag)
    else:
        blocks = DOCTRINE_BLOCKS

    return {
        "doctrines": [b.to_dict() for b in blocks],
        "total": len(blocks),
    }


@app.get("/doctrines/{topic}")
async def get_doctrine(topic: str) -> Dict[str, Any]:
    """Get a specific doctrine block by topic."""
    block = get_doctrine_block(topic)
    if not block:
        raise HTTPException(status_code=404, detail=f"Doctrine topic '{topic}' not found")
    return block.to_dict()


@app.get("/doctrines-coverage")
async def doctrines_coverage() -> Dict[str, Any]:
    """Get doctrine coverage map."""
    return get_coverage_map()


@app.get("/semantic-health")
async def semantic_health_endpoint() -> Dict[str, Any]:
    """Get semantic module health."""
    return semantic_health()


@app.get("/telemetry")
async def telemetry_endpoint() -> Dict[str, Any]:
    """Get full telemetry dashboard."""
    return telemetry_dashboard()


@app.get("/telemetry/summary")
async def telemetry_summary_endpoint() -> Dict[str, Any]:
    """Get compact telemetry summary."""
    return telemetry_health()


@app.get("/config")
async def config_endpoint() -> Dict[str, Any]:
    """Get engine configuration."""
    return {
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "engine_version": ENGINE_VERSION,
        "port": ENGINE_PORT,
        "authority": ENGINE_AUTHORITY,
        "tier": ENGINE_TIER,
        "mode": ENGINE_MODE,
        "config": analyzer.config,
    }


@app.get("/stats")
async def stats_endpoint() -> Dict[str, Any]:
    """Get engine statistics."""
    return {
        "engine_id": ENGINE_ID,
        "uptime_seconds": round(analyzer.uptime_seconds, 1),
        "request_count": analyzer._request_count,
        "doctrine_cache": doctrine_cache_health(),
        "search_index": search_index_health(),
        "telemetry": telemetry_health(),
    }


@app.post("/ingest")
async def ingest_record(record_data: Dict[str, Any]) -> Dict[str, Any]:
    """Ingest a new easement record into the search index."""
    try:
        etype = EasementType(record_data.get("easement_type", "unknown"))
    except ValueError:
        etype = EasementType.UNKNOWN

    try:
        estatus = EasementStatus(record_data.get("status", "unknown"))
    except ValueError:
        estatus = EasementStatus.UNKNOWN

    record = EasementRecord(
        record_id=record_data.get("record_id", str(uuid.uuid4())),
        easement_type=etype,
        status=estatus,
        grantor=record_data.get("grantor", ""),
        grantee=record_data.get("grantee", ""),
        pipeline_operator=record_data.get("pipeline_operator", ""),
        county=record_data.get("county", ""),
        state=record_data.get("state", "TX"),
        survey=record_data.get("survey", ""),
        abstract_number=record_data.get("abstract_number", ""),
        section=record_data.get("section", ""),
        block=record_data.get("block", ""),
        legal_description=record_data.get("legal_description", ""),
        instrument_number=record_data.get("instrument_number", ""),
        volume=record_data.get("volume", ""),
        page=record_data.get("page", ""),
        recording_date=record_data.get("recording_date", ""),
        effective_date=record_data.get("effective_date", ""),
        width_ft=float(record_data.get("width_ft", 0)),
        depth_ft=float(record_data.get("depth_ft", 0)),
        length_ft=float(record_data.get("length_ft", 0)),
        acreage=float(record_data.get("acreage", 0)),
        pipe_diameter_inches=float(record_data.get("pipe_diameter_inches", 0)),
        product_type=record_data.get("product_type", ""),
        operating_pressure_psi=float(record_data.get("operating_pressure_psi", 0)),
        consideration=float(record_data.get("consideration", 0)),
        annual_rental=float(record_data.get("annual_rental", 0)),
        purpose=record_data.get("purpose", ""),
        notes=record_data.get("notes", ""),
        restrictions=record_data.get("restrictions", ""),
        source=record_data.get("source", "manual_ingest"),
    )

    idx = get_search_index()
    idx.add_record(record)
    get_telemetry().record_request("/ingest", 0)

    return {
        "status": "ingested",
        "record_id": record.record_id,
        "content_hash": record.content_hash,
        "index_size": idx.size,
    }


@app.post("/ingest/batch")
async def ingest_batch(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Ingest a batch of easement records into the search index."""
    ingested = 0
    errors_list: List[Dict[str, Any]] = []
    idx = get_search_index()

    for i, record_data in enumerate(records):
        try:
            etype_val = record_data.get("easement_type", "unknown")
            try:
                etype = EasementType(etype_val)
            except ValueError:
                etype = EasementType.UNKNOWN

            estatus_val = record_data.get("status", "unknown")
            try:
                estatus = EasementStatus(estatus_val)
            except ValueError:
                estatus = EasementStatus.UNKNOWN

            record = EasementRecord(
                record_id=record_data.get("record_id", str(uuid.uuid4())),
                easement_type=etype,
                status=estatus,
                grantor=record_data.get("grantor", ""),
                grantee=record_data.get("grantee", ""),
                pipeline_operator=record_data.get("pipeline_operator", ""),
                county=record_data.get("county", ""),
                state=record_data.get("state", "TX"),
                survey=record_data.get("survey", ""),
                abstract_number=record_data.get("abstract_number", ""),
                section=record_data.get("section", ""),
                block=record_data.get("block", ""),
                legal_description=record_data.get("legal_description", ""),
                instrument_number=record_data.get("instrument_number", ""),
                volume=record_data.get("volume", ""),
                page=record_data.get("page", ""),
                recording_date=record_data.get("recording_date", ""),
                effective_date=record_data.get("effective_date", ""),
                width_ft=float(record_data.get("width_ft", 0)),
                depth_ft=float(record_data.get("depth_ft", 0)),
                length_ft=float(record_data.get("length_ft", 0)),
                acreage=float(record_data.get("acreage", 0)),
                pipe_diameter_inches=float(record_data.get("pipe_diameter_inches", 0)),
                product_type=record_data.get("product_type", ""),
                operating_pressure_psi=float(record_data.get("operating_pressure_psi", 0)),
                consideration=float(record_data.get("consideration", 0)),
                annual_rental=float(record_data.get("annual_rental", 0)),
                purpose=record_data.get("purpose", ""),
                notes=record_data.get("notes", ""),
                restrictions=record_data.get("restrictions", ""),
                source=record_data.get("source", "batch_ingest"),
            )
            idx.add_record(record)
            ingested += 1
        except Exception as e:
            errors_list.append({"index": i, "error": str(e)})

    get_telemetry().record_request("/ingest/batch", 0, result_count=ingested)

    return {
        "status": "batch_complete",
        "ingested": ingested,
        "errors": len(errors_list),
        "error_details": errors_list[:20],
        "index_size": idx.size,
    }


@app.post("/parse-instrument")
async def parse_instrument_endpoint(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse a full easement instrument text and extract structured data
    including easement type, parties, dimensions, duration, and terms.
    """
    start = time.time()
    text = request.get("text", "")
    if not text:
        raise HTTPException(status_code=400, detail="text field is required")

    # Import semantic clause extraction
    from semantic import (
        extract_clause_matches,
        extract_dimensions_from_text,
        normalize_party_name,
        normalize_legal_description,
    )

    # Classify instrument type
    instrument_class = classify_instrument_type(text)

    # Extract clause matches
    clause_matches = extract_clause_matches(text)

    # Extract dimensions
    dimensions = extract_dimensions_from_text(text)

    # Extract easement terms
    terms = extract_easement_terms(text)

    # Resolve synonyms
    synonyms_found = resolve_synonyms(text)

    # Extract parties (basic pattern matching)
    grantor_patterns = [
        r"(?:GRANTOR|Grantor)(?:\s*:\s*|\s+is\s+)([\w\s,\.]+?)(?:\s*,\s*(?:a\s+|an?\s+)|\s*\()",
        r"(?:from|FROM)\s+([\w\s,\.]+?)(?:\s*,\s*(?:a\s+|an?\s+)|\s*to\s+|\s*\()",
    ]
    grantors: List[str] = []
    for pattern in grantor_patterns:
        for match in re.finditer(pattern, text):
            name = normalize_party_name(match.group(1))
            if name and len(name) > 2:
                grantors.append(name)

    grantee_patterns = [
        r"(?:GRANTEE|Grantee)(?:\s*:\s*|\s+is\s+)([\w\s,\.]+?)(?:\s*,\s*(?:a\s+|an?\s+)|\s*\()",
        r"(?:grants?\s+(?:and\s+conveys?\s+)?(?:unto|to))\s+([\w\s,\.]+?)(?:\s*,\s*(?:a\s+|an?\s+)|\s*\()",
    ]
    grantees: List[str] = []
    for pattern in grantee_patterns:
        for match in re.finditer(pattern, text, flags=re.IGNORECASE):
            name = normalize_party_name(match.group(1))
            if name and len(name) > 2:
                grantees.append(name)

    # Duration extraction
    duration = "perpetual"
    if clause_matches.get("duration_specification"):
        for m in clause_matches["duration_specification"]:
            matched_text = m["matched_text"].lower()
            if "perpetui" in matched_text or "perpetual" in matched_text:
                duration = "perpetual"
                break
            groups = m.get("captured_groups", [])
            if groups:
                try:
                    years = int(groups[0])
                    duration = f"{years} years"
                    break
                except (ValueError, IndexError):
                    pass

    # Pipeline specifics
    pipeline_info: Dict[str, Any] = {}
    if clause_matches.get("pipeline_specification"):
        for m in clause_matches["pipeline_specification"]:
            matched_text = m["matched_text"].lower()
            groups = m.get("captured_groups", [])
            if groups:
                for g in groups:
                    if g:
                        try:
                            pipeline_info["diameter_inches"] = float(g)
                            break
                        except ValueError:
                            pass
            if "natural gas" in matched_text:
                pipeline_info["product_type"] = "natural_gas"
            elif "crude" in matched_text or "oil" in matched_text:
                pipeline_info["product_type"] = "crude_oil"
            elif "produced water" in matched_text or "salt water" in matched_text or "swd" in matched_text:
                pipeline_info["product_type"] = "produced_water"
            elif "product" in matched_text:
                pipeline_info["product_type"] = "petroleum_products"

    elapsed = (time.time() - start) * 1000
    get_telemetry().record_request("/parse-instrument", elapsed)

    return {
        "instrument_classification": instrument_class,
        "clause_matches": {k: len(v) for k, v in clause_matches.items()},
        "clause_details": clause_matches,
        "dimensions": dimensions,
        "terms_found": len(terms),
        "terms": terms[:50],
        "canonical_terms_matched": list(synonyms_found.keys()),
        "grantors": grantors,
        "grantees": grantees,
        "duration": duration,
        "pipeline_info": pipeline_info,
        "latency_ms": round(elapsed, 2),
    }


@app.get("/easement-types")
async def list_easement_types() -> Dict[str, Any]:
    """List all recognized easement types with descriptions."""
    types = []
    easement_type_config = analyzer.config.get("easement_types", {})
    for type_key, type_info in easement_type_config.items():
        types.append({
            "type_key": type_key,
            "description": type_info.get("description", ""),
            "recording_required": type_info.get("recording_required", None),
            "typical_duration": type_info.get("typical_duration", ""),
            "runs_with_land": type_info.get("runs_with_land", None),
        })
    return {"easement_types": types, "total": len(types)}


@app.get("/pipeline-specs")
async def pipeline_specs_endpoint() -> Dict[str, Any]:
    """Get pipeline specification reference data."""
    return {
        "pipeline_specifications": analyzer.config.get("pipeline_specifications", {}),
        "txdot_standards": analyzer.config.get("txdot_standards", {}),
        "rrc_requirements": analyzer.config.get("rrc_requirements", {}),
    }


@app.get("/valuation-factors")
async def valuation_factors_endpoint() -> Dict[str, Any]:
    """Get ROW and surface damage valuation reference factors."""
    return {
        "valuation_factors": analyzer.config.get("valuation_factors", {}),
        "surface_damage_act": analyzer.config.get("surface_damage_act", {}),
        "accommodation_doctrine": analyzer.config.get("accommodation_doctrine", {}),
    }


@app.get("/permian-counties")
async def permian_counties_endpoint() -> Dict[str, Any]:
    """List Permian Basin counties with integration status."""
    counties = analyzer.config.get("texas_counties_permian_basin", [])
    return {
        "counties": counties,
        "total": len(counties),
        "region": "Permian Basin",
        "state": "TX",
    }


@app.post("/row-compensation-estimate")
async def row_compensation_estimate(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Estimate ROW compensation based on acreage, land value, and damage factors.
    Uses the before-and-after method standard in Texas condemnation proceedings.
    """
    start = time.time()

    acreage_in_row = float(request.get("acreage_in_row", 0))
    total_tract_acreage = float(request.get("total_tract_acreage", 0))
    land_value_per_acre = float(request.get("land_value_per_acre", 0))
    crop_value_per_acre = float(request.get("crop_value_per_acre", 0))
    has_improvements_in_row = request.get("has_improvements_in_row", False)
    improvement_value = float(request.get("improvement_value", 0))
    is_condemnation = request.get("is_condemnation", False)
    county = request.get("county", "")

    # Easement strip value (typically 60-80% of fee value for pipeline ROW)
    easement_factor = 0.70  # 70% of fee value for permanent pipeline easement
    if request.get("easement_type") == "temporary":
        easement_factor = 0.25  # 25% for temporary construction easement

    strip_value = acreage_in_row * land_value_per_acre * easement_factor

    # Crop damage (one-time)
    crop_damage = acreage_in_row * crop_value_per_acre

    # Improvement damage
    improvement_damage = improvement_value if has_improvements_in_row else 0.0

    # Severance damages (impact on remainder)
    remainder_acreage = total_tract_acreage - acreage_in_row
    severance_factor = 0.0
    if total_tract_acreage > 0 and acreage_in_row / total_tract_acreage > 0.10:
        severance_factor = 0.05  # 5% diminution if ROW takes more than 10% of tract
    if acreage_in_row / max(total_tract_acreage, 1) > 0.25:
        severance_factor = 0.10  # 10% if more than 25%

    severance_damages = remainder_acreage * land_value_per_acre * severance_factor

    # Total compensation
    total_estimate = strip_value + crop_damage + improvement_damage + severance_damages

    # Permian Basin premium
    if county.lower() in TEXAS_PERMIAN_COUNTIES:
        total_estimate *= 1.15  # 15% premium for high-demand Permian Basin corridor

    elapsed = (time.time() - start) * 1000
    get_telemetry().record_request("/row-compensation-estimate", elapsed)

    return {
        "strip_value": round(strip_value, 2),
        "crop_damage": round(crop_damage, 2),
        "improvement_damage": round(improvement_damage, 2),
        "severance_damages": round(severance_damages, 2),
        "total_estimate": round(total_estimate, 2),
        "easement_factor": easement_factor,
        "severance_factor": severance_factor,
        "method": "before_and_after",
        "is_condemnation": is_condemnation,
        "county": county,
        "permian_premium_applied": county.lower() in TEXAS_PERMIAN_COUNTIES,
        "notes": (
            "Estimates based on standard Texas ROW compensation methodology. "
            "Actual compensation should be determined by qualified appraiser. "
            "In condemnation proceedings, special commissioners or jury "
            "determine just compensation per Tex. Prop. Code Ch. 21."
        ),
        "statutory_basis": [
            "Tex. Prop. Code \xA721.042 (Just Compensation)",
            "State v. Heal, 917 S.W.2d 6 (Tex. 1996) (before-and-after method)",
        ],
        "latency_ms": round(elapsed, 2),
    }


@app.post("/abandonment-analysis")
async def abandonment_analysis(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze whether an easement has been abandoned or extinguished.
    Evaluates intent, non-use, merger, and other extinguishment factors.
    """
    start = time.time()

    easement_type = request.get("easement_type", "unknown")
    years_of_non_use = int(request.get("years_of_non_use", 0))
    intent_evidence = request.get("intent_evidence", "")
    physical_improvements_removed = request.get("physical_improvements_removed", False)
    pipeline_purged = request.get("pipeline_purged", False)
    common_ownership = request.get("common_ownership_achieved", False)
    written_release_exists = request.get("written_release_exists", False)
    servient_owner_acted_in_reliance = request.get("servient_owner_reliance", False)

    factors: List[Dict[str, Any]] = []
    abandonment_likelihood = 0.0

    # Factor 1: Intent to abandon
    if intent_evidence:
        factors.append({
            "factor": "Intent Evidence",
            "present": True,
            "description": f"Evidence of intent to abandon: {intent_evidence}",
            "weight": 0.30,
        })
        abandonment_likelihood += 0.30
    else:
        factors.append({
            "factor": "Intent Evidence",
            "present": False,
            "description": "No affirmative evidence of intent to abandon",
            "weight": 0.0,
        })

    # Factor 2: Physical actions inconsistent with continued use
    if physical_improvements_removed:
        factors.append({
            "factor": "Physical Removal",
            "present": True,
            "description": "Physical improvements (pipeline, poles, etc.) have been removed",
            "weight": 0.25,
        })
        abandonment_likelihood += 0.25

    if pipeline_purged:
        factors.append({
            "factor": "Pipeline Purged",
            "present": True,
            "description": "Pipeline has been purged, filled, and/or capped per RRC procedure",
            "weight": 0.20,
        })
        abandonment_likelihood += 0.20

    # Factor 3: Non-use (alone insufficient in Texas)
    if years_of_non_use > 0:
        factors.append({
            "factor": "Non-Use",
            "present": True,
            "description": (
                f"{years_of_non_use} years of non-use. IMPORTANT: In Texas, "
                f"mere non-use alone is INSUFFICIENT to establish abandonment, "
                f"regardless of duration. Nat'l Resort Communities v. Cain (1975)."
            ),
            "weight": min(years_of_non_use * 0.01, 0.10),
        })
        abandonment_likelihood += min(years_of_non_use * 0.01, 0.10)

    # Factor 4: Merger
    if common_ownership:
        factors.append({
            "factor": "Merger",
            "present": True,
            "description": (
                "Dominant and servient estates are now under common ownership. "
                "Merger extinguishes the easement by operation of law."
            ),
            "weight": 0.95,
        })
        abandonment_likelihood = 0.95

    # Factor 5: Written release
    if written_release_exists:
        factors.append({
            "factor": "Written Release",
            "present": True,
            "description": "A written release of the easement has been executed and (presumably) recorded.",
            "weight": 0.99,
        })
        abandonment_likelihood = 0.99

    # Factor 6: Estoppel
    if servient_owner_acted_in_reliance:
        factors.append({
            "factor": "Estoppel/Reliance",
            "present": True,
            "description": (
                "Servient owner acted in detrimental reliance on apparent "
                "abandonment (e.g., constructed improvements over easement)."
            ),
            "weight": 0.15,
        })
        abandonment_likelihood += 0.15

    abandonment_likelihood = min(abandonment_likelihood, 1.0)

    # Determine status
    if abandonment_likelihood >= 0.80:
        status = "likely_abandoned"
        recommendation = "Strong evidence supports abandonment. Consider quiet title action to clear records."
    elif abandonment_likelihood >= 0.50:
        status = "possibly_abandoned"
        recommendation = "Evidence is mixed. Additional investigation recommended before relying on abandonment."
    elif abandonment_likelihood >= 0.20:
        status = "unlikely_abandoned"
        recommendation = "Insufficient evidence for abandonment. Non-use alone does not suffice in Texas."
    else:
        status = "not_abandoned"
        recommendation = "No meaningful evidence of abandonment. Easement remains enforceable."

    elapsed = (time.time() - start) * 1000
    get_telemetry().record_request("/abandonment-analysis", elapsed)

    return {
        "easement_type": easement_type,
        "abandonment_likelihood": round(abandonment_likelihood, 2),
        "status": status,
        "recommendation": recommendation,
        "factors": factors,
        "key_doctrine": (
            "Texas law requires both INTENT to abandon AND AFFIRMATIVE ACTS "
            "inconsistent with continued use. Mere non-use, no matter how long, "
            "is insufficient. Nat'l Resort Communities, Inc. v. Cain, "
            "526 S.W.2d 510 (Tex. 1975)."
        ),
        "statutory_basis": [
            "Common law (no specific Texas statute for easement abandonment)",
            "Tex. Prop. Code \xA75.021 (written release for express easement)",
        ],
        "leading_cases": [
            "Nat'l Resort Communities, Inc. v. Cain, 526 S.W.2d 510 (Tex. 1975)",
            "Humphrey-Trott Land Co. v. Andrews County, 733 S.W.2d 649 (Tex. App.—El Paso 1987)",
        ],
        "latency_ms": round(elapsed, 2),
    }


@app.post("/overburdening-check")
async def overburdening_check(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Check whether a proposed use of an easement constitutes overburdening.
    Based on Marcus Cable v. Krohn analysis framework.
    """
    start = time.time()

    original_grant_purpose = request.get("original_grant_purpose", "")
    proposed_use = request.get("proposed_use", "")
    original_width_ft = float(request.get("original_width_ft", 0))
    proposed_width_ft = float(request.get("proposed_width_ft", 0))
    benefits_non_dominant = request.get("benefits_non_dominant_parcel", False)
    third_party_use = request.get("third_party_use", False)
    technology_change = request.get("technology_change", False)

    risk_factors: List[str] = []
    overburdening_risk = 0.0

    # Check 1: Use exceeds scope of original grant
    if original_grant_purpose and proposed_use:
        original_lower = original_grant_purpose.lower()
        proposed_lower = proposed_use.lower()

        # Different fundamental purpose
        if ("electric" in original_lower and "cable" in proposed_lower) or \
           ("telephone" in original_lower and "fiber" in proposed_lower and "data" in proposed_lower):
            risk_factors.append(
                f"Proposed use ({proposed_use}) differs fundamentally from "
                f"original grant purpose ({original_grant_purpose}). "
                f"See Marcus Cable v. Krohn (2002)."
            )
            overburdening_risk += 0.40

        if ("pipeline" in original_lower and "fiber" in proposed_lower):
            risk_factors.append(
                "Adding fiber optic cable to pipeline easement likely exceeds "
                "scope unless grant contains broad 'utility' language."
            )
            overburdening_risk += 0.35

    # Check 2: Physical expansion
    if proposed_width_ft > original_width_ft and original_width_ft > 0:
        expansion_pct = (proposed_width_ft - original_width_ft) / original_width_ft * 100
        risk_factors.append(
            f"Proposed width ({proposed_width_ft} ft) exceeds original grant "
            f"width ({original_width_ft} ft) by {expansion_pct:.0f}%."
        )
        overburdening_risk += min(expansion_pct / 200, 0.30)

    # Check 3: Benefits non-dominant parcel
    if benefits_non_dominant:
        risk_factors.append(
            "Use benefits a parcel other than the dominant estate. "
            "Dominant estate owner cannot use appurtenant easement for "
            "benefit of non-dominant land."
        )
        overburdening_risk += 0.35

    # Check 4: Unauthorized third-party use
    if third_party_use:
        risk_factors.append(
            "Third-party use piggybacking on existing easement without "
            "authorization from servient estate owner."
        )
        overburdening_risk += 0.30

    # Check 5: Technology evolution
    if technology_change:
        risk_factors.append(
            "Proposed use involves technology change. Some courts allow "
            "reasonable technology evolution if consistent with original purpose. "
            "Key question: was the new use within reasonable contemplation "
            "of the parties at the time of grant?"
        )
        overburdening_risk += 0.15

    overburdening_risk = min(overburdening_risk, 1.0)

    if overburdening_risk >= 0.60:
        status = "high_risk"
        recommendation = (
            "Significant overburdening risk. Recommend obtaining new easement or "
            "amendment to existing easement with additional compensation to servient owner."
        )
    elif overburdening_risk >= 0.30:
        status = "moderate_risk"
        recommendation = (
            "Moderate overburdening risk. Review original grant language carefully. "
            "Consider negotiating amendment or separate easement for proposed use."
        )
    else:
        status = "low_risk"
        recommendation = (
            "Low overburdening risk based on available information. "
            "Verify proposed use falls within reasonable scope of original grant."
        )

    elapsed = (time.time() - start) * 1000
    get_telemetry().record_request("/overburdening-check", elapsed)

    return {
        "overburdening_risk": round(overburdening_risk, 2),
        "status": status,
        "recommendation": recommendation,
        "risk_factors": risk_factors,
        "original_grant_purpose": original_grant_purpose,
        "proposed_use": proposed_use,
        "key_doctrine": (
            "Marcus Cable Assocs. v. Krohn, 90 S.W.3d 697 (Tex. 2002): "
            "The scope of an easement is determined by the grant instrument. "
            "Uses not within the reasonable contemplation of the parties at "
            "the time of the grant constitute overburdening."
        ),
        "leading_cases": [
            "Marcus Cable Assocs. v. Krohn, 90 S.W.3d 697 (Tex. 2002)",
            "Coleman v. Forister, 514 S.W.2d 899 (Tex. 1974)",
            "City of Tyler v. Likes, 962 S.W.2d 489 (Tex. 1997)",
        ],
        "latency_ms": round(elapsed, 2),
    }


@app.get("/operators")
async def list_operators() -> Dict[str, Any]:
    """List all recognized pipeline operators with aliases."""
    operators = []
    for canonical, aliases in OPERATOR_ALIAS_MAP.items():
        operators.append({
            "canonical_name": canonical,
            "aliases": aliases,
            "alias_count": len(aliases),
        })
    return {
        "operators": sorted(operators, key=lambda x: x["canonical_name"]),
        "total": len(operators),
    }


@app.get("/abbreviations")
async def list_abbreviations() -> Dict[str, Any]:
    """List all recognized abbreviations with expansions."""
    return {
        "abbreviations": ABBREVIATION_MAP,
        "total": len(ABBREVIATION_MAP),
    }


@app.post("/normalize")
async def normalize_text(request: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize a query or text through the semantic pipeline."""
    text = request.get("text", "")
    if not text:
        raise HTTPException(status_code=400, detail="text field is required")

    normalized = normalize_query(text)
    expanded = expand_abbreviations(text)
    synonyms_found = resolve_synonyms(text)
    terms = extract_easement_terms(text)

    # Try operator resolution
    operator = resolve_operator(text)

    return {
        "original": text,
        "normalized": normalized,
        "expanded": expanded,
        "canonical_terms": list(synonyms_found.keys()),
        "synonym_matches": synonyms_found,
        "easement_terms_found": len(terms),
        "resolved_operator": operator,
    }


@app.post("/common-carrier-analysis")
async def common_carrier_analysis(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze whether an entity qualifies as a common carrier pipeline
    under Texas law for eminent domain purposes (Denbury test).
    """
    start = time.time()

    company_name = request.get("company_name", "")
    pipeline_description = request.get("pipeline_description", "")
    transports_for_public = request.get("transports_for_public", False)
    published_tariffs = request.get("published_tariffs", False)
    third_party_contracts = request.get("third_party_contracts", False)
    percentage_own_product = float(request.get("percentage_own_product", 100))
    rrc_permit_type = request.get("rrc_permit_type", "")
    t4_permit_active = request.get("t4_permit_active", False)

    factors: List[Dict[str, Any]] = []
    common_carrier_score = 0.0

    # Factor 1: T-4 permit status
    if t4_permit_active:
        factors.append({
            "factor": "T-4 Permit",
            "status": "active",
            "description": "Active T-4 permit filed with RRC indicates common carrier registration",
            "weight": 0.15,
            "note": "T-4 filing is necessary but NOT sufficient for common carrier status per Denbury",
        })
        common_carrier_score += 0.15
    else:
        factors.append({
            "factor": "T-4 Permit",
            "status": "missing",
            "description": "No active T-4 permit. Common carrier pipelines must hold T-4 permit.",
            "weight": 0.0,
        })

    # Factor 2: Public transportation
    if transports_for_public:
        factors.append({
            "factor": "Public Transportation",
            "status": "confirmed",
            "description": "Pipeline transports or offers to transport product for third parties",
            "weight": 0.30,
        })
        common_carrier_score += 0.30
    else:
        factors.append({
            "factor": "Public Transportation",
            "status": "not_demonstrated",
            "description": "No evidence of actual or offered third-party transportation",
            "weight": 0.0,
            "note": "This is the critical factor under Denbury. Pipeline must actually serve public.",
        })

    # Factor 3: Published tariffs
    if published_tariffs:
        factors.append({
            "factor": "Published Tariffs",
            "status": "confirmed",
            "description": "Pipeline has published tariff rates for third-party transportation",
            "weight": 0.20,
        })
        common_carrier_score += 0.20
    else:
        factors.append({
            "factor": "Published Tariffs",
            "status": "not_published",
            "description": "No published tariff rates found. Common carriers must offer service at published rates.",
            "weight": 0.0,
        })

    # Factor 4: Third-party contracts
    if third_party_contracts:
        factors.append({
            "factor": "Third-Party Contracts",
            "status": "confirmed",
            "description": "Active third-party transportation contracts exist",
            "weight": 0.20,
        })
        common_carrier_score += 0.20
    else:
        factors.append({
            "factor": "Third-Party Contracts",
            "status": "none",
            "description": "No known third-party transportation contracts. Supports argument pipeline is private.",
            "weight": 0.0,
        })

    # Factor 5: Percentage of own product
    if percentage_own_product < 50:
        factors.append({
            "factor": "Product Mix",
            "status": "majority_third_party",
            "description": f"Only {percentage_own_product}% own product -- majority serves public",
            "weight": 0.15,
        })
        common_carrier_score += 0.15
    elif percentage_own_product < 80:
        factors.append({
            "factor": "Product Mix",
            "status": "mixed",
            "description": f"{percentage_own_product}% own product -- some third-party service",
            "weight": 0.08,
        })
        common_carrier_score += 0.08
    else:
        factors.append({
            "factor": "Product Mix",
            "status": "primarily_own_product",
            "description": (
                f"{percentage_own_product}% own product. Pipeline appears to primarily "
                f"serve the company's own production. Denbury raises concern."
            ),
            "weight": 0.0,
        })

    common_carrier_score = min(common_carrier_score, 1.0)

    if common_carrier_score >= 0.70:
        status = "likely_common_carrier"
        eminent_domain_authority = "probable"
        recommendation = (
            "Entity likely qualifies as common carrier with eminent domain authority. "
            "Landowner may need to negotiate ROW or face condemnation proceedings."
        )
    elif common_carrier_score >= 0.40:
        status = "uncertain"
        eminent_domain_authority = "disputed"
        recommendation = (
            "Common carrier status is uncertain. Landowner should challenge the entity's "
            "standing to condemn under the Denbury test. Request evidence of actual "
            "third-party transportation or binding commitments to serve the public."
        )
    else:
        status = "likely_not_common_carrier"
        eminent_domain_authority = "unlikely"
        recommendation = (
            "Entity likely does not qualify as a bona fide common carrier. "
            "Filing a T-4 permit alone is insufficient. Without actual or committed "
            "third-party service, condemnation should be challenged and likely dismissed."
        )

    elapsed = (time.time() - start) * 1000
    get_telemetry().record_request("/common-carrier-analysis", elapsed)

    return {
        "company_name": company_name,
        "common_carrier_score": round(common_carrier_score, 2),
        "status": status,
        "eminent_domain_authority": eminent_domain_authority,
        "recommendation": recommendation,
        "factors": factors,
        "denbury_test": (
            "Denbury Green Pipeline-Texas LLC v. Texas Rice Land Partners Ltd., "
            "510 S.W.3d 909 (Tex. 2017): A pipeline entity must prove it is a "
            "bona fide common carrier actually serving or committed to serve the "
            "public. Merely filing a T-4 permit with the RRC is necessary but "
            "not sufficient. The entity must demonstrate a reasonable probability "
            "that the pipeline will serve the public by transporting product for "
            "third parties, not exclusively for its own use."
        ),
        "statutory_basis": [
            "Tex. Nat. Res. Code \xA7111.002 (Definition of Common Carrier)",
            "Tex. Nat. Res. Code \xA7111.019 (Right of Eminent Domain)",
            "Tex. Prop. Code Ch. 21 (Eminent Domain Procedures)",
        ],
        "leading_cases": [
            "Denbury Green Pipeline-Texas LLC v. Texas Rice Land Partners Ltd., 510 S.W.3d 909 (Tex. 2017)",
            "Texas Rice Land Partners, Ltd. v. Denbury Green Pipeline-Texas, LLC, 363 S.W.3d 192 (Tex. 2012)",
            "Hubenak v. San Jacinto Gas Transmission Co., 141 S.W.3d 172 (Tex. 2004)",
        ],
        "latency_ms": round(elapsed, 2),
    }


@app.post("/lm07-integration-check")
async def lm07_integration_check(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Verify integration with LM07 Legal Description Parser.
    Attempts to parse a legal description for an easement instrument
    through the LM07 engine.
    """
    legal_description = request.get("legal_description", "")
    if not legal_description:
        raise HTTPException(status_code=400, detail="legal_description is required")

    # LM07 integration configuration
    lm07_config = analyzer.config.get("integration", {}).get("lm07_legal_description_parser", {})
    lm07_port = lm07_config.get("port", 8427)
    lm07_endpoint = lm07_config.get("endpoint", "/parse")
    lm07_url = f"http://localhost:{lm07_port}{lm07_endpoint}"

    # Normalize the legal description locally
    from semantic import normalize_legal_description
    normalized = normalize_legal_description(legal_description)

    # Attempt LM07 call (non-blocking, with graceful degradation)
    lm07_result: Optional[Dict[str, Any]] = None
    lm07_available = False

    try:
        import httpx
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(lm07_url, json={"text": legal_description})
            if resp.status_code == 200:
                lm07_result = resp.json()
                lm07_available = True
    except Exception as e:
        logger.debug(f"LM07 not available at {lm07_url}: {e}")

    # Local fallback parsing
    import re
    local_parse: Dict[str, Any] = {
        "raw": legal_description,
        "normalized": normalized,
        "type": "unknown",
    }

    # Detect PLSS pattern
    plss_pattern = r"Section\s+(\d+),?\s*Block\s+([A-Z0-9\-]+),?\s*(?:Township\s+(\d+[NS]),?\s*Range\s+(\d+[EW]))?'?"
    plss_match = re.search(plss_pattern, normalized, flags=re.IGNORECASE)
    if plss_match:
        local_parse["type"] = "plss"
        local_parse["section"] = plss_match.group(1)
        local_parse["block"] = plss_match.group(2)
        if plss_match.group(3):
            local_parse["township"] = plss_match.group(3)
        if plss_match.group(4):
            local_parse["range"] = plss_match.group(4)

    # Detect lot/block pattern
    lot_pattern = r"Lot\s+(\d+),?\s*Block\s+([A-Z0-9\-]+),?\s*(.+?)(?:,|\.|$)"
    lot_match = re.search(lot_pattern, normalized, flags=re.IGNORECASE)
    if lot_match:
        local_parse["type"] = "lot_block"
        local_parse["lot"] = lot_match.group(1)
        local_parse["block"] = lot_match.group(2)
        local_parse["subdivision"] = lot_match.group(3).strip()

    # Detect abstract/survey
    abstract_pattern = r"Abstract\s+(?:No\.?\s*)?([A-Z]?\d+)"
    abs_match = re.search(abstract_pattern, normalized, flags=re.IGNORECASE)
    if abs_match:
        local_parse["abstract_number"] = abs_match.group(1)

    survey_pattern = r"Survey\s+(?:No\.?\s*)?([A-Z]?\d+)"
    survey_match = re.search(survey_pattern, normalized, flags=re.IGNORECASE)
    if survey_match:
        local_parse["survey"] = survey_match.group(1)

    # Detect metes and bounds
    if re.search(r'thence|bearing|N\s*\d+|S\s*\d+|beginning', normalized, flags=re.IGNORECASE):
        local_parse["type"] = "metes_and_bounds"

    return {
        "lm07_available": lm07_available,
        "lm07_result": lm07_result,
        "local_parse": local_parse,
        "legal_description": legal_description,
        "normalized": normalized,
    }


@app.get("/doctrine-drift")
async def doctrine_drift_check() -> Dict[str, Any]:
    """
    Check for doctrine drift -- identify stale or outdated doctrine
    blocks that may need updating.
    """
    health = doctrine_cache_health()
    stale_topics = health.get("stale_topics", [])
    coverage = health.get("coverage", {})

    drift_report: List[Dict[str, Any]] = []
    for topic in stale_topics:
        block = get_doctrine_block(topic)
        if block:
            drift_report.append({
                "topic": topic,
                "category": block.category,
                "last_updated": block.last_updated,
                "authority_score": block.authority_score,
                "is_stale": True,
                "recommendation": "Review and update doctrine block with current case law and statutory changes",
            })

    # Check coverage gaps
    expected_categories = [
        "Express Easements", "Implied Easements", "Prescriptive Easements",
        "Appurtenant vs In Gross", "Pipeline ROW", "Surface Use Agreements",
        "Accommodation Doctrine", "Dominant/Servient Estate", "Road Easements",
        "Utility Easements", "Eminent Domain", "Abandonment/Extinguishment",
        "Overburdening", "Scope Limitations", "Texas Natural Resources Code",
        "Reasonable Use", "Conservation Easements", "Flowage/Drainage",
        "Easement Relocation", "TxDOT Crossings", "Easement Conflicts",
        "Easement Assignments",
    ]

    existing_categories = set(coverage.keys())
    missing_categories = [c for c in expected_categories if c.lower() not in existing_categories]

    return {
        "total_blocks": health.get("total_blocks", 0),
        "stale_blocks": len(stale_topics),
        "drift_report": drift_report,
        "coverage_gaps": missing_categories,
        "coverage_summary": coverage,
    }


# ============================================================================
# CLOUD-ENRICHED QUERY ENDPOINT
# ============================================================================

class _CloudQueryReq(BaseModel):
    query: str = ""
    prompt: str = ""
    mode: str = "analysis"
    include_cloud: bool = True


@app.post("/query")
async def cloud_query(request: _CloudQueryReq):
    import time as _time
    start = _time.monotonic()
    q = request.query or request.prompt
    cloud_data = {}
    cloud_citations = []
    if _CLOUD_AVAILABLE and request.include_cloud:
        try:
            cloud = await retrieve_cloud_knowledge(q, category="easement")
            cloud_data = {"records": cloud.total_records, "merged_context": cloud.merged_text(3000), "sources_succeeded": cloud.sources_succeeded, "retrieval_time_ms": cloud.retrieval_time_ms}
            cloud_citations = cloud.citation_list()
        except Exception as e:
            logger.warning(f"Cloud retrieval failed: {e}")
    elapsed = (_time.monotonic() - start) * 1000
    return {"engine_id": ENGINE_ID, "engine_name": ENGINE_NAME, "query": q, "cloud_knowledge": cloud_data, "cloud_citations": cloud_citations, "processing_time_ms": round(elapsed, 2), "cloud_available": _CLOUD_AVAILABLE}


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    logger.remove()
    logger.add(
        sys.stderr,
        level="INFO",
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>"
        ),
    )
    logger.add(
        Path(__file__).parent / "logs" / "lm14_{time:YYYY-MM-DD}.log",
        rotation="1 day",
        retention="30 days",
        level="DEBUG",
    )

    logger.info(f"Launching {ENGINE_ID} {ENGINE_NAME} v{ENGINE_VERSION} on port {ENGINE_PORT}")
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    uvicorn.run(
        "engine:app",
        host="0.0.0.0",
        port=ENGINE_PORT,
        reload=False,
        log_level="info",
    )
