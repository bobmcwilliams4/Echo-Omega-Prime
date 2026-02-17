"""
LG18 Legislative Analysis Engine - Main FastAPI Engine
========================================================
Production-grade legislative analysis engine implementing all 20 TIE
components for federal and state legislative process review, statutory
construction canon application, bill drafting analysis, regulatory
rulemaking assessment, Chevron/Loper Bright deference analysis,
congressional oversight, preemption, delegation doctrine, redistricting,
lobbying regulation, constitutional amendment, and legislative privilege.

TIE-20 Components:
    1.  three_layer_response
    2.  response_modes (fast, analysis, memo, bill_analysis, regulatory_review)
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

Port: 8408
Engine: LG18 Legislative Analysis
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
    BillComparisonEngine,
    BillComparisonResult,
    CanonMatchResult,
    CanonOfConstructionMatcher,
    DoctrineSearchIndex,
    LegislativeHistoryEntry,
    LegislativeHistorySearcher,
    RulemakingSearchTracker,
    SearchResult,
    compute_query_hash,
    get_bill_comparison,
    get_canon_matcher,
    get_leg_history_searcher,
    get_rulemaking_tracker,
    get_search_index,
)
from semantic import (
    BillAnalyzer,
    NormalizationResult,
    PreemptionAnalyzer,
    RegulatoryTracker,
    StatutoryConstructionEngine,
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
    LegislativeMetricType,
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

ENGINE_ID: str = "LG18"
ENGINE_NAME: str = "Legislative Analysis Engine"
ENGINE_VERSION: str = "2.0.0"
ENGINE_PORT: int = 8408
ENGINE_HOST: str = "0.0.0.0"
ENGINE_AUTHORITY: float = 5.0
ENGINE_TIER: str = "LEGAL"
ENGINE_MODE: str = "EF"

CONFIG_PATH: Path = Path(__file__).parent / "config.json"
LOG_DIR: Path = Path(__file__).parent / "logs"
AUDIT_LOG_PATH: Path = LOG_DIR / "audit_trail.jsonl"
DRIFT_REGISTRY_PATH: Path = Path(__file__).parent / "doctrine_drift_registry.json"

BANNED_PHRASES: List[str] = [
    "This bill will definitely pass",
    "The court will certainly uphold this statute",
    "Chevron deference guarantees agency action",
    "No court would strike this delegation",
    "This regulation is bulletproof under APA",
    "The filibuster will absolutely block this",
    "Preemption is guaranteed here",
    "Legislative history conclusively proves intent",
    "This canon of construction always controls",
    "There is zero risk of constitutional challenge",
    "The veto will certainly be overridden",
    "No state law can survive this preemption",
    "Loper Bright eliminated all agency deference",
    "This redistricting plan is litigation-proof",
]

REQUIRED_DISCLAIMERS: Dict[str, str] = {
    "not_legal_advice": (
        "This analysis is for informational purposes only and does not "
        "constitute legal advice. Consult a licensed attorney for specific legal guidance."
    ),
    "jurisdiction_specific": (
        "Legislative and regulatory law varies significantly by jurisdiction "
        "and is subject to frequent change. This analysis may not reflect the "
        "most current developments."
    ),
    "fact_dependent": (
        "Legislative outcomes depend on political dynamics, procedural rules, "
        "and evolving judicial interpretation. This analysis is based on the "
        "information provided."
    ),
    "deference_caveat": (
        "Following Loper Bright Enterprises v. Ramos (2024), the landscape "
        "of judicial deference to agency interpretation is in flux. Prior "
        "Chevron-based analyses may require reassessment."
    ),
}

AUTHORITY_WEIGHTS: Dict[str, int] = {
    "us_supreme_court": 100,
    "state_supreme_court": 90,
    "federal_circuit_court": 85,
    "state_appellate_court": 75,
    "federal_district_court": 70,
    "state_trial_court": 55,
    "us_constitution": 100,
    "federal_statute": 95,
    "state_constitution": 92,
    "state_statute": 90,
    "congressional_rule": 80,
    "cfr_regulation": 80,
    "executive_order": 75,
    "committee_report": 60,
    "floor_statement": 45,
    "signing_statement": 40,
    "crs_report": 55,
    "gao_report": 60,
    "agency_guidance": 50,
    "treatise": 40,
    "law_review": 30,
}

CONFIDENCE_BANDS: Dict[str, Dict[str, Any]] = {
    "DEFENSIBLE": {"min_score": 0.85, "label": "Position is well-supported by established legislative law and precedent", "requires_caveat": False},
    "SUPPORTABLE": {"min_score": 0.65, "label": "Position has reasonable support but some uncertainty in application", "requires_caveat": True},
    "DISCLOSURE": {"min_score": 0.50, "label": "Position requires disclosure of contrary authority or evolving doctrine", "requires_caveat": True},
    "HIGH_RISK": {"min_score": 0.0, "label": "Position faces significant adverse authority or post-Loper Bright uncertainty", "requires_caveat": True},
}

LEG_CATEGORY_METRIC_MAP: Dict[str, LegislativeMetricType] = {
    "statutory_construction": LegislativeMetricType.STATUTORY_CONSTRUCTION_QUERY,
    "congressional_procedure": LegislativeMetricType.CONGRESSIONAL_PROCEDURE_QUERY,
    "regulatory_rulemaking": LegislativeMetricType.REGULATORY_RULEMAKING_QUERY,
    "preemption": LegislativeMetricType.PREEMPTION_QUERY,
    "delegation": LegislativeMetricType.DELEGATION_QUERY,
    "redistricting": LegislativeMetricType.REDISTRICTING_QUERY,
    "lobbying_regulation": LegislativeMetricType.LOBBYING_QUERY,
    "constitutional_process": LegislativeMetricType.CONSTITUTIONAL_AMENDMENT_QUERY,
    "state_legislative_process": LegislativeMetricType.TEXAS_LEGISLATURE_QUERY,
    "legislative_process": LegislativeMetricType.BILL_ANALYSIS,
    "legislative_privilege": LegislativeMetricType.OVERSIGHT_QUERY,
    "budget_process": LegislativeMetricType.APPROPRIATIONS_QUERY,
    "congressional_oversight": LegislativeMetricType.OVERSIGHT_QUERY,
    "direct_democracy": LegislativeMetricType.BILL_ANALYSIS,
}


# ============================================================================
# PYDANTIC REQUEST/RESPONSE MODELS
# ============================================================================

class QueryRequest(BaseModel):
    """Incoming query request."""
    query: str = Field(..., min_length=3, max_length=5000, description="The legislative analysis question")
    mode: str = Field("fast", description="Response mode: fast, analysis, memo, bill_analysis, regulatory_review")
    jurisdiction: Optional[str] = Field(None, description="Jurisdiction filter (e.g. federal, texas)")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context for analysis")
    include_citations: bool = Field(True, description="Include statutory and case citations")
    include_practice_tips: bool = Field(False, description="Include practice tips in response")
    max_results: int = Field(5, ge=1, le=20, description="Maximum doctrine results to return")

    @field_validator("mode")
    @classmethod
    def validate_mode(cls, v: str) -> str:
        valid_modes = {"fast", "analysis", "memo", "bill_analysis", "regulatory_review"}
        if v not in valid_modes:
            raise ValueError(f"Invalid mode '{v}'. Must be one of: {valid_modes}")
        return v


class CanonRequest(BaseModel):
    """Canon of construction analysis request."""
    statutory_text: str = Field(..., min_length=5, description="Statutory text to interpret")
    context: str = Field("", description="Additional context for interpretation")
    canon: Optional[str] = Field(None, description="Specific canon to apply (auto-detected if omitted)")


class PreemptionRequest(BaseModel):
    """Preemption analysis request."""
    federal_statute: str = Field(..., description="Federal statute or provision at issue")
    state_law: str = Field(..., description="State law or provision at issue")
    preemption_type: str = Field("express", description="Type: express, field, conflict")


class RulemakingRequest(BaseModel):
    """Rulemaking analysis request."""
    rule_info: Dict[str, Any] = Field(..., description="Rule information including type, dates, and compliance data")
    analysis_type: str = Field("compliance", description="Analysis type: compliance, cra_vulnerability, deference")


class BillAnalysisRequest(BaseModel):
    """Bill analysis request."""
    bill_text: str = Field("", description="Bill text to analyze (can be excerpt)")
    subject_areas: List[str] = Field(default_factory=list, description="Subject areas for committee referral analysis")


class BillCompareRequest(BaseModel):
    """Bill comparison request."""
    bill_a: Dict[str, Any] = Field(..., description="First bill data")
    bill_b: Dict[str, Any] = Field(..., description="Second bill data")


class LegHistoryRequest(BaseModel):
    """Legislative history assessment request."""
    question: str = Field(..., min_length=3, description="Interpretive question")
    available_sources: List[str] = Field(default_factory=list, description="Available source types")


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
    leg_category: Optional[str] = Field(None, description="Legislative category context")


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
    leg_category: Optional[str]
    analysis: Dict[str, Any]
    citations: List[Dict[str, Any]]
    disclaimers: List[str]
    practice_tips: List[str]
    trace_id: str
    duration_ms: float
    determinism_hash: str
    timestamp: str


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def _get_confidence_band(score: float) -> Tuple[str, str, bool]:
    """Determine the confidence band for a given score."""
    for band_name, band_info in CONFIDENCE_BANDS.items():
        if score >= band_info["min_score"]:
            return band_name, band_info["label"], band_info["requires_caveat"]
    return "HIGH_RISK", CONFIDENCE_BANDS["HIGH_RISK"]["label"], True


def _apply_epistemic_guardrails(text: str) -> str:
    """Check text against banned phrases and strip them."""
    for phrase in BANNED_PHRASES:
        if phrase.lower() in text.lower():
            logger.warning("Epistemic guardrail triggered: banned phrase detected")
            text = text.replace(phrase, "[CLAIM REMOVED - exceeds epistemic bounds]")
    return text


def _build_disclaimers(requires_caveat: bool, jurisdiction: Optional[str]) -> List[str]:
    """Build the appropriate disclaimers for a response."""
    disclaimers = [REQUIRED_DISCLAIMERS["not_legal_advice"]]
    if requires_caveat:
        disclaimers.append(REQUIRED_DISCLAIMERS["jurisdiction_specific"])
        disclaimers.append(REQUIRED_DISCLAIMERS["fact_dependent"])
    if jurisdiction:
        disclaimers.append(REQUIRED_DISCLAIMERS["jurisdiction_specific"])
    disclaimers.append(REQUIRED_DISCLAIMERS["deference_caveat"])
    return list(dict.fromkeys(disclaimers))


def _compute_determinism_hash(response_data: Dict[str, Any]) -> str:
    """Compute SHA-256 determinism hash of the response."""
    hashable = {
        "query_hash": response_data.get("query_hash", ""),
        "confidence_score": response_data.get("confidence_score", 0),
        "confidence_band": response_data.get("confidence_band", ""),
        "layer_used": response_data.get("layer_used", ""),
        "analysis_keys": sorted(response_data.get("analysis", {}).keys()),
        "citations_count": len(response_data.get("citations", [])),
    }
    content = json.dumps(hashable, sort_keys=True)
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def _extract_citations(blocks: List[DoctrineCacheBlock]) -> List[Dict[str, Any]]:
    """Extract citations from doctrine blocks."""
    citations: List[Dict[str, Any]] = []
    seen: Set[str] = set()
    for block in blocks:
        for case in block.leading_cases:
            if case not in seen:
                seen.add(case)
                citations.append({
                    "type": "case",
                    "citation": case,
                    "topic": block.topic,
                    "authority_score": block.authority_score,
                })
        for statute in block.key_statutes:
            if statute not in seen:
                seen.add(statute)
                citations.append({
                    "type": "statute",
                    "citation": statute,
                    "topic": block.topic,
                    "authority_score": block.authority_score,
                })
    return citations


def _detect_leg_category(query: str, norm_result: NormalizationResult) -> str:
    """Detect the legislative category of a query."""
    if norm_result.detected_categories:
        return norm_result.detected_categories[0]
    query_lower = query.lower()
    category_keywords: Dict[str, List[str]] = {
        "statutory_construction": ["canon", "interpret", "construction", "textualism", "purposivism", "plain meaning", "ejusdem", "noscitur", "expressio"],
        "congressional_procedure": ["filibuster", "cloture", "reconciliation", "senate rule", "house rule", "conference committee", "markup"],
        "regulatory_rulemaking": ["rulemaking", "notice and comment", "apa", "nprm", "final rule", "chevron", "deference", "loper bright", "skidmore"],
        "preemption": ["preempt", "preemption", "supremacy", "field preemption", "conflict preemption", "express preemption"],
        "delegation": ["nondelegation", "delegation", "intelligible principle"],
        "redistricting": ["redistrict", "gerrymander", "one person one vote", "reapportion"],
        "lobbying_regulation": ["lobby", "fara", "foreign agent", "disclosure act"],
        "constitutional_process": ["amendment", "article v", "ratification", "convention"],
        "state_legislative_process": ["texas legislat", "sunset review", "biennial session"],
        "legislative_process": ["bill", "veto", "signing statement", "enrolled bill", "pocket veto"],
        "legislative_privilege": ["speech or debate", "legislative privilege", "congressional immunity"],
        "budget_process": ["appropriation", "debt ceiling", "continuing resolution", "sequestration"],
        "congressional_oversight": ["oversight", "subpoena", "investigation", "gao", "inspector general", "cra"],
    }
    for category, keywords in category_keywords.items():
        if any(kw in query_lower for kw in keywords):
            return category
    return "legislative_process"


# ============================================================================
# CORE ANALYSIS FUNCTIONS
# ============================================================================

async def _layer_1_doctrine_cache(
    query: str,
    norm_result: NormalizationResult,
    jurisdiction: Optional[str],
    max_results: int,
) -> Tuple[Optional[List[DoctrineCacheBlock]], float]:
    """Layer 1: Doctrine cache lookup."""
    category = norm_result.detected_categories[0] if norm_result.detected_categories else None
    blocks = search_doctrines(query, category=category, top_k=max_results)
    if not blocks:
        return None, 0.0
    avg_confidence = sum(b.confidence for b in blocks) / len(blocks)
    avg_authority = sum(b.authority_score for b in blocks) / len(blocks)
    score = avg_confidence * avg_authority
    if jurisdiction:
        jurisdiction_match = any(
            b.jurisdiction == jurisdiction or b.jurisdiction == "federal"
            for b in blocks
        )
        if not jurisdiction_match:
            score *= 0.7
    return blocks, score


async def _layer_2_semantic_search(
    query: str,
    norm_result: NormalizationResult,
    jurisdiction: Optional[str],
    max_results: int,
) -> Tuple[Optional[List[SearchResult]], float]:
    """Layer 2: Semantic search via TF-IDF index."""
    search_index = get_search_index()
    if not search_index._built:
        for block in DOCTRINE_BLOCKS:
            search_index.add_document(
                doc_id=block.topic,
                content=block.content_for_search(),
                metadata={
                    "topic": block.topic,
                    "category": block.category,
                    "subcategory": block.subcategory,
                    "authority_score": block.authority_score,
                    "confidence": block.confidence,
                    "jurisdiction": block.jurisdiction,
                    "staleness_days": block.staleness_days,
                },
            )
        search_index.build()

    category_filter = norm_result.detected_categories[0] if norm_result.detected_categories else None
    results = search_index.search(
        query=norm_result.normalized_query,
        top_k=max_results,
        category_filter=category_filter,
    )
    if not results:
        return None, 0.0
    avg_score = sum(r.score for r in results) / len(results)
    return results, min(avg_score * 1.2, 1.0)


async def _layer_3_legislative_analysis(
    query: str,
    norm_result: NormalizationResult,
    leg_category: str,
    jurisdiction: Optional[str],
) -> Tuple[Dict[str, Any], float]:
    """Layer 3: Structured legislative analysis."""
    analysis: Dict[str, Any] = {
        "category": leg_category,
        "jurisdiction": jurisdiction or "federal",
        "query_normalized": norm_result.normalized_query,
    }

    if leg_category == "statutory_construction":
        canon_engine = StatutoryConstructionEngine()
        applicable = canon_engine.identify_applicable_canons(query)
        analysis["applicable_canons"] = applicable
        if applicable:
            top_canon = applicable[0]["canon"]
            analysis["primary_canon_application"] = canon_engine.apply_canon(
                top_canon, query, norm_result.normalized_query
            )
        analysis["interpretive_framework"] = (
            "Under the current Supreme Court's approach, begin with the plain text. "
            "If unambiguous, apply as written (Bostock v. Clayton County, 2020). "
            "If ambiguous, consider structural canons, then substantive canons. "
            "Legislative history is used sparingly, primarily to confirm textual meaning."
        )
    elif leg_category == "regulatory_rulemaking":
        reg_tracker = RegulatoryTracker()
        analysis["deference_landscape"] = {
            "chevron": "OVERRULED by Loper Bright (2024). Courts exercise independent judgment.",
            "skidmore": "ACTIVE. Agency views given persuasive weight based on thoroughness and consistency.",
            "auer_kisor": "NARROWED by Kisor v. Wilkie (2019). Deference only for genuinely ambiguous regulations.",
            "major_questions": "ACTIVE. Clear congressional authorization required for actions of vast significance.",
        }
        analysis["post_loper_bright_framework"] = (
            "After Loper Bright Enterprises v. Ramos (2024), courts must exercise independent "
            "judgment in determining statutory meaning under APA Section 706. Agency interpretations "
            "may inform but do not control. Skidmore persuasive weight survives."
        )
    elif leg_category == "preemption":
        preemption_analyzer = PreemptionAnalyzer()
        analysis["preemption_framework"] = {
            "types": ["express", "field", "conflict (impossibility + obstacle)"],
            "presumption": "Against preemption in areas of traditional state regulation (Rice v. Santa Fe Elevator Corp.)",
            "key_principle": "Start with the text of any preemption clause; check for savings clauses",
        }
    elif leg_category == "congressional_procedure":
        analysis["procedural_framework"] = {
            "house": "Majority rules; Rules Committee controls floor debate; germaneness required",
            "senate": "60-vote cloture threshold for most measures; unanimous consent agreements; reconciliation bypass",
            "reconciliation": "Simple majority; limited to tax, spending, debt limit; Byrd Rule restricts extraneous provisions",
        }
    elif leg_category == "delegation":
        analysis["delegation_framework"] = {
            "intelligible_principle": "Congress must provide an intelligible principle to guide agency discretion",
            "current_standard": "Very permissive since 1935; no federal statute struck down on nondelegation grounds since Schechter Poultry",
            "major_questions_as_proxy": "The major questions doctrine (West Virginia v. EPA, 2022) functions as a practical nondelegation limit",
            "future_trajectory": "Justice Gorsuch's Gundy dissent signals potential reinvigoration of the nondelegation doctrine",
        }
    else:
        analysis["general_framework"] = (
            "Analyze the legislative question under the applicable constitutional, "
            "statutory, and procedural framework. Identify controlling authority, "
            "apply relevant canons of construction, and assess the confidence level."
        )

    confidence = 0.70
    if norm_result.matched_terms:
        confidence = min(0.85, confidence + 0.05 * len(norm_result.matched_terms))

    return analysis, confidence


async def _layer_4_deep_analysis(
    query: str,
    norm_result: NormalizationResult,
    leg_category: str,
    jurisdiction: Optional[str],
    include_risk: bool,
    include_alternatives: bool,
) -> Tuple[Dict[str, Any], float]:
    """Layer 4: Deep multi-doctrine synthesis."""
    analysis: Dict[str, Any] = {}

    all_blocks = search_doctrines(query, top_k=10)
    categories_covered = set(b.category for b in all_blocks)
    analysis["doctrines_consulted"] = [b.topic for b in all_blocks]
    analysis["categories_covered"] = sorted(categories_covered)
    analysis["cross_doctrine_synthesis"] = (
        f"Analyzed across {len(categories_covered)} doctrinal categories with "
        f"{len(all_blocks)} relevant blocks. "
        "Cross-references and interactions identified between applicable doctrines."
    )

    if include_risk:
        risk_factors: List[str] = []
        for block in all_blocks:
            risk_factors.extend(block.risk_factors)
        analysis["risk_assessment"] = {
            "risk_factors": risk_factors[:10],
            "overall_risk_level": "medium" if len(risk_factors) > 3 else "low",
            "mitigation_strategies": [
                "Develop arguments under multiple alternative canons/frameworks",
                "Preserve issues for appeal by raising all viable grounds",
                "Monitor legislative and judicial developments that may alter the analysis",
                "File detailed comments during any notice-and-comment period to preserve judicial review",
            ],
        }

    if include_alternatives:
        analysis["alternative_approaches"] = [
            {
                "approach": "Textual argument",
                "description": "Frame the argument primarily in terms of statutory text and ordinary meaning",
                "strength": "Strong under current Supreme Court textualist majority",
            },
            {
                "approach": "Structural argument",
                "description": "Use the statute's structure, context, and design to support the interpretation",
                "strength": "Effective when text alone is ambiguous; King v. Burwell approach",
            },
            {
                "approach": "Historical/purposive argument",
                "description": "Invoke legislative history and statutory purpose to support the reading",
                "strength": "Useful in lower courts; less effective at SCOTUS under current composition",
            },
            {
                "approach": "Major questions challenge",
                "description": "Challenge agency action as exceeding clear congressional authorization",
                "strength": "Very strong post-West Virginia v. EPA for major regulatory actions",
            },
        ]

    confidence = 0.75
    if len(all_blocks) >= 5:
        confidence = min(0.90, confidence + 0.03 * len(all_blocks))

    return analysis, confidence


# ============================================================================
# DRIFT WATCHER
# ============================================================================

class DriftWatcher:
    """Monitors doctrine drift signals and adjusts confidence."""

    def __init__(self) -> None:
        self._signals: List[Dict[str, Any]] = []
        self._registry_path = DRIFT_REGISTRY_PATH

    def add_signal(self, signal: DriftSignal) -> Dict[str, Any]:
        """Add a drift signal and assess impact."""
        entry = {
            "signal_type": signal.signal_type,
            "topic": signal.topic,
            "description": signal.description,
            "source": signal.source,
            "authority_level": signal.authority_level,
            "confidence_impact": signal.confidence_impact,
            "received_at": datetime.now(timezone.utc).isoformat(),
        }
        self._signals.append(entry)

        block = get_doctrine_block(signal.topic)
        impact_assessment: Dict[str, Any] = {
            "signal": entry,
            "topic_found": block is not None,
        }
        if block:
            old_confidence = block.confidence
            new_confidence = max(0.1, min(1.0, old_confidence + signal.confidence_impact))
            impact_assessment["old_confidence"] = round(old_confidence, 4)
            impact_assessment["new_confidence"] = round(new_confidence, 4)
            impact_assessment["change"] = round(new_confidence - old_confidence, 4)
            impact_assessment["action_required"] = abs(signal.confidence_impact) > 0.1

            record_doctrine_mutation(
                mutation_type=MutationType.DRIFT_DETECTED,
                origin=MutationOrigin.DRIFT_WATCHER,
                topic=signal.topic,
                description=signal.description,
                old_value=old_confidence,
                new_value=new_confidence,
            )

        self._save_registry()
        return impact_assessment

    def get_signals(self) -> List[Dict[str, Any]]:
        """Return all drift signals."""
        return list(self._signals)

    def _save_registry(self) -> None:
        """Persist drift signals to registry file."""
        try:
            with open(self._registry_path, "w", encoding="utf-8") as f:
                json.dump(self._signals, f, indent=2, default=str)
        except OSError as exc:
            logger.error("Failed to save drift registry: {}", exc)


# ============================================================================
# FACT FRAGILITY SCORER
# ============================================================================

class FactFragilityScorer:
    """Scores the fragility of factual assertions in legislative analysis."""

    FRAGILITY_INDICATORS: ClassVar[Dict[str, float]] = {
        "subjective": 0.3,
        "speculative": 0.35,
        "contested": 0.25,
        "evolving": 0.2,
        "jurisdictional_variation": 0.15,
        "temporal": 0.1,
        "political": 0.2,
        "post_loper_bright": 0.25,
    }

    def score_facts(
        self,
        facts: List[str],
        jurisdiction: Optional[str] = None,
        leg_category: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Score a list of factual assertions for fragility."""
        results: List[Dict[str, Any]] = []
        for fact in facts:
            fact_lower = fact.lower()
            fragility = 0.0
            indicators: List[str] = []

            if any(w in fact_lower for w in ["likely", "probably", "may", "could", "might", "possibly"]):
                fragility += self.FRAGILITY_INDICATORS["speculative"]
                indicators.append("speculative_language")

            if any(w in fact_lower for w in ["all courts", "every", "always", "never", "unanimous"]):
                fragility += self.FRAGILITY_INDICATORS["contested"]
                indicators.append("absolute_claim")

            if any(w in fact_lower for w in ["evolving", "developing", "emerging", "shifting", "uncertain"]):
                fragility += self.FRAGILITY_INDICATORS["evolving"]
                indicators.append("evolving_doctrine")

            if any(w in fact_lower for w in ["chevron", "deference", "agency interpretation"]):
                fragility += self.FRAGILITY_INDICATORS["post_loper_bright"]
                indicators.append("post_loper_bright_uncertainty")

            if any(w in fact_lower for w in ["political", "partisan", "controversial"]):
                fragility += self.FRAGILITY_INDICATORS["political"]
                indicators.append("political_dimension")

            if any(w in fact_lower for w in ["state", "varies by", "jurisdiction"]):
                fragility += self.FRAGILITY_INDICATORS["jurisdictional_variation"]
                indicators.append("jurisdictional_variation")

            if any(w in fact_lower for w in ["currently", "as of", "recent", "pending"]):
                fragility += self.FRAGILITY_INDICATORS["temporal"]
                indicators.append("temporal_dependency")

            fragility = min(fragility, 1.0)
            stability = 1.0 - fragility

            results.append({
                "fact": fact,
                "fragility_score": round(fragility, 4),
                "stability_score": round(stability, 4),
                "indicators": indicators,
                "recommendation": (
                    "Fact is stable; suitable for reliance" if stability > 0.7
                    else "Fact has moderate fragility; verify with current authority" if stability > 0.4
                    else "Fact is highly fragile; independent verification required"
                ),
            })

        return results


