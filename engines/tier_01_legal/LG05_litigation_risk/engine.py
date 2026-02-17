"""
LG05 LITIGATION RISK ENGINE - Main Engine (TIE-20 Compliant)
Production-grade litigation risk assessment engine with deterministic case merit
scoring, damages estimation, jurisdiction analysis, discovery cost modeling,
settlement valuation, and precedent matching with full audit trail.

Engine: LG05 | Tier: 1 (LEGAL) | Mode: DET | Port: 8395 | Authority: 5.0
Architecture: TIE-20 (20 mandatory components)
Version: 1.0.0
Author: ECHO OMEGA PRIME

TIE-20 Components Implemented:
    1.  three_layer_response (Quick/Standard/Deep)
    2.  response_modes (DET/EF/HYBRID)
    3.  doctrine_cache loading from doctrines.py
    4.  authority_hardening
    5.  confidence_stratification
    6.  semantic_normalization from semantic.py
    7.  vector_search_chromadb from search.py
    8.  telemetry_module from telemetry.py
    9.  doctrine_drift_watcher
    10. doctrine_coverage_map
    11. metrics_collector
    12. health_endpoint (/health)
    13. zoned_analysis
    14. fact_fragility_scoring
    15. audit_trail_jsonl
    16. determinism_hash_sha256
    17. fastapi_server (FastAPI app with routes)
    18. loguru_logging
    19. multi_doctrine_decomposition
    20. deep_analysis_mode
"""

import hashlib
import json
import math
import os
import sys
import threading
import time
import traceback
import uuid
from collections import defaultdict
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, FrozenSet, List, Optional, Set, Tuple, Union

import uvicorn
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import BaseModel, Field, field_validator

# ---------------------------------------------------------------------------
# Local imports from sibling modules
# ---------------------------------------------------------------------------

# Ensure sibling modules are importable
ENGINE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ENGINE_DIR))
from doctrines import (
    DOCTRINE_CACHE,
    DOCTRINE_INTERACTIONS,
    AuthorityLevel,
    ConfidenceLevel,
    DoctrineBlock,
    DoctrineInteraction,
    DoctrineCoverageMap,
    LitigationCategory,
    RiskSeverity,
    get_all_categories,
    get_all_doctrine_keys,
    get_coverage_map,
    get_doctrine,
    get_doctrine_count,
    get_doctrines_by_category,
    get_interaction_edges_for,
    search_doctrines_by_keyword,
)
from search import (
    InvertedIndex,
    SearchDocument,
    SearchQuery,
    SearchResult,
    SearchScope,
    SortOrder,
    compare_cases,
    get_search_index,
    trigram_similarity,
)
from semantic import (
    CANONICAL_TERMS,
    SEMANTIC_MAP,
    SEMANTIC_VERSION,
    TOTAL_MAPPINGS,
    NormalizationResult,
    compute_text_hash,
    get_all_terms_for_canonical,
    get_canonical_for_term,
    get_map_metadata,
    normalize_semantics,
)
from telemetry import (
    AuditDatabase,
    ErrorDomain,
    JSONLWriter,
    MutationOrigin,
    MutationType,
    PerformanceTelemetry,
    TelemetryManager,
    complete_trace,
    get_telemetry,
    log_error,
    record_damages_estimation,
    record_doctrine_mutation,
    record_jurisdiction_analysis,
    record_reasoning_step,
    record_risk_assessment,
    trace_query,
)

# ---------------------------------------------------------------------------
# ENGINE CONSTANTS
# ---------------------------------------------------------------------------
ENGINE_ID: str = "LG05"
ENGINE_NAME: str = "Litigation Risk Engine"
ENGINE_VERSION: str = "1.0.0"
ENGINE_PORT: int = 8395
ENGINE_HOST: str = "0.0.0.0"
AUTHORITY_LEVEL: float = 5.0
TIER: int = 1
TIER_NAME: str = "LEGAL"
MODE: str = "DET"

CONFIG_PATH: Path = Path(__file__).parent / "config.json"
AUDIT_LOG_PATH: Path = Path(__file__).parent / "telemetry" / "audit_trail.jsonl"

BANNED_PHRASES: FrozenSet[str] = frozenset({
    "you will definitely win",
    "there is no litigation risk",
    "this case is guaranteed to settle",
    "no jury would ever find liability",
    "damages are capped at zero",
    "you cannot lose this case",
    "the statute of limitations has definitely expired",
    "this claim is frivolous",
})

RISK_DIMENSION_WEIGHTS: Dict[str, float] = {
    "case_merit": 0.25,
    "damages_exposure": 0.20,
    "jurisdiction_risk": 0.15,
    "discovery_cost": 0.15,
    "settlement_pressure": 0.15,
    "regulatory_escalation": 0.10,
}

CONFIDENCE_THRESHOLDS: Dict[str, float] = {
    "well_settled": 0.90,
    "generally_accepted": 0.75,
    "jurisdiction_dependent": 0.60,
    "evolving_law": 0.45,
    "high_risk": 0.30,
}

RESPONSE_MODE_MAP: Dict[str, str] = {
    "DET": "deterministic",
    "EF": "empirical_flexible",
    "HYBRID": "hybrid",
}

# ---------------------------------------------------------------------------
# Loguru configuration
# ---------------------------------------------------------------------------
LOG_DIR: Path = Path(__file__).parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logger.add(
    LOG_DIR / "lg05_engine_{time}.log",
    rotation="50 MB",
    retention="60 days",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level:<8} | {module}:{function}:{line} | {message}",
    serialize=True,
    enqueue=True,
)


# ============================================================================
# CONFIGURATION LOADER
# ============================================================================

def load_engine_config() -> Dict[str, Any]:
    """Load engine configuration from config.json."""
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as fh:
            config = json.load(fh)
        logger.info(f"Config loaded from {CONFIG_PATH} | keys={len(config)}")
        return config
    logger.warning(f"Config not found at {CONFIG_PATH}, using defaults")
    return {
        "engine_id": ENGINE_ID,
        "port": ENGINE_PORT,
        "mode": MODE,
        "authority_level": AUTHORITY_LEVEL,
    }


ENGINE_CONFIG: Dict[str, Any] = load_engine_config()


# ============================================================================
# PYDANTIC REQUEST / RESPONSE MODELS
# ============================================================================

class ResponseModeEnum(str, Enum):
    """Supported response modes."""
    DET = "DET"
    EF = "EF"
    HYBRID = "HYBRID"


class AnalysisDepthEnum(str, Enum):
    """Three-layer analysis depth."""
    QUICK = "QUICK"
    STANDARD = "STANDARD"
    DEEP = "DEEP"


