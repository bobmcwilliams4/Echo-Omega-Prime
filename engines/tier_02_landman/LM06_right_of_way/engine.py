"""
LM06 Right of Way Engine - Main FastAPI Engine
===============================================
Production-grade pipeline ROW acquisition and management engine implementing
all 20 TIE components for:
- Pipeline ROW negotiation and acquisition
- Condemnation/eminent domain proceedings
- FERC certificate proceedings
- Easement types (fee vs easement, temporary vs permanent, blanket vs strip)
- Surface damage and restoration
- Crossing agreements (railroad, highway, river, pipeline)
- Dominant/servient estate rights and accommodation doctrine
- ROW valuation and appraisal
- Texas Railroad Commission compliance
- Federal pipeline safety (49 CFR 192/195)

TIE-20 Components:
    1.  three_layer_response (doctrine cache → semantic search → deep analysis)
    2.  response_modes (FAST, DEFENSE, MEMO)
    3.  doctrine_cache (48 blocks covering all ROW domains)
    4.  authority_hardening (hierarchical authority weights)
    5.  confidence_stratification (DEFENSIBLE/AGGRESSIVE/DISCLOSURE/HIGH_RISK)
    6.  semantic_normalization (ROW terminology, abbreviations, operators)
    7.  vector_search (TF-IDF inverted index for ROW records)
    8.  telemetry_module (latency, cache hits, error tracking)
    9.  doctrine_drift_watcher (detect doctrine coverage gaps)
    10. doctrine_coverage_map (track triggered/missed doctrines)
    11. metrics_collector (queries/hour, error rate, percentiles)
    12. health_endpoint (comprehensive health check)
    13. zoned_analysis (PLANNING/REPORTING/AUDIT zones)
    14. fact_fragility_scoring (verifiability, recharacterization risk)
    15. audit_trail_jsonl (every query logged for forensic review)
    16. determinism_hash_sha256 (reproducibility hash)
    17. fastapi_server (full FastAPI with CORS, lifespan, typed endpoints)
    18. loguru_logging (structured logging, rotation, no print)
    19. multi_doctrine_decomposition (issue categories, interaction DAG)
    20. deep_analysis_mode (multi-source synthesis, full reasoning chain)

Port: 8506
Engine: LM06 Right of Way
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
    logger.warning("Cloud retriever not available (import failed)")

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
    IssueCategory,
    ConfidenceStratification,
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
    OPERATOR_ALIAS_MAP,
    INSTRUMENT_TYPE_MAP,
    TEXAS_PERMIAN_COUNTIES,
    normalize_query,
    expand_abbreviations,
    resolve_synonyms,
    resolve_operator,
    classify_instrument_type,
    extract_row_dimensions,
    extract_compensation_amount,
    extract_pipeline_specs,
    is_permian_county,
    get_all_canonical_terms,
    semantic_health,
)
from search import (
    ROWRecord,
    ROWType,
    ROWStatus,
    SearchQuery,
    SearchResult,
    SearchResponse,
    SortField,
    SortOrder,
    SearchIndex,
    build_search_index,
    get_search_index,
    search_records,
    filter_by_location,
    filter_by_type,
    filter_by_operator,
    filter_by_dimensions,
    search_index_health,
)
from telemetry import (
    QueryPhase,
    ErrorDomain,
    TelemetryCollector,
    PhaseTimer,
    get_telemetry,
    record_query,
    get_snapshot,
    telemetry_dashboard,
    telemetry_health,
    reset_telemetry,
)


# ============================================================================
# CONSTANTS
# ============================================================================

ENGINE_ID = "LM06"
ENGINE_NAME = "Right of Way"
ENGINE_VERSION = "1.0.0"
ENGINE_PORT = 8506
ENGINE_AUTHORITY = 8.0
ENGINE_TIER = "LANDMAN"
ENGINE_MODE = "DET"

CONFIG_PATH = Path(__file__).parent / "config.json"
AUDIT_LOG_DIR = Path(__file__).parent / "audit_logs"
AUDIT_LOG_DIR.mkdir(exist_ok=True)


# ============================================================================
# RESPONSE MODE ENUM
# ============================================================================

class ResponseMode(str, Enum):
    FAST = "fast"
    DEFENSE = "defense"
    MEMO = "memo"


# ============================================================================
# POSITION ZONE ENUM
# ============================================================================

class PositionZone(str, Enum):
    PLANNING = "planning"
    REPORTING = "reporting"
    AUDIT = "audit"


# ============================================================================
# PYDANTIC MODELS - REQUEST / RESPONSE
# ============================================================================

class ROWQueryRequest(BaseModel):
    """Request model for ROW analysis queries."""
    query: str = Field(..., min_length=1, max_length=5000, description="The ROW analysis query")
    mode: ResponseMode = Field(default=ResponseMode.DEFENSE, description="Response mode")
    zone: PositionZone = Field(default=PositionZone.REPORTING, description="Position zone")
    county: Optional[str] = Field(default=None, description="County filter")
    state: Optional[str] = Field(default="TX", description="State filter")
    operator: Optional[str] = Field(default=None, description="Pipeline operator filter")
    include_doctrines: bool = Field(default=True, description="Include matched doctrine blocks")
    include_search_results: bool = Field(default=False, description="Include ROW record search results")
    max_doctrines: int = Field(default=5, ge=1, le=20, description="Max doctrine blocks to return")
    cloud_retrieval: bool = Field(default=False, description="Enable cloud knowledge retrieval")

    @field_validator("query")
    @classmethod
    def validate_query(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Query cannot be empty")
        return v.strip()


class DoctrineBlockResponse(BaseModel):
    """Doctrine block in response."""
    topic: str
    category: str
    confidence: float
    confidence_stratification: str
    conclusion: str
    reasoning_summary: str
    primary_authority: List[str]
    controlling_precedent: str
    tags: List[str]


class ROWQueryResponse(BaseModel):
    """Response model for ROW analysis queries."""
    query_id: str
    query: str
    mode: str
    zone: str
    answer: str
    confidence: float
    confidence_stratification: str
    doctrines_triggered: List[DoctrineBlockResponse]
    search_results: Optional[SearchResponse]
    issue_categories: List[str]
    fact_fragility_score: float
    determinism_hash: str
    metadata: Dict[str, Any]
    latency_ms: float


class HealthResponse(BaseModel):
    """Health check response."""
    engine_id: str
    engine_name: str
    version: str
    status: str
    uptime_seconds: float
    total_queries: int
    error_rate: float
    avg_latency_ms: float
    cache_hit_rate: float
    doctrine_count: int
    search_index_records: int
    cloud_available: bool


class CoverageMapResponse(BaseModel):
    """Doctrine coverage map response."""
    total_blocks: int
    categories: int
    coverage_by_category: Dict[str, int]
    top_categories: List[Dict[str, Any]]
    gaps: List[str]


# ============================================================================
# DOCTRINE DRIFT WATCHER
# ============================================================================

@dataclass
class DoctrineDriftWatcher:
    """
    Tracks doctrine usage over time to detect drift (coverage gaps, unused doctrines).
    """
    triggered_doctrines: Dict[str, int] = dc_field(default_factory=dict)
    missed_queries: List[str] = dc_field(default_factory=list)
    total_queries: int = 0

    def record_triggered(self, topics: List[str]) -> None:
        """Record doctrine topics triggered for a query."""
        self.total_queries += 1
        if not topics:
            # No doctrines triggered = potential gap
            self.missed_queries.append(f"query_{self.total_queries}")
        for topic in topics:
            self.triggered_doctrines[topic] = self.triggered_doctrines.get(topic, 0) + 1

    def get_coverage_stats(self) -> Dict[str, Any]:
        """Get coverage statistics."""
        total_doctrines = len(DOCTRINE_BLOCKS)
        triggered_count = len(self.triggered_doctrines)
        untriggered_count = total_doctrines - triggered_count

        return {
            "total_doctrines": total_doctrines,
            "triggered_doctrines": triggered_count,
            "untriggered_doctrines": untriggered_count,
            "coverage_pct": (triggered_count / total_doctrines * 100) if total_doctrines > 0 else 0.0,
            "missed_query_count": len(self.missed_queries),
            "top_triggered": sorted(self.triggered_doctrines.items(), key=lambda x: x[1], reverse=True)[:10],
        }


_DRIFT_WATCHER: Optional[DoctrineDriftWatcher] = None


def get_drift_watcher() -> DoctrineDriftWatcher:
    """Get singleton drift watcher."""
    global _DRIFT_WATCHER
    if _DRIFT_WATCHER is None:
        _DRIFT_WATCHER = DoctrineDriftWatcher()
    return _DRIFT_WATCHER


# ============================================================================
# FACT FRAGILITY SCORING
# ============================================================================

def calculate_fact_fragility(query: str, doctrines: List[DoctrineCacheBlock]) -> float:
    """
    Calculate fact fragility score (0.0 = solid facts, 1.0 = highly fragile).

    Factors:
    - Verifiability: Can facts be verified from public records?
    - Recharacterization risk: Could facts be interpreted differently?
    - Testimony dependence: Does answer rely on witness testimony vs documents?
    - Authority strength: Higher authority sources = lower fragility
    """
    fragility_score = 0.5  # Baseline

    # Check for verifiable terms (public records, statutes, regulations = low fragility)
    verifiable_terms = {
        "statute", "regulation", "code", "cfr", "usc", "recorded", "filed",
        "certificate", "survey", "plat", "deed", "easement agreement",
    }
    query_lower = query.lower()
    verifiable_count = sum(1 for term in verifiable_terms if term in query_lower)

    if verifiable_count > 0:
        fragility_score -= 0.1 * min(verifiable_count, 3)

    # Check for fragile terms (valuation, intent, custom, practice = high fragility)
    fragile_terms = {
        "intent", "custom", "practice", "reasonable", "unreasonable",
        "good faith", "bad faith", "fair", "unfair", "adequate", "inadequate",
    }
    fragile_count = sum(1 for term in fragile_terms if term in query_lower)

    if fragile_count > 0:
        fragility_score += 0.1 * min(fragile_count, 3)

    # Authority strength: Higher authority = lower fragility
    if doctrines:
        avg_authority = sum(d.authority_weight for d in doctrines) / len(doctrines)
        # Authority 9.0-10.0 = very solid (Supreme Court, federal statute)
        # Authority 5.0-7.0 = moderate fragility (case law, industry practice)
        if avg_authority >= 9.0:
            fragility_score -= 0.15
        elif avg_authority < 7.0:
            fragility_score += 0.15

    # Clamp to [0.0, 1.0]
    return max(0.0, min(1.0, fragility_score))


# ============================================================================
# DETERMINISM HASH (SHA-256)
# ============================================================================

def calculate_determinism_hash(query: str, doctrines: List[str], mode: str) -> str:
    """
    Calculate SHA-256 hash for query reproducibility.

    Hash includes: query text, triggered doctrine topics (sorted), response mode.
    Same inputs = same hash (deterministic).
    """
    hash_input = f"{query}|{','.join(sorted(doctrines))}|{mode}"
    return hashlib.sha256(hash_input.encode('utf-8')).hexdigest()


# ============================================================================
# AUDIT LOGGING (JSONL)
# ============================================================================

def log_query_audit(
    query_id: str,
    query: str,
    mode: str,
    zone: str,
    doctrines_triggered: List[str],
    answer: str,
    confidence: float,
    latency_ms: float,
    error: Optional[str] = None,
) -> None:
    """
    Log query to audit trail (JSONL format).

    Each line = one JSON object (query record).
    Append-only, never modify existing logs.
    """
    audit_record = {
        "query_id": query_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "query": query,
        "mode": mode,
        "zone": zone,
        "doctrines_triggered": doctrines_triggered,
        "answer": answer[:500],  # Truncate long answers
        "confidence": confidence,
        "latency_ms": latency_ms,
        "error": error,
    }

    # Append to today's audit log file
    log_file = AUDIT_LOG_DIR / f"audit_{datetime.now(timezone.utc).strftime('%Y%m%d')}.jsonl"
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(json.dumps(audit_record) + '\n')


# ============================================================================
# THREE-LAYER RESPONSE ENGINE
# ============================================================================

def three_layer_response(
    query: str,
    mode: ResponseMode,
    zone: PositionZone,
    county: Optional[str],
    operator: Optional[str],
    include_search: bool,
    cloud_retrieval: bool,
    phase_latencies: Dict[QueryPhase, float],
) -> Tuple[str, float, ConfidenceStratification, List[DoctrineCacheBlock], Optional[SearchResponse]]:
    """
    Three-layer response strategy:
    1. Doctrine Cache (0-50ms): Pre-compiled expert reasoning
    2. Semantic Search (50-200ms): ROW record search + normalization
    3. Deep Analysis (200-2000ms): Multi-source synthesis + cloud retrieval

    Returns:
        (answer, confidence, stratification, doctrines, search_results)
    """
    # LAYER 1: DOCTRINE CACHE (fast path)
    with PhaseTimer(QueryPhase.NORMALIZATION, phase_latencies):
        normalized_query = normalize_query(query)

    with PhaseTimer(QueryPhase.DOCTRINE_CACHE, phase_latencies):
        matched_doctrines = search_doctrines(normalized_query, max_results=5)

    # LAYER 2: SEMANTIC SEARCH (if needed)
    search_results = None
    if include_search and (not matched_doctrines or mode != ResponseMode.FAST):
        with PhaseTimer(QueryPhase.SEMANTIC_SEARCH, phase_latencies):
            search_query = SearchQuery(
                query=normalized_query,
                county=county,
                operator=operator,
                limit=10,
            )
            search_index = get_search_index()
            if search_index.total_docs > 0:
                search_results = search_records(search_query, search_index)

    # LAYER 3: DEEP ANALYSIS (if needed)
    cloud_data = None
    if cloud_retrieval and _CLOUD_AVAILABLE and mode in (ResponseMode.DEFENSE, ResponseMode.MEMO):
        with PhaseTimer(QueryPhase.CLOUD_RETRIEVAL, phase_latencies):
            try:
                cloud_data = retrieve_cloud_knowledge(query, domain="row_acquisition")
            except Exception as e:
                logger.warning(f"Cloud retrieval failed: {e}")

    # SYNTHESIZE ANSWER
    with PhaseTimer(QueryPhase.DEEP_ANALYSIS, phase_latencies):
        answer, confidence, stratification = synthesize_answer(
            query=query,
            normalized_query=normalized_query,
            mode=mode,
            zone=zone,
            doctrines=matched_doctrines,
            search_results=search_results,
            cloud_data=cloud_data,
        )

    return answer, confidence, stratification, matched_doctrines, search_results


def synthesize_answer(
    query: str,
    normalized_query: str,
    mode: ResponseMode,
    zone: PositionZone,
    doctrines: List[DoctrineCacheBlock],
    search_results: Optional[SearchResponse],
    cloud_data: Optional[Dict[str, Any]],
) -> Tuple[str, float, ConfidenceStratification]:
    """
    Synthesize final answer from doctrine cache, search results, and cloud data.

    Response modes:
    - FAST: Concise answer (1-2 paragraphs), doctrine cache only
    - DEFENSE: Audit-ready analysis (3-5 paragraphs), citations, authority hardening
    - MEMO: Full memorandum (5-10 paragraphs), reasoning chain, counter-arguments

    Position zones:
    - PLANNING: Aggressive positioning, maximize client advantage
    - REPORTING: Balanced analysis, both sides presented
    - AUDIT: Conservative, disclosure-heavy, minimize risk
    """
    if not doctrines and not search_results:
        # No doctrine matches, no search results = low confidence
        return (
            f"Insufficient ROW doctrine coverage for query: '{query}'. "
            f"Recommend manual legal research on: {', '.join(extract_key_terms(normalized_query))}.",
            0.3,
            ConfidenceStratification.DISCLOSURE,
        )

    # Build answer from doctrines
    answer_parts = []

    if mode == ResponseMode.FAST:
        # FAST: Concise, doctrine conclusions only
        if doctrines:
            top_doctrine = doctrines[0]
            answer_parts.append(f"**{top_doctrine.topic}**")
            answer_parts.append(' '.join(top_doctrine.conclusion_template[:2]))

            if zone == PositionZone.AUDIT:
                answer_parts.append(f"\n\n*Disclosure: {top_doctrine.disclosure_caveat or 'Standard ROW analysis, consult attorney for specific transaction.'}*")

        confidence = 0.7 if doctrines else 0.4
        stratification = ConfidenceStratification.DEFENSIBLE if zone == PositionZone.REPORTING else ConfidenceStratification.AGGRESSIVE

    elif mode == ResponseMode.DEFENSE:
        # DEFENSE: Audit-ready, citations, authority hardening
        answer_parts.append(f"## ROW Analysis: {query}\n")

        for i, doctrine in enumerate(doctrines[:3], 1):
            answer_parts.append(f"### {i}. {doctrine.topic}")
            answer_parts.append(' '.join(doctrine.conclusion_template))
            answer_parts.append(f"\n**Controlling Authority:** {doctrine.controlling_precedent}")
            answer_parts.append(f"**Primary Authority:** {'; '.join(doctrine.primary_authority[:3])}")

            if zone == PositionZone.PLANNING:
                # Aggressive: emphasize resolution strategy
                answer_parts.append(f"\n**Strategy:** {doctrine.resolution_strategy}")
            elif zone == PositionZone.AUDIT:
                # Conservative: emphasize adversary position and disclosure
                answer_parts.append(f"\n**Adversary Position:** {doctrine.adversary_position}")
                if doctrine.disclosure_caveat:
                    answer_parts.append(f"\n**Disclosure:** {doctrine.disclosure_caveat}")

            answer_parts.append("")  # Blank line

        if search_results and search_results.total_results > 0:
            answer_parts.append(f"### Comparable ROW Transactions")
            answer_parts.append(f"Found {search_results.total_results} comparable ROW records:")
            for result in search_results.results[:3]:
                answer_parts.append(f"- {result.snippet}")

        confidence = 0.85 if doctrines else 0.5
        stratification = ConfidenceStratification.DEFENSIBLE if zone == PositionZone.REPORTING else ConfidenceStratification.AGGRESSIVE if zone == PositionZone.PLANNING else ConfidenceStratification.DISCLOSURE

    elif mode == ResponseMode.MEMO:
        # MEMO: Full memorandum, reasoning chain, counter-arguments
        answer_parts.append(f"# MEMORANDUM: {query}\n")
        answer_parts.append(f"**Date:** {datetime.now(timezone.utc).strftime('%Y-%m-%d')}")
        answer_parts.append(f"**Engine:** {ENGINE_NAME} v{ENGINE_VERSION}")
        answer_parts.append(f"**Position Zone:** {zone.value.upper()}\n")

        answer_parts.append("## EXECUTIVE SUMMARY\n")
        if doctrines:
            summary_doctrine = doctrines[0]
            answer_parts.append(' '.join(summary_doctrine.conclusion_template))
            answer_parts.append("")

        answer_parts.append("## LEGAL ANALYSIS\n")
        for i, doctrine in enumerate(doctrines[:5], 1):
            answer_parts.append(f"### {i}. {doctrine.topic}")
            answer_parts.append(f"**Category:** {doctrine.category.value.replace('_', ' ').title()}")
            answer_parts.append(f"**Confidence Stratification:** {doctrine.confidence_stratification.value.upper()}")
            answer_parts.append("")

            answer_parts.append("**Conclusion:**")
            answer_parts.append(' '.join(doctrine.conclusion_template))
            answer_parts.append("")

            answer_parts.append("**Reasoning Framework:**")
            answer_parts.append(doctrine.reasoning_framework)
            answer_parts.append("")

            answer_parts.append("**Key Factors:**")
            for factor in doctrine.key_factors[:5]:
                answer_parts.append(f"- {factor}")
            answer_parts.append("")

            answer_parts.append("**Primary Authority:**")
            for auth in doctrine.primary_authority[:5]:
                answer_parts.append(f"- {auth}")
            answer_parts.append("")

            answer_parts.append(f"**Controlling Precedent:** {doctrine.controlling_precedent}")
            answer_parts.append("")

            if zone == PositionZone.PLANNING:
                answer_parts.append("**Counter-Arguments (Anticipate Adversary):**")
                for arg in doctrine.counter_arguments[:3]:
                    answer_parts.append(f"- {arg}")
                answer_parts.append("")
                answer_parts.append(f"**Resolution Strategy:** {doctrine.resolution_strategy}")
            elif zone == PositionZone.AUDIT:
                answer_parts.append(f"**Adversary Position:** {doctrine.adversary_position}")
                if doctrine.disclosure_caveat:
                    answer_parts.append(f"\n**DISCLOSURE:** {doctrine.disclosure_caveat}")

            answer_parts.append("\n---\n")

        if search_results and search_results.total_results > 0:
            answer_parts.append("## COMPARABLE TRANSACTIONS\n")
            answer_parts.append(f"Search identified {search_results.total_results} comparable ROW records:\n")
            for result in search_results.results[:5]:
                answer_parts.append(f"**{result.record_id}**: {result.snippet}")
                answer_parts.append("")

        answer_parts.append("## CONCLUSION\n")
        answer_parts.append(f"Based on {len(doctrines)} triggered doctrine blocks, the ROW analysis is {get_confidence_label(doctrines[0].confidence if doctrines else 0.5)}.")
        if zone == PositionZone.AUDIT:
            answer_parts.append("\n*This analysis is for informational purposes only and does not constitute legal advice. Consult a licensed attorney for specific ROW transactions.*")

        confidence = 0.9 if doctrines else 0.6
        stratification = ConfidenceStratification.DEFENSIBLE if zone == PositionZone.REPORTING else ConfidenceStratification.AGGRESSIVE if zone == PositionZone.PLANNING else ConfidenceStratification.DISCLOSURE

    return '\n'.join(answer_parts), confidence, stratification


def get_confidence_label(confidence: float) -> str:
    """Get human-readable confidence label."""
    if confidence >= 0.9:
        return "HIGH CONFIDENCE"
    elif confidence >= 0.7:
        return "MODERATE CONFIDENCE"
    elif confidence >= 0.5:
        return "LOW-MODERATE CONFIDENCE"
    else:
        return "LOW CONFIDENCE"


def extract_key_terms(query: str) -> List[str]:
    """Extract key terms from query for manual research suggestions."""
    # Simple extraction: nouns, proper nouns, ROW-specific terms
    import re
    tokens = re.findall(r'\b[A-Z][a-z]+\b|\b(?:easement|condemnation|ferc|row|rrc|pipeline)\b', query, re.IGNORECASE)
    return list(set(tokens))[:5]


# ============================================================================
# FASTAPI LIFESPAN
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI lifespan context manager (startup/shutdown)."""
    # STARTUP
    logger.info(f"Starting {ENGINE_NAME} v{ENGINE_VERSION} on port {ENGINE_PORT}")

    # Configure loguru
    logger.remove()  # Remove default handler
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> | <level>{message}</level>",
        level="INFO",
    )
    logger.add(
        Path(__file__).parent / "logs" / f"{ENGINE_ID}.log",
        rotation="50 MB",
        retention="30 days",
        level="DEBUG",
    )

    # Load config
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, 'r') as f:
            config = json.load(f)
            logger.info(f"Loaded config: {config['engine_name']} (Tier: {config['tier']})")

    # Initialize doctrine cache
    doctrine_health = doctrine_cache_health()
    logger.info(f"Doctrine cache: {doctrine_health['total_blocks']} blocks, {doctrine_health['categories']} categories")

    # Initialize search index (empty initially, populated on first query or bulk load)
    search_health = search_index_health()
    logger.info(f"Search index: {search_health['total_records']} records")

    # Initialize telemetry
    telemetry = get_telemetry()
    logger.info("Telemetry collector initialized")

    logger.success(f"{ENGINE_NAME} ready on port {ENGINE_PORT}")

    yield

    # SHUTDOWN
    logger.info(f"Shutting down {ENGINE_NAME}")
    final_snapshot = get_snapshot()
    logger.info(f"Final stats: {final_snapshot.total_queries} queries, {final_snapshot.error_rate:.2%} error rate")