# ============================================================================
# LIFESPAN & APP SETUP
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler: build caches on startup."""
    logger.info("Starting {} v{} on port {}", ENGINE_NAME, ENGINE_VERSION, ENGINE_PORT)
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    build_doctrine_cache()
    logger.info("Doctrine cache built: {} blocks", len(DOCTRINE_BLOCKS))

    search_index = get_search_index()
    for block in DOCTRINE_BLOCKS:
        search_index.add_document(
            doc_id=block.topic,
            content=block.content_for_search(),
            metadata={
                "topic": block.topic,
                "category": block.category,
                "subcategory": block.subcategory,
                "authority_score": block.authority_score,
                "confidence": block.confidence,
                "jurisdiction": block.jurisdiction,
                "staleness_days": block.staleness_days,
            },
        )
    search_index.build()
    logger.info("Search index built: {}", search_index.get_index_stats())

    get_telemetry(LOG_DIR)
    logger.info("{} fully operational", ENGINE_NAME)

    yield

    logger.info("{} shutting down", ENGINE_NAME)


app = FastAPI(
    title=ENGINE_NAME,
    version=ENGINE_VERSION,
    description=(
        f"TIE-20 compliant {ENGINE_NAME} (Engine {ENGINE_ID}). "
        "Provides statutory construction, congressional procedure, regulatory rulemaking, "
        "preemption, delegation, redistricting, lobbying, and legislative process analysis."
    ),
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# TIE COMPONENT 12: HEALTH ENDPOINT
# ============================================================================

@app.get("/health")
async def health() -> Dict[str, Any]:
    """Health check endpoint."""
    cache_stats = get_doctrine_cache_stats()
    search_stats = get_search_index().get_index_stats()
    dict_integrity = verify_dictionary_integrity()
    telemetry_health = get_telemetry().get_health()

    return {
        "status": "healthy",
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "engine_version": ENGINE_VERSION,
        "engine_mode": ENGINE_MODE,
        "port": ENGINE_PORT,
        "tier": ENGINE_TIER,
        "authority": ENGINE_AUTHORITY,
        "doctrine_cache": cache_stats,
        "search_index": search_stats,
        "semantic_dictionary": {
            "valid": dict_integrity["valid"],
            "entries": dict_integrity["total_entries"],
            "version": get_semantic_map_version(),
        },
        "telemetry": {
            "status": telemetry_health["status"],
            "uptime_seconds": telemetry_health["uptime_seconds"],
            "total_queries": telemetry_health["metrics"]["total_queries"],
        },
        "tie_components": {
            "three_layer_response": True,
            "response_modes": ["fast", "analysis", "memo", "bill_analysis", "regulatory_review"],
            "doctrine_cache": True,
            "authority_hardening": True,
            "confidence_stratification": True,
            "semantic_normalization": True,
            "vector_search_tfidf": True,
            "telemetry_module": True,
            "doctrine_drift_watcher": True,
            "doctrine_coverage_map": True,
            "metrics_collector": True,
            "health_endpoint": True,
            "zoned_analysis": True,
            "fact_fragility_scoring": True,
            "audit_trail_jsonl": True,
            "determinism_hash_sha256": True,
            "fastapi_server": True,
            "loguru_logging": True,
            "multi_doctrine_decomposition": True,
            "deep_analysis_mode": True,
        },
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ============================================================================
# MAIN QUERY ENDPOINT - THREE LAYER RESPONSE
# ============================================================================

@app.post("/query", response_model=EngineResponse)
async def query_endpoint(request: QueryRequest) -> EngineResponse:
    """Main query endpoint implementing three-layer response architecture."""
    query_hash = compute_query_hash(request.query, request.mode)
    trace = trace_query(request.query, query_hash, request.mode)

    norm_step = trace.add_step("semantic_normalization", ResponseLayer.DOCTRINE_CACHE)
    norm_result = normalize_query(request.query)
    norm_step.complete()

    leg_category = _detect_leg_category(request.query, norm_result)
    trace.leg_category = leg_category
    trace.jurisdiction = request.jurisdiction or norm_result.detected_jurisdiction

    metric_type = LEG_CATEGORY_METRIC_MAP.get(leg_category)
    if metric_type:
        get_telemetry().record_legislative_metric(metric_type)

    layer_used = ResponseLayer.FALLBACK
    confidence_score = 0.0
    analysis: Dict[str, Any] = {}
    matched_blocks: List[DoctrineCacheBlock] = []

    # Layer 1: Doctrine Cache
    cache_step = trace.add_step("doctrine_cache_lookup", ResponseLayer.DOCTRINE_CACHE)
    blocks, cache_score = await _layer_1_doctrine_cache(
        request.query, norm_result, request.jurisdiction, request.max_results
    )
    cache_step.complete()

    if blocks and cache_score >= 0.6 and request.mode == "fast":
        matched_blocks = blocks
        confidence_score = cache_score
        layer_used = ResponseLayer.DOCTRINE_CACHE
        analysis = {
            "source": "doctrine_cache",
            "matched_topics": [b.topic for b in blocks],
            "summaries": [{"topic": b.topic, "summary": b.summary, "category": b.category} for b in blocks],
        }
    else:
        # Layer 2: Semantic Search
        search_step = trace.add_step("semantic_search", ResponseLayer.SEMANTIC_SEARCH)
        search_results, search_score = await _layer_2_semantic_search(
            request.query, norm_result, request.jurisdiction, request.max_results
        )
        search_step.complete()

        if blocks:
            matched_blocks = blocks

        if search_results and search_score >= 0.4 and request.mode in ("fast", "analysis"):
            confidence_score = max(cache_score, search_score)
            layer_used = ResponseLayer.SEMANTIC_SEARCH
            analysis = {
                "source": "semantic_search",
                "search_results": [r.to_dict() for r in search_results[:request.max_results]],
                "matched_topics": [b.topic for b in matched_blocks] if matched_blocks else [],
            }
        else:
            # Layer 3: Legislative Analysis
            analysis_step = trace.add_step("legislative_analysis", ResponseLayer.LEGISLATIVE_ANALYSIS)
            leg_analysis, leg_confidence = await _layer_3_legislative_analysis(
                request.query, norm_result, leg_category, request.jurisdiction
            )
            analysis_step.complete()

            confidence_score = max(cache_score, search_score if search_results else 0.0, leg_confidence)
            layer_used = ResponseLayer.LEGISLATIVE_ANALYSIS
            analysis = {
                "source": "legislative_analysis",
                **leg_analysis,
                "matched_topics": [b.topic for b in matched_blocks] if matched_blocks else [],
                "search_results": [r.to_dict() for r in (search_results or [])[:3]],
            }

            # Layer 4: Deep Analysis for memo/bill_analysis/regulatory_review modes
            if request.mode in ("memo", "bill_analysis", "regulatory_review"):
                deep_step = trace.add_step("deep_analysis", ResponseLayer.DEEP_ANALYSIS)
                deep_analysis, deep_confidence = await _layer_4_deep_analysis(
                    request.query, norm_result, leg_category, request.jurisdiction,
                    include_risk=True, include_alternatives=True,
                )
                deep_step.complete()
                confidence_score = max(confidence_score, deep_confidence)
                layer_used = ResponseLayer.DEEP_ANALYSIS
                analysis["deep_analysis"] = deep_analysis

    # Build response
    band_name, band_label, requires_caveat = _get_confidence_band(confidence_score)
    citations = _extract_citations(matched_blocks) if matched_blocks else []
    trace.citations_count = len(citations)
    disclaimers = _build_disclaimers(requires_caveat, request.jurisdiction)

    practice_tips: List[str] = []
    if request.include_practice_tips and matched_blocks:
        for block in matched_blocks:
            practice_tips.extend(block.practice_tips)
        practice_tips = list(dict.fromkeys(practice_tips))[:10]

    analysis["normalization"] = {
        "matched_terms": len(norm_result.matched_terms),
        "detected_categories": norm_result.detected_categories,
        "detected_citations": norm_result.detected_citations,
        "detected_jurisdiction": norm_result.detected_jurisdiction,
    }

    trace.complete(layer_used, confidence_score, band_name)
    complete_trace(trace)

    response_data = {
        "query_hash": query_hash,
        "confidence_score": confidence_score,
        "confidence_band": band_name,
        "layer_used": layer_used.value,
        "analysis": analysis,
        "citations": citations,
    }
    determinism_hash = _compute_determinism_hash(response_data)

    return EngineResponse(
        query_hash=query_hash,
        response_mode=request.mode,
        confidence_score=round(confidence_score, 4),
        confidence_band=band_name,
        confidence_label=band_label,
        requires_caveat=requires_caveat,
        layer_used=layer_used.value,
        jurisdiction=request.jurisdiction or norm_result.detected_jurisdiction,
        leg_category=leg_category,
        analysis=analysis,
        citations=citations if request.include_citations else [],
        disclaimers=disclaimers,
        practice_tips=practice_tips,
        trace_id=trace.trace_id,
        duration_ms=round(trace.total_duration_ms, 3),
        determinism_hash=determinism_hash,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


# ============================================================================
# CANON APPLICATION ENDPOINT
# ============================================================================

@app.post("/canon/apply")
async def apply_canon(request: CanonRequest) -> Dict[str, Any]:
    """Apply a canon of statutory construction to a statutory text."""
    construction_engine = StatutoryConstructionEngine()
    if request.canon:
        result = construction_engine.apply_canon(
            request.canon, request.statutory_text, request.context
        )
    else:
        applicable = construction_engine.identify_applicable_canons(request.statutory_text)
        if applicable:
            top_canon = applicable[0]["canon"]
            result = construction_engine.apply_canon(
                top_canon, request.statutory_text, request.context
            )
            result["all_applicable_canons"] = applicable
        else:
            result = construction_engine.apply_canon(
                "plain_meaning_rule", request.statutory_text, request.context
            )
    return {"engine_id": ENGINE_ID, "result": result}


@app.post("/canon/match")
async def match_canons(request: QueryRequest) -> Dict[str, Any]:
    """Match a query to applicable canons of construction."""
    matcher = get_canon_matcher()
    matches = matcher.match_canons(request.query, top_k=request.max_results)
    return {
        "engine_id": ENGINE_ID,
        "query": request.query,
        "matches": [m.to_dict() for m in matches],
    }


# ============================================================================
# PREEMPTION ANALYSIS ENDPOINT
# ============================================================================

@app.post("/preemption/analyze")
async def analyze_preemption(request: PreemptionRequest) -> Dict[str, Any]:
    """Analyze a preemption issue."""
    analyzer = PreemptionAnalyzer()
    result = analyzer.analyze_preemption(
        request.federal_statute, request.state_law, request.preemption_type
    )
    return {"engine_id": ENGINE_ID, "result": result}


# ============================================================================
# REGULATORY RULEMAKING ENDPOINTS
# ============================================================================

@app.post("/rulemaking/analyze")
async def analyze_rulemaking(request: RulemakingRequest) -> Dict[str, Any]:
    """Analyze regulatory rulemaking compliance or vulnerability."""
    reg_tracker = RegulatoryTracker()
    rm_search = get_rulemaking_tracker()

    if request.analysis_type == "compliance":
        result = reg_tracker.analyze_rulemaking_compliance(request.rule_info)
    elif request.analysis_type == "cra_vulnerability":
        result = rm_search.assess_cra_vulnerability(request.rule_info)
    elif request.analysis_type == "deference":
        doctrine = request.rule_info.get("deference_doctrine", "chevron")
        result = reg_tracker.assess_deference(doctrine)
    else:
        result = {"error": f"Unknown analysis type: {request.analysis_type}"}

    return {"engine_id": ENGINE_ID, "analysis_type": request.analysis_type, "result": result}


@app.get("/rulemaking/types")
async def rulemaking_types() -> Dict[str, Any]:
    """List available rulemaking types and their details."""
    tracker = get_rulemaking_tracker()
    types = {}
    for rt in ["notice_and_comment", "formal_rulemaking", "direct_final_rule", "interim_final_rule", "negotiated_rulemaking"]:
        types[rt] = tracker.get_rulemaking_info(rt)
    return {"engine_id": ENGINE_ID, "rulemaking_types": types}


# ============================================================================
# BILL ANALYSIS ENDPOINTS
# ============================================================================

@app.post("/bill/analyze")
async def analyze_bill(request: BillAnalysisRequest) -> Dict[str, Any]:
    """Analyze a bill's structure and drafting quality."""
    analyzer = BillAnalyzer()
    result: Dict[str, Any] = {}
    if request.bill_text:
        result["structure_analysis"] = analyzer.analyze_bill_structure(request.bill_text)
    if request.subject_areas:
        result["committee_referrals"] = analyzer.identify_committees(request.subject_areas)
    return {"engine_id": ENGINE_ID, "result": result}