class RiskLevelEnum(str, Enum):
    """Risk severity levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NEGLIGIBLE = "negligible"


class LitigationTypeEnum(str, Enum):
    """Supported litigation types."""
    BREACH_OF_CONTRACT = "breach_of_contract"
    NEGLIGENCE = "negligence"
    STRICT_LIABILITY = "strict_liability"
    INTENTIONAL_TORT = "intentional_tort"
    WRONGFUL_TERMINATION = "wrongful_termination"
    EMPLOYMENT_DISCRIMINATION = "employment_discrimination"
    FLSA_WAGE_HOUR = "flsa_wage_hour"
    SECURITIES_FRAUD_10B5 = "securities_fraud_10b5"
    CLASS_ACTION = "class_action"
    DERIVATIVE_ACTION = "derivative_action"
    ANTITRUST_SHERMAN = "antitrust_sherman"
    ANTITRUST_CLAYTON = "antitrust_clayton"
    PATENT_INFRINGEMENT = "patent_infringement"
    TRADE_SECRET = "trade_secret_misappropriation"
    TRADEMARK_INFRINGEMENT = "trademark_infringement"
    COPYRIGHT_INFRINGEMENT = "copyright_infringement"
    ENVIRONMENTAL_CERCLA = "environmental_cercla"
    TOXIC_TORT = "toxic_tort"
    PRODUCTS_LIABILITY = "products_liability"
    MEDICAL_MALPRACTICE = "medical_malpractice"
    INSURANCE_COVERAGE = "insurance_coverage"
    INSURANCE_BAD_FAITH = "insurance_bad_faith"
    REAL_ESTATE_DISPUTE = "real_estate_dispute"
    CONSTRUCTION_DEFECT = "construction_defect"
    QUI_TAM_WHISTLEBLOWER = "qui_tam_whistleblower"
    REGULATORY_ENFORCEMENT = "regulatory_enforcement"
    ADMINISTRATIVE_ACTION = "administrative_action"
    ARBITRATION = "arbitration"
    COMMERCIAL_FRAUD = "commercial_fraud"
    PARTNERSHIP_DISPUTE = "partnership_dispute"


class ClaimFact(BaseModel):
    """A single factual assertion relevant to a claim."""
    description: str = Field(..., min_length=1, max_length=5000)
    source: str = Field(default="client_provided")
    verified: bool = Field(default=False)
    strength: float = Field(default=0.5, ge=0.0, le=1.0)
    fragility_score: Optional[float] = Field(default=None, ge=0.0, le=1.0)


class ClaimDetail(BaseModel):
    """Details for a single claim within a case."""
    claim_type: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1, max_length=10000)
    facts: List[ClaimFact] = Field(default_factory=list)
    statute_reference: Optional[str] = None
    damages_estimate_low: Optional[float] = Field(default=None, ge=0.0)
    damages_estimate_high: Optional[float] = Field(default=None, ge=0.0)


class PartyInfo(BaseModel):
    """Information about a party to the litigation."""
    name: str = Field(..., min_length=1, max_length=500)
    role: str = Field(default="defendant")
    entity_type: str = Field(default="individual")
    jurisdiction_state: Optional[str] = None
    resources_level: str = Field(default="moderate")


class LitigationRiskRequest(BaseModel):
    """Full litigation risk assessment request."""
    case_description: str = Field(..., min_length=10, max_length=50000)
    litigation_type: str = Field(default="breach_of_contract")
    jurisdiction: str = Field(default="federal")
    claims: List[ClaimDetail] = Field(default_factory=list)
    parties: List[PartyInfo] = Field(default_factory=list)
    facts: List[ClaimFact] = Field(default_factory=list)
    amount_in_controversy: Optional[float] = Field(default=None, ge=0.0)
    response_mode: ResponseModeEnum = Field(default=ResponseModeEnum.DET)
    analysis_depth: AnalysisDepthEnum = Field(default=AnalysisDepthEnum.STANDARD)
    include_citations: bool = Field(default=True)
    include_settlement_analysis: bool = Field(default=True)
    include_discovery_cost: bool = Field(default=True)
    include_damages_estimate: bool = Field(default=True)
    include_jurisdiction_analysis: bool = Field(default=True)
    session_id: Optional[str] = None

    @field_validator("case_description")
    @classmethod
    def validate_case_description(cls, v: str) -> str:
        """Ensure case description is substantive."""
        if len(v.split()) < 5:
            raise ValueError("Case description must contain at least 5 words")
        return v


class QuickTriageRequest(BaseModel):
    """Lightweight triage request for fast risk screening."""
    case_summary: str = Field(..., min_length=10, max_length=5000)
    litigation_type: str = Field(default="breach_of_contract")
    jurisdiction: str = Field(default="federal")


class DamagesEstimationRequest(BaseModel):
    """Request for standalone damages estimation."""
    litigation_type: str = Field(default="breach_of_contract")
    claims: List[ClaimDetail] = Field(default_factory=list)
    amount_in_controversy: Optional[float] = Field(default=None, ge=0.0)
    jurisdiction: str = Field(default="federal")
    punitive_likely: bool = Field(default=False)
    attorneys_fees_recoverable: bool = Field(default=False)
    class_action: bool = Field(default=False)
    class_size: Optional[int] = Field(default=None, ge=1)


class SettlementAnalysisRequest(BaseModel):
    """Request for standalone settlement valuation."""
    litigation_type: str = Field(default="breach_of_contract")
    liability_probability: float = Field(default=0.5, ge=0.0, le=1.0)
    damages_low: float = Field(default=0.0, ge=0.0)
    damages_high: float = Field(default=0.0, ge=0.0)
    litigation_cost_estimate: float = Field(default=50000.0, ge=0.0)
    time_to_trial_months: int = Field(default=18, ge=1, le=120)
    publicity_risk: float = Field(default=0.3, ge=0.0, le=1.0)
    business_disruption: float = Field(default=0.3, ge=0.0, le=1.0)
    precedent_value: float = Field(default=0.2, ge=0.0, le=1.0)


class DiscoveryCostRequest(BaseModel):
    """Request for standalone discovery cost modeling."""
    document_volume_estimate: int = Field(default=10000, ge=0)
    custodian_count: int = Field(default=5, ge=1)
    deposition_count: int = Field(default=10, ge=0)
    expert_witness_count: int = Field(default=2, ge=0)
    e_discovery_needed: bool = Field(default=True)
    international_discovery: bool = Field(default=False)
    privilege_review_complexity: str = Field(default="moderate")


class JurisdictionAnalysisRequest(BaseModel):
    """Request for standalone jurisdiction analysis."""
    jurisdiction: str = Field(..., min_length=1)
    litigation_type: str = Field(default="breach_of_contract")
    defendant_state: Optional[str] = None
    plaintiff_state: Optional[str] = None
    forum_selection_clause: bool = Field(default=False)
    amount_in_controversy: Optional[float] = Field(default=None, ge=0.0)


class DoctrineSearchRequest(BaseModel):
    """Request for doctrine search."""
    query: str = Field(..., min_length=1, max_length=1000)
    category: Optional[str] = None
    max_results: int = Field(default=20, ge=1, le=100)


class CaseComparisonRequest(BaseModel):
    """Request to compare two cases."""
    case_a_description: str = Field(..., min_length=10, max_length=10000)
    case_b_description: str = Field(..., min_length=10, max_length=10000)
    litigation_type: Optional[str] = None


class StatuteOfLimitationsRequest(BaseModel):
    """Request for statute of limitations analysis."""
    litigation_type: str = Field(default="breach_of_contract")
    jurisdiction: str = Field(default="federal")
    date_of_injury: Optional[str] = None
    date_of_discovery: Optional[str] = None
    tolling_events: List[str] = Field(default_factory=list)


# --- Response Models ---

class PrecedentCitation(BaseModel):
    """A controlling precedent citation."""
    case_name: str
    citation: str
    year: int
    court: str
    holding: str
    relevance_score: float


class RiskDimensionScore(BaseModel):
    """Score for a single risk dimension."""
    dimension: str
    score: float = Field(ge=0.0, le=1.0)
    weight: float
    weighted_score: float
    factors_evaluated: List[str]
    key_finding: str


class DamagesRange(BaseModel):
    """Damages range estimate."""
    category: str
    low: float
    high: float
    methodology: str
    confidence: float


class SettlementValuation(BaseModel):
    """Settlement valuation output."""
    expected_value: float
    settlement_range_low: float
    settlement_range_high: float
    zopa_exists: bool
    zopa_low: Optional[float]
    zopa_high: Optional[float]
    recommendation: str
    factors: Dict[str, float]


class DiscoveryCostEstimate(BaseModel):
    """Discovery cost estimate output."""
    document_review_cost: float
    deposition_cost: float
    expert_witness_cost: float
    e_discovery_cost: float
    miscellaneous_cost: float
    total_estimate: float
    cost_per_document: float
    proportionality_warning: Optional[str]


class JurisdictionAssessment(BaseModel):
    """Jurisdiction analysis output."""
    jurisdiction: str
    venue_favorability: float
    personal_jurisdiction_risk: float
    subject_matter_jurisdiction: str
    jury_tendency: str
    local_rules_impact: str
    overall_favorability: float
    recommended_venue: Optional[str]
    notes: List[str]


class EpistemicDisclosure(BaseModel):
    """Required epistemic disclosure."""
    jurisdiction_variance: str
    not_legal_advice: str
    temporal_caveat: str
    fact_dependency: str


class FactFragilityResult(BaseModel):
    """Result of fact fragility scoring."""
    fact_index: int
    description: str
    fragility_score: float
    fragility_label: str
    vulnerability_factors: List[str]
    mitigation_suggestions: List[str]


class LitigationRiskResponse(BaseModel):
    """Full litigation risk assessment response."""
    engine_id: str = ENGINE_ID
    engine_version: str = ENGINE_VERSION
    trace_id: str
    timestamp: str
    response_mode: str
    analysis_depth: str
    response_layer: str
    litigation_type: str
    jurisdiction: str
    composite_risk_score: float
    risk_level: str
    confidence: float
    risk_dimensions: List[RiskDimensionScore]
    matched_doctrines: List[str]
    precedent_citations: List[PrecedentCitation]
    analysis_summary: str
    key_risk_factors: List[str]
    recommended_actions: List[str]
    damages_estimate: Optional[List[DamagesRange]] = None
    settlement_analysis: Optional[SettlementValuation] = None
    discovery_cost: Optional[DiscoveryCostEstimate] = None
    jurisdiction_analysis: Optional[JurisdictionAssessment] = None
    fact_fragility: Optional[List[FactFragilityResult]] = None
    epistemic_disclosures: EpistemicDisclosure
    determinism_hash: str
    latency_ms: float
    warnings: List[str] = Field(default_factory=list)


class QuickTriageResponse(BaseModel):
    """Quick triage response."""
    engine_id: str = ENGINE_ID
    trace_id: str
    timestamp: str
    litigation_type: str
    risk_level: str
    risk_score: float
    confidence: float
    top_risks: List[str]
    recommended_depth: str
    determinism_hash: str
    latency_ms: float


class HealthResponse(BaseModel):
    """Health endpoint response."""
    engine_id: str
    engine_name: str
    version: str
    status: str
    port: int
    mode: str
    tier: int
    tier_name: str
    authority_level: float
    uptime_seconds: float
    doctrine_count: int
    semantic_mappings: int
    search_index_docs: int
    telemetry_session: str
    telemetry_events: int
    performance: Dict[str, Any]
    timestamp: str


# ============================================================================
# (3) DOCTRINE CACHE LOADING
# ============================================================================

class DoctrineCacheManager:
    """Manages the doctrine cache with integrity verification and drift detection."""

    def __init__(self) -> None:
        self._cache: Dict[str, DoctrineBlock] = dict(DOCTRINE_CACHE)
        self._load_time: float = time.time()
        self._access_counts: Dict[str, int] = defaultdict(int)
        self._miss_log: List[str] = []
        self._integrity_hash: str = self._compute_integrity_hash()
        self._coverage_map: DoctrineCoverageMap = get_coverage_map()
        logger.info(
            f"DoctrineCacheManager initialized | doctrines={len(self._cache)} | "
            f"integrity={self._integrity_hash[:16]}"
        )

    def _compute_integrity_hash(self) -> str:
        """Compute SHA-256 integrity hash over all doctrine keys and topics."""
        content_parts: List[str] = []
        for key in sorted(self._cache.keys()):
            block = self._cache[key]
            content_parts.append(f"{key}:{block.topic}:{block.category.value}:{block.risk_severity.value}")
        combined = "|".join(content_parts)
        return hashlib.sha256(combined.encode("utf-8")).hexdigest()

    def get(self, key: str) -> Optional[DoctrineBlock]:
        """Retrieve a doctrine block by key."""
        block = self._cache.get(key)
        if block:
            self._access_counts[key] += 1
        else:
            self._miss_log.append(key)
            if len(self._miss_log) > 500:
                self._miss_log = self._miss_log[-250:]
        return block

    def search_by_keyword(self, keyword: str) -> List[DoctrineBlock]:
        """Search doctrines by keyword."""
        return search_doctrines_by_keyword(keyword)

    def search_by_category(self, category: LitigationCategory) -> List[DoctrineBlock]:
        """Get all doctrines for a category."""
        return get_doctrines_by_category(category)

    def get_interactions(self, key: str) -> List[DoctrineInteraction]:
        """Get all interaction edges for a doctrine."""
        return get_interaction_edges_for(key)

    def get_all_keys(self) -> List[str]:
        """Get all doctrine keys."""
        return sorted(self._cache.keys())

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return {
            "total_doctrines": len(self._cache),
            "total_accesses": sum(self._access_counts.values()),
            "unique_accessed": len(self._access_counts),
            "top_accessed": sorted(
                self._access_counts.items(), key=lambda x: x[1], reverse=True
            )[:10],
            "miss_count": len(self._miss_log),
            "recent_misses": self._miss_log[-10:],
            "integrity_hash": self._integrity_hash[:16],
            "load_time": self._load_time,
            "categories": self._coverage_map.get_coverage_stats(),
            "uncovered_categories": self._coverage_map.get_uncovered_categories(),
        }

    def verify_integrity(self) -> bool:
        """Verify cache integrity has not drifted."""
        current_hash = self._compute_integrity_hash()
        intact = current_hash == self._integrity_hash
        if not intact:
            logger.warning(
                f"Doctrine cache integrity drift detected | "
                f"expected={self._integrity_hash[:16]} | current={current_hash[:16]}"
            )
        return intact

    @property
    def coverage_map(self) -> DoctrineCoverageMap:
        """Get the doctrine coverage map."""
        return self._coverage_map

    @property
    def integrity_hash(self) -> str:
        """Current integrity hash."""
        return self._integrity_hash


# ============================================================================
# (4) AUTHORITY HARDENING
# ============================================================================

class AuthorityHardener:
    """Enforces authority hierarchy on risk assessments and recommendations."""

    AUTHORITY_WEIGHTS: Dict[str, float] = {
        "statute": 1.0,
        "regulation": 0.85,
        "case_law": 0.70,
        "restatement": 0.60,
        "treatise": 0.40,
        "practice_guide": 0.25,
    }

    MINIMUM_AUTHORITY_FOR_DEFINITIVE: float = 0.70
    MINIMUM_AUTHORITY_FOR_ADVISORY: float = 0.40

    def __init__(self) -> None:
        self._hardening_log: List[Dict[str, Any]] = []
        logger.info("AuthorityHardener initialized")

    def compute_authority_weight(self, doctrine: DoctrineBlock) -> float:
        """Compute the authority weight for a doctrine block."""
        base_weight = self.AUTHORITY_WEIGHTS.get(doctrine.authority.value, 0.2)
        confidence_modifier = CONFIDENCE_THRESHOLDS.get(doctrine.confidence.value, 0.5)
        combined = base_weight * 0.6 + confidence_modifier * 0.4
        return round(min(1.0, combined), 4)

    def harden_response(
        self,
        doctrines_used: List[DoctrineBlock],
        raw_risk_score: float,
        raw_confidence: float,
    ) -> Tuple[float, float, str, List[str]]:
        """Apply authority hardening to raw risk scores.

        Returns:
            Tuple of (hardened_risk_score, hardened_confidence, authority_tier, warnings)
        """
        if not doctrines_used:
            return raw_risk_score, max(raw_confidence * 0.5, 0.1), "unsubstantiated", [
                "No authoritative doctrines matched. Assessment based on general principles only."
            ]

        authority_weights: List[float] = []
        for doctrine in doctrines_used:
            authority_weights.append(self.compute_authority_weight(doctrine))

        max_authority = max(authority_weights)
        avg_authority = sum(authority_weights) / len(authority_weights)
        weighted_authority = max_authority * 0.6 + avg_authority * 0.4

        warnings: List[str] = []

        if weighted_authority >= self.MINIMUM_AUTHORITY_FOR_DEFINITIVE:
            authority_tier = "definitive"
            confidence_modifier = 1.0
        elif weighted_authority >= self.MINIMUM_AUTHORITY_FOR_ADVISORY:
            authority_tier = "advisory"
            confidence_modifier = 0.80
            warnings.append(
                "Assessment based primarily on case law and practice guidance. "
                "Statutory analysis may yield different conclusions."
            )
        else:
            authority_tier = "preliminary"
            confidence_modifier = 0.55
            warnings.append(
                "Assessment based on limited authority sources. "
                "Further research with primary sources is strongly recommended."
            )

        hardened_confidence = round(min(1.0, raw_confidence * confidence_modifier), 4)

        risk_stability = 1.0 - (0.3 * (1.0 - weighted_authority))
        hardened_risk = round(raw_risk_score * risk_stability, 4)

        jurisdiction_dependent = any(
            d.confidence == ConfidenceLevel.JURISDICTION_DEPENDENT for d in doctrines_used
        )
        if jurisdiction_dependent:
            warnings.append(
                "One or more applicable doctrines are jurisdiction-dependent. "
                "Results may vary significantly by state."
            )
            hardened_confidence = round(hardened_confidence * 0.90, 4)

        evolving_law = any(
            d.confidence == ConfidenceLevel.EVOLVING_LAW for d in doctrines_used
        )
        if evolving_law:
            warnings.append(
                "Evolving area of law detected. Recent developments may not be "
                "fully reflected in this assessment."
            )
            hardened_confidence = round(hardened_confidence * 0.85, 4)

        self._hardening_log.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "doctrines_count": len(doctrines_used),
            "max_authority": max_authority,
            "avg_authority": avg_authority,
            "weighted_authority": weighted_authority,
            "authority_tier": authority_tier,
            "raw_risk": raw_risk_score,
            "hardened_risk": hardened_risk,
            "raw_confidence": raw_confidence,
            "hardened_confidence": hardened_confidence,
            "warnings_count": len(warnings),
        })

        return hardened_risk, hardened_confidence, authority_tier, warnings

    def get_hardening_stats(self) -> Dict[str, Any]:
        """Get authority hardening statistics."""
        if not self._hardening_log:
            return {"total_hardenings": 0}
        return {
            "total_hardenings": len(self._hardening_log),
            "avg_authority": round(
                sum(h["weighted_authority"] for h in self._hardening_log) / len(self._hardening_log), 3
            ),
            "tier_distribution": {
                tier: sum(1 for h in self._hardening_log if h["authority_tier"] == tier)
                for tier in ["definitive", "advisory", "preliminary", "unsubstantiated"]
            },
        }


# ============================================================================
# (5) CONFIDENCE STRATIFICATION
# ============================================================================

class ConfidenceStratifier:
    """Stratifies confidence levels across multiple dimensions."""

    def __init__(self) -> None:
        logger.info("ConfidenceStratifier initialized")

    def stratify(
        self,
        doctrines: List[DoctrineBlock],
        fact_count: int,
        fact_avg_strength: float,
        jurisdiction_specificity: float,
        temporal_relevance: float,
    ) -> Dict[str, Any]:
        """Compute stratified confidence across multiple dimensions.

        Returns a dictionary with per-dimension confidence and composite score.
        """
        doctrine_confidence = self._doctrine_dimension(doctrines)
        factual_confidence = self._factual_dimension(fact_count, fact_avg_strength)
        jurisdictional_confidence = self._jurisdictional_dimension(
            doctrines, jurisdiction_specificity
        )
        temporal_confidence = self._temporal_dimension(doctrines, temporal_relevance)

        composite = (
            doctrine_confidence * 0.35
            + factual_confidence * 0.25
            + jurisdictional_confidence * 0.20
            + temporal_confidence * 0.20
        )

        if composite >= 0.85:
            confidence_tier = "HIGH"
        elif composite >= 0.65:
            confidence_tier = "MODERATE"
        elif composite >= 0.45:
            confidence_tier = "LOW"
        else:
            confidence_tier = "VERY_LOW"

        return {
            "composite": round(composite, 4),
            "tier": confidence_tier,
            "dimensions": {
                "doctrine": round(doctrine_confidence, 4),
                "factual": round(factual_confidence, 4),
                "jurisdictional": round(jurisdictional_confidence, 4),
                "temporal": round(temporal_confidence, 4),
            },
            "weights": {
                "doctrine": 0.35,
                "factual": 0.25,
                "jurisdictional": 0.20,
                "temporal": 0.20,
            },
        }

    def _doctrine_dimension(self, doctrines: List[DoctrineBlock]) -> float:
        """Confidence from doctrine authority level."""
        if not doctrines:
            return 0.2
        scores: List[float] = []
        for d in doctrines:
            base = CONFIDENCE_THRESHOLDS.get(d.confidence.value, 0.5)
            auth_bonus = d.authority.weight / 100.0 * 0.3
            scores.append(min(1.0, base + auth_bonus))
        return sum(scores) / len(scores)

    def _factual_dimension(self, fact_count: int, avg_strength: float) -> float:
        """Confidence from factual support."""
        if fact_count == 0:
            return 0.3
        count_factor = min(1.0, fact_count / 10.0)
        return count_factor * 0.5 + avg_strength * 0.5

    def _jurisdictional_dimension(
        self, doctrines: List[DoctrineBlock], specificity: float
    ) -> float:
        """Confidence from jurisdictional specificity."""
        if not doctrines:
            return specificity * 0.5
        jd_count = sum(
            1 for d in doctrines
            if d.confidence == ConfidenceLevel.JURISDICTION_DEPENDENT
        )
        jd_ratio = jd_count / len(doctrines)
        penalty = jd_ratio * 0.3
        return max(0.1, specificity - penalty)

    def _temporal_dimension(
        self, doctrines: List[DoctrineBlock], relevance: float
    ) -> float:
        """Confidence from temporal relevance of authorities."""
        if not doctrines:
            return relevance * 0.5
        evolving_count = sum(
            1 for d in doctrines if d.confidence == ConfidenceLevel.EVOLVING_LAW
        )
        evolving_penalty = (evolving_count / len(doctrines)) * 0.25
        return max(0.1, relevance - evolving_penalty)


# ============================================================================
# (6) SEMANTIC NORMALIZATION INTEGRATION
# ============================================================================

class SemanticNormalizer:
    """Wrapper around semantic.py normalization for engine use."""

    def __init__(self) -> None:
        self._normalization_count: int = 0
        self._total_mappings_applied: int = 0
        logger.info(
            f"SemanticNormalizer initialized | mappings={TOTAL_MAPPINGS} | "
            f"version={SEMANTIC_VERSION}"
        )

    def normalize(self, text: str) -> NormalizationResult:
        """Normalize litigation text using semantic dictionary."""
        result = normalize_semantics(text)
        self._normalization_count += 1
        self._total_mappings_applied += result.mappings_applied
        return result

    def extract_key_terms(self, text: str) -> List[str]:
        """Extract canonical litigation terms from text."""
        normalized = self.normalize(text)
        found_terms: List[str] = []
        for canonical in CANONICAL_TERMS:
            if canonical in normalized.normalized:
                found_terms.append(canonical)
        return sorted(set(found_terms))

    def compute_hash(self, text: str) -> str:
        """Compute deterministic hash of normalized text."""
        normalized = self.normalize(text)
        return normalized.text_hash

    def get_stats(self) -> Dict[str, Any]:
        """Get normalization statistics."""
        return {
            "total_normalizations": self._normalization_count,
            "total_mappings_applied": self._total_mappings_applied,
            "avg_mappings_per_query": (
                round(self._total_mappings_applied / max(self._normalization_count, 1), 2)
            ),
            "semantic_version": SEMANTIC_VERSION,
            "total_mappings_available": TOTAL_MAPPINGS,
            "map_metadata": get_map_metadata(),
        }


# ============================================================================
# (7) VECTOR SEARCH INTEGRATION
# ============================================================================

class SearchEngine:
    """Wrapper around search.py for engine-level search operations."""

    def __init__(self) -> None:
        self._index: InvertedIndex = get_search_index()
        self._search_count: int = 0
        logger.info(
            f"SearchEngine initialized | docs={self._index.document_count} | "
            f"terms={self._index.term_count}"
        )

    def search(
        self,
        query_text: str,
        litigation_type: Optional[str] = None,
        jurisdiction: Optional[str] = None,
        risk_level: Optional[str] = None,
        max_results: int = 20,
        scope: SearchScope = SearchScope.ALL,
    ) -> List[SearchResult]:
        """Execute a search against the index."""
        sq = SearchQuery(
            text=query_text,
            scope=scope,
            litigation_type=litigation_type,
            jurisdiction=jurisdiction,
            risk_level=risk_level,
            max_results=max_results,
        )
        results = self._index.search(sq)
        self._search_count += 1
        return results

    def search_doctrines(self, query_text: str, max_results: int = 10) -> List[SearchResult]:
        """Search only doctrine documents."""
        return self.search(query_text, max_results=max_results, scope=SearchScope.DOCTRINES)

    def search_cases(self, query_text: str, max_results: int = 10) -> List[SearchResult]:
        """Search only case law documents."""
        return self.search(query_text, max_results=max_results, scope=SearchScope.CASES)

    def add_document(self, doc: SearchDocument) -> None:
        """Add a document to the search index."""
        self._index.add_document(doc)

    def compare(self, doc_a_id: str, doc_b_id: str):
        """Compare two indexed documents."""
        return compare_cases(self._index, doc_a_id, doc_b_id)

    def get_stats(self) -> Dict[str, Any]:
        """Get search engine statistics."""
        return {
            "total_searches": self._search_count,
            "index_stats": self._index.get_stats(),
        }


# ============================================================================
# (8) TELEMETRY MODULE INTEGRATION
# ============================================================================

class EngineTelemeter:
    """Engine-level telemetry integration."""

    def __init__(self) -> None:
        self._tm: TelemetryManager = get_telemetry()
        self._audit_writer: JSONLWriter = JSONLWriter(AUDIT_LOG_PATH)
        logger.info(f"EngineTelemeter initialized | session={self._tm.session_id}")

    def start_trace(
        self, query_text: str, litigation_type: str, jurisdiction: str, mode: str
    ) -> Tuple[str, float]:
        """Start a query trace."""
        return trace_query(query_text, litigation_type, jurisdiction, mode, AUTHORITY_LEVEL)

    def end_trace(
        self,
        trace_id: str,
        start_time: float,
        query_text: str,
        litigation_type: str,
        jurisdiction: str,
        mode: str,
        layer: str,
        doctrine_keys: List[str],
        risk_score: float,
        confidence: float,
        determinism_hash: str,
        error: Optional[str] = None,
        warnings: Optional[List[str]] = None,
    ) -> None:
        """Complete a query trace."""
        complete_trace(
            trace_id=trace_id,
            start_time=start_time,
            query_text=query_text,
            litigation_type=litigation_type,
            jurisdiction=jurisdiction,
            response_mode=mode,
            response_layer=layer,
            doctrine_keys=doctrine_keys,
            risk_score=risk_score,
            confidence=confidence,
            determinism_hash=determinism_hash,
            authority_level=AUTHORITY_LEVEL,
            error=error,
            warnings=warnings,
        )

    def log_audit_event(self, event_type: str, data: Dict[str, Any]) -> None:
        """Write an event to the audit trail."""
        record = {
            "event_type": event_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "session_id": self._tm.session_id,
            "engine_id": ENGINE_ID,
            "data": data,
        }
        self._audit_writer.write(record)

    def log_reasoning_step(
        self,
        trace_id: str,
        step_number: int,
        step_name: str,
        input_state: Dict[str, Any],
        output_state: Dict[str, Any],
        duration_ms: float,
        doctrine_applied: Optional[str] = None,
        confidence_delta: float = 0.0,
    ) -> None:
        """Record a reasoning step."""
        record_reasoning_step(
            trace_id=trace_id,
            step_number=step_number,
            step_name=step_name,
            input_state=input_state,
            output_state=output_state,
            duration_ms=duration_ms,
            doctrine_applied=doctrine_applied,
            confidence_delta=confidence_delta,
        )

    def log_error(
        self, domain: ErrorDomain, message: str,
        trace_id: Optional[str] = None, exc: Optional[Exception] = None,
    ) -> str:
        """Log an error."""
        return log_error(domain=domain, message=message, trace_id=trace_id, exc=exc)

    def get_performance(self) -> Dict[str, Any]:
        """Get performance metrics."""
        return self._tm.performance.get_full_report()

    @property
    def session_id(self) -> str:
        """Current telemetry session ID."""
        return self._tm.session_id

    @property
    def uptime(self) -> float:
        """Seconds since telemetry init."""
        return self._tm.uptime_seconds

    @property
    def event_count(self) -> int:
        """Total audit events."""
        return self._tm.audit_db.count_events()


# ============================================================================
# (9) DOCTRINE DRIFT WATCHER
# ============================================================================

class DoctrineDriftWatcher:
    """Monitors doctrine cache for integrity drift and staleness."""

    def __init__(self, cache_manager: DoctrineCacheManager) -> None:
        self._cache = cache_manager
        self._baseline_hash: str = cache_manager.integrity_hash
        self._check_count: int = 0
        self._drift_events: List[Dict[str, Any]] = []
        self._last_check: float = time.time()
        logger.info(f"DoctrineDriftWatcher initialized | baseline={self._baseline_hash[:16]}")

    def check_drift(self) -> Dict[str, Any]:
        """Run a drift check against baseline."""
        self._check_count += 1
        self._last_check = time.time()
        current_intact = self._cache.verify_integrity()

        result: Dict[str, Any] = {
            "check_number": self._check_count,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "baseline_hash": self._baseline_hash[:16],
            "current_hash": self._cache.integrity_hash[:16],
            "integrity_intact": current_intact,
            "drift_detected": not current_intact,
        }

        if not current_intact:
            drift_event = {
                "event": "doctrine_drift_detected",
                "check_number": self._check_count,
                "timestamp": result["timestamp"],
                "baseline": self._baseline_hash[:16],
                "current": self._cache.integrity_hash[:16],
            }
            self._drift_events.append(drift_event)
            logger.warning(f"Doctrine drift detected at check #{self._check_count}")
            record_doctrine_mutation(
                doctrine_key="__ALL__",
                mutation_type=MutationType.MODIFY,
                origin=MutationOrigin.DRIFT_CORRECTION,
                before_hash=self._baseline_hash[:16],
                after_hash=self._cache.integrity_hash[:16],
                justification="Drift detected by DoctrineDriftWatcher",
            )

        return result

    def get_coverage_gaps(self) -> Dict[str, Any]:
        """Identify coverage gaps in doctrine library."""
        cov = self._cache.coverage_map
        stats = cov.get_coverage_stats()
        uncovered = cov.get_uncovered_categories()
        return {
            "stats": stats,
            "uncovered_categories": uncovered,
            "gap_severity": "critical" if len(uncovered) > 3 else (
                "moderate" if len(uncovered) > 1 else "acceptable"
            ),
        }

    def get_staleness_report(self) -> Dict[str, Any]:
        """Report on doctrine staleness based on precedent dates."""
        stale_doctrines: List[str] = []
        current_year = datetime.now(timezone.utc).year
        for key in self._cache.get_all_keys():
            block = self._cache.get(key)
            if block and block.precedents:
                newest = max(p.year for p in block.precedents)
                if current_year - newest > 10:
                    stale_doctrines.append(key)
        return {
            "total_doctrines": len(self._cache.get_all_keys()),
            "stale_count": len(stale_doctrines),
            "stale_keys": stale_doctrines,
            "stale_threshold_years": 10,
        }

    def get_drift_history(self) -> List[Dict[str, Any]]:
        """Get all recorded drift events."""
        return list(self._drift_events)

    def get_stats(self) -> Dict[str, Any]:
        """Get watcher statistics."""
        return {
            "check_count": self._check_count,
            "drift_events": len(self._drift_events),
            "last_check": self._last_check,
            "baseline_hash": self._baseline_hash[:16],
        }


# ============================================================================
# (10) DOCTRINE COVERAGE MAP - integrated via DoctrineCacheManager
# (11) METRICS COLLECTOR
# ============================================================================

class MetricsCollector:
    """Collects and aggregates engine metrics across all components."""

    def __init__(self) -> None:
        self._counters: Dict[str, int] = defaultdict(int)
        self._gauges: Dict[str, float] = {}
        self._histograms: Dict[str, List[float]] = defaultdict(list)
        self._lock = threading.Lock()
        self._start_time: float = time.time()
        logger.info("MetricsCollector initialized")

    def increment(self, name: str, value: int = 1) -> None:
        """Increment a counter metric."""
        with self._lock:
            self._counters[name] += value

    def set_gauge(self, name: str, value: float) -> None:
        """Set a gauge metric to a specific value."""
        with self._lock:
            self._gauges[name] = value

    def observe(self, name: str, value: float) -> None:
        """Add an observation to a histogram metric."""
        with self._lock:
            self._histograms[name].append(value)
            if len(self._histograms[name]) > 1000:
                self._histograms[name] = self._histograms[name][-500:]

    def get_counter(self, name: str) -> int:
        """Get a counter value."""
        return self._counters.get(name, 0)

    def get_gauge(self, name: str) -> float:
        """Get a gauge value."""
        return self._gauges.get(name, 0.0)

    def get_histogram_stats(self, name: str) -> Dict[str, float]:
        """Get histogram statistics."""
        with self._lock:
            values = self._histograms.get(name, [])
            if not values:
                return {"count": 0, "avg": 0.0, "min": 0.0, "max": 0.0, "p50": 0.0, "p95": 0.0}
            s = sorted(values)
            n = len(s)
            return {
                "count": n,
                "avg": round(sum(s) / n, 3),
                "min": round(s[0], 3),
                "max": round(s[-1], 3),
                "p50": round(s[n // 2], 3),
                "p95": round(s[min(int(n * 0.95), n - 1)], 3),
            }

    def get_all_metrics(self) -> Dict[str, Any]:
        """Get all collected metrics."""
        with self._lock:
            histogram_stats = {
                name: self.get_histogram_stats(name)
                for name in self._histograms
            }
        return {
            "counters": dict(self._counters),
            "gauges": dict(self._gauges),
            "histograms": histogram_stats,
            "uptime_seconds": round(time.time() - self._start_time, 1),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


# ============================================================================
# (13) ZONED ANALYSIS
# ============================================================================

class ZonedAnalyzer:
    """Performs zoned risk analysis across geographic and legal zones."""

    ZONE_PROFILES: Dict[str, Dict[str, Any]] = {
        "federal": {
            "jury_tendency": 0.50,
            "damages_tendency": "moderate",
            "class_action_friendly": True,
            "discovery_scope": "broad",
            "median_disposition_months": 24,
        },
        "california": {
            "jury_tendency": 0.65,
            "damages_tendency": "plaintiff_favorable",
            "class_action_friendly": True,
            "discovery_scope": "very_broad",
            "median_disposition_months": 30,
            "special_rules": ["PAGA", "UCL", "Prop_65"],
        },
        "texas": {
            "jury_tendency": 0.45,
            "damages_tendency": "moderate",
            "class_action_friendly": False,
            "discovery_scope": "moderate",
            "median_disposition_months": 18,
            "special_rules": ["TCPA", "DTPA", "loser_pays_partial"],
        },
        "new_york": {
            "jury_tendency": 0.55,
            "damages_tendency": "moderate_to_high",
            "class_action_friendly": True,
            "discovery_scope": "broad",
            "median_disposition_months": 36,
            "special_rules": ["CPLR_3211", "commercial_division"],
        },
        "delaware": {
            "jury_tendency": 0.40,
            "damages_tendency": "moderate",
            "class_action_friendly": True,
            "discovery_scope": "moderate",
            "median_disposition_months": 15,
            "special_rules": ["chancery_court", "corporate_expertise"],
        },
        "florida": {
            "jury_tendency": 0.55,
            "damages_tendency": "moderate_to_high",
            "class_action_friendly": False,
            "discovery_scope": "broad",
            "median_disposition_months": 22,
            "special_rules": ["tort_reform_2023", "bad_faith_statute"],
        },
        "illinois": {
            "jury_tendency": 0.60,
            "damages_tendency": "plaintiff_favorable",
            "class_action_friendly": True,
            "discovery_scope": "broad",
            "median_disposition_months": 28,
            "special_rules": ["BIPA", "wage_act"],
        },
    }

    DEFAULT_PROFILE: Dict[str, Any] = {
        "jury_tendency": 0.50,
        "damages_tendency": "moderate",
        "class_action_friendly": False,
        "discovery_scope": "moderate",
        "median_disposition_months": 20,
    }

    def __init__(self) -> None:
        logger.info(f"ZonedAnalyzer initialized | zones={len(self.ZONE_PROFILES)}")

    def analyze_zone(self, jurisdiction: str, litigation_type: str) -> Dict[str, Any]:
        """Analyze risk factors for a specific jurisdiction zone."""
        key = jurisdiction.lower().replace(" ", "_")
        profile = self.ZONE_PROFILES.get(key, self.DEFAULT_PROFILE)

        jury_risk = profile["jury_tendency"]
        class_action_risk = 0.7 if profile.get("class_action_friendly") else 0.3
        discovery_factor = {
            "very_broad": 0.9, "broad": 0.7, "moderate": 0.5, "narrow": 0.3,
        }.get(profile.get("discovery_scope", "moderate"), 0.5)

        disposition_months = profile.get("median_disposition_months", 20)
        time_cost_factor = min(1.0, disposition_months / 36.0)

        special_rules = profile.get("special_rules", [])
        special_risk_boost = len(special_rules) * 0.05

        zone_risk_score = (
            jury_risk * 0.30
            + class_action_risk * 0.15
            + discovery_factor * 0.20
            + time_cost_factor * 0.20
            + min(0.3, special_risk_boost) * 0.15
        )

        return {
            "jurisdiction": jurisdiction,
            "zone_profile": profile,
            "zone_risk_score": round(zone_risk_score, 4),
            "jury_risk": round(jury_risk, 4),
            "class_action_risk": round(class_action_risk, 4),
            "discovery_factor": round(discovery_factor, 4),
            "time_cost_factor": round(time_cost_factor, 4),
            "special_rules": special_rules,
            "disposition_months": disposition_months,
        }

    def compare_zones(self, zone_a: str, zone_b: str, litigation_type: str) -> Dict[str, Any]:
        """Compare two jurisdictional zones for litigation risk."""
        analysis_a = self.analyze_zone(zone_a, litigation_type)
        analysis_b = self.analyze_zone(zone_b, litigation_type)

        delta = analysis_a["zone_risk_score"] - analysis_b["zone_risk_score"]
        if abs(delta) < 0.05:
            recommendation = "Zones present comparable risk profiles"
        elif delta > 0:
            recommendation = f"{zone_a} presents higher risk ({delta:+.3f}); consider {zone_b} if venue flexibility exists"
        else:
            recommendation = f"{zone_b} presents higher risk ({-delta:+.3f}); consider {zone_a} if venue flexibility exists"

        return {
            "zone_a": analysis_a,
            "zone_b": analysis_b,
            "risk_delta": round(delta, 4),
            "recommendation": recommendation,
        }


# ============================================================================
# (14) FACT FRAGILITY SCORING
# ============================================================================

class FactFragilityScorer:
    """Scores the fragility of factual assertions in a litigation context."""

    VULNERABILITY_FACTORS: Dict[str, float] = {
        "unverified": 0.30,
        "single_source": 0.20,
        "oral_only": 0.25,
        "contradicted": 0.40,
        "time_dependent": 0.15,
        "expert_dependent": 0.20,
        "circumstantial": 0.15,
        "hearsay_risk": 0.25,
        "privilege_risk": 0.10,
        "spoliation_risk": 0.20,
    }

    def __init__(self) -> None:
        logger.info("FactFragilityScorer initialized")

    def score_fact(self, fact: ClaimFact) -> FactFragilityResult:
        """Score the fragility of a single fact."""
        vulnerabilities: List[str] = []
        mitigations: List[str] = []
        fragility = 0.0

        if not fact.verified:
            fragility += self.VULNERABILITY_FACTORS["unverified"]
            vulnerabilities.append("Fact has not been independently verified")
            mitigations.append("Obtain corroborating documentation or witness statements")

        if fact.strength < 0.3:
            fragility += self.VULNERABILITY_FACTORS["single_source"]
            vulnerabilities.append("Very low factual strength rating")
            mitigations.append("Strengthen with additional evidence sources")
        elif fact.strength < 0.5:
            fragility += self.VULNERABILITY_FACTORS["single_source"] * 0.5
            vulnerabilities.append("Below-average factual strength")
            mitigations.append("Consider supplementary evidence")

        desc_lower = fact.description.lower()

        oral_indicators = ["said", "told", "verbal", "oral", "conversation", "phone call", "meeting"]
        if any(ind in desc_lower for ind in oral_indicators):
            fragility += self.VULNERABILITY_FACTORS["oral_only"]
            vulnerabilities.append("Fact may rely on oral testimony without documentation")
            mitigations.append("Attempt to identify contemporaneous written records or witnesses")

        hearsay_indicators = ["reportedly", "allegedly", "informed by", "told that", "heard that"]
        if any(ind in desc_lower for ind in hearsay_indicators):
            fragility += self.VULNERABILITY_FACTORS["hearsay_risk"]
            vulnerabilities.append("Potential hearsay concern")
            mitigations.append("Identify original declarant; evaluate hearsay exceptions")

        time_indicators = ["approximately", "around", "about", "sometime", "roughly"]
        if any(ind in desc_lower for ind in time_indicators):
            fragility += self.VULNERABILITY_FACTORS["time_dependent"]
            vulnerabilities.append("Temporal imprecision may weaken fact")
            mitigations.append("Pin down exact dates through records review")

        expert_indicators = ["expert", "specialist", "analysis", "opinion", "assessment", "study"]
        if any(ind in desc_lower for ind in expert_indicators):
            fragility += self.VULNERABILITY_FACTORS["expert_dependent"]
            vulnerabilities.append("Fact depends on expert opinion which may face Daubert challenge")
            mitigations.append("Ensure expert methodology meets Daubert reliability standards")

        circumstantial_indicators = ["suggests", "implies", "indicates", "appears", "seems", "likely"]
        if any(ind in desc_lower for ind in circumstantial_indicators):
            fragility += self.VULNERABILITY_FACTORS["circumstantial"]
            vulnerabilities.append("Circumstantial characterization may be challenged")
            mitigations.append("Identify direct evidence supporting the inference")

        fragility = min(1.0, fragility)

        if fragility < 0.2:
            label = "robust"
        elif fragility < 0.4:
            label = "moderate"
        elif fragility < 0.6:
            label = "fragile"
        elif fragility < 0.8:
            label = "very_fragile"
        else:
            label = "critical"

        return FactFragilityResult(
            fact_index=0,
            description=fact.description[:200],
            fragility_score=round(fragility, 4),
            fragility_label=label,
            vulnerability_factors=vulnerabilities,
            mitigation_suggestions=mitigations,
        )

    def score_all_facts(self, facts: List[ClaimFact]) -> List[FactFragilityResult]:
        """Score fragility for all facts in a case."""
        results: List[FactFragilityResult] = []
        for idx, fact in enumerate(facts):
            result = self.score_fact(fact)
            result.fact_index = idx
            results.append(result)
        return results

    def get_aggregate_fragility(self, facts: List[ClaimFact]) -> Dict[str, Any]:
        """Get aggregate fragility metrics across all facts."""
        if not facts:
            return {"total_facts": 0, "avg_fragility": 0.0, "max_fragility": 0.0}
        results = self.score_all_facts(facts)
        scores = [r.fragility_score for r in results]
        return {
            "total_facts": len(facts),
            "avg_fragility": round(sum(scores) / len(scores), 4),
            "max_fragility": round(max(scores), 4),
            "min_fragility": round(min(scores), 4),
            "critical_count": sum(1 for s in scores if s >= 0.8),
            "fragile_count": sum(1 for s in scores if 0.6 <= s < 0.8),
            "robust_count": sum(1 for s in scores if s < 0.2),
        }


# ============================================================================
# STATUTE OF LIMITATIONS TRACKER
# ============================================================================

class StatuteOfLimitationsTracker:
    """Tracks statute of limitations across litigation types and jurisdictions."""

    SOL_TABLE: Dict[str, Dict[str, float]] = {
        "breach_of_contract": {
            "federal": 4.0, "california": 4.0, "texas": 4.0, "new_york": 6.0,
            "delaware": 3.0, "florida": 5.0, "illinois": 10.0, "default": 4.0,
        },
        "negligence": {
            "federal": 2.0, "california": 2.0, "texas": 2.0, "new_york": 3.0,
            "delaware": 2.0, "florida": 4.0, "illinois": 2.0, "default": 2.0,
        },
        "fraud": {
            "federal": 3.0, "california": 3.0, "texas": 4.0, "new_york": 6.0,
            "delaware": 3.0, "florida": 4.0, "illinois": 5.0, "default": 3.0,
        },
        "wrongful_termination": {
            "federal": 2.0, "california": 2.0, "texas": 2.0, "new_york": 3.0,
            "default": 2.0,
        },
        "employment_discrimination": {
            "federal": 0.82, "california": 1.0, "texas": 0.82, "new_york": 3.0,
            "default": 0.82,
        },
        "securities_fraud_10b5": {
            "federal": 2.0, "default": 2.0,
        },
        "patent_infringement": {
            "federal": 6.0, "default": 6.0,
        },
        "antitrust_sherman": {
            "federal": 4.0, "default": 4.0,
        },
        "environmental_cercla": {
            "federal": 6.0, "default": 6.0,
        },
        "products_liability": {
            "federal": 2.0, "california": 2.0, "texas": 2.0, "new_york": 3.0,
            "florida": 4.0, "illinois": 2.0, "default": 2.0,
        },
        "insurance_bad_faith": {
            "federal": 2.0, "california": 2.0, "texas": 2.0, "new_york": 6.0,
            "default": 2.0,
        },
        "trade_secret_misappropriation": {
            "federal": 3.0, "california": 3.0, "texas": 3.0, "default": 3.0,
        },
        "trademark_infringement": {
            "federal": 3.0, "default": 3.0,
        },
        "qui_tam_whistleblower": {
            "federal": 6.0, "default": 6.0,
        },
        "flsa_wage_hour": {
            "federal": 2.0, "default": 2.0,
        },
        "class_action": {
            "default": 3.0,
        },
    }

    TOLLING_DOCTRINES: Dict[str, str] = {
        "fraudulent_concealment": (
            "Statute tolled during period defendant actively concealed the cause of action. "
            "Plaintiff must show (1) defendant concealed facts, (2) plaintiff failed to "
            "discover facts within limitations period, (3) plaintiff was diligent."
        ),
        "discovery_rule": (
            "Statute accrues when plaintiff discovers or should have discovered the injury "
            "and its cause, rather than at the date of injury."
        ),
        "minority": (
            "Statute tolled during minority. In most states, limitations period begins "
            "running when plaintiff reaches age of majority (typically 18)."
        ),
        "mental_incapacity": (
            "Statute tolled during period of mental incapacity. Must show plaintiff was "
            "unable to manage affairs or understand legal rights."
        ),
        "defendant_absence": (
            "Statute tolled during period defendant is absent from the jurisdiction, "
            "preventing service of process."
        ),
        "bankruptcy_stay": (
            "Automatic stay under 11 USC 362 tolls limitations period during bankruptcy. "
            "Period resumes upon lifting of stay or dismissal."
        ),
        "class_action_tolling": (
            "American Pipe tolling: filing of class action tolls SOL for putative class "
            "members. Individual actions must be filed within reasonable time after "
            "class certification is denied or class is decertified."
        ),
        "equitable_estoppel": (
            "Defendant may be estopped from asserting SOL defense if defendant's conduct "
            "induced plaintiff to delay filing beyond the limitations period."
        ),
    }

    REPOSE_PERIODS: Dict[str, float] = {
        "products_liability": 12.0,
        "construction_defect": 10.0,
        "securities_fraud_10b5": 5.0,
        "accounting_malpractice": 15.0,
    }

    def __init__(self) -> None:
        logger.info(
            f"StatuteOfLimitationsTracker initialized | "
            f"types={len(self.SOL_TABLE)} | tolling_doctrines={len(self.TOLLING_DOCTRINES)}"
        )

    def get_sol(self, litigation_type: str, jurisdiction: str) -> Optional[float]:
        """Get the statute of limitations in years for a litigation type and jurisdiction."""
        type_table = self.SOL_TABLE.get(litigation_type, {})
        jur_key = jurisdiction.lower().replace(" ", "_")
        sol = type_table.get(jur_key)
        if sol is None:
            sol = type_table.get("default")
        return sol

    def check_expiration(
        self,
        litigation_type: str,
        jurisdiction: str,
        injury_date: str,
        discovery_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Check whether the statute of limitations has expired."""
        sol_years = self.get_sol(litigation_type, jurisdiction)
        if sol_years is None:
            return {
                "litigation_type": litigation_type,
                "jurisdiction": jurisdiction,
                "sol_years": None,
                "status": "unknown",
                "message": "No SOL data available for this litigation type/jurisdiction combination.",
            }

        try:
            accrual_str = discovery_date if discovery_date else injury_date
            accrual = datetime.fromisoformat(accrual_str)
            if accrual.tzinfo is None:
                accrual = accrual.replace(tzinfo=timezone.utc)

            sol_days = int(sol_years * 365.25)
            from datetime import timedelta
            deadline = accrual + timedelta(days=sol_days)
            now = datetime.now(timezone.utc)
            remaining = (deadline - now).days

            if remaining < 0:
                status = "expired"
                urgency = "CRITICAL - Claim is time-barred absent tolling"
            elif remaining < 90:
                status = "imminent"
                urgency = "URGENT - Less than 90 days remaining"
            elif remaining < 365:
                status = "approaching"
                urgency = "WARNING - Less than 1 year remaining"
            else:
                status = "within_period"
                urgency = "Within limitations period"

            return {
                "litigation_type": litigation_type,
                "jurisdiction": jurisdiction,
                "sol_years": sol_years,
                "accrual_date": accrual.isoformat(),
                "deadline": deadline.isoformat(),
                "days_remaining": remaining,
                "status": status,
                "urgency": urgency,
                "discovery_rule_applied": discovery_date is not None,
                "repose_period": self.REPOSE_PERIODS.get(litigation_type),
            }
        except (ValueError, OverflowError) as exc:
            return {
                "litigation_type": litigation_type,
                "jurisdiction": jurisdiction,
                "sol_years": sol_years,
                "status": "error",
                "message": f"Date parsing error: {str(exc)}",
            }

    def get_tolling_doctrines(self) -> Dict[str, str]:
        """Return all tolling doctrines with descriptions."""
        return dict(self.TOLLING_DOCTRINES)

    def get_applicable_tolling(self, tolling_events: List[str]) -> List[Dict[str, str]]:
        """Match tolling events to applicable doctrines."""
        results: List[Dict[str, str]] = []
        for event in tolling_events:
            event_lower = event.lower()
            for doctrine_key, description in self.TOLLING_DOCTRINES.items():
                key_words = doctrine_key.replace("_", " ").split()
                if any(word in event_lower for word in key_words):
                    results.append({
                        "event": event,
                        "doctrine": doctrine_key,
                        "description": description,
                    })
        return results


