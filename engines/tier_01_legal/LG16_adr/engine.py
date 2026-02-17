"""
LG16 ADR Engine - Main FastAPI Engine
=========================================
Production-grade alternative dispute resolution analysis engine implementing
all 20 TIE components for arbitration (FAA 9 USC 1-16, RUAA, AAA, JAMS,
FINRA, ICSID, UNCITRAL, ICC), mediation (UMA, facilitative/evaluative/
transformative), negotiation theory (BATNA/WATNA/ZOPA), hybrid processes
(med-arb, arb-med), clause drafting/enforceability, judicial review of
awards (vacatur under FAA Section 10), confirmation/enforcement under the
New York Convention, class action arbitration, securities arbitration,
employment arbitration, consumer arbitration, construction disputes,
oil and gas JOA arbitration, Texas ADR Act (CPRC Ch. 154), and
international commercial/investment treaty arbitration.

TIE-20 Components:
    1.  three_layer_response
    2.  response_modes (fast, analysis, memo, clause_review, process_design)
    3.  doctrine_cache
    4.  authority_hardening
    5.  confidence_stratification
    6.  semantic_normalization
    7.  vector_search_tfidf (TF-IDF inverted index)
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

Port: 8406
Engine: LG16 ADR Engine
Version: 2.0.0
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
    get_doctrine_cache,
    get_doctrine_cache_hash,
    get_doctrine_cache_stats,
    get_stale_doctrines,
    search_doctrines,
    verify_doctrine_integrity,
)
from search import (
    ArbitrationRulesResult,
    ArbitrationRulesSearcher,
    AwardEnforceabilityChecker,
    AwardEnforceabilityResult,
    ClauseValidationResult,
    ClauseValidator,
    DisputeResolutionAdvisor,
    DisputeResolutionAdvisory,
    DoctrineSearchIndex,
    SearchResult,
    compute_query_hash,
    get_clause_validator,
    get_dispute_advisor,
    get_enforceability_checker,
    get_rules_searcher,
    get_search_index,
)
from semantic import (
    ArbitrationClauseAnalyzer,
    NormalizationResult,
    get_jurisdiction_map,
    get_semantic_map,
    get_semantic_map_hash,
    get_semantic_map_version,
    normalize_query,
    verify_dictionary_integrity,
)
from telemetry import (
    ADRMetricType,
    AuditTrailWriter,
    CitationLookupType,
    DriftSeverity,
    DriftWatcher,
    ErrorDomain,
    MetricsAggregator,
    MutationOrigin,
    MutationType,
    QueryTrace,
    ResponseLayer,
    TelemetryCollector,
    complete_trace,
    get_telemetry,
    log_error,
    record_citation_lookup,
    record_doctrine_mutation,
    trace_query,
)


# ============================================================================
# CONSTANTS
# ============================================================================

ENGINE_ID: str = "LG16"
ENGINE_NAME: str = "ADR Engine (Alternative Dispute Resolution)"
ENGINE_VERSION: str = "2.0.0"
ENGINE_PORT: int = 8406
ENGINE_HOST: str = "0.0.0.0"
ENGINE_AUTHORITY: float = 5.0
ENGINE_TIER: str = "LEGAL"
ENGINE_MODE: str = "DET"

CONFIG_PATH: Path = Path(__file__).parent / "config.json"
LOG_DIR: Path = Path(__file__).parent / "logs"
AUDIT_LOG_PATH: Path = LOG_DIR / "audit_trail.jsonl"
DRIFT_REGISTRY_PATH: Path = Path(__file__).parent / "doctrine_drift_registry.json"

BANNED_PHRASES: List[str] = [
    "This arbitration clause is definitely enforceable",
    "There is absolutely no basis to vacate this award",
    "You will certainly win this arbitration",
    "The FAA does not apply here",
    "This clause is guaranteed to be upheld",
    "There is zero risk of unconscionability",
    "No court would compel arbitration in this case",
    "The New York Convention will definitely enforce this award",
    "ICSID jurisdiction is guaranteed",
    "This is absolutely a valid delegation clause",
    "No arbitrator would rule against you",
    "Class arbitration is definitely available",
    "The mediation will certainly succeed",
    "This arbitration agreement covers all possible disputes",
]

REQUIRED_DISCLAIMERS: Dict[str, str] = {
    "not_legal_advice": (
        "This analysis is for informational purposes only and does not "
        "constitute legal advice. Consult a licensed attorney for specific "
        "legal guidance on ADR matters."
    ),
    "jurisdiction_specific": (
        "ADR law varies significantly by jurisdiction, including differences "
        "between state arbitration acts, the FAA, and international conventions. "
        "This analysis may not apply in all jurisdictions."
    ),
    "fact_dependent": (
        "ADR outcomes depend heavily on specific facts, arbitration agreement "
        "language, applicable rules, and the selected decision-maker. This "
        "analysis is based on the information provided."
    ),
    "enforcement_risk": (
        "Arbitration award enforcement and clause enforceability involve "
        "evolving legal standards. Courts may reach different conclusions "
        "depending on the facts and applicable precedent."
    ),
}

AUTHORITY_WEIGHTS: Dict[str, int] = {
    "us_supreme_court": 100,
    "federal_circuit_court": 85,
    "federal_district_court": 70,
    "state_supreme_court": 90,
    "state_appellate_court": 75,
    "state_trial_court": 55,
    "federal_statute": 95,
    "state_statute": 90,
    "cfr_regulation": 80,
    "treaty": 95,
    "model_law": 70,
    "institutional_rule": 75,
    "advisory_opinion": 60,
    "treatise": 40,
    "law_review": 30,
    "restatement": 50,
}

CONFIDENCE_BANDS: Dict[str, Dict[str, Any]] = {
    "DEFENSIBLE": {"min_score": 0.85, "label": "Position is well-supported by established ADR law and precedent", "requires_caveat": False},
    "SUPPORTABLE": {"min_score": 0.65, "label": "Position has reasonable support but some uncertainty in application", "requires_caveat": True},
    "DISCLOSURE": {"min_score": 0.50, "label": "Position requires disclosure of contrary authority or enforcement risk", "requires_caveat": True},
    "HIGH_RISK": {"min_score": 0.0, "label": "Position faces significant adverse authority or circuit split", "requires_caveat": True},
}

ADR_ZONE_METRIC_MAP: Dict[str, ADRMetricType] = {
    "arbitration": ADRMetricType.ARBITRATION_QUERY,
    "mediation": ADRMetricType.MEDIATION_QUERY,
    "negotiation": ADRMetricType.NEGOTIATION_QUERY,
    "enforcement": ADRMetricType.ENFORCEMENT_QUERY,
    "clause_review": ADRMetricType.CLAUSE_REVIEW,
    "process_design": ADRMetricType.PROCESS_DESIGN,
    "vacatur": ADRMetricType.VACATUR_ANALYSIS,
    "ny_convention": ADRMetricType.NY_CONVENTION_QUERY,
    "icsid": ADRMetricType.ICSID_QUERY,
    "consumer": ADRMetricType.CONSUMER_ARB_QUERY,
    "employment": ADRMetricType.EMPLOYMENT_ARB_QUERY,
    "securities": ADRMetricType.SECURITIES_ARB_QUERY,
    "construction": ADRMetricType.CONSTRUCTION_ARB_QUERY,
    "oil_gas": ADRMetricType.OIL_GAS_ARB_QUERY,
    "texas_adr": ADRMetricType.TEXAS_ADR_QUERY,
    "international": ADRMetricType.INTERNATIONAL_ARB_QUERY,
    "class_arbitration": ADRMetricType.CLASS_ARBITRATION_QUERY,
    "hybrid": ADRMetricType.HYBRID_PROCESS_QUERY,
}


# ============================================================================
# PYDANTIC REQUEST/RESPONSE MODELS
# ============================================================================

class QueryRequest(BaseModel):
    """Incoming query request."""
    query: str = Field(..., min_length=3, max_length=5000, description="The ADR law question")
    mode: str = Field("fast", description="Response mode: fast, analysis, memo, clause_review, process_design")
    jurisdiction: Optional[str] = Field(None, description="Jurisdiction filter (e.g. TX, CA, NY, FEDERAL, INTERNATIONAL)")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context for analysis")
    include_citations: bool = Field(True, description="Include statutory and case citations")
    include_practice_tips: bool = Field(False, description="Include practice tips in response")
    max_results: int = Field(5, ge=1, le=20, description="Maximum doctrine results to return")

    @field_validator("mode")
    @classmethod
    def validate_mode(cls, v: str) -> str:
        valid_modes = {"fast", "analysis", "memo", "clause_review", "process_design"}
        if v not in valid_modes:
            raise ValueError(f"Invalid mode '{v}'. Must be one of: {valid_modes}")
        return v


class ClauseReviewRequest(BaseModel):
    """Arbitration clause review request."""
    clause_text: str = Field(..., min_length=10, max_length=10000, description="Full text of the arbitration clause")
    consumer: bool = Field(False, description="Is this a consumer contract?")
    employment: bool = Field(False, description="Is this an employment agreement?")
    international: bool = Field(False, description="Is this for international disputes?")


class ProcessDesignRequest(BaseModel):
    """Dispute resolution process design request."""
    dispute_type: str = Field(..., min_length=2, description="Type of dispute (commercial, employment, securities, etc.)")
    amount: float = Field(0.0, ge=0, description="Amount in dispute (USD)")
    complexity: str = Field("medium", description="Dispute complexity: low, medium, high")
    ongoing_relationship: bool = Field(False, description="Do parties have an ongoing relationship?")
    confidentiality_needed: bool = Field(True, description="Is confidentiality important?")
    speed_priority: str = Field("medium", description="Speed priority: fast, medium, slow")
    international: bool = Field(False, description="Is this an international dispute?")
    number_of_parties: int = Field(2, ge=2, le=50, description="Number of parties")


class AwardEnforceabilityRequest(BaseModel):
    """Award enforceability analysis request."""
    description: str = Field(..., min_length=10, max_length=10000, description="Description of the award and circumstances")
    international: bool = Field(False, description="Is this an international arbitration award?")
    seat: Optional[str] = Field(None, description="Seat of arbitration (city/country)")
    enforcement_country: str = Field("US", description="Country where enforcement is sought")


class DisputeClassifyRequest(BaseModel):
    """Dispute classification request."""
    description: str = Field(..., min_length=10, max_length=5000, description="Description of the dispute")
    parties: Optional[List[str]] = Field(None, description="Parties involved")
    industry: Optional[str] = Field(None, description="Industry sector")
    jurisdiction: Optional[str] = Field(None, description="Jurisdiction")


class DriftSignal(BaseModel):
    """Doctrine drift signal."""
    signal_type: str = Field(..., description="Type of drift signal")
    topic: str = Field(..., description="Affected doctrine topic")
    description: str = Field(..., description="Description of the change")
    source: Optional[str] = Field(None, description="Source of the signal")
    authority_level: Optional[str] = Field(None, description="Authority level of the source")
    confidence_impact: float = Field(0.0, description="Impact on confidence score (-1.0 to 1.0)")


class FactFragilityRequest(BaseModel):
    """Fact fragility scoring request."""
    facts: List[str] = Field(..., min_length=1, description="List of factual assertions to score")
    jurisdiction: Optional[str] = Field(None, description="Jurisdiction context")
    adr_zone: Optional[str] = Field(None, description="ADR zone context")


class MultiDoctrineRequest(BaseModel):
    """Multi-doctrine decomposition request."""
    query: str = Field(..., min_length=3, max_length=5000, description="Complex query to decompose")
    mode: str = Field("analysis", description="Response mode")
    jurisdiction: Optional[str] = Field(None, description="Jurisdiction filter")
    max_doctrines: int = Field(5, ge=1, le=10, description="Maximum doctrines to decompose into")


class DeepAnalysisRequest(BaseModel):
    """Deep analysis request."""
    query: str = Field(..., min_length=3, max_length=10000, description="Query for deep analysis")
    jurisdiction: Optional[str] = Field(None, description="Jurisdiction filter")
    include_risk_assessment: bool = Field(True, description="Include risk assessment")
    include_alternatives: bool = Field(True, description="Include alternative approaches")
    include_timeline: bool = Field(False, description="Include timeline considerations")


class EngineResponse(BaseModel):
    """Standard engine response."""
    engine_id: str = ENGINE_ID
    engine_name: str = ENGINE_NAME
    engine_version: str = ENGINE_VERSION
    query_hash: str
    response_mode: str
    confidence_score: float
    confidence_band: str
    confidence_label: str
    requires_caveat: bool
    layer_used: str
    jurisdiction: Optional[str]
    adr_zone: Optional[str]
    analysis: Dict[str, Any]
    citations: List[Dict[str, Any]]
    disclaimers: List[str]
    practice_tips: List[str]
    determinism_hash: str
    trace_id: str
    processing_time_ms: float
    timestamp: str


# ============================================================================
# CORE ENGINE LOGIC
# ============================================================================

class ADREngine:
    """Core engine implementing all 20 TIE components for ADR law.

    Orchestrates doctrine cache, semantic normalization, search, telemetry,
    authority hardening, confidence stratification, drift watching, zoned
    analysis, and deep analysis for alternative dispute resolution queries.
    """

    def __init__(self, config: Dict[str, Any]) -> None:
        self._config: Dict[str, Any] = config
        self._engine_id: str = config.get("engine_id", ENGINE_ID)
        self._port: int = config.get("port", ENGINE_PORT)
        self._authority: float = config.get("authority_level", ENGINE_AUTHORITY)

        # TIE Component 3: Doctrine Cache
        self._doctrine_cache: DoctrineCacheIndex = build_doctrine_cache()

        # TIE Component 7: Vector Search (TF-IDF inverted index)
        self._search_index: DoctrineSearchIndex = get_search_index()

        # TIE Component 6: Semantic Normalization
        self._semantic_version: str = get_semantic_map_version()

        # TIE Component 8: Telemetry Module
        self._telemetry: TelemetryCollector = get_telemetry(LOG_DIR)

        # TIE Component 11: Metrics Collector
        self._metrics: MetricsAggregator = self._telemetry._metrics

        # Specialized analyzers
        self._rules_searcher: ArbitrationRulesSearcher = get_rules_searcher()
        self._enforceability_checker: AwardEnforceabilityChecker = get_enforceability_checker()
        self._clause_validator: ClauseValidator = get_clause_validator()
        self._dispute_advisor: DisputeResolutionAdvisor = get_dispute_advisor()
        self._clause_analyzer: ArbitrationClauseAnalyzer = ArbitrationClauseAnalyzer()

        # TIE Component 9: Doctrine Drift Watcher
        self._drift_registry: Dict[str, Any] = self._load_drift_registry()

        # TIE Component 15: Audit Trail
        self._audit: AuditTrailWriter = self._telemetry.audit

        # Index doctrine blocks for search
        self._index_doctrines()

        self._boot_time: str = datetime.now(timezone.utc).isoformat()
        self._query_count: int = 0

        logger.info(
            f"ADREngine initialized | id={self._engine_id} | "
            f"port={self._port} | doctrines={len(DOCTRINE_BLOCKS)} | "
            f"semantic_v={self._semantic_version}"
        )

    # -----------------------------------------------------------------------
    # Initialization helpers
    # -----------------------------------------------------------------------

    def _index_doctrines(self) -> None:
        """Index all doctrine blocks into the TF-IDF search index."""
        for block in DOCTRINE_BLOCKS:
            self._search_index.add_document(
                doc_id=block.topic,
                topic=block.topic,
                content=block.content_for_search(),
                adr_category=block.category,
                authority_score=block.authority_score,
                jurisdiction=block.jurisdiction,
                metadata={
                    "subcategory": block.subcategory,
                    "key_statutes": block.key_statutes[:3],
                    "leading_cases": block.leading_cases[:2],
                    "confidence": block.confidence,
                },
            )
        logger.info(f"Indexed {len(DOCTRINE_BLOCKS)} doctrine blocks into search index")

    def _load_drift_registry(self) -> Dict[str, Any]:
        """Load the doctrine drift registry from disk."""
        if DRIFT_REGISTRY_PATH.exists():
            try:
                with open(DRIFT_REGISTRY_PATH, "r", encoding="utf-8") as fh:
                    return json.load(fh)
            except (json.JSONDecodeError, OSError) as exc:
                logger.warning(f"Failed to load drift registry: {exc}")
        return {"signals": [], "last_check": "", "version": ENGINE_VERSION}

    def _save_drift_registry(self) -> None:
        """Save the doctrine drift registry to disk."""
        try:
            DRIFT_REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
            with open(DRIFT_REGISTRY_PATH, "w", encoding="utf-8") as fh:
                json.dump(self._drift_registry, fh, indent=2)
        except OSError as exc:
            logger.error(f"Failed to save drift registry: {exc}")

    # -----------------------------------------------------------------------
    # TIE Component 13: Zoned Analysis
    # -----------------------------------------------------------------------

    def _detect_adr_zone(self, normalization: NormalizationResult) -> str:
        """Detect the ADR zone for the query."""
        zone_keywords: Dict[str, List[str]] = {
            "arbitration": ["arbitration", "arbitrate", "arbitrator", "arbitral", "faa", "9 usc"],
            "mediation": ["mediation", "mediate", "mediator", "uma", "facilitative", "evaluative", "transformative"],
            "negotiation": ["negotiation", "negotiate", "batna", "watna", "zopa", "settlement"],
            "enforcement": ["enforce", "enforcement", "confirm", "confirmation", "vacatur", "vacate", "modify"],
            "clause_review": ["clause", "provision", "agreement", "drafting", "unconscionability", "pathological"],
            "process_design": ["process", "design", "recommend", "which method", "best approach"],
            "ny_convention": ["new york convention", "nyc", "foreign award", "international enforcement"],
            "icsid": ["icsid", "investor state", "investment treaty", "bilateral investment", "bit"],
            "consumer": ["consumer", "adhesion", "mandatory arbitration", "forced arbitration"],
            "employment": ["employment", "employee", "employer", "epic systems", "workplace"],
            "securities": ["securities", "finra", "broker", "investment fraud", "churning", "suitability"],
            "construction": ["construction", "aia", "contractor", "subcontractor", "defect", "delay claim"],
            "oil_gas": ["oil", "gas", "joa", "operating agreement", "mineral", "royalty", "wellbore"],
            "texas_adr": ["texas adr", "cprc 154", "cprc 171", "texas arbitration", "tex. civ. prac."],
            "international": ["international", "cross-border", "icc", "uncitral", "lcia", "siac"],
            "class_arbitration": ["class arbitration", "class action", "class waiver", "at&t v. concepcion", "epic systems"],
            "hybrid": ["med-arb", "arb-med", "hybrid", "multi-step", "escalation clause"],
        }

        query_lower = normalization.normalized_query.lower()
        all_tokens = normalization.tokens + [t.get("canonical", "") for t in normalization.matched_terms]
        token_text = " ".join(all_tokens).lower()
        combined = query_lower + " " + token_text

        scores: Dict[str, float] = {}
        for zone, keywords in zone_keywords.items():
            score = sum(1.0 for kw in keywords if kw in combined)
            if score > 0:
                scores[zone] = score

        if scores:
            return max(scores, key=scores.get)
        return "arbitration"

    # -----------------------------------------------------------------------
    # TIE Component 4: Authority Hardening
    # -----------------------------------------------------------------------

    def _harden_response(self, text: str) -> str:
        """Remove banned phrases and apply authority hardening."""
        hardened = text
        for phrase in BANNED_PHRASES:
            if phrase.lower() in hardened.lower():
                idx = hardened.lower().find(phrase.lower())
                hardened = hardened[:idx] + "[POSITION REQUIRES ANALYSIS]" + hardened[idx + len(phrase):]
        return hardened

    # -----------------------------------------------------------------------
    # TIE Component 5: Confidence Stratification
    # -----------------------------------------------------------------------

    def _stratify_confidence(self, score: float) -> Tuple[str, str, bool]:
        """Stratify confidence score into bands."""
        for band_name, band_info in CONFIDENCE_BANDS.items():
            if score >= band_info["min_score"]:
                return band_name, band_info["label"], band_info["requires_caveat"]
        fallback = CONFIDENCE_BANDS["HIGH_RISK"]
        return "HIGH_RISK", fallback["label"], fallback["requires_caveat"]

    # -----------------------------------------------------------------------
    # TIE Component 14: Fact Fragility Scoring
    # -----------------------------------------------------------------------

    def score_fact_fragility(self, facts: List[str], jurisdiction: Optional[str] = None, adr_zone: Optional[str] = None) -> List[Dict[str, Any]]:
        """Score the fragility of factual assertions in ADR context."""
        fragility_indicators: Dict[str, List[str]] = {
            "high_fragility": [
                "oral agreement", "handshake", "verbal", "implied consent", "course of dealing",
                "uncertain", "approximately", "probably", "may have", "believed to be",
                "unsigned", "draft", "preliminary", "tentative", "without prejudice",
            ],
            "medium_fragility": [
                "email", "standard form", "boilerplate", "incorporated by reference",
                "clickwrap", "browsewrap", "check-the-box", "typically", "usually",
                "according to", "reportedly", "appears to", "suggests",
            ],
            "low_fragility": [
                "signed agreement", "notarized", "written consent", "acknowledged",
                "court order", "stipulated", "admitted", "undisputed", "certified",
                "recorded", "filed with court", "docket entry", "exhibit",
            ],
        }

        results: List[Dict[str, Any]] = []
        for fact in facts:
            fact_lower = fact.lower()
            high_count = sum(1 for ind in fragility_indicators["high_fragility"] if ind in fact_lower)
            med_count = sum(1 for ind in fragility_indicators["medium_fragility"] if ind in fact_lower)
            low_count = sum(1 for ind in fragility_indicators["low_fragility"] if ind in fact_lower)

            if high_count > 0:
                fragility_score = min(0.4 + high_count * 0.15, 0.95)
                fragility_level = "HIGH"
            elif med_count > 0 and low_count == 0:
                fragility_score = 0.3 + med_count * 0.1
                fragility_level = "MEDIUM"
            elif low_count > 0:
                fragility_score = max(0.15 - low_count * 0.03, 0.05)
                fragility_level = "LOW"
            else:
                fragility_score = 0.35
                fragility_level = "MODERATE"

            vulnerability_notes: List[str] = []
            if "oral" in fact_lower or "verbal" in fact_lower:
                vulnerability_notes.append("Oral agreements face Statute of Frauds challenges and evidentiary difficulties")
            if "unsigned" in fact_lower or "draft" in fact_lower:
                vulnerability_notes.append("Unsigned or draft documents may not constitute binding agreements to arbitrate")
            if "browsewrap" in fact_lower:
                vulnerability_notes.append("Browsewrap agreements face enforceability challenges (Nguyen v. Barnes & Noble)")
            if "clickwrap" in fact_lower:
                vulnerability_notes.append("Clickwrap generally enforceable if clear and conspicuous (Sgouros v. TransUnion)")
            if any(kw in fact_lower for kw in ["implied", "course of dealing"]):
                vulnerability_notes.append("Implied agreement to arbitrate requires clear course of dealing evidence")
            if not vulnerability_notes:
                vulnerability_notes.append("Standard evidentiary requirements apply; verify documentary support")

            results.append({
                "fact": fact,
                "fragility_score": round(fragility_score, 4),
                "fragility_level": fragility_level,
                "vulnerability_notes": vulnerability_notes,
                "jurisdiction_note": f"Apply {jurisdiction or 'general'} law standards for agreement formation" if jurisdiction else None,
                "adr_zone": adr_zone,
            })

        return results

    # -----------------------------------------------------------------------
    # TIE Component 16: Determinism Hash
    # -----------------------------------------------------------------------

    def _compute_determinism_hash(self, query_hash: str, analysis: Dict[str, Any], confidence: float) -> str:
        """Compute SHA-256 determinism hash for the response."""
        payload = {
            "engine_id": ENGINE_ID,
            "engine_version": ENGINE_VERSION,
            "query_hash": query_hash,
            "confidence": round(confidence, 4),
            "analysis_keys": sorted(analysis.keys()),
            "salt": "LG16_ADR_v2",
        }
        return hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()

    # -----------------------------------------------------------------------
    # TIE Component 1: Three-Layer Response
    # -----------------------------------------------------------------------

    async def process_query(self, request: QueryRequest) -> EngineResponse:
        """Process an ADR law query through the three-layer pipeline.

        Layer 1: Doctrine Cache (fast, pre-compiled answers)
        Layer 2: Semantic Search (TF-IDF indexed search)
        Layer 3: Deep Analysis (multi-doctrine synthesis)
        """
        start = time.monotonic()
        self._query_count += 1

        # TIE Component 6: Semantic Normalization
        normalization = normalize_query(request.query)
        q_hash = compute_query_hash(request.query)

        # TIE Component 8: Telemetry - start trace
        trace = trace_query(request.query, q_hash, request.mode)

        # TIE Component 13: Zoned Analysis
        adr_zone = self._detect_adr_zone(normalization)
        trace.adr_zone = adr_zone
        trace.jurisdiction = request.jurisdiction

        # TIE Component 11: Metrics - record zone
        if adr_zone in ADR_ZONE_METRIC_MAP:
            self._telemetry.record_adr_metric(ADR_ZONE_METRIC_MAP[adr_zone])

        jurisdiction = request.jurisdiction

        layer_used = ResponseLayer.FALLBACK
        analysis: Dict[str, Any] = {}
        citations: List[Dict[str, Any]] = []
        practice_tips: List[str] = []
        confidence_score: float = 0.0

        # --- LAYER 1: Doctrine Cache ---
        step1 = trace.add_step("doctrine_cache_lookup", ResponseLayer.DOCTRINE_CACHE, adr_zone)
        doctrine_result = self._layer1_doctrine_cache(normalization, jurisdiction)
        step1.complete()
        step1.metadata["hits"] = len(doctrine_result.get("blocks", []))

        if doctrine_result.get("blocks"):
            trace.doctrine_hits = len(doctrine_result["blocks"])
            layer_used = ResponseLayer.DOCTRINE_CACHE
            analysis = doctrine_result
            confidence_score = doctrine_result.get("confidence", 0.7)
            citations = doctrine_result.get("citations", [])
            practice_tips = doctrine_result.get("practice_tips", [])

            if request.mode == "fast" and confidence_score >= 0.65:
                return self._build_response(
                    request, trace, layer_used, analysis, citations,
                    practice_tips, confidence_score, q_hash, jurisdiction,
                    normalization, adr_zone, start,
                )

        # --- LAYER 2: Semantic Search ---
        step2 = trace.add_step("semantic_search", ResponseLayer.SEMANTIC_SEARCH, adr_zone)
        search_results = self._layer2_semantic_search(normalization, jurisdiction, request.max_results)
        step2.complete()
        step2.metadata["results"] = len(search_results)
        trace.search_results = len(search_results)

        if search_results:
            layer_used = ResponseLayer.SEMANTIC_SEARCH
            search_analysis = self._synthesize_search_results(search_results, normalization, jurisdiction)
            if not analysis.get("blocks"):
                analysis = search_analysis
                confidence_score = search_analysis.get("confidence", 0.6)
            else:
                analysis["search_supplement"] = search_analysis
                confidence_score = max(confidence_score, search_analysis.get("confidence", 0.5))
            citations.extend(search_analysis.get("citations", []))
            practice_tips.extend(search_analysis.get("practice_tips", []))

            if request.mode in ("fast", "analysis") and confidence_score >= 0.50:
                return self._build_response(
                    request, trace, layer_used, analysis, citations,
                    practice_tips, confidence_score, q_hash, jurisdiction,
                    normalization, adr_zone, start,
                )

        # --- LAYER 3: Deep Analysis ---
        step3 = trace.add_step("deep_analysis", ResponseLayer.DEEP_ANALYSIS, adr_zone)
        deep_result = self._layer3_deep_analysis(request.query, normalization, jurisdiction, adr_zone, analysis)
        step3.complete()

        if deep_result:
            layer_used = ResponseLayer.DEEP_ANALYSIS
            analysis["deep_analysis"] = deep_result
            confidence_score = max(confidence_score, deep_result.get("confidence", 0.45))
            citations.extend(deep_result.get("citations", []))
            practice_tips.extend(deep_result.get("practice_tips", []))

        # Fallback if nothing matched
        if not analysis:
            layer_used = ResponseLayer.FALLBACK
            analysis = self._build_fallback_response(request.query, normalization, jurisdiction, adr_zone)
            confidence_score = 0.35

        return self._build_response(
            request, trace, layer_used, analysis, citations,
            practice_tips, confidence_score, q_hash, jurisdiction,
            normalization, adr_zone, start,
        )

    # -----------------------------------------------------------------------
    # Layer 1: Doctrine Cache
    # -----------------------------------------------------------------------

    def _layer1_doctrine_cache(
        self,
        normalization: NormalizationResult,
        jurisdiction: Optional[str],
    ) -> Dict[str, Any]:
        """Retrieve pre-compiled doctrine blocks matching the query."""
        blocks: List[DoctrineCacheBlock] = []
        citations: List[Dict[str, Any]] = []
        tips: List[str] = []

        for term in normalization.matched_terms:
            canonical = term.get("canonical", "")
            block = self._doctrine_cache.get_by_topic(canonical)
            if block and block not in blocks:
                blocks.append(block)

        for cat in normalization.detected_categories:
            cat_blocks = self._doctrine_cache.get_by_category(cat)
            for block in cat_blocks:
                if block not in blocks:
                    blocks.append(block)

        if not blocks:
            blocks = self._doctrine_cache.search_blocks(normalization.normalized_query.lower(), top_k=3)

        if jurisdiction and blocks:
            filtered = [b for b in blocks if b.jurisdiction in ("federal", "international", jurisdiction)]
            if filtered:
                blocks = filtered

        for block in blocks[:5]:
            for statute in block.key_statutes:
                citations.append({"type": "statute", "text": statute, "authority": "statutory", "source": block.topic})
            for case in block.leading_cases:
                citations.append({"type": "case", "text": case, "authority": "case_law", "source": block.topic})
            tips.extend(block.practice_tips)

        if blocks:
            avg_conf = sum(b.confidence for b in blocks) / len(blocks)
            avg_auth = sum(b.authority_score for b in blocks) / len(blocks)
            confidence = (avg_conf * 0.6) + (avg_auth * 0.3) + (min(len(blocks), 3) / 3.0 * 0.1)
        else:
            confidence = 0.0

        return {
            "blocks": [b.to_dict() for b in blocks[:5]],
            "block_count": len(blocks),
            "citations": citations[:15],
            "practice_tips": list(dict.fromkeys(tips))[:10],
            "confidence": round(min(confidence, 1.0), 4),
            "source": "doctrine_cache",
        }

    # -----------------------------------------------------------------------
    # Layer 2: Semantic Search
    # -----------------------------------------------------------------------

    def _layer2_semantic_search(
        self,
        normalization: NormalizationResult,
        jurisdiction: Optional[str],
        max_results: int,
    ) -> List[SearchResult]:
        """Search over indexed doctrine blocks using TF-IDF."""
        query_tokens = normalization.tokens + [
            t["canonical"] for t in normalization.matched_terms
        ]
        if not query_tokens:
            return []

        adr_zone = self._detect_adr_zone(normalization)
        results = self._search_index.search(
            query_tokens=query_tokens,
            top_k=max_results,
            score_threshold=0.1,
            adr_category_filter=adr_zone if adr_zone else None,
            jurisdiction_filter=jurisdiction,
            authority_weight=0.3,
            recency_weight=0.1,
        )

        if not results and adr_zone:
            results = self._search_index.search(
                query_tokens=query_tokens,
                top_k=max_results,
                score_threshold=0.05,
                authority_weight=0.3,
                recency_weight=0.1,
            )

        return results

    def _synthesize_search_results(
        self,
        results: List[SearchResult],
        normalization: NormalizationResult,
        jurisdiction: Optional[str],
    ) -> Dict[str, Any]:
        """Synthesize search results into structured analysis."""
        citations: List[Dict[str, Any]] = []
        tips: List[str] = []

        for result in results:
            block = self._doctrine_cache.get_by_topic(result.topic)
            if block:
                for statute in block.key_statutes[:2]:
                    citations.append({"type": "statute", "text": statute, "authority": "statutory", "source": result.topic})
                for case in block.leading_cases[:1]:
                    citations.append({"type": "case", "text": case, "authority": "case_law", "source": result.topic})
                tips.extend(block.practice_tips[:2])

        avg_score = sum(r.score for r in results) / max(len(results), 1)

        return {
            "search_results": [r.to_dict() for r in results],
            "result_count": len(results),
            "avg_score": round(avg_score, 4),
            "citations": citations[:10],
            "practice_tips": list(dict.fromkeys(tips))[:5],
            "confidence": round(min(avg_score + 0.15, 1.0), 4),
            "source": "semantic_search",
        }

    # -----------------------------------------------------------------------
    # Layer 3: Deep Analysis (TIE Component 20)
    # -----------------------------------------------------------------------

    def _layer3_deep_analysis(
        self,
        query: str,
        normalization: NormalizationResult,
        jurisdiction: Optional[str],
        adr_zone: str,
        existing_analysis: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Perform deep multi-doctrine analysis for complex ADR queries."""
        deep: Dict[str, Any] = {
            "analysis_type": "deep",
            "adr_zone": adr_zone,
            "jurisdiction": jurisdiction,
            "sub_analyses": [],
            "cross_references": [],
            "risk_factors": [],
            "practice_tips": [],
            "citations": [],
            "confidence": 0.5,
        }

        all_blocks = self._doctrine_cache.search_blocks(query.lower(), top_k=8)
        if jurisdiction:
            filtered = [b for b in all_blocks if b.jurisdiction in ("federal", "international", jurisdiction)]
            if filtered:
                all_blocks = filtered

        for block in all_blocks[:5]:
            sub = {
                "topic": block.topic,
                "category": block.category,
                "key_principle": block.key_statutes[0] if block.key_statutes else "General ADR principle",
                "application_notes": block.analysis_notes[:200] if hasattr(block, "analysis_notes") and block.analysis_notes else block.content_for_search()[:200],
                "authority_score": block.authority_score,
                "confidence": block.confidence,
            }
            deep["sub_analyses"].append(sub)

            for statute in block.key_statutes[:2]:
                deep["citations"].append({"type": "statute", "text": statute, "authority": "statutory", "source": block.topic})
            for case in block.leading_cases[:1]:
                deep["citations"].append({"type": "case", "text": case, "authority": "case_law", "source": block.topic})
            deep["practice_tips"].extend(block.practice_tips[:2])

        # Generate zone-specific risk factors
        zone_risks = self._generate_zone_risks(adr_zone, query, jurisdiction)
        deep["risk_factors"] = zone_risks

        # Cross-references between doctrines
        if len(all_blocks) >= 2:
            for i in range(len(all_blocks[:5])):
                for j in range(i + 1, len(all_blocks[:5])):
                    b1, b2 = all_blocks[i], all_blocks[j]
                    if b1.category == b2.category or set(b1.key_statutes) & set(b2.key_statutes):
                        deep["cross_references"].append({
                            "from_topic": b1.topic,
                            "to_topic": b2.topic,
                            "relationship": "shared_category" if b1.category == b2.category else "shared_statute",
                        })

        if deep["sub_analyses"]:
            avg_conf = sum(s["confidence"] for s in deep["sub_analyses"]) / len(deep["sub_analyses"])
            deep["confidence"] = round(min(avg_conf + 0.05, 1.0), 4)

        deep["practice_tips"] = list(dict.fromkeys(deep["practice_tips"]))[:8]
        deep["citations"] = deep["citations"][:12]

        return deep

    def _generate_zone_risks(self, adr_zone: str, query: str, jurisdiction: Optional[str]) -> List[Dict[str, Any]]:
        """Generate ADR zone-specific risk factors."""
        risks: List[Dict[str, Any]] = []
        query_lower = query.lower()

        zone_risk_map: Dict[str, List[Dict[str, Any]]] = {
            "arbitration": [
                {"risk": "Arbitrability challenge: opposing party may argue claims are not subject to arbitration", "severity": "MEDIUM",
                 "keywords": ["statutory claim", "public injunction", "arbitrability"]},
                {"risk": "Unconscionability defense may invalidate arbitration agreement (especially consumer/employment)", "severity": "HIGH",
                 "keywords": ["unconscionable", "adhesion", "consumer", "employee", "unfair"]},
                {"risk": "FAA preemption issue: state law may conflict with federal arbitration policy", "severity": "MEDIUM",
                 "keywords": ["state law", "preemption", "faa", "at&t v. concepcion"]},
            ],
            "enforcement": [
                {"risk": "Vacatur motion: opposing party may seek to vacate under FAA Section 10", "severity": "HIGH",
                 "keywords": ["vacatur", "vacate", "challenge", "set aside"]},
                {"risk": "Manifest disregard defense (viability varies by circuit post-Hall Street)", "severity": "MEDIUM",
                 "keywords": ["manifest disregard", "hall street", "error of law"]},
                {"risk": "Statute of limitations: 3-month window for vacatur (9 USC 12), 1 year for confirmation (9 USC 9)", "severity": "HIGH",
                 "keywords": ["deadline", "time limit", "limitation", "late", "expired"]},
            ],
            "ny_convention": [
                {"risk": "Public policy defense under Art. V(2)(b) of New York Convention", "severity": "HIGH",
                 "keywords": ["public policy", "enforcement", "foreign award"]},
                {"risk": "Award may be challenged at seat of arbitration (annulment proceeding)", "severity": "MEDIUM",
                 "keywords": ["annul", "set aside", "seat", "country of origin"]},
            ],
            "consumer": [
                {"risk": "Ending Forced Arbitration Act (P.L. 117-90) may void clause for sexual assault/harassment claims", "severity": "HIGH",
                 "keywords": ["sexual assault", "harassment", "efaa", "117-90"]},
                {"risk": "Effective vindication doctrine may prevent enforcement if costs are prohibitive", "severity": "MEDIUM",
                 "keywords": ["cost", "fee", "prohibitive", "vindication"]},
            ],
            "employment": [
                {"risk": "NLRA Section 7 collective action rights (Epic Systems Corp. v. Lewis resolved in favor of enforcement)", "severity": "MEDIUM",
                 "keywords": ["collective", "class", "nlra", "section 7", "epic systems"]},
                {"risk": "State-specific restrictions on employment arbitration (CA, NY, NJ)", "severity": "MEDIUM",
                 "keywords": ["california", "new york", "new jersey", "state restriction"]},
            ],
            "securities": [
                {"risk": "FINRA 6-year eligibility rule may bar older claims", "severity": "HIGH",
                 "keywords": ["6 year", "eligibility", "time bar", "old claim"]},
                {"risk": "Expungement proceedings face heightened scrutiny (FINRA Rule 12805)", "severity": "MEDIUM",
                 "keywords": ["expungement", "brokercheck", "crd"]},
            ],
            "mediation": [
                {"risk": "Confidentiality protections may be incomplete if UMA not enacted in jurisdiction", "severity": "MEDIUM",
                 "keywords": ["confidential", "privilege", "uma", "disclosure"]},
                {"risk": "Mediator may lack immunity in jurisdictions without statutory protection", "severity": "LOW",
                 "keywords": ["immunity", "liability", "mediator"]},
            ],
        }

        zone_risks = zone_risk_map.get(adr_zone, [])
        for risk_item in zone_risks:
            if any(kw in query_lower for kw in risk_item["keywords"]):
                risks.append({"risk": risk_item["risk"], "severity": risk_item["severity"], "zone": adr_zone})

        if not risks:
            for risk_item in zone_risks[:2]:
                risks.append({"risk": risk_item["risk"], "severity": risk_item["severity"], "zone": adr_zone})

        return risks

    # -----------------------------------------------------------------------
    # Fallback Response
    # -----------------------------------------------------------------------

    def _build_fallback_response(
        self,
        query: str,
        normalization: NormalizationResult,
        jurisdiction: Optional[str],
        adr_zone: str,
    ) -> Dict[str, Any]:
        """Build a fallback response when no doctrine blocks match."""
        return {
            "source": "fallback",
            "adr_zone": adr_zone,
            "message": (
                "No specific doctrine blocks matched this query. The analysis below "
                "provides general ADR guidance based on detected context."
            ),
            "detected_terms": [t.get("canonical", "") for t in normalization.matched_terms],
            "detected_categories": normalization.detected_categories,
            "general_guidance": [
                "Review the specific arbitration agreement or ADR clause for governing rules and procedures",
                "Identify the applicable arbitral institution (AAA, JAMS, ICC, UNCITRAL, FINRA, ICSID)",
                "Determine whether FAA, state arbitration act, or international convention governs",
                "Consider unconscionability and enforceability challenges to the arbitration agreement",
                "Evaluate whether the dispute is arbitrable under applicable law",
                f"Consult a licensed attorney in {jurisdiction or 'the relevant jurisdiction'} for specific guidance",
            ],
            "key_statutes": [
                "Federal Arbitration Act, 9 USC 1-16",
                "New York Convention, 9 USC 201-208",
                "Texas Arbitration Act, CPRC Ch. 171",
                "Texas ADR Act, CPRC Ch. 154",
            ],
        }

    # -----------------------------------------------------------------------
    # Response Builder
    # -----------------------------------------------------------------------

    def _build_response(
        self,
        request: QueryRequest,
        trace: QueryTrace,
        layer_used: ResponseLayer,
        analysis: Dict[str, Any],
        citations: List[Dict[str, Any]],
        practice_tips: List[str],
        confidence_score: float,
        query_hash: str,
        jurisdiction: Optional[str],
        normalization: NormalizationResult,
        adr_zone: str,
        start_time: float,
    ) -> EngineResponse:
        """Build the final EngineResponse with all TIE components."""
        # TIE Component 5: Confidence Stratification
        band, label, requires_caveat = self._stratify_confidence(confidence_score)

        # TIE Component 4: Authority Hardening
        if isinstance(analysis.get("message"), str):
            analysis["message"] = self._harden_response(analysis["message"])

        # TIE Component 16: Determinism Hash
        det_hash = self._compute_determinism_hash(query_hash, analysis, confidence_score)

        # Disclaimers
        disclaimers: List[str] = [REQUIRED_DISCLAIMERS["not_legal_advice"]]
        if requires_caveat:
            disclaimers.append(REQUIRED_DISCLAIMERS["fact_dependent"])
        if jurisdiction:
            disclaimers.append(REQUIRED_DISCLAIMERS["jurisdiction_specific"])
        if adr_zone in ("enforcement", "ny_convention"):
            disclaimers.append(REQUIRED_DISCLAIMERS["enforcement_risk"])

        # Deduplicate citations and tips
        seen_citations: Set[str] = set()
        unique_citations: List[Dict[str, Any]] = []
        for cit in citations:
            key = cit.get("text", "")
            if key not in seen_citations:
                seen_citations.add(key)
                unique_citations.append(cit)

        unique_tips = list(dict.fromkeys(practice_tips))

        # Complete trace
        trace.confidence_score = confidence_score
        trace.confidence_band = band
        trace.final_layer = layer_used
        trace.determinism_hash = det_hash
        trace.citations_found = len(unique_citations)
        complete_trace(trace)

        elapsed_ms = (time.monotonic() - start_time) * 1000.0

        return EngineResponse(
            engine_id=ENGINE_ID,
            engine_name=ENGINE_NAME,
            engine_version=ENGINE_VERSION,
            query_hash=query_hash,
            response_mode=request.mode,
            confidence_score=round(confidence_score, 4),
            confidence_band=band,
            confidence_label=label,
            requires_caveat=requires_caveat,
            layer_used=layer_used.value,
            jurisdiction=jurisdiction,
            adr_zone=adr_zone,
            analysis=analysis,
            citations=unique_citations[:15] if request.include_citations else [],
            disclaimers=disclaimers,
            practice_tips=unique_tips[:10] if request.include_practice_tips else [],
            determinism_hash=det_hash,
            trace_id=trace.trace_id,
            processing_time_ms=round(elapsed_ms, 3),
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

    # -----------------------------------------------------------------------
    # TIE Component 19: Multi-Doctrine Decomposition
    # -----------------------------------------------------------------------

    async def multi_doctrine_decompose(self, request: MultiDoctrineRequest) -> Dict[str, Any]:
        """Decompose a complex query into multiple doctrine analyses."""
        normalization = normalize_query(request.query)
        q_hash = compute_query_hash(request.query)
        adr_zone = self._detect_adr_zone(normalization)

        all_blocks = self._doctrine_cache.search_blocks(request.query.lower(), top_k=request.max_doctrines * 2)
        if request.jurisdiction:
            filtered = [b for b in all_blocks if b.jurisdiction in ("federal", "international", request.jurisdiction)]
            if filtered:
                all_blocks = filtered

        decomposed: List[Dict[str, Any]] = []
        for block in all_blocks[:request.max_doctrines]:
            sub_result = {
                "topic": block.topic,
                "category": block.category,
                "subcategory": block.subcategory,
                "confidence": block.confidence,
                "authority_score": block.authority_score,
                "key_statutes": block.key_statutes[:3],
                "leading_cases": block.leading_cases[:2],
                "practice_tips": block.practice_tips[:3],
                "content_summary": block.content_for_search()[:300],
            }
            decomposed.append(sub_result)

        avg_conf = sum(d["confidence"] for d in decomposed) / max(len(decomposed), 1) if decomposed else 0.35

        return {
            "engine_id": ENGINE_ID,
            "query_hash": q_hash,
            "adr_zone": adr_zone,
            "decomposition_count": len(decomposed),
            "doctrines": decomposed,
            "confidence": round(avg_conf, 4),
            "determinism_hash": self._compute_determinism_hash(q_hash, {"doctrines": len(decomposed)}, avg_conf),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    # -----------------------------------------------------------------------
    # Clause Review
    # -----------------------------------------------------------------------

    async def review_clause(self, request: ClauseReviewRequest) -> Dict[str, Any]:
        """Review an arbitration clause for completeness and enforceability."""
        self._telemetry.record_adr_metric(ADRMetricType.CLAUSE_REVIEW)
        context = {
            "consumer": request.consumer,
            "employment": request.employment,
            "international": request.international,
        }
        result = self._clause_validator.validate_clause(request.clause_text, context)
        q_hash = compute_query_hash(request.clause_text)

        self._audit.append("clause_review", {
            "query_hash": q_hash,
            "overall_valid": result.overall_valid,
            "completeness": result.completeness_score,
            "unconscionability_risks": len(result.unconscionability_risks),
            "pathological_issues": len(result.pathological_issues),
        })

        return {
            "engine_id": ENGINE_ID,
            "engine_version": ENGINE_VERSION,
            "query_hash": q_hash,
            "validation": result.to_dict(),
            "disclaimers": [REQUIRED_DISCLAIMERS["not_legal_advice"], REQUIRED_DISCLAIMERS["jurisdiction_specific"]],
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    # -----------------------------------------------------------------------
    # Process Design
    # -----------------------------------------------------------------------

    async def design_process(self, request: ProcessDesignRequest) -> Dict[str, Any]:
        """Design a dispute resolution process based on dispute characteristics."""
        self._telemetry.record_adr_metric(ADRMetricType.PROCESS_DESIGN)
        dispute_facts = {
            "dispute_type": request.dispute_type,
            "amount": request.amount,
            "complexity": request.complexity,
            "ongoing_relationship": request.ongoing_relationship,
            "confidentiality_needed": request.confidentiality_needed,
            "speed_priority": request.speed_priority,
            "international": request.international,
            "number_of_parties": request.number_of_parties,
        }
        result = self._dispute_advisor.recommend(dispute_facts)
        q_hash = compute_query_hash(json.dumps(dispute_facts, sort_keys=True))

        self._audit.append("process_design", {
            "query_hash": q_hash,
            "recommended_process": result.recommended_process,
            "recommended_institution": result.recommended_institution,
        })

        return {
            "engine_id": ENGINE_ID,
            "engine_version": ENGINE_VERSION,
            "query_hash": q_hash,
            "recommendation": result.to_dict(),
            "disclaimers": [REQUIRED_DISCLAIMERS["not_legal_advice"]],
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    # -----------------------------------------------------------------------
    # Award Enforceability
    # -----------------------------------------------------------------------

    async def check_award_enforceability(self, request: AwardEnforceabilityRequest) -> Dict[str, Any]:
        """Check enforceability of an arbitration award."""
        self._telemetry.record_adr_metric(ADRMetricType.AWARD_REVIEW)
        award_facts = {
            "description": request.description,
            "international": request.international,
            "seat": request.seat,
            "enforcement_country": request.enforcement_country,
        }
        result = self._enforceability_checker.check_enforceability(award_facts)
        q_hash = compute_query_hash(request.description)

        self._audit.append("award_enforceability", {
            "query_hash": q_hash,
            "enforceable": result.enforceable,
            "risk_assessment": result.risk_assessment,
            "vacatur_grounds": len(result.vacatur_grounds_present),
            "nyc_defenses": len(result.new_york_convention_defenses),
        })

        return {
            "engine_id": ENGINE_ID,
            "engine_version": ENGINE_VERSION,
            "query_hash": q_hash,
            "enforceability": result.to_dict(),
            "disclaimers": [REQUIRED_DISCLAIMERS["not_legal_advice"], REQUIRED_DISCLAIMERS["enforcement_risk"]],
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    # -----------------------------------------------------------------------
    # Dispute Classification
    # -----------------------------------------------------------------------

    async def classify_dispute(self, request: DisputeClassifyRequest) -> Dict[str, Any]:
        """Classify a dispute and recommend appropriate ADR mechanisms."""
        self._telemetry.record_adr_metric(ADRMetricType.DISPUTE_CLASSIFICATION)
        normalization = normalize_query(request.description)
        adr_zone = self._detect_adr_zone(normalization)
        q_hash = compute_query_hash(request.description)

        description_lower = request.description.lower()
        industry = (request.industry or "").lower()

        dispute_categories: List[Dict[str, Any]] = []
        category_keywords: Dict[str, List[str]] = {
            "commercial_contract": ["contract", "breach", "warranty", "payment", "delivery", "performance"],
            "employment": ["employment", "termination", "discrimination", "harassment", "wage", "overtime"],
            "construction": ["construction", "defect", "delay", "change order", "contractor", "subcontractor"],
            "securities": ["securities", "investment", "broker", "fraud", "misrepresentation", "suitability"],
            "consumer": ["consumer", "product", "service", "warranty", "refund", "deceptive"],
            "real_estate": ["real estate", "property", "lease", "landlord", "tenant", "boundary"],
            "oil_gas": ["oil", "gas", "mineral", "royalty", "joa", "operating agreement", "wellbore"],
            "ip": ["patent", "trademark", "copyright", "trade secret", "licensing", "infringement"],
            "international_trade": ["international", "cross-border", "trade", "customs", "export", "import"],
            "family": ["divorce", "custody", "family", "matrimonial", "prenuptial"],
            "insurance": ["insurance", "coverage", "claim", "policyholder", "underinsured", "bad faith"],
            "healthcare": ["healthcare", "medical", "hospital", "malpractice", "hipaa"],
        }

        for category, keywords in category_keywords.items():
            score = sum(1 for kw in keywords if kw in description_lower or kw in industry)
            if score > 0:
                dispute_categories.append({"category": category, "score": score, "confidence": min(score * 0.2 + 0.3, 0.95)})

        dispute_categories.sort(key=lambda x: x["score"], reverse=True)
        primary_category = dispute_categories[0]["category"] if dispute_categories else "commercial_contract"

        complexity_indicators = ["multi-party", "international", "regulatory", "class action", "injunctive",
                                 "complex", "technical", "expert", "large", "millions"]
        complexity_score = sum(1 for ind in complexity_indicators if ind in description_lower)
        complexity = "high" if complexity_score >= 3 else "medium" if complexity_score >= 1 else "low"

        recommended_mechanisms: List[Dict[str, str]] = []
        if primary_category in ("family", "employment") or "relationship" in description_lower:
            recommended_mechanisms.append({"mechanism": "Mediation", "rationale": "Preserves relationships and allows creative solutions"})
            recommended_mechanisms.append({"mechanism": "Med-Arb", "rationale": "Provides binding backstop if mediation fails"})
        if primary_category == "construction":
            recommended_mechanisms.append({"mechanism": "Dispute Review Board", "rationale": "Real-time resolution during project performance"})
        if primary_category in ("securities",):
            recommended_mechanisms.append({"mechanism": "FINRA Arbitration", "rationale": "Mandatory for customer-broker disputes"})
        recommended_mechanisms.append({"mechanism": "Arbitration", "rationale": "Provides final, binding resolution with expert decision-maker"})

        self._audit.append("dispute_classify", {
            "query_hash": q_hash,
            "primary_category": primary_category,
            "complexity": complexity,
            "adr_zone": adr_zone,
        })

        return {
            "engine_id": ENGINE_ID,
            "engine_version": ENGINE_VERSION,
            "query_hash": q_hash,
            "classification": {
                "primary_category": primary_category,
                "all_categories": dispute_categories[:5],
                "adr_zone": adr_zone,
                "complexity": complexity,
                "recommended_mechanisms": recommended_mechanisms,
                "parties": request.parties or [],
                "jurisdiction": request.jurisdiction,
            },
            "disclaimers": [REQUIRED_DISCLAIMERS["not_legal_advice"]],
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    # -----------------------------------------------------------------------
    # Health Endpoint Data (TIE Component 12)
    # -----------------------------------------------------------------------

    def get_health(self) -> Dict[str, Any]:
        """Return engine health status."""
        return {
            "status": "healthy",
            "engine_id": ENGINE_ID,
            "engine_name": ENGINE_NAME,
            "engine_version": ENGINE_VERSION,
            "port": ENGINE_PORT,
            "authority": ENGINE_AUTHORITY,
            "mode": ENGINE_MODE,
            "tier": ENGINE_TIER,
            "boot_time": self._boot_time,
            "uptime_seconds": round(time.monotonic(), 2),
            "query_count": self._query_count,
            "doctrine_count": len(DOCTRINE_BLOCKS),
            "search_index_docs": self._search_index.document_count,
            "search_index_vocab": self._search_index.vocabulary_size,
            "semantic_version": self._semantic_version,
            "tie_components": 20,
            "zones": list(ADR_ZONE_METRIC_MAP.keys()),
            "doctrine_cache_hash": get_doctrine_cache_hash(),
            "semantic_map_hash": get_semantic_map_hash(),
            "audit_entries": self._audit.entry_count,
            "drift_summary": self._telemetry.drift_watcher.get_drift_summary(),
            "metrics_summary": self._telemetry.get_metrics_summary(),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    # -----------------------------------------------------------------------
    # Drift Signal Registration
    # -----------------------------------------------------------------------

    def register_drift_signal(self, signal: DriftSignal) -> Dict[str, Any]:
        """Register a doctrine drift signal."""
        severity = DriftSeverity.MEDIUM
        if abs(signal.confidence_impact) >= 0.3:
            severity = DriftSeverity.CRITICAL
        elif abs(signal.confidence_impact) >= 0.15:
            severity = DriftSeverity.HIGH

        result = self._telemetry.record_drift_signal(
            signal_type=signal.signal_type,
            topic=signal.topic,
            description=signal.description,
            severity=severity,
            source=signal.source,
            confidence_impact=signal.confidence_impact,
        )
        return result

    # -----------------------------------------------------------------------
    # Coverage Map (TIE Component 10)
    # -----------------------------------------------------------------------

    def get_coverage_map(self) -> Dict[str, Any]:
        """Return doctrine coverage map."""
        raw_map = get_coverage_map()
        categories = get_all_doctrine_categories()
        topics = get_all_doctrine_topics()
        stats = get_doctrine_cache_stats()

        return {
            "engine_id": ENGINE_ID,
            "coverage_map": raw_map,
            "categories": categories,
            "topics": topics,
            "stats": stats,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    # -----------------------------------------------------------------------
    # Fact Fragility Endpoint
    # -----------------------------------------------------------------------

    async def score_facts(self, request: FactFragilityRequest) -> Dict[str, Any]:
        """Score fact fragility for ADR context."""
        results = self.score_fact_fragility(request.facts, request.jurisdiction, request.adr_zone)
        avg_fragility = sum(r["fragility_score"] for r in results) / max(len(results), 1)

        return {
            "engine_id": ENGINE_ID,
            "engine_version": ENGINE_VERSION,
            "fact_scores": results,
            "average_fragility": round(avg_fragility, 4),
            "overall_level": "HIGH" if avg_fragility > 0.6 else "MEDIUM" if avg_fragility > 0.3 else "LOW",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


# ============================================================================
# FASTAPI APPLICATION (TIE Component 17)
# ============================================================================

_engine: Optional[ADREngine] = None


def _load_config() -> Dict[str, Any]:
    """Load engine configuration from config.json."""
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as fh:
                return json.load(fh)
        except (json.JSONDecodeError, OSError) as exc:
            logger.warning(f"Failed to load config: {exc}")
    return {"engine_id": ENGINE_ID, "port": ENGINE_PORT, "authority_level": ENGINE_AUTHORITY}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    global _engine
    # TIE Component 18: Loguru Logging
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logger.add(
        LOG_DIR / "lg16_adr_{time}.log",
        rotation="50 MB",
        retention="30 days",
        compression="gz",
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level:<8} | {name}:{function}:{line} | {message}",
    )
    config = _load_config()
    _engine = ADREngine(config)
    logger.info(f"LG16 ADR Engine started on port {ENGINE_PORT}")
    yield
    logger.info("LG16 ADR Engine shutting down")


app = FastAPI(
    title="LG16 ADR Engine",
    description="Alternative Dispute Resolution analysis engine with 20 TIE components",
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


def _get_engine() -> ADREngine:
    """Get the initialized engine instance."""
    if _engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    return _engine


# ============================================================================
# ENDPOINTS
# ============================================================================

@app.post("/query", response_model=EngineResponse)
async def query_endpoint(request: QueryRequest) -> EngineResponse:
    """Process an ADR law query through the three-layer pipeline."""
    engine = _get_engine()
    return await engine.process_query(request)


@app.get("/health")
async def health_endpoint() -> Dict[str, Any]:
    """Return engine health status (TIE Component 12)."""
    engine = _get_engine()
    return engine.get_health()


@app.post("/clause-review")
async def clause_review_endpoint(request: ClauseReviewRequest) -> Dict[str, Any]:
    """Review an arbitration clause for completeness and enforceability."""
    engine = _get_engine()
    return await engine.review_clause(request)


@app.post("/process-design")
async def process_design_endpoint(request: ProcessDesignRequest) -> Dict[str, Any]:
    """Design a dispute resolution process based on dispute characteristics."""
    engine = _get_engine()
    return await engine.design_process(request)


@app.post("/award-enforceability")
async def award_enforceability_endpoint(request: AwardEnforceabilityRequest) -> Dict[str, Any]:
    """Check enforceability of an arbitration award."""
    engine = _get_engine()
    return await engine.check_award_enforceability(request)


@app.post("/dispute-classify")
async def dispute_classify_endpoint(request: DisputeClassifyRequest) -> Dict[str, Any]:
    """Classify a dispute and recommend appropriate ADR mechanisms."""
    engine = _get_engine()
    return await engine.classify_dispute(request)


@app.post("/fact-fragility")
async def fact_fragility_endpoint(request: FactFragilityRequest) -> Dict[str, Any]:
    """Score fact fragility for ADR context (TIE Component 14)."""
    engine = _get_engine()
    return await engine.score_facts(request)


@app.post("/multi-doctrine")
async def multi_doctrine_endpoint(request: MultiDoctrineRequest) -> Dict[str, Any]:
    """Decompose a complex query into multiple doctrine analyses (TIE Component 19)."""
    engine = _get_engine()
    return await engine.multi_doctrine_decompose(request)


@app.post("/deep-analysis")
async def deep_analysis_endpoint(request: DeepAnalysisRequest) -> Dict[str, Any]:
    """Perform deep multi-doctrine analysis (TIE Component 20)."""
    engine = _get_engine()
    normalization = normalize_query(request.query)
    q_hash = compute_query_hash(request.query)
    adr_zone = engine._detect_adr_zone(normalization)

    deep_result = engine._layer3_deep_analysis(
        request.query, normalization, request.jurisdiction, adr_zone, {},
    )

    if request.include_risk_assessment:
        deep_result["zone_risks"] = engine._generate_zone_risks(adr_zone, request.query, request.jurisdiction)

    if request.include_alternatives:
        dispute_facts = {
            "dispute_type": adr_zone,
            "amount": 0,
            "complexity": "high",
            "ongoing_relationship": False,
            "confidentiality_needed": True,
            "speed_priority": "medium",
            "international": "international" in request.query.lower(),
            "number_of_parties": 2,
        }
        advisory = engine._dispute_advisor.recommend(dispute_facts)
        deep_result["alternative_processes"] = advisory.to_dict()

    det_hash = engine._compute_determinism_hash(q_hash, deep_result, deep_result.get("confidence", 0.5))

    return {
        "engine_id": ENGINE_ID,
        "engine_version": ENGINE_VERSION,
        "query_hash": q_hash,
        "adr_zone": adr_zone,
        "deep_analysis": deep_result,
        "determinism_hash": det_hash,
        "disclaimers": [REQUIRED_DISCLAIMERS["not_legal_advice"], REQUIRED_DISCLAIMERS["fact_dependent"]],
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.post("/drift-signal")
async def drift_signal_endpoint(signal: DriftSignal) -> Dict[str, Any]:
    """Register a doctrine drift signal (TIE Component 9)."""
    engine = _get_engine()
    result = engine.register_drift_signal(signal)
    return {"status": "registered", "signal": result}


@app.get("/coverage-map")
async def coverage_map_endpoint() -> Dict[str, Any]:
    """Return doctrine coverage map (TIE Component 10)."""
    engine = _get_engine()
    return engine.get_coverage_map()


@app.get("/metrics")
async def metrics_endpoint() -> Dict[str, Any]:
    """Return engine metrics (TIE Component 11)."""
    engine = _get_engine()
    return engine._telemetry.get_metrics_summary()


@app.get("/audit/verify")
async def audit_verify_endpoint() -> Dict[str, Any]:
    """Verify audit trail integrity (TIE Component 15)."""
    engine = _get_engine()
    return engine._audit.verify_chain()


@app.get("/audit/recent")
async def audit_recent_endpoint(limit: int = Query(50, ge=1, le=500)) -> Dict[str, Any]:
    """Return recent audit entries."""
    engine = _get_engine()
    entries = engine._audit.get_recent_entries(limit)
    return {"entries": entries, "count": len(entries)}


@app.get("/drift/active")
async def drift_active_endpoint() -> Dict[str, Any]:
    """Return active drift signals."""
    engine = _get_engine()
    signals = engine._telemetry.drift_watcher.get_active_signals()
    return {"signals": signals, "count": len(signals)}


@app.get("/doctrine/integrity")
async def doctrine_integrity_endpoint() -> Dict[str, Any]:
    """Verify doctrine cache integrity."""
    integrity = verify_doctrine_integrity()
    return {
        "engine_id": ENGINE_ID,
        "integrity": integrity,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/doctrine/stale")
async def doctrine_stale_endpoint() -> Dict[str, Any]:
    """Return stale doctrine topics."""
    stale = get_stale_doctrines()
    return {
        "engine_id": ENGINE_ID,
        "stale_doctrines": stale,
        "count": len(stale),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/semantic/integrity")
async def semantic_integrity_endpoint() -> Dict[str, Any]:
    """Verify semantic dictionary integrity."""
    integrity = verify_dictionary_integrity()
    return {
        "engine_id": ENGINE_ID,
        "integrity": integrity,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "engine:app",
        host=ENGINE_HOST,
        port=ENGINE_PORT,
        reload=False,
        log_level="info",
    )