@app.post("/bill/compare")
async def compare_bills(request: BillCompareRequest) -> Dict[str, Any]:
    """Compare two bill versions."""
    engine = get_bill_comparison()
    result = engine.compare_bills(request.bill_a, request.bill_b)
    return {"engine_id": ENGINE_ID, "result": result.to_dict()}


# ============================================================================
# LEGISLATIVE HISTORY ENDPOINT
# ============================================================================

@app.post("/legislative-history/assess")
async def assess_leg_history(request: LegHistoryRequest) -> Dict[str, Any]:
    """Assess the value of legislative history for an interpretive question."""
    searcher = get_leg_history_searcher()
    result = searcher.assess_legislative_history_value(
        request.question, request.available_sources
    )
    return {"engine_id": ENGINE_ID, "result": result}


# ============================================================================
# DRIFT WATCHER ENDPOINT
# ============================================================================

@app.post("/drift/signal")
async def report_drift_signal(signal: DriftSignal) -> Dict[str, Any]:
    """Report a doctrine drift signal."""
    watcher = DriftWatcher()
    impact = watcher.add_signal(signal)
    return {"engine_id": ENGINE_ID, "impact": impact}


@app.get("/drift/signals")
async def get_drift_signals() -> Dict[str, Any]:
    """Get all drift signals."""
    watcher = DriftWatcher()
    return {"engine_id": ENGINE_ID, "signals": watcher.get_signals()}


