"""
LG12 Bankruptcy Law Engine - Main FastAPI Engine
====================================================
Production-grade bankruptcy law analysis engine implementing all 20 TIE
components for Chapter 7 liquidation, Chapter 11 reorganization, Chapter 13
wage earner plans, Chapter 12 family farmer, Chapter 15 cross-border,
means test, automatic stay, discharge/dischargeability, exemptions
(federal vs state/TX homestead), preference actions, fraudulent transfers,
proof of claim, plan confirmation, adversary proceedings, reaffirmation
agreements, student loan discharge (Brunner test), tax debt discharge,
lien stripping/cramdown, trustee powers, US Trustee oversight, BAPCPA,
Bankruptcy Code (Title 11 USC), FRBP, and Texas exemptions.

TIE-20 Components:
    1.  three_layer_response
    2.  response_modes (fast, analysis, memo, means_test, plan_review)
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

Port: 8402
Engine: LG12 Bankruptcy Law
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
    DischargeAnalyzer,
    DischargeResult,
    DoctrineSearchIndex,
    ExemptionAnalyzer,
    ExemptionResult,
    FraudulentTransferAnalyzer,
    FraudulentTransferResult,
    MeansTestCalculator,
    MeansTestResult,
    PreferenceAnalyzer,
    PreferenceResult,
    SearchResult,
    compute_query_hash,
    get_discharge_analyzer,
    get_exemption_analyzer,
    get_fraudulent_transfer_analyzer,
    get_means_test_calculator,
    get_preference_analyzer,
    get_search_index,
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
    BankruptcyMetricType,
    CitationLookupType,
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
    record_bk_metric,
    record_citation_lookup,
    record_doctrine_mutation,
    trace_query,
)


# ============================================================================
# CONSTANTS
# ============================================================================

ENGINE_ID: str = "LG12"
ENGINE_NAME: str = "Bankruptcy Law Engine"
ENGINE_VERSION: str = "2.0.0"
ENGINE_PORT: int = 8402
ENGINE_HOST: str = "0.0.0.0"
ENGINE_AUTHORITY: float = 5.0
ENGINE_TIER: str = "LEGAL"
ENGINE_MODE: str = "DET"

CONFIG_PATH: Path = Path(__file__).parent / "config.json"
LOG_DIR: Path = Path(__file__).parent / "logs"
AUDIT_LOG_PATH: Path = LOG_DIR / "audit_trail.jsonl"
DRIFT_REGISTRY_PATH: Path = Path(__file__).parent / "doctrine_drift_registry.json"

BANNED_PHRASES: List[str] = [
    "Your debts will definitely be discharged",
    "You are guaranteed to pass the means test",
    "The automatic stay cannot be lifted",
    "This transfer is absolutely safe from avoidance",
    "No creditor can challenge this exemption",
    "Your student loans will be discharged",
    "The court will certainly confirm this plan",
    "This asset is completely exempt",
    "You will not lose any property",
    "The trustee cannot touch this",
    "Filing bankruptcy is always the best option",
    "There is no risk of dismissal",
    "Your case will definitely convert successfully",
    "The preference claim has no merit",
]

REQUIRED_DISCLAIMERS: Dict[str, str] = {
    "not_legal_advice": (
        "This analysis is for informational purposes only and does not "
        "constitute legal advice. Consult a licensed bankruptcy attorney "
        "for specific legal guidance."
    ),
    "jurisdiction_specific": (
        "Bankruptcy law varies by circuit and district. Local rules and "
        "standing orders may affect outcomes. This analysis may not apply "
        "in all jurisdictions."
    ),
    "fact_dependent": (
        "Bankruptcy outcomes depend heavily on specific financial facts, "
        "income, assets, debts, and prior filing history. This analysis "
        "is based on the information provided."
    ),
    "exemption_caveat": (
        "Exemption amounts are adjusted periodically. State exemptions vary "
        "dramatically. Texas exemptions referenced herein are subject to "
        "the domicile requirement and homestead cap under BAPCPA."
    ),
}

AUTHORITY_WEIGHTS: Dict[str, int] = {
    "us_supreme_court": 100,
    "federal_circuit_court": 85,
    "bankruptcy_appellate_panel": 78,
    "federal_district_court": 70,
    "bankruptcy_court": 68,
    "state_supreme_court": 65,
    "state_appellate_court": 55,
    "federal_statute_title_11": 98,
    "federal_statute_title_28": 92,
    "frbp": 90,
    "local_bankruptcy_rules": 60,
    "cfr_regulation": 75,
    "us_trustee_guideline": 65,
    "restatement": 45,
    "treatise_collier": 50,
    "treatise_norton": 48,
    "law_review": 30,
    "abi_journal": 35,
    "census_median_data": 55,
}

CONFIDENCE_BANDS: Dict[str, Dict[str, Any]] = {
    "DEFENSIBLE": {"min_score": 0.85, "requires_caveat": False},
    "SUPPORTABLE": {"min_score": 0.65, "requires_caveat": True},
    "DISCLOSURE": {"min_score": 0.50, "requires_caveat": True},
    "HIGH_RISK": {"min_score": 0.0, "requires_caveat": True},
}


# ============================================================================
# RESPONSE MODE ENUM
# ============================================================================

class ResponseMode(str, Enum):
    """Available response modes for the Bankruptcy Law Engine."""
    FAST = "fast"
    ANALYSIS = "analysis"
    MEMO = "memo"
    MEANS_TEST = "means_test"
    PLAN_REVIEW = "plan_review"


# ============================================================================
# PYDANTIC REQUEST / RESPONSE MODELS
# ============================================================================

class QueryRequest(BaseModel):
    """Request model for bankruptcy law queries."""
    query: str = Field(..., min_length=3, max_length=5000, description="Bankruptcy law question or scenario")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response depth mode")
    chapter_filter: Optional[str] = Field(default=None, description="Filter to specific chapter (7, 11, 13, 12, 15)")
    jurisdiction: Optional[str] = Field(default=None, description="Jurisdiction hint (e.g., texas_western, 5th_circuit)")
    include_texas: bool = Field(default=True, description="Include Texas-specific analysis")
    top_k: int = Field(default=5, ge=1, le=20, description="Number of doctrine results to return")

    @field_validator("query")
    @classmethod
    def validate_query_not_empty(cls, v: str) -> str:
        stripped = v.strip()
        if len(stripped) < 3:
            raise ValueError("Query must be at least 3 characters")
        return stripped


class MeansTestRequest(BaseModel):
    """Request model for means test calculation."""
    monthly_income: float = Field(..., ge=0, description="Current monthly income (CMI)")
    household_size: int = Field(..., ge=1, le=15, description="Household size")
    state: str = Field(default="TX", description="State of residence")
    is_veteran: bool = Field(default=False, description="Disabled veteran status")
    is_reservist: bool = Field(default=False, description="Reservist/National Guard")
    non_consumer_majority: bool = Field(default=False, description="Non-consumer debts > 50%")
    secured_debt_payments: float = Field(default=0.0, ge=0, description="Average monthly secured debt payments")
    priority_debt_payments: float = Field(default=0.0, ge=0, description="Average monthly priority debt payments")
    special_circumstances: float = Field(default=0.0, ge=0, description="Special circumstances deduction")
    additional_deductions: Optional[Dict[str, float]] = Field(default=None, description="Additional allowable deductions")


class ExemptionRequest(BaseModel):
    """Request model for exemption analysis."""
    assets: List[Dict[str, Any]] = Field(..., min_length=1, description="List of assets with name, value, type")
    state: str = Field(default="TX", description="State of residence")
    is_married: bool = Field(default=False, description="Marital status")
    is_urban: bool = Field(default=True, description="Urban or rural homestead")


class DischargeRequest(BaseModel):
    """Request model for discharge analysis."""
    debt_type: str = Field(..., min_length=2, description="Type of debt (e.g., student_loan, tax, child_support)")
    debt_amount: Optional[float] = Field(default=None, ge=0, description="Amount of debt")
    additional_facts: Optional[Dict[str, Any]] = Field(default=None, description="Additional relevant facts")


class PreferenceRequest(BaseModel):
    """Request model for preference analysis."""
    transfer_date: str = Field(..., description="Date of transfer (YYYY-MM-DD)")
    petition_date: str = Field(..., description="Bankruptcy petition date (YYYY-MM-DD)")
    transfer_amount: float = Field(..., ge=0, description="Amount transferred")
    creditor_name: str = Field(..., description="Name of creditor")
    is_insider: bool = Field(default=False, description="Is creditor an insider")
    was_insolvent: bool = Field(default=True, description="Was debtor insolvent at time of transfer")
    on_account_of_antecedent_debt: bool = Field(default=True, description="Transfer on account of pre-existing debt")
    enables_greater_recovery: bool = Field(default=True, description="Creditor receives more than in Ch 7")
    ordinary_course: bool = Field(default=False, description="Ordinary course of business defense")
    contemporaneous_exchange: bool = Field(default=False, description="Contemporaneous exchange defense")
    subsequent_new_value: float = Field(default=0.0, ge=0, description="Subsequent new value provided")


class FraudTransferRequest(BaseModel):
    """Request model for fraudulent transfer analysis."""
    transfer_description: str = Field(..., description="Description of the transfer")
    transfer_value: float = Field(..., ge=0, description="Value of property transferred")
    value_received: float = Field(default=0.0, ge=0, description="Value received in exchange")
    badges_present: List[str] = Field(default_factory=list, description="Badges of fraud present")
    debtor_insolvent: Optional[bool] = Field(default=None, description="Was debtor insolvent at time of transfer")


class EngineResponse(BaseModel):
    """Standard response envelope for the Bankruptcy Law Engine."""
    engine_id: str = ENGINE_ID
    engine_name: str = ENGINE_NAME
    engine_version: str = ENGINE_VERSION
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    trace_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    mode: str = "fast"
    query: str = ""
    response_layer: str = "doctrine_cache"
    confidence: float = 0.0
    confidence_band: str = "HIGH_RISK"
    determinism_hash: str = ""
    analysis: Dict[str, Any] = Field(default_factory=dict)
    doctrine_hits: List[Dict[str, Any]] = Field(default_factory=list)
    search_results: List[Dict[str, Any]] = Field(default_factory=list)
    citations: List[str] = Field(default_factory=list)
    disclaimers: List[str] = Field(default_factory=list)
    texas_notes: Optional[str] = None
    normalization: Optional[Dict[str, Any]] = None
    timing_ms: float = 0.0
    metadata: Dict[str, Any] = Field(default_factory=dict)


# ============================================================================
# EPISTEMIC GUARDRAILS
# ============================================================================

def apply_epistemic_guardrails(text: str) -> Tuple[str, List[str]]:
    """Scan text for banned phrases and apply guardrails.

    Returns:
        Tuple of (sanitized_text, list_of_violations_found)
    """
    violations: List[str] = []
    sanitized = text
    for phrase in BANNED_PHRASES:
        if phrase.lower() in sanitized.lower():
            violations.append(f"Banned phrase detected: '{phrase}'")
            sanitized = sanitized.replace(phrase, "[ANALYSIS REQUIRES QUALIFICATION]")
    return sanitized, violations


def get_confidence_band(score: float) -> str:
    """Determine the confidence band for a given score."""
    for band_name, band_config in CONFIDENCE_BANDS.items():
        if score >= band_config["min_score"]:
            return band_name
    return "HIGH_RISK"


def get_required_disclaimers(band: str, categories: List[str]) -> List[str]:
    """Get disclaimers required for the given confidence band and categories."""
    disclaimers = [REQUIRED_DISCLAIMERS["not_legal_advice"]]
    if band != "DEFENSIBLE":
        disclaimers.append(REQUIRED_DISCLAIMERS["jurisdiction_specific"])
        disclaimers.append(REQUIRED_DISCLAIMERS["fact_dependent"])
    if any(cat in categories for cat in ["exemptions", "texas_homestead", "exemption_planning"]):
        disclaimers.append(REQUIRED_DISCLAIMERS["exemption_caveat"])
    return disclaimers


# ============================================================================
# AUTHORITY HARDENING
# ============================================================================

def compute_authority_score(citations: List[str]) -> float:
    """Compute aggregate authority score from citation sources."""
    if not citations:
        return 0.3
    scores: List[float] = []
    for citation in citations:
        cite_lower = citation.lower()
        matched_weight = 30  # default
        for source, weight in AUTHORITY_WEIGHTS.items():
            source_terms = source.replace("_", " ")
            if source_terms in cite_lower:
                matched_weight = weight
                break
        if "u.s." in cite_lower and "f." not in cite_lower and "b.r." not in cite_lower:
            matched_weight = max(matched_weight, 100)
        elif "f.3d" in cite_lower or "f.2d" in cite_lower or "f.4th" in cite_lower:
            matched_weight = max(matched_weight, 85)
        elif "b.r." in cite_lower:
            matched_weight = max(matched_weight, 68)
        elif "11 usc" in cite_lower or "title 11" in cite_lower:
            matched_weight = max(matched_weight, 98)
        elif "frbp" in cite_lower or "bankr. r." in cite_lower:
            matched_weight = max(matched_weight, 90)
        scores.append(matched_weight / 100.0)
    return min(sum(scores) / len(scores) + (len(scores) * 0.02), 0.99)


# ============================================================================
# FACT FRAGILITY SCORING
# ============================================================================

@dataclass
class FragilityAssessment:
    """Assessment of how fragile a legal position is to changed facts."""
    overall_fragility: float
    fragile_factors: List[Dict[str, Any]]
    stable_factors: List[Dict[str, Any]]
    recommendation: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "overall_fragility": round(self.overall_fragility, 4),
            "fragile_factors": self.fragile_factors,
            "stable_factors": self.stable_factors,
            "recommendation": self.recommendation,
        }


def assess_fact_fragility(
    query: str,
    confidence: float,
    detected_categories: List[str],
    chapter_type: Optional[str] = None,
) -> FragilityAssessment:
    """Assess the fragility of a legal analysis to changed facts."""
    fragile: List[Dict[str, Any]] = []
    stable: List[Dict[str, Any]] = []
    fragility_score = 0.0

    # Means test is highly fragile to income changes
    if "eligibility" in detected_categories or "means_test" in query.lower():
        fragile.append({
            "factor": "income_variability",
            "description": "Means test result is highly sensitive to income fluctuations in the 6-month lookback",
            "impact": 0.20,
        })
        fragility_score += 0.20

    # Exemption planning is fragile to asset valuation
    if "exemptions" in detected_categories:
        fragile.append({
            "factor": "asset_valuation",
            "description": "Exemption analysis depends on accurate property valuations which can change",
            "impact": 0.15,
        })
        fragility_score += 0.15

    # Discharge analysis is relatively stable for categorical debts
    if "discharge" in detected_categories:
        stable.append({
            "factor": "statutory_categories",
            "description": "Nondischargeability categories under 523 are well-defined statutory provisions",
            "impact": 0.0,
        })

    # Avoidance actions are fragile to factual disputes
    if "avoidance" in detected_categories:
        fragile.append({
            "factor": "factual_disputes",
            "description": "Avoidance actions depend on factual determinations (insolvency, intent, timing)",
            "impact": 0.18,
        })
        fragility_score += 0.18

    # Plan confirmation is fragile to feasibility
    if "plan" in detected_categories or chapter_type in ["chapter_11", "chapter_13"]:
        fragile.append({
            "factor": "plan_feasibility",
            "description": "Plan confirmation depends on debtor's ability to make payments over plan term",
            "impact": 0.15,
        })
        fragility_score += 0.15

    # Automatic stay is generally stable but fragile for serial filers
    if "stay" in detected_categories:
        if "serial" in query.lower() or "repeat" in query.lower():
            fragile.append({
                "factor": "filing_history",
                "description": "Serial filer stay limitations depend on prior filing history within 1 year",
                "impact": 0.12,
            })
            fragility_score += 0.12
        else:
            stable.append({
                "factor": "automatic_protection",
                "description": "Automatic stay arises by operation of law upon filing",
                "impact": 0.0,
            })

    # Texas-specific factors
    if any("texas" in cat or "tx" in cat for cat in detected_categories):
        fragile.append({
            "factor": "domicile_requirement",
            "description": "730-day domicile requirement for state exemptions under BAPCPA",
            "impact": 0.10,
        })
        fragility_score += 0.10

    fragility_score = min(fragility_score, 0.95)

    if fragility_score > 0.50:
        recommendation = "HIGH FRAGILITY: Analysis is highly sensitive to factual changes. Verify all underlying facts and consider sensitivity analysis."
    elif fragility_score > 0.25:
        recommendation = "MODERATE FRAGILITY: Some factors are sensitive to change. Document key factual assumptions."
    else:
        recommendation = "LOW FRAGILITY: Analysis rests on relatively stable legal foundations. Standard verification sufficient."

    return FragilityAssessment(
        overall_fragility=fragility_score,
        fragile_factors=fragile,
        stable_factors=stable,
        recommendation=recommendation,
    )


# ============================================================================
# DOCTRINE DRIFT WATCHER
# ============================================================================

class DoctrineDriftWatcher:
    """Monitor doctrine blocks for staleness and legal developments."""

    def __init__(self, registry_path: Path) -> None:
        self._registry_path = registry_path
        self._signals: List[Dict[str, Any]] = []
        self._load_registry()

    def _load_registry(self) -> None:
        """Load drift registry from disk."""
        if self._registry_path.exists():
            try:
                with self._registry_path.open("r", encoding="utf-8") as fh:
                    data = json.load(fh)
                    self._signals = data.get("signals", [])
            except (json.JSONDecodeError, OSError) as exc:
                logger.warning(f"Could not load drift registry: {exc}")
                self._signals = []

    def _save_registry(self) -> None:
        """Save drift registry to disk."""
        try:
            self._registry_path.parent.mkdir(parents=True, exist_ok=True)
            with self._registry_path.open("w", encoding="utf-8") as fh:
                json.dump({"signals": self._signals, "last_updated": datetime.now(timezone.utc).isoformat()}, fh, indent=2, default=str)
        except OSError as exc:
            logger.error(f"Could not save drift registry: {exc}")

    def record_signal(
        self,
        signal_type: str,
        affected_topics: List[str],
        description: str,
        source: str = "manual",
    ) -> Dict[str, Any]:
        """Record a doctrine drift signal."""
        signal = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "signal_type": signal_type,
            "affected_topics": affected_topics,
            "description": description,
            "source": source,
            "resolved": False,
        }
        self._signals.append(signal)
        self._save_registry()
        logger.info(f"Drift signal recorded: {signal_type} affecting {affected_topics}")
        return signal

    def get_unresolved_signals(self) -> List[Dict[str, Any]]:
        """Return all unresolved drift signals."""
        return [s for s in self._signals if not s.get("resolved", False)]

    def resolve_signal(self, signal_id: str) -> bool:
        """Mark a drift signal as resolved."""
        for signal in self._signals:
            if signal.get("id") == signal_id:
                signal["resolved"] = True
                signal["resolved_at"] = datetime.now(timezone.utc).isoformat()
                self._save_registry()
                return True
        return False

    def check_staleness(self, threshold_days: int = 90) -> List[Dict[str, Any]]:
        """Check all doctrine blocks for staleness."""
        stale = get_stale_doctrines(threshold_days)
        return [{"topic": b.topic, "staleness_days": b.staleness_days, "last_updated": b.last_updated} for b in stale]

    def get_stats(self) -> Dict[str, Any]:
        """Return drift watcher statistics."""
        unresolved = self.get_unresolved_signals()
        return {
            "total_signals": len(self._signals),
            "unresolved": len(unresolved),
            "signal_types": dict(Counter(s["signal_type"] for s in self._signals)),
        }


# ============================================================================
# MULTI-DOCTRINE DECOMPOSITION
# ============================================================================

def decompose_multi_doctrine(
    query: str,
    normalization: NormalizationResult,
) -> List[Dict[str, Any]]:
    """Decompose a complex query into multiple doctrine areas for parallel analysis."""
    components: List[Dict[str, Any]] = []
    categories = normalization.detected_categories
    chapter = normalization.detected_chapter

    if "eligibility" in categories or "means_test" in query.lower():
        components.append({
            "area": "means_test_eligibility",
            "description": "Chapter 7 means test and eligibility determination",
            "priority": 1,
            "requires": ["income_data", "household_size"],
        })

    if "exemptions" in categories:
        components.append({
            "area": "exemption_analysis",
            "description": "Federal vs state exemption analysis with Texas specifics",
            "priority": 2,
            "requires": ["asset_schedule", "state_of_domicile"],
        })

    if "discharge" in categories:
        components.append({
            "area": "discharge_determination",
            "description": "Dischargeability analysis for specific debt types",
            "priority": 2,
            "requires": ["debt_types", "factual_basis"],
        })

    if "stay" in categories:
        components.append({
            "area": "automatic_stay_analysis",
            "description": "Automatic stay scope, exceptions, and relief grounds",
            "priority": 1,
            "requires": ["filing_history", "creditor_actions"],
        })

    if "avoidance" in categories:
        components.append({
            "area": "avoidance_action_analysis",
            "description": "Preference and fraudulent transfer evaluation",
            "priority": 3,
            "requires": ["transfer_details", "timeline"],
        })

    if "plan" in categories or chapter in ["chapter_11", "chapter_13"]:
        components.append({
            "area": "plan_confirmation_analysis",
            "description": "Plan confirmation requirements and feasibility",
            "priority": 3,
            "requires": ["plan_terms", "creditor_classes"],
        })

    if "adversary" in categories:
        components.append({
            "area": "adversary_proceeding_analysis",
            "description": "Adversary proceeding requirements and strategy",
            "priority": 4,
            "requires": ["claim_basis", "bar_dates"],
        })

    if not components:
        components.append({
            "area": "general_bankruptcy_analysis",
            "description": "General bankruptcy law analysis and guidance",
            "priority": 1,
            "requires": [],
        })

    return sorted(components, key=lambda c: c["priority"])


# ============================================================================
# DEEP ANALYSIS ENGINE
# ============================================================================

def perform_deep_analysis(
    query: str,
    normalization: NormalizationResult,
    doctrine_hits: List[DoctrineCacheBlock],
    search_results: List[SearchResult],
) -> Dict[str, Any]:
    """Perform deep multi-doctrine synthesis analysis."""
    analysis: Dict[str, Any] = {
        "type": "deep_analysis",
        "query_classification": {
            "detected_chapter": normalization.detected_chapter,
            "categories": normalization.detected_categories,
            "texas_specific": normalization.texas_specific,
            "citation_count": len(normalization.detected_citations),
        },
        "doctrine_synthesis": [],
        "cross_references": [],
        "risk_assessment": {},
        "strategic_recommendations": [],
        "procedural_timeline": [],
    }

    # Synthesize across doctrine hits
    for doctrine in doctrine_hits:
        synthesis = {
            "topic": doctrine.topic,
            "category": doctrine.category,
            "key_points": doctrine.elements[:5],
            "authority": doctrine.authority_score,
            "confidence": doctrine.confidence,
            "applicable_defenses": doctrine.defenses[:3],
            "practice_tips": doctrine.practice_tips[:3],
        }
        if doctrine.texas_notes and normalization.texas_specific:
            synthesis["texas_notes"] = doctrine.texas_notes
        analysis["doctrine_synthesis"].append(synthesis)

    # Cross-reference detection
    seen_related: Set[str] = set()
    for doctrine in doctrine_hits:
        for related in doctrine.related_topics:
            if related not in seen_related:
                seen_related.add(related)
                related_block = get_doctrine_block(related)
                if related_block:
                    analysis["cross_references"].append({
                        "topic": related,
                        "category": related_block.category,
                        "relevance": "Related doctrine identified through cross-reference analysis",
                    })

    # Risk assessment
    risk_factors: List[str] = []
    for doctrine in doctrine_hits:
        risk_factors.extend(doctrine.risk_factors)
    analysis["risk_assessment"] = {
        "total_risk_factors": len(risk_factors),
        "factors": risk_factors[:10],
        "overall_risk_level": "HIGH" if len(risk_factors) > 5 else "MODERATE" if len(risk_factors) > 2 else "LOW",
    }

    # Strategic recommendations based on chapter type
    chapter = normalization.detected_chapter
    if chapter == "chapter_7":
        analysis["strategic_recommendations"] = [
            "Verify means test eligibility before filing",
            "Maximize exemptions through proper planning (within legal limits)",
            "Review all transfers in 90-day and 2-year lookback periods",
            "Ensure all BAPCPA requirements are met (counseling, courses, documentation)",
        ]
    elif chapter == "chapter_13":
        analysis["strategic_recommendations"] = [
            "Calculate projected disposable income using forward-looking approach (Lanning)",
            "Evaluate lien stripping opportunities for underwater junior liens",
            "Consider Chapter 20 strategy if appropriate",
            "Verify eligibility debt limits ($2.75M secured and unsecured)",
        ]
    elif chapter == "chapter_11":
        analysis["strategic_recommendations"] = [
            "Evaluate Subchapter V eligibility (debts < $7.5M)",
            "Plan first-day motion strategy (cash collateral, DIP financing, critical vendors)",
            "Assess classification strategy for plan confirmation",
            "Monitor exclusivity period deadlines",
        ]
    else:
        analysis["strategic_recommendations"] = [
            "Determine appropriate chapter based on debtor's circumstances",
            "Conduct comprehensive asset and liability analysis",
            "Review exemption strategy for applicable state",
            "Assess discharge eligibility for all debt categories",
        ]

    # Procedural timeline
    analysis["procedural_timeline"] = [
        {"step": 1, "event": "Pre-filing credit counseling (180 days before)", "deadline": "Pre-filing"},
        {"step": 2, "event": "File petition, schedules, SOFA, means test", "deadline": "Filing date"},
        {"step": 3, "event": "Automatic stay takes effect", "deadline": "Immediately upon filing"},
        {"step": 4, "event": "341 Meeting of Creditors", "deadline": "20-40 days after filing"},
        {"step": 5, "event": "Deadline for 523(c) complaints", "deadline": "60 days after first 341 date"},
        {"step": 6, "event": "Deadline for 727 complaints", "deadline": "60 days after first 341 date"},
        {"step": 7, "event": "Financial management course", "deadline": "Before discharge"},
        {"step": 8, "event": "Discharge entered (Ch 7)", "deadline": "~60 days after 341 meeting"},
    ]

    return analysis


# ============================================================================
# CORE QUERY PROCESSING PIPELINE
# ============================================================================

def process_query(
    query: str,
    mode: ResponseMode = ResponseMode.FAST,
    chapter_filter: Optional[str] = None,
    jurisdiction: Optional[str] = None,
    include_texas: bool = True,
    top_k: int = 5,
) -> EngineResponse:
    """Process a bankruptcy law query through the full TIE-20 pipeline."""
    # Start trace
    trace = trace_query(query, mode.value)
    start = time.monotonic()

    try:
        # [TIE-6] Semantic normalization
        norm_start = time.monotonic()
        normalization = normalize_query(query)
        trace.normalization_ms = (time.monotonic() - norm_start) * 1000.0

        # [TIE-3] Doctrine cache lookup
        doctrine_start = time.monotonic()
        doctrine_hits: List[DoctrineCacheBlock] = search_doctrines(query, top_k=top_k)
        trace.doctrine_lookup_ms = (time.monotonic() - doctrine_start) * 1000.0
        trace.doctrine_hits = len(doctrine_hits)

        # Filter by chapter if requested
        if chapter_filter:
            doctrine_hits = [d for d in doctrine_hits if chapter_filter.lower() in d.topic.lower() or chapter_filter.lower() in d.category.lower()] or doctrine_hits

        # [TIE-7] TF-IDF search
        search_start = time.monotonic()
        search_index = get_search_index()
        if not search_index._built:
            for block in DOCTRINE_BLOCKS:
                search_index.add_document(
                    doc_id=block.topic,
                    content=block.content_for_search(),
                    metadata=block.to_dict(),
                )
            search_index.build()
        search_results = search_index.search(
            query=normalization.normalized_query or query,
            top_k=top_k,
            category_filter=chapter_filter,
            jurisdiction_filter=jurisdiction,
        )
        trace.search_ms = (time.monotonic() - search_start) * 1000.0
        trace.search_results = len(search_results)

        # Determine response layer
        if doctrine_hits:
            response_layer = ResponseLayer.DOCTRINE_CACHE
        elif search_results:
            response_layer = ResponseLayer.SEMANTIC_SEARCH
        else:
            response_layer = ResponseLayer.FALLBACK
        trace.response_layer = response_layer

        # [TIE-4] Authority hardening
        all_citations: List[str] = []
        for d in doctrine_hits:
            all_citations.extend(d.key_statutes)
            all_citations.extend(d.leading_cases[:3])
        authority_score = compute_authority_score(all_citations)

        # [TIE-5] Confidence stratification
        base_confidence = 0.5
        if doctrine_hits:
            base_confidence = max(d.confidence for d in doctrine_hits)
        if search_results:
            base_confidence = max(base_confidence, max(r.score for r in search_results) * 0.9)
        base_confidence = min((base_confidence + authority_score) / 2.0, 0.99)
        confidence_band = get_confidence_band(base_confidence)

        # [TIE-14] Fact fragility scoring
        fragility = assess_fact_fragility(
            query, base_confidence,
            normalization.detected_categories,
            normalization.detected_chapter,
        )

        # Record chapter-specific metric
        chapter = normalization.detected_chapter
        if chapter == "chapter_7":
            record_bk_metric(BankruptcyMetricType.CHAPTER_7_QUERY)
        elif chapter == "chapter_11":
            record_bk_metric(BankruptcyMetricType.CHAPTER_11_QUERY)
        elif chapter == "chapter_13":
            record_bk_metric(BankruptcyMetricType.CHAPTER_13_QUERY)
        elif chapter == "chapter_12":
            record_bk_metric(BankruptcyMetricType.CHAPTER_12_QUERY)
        elif chapter == "chapter_15":
            record_bk_metric(BankruptcyMetricType.CHAPTER_15_QUERY)

        # Build analysis based on mode
        analysis: Dict[str, Any] = {}

        if mode in (ResponseMode.ANALYSIS, ResponseMode.MEMO, ResponseMode.PLAN_REVIEW):
            # [TIE-19] Multi-doctrine decomposition
            analysis["decomposition"] = decompose_multi_doctrine(query, normalization)
            analysis["fragility"] = fragility.to_dict()

        if mode in (ResponseMode.MEMO, ResponseMode.PLAN_REVIEW):
            # [TIE-20] Deep analysis
            deep = perform_deep_analysis(query, normalization, doctrine_hits, search_results)
            analysis["deep_analysis"] = deep

        # [TIE-1] Three-layer response construction
        analysis["primary_response"] = {
            "summary": doctrine_hits[0].summary if doctrine_hits else "No direct doctrine match found. Analysis based on search results.",
            "key_statutes": doctrine_hits[0].key_statutes if doctrine_hits else [],
            "elements": doctrine_hits[0].elements[:5] if doctrine_hits else [],
            "leading_cases": doctrine_hits[0].leading_cases[:3] if doctrine_hits else [],
        }

        # Texas notes
        texas_notes: Optional[str] = None
        if include_texas:
            for d in doctrine_hits:
                if d.texas_notes:
                    texas_notes = d.texas_notes
                    break

        # Apply epistemic guardrails
        response_text = json.dumps(analysis.get("primary_response", {}))
        _, violations = apply_epistemic_guardrails(response_text)
        if violations:
            logger.warning(f"Epistemic violations detected: {violations}")

        # Get disclaimers
        disclaimers = get_required_disclaimers(confidence_band, normalization.detected_categories)

        # [TIE-16] Determinism hash
        determinism_payload = json.dumps({
            "query": query,
            "mode": mode.value,
            "doctrine_topics": [d.topic for d in doctrine_hits],
            "confidence": base_confidence,
        }, sort_keys=True)
        determinism_hash = hashlib.sha256(determinism_payload.encode("utf-8")).hexdigest()

        # Complete trace
        trace.confidence = base_confidence
        trace.chapter_type = chapter
        trace.bankruptcy_category = normalization.detected_categories[0] if normalization.detected_categories else None
        trace.citations_returned = len(all_citations)
        trace.end_time = time.monotonic()
        trace.analysis_ms = (trace.end_time - start) * 1000.0 - trace.normalization_ms - trace.doctrine_lookup_ms - trace.search_ms
        complete_trace(trace)

        total_ms = (time.monotonic() - start) * 1000.0

        return EngineResponse(
            trace_id=trace.trace_id,
            mode=mode.value,
            query=query,
            response_layer=response_layer.value,
            confidence=round(base_confidence, 4),
            confidence_band=confidence_band,
            determinism_hash=determinism_hash,
            analysis=analysis,
            doctrine_hits=[d.to_dict() for d in doctrine_hits],
            search_results=[r.to_dict() for r in search_results],
            citations=all_citations[:20],
            disclaimers=disclaimers,
            texas_notes=texas_notes,
            normalization=normalization.to_dict(),
            timing_ms=round(total_ms, 3),
            metadata={
                "authority_score": round(authority_score, 4),
                "fragility": fragility.to_dict(),
                "detected_chapter": chapter,
                "detected_categories": normalization.detected_categories,
                "epistemic_violations": len(violations),
            },
        )

    except Exception as exc:
        trace.error = str(exc)
        trace.response_layer = ResponseLayer.ERROR
        complete_trace(trace)
        log_error(ErrorDomain.SYSTEM, f"Query processing error: {exc}", trace.trace_id)
        raise


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler for startup and shutdown."""
    # Startup
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logger.add(
        LOG_DIR / "lg12_bankruptcy.log",
        rotation="50 MB",
        retention="30 days",
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {message}",
        level="INFO",
    )
    logger.info(f"LG12 Bankruptcy Law Engine v{ENGINE_VERSION} starting on port {ENGINE_PORT}")

    # Build doctrine cache
    cache = build_doctrine_cache()
    logger.info(f"Doctrine cache built: {cache.stats()}")

    # Initialize search index
    idx = get_search_index()
    for block in DOCTRINE_BLOCKS:
        idx.add_document(block.topic, block.content_for_search(), block.to_dict())
    idx.build()
    logger.info(f"Search index built: {idx.get_stats()}")

    # Initialize telemetry
    telem = get_telemetry(AUDIT_LOG_PATH)
    logger.info(f"Telemetry initialized: audit={AUDIT_LOG_PATH}")

    # Verify integrity
    dict_check = verify_dictionary_integrity()
    logger.info(f"Semantic dictionary: {dict_check['total_entries']} entries, valid={dict_check['valid']}")
    doctrine_check = verify_doctrine_integrity()
    logger.info(f"Doctrine integrity: {doctrine_check['total_blocks']} blocks, valid={doctrine_check['valid']}")

    logger.info(f"LG12 Bankruptcy Law Engine READY on {ENGINE_HOST}:{ENGINE_PORT}")
    yield
    # Shutdown
    logger.info("LG12 Bankruptcy Law Engine shutting down")


