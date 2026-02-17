"""
WILL PARSER INTELLIGENCE ENGINE — Production Architecture

Parse will provisions with precision: devises, bequests, conditions, trusts, powers of appointment.
Professional-grade estate planning and probate doctrine system.

Architecture:
    Layer 1: Doctrine Cache (0-200ms) - 52 pre-compiled expert reasoning blocks
    Layer 2: Semantic Retrieval (200-700ms) - Cloud vector search on cache miss
    Layer 3: Deep Analysis (on-demand) - Multi-doctrine synthesis

Response Modes:
    FAST: Doctrine-driven, minimal citations, sub-2 seconds
    DEFENSE: Structured reasoning, litigation-ready, burden analysis
    MEMO: Long-form, citation-heavy, estate planning documentation

Domain: Will construction, testamentary devises, Texas Estates Code
Authority: 11.0 SOVEREIGN
Port: 8652
Version: 1.0.0
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Literal
from enum import Enum
from dataclasses import dataclass
from datetime import datetime, timezone
from contextlib import asynccontextmanager
import hashlib
import time
from pathlib import Path
from loguru import logger

# Local module imports
import sys

# Ensure sibling modules are importable
ENGINE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ENGINE_DIR))
from doctrines import get_all_doctrines, get_doctrine_by_topic, search_doctrines_by_keyword, DoctrineBlock, ConfidenceLevel
from semantic import normalize_semantics, get_related_concepts, extract_statute_references
from search import get_vector_search
from telemetry import (
    get_telemetry,
    trace_query,
    complete_trace,
    log_error,
    record_doctrine_mutation,
    ErrorDomain,
    ResponseLayer,
    MutationType,
    MutationOrigin
)

# Configure logging
LOG_DIR = Path("O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/P02_will_parser/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

logger.add(
    LOG_DIR / "will_parser_{time}.log",
    rotation="50 MB",
    retention="30 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {message}"
)


# ==============================================================================
# ENUMS AND REQUEST/RESPONSE MODELS
# ==============================================================================

class ResponseMode(str, Enum):
    FAST = "fast"
    DEFENSE = "defense"
    MEMO = "memo"


class PositionZone(str, Enum):
    """Separation layer for analysis output."""
    PLANNING = "planning"
    REPORTING = "reporting"
    AUDIT = "audit"


class WillProvisionType(str, Enum):
    """Types of will provisions to parse."""
    SPECIFIC_DEVISE = "specific_devise"
    GENERAL_DEVISE = "general_devise"
    DEMONSTRATIVE_DEVISE = "demonstrative_devise"
    RESIDUARY_CLAUSE = "residuary_clause"
    CLASS_GIFT = "class_gift"
    POWER_OF_APPOINTMENT = "power_of_appointment"
    TRUST_PROVISION = "trust_provision"
    CONDITION = "condition"
    LIFE_ESTATE = "life_estate"
    REVOCATION_CLAUSE = "revocation_clause"
    NO_CONTEST_CLAUSE = "no_contest_clause"
    EXECUTOR_APPOINTMENT = "executor_appointment"


class WillParserRequest(BaseModel):
    """Request model for will parsing queries."""
    query: str = Field(..., description="Will provision text or construction question")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response mode")
    position_zone: PositionZone = Field(default=PositionZone.PLANNING, description="Analysis zone")
    provision_type: Optional[WillProvisionType] = Field(None, description="Type of provision if known")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional context")


class WillParserResponse(BaseModel):
    """Response model for will parser engine."""
    query: str
    normalized_query: str
    response_layer: ResponseLayer
    mode: ResponseMode
    position_zone: PositionZone
    conclusion: str
    reasoning: Optional[str] = None
    authorities: List[str]
    confidence_level: str
    doctrine_topics: List[str]
    statute_references: List[str]
    risk_factors: List[str]
    recommendations: List[str]
    latency_ms: float
    determinism_hash: str
    trace_id: str


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    engine_id: str
    version: str
    port: int
    doctrines_loaded: int
    vector_search_enabled: bool
    telemetry_active: bool
    cache_hit_rate: float
    avg_latency_ms: float
    uptime_seconds: float


# ==============================================================================
# WILL PARSER ENGINE CORE
# ==============================================================================

class WillParserEngine:
    """
    Main intelligence engine for will construction and probate doctrine.
    TIE-20 compliant architecture.
    """

    def __init__(self):
        self.doctrines = get_all_doctrines()
        self.vector_search = get_vector_search()
        self.telemetry = get_telemetry(LOG_DIR)
        self.start_time = time.time()
        self.query_count = 0
        self.cache_hits = 0

        logger.info(f"Will Parser Engine initialized with {len(self.doctrines)} doctrine blocks")

    # ==========================================================================
    # COMPONENT 1: THREE-LAYER RESPONSE
    # ==========================================================================

    def three_layer_response(
        self,
        query: str,
        mode: ResponseMode,
        position_zone: PositionZone,
        provision_type: Optional[WillProvisionType] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> WillParserResponse:
        """
        Execute three-layer response architecture:
        Layer 1: Doctrine cache (0-200ms)
        Layer 2: Semantic retrieval (200-700ms)
        Layer 3: Deep analysis (on-demand)
        """
        start = time.time()
        trace_id = trace_query(query, query)
        self.query_count += 1

        try:
            # Semantic normalization
            norm_result = normalize_semantics(query)
            normalized_query = norm_result.normalized_query
            statute_refs = extract_statute_references(query)

            # Layer 1: Doctrine cache
            matched_doctrines = self._search_doctrine_cache(normalized_query, norm_result.domain_concepts)
            if matched_doctrines:
                self.cache_hits += 1
                response = self._build_response_from_doctrines(
                    query, normalized_query, matched_doctrines, mode, position_zone,
                    ResponseLayer.DOCTRINE_CACHE, trace_id, statute_refs, context or {}
                )
                latency = (time.time() - start) * 1000
                response.latency_ms = round(latency, 2)
                complete_trace(
                    trace_id, ResponseLayer.DOCTRINE_CACHE, latency,
                    [d.topic for d in matched_doctrines], True, response.confidence_level,
                    statute_refs=statute_refs, context=context
                )
                return response

            # Layer 2: Semantic retrieval (vector search)
            vector_results = self.vector_search.search(normalized_query, top_k=5)
            if vector_results:
                response = self._build_response_from_vectors(
                    query, normalized_query, vector_results, mode, position_zone,
                    trace_id, statute_refs, context or {}
                )
                latency = (time.time() - start) * 1000
                response.latency_ms = round(latency, 2)
                complete_trace(
                    trace_id, ResponseLayer.SEMANTIC_RETRIEVAL, latency,
                    [], False, response.confidence_level,
                    vector_search_used=True, statute_refs=statute_refs
                )
                return response

            # Layer 3: Deep analysis (fallback)
            response = self._deep_analysis(
                query, normalized_query, mode, position_zone, trace_id, statute_refs, context or {}
            )
            latency = (time.time() - start) * 1000
            response.latency_ms = round(latency, 2)
            complete_trace(
                trace_id, ResponseLayer.DEEP_ANALYSIS, latency,
                [], False, response.confidence_level
            )
            return response

        except Exception as e:
            log_error(trace_id, str(e), ErrorDomain.SYSTEM)
            raise HTTPException(status_code=500, detail=f"Engine error: {str(e)}")

    # ==========================================================================
    # COMPONENT 2: RESPONSE MODES
    # ==========================================================================

    def _format_response_by_mode(
        self,
        doctrines: List[DoctrineBlock],
        mode: ResponseMode,
        position_zone: PositionZone
    ) -> tuple[str, Optional[str], List[str]]:
        """
        Format response according to selected mode:
        FAST: Concise, doctrine-driven
        DEFENSE: Structured reasoning, audit-ready
        MEMO: Long-form, citation-heavy
        """
        if mode == ResponseMode.FAST:
            # Concise conclusion from primary doctrine
            primary = doctrines[0]
            conclusion = " ".join(primary.conclusion_template)
            reasoning = None
            authorities = primary.primary_authority[:3]

        elif mode == ResponseMode.DEFENSE:
            # Structured reasoning with burden analysis
            primary = doctrines[0]
            conclusion = " ".join(primary.conclusion_template)
            reasoning = f"""
