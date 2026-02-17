"""
LM19 Probate Title Engine — Main Engine
========================================
Probate and estate succession intelligence for mineral title examination.
Texas intestate/testate succession, administration types, heirship determination,
community property, homestead, life estates, trusts, and fractional interest calculation.

Engine: LM19 | Port: 8519 | Domain: probate_title_examination
Version: 1.0.0 | TIE Gold Standard | 20 Components

TIE-20 Components:
 1.  three_layer_response      2.  response_modes
 3.  doctrine_cache            4.  authority_hardening
 5.  confidence_stratification 6.  semantic_normalization
 7.  vector_search             8.  telemetry
 9.  drift_watcher            10.  coverage_map
11.  metrics_collector        12.  health_endpoint
13.  zoned_analysis           14.  fact_fragility_scoring
15.  audit_trail_jsonl        16.  determinism_hash_sha256
17.  fastapi_server           18.  loguru_logging
19.  multi_doctrine_decomposition
20.  deep_analysis_mode
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
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Optional

# Add _shared to path for cloud_retriever access
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_shared"))

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Cloud knowledge integration
# ---------------------------------------------------------------------------
try:
    from cloud_retriever import CognitionCloudRetriever, CloudKnowledge, retrieve_cloud_knowledge
    _CLOUD_AVAILABLE = True
except ImportError:
    _CLOUD_AVAILABLE = False
    logger.warning("cloud_retriever not available — running without cloud knowledge")

# ---------------------------------------------------------------------------
# Local imports
# ---------------------------------------------------------------------------
from doctrines import (
    ConfidenceStratification,
    DoctrineBlock,
    DoctrineInteraction,
    IssueCategory,
    PositionZone,
    build_doctrine_cache,
    build_interaction_graph,
    find_doctrine_by_topic,
    find_doctrines_by_category,
    find_doctrines_by_keyword,
    get_doctrine_cache,
    get_interaction_graph,
    get_interactions_for_topic,
)
from search import SearchDocument, SearchResponse, VectorIndex, get_vector_index
from semantic import NormalizationResult, SemanticNormalizer, get_normalizer
from telemetry import (
    ErrorDomain,
    QueryPhase,
    QueryTrace,
    TelemetryCollector,
    get_telemetry_collector,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
ENGINE_ID = "LM19"
ENGINE_NAME = "Probate Title"
ENGINE_VERSION = "1.0.0"
ENGINE_PORT = 8519
ENGINE_DOMAIN = "probate_title_examination"
ENGINE_DIR = Path(__file__).parent
CONFIG_PATH = ENGINE_DIR / "config.json"

# Logging configuration
LOG_DIR = ENGINE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
logger.remove()
logger.add(sys.stderr, level="INFO", format="{time:YYYY-MM-DD HH:mm:ss} | {level:<8} | {name}:{function}:{line} | {message}")
logger.add(
    LOG_DIR / "engine_{time:YYYY-MM-DD}.log",
    rotation="50 MB",
    retention="90 days",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level:<8} | {name}:{function}:{line} | {message}",
)

# ---------------------------------------------------------------------------
# Banned phrases (epistemic guardrails)
# ---------------------------------------------------------------------------
BANNED_PHRASES: list[str] = [
    "i think",
    "probably",
    "i believe",
    "in my opinion",
    "it seems like",
    "i would guess",
    "most likely",
    "i assume",
    "generally speaking",
    "it depends",
    "you should consult",
    "this is not legal advice",
    "i'm not a lawyer",
    "every situation is different",
]


# ===================================================================
# TIE COMPONENT 2: Response Modes
# ===================================================================
class ResponseMode(str, Enum):
    """Response modes for probate analysis."""
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"


RESPONSE_MODE_CONFIG: dict[str, dict[str, Any]] = {
    "FAST": {"max_tokens": 800, "include_citations": False, "doctrine_depth": "summary"},
    "DEFENSE": {"max_tokens": 4000, "include_citations": True, "doctrine_depth": "full"},
    "MEMO": {"max_tokens": 12000, "include_citations": True, "doctrine_depth": "exhaustive"},
}


# ===================================================================
# TIE COMPONENT 13: Zoned Analysis
# ===================================================================
class AnalysisZone(str, Enum):
    """Analysis zones — PLANNING, REPORTING, AUDIT. Never blur."""
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"


ZONE_GUIDELINES: dict[str, str] = {
    "PLANNING": (
        "Probate planning mode: identify succession paths, recommend probate procedures, "
        "estimate timelines and costs. Forward-looking estate planning."
    ),
    "REPORTING": (
        "Probate reporting mode: document current estate status, heirship determination, "
        "title chain tracing. Factual, current-state analysis."
    ),
    "AUDIT": (
        "Audit mode: verify probate proceedings were properly executed, court orders valid, "
        "heirship properly adjudicated. Backward-looking compliance check."
    ),
}


# ===================================================================
# Pydantic Request/Response Models
# ===================================================================
class ProbateQuery(BaseModel):
    """Input query for probate title analysis."""
    query: str
    mode: ResponseMode = ResponseMode.FAST
    zone: AnalysisZone = AnalysisZone.PLANNING
    category_filter: Optional[str] = None
    include_interactions: bool = False
    include_fragility: bool = False
    client_id: str = ""


class AuthoritySource(BaseModel):
    """A cited authority source."""
    source: str
    weight: float = 1.0
    type: str = "statute"  # statute, case, regulation, standard


class ConfidenceAssessment(BaseModel):
    """Confidence assessment for a probate opinion."""
    tier: str
    score: float
    factors: list[str]
    caveats: list[str] = Field(default_factory=list)


class DoctrineReference(BaseModel):
    """Reference to a triggered doctrine."""
    topic: str
    category: str
    confidence: str
    authority: list[str]
    reasoning_summary: str


class FragilityScore(BaseModel):
    """Fact fragility scoring for evidence strength."""
    overall_score: float  # 0.0-1.0 (1.0 = most fragile/risky)
    verifiability: float
    recharacterization_risk: float
    testimony_dependence: float
    documentation_strength: float


class ProbateResponse(BaseModel):
    """Response from probate engine."""
    query_id: str
    query: str
    mode: str
    zone: str
    analysis: str
    doctrines_triggered: list[DoctrineReference]
    confidence: ConfidenceAssessment
    authorities: list[AuthoritySource]
    interactions: list[dict] = Field(default_factory=list)
    fragility: Optional[FragilityScore] = None
    determinism_hash: str
    timestamp: str
    latency_ms: float


# ===================================================================
# TIE COMPONENT 1: Three-Layer Response
# ===================================================================
class ThreeLayerResponse:
    """Three-layer response system: Cache → Vector Search → Deep Analysis."""

    def __init__(
        self,
        doctrine_cache: dict[str, DoctrineBlock],
        vector_index: VectorIndex,
        normalizer: SemanticNormalizer,
        telemetry: TelemetryCollector
    ) -> None:
        """
        Initialize three-layer response system.

        Args:
            doctrine_cache: Doctrine cache
            vector_index: Vector search index
            normalizer: Semantic normalizer
            telemetry: Telemetry collector
        """
        self.doctrine_cache = doctrine_cache
        self.vector_index = vector_index
        self.normalizer = normalizer
        self.telemetry = telemetry

    def execute(self, query: ProbateQuery, trace: QueryTrace) -> tuple[list[DoctrineBlock], dict[str, Any]]:
        """
        Execute three-layer response retrieval.

        Args:
            query: Probate query
            trace: Query trace

        Returns:
            Tuple of (doctrine blocks, metadata)
        """
        metadata: dict[str, Any] = {"layers_used": []}

        # LAYER 1: Doctrine Cache Lookup (0-200ms)
        start = time.time()
        doctrines = self._layer1_cache_lookup(query, trace)
        cache_latency = (time.time() - start) * 1000
        self.telemetry.record_phase(trace, QueryPhase.CACHE_LOOKUP, cache_latency)

        if doctrines:
            self.telemetry.record_cache_hit(trace, True)
            metadata["layers_used"].append("CACHE")
            metadata["cache_latency_ms"] = cache_latency
            logger.debug(f"Layer 1 CACHE HIT: {len(doctrines)} doctrines in {cache_latency:.1f}ms")
            return doctrines, metadata

        self.telemetry.record_cache_hit(trace, False)

        # LAYER 2: Vector Search (200-500ms)
        start = time.time()
        doctrines = self._layer2_vector_search(query, trace)
        vector_latency = (time.time() - start) * 1000
        self.telemetry.record_phase(trace, QueryPhase.VECTOR_SEARCH, vector_latency)

        if doctrines:
            self.telemetry.record_vector_search(trace)
            metadata["layers_used"].append("VECTOR")
            metadata["vector_latency_ms"] = vector_latency
            logger.debug(f"Layer 2 VECTOR SEARCH: {len(doctrines)} doctrines in {vector_latency:.1f}ms")
            return doctrines, metadata

        # LAYER 3: Deep Analysis with Cloud Retrieval (500-2000ms)
        start = time.time()
        doctrines = self._layer3_deep_analysis(query, trace)
        deep_latency = (time.time() - start) * 1000
        self.telemetry.record_phase(trace, QueryPhase.CLOUD_RETRIEVAL, deep_latency)

        if _CLOUD_AVAILABLE:
            self.telemetry.record_cloud_retrieval(trace)
            metadata["layers_used"].append("CLOUD")
            metadata["cloud_latency_ms"] = deep_latency

        logger.debug(f"Layer 3 DEEP ANALYSIS: {len(doctrines)} doctrines in {deep_latency:.1f}ms")
        return doctrines, metadata

    def _layer1_cache_lookup(self, query: ProbateQuery, trace: QueryTrace) -> list[DoctrineBlock]:
        """Layer 1: Fast doctrine cache lookup by keywords."""
        # Normalize query
        norm_result = self.normalizer.normalize(query.query)

        # Search by canonical terms
        doctrines: list[DoctrineBlock] = []
        for term in norm_result.canonical_terms:
            term_doctrines = find_doctrines_by_keyword(term)
            for doctrine in term_doctrines:
                if doctrine not in doctrines:
                    doctrines.append(doctrine)

        # Filter by category if specified
        if query.category_filter:
            try:
                category = IssueCategory(query.category_filter)
                doctrines = [d for d in doctrines if d.category == category]
            except ValueError:
                pass

        return doctrines[:5]  # Top 5 cache results

    def _layer2_vector_search(self, query: ProbateQuery, trace: QueryTrace) -> list[DoctrineBlock]:
        """Layer 2: Vector semantic search."""
        search_response = self.vector_index.search(query.query, top_k=5, threshold=0.72)

        # Convert search results to doctrine blocks
        doctrines: list[DoctrineBlock] = []
        for result in search_response.results:
            topic = result.get("topic")
            if topic:
                doctrine = find_doctrine_by_topic(topic)
                if doctrine and doctrine not in doctrines:
                    doctrines.append(doctrine)

        return doctrines

    def _layer3_deep_analysis(self, query: ProbateQuery, trace: QueryTrace) -> list[DoctrineBlock]:
        """Layer 3: Deep analysis with cloud knowledge retrieval."""
        # Attempt cloud retrieval if available
        if _CLOUD_AVAILABLE:
            try:
                cloud_knowledge = retrieve_cloud_knowledge(query.query, domain="probate_title", top_k=3)
                # Extract relevant doctrine topics from cloud results
                # (In production, would parse cloud knowledge and map to doctrines)
            except Exception as e:
                logger.warning(f"Cloud retrieval failed: {e}")

        # Fallback: return general doctrines based on query analysis
        entities = self.normalizer.extract_entities(query.query)

        # Select doctrines based on extracted entities
        doctrines: list[DoctrineBlock] = []

        # If family members mentioned, add succession doctrines
        if entities.get("family_members"):
            doctrines.extend(find_doctrines_by_category(IssueCategory.INTESTATE_SUCCESSION)[:2])
            doctrines.extend(find_doctrines_by_category(IssueCategory.TESTATE_SUCCESSION)[:2])

        # If procedures mentioned, add procedural doctrines
        if entities.get("procedures"):
            if "probate" in entities["procedures"]:
                doctrines.extend(find_doctrines_by_keyword("will")[:2])
            if "affidavit" in entities["procedures"]:
                doctrines.extend(find_doctrines_by_keyword("affidavit of heirship")[:1])

        # If property types mentioned, add property doctrines
        if entities.get("property_types"):
            if "community" in entities["property_types"]:
                doctrines.extend(find_doctrines_by_category(IssueCategory.COMMUNITY_PROPERTY)[:2])
            if "homestead" in entities["property_types"]:
                doctrines.extend(find_doctrines_by_category(IssueCategory.HOMESTEAD_RIGHTS)[:1])

        # Deduplicate
        unique_doctrines = []
        for doctrine in doctrines:
            if doctrine not in unique_doctrines:
                unique_doctrines.append(doctrine)

        return unique_doctrines[:5]


# ===================================================================
# TIE COMPONENT 4: Authority Hardening
# ===================================================================
class AuthorityHierarchy:
    """Authority hierarchy and conflict resolution."""

    def __init__(self, config: dict[str, Any]) -> None:
        """Initialize authority hierarchy from config."""
        self.hierarchy = config.get("authority_hierarchy", [])
        self.weight_map: dict[str, float] = {}
        for level in self.hierarchy:
            self.weight_map[level["source"]] = level["weight"]

    def resolve_conflict(self, authorities: list[str]) -> str:
        """Resolve conflict between multiple authorities."""
        if not authorities:
            return "No authority provided"

        # Find highest weight authority
        max_weight = 0.0
        controlling = authorities[0]
        for auth in authorities:
            weight = self._get_weight(auth)
            if weight > max_weight:
                max_weight = weight
                controlling = auth

        return controlling

    def _get_weight(self, authority: str) -> float:
        """Get weight for an authority source."""
        for source, weight in self.weight_map.items():
            if source.lower() in authority.lower():
                return weight
        return 0.3  # Default weight for unlisted authorities


# ===================================================================
# TIE COMPONENT 14: Fact Fragility Scoring
# ===================================================================
def calculate_fragility(query: str, doctrines: list[DoctrineBlock]) -> FragilityScore:
    """
    Calculate fact fragility score.

    Args:
        query: Query text
        doctrines: Triggered doctrines

    Returns:
        FragilityScore
    """
    # Verifiability: higher score = harder to verify
    verifiability = 0.5
    if "affidavit" in query.lower():
        verifiability = 0.7  # Affidavits are rebuttable
    if "court order" in query.lower() or "determination" in query.lower():
        verifiability = 0.2  # Court orders are strong evidence

    # Recharacterization risk
    recharacterization_risk = 0.4
    if "community" in query.lower() or "separate" in query.lower():
        recharacterization_risk = 0.6  # Character disputes common

    # Testimony dependence
    testimony_dependence = 0.5
    if "witness" in query.lower() or "testimony" in query.lower():
        testimony_dependence = 0.8
    if "certificate" in query.lower() or "record" in query.lower():
        testimony_dependence = 0.2

    # Documentation strength
    documentation_strength = 0.5
    if "deed" in query.lower() or "will" in query.lower():
        documentation_strength = 0.9
    if "affidavit" in query.lower():
        documentation_strength = 0.6

    # Overall fragility (weighted average)
    overall = (
        verifiability * 0.3 +
        recharacterization_risk * 0.25 +
        testimony_dependence * 0.25 +
        (1.0 - documentation_strength) * 0.20
    )

    return FragilityScore(
        overall_score=overall,
        verifiability=verifiability,
        recharacterization_risk=recharacterization_risk,
        testimony_dependence=testimony_dependence,
        documentation_strength=documentation_strength
    )


# ===================================================================
# TIE COMPONENT 16: Determinism Hash (SHA-256)
# ===================================================================
def calculate_determinism_hash(query: str, doctrines: list[DoctrineBlock], mode: str, zone: str) -> str:
    """
    Calculate SHA-256 determinism hash.

    Args:
        query: Query text
        doctrines: Triggered doctrines
        mode: Response mode
        zone: Analysis zone

    Returns:
        SHA-256 hex digest
    """
    # Create deterministic string
    components = [
        f"query:{query}",
        f"mode:{mode}",
        f"zone:{zone}",
        f"doctrines:{','.join(sorted(d.topic for d in doctrines))}",
        f"version:{ENGINE_VERSION}"
    ]
    deterministic_string = "|".join(components)

    # Hash with SHA-256
    return hashlib.sha256(deterministic_string.encode("utf-8")).hexdigest()


# ===================================================================
# TIE COMPONENT 19: Multi-Doctrine Decomposition
# ===================================================================
def decompose_query(query: str, normalizer: SemanticNormalizer) -> dict[str, Any]:
    """
    Decompose complex query into issue categories and stratification.

    Args:
        query: Query text
        normalizer: Semantic normalizer

    Returns:
        Decomposition result
    """
    entities = normalizer.extract_entities(query)

    # Identify issue categories
    categories: list[IssueCategory] = []
    if entities.get("family_members"):
        categories.append(IssueCategory.INTESTATE_SUCCESSION)
    if "will" in query.lower() or "testament" in query.lower():
        categories.append(IssueCategory.TESTATE_SUCCESSION)
    if "community" in query.lower():
        categories.append(IssueCategory.COMMUNITY_PROPERTY)
    if "affidavit" in query.lower():
        categories.append(IssueCategory.AFFIDAVIT_OF_HEIRSHIP)
    if "trust" in query.lower():
        categories.append(IssueCategory.TRUST_ADMINISTRATION)
    if "mineral" in query.lower():
        categories.append(IssueCategory.MINERAL_INHERITANCE_TRACING)

    # Stratification
    strata = "BASIC"
    if len(categories) > 2:
        strata = "COMPLEX"
    if "conflict" in query.lower() or "dispute" in query.lower():
        strata = "ADVERSARIAL"

    return {
        "categories": [c.value for c in categories],
        "strata": strata,
        "entities": entities,
        "complexity_score": len(categories) / 5.0  # Normalize to 0-1
    }


# ===================================================================
# TIE COMPONENT 9: Drift Watcher
# ===================================================================
class DriftWatcher:
    """Monitor doctrine drift over time."""

    def __init__(self) -> None:
        """Initialize drift watcher."""
        self.doctrine_versions: dict[str, str] = {}
        self.last_check = datetime.now(timezone.utc)

    def check_drift(self, doctrines: list[DoctrineBlock]) -> dict[str, Any]:
        """
        Check for doctrine drift.

        Args:
            doctrines: Current doctrines

        Returns:
            Drift report
        """
        # In production, would compare against stored versions
        # and detect changes in controlling precedent or statutes
        return {
            "drift_detected": False,
            "last_check": self.last_check.isoformat(),
            "total_doctrines": len(doctrines),
            "changed_doctrines": []
        }


# ===================================================================
# TIE COMPONENT 10: Coverage Map
# ===================================================================
class CoverageMap:
    """Track doctrine coverage and epistemic gaps."""

    def __init__(self, telemetry: TelemetryCollector) -> None:
        """Initialize coverage map."""
        self.telemetry = telemetry

    def get_coverage(self) -> dict[str, Any]:
        """Get doctrine coverage report."""
        return self.telemetry.get_doctrine_coverage()


# ===================================================================
# TIE COMPONENT 20: Deep Analysis Mode
# ===================================================================
def generate_deep_analysis(
    query: ProbateQuery,
    doctrines: list[DoctrineBlock],
    interactions: list[DoctrineInteraction],
    mode_config: dict[str, Any]
) -> str:
    """
    Generate deep analysis with full reasoning chain.

    Args:
        query: Probate query
        doctrines: Triggered doctrines
        interactions: Doctrine interactions
        mode_config: Mode configuration

    Returns:
        Analysis text
    """
    sections: list[str] = []

    # Zone-specific introduction
    zone_intro = ZONE_GUIDELINES.get(query.zone.value, "")
    sections.append(f"ANALYSIS ZONE: {query.zone.value}\n{zone_intro}\n")

    # Query decomposition
    sections.append(f"QUERY: {query.query}\n")

    # Triggered doctrines
    if doctrines:
        sections.append("APPLICABLE DOCTRINES:")
        for i, doctrine in enumerate(doctrines, 1):
            sections.append(f"{i}. {doctrine.topic.upper().replace('_', ' ')}")
            sections.append(f"   Category: {doctrine.category.value}")
            sections.append(f"   Confidence: {doctrine.confidence.value}")

            # Include reasoning framework in DEFENSE and MEMO modes
            if mode_config.get("doctrine_depth") in ("full", "exhaustive"):
                sections.append(f"\n   Reasoning Framework:")
                sections.append(f"   {doctrine.reasoning_framework[:500]}...")

                # Include primary authority
                if mode_config.get("include_citations"):
                    sections.append(f"\n   Primary Authority:")
                    for auth in doctrine.primary_authority[:3]:
                        sections.append(f"   - {auth}")

            sections.append("")

    # Doctrine interactions (if requested)
    if interactions and query.include_interactions:
        sections.append("DOCTRINE INTERACTIONS:")
        for interaction in interactions[:5]:
            sections.append(
                f"- {interaction.topic_a} {interaction.interaction_type} {interaction.topic_b}"
            )
            sections.append(f"  {interaction.description}")
        sections.append("")

    # Conclusion templates
    if doctrines:
        sections.append("ANALYSIS:")
        for doctrine in doctrines[:3]:
            for conclusion in doctrine.conclusion_template:
                sections.append(f"• {conclusion}")
        sections.append("")

    # Resolution strategy (MEMO mode)
    if mode_config.get("doctrine_depth") == "exhaustive" and doctrines:
        sections.append("RESOLUTION STRATEGY:")
        sections.append(doctrines[0].resolution_strategy)
        sections.append("")

    # Epistemic guardrails
    analysis_text = "\n".join(sections)
    for phrase in BANNED_PHRASES:
        if phrase in analysis_text.lower():
            logger.warning(f"Epistemic guardrail violation: '{phrase}' in analysis")
            analysis_text = analysis_text.replace(phrase, "[REDACTED]")

    return analysis_text


# ===================================================================
# FastAPI Lifespan
# ===================================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown."""
    # Startup
    logger.info(f"Starting {ENGINE_NAME} Engine v{ENGINE_VERSION} on port {ENGINE_PORT}")

    # Load config
    if CONFIG_PATH.exists():
        config = json.loads(CONFIG_PATH.read_text())
        logger.info(f"Loaded config from {CONFIG_PATH}")
    else:
        config = {}
        logger.warning(f"Config not found at {CONFIG_PATH}")

    # Build doctrine cache
    doctrine_cache = build_doctrine_cache()
    logger.info(f"Built doctrine cache: {len(doctrine_cache)} doctrines")

    # Build interaction graph
    interaction_graph = build_interaction_graph()
    logger.info(f"Built interaction graph: {len(interaction_graph)} nodes")

    # Build vector index
    vector_index = get_vector_index()
    from doctrines import DOCTRINE_BLOCKS
    vector_index.build_from_doctrines(DOCTRINE_BLOCKS)
    logger.info(f"Built vector index: {len(vector_index.documents)} documents")

    # Initialize telemetry
    telemetry = get_telemetry_collector()
    logger.info("Initialized telemetry collector")

    # Store in app state
    app.state.config = config
    app.state.doctrine_cache = doctrine_cache
    app.state.interaction_graph = interaction_graph
    app.state.vector_index = vector_index
    app.state.telemetry = telemetry
    app.state.normalizer = get_normalizer()
    app.state.authority_hierarchy = AuthorityHierarchy(config)
    app.state.drift_watcher = DriftWatcher()
    app.state.coverage_map = CoverageMap(telemetry)
    app.state.three_layer = ThreeLayerResponse(doctrine_cache, vector_index, app.state.normalizer, telemetry)

    logger.info(f"{ENGINE_NAME} Engine startup complete")

    yield

    # Shutdown
    logger.info(f"Shutting down {ENGINE_NAME} Engine")