app = FastAPI(
    title="LG12 Bankruptcy Law Engine",
    description=(
        "Production-grade bankruptcy law analysis engine implementing all 20 TIE "
        "components. Covers Chapter 7/11/13/12/15, means test, automatic stay, "
        "discharge, exemptions, avoidance actions, plan confirmation, and Texas specifics."
    ),
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
# [TIE-12] HEALTH ENDPOINT
# ============================================================================

@app.get("/health")
async def health_check() -> Dict[str, Any]:
    """Health check endpoint returning engine status and component health."""
    doctrine_stats = get_doctrine_cache_stats()
    search_stats = get_search_index().get_stats()
    dict_integrity = verify_dictionary_integrity()
    telem_metrics = get_telemetry().get_metrics()
    return {
        "status": "healthy",
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "engine_version": ENGINE_VERSION,
        "port": ENGINE_PORT,
        "tier": ENGINE_TIER,
        "mode": ENGINE_MODE,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "components": {
            "doctrine_cache": {"status": "ok", "blocks": doctrine_stats["total_blocks"], "hash": doctrine_stats["hash"][:16]},
            "search_index": {"status": "ok", **search_stats},
            "semantic_dictionary": {"status": "ok" if dict_integrity["valid"] else "degraded", "entries": dict_integrity["total_entries"]},
            "telemetry": {"status": "ok", "uptime_seconds": telem_metrics["uptime_seconds"]},
            "audit_trail": {"status": "ok", "entries": telem_metrics["audit_trail"]["entries"]},
        },
    }


# ============================================================================
# [TIE-17] MAIN QUERY ENDPOINT
# ============================================================================

@app.post("/query", response_model=EngineResponse)
async def handle_query(request: QueryRequest) -> EngineResponse:
    """Process a bankruptcy law query through the full TIE-20 pipeline."""
    return process_query(
        query=request.query,
        mode=request.mode,
        chapter_filter=request.chapter_filter,
        jurisdiction=request.jurisdiction,
        include_texas=request.include_texas,
        top_k=request.top_k,
    )


# ============================================================================
# MEANS TEST ENDPOINT
# ============================================================================

@app.post("/means-test")
async def handle_means_test(request: MeansTestRequest) -> Dict[str, Any]:
    """Calculate the Chapter 7 means test."""
    trace = trace_query(f"means_test: income={request.monthly_income} hhsize={request.household_size}", "means_test")
    record_bk_metric(BankruptcyMetricType.MEANS_TEST_CALCULATION)
    try:
        calculator = get_means_test_calculator()
        result = calculator.calculate(
            monthly_income=request.monthly_income,
            household_size=request.household_size,
            state=request.state,
            is_veteran=request.is_veteran,
            is_reservist=request.is_reservist,
            non_consumer_debt_majority=request.non_consumer_majority,
            secured_debt_payments=request.secured_debt_payments,
            priority_debt_payments=request.priority_debt_payments,
            special_circumstances_amount=request.special_circumstances,
            additional_deductions=request.additional_deductions,
        )
        trace.confidence = result.confidence
        trace.response_layer = ResponseLayer.BANKRUPTCY_ANALYSIS
        complete_trace(trace)
        return {
            "engine_id": ENGINE_ID,
            "endpoint": "means_test",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "result": result.to_dict(),
            "disclaimers": [REQUIRED_DISCLAIMERS["not_legal_advice"], REQUIRED_DISCLAIMERS["fact_dependent"]],
        }
    except Exception as exc:
        trace.error = str(exc)
        complete_trace(trace)
        raise HTTPException(status_code=500, detail=str(exc))


# ============================================================================
# EXEMPTION ANALYSIS ENDPOINT
# ============================================================================

@app.post("/exemptions")
async def handle_exemptions(request: ExemptionRequest) -> Dict[str, Any]:
    """Analyze asset exemptions under applicable law."""
    trace = trace_query(f"exemptions: {len(request.assets)} assets, state={request.state}", "analysis")
    record_bk_metric(BankruptcyMetricType.EXEMPTION_ANALYSIS)
    try:
        analyzer = get_exemption_analyzer()
        result = analyzer.analyze(
            assets=request.assets,
            state=request.state,
            is_married=request.is_married,
            is_urban=request.is_urban,
        )
        trace.confidence = result.confidence
        trace.response_layer = ResponseLayer.BANKRUPTCY_ANALYSIS
        complete_trace(trace)
        return {
            "engine_id": ENGINE_ID,
            "endpoint": "exemptions",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "result": result.to_dict(),
            "disclaimers": [REQUIRED_DISCLAIMERS["not_legal_advice"], REQUIRED_DISCLAIMERS["exemption_caveat"]],
        }
    except Exception as exc:
        trace.error = str(exc)
        complete_trace(trace)
        raise HTTPException(status_code=500, detail=str(exc))


# ============================================================================
# DISCHARGE ANALYSIS ENDPOINT
# ============================================================================

@app.post("/discharge")
async def handle_discharge(request: DischargeRequest) -> Dict[str, Any]:
    """Analyze whether a specific debt is dischargeable."""
    trace = trace_query(f"discharge: {request.debt_type}", "analysis")
    record_bk_metric(BankruptcyMetricType.DISCHARGE_DETERMINATION)
    try:
        analyzer = get_discharge_analyzer()
        result = analyzer.analyze_discharge(
            debt_type=request.debt_type,
            debt_amount=request.debt_amount,
            additional_facts=request.additional_facts,
        )
        trace.confidence = result.discharge_confidence
        trace.response_layer = ResponseLayer.BANKRUPTCY_ANALYSIS
        complete_trace(trace)
        return {
            "engine_id": ENGINE_ID,
            "endpoint": "discharge",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "result": result.to_dict(),
            "disclaimers": [REQUIRED_DISCLAIMERS["not_legal_advice"], REQUIRED_DISCLAIMERS["jurisdiction_specific"]],
        }
    except Exception as exc:
        trace.error = str(exc)
        complete_trace(trace)
        raise HTTPException(status_code=500, detail=str(exc))


# ============================================================================
# PREFERENCE ANALYSIS ENDPOINT
# ============================================================================

@app.post("/preference")
async def handle_preference(request: PreferenceRequest) -> Dict[str, Any]:
    """Analyze a potential preferential transfer."""
    trace = trace_query(f"preference: {request.creditor_name} ${request.transfer_amount}", "analysis")
    record_bk_metric(BankruptcyMetricType.PREFERENCE_ANALYSIS)
    try:
        analyzer = get_preference_analyzer()
        result = analyzer.analyze(
            transfer_date=request.transfer_date,
            petition_date=request.petition_date,
            transfer_amount=request.transfer_amount,
            creditor_name=request.creditor_name,
            is_insider=request.is_insider,
            was_insolvent=request.was_insolvent,
            on_account_of_antecedent_debt=request.on_account_of_antecedent_debt,
            enables_greater_recovery=request.enables_greater_recovery,
            ordinary_course=request.ordinary_course,
            contemporaneous_exchange=request.contemporaneous_exchange,
            subsequent_new_value=request.subsequent_new_value,
        )
        trace.confidence = result.avoidance_confidence
        trace.response_layer = ResponseLayer.BANKRUPTCY_ANALYSIS
        complete_trace(trace)
        return {
            "engine_id": ENGINE_ID,
            "endpoint": "preference",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "result": result.to_dict(),
            "disclaimers": [REQUIRED_DISCLAIMERS["not_legal_advice"], REQUIRED_DISCLAIMERS["fact_dependent"]],
        }
    except Exception as exc:
        trace.error = str(exc)
        complete_trace(trace)
        raise HTTPException(status_code=500, detail=str(exc))


# ============================================================================
# FRAUDULENT TRANSFER ENDPOINT
# ============================================================================

@app.post("/fraudulent-transfer")
async def handle_fraudulent_transfer(request: FraudTransferRequest) -> Dict[str, Any]:
    """Analyze a potential fraudulent transfer."""
    trace = trace_query(f"fraudulent_transfer: ${request.transfer_value}", "analysis")
    record_bk_metric(BankruptcyMetricType.FRAUDULENT_TRANSFER_ANALYSIS)
    try:
        analyzer = get_fraudulent_transfer_analyzer()
        result = analyzer.analyze(
            transfer_description=request.transfer_description,
            transfer_value=request.transfer_value,
            value_received=request.value_received,
            badges_present=request.badges_present,
            debtor_insolvent=request.debtor_insolvent,
        )
        trace.confidence = result.confidence
        trace.response_layer = ResponseLayer.BANKRUPTCY_ANALYSIS
        complete_trace(trace)
        return {
            "engine_id": ENGINE_ID,
            "endpoint": "fraudulent_transfer",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "result": result.to_dict(),
            "disclaimers": [REQUIRED_DISCLAIMERS["not_legal_advice"], REQUIRED_DISCLAIMERS["fact_dependent"]],
        }
    except Exception as exc:
        trace.error = str(exc)
        complete_trace(trace)
        raise HTTPException(status_code=500, detail=str(exc))


# ============================================================================
# DOCTRINE ENDPOINTS
# ============================================================================

@app.get("/doctrines")
async def list_doctrines(
    category: Optional[str] = Query(default=None, description="Filter by category"),
) -> Dict[str, Any]:
    """List all available doctrine blocks."""
    cache = get_doctrine_cache()
    if category:
        blocks = cache.get_by_category(category)
    else:
        blocks = DOCTRINE_BLOCKS
    return {
        "engine_id": ENGINE_ID,
        "total": len(blocks),
        "categories": sorted(cache.all_categories()),
        "doctrines": [{"topic": b.topic, "category": b.category, "confidence": b.confidence, "summary": b.summary[:200]} for b in blocks],
    }


@app.get("/doctrines/{topic}")
async def get_doctrine(topic: str) -> Dict[str, Any]:
    """Get a specific doctrine block by topic."""
    block = get_doctrine_block(topic)
    if not block:
        raise HTTPException(status_code=404, detail=f"Doctrine topic '{topic}' not found")
    return {"engine_id": ENGINE_ID, "doctrine": block.to_dict()}


@app.get("/doctrines-coverage")
async def doctrine_coverage() -> Dict[str, Any]:
    """Get doctrine coverage map with staleness data."""
    return {
        "engine_id": ENGINE_ID,
        "coverage": get_coverage_map(),
        "stats": get_doctrine_cache_stats(),
        "integrity": verify_doctrine_integrity(),
    }


# ============================================================================
# TELEMETRY / METRICS ENDPOINTS
# ============================================================================

@app.get("/metrics")
async def get_metrics() -> Dict[str, Any]:
    """Get engine telemetry metrics."""
    return get_telemetry().get_metrics()


@app.get("/metrics/traces")
async def get_traces(count: int = Query(default=50, ge=1, le=500)) -> Dict[str, Any]:
    """Get recent query traces."""
    return {"engine_id": ENGINE_ID, "traces": get_telemetry().get_recent_traces(count)}


@app.get("/metrics/errors")
async def get_errors(count: int = Query(default=50, ge=1, le=500)) -> Dict[str, Any]:
    """Get recent errors."""
    return {"engine_id": ENGINE_ID, "errors": get_telemetry().get_recent_errors(count)}


@app.get("/metrics/mutations")
async def get_mutations(count: int = Query(default=50, ge=1, le=500)) -> Dict[str, Any]:
    """Get recent doctrine mutations."""
    return {"engine_id": ENGINE_ID, "mutations": get_telemetry().get_recent_mutations(count)}


@app.get("/audit/verify")
async def verify_audit() -> Dict[str, Any]:
    """Verify audit trail hash chain integrity."""
    return {"engine_id": ENGINE_ID, **get_telemetry().verify_audit_chain()}


# ============================================================================
# SEMANTIC / SEARCH ENDPOINTS
# ============================================================================

@app.get("/semantic/normalize")
async def normalize_endpoint(q: str = Query(..., min_length=2)) -> Dict[str, Any]:
    """Normalize a bankruptcy query through the semantic pipeline."""
    result = normalize_query(q)
    return {"engine_id": ENGINE_ID, "normalization": result.to_dict()}


@app.get("/semantic/dictionary")
async def semantic_dictionary() -> Dict[str, Any]:
    """Get semantic dictionary metadata and integrity status."""
    return {"engine_id": ENGINE_ID, **verify_dictionary_integrity()}


@app.get("/search")
async def search_endpoint(
    q: str = Query(..., min_length=2),
    top_k: int = Query(default=5, ge=1, le=20),
    category: Optional[str] = Query(default=None),
) -> Dict[str, Any]:
    """Search the doctrine index."""
    idx = get_search_index()
    results = idx.search(q, top_k=top_k, category_filter=category)
    return {
        "engine_id": ENGINE_ID,
        "query": q,
        "results": [r.to_dict() for r in results],
        "total": len(results),
    }


# ============================================================================
# DRIFT WATCHER ENDPOINT
# ============================================================================

@app.get("/drift")
async def drift_status() -> Dict[str, Any]:
    """Get doctrine drift watcher status."""
    watcher = DoctrineDriftWatcher(DRIFT_REGISTRY_PATH)
    return {
        "engine_id": ENGINE_ID,
        "stats": watcher.get_stats(),
        "unresolved_signals": watcher.get_unresolved_signals(),
        "stale_doctrines": watcher.check_staleness(90),
    }


# ============================================================================
# JURISDICTION MAP ENDPOINT
# ============================================================================

@app.get("/jurisdictions")
async def list_jurisdictions() -> Dict[str, Any]:
    """List supported bankruptcy jurisdictions."""
    return {"engine_id": ENGINE_ID, "jurisdictions": get_jurisdiction_map()}


# ============================================================================
# CONFIG ENDPOINT
# ============================================================================

@app.get("/config")
async def get_config() -> Dict[str, Any]:
    """Get engine configuration."""
    if CONFIG_PATH.exists():
        with CONFIG_PATH.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    return {"error": "Configuration file not found"}


# ============================================================================
# CHAPTER SELECTION ADVISOR
# ============================================================================

class ChapterSelectionRequest(BaseModel):
    """Request model for chapter selection advisory."""
    monthly_income: float = Field(..., ge=0, description="Current monthly income")
    household_size: int = Field(default=1, ge=1, le=15)
    total_secured_debt: float = Field(default=0.0, ge=0)
    total_unsecured_debt: float = Field(default=0.0, ge=0)
    total_priority_debt: float = Field(default=0.0, ge=0)
    has_regular_income: bool = Field(default=True)
    is_business_debtor: bool = Field(default=False)
    is_farmer: bool = Field(default=False)
    wants_to_keep_property: bool = Field(default=True)
    has_prior_filing: bool = Field(default=False)
    prior_filing_chapter: Optional[str] = Field(default=None)
    years_since_prior_discharge: Optional[int] = Field(default=None)
    state: str = Field(default="TX")
    non_exempt_asset_value: float = Field(default=0.0, ge=0)
    student_loan_debt: float = Field(default=0.0, ge=0)
    tax_debt: float = Field(default=0.0, ge=0)
    domestic_support_debt: float = Field(default=0.0, ge=0)


@dataclass
class ChapterRecommendation:
    """A chapter recommendation with reasoning."""
    chapter: str
    score: float
    eligible: bool
    reasons: List[str]
    risks: List[str]
    disqualifiers: List[str]
    citations: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "chapter": self.chapter,
            "score": round(self.score, 4),
            "eligible": self.eligible,
            "reasons": self.reasons,
            "risks": self.risks,
            "disqualifiers": self.disqualifiers,
            "citations": self.citations,
        }


