"""
LG06 IP ANALYSIS ENGINE - Production Architecture
====================================================
Professional-grade intellectual property analysis system for patent,
trademark, copyright, and trade secret law.

Architecture:
    Layer 1: Doctrine Cache (0-200ms) - Pre-compiled expert IP reasoning
    Layer 2: Semantic Search (200-700ms) - TF-IDF on cache miss
    Layer 3: IP Analysis (700-1500ms) - Structured IP analysis, claim mapping
    Layer 4: Deep Analysis (on-demand) - Multi-doctrine synthesis, FTO, portfolio

Response Modes:
    FAST: Doctrine-driven, minimal citations, sub-2 seconds
    ANALYSIS: Structured IP analysis with claim mapping and statutory framework
    MEMO: Full IP memorandum with comprehensive citation and risk assessment
    FTO: Freedom-to-operate opinion with infringement risk matrix
    PORTFOLIO: Full IP portfolio assessment with valuation and strategy

TIE-20 Components:
    1.  three_layer_response
    2.  response_modes
    3.  doctrine_cache
    4.  authority_hardening
    5.  confidence_stratification
    6.  semantic_normalization
    7.  vector_search_chromadb (TF-IDF implementation)
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

Port: 8396
Engine ID: LG06
Tier: LEGAL (Auth 5.0)
Mode: DET (Deterministic)

Version: 2.0.0
Author: ECHO OMEGA PRIME
Authority: 11.0 SOVEREIGN
"""

from fastapi import FastAPI, HTTPException, Depends, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import ClassVar, Optional, List, Dict, Any, Literal, Tuple, Set
from enum import Enum
from dataclasses import dataclass, field as dc_field
from datetime import datetime, timezone
from contextlib import asynccontextmanager
import hashlib
import json
import math
import re
import time
import traceback
import uuid
from collections import Counter, defaultdict
from pathlib import Path

from loguru import logger

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

import sys
ENGINE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ENGINE_DIR))
sys.path.insert(0, str(ENGINE_DIR.parent / "_shared"))

from telemetry import (
    get_telemetry,
    trace_query,
    complete_trace,
    log_error,
    record_doctrine_mutation,
    record_citation_lookup,
    ErrorDomain,
    ResponseLayer,
    MutationType,
    MutationOrigin,
    CitationLookupType,
    IPMetricType,
    TelemetryCollector,
    QueryTrace,
    TelemetryStep,
)

from semantic import (
    normalize_query,
    NormalizationResult,
    get_semantic_map,
    get_governance_metadata as get_semantic_governance,
    get_semantic_map_version,
    get_semantic_map_hash,
    verify_dictionary_integrity,
    get_citation_patterns,
    get_nice_classification,
    get_cpc_sections,
    CITATION_PATTERNS,
)

import sys

# Ensure sibling modules are importable
ENGINE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ENGINE_DIR))
from doctrines import (
    DOCTRINE_CACHE,
    DoctrineResponse,
    IPDoctrineEngine,
    get_engine as get_doctrine_engine,
    get_doctrine_hash,
    get_doctrine_count,
)

from search import (
    DoctrineSearchIndex,
    SearchResult,
    PatentClaimParser,
    ParsedClaim,
    PriorArtSearchEngine,
    PriorArtResult,
    InfringementMapper,
    InfringementAnalysisResult,
    FTOElementMapping,
    TrademarkSearchEngine,
    get_search_index,
    get_claim_parser,
    get_prior_art_engine,
    get_infringement_mapper,
    get_trademark_engine,
    compute_query_hash,
)

# ============================================================================
# LOGGING SETUP (TIE-20 Component #18: loguru_logging)
# ============================================================================

LOG_DIR = Path("O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/LG06_ip_analysis/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

logger.add(
    LOG_DIR / "lg06_engine_{time}.log",
    rotation="50 MB",
    retention="30 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {message}",
)

AUDIT_LOG = LOG_DIR / "audit_trail.jsonl"

# Load config
CONFIG_PATH = Path(__file__).parent / "config.json"
with open(CONFIG_PATH, "r", encoding="utf-8") as _cf:
    ENGINE_CONFIG = json.load(_cf)


# ############################################################################
#
# SECTION 1: ENUMS, CONSTANTS, AND CONFIGURATION
#
# ############################################################################

# ============================================================================
# ENGINE IDENTITY
# ============================================================================

ENGINE_ID = "LG06"
ENGINE_NAME = "IP Analysis Engine"
ENGINE_VERSION = "2.0.0"
ENGINE_PORT = 8396
ENGINE_TIER = "LEGAL"
ENGINE_MODE = "DET"
AUTHORITY_LEVEL = 5.0
AUTHORITY_GATE = 5.0

# ============================================================================
# RESPONSE MODE ENUM
# ============================================================================

class ResponseMode(str, Enum):
    """Available response modes for the IP Analysis Engine."""
    FAST = "fast"
    ANALYSIS = "analysis"
    MEMO = "memo"
    FTO = "fto"
    PORTFOLIO = "portfolio"


# ============================================================================
# IP CATEGORY ENUM
# ============================================================================

class IPCategory(str, Enum):
    """Intellectual property categories."""
    PATENT = "patent"
    TRADEMARK = "trademark"
    COPYRIGHT = "copyright"
    TRADE_SECRET = "trade_secret"
    LICENSING = "licensing"
    INTERNATIONAL = "international"
    FTO = "fto"
    PORTFOLIO = "portfolio"
    VALUATION = "valuation"
    INFRINGEMENT = "infringement"
    OPEN_SOURCE = "open_source"
    GENERAL = "general"


# ============================================================================
# CONFIDENCE BANDS
# ============================================================================

CONFIDENCE_BANDS = ENGINE_CONFIG.get("confidence_bands", {
    "DEFENSIBLE": {"min_score": 0.85},
    "SUPPORTABLE": {"min_score": 0.65},
    "DISCLOSURE": {"min_score": 0.50},
    "HIGH_RISK": {"min_score": 0.0},
})


def classify_confidence(score: float) -> str:
    """Classify a confidence score into a named band."""
    if score >= 0.85:
        return "DEFENSIBLE"
    if score >= 0.65:
        return "SUPPORTABLE"
    if score >= 0.50:
        return "DISCLOSURE"
    return "HIGH_RISK"


# ============================================================================
# EPISTEMIC GUARDRAILS
# ============================================================================

BANNED_PHRASES: List[str] = ENGINE_CONFIG.get("epistemic_guardrails", {}).get("banned_phrases", [])
REQUIRED_DISCLAIMERS: Dict[str, str] = ENGINE_CONFIG.get("epistemic_guardrails", {}).get("required_disclaimers", {})


def apply_epistemic_guardrails(text: str) -> Tuple[str, List[str]]:
    """Check text for banned phrases and apply guardrails.

    Returns the cleaned text and a list of violations found.
    """
    violations: List[str] = []
    cleaned = text
    for phrase in BANNED_PHRASES:
        if phrase.lower() in cleaned.lower():
            violations.append(f"Banned phrase detected: '{phrase}'")
            cleaned = re.sub(re.escape(phrase), "[REDACTED - epistemic guardrail]", cleaned, flags=re.IGNORECASE)
    return cleaned, violations


# ############################################################################
#
# SECTION 2: PYDANTIC MODELS
#
# ############################################################################

# ============================================================================
# REQUEST MODELS
# ============================================================================

class IPQueryRequest(BaseModel):
    """Primary query request model."""
    query: str = Field(..., min_length=3, max_length=5000, description="The IP query to analyze")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response mode")
    authority_level: float = Field(default=5.0, ge=0.0, le=11.0, description="Required authority level")
    ip_category: Optional[IPCategory] = Field(default=None, description="Filter by IP category")
    include_citations: bool = Field(default=True, description="Include legal citations")
    include_analysis: bool = Field(default=True, description="Include analysis breakdown")
    max_results: int = Field(default=5, ge=1, le=20, description="Maximum doctrine results")
    deep_analysis: bool = Field(default=False, description="Enable deep multi-doctrine analysis")

    model_config: ClassVar[Dict[str, Any]] = {"json_schema_extra": {
        "example": {
            "query": "What are the requirements for patenting a software invention under 35 USC 101?",
            "mode": "analysis",
            "authority_level": 5.0,
            "ip_category": "patent",
            "include_citations": True,
            "include_analysis": True,
            "max_results": 5,
            "deep_analysis": False,
        }
    }}


class ClaimAnalysisRequest(BaseModel):
    """Request for patent claim analysis."""
    claims_text: str = Field(..., min_length=10, max_length=50000, description="Patent claims text")
    product_features: Optional[List[str]] = Field(default=None, description="Product features for FTO/infringement")
    analysis_type: Literal["parse", "infringement", "fto"] = Field(default="parse")
    patent_id: Optional[str] = Field(default=None, description="Patent number for reference")
    target_claims: Optional[List[int]] = Field(default=None, description="Specific claims to analyze")


class TrademarkSearchRequest(BaseModel):
    """Request for trademark clearance search."""
    proposed_mark: str = Field(..., min_length=1, max_length=500, description="Proposed trademark")
    nice_classes: Optional[List[int]] = Field(default=None, description="Nice classification classes")
    goods_services: Optional[str] = Field(default=None, description="Description of goods/services")


class PriorArtSearchRequest(BaseModel):
    """Request for prior art search."""
    invention_description: str = Field(..., min_length=10, max_length=10000, description="Invention description")
    keywords: Optional[List[str]] = Field(default=None, description="Additional search keywords")
    top_k: int = Field(default=5, ge=1, le=20, description="Maximum results")


class DriftWatcherRequest(BaseModel):
    """Request for doctrine drift analysis."""
    topic: Optional[str] = Field(default=None, description="Specific topic to check")
    category: Optional[IPCategory] = Field(default=None, description="Category to check")
    max_age_days: int = Field(default=90, ge=1, le=365, description="Max acceptable age in days")


# ============================================================================
# RESPONSE MODELS
# ============================================================================

class DoctrineResultModel(BaseModel):
    """A single doctrine result in the response."""
    topic: str
    title: str
    category: str
    content: str
    authority: str
    confidence: float
    confidence_band: str
    citations: List[str]
    tags: List[str]
    last_updated: str
    determinism_hash: str


class SearchResultModel(BaseModel):
    """A single search result in the response."""
    doc_id: str
    topic: str
    score: float
    ip_category: str
    matched_tokens: List[str]


class IPQueryResponse(BaseModel):
    """Primary query response model."""
    engine_id: str = ENGINE_ID
    engine_version: str = ENGINE_VERSION
    query_hash: str
    response_mode: str
    ip_category: Optional[str]
    confidence: float
    confidence_band: str
    doctrine_results: List[DoctrineResultModel]
    search_results: List[SearchResultModel]
    analysis: Optional[Dict[str, Any]] = None
    deep_analysis: Optional[Dict[str, Any]] = None
    citations: List[str]
    disclaimers: List[str]
    epistemic_violations: List[str]
    normalization: Dict[str, Any]
    determinism_hash: str
    response_time_ms: float
    layer: str
    telemetry: Dict[str, Any]


class ClaimAnalysisResponse(BaseModel):
    """Response for claim analysis."""
    engine_id: str = ENGINE_ID
    analysis_type: str
    patent_id: Optional[str]
    claims: List[Dict[str, Any]]
    infringement_results: Optional[List[Dict[str, Any]]] = None
    claim_tree: Optional[Dict[str, Any]] = None
    summary: Dict[str, Any]
    determinism_hash: str
    response_time_ms: float


class TrademarkSearchResponse(BaseModel):
    """Response for trademark clearance search."""
    engine_id: str = ENGINE_ID
    proposed_mark: str
    conflicts: List[Dict[str, Any]]
    risk_assessment: Dict[str, Any]
    recommendations: List[str]
    determinism_hash: str
    response_time_ms: float


class PriorArtSearchResponse(BaseModel):
    """Response for prior art search."""
    engine_id: str = ENGINE_ID
    references: List[Dict[str, Any]]
    risk_summary: Dict[str, Any]
    determinism_hash: str
    response_time_ms: float


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    engine_id: str
    engine_name: str
    engine_version: str
    port: int
    tier: str
    mode: str
    authority_level: float
    uptime_seconds: float
    doctrine_count: int
    doctrine_hash: str
    semantic_version: str
    semantic_hash: str
    search_index_stats: Dict[str, Any]
    telemetry: Dict[str, Any]
    timestamp: str


# ############################################################################
#
# SECTION 3: AUTHORITY HARDENING (TIE-20 Component #4)
#
# ############################################################################

def enforce_authority_gate(requested_level: float) -> bool:
    """Enforce authority gate - only allow queries at or above gate level."""
    return requested_level >= AUTHORITY_GATE


def authority_gate_middleware(request_level: float) -> None:
    """Middleware that raises HTTP 403 if authority level is insufficient."""
    if not enforce_authority_gate(request_level):
        raise HTTPException(
            status_code=403,
            detail=f"Authority level {request_level} is below gate threshold {AUTHORITY_GATE}. "
                   f"Engine {ENGINE_ID} requires authority >= {AUTHORITY_GATE}.",
        )


# ############################################################################
#
# SECTION 4: ZONE ANALYSIS (TIE-20 Component #13)
#
# ############################################################################

class IPZone(str, Enum):
    """IP analysis zones for structured reasoning."""
    PATENTABILITY = "patentability"
    PROSECUTION = "prosecution"
    INFRINGEMENT = "infringement"
    VALIDITY = "validity"
    TRADEMARK_CLEARANCE = "trademark_clearance"
    TRADEMARK_ENFORCEMENT = "trademark_enforcement"
    COPYRIGHT_PROTECTION = "copyright_protection"
    COPYRIGHT_DEFENSE = "copyright_defense"
    TRADE_SECRET_PROTECTION = "trade_secret_protection"
    TRADE_SECRET_LITIGATION = "trade_secret_litigation"
    LICENSING = "licensing"
    VALUATION = "valuation"
    FTO = "fto"
    PORTFOLIO = "portfolio"
    INTERNATIONAL = "international"
    DESIGN_PATENT = "design_patent"
    OPEN_SOURCE = "open_source"


ZONE_DOCTRINE_MAP: Dict[str, List[str]] = {
    "patentability": [
        "patentable_subject_matter_101", "novelty_102",
        "non_obviousness_103", "written_description_enablement_112",
    ],
    "prosecution": [
        "patent_prosecution_strategy", "written_description_enablement_112",
    ],
    "infringement": [
        "patent_infringement_271", "claim_construction", "patent_damages",
    ],
    "validity": [
        "novelty_102", "non_obviousness_103",
        "written_description_enablement_112", "inter_partes_review",
    ],
    "trademark_clearance": [
        "trademark_distinctiveness", "likelihood_of_confusion",
    ],
    "trademark_enforcement": [
        "likelihood_of_confusion", "trademark_dilution", "trade_dress_protection",
    ],
    "copyright_protection": [
        "copyright_originality_fixation", "copyright_infringement_analysis",
    ],
    "copyright_defense": [
        "fair_use_defense", "dmca_framework",
    ],
    "trade_secret_protection": [
        "trade_secret_elements",
    ],
    "trade_secret_litigation": [
        "trade_secret_misappropriation",
    ],
    "licensing": [
        "ip_licensing_frameworks",
    ],
    "valuation": [
        "ip_valuation_methods",
    ],
    "fto": [
        "freedom_to_operate_analysis", "patent_infringement_271", "claim_construction",
    ],
    "portfolio": [
        "patent_prosecution_strategy", "ip_licensing_frameworks", "ip_valuation_methods",
    ],
    "international": [
        "pct_international_filing",
    ],
    "design_patent": [
        "design_patent_law",
    ],
    "open_source": [
        "ip_licensing_frameworks",
    ],
}


def detect_zones(norm_result: NormalizationResult) -> List[str]:
    """Detect applicable IP zones from normalized query."""
    zones: Set[str] = set()
    ip_type = norm_result.detected_ip_type
    categories = set(norm_result.detected_categories)
    tokens = set(t.lower() for t in norm_result.tokens)

    # Direct IP type mapping
    type_zone_map = {
        "patent": ["patentability", "prosecution"],
        "trademark": ["trademark_clearance"],
        "copyright": ["copyright_protection"],
        "trade_secret": ["trade_secret_protection"],
        "licensing": ["licensing"],
        "international": ["international"],
        "fto": ["fto"],
        "portfolio": ["portfolio"],
        "valuation": ["valuation"],
        "infringement": ["infringement"],
        "open_source": ["open_source"],
    }
    if ip_type and ip_type in type_zone_map:
        zones.update(type_zone_map[ip_type])

    # Keyword-based zone detection
    keyword_zones = {
        "infringement": ["infringement"],
        "infringe": ["infringement"],
        "validity": ["validity"],
        "invalid": ["validity"],
        "ipr": ["validity"],
        "ptab": ["validity"],
        "prosecution": ["prosecution"],
        "file": ["prosecution"],
        "claim": ["infringement", "prosecution"],
        "fto": ["fto"],
        "freedom": ["fto"],
        "clearance": ["trademark_clearance", "fto"],
        "dilution": ["trademark_enforcement"],
        "fair_use": ["copyright_defense"],
        "dmca": ["copyright_defense"],
        "misappropriation": ["trade_secret_litigation"],
        "license": ["licensing"],
        "royalty": ["licensing"],
        "valuation": ["valuation"],
        "portfolio": ["portfolio"],
        "pct": ["international"],
        "design": ["design_patent"],
        "open_source": ["open_source"],
        "gpl": ["open_source"],
        "damages": ["infringement"],
    }
    for token in tokens:
        if token in keyword_zones:
            zones.update(keyword_zones[token])

    return sorted(zones) if zones else ["patentability"]


# ############################################################################
#
# SECTION 5: FACT FRAGILITY SCORING (TIE-20 Component #14)
#
# ############################################################################

@dataclass
class FactFragilityAssessment:
    """Assessment of how fragile (changeable) a legal fact/position is."""
    fact_text: str
    fragility_score: float  # 0.0 = rock solid, 1.0 = extremely fragile
    fragility_factors: List[str]
    stability_factors: List[str]
    recommended_monitoring: List[str]
    ip_category: str

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "fact_text": self.fact_text[:200],
            "fragility_score": round(self.fragility_score, 4),
            "fragility_factors": self.fragility_factors,
            "stability_factors": self.stability_factors,
            "recommended_monitoring": self.recommended_monitoring,
            "ip_category": self.ip_category,
        }


