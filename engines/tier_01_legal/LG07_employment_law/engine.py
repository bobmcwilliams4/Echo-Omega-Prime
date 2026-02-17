"""
LG07 EMPLOYMENT LAW ENGINE - Production Architecture
=======================================================
Professional-grade employment law analysis system covering federal and
state employment statutes, discrimination, wage/hour, leave, safety,
benefits, labor relations, and employment contract disputes.

Architecture:
    Layer 1: Doctrine Cache (0-200ms) - Pre-compiled expert employment reasoning
    Layer 2: Semantic Search (200-700ms) - TF-IDF + BM25 on cache miss
    Layer 3: Employment Analysis (700-1500ms) - Structured claim analysis
    Layer 4: Deep Analysis (on-demand) - Multi-doctrine synthesis

Response Modes:
    FAST: Doctrine-driven, minimal citations, sub-2 seconds
    REVIEW: Detailed analysis with compliance scoring and recommendations
    MEMO: Full legal memorandum with statutory analysis and case law

TIE-20 Components:
    1.  three_layer_response
    2.  response_modes
    3.  doctrine_cache
    4.  authority_hardening
    5.  confidence_stratification
    6.  semantic_normalization
    7.  vector_search_chromadb (TF-IDF/BM25 implementation)
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

Port: 8397
Engine ID: LG07
Tier: LEGAL (Auth 5.0)
Mode: DET (Deterministic)

Version: 1.0.0
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
    EmploymentMetricType,
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
    get_agency_map,
    get_statute_patterns,
    CITATION_PATTERNS,
)

import sys

# Ensure sibling modules are importable
ENGINE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ENGINE_DIR))
from doctrines import (
    DOCTRINE_CACHE,
    DoctrineResponse,
    EmploymentDoctrineEngine,
    get_engine as get_doctrine_engine,
    get_doctrine_hash,
    get_doctrine_count,
)

from search import (
    DoctrineSearchIndex,
    SearchResult,
    HybridSearchEngine,
    EmploymentClaimClassifier,
    ClaimType,
    StatuteSearchEngine,
    CaseSearchEngine,
    SearchResultAggregator,
    get_search_index,
    get_hybrid_engine,
    search_doctrines,
    hybrid_search,
)

# ============================================================================
# CONSTANTS
# ============================================================================

ENGINE_ID = "LG07"
ENGINE_NAME = "Employment Law Engine"
ENGINE_VERSION = "1.0.0"
ENGINE_PORT = 8397
ENGINE_TIER = "LEGAL"
ENGINE_MODE = "DET"
AUTHORITY_LEVEL = 5.0

CONFIG_PATH = Path("O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/LG07_employment_law/config.json")
LOG_DIR = Path("O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/LG07_employment_law/logs")
TELEMETRY_DIR = Path("O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/LG07_employment_law/telemetry")
AUDIT_DIR = Path("O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/LG07_employment_law/audit")

BANNED_PHRASES: List[str] = [
    "this is definitely illegal",
    "you will certainly win",
    "there is no risk of liability",
    "this is guaranteed to be enforceable",
    "no court would rule against",
    "this is completely compliant",
    "there are no employment law issues",
    "this termination is bulletproof",
    "you cannot be sued for this",
    "this is always lawful",
]

DISCLOSURE_TEMPLATES: Dict[str, str] = {
    "jurisdiction_variance": "Employment law varies significantly by state and locality. This analysis assumes {jurisdiction} law unless otherwise specified.",
    "not_legal_advice": "This analysis is for informational purposes only. Consult qualified employment counsel for binding legal opinions.",
    "temporal_caveat": "Employment law evolves through legislation, regulation, and case law. This analysis reflects law as of {analysis_date}.",
    "fact_dependency": "Conclusions depend on the accuracy and completeness of the facts provided. Material omissions may change the analysis.",
    "administrative_requirements": "Many employment claims require exhaustion of administrative remedies (EEOC filing, DOL complaint) before litigation.",
}


# ============================================================================
# PYDANTIC MODELS - REQUEST/RESPONSE
# ============================================================================

class ResponseMode(str, Enum):
    """Available response modes."""
    FAST = "FAST"
    REVIEW = "REVIEW"
    MEMO = "MEMO"


class AnalysisRequest(BaseModel):
    """Incoming analysis request."""
    query: str = Field(..., min_length=3, max_length=10000, description="Employment law question or scenario")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response mode")
    jurisdiction: str = Field(default="federal", description="Jurisdiction for analysis")
    include_citations: bool = Field(default=True, description="Include case/statute citations")
    include_risk_score: bool = Field(default=True, description="Include risk assessment")
    include_remedies: bool = Field(default=True, description="Include available remedies")
    include_elements: bool = Field(default=True, description="Include claim elements")
    include_defenses: bool = Field(default=True, description="Include available defenses")
    max_doctrines: int = Field(default=5, ge=1, le=50, description="Maximum doctrines to analyze")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")


class BatchRequest(BaseModel):
    """Batch analysis request."""
    queries: List[str] = Field(..., min_length=1, max_length=20, description="List of queries")
    mode: ResponseMode = Field(default=ResponseMode.FAST)
    jurisdiction: str = Field(default="federal")


class DoctrineQueryRequest(BaseModel):
    """Request to look up a specific doctrine."""
    topic: str = Field(..., min_length=1, description="Doctrine topic key")


class SearchRequest(BaseModel):
    """Search request."""
    query: str = Field(..., min_length=2, max_length=5000)
    max_results: int = Field(default=20, ge=1, le=100)
    category_filter: Optional[str] = Field(default=None)
    include_statutes: bool = Field(default=True)
    include_cases: bool = Field(default=True)


class RiskCategory(BaseModel):
    """A single risk category with score."""
    category: str
    score: float = Field(ge=0.0, le=1.0)
    weight: float = Field(ge=0.0, le=1.0)
    description: str
    factors: List[str]


class RiskAssessment(BaseModel):
    """Comprehensive risk assessment."""
    overall_score: float = Field(ge=0.0, le=1.0)
    overall_band: str
    categories: List[RiskCategory]
    mitigating_factors: List[str]
    aggravating_factors: List[str]


class FactFragilityScore(BaseModel):
    """Fact fragility analysis for a query."""
    overall_fragility: float = Field(ge=0.0, le=1.0)
    fragility_band: str
    critical_facts: List[Dict[str, Any]]
    assumption_risks: List[str]
    missing_information: List[str]


class AnalysisResponse(BaseModel):
    """Structured analysis response."""
    engine_id: str = ENGINE_ID
    engine_version: str = ENGINE_VERSION
    trace_id: str
    query: str
    mode: str
    jurisdiction: str
    response_layer: str
    answer: str
    summary: str
    claim_type: str
    claim_confidence: float
    confidence: float
    confidence_band: str
    determinism_hash: str
    citations: List[str]
    statutes: List[str]
    elements: List[str]
    defenses: List[str]
    remedies: List[str]
    risk_assessment: Optional[RiskAssessment] = None
    fact_fragility: Optional[FactFragilityScore] = None
    doctrines_used: List[str]
    search_results_count: int
    processing_time_ms: float
    disclosures: List[str]
    epistemic_guardrails: Dict[str, Any]
    timestamp: str


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    engine_id: str
    engine_name: str
    engine_version: str
    port: int
    tier: str
    mode: str
    uptime_seconds: float
    doctrine_count: int
    doctrine_hash: str
    semantic_map_hash: str
    total_queries: int
    error_rate: float
    cache_hit_rate: float
    latency_p50: float
    latency_p99: float
    telemetry_chain_state: Dict[str, Any]


# ============================================================================
# CONFIDENCE STRATIFICATION
# ============================================================================

class ConfidenceStratifier:
    """Maps raw confidence scores to stratified bands with explanations."""

    BANDS: ClassVar[List[Tuple[float, float, str, str]]] = [
        (0.90, 1.00, "HIGH", "Strong statutory/case law support with clear precedent"),
        (0.75, 0.90, "MEDIUM-HIGH", "Well-supported with some jurisdictional variation"),
        (0.60, 0.75, "MEDIUM", "Reasonable support but significant fact-dependency"),
        (0.40, 0.60, "LOW-MEDIUM", "Uncertain outcome; competing legal theories apply"),
        (0.00, 0.40, "LOW", "Highly speculative; limited precedent or novel theory"),
    ]

    def stratify(self, confidence: float) -> Dict[str, Any]:
        """Stratify a confidence score into a band."""
        for low, high, band, description in self.BANDS:
            if low <= confidence <= high:
                return {
                    "score": round(confidence, 4),
                    "band": band,
                    "description": description,
                    "range": [low, high],
                }
        return {"score": round(confidence, 4), "band": "UNKNOWN", "description": "Unable to classify", "range": [0.0, 1.0]}

    def adjust_for_jurisdiction(self, confidence: float, jurisdiction: str) -> float:
        """Adjust confidence based on jurisdiction specificity."""
        if jurisdiction == "federal":
            return confidence
        if jurisdiction == "texas":
            return confidence * 0.95
        return confidence * 0.85

    def adjust_for_fact_completeness(self, confidence: float, fact_count: int) -> float:
        """Adjust confidence based on fact completeness."""
        if fact_count >= 10:
            return confidence
        if fact_count >= 5:
            return confidence * 0.90
        if fact_count >= 3:
            return confidence * 0.80
        return confidence * 0.65


# ============================================================================
# AUTHORITY HARDENING
# ============================================================================

class AuthorityHardener:
    """Validates and ranks authority sources for employment law citations."""

    AUTHORITY_HIERARCHY: ClassVar[Dict[str, float]] = {
        "us_supreme_court": 1.0,
        "federal_circuit_court": 0.9,
        "federal_district_court": 0.8,
        "state_supreme_court": 0.85,
        "state_appellate_court": 0.75,
        "federal_statute": 0.95,
        "state_statute": 0.88,
        "federal_regulation": 0.85,
        "eeoc_guidance": 0.75,
        "dol_opinion_letter": 0.70,
        "nlrb_decision": 0.80,
        "osha_standard": 0.82,
        "treatise": 0.60,
        "law_review": 0.55,
        "secondary_source": 0.40,
    }

    def rank_authorities(self, authorities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Rank authorities by hierarchy weight."""
        for auth in authorities:
            auth_type = auth.get("type", "secondary_source")
            auth["weight"] = self.AUTHORITY_HIERARCHY.get(auth_type, 0.3)
        return sorted(authorities, key=lambda a: a["weight"], reverse=True)

    def validate_citation(self, citation: str) -> Dict[str, Any]:
        """Validate a legal citation format."""
        for pattern, citation_type in CITATION_PATTERNS.items():
            if re.search(pattern, citation, re.IGNORECASE):
                return {
                    "citation": citation,
                    "type": citation_type,
                    "valid": True,
                    "weight": self.AUTHORITY_HIERARCHY.get(
                        self._map_citation_type(citation_type), 0.5
                    ),
                }
        return {"citation": citation, "type": "unknown", "valid": False, "weight": 0.3}

    def _map_citation_type(self, citation_type: str) -> str:
        """Map citation format type to authority hierarchy key."""
        mapping = {
            "us_reporter": "us_supreme_court",
            "supreme_court_reporter": "us_supreme_court",
            "lawyers_edition": "us_supreme_court",
            "federal_reporter": "federal_circuit_court",
            "federal_supplement": "federal_district_court",
            "south_western_reporter": "state_appellate_court",
            "cfr_labor": "federal_regulation",
            "cfr_public_health": "federal_regulation",
            "eeoc_case": "eeoc_guidance",
            "nlrb_case": "nlrb_decision",
        }
        return mapping.get(citation_type, "secondary_source")

    def compute_authority_score(self, citations: List[str]) -> float:
        """Compute aggregate authority score from citations."""
        if not citations:
            return 0.3
        weights: List[float] = []
        for citation in citations:
            result = self.validate_citation(citation)
            weights.append(result["weight"])
        return round(sum(weights) / len(weights), 4) if weights else 0.3


# ============================================================================
# RISK ASSESSMENT ENGINE
# ============================================================================

class RiskAssessmentEngine:
    """Comprehensive employment law risk assessment."""

    RISK_CATEGORIES: ClassVar[Dict[str, Dict[str, Any]]] = {
        "liability": {
            "weight": 0.25,
            "description": "Financial exposure from litigation",
            "factors": ["compensatory_damages", "punitive_damages", "back_pay", "front_pay", "liquidated_damages"],
        },
        "regulatory": {
            "weight": 0.20,
            "description": "Government enforcement action risk",
            "factors": ["dol_enforcement", "eeoc_charges", "osha_citations", "nlrb_complaints", "state_agency_actions"],
        },
        "operational": {
            "weight": 0.20,
            "description": "Impact on business operations",
            "factors": ["workforce_disruption", "morale_impact", "retention_risk", "productivity_loss"],
        },
        "reputational": {
            "weight": 0.15,
            "description": "Brand and public perception damage",
            "factors": ["media_exposure", "class_action_risk", "employer_brand", "recruiting_impact"],
        },
        "compliance": {
            "weight": 0.10,
            "description": "Systematic compliance posture",
            "factors": ["policy_gaps", "training_deficiency", "documentation_failures", "audit_readiness"],
        },
        "strategic": {
            "weight": 0.10,
            "description": "Long-term strategic implications",
            "factors": ["precedent_setting", "multi_jurisdiction", "union_organizing", "legislative_changes"],
        },
    }

    def assess(self, query: str, claim_type: ClaimType,
               doctrine_confidence: float, jurisdiction: str) -> RiskAssessment:
        """Perform risk assessment based on query analysis."""
        categories: List[RiskCategory] = []

        for cat_name, cat_info in self.RISK_CATEGORIES.items():
            score = self._score_category(cat_name, query, claim_type, doctrine_confidence)
            categories.append(RiskCategory(
                category=cat_name,
                score=score,
                weight=cat_info["weight"],
                description=cat_info["description"],
                factors=cat_info["factors"],
            ))

        overall = sum(c.score * c.weight for c in categories)
        overall_band = self._band(overall)
        mitigating = self._get_mitigating_factors(query, claim_type)
        aggravating = self._get_aggravating_factors(query, claim_type)

        return RiskAssessment(
            overall_score=round(overall, 4),
            overall_band=overall_band,
            categories=categories,
            mitigating_factors=mitigating,
            aggravating_factors=aggravating,
        )

    def _score_category(self, category: str, query: str, claim_type: ClaimType,
                         confidence: float) -> float:
        """Score a single risk category."""
        query_lower = query.lower()
        base_score = 0.5

        high_risk_terms = {
            "liability": ["class action", "punitive", "willful", "systemic", "pattern"],
            "regulatory": ["eeoc", "dol", "osha", "nlrb", "investigation", "audit"],
            "operational": ["mass layoff", "strike", "walkout", "shutdown", "reorganization"],
            "reputational": ["media", "press", "public", "social media", "lawsuit"],
            "compliance": ["no policy", "no training", "undocumented", "no records"],
            "strategic": ["precedent", "multi-state", "union", "legislation"],
        }

        for term in high_risk_terms.get(category, []):
            if term in query_lower:
                base_score += 0.1

        # Claim type adjustment
        high_risk_claims = {ClaimType.DISCRIMINATION, ClaimType.HARASSMENT, ClaimType.RETALIATION}
        if claim_type in high_risk_claims:
            base_score += 0.1

        # Confidence inverse adjustment
        base_score += (1.0 - confidence) * 0.15

        return round(min(1.0, max(0.0, base_score)), 4)

    def _band(self, score: float) -> str:
        """Map risk score to band."""
        if score >= 0.80:
            return "CRITICAL"
        if score >= 0.65:
            return "HIGH"
        if score >= 0.45:
            return "MODERATE"
        if score >= 0.25:
            return "LOW"
        return "MINIMAL"

    def _get_mitigating_factors(self, query: str, claim_type: ClaimType) -> List[str]:
        """Identify mitigating factors from query."""
        factors: List[str] = []
        query_lower = query.lower()
        if "policy" in query_lower and ("updated" in query_lower or "revised" in query_lower):
            factors.append("Updated policies may demonstrate good faith compliance efforts")
        if "training" in query_lower:
            factors.append("Anti-discrimination/harassment training may support affirmative defense")
        if "documented" in query_lower or "records" in query_lower:
            factors.append("Documentation of legitimate business reasons strengthens defense")
        if "investigation" in query_lower:
            factors.append("Prompt investigation of complaints demonstrates reasonable care")
        if "consistent" in query_lower:
            factors.append("Consistent application of policies reduces disparate treatment risk")
        return factors

    def _get_aggravating_factors(self, query: str, claim_type: ClaimType) -> List[str]:
        """Identify aggravating factors from query."""
        factors: List[str] = []
        query_lower = query.lower()
        if "no investigation" in query_lower or "ignored complaint" in query_lower:
            factors.append("Failure to investigate complaints increases liability exposure")
        if "pattern" in query_lower or "multiple" in query_lower:
            factors.append("Pattern of similar conduct suggests systemic problem")
        if "manager" in query_lower or "supervisor" in query_lower:
            factors.append("Managerial involvement imputes employer liability")
        if "written warning" not in query_lower and "terminated" in query_lower:
            factors.append("Absence of progressive discipline weakens legitimate reason defense")
        if "close in time" in query_lower or "shortly after" in query_lower:
            factors.append("Temporal proximity supports inference of retaliation")
        return factors


