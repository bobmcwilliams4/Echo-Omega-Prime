"""
LG17 Legal Ethics Engine - Main FastAPI Engine
=================================================
Production-grade legal ethics analysis engine implementing all 20 TIE
components for ABA Model Rules of Professional Conduct, attorney-client
privilege, work product doctrine, conflicts of interest, confidentiality,
competence, fees, advertising, UPL/MJP, discipline/sanctions, malpractice,
fiduciary duties, trust accounts (IOLTA), organization as client, diminished
capacity, prosecutorial ethics (Brady), judicial ethics (CJC), mediator
ethics, arbitrator disclosure, Texas DRPC, SOX Section 205, legal tech
ethics (AI, ghost-writing, metadata).

TIE-20 Components:
    1.  three_layer_response
    2.  response_modes (fast, analysis, memo, ethics_opinion, conflict_check)
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

Port: 8407
Engine: LG17 Legal Ethics
Version: 2.0.0
Mode: DET (Deterministic)
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
    ConflictScreener,
    ConflictScreenResult,
    DisciplinaryActionSearcher,
    DoctrineSearchIndex,
    EthicsRuleSearcher,
    MalpracticeRiskAssessor,
    MalpracticeRiskLevel,
    MalpracticeRiskResult,
    SearchResult,
    build_search_index,
    compute_query_hash,
)
from semantic import (
    ConflictChecker,
    ConflictCheckResult,
    ConflictType,
    FeeReasonablenessCalculator,
    FeeReasonablenessResult,
    NormalizationResult,
    PrivilegeAnalyzer,
    PrivilegeAnalysisResult,
    normalize_semantics,
    get_normalizer,
)
from telemetry import (
    AlertSeverity,
    DoctrineMutation,
    ErrorDomain,
    MutationOrigin,
    MutationType,
    QueryTrace,
    ResponseLayer,
    TelemetryCollector,
    complete_trace,
    get_telemetry,
    log_error,
    record_doctrine_mutation,
    trace_query,
)


# ============================================================================
# CONFIGURATION
# ============================================================================

ENGINE_ID = "LG17"
ENGINE_NAME = "Legal Ethics Engine"
ENGINE_VERSION = "2.0.0"
ENGINE_PORT = 8407
ENGINE_DOMAIN = "legal_ethics"
ENGINE_MODE = "DET"
ENGINE_AUTHORITY = 5.0

ENGINE_DIR = Path(__file__).parent
CONFIG_PATH = ENGINE_DIR / "config.json"
LOG_DIR = ENGINE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logger.add(
    LOG_DIR / "lg17_engine_{time}.log",
    rotation="50 MB",
    retention="30 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level:<8} | {name}:{function}:{line} | {message}",
)


def load_config() -> Dict[str, Any]:
    """Load engine configuration from config.json."""
    if CONFIG_PATH.exists():
        with CONFIG_PATH.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    logger.warning(f"Config not found at {CONFIG_PATH}, using defaults")
    return {}


CONFIG = load_config()


# ============================================================================
# TIE COMPONENT 2: RESPONSE MODES
# ============================================================================

class ResponseMode(str, Enum):
    """Response mode determines output depth and format."""
    FAST = "FAST"
    ANALYSIS = "ANALYSIS"
    MEMO = "MEMO"
    ETHICS_OPINION = "ETHICS_OPINION"
    CONFLICT_CHECK = "CONFLICT_CHECK"


class AnalysisLayer(str, Enum):
    """Analysis depth layer."""
    QUICK = "QUICK"
    STANDARD = "STANDARD"
    DEEP = "DEEP"


# ============================================================================
# TIE COMPONENT 5: CONFIDENCE STRATIFICATION
# ============================================================================

class ConfidenceLevel(str, Enum):
    """Confidence level classification."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNCERTAIN = "uncertain"


CONFIDENCE_THRESHOLDS = CONFIG.get("confidence_thresholds", {
    "high": 0.85,
    "medium": 0.65,
    "low": 0.40,
    "uncertain": 0.20,
})


def classify_confidence(score: float) -> ConfidenceLevel:
    """Classify a confidence score into a level."""
    if score >= CONFIDENCE_THRESHOLDS["high"]:
        return ConfidenceLevel.HIGH
    elif score >= CONFIDENCE_THRESHOLDS["medium"]:
        return ConfidenceLevel.MEDIUM
    elif score >= CONFIDENCE_THRESHOLDS["low"]:
        return ConfidenceLevel.LOW
    return ConfidenceLevel.UNCERTAIN


# ============================================================================
# TIE COMPONENT 4: AUTHORITY HARDENING
# ============================================================================

BANNED_PHRASES: List[str] = [
    "i think",
    "i believe",
    "probably",
    "it seems like",
    "in my opinion",
    "you should consider",
    "it might be",
    "it could be",
    "this might",
    "maybe",
    "perhaps",
    "i would guess",
    "it appears that",
    "one could argue",
    "it is possible that",
    "you might want to",
    "i suggest",
]

DISCLOSURE_CAVEATS: Dict[str, str] = {
    "general": "This analysis is for informational purposes only and does not constitute legal advice. Consult qualified legal ethics counsel for situation-specific guidance.",
    "conflict": "Conflict-of-interest analysis is highly fact-specific. This screening identifies potential conflicts based on the information provided; a comprehensive review by qualified counsel is recommended.",
    "privilege": "Privilege determinations depend on the specific facts and applicable jurisdiction. This analysis identifies likely privilege protections but a definitive determination requires review of the actual communications.",
    "discipline": "Disciplinary sanction analysis is based on ABA Standards and published precedent. Actual sanctions vary by jurisdiction, hearing panel, and specific circumstances.",
    "malpractice": "Malpractice risk assessment is based on common risk factors. This is not a legal opinion on liability exposure. Consult with a legal malpractice specialist for case-specific assessment.",
    "fees": "Fee reasonableness is determined by the specific facts under the eight factors of Model Rule 1.5(a). This analysis provides a framework assessment, not a definitive determination.",
    "texas": "Texas Disciplinary Rules of Professional Conduct differ from the ABA Model Rules in several significant ways. Confirm applicable rules with the State Bar of Texas for Texas-specific matters.",
}