# Global SOL tracker instance
_sol_tracker = StatuteOfLimitationsTracker()


# ============================================================================
# INSURANCE COVERAGE ANALYZER
# ============================================================================

class InsuranceCoverageAnalyzer:
    """Analyzes insurance coverage implications for litigation risk."""

    COVERAGE_TYPES: Dict[str, Dict[str, Any]] = {
        "cgl": {
            "name": "Commercial General Liability",
            "typically_covers": [
                "negligence", "products_liability", "premises_liability",
                "personal_injury", "advertising_injury",
            ],
            "typically_excludes": [
                "intentional_tort", "breach_of_contract", "employment_discrimination",
                "pollution", "professional_errors", "securities_fraud_10b5",
            ],
            "common_limits": {"per_occurrence": 1_000_000, "aggregate": 2_000_000},
        },
        "d_and_o": {
            "name": "Directors & Officers",
            "typically_covers": [
                "securities_fraud_10b5", "derivative_action", "regulatory_enforcement",
                "fiduciary_breach", "employment_discrimination",
            ],
            "typically_excludes": [
                "fraud_established", "criminal_conduct", "personal_profit",
            ],
            "common_limits": {"per_claim": 5_000_000, "aggregate": 5_000_000},
        },
        "epl": {
            "name": "Employment Practices Liability",
            "typically_covers": [
                "wrongful_termination", "employment_discrimination", "sexual_harassment",
                "retaliation", "flsa_wage_hour",
            ],
            "typically_excludes": [
                "intentional_criminal_acts", "osha_fines", "workers_comp",
            ],
            "common_limits": {"per_claim": 1_000_000, "aggregate": 2_000_000},
        },
        "professional_liability": {
            "name": "Professional Liability (E&O)",
            "typically_covers": [
                "professional_negligence", "errors_omissions", "medical_malpractice",
            ],
            "typically_excludes": [
                "intentional_misconduct", "criminal_acts", "bodily_injury",
            ],
            "common_limits": {"per_claim": 1_000_000, "aggregate": 3_000_000},
        },
        "cyber": {
            "name": "Cyber Liability",
            "typically_covers": [
                "data_breach", "ransomware", "privacy_violation",
                "notification_costs", "regulatory_fines",
            ],
            "typically_excludes": [
                "patent_infringement", "trade_secret", "prior_known_events",
            ],
            "common_limits": {"per_claim": 2_000_000, "aggregate": 5_000_000},
        },
    }

    def __init__(self) -> None:
        logger.info(f"InsuranceCoverageAnalyzer initialized | policies={len(self.COVERAGE_TYPES)}")

    def assess_coverage(self, litigation_type: str) -> Dict[str, Any]:
        """Assess which insurance policies may respond to this litigation type."""
        potentially_covered: List[Dict[str, Any]] = []
        likely_excluded: List[Dict[str, Any]] = []

        for policy_type, policy_info in self.COVERAGE_TYPES.items():
            covers = policy_info["typically_covers"]
            excludes = policy_info["typically_excludes"]

            if litigation_type in covers or any(
                lit_type in litigation_type for lit_type in covers
            ):
                potentially_covered.append({
                    "policy_type": policy_type,
                    "policy_name": policy_info["name"],
                    "common_limits": policy_info["common_limits"],
                    "coverage_status": "potentially_covered",
                })
            elif litigation_type in excludes or any(
                lit_type in litigation_type for lit_type in excludes
            ):
                likely_excluded.append({
                    "policy_type": policy_type,
                    "policy_name": policy_info["name"],
                    "coverage_status": "likely_excluded",
                    "exclusion_basis": "standard_policy_exclusion",
                })

        total_potential_limits = sum(
            p["common_limits"].get("per_claim", 0) for p in potentially_covered
        )

        return {
            "litigation_type": litigation_type,
            "potentially_covered_by": potentially_covered,
            "likely_excluded_from": likely_excluded,
            "total_potential_coverage": total_potential_limits,
            "coverage_notes": [
                "Coverage assessment is preliminary. Actual coverage depends on specific policy terms.",
                "Timely notice to insurers is critical. Late notice may void coverage.",
                "Reservation of rights letters should be carefully reviewed with coverage counsel.",
            ],
        }