# ============================================================================
# FACT FRAGILITY SCORER
# ============================================================================

class FactFragilityScorer:
    """Assess how sensitive the legal conclusion is to factual assumptions."""

    def score(self, query: str, doctrines_used: List[str],
              confidence: float) -> FactFragilityScore:
        """Compute fact fragility for the analysis."""
        critical_facts = self._identify_critical_facts(query, doctrines_used)
        assumptions = self._identify_assumptions(query)
        missing = self._identify_missing_info(query, doctrines_used)

        fragility = 0.3
        fragility += len(assumptions) * 0.05
        fragility += len(missing) * 0.08
        fragility -= len(critical_facts) * 0.02
        fragility = max(0.0, min(1.0, fragility))

        band = self._fragility_band(fragility)

        return FactFragilityScore(
            overall_fragility=round(fragility, 4),
            fragility_band=band,
            critical_facts=critical_facts,
            assumption_risks=assumptions,
            missing_information=missing,
        )

    def _identify_critical_facts(self, query: str, doctrines: List[str]) -> List[Dict[str, Any]]:
        """Identify facts that are critical to the analysis."""
        facts: List[Dict[str, Any]] = []
        query_lower = query.lower()

        fact_patterns = {
            "employer_size": {"pattern": r"\b\d+\s*employees?\b", "importance": "HIGH",
                             "reason": "Employer size determines statutory coverage (15 for Title VII, 20 for ADEA, 50 for FMLA)"},
            "tenure": {"pattern": r"\b\d+\s*(?:year|month)s?\b.*(?:employed|worked|tenure)", "importance": "MEDIUM",
                      "reason": "Employment duration affects FMLA eligibility, statute of limitations, and damages calculation"},
            "protected_class": {"pattern": r"\b(?:race|sex|gender|religion|age|disability|national origin|pregnancy)\b",
                               "importance": "HIGH", "reason": "Protected class membership is a prima facie element"},
            "adverse_action": {"pattern": r"\b(?:fired|terminated|demoted|suspended|transferred|reduced|cut)\b",
                              "importance": "HIGH", "reason": "Adverse action is required element for most employment claims"},
            "timing": {"pattern": r"\b(?:after|before|within|during|immediately|shortly)\b",
                      "importance": "MEDIUM", "reason": "Temporal proximity is relevant to causation in retaliation claims"},
        }

        for fact_name, info in fact_patterns.items():
            match = re.search(info["pattern"], query_lower)
            if match:
                facts.append({
                    "fact": fact_name,
                    "value": match.group(),
                    "importance": info["importance"],
                    "reason": info["reason"],
                })

        return facts

    def _identify_assumptions(self, query: str) -> List[str]:
        """Identify assumptions being made in the analysis."""
        assumptions: List[str] = []
        query_lower = query.lower()

        if "employer" not in query_lower and "company" not in query_lower:
            assumptions.append("Assuming an employer-employee relationship exists (not independent contractor)")
        if not re.search(r"\b\d+\s*employees?\b", query_lower):
            assumptions.append("Employer size not specified; assuming statutory coverage thresholds are met")
        if "state" not in query_lower and "texas" not in query_lower:
            assumptions.append("No state specified; analyzing under federal law with general state law principles")
        if "date" not in query_lower and "when" not in query_lower:
            assumptions.append("Timeline not specified; assuming within applicable statute of limitations")
        if "exhausted" not in query_lower and "eeoc" not in query_lower:
            assumptions.append("Administrative exhaustion status unknown; assuming prerequisite requirements can be met")

        return assumptions

    def _identify_missing_info(self, query: str, doctrines: List[str]) -> List[str]:
        """Identify information gaps that could affect analysis."""
        missing: List[str] = []
        query_lower = query.lower()

        if "salary" not in query_lower and "wage" not in query_lower and "pay" not in query_lower:
            if any("flsa" in d for d in doctrines):
                missing.append("Compensation details (salary, hourly rate, job duties) needed for FLSA exemption analysis")
        if "accommodation" in query_lower and "disability" not in query_lower:
            missing.append("Specific disability and functional limitations needed for ADA accommodation analysis")
        if "terminated" in query_lower and "reason" not in query_lower:
            missing.append("Stated reason for termination needed to evaluate pretext")
        if "harassment" in query_lower and "frequency" not in query_lower:
            missing.append("Frequency, severity, and duration of alleged conduct needed for severe-or-pervasive analysis")

        return missing

    def _fragility_band(self, score: float) -> str:
        """Map fragility score to a band."""
        if score >= 0.70:
            return "HIGH_FRAGILITY"
        if score >= 0.45:
            return "MODERATE_FRAGILITY"
        if score >= 0.20:
            return "LOW_FRAGILITY"
        return "STABLE"


# ============================================================================
# DOCTRINE DRIFT WATCHER
# ============================================================================

class DoctrineDriftWatcher:
    """Monitor doctrine cache for staleness, legislative changes, and drift."""

    def __init__(self) -> None:
        """Initialize drift watcher."""
        self._drift_log: List[Dict[str, Any]] = []
        self._staleness_threshold_days: int = 365
        self._last_check: Optional[str] = None

    def check_staleness(self) -> List[Dict[str, Any]]:
        """Check all doctrine blocks for staleness."""
        stale: List[Dict[str, Any]] = []
        now = datetime.now(timezone.utc)

        for key, block in DOCTRINE_CACHE.items():
            last_updated = block.get("last_updated", "")
            if not last_updated:
                stale.append({"topic": block["topic"], "reason": "No last_updated date", "severity": "MEDIUM"})
                continue
            try:
                update_date = datetime.fromisoformat(last_updated + "T00:00:00+00:00")
                age_days = (now - update_date).days
                if age_days > self._staleness_threshold_days:
                    stale.append({
                        "topic": block["topic"],
                        "reason": f"Last updated {age_days} days ago (threshold: {self._staleness_threshold_days})",
                        "severity": "HIGH" if age_days > 730 else "MEDIUM",
                        "age_days": age_days,
                    })
            except ValueError:
                stale.append({"topic": block["topic"], "reason": f"Invalid date format: {last_updated}", "severity": "LOW"})

        self._last_check = now.isoformat()
        return stale

    def check_coverage_gaps(self) -> List[Dict[str, Any]]:
        """Identify areas with insufficient doctrine coverage."""
        expected_categories = {
            "title_vii", "ada", "adea", "fmla", "flsa", "osha",
            "erisa", "nlra", "workers_comp", "termination", "non_compete",
            "warn_act", "whistleblower", "texas_labor",
        }
        covered_categories = set()
        for block in DOCTRINE_CACHE.values():
            covered_categories.add(block.get("category", ""))

        gaps: List[Dict[str, Any]] = []
        for expected in expected_categories:
            if expected not in covered_categories:
                gaps.append({"category": expected, "status": "MISSING", "doctrines_count": 0})
            else:
                count = sum(1 for b in DOCTRINE_CACHE.values() if b.get("category") == expected)
                if count < 2:
                    gaps.append({"category": expected, "status": "THIN", "doctrines_count": count})

        return gaps

    def get_drift_report(self) -> Dict[str, Any]:
        """Get comprehensive drift report."""
        return {
            "staleness_check": self.check_staleness(),
            "coverage_gaps": self.check_coverage_gaps(),
            "total_doctrines": len(DOCTRINE_CACHE),
            "last_check": self._last_check,
            "staleness_threshold_days": self._staleness_threshold_days,
        }


# ============================================================================
# DOCTRINE COVERAGE MAP
# ============================================================================

class DoctrineCoverageMap:
    """Map of doctrine coverage across employment law domains."""

    def generate(self) -> Dict[str, Any]:
        """Generate full coverage map."""
        category_map: Dict[str, List[str]] = defaultdict(list)
        for key, block in DOCTRINE_CACHE.items():
            category = block.get("category", "uncategorized")
            category_map[category].append(block["topic"])

        coverage: Dict[str, Any] = {}
        for category, topics in category_map.items():
            coverage[category] = {
                "topic_count": len(topics),
                "topics": topics,
                "avg_confidence": round(
                    sum(DOCTRINE_CACHE[t].get("confidence", 0.5) for t in topics if t in DOCTRINE_CACHE) / max(len(topics), 1), 4
                ),
            }

        return {
            "total_doctrines": len(DOCTRINE_CACHE),
            "total_categories": len(category_map),
            "coverage": coverage,
            "doctrine_hash": get_doctrine_hash(),
        }


# ============================================================================
# ZONED ANALYSIS
# ============================================================================

class ZonedAnalyzer:
    """Analyze employment law issues within jurisdictional zones."""

    FEDERAL_ZONE: ClassVar[Dict[str, Any]] = {
        "zone": "federal",
        "courts": ["U.S. Supreme Court", "Circuit Courts of Appeals", "District Courts"],
        "agencies": ["EEOC", "DOL", "OSHA", "NLRB", "EBSA"],
        "primary_statutes": ["Title VII", "ADA", "ADEA", "FMLA", "FLSA", "OSHA", "ERISA", "NLRA"],
    }

    TEXAS_ZONE: ClassVar[Dict[str, Any]] = {
        "zone": "texas",
        "courts": ["Texas Supreme Court", "Texas Courts of Appeals", "Texas District Courts"],
        "agencies": ["TWC", "TWC Civil Rights Division"],
        "primary_statutes": ["TCHRA (Ch. 21)", "Texas Payday Law (Ch. 61)", "Ch. 451 Anti-Retaliation",
                            "Ch. 554 Whistleblower", "Bus. & Com. Code 15.50 (Non-Compete)"],
        "key_differences": [
            "Texas is strong at-will state with narrow Sabine Pilot exception",
            "TCHRA mirrors Title VII but interpreted under Texas law",
            "Texas does not recognize implied contract exception to at-will",
            "Non-competes enforceable if ancillary to enforceable agreement (15.50)",
            "No private right of action under Texas Payday Law (TWC admin only)",
            "Workers comp is elective for private employers in Texas",
        ],
    }

    def get_zone_info(self, jurisdiction: str) -> Dict[str, Any]:
        """Get zone information for a jurisdiction."""
        if jurisdiction.lower() == "texas" or jurisdiction.lower() == "tx":
            return self.TEXAS_ZONE
        return self.FEDERAL_ZONE

    def analyze_jurisdictional_issues(self, query: str, jurisdiction: str) -> Dict[str, Any]:
        """Identify jurisdictional issues in the analysis."""
        zone = self.get_zone_info(jurisdiction)
        issues: List[str] = []
        query_lower = query.lower()

        if jurisdiction == "federal":
            if "texas" in query_lower or "tx" in query_lower:
                issues.append("Query mentions Texas; consider state-specific provisions")
            if "state" in query_lower:
                issues.append("State law may provide additional protections beyond federal floor")
        elif jurisdiction == "texas":
            if any(term in query_lower for term in ["fmla", "flsa", "osha", "nlra", "erisa"]):
                issues.append("Federal statute referenced; Texas has limited state analogs for some areas")

        return {
            "zone": zone,
            "jurisdictional_issues": issues,
            "applicable_forums": zone.get("courts", []),
            "applicable_agencies": zone.get("agencies", []),
        }


# ============================================================================
# MULTI-DOCTRINE DECOMPOSITION
# ============================================================================

class MultiDoctrineDecomposer:
    """Decompose complex queries into multiple doctrine analyses."""

    def __init__(self) -> None:
        """Initialize decomposer."""
        self._classifier = EmploymentClaimClassifier()
        self._doctrine_engine = get_doctrine_engine()

    def decompose(self, query: str) -> Dict[str, Any]:
        """Decompose a query into constituent doctrine lookups."""
        claims = self._classifier.classify(query)

        doctrine_lookups: List[Dict[str, Any]] = []
        for claim_type, confidence in claims:
            category = claim_type.value
            doctrines = self._doctrine_engine.search_by_category(category)
            if not doctrines:
                doctrines = self._doctrine_engine.search_by_text(category, max_results=3)

            for doctrine in doctrines[:3]:
                doctrine_lookups.append({
                    "claim_type": claim_type.value,
                    "claim_confidence": confidence,
                    "doctrine_topic": doctrine.topic,
                    "doctrine_title": doctrine.title,
                    "doctrine_confidence": doctrine.confidence,
                })

        return {
            "query": query,
            "claim_types": [(ct.value, conf) for ct, conf in claims],
            "doctrine_lookups": doctrine_lookups,
            "is_multi_doctrine": len(claims) > 1,
            "total_doctrines": len(doctrine_lookups),
        }


