"""
ECHO R08 SPACING RULES ENGINE - TIE-20 Gold Standard
=====================================================
Well spacing and density rules for oil & gas operations.

Architecture:
    Layer 1: Doctrine Cache (0-200ms) - Pre-compiled expert reasoning
    Layer 2: Semantic Retrieval (200-700ms) - Fast RAG on cache miss
    Layer 3: Deep Analysis (on-demand) - Multi-source synthesis

Response Modes:
    FAST: Doctrine-driven, minimal citations, sub-2 seconds
    DEFENSE: Structured reasoning, audit-ready, burden analysis
    MEMO: Long-form, citation-heavy, firm documentation

Domain:
    Rule 37 (spacing), Rule 38 (density), horizontal well spacing,
    special field rules, pooling, correlative rights, urban drilling,
    diagonal rule, stacked laterals, multi-lateral spacing

Port: 8708
Version: 2.0.0
Author: ECHO OMEGA PRIME
Authority: 11.0 SOVEREIGN
"""

# ==============================================================================
# IMPORTS
# ==============================================================================

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Literal, Tuple
from enum import Enum
from dataclasses import dataclass, field as dataclass_field
from datetime import datetime, timezone
from contextlib import asynccontextmanager
import hashlib
import json
import time
import uuid
from pathlib import Path
from loguru import logger
import sys

# ==============================================================================
# PATH SETUP - Must precede local imports
# ==============================================================================

ENGINE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ENGINE_DIR))

# ==============================================================================
# LOCAL MODULE IMPORTS
# ==============================================================================

from telemetry import get_telemetry, trace_query, complete_trace, log_error, ErrorDomain
from semantic import normalize_semantics, NormalizationResult
from doctrines import DOCTRINE_CACHE, DoctrineBlock, match_doctrines, ConfidenceStratification
from search import vector_search

# ==============================================================================
# CLOUD RETRIEVER (Optional - graceful degradation if unavailable)
# ==============================================================================

try:
    from cloud_retriever import CloudRetriever
    _cloud_retriever = CloudRetriever()
    _cloud_available = True
    logger.info("Cloud retriever loaded successfully")
except ImportError:
    _cloud_retriever = None
    _cloud_available = False
    logger.info("Cloud retriever not available - operating in local-only mode")

# ==============================================================================
# CONSTANTS
# ==============================================================================

ENGINE_NAME = "R08_spacing_rules"
ENGINE_VERSION = "2.0.0"
ENGINE_PORT = 8708
ENGINE_DOMAIN = "well_spacing_density"

LOG_DIR = Path("O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/R08_spacing_rules/logs")
LOG_DIR.mkdir(exist_ok=True, parents=True)

AUDIT_LOG = LOG_DIR / "audit_trail.jsonl"

logger.add(
    LOG_DIR / "r08_engine_{time}.log",
    rotation="50 MB",
    retention="30 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {message}",
)

# ==============================================================================
# TIE COMPONENT 6: SEMANTIC NORMALIZATION - Spacing Term Map
# ==============================================================================

SPACING_TERM_NORMALIZATION: Dict[str, str] = {
    "rule 37": "rule_37_spacing",
    "rule37": "rule_37_spacing",
    "statewide rule 37": "rule_37_spacing",
    "swr 37": "rule_37_spacing",
    "spacing rule": "rule_37_spacing",
    "well spacing": "rule_37_spacing",
    "lease line setback": "rule_37_spacing",
    "property line distance": "rule_37_spacing",
    "between-well distance": "rule_37_spacing",
    "inter-well spacing": "rule_37_spacing",
    "467 feet": "oil_lease_line_setback",
    "467 ft": "oil_lease_line_setback",
    "1200 feet": "oil_between_well_distance",
    "1200 ft": "oil_between_well_distance",
    "1,200 feet": "oil_between_well_distance",
    "330 feet": "gas_lease_line_setback",
    "330 ft": "gas_lease_line_setback",
    "660 feet": "gas_between_well_distance",
    "660 ft": "gas_between_well_distance",
    "rule 38": "rule_38_density",
    "rule38": "rule_38_density",
    "statewide rule 38": "rule_38_density",
    "swr 38": "rule_38_density",
    "density rule": "rule_38_density",
    "proration unit": "rule_38_density",
    "proration": "rule_38_density",
    "allocation formula": "rule_38_density",
    "40 acres": "oil_proration_unit",
    "640 acres": "gas_proration_unit",
    "horizontal spacing": "horizontal_well_spacing",
    "horizontal well spacing": "horizontal_well_spacing",
    "lateral spacing": "horizontal_well_spacing",
    "lateral setback": "horizontal_well_spacing",
    "stacked laterals": "stacked_lateral_spacing",
    "stacked lateral": "stacked_lateral_spacing",
    "multi-lateral": "multi_lateral_spacing",
    "multilateral": "multi_lateral_spacing",
    "diagonal rule": "diagonal_spacing_rule",
    "diagonal setback": "diagonal_spacing_rule",
    "pooling": "pooling_general",
    "voluntary pooling": "voluntary_pooling",
    "forced pooling": "forced_pooling",
    "compulsory pooling": "forced_pooling",
    "mineral interest pooling": "forced_pooling",
    "mipa": "forced_pooling",
    "mineral interest pooling act": "forced_pooling",
    "correlative rights": "correlative_rights",
    "drainage": "correlative_rights",
    "offset drainage": "correlative_rights",
    "confiscation": "correlative_rights",
    "special field rules": "special_field_rules",
    "field rules": "special_field_rules",
    "field-specific rules": "special_field_rules",
    "field specific": "special_field_rules",
    "urban drilling": "urban_drilling_spacing",
    "city ordinance": "urban_drilling_spacing",
    "municipal drilling": "urban_drilling_spacing",
    "protected use": "urban_drilling_spacing",
    "rrc": "railroad_commission",
    "railroad commission": "railroad_commission",
    "texas railroad commission": "railroad_commission",
    "exception": "spacing_exception",
    "rule 37 exception": "spacing_exception",
    "spacing exception": "spacing_exception",
    "variance": "spacing_exception",
    "w-1": "drilling_permit",
    "drilling permit": "drilling_permit",
    "form w-1": "drilling_permit",
    "permit to drill": "drilling_permit",
    "form p-4": "production_report",
    "p-4": "production_report",
    "monthly production": "production_report",
    "downspacing": "density_exception",
    "down-spacing": "density_exception",
    "infill drilling": "density_exception",
    "infill well": "density_exception",
    "offset well": "offset_well",
    "offset operator": "offset_operator",
    "permian basin": "permian_basin_field",
    "eagle ford": "eagle_ford_field",
    "barnett shale": "barnett_shale_field",
    "haynesville": "haynesville_field",
    "spraberry": "spraberry_trend_field",
    "wolfcamp": "wolfcamp_field",
    "bone spring": "bone_spring_field",
    "delaware basin": "delaware_basin_field",
    "midland basin": "midland_basin_field",
}

# ==============================================================================
# TIE COMPONENT 4: AUTHORITY HARDENING
# ==============================================================================


class AuthorityLevel(str, Enum):
    """Hierarchical authority levels for well spacing doctrine."""
    CONSTITUTIONAL = "constitutional"
    STATUTORY = "statutory"
    REGULATORY = "regulatory"
    ADMINISTRATIVE_RULING = "administrative_ruling"
    FIELD_RULE = "field_rule"
    INDUSTRY_PRACTICE = "industry_practice"
    ADVISORY = "advisory"
    COMMENTARY = "commentary"


AUTHORITY_WEIGHTS: Dict[str, float] = {
    # Constitutional provisions
    "TX_CONST_ART_XVI_S59": 1.00,
    # Statutory authorities
    "TX_NRC_85": 0.95,
    "TX_NRC_86": 0.95,
    "TX_NRC_102": 0.93,
    "TX_NRC_91": 0.92,
    "TX_LOCAL_GOV_81": 0.90,
    # Administrative Code (Statewide Rules)
    "16_TAC_3.37": 0.92,
    "16_TAC_3.38": 0.92,
    "16_TAC_3.36": 0.90,
    "16_TAC_3.40": 0.89,
    "16_TAC_3.42": 0.88,
    "16_TAC_3.46": 0.87,
    # RRC Dockets and Rulings
    "RRC_FINAL_ORDER": 0.85,
    "RRC_EXAMINER_REPORT": 0.78,
    "RRC_ADVISORY_BULLETIN": 0.70,
    # Court Decisions
    "TX_SUPREME_COURT": 0.95,
    "TX_COURT_APPEALS": 0.88,
    "TX_DISTRICT_COURT": 0.80,
    # Field-Specific Rules
    "FIELD_RULE_PERMIAN": 0.86,
    "FIELD_RULE_EAGLE_FORD": 0.86,
    "FIELD_RULE_BARNETT": 0.86,
    "FIELD_RULE_HAYNESVILLE": 0.86,
    "FIELD_RULE_GENERAL": 0.82,
    # Industry Practice
    "API_STANDARD": 0.65,
    "SPE_GUIDELINE": 0.60,
    "INDUSTRY_CUSTOM": 0.50,
    # Advisory / Commentary
    "RRC_FAQ": 0.55,
    "LEGAL_COMMENTARY": 0.45,
    "ACADEMIC_ARTICLE": 0.40,
}


def classify_authority(source: str) -> AuthorityLevel:
    """Classify an authority source into its hierarchical level."""
    source_upper = source.upper()
    if "CONSTITUTION" in source_upper or "CONST" in source_upper:
        return AuthorityLevel.CONSTITUTIONAL
    if any(term in source_upper for term in [
        "NATURAL RESOURCES CODE", "NRC", "LOCAL GOVERNMENT CODE",
        "CHAPTER 102", "CHAPTER 85", "CHAPTER 86", "CHAPTER 91",
    ]):
        return AuthorityLevel.STATUTORY
    if any(term in source_upper for term in [
        "TAC", "STATEWIDE RULE", "SWR", "16 TAC",
    ]):
        return AuthorityLevel.REGULATORY
    if any(term in source_upper for term in [
        "FINAL ORDER", "DOCKET", "EXAMINER", "RRC ORDER",
    ]):
        return AuthorityLevel.ADMINISTRATIVE_RULING
    if any(term in source_upper for term in [
        "FIELD RULE", "FIELD-SPECIFIC", "SPECIAL FIELD",
    ]):
        return AuthorityLevel.FIELD_RULE
    if any(term in source_upper for term in [
        "API", "SPE", "INDUSTRY", "CUSTOM", "PRACTICE",
    ]):
        return AuthorityLevel.INDUSTRY_PRACTICE
    if any(term in source_upper for term in [
        "FAQ", "ADVISORY", "BULLETIN", "GUIDANCE",
    ]):
        return AuthorityLevel.ADVISORY
    return AuthorityLevel.COMMENTARY