# Global insurance analyzer
_insurance_analyzer = InsuranceCoverageAnalyzer()


# ============================================================================
# (15) AUDIT TRAIL JSONL - integrated via EngineTelemeter
# (16) DETERMINISM HASH SHA-256
# ============================================================================

class DeterminismHasher:
    """Computes deterministic SHA-256 hashes for response reproducibility verification."""

    def __init__(self) -> None:
        self._hash_count: int = 0

    def hash_response(
        self,
        query_text: str,
        litigation_type: str,
        jurisdiction: str,
        doctrine_keys: List[str],
        risk_score: float,
        confidence: float,
    ) -> str:
        """Compute a determinism hash for a complete response."""
        payload = json.dumps({
            "query": query_text[:500],
            "type": litigation_type,
            "jurisdiction": jurisdiction,
            "doctrines": sorted(doctrine_keys),
            "risk": round(risk_score, 6),
            "confidence": round(confidence, 6),
            "engine": ENGINE_ID,
            "version": ENGINE_VERSION,
        }, sort_keys=True, separators=(",", ":"))
        h = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        self._hash_count += 1
        return h

    def hash_text(self, text: str) -> str:
        """Hash arbitrary text."""
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def verify_hash(self, expected: str, actual: str) -> bool:
        """Verify two hashes match."""
        return expected == actual

    @property
    def hash_count(self) -> int:
        """Total hashes computed."""
        return self._hash_count


# ============================================================================
# RISK SCORING ENGINE
# ============================================================================

class RiskScoringEngine:
    """Core risk scoring engine computing composite risk across 6 dimensions."""

    def __init__(
        self,
        cache: DoctrineCacheManager,
        normalizer: SemanticNormalizer,
        search_engine: SearchEngine,
    ) -> None:
        self._cache = cache
        self._normalizer = normalizer
        self._search = search_engine
        logger.info("RiskScoringEngine initialized")

    def score_case_merit(
        self,
        litigation_type: str,
        facts: List[ClaimFact],
        claims: List[ClaimDetail],
        doctrines: List[DoctrineBlock],
    ) -> Tuple[float, str]:
        """Score the merit of the case (0.0-1.0 where 1.0 = very strong case against defendant)."""
        if not doctrines:
            return 0.5, "Insufficient doctrine coverage to assess case merit"

        legal_theory_strength = 0.5
        for d in doctrines:
            if d.confidence == ConfidenceLevel.WELL_SETTLED:
                legal_theory_strength = max(legal_theory_strength, 0.8)
            elif d.confidence == ConfidenceLevel.GENERALLY_ACCEPTED:
                legal_theory_strength = max(legal_theory_strength, 0.65)

        factual_support = 0.3
        if facts:
            verified = sum(1 for f in facts if f.verified)
            high_strength = sum(1 for f in facts if f.strength >= 0.7)
            factual_support = min(1.0, (verified * 0.15 + high_strength * 0.10 + len(facts) * 0.03))

        burden_factor = 0.5
        for d in doctrines:
            if d.burden_of_proof == "beyond_reasonable_doubt":
                burden_factor = 0.3
            elif d.burden_of_proof == "clear_and_convincing":
                burden_factor = 0.4
            elif d.burden_of_proof == "preponderance_of_evidence":
                burden_factor = 0.55

        defense_exposure = 0.5
        for d in doctrines:
            multipliers = d.risk_multipliers
            for key, mult in multipliers.items():
                if mult < 1.0:
                    defense_exposure = max(defense_exposure, 0.7)

        score = (
            legal_theory_strength * 0.35
            + factual_support * 0.30
            + burden_factor * 0.20
            + defense_exposure * 0.15
        )

        finding = (
            f"Case merit assessment: legal theory strength={legal_theory_strength:.2f}, "
            f"factual support={factual_support:.2f}, burden factor={burden_factor:.2f}"
        )

        return round(score, 4), finding

    def score_damages_exposure(
        self,
        litigation_type: str,
        amount_in_controversy: Optional[float],
        claims: List[ClaimDetail],
        doctrines: List[DoctrineBlock],
    ) -> Tuple[float, str]:
        """Score damages exposure risk (0.0-1.0 where 1.0 = extreme exposure)."""
        base_score = 0.5

        if amount_in_controversy:
            if amount_in_controversy > 10_000_000:
                base_score = 0.9
            elif amount_in_controversy > 1_000_000:
                base_score = 0.75
            elif amount_in_controversy > 100_000:
                base_score = 0.55
            else:
                base_score = 0.35

        punitive_risk = 0.0
        for d in doctrines:
            if "punitive" in d.damages_guidance.lower():
                punitive_risk = max(punitive_risk, 0.3)
            if d.risk_severity == RiskSeverity.CRITICAL:
                punitive_risk = max(punitive_risk, 0.2)

        treble_risk = 0.0
        for d in doctrines:
            if "treble" in d.damages_guidance.lower():
                treble_risk = 0.4

        claims_complexity = min(1.0, len(claims) * 0.1)

        score = base_score * 0.50 + punitive_risk * 0.20 + treble_risk * 0.15 + claims_complexity * 0.15
        score = min(1.0, score)

        finding = (
            f"Damages exposure: base={base_score:.2f}, punitive_risk={punitive_risk:.2f}, "
            f"treble_risk={treble_risk:.2f}, claims_complexity={claims_complexity:.2f}"
        )

        return round(score, 4), finding

    def score_jurisdiction_risk(
        self,
        jurisdiction: str,
        litigation_type: str,
        doctrines: List[DoctrineBlock],
        zoned: ZonedAnalyzer,
    ) -> Tuple[float, str]:
        """Score jurisdiction-specific risk."""
        zone_analysis = zoned.analyze_zone(jurisdiction, litigation_type)
        zone_risk = zone_analysis["zone_risk_score"]

        jd_penalty = 0.0
        for d in doctrines:
            if d.confidence == ConfidenceLevel.JURISDICTION_DEPENDENT:
                jd_penalty += 0.05

        score = min(1.0, zone_risk + jd_penalty)
        finding = (
            f"Jurisdiction risk for {jurisdiction}: zone_score={zone_risk:.2f}, "
            f"jd_penalty={jd_penalty:.2f}"
        )

        return round(score, 4), finding

    def score_discovery_cost(
        self,
        claims: List[ClaimDetail],
        facts: List[ClaimFact],
        parties: List[PartyInfo],
        doctrines: List[DoctrineBlock],
    ) -> Tuple[float, str]:
        """Score discovery cost burden (0.0-1.0 where 1.0 = extremely expensive)."""
        volume_factor = min(1.0, (len(claims) * 0.08 + len(facts) * 0.04))
        party_factor = min(1.0, len(parties) * 0.12)

        complexity_factor = 0.3
        for d in doctrines:
            if d.category in (LitigationCategory.SECURITIES, LitigationCategory.ANTITRUST):
                complexity_factor = max(complexity_factor, 0.7)
            elif d.category == LitigationCategory.CLASS_ACTION:
                complexity_factor = max(complexity_factor, 0.8)
            elif d.category in (LitigationCategory.ENVIRONMENTAL, LitigationCategory.IP_LITIGATION):
                complexity_factor = max(complexity_factor, 0.6)

        expert_factor = 0.3
        for d in doctrines:
            if any("expert" in kw for kw in d.keywords):
                expert_factor = max(expert_factor, 0.6)
            if d.category == LitigationCategory.PRODUCTS_LIABILITY:
                expert_factor = max(expert_factor, 0.7)

        score = (
            volume_factor * 0.25
            + party_factor * 0.20
            + complexity_factor * 0.30
            + expert_factor * 0.25
        )

        finding = (
            f"Discovery cost: volume={volume_factor:.2f}, parties={party_factor:.2f}, "
            f"complexity={complexity_factor:.2f}, expert_needs={expert_factor:.2f}"
        )

        return round(min(1.0, score), 4), finding

    def score_settlement_pressure(
        self,
        litigation_type: str,
        risk_score: float,
        damages_exposure: float,
        discovery_cost_score: float,
        doctrines: List[DoctrineBlock],
    ) -> Tuple[float, str]:
        """Score settlement pressure (0.0-1.0 where 1.0 = extreme pressure to settle)."""
        cost_ratio = (discovery_cost_score * 0.5 + damages_exposure * 0.5)

        publicity_risk = 0.3
        high_profile_types = {
            "employment_discrimination", "securities_fraud_10b5", "class_action",
            "environmental_cercla", "products_liability",
        }
        if litigation_type in high_profile_types:
            publicity_risk = 0.7

        precedent_value = 0.3
        for d in doctrines:
            if d.confidence == ConfidenceLevel.EVOLVING_LAW:
                precedent_value = max(precedent_value, 0.6)

        business_disruption = min(1.0, discovery_cost_score * 1.2)

        score = (
            cost_ratio * 0.35
            + publicity_risk * 0.25
            + business_disruption * 0.25
            + precedent_value * 0.15
        )

        finding = (
            f"Settlement pressure: cost_ratio={cost_ratio:.2f}, publicity={publicity_risk:.2f}, "
            f"disruption={business_disruption:.2f}, precedent_value={precedent_value:.2f}"
        )

        return round(min(1.0, score), 4), finding

    def score_regulatory_escalation(
        self,
        litigation_type: str,
        doctrines: List[DoctrineBlock],
    ) -> Tuple[float, str]:
        """Score risk of regulatory escalation."""
        base = 0.2
        regulatory_types = {
            "regulatory_enforcement", "qui_tam_whistleblower", "environmental_cercla",
            "securities_fraud_10b5", "antitrust_sherman", "antitrust_clayton",
            "administrative_action",
        }
        if litigation_type in regulatory_types:
            base = 0.7

        agency_factor = 0.0
        for d in doctrines:
            if d.category == LitigationCategory.REGULATORY:
                agency_factor = max(agency_factor, 0.4)
            if "enforcement" in " ".join(d.keywords):
                agency_factor = max(agency_factor, 0.3)
            if "criminal" in d.damages_guidance.lower():
                agency_factor = max(agency_factor, 0.5)

        score = base * 0.60 + agency_factor * 0.40

        finding = (
            f"Regulatory escalation: base={base:.2f}, agency_factor={agency_factor:.2f}"
        )

        return round(min(1.0, score), 4), finding

    def compute_composite_risk(
        self,
        merit: float,
        damages: float,
        jurisdiction: float,
        discovery: float,
        settlement: float,
        regulatory: float,
    ) -> Tuple[float, str]:
        """Compute weighted composite risk score."""
        composite = (
            merit * RISK_DIMENSION_WEIGHTS["case_merit"]
            + damages * RISK_DIMENSION_WEIGHTS["damages_exposure"]
            + jurisdiction * RISK_DIMENSION_WEIGHTS["jurisdiction_risk"]
            + discovery * RISK_DIMENSION_WEIGHTS["discovery_cost"]
            + settlement * RISK_DIMENSION_WEIGHTS["settlement_pressure"]
            + regulatory * RISK_DIMENSION_WEIGHTS["regulatory_escalation"]
        )

        composite = round(min(1.0, max(0.0, composite)), 4)

        if composite >= 0.80:
            level = "critical"
        elif composite >= 0.60:
            level = "high"
        elif composite >= 0.40:
            level = "medium"
        elif composite >= 0.20:
            level = "low"
        else:
            level = "negligible"

        return composite, level