def evaluate_chapter_selection(req: ChapterSelectionRequest) -> List[ChapterRecommendation]:
    """Evaluate which bankruptcy chapter is most appropriate."""
    recommendations: List[ChapterRecommendation] = []

    # ---- CHAPTER 7 EVALUATION ----
    ch7_eligible = True
    ch7_reasons: List[str] = []
    ch7_risks: List[str] = []
    ch7_disq: List[str] = []
    ch7_score = 0.5

    annualized = req.monthly_income * 12
    tx_median = TX_MEDIAN_INCOME.get(min(req.household_size, 10), 103176.0)
    from search import TX_MEDIAN_INCOME

    if annualized <= tx_median:
        ch7_reasons.append(f"Below TX median income (${annualized:,.0f} vs ${tx_median:,.0f}) - passes means test")
        ch7_score += 0.25
    else:
        ch7_risks.append(f"Above TX median income - means test required (${annualized:,.0f} vs ${tx_median:,.0f})")
        ch7_score -= 0.15

    if req.non_exempt_asset_value == 0:
        ch7_reasons.append("No non-exempt assets - no-asset Chapter 7 case likely")
        ch7_score += 0.15
    elif req.non_exempt_asset_value > 10000:
        ch7_risks.append(f"Non-exempt assets of ${req.non_exempt_asset_value:,.0f} may be liquidated")
        ch7_score -= 0.10

    if req.has_prior_filing and req.prior_filing_chapter == "7":
        if req.years_since_prior_discharge is not None and req.years_since_prior_discharge < 8:
            ch7_eligible = False
            ch7_disq.append(f"Prior Chapter 7 discharge within 8 years ({req.years_since_prior_discharge} years ago)")
        elif req.years_since_prior_discharge is not None and req.years_since_prior_discharge >= 8:
            ch7_reasons.append("Prior Chapter 7 discharge was 8+ years ago - eligible")

    if req.has_prior_filing and req.prior_filing_chapter == "13":
        if req.years_since_prior_discharge is not None and req.years_since_prior_discharge < 6:
            ch7_eligible = False
            ch7_disq.append(f"Prior Chapter 13 discharge within 6 years ({req.years_since_prior_discharge} years ago)")

    if not req.wants_to_keep_property and req.non_exempt_asset_value < 5000:
        ch7_reasons.append("Debtor willing to surrender property - Chapter 7 liquidation appropriate")
        ch7_score += 0.10

    if req.domestic_support_debt > 0:
        ch7_risks.append("Domestic support obligations survive discharge")

    if req.student_loan_debt > 0:
        ch7_risks.append("Student loans survive discharge unless undue hardship shown (Brunner test)")

    recommendations.append(ChapterRecommendation(
        chapter="Chapter 7",
        score=max(ch7_score, 0.1) if ch7_eligible else 0.0,
        eligible=ch7_eligible,
        reasons=ch7_reasons,
        risks=ch7_risks,
        disqualifiers=ch7_disq,
        citations=["11 USC 707(b)", "11 USC 727"],
    ))

    # ---- CHAPTER 13 EVALUATION ----
    ch13_eligible = True
    ch13_reasons: List[str] = []
    ch13_risks: List[str] = []
    ch13_disq: List[str] = []
    ch13_score = 0.5

    total_debt = req.total_secured_debt + req.total_unsecured_debt + req.total_priority_debt
    if req.total_secured_debt > 2750000 or req.total_unsecured_debt > 2750000:
        ch13_eligible = False
        ch13_disq.append(f"Debt exceeds Chapter 13 limits: secured ${req.total_secured_debt:,.0f}, unsecured ${req.total_unsecured_debt:,.0f}")

    if not req.has_regular_income:
        ch13_eligible = False
        ch13_disq.append("No regular income - Chapter 13 requires regular income source")

    if req.wants_to_keep_property:
        ch13_reasons.append("Chapter 13 allows debtor to retain all property while repaying through plan")
        ch13_score += 0.20

    if req.total_secured_debt > 0 and req.wants_to_keep_property:
        ch13_reasons.append("Can cure mortgage arrears and cramdown secured claims through plan")
        ch13_score += 0.15

    if annualized > tx_median:
        ch13_reasons.append("Above-median income may make Chapter 7 difficult - Chapter 13 is an alternative")
        ch13_score += 0.15

    if req.non_exempt_asset_value > 10000:
        ch13_reasons.append(f"Protects ${req.non_exempt_asset_value:,.0f} in non-exempt assets from liquidation")
        ch13_score += 0.15

    if annualized > tx_median:
        ch13_risks.append("60-month plan commitment required for above-median debtors")
    else:
        ch13_reasons.append("Below-median income: 36-month plan minimum")

    if req.has_prior_filing and req.prior_filing_chapter == "13":
        if req.years_since_prior_discharge is not None and req.years_since_prior_discharge < 2:
            ch13_eligible = False
            ch13_disq.append(f"Prior Chapter 13 discharge within 2 years ({req.years_since_prior_discharge} years ago)")

    recommendations.append(ChapterRecommendation(
        chapter="Chapter 13",
        score=max(ch13_score, 0.1) if ch13_eligible else 0.0,
        eligible=ch13_eligible,
        reasons=ch13_reasons,
        risks=ch13_risks,
        disqualifiers=ch13_disq,
        citations=["11 USC 1301-1330", "11 USC 1322", "11 USC 1325"],
    ))

    # ---- CHAPTER 11 EVALUATION ----
    ch11_eligible = True
    ch11_reasons: List[str] = []
    ch11_risks: List[str] = []
    ch11_disq: List[str] = []
    ch11_score = 0.3

    if req.is_business_debtor:
        ch11_reasons.append("Business debtor - Chapter 11 allows continued operations during reorganization")
        ch11_score += 0.25

    if req.total_secured_debt > 2750000 or req.total_unsecured_debt > 2750000:
        ch11_reasons.append("Debt exceeds Chapter 13 limits - Chapter 11 is available alternative")
        ch11_score += 0.20

    if total_debt <= 7500000:
        ch11_reasons.append(f"Eligible for Subchapter V (SBRA) - streamlined process, no APR, no disclosure statement")
        ch11_score += 0.10

    ch11_risks.append("High administrative costs (professional fees, UST fees)")
    ch11_risks.append("Complex process requiring disclosure statement and plan solicitation")

    if not req.is_business_debtor and req.total_secured_debt <= 2750000 and req.total_unsecured_debt <= 2750000:
        ch11_score -= 0.20
        ch11_risks.append("Individual non-business debtor may be better served by Chapter 7 or 13")

    recommendations.append(ChapterRecommendation(
        chapter="Chapter 11",
        score=max(ch11_score, 0.1) if ch11_eligible else 0.0,
        eligible=ch11_eligible,
        reasons=ch11_reasons,
        risks=ch11_risks,
        disqualifiers=ch11_disq,
        citations=["11 USC 1101-1195", "11 USC 1181-1195 (Sub V)"],
    ))

    # ---- CHAPTER 12 EVALUATION ----
    ch12_eligible = req.is_farmer
    ch12_reasons: List[str] = []
    ch12_risks: List[str] = []
    ch12_disq: List[str] = []
    ch12_score = 0.3

    if req.is_farmer:
        ch12_reasons.append("Family farmer debtor - Chapter 12 provides tailored relief")
        ch12_score += 0.30
        if total_debt <= 11097350:
            ch12_reasons.append(f"Total debt ${total_debt:,.0f} within $11,097,350 Chapter 12 limit")
            ch12_score += 0.15
        else:
            ch12_eligible = False
            ch12_disq.append(f"Total debt ${total_debt:,.0f} exceeds $11,097,350 limit")
        ch12_reasons.append("Can modify secured claims including farmland mortgage (unlike Chapter 13)")
    else:
        ch12_disq.append("Not a family farmer or fisherman - Chapter 12 not available")

    recommendations.append(ChapterRecommendation(
        chapter="Chapter 12",
        score=max(ch12_score, 0.1) if ch12_eligible else 0.0,
        eligible=ch12_eligible,
        reasons=ch12_reasons,
        risks=ch12_risks,
        disqualifiers=ch12_disq,
        citations=["11 USC 1201-1231"],
    ))

    # Sort by score descending
    recommendations.sort(key=lambda r: r.score, reverse=True)
    return recommendations