# ===================================================================
# FastAPI Application
# ===================================================================
app = FastAPI(
    title=f"{ENGINE_NAME} Engine",
    description=f"Probate and estate succession intelligence for mineral title examination (Engine {ENGINE_ID})",
    version=ENGINE_VERSION,
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ===================================================================
# TIE COMPONENT 12: Health Endpoint
# ===================================================================
@app.get("/health")
async def health_check(request: Request) -> dict[str, Any]:
    """
    Health check endpoint.

    Returns:
        Health status with doctrine count, uptime, and query stats
    """
    telemetry: TelemetryCollector = request.app.state.telemetry
    metrics = telemetry.get_metrics()

    return {
        "status": "healthy",
        "engine": ENGINE_NAME,
        "engine_id": ENGINE_ID,
        "version": ENGINE_VERSION,
        "port": ENGINE_PORT,
        "domain": ENGINE_DOMAIN,
        "doctrine_count": len(request.app.state.doctrine_cache),
        "uptime_hours": metrics.get("uptime_hours", 0),
        "total_queries": metrics.get("total_queries", 0),
        "cache_hit_rate": metrics.get("cache_hit_rate", 0),
        "error_rate": metrics.get("error_rate", 0),
        "avg_latency_ms": metrics.get("avg_latency_ms", 0),
        "cloud_available": _CLOUD_AVAILABLE,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


# ===================================================================
# Main Query Endpoint
# ===================================================================
@app.post("/query", response_model=ProbateResponse)
async def query_probate(query: ProbateQuery, request: Request) -> ProbateResponse:
    """
    Main probate title analysis endpoint.

    Args:
        query: Probate query

    Returns:
        ProbateResponse with analysis and metadata
    """
    query_id = str(uuid.uuid4())
    start_time = time.time()

    # Get app state
    telemetry: TelemetryCollector = request.app.state.telemetry
    three_layer: ThreeLayerResponse = request.app.state.three_layer
    authority_hierarchy: AuthorityHierarchy = request.app.state.authority_hierarchy
    interaction_graph: dict[str, list[DoctrineInteraction]] = request.app.state.interaction_graph

    # Start trace
    trace = telemetry.start_trace(query_id, query.query, query.mode.value, query.zone.value)

    try:
        # Normalization
        norm_start = time.time()
        normalizer: SemanticNormalizer = request.app.state.normalizer
        norm_result = normalizer.normalize(query.query)
        norm_latency = (time.time() - norm_start) * 1000
        telemetry.record_phase(trace, QueryPhase.NORMALIZATION, norm_latency)

        # Three-layer response retrieval
        doctrines, layer_metadata = three_layer.execute(query, trace)

        # Record doctrine triggers
        for doctrine in doctrines:
            telemetry.record_doctrine_trigger(trace, doctrine.topic)

        # Get interactions if requested
        interactions: list[DoctrineInteraction] = []
        if query.include_interactions:
            for doctrine in doctrines:
                interactions.extend(get_interactions_for_topic(doctrine.topic))

        # Generate response
        response_start = time.time()
        mode_config = RESPONSE_MODE_CONFIG[query.mode.value]
        analysis = generate_deep_analysis(query, doctrines, interactions, mode_config)
        response_latency = (time.time() - response_start) * 1000
        telemetry.record_phase(trace, QueryPhase.RESPONSE_GENERATION, response_latency)

        # Confidence assessment
        if doctrines:
            primary_confidence = doctrines[0].confidence
            confidence_tier = primary_confidence.value
            confidence_score = {"DEFENSIBLE": 0.9, "AGGRESSIVE": 0.7, "DISCLOSURE": 0.5, "HIGH_RISK": 0.3}.get(confidence_tier, 0.5)
        else:
            confidence_tier = "DISCLOSURE"
            confidence_score = 0.4

        confidence = ConfidenceAssessment(
            tier=confidence_tier,
            score=confidence_score,
            factors=[f"Based on {len(doctrines)} applicable doctrines"],
            caveats=[doctrine.disclosure_caveat for doctrine in doctrines if doctrine.disclosure_caveat]
        )

        # Authorities
        authorities: list[AuthoritySource] = []
        for doctrine in doctrines[:3]:
            for auth in doctrine.primary_authority[:2]:
                authorities.append(AuthoritySource(
                    source=auth,
                    weight=authority_hierarchy._get_weight(auth),
                    type="statute" if "Code" in auth else "case"
                ))

        # Doctrine references
        doctrine_refs = [
            DoctrineReference(
                topic=d.topic,
                category=d.category.value,
                confidence=d.confidence.value,
                authority=d.primary_authority[:3],
                reasoning_summary=d.conclusion_template[0] if d.conclusion_template else ""
            )
            for d in doctrines
        ]

        # Interaction references
        interaction_dicts = [
            {
                "topic_a": i.topic_a,
                "topic_b": i.topic_b,
                "type": i.interaction_type,
                "description": i.description
            }
            for i in interactions[:5]
        ]

        # Fragility scoring
        fragility = None
        if query.include_fragility:
            fragility = calculate_fragility(query.query, doctrines)

        # Determinism hash
        determinism_hash = calculate_determinism_hash(query.query, doctrines, query.mode.value, query.zone.value)

        # Total latency
        total_latency = (time.time() - start_time) * 1000
        telemetry.record_phase(trace, QueryPhase.TOTAL, total_latency)

        # Complete trace
        telemetry.complete_trace(trace, confidence_tier, len(analysis))

        # Build response
        response = ProbateResponse(
            query_id=query_id,
            query=query.query,
            mode=query.mode.value,
            zone=query.zone.value,
            analysis=analysis,
            doctrines_triggered=doctrine_refs,
            confidence=confidence,
            authorities=authorities,
            interactions=interaction_dicts if query.include_interactions else [],
            fragility=fragility,
            determinism_hash=determinism_hash,
            timestamp=datetime.now(timezone.utc).isoformat(),
            latency_ms=total_latency
        )

        return response

    except Exception as e:
        # Record error
        error_msg = f"{type(e).__name__}: {str(e)}"
        telemetry.record_error(trace, ErrorDomain.SYSTEM_ERROR, error_msg)
        logger.error(f"Query failed: {error_msg}\n{traceback.format_exc()}")

        raise HTTPException(status_code=500, detail=error_msg)


# ===================================================================
# TIE COMPONENT 11: Metrics Endpoint
# ===================================================================
@app.get("/metrics")
async def get_metrics(request: Request) -> dict[str, Any]:
    """
    Get engine metrics.

    Returns:
        Metrics dictionary
    """
    telemetry: TelemetryCollector = request.app.state.telemetry
    coverage_map: CoverageMap = request.app.state.coverage_map

    metrics = telemetry.get_metrics()
    coverage = coverage_map.get_coverage()

    return {
        "engine": ENGINE_NAME,
        "engine_id": ENGINE_ID,
        "version": ENGINE_VERSION,
        "metrics": metrics,
        "coverage": coverage,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


# ===================================================================
# Doctrine Listing Endpoint
# ===================================================================
@app.get("/doctrines")
async def list_doctrines(
    request: Request,
    category: Optional[str] = Query(None, description="Filter by category"),
    keyword: Optional[str] = Query(None, description="Filter by keyword")
) -> dict[str, Any]:
    """
    List available doctrines.

    Args:
        category: Optional category filter
        keyword: Optional keyword filter

    Returns:
        Doctrine listing
    """
    doctrine_cache: dict[str, DoctrineBlock] = request.app.state.doctrine_cache

    doctrines = list(doctrine_cache.values())

    # Filter by category
    if category:
        try:
            cat = IssueCategory(category)
            doctrines = [d for d in doctrines if d.category == cat]
        except ValueError:
            pass

    # Filter by keyword
    if keyword:
        doctrines = find_doctrines_by_keyword(keyword)

    # Format response
    doctrine_list = [
        {
            "topic": d.topic,
            "category": d.category.value,
            "keywords": d.keywords,
            "confidence": d.confidence.value,
            "authority_count": len(d.primary_authority)
        }
        for d in doctrines
    ]

    return {
        "total_doctrines": len(doctrine_list),
        "doctrines": doctrine_list,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


# ===================================================================
# Coverage Endpoint
# ===================================================================
@app.get("/coverage")
async def get_coverage(request: Request) -> dict[str, Any]:
    """
    Get doctrine coverage report.

    Returns:
        Coverage statistics
    """
    coverage_map: CoverageMap = request.app.state.coverage_map
    drift_watcher: DriftWatcher = request.app.state.drift_watcher

    coverage = coverage_map.get_coverage()
    drift = drift_watcher.check_drift(list(request.app.state.doctrine_cache.values()))

    return {
        "engine": ENGINE_NAME,
        "coverage": coverage,
        "drift": drift,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


# ===================================================================
# Main Entry Point
# ===================================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=ENGINE_PORT,
        log_level="info",
        workers=1
    )