# ============================================================================
# FACT FRAGILITY ENDPOINT
# ============================================================================

@app.post("/fragility/score")
async def score_fact_fragility(request: FactFragilityRequest) -> Dict[str, Any]:
    """Score factual assertions for fragility."""
    scorer = FactFragilityScorer()
    results = scorer.score_facts(
        request.facts, request.jurisdiction, request.leg_category
    )
    avg_fragility = sum(r["fragility_score"] for r in results) / max(len(results), 1)
    return {
        "engine_id": ENGINE_ID,
        "scores": results,
        "average_fragility": round(avg_fragility, 4),
        "total_facts": len(results),
    }


# ============================================================================
# MULTI-DOCTRINE DECOMPOSITION ENDPOINT
# ============================================================================

@app.post("/multi-doctrine/decompose")
async def decompose_multi_doctrine(request: MultiDoctrineRequest) -> Dict[str, Any]:
    """Decompose a complex query into constituent doctrines."""
    norm_result = normalize_query(request.query)
    blocks = search_doctrines(request.query, top_k=request.max_doctrines)

    decomposition: List[Dict[str, Any]] = []
    for block in blocks:
        decomposition.append({
            "doctrine_topic": block.topic,
            "category": block.category,
            "summary": block.summary[:300],
            "authority_score": block.authority_score,
            "confidence": block.confidence,
            "key_statutes": block.key_statutes[:3],
            "leading_cases": block.leading_cases[:2],
        })

    cross_references: List[str] = []
    for i, b1 in enumerate(blocks):
        for b2 in blocks[i + 1:]:
            overlap = set(b1.related_topics) & {b2.topic}
            reverse_overlap = set(b2.related_topics) & {b1.topic}
            if overlap or reverse_overlap:
                cross_references.append(f"{b1.topic} <-> {b2.topic}")

    return {
        "engine_id": ENGINE_ID,
        "query": request.query,
        "decomposition": decomposition,
        "cross_references": cross_references,
        "total_doctrines": len(decomposition),
        "normalization": norm_result.to_dict(),
    }


# ============================================================================
# DEEP ANALYSIS ENDPOINT
# ============================================================================