def apply_authority_hardening(text: str) -> str:
    """Remove soft language from analysis text."""
    result = text
    for phrase in BANNED_PHRASES:
        lower_result = result.lower()
        idx = lower_result.find(phrase)
        while idx != -1:
            end = idx + len(phrase)
            result = result[:idx] + result[end:]
            lower_result = result.lower()
            idx = lower_result.find(phrase)
    result = " ".join(result.split())
    return result


# ============================================================================
# TIE COMPONENT 14: FACT FRAGILITY SCORING
# ============================================================================

def compute_fact_fragility(
    query: str,
    doctrine_confidence: float,
    jurisdiction: str,
    rules_detected: int,
) -> Dict[str, Any]:
    """Compute how fragile the factual basis is for the analysis."""
    fragility_score = 0.0
    factors: List[str] = []

    # Jurisdiction variability
    if jurisdiction not in ("ABA_MODEL", "FEDERAL"):
        fragility_score += 0.15
        factors.append(f"State-specific rules ({jurisdiction}) may vary from Model Rules")

    # Low rule detection
    if rules_detected == 0:
        fragility_score += 0.25
        factors.append("No specific rules detected in query — analysis may be broad")
    elif rules_detected == 1:
        fragility_score += 0.05

    # Query ambiguity
    ambiguous_terms = ["can i", "should i", "is it ok", "what happens if", "what if"]
    for term in ambiguous_terms:
        if term in query.lower():
            fragility_score += 0.10
            factors.append(f"Ambiguous phrasing detected ('{term}')")
            break

    # Low doctrine confidence
    if doctrine_confidence < 0.65:
        fragility_score += 0.20
        factors.append("Doctrine match confidence below threshold")

    fragility_score = min(1.0, fragility_score)
    fragility_level = "high" if fragility_score > 0.5 else ("moderate" if fragility_score > 0.25 else "low")

    return {
        "fragility_score": round(fragility_score, 3),
        "fragility_level": fragility_level,
        "factors": factors,
        "recommendation": (
            "Analysis is based on well-established rules with high confidence"
            if fragility_level == "low"
            else "Analysis depends on fact-specific determinations — verify with the applicable jurisdiction's rules"
        ),
    }


# ============================================================================
# TIE COMPONENT 13: ZONED ANALYSIS
# ============================================================================

ETHICS_ZONES: Dict[str, Dict[str, Any]] = {
    "client_relationship": {
        "rules": ["1.1", "1.2", "1.3", "1.4", "1.5", "1.6", "1.14", "1.15", "1.16"],
        "description": "Client-lawyer relationship duties",
        "topics": ["competence", "scope", "diligence", "communication", "fees", "confidentiality", "diminished_capacity", "trust_accounts", "withdrawal"],
    },
    "conflicts": {
        "rules": ["1.7", "1.8", "1.9", "1.10", "1.11", "1.12", "1.13"],
        "description": "Conflicts of interest",
        "topics": ["concurrent", "successive", "imputed", "government", "organization"],
    },
    "advocacy": {
        "rules": ["3.1", "3.3", "3.4", "3.5", "3.6", "3.7", "3.8"],
        "description": "Advocate duties",
        "topics": ["candor", "fairness", "trial_publicity", "prosecutorial"],
    },
    "third_parties": {
        "rules": ["4.1", "4.2", "4.3", "4.4"],
        "description": "Dealings with third parties",
        "topics": ["truthfulness", "no_contact", "unrepresented"],
    },
    "law_practice": {
        "rules": ["5.1", "5.3", "5.4", "5.5", "5.7"],
        "description": "Law firms, supervision, UPL",
        "topics": ["supervision", "nonlawyer", "professional_independence", "upl", "mjp"],
    },
    "advertising": {
        "rules": ["7.1", "7.2", "7.3"],
        "description": "Information about legal services",
        "topics": ["advertising", "solicitation", "barratry"],
    },
    "integrity": {
        "rules": ["8.1", "8.3", "8.4", "8.5"],
        "description": "Professional integrity",
        "topics": ["reporting", "misconduct", "discipline"],
    },
    "privilege": {
        "rules": [],
        "description": "Attorney-client privilege and work product",
        "topics": ["privilege", "upjohn", "crime_fraud", "work_product"],
    },
    "judicial_adr": {
        "rules": [],
        "description": "Judicial ethics, mediator/arbitrator ethics",
        "topics": ["judicial_ethics", "mediator", "arbitrator"],
    },
    "emerging": {
        "rules": [],
        "description": "Legal technology, AI, social media ethics",
        "topics": ["legal_tech", "ai", "ghost_writing", "metadata", "social_media"],
    },
}


def detect_zone(query: str, ethics_domains: List[str]) -> str:
    """Detect the analysis zone based on query and detected domains."""
    zone_scores: Dict[str, int] = defaultdict(int)
    lower_query = query.lower()

    for zone_name, zone_info in ETHICS_ZONES.items():
        for topic in zone_info["topics"]:
            if topic in lower_query:
                zone_scores[zone_name] += 2
            for domain in ethics_domains:
                if topic in domain:
                    zone_scores[zone_name] += 1

    if not zone_scores:
        return "client_relationship"

    return max(zone_scores.items(), key=lambda x: x[1])[0]