# ============================================================================
# DAMAGES ESTIMATOR
# ============================================================================

class DamagesEstimator:
    """Computes damages range estimates based on litigation type and facts."""

    COMPENSATORY_BASELINES: Dict[str, Tuple[float, float]] = {
        "breach_of_contract": (50_000, 500_000),
        "negligence": (25_000, 1_000_000),
        "strict_liability": (100_000, 5_000_000),
        "intentional_tort": (50_000, 2_000_000),
        "wrongful_termination": (75_000, 750_000),
        "employment_discrimination": (50_000, 500_000),
        "flsa_wage_hour": (10_000, 200_000),
        "securities_fraud_10b5": (1_000_000, 50_000_000),
        "class_action": (500_000, 100_000_000),
        "antitrust_sherman": (500_000, 50_000_000),
        "patent_infringement": (250_000, 10_000_000),
        "trade_secret_misappropriation": (100_000, 5_000_000),
        "trademark_infringement": (50_000, 2_000_000),
        "environmental_cercla": (500_000, 50_000_000),
        "products_liability": (100_000, 10_000_000),
        "insurance_bad_faith": (100_000, 5_000_000),
        "qui_tam_whistleblower": (200_000, 20_000_000),
    }

    DEFAULT_BASELINE: Tuple[float, float] = (50_000, 1_000_000)

    def __init__(self) -> None:
        logger.info("DamagesEstimator initialized")

    def estimate(
        self,
        litigation_type: str,
        claims: List[ClaimDetail],
        amount_in_controversy: Optional[float],
        doctrines: List[DoctrineBlock],
        punitive_likely: bool = False,
        attorneys_fees_recoverable: bool = False,
        class_action: bool = False,
        class_size: Optional[int] = None,
    ) -> List[DamagesRange]:
        """Estimate damages ranges for the case."""
        results: List[DamagesRange] = []

        base_low, base_high = self.COMPENSATORY_BASELINES.get(
            litigation_type, self.DEFAULT_BASELINE
        )

        if amount_in_controversy:
            base_low = min(base_low, amount_in_controversy * 0.3)
            base_high = max(base_high, amount_in_controversy * 1.5)

        claims_multiplier = max(1.0, 1.0 + len(claims) * 0.1)
        comp_low = base_low * claims_multiplier
        comp_high = base_high * claims_multiplier

        if class_action and class_size:
            comp_low *= min(class_size, 100)
            comp_high *= min(class_size, 1000)

        results.append(DamagesRange(
            category="compensatory",
            low=round(comp_low, 2),
            high=round(comp_high, 2),
            methodology="baseline_adjusted_by_litigation_type_and_claims",
            confidence=0.6,
        ))

        conseq_low = comp_low * 0.2
        conseq_high = comp_high * 0.5
        results.append(DamagesRange(
            category="consequential",
            low=round(conseq_low, 2),
            high=round(conseq_high, 2),
            methodology="percentage_of_compensatory",
            confidence=0.4,
        ))

        pun_low = 0.0
        pun_high = 0.0
        if punitive_likely:
            pun_low = comp_low * 1.0
            pun_high = comp_high * 4.0
        else:
            for d in doctrines:
                if "punitive" in d.damages_guidance.lower():
                    pun_low = comp_low * 0.5
                    pun_high = comp_high * 3.0
                    break

        results.append(DamagesRange(
            category="punitive",
            low=round(pun_low, 2),
            high=round(pun_high, 2),
            methodology="ratio_to_compensatory_bmw_guideposts",
            confidence=0.3 if pun_high > 0 else 0.8,
        ))

        stat_low = 0.0
        stat_high = 0.0
        for d in doctrines:
            if "treble" in d.damages_guidance.lower():
                stat_low = comp_low * 2.0
                stat_high = comp_high * 2.0
                break
            if "liquidated" in d.damages_guidance.lower():
                stat_low = comp_low * 0.5
                stat_high = comp_high * 1.0
                break

        results.append(DamagesRange(
            category="statutory",
            low=round(stat_low, 2),
            high=round(stat_high, 2),
            methodology="statutory_multiplier_analysis",
            confidence=0.5,
        ))

        if attorneys_fees_recoverable:
            fee_low = (comp_low + conseq_low) * 0.15
            fee_high = (comp_high + conseq_high) * 0.40
        else:
            fee_low = 50_000
            fee_high = 500_000
            for d in doctrines:
                if "attorneys" in d.damages_guidance.lower() and "fees" in d.damages_guidance.lower():
                    fee_low = (comp_low + conseq_low) * 0.15
                    fee_high = (comp_high + conseq_high) * 0.35
                    break

        results.append(DamagesRange(
            category="attorneys_fees",
            low=round(fee_low, 2),
            high=round(fee_high, 2),
            methodology="percentage_of_recovery_or_lodestar",
            confidence=0.5,
        ))

        total_low = sum(r.low for r in results)
        total_high = sum(r.high for r in results)
        results.append(DamagesRange(
            category="total_exposure",
            low=round(total_low, 2),
            high=round(total_high, 2),
            methodology="sum_of_all_categories",
            confidence=0.35,
        ))

        return results


# ============================================================================
# SETTLEMENT ANALYZER
# ============================================================================

class SettlementAnalyzer:
    """Computes settlement valuations using expected value methodology."""

    def __init__(self) -> None:
        logger.info("SettlementAnalyzer initialized")

    def analyze(
        self,
        liability_probability: float,
        damages_low: float,
        damages_high: float,
        litigation_cost: float,
        time_to_trial_months: int,
        publicity_risk: float,
        business_disruption: float,
        precedent_value: float,
    ) -> SettlementValuation:
        """Compute settlement valuation."""
        expected_damages = liability_probability * ((damages_low + damages_high) / 2.0)
        expected_value = expected_damages + litigation_cost

        discount_rate = 0.05
        years = time_to_trial_months / 12.0
        present_value_factor = 1.0 / ((1.0 + discount_rate) ** years)
        pv_expected = expected_value * present_value_factor

        publicity_adjustment = 1.0 + (publicity_risk * 0.3)
        disruption_adjustment = 1.0 + (business_disruption * 0.2)
        precedent_discount = 1.0 - (precedent_value * 0.15)

        adjusted_value = pv_expected * publicity_adjustment * disruption_adjustment * precedent_discount

        settlement_low = adjusted_value * 0.4
        settlement_high = adjusted_value * 0.85

        plaintiff_minimum = expected_damages * 0.3
        defendant_maximum = expected_value * 0.75

        zopa_exists = plaintiff_minimum < defendant_maximum
        zopa_low = plaintiff_minimum if zopa_exists else None
        zopa_high = defendant_maximum if zopa_exists else None

        if zopa_exists:
            if settlement_high < plaintiff_minimum * 1.5:
                recommendation = "Settlement likely achievable within ZOPA; pursue early mediation"
            else:
                recommendation = "ZOPA exists but wide range; structured negotiation recommended"
        else:
            recommendation = "No clear ZOPA; positions far apart. Consider early case evaluation or MSJ"

        return SettlementValuation(
            expected_value=round(expected_value, 2),
            settlement_range_low=round(settlement_low, 2),
            settlement_range_high=round(settlement_high, 2),
            zopa_exists=zopa_exists,
            zopa_low=round(zopa_low, 2) if zopa_low else None,
            zopa_high=round(zopa_high, 2) if zopa_high else None,
            recommendation=recommendation,
            factors={
                "liability_probability": liability_probability,
                "expected_damages": round(expected_damages, 2),
                "litigation_cost": litigation_cost,
                "present_value_factor": round(present_value_factor, 4),
                "publicity_adjustment": round(publicity_adjustment, 4),
                "disruption_adjustment": round(disruption_adjustment, 4),
                "precedent_discount": round(precedent_discount, 4),
            },
        )


# ============================================================================
# DISCOVERY COST MODELER
# ============================================================================

class DiscoveryCostModeler:
    """Models discovery costs based on case parameters."""

    COST_PER_DOCUMENT_REVIEW: float = 1.50
    COST_PER_DEPOSITION_DAY: float = 5000.0
    COST_PER_EXPERT_ENGAGEMENT: float = 75000.0
    E_DISCOVERY_BASE_COST: float = 25000.0
    E_DISCOVERY_PER_CUSTODIAN: float = 8000.0
    E_DISCOVERY_PER_GB: float = 500.0
    INTERNATIONAL_MULTIPLIER: float = 2.5

    PRIVILEGE_MULTIPLIERS: Dict[str, float] = {
        "low": 1.0,
        "moderate": 1.3,
        "high": 1.8,
        "extreme": 2.5,
    }

    def __init__(self) -> None:
        logger.info("DiscoveryCostModeler initialized")

    def estimate(
        self,
        document_volume: int,
        custodian_count: int,
        deposition_count: int,
        expert_count: int,
        e_discovery: bool,
        international: bool,
        privilege_complexity: str,
    ) -> DiscoveryCostEstimate:
        """Estimate total discovery costs."""
        privilege_mult = self.PRIVILEGE_MULTIPLIERS.get(privilege_complexity, 1.3)

        doc_review = document_volume * self.COST_PER_DOCUMENT_REVIEW * privilege_mult
        depo_cost = deposition_count * self.COST_PER_DEPOSITION_DAY * 2
        expert_cost = expert_count * self.COST_PER_EXPERT_ENGAGEMENT

        e_disc_cost = 0.0
        if e_discovery:
            e_disc_cost = (
                self.E_DISCOVERY_BASE_COST
                + custodian_count * self.E_DISCOVERY_PER_CUSTODIAN
                + document_volume * 0.001 * self.E_DISCOVERY_PER_GB
            )

        misc = (doc_review + depo_cost + expert_cost + e_disc_cost) * 0.08

        if international:
            doc_review *= self.INTERNATIONAL_MULTIPLIER
            depo_cost *= self.INTERNATIONAL_MULTIPLIER * 0.8
            e_disc_cost *= self.INTERNATIONAL_MULTIPLIER * 0.6

        total = doc_review + depo_cost + expert_cost + e_disc_cost + misc
        cost_per_doc = total / max(document_volume, 1)

        proportionality_warning = None
        if total > 500000 and document_volume < 5000:
            proportionality_warning = (
                "Discovery costs appear disproportionate to document volume. "
                "Consider Rule 26(b)(1) proportionality objections."
            )

        return DiscoveryCostEstimate(
            document_review_cost=round(doc_review, 2),
            deposition_cost=round(depo_cost, 2),
            expert_witness_cost=round(expert_cost, 2),
            e_discovery_cost=round(e_disc_cost, 2),
            miscellaneous_cost=round(misc, 2),
            total_estimate=round(total, 2),
            cost_per_document=round(cost_per_doc, 2),
            proportionality_warning=proportionality_warning,
        )


# ============================================================================
# JURISDICTION ANALYZER
# ============================================================================

class JurisdictionAnalyzer:
    """Performs jurisdiction-specific analysis for litigation risk."""

    def __init__(self, zoned: ZonedAnalyzer) -> None:
        self._zoned = zoned
        logger.info("JurisdictionAnalyzer initialized")

    def analyze(
        self,
        jurisdiction: str,
        litigation_type: str,
        defendant_state: Optional[str],
        plaintiff_state: Optional[str],
        forum_selection_clause: bool,
        amount_in_controversy: Optional[float],
        doctrines: List[DoctrineBlock],
    ) -> JurisdictionAssessment:
        """Perform comprehensive jurisdiction analysis."""
        zone = self._zoned.analyze_zone(jurisdiction, litigation_type)

        venue_favorability = 1.0 - zone["zone_risk_score"]
        if forum_selection_clause:
            venue_favorability = min(1.0, venue_favorability + 0.2)

        pj_risk = 0.3
        if defendant_state and defendant_state.lower() != jurisdiction.lower():
            pj_risk = 0.6
        if forum_selection_clause:
            pj_risk = max(0.1, pj_risk - 0.3)

        smj = "federal_question"
        if jurisdiction.lower() != "federal":
            smj = "state_court"
        if amount_in_controversy and amount_in_controversy > 75000:
            if plaintiff_state and defendant_state and plaintiff_state != defendant_state:
                smj = "diversity_jurisdiction"

        jury_tendency = zone.get("jury_risk", 0.5)
        if jury_tendency > 0.6:
            jury_label = "plaintiff_favorable"
        elif jury_tendency > 0.4:
            jury_label = "neutral"
        else:
            jury_label = "defense_favorable"

        special_rules = zone.get("special_rules", [])
        local_impact = "moderate"
        if len(special_rules) > 2:
            local_impact = "significant"
        elif len(special_rules) == 0:
            local_impact = "minimal"

        overall = venue_favorability * 0.4 + (1.0 - pj_risk) * 0.3 + (1.0 - jury_tendency) * 0.3

        notes: List[str] = []
        for d in doctrines:
            if d.jurisdiction_notes:
                notes.append(d.jurisdiction_notes)

        recommended_venue = None
        if pj_risk > 0.5 and not forum_selection_clause:
            recommended_venue = defendant_state or jurisdiction

        record_jurisdiction_analysis(
            trace_id=str(uuid.uuid4()),
            jurisdiction=jurisdiction,
            venue_favorability=venue_favorability,
            judge_profile_available=False,
            jury_tendency=jury_tendency,
            local_rules_impact=len(special_rules) * 0.15,
            overall_favorability=overall,
            recommended_venue=recommended_venue,
        )

        return JurisdictionAssessment(
            jurisdiction=jurisdiction,
            venue_favorability=round(venue_favorability, 4),
            personal_jurisdiction_risk=round(pj_risk, 4),
            subject_matter_jurisdiction=smj,
            jury_tendency=jury_label,
            local_rules_impact=local_impact,
            overall_favorability=round(overall, 4),
            recommended_venue=recommended_venue,
            notes=notes[:5],
        )


# ============================================================================
# (19) MULTI-DOCTRINE DECOMPOSITION
# ============================================================================

