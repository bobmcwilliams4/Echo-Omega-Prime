"""
LG14 Healthcare Law Engine - Main FastAPI Engine
====================================================
Production-grade healthcare law analysis engine implementing all 20 TIE
components for HIPAA privacy/security/breach notification, HITECH Act,
ACA compliance, Medicare/Medicaid fraud (FCA, AKS, Stark), medical
malpractice, informed consent, patient rights, clinical trials/IRB, FDA
drug/device regulation, MHPAEA, EMTALA, telemedicine, licensing,
healthcare M&A, 501(r), pharmacy law, 42 CFR Part 2, public health
emergency law, and healthcare data interoperability analysis.

TIE-20 Components:
    1.  three_layer_response
    2.  response_modes (fast, analysis, memo, compliance_audit, regulatory_review)
    3.  doctrine_cache
    4.  authority_hardening
    5.  confidence_stratification
    6.  semantic_normalization
    7.  vector_search_tfidf (TF-IDF inverted index implementation)
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

Port: 8404
Engine: LG14 Healthcare Law
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
    DoctrineSearchIndex,
    FDARegulationSearcher,
    FDARegulationResult,
    FraudRiskResult,
    HIPAAComplianceChecker,
    HIPAAComplianceResult,
    MalpracticeAnalyzer,
    MalpracticeAnalysisResult,
    MedicareFraudDetector,
    SearchResult,
    compute_query_hash,
    get_fda_searcher,
    get_fraud_detector,
    get_hipaa_checker,
    get_malpractice_analyzer,
    get_search_index,
)
from semantic import (
    HIPAAAnalyzer,
    NormalizationResult,
    StarkLawAnalyzer,
    get_jurisdiction_map,
    get_semantic_map,
    get_semantic_map_hash,
    get_semantic_map_version,
    normalize_query,
    verify_dictionary_integrity,
)
from telemetry import (
    AuditTrail,
    CitationLookupType,
    ErrorDomain,
    HealthcareMetricType,
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

ENGINE_ID: str = "LG14"
ENGINE_NAME: str = "Healthcare Law Engine"
ENGINE_VERSION: str = "2.0.0"
ENGINE_PORT: int = 8404
ENGINE_HOST: str = "0.0.0.0"
ENGINE_AUTHORITY: float = 5.0
ENGINE_TIER: str = "LEGAL"
ENGINE_MODE: str = "EF"

CONFIG_PATH: Path = Path(__file__).parent / "config.json"
LOG_DIR: Path = Path(__file__).parent / "logs"
AUDIT_LOG_PATH: Path = LOG_DIR / "audit_trail.jsonl"
DRIFT_REGISTRY_PATH: Path = Path(__file__).parent / "doctrine_drift_registry.json"

BANNED_PHRASES: List[str] = [
    "This is definitely HIPAA compliant",
    "There is absolutely no Stark Law violation",
    "You will certainly win this malpractice case",
    "The Anti-Kickback Statute does not apply here",
    "This arrangement is guaranteed to be legal",
    "There is zero enforcement risk",
    "OCR will definitely not investigate",
    "The False Claims Act cannot reach this conduct",
    "EMTALA does not apply to this facility",
    "This is absolutely a safe harbor arrangement",
    "No court would find an FCA violation",
    "Your HIPAA breach does not require notification",
    "This clinical trial is fully compliant",
    "The FDA will certainly approve this device",
]

REQUIRED_DISCLAIMERS: Dict[str, str] = {
    "not_legal_advice": (
        "This analysis is for informational purposes only and does not "
        "constitute legal advice. Consult a licensed healthcare attorney "
        "for specific legal guidance."
    ),
    "jurisdiction_specific": (
        "Healthcare law varies significantly by state and involves complex "
        "federal-state interactions. This analysis may not apply in all jurisdictions."
    ),
    "fact_dependent": (
        "Healthcare law outcomes depend heavily on specific facts, regulatory "
        "interpretation, and enforcement priorities. This analysis is based "
        "on the information provided."
    ),
    "regulatory_risk": (
        "Healthcare regulatory enforcement is active and evolving. Government "
        "interpretations may differ from the analysis presented. Consider "
        "obtaining regulatory counsel."
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
    "oig_advisory_opinion": 75,
    "cms_guidance": 75,
    "fda_guidance": 70,
    "hhs_regulation": 80,
    "ocr_guidance": 70,
    "compliance_guidance": 60,
    "treatise": 40,
    "law_review": 30,
    "cms_manual": 65,
    "restatement_torts": 50,
}

CONFIDENCE_BANDS: Dict[str, Dict[str, Any]] = {
    "DEFENSIBLE": {"min_score": 0.85, "label": "Position is well-supported by established healthcare law and precedent", "requires_caveat": False},
    "SUPPORTABLE": {"min_score": 0.65, "label": "Position has reasonable support but some uncertainty in application", "requires_caveat": True},
    "DISCLOSURE": {"min_score": 0.50, "label": "Position requires disclosure of contrary authority or regulatory risk", "requires_caveat": True},
    "HIGH_RISK": {"min_score": 0.0, "label": "Position faces significant adverse authority or active enforcement risk", "requires_caveat": True},
}

HC_CATEGORY_METRIC_MAP: Dict[str, HealthcareMetricType] = {
    "hipaa": HealthcareMetricType.HIPAA_QUERY,
    "fraud_abuse": HealthcareMetricType.FRAUD_ABUSE_QUERY,
    "malpractice": HealthcareMetricType.MALPRACTICE_QUERY,
    "fda": HealthcareMetricType.FDA_QUERY,
    "emtala": HealthcareMetricType.EMTALA_QUERY,
    "aca": HealthcareMetricType.ACA_QUERY,
    "telemedicine": HealthcareMetricType.TELEMEDICINE_QUERY,
    "clinical_trials": HealthcareMetricType.CLINICAL_TRIALS_QUERY,
    "parity": HealthcareMetricType.PARITY_QUERY,
    "interoperability": HealthcareMetricType.INTEROPERABILITY_QUERY,
    "pharmacy": HealthcareMetricType.PHARMACY_QUERY,
    "public_health": HealthcareMetricType.PUBLIC_HEALTH_QUERY,
    "tax_exempt": HealthcareMetricType.TAX_EXEMPT_QUERY,
    "licensing": HealthcareMetricType.LICENSING_QUERY,
    "compliance": HealthcareMetricType.COMPLIANCE_CHECK,
    "regulatory": HealthcareMetricType.REGULATORY_REVIEW,
}


# ============================================================================
# PYDANTIC REQUEST/RESPONSE MODELS
# ============================================================================

class QueryRequest(BaseModel):
    """Incoming query request."""
    query: str = Field(..., min_length=3, max_length=5000, description="The healthcare law question")
    mode: str = Field("fast", description="Response mode: fast, analysis, memo, compliance_audit, regulatory_review")
    jurisdiction: Optional[str] = Field(None, description="Jurisdiction filter (e.g. TX, CA, NY)")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context for analysis")
    include_citations: bool = Field(True, description="Include statutory and case citations")
    include_practice_tips: bool = Field(False, description="Include practice tips in response")
    max_results: int = Field(5, ge=1, le=20, description="Maximum doctrine results to return")

    @field_validator("mode")
    @classmethod
    def validate_mode(cls, v: str) -> str:
        valid_modes = {"fast", "analysis", "memo", "compliance_audit", "regulatory_review"}
        if v not in valid_modes:
            raise ValueError(f"Invalid mode '{v}'. Must be one of: {valid_modes}")
        return v


class HIPAAComplianceRequest(BaseModel):
    """HIPAA compliance check request."""
    answers: Dict[str, bool] = Field(..., description="Compliance requirement answers (requirement_id -> met)")


class MalpracticeRequest(BaseModel):
    """Malpractice analysis request."""
    description: str = Field(..., min_length=10, description="Description of the malpractice scenario")
    jurisdiction: Optional[str] = Field(None, description="State jurisdiction")


class FDAPathwayRequest(BaseModel):
    """FDA regulatory pathway request."""
    product_type: str = Field(..., description="Product type: drug, biologic, device")
    product_description: str = Field(..., min_length=5, description="Description of the product")

    @field_validator("product_type")
    @classmethod
    def validate_product_type(cls, v: str) -> str:
        valid = {"drug", "biologic", "device"}
        if v not in valid:
            raise ValueError(f"Invalid product_type '{v}'. Must be one of: {valid}")
        return v


class FraudRiskRequest(BaseModel):
    """Fraud risk assessment request."""
    description: str = Field(..., min_length=10, description="Description of the arrangement to assess")


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
    hc_category: Optional[str] = Field(None, description="Healthcare category context")


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
    hc_category: Optional[str]
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

class HealthcareLawEngine:
    """Core engine implementing all 20 TIE components for healthcare law.

    Orchestrates doctrine cache, semantic normalization, search,
    telemetry, authority hardening, confidence stratification,
    drift watching, and deep analysis for healthcare law queries.
    """

    def __init__(self, config: Dict[str, Any]) -> None:
        self._config: Dict[str, Any] = config
        self._engine_id: str = config.get("engine_id", ENGINE_ID)
        self._port: int = config.get("port", ENGINE_PORT)
        self._authority: float = config.get("engine_authority", ENGINE_AUTHORITY)

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
        self._hipaa_checker: HIPAAComplianceChecker = get_hipaa_checker()
        self._malpractice_analyzer: MalpracticeAnalyzer = get_malpractice_analyzer()
        self._fda_searcher: FDARegulationSearcher = get_fda_searcher()
        self._fraud_detector: MedicareFraudDetector = get_fraud_detector()
        self._hipaa_analyzer: HIPAAAnalyzer = HIPAAAnalyzer()
        self._stark_analyzer: StarkLawAnalyzer = StarkLawAnalyzer()

        # TIE Component 9: Doctrine Drift Watcher
        self._drift_registry: Dict[str, Any] = self._load_drift_registry()

        # TIE Component 15: Audit Trail
        self._audit: AuditTrail = self._telemetry._audit

        # Index doctrine blocks for search
        self._index_doctrines()

        self._boot_time: str = datetime.now(timezone.utc).isoformat()
        self._query_count: int = 0

        logger.info(
            f"HealthcareLawEngine initialized | id={self._engine_id} | "
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
                hc_category=block.category,
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
    # TIE Component 1: Three-Layer Response
    # -----------------------------------------------------------------------

    async def process_query(self, request: QueryRequest) -> EngineResponse:
        """Process a healthcare law query through the three-layer pipeline.

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
        trace.hc_category = normalization.detected_hc_type
        trace.jurisdiction = request.jurisdiction or normalization.detected_jurisdiction

        # TIE Component 11: Metrics - record category
        if normalization.detected_hc_type and normalization.detected_hc_type in HC_CATEGORY_METRIC_MAP:
            self._telemetry.record_hc_metric(HC_CATEGORY_METRIC_MAP[normalization.detected_hc_type])

        jurisdiction = request.jurisdiction or normalization.detected_jurisdiction

        layer_used = ResponseLayer.FALLBACK
        analysis: Dict[str, Any] = {}
        citations: List[Dict[str, Any]] = []
        practice_tips: List[str] = []
        confidence_score: float = 0.0

        # --- LAYER 1: Doctrine Cache ---
        step1 = trace.add_step("doctrine_cache_lookup", ResponseLayer.DOCTRINE_CACHE, normalization.detected_hc_type)
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
                    normalization, start,
                )

        # --- LAYER 2: Semantic Search ---
        step2 = trace.add_step("semantic_search", ResponseLayer.SEMANTIC_SEARCH, normalization.detected_hc_type)
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
                    normalization, start,
                )

        # --- LAYER 3: Deep Analysis ---
        step3 = trace.add_step("deep_analysis", ResponseLayer.DEEP_ANALYSIS, normalization.detected_hc_type)
        deep_result = self._layer3_deep_analysis(request.query, normalization, jurisdiction, analysis)
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
            analysis = self._build_fallback_response(request.query, normalization, jurisdiction)
            confidence_score = 0.35

        return self._build_response(
            request, trace, layer_used, analysis, citations,
            practice_tips, confidence_score, q_hash, jurisdiction,
            normalization, start,
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
            filtered = [b for b in blocks if b.jurisdiction in ("federal", jurisdiction)]
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

        hc_cat = normalization.detected_hc_type
        results = self._search_index.search(
            query_tokens=query_tokens,
            top_k=max_results,
            score_threshold=0.1,
            hc_category_filter=hc_cat if hc_cat else None,
            jurisdiction_filter=jurisdiction,
            authority_weight=0.3,
            recency_weight=0.1,
        )

        if not results and hc_cat:
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
        """Synthesize search results into a structured analysis."""
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
        existing_analysis: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Multi-doctrine synthesis for complex queries."""
        categories = normalization.detected_categories
        if len(categories) < 2 and existing_analysis.get("blocks"):
            return {}

        all_blocks: List[DoctrineCacheBlock] = []
        for cat in categories:
            all_blocks.extend(self._doctrine_cache.get_by_category(cat))

        if not all_blocks:
            all_blocks = self._doctrine_cache.search_blocks(query.lower(), top_k=5)

        if not all_blocks:
            return {}

        cross_refs: List[Dict[str, Any]] = []
        for i, block_a in enumerate(all_blocks[:5]):
            for block_b in all_blocks[i + 1:5]:
                overlap = set(block_a.related_topics) & {block_b.topic}
                overlap |= set(block_b.related_topics) & {block_a.topic}
                if overlap or block_a.category != block_b.category:
                    cross_refs.append({
                        "topic_a": block_a.topic,
                        "topic_b": block_b.topic,
                        "relationship": "cross_doctrine" if not overlap else "related",
                        "overlapping_topics": list(overlap),
                    })

        citations: List[Dict[str, Any]] = []
        tips: List[str] = []
        for block in all_blocks[:5]:
            for statute in block.key_statutes[:2]:
                citations.append({"type": "statute", "text": statute, "source": block.topic})
            for case in block.leading_cases[:1]:
                citations.append({"type": "case", "text": case, "source": block.topic})
            tips.extend(block.practice_tips[:2])

        risk_factors: List[str] = []
        for block in all_blocks[:5]:
            risk_factors.extend(block.risk_factors)

        avg_conf = sum(b.confidence for b in all_blocks[:5]) / max(len(all_blocks[:5]), 1)

        return {
            "doctrines_analyzed": [b.topic for b in all_blocks[:5]],
            "categories_involved": list(set(b.category for b in all_blocks[:5])),
            "cross_references": cross_refs,
            "risk_factors": list(dict.fromkeys(risk_factors))[:10],
            "citations": citations[:10],
            "practice_tips": list(dict.fromkeys(tips))[:5],
            "confidence": round(min(avg_conf, 0.95), 4),
            "synthesis_note": f"Deep analysis across {len(set(b.category for b in all_blocks[:5]))} categories with {len(cross_refs)} cross-references identified.",
            "source": "deep_analysis",
        }

    # -----------------------------------------------------------------------
    # Fallback response
    # -----------------------------------------------------------------------

    def _build_fallback_response(
        self,
        query: str,
        normalization: NormalizationResult,
        jurisdiction: Optional[str],
    ) -> Dict[str, Any]:
        """Build a fallback response when no doctrine matches."""
        return {
            "message": "No direct doctrine match found for this query. The question may require specialized analysis beyond the cached doctrine library.",
            "suggestions": [
                "Try rephrasing the query using standard healthcare law terminology",
                "Specify a jurisdiction for more targeted results",
                "Break complex questions into individual sub-questions",
                "Use specific terms like HIPAA, Stark Law, AKS, FCA, EMTALA, or ACA",
            ],
            "detected_categories": normalization.detected_categories,
            "detected_hc_type": normalization.detected_hc_type,
            "matched_terms": normalization.matched_terms,
            "unmatched_tokens": normalization.unmatched_tokens,
            "source": "fallback",
        }

    # -----------------------------------------------------------------------
    # TIE Component 4: Authority Hardening
    # -----------------------------------------------------------------------

    def _harden_authority(self, citations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Assign authority scores and sort citations by weight."""
        for citation in citations:
            auth_type = citation.get("authority", "treatise")
            weight = AUTHORITY_WEIGHTS.get(auth_type, 30)
            citation["authority_weight"] = weight
        citations.sort(key=lambda c: c.get("authority_weight", 0), reverse=True)
        return citations

    # -----------------------------------------------------------------------
    # TIE Component 5: Confidence Stratification
    # -----------------------------------------------------------------------

    def _stratify_confidence(self, score: float) -> Tuple[str, str, bool]:
        """Map a confidence score to a band, label, and caveat requirement."""
        for band_name, band_info in CONFIDENCE_BANDS.items():
            if score >= band_info["min_score"]:
                return band_name, band_info["label"], band_info["requires_caveat"]
        return "HIGH_RISK", CONFIDENCE_BANDS["HIGH_RISK"]["label"], True

    # -----------------------------------------------------------------------
    # TIE Component 13: Zoned Analysis
    # -----------------------------------------------------------------------

    def analyze_hipaa_compliance(self, request: HIPAAComplianceRequest) -> Dict[str, Any]:
        """Perform HIPAA compliance gap analysis."""
        result = self._hipaa_checker.check_compliance(request.answers)
        self._telemetry.record_hc_metric(HealthcareMetricType.COMPLIANCE_CHECK)
        self._audit.append("hipaa_compliance_check", {
            "overall_score": result.overall_score,
            "risk_level": result.risk_level,
            "gap_count": len(result.gaps),
        })
        return result.to_dict()

    def analyze_malpractice(self, request: MalpracticeRequest) -> Dict[str, Any]:
        """Perform malpractice claim element analysis."""
        result = self._malpractice_analyzer.analyze_claim({
            "description": request.description,
            "jurisdiction": request.jurisdiction or "General",
        })
        self._telemetry.record_hc_metric(HealthcareMetricType.MALPRACTICE_QUERY)
        self._audit.append("malpractice_analysis", {
            "duty_established": result.duty_established,
            "risk_assessment": result.risk_assessment,
        })
        return result.to_dict()

    def analyze_fda_pathway(self, request: FDAPathwayRequest) -> Dict[str, Any]:
        """Determine FDA regulatory pathway."""
        result = self._fda_searcher.analyze_pathway(request.product_type, request.product_description)
        self._telemetry.record_hc_metric(HealthcareMetricType.FDA_QUERY)
        self._audit.append("fda_pathway_analysis", {
            "product_type": request.product_type,
            "classification": result.classification,
        })
        return result.to_dict()

    def assess_fraud_risk(self, request: FraudRiskRequest) -> Dict[str, Any]:
        """Assess Medicare fraud risk for an arrangement."""
        result = self._fraud_detector.assess_risk({"description": request.description})
        self._telemetry.record_hc_metric(HealthcareMetricType.FRAUD_ABUSE_QUERY)
        self._audit.append("fraud_risk_assessment", {
            "risk_level": result.risk_level,
            "risk_score": result.risk_score,
            "indicator_count": len(result.indicators),
        })
        return result.to_dict()

    # -----------------------------------------------------------------------
    # TIE Component 14: Fact Fragility Scoring
    # -----------------------------------------------------------------------

    def score_fact_fragility(self, request: FactFragilityRequest) -> Dict[str, Any]:
        """Score the fragility of factual assertions in healthcare law context."""
        scored_facts: List[Dict[str, Any]] = []
        fragility_keywords_high = {
            "oral", "verbal", "assumed", "allegedly", "uncertain", "disputed",
            "undocumented", "unverified", "informal", "approximate", "estimated",
            "off-label", "unapproved", "unlicensed", "unregistered",
        }
        fragility_keywords_medium = {
            "partial", "conditional", "contingent", "temporary", "possible",
            "might", "could", "may", "some", "generally", "typically",
        }
        stability_keywords = {
            "documented", "verified", "certified", "licensed", "registered",
            "approved", "fda-approved", "published", "peer-reviewed",
            "audited", "compliant", "signed", "notarized", "recorded",
        }

        for fact in request.facts:
            fact_lower = fact.lower()
            high_hits = sum(1 for kw in fragility_keywords_high if kw in fact_lower)
            med_hits = sum(1 for kw in fragility_keywords_medium if kw in fact_lower)
            stable_hits = sum(1 for kw in stability_keywords if kw in fact_lower)

            raw_fragility = (high_hits * 0.3 + med_hits * 0.15 - stable_hits * 0.2)
            fragility_score = max(0.0, min(1.0, 0.5 + raw_fragility))

            if fragility_score >= 0.7:
                risk_level = "HIGH"
                recommendation = "This fact is highly fragile. Verify with regulatory documentation, compliance records, or official filings before relying on it."
            elif fragility_score >= 0.5:
                risk_level = "MEDIUM"
                recommendation = "This fact has moderate fragility. Consider obtaining corroborating evidence from regulatory or clinical sources."
            else:
                risk_level = "LOW"
                recommendation = "This fact appears relatively stable. Standard verification recommended."

            scored_facts.append({
                "fact": fact,
                "fragility_score": round(fragility_score, 4),
                "risk_level": risk_level,
                "high_fragility_indicators": high_hits,
                "medium_fragility_indicators": med_hits,
                "stability_indicators": stable_hits,
                "recommendation": recommendation,
            })

        avg_fragility = sum(f["fragility_score"] for f in scored_facts) / max(len(scored_facts), 1)

        return {
            "facts": scored_facts,
            "average_fragility": round(avg_fragility, 4),
            "total_facts": len(scored_facts),
            "high_risk_count": sum(1 for f in scored_facts if f["risk_level"] == "HIGH"),
            "overall_assessment": (
                "The factual basis is fragile and regulatory conclusions should be heavily caveated."
                if avg_fragility >= 0.6
                else "The factual basis is reasonably stable but standard verification is recommended."
                if avg_fragility >= 0.4
                else "The factual basis appears stable and supports confident analysis."
            ),
        }

    # -----------------------------------------------------------------------
    # TIE Component 16: Determinism Hash
    # -----------------------------------------------------------------------

    def _compute_determinism_hash(self, analysis: Dict[str, Any], q_hash: str) -> str:
        """Compute SHA-256 determinism hash for response reproducibility."""
        content = json.dumps({"query_hash": q_hash, "analysis": analysis}, sort_keys=True, default=str)
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    # -----------------------------------------------------------------------
    # TIE Component 19: Multi-Doctrine Decomposition
    # -----------------------------------------------------------------------

    async def decompose_multi_doctrine(self, request: MultiDoctrineRequest) -> Dict[str, Any]:
        """Decompose a complex query into multiple doctrine analyses."""
        normalization = normalize_query(request.query)
        categories = normalization.detected_categories[:request.max_doctrines]

        if not categories:
            categories = ["hipaa", "fraud_abuse"]

        decomposed: List[Dict[str, Any]] = []
        for cat in categories:
            blocks = self._doctrine_cache.get_by_category(cat)
            if blocks:
                block = blocks[0]
                decomposed.append({
                    "category": cat,
                    "primary_doctrine": block.topic,
                    "summary": block.summary[:300],
                    "key_statutes": block.key_statutes[:3],
                    "confidence": block.confidence,
                    "authority_score": block.authority_score,
                })

        cross_refs: List[Dict[str, Any]] = []
        for i, d_a in enumerate(decomposed):
            for d_b in decomposed[i + 1:]:
                cross_refs.append({
                    "category_a": d_a["category"],
                    "category_b": d_b["category"],
                    "interaction_note": f"Analyze interaction between {d_a['category']} and {d_b['category']} requirements",
                })

        return {
            "original_query": request.query,
            "decomposed_doctrines": decomposed,
            "cross_references": cross_refs,
            "total_categories": len(categories),
            "recommendation": f"This query spans {len(categories)} healthcare law domains requiring coordinated analysis.",
        }

    # -----------------------------------------------------------------------
    # TIE Component 9: Doctrine Drift Watcher
    # -----------------------------------------------------------------------

    def register_drift_signal(self, signal: DriftSignal) -> Dict[str, Any]:
        """Register a doctrine drift signal."""
        entry = {
            "signal_type": signal.signal_type,
            "topic": signal.topic,
            "description": signal.description,
            "source": signal.source,
            "authority_level": signal.authority_level,
            "confidence_impact": signal.confidence_impact,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self._drift_registry.setdefault("signals", []).append(entry)
        self._drift_registry["last_check"] = datetime.now(timezone.utc).isoformat()
        self._save_drift_registry()

        record_doctrine_mutation(
            MutationType.DRIFT_DETECTED,
            MutationOrigin.DRIFT_WATCHER,
            signal.topic,
            {"signal_type": signal.signal_type, "impact": signal.confidence_impact},
        )

        return {"registered": True, "total_signals": len(self._drift_registry["signals"])}

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
        q_hash: str,
        jurisdiction: Optional[str],
        normalization: NormalizationResult,
        start: float,
    ) -> EngineResponse:
        """Build the standardized engine response."""
        # TIE Component 4: Authority Hardening
        hardened_citations = self._harden_authority(citations)

        # TIE Component 5: Confidence Stratification
        band, label, requires_caveat = self._stratify_confidence(confidence_score)

        # Disclaimers
        disclaimers = [REQUIRED_DISCLAIMERS["not_legal_advice"]]
        if requires_caveat:
            disclaimers.append(REQUIRED_DISCLAIMERS["regulatory_risk"])
        if jurisdiction:
            disclaimers.append(REQUIRED_DISCLAIMERS["jurisdiction_specific"])
        disclaimers.append(REQUIRED_DISCLAIMERS["fact_dependent"])

        # Deduplicate practice tips
        unique_tips = list(dict.fromkeys(practice_tips))

        # TIE Component 16: Determinism Hash
        det_hash = self._compute_determinism_hash(analysis, q_hash)

        # Complete trace
        trace.final_layer = layer_used
        trace.confidence_score = confidence_score
        trace.confidence_band = band
        trace.citations_found = len(hardened_citations)
        trace.determinism_hash = det_hash
        complete_trace(trace)

        elapsed_ms = (time.monotonic() - start) * 1000.0

        return EngineResponse(
            query_hash=q_hash,
            response_mode=request.mode,
            confidence_score=round(confidence_score, 4),
            confidence_band=band,
            confidence_label=label,
            requires_caveat=requires_caveat,
            layer_used=layer_used.value,
            jurisdiction=jurisdiction,
            hc_category=normalization.detected_hc_type,
            analysis=analysis,
            citations=hardened_citations[:15] if request.include_citations else [],
            disclaimers=disclaimers,
            practice_tips=unique_tips[:10] if request.include_practice_tips else [],
            determinism_hash=det_hash,
            trace_id=trace.trace_id,
            processing_time_ms=round(elapsed_ms, 3),
            timestamp=datetime.now(timezone.utc).isoformat(),
        )


# ============================================================================
# FASTAPI APPLICATION SETUP
# ============================================================================

def _load_config() -> Dict[str, Any]:
    """Load engine configuration from config.json."""
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as fh:
                return json.load(fh)
        except (json.JSONDecodeError, OSError) as exc:
            logger.warning(f"Failed to load config: {exc}")
    return {"engine_id": ENGINE_ID, "port": ENGINE_PORT, "engine_authority": ENGINE_AUTHORITY}


_engine: Optional[HealthcareLawEngine] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: initialize engine on startup."""
    global _engine
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    config = _load_config()
    _engine = HealthcareLawEngine(config)
    logger.info(f"LG14 Healthcare Law Engine started on port {ENGINE_PORT}")
    yield
    logger.info("LG14 Healthcare Law Engine shutting down")


app = FastAPI(
    title=ENGINE_NAME,
    version=ENGINE_VERSION,
    description="TIE-20 compliant healthcare law analysis engine",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


def _get_engine() -> HealthcareLawEngine:
    """Get the engine instance or raise."""
    if _engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    return _engine


# ============================================================================
# FASTAPI ENDPOINTS
# ============================================================================

@app.get("/health")
async def health_check() -> Dict[str, Any]:
    """TIE Component 12: Health endpoint."""
    engine = _get_engine()
    return {
        "status": "healthy",
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "engine_version": ENGINE_VERSION,
        "engine_mode": ENGINE_MODE,
        "port": ENGINE_PORT,
        "authority": ENGINE_AUTHORITY,
        "tier": ENGINE_TIER,
        "uptime_since": engine._boot_time,
        "query_count": engine._query_count,
        "doctrine_blocks": len(DOCTRINE_BLOCKS),
        "semantic_version": engine._semantic_version,
        "search_index_docs": engine._search_index.document_count,
        "search_index_vocab": engine._search_index.vocabulary_size,
        "doctrine_cache_hash": get_doctrine_cache_hash(),
        "semantic_map_hash": get_semantic_map_hash(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.post("/query")
async def query_endpoint(request: QueryRequest) -> EngineResponse:
    """Main query endpoint - processes healthcare law queries through 3-layer pipeline."""
    engine = _get_engine()
    return await engine.process_query(request)


@app.post("/hipaa/compliance")
async def hipaa_compliance_endpoint(request: HIPAAComplianceRequest) -> Dict[str, Any]:
    """HIPAA compliance gap analysis."""
    engine = _get_engine()
    return engine.analyze_hipaa_compliance(request)


@app.get("/hipaa/requirements")
async def hipaa_requirements_endpoint() -> Dict[str, Any]:
    """Get HIPAA compliance requirement checklist."""
    engine = _get_engine()
    return engine._hipaa_checker.get_requirements()


@app.post("/malpractice/analyze")
async def malpractice_endpoint(request: MalpracticeRequest) -> Dict[str, Any]:
    """Medical malpractice claim element analysis."""
    engine = _get_engine()
    return engine.analyze_malpractice(request)


@app.post("/fda/pathway")
async def fda_pathway_endpoint(request: FDAPathwayRequest) -> Dict[str, Any]:
    """FDA regulatory pathway analysis."""
    engine = _get_engine()
    return engine.analyze_fda_pathway(request)


@app.post("/fraud/risk")
async def fraud_risk_endpoint(request: FraudRiskRequest) -> Dict[str, Any]:
    """Medicare fraud risk assessment."""
    engine = _get_engine()
    return engine.assess_fraud_risk(request)


@app.post("/fact-fragility")
async def fact_fragility_endpoint(request: FactFragilityRequest) -> Dict[str, Any]:
    """TIE Component 14: Fact fragility scoring."""
    engine = _get_engine()
    return engine.score_fact_fragility(request)


@app.post("/multi-doctrine")
async def multi_doctrine_endpoint(request: MultiDoctrineRequest) -> Dict[str, Any]:
    """TIE Component 19: Multi-doctrine decomposition."""
    engine = _get_engine()
    return await engine.decompose_multi_doctrine(request)


@app.post("/drift/signal")
async def drift_signal_endpoint(signal: DriftSignal) -> Dict[str, Any]:
    """TIE Component 9: Register a doctrine drift signal."""
    engine = _get_engine()
    return engine.register_drift_signal(signal)


@app.get("/drift/registry")
async def drift_registry_endpoint() -> Dict[str, Any]:
    """Get the current drift registry."""
    engine = _get_engine()
    return engine._drift_registry


@app.get("/coverage")
async def coverage_endpoint() -> Dict[str, Any]:
    """TIE Component 10: Doctrine coverage map."""
    return get_coverage_map()


@app.get("/doctrines")
async def doctrines_endpoint() -> Dict[str, Any]:
    """List all doctrine topics and categories."""
    return {
        "topics": get_all_doctrine_topics(),
        "categories": get_all_doctrine_categories(),
        "stats": get_doctrine_cache_stats(),
    }


@app.get("/doctrine/{topic}")
async def doctrine_detail_endpoint(topic: str) -> Dict[str, Any]:
    """Get a specific doctrine block by topic."""
    block = get_doctrine_block(topic)
    if block is None:
        raise HTTPException(status_code=404, detail=f"Doctrine topic '{topic}' not found")
    return block.to_dict()


@app.get("/integrity")
async def integrity_endpoint() -> Dict[str, Any]:
    """Verify doctrine and semantic dictionary integrity."""
    return {
        "doctrine_integrity": verify_doctrine_integrity(),
        "semantic_integrity": verify_dictionary_integrity(),
    }


@app.get("/metrics")
async def metrics_endpoint() -> Dict[str, Any]:
    """TIE Component 11: Metrics collector."""
    engine = _get_engine()
    return engine._telemetry.get_metrics_summary()


@app.get("/audit/verify")
async def audit_verify_endpoint() -> Dict[str, Any]:
    """TIE Component 15: Verify audit trail integrity."""
    engine = _get_engine()
    return engine._audit.verify_chain()


@app.get("/stale-doctrines")
async def stale_doctrines_endpoint(threshold_days: int = Query(90, ge=1)) -> Dict[str, Any]:
    """Get doctrine blocks exceeding staleness threshold."""
    stale = get_stale_doctrines(threshold_days)
    return {
        "threshold_days": threshold_days,
        "stale_count": len(stale),
        "stale_doctrines": [b.to_dict() for b in stale],
    }


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    logger.remove()
    logger.add(
        sys.stderr,
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {message}",
        level="INFO",
    )
    logger.add(
        LOG_DIR / "engine.log",
        rotation="50 MB",
        retention="30 days",
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {message}",
        level="DEBUG",
    )

    logger.info(f"Starting {ENGINE_NAME} v{ENGINE_VERSION} on port {ENGINE_PORT}")
    uvicorn.run(
        "engine:app",
        host=ENGINE_HOST,
        port=ENGINE_PORT,
        reload=False,
        log_level="info",
    )