def resolve_authority_conflict(
    authority_a: str,
    authority_b: str,
) -> Dict[str, Any]:
    """Resolve conflict between two authority sources using hierarchical weights."""
    level_a = classify_authority(authority_a)
    level_b = classify_authority(authority_b)
    weight_a = _lookup_authority_weight(authority_a)
    weight_b = _lookup_authority_weight(authority_b)

    if weight_a > weight_b:
        winner, loser = authority_a, authority_b
        winner_level, loser_level = level_a, level_b
        winner_weight, loser_weight = weight_a, weight_b
    elif weight_b > weight_a:
        winner, loser = authority_b, authority_a
        winner_level, loser_level = level_b, level_a
        winner_weight, loser_weight = weight_b, weight_a
    else:
        winner, loser = authority_a, authority_b
        winner_level, loser_level = level_a, level_b
        winner_weight, loser_weight = weight_a, weight_b

    return {
        "prevailing_authority": winner,
        "prevailing_level": winner_level.value,
        "prevailing_weight": winner_weight,
        "subordinate_authority": loser,
        "subordinate_level": loser_level.value,
        "subordinate_weight": loser_weight,
        "weight_differential": round(abs(winner_weight - loser_weight), 4),
        "conflict_resolution_note": _generate_conflict_note(
            winner, winner_level, loser, loser_level
        ),
    }


def _lookup_authority_weight(source: str) -> float:
    """Look up the weight for an authority source."""
    source_upper = source.upper().replace(" ", "_").replace("§", "")
    for key, weight in AUTHORITY_WEIGHTS.items():
        if key in source_upper or source_upper in key:
            return weight
    level = classify_authority(source)
    level_defaults = {
        AuthorityLevel.CONSTITUTIONAL: 0.98,
        AuthorityLevel.STATUTORY: 0.90,
        AuthorityLevel.REGULATORY: 0.85,
        AuthorityLevel.ADMINISTRATIVE_RULING: 0.78,
        AuthorityLevel.FIELD_RULE: 0.82,
        AuthorityLevel.INDUSTRY_PRACTICE: 0.55,
        AuthorityLevel.ADVISORY: 0.50,
        AuthorityLevel.COMMENTARY: 0.40,
    }
    return level_defaults.get(level, 0.40)


def _generate_conflict_note(
    winner: str,
    winner_level: AuthorityLevel,
    loser: str,
    loser_level: AuthorityLevel,
) -> str:
    """Generate a human-readable conflict resolution explanation."""
    if winner_level == loser_level:
        return (
            f"Both '{winner}' and '{loser}' are at the {winner_level.value} level. "
            f"Prevailing authority selected by specificity weight. "
            f"Field-specific rules supersede statewide rules within their jurisdiction."
        )
    return (
        f"'{winner}' ({winner_level.value}) prevails over '{loser}' ({loser_level.value}). "
        f"Higher-level authorities control unless a specific statutory delegation exists. "
        f"Field rules adopted by RRC order have regulatory force within their fields."
    )


# ==============================================================================
# TIE COMPONENT 5: CONFIDENCE STRATIFICATION
# ==============================================================================


class ConfidenceTier(str, Enum):
    """Confidence stratification tiers for spacing analysis."""
    DEFENSIBLE = "defensible"
    AGGRESSIVE = "aggressive"
    DISCLOSURE = "disclosure"
    HIGH_RISK = "high_risk"


CONFIDENCE_THRESHOLDS: Dict[ConfidenceTier, Tuple[float, float]] = {
    ConfidenceTier.DEFENSIBLE: (0.85, 1.00),
    ConfidenceTier.AGGRESSIVE: (0.70, 0.849),
    ConfidenceTier.DISCLOSURE: (0.50, 0.699),
    ConfidenceTier.HIGH_RISK: (0.00, 0.499),
}

CONFIDENCE_DESCRIPTIONS: Dict[ConfidenceTier, str] = {
    ConfidenceTier.DEFENSIBLE: (
        "Position supported by clear statewide rule, established field rules, "
        "or direct RRC precedent. High confidence in regulatory compliance."
    ),
    ConfidenceTier.AGGRESSIVE: (
        "Position based on reasonable interpretation of spacing rules but may face "
        "challenge from offset operators or RRC staff. Exception application may be required."
    ),
    ConfidenceTier.DISCLOSURE: (
        "Position requires disclosure of uncertainty. Field-specific rules may differ from "
        "statewide rules. Recommend confirming with RRC field office before drilling."
    ),
    ConfidenceTier.HIGH_RISK: (
        "Significant uncertainty about spacing compliance. Multiple interpretations possible. "
        "Strong recommendation to obtain RRC ruling or legal opinion before proceeding."
    ),
}


def stratify_confidence(score: float) -> Dict[str, Any]:
    """Classify a confidence score into a stratification tier with metadata."""
    for tier, (low, high) in CONFIDENCE_THRESHOLDS.items():
        if low <= score <= high:
            return {
                "tier": tier.value,
                "score": round(score, 4),
                "range": f"{low:.2f}-{high:.2f}",
                "description": CONFIDENCE_DESCRIPTIONS[tier],
                "requires_disclosure": tier in (
                    ConfidenceTier.DISCLOSURE,
                    ConfidenceTier.HIGH_RISK,
                ),
                "requires_field_verification": tier in (
                    ConfidenceTier.AGGRESSIVE,
                    ConfidenceTier.DISCLOSURE,
                    ConfidenceTier.HIGH_RISK,
                ),
            }
    return {
        "tier": ConfidenceTier.HIGH_RISK.value,
        "score": round(score, 4),
        "range": "0.00-0.499",
        "description": CONFIDENCE_DESCRIPTIONS[ConfidenceTier.HIGH_RISK],
        "requires_disclosure": True,
        "requires_field_verification": True,
    }


# ==============================================================================
# EPISTEMIC GUARDRAILS - Banned Phrases
# ==============================================================================

BANNED_PHRASES: List[str] = [
    "guaranteed compliance",
    "definitely legal",
    "no risk",
    "always permitted",
    "never requires",
    "100% certain",
    "guaranteed to be approved",
    "no exception needed",
    "always compliant",
    "cannot be denied",
    "will always pass",
    "absolute certainty",
    "impossible to fail",
    "guaranteed approval",
    "no need to verify",
    "skip the hearing",
    "ignore field rules",
    "field rules don't apply",
    "no offset notice required",
    "correlative rights don't matter",
    "RRC will always approve",
    "no protest possible",
    "drainage is irrelevant",
    "the law is clear on this",
    "this is black and white",
    "no ambiguity exists",
]


def apply_epistemic_guardrails(text: str) -> Dict[str, Any]:
    """Check text for banned phrases and apply epistemic guardrails."""
    violations: List[str] = []
    text_lower = text.lower()
    for phrase in BANNED_PHRASES:
        if phrase in text_lower:
            violations.append(phrase)

    if violations:
        logger.warning(f"Epistemic guardrail violations: {violations}")
    return {
        "passed": len(violations) == 0,
        "violations": violations,
        "violation_count": len(violations),
        "disclosure_caveat": (
            "Analysis is based on general statewide rules and available field rules. "
            "Specific field rules, pending RRC orders, or recent docket decisions may "
            "modify applicable spacing requirements. Consult RRC records and obtain "
            "legal review before committing capital to drill."
        ) if violations else None,
    }


# ==============================================================================
# TIE COMPONENT 13: ZONED ANALYSIS
# ==============================================================================


class AnalysisZone(str, Enum):
    """Distinct analysis zones - never blurred."""
    PLANNING = "planning"
    REPORTING = "reporting"
    AUDIT = "audit"


ZONE_CONSTRAINTS: Dict[AnalysisZone, Dict[str, Any]] = {
    AnalysisZone.PLANNING: {
        "description": "Pre-drilling planning and permit application analysis",
        "allowed_actions": [
            "evaluate_spacing_compliance",
            "identify_exception_requirements",
            "assess_field_rules",
            "calculate_setback_distances",
            "review_pooling_options",
            "determine_permit_requirements",
        ],
        "prohibited_actions": [
            "certify_compliance",
            "issue_legal_opinion",
            "approve_permit",
        ],
        "output_label": "PLANNING ANALYSIS - Not a compliance certification",
        "requires_field_verification": True,
    },
    AnalysisZone.REPORTING: {
        "description": "Production reporting and regulatory compliance tracking",
        "allowed_actions": [
            "verify_spacing_as_drilled",
            "check_unit_acreage",
            "validate_proration_assignment",
            "confirm_permit_conditions_met",
            "review_field_rule_compliance",
        ],
        "prohibited_actions": [
            "modify_permit_conditions",
            "waive_spacing_requirements",
            "approve_exception",
        ],
        "output_label": "REPORTING ANALYSIS - Verify with RRC records",
        "requires_field_verification": False,
    },
    AnalysisZone.AUDIT: {
        "description": "Regulatory audit and enforcement action analysis",
        "allowed_actions": [
            "reconstruct_spacing_history",
            "assess_violation_exposure",
            "calculate_penalty_risk",
            "identify_remediation_options",
            "evaluate_exception_validity",
            "review_hearing_record",
        ],
        "prohibited_actions": [
            "conceal_violations",
            "minimize_penalty_exposure",
            "advise_non_compliance",
        ],
        "output_label": "AUDIT ANALYSIS - Privileged and confidential",
        "requires_field_verification": True,
    },
}


def determine_zone(question: str, mode: str) -> AnalysisZone:
    """Determine the appropriate analysis zone from query context."""
    q_lower = question.lower()

    audit_indicators = [
        "audit", "violation", "penalty", "enforcement", "hearing",
        "docket", "compliance review", "inspection", "fine", "remediation",
        "plugging order", "show cause",
    ]
    reporting_indicators = [
        "report", "p-4", "production report", "as-drilled", "completion",
        "allowable", "allocation", "proration", "unit assignment",
        "monthly production", "annual report",
    ]
    planning_indicators = [
        "plan", "permit", "drill", "where can", "how far", "setback",
        "exception", "spacing", "density", "pooling", "can I drill",
        "proposed well", "new well", "development plan", "pad",
    ]

    if any(ind in q_lower for ind in audit_indicators):
        return AnalysisZone.AUDIT
    if any(ind in q_lower for ind in reporting_indicators):
        return AnalysisZone.REPORTING
    if any(ind in q_lower for ind in planning_indicators):
        return AnalysisZone.PLANNING

    if mode == "defense":
        return AnalysisZone.AUDIT
    return AnalysisZone.PLANNING


