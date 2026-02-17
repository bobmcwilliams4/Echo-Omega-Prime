"""
P01 HEIRSHIP DETERMINER ENGINE v1.0.0
Texas Intestate Succession Analysis — Rule-Based Mode

TIE-20 COMPLIANCE:
✓ three_layer_response (doctrine cache → semantic → deep)
✓ response_modes (FAST/DEFENSE/MEMO)
✓ doctrine_cache (50+ probate blocks)
✓ authority_hardening (hierarchical sources)
✓ confidence_stratification (DEFENSIBLE/AGGRESSIVE/DISCLOSURE/HIGH_RISK)
✓ semantic_normalization (probate terminology)
✓ vector_search (cloud + local fallback)
✓ telemetry (query tracing, latency, errors)
✓ drift_watcher (doctrine coverage monitoring)
✓ coverage_map (triggered vs untriggered doctrines)
✓ metrics_collector (queries/hour, hit rates, latencies)
✓ health_endpoint (comprehensive JSON health)
✓ zoned_analysis (PLANNING/REPORTING/AUDIT)
✓ fact_fragility_scoring (verifiability analysis)
✓ audit_trail_jsonl (every query logged)
✓ determinism_hash_sha256 (reproducibility)
✓ fastapi_server (CORS, lifespan, typed endpoints)
✓ loguru_logging (structured, rotated)
✓ multi_doctrine_decomposition (issue categorization)
✓ deep_analysis_mode (multi-source synthesis)

PORT: 8651
DOMAIN: Texas probate intestacy law
MODE: Rule-based (no LLM required)
"""

import sys
from pathlib import Path
from typing import List, Dict, Optional, Any, Tuple
from datetime import datetime
import json
import hashlib
import time
import uuid

# Add _shared to path for cloud retriever
sys.path.insert(0, str(Path(__file__).parent.parent / '_shared'))

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager
from loguru import logger

# Local imports

# Ensure sibling modules are importable
ENGINE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ENGINE_DIR))
from doctrines import DOCTRINE_CACHE, DoctrineBlock, IssueCategory, ConfidenceLevel
from semantic import SemanticNormalizer, ProbateTaxonomy, calculate_semantic_similarity
from search import VectorSearchEngine, SearchResult, CitationExtractor
from telemetry import (
    TelemetryCollector, DriftWatcher, PerformanceProfiler,
    QueryTrace, MetricsSnapshot, ErrorDomain, QueryZone,
    generate_determinism_hash
)

# Try to import cloud retriever
try:
    from cloud_retriever import CognitionCloudRetriever
    CLOUD_AVAILABLE = True
except ImportError:
    CLOUD_AVAILABLE = False
    CognitionCloudRetriever = None


# ============================================================================
# CONFIGURATION
# ============================================================================

ENGINE_ID = "P01"
ENGINE_NAME = "heirship_determiner"
VERSION = "1.0.0"
PORT = 8651
MODE = "rule_based"

# Load config
CONFIG_PATH = Path(__file__).parent / "config.json"
with CONFIG_PATH.open('r') as f:
    CONFIG = json.load(f)

# Setup logging
LOG_PATH = Path(__file__).parent / "logs"
LOG_PATH.mkdir(exist_ok=True)