class FactFragilityScorer:
    """Scores the fragility of IP legal positions."""

    FRAGILITY_INDICATORS: ClassVar[Dict[str, float]] = {
        "circuit_split": 0.35,
        "scotus_cert_pending": 0.40,
        "en_banc_rehearing": 0.30,
        "recent_legislative_change": 0.25,
        "evolving_case_law": 0.20,
        "ptab_precedential": 0.15,
        "mpep_revision": 0.15,
        "alice_101_uncertainty": 0.30,
        "new_administration": 0.10,
        "international_treaty_change": 0.15,
        "ai_generated_content_uncertainty": 0.35,
    }

    STABILITY_INDICATORS: ClassVar[Dict[str, float]] = {
        "scotus_settled": -0.35,
        "unanimous_circuits": -0.30,
        "longstanding_precedent": -0.25,
        "statutory_clarity": -0.20,
        "mpep_established": -0.15,
        "black_letter_law": -0.40,
        "consistent_ptab_decisions": -0.15,
    }

    def score(self, content: str, ip_category: str, doctrine_age_days: int = 0) -> FactFragilityAssessment:
        """Score the fragility of an IP position."""
        base_score = 0.3
        fragility_factors: List[str] = []
        stability_factors: List[str] = []
        monitoring: List[str] = []
        content_lower = content.lower()

        # Check fragility indicators
        for indicator, weight in self.FRAGILITY_INDICATORS.items():
            readable = indicator.replace("_", " ")
            if self._indicator_present(content_lower, indicator):
                base_score += weight
                fragility_factors.append(readable)
                monitoring.append(f"Monitor: {readable}")

        # Check stability indicators
        for indicator, weight in self.STABILITY_INDICATORS.items():
            readable = indicator.replace("_", " ")
            if self._indicator_present(content_lower, indicator):
                base_score += weight
                stability_factors.append(readable)

        # Age factor
        if doctrine_age_days > 180:
            age_penalty = min((doctrine_age_days - 180) / 365.0, 0.2)
            base_score += age_penalty
            fragility_factors.append(f"Doctrine age: {doctrine_age_days} days")
            monitoring.append("Review doctrine for recent developments")

        # Category-specific adjustments
        category_adjustments = {
            "patent": 0.0,
            "trademark": -0.05,  # TM law more stable
            "copyright": 0.05,   # Fair use evolving
            "trade_secret": -0.05,
            "licensing": -0.05,
            "international": 0.10,  # More volatile
        }
        base_score += category_adjustments.get(ip_category, 0.0)

        final_score = max(0.0, min(1.0, base_score))

        if not monitoring:
            monitoring.append("Standard periodic review recommended")

        return FactFragilityAssessment(
            fact_text=content[:200],
            fragility_score=final_score,
            fragility_factors=fragility_factors,
            stability_factors=stability_factors,
            recommended_monitoring=monitoring,
            ip_category=ip_category,
        )

    def _indicator_present(self, text: str, indicator: str) -> bool:
        """Check if a fragility/stability indicator is present in text."""
        keywords = indicator.replace("_", " ").split()
        return all(kw in text for kw in keywords)


# ############################################################################
#
# SECTION 6: DOCTRINE DRIFT WATCHER (TIE-20 Component #9)
#
# ############################################################################

class DoctrineDriftWatcher:
    """Monitors doctrine cache for staleness and drift signals."""

    def __init__(self) -> None:
        self._drift_registry: Dict[str, Dict[str, Any]] = {}
        self._staleness_threshold_days: int = ENGINE_CONFIG.get("drift_watcher", {}).get("staleness_threshold_days", 90)
        self._confidence_reduction: float = ENGINE_CONFIG.get("drift_watcher", {}).get("confidence_reduction_percent", 10) / 100.0
        self._signal_types: List[str] = ENGINE_CONFIG.get("drift_watcher", {}).get("signal_types", [])
        logger.info(f"DoctrineDriftWatcher initialized | threshold={self._staleness_threshold_days}d")

    def check_staleness(self, topic: str, last_updated: str) -> Dict[str, Any]:
        """Check if a doctrine topic is stale."""
        try:
            updated_dt = datetime.fromisoformat(last_updated)
            if updated_dt.tzinfo is None:
                updated_dt = updated_dt.replace(tzinfo=timezone.utc)
            age_days = (datetime.now(timezone.utc) - updated_dt).days
        except (ValueError, TypeError):
            age_days = 999

        is_stale = age_days > self._staleness_threshold_days
        confidence_penalty = self._confidence_reduction if is_stale else 0.0

        return {
            "topic": topic,
            "age_days": age_days,
            "threshold_days": self._staleness_threshold_days,
            "is_stale": is_stale,
            "confidence_penalty": confidence_penalty,
            "recommendation": "Review and update doctrine" if is_stale else "Current",
        }

    def check_all(self) -> List[Dict[str, Any]]:
        """Check all doctrines for staleness."""
        results: List[Dict[str, Any]] = []
        for block in DOCTRINE_CACHE:
            result = self.check_staleness(block["topic"], block.get("last_updated", "2020-01-01"))
            results.append(result)
        return results

    def register_drift_signal(self, topic: str, signal_type: str, description: str) -> str:
        """Register a drift signal for a doctrine topic."""
        signal_id = str(uuid.uuid4())
        self._drift_registry[signal_id] = {
            "topic": topic,
            "signal_type": signal_type,
            "description": description,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "resolved": False,
        }
        record_doctrine_mutation(
            mutation_type=MutationType.DRIFT_DETECTED,
            origin=MutationOrigin.DRIFT_WATCHER,
            topic=topic,
            description=description,
            ip_category=None,
        )
        logger.warning(f"Drift signal registered: {topic} - {signal_type}: {description}")
        return signal_id

    def get_active_signals(self) -> List[Dict[str, Any]]:
        """Get all active (unresolved) drift signals."""
        return [
            {"signal_id": sid, **data}
            for sid, data in self._drift_registry.items()
            if not data.get("resolved", False)
        ]

    def get_stats(self) -> Dict[str, Any]:
        """Get drift watcher statistics."""
        total_signals = len(self._drift_registry)
        active_signals = sum(1 for d in self._drift_registry.values() if not d.get("resolved", False))
        return {
            "total_signals": total_signals,
            "active_signals": active_signals,
            "threshold_days": self._staleness_threshold_days,
            "signal_types": self._signal_types,
        }


# ############################################################################
#
# SECTION 7: DOCTRINE COVERAGE MAP (TIE-20 Component #10)
#
# ############################################################################

class DoctrineCoverageMap:
    """Maps coverage of IP doctrine topics to identify gaps."""

    IP_TOPIC_UNIVERSE: ClassVar[Dict[str, List[str]]] = {
        "patent": [
            "patentable_subject_matter_101", "novelty_102", "non_obviousness_103",
            "written_description_enablement_112", "claim_construction",
            "patent_infringement_271", "patent_damages", "inter_partes_review",
            "design_patent_law", "patent_prosecution_strategy",
        ],
        "trademark": [
            "trademark_distinctiveness", "likelihood_of_confusion",
            "trademark_dilution", "trade_dress_protection",
        ],
        "copyright": [
            "copyright_originality_fixation", "fair_use_defense",
            "copyright_infringement_analysis", "dmca_framework",
        ],
        "trade_secret": [
            "trade_secret_elements", "trade_secret_misappropriation",
        ],
        "licensing": [
            "ip_licensing_frameworks",
        ],
        "valuation": [
            "ip_valuation_methods",
        ],
        "international": [
            "pct_international_filing",
        ],
        "fto": [
            "freedom_to_operate_analysis",
        ],
    }

    def __init__(self) -> None:
        self._covered_topics: Set[str] = set()
        self._refresh()

    def _refresh(self) -> None:
        """Refresh coverage from doctrine cache."""
        self._covered_topics = {block["topic"] for block in DOCTRINE_CACHE}

    def get_coverage(self) -> Dict[str, Any]:
        """Get full coverage analysis."""
        self._refresh()
        coverage_by_category: Dict[str, Dict[str, Any]] = {}
        total_expected = 0
        total_covered = 0

        for category, expected_topics in self.IP_TOPIC_UNIVERSE.items():
            covered = [t for t in expected_topics if t in self._covered_topics]
            missing = [t for t in expected_topics if t not in self._covered_topics]
            total_expected += len(expected_topics)
            total_covered += len(covered)

            coverage_by_category[category] = {
                "expected": len(expected_topics),
                "covered": len(covered),
                "missing": len(missing),
                "coverage_pct": round(len(covered) / max(len(expected_topics), 1) * 100, 1),
                "covered_topics": covered,
                "missing_topics": missing,
            }

        overall_pct = round(total_covered / max(total_expected, 1) * 100, 1)

        return {
            "overall_coverage_pct": overall_pct,
            "total_expected": total_expected,
            "total_covered": total_covered,
            "total_missing": total_expected - total_covered,
            "by_category": coverage_by_category,
        }


# ############################################################################
#
# SECTION 8: DETERMINISM HASH (TIE-20 Component #16)
#
# ############################################################################

def compute_determinism_hash(
    query: str,
    response_content: str,
    doctrine_topics: List[str],
    confidence: float,
    mode: str,
) -> str:
    """Compute SHA-256 determinism hash for response verification."""
    hash_input = json.dumps({
        "engine_id": ENGINE_ID,
        "engine_version": ENGINE_VERSION,
        "query": query.strip().lower(),
        "response_content_hash": hashlib.sha256(response_content.encode("utf-8")).hexdigest(),
        "doctrine_topics": sorted(doctrine_topics),
        "confidence": round(confidence, 4),
        "mode": mode,
    }, sort_keys=True)
    return hashlib.sha256(hash_input.encode("utf-8")).hexdigest()


# ############################################################################
#
# SECTION 9: MULTI-DOCTRINE DECOMPOSITION (TIE-20 Component #19)
#
# ############################################################################

class MultiDoctrineDecomposer:
    """Decomposes complex IP queries into multiple doctrine analyses."""

    def decompose(self, norm_result: NormalizationResult, zones: List[str]) -> List[Dict[str, Any]]:
        """Break a complex query into sub-analyses mapped to doctrine topics."""
        sub_analyses: List[Dict[str, Any]] = []
        engine = get_doctrine_engine()

        for zone in zones:
            topic_ids = ZONE_DOCTRINE_MAP.get(zone, [])
            for topic_id in topic_ids:
                doctrine = engine.lookup(topic_id)
                if doctrine:
                    sub_analyses.append({
                        "zone": zone,
                        "topic": topic_id,
                        "title": doctrine.title,
                        "category": doctrine.category,
                        "confidence": doctrine.confidence,
                        "relevance": self._compute_relevance(norm_result, doctrine),
                    })

        sub_analyses.sort(key=lambda x: x["relevance"], reverse=True)
        return sub_analyses

    def _compute_relevance(self, norm_result: NormalizationResult, doctrine: DoctrineResponse) -> float:
        """Compute relevance of a doctrine to the normalized query."""
        token_set = set(t.lower() for t in norm_result.tokens)
        tag_set = set(doctrine.tags)
        tag_overlap = len(token_set.intersection(tag_set))

        category_match = 1.0 if norm_result.detected_ip_type == doctrine.category else 0.0
        content_hits = sum(1 for t in token_set if t in doctrine.content.lower())

        return (
            tag_overlap * 0.4 +
            category_match * 0.3 +
            min(content_hits * 0.1, 0.3)
        )


# ############################################################################
#
# SECTION 10: DEEP ANALYSIS MODE (TIE-20 Component #20)
#
# ############################################################################