DOCTRINE ANALYSIS:
{primary.reasoning_framework}

BURDEN OF PROOF: {primary.burden_holder}

ADVERSARY POSITION: {primary.adversary_position}

RESOLUTION STRATEGY: {primary.resolution_strategy}

CONFIDENCE STRATIFICATION: {primary.confidence_stratification}
            """.strip()
            authorities = primary.primary_authority

        else:  # MEMO mode
            # Long-form with multiple doctrines and full citations
            primary = doctrines[0]
            conclusions = []
            for i, d in enumerate(doctrines[:3], 1):
                conclusions.append(f"{i}. {' '.join(d.conclusion_template)}")

            conclusion = "\n\n".join(conclusions)
            reasoning = f"""
PRIMARY DOCTRINE: {primary.topic}

{primary.reasoning_framework}

KEY FACTORS:
{chr(10).join(f'  • {factor}' for factor in primary.key_factors)}

COUNTER-ARGUMENTS:
{chr(10).join(f'  • {arg}' for arg in primary.counter_arguments)}

CONTROLLING PRECEDENT: {primary.controlling_precedent or 'Not specified'}

RELATED DOCTRINES:
{chr(10).join(f'  • {d.topic}' for d in doctrines[1:3])}
            """.strip()
            authorities = []
            for d in doctrines[:3]:
                authorities.extend(d.primary_authority)

        return conclusion, reasoning, authorities

    # ==========================================================================
    # COMPONENT 3: DOCTRINE CACHE (52 blocks)
    # ==========================================================================

    def _search_doctrine_cache(
        self,
        normalized_query: str,
        domain_concepts: List[str]
    ) -> List[DoctrineBlock]:
        """
        Search doctrine cache for matching blocks.
        Returns up to 3 best-matching doctrines.
        """
        scored_doctrines = []

        for doctrine in self.doctrines:
            score = 0.0

            # Keyword match in query
            for keyword in doctrine.keywords:
                if keyword.lower() in normalized_query.lower():
                    score += 1.0

            # Domain concept match
            for concept in domain_concepts:
                if concept.lower() in doctrine.topic.lower():
                    score += 2.0
                for keyword in doctrine.keywords:
                    if concept.lower() in keyword.lower():
                        score += 0.5

            # Topic match (highest weight)
            if any(word in doctrine.topic.lower() for word in normalized_query.lower().split()):
                score += 3.0

            if score > 0:
                scored_doctrines.append((score, doctrine))

        # Sort by score and return top 3
        scored_doctrines.sort(reverse=True, key=lambda x: x[0])
        return [d for score, d in scored_doctrines[:3] if score >= 1.0]

    # ==========================================================================
    # COMPONENT 4-6: AUTHORITY, CONFIDENCE, SEMANTIC NORMALIZATION
    # ==========================================================================

    def _apply_authority_hardening(self, authorities: List[str]) -> List[str]:
        """
        Apply hierarchical authority weighting.
        Statutes > Case law > Restatement > Treatises
        """
        weighted = []
        for auth in authorities:
            if "Texas Estates Code §" in auth or "§" in auth:
                weighted.append(("STATUTE", auth))
            elif "S.W." in auth or "Tex." in auth:
                weighted.append(("CASE_LAW", auth))
            elif "Restatement" in auth:
                weighted.append(("RESTATEMENT", auth))
            else:
                weighted.append(("TREATISE", auth))

        # Sort by authority hierarchy
        order = {"STATUTE": 0, "CASE_LAW": 1, "RESTATEMENT": 2, "TREATISE": 3}
        weighted.sort(key=lambda x: order.get(x[0], 99))
        return [auth for _, auth in weighted]

    def _stratify_confidence(
        self,
        doctrines: List[DoctrineBlock],
        cache_hit: bool
    ) -> str:
        """Map confidence to DEFENSIBLE/AGGRESSIVE/DISCLOSURE/HIGH_RISK."""
        if not doctrines:
            return "HIGH_RISK"

        primary = doctrines[0]
        if cache_hit and primary.confidence == ConfidenceLevel.DEFENSIBLE:
            return "DEFENSIBLE"
        elif primary.confidence == ConfidenceLevel.AGGRESSIVE:
            return "AGGRESSIVE"
        elif primary.confidence == ConfidenceLevel.DISCLOSURE:
            return "DISCLOSURE"
        else:
            return "HIGH_RISK"

    # ==========================================================================
    # COMPONENT 7: VECTOR SEARCH (implemented in search.py)
    # ==========================================================================

    # ==========================================================================
    # COMPONENT 8: TELEMETRY (implemented in telemetry.py)
    # ==========================================================================

    # ==========================================================================
    # COMPONENT 9: DRIFT WATCHER (placeholder for future expansion)
    # ==========================================================================

    def _detect_doctrine_drift(self, doctrine_topic: str) -> bool:
        """Detect if doctrine has drifted from original formulation."""
        # Placeholder: would compare current doctrine to baseline hash
        return False

    # ==========================================================================
    # COMPONENT 10: COVERAGE MAP
    # ==========================================================================

    def get_coverage_map(self) -> Dict[str, Any]:
        """Return doctrine coverage map showing triggered vs. untriggered doctrines."""
        all_topics = [d.topic for d in self.doctrines]
        # Would track which doctrines have been triggered in queries
        return {
            "total_doctrines": len(all_topics),
            "topics": all_topics,
            "coverage_rate": "Not yet implemented"
        }

    # ==========================================================================
    # COMPONENT 11: METRICS COLLECTOR (integrated with telemetry)
    # ==========================================================================

    def get_metrics(self) -> Dict[str, Any]:
        """Return performance metrics."""
        perf = self.telemetry.get_performance_metrics()
        return {
            "total_queries": perf.total_queries,
            "cache_hits": perf.cache_hits,
            "cache_misses": perf.cache_misses,
            "cache_hit_rate": round(perf.cache_hits / max(perf.total_queries, 1), 3),
            "avg_latency_ms": perf.avg_latency_ms,
            "p95_latency_ms": perf.p95_latency_ms,
            "p99_latency_ms": perf.p99_latency_ms,
            "error_count": perf.error_count,
            "error_rate": perf.error_rate,
        }

    # ==========================================================================
    # COMPONENT 12: HEALTH ENDPOINT
    # ==========================================================================

    def health_check(self) -> HealthResponse:
        """Comprehensive health check."""
        metrics = self.get_metrics()
        return HealthResponse(
            status="healthy",
            engine_id="P02_will_parser",
            version="1.0.0",
            port=8652,
            doctrines_loaded=len(self.doctrines),
            vector_search_enabled=self.vector_search.enabled,
            telemetry_active=True,
            cache_hit_rate=metrics.get("cache_hit_rate", 0.0),
            avg_latency_ms=metrics.get("avg_latency_ms", 0.0),
            uptime_seconds=round(time.time() - self.start_time, 2)
        )

    # ==========================================================================
    # COMPONENT 13: ZONED ANALYSIS
    # ==========================================================================

    def _apply_position_zone(
        self,
        conclusion: str,
        position_zone: PositionZone
    ) -> str:
        """Apply zone-specific epistemic guardrails."""
        if position_zone == PositionZone.PLANNING:
            # Planning: more flexible, strategic
            disclaimer = "\n\nPLANNING ZONE: This analysis is for estate planning purposes. Testamentary intent and will validity depend on specific facts and circumstances."
        elif position_zone == PositionZone.REPORTING:
            # Reporting: balanced, informational
            disclaimer = "\n\nREPORTING ZONE: This analysis reflects will construction doctrine under Texas law. Actual outcomes depend on specific will language, facts, and judicial interpretation."
        else:  # AUDIT
            # Audit: conservative, disclosure-heavy
            disclaimer = "\n\nAUDIT ZONE: This analysis identifies doctrine and authority only. Will contests involve factual disputes and judicial discretion. Legal counsel should review all will validity and construction questions."

        return conclusion + disclaimer

    # ==========================================================================
    # COMPONENT 14: FACT FRAGILITY SCORING
    # ==========================================================================

    def _assess_fact_fragility(self, doctrines: List[DoctrineBlock]) -> List[str]:
        """Assess fragility of factual predicates."""
        risk_factors = []
        if not doctrines:
            return ["Insufficient doctrine match - analysis based on general principles"]

        primary = doctrines[0]

        # High fragility if relies on witness testimony
        if "witness" in primary.burden_holder.lower():
            risk_factors.append("Relies on witness testimony (availability and credibility risk)")

        # High fragility if testamentary capacity at issue
        if "capacity" in primary.topic.lower():
            risk_factors.append("Testamentary capacity is fact-intensive and subject to expert testimony")

        # High fragility if undue influence claim
        if "undue influence" in primary.topic.lower():
            risk_factors.append("Undue influence involves subjective intent and circumstantial evidence")

        # High fragility if ambiguous will language
        if "ambiguity" in " ".join(primary.keywords).lower():
            risk_factors.append("Will construction depends on extrinsic evidence and judicial interpretation")

        return risk_factors

    # ==========================================================================
    # COMPONENT 15: AUDIT TRAIL (JSONL) - implemented in telemetry
    # ==========================================================================

    # ==========================================================================
    # COMPONENT 16: DETERMINISM HASH (SHA-256)
    # ==========================================================================

    def _compute_determinism_hash(self, query: str, conclusion: str) -> str:
        """Compute SHA-256 hash for reproducibility verification."""
        payload = f"{query}|{conclusion}".encode("utf-8")
        return hashlib.sha256(payload).hexdigest()[:16]

    # ==========================================================================
    # COMPONENT 17: FASTAPI SERVER (defined below)
    # ==========================================================================

    # ==========================================================================
    # COMPONENT 18: LOGURU LOGGING (configured above)
    # ==========================================================================

    # ==========================================================================
    # COMPONENT 19: MULTI-DOCTRINE DECOMPOSITION
    # ==========================================================================

    def _decompose_multi_doctrine_query(self, query: str) -> List[str]:
        """Identify if query spans multiple doctrine areas."""
        issue_categories = []

        keyword_map = {
            "execution": ["witness", "sign", "attest", "formalities", "§251.051"],
            "capacity": ["sound mind", "competent", "lucid interval", "dementia"],
            "validity": ["undue influence", "fraud", "duress", "contest"],
            "construction": ["ambiguous", "intent", "interpret", "meaning"],
            "devise": ["specific", "general", "residuary", "bequest"],
            "revocation": ["revoke", "cancel", "destroy", "subsequent will"],
        }

        query_lower = query.lower()
        for category, keywords in keyword_map.items():
            if any(kw in query_lower for kw in keywords):
                issue_categories.append(category)

        return issue_categories if issue_categories else ["general"]

    # ==========================================================================
    # COMPONENT 20: DEEP ANALYSIS MODE
    # ==========================================================================

    def _deep_analysis(
        self,
        query: str,
        normalized_query: str,
        mode: ResponseMode,
        position_zone: PositionZone,
        trace_id: str,
        statute_refs: List[str],
        context: Dict[str, Any]
    ) -> WillParserResponse:
        """
        Deep analysis when cache misses and vector search fails.
        Multi-source synthesis and reasoning chain.
        """
        # Decompose into issue categories
        issue_categories = self._decompose_multi_doctrine_query(query)

        # Build general response
        conclusion = f"""