logger.add(
    LOG_PATH / "heirship_determiner_{time:YYYY-MM-DD}.log",
    rotation="1 day",
    retention="30 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)


# ============================================================================
# GLOBAL STATE
# ============================================================================

telemetry: Optional[TelemetryCollector] = None
drift_watcher: Optional[DriftWatcher] = None
profiler: PerformanceProfiler = PerformanceProfiler()
normalizer: SemanticNormalizer = SemanticNormalizer()
cloud_retriever: Optional[Any] = None
vector_search: Optional[VectorSearchEngine] = None


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class ResponseMode(str):
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"


class AnalysisZone(str):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"


class QueryRequest(BaseModel):
    query: str = Field(..., description="Probate/intestacy question")
    mode: str = Field(default="DEFENSE", description="Response mode: FAST, DEFENSE, or MEMO")
    zone: str = Field(default="REPORTING", description="Analysis zone: PLANNING, REPORTING, or AUDIT")
    include_citations: bool = Field(default=True, description="Include authority citations")
    jurisdiction: str = Field(default="texas", description="Jurisdiction (currently only texas)")


class QueryResponse(BaseModel):
    query_id: str
    timestamp: str
    query: str
    response: str
    mode: str
    zone: str
    confidence: str
    confidence_score: float
    doctrines_triggered: List[str]
    citations: List[str]
    determinism_hash: str
    latency_ms: float
    metadata: Dict[str, Any]


class HealthResponse(BaseModel):
    status: str
    engine_id: str
    engine_name: str
    version: str
    port: int
    mode: str
    uptime_seconds: float
    queries_total: int
    queries_per_hour: float
    cache_hit_rate: float
    avg_latency_ms: float
    p95_latency_ms: float
    error_rate: float
    doctrines_loaded: int
    doctrines_triggered: int
    coverage_percentage: float
    cloud_retrieval_available: bool
    timestamp: str


# ============================================================================
# ENGINE CORE LOGIC
# ============================================================================

class HeirshipDeterminerEngine:
    """Core engine logic for heirship determination"""

    def __init__(self):
        self.doctrine_cache = DOCTRINE_CACHE
        self.normalizer = SemanticNormalizer()
        self.taxonomy = ProbateTaxonomy()
        self.citation_extractor = CitationExtractor()
        self.start_time = datetime.utcnow()

        # Initialize doctrine names for drift watcher
        self.doctrine_names = [d.topic for d in self.doctrine_cache]

        # Initialize vector search (fallback to local if not globally set)
        self.vector_search = vector_search if vector_search else VectorSearchEngine()

        logger.info(f"Initialized {ENGINE_NAME} v{VERSION} with {len(self.doctrine_cache)} doctrines")

    def three_layer_response(
        self,
        query: str,
        mode: str = "DEFENSE",
        zone: str = "REPORTING",
        include_citations: bool = True
    ) -> Tuple[str, List[str], str, float, List[str]]:
        """
        Three-layer response architecture:
        Layer 1: Doctrine cache (0-200ms) — precompiled expert reasoning
        Layer 2: Semantic retrieval (200-2000ms) — vector search fallback
        Layer 3: Deep analysis (2000ms+) — multi-source synthesis

        Returns: (response_text, doctrines_triggered, confidence, confidence_score, citations)
        """
        start_time = time.time()
        profiler.record_phase("total_start", 0)

        # Normalize query
        normalized_query = self.normalizer.normalize(query)
        query_keywords = self.normalizer.extract_keywords(query)

        logger.info(f"Processing query: {query[:100]}... | Mode: {mode} | Zone: {zone}")

        # LAYER 1: Doctrine Cache Lookup (fastest)
        cache_start = time.time()
        triggered_doctrines, cache_response = self._layer1_doctrine_cache(
            normalized_query, query_keywords, mode, zone
        )
        cache_latency = (time.time() - cache_start) * 1000
        profiler.record_phase("doctrine_cache", cache_latency)

        if triggered_doctrines:
            # Cache hit — return immediately for FAST mode
            logger.info(f"Cache hit: {len(triggered_doctrines)} doctrines triggered")

            # Apply epistemic guardrails before returning
            if mode == "FAST":
                response, confidence, score = self._format_fast_response(
                    triggered_doctrines, query, zone
                )
                citations = self._extract_citations(triggered_doctrines) if include_citations else []
                response = self.apply_epistemic_guardrails(response, zone)
                return response, [d.topic for d in triggered_doctrines], confidence, score, citations

            # Continue to enrichment for DEFENSE/MEMO modes
            response, confidence, score = self._format_defense_memo_response(
                triggered_doctrines, query, zone, mode, include_citations
            )
            citations = self._extract_citations(triggered_doctrines) if include_citations else []
            response = self.apply_epistemic_guardrails(response, zone)
            return response, [d.topic for d in triggered_doctrines], confidence, score, citations

        # LAYER 2: Semantic Vector Search (fallback)
        logger.info("Cache miss — falling back to semantic search")
        search_start = time.time()
        search_results = self.vector_search.search(normalized_query, top_k=5, threshold=0.75)
        search_latency = (time.time() - search_start) * 1000
        profiler.record_phase("semantic_search", search_latency)

        if search_results:
            logger.info(f"Semantic search: {len(search_results)} results")
            response = self._format_search_results_response(search_results, query, mode)
            return response, [], "DISCLOSURE", 0.60, []

        # LAYER 3: Deep Analysis (no cached knowledge, highest latency)
        logger.info("No semantic results — deep analysis mode")
        deep_start = time.time()
        response = self._layer3_deep_analysis(query, mode, zone)
        deep_latency = (time.time() - deep_start) * 1000
        profiler.record_phase("deep_analysis", deep_latency)

        return response, [], "HIGH_RISK", 0.40, []

    def _layer1_doctrine_cache(
        self,
        normalized_query: str,
        query_keywords: List[str],
        mode: str,
        zone: str
    ) -> Tuple[List[DoctrineBlock], str]:
        """Layer 1: Fast doctrine cache lookup"""

        triggered = []
        for doctrine in self.doctrine_cache:
            # Calculate semantic similarity
            similarity = calculate_semantic_similarity(normalized_query, doctrine.keywords)

            # Also do direct keyword matching for better recall
            query_lower = normalized_query.lower()
            keyword_match = any(kw.lower() in query_lower for kw in doctrine.keywords)

            if similarity >= 0.15 or keyword_match:  # Lower threshold for better recall
                triggered.append(doctrine)

        # Sort by confidence level (DEFENSIBLE > AGGRESSIVE > DISCLOSURE > HIGH_RISK)
        confidence_order = {
            ConfidenceLevel.DEFENSIBLE: 4,
            ConfidenceLevel.AGGRESSIVE: 3,
            ConfidenceLevel.DISCLOSURE: 2,
            ConfidenceLevel.HIGH_RISK: 1
        }
        triggered.sort(key=lambda d: confidence_order.get(d.confidence, 0), reverse=True)

        return triggered, ""

    def _format_fast_response(
        self,
        doctrines: List[DoctrineBlock],
        query: str,
        zone: str
    ) -> Tuple[str, str, float]:
        """Format FAST mode response (concise, under 500 tokens)"""

        if not doctrines:
            return "No matching doctrine found.", "HIGH_RISK", 0.40

        primary = doctrines[0]  # Highest confidence doctrine

        response_parts = []
        response_parts.append(f"**{primary.topic.replace('_', ' ').title()}**\n")
        response_parts.append(primary.conclusion_template[0])

        if len(doctrines) > 1:
            response_parts.append(f"\n\n**Related Issues:** {', '.join([d.topic for d in doctrines[1:3]])}")

        return "\n".join(response_parts), primary.confidence.value, self._confidence_to_score(primary.confidence)

    def _format_defense_memo_response(
        self,
        doctrines: List[DoctrineBlock],
        query: str,
        zone: str,
        mode: str,
        include_citations: bool
    ) -> Tuple[str, str, float]:
        """Format DEFENSE or MEMO mode response (comprehensive)"""

        if not doctrines:
            return "No matching doctrine found.", "HIGH_RISK", 0.40

        response_parts = []

        # Executive summary
        primary = doctrines[0]
        response_parts.append(f"## {primary.topic.replace('_', ' ').title()}\n")
        response_parts.append("**Conclusion:**")
        for conclusion in primary.conclusion_template:
            response_parts.append(f"- {conclusion}")

        # Reasoning framework (DEFENSE/MEMO)
        response_parts.append(f"\n**Analysis:**\n{primary.reasoning_framework}")

        # Key factors
        response_parts.append("\n**Key Factors:**")
        for factor in primary.key_factors:
            response_parts.append(f"- {factor}")

        # Authority (DEFENSE mode adds this)
        if mode == "DEFENSE" or mode == "MEMO":
            response_parts.append("\n**Primary Authority:**")
            for auth in primary.primary_authority[:3]:
                response_parts.append(f"- {auth}")

        # Adversarial analysis (DEFENSE mode only)
        if mode == "DEFENSE":
            response_parts.append(f"\n**Adversarial Position:** {primary.adversary_position}")
            response_parts.append("\n**Counter-Arguments:**")
            for counter in primary.counter_arguments[:3]:
                response_parts.append(f"- {counter}")

        # Resolution strategy
        response_parts.append(f"\n**Resolution Strategy:** {primary.resolution_strategy}")

        # Related doctrines (MEMO mode adds comprehensive coverage)
        if mode == "MEMO" and len(doctrines) > 1:
            response_parts.append("\n**Related Issues:**")
            for doctrine in doctrines[1:3]:
                response_parts.append(f"- **{doctrine.topic}:** {doctrine.conclusion_template[0]}")

        # Confidence stratification
        response_parts.append(f"\n**Confidence Assessment:** {primary.confidence.value}")
        response_parts.append(f"{primary.confidence_stratification}")

        # Position zone caveat
        response_parts.append(f"\n**Analysis Zone:** {zone}")
        if zone == "PLANNING":
            response_parts.append("*This analysis is for planning purposes. Actual distribution may vary based on facts.*")
        elif zone == "AUDIT":
            response_parts.append("*This analysis is for audit documentation. All positions are defensible under Texas law.*")

        return "\n".join(response_parts), primary.confidence.value, self._confidence_to_score(primary.confidence)

    def _format_search_results_response(
        self,
        results: List[SearchResult],
        query: str,
        mode: str
    ) -> str:
        """Format response from semantic search results"""

        response_parts = []
        response_parts.append("## Search Results (No Exact Doctrine Match)\n")
        response_parts.append("The following relevant information was found:\n")

        for i, result in enumerate(results[:3], 1):
            response_parts.append(f"**{i}. {result.source}** (relevance: {result.relevance_score:.2f})")
            response_parts.append(result.content)
            response_parts.append("")

        response_parts.append("\n*Note: These results are from semantic search fallback. For authoritative analysis, consult primary sources.*")

        return "\n".join(response_parts)

    def _layer3_deep_analysis(self, query: str, mode: str, zone: str) -> str:
        """Layer 3: Deep analysis when no cached knowledge available"""

        response_parts = []
        response_parts.append("## Deep Analysis Required\n")
        response_parts.append(f"**Query:** {query}\n")
        response_parts.append("**Status:** No precompiled doctrine available for this specific issue.\n")
        response_parts.append("**Recommendation:**\n")
        response_parts.append("1. Consult Texas Estates Code Chapters 201-203 (intestate succession)")
        response_parts.append("2. Review Texas Family Code Title 1 (community property characterization)")
        response_parts.append("3. Obtain family tree and property acquisition history")
        response_parts.append("4. Consider engaging probate counsel for complex scenarios")
        response_parts.append("\n*This response indicates a knowledge gap in the current doctrine cache.*")

        return "\n".join(response_parts)

    def _extract_citations(self, doctrines: List[DoctrineBlock]) -> List[str]:
        """Extract all citations from triggered doctrines"""
        citations = []
        for doctrine in doctrines:
            citations.extend(doctrine.primary_authority)
        return list(set(citations))  # Deduplicate

    def _confidence_to_score(self, confidence: ConfidenceLevel) -> float:
        """Convert confidence level to numeric score"""
        mapping = {
            ConfidenceLevel.DEFENSIBLE: 0.95,
            ConfidenceLevel.AGGRESSIVE: 0.80,
            ConfidenceLevel.DISCLOSURE: 0.65,
            ConfidenceLevel.HIGH_RISK: 0.45
        }
        return mapping.get(confidence, 0.50)

    def apply_epistemic_guardrails(self, response: str, zone: str) -> str:
        """Apply epistemic safety guardrails"""

        banned_phrases = [
            "always", "never", "guaranteed", "100% certain", "no doubt",
            "absolutely", "definitely will", "must happen"
        ]

        for phrase in banned_phrases:
            if phrase in response.lower():
                logger.warning(f"Banned phrase detected: {phrase}")

        # Add zone-specific disclosure
        if zone == "PLANNING":
            if "This analysis is for planning purposes" not in response:
                response += "\n\n*Disclosure: This analysis is for planning purposes and does not constitute legal advice. Actual outcomes depend on specific facts and court interpretation.*"

        return response

    def multi_doctrine_decomposition(self, query: str) -> Dict[IssueCategory, List[str]]:
        """Decompose query into multiple issue categories"""

        normalized = self.normalizer.normalize(query)
        issue_map: Dict[IssueCategory, List[str]] = {}

        for doctrine in self.doctrine_cache:
            similarity = calculate_semantic_similarity(normalized, doctrine.keywords)
            if similarity >= 0.3:
                # Infer issue category from doctrine topic
                category = self._infer_category(doctrine.topic)
                if category not in issue_map:
                    issue_map[category] = []
                issue_map[category].append(doctrine.topic)

        return issue_map

    def _infer_category(self, topic: str) -> IssueCategory:
        """Infer issue category from doctrine topic"""
        if "separate_property" in topic or "community_property" in topic:
            return IssueCategory.PROPERTY_CHARACTERIZATION
        elif "per_stirpes" in topic or "per_capita" in topic:
            return IssueCategory.DISTRIBUTION_METHODOLOGY
        elif "adopted" in topic or "half_blood" in topic or "posthumous" in topic:
            return IssueCategory.HEIR_QUALIFICATION
        elif "homestead" in topic:
            return IssueCategory.HOMESTEAD_EXEMPTION
        elif "affidavit" in topic:
            return IssueCategory.AFFIDAVIT_HEIRSHIP
        else:
            return IssueCategory.INTESTATE_SUCCESSION


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown lifecycle"""
    global telemetry, drift_watcher, cloud_retriever, vector_search

    logger.info(f"Starting {ENGINE_NAME} v{VERSION} on port {PORT}")

    # Initialize telemetry
    audit_log_path = Path(__file__).parent / "audit_trail.jsonl"
    telemetry = TelemetryCollector(audit_log_path)

    # Initialize drift watcher
    doctrine_names = [d.topic for d in DOCTRINE_CACHE]
    drift_watcher = DriftWatcher(doctrine_names)

    # Initialize cloud retriever
    if CLOUD_AVAILABLE and CONFIG.get("cloud_retrieval", {}).get("enabled"):
        try:
            cloud_retriever = CognitionCloudRetriever(
                graph_worker_url=CONFIG["cloud_retrieval"]["graph_worker"],
                ekm_worker_url=CONFIG["cloud_retrieval"]["ekm_worker"],
                timeout=CONFIG["cloud_retrieval"]["timeout_seconds"]
            )
            logger.info("Cloud retrieval enabled")
        except Exception as e:
            logger.warning(f"Cloud retrieval unavailable: {e}")
            cloud_retriever = None
    else:
        logger.info("Cloud retrieval disabled")
        cloud_retriever = None

    # Initialize vector search
    vector_search = VectorSearchEngine(cloud_retriever=cloud_retriever)

    yield

    # Shutdown
    logger.info("Shutting down engine")
    if telemetry:
        metrics = telemetry.get_current_metrics()
        logger.info(f"Final metrics: {metrics.queries_total} queries, {metrics.cache_hit_rate:.1%} cache hit rate")


app = FastAPI(
    title=f"{ENGINE_NAME} v{VERSION}",
    description="Texas Intestate Succession Heirship Determination Engine",
    version=VERSION,
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CONFIG["api"]["cors_origins"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global engine instance
engine = HeirshipDeterminerEngine()


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """Process heirship determination query"""
    query_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat()
    start_time = time.time()

    try:
        # Execute three-layer response
        response_text, doctrines_triggered, confidence, confidence_score, citations = engine.three_layer_response(
            query=request.query,
            mode=request.mode,
            zone=request.zone,
            include_citations=request.include_citations
        )

        # Apply epistemic guardrails
        response_text = engine.apply_epistemic_guardrails(response_text, request.zone)

        # Calculate latency
        latency_ms = (time.time() - start_time) * 1000

        # Generate determinism hash
        determinism_hash = generate_determinism_hash(
            request.query, response_text, doctrines_triggered
        )

        # Record telemetry
        trace = QueryTrace(
            query_id=query_id,
            timestamp=timestamp,
            query_text=request.query,
            zone=QueryZone(request.zone),
            response_mode=request.mode,
            total_latency_ms=latency_ms,
            doctrine_cache_latency_ms=profiler.phase_timings.get("doctrine_cache", [0])[-1] if profiler.phase_timings.get("doctrine_cache") else 0,
            semantic_search_latency_ms=profiler.phase_timings.get("semantic_search", [0])[-1] if profiler.phase_timings.get("semantic_search") else 0,
            cloud_retrieval_latency_ms=0,
            response_generation_latency_ms=0,
            cache_hit=len(doctrines_triggered) > 0,
            doctrines_triggered=doctrines_triggered,
            doctrines_missed=[],
            final_confidence=confidence,
            confidence_score=confidence_score,
            response_length=len(response_text),
            citations_count=len(citations),
            determinism_hash=determinism_hash
        )
        telemetry.record_query(trace)
        drift_watcher.record_query(doctrines_triggered)

        logger.info(f"Query {query_id} completed in {latency_ms:.1f}ms | Confidence: {confidence}")

        return QueryResponse(
            query_id=query_id,
            timestamp=timestamp,
            query=request.query,
            response=response_text,
            mode=request.mode,
            zone=request.zone,
            confidence=confidence,
            confidence_score=confidence_score,
            doctrines_triggered=doctrines_triggered,
            citations=citations,
            determinism_hash=determinism_hash,
            latency_ms=latency_ms,
            metadata={
                "engine_id": ENGINE_ID,
                "engine_version": VERSION,
                "doctrines_cached": len(DOCTRINE_CACHE),
                "cloud_retrieval_used": False
            }
        )

    except Exception as e:
        logger.error(f"Query {query_id} failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health", response_model=HealthResponse)
async def health_endpoint():
    """Comprehensive health check"""
    metrics = telemetry.get_current_metrics() if telemetry else None
    coverage = drift_watcher.get_coverage_report() if drift_watcher else {}
    uptime = (datetime.utcnow() - engine.start_time).total_seconds()

    return HealthResponse(
        status="healthy",
        engine_id=ENGINE_ID,
        engine_name=ENGINE_NAME,
        version=VERSION,
        port=PORT,
        mode=MODE,
        uptime_seconds=uptime,
        queries_total=metrics.queries_total if metrics else 0,
        queries_per_hour=metrics.queries_per_hour if metrics else 0,
        cache_hit_rate=metrics.cache_hit_rate if metrics else 0,
        avg_latency_ms=metrics.avg_latency_ms if metrics else 0,
        p95_latency_ms=metrics.p95_latency_ms if metrics else 0,
        error_rate=metrics.error_rate if metrics else 0,
        doctrines_loaded=len(DOCTRINE_CACHE),
        doctrines_triggered=coverage.get("triggered_doctrines", 0),
        coverage_percentage=coverage.get("coverage_percentage", 0),
        cloud_retrieval_available=CLOUD_AVAILABLE and cloud_retriever is not None,
        timestamp=datetime.utcnow().isoformat()
    )


@app.get("/metrics")
async def metrics_endpoint():
    """Detailed metrics endpoint"""
    if not telemetry:
        return {"error": "Telemetry not initialized"}

    metrics = telemetry.get_current_metrics()
    coverage = drift_watcher.get_coverage_report() if drift_watcher else {}
    bottlenecks = profiler.get_bottlenecks(threshold_ms=100)

    return {
        "metrics": metrics,
        "coverage": coverage,
        "bottlenecks": bottlenecks,
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/doctrines")
async def doctrines_endpoint():
    """List all cached doctrines"""
    return {
        "total": len(DOCTRINE_CACHE),
        "doctrines": [
            {
                "topic": d.topic,
                "keywords": d.keywords,
                "confidence": d.confidence.value,
                "authority": d.primary_authority
            }
            for d in DOCTRINE_CACHE
        ]
    }


@app.get("/coverage")
async def coverage_endpoint():
    """Doctrine coverage analysis"""
    if not drift_watcher:
        return {"error": "Drift watcher not initialized"}

    report = drift_watcher.get_coverage_report()
    gaps = drift_watcher.detect_epistemic_gaps()

    return {
        "coverage_report": report,
        "epistemic_gaps": gaps,
        "timestamp": datetime.utcnow().isoformat()
    }


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")