@app.post("/chapter-selection")
async def handle_chapter_selection(request: ChapterSelectionRequest) -> Dict[str, Any]:
    """Evaluate which bankruptcy chapter is most appropriate."""
    trace = trace_query(f"chapter_selection: income={request.monthly_income}", "analysis")
    try:
        recommendations = evaluate_chapter_selection(request)
        trace.confidence = recommendations[0].score if recommendations else 0.5
        trace.response_layer = ResponseLayer.BANKRUPTCY_ANALYSIS
        complete_trace(trace)
        return {
            "engine_id": ENGINE_ID,
            "endpoint": "chapter_selection",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "recommendations": [r.to_dict() for r in recommendations],
            "top_recommendation": recommendations[0].to_dict() if recommendations else None,
            "disclaimers": [
                REQUIRED_DISCLAIMERS["not_legal_advice"],
                REQUIRED_DISCLAIMERS["fact_dependent"],
                REQUIRED_DISCLAIMERS["jurisdiction_specific"],
            ],
        }
    except Exception as exc:
        trace.error = str(exc)
        complete_trace(trace)
        raise HTTPException(status_code=500, detail=str(exc))


# ============================================================================
# AUTOMATIC STAY ANALYSIS ENDPOINT
# ============================================================================

class StayAnalysisRequest(BaseModel):
    """Request model for automatic stay analysis."""
    creditor_action: str = Field(..., description="Description of creditor action or proposed action")
    case_chapter: str = Field(default="7", description="Chapter under which case is filed")
    is_serial_filer: bool = Field(default=False)
    prior_dismissals_in_year: int = Field(default=0, ge=0, le=10)
    days_since_filing: int = Field(default=0, ge=0)
    creditor_is_secured: bool = Field(default=False)
    collateral_value: Optional[float] = Field(default=None, ge=0)
    debt_amount: Optional[float] = Field(default=None, ge=0)
    adequate_protection_offered: bool = Field(default=False)
    is_domestic_support: bool = Field(default=False)
    is_criminal_proceeding: bool = Field(default=False)
    is_tax_audit: bool = Field(default=False)
    has_equity_in_property: Optional[bool] = Field(default=None)
    property_necessary_for_reorg: Optional[bool] = Field(default=None)


@dataclass
class StayAnalysisResult:
    """Result of an automatic stay analysis."""
    stay_applicable: bool
    stay_scope: str
    exceptions_applicable: List[Dict[str, str]]
    serial_filer_limitation: Optional[Dict[str, Any]]
    relief_grounds: List[Dict[str, Any]]
    relief_likely: bool
    relief_confidence: float
    codebtor_stay: bool
    recommendations: List[str]
    citations: List[str]
    timeline: List[Dict[str, str]]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "stay_applicable": self.stay_applicable,
            "stay_scope": self.stay_scope,
            "exceptions_applicable": self.exceptions_applicable,
            "serial_filer_limitation": self.serial_filer_limitation,
            "relief_grounds": self.relief_grounds,
            "relief_likely": self.relief_likely,
            "relief_confidence": round(self.relief_confidence, 4),
            "codebtor_stay": self.codebtor_stay,
            "recommendations": self.recommendations,
            "citations": self.citations,
            "timeline": self.timeline,
        }


def analyze_automatic_stay(req: StayAnalysisRequest) -> StayAnalysisResult:
    """Analyze the automatic stay's applicability and potential for relief."""
    citations = ["11 USC 362(a)", "11 USC 362(b)", "11 USC 362(c)", "11 USC 362(d)"]
    exceptions: List[Dict[str, str]] = []
    relief_grounds: List[Dict[str, Any]] = []
    recommendations: List[str] = []
    timeline: List[Dict[str, str]] = []

    stay_applicable = True
    serial_limitation: Optional[Dict[str, Any]] = None
    codebtor_stay = req.case_chapter == "13"

    # Check serial filer limitations
    if req.prior_dismissals_in_year >= 2:
        stay_applicable = False
        serial_limitation = {
            "rule": "362(c)(4)",
            "effect": "NO automatic stay arises — must file motion to impose stay within 30 days",
            "prior_dismissals": req.prior_dismissals_in_year,
            "required_action": "File motion to impose stay showing good faith change in circumstances",
        }
        recommendations.append("URGENT: No automatic stay. File motion to impose stay immediately upon filing.")
        citations.append("11 USC 362(c)(4)")
    elif req.prior_dismissals_in_year == 1:
        serial_limitation = {
            "rule": "362(c)(3)",
            "effect": "Stay terminates after 30 days unless court extends upon showing of good faith",
            "prior_dismissals": 1,
            "required_action": "File motion to extend stay within 30 days of filing",
        }
        recommendations.append("Stay terminates in 30 days. File extension motion immediately.")
        citations.append("11 USC 362(c)(3)")

    # Check exceptions
    if req.is_criminal_proceeding:
        exceptions.append({
            "section": "362(b)(1)",
            "description": "Criminal proceedings are excepted from the automatic stay",
        })
    if req.is_domestic_support:
        exceptions.append({
            "section": "362(b)(2)",
            "description": "DSO establishment, modification, and collection from non-estate property excepted",
        })
    if req.is_tax_audit:
        exceptions.append({
            "section": "362(b)(9)",
            "description": "Tax audit proceedings are excepted from the automatic stay",
        })

    # Evaluate stay relief grounds
    relief_likely = False
    relief_confidence = 0.3

    if req.creditor_is_secured:
        # 362(d)(1): Lack of adequate protection
        if not req.adequate_protection_offered:
            relief_grounds.append({
                "section": "362(d)(1)",
                "ground": "Lack of adequate protection",
                "analysis": "Secured creditor may obtain relief if collateral is declining and no adequate protection offered",
                "strength": "moderate",
            })
            relief_confidence += 0.15

        # 362(d)(2): No equity and not necessary
        if req.has_equity_in_property is False and req.property_necessary_for_reorg is False:
            relief_grounds.append({
                "section": "362(d)(2)",
                "ground": "No equity and property not necessary for effective reorganization",
                "analysis": "Both prongs satisfied — stay relief likely",
                "strength": "strong",
            })
            relief_likely = True
            relief_confidence += 0.30
        elif req.has_equity_in_property is False:
            relief_grounds.append({
                "section": "362(d)(2)",
                "ground": "No equity (first prong met); necessity for reorganization to be determined",
                "analysis": "First prong met but second prong uncertain — depends on debtor's reorganization plan",
                "strength": "moderate",
            })
            relief_confidence += 0.10

        # Undersecured analysis
        if req.collateral_value is not None and req.debt_amount is not None:
            if req.collateral_value < req.debt_amount:
                equity_cushion = req.collateral_value / req.debt_amount if req.debt_amount > 0 else 0
                relief_grounds.append({
                    "section": "362(d)(1)",
                    "ground": f"Undersecured: collateral ${req.collateral_value:,.0f} vs debt ${req.debt_amount:,.0f}",
                    "analysis": f"Equity cushion: {equity_cushion:.1%}. Timbers: no interest as adequate protection for undersecured creditors.",
                    "strength": "moderate" if equity_cushion < 0.8 else "weak",
                })

    if not relief_likely and relief_confidence > 0.5:
        relief_likely = True

    # Build timeline
    timeline = [
        {"event": "Automatic stay takes effect", "when": "Immediately upon filing"},
        {"event": "Motion for stay relief filed by creditor", "when": "Any time after filing"},
        {"event": "Preliminary hearing on stay relief", "when": "Within 30 days of motion under 362(e)"},
        {"event": "Final hearing on stay relief", "when": "Within 30 days of preliminary hearing"},
    ]
    if serial_limitation:
        timeline.insert(1, {"event": "Motion to extend/impose stay filed", "when": "Within 30 days of filing"})

    # Recommendations
    if req.creditor_is_secured and not req.adequate_protection_offered:
        recommendations.append("Consider offering adequate protection to forestall stay relief motion")
    if relief_likely:
        recommendations.append("Stay relief appears likely — prepare for post-relief proceedings")
        if req.case_chapter in ("11", "13"):
            recommendations.append("Consider filing plan quickly to demonstrate reorganization viability")

    stay_scope = "Full automatic stay in effect" if stay_applicable else "No automatic stay (serial filer limitation)"

    return StayAnalysisResult(
        stay_applicable=stay_applicable,
        stay_scope=stay_scope,
        exceptions_applicable=exceptions,
        serial_filer_limitation=serial_limitation,
        relief_grounds=relief_grounds,
        relief_likely=relief_likely,
        relief_confidence=relief_confidence,
        codebtor_stay=codebtor_stay,
        recommendations=recommendations,
        citations=citations,
        timeline=timeline,
    )


@app.post("/stay-analysis")
async def handle_stay_analysis(request: StayAnalysisRequest) -> Dict[str, Any]:
    """Analyze the automatic stay's applicability and potential for relief."""
    trace = trace_query(f"stay_analysis: {request.creditor_action[:50]}", "analysis")
    record_bk_metric(BankruptcyMetricType.STAY_ANALYSIS)
    try:
        result = analyze_automatic_stay(request)
        trace.confidence = result.relief_confidence
        trace.response_layer = ResponseLayer.BANKRUPTCY_ANALYSIS
        complete_trace(trace)
        return {
            "engine_id": ENGINE_ID,
            "endpoint": "stay_analysis",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "result": result.to_dict(),
            "disclaimers": [REQUIRED_DISCLAIMERS["not_legal_advice"], REQUIRED_DISCLAIMERS["jurisdiction_specific"]],
        }
    except Exception as exc:
        trace.error = str(exc)
        complete_trace(trace)
        raise HTTPException(status_code=500, detail=str(exc))


# ============================================================================
# LIEN STRIP ANALYSIS ENDPOINT
# ============================================================================

class LienStripRequest(BaseModel):
    """Request model for lien strip analysis."""
    property_value: float = Field(..., ge=0, description="Current fair market value of property")
    first_mortgage_balance: float = Field(..., ge=0, description="First mortgage balance")
    second_mortgage_balance: float = Field(default=0.0, ge=0, description="Second mortgage/lien balance")
    third_mortgage_balance: float = Field(default=0.0, ge=0, description="Third mortgage/lien balance")
    is_principal_residence: bool = Field(default=True, description="Is this the debtor's principal residence")
    chapter: str = Field(default="13", description="Chapter under which case is filed (13 or 20)")
    has_prior_ch7_discharge: bool = Field(default=False, description="Has prior Chapter 7 discharge (Chapter 20)")


@dataclass
class LienStripResult:
    """Result of a lien strip analysis."""
    property_value: float
    first_mortgage: float
    equity_after_first: float
    second_lien_strippable: bool
    second_lien_balance: float
    second_lien_secured_portion: float
    second_lien_unsecured_portion: float
    third_lien_strippable: bool
    third_lien_balance: float
    chapter_20_applicable: bool
    total_lien_reduction: float
    recommendations: List[str]
    warnings: List[str]
    citations: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "property_value": round(self.property_value, 2),
            "first_mortgage": round(self.first_mortgage, 2),
            "equity_after_first": round(self.equity_after_first, 2),
            "second_lien_strippable": self.second_lien_strippable,
            "second_lien_balance": round(self.second_lien_balance, 2),
            "second_lien_secured_portion": round(self.second_lien_secured_portion, 2),
            "second_lien_unsecured_portion": round(self.second_lien_unsecured_portion, 2),
            "third_lien_strippable": self.third_lien_strippable,
            "third_lien_balance": round(self.third_lien_balance, 2),
            "chapter_20_applicable": self.chapter_20_applicable,
            "total_lien_reduction": round(self.total_lien_reduction, 2),
            "recommendations": self.recommendations,
            "warnings": self.warnings,
            "citations": self.citations,
        }


