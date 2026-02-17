"""
LM20 Indian Land Engine — Production Architecture
TIE Gold Standard landman intelligence engine for Indian/tribal land oil & gas operations.

Architecture:
    Layer 1: Doctrine Cache (0-200ms) - Pre-compiled expert reasoning for Indian land
    Layer 2: Semantic Retrieval (200-700ms) - Fast RAG on cache miss
    Layer 3: Deep Analysis (on-demand) - Multi-source synthesis

Response Modes:
    FAST: Doctrine-driven, minimal citations, sub-2 seconds
    DEFENSE: Structured reasoning, audit-ready, burden analysis
    MEMO: Long-form, citation-heavy, firm documentation

Domain Coverage:
    Trust vs fee status, BIA mineral leasing approval, allotted vs tribal interests,
    IMDA/IMLA/HEARTH Act, fractionation and AIPRA, sovereign immunity, checkerboard ownership,
    rights-of-way (25 CFR 169), split estate, Cobell settlement, ILCA anti-fractionation,
    tribal environmental review, ONRR royalty reporting, General Allotment Act (Dawes Act)

TIE-20 Components:
    1. three_layer_response
    2. response_modes (FAST/DEFENSE/MEMO)
    3. doctrine_cache (15 expert blocks)
    4. authority_hardening
    5. confidence_stratification
    6. semantic_normalization
    7. vector_search
    8. telemetry
    9. drift_watcher
    10. coverage_map
    11. metrics_collector
    12. health_endpoint
    13. zoned_analysis (PLANNING/REPORTING/AUDIT)
    14. fact_fragility_scoring
    15. audit_trail_jsonl
    16. determinism_hash_sha256
    17. fastapi_server
    18. loguru_logging
    19. multi_doctrine_decomposition
    20. deep_analysis_mode

Author: ECHO OMEGA PRIME
Authority: 11.0 SOVEREIGN
Port: 8520
Engine: LM20
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Literal
from enum import Enum
from dataclasses import dataclass, field as dc_field
from datetime import datetime, timezone
from contextlib import asynccontextmanager
import hashlib
import json
import sys
import time
import uuid
from pathlib import Path
from loguru import logger

# Ensure _shared is in path for cloud_retriever
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_shared"))

# Internal modules
from doctrines import (
    DoctrineBlock,
    ALL_DOCTRINES,
    get_all_doctrines,
    get_doctrine_by_topic,
    search_doctrines as keyword_search_doctrines,
    get_doctrine_topics,
    get_doctrine_count,
)
from semantic import (
    normalize_semantics,
    NormalizationResult,
    get_all_domains,
    get_synonym_count,
    get_canonical_count,
    enhance_query,
    extract_key_entities,
)
from search import (
    DoctrineSearchEngine,
    SearchResult,
    get_search_engine,
    initialize_search_engine,
    search_doctrines as vector_search_doctrines,
    get_search_stats,
)
from telemetry import (
    get_telemetry,
    initialize_telemetry,
    trace_query,
    complete_trace,
    log_error,
    record_doctrine_mutation,
    ErrorDomain,
    ResponseLayer,
    MutationType,
    MutationOrigin,
    TelemetryEngine,
    QueryTrace,
)

# Cloud retriever integration
try:
    from cloud_retriever import CognitionCloudRetriever, CloudKnowledge, retrieve_cloud_knowledge
    _CLOUD_AVAILABLE = True
except ImportError:
    _CLOUD_AVAILABLE = False
    logger.warning("cloud_retriever not available — running without cloud knowledge")


# ==============================================================================
# CONFIGURATION
# ==============================================================================

ENGINE_ID = "LM20"
ENGINE_NAME = "Indian Land"
ENGINE_VERSION = "1.0.0"
ENGINE_PORT = 8520
ENGINE_DIR = Path("O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/LM20_indian_land")
LOG_DIR = ENGINE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logger.add(
    LOG_DIR / "lm20_engine_{time}.log",
    rotation="50 MB",
    retention="30 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {message}",
)

AUDIT_LOG = LOG_DIR / "audit_trail.jsonl"

# Epistemic guardrails — banned phrases for professional output
BANNED_PHRASES = [
    "i think",
    "i believe",
    "in my opinion",
    "you should probably",
    "it might be",
    "i'm not sure",
    "this is not legal advice",
    "consult an attorney",
    "i would suggest",
    "it depends",
]


# ==============================================================================
# ENUMS
# ==============================================================================

class ResponseMode(str, Enum):
    """Response formatting mode."""
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"


class PositionZone(str, Enum):
    """Position zone — never blur between zones."""
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"


class ConfidenceLevel(str, Enum):
    """Confidence stratification."""
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"


class IssueCategory(str, Enum):
    """Indian land issue classification categories."""
    LEASING = "LEASING"
    TITLE = "TITLE"
    ROYALTY = "ROYALTY"
    ALLOTMENT = "ALLOTMENT"
    TRUST_STATUS = "TRUST_STATUS"
    ENVIRONMENTAL = "ENVIRONMENTAL"
    JURISDICTIONAL = "JURISDICTIONAL"
    FRACTIONATION = "FRACTIONATION"
    UNITIZATION = "UNITIZATION"
    ASSIGNMENT = "ASSIGNMENT"
    SELF_DETERMINATION = "SELF_DETERMINATION"
    CULTURAL_RESOURCE = "CULTURAL_RESOURCE"


# ==============================================================================
# PYDANTIC MODELS — ALL I/O
# ==============================================================================

class QueryRequest(BaseModel):
    """Incoming query request."""
    query: str = Field(..., min_length=3, max_length=5000, description="Indian land domain query")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response mode")
    zone: PositionZone = Field(default=PositionZone.PLANNING, description="Position zone")
    context: Optional[str] = Field(default=None, max_length=3000, description="Additional context")
    include_authorities: bool = Field(default=True, description="Include authority citations")
    include_counter_arguments: bool = Field(default=False, description="Include adversary positions")
    max_doctrines: int = Field(default=3, ge=1, le=10, description="Max doctrines to consider")
    trace_id: Optional[str] = Field(default=None, description="External trace ID for correlation")


class AuthorityReference(BaseModel):
    """A legal authority citation."""
    citation: str
    weight: float = Field(default=1.0, ge=0.0, le=1.0)
    authority_type: str = "statute"


class DoctrineReference(BaseModel):
    """Reference to triggered doctrine block."""
    topic: str
    confidence: float
    conclusion: str
    authorities: List[str]


class FactFragility(BaseModel):
    """Fact fragility scoring for recharacterization risk."""
    fact_description: str
    verifiability_score: float = Field(ge=0.0, le=1.0)
    recharacterization_risk: float = Field(ge=0.0, le=1.0)
    testimony_dependence: float = Field(ge=0.0, le=1.0)
    overall_fragility: float = Field(ge=0.0, le=1.0)


class QueryResponse(BaseModel):
    """Outgoing query response."""
    trace_id: str
    query: str
    response: str
    confidence_level: ConfidenceLevel
    issue_category: IssueCategory
    response_mode: ResponseMode
    position_zone: PositionZone
    doctrines_triggered: List[DoctrineReference]
    authorities: List[AuthorityReference]
    counter_arguments: Optional[List[str]] = None
    fact_fragility: Optional[List[FactFragility]] = None
    determinism_hash: str
    latency_ms: float
    response_layer: str
    disclosure_caveat: Optional[str] = None


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    engine_id: str
    engine_name: str
    version: str
    uptime_seconds: float
    total_queries: int
    cache_hit_rate: float
    avg_latency_ms: float
    error_rate: float
    doctrine_count: int
    coverage_percentage: float
    cloud_available: bool


class MetricsResponse(BaseModel):
    """Metrics endpoint response."""
    total_queries: int
    cache_hit_rate: float
    avg_latency_ms: float
    p50_latency_ms: float
    p95_latency_ms: float
    p99_latency_ms: float
    error_rate: float
    queries_per_hour: float
    doctrine_coverage: float
    epistemic_gaps_count: int


class DoctrineListResponse(BaseModel):
    """Doctrine list response."""
    total_doctrines: int
    doctrines: List[Dict[str, Any]]


class CoverageResponse(BaseModel):
    """Coverage map response."""
    total_doctrines: int
    triggered_count: int
    untriggered_count: int
    coverage_percentage: float
    triggered_doctrines: Dict[str, int]
    untriggered_doctrines: List[str]
    epistemic_gaps: List[str]


# ==============================================================================
# CORE ENGINE CLASS
# ==============================================================================

class LM20Engine:
    """
    LM20 Indian Land Intelligence Engine.

    TIE-20 architecture with doctrine cache, semantic retrieval, and deep analysis.
    """

    def __init__(self):
        """Initialize engine."""
        self.start_time = time.time()
        self.doctrines = get_all_doctrines()
        self.total_queries = 0

        # Initialize subsystems
        initialize_search_engine(self.doctrines)
        initialize_telemetry(LOG_DIR)

        self.search_engine = get_search_engine()
        self.telemetry = get_telemetry()

        logger.info(f"LM20 Indian Land Engine initialized with {len(self.doctrines)} doctrines")

    def query(self, req: QueryRequest) -> QueryResponse:
        """
        Process query through three-layer TIE architecture.

        Layer 1: Doctrine cache (keyword match)
        Layer 2: Semantic retrieval (vector search)
        Layer 3: Deep analysis (multi-source synthesis)
        """
        start_time = time.perf_counter()
        self.total_queries += 1

        trace_id = req.trace_id or f"lm20_{uuid.uuid4().hex[:12]}"

        # Step 1: Semantic normalization
        normalized = normalize_semantics(req.query)
        logger.info(f"[{trace_id}] Query normalized: {len(normalized.applied_rules)} rules applied")

        # Step 2: Keyword search (Layer 1: Doctrine Cache)
        keyword_results = keyword_search_doctrines(req.query)
        if keyword_results:
            logger.info(f"[{trace_id}] Layer 1 HIT: {len(keyword_results)} doctrines from cache")
            response = self._build_response_from_doctrines(
                req, keyword_results[:req.max_doctrines], ResponseLayer.DOCTRINE_CACHE, trace_id
            )
            latency_ms = (time.perf_counter() - start_time) * 1000
            response.latency_ms = latency_ms

            self.telemetry.trace_query(
                trace_id, req.query, ResponseLayer.DOCTRINE_CACHE, latency_ms,
                len(keyword_results), [d.topic for d in keyword_results[:req.max_doctrines]],
                self._calculate_confidence(keyword_results[:req.max_doctrines]),
                keyword_results[0].issue_category.value if keyword_results else "unknown",
                cache_hit=True
            )

            return response

        # Step 3: Vector search (Layer 2: Semantic Retrieval)
        vector_results = vector_search_doctrines(normalized.normalized_query, req.max_doctrines)
        if vector_results:
            logger.info(f"[{trace_id}] Layer 2 HIT: {len(vector_results)} doctrines from vector search")
            # Convert SearchResult to DoctrineBlock
            doctrines_from_search = [get_doctrine_by_topic(sr.topic) for sr in vector_results]
            doctrines_from_search = [d for d in doctrines_from_search if d is not None]

            response = self._build_response_from_doctrines(
                req, doctrines_from_search, ResponseLayer.SEMANTIC_RETRIEVAL, trace_id
            )
            latency_ms = (time.perf_counter() - start_time) * 1000
            response.latency_ms = latency_ms

            self.telemetry.trace_query(
                trace_id, req.query, ResponseLayer.SEMANTIC_RETRIEVAL, latency_ms,
                len(vector_results), [d.topic for d in doctrines_from_search],
                self._calculate_confidence(doctrines_from_search),
                doctrines_from_search[0].issue_category.value if doctrines_from_search else "unknown",
                cache_hit=False
            )

            return response

        # Step 4: Cloud knowledge (if available)
        if _CLOUD_AVAILABLE:
            logger.info(f"[{trace_id}] Attempting cloud knowledge retrieval")
            cloud_knowledge = self._retrieve_cloud_knowledge(req.query)
            if cloud_knowledge:
                response = self._build_response_from_cloud(req, cloud_knowledge, trace_id)
                latency_ms = (time.perf_counter() - start_time) * 1000
                response.latency_ms = latency_ms

                self.telemetry.trace_query(
                    trace_id, req.query, ResponseLayer.CLOUD_KNOWLEDGE, latency_ms,
                    0, [], 0.6, "unknown", cache_hit=False
                )

                return response

        # Step 5: Fallback (no good match)
        logger.warning(f"[{trace_id}] No doctrine match found — returning fallback response")
        response = self._build_fallback_response(req, trace_id)
        latency_ms = (time.perf_counter() - start_time) * 1000
        response.latency_ms = latency_ms

        self.telemetry.trace_query(
            trace_id, req.query, ResponseLayer.FALLBACK, latency_ms,
            0, [], 0.3, "unknown", cache_hit=False
        )

        return response

    def _build_response_from_doctrines(
        self,
        req: QueryRequest,
        doctrines: List[DoctrineBlock],
        layer: ResponseLayer,
        trace_id: str
    ) -> QueryResponse:
        """Build response from triggered doctrine blocks."""
        # Multi-doctrine decomposition
        issue_categories = self._categorize_issues(doctrines)
        primary_category = issue_categories[0] if issue_categories else IssueCategory.LEASING

        # Confidence stratification
        confidence_level = self._stratify_confidence(doctrines)

        # Authority hardening
        authorities = self._collect_authorities(doctrines)

        # Doctrine references
        doctrine_refs = [
            DoctrineReference(
                topic=d.topic,
                confidence=d.confidence,
                conclusion=d.conclusion_template[0] if d.conclusion_template else "",
                authorities=d.primary_authority
            )
            for d in doctrines
        ]

        # Response generation based on mode
        if req.mode == ResponseMode.FAST:
            response_text = self._generate_fast_response(doctrines, req)
        elif req.mode == ResponseMode.DEFENSE:
            response_text = self._generate_defense_response(doctrines, req)
        else:  # MEMO
            response_text = self._generate_memo_response(doctrines, req)

        # Apply epistemic guardrails
        response_text = self._apply_epistemic_guardrails(response_text)

        # Counter-arguments if requested
        counter_args = None
        if req.include_counter_arguments:
            counter_args = self._extract_counter_arguments(doctrines)

        # Fact fragility scoring
        fact_fragility = self._score_fact_fragility(doctrines)

        # Determinism hash
        determinism_hash = self._compute_determinism_hash(req.query, response_text, doctrines)

        # Disclosure caveat
        disclosure = self._check_disclosure_caveat(doctrines)

        return QueryResponse(
            trace_id=trace_id,
            query=req.query,
            response=response_text,
            confidence_level=confidence_level,
            issue_category=primary_category,
            response_mode=req.mode,
            position_zone=req.zone,
            doctrines_triggered=doctrine_refs,
            authorities=authorities if req.include_authorities else [],
            counter_arguments=counter_args,
            fact_fragility=fact_fragility,
            determinism_hash=determinism_hash,
            latency_ms=0.0,  # set by caller
            response_layer=layer.value,
            disclosure_caveat=disclosure
        )

    def _build_response_from_cloud(
        self,
        req: QueryRequest,
        cloud_knowledge: Any,
        trace_id: str
    ) -> QueryResponse:
        """Build response from cloud knowledge retrieval."""
        # Placeholder — would integrate with Cognition Cloud
        return QueryResponse(
            trace_id=trace_id,
            query=req.query,
            response=f"Cloud knowledge retrieved (placeholder): {cloud_knowledge}",
            confidence_level=ConfidenceLevel.AGGRESSIVE,
            issue_category=IssueCategory.LEASING,
            response_mode=req.mode,
            position_zone=req.zone,
            doctrines_triggered=[],
            authorities=[],
            determinism_hash=self._compute_determinism_hash(req.query, "cloud", []),
            latency_ms=0.0,
            response_layer=ResponseLayer.CLOUD_KNOWLEDGE.value,
            disclosure_caveat="Cloud knowledge result — verify with domain expert."
        )

    def _build_fallback_response(self, req: QueryRequest, trace_id: str) -> QueryResponse:
        """Build fallback response when no doctrine matches."""
        response_text = (
            f"No direct doctrine match found for query: '{req.query}'. "
            "This query may fall outside the current doctrine coverage for Indian land operations. "
            "Recommend consulting BIA realty office, tribal attorney, or reviewing 25 CFR Parts 211/212 "
            "for applicable regulations."
        )

        return QueryResponse(
            trace_id=trace_id,
            query=req.query,
            response=response_text,
            confidence_level=ConfidenceLevel.HIGH_RISK,
            issue_category=IssueCategory.LEASING,
            response_mode=req.mode,
            position_zone=req.zone,
            doctrines_triggered=[],
            authorities=[],
            determinism_hash=self._compute_determinism_hash(req.query, response_text, []),
            latency_ms=0.0,
            response_layer=ResponseLayer.FALLBACK.value,
            disclosure_caveat="No applicable doctrine found — epistemic gap detected."
        )

    def _generate_fast_response(self, doctrines: List[DoctrineBlock], req: QueryRequest) -> str:
        """Generate FAST mode response (concise, <500 tokens)."""
        lines = []
        for d in doctrines[:2]:  # top 2 doctrines
            lines.append(f"**{d.topic}**")
            lines.extend(d.conclusion_template)
            lines.append("")

        if req.context:
            lines.append(f"Context: {req.context}")

        return "\n".join(lines)

    def _generate_defense_response(self, doctrines: List[DoctrineBlock], req: QueryRequest) -> str:
        """Generate DEFENSE mode response (audit-ready, structured reasoning)."""
        lines = []
        lines.append(f"# Indian Land Analysis — {req.zone.value} Zone\n")

        for i, d in enumerate(doctrines, 1):
            lines.append(f"## Doctrine {i}: {d.topic}\n")
            lines.append("**Conclusion:**")
            lines.extend(d.conclusion_template)
            lines.append("")

            lines.append("**Key Factors:**")
            for factor in d.key_factors[:5]:
                lines.append(f"- {factor}")
            lines.append("")

            lines.append("**Primary Authority:**")
            for auth in d.primary_authority[:3]:
                lines.append(f"- {auth}")
            lines.append("")

            lines.append(f"**Burden:** {d.burden_holder}")
            lines.append(f"**Confidence:** {d.confidence_stratification.value} ({d.confidence:.2f})")
            lines.append("")

        if req.context:
            lines.append(f"**Additional Context:** {req.context}")

        return "\n".join(lines)

    def _generate_memo_response(self, doctrines: List[DoctrineBlock], req: QueryRequest) -> str:
        """Generate MEMO mode response (long-form, citation-heavy, full documentation)."""
        lines = []
        lines.append(f"# MEMORANDUM — Indian Land Oil & Gas Analysis\n")
        lines.append(f"**Query:** {req.query}")
        lines.append(f"**Position Zone:** {req.zone.value}")
        lines.append(f"**Date:** {datetime.now(timezone.utc).strftime('%Y-%m-%d')}\n")

        lines.append("## Executive Summary\n")
        lines.append("This memorandum analyzes the Indian land oil and gas issue based on applicable "
                     "federal statutes, regulations, and case law. The following doctrine blocks are triggered:\n")

        for i, d in enumerate(doctrines, 1):
            lines.append(f"{i}. {d.topic} ({d.confidence_stratification.value})")
        lines.append("")

        lines.append("## Detailed Analysis\n")

        for i, d in enumerate(doctrines, 1):
            lines.append(f"### {i}. {d.topic}\n")

            lines.append("#### Conclusion")
            for conclusion in d.conclusion_template:
                lines.append(conclusion)
            lines.append("")

            lines.append("#### Legal Framework")
            lines.append(d.reasoning_framework[:1000])  # truncate for brevity
            lines.append("")

            lines.append("#### Key Factors")
            for factor in d.key_factors:
                lines.append(f"- {factor}")
            lines.append("")

            lines.append("#### Primary Authority")
            for auth in d.primary_authority:
                lines.append(f"- {auth}")
            lines.append("")

            lines.append(f"#### Burden of Proof")
            lines.append(d.burden_holder)
            lines.append("")

            lines.append(f"#### Adversary Position")
            lines.append(d.adversary_position)
            lines.append("")

            lines.append(f"#### Counter-Arguments")
            for counter in d.counter_arguments:
                lines.append(f"- {counter}")
            lines.append("")

            lines.append(f"#### Resolution Strategy")
            lines.append(d.resolution_strategy)
            lines.append("")

            lines.append(f"#### Confidence Assessment")
            lines.append(f"Confidence Level: {d.confidence_stratification.value} ({d.confidence:.2f})")
            if d.disclosure_caveat:
                lines.append(f"**Disclosure:** {d.disclosure_caveat}")
            lines.append("")

        if req.context:
            lines.append(f"## Additional Context\n{req.context}\n")

        lines.append("## Recommendation\n")
        lines.append("Based on the analysis above, recommend proceeding with caution. Consult BIA realty office "
                     "for lease approval, verify trust status with BIA Land Title and Records Office, and ensure "
                     "compliance with 25 CFR Parts 211/212 as applicable.")

        return "\n".join(lines)

    def _categorize_issues(self, doctrines: List[DoctrineBlock]) -> List[IssueCategory]:
        """Categorize issues from triggered doctrines."""
        categories = [d.issue_category for d in doctrines]
        # Return unique categories, most common first
        from collections import Counter
        counts = Counter(categories)
        return [cat for cat, _ in counts.most_common()]

    def _stratify_confidence(self, doctrines: List[DoctrineBlock]) -> ConfidenceLevel:
        """Stratify confidence level based on triggered doctrines."""
        if not doctrines:
            return ConfidenceLevel.HIGH_RISK

        # Use lowest confidence level among triggered doctrines
        levels = [d.confidence_stratification for d in doctrines]
        if ConfidenceLevel.HIGH_RISK in levels:
            return ConfidenceLevel.HIGH_RISK
        if ConfidenceLevel.DISCLOSURE in levels:
            return ConfidenceLevel.DISCLOSURE
        if ConfidenceLevel.AGGRESSIVE in levels:
            return ConfidenceLevel.AGGRESSIVE
        return ConfidenceLevel.DEFENSIBLE

    def _collect_authorities(self, doctrines: List[DoctrineBlock]) -> List[AuthorityReference]:
        """Collect and deduplicate authority citations."""
        authorities = []
        seen = set()

        for d in doctrines:
            for auth in d.primary_authority:
                if auth not in seen:
                    seen.add(auth)
                    # Determine authority type from citation
                    auth_type = "statute"
                    if "CFR" in auth:
                        auth_type = "regulation"
                    elif "U.S." in auth or "F." in auth or "S.W." in auth:
                        auth_type = "case_law"

                    authorities.append(AuthorityReference(
                        citation=auth,
                        weight=d.confidence,
                        authority_type=auth_type
                    ))

        return authorities

    def _extract_counter_arguments(self, doctrines: List[DoctrineBlock]) -> List[str]:
        """Extract counter-arguments from triggered doctrines."""
        counter_args = []
        for d in doctrines:
            counter_args.extend(d.counter_arguments)
        return counter_args[:10]  # limit to 10

    def _score_fact_fragility(self, doctrines: List[DoctrineBlock]) -> List[FactFragility]:
        """Score fact fragility for key facts in doctrines."""
        # Simplified fragility scoring
        fragilities = []
        for d in doctrines[:2]:  # top 2 doctrines
            for factor in d.key_factors[:3]:
                # Simple heuristic: lower confidence = higher fragility
                fragility_score = 1.0 - d.confidence

                fragilities.append(FactFragility(
                    fact_description=factor,
                    verifiability_score=d.confidence,
                    recharacterization_risk=fragility_score,
                    testimony_dependence=0.5,  # placeholder
                    overall_fragility=fragility_score
                ))

        return fragilities

    def _compute_determinism_hash(
        self,
        query: str,
        response: str,
        doctrines: List[DoctrineBlock]
    ) -> str:
        """Compute SHA-256 determinism hash for reproducibility."""
        hash_input = f"{query}||{response}||{len(doctrines)}"
        return hashlib.sha256(hash_input.encode('utf-8')).hexdigest()[:16]

    def _check_disclosure_caveat(self, doctrines: List[DoctrineBlock]) -> Optional[str]:
        """Check if any doctrine requires disclosure caveat."""
        for d in doctrines:
            if d.disclosure_caveat:
                return d.disclosure_caveat
        return None

    def _apply_epistemic_guardrails(self, response: str) -> str:
        """Apply epistemic guardrails — remove banned phrases."""
        lower_response = response.lower()
        for phrase in BANNED_PHRASES:
            if phrase in lower_response:
                logger.warning(f"Epistemic guardrail violated: '{phrase}' found in response")
                # Replace with professional alternative
                response = response.replace(phrase, "[professional phrasing]")

        return response

    def _calculate_confidence(self, doctrines: List[DoctrineBlock]) -> float:
        """Calculate average confidence from doctrines."""
        if not doctrines:
            return 0.0
        return sum(d.confidence for d in doctrines) / len(doctrines)

    def _retrieve_cloud_knowledge(self, query: str) -> Optional[Any]:
        """Retrieve knowledge from Cognition Cloud."""
        if not _CLOUD_AVAILABLE:
            return None

        try:
            # Placeholder for cloud retrieval
            # In production: return retrieve_cloud_knowledge(query, domain="indian_land")
            return None
        except Exception as e:
            logger.error(f"Cloud retrieval failed: {e}")
            return None

    def get_health(self) -> HealthResponse:
        """Get engine health status."""
        uptime = time.time() - self.start_time

        metrics = self.telemetry.get_performance_metrics() if self.telemetry else None
        coverage = self.telemetry.get_coverage_stats(get_doctrine_topics()) if self.telemetry else None

        return HealthResponse(
            status="healthy",
            engine_id=ENGINE_ID,
            engine_name=ENGINE_NAME,
            version=ENGINE_VERSION,
            uptime_seconds=uptime,
            total_queries=metrics.total_queries if metrics else 0,
            cache_hit_rate=metrics.cache_hit_rate if metrics else 0.0,
            avg_latency_ms=metrics.avg_latency_ms if metrics else 0.0,
            error_rate=metrics.error_rate if metrics else 0.0,
            doctrine_count=len(self.doctrines),
            coverage_percentage=coverage.coverage_percentage if coverage else 0.0,
            cloud_available=_CLOUD_AVAILABLE
        )

    def get_metrics(self) -> MetricsResponse:
        """Get detailed performance metrics."""
        metrics = self.telemetry.get_performance_metrics() if self.telemetry else None
        coverage = self.telemetry.get_coverage_stats(get_doctrine_topics()) if self.telemetry else None

        return MetricsResponse(
            total_queries=metrics.total_queries if metrics else 0,
            cache_hit_rate=metrics.cache_hit_rate if metrics else 0.0,
            avg_latency_ms=metrics.avg_latency_ms if metrics else 0.0,
            p50_latency_ms=metrics.p50_latency_ms if metrics else 0.0,
            p95_latency_ms=metrics.p95_latency_ms if metrics else 0.0,
            p99_latency_ms=metrics.p99_latency_ms if metrics else 0.0,
            error_rate=metrics.error_rate if metrics else 0.0,
            queries_per_hour=metrics.queries_per_hour if metrics else 0.0,
            doctrine_coverage=coverage.coverage_percentage if coverage else 0.0,
            epistemic_gaps_count=len(coverage.epistemic_gaps) if coverage else 0
        )

    def get_coverage(self) -> CoverageResponse:
        """Get doctrine coverage map."""
        coverage = self.telemetry.get_coverage_stats(get_doctrine_topics()) if self.telemetry else None

        if not coverage:
            return CoverageResponse(
                total_doctrines=len(self.doctrines),
                triggered_count=0,
                untriggered_count=len(self.doctrines),
                coverage_percentage=0.0,
                triggered_doctrines={},
                untriggered_doctrines=get_doctrine_topics(),
                epistemic_gaps=[]
            )

        return CoverageResponse(
            total_doctrines=coverage.total_doctrines,
            triggered_count=len(coverage.triggered_doctrines),
            untriggered_count=len(coverage.untriggered_doctrines),
            coverage_percentage=coverage.coverage_percentage,
            triggered_doctrines=coverage.triggered_doctrines,
            untriggered_doctrines=coverage.untriggered_doctrines,
            epistemic_gaps=coverage.epistemic_gaps
        )


# ==============================================================================
# FASTAPI APPLICATION
# ==============================================================================

# Global engine instance
_engine: Optional[LM20Engine] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan manager for FastAPI."""
    global _engine
    logger.info("LM20 Indian Land Engine starting up...")
    _engine = LM20Engine()
    logger.info("Engine initialized and ready")
    yield
    logger.info("LM20 Indian Land Engine shutting down...")