# ============================================================================
# PYDANTIC MODELS - REQUEST / RESPONSE
# ============================================================================

class EthicsQueryRequest(BaseModel):
    """Incoming query request."""
    query: str = Field(..., min_length=3, max_length=10000, description="The legal ethics question")
    response_mode: ResponseMode = Field(default=ResponseMode.ANALYSIS, description="Response depth mode")
    analysis_layer: AnalysisLayer = Field(default=AnalysisLayer.STANDARD, description="Analysis depth")
    jurisdiction: str = Field(default="ABA_MODEL", description="Primary jurisdiction")
    include_texas_notes: bool = Field(default=True, description="Include Texas-specific annotations")
    include_practice_tips: bool = Field(default=True, description="Include practice tips")
    max_results: int = Field(default=10, ge=1, le=50, description="Maximum search results")

    @field_validator("query")
    @classmethod
    def validate_query(cls, v: str) -> str:
        stripped = v.strip()
        if len(stripped) < 3:
            raise ValueError("Query must be at least 3 characters")
        return stripped


class EthicsQueryResponse(BaseModel):
    """Response to a legal ethics query."""
    engine_id: str = ENGINE_ID
    engine_version: str = ENGINE_VERSION
    engine_mode: str = ENGINE_MODE
    query: str
    normalized_query: str
    response_mode: str
    analysis_layer: str
    jurisdiction: str
    # TIE Component 1: Three-layer response
    doctrine_response: Optional[Dict[str, Any]] = None
    search_response: Optional[Dict[str, Any]] = None
    deep_response: Optional[Dict[str, Any]] = None
    # Core analysis
    primary_analysis: str
    rules_applicable: List[str]
    ethics_domains: List[str]
    privilege_indicators: List[str]
    conflict_indicators: List[str]
    # TIE Components
    confidence: float
    confidence_level: str
    citations: List[str]
    practice_tips: List[str]
    texas_notes: Optional[str] = None
    fact_fragility: Optional[Dict[str, Any]] = None
    analysis_zone: str
    disclosure_caveat: str
    # Metadata
    normalization_info: Dict[str, Any]
    search_results_count: int
    doctrine_blocks_matched: int
    response_layer: str
    determinism_hash: str
    trace_id: str
    latency_ms: float
    timestamp: str


class ConflictCheckRequest(BaseModel):
    """Request for conflict check."""
    current_client: str = Field(..., min_length=2)
    prospective_client: str = Field(..., min_length=2)
    matter_description: str = Field(default="")
    prior_representations: List[str] = Field(default_factory=list)


class PrivilegeCheckRequest(BaseModel):
    """Request for privilege analysis."""
    description: str = Field(..., min_length=10)
    communication_type: str = Field(default="")
    parties_involved: List[str] = Field(default_factory=list)
    purpose: str = Field(default="")


class FeeCheckRequest(BaseModel):
    """Request for fee reasonableness analysis."""
    fee_amount: float = Field(..., gt=0)
    hours_worked: float = Field(default=0.0, ge=0)
    hourly_rate: float = Field(default=0.0, ge=0)
    matter_type: str = Field(default="")
    matter_complexity: str = Field(default="moderate")
    jurisdiction: str = Field(default="TX")
    results_obtained: str = Field(default="")
    lawyer_experience_years: int = Field(default=10, ge=0)
    is_contingent: bool = Field(default=False)
    contingent_percentage: float = Field(default=0.0, ge=0, le=100)


class MalpracticeRiskRequest(BaseModel):
    """Request for malpractice risk assessment."""
    matter_description: str = Field(..., min_length=10)
    risk_factors: List[str] = Field(default_factory=list)
    has_engagement_letter: bool = Field(default=True)
    has_malpractice_insurance: bool = Field(default=True)
    lawyer_experience_years: int = Field(default=10, ge=0)


class DisciplineAnalysisRequest(BaseModel):
    """Request for discipline/sanction analysis."""
    violation_type: str = Field(..., min_length=3)
    mental_state: str = Field(default="knowing")
    injury_level: str = Field(default="moderate")
    prior_discipline: bool = Field(default=False)
    cooperative: bool = Field(default=True)


class ConflictScreenRequest(BaseModel):
    """Request for multi-party conflict screening."""
    client_name: str = Field(..., min_length=2)
    adverse_parties: List[str] = Field(default_factory=list)
    related_entities: List[str] = Field(default_factory=list)
    matter_description: str = Field(default="")
    prior_clients: List[str] = Field(default_factory=list)


# ============================================================================
# ENGINE STATE
# ============================================================================

class EngineState:
    """Holds initialized engine components."""

    def __init__(self) -> None:
        self.doctrine_cache: Optional[DoctrineCacheIndex] = None
        self.search_index: Optional[DoctrineSearchIndex] = None
        self.telemetry: Optional[TelemetryCollector] = None
        self.conflict_checker = ConflictChecker()
        self.privilege_analyzer = PrivilegeAnalyzer()
        self.fee_calculator = FeeReasonablenessCalculator()
        self.ethics_rule_searcher = EthicsRuleSearcher()
        self.conflict_screener = ConflictScreener()
        self.malpractice_assessor = MalpracticeRiskAssessor()
        self.discipline_searcher = DisciplinaryActionSearcher()
        self.boot_time: float = time.time()
        self.query_count: int = 0

    def initialize(self) -> None:
        """Initialize all engine components."""
        start = time.time()
        self.doctrine_cache = build_doctrine_cache()
        self.search_index = build_search_index(DOCTRINE_BLOCKS)
        self.telemetry = get_telemetry()
        elapsed = (time.time() - start) * 1000
        logger.info(
            f"LG17 Legal Ethics Engine initialized in {elapsed:.1f}ms: "
            f"{self.doctrine_cache.total_blocks} doctrine blocks, "
            f"{self.search_index.total_documents} search docs"
        )


