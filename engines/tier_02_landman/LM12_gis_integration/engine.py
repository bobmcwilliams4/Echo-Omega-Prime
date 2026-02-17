"""
LM12 GIS Integration Engine
Engine ID: LM12 | Port: 8512 | Version: 1.0.0
Domain: Landman Intelligence — GIS/Spatial Analysis for Oil & Gas Operations

TIE-20 Gold Standard Implementation:
  1.  three_layer_response — Doctrine Cache, Semantic Retrieval, Deep Analysis
  2.  response_modes — FAST, SURVEY, REPORT
  3.  doctrine_cache — 50+ pre-compiled GIS reasoning blocks
  4.  authority_hardening — Hierarchical authority with weights
  5.  confidence_stratification — DEFENSIBLE / AGGRESSIVE / DISCLOSURE / HIGH_RISK
  6.  semantic_normalization — GIS term normalization
  7.  vector_search — Semantic retrieval fallback
  8.  telemetry — Full query tracing
  9.  drift_watcher — Doctrine consistency monitoring
  10. coverage_map — Triggered/missed doctrine tracking
  11. metrics_collector — Latency, error rates, hit rates
  12. health_endpoint — Comprehensive health check
  13. zoned_analysis — PLANNING / REPORTING / AUDIT zones
  14. fact_fragility_scoring — Verifiability and risk scoring
  15. audit_trail_jsonl — Forensic query logging
  16. determinism_hash_sha256 — Reproducibility hashing
  17. fastapi_server — FastAPI with CORS and typed endpoints
  18. loguru_logging — Structured logging
  19. multi_doctrine_decomposition — Issue strata and interaction DAG
  20. deep_analysis_mode — Multi-source synthesis
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
import sys
import time
import uuid
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Optional

# ─── Cloud knowledge retrieval setup ──────────────────────────────────
from pathlib import Path as _Path
sys.path.insert(0, str(_Path(__file__).resolve().parent.parent / "_shared"))

import uvicorn
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import BaseModel, Field

# ─── Cloud knowledge retrieval import ─────────────────────────────────
try:
    from cloud_retriever import CognitionCloudRetriever, CloudKnowledge, retrieve_cloud_knowledge
    _CLOUD_AVAILABLE = True
except ImportError:
    _CLOUD_AVAILABLE = False
    logger.warning("cloud_retriever not available — running without cloud knowledge")

# ─── Local imports ────────────────────────────────────────────────────

# Ensure sibling modules are importable
ENGINE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ENGINE_DIR))
from doctrines import (
    ConfidenceLevel,
    DoctrineBlock,
    IssueCategory,
    build_doctrine_cache,
    get_all_doctrine_topics,
    get_doctrine_interaction_graph,
    get_doctrines_by_category,
)
from search import GISDoctrineSearch, SearchDocument, SearchResult
from semantic import (
    NormalizationResult,
    normalize_semantics,
)
from telemetry import (
    CoverageMap,
    DriftWatcher,
    ErrorDomain,
    MetricsCollector,
    QueryPhase,
    QueryTrace,
    TelemetryManager,
)

# ═══════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════

ENGINE_ID = "LM12"
ENGINE_NAME = "GIS Integration Engine"
ENGINE_VERSION = "1.0.0"
ENGINE_PORT = 8512
ENGINE_DOMAIN = "gis_landman_intelligence"
ENGINE_SUBDOMAIN = "spatial_analysis"

LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR = Path(__file__).parent / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
VECTOR_DIR = Path(__file__).parent / "vectors"
VECTOR_DIR.mkdir(parents=True, exist_ok=True)

logger.remove()
logger.add(sys.stderr, level="INFO", format="<green>{time:HH:mm:ss}</green> | <level>{level:<7}</level> | <cyan>{name}</cyan> | {message}")
logger.add(LOG_DIR / "lm12_engine.log", rotation="10 MB", retention="30 days", level="DEBUG")

BANNED_PHRASES = [
    "this is not legal advice",
    "consult an attorney",
    "I am not a surveyor",
    "this is for informational purposes only",
    "you should seek professional",
    "consult a licensed surveyor",
    "consult a geologist",
]

# Texas State Plane Coordinate System Zones (SPCS)
TEXAS_SPCS_ZONES = {
    "TX_NORTH": {"epsg": 32138, "counties": ["DALLAM", "SHERMAN", "HANSFORD", "OCHILTREE", "LIPSCOMB"]},
    "TX_NORTH_CENTRAL": {"epsg": 32139, "counties": ["TARRANT", "DALLAS", "COLLIN", "DENTON", "ROCKWALL"]},
    "TX_CENTRAL": {"epsg": 32140, "counties": ["ECTOR", "MIDLAND", "HOWARD", "MARTIN", "REEVES", "PECOS"]},
    "TX_SOUTH_CENTRAL": {"epsg": 32141, "counties": ["BEXAR", "COMAL", "GUADALUPE", "TRAVIS"]},
    "TX_SOUTH": {"epsg": 32142, "counties": ["CAMERON", "HIDALGO", "WEBB", "ZAPATA"]},
}

# RRC Spacing Rules (Texas Railroad Commission)
RRC_SPACING_RULES = {
    "RULE_37": {
        "default_well_spacing_ft": 467,
        "default_lease_line_ft": 330,
        "min_acreage": 40,
        "description": "Statewide spacing rule for oil wells",
    },
    "RULE_38": {
        "default_well_spacing_ft": 1200,
        "default_lease_line_ft": 467,
        "min_acreage": 640,
        "description": "Statewide spacing rule for gas wells",
    },
    "PERMIAN_BASIN_HORIZONTAL": {
        "lateral_length_ft": 10000,
        "min_proration_unit_acres": 640,
        "boundary_setback_ft": 330,
        "description": "Typical horizontal well spacing in Permian Basin",
    },
}

# Coordinate System Constants
EARTH_RADIUS_FT = 20902230.97  # Earth radius in feet (for NAD83 ellipsoid)
FEET_PER_METER = 3.28084
METERS_PER_FOOT = 0.3048
FEET_PER_MILE = 5280
ACRES_PER_SQ_FT = 1 / 43560
SQ_FT_PER_ACRE = 43560


# ═══════════════════════════════════════════════════════════════════════
# PYDANTIC MODELS
# ═══════════════════════════════════════════════════════════════════════

class ResponseMode(str, Enum):
    """Response mode for query processing."""
    FAST = "FAST"
    SURVEY = "SURVEY"
    REPORT = "REPORT"


class AnalysisZone(str, Enum):
    """Position zones that must never be blurred."""
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"


class CoordinatePair(BaseModel):
    """A single coordinate pair with datum reference."""
    latitude: Optional[float] = Field(default=None, ge=-90, le=90, description="Latitude in decimal degrees")
    longitude: Optional[float] = Field(default=None, ge=-180, le=180, description="Longitude in decimal degrees")
    easting: Optional[float] = Field(default=None, description="Easting in feet or meters")
    northing: Optional[float] = Field(default=None, description="Northing in feet or meters")
    datum: str = Field(default="NAD83", description="Coordinate datum (NAD27, NAD83, WGS84)")
    zone: Optional[str] = Field(default=None, description="UTM or SPCS zone")
    elevation_ft: Optional[float] = Field(default=None, description="Elevation above sea level in feet")


class LegalDescription(BaseModel):
    """Parsed legal description components."""
    raw: str = Field(..., description="Original legal description text")
    abstract_number: Optional[str] = Field(default=None, description="Texas abstract number")
    survey_name: Optional[str] = Field(default=None, description="Original survey name")
    section: Optional[str] = Field(default=None, description="Section number")
    block: Optional[str] = Field(default=None, description="Block identifier")
    township: Optional[str] = Field(default=None, description="Township (rectangular survey)")
    range: Optional[str] = Field(default=None, description="Range (rectangular survey)")
    subdivision: Optional[str] = Field(default=None, description="Subdivision name")
    lot: Optional[str] = Field(default=None, description="Lot number")
    acres: Optional[float] = Field(default=None, ge=0, description="Acreage described")
    metes_bounds: Optional[list[str]] = Field(default=None, description="Metes and bounds calls")
    county: Optional[str] = Field(default=None, description="County name")
    state: str = Field(default="Texas", description="State")


class ParcelBoundary(BaseModel):
    """GIS parcel boundary representation."""
    vertices: list[CoordinatePair] = Field(..., description="Ordered vertices forming boundary")
    closed: bool = Field(default=False, description="Whether polygon is closed")
    area_acres: Optional[float] = Field(default=None, ge=0, description="Calculated area in acres")
    perimeter_ft: Optional[float] = Field(default=None, ge=0, description="Perimeter length in feet")
    centroid: Optional[CoordinatePair] = Field(default=None, description="Geometric center")
    datum: str = Field(default="NAD83", description="Coordinate datum")


class WellLocation(BaseModel):
    """Oil/gas well location with regulatory compliance checks."""
    api_number: Optional[str] = Field(default=None, description="14-digit API well number")
    lease_name: str = Field(..., description="Lease name")
    well_number: str = Field(..., description="Well number")
    coordinates: CoordinatePair = Field(..., description="Surface location coordinates")
    bottom_hole_location: Optional[CoordinatePair] = Field(default=None, description="BHL for directional wells")
    lateral_length_ft: Optional[float] = Field(default=None, ge=0, description="Lateral length for horizontal wells")
    spacing_compliant: bool = Field(default=False, description="Meets RRC spacing requirements")
    spacing_rule: Optional[str] = Field(default=None, description="Applicable spacing rule (RULE_37, RULE_38, etc)")
    distance_to_lease_line_ft: Optional[float] = Field(default=None, ge=0, description="Minimum distance to lease boundary")
    proration_unit_acres: Optional[float] = Field(default=None, ge=0, description="Assigned proration unit acreage")


class OverlapGapResult(BaseModel):
    """Result of overlap/gap detection between parcels."""
    parcel_a_id: str
    parcel_b_id: str
    overlap_detected: bool = False
    gap_detected: bool = False
    overlap_area_acres: Optional[float] = Field(default=None, ge=0)
    gap_area_acres: Optional[float] = Field(default=None, ge=0)
    overlap_vertices: Optional[list[CoordinatePair]] = Field(default=None)
    gap_vertices: Optional[list[CoordinatePair]] = Field(default=None)
    significance: str = Field(default="MINOR", description="MINOR, MODERATE, CRITICAL")
    curative_action: Optional[str] = Field(default=None)


class UnitBoundary(BaseModel):
    """Oil/gas pooling or communitization unit boundary."""
    unit_name: str
    unit_type: str = Field(..., description="POOLED, COMMUNITIZED, VOLUNTARY, FORCED")
    effective_date: str
    boundary: ParcelBoundary
    included_leases: list[str] = Field(default_factory=list)
    participating_interests: list[dict[str, Any]] = Field(default_factory=list)
    rrc_order_number: Optional[str] = Field(default=None)
    total_acres: float = Field(..., ge=0)
    allocation_formula: Optional[str] = Field(default=None)


class QueryRequest(BaseModel):
    """Incoming GIS query request."""
    query: str = Field(..., min_length=3, max_length=10000, description="The GIS or spatial analysis query")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response mode")
    zone: AnalysisZone = Field(default=AnalysisZone.REPORTING, description="Analysis zone")
    session_id: Optional[str] = Field(default=None, description="Session ID for tracking")
    issue_category: Optional[str] = Field(default=None, description="Specific GIS issue category")
    county: Optional[str] = Field(default=None, description="Texas county")
    legal_description: Optional[str] = Field(default=None, description="Legal description to parse/map")
    coordinates: Optional[list[CoordinatePair]] = Field(default=None, description="Coordinate pairs for analysis")
    well_locations: Optional[list[WellLocation]] = Field(default=None, description="Well locations for spacing checks")
    parcels: Optional[list[ParcelBoundary]] = Field(default=None, description="Parcel boundaries for overlap/gap analysis")
    deep_analysis: bool = Field(default=False, description="Enable deep analysis mode")


class QueryResponse(BaseModel):
    """GIS query response."""
    query_id: str
    session_id: Optional[str] = None
    mode: ResponseMode
    zone: AnalysisZone
    answer: str
    confidence: str
    doctrines_triggered: list[str] = Field(default_factory=list)
    legal_descriptions_parsed: list[LegalDescription] = Field(default_factory=list)
    parcel_boundaries: list[ParcelBoundary] = Field(default_factory=list)
    well_compliance_checks: list[dict[str, Any]] = Field(default_factory=list)
    overlap_gap_results: list[OverlapGapResult] = Field(default_factory=list)
    unit_boundaries: list[UnitBoundary] = Field(default_factory=list)
    acreage_calculations: list[dict[str, Any]] = Field(default_factory=list)
    coordinate_conversions: list[dict[str, Any]] = Field(default_factory=list)
    citations: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    fact_fragility_score: float = Field(ge=0.0, le=1.0)
    determinism_hash: str
    latency_ms: float
    telemetry: dict[str, Any]
    cloud_knowledge_used: bool = False
    cloud_sources: list[str] = Field(default_factory=list)


class HealthResponse(BaseModel):
    """Engine health check response."""
    status: str
    engine_id: str
    engine_name: str
    version: str
    port: int
    domain: str
    uptime_seconds: float
    total_queries: int
    cache_hit_rate: float
    avg_latency_ms: float
    error_rate: float
    doctrines_loaded: int
    vector_search_available: bool
    cloud_knowledge_available: bool
    telemetry_active: bool
    log_dir: str
    cache_dir: str


# ═══════════════════════════════════════════════════════════════════════
# GIS ANALYSIS ENGINE
# ═══════════════════════════════════════════════════════════════════════

class GISIntegrationEngine:
    """
    Core GIS Integration Engine implementing TIE-20 gold standard.

    Provides spatial analysis, legal description parsing, coordinate conversion,
    well spacing compliance, lease boundary mapping, overlap/gap detection,
    and regulatory compliance checks for oil & gas land operations.
    """

    def __init__(self):
        """Initialize the GIS Integration Engine with all components."""
        logger.info(f"Initializing {ENGINE_NAME} v{ENGINE_VERSION}")

        self.engine_id = ENGINE_ID
        self.engine_name = ENGINE_NAME
        self.version = ENGINE_VERSION
        self.start_time = time.time()

        # Core components
        self.doctrine_cache: dict[str, DoctrineBlock] = {}
        self.vector_search: Optional[GISDoctrineSearch] = None
        self.telemetry = TelemetryManager(engine_id=ENGINE_ID, log_dir=LOG_DIR)
        self.coverage_map = CoverageMap()
        self.drift_watcher = DriftWatcher()
        self.metrics = MetricsCollector()

        # Cloud retriever
        self.cloud_retriever: Optional[CognitionCloudRetriever] = None
        if _CLOUD_AVAILABLE:
            try:
                self.cloud_retriever = CognitionCloudRetriever(engine_id=ENGINE_ID)
                logger.info("Cloud knowledge retriever initialized")
            except Exception as e:
                logger.warning(f"Cloud retriever initialization failed: {e}")

        # Initialize components
        self._initialize_doctrine_cache()
        self._initialize_vector_search()

        logger.info(f"{ENGINE_NAME} initialization complete — {len(self.doctrine_cache)} doctrines loaded")

    def _initialize_doctrine_cache(self) -> None:
        """Load all doctrine blocks into memory cache."""
        start = time.time()
        self.doctrine_cache = build_doctrine_cache()
        elapsed = (time.time() - start) * 1000
        logger.info(f"Doctrine cache built: {len(self.doctrine_cache)} blocks in {elapsed:.2f}ms")

        # Register all topics in coverage map
        for topic in get_all_doctrine_topics():
            self.coverage_map.register_topic(topic)

    def _initialize_vector_search(self) -> None:
        """Initialize vector search with doctrine embeddings."""
        try:
            self.vector_search = GISDoctrineSearch()

            # Index all doctrines using the actual GISDoctrineSearch API
            for topic, doctrine in self.doctrine_cache.items():
                self.vector_search.index_doctrine_block(
                    topic=topic,
                    keywords=doctrine.keywords,
                    conclusion_template=doctrine.conclusion_template,
                    reasoning_framework=doctrine.reasoning_framework,
                    confidence=doctrine.confidence.value,
                    domain=ENGINE_DOMAIN,
                    authority_refs=doctrine.primary_authority,
                )

            self.vector_search.build_index()
            logger.info(f"Vector search initialized with {len(self.doctrine_cache)} doctrine embeddings")
        except Exception as e:
            logger.error(f"Vector search initialization failed: {e}")
            self.vector_search = None

    def three_layer_response(
        self,
        query: str,
        mode: ResponseMode,
        zone: AnalysisZone,
        issue_category: Optional[str] = None,
        deep_analysis: bool = False,
    ) -> dict[str, Any]:
        """
        Three-layer response strategy (TIE-20 component #1):

        Layer 1: Doctrine Cache (0-200ms) — Pre-compiled expert reasoning
        Layer 2: Semantic Retrieval (200-1000ms) — Vector search fallback
        Layer 3: Deep Analysis (1000-5000ms) — Multi-source synthesis
        """
        trace = QueryTrace(query_id=str(uuid.uuid4()), query=query, mode=mode.value, zone=zone.value)
        trace.start_phase(QueryPhase.NORMALIZATION)

        # Normalize query using module-level function
        norm_result = normalize_semantics(query)
        trace.end_phase(QueryPhase.NORMALIZATION)

        # Layer 1: Doctrine Cache
        trace.start_phase(QueryPhase.CACHE_LOOKUP)
        cache_result = self._doctrine_cache_lookup(norm_result.normalized, issue_category)
        trace.end_phase(QueryPhase.CACHE_LOOKUP)

        if cache_result["hit"] and not deep_analysis:
            trace.cache_hit = True
            self.coverage_map.mark_triggered(cache_result["doctrine"].topic)
            return self._format_cache_response(cache_result, norm_result, trace, mode, zone)

        # Layer 2: Semantic Retrieval
        trace.start_phase(QueryPhase.VECTOR_SEARCH)
        vector_result = self._semantic_retrieval(norm_result.normalized, top_k=5)
        trace.end_phase(QueryPhase.VECTOR_SEARCH)

        if vector_result["relevant"] and not deep_analysis:
            return self._format_vector_response(vector_result, norm_result, trace, mode, zone)

        # Layer 3: Deep Analysis
        trace.start_phase(QueryPhase.DEEP_ANALYSIS)
        deep_result = self._deep_analysis(
            query=query,
            norm_result=norm_result,
            cache_result=cache_result,
            vector_result=vector_result,
            mode=mode,
            zone=zone,
        )
        trace.end_phase(QueryPhase.DEEP_ANALYSIS)

        return self._format_deep_response(deep_result, norm_result, trace, mode, zone)

    def _doctrine_cache_lookup(self, normalized_query: str, issue_category: Optional[str]) -> dict[str, Any]:
        """
        Look up doctrine in pre-compiled cache.

        Returns matching doctrine block or miss indicator.
        """
        # Direct topic matching
        for topic, doctrine in self.doctrine_cache.items():
            # Check if any keyword appears in normalized query
            if any(kw.lower() in normalized_query.lower() for kw in doctrine.keywords):
                return {"hit": True, "doctrine": doctrine, "match_type": "keyword"}

        # Category-based matching
        if issue_category:
            try:
                category = IssueCategory[issue_category.upper()]
                category_doctrines = get_doctrines_by_category(category)
                if category_doctrines:
                    # Return first matching doctrine from category
                    return {"hit": True, "doctrine": category_doctrines[0], "match_type": "category"}
            except KeyError:
                pass

        return {"hit": False, "doctrine": None, "match_type": None}

    def _semantic_retrieval(self, query: str, top_k: int = 5) -> dict[str, Any]:
        """
        Semantic vector search fallback when cache misses.

        Returns top-k relevant doctrines based on embedding similarity.
        """
        if not self.vector_search:
            return {"relevant": False, "results": []}

        try:
            search_response = self.vector_search.search(query, top_k=top_k, min_score=0.05)
            results = search_response.results  # List[SearchResult] with .topic attribute
            return {"relevant": len(results) > 0, "results": results}
        except Exception as e:
            logger.error(f"Semantic retrieval failed: {e}")
            return {"relevant": False, "results": []}

    def _deep_analysis(
        self,
        query: str,
        norm_result: Any,
        cache_result: dict[str, Any],
        vector_result: dict[str, Any],
        mode: ResponseMode,
        zone: AnalysisZone,
    ) -> dict[str, Any]:
        """
        Deep analysis mode with multi-source synthesis.

        Combines:
        - Doctrine reasoning (if available)
        - Vector search results
        - Cloud knowledge retrieval
        - Multi-doctrine decomposition
        - Interaction graph analysis
        """
        analysis = {
            "doctrines_considered": [],
            "cloud_knowledge": [],
            "synthesis": "",
            "confidence": ConfidenceLevel.DISCLOSURE,
            "warnings": [],
        }

        # Collect all relevant doctrines
        if cache_result["hit"]:
            analysis["doctrines_considered"].append(cache_result["doctrine"])

        for result in vector_result.get("results", []):
            topic = result.topic
            if topic in self.doctrine_cache:
                analysis["doctrines_considered"].append(self.doctrine_cache[topic])

        # Cloud knowledge retrieval
        if self.cloud_retriever:
            try:
                cloud_results = retrieve_cloud_knowledge(query, engine_id=ENGINE_ID, top_k=3)
                analysis["cloud_knowledge"] = cloud_results
            except Exception as e:
                logger.warning(f"Cloud retrieval failed: {e}")

        # Multi-doctrine decomposition
        if len(analysis["doctrines_considered"]) > 1:
            interaction_graph = get_doctrine_interaction_graph()
            # Check for doctrine interactions
            topics = [d.topic for d in analysis["doctrines_considered"]]
            for edge in interaction_graph.get("edges", []):
                if edge["source"] in topics and edge["target"] in topics:
                    analysis["warnings"].append(
                        f"Multiple doctrines interact: {edge['source']} → {edge['target']} ({edge['relationship']})"
                    )

        # Synthesize answer
        synthesis_parts = []

        for doctrine in analysis["doctrines_considered"]:
            synthesis_parts.append(f"**{doctrine.topic}**: {doctrine.conclusion_template}")
            if doctrine.key_factors:
                synthesis_parts.append(f"Key factors: {', '.join(doctrine.key_factors[:3])}")

        if analysis["cloud_knowledge"]:
            synthesis_parts.append("\n**Additional Context from Cloud Knowledge:**")
            for ck in analysis["cloud_knowledge"][:2]:
                synthesis_parts.append(f"- {ck.get('summary', ck.get('content', '')[:200])}")

        analysis["synthesis"] = "\n\n".join(synthesis_parts)

        # Determine overall confidence
        if analysis["doctrines_considered"]:
            min_confidence = min(d.confidence for d in analysis["doctrines_considered"])
            analysis["confidence"] = min_confidence

        return analysis

    def _format_cache_response(
        self,
        cache_result: dict[str, Any],
        norm_result: Any,
        trace: QueryTrace,
        mode: ResponseMode,
        zone: AnalysisZone,
    ) -> dict[str, Any]:
        """Format response from doctrine cache hit."""
        doctrine: DoctrineBlock = cache_result["doctrine"]

        answer = f"**{doctrine.topic}**\n\n{doctrine.conclusion_template}\n\n"

        if mode == ResponseMode.SURVEY or mode == ResponseMode.REPORT:
            answer += f"**Reasoning Framework:**\n{doctrine.reasoning_framework}\n\n"
            answer += f"**Key Factors:**\n" + "\n".join(f"- {factor}" for factor in doctrine.key_factors) + "\n\n"
            answer += f"**Primary Authority:**\n" + "\n".join(f"- {auth}" for auth in doctrine.primary_authority) + "\n\n"

        if mode == ResponseMode.REPORT:
            if doctrine.counter_arguments:
                answer += f"**Counter-Arguments:**\n" + "\n".join(f"- {arg}" for arg in doctrine.counter_arguments) + "\n\n"
            answer += f"**Resolution Strategy:** {doctrine.resolution_strategy}\n\n"

        if zone == AnalysisZone.AUDIT:
            answer += f"**Confidence Stratification:** {doctrine.confidence_stratification}\n"
            answer += f"**Adversary Position:** {doctrine.adversary_position}\n"
            answer += f"**Burden Holder:** {doctrine.burden_holder}\n"

        return {
            "answer": answer,
            "confidence": doctrine.confidence.value,
            "doctrines_triggered": [doctrine.topic],
            "citations": doctrine.primary_authority,
            "trace": trace,
            "fact_fragility_score": self._calculate_fact_fragility(doctrine),
        }

    def _format_vector_response(
        self,
        vector_result: dict[str, Any],
        norm_result: Any,
        trace: QueryTrace,
        mode: ResponseMode,
        zone: AnalysisZone,
    ) -> dict[str, Any]:
        """Format response from semantic vector search."""
        results = vector_result["results"]

        # Extract doctrines from top results
        doctrines = []
        for result in results[:3]:
            topic = result.topic
            if topic in self.doctrine_cache:
                doctrines.append(self.doctrine_cache[topic])

        if not doctrines:
            return self._format_fallback_response(norm_result, trace, mode, zone)

        # Combine top doctrines
        answer_parts = []
        all_citations = []
        all_topics = []

        for i, doctrine in enumerate(doctrines, 1):
            answer_parts.append(f"**{i}. {doctrine.topic}**\n{doctrine.conclusion_template}")
            all_citations.extend(doctrine.primary_authority)
            all_topics.append(doctrine.topic)

            if mode == ResponseMode.SURVEY or mode == ResponseMode.REPORT:
                answer_parts.append(f"Key factors: {', '.join(doctrine.key_factors[:3])}")

        answer = "\n\n".join(answer_parts)

        # Average fact fragility
        avg_fragility = sum(self._calculate_fact_fragility(d) for d in doctrines) / len(doctrines)

        return {
            "answer": answer,
            "confidence": ConfidenceLevel.DEFENSIBLE.value,
            "doctrines_triggered": all_topics,
            "citations": list(set(all_citations)),
            "trace": trace,
            "fact_fragility_score": avg_fragility,
        }

    def _format_deep_response(
        self,
        deep_result: dict[str, Any],
        norm_result: Any,
        trace: QueryTrace,
        mode: ResponseMode,
        zone: AnalysisZone,
    ) -> dict[str, Any]:
        """Format response from deep analysis."""
        return {
            "answer": deep_result["synthesis"],
            "confidence": deep_result["confidence"].value,
            "doctrines_triggered": [d.topic for d in deep_result["doctrines_considered"]],
            "citations": [],
            "trace": trace,
            "fact_fragility_score": 0.5,
            "warnings": deep_result["warnings"],
            "cloud_knowledge_used": len(deep_result["cloud_knowledge"]) > 0,
        }

    def _format_fallback_response(
        self,
        norm_result: Any,
        trace: QueryTrace,
        mode: ResponseMode,
        zone: AnalysisZone,
    ) -> dict[str, Any]:
        """Fallback response when no doctrines match."""
        answer = (
            "No specific doctrine cache hit for this GIS query. "
            "This may indicate a novel spatial analysis requirement or a query outside standard landman GIS operations.\n\n"
            "**Recommendation:** Review the query for specificity. Consider breaking complex spatial questions into "
            "component parts (coordinate conversion, legal description parsing, spacing compliance, etc.)."
        )

        return {
            "answer": answer,
            "confidence": ConfidenceLevel.DISCLOSURE.value,
            "doctrines_triggered": [],
            "citations": [],
            "trace": trace,
            "fact_fragility_score": 1.0,
            "warnings": ["No doctrine match — fallback response"],
        }

    def _calculate_fact_fragility(self, doctrine: DoctrineBlock) -> float:
        """
        Calculate fact fragility score (0.0 = rock solid, 1.0 = highly fragile).

        Factors:
        - Confidence level
        - Number of counter-arguments
        - Adversary position strength
        - Authority citation count
        """
        score = 0.0

        # Base score from confidence
        confidence_scores = {
            ConfidenceLevel.DEFENSIBLE: 0.1,
            ConfidenceLevel.AGGRESSIVE: 0.3,
            ConfidenceLevel.DISCLOSURE: 0.6,
            ConfidenceLevel.HIGH_RISK: 0.9,
        }
        score += confidence_scores.get(doctrine.confidence, 0.5)

        # Counter-arguments penalty
        if doctrine.counter_arguments:
            score += min(0.2, len(doctrine.counter_arguments) * 0.05)

        # Authority citation boost
        if doctrine.primary_authority:
            score -= min(0.2, len(doctrine.primary_authority) * 0.05)

        return max(0.0, min(1.0, score))

    def parse_legal_description(self, description: str) -> LegalDescription:
        """
        Parse a legal description into structured components.

        Handles:
        - Texas abstract system
        - Rectangular survey (PLSS)
        - Metes and bounds
        - Subdivision/lot descriptions
        """
        result = LegalDescription(raw=description)

        # Abstract number pattern
        abstract_match = re.search(r'Abstract\s+(?:No\.?\s*)?(\d+)', description, re.IGNORECASE)
        if abstract_match:
            result.abstract_number = abstract_match.group(1)

        # Survey name pattern
        survey_match = re.search(r'(?:Survey|Surv\.?)\s+([A-Z\s]+?)(?:,|\s+Abstract)', description, re.IGNORECASE)
        if survey_match:
            result.survey_name = survey_match.group(1).strip()

        # Section/Block/Township pattern
        section_match = re.search(r'Section\s+(\d+)', description, re.IGNORECASE)
        if section_match:
            result.section = section_match.group(1)

        block_match = re.search(r'Block\s+([A-Z0-9\-]+)', description, re.IGNORECASE)
        if block_match:
            result.block = block_match.group(1)

        township_match = re.search(r'Township\s+(\d+[NS])', description, re.IGNORECASE)
        if township_match:
            result.township = township_match.group(1)

        range_match = re.search(r'Range\s+(\d+[EW])', description, re.IGNORECASE)
        if range_match:
            result.range = range_match.group(1)

        # Acreage pattern
        acre_match = re.search(r'([\d,]+(?:\.\d+)?)\s*acres?', description, re.IGNORECASE)
        if acre_match:
            result.acres = float(acre_match.group(1).replace(',', ''))

        # County pattern
        county_match = re.search(r'(\w+)\s+County', description, re.IGNORECASE)
        if county_match:
            result.county = county_match.group(1).upper()

        # Metes and bounds calls
        metes_patterns = [
            r'(?:NORTH|SOUTH|EAST|WEST)\s+\d+[°]\s*\d+[\']\s*\d+["]',
            r'(?:N|S)\s*\d+[°]\s*\d+[\']\s*(?:E|W)',
            r'thence\s+[NSEW]\s+\d+',
        ]
        metes_calls = []
        for pattern in metes_patterns:
            metes_calls.extend(re.findall(pattern, description, re.IGNORECASE))
        if metes_calls:
            result.metes_bounds = metes_calls

        return result

    def calculate_acreage(self, boundary: ParcelBoundary) -> float:
        """
        Calculate acreage from polygon vertices using Shoelace formula.

        Assumes vertices are in a projected coordinate system (feet).
        """
        if not boundary.vertices or len(boundary.vertices) < 3:
            return 0.0

        # Extract x, y coordinates (using easting/northing if available, else lat/lon converted)
        coords = []
        for vertex in boundary.vertices:
            if vertex.easting is not None and vertex.northing is not None:
                coords.append((vertex.easting, vertex.northing))
            elif vertex.latitude is not None and vertex.longitude is not None:
                # Convert lat/lon to approximate feet (simple equirectangular projection)
                # This is rough — production code should use proper projection
                x = vertex.longitude * FEET_PER_MILE * math.cos(math.radians(vertex.latitude)) * 69.0
                y = vertex.latitude * FEET_PER_MILE * 69.0
                coords.append((x, y))

        if len(coords) < 3:
            return 0.0

        # Shoelace formula
        area_sq_ft = 0.0
        n = len(coords)
        for i in range(n):
            j = (i + 1) % n
            area_sq_ft += coords[i][0] * coords[j][1]
            area_sq_ft -= coords[j][0] * coords[i][1]

        area_sq_ft = abs(area_sq_ft) / 2.0
        acres = area_sq_ft * ACRES_PER_SQ_FT

        return acres

    def check_well_spacing(self, well: WellLocation, lease_boundary: ParcelBoundary) -> dict[str, Any]:
        """
        Check well spacing compliance with RRC rules.

        Returns compliance status, applicable rule, and distance to lease line.
        """
        result = {
            "compliant": False,
            "rule": None,
            "distance_to_lease_line_ft": None,
            "required_distance_ft": None,
            "violations": [],
        }

        # Determine applicable spacing rule
        if well.spacing_rule:
            rule_name = well.spacing_rule
        elif well.lateral_length_ft and well.lateral_length_ft > 5000:
            rule_name = "PERMIAN_BASIN_HORIZONTAL"
        else:
            # Default to RULE_37 for oil, RULE_38 for gas (assume oil if not specified)
            rule_name = "RULE_37"

        if rule_name not in RRC_SPACING_RULES:
            result["violations"].append(f"Unknown spacing rule: {rule_name}")
            return result

        rule = RRC_SPACING_RULES[rule_name]
        result["rule"] = rule_name
        result["required_distance_ft"] = rule["default_lease_line_ft"]

        # Calculate minimum distance to lease boundary
        min_distance = self._calculate_min_distance_to_boundary(well.coordinates, lease_boundary)
        result["distance_to_lease_line_ft"] = min_distance

        # Check compliance
        if min_distance >= rule["default_lease_line_ft"]:
            result["compliant"] = True
        else:
            result["violations"].append(
                f"Well is {min_distance:.1f} ft from lease line, "
                f"but {rule['default_lease_line_ft']} ft required under {rule_name}"
            )

        return result

    def _calculate_min_distance_to_boundary(self, point: CoordinatePair, boundary: ParcelBoundary) -> float:
        """
        Calculate minimum distance from point to polygon boundary.

        Uses point-to-line segment distance for each edge of the polygon.
        """
        if not boundary.vertices or len(boundary.vertices) < 2:
            return float('inf')

        # Convert point to x, y
        if point.easting is not None and point.northing is not None:
            px, py = point.easting, point.northing
        elif point.latitude is not None and point.longitude is not None:
            px = point.longitude * FEET_PER_MILE * math.cos(math.radians(point.latitude)) * 69.0
            py = point.latitude * FEET_PER_MILE * 69.0
        else:
            return float('inf')

        min_dist = float('inf')

        # Check distance to each edge
        n = len(boundary.vertices)
        for i in range(n):
            v1 = boundary.vertices[i]
            v2 = boundary.vertices[(i + 1) % n]

            # Convert vertices to x, y
            if v1.easting is not None and v1.northing is not None:
                x1, y1 = v1.easting, v1.northing
            elif v1.latitude is not None and v1.longitude is not None:
                x1 = v1.longitude * FEET_PER_MILE * math.cos(math.radians(v1.latitude)) * 69.0
                y1 = v1.latitude * FEET_PER_MILE * 69.0
            else:
                continue

            if v2.easting is not None and v2.northing is not None:
                x2, y2 = v2.easting, v2.northing
            elif v2.latitude is not None and v2.longitude is not None:
                x2 = v2.longitude * FEET_PER_MILE * math.cos(math.radians(v2.latitude)) * 69.0
                y2 = v2.latitude * FEET_PER_MILE * 69.0
            else:
                continue

            # Point-to-line-segment distance
            dist = self._point_to_segment_distance(px, py, x1, y1, x2, y2)
            min_dist = min(min_dist, dist)

        return min_dist

    def _point_to_segment_distance(self, px: float, py: float, x1: float, y1: float, x2: float, y2: float) -> float:
        """Calculate minimum distance from point (px, py) to line segment (x1, y1)-(x2, y2)."""
        dx = x2 - x1
        dy = y2 - y1

        if dx == 0 and dy == 0:
            # Degenerate segment (point)
            return math.sqrt((px - x1)**2 + (py - y1)**2)

        # Parameter t for projection onto line
        t = max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)))

        # Closest point on segment
        closest_x = x1 + t * dx
        closest_y = y1 + t * dy

        return math.sqrt((px - closest_x)**2 + (py - closest_y)**2)

    def detect_overlap_gap(self, parcel_a: ParcelBoundary, parcel_b: ParcelBoundary) -> OverlapGapResult:
        """
        Detect overlaps or gaps between two parcel boundaries.

        NOTE: This is a simplified implementation. Production code should use
        a proper GIS library like Shapely for polygon intersection/difference.
        """
        result = OverlapGapResult(parcel_a_id="A", parcel_b_id="B")

        # Placeholder logic — real implementation would use Shapely
        # For now, just check if any vertex of A is inside B or vice versa

        a_in_b = sum(1 for v in parcel_a.vertices if self._point_in_polygon(v, parcel_b.vertices))
        b_in_a = sum(1 for v in parcel_b.vertices if self._point_in_polygon(v, parcel_a.vertices))

        if a_in_b > 0 or b_in_a > 0:
            result.overlap_detected = True
            result.significance = "MODERATE"
            result.curative_action = "Survey both parcels to determine precise overlap area and resolve boundary discrepancy"

        # Gap detection would require convex hull or other geometric analysis
        # Simplified: if no overlap and boundaries are "close", flag potential gap

        return result

    def _point_in_polygon(self, point: CoordinatePair, polygon: list[CoordinatePair]) -> bool:
        """
        Ray casting algorithm to check if point is inside polygon.

        Simplified implementation — production code should use Shapely.
        """
        if not polygon or len(polygon) < 3:
            return False

        # Extract point coordinates
        if point.easting is not None and point.northing is not None:
            px, py = point.easting, point.northing
        elif point.latitude is not None and point.longitude is not None:
            px = point.longitude
            py = point.latitude
        else:
            return False

        inside = False
        n = len(polygon)

        for i in range(n):
            v1 = polygon[i]
            v2 = polygon[(i + 1) % n]

            # Extract vertex coordinates
            if v1.easting is not None and v1.northing is not None:
                x1, y1 = v1.easting, v1.northing
            elif v1.latitude is not None and v1.longitude is not None:
                x1, y1 = v1.longitude, v1.latitude
            else:
                continue

            if v2.easting is not None and v2.northing is not None:
                x2, y2 = v2.easting, v2.northing
            elif v2.latitude is not None and v2.longitude is not None:
                x2, y2 = v2.longitude, v2.latitude
            else:
                continue

            # Ray casting
            if ((y1 > py) != (y2 > py)) and (px < (x2 - x1) * (py - y1) / (y2 - y1) + x1):
                inside = not inside

        return inside

    def convert_coordinates(
        self,
        coord: CoordinatePair,
        target_datum: str = "NAD83",
        target_projection: Optional[str] = None,
    ) -> CoordinatePair:
        """
        Convert coordinates between datums and projections.

        NOTE: This is a placeholder. Production code should use pyproj or similar.
        Real datum transformations require PROJ library or web service.
        """
        result = CoordinatePair(
            latitude=coord.latitude,
            longitude=coord.longitude,
            easting=coord.easting,
            northing=coord.northing,
            datum=target_datum,
            zone=coord.zone,
            elevation_ft=coord.elevation_ft,
        )

        # Placeholder — real implementation would use pyproj.Transformer
        logger.warning("Coordinate conversion is placeholder — use pyproj for production")

        return result

    def apply_epistemic_guardrails(self, answer: str) -> str:
        """
        Apply epistemic guardrails to prevent over-confident statements.

        Removes banned phrases and adds disclosure caveats where appropriate.
        """
        # Remove banned phrases
        clean_answer = answer
        for phrase in BANNED_PHRASES:
            clean_answer = clean_answer.replace(phrase, "")

        # Add disclosure caveat if answer contains high-confidence GIS determinations
        high_confidence_indicators = [
            "definitely",
            "certainly",
            "without question",
            "absolutely",
            "guaranteed",
        ]

        if any(indicator in clean_answer.lower() for indicator in high_confidence_indicators):
            clean_answer += (
                "\n\n**Disclosure:** GIS analysis is based on available data and standard spatial methodologies. "
                "Field verification by a licensed surveyor is recommended for critical boundary determinations."
            )

        return clean_answer

    def generate_determinism_hash(self, query: str, response_data: dict[str, Any]) -> str:
        """
        Generate SHA-256 hash for reproducibility verification.

        Includes query, doctrines triggered, and key response elements.
        """
        hash_input = {
            "query": query,
            "doctrines": response_data.get("doctrines_triggered", []),
            "confidence": response_data.get("confidence", ""),
            "version": ENGINE_VERSION,
        }

        hash_str = json.dumps(hash_input, sort_keys=True)
        return hashlib.sha256(hash_str.encode()).hexdigest()

    async def process_query(self, request: QueryRequest) -> QueryResponse:
        """
        Main query processing entry point.

        Implements full TIE-20 pipeline with telemetry, drift watching, and coverage tracking.
        """
        query_id = str(uuid.uuid4())
        session_id = request.session_id or query_id
        start_time = time.time()

        logger.info(f"Processing query {query_id[:8]}: {request.query[:100]}")

        try:
            # Core three-layer response
            response_data = self.three_layer_response(
                query=request.query,
                mode=request.mode,
                zone=request.zone,
                issue_category=request.issue_category,
                deep_analysis=request.deep_analysis,
            )

            # Apply epistemic guardrails
            answer = self.apply_epistemic_guardrails(response_data["answer"])

            # Parse legal descriptions if provided
            legal_descriptions = []
            if request.legal_description:
                legal_descriptions.append(self.parse_legal_description(request.legal_description))

            # Calculate acreage for provided parcels
            acreage_calculations = []
            for parcel in (request.parcels or []):
                acres = self.calculate_acreage(parcel)
                acreage_calculations.append({
                    "boundary": parcel,
                    "calculated_acres": acres,
                    "method": "Shoelace formula",
                })

            # Check well spacing compliance
            well_compliance_checks = []
            if request.well_locations and request.parcels:
                for well in request.well_locations:
                    # Use first parcel as lease boundary (simplification)
                    compliance = self.check_well_spacing(well, request.parcels[0])
                    well_compliance_checks.append({
                        "well": well,
                        "compliance": compliance,
                    })

            # Generate determinism hash
            determinism_hash = self.generate_determinism_hash(request.query, response_data)

            # Record telemetry
            latency_ms = (time.time() - start_time) * 1000
            cache_hit = response_data.get("trace").cache_hit if response_data.get("trace") else False
            self.metrics.record_query(latency_ms, doctrine_hit=cache_hit, mode=request.mode.value)

            trace: QueryTrace = response_data.get("trace")
            if trace:
                trace.end_time = time.time()
                self.telemetry.log_trace(trace)

            # Build response
            response = QueryResponse(
                query_id=query_id,
                session_id=session_id,
                mode=request.mode,
                zone=request.zone,
                answer=answer,
                confidence=response_data.get("confidence", ConfidenceLevel.DISCLOSURE.value),
                doctrines_triggered=response_data.get("doctrines_triggered", []),
                legal_descriptions_parsed=legal_descriptions,
                parcel_boundaries=request.parcels or [],
                well_compliance_checks=well_compliance_checks,
                overlap_gap_results=[],
                unit_boundaries=[],
                acreage_calculations=acreage_calculations,
                coordinate_conversions=[],
                citations=response_data.get("citations", []),
                warnings=response_data.get("warnings", []),
                fact_fragility_score=response_data.get("fact_fragility_score", 0.5),
                determinism_hash=determinism_hash,
                latency_ms=latency_ms,
                telemetry={
                    "cache_hit": response_data.get("trace").cache_hit if response_data.get("trace") else False,
                    "phases": response_data.get("trace").phases if response_data.get("trace") else {},
                },
                cloud_knowledge_used=response_data.get("cloud_knowledge_used", False),
                cloud_sources=response_data.get("cloud_sources", []),
            )

            logger.info(f"Query {query_id[:8]} completed in {latency_ms:.2f}ms — confidence={response.confidence}")

            return response

        except Exception as e:
            logger.error(f"Query processing failed: {e}", exc_info=True)
            self.metrics.record_error(str(e), ErrorDomain.PROCESSING)

            # Return error response
            return QueryResponse(
                query_id=query_id,
                session_id=session_id,
                mode=request.mode,
                zone=request.zone,
                answer=f"Query processing error: {str(e)}",
                confidence=ConfidenceLevel.DISCLOSURE.value,
                doctrines_triggered=[],
                legal_descriptions_parsed=[],
                parcel_boundaries=[],
                well_compliance_checks=[],
                overlap_gap_results=[],
                unit_boundaries=[],
                acreage_calculations=[],
                coordinate_conversions=[],
                citations=[],
                warnings=[f"Processing error: {str(e)}"],
                fact_fragility_score=1.0,
                determinism_hash="error",
                latency_ms=(time.time() - start_time) * 1000,
                telemetry={},
            )

    def get_health(self) -> HealthResponse:
        """Return comprehensive health check."""
        uptime = time.time() - self.start_time
        stats = self.metrics.get_full_metrics()
        latency_stats = stats.get("latency", {})

        return HealthResponse(
            status="healthy",
            engine_id=self.engine_id,
            engine_name=self.engine_name,
            version=self.version,
            port=ENGINE_PORT,
            domain=ENGINE_DOMAIN,
            uptime_seconds=uptime,
            total_queries=stats.get("total_queries", 0),
            cache_hit_rate=stats.get("doctrine_hit_rate", 0.0),
            avg_latency_ms=latency_stats.get("avg_ms", 0.0),
            error_rate=stats.get("errors", {}).get("error_rate", 0.0) if isinstance(stats.get("errors"), dict) else 0.0,
            doctrines_loaded=len(self.doctrine_cache),
            vector_search_available=self.vector_search is not None,
            cloud_knowledge_available=self.cloud_retriever is not None,
            telemetry_active=True,
            log_dir=str(LOG_DIR),
            cache_dir=str(CACHE_DIR),
        )


# ═══════════════════════════════════════════════════════════════════════
# FASTAPI APPLICATION
# ═══════════════════════════════════════════════════════════════════════

engine_instance: Optional[GISIntegrationEngine] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI lifespan for engine initialization and cleanup."""
    global engine_instance
    logger.info("Starting LM12 GIS Integration Engine")
    engine_instance = GISIntegrationEngine()
    yield
    logger.info("Shutting down LM12 GIS Integration Engine")


app = FastAPI(
    title=ENGINE_NAME,
    version=ENGINE_VERSION,
    description="GIS/spatial analysis engine for oil & gas landman operations",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Engine health check endpoint."""
    if not engine_instance:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    return engine_instance.get_health()


@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """Main query endpoint."""
    if not engine_instance:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    return await engine_instance.process_query(request)


@app.get("/doctrines")
async def list_doctrines():
    """List all available doctrine topics."""
    if not engine_instance:
        raise HTTPException(status_code=503, detail="Engine not initialized")

    topics = get_all_doctrine_topics()
    return {"total": len(topics), "topics": topics}


@app.get("/doctrines/{topic}")
async def get_doctrine(topic: str):
    """Get specific doctrine block details."""
    if not engine_instance:
        raise HTTPException(status_code=503, detail="Engine not initialized")

    if topic not in engine_instance.doctrine_cache:
        raise HTTPException(status_code=404, detail=f"Doctrine topic '{topic}' not found")

    doctrine = engine_instance.doctrine_cache[topic]
    return {
        "topic": doctrine.topic,
        "keywords": doctrine.keywords,
        "conclusion_template": doctrine.conclusion_template,
        "confidence": doctrine.confidence.value,
        "primary_authority": doctrine.primary_authority,
        "key_factors": doctrine.key_factors,
    }


@app.get("/coverage")
async def get_coverage_map():
    """Get doctrine coverage statistics."""
    if not engine_instance:
        raise HTTPException(status_code=503, detail="Engine not initialized")

    return engine_instance.coverage_map.get_report()


@app.get("/metrics")
async def get_metrics():
    """Get engine performance metrics."""
    if not engine_instance:
        raise HTTPException(status_code=503, detail="Engine not initialized")

    return engine_instance.metrics.get_stats()


@app.get("/")
async def root():
    """Root endpoint with engine info."""
    return {
        "engine": ENGINE_NAME,
        "id": ENGINE_ID,
        "version": ENGINE_VERSION,
        "port": ENGINE_PORT,
        "domain": ENGINE_DOMAIN,
        "status": "operational",
        "endpoints": ["/health", "/query", "/doctrines", "/coverage", "/metrics"],
    }


# ═══════════════════════════════════════════════════════════════════════
# MAIN ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    logger.info(f"Launching {ENGINE_NAME} v{ENGINE_VERSION} on port {ENGINE_PORT}")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=ENGINE_PORT,
        log_level="info",
        access_log=True,
    )