This query involves will construction issues in the following areas: {', '.join(issue_categories)}.

Under Texas Estates Code and common law, will construction requires examining:
1. Testator's intent as expressed in the four corners of the will
2. Plain meaning of will language unless ambiguity exists
3. Extrinsic evidence only if latent ambiguity is shown
4. Application of construction rules (specific devise, general devise, residuary clause, anti-lapse, etc.)

Without access to the specific will language and factual context, a detailed analysis is not possible.
Consultation with the relevant doctrine blocks in this engine (52 topics covering Texas Estates Code Chapters 251-256)
would provide specific guidance once the issue is clarified.
        """.strip()

        reasoning = f"""
ISSUE CATEGORIZATION: {', '.join(issue_categories)}

RECOMMENDED DOCTRINE REVIEW:
- Will execution requirements (§251.051 attested will, §251.052 holographic will)
- Testamentary capacity and undue influence standards
- Devise classification (specific, general, demonstrative, residuary)
- Will construction doctrines (anti-lapse §255.153, class gifts, powers of appointment)
- Revocation methods (§253.002)
- Will contest grounds (§256.201)

NEXT STEPS:
1. Identify specific will provision at issue
2. Classify provision type (devise, condition, trust, power, etc.)
3. Apply relevant doctrine block for detailed analysis
        """.strip()

        authorities = [
            "Texas Estates Code Chapter 251 (Will Execution)",
            "Texas Estates Code Chapter 255 (Devise Construction)",
            "Restatement (Third) of Property: Wills and Other Donative Transfers"
        ]

        conclusion = self._apply_position_zone(conclusion, position_zone)
        determinism_hash = self._compute_determinism_hash(query, conclusion)

        return WillParserResponse(
            query=query,
            normalized_query=normalized_query,
            response_layer=ResponseLayer.DEEP_ANALYSIS,
            mode=mode,
            position_zone=position_zone,
            conclusion=conclusion,
            reasoning=reasoning if mode != ResponseMode.FAST else None,
            authorities=authorities,
            confidence_level="DISCLOSURE",
            doctrine_topics=issue_categories,
            statute_references=statute_refs,
            risk_factors=["General analysis without specific will language or facts"],
            recommendations=["Provide will text for provision-specific parsing", "Clarify factual context"],
            latency_ms=0.0,  # Will be set by caller
            determinism_hash=determinism_hash,
            trace_id=trace_id
        )

    # ==========================================================================
    # HELPER: BUILD RESPONSE FROM DOCTRINES
    # ==========================================================================

    def _build_response_from_doctrines(
        self,
        query: str,
        normalized_query: str,
        doctrines: List[DoctrineBlock],
        mode: ResponseMode,
        position_zone: PositionZone,
        layer: ResponseLayer,
        trace_id: str,
        statute_refs: List[str],
        context: Dict[str, Any]
    ) -> WillParserResponse:
        """Build response from matched doctrine blocks."""
        conclusion, reasoning, authorities = self._format_response_by_mode(doctrines, mode, position_zone)
        conclusion = self._apply_position_zone(conclusion, position_zone)
        authorities = self._apply_authority_hardening(authorities)
        confidence = self._stratify_confidence(doctrines, layer == ResponseLayer.DOCTRINE_CACHE)
        risk_factors = self._assess_fact_fragility(doctrines)

        # Extract recommendations from primary doctrine
        primary = doctrines[0]
        recommendations = [primary.resolution_strategy] if primary.resolution_strategy else []

        determinism_hash = self._compute_determinism_hash(query, conclusion)

        return WillParserResponse(
            query=query,
            normalized_query=normalized_query,
            response_layer=layer,
            mode=mode,
            position_zone=position_zone,
            conclusion=conclusion,
            reasoning=reasoning,
            authorities=authorities,
            confidence_level=confidence,
            doctrine_topics=[d.topic for d in doctrines],
            statute_references=statute_refs,
            risk_factors=risk_factors,
            recommendations=recommendations,
            latency_ms=0.0,  # Set by caller
            determinism_hash=determinism_hash,
            trace_id=trace_id
        )

    def _build_response_from_vectors(
        self,
        query: str,
        normalized_query: str,
        vector_results: List[Dict[str, Any]],
        mode: ResponseMode,
        position_zone: PositionZone,
        trace_id: str,
        statute_refs: List[str],
        context: Dict[str, Any]
    ) -> WillParserResponse:
        """Build response from vector search results."""
        # Synthesize conclusion from top vector results
        top_result = vector_results[0]
        conclusion = f"""