# ==============================================================================
# TIE COMPONENT 14: FACT FRAGILITY SCORING
# ==============================================================================


def score_fact_fragility(
    doctrine: DoctrineBlock,
    question: str,
) -> Dict[str, Any]:
    """Score the fragility of facts underlying a spacing doctrine response."""
    verifiability = _score_verifiability(doctrine)
    recharacterization_risk = _score_recharacterization_risk(doctrine, question)
    testimony_dependence = _score_testimony_dependence(doctrine)
    field_rule_volatility = _score_field_rule_volatility(doctrine)

    composite = round(
        (verifiability * 0.30)
        + (recharacterization_risk * 0.25)
        + (testimony_dependence * 0.20)
        + (field_rule_volatility * 0.25),
        4,
    )

    return {
        "composite_fragility": composite,
        "verifiability": round(verifiability, 4),
        "recharacterization_risk": round(recharacterization_risk, 4),
        "testimony_dependence": round(testimony_dependence, 4),
        "field_rule_volatility": round(field_rule_volatility, 4),
        "fragility_assessment": _fragility_label(composite),
        "mitigation_recommendations": _fragility_mitigations(
            verifiability, recharacterization_risk,
            testimony_dependence, field_rule_volatility,
        ),
    }


def _score_verifiability(doctrine: DoctrineBlock) -> float:
    """Score how verifiable the underlying facts are (0=hard to verify, 1=easily verified)."""
    score = 0.5
    authority_count = len(doctrine.primary_authority)
    if authority_count >= 3:
        score += 0.25
    elif authority_count >= 2:
        score += 0.15
    elif authority_count >= 1:
        score += 0.05

    has_regulatory_cite = any(
        term in auth.upper()
        for auth in doctrine.primary_authority
        for term in ["TAC", "NRC", "NATURAL RESOURCES CODE", "STATEWIDE"]
    )
    if has_regulatory_cite:
        score += 0.15

    if doctrine.controlling_precedent:
        score += 0.10

    return min(score, 1.0)


def _score_recharacterization_risk(doctrine: DoctrineBlock, question: str) -> float:
    """Score the risk that facts could be recharacterized (0=low risk, 1=high risk)."""
    score = 0.3
    q_lower = question.lower()

    ambiguity_terms = [
        "exception", "variance", "reasonable", "undue hardship",
        "good cause", "may", "discretion", "judgment", "interpret",
    ]
    ambiguity_hits = sum(1 for term in ambiguity_terms if term in q_lower)
    score += min(ambiguity_hits * 0.08, 0.40)

    if len(doctrine.counter_arguments) >= 3:
        score += 0.15
    elif len(doctrine.counter_arguments) >= 1:
        score += 0.08

    if "field" in q_lower or "special" in q_lower:
        score += 0.10

    return min(score, 1.0)


def _score_testimony_dependence(doctrine: DoctrineBlock) -> float:
    """Score dependence on testimony vs. documentary evidence (0=documentary, 1=testimony)."""
    score = 0.2
    testimony_terms = [
        "hearing", "testimony", "witness", "expert opinion", "engineer",
        "geologist", "reservoir", "estimate", "projection",
    ]
    framework_lower = doctrine.reasoning_framework.lower()
    hits = sum(1 for term in testimony_terms if term in framework_lower)
    score += min(hits * 0.10, 0.50)

    resolution_lower = doctrine.resolution_strategy.lower()
    if "hearing" in resolution_lower:
        score += 0.15
    if "expert" in resolution_lower or "engineer" in resolution_lower:
        score += 0.10

    return min(score, 1.0)


def _score_field_rule_volatility(doctrine: DoctrineBlock) -> float:
    """Score how likely the applicable field rule is to change (0=stable, 1=volatile)."""
    score = 0.2
    topic_lower = doctrine.topic.lower()

    if "field" in topic_lower or "special" in topic_lower:
        score += 0.30
    if "horizontal" in topic_lower:
        score += 0.20
    if "urban" in topic_lower:
        score += 0.25
    if "statewide" in topic_lower or "rule 37" in topic_lower or "rule 38" in topic_lower:
        score -= 0.10

    return max(min(score, 1.0), 0.0)


def _fragility_label(composite: float) -> str:
    """Assign a human-readable fragility label."""
    if composite < 0.30:
        return "LOW - Well-established regulatory framework with clear authority"
    if composite < 0.55:
        return "MODERATE - Established rules but field-specific variation possible"
    if composite < 0.75:
        return "ELEVATED - Significant interpretation required, field rules may differ"
    return "HIGH - Multiple competing interpretations, RRC discretion dominates"


def _fragility_mitigations(
    verifiability: float,
    recharacterization: float,
    testimony: float,
    volatility: float,
) -> List[str]:
    """Generate mitigation recommendations based on fragility scores."""
    mitigations: List[str] = []
    if verifiability < 0.50:
        mitigations.append(
            "Obtain certified copies of applicable field rules from RRC"
        )
        mitigations.append(
            "Verify current spacing requirements with RRC district office"
        )
    if recharacterization > 0.50:
        mitigations.append(
            "Document factual basis for exception application thoroughly"
        )
        mitigations.append(
            "Prepare for potential offset operator protests and RRC hearing"
        )
    if testimony > 0.50:
        mitigations.append(
            "Retain qualified petroleum engineer for spacing testimony"
        )
        mitigations.append(
            "Prepare engineering exhibits showing no drainage impact"
        )
    if volatility > 0.50:
        mitigations.append(
            "Monitor RRC docket for pending field rule amendments"
        )
        mitigations.append(
            "Consider whether proposed rule changes affect development timing"
        )
    if not mitigations:
        mitigations.append("Standard due diligence - confirm with current RRC records")
    return mitigations


# ==============================================================================
# TIE COMPONENT 19: MULTI-DOCTRINE DECOMPOSITION
# ==============================================================================


class IssueCategory(str, Enum):
    """Issue categories for multi-doctrine decomposition."""
    LEASE_LINE_SPACING = "lease_line_spacing"
    BETWEEN_WELL_SPACING = "between_well_spacing"
    DENSITY_PRORATION = "density_proration"
    HORIZONTAL_SPACING = "horizontal_spacing"
    POOLING_UNITIZATION = "pooling_unitization"
    CORRELATIVE_RIGHTS = "correlative_rights"
    SPECIAL_FIELD_RULES = "special_field_rules"
    URBAN_DRILLING = "urban_drilling"
    EXCEPTION_APPLICATION = "exception_application"
    DRILLING_PERMIT = "drilling_permit"
    STACKED_LATERAL = "stacked_lateral"
    DIAGONAL_RULE = "diagonal_rule"


INTERACTION_EDGES: List[Dict[str, Any]] = [
    {
        "from": IssueCategory.LEASE_LINE_SPACING.value,
        "to": IssueCategory.CORRELATIVE_RIGHTS.value,
        "relationship": "Lease line spacing exists to protect correlative rights of adjacent mineral owners",
        "strength": 0.95,
    },
    {
        "from": IssueCategory.LEASE_LINE_SPACING.value,
        "to": IssueCategory.EXCEPTION_APPLICATION.value,
        "relationship": "Operators unable to meet lease line setbacks must apply for Rule 37 exception",
        "strength": 0.92,
    },
    {
        "from": IssueCategory.BETWEEN_WELL_SPACING.value,
        "to": IssueCategory.DENSITY_PRORATION.value,
        "relationship": "Between-well spacing controls density within a proration unit",
        "strength": 0.90,
    },
    {
        "from": IssueCategory.DENSITY_PRORATION.value,
        "to": IssueCategory.DRILLING_PERMIT.value,
        "relationship": "Density exceptions require RRC approval as part of drilling permit process",
        "strength": 0.88,
    },
    {
        "from": IssueCategory.HORIZONTAL_SPACING.value,
        "to": IssueCategory.DIAGONAL_RULE.value,
        "relationship": "Horizontal wells use diagonal rule for property line setback measurement",
        "strength": 0.93,
    },
    {
        "from": IssueCategory.HORIZONTAL_SPACING.value,
        "to": IssueCategory.STACKED_LATERAL.value,
        "relationship": "Stacked laterals require vertical separation plus horizontal spacing compliance",
        "strength": 0.88,
    },
    {
        "from": IssueCategory.HORIZONTAL_SPACING.value,
        "to": IssueCategory.SPECIAL_FIELD_RULES.value,
        "relationship": "Most horizontal plays have field-specific spacing rules superseding statewide rules",
        "strength": 0.91,
    },
    {
        "from": IssueCategory.POOLING_UNITIZATION.value,
        "to": IssueCategory.CORRELATIVE_RIGHTS.value,
        "relationship": "Pooling is the mechanism to protect correlative rights when mineral interests are fragmented",
        "strength": 0.94,
    },
    {
        "from": IssueCategory.POOLING_UNITIZATION.value,
        "to": IssueCategory.LEASE_LINE_SPACING.value,
        "relationship": "Pooled units may modify effective lease lines for spacing purposes",
        "strength": 0.85,
    },
    {
        "from": IssueCategory.URBAN_DRILLING.value,
        "to": IssueCategory.LEASE_LINE_SPACING.value,
        "relationship": "Urban drilling imposes additional surface setbacks beyond RRC spacing rules",
        "strength": 0.87,
    },
    {
        "from": IssueCategory.URBAN_DRILLING.value,
        "to": IssueCategory.HORIZONTAL_SPACING.value,
        "relationship": "Urban drilling commonly uses horizontal wells to access minerals from pad sites",
        "strength": 0.86,
    },
    {
        "from": IssueCategory.SPECIAL_FIELD_RULES.value,
        "to": IssueCategory.DENSITY_PRORATION.value,
        "relationship": "Field rules specify field-specific proration units and density limits",
        "strength": 0.90,
    },
    {
        "from": IssueCategory.SPECIAL_FIELD_RULES.value,
        "to": IssueCategory.LEASE_LINE_SPACING.value,
        "relationship": "Field rules may modify statewide lease line and between-well spacing requirements",
        "strength": 0.91,
    },
    {
        "from": IssueCategory.EXCEPTION_APPLICATION.value,
        "to": IssueCategory.DRILLING_PERMIT.value,
        "relationship": "Exception approval is prerequisite to drilling permit issuance for non-conforming locations",
        "strength": 0.95,
    },
    {
        "from": IssueCategory.CORRELATIVE_RIGHTS.value,
        "to": IssueCategory.EXCEPTION_APPLICATION.value,
        "relationship": "Correlative rights of offset operators are primary consideration in exception hearings",
        "strength": 0.93,
    },
    {
        "from": IssueCategory.STACKED_LATERAL.value,
        "to": IssueCategory.DENSITY_PRORATION.value,
        "relationship": "Stacked laterals in different zones may each require density exceptions",
        "strength": 0.86,
    },
    {
        "from": IssueCategory.DIAGONAL_RULE.value,
        "to": IssueCategory.LEASE_LINE_SPACING.value,
        "relationship": "Diagonal rule measures perpendicular distance from lateral to nearest lease line",
        "strength": 0.92,
    },
]