ENGINE_STATE = EngineState()


# ============================================================================
# TIE COMPONENT 16: DETERMINISM HASH
# ============================================================================

def compute_determinism_hash(
    query: str,
    response_mode: str,
    analysis_layer: str,
    jurisdiction: str,
    primary_analysis: str,
) -> str:
    """Compute SHA-256 determinism hash for the response."""
    salt = CONFIG.get("determinism", {}).get("salt", "LG17_LEGAL_ETHICS_v2")
    content = f"{salt}|{query}|{response_mode}|{analysis_layer}|{jurisdiction}|{primary_analysis}|{ENGINE_VERSION}"
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


# ============================================================================
# TIE COMPONENT 19: MULTI-DOCTRINE DECOMPOSITION
# ============================================================================

def decompose_multi_doctrine(
    query: str,
    doctrine_results: List[DoctrineCacheBlock],
    search_results: List[SearchResult],
) -> Dict[str, Any]:
    """Decompose a query that spans multiple doctrine areas."""
    doctrine_groups: Dict[str, List[str]] = defaultdict(list)
    for block in doctrine_results:
        doctrine_groups[block.category].append(block.topic)
    for result in search_results:
        if result.category:
            doctrine_groups[result.category].append(result.topic)

    return {
        "multi_doctrine": len(doctrine_groups) > 1,
        "doctrine_groups": dict(doctrine_groups),
        "primary_doctrine": max(doctrine_groups.items(), key=lambda x: len(x[1]))[0] if doctrine_groups else "unknown",
        "cross_cutting_topics": [
            topic
            for topics in doctrine_groups.values()
            for topic in topics
            if sum(1 for ts in doctrine_groups.values() if topic in ts) > 1
        ],
        "total_doctrines_involved": sum(len(v) for v in doctrine_groups.values()),
    }


# ============================================================================
# TIE COMPONENT 1: THREE-LAYER RESPONSE BUILDER
# ============================================================================

async def build_three_layer_response(
    query: str,
    norm_result: NormalizationResult,
    response_mode: ResponseMode,
    analysis_layer: AnalysisLayer,
    jurisdiction: str,
    include_texas_notes: bool,
    include_practice_tips: bool,
    max_results: int,
    trace: QueryTrace,
) -> Dict[str, Any]:
    """Build the three-layer response: doctrine -> search -> deep."""
    result: Dict[str, Any] = {
        "doctrine_response": None,
        "search_response": None,
        "deep_response": None,
        "primary_analysis": "",
        "rules_applicable": [],
        "citations": [],
        "practice_tips": [],
        "texas_notes": None,
        "confidence": 0.0,
        "response_layer": "fallback",
        "doctrine_blocks_matched": 0,
        "search_results_count": 0,
    }

    # LAYER 1: Doctrine Cache
    t0 = time.time()
    doctrine_blocks = search_doctrines(query, max_results=max_results)
    if norm_result.rules_detected:
        for rule in norm_result.rules_detected:
            topic_block = get_doctrine_block(rule.lower().replace("rule_", "").replace("_", "_"))
            if topic_block and topic_block not in doctrine_blocks:
                doctrine_blocks.insert(0, topic_block)

    doctrine_ms = (time.time() - t0) * 1000
    trace.add_sub_trace("doctrine_cache", doctrine_ms, {"blocks_found": len(doctrine_blocks)})

    if doctrine_blocks:
        primary_block = doctrine_blocks[0]
        result["doctrine_response"] = {
            "blocks": [b.to_dict() for b in doctrine_blocks[:5]],
            "primary_topic": primary_block.topic,
            "primary_category": primary_block.category,
        }
        result["primary_analysis"] = primary_block.analysis
        result["rules_applicable"] = [
            b.rule_reference for b in doctrine_blocks if b.rule_reference
        ]
        result["citations"] = [b.authority for b in doctrine_blocks if b.authority]
        if include_practice_tips:
            for b in doctrine_blocks[:3]:
                result["practice_tips"].extend(b.practice_tips)
        if include_texas_notes:
            texas_parts = [b.texas_notes for b in doctrine_blocks if b.texas_notes]
            if texas_parts:
                result["texas_notes"] = " | ".join(texas_parts[:3])
        result["confidence"] = primary_block.confidence
        result["response_layer"] = "doctrine_cache"
        result["doctrine_blocks_matched"] = len(doctrine_blocks)
        trace.doctrine_topic = primary_block.topic
        trace.doctrine_blocks_matched = len(doctrine_blocks)

        if response_mode == ResponseMode.FAST:
            trace.complete(ResponseLayer.DOCTRINE_CACHE, primary_block.confidence)
            return result

    # LAYER 2: Search Index
    t1 = time.time()
    search_results: List[SearchResult] = []
    if ENGINE_STATE.search_index:
        search_results = ENGINE_STATE.search_index.search(query, top_k=max_results)
    search_ms = (time.time() - t1) * 1000
    trace.add_sub_trace("search_index", search_ms, {"results_found": len(search_results)})
    trace.search_results_count = len(search_results)

    if search_results:
        result["search_response"] = {
            "results": [
                {
                    "topic": r.topic,
                    "category": r.category,
                    "score": r.score,
                    "snippet": r.snippet,
                    "authority": r.authority,
                    "rule_reference": r.rule_reference,
                }
                for r in search_results[:10]
            ],
            "total_results": len(search_results),
        }
        result["search_results_count"] = len(search_results)
        if not result["primary_analysis"] and search_results:
            result["primary_analysis"] = search_results[0].snippet
            result["response_layer"] = "semantic_search"
            result["confidence"] = max(result["confidence"], 0.65)
        if not result["citations"]:
            result["citations"] = [r.authority for r in search_results if r.authority][:5]
        if not result["rules_applicable"]:
            result["rules_applicable"] = [r.rule_reference for r in search_results if r.rule_reference][:5]

    # LAYER 3: Deep Analysis
    if analysis_layer in (AnalysisLayer.STANDARD, AnalysisLayer.DEEP):
        t2 = time.time()
        decomposition = decompose_multi_doctrine(query, doctrine_blocks, search_results)
        zone = detect_zone(query, norm_result.ethics_domains)
        fact_frag = compute_fact_fragility(
            query,
            result["confidence"],
            jurisdiction,
            len(norm_result.rules_detected),
        )
        deep_ms = (time.time() - t2) * 1000
        trace.add_sub_trace("deep_analysis", deep_ms)

        result["deep_response"] = {
            "decomposition": decomposition,
            "zone": zone,
            "zone_info": ETHICS_ZONES.get(zone, {}),
            "fact_fragility": fact_frag,
            "ethics_domains": norm_result.ethics_domains,
            "privilege_indicators": norm_result.privilege_indicators,
            "conflict_indicators": norm_result.conflict_indicators,
            "discipline_indicators": norm_result.discipline_indicators,
        }

        if not result["response_layer"] or result["response_layer"] == "fallback":
            result["response_layer"] = "deep_analysis"

    # Apply authority hardening
    if result["primary_analysis"]:
        result["primary_analysis"] = apply_authority_hardening(result["primary_analysis"])

    # Fallback
    if not result["primary_analysis"]:
        result["primary_analysis"] = (
            "The query did not match specific doctrine blocks or search index entries. "
            "Consider refining the query with specific Model Rule references, ethics concepts, "
            "or practice area terminology."
        )
        result["confidence"] = 0.20
        result["response_layer"] = "fallback"

    return result


