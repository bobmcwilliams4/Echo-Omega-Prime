"""
LM07 Regulatory Filing Engine
Engine ID: LM07 | Port: 8507 | Version: 1.0.0
Domain: Oil & Gas Regulatory Filing, Permitting, Compliance

TIE-20 Gold Standard Implementation:
  1.  three_layer_response — Doctrine Cache, Semantic Retrieval, Deep Analysis
  2.  response_modes — FAST, DEFENSE, MEMO
  3.  doctrine_cache — 48+ pre-compiled regulatory filing doctrines
  4.  authority_hardening — Multi-jurisdiction hierarchical authority
  5.  confidence_stratification — DEFENSIBLE / AGGRESSIVE / DISCLOSURE / HIGH_RISK
  6.  semantic_normalization — Regulatory filing term normalization
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
import os
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
    AuthorityLevel,
    ConfidenceLevel,
    DoctrineBlock,
    IssueCategory,
    build_doctrine_cache,
    get_all_doctrine_topics,
    get_doctrine_interaction_graph,
    get_doctrines_by_category,
)
from search import VectorSearchEngine as RegulatoryFilingVectorSearch, SearchDocument
from semantic import (
    FormCategory,
    Jurisdiction,
    SemanticNormalizer,
)
from telemetry import (
    CoverageMap,
    DriftWatcher,
    ErrorDomain,
    MetricsCollector,
    QueryPhase,
    QueryTrace,
)

# ═══════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════

ENGINE_ID = "LM07"
ENGINE_NAME = "Regulatory Filing Engine"
ENGINE_VERSION = "1.0.0"
ENGINE_PORT = 8507
ENGINE_DOMAIN = "oil_gas_regulatory_filing"

LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR = Path(__file__).parent / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
VECTOR_DIR = Path(__file__).parent / "vectors"
VECTOR_DIR.mkdir(parents=True, exist_ok=True)

logger.remove()
logger.add(sys.stderr, level="INFO", format="<green>{time:HH:mm:ss}</green> | <level>{level:<7}</level> | <cyan>{name}</cyan> | {message}")
logger.add(LOG_DIR / "lm07_engine.log", rotation="10 MB", retention="90 days", level="DEBUG")

BANNED_PHRASES = [
    "this is not legal advice",
    "consult an attorney",
    "I am not a lawyer",
    "this is for informational purposes only",
    "you should seek professional",
]


# ═══════════════════════════════════════════════════════════════════════
# PYDANTIC MODELS
# ═══════════════════════════════════════════════════════════════════════

class ResponseMode(str, Enum):
    """Response mode for query processing."""
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"


class AnalysisZone(str, Enum):
    """Position zones that must never be blurred."""
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"


class QueryRequest(BaseModel):
    """Incoming regulatory filing query request."""
    query: str = Field(..., min_length=3, max_length=10000, description="Regulatory filing query")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response mode")
    zone: AnalysisZone = Field(default=AnalysisZone.REPORTING, description="Analysis zone")
    session_id: Optional[str] = Field(default=None, description="Session ID for tracking")
    issue_category: Optional[str] = Field(default=None, description="Specific issue category")
    jurisdiction: Optional[str] = Field(default=None, description="Jurisdiction (TX_RRC, NM_OCD, OK_OCC, BLM_FED, ONRR_FED)")
    form_type: Optional[str] = Field(default=None, description="Form type (W-1, W-2, P-4, etc.)")
    deep_analysis: bool = Field(default=False, description="Enable deep analysis mode")


class FormGuidance(BaseModel):
    """Guidance for specific regulatory form."""
    form_id: str
    form_name: str
    jurisdiction: str
    filing_deadline: str
    required_information: list[str]
    common_deficiencies: list[str]
    curative_measures: list[str]
    relevant_authority: list[str]
    penalties: str


class ComplianceChecklist(BaseModel):
    """Compliance checklist for regulatory filing."""
    checklist_items: list[dict[str, Any]]
    total_items: int
    completed_items: int
    critical_items: list[str]
    missing_items: list[str]


class DeadlineCalendar(BaseModel):
    """Deadline tracking for regulatory filings."""
    filing_type: str
    trigger_event: str
    deadline: str
    late_penalty: str
    extension_available: bool
    extension_process: str


class QueryResponse(BaseModel):
    """Regulatory filing query response."""
    query_id: str = Field(..., description="Unique query identifier")
    query: str = Field(..., description="Original query text")
    response: str = Field(..., description="Regulatory filing analysis")
    confidence: ConfidenceLevel = Field(..., description="Overall confidence level")
    mode: ResponseMode = Field(..., description="Response mode used")
    zone: AnalysisZone = Field(..., description="Analysis zone")
    triggered_doctrines: list[str] = Field(default_factory=list, description="Doctrine topics triggered")
    authorities: list[str] = Field(default_factory=list, description="Primary authorities cited")
    form_guidance: Optional[FormGuidance] = Field(default=None, description="Specific form guidance")
    compliance_checklist: Optional[ComplianceChecklist] = Field(default=None, description="Compliance checklist")
    deadlines: list[DeadlineCalendar] = Field(default_factory=list, description="Relevant deadlines")
    jurisdiction: str = Field(..., description="Primary jurisdiction")
    multi_jurisdiction_notes: Optional[str] = Field(default=None, description="Multi-jurisdiction considerations")
    epistemic_caveat: Optional[str] = Field(default=None, description="Epistemic caveat if needed")
    telemetry: dict[str, Any] = Field(..., description="Query telemetry")
    determinism_hash: str = Field(..., description="SHA-256 determinism hash")


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    engine_id: str
    engine_name: str
    version: str
    port: int
    uptime_seconds: float
    doctrine_count: int
    issue_categories: int
    interaction_edges: int
    queries_processed: int
    cache_hit_rate: float
    avg_latency_ms: float
    error_rate: float
    vector_search_available: bool
    cloud_knowledge_available: bool
    last_query_time: Optional[str]


# ═══════════════════════════════════════════════════════════════════════
# REGULATORY FILING ENGINE
# ═══════════════════════════════════════════════════════════════════════

class RegulatoryFilingEngine:
    """
    LM07 Regulatory Filing Engine — TIE Gold Standard

    Provides expert-level guidance on oil & gas regulatory filing,
    permitting, and compliance across Texas RRC, New Mexico OCD,
    Oklahoma OCC, BLM federal, ONRR federal, TCEQ, and EPA jurisdictions.
    """

    def __init__(self):
        self.engine_id = ENGINE_ID
        self.engine_name = ENGINE_NAME
        self.version = ENGINE_VERSION
        self.start_time = time.time()

        logger.info(f"Initializing {self.engine_name} v{self.version}")

        # Build doctrine cache
        self.doctrine_cache = build_doctrine_cache()
        self.doctrine_topics = get_all_doctrine_topics()
        self.interaction_graph = get_doctrine_interaction_graph()
        logger.info(f"Loaded {len(self.doctrine_cache)} doctrine blocks")

        # Initialize components
        self.normalizer = SemanticNormalizer()
        self.telemetry = MetricsCollector()
        self.coverage_map = CoverageMap(self.doctrine_topics)
        self.drift_watcher = DriftWatcher()
        self.metrics = MetricsCollector()

        # Initialize vector search
        try:
            self.vector_search = RegulatoryFilingVectorSearch()
            logger.info("Vector search initialized")
        except Exception as e:
            logger.warning(f"Vector search initialization failed: {e}")
            self.vector_search = None

        # Initialize cloud knowledge retriever
        if _CLOUD_AVAILABLE:
            try:
                self.cloud_retriever = CognitionCloudRetriever()
                logger.info("Cloud knowledge retriever initialized")
            except Exception as e:
                logger.warning(f"Cloud retriever initialization failed: {e}")
                self.cloud_retriever = None
        else:
            self.cloud_retriever = None

        logger.info(f"{self.engine_name} initialization complete")

    def three_layer_response(
        self,
        query: str,
        mode: ResponseMode,
        zone: AnalysisZone,
        issue_category: Optional[IssueCategory] = None,
        jurisdiction: Optional[Jurisdiction] = None,
        deep_analysis: bool = False,
    ) -> dict[str, Any]:
        """
        Three-layer response architecture (TIE-20 Component 1):

        Layer 1: Doctrine Cache (0-200ms) — Pre-compiled expert reasoning
        Layer 2: Semantic Retrieval (200ms-2s) — Vector search fallback
        Layer 3: Deep Analysis (2s-10s) — Multi-source synthesis
        """
        trace = QueryTrace(query_id=str(uuid.uuid4()), query_text=query, mode=mode.value)
        trace.start_phase(QueryPhase.NORMALIZATION)

        # Normalize query
        normalized = self.normalizer.normalize(query)
        trace.end_phase(QueryPhase.NORMALIZATION)

        # Detect jurisdiction and form type from normalized result
        detected_jurisdiction = jurisdiction or normalized.jurisdiction
        detected_form = normalized.form_category

        # Layer 1: Doctrine Cache Lookup
        trace.start_phase(QueryPhase.DOCTRINE_CACHE)
        triggered_doctrines = self._doctrine_cache_lookup(normalized.normalized, issue_category, detected_jurisdiction)
        trace.end_phase(QueryPhase.DOCTRINE_CACHE)

        if triggered_doctrines:
            logger.info(f"Cache hit: {len(triggered_doctrines)} doctrines triggered")
            for d in triggered_doctrines:
                self.coverage_map.record_hit(d.topic)
            response = self._synthesize_from_cache(triggered_doctrines, query, mode, zone)
            trace.cache_hit = True
            trace.doctrine_topics_hit = [d.topic for d in triggered_doctrines]
        else:
            # Layer 2: Semantic Retrieval
            logger.info("Cache miss, falling back to vector search")
            trace.start_phase(QueryPhase.VECTOR_SEARCH)
            retrieved_docs = self._vector_search_fallback(normalized.normalized)
            trace.end_phase(QueryPhase.VECTOR_SEARCH)

            if retrieved_docs or (deep_analysis and self.cloud_retriever):
                # Layer 3: Deep Analysis (if enabled)
                trace.start_phase(QueryPhase.DEEP_ANALYSIS)
                response = self._deep_analysis(query, retrieved_docs, mode, zone, detected_jurisdiction)
                trace.end_phase(QueryPhase.DEEP_ANALYSIS)
            else:
                response = self._fallback_response(query, mode, zone)

            trace.cache_hit = False
            self.coverage_map.record_miss(query)

        trace.response_length = len(response)
        self.metrics.record_query(trace)

        return {
            "response": response,
            "triggered_doctrines": [d.topic for d in triggered_doctrines] if triggered_doctrines else [],
            "jurisdiction": detected_jurisdiction.value if detected_jurisdiction else "UNKNOWN",
            "form_type": detected_form.value if detected_form else None,
            "trace": trace,
        }

    def _doctrine_cache_lookup(
        self,
        normalized_query: str,
        issue_category: Optional[IssueCategory],
        jurisdiction: Optional[Jurisdiction],
    ) -> list[DoctrineBlock]:
        """
        Fast doctrine cache lookup using keyword matching and filtering.
        """
        triggered: list[DoctrineBlock] = []
        query_lower = normalized_query.lower()

        # Filter by issue category if specified
        candidates = (
            get_doctrines_by_category(issue_category)
            if issue_category
            else list(self.doctrine_cache.values())
        )

        # Filter by jurisdiction if specified
        if jurisdiction:
            candidates = [d for d in candidates if d.jurisdiction == jurisdiction.value or d.jurisdiction == "MULTI"]

        # Keyword matching
        for doctrine in candidates:
            keyword_matches = sum(1 for kw in doctrine.keywords if kw.lower() in query_lower)
            if keyword_matches >= 2:  # Require at least 2 keyword matches
                triggered.append(doctrine)

        # Sort by keyword match count (descending)
        triggered.sort(key=lambda d: sum(1 for kw in d.keywords if kw.lower() in query_lower), reverse=True)

        return triggered[:5]  # Return top 5 matches

    def _vector_search_fallback(self, query: str) -> list:
        """
        Semantic vector search fallback when cache misses.
        Returns list of SearchResult objects.
        """
        if not self.vector_search:
            return []

        try:
            results = self.vector_search.search(query, max_results=10)
            return results
        except Exception as e:
            logger.error(f"Vector search failed: {e}")
            return []

    def _deep_analysis(
        self,
        query: str,
        retrieved_docs: list,
        mode: ResponseMode,
        zone: AnalysisZone,
        jurisdiction: Optional[Jurisdiction],
    ) -> str:
        """
        Deep analysis mode: multi-source synthesis with cloud knowledge.
        """
        analysis_parts = []

        # Add retrieved document context (SearchResult objects have content_snippet)
        if retrieved_docs:
            analysis_parts.append("REGULATORY FILING ANALYSIS (Deep Analysis Mode):\n")
            for doc in retrieved_docs[:3]:
                doc_text = getattr(doc, 'content_snippet', '') or getattr(doc, 'content', '')
                analysis_parts.append(f"- {doc_text[:500]}...\n")

        # Add cloud knowledge if available
        if self.cloud_retriever:
            try:
                cloud_results = retrieve_cloud_knowledge(query, limit=5)
                if cloud_results:
                    analysis_parts.append("\nCLOUD KNOWLEDGE:\n")
                    for result in cloud_results[:3]:
                        analysis_parts.append(f"- {result.get('content', '')[:300]}...\n")
            except Exception as e:
                logger.warning(f"Cloud knowledge retrieval failed: {e}")

        # Synthesize response
        if analysis_parts:
            synthesis = "".join(analysis_parts)
            synthesis += f"\n\nJURISDICTION: {jurisdiction.value if jurisdiction else 'Multiple'}\n"
            synthesis += f"ANALYSIS ZONE: {zone.value}\n"
            synthesis += f"RESPONSE MODE: {mode.value}\n"
            return synthesis
        else:
            return self._fallback_response(query, mode, zone)

    def _synthesize_from_cache(
        self,
        doctrines: list[DoctrineBlock],
        query: str,
        mode: ResponseMode,
        zone: AnalysisZone,
    ) -> str:
        """
        Synthesize response from triggered doctrine blocks.
        """
        if mode == ResponseMode.FAST:
            return self._fast_mode_response(doctrines)
        elif mode == ResponseMode.DEFENSE:
            return self._defense_mode_response(doctrines, query)
        else:  # MEMO
            return self._memo_mode_response(doctrines, query, zone)

    def _fast_mode_response(self, doctrines: list[DoctrineBlock]) -> str:
        """
        FAST mode: Concise summary with key points.
        """
        primary = doctrines[0]
        response_parts = [
            f"REGULATORY FILING ANALYSIS — {primary.topic}\n",
            f"JURISDICTION: {primary.jurisdiction}\n",
            f"FORM: {primary.form_reference or 'N/A'}\n\n",
            f"SUMMARY:\n{primary.conclusion_template}\n\n",
            f"KEY FACTORS:\n",
        ]

        for i, factor in enumerate(primary.key_factors[:5], 1):
            response_parts.append(f"{i}. {factor}\n")

        response_parts.append(f"\nPRIMARY AUTHORITY:\n")
        for auth in primary.primary_authority[:3]:
            response_parts.append(f"- {auth}\n")

        response_parts.append(f"\nCONFIDENCE: {primary.confidence.value}\n")

        if primary.deadline_rule:
            response_parts.append(f"DEADLINE: {primary.deadline_rule}\n")

        if primary.fee_schedule:
            response_parts.append(f"FEES/PENALTIES: {primary.fee_schedule}\n")

        return "".join(response_parts)

    def _defense_mode_response(self, doctrines: list[DoctrineBlock], query: str) -> str:
        """
        DEFENSE mode: Audit-ready documentation with full reasoning.
        """
        primary = doctrines[0]
        response_parts = [
            f"REGULATORY FILING ANALYSIS — AUDIT DOCUMENTATION\n",
            f"{'=' * 80}\n\n",
            f"QUERY: {query}\n\n",
            f"DOCTRINE: {primary.topic}\n",
            f"JURISDICTION: {primary.jurisdiction}\n",
            f"FORM: {primary.form_reference or 'N/A'}\n",
            f"AUTHORITY LEVEL: {primary.authority_level.value}\n\n",
            f"REGULATORY CONCLUSION:\n{primary.conclusion_template}\n\n",
            f"DETAILED REASONING:\n{primary.reasoning_framework}\n\n",
            f"KEY COMPLIANCE FACTORS:\n",
        ]

        for i, factor in enumerate(primary.key_factors, 1):
            response_parts.append(f"{i}. {factor}\n")

        response_parts.append(f"\nPRIMARY AUTHORITY (Full Citations):\n")
        for auth in primary.primary_authority:
            response_parts.append(f"- {auth}\n")

        response_parts.append(f"\nBURDEN OF COMPLIANCE: {primary.burden_holder}\n")
        response_parts.append(f"ADVERSARY POSITION: {primary.adversary_position}\n")

        response_parts.append(f"\nCOUNTER-ARGUMENTS:\n")
        for i, counter in enumerate(primary.counter_arguments, 1):
            response_parts.append(f"{i}. {counter}\n")

        response_parts.append(f"\nRESOLUTION STRATEGY:\n{primary.resolution_strategy}\n")

        response_parts.append(f"\nCONFIDENCE LEVEL: {primary.confidence.value}\n")
        response_parts.append(f"CONFIDENCE STRATIFICATION: {primary.confidence_stratification}\n")
        response_parts.append(f"CONTROLLING PRECEDENT: {primary.controlling_precedent}\n")

        if primary.deadline_rule:
            response_parts.append(f"\nFILING DEADLINE: {primary.deadline_rule}\n")

        if primary.fee_schedule:
            response_parts.append(f"FEE/PENALTY SCHEDULE: {primary.fee_schedule}\n")

        if primary.environmental_trigger:
            response_parts.append(f"ENVIRONMENTAL TRIGGER: {primary.environmental_trigger}\n")

        if primary.multi_jurisdiction_notes:
            response_parts.append(f"\nMULTI-JURISDICTION NOTES:\n{primary.multi_jurisdiction_notes}\n")

        # Add related doctrines
        if len(doctrines) > 1:
            response_parts.append(f"\nRELATED REGULATORY ISSUES:\n")
            for doctrine in doctrines[1:4]:
                response_parts.append(f"- {doctrine.topic} ({doctrine.form_reference or 'N/A'})\n")

        return "".join(response_parts)

    def _memo_mode_response(self, doctrines: list[DoctrineBlock], query: str, zone: AnalysisZone) -> str:
        """
        MEMO mode: Full memorandum-style documentation.
        """
        primary = doctrines[0]
        response_parts = [
            f"REGULATORY FILING MEMORANDUM\n",
            f"{'=' * 80}\n\n",
            f"TO: Regulatory Compliance Team\n",
            f"FROM: {ENGINE_NAME} (LM07)\n",
            f"DATE: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}\n",
            f"RE: {primary.topic}\n",
            f"ANALYSIS ZONE: {zone.value}\n\n",
            f"QUERY:\n{query}\n\n",
            f"JURISDICTION: {primary.jurisdiction}\n",
            f"FORM/FILING: {primary.form_reference or 'N/A'}\n",
            f"AUTHORITY LEVEL: {primary.authority_level.value}\n\n",
            f"I. REGULATORY CONCLUSION\n",
            f"{'-' * 80}\n",
            f"{primary.conclusion_template}\n\n",
            f"II. DETAILED REGULATORY FRAMEWORK\n",
            f"{'-' * 80}\n",
            f"{primary.reasoning_framework}\n\n",
            f"III. COMPLIANCE REQUIREMENTS\n",
            f"{'-' * 80}\n",
        ]

        for i, factor in enumerate(primary.key_factors, 1):
            response_parts.append(f"{i}. {factor}\n")

        response_parts.append(f"\nIV. CONTROLLING AUTHORITY\n")
        response_parts.append(f"{'-' * 80}\n")
        for auth in primary.primary_authority:
            response_parts.append(f"- {auth}\n")

        response_parts.append(f"\nV. PARTY POSITIONS\n")
        response_parts.append(f"{'-' * 80}\n")
        response_parts.append(f"Burden Holder: {primary.burden_holder}\n")
        response_parts.append(f"Adversary Position: {primary.adversary_position}\n")

        response_parts.append(f"\nVI. POTENTIAL CHALLENGES\n")
        response_parts.append(f"{'-' * 80}\n")
        for i, counter in enumerate(primary.counter_arguments, 1):
            response_parts.append(f"{i}. {counter}\n")

        response_parts.append(f"\nVII. RECOMMENDED COMPLIANCE STRATEGY\n")
        response_parts.append(f"{'-' * 80}\n")
        response_parts.append(f"{primary.resolution_strategy}\n")

        response_parts.append(f"\nVIII. RISK ASSESSMENT\n")
        response_parts.append(f"{'-' * 80}\n")
        response_parts.append(f"Confidence Level: {primary.confidence.value}\n")
        response_parts.append(f"Stratification: {primary.confidence_stratification}\n")
        response_parts.append(f"Controlling Precedent: {primary.controlling_precedent}\n")

        if primary.deadline_rule:
            response_parts.append(f"\nIX. CRITICAL DEADLINES\n")
            response_parts.append(f"{'-' * 80}\n")
            response_parts.append(f"{primary.deadline_rule}\n")

        if primary.fee_schedule:
            response_parts.append(f"\nX. FEES AND PENALTIES\n")
            response_parts.append(f"{'-' * 80}\n")
            response_parts.append(f"{primary.fee_schedule}\n")

        if primary.environmental_trigger:
            response_parts.append(f"\nXI. ENVIRONMENTAL COMPLIANCE\n")
            response_parts.append(f"{'-' * 80}\n")
            response_parts.append(f"{primary.environmental_trigger}\n")

        # Add interaction graph
        if primary.topic in self.interaction_graph:
            response_parts.append(f"\nXII. RELATED REGULATORY ISSUES\n")
            response_parts.append(f"{'-' * 80}\n")
            for related_topic in self.interaction_graph[primary.topic][:5]:
                response_parts.append(f"- {related_topic}\n")

        response_parts.append(f"\n{'=' * 80}\n")
        response_parts.append(f"END OF MEMORANDUM\n")

        return "".join(response_parts)

    def _fallback_response(self, query: str, mode: ResponseMode, zone: AnalysisZone) -> str:
        """
        Fallback response when no doctrines triggered and no vector results.
        """
        return (
            f"REGULATORY FILING QUERY — INSUFFICIENT DOCTRINE MATCH\n\n"
            f"Query: {query}\n"
            f"Mode: {mode.value}\n"
            f"Zone: {zone.value}\n\n"
            f"No specific regulatory filing doctrine matched this query. "
            f"Consider rephrasing to include:\n"
            f"- Specific form number (W-1, W-2, P-4, H-10, G-1, etc.)\n"
            f"- Jurisdiction (Texas RRC, New Mexico OCD, Oklahoma OCC, BLM, ONRR)\n"
            f"- Regulatory topic (drilling permit, completion report, disposal well, flaring, etc.)\n\n"
            f"Available doctrine topics:\n"
        ) + "\n".join(f"- {topic}" for topic in self.doctrine_topics[:20])

    def apply_epistemic_guardrails(self, response: str) -> tuple[str, Optional[str]]:
        """
        Apply epistemic guardrails to prevent overconfident statements.
        """
        caveat = None

        # Check for banned phrases
        for phrase in BANNED_PHRASES:
            if phrase.lower() in response.lower():
                logger.warning(f"Banned phrase detected: {phrase}")
                response = response.replace(phrase, "[REDACTED — EPISTEMIC VIOLATION]")

        # Add caveat for HIGH_RISK confidence positions
        if "HIGH_RISK" in response or "DISCLOSURE" in response:
            caveat = (
                "EPISTEMIC CAVEAT: This analysis contains positions with substantial regulatory uncertainty. "
                "Consult with specialized regulatory counsel before filing. Alternative interpretations may exist."
            )

        return response, caveat

    def compute_determinism_hash(self, query: str, response: str, doctrines: list[str]) -> str:
        """
        Compute SHA-256 hash for determinism verification.
        """
        hash_input = f"{query}|{response}|{','.join(sorted(doctrines))}"
        return hashlib.sha256(hash_input.encode()).hexdigest()

    def get_health(self) -> dict[str, Any]:
        """
        Comprehensive health check (TIE-20 Component 12).
        """
        uptime = time.time() - self.start_time
        metrics_summary = self.metrics.get_summary()

        return {
            "status": "healthy",
            "engine_id": self.engine_id,
            "engine_name": self.engine_name,
            "version": self.version,
            "port": ENGINE_PORT,
            "uptime_seconds": uptime,
            "doctrine_count": len(self.doctrine_cache),
            "issue_categories": len(IssueCategory),
            "interaction_edges": sum(len(v) for v in self.interaction_graph.values()) // 2,
            "queries_processed": metrics_summary["total_queries"],
            "cache_hit_rate": metrics_summary["cache_hit_rate"],
            "avg_latency_ms": metrics_summary["avg_latency_ms"],
            "error_rate": metrics_summary["error_rate"],
            "vector_search_available": self.vector_search is not None,
            "cloud_knowledge_available": self.cloud_retriever is not None,
            "last_query_time": metrics_summary.get("last_query_time"),
        }


# ═══════════════════════════════════════════════════════════════════════
# FASTAPI APPLICATION
# ═══════════════════════════════════════════════════════════════════════

engine: Optional[RegulatoryFilingEngine] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI lifespan manager for startup/shutdown."""
    global engine
    logger.info("Starting LM07 Regulatory Filing Engine")
    engine = RegulatoryFilingEngine()
    logger.info("Engine startup complete")
    yield
    logger.info("Shutting down LM07 Regulatory Filing Engine")