def analyze_lien_strip(req: LienStripRequest) -> LienStripResult:
    """Analyze lien stripping opportunity."""
    citations = ["11 USC 506(a)", "11 USC 1322(b)(2)"]
    recommendations: List[str] = []
    warnings: List[str] = []

    equity_after_first = req.property_value - req.first_mortgage_balance
    second_strippable = False
    second_secured = 0.0
    second_unsecured = req.second_mortgage_balance
    third_strippable = False
    total_reduction = 0.0
    ch20 = False

    if equity_after_first <= 0:
        # First mortgage is underwater — second lien is wholly unsecured
        second_strippable = True
        second_secured = 0.0
        second_unsecured = req.second_mortgage_balance
        total_reduction += req.second_mortgage_balance
        recommendations.append(
            f"Second lien of ${req.second_mortgage_balance:,.2f} is WHOLLY UNSECURED "
            f"(property value ${req.property_value:,.2f} < first mortgage ${req.first_mortgage_balance:,.2f}). "
            f"Eligible for lien stripping."
        )
        citations.append("Bank of America v. Caulkett, 575 U.S. 790 (2015)")

        # Third lien also strippable if second is wholly unsecured
        if req.third_mortgage_balance > 0:
            third_strippable = True
            total_reduction += req.third_mortgage_balance
            recommendations.append(
                f"Third lien of ${req.third_mortgage_balance:,.2f} is also wholly unsecured — strippable."
            )
    else:
        # Some equity exists after first mortgage
        if equity_after_first < req.second_mortgage_balance:
            # Second lien is undersecured but NOT wholly unsecured — CANNOT strip in Ch 7 per Caulkett
            second_secured = equity_after_first
            second_unsecured = req.second_mortgage_balance - equity_after_first
            second_strippable = False
            warnings.append(
                f"Second lien is PARTIALLY secured (${equity_after_first:,.2f} of ${req.second_mortgage_balance:,.2f}). "
                f"Cannot strip partially secured lien per Caulkett. Can bifurcate under 506(a) in Chapter 13."
            )
            # In Chapter 13, can bifurcate but not strip
            recommendations.append(
                f"In Chapter 13, second lien can be BIFURCATED: secured portion ${second_secured:,.2f}, "
                f"unsecured portion ${second_unsecured:,.2f}."
            )
        else:
            second_secured = req.second_mortgage_balance
            second_unsecured = 0.0
            warnings.append("Second lien is fully secured — no lien stripping available.")

        # Third lien analysis
        equity_after_second = equity_after_first - req.second_mortgage_balance
        if equity_after_second <= 0 and req.third_mortgage_balance > 0:
            third_strippable = True
            total_reduction += req.third_mortgage_balance
            recommendations.append(
                f"Third lien of ${req.third_mortgage_balance:,.2f} is wholly unsecured — strippable."
            )

    # Chapter 20 analysis
    if req.has_prior_ch7_discharge and second_strippable:
        ch20 = True
        recommendations.append(
            "Chapter 20 strategy applicable: Prior Chapter 7 discharge eliminates personal liability. "
            "Chapter 13 plan can strip wholly unsecured liens through plan completion "
            "(no Chapter 13 discharge required for lien strip to take effect)."
        )
        citations.extend([
            "Johnson v. Home State Bank, 501 U.S. 78 (1991)",
            "In re Branigan, 465 B.R. 492 (9th Cir. BAP 2012)",
        ])

    if req.chapter == "7" and second_strippable:
        warnings.append(
            "Lien stripping is NOT available in Chapter 7 per Caulkett/Dewsnup. "
            "Consider Chapter 13 or Chapter 20 strategy."
        )
        second_strippable = False
        total_reduction = 0.0

    if not req.is_principal_residence:
        recommendations.append(
            "Anti-modification rule (1322(b)(2)) does not apply to non-principal-residence property. "
            "Secured claims can be modified through Chapter 13 plan."
        )
        citations.append("Nobelman v. American Savings Bank, 508 U.S. 324 (1993)")

    return LienStripResult(
        property_value=req.property_value,
        first_mortgage=req.first_mortgage_balance,
        equity_after_first=equity_after_first,
        second_lien_strippable=second_strippable,
        second_lien_balance=req.second_mortgage_balance,
        second_lien_secured_portion=second_secured,
        second_lien_unsecured_portion=second_unsecured,
        third_lien_strippable=third_strippable,
        third_lien_balance=req.third_mortgage_balance,
        chapter_20_applicable=ch20,
        total_lien_reduction=total_reduction,
        recommendations=recommendations,
        warnings=warnings,
        citations=citations,
    )


@app.post("/lien-strip")
async def handle_lien_strip(request: LienStripRequest) -> Dict[str, Any]:
    """Analyze lien stripping opportunity."""
    trace = trace_query(f"lien_strip: value=${request.property_value} 1st=${request.first_mortgage_balance}", "analysis")
    record_bk_metric(BankruptcyMetricType.LIEN_STRIP_ANALYSIS)
    try:
        result = analyze_lien_strip(request)
        trace.confidence = 0.85
        trace.response_layer = ResponseLayer.BANKRUPTCY_ANALYSIS
        complete_trace(trace)
        return {
            "engine_id": ENGINE_ID,
            "endpoint": "lien_strip",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "result": result.to_dict(),
            "disclaimers": [REQUIRED_DISCLAIMERS["not_legal_advice"], REQUIRED_DISCLAIMERS["fact_dependent"]],
        }
    except Exception as exc:
        trace.error = str(exc)
        complete_trace(trace)
        raise HTTPException(status_code=500, detail=str(exc))


# ============================================================================
# DEBT TRIAGE ENDPOINT
# ============================================================================

class DebtTriageRequest(BaseModel):
    """Request model for debt triage analysis."""
    debts: List[Dict[str, Any]] = Field(..., min_length=1, description="List of debts with type, amount, creditor, secured status")


@app.post("/debt-triage")
async def handle_debt_triage(request: DebtTriageRequest) -> Dict[str, Any]:
    """Triage debts by dischargeability, priority, and treatment in bankruptcy."""
    trace = trace_query(f"debt_triage: {len(request.debts)} debts", "analysis")
    try:
        discharge_analyzer = get_discharge_analyzer()
        results: List[Dict[str, Any]] = []
        total_dischargeable = 0.0
        total_nondischargeable = 0.0
        total_secured = 0.0
        total_priority = 0.0
        total_general_unsecured = 0.0

        for debt in request.debts:
            debt_type = debt.get("type", "general")
            amount = float(debt.get("amount", 0))
            creditor = debt.get("creditor", "unknown")
            is_secured = debt.get("secured", False)
            is_priority = debt.get("priority", False)

            discharge_result = discharge_analyzer.analyze_discharge(
                debt_type=debt_type,
                debt_amount=amount,
                additional_facts=debt.get("facts", {}),
            )

            classification = "general_unsecured"
            if is_secured:
                classification = "secured"
                total_secured += amount
            elif is_priority:
                classification = "priority_unsecured"
                total_priority += amount
            else:
                total_general_unsecured += amount

            if discharge_result.dischargeable:
                total_dischargeable += amount
            else:
                total_nondischargeable += amount

            results.append({
                "creditor": creditor,
                "type": debt_type,
                "amount": round(amount, 2),
                "classification": classification,
                "dischargeable": discharge_result.dischargeable,
                "discharge_confidence": round(discharge_result.discharge_confidence, 4),
                "exceptions": discharge_result.applicable_exceptions,
                "risk_factors": discharge_result.risk_factors[:3],
            })

        trace.confidence = 0.80
        trace.response_layer = ResponseLayer.BANKRUPTCY_ANALYSIS
        complete_trace(trace)

        return {
            "engine_id": ENGINE_ID,
            "endpoint": "debt_triage",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "summary": {
                "total_debts": len(request.debts),
                "total_amount": round(sum(float(d.get("amount", 0)) for d in request.debts), 2),
                "total_dischargeable": round(total_dischargeable, 2),
                "total_nondischargeable": round(total_nondischargeable, 2),
                "total_secured": round(total_secured, 2),
                "total_priority": round(total_priority, 2),
                "total_general_unsecured": round(total_general_unsecured, 2),
                "discharge_percentage": round(
                    total_dischargeable / max(total_dischargeable + total_nondischargeable, 1) * 100, 1
                ),
            },
            "debts": results,
            "disclaimers": [REQUIRED_DISCLAIMERS["not_legal_advice"], REQUIRED_DISCLAIMERS["fact_dependent"]],
        }
    except Exception as exc:
        trace.error = str(exc)
        complete_trace(trace)
        raise HTTPException(status_code=500, detail=str(exc))


# ============================================================================
# TIMELINE GENERATOR ENDPOINT
# ============================================================================

@app.get("/timeline/{chapter}")
async def generate_timeline(
    chapter: str,
    filing_date: Optional[str] = Query(default=None, description="Filing date (YYYY-MM-DD)"),
) -> Dict[str, Any]:
    """Generate a procedural timeline for a bankruptcy case."""
    from datetime import timedelta
    base_date = datetime.now(timezone.utc)
    if filing_date:
        try:
            base_date = datetime.fromisoformat(filing_date).replace(tzinfo=timezone.utc)
        except ValueError:
            pass

    chapter_lower = chapter.lower().replace("chapter_", "").replace("chapter", "").strip()

    if chapter_lower == "7":
        timeline = [
            {"day": -180, "event": "Pre-filing credit counseling (must be within 180 days)", "required": True, "citation": "11 USC 109(h)"},
            {"day": 0, "event": "File Chapter 7 petition, schedules, SOFA, means test", "required": True, "citation": "FRBP 1002, 1007"},
            {"day": 0, "event": "Automatic stay takes effect", "required": False, "citation": "11 USC 362(a)"},
            {"day": 14, "event": "File remaining schedules if not filed with petition", "required": True, "citation": "FRBP 1007(c)"},
            {"day": 30, "event": "Provide tax returns to trustee (7 days before 341 meeting)", "required": True, "citation": "11 USC 521(e)"},
            {"day": 37, "event": "341 Meeting of Creditors (between 21-40 days after filing)", "required": True, "citation": "FRBP 2003(a)"},
            {"day": 67, "event": "Deadline for 727 objection to discharge (60 days after 341)", "required": False, "citation": "FRBP 4004(a)"},
            {"day": 67, "event": "Deadline for 523(c) dischargeability complaints (60 days after 341)", "required": False, "citation": "FRBP 4007(c)"},
            {"day": 67, "event": "Deadline for lien avoidance motions under 522(f)", "required": False, "citation": "11 USC 522(f)"},
            {"day": 97, "event": "Discharge entered (approximately 60 days after 341 meeting)", "required": False, "citation": "11 USC 727"},
            {"day": 97, "event": "Financial management course must be completed before discharge", "required": True, "citation": "11 USC 727(a)(11)"},
            {"day": 120, "event": "Case closed (typical)", "required": False, "citation": "11 USC 350"},
        ]
    elif chapter_lower == "13":
        timeline = [
            {"day": -180, "event": "Pre-filing credit counseling", "required": True, "citation": "11 USC 109(h)"},
            {"day": 0, "event": "File Chapter 13 petition, schedules, SOFA, plan", "required": True, "citation": "FRBP 1002, 3015"},
            {"day": 0, "event": "Automatic stay and co-debtor stay take effect", "required": False, "citation": "11 USC 362, 1301"},
            {"day": 14, "event": "File plan if not filed with petition", "required": True, "citation": "FRBP 3015(b)"},
            {"day": 30, "event": "First plan payment due (within 30 days of filing)", "required": True, "citation": "11 USC 1326(a)(1)"},
            {"day": 37, "event": "341 Meeting of Creditors", "required": True, "citation": "FRBP 2003(a)"},
            {"day": 67, "event": "Deadline for 523(c) complaints", "required": False, "citation": "FRBP 4007(c)"},
            {"day": 67, "event": "Deadline for objections to plan confirmation", "required": False, "citation": "FRBP 3015"},
            {"day": 90, "event": "Plan confirmation hearing (approximate)", "required": True, "citation": "11 USC 1324"},
            {"day": 1095, "event": "Plan completion (36 months for below-median)", "required": True, "citation": "11 USC 1325(b)(4)"},
            {"day": 1825, "event": "Plan completion (60 months for above-median)", "required": True, "citation": "11 USC 1325(b)(4)"},
            {"day": 1830, "event": "Discharge entered upon plan completion", "required": False, "citation": "11 USC 1328(a)"},
        ]
    elif chapter_lower == "11":
        timeline = [
            {"day": 0, "event": "File Chapter 11 petition, first day motions", "required": True, "citation": "FRBP 1002"},
            {"day": 0, "event": "Automatic stay takes effect, DIP status begins", "required": False, "citation": "11 USC 362, 1107"},
            {"day": 1, "event": "First day hearing (cash collateral, DIP financing, critical vendors)", "required": True, "citation": "11 USC 363, 364"},
            {"day": 37, "event": "341 Meeting of Creditors", "required": True, "citation": "FRBP 2003"},
            {"day": 45, "event": "Schedules and SOFA due (if not filed with petition)", "required": True, "citation": "FRBP 1007"},
            {"day": 120, "event": "Exclusivity period for plan filing (extendable to 18 months)", "required": False, "citation": "11 USC 1121(b)"},
            {"day": 180, "event": "Exclusivity period for plan solicitation (extendable to 20 months)", "required": False, "citation": "11 USC 1121(c)"},
            {"day": 150, "event": "Disclosure statement filed", "required": True, "citation": "11 USC 1125"},
            {"day": 180, "event": "Disclosure statement approved, solicitation begins", "required": True, "citation": "11 USC 1125(b)"},
            {"day": 210, "event": "Voting deadline", "required": True, "citation": "FRBP 3018"},
            {"day": 240, "event": "Plan confirmation hearing", "required": True, "citation": "11 USC 1128"},
            {"day": 270, "event": "Plan effective date", "required": False, "citation": "Plan terms"},
        ]
    else:
        timeline = [{"day": 0, "event": f"Filing date for Chapter {chapter_lower}", "required": True, "citation": "11 USC"}]

    # Add actual dates
    for item in timeline:
        try:
            item["date"] = (base_date + timedelta(days=item["day"])).strftime("%Y-%m-%d")
        except (OverflowError, ValueError):
            item["date"] = "N/A"

    return {
        "engine_id": ENGINE_ID,
        "endpoint": "timeline",
        "chapter": chapter_lower,
        "filing_date": base_date.strftime("%Y-%m-%d"),
        "timeline": timeline,
        "disclaimers": [
            REQUIRED_DISCLAIMERS["not_legal_advice"],
            "Actual deadlines may vary based on local rules and court orders.",
        ],
    }


# ============================================================================
# BATCH QUERY ENDPOINT
# ============================================================================

class BatchQueryRequest(BaseModel):
    """Request model for batch queries."""
    queries: List[str] = Field(..., min_length=1, max_length=10, description="List of queries to process")
    mode: ResponseMode = Field(default=ResponseMode.FAST)


@app.post("/batch-query")
async def handle_batch_query(request: BatchQueryRequest) -> Dict[str, Any]:
    """Process multiple bankruptcy law queries in batch."""
    results: List[Dict[str, Any]] = []
    total_start = time.monotonic()

    for q in request.queries:
        try:
            response = process_query(query=q, mode=request.mode)
            results.append({
                "query": q,
                "status": "success",
                "confidence": response.confidence,
                "confidence_band": response.confidence_band,
                "response_layer": response.response_layer,
                "doctrine_count": len(response.doctrine_hits),
                "top_doctrine": response.doctrine_hits[0]["topic"] if response.doctrine_hits else None,
                "timing_ms": response.timing_ms,
            })
        except Exception as exc:
            results.append({
                "query": q,
                "status": "error",
                "error": str(exc),
            })

    total_ms = (time.monotonic() - total_start) * 1000.0
    return {
        "engine_id": ENGINE_ID,
        "endpoint": "batch_query",
        "total_queries": len(request.queries),
        "successful": sum(1 for r in results if r["status"] == "success"),
        "failed": sum(1 for r in results if r["status"] == "error"),
        "total_time_ms": round(total_ms, 3),
        "results": results,
    }


# ============================================================================
# REAFFIRMATION AGREEMENT ANALYZER
# ============================================================================

class ReaffirmationRequest(BaseModel):
    """Request model for reaffirmation agreement analysis."""
    debt_type: str = Field(..., description="Type of debt (auto_loan, mortgage, credit_card, personal_loan)")
    debt_balance: float = Field(..., ge=0, description="Current balance of the debt")
    collateral_value: float = Field(default=0.0, ge=0, description="Current value of collateral")
    monthly_payment: float = Field(default=0.0, ge=0, description="Monthly payment on the debt")
    interest_rate: float = Field(default=0.0, ge=0, le=100, description="Annual interest rate")
    debtor_monthly_income: float = Field(default=0.0, ge=0, description="Debtor's gross monthly income")
    debtor_monthly_expenses: float = Field(default=0.0, ge=0, description="Debtor's total monthly expenses")
    is_represented: bool = Field(default=True, description="Debtor has attorney representation")
    debtor_is_current: bool = Field(default=True, description="Debtor is current on payments")
    remaining_months: int = Field(default=60, ge=1, description="Remaining months on loan")