Based on semantic retrieval from will construction knowledge base:

{top_result['content']}

(Source: {top_result['source']}, Relevance: {top_result['score']:.2f})
        """.strip()

        authorities = [r['source'] for r in vector_results if r.get('source')]
        conclusion = self._apply_position_zone(conclusion, position_zone)
        determinism_hash = self._compute_determinism_hash(query, conclusion)

        return WillParserResponse(
            query=query,
            normalized_query=normalized_query,
            response_layer=ResponseLayer.SEMANTIC_RETRIEVAL,
            mode=mode,
            position_zone=position_zone,
            conclusion=conclusion,
            reasoning=None if mode == ResponseMode.FAST else "Retrieved via vector search. Cache miss.",
            authorities=authorities[:5],
            confidence_level="DISCLOSURE",
            doctrine_topics=[r.get('topic', 'unknown') for r in vector_results],
            statute_references=statute_refs,
            risk_factors=["Based on vector search, not doctrine cache"],
            recommendations=["Review matched doctrine blocks for detailed analysis"],
            latency_ms=0.0,
            determinism_hash=determinism_hash,
            trace_id=trace_id
        )


# ==============================================================================
# FASTAPI APPLICATION
# ==============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown."""
    logger.info("Will Parser Engine starting up...")
    yield
    logger.info("Will Parser Engine shutting down...")