def decompose_issues(question: str, matched_doctrines: List[DoctrineBlock]) -> Dict[str, Any]:
    """Decompose a complex spacing question into issue categories with interaction analysis."""
    q_lower = question.lower()
    detected_categories: List[Dict[str, Any]] = []

    category_indicators: Dict[IssueCategory, List[str]] = {
        IssueCategory.LEASE_LINE_SPACING: [
            "lease line", "property line", "setback", "467", "330",
        ],
        IssueCategory.BETWEEN_WELL_SPACING: [
            "between well", "inter-well", "1200", "660", "well-to-well",
        ],
        IssueCategory.DENSITY_PRORATION: [
            "density", "proration", "allowable", "40 acres", "640 acres", "downspacing",
        ],
        IssueCategory.HORIZONTAL_SPACING: [
            "horizontal", "lateral", "multi-lateral", "pad",
        ],
        IssueCategory.POOLING_UNITIZATION: [
            "pooling", "unitization", "unit", "unleased", "mineral interest",
        ],
        IssueCategory.CORRELATIVE_RIGHTS: [
            "correlative", "drainage", "offset", "confiscation", "protect",
        ],
        IssueCategory.SPECIAL_FIELD_RULES: [
            "field rule", "special rule", "field-specific", "permian", "eagle ford",
            "barnett", "haynesville", "spraberry", "wolfcamp",
        ],
        IssueCategory.URBAN_DRILLING: [
            "urban", "city", "municipal", "ordinance", "protected use",
        ],
        IssueCategory.EXCEPTION_APPLICATION: [
            "exception", "variance", "rule 37 exception", "hardship",
        ],
        IssueCategory.DRILLING_PERMIT: [
            "permit", "w-1", "drilling permit", "application",
        ],
        IssueCategory.STACKED_LATERAL: [
            "stacked", "stacked lateral", "multi-zone", "vertically",
        ],
        IssueCategory.DIAGONAL_RULE: [
            "diagonal", "perpendicular", "diagonal rule",
        ],
    }

    for category, indicators in category_indicators.items():
        matched_indicators = [ind for ind in indicators if ind in q_lower]
        if matched_indicators:
            detected_categories.append({
                "category": category.value,
                "matched_indicators": matched_indicators,
                "confidence": min(0.50 + len(matched_indicators) * 0.15, 0.95),
            })

    for doctrine in matched_doctrines:
        topic_lower = doctrine.topic.lower()
        for category, indicators in category_indicators.items():
            if any(ind in topic_lower for ind in indicators):
                already_present = any(
                    dc["category"] == category.value for dc in detected_categories
                )
                if not already_present:
                    detected_categories.append({
                        "category": category.value,
                        "matched_indicators": [f"doctrine:{doctrine.topic}"],
                        "confidence": doctrine.confidence * 0.8,
                    })

    detected_category_values = {dc["category"] for dc in detected_categories}
    relevant_edges = [
        edge for edge in INTERACTION_EDGES
        if edge["from"] in detected_category_values or edge["to"] in detected_category_values
    ]

    strata = _build_issue_strata(detected_categories, relevant_edges)

    return {
        "detected_categories": detected_categories,
        "category_count": len(detected_categories),
        "interaction_edges": relevant_edges,
        "edge_count": len(relevant_edges),
        "strata": strata,
        "complexity_score": _calculate_complexity(detected_categories, relevant_edges),
        "recommended_analysis_depth": (
            "deep" if len(detected_categories) >= 3
            else "standard" if len(detected_categories) >= 2
            else "focused"
        ),
    }