@dataclass
class ReaffirmationResult:
    """Result of reaffirmation agreement analysis."""
    recommended: bool
    recommendation_strength: str
    undue_hardship_flag: bool
    presumption_of_undue_hardship: bool
    net_benefit: float
    cost_to_replace: float
    equity_in_collateral: float
    monthly_budget_impact: float
    alternatives: List[Dict[str, str]]
    risks: List[str]
    benefits: List[str]
    legal_requirements: List[str]
    citations: List[str]
    court_approval_required: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "recommended": self.recommended,
            "recommendation_strength": self.recommendation_strength,
            "undue_hardship_flag": self.undue_hardship_flag,
            "presumption_of_undue_hardship": self.presumption_of_undue_hardship,
            "net_benefit": round(self.net_benefit, 2),
            "cost_to_replace": round(self.cost_to_replace, 2),
            "equity_in_collateral": round(self.equity_in_collateral, 2),
            "monthly_budget_impact": round(self.monthly_budget_impact, 2),
            "alternatives": self.alternatives,
            "risks": self.risks,
            "benefits": self.benefits,
            "legal_requirements": self.legal_requirements,
            "citations": self.citations,
            "court_approval_required": self.court_approval_required,
        }


def analyze_reaffirmation(req: ReaffirmationRequest) -> ReaffirmationResult:
    """Analyze whether a reaffirmation agreement is advisable."""
    citations = [
        "11 USC 524(c)", "11 USC 524(d)", "11 USC 524(k)",
        "11 USC 521(a)(2)", "11 USC 362(h)",
    ]
    risks: List[str] = []
    benefits: List[str] = []
    alternatives: List[Dict[str, str]] = []
    requirements: List[str] = []

    equity = req.collateral_value - req.debt_balance
    disposable_income = req.debtor_monthly_income - req.debtor_monthly_expenses
    budget_impact = req.monthly_payment / max(req.debtor_monthly_income, 1)

    # Presumption of undue hardship: Schedule I/J shows negative disposable income
    presumption_hardship = disposable_income < req.monthly_payment
    undue_hardship = disposable_income < 0 or (disposable_income < req.monthly_payment * 0.5)

    # Legal requirements
    requirements.append("Agreement must be made before discharge is granted")
    requirements.append("Debtor must receive all required disclosures under 524(k)")
    requirements.append("Agreement must be filed with the court")
    if not req.is_represented:
        requirements.append("COURT APPROVAL REQUIRED: Debtor is not represented by attorney")
        requirements.append("Court must find agreement does not impose undue hardship")
        requirements.append("Court must find agreement is in debtor's best interest")
    else:
        requirements.append("Attorney must certify debtor was fully advised")
        requirements.append("Attorney must certify agreement does not impose undue hardship")
        requirements.append("Attorney must certify debtor is able to make payments")
    requirements.append("Debtor has 60 days after filing to rescind the agreement")
    requirements.append("Agreement is not enforceable if required disclosures are lacking")

    court_approval = not req.is_represented or presumption_hardship

    # Benefits analysis
    if equity > 0:
        benefits.append(f"Preserve ${equity:,.2f} equity in collateral")
    if req.debtor_is_current:
        benefits.append("Maintain positive payment history and credit relationship")
    if req.debt_type == "auto_loan":
        benefits.append("Retain vehicle — essential for transportation and employment")
        cost_to_replace = req.collateral_value * 1.15  # Replacement cost premium
    elif req.debt_type == "mortgage":
        benefits.append("Retain home — provides housing stability")
        cost_to_replace = req.collateral_value * 1.20
    else:
        cost_to_replace = req.collateral_value

    if req.interest_rate < 8.0 and equity >= 0:
        benefits.append(f"Favorable interest rate ({req.interest_rate:.1f}%) — better than replacement financing")

    # Risk analysis
    if presumption_hardship:
        risks.append("PRESUMPTION OF UNDUE HARDSHIP: Budget shows insufficient income to cover payment")
    if undue_hardship:
        risks.append("Reaffirmation may impose undue hardship — debtor cannot afford payments")
    if equity < 0:
        risks.append(f"Negative equity of ${abs(equity):,.2f} — debtor underwater on collateral")
        risks.append("Debtor would owe balance after surrendering collateral if reaffirmed")
    if budget_impact > 0.25:
        risks.append(f"Payment consumes {budget_impact:.0%} of gross income — high debt burden")
    if req.remaining_months > 60:
        risks.append(f"Long remaining term ({req.remaining_months} months) increases total cost")
    risks.append("Debt survives bankruptcy — no second chance if financial difficulty recurs")
    risks.append("Deficiency liability restored — creditor can sue for deficiency after repossession")

    # Alternatives
    alternatives.append({
        "option": "Surrender collateral",
        "description": "Surrender collateral and discharge the debt entirely. "
                       f"Lose collateral worth ${req.collateral_value:,.2f} but eliminate ${req.debt_balance:,.2f} debt.",
        "best_when": "Negative equity, high payments, or collateral not essential",
    })
    alternatives.append({
        "option": "Redemption under 722",
        "description": f"Pay lump sum equal to replacement value (${req.collateral_value:,.2f}) to redeem collateral. "
                       "Must be paid in full at time of redemption.",
        "best_when": "Collateral value less than debt balance and debtor has lump sum available",
    })
    if req.debt_type == "auto_loan":
        alternatives.append({
            "option": "Ride-through (if available in jurisdiction)",
            "description": "Continue making payments without formal reaffirmation. "
                           "Not available in all circuits after BAPCPA.",
            "best_when": "Debtor wants to keep property but avoid deficiency risk",
        })
    if req.debt_type == "mortgage":
        alternatives.append({
            "option": "Retain and pay (informal ride-through)",
            "description": "Continue mortgage payments without reaffirming. "
                           "Lien passes through bankruptcy — keep paying to keep house. "
                           "No personal liability but lien remains.",
            "best_when": "Debtor wants to keep home but does not want to restore personal liability",
        })

    # Net benefit calculation
    total_cost_reaffirm = req.monthly_payment * req.remaining_months
    net_benefit = req.collateral_value - total_cost_reaffirm
    if equity < 0 and undue_hardship:
        net_benefit -= abs(equity) * 2  # Penalty for underwater + hardship

    # Recommendation
    recommended = False
    strength = "weak"

    if equity >= 0 and not undue_hardship and not presumption_hardship:
        recommended = True
        strength = "strong"
    elif equity >= 0 and not undue_hardship:
        recommended = True
        strength = "moderate"
    elif equity < 0 and not undue_hardship and req.debt_type in ("auto_loan", "mortgage"):
        # Essential asset, manageable payments
        if budget_impact < 0.20:
            recommended = True
            strength = "weak"
        else:
            recommended = False
            strength = "not_recommended"
    else:
        recommended = False
        strength = "not_recommended"

    return ReaffirmationResult(
        recommended=recommended,
        recommendation_strength=strength,
        undue_hardship_flag=undue_hardship,
        presumption_of_undue_hardship=presumption_hardship,
        net_benefit=net_benefit,
        cost_to_replace=cost_to_replace,
        equity_in_collateral=equity,
        monthly_budget_impact=budget_impact,
        alternatives=alternatives,
        risks=risks,
        benefits=benefits,
        legal_requirements=requirements,
        citations=citations,
        court_approval_required=court_approval,
    )


@app.post("/reaffirmation")
async def handle_reaffirmation(request: ReaffirmationRequest) -> Dict[str, Any]:
    """Analyze whether a reaffirmation agreement is advisable."""
    trace = trace_query(f"reaffirmation: {request.debt_type} ${request.debt_balance:,.0f}", "analysis")
    record_bk_metric(BankruptcyMetricType.DISCHARGE_DETERMINATION)
    try:
        result = analyze_reaffirmation(request)
        trace.confidence = 0.82 if result.recommended else 0.75
        trace.response_layer = ResponseLayer.BANKRUPTCY_ANALYSIS
        complete_trace(trace)
        return {
            "engine_id": ENGINE_ID,
            "endpoint": "reaffirmation",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "result": result.to_dict(),
            "disclaimers": [
                REQUIRED_DISCLAIMERS["not_legal_advice"],
                REQUIRED_DISCLAIMERS["fact_dependent"],
                "Reaffirmation decisions have significant long-term financial consequences. "
                "This analysis is a starting point, not a substitute for attorney advice.",
            ],
        }
    except Exception as exc:
        trace.error = str(exc)
        complete_trace(trace)
        raise HTTPException(status_code=500, detail=str(exc))


# ============================================================================
# CHAPTER 13 PLAN FEASIBILITY CALCULATOR
# ============================================================================

class PlanFeasibilityRequest(BaseModel):
    """Request model for Chapter 13 plan feasibility analysis."""
    monthly_gross_income: float = Field(..., ge=0, description="Monthly gross income from all sources")
    monthly_taxes_withheld: float = Field(default=0.0, ge=0, description="Monthly tax withholding")
    monthly_social_security: float = Field(default=0.0, ge=0, description="Monthly SS/Medicare withholding")
    monthly_health_insurance: float = Field(default=0.0, ge=0, description="Monthly health insurance premium")
    monthly_retirement_mandatory: float = Field(default=0.0, ge=0, description="Mandatory retirement contributions")
    monthly_living_expenses: float = Field(default=0.0, ge=0, description="Reasonable living expenses")
    monthly_mortgage: float = Field(default=0.0, ge=0, description="Monthly mortgage payment")
    monthly_auto_payment: float = Field(default=0.0, ge=0, description="Monthly auto loan payment")
    monthly_child_support: float = Field(default=0.0, ge=0, description="Monthly DSO obligations")
    mortgage_arrears: float = Field(default=0.0, ge=0, description="Total mortgage arrears to cure")
    priority_tax_debt: float = Field(default=0.0, ge=0, description="Priority tax debt (3/2/240 not met)")
    domestic_support_arrears: float = Field(default=0.0, ge=0, description="DSO arrears")
    total_unsecured_debt: float = Field(default=0.0, ge=0, description="Total general unsecured claims")
    non_exempt_asset_value: float = Field(default=0.0, ge=0, description="Value of non-exempt assets (liquidation test)")
    household_size: int = Field(default=1, ge=1, le=15)
    state: str = Field(default="TX")
    is_above_median: bool = Field(default=False)


@dataclass
class PlanFeasibilityResult:
    """Result of plan feasibility analysis."""
    monthly_disposable_income: float
    plan_length_months: int
    monthly_plan_payment: float
    total_plan_payments: float
    priority_claims_payable: bool
    liquidation_test_met: bool
    minimum_unsecured_pct: float
    projected_unsecured_pct: float
    feasible: bool
    feasibility_score: float
    monthly_budget_breakdown: Dict[str, float]
    plan_summary: Dict[str, Any]
    issues: List[str]
    recommendations: List[str]
    citations: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "monthly_disposable_income": round(self.monthly_disposable_income, 2),
            "plan_length_months": self.plan_length_months,
            "monthly_plan_payment": round(self.monthly_plan_payment, 2),
            "total_plan_payments": round(self.total_plan_payments, 2),
            "priority_claims_payable": self.priority_claims_payable,
            "liquidation_test_met": self.liquidation_test_met,
            "minimum_unsecured_pct": round(self.minimum_unsecured_pct, 2),
            "projected_unsecured_pct": round(self.projected_unsecured_pct, 2),
            "feasible": self.feasible,
            "feasibility_score": round(self.feasibility_score, 4),
            "monthly_budget_breakdown": {k: round(v, 2) for k, v in self.monthly_budget_breakdown.items()},
            "plan_summary": self.plan_summary,
            "issues": self.issues,
            "recommendations": self.recommendations,
            "citations": self.citations,
        }


def calculate_plan_feasibility(req: PlanFeasibilityRequest) -> PlanFeasibilityResult:
    """Calculate Chapter 13 plan feasibility."""
    citations = [
        "11 USC 1325(a)(4)", "11 USC 1325(a)(6)", "11 USC 1325(b)",
        "11 USC 1322(a)(1)", "11 USC 1326(a)",
    ]
    issues: List[str] = []
    recommendations: List[str] = []

    # Calculate net disposable income
    payroll_deductions = (
        req.monthly_taxes_withheld + req.monthly_social_security
        + req.monthly_health_insurance + req.monthly_retirement_mandatory
    )
    net_income = req.monthly_gross_income - payroll_deductions

    total_expenses = (
        req.monthly_living_expenses + req.monthly_mortgage
        + req.monthly_auto_payment + req.monthly_child_support
    )

    disposable_income = net_income - total_expenses

    budget_breakdown = {
        "gross_income": req.monthly_gross_income,
        "payroll_deductions": payroll_deductions,
        "net_income": net_income,
        "living_expenses": req.monthly_living_expenses,
        "mortgage": req.monthly_mortgage,
        "auto_payment": req.monthly_auto_payment,
        "child_support": req.monthly_child_support,
        "total_expenses": total_expenses,
        "disposable_income": disposable_income,
    }

    # Plan length: above-median = 60 months, below = 36-60
    plan_months = 60 if req.is_above_median else 36

    # Must-pay amounts through plan
    must_pay_priority = req.priority_tax_debt + req.domestic_support_arrears
    must_pay_arrears = req.mortgage_arrears
    total_must_pay = must_pay_priority + must_pay_arrears

    # Monthly plan payment = disposable income (projected, per Lanning)
    monthly_plan = max(disposable_income, 0)
    total_plan = monthly_plan * plan_months

    # Trustee fee (typically 5-10%)
    trustee_fee_pct = 0.07
    total_after_trustee = total_plan * (1.0 - trustee_fee_pct)

    # Check: can priority claims and cure arrears be paid in full?
    priority_payable = total_after_trustee >= total_must_pay
    if not priority_payable:
        issues.append(
            f"PLAN INFEASIBLE: Priority claims (${total_must_pay:,.2f}) exceed "
            f"total plan capacity (${total_after_trustee:,.2f}). "
            f"Priority claims must be paid in full under 1322(a)(1)."
        )

    # Liquidation test: unsecured creditors must receive at least what they
    # would get in Chapter 7 (i.e., value of non-exempt assets)
    amount_available_for_unsecured = max(total_after_trustee - total_must_pay, 0)
    liquidation_test_met = amount_available_for_unsecured >= req.non_exempt_asset_value

    if not liquidation_test_met:
        issues.append(
            f"LIQUIDATION TEST FAILURE: Plan provides ${amount_available_for_unsecured:,.2f} "
            f"to unsecured creditors, less than ${req.non_exempt_asset_value:,.2f} "
            f"they would receive in Chapter 7 liquidation."
        )
        citations.append("11 USC 1325(a)(4)")

    # Unsecured percentage
    min_unsecured_pct = (req.non_exempt_asset_value / max(req.total_unsecured_debt, 1)) * 100
    projected_unsecured_pct = (amount_available_for_unsecured / max(req.total_unsecured_debt, 1)) * 100

    # Feasibility (1325(a)(6): debtor will be able to make all payments)
    feasible = True
    feasibility_score = 0.80

    if disposable_income <= 0:
        feasible = False
        feasibility_score = 0.10
        issues.append("No disposable income — plan payments cannot be funded")
    elif disposable_income < 100:
        issues.append(f"Very low disposable income (${disposable_income:,.2f}/mo) — plan vulnerable to any income disruption")
        feasibility_score = 0.35
    elif not priority_payable:
        feasible = False
        feasibility_score = 0.20
    elif not liquidation_test_met:
        feasibility_score = 0.45
        recommendations.append("Increase plan payment or extend plan length to meet liquidation test")

    if disposable_income > 0 and total_plan > total_must_pay:
        feasibility_score = min(feasibility_score + 0.15, 0.95)

    # Recommendations
    if feasible and disposable_income > 500:
        recommendations.append("Plan appears feasible with adequate disposable income cushion")
    if req.is_above_median and plan_months == 60:
        recommendations.append("Above-median debtor: 60-month plan commitment required (applicable commitment period)")
    elif not req.is_above_median and plan_months == 36:
        recommendations.append("Below-median debtor: 36-month minimum. Can extend to 60 months if needed to meet liquidation test.")
    if req.mortgage_arrears > 0:
        monthly_cure = req.mortgage_arrears / plan_months
        recommendations.append(f"Mortgage cure: ${monthly_cure:,.2f}/month over {plan_months} months to cure ${req.mortgage_arrears:,.2f} arrears")
    if projected_unsecured_pct < 10:
        recommendations.append(f"Low unsecured dividend ({projected_unsecured_pct:.1f}%). Court may scrutinize good faith under 1325(a)(3).")
    if projected_unsecured_pct >= 100:
        recommendations.append("100% plan — all unsecured creditors paid in full. Consider shorter plan term.")

    plan_summary = {
        "plan_length_months": plan_months,
        "monthly_payment": round(monthly_plan, 2),
        "total_payments": round(total_plan, 2),
        "trustee_fee_pct": trustee_fee_pct,
        "amount_to_trustee": round(total_plan, 2),
        "trustee_fee": round(total_plan * trustee_fee_pct, 2),
        "net_after_trustee": round(total_after_trustee, 2),
        "priority_claims": round(total_must_pay, 2),
        "mortgage_cure": round(req.mortgage_arrears, 2),
        "amount_for_unsecured": round(amount_available_for_unsecured, 2),
        "unsecured_percentage": round(projected_unsecured_pct, 1),
    }

    return PlanFeasibilityResult(
        monthly_disposable_income=disposable_income,
        plan_length_months=plan_months,
        monthly_plan_payment=monthly_plan,
        total_plan_payments=total_plan,
        priority_claims_payable=priority_payable,
        liquidation_test_met=liquidation_test_met,
        minimum_unsecured_pct=min_unsecured_pct,
        projected_unsecured_pct=projected_unsecured_pct,
        feasible=feasible,
        feasibility_score=feasibility_score,
        monthly_budget_breakdown=budget_breakdown,
        plan_summary=plan_summary,
        issues=issues,
        recommendations=recommendations,
        citations=citations,
    )