class MultiDoctrineDecomposer:
    """Decomposes complex legal queries into multiple applicable doctrine domains
    and synthesizes cross-doctrine analysis."""

    def __init__(self, cache: DoctrineCacheManager, normalizer: SemanticNormalizer) -> None:
        self._cache = cache
        self._normalizer = normalizer
        logger.info("MultiDoctrineDecomposer initialized")

    def decompose(
        self,
        case_description: str,
        litigation_type: str,
        claims: List[ClaimDetail],
    ) -> Dict[str, Any]:
        """Decompose a case into applicable doctrine domains.

        Returns dict with matched doctrines, interaction graph, and synthesis.
        """
        norm = self._normalizer.normalize(case_description)
        key_terms = self._normalizer.extract_key_terms(case_description)

        keyword_matches: Dict[str, DoctrineBlock] = {}
        for term in key_terms:
            for block in self._cache.search_by_keyword(term):
                keyword_matches[block.key] = block

        claims_text = " ".join(c.description for c in claims) if claims else ""
        if claims_text:
            claims_norm = self._normalizer.normalize(claims_text)
            claims_terms = self._normalizer.extract_key_terms(claims_text)
            for term in claims_terms:
                for block in self._cache.search_by_keyword(term):
                    keyword_matches[block.key] = block

        category_map = self._map_to_litigation_category(litigation_type)
        if category_map:
            for block in self._cache.search_by_category(category_map):
                keyword_matches[block.key] = block

        interactions = self._build_interaction_graph(list(keyword_matches.keys()))

        primary_doctrines: List[str] = []
        supporting_doctrines: List[str] = []
        for key, block in keyword_matches.items():
            if block.category.value == category_map.value if category_map else False:
                primary_doctrines.append(key)
            else:
                supporting_doctrines.append(key)

        if not primary_doctrines and keyword_matches:
            primary_doctrines = list(keyword_matches.keys())[:5]
            supporting_doctrines = list(keyword_matches.keys())[5:]

        synthesis = self._synthesize(
            primary_doctrines, supporting_doctrines, keyword_matches, interactions
        )

        return {
            "normalized_query_hash": norm.text_hash,
            "key_terms_extracted": key_terms,
            "total_doctrines_matched": len(keyword_matches),
            "primary_doctrines": primary_doctrines,
            "supporting_doctrines": supporting_doctrines,
            "interaction_edges": interactions,
            "synthesis": synthesis,
            "all_matched_keys": sorted(keyword_matches.keys()),
        }

    def _map_to_litigation_category(self, litigation_type: str) -> Optional[LitigationCategory]:
        """Map litigation type string to LitigationCategory enum."""
        mapping: Dict[str, LitigationCategory] = {
            "breach_of_contract": LitigationCategory.CONTRACT_DISPUTE,
            "negligence": LitigationCategory.TORT_LIABILITY,
            "strict_liability": LitigationCategory.TORT_LIABILITY,
            "intentional_tort": LitigationCategory.TORT_LIABILITY,
            "wrongful_termination": LitigationCategory.EMPLOYMENT,
            "employment_discrimination": LitigationCategory.EMPLOYMENT,
            "flsa_wage_hour": LitigationCategory.EMPLOYMENT,
            "securities_fraud_10b5": LitigationCategory.SECURITIES,
            "class_action": LitigationCategory.CLASS_ACTION,
            "antitrust_sherman": LitigationCategory.ANTITRUST,
            "antitrust_clayton": LitigationCategory.ANTITRUST,
            "patent_infringement": LitigationCategory.IP_LITIGATION,
            "trade_secret_misappropriation": LitigationCategory.IP_LITIGATION,
            "trademark_infringement": LitigationCategory.IP_LITIGATION,
            "copyright_infringement": LitigationCategory.IP_LITIGATION,
            "environmental_cercla": LitigationCategory.ENVIRONMENTAL,
            "toxic_tort": LitigationCategory.ENVIRONMENTAL,
            "products_liability": LitigationCategory.PRODUCTS_LIABILITY,
            "insurance_coverage": LitigationCategory.INSURANCE,
            "insurance_bad_faith": LitigationCategory.INSURANCE,
            "regulatory_enforcement": LitigationCategory.REGULATORY,
            "qui_tam_whistleblower": LitigationCategory.REGULATORY,
            "commercial_fraud": LitigationCategory.TORT_LIABILITY,
        }
        return mapping.get(litigation_type)

    def _build_interaction_graph(self, matched_keys: List[str]) -> List[Dict[str, str]]:
        """Build interaction edges between matched doctrines."""
        edges: List[Dict[str, str]] = []
        matched_set = set(matched_keys)
        for interaction in DOCTRINE_INTERACTIONS:
            if interaction.source_key in matched_set and interaction.target_key in matched_set:
                edges.append({
                    "source": interaction.source_key,
                    "target": interaction.target_key,
                    "relationship": interaction.relationship,
                    "strength": str(interaction.strength),
                    "description": interaction.description,
                })
        return edges

    def _synthesize(
        self,
        primary: List[str],
        supporting: List[str],
        all_matched: Dict[str, DoctrineBlock],
        interactions: List[Dict[str, str]],
    ) -> str:
        """Synthesize a cross-doctrine analysis summary."""
        parts: List[str] = []

        if primary:
            parts.append(f"Primary doctrines ({len(primary)}): ")
            for key in primary[:5]:
                block = all_matched.get(key)
                if block:
                    parts.append(f"  - {block.topic} [{block.authority.value}/{block.confidence.value}]")

        if supporting:
            parts.append(f"Supporting doctrines ({len(supporting)}): ")
            for key in supporting[:5]:
                block = all_matched.get(key)
                if block:
                    parts.append(f"  - {block.topic}")

        if interactions:
            parts.append(f"Cross-doctrine interactions ({len(interactions)}):")
            for edge in interactions[:5]:
                parts.append(f"  - {edge['source']} --[{edge['relationship']}]--> {edge['target']}")

        if not parts:
            return "No applicable doctrines identified for synthesis."

        return "\n".join(parts)


# ============================================================================
# (20) DEEP ANALYSIS MODE
# ============================================================================

class DeepAnalyzer:
    """Performs deep multi-source analysis for complex litigation risk assessment."""

    def __init__(
        self,
        cache: DoctrineCacheManager,
        search_engine: SearchEngine,
        normalizer: SemanticNormalizer,
        decomposer: MultiDoctrineDecomposer,
        risk_scorer: RiskScoringEngine,
        damages_estimator: DamagesEstimator,
        settlement_analyzer: SettlementAnalyzer,
        discovery_modeler: DiscoveryCostModeler,
        jurisdiction_analyzer: JurisdictionAnalyzer,
        fragility_scorer: FactFragilityScorer,
        zoned: ZonedAnalyzer,
    ) -> None:
        self._cache = cache
        self._search = search_engine
        self._normalizer = normalizer
        self._decomposer = decomposer
        self._risk_scorer = risk_scorer
        self._damages = damages_estimator
        self._settlement = settlement_analyzer
        self._discovery = discovery_modeler
        self._jurisdiction = jurisdiction_analyzer
        self._fragility = fragility_scorer
        self._zoned = zoned
        logger.info("DeepAnalyzer initialized")

    def analyze(self, req: LitigationRiskRequest, trace_id: str) -> Dict[str, Any]:
        """Perform full deep analysis."""
        decomposition = self._decomposer.decompose(
            req.case_description, req.litigation_type, req.claims,
        )
        matched_keys = decomposition["all_matched_keys"]
        doctrines = [self._cache.get(k) for k in matched_keys if self._cache.get(k)]

        search_results = self._search.search(
            req.case_description[:500],
            litigation_type=req.litigation_type,
            jurisdiction=req.jurisdiction,
            max_results=10,
        )

        additional_keys: List[str] = []
        for sr in search_results:
            if sr.doc_type == "doctrines" and sr.doc_id.startswith("doctrine_"):
                dk = sr.doc_id.replace("doctrine_", "")
                if dk not in matched_keys:
                    block = self._cache.get(dk)
                    if block:
                        doctrines.append(block)
                        additional_keys.append(dk)

        all_keys = matched_keys + additional_keys

        facts = req.facts or []
        claims = req.claims or []
        parties = req.parties or []

        merit_score, merit_finding = self._risk_scorer.score_case_merit(
            req.litigation_type, facts, claims, doctrines
        )
        damages_score, damages_finding = self._risk_scorer.score_damages_exposure(
            req.litigation_type, req.amount_in_controversy, claims, doctrines
        )
        jurisdiction_score, jur_finding = self._risk_scorer.score_jurisdiction_risk(
            req.jurisdiction, req.litigation_type, doctrines, self._zoned
        )
        discovery_score, disc_finding = self._risk_scorer.score_discovery_cost(
            claims, facts, parties, doctrines
        )
        settlement_score, settle_finding = self._risk_scorer.score_settlement_pressure(
            req.litigation_type, merit_score, damages_score, discovery_score, doctrines
        )
        regulatory_score, reg_finding = self._risk_scorer.score_regulatory_escalation(
            req.litigation_type, doctrines
        )

        composite, risk_level = self._risk_scorer.compute_composite_risk(
            merit_score, damages_score, jurisdiction_score,
            discovery_score, settlement_score, regulatory_score,
        )

        damages_estimate = None
        if req.include_damages_estimate:
            damages_estimate = self._damages.estimate(
                litigation_type=req.litigation_type,
                claims=claims,
                amount_in_controversy=req.amount_in_controversy,
                doctrines=doctrines,
            )

        settlement_result = None
        if req.include_settlement_analysis and damages_estimate:
            total_range = next(
                (d for d in damages_estimate if d.category == "total_exposure"), None
            )
            if total_range:
                settlement_result = self._settlement.analyze(
                    liability_probability=merit_score,
                    damages_low=total_range.low,
                    damages_high=total_range.high,
                    litigation_cost=150_000,
                    time_to_trial_months=24,
                    publicity_risk=settlement_score * 0.5,
                    business_disruption=discovery_score * 0.6,
                    precedent_value=0.3,
                )

        discovery_estimate = None
        if req.include_discovery_cost:
            discovery_estimate = self._discovery.estimate(
                document_volume=max(5000, len(facts) * 1000),
                custodian_count=max(3, len(parties)),
                deposition_count=max(5, len(parties) * 2),
                expert_count=2,
                e_discovery=True,
                international=False,
                privilege_complexity="moderate",
            )

        jurisdiction_assessment = None
        if req.include_jurisdiction_analysis:
            defendant_state = None
            plaintiff_state = None
            for p in parties:
                if p.role.lower() == "defendant" and p.jurisdiction_state:
                    defendant_state = p.jurisdiction_state
                elif p.role.lower() == "plaintiff" and p.jurisdiction_state:
                    plaintiff_state = p.jurisdiction_state

            jurisdiction_assessment = self._jurisdiction.analyze(
                jurisdiction=req.jurisdiction,
                litigation_type=req.litigation_type,
                defendant_state=defendant_state,
                plaintiff_state=plaintiff_state,
                forum_selection_clause=False,
                amount_in_controversy=req.amount_in_controversy,
                doctrines=doctrines,
            )

        fragility_results = None
        if facts:
            fragility_results = self._fragility.score_all_facts(facts)

        precedents: List[PrecedentCitation] = []
        if req.include_citations:
            seen_citations: Set[str] = set()
            for d in doctrines:
                for p in d.precedents:
                    if p.citation not in seen_citations:
                        precedents.append(PrecedentCitation(
                            case_name=p.case_name,
                            citation=p.citation,
                            year=p.year,
                            court=p.court,
                            holding=p.holding,
                            relevance_score=p.relevance_score,
                        ))
                        seen_citations.add(p.citation)

        risk_dimensions = [
            RiskDimensionScore(
                dimension="case_merit", score=merit_score,
                weight=RISK_DIMENSION_WEIGHTS["case_merit"],
                weighted_score=round(merit_score * RISK_DIMENSION_WEIGHTS["case_merit"], 4),
                factors_evaluated=["legal_theory_strength", "factual_support", "burden_of_proof"],
                key_finding=merit_finding,
            ),
            RiskDimensionScore(
                dimension="damages_exposure", score=damages_score,
                weight=RISK_DIMENSION_WEIGHTS["damages_exposure"],
                weighted_score=round(damages_score * RISK_DIMENSION_WEIGHTS["damages_exposure"], 4),
                factors_evaluated=["amount_in_controversy", "punitive_risk", "treble_damages"],
                key_finding=damages_finding,
            ),
            RiskDimensionScore(
                dimension="jurisdiction_risk", score=jurisdiction_score,
                weight=RISK_DIMENSION_WEIGHTS["jurisdiction_risk"],
                weighted_score=round(jurisdiction_score * RISK_DIMENSION_WEIGHTS["jurisdiction_risk"], 4),
                factors_evaluated=["venue_favorability", "jury_tendency", "local_rules"],
                key_finding=jur_finding,
            ),
            RiskDimensionScore(
                dimension="discovery_cost", score=discovery_score,
                weight=RISK_DIMENSION_WEIGHTS["discovery_cost"],
                weighted_score=round(discovery_score * RISK_DIMENSION_WEIGHTS["discovery_cost"], 4),
                factors_evaluated=["document_volume", "complexity", "expert_needs"],
                key_finding=disc_finding,
            ),
            RiskDimensionScore(
                dimension="settlement_pressure", score=settlement_score,
                weight=RISK_DIMENSION_WEIGHTS["settlement_pressure"],
                weighted_score=round(settlement_score * RISK_DIMENSION_WEIGHTS["settlement_pressure"], 4),
                factors_evaluated=["cost_ratio", "publicity_risk", "business_disruption"],
                key_finding=settle_finding,
            ),
            RiskDimensionScore(
                dimension="regulatory_escalation", score=regulatory_score,
                weight=RISK_DIMENSION_WEIGHTS["regulatory_escalation"],
                weighted_score=round(regulatory_score * RISK_DIMENSION_WEIGHTS["regulatory_escalation"], 4),
                factors_evaluated=["agency_involvement", "enforcement_trends"],
                key_finding=reg_finding,
            ),
        ]

        key_risk_factors = self._extract_key_risk_factors(
            doctrines, risk_dimensions, risk_level
        )
        recommended_actions = self._generate_recommendations(
            risk_level, risk_dimensions, doctrines, req.litigation_type
        )
        analysis_summary = self._generate_summary(
            req.litigation_type, req.jurisdiction, composite, risk_level,
            len(doctrines), decomposition,
        )

        record_risk_assessment(
            trace_id=trace_id,
            litigation_type=req.litigation_type,
            merit_score=merit_score,
            damages_score=damages_score,
            jurisdiction_score=jurisdiction_score,
            discovery_score=discovery_score,
            settlement_score=settlement_score,
            regulatory_score=regulatory_score,
            composite_score=composite,
            risk_level=risk_level,
            confidence=0.7,
            factors_evaluated=sum(len(d.factors_evaluated) for d in risk_dimensions),
        )

        return {
            "composite_risk_score": composite,
            "risk_level": risk_level,
            "risk_dimensions": risk_dimensions,
            "all_doctrine_keys": all_keys,
            "precedent_citations": precedents,
            "analysis_summary": analysis_summary,
            "key_risk_factors": key_risk_factors,
            "recommended_actions": recommended_actions,
            "damages_estimate": damages_estimate,
            "settlement_analysis": settlement_result,
            "discovery_cost": discovery_estimate,
            "jurisdiction_analysis": jurisdiction_assessment,
            "fact_fragility": fragility_results,
            "decomposition": decomposition,
        }

    def _extract_key_risk_factors(
        self,
        doctrines: List[DoctrineBlock],
        dimensions: List[RiskDimensionScore],
        risk_level: str,
    ) -> List[str]:
        """Extract the top risk factors from the analysis."""
        factors: List[str] = []

        sorted_dims = sorted(dimensions, key=lambda d: d.score, reverse=True)
        for dim in sorted_dims[:3]:
            factors.append(
                f"{dim.dimension.replace('_', ' ').title()}: {dim.key_finding}"
            )

        for d in doctrines[:3]:
            if d.risk_severity in (RiskSeverity.CRITICAL, RiskSeverity.HIGH):
                factors.append(
                    f"Doctrine risk ({d.risk_severity.value}): {d.topic}"
                )

        return factors[:8]

    def _generate_recommendations(
        self,
        risk_level: str,
        dimensions: List[RiskDimensionScore],
        doctrines: List[DoctrineBlock],
        litigation_type: str,
    ) -> List[str]:
        """Generate actionable recommendations based on risk assessment."""
        recs: List[str] = []

        if risk_level == "critical":
            recs.append("Immediate legal counsel engagement recommended for critical risk level")
            recs.append("Consider early settlement discussions to limit exposure")
            recs.append("Implement litigation hold and evidence preservation protocols")
        elif risk_level == "high":
            recs.append("Engage specialized litigation counsel for detailed case evaluation")
            recs.append("Prepare preliminary defense strategy and identify key witnesses")
            recs.append("Assess insurance coverage and provide timely notice to carriers")
        elif risk_level == "medium":
            recs.append("Monitor situation and prepare contingency litigation plan")
            recs.append("Review relevant contracts and documentation for defensive posture")
        else:
            recs.append("Document risk assessment for file; monitor for changes in circumstances")

        for dim in dimensions:
            if dim.dimension == "discovery_cost" and dim.score > 0.6:
                recs.append("Consider early case management conference to narrow discovery scope")
            if dim.dimension == "settlement_pressure" and dim.score > 0.7:
                recs.append("Evaluate mediation or early neutral evaluation to explore settlement")
            if dim.dimension == "regulatory_escalation" and dim.score > 0.5:
                recs.append("Assess voluntary disclosure options with regulatory counsel")

        for d in doctrines:
            if d.statute_of_limitations_years and d.statute_of_limitations_years <= 1.0:
                recs.append(
                    f"Urgent: Short statute of limitations ({d.statute_of_limitations_years} years) "
                    f"for {d.topic}. Verify filing deadlines immediately."
                )
                break

        return recs[:10]

    def _generate_summary(
        self,
        litigation_type: str,
        jurisdiction: str,
        composite: float,
        risk_level: str,
        doctrine_count: int,
        decomposition: Dict[str, Any],
    ) -> str:
        """Generate a narrative analysis summary."""
        primary_count = len(decomposition.get("primary_doctrines", []))
        interaction_count = len(decomposition.get("interaction_edges", []))

        summary = (
            f"Litigation risk assessment for {litigation_type.replace('_', ' ')} in {jurisdiction} "
            f"jurisdiction yields a composite risk score of {composite:.2f} ({risk_level} risk). "
            f"Analysis evaluated {doctrine_count} applicable doctrines across "
            f"{primary_count} primary domains with {interaction_count} cross-doctrine "
            f"interactions identified. "
        )

        if risk_level in ("critical", "high"):
            summary += (
                "Significant risk factors warrant immediate attention and engagement "
                "of specialized litigation counsel. Early case assessment and "
                "preservation protocols are strongly recommended."
            )
        elif risk_level == "medium":
            summary += (
                "Moderate risk factors present. Recommend monitoring and contingency "
                "planning with periodic reassessment as facts develop."
            )
        else:
            summary += (
                "Risk profile is within acceptable parameters. Standard monitoring "
                "and documentation recommended."
            )

        return summary


