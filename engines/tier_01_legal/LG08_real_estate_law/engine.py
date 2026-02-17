"""
LG08 Real Estate Law Engine - Main FastAPI Engine
====================================================
Production-grade real estate law analysis engine implementing all 20 TIE
components for property transaction review, title examination, deed analysis,
easement interpretation, zoning compliance, landlord-tenant law, eminent
domain, financing, foreclosure, 1031 exchanges, RESPA/TILA/Fair Housing
compliance, Texas Property Code, community property, homestead exemption,
and oil/gas mineral rights analysis.

TIE-20 Components:
    1.  three_layer_response
    2.  response_modes (fast, analysis, memo, title_opinion, transaction_review)
    3.  doctrine_cache
    4.  authority_hardening
    5.  confidence_stratification
    6.  semantic_normalization
    7.  vector_search_chromadb (TF-IDF inverted index implementation)
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

Port: 8398
Engine: LG08 Real Estate Law
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
    DeedInterpreter,
    EncumbranceRecord,
    Exchange1031Result,
    Exchange1031Validator,
    SearchResult,
    TitleChainAnalyzer,
    TitleChainEntry,
    TransactionChecklistGenerator,
    ZoningComplianceChecker,
    ZoningComplianceResult,
    compute_query_hash,
    get_checklist_generator,
    get_deed_interpreter,
    get_exchange_validator,
    get_search_index,
    get_title_analyzer,
    get_zoning_checker,
)
from semantic import (
    NormalizationResult,
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
    MetricsAggregator,
    MutationOrigin,
    MutationType,
    QueryTrace,
    RealEstateMetricType,
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

ENGINE_ID: str = "LG08"
ENGINE_NAME: str = "Real Estate Law Engine"
ENGINE_VERSION: str = "2.0.0"
ENGINE_PORT: int = 8398
ENGINE_HOST: str = "0.0.0.0"
ENGINE_AUTHORITY: float = 5.0
ENGINE_TIER: str = "LEGAL"
ENGINE_MODE: str = "DET"

CONFIG_PATH: Path = Path(__file__).parent / "config.json"
LOG_DIR: Path = Path(__file__).parent / "logs"
AUDIT_LOG_PATH: Path = LOG_DIR / "audit_trail.jsonl"
DRIFT_REGISTRY_PATH: Path = Path(__file__).parent / "doctrine_drift_registry.json"

BANNED_PHRASES: List[str] = [
    "This title is definitely clear",
    "There are absolutely no encumbrances",
    "The property is guaranteed to close",
    "You will certainly win this foreclosure",
    "No court would find a taking",
    "This deed is bulletproof",
    "The zoning will definitely be approved",
    "There is zero risk in this transaction",
    "The HOA cannot enforce this restriction",
    "This lease is completely enforceable",
    "Your homestead claim is guaranteed",
    "The mineral rights are absolutely separated",
    "This 1031 exchange will certainly qualify",
    "RESPA does not apply here",
]

REQUIRED_DISCLAIMERS: Dict[str, str] = {
    "not_legal_advice": (
        "This analysis is for informational purposes only and does not "
        "constitute legal advice. Consult a licensed real estate attorney "
        "for specific legal guidance."
    ),
    "jurisdiction_specific": (
        "Real estate law varies significantly by state and locality. "
        "This analysis may not apply in all jurisdictions."
    ),
    "fact_dependent": (
        "Real estate outcomes depend heavily on specific facts, property "
        "conditions, title history, and local regulations. This analysis "
        "is based on the information provided."
    ),
    "title_caveat": (
        "Title opinions and searches cannot guarantee completeness. "
        "Undiscovered liens, encumbrances, or defects may exist."
    ),
}

AUTHORITY_WEIGHTS: Dict[str, int] = {
    "us_supreme_court": 100,
    "state_supreme_court": 90,
    "federal_circuit_court": 85,
    "state_appellate_court": 75,
    "federal_district_court": 70,
    "state_trial_court": 55,
    "federal_statute": 95,
    "state_statute": 90,
    "local_ordinance": 60,
    "cfr_regulation": 80,
    "cfpb_guidance": 70,
    "hud_regulation": 75,
    "alta_form": 65,
    "restatement_property": 50,
    "treatise": 40,
    "title_standard": 55,
    "bar_association_opinion": 45,
    "law_review": 30,
}

CONFIDENCE_BANDS: Dict[str, Dict[str, Any]] = {
    "DEFENSIBLE": {"min_score": 0.85, "label": "Position is well-supported by established real estate law and precedent", "requires_caveat": False},
    "SUPPORTABLE": {"min_score": 0.65, "label": "Position has reasonable support but some uncertainty in application", "requires_caveat": True},
    "DISCLOSURE": {"min_score": 0.50, "label": "Position requires disclosure of contrary authority or jurisdictional variation", "requires_caveat": True},
    "HIGH_RISK": {"min_score": 0.0, "label": "Position faces significant adverse authority or untested legal theory", "requires_caveat": True},
}

RE_CATEGORY_METRIC_MAP: Dict[str, RealEstateMetricType] = {
    "title": RealEstateMetricType.TITLE_QUERY,
    "deed": RealEstateMetricType.DEED_QUERY,
    "easement": RealEstateMetricType.EASEMENT_QUERY,
    "zoning": RealEstateMetricType.ZONING_QUERY,
    "landlord_tenant": RealEstateMetricType.LANDLORD_TENANT_QUERY,
    "financing": RealEstateMetricType.FINANCING_QUERY,
    "foreclosure": RealEstateMetricType.FORECLOSURE_QUERY,
    "tax": RealEstateMetricType.TAX_QUERY,
    "eminent_domain": RealEstateMetricType.EMINENT_DOMAIN_QUERY,
    "hoa": RealEstateMetricType.HOA_QUERY,
    "mineral_rights": RealEstateMetricType.MINERAL_RIGHTS_QUERY,
    "tax_exchange": RealEstateMetricType.EXCHANGE_1031_QUERY,
    "compliance": RealEstateMetricType.COMPLIANCE_CHECK,
    "transaction": RealEstateMetricType.TRANSACTION_REVIEW,
    "texas": RealEstateMetricType.TEXAS_SPECIFIC,
}


# ============================================================================
# PYDANTIC REQUEST/RESPONSE MODELS
# ============================================================================

class QueryRequest(BaseModel):
    """Incoming query request."""
    query: str = Field(..., min_length=3, max_length=5000, description="The real estate law question")
    mode: str = Field("fast", description="Response mode: fast, analysis, memo, title_opinion, transaction_review")
    jurisdiction: Optional[str] = Field(None, description="Jurisdiction filter (e.g. TX, CA, NY)")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context for analysis")
    include_citations: bool = Field(True, description="Include statutory and case citations")
    include_practice_tips: bool = Field(False, description="Include practice tips in response")
    max_results: int = Field(5, ge=1, le=20, description="Maximum doctrine results to return")

    @field_validator("mode")
    @classmethod
    def validate_mode(cls, v: str) -> str:
        valid_modes = {"fast", "analysis", "memo", "title_opinion", "transaction_review"}
        if v not in valid_modes:
            raise ValueError(f"Invalid mode '{v}'. Must be one of: {valid_modes}")
        return v


class DeedAnalysisRequest(BaseModel):
    """Deed analysis request."""
    deed_type: str = Field(..., description="Type of deed to analyze")
    compare_with: Optional[str] = Field(None, description="Second deed type for comparison")


class ZoningCheckRequest(BaseModel):
    """Zoning compliance check request."""
    zoning_code: str = Field(..., description="Current zoning classification (e.g. R-1, C-2)")
    proposed_use: str = Field(..., description="Proposed use of the property")


class Exchange1031Request(BaseModel):
    """1031 exchange validation request."""
    relinquished_type: str = Field(..., description="Type of property being sold")
    replacement_type: str = Field(..., description="Type of replacement property")
    held_for_investment: bool = Field(True, description="Property held for investment/business")
    using_qi: bool = Field(True, description="Using a qualified intermediary")
    days_since_close: int = Field(0, ge=0, description="Days since relinquished property closing")
    replacement_identified: bool = Field(False, description="Replacement property identified")
    same_taxpayer: bool = Field(True, description="Same taxpayer on both transactions")
    related_party: bool = Field(False, description="Related party transaction")
    exchange_type: str = Field("delayed", description="Exchange type: delayed, reverse, simultaneous, improvement")


class TitleChainRequest(BaseModel):
    """Title chain analysis request."""
    chain_data: Optional[List[Dict[str, Any]]] = Field(None, description="Chain of title data (uses sample if omitted)")


class TransactionChecklistRequest(BaseModel):
    """Transaction checklist request."""
    transaction_type: str = Field("purchase", description="Transaction type: purchase, sale, lease")


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
    re_category: Optional[str] = Field(None, description="Real estate category context")


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
    re_category: Optional[str]
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

class RealEstateLawEngine:
    """Core engine implementing all 20 TIE components.

    Orchestrates doctrine cache, semantic normalization, search,
    telemetry, authority hardening, confidence stratification,
    drift watching, and deep analysis for real estate law queries.
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

        # Search helpers
        self._title_analyzer: TitleChainAnalyzer = get_title_analyzer()
        self._deed_interpreter: DeedInterpreter = get_deed_interpreter()
        self._zoning_checker: ZoningComplianceChecker = get_zoning_checker()
        self._exchange_validator: Exchange1031Validator = get_exchange_validator()
        self._checklist_gen: TransactionChecklistGenerator = get_checklist_generator()

        # TIE Component 9: Doctrine Drift Watcher
        self._drift_registry: Dict[str, Any] = self._load_drift_registry()

        # TIE Component 15: Audit Trail
        self._audit: AuditTrail = self._telemetry._audit

        # Index doctrine blocks for search
        self._index_doctrines()

        self._boot_time: str = datetime.now(timezone.utc).isoformat()
        self._query_count: int = 0

        logger.info(
            f"RealEstateLawEngine initialized | id={self._engine_id} | "
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
                re_category=block.category,
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
        """Process a real estate law query through the three-layer pipeline.

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
        trace.re_category = normalization.detected_re_type
        trace.jurisdiction = request.jurisdiction or normalization.detected_jurisdiction

        # TIE Component 11: Metrics - record category
        if normalization.detected_re_type and normalization.detected_re_type in RE_CATEGORY_METRIC_MAP:
            self._telemetry.record_re_metric(RE_CATEGORY_METRIC_MAP[normalization.detected_re_type])

        # Determine jurisdiction
        jurisdiction = request.jurisdiction or normalization.detected_jurisdiction

        layer_used = ResponseLayer.FALLBACK
        analysis: Dict[str, Any] = {}
        citations: List[Dict[str, Any]] = []
        practice_tips: List[str] = []
        confidence_score: float = 0.0

        # --- LAYER 1: Doctrine Cache ---
        step1 = trace.add_step("doctrine_cache_lookup", ResponseLayer.DOCTRINE_CACHE, normalization.detected_re_type)
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
                # Fast mode: return doctrine cache result immediately
                return self._build_response(
                    request, trace, layer_used, analysis, citations,
                    practice_tips, confidence_score, q_hash, jurisdiction,
                    normalization, start,
                )

        # --- LAYER 2: Semantic Search ---
        step2 = trace.add_step("semantic_search", ResponseLayer.SEMANTIC_SEARCH, normalization.detected_re_type)
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
        step3 = trace.add_step("deep_analysis", ResponseLayer.DEEP_ANALYSIS, normalization.detected_re_type)
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

        # Direct topic match
        for term in normalization.matched_terms:
            canonical = term.get("canonical", "")
            block = self._doctrine_cache.get_by_topic(canonical)
            if block and block not in blocks:
                blocks.append(block)

        # Category match
        for cat in normalization.detected_categories:
            cat_blocks = self._doctrine_cache.get_by_category(cat)
            for block in cat_blocks:
                if block not in blocks:
                    blocks.append(block)

        # Free-text search over doctrine content
        if not blocks:
            blocks = self._doctrine_cache.search_blocks(normalization.normalized_query.lower(), top_k=3)

        # Filter by jurisdiction if specified
        if jurisdiction and blocks:
            filtered = [b for b in blocks if b.jurisdiction in ("federal", jurisdiction)]
            if filtered:
                blocks = filtered

        # Extract citations and tips from matched blocks
        for block in blocks[:5]:
            for statute in block.key_statutes:
                citations.append({"type": "statute", "text": statute, "authority": "statutory", "source": block.topic})
            for case in block.leading_cases:
                citations.append({"type": "case", "text": case, "authority": "case_law", "source": block.topic})
            tips.extend(block.practice_tips)

        # Compute confidence from matched blocks
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

        re_cat = normalization.detected_re_type
        results = self._search_index.search(
            query_tokens=query_tokens,
            top_k=max_results,
            score_threshold=0.1,
            re_category_filter=re_cat if re_cat else None,
            jurisdiction_filter=jurisdiction,
            authority_weight=0.3,
            recency_weight=0.1,
        )

        # If category filter returned nothing, try without filter
        if not results and re_cat:
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

        # Cross-reference analysis
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

        # Aggregate citations
        citations: List[Dict[str, Any]] = []
        tips: List[str] = []
        for block in all_blocks[:5]:
            for statute in block.key_statutes[:2]:
                citations.append({"type": "statute", "text": statute, "source": block.topic})
            for case in block.leading_cases[:1]:
                citations.append({"type": "case", "text": case, "source": block.topic})
            tips.extend(block.practice_tips[:2])

        # Risk factors
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
                "Try rephrasing the query using standard real estate terminology",
                "Specify a jurisdiction for more targeted results",
                "Break complex questions into individual sub-questions",
            ],
            "detected_categories": normalization.detected_categories,
            "detected_re_type": normalization.detected_re_type,
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

    def analyze_zoning(self, request: ZoningCheckRequest) -> Dict[str, Any]:
        """Perform zoning compliance analysis."""
        result = self._zoning_checker.check_compliance(request.zoning_code, request.proposed_use)
        self._telemetry.record_re_metric(RealEstateMetricType.ZONING_QUERY)
        self._audit.append("zoning_analysis", {
            "zoning_code": request.zoning_code,
            "proposed_use": request.proposed_use,
            "compliant": result.compliant,
        })
        return result.to_dict()

    # -----------------------------------------------------------------------
    # TIE Component 14: Fact Fragility Scoring
    # -----------------------------------------------------------------------

    def score_fact_fragility(self, request: FactFragilityRequest) -> Dict[str, Any]:
        """Score the fragility of factual assertions.

        Fragility measures how sensitive the legal outcome is to
        changes in the stated facts. Higher fragility means the
        conclusion is more vulnerable to factual variation.
        """
        scored_facts: List[Dict[str, Any]] = []
        fragility_keywords_high = {
            "oral", "verbal", "handshake", "approximate", "estimated",
            "believed", "assumed", "allegedly", "uncertain", "disputed",
            "unrecorded", "undisclosed", "unlicensed", "informal",
        }
        fragility_keywords_medium = {
            "partial", "conditional", "contingent", "temporary", "possible",
            "might", "could", "may", "some", "several", "generally",
        }
        stability_keywords = {
            "recorded", "notarized", "signed", "written", "surveyed",
            "appraised", "inspected", "certified", "confirmed", "documented",
            "verified", "established", "proven", "acknowledged",
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
                recommendation = "This fact is highly fragile. Verify with documentary evidence before relying on it for legal conclusions."
            elif fragility_score >= 0.5:
                risk_level = "MEDIUM"
                recommendation = "This fact has moderate fragility. Consider obtaining corroborating evidence."
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
                "The factual basis is fragile and conclusions should be heavily caveated."
                if avg_fragility >= 0.6
                else "The factual basis is reasonably stable but standard verification is recommended."
                if avg_fragility >= 0.4
                else "The factual basis appears solid. Normal due diligence applies."
            ),
        }

    # -----------------------------------------------------------------------
    # TIE Component 9: Doctrine Drift Watcher
    # -----------------------------------------------------------------------

    def record_drift_signal(self, signal: DriftSignal) -> Dict[str, Any]:
        """Record a doctrine drift signal and assess impact."""
        signal_record = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "signal_type": signal.signal_type,
            "topic": signal.topic,
            "description": signal.description,
            "source": signal.source,
            "authority_level": signal.authority_level,
            "confidence_impact": signal.confidence_impact,
        }
        self._drift_registry.setdefault("signals", []).append(signal_record)
        self._drift_registry["last_check"] = datetime.now(timezone.utc).isoformat()
        self._save_drift_registry()

        # Record mutation in telemetry
        record_doctrine_mutation(
            mutation_type=MutationType.DRIFT_DETECTED,
            origin=MutationOrigin.DRIFT_WATCHER,
            topic=signal.topic,
            description=signal.description,
            re_category=signal.signal_type,
            triggering_authority=signal.authority_level,
        )

        # Audit trail entry
        self._audit.append("drift_signal", signal_record)

        # Check if the topic exists and assess staleness
        block = self._doctrine_cache.get_by_topic(signal.topic)
        affected = block is not None

        return {
            "signal_id": signal_record["id"],
            "recorded": True,
            "topic_found": affected,
            "topic_confidence_before": block.confidence if block else None,
            "recommended_action": (
                "Review and update doctrine block"
                if affected
                else "Monitor - no existing doctrine block for this topic"
            ),
        }

    def get_drift_registry(self) -> Dict[str, Any]:
        """Get the current drift registry."""
        return {
            "signals": self._drift_registry.get("signals", [])[-20:],
            "total_signals": len(self._drift_registry.get("signals", [])),
            "last_check": self._drift_registry.get("last_check", "never"),
            "version": self._drift_registry.get("version", ENGINE_VERSION),
        }

    # -----------------------------------------------------------------------
    # TIE Component 19: Multi-Doctrine Decomposition
    # -----------------------------------------------------------------------

    async def multi_doctrine_decomposition(self, request: MultiDoctrineRequest) -> Dict[str, Any]:
        """Decompose a complex query into multiple doctrine analyses."""
        normalization = normalize_query(request.query)
        categories = normalization.detected_categories

        if not categories:
            categories = ["transaction"]

        decomposed: List[Dict[str, Any]] = []
        all_citations: List[Dict[str, Any]] = []
        all_tips: List[str] = []

        for cat in categories[:request.max_doctrines]:
            blocks = self._doctrine_cache.get_by_category(cat)
            if not blocks:
                continue

            best_block = max(blocks, key=lambda b: b.confidence)
            sub_analysis = {
                "category": cat,
                "primary_doctrine": best_block.topic,
                "summary": best_block.summary[:300],
                "confidence": best_block.confidence,
                "key_statutes": best_block.key_statutes[:3],
                "leading_cases": best_block.leading_cases[:2],
                "elements": best_block.elements[:5],
                "defenses": best_block.defenses[:3],
                "remedies": best_block.remedies[:3],
                "risk_factors": best_block.risk_factors[:3],
            }
            decomposed.append(sub_analysis)

            for statute in best_block.key_statutes[:2]:
                all_citations.append({"type": "statute", "text": statute, "source": best_block.topic})
            for case in best_block.leading_cases[:1]:
                all_citations.append({"type": "case", "text": case, "source": best_block.topic})
            all_tips.extend(best_block.practice_tips[:2])

        avg_confidence = sum(d["confidence"] for d in decomposed) / max(len(decomposed), 1)

        return {
            "query": request.query,
            "decomposition_count": len(decomposed),
            "categories_analyzed": [d["category"] for d in decomposed],
            "decomposed_analyses": decomposed,
            "cross_doctrine_note": f"Query spans {len(decomposed)} doctrine areas. Each area should be evaluated independently and then synthesized.",
            "overall_confidence": round(avg_confidence, 4),
            "citations": all_citations[:15],
            "practice_tips": list(dict.fromkeys(all_tips))[:8],
            "jurisdiction": request.jurisdiction or normalization.detected_jurisdiction,
        }

    # -----------------------------------------------------------------------
    # Deep Analysis (TIE Component 20)
    # -----------------------------------------------------------------------

    async def deep_analysis(self, request: DeepAnalysisRequest) -> Dict[str, Any]:
        """Perform deep multi-faceted analysis of a real estate question."""
        normalization = normalize_query(request.query)
        jurisdiction = request.jurisdiction or normalization.detected_jurisdiction

        # Gather all relevant doctrine blocks
        all_blocks: List[DoctrineCacheBlock] = []
        for cat in normalization.detected_categories:
            all_blocks.extend(self._doctrine_cache.get_by_category(cat))
        if not all_blocks:
            all_blocks = self._doctrine_cache.search_blocks(request.query.lower(), top_k=5)

        if not all_blocks:
            return {
                "query": request.query,
                "status": "no_matching_doctrines",
                "recommendation": "The query does not match any pre-compiled doctrines. Consider narrowing the question or specifying a real estate category.",
            }

        # Build comprehensive analysis
        analysis_sections: List[Dict[str, Any]] = []
        for block in all_blocks[:5]:
            section = {
                "topic": block.topic,
                "category": block.category,
                "summary": block.summary,
                "key_statutes": block.key_statutes,
                "elements": block.elements,
                "defenses": block.defenses,
                "remedies": block.remedies,
                "leading_cases": block.leading_cases,
                "confidence": block.confidence,
                "authority_score": block.authority_score,
            }

            if jurisdiction and block.texas_notes and jurisdiction == "TX":
                section["texas_specific"] = block.texas_notes

            analysis_sections.append(section)

        # Risk assessment
        risk_assessment: Dict[str, Any] = {}
        if request.include_risk_assessment:
            all_risks = []
            for block in all_blocks[:5]:
                all_risks.extend(block.risk_factors)
            risk_assessment = {
                "risk_factors": list(dict.fromkeys(all_risks))[:10],
                "risk_level": "HIGH" if len(all_risks) > 5 else "MEDIUM" if len(all_risks) > 2 else "LOW",
                "mitigation": [
                    "Obtain title insurance to protect against undiscovered defects",
                    "Engage qualified legal counsel for jurisdiction-specific guidance",
                    "Conduct thorough due diligence including surveys and inspections",
                ],
            }

        # Alternative approaches
        alternatives: List[Dict[str, str]] = []
        if request.include_alternatives:
            for block in all_blocks[:3]:
                for topic in block.related_topics[:2]:
                    related = self._doctrine_cache.get_by_topic(topic)
                    if related:
                        alternatives.append({
                            "topic": related.topic,
                            "category": related.category,
                            "summary": related.summary[:200],
                        })

        avg_conf = sum(b.confidence for b in all_blocks[:5]) / max(len(all_blocks[:5]), 1)

        return {
            "query": request.query,
            "jurisdiction": jurisdiction,
            "categories_analyzed": list(set(b.category for b in all_blocks[:5])),
            "analysis_sections": analysis_sections,
            "risk_assessment": risk_assessment,
            "alternative_approaches": alternatives[:5],
            "overall_confidence": round(avg_conf, 4),
            "disclaimers": [REQUIRED_DISCLAIMERS["not_legal_advice"], REQUIRED_DISCLAIMERS["jurisdiction_specific"]],
        }

    # -----------------------------------------------------------------------
    # Deed, Title, Exchange, Checklist analyses
    # -----------------------------------------------------------------------

    def analyze_deed(self, request: DeedAnalysisRequest) -> Dict[str, Any]:
        """Analyze a deed type."""
        self._telemetry.record_re_metric(RealEstateMetricType.DEED_QUERY)
        result = self._deed_interpreter.interpret_deed(request.deed_type)
        if request.compare_with:
            comparison = self._deed_interpreter.compare_deeds(request.deed_type, request.compare_with)
            result["comparison"] = comparison
        self._audit.append("deed_analysis", {"deed_type": request.deed_type, "compare_with": request.compare_with})
        return result

    def analyze_title_chain(self, request: TitleChainRequest) -> Dict[str, Any]:
        """Analyze a chain of title."""
        self._telemetry.record_re_metric(RealEstateMetricType.TITLE_QUERY)
        chain = self._title_analyzer.analyze_chain(request.chain_data)
        encumbrances = self._title_analyzer.identify_encumbrances(chain)
        opinion = self._title_analyzer.generate_title_opinion(chain, encumbrances)
        self._audit.append("title_chain_analysis", {"chain_length": len(chain), "encumbrances": len(encumbrances)})
        return {
            "chain": [e.to_dict() for e in chain],
            "active_encumbrances": [e.to_dict() for e in encumbrances],
            "title_opinion": opinion,
        }

    def validate_1031_exchange(self, request: Exchange1031Request) -> Dict[str, Any]:
        """Validate a 1031 exchange."""
        self._telemetry.record_re_metric(RealEstateMetricType.EXCHANGE_1031_QUERY)
        result = self._exchange_validator.validate(
            relinquished_type=request.relinquished_type,
            replacement_type=request.replacement_type,
            held_for_investment=request.held_for_investment,
            using_qi=request.using_qi,
            days_since_relinquished_close=request.days_since_close,
            replacement_identified=request.replacement_identified,
            same_taxpayer=request.same_taxpayer,
            related_party=request.related_party,
            exchange_type=request.exchange_type,
        )
        self._audit.append("1031_exchange_validation", {"qualifies": result.qualifies, "exchange_type": request.exchange_type})
        return result.to_dict()

    def generate_checklist(self, request: TransactionChecklistRequest) -> Dict[str, Any]:
        """Generate a transaction due diligence checklist."""
        self._telemetry.record_re_metric(RealEstateMetricType.TRANSACTION_REVIEW)
        checklist = self._checklist_gen.generate_checklist(request.transaction_type)
        self._audit.append("checklist_generated", {"transaction_type": request.transaction_type, "items": len(checklist)})
        return {
            "transaction_type": request.transaction_type,
            "checklist": checklist,
            "total_items": len(checklist),
        }

    # -----------------------------------------------------------------------
    # TIE Component 16: Determinism Hash (SHA-256)
    # -----------------------------------------------------------------------

    def _compute_determinism_hash(self, analysis: Dict[str, Any], q_hash: str) -> str:
        """Compute a deterministic SHA-256 hash of the response."""
        content = json.dumps({"query_hash": q_hash, "analysis": analysis}, sort_keys=True, default=str)
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    # -----------------------------------------------------------------------
    # Epistemic guardrails
    # -----------------------------------------------------------------------

    def _apply_epistemic_guardrails(self, text: str) -> str:
        """Strip banned phrases from response text."""
        result = text
        for phrase in BANNED_PHRASES:
            if phrase.lower() in result.lower():
                result = result.replace(phrase, "[REDACTED - overconfident assertion removed]")
        return result

    def _select_disclaimers(self, confidence_band: str, re_category: Optional[str]) -> List[str]:
        """Select appropriate disclaimers based on confidence and category."""
        disclaimers = [REQUIRED_DISCLAIMERS["not_legal_advice"]]
        if confidence_band in ("DISCLOSURE", "HIGH_RISK"):
            disclaimers.append(REQUIRED_DISCLAIMERS["jurisdiction_specific"])
            disclaimers.append(REQUIRED_DISCLAIMERS["fact_dependent"])
        if re_category in ("title", "deed"):
            disclaimers.append(REQUIRED_DISCLAIMERS["title_caveat"])
        return disclaimers

    # -----------------------------------------------------------------------
    # Response builder
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
        """Build the final engine response."""
        # TIE Component 4: Authority Hardening
        hardened_citations = self._harden_authority(citations) if request.include_citations else []

        # TIE Component 5: Confidence Stratification
        band, label, requires_caveat = self._stratify_confidence(confidence_score)

        # Select disclaimers
        disclaimers = self._select_disclaimers(band, normalization.detected_re_type)

        # Select practice tips
        final_tips = list(dict.fromkeys(practice_tips))[:10] if request.include_practice_tips else []

        # TIE Component 16: Determinism Hash
        det_hash = self._compute_determinism_hash(analysis, q_hash)

        # Complete telemetry trace
        trace.confidence_score = confidence_score
        trace.confidence_band = band
        trace.citations_found = len(hardened_citations)
        trace.determinism_hash = det_hash
        complete_trace(trace, layer_used)

        processing_time = (time.monotonic() - start) * 1000.0

        # Add normalization info to analysis
        analysis["normalization"] = {
            "original_query": normalization.original_query,
            "normalized_query": normalization.normalized_query,
            "matched_terms": normalization.matched_terms,
            "detected_categories": normalization.detected_categories,
            "detected_re_type": normalization.detected_re_type,
            "detected_citations": normalization.detected_citations,
            "detected_recordings": normalization.detected_recordings,
            "normalization_confidence": normalization.confidence,
        }

        return EngineResponse(
            query_hash=q_hash,
            response_mode=request.mode,
            confidence_score=round(confidence_score, 4),
            confidence_band=band,
            confidence_label=label,
            requires_caveat=requires_caveat,
            layer_used=layer_used.value,
            jurisdiction=jurisdiction,
            re_category=normalization.detected_re_type,
            analysis=analysis,
            citations=hardened_citations[:15],
            disclaimers=disclaimers,
            practice_tips=final_tips,
            determinism_hash=det_hash,
            trace_id=trace.trace_id,
            processing_time_ms=round(processing_time, 3),
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

    # -----------------------------------------------------------------------
    # TIE Component 12: Health endpoint data
    # -----------------------------------------------------------------------

    def get_health(self) -> Dict[str, Any]:
        """Get comprehensive engine health status."""
        telemetry_health = self._telemetry.get_health()
        doctrine_stats = get_doctrine_cache_stats()
        search_stats = self._search_index.get_stats()
        semantic_integrity = verify_dictionary_integrity()
        doctrine_integrity = verify_doctrine_integrity()

        return {
            "status": "healthy",
            "engine_id": self._engine_id,
            "engine_name": ENGINE_NAME,
            "engine_version": ENGINE_VERSION,
            "port": self._port,
            "authority": self._authority,
            "tier": ENGINE_TIER,
            "mode": ENGINE_MODE,
            "boot_time": self._boot_time,
            "query_count": self._query_count,
            "doctrine_cache": doctrine_stats,
            "doctrine_integrity": doctrine_integrity,
            "search_index": search_stats,
            "semantic_map": semantic_integrity,
            "telemetry": telemetry_health,
            "drift_registry": {
                "signal_count": len(self._drift_registry.get("signals", [])),
                "last_check": self._drift_registry.get("last_check", "never"),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


# ============================================================================
# FASTAPI APPLICATION (TIE Component 17)
# ============================================================================

_engine: Optional[RealEstateLawEngine] = None


def _load_config() -> Dict[str, Any]:
    """Load engine configuration from config.json."""
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as fh:
                return json.load(fh)
        except (json.JSONDecodeError, OSError) as exc:
            logger.warning(f"Failed to load config: {exc}. Using defaults.")
    return {
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "engine_version": ENGINE_VERSION,
        "port": ENGINE_PORT,
        "host": ENGINE_HOST,
        "engine_authority": ENGINE_AUTHORITY,
    }


def _get_engine() -> RealEstateLawEngine:
    """Get or create the engine singleton."""
    global _engine
    if _engine is None:
        config = _load_config()
        _engine = RealEstateLawEngine(config)
    return _engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # TIE Component 18: Loguru Logging
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logger.add(
        LOG_DIR / "lg08_engine.log",
        rotation="50 MB",
        retention="30 days",
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {message}",
        level="INFO",
    )
    logger.info(f"LG08 Real Estate Law Engine starting on port {ENGINE_PORT}")
    engine = _get_engine()
    logger.info(f"Engine initialized: {ENGINE_ID} v{ENGINE_VERSION}")
    yield
    logger.info("LG08 Real Estate Law Engine shutting down")


app = FastAPI(
    title=f"{ENGINE_ID} - {ENGINE_NAME}",
    description="Production-grade real estate law analysis engine with 20 TIE components",
    version=ENGINE_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


# ============================================================================
# ROUTES - Core Query
# ============================================================================

@app.post("/query", response_model=EngineResponse)
async def query_endpoint(request: QueryRequest) -> EngineResponse:
    """Main query endpoint - processes real estate law questions through the
    three-layer pipeline (doctrine cache, semantic search, deep analysis)."""
    engine = _get_engine()
    return await engine.process_query(request)


@app.post("/query/multi-doctrine")
async def multi_doctrine_endpoint(request: MultiDoctrineRequest) -> JSONResponse:
    """Multi-doctrine decomposition endpoint for complex queries spanning
    multiple real estate law areas."""
    engine = _get_engine()
    result = await engine.multi_doctrine_decomposition(request)
    return JSONResponse(content=result)


@app.post("/query/deep-analysis")
async def deep_analysis_endpoint(request: DeepAnalysisRequest) -> JSONResponse:
    """Deep analysis endpoint for comprehensive multi-faceted analysis."""
    engine = _get_engine()
    result = await engine.deep_analysis(request)
    return JSONResponse(content=result)


# ============================================================================
# ROUTES - Specialized Analysis
# ============================================================================

@app.post("/analyze/deed")
async def deed_analysis_endpoint(request: DeedAnalysisRequest) -> JSONResponse:
    """Deed type analysis and comparison endpoint."""
    engine = _get_engine()
    result = engine.analyze_deed(request)
    return JSONResponse(content=result)


@app.post("/analyze/title-chain")
async def title_chain_endpoint(request: TitleChainRequest) -> JSONResponse:
    """Title chain analysis with encumbrance detection and title opinion."""
    engine = _get_engine()
    result = engine.analyze_title_chain(request)
    return JSONResponse(content=result)


@app.post("/analyze/zoning")
async def zoning_endpoint(request: ZoningCheckRequest) -> JSONResponse:
    """Zoning compliance check endpoint."""
    engine = _get_engine()
    result = engine.analyze_zoning(request)
    return JSONResponse(content=result)


@app.post("/analyze/1031-exchange")
async def exchange_1031_endpoint(request: Exchange1031Request) -> JSONResponse:
    """IRC Section 1031 exchange validation endpoint."""
    engine = _get_engine()
    result = engine.validate_1031_exchange(request)
    return JSONResponse(content=result)


@app.post("/analyze/checklist")
async def checklist_endpoint(request: TransactionChecklistRequest) -> JSONResponse:
    """Transaction due diligence checklist generator."""
    engine = _get_engine()
    result = engine.generate_checklist(request)
    return JSONResponse(content=result)


@app.post("/analyze/fact-fragility")
async def fact_fragility_endpoint(request: FactFragilityRequest) -> JSONResponse:
    """Fact fragility scoring endpoint."""
    engine = _get_engine()
    result = engine.score_fact_fragility(request)
    return JSONResponse(content=result)


# ============================================================================
# ROUTES - Doctrine Management
# ============================================================================

@app.get("/doctrines")
async def list_doctrines() -> JSONResponse:
    """List all available doctrine topics."""
    topics = get_all_doctrine_topics()
    categories = get_all_doctrine_categories()
    return JSONResponse(content={
        "topics": topics,
        "categories": categories,
        "total_topics": len(topics),
        "total_categories": len(categories),
    })


@app.get("/doctrines/{topic}")
async def get_doctrine(topic: str) -> JSONResponse:
    """Get a specific doctrine block by topic."""
    block = get_doctrine_block(topic)
    if not block:
        raise HTTPException(status_code=404, detail=f"Doctrine topic '{topic}' not found")
    return JSONResponse(content=block.to_dict())


@app.get("/doctrines/category/{category}")
async def get_doctrines_by_category(category: str) -> JSONResponse:
    """Get all doctrine blocks in a category."""
    from doctrines import get_doctrine_blocks_by_category
    blocks = get_doctrine_blocks_by_category(category)
    if not blocks:
        raise HTTPException(status_code=404, detail=f"No doctrines found for category '{category}'")
    return JSONResponse(content={
        "category": category,
        "blocks": [b.to_dict() for b in blocks],
        "count": len(blocks),
    })


@app.get("/doctrines/search/{query}")
async def search_doctrines_endpoint(query: str, top_k: int = Query(5, ge=1, le=20)) -> JSONResponse:
    """Search doctrine blocks by free text."""
    results = search_doctrines(query, top_k=top_k)
    return JSONResponse(content={
        "query": query,
        "results": [b.to_dict() for b in results],
        "count": len(results),
    })


# ============================================================================
# ROUTES - Coverage & Drift (TIE Components 9, 10)
# ============================================================================

@app.get("/coverage")
async def coverage_map_endpoint() -> JSONResponse:
    """Get the full doctrine coverage map."""
    return JSONResponse(content=get_coverage_map())


@app.get("/drift")
async def drift_registry_endpoint() -> JSONResponse:
    """Get the doctrine drift registry."""
    engine = _get_engine()
    return JSONResponse(content=engine.get_drift_registry())


@app.post("/drift/signal")
async def drift_signal_endpoint(signal: DriftSignal) -> JSONResponse:
    """Record a doctrine drift signal."""
    engine = _get_engine()
    result = engine.record_drift_signal(signal)
    return JSONResponse(content=result)


@app.get("/stale")
async def stale_doctrines_endpoint(max_days: int = Query(90, ge=1, le=365)) -> JSONResponse:
    """Get stale doctrine blocks exceeding the staleness threshold."""
    stale = get_stale_doctrines(max_days)
    return JSONResponse(content={
        "threshold_days": max_days,
        "stale_blocks": [b.to_dict() for b in stale],
        "count": len(stale),
    })


# ============================================================================
# ROUTES - Telemetry & Metrics (TIE Components 8, 11)
# ============================================================================

@app.get("/metrics")
async def metrics_endpoint() -> JSONResponse:
    """Get aggregated engine metrics."""
    telemetry = get_telemetry()
    return JSONResponse(content=telemetry.get_health())


@app.get("/metrics/traces")
async def recent_traces_endpoint(count: int = Query(20, ge=1, le=100)) -> JSONResponse:
    """Get recent query traces."""
    telemetry = get_telemetry()
    return JSONResponse(content={"traces": telemetry.get_recent_traces(count)})


@app.get("/metrics/mutations")
async def recent_mutations_endpoint(count: int = Query(20, ge=1, le=100)) -> JSONResponse:
    """Get recent doctrine mutations."""
    telemetry = get_telemetry()
    return JSONResponse(content={"mutations": telemetry.get_recent_mutations(count)})


@app.get("/metrics/citations")
async def recent_citations_endpoint(count: int = Query(20, ge=1, le=100)) -> JSONResponse:
    """Get recent citation lookups."""
    telemetry = get_telemetry()
    return JSONResponse(content={"citations": telemetry.get_recent_citations(count)})


@app.get("/metrics/errors")
async def recent_errors_endpoint() -> JSONResponse:
    """Get recent errors."""
    telemetry = get_telemetry()
    return JSONResponse(content={"errors": telemetry._errors.get_recent(20), "stats": telemetry._errors.get_stats()})


# ============================================================================
# ROUTES - Audit Trail (TIE Component 15)
# ============================================================================

@app.get("/audit/verify")
async def audit_verify_endpoint() -> JSONResponse:
    """Verify the audit trail hash chain integrity."""
    telemetry = get_telemetry()
    result = telemetry.verify_audit_chain()
    return JSONResponse(content=result)


@app.get("/audit/stats")
async def audit_stats_endpoint() -> JSONResponse:
    """Get audit trail statistics."""
    telemetry = get_telemetry()
    return JSONResponse(content=telemetry._audit.get_stats())


# ============================================================================
# ROUTES - Semantic Map
# ============================================================================

@app.get("/semantic/map")
async def semantic_map_endpoint() -> JSONResponse:
    """Get the semantic normalization map."""
    sem_map = get_semantic_map()
    return JSONResponse(content={
        "version": get_semantic_map_version(),
        "term_count": len(sem_map),
        "hash": get_semantic_map_hash(),
        "categories": list(set(v["category"] for v in sem_map.values())),
    })


@app.get("/semantic/normalize")
async def semantic_normalize_endpoint(query: str = Query(..., min_length=3)) -> JSONResponse:
    """Normalize a query through the semantic map."""
    result = normalize_query(query)
    return JSONResponse(content=result.to_dict())


@app.get("/semantic/jurisdictions")
async def jurisdictions_endpoint() -> JSONResponse:
    """Get the jurisdiction mapping data."""
    return JSONResponse(content=get_jurisdiction_map())


@app.get("/semantic/integrity")
async def semantic_integrity_endpoint() -> JSONResponse:
    """Verify semantic dictionary integrity."""
    return JSONResponse(content=verify_dictionary_integrity())


# ============================================================================
# ROUTES - Health (TIE Component 12)
# ============================================================================

@app.get("/health")
async def health_endpoint() -> JSONResponse:
    """Comprehensive engine health check."""
    engine = _get_engine()
    return JSONResponse(content=engine.get_health())


@app.get("/")
async def root_endpoint() -> JSONResponse:
    """Root endpoint - engine identity and status."""
    return JSONResponse(content={
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "engine_version": ENGINE_VERSION,
        "port": ENGINE_PORT,
        "tier": ENGINE_TIER,
        "authority": ENGINE_AUTHORITY,
        "mode": ENGINE_MODE,
        "status": "operational",
        "endpoints": [
            "/query", "/query/multi-doctrine", "/query/deep-analysis",
            "/analyze/deed", "/analyze/title-chain", "/analyze/zoning",
            "/analyze/1031-exchange", "/analyze/checklist", "/analyze/fact-fragility",
            "/doctrines", "/doctrines/{topic}", "/doctrines/category/{category}",
            "/doctrines/search/{query}",
            "/coverage", "/drift", "/drift/signal", "/stale",
            "/metrics", "/metrics/traces", "/metrics/mutations",
            "/metrics/citations", "/metrics/errors",
            "/audit/verify", "/audit/stats",
            "/semantic/map", "/semantic/normalize", "/semantic/jurisdictions",
            "/semantic/integrity",
            "/health",
        ],
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })


# ============================================================================
# CONFIGURATION ENDPOINT
# ============================================================================

@app.get("/config")
async def config_endpoint() -> JSONResponse:
    """Get the current engine configuration (non-sensitive fields)."""
    config = _load_config()
    safe_config = {
        "engine_id": config.get("engine_id"),
        "engine_name": config.get("engine_name"),
        "engine_version": config.get("engine_version"),
        "port": config.get("port"),
        "engine_authority": config.get("engine_authority"),
        "engine_tier": config.get("engine_tier"),
        "engine_mode": config.get("engine_mode"),
        "real_estate_categories": list(config.get("real_estate_categories", {}).keys()),
        "response_modes": list(config.get("response_modes", {}).keys()),
        "confidence_bands": list(config.get("confidence_bands", {}).keys()),
    }
    return JSONResponse(content=safe_config)


# ============================================================================
# INTEGRITY ENDPOINT
# ============================================================================

@app.get("/integrity")
async def integrity_endpoint() -> JSONResponse:
    """Full integrity verification of all engine components."""
    doctrine = verify_doctrine_integrity()
    semantic = verify_dictionary_integrity()
    telemetry = get_telemetry()
    audit = telemetry.verify_audit_chain()
    cache_hash = get_doctrine_cache_hash()
    semantic_hash = get_semantic_map_hash()

    return JSONResponse(content={
        "engine_id": ENGINE_ID,
        "engine_version": ENGINE_VERSION,
        "doctrine_cache": doctrine,
        "semantic_map": semantic,
        "audit_chain": audit,
        "hashes": {
            "doctrine_cache": cache_hash,
            "semantic_map": semantic_hash,
        },
        "overall_valid": doctrine["valid"] and semantic["valid"] and audit["chain_valid"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })


# ============================================================================
# ADVANCED TITLE OPINION GENERATOR
# ============================================================================

class TitleOpinionGenerator:
    """Generates structured title opinions from chain of title data
    with requirement scheduling, exception analysis, and risk scoring.

    Implements a multi-step title examination workflow:
    1. Chain continuity verification
    2. Encumbrance identification and classification
    3. Lien priority analysis
    4. Exception categorization (standard vs. special)
    5. Requirement formulation
    6. Marketability determination
    7. Insurability assessment
    8. Risk scoring and recommendation
    """

    STANDARD_EXCEPTIONS: ClassVar[List[Dict[str, str]]] = [
        {
            "exception": "Rights or claims of parties in possession not shown by the public records",
            "type": "standard",
            "cure": "Survey and physical inspection of the property",
        },
        {
            "exception": "Encroachments, overlaps, boundary line disputes, or other matters that would be disclosed by an accurate survey",
            "type": "standard",
            "cure": "Obtain current ALTA/NSPS land title survey",
        },
        {
            "exception": "Easements or claims of easements not shown by the public records",
            "type": "standard",
            "cure": "Physical inspection and survey; title company affidavit",
        },
        {
            "exception": "Any lien for real estate taxes or assessments not yet due and payable",
            "type": "standard",
            "cure": "Tax certificate showing current status",
        },
        {
            "exception": "Any lien or right to a lien for services, labor, or materials",
            "type": "standard",
            "cure": "Lien waiver affidavit from seller; inspection for recent improvements",
        },
        {
            "exception": "Defects, liens, encumbrances, or other matters created by or against the insured after the date of policy",
            "type": "standard",
            "cure": "N/A - post-policy matters excluded",
        },
        {
            "exception": "Water rights, claims, or title to water",
            "type": "standard",
            "cure": "Water rights search in applicable jurisdictions",
        },
        {
            "exception": "Mineral reservations and rights of third parties in subsurface minerals",
            "type": "standard",
            "cure": "Mineral title opinion; verify mineral estate ownership",
        },
    ]

    REQUIREMENT_TEMPLATES: ClassVar[Dict[str, Dict[str, str]]] = {
        "unreleased_mortgage": {
            "description": "Obtain and record release/satisfaction of mortgage/DOT",
            "priority": "critical",
            "typical_timeline": "5-10 business days",
            "responsible_party": "Seller/Seller's Lender",
        },
        "gap_in_chain": {
            "description": "Obtain corrective deed or affidavit to bridge chain of title gap",
            "priority": "critical",
            "typical_timeline": "10-30 business days",
            "responsible_party": "Seller",
        },
        "judgment_lien": {
            "description": "Obtain release of judgment or pay judgment at closing",
            "priority": "high",
            "typical_timeline": "5-15 business days",
            "responsible_party": "Seller",
        },
        "tax_lien": {
            "description": "Pay delinquent taxes and obtain certificate of satisfaction",
            "priority": "critical",
            "typical_timeline": "3-10 business days",
            "responsible_party": "Seller",
        },
        "mechanics_lien": {
            "description": "Obtain lien release or post bond to discharge mechanics lien",
            "priority": "high",
            "typical_timeline": "10-20 business days",
            "responsible_party": "Seller/Contractor",
        },
        "probate_required": {
            "description": "Complete probate proceedings to establish authority to convey",
            "priority": "critical",
            "typical_timeline": "30-180 days",
            "responsible_party": "Estate representative",
        },
        "spousal_joinder": {
            "description": "Obtain joinder of spouse on conveyance document",
            "priority": "critical",
            "typical_timeline": "At closing",
            "responsible_party": "Seller and Spouse",
        },
        "entity_authority": {
            "description": "Provide corporate resolution, partnership agreement, or trust certificate authorizing sale",
            "priority": "high",
            "typical_timeline": "5-10 business days",
            "responsible_party": "Entity Seller",
        },
        "survey_required": {
            "description": "Obtain current ALTA/NSPS land title survey",
            "priority": "medium",
            "typical_timeline": "10-21 business days",
            "responsible_party": "Buyer (usually)",
        },
        "hoa_estoppel": {
            "description": "Obtain HOA estoppel letter or clearance certificate",
            "priority": "medium",
            "typical_timeline": "5-15 business days",
            "responsible_party": "Seller",
        },
    }

    def __init__(self) -> None:
        self._title_analyzer = get_title_analyzer()
        logger.info("TitleOpinionGenerator initialized")

    def generate_opinion(
        self,
        chain_data: Optional[List[Dict[str, Any]]] = None,
        property_description: Optional[str] = None,
        jurisdiction: str = "TX",
        opinion_type: str = "preliminary",
    ) -> Dict[str, Any]:
        """Generate a structured title opinion."""
        chain = self._title_analyzer.analyze_chain(chain_data)
        encumbrances = self._title_analyzer.identify_encumbrances(chain)

        # Step 1: Chain analysis
        chain_issues = self._analyze_chain_continuity(chain)

        # Step 2: Encumbrance classification
        classified_encumbrances = self._classify_encumbrances(encumbrances)

        # Step 3: Lien priority
        lien_priority = self._determine_lien_priority(encumbrances)

        # Step 4: Exception categorization
        exceptions = self._categorize_exceptions(chain, encumbrances)

        # Step 5: Requirements
        requirements = self._formulate_requirements(chain_issues, classified_encumbrances)

        # Step 6: Marketability
        marketability = self._assess_marketability(chain_issues, classified_encumbrances, requirements)

        # Step 7: Insurability
        insurability = self._assess_insurability(chain_issues, classified_encumbrances)

        # Step 8: Risk score
        risk_score = self._compute_risk_score(chain_issues, classified_encumbrances, requirements)

        current_owner = chain[-1].grantee if chain else "Unknown"
        vesting_type = self._determine_vesting(chain[-1]) if chain else "Unknown"

        return {
            "opinion_type": opinion_type,
            "jurisdiction": jurisdiction,
            "property_description": property_description or "See attached legal description",
            "effective_date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "current_owner": current_owner,
            "vesting_type": vesting_type,
            "chain_of_title": {
                "entries": [e.to_dict() for e in chain],
                "total_instruments": len(chain),
                "issues": chain_issues,
            },
            "encumbrances": classified_encumbrances,
            "lien_priority": lien_priority,
            "exceptions": exceptions,
            "requirements": requirements,
            "marketability": marketability,
            "insurability": insurability,
            "risk_assessment": risk_score,
            "opinion_conclusion": self._draft_conclusion(marketability, insurability, requirements, risk_score),
            "disclaimers": [
                REQUIRED_DISCLAIMERS["not_legal_advice"],
                REQUIRED_DISCLAIMERS["title_caveat"],
                REQUIRED_DISCLAIMERS["jurisdiction_specific"],
            ],
        }

    def _analyze_chain_continuity(self, chain: List[TitleChainEntry]) -> List[Dict[str, Any]]:
        """Analyze chain of title for continuity issues."""
        issues: List[Dict[str, Any]] = []
        for i, entry in enumerate(chain):
            for issue in entry.issues_detected:
                issues.append({
                    "instrument": entry.instrument_number,
                    "issue_type": issue,
                    "description": self._describe_issue(issue, entry),
                    "severity": self._rate_issue_severity(issue),
                    "cure_available": True,
                    "cure_method": self._suggest_cure(issue, entry),
                })
        return issues

    def _classify_encumbrances(self, encumbrances: List[EncumbranceRecord]) -> List[Dict[str, Any]]:
        """Classify encumbrances by type and impact."""
        classified: List[Dict[str, Any]] = []
        for enc in encumbrances:
            classified.append({
                **enc.to_dict(),
                "classification": self._get_encumbrance_class(enc.encumbrance_type),
                "impact_on_closing": self._assess_closing_impact(enc),
                "estimated_cost_to_cure": self._estimate_cure_cost(enc),
            })
        return classified

    def _determine_lien_priority(self, encumbrances: List[EncumbranceRecord]) -> List[Dict[str, Any]]:
        """Determine lien priority order."""
        priority_list: List[Dict[str, Any]] = []
        for enc in sorted(encumbrances, key=lambda e: e.priority_position):
            priority_list.append({
                "position": enc.priority_position,
                "type": enc.encumbrance_type,
                "holder": enc.holder,
                "amount": enc.amount,
                "status": enc.status,
                "priority_basis": self._explain_priority(enc),
            })
        return priority_list

    def _categorize_exceptions(
        self,
        chain: List[TitleChainEntry],
        encumbrances: List[EncumbranceRecord],
    ) -> Dict[str, Any]:
        """Categorize title exceptions as standard or special."""
        special_exceptions: List[Dict[str, str]] = []
        for enc in encumbrances:
            if enc.status == "active" and enc.affects_marketability:
                special_exceptions.append({
                    "exception": f"{enc.encumbrance_type}: {enc.description}",
                    "type": "special",
                    "reference": enc.recorded_reference,
                    "cure": enc.cure_method or "Contact title company for cure options",
                })
        for entry in chain:
            for issue in entry.issues_detected:
                if issue not in ("limited_warranty_only",):
                    special_exceptions.append({
                        "exception": f"Chain issue at {entry.instrument_number}: {issue}",
                        "type": "special",
                        "reference": entry.instrument_number,
                        "cure": self._suggest_cure(issue, entry),
                    })

        return {
            "standard_exceptions": self.STANDARD_EXCEPTIONS,
            "special_exceptions": special_exceptions,
            "total_standard": len(self.STANDARD_EXCEPTIONS),
            "total_special": len(special_exceptions),
        }

    def _formulate_requirements(
        self,
        chain_issues: List[Dict[str, Any]],
        encumbrances: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """Formulate requirements that must be satisfied before closing."""
        requirements: List[Dict[str, Any]] = []
        req_id = 1

        for issue in chain_issues:
            issue_type = issue.get("issue_type", "")
            template = self.REQUIREMENT_TEMPLATES.get(issue_type, self.REQUIREMENT_TEMPLATES.get("gap_in_chain", {}))
            requirements.append({
                "requirement_id": f"REQ-{req_id:03d}",
                "description": template.get("description", f"Resolve issue: {issue_type}"),
                "priority": template.get("priority", "high"),
                "timeline": template.get("typical_timeline", "TBD"),
                "responsible_party": template.get("responsible_party", "Seller"),
                "status": "open",
                "related_instrument": issue.get("instrument", ""),
            })
            req_id += 1

        for enc in encumbrances:
            if enc.get("status") == "active" and enc.get("affects_marketability"):
                enc_type = enc.get("encumbrance_type", "unknown")
                template = self.REQUIREMENT_TEMPLATES.get(
                    "unreleased_mortgage" if "mortgage" in enc_type else "judgment_lien",
                    self.REQUIREMENT_TEMPLATES["unreleased_mortgage"],
                )
                requirements.append({
                    "requirement_id": f"REQ-{req_id:03d}",
                    "description": template.get("description", f"Resolve encumbrance: {enc_type}"),
                    "priority": template.get("priority", "high"),
                    "timeline": template.get("typical_timeline", "TBD"),
                    "responsible_party": template.get("responsible_party", "Seller"),
                    "status": "open",
                    "related_encumbrance": enc.get("recorded_reference", ""),
                })
                req_id += 1

        return requirements

    def _assess_marketability(
        self,
        chain_issues: List[Dict[str, Any]],
        encumbrances: List[Dict[str, Any]],
        requirements: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Assess whether title is marketable."""
        critical_issues = [i for i in chain_issues if i.get("severity") == "critical"]
        active_encumbrances = [e for e in encumbrances if e.get("status") == "active" and e.get("affects_marketability")]
        critical_requirements = [r for r in requirements if r.get("priority") == "critical"]

        is_marketable = len(critical_issues) == 0 and len(active_encumbrances) == 0
        can_be_made_marketable = len(critical_issues) <= 2 and all(
            i.get("cure_available", False) for i in chain_issues
        )

        return {
            "currently_marketable": is_marketable,
            "can_be_made_marketable": can_be_made_marketable,
            "critical_issues": len(critical_issues),
            "active_encumbrances": len(active_encumbrances),
            "critical_requirements": len(critical_requirements),
            "assessment": (
                "Title appears marketable subject to standard exceptions."
                if is_marketable
                else f"Title is NOT currently marketable. {len(critical_requirements)} critical requirements must be satisfied."
                if can_be_made_marketable
                else "Title has significant issues that may prevent closing. Extensive curative work required."
            ),
        }

    def _assess_insurability(
        self,
        chain_issues: List[Dict[str, Any]],
        encumbrances: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Assess whether title is insurable."""
        critical_count = sum(1 for i in chain_issues if i.get("severity") == "critical")
        active_count = sum(1 for e in encumbrances if e.get("status") == "active")

        is_insurable = critical_count <= 1 and active_count <= 2
        with_exceptions = critical_count <= 2

        return {
            "insurable": is_insurable,
            "insurable_with_exceptions": with_exceptions,
            "exceptions_required": active_count + critical_count,
            "assessment": (
                "Title appears insurable under standard ALTA owner's policy."
                if is_insurable
                else "Title may be insurable with special exceptions noted in Schedule B."
                if with_exceptions
                else "Title insurability uncertain. Curative work recommended before seeking title insurance."
            ),
        }

    def _compute_risk_score(
        self,
        chain_issues: List[Dict[str, Any]],
        encumbrances: List[Dict[str, Any]],
        requirements: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Compute overall title risk score (0-100, lower is better)."""
        score = 0
        for issue in chain_issues:
            severity = issue.get("severity", "medium")
            if severity == "critical":
                score += 25
            elif severity == "high":
                score += 15
            elif severity == "medium":
                score += 8
            else:
                score += 3

        for enc in encumbrances:
            if enc.get("status") == "active" and enc.get("affects_marketability"):
                score += 20

        for req in requirements:
            if req.get("priority") == "critical":
                score += 10
            elif req.get("priority") == "high":
                score += 5

        score = min(score, 100)

        if score <= 15:
            risk_level = "LOW"
            recommendation = "Title risk is low. Standard closing procedures should be sufficient."
        elif score <= 40:
            risk_level = "MODERATE"
            recommendation = "Title has moderate risk. Ensure all requirements are satisfied before closing."
        elif score <= 70:
            risk_level = "HIGH"
            recommendation = "Title risk is elevated. Consider extended title insurance coverage and legal review."
        else:
            risk_level = "CRITICAL"
            recommendation = "Title risk is critical. Do not proceed without comprehensive curative work and legal counsel review."

        return {
            "risk_score": score,
            "risk_level": risk_level,
            "recommendation": recommendation,
            "factors": {
                "chain_issues": len(chain_issues),
                "active_encumbrances": sum(1 for e in encumbrances if e.get("status") == "active"),
                "open_requirements": len(requirements),
            },
        }

    def _draft_conclusion(
        self,
        marketability: Dict[str, Any],
        insurability: Dict[str, Any],
        requirements: List[Dict[str, Any]],
        risk: Dict[str, Any],
    ) -> str:
        """Draft the opinion conclusion."""
        parts: List[str] = []
        if marketability["currently_marketable"]:
            parts.append("Based on the examination of the chain of title, the title appears to be marketable subject to the standard exceptions noted herein.")
        else:
            parts.append(f"The title is NOT currently marketable. {len(requirements)} requirement(s) must be satisfied before closing.")

        if insurability["insurable"]:
            parts.append("The title appears insurable under a standard ALTA owner's policy.")
        elif insurability["insurable_with_exceptions"]:
            parts.append("The title may be insurable with special exceptions as noted.")

        parts.append(f"Overall risk assessment: {risk['risk_level']} (score: {risk['risk_score']}/100).")
        parts.append(risk["recommendation"])

        return " ".join(parts)

    def _describe_issue(self, issue_type: str, entry: TitleChainEntry) -> str:
        """Generate a human-readable description of a chain issue."""
        descriptions: Dict[str, str] = {
            "gap_in_chain": f"Missing link between consecutive owners at instrument {entry.instrument_number}. The grantee of the prior instrument does not match the grantor of this instrument.",
            "limited_warranty_only": f"Instrument {entry.instrument_number} is a special warranty deed providing limited protection. Pre-ownership defects are not warranted.",
            "no_warranty_protection": f"Instrument {entry.instrument_number} is a quitclaim deed with no warranty protection. All title risk falls on the grantee.",
        }
        return descriptions.get(issue_type, f"Issue '{issue_type}' detected at instrument {entry.instrument_number}")

    def _rate_issue_severity(self, issue_type: str) -> str:
        """Rate the severity of a chain issue."""
        severity_map: Dict[str, str] = {
            "gap_in_chain": "critical",
            "no_warranty_protection": "high",
            "limited_warranty_only": "medium",
            "missing_spousal_joinder": "critical",
            "defective_acknowledgment": "high",
            "unreleased_lien": "high",
        }
        return severity_map.get(issue_type, "medium")

    def _suggest_cure(self, issue_type: str, entry: TitleChainEntry) -> str:
        """Suggest a cure for a chain issue."""
        cures: Dict[str, str] = {
            "gap_in_chain": f"Obtain a corrective deed from the prior grantee to {entry.grantor}, or an affidavit of identity if the parties are the same person.",
            "limited_warranty_only": "Obtain enhanced title insurance endorsement to cover pre-ownership defects.",
            "no_warranty_protection": "Obtain title insurance with enhanced coverage. Consider quiet title action if concerns exist.",
            "missing_spousal_joinder": "Obtain joinder deed from the non-joining spouse or evidence the property is separate property.",
            "defective_acknowledgment": "Obtain a re-acknowledged deed or corrective affidavit from the notary.",
        }
        return cures.get(issue_type, "Consult with title company or real estate attorney for appropriate cure.")

    def _determine_vesting(self, entry: TitleChainEntry) -> str:
        """Determine the vesting type from the last chain entry."""
        grantee = entry.grantee.lower()
        if "&" in grantee or "and" in grantee:
            if "husband and wife" in grantee or "h/w" in grantee:
                return "Community Property (married couple)"
            return "Joint Tenants or Tenants in Common"
        if "llc" in grantee or "inc" in grantee or "corp" in grantee:
            return "Entity Ownership"
        if "trust" in grantee:
            return "Trust Ownership"
        return "Individual Ownership (sole)"

    def _get_encumbrance_class(self, enc_type: str) -> str:
        """Classify an encumbrance type."""
        class_map: Dict[str, str] = {
            "mortgage_lien": "voluntary_lien",
            "mechanics_lien": "involuntary_lien",
            "tax_lien": "statutory_lien",
            "judgment_lien": "involuntary_lien",
            "lis_pendens": "notice_of_litigation",
            "easement": "non_monetary_encumbrance",
            "restrictive_covenant": "non_monetary_encumbrance",
        }
        return class_map.get(enc_type, "other")

    def _assess_closing_impact(self, enc: EncumbranceRecord) -> str:
        """Assess the impact of an encumbrance on closing."""
        if enc.encumbrance_type in ("mortgage_lien",) and enc.status == "active":
            return "Must be satisfied at closing from sale proceeds"
        if enc.encumbrance_type in ("tax_lien",):
            return "Must be paid before or at closing; senior lien position"
        if enc.encumbrance_type in ("mechanics_lien",):
            return "Must be released or bonded before closing"
        if enc.encumbrance_type in ("lis_pendens",):
            return "May cloud title; must be resolved or insured around"
        return "Review impact with title company"

    def _estimate_cure_cost(self, enc: EncumbranceRecord) -> str:
        """Estimate the cost to cure an encumbrance."""
        if enc.amount:
            return f"Approximately ${enc.amount:,.2f} plus recording fees and interest"
        return "Amount TBD - obtain payoff statement"


# ============================================================================
# HOMESTEAD ANALYSIS MODULE
# ============================================================================

class HomesteadAnalyzer:
    """Analyzes Texas homestead exemption applicability and protection.

    Implements constitutional homestead analysis under Texas
    Constitution Article XVI, Sections 50 and 51, and
    Texas Property Code Chapter 41.
    """

    PERMITTED_LIENS: ClassVar[List[Dict[str, str]]] = [
        {"type": "purchase_money", "description": "Purchase money mortgage or deed of trust used to acquire the homestead", "constitutional_basis": "Art. XVI, SS 50(a)(1)"},
        {"type": "property_tax", "description": "Property tax liens and assessments", "constitutional_basis": "Art. XVI, SS 50(a)(2)"},
        {"type": "home_improvement", "description": "Mechanic's or materialman's lien for work/materials on the homestead", "constitutional_basis": "Art. XVI, SS 50(a)(5)"},
        {"type": "home_equity", "description": "Home equity loan (subject to strict constitutional requirements)", "constitutional_basis": "Art. XVI, SS 50(a)(6)"},
        {"type": "reverse_mortgage", "description": "Reverse mortgage for homeowner age 62+", "constitutional_basis": "Art. XVI, SS 50(a)(7)"},
        {"type": "owelty_of_partition", "description": "Partition lien in divorce or probate", "constitutional_basis": "Art. XVI, SS 50(a)(3)"},
        {"type": "refinance", "description": "Refinancing of existing liens on homestead", "constitutional_basis": "Art. XVI, SS 50(a)(4)"},
        {"type": "federal_tax_lien", "description": "Federal tax lien (IRS) - not subject to state homestead protection due to Supremacy Clause", "constitutional_basis": "Supremacy Clause / 26 USC 6321"},
    ]

    HOME_EQUITY_REQUIREMENTS: ClassVar[List[Dict[str, str]]] = [
        {"requirement": "80% LTV maximum", "description": "Loan cannot exceed 80% of fair market value of the homestead at time of closing"},
        {"requirement": "No personal liability", "description": "Borrower is not personally liable on the note (non-recourse in effect)"},
        {"requirement": "Single lump sum advance", "description": "Proceeds must be disbursed in a single lump sum (HELOC exception under SS 50(t))"},
        {"requirement": "12-day waiting period", "description": "Loan cannot close earlier than 12 days after application"},
        {"requirement": "One day before closing", "description": "Final closing disclosure must be provided at least one day before closing"},
        {"requirement": "3% fee cap", "description": "Total fees (excluding certain items) cannot exceed 3% of the original principal balance"},
        {"requirement": "Title company closing", "description": "Must close at the office of a title company, attorney, or lender"},
        {"requirement": "Right of rescission", "description": "Borrower has 3 days to rescind after closing"},
        {"requirement": "One at a time", "description": "Only one home equity loan may be outstanding on the homestead at a time"},
        {"requirement": "Once per year", "description": "Homestead cannot be encumbered by more than one home equity loan in a 12-month period"},
    ]

    def __init__(self) -> None:
        logger.info("HomesteadAnalyzer initialized")

    def analyze_homestead(
        self,
        property_type: str,
        location: str,
        acreage: float,
        is_primary_residence: bool,
        marital_status: str,
        proposed_lien_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Analyze homestead exemption applicability."""
        is_urban = location.lower() in ("urban", "city", "town", "municipality")
        max_acreage = 10.0 if is_urban else (200.0 if marital_status.lower() in ("married", "family") else 100.0)
        qualifies = is_primary_residence and acreage <= max_acreage

        # Lien analysis
        lien_analysis: Optional[Dict[str, Any]] = None
        if proposed_lien_type:
            lien_analysis = self._analyze_proposed_lien(proposed_lien_type, qualifies)

        # Tax exemption analysis
        tax_exemption = self._analyze_tax_exemption(is_primary_residence, marital_status)

        return {
            "qualifies_as_homestead": qualifies,
            "property_type": property_type,
            "location_type": "urban" if is_urban else "rural",
            "acreage": acreage,
            "max_acreage_allowed": max_acreage,
            "acreage_within_limits": acreage <= max_acreage,
            "is_primary_residence": is_primary_residence,
            "marital_status": marital_status,
            "forced_sale_protection": qualifies,
            "permitted_liens": self.PERMITTED_LIENS,
            "proposed_lien_analysis": lien_analysis,
            "tax_exemption": tax_exemption,
            "constitutional_basis": "Tex. Const. Art. XVI, SS 50-51",
            "statutory_basis": "Tex. Prop. Code Ch. 41",
            "practice_note": (
                "Texas homestead protection is automatic and does not require filing, "
                "though a homestead designation may be filed with the county clerk. "
                "Both spouses must join in any conveyance or encumbrance of the homestead."
            ),
        }

    def _analyze_proposed_lien(self, lien_type: str, is_homestead: bool) -> Dict[str, Any]:
        """Analyze whether a proposed lien can attach to the homestead."""
        lien_lower = lien_type.lower()
        permitted = False
        constitutional_basis = ""
        requirements: List[Dict[str, str]] = []
        warnings: List[str] = []

        for permitted_lien in self.PERMITTED_LIENS:
            if permitted_lien["type"] in lien_lower or lien_lower in permitted_lien["type"]:
                permitted = True
                constitutional_basis = permitted_lien["constitutional_basis"]
                if "home_equity" in lien_lower:
                    requirements = self.HOME_EQUITY_REQUIREMENTS
                    warnings.append("Home equity loans on Texas homesteads are subject to the most restrictive requirements of any state. Strict compliance is mandatory.")
                break

        if not permitted and is_homestead:
            warnings.append(f"The proposed lien type '{lien_type}' is NOT a permitted homestead lien under the Texas Constitution. The lien would be VOID if placed on homestead property.")

        return {
            "lien_type": lien_type,
            "permitted_on_homestead": permitted,
            "constitutional_basis": constitutional_basis,
            "special_requirements": requirements,
            "warnings": warnings,
            "recommendation": (
                "Lien may be placed on homestead if all requirements are met."
                if permitted
                else "STOP - This lien type cannot be placed on Texas homestead property."
            ),
        }

    def _analyze_tax_exemption(self, is_primary_residence: bool, marital_status: str) -> Dict[str, Any]:
        """Analyze property tax homestead exemption."""
        exemptions: List[Dict[str, Any]] = []

        if is_primary_residence:
            exemptions.append({
                "type": "General Homestead",
                "amount": "$100,000",
                "applies_to": "School district taxes",
                "statutory_basis": "Tex. Tax Code SS 11.13(b)",
                "filing_deadline": "April 30 (one-time filing)",
            })
            exemptions.append({
                "type": "Optional Homestead",
                "amount": "Up to 20% of appraised value (varies by taxing unit)",
                "applies_to": "City, county, and special district taxes (if adopted)",
                "statutory_basis": "Tex. Tax Code SS 11.13(n)",
                "filing_deadline": "April 30",
            })

        return {
            "eligible": is_primary_residence,
            "exemptions": exemptions,
            "total_exemption_types": len(exemptions),
            "appraisal_cap": "10% annual increase cap for homestead properties (Tex. Tax Code SS 23.23)",
            "additional_exemptions": [
                "Over 65 or Disabled: Additional $10,000 school exemption + tax freeze",
                "Disabled Veteran: Up to 100% exemption based on disability rating",
                "Surviving Spouse of Veteran: May inherit 100% exemption",
            ],
        }


# ============================================================================
# MINERAL RIGHTS ANALYZER
# ============================================================================

class MineralRightsAnalyzer:
    """Analyzes mineral rights, surface-mineral estate conflicts,
    and oil and gas lease issues specific to Texas and the Permian Basin.

    Implements the accommodation doctrine analysis from Getty Oil v. Jones
    and evaluates common mineral rights disputes.
    """

    MINERAL_INTEREST_TYPES: ClassVar[Dict[str, Dict[str, str]]] = {
        "royalty_interest": {
            "description": "Right to receive a share of production (typically 1/8 to 1/4) free of production costs",
            "cost_bearing": "No - free of production costs",
            "executive_right": "No - cannot execute leases",
            "transferable": "Yes - freely transferable",
        },
        "overriding_royalty": {
            "description": "Royalty interest carved out of the working interest in a lease, not derived from mineral ownership",
            "cost_bearing": "No - free of production costs",
            "executive_right": "No",
            "transferable": "Yes - but terminates with the lease",
        },
        "working_interest": {
            "description": "Right to develop and operate minerals, bearing proportionate share of costs",
            "cost_bearing": "Yes - bears proportionate share of drilling and operating costs",
            "executive_right": "Typically yes - can execute leases",
            "transferable": "Yes - freely transferable",
        },
        "nonparticipating_royalty": {
            "description": "Royalty interest that does not include the right to lease or participate in lease bonus",
            "cost_bearing": "No",
            "executive_right": "No - cannot execute leases or receive bonus",
            "transferable": "Yes",
        },
        "executive_right": {
            "description": "Right to execute oil and gas leases on behalf of mineral owners",
            "cost_bearing": "N/A",
            "executive_right": "Yes - defines this interest type",
            "transferable": "Yes - can be severed from mineral estate",
        },
    }

    def __init__(self) -> None:
        logger.info("MineralRightsAnalyzer initialized")

    def analyze_mineral_interest(
        self,
        interest_type: str,
        fraction: Optional[str] = None,
        surface_owner_same: bool = False,
    ) -> Dict[str, Any]:
        """Analyze a mineral interest type and its characteristics."""
        info = self.MINERAL_INTEREST_TYPES.get(interest_type.lower().replace(" ", "_"))
        if not info:
            return {
                "interest_type": interest_type,
                "recognized": False,
                "message": f"Interest type '{interest_type}' not recognized. Known types: {list(self.MINERAL_INTEREST_TYPES.keys())}",
            }

        return {
            "interest_type": interest_type,
            "recognized": True,
            "details": info,
            "fraction": fraction,
            "surface_owner_same": surface_owner_same,
            "split_estate": not surface_owner_same,
            "accommodation_doctrine_applies": not surface_owner_same,
            "key_cases": [
                "Getty Oil Co. v. Jones, 470 S.W.2d 618 (Tex. 1971) - accommodation doctrine",
                "Moser v. US Steel Corp., 676 S.W.2d 99 (Tex. 1984) - executive duty",
                "French v. Chevron U.S.A., Inc., 896 S.W.2d 795 (Tex. 1995) - royalty calculation",
            ],
            "practical_considerations": self._get_practical_considerations(interest_type, surface_owner_same),
        }

    def analyze_accommodation_doctrine(
        self,
        surface_use: str,
        mineral_operation: str,
        alternative_means_available: bool,
    ) -> Dict[str, Any]:
        """Analyze whether the accommodation doctrine applies."""
        doctrine_applies = not alternative_means_available is False

        return {
            "surface_use": surface_use,
            "mineral_operation": mineral_operation,
            "alternative_means_available": alternative_means_available,
            "accommodation_required": alternative_means_available,
            "analysis": {
                "mineral_estate_dominant": True,
                "implied_surface_use_right": True,
                "reasonably_necessary_test": "Mineral owner may use surface to the extent reasonably necessary for mineral operations",
                "accommodation_test": (
                    "When the mineral owner has reasonable alternative means of accessing the minerals, "
                    "the mineral owner must accommodate existing surface uses (Getty Oil v. Jones)."
                    if alternative_means_available
                    else "If no reasonable alternative means exist, the mineral estate's dominance prevails "
                    "and the surface owner must yield."
                ),
            },
            "recommendation": (
                f"The mineral operator should accommodate the existing surface use ('{surface_use}') "
                f"because alternative means of conducting '{mineral_operation}' are available."
                if alternative_means_available
                else f"The mineral operator may proceed with '{mineral_operation}' using the surface, "
                f"as no reasonable alternative means are available. Surface owner should negotiate a surface use agreement."
            ),
            "key_cases": [
                "Getty Oil Co. v. Jones, 470 S.W.2d 618 (Tex. 1971)",
                "Merriman v. XTO Energy Inc., 407 S.W.3d 244 (Tex. 2013)",
            ],
            "surface_damage_statute": "Tex. Nat. Res. Code SS 91.751-91.757 may require compensation for surface damages in certain circumstances.",
        }

    def _get_practical_considerations(self, interest_type: str, surface_same: bool) -> List[str]:
        """Get practical considerations for a mineral interest type."""
        considerations: List[str] = []
        if "royalty" in interest_type.lower():
            considerations.append("Verify royalty fraction and whether it is a fixed or floating royalty")
            considerations.append("Confirm whether the royalty is calculated on gross production or net of post-production costs")
            considerations.append("Check for minimum royalty or shut-in royalty provisions in the lease")
        if "working" in interest_type.lower():
            considerations.append("Working interest holders are liable for their proportionate share of all drilling and operating costs")
            considerations.append("Verify operator status and joint operating agreement terms")
            considerations.append("Review AFE (Authorization for Expenditure) approval requirements")
        if not surface_same:
            considerations.append("Split estate: surface owner and mineral owner are different parties")
            considerations.append("Accommodation doctrine applies: mineral owner must accommodate existing surface uses if alternatives exist")
            considerations.append("Consider negotiating a surface use agreement before operations commence")
            considerations.append("Surface damage compensation may be required under state law")
        return considerations


# ============================================================================
# ADDITIONAL FASTAPI ROUTES FOR ADVANCED MODULES
# ============================================================================

_title_opinion_gen: Optional[TitleOpinionGenerator] = None
_homestead_analyzer: Optional[HomesteadAnalyzer] = None
_mineral_analyzer: Optional[MineralRightsAnalyzer] = None


def _get_title_opinion_gen() -> TitleOpinionGenerator:
    """Get or create title opinion generator singleton."""
    global _title_opinion_gen
    if _title_opinion_gen is None:
        _title_opinion_gen = TitleOpinionGenerator()
    return _title_opinion_gen


def _get_homestead_analyzer() -> HomesteadAnalyzer:
    """Get or create homestead analyzer singleton."""
    global _homestead_analyzer
    if _homestead_analyzer is None:
        _homestead_analyzer = HomesteadAnalyzer()
    return _homestead_analyzer


def _get_mineral_analyzer() -> MineralRightsAnalyzer:
    """Get or create mineral rights analyzer singleton."""
    global _mineral_analyzer
    if _mineral_analyzer is None:
        _mineral_analyzer = MineralRightsAnalyzer()
    return _mineral_analyzer


class TitleOpinionRequest(BaseModel):
    """Title opinion generation request."""
    chain_data: Optional[List[Dict[str, Any]]] = Field(None, description="Chain of title data")
    property_description: Optional[str] = Field(None, description="Legal description of property")
    jurisdiction: str = Field("TX", description="Jurisdiction (state code)")
    opinion_type: str = Field("preliminary", description="Opinion type: preliminary, final, update")


class HomesteadRequest(BaseModel):
    """Homestead analysis request."""
    property_type: str = Field("single_family", description="Property type")
    location: str = Field("urban", description="Location: urban or rural")
    acreage: float = Field(0.25, ge=0.0, description="Property acreage")
    is_primary_residence: bool = Field(True, description="Is this the primary residence")
    marital_status: str = Field("married", description="Marital status: single, married, family")
    proposed_lien_type: Optional[str] = Field(None, description="Proposed lien type to analyze")


class MineralInterestRequest(BaseModel):
    """Mineral interest analysis request."""
    interest_type: str = Field(..., description="Type of mineral interest")
    fraction: Optional[str] = Field(None, description="Fractional interest (e.g. 1/8)")
    surface_owner_same: bool = Field(False, description="Same person owns surface and minerals")


class AccommodationDoctrineRequest(BaseModel):
    """Accommodation doctrine analysis request."""
    surface_use: str = Field(..., description="Existing surface use")
    mineral_operation: str = Field(..., description="Proposed mineral operation")
    alternative_means_available: bool = Field(True, description="Are alternative means available to mineral operator")


@app.post("/analyze/title-opinion")
async def title_opinion_endpoint(request: TitleOpinionRequest) -> JSONResponse:
    """Generate a structured title opinion."""
    engine = _get_engine()
    engine._telemetry.record_re_metric(RealEstateMetricType.TITLE_OPINION)
    gen = _get_title_opinion_gen()
    result = gen.generate_opinion(
        chain_data=request.chain_data,
        property_description=request.property_description,
        jurisdiction=request.jurisdiction,
        opinion_type=request.opinion_type,
    )
    engine._audit.append("title_opinion_generated", {
        "jurisdiction": request.jurisdiction,
        "opinion_type": request.opinion_type,
    })
    return JSONResponse(content=result)


@app.post("/analyze/homestead")
async def homestead_endpoint(request: HomesteadRequest) -> JSONResponse:
    """Analyze Texas homestead exemption applicability."""
    engine = _get_engine()
    engine._telemetry.record_re_metric(RealEstateMetricType.TEXAS_SPECIFIC)
    analyzer = _get_homestead_analyzer()
    result = analyzer.analyze_homestead(
        property_type=request.property_type,
        location=request.location,
        acreage=request.acreage,
        is_primary_residence=request.is_primary_residence,
        marital_status=request.marital_status,
        proposed_lien_type=request.proposed_lien_type,
    )
    engine._audit.append("homestead_analysis", {
        "qualifies": result["qualifies_as_homestead"],
        "proposed_lien": request.proposed_lien_type,
    })
    return JSONResponse(content=result)


@app.post("/analyze/mineral-interest")
async def mineral_interest_endpoint(request: MineralInterestRequest) -> JSONResponse:
    """Analyze a mineral interest type."""
    engine = _get_engine()
    engine._telemetry.record_re_metric(RealEstateMetricType.MINERAL_RIGHTS_QUERY)
    analyzer = _get_mineral_analyzer()
    result = analyzer.analyze_mineral_interest(
        interest_type=request.interest_type,
        fraction=request.fraction,
        surface_owner_same=request.surface_owner_same,
    )
    engine._audit.append("mineral_interest_analysis", {"interest_type": request.interest_type})
    return JSONResponse(content=result)


@app.post("/analyze/accommodation-doctrine")
async def accommodation_doctrine_endpoint(request: AccommodationDoctrineRequest) -> JSONResponse:
    """Analyze accommodation doctrine applicability for surface-mineral conflicts."""
    engine = _get_engine()
    engine._telemetry.record_re_metric(RealEstateMetricType.MINERAL_RIGHTS_QUERY)
    analyzer = _get_mineral_analyzer()
    result = analyzer.analyze_accommodation_doctrine(
        surface_use=request.surface_use,
        mineral_operation=request.mineral_operation,
        alternative_means_available=request.alternative_means_available,
    )
    engine._audit.append("accommodation_doctrine_analysis", {
        "surface_use": request.surface_use,
        "mineral_operation": request.mineral_operation,
    })
    return JSONResponse(content=result)


# ============================================================================
# BATCH QUERY ENDPOINT
# ============================================================================

class BatchQueryRequest(BaseModel):
    """Batch query request for processing multiple queries."""
    queries: List[QueryRequest] = Field(..., min_length=1, max_length=10, description="List of queries to process")


@app.post("/query/batch")
async def batch_query_endpoint(request: BatchQueryRequest) -> JSONResponse:
    """Process multiple queries in a batch."""
    engine = _get_engine()
    results: List[Dict[str, Any]] = []

    for query_req in request.queries:
        response = await engine.process_query(query_req)
        results.append(response.model_dump())

    return JSONResponse(content={
        "batch_size": len(results),
        "results": results,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })


# ============================================================================
# COMPARISON ENDPOINT
# ============================================================================

class ComparisonRequest(BaseModel):
    """Compare two real estate concepts or approaches."""
    concept_a: str = Field(..., description="First concept or approach")
    concept_b: str = Field(..., description="Second concept or approach")
    jurisdiction: Optional[str] = Field(None, description="Jurisdiction context")


@app.post("/analyze/compare")
async def comparison_endpoint(request: ComparisonRequest) -> JSONResponse:
    """Compare two real estate concepts, approaches, or instruments."""
    engine = _get_engine()

    norm_a = normalize_query(request.concept_a)
    norm_b = normalize_query(request.concept_b)

    blocks_a = search_doctrines(request.concept_a, top_k=2)
    blocks_b = search_doctrines(request.concept_b, top_k=2)

    comparison: Dict[str, Any] = {
        "concept_a": {
            "query": request.concept_a,
            "categories": norm_a.detected_categories,
            "re_type": norm_a.detected_re_type,
            "doctrine_blocks": [b.to_dict() for b in blocks_a],
        },
        "concept_b": {
            "query": request.concept_b,
            "categories": norm_b.detected_categories,
            "re_type": norm_b.detected_re_type,
            "doctrine_blocks": [b.to_dict() for b in blocks_b],
        },
        "comparison_dimensions": [],
        "jurisdiction": request.jurisdiction or norm_a.detected_jurisdiction or norm_b.detected_jurisdiction,
    }

    # Build comparison dimensions
    if blocks_a and blocks_b:
        a_block = blocks_a[0]
        b_block = blocks_b[0]

        dimensions: List[Dict[str, Any]] = [
            {
                "dimension": "Authority Score",
                "concept_a": a_block.authority_score,
                "concept_b": b_block.authority_score,
                "advantage": request.concept_a if a_block.authority_score >= b_block.authority_score else request.concept_b,
            },
            {
                "dimension": "Confidence",
                "concept_a": a_block.confidence,
                "concept_b": b_block.confidence,
                "advantage": request.concept_a if a_block.confidence >= b_block.confidence else request.concept_b,
            },
            {
                "dimension": "Key Statutes Count",
                "concept_a": len(a_block.key_statutes),
                "concept_b": len(b_block.key_statutes),
                "advantage": request.concept_a if len(a_block.key_statutes) >= len(b_block.key_statutes) else request.concept_b,
            },
            {
                "dimension": "Available Remedies",
                "concept_a": len(a_block.remedies),
                "concept_b": len(b_block.remedies),
                "advantage": request.concept_a if len(a_block.remedies) >= len(b_block.remedies) else request.concept_b,
            },
            {
                "dimension": "Risk Factors",
                "concept_a": len(a_block.risk_factors),
                "concept_b": len(b_block.risk_factors),
                "advantage": request.concept_a if len(a_block.risk_factors) <= len(b_block.risk_factors) else request.concept_b,
            },
        ]
        comparison["comparison_dimensions"] = dimensions

    engine._audit.append("comparison_analysis", {
        "concept_a": request.concept_a,
        "concept_b": request.concept_b,
    })

    return JSONResponse(content=comparison)


# ============================================================================
# CLOSING COST ESTIMATOR
# ============================================================================

class ClosingCostEstimator:
    """
    Estimates closing costs for real estate transactions including
    buyer and seller cost breakdowns, transfer taxes, recording fees,
    title insurance premiums, prorated items, and jurisdiction-specific
    charges.
    """

    # Standard closing cost items with typical percentage ranges
    BUYER_COST_ITEMS: ClassVar[Dict[str, Dict[str, Any]]] = {
        "loan_origination_fee": {
            "description": "Loan origination fee (points)",
            "typical_pct": 0.01,
            "min_pct": 0.005,
            "max_pct": 0.02,
            "applies_to": "loan_amount",
            "category": "lender_fees",
        },
        "appraisal_fee": {
            "description": "Property appraisal fee",
            "flat_amount": 450.0,
            "min_amount": 300.0,
            "max_amount": 800.0,
            "category": "third_party_fees",
        },
        "credit_report_fee": {
            "description": "Credit report fee",
            "flat_amount": 30.0,
            "min_amount": 25.0,
            "max_amount": 50.0,
            "category": "lender_fees",
        },
        "flood_certification": {
            "description": "Flood zone certification fee",
            "flat_amount": 25.0,
            "min_amount": 15.0,
            "max_amount": 50.0,
            "category": "third_party_fees",
        },
        "title_search": {
            "description": "Title search and examination",
            "flat_amount": 350.0,
            "min_amount": 200.0,
            "max_amount": 600.0,
            "category": "title_fees",
        },
        "title_insurance_lender": {
            "description": "Lender's title insurance policy",
            "typical_pct": 0.005,
            "min_pct": 0.003,
            "max_pct": 0.008,
            "applies_to": "loan_amount",
            "category": "title_fees",
        },
        "title_insurance_owner": {
            "description": "Owner's title insurance policy",
            "typical_pct": 0.005,
            "min_pct": 0.003,
            "max_pct": 0.008,
            "applies_to": "purchase_price",
            "category": "title_fees",
        },
        "survey": {
            "description": "Property survey",
            "flat_amount": 500.0,
            "min_amount": 300.0,
            "max_amount": 1500.0,
            "category": "third_party_fees",
        },
        "recording_fees": {
            "description": "Recording fees (deed, mortgage)",
            "flat_amount": 125.0,
            "min_amount": 50.0,
            "max_amount": 300.0,
            "category": "government_fees",
        },
        "home_inspection": {
            "description": "Home inspection fee",
            "flat_amount": 400.0,
            "min_amount": 250.0,
            "max_amount": 700.0,
            "category": "third_party_fees",
        },
        "attorney_fee_buyer": {
            "description": "Buyer's attorney fee",
            "flat_amount": 750.0,
            "min_amount": 500.0,
            "max_amount": 2000.0,
            "category": "professional_fees",
        },
        "escrow_fee": {
            "description": "Escrow/closing agent fee",
            "flat_amount": 500.0,
            "min_amount": 300.0,
            "max_amount": 1200.0,
            "category": "settlement_fees",
        },
        "prepaid_interest": {
            "description": "Prepaid interest (per diem to month end)",
            "typical_pct": 0.002,
            "min_pct": 0.001,
            "max_pct": 0.005,
            "applies_to": "loan_amount",
            "category": "prepaid_items",
        },
        "homeowners_insurance_premium": {
            "description": "First year homeowners insurance",
            "typical_pct": 0.005,
            "min_pct": 0.003,
            "max_pct": 0.012,
            "applies_to": "purchase_price",
            "category": "prepaid_items",
        },
        "property_tax_escrow": {
            "description": "Property tax escrow (initial deposit)",
            "typical_pct": 0.005,
            "min_pct": 0.002,
            "max_pct": 0.010,
            "applies_to": "purchase_price",
            "category": "escrow_reserves",
        },
    }

    SELLER_COST_ITEMS: ClassVar[Dict[str, Dict[str, Any]]] = {
        "real_estate_commission": {
            "description": "Real estate agent commission",
            "typical_pct": 0.06,
            "min_pct": 0.04,
            "max_pct": 0.06,
            "applies_to": "purchase_price",
            "category": "commission",
        },
        "transfer_tax": {
            "description": "Transfer tax / documentary stamps",
            "typical_pct": 0.002,
            "min_pct": 0.0,
            "max_pct": 0.025,
            "applies_to": "purchase_price",
            "category": "government_fees",
        },
        "attorney_fee_seller": {
            "description": "Seller's attorney fee",
            "flat_amount": 500.0,
            "min_amount": 300.0,
            "max_amount": 1500.0,
            "category": "professional_fees",
        },
        "title_insurance_owner_seller": {
            "description": "Owner's title policy (seller pays in some jurisdictions)",
            "typical_pct": 0.005,
            "min_pct": 0.003,
            "max_pct": 0.008,
            "applies_to": "purchase_price",
            "category": "title_fees",
        },
        "payoff_fees": {
            "description": "Existing mortgage payoff and recording",
            "flat_amount": 250.0,
            "min_amount": 100.0,
            "max_amount": 500.0,
            "category": "payoff_costs",
        },
        "hoa_estoppel": {
            "description": "HOA estoppel certificate",
            "flat_amount": 250.0,
            "min_amount": 100.0,
            "max_amount": 500.0,
            "category": "hoa_fees",
        },
        "prorated_property_taxes": {
            "description": "Prorated property taxes owed at closing",
            "typical_pct": 0.003,
            "min_pct": 0.001,
            "max_pct": 0.010,
            "applies_to": "purchase_price",
            "category": "prorations",
        },
    }

    # Texas-specific adjustments — no state transfer tax
    TX_ADJUSTMENTS: ClassVar[Dict[str, Any]] = {
        "transfer_tax": {"typical_pct": 0.0, "min_pct": 0.0, "max_pct": 0.0, "note": "Texas has no transfer tax"},
        "title_insurance_payer": "seller",
        "survey_required": True,
        "attorney_required": False,
        "escrow_officer": "title_company",
    }

    def __init__(self) -> None:
        """Initialize closing cost estimator."""
        logger.info("ClosingCostEstimator initialized")

    def _calc_item_cost(
        self,
        item: Dict[str, Any],
        purchase_price: float,
        loan_amount: float,
    ) -> float:
        """Calculate cost for a single line item."""
        if "flat_amount" in item:
            return item["flat_amount"]
        pct = item.get("typical_pct", 0.0)
        base = purchase_price if item.get("applies_to") == "purchase_price" else loan_amount
        return round(base * pct, 2)

    def estimate_closing_costs(
        self,
        purchase_price: float,
        loan_amount: float,
        jurisdiction: str = "TX",
        property_type: str = "single_family",
        is_cash: bool = False,
    ) -> Dict[str, Any]:
        """
        Estimate total closing costs for a real estate transaction.

        Args:
            purchase_price: Property purchase price.
            loan_amount: Loan amount (0 for cash deals).
            jurisdiction: State abbreviation.
            property_type: Property type classification.
            is_cash: True if all-cash transaction (no lender fees).

        Returns:
            Detailed closing cost breakdown with buyer/seller splits.
        """
        buyer_items: List[Dict[str, Any]] = []
        seller_items: List[Dict[str, Any]] = []
        is_texas = jurisdiction.upper() in ("TX", "TEXAS")

        # Buyer costs
        for item_key, item_def in self.BUYER_COST_ITEMS.items():
            if is_cash and item_def.get("category") in ("lender_fees", "prepaid_items", "escrow_reserves"):
                if item_key not in ("homeowners_insurance_premium",):
                    continue
            if is_cash and item_key in ("loan_origination_fee", "title_insurance_lender", "prepaid_interest", "property_tax_escrow"):
                continue
            cost = self._calc_item_cost(item_def, purchase_price, loan_amount)
            # Texas: seller typically pays owner's title insurance
            if is_texas and item_key == "title_insurance_owner":
                continue  # Moved to seller side
            buyer_items.append({
                "item": item_key,
                "description": item_def["description"],
                "amount": cost,
                "category": item_def["category"],
            })

        # Seller costs
        for item_key, item_def in self.SELLER_COST_ITEMS.items():
            adjusted = dict(item_def)
            if is_texas and item_key == "transfer_tax":
                adjusted.update(self.TX_ADJUSTMENTS.get("transfer_tax", {}))
            cost = self._calc_item_cost(adjusted, purchase_price, loan_amount)
            seller_items.append({
                "item": item_key,
                "description": adjusted["description"],
                "amount": cost,
                "category": adjusted["category"],
            })

        # In Texas, add owner's title insurance to seller costs
        if is_texas:
            oti = self.BUYER_COST_ITEMS["title_insurance_owner"]
            cost = self._calc_item_cost(oti, purchase_price, loan_amount)
            seller_items.append({
                "item": "title_insurance_owner",
                "description": oti["description"] + " (seller pays in TX)",
                "amount": cost,
                "category": oti["category"],
            })

        buyer_total = sum(i["amount"] for i in buyer_items)
        seller_total = sum(i["amount"] for i in seller_items)

        return {
            "purchase_price": purchase_price,
            "loan_amount": loan_amount,
            "jurisdiction": jurisdiction,
            "property_type": property_type,
            "is_cash_transaction": is_cash,
            "buyer_costs": {
                "items": buyer_items,
                "total": round(buyer_total, 2),
                "pct_of_price": round(buyer_total / purchase_price * 100, 2) if purchase_price > 0 else 0.0,
            },
            "seller_costs": {
                "items": seller_items,
                "total": round(seller_total, 2),
                "pct_of_price": round(seller_total / purchase_price * 100, 2) if purchase_price > 0 else 0.0,
            },
            "combined_total": round(buyer_total + seller_total, 2),
            "texas_notes": [
                "Texas has no state transfer tax on real property conveyances.",
                "Seller customarily pays for owner's title insurance policy in Texas.",
                "Texas uses title companies as settlement agents (no attorney requirement).",
                "Texas property tax rates average 1.60%-2.23% depending on county.",
            ] if is_texas else [],
            "disclaimers": [
                "Estimates only — actual costs may vary based on lender, title company, and local customs.",
                "Does not include seller concessions or buyer credits that may be negotiated.",
                "Property tax prorations depend on closing date and taxing authority fiscal year.",
            ],
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


# ============================================================================
# LEASE ANALYZER
# ============================================================================

class LeaseAnalyzer:
    """
    Analyzes residential and commercial lease agreements for legal compliance,
    risk factors, prohibited provisions, and jurisdiction-specific requirements.
    Implements Texas Property Code Chapter 92 (Residential Tenancies) and
    Chapter 93 (Commercial Tenancies) compliance checking.
    """

    PROHIBITED_LEASE_PROVISIONS_TX: ClassVar[List[Dict[str, str]]] = [
        {
            "provision": "Waiver of tenant's right to jury trial",
            "statute": "Tex. Prop. Code § 92.006(b)",
            "consequence": "Void and unenforceable",
        },
        {
            "provision": "Waiver of tenant's right to repair and deduct",
            "statute": "Tex. Prop. Code § 92.006(b)",
            "consequence": "Void and unenforceable",
        },
        {
            "provision": "Waiver of landlord's duty to mitigate damages",
            "statute": "Tex. Prop. Code § 91.006",
            "consequence": "Provision is void — landlord has statutory duty to mitigate",
        },
        {
            "provision": "Automatic lease renewal without 30-day notice",
            "statute": "Tex. Prop. Code § 91.001(e)",
            "consequence": "Renewal provision may be unenforceable if no adequate notice given",
        },
        {
            "provision": "Confession of judgment clause",
            "statute": "Tex. Prop. Code § 92.006(b)",
            "consequence": "Absolutely void and unenforceable in Texas",
        },
        {
            "provision": "Waiver of notice to vacate",
            "statute": "Tex. Prop. Code § 24.005",
            "consequence": "Void — 3-day notice to vacate is mandatory pre-eviction requirement",
        },
        {
            "provision": "Excessive late fee (greater than reasonable estimate of damages)",
            "statute": "Tex. Prop. Code § 92.019",
            "consequence": "Unenforceable if not a reasonable estimate of actual damages",
        },
        {
            "provision": "Lockout provision without court order",
            "statute": "Tex. Prop. Code § 92.0081",
            "consequence": "Illegal — landlord liable for actual damages + one month rent + $500",
        },
        {
            "provision": "Interruption of utilities as eviction tactic",
            "statute": "Tex. Prop. Code § 92.008",
            "consequence": "Illegal — tenant may recover actual damages + one month rent + $500 + attorney fees",
        },
        {
            "provision": "Waiver of landlord obligation to return security deposit",
            "statute": "Tex. Prop. Code § 92.103",
            "consequence": "Void — 30-day return requirement cannot be waived",
        },
    ]

    REQUIRED_LEASE_DISCLOSURES_TX: ClassVar[List[Dict[str, str]]] = [
        {
            "disclosure": "Name and address of property owner/manager",
            "statute": "Tex. Prop. Code § 92.201",
            "penalty": "Tenant may terminate if not provided within 7 days of request",
        },
        {
            "disclosure": "Right to repair and deduct for conditions affecting health/safety",
            "statute": "Tex. Prop. Code § 92.0561",
            "penalty": "Landlord liability if conditions not remedied after notice",
        },
        {
            "disclosure": "Lead-based paint disclosure (pre-1978 properties)",
            "statute": "42 U.S.C. § 4852d; 24 CFR Part 35",
            "penalty": "Up to $19,507 per violation; treble damages in private action",
        },
        {
            "disclosure": "Smoke detector compliance",
            "statute": "Tex. Prop. Code § 92.255",
            "penalty": "Landlord liable for damages if non-compliant detector causes harm",
        },
        {
            "disclosure": "Flood risk disclosure (if in 100-year floodplain)",
            "statute": "Tex. Prop. Code § 92.0135",
            "penalty": "Tenant may terminate within 3 days or sue for damages",
        },
    ]

    LEASE_RISK_FACTORS: ClassVar[List[Dict[str, Any]]] = [
        {"factor": "no_written_lease", "severity": "HIGH", "description": "Oral lease — difficult to enforce terms; defaults to month-to-month under Texas law"},
        {"factor": "no_security_deposit_limit", "severity": "MEDIUM", "description": "Texas has no statutory cap on security deposits for residential leases"},
        {"factor": "ambiguous_maintenance_responsibility", "severity": "HIGH", "description": "Unclear allocation of repair duties between landlord and tenant"},
        {"factor": "missing_holdover_provision", "severity": "MEDIUM", "description": "No holdover rent provision may default to original rent rate"},
        {"factor": "blanket_indemnification", "severity": "HIGH", "description": "One-sided indemnification clause may be unconscionable"},
        {"factor": "personal_guaranty_unlimited", "severity": "HIGH", "description": "Unlimited personal guaranty exposes guarantor to uncapped liability"},
        {"factor": "no_force_majeure", "severity": "MEDIUM", "description": "No force majeure clause may bind parties even during extraordinary events"},
        {"factor": "no_sublease_provision", "severity": "LOW", "description": "Silence on subletting defaults to landlord's reasonable consent required"},
        {"factor": "auto_renewal_trap", "severity": "MEDIUM", "description": "Auto-renewal with short opt-out window may trap tenant in unwanted term"},
        {"factor": "triple_net_without_caps", "severity": "HIGH", "description": "NNN lease without expense caps exposes tenant to unlimited pass-through increases"},
    ]

    def __init__(self) -> None:
        """Initialize lease analyzer."""
        logger.info("LeaseAnalyzer initialized")

    def analyze_lease(
        self,
        lease_type: str,
        term_months: int,
        monthly_rent: float,
        jurisdiction: str = "TX",
        security_deposit: Optional[float] = None,
        late_fee_amount: Optional[float] = None,
        has_personal_guaranty: bool = False,
        lease_provisions: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Analyze a lease for legal compliance, risk factors, and enforceability.

        Args:
            lease_type: residential or commercial.
            term_months: Lease duration in months.
            monthly_rent: Monthly rent amount.
            jurisdiction: State abbreviation.
            security_deposit: Security deposit amount if any.
            late_fee_amount: Late fee charged per occurrence.
            has_personal_guaranty: Whether a personal guaranty is attached.
            lease_provisions: List of provision descriptions to check.

        Returns:
            Comprehensive lease analysis with compliance, risks, and recommendations.
        """
        is_texas = jurisdiction.upper() in ("TX", "TEXAS")
        is_residential = lease_type.lower() in ("residential", "apartment", "house", "condo")
        issues: List[Dict[str, Any]] = []
        recommendations: List[str] = []
        risk_score: float = 0.0
        risk_items: List[Dict[str, Any]] = []

        # Security deposit analysis
        deposit_analysis: Dict[str, Any] = {"provided": security_deposit is not None}
        if security_deposit is not None:
            deposit_ratio = security_deposit / monthly_rent if monthly_rent > 0 else 0
            deposit_analysis["amount"] = security_deposit
            deposit_analysis["months_equivalent"] = round(deposit_ratio, 2)
            if is_texas and is_residential:
                deposit_analysis["statutory_cap"] = "None (Texas has no statutory cap on residential security deposits)"
                deposit_analysis["return_deadline_days"] = 30
                deposit_analysis["statute"] = "Tex. Prop. Code § 92.103"
                if deposit_ratio > 3.0:
                    issues.append({
                        "issue": "Excessive security deposit",
                        "severity": "MEDIUM",
                        "detail": f"Security deposit of {deposit_ratio:.1f}x monthly rent may be challenged as unconscionable",
                        "recommendation": "Consider reducing deposit to 1-2 months rent to avoid potential unconscionability challenge",
                    })
                    risk_score += 15.0

        # Late fee analysis
        late_fee_analysis: Dict[str, Any] = {"provided": late_fee_amount is not None}
        if late_fee_amount is not None:
            late_fee_pct = late_fee_amount / monthly_rent * 100 if monthly_rent > 0 else 0
            late_fee_analysis["amount"] = late_fee_amount
            late_fee_analysis["pct_of_rent"] = round(late_fee_pct, 2)
            if is_texas and is_residential:
                late_fee_analysis["statute"] = "Tex. Prop. Code § 92.019"
                late_fee_analysis["standard"] = "Must be reasonable estimate of damages"
                if late_fee_pct > 12.0:
                    issues.append({
                        "issue": "Potentially excessive late fee",
                        "severity": "HIGH",
                        "detail": f"Late fee of {late_fee_pct:.1f}% of rent exceeds typical 8-12% range",
                        "statute": "Tex. Prop. Code § 92.019",
                        "recommendation": "Reduce late fee to no more than 10% of monthly rent",
                    })
                    risk_score += 20.0

        # Provision compliance check
        prohibited_matches: List[Dict[str, str]] = []
        if lease_provisions and is_texas:
            provisions_lower = [p.lower() for p in lease_provisions]
            for prohibited in self.PROHIBITED_LEASE_PROVISIONS_TX:
                prov_lower = prohibited["provision"].lower()
                for user_prov in provisions_lower:
                    # Simple keyword overlap scoring
                    prov_words = set(prov_lower.split())
                    user_words = set(user_prov.split())
                    overlap = len(prov_words & user_words) / max(len(prov_words), 1)
                    if overlap > 0.4:
                        prohibited_matches.append(prohibited)
                        risk_score += 25.0
                        break

        # Risk factor assessment
        for rf in self.LEASE_RISK_FACTORS:
            severity_weight = {"HIGH": 20.0, "MEDIUM": 10.0, "LOW": 5.0}
            if rf["factor"] == "personal_guaranty_unlimited" and has_personal_guaranty:
                risk_items.append(rf)
                risk_score += severity_weight.get(rf["severity"], 5.0)
            elif rf["factor"] == "no_written_lease" and term_months == 0:
                risk_items.append(rf)
                risk_score += severity_weight.get(rf["severity"], 5.0)
            elif rf["factor"] == "auto_renewal_trap" and term_months >= 12:
                risk_items.append(rf)
                risk_score += severity_weight.get(rf["severity"], 5.0)

        # Normalize risk score to 0-100
        risk_score = min(risk_score, 100.0)

        # Build recommendations
        if is_texas and is_residential:
            recommendations.extend([
                "Ensure lease includes landlord name/address per Tex. Prop. Code § 92.201.",
                "Include smoke detector compliance provision per Tex. Prop. Code § 92.255.",
                "Include flood disclosure if property is in 100-year floodplain per Tex. Prop. Code § 92.0135.",
                "Specify security deposit return address and 30-day return timeline per § 92.103.",
            ])
        if not is_residential:
            recommendations.extend([
                "Include CAM reconciliation provision with annual audit right for commercial tenants.",
                "Specify permitted use clearly to avoid restrictive use disputes.",
                "Include expense stop or cap on NNN pass-throughs to limit tenant exposure.",
                "Address tenant improvement allowance and construction timeline.",
            ])

        # Risk band classification
        if risk_score >= 70.0:
            risk_band = "HIGH_RISK"
        elif risk_score >= 40.0:
            risk_band = "MODERATE_RISK"
        elif risk_score >= 15.0:
            risk_band = "LOW_RISK"
        else:
            risk_band = "MINIMAL_RISK"

        return {
            "lease_type": lease_type,
            "term_months": term_months,
            "monthly_rent": monthly_rent,
            "jurisdiction": jurisdiction,
            "is_residential": is_residential,
            "security_deposit_analysis": deposit_analysis,
            "late_fee_analysis": late_fee_analysis,
            "prohibited_provision_matches": prohibited_matches,
            "required_disclosures": self.REQUIRED_LEASE_DISCLOSURES_TX if is_texas else [],
            "risk_factors_triggered": risk_items,
            "issues_found": issues,
            "recommendations": recommendations,
            "risk_score": round(risk_score, 1),
            "risk_band": risk_band,
            "applicable_statutes": {
                "residential": "Tex. Prop. Code Ch. 92" if is_texas else f"{jurisdiction} residential tenancy statute",
                "commercial": "Tex. Prop. Code Ch. 93" if is_texas else f"{jurisdiction} commercial tenancy statute",
                "eviction": "Tex. Prop. Code Ch. 24" if is_texas else f"{jurisdiction} eviction statute",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


# ============================================================================
# SINGLETON ACCESSORS FOR NEW MODULES
# ============================================================================

_closing_cost_estimator: Optional[ClosingCostEstimator] = None
_lease_analyzer: Optional[LeaseAnalyzer] = None


def _get_closing_cost_estimator() -> ClosingCostEstimator:
    """Get or create singleton ClosingCostEstimator."""
    global _closing_cost_estimator
    if _closing_cost_estimator is None:
        _closing_cost_estimator = ClosingCostEstimator()
    return _closing_cost_estimator


def _get_lease_analyzer() -> LeaseAnalyzer:
    """Get or create singleton LeaseAnalyzer."""
    global _lease_analyzer
    if _lease_analyzer is None:
        _lease_analyzer = LeaseAnalyzer()
    return _lease_analyzer


# ============================================================================
# CLOSING COST ENDPOINT
# ============================================================================

class ClosingCostRequest(BaseModel):
    """Request model for closing cost estimation."""
    purchase_price: float = Field(..., gt=0, description="Property purchase price")
    loan_amount: float = Field(0.0, ge=0, description="Loan amount (0 for cash)")
    jurisdiction: str = Field("TX", description="State abbreviation")
    property_type: str = Field("single_family", description="Property type")
    is_cash: bool = Field(False, description="All-cash transaction")


@app.post("/analyze/closing-costs")
async def closing_costs_endpoint(request: ClosingCostRequest) -> JSONResponse:
    """Estimate closing costs for a real estate transaction."""
    engine = _get_engine()
    engine._telemetry.record_re_metric(RealEstateMetricType.TRANSACTION_REVIEW)
    estimator = _get_closing_cost_estimator()
    result = estimator.estimate_closing_costs(
        purchase_price=request.purchase_price,
        loan_amount=request.loan_amount,
        jurisdiction=request.jurisdiction,
        property_type=request.property_type,
        is_cash=request.is_cash,
    )
    engine._audit.append("closing_cost_estimate", {
        "purchase_price": request.purchase_price,
        "jurisdiction": request.jurisdiction,
    })
    return JSONResponse(content=result)


# ============================================================================
# LEASE ANALYSIS ENDPOINT
# ============================================================================

class LeaseAnalysisRequest(BaseModel):
    """Request model for lease analysis."""
    lease_type: str = Field(..., description="residential or commercial")
    term_months: int = Field(..., ge=0, description="Lease duration in months (0 for month-to-month)")
    monthly_rent: float = Field(..., gt=0, description="Monthly rent amount")
    jurisdiction: str = Field("TX", description="State abbreviation")
    security_deposit: Optional[float] = Field(None, ge=0, description="Security deposit amount")
    late_fee_amount: Optional[float] = Field(None, ge=0, description="Late fee per occurrence")
    has_personal_guaranty: bool = Field(False, description="Whether personal guaranty is attached")
    lease_provisions: Optional[List[str]] = Field(None, description="List of provision descriptions to check")


@app.post("/analyze/lease")
async def lease_analysis_endpoint(request: LeaseAnalysisRequest) -> JSONResponse:
    """Analyze a lease for legal compliance, risk factors, and enforceability."""
    engine = _get_engine()
    engine._telemetry.record_re_metric(RealEstateMetricType.LANDLORD_TENANT)
    analyzer = _get_lease_analyzer()
    result = analyzer.analyze_lease(
        lease_type=request.lease_type,
        term_months=request.term_months,
        monthly_rent=request.monthly_rent,
        jurisdiction=request.jurisdiction,
        security_deposit=request.security_deposit,
        late_fee_amount=request.late_fee_amount,
        has_personal_guaranty=request.has_personal_guaranty,
        lease_provisions=request.lease_provisions,
    )
    engine._audit.append("lease_analysis", {
        "lease_type": request.lease_type,
        "term_months": request.term_months,
        "risk_band": result["risk_band"],
    })
    return JSONResponse(content=result)


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    logger.info(f"Starting LG08 Real Estate Law Engine on port {ENGINE_PORT}")
    uvicorn.run(
        "engine:app",
        host=ENGINE_HOST,
        port=ENGINE_PORT,
        reload=False,
        log_level="info",
        access_log=True,
    )