def _build_issue_strata(
    categories: List[Dict[str, Any]],
    edges: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Build strata (layers) of issue resolution order."""
    if not categories:
        return []

    category_deps: Dict[str, List[str]] = {}
    for cat in categories:
        category_deps[cat["category"]] = []

    cat_set = {c["category"] for c in categories}
    for edge in edges:
        if edge["from"] in cat_set and edge["to"] in cat_set:
            category_deps.setdefault(edge["to"], []).append(edge["from"])

    resolved: set = set()
    strata: List[Dict[str, Any]] = []
    remaining = set(category_deps.keys())
    level = 0

    while remaining:
        current_stratum = []
        for cat in list(remaining):
            deps = category_deps.get(cat, [])
            if all(d in resolved or d not in remaining for d in deps):
                current_stratum.append(cat)
        if not current_stratum:
            current_stratum = list(remaining)
        for cat in current_stratum:
            remaining.discard(cat)
            resolved.add(cat)
        strata.append({
            "level": level,
            "categories": current_stratum,
            "description": f"Resolve these issues at stratum {level} before proceeding",
        })
        level += 1

    return strata


def _calculate_complexity(
    categories: List[Dict[str, Any]],
    edges: List[Dict[str, Any]],
) -> float:
    """Calculate a complexity score for the multi-doctrine decomposition."""
    cat_count = len(categories)
    edge_count = len(edges)
    if cat_count == 0:
        return 0.0
    avg_edge_strength = (
        sum(e["strength"] for e in edges) / edge_count if edge_count > 0 else 0.0
    )
    raw_score = (cat_count * 0.20) + (edge_count * 0.10) + (avg_edge_strength * 0.30)
    return round(min(raw_score, 1.0), 4)


# ==============================================================================
# TIE COMPONENT 11: METRICS COLLECTOR
# ==============================================================================


class MetricsCollector:
    """Lightweight metrics for operational awareness. No external dependencies."""

    def __init__(self) -> None:
        self.latencies: List[float] = []
        self.errors: List[float] = []
        self.queries: List[float] = []
        self.doctrine_hits: int = 0
        self.doctrine_misses: int = 0
        self.last_error: Optional[str] = None
        self.active_queries: int = 0
        self._max_latencies: int = 200
        self.zone_counts: Dict[str, int] = {z.value: 0 for z in AnalysisZone}
        self.tier_counts: Dict[str, int] = {t.value: 0 for t in ConfidenceTier}
        self.mode_counts: Dict[str, int] = {"fast": 0, "defense": 0, "memo": 0}
        self.total_queries: int = 0

    def record_query(
        self,
        latency_ms: float,
        doctrine_hit: bool,
        zone: Optional[str] = None,
        tier: Optional[str] = None,
        mode: Optional[str] = None,
    ) -> None:
        """Record a completed query with full metadata."""
        now = time.time()
        self.latencies.append(latency_ms)
        if len(self.latencies) > self._max_latencies:
            self.latencies.pop(0)
        self.queries.append(now)
        cutoff = now - 3600
        self.queries = [t for t in self.queries if t > cutoff]
        self.total_queries += 1
        if doctrine_hit:
            self.doctrine_hits += 1
        else:
            self.doctrine_misses += 1
        if zone and zone in self.zone_counts:
            self.zone_counts[zone] += 1
        if tier and tier in self.tier_counts:
            self.tier_counts[tier] += 1
        if mode and mode in self.mode_counts:
            self.mode_counts[mode] += 1

    def record_error(self, error_msg: str) -> None:
        """Record an error occurrence."""
        self.errors.append(time.time())
        self.last_error = f"{datetime.now(timezone.utc).isoformat()}: {error_msg[:200]}"
        cutoff = time.time() - 86400
        self.errors = [t for t in self.errors if t > cutoff]

    def query_start(self) -> None:
        self.active_queries += 1

    def query_end(self) -> None:
        self.active_queries = max(0, self.active_queries - 1)

    def get_latency_stats(self) -> Dict[str, float]:
        if not self.latencies:
            return {"avg_ms": 0.0, "p50_ms": 0.0, "p95_ms": 0.0, "p99_ms": 0.0, "last_ms": 0.0}
        sorted_lat = sorted(self.latencies)
        n = len(sorted_lat)
        return {
            "avg_ms": round(sum(self.latencies) / n, 2),
            "p50_ms": round(sorted_lat[int(n * 0.50)], 2),
            "p95_ms": round(sorted_lat[min(int(n * 0.95), n - 1)], 2),
            "p99_ms": round(sorted_lat[min(int(n * 0.99), n - 1)], 2),
            "last_ms": round(self.latencies[-1], 2),
        }

    def get_error_stats(self) -> Dict[str, Any]:
        now = time.time()
        return {
            "last_hour": sum(1 for t in self.errors if t > now - 3600),
            "last_24h": len(self.errors),
            "last_error": self.last_error,
        }

    def get_doctrine_hit_rate(self) -> float:
        total = self.doctrine_hits + self.doctrine_misses
        return round(self.doctrine_hits / total, 4) if total > 0 else 1.0

    def queries_last_hour(self) -> int:
        return sum(1 for t in self.queries if t > time.time() - 3600)

    def get_full_metrics(self) -> Dict[str, Any]:
        """Return comprehensive metrics snapshot."""
        return {
            "latency": self.get_latency_stats(),
            "errors": self.get_error_stats(),
            "doctrine_hit_rate": self.get_doctrine_hit_rate(),
            "queries_last_hour": self.queries_last_hour(),
            "total_queries": self.total_queries,
            "active_queries": self.active_queries,
            "zone_distribution": dict(self.zone_counts),
            "tier_distribution": dict(self.tier_counts),
            "mode_distribution": dict(self.mode_counts),
        }


_metrics = MetricsCollector()


def get_metrics() -> MetricsCollector:
    return _metrics


# ==============================================================================
# TIE COMPONENT 9: DRIFT WATCHER
# ==============================================================================


class DriftWatcher:
    """Monitors doctrine drift over time by tracking query patterns and outcomes."""

    def __init__(self) -> None:
        self.observations: List[Dict[str, Any]] = []
        self.drift_alerts: List[Dict[str, Any]] = []
        self._max_observations: int = 500
        self._drift_threshold: float = 0.15

    def observe(
        self,
        doctrine_topic: str,
        confidence: float,
        matched: bool,
        question_fragment: str,
    ) -> None:
        """Record a doctrine observation for drift analysis."""
        self.observations.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "topic": doctrine_topic,
            "confidence": confidence,
            "matched": matched,
            "question_fragment": question_fragment[:100],
        })
        if len(self.observations) > self._max_observations:
            self.observations.pop(0)
        self._check_drift(doctrine_topic)

    def _check_drift(self, topic: str) -> None:
        """Check if a doctrine topic is drifting from expected patterns."""
        topic_obs = [o for o in self.observations if o["topic"] == topic]
        if len(topic_obs) < 10:
            return

        recent = topic_obs[-10:]
        older = topic_obs[:-10] if len(topic_obs) > 10 else topic_obs[:5]
        if not older:
            return

        recent_conf = sum(o["confidence"] for o in recent) / len(recent)
        older_conf = sum(o["confidence"] for o in older) / len(older)
        confidence_delta = abs(recent_conf - older_conf)

        recent_match_rate = sum(1 for o in recent if o["matched"]) / len(recent)
        older_match_rate = sum(1 for o in older if o["matched"]) / max(len(older), 1)
        match_rate_delta = abs(recent_match_rate - older_match_rate)

        if confidence_delta > self._drift_threshold or match_rate_delta > self._drift_threshold:
            alert = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "topic": topic,
                "confidence_delta": round(confidence_delta, 4),
                "match_rate_delta": round(match_rate_delta, 4),
                "recent_confidence": round(recent_conf, 4),
                "older_confidence": round(older_conf, 4),
                "recent_match_rate": round(recent_match_rate, 4),
                "older_match_rate": round(older_match_rate, 4),
                "severity": "HIGH" if confidence_delta > 0.25 else "MODERATE",
                "recommendation": (
                    f"Review doctrine '{topic}' for potential regulatory changes or "
                    f"field rule updates. Confidence shifted by {confidence_delta:.2%}."
                ),
            }
            self.drift_alerts.append(alert)
            logger.warning(f"Drift detected for '{topic}': delta={confidence_delta:.4f}")

    def get_drift_report(self) -> Dict[str, Any]:
        """Generate a comprehensive drift report."""
        topic_stats: Dict[str, Dict[str, Any]] = {}
        for obs in self.observations:
            topic = obs["topic"]
            if topic not in topic_stats:
                topic_stats[topic] = {"count": 0, "total_conf": 0.0, "matches": 0}
            topic_stats[topic]["count"] += 1
            topic_stats[topic]["total_conf"] += obs["confidence"]
            if obs["matched"]:
                topic_stats[topic]["matches"] += 1

        summaries = []
        for topic, stats in topic_stats.items():
            summaries.append({
                "topic": topic,
                "observation_count": stats["count"],
                "avg_confidence": round(stats["total_conf"] / stats["count"], 4),
                "match_rate": round(stats["matches"] / stats["count"], 4),
            })

        return {
            "total_observations": len(self.observations),
            "active_alerts": len(self.drift_alerts),
            "alerts": self.drift_alerts[-20:],
            "topic_summaries": summaries,
            "drift_threshold": self._drift_threshold,
        }


_drift_watcher = DriftWatcher()


def get_drift_watcher() -> DriftWatcher:
    return _drift_watcher


# ==============================================================================
# TIE COMPONENT 10: COVERAGE MAP
# ==============================================================================


class CoverageMap:
    """Tracks doctrine coverage and identifies epistemic gaps."""

    def __init__(self, doctrines: List[DoctrineBlock]) -> None:
        self.doctrine_topics: List[str] = [d.topic for d in doctrines]
        self.triggered: Dict[str, int] = {d.topic: 0 for d in doctrines}
        self.missed_queries: List[Dict[str, Any]] = []
        self._max_missed: int = 200

    def record_hit(self, topic: str) -> None:
        """Record that a doctrine was triggered."""
        if topic in self.triggered:
            self.triggered[topic] += 1

    def record_miss(self, question: str, keywords: List[str]) -> None:
        """Record a query that missed all doctrines (epistemic gap)."""
        self.missed_queries.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "question": question[:200],
            "keywords": keywords[:10],
        })
        if len(self.missed_queries) > self._max_missed:
            self.missed_queries.pop(0)

    def get_coverage_report(self) -> Dict[str, Any]:
        """Generate a coverage report showing triggered vs untriggered doctrines."""
        total = len(self.doctrine_topics)
        triggered_count = sum(1 for count in self.triggered.values() if count > 0)
        untriggered = [topic for topic, count in self.triggered.items() if count == 0]
        most_triggered = sorted(
            self.triggered.items(), key=lambda x: x[1], reverse=True
        )[:10]

        keyword_freq: Dict[str, int] = {}
        for miss in self.missed_queries:
            for kw in miss.get("keywords", []):
                keyword_freq[kw] = keyword_freq.get(kw, 0) + 1
        gap_keywords = sorted(keyword_freq.items(), key=lambda x: x[1], reverse=True)[:15]

        return {
            "total_doctrines": total,
            "triggered_doctrines": triggered_count,
            "untriggered_doctrines": total - triggered_count,
            "coverage_percentage": round(
                (triggered_count / total * 100) if total > 0 else 0.0, 2
            ),
            "untriggered_topics": untriggered,
            "most_triggered": [
                {"topic": t, "count": c} for t, c in most_triggered
            ],
            "epistemic_gaps": {
                "total_missed_queries": len(self.missed_queries),
                "frequent_gap_keywords": [
                    {"keyword": kw, "frequency": freq} for kw, freq in gap_keywords
                ],
                "recent_misses": self.missed_queries[-10:],
            },
        }


_coverage_map = CoverageMap(DOCTRINE_CACHE)


def get_coverage_map() -> CoverageMap:
    return _coverage_map


# ==============================================================================
# TIE COMPONENT 2: RESPONSE MODES
# ==============================================================================


class ResponseMode(str, Enum):
    FAST = "fast"
    DEFENSE = "defense"
    MEMO = "memo"


# ==============================================================================
# TIE COMPONENT 15: AUDIT TRAIL (JSONL)
# ==============================================================================


def write_audit_entry(entry: Dict[str, Any]) -> None:
    """Append a single audit entry to the JSONL audit trail."""
    entry["_audit_timestamp"] = datetime.now(timezone.utc).isoformat()
    entry["_engine"] = ENGINE_NAME
    entry["_version"] = ENGINE_VERSION
    try:
        with open(AUDIT_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, default=str) + "\n")
    except Exception as exc:
        logger.error(f"Failed to write audit entry: {exc}")


def read_audit_trail(limit: int = 100) -> List[Dict[str, Any]]:
    """Read the most recent audit trail entries."""
    entries: List[Dict[str, Any]] = []
    if not AUDIT_LOG.exists():
        return entries
    try:
        with open(AUDIT_LOG, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for line in lines[-limit:]:
            line = line.strip()
            if line:
                entries.append(json.loads(line))
    except Exception as exc:
        logger.error(f"Failed to read audit trail: {exc}")
    return entries


# ==============================================================================
# TIE COMPONENT 16: DETERMINISM HASH (SHA-256)
# ==============================================================================


def compute_determinism_hash(
    question: str,
    doctrine_topic: str,
    confidence: float,
    mode: str,
    zone: str,
) -> str:
    """Compute SHA-256 determinism hash for response reproducibility."""
    hash_input = (
        f"R08|{question}|{doctrine_topic}|{confidence:.4f}|{mode}|{zone}|{ENGINE_VERSION}"
    )
    return hashlib.sha256(hash_input.encode("utf-8")).hexdigest()


# ==============================================================================
# PYDANTIC MODELS - Request / Response
# ==============================================================================


class SpacingQuery(BaseModel):
    """Query model for spacing analysis requests."""
    question: str = Field(..., min_length=10, description="The spacing question to analyze")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response mode")
    jurisdiction: str = Field(default="Texas", description="Applicable jurisdiction")
    field_name: Optional[str] = Field(default=None, description="Specific field name if known")
    well_type: Optional[str] = Field(default=None, description="vertical, horizontal, or directional")
    include_trace: bool = Field(default=False, description="Include telemetry trace in response")
    include_fragility: bool = Field(default=False, description="Include fact fragility scoring")
    include_decomposition: bool = Field(default=False, description="Include multi-doctrine decomposition")


class Citation(BaseModel):
    """Citation to an authority source."""
    authority: str
    reference: str
    relevance: str
    level: Optional[str] = None
    weight: Optional[float] = None


class SpacingResponse(BaseModel):
    """Full response model for spacing analysis."""
    query_id: str
    question: str
    mode: ResponseMode
    zone: str
    conclusion: str
    reasoning: str
    key_factors: List[str]
    citations: List[Citation]
    spacing_requirements: Optional[List[str]] = None
    exception_criteria: Optional[List[str]] = None
    pooling_options: Optional[List[str]] = None
    doctrine_match: bool
    confidence_tier: str
    confidence_stratification: Optional[Dict[str, Any]] = None
    response_layer: Literal["doctrine", "retrieval", "deep_analysis"]
    latency_ms: float
    determinism_hash: str
    limitations: List[str] = Field(default_factory=list)
    disclosure_caveat: Optional[str] = None
    fact_fragility: Optional[Dict[str, Any]] = None
    issue_decomposition: Optional[Dict[str, Any]] = None
    authority_chain: Optional[List[Dict[str, Any]]] = None
    timestamp: str
    version: str = ENGINE_VERSION


class HealthResponse(BaseModel):
    """Comprehensive health check response."""
    status: Literal["healthy", "degraded", "unhealthy"]
    engine: str
    version: str
    port: int
    domain: str
    uptime_seconds: float
    cloud_retriever_available: bool
    doctrine_cache: Dict[str, Any]
    metrics: Dict[str, Any]
    drift_summary: Dict[str, Any]
    coverage_summary: Dict[str, Any]
    telemetry_summary: Dict[str, Any]
    audit_trail_entries: int
    timestamp: str


# ==============================================================================
# INLINE SPACING NORMALIZATION
# ==============================================================================


def normalize_spacing_terms(text: str) -> str:
    """Apply spacing-domain-specific term normalization."""
    normalized = text.lower()
    for original, replacement in SPACING_TERM_NORMALIZATION.items():
        if original in normalized:
            normalized = normalized.replace(original, replacement)
    return normalized


# ==============================================================================
# TIE COMPONENT 1: THREE-LAYER RESPONSE
# ==============================================================================


def three_layer_response(
    query: SpacingQuery,
    normalized: NormalizationResult,
    trace_id: str,
) -> SpacingResponse:
    """
    Three-layer response architecture:
        Layer 1: Doctrine Cache (0-200ms) - Pre-compiled expert reasoning
        Layer 2: Semantic Retrieval (200-700ms) - Vector search on cache miss
        Layer 3: Deep Analysis (on-demand) - Multi-source synthesis
    """
    start_time = time.time()
    metrics = get_metrics()
    drift = get_drift_watcher()
    coverage = get_coverage_map()
    metrics.query_start()

    zone = determine_zone(query.question, query.mode.value)
    zone_meta = ZONE_CONSTRAINTS[zone]

    spacing_normalized = normalize_spacing_terms(normalized.normalized_text)

    try:
        # LAYER 1: Doctrine Cache
        matched_doctrines = match_doctrines(spacing_normalized, normalized.keywords)

        if matched_doctrines:
            primary = matched_doctrines[0]
            logger.info(
                f"[{trace_id}] Layer 1 HIT: {len(matched_doctrines)} doctrines, "
                f"primary='{primary.topic}'"
            )

            coverage.record_hit(primary.topic)
            drift.observe(primary.topic, primary.confidence, True, query.question[:80])

            response = _build_doctrine_response(
                query, matched_doctrines, trace_id, start_time, zone
            )

            conf_strat = stratify_confidence(primary.confidence)
            metrics.record_query(
                response.latency_ms, True,
                zone=zone.value, tier=conf_strat["tier"], mode=query.mode.value,
            )
            metrics.query_end()

            write_audit_entry({
                "trace_id": trace_id,
                "layer": "doctrine",
                "question": query.question[:200],
                "doctrine_topic": primary.topic,
                "confidence": primary.confidence,
                "tier": conf_strat["tier"],
                "zone": zone.value,
                "mode": query.mode.value,
                "latency_ms": response.latency_ms,
            })

            return response

        # LAYER 2: Semantic / Vector Retrieval
        logger.info(f"[{trace_id}] Layer 1 MISS. Attempting vector retrieval.")
        search_results = vector_search(spacing_normalized, top_k=5)

        if _cloud_available and _cloud_retriever is not None and not search_results:
            try:
                cloud_results = _cloud_retriever.search(spacing_normalized, top_k=5)
                if cloud_results:
                    search_results = cloud_results
                    logger.info(f"[{trace_id}] Cloud retriever returned {len(cloud_results)} results")
            except Exception as cloud_exc:
                logger.warning(f"[{trace_id}] Cloud retriever failed: {cloud_exc}")

        if search_results:
            logger.info(f"[{trace_id}] Layer 2 HIT: {len(search_results)} results")
            coverage.record_miss(query.question, normalized.keywords)
            response = _build_retrieval_response(
                query, search_results, trace_id, start_time, zone
            )
            metrics.record_query(
                response.latency_ms, False,
                zone=zone.value, mode=query.mode.value,
            )
            metrics.query_end()

            write_audit_entry({
                "trace_id": trace_id,
                "layer": "retrieval",
                "question": query.question[:200],
                "result_count": len(search_results),
                "zone": zone.value,
                "mode": query.mode.value,
                "latency_ms": response.latency_ms,
            })

            return response

        # LAYER 3: Deep Analysis
        logger.info(f"[{trace_id}] Layer 2 MISS. Entering deep analysis.")
        coverage.record_miss(query.question, normalized.keywords)
        response = _build_deep_analysis_response(
            query, trace_id, start_time, zone, normalized
        )
        metrics.record_query(
            response.latency_ms, False,
            zone=zone.value, mode=query.mode.value,
        )
        metrics.query_end()

        write_audit_entry({
            "trace_id": trace_id,
            "layer": "deep_analysis",
            "question": query.question[:200],
            "zone": zone.value,
            "mode": query.mode.value,
            "latency_ms": response.latency_ms,
        })

        return response

    except Exception as exc:
        metrics.record_error(str(exc))
        metrics.query_end()
        log_error(trace_id, ErrorDomain.QUERY_PROCESSING, str(exc))
        logger.error(f"[{trace_id}] Three-layer response failed: {exc}")
        raise


# ==============================================================================
# RESPONSE BUILDERS
# ==============================================================================


def _build_doctrine_response(
    query: SpacingQuery,
    doctrines: List[DoctrineBlock],
    trace_id: str,
    start_time: float,
    zone: AnalysisZone,
) -> SpacingResponse:
    """Build response from doctrine cache hit (Layer 1)."""
    primary = doctrines[0]

    conclusion = _format_conclusion(primary, query, zone)
    reasoning = _format_reasoning(primary, query, zone, doctrines)
    key_factors = _extract_key_factors(primary, query)

    citations = _build_citations(primary, doctrines)

    spacing_requirements = [
        f for f in primary.key_factors
        if any(kw in f.lower() for kw in [
            "feet", "ft", "acres", "distance", "spacing", "setback",
        ])
    ]

    exception_criteria = [
        f for f in primary.key_factors
        if any(kw in f.lower() for kw in [
            "exception", "variance", "hardship", "application",
        ])
    ]

    pooling_options = []
    for doctrine in doctrines:
        if "pooling" in doctrine.topic.lower():
            pooling_options = [
                "Voluntary pooling by written agreement among mineral owners",
                "Forced pooling under Texas Natural Resources Code Chapter 102",
                "Pooling designations in original lease provisions",
                "RRC-approved pooling as condition of spacing exception",
            ]
            break

    conf_strat = stratify_confidence(primary.confidence)
    determinism = compute_determinism_hash(
        query.question, primary.topic, primary.confidence,
        query.mode.value, zone.value,
    )

    guardrail_check = apply_epistemic_guardrails(conclusion + " " + reasoning)

    authority_chain = _build_authority_chain(primary, doctrines)

    fragility = None
    if query.include_fragility:
        fragility = score_fact_fragility(primary, query.question)

    decomposition = None
    if query.include_decomposition:
        decomposition = decompose_issues(query.question, doctrines)

    latency_ms = round((time.time() - start_time) * 1000, 2)

    limitations = _build_limitations(primary, zone, conf_strat)

    return SpacingResponse(
        query_id=trace_id,
        question=query.question,
        mode=query.mode,
        zone=zone.value,
        conclusion=conclusion,
        reasoning=reasoning,
        key_factors=key_factors,
        citations=citations,
        spacing_requirements=spacing_requirements if spacing_requirements else None,
        exception_criteria=exception_criteria if exception_criteria else None,
        pooling_options=pooling_options if pooling_options else None,
        doctrine_match=True,
        confidence_tier=conf_strat["tier"],
        confidence_stratification=conf_strat,
        response_layer="doctrine",
        latency_ms=latency_ms,
        determinism_hash=determinism,
        limitations=limitations,
        disclosure_caveat=guardrail_check.get("disclosure_caveat"),
        fact_fragility=fragility,
        issue_decomposition=decomposition,
        authority_chain=authority_chain,
        timestamp=datetime.now(timezone.utc).isoformat(),
        version=ENGINE_VERSION,
    )


def _build_retrieval_response(
    query: SpacingQuery,
    results: List[Dict[str, Any]],
    trace_id: str,
    start_time: float,
    zone: AnalysisZone,
) -> SpacingResponse:
    """Build response from vector/semantic retrieval (Layer 2)."""
    top_result = results[0]

    conclusion = (
        f"Spacing analysis based on semantic retrieval: "
        f"{top_result.get('content', 'Relevant spacing provisions identified')}. "
        f"This analysis is based on {len(results)} matched provisions and should be "
        f"verified against current RRC field rules."
    )

    reasoning_parts = [
        f"Semantic retrieval matched {len(results)} spacing-related provisions.",
        f"Top result relevance score: {top_result.get('score', 0.0):.3f}.",
    ]
    if query.field_name:
        reasoning_parts.append(
            f"Field-specific search for '{query.field_name}' may yield additional rules."
        )
    reasoning = " ".join(reasoning_parts)

    key_factors = [
        "Spacing requirements identified via semantic search",
        f"Top relevance score: {top_result.get('score', 0.0):.3f}",
        f"Analysis zone: {zone.value}",
        "Verify with RRC district office for field-specific rules",
    ]

    citations = [
        Citation(
            authority="Spacing Provision",
            reference=result.get("source", "Knowledge Base"),
            relevance=f"Relevance: {result.get('score', 0.0):.3f}",
            level="regulatory",
            weight=result.get("score", 0.5),
        )
        for result in results[:3]
    ]

    determinism = compute_determinism_hash(
        query.question, "retrieval", 0.60, query.mode.value, zone.value,
    )

    latency_ms = round((time.time() - start_time) * 1000, 2)

    return SpacingResponse(
        query_id=trace_id,
        question=query.question,
        mode=query.mode,
        zone=zone.value,
        conclusion=conclusion,
        reasoning=reasoning,
        key_factors=key_factors,
        citations=citations,
        doctrine_match=False,
        confidence_tier=ConfidenceTier.DISCLOSURE.value,
        confidence_stratification=stratify_confidence(0.60),
        response_layer="retrieval",
        latency_ms=latency_ms,
        determinism_hash=determinism,
        limitations=[
            "Response based on semantic retrieval, not pre-compiled doctrine",
            "Field-specific rules may differ from general provisions",
            "Verify spacing requirements with RRC before drilling",
        ],
        disclosure_caveat=(
            "This analysis is based on semantic retrieval from the knowledge base. "
            "It should not be relied upon without verification of current field rules "
            "and RRC records."
        ),
        timestamp=datetime.now(timezone.utc).isoformat(),
        version=ENGINE_VERSION,
    )


def _build_deep_analysis_response(
    query: SpacingQuery,
    trace_id: str,
    start_time: float,
    zone: AnalysisZone,
    normalized: NormalizationResult,
) -> SpacingResponse:
    """Build response from deep analysis (Layer 3) - multi-source synthesis."""
    q_lower = query.question.lower()

    # TIE COMPONENT 20: DEEP ANALYSIS MODE
    analysis_sources: List[str] = []
    reasoning_chain: List[str] = []

    # Step 1: Identify applicable statewide rules
    reasoning_chain.append(
        "Step 1 - Statewide Rule Identification: Texas statewide Rules 37 and 38 "
        "establish baseline spacing and density requirements for all oil and gas wells."
    )
    analysis_sources.append("16 TAC Chapter 3 (Statewide Rules)")

    # Step 2: Check for field-specific rules
    if query.field_name:
        reasoning_chain.append(
            f"Step 2 - Field Rule Check: Query references field '{query.field_name}'. "
            f"Field-specific rules adopted by RRC order may supersede statewide rules. "
            f"Must obtain current field rules from RRC."
        )
        analysis_sources.append(f"RRC Field Rules for {query.field_name}")
    else:
        reasoning_chain.append(
            "Step 2 - Field Rule Check: No specific field identified. "
            "Statewide spacing rules apply unless operator can identify applicable field rules."
        )

    # Step 3: Well type analysis
    well_type = query.well_type or ("horizontal" if "horizontal" in q_lower else "vertical")
    if well_type == "horizontal":
        reasoning_chain.append(
            "Step 3 - Well Type: Horizontal well identified. Modified spacing rules apply. "
            "Diagonal rule for lease line setbacks. Lateral-to-lateral spacing required. "
            "Special horizontal provisions under Rule 37."
        )
        analysis_sources.append("16 TAC §3.37 (Horizontal Provisions)")
    else:
        reasoning_chain.append(
            "Step 3 - Well Type: Vertical well. Standard Rule 37 spacing applies. "
            "Oil: 467 ft lease line / 1,200 ft between wells. "
            "Gas: 330 ft lease line / 660 ft between wells."
        )
        analysis_sources.append("16 TAC §3.37 (Standard Spacing)")

    # Step 4: Exception analysis
    if any(term in q_lower for term in ["exception", "variance", "small tract", "hardship"]):
        reasoning_chain.append(
            "Step 4 - Exception Analysis: Spacing exception may be required. "
            "Operator must file Rule 37 exception application with RRC, "
            "notify offset operators, and demonstrate no drainage impact. "
            "Hearing may be required if protests are filed."
        )
        analysis_sources.append("RRC Exception Application Process")
    else:
        reasoning_chain.append(
            "Step 4 - Exception Analysis: No clear exception indicators. "
            "Standard spacing compliance analysis applies."
        )

    # Step 5: Correlative rights assessment
    if any(term in q_lower for term in ["drainage", "offset", "correlative", "confiscation"]):
        reasoning_chain.append(
            "Step 5 - Correlative Rights: Drainage and correlative rights are central "
            "to spacing analysis. Must assess whether proposed well location adequately "
            "protects adjacent mineral owners from uncompensated drainage."
        )
        analysis_sources.append("Texas Natural Resources Code §85 (Correlative Rights)")
    else:
        reasoning_chain.append(
            "Step 5 - Correlative Rights: Standard correlative rights protections "
            "apply through compliance with applicable spacing rules."
        )

    # Step 6: Pooling analysis
    if any(term in q_lower for term in ["pooling", "unit", "unleased"]):
        reasoning_chain.append(
            "Step 6 - Pooling: Pooling of mineral interests may be necessary "
            "to comply with spacing requirements or to develop fragmented mineral "
            "ownership. Voluntary pooling preferred; forced pooling available under "
            "Texas Natural Resources Code Chapter 102."
        )
        analysis_sources.append("Texas Natural Resources Code Chapter 102 (MIPA)")
    else:
        reasoning_chain.append(
            "Step 6 - Pooling: No specific pooling issues identified in query."
        )

    # Step 7: Synthesis
    reasoning_chain.append(
        "Step 7 - Synthesis: This analysis integrates statewide rules, field-specific "
        "provisions, well type considerations, and correlative rights protections. "
        "A definitive spacing determination requires review of current RRC records, "
        "applicable field rules, and plat/survey of proposed well location."
    )

    full_reasoning = "\n".join(reasoning_chain)

    conclusion = (
        f"Deep analysis of spacing query in {zone.value} zone. "
        f"This question requires field-specific research beyond pre-compiled doctrine. "
        f"The analysis synthesized {len(analysis_sources)} authority sources through "
        f"a {len(reasoning_chain)}-step reasoning chain. "
        f"Recommend consulting RRC field office and obtaining current field rules "
        f"before committing capital to drill."
    )

    key_factors = [
        "Standard statewide spacing rules provide baseline requirements",
        "Field-specific rules may supersede statewide rules",
        f"Well type: {well_type} - spacing rules vary by well type",
        "Exception applications available through RRC",
        "Correlative rights of offset operators must be protected",
        "Consult RRC district office for current field rules",
    ]

    citations = [
        Citation(
            authority=source.split("(")[0].strip(),
            reference=source,
            relevance="Deep analysis source",
            level=classify_authority(source).value,
            weight=_lookup_authority_weight(source),
        )
        for source in analysis_sources
    ]

    determinism = compute_determinism_hash(
        query.question, "deep_analysis", 0.45, query.mode.value, zone.value,
    )

    latency_ms = round((time.time() - start_time) * 1000, 2)

    decomposition = None
    if query.include_decomposition:
        decomposition = decompose_issues(query.question, [])

    return SpacingResponse(
        query_id=trace_id,
        question=query.question,
        mode=query.mode,
        zone=zone.value,
        conclusion=conclusion,
        reasoning=full_reasoning,
        key_factors=key_factors,
        citations=citations,
        doctrine_match=False,
        confidence_tier=ConfidenceTier.HIGH_RISK.value,
        confidence_stratification=stratify_confidence(0.45),
        response_layer="deep_analysis",
        latency_ms=latency_ms,
        determinism_hash=determinism,
        limitations=[
            "No doctrine cache match - response based on deep analysis",
            "Field-specific rules not available in doctrine cache",
            "Requires verification with RRC records",
            "This is not a compliance certification",
            f"Zone: {ZONE_CONSTRAINTS[zone]['output_label']}",
        ],
        disclosure_caveat=(
            "This deep analysis response is based on general regulatory knowledge "
            "and does not constitute a compliance certification. Specific field rules, "
            "pending RRC orders, or recent regulatory changes may affect the analysis. "
            "Obtain legal review and RRC confirmation before proceeding."
        ),
        issue_decomposition=decomposition,
        timestamp=datetime.now(timezone.utc).isoformat(),
        version=ENGINE_VERSION,
    )


# ==============================================================================
# RESPONSE FORMATTING HELPERS
# ==============================================================================


def _format_conclusion(
    doctrine: DoctrineBlock,
    query: SpacingQuery,
    zone: AnalysisZone,
) -> str:
    """Format the conclusion based on response mode and zone."""
    base_conclusion = doctrine.conclusion_template
    if "{jurisdiction}" in base_conclusion:
        base_conclusion = base_conclusion.replace("{jurisdiction}", query.jurisdiction)

    if query.mode == ResponseMode.FAST:
        return base_conclusion

    if query.mode == ResponseMode.DEFENSE:
        zone_label = ZONE_CONSTRAINTS[zone]["output_label"]
        return (
            f"[{zone_label}] {base_conclusion} "
            f"Burden of proof: {doctrine.burden_holder}. "
            f"Adversary position: {doctrine.adversary_position}."
        )

    if query.mode == ResponseMode.MEMO:
        return (
            f"MEMORANDUM - SPACING ANALYSIS\n"
            f"Zone: {zone.value.upper()}\n"
            f"Jurisdiction: {query.jurisdiction}\n"
            f"{'=' * 60}\n\n"
            f"{base_conclusion}\n\n"
            f"Resolution Strategy: {doctrine.resolution_strategy}\n"
            f"Burden: {doctrine.burden_holder}\n"
            f"Adversary: {doctrine.adversary_position}"
        )

    return base_conclusion


def _format_reasoning(
    primary: DoctrineBlock,
    query: SpacingQuery,
    zone: AnalysisZone,
    all_doctrines: List[DoctrineBlock],
) -> str:
    """Format reasoning based on response mode."""
    if query.mode == ResponseMode.FAST:
        return primary.reasoning_framework[:500]

    if query.mode == ResponseMode.DEFENSE:
        parts = [
            f"PRIMARY DOCTRINE: {primary.topic}",
            f"Framework: {primary.reasoning_framework}",
            f"Counter-arguments: {'; '.join(primary.counter_arguments)}",
            f"Resolution: {primary.resolution_strategy}",
        ]
        if len(all_doctrines) > 1:
            parts.append(
                f"SECONDARY DOCTRINES: {', '.join(d.topic for d in all_doctrines[1:3])}"
            )
        return "\n".join(parts)

    if query.mode == ResponseMode.MEMO:
        parts = [
            "I. PRIMARY ANALYSIS",
            f"   Topic: {primary.topic}",
            f"   Framework: {primary.reasoning_framework}",
            "",
            "II. BURDEN ANALYSIS",
            f"   Burden holder: {primary.burden_holder}",
            f"   Adversary: {primary.adversary_position}",
            "",
            "III. COUNTER-ARGUMENTS",
        ]
        for i, arg in enumerate(primary.counter_arguments, 1):
            parts.append(f"   {i}. {arg}")
        parts.extend([
            "",
            "IV. RESOLUTION STRATEGY",
            f"   {primary.resolution_strategy}",
        ])
        if len(all_doctrines) > 1:
            parts.extend([
                "",
                "V. RELATED DOCTRINES",
            ])
            for doctrine in all_doctrines[1:4]:
                parts.append(f"   - {doctrine.topic} (confidence: {doctrine.confidence:.2f})")
        return "\n".join(parts)

    return primary.reasoning_framework


def _extract_key_factors(doctrine: DoctrineBlock, query: SpacingQuery) -> List[str]:
    """Extract and prioritize key factors based on query context."""
    factors = list(doctrine.key_factors)

    if query.well_type == "horizontal" and "horizontal" not in doctrine.topic.lower():
        factors.insert(0, "NOTE: Query specifies horizontal well - review horizontal-specific spacing rules")
    if query.field_name:
        factors.insert(0, f"NOTE: Field '{query.field_name}' may have special spacing rules")

    return factors[:8]


def _build_citations(
    primary: DoctrineBlock,
    all_doctrines: List[DoctrineBlock],
) -> List[Citation]:
    """Build citation list with authority classification."""
    citations: List[Citation] = []
    seen_refs: set = set()

    for auth in primary.primary_authority:
        if auth not in seen_refs:
            level = classify_authority(auth)
            weight = _lookup_authority_weight(auth)
            citations.append(Citation(
                authority=auth.split("(")[0].strip() if "(" in auth else auth,
                reference=auth,
                relevance="Primary spacing authority",
                level=level.value,
                weight=weight,
            ))
            seen_refs.add(auth)

    for doctrine in all_doctrines[1:3]:
        for auth in doctrine.primary_authority[:1]:
            if auth not in seen_refs:
                level = classify_authority(auth)
                weight = _lookup_authority_weight(auth)
                citations.append(Citation(
                    authority=auth.split("(")[0].strip() if "(" in auth else auth,
                    reference=auth,
                    relevance=f"Supporting authority ({doctrine.topic})",
                    level=level.value,
                    weight=weight,
                ))
                seen_refs.add(auth)

    citations.sort(key=lambda c: c.weight or 0.0, reverse=True)
    return citations


def _build_authority_chain(
    primary: DoctrineBlock,
    all_doctrines: List[DoctrineBlock],
) -> List[Dict[str, Any]]:
    """Build a hierarchical authority chain for the response."""
    chain: List[Dict[str, Any]] = []
    seen: set = set()

    for doctrine in [primary] + all_doctrines[1:3]:
        for auth in doctrine.primary_authority:
            if auth not in seen:
                level = classify_authority(auth)
                weight = _lookup_authority_weight(auth)
                chain.append({
                    "authority": auth,
                    "level": level.value,
                    "weight": weight,
                    "doctrine": doctrine.topic,
                })
                seen.add(auth)

    if primary.controlling_precedent and primary.controlling_precedent not in seen:
        level = classify_authority(primary.controlling_precedent)
        weight = _lookup_authority_weight(primary.controlling_precedent)
        chain.append({
            "authority": primary.controlling_precedent,
            "level": level.value,
            "weight": weight,
            "doctrine": primary.topic,
            "role": "controlling_precedent",
        })

    chain.sort(key=lambda x: x["weight"], reverse=True)
    return chain


def _build_limitations(
    doctrine: DoctrineBlock,
    zone: AnalysisZone,
    conf_strat: Dict[str, Any],
) -> List[str]:
    """Build context-aware limitations list."""
    limitations: List[str] = []

    if zone == AnalysisZone.PLANNING:
        limitations.append("Planning analysis only - not a compliance certification")
    if zone == AnalysisZone.AUDIT:
        limitations.append("Audit analysis - verify all facts against RRC records")

    if conf_strat.get("requires_field_verification"):
        limitations.append("Field-specific rules should be verified with RRC")
    if conf_strat.get("requires_disclosure"):
        limitations.append("Position requires disclosure of regulatory uncertainty")

    if doctrine.confidence < 0.85:
        limitations.append(
            f"Moderate confidence ({doctrine.confidence:.2f}) - additional verification recommended"
        )

    limitations.append(
        "Spacing rules may be modified by pending RRC orders or field rule amendments"
    )

    return limitations


# ==============================================================================
# TIE COMPONENT 17: FASTAPI SERVER
# ==============================================================================

_start_time = time.time()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management."""
    logger.info(f"R08 Spacing Rules Engine v{ENGINE_VERSION} starting on port {ENGINE_PORT}")
    logger.info(f"Doctrine cache: {len(DOCTRINE_CACHE)} topics loaded")
    logger.info(f"Authority weights: {len(AUTHORITY_WEIGHTS)} sources configured")
    logger.info(f"Spacing term normalization: {len(SPACING_TERM_NORMALIZATION)} mappings")
    logger.info(f"Interaction edges: {len(INTERACTION_EDGES)} edges")
    logger.info(f"Banned phrases: {len(BANNED_PHRASES)} epistemic guardrails")
    logger.info(f"Cloud retriever: {'available' if _cloud_available else 'not available'}")
    yield
    logger.info("R08 Spacing Rules Engine shutting down")


app = FastAPI(
    title="ECHO R08 Spacing Rules Engine",
    description=(
        "TIE-20 Gold Standard engine for well spacing and density rule analysis. "
        "Covers Rule 37 spacing, Rule 38 density, horizontal well spacing, "
        "special field rules, pooling, and correlative rights."
    ),
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


# ==============================================================================
# ENDPOINTS
# ==============================================================================


@app.post("/query", response_model=SpacingResponse)
async def query_endpoint(query: SpacingQuery) -> SpacingResponse:
    """Primary query endpoint - three-layer spacing analysis."""
    trace_id = str(uuid.uuid4())
    logger.info(f"[{trace_id}] Query: mode={query.mode.value}, question={query.question[:100]}")

    try:
        normalized = normalize_semantics(query.question)
        response = three_layer_response(query, normalized, trace_id)
        return response
    except Exception as exc:
        logger.error(f"[{trace_id}] Query failed: {exc}")
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Comprehensive health check endpoint."""
    metrics = get_metrics()
    drift = get_drift_watcher()
    coverage = get_coverage_map()
    telemetry = get_telemetry()

    coverage_report = coverage.get_coverage_report()
    drift_report = drift.get_drift_report()
    telemetry_summary = telemetry.get_trace_summary()

    error_stats = metrics.get_error_stats()
    status = "healthy"
    if error_stats["last_hour"] > 10:
        status = "unhealthy"
    elif error_stats["last_hour"] > 3:
        status = "degraded"

    audit_count = 0
    if AUDIT_LOG.exists():
        try:
            with open(AUDIT_LOG, "r", encoding="utf-8") as f:
                audit_count = sum(1 for _ in f)
        except Exception:
            audit_count = -1

    return HealthResponse(
        status=status,
        engine=ENGINE_NAME,
        version=ENGINE_VERSION,
        port=ENGINE_PORT,
        domain=ENGINE_DOMAIN,
        uptime_seconds=round(time.time() - _start_time, 2),
        cloud_retriever_available=_cloud_available,
        doctrine_cache={
            "status": "operational",
            "topics": len(DOCTRINE_CACHE),
            "topic_list": [d.topic for d in DOCTRINE_CACHE],
            "hit_rate": metrics.get_doctrine_hit_rate(),
        },
        metrics=metrics.get_full_metrics(),
        drift_summary={
            "total_observations": drift_report["total_observations"],
            "active_alerts": drift_report["active_alerts"],
        },
        coverage_summary={
            "total_doctrines": coverage_report["total_doctrines"],
            "triggered": coverage_report["triggered_doctrines"],
            "coverage_pct": coverage_report["coverage_percentage"],
            "gap_count": coverage_report["epistemic_gaps"]["total_missed_queries"],
        },
        telemetry_summary=telemetry_summary,
        audit_trail_entries=audit_count,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


@app.get("/metrics")
async def metrics_endpoint() -> Dict[str, Any]:
    """Full metrics snapshot."""
    return {
        "engine": ENGINE_NAME,
        "version": ENGINE_VERSION,
        "metrics": get_metrics().get_full_metrics(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/drift")
async def drift_endpoint() -> Dict[str, Any]:
    """Drift watcher report."""
    return {
        "engine": ENGINE_NAME,
        "drift_report": get_drift_watcher().get_drift_report(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/coverage")
async def coverage_endpoint() -> Dict[str, Any]:
    """Coverage map report."""
    return {
        "engine": ENGINE_NAME,
        "coverage_report": get_coverage_map().get_coverage_report(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/doctrines")
async def list_doctrines() -> Dict[str, Any]:
    """List all loaded doctrines with metadata."""
    doctrines_list = []
    for d in DOCTRINE_CACHE:
        doctrines_list.append({
            "topic": d.topic,
            "keywords": d.keywords,
            "confidence": d.confidence,
            "confidence_stratification": d.confidence_stratification.value,
            "burden_holder": d.burden_holder,
            "adversary_position": d.adversary_position,
            "primary_authority": d.primary_authority,
            "controlling_precedent": d.controlling_precedent,
            "entity_scope": d.entity_scope,
            "key_factor_count": len(d.key_factors),
            "counter_argument_count": len(d.counter_arguments),
        })
    return {
        "engine": ENGINE_NAME,
        "total": len(DOCTRINE_CACHE),
        "doctrines": doctrines_list,
    }


@app.get("/authorities")
async def list_authorities() -> Dict[str, Any]:
    """List all authority weights and classification rules."""
    classified: List[Dict[str, Any]] = []
    for source, weight in sorted(AUTHORITY_WEIGHTS.items(), key=lambda x: x[1], reverse=True):
        classified.append({
            "source": source,
            "weight": weight,
            "level": classify_authority(source).value,
        })
    return {
        "engine": ENGINE_NAME,
        "total_authorities": len(AUTHORITY_WEIGHTS),
        "authority_levels": [level.value for level in AuthorityLevel],
        "authorities": classified,
    }


@app.get("/guardrails")
async def guardrails_endpoint() -> Dict[str, Any]:
    """Display epistemic guardrails configuration."""
    return {
        "engine": ENGINE_NAME,
        "banned_phrases": BANNED_PHRASES,
        "banned_phrase_count": len(BANNED_PHRASES),
        "confidence_tiers": {
            tier.value: {
                "range": f"{low:.2f}-{high:.2f}",
                "description": CONFIDENCE_DESCRIPTIONS[tier],
            }
            for tier, (low, high) in CONFIDENCE_THRESHOLDS.items()
        },
        "zones": {
            zone.value: constraints
            for zone, constraints in ZONE_CONSTRAINTS.items()
        },
    }


@app.get("/audit-trail")
async def audit_trail_endpoint(limit: int = 50) -> Dict[str, Any]:
    """Read recent audit trail entries."""
    entries = read_audit_trail(limit=min(limit, 500))
    return {
        "engine": ENGINE_NAME,
        "total_returned": len(entries),
        "requested_limit": limit,
        "entries": entries,
    }


@app.post("/authority-conflict")
async def authority_conflict_endpoint(
    authority_a: str,
    authority_b: str,
) -> Dict[str, Any]:
    """Resolve a conflict between two authority sources."""
    resolution = resolve_authority_conflict(authority_a, authority_b)
    return {
        "engine": ENGINE_NAME,
        "resolution": resolution,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.post("/validate-guardrails")
async def validate_guardrails_endpoint(text: str) -> Dict[str, Any]:
    """Validate text against epistemic guardrails."""
    result = apply_epistemic_guardrails(text)
    return {
        "engine": ENGINE_NAME,
        "validation": result,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ==============================================================================
# ENTRYPOINT
# ==============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=ENGINE_PORT)