# ============================================================================
# EPISTEMIC GUARDRAILS
# ============================================================================

class EpistemicGuardrails:
    """Enforces epistemic hygiene on all engine outputs."""

    def __init__(self) -> None:
        self._violations_blocked: int = 0
        logger.info("EpistemicGuardrails initialized")

    def check_text(self, text: str) -> Tuple[str, List[str]]:
        """Check text for banned phrases and return sanitized version with warnings."""
        warnings: List[str] = []
        sanitized = text
        text_lower = text.lower()

        for banned in BANNED_PHRASES:
            if banned in text_lower:
                sanitized = sanitized.replace(banned, "[ASSERTION REMOVED - EXCEEDS EPISTEMIC BOUNDS]")
                warnings.append(f"Removed banned phrase: '{banned}'")
                self._violations_blocked += 1

        return sanitized, warnings

    def generate_disclosures(
        self, jurisdiction: str, analysis_date: Optional[str] = None,
    ) -> EpistemicDisclosure:
        """Generate required epistemic disclosures for a response."""
        date_str = analysis_date or datetime.now(timezone.utc).strftime("%Y-%m-%d")
        config_disclosures = ENGINE_CONFIG.get("epistemic_guardrails", {}).get(
            "required_disclosures", {}
        )

        return EpistemicDisclosure(
            jurisdiction_variance=config_disclosures.get(
                "jurisdiction_variance",
                f"Litigation outcomes vary significantly by jurisdiction. "
                f"This assessment assumes {jurisdiction} law unless otherwise specified.",
            ).format(jurisdiction=jurisdiction),
            not_legal_advice=config_disclosures.get(
                "not_legal_advice",
                "This risk assessment is for informational and planning purposes. "
                "Consult qualified litigation counsel for case-specific legal advice.",
            ),
            temporal_caveat=config_disclosures.get(
                "temporal_caveat",
                f"Legal standards and judicial precedent evolve. "
                f"This assessment reflects the legal landscape as of {date_str}.",
            ).format(analysis_date=date_str),
            fact_dependency=config_disclosures.get(
                "fact_dependency",
                "Risk conclusions depend on the accuracy and completeness of the facts "
                "provided. Undisclosed facts may materially alter the assessment.",
            ),
        )

    @property
    def violations_blocked(self) -> int:
        """Count of banned phrase violations blocked."""
        return self._violations_blocked


# ============================================================================
# (1) THREE-LAYER RESPONSE ORCHESTRATOR  +  (2) RESPONSE MODES
# ============================================================================

class ThreeLayerOrchestrator:
    """Orchestrates responses across Quick/Standard/Deep layers with DET/EF/HYBRID modes."""

    def __init__(
        self,
        cache: DoctrineCacheManager,
        normalizer: SemanticNormalizer,
        search_engine: SearchEngine,
        hardener: AuthorityHardener,
        stratifier: ConfidenceStratifier,
        decomposer: MultiDoctrineDecomposer,
        deep_analyzer: DeepAnalyzer,
        hasher: DeterminismHasher,
        guardrails: EpistemicGuardrails,
        telemeter: EngineTelemeter,
        fragility_scorer: FactFragilityScorer,
        metrics: MetricsCollector,
    ) -> None:
        self._cache = cache
        self._normalizer = normalizer
        self._search = search_engine
        self._hardener = hardener
        self._stratifier = stratifier
        self._decomposer = decomposer
        self._deep = deep_analyzer
        self._hasher = hasher
        self._guardrails = guardrails
        self._telemetry = telemeter
        self._fragility = fragility_scorer
        self._metrics = metrics
        logger.info("ThreeLayerOrchestrator initialized")

    def process(self, req: LitigationRiskRequest) -> LitigationRiskResponse:
        """Process a full litigation risk request through the three-layer pipeline."""
        start_time = time.time()
        trace_id, _ = self._telemetry.start_trace(
            req.case_description[:200], req.litigation_type, req.jurisdiction,
            req.response_mode.value,
        )
        self._metrics.increment("total_requests")

        try:
            if req.analysis_depth == AnalysisDepthEnum.QUICK:
                result = self._quick_layer(req, trace_id)
                response_layer = "doctrine"
            elif req.analysis_depth == AnalysisDepthEnum.STANDARD:
                result = self._standard_layer(req, trace_id)
                response_layer = "semantic"
            else:
                result = self._deep_layer(req, trace_id)
                response_layer = "deep"

            latency_ms = (time.time() - start_time) * 1000
            self._metrics.observe("response_latency_ms", latency_ms)
            self._metrics.increment(f"layer_{response_layer}")

            det_hash = self._hasher.hash_response(
                req.case_description,
                req.litigation_type,
                req.jurisdiction,
                result.get("all_doctrine_keys", []),
                result["composite_risk_score"],
                result.get("confidence", 0.5),
            )

            disclosures = self._guardrails.generate_disclosures(req.jurisdiction)
            summary, summary_warnings = self._guardrails.check_text(
                result.get("analysis_summary", "")
            )
            all_warnings = result.get("warnings", []) + summary_warnings

            self._telemetry.end_trace(
                trace_id=trace_id,
                start_time=start_time,
                query_text=req.case_description[:200],
                litigation_type=req.litigation_type,
                jurisdiction=req.jurisdiction,
                mode=req.response_mode.value,
                layer=response_layer,
                doctrine_keys=result.get("all_doctrine_keys", []),
                risk_score=result["composite_risk_score"],
                confidence=result.get("confidence", 0.5),
                determinism_hash=det_hash,
                warnings=all_warnings,
            )

            return LitigationRiskResponse(
                trace_id=trace_id,
                timestamp=datetime.now(timezone.utc).isoformat(),
                response_mode=req.response_mode.value,
                analysis_depth=req.analysis_depth.value,
                response_layer=response_layer,
                litigation_type=req.litigation_type,
                jurisdiction=req.jurisdiction,
                composite_risk_score=result["composite_risk_score"],
                risk_level=result["risk_level"],
                confidence=result.get("confidence", 0.5),
                risk_dimensions=result.get("risk_dimensions", []),
                matched_doctrines=result.get("all_doctrine_keys", []),
                precedent_citations=result.get("precedent_citations", []),
                analysis_summary=summary,
                key_risk_factors=result.get("key_risk_factors", []),
                recommended_actions=result.get("recommended_actions", []),
                damages_estimate=result.get("damages_estimate"),
                settlement_analysis=result.get("settlement_analysis"),
                discovery_cost=result.get("discovery_cost"),
                jurisdiction_analysis=result.get("jurisdiction_analysis"),
                fact_fragility=result.get("fact_fragility"),
                epistemic_disclosures=disclosures,
                determinism_hash=det_hash,
                latency_ms=round(latency_ms, 2),
                warnings=all_warnings,
            )

        except Exception as exc:
            latency_ms = (time.time() - start_time) * 1000
            self._metrics.increment("errors")
            error_id = self._telemetry.log_error(
                ErrorDomain.UNKNOWN,
                f"Orchestration error: {str(exc)}",
                trace_id=trace_id,
                exc=exc,
            )
            logger.exception(f"Orchestration failed | trace={trace_id} | error={str(exc)}")
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "Litigation risk assessment failed",
                    "error_id": error_id,
                    "trace_id": trace_id,
                    "message": str(exc),
                },
            )

    def _quick_layer(self, req: LitigationRiskRequest, trace_id: str) -> Dict[str, Any]:
        """Quick doctrine-cache-only analysis (Layer 1)."""
        step_start = time.time()

        norm = self._normalizer.normalize(req.case_description)
        key_terms = self._normalizer.extract_key_terms(req.case_description)

        matched: Dict[str, DoctrineBlock] = {}
        for term in key_terms:
            for block in self._cache.search_by_keyword(term):
                matched[block.key] = block

        if not matched:
            for kw in req.case_description.lower().split()[:20]:
                for block in self._cache.search_by_keyword(kw):
                    matched[block.key] = block
                    if len(matched) >= 3:
                        break
                if len(matched) >= 3:
                    break

        doctrines = list(matched.values())
        all_keys = sorted(matched.keys())

        raw_risk = 0.5
        if doctrines:
            severity_scores = {
                RiskSeverity.CRITICAL: 0.9,
                RiskSeverity.HIGH: 0.7,
                RiskSeverity.MEDIUM: 0.5,
                RiskSeverity.LOW: 0.3,
                RiskSeverity.NEGLIGIBLE: 0.1,
            }
            risk_values = [severity_scores.get(d.risk_severity, 0.5) for d in doctrines]
            raw_risk = sum(risk_values) / len(risk_values)

        raw_confidence = 0.5
        hardened_risk, hardened_conf, authority_tier, warnings = self._hardener.harden_response(
            doctrines, raw_risk, raw_confidence,
        )

        _, risk_level = RiskScoringEngine(
            self._cache, self._normalizer, self._search
        ).compute_composite_risk(
            hardened_risk, hardened_risk, hardened_risk,
            hardened_risk, hardened_risk, hardened_risk,
        )

        step_ms = (time.time() - step_start) * 1000
        self._telemetry.log_reasoning_step(
            trace_id, 1, "quick_doctrine_match",
            {"terms": key_terms[:10]},
            {"matched": len(matched), "risk": hardened_risk},
            step_ms,
        )

        return {
            "composite_risk_score": hardened_risk,
            "risk_level": risk_level,
            "confidence": hardened_conf,
            "all_doctrine_keys": all_keys,
            "risk_dimensions": [],
            "precedent_citations": [],
            "analysis_summary": (
                f"Quick triage: {len(matched)} doctrines matched, "
                f"risk={hardened_risk:.2f} ({risk_level}), "
                f"authority_tier={authority_tier}"
            ),
            "key_risk_factors": [d.topic for d in doctrines[:5]],
            "recommended_actions": [
                "Quick triage complete. Upgrade to STANDARD or DEEP for detailed analysis."
            ],
            "warnings": warnings,
        }

    def _standard_layer(self, req: LitigationRiskRequest, trace_id: str) -> Dict[str, Any]:
        """Standard semantic-search-enhanced analysis (Layer 2)."""
        step_start = time.time()

        decomposition = self._decomposer.decompose(
            req.case_description, req.litigation_type, req.claims,
        )

        search_results = self._search.search(
            req.case_description[:500],
            litigation_type=req.litigation_type,
            jurisdiction=req.jurisdiction,
            max_results=15,
        )

        matched_keys = list(decomposition["all_matched_keys"])
        for sr in search_results:
            if sr.doc_type == "doctrines" and sr.doc_id.startswith("doctrine_"):
                dk = sr.doc_id.replace("doctrine_", "")
                if dk not in matched_keys:
                    matched_keys.append(dk)

        doctrines = [self._cache.get(k) for k in matched_keys if self._cache.get(k)]
        facts = req.facts or []
        claims = req.claims or []

        fact_avg_strength = (
            sum(f.strength for f in facts) / len(facts) if facts else 0.3
        )
        stratified = self._stratifier.stratify(
            doctrines,
            fact_count=len(facts),
            fact_avg_strength=fact_avg_strength,
            jurisdiction_specificity=0.6,
            temporal_relevance=0.7,
        )

        raw_risk = 0.5
        if doctrines:
            severity_scores = {
                RiskSeverity.CRITICAL: 0.9, RiskSeverity.HIGH: 0.7,
                RiskSeverity.MEDIUM: 0.5, RiskSeverity.LOW: 0.3,
                RiskSeverity.NEGLIGIBLE: 0.1,
            }
            risk_values = [severity_scores.get(d.risk_severity, 0.5) for d in doctrines]
            raw_risk = sum(risk_values) / len(risk_values)

        hardened_risk, hardened_conf, authority_tier, auth_warnings = self._hardener.harden_response(
            doctrines, raw_risk, stratified["composite"],
        )

        _, risk_level = RiskScoringEngine(
            self._cache, self._normalizer, self._search
        ).compute_composite_risk(
            hardened_risk, hardened_risk * 0.9, hardened_risk * 0.8,
            hardened_risk * 0.7, hardened_risk * 0.6, hardened_risk * 0.5,
        )

        precedents: List[PrecedentCitation] = []
        if req.include_citations:
            seen: Set[str] = set()
            for d in doctrines:
                for p in d.precedents:
                    if p.citation not in seen:
                        precedents.append(PrecedentCitation(
                            case_name=p.case_name, citation=p.citation,
                            year=p.year, court=p.court,
                            holding=p.holding, relevance_score=p.relevance_score,
                        ))
                        seen.add(p.citation)

        step_ms = (time.time() - step_start) * 1000
        self._telemetry.log_reasoning_step(
            trace_id, 1, "standard_semantic_analysis",
            {"decomposition_keys": len(matched_keys), "search_results": len(search_results)},
            {"risk": hardened_risk, "confidence": hardened_conf, "risk_level": risk_level},
            step_ms,
        )

        return {
            "composite_risk_score": hardened_risk,
            "risk_level": risk_level,
            "confidence": hardened_conf,
            "all_doctrine_keys": matched_keys,
            "risk_dimensions": [],
            "precedent_citations": precedents,
            "analysis_summary": (
                f"Standard analysis: {len(matched_keys)} doctrines evaluated, "
                f"risk={hardened_risk:.2f} ({risk_level}), "
                f"confidence={hardened_conf:.2f} ({stratified['tier']}), "
                f"authority_tier={authority_tier}"
            ),
            "key_risk_factors": [d.topic for d in doctrines[:5] if d],
            "recommended_actions": [
                "Standard analysis complete. For full damages/settlement/discovery modeling, "
                "upgrade to DEEP analysis depth."
            ],
            "warnings": auth_warnings,
        }

    def _deep_layer(self, req: LitigationRiskRequest, trace_id: str) -> Dict[str, Any]:
        """Deep multi-source analysis (Layer 3)."""
        result = self._deep.analyze(req, trace_id)

        doctrines = [
            self._cache.get(k) for k in result.get("all_doctrine_keys", [])
            if self._cache.get(k)
        ]
        facts = req.facts or []
        fact_avg_strength = (
            sum(f.strength for f in facts) / len(facts) if facts else 0.3
        )

        stratified = self._stratifier.stratify(
            doctrines,
            fact_count=len(facts),
            fact_avg_strength=fact_avg_strength,
            jurisdiction_specificity=0.7,
            temporal_relevance=0.8,
        )

        hardened_risk, hardened_conf, authority_tier, auth_warnings = self._hardener.harden_response(
            doctrines, result["composite_risk_score"], stratified["composite"],
        )

        result["composite_risk_score"] = hardened_risk
        result["confidence"] = hardened_conf
        result["warnings"] = result.get("warnings", []) + auth_warnings

        return result

    def quick_triage(self, req: QuickTriageRequest) -> QuickTriageResponse:
        """Fast triage endpoint."""
        start_time = time.time()
        trace_id = str(uuid.uuid4())

        norm = self._normalizer.normalize(req.case_summary)
        key_terms = self._normalizer.extract_key_terms(req.case_summary)

        matched: Dict[str, DoctrineBlock] = {}
        for term in key_terms:
            for block in self._cache.search_by_keyword(term):
                matched[block.key] = block

        doctrines = list(matched.values())
        raw_risk = 0.5
        if doctrines:
            sev = {
                RiskSeverity.CRITICAL: 0.9, RiskSeverity.HIGH: 0.7,
                RiskSeverity.MEDIUM: 0.5, RiskSeverity.LOW: 0.3,
                RiskSeverity.NEGLIGIBLE: 0.1,
            }
            raw_risk = sum(sev.get(d.risk_severity, 0.5) for d in doctrines) / len(doctrines)

        hardened_risk, conf, _, _ = self._hardener.harden_response(doctrines, raw_risk, 0.5)

        if hardened_risk >= 0.8:
            risk_level = "critical"
        elif hardened_risk >= 0.6:
            risk_level = "high"
        elif hardened_risk >= 0.4:
            risk_level = "medium"
        elif hardened_risk >= 0.2:
            risk_level = "low"
        else:
            risk_level = "negligible"

        top_risks = [d.topic for d in doctrines[:5]]

        if risk_level in ("critical", "high"):
            recommended_depth = "DEEP"
        elif risk_level == "medium":
            recommended_depth = "STANDARD"
        else:
            recommended_depth = "QUICK"

        det_hash = self._hasher.hash_response(
            req.case_summary, req.litigation_type, req.jurisdiction,
            sorted(matched.keys()), hardened_risk, conf,
        )

        latency_ms = (time.time() - start_time) * 1000
        self._metrics.increment("triage_requests")

        return QuickTriageResponse(
            trace_id=trace_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            litigation_type=req.litigation_type,
            risk_level=risk_level,
            risk_score=round(hardened_risk, 4),
            confidence=round(conf, 4),
            top_risks=top_risks,
            recommended_depth=recommended_depth,
            determinism_hash=det_hash,
            latency_ms=round(latency_ms, 2),
        )


# ============================================================================
# (17) FASTAPI SERVER + (12) HEALTH ENDPOINT + (18) LOGURU LOGGING
# ============================================================================