@app.post("/plan-feasibility")
async def handle_plan_feasibility(request: PlanFeasibilityRequest) -> Dict[str, Any]:
    """Calculate Chapter 13 plan feasibility."""
    trace = trace_query(f"plan_feasibility: income=${request.monthly_gross_income:,.0f}", "plan_review")
    record_bk_metric(BankruptcyMetricType.PLAN_FEASIBILITY)
    try:
        result = calculate_plan_feasibility(request)
        trace.confidence = result.feasibility_score
        trace.response_layer = ResponseLayer.BANKRUPTCY_ANALYSIS
        complete_trace(trace)
        return {
            "engine_id": ENGINE_ID,
            "endpoint": "plan_feasibility",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "result": result.to_dict(),
            "disclaimers": [
                REQUIRED_DISCLAIMERS["not_legal_advice"],
                REQUIRED_DISCLAIMERS["fact_dependent"],
                "Plan feasibility is ultimately determined by the bankruptcy court. "
                "This projection uses forward-looking income per Hamilton v. Lanning, 560 U.S. 505 (2010).",
            ],
        }
    except Exception as exc:
        trace.error = str(exc)
        complete_trace(trace)
        raise HTTPException(status_code=500, detail=str(exc))


# ============================================================================
# ADVERSARY PROCEEDING EVALUATOR
# ============================================================================

class AdversaryRequest(BaseModel):
    """Request model for adversary proceeding analysis."""
    cause_of_action: str = Field(..., description="Type of adversary proceeding")
    factual_summary: str = Field(default="", description="Brief factual summary")
    amount_at_issue: float = Field(default=0.0, ge=0, description="Dollar amount at issue")
    is_plaintiff_debtor: bool = Field(default=False, description="Is the debtor the plaintiff?")
    is_plaintiff_trustee: bool = Field(default=False, description="Is the trustee the plaintiff?")
    is_plaintiff_creditor: bool = Field(default=False, description="Is a creditor the plaintiff?")
    days_since_341: Optional[int] = Field(default=None, ge=0, description="Days since 341 meeting")
    filing_deadline_known: bool = Field(default=False)


@dataclass
class AdversaryResult:
    """Result of adversary proceeding analysis."""
    proceeding_type: str
    frbp_rule: str
    elements: List[str]
    defenses: List[str]
    burden_of_proof: str
    bar_date_info: str
    bar_date_days_remaining: Optional[int]
    statute_of_limitations: str
    filing_fee: str
    discovery_scope: str
    estimated_complexity: str
    strategic_considerations: List[str]
    likely_outcomes: List[Dict[str, str]]
    citations: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "proceeding_type": self.proceeding_type,
            "frbp_rule": self.frbp_rule,
            "elements": self.elements,
            "defenses": self.defenses,
            "burden_of_proof": self.burden_of_proof,
            "bar_date_info": self.bar_date_info,
            "bar_date_days_remaining": self.bar_date_days_remaining,
            "statute_of_limitations": self.statute_of_limitations,
            "filing_fee": self.filing_fee,
            "discovery_scope": self.discovery_scope,
            "estimated_complexity": self.estimated_complexity,
            "strategic_considerations": self.strategic_considerations,
            "likely_outcomes": self.likely_outcomes,
            "citations": self.citations,
        }


# Adversary proceeding type database
ADVERSARY_TYPES: Dict[str, Dict[str, Any]] = {
    "preference": {
        "frbp": "FRBP 7001(1)",
        "elements": [
            "Transfer of debtor's interest in property",
            "To or for the benefit of a creditor",
            "On account of antecedent debt",
            "Made while debtor was insolvent",
            "Within 90 days before petition (1 year for insiders)",
            "Enables creditor to receive more than in Chapter 7 liquidation",
        ],
        "defenses": [
            "Contemporaneous exchange for new value (547(c)(1))",
            "Ordinary course of business (547(c)(2))",
            "Purchase money security interest (547(c)(3))",
            "Subsequent new value (547(c)(4))",
            "Floating lien (547(c)(5))",
            "Small preference safe harbor: consumer <$600, business <$7,575 (547(c)(9))",
        ],
        "burden": "Trustee bears burden of proving elements; defendant bears burden of proving defenses",
        "sol": "2 years after order for relief (11 USC 546(a))",
        "fee": "$350 filing fee",
        "complexity": "moderate",
        "citations": ["11 USC 547", "11 USC 546(a)", "FRBP 7001"],
    },
    "fraudulent_transfer": {
        "frbp": "FRBP 7001(1)",
        "elements": [
            "Transfer of debtor's interest in property (actual fraud: intent to hinder, delay, or defraud)",
            "Constructive fraud: reasonably equivalent value not received AND insolvent/undercapitalized",
        ],
        "defenses": [
            "Good faith transferee for value (548(c))",
            "Charitable contribution defense (548(a)(2))",
            "Securities settlement payment defense (546(e))",
            "Statute of limitations expired",
        ],
        "burden": "Trustee/plaintiff bears burden; badges of fraud create rebuttable inference for actual fraud",
        "sol": "2 years under 548; state law may extend via 544(b)",
        "fee": "$350 filing fee",
        "complexity": "high",
        "citations": ["11 USC 548", "11 USC 544(b)", "FRBP 7001"],
    },
    "discharge_objection": {
        "frbp": "FRBP 7001(4)",
        "elements": [
            "Specific ground under 727(a): fraud, concealment, destruction of records, "
            "failure to explain loss of assets, prior discharge within 8/6 years, "
            "failure to complete financial management course",
        ],
        "defenses": [
            "No intent to defraud",
            "Records adequate to ascertain financial condition",
            "Satisfactory explanation for asset loss",
            "Time bar not triggered (prior discharge long enough ago)",
        ],
        "burden": "Objecting party bears burden of proving 727(a) ground by preponderance",
        "sol": "60 days after first date set for 341 meeting (FRBP 4004(a))",
        "fee": "$350 filing fee",
        "complexity": "moderate",
        "citations": ["11 USC 727(a)", "FRBP 4004", "FRBP 7001"],
    },
    "dischargeability": {
        "frbp": "FRBP 7001(6)",
        "elements": [
            "Specific debt falls within 523(a) exception category",
            "For 523(a)(2)(fraud), (4)(fiduciary/embezzlement), (6)(willful/malicious): "
            "timely complaint required within 60 days after 341 meeting",
        ],
        "defenses": [
            "Debt does not fit statutory exception",
            "Required elements not proved",
            "Complaint not timely filed (for 523(c) debts)",
            "Settlement of underlying claim",
        ],
        "burden": "Creditor bears burden of proving nondischargeability by preponderance; "
                  "523(a)(2) requires actual fraud showing",
        "sol": "523(c) debts: 60 days after 341 meeting; other 523(a) debts: any time",
        "fee": "$350 filing fee",
        "complexity": "moderate",
        "citations": ["11 USC 523", "FRBP 4007", "FRBP 7001"],
    },
    "lien_avoidance": {
        "frbp": "FRBP 7001(2) (or motion under some local rules)",
        "elements": [
            "Lien impairs exemption debtor could claim under 522(b)",
            "Lien is judicial lien or nonpossessory nonpurchase-money security interest",
            "Property is of a type that would be exempt absent the lien",
        ],
        "defenses": [
            "Lien is consensual/purchase-money",
            "Property not exempt even without lien",
            "Insufficient value to support exemption impairment finding",
        ],
        "burden": "Debtor bears burden of demonstrating lien impairment of exemption",
        "sol": "Before case closure; typically at or before discharge",
        "fee": "$0 if by motion; $350 if adversary complaint",
        "complexity": "low",
        "citations": ["11 USC 522(f)", "FRBP 4003(d)", "FRBP 7001"],
    },
}


def evaluate_adversary(req: AdversaryRequest) -> AdversaryResult:
    """Evaluate an adversary proceeding."""
    cause_lower = req.cause_of_action.lower().replace(" ", "_").replace("-", "_")

    # Match to known type
    matched_type = None
    for type_key, type_data in ADVERSARY_TYPES.items():
        if type_key in cause_lower or cause_lower in type_key:
            matched_type = type_key
            break

    if matched_type is None:
        # Default for unknown type
        matched_type = "dischargeability"
        if "prefer" in cause_lower:
            matched_type = "preference"
        elif "fraud" in cause_lower:
            matched_type = "fraudulent_transfer"
        elif "discharge" in cause_lower and "ability" not in cause_lower:
            matched_type = "discharge_objection"
        elif "lien" in cause_lower or "avoid" in cause_lower:
            matched_type = "lien_avoidance"

    type_info = ADVERSARY_TYPES[matched_type]

    # Bar date calculation
    bar_date_days: Optional[int] = None
    bar_date_info = type_info["sol"]
    if req.days_since_341 is not None:
        if matched_type in ("discharge_objection", "dischargeability"):
            remaining = 60 - req.days_since_341
            bar_date_days = max(remaining, 0)
            if remaining <= 0:
                bar_date_info = f"BAR DATE EXPIRED: 60-day deadline passed {abs(remaining)} days ago"
            elif remaining <= 14:
                bar_date_info = f"URGENT: Only {remaining} days remaining to file complaint"
            else:
                bar_date_info = f"{remaining} days remaining until 60-day bar date"

    # Strategic considerations
    strategic: List[str] = []
    if req.is_plaintiff_trustee and matched_type in ("preference", "fraudulent_transfer"):
        strategic.append("Trustee avoidance actions benefit the estate — recovered funds distributed to all creditors")
        strategic.append("Consider demand letter before filing — many preferences settle pre-litigation")
        if req.amount_at_issue < 7575 and matched_type == "preference":
            strategic.append(f"WARNING: Transfer of ${req.amount_at_issue:,.0f} may fall under small preference safe harbor ($7,575)")
    if req.is_plaintiff_creditor and matched_type in ("discharge_objection", "dischargeability"):
        strategic.append("Creditor must file complaint within strict bar dates — monitor 341 meeting scheduling")
        strategic.append("Consider whether litigation cost justifies potential recovery")
    if matched_type == "discharge_objection":
        strategic.append("Denial of discharge affects ALL debts — severe consequence for debtor")
        strategic.append("Courts construe 727(a) liberally in favor of debtor — high burden on objector")
    if matched_type == "lien_avoidance":
        strategic.append("Lien avoidance can often be accomplished by motion rather than adversary proceeding")
        strategic.append("Check local rules — some districts allow 522(f) motions without adversary")

    # Likely outcomes
    outcomes: List[Dict[str, str]] = [
        {
            "outcome": "Plaintiff prevails",
            "probability": "varies by facts",
            "effect": f"Recovery/relief of ${req.amount_at_issue:,.0f}" if req.amount_at_issue > 0 else "Relief granted",
        },
        {
            "outcome": "Settlement",
            "probability": "common (60-70% of avoidance actions)",
            "effect": "Negotiated resolution, typically 30-60% of claimed amount",
        },
        {
            "outcome": "Defendant prevails",
            "probability": "varies by facts",
            "effect": "Claim dismissed, status quo preserved",
        },
    ]

    return AdversaryResult(
        proceeding_type=matched_type,
        frbp_rule=type_info["frbp"],
        elements=type_info["elements"],
        defenses=type_info["defenses"],
        burden_of_proof=type_info["burden"],
        bar_date_info=bar_date_info,
        bar_date_days_remaining=bar_date_days,
        statute_of_limitations=type_info["sol"],
        filing_fee=type_info["fee"],
        discovery_scope="Full FRBP Part VII discovery (interrogatories, depositions, document requests, RFAs)",
        estimated_complexity=type_info["complexity"],
        strategic_considerations=strategic,
        likely_outcomes=outcomes,
        citations=type_info["citations"],
    )


@app.post("/adversary")
async def handle_adversary(request: AdversaryRequest) -> Dict[str, Any]:
    """Evaluate an adversary proceeding."""
    trace = trace_query(f"adversary: {request.cause_of_action}", "analysis")
    record_bk_metric(BankruptcyMetricType.ADVERSARY_PROCEEDING)
    try:
        result = evaluate_adversary(request)
        trace.confidence = 0.78
        trace.response_layer = ResponseLayer.BANKRUPTCY_ANALYSIS
        complete_trace(trace)
        return {
            "engine_id": ENGINE_ID,
            "endpoint": "adversary",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "result": result.to_dict(),
            "disclaimers": [
                REQUIRED_DISCLAIMERS["not_legal_advice"],
                REQUIRED_DISCLAIMERS["jurisdiction_specific"],
                "Adversary proceeding strategy should be developed with bankruptcy litigation counsel.",
            ],
        }
    except Exception as exc:
        trace.error = str(exc)
        complete_trace(trace)
        raise HTTPException(status_code=500, detail=str(exc))


# ============================================================================
# CREDITOR PRIORITY WATERFALL CALCULATOR
# ============================================================================

class WaterfallRequest(BaseModel):
    """Request model for creditor priority waterfall calculation."""
    total_estate_value: float = Field(..., ge=0, description="Total liquidation value of estate")
    admin_claims_503: float = Field(default=0.0, ge=0, description="Administrative expense claims (503)")
    gap_claims_502f: float = Field(default=0.0, ge=0, description="Involuntary gap claims (502(f))")
    wage_claims_507a4: float = Field(default=0.0, ge=0, description="Wage claims ($15,150 cap per employee)")
    benefit_claims_507a5: float = Field(default=0.0, ge=0, description="Employee benefit plan claims ($15,150 cap)")
    farmer_fisher_507a6: float = Field(default=0.0, ge=0, description="Farmer/fisherman claims ($7,575 cap)")
    consumer_deposit_507a7: float = Field(default=0.0, ge=0, description="Consumer deposit claims ($3,350 cap)")
    tax_claims_507a8: float = Field(default=0.0, ge=0, description="Tax claims")
    dip_commitment_507a9: float = Field(default=0.0, ge=0, description="FDIC/commitment claims")
    death_injury_507a10: float = Field(default=0.0, ge=0, description="Death/injury from DUI claims")
    general_unsecured: float = Field(default=0.0, ge=0, description="General unsecured claims")
    subordinated_claims: float = Field(default=0.0, ge=0, description="Subordinated claims (510)")
    secured_claims: float = Field(default=0.0, ge=0, description="Total secured claims (paid from collateral first)")
    secured_collateral_value: float = Field(default=0.0, ge=0, description="Value of secured collateral")


def calculate_waterfall(req: WaterfallRequest) -> Dict[str, Any]:
    """Calculate creditor distribution waterfall under 726."""
    estate = req.total_estate_value

    # Secured claims satisfied first from their collateral
    secured_recovery = min(req.secured_claims, req.secured_collateral_value)
    secured_deficiency = max(req.secured_claims - req.secured_collateral_value, 0)

    # Remaining estate after secured claims take collateral
    # (In practice, estate = unencumbered assets + surplus from secured collateral)
    remaining = estate
    waterfall: List[Dict[str, Any]] = []

    priority_layers = [
        ("507(a)(1) — Domestic support obligations", 0.0),  # Always first but no field for DSO in this model
        ("507(a)(2) — Administrative expense claims", req.admin_claims_503),
        ("502(f) — Involuntary gap claims", req.gap_claims_502f),
        ("507(a)(4) — Wage claims (up to $15,150/employee)", req.wage_claims_507a4),
        ("507(a)(5) — Employee benefit plan claims", req.benefit_claims_507a5),
        ("507(a)(6) — Farmer/fisherman claims", req.farmer_fisher_507a6),
        ("507(a)(7) — Consumer deposit claims", req.consumer_deposit_507a7),
        ("507(a)(8) — Tax claims", req.tax_claims_507a8),
        ("507(a)(9) — FDIC/commitment claims", req.dip_commitment_507a9),
        ("507(a)(10) — Death/injury from DUI", req.death_injury_507a10),
    ]

    total_priority_claims = sum(amount for _, amount in priority_layers)
    subordinated_total_claims = req.subordinated_claims + secured_deficiency
    total_all_claims = total_priority_claims + req.general_unsecured + subordinated_total_claims

    for priority_name, claim_amount in priority_layers:
        if claim_amount <= 0:
            continue
        paid = min(claim_amount, remaining)
        pct = (paid / claim_amount * 100) if claim_amount > 0 else 0
        waterfall.append({
            "priority": priority_name,
            "claim_amount": round(claim_amount, 2),
            "amount_paid": round(paid, 2),
            "recovery_pct": round(pct, 1),
            "paid_in_full": paid >= claim_amount,
        })
        remaining = max(remaining - paid, 0)

    # General unsecured (726(a)(4) — includes secured deficiencies)
    total_general = req.general_unsecured + secured_deficiency
    if total_general > 0:
        paid = min(total_general, remaining)
        pct = (paid / total_general * 100) if total_general > 0 else 0
        waterfall.append({
            "priority": "726(a)(4) — General unsecured claims (including secured deficiencies)",
            "claim_amount": round(total_general, 2),
            "amount_paid": round(paid, 2),
            "recovery_pct": round(pct, 1),
            "paid_in_full": paid >= total_general,
        })
        remaining = max(remaining - paid, 0)

    # Subordinated claims (510)
    if req.subordinated_claims > 0:
        paid = min(req.subordinated_claims, remaining)
        pct = (paid / req.subordinated_claims * 100) if req.subordinated_claims > 0 else 0
        waterfall.append({
            "priority": "510 — Subordinated claims",
            "claim_amount": round(req.subordinated_claims, 2),
            "amount_paid": round(paid, 2),
            "recovery_pct": round(pct, 1),
            "paid_in_full": paid >= req.subordinated_claims,
        })
        remaining = max(remaining - paid, 0)

    # Surplus to debtor
    waterfall.append({
        "priority": "Surplus — returned to debtor",
        "claim_amount": 0,
        "amount_paid": round(remaining, 2),
        "recovery_pct": 100.0 if remaining > 0 else 0.0,
        "paid_in_full": True,
    })

    return {
        "engine_id": ENGINE_ID,
        "endpoint": "waterfall",
        "estate_value": round(req.total_estate_value, 2),
        "secured_recovery": round(secured_recovery, 2),
        "secured_deficiency": round(secured_deficiency, 2),
        "total_distributed": round(req.total_estate_value - remaining, 2),
        "surplus": round(remaining, 2),
        "waterfall": waterfall,
        "citations": [
            "11 USC 507(a)", "11 USC 726(a)", "11 USC 510",
            "11 USC 725", "11 USC 503(b)",
        ],
        "disclaimers": [REQUIRED_DISCLAIMERS["not_legal_advice"]],
    }