# ============================================================================
# TIE COMPONENT 9: DOCTRINE DRIFT WATCHER
# ============================================================================

class DoctrineDriftWatcher:
    """Monitor doctrine cache for drift, staleness, and integrity issues."""

    def __init__(self) -> None:
        self._baseline_hash: str = get_doctrine_cache_hash()
        self._last_check: float = time.time()
        self._check_interval_seconds: int = 3600
        self._drift_events: List[Dict[str, Any]] = []

    def check_drift(self) -> Dict[str, Any]:
        """Check for doctrine drift from baseline."""
        current_hash = get_doctrine_cache_hash()
        integrity = verify_doctrine_integrity()
        stale = get_stale_doctrines(max_age_days=365)
        drifted = current_hash != self._baseline_hash

        result = {
            "drifted": drifted,
            "baseline_hash": self._baseline_hash[:16] + "...",
            "current_hash": current_hash[:16] + "...",
            "integrity": integrity,
            "stale_doctrines": stale,
            "stale_count": len(stale),
            "last_check": datetime.fromtimestamp(self._last_check, tz=timezone.utc).isoformat(),
        }

        if drifted:
            event = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "old_hash": self._baseline_hash[:16],
                "new_hash": current_hash[:16],
            }
            self._drift_events.append(event)
            logger.warning(f"Doctrine drift detected: {event}")

        self._last_check = time.time()
        return result

    def reset_baseline(self) -> str:
        """Reset the baseline hash to current state."""
        self._baseline_hash = get_doctrine_cache_hash()
        return self._baseline_hash


DRIFT_WATCHER = DoctrineDriftWatcher()