@app.post("/deep-analysis")
async def deep_analysis_endpoint(request: DeepAnalysisRequest) -> Dict[str, Any]:
    """Perform deep multi-doctrine analysis."""
    norm_result = normalize_query(request.query)
    leg_category = _detect_leg_category(request.query, norm_result)

    deep_analysis, confidence = await _layer_4_deep_analysis(
        request.query, norm_result, leg_category, request.jurisdiction,
        include_risk=request.include_risk_assessment,
        include_alternatives=request.include_alternatives,
    )

    if request.include_timeline:
        deep_analysis["timeline_considerations"] = [
            "Congressional session calendars constrain legislative action windows",
            "APA notice-and-comment typically requires 6-18 months",
            "CRA lookback window applies to rules finalized in last ~60 legislative days of prior Congress",
            "Redistricting must follow decennial census (next: 2030)",
            "Post-Loper Bright challenges to existing agency interpretations have no statutory deadline",
        ]

    band_name, band_label, requires_caveat = _get_confidence_band(confidence)
    disclaimers = _build_disclaimers(requires_caveat, request.jurisdiction)

    return {
        "engine_id": ENGINE_ID,
        "query": request.query[:200],
        "leg_category": leg_category,
        "jurisdiction": request.jurisdiction,
        "confidence_score": round(confidence, 4),
        "confidence_band": band_name,
        "confidence_label": band_label,
        "analysis": deep_analysis,
        "disclaimers": disclaimers,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ============================================================================
# COVERAGE MAP ENDPOINT
# ============================================================================

@app.get("/coverage")
async def coverage_map() -> Dict[str, Any]:
    """Return the doctrine coverage map."""
    coverage = get_coverage_map()
    categories = get_all_doctrine_categories()
    topics = get_all_doctrine_topics()
    return {
        "engine_id": ENGINE_ID,
        "total_topics": len(topics),
        "total_categories": len(categories),
        "categories": categories,
        "coverage": coverage,
    }


# ============================================================================
# STALE DOCTRINES ENDPOINT
# ============================================================================

@app.get("/stale")
async def stale_doctrines(threshold_days: int = Query(90, ge=1)) -> Dict[str, Any]:
    """Return doctrines that exceed the staleness threshold."""
    stale = get_stale_doctrines(threshold_days)
    return {
        "engine_id": ENGINE_ID,
        "threshold_days": threshold_days,
        "stale_count": len(stale),
        "stale_doctrines": [{"topic": b.topic, "staleness_days": b.staleness_days, "last_updated": b.last_updated} for b in stale],
    }


# ============================================================================
# DOCTRINE INTEGRITY ENDPOINT
# ============================================================================

@app.get("/integrity")
async def doctrine_integrity() -> Dict[str, Any]:
    """Verify doctrine cache and semantic dictionary integrity."""
    doctrine_check = verify_doctrine_integrity()
    dict_check = verify_dictionary_integrity()
    return {
        "engine_id": ENGINE_ID,
        "doctrine_cache": doctrine_check,
        "semantic_dictionary": dict_check,
        "overall_valid": doctrine_check["valid"] and dict_check["valid"],
    }


# ============================================================================
# METRICS ENDPOINT
# ============================================================================

@app.get("/metrics")
async def metrics() -> Dict[str, Any]:
    """Return telemetry metrics."""
    telemetry = get_telemetry()
    health = telemetry.get_health()
    return {
        "engine_id": ENGINE_ID,
        "metrics": health["metrics"],
        "errors": health["errors"],
        "mutations": health["mutations"],
        "audit": health["audit"],
    }


# ============================================================================
# AUDIT TRAIL ENDPOINT
# ============================================================================

@app.get("/audit/verify")
async def verify_audit() -> Dict[str, Any]:
    """Verify the integrity of the audit trail."""
    audit = AuditTrail(AUDIT_LOG_PATH)
    result = audit.verify_chain()
    return {"engine_id": ENGINE_ID, "audit_verification": result}


# ============================================================================
# SEMANTIC MAP ENDPOINT
# ============================================================================

@app.get("/semantic")
async def semantic_map_info() -> Dict[str, Any]:
    """Return semantic map information."""
    integrity = verify_dictionary_integrity()
    return {
        "engine_id": ENGINE_ID,
        "version": get_semantic_map_version(),
        "hash": get_semantic_map_hash()[:16],
        "total_entries": integrity["total_entries"],
        "total_synonyms": integrity["total_synonyms"],
        "total_categories": integrity["total_categories"],
        "valid": integrity["valid"],
    }


# ============================================================================
# SEARCH INDEX ENDPOINT
# ============================================================================

@app.get("/search/stats")
async def search_stats() -> Dict[str, Any]:
    """Return search index statistics."""
    stats = get_search_index().get_index_stats()
    return {"engine_id": ENGINE_ID, "search_index": stats}


# ============================================================================
# CONFIG ENDPOINT
# ============================================================================

@app.get("/config")
async def get_config() -> Dict[str, Any]:
    """Return engine configuration."""
    config: Dict[str, Any] = {}
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                config = json.load(f)
        except (json.JSONDecodeError, OSError) as exc:
            logger.error("Failed to load config: {}", exc)
            config = {"error": str(exc)}
    return {"engine_id": ENGINE_ID, "config": config}


# ============================================================================
# JURISDICTION MAP ENDPOINT
# ============================================================================

@app.get("/jurisdictions")
async def jurisdictions() -> Dict[str, Any]:
    """Return the jurisdiction map."""
    return {"engine_id": ENGINE_ID, "jurisdictions": get_jurisdiction_map()}


# ============================================================================
# DEFERENCE DOCTRINES ENDPOINT
# ============================================================================

@app.get("/deference")
async def deference_status() -> Dict[str, Any]:
    """Return the current status of judicial deference doctrines."""
    tracker = RegulatoryTracker()
    doctrines = {}
    for doctrine in ["chevron", "skidmore", "auer", "major_questions"]:
        doctrines[doctrine] = tracker.assess_deference(doctrine)
    return {"engine_id": ENGINE_ID, "deference_doctrines": doctrines}


# ============================================================================
# AUTHORITY WEIGHTS ENDPOINT
# ============================================================================

@app.get("/authority-weights")
async def authority_weights() -> Dict[str, Any]:
    """Return the authority weight table."""
    return {
        "engine_id": ENGINE_ID,
        "weights": AUTHORITY_WEIGHTS,
        "total_sources": len(AUTHORITY_WEIGHTS),
    }


# ============================================================================
# ZONED ANALYSIS ENDPOINT (TIE COMPONENT 13)
# ============================================================================

class ZonedAnalysisEngine:
    """Performs zoned analysis routing queries to the most appropriate doctrinal zone."""

    ZONES: ClassVar[Dict[str, Dict[str, Any]]] = {
        "federal_legislative": {
            "description": "Federal legislative process, Article I, bicameralism, presentment",
            "categories": ["congressional_procedure", "legislative_process", "budget_process", "constitutional_process"],
            "authority_floor": "us_constitution",
            "key_sources": ["U.S. Const. Art. I", "House Rules", "Senate Rules", "Congressional Budget Act"],
        },
        "statutory_interpretation": {
            "description": "Canons of construction, textualism, purposivism, legislative history",
            "categories": ["statutory_construction"],
            "authority_floor": "us_supreme_court",
            "key_sources": ["Bostock v. Clayton County", "King v. Burwell", "Scalia & Garner Reading Law"],
        },
        "administrative_law": {
            "description": "APA rulemaking, deference doctrines, Chevron/Loper Bright, major questions",
            "categories": ["regulatory_rulemaking", "delegation"],
            "authority_floor": "federal_statute",
            "key_sources": ["5 USC 553", "5 USC 706", "Loper Bright v. Ramos", "West Virginia v. EPA"],
        },
        "federalism": {
            "description": "Preemption analysis, Supremacy Clause, federal-state interaction",
            "categories": ["preemption"],
            "authority_floor": "us_constitution",
            "key_sources": ["U.S. Const. Art. VI Cl. 2", "Arizona v. United States", "Wyeth v. Levine"],
        },
        "state_legislative": {
            "description": "State legislative processes, Texas Legislature, sunset review",
            "categories": ["state_legislative_process", "direct_democracy"],
            "authority_floor": "state_constitution",
            "key_sources": ["Texas Const. Art. III", "Tex. Gov't Code Ch. 325"],
        },
        "oversight_ethics": {
            "description": "Congressional oversight, lobbying regulation, legislative privilege",
            "categories": ["congressional_oversight", "lobbying_regulation", "legislative_privilege"],
            "authority_floor": "federal_statute",
            "key_sources": ["2 USC 1601 (LDA)", "22 USC 611 (FARA)", "U.S. Const. Art. I Sec. 6"],
        },
        "electoral_process": {
            "description": "Redistricting, voting rights, ballot initiatives",
            "categories": ["redistricting"],
            "authority_floor": "us_constitution",
            "key_sources": ["U.S. Const. Amend. XIV", "VRA Sec. 2", "Rucho v. Common Cause"],
        },
    }

    def route_to_zone(self, leg_category: str) -> Dict[str, Any]:
        """Route a query to the appropriate doctrinal zone based on category."""
        for zone_name, zone_info in self.ZONES.items():
            if leg_category in zone_info["categories"]:
                return {
                    "zone": zone_name,
                    "description": zone_info["description"],
                    "authority_floor": zone_info["authority_floor"],
                    "key_sources": zone_info["key_sources"],
                    "matched_on": leg_category,
                }
        return {
            "zone": "federal_legislative",
            "description": "Default zone: federal legislative process",
            "authority_floor": "us_constitution",
            "key_sources": ["U.S. Const. Art. I"],
            "matched_on": "default",
        }

    def get_zone_analysis(
        self,
        query: str,
        zone_name: str,
        jurisdiction: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Perform zone-specific analysis."""
        zone = self.ZONES.get(zone_name)
        if not zone:
            return {"error": f"Unknown zone: {zone_name}"}

        zone_categories = zone["categories"]
        relevant_blocks = []
        for block in DOCTRINE_BLOCKS:
            if block.category in zone_categories:
                relevant_blocks.append(block)

        query_lower = query.lower()
        scored_blocks: List[Tuple[float, DoctrineCacheBlock]] = []
        for block in relevant_blocks:
            score = 0.0
            for word in query_lower.split():
                if word in block.topic.lower() or word in block.summary.lower():
                    score += 0.2
            if score > 0:
                scored_blocks.append((score, block))
        scored_blocks.sort(key=lambda x: x[0], reverse=True)

        top_blocks = [b for _, b in scored_blocks[:5]]
        return {
            "zone": zone_name,
            "description": zone["description"],
            "relevant_doctrines": [
                {
                    "topic": b.topic,
                    "summary": b.summary[:200],
                    "authority_score": b.authority_score,
                    "confidence": b.confidence,
                }
                for b in top_blocks
            ],
            "total_zone_doctrines": len(relevant_blocks),
            "authority_floor": zone["authority_floor"],
            "key_sources": zone["key_sources"],
            "jurisdiction": jurisdiction,
        }


@app.post("/zone/analyze")
async def zoned_analysis(request: QueryRequest) -> Dict[str, Any]:
    """Perform zoned analysis routing the query to the appropriate doctrinal zone."""
    norm_result = normalize_query(request.query)
    leg_category = _detect_leg_category(request.query, norm_result)

    zone_engine = ZonedAnalysisEngine()
    routing = zone_engine.route_to_zone(leg_category)
    zone_analysis = zone_engine.get_zone_analysis(
        request.query, routing["zone"], request.jurisdiction
    )

    return {
        "engine_id": ENGINE_ID,
        "routing": routing,
        "zone_analysis": zone_analysis,
        "leg_category": leg_category,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/zones")
async def list_zones() -> Dict[str, Any]:
    """List all doctrinal zones."""
    engine = ZonedAnalysisEngine()
    zones = {}
    for zone_name, zone_info in engine.ZONES.items():
        zones[zone_name] = {
            "description": zone_info["description"],
            "categories": zone_info["categories"],
            "authority_floor": zone_info["authority_floor"],
            "key_sources_count": len(zone_info["key_sources"]),
        }
    return {"engine_id": ENGINE_ID, "zones": zones}


# ============================================================================
# LEGISLATIVE IMPACT ASSESSMENT
# ============================================================================

class LegislativeImpactAssessor:
    """Assesses the potential impact of proposed legislation."""

    IMPACT_DIMENSIONS: ClassVar[List[str]] = [
        "economic_impact",
        "regulatory_burden",
        "preemption_effect",
        "constitutional_risk",
        "political_feasibility",
        "enforcement_complexity",
        "judicial_review_vulnerability",
        "stakeholder_impact",
        "federal_state_relations",
        "sunset_and_review",
    ]

    ASSESSMENT_FACTORS: ClassVar[Dict[str, Dict[str, Any]]] = {
        "economic_impact": {
            "description": "Estimated economic effect on regulated entities and the broader economy",
            "metrics": ["annual_cost_to_industry", "annual_benefit_to_public", "net_economic_effect"],
            "threshold_major": 100_000_000,
            "cbo_score_required": True,
        },
        "regulatory_burden": {
            "description": "Compliance burden imposed on regulated entities",
            "metrics": ["paperwork_hours", "new_reporting_requirements", "new_permits_required"],
            "pra_applicable": True,
            "rfa_applicable": True,
        },
        "preemption_effect": {
            "description": "Effect on state and local regulatory authority",
            "metrics": ["state_laws_preempted", "local_ordinances_affected", "savings_clause_scope"],
            "presumption_against_preemption": True,
        },
        "constitutional_risk": {
            "description": "Risk of constitutional challenge",
            "metrics": ["nondelegation_risk", "commerce_clause_risk", "due_process_risk", "first_amendment_risk"],
            "major_questions_risk": True,
        },
        "political_feasibility": {
            "description": "Likelihood of passage given current political dynamics",
            "metrics": ["bipartisan_support", "committee_support", "leadership_support", "filibuster_risk"],
            "reconciliation_eligible": False,
        },
        "enforcement_complexity": {
            "description": "Difficulty of implementing and enforcing the legislation",
            "metrics": ["agency_capacity", "enforcement_mechanism", "penalty_structure", "judicial_review_provision"],
        },
        "judicial_review_vulnerability": {
            "description": "Vulnerability to successful judicial challenge",
            "metrics": ["arbitrary_capricious_risk", "delegation_challenge_risk", "vagueness_challenge_risk"],
            "post_loper_bright": True,
        },
        "stakeholder_impact": {
            "description": "Impact on key stakeholder groups",
            "metrics": ["industry_groups", "consumer_groups", "state_governments", "federal_agencies"],
        },
        "federal_state_relations": {
            "description": "Effect on the federal-state regulatory balance",
            "metrics": ["cooperative_federalism", "commandeering_risk", "conditional_spending"],
        },
        "sunset_and_review": {
            "description": "Built-in review and sunset mechanisms",
            "metrics": ["sunset_provision", "gao_review", "ig_review", "congressional_reporting"],
        },
    }

    def assess_impact(self, bill_info: Dict[str, Any]) -> Dict[str, Any]:
        """Assess the impact of proposed legislation across all dimensions."""
        assessments: Dict[str, Dict[str, Any]] = {}

        for dimension in self.IMPACT_DIMENSIONS:
            factor = self.ASSESSMENT_FACTORS.get(dimension, {})
            score = 0.5
            notes: List[str] = []

            if dimension == "economic_impact":
                annual_cost = bill_info.get("estimated_annual_cost", 0)
                if annual_cost >= factor.get("threshold_major", 100_000_000):
                    score = 0.9
                    notes.append("Major rule threshold exceeded; OIRA review required under E.O. 12866")
                    notes.append("CBO score required for budget impact assessment")
                elif annual_cost > 0:
                    score = 0.6
                    notes.append("Economic impact present but below major rule threshold")
                else:
                    score = 0.3
                    notes.append("Minimal direct economic impact identified")

            elif dimension == "constitutional_risk":
                has_broad_delegation = bill_info.get("broad_delegation", False)
                has_preemption = bill_info.get("preemption_clause", False)
                regulatory_scope = bill_info.get("regulatory_scope", "narrow")

                if has_broad_delegation:
                    score += 0.2
                    notes.append("Broad delegation may face nondelegation or major questions challenge")
                if has_preemption:
                    score += 0.1
                    notes.append("Preemption clause present; scope may be litigated")
                if regulatory_scope in ("broad", "transformative"):
                    score += 0.2
                    notes.append("Broad regulatory scope increases major questions doctrine risk")
                score = min(score, 1.0)

            elif dimension == "political_feasibility":
                bipartisan = bill_info.get("bipartisan_support", False)
                reconciliation = bill_info.get("reconciliation_eligible", False)
                if bipartisan:
                    score = 0.8
                    notes.append("Bipartisan support increases passage likelihood")
                elif reconciliation:
                    score = 0.6
                    notes.append("Reconciliation-eligible: can bypass filibuster with simple majority")
                else:
                    score = 0.4
                    notes.append("May face filibuster; 60-vote threshold applies in Senate")

            elif dimension == "judicial_review_vulnerability":
                post_loper = True
                if post_loper:
                    score = 0.6
                    notes.append("Post-Loper Bright: courts exercise independent judgment on statutory meaning")
                    notes.append("Agency interpretations will receive Skidmore persuasive weight, not Chevron deference")

            assessments[dimension] = {
                "description": factor.get("description", ""),
                "score": round(score, 4),
                "level": "high" if score >= 0.7 else "medium" if score >= 0.4 else "low",
                "notes": notes,
            }

        overall_impact = sum(a["score"] for a in assessments.values()) / max(len(assessments), 1)

        return {
            "bill_info": bill_info,
            "assessments": assessments,
            "overall_impact_score": round(overall_impact, 4),
            "overall_impact_level": "high" if overall_impact >= 0.7 else "medium" if overall_impact >= 0.4 else "low",
            "dimensions_assessed": len(assessments),
            "assessed_at": datetime.now(timezone.utc).isoformat(),
        }


@app.post("/impact/assess")
async def assess_legislative_impact(bill_info: Dict[str, Any]) -> Dict[str, Any]:
    """Assess the potential impact of proposed legislation."""
    assessor = LegislativeImpactAssessor()
    result = assessor.assess_impact(bill_info)
    return {"engine_id": ENGINE_ID, "result": result}


# ============================================================================
# CONGRESSIONAL PROCEDURE ADVISOR
# ============================================================================

class CongressionalProcedureAdvisor:
    """Provides detailed congressional procedure analysis and strategy."""

    HOUSE_PROCEDURES: ClassVar[Dict[str, Dict[str, Any]]] = {
        "introduction": {
            "description": "Member introduces bill by dropping it in the hopper",
            "requirements": "Any member may introduce a bill; no co-sponsor requirement",
            "timing": "Available any time Congress is in session",
        },
        "committee_referral": {
            "description": "Speaker refers bill to standing committee(s) of jurisdiction",
            "requirements": "Bill must fall within committee jurisdiction",
            "timing": "Typically same day as introduction",
            "key_consideration": "Multiple referral possible for bills spanning jurisdictions",
        },
        "committee_action": {
            "description": "Committee may hold hearings, markup, and vote on the bill",
            "requirements": "Chairman controls agenda; majority vote to report",
            "timing": "Varies widely; most bills never receive committee action",
            "key_consideration": "Chairman's mark is the starting point for markup amendments",
        },
        "rules_committee": {
            "description": "Rules Committee sets terms for floor debate (open, closed, or structured rule)",
            "requirements": "Majority of Rules Committee; reflects Speaker's priorities",
            "timing": "After committee reports the bill",
            "key_consideration": "Closed rules limit amendments; open rules permit any germane amendment",
        },
        "floor_debate": {
            "description": "Full House debates and votes on the bill under the adopted rule",
            "requirements": "Quorum (218 members); simple majority to pass",
            "timing": "Scheduled by Majority Leader; typically one day of debate",
            "key_consideration": "Motion to recommit is the minority's last chance to amend",
        },
        "engrossment_messaging": {
            "description": "Passed bill is engrossed and sent (messaged) to the Senate",
            "requirements": "Automatic upon passage",
            "timing": "Same day or next business day",
        },
    }

    SENATE_PROCEDURES: ClassVar[Dict[str, Dict[str, Any]]] = {
        "introduction": {
            "description": "Senator introduces bill; first and second reading automatic",
            "requirements": "Any Senator may introduce; recognition by presiding officer",
            "timing": "Available any time Senate is in session",
        },
        "committee_referral": {
            "description": "Presiding officer refers bill to committee of jurisdiction",
            "requirements": "Based on committee jurisdiction rules",
            "timing": "Automatic after introduction",
        },
        "committee_action": {
            "description": "Committee may hold hearings, markup, and report the bill",
            "requirements": "Chairman controls agenda; majority vote to report",
            "timing": "Varies; tagging rule allows 48-hour delay",
        },
        "floor_consideration": {
            "description": "Majority Leader schedules the bill for floor action via unanimous consent or motion to proceed",
            "requirements": "Three-fifths vote (60) to invoke cloture on motion to proceed; or UC agreement",
            "timing": "Majority Leader controls schedule",
            "key_consideration": "Without UC, 60 votes needed to overcome filibuster on motion to proceed",
        },
        "amendment_process": {
            "description": "Senators may offer amendments; no germaneness requirement (usually)",
            "requirements": "Any Senator may offer; limited post-cloture",
            "timing": "During floor consideration",
            "key_consideration": "Non-germane amendments (riders) are permitted unless UC agreement or reconciliation",
        },
        "cloture_and_vote": {
            "description": "Cloture requires 60 votes; 30 hours post-cloture debate; simple majority to pass",
            "requirements": "Petition filed by 16 Senators; vote on cloture 2 days later",
            "timing": "After floor debate",
            "key_consideration": "Post-cloture amendments must be germane and filed before cloture vote",
        },
    }

    RECONCILIATION_PROCEDURE: ClassVar[Dict[str, Any]] = {
        "overview": "Budget reconciliation allows tax, spending, and debt limit legislation to pass the Senate with 51 votes",
        "steps": [
            "1. Budget resolution includes reconciliation instructions to committees",
            "2. Instructed committees report legislation meeting dollar targets",
            "3. Budget Committee assembles omnibus reconciliation bill (no substantive changes)",
            "4. Senate debate limited to 20 hours (no filibuster)",
            "5. Amendments must be germane and budget-neutral (Byrd Rule applies)",
            "6. Simple majority required for passage (51 votes, or 50 + VP)",
            "7. Conference with House version if necessary",
        ],
        "byrd_rule_tests": [
            "Provision must produce a change in outlays or revenues",
            "If no budget committee recommendation, provision must be within committee jurisdiction",
            "Provision must not increase the deficit beyond the budget window",
            "Changes in outlays or revenues must not be merely incidental to non-budgetary policy",
            "Provision must not increase deficits for fiscal years beyond the budget window (unless offset)",
            "Provision must not change Social Security outlays or revenues",
        ],
        "key_limitation": "Only one reconciliation bill per topic (spending, revenue, debt limit) per budget resolution per fiscal year",
    }

    def get_procedure_guide(self, chamber: str) -> Dict[str, Any]:
        """Get the procedural guide for a specific chamber."""
        if chamber.lower() == "house":
            return {
                "chamber": "House of Representatives",
                "procedures": self.HOUSE_PROCEDURES,
                "key_rule": "Rules Committee controls floor debate terms; simple majority governs",
            }
        elif chamber.lower() == "senate":
            return {
                "chamber": "Senate",
                "procedures": self.SENATE_PROCEDURES,
                "key_rule": "60-vote cloture threshold for most measures; unlimited debate otherwise",
            }
        elif chamber.lower() == "reconciliation":
            return {
                "chamber": "Reconciliation (Both)",
                "procedure": self.RECONCILIATION_PROCEDURE,
                "key_rule": "Simple majority; Byrd Rule restricts extraneous provisions",
            }
        return {"error": f"Unknown chamber: {chamber}. Use 'house', 'senate', or 'reconciliation'."}

    def assess_passage_pathway(
        self,
        bill_info: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Assess the most viable pathway for a bill's passage."""
        is_budget_related = bill_info.get("budget_related", False)
        has_60_votes = bill_info.get("has_60_votes", False)
        bipartisan = bill_info.get("bipartisan", False)
        byrd_rule_compliant = bill_info.get("byrd_rule_compliant", True)
        urgent = bill_info.get("urgent", False)

        pathways: List[Dict[str, Any]] = []

        if is_budget_related and byrd_rule_compliant:
            pathways.append({
                "pathway": "Budget Reconciliation",
                "viability": 0.8,
                "pros": ["Simple majority (51 votes)", "No filibuster", "Time-limited debate"],
                "cons": ["Limited to tax, spending, debt limit", "Byrd Rule restricts policy provisions", "Only once per budget resolution per topic"],
                "key_requirement": "Budget resolution with reconciliation instructions must pass first",
            })

        if has_60_votes or bipartisan:
            pathways.append({
                "pathway": "Regular Order (60-vote threshold)",
                "viability": 0.7 if has_60_votes else 0.5,
                "pros": ["No content limitations", "Full amendment process", "Stronger legislative legitimacy"],
                "cons": ["60-vote cloture threshold in Senate", "Lengthy floor process", "Amendment exposure"],
                "key_requirement": "60 votes for cloture or unanimous consent agreement",
            })

        if urgent:
            pathways.append({
                "pathway": "Suspension of the Rules (House) / UC Agreement (Senate)",
                "viability": 0.4,
                "pros": ["Faster consideration", "Limited debate"],
                "cons": ["Two-thirds required in House", "Any Senator can object to UC", "No amendments"],
                "key_requirement": "Broad bipartisan support required",
            })

        pathways.append({
            "pathway": "Must-Pass Vehicle (Attach to NDAA, Appropriations, etc.)",
            "viability": 0.6,
            "pros": ["Leverages must-pass legislation", "Avoids standalone filibuster"],
            "cons": ["Germaneness issues", "Conference committee may strip", "Political opposition to riders"],
            "key_requirement": "Identify appropriate vehicle and supportive committee chairs",
        })

        pathways.sort(key=lambda p: p["viability"], reverse=True)

        return {
            "bill_info": bill_info,
            "recommended_pathway": pathways[0]["pathway"] if pathways else "None identified",
            "all_pathways": pathways,
            "total_options": len(pathways),
            "assessed_at": datetime.now(timezone.utc).isoformat(),
        }


@app.get("/procedure/{chamber}")
async def procedure_guide(chamber: str) -> Dict[str, Any]:
    """Get the procedural guide for a chamber."""
    advisor = CongressionalProcedureAdvisor()
    result = advisor.get_procedure_guide(chamber)
    return {"engine_id": ENGINE_ID, "result": result}


@app.post("/passage/pathway")
async def passage_pathway(bill_info: Dict[str, Any]) -> Dict[str, Any]:
    """Assess the most viable pathway for a bill's passage."""
    advisor = CongressionalProcedureAdvisor()
    result = advisor.assess_passage_pathway(bill_info)
    return {"engine_id": ENGINE_ID, "result": result}


# ============================================================================
# APPROPRIATIONS ANALYZER
# ============================================================================

class AppropriationsAnalyzer:
    """Analyzes appropriations process and budget issues."""

    APPROPRIATIONS_SUBCOMMITTEES: ClassVar[List[str]] = [
        "Agriculture, Rural Development, FDA",
        "Commerce, Justice, Science",
        "Defense",
        "Energy and Water",
        "Financial Services and General Government",
        "Homeland Security",
        "Interior, Environment",
        "Labor, HHS, Education",
        "Legislative Branch",
        "Military Construction, Veterans Affairs",
        "State, Foreign Operations",
        "Transportation, HUD",
    ]

    BUDGET_PROCESS_TIMELINE: ClassVar[List[Dict[str, str]]] = [
        {"step": "President's Budget", "deadline": "First Monday in February", "description": "President submits budget request to Congress"},
        {"step": "Budget Resolution", "deadline": "April 15", "description": "Congress adopts budget resolution setting spending levels"},
        {"step": "302(a) Allocations", "deadline": "Shortly after budget resolution", "description": "Budget Committee allocates spending to Appropriations Committees"},
        {"step": "302(b) Suballocations", "deadline": "Before markup", "description": "Appropriations Committee allocates among subcommittees"},
        {"step": "Subcommittee Markups", "deadline": "May-June", "description": "Subcommittees mark up individual bills"},
        {"step": "Full Committee Markups", "deadline": "June-July", "description": "Full Appropriations Committee considers bills"},
        {"step": "Floor Action", "deadline": "June-September", "description": "Full chamber considers appropriations bills"},
        {"step": "Conference/Resolution", "deadline": "By September 30", "description": "Resolve differences between chambers"},
        {"step": "Presidential Action", "deadline": "Before October 1", "description": "President signs or vetoes; CR if needed"},
    ]

    def get_budget_timeline(self) -> Dict[str, Any]:
        """Return the standard budget process timeline."""
        return {
            "fiscal_year_start": "October 1",
            "timeline": self.BUDGET_PROCESS_TIMELINE,
            "subcommittees": self.APPROPRIATIONS_SUBCOMMITTEES,
            "key_statutes": [
                "Congressional Budget Act of 1974 (2 USC 621 et seq.)",
                "Antideficiency Act (31 USC 1341-1342, 1511-1519)",
                "Impoundment Control Act (2 USC 681-688)",
                "PAYGO Act of 2010 (Title I of Pub. L. 111-139)",
            ],
            "key_issues": {
                "continuing_resolution": "Temporary funding at prior-year levels if regular appropriations not enacted by Oct. 1",
                "government_shutdown": "Failure to enact CR or regular appropriations results in funding gap",
                "sequestration": "Automatic across-the-board cuts triggered by failure to meet deficit targets",
                "debt_ceiling": "Statutory limit on federal borrowing (31 USC 3101); must be raised or suspended",
                "earmarks": "Congressionally directed spending; rules vary by chamber and Congress",
            },
        }

    def assess_shutdown_risk(self, current_status: Dict[str, Any]) -> Dict[str, Any]:
        """Assess the risk of a government shutdown."""
        days_to_deadline = current_status.get("days_to_funding_deadline", 30)
        bills_enacted = current_status.get("appropriations_bills_enacted", 0)
        cr_in_effect = current_status.get("cr_in_effect", False)
        political_agreement = current_status.get("political_agreement", False)

        risk_score = 0.0
        factors: List[str] = []

        if days_to_deadline <= 7:
            risk_score += 0.4
            factors.append("Less than 7 days to funding deadline")
        elif days_to_deadline <= 30:
            risk_score += 0.2
            factors.append("Less than 30 days to funding deadline")

        if bills_enacted < 12:
            gap = 12 - bills_enacted
            risk_score += 0.05 * gap
            factors.append(f"{gap} of 12 regular appropriations bills not enacted")

        if not political_agreement:
            risk_score += 0.2
            factors.append("No bipartisan agreement on spending levels")

        if cr_in_effect:
            risk_score += 0.1
            factors.append("Currently operating under continuing resolution")

        risk_score = min(risk_score, 1.0)

        return {
            "shutdown_risk_score": round(risk_score, 4),
            "risk_level": "high" if risk_score >= 0.6 else "medium" if risk_score >= 0.3 else "low",
            "factors": factors,
            "current_status": current_status,
            "key_deadline": f"{days_to_deadline} days to funding deadline",
            "assessed_at": datetime.now(timezone.utc).isoformat(),
        }


@app.get("/appropriations/timeline")
async def appropriations_timeline() -> Dict[str, Any]:
    """Return the standard appropriations process timeline."""
    analyzer = AppropriationsAnalyzer()
    return {"engine_id": ENGINE_ID, "result": analyzer.get_budget_timeline()}


@app.post("/appropriations/shutdown-risk")
async def shutdown_risk(current_status: Dict[str, Any]) -> Dict[str, Any]:
    """Assess government shutdown risk."""
    analyzer = AppropriationsAnalyzer()
    result = analyzer.assess_shutdown_risk(current_status)
    return {"engine_id": ENGINE_ID, "result": result}


# ============================================================================
# SIGNING STATEMENT ANALYZER
# ============================================================================

class SigningStatementAnalyzer:
    """Analyzes presidential signing statements and their legal effect."""

    STATEMENT_CATEGORIES: ClassVar[Dict[str, Dict[str, Any]]] = {
        "constitutional_objection": {
            "description": "President raises constitutional concerns about specific provisions",
            "legal_effect": "No binding legal effect on courts; may signal nonenforcement",
            "frequency": "Most common and most controversial type",
            "examples": [
                "Objection to reporting requirements as infringing executive privilege",
                "Objection to legislative veto provisions (post-Chadha)",
                "Objection to provisions limiting Commander-in-Chief authority",
            ],
        },
        "interpretive": {
            "description": "President states executive branch interpretation of ambiguous provisions",
            "legal_effect": "No binding effect; may be cited as evidence of statutory meaning but carries minimal weight",
            "frequency": "Common; used to guide agency implementation",
            "examples": [
                "Clarifying the scope of a broad delegation",
                "Interpreting ambiguous enforcement provisions",
                "Defining terms not defined in the statute",
            ],
        },
        "political_rhetorical": {
            "description": "President makes political statements about the legislation",
            "legal_effect": "No legal effect; purely political communication",
            "frequency": "Very common for major legislation",
            "examples": [
                "Praising bipartisan cooperation",
                "Highlighting key provisions",
                "Signaling policy priorities",
            ],
        },
    }

    def analyze_statement(self, statement_info: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a presidential signing statement."""
        statement_type = statement_info.get("type", "interpretive")
        category = self.STATEMENT_CATEGORIES.get(statement_type, self.STATEMENT_CATEGORIES["interpretive"])

        return {
            "statement_type": statement_type,
            "category": category,
            "legal_weight": "None (signing statements have no binding legal effect on courts)",
            "practical_significance": (
                "May signal executive nonenforcement of specific provisions; "
                "agencies may use as implementation guidance; "
                "courts have generally not treated signing statements as legislative history"
            ),
            "key_precedent": "Signing statements have been used since Monroe but became controversial under George W. Bush",
            "aba_position": "ABA opposes using signing statements to circumvent legislative intent (2006 resolution)",
            "analyzed_at": datetime.now(timezone.utc).isoformat(),
        }


@app.post("/signing-statement/analyze")
async def analyze_signing_statement(statement_info: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze a presidential signing statement."""
    analyzer = SigningStatementAnalyzer()
    result = analyzer.analyze_statement(statement_info)
    return {"engine_id": ENGINE_ID, "result": result}


# ============================================================================
# TEXAS SUNSET REVIEW ANALYZER
# ============================================================================

class TexasSunsetAnalyzer:
    """Analyzes Texas Sunset Advisory Commission review process."""

    SUNSET_PROCESS_STEPS: ClassVar[List[Dict[str, str]]] = [
        {"step": "Self-Evaluation Report", "description": "Agency submits SER to SAC 18 months before sunset date"},
        {"step": "Staff Review", "description": "SAC staff conducts comprehensive review of agency operations"},
        {"step": "Staff Report", "description": "SAC staff publishes detailed report with recommendations"},
        {"step": "Public Hearing", "description": "SAC holds public hearing on agency; stakeholder testimony"},
        {"step": "Decision Meeting", "description": "SAC votes on recommendations (continue, modify, abolish)"},
        {"step": "SAC Report to Legislature", "description": "SAC sends final report and recommendations to Legislature"},
        {"step": "Sunset Bill Filed", "description": "Sunset bill implementing SAC recommendations is filed"},
        {"step": "Legislative Action", "description": "Legislature considers sunset bill; may modify SAC recommendations"},
        {"step": "Governor Action", "description": "Governor signs or vetoes sunset legislation"},
        {"step": "Effective Date", "description": "If no sunset bill passes, agency is abolished on September 1 following next regular session"},
    ]

    def get_sunset_guide(self) -> Dict[str, Any]:
        """Return the Texas Sunset Review process guide."""
        return {
            "authority": "Tex. Gov't Code Ch. 325 (Texas Sunset Act)",
            "review_cycle": "12 years for most agencies",
            "commission": "Sunset Advisory Commission (5 House members, 5 Senate members, 2 public members)",
            "process_steps": self.SUNSET_PROCESS_STEPS,
            "possible_outcomes": [
                "Continue agency with reforms",
                "Continue agency without changes",
                "Merge agency with another",
                "Transfer agency functions elsewhere",
                "Abolish agency (automatic if sunset bill not passed)",
            ],
            "key_dates": "Agency sunset date is September 1 following the next regular legislative session after the review cycle expires",
            "notable_reviews": [
                "Texas Railroad Commission (periodic review; multiple reform recommendations)",
                "Texas Dept. of Licensing and Regulation (2019; significant restructuring)",
                "Texas Workforce Commission (2015; continued with modifications)",
            ],
        }

    def assess_sunset_risk(self, agency_info: Dict[str, Any]) -> Dict[str, Any]:
        """Assess an agency's risk profile for sunset review."""
        performance_issues = agency_info.get("performance_issues", False)
        public_complaints = agency_info.get("public_complaints", "low")
        overlap_with_other = agency_info.get("overlap_with_other_agency", False)
        political_controversy = agency_info.get("political_controversy", "low")
        essential_function = agency_info.get("essential_function", True)

        risk_score = 0.2
        factors: List[str] = []

        if performance_issues:
            risk_score += 0.2
            factors.append("Performance issues identified in prior reviews")
        if public_complaints in ("high", "very_high"):
            risk_score += 0.15
            factors.append("High volume of public complaints")
        if overlap_with_other:
            risk_score += 0.2
            factors.append("Functional overlap with another agency (merger risk)")
        if political_controversy in ("high", "very_high"):
            risk_score += 0.15
            factors.append("Agency is politically controversial")
        if not essential_function:
            risk_score += 0.25
            factors.append("Agency function may not be considered essential")

        risk_score = min(risk_score, 1.0)

        return {
            "agency_info": agency_info,
            "sunset_risk_score": round(risk_score, 4),
            "risk_level": "high" if risk_score >= 0.6 else "medium" if risk_score >= 0.3 else "low",
            "likely_outcome": (
                "Abolition or major restructuring" if risk_score >= 0.6
                else "Continuation with reforms" if risk_score >= 0.3
                else "Continuation with minor changes"
            ),
            "factors": factors,
            "assessed_at": datetime.now(timezone.utc).isoformat(),
        }


@app.get("/texas/sunset/guide")
async def texas_sunset_guide() -> Dict[str, Any]:
    """Return the Texas Sunset Review process guide."""
    analyzer = TexasSunsetAnalyzer()
    return {"engine_id": ENGINE_ID, "result": analyzer.get_sunset_guide()}


@app.post("/texas/sunset/risk")
async def texas_sunset_risk(agency_info: Dict[str, Any]) -> Dict[str, Any]:
    """Assess an agency's risk profile for Texas Sunset Review."""
    analyzer = TexasSunsetAnalyzer()
    result = analyzer.assess_sunset_risk(agency_info)
    return {"engine_id": ENGINE_ID, "result": result}


# ============================================================================
# DOCTRINE TOPICS ENDPOINT
# ============================================================================

@app.get("/doctrines/topics")
async def doctrine_topics() -> Dict[str, Any]:
    """List all doctrine topics."""
    topics = get_all_doctrine_topics()
    return {"engine_id": ENGINE_ID, "topics": topics, "total": len(topics)}


@app.get("/doctrines/categories")
async def doctrine_categories() -> Dict[str, Any]:
    """List all doctrine categories."""
    categories = get_all_doctrine_categories()
    return {"engine_id": ENGINE_ID, "categories": categories, "total": len(categories)}


@app.get("/doctrines/{topic}")
async def get_doctrine(topic: str) -> Dict[str, Any]:
    """Retrieve a single doctrine block by topic."""
    block = get_doctrine_block(topic)
    if not block:
        raise HTTPException(status_code=404, detail=f"Doctrine topic '{topic}' not found")
    return {"engine_id": ENGINE_ID, "doctrine": block.to_dict()}


# ============================================================================
# BATCH QUERY ENDPOINT
# ============================================================================

@app.post("/query/batch")
async def batch_query(requests: List[QueryRequest]) -> Dict[str, Any]:
    """Process multiple queries in batch."""
    if len(requests) > 20:
        raise HTTPException(status_code=400, detail="Maximum 20 queries per batch")

    results: List[Dict[str, Any]] = []
    for req in requests:
        try:
            response = await query_endpoint(req)
            results.append({
                "query": req.query[:100],
                "mode": req.mode,
                "confidence_score": response.confidence_score,
                "confidence_band": response.confidence_band,
                "leg_category": response.leg_category,
                "trace_id": response.trace_id,
                "duration_ms": response.duration_ms,
                "success": True,
            })
        except Exception as exc:
            results.append({
                "query": req.query[:100],
                "mode": req.mode,
                "error": str(exc),
                "success": False,
            })

    successful = sum(1 for r in results if r.get("success"))
    return {
        "engine_id": ENGINE_ID,
        "total": len(results),
        "successful": successful,
        "failed": len(results) - successful,
        "results": results,
    }


# ============================================================================
# NORMALIZATION ENDPOINT
# ============================================================================

@app.post("/normalize")
async def normalize_endpoint(request: QueryRequest) -> Dict[str, Any]:
    """Normalize a query through the semantic dictionary."""
    result = normalize_query(request.query)
    return {"engine_id": ENGINE_ID, "normalization": result.to_dict()}


# ============================================================================
# VERSION / INFO ENDPOINT
# ============================================================================

@app.get("/info")
async def engine_info() -> Dict[str, Any]:
    """Return engine information and metadata."""
    return {
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "engine_version": ENGINE_VERSION,
        "engine_mode": ENGINE_MODE,
        "port": ENGINE_PORT,
        "tier": ENGINE_TIER,
        "authority": ENGINE_AUTHORITY,
        "domain": "Legislative Analysis",
        "doctrine_blocks": len(DOCTRINE_BLOCKS),
        "semantic_map_entries": len(get_semantic_map()),
        "confidence_bands": list(CONFIDENCE_BANDS.keys()),
        "response_modes": ["fast", "analysis", "memo", "bill_analysis", "regulatory_review"],
        "banned_phrases_count": len(BANNED_PHRASES),
        "authority_weight_sources": len(AUTHORITY_WEIGHTS),
        "build_date": "2026-02-10",
        "build_author": "ECHO OMEGA PRIME",
    }


# ============================================================================
# ERROR HANDLER
# ============================================================================

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Global exception handler for unhandled errors."""
    error_id = log_error(
        domain=ErrorDomain.SYSTEM,
        message=str(exc),
        metadata={"path": str(request.url), "method": request.method},
    )
    logger.exception("Unhandled error [{}]: {}", error_id, exc)
    return JSONResponse(
        status_code=500,
        content={
            "engine_id": ENGINE_ID,
            "error_id": error_id,
            "message": "Internal server error",
            "detail": str(exc),
        },
    )


# ============================================================================
# ENTRYPOINT
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
        level="DEBUG",
    )

    logger.info(
        "Launching {} v{} on {}:{}",
        ENGINE_NAME,
        ENGINE_VERSION,
        ENGINE_HOST,
        ENGINE_PORT,
    )

    uvicorn.run(
        "engine:app",
        host=ENGINE_HOST,
        port=ENGINE_PORT,
        reload=False,
        workers=1,
        log_level="info",
    )