class DeepAnalysisEngine:
    """Performs deep multi-source IP analysis combining doctrines, search, and specialized modules."""

    def __init__(self) -> None:
        self._fragility_scorer = FactFragilityScorer()
        self._decomposer = MultiDoctrineDecomposer()

    def analyze(
        self,
        query: str,
        norm_result: NormalizationResult,
        zones: List[str],
        doctrine_results: List[DoctrineResponse],
        search_results: List[SearchResult],
    ) -> Dict[str, Any]:
        """Perform deep analysis combining all available intelligence."""
        start = time.monotonic()

        # Decompose into sub-analyses
        sub_analyses = self._decomposer.decompose(norm_result, zones)

        # Compute fragility for each doctrine result
        fragility_assessments: List[Dict[str, Any]] = []
        for doctrine in doctrine_results:
            assessment = self._fragility_scorer.score(
                doctrine.content,
                doctrine.category,
                doctrine_age_days=self._compute_age_days(doctrine.last_updated),
            )
            fragility_assessments.append(assessment.to_dict())

        # Build synthesis
        synthesis = self._synthesize(norm_result, doctrine_results, search_results, zones)

        # Risk matrix
        risk_matrix = self._build_risk_matrix(doctrine_results, fragility_assessments)

        # Recommendations
        recommendations = self._generate_recommendations(
            norm_result, doctrine_results, fragility_assessments, risk_matrix
        )

        duration = (time.monotonic() - start) * 1000.0

        return {
            "deep_analysis": True,
            "zones_analyzed": zones,
            "sub_analyses": sub_analyses[:10],
            "fragility_assessments": fragility_assessments,
            "synthesis": synthesis,
            "risk_matrix": risk_matrix,
            "recommendations": recommendations,
            "analysis_time_ms": round(duration, 3),
        }

    def _synthesize(
        self,
        norm_result: NormalizationResult,
        doctrines: List[DoctrineResponse],
        search_results: List[SearchResult],
        zones: List[str],
    ) -> Dict[str, Any]:
        """Synthesize findings across doctrines and search results."""
        all_citations: List[str] = []
        all_authorities: Set[str] = set()
        categories_covered: Set[str] = set()
        avg_confidence = 0.0

        for d in doctrines:
            all_citations.extend(d.citations)
            all_authorities.add(d.authority)
            categories_covered.add(d.category)
            avg_confidence += d.confidence

        if doctrines:
            avg_confidence /= len(doctrines)

        return {
            "total_doctrines_consulted": len(doctrines),
            "total_search_results": len(search_results),
            "categories_covered": sorted(categories_covered),
            "zones_analyzed": zones,
            "unique_citations": len(set(all_citations)),
            "unique_authorities": len(all_authorities),
            "average_confidence": round(avg_confidence, 4),
            "confidence_band": classify_confidence(avg_confidence),
            "ip_type": norm_result.detected_ip_type,
            "key_citations": list(set(all_citations))[:15],
        }

    def _build_risk_matrix(
        self,
        doctrines: List[DoctrineResponse],
        fragility_assessments: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Build a risk matrix from doctrines and fragility."""
        risk_levels: Dict[str, int] = {"low": 0, "medium": 0, "high": 0, "critical": 0}

        for assessment in fragility_assessments:
            score = assessment.get("fragility_score", 0.5)
            if score >= 0.7:
                risk_levels["critical"] += 1
            elif score >= 0.5:
                risk_levels["high"] += 1
            elif score >= 0.3:
                risk_levels["medium"] += 1
            else:
                risk_levels["low"] += 1

        total = sum(risk_levels.values())
        overall = "low"
        if risk_levels["critical"] > 0:
            overall = "critical"
        elif risk_levels["high"] > total * 0.3:
            overall = "high"
        elif risk_levels["medium"] > total * 0.5:
            overall = "medium"

        return {
            "overall_risk": overall,
            "risk_distribution": risk_levels,
            "total_assessed": total,
        }

    def _generate_recommendations(
        self,
        norm_result: NormalizationResult,
        doctrines: List[DoctrineResponse],
        fragility_assessments: List[Dict[str, Any]],
        risk_matrix: Dict[str, Any],
    ) -> List[str]:
        """Generate actionable recommendations based on analysis."""
        recs: List[str] = []
        ip_type = norm_result.detected_ip_type

        if ip_type == "patent":
            recs.append("Conduct thorough prior art search before filing.")
            recs.append("Draft claims at multiple levels of breadth for prosecution flexibility.")
            recs.append("Consider provisional application to secure early filing date.")
        elif ip_type == "trademark":
            recs.append("Perform comprehensive trademark clearance search including TESS, common law, and state registrations.")
            recs.append("Evaluate distinctiveness spectrum position of proposed mark.")
            recs.append("Consider filing intent-to-use application for early priority.")
        elif ip_type == "copyright":
            recs.append("Register copyright with USCO for statutory damages and attorney fees eligibility.")
            recs.append("Document creation process for authorship evidence.")
        elif ip_type == "trade_secret":
            recs.append("Implement comprehensive reasonable measures program.")
            recs.append("Use NDAs, access controls, and exit interviews.")
        elif ip_type == "fto":
            recs.append("Map all claim elements to product features systematically.")
            recs.append("Evaluate design-around options for high-risk claims.")
            recs.append("Consider obtaining non-infringement opinion from patent counsel.")

        if risk_matrix.get("overall_risk") in ("high", "critical"):
            recs.append("ELEVATED RISK: Consult with specialized IP counsel before proceeding.")

        for assessment in fragility_assessments:
            if assessment.get("fragility_score", 0) > 0.6:
                recs.append(f"Monitor developments in: {assessment.get('ip_category', 'IP law')}")
                break

        return recs

    def _compute_age_days(self, last_updated: str) -> int:
        """Compute age in days from last_updated string."""
        try:
            dt = datetime.fromisoformat(last_updated)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return (datetime.now(timezone.utc) - dt).days
        except (ValueError, TypeError):
            return 365


# ############################################################################
#
# SECTION 11: THREE-LAYER RESPONSE ENGINE (TIE-20 Component #1)
#
# ############################################################################

class ThreeLayerResponseEngine:
    """Processes queries through the three-layer architecture.

    Layer 1: Doctrine Cache (fast, pre-compiled)
    Layer 2: Semantic Search (TF-IDF over doctrine blocks)
    Layer 3: IP Analysis (structured analysis with specialized modules)
    Layer 4: Deep Analysis (multi-doctrine synthesis, on-demand)
    """

    def __init__(self) -> None:
        self._doctrine_engine = get_doctrine_engine()
        self._search_index = get_search_index()
        self._drift_watcher = DoctrineDriftWatcher()
        self._coverage_map = DoctrineCoverageMap()
        self._deep_analysis = DeepAnalysisEngine()
        self._fragility_scorer = FactFragilityScorer()
        self._index_doctrines()

    def _index_doctrines(self) -> None:
        """Index all doctrine blocks into the search index."""
        for block in DOCTRINE_CACHE:
            self._search_index.add_document(
                doc_id=block["topic"],
                topic=block["topic"],
                content=f"{block['title']} {block['content']}",
                ip_category=block["category"],
                authority_score=block["confidence"],
                metadata={"tags": block.get("tags", []), "authority": block.get("authority", "")},
            )
        logger.info(f"Indexed {len(DOCTRINE_CACHE)} doctrine blocks into search index")

    def process_query(
        self,
        query: str,
        mode: ResponseMode,
        ip_category_filter: Optional[str] = None,
        max_results: int = 5,
        enable_deep: bool = False,
    ) -> Dict[str, Any]:
        """Process an IP query through all layers."""
        start = time.monotonic()
        query_hash = compute_query_hash(query)
        trace = trace_query(query, query_hash, mode.value)

        try:
            # Step 1: Semantic normalization
            step_norm = trace.add_step("semantic_normalization", ResponseLayer.DOCTRINE_CACHE)
            norm_result = normalize_query(query)
            step_norm.complete()
            step_norm.metadata = {"matched_terms": len(norm_result.matched_terms), "ip_type": norm_result.detected_ip_type}

            # Step 2: Zone detection
            zones = detect_zones(norm_result)

            # Step 3: Doctrine cache lookup (Layer 1)
            step_doctrine = trace.add_step("doctrine_lookup", ResponseLayer.DOCTRINE_CACHE)
            doctrine_results = self._query_doctrines(norm_result, zones, ip_category_filter, max_results)
            step_doctrine.complete()
            step_doctrine.metadata = {"hits": len(doctrine_results)}
            trace.doctrine_hits = len(doctrine_results)

            # Step 4: Semantic search (Layer 2)
            step_search = trace.add_step("semantic_search", ResponseLayer.SEMANTIC_SEARCH)
            search_results = self._search_index.search(
                query_tokens=norm_result.tokens,
                top_k=max_results,
                ip_category_filter=ip_category_filter,
            )
            step_search.complete()
            step_search.metadata = {"results": len(search_results)}
            trace.search_results = len(search_results)

            # Step 5: Compute confidence
            confidence = self._compute_confidence(doctrine_results, search_results, norm_result)
            confidence_band = classify_confidence(confidence)
            trace.confidence_score = confidence
            trace.confidence_band = confidence_band
            trace.ip_category = norm_result.detected_ip_type

            # Step 6: Build response content
            response_content = self._build_response_content(doctrine_results, search_results, mode)

            # Step 7: Epistemic guardrails
            cleaned_content, violations = apply_epistemic_guardrails(response_content)

            # Step 8: Deep analysis (Layer 4, if requested)
            deep_result = None
            if enable_deep and mode in (ResponseMode.MEMO, ResponseMode.FTO, ResponseMode.PORTFOLIO):
                step_deep = trace.add_step("deep_analysis", ResponseLayer.DEEP_ANALYSIS)
                deep_result = self._deep_analysis.analyze(
                    query, norm_result, zones, doctrine_results, search_results
                )
                step_deep.complete()

            # Step 9: Collect citations
            all_citations = self._collect_citations(doctrine_results, search_results)

            # Step 10: Disclaimers
            disclaimers = self._get_disclaimers(mode, norm_result)

            # Step 11: Determinism hash
            doctrine_topics = [d.topic for d in doctrine_results]
            det_hash = compute_determinism_hash(query, cleaned_content, doctrine_topics, confidence, mode.value)

            # Step 12: IP metrics
            self._record_ip_metrics(norm_result)

            # Determine final layer
            final_layer = ResponseLayer.DOCTRINE_CACHE
            if deep_result:
                final_layer = ResponseLayer.DEEP_ANALYSIS
            elif search_results:
                final_layer = ResponseLayer.SEMANTIC_SEARCH

            complete_trace(trace, final_layer)
            total_time = (time.monotonic() - start) * 1000.0

            return {
                "query_hash": query_hash,
                "response_mode": mode.value,
                "ip_category": norm_result.detected_ip_type,
                "confidence": confidence,
                "confidence_band": confidence_band,
                "doctrine_results": [d.to_dict() for d in doctrine_results],
                "search_results": [s.to_dict() for s in search_results],
                "analysis": {
                    "zones": zones,
                    "normalization": norm_result.to_dict(),
                    "content": cleaned_content,
                },
                "deep_analysis": deep_result,
                "citations": all_citations,
                "disclaimers": disclaimers,
                "epistemic_violations": violations,
                "determinism_hash": det_hash,
                "response_time_ms": round(total_time, 3),
                "layer": final_layer.value,
                "telemetry": {
                    "trace_id": trace.trace_id,
                    "steps": len(trace.steps),
                    "doctrine_hits": trace.doctrine_hits,
                    "search_results": trace.search_results,
                },
            }

        except Exception as exc:
            error_msg = f"Query processing error: {str(exc)}"
            logger.error(f"{error_msg}\n{traceback.format_exc()}")
            log_error(ErrorDomain.SYSTEM, error_msg, {"query": query[:200]})
            complete_trace(trace, ResponseLayer.ERROR)
            raise HTTPException(status_code=500, detail=error_msg) from exc

    def _query_doctrines(
        self,
        norm_result: NormalizationResult,
        zones: List[str],
        category_filter: Optional[str],
        max_results: int,
    ) -> List[DoctrineResponse]:
        """Query doctrine cache using normalized tokens and zones."""
        results: List[DoctrineResponse] = []
        seen_topics: Set[str] = set()

        # Zone-based lookup
        for zone in zones:
            topic_ids = ZONE_DOCTRINE_MAP.get(zone, [])
            for topic_id in topic_ids:
                if topic_id in seen_topics:
                    continue
                doctrine = self._doctrine_engine.lookup(topic_id)
                if doctrine:
                    if category_filter and doctrine.category != category_filter:
                        continue
                    results.append(doctrine)
                    seen_topics.add(topic_id)

        # Token-based search
        if len(results) < max_results:
            token_results = self._doctrine_engine.search_by_tokens(
                norm_result.tokens,
                top_k=max_results - len(results),
            )
            for tr in token_results:
                if tr.topic not in seen_topics:
                    if category_filter and tr.category != category_filter:
                        continue
                    results.append(tr)
                    seen_topics.add(tr.topic)

        # Apply staleness penalties
        for result in results:
            staleness = self._drift_watcher.check_staleness(result.topic, result.last_updated)
            if staleness["is_stale"]:
                result.confidence = max(0.0, result.confidence - staleness["confidence_penalty"])
                result.confidence_band = classify_confidence(result.confidence)

        return results[:max_results]

    def _compute_confidence(
        self,
        doctrines: List[DoctrineResponse],
        search_results: List[SearchResult],
        norm_result: NormalizationResult,
    ) -> float:
        """Compute overall response confidence."""
        if not doctrines and not search_results:
            return 0.15

        doctrine_conf = sum(d.confidence for d in doctrines) / max(len(doctrines), 1)
        search_conf = sum(s.score for s in search_results) / max(len(search_results), 1)
        norm_conf = norm_result.confidence

        return (
            doctrine_conf * 0.5 +
            search_conf * 0.2 +
            norm_conf * 0.3
        )

    def _build_response_content(
        self,
        doctrines: List[DoctrineResponse],
        search_results: List[SearchResult],
        mode: ResponseMode,
    ) -> str:
        """Build textual response content from results."""
        parts: List[str] = []
        for d in doctrines:
            if mode == ResponseMode.FAST:
                parts.append(f"[{d.title}] {d.content[:300]}...")
            elif mode in (ResponseMode.ANALYSIS, ResponseMode.MEMO, ResponseMode.FTO, ResponseMode.PORTFOLIO):
                parts.append(f"## {d.title}\n\n{d.content}\n\nAuthority: {d.authority}\nConfidence: {d.confidence_band} ({d.confidence:.2f})")
        return "\n\n".join(parts)

    def _collect_citations(
        self,
        doctrines: List[DoctrineResponse],
        search_results: List[SearchResult],
    ) -> List[str]:
        """Collect unique citations from all results."""
        citations: Set[str] = set()
        for d in doctrines:
            citations.update(d.citations)
        return sorted(citations)

    def _get_disclaimers(self, mode: ResponseMode, norm_result: NormalizationResult) -> List[str]:
        """Get applicable disclaimers for the response."""
        disclaimers: List[str] = [REQUIRED_DISCLAIMERS.get("not_legal_advice", "")]
        if norm_result.detected_ip_type in ("international", None):
            disclaimers.append(REQUIRED_DISCLAIMERS.get("jurisdiction_specific", ""))
        disclaimers.append(REQUIRED_DISCLAIMERS.get("fact_dependent", ""))
        if norm_result.detected_ip_type == "patent":
            disclaimers.append(REQUIRED_DISCLAIMERS.get("prior_art_caveat", ""))
        return [d for d in disclaimers if d]

    def _record_ip_metrics(self, norm_result: NormalizationResult) -> None:
        """Record IP-specific telemetry metrics."""
        telemetry = get_telemetry()
        ip_type = norm_result.detected_ip_type
        metric_map = {
            "patent": IPMetricType.PATENT_QUERY,
            "trademark": IPMetricType.TRADEMARK_QUERY,
            "copyright": IPMetricType.COPYRIGHT_QUERY,
            "trade_secret": IPMetricType.TRADE_SECRET_QUERY,
            "infringement": IPMetricType.INFRINGEMENT_CHECK,
            "fto": IPMetricType.FTO_ANALYSIS,
            "licensing": IPMetricType.LICENSING_ANALYSIS,
            "portfolio": IPMetricType.PORTFOLIO_REVIEW,
            "valuation": IPMetricType.VALUATION,
        }
        if ip_type and ip_type in metric_map:
            telemetry.record_ip_metric(metric_map[ip_type])

    def get_coverage(self) -> Dict[str, Any]:
        """Get doctrine coverage map."""
        return self._coverage_map.get_coverage()

    def get_drift_status(self) -> List[Dict[str, Any]]:
        """Get drift watcher status."""
        return self._drift_watcher.check_all()


# ############################################################################
#
# SECTION 12: FASTAPI APPLICATION (TIE-20 Component #17)
#
# ############################################################################

# ============================================================================
# APP LIFESPAN
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    logger.info(f"Starting {ENGINE_NAME} v{ENGINE_VERSION} on port {ENGINE_PORT}")
    logger.info(f"Engine ID: {ENGINE_ID} | Tier: {ENGINE_TIER} | Mode: {ENGINE_MODE}")
    logger.info(f"Authority Level: {AUTHORITY_LEVEL} | Gate: {AUTHORITY_GATE}")
    logger.info(f"Doctrine Cache: {get_doctrine_count()} blocks | Hash: {get_doctrine_hash()[:16]}...")
    logger.info(f"Semantic Map: v{get_semantic_map_version()} | Hash: {get_semantic_map_hash()[:16]}...")

    # Initialize all singletons
    get_telemetry(LOG_DIR)
    get_doctrine_engine()
    get_search_index()
    get_claim_parser()
    get_prior_art_engine()
    get_infringement_mapper()
    get_trademark_engine()

    # Initialize three-layer engine (indexes doctrines)
    app.state.engine = ThreeLayerResponseEngine()

    logger.info(f"{ENGINE_NAME} is OPERATIONAL")
    yield
    logger.info(f"{ENGINE_NAME} shutting down")


# ============================================================================
# APP CREATION
# ============================================================================

app = FastAPI(
    title=f"ECHO OMEGA PRIME - {ENGINE_NAME}",
    description=f"TIE-20 compliant {ENGINE_NAME} for patent, trademark, copyright, and trade secret analysis.",
    version=ENGINE_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ENGINE_CONFIG.get("cors", {}).get("allow_origins", ["*"]),
    allow_credentials=True,
    allow_methods=ENGINE_CONFIG.get("cors", {}).get("allow_methods", ["*"]),
    allow_headers=ENGINE_CONFIG.get("cors", {}).get("allow_headers", ["*"]),
)


# ============================================================================
# DEPENDENCY: Get Engine
# ============================================================================

def get_engine(request: Request) -> ThreeLayerResponseEngine:
    """FastAPI dependency to get the engine instance."""
    return request.app.state.engine


# ============================================================================
# HEALTH ENDPOINT (TIE-20 Component #12)
# ============================================================================

@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    telemetry = get_telemetry()
    health = telemetry.get_health()
    search_stats = get_search_index().get_stats()

    return HealthResponse(
        status="healthy",
        engine_id=ENGINE_ID,
        engine_name=ENGINE_NAME,
        engine_version=ENGINE_VERSION,
        port=ENGINE_PORT,
        tier=ENGINE_TIER,
        mode=ENGINE_MODE,
        authority_level=AUTHORITY_LEVEL,
        uptime_seconds=health.get("uptime_seconds", 0),
        doctrine_count=get_doctrine_count(),
        doctrine_hash=get_doctrine_hash()[:32],
        semantic_version=get_semantic_map_version(),
        semantic_hash=get_semantic_map_hash()[:32],
        search_index_stats=search_stats,
        telemetry=health.get("metrics", {}),
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


@app.get("/")
async def root() -> Dict[str, Any]:
    """Root endpoint with engine info."""
    return {
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "engine_version": ENGINE_VERSION,
        "port": ENGINE_PORT,
        "tier": ENGINE_TIER,
        "mode": ENGINE_MODE,
        "authority_level": AUTHORITY_LEVEL,
        "status": "operational",
        "endpoints": [
            "/health",
            "/query",
            "/claims/analyze",
            "/trademark/search",
            "/prior-art/search",
            "/coverage",
            "/drift",
            "/metrics",
            "/telemetry/traces",
            "/telemetry/mutations",
            "/telemetry/audit/verify",
            "/doctrines",
            "/doctrines/{topic}",
            "/semantic/normalize",
            "/semantic/integrity",
        ],
    }


# ============================================================================
# PRIMARY QUERY ENDPOINT
# ============================================================================

@app.post("/query", response_model=IPQueryResponse)
async def query_ip(
    request: IPQueryRequest,
    engine: ThreeLayerResponseEngine = Depends(get_engine),
) -> IPQueryResponse:
    """Primary IP analysis query endpoint.

    Processes queries through the three-layer architecture:
    1. Doctrine Cache (fast lookup)
    2. Semantic Search (TF-IDF)
    3. IP Analysis (structured)
    4. Deep Analysis (multi-doctrine, on-demand)
    """
    authority_gate_middleware(request.authority_level)

    result = engine.process_query(
        query=request.query,
        mode=request.mode,
        ip_category_filter=request.ip_category.value if request.ip_category else None,
        max_results=request.max_results,
        enable_deep=request.deep_analysis,
    )

    return IPQueryResponse(
        query_hash=result["query_hash"],
        response_mode=result["response_mode"],
        ip_category=result["ip_category"],
        confidence=result["confidence"],
        confidence_band=result["confidence_band"],
        doctrine_results=[DoctrineResultModel(**d) for d in result["doctrine_results"]],
        search_results=[SearchResultModel(
            doc_id=s["doc_id"],
            topic=s["topic"],
            score=s["score"],
            ip_category=s["ip_category"],
            matched_tokens=s["matched_tokens"],
        ) for s in result["search_results"]],
        analysis=result.get("analysis"),
        deep_analysis=result.get("deep_analysis"),
        citations=result["citations"],
        disclaimers=result["disclaimers"],
        epistemic_violations=result["epistemic_violations"],
        normalization=result["analysis"]["normalization"] if result.get("analysis") else {},
        determinism_hash=result["determinism_hash"],
        response_time_ms=result["response_time_ms"],
        layer=result["layer"],
        telemetry=result["telemetry"],
    )


# ============================================================================
# CLAIM ANALYSIS ENDPOINT
# ============================================================================

@app.post("/claims/analyze", response_model=ClaimAnalysisResponse)
async def analyze_claims(request: ClaimAnalysisRequest) -> ClaimAnalysisResponse:
    """Analyze patent claims - parse, infringement, or FTO."""
    start = time.monotonic()
    parser = get_claim_parser()
    claims = parser.parse_claims(request.claims_text)

    infringement_results = None
    if request.analysis_type in ("infringement", "fto") and request.product_features:
        mapper = get_infringement_mapper()
        inf_results = mapper.analyze_infringement(
            patent_id=request.patent_id or "UNKNOWN",
            claims=claims,
            product_features=request.product_features,
            claim_numbers=request.target_claims,
        )
        infringement_results = [r.to_dict() for r in inf_results]

    claim_tree = parser.get_claim_tree(claims)
    independent_claims = parser.get_independent_claims(claims)

    summary = {
        "total_claims": len(claims),
        "independent_claims": len(independent_claims),
        "dependent_claims": len(claims) - len(independent_claims),
        "method_claims": sum(1 for c in claims if c.method_claim),
        "apparatus_claims": sum(1 for c in claims if c.apparatus_claim),
        "system_claims": sum(1 for c in claims if c.system_claim),
        "means_plus_function": sum(1 for c in claims if c.means_plus_function),
        "composition_claims": sum(1 for c in claims if c.composition_claim),
    }

    if infringement_results:
        high_risk = sum(1 for r in infringement_results if r["risk_level"] in ("high", "critical"))
        summary["infringement_high_risk_claims"] = high_risk
        summary["infringement_overall_risk"] = "high" if high_risk > 0 else "low"

    content_for_hash = json.dumps([c.to_dict() for c in claims], sort_keys=True)
    det_hash = hashlib.sha256(content_for_hash.encode("utf-8")).hexdigest()

    return ClaimAnalysisResponse(
        analysis_type=request.analysis_type,
        patent_id=request.patent_id,
        claims=[c.to_dict() for c in claims],
        infringement_results=infringement_results,
        claim_tree=dict(claim_tree) if claim_tree else None,
        summary=summary,
        determinism_hash=det_hash,
        response_time_ms=round((time.monotonic() - start) * 1000.0, 3),
    )


# ============================================================================
# TRADEMARK SEARCH ENDPOINT
# ============================================================================

@app.post("/trademark/search", response_model=TrademarkSearchResponse)
async def search_trademarks(request: TrademarkSearchRequest) -> TrademarkSearchResponse:
    """Trademark clearance search."""
    start = time.monotonic()
    tm_engine = get_trademark_engine()
    conflicts = tm_engine.search(request.proposed_mark, request.nice_classes)

    high_risk = sum(1 for c in conflicts if c["confusion_risk"] > 0.6)
    medium_risk = sum(1 for c in conflicts if 0.35 < c["confusion_risk"] <= 0.6)

    risk_assessment = {
        "total_conflicts": len(conflicts),
        "high_risk_conflicts": high_risk,
        "medium_risk_conflicts": medium_risk,
        "low_risk_conflicts": len(conflicts) - high_risk - medium_risk,
        "overall_risk": "high" if high_risk > 0 else ("medium" if medium_risk > 0 else "low"),
        "recommended_action": (
            "DO NOT PROCEED without legal counsel review" if high_risk > 0
            else "Proceed with caution - monitor cited marks" if medium_risk > 0
            else "Proceed with standard trademark application"
        ),
    }

    recommendations: List[str] = []
    if high_risk > 0:
        recommendations.append("Consult trademark attorney before filing.")
        recommendations.append("Consider modifying the proposed mark to increase distinctiveness.")
    if request.nice_classes:
        recommendations.append(f"File in Nice Classes: {request.nice_classes}")
    else:
        recommendations.append("Identify specific goods/services to determine Nice Classification.")
    recommendations.append("Consider use-based (1(a)) or intent-to-use (1(b)) application basis.")

    content_for_hash = json.dumps(conflicts, sort_keys=True, default=str)
    det_hash = hashlib.sha256(content_for_hash.encode("utf-8")).hexdigest()

    return TrademarkSearchResponse(
        proposed_mark=request.proposed_mark,
        conflicts=conflicts,
        risk_assessment=risk_assessment,
        recommendations=recommendations,
        determinism_hash=det_hash,
        response_time_ms=round((time.monotonic() - start) * 1000.0, 3),
    )


# ============================================================================
# PRIOR ART SEARCH ENDPOINT
# ============================================================================

@app.post("/prior-art/search", response_model=PriorArtSearchResponse)
async def search_prior_art(request: PriorArtSearchRequest) -> PriorArtSearchResponse:
    """Prior art search endpoint."""
    start = time.monotonic()
    pa_engine = get_prior_art_engine()

    # Tokenize the invention description
    tokens = re.findall(r"\w+", request.invention_description.lower())
    if request.keywords:
        tokens.extend(k.lower() for k in request.keywords)

    references = pa_engine.search(tokens, top_k=request.top_k)

    total_refs = len(references)
    high_anticipation = sum(1 for r in references if r.anticipation_risk > 0.5)
    high_obviousness = sum(1 for r in references if r.obviousness_risk > 0.5)

    risk_summary = {
        "total_references_found": total_refs,
        "high_anticipation_risk": high_anticipation,
        "high_obviousness_risk": high_obviousness,
        "overall_patentability_risk": (
            "high" if high_anticipation > 0
            else "medium" if high_obviousness > 0
            else "low"
        ),
        "recommendation": (
            "Significant prior art exists - review claims for novelty issues"
            if high_anticipation > 0
            else "Prior art suggests potential obviousness - strengthen inventive step arguments"
            if high_obviousness > 0
            else "Limited relevant prior art found - patentability appears favorable"
        ),
    }

    content_for_hash = json.dumps([r.to_dict() for r in references], sort_keys=True)
    det_hash = hashlib.sha256(content_for_hash.encode("utf-8")).hexdigest()

    return PriorArtSearchResponse(
        references=[r.to_dict() for r in references],
        risk_summary=risk_summary,
        determinism_hash=det_hash,
        response_time_ms=round((time.monotonic() - start) * 1000.0, 3),
    )


# ============================================================================
# DOCTRINE ENDPOINTS
# ============================================================================

@app.get("/doctrines")
async def list_doctrines() -> Dict[str, Any]:
    """List all available doctrine topics."""
    engine = get_doctrine_engine()
    return {
        "engine_id": ENGINE_ID,
        "total_doctrines": get_doctrine_count(),
        "topics": engine.get_all_topics(),
        "categories": engine.get_all_categories(),
        "tags": engine.get_all_tags(),
        "stats": engine.get_stats(),
        "hash": get_doctrine_hash()[:32],
    }


@app.get("/doctrines/{topic}")
async def get_doctrine(topic: str) -> Dict[str, Any]:
    """Get a specific doctrine by topic."""
    engine = get_doctrine_engine()
    doctrine = engine.lookup(topic)
    if not doctrine:
        raise HTTPException(status_code=404, detail=f"Doctrine topic '{topic}' not found")
    return doctrine.to_dict()


# ============================================================================
# COVERAGE AND DRIFT ENDPOINTS
# ============================================================================

@app.get("/coverage")
async def get_coverage(engine: ThreeLayerResponseEngine = Depends(get_engine)) -> Dict[str, Any]:
    """Get doctrine coverage map."""
    return engine.get_coverage()


@app.get("/drift")
async def get_drift_status(engine: ThreeLayerResponseEngine = Depends(get_engine)) -> Dict[str, Any]:
    """Get doctrine drift/staleness status."""
    results = engine.get_drift_status()
    stale_count = sum(1 for r in results if r["is_stale"])
    return {
        "engine_id": ENGINE_ID,
        "total_checked": len(results),
        "stale_count": stale_count,
        "current_count": len(results) - stale_count,
        "details": results,
    }


# ============================================================================
# SEMANTIC ENDPOINTS
# ============================================================================

@app.post("/semantic/normalize")
async def normalize_endpoint(query: str = Query(..., min_length=3)) -> Dict[str, Any]:
    """Normalize a query through the semantic map."""
    result = normalize_query(query)
    return result.to_dict()


@app.get("/semantic/integrity")
async def semantic_integrity() -> Dict[str, Any]:
    """Verify semantic dictionary integrity."""
    return verify_dictionary_integrity()


@app.get("/semantic/governance")
async def semantic_governance() -> Dict[str, Any]:
    """Get semantic module governance metadata."""
    return get_semantic_governance()


# ============================================================================
# METRICS AND TELEMETRY ENDPOINTS (TIE-20 Component #11)
# ============================================================================

@app.get("/metrics")
async def get_metrics() -> Dict[str, Any]:
    """Get engine metrics snapshot."""
    telemetry = get_telemetry()
    return telemetry.get_health()


@app.get("/telemetry/traces")
async def get_traces(count: int = Query(default=20, ge=1, le=100)) -> Dict[str, Any]:
    """Get recent query traces."""
    telemetry = get_telemetry()
    return {
        "engine_id": ENGINE_ID,
        "traces": telemetry.get_recent_traces(count),
    }


@app.get("/telemetry/mutations")
async def get_mutations(count: int = Query(default=20, ge=1, le=100)) -> Dict[str, Any]:
    """Get recent doctrine mutations."""
    telemetry = get_telemetry()
    return {
        "engine_id": ENGINE_ID,
        "mutations": telemetry.get_recent_mutations(count),
    }


@app.get("/telemetry/citations")
async def get_citation_lookups(count: int = Query(default=20, ge=1, le=100)) -> Dict[str, Any]:
    """Get recent citation lookups."""
    telemetry = get_telemetry()
    return {
        "engine_id": ENGINE_ID,
        "citations": telemetry.get_recent_citations(count),
    }


@app.get("/telemetry/audit/verify")
async def verify_audit() -> Dict[str, Any]:
    """Verify audit trail hash chain integrity."""
    telemetry = get_telemetry()
    return telemetry.verify_audit_chain()


# ============================================================================
# NICE CLASSIFICATION AND CPC LOOKUP ENDPOINTS
# ============================================================================

@app.get("/nice-classification")
async def nice_classification() -> Dict[str, Any]:
    """Get Nice Classification for trademarks."""
    return {
        "total_classes": len(get_nice_classification()),
        "classes": get_nice_classification(),
    }


@app.get("/cpc-sections")
async def cpc_sections() -> Dict[str, Any]:
    """Get CPC patent classification sections."""
    return {
        "total_sections": len(get_cpc_sections()),
        "sections": get_cpc_sections(),
    }


# ############################################################################
#
# SECTION 13: PATENT PROSECUTION ADVISOR
#
# ############################################################################

class PatentProsecutionAdvisor:
    """Provides structured patent prosecution guidance and strategy.

    Analyzes office actions, suggests responses, and tracks prosecution timelines.
    """

    OFFICE_ACTION_TYPES: ClassVar[Dict[str, Dict[str, Any]]] = {
        "non_final_rejection": {
            "label": "Non-Final Office Action",
            "response_deadline_months": 3,
            "extension_available": True,
            "max_extensions": 3,
            "extension_cost_per_month_usd": 200,
            "strategy": "Address all rejections substantively. Consider interview with examiner. Amend claims if necessary but minimize narrowing.",
        },
        "final_rejection": {
            "label": "Final Office Action",
            "response_deadline_months": 3,
            "extension_available": True,
            "max_extensions": 3,
            "extension_cost_per_month_usd": 200,
            "strategy": "Options: (1) File RCE with amended claims, (2) File appeal to PTAB, (3) File continuation. After-final amendment is possible but rarely entered.",
        },
        "restriction_requirement": {
            "label": "Restriction Requirement",
            "response_deadline_months": 1,
            "extension_available": True,
            "max_extensions": 3,
            "extension_cost_per_month_usd": 200,
            "strategy": "Elect the commercially most valuable invention. File divisional applications for non-elected inventions. Traverse if restriction is improper.",
        },
        "ex_parte_quayle": {
            "label": "Ex Parte Quayle Action",
            "response_deadline_months": 2,
            "extension_available": True,
            "max_extensions": 3,
            "extension_cost_per_month_usd": 200,
            "strategy": "Claims are allowable in substance. Only formal matters to address. Quick response recommended.",
        },
        "notice_of_allowance": {
            "label": "Notice of Allowance",
            "response_deadline_months": 3,
            "extension_available": False,
            "max_extensions": 0,
            "extension_cost_per_month_usd": 0,
            "strategy": "Pay issue fee promptly. Review claims one final time. Consider filing continuation for additional claims before payment.",
        },
    }

    REJECTION_TYPES: ClassVar[Dict[str, Dict[str, Any]]] = {
        "101_abstract_idea": {
            "statute": "35 USC 101",
            "label": "Abstract Idea Rejection",
            "response_strategies": [
                "Argue claims are not directed to an abstract idea under Step 2A Prong One",
                "Show practical application under Step 2A Prong Two (specific technological improvement)",
                "Demonstrate inventive concept under Step 2B (unconventional combination)",
                "Cite recent Federal Circuit cases finding eligibility in similar technology",
                "Amend claims to recite specific technical implementation details",
                "Request interview with examiner to discuss technology specifics",
            ],
            "key_cases": [
                "Enfish v. Microsoft (self-referential table = eligible)",
                "McRO v. Bandai Namco (specific rules for animation = eligible)",
                "Core Wireless v. LG (improved user interface = eligible)",
                "Berkheimer v. HP (inventive concept is factual question)",
            ],
        },
        "102_anticipation": {
            "statute": "35 USC 102",
            "label": "Anticipation Rejection",
            "response_strategies": [
                "Distinguish claims from cited reference on missing element(s)",
                "Argue reference does not disclose element explicitly or inherently",
                "Show reference is not prior art (post-EFD, inventor disclosure exception)",
                "Narrow claims to exclude anticipated embodiment while maintaining scope",
                "Challenge reference date or status as prior art",
                "Submit Rule 1.130 declaration to remove reference under 102(b) exception",
            ],
            "key_cases": [
                "In re Schreiber (anticipation requires every element)",
                "Kennametal v. Ingersoll (inherent disclosure must be necessary)",
                "Helsinn v. Teva (on-sale bar applies even with NDA)",
            ],
        },
        "103_obviousness": {
            "statute": "35 USC 103",
            "label": "Obviousness Rejection",
            "response_strategies": [
                "Argue no motivation to combine references (KSR flexible but requires articulated reasoning)",
                "Show no reasonable expectation of success in combination",
                "Present secondary considerations: commercial success, long-felt need, failure of others",
                "Argue teaching away in one or more references",
                "Challenge characterization of PHOSITA skill level",
                "Show unexpected results from the claimed combination",
                "Amend claims to add distinguishing feature not taught by any reference",
                "Argue references are non-analogous art",
            ],
            "key_cases": [
                "Graham v. John Deere (four-factor framework)",
                "KSR v. Teleflex (flexible TSM, common sense)",
                "In re Soni (teaching away negates combination)",
            ],
        },
        "112a_written_description": {
            "statute": "35 USC 112(a)",
            "label": "Written Description Rejection",
            "response_strategies": [
                "Point to specific passages in specification supporting each claim element",
                "Cite original claims as evidence of possession (if not new matter)",
                "Argue that a PHOSITA would recognize adequate description",
                "Amend claims to align more closely with described embodiments",
                "Add supporting evidence via supplemental declaration",
            ],
            "key_cases": [
                "Ariad v. Eli Lilly (separate written description requirement)",
                "Capon v. Eshhar (genus/species description adequacy)",
            ],
        },
        "112a_enablement": {
            "statute": "35 USC 112(a)",
            "label": "Enablement Rejection",
            "response_strategies": [
                "Address Wands factors: show limited experimentation needed",
                "Provide examples demonstrating practice of full scope of claims",
                "Argue PHOSITA skill level is high enough to fill gaps",
                "Narrow claims to reduce scope to enabled embodiments",
                "Submit additional experimental data or working examples",
            ],
            "key_cases": [
                "In re Wands (8-factor enablement test)",
                "Amgen v. Sanofi (full scope enablement required)",
            ],
        },
        "112b_indefiniteness": {
            "statute": "35 USC 112(b)",
            "label": "Indefiniteness Rejection",
            "response_strategies": [
                "Provide clear definition from specification for disputed term",
                "Amend claim to use more precise language",
                "Cite Nautilus standard: reasonable certainty to PHOSITA",
                "Show term has well-understood meaning in the art",
                "Add explicit antecedent basis for claim terms",
            ],
            "key_cases": [
                "Nautilus v. Biosig (reasonable certainty standard)",
                "Williamson v. Citrix (means-plus-function rebuttable presumption)",
            ],
        },
    }

    MAINTENANCE_FEES: ClassVar[Dict[str, Dict[str, Any]]] = {
        "3_5_year": {
            "label": "3.5 Year Maintenance Fee",
            "due_years": 3.5,
            "large_entity_usd": 2000,
            "small_entity_usd": 1000,
            "micro_entity_usd": 500,
            "grace_period_months": 6,
            "surcharge_usd": 160,
        },
        "7_5_year": {
            "label": "7.5 Year Maintenance Fee",
            "due_years": 7.5,
            "large_entity_usd": 3760,
            "small_entity_usd": 1880,
            "micro_entity_usd": 940,
            "grace_period_months": 6,
            "surcharge_usd": 160,
        },
        "11_5_year": {
            "label": "11.5 Year Maintenance Fee",
            "due_years": 11.5,
            "large_entity_usd": 7700,
            "small_entity_usd": 3850,
            "micro_entity_usd": 1925,
            "grace_period_months": 6,
            "surcharge_usd": 160,
        },
    }

    def get_office_action_strategy(self, action_type: str) -> Dict[str, Any]:
        """Get strategy for responding to a specific office action type."""
        oa_info = self.OFFICE_ACTION_TYPES.get(action_type)
        if not oa_info:
            return {"error": f"Unknown office action type: {action_type}"}
        return {
            "action_type": action_type,
            **oa_info,
        }

    def get_rejection_response(self, rejection_type: str) -> Dict[str, Any]:
        """Get response strategies for a specific rejection type."""
        rej_info = self.REJECTION_TYPES.get(rejection_type)
        if not rej_info:
            return {"error": f"Unknown rejection type: {rejection_type}"}
        return {
            "rejection_type": rejection_type,
            **rej_info,
        }

    def get_maintenance_schedule(self, entity_size: str = "large") -> List[Dict[str, Any]]:
        """Get patent maintenance fee schedule."""
        schedule: List[Dict[str, Any]] = []
        for fee_id, fee_info in self.MAINTENANCE_FEES.items():
            fee_key = f"{entity_size}_entity_usd"
            amount = fee_info.get(fee_key, fee_info.get("large_entity_usd", 0))
            schedule.append({
                "fee_id": fee_id,
                "label": fee_info["label"],
                "due_years_from_grant": fee_info["due_years"],
                "amount_usd": amount,
                "grace_period_months": fee_info["grace_period_months"],
                "surcharge_usd": fee_info["surcharge_usd"],
            })
        return schedule

    def estimate_prosecution_cost(
        self,
        application_type: str = "utility",
        entity_size: str = "large",
        expected_oas: int = 2,
        international: bool = False,
        countries: int = 0,
    ) -> Dict[str, Any]:
        """Estimate total patent prosecution cost."""
        base_costs = {
            "utility": {"filing_fee": 1820, "search_fee": 700, "exam_fee": 800},
            "design": {"filing_fee": 1020, "search_fee": 160, "exam_fee": 600},
            "provisional": {"filing_fee": 320, "search_fee": 0, "exam_fee": 0},
            "plant": {"filing_fee": 1180, "search_fee": 420, "exam_fee": 620},
        }

        costs = base_costs.get(application_type, base_costs["utility"])
        entity_multipliers = {"large": 1.0, "small": 0.5, "micro": 0.25}
        multiplier = entity_multipliers.get(entity_size, 1.0)

        filing = costs["filing_fee"] * multiplier
        search = costs["search_fee"] * multiplier
        exam = costs["exam_fee"] * multiplier
        issue_fee = 1200 * multiplier

        attorney_drafting = 8000 if application_type == "utility" else 4000
        attorney_oa_response = 3000 * expected_oas
        attorney_misc = 1500

        pct_fee = 0
        national_phase_per_country = 0
        if international:
            pct_fee = 4000
            national_phase_per_country = 5000
            translation_per_country = 3000
            total_international = pct_fee + (national_phase_per_country + translation_per_country) * max(countries, 1)
        else:
            total_international = 0
            translation_per_country = 0

        total_domestic = filing + search + exam + issue_fee + attorney_drafting + attorney_oa_response + attorney_misc
        total = total_domestic + total_international

        return {
            "application_type": application_type,
            "entity_size": entity_size,
            "domestic_costs": {
                "filing_fee": round(filing, 2),
                "search_fee": round(search, 2),
                "exam_fee": round(exam, 2),
                "issue_fee": round(issue_fee, 2),
                "attorney_drafting": attorney_drafting,
                "attorney_oa_responses": attorney_oa_response,
                "attorney_misc": attorney_misc,
                "subtotal": round(total_domestic, 2),
            },
            "international_costs": {
                "pct_filing": pct_fee,
                "national_phase_per_country": national_phase_per_country,
                "translation_per_country": translation_per_country,
                "countries": countries,
                "subtotal": round(total_international, 2),
            } if international else None,
            "total_estimated_usd": round(total, 2),
            "note": "Estimates based on typical prosecution. Actual costs vary based on complexity, technology, and attorney rates.",
        }


# ############################################################################
#
# SECTION 14: IP PORTFOLIO ANALYZER
#
# ############################################################################

class IPPortfolioAnalyzer:
    """Analyzes and manages IP portfolios with strategic recommendations.

    Provides portfolio-level analysis including asset categorization,
    competitive positioning, gap analysis, monetization assessment,
    and strategic recommendations.
    """

    PORTFOLIO_HEALTH_METRICS: ClassVar[List[str]] = [
        "total_assets",
        "asset_diversity",
        "geographic_coverage",
        "technology_coverage",
        "competitive_strength",
        "monetization_potential",
        "maintenance_burden",
        "enforcement_readiness",
        "expiration_risk",
        "prior_art_vulnerability",
    ]

    def analyze_portfolio(self, assets: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze an IP portfolio and generate strategic assessment."""
        start = time.monotonic()

        # Categorize assets
        categorized = self._categorize_assets(assets)

        # Compute health metrics
        health = self._compute_health(assets, categorized)

        # Identify gaps
        gaps = self._identify_gaps(categorized)

        # Generate strategic recommendations
        recommendations = self._strategic_recommendations(assets, health, gaps)

        # Monetization assessment
        monetization = self._assess_monetization(assets, categorized)

        # Expiration timeline
        timeline = self._build_expiration_timeline(assets)

        duration = (time.monotonic() - start) * 1000.0

        return {
            "portfolio_size": len(assets),
            "categorization": categorized,
            "health_metrics": health,
            "gaps": gaps,
            "strategic_recommendations": recommendations,
            "monetization_assessment": monetization,
            "expiration_timeline": timeline,
            "analysis_time_ms": round(duration, 3),
        }

    def _categorize_assets(self, assets: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Categorize assets by type, status, and technology area."""
        by_type: Counter = Counter()
        by_status: Counter = Counter()
        by_technology: Counter = Counter()
        by_jurisdiction: Counter = Counter()

        for asset in assets:
            by_type[asset.get("type", "unknown")] += 1
            by_status[asset.get("status", "unknown")] += 1
            by_technology[asset.get("technology_area", "general")] += 1
            by_jurisdiction[asset.get("jurisdiction", "US")] += 1

        return {
            "by_type": dict(by_type),
            "by_status": dict(by_status),
            "by_technology": dict(by_technology),
            "by_jurisdiction": dict(by_jurisdiction),
        }

    def _compute_health(self, assets: List[Dict[str, Any]], categorized: Dict[str, Any]) -> Dict[str, Any]:
        """Compute portfolio health metrics."""
        total = len(assets) if assets else 1

        # Diversity score: how spread across IP types
        type_count = len(categorized.get("by_type", {}))
        diversity = min(type_count / 4.0, 1.0)  # 4 major types = max diversity

        # Geographic coverage
        jurisdiction_count = len(categorized.get("by_jurisdiction", {}))
        geo_coverage = min(jurisdiction_count / 10.0, 1.0)  # 10+ jurisdictions = excellent

        # Technology coverage
        tech_count = len(categorized.get("by_technology", {}))
        tech_coverage = min(tech_count / 5.0, 1.0)

        # Active ratio
        active = sum(1 for a in assets if a.get("status") in ("active", "granted", "registered"))
        active_ratio = active / total

        # Overall health score
        overall = (diversity * 0.2 + geo_coverage * 0.2 + tech_coverage * 0.2 + active_ratio * 0.4)

        return {
            "overall_score": round(overall, 4),
            "overall_grade": self._grade(overall),
            "diversity_score": round(diversity, 4),
            "geographic_coverage": round(geo_coverage, 4),
            "technology_coverage": round(tech_coverage, 4),
            "active_asset_ratio": round(active_ratio, 4),
            "total_assets": total,
            "active_assets": active,
        }

    def _identify_gaps(self, categorized: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify gaps in portfolio coverage."""
        gaps: List[Dict[str, Any]] = []
        desired_types = {"utility_patent", "design_patent", "trademark", "copyright", "trade_secret"}
        existing_types = set(categorized.get("by_type", {}).keys())
        missing = desired_types - existing_types

        for missing_type in missing:
            gaps.append({
                "type": "missing_ip_type",
                "detail": f"No {missing_type.replace('_', ' ')} assets in portfolio",
                "severity": "high" if missing_type in ("utility_patent", "trademark") else "medium",
                "recommendation": f"Consider developing {missing_type.replace('_', ' ')} protection strategy",
            })

        # Check geographic gaps
        jurisdictions = set(categorized.get("by_jurisdiction", {}).keys())
        if "US" not in jurisdictions:
            gaps.append({
                "type": "geographic_gap",
                "detail": "No US IP protection",
                "severity": "critical",
                "recommendation": "Prioritize US filings for market protection",
            })

        key_markets = {"US", "EU", "CN", "JP", "KR"}
        missing_markets = key_markets - jurisdictions
        if missing_markets:
            gaps.append({
                "type": "geographic_gap",
                "detail": f"Missing protection in key markets: {', '.join(sorted(missing_markets))}",
                "severity": "medium",
                "recommendation": "Evaluate filing strategy for missing jurisdictions based on commercial plans",
            })

        return gaps

    def _strategic_recommendations(
        self,
        assets: List[Dict[str, Any]],
        health: Dict[str, Any],
        gaps: List[Dict[str, Any]],
    ) -> List[str]:
        """Generate strategic recommendations."""
        recs: List[str] = []

        if health["overall_score"] < 0.5:
            recs.append("PORTFOLIO HEALTH BELOW AVERAGE: Prioritize strengthening IP coverage.")

        if health["diversity_score"] < 0.5:
            recs.append("Diversify IP assets across multiple protection types (patent, trademark, copyright, trade secret).")

        if health["geographic_coverage"] < 0.3:
            recs.append("Expand geographic coverage to key commercial markets.")

        if health["active_asset_ratio"] < 0.7:
            recs.append("Review and prune inactive/abandoned assets. Consider revival if strategically valuable.")

        critical_gaps = [g for g in gaps if g["severity"] == "critical"]
        if critical_gaps:
            for gap in critical_gaps:
                recs.append(f"CRITICAL GAP: {gap['detail']} - {gap['recommendation']}")

        recs.append("Conduct annual portfolio audit to align IP strategy with business objectives.")
        recs.append("Review competitor portfolios for white space opportunities.")
        recs.append("Implement IP docketing system for deadline management.")

        return recs

    def _assess_monetization(self, assets: List[Dict[str, Any]], categorized: Dict[str, Any]) -> Dict[str, Any]:
        """Assess portfolio monetization potential."""
        licenseable = sum(1 for a in assets if a.get("type") in ("utility_patent", "design_patent"))
        total = len(assets) if assets else 1
        licenseable_ratio = licenseable / total

        strategies: List[str] = []
        if licenseable > 5:
            strategies.append("Patent licensing program: Identify licensees in adjacent markets")
            strategies.append("Patent pool participation: Consider joining relevant technology pools")
        if licenseable > 20:
            strategies.append("Assertion program: Evaluate enforcement against identified infringers")
            strategies.append("Portfolio sale: High-value patents may attract strategic buyers")
        strategies.append("Cross-licensing: Use portfolio as leverage in cross-license negotiations")
        strategies.append("IP-backed financing: Use portfolio as collateral for secured lending")

        return {
            "licenseable_assets": licenseable,
            "licenseable_ratio": round(licenseable_ratio, 4),
            "monetization_strategies": strategies,
            "estimated_annual_licensing_potential": "Requires individual asset valuation",
        }

    def _build_expiration_timeline(self, assets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Build expiration timeline for portfolio assets."""
        timeline: List[Dict[str, Any]] = []
        for asset in assets:
            expiration = asset.get("expiration_date")
            if expiration:
                timeline.append({
                    "asset_id": asset.get("id", "unknown"),
                    "asset_type": asset.get("type", "unknown"),
                    "title": asset.get("title", "Untitled")[:100],
                    "expiration_date": expiration,
                })
        timeline.sort(key=lambda x: x["expiration_date"])
        return timeline[:20]

    @staticmethod
    def _grade(score: float) -> str:
        """Convert score to letter grade."""
        if score >= 0.9:
            return "A+"
        if score >= 0.8:
            return "A"
        if score >= 0.7:
            return "B"
        if score >= 0.6:
            return "C"
        if score >= 0.5:
            return "D"
        return "F"


# ############################################################################
#
# SECTION 15: OPEN SOURCE IP COMPLIANCE CHECKER
#
# ############################################################################

class OpenSourceComplianceChecker:
    """Checks open source license compliance and identifies IP risks.

    Analyzes license obligations, compatibility issues, and
    provides compliance recommendations.
    """

    LICENSE_DATABASE: ClassVar[Dict[str, Dict[str, Any]]] = {
        "MIT": {
            "spdx": "MIT",
            "type": "permissive",
            "copyleft": False,
            "patent_grant": False,
            "attribution_required": True,
            "source_disclosure": False,
            "compatible_with": ["MIT", "BSD-2-Clause", "BSD-3-Clause", "Apache-2.0", "ISC", "Unlicense"],
            "incompatible_with": [],
            "obligations": [
                "Include copyright notice and license text in distributions",
                "No warranty - provided 'as is'",
            ],
            "commercial_use": True,
            "modification_allowed": True,
            "distribution_allowed": True,
            "patent_risk": "low",
        },
        "Apache-2.0": {
            "spdx": "Apache-2.0",
            "type": "permissive",
            "copyleft": False,
            "patent_grant": True,
            "attribution_required": True,
            "source_disclosure": False,
            "compatible_with": ["MIT", "BSD-2-Clause", "BSD-3-Clause", "ISC", "Unlicense"],
            "incompatible_with": ["GPL-2.0-only"],
            "obligations": [
                "Include copyright notice and license text",
                "State changes made to the code",
                "Include NOTICE file if provided",
                "Patent grant terminates if patent litigation initiated",
            ],
            "commercial_use": True,
            "modification_allowed": True,
            "distribution_allowed": True,
            "patent_risk": "low",
        },
        "GPL-2.0": {
            "spdx": "GPL-2.0-only",
            "type": "copyleft",
            "copyleft": True,
            "patent_grant": False,
            "attribution_required": True,
            "source_disclosure": True,
            "compatible_with": ["GPL-2.0-only", "LGPL-2.1-only"],
            "incompatible_with": ["Apache-2.0", "GPL-3.0-only", "CDDL-1.0"],
            "obligations": [
                "Distribute source code of derivative works under GPL-2.0",
                "Include copyright notice and GPL text",
                "No additional restrictions beyond GPL terms",
                "Provide Installation Information for User Products",
            ],
            "commercial_use": True,
            "modification_allowed": True,
            "distribution_allowed": True,
            "patent_risk": "medium",
        },
        "GPL-3.0": {
            "spdx": "GPL-3.0-only",
            "type": "copyleft",
            "copyleft": True,
            "patent_grant": True,
            "attribution_required": True,
            "source_disclosure": True,
            "compatible_with": ["GPL-3.0-only", "LGPL-3.0-only", "AGPL-3.0-only"],
            "incompatible_with": ["GPL-2.0-only", "CDDL-1.0"],
            "obligations": [
                "Distribute source code of derivative works under GPL-3.0",
                "Include copyright notice and GPL text",
                "Provide Installation Information for User Products",
                "No tivoization (anti-DRM provisions)",
                "Explicit patent grant - terminates on patent litigation",
            ],
            "commercial_use": True,
            "modification_allowed": True,
            "distribution_allowed": True,
            "patent_risk": "low",
        },
        "AGPL-3.0": {
            "spdx": "AGPL-3.0-only",
            "type": "copyleft",
            "copyleft": True,
            "patent_grant": True,
            "attribution_required": True,
            "source_disclosure": True,
            "compatible_with": ["AGPL-3.0-only", "GPL-3.0-only"],
            "incompatible_with": ["GPL-2.0-only", "Apache-2.0", "MIT"],
            "obligations": [
                "All GPL-3.0 obligations apply",
                "Network interaction triggers source disclosure (SaaS/cloud)",
                "Users interacting over a network must be offered source",
            ],
            "commercial_use": True,
            "modification_allowed": True,
            "distribution_allowed": True,
            "patent_risk": "low",
        },
        "LGPL-2.1": {
            "spdx": "LGPL-2.1-only",
            "type": "weak_copyleft",
            "copyleft": True,
            "patent_grant": False,
            "attribution_required": True,
            "source_disclosure": True,
            "compatible_with": ["LGPL-2.1-only", "GPL-2.0-only"],
            "incompatible_with": [],
            "obligations": [
                "Modifications to LGPL library must be disclosed",
                "Applications linking to library are NOT derivative works",
                "Dynamic linking preserves proprietary status of application",
                "Static linking requires providing object files for relinking",
            ],
            "commercial_use": True,
            "modification_allowed": True,
            "distribution_allowed": True,
            "patent_risk": "medium",
        },
        "BSD-2-Clause": {
            "spdx": "BSD-2-Clause",
            "type": "permissive",
            "copyleft": False,
            "patent_grant": False,
            "attribution_required": True,
            "source_disclosure": False,
            "compatible_with": ["MIT", "BSD-3-Clause", "Apache-2.0", "ISC"],
            "incompatible_with": [],
            "obligations": [
                "Include copyright notice and license text in source and binary distributions",
            ],
            "commercial_use": True,
            "modification_allowed": True,
            "distribution_allowed": True,
            "patent_risk": "medium",
        },
        "BSD-3-Clause": {
            "spdx": "BSD-3-Clause",
            "type": "permissive",
            "copyleft": False,
            "patent_grant": False,
            "attribution_required": True,
            "source_disclosure": False,
            "compatible_with": ["MIT", "BSD-2-Clause", "Apache-2.0", "ISC"],
            "incompatible_with": [],
            "obligations": [
                "Include copyright notice and license text",
                "Do not use contributor names for endorsement without permission",
            ],
            "commercial_use": True,
            "modification_allowed": True,
            "distribution_allowed": True,
            "patent_risk": "medium",
        },
        "MPL-2.0": {
            "spdx": "MPL-2.0",
            "type": "weak_copyleft",
            "copyleft": True,
            "patent_grant": True,
            "attribution_required": True,
            "source_disclosure": True,
            "compatible_with": ["MPL-2.0", "Apache-2.0", "LGPL-2.1-only", "GPL-2.0-only", "GPL-3.0-only"],
            "incompatible_with": [],
            "obligations": [
                "Modified MPL files must be disclosed under MPL-2.0",
                "Separate proprietary files can be kept proprietary",
                "File-level copyleft (not project-level)",
                "Patent grant included - terminates on litigation",
            ],
            "commercial_use": True,
            "modification_allowed": True,
            "distribution_allowed": True,
            "patent_risk": "low",
        },
        "Unlicense": {
            "spdx": "Unlicense",
            "type": "public_domain",
            "copyleft": False,
            "patent_grant": False,
            "attribution_required": False,
            "source_disclosure": False,
            "compatible_with": ["MIT", "BSD-2-Clause", "BSD-3-Clause", "Apache-2.0", "ISC"],
            "incompatible_with": [],
            "obligations": [
                "No obligations - public domain dedication",
            ],
            "commercial_use": True,
            "modification_allowed": True,
            "distribution_allowed": True,
            "patent_risk": "high",
        },
    }

    def check_compliance(self, project_licenses: List[str], target_license: Optional[str] = None) -> Dict[str, Any]:
        """Check compliance of a project using multiple open source licenses."""
        results: Dict[str, Any] = {
            "total_licenses": len(project_licenses),
            "license_details": [],
            "compatibility_issues": [],
            "obligations": [],
            "overall_risk": "low",
            "copyleft_present": False,
            "patent_risks": [],
            "recommendations": [],
        }

        all_obligations: Set[str] = set()
        has_copyleft = False
        has_strong_copyleft = False
        risk_score = 0

        for lic_name in project_licenses:
            lic_info = self.LICENSE_DATABASE.get(lic_name)
            if not lic_info:
                results["license_details"].append({
                    "license": lic_name,
                    "status": "unknown",
                    "warning": f"License '{lic_name}' not in database - manual review required",
                })
                risk_score += 3
                continue

            results["license_details"].append({
                "license": lic_name,
                "spdx": lic_info["spdx"],
                "type": lic_info["type"],
                "copyleft": lic_info["copyleft"],
                "patent_grant": lic_info["patent_grant"],
                "commercial_use": lic_info["commercial_use"],
                "status": "known",
            })

            for obligation in lic_info["obligations"]:
                all_obligations.add(f"[{lic_name}] {obligation}")

            if lic_info["copyleft"]:
                has_copyleft = True
                if lic_info["type"] == "copyleft":
                    has_strong_copyleft = True
                    risk_score += 2

            if lic_info["patent_risk"] == "high":
                risk_score += 2
                results["patent_risks"].append(f"{lic_name}: No patent grant - patent infringement risk exists")
            elif lic_info["patent_risk"] == "medium":
                risk_score += 1
                results["patent_risks"].append(f"{lic_name}: No explicit patent grant - implied license may apply")

        # Check compatibility between licenses
        for i, lic_a in enumerate(project_licenses):
            for lic_b in project_licenses[i + 1:]:
                info_a = self.LICENSE_DATABASE.get(lic_a, {})
                info_b = self.LICENSE_DATABASE.get(lic_b, {})
                incompatible_a = info_a.get("incompatible_with", [])
                incompatible_b = info_b.get("incompatible_with", [])

                spdx_a = info_a.get("spdx", lic_a)
                spdx_b = info_b.get("spdx", lic_b)

                if spdx_b in incompatible_a or spdx_a in incompatible_b:
                    results["compatibility_issues"].append({
                        "license_a": lic_a,
                        "license_b": lic_b,
                        "issue": f"{lic_a} and {lic_b} are incompatible - cannot combine in same work",
                        "severity": "critical",
                    })
                    risk_score += 5

        # Check target license compatibility
        if target_license and target_license in self.LICENSE_DATABASE:
            target_info = self.LICENSE_DATABASE[target_license]
            for lic in project_licenses:
                lic_info = self.LICENSE_DATABASE.get(lic, {})
                spdx = lic_info.get("spdx", lic)
                if spdx in target_info.get("incompatible_with", []):
                    results["compatibility_issues"].append({
                        "license_a": lic,
                        "license_b": target_license,
                        "issue": f"Dependency {lic} is incompatible with target license {target_license}",
                        "severity": "critical",
                    })
                    risk_score += 5

        results["obligations"] = sorted(all_obligations)
        results["copyleft_present"] = has_copyleft

        # Overall risk
        if risk_score >= 8:
            results["overall_risk"] = "critical"
        elif risk_score >= 5:
            results["overall_risk"] = "high"
        elif risk_score >= 2:
            results["overall_risk"] = "medium"
        else:
            results["overall_risk"] = "low"

        # Recommendations
        if has_strong_copyleft:
            results["recommendations"].append("Strong copyleft detected: Derivative works must be open-sourced under same license.")
            results["recommendations"].append("Consider replacing copyleft dependencies with permissive alternatives if proprietary distribution is required.")
        if results["compatibility_issues"]:
            results["recommendations"].append("CRITICAL: License incompatibilities detected. Resolve before distribution.")
        if results["patent_risks"]:
            results["recommendations"].append("Patent risk detected in some licenses. Consider obtaining explicit patent licenses where needed.")
        results["recommendations"].append("Maintain a Software Bill of Materials (SBOM) tracking all OSS components and licenses.")
        results["recommendations"].append("Implement automated license scanning in CI/CD pipeline.")

        return results


# ############################################################################
#
# SECTION 16: ADDITIONAL API ENDPOINTS
#
# ############################################################################

# ============================================================================
# PROSECUTION ADVISOR ENDPOINTS
# ============================================================================

_prosecution_advisor = PatentProsecutionAdvisor()
_portfolio_analyzer = IPPortfolioAnalyzer()
_oss_checker = OpenSourceComplianceChecker()


class ProsecutionCostRequest(BaseModel):
    """Request for prosecution cost estimate."""
    application_type: Literal["utility", "design", "provisional", "plant"] = "utility"
    entity_size: Literal["large", "small", "micro"] = "large"
    expected_office_actions: int = Field(default=2, ge=0, le=10)
    international: bool = False
    countries: int = Field(default=0, ge=0, le=50)


class PortfolioAnalysisRequest(BaseModel):
    """Request for portfolio analysis."""
    assets: List[Dict[str, Any]] = Field(..., min_length=1, description="List of IP assets")


class OSSComplianceRequest(BaseModel):
    """Request for open source compliance check."""
    licenses: List[str] = Field(..., min_length=1, description="List of license identifiers")
    target_license: Optional[str] = Field(default=None, description="Target output license")


@app.get("/prosecution/office-action/{action_type}")
async def get_oa_strategy(action_type: str) -> Dict[str, Any]:
    """Get strategy for responding to an office action."""
    return _prosecution_advisor.get_office_action_strategy(action_type)


@app.get("/prosecution/rejection/{rejection_type}")
async def get_rejection_strategy(rejection_type: str) -> Dict[str, Any]:
    """Get response strategies for a specific rejection type."""
    return _prosecution_advisor.get_rejection_response(rejection_type)


@app.get("/prosecution/maintenance-fees")
async def get_maintenance_fees(
    entity_size: Literal["large", "small", "micro"] = Query(default="large"),
) -> Dict[str, Any]:
    """Get patent maintenance fee schedule."""
    return {
        "engine_id": ENGINE_ID,
        "entity_size": entity_size,
        "schedule": _prosecution_advisor.get_maintenance_schedule(entity_size),
    }


@app.post("/prosecution/cost-estimate")
async def estimate_cost(request: ProsecutionCostRequest) -> Dict[str, Any]:
    """Estimate total patent prosecution cost."""
    estimate = _prosecution_advisor.estimate_prosecution_cost(
        application_type=request.application_type,
        entity_size=request.entity_size,
        expected_oas=request.expected_office_actions,
        international=request.international,
        countries=request.countries,
    )
    content_hash = hashlib.sha256(json.dumps(estimate, sort_keys=True).encode("utf-8")).hexdigest()
    return {
        "engine_id": ENGINE_ID,
        "estimate": estimate,
        "determinism_hash": content_hash,
    }


# ============================================================================
# PORTFOLIO ANALYSIS ENDPOINTS
# ============================================================================

@app.post("/portfolio/analyze")
async def analyze_portfolio(request: PortfolioAnalysisRequest) -> Dict[str, Any]:
    """Analyze an IP portfolio."""
    result = _portfolio_analyzer.analyze_portfolio(request.assets)
    content_hash = hashlib.sha256(json.dumps(result, sort_keys=True, default=str).encode("utf-8")).hexdigest()
    return {
        "engine_id": ENGINE_ID,
        "analysis": result,
        "determinism_hash": content_hash,
    }


# ============================================================================
# OPEN SOURCE COMPLIANCE ENDPOINTS
# ============================================================================

@app.post("/oss/compliance-check")
async def check_oss_compliance(request: OSSComplianceRequest) -> Dict[str, Any]:
    """Check open source license compliance."""
    result = _oss_checker.check_compliance(request.licenses, request.target_license)
    content_hash = hashlib.sha256(json.dumps(result, sort_keys=True).encode("utf-8")).hexdigest()
    return {
        "engine_id": ENGINE_ID,
        "compliance": result,
        "determinism_hash": content_hash,
    }


@app.get("/oss/licenses")
async def list_oss_licenses() -> Dict[str, Any]:
    """List all known open source licenses."""
    return {
        "engine_id": ENGINE_ID,
        "total_licenses": len(OpenSourceComplianceChecker.LICENSE_DATABASE),
        "licenses": {
            name: {
                "spdx": info["spdx"],
                "type": info["type"],
                "copyleft": info["copyleft"],
                "patent_grant": info["patent_grant"],
                "commercial_use": info["commercial_use"],
            }
            for name, info in OpenSourceComplianceChecker.LICENSE_DATABASE.items()
        },
    }


# ============================================================================
# IP STATUTE REFERENCE ENDPOINTS
# ============================================================================

IP_STATUTE_QUICK_REF: Dict[str, Dict[str, Any]] = {
    "35_usc_101": {
        "title": "Inventions Patentable",
        "text": "Whoever invents or discovers any new and useful process, machine, manufacture, or composition of matter, or any new and useful improvement thereof, may obtain a patent therefor, subject to the conditions and requirements of this title.",
        "key_cases": ["Alice v. CLS Bank", "Mayo v. Prometheus", "Bilski v. Kappos"],
        "category": "patent",
    },
    "35_usc_102": {
        "title": "Conditions for Patentability; Novelty",
        "text": "A person shall be entitled to a patent unless the claimed invention was patented, described in a printed publication, or in public use, on sale, or otherwise available to the public before the effective filing date of the claimed invention.",
        "key_cases": ["Helsinn v. Teva", "In re Schreiber"],
        "category": "patent",
    },
    "35_usc_103": {
        "title": "Conditions for Patentability; Non-obvious Subject Matter",
        "text": "A patent for a claimed invention may not be obtained if the differences between the claimed invention and the prior art are such that the claimed invention as a whole would have been obvious before the effective filing date.",
        "key_cases": ["Graham v. John Deere", "KSR v. Teleflex"],
        "category": "patent",
    },
    "35_usc_112": {
        "title": "Specification",
        "text": "The specification shall contain a written description of the invention, and of the manner and process of making and using it, in such full, clear, concise, and exact terms as to enable any person skilled in the art to make and use the same.",
        "key_cases": ["Nautilus v. Biosig", "Ariad v. Eli Lilly", "In re Wands"],
        "category": "patent",
    },
    "35_usc_271": {
        "title": "Infringement of Patent",
        "text": "Whoever without authority makes, uses, offers to sell, or sells any patented invention, within the United States or imports into the United States any patented invention during the term of the patent therefor, infringes the patent.",
        "key_cases": ["Halo v. Pulse", "Global-Tech v. SEB", "Akamai v. Limelight"],
        "category": "patent",
    },
    "15_usc_1051": {
        "title": "Lanham Act - Registration of Trademarks",
        "text": "The owner of a trademark used in commerce may request registration on the principal register by filing an application with the PTO.",
        "key_cases": ["Matal v. Tam", "Iancu v. Brunetti"],
        "category": "trademark",
    },
    "15_usc_1125": {
        "title": "Lanham Act - False Designations of Origin; Dilution",
        "text": "Section 43(a) provides a federal cause of action for unfair competition, false advertising, and trade dress infringement. Section 43(c) addresses dilution of famous marks.",
        "key_cases": ["Two Pesos v. Taco Cabana", "Moseley v. V Secret"],
        "category": "trademark",
    },
    "17_usc_102": {
        "title": "Copyright - Subject Matter",
        "text": "Copyright protection subsists in original works of authorship fixed in any tangible medium of expression from which they can be perceived, reproduced, or otherwise communicated.",
        "key_cases": ["Feist v. Rural Telephone", "Baker v. Selden"],
        "category": "copyright",
    },
    "17_usc_107": {
        "title": "Copyright - Fair Use",
        "text": "The fair use of a copyrighted work for purposes such as criticism, comment, news reporting, teaching, scholarship, or research is not an infringement of copyright.",
        "key_cases": ["Campbell v. Acuff-Rose", "Andy Warhol v. Goldsmith", "Google v. Oracle"],
        "category": "copyright",
    },
    "18_usc_1836": {
        "title": "Defend Trade Secrets Act - Civil Proceedings",
        "text": "An owner of a trade secret that is misappropriated may bring a civil action if the trade secret is related to a product or service used in, or intended for use in, interstate or foreign commerce.",
        "key_cases": ["Waymo v. Uber"],
        "category": "trade_secret",
    },
}


@app.get("/statutes")
async def list_statutes() -> Dict[str, Any]:
    """List all IP statute quick references."""
    return {
        "engine_id": ENGINE_ID,
        "total_statutes": len(IP_STATUTE_QUICK_REF),
        "statutes": {
            k: {"title": v["title"], "category": v["category"]}
            for k, v in IP_STATUTE_QUICK_REF.items()
        },
    }


@app.get("/statutes/{statute_id}")
async def get_statute(statute_id: str) -> Dict[str, Any]:
    """Get a specific IP statute quick reference."""
    ref = IP_STATUTE_QUICK_REF.get(statute_id)
    if not ref:
        raise HTTPException(status_code=404, detail=f"Statute '{statute_id}' not found")
    return {
        "engine_id": ENGINE_ID,
        "statute_id": statute_id,
        **ref,
    }


# ############################################################################
#
# SECTION 17: IP TIMELINE AND DEADLINE TRACKER
#
# ############################################################################

class IPDeadlineTracker:
    """Tracks IP prosecution deadlines, maintenance fees, and renewal dates.

    Provides comprehensive timeline management for patent, trademark,
    and copyright portfolios with alerting thresholds.
    """

    PATENT_DEADLINES: ClassVar[Dict[str, Dict[str, Any]]] = {
        "provisional_to_non_provisional": {
            "label": "File Non-Provisional from Provisional",
            "months_from_event": 12,
            "event": "provisional_filing",
            "extendable": False,
            "penalty": "Loss of provisional filing date",
            "critical": True,
        },
        "paris_convention_priority": {
            "label": "Paris Convention Priority Deadline",
            "months_from_event": 12,
            "event": "first_filing",
            "extendable": False,
            "penalty": "Loss of priority date for foreign filings",
            "critical": True,
        },
        "pct_filing": {
            "label": "PCT International Filing Deadline",
            "months_from_event": 12,
            "event": "priority_date",
            "extendable": False,
            "penalty": "Cannot file PCT application",
            "critical": True,
        },
        "pct_national_phase": {
            "label": "PCT National Phase Entry",
            "months_from_event": 30,
            "event": "priority_date",
            "extendable": False,
            "penalty": "Loss of rights in non-entered countries",
            "critical": True,
        },
        "office_action_response": {
            "label": "Office Action Response",
            "months_from_event": 3,
            "event": "office_action_mailing",
            "extendable": True,
            "max_extension_months": 3,
            "penalty": "Application abandoned",
            "critical": True,
        },
        "issue_fee_payment": {
            "label": "Issue Fee Payment",
            "months_from_event": 3,
            "event": "notice_of_allowance",
            "extendable": False,
            "penalty": "Application abandoned",
            "critical": True,
        },
        "maintenance_3_5": {
            "label": "3.5 Year Maintenance Fee",
            "months_from_event": 42,
            "event": "grant_date",
            "extendable": True,
            "max_extension_months": 6,
            "penalty": "Patent expires",
            "critical": True,
        },
        "maintenance_7_5": {
            "label": "7.5 Year Maintenance Fee",
            "months_from_event": 90,
            "event": "grant_date",
            "extendable": True,
            "max_extension_months": 6,
            "penalty": "Patent expires",
            "critical": True,
        },
        "maintenance_11_5": {
            "label": "11.5 Year Maintenance Fee",
            "months_from_event": 138,
            "event": "grant_date",
            "extendable": True,
            "max_extension_months": 6,
            "penalty": "Patent expires",
            "critical": True,
        },
        "ipr_petition_deadline": {
            "label": "IPR Petition Deadline (1 year from service)",
            "months_from_event": 12,
            "event": "infringement_complaint_service",
            "extendable": False,
            "penalty": "Time-barred from filing IPR",
            "critical": True,
        },
    }

    TRADEMARK_DEADLINES: ClassVar[Dict[str, Dict[str, Any]]] = {
        "response_to_office_action": {
            "label": "Trademark Office Action Response",
            "months_from_event": 3,
            "event": "office_action_issuance",
            "extendable": True,
            "max_extension_months": 3,
            "penalty": "Application abandoned",
            "critical": True,
        },
        "statement_of_use": {
            "label": "Statement of Use Filing",
            "months_from_event": 6,
            "event": "notice_of_allowance",
            "extendable": True,
            "max_extension_months": 30,
            "penalty": "Application abandoned",
            "critical": True,
        },
        "section_8_declaration": {
            "label": "Section 8 Declaration of Continued Use",
            "months_from_event": 72,
            "event": "registration_date",
            "extendable": True,
            "max_extension_months": 6,
            "penalty": "Registration cancelled",
            "critical": True,
        },
        "section_9_renewal": {
            "label": "Section 9 Renewal",
            "months_from_event": 120,
            "event": "registration_date",
            "extendable": True,
            "max_extension_months": 6,
            "penalty": "Registration expires",
            "critical": True,
        },
        "section_15_incontestability": {
            "label": "Section 15 Declaration of Incontestability",
            "months_from_event": 60,
            "event": "registration_date",
            "extendable": False,
            "penalty": "Lose ability to claim incontestable status (optional deadline)",
            "critical": False,
        },
        "madrid_renewal": {
            "label": "Madrid Protocol International Renewal",
            "months_from_event": 120,
            "event": "international_registration_date",
            "extendable": True,
            "max_extension_months": 6,
            "penalty": "International registration lapses",
            "critical": True,
        },
    }

    COPYRIGHT_DEADLINES: ClassVar[Dict[str, Dict[str, Any]]] = {
        "registration_for_statutory_damages": {
            "label": "Registration Before Infringement (or within 3 months of publication)",
            "months_from_event": 3,
            "event": "first_publication",
            "extendable": False,
            "penalty": "Lose right to statutory damages and attorney fees",
            "critical": True,
        },
        "dmca_counter_notice_window": {
            "label": "DMCA Counter-Notice Restoration",
            "months_from_event": 0,
            "event": "counter_notice_filed",
            "extendable": False,
            "penalty": "Material restored if no lawsuit filed within 10-14 business days",
            "critical": False,
        },
    }

    def get_all_deadlines(self) -> Dict[str, Any]:
        """Get all tracked deadline types."""
        return {
            "patent": self.PATENT_DEADLINES,
            "trademark": self.TRADEMARK_DEADLINES,
            "copyright": self.COPYRIGHT_DEADLINES,
            "total_deadline_types": (
                len(self.PATENT_DEADLINES) +
                len(self.TRADEMARK_DEADLINES) +
                len(self.COPYRIGHT_DEADLINES)
            ),
        }

    def compute_deadline(self, deadline_type: str, event_date: str, ip_type: str = "patent") -> Dict[str, Any]:
        """Compute a specific deadline from an event date."""
        deadline_db = {
            "patent": self.PATENT_DEADLINES,
            "trademark": self.TRADEMARK_DEADLINES,
            "copyright": self.COPYRIGHT_DEADLINES,
        }
        db = deadline_db.get(ip_type, {})
        deadline_info = db.get(deadline_type)
        if not deadline_info:
            return {"error": f"Unknown deadline type: {deadline_type} for ip_type: {ip_type}"}

        try:
            event_dt = datetime.fromisoformat(event_date)
            if event_dt.tzinfo is None:
                event_dt = event_dt.replace(tzinfo=timezone.utc)
            months = deadline_info["months_from_event"]
            # Approximate month calculation
            deadline_dt = event_dt.replace(
                year=event_dt.year + (event_dt.month + months - 1) // 12,
                month=(event_dt.month + months - 1) % 12 + 1,
            )
            days_remaining = (deadline_dt - datetime.now(timezone.utc)).days
            urgency = "critical" if days_remaining < 30 else (
                "urgent" if days_remaining < 90 else (
                    "upcoming" if days_remaining < 180 else "scheduled"
                )
            )
        except (ValueError, TypeError) as exc:
            return {"error": f"Invalid date format: {exc}"}

        return {
            "deadline_type": deadline_type,
            "label": deadline_info["label"],
            "event_date": event_date,
            "deadline_date": deadline_dt.isoformat(),
            "days_remaining": days_remaining,
            "urgency": urgency,
            "extendable": deadline_info["extendable"],
            "max_extension_months": deadline_info.get("max_extension_months", 0),
            "penalty_for_missing": deadline_info["penalty"],
            "critical": deadline_info["critical"],
        }


# ############################################################################
#
# SECTION 18: IP INFRINGEMENT RISK CALCULATOR
#
# ############################################################################

class InfringementRiskCalculator:
    """Calculates comprehensive infringement risk scores for IP assets.

    Factors in claim strength, prosecution history, prior art landscape,
    and enforcement considerations.
    """

    RISK_FACTORS: ClassVar[Dict[str, Dict[str, Any]]] = {
        "claim_breadth": {
            "label": "Claim Breadth",
            "weight": 0.20,
            "description": "Broader claims = higher risk of reading on accused product",
            "scale": "1-10 where 10 = extremely broad claims",
        },
        "prosecution_history": {
            "label": "Prosecution History Strength",
            "weight": 0.15,
            "description": "Clean prosecution = fewer estoppel arguments available",
            "scale": "1-10 where 10 = no narrowing amendments, clean history",
        },
        "prior_art_vulnerability": {
            "label": "Prior Art Vulnerability",
            "weight": 0.15,
            "description": "Vulnerability of patent to invalidity challenge",
            "scale": "1-10 where 10 = highly vulnerable (close prior art exists)",
        },
        "market_overlap": {
            "label": "Market Overlap",
            "weight": 0.15,
            "description": "Degree of commercial overlap between patented and accused products",
            "scale": "1-10 where 10 = identical market",
        },
        "technology_similarity": {
            "label": "Technology Similarity",
            "weight": 0.20,
            "description": "Technical similarity between patented invention and accused product",
            "scale": "1-10 where 10 = functionally identical",
        },
        "patent_holder_litigiousness": {
            "label": "Patent Holder Litigiousness",
            "weight": 0.10,
            "description": "History and propensity of patent holder to enforce",
            "scale": "1-10 where 10 = very aggressive enforcement (PAE/NPE)",
        },
        "damages_exposure": {
            "label": "Damages Exposure",
            "weight": 0.05,
            "description": "Potential financial exposure if infringement is found",
            "scale": "1-10 where 10 = very high damages (large market, willful)",
        },
    }

    def calculate_risk(self, factor_scores: Dict[str, float]) -> Dict[str, Any]:
        """Calculate composite infringement risk from factor scores."""
        weighted_sum = 0.0
        factor_details: List[Dict[str, Any]] = []
        total_weight = 0.0

        for factor_id, factor_info in self.RISK_FACTORS.items():
            score = factor_scores.get(factor_id, 5.0)
            score = max(1.0, min(10.0, score))
            weight = factor_info["weight"]
            weighted_contribution = (score / 10.0) * weight
            weighted_sum += weighted_contribution
            total_weight += weight

            factor_details.append({
                "factor": factor_id,
                "label": factor_info["label"],
                "score": score,
                "weight": weight,
                "contribution": round(weighted_contribution, 4),
            })

        composite_risk = weighted_sum / total_weight if total_weight > 0 else 0.5

        if composite_risk >= 0.75:
            risk_level = "critical"
            recommendation = "Immediate legal counsel consultation recommended. Consider design-around or licensing."
        elif composite_risk >= 0.55:
            risk_level = "high"
            recommendation = "Detailed FTO opinion recommended. Evaluate design-around options and insurance."
        elif composite_risk >= 0.35:
            risk_level = "medium"
            recommendation = "Monitor situation. Consider obtaining formal FTO opinion for key markets."
        else:
            risk_level = "low"
            recommendation = "Low risk. Standard monitoring sufficient. Document non-infringement position."

        content_hash = hashlib.sha256(
            json.dumps(factor_scores, sort_keys=True).encode("utf-8")
        ).hexdigest()

        return {
            "composite_risk_score": round(composite_risk, 4),
            "risk_level": risk_level,
            "recommendation": recommendation,
            "factor_details": factor_details,
            "determinism_hash": content_hash,
        }

    def get_factor_definitions(self) -> Dict[str, Any]:
        """Get all risk factor definitions."""
        return {
            "factors": {
                k: {"label": v["label"], "weight": v["weight"], "description": v["description"], "scale": v["scale"]}
                for k, v in self.RISK_FACTORS.items()
            },
            "total_factors": len(self.RISK_FACTORS),
        }


# ############################################################################
#
# SECTION 19: IP COMPARISON MATRIX
#
# ############################################################################

class IPComparisonMatrix:
    """Provides comparative analysis across IP protection types.

    Helps users understand which form of IP protection best suits
    their needs based on specific criteria.
    """

    COMPARISON_DATA: ClassVar[Dict[str, Dict[str, Any]]] = {
        "utility_patent": {
            "what_it_protects": "Novel, useful, non-obvious inventions (processes, machines, manufactures, compositions)",
            "duration": "20 years from filing date",
            "cost_range": "$10,000 - $30,000+ (prosecution through grant)",
            "time_to_obtain": "2-4 years average",
            "geographic_scope": "Country-by-country (can use PCT for international)",
            "registration_required": True,
            "protects_against_independent_creation": True,
            "protects_against_reverse_engineering": True,
            "public_disclosure": True,
            "maintenance_required": True,
            "strength": "Strong - exclusive right to make, use, sell",
            "best_for": "Products that can be reverse-engineered, technology with clear 20-year commercial window",
            "limitations": "Time-limited, expensive, requires disclosure, subject to invalidity challenges",
        },
        "design_patent": {
            "what_it_protects": "Ornamental appearance of a functional article",
            "duration": "15 years from grant date",
            "cost_range": "$3,000 - $10,000",
            "time_to_obtain": "1-2 years average",
            "geographic_scope": "Country-by-country (can use Hague for international)",
            "registration_required": True,
            "protects_against_independent_creation": True,
            "protects_against_reverse_engineering": True,
            "public_disclosure": True,
            "maintenance_required": False,
            "strength": "Moderate - only ornamental aspects, not function",
            "best_for": "Product designs, user interfaces, consumer electronics",
            "limitations": "Only protects appearance, not function; ordinary observer test",
        },
        "trademark": {
            "what_it_protects": "Brand identifiers: names, logos, slogans, sounds, colors, trade dress",
            "duration": "Potentially unlimited (renewable every 10 years)",
            "cost_range": "$1,500 - $5,000 per class (US)",
            "time_to_obtain": "8-12 months average",
            "geographic_scope": "Country-by-country (can use Madrid for international)",
            "registration_required": False,
            "protects_against_independent_creation": True,
            "protects_against_reverse_engineering": "N/A",
            "public_disclosure": True,
            "maintenance_required": True,
            "strength": "Strong for distinctive marks in registered classes",
            "best_for": "Brand names, logos, product packaging, marketing slogans",
            "limitations": "Must use in commerce, must maintain, risk of genericide",
        },
        "copyright": {
            "what_it_protects": "Original works of authorship fixed in tangible medium",
            "duration": "Life + 70 years (individual) or 95 years from publication (work for hire)",
            "cost_range": "$35 - $65 (registration fee only)",
            "time_to_obtain": "3-6 months for registration (protection is automatic upon creation)",
            "geographic_scope": "Automatic in Berne Convention countries (181 members)",
            "registration_required": False,
            "protects_against_independent_creation": False,
            "protects_against_reverse_engineering": "N/A",
            "public_disclosure": False,
            "maintenance_required": False,
            "strength": "Strong for creative expression; does not protect ideas or facts",
            "best_for": "Software code, written works, artistic works, music, film, architecture",
            "limitations": "Does not protect ideas, only expression; fair use defense available",
        },
        "trade_secret": {
            "what_it_protects": "Valuable confidential business information",
            "duration": "Potentially unlimited (as long as secrecy maintained)",
            "cost_range": "$0 for protection + ongoing security costs",
            "time_to_obtain": "Immediate (no registration)",
            "geographic_scope": "Wherever secrecy is maintained; DTSA for federal claims",
            "registration_required": False,
            "protects_against_independent_creation": False,
            "protects_against_reverse_engineering": False,
            "public_disclosure": False,
            "maintenance_required": True,
            "strength": "Moderate - only against misappropriation",
            "best_for": "Formulas, processes not visible in product, customer lists, pricing",
            "limitations": "No protection against independent discovery or reverse engineering; lost if disclosed",
        },
    }

    def get_full_comparison(self) -> Dict[str, Any]:
        """Get the full comparison matrix."""
        return {
            "ip_types": self.COMPARISON_DATA,
            "total_types": len(self.COMPARISON_DATA),
            "comparison_criteria": [
                "what_it_protects", "duration", "cost_range", "time_to_obtain",
                "geographic_scope", "registration_required", "protects_against_independent_creation",
                "protects_against_reverse_engineering", "public_disclosure", "maintenance_required",
                "strength", "best_for", "limitations",
            ],
        }

    def compare_two(self, type_a: str, type_b: str) -> Dict[str, Any]:
        """Compare two IP protection types side by side."""
        data_a = self.COMPARISON_DATA.get(type_a)
        data_b = self.COMPARISON_DATA.get(type_b)
        if not data_a or not data_b:
            return {"error": f"Unknown IP type(s): {type_a}, {type_b}"}

        comparison: List[Dict[str, Any]] = []
        for key in data_a:
            comparison.append({
                "criterion": key.replace("_", " ").title(),
                type_a: data_a[key],
                type_b: data_b[key],
            })

        return {
            "type_a": type_a,
            "type_b": type_b,
            "comparison": comparison,
        }

    def recommend(self, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Recommend IP protection types based on criteria."""
        recommendations: List[Dict[str, Any]] = []

        needs_reverse_eng_protection = criteria.get("reverse_engineerable", False)
        needs_independent_creation_protection = criteria.get("independent_creation_risk", False)
        needs_long_duration = criteria.get("long_duration", False)
        is_visible_in_product = criteria.get("visible_in_product", True)
        budget_constraint = criteria.get("budget_limited", False)
        needs_international = criteria.get("international", False)
        is_creative_work = criteria.get("creative_work", False)
        is_brand = criteria.get("brand", False)

        if is_brand:
            recommendations.append({
                "type": "trademark",
                "priority": "primary",
                "rationale": "Brand identifiers should be protected with trademark registration",
            })

        if is_creative_work:
            recommendations.append({
                "type": "copyright",
                "priority": "primary",
                "rationale": "Creative works receive automatic copyright protection; registration recommended for statutory damages",
            })

        if needs_reverse_eng_protection and is_visible_in_product:
            recommendations.append({
                "type": "utility_patent",
                "priority": "primary",
                "rationale": "Patent protection is the only IP right that protects against reverse engineering and independent creation",
            })

        if not is_visible_in_product and needs_long_duration:
            recommendations.append({
                "type": "trade_secret",
                "priority": "primary",
                "rationale": "Process or formula not visible in product benefits from unlimited trade secret duration",
            })

        if is_visible_in_product and not needs_reverse_eng_protection:
            recommendations.append({
                "type": "design_patent",
                "priority": "secondary",
                "rationale": "Product appearance can be protected with design patents at lower cost than utility patents",
            })

        if not recommendations:
            recommendations.append({
                "type": "utility_patent",
                "priority": "primary",
                "rationale": "When in doubt, utility patent provides the broadest protection for novel inventions",
            })
            recommendations.append({
                "type": "trade_secret",
                "priority": "secondary",
                "rationale": "Complement patent with trade secret protection for non-patented aspects",
            })

        return recommendations


# ============================================================================
# ADDITIONAL ENDPOINTS FOR NEW MODULES
# ============================================================================

_deadline_tracker = IPDeadlineTracker()
_risk_calculator = InfringementRiskCalculator()
_comparison_matrix = IPComparisonMatrix()


class RiskCalculationRequest(BaseModel):
    """Request for infringement risk calculation."""
    factor_scores: Dict[str, float] = Field(
        ...,
        description="Risk factor scores (1-10 scale)",
        json_schema_extra={
            "example": {
                "claim_breadth": 7,
                "prosecution_history": 6,
                "prior_art_vulnerability": 4,
                "market_overlap": 8,
                "technology_similarity": 7,
                "patent_holder_litigiousness": 5,
                "damages_exposure": 6,
            }
        },
    )


class DeadlineComputeRequest(BaseModel):
    """Request to compute a specific deadline."""
    deadline_type: str = Field(..., description="Type of deadline")
    event_date: str = Field(..., description="Date of triggering event (ISO format)")
    ip_type: Literal["patent", "trademark", "copyright"] = Field(default="patent")


class IPRecommendationRequest(BaseModel):
    """Request for IP protection recommendation."""
    reverse_engineerable: bool = Field(default=False)
    independent_creation_risk: bool = Field(default=False)
    long_duration: bool = Field(default=False)
    visible_in_product: bool = Field(default=True)
    budget_limited: bool = Field(default=False)
    international: bool = Field(default=False)
    creative_work: bool = Field(default=False)
    brand: bool = Field(default=False)


@app.get("/deadlines")
async def list_deadlines() -> Dict[str, Any]:
    """List all tracked IP deadline types."""
    return {
        "engine_id": ENGINE_ID,
        "deadlines": _deadline_tracker.get_all_deadlines(),
    }


@app.post("/deadlines/compute")
async def compute_deadline(request: DeadlineComputeRequest) -> Dict[str, Any]:
    """Compute a specific deadline from an event date."""
    result = _deadline_tracker.compute_deadline(
        request.deadline_type, request.event_date, request.ip_type,
    )
    return {
        "engine_id": ENGINE_ID,
        "result": result,
    }


@app.post("/risk/calculate")
async def calculate_risk(request: RiskCalculationRequest) -> Dict[str, Any]:
    """Calculate infringement risk from factor scores."""
    result = _risk_calculator.calculate_risk(request.factor_scores)
    return {
        "engine_id": ENGINE_ID,
        **result,
    }


@app.get("/risk/factors")
async def list_risk_factors() -> Dict[str, Any]:
    """List all infringement risk factor definitions."""
    return {
        "engine_id": ENGINE_ID,
        **_risk_calculator.get_factor_definitions(),
    }


@app.get("/comparison")
async def get_ip_comparison() -> Dict[str, Any]:
    """Get the full IP protection type comparison matrix."""
    return {
        "engine_id": ENGINE_ID,
        **_comparison_matrix.get_full_comparison(),
    }


@app.get("/comparison/{type_a}/{type_b}")
async def compare_ip_types(type_a: str, type_b: str) -> Dict[str, Any]:
    """Compare two IP protection types side by side."""
    result = _comparison_matrix.compare_two(type_a, type_b)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return {
        "engine_id": ENGINE_ID,
        **result,
    }


@app.post("/recommend")
async def recommend_ip_protection(request: IPRecommendationRequest) -> Dict[str, Any]:
    """Recommend IP protection types based on criteria."""
    criteria = request.model_dump()
    recommendations = _comparison_matrix.recommend(criteria)
    content_hash = hashlib.sha256(
        json.dumps(recommendations, sort_keys=True).encode("utf-8")
    ).hexdigest()
    return {
        "engine_id": ENGINE_ID,
        "criteria": criteria,
        "recommendations": recommendations,
        "determinism_hash": content_hash,
    }


# ============================================================================
# ENGINE INFO AND VERSION ENDPOINTS
# ============================================================================

@app.get("/version")
async def get_version() -> Dict[str, Any]:
    """Get complete engine version and capability information."""
    return {
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "engine_version": ENGINE_VERSION,
        "port": ENGINE_PORT,
        "tier": ENGINE_TIER,
        "mode": ENGINE_MODE,
        "authority_level": AUTHORITY_LEVEL,
        "authority_gate": AUTHORITY_GATE,
        "tie_components": [
            "three_layer_response",
            "response_modes",
            "doctrine_cache",
            "authority_hardening",
            "confidence_stratification",
            "semantic_normalization",
            "vector_search_tfidf",
            "telemetry_module",
            "doctrine_drift_watcher",
            "doctrine_coverage_map",
            "metrics_collector",
            "health_endpoint",
            "zoned_analysis",
            "fact_fragility_scoring",
            "audit_trail_jsonl",
            "determinism_hash_sha256",
            "fastapi_server",
            "loguru_logging",
            "multi_doctrine_decomposition",
            "deep_analysis_mode",
        ],
        "ip_domains": [
            "patent_law_35_usc",
            "trademark_law_lanham_act",
            "copyright_law_17_usc",
            "trade_secrets_dtsa_utsa",
            "design_patents",
            "plant_patents",
            "patent_prosecution",
            "patent_litigation",
            "ptab_proceedings",
            "international_ip_pct_madrid_hague",
            "ip_licensing",
            "ip_valuation",
            "freedom_to_operate",
            "prior_art_search",
            "infringement_analysis",
            "open_source_compliance",
            "ai_generated_ip",
            "standard_essential_patents",
        ],
        "capabilities": {
            "query_modes": ["fast", "analysis", "memo", "fto", "portfolio"],
            "claim_analysis": ["parse", "infringement", "fto"],
            "trademark_clearance": True,
            "prior_art_search": True,
            "prosecution_guidance": True,
            "portfolio_analysis": True,
            "oss_compliance": True,
            "deadline_tracking": True,
            "risk_calculation": True,
            "ip_comparison": True,
            "protection_recommendation": True,
        },
        "doctrine_cache": {
            "total_blocks": get_doctrine_count(),
            "hash": get_doctrine_hash()[:32],
        },
        "semantic_map": {
            "version": get_semantic_map_version(),
            "hash": get_semantic_map_hash()[:32],
        },
        "config_hash": hashlib.sha256(json.dumps(ENGINE_CONFIG, sort_keys=True).encode("utf-8")).hexdigest()[:32],
    }


# ############################################################################
#
# SECTION 20: PATENT TERM CALCULATOR
#
# ############################################################################

class PatentTermCalculator:
    """Calculates patent term including adjustments and extensions.

    Handles PTA (Patent Term Adjustment), PTE (Patent Term Extension),
    terminal disclaimers, and expiration date computation.
    """

    def calculate_term(
        self,
        filing_date: str,
        grant_date: str,
        patent_type: str = "utility",
        pta_days: int = 0,
        pte_days: int = 0,
        terminal_disclaimer: bool = False,
        td_expiration_date: Optional[str] = None,
        priority_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Calculate patent term with all adjustments.

        Args:
            filing_date: Non-provisional filing date (ISO format)
            grant_date: Patent grant date (ISO format)
            patent_type: utility, design, or plant
            pta_days: Patent Term Adjustment days (35 USC 154(b))
            pte_days: Patent Term Extension days (35 USC 156, pharma)
            terminal_disclaimer: Whether a terminal disclaimer was filed
            td_expiration_date: Terminal disclaimer tied-to patent expiration
            priority_date: Earliest priority date (for continuation chains)
        """
        try:
            file_dt = datetime.fromisoformat(filing_date)
            grant_dt = datetime.fromisoformat(grant_date)
            if file_dt.tzinfo is None:
                file_dt = file_dt.replace(tzinfo=timezone.utc)
            if grant_dt.tzinfo is None:
                grant_dt = grant_dt.replace(tzinfo=timezone.utc)
        except (ValueError, TypeError) as exc:
            return {"error": f"Invalid date: {exc}"}

        # Base term calculation
        if patent_type == "utility" or patent_type == "plant":
            base_term_years = 20
            base_expiration = file_dt.replace(year=file_dt.year + base_term_years)
        elif patent_type == "design":
            base_term_years = 15
            base_expiration = grant_dt.replace(year=grant_dt.year + base_term_years)
        else:
            return {"error": f"Unknown patent type: {patent_type}"}

        # Apply PTA
        from datetime import timedelta
        adjusted_expiration = base_expiration + timedelta(days=pta_days)

        # Apply PTE
        extended_expiration = adjusted_expiration + timedelta(days=pte_days)

        # Apply terminal disclaimer
        final_expiration = extended_expiration
        td_limited = False
        if terminal_disclaimer and td_expiration_date:
            try:
                td_dt = datetime.fromisoformat(td_expiration_date)
                if td_dt.tzinfo is None:
                    td_dt = td_dt.replace(tzinfo=timezone.utc)
                if td_dt < final_expiration:
                    final_expiration = td_dt
                    td_limited = True
            except (ValueError, TypeError):
                pass

        # Days remaining
        now = datetime.now(timezone.utc)
        days_remaining = (final_expiration - now).days
        is_expired = days_remaining <= 0

        # Prosecution time
        prosecution_days = (grant_dt - file_dt).days

        return {
            "patent_type": patent_type,
            "filing_date": filing_date,
            "grant_date": grant_date,
            "base_term_years": base_term_years,
            "base_expiration": base_expiration.isoformat(),
            "pta_days": pta_days,
            "pte_days": pte_days,
            "terminal_disclaimer": terminal_disclaimer,
            "td_limited": td_limited,
            "final_expiration": final_expiration.isoformat(),
            "days_remaining": days_remaining,
            "is_expired": is_expired,
            "prosecution_time_days": prosecution_days,
            "total_adjustment_days": pta_days + pte_days,
            "status": "expired" if is_expired else ("expiring_soon" if days_remaining < 365 else "active"),
        }

    def explain_pta(self) -> Dict[str, Any]:
        """Explain Patent Term Adjustment components."""
        return {
            "title": "Patent Term Adjustment (PTA) - 35 USC 154(b)",
            "description": (
                "PTA compensates patentees for USPTO delays during prosecution. "
                "Net PTA = A-delay + B-delay + C-delay - Applicant delay overlap."
            ),
            "components": {
                "a_delay": {
                    "label": "14-Month Guarantee (A Delay)",
                    "description": "Days beyond 14 months for first office action from filing",
                    "statute": "35 USC 154(b)(1)(A)(i)",
                },
                "b_delay": {
                    "label": "4-Month Response Guarantee (B Delay)",
                    "description": "Days beyond 4 months for each subsequent response from USPTO",
                    "statute": "35 USC 154(b)(1)(A)(ii)",
                },
                "c_delay": {
                    "label": "3-Year Guarantee (C Delay)",
                    "description": "Days beyond 3 years from filing to grant (excluding applicant-caused delays, RCEs, appeals, etc.)",
                    "statute": "35 USC 154(b)(1)(B)",
                },
                "applicant_delay": {
                    "label": "Applicant Delay Reduction",
                    "description": "Days of delay attributable to applicant (e.g., responses filed after 3 months)",
                    "statute": "35 USC 154(b)(2)(C)",
                },
                "overlap_reduction": {
                    "label": "Overlap Reduction",
                    "description": "A, B, and C delays cannot be double-counted for overlapping periods",
                    "statute": "35 USC 154(b)(2)(A)",
                },
            },
            "dispute_process": "File request for reconsideration with USPTO within 2 months of grant, or appeal to Federal Circuit within 180 days.",
        }

    def explain_pte(self) -> Dict[str, Any]:
        """Explain Patent Term Extension for pharmaceuticals."""
        return {
            "title": "Patent Term Extension (PTE) - 35 USC 156",
            "description": (
                "PTE compensates for regulatory review time that prevents marketing of "
                "FDA-regulated products (drugs, biologics, medical devices, food/color additives)."
            ),
            "eligibility": [
                "Patent has not expired",
                "Patent has never been extended before",
                "Application filed within 60 days of FDA approval",
                "Only one patent per product may be extended",
                "Patent must claim the approved product or method of use",
            ],
            "calculation": {
                "formula": "PTE = (0.5 * Testing Phase) + Approval Phase - Applicant Delay",
                "maximum": "5 years",
                "remaining_term_cap": "Total remaining term after extension cannot exceed 14 years from FDA approval",
            },
            "common_products": [
                "New chemical entity drugs",
                "Biologic products",
                "New animal drugs",
                "Medical devices requiring premarket approval",
            ],
        }


# ============================================================================
# PATENT TERM ENDPOINTS
# ============================================================================

_term_calculator = PatentTermCalculator()


class PatentTermRequest(BaseModel):
    """Request for patent term calculation."""
    filing_date: str = Field(..., description="Filing date (ISO format)")
    grant_date: str = Field(..., description="Grant date (ISO format)")
    patent_type: Literal["utility", "design", "plant"] = Field(default="utility")
    pta_days: int = Field(default=0, ge=0, description="Patent Term Adjustment days")
    pte_days: int = Field(default=0, ge=0, description="Patent Term Extension days")
    terminal_disclaimer: bool = Field(default=False)
    td_expiration_date: Optional[str] = Field(default=None)
    priority_date: Optional[str] = Field(default=None)


@app.post("/patent-term/calculate")
async def calculate_patent_term(request: PatentTermRequest) -> Dict[str, Any]:
    """Calculate patent term with all adjustments."""
    result = _term_calculator.calculate_term(
        filing_date=request.filing_date,
        grant_date=request.grant_date,
        patent_type=request.patent_type,
        pta_days=request.pta_days,
        pte_days=request.pte_days,
        terminal_disclaimer=request.terminal_disclaimer,
        td_expiration_date=request.td_expiration_date,
        priority_date=request.priority_date,
    )
    content_hash = hashlib.sha256(
        json.dumps(result, sort_keys=True, default=str).encode("utf-8")
    ).hexdigest()
    return {
        "engine_id": ENGINE_ID,
        **result,
        "determinism_hash": content_hash,
    }


@app.get("/patent-term/explain-pta")
async def explain_pta() -> Dict[str, Any]:
    """Explain Patent Term Adjustment components."""
    return {
        "engine_id": ENGINE_ID,
        **_term_calculator.explain_pta(),
    }


@app.get("/patent-term/explain-pte")
async def explain_pte() -> Dict[str, Any]:
    """Explain Patent Term Extension for pharmaceuticals."""
    return {
        "engine_id": ENGINE_ID,
        **_term_calculator.explain_pte(),
    }


# ############################################################################
#
# SECTION 21: IP LITIGATION VENUE ANALYZER
#
# ############################################################################

class IPLitigationVenueAnalyzer:
    """Analyze optimal litigation venues for IP disputes."""

    VENUE_DATA: ClassVar[Dict[str, Dict[str, Any]]] = {
        "wdtx": {
            "name": "Western District of Texas (Waco Division)",
            "judge": "Judge Alan Albright (2018-present, cases reassigned 2022+)",
            "speed": "fast",
            "avg_months_to_trial": 18,
            "patent_case_volume": "very_high",
            "plaintiff_win_rate": 0.52,
            "markman_timing": "early",
            "local_rules": "Patent-specific local rules, mandatory initial disclosures",
            "strengths": ["Fast scheduling", "Early Markman hearings", "Patent expertise"],
            "weaknesses": ["TC Heartland venue challenges", "Case reassignment policy post-2022"],
            "notes": "Was #1 patent venue 2019-2022; SCOTUS TC Heartland limits venue to incorporation state or regular established business",
        },
        "edtx": {
            "name": "Eastern District of Texas (Marshall Division)",
            "judge": "Multiple experienced patent judges",
            "speed": "moderate",
            "avg_months_to_trial": 24,
            "patent_case_volume": "high",
            "plaintiff_win_rate": 0.50,
            "markman_timing": "moderate",
            "local_rules": "Patent-specific local rules since 2005",
            "strengths": ["Experienced jurors", "Established patent rules", "Plaintiff-friendly procedures"],
            "weaknesses": ["TC Heartland venue transfers", "Distance from tech centers"],
            "notes": "Historically #1 patent venue; declined after TC Heartland",
        },
        "dnj": {
            "name": "District of New Jersey",
            "judge": "Multiple patent-experienced judges",
            "speed": "moderate",
            "avg_months_to_trial": 30,
            "patent_case_volume": "high",
            "plaintiff_win_rate": 0.45,
            "markman_timing": "moderate",
            "local_rules": "Local Patent Rules (2009, amended 2021)",
            "strengths": ["Pharmaceutical patent expertise (Hatch-Waxman)", "Large corporate defendant pool"],
            "weaknesses": ["Longer timeline", "Split jury verdicts"],
            "notes": "Premier venue for ANDA/Hatch-Waxman pharmaceutical patent cases",
        },
        "ndca": {
            "name": "Northern District of California (San Jose/San Francisco)",
            "judge": "Multiple tech-savvy judges",
            "speed": "moderate_slow",
            "avg_months_to_trial": 30,
            "patent_case_volume": "high",
            "plaintiff_win_rate": 0.40,
            "markman_timing": "moderate",
            "local_rules": "Patent Local Rules (detailed, since 2001)",
            "strengths": ["Tech-literate judges/jurors", "Strong patent rules", "Silicon Valley proximity"],
            "weaknesses": ["Defendant-friendly", "Longer timelines", "Higher invalidity rates"],
            "notes": "Preferred by tech defendants; strong prior art analysis",
        },
        "dde": {
            "name": "District of Delaware",
            "judge": "Chief Judge Connolly and experienced patent bench",
            "speed": "moderate",
            "avg_months_to_trial": 24,
            "patent_case_volume": "very_high",
            "plaintiff_win_rate": 0.48,
            "markman_timing": "moderate_late",
            "local_rules": "Default Standard for Discovery (2011), streamlined patent procedures",
            "strengths": ["Incorporation venue for most US corps", "Specialized patent bar", "High volume"],
            "weaknesses": ["Crowded docket", "Administrative patent judges rotation"],
            "notes": "Post-TC Heartland surge as many defendants incorporated in Delaware",
        },
        "itc": {
            "name": "International Trade Commission (Section 337)",
            "judge": "Administrative Law Judges",
            "speed": "fast",
            "avg_months_to_trial": 15,
            "patent_case_volume": "moderate",
            "plaintiff_win_rate": 0.55,
            "markman_timing": "early",
            "local_rules": "19 CFR Part 210",
            "strengths": ["Fast timeline", "No eBay analysis for exclusion orders", "In rem jurisdiction",
                          "No damages (exclusion orders only)", "Parallel to district court"],
            "weaknesses": ["No monetary damages", "Domestic industry requirement", "Limited discovery",
                           "Presidential review period"],
            "notes": "Best for import exclusion; requires showing domestic industry (manufacturing, licensing, or substantial investment)",
        },
    }

    def analyze_venue(
        self,
        ip_type: str,
        plaintiff_type: str,
        defendant_location: str,
        speed_priority: str = "moderate",
        budget_constraint: str = "moderate",
    ) -> Dict[str, Any]:
        """Analyze optimal venues for an IP dispute."""
        recommendations: List[Dict[str, Any]] = []
        for venue_id, venue in self.VENUE_DATA.items():
            score = 0.5
            factors: List[str] = []
            if speed_priority == "fast" and venue["speed"] in ("fast",):
                score += 0.15
                factors.append("Fast timeline matches priority")
            elif speed_priority == "moderate" and venue["speed"] in ("fast", "moderate"):
                score += 0.10
                factors.append("Timeline acceptable")
            if plaintiff_type == "npe" and venue.get("plaintiff_win_rate", 0) > 0.50:
                score += 0.10
                factors.append("Above-average plaintiff win rate")
            elif plaintiff_type == "practicing" and venue.get("plaintiff_win_rate", 0) > 0.45:
                score += 0.08
                factors.append("Reasonable plaintiff success rate")
            if ip_type == "pharmaceutical" and venue_id == "dnj":
                score += 0.20
                factors.append("Premier Hatch-Waxman venue")
            elif ip_type == "technology" and venue_id == "ndca":
                score += 0.15
                factors.append("Tech-literate jurisdiction")
            if venue_id == "itc" and ip_type == "import":
                score += 0.25
                factors.append("ITC exclusion order for import disputes")
            recommendations.append({
                "venue_id": venue_id,
                "venue_name": venue["name"],
                "score": round(min(score, 1.0), 3),
                "avg_months_to_trial": venue["avg_months_to_trial"],
                "plaintiff_win_rate": venue["plaintiff_win_rate"],
                "factors": factors,
                "strengths": venue["strengths"],
                "weaknesses": venue["weaknesses"],
                "notes": venue["notes"],
            })
        recommendations.sort(key=lambda x: x["score"], reverse=True)
        return {
            "ip_type": ip_type,
            "plaintiff_type": plaintiff_type,
            "defendant_location": defendant_location,
            "speed_priority": speed_priority,
            "recommendations": recommendations[:4],
            "total_venues_analyzed": len(self.VENUE_DATA),
            "disclaimer": "Venue analysis is informational only. Consult litigation counsel for venue selection.",
        }

    def get_venue_detail(self, venue_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific venue."""
        venue = self.VENUE_DATA.get(venue_id)
        if venue is None:
            return None
        return {"venue_id": venue_id, **venue}

    def compare_venues(self, venue_ids: List[str]) -> Dict[str, Any]:
        """Compare multiple venues side by side."""
        venues = []
        for vid in venue_ids:
            v = self.VENUE_DATA.get(vid)
            if v:
                venues.append({"venue_id": vid, **v})
        if not venues:
            return {"error": "No valid venues found", "requested": venue_ids}
        return {
            "comparison": venues,
            "fastest": min(venues, key=lambda x: x["avg_months_to_trial"])["name"],
            "highest_plaintiff_rate": max(venues, key=lambda x: x["plaintiff_win_rate"])["name"],
        }


_venue_analyzer = IPLitigationVenueAnalyzer()


@app.post("/venue/analyze")
async def analyze_venue(
    ip_type: str = "technology",
    plaintiff_type: str = "practicing",
    defendant_location: str = "unknown",
    speed_priority: str = "moderate",
) -> Dict[str, Any]:
    """Analyze optimal IP litigation venues."""
    result = _venue_analyzer.analyze_venue(
        ip_type=ip_type,
        plaintiff_type=plaintiff_type,
        defendant_location=defendant_location,
        speed_priority=speed_priority,
    )
    return {"engine_id": ENGINE_ID, **result}


@app.get("/venue/{venue_id}")
async def get_venue_detail(venue_id: str) -> Dict[str, Any]:
    """Get detailed venue information."""
    detail = _venue_analyzer.get_venue_detail(venue_id)
    if detail is None:
        return {"engine_id": ENGINE_ID, "error": f"Venue '{venue_id}' not found"}
    return {"engine_id": ENGINE_ID, **detail}


@app.post("/venue/compare")
async def compare_venues(venue_ids: List[str]) -> Dict[str, Any]:
    """Compare multiple litigation venues."""
    result = _venue_analyzer.compare_venues(venue_ids)
    return {"engine_id": ENGINE_ID, **result}


# ############################################################################
#
# SECTION 22: MAIN ENTRY POINT
#
# ############################################################################

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "engine:app",
        host=ENGINE_CONFIG.get("host", "0.0.0.0"),
        port=ENGINE_PORT,
        reload=False,
        log_level="info",
    )