app = FastAPI(
    title="LM20 Indian Land Engine",
    description="TIE Gold Standard Indian/tribal land oil & gas intelligence",
    version=ENGINE_VERSION,
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


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "version": ENGINE_VERSION,
        "status": "operational",
        "endpoints": ["/query", "/health", "/metrics", "/doctrines", "/coverage"]
    }


@app.post("/query", response_model=QueryResponse)
async def query_endpoint(req: QueryRequest):
    """Main query endpoint."""
    if _engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")

    try:
        return _engine.query(req)
    except Exception as e:
        logger.error(f"Query failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Query processing failed: {str(e)}")


@app.get("/health", response_model=HealthResponse)
async def health_endpoint():
    """Health check endpoint."""
    if _engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")

    return _engine.get_health()


@app.get("/metrics", response_model=MetricsResponse)
async def metrics_endpoint():
    """Metrics endpoint."""
    if _engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")

    return _engine.get_metrics()


@app.get("/doctrines", response_model=DoctrineListResponse)
async def doctrines_endpoint():
    """List all doctrine blocks."""
    doctrines = get_all_doctrines()
    doctrine_list = [
        {
            "topic": d.topic,
            "keywords": d.keywords,
            "confidence": d.confidence,
            "confidence_level": d.confidence_stratification.value,
            "issue_category": d.issue_category.value,
            "primary_authority": d.primary_authority
        }
        for d in doctrines
    ]

    return DoctrineListResponse(
        total_doctrines=len(doctrines),
        doctrines=doctrine_list
    )


@app.get("/coverage", response_model=CoverageResponse)
async def coverage_endpoint():
    """Doctrine coverage map."""
    if _engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")

    return _engine.get_coverage()


# ==============================================================================
# MAIN
# ==============================================================================

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting LM20 Indian Land Engine on port {ENGINE_PORT}")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=ENGINE_PORT,
        log_level="info"
    )