# ============================================================================
# FASTAPI APP
# ============================================================================

app = FastAPI(
    title=f"{ENGINE_NAME} Engine",
    description="TIE Gold Standard engine for pipeline ROW acquisition, condemnation, and surface rights",
    version=ENGINE_VERSION,
    lifespan=lifespan,
)

# CORS middleware
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

@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint."""
    return {
        "engine": ENGINE_NAME,
        "version": ENGINE_VERSION,
        "status": "operational",
        "endpoints": ["/health", "/query", "/metrics", "/doctrines", "/coverage"],
    }


@app.get("/health", response_model=HealthResponse)
async def health():
    """Comprehensive health check."""
    telemetry_snapshot = get_snapshot()
    doctrine_health_data = doctrine_cache_health()
    search_health_data = search_index_health()

    return HealthResponse(
        engine_id=ENGINE_ID,
        engine_name=ENGINE_NAME,
        version=ENGINE_VERSION,
        status="healthy" if telemetry_snapshot.error_rate < 0.1 else "degraded",
        uptime_seconds=telemetry_snapshot.uptime_seconds,
        total_queries=telemetry_snapshot.total_queries,
        error_rate=telemetry_snapshot.error_rate,
        avg_latency_ms=telemetry_snapshot.avg_latency_ms,
        cache_hit_rate=telemetry_snapshot.cache_hit_rate,
        doctrine_count=doctrine_health_data["total_blocks"],
        search_index_records=search_health_data["total_records"],
        cloud_available=_CLOUD_AVAILABLE,
    )


@app.post("/query", response_model=ROWQueryResponse)
async def query_row(request: ROWQueryRequest):
    """Main ROW analysis query endpoint."""
    query_id = str(uuid.uuid4())
    start_time = time.perf_counter()
    phase_latencies: Dict[QueryPhase, float] = {}

    try:
        # Three-layer response
        answer, confidence, stratification, matched_doctrines, search_results = three_layer_response(
            query=request.query,
            mode=request.mode,
            zone=request.zone,
            county=request.county,
            operator=request.operator,
            include_search=request.include_search_results,
            cloud_retrieval=request.cloud_retrieval,
            phase_latencies=phase_latencies,
        )

        # Record drift watcher
        drift_watcher = get_drift_watcher()
        triggered_topics = [d.topic for d in matched_doctrines]
        drift_watcher.record_triggered(triggered_topics)

        # Fact fragility scoring
        fact_fragility = calculate_fact_fragility(request.query, matched_doctrines)

        # Determinism hash
        determinism_hash = calculate_determinism_hash(request.query, triggered_topics, request.mode.value)

        # Issue categories
        issue_categories = list(set(d.category.value for d in matched_doctrines))

        # Total latency
        total_latency_ms = (time.perf_counter() - start_time) * 1000

        # Record telemetry
        record_query(
            query_id=query_id,
            query_text=request.query,
            response_mode=request.mode.value,
            total_latency_ms=total_latency_ms,
            phase_latencies=phase_latencies,
            doctrine_hits=len(matched_doctrines),
            doctrine_misses=0 if matched_doctrines else 1,
            search_results=search_results.total_results if search_results else 0,
            cloud_calls=1 if request.cloud_retrieval else 0,
        )

        # Audit log
        log_query_audit(
            query_id=query_id,
            query=request.query,
            mode=request.mode.value,
            zone=request.zone.value,
            doctrines_triggered=triggered_topics,
            answer=answer,
            confidence=confidence,
            latency_ms=total_latency_ms,
        )

        # Build response
        doctrine_responses = []
        if request.include_doctrines:
            for doctrine in matched_doctrines[:request.max_doctrines]:
                doctrine_responses.append(DoctrineBlockResponse(
                    topic=doctrine.topic,
                    category=doctrine.category.value,
                    confidence=doctrine.confidence,
                    confidence_stratification=doctrine.confidence_stratification.value,
                    conclusion=' '.join(doctrine.conclusion_template),
                    reasoning_summary=doctrine.reasoning_framework,
                    primary_authority=doctrine.primary_authority,
                    controlling_precedent=doctrine.controlling_precedent,
                    tags=doctrine.tags,
                ))

        return ROWQueryResponse(
            query_id=query_id,
            query=request.query,
            mode=request.mode.value,
            zone=request.zone.value,
            answer=answer,
            confidence=confidence,
            confidence_stratification=stratification.value,
            doctrines_triggered=doctrine_responses,
            search_results=search_results if request.include_search_results else None,
            issue_categories=issue_categories,
            fact_fragility_score=fact_fragility,
            determinism_hash=determinism_hash,
            metadata={
                "doctrine_count": len(matched_doctrines),
                "search_result_count": search_results.total_results if search_results else 0,
                "cloud_retrieval_used": request.cloud_retrieval and _CLOUD_AVAILABLE,
            },
            latency_ms=total_latency_ms,
        )

    except Exception as e:
        logger.error(f"Query failed: {e}", exc_info=True)
        total_latency_ms = (time.perf_counter() - start_time) * 1000

        # Record error telemetry
        record_query(
            query_id=query_id,
            query_text=request.query,
            response_mode=request.mode.value,
            total_latency_ms=total_latency_ms,
            phase_latencies=phase_latencies,
            error=str(e),
            error_domain=ErrorDomain.SYSTEM,
        )

        # Audit log error
        log_query_audit(
            query_id=query_id,
            query=request.query,
            mode=request.mode.value,
            zone=request.zone.value,
            doctrines_triggered=[],
            answer="",
            confidence=0.0,
            latency_ms=total_latency_ms,
            error=str(e),
        )

        raise HTTPException(status_code=500, detail=f"Query processing failed: {str(e)}")


@app.get("/metrics")
async def metrics():
    """Get telemetry metrics dashboard."""
    dashboard = telemetry_dashboard()
    return dashboard.dict()


@app.get("/doctrines")
async def list_doctrines(
    category: Optional[str] = Query(None, description="Filter by category"),
    tag: Optional[str] = Query(None, description="Filter by tag"),
):
    """List all doctrine blocks (optionally filtered)."""
    if category:
        try:
            cat_enum = IssueCategory(category)
            blocks = get_blocks_by_category(cat_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid category: {category}")
    elif tag:
        blocks = get_blocks_by_tag(tag)
    else:
        blocks = list(DOCTRINE_BLOCKS.values())

    return {
        "total": len(blocks),
        "doctrines": [
            {
                "topic": b.topic,
                "category": b.category.value,
                "keywords": b.keywords,
                "confidence": b.confidence,
                "tags": b.tags,
            }
            for b in blocks
        ],
    }


@app.get("/coverage", response_model=CoverageMapResponse)
async def coverage_map():
    """Get doctrine coverage map."""
    drift_watcher = get_drift_watcher()
    coverage_stats = drift_watcher.get_coverage_stats()
    coverage_by_category = get_coverage_map()

    # Top categories by doctrine count
    top_categories = [
        {"category": cat, "count": count}
        for cat, count in sorted(coverage_by_category.items(), key=lambda x: x[1], reverse=True)
    ]

    # Identify gaps (categories with <3 doctrines)
    gaps = [cat for cat, count in coverage_by_category.items() if count < 3]

    return CoverageMapResponse(
        total_blocks=coverage_stats["total_doctrines"],
        categories=len(coverage_by_category),
        coverage_by_category=coverage_by_category,
        top_categories=top_categories,
        gaps=gaps,
    )


@app.get("/drift")
async def drift_stats():
    """Get doctrine drift statistics."""
    drift_watcher = get_drift_watcher()
    return drift_watcher.get_coverage_stats()


@app.get("/semantic")
async def semantic_stats():
    """Get semantic normalization statistics."""
    return semantic_health()


@app.get("/search")
async def search_stats():
    """Get search index statistics."""
    return search_index_health()


# ============================================================================
# MAIN (for local testing)
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    logger.info(f"Starting {ENGINE_NAME} v{ENGINE_VERSION} on port {ENGINE_PORT}")
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    uvicorn.run(
        "engine:app",
        host="0.0.0.0",
        port=ENGINE_PORT,
        reload=False,
        log_level="info",
    )