@app.post("/waterfall")
async def handle_waterfall(request: WaterfallRequest) -> Dict[str, Any]:
    """Calculate creditor priority waterfall distribution."""
    trace = trace_query(f"waterfall: estate=${request.total_estate_value:,.0f}", "analysis")
    record_bk_metric(BankruptcyMetricType.PLAN_FEASIBILITY)
    try:
        result = calculate_waterfall(request)
        trace.confidence = 0.88
        trace.response_layer = ResponseLayer.BANKRUPTCY_ANALYSIS
        complete_trace(trace)
        return result
    except Exception as exc:
        trace.error = str(exc)
        complete_trace(trace)
        raise HTTPException(status_code=500, detail=str(exc))


# ============================================================================
# STATE EXEMPTION COMPARISON ENGINE
# ============================================================================

# Comprehensive state exemption data for comparison
STATE_EXEMPTIONS_DB: Dict[str, Dict[str, Any]] = {
    "TX": {
        "name": "Texas",
        "homestead": {"value": "Unlimited", "acreage_urban": "10 acres", "acreage_rural": "200 acres (family)",
                      "notes": "TX Const. Art. XVI, Sec. 51; TX Prop. Code 41.001-41.003"},
        "personal_property": {"value": 100000, "married_value": 200000, "notes": "TX Prop. Code 42.001"},
        "retirement": {"value": "Unlimited (qualified plans)", "notes": "TX Prop. Code 42.0021"},
        "wages": {"value": "100% if head of household", "notes": "TX Prop. Code 42.001(b)(1)"},
        "vehicle": {"value": "1 per licensed household member (included in personal property cap)",
                    "notes": "TX Prop. Code 42.002(a)(2)"},
        "life_insurance": {"value": "Unlimited (cash value of policy)", "notes": "TX Insurance Code 1108.051"},
        "opts_out_of_federal": True,
        "domicile_period": "730 days",
        "wildcard": 0,
    },
    "FL": {
        "name": "Florida",
        "homestead": {"value": "Unlimited", "acreage_urban": "0.5 acre", "acreage_rural": "160 acres",
                      "notes": "FL Const. Art. X, Sec. 4"},
        "personal_property": {"value": 1000, "married_value": 2000, "notes": "FL Stat. 222.25(4)"},
        "retirement": {"value": "Unlimited (qualified plans)", "notes": "FL Stat. 222.21"},
        "wages": {"value": "100% if head of household; otherwise $750/week", "notes": "FL Stat. 222.11"},
        "vehicle": {"value": 1000, "notes": "FL Stat. 222.25(2)"},
        "life_insurance": {"value": "Unlimited (cash value)", "notes": "FL Stat. 222.14"},
        "opts_out_of_federal": True,
        "domicile_period": "730 days",
        "wildcard": 4000,
    },
    "CA": {
        "name": "California",
        "homestead": {"value": "300K-600K (depending on median sale price in county)",
                      "notes": "CA CCP 704.730"},
        "personal_property": {"value": "Various per category", "notes": "CA CCP 704.010-704.210"},
        "retirement": {"value": "Unlimited (qualified plans)", "notes": "CA CCP 704.115"},
        "wages": {"value": "75% exempt", "notes": "CA CCP 706.050"},
        "vehicle": {"value": 3325, "notes": "CA CCP 704.010"},
        "life_insurance": {"value": 14200, "notes": "CA CCP 704.100"},
        "opts_out_of_federal": True,
        "domicile_period": "730 days",
        "wildcard": 33650,
    },
    "NY": {
        "name": "New York",
        "homestead": {"value": "150K-1M (depending on county)", "notes": "NY CPLR 5206(a)"},
        "personal_property": {"value": "Per category", "notes": "NY CPLR 5205, Debt. & Cred. 282"},
        "retirement": {"value": "Unlimited (qualified plans)", "notes": "NY CPLR 5205(c)"},
        "wages": {"value": "90% exempt", "notes": "NY CPLR 5231"},
        "vehicle": {"value": 4825, "notes": "NY Debt. & Cred. 282(1)"},
        "life_insurance": {"value": "Unlimited (cash value)", "notes": "NY Ins. Law 3212"},
        "opts_out_of_federal": True,
        "domicile_period": "730 days",
        "wildcard": 1175,
    },
    "FEDERAL": {
        "name": "Federal (11 USC 522(d))",
        "homestead": {"value": 27900, "notes": "11 USC 522(d)(1) (adjusted triennially)"},
        "personal_property": {"value": "Various per category", "notes": "11 USC 522(d)(3-6)"},
        "retirement": {"value": "Unlimited (qualified); IRA $1.5M cap", "notes": "11 USC 522(b)(3)(C), (n)"},
        "wages": {"value": "Per state wage exemption law", "notes": "Not covered under 522(d)"},
        "vehicle": {"value": 4450, "notes": "11 USC 522(d)(2)"},
        "life_insurance": {"value": 14850, "notes": "11 USC 522(d)(8)"},
        "opts_out_of_federal": False,
        "domicile_period": "N/A",
        "wildcard": 1475 + 13950,  # 522(d)(5) unused homestead + wildcard
    },
}


@app.get("/exemption-comparison")
async def exemption_comparison(
    states: str = Query(..., description="Comma-separated state codes (e.g., TX,FL,CA,FEDERAL)"),
    asset_type: Optional[str] = Query(default=None, description="Filter by asset type (homestead, vehicle, etc.)"),
) -> Dict[str, Any]:
    """Compare exemptions across states."""
    state_list = [s.strip().upper() for s in states.split(",")]
    comparison: List[Dict[str, Any]] = []

    for state_code in state_list:
        if state_code in STATE_EXEMPTIONS_DB:
            state_data = STATE_EXEMPTIONS_DB[state_code]
            if asset_type:
                # Return specific asset type
                asset_info = state_data.get(asset_type, {})
                comparison.append({
                    "state": state_code,
                    "name": state_data["name"],
                    "asset_type": asset_type,
                    "exemption": asset_info,
                    "opts_out_of_federal": state_data["opts_out_of_federal"],
                    "wildcard": state_data.get("wildcard", 0),
                })
            else:
                comparison.append({
                    "state": state_code,
                    "name": state_data["name"],
                    "homestead": state_data["homestead"],
                    "personal_property": state_data["personal_property"],
                    "retirement": state_data["retirement"],
                    "wages": state_data["wages"],
                    "vehicle": state_data["vehicle"],
                    "life_insurance": state_data["life_insurance"],
                    "opts_out_of_federal": state_data["opts_out_of_federal"],
                    "wildcard": state_data.get("wildcard", 0),
                    "domicile_period": state_data["domicile_period"],
                })
        else:
            comparison.append({
                "state": state_code,
                "error": f"State '{state_code}' not in database. Available: {', '.join(STATE_EXEMPTIONS_DB.keys())}",
            })

    return {
        "engine_id": ENGINE_ID,
        "endpoint": "exemption_comparison",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "states_compared": state_list,
        "comparison": comparison,
        "notes": [
            "BAPCPA 730-day domicile rule: Debtor must have been domiciled in state for 730 days before filing",
            "If debtor moved within 730 days, prior state's exemptions apply",
            "Federal exemptions available only if state has not opted out",
            "Exemption amounts are periodically adjusted — verify current amounts",
        ],
        "citations": [
            "11 USC 522(b)", "11 USC 522(d)", "11 USC 522(b)(3)(A) (730-day rule)",
        ],
        "disclaimers": [REQUIRED_DISCLAIMERS["not_legal_advice"], REQUIRED_DISCLAIMERS["exemption_caveat"]],
    }


# ============================================================================
# BANKRUPTCY ABUSE / BAD FAITH DETECTION
# ============================================================================

class AbuseDetectionRequest(BaseModel):
    """Request model for bankruptcy abuse detection."""
    income_to_expense_ratio: float = Field(default=1.0, ge=0, description="Ratio of income to expenses")
    luxury_purchases_90_days: float = Field(default=0.0, ge=0, description="Luxury purchases within 90 days of filing")
    cash_advances_70_days: float = Field(default=0.0, ge=0, description="Cash advances within 70 days of filing")
    transferred_assets_2_years: float = Field(default=0.0, ge=0, description="Total assets transferred in 2 years")
    prior_filings_in_year: int = Field(default=0, ge=0, description="Number of filings in past year")
    failed_to_file_taxes: bool = Field(default=False, description="Failed to file required tax returns")
    incomplete_schedules: bool = Field(default=False, description="Filed incomplete/inaccurate schedules")
    eve_of_bankruptcy_planning: bool = Field(default=False, description="Aggressive pre-filing asset protection")
    significant_insider_payments: bool = Field(default=False, description="Large payments to insiders pre-filing")
    lifestyle_inconsistent: bool = Field(default=False, description="Lifestyle inconsistent with claimed income")
    selective_debt_loading: bool = Field(default=False, description="Ran up debt with intent not to repay")


def detect_abuse(req: AbuseDetectionRequest) -> Dict[str, Any]:
    """Analyze potential bankruptcy abuse indicators."""
    red_flags: List[Dict[str, Any]] = []
    yellow_flags: List[Dict[str, Any]] = []
    abuse_score = 0.0

    # 523(a)(2)(C) presumption: luxury goods > $800 within 90 days
    if req.luxury_purchases_90_days > 800:
        red_flags.append({
            "flag": "Luxury goods presumption",
            "section": "523(a)(2)(C)(i)",
            "detail": f"${req.luxury_purchases_90_days:,.2f} in luxury goods within 90 days creates "
                      "presumption of nondischargeability for those debts",
            "severity": "high",
        })
        abuse_score += 0.20

    # 523(a)(2)(C) presumption: cash advances > $1,100 within 70 days
    if req.cash_advances_70_days > 1100:
        red_flags.append({
            "flag": "Cash advance presumption",
            "section": "523(a)(2)(C)(ii)",
            "detail": f"${req.cash_advances_70_days:,.2f} in cash advances within 70 days creates "
                      "presumption of nondischargeability",
            "severity": "high",
        })
        abuse_score += 0.20

    # Asset transfers
    if req.transferred_assets_2_years > 10000:
        red_flags.append({
            "flag": "Pre-petition asset transfers",
            "section": "548/727(a)(2)",
            "detail": f"${req.transferred_assets_2_years:,.2f} in transfers within 2 years — "
                      "potential fraudulent transfer and/or discharge denial",
            "severity": "high",
        })
        abuse_score += 0.15

    # Serial filing
    if req.prior_filings_in_year >= 2:
        red_flags.append({
            "flag": "Serial filer — possible bad faith",
            "section": "362(c)(4), 707(b)(3)",
            "detail": f"{req.prior_filings_in_year} filings in past year — no automatic stay, "
                      "possible dismissal for bad faith",
            "severity": "critical",
        })
        abuse_score += 0.25
    elif req.prior_filings_in_year == 1:
        yellow_flags.append({
            "flag": "Repeat filer",
            "section": "362(c)(3)",
            "detail": "One prior filing in year — stay limited to 30 days, heightened scrutiny",
            "severity": "moderate",
        })
        abuse_score += 0.10

    # Tax return failures
    if req.failed_to_file_taxes:
        red_flags.append({
            "flag": "Missing tax returns",
            "section": "521(e)(2), 1307(c)",
            "detail": "Failure to file required tax returns may result in dismissal or conversion",
            "severity": "moderate",
        })
        abuse_score += 0.10

    # Incomplete schedules
    if req.incomplete_schedules:
        red_flags.append({
            "flag": "Incomplete or inaccurate schedules",
            "section": "727(a)(4)",
            "detail": "Material omissions or false statements in schedules may result in denial of discharge",
            "severity": "high",
        })
        abuse_score += 0.15

    # Eve-of-bankruptcy planning
    if req.eve_of_bankruptcy_planning:
        yellow_flags.append({
            "flag": "Aggressive pre-filing planning",
            "section": "522(o), 548",
            "detail": "Aggressive asset protection strategies close to filing may be scrutinized",
            "severity": "moderate",
        })
        abuse_score += 0.10

    # Insider payments
    if req.significant_insider_payments:
        red_flags.append({
            "flag": "Insider preference payments",
            "section": "547(b) (1-year lookback for insiders)",
            "detail": "Payments to insiders within 1 year are avoidable as preferences",
            "severity": "high",
        })
        abuse_score += 0.15

    # Lifestyle inconsistency
    if req.lifestyle_inconsistent:
        yellow_flags.append({
            "flag": "Lifestyle inconsistency",
            "section": "707(b)(3)",
            "detail": "Lifestyle inconsistent with claimed income may indicate bad faith or unreported income",
            "severity": "moderate",
        })
        abuse_score += 0.10

    # Selective debt loading
    if req.selective_debt_loading:
        red_flags.append({
            "flag": "Selective debt loading",
            "section": "523(a)(2), 707(b)(3)",
            "detail": "Running up debt with intent not to repay may result in nondischargeability "
                      "and/or dismissal for bad faith",
            "severity": "critical",
        })
        abuse_score += 0.20

    abuse_score = min(abuse_score, 1.0)

    risk_level = "LOW"
    if abuse_score >= 0.60:
        risk_level = "CRITICAL"
    elif abuse_score >= 0.40:
        risk_level = "HIGH"
    elif abuse_score >= 0.20:
        risk_level = "MODERATE"

    return {
        "engine_id": ENGINE_ID,
        "endpoint": "abuse_detection",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "abuse_score": round(abuse_score, 4),
        "risk_level": risk_level,
        "red_flags": red_flags,
        "yellow_flags": yellow_flags,
        "total_flags": len(red_flags) + len(yellow_flags),
        "recommendations": [
            "Address all red flags before filing to minimize risk of dismissal or denial of discharge",
            "Ensure complete and accurate disclosure of all transfers, income, and assets",
            "Consult with counsel regarding any pre-filing planning strategies",
        ] if abuse_score > 0.20 else ["No significant abuse indicators detected"],
        "citations": [
            "11 USC 707(b)(3) (bad faith/totality of circumstances)",
            "11 USC 523(a)(2)(C) (luxury goods/cash advance presumptions)",
            "11 USC 727(a) (grounds for denial of discharge)",
            "11 USC 548 (fraudulent transfer avoidance)",
        ],
        "disclaimers": [REQUIRED_DISCLAIMERS["not_legal_advice"], REQUIRED_DISCLAIMERS["fact_dependent"]],
    }


@app.post("/abuse-detection")
async def handle_abuse_detection(request: AbuseDetectionRequest) -> Dict[str, Any]:
    """Detect potential bankruptcy abuse indicators."""
    trace = trace_query("abuse_detection", "analysis")
    try:
        result = detect_abuse(request)
        trace.confidence = 1.0 - float(result.get("abuse_score", 0.5))
        trace.response_layer = ResponseLayer.BANKRUPTCY_ANALYSIS
        complete_trace(trace)
        return result
    except Exception as exc:
        trace.error = str(exc)
        complete_trace(trace)
        raise HTTPException(status_code=500, detail=str(exc))


# ============================================================================
# ENGINE INTROSPECTION ENDPOINT
# ============================================================================

@app.get("/introspect")
async def introspect() -> Dict[str, Any]:
    """Return engine capabilities and available endpoints."""
    routes: List[Dict[str, str]] = []
    for route in app.routes:
        if hasattr(route, "path") and hasattr(route, "methods"):
            routes.append({
                "path": route.path,
                "methods": list(route.methods) if route.methods else [],
                "name": getattr(route, "name", ""),
            })

    return {
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "engine_version": ENGINE_VERSION,
        "port": ENGINE_PORT,
        "tier": ENGINE_TIER,
        "tie_components": [
            "three_layer_response", "response_modes", "doctrine_cache",
            "authority_hardening", "confidence_stratification", "semantic_normalization",
            "vector_search_tfidf", "telemetry_module", "doctrine_drift_watcher",
            "doctrine_coverage_map", "metrics_collector", "health_endpoint",
            "zoned_analysis", "fact_fragility_scoring", "audit_trail_jsonl",
            "determinism_hash_sha256", "fastapi_server", "loguru_logging",
            "multi_doctrine_decomposition", "deep_analysis_mode",
        ],
        "domain_coverage": [
            "chapter_7_liquidation", "chapter_11_reorganization", "chapter_13_wage_earner",
            "chapter_12_family_farmer", "chapter_15_cross_border", "means_test",
            "automatic_stay", "discharge_dischargeability", "federal_state_exemptions",
            "texas_homestead", "preference_avoidance", "fraudulent_transfer",
            "plan_confirmation", "adversary_proceedings", "reaffirmation_agreements",
            "student_loan_brunner_test", "tax_debt_discharge", "lien_stripping_cramdown",
            "trustee_powers", "us_trustee_oversight", "bapcpa", "creditor_priority_waterfall",
            "plan_feasibility", "abuse_detection",
        ],
        "endpoints": routes,
        "total_endpoints": len(routes),
        "total_doctrine_blocks": len(DOCTRINE_BLOCKS),
        "python_version": sys.version,
    }


# ============================================================================
# ENTRYPOINT
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