# ============================================================================
# DEEP ANALYSIS ENGINE
# ============================================================================

class DeepAnalysisEngine:
    """Multi-source synthesis for complex employment disputes."""

    def __init__(self) -> None:
        """Initialize deep analysis engine."""
        self._doctrine_engine = get_doctrine_engine()
        self._decomposer = MultiDoctrineDecomposer()
        self._risk_engine = RiskAssessmentEngine()
        self._fragility_scorer = FactFragilityScorer()
        self._zoned_analyzer = ZonedAnalyzer()

    def analyze(self, query: str, jurisdiction: str = "federal",
                max_doctrines: int = 5) -> Dict[str, Any]:
        """Perform deep multi-doctrine analysis."""
        start = time.monotonic()

        # Decompose
        decomposition = self._decomposer.decompose(query)
        primary_claim = decomposition["claim_types"][0] if decomposition["claim_types"] else ("general", 0.3)
        claim_type_enum = ClaimType(primary_claim[0]) if primary_claim[0] != "general" else ClaimType.GENERAL

        # Gather doctrines
        doctrines_used: List[DoctrineResponse] = []
        for lookup in decomposition["doctrine_lookups"][:max_doctrines]:
            doctrine = self._doctrine_engine.lookup(lookup["doctrine_topic"])
            if doctrine:
                doctrines_used.append(doctrine)

        # Jurisdictional analysis
        zone_analysis = self._zoned_analyzer.analyze_jurisdictional_issues(query, jurisdiction)

        # Risk assessment
        avg_confidence = sum(d.confidence for d in doctrines_used) / max(len(doctrines_used), 1)
        risk = self._risk_engine.assess(query, claim_type_enum, avg_confidence, jurisdiction)

        # Fact fragility
        fragility = self._fragility_scorer.score(
            query, [d.topic for d in doctrines_used], avg_confidence
        )

        # Build synthesis
        synthesis_parts: List[str] = []
        all_citations: List[str] = []
        all_statutes: List[str] = []
        all_elements: List[str] = []
        all_defenses: List[str] = []
        all_remedies: List[str] = []

        for doctrine in doctrines_used:
            synthesis_parts.append(f"[{doctrine.title}] {doctrine.content}")
            all_citations.extend(doctrine.citations)
            block = self._doctrine_engine.get_doctrine_block(doctrine.topic)
            if block:
                all_statutes.extend(block.get("key_statutes", []))
                all_elements.extend(block.get("elements", []))
                all_defenses.extend(block.get("defenses", []))
                all_remedies.extend(block.get("remedies", []))

        # Deduplicate
        all_citations = list(dict.fromkeys(all_citations))
        all_statutes = list(dict.fromkeys(all_statutes))
        all_elements = list(dict.fromkeys(all_elements))
        all_defenses = list(dict.fromkeys(all_defenses))
        all_remedies = list(dict.fromkeys(all_remedies))

        elapsed = (time.monotonic() - start) * 1000.0

        return {
            "synthesis": "\n\n".join(synthesis_parts),
            "decomposition": decomposition,
            "doctrines_used": [d.to_dict() for d in doctrines_used],
            "zone_analysis": zone_analysis,
            "risk_assessment": risk,
            "fact_fragility": fragility,
            "citations": all_citations,
            "statutes": all_statutes,
            "elements": all_elements,
            "defenses": all_defenses,
            "remedies": all_remedies,
            "confidence": avg_confidence,
            "processing_time_ms": round(elapsed, 3),
        }


# ============================================================================
# EPISTEMIC GUARDRAILS
# ============================================================================

class EpistemicGuardrails:
    """Enforce epistemic integrity on engine outputs."""

    def check(self, text: str) -> Dict[str, Any]:
        """Check text for banned phrases and required disclosures."""
        violations: List[str] = []
        text_lower = text.lower()

        for phrase in BANNED_PHRASES:
            if phrase.lower() in text_lower:
                violations.append(f"Banned phrase detected: '{phrase}'")

        return {
            "passed": len(violations) == 0,
            "violations": violations,
            "checked_phrases": len(BANNED_PHRASES),
        }

    def get_disclosures(self, jurisdiction: str = "federal",
                         analysis_date: Optional[str] = None) -> List[str]:
        """Generate required disclosures for the analysis."""
        if analysis_date is None:
            analysis_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        disclosures: List[str] = []
        for key, template in DISCLOSURE_TEMPLATES.items():
            disclosure = template.format(
                jurisdiction=jurisdiction,
                analysis_date=analysis_date,
            )
            disclosures.append(disclosure)
        return disclosures


# ============================================================================
# DETERMINISM HASHER
# ============================================================================

class DeterminismHasher:
    """Compute SHA-256 determinism hashes for reproducible analysis."""

    def hash_response(self, query: str, answer: str, citations: List[str],
                       confidence: float, doctrines_used: List[str]) -> str:
        """Compute determinism hash for a complete response."""
        hash_input = json.dumps({
            "query": query.strip().lower(),
            "answer": answer.strip(),
            "citations": sorted(citations),
            "confidence": round(confidence, 4),
            "doctrines": sorted(doctrines_used),
            "engine": ENGINE_ID,
            "version": ENGINE_VERSION,
        }, sort_keys=True)
        return hashlib.sha256(hash_input.encode("utf-8")).hexdigest()

    def hash_query(self, query: str) -> str:
        """Compute hash of just the query for caching."""
        return hashlib.sha256(query.strip().lower().encode("utf-8")).hexdigest()[:16]


# ============================================================================
# THREE-LAYER RESPONSE PROCESSOR
# ============================================================================