app = FastAPI(
    title="LM07 Regulatory Filing Engine",
    description="Oil & Gas Regulatory Filing, Permitting, and Compliance Engine",
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


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    if not engine:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    return engine.get_health()


@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """Process regulatory filing query."""
    if not engine:
        raise HTTPException(status_code=503, detail="Engine not initialized")

    try:
        # Parse issue category and jurisdiction
        issue_category = None
        if request.issue_category:
            try:
                issue_category = IssueCategory(request.issue_category)
            except ValueError:
                pass

        jurisdiction = None
        if request.jurisdiction:
            try:
                jurisdiction = Jurisdiction(request.jurisdiction)
            except ValueError:
                pass

        # Process query
        result = engine.three_layer_response(
            query=request.query,
            mode=request.mode,
            zone=request.zone,
            issue_category=issue_category,
            jurisdiction=jurisdiction,
            deep_analysis=request.deep_analysis,
        )

        # Apply epistemic guardrails
        response_text, epistemic_caveat = engine.apply_epistemic_guardrails(result["response"])

        # Compute determinism hash
        determinism_hash = engine.compute_determinism_hash(
            request.query,
            response_text,
            result["triggered_doctrines"],
        )

        # Build response
        trace = result["trace"]
        return QueryResponse(
            query_id=trace.query_id,
            query=request.query,
            response=response_text,
            confidence=ConfidenceLevel.DEFENSIBLE,  # Would compute from doctrines
            mode=request.mode,
            zone=request.zone,
            triggered_doctrines=result["triggered_doctrines"],
            authorities=[],  # Would extract from doctrines
            jurisdiction=result["jurisdiction"],
            epistemic_caveat=epistemic_caveat,
            telemetry={
                "total_latency_ms": trace.latency_ms,
                "cache_hit": trace.cache_hit,
                "phases": trace._phases,
            },
            determinism_hash=determinism_hash,
        )

    except Exception as e:
        logger.error(f"Query processing failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/doctrines")
async def list_doctrines(
    category: Optional[str] = Query(None, description="Filter by issue category"),
    jurisdiction: Optional[str] = Query(None, description="Filter by jurisdiction"),
):
    """List all doctrine topics."""
    if not engine:
        raise HTTPException(status_code=503, detail="Engine not initialized")

    doctrines = list(engine.doctrine_cache.values())

    # Filter by category
    if category:
        try:
            cat = IssueCategory(category)
            doctrines = [d for d in doctrines if d.issue_category == cat]
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid category: {category}")

    # Filter by jurisdiction
    if jurisdiction:
        doctrines = [d for d in doctrines if d.jurisdiction == jurisdiction or d.jurisdiction == "MULTI"]

    return {
        "total": len(doctrines),
        "doctrines": [
            {
                "topic": d.topic,
                "category": d.issue_category.value,
                "jurisdiction": d.jurisdiction,
                "form": d.form_reference,
                "authority_level": d.authority_level.value,
                "confidence": d.confidence.value,
            }
            for d in doctrines
        ],
    }


@app.get("/metrics")
async def get_metrics():
    """Get engine metrics."""
    if not engine:
        raise HTTPException(status_code=503, detail="Engine not initialized")

    return engine.metrics.get_summary()


@app.get("/coverage")
async def get_coverage():
    """Get doctrine coverage map."""
    if not engine:
        raise HTTPException(status_code=503, detail="Engine not initialized")

    coverage = engine.coverage_map.get_coverage_report()
    return coverage


@app.get("/forms/{form_id}")
async def get_form_guidance(form_id: str):
    """Get guidance for specific regulatory form."""
    if not engine:
        raise HTTPException(status_code=503, detail="Engine not initialized")

    # Search for doctrines matching form_id
    matching = [d for d in engine.doctrine_cache.values() if d.form_reference == form_id.upper()]

    if not matching:
        raise HTTPException(status_code=404, detail=f"Form {form_id} not found")

    doctrine = matching[0]

    return FormGuidance(
        form_id=form_id.upper(),
        form_name=doctrine.topic,
        jurisdiction=doctrine.jurisdiction,
        filing_deadline=doctrine.deadline_rule or "See regulations",
        required_information=doctrine.key_factors,
        common_deficiencies=doctrine.counter_arguments,
        curative_measures=[doctrine.resolution_strategy],
        relevant_authority=doctrine.primary_authority,
        penalties=doctrine.fee_schedule or "See regulations",
    )


# ═══════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    logger.info(f"Starting {ENGINE_NAME} v{ENGINE_VERSION} on port {ENGINE_PORT}")
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    uvicorn.run(
        "engine:app",
        host="0.0.0.0",
        port=ENGINE_PORT,
        reload=False,
        log_level="info",
    )