app = FastAPI(
    title="Will Parser Intelligence Engine",
    description="Parse will provisions - devises, bequests, conditions, trusts, powers. Texas Estates Code authority.",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global engine instance
engine = WillParserEngine()


# ==============================================================================
# API ENDPOINTS
# ==============================================================================

@app.post("/parse", response_model=WillParserResponse)
async def parse_will_provision(request: WillParserRequest):
    """
    Parse will provision or answer will construction question.

    TIE-20 compliant three-layer response architecture.
    """
    try:
        response = engine.three_layer_response(
            query=request.query,
            mode=request.mode,
            position_zone=request.position_zone,
            provision_type=request.provision_type,
            context=request.context
        )
        return response
    except Exception as e:
        logger.error(f"Parse error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health", response_model=HealthResponse)
async def health():
    """Comprehensive health check with metrics."""
    return engine.health_check()


@app.get("/doctrines")
async def list_doctrines():
    """List all available doctrine topics."""
    return {
        "total": len(engine.doctrines),
        "topics": [d.topic for d in engine.doctrines]
    }


@app.get("/doctrine/{topic}")
async def get_doctrine(topic: str):
    """Retrieve specific doctrine block by topic."""
    doctrine = get_doctrine_by_topic(topic)
    if not doctrine:
        raise HTTPException(status_code=404, detail=f"Doctrine topic '{topic}' not found")

    return {
        "topic": doctrine.topic,
        "keywords": doctrine.keywords,
        "conclusion": doctrine.conclusion_template,
        "authorities": doctrine.primary_authority,
        "confidence": doctrine.confidence.value,
    }


@app.get("/metrics")
async def metrics():
    """Return performance metrics."""
    return engine.get_metrics()


@app.get("/coverage")
async def coverage():
    """Return doctrine coverage map."""
    return engine.get_coverage_map()


@app.get("/")
async def root():
    """Root endpoint - engine information."""
    return {
        "engine": "Will Parser Intelligence Engine",
        "version": "1.0.0",
        "port": 8652,
        "mode": "hybrid",
        "doctrines": len(engine.doctrines),
        "endpoints": ["/parse", "/health", "/doctrines", "/doctrine/{topic}", "/metrics", "/coverage"]
    }


# ==============================================================================
# MAIN ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "engine:app",
        host="0.0.0.0",
        port=8652,
        log_level="info",
        reload=False
    )