# ============================================================================
# FASTAPI LIFESPAN
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize engine on startup, cleanup on shutdown."""
    logger.info(f"Starting LG17 Legal Ethics Engine v{ENGINE_VERSION} on port {ENGINE_PORT}")
    ENGINE_STATE.initialize()
    yield
    logger.info("LG17 Legal Ethics Engine shutting down")


# ============================================================================
# TIE COMPONENT 17: FASTAPI SERVER
# ============================================================================

app = FastAPI(
    title="LG17 Legal Ethics Engine",
    description=(
        "Comprehensive legal ethics analysis engine implementing all 20 TIE components. "
        "Covers ABA Model Rules, attorney-client privilege, work product doctrine, "
        "conflicts of interest, confidentiality, fees, discipline, malpractice, "
        "judicial ethics, ADR ethics, legal tech ethics, and Texas-specific rules."
    ),
    version=ENGINE_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CONFIG.get("api", {}).get("cors_origins", ["*"]),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# TIE COMPONENT 12: HEALTH ENDPOINT
# ============================================================================

@app.get("/health")
async def health_check() -> Dict[str, Any]:
    """Health check endpoint."""
    telemetry = get_telemetry()
    cache_stats = get_doctrine_cache_stats()
    return {
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "version": ENGINE_VERSION,
        "mode": ENGINE_MODE,
        "port": ENGINE_PORT,
        "authority": ENGINE_AUTHORITY,
        "status": "healthy",
        "uptime_seconds": round(time.time() - ENGINE_STATE.boot_time, 1),
        "query_count": ENGINE_STATE.query_count,
        "doctrine_cache": cache_stats,
        "search_index": {
            "total_documents": ENGINE_STATE.search_index.total_documents if ENGINE_STATE.search_index else 0,
            "total_terms": ENGINE_STATE.search_index.total_terms if ENGINE_STATE.search_index else 0,
        },
        "telemetry": telemetry.get_health(),
        "tie_components": "20/20",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ============================================================================
# MAIN QUERY ENDPOINT
# ============================================================================

@app.post("/query", response_model=EthicsQueryResponse)
async def query_ethics(request: EthicsQueryRequest) -> EthicsQueryResponse:
    """Process a legal ethics query through the full TIE-20 pipeline."""
    ENGINE_STATE.query_count += 1
    telemetry = get_telemetry()

    # Start trace
    trace = trace_query(
        query_text=request.query,
        response_mode=request.response_mode.value,
        analysis_layer=request.analysis_layer.value,
        jurisdiction=request.jurisdiction,
    )

    try:
        # TIE Component 6: Semantic normalization
        t_norm = time.time()
        norm_result = normalize_semantics(request.query)
        norm_ms = (time.time() - t_norm) * 1000
        trace.add_sub_trace("semantic_normalization", norm_ms)
        trace.semantic_normalized = bool(norm_result.mappings_applied)
        trace.jurisdiction = norm_result.jurisdiction_detected or request.jurisdiction

        # Record domain-specific telemetry
        for domain in norm_result.ethics_domains:
            telemetry.ethics_metrics.record_domain_query(domain)

        # Build three-layer response
        layers = await build_three_layer_response(
            query=request.query,
            norm_result=norm_result,
            response_mode=request.response_mode,
            analysis_layer=request.analysis_layer,
            jurisdiction=request.jurisdiction,
            include_texas_notes=request.include_texas_notes,
            include_practice_tips=request.include_practice_tips,
            max_results=request.max_results,
            trace=trace,
        )

        confidence = layers["confidence"]
        confidence_level = classify_confidence(confidence)

        # Compute determinism hash
        det_hash = compute_determinism_hash(
            query=request.query,
            response_mode=request.response_mode.value,
            analysis_layer=request.analysis_layer.value,
            jurisdiction=request.jurisdiction,
            primary_analysis=layers["primary_analysis"],
        )

        # Compute fact fragility
        fact_frag = compute_fact_fragility(
            request.query,
            confidence,
            request.jurisdiction,
            len(norm_result.rules_detected),
        )

        # Determine zone
        zone = detect_zone(request.query, norm_result.ethics_domains)

        # Select disclosure caveat
        caveat_key = "general"
        if norm_result.conflict_indicators:
            caveat_key = "conflict"
        elif norm_result.privilege_indicators:
            caveat_key = "privilege"
        elif any(d in norm_result.ethics_domains for d in ["discipline", "disbarment", "suspension"]):
            caveat_key = "discipline"
        elif any(d in norm_result.ethics_domains for d in ["malpractice", "fiduciary_duty"]):
            caveat_key = "malpractice"
        elif any(d in norm_result.ethics_domains for d in ["fees", "contingency_fees", "fee_splitting"]):
            caveat_key = "fees"
        elif request.jurisdiction == "TX" or "texas" in request.query.lower():
            caveat_key = "texas"

        # Complete trace
        trace.complete(
            layer=ResponseLayer(layers["response_layer"]) if layers["response_layer"] in [e.value for e in ResponseLayer] else ResponseLayer.FALLBACK,
            confidence=confidence,
        )
        complete_trace(trace)

        return EthicsQueryResponse(
            query=request.query,
            normalized_query=norm_result.normalized_query,
            response_mode=request.response_mode.value,
            analysis_layer=request.analysis_layer.value,
            jurisdiction=request.jurisdiction,
            doctrine_response=layers["doctrine_response"],
            search_response=layers["search_response"],
            deep_response=layers["deep_response"],
            primary_analysis=layers["primary_analysis"],
            rules_applicable=layers["rules_applicable"],
            ethics_domains=norm_result.ethics_domains,
            privilege_indicators=norm_result.privilege_indicators,
            conflict_indicators=norm_result.conflict_indicators,
            confidence=round(confidence, 4),
            confidence_level=confidence_level.value,
            citations=layers["citations"],
            practice_tips=layers["practice_tips"][:10],
            texas_notes=layers["texas_notes"],
            fact_fragility=fact_frag,
            analysis_zone=zone,
            disclosure_caveat=DISCLOSURE_CAVEATS.get(caveat_key, DISCLOSURE_CAVEATS["general"]),
            normalization_info={
                "mappings_applied": len(norm_result.mappings_applied),
                "rules_detected": norm_result.rules_detected,
                "ethics_domains": norm_result.ethics_domains,
                "jurisdiction_detected": norm_result.jurisdiction_detected,
                "confidence_boost": norm_result.confidence_boost,
                "duration_ms": round(norm_result.duration_ms, 3),
            },
            search_results_count=layers["search_results_count"],
            doctrine_blocks_matched=layers["doctrine_blocks_matched"],
            response_layer=layers["response_layer"],
            determinism_hash=det_hash,
            trace_id=trace.trace_id,
            latency_ms=round(trace.total_ms, 3),
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

    except Exception as exc:
        trace.error_message = str(exc)
        trace.error_domain = ErrorDomain.SYSTEM
        trace.complete(ResponseLayer.ERROR, 0.0)
        complete_trace(trace)
        log_error(ErrorDomain.SYSTEM, str(exc), trace_id=trace.trace_id)
        raise HTTPException(status_code=500, detail=f"Query processing error: {exc}")


# ============================================================================
# CONFLICT CHECK ENDPOINT
# ============================================================================

@app.post("/conflict-check")
async def conflict_check(request: ConflictCheckRequest) -> Dict[str, Any]:
    """Run a conflict-of-interest check."""
    telemetry = get_telemetry()
    telemetry.ethics_metrics.record_conflict_check()
    result = ENGINE_STATE.conflict_checker.check(
        current_client=request.current_client,
        prospective_client=request.prospective_client,
        matter_description=request.matter_description,
        prior_representations=request.prior_representations,
    )
    return {
        "engine_id": ENGINE_ID,
        "analysis_type": "conflict_check",
        "conflict_found": result.conflict_found,
        "conflict_type": result.conflict_type.value if result.conflict_type else None,
        "parties_involved": result.parties_involved,
        "rule_applicable": result.rule_applicable,
        "consentable": result.consentable,
        "consent_requirements": result.consent_requirements,
        "screening_available": result.screening_available,
        "risk_level": result.risk_level,
        "analysis": result.analysis,
        "recommendations": result.recommendations,
        "disclosure_caveat": DISCLOSURE_CAVEATS["conflict"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ============================================================================
# CONFLICT SCREEN ENDPOINT
# ============================================================================

@app.post("/conflict-screen")
async def conflict_screen(request: ConflictScreenRequest) -> Dict[str, Any]:
    """Screen multiple parties for conflicts."""
    telemetry = get_telemetry()
    telemetry.ethics_metrics.record_conflict_check()
    result = ENGINE_STATE.conflict_screener.screen_parties(
        client_name=request.client_name,
        adverse_parties=request.adverse_parties,
        related_entities=request.related_entities,
        matter_description=request.matter_description,
        prior_clients=request.prior_clients,
    )
    return {
        "engine_id": ENGINE_ID,
        "analysis_type": "conflict_screen",
        "conflicts_found": result.conflicts_found,
        "total_pairs_checked": result.total_pairs_checked,
        "conflicts": result.conflicts,
        "clear_pairs": result.clear_pairs,
        "screening_hash": result.screening_hash,
        "duration_ms": result.duration_ms,
        "disclosure_caveat": DISCLOSURE_CAVEATS["conflict"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ============================================================================
# PRIVILEGE CHECK ENDPOINT
# ============================================================================

@app.post("/privilege-check")
async def privilege_check(request: PrivilegeCheckRequest) -> Dict[str, Any]:
    """Analyze attorney-client privilege / work product protection."""
    telemetry = get_telemetry()
    telemetry.ethics_metrics.record_privilege_assessment()
    result = ENGINE_STATE.privilege_analyzer.analyze_privilege(
        description=request.description,
        communication_type=request.communication_type,
        parties_involved=request.parties_involved,
        purpose=request.purpose,
    )
    return {
        "engine_id": ENGINE_ID,
        "analysis_type": "privilege_check",
        "privilege_likely": result.privilege_likely,
        "privilege_type": result.privilege_type.value if result.privilege_type else None,
        "elements_met": result.elements_met,
        "elements_missing": result.elements_missing,
        "exceptions_applicable": result.exceptions_applicable,
        "waiver_risk": result.waiver_risk,
        "analysis": result.analysis,
        "recommendations": result.recommendations,
        "disclosure_caveat": DISCLOSURE_CAVEATS["privilege"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ============================================================================
# FEE REASONABLENESS ENDPOINT
# ============================================================================

@app.post("/fee-check")
async def fee_check(request: FeeCheckRequest) -> Dict[str, Any]:
    """Analyze fee reasonableness under Rule 1.5(a)."""
    telemetry = get_telemetry()
    telemetry.ethics_metrics.record_fee_check()
    result = ENGINE_STATE.fee_calculator.analyze(
        fee_amount=request.fee_amount,
        hours_worked=request.hours_worked,
        hourly_rate=request.hourly_rate,
        matter_type=request.matter_type,
        matter_complexity=request.matter_complexity,
        jurisdiction=request.jurisdiction,
        results_obtained=request.results_obtained,
        lawyer_experience_years=request.lawyer_experience_years,
        is_contingent=request.is_contingent,
        contingent_percentage=request.contingent_percentage,
    )
    return {
        "engine_id": ENGINE_ID,
        "analysis_type": "fee_reasonableness",
        "reasonable": result.reasonable,
        "score": result.score,
        "factors": result.factors,
        "analysis": result.analysis,
        "recommendations": result.recommendations,
        "disclosure_caveat": DISCLOSURE_CAVEATS["fees"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ============================================================================
# MALPRACTICE RISK ENDPOINT
# ============================================================================

@app.post("/malpractice-risk")
async def malpractice_risk(request: MalpracticeRiskRequest) -> Dict[str, Any]:
    """Assess malpractice risk exposure."""
    result = ENGINE_STATE.malpractice_assessor.assess(
        matter_description=request.matter_description,
        risk_factors=request.risk_factors,
        has_engagement_letter=request.has_engagement_letter,
        has_malpractice_insurance=request.has_malpractice_insurance,
        lawyer_experience_years=request.lawyer_experience_years,
    )
    return {
        "engine_id": ENGINE_ID,
        "analysis_type": "malpractice_risk",
        "risk_level": result.risk_level.value,
        "risk_score": result.risk_score,
        "risk_factors": result.risk_factors,
        "mitigation_steps": result.mitigation_steps,
        "insurance_considerations": result.insurance_considerations,
        "analysis": result.analysis,
        "disclosure_caveat": DISCLOSURE_CAVEATS["malpractice"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ============================================================================
# DISCIPLINE ANALYSIS ENDPOINT
# ============================================================================

@app.post("/discipline-analysis")
async def discipline_analysis(request: DisciplineAnalysisRequest) -> Dict[str, Any]:
    """Analyze potential disciplinary sanctions."""
    telemetry = get_telemetry()
    telemetry.ethics_metrics.record_discipline_risk()
    result = ENGINE_STATE.discipline_searcher.analyze_sanction_factors(
        violation_type=request.violation_type,
        mental_state=request.mental_state,
        injury_level=request.injury_level,
        prior_discipline=request.prior_discipline,
        cooperative=request.cooperative,
    )
    return {
        "engine_id": ENGINE_ID,
        "analysis_type": "discipline_analysis",
        **result,
        "disclosure_caveat": DISCLOSURE_CAVEATS["discipline"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ============================================================================
# DOCTRINE ENDPOINTS
# ============================================================================

@app.get("/doctrines")
async def list_doctrines() -> Dict[str, Any]:
    """List all doctrine topics and categories."""
    return {
        "engine_id": ENGINE_ID,
        "stats": get_doctrine_cache_stats(),
        "topics": get_all_doctrine_topics(),
        "categories": get_all_doctrine_categories(),
        "coverage_map": get_coverage_map(),
    }


@app.get("/doctrine/{topic}")
async def get_doctrine(topic: str) -> Dict[str, Any]:
    """Get a specific doctrine block by topic."""
    block = get_doctrine_block(topic)
    if not block:
        raise HTTPException(status_code=404, detail=f"Doctrine topic '{topic}' not found")
    return {
        "engine_id": ENGINE_ID,
        "doctrine": block.to_dict(),
    }


# ============================================================================
# TIE COMPONENT 10: DOCTRINE COVERAGE MAP
# ============================================================================

@app.get("/coverage")
async def get_doctrine_coverage() -> Dict[str, Any]:
    """Get the doctrine coverage map."""
    coverage = get_coverage_map()
    integrity = verify_doctrine_integrity()
    return {
        "engine_id": ENGINE_ID,
        "coverage_map": coverage,
        "integrity": integrity,
        "total_blocks": len(DOCTRINE_BLOCKS),
        "total_categories": len(coverage),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ============================================================================
# TIE COMPONENT 9: DRIFT WATCHER ENDPOINT
# ============================================================================

@app.get("/drift")
async def check_doctrine_drift() -> Dict[str, Any]:
    """Check for doctrine drift."""
    return {
        "engine_id": ENGINE_ID,
        "drift_report": DRIFT_WATCHER.check_drift(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ============================================================================
# TIE COMPONENT 11: METRICS ENDPOINT
# ============================================================================

@app.get("/metrics")
async def get_metrics() -> Dict[str, Any]:
    """Get telemetry metrics."""
    telemetry = get_telemetry()
    return {
        "engine_id": ENGINE_ID,
        "health": telemetry.get_health(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ============================================================================
# TIE COMPONENT 15: AUDIT TRAIL ENDPOINT
# ============================================================================

@app.get("/audit")
async def get_audit_trail() -> Dict[str, Any]:
    """Get audit trail status and verify integrity."""
    telemetry = get_telemetry()
    valid, count, error = telemetry.audit.verify_chain(max_entries=10000)
    return {
        "engine_id": ENGINE_ID,
        "audit_trail": {
            "entry_count": telemetry.audit.entry_count,
            "last_hash": telemetry.audit.last_hash[:16] + "...",
            "chain_valid": valid,
            "verified_entries": count,
            "error": error,
        },
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ============================================================================
# RULE SEARCH ENDPOINT
# ============================================================================

@app.get("/rules/search")
async def search_rules(keyword: str = Query(..., min_length=2)) -> Dict[str, Any]:
    """Search Model Rules by keyword."""
    results = ENGINE_STATE.ethics_rule_searcher.search_by_keyword(keyword)
    return {
        "engine_id": ENGINE_ID,
        "keyword": keyword,
        "results": results,
        "total_found": len(results),
    }


@app.get("/rules/{rule_number}")
async def get_rule_info(rule_number: str) -> Dict[str, Any]:
    """Get information about a specific Model Rule."""
    title = ENGINE_STATE.ethics_rule_searcher.get_rule_title(rule_number)
    category = ENGINE_STATE.ethics_rule_searcher.get_category_for_rule(rule_number)
    related = ENGINE_STATE.ethics_rule_searcher.get_related_rules(rule_number)
    return {
        "engine_id": ENGINE_ID,
        "rule": rule_number,
        "title": title,
        "category": category,
        "related_rules": related,
    }


# ============================================================================
# ZONES ENDPOINT
# ============================================================================

@app.get("/zones")
async def get_ethics_zones() -> Dict[str, Any]:
    """Get ethics analysis zones."""
    return {
        "engine_id": ENGINE_ID,
        "zones": ETHICS_ZONES,
    }


# ============================================================================
# VIOLATION TYPES ENDPOINT
# ============================================================================

@app.get("/violation-types")
async def get_violation_types() -> Dict[str, Any]:
    """Get known violation types for discipline analysis."""
    return {
        "engine_id": ENGINE_ID,
        "violation_types": ENGINE_STATE.discipline_searcher.get_all_violation_types(),
    }


# ============================================================================
# ROOT ENDPOINT
# ============================================================================

@app.get("/")
async def root() -> Dict[str, Any]:
    """Root endpoint with engine info."""
    return {
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "version": ENGINE_VERSION,
        "mode": ENGINE_MODE,
        "port": ENGINE_PORT,
        "authority": ENGINE_AUTHORITY,
        "tier": "LEGAL",
        "tie_version": "20.0",
        "domain": ENGINE_DOMAIN,
        "status": "operational",
        "endpoints": [
            "GET  /health",
            "GET  /metrics",
            "GET  /audit",
            "GET  /doctrines",
            "GET  /doctrine/{topic}",
            "GET  /coverage",
            "GET  /drift",
            "GET  /zones",
            "GET  /rules/search?keyword=...",
            "GET  /rules/{rule_number}",
            "GET  /violation-types",
            "POST /query",
            "POST /conflict-check",
            "POST /conflict-screen",
            "POST /privilege-check",
            "POST /fee-check",
            "POST /malpractice-risk",
            "POST /discipline-analysis",
        ],
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ============================================================================
# UVICORN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "engine:app",
        host="0.0.0.0",
        port=ENGINE_PORT,
        reload=False,
        log_level="info",
    )