# Component singletons
_cache_manager = DoctrineCacheManager()
_normalizer = SemanticNormalizer()
_search_engine = SearchEngine()
_hardener = AuthorityHardener()
_stratifier = ConfidenceStratifier()
_hasher = DeterminismHasher()
_guardrails = EpistemicGuardrails()
_telemeter = EngineTelemeter()
_drift_watcher = DoctrineDriftWatcher(_cache_manager)
_metrics = MetricsCollector()
_zoned = ZonedAnalyzer()
_fragility_scorer = FactFragilityScorer()
_damages_estimator = DamagesEstimator()
_settlement_analyzer = SettlementAnalyzer()
_discovery_modeler = DiscoveryCostModeler()
_jurisdiction_analyzer = JurisdictionAnalyzer(_zoned)
_decomposer = MultiDoctrineDecomposer(_cache_manager, _normalizer)
_deep_analyzer = DeepAnalyzer(
    _cache_manager, _search_engine, _normalizer, _decomposer,
    RiskScoringEngine(_cache_manager, _normalizer, _search_engine),
    _damages_estimator, _settlement_analyzer, _discovery_modeler,
    _jurisdiction_analyzer, _fragility_scorer, _zoned,
)
_orchestrator = ThreeLayerOrchestrator(
    _cache_manager, _normalizer, _search_engine, _hardener,
    _stratifier, _decomposer, _deep_analyzer, _hasher,
    _guardrails, _telemeter, _fragility_scorer, _metrics,
)

_engine_start_time: float = time.time()


@asynccontextmanager
async def lifespan(application: FastAPI):
    """Application lifespan handler."""
    logger.info(
        f"LG05 Litigation Risk Engine starting | port={ENGINE_PORT} | "
        f"doctrines={get_doctrine_count()} | version={ENGINE_VERSION}"
    )
    yield
    logger.info("LG05 Litigation Risk Engine shutting down")


app = FastAPI(
    title="LG05 Litigation Risk Engine",
    description=(
        "Production-grade litigation risk assessment engine with deterministic "
        "case merit scoring, damages estimation, jurisdiction analysis, discovery "
        "cost modeling, settlement valuation, and precedent matching."
    ),
    version=ENGINE_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- ROUTES ---

@app.get("/health", response_model=HealthResponse)
async def health_endpoint() -> HealthResponse:
    """Health check endpoint returning full engine status."""
    return HealthResponse(
        engine_id=ENGINE_ID,
        engine_name=ENGINE_NAME,
        version=ENGINE_VERSION,
        status="operational",
        port=ENGINE_PORT,
        mode=MODE,
        tier=TIER,
        tier_name=TIER_NAME,
        authority_level=AUTHORITY_LEVEL,
        uptime_seconds=round(time.time() - _engine_start_time, 1),
        doctrine_count=get_doctrine_count(),
        semantic_mappings=TOTAL_MAPPINGS,
        search_index_docs=_search_engine._index.document_count,
        telemetry_session=_telemeter.session_id,
        telemetry_events=_telemeter.event_count,
        performance=_telemeter.get_performance(),
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


@app.post("/analyze", response_model=LitigationRiskResponse)
async def analyze_litigation_risk(req: LitigationRiskRequest) -> LitigationRiskResponse:
    """Full litigation risk assessment endpoint."""
    _metrics.increment("analyze_requests")
    return _orchestrator.process(req)


@app.post("/triage", response_model=QuickTriageResponse)
async def quick_triage(req: QuickTriageRequest) -> QuickTriageResponse:
    """Quick triage endpoint for fast risk screening."""
    return _orchestrator.quick_triage(req)


@app.post("/damages/estimate")
async def estimate_damages(req: DamagesEstimationRequest) -> Dict[str, Any]:
    """Standalone damages estimation endpoint."""
    _metrics.increment("damages_requests")
    doctrines_matched: List[DoctrineBlock] = []
    for block in DOCTRINE_CACHE.values():
        if block.category.value in (req.litigation_type, "tort_liability", "contract_dispute"):
            doctrines_matched.append(block)

    results = _damages_estimator.estimate(
        litigation_type=req.litigation_type,
        claims=req.claims,
        amount_in_controversy=req.amount_in_controversy,
        doctrines=doctrines_matched,
        punitive_likely=req.punitive_likely,
        attorneys_fees_recoverable=req.attorneys_fees_recoverable,
        class_action=req.class_action,
        class_size=req.class_size,
    )

    return {
        "engine_id": ENGINE_ID,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "litigation_type": req.litigation_type,
        "damages_ranges": [r.model_dump() for r in results],
    }


@app.post("/settlement/analyze")
async def analyze_settlement(req: SettlementAnalysisRequest) -> Dict[str, Any]:
    """Standalone settlement valuation endpoint."""
    _metrics.increment("settlement_requests")
    result = _settlement_analyzer.analyze(
        liability_probability=req.liability_probability,
        damages_low=req.damages_low,
        damages_high=req.damages_high,
        litigation_cost=req.litigation_cost_estimate,
        time_to_trial_months=req.time_to_trial_months,
        publicity_risk=req.publicity_risk,
        business_disruption=req.business_disruption,
        precedent_value=req.precedent_value,
    )
    return {
        "engine_id": ENGINE_ID,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "settlement_valuation": result.model_dump(),
    }


@app.post("/discovery/cost")
async def estimate_discovery_cost(req: DiscoveryCostRequest) -> Dict[str, Any]:
    """Standalone discovery cost estimation endpoint."""
    _metrics.increment("discovery_requests")
    result = _discovery_modeler.estimate(
        document_volume=req.document_volume_estimate,
        custodian_count=req.custodian_count,
        deposition_count=req.deposition_count,
        expert_count=req.expert_witness_count,
        e_discovery=req.e_discovery_needed,
        international=req.international_discovery,
        privilege_complexity=req.privilege_review_complexity,
    )
    return {
        "engine_id": ENGINE_ID,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "discovery_cost_estimate": result.model_dump(),
    }


@app.post("/jurisdiction/analyze")
async def analyze_jurisdiction(req: JurisdictionAnalysisRequest) -> Dict[str, Any]:
    """Standalone jurisdiction analysis endpoint."""
    _metrics.increment("jurisdiction_requests")
    doctrines: List[DoctrineBlock] = []
    for block in DOCTRINE_CACHE.values():
        if block.category == LitigationCategory.CIVIL_PROCEDURE:
            doctrines.append(block)

    result = _jurisdiction_analyzer.analyze(
        jurisdiction=req.jurisdiction,
        litigation_type=req.litigation_type,
        defendant_state=req.defendant_state,
        plaintiff_state=req.plaintiff_state,
        forum_selection_clause=req.forum_selection_clause,
        amount_in_controversy=req.amount_in_controversy,
        doctrines=doctrines,
    )
    return {
        "engine_id": ENGINE_ID,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "jurisdiction_assessment": result.model_dump(),
    }


@app.post("/doctrines/search")
async def search_doctrines_endpoint(req: DoctrineSearchRequest) -> Dict[str, Any]:
    """Search the doctrine library."""
    _metrics.increment("doctrine_search_requests")
    results = _search_engine.search(
        req.query,
        max_results=req.max_results,
        scope=SearchScope.DOCTRINES,
    )
    return {
        "engine_id": ENGINE_ID,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "query": req.query,
        "results": [
            {
                "doc_id": r.doc_id,
                "title": r.title,
                "snippet": r.snippet,
                "relevance_score": r.relevance_score,
                "litigation_type": r.litigation_type,
                "risk_level": r.risk_level,
                "match_terms": r.match_terms,
            }
            for r in results
        ],
        "total_results": len(results),
    }


@app.get("/doctrines/list")
async def list_doctrines() -> Dict[str, Any]:
    """List all available doctrines."""
    doctrines = []
    for key in sorted(DOCTRINE_CACHE.keys()):
        block = DOCTRINE_CACHE[key]
        doctrines.append({
            "key": key,
            "topic": block.topic,
            "category": block.category.value,
            "authority": block.authority.value,
            "confidence": block.confidence.value,
            "risk_severity": block.risk_severity.value,
            "keywords": block.keywords[:5],
            "precedent_count": len(block.precedents),
        })
    return {
        "engine_id": ENGINE_ID,
        "total_doctrines": len(doctrines),
        "doctrines": doctrines,
    }


@app.get("/doctrines/{key}")
async def get_doctrine_detail(key: str) -> Dict[str, Any]:
    """Get detailed information about a specific doctrine."""
    block = _cache_manager.get(key)
    if not block:
        raise HTTPException(status_code=404, detail=f"Doctrine '{key}' not found")
    interactions = _cache_manager.get_interactions(key)
    return {
        "engine_id": ENGINE_ID,
        "doctrine": {
            "key": block.key,
            "topic": block.topic,
            "category": block.category.value,
            "keywords": block.keywords,
            "conclusion_template": block.conclusion_template,
            "analysis_framework": block.analysis_framework,
            "key_factors": block.key_factors,
            "authority": block.authority.value,
            "confidence": block.confidence.value,
            "risk_severity": block.risk_severity.value,
            "jurisdiction_notes": block.jurisdiction_notes,
            "risk_multipliers": block.risk_multipliers,
            "damages_guidance": block.damages_guidance,
            "settlement_factors": block.settlement_factors,
            "statute_of_limitations_years": block.statute_of_limitations_years,
            "burden_of_proof": block.burden_of_proof,
            "precedents": [
                {
                    "case_name": p.case_name,
                    "citation": p.citation,
                    "year": p.year,
                    "court": p.court,
                    "holding": p.holding,
                }
                for p in block.precedents
            ],
        },
        "interactions": [
            {
                "source": i.source_key,
                "target": i.target_key,
                "relationship": i.relationship,
                "strength": i.strength,
                "description": i.description,
            }
            for i in interactions
        ],
    }


@app.post("/compare")
async def compare_cases_endpoint(req: CaseComparisonRequest) -> Dict[str, Any]:
    """Compare two cases for similarity and risk differentials."""
    _metrics.increment("comparison_requests")

    norm_a = _normalizer.normalize(req.case_a_description)
    norm_b = _normalizer.normalize(req.case_b_description)

    terms_a = _normalizer.extract_key_terms(req.case_a_description)
    terms_b = _normalizer.extract_key_terms(req.case_b_description)

    common = set(terms_a) & set(terms_b)
    only_a = set(terms_a) - set(terms_b)
    only_b = set(terms_b) - set(terms_a)

    similarity = trigram_similarity(norm_a.normalized, norm_b.normalized)

    return {
        "engine_id": ENGINE_ID,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "similarity_score": round(similarity, 4),
        "common_terms": sorted(common),
        "unique_to_case_a": sorted(only_a),
        "unique_to_case_b": sorted(only_b),
        "case_a_hash": norm_a.text_hash,
        "case_b_hash": norm_b.text_hash,
    }


@app.get("/drift/check")
async def check_drift() -> Dict[str, Any]:
    """Run a doctrine drift check."""
    return _drift_watcher.check_drift()


@app.get("/drift/coverage")
async def get_coverage() -> Dict[str, Any]:
    """Get doctrine coverage analysis."""
    return _drift_watcher.get_coverage_gaps()


@app.get("/drift/staleness")
async def get_staleness() -> Dict[str, Any]:
    """Get doctrine staleness report."""
    return _drift_watcher.get_staleness_report()


@app.get("/metrics")
async def get_metrics() -> Dict[str, Any]:
    """Get all engine metrics."""
    return {
        "engine_id": ENGINE_ID,
        "engine_metrics": _metrics.get_all_metrics(),
        "cache_stats": _cache_manager.get_stats(),
        "search_stats": _search_engine.get_stats(),
        "normalizer_stats": _normalizer.get_stats(),
        "hardener_stats": _hardener.get_hardening_stats(),
        "drift_stats": _drift_watcher.get_stats(),
        "hasher_stats": {"hash_count": _hasher.hash_count},
        "guardrails_stats": {"violations_blocked": _guardrails.violations_blocked},
        "performance": _telemeter.get_performance(),
    }


@app.get("/zones/{jurisdiction}")
async def get_zone_profile(jurisdiction: str) -> Dict[str, Any]:
    """Get zone profile for a jurisdiction."""
    return _zoned.analyze_zone(jurisdiction, "general")


@app.get("/zones/compare/{zone_a}/{zone_b}")
async def compare_zones(zone_a: str, zone_b: str) -> Dict[str, Any]:
    """Compare two jurisdictional zones."""
    return _zoned.compare_zones(zone_a, zone_b, "general")


@app.post("/sol/analyze")
async def analyze_sol(req: StatuteOfLimitationsRequest) -> Dict[str, Any]:
    """Analyze statute of limitations for a case."""
    _metrics.increment("sol_requests")
    matched: List[DoctrineBlock] = []
    for block in DOCTRINE_CACHE.values():
        if block.statute_of_limitations_years is not None:
            for kw in block.keywords:
                if kw in req.litigation_type.lower() or req.litigation_type.lower() in kw:
                    matched.append(block)
                    break

    sol_years = None
    doctrine_key = None
    for d in matched:
        if d.statute_of_limitations_years is not None:
            sol_years = d.statute_of_limitations_years
            doctrine_key = d.key
            break

    expired = False
    days_remaining = None
    if sol_years and req.date_of_injury:
        try:
            injury_date = datetime.fromisoformat(req.date_of_injury)
            deadline = injury_date.replace(
                year=injury_date.year + int(sol_years),
                month=injury_date.month,
            )
            now = datetime.now(timezone.utc)
            if now.tzinfo is None:
                now = now.replace(tzinfo=timezone.utc)
            if injury_date.tzinfo is None:
                injury_date = injury_date.replace(tzinfo=timezone.utc)
                deadline = deadline.replace(tzinfo=timezone.utc)
            delta = deadline - now
            days_remaining = delta.days
            expired = days_remaining < 0
        except (ValueError, OverflowError):
            days_remaining = None

    return {
        "engine_id": ENGINE_ID,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "litigation_type": req.litigation_type,
        "jurisdiction": req.jurisdiction,
        "statute_of_limitations_years": sol_years,
        "doctrine_source": doctrine_key,
        "expired": expired,
        "days_remaining": days_remaining,
        "tolling_events": req.tolling_events,
        "discovery_rule_note": (
            "Discovery rule may delay accrual if injury was not immediately apparent. "
            "Verify whether jurisdiction applies discovery rule to this claim type."
        ),
    }


@app.get("/audit/trail")
async def get_audit_trail(
    trace_id: Optional[str] = None,
    event_type: Optional[str] = None,
    limit: int = Query(default=50, ge=1, le=500),
) -> Dict[str, Any]:
    """Retrieve audit trail records."""
    tm = get_telemetry()
    records = tm.audit_db.get_audit_trail(
        trace_id=trace_id, event_type=event_type, limit=limit,
    )
    return {
        "engine_id": ENGINE_ID,
        "total_records": len(records),
        "records": records,
    }


@app.get("/insurance/coverage/{litigation_type}")
async def assess_insurance_coverage(litigation_type: str) -> Dict[str, Any]:
    """Assess insurance coverage for a litigation type."""
    _metrics.increment("insurance_requests")
    return {
        "engine_id": ENGINE_ID,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        **_insurance_analyzer.assess_coverage(litigation_type),
    }


@app.get("/sol/lookup/{litigation_type}/{jurisdiction}")
async def lookup_sol(litigation_type: str, jurisdiction: str) -> Dict[str, Any]:
    """Look up statute of limitations for litigation type and jurisdiction."""
    _metrics.increment("sol_lookup_requests")
    sol_years = _sol_tracker.get_sol(litigation_type, jurisdiction)
    repose = _sol_tracker.REPOSE_PERIODS.get(litigation_type)
    return {
        "engine_id": ENGINE_ID,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "litigation_type": litigation_type,
        "jurisdiction": jurisdiction,
        "statute_of_limitations_years": sol_years,
        "repose_period_years": repose,
        "tolling_doctrines_available": list(_sol_tracker.TOLLING_DOCTRINES.keys()),
    }


@app.post("/sol/check-expiration")
async def check_sol_expiration(
    litigation_type: str = "breach_of_contract",
    jurisdiction: str = "federal",
    injury_date: str = "2024-01-01",
    discovery_date: Optional[str] = None,
) -> Dict[str, Any]:
    """Check whether statute of limitations has expired for a claim."""
    _metrics.increment("sol_expiration_requests")
    result = _sol_tracker.check_expiration(
        litigation_type=litigation_type,
        jurisdiction=jurisdiction,
        injury_date=injury_date,
        discovery_date=discovery_date,
    )
    return {"engine_id": ENGINE_ID, **result}


@app.get("/tolling/doctrines")
async def get_tolling_doctrines() -> Dict[str, Any]:
    """Get all available tolling doctrines."""
    return {
        "engine_id": ENGINE_ID,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "tolling_doctrines": _sol_tracker.get_tolling_doctrines(),
        "total_doctrines": len(_sol_tracker.TOLLING_DOCTRINES),
    }


@app.get("/")
async def root() -> Dict[str, Any]:
    """Root endpoint with engine info."""
    return {
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "version": ENGINE_VERSION,
        "status": "operational",
        "port": ENGINE_PORT,
        "tier": TIER,
        "tier_name": TIER_NAME,
        "mode": MODE,
        "endpoints": [
            "/health",
            "/analyze",
            "/triage",
            "/damages/estimate",
            "/settlement/analyze",
            "/discovery/cost",
            "/jurisdiction/analyze",
            "/doctrines/search",
            "/doctrines/list",
            "/doctrines/{key}",
            "/compare",
            "/drift/check",
            "/drift/coverage",
            "/drift/staleness",
            "/metrics",
            "/zones/{jurisdiction}",
            "/zones/compare/{zone_a}/{zone_b}",
            "/sol/analyze",
            "/sol/lookup/{litigation_type}/{jurisdiction}",
            "/sol/check-expiration",
            "/tolling/doctrines",
            "/insurance/coverage/{litigation_type}",
            "/audit/trail",
            "/docs",
        ],
    }


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main() -> None:
    """Start the LG05 Litigation Risk Engine."""
    logger.info(
        f"Starting LG05 Litigation Risk Engine | "
        f"port={ENGINE_PORT} | version={ENGINE_VERSION} | "
        f"doctrines={get_doctrine_count()} | mappings={TOTAL_MAPPINGS}"
    )
    uvicorn.run(
        "engine:app",
        host=ENGINE_HOST,
        port=ENGINE_PORT,
        reload=False,
        log_level="info",
        access_log=True,
    )


if __name__ == "__main__":
    main()