class ThreeLayerProcessor:
    """Core three-layer response processing pipeline."""

    def __init__(self) -> None:
        """Initialize processor with all sub-engines."""
        self._doctrine_engine = get_doctrine_engine()
        self._search_index = get_search_index()
        self._hybrid_engine = get_hybrid_engine()
        self._deep_engine = DeepAnalysisEngine()
        self._risk_engine = RiskAssessmentEngine()
        self._fragility_scorer = FactFragilityScorer()
        self._confidence_stratifier = ConfidenceStratifier()
        self._authority_hardener = AuthorityHardener()
        self._guardrails = EpistemicGuardrails()
        self._hasher = DeterminismHasher()
        self._zoned_analyzer = ZonedAnalyzer()
        self._classifier = EmploymentClaimClassifier()
        self._index_initialized = False

    def _ensure_index(self) -> None:
        """Ensure the search index is populated from doctrine cache."""
        if self._index_initialized:
            return
        for key, block in DOCTRINE_CACHE.items():
            content = block.get("summary", "")
            if block.get("elements"):
                content += " " + " ".join(block["elements"])
            if block.get("defenses"):
                content += " " + " ".join(block["defenses"])
            self._search_index.add_document(
                doc_id=key,
                topic=block["topic"],
                content=content,
                category=block.get("category", ""),
                authority="; ".join(block.get("key_statutes", [])),
                confidence=block.get("confidence", 0.5),
                tags=block.get("tags", []),
                last_updated=block.get("last_updated", ""),
            )
        self._search_index.build()
        self._index_initialized = True
        logger.info("Search index populated with {} doctrine blocks", len(DOCTRINE_CACHE))

    def process(self, request: AnalysisRequest) -> AnalysisResponse:
        """Process a request through the three-layer pipeline."""
        self._ensure_index()
        telemetry = get_telemetry()
        trace = telemetry.trace_query(request.query, request.mode.value)

        try:
            # Step 1: Semantic normalization
            step_norm = trace.begin_step("semantic_normalization")
            norm_result = normalize_query(request.query)
            step_norm.complete({"terms": len(norm_result.canonical_terms), "categories": norm_result.detected_categories})

            # Step 2: Claim classification
            step_classify = trace.begin_step("claim_classification")
            claim_type, claim_conf = self._classifier.get_primary_claim(request.query)
            step_classify.complete({"claim_type": claim_type.value, "confidence": claim_conf})

            # Step 3: Jurisdiction detection
            jurisdiction = norm_result.jurisdiction if norm_result.jurisdiction != "federal" else request.jurisdiction

            # LAYER 1: Doctrine Cache
            step_layer1 = trace.begin_step("layer1_doctrine_cache")
            doctrine_response = self._try_doctrine_cache(norm_result, claim_type)
            if doctrine_response:
                step_layer1.complete({"hit": True, "topic": doctrine_response.topic})
                trace.response_layer = ResponseLayer.DOCTRINE_CACHE
                trace.cached = True
                trace.doctrine_hits = 1
                trace.doctrines_used = [doctrine_response.topic]
            else:
                step_layer1.complete({"hit": False})

            # LAYER 2: Semantic Search (on cache miss or REVIEW/MEMO mode)
            search_results: List[SearchResult] = []
            if not doctrine_response or request.mode != ResponseMode.FAST:
                step_layer2 = trace.begin_step("layer2_semantic_search")
                search_results = self._search_index.search(
                    request.query, max_results=request.max_doctrines,
                    boost_categories=norm_result.detected_categories,
                )
                step_layer2.complete({"results": len(search_results)})
                trace.search_results = len(search_results)
                if not doctrine_response and search_results:
                    trace.response_layer = ResponseLayer.SEMANTIC_SEARCH

            # LAYER 3: Deep Analysis (for MEMO mode or complex queries)
            deep_result: Optional[Dict[str, Any]] = None
            if request.mode == ResponseMode.MEMO or (not doctrine_response and not search_results):
                step_layer3 = trace.begin_step("layer3_deep_analysis")
                deep_result = self._deep_engine.analyze(
                    request.query, jurisdiction=jurisdiction,
                    max_doctrines=request.max_doctrines,
                )
                step_layer3.complete({"doctrines": deep_result.get("total_doctrines_used", 0) if deep_result else 0})
                trace.response_layer = ResponseLayer.DEEP_ANALYSIS

            # Build response
            step_build = trace.begin_step("build_response")
            response = self._build_response(
                request=request,
                trace=trace,
                norm_result=norm_result,
                claim_type=claim_type,
                claim_conf=claim_conf,
                jurisdiction=jurisdiction,
                doctrine_response=doctrine_response,
                search_results=search_results,
                deep_result=deep_result,
            )
            step_build.complete()

            # Finalize trace
            trace.confidence = response.confidence
            trace.employment_domain = claim_type.value
            trace.determinism_hash = response.determinism_hash
            trace.jurisdiction = jurisdiction
            trace.statutes_referenced = response.statutes

            telemetry.complete_trace(trace)
            telemetry.performance.record_endpoint(f"/analyze/{request.mode.value}", trace.total_duration_ms)

            return response

        except Exception as e:
            trace.error = str(e)
            telemetry.complete_trace(trace)
            telemetry.log_error(
                ErrorDomain.SYSTEM, str(e), severity="HIGH",
                stack_trace=traceback.format_exc(),
                query_context=request.query[:500],
            )
            raise

    def _try_doctrine_cache(self, norm: NormalizationResult,
                            claim_type: ClaimType) -> Optional[DoctrineResponse]:
        """Attempt direct doctrine cache lookup."""
        # Try canonical terms first
        for term in norm.canonical_terms:
            response = self._doctrine_engine.lookup(term)
            if response:
                return response

        # Try category-based lookup
        for category in norm.detected_categories:
            results = self._doctrine_engine.search_by_category(category)
            if results:
                return results[0]

        # Try claim type
        results = self._doctrine_engine.search_by_category(claim_type.value)
        if results:
            return results[0]

        return None

    def _build_response(self, request: AnalysisRequest, trace: QueryTrace,
                         norm_result: NormalizationResult, claim_type: ClaimType,
                         claim_conf: float, jurisdiction: str,
                         doctrine_response: Optional[DoctrineResponse],
                         search_results: List[SearchResult],
                         deep_result: Optional[Dict[str, Any]]) -> AnalysisResponse:
        """Build the final analysis response."""

        # Aggregate content
        answer_parts: List[str] = []
        summary_parts: List[str] = []
        all_citations: List[str] = []
        all_statutes: List[str] = []
        all_elements: List[str] = []
        all_defenses: List[str] = []
        all_remedies: List[str] = []
        doctrines_used: List[str] = []
        confidence = 0.5

        # From doctrine cache
        if doctrine_response:
            answer_parts.append(doctrine_response.content)
            summary_parts.append(f"[{doctrine_response.title}] {doctrine_response.content[:200]}")
            all_citations.extend(doctrine_response.citations)
            doctrines_used.append(doctrine_response.topic)
            confidence = doctrine_response.confidence
            block = self._doctrine_engine.get_doctrine_block(doctrine_response.topic)
            if block:
                all_statutes.extend(block.get("key_statutes", []))
                all_elements.extend(block.get("elements", []))
                all_defenses.extend(block.get("defenses", []))
                all_remedies.extend(block.get("remedies", []))

        # From search results
        for sr in search_results[:3]:
            if sr.topic not in doctrines_used:
                answer_parts.append(sr.content[:300])
                doctrines_used.append(sr.topic)
                doc = self._search_index.get_document(sr.doc_id)
                if doc:
                    block = DOCTRINE_CACHE.get(sr.doc_id)
                    if block:
                        all_citations.extend(block.get("leading_cases", []))
                        all_statutes.extend(block.get("key_statutes", []))

        # From deep analysis
        if deep_result:
            if deep_result.get("synthesis"):
                answer_parts.append(deep_result["synthesis"])
            all_citations.extend(deep_result.get("citations", []))
            all_statutes.extend(deep_result.get("statutes", []))
            all_elements.extend(deep_result.get("elements", []))
            all_defenses.extend(deep_result.get("defenses", []))
            all_remedies.extend(deep_result.get("remedies", []))
            for d in deep_result.get("doctrines_used", []):
                topic = d.get("topic", "")
                if topic and topic not in doctrines_used:
                    doctrines_used.append(topic)
            confidence = deep_result.get("confidence", confidence)

        # Deduplicate
        all_citations = list(dict.fromkeys(all_citations))
        all_statutes = list(dict.fromkeys(all_statutes))
        all_elements = list(dict.fromkeys(all_elements))
        all_defenses = list(dict.fromkeys(all_defenses))
        all_remedies = list(dict.fromkeys(all_remedies))

        # Confidence adjustment
        confidence = self._confidence_stratifier.adjust_for_jurisdiction(confidence, jurisdiction)
        confidence_info = self._confidence_stratifier.stratify(confidence)

        # Build answer text
        answer = "\n\n".join(answer_parts) if answer_parts else "No relevant doctrine found for this query."
        summary = " | ".join(summary_parts) if summary_parts else "No analysis available."

        # Risk assessment
        risk_assessment: Optional[RiskAssessment] = None
        if request.include_risk_score:
            risk_assessment = self._risk_engine.assess(
                request.query, claim_type, confidence, jurisdiction
            )

        # Fact fragility
        fact_fragility: Optional[FactFragilityScore] = None
        if request.mode != ResponseMode.FAST:
            fact_fragility = self._fragility_scorer.score(
                request.query, doctrines_used, confidence
            )

        # Determinism hash
        det_hash = self._hasher.hash_response(
            request.query, answer, all_citations, confidence, doctrines_used
        )

        # Epistemic guardrails
        guardrail_check = self._guardrails.check(answer)
        disclosures = self._guardrails.get_disclosures(jurisdiction)

        # Filter by request flags
        if not request.include_citations:
            all_citations = []
        if not request.include_elements:
            all_elements = []
        if not request.include_defenses:
            all_defenses = []
        if not request.include_remedies:
            all_remedies = []

        return AnalysisResponse(
            trace_id=trace.trace_id,
            query=request.query,
            mode=request.mode.value,
            jurisdiction=jurisdiction,
            response_layer=trace.response_layer.value,
            answer=answer,
            summary=summary[:500],
            claim_type=claim_type.value,
            claim_confidence=round(claim_conf, 4),
            confidence=round(confidence, 4),
            confidence_band=confidence_info["band"],
            determinism_hash=det_hash[:32],
            citations=all_citations,
            statutes=all_statutes,
            elements=all_elements,
            defenses=all_defenses,
            remedies=all_remedies,
            risk_assessment=risk_assessment,
            fact_fragility=fact_fragility,
            doctrines_used=doctrines_used,
            search_results_count=len(search_results),
            processing_time_ms=round((time.monotonic() - trace.start_time) * 1000.0, 3),
            disclosures=disclosures,
            epistemic_guardrails=guardrail_check,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler for startup/shutdown."""
    # Startup
    logger.info("LG07 Employment Law Engine starting on port {}", ENGINE_PORT)

    # Initialize telemetry
    telemetry = get_telemetry(TELEMETRY_DIR)
    logger.info("Telemetry initialized at {}", TELEMETRY_DIR)

    # Initialize doctrine engine
    doctrine_engine = get_doctrine_engine()
    logger.info("Doctrine engine loaded: {} doctrines", len(DOCTRINE_CACHE))

    # Initialize search index
    search_idx = get_search_index()
    for key, block in DOCTRINE_CACHE.items():
        content = block.get("summary", "")
        if block.get("elements"):
            content += " " + " ".join(block["elements"])
        search_idx.add_document(
            doc_id=key,
            topic=block["topic"],
            content=content,
            category=block.get("category", ""),
            authority="; ".join(block.get("key_statutes", [])),
            confidence=block.get("confidence", 0.5),
            tags=block.get("tags", []),
            last_updated=block.get("last_updated", ""),
        )
    search_idx.build()
    logger.info("Search index built: {} documents", search_idx.get_index_stats()["total_documents"])

    # Create directories
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)

    logger.info("LG07 Employment Law Engine READY on port {}", ENGINE_PORT)

    yield

    # Shutdown
    logger.info("LG07 Employment Law Engine shutting down")
    telemetry.snapshot_performance()
    logger.info("Final performance snapshot recorded")


app = FastAPI(
    title="LG07 Employment Law Engine",
    description="Production-grade employment law analysis engine with TIE-20 architecture",
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


# ============================================================================
# DEPENDENCY INJECTION
# ============================================================================

def get_processor() -> ThreeLayerProcessor:
    """Get the three-layer processor singleton."""
    if not hasattr(get_processor, "_instance"):
        get_processor._instance = ThreeLayerProcessor()
    return get_processor._instance


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/health")
async def health_check() -> HealthResponse:
    """Health endpoint - TIE-20 component #12."""
    telemetry = get_telemetry()
    metrics = telemetry.metrics
    latency = metrics.get_latency_stats()

    return HealthResponse(
        status="healthy",
        engine_id=ENGINE_ID,
        engine_name=ENGINE_NAME,
        engine_version=ENGINE_VERSION,
        port=ENGINE_PORT,
        tier=ENGINE_TIER,
        mode=ENGINE_MODE,
        uptime_seconds=metrics.get_uptime_seconds(),
        doctrine_count=get_doctrine_count(),
        doctrine_hash=get_doctrine_hash(),
        semantic_map_hash=get_semantic_map_hash(),
        total_queries=metrics.total_queries,
        error_rate=metrics.get_error_rate(),
        cache_hit_rate=metrics.get_cache_hit_rate(),
        latency_p50=latency["p50"],
        latency_p99=latency["p99"],
        telemetry_chain_state=telemetry.audit.get_chain_state(),
    )


@app.post("/analyze")
async def analyze(request: AnalysisRequest,
                  processor: ThreeLayerProcessor = Depends(get_processor)) -> AnalysisResponse:
    """Main analysis endpoint - three-layer response processing."""
    try:
        return processor.process(request)
    except Exception as e:
        logger.error("Analysis failed: {}", str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze/batch")
async def analyze_batch(request: BatchRequest,
                        processor: ThreeLayerProcessor = Depends(get_processor)) -> Dict[str, Any]:
    """Batch analysis endpoint."""
    results: List[Dict[str, Any]] = []
    errors: List[Dict[str, str]] = []

    for idx, query in enumerate(request.queries):
        try:
            single_request = AnalysisRequest(
                query=query, mode=request.mode, jurisdiction=request.jurisdiction
            )
            response = processor.process(single_request)
            results.append(response.model_dump())
        except Exception as e:
            errors.append({"index": str(idx), "query": query[:100], "error": str(e)})

    return {
        "results": results,
        "errors": errors,
        "total": len(request.queries),
        "successful": len(results),
        "failed": len(errors),
    }


@app.post("/search")
async def search_endpoint(request: SearchRequest) -> Dict[str, Any]:
    """Hybrid search across doctrines, statutes, and cases."""
    engine = get_hybrid_engine()
    return engine.search(
        request.query,
        max_results=request.max_results,
        include_statutes=request.include_statutes,
        include_cases=request.include_cases,
        category_filter=request.category_filter,
    )


@app.get("/doctrine/{topic}")
async def get_doctrine(topic: str) -> Dict[str, Any]:
    """Look up a specific doctrine by topic."""
    engine = get_doctrine_engine()
    response = engine.lookup(topic)
    if not response:
        raise HTTPException(status_code=404, detail=f"Doctrine '{topic}' not found")
    return response.to_dict()


@app.get("/doctrines")
async def list_doctrines(category: Optional[str] = None) -> Dict[str, Any]:
    """List all doctrines, optionally filtered by category."""
    engine = get_doctrine_engine()
    if category:
        doctrines = engine.search_by_category(category)
        return {
            "category": category,
            "count": len(doctrines),
            "doctrines": [d.to_dict() for d in doctrines],
        }
    return {
        "total": get_doctrine_count(),
        "categories": engine.get_category_counts(),
        "topics": engine.get_all_topics(),
    }


@app.get("/doctrines/coverage")
async def doctrine_coverage() -> Dict[str, Any]:
    """Get doctrine coverage map."""
    coverage_map = DoctrineCoverageMap()
    return coverage_map.generate()


@app.get("/doctrines/drift")
async def doctrine_drift() -> Dict[str, Any]:
    """Check doctrine drift and staleness."""
    watcher = DoctrineDriftWatcher()
    return watcher.get_drift_report()


@app.post("/normalize")
async def normalize_endpoint(query: str = Query(..., min_length=2)) -> Dict[str, Any]:
    """Normalize employment law query through semantic pipeline."""
    result = normalize_query(query)
    return result.to_dict()


@app.get("/semantic/stats")
async def semantic_stats() -> Dict[str, Any]:
    """Get semantic dictionary statistics."""
    from semantic import _get_normalizer
    normalizer = _get_normalizer()
    return normalizer.get_map_stats()


@app.get("/semantic/governance")
async def semantic_governance() -> Dict[str, Any]:
    """Get semantic dictionary governance metadata."""
    return get_semantic_governance()


@app.get("/semantic/integrity")
async def semantic_integrity() -> Dict[str, Any]:
    """Verify semantic dictionary integrity."""
    return verify_dictionary_integrity()


@app.get("/statutes")
async def list_statutes() -> Dict[str, Any]:
    """List all indexed federal employment statutes."""
    engine = StatuteSearchEngine()
    return {"statutes": engine.STATUTE_INDEX, "count": len(engine.STATUTE_INDEX)}


@app.get("/cases")
async def list_cases() -> Dict[str, Any]:
    """List all indexed landmark employment cases."""
    engine = CaseSearchEngine()
    return {"cases": engine.LANDMARK_CASES, "count": len(engine.LANDMARK_CASES)}


@app.get("/agencies")
async def list_agencies() -> Dict[str, Any]:
    """List all employment law agency acronyms."""
    return {"agencies": get_agency_map(), "count": len(get_agency_map())}


@app.get("/risk/categories")
async def risk_categories() -> Dict[str, Any]:
    """Get risk assessment category definitions."""
    return {"categories": RiskAssessmentEngine.RISK_CATEGORIES}


@app.get("/zones/{jurisdiction}")
async def get_zone(jurisdiction: str) -> Dict[str, Any]:
    """Get jurisdictional zone information."""
    analyzer = ZonedAnalyzer()
    return analyzer.get_zone_info(jurisdiction)


@app.get("/metrics")
async def get_metrics() -> Dict[str, Any]:
    """Get engine metrics - TIE-20 component #11."""
    telemetry = get_telemetry()
    return telemetry.metrics.to_dict()


@app.get("/metrics/performance")
async def get_performance_metrics() -> Dict[str, Any]:
    """Get endpoint performance metrics."""
    telemetry = get_telemetry()
    return telemetry.performance.get_all_stats()


@app.get("/metrics/aggregated")
async def get_aggregated_metrics() -> Dict[str, Any]:
    """Get rolling window aggregated metrics."""
    telemetry = get_telemetry()
    return telemetry.aggregator.get_summary()


@app.get("/metrics/errors")
async def get_error_metrics() -> Dict[str, Any]:
    """Get error tracking metrics."""
    telemetry = get_telemetry()
    return telemetry.errors.get_stats()


@app.get("/metrics/errors/recent")
async def get_recent_errors(limit: int = Query(default=20, ge=1, le=100)) -> Dict[str, Any]:
    """Get recent errors."""
    telemetry = get_telemetry()
    return {"errors": telemetry.errors.get_recent(limit), "count": limit}


@app.get("/metrics/mutations")
async def get_mutations(limit: int = Query(default=20, ge=1, le=100)) -> Dict[str, Any]:
    """Get recent doctrine mutations."""
    telemetry = get_telemetry()
    return {"mutations": telemetry.mutations.get_recent(limit)}


@app.get("/metrics/slow-queries")
async def get_slow_queries(limit: int = Query(default=50, ge=1, le=200)) -> Dict[str, Any]:
    """Get recent slow queries."""
    telemetry = get_telemetry()
    return {"slow_queries": telemetry.performance.get_slow_queries(limit)}


@app.get("/audit/chain")
async def get_audit_chain() -> Dict[str, Any]:
    """Get audit trail chain state."""
    telemetry = get_telemetry()
    return telemetry.audit.get_chain_state()


@app.get("/audit/verify/{log_file}")
async def verify_audit_chain(log_file: str) -> Dict[str, Any]:
    """Verify integrity of an audit log file."""
    telemetry = get_telemetry()
    return telemetry.audit.verify_chain(log_file)


@app.get("/search/index/stats")
async def search_index_stats() -> Dict[str, Any]:
    """Get search index statistics."""
    idx = get_search_index()
    return idx.get_index_stats()


@app.get("/search/hybrid/stats")
async def hybrid_search_stats() -> Dict[str, Any]:
    """Get hybrid search engine statistics."""
    engine = get_hybrid_engine()
    return engine.get_stats()


@app.get("/config")
async def get_config() -> Dict[str, Any]:
    """Get engine configuration."""
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"error": "Configuration file not found"}


@app.get("/guardrails")
async def get_guardrails() -> Dict[str, Any]:
    """Get epistemic guardrail configuration."""
    return {
        "banned_phrases": BANNED_PHRASES,
        "disclosure_templates": DISCLOSURE_TEMPLATES,
        "banned_count": len(BANNED_PHRASES),
        "disclosure_count": len(DISCLOSURE_TEMPLATES),
    }


@app.post("/metrics/reset")
async def reset_metrics() -> Dict[str, str]:
    """Reset all metrics counters."""
    telemetry = get_telemetry()
    telemetry.metrics.reset()
    return {"status": "Metrics reset successfully"}


@app.post("/metrics/snapshot")
async def take_snapshot() -> Dict[str, str]:
    """Take a performance snapshot."""
    telemetry = get_telemetry()
    telemetry.snapshot_performance()
    return {"status": "Performance snapshot recorded"}


@app.post("/classify")
async def classify_claim(query: str = Query(..., min_length=2)) -> Dict[str, Any]:
    """Classify an employment law query into claim types."""
    classifier = EmploymentClaimClassifier()
    results = classifier.classify(query)
    norm = normalize_query(query)
    return {
        "query": query,
        "claim_types": [{"type": ct.value, "confidence": conf} for ct, conf in results],
        "primary_claim": results[0][0].value if results else "general",
        "primary_confidence": results[0][1] if results else 0.3,
        "detected_categories": norm.detected_categories,
        "detected_statutes": norm.detected_statutes,
        "jurisdiction": norm.jurisdiction,
    }


@app.post("/risk")
async def assess_risk(request: AnalysisRequest) -> Dict[str, Any]:
    """Standalone risk assessment endpoint."""
    classifier = EmploymentClaimClassifier()
    claim_type, claim_conf = classifier.get_primary_claim(request.query)
    risk_engine = RiskAssessmentEngine()
    risk = risk_engine.assess(request.query, claim_type, claim_conf, request.jurisdiction)
    return {
        "query": request.query,
        "claim_type": claim_type.value,
        "claim_confidence": round(claim_conf, 4),
        "risk_assessment": risk.model_dump(),
    }


@app.post("/fragility")
async def assess_fragility(request: AnalysisRequest) -> Dict[str, Any]:
    """Standalone fact fragility assessment endpoint."""
    classifier = EmploymentClaimClassifier()
    claim_type, claim_conf = classifier.get_primary_claim(request.query)
    doctrine_engine = get_doctrine_engine()
    results = doctrine_engine.search_by_text(request.query, max_results=3)
    doctrines_used = [r.topic for r in results]
    scorer = FactFragilityScorer()
    fragility = scorer.score(request.query, doctrines_used, claim_conf)
    return {
        "query": request.query,
        "claim_type": claim_type.value,
        "doctrines_analyzed": doctrines_used,
        "fragility": fragility.model_dump(),
    }


@app.post("/decompose")
async def decompose_query(query: str = Query(..., min_length=2)) -> Dict[str, Any]:
    """Decompose a complex query into constituent doctrine lookups."""
    decomposer = MultiDoctrineDecomposer()
    return decomposer.decompose(query)


@app.post("/deep-analyze")
async def deep_analyze(request: AnalysisRequest) -> Dict[str, Any]:
    """Deep multi-doctrine analysis endpoint."""
    engine = DeepAnalysisEngine()
    result = engine.analyze(
        request.query, jurisdiction=request.jurisdiction,
        max_doctrines=request.max_doctrines,
    )
    # Convert Pydantic models to dicts for JSON serialization
    if hasattr(result.get("risk_assessment"), "model_dump"):
        result["risk_assessment"] = result["risk_assessment"].model_dump()
    if hasattr(result.get("fact_fragility"), "model_dump"):
        result["fact_fragility"] = result["fact_fragility"].model_dump()
    return result


@app.get("/zones/{jurisdiction}/issues")
async def get_jurisdictional_issues(jurisdiction: str,
                                     query: str = Query(..., min_length=2)) -> Dict[str, Any]:
    """Analyze jurisdictional issues for a query in a specific zone."""
    analyzer = ZonedAnalyzer()
    return analyzer.analyze_jurisdictional_issues(query, jurisdiction)


@app.get("/doctrine/{topic}/elements")
async def get_doctrine_elements(topic: str) -> Dict[str, Any]:
    """Get legal elements for a specific doctrine topic."""
    engine = get_doctrine_engine()
    elements = engine.get_elements_for_topic(topic)
    if not elements:
        raise HTTPException(status_code=404, detail=f"No elements found for topic '{topic}'")
    return {"topic": topic, "elements": elements, "count": len(elements)}


@app.get("/doctrine/{topic}/defenses")
async def get_doctrine_defenses(topic: str) -> Dict[str, Any]:
    """Get available defenses for a specific doctrine topic."""
    engine = get_doctrine_engine()
    defenses = engine.get_defenses_for_topic(topic)
    if not defenses:
        raise HTTPException(status_code=404, detail=f"No defenses found for topic '{topic}'")
    return {"topic": topic, "defenses": defenses, "count": len(defenses)}


@app.get("/doctrine/{topic}/remedies")
async def get_doctrine_remedies(topic: str) -> Dict[str, Any]:
    """Get available remedies for a specific doctrine topic."""
    engine = get_doctrine_engine()
    remedies = engine.get_remedies_for_topic(topic)
    if not remedies:
        raise HTTPException(status_code=404, detail=f"No remedies found for topic '{topic}'")
    return {"topic": topic, "remedies": remedies, "count": len(remedies)}


@app.get("/doctrine/{topic}/cases")
async def get_doctrine_cases(topic: str) -> Dict[str, Any]:
    """Get leading cases for a specific doctrine topic."""
    engine = get_doctrine_engine()
    cases = engine.get_cases_for_topic(topic)
    if not cases:
        raise HTTPException(status_code=404, detail=f"No cases found for topic '{topic}'")
    return {"topic": topic, "leading_cases": cases, "count": len(cases)}


@app.get("/doctrine/{topic}/statutes")
async def get_doctrine_statutes(topic: str) -> Dict[str, Any]:
    """Get key statutes for a specific doctrine topic."""
    engine = get_doctrine_engine()
    statutes = engine.get_statutes_for_topic(topic)
    if not statutes:
        raise HTTPException(status_code=404, detail=f"No statutes found for topic '{topic}'")
    return {"topic": topic, "key_statutes": statutes, "count": len(statutes)}


@app.get("/citations/validate")
async def validate_citation(citation: str = Query(..., min_length=3)) -> Dict[str, Any]:
    """Validate a legal citation format and rank its authority."""
    hardener = AuthorityHardener()
    return hardener.validate_citation(citation)


@app.post("/citations/rank")
async def rank_citations(citations: List[str]) -> Dict[str, Any]:
    """Rank a list of citations by authority hierarchy."""
    hardener = AuthorityHardener()
    validated = [hardener.validate_citation(c) for c in citations]
    validated.sort(key=lambda x: x.get("weight", 0), reverse=True)
    authority_score = hardener.compute_authority_score(citations)
    return {
        "citations": validated,
        "aggregate_authority_score": authority_score,
        "count": len(citations),
    }


@app.get("/confidence/stratify")
async def stratify_confidence(score: float = Query(..., ge=0.0, le=1.0)) -> Dict[str, Any]:
    """Stratify a confidence score into a band with explanation."""
    stratifier = ConfidenceStratifier()
    return stratifier.stratify(score)


# ============================================================================
# COMPLIANCE CHECKLIST GENERATOR
# ============================================================================

class ComplianceChecklistGenerator:
    """Generate employment law compliance checklists based on query context."""

    CHECKLISTS: ClassVar[Dict[str, List[Dict[str, str]]]] = {
        "termination": [
            {"item": "Review employee file for documentation of performance issues", "priority": "HIGH"},
            {"item": "Ensure progressive discipline policy was followed (if applicable)", "priority": "HIGH"},
            {"item": "Check for recent protected activity (complaints, FMLA, workers comp)", "priority": "CRITICAL"},
            {"item": "Confirm no discriminatory pattern among recent terminations", "priority": "HIGH"},
            {"item": "Calculate final pay timeline (state law requirements)", "priority": "MEDIUM"},
            {"item": "Prepare separation/severance agreement if applicable", "priority": "MEDIUM"},
            {"item": "OWBPA compliance if employee is 40+ and releasing ADEA claims", "priority": "HIGH"},
            {"item": "COBRA notification requirements", "priority": "MEDIUM"},
            {"item": "Return of company property and access revocation", "priority": "LOW"},
            {"item": "Document legitimate business reason contemporaneously", "priority": "HIGH"},
            {"item": "Check non-compete/non-solicitation agreements", "priority": "MEDIUM"},
            {"item": "WARN Act analysis if part of larger layoff", "priority": "CRITICAL"},
        ],
        "hiring": [
            {"item": "Review job posting for discriminatory language", "priority": "HIGH"},
            {"item": "Ensure consistent interview questions for all candidates", "priority": "HIGH"},
            {"item": "Document selection criteria before reviewing applications", "priority": "MEDIUM"},
            {"item": "FCRA-compliant background check authorization and disclosure", "priority": "HIGH"},
            {"item": "Ban-the-box compliance (if applicable jurisdiction)", "priority": "MEDIUM"},
            {"item": "Pay transparency compliance (salary range in posting)", "priority": "MEDIUM"},
            {"item": "Salary history inquiry prohibition (if applicable)", "priority": "MEDIUM"},
            {"item": "ADA - do not ask disability-related questions pre-offer", "priority": "HIGH"},
            {"item": "I-9 completion within 3 business days of start", "priority": "CRITICAL"},
            {"item": "E-Verify (if required by state or federal contract)", "priority": "MEDIUM"},
            {"item": "Worker classification (employee vs. contractor)", "priority": "HIGH"},
        ],
        "accommodation": [
            {"item": "Acknowledge accommodation request in writing", "priority": "HIGH"},
            {"item": "Initiate interactive process promptly", "priority": "CRITICAL"},
            {"item": "Request medical documentation (if disability not obvious)", "priority": "MEDIUM"},
            {"item": "Identify essential functions of the position", "priority": "HIGH"},
            {"item": "Brainstorm potential accommodations with employee", "priority": "HIGH"},
            {"item": "Document each step of the interactive process", "priority": "CRITICAL"},
            {"item": "Evaluate undue hardship factors if denying", "priority": "HIGH"},
            {"item": "Consider reassignment to vacant position as last resort", "priority": "MEDIUM"},
            {"item": "Provide accommodation in writing with timeline", "priority": "MEDIUM"},
            {"item": "Follow up to ensure accommodation is effective", "priority": "MEDIUM"},
        ],
        "investigation": [
            {"item": "Assign trained, neutral investigator", "priority": "CRITICAL"},
            {"item": "Interim protective measures (separation of parties)", "priority": "HIGH"},
            {"item": "Interview complainant first (detailed, open-ended questions)", "priority": "HIGH"},
            {"item": "Interview accused (provide fair opportunity to respond)", "priority": "HIGH"},
            {"item": "Interview witnesses identified by both parties", "priority": "HIGH"},
            {"item": "Collect and preserve documentary evidence", "priority": "HIGH"},
            {"item": "Assess credibility using consistent factors", "priority": "MEDIUM"},
            {"item": "Make factual findings based on preponderance standard", "priority": "HIGH"},
            {"item": "Determine appropriate corrective action", "priority": "HIGH"},
            {"item": "Communicate outcome to complainant and accused", "priority": "MEDIUM"},
            {"item": "Document entire investigation in confidential file", "priority": "CRITICAL"},
            {"item": "Monitor for retaliation after investigation", "priority": "HIGH"},
            {"item": "Anti-retaliation notice to all parties", "priority": "MEDIUM"},
        ],
    }

    def generate(self, context: str) -> Dict[str, Any]:
        """Generate a compliance checklist based on context."""
        context_lower = context.lower()
        matched_checklists: Dict[str, Any] = {}

        for checklist_name, items in self.CHECKLISTS.items():
            if checklist_name in context_lower:
                matched_checklists[checklist_name] = items
            elif checklist_name == "termination" and any(
                t in context_lower for t in ["fired", "terminated", "let go", "discharge"]
            ):
                matched_checklists[checklist_name] = items
            elif checklist_name == "accommodation" and any(
                t in context_lower for t in ["accommodation", "ada", "disability", "modified"]
            ):
                matched_checklists[checklist_name] = items
            elif checklist_name == "investigation" and any(
                t in context_lower for t in ["investigation", "complaint", "harassment", "misconduct"]
            ):
                matched_checklists[checklist_name] = items
            elif checklist_name == "hiring" and any(
                t in context_lower for t in ["hiring", "recruit", "interview", "applicant", "candidate"]
            ):
                matched_checklists[checklist_name] = items

        if not matched_checklists:
            matched_checklists["termination"] = self.CHECKLISTS["termination"]

        return {
            "context": context,
            "checklists": matched_checklists,
            "total_items": sum(len(items) for items in matched_checklists.values()),
        }


@app.post("/checklist")
async def generate_checklist(query: str = Query(..., min_length=2)) -> Dict[str, Any]:
    """Generate employment law compliance checklist based on query context."""
    generator = ComplianceChecklistGenerator()
    return generator.generate(query)


# ============================================================================
# STATUTE OF LIMITATIONS CALCULATOR
# ============================================================================

class StatuteOfLimitationsCalculator:
    """Calculate applicable statutes of limitations for employment claims."""

    LIMITATIONS: ClassVar[Dict[str, Dict[str, Any]]] = {
        "title_vii": {
            "admin_filing": "180 days (300 with state agency deferral) from discriminatory act",
            "lawsuit": "90 days from receipt of EEOC right-to-sue letter",
            "notes": "Continuing violation doctrine may extend for hostile environment claims",
        },
        "ada": {
            "admin_filing": "180 days (300 with state agency deferral) from discriminatory act",
            "lawsuit": "90 days from receipt of EEOC right-to-sue letter",
            "notes": "Same as Title VII; failure to accommodate may be continuing violation",
        },
        "adea": {
            "admin_filing": "180 days (300 with state agency deferral) from discriminatory act",
            "lawsuit": "60 days after filing EEOC charge (no right-to-sue letter required)",
            "notes": "OWBPA 21/45-day consideration period for waivers; 7-day revocation",
        },
        "fmla": {
            "admin_filing": "No administrative prerequisite",
            "lawsuit": "2 years from violation (3 years for willful)",
            "notes": "Each denial of FMLA rights is a separate violation",
        },
        "flsa": {
            "admin_filing": "No administrative prerequisite for private suits",
            "lawsuit": "2 years from violation (3 years for willful)",
            "notes": "Each paycheck can be a separate violation; Portal-to-Portal Act applies",
        },
        "epa": {
            "admin_filing": "No EEOC filing required (but can file)",
            "lawsuit": "2 years from violation (3 years for willful)",
            "notes": "Lilly Ledbetter Act: each discriminatory paycheck restarts the clock",
        },
        "section_1981": {
            "admin_filing": "No administrative prerequisite",
            "lawsuit": "4 years (28 U.S.C. 1658(a))",
            "notes": "Broader than Title VII - covers race discrimination in contracts, no employer size limit",
        },
        "erisa": {
            "admin_filing": "Exhaust internal claims procedure first",
            "lawsuit": "Varies: breach of fiduciary duty 6 years from breach (3 years from actual knowledge)",
            "notes": "Benefits denial: plan-specified deadline or reasonable time",
        },
        "osha_11c": {
            "admin_filing": "30 days from retaliation to file with OSHA",
            "lawsuit": "No private right of action (OSHA prosecutes)",
            "notes": "Very short deadline; some circuit courts allow equitable tolling",
        },
        "texas_tchra": {
            "admin_filing": "180 days from discriminatory act to file with TWC",
            "lawsuit": "60-day waiting period, then 2 years from filing",
            "notes": "Cross-filing with EEOC extends to 300 days",
        },
        "warn_act": {
            "admin_filing": "No administrative prerequisite",
            "lawsuit": "Varies by circuit; generally 1-3 years under most appropriate state SOL",
            "notes": "No express federal SOL; courts borrow state law",
        },
    }

    def calculate(self, claim_type: str) -> Dict[str, Any]:
        """Get statute of limitations for a claim type."""
        claim_lower = claim_type.lower().replace(" ", "_").replace("-", "_")
        for key, info in self.LIMITATIONS.items():
            if key in claim_lower or claim_lower in key:
                return {"claim_type": key, **info}
        return {"claim_type": claim_type, "admin_filing": "Unknown", "lawsuit": "Unknown",
                "notes": "Claim type not found in limitations database"}

    def get_all(self) -> Dict[str, Any]:
        """Get all statutes of limitations."""
        return {"limitations": self.LIMITATIONS, "count": len(self.LIMITATIONS)}


@app.get("/limitations/{claim_type}")
async def get_limitations(claim_type: str) -> Dict[str, Any]:
    """Get statute of limitations for a specific claim type."""
    calc = StatuteOfLimitationsCalculator()
    return calc.calculate(claim_type)


@app.get("/limitations")
async def list_all_limitations() -> Dict[str, Any]:
    """List all statutes of limitations."""
    calc = StatuteOfLimitationsCalculator()
    return calc.get_all()


# ============================================================================
# DAMAGES CALCULATOR
# ============================================================================

class DamagesCalculator:
    """Estimate potential damages for employment law claims."""

    TITLE_VII_CAPS: ClassVar[Dict[str, int]] = {
        "15-100": 50000,
        "101-200": 100000,
        "201-500": 200000,
        "501+": 300000,
    }

    def estimate(self, claim_type: str, annual_salary: float,
                 years_employed: float, employer_size: int) -> Dict[str, Any]:
        """Estimate potential damages range."""
        estimates: Dict[str, Any] = {
            "claim_type": claim_type,
            "annual_salary": annual_salary,
            "years_employed": years_employed,
            "employer_size": employer_size,
        }

        # Back pay
        back_pay_months = min(years_employed * 12, 36)
        back_pay = round(annual_salary * (back_pay_months / 12), 2)
        estimates["back_pay"] = {"amount": back_pay, "months": back_pay_months,
                                  "note": "Mitigated by duty to seek comparable employment"}

        # Front pay
        front_pay_months = min(24, max(6, int(years_employed * 3)))
        front_pay = round(annual_salary * (front_pay_months / 12), 2)
        estimates["front_pay"] = {"amount": front_pay, "months": front_pay_months,
                                   "note": "Alternative to reinstatement; court discretion"}

        # Compensatory/punitive caps (Title VII/ADA)
        cap = 0
        for range_str, cap_amount in self.TITLE_VII_CAPS.items():
            parts = range_str.replace("+", "").split("-")
            low = int(parts[0])
            high = int(parts[-1]) if len(parts) > 1 else 999999
            if low <= employer_size <= high:
                cap = cap_amount
                break
        if employer_size > 500:
            cap = 300000

        estimates["compensatory_punitive_cap"] = {
            "cap": cap,
            "note": "Combined cap for compensatory + punitive damages under Title VII/ADA",
            "does_not_apply_to": ["back pay", "front pay", "attorneys fees", "FLSA", "Section 1981"],
        }

        # Liquidated damages
        claim_lower = claim_type.lower()
        if "flsa" in claim_lower or "overtime" in claim_lower or "wage" in claim_lower:
            estimates["liquidated_damages"] = {
                "amount": back_pay,
                "note": "Equal to back pay unless employer shows good faith (FLSA)",
            }
        elif "adea" in claim_lower or "age" in claim_lower:
            estimates["liquidated_damages"] = {
                "amount": back_pay,
                "note": "Equal to back pay for willful ADEA violations (in lieu of comp/punitive)",
            }
        elif "fmla" in claim_lower:
            estimates["liquidated_damages"] = {
                "amount": back_pay,
                "note": "Equal to back pay unless employer shows good faith (FMLA)",
            }

        # Attorneys fees estimate
        estimates["attorneys_fees"] = {
            "low_estimate": round(annual_salary * 0.5, 2),
            "high_estimate": round(annual_salary * 3.0, 2),
            "note": "Lodestar method; prevailing plaintiff entitled under most employment statutes",
        }

        # Total range
        low_total = back_pay + estimates.get("attorneys_fees", {}).get("low_estimate", 0)
        high_total = (back_pay + front_pay + cap +
                      estimates.get("liquidated_damages", {}).get("amount", 0) +
                      estimates.get("attorneys_fees", {}).get("high_estimate", 0))
        estimates["total_range"] = {
            "low": round(low_total, 2),
            "high": round(high_total, 2),
            "note": "Rough estimate only. Actual damages depend on facts, jurisdiction, and litigation outcomes.",
        }

        return estimates


@app.post("/damages/estimate")
async def estimate_damages(claim_type: str = Query(...),
                            annual_salary: float = Query(..., ge=0),
                            years_employed: float = Query(..., ge=0),
                            employer_size: int = Query(..., ge=1)) -> Dict[str, Any]:
    """Estimate potential damages for an employment claim."""
    calc = DamagesCalculator()
    return calc.estimate(claim_type, annual_salary, years_employed, employer_size)


# ============================================================================
# EEOC PROCESS GUIDE
# ============================================================================

class EEOCProcessGuide:
    """Guide for navigating the EEOC administrative process."""

    STEPS: ClassVar[List[Dict[str, str]]] = [
        {"step": "1", "action": "File Charge of Discrimination",
         "deadline": "180 days from discriminatory act (300 days if state agency)",
         "details": "File with nearest EEOC office or online at publicportal.eeoc.gov. Include: name, address, phone; employer info; description of discriminatory acts; dates; basis of discrimination."},
        {"step": "2", "action": "EEOC Notification to Employer",
         "deadline": "Within 10 days of filing",
         "details": "EEOC sends copy of charge to employer. Employer must preserve all relevant personnel records."},
        {"step": "3", "action": "Mediation Offer",
         "deadline": "Typically within 30 days",
         "details": "EEOC may offer voluntary mediation. Both parties must agree. Confidential. No admission. Settlements are binding."},
        {"step": "4", "action": "Investigation",
         "deadline": "Varies (months to years)",
         "details": "If mediation declined/fails, EEOC investigates. May request position statement from employer, interview witnesses, request documents."},
        {"step": "5", "action": "Determination",
         "deadline": "After investigation",
         "details": "EEOC issues determination: (a) Reasonable Cause - attempts conciliation, or (b) No Reasonable Cause - issues right-to-sue letter."},
        {"step": "6", "action": "Conciliation (if Reasonable Cause)",
         "deadline": "30 days typically",
         "details": "EEOC attempts to resolve through voluntary agreement. If conciliation fails, EEOC may file suit or issue right-to-sue."},
        {"step": "7", "action": "Right-to-Sue Letter",
         "deadline": "Can request after 180 days from filing (even if investigation ongoing)",
         "details": "EEOC issues right-to-sue letter. Charging party has 90 DAYS from receipt to file federal lawsuit."},
        {"step": "8", "action": "File Federal Lawsuit",
         "deadline": "90 days from receipt of right-to-sue letter",
         "details": "File complaint in federal district court (or state court in some cases). STRICT 90-day deadline."},
    ]

    def get_process(self) -> Dict[str, Any]:
        """Get full EEOC process guide."""
        return {
            "process": self.STEPS,
            "total_steps": len(self.STEPS),
            "key_deadlines": {
                "filing_deadline": "180/300 days from discriminatory act",
                "right_to_sue_request": "After 180 days from filing charge",
                "lawsuit_deadline": "90 days from receipt of right-to-sue letter",
            },
            "online_filing": "https://publicportal.eeoc.gov",
        }


@app.get("/eeoc/process")
async def eeoc_process() -> Dict[str, Any]:
    """Get EEOC administrative process guide."""
    guide = EEOCProcessGuide()
    return guide.get_process()


# ============================================================================
# EMPLOYER SIZE THRESHOLD CHECKER
# ============================================================================

class EmployerSizeChecker:
    """Check which employment laws apply based on employer size."""

    THRESHOLDS: ClassVar[Dict[str, Dict[str, Any]]] = {
        "FLSA": {"minimum_employees": 0, "note": "Covers enterprises with $500K+ annual revenue or individual coverage for interstate commerce workers"},
        "FMLA": {"minimum_employees": 50, "note": "50+ employees within 75 miles; employee must have 12 months and 1,250 hours"},
        "Title VII": {"minimum_employees": 15, "note": "15+ employees for 20+ calendar weeks in current or preceding year"},
        "ADA": {"minimum_employees": 15, "note": "Same as Title VII"},
        "ADEA": {"minimum_employees": 20, "note": "20+ employees for 20+ calendar weeks"},
        "GINA": {"minimum_employees": 15, "note": "Same as Title VII"},
        "EPA": {"minimum_employees": 0, "note": "Covers all employers covered by FLSA (no separate threshold)"},
        "Section 1981": {"minimum_employees": 0, "note": "No minimum employer size (race discrimination in contracts)"},
        "WARN Act": {"minimum_employees": 100, "note": "100+ full-time employees (not counting part-time)"},
        "USERRA": {"minimum_employees": 0, "note": "All employers regardless of size"},
        "NLRA": {"minimum_employees": 0, "note": "Jurisdictional standards based on business volume, not employee count"},
        "OSHA": {"minimum_employees": 0, "note": "All employers with employees; some exemptions for small employers (<10) from recordkeeping"},
        "ERISA": {"minimum_employees": 0, "note": "Any employer maintaining a covered benefit plan"},
        "COBRA": {"minimum_employees": 20, "note": "20+ employees on more than 50% of typical business days"},
        "TCHRA (Texas)": {"minimum_employees": 15, "note": "15+ for discrimination (20+ for age)"},
    }

    def check(self, employer_size: int) -> Dict[str, Any]:
        """Check which laws apply to an employer of given size."""
        applicable: List[Dict[str, Any]] = []
        not_applicable: List[Dict[str, Any]] = []

        for statute, info in self.THRESHOLDS.items():
            entry = {"statute": statute, **info}
            if employer_size >= info["minimum_employees"]:
                applicable.append(entry)
            else:
                not_applicable.append(entry)

        return {
            "employer_size": employer_size,
            "applicable_statutes": applicable,
            "not_applicable_statutes": not_applicable,
            "applicable_count": len(applicable),
            "not_applicable_count": len(not_applicable),
        }


@app.get("/thresholds/{employer_size}")
async def check_thresholds(employer_size: int) -> Dict[str, Any]:
    """Check which employment laws apply based on employer size."""
    checker = EmployerSizeChecker()
    return checker.check(employer_size)


@app.get("/thresholds")
async def list_all_thresholds() -> Dict[str, Any]:
    """List all employer size thresholds."""
    return {"thresholds": EmployerSizeChecker.THRESHOLDS, "count": len(EmployerSizeChecker.THRESHOLDS)}


@app.get("/info")
async def engine_info() -> Dict[str, Any]:
    """Get comprehensive engine information."""
    return {
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "engine_version": ENGINE_VERSION,
        "port": ENGINE_PORT,
        "tier": ENGINE_TIER,
        "mode": ENGINE_MODE,
        "authority_level": AUTHORITY_LEVEL,
        "architecture": "TIE-20",
        "components": [
            "three_layer_response", "response_modes", "doctrine_cache",
            "authority_hardening", "confidence_stratification", "semantic_normalization",
            "vector_search_chromadb", "telemetry_module", "doctrine_drift_watcher",
            "doctrine_coverage_map", "metrics_collector", "health_endpoint",
            "zoned_analysis", "fact_fragility_scoring", "audit_trail_jsonl",
            "determinism_hash_sha256", "fastapi_server", "loguru_logging",
            "multi_doctrine_decomposition", "deep_analysis_mode",
        ],
        "response_modes": ["FAST", "REVIEW", "MEMO"],
        "doctrine_count": get_doctrine_count(),
        "doctrine_hash": get_doctrine_hash(),
        "semantic_version": get_semantic_map_version(),
        "semantic_hash": get_semantic_map_hash(),
        "employment_domains": [
            "title_vii", "ada", "adea", "fmla", "flsa", "osha",
            "erisa", "nlra", "workers_comp", "termination", "non_compete",
            "warn_act", "whistleblower", "texas_labor",
        ],
    }


# ============================================================================
# RESPONSE FORMATTER
# ============================================================================

class ResponseFormatter:
    """Format analysis responses for different output modes."""

    def format_fast(self, response: AnalysisResponse) -> Dict[str, Any]:
        """Format for FAST mode - minimal, high-speed response."""
        return {
            "trace_id": response.trace_id,
            "answer": response.answer[:500],
            "claim_type": response.claim_type,
            "confidence": response.confidence,
            "confidence_band": response.confidence_band,
            "risk_score": response.risk_assessment.overall_score if response.risk_assessment else None,
            "risk_band": response.risk_assessment.overall_band if response.risk_assessment else None,
            "processing_time_ms": response.processing_time_ms,
        }

    def format_review(self, response: AnalysisResponse) -> Dict[str, Any]:
        """Format for REVIEW mode - detailed with structured analysis."""
        result: Dict[str, Any] = {
            "trace_id": response.trace_id,
            "query": response.query,
            "claim_type": response.claim_type,
            "claim_confidence": response.claim_confidence,
            "jurisdiction": response.jurisdiction,
            "analysis": {
                "answer": response.answer,
                "summary": response.summary,
                "response_layer": response.response_layer,
                "confidence": response.confidence,
                "confidence_band": response.confidence_band,
            },
            "legal_framework": {
                "statutes": response.statutes,
                "elements": response.elements,
                "defenses": response.defenses,
                "remedies": response.remedies,
                "citations": response.citations,
            },
            "risk_assessment": response.risk_assessment.model_dump() if response.risk_assessment else None,
            "fact_fragility": response.fact_fragility.model_dump() if response.fact_fragility else None,
            "doctrines_used": response.doctrines_used,
            "disclosures": response.disclosures,
            "processing_time_ms": response.processing_time_ms,
            "determinism_hash": response.determinism_hash,
        }
        return result

    def format_memo(self, response: AnalysisResponse) -> Dict[str, Any]:
        """Format for MEMO mode - full legal memorandum structure."""
        memo_sections: List[Dict[str, Any]] = []

        # Section I: Statement of Issue
        memo_sections.append({
            "section": "I. STATEMENT OF ISSUE",
            "content": f"This memorandum analyzes the following employment law question: {response.query}",
        })

        # Section II: Brief Answer
        memo_sections.append({
            "section": "II. BRIEF ANSWER",
            "content": response.summary,
        })

        # Section III: Statement of Facts
        memo_sections.append({
            "section": "III. STATEMENT OF FACTS",
            "content": "Based on the information provided, the relevant facts are set forth in the query above. "
                       "Additional facts may be necessary for a complete analysis.",
        })

        # Section IV: Applicable Law
        statutes_text = "\n".join(f"  - {s}" for s in response.statutes) if response.statutes else "  No specific statutes identified."
        memo_sections.append({
            "section": "IV. APPLICABLE LAW",
            "content": f"The following statutes and regulations govern this analysis:\n{statutes_text}",
        })

        # Section V: Analysis
        memo_sections.append({
            "section": "V. ANALYSIS",
            "content": response.answer,
        })

        # Section VI: Elements
        if response.elements:
            elements_text = "\n".join(f"  {i+1}. {e}" for i, e in enumerate(response.elements))
            memo_sections.append({
                "section": "VI. ELEMENTS OF CLAIM",
                "content": f"The following elements must be established:\n{elements_text}",
            })

        # Section VII: Defenses
        if response.defenses:
            defenses_text = "\n".join(f"  - {d}" for d in response.defenses)
            memo_sections.append({
                "section": "VII. POTENTIAL DEFENSES",
                "content": f"The following defenses may be available:\n{defenses_text}",
            })

        # Section VIII: Remedies
        if response.remedies:
            remedies_text = "\n".join(f"  - {r}" for r in response.remedies)
            memo_sections.append({
                "section": "VIII. AVAILABLE REMEDIES",
                "content": f"If liability is established, the following remedies may be available:\n{remedies_text}",
            })

        # Section IX: Risk Assessment
        if response.risk_assessment:
            memo_sections.append({
                "section": "IX. RISK ASSESSMENT",
                "content": f"Overall Risk: {response.risk_assessment.overall_band} "
                           f"(Score: {response.risk_assessment.overall_score:.2f})",
            })

        # Section X: Citations
        if response.citations:
            citations_text = "\n".join(f"  - {c}" for c in response.citations)
            memo_sections.append({
                "section": "X. AUTHORITIES CITED",
                "content": citations_text,
            })

        # Section XI: Disclosures
        disclosures_text = "\n".join(f"  - {d}" for d in response.disclosures)
        memo_sections.append({
            "section": "XI. DISCLOSURES AND LIMITATIONS",
            "content": disclosures_text,
        })

        return {
            "trace_id": response.trace_id,
            "memo_format": "LEGAL_MEMORANDUM",
            "date": datetime.now(timezone.utc).strftime("%B %d, %Y"),
            "re": f"Employment Law Analysis - {response.claim_type.replace('_', ' ').title()}",
            "jurisdiction": response.jurisdiction,
            "sections": memo_sections,
            "confidence": response.confidence,
            "confidence_band": response.confidence_band,
            "determinism_hash": response.determinism_hash,
            "processing_time_ms": response.processing_time_ms,
        }

    def format_response(self, response: AnalysisResponse, mode: str) -> Dict[str, Any]:
        """Route to appropriate formatter based on mode."""
        if mode == "FAST":
            return self.format_fast(response)
        elif mode == "MEMO":
            return self.format_memo(response)
        return self.format_review(response)


@app.post("/analyze/formatted")
async def analyze_formatted(request: AnalysisRequest,
                             processor: ThreeLayerProcessor = Depends(get_processor)) -> Dict[str, Any]:
    """Analyze with formatted output based on mode."""
    response = processor.process(request)
    formatter = ResponseFormatter()
    return formatter.format_response(response, request.mode.value)


# ============================================================================
# TIMELINE ANALYZER
# ============================================================================

class TimelineAnalyzer:
    """Analyze employment dispute timelines for critical deadlines."""

    CRITICAL_DEADLINES: ClassVar[Dict[str, Dict[str, Any]]] = {
        "eeoc_filing": {
            "description": "File EEOC Charge of Discrimination",
            "days": 180,
            "extended_days": 300,
            "extension_condition": "State or local agency with worksharing agreement",
            "applies_to": ["Title VII", "ADA", "ADEA", "GINA"],
            "consequences": "Claim may be time-barred",
        },
        "right_to_sue_lawsuit": {
            "description": "File federal lawsuit after receiving right-to-sue letter",
            "days": 90,
            "extended_days": None,
            "extension_condition": None,
            "applies_to": ["Title VII", "ADA"],
            "consequences": "Claim dismissed as untimely; strict deadline",
        },
        "flsa_sol": {
            "description": "FLSA statute of limitations from violation",
            "days": 730,
            "extended_days": 1095,
            "extension_condition": "Willful violation (3 years)",
            "applies_to": ["FLSA"],
            "consequences": "Back pay limited to SOL period",
        },
        "osha_complaint": {
            "description": "File OSHA Section 11(c) retaliation complaint",
            "days": 30,
            "extended_days": None,
            "extension_condition": None,
            "applies_to": ["OSHA"],
            "consequences": "Very short; equitable tolling may apply in some circuits",
        },
        "warn_act_notice": {
            "description": "WARN Act 60-day advance notice requirement",
            "days": 60,
            "extended_days": None,
            "extension_condition": None,
            "applies_to": ["WARN Act"],
            "consequences": "Per-day damages for each day of violation",
        },
        "cobra_election": {
            "description": "COBRA election period",
            "days": 60,
            "extended_days": None,
            "extension_condition": None,
            "applies_to": ["COBRA/ERISA"],
            "consequences": "Loss of right to continuation coverage",
        },
        "owbpa_consideration": {
            "description": "OWBPA consideration period for ADEA waiver",
            "days": 21,
            "extended_days": 45,
            "extension_condition": "Group termination/exit incentive program",
            "applies_to": ["ADEA/OWBPA"],
            "consequences": "Waiver is invalid and unenforceable",
        },
        "owbpa_revocation": {
            "description": "OWBPA revocation period for ADEA waiver",
            "days": 7,
            "extended_days": None,
            "extension_condition": None,
            "applies_to": ["ADEA/OWBPA"],
            "consequences": "Employee may revoke waiver within 7 days of signing",
        },
        "texas_final_pay_fired": {
            "description": "Texas final paycheck deadline if terminated",
            "days": 6,
            "extended_days": None,
            "extension_condition": None,
            "applies_to": ["Texas Payday Law"],
            "consequences": "TWC wage claim; administrative penalties",
        },
        "i9_completion": {
            "description": "I-9 form completion deadline from hire date",
            "days": 3,
            "extended_days": None,
            "extension_condition": "3 business days",
            "applies_to": ["IRCA"],
            "consequences": "Civil penalties per violation ($252-$2,507 per form)",
        },
    }

    def get_applicable_deadlines(self, claim_types: List[str]) -> List[Dict[str, Any]]:
        """Get all applicable deadlines for given claim types."""
        results: List[Dict[str, Any]] = []
        for key, deadline in self.CRITICAL_DEADLINES.items():
            for claim in claim_types:
                claim_upper = claim.upper().replace("_", " ")
                for applies in deadline["applies_to"]:
                    if applies.upper() in claim_upper or claim_upper in applies.upper():
                        results.append({"deadline_key": key, **deadline})
                        break
        return results

    def get_all_deadlines(self) -> Dict[str, Any]:
        """Get all critical deadlines."""
        return {"deadlines": self.CRITICAL_DEADLINES, "count": len(self.CRITICAL_DEADLINES)}


@app.get("/timeline/deadlines")
async def get_all_deadlines() -> Dict[str, Any]:
    """Get all critical employment law deadlines."""
    analyzer = TimelineAnalyzer()
    return analyzer.get_all_deadlines()


@app.post("/timeline/applicable")
async def get_applicable_deadlines(claim_types: List[str]) -> Dict[str, Any]:
    """Get applicable deadlines for specific claim types."""
    analyzer = TimelineAnalyzer()
    results = analyzer.get_applicable_deadlines(claim_types)
    return {"claim_types": claim_types, "deadlines": results, "count": len(results)}


# ============================================================================
# COMPARISON ENGINE
# ============================================================================

class ClaimComparisonEngine:
    """Compare different employment law claims side by side."""

    def compare(self, claim_types: List[str]) -> Dict[str, Any]:
        """Compare multiple claim types across key dimensions."""
        doctrine_engine = get_doctrine_engine()
        comparisons: List[Dict[str, Any]] = []

        for claim_type in claim_types:
            results = doctrine_engine.search_by_text(claim_type, max_results=1)
            if results:
                doctrine = results[0]
                block = doctrine_engine.get_doctrine_block(doctrine.topic)
                if block:
                    comparisons.append({
                        "claim_type": claim_type,
                        "topic": doctrine.topic,
                        "title": doctrine.title,
                        "category": doctrine.category,
                        "confidence": doctrine.confidence,
                        "key_statutes": block.get("key_statutes", []),
                        "elements_count": len(block.get("elements", [])),
                        "elements": block.get("elements", []),
                        "defenses_count": len(block.get("defenses", [])),
                        "defenses": block.get("defenses", []),
                        "remedies": block.get("remedies", []),
                        "leading_cases_count": len(block.get("leading_cases", [])),
                    })
            else:
                comparisons.append({
                    "claim_type": claim_type,
                    "topic": "not_found",
                    "title": f"No doctrine found for '{claim_type}'",
                    "category": "unknown",
                    "confidence": 0.0,
                    "key_statutes": [],
                    "elements_count": 0,
                    "elements": [],
                    "defenses_count": 0,
                    "defenses": [],
                    "remedies": [],
                    "leading_cases_count": 0,
                })

        return {
            "claim_types": claim_types,
            "comparisons": comparisons,
            "count": len(comparisons),
        }


@app.post("/compare")
async def compare_claims(claim_types: List[str]) -> Dict[str, Any]:
    """Compare multiple employment law claim types side by side."""
    if len(claim_types) < 2:
        raise HTTPException(status_code=400, detail="At least 2 claim types required for comparison")
    if len(claim_types) > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 claim types per comparison")
    engine = ClaimComparisonEngine()
    return engine.compare(claim_types)


# ============================================================================
# ISSUE SPOTTER
# ============================================================================

class IssueSpotter:
    """Identify all potential employment law issues in a fact pattern."""

    ISSUE_PATTERNS: ClassVar[Dict[str, Dict[str, Any]]] = {
        "discrimination": {
            "triggers": ["race", "sex", "gender", "religion", "national origin", "color", "pregnancy",
                        "disability", "age", "genetic", "orientation", "transgender"],
            "claim": "Employment discrimination (Title VII, ADA, ADEA, GINA)",
            "urgency": "HIGH",
        },
        "harassment": {
            "triggers": ["harassment", "hostile", "inappropriate", "unwelcome", "sexual", "offensive",
                        "severe", "pervasive", "touching", "comments"],
            "claim": "Workplace harassment (Title VII hostile work environment)",
            "urgency": "HIGH",
        },
        "retaliation": {
            "triggers": ["retaliated", "retaliation", "complained", "reported", "filed complaint",
                        "punished", "adverse action", "after filing"],
            "claim": "Retaliation (Title VII, FLSA, FMLA, OSHA, whistleblower)",
            "urgency": "HIGH",
        },
        "wage_theft": {
            "triggers": ["unpaid", "overtime", "minimum wage", "off the clock", "misclassified",
                        "independent contractor", "no overtime", "salary deduction"],
            "claim": "Wage and hour violation (FLSA)",
            "urgency": "MEDIUM",
        },
        "leave_interference": {
            "triggers": ["denied leave", "fmla", "medical leave", "family leave", "maternity",
                        "fired after leave", "return from leave"],
            "claim": "FMLA interference or retaliation",
            "urgency": "HIGH",
        },
        "safety_concern": {
            "triggers": ["unsafe", "hazard", "injury", "osha", "danger", "safety violation",
                        "no protection", "chemical exposure"],
            "claim": "OSHA violation or safety-related retaliation",
            "urgency": "HIGH",
        },
        "wrongful_termination": {
            "triggers": ["fired", "terminated", "let go", "wrongful", "no reason",
                        "forced to resign", "constructive discharge"],
            "claim": "Wrongful termination or constructive discharge",
            "urgency": "HIGH",
        },
        "non_compete_issue": {
            "triggers": ["non-compete", "noncompete", "cant work", "restrictive covenant",
                        "trade secret", "competition"],
            "claim": "Non-compete/restrictive covenant dispute",
            "urgency": "MEDIUM",
        },
        "benefits_denial": {
            "triggers": ["benefits denied", "pension", "401k", "health plan", "erisa",
                        "fiduciary", "vesting"],
            "claim": "ERISA benefits claim",
            "urgency": "MEDIUM",
        },
        "mass_layoff": {
            "triggers": ["mass layoff", "plant closing", "reduction in force", "rif",
                        "no notice", "warn act"],
            "claim": "WARN Act violation",
            "urgency": "HIGH",
        },
    }

    def spot_issues(self, fact_pattern: str) -> Dict[str, Any]:
        """Identify all potential employment law issues in a fact pattern."""
        fact_lower = fact_pattern.lower()
        spotted_issues: List[Dict[str, Any]] = []

        for issue_key, info in self.ISSUE_PATTERNS.items():
            matched_triggers: List[str] = []
            for trigger in info["triggers"]:
                if trigger in fact_lower:
                    matched_triggers.append(trigger)

            if matched_triggers:
                spotted_issues.append({
                    "issue": issue_key,
                    "claim": info["claim"],
                    "urgency": info["urgency"],
                    "matched_triggers": matched_triggers,
                    "trigger_count": len(matched_triggers),
                    "confidence": min(0.95, 0.3 + 0.15 * len(matched_triggers)),
                })

        spotted_issues.sort(key=lambda x: (-len(x["matched_triggers"]), x["urgency"] == "HIGH"), reverse=False)
        spotted_issues.sort(key=lambda x: x["trigger_count"], reverse=True)

        return {
            "fact_pattern": fact_pattern[:500],
            "issues_spotted": spotted_issues,
            "total_issues": len(spotted_issues),
            "high_urgency_count": sum(1 for i in spotted_issues if i["urgency"] == "HIGH"),
        }


@app.post("/spot-issues")
async def spot_issues(fact_pattern: str = Query(..., min_length=10)) -> Dict[str, Any]:
    """Spot all potential employment law issues in a fact pattern."""
    spotter = IssueSpotter()
    return spotter.spot_issues(fact_pattern)


# ============================================================================
# ADMINISTRATIVE REMEDY CHECKER
# ============================================================================

class AdministrativeRemedyChecker:
    """Check administrative exhaustion requirements for employment claims."""

    REQUIREMENTS: ClassVar[Dict[str, Dict[str, Any]]] = {
        "title_vii": {
            "agency": "EEOC",
            "required": True,
            "filing_deadline": "180/300 days",
            "process": "File charge -> EEOC investigation -> Right-to-sue letter -> 90-day lawsuit deadline",
            "consequences_of_failure": "Claim dismissed for failure to exhaust",
        },
        "ada": {
            "agency": "EEOC",
            "required": True,
            "filing_deadline": "180/300 days",
            "process": "Same as Title VII",
            "consequences_of_failure": "Claim dismissed for failure to exhaust",
        },
        "adea": {
            "agency": "EEOC",
            "required": True,
            "filing_deadline": "180/300 days",
            "process": "File charge -> 60-day waiting period -> may file suit (no right-to-sue letter required)",
            "consequences_of_failure": "Claim dismissed for failure to exhaust",
        },
        "fmla": {
            "agency": "None",
            "required": False,
            "filing_deadline": "N/A",
            "process": "Direct filing in federal or state court within 2/3-year SOL",
            "consequences_of_failure": "N/A",
        },
        "flsa": {
            "agency": "None (or DOL complaint optional)",
            "required": False,
            "filing_deadline": "N/A",
            "process": "Direct filing in federal or state court within 2/3-year SOL",
            "consequences_of_failure": "N/A",
        },
        "epa": {
            "agency": "None (EEOC optional)",
            "required": False,
            "filing_deadline": "N/A",
            "process": "Direct filing within 2/3-year SOL",
            "consequences_of_failure": "N/A",
        },
        "section_1981": {
            "agency": "None",
            "required": False,
            "filing_deadline": "N/A",
            "process": "Direct filing within 4-year SOL",
            "consequences_of_failure": "N/A",
        },
        "erisa": {
            "agency": "Plan administrator",
            "required": True,
            "filing_deadline": "Per plan terms",
            "process": "Exhaust internal claims and appeals procedure",
            "consequences_of_failure": "Claim dismissed for failure to exhaust (but futility exception may apply)",
        },
        "texas_tchra": {
            "agency": "TWC Civil Rights Division",
            "required": True,
            "filing_deadline": "180 days (300 if cross-filed with EEOC)",
            "process": "File complaint with TWC -> 180-day investigation period -> right-to-sue",
            "consequences_of_failure": "Claim dismissed for failure to exhaust",
        },
    }

    def check(self, claim_type: str) -> Dict[str, Any]:
        """Check exhaustion requirements for a claim type."""
        claim_lower = claim_type.lower().replace(" ", "_").replace("-", "_")
        for key, info in self.REQUIREMENTS.items():
            if key in claim_lower or claim_lower in key:
                return {"claim_type": key, **info}
        return {"claim_type": claim_type, "agency": "Unknown", "required": None,
                "filing_deadline": "Unknown", "process": "Consult applicable statute",
                "consequences_of_failure": "Unknown"}

    def check_all(self) -> Dict[str, Any]:
        """Get all administrative exhaustion requirements."""
        return {"requirements": self.REQUIREMENTS, "count": len(self.REQUIREMENTS)}


@app.get("/exhaustion/{claim_type}")
async def check_exhaustion(claim_type: str) -> Dict[str, Any]:
    """Check administrative exhaustion requirements for a claim type."""
    checker = AdministrativeRemedyChecker()
    return checker.check(claim_type)


@app.get("/exhaustion")
async def list_exhaustion_requirements() -> Dict[str, Any]:
    """List all administrative exhaustion requirements."""
    checker = AdministrativeRemedyChecker()
    return checker.check_all()


# ============================================================================
# EMPLOYMENT LAW DOCUMENT GENERATOR
# ============================================================================

class DocumentGenerator:
    """Generates structured employment law documents and templates."""

    DOCUMENT_TEMPLATES: Dict[str, Dict[str, Any]] = {
        "demand_letter": {
            "name": "Employment Demand Letter",
            "sections": ["header", "factual_background", "legal_basis", "damages_calculation", "demand", "deadline", "closing"],
            "description": "Pre-litigation demand letter for employment claims",
        },
        "eeoc_charge": {
            "name": "EEOC Charge of Discrimination",
            "sections": ["charging_party_info", "respondent_info", "discrimination_basis", "date_of_harm", "factual_allegations", "remedy_sought"],
            "description": "Template for filing EEOC charge of discrimination",
        },
        "position_statement": {
            "name": "Employer Position Statement",
            "sections": ["company_background", "complainant_history", "factual_response", "legitimate_reasons", "policy_compliance", "witness_list"],
            "description": "Employer response to EEOC charge",
        },
        "separation_agreement": {
            "name": "Separation and Release Agreement",
            "sections": ["parties", "separation_terms", "consideration", "general_release", "adea_waiver", "confidentiality", "non_disparagement", "cooperation", "governing_law"],
            "description": "Employee separation with OWBPA-compliant release",
        },
        "workplace_investigation_report": {
            "name": "Workplace Investigation Report",
            "sections": ["scope", "methodology", "witnesses_interviewed", "documents_reviewed", "factual_findings", "credibility_assessment", "conclusions", "recommendations"],
            "description": "Internal investigation report template",
        },
    }

    def get_template(self, template_type: str) -> Dict[str, Any]:
        """Get document template by type."""
        template = self.DOCUMENT_TEMPLATES.get(template_type)
        if not template:
            return {"error": f"Unknown template: {template_type}", "available": list(self.DOCUMENT_TEMPLATES.keys())}
        return {
            "template_type": template_type,
            "name": template["name"],
            "description": template["description"],
            "sections": template["sections"],
            "section_guidance": self._get_section_guidance(template_type, template["sections"]),
        }

    def _get_section_guidance(self, template_type: str, sections: List[str]) -> Dict[str, str]:
        """Provide guidance for each section of the document."""
        guidance_map: Dict[str, Dict[str, str]] = {
            "demand_letter": {
                "header": "Identify sender, recipient, date, and RE line with employee name and claim type",
                "factual_background": "Chronological narrative of relevant events, employment dates, position, protected class status",
                "legal_basis": "Identify all applicable statutes and legal theories with elements analysis",
                "damages_calculation": "Itemize economic damages (back pay, front pay, benefits) and non-economic damages (emotional distress)",
                "demand": "State specific dollar amount or terms demanded, including non-monetary relief",
                "deadline": "Set reasonable response deadline (typically 10-30 days) and state intent to file if unresolved",
                "closing": "Professional closing with contact information and preservation of all rights",
            },
            "eeoc_charge": {
                "charging_party_info": "Full name, address, phone, email of the charging party",
                "respondent_info": "Employer name, address, number of employees, EIN if available",
                "discrimination_basis": "Check all applicable: race, color, sex, religion, national origin, age, disability, genetic information, retaliation",
                "date_of_harm": "Date of most recent discriminatory act (critical for timeliness - 180/300 day deadline)",
                "factual_allegations": "Concise narrative: what happened, when, who was involved, comparators if any",
                "remedy_sought": "Back pay, reinstatement, compensatory damages, policy changes, training",
            },
            "separation_agreement": {
                "parties": "Full legal names of employer entity and employee",
                "separation_terms": "Last day of employment, transition duties, return of property, reference agreement",
                "consideration": "Severance amount, benefits continuation (COBRA subsidy), outplacement services",
                "general_release": "Broad release of all claims arising from employment (list specific statutes released)",
                "adea_waiver": "OWBPA requirements: 21/45 day consideration period, 7-day revocation right, advise to consult attorney, list of decisional unit for group terminations",
                "confidentiality": "Non-disclosure of agreement terms (carve-outs for spouse, attorney, tax advisor, government agencies)",
                "non_disparagement": "Mutual non-disparagement with carve-outs for truthful statements to government agencies",
                "cooperation": "Post-separation cooperation in litigation and transition matters",
                "governing_law": "Choice of law (typically employer's state) and venue for disputes",
            },
        }
        return guidance_map.get(template_type, {section: f"Complete the {section} section with relevant details" for section in sections})

    def list_templates(self) -> List[Dict[str, str]]:
        """List all available document templates."""
        return [
            {"type": key, "name": val["name"], "description": val["description"]}
            for key, val in self.DOCUMENT_TEMPLATES.items()
        ]


# ============================================================================
# JURISDICTION ANALYZER
# ============================================================================

class JurisdictionAnalyzer:
    """Analyze multi-jurisdictional employment law issues."""

    FEDERAL_THRESHOLDS: Dict[str, Dict[str, Any]] = {
        "title_vii": {"min_employees": 15, "statute": "42 U.S.C. 2000e(b)", "filing_deadline_days": 300, "agency": "EEOC"},
        "ada": {"min_employees": 15, "statute": "42 U.S.C. 12111(5)", "filing_deadline_days": 300, "agency": "EEOC"},
        "adea": {"min_employees": 20, "statute": "29 U.S.C. 630(b)", "filing_deadline_days": 300, "agency": "EEOC"},
        "fmla": {"min_employees": 50, "statute": "29 U.S.C. 2611(4)", "filing_deadline_days": 730, "agency": "DOL"},
        "flsa": {"min_employees": 1, "statute": "29 U.S.C. 203(d)", "filing_deadline_days": 730, "agency": "DOL"},
        "eppa": {"min_employees": 1, "statute": "29 U.S.C. 2006", "filing_deadline_days": 1095, "agency": "DOL"},
        "warn": {"min_employees": 100, "statute": "29 U.S.C. 2101(a)(1)", "filing_deadline_days": 1095, "agency": "DOL"},
        "section_1981": {"min_employees": 1, "statute": "42 U.S.C. 1981", "filing_deadline_days": 1460, "agency": "EEOC/Court"},
        "equal_pay_act": {"min_employees": 1, "statute": "29 U.S.C. 206(d)", "filing_deadline_days": 730, "agency": "EEOC"},
        "gina": {"min_employees": 15, "statute": "42 U.S.C. 2000ff-1", "filing_deadline_days": 300, "agency": "EEOC"},
        "userra": {"min_employees": 1, "statute": "38 U.S.C. 4303(4)", "filing_deadline_days": 0, "agency": "DOL/VETS"},
        "nlra": {"min_employees": 1, "statute": "29 U.S.C. 152(2)", "filing_deadline_days": 180, "agency": "NLRB"},
        "osha_11c": {"min_employees": 1, "statute": "29 U.S.C. 660(c)", "filing_deadline_days": 30, "agency": "OSHA"},
        "cobra": {"min_employees": 20, "statute": "29 U.S.C. 1161", "filing_deadline_days": 1095, "agency": "DOL"},
        "erisa": {"min_employees": 1, "statute": "29 U.S.C. 1003", "filing_deadline_days": 2190, "agency": "DOL"},
    }

    TEXAS_SPECIFICS: Dict[str, Dict[str, Any]] = {
        "tchra": {"statute": "Tex. Lab. Code Ch. 21", "min_employees": 15, "filing_deadline_days": 180, "agency": "TWC"},
        "payday_law": {"statute": "Tex. Lab. Code Ch. 61", "min_employees": 1, "filing_deadline_days": 180, "agency": "TWC"},
        "workers_comp_retaliation": {"statute": "Tex. Lab. Code 451.001", "min_employees": 1, "filing_deadline_days": 730, "agency": "Court"},
        "non_compete": {"statute": "Tex. Bus. & Com. Code 15.50", "min_employees": 1, "filing_deadline_days": 1460, "agency": "Court"},
        "whistleblower": {"statute": "Tex. Gov. Code Ch. 554", "min_employees": 1, "filing_deadline_days": 90, "agency": "Court"},
        "mini_cobra": {"statute": "Tex. Ins. Code Ch. 1251", "min_employees": 2, "filing_deadline_days": 1095, "agency": "TDI"},
    }

    def analyze_jurisdiction(self, employee_count: int, state: str = "TX") -> Dict[str, Any]:
        """Determine which federal and state laws apply based on employer size and location."""
        applicable_federal: List[Dict[str, Any]] = []
        for law, info in self.FEDERAL_THRESHOLDS.items():
            if employee_count >= info["min_employees"]:
                applicable_federal.append({
                    "law": law,
                    "statute": info["statute"],
                    "filing_deadline_days": info["filing_deadline_days"],
                    "agency": info["agency"],
                    "applicable": True,
                })
            else:
                applicable_federal.append({
                    "law": law,
                    "statute": info["statute"],
                    "min_employees_required": info["min_employees"],
                    "applicable": False,
                    "reason": f"Requires {info['min_employees']} employees, employer has {employee_count}",
                })

        applicable_state: List[Dict[str, Any]] = []
        if state.upper() == "TX":
            for law, info in self.TEXAS_SPECIFICS.items():
                if employee_count >= info["min_employees"]:
                    applicable_state.append({
                        "law": law,
                        "statute": info["statute"],
                        "filing_deadline_days": info["filing_deadline_days"],
                        "agency": info["agency"],
                        "applicable": True,
                    })

        return {
            "employee_count": employee_count,
            "state": state,
            "federal_laws": applicable_federal,
            "state_laws": applicable_state,
            "total_applicable": sum(1 for f in applicable_federal if f["applicable"]) + len(applicable_state),
            "critical_deadlines": self._get_critical_deadlines(applicable_federal, applicable_state),
        }

    def _get_critical_deadlines(self, federal: List[Dict[str, Any]], state: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Extract and sort critical filing deadlines."""
        deadlines: List[Dict[str, Any]] = []
        for law in federal + state:
            if law.get("applicable") and law.get("filing_deadline_days", 0) > 0:
                deadlines.append({
                    "law": law["law"],
                    "deadline_days": law["filing_deadline_days"],
                    "agency": law["agency"],
                })
        deadlines.sort(key=lambda x: x["deadline_days"])
        return deadlines


# ============================================================================
# DOCUMENT AND JURISDICTION API ENDPOINTS
# ============================================================================

@app.get("/documents/templates")
async def list_document_templates() -> Dict[str, Any]:
    """List all available document templates."""
    gen = DocumentGenerator()
    return {"templates": gen.list_templates(), "count": len(gen.DOCUMENT_TEMPLATES)}


@app.get("/documents/template/{template_type}")
async def get_document_template(template_type: str) -> Dict[str, Any]:
    """Get a specific document template with section guidance."""
    gen = DocumentGenerator()
    return gen.get_template(template_type)


@app.get("/jurisdiction/analyze")
async def analyze_jurisdiction(employee_count: int = 50, state: str = "TX") -> Dict[str, Any]:
    """Analyze applicable employment laws based on employer size and state."""
    analyzer = JurisdictionAnalyzer()
    return analyzer.analyze_jurisdiction(employee_count, state)


@app.get("/jurisdiction/deadlines")
async def get_filing_deadlines(employee_count: int = 50, state: str = "TX") -> Dict[str, Any]:
    """Get critical filing deadlines for applicable employment laws."""
    analyzer = JurisdictionAnalyzer()
    result = analyzer.analyze_jurisdiction(employee_count, state)
    return {
        "employee_count": employee_count,
        "state": state,
        "deadlines": result["critical_deadlines"],
        "warning": "Filing deadlines are measured from the date of the adverse action. Some deadlines are jurisdictional and cannot be extended.",
    }


@app.get("/jurisdiction/federal-thresholds")
async def get_federal_thresholds() -> Dict[str, Any]:
    """Get all federal employment law employer size thresholds."""
    analyzer = JurisdictionAnalyzer()
    return {
        "thresholds": [
            {"law": k, "min_employees": v["min_employees"], "statute": v["statute"], "agency": v["agency"]}
            for k, v in sorted(analyzer.FEDERAL_THRESHOLDS.items(), key=lambda x: x[1]["min_employees"])
        ],
    }


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    logger.add(
        LOG_DIR / "engine_{time}.log",
        rotation="100 MB",
        retention="90 days",
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level:8} | {name}:{function}:{line} | {message}",
    )

    logger.info("Starting LG07 Employment Law Engine on port {}", ENGINE_PORT)

    uvicorn.run(
        "engine:app",
        host="0.0.0.0",
        port=ENGINE_PORT,
        reload=False,
        workers=1,
        log_level="info",
    )