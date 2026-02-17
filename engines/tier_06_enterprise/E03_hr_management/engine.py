"""
E03 HR Management Engine - ECHO OMEGA PRIME
=============================================
Workforce analytics, compensation analysis, performance management,
succession planning, benefits optimization, compliance tracking,
recruiting pipeline, and employee engagement.

TIE-20 Compliant | Port 8903 | v1.0.0
"""

import asyncio
import hashlib
import json
import math
import os
import statistics
import time
import uuid
from collections import defaultdict
from datetime import datetime, timedelta, date
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import uvicorn
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator

try:
    from loguru import logger
except ImportError:
    import logging as _logging
    logger = _logging.getLogger("E03_hr_management")
    logger.add = lambda *a, **kw: None

# ═══════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════

ENGINE_ID = "E03"
ENGINE_NAME = "HR Management Engine"
ENGINE_VERSION = "1.0.0"
ENGINE_PORT = 8903
ENGINE_DOMAIN = "human_capital_management"

LOG_DIR = Path("O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/E03_hr_management/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
AUDIT_LOG = LOG_DIR / "audit_trail.jsonl"

logger.add(LOG_DIR / "engine.log", rotation="50 MB", retention="30 days", level="DEBUG")

BANNED_PHRASES = [
    "this is not legal advice",
    "consult an attorney",
    "I'm just an AI",
    "as a language model",
    "I cannot provide",
]

CONFIDENCE_THRESHOLDS = {
    "DEFENSIBLE": 0.85,
    "AGGRESSIVE": 0.65,
    "DISCLOSURE": 0.50,
    "HIGH_RISK": 0.35,
}

FLSA_SALARY_THRESHOLD_2026 = 58656
FMLA_ELIGIBILITY_HOURS = 1250
FMLA_ELIGIBILITY_MONTHS = 12
ADA_EMPLOYER_THRESHOLD = 15
COBRA_EMPLOYER_THRESHOLD = 20
EEO1_EMPLOYER_THRESHOLD = 100
WARN_ACT_THRESHOLD = 100
OSHA_RECORDKEEPING_THRESHOLD = 10


# ═══════════════════════════════════════════════════════════════
# ENUMS
# ═══════════════════════════════════════════════════════════════

class IssueCategory(str, Enum):
    WORKFORCE_ANALYTICS = "workforce_analytics"
    COMPENSATION = "compensation"
    PERFORMANCE = "performance"
    SUCCESSION = "succession"
    BENEFITS = "benefits"
    COMPLIANCE = "compliance"
    RECRUITING = "recruiting"
    ENGAGEMENT = "engagement"
    ORGANIZATIONAL_DESIGN = "organizational_design"
    LEARNING_DEVELOPMENT = "learning_development"
    EMPLOYEE_RELATIONS = "employee_relations"
    HR_TECHNOLOGY = "hr_technology"


class ResponseMode(str, Enum):
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"


class ConfidenceLevel(str, Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"


class PositionZone(str, Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"


class EmploymentType(str, Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    TEMP = "temporary"
    INTERN = "intern"


class FlsaStatus(str, Enum):
    EXEMPT = "exempt"
    NON_EXEMPT = "non_exempt"


class PerformanceRating(str, Enum):
    EXCEEDS = "exceeds_expectations"
    MEETS_PLUS = "meets_plus"
    MEETS = "meets_expectations"
    DEVELOPING = "developing"
    BELOW = "below_expectations"


class FlightRisk(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MODERATE = "moderate"
    LOW = "low"


# ═══════════════════════════════════════════════════════════════
# PYDANTIC MODELS
# ═══════════════════════════════════════════════════════════════

class EmployeeRecord(BaseModel):
    employee_id: str
    first_name: str
    last_name: str
    department: str
    title: str
    hire_date: str
    employment_type: EmploymentType = EmploymentType.FULL_TIME
    flsa_status: FlsaStatus = FlsaStatus.NON_EXEMPT
    salary: float = 0.0
    bonus_target_pct: float = 0.0
    manager_id: Optional[str] = None
    location: str = ""
    performance_rating: Optional[PerformanceRating] = None
    flight_risk: FlightRisk = FlightRisk.LOW
    tenure_months: int = 0
    is_active: bool = True


class CompensationBand(BaseModel):
    band_id: str
    title: str
    grade_level: int
    min_salary: float
    mid_salary: float
    max_salary: float
    bonus_target_pct: float = 0.0
    equity_eligible: bool = False


class RequisitionRecord(BaseModel):
    req_id: str
    title: str
    department: str
    hiring_manager: str
    opened_date: str
    target_fill_date: Optional[str] = None
    status: str = "open"
    applicant_count: int = 0
    interview_count: int = 0
    offer_count: int = 0
    source: str = ""
    salary_range_min: float = 0.0
    salary_range_max: float = 0.0


class EngagementSurveyResult(BaseModel):
    survey_id: str
    period: str
    department: str
    response_rate: float = 0.0
    overall_score: float = 0.0
    manager_score: float = 0.0
    growth_score: float = 0.0
    compensation_score: float = 0.0
    culture_score: float = 0.0
    worklife_score: float = 0.0
    enps: float = 0.0


class ComplianceCheckResult(BaseModel):
    check_id: str
    regulation: str
    area: str
    status: str = "pending"
    findings: List[str] = Field(default_factory=list)
    risk_level: str = "low"
    remediation_actions: List[str] = Field(default_factory=list)
    due_date: Optional[str] = None


class HRQuery(BaseModel):
    query: str
    category: Optional[IssueCategory] = None
    mode: ResponseMode = ResponseMode.FAST
    zone: PositionZone = PositionZone.PLANNING
    context: Dict[str, Any] = Field(default_factory=dict)
    employee_count: Optional[int] = None
    industry: Optional[str] = None
    state: Optional[str] = None


class DoctrineBlock(BaseModel):
    topic: str
    keywords: List[str]
    conclusion_template: str
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    burden_holder: str = ""
    adversary_position: str = ""
    counter_arguments: List[str] = Field(default_factory=list)
    resolution_strategy: str = ""
    entity_scope: str = "all_employers"
    confidence: float = 0.85
    confidence_stratification: ConfidenceLevel = ConfidenceLevel.DEFENSIBLE
    controlling_precedent: str = ""


class AnalysisResponse(BaseModel):
    engine_id: str = ENGINE_ID
    engine_version: str = ENGINE_VERSION
    query: str
    category: IssueCategory
    mode: ResponseMode
    zone: PositionZone
    confidence: float
    confidence_level: ConfidenceLevel
    primary_analysis: str
    supporting_reasoning: str
    key_factors: List[str]
    authorities_cited: List[str]
    risk_factors: List[str]
    recommendations: List[str]
    counter_arguments: List[str]
    doctrine_hits: List[str]
    determinism_hash: str
    latency_ms: float
    timestamp: str


class HealthResponse(BaseModel):
    engine_id: str = ENGINE_ID
    engine_name: str = ENGINE_NAME
    version: str = ENGINE_VERSION
    status: str = "healthy"
    uptime_seconds: float = 0.0
    port: int = ENGINE_PORT
    domain: str = ENGINE_DOMAIN
    total_queries: int = 0
    cache_hit_rate: float = 0.0
    avg_latency_ms: float = 0.0
    doctrine_count: int = 0
    categories: List[str] = Field(default_factory=list)
    last_query_time: Optional[str] = None


# ═══════════════════════════════════════════════════════════════
# TELEMETRY & METRICS
# ═══════════════════════════════════════════════════════════════

class TelemetryCollector:
    """Full query tracing, latency tracking, error domains."""

    def __init__(self) -> None:
        self.start_time: float = time.time()
        self.query_count: int = 0
        self.cache_hits: int = 0
        self.cache_misses: int = 0
        self.errors: List[Dict[str, Any]] = []
        self.latencies: List[float] = []
        self.category_counts: Dict[str, int] = defaultdict(int)
        self.hourly_counts: Dict[str, int] = defaultdict(int)
        self.last_query_time: Optional[str] = None
        self.doctrine_hit_counts: Dict[str, int] = defaultdict(int)

    def record_query(self, category: str, latency_ms: float, cache_hit: bool) -> None:
        self.query_count += 1
        self.latencies.append(latency_ms)
        self.category_counts[category] += 1
        hour_key = datetime.utcnow().strftime("%Y-%m-%d-%H")
        self.hourly_counts[hour_key] += 1
        self.last_query_time = datetime.utcnow().isoformat()
        if cache_hit:
            self.cache_hits += 1
        else:
            self.cache_misses += 1

    def record_error(self, error_type: str, message: str, context: Dict[str, Any]) -> None:
        self.errors.append({
            "type": error_type,
            "message": message,
            "context": context,
            "timestamp": datetime.utcnow().isoformat(),
        })

    def record_doctrine_hit(self, topic: str) -> None:
        self.doctrine_hit_counts[topic] += 1

    @property
    def uptime_seconds(self) -> float:
        return time.time() - self.start_time

    @property
    def avg_latency_ms(self) -> float:
        if not self.latencies:
            return 0.0
        return statistics.mean(self.latencies)

    @property
    def p95_latency_ms(self) -> float:
        if len(self.latencies) < 2:
            return self.avg_latency_ms
        sorted_lat = sorted(self.latencies)
        idx = int(len(sorted_lat) * 0.95)
        return sorted_lat[min(idx, len(sorted_lat) - 1)]

    @property
    def cache_hit_rate(self) -> float:
        total = self.cache_hits + self.cache_misses
        if total == 0:
            return 0.0
        return self.cache_hits / total

    @property
    def error_rate(self) -> float:
        if self.query_count == 0:
            return 0.0
        return len(self.errors) / self.query_count

    def get_metrics(self) -> Dict[str, Any]:
        return {
            "uptime_seconds": round(self.uptime_seconds, 1),
            "total_queries": self.query_count,
            "cache_hit_rate": round(self.cache_hit_rate, 4),
            "avg_latency_ms": round(self.avg_latency_ms, 2),
            "p95_latency_ms": round(self.p95_latency_ms, 2),
            "error_rate": round(self.error_rate, 4),
            "errors_total": len(self.errors),
            "category_distribution": dict(self.category_counts),
            "hourly_throughput": dict(self.hourly_counts),
            "top_doctrines": dict(sorted(
                self.doctrine_hit_counts.items(),
                key=lambda x: x[1], reverse=True
            )[:10]),
        }


telemetry = TelemetryCollector()


# ═══════════════════════════════════════════════════════════════
# AUDIT TRAIL (JSONL)
# ═══════════════════════════════════════════════════════════════

def write_audit_log(entry: Dict[str, Any]) -> None:
    """Append query to JSONL audit trail for forensic review."""
    entry["timestamp"] = datetime.utcnow().isoformat()
    entry["engine_id"] = ENGINE_ID
    try:
        with open(AUDIT_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, default=str) + "\n")
    except Exception as exc:
        logger.error(f"Audit log write failed: {exc}")


# ═══════════════════════════════════════════════════════════════
# DETERMINISM HASH (SHA-256)
# ═══════════════════════════════════════════════════════════════

def compute_determinism_hash(query: str, analysis: str, factors: List[str]) -> str:
    """SHA-256 hash for reproducibility verification."""
    payload = json.dumps({
        "query": query,
        "analysis": analysis,
        "factors": sorted(factors),
        "engine": ENGINE_ID,
        "version": ENGINE_VERSION,
    }, sort_keys=True)
    return hashlib.sha256(payload.encode()).hexdigest()


# ═══════════════════════════════════════════════════════════════
# SEMANTIC NORMALIZATION
# ═══════════════════════════════════════════════════════════════

HR_TERM_MAP: Dict[str, str] = {
    "firing": "involuntary_termination",
    "fired": "involuntary_termination",
    "let go": "involuntary_termination",
    "laid off": "reduction_in_force",
    "layoff": "reduction_in_force",
    "rif": "reduction_in_force",
    "quit": "voluntary_resignation",
    "resigned": "voluntary_resignation",
    "pay raise": "salary_adjustment",
    "raise": "salary_adjustment",
    "bonus": "variable_compensation",
    "incentive": "variable_compensation",
    "pto": "paid_time_off",
    "vacation": "paid_time_off",
    "sick leave": "sick_time",
    "fmla": "family_medical_leave",
    "maternity": "parental_leave",
    "paternity": "parental_leave",
    "ada": "disability_accommodation",
    "reasonable accommodation": "disability_accommodation",
    "harassment": "workplace_harassment",
    "hostile work environment": "workplace_harassment",
    "discrimination": "employment_discrimination",
    "eeo": "equal_employment_opportunity",
    "title vii": "title_vii_civil_rights",
    "overtime": "flsa_overtime",
    "exempt": "flsa_exemption",
    "non-exempt": "flsa_non_exempt",
    "w2": "tax_form_w2",
    "i9": "employment_eligibility_verification",
    "e-verify": "employment_eligibility_verification",
    "onboarding": "new_hire_onboarding",
    "offboarding": "employee_separation",
    "exit interview": "separation_feedback",
    "pip": "performance_improvement_plan",
    "probation": "performance_improvement_plan",
    "hipo": "high_potential_talent",
    "high potential": "high_potential_talent",
    "9-box": "nine_box_talent_grid",
    "succession": "succession_planning",
    "bench strength": "successor_readiness",
    "headcount": "workforce_headcount",
    "fte": "full_time_equivalent",
    "turnover": "employee_turnover",
    "attrition": "employee_attrition",
    "retention": "employee_retention",
    "engagement": "employee_engagement",
    "enps": "employee_net_promoter_score",
    "pulse survey": "engagement_pulse_survey",
    "comp ratio": "compa_ratio",
    "compa-ratio": "compa_ratio",
    "market rate": "market_reference_point",
    "salary band": "compensation_band",
    "pay grade": "compensation_grade",
    "job evaluation": "job_worth_assessment",
    "hay method": "hay_group_job_evaluation",
    "total rewards": "total_compensation_package",
    "equity": "stock_equity_compensation",
    "rsu": "restricted_stock_unit",
    "stock option": "equity_stock_option",
    "espp": "employee_stock_purchase_plan",
    "cobra": "cobra_continuation_coverage",
    "open enrollment": "benefits_open_enrollment",
    "hsa": "health_savings_account",
    "fsa": "flexible_spending_account",
    "401k": "retirement_401k",
    "pension": "defined_benefit_pension",
    "vesting": "benefit_vesting_schedule",
    "warn act": "warn_act_notification",
    "osha": "osha_workplace_safety",
    "workers comp": "workers_compensation",
    "flsa": "fair_labor_standards_act",
    "nlra": "national_labor_relations_act",
    "eeoc": "equal_employment_opportunity_commission",
    "dol": "department_of_labor",
    "recruiter": "talent_acquisition_specialist",
    "ats": "applicant_tracking_system",
    "time to fill": "time_to_fill_metric",
    "cost per hire": "cost_per_hire_metric",
    "quality of hire": "quality_of_hire_metric",
    "source of hire": "recruitment_source_effectiveness",
    "offer acceptance": "offer_acceptance_rate",
    "interview": "candidate_interview",
    "background check": "pre_employment_screening",
    "drug test": "pre_employment_screening",
    "okr": "objectives_key_results",
    "kpi": "key_performance_indicator",
    "calibration": "performance_calibration",
    "360 review": "multi_rater_feedback",
    "annual review": "annual_performance_review",
    "continuous feedback": "continuous_performance_management",
    "lms": "learning_management_system",
    "training": "employee_development_training",
    "upskilling": "skill_development_program",
    "reskilling": "workforce_reskilling",
    "dei": "diversity_equity_inclusion",
    "d&i": "diversity_equity_inclusion",
    "belonging": "diversity_equity_inclusion",
    "org design": "organizational_design",
    "restructuring": "organizational_restructuring",
    "span of control": "management_span_of_control",
    "org chart": "organizational_hierarchy",
    "hris": "hr_information_system",
    "hcm": "human_capital_management",
    "saas": "software_as_service",
}


def normalize_hr_term(text: str) -> str:
    """Normalize HR terminology to canonical forms."""
    lower = text.lower().strip()
    for raw, canonical in HR_TERM_MAP.items():
        if raw in lower:
            lower = lower.replace(raw, canonical)
    return lower


def extract_hr_keywords(text: str) -> List[str]:
    """Extract recognized HR keywords from query text."""
    lower = text.lower()
    found = []
    for raw, canonical in HR_TERM_MAP.items():
        if raw in lower and canonical not in found:
            found.append(canonical)
    return found


# ═══════════════════════════════════════════════════════════════
# AUTHORITY HARDENING
# ═══════════════════════════════════════════════════════════════

AUTHORITY_HIERARCHY: List[Dict[str, Any]] = [
    {"level": 1, "source": "federal_statute", "weight": 1.0, "examples": ["FLSA", "FMLA", "ADA", "Title VII", "ADEA", "WARN Act"]},
    {"level": 2, "source": "federal_regulation", "weight": 0.95, "examples": ["29 CFR 541", "29 CFR 825", "29 CFR 1910"]},
    {"level": 3, "source": "agency_guidance", "weight": 0.85, "examples": ["EEOC Guidance", "DOL Opinion Letter", "OSHA Directive"]},
    {"level": 4, "source": "federal_case_law", "weight": 0.80, "examples": ["SCOTUS", "Circuit Court of Appeals"]},
    {"level": 5, "source": "state_statute", "weight": 0.75, "examples": ["CA Labor Code", "NY Labor Law", "TX Labor Code"]},
    {"level": 6, "source": "state_regulation", "weight": 0.70, "examples": ["CA DLSE", "NY DOL Reg"]},
    {"level": 7, "source": "professional_standard", "weight": 0.60, "examples": ["SHRM Guidelines", "WorldatWork Standards"]},
    {"level": 8, "source": "industry_benchmark", "weight": 0.50, "examples": ["Mercer Survey", "Radford Data", "BLS OES"]},
    {"level": 9, "source": "best_practice", "weight": 0.40, "examples": ["SHRM Toolkit", "Bersin Research"]},
    {"level": 10, "source": "internal_policy", "weight": 0.30, "examples": ["Employee Handbook", "HR SOP"]},
]


def get_authority_weight(source_type: str) -> float:
    """Return weight for a given authority source type."""
    for auth in AUTHORITY_HIERARCHY:
        if auth["source"] == source_type:
            return auth["weight"]
    return 0.20


def resolve_authority_conflict(authorities: List[Dict[str, Any]]) -> Dict[str, Any]:
    """When authorities conflict, higher-level authority prevails."""
    if not authorities:
        return {"resolution": "no_authority", "prevailing": None}
    sorted_auth = sorted(authorities, key=lambda a: a.get("weight", 0), reverse=True)
    prevailing = sorted_auth[0]
    conflicting = [a for a in sorted_auth[1:] if a.get("position") != prevailing.get("position")]
    return {
        "resolution": "hierarchy_based",
        "prevailing": prevailing,
        "conflicting_authorities": conflicting,
        "reasoning": f"Federal authority ({prevailing.get('source', 'unknown')}) "
                     f"preempts lower-level sources per Supremacy Clause and regulatory hierarchy.",
    }


# ═══════════════════════════════════════════════════════════════
# CONFIDENCE STRATIFICATION
# ═══════════════════════════════════════════════════════════════

def stratify_confidence(
    base_score: float,
    authority_level: int,
    regulatory_clarity: float,
    state_variation: bool,
    recent_changes: bool,
) -> Tuple[float, ConfidenceLevel]:
    """Compute stratified confidence with HR-specific adjustments."""
    adjusted = base_score
    if authority_level <= 2:
        adjusted += 0.10
    elif authority_level >= 7:
        adjusted -= 0.10
    if regulatory_clarity < 0.5:
        adjusted -= 0.15
    if state_variation:
        adjusted -= 0.10
    if recent_changes:
        adjusted -= 0.05
    adjusted = max(0.10, min(0.99, adjusted))
    if adjusted >= CONFIDENCE_THRESHOLDS["DEFENSIBLE"]:
        level = ConfidenceLevel.DEFENSIBLE
    elif adjusted >= CONFIDENCE_THRESHOLDS["AGGRESSIVE"]:
        level = ConfidenceLevel.AGGRESSIVE
    elif adjusted >= CONFIDENCE_THRESHOLDS["DISCLOSURE"]:
        level = ConfidenceLevel.DISCLOSURE
    else:
        level = ConfidenceLevel.HIGH_RISK
    return round(adjusted, 4), level


# ═══════════════════════════════════════════════════════════════
# FACT FRAGILITY SCORING
# ═══════════════════════════════════════════════════════════════

def score_fact_fragility(
    verifiability: float,
    regulatory_stability: float,
    state_dependency: float,
    employer_size_dependency: float,
    industry_dependency: float,
) -> Dict[str, Any]:
    """Score how fragile/stable an HR fact or position is."""
    composite = (
        verifiability * 0.30
        + regulatory_stability * 0.25
        + (1.0 - state_dependency) * 0.20
        + (1.0 - employer_size_dependency) * 0.15
        + (1.0 - industry_dependency) * 0.10
    )
    if composite >= 0.80:
        fragility = "STABLE"
    elif composite >= 0.60:
        fragility = "MODERATE"
    elif composite >= 0.40:
        fragility = "FRAGILE"
    else:
        fragility = "HIGHLY_FRAGILE"
    return {
        "composite_score": round(composite, 4),
        "fragility_level": fragility,
        "verifiability": verifiability,
        "regulatory_stability": regulatory_stability,
        "state_dependency": state_dependency,
        "employer_size_dependency": employer_size_dependency,
        "industry_dependency": industry_dependency,
    }


# ═══════════════════════════════════════════════════════════════
# DOCTRINE CACHE — 55 Pre-compiled Expert Reasoning Blocks
# ═══════════════════════════════════════════════════════════════

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="flsa_overtime_classification",
        keywords=["flsa", "overtime", "exempt", "non-exempt", "salary_threshold", "duties_test"],
        conclusion_template=(
            "FLSA exemption requires meeting BOTH the salary basis test (${threshold}/year as of 2026) "
            "AND the duties test for executive, administrative, professional, computer, or outside sales "
            "exemptions. Misclassification exposes employers to back-pay liability for 2-3 years of "
            "unpaid overtime, liquidated damages, and attorney fees under 29 USC 216(b)."
        ),
        reasoning_framework=(
            "STEP 1: Verify salary basis - employee must receive predetermined fixed salary not subject "
            "to reduction based on quality/quantity of work. STEP 2: Apply primary duty test for claimed "
            "exemption category. Executive: manages enterprise/department, directs 2+ employees, has "
            "hiring/firing authority. Administrative: office/non-manual work directly related to management "
            "or business operations, exercises discretion and independent judgment on significant matters. "
            "Professional: work requiring advanced knowledge in science/learning customarily acquired by "
            "prolonged specialized instruction. STEP 3: Evaluate job duties as actually performed, not "
            "job title or description. STEP 4: Consider state-specific tests (CA uses quantitative 50% "
            "test; federal uses primary duty qualitative test). STEP 5: Document classification rationale "
            "with contemporaneous analysis tied to actual job duties."
        ),
        key_factors=[
            "Salary must meet minimum threshold ($58,656 for 2026)",
            "Primary duty must satisfy specific exemption duties test",
            "Job title alone never determines exempt status",
            "Actual duties performed control, not job description",
            "State tests may impose stricter requirements than federal",
            "Misclassification risk includes 2-3 year lookback period",
        ],
        primary_authority=[
            "29 USC 213(a)(1) - FLSA white collar exemptions",
            "29 CFR Part 541 - Defining exempt duties",
            "DOL Final Rule 2024 salary threshold update",
            "Auer v. Robbins, 519 U.S. 452 (1997)",
        ],
        burden_holder="employer",
        adversary_position="DOL or employee claims misclassification; narrow construction of exemptions applies.",
        counter_arguments=[
            "Exemptions are affirmatively asserted defenses - employer bears burden of proof",
            "Courts construe FLSA exemptions narrowly against employer",
            "Hybrid roles with mixed duties create substantial classification risk",
            "State laws like California impose stricter quantitative duties tests",
            "DOL salary threshold has been subject to litigation and may change",
        ],
        resolution_strategy="Conduct comprehensive job analysis mapping actual duties to exemption criteria. Document analysis with specific examples and time allocation. Review state requirements for multi-state employers.",
        entity_scope="all_employers",
        confidence=0.90,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="29 CFR 541; DOL Fact Sheet #17A",
    ),
    DoctrineBlock(
        topic="fmla_eligibility_and_entitlement",
        keywords=["fmla", "family_medical_leave", "12_weeks", "serious_health_condition", "eligible_employee"],
        conclusion_template=(
            "FMLA provides up to 12 workweeks of unpaid, job-protected leave per 12-month period for "
            "eligible employees of covered employers. Eligibility requires 12 months of employment and "
            "1,250 hours worked in the preceding 12 months at a worksite with 50+ employees within 75 miles."
        ),
        reasoning_framework=(
            "STEP 1: Confirm employer coverage (50+ employees within 75-mile radius for 20+ calendar weeks). "
            "STEP 2: Verify employee eligibility (12 months tenure, 1,250 hours, worksite threshold). "
            "STEP 3: Identify qualifying reason: birth/adoption, serious health condition of employee or "
            "family member, qualifying exigency, military caregiver. STEP 4: Calculate leave entitlement "
            "based on employer's designated 12-month period method. STEP 5: Assess intermittent leave "
            "eligibility when medically necessary. STEP 6: Evaluate concurrent state leave law requirements "
            "which may provide greater benefits. STEP 7: Ensure proper notice and medical certification "
            "procedures are followed."
        ),
        key_factors=[
            "50-employee threshold counted within 75-mile radius",
            "12 months employment need not be consecutive",
            "1,250 hours is actual hours worked, not paid hours",
            "Serious health condition requires incapacity plus treatment",
            "Employer must designate leave as FMLA-qualifying",
            "State laws may provide broader leave rights",
        ],
        primary_authority=[
            "29 USC 2611-2619 - Family and Medical Leave Act",
            "29 CFR Part 825 - FMLA regulations",
            "Ragsdale v. Wolverine World Wide, 535 U.S. 81 (2002)",
        ],
        burden_holder="employee_initial_then_employer",
        adversary_position="Employee alleges FMLA interference or retaliation. Employer must show legitimate non-discriminatory reason for adverse action.",
        counter_arguments=[
            "Employee may not have provided adequate notice of need for leave",
            "Condition may not meet serious health condition definition",
            "Employee may have exhausted 12-week entitlement under employer's method",
            "Intermittent leave request may not be medically supported",
            "Employer's honest belief of leave abuse may justify investigation",
        ],
        resolution_strategy="Implement consistent FMLA administration with proper notice forms, medical certification, designation notices, and return-to-work procedures. Train managers on anti-retaliation obligations.",
        entity_scope="employers_50_plus",
        confidence=0.92,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="29 CFR 825; DOL WHD Fact Sheet 28",
    ),
    DoctrineBlock(
        topic="pay_equity_analysis",
        keywords=["pay_equity", "equal_pay", "compensation_gap", "gender_pay", "pay_disparity", "compa_ratio"],
        conclusion_template=(
            "Pay equity analysis requires systematic comparison of compensation across protected classes "
            "controlling for legitimate differentiating factors (experience, education, performance, location, "
            "job responsibilities). The Equal Pay Act requires equal pay for equal work regardless of sex; "
            "Title VII and state laws extend to race, ethnicity, and other protected classes."
        ),
        reasoning_framework=(
            "STEP 1: Define comparable groups using job families, grades, or substantially similar work criteria. "
            "STEP 2: Select appropriate statistical methodology (multiple regression, cohort analysis, or paired "
            "comparison). STEP 3: Identify legitimate pay factors as control variables: tenure, experience, "
            "education, performance ratings, location, shift differential, certifications. STEP 4: Run regression "
            "analysis controlling for legitimate factors - residual gap attributable to protected class indicates "
            "potential liability. STEP 5: Apply practical and statistical significance thresholds. STEP 6: "
            "Develop remediation plan for statistically significant gaps. STEP 7: Consider attorney-client "
            "privilege for proactive self-audit. STEP 8: Document decision framework for ongoing monitoring."
        ),
        key_factors=[
            "EPA uses 'equal work' standard (substantially equal skill, effort, responsibility, working conditions)",
            "Title VII uses broader 'comparable work' standard",
            "Employer affirmative defenses: seniority, merit, quantity/quality, factor other than sex",
            "State laws increasingly restrict prior salary inquiries",
            "Proactive audits should be conducted under privilege",
            "Statistical significance (p < 0.05) triggers remediation need",
        ],
        primary_authority=[
            "29 USC 206(d) - Equal Pay Act",
            "42 USC 2000e-2 - Title VII compensation discrimination",
            "Corning Glass Works v. Brennan, 417 U.S. 188 (1974)",
            "Rizo v. Yovino, 950 F.3d 1217 (9th Cir. 2020)",
        ],
        burden_holder="employee_then_employer_defense",
        adversary_position="Employee/EEOC demonstrates pay differential between comparable employees of different protected classes. Employer must prove affirmative defense.",
        counter_arguments=[
            "Pay differences explained by legitimate non-discriminatory factors",
            "Market forces as 'factor other than sex' defense (circuit split)",
            "Prior salary as justification increasingly rejected by courts and state laws",
            "Small sample sizes may not support statistical significance finding",
            "Performance-based pay differences require validated, unbiased rating system",
        ],
        resolution_strategy="Conduct privileged pay equity audit using regression analysis. Remediate statistically significant gaps. Implement ongoing monitoring with compensation decision documentation.",
        entity_scope="all_employers",
        confidence=0.87,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Corning Glass Works v. Brennan; Rizo v. Yovino",
    ),
    DoctrineBlock(
        topic="ada_reasonable_accommodation",
        keywords=["ada", "disability", "accommodation", "interactive_process", "undue_hardship", "essential_function"],
        conclusion_template=(
            "The ADA requires employers with 15+ employees to provide reasonable accommodations to qualified "
            "individuals with disabilities unless doing so would impose undue hardship. The interactive process "
            "is the mandatory dialogue between employer and employee to identify effective accommodations. "
            "Failure to engage in the interactive process in good faith is itself an ADA violation."
        ),
        reasoning_framework=(
            "STEP 1: Determine if individual has a disability under ADA (physical/mental impairment that "
            "substantially limits major life activity). STEP 2: Assess whether individual is 'qualified' - "
            "can perform essential functions with or without accommodation. STEP 3: Initiate interactive "
            "process upon knowledge of disability-related need. STEP 4: Identify potential accommodations "
            "(modified schedule, assistive technology, job restructuring, reassignment). STEP 5: Evaluate "
            "undue hardship factors (cost, operational impact, facility resources, financial capacity). "
            "STEP 6: Select and implement effective accommodation. STEP 7: Monitor effectiveness and "
            "adjust as needed."
        ),
        key_factors=[
            "ADAAA significantly broadened disability definition in 2008",
            "Interactive process must be initiated in good faith",
            "Essential functions determined by employer but must be bona fide",
            "Undue hardship considers entire organization's resources, not just department",
            "Reassignment is accommodation of last resort",
            "Documentation of interactive process is critical evidence",
        ],
        primary_authority=[
            "42 USC 12101-12213 - Americans with Disabilities Act",
            "29 CFR Part 1630 - EEOC ADA regulations",
            "EEOC Enforcement Guidance on Reasonable Accommodation (2002)",
            "US Airways v. Barnett, 535 U.S. 391 (2002)",
        ],
        burden_holder="employee_initial_then_employer",
        adversary_position="Employee requests accommodation; employer must show undue hardship or that no reasonable accommodation exists.",
        counter_arguments=[
            "Employer's essential function determination entitled to some deference",
            "Attendance may be essential function depending on job requirements",
            "Open-ended leave not required as accommodation",
            "Direct threat defense if accommodation cannot mitigate safety risk",
            "Employee must be qualified independent of accommodation for essential functions",
        ],
        resolution_strategy="Establish standardized interactive process workflow with documentation. Train managers on recognizing accommodation requests (need not use magic words). Centralize accommodation decisions with HR/legal.",
        entity_scope="employers_15_plus",
        confidence=0.88,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="US Airways v. Barnett; EEOC Guidance",
    ),
    DoctrineBlock(
        topic="workforce_turnover_analysis",
        keywords=["turnover", "attrition", "retention", "voluntary_separation", "involuntary_termination", "exit_analysis"],
        conclusion_template=(
            "Turnover analysis must distinguish voluntary from involuntary separations, regrettable from "
            "non-regrettable attrition, and first-year from tenured turnover. Best practice uses cohort-based "
            "survival analysis, controlling for department, manager, tenure band, and performance level to "
            "identify systemic retention risks versus random variation."
        ),
        reasoning_framework=(
            "STEP 1: Calculate overall turnover rate (separations / avg headcount * 100) monthly and annualized. "
            "STEP 2: Segment by type (voluntary, involuntary, retirement, RIF, death/disability). "
            "STEP 3: Apply regrettable classification (high performers leaving = regrettable). "
            "STEP 4: Analyze by cohort: department, manager, hire date vintage, performance tier, demographics. "
            "STEP 5: Run survival analysis (Kaplan-Meier or Cox proportional hazard) for tenure-based risk. "
            "STEP 6: Identify leading indicators (engagement scores, skip-level meetings, promotion velocity). "
            "STEP 7: Calculate cost of turnover per position (recruiting + onboarding + productivity ramp + "
            "knowledge loss). STEP 8: Benchmark against industry and BLS JOLTS data."
        ),
        key_factors=[
            "Voluntary turnover is more actionable than involuntary",
            "First-year turnover signals onboarding or hiring quality issues",
            "Manager-specific turnover indicates leadership problems",
            "Industry benchmarks vary significantly (tech 13-15%, healthcare 19-22%)",
            "Cost of turnover ranges from 50-200% of annual salary depending on role",
            "Predictive models can identify flight risk 3-6 months ahead",
        ],
        primary_authority=[
            "BLS JOLTS Survey - national turnover benchmarks",
            "SHRM Human Capital Benchmarking Report",
            "Work Institute Retention Report",
            "Bersin Talent Management Framework",
        ],
        burden_holder="hr_analytics_team",
        adversary_position="Leadership views turnover as unavoidable market condition rather than addressable organizational issue.",
        counter_arguments=[
            "Some turnover is healthy and brings fresh perspectives",
            "Low turnover can indicate stagnation or fear-based culture",
            "External labor market conditions drive turnover beyond employer control",
            "Remote work has fundamentally altered turnover patterns and benchmarks",
            "Turnover rates alone miss the quality dimension - who is leaving matters",
        ],
        resolution_strategy="Implement monthly turnover dashboard segmented by type, department, tenure, and performance. Run quarterly survival analysis. Build predictive flight risk model using engagement, compensation, and behavioral signals.",
        entity_scope="all_employers",
        confidence=0.85,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="SHRM Benchmarking Standards; BLS JOLTS methodology",
    ),
    DoctrineBlock(
        topic="compensation_band_design",
        keywords=["salary_band", "pay_range", "compensation_structure", "grade_level", "market_pricing", "hay_method"],
        conclusion_template=(
            "Compensation band design involves job evaluation (internal equity) and market pricing (external "
            "competitiveness) to create salary ranges with defined minimums, midpoints, and maximums. "
            "Typical band spread is 40-60% for professional roles and 20-30% for entry-level positions. "
            "Midpoint progression between grades should be 10-15% to incentivize promotion."
        ),
        reasoning_framework=(
            "STEP 1: Conduct job evaluation using point-factor (Hay), whole-job ranking, or market-pricing "
            "methodology. STEP 2: Benchmark positions against published survey data (Mercer, Radford, "
            "Culpepper, ERI, BLS OES). STEP 3: Age survey data to current date using projected increase "
            "budgets. STEP 4: Set band midpoints at target market percentile (50th competitive, 75th "
            "for hot skills). STEP 5: Define band spread (min to max range). STEP 6: Calculate overlap "
            "between adjacent grades (25-35% typical). STEP 7: Map employees to bands and calculate "
            "compa-ratios (salary / midpoint). STEP 8: Identify outliers below minimum or above maximum. "
            "STEP 9: Develop remediation plan with timeline and budget. STEP 10: Establish annual review "
            "cycle tied to survey updates."
        ),
        key_factors=[
            "Job evaluation establishes internal equity hierarchy",
            "Market pricing ensures external competitiveness",
            "Band spread reflects career progression within grade",
            "Compa-ratio distribution reveals pay equity patterns",
            "Hot skills premiums may justify above-midpoint positioning",
            "Geographic differentials needed for multi-location employers",
        ],
        primary_authority=[
            "WorldatWork Compensation Design Principles",
            "Hay Group Guide Chart-Profile Method",
            "Mercer IPE (International Position Evaluation)",
            "BLS Occupational Employment Statistics",
        ],
        burden_holder="compensation_team",
        adversary_position="Employees perceive pay as unfair without transparent structure. Managers make ad hoc pay decisions undermining internal equity.",
        counter_arguments=[
            "Rigid bands may impede hiring in competitive talent markets",
            "Survey data lags current market by 6-18 months",
            "Small employers may lack sufficient data for reliable benchmarking",
            "Remote work complicates geographic differential decisions",
            "Pay transparency laws force reconsideration of band communication strategy",
        ],
        resolution_strategy="Design bands using blended job evaluation and market pricing approach. Target 50th percentile for base, 75th for total compensation. Review annually with survey data refresh.",
        entity_scope="all_employers",
        confidence=0.86,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="WorldatWork Compensation Standards; Hay/Mercer methodologies",
    ),
    DoctrineBlock(
        topic="performance_calibration_process",
        keywords=["calibration", "performance_review", "forced_ranking", "bell_curve", "rating_distribution"],
        conclusion_template=(
            "Performance calibration aligns rating standards across managers to ensure fair, consistent evaluation. "
            "Best practice uses facilitated cross-functional sessions where managers present and defend ratings "
            "with evidence. Forced ranking/distribution is declining due to legal risk and engagement impact, "
            "replaced by calibration-guided distribution with manager discretion."
        ),
        reasoning_framework=(
            "STEP 1: Define performance dimensions and rating scale with behavioral anchors. "
            "STEP 2: Managers complete initial ratings with evidence documentation. "
            "STEP 3: Aggregate ratings by department to identify distribution skews. "
            "STEP 4: Conduct calibration sessions with skip-level and cross-functional managers. "
            "STEP 5: Discuss outliers (top and bottom performers) with supporting evidence. "
            "STEP 6: Adjust ratings based on calibration discussion and objective criteria. "
            "STEP 7: Review for adverse impact across protected classes. "
            "STEP 8: Finalize ratings and link to compensation, development, and succession actions."
        ),
        key_factors=[
            "Calibration reduces manager bias and rating inflation",
            "Evidence-based ratings (not opinions) survive legal scrutiny",
            "Forced ranking systems face increasing legal and cultural pushback",
            "Rating distribution should reflect actual performance, not forced curve",
            "Recency bias and halo effect are primary calibration targets",
            "Documentation quality correlates with legal defensibility",
        ],
        primary_authority=[
            "SHRM Performance Management Toolkit",
            "EEOC Uniform Guidelines on Employee Selection Procedures",
            "Bersin High-Impact Performance Management Research",
        ],
        burden_holder="hr_and_management",
        adversary_position="Employees challenge ratings as subjective. Calibration adjustments perceived as arbitrary if process lacks transparency.",
        counter_arguments=[
            "Calibration can itself introduce bias if dominated by strong personalities",
            "Statistical forced distribution demotivates high-performing teams",
            "Peer comparison disadvantages those in high-performing groups",
            "Continuous feedback may reduce need for annual calibration",
            "Manager training on rating scales is more effective than forced calibration",
        ],
        resolution_strategy="Implement evidence-based calibration with defined criteria, adverse impact review, and appeals process. Move toward continuous performance management supplemented by annual calibration.",
        entity_scope="all_employers",
        confidence=0.82,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="EEOC Uniform Guidelines; Griggs v. Duke Power (adverse impact)",
    ),
    DoctrineBlock(
        topic="succession_planning_framework",
        keywords=["succession", "talent_pipeline", "bench_strength", "nine_box", "high_potential", "leadership_development"],
        conclusion_template=(
            "Succession planning identifies and develops internal candidates for critical roles. The 9-box grid "
            "(performance x potential) segments talent for differentiated development investment. Bench strength "
            "ratio (ready-now successors / critical positions) measures pipeline health. Target: 1-2 ready-now "
            "successors per critical role."
        ),
        reasoning_framework=(
            "STEP 1: Identify critical positions (revenue impact, knowledge risk, replacement difficulty). "
            "STEP 2: Assess current bench using 9-box grid (performance on x-axis, potential on y-axis). "
            "STEP 3: Classify successor readiness: Ready Now (0-12 months), Ready Soon (1-2 years), "
            "Developing (2-3+ years). STEP 4: Create individual development plans (IDPs) for successors. "
            "STEP 5: Implement accelerated development (stretch assignments, mentoring, executive coaching, "
            "cross-functional rotations). STEP 6: Conduct annual talent review with executive committee. "
            "STEP 7: Track movement and readiness progress quarterly. STEP 8: Integrate with workforce "
            "planning for external pipeline strategies."
        ),
        key_factors=[
            "Critical role identification based on business impact, not org chart",
            "9-box potential assessment must use defined criteria, not gut feel",
            "Diversity of successor pool is legal and business imperative",
            "Emergency succession differs from developmental succession",
            "Board succession oversight required for C-suite positions",
            "Knowledge transfer planning prevents institutional memory loss",
        ],
        primary_authority=[
            "SHRM Succession Planning Toolkit",
            "Bersin Talent Management Framework",
            "Spencer Stuart Board Succession Governance",
            "DDI Global Leadership Forecast",
        ],
        burden_holder="hr_and_executive_leadership",
        adversary_position="Organization promotes based on tenure or availability rather than readiness, creating leadership capability gaps.",
        counter_arguments=[
            "9-box assessments can embed bias in potential ratings",
            "Labeling employees as HiPo/not creates retention risk for those excluded",
            "External hires may outperform internal succession pipeline",
            "Rapid organizational change can invalidate succession assumptions",
            "Development investments in successors may not yield returns if they leave",
        ],
        resolution_strategy="Implement structured succession process with defined potential criteria, diverse slates, and measurable IDP progress. Review quarterly with executive sponsor.",
        entity_scope="all_employers",
        confidence=0.83,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="SHRM Best Practice; Bersin Research",
    ),
    DoctrineBlock(
        topic="benefits_cost_optimization",
        keywords=["benefits", "health_insurance", "cost_containment", "plan_design", "hsa", "wellness"],
        conclusion_template=(
            "Benefits cost optimization balances cost containment with talent attraction/retention objectives. "
            "Key levers include plan design (HDHP+HSA shift), vendor negotiation, wellness programs, pharmacy "
            "benefits management, and self-insurance for employers with 200+ employees. Total benefits cost "
            "typically represents 30-35% of total compensation."
        ),
        reasoning_framework=(
            "STEP 1: Benchmark total benefits cost as percentage of payroll against industry peers. "
            "STEP 2: Analyze claims data for cost drivers (top diagnoses, high-cost claimants, pharmacy utilization). "
            "STEP 3: Model plan design alternatives (copay vs coinsurance, deductible levels, HDHP+HSA). "
            "STEP 4: Evaluate self-insurance feasibility (stop-loss analysis, cash flow modeling). "
            "STEP 5: Review pharmacy benefit design (formulary tiers, specialty drug management, biosimilars). "
            "STEP 6: Assess wellness program ROI (participation rates, claims impact, engagement correlation). "
            "STEP 7: Negotiate carrier/TPA terms with competitive bidding process. "
            "STEP 8: Model employee cost-sharing changes and communication strategy."
        ),
        key_factors=[
            "Healthcare costs rising 6-8% annually require proactive management",
            "HDHP+HSA shift to consumer-directed care is dominant trend",
            "Self-insurance provides data access and plan design flexibility",
            "Pharmacy costs are fastest-growing benefit expense category",
            "Wellness programs show mixed ROI evidence but positive engagement impact",
            "ACA compliance requirements constrain plan design options",
        ],
        primary_authority=[
            "KFF Employer Health Benefits Survey",
            "Mercer National Survey of Employer-Sponsored Health Plans",
            "ACA (26 USC 4980H) - Employer Shared Responsibility",
            "ERISA (29 USC 1001-1461) - Plan administration requirements",
        ],
        burden_holder="benefits_team",
        adversary_position="Employees expect rich benefits without cost increases. CFO demands cost containment. Balance is the challenge.",
        counter_arguments=[
            "Aggressive cost-shifting to employees harms recruitment",
            "High-deductible plans may discourage preventive care utilization",
            "Self-insurance requires sophisticated administration and risk tolerance",
            "Wellness incentives may create ADA/GINA compliance issues",
            "Plan design changes during open enrollment require careful communication",
        ],
        resolution_strategy="Conduct annual benefits strategy review with actuarial analysis. Model 3-year cost projections under multiple scenarios. Implement incremental plan design changes with strong communication.",
        entity_scope="all_employers",
        confidence=0.84,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="ACA; ERISA; KFF Survey benchmarks",
    ),
    DoctrineBlock(
        topic="recruiting_metrics_pipeline",
        keywords=["recruiting", "time_to_fill", "cost_per_hire", "source_effectiveness", "quality_of_hire", "applicant_tracking"],
        conclusion_template=(
            "Recruiting effectiveness is measured through a balanced scorecard of efficiency (time-to-fill, "
            "cost-per-hire), quality (quality-of-hire, new hire retention), and diversity (slate diversity, "
            "conversion rates by demographic). Median time-to-fill is 36-44 days; cost-per-hire ranges "
            "$3,000-$5,000 for professional roles per SHRM benchmarks."
        ),
        reasoning_framework=(
            "STEP 1: Define and standardize metric calculations across organization. Time-to-fill starts at "
            "req approval (not posting). STEP 2: Track funnel conversion rates: applicant->screen->interview->"
            "offer->acceptance. STEP 3: Analyze source effectiveness by channel (employee referral, job board, "
            "LinkedIn, agency, career fair) measuring quality and cost. STEP 4: Calculate cost-per-hire using "
            "SHRM/ANSI standard (internal + external costs / total hires). STEP 5: Implement quality-of-hire "
            "composite (new hire performance rating + manager satisfaction + retention at 6/12 months). "
            "STEP 6: Monitor candidate experience (NPS survey at each stage). STEP 7: Review adverse impact "
            "in selection process at each funnel stage. STEP 8: Benchmark metrics against SHRM and industry data."
        ),
        key_factors=[
            "Time-to-fill varies dramatically by role complexity and market",
            "Employee referrals consistently produce highest quality-of-hire",
            "Agency fees typically 15-25% of first-year salary",
            "Offer acceptance rate below 80% signals compensation or process issues",
            "Adverse impact analysis required at each selection stage",
            "Quality-of-hire is the most important but hardest-to-measure metric",
        ],
        primary_authority=[
            "SHRM/ANSI Cost-Per-Hire Standard (ANSI/SHRM 06001.2012)",
            "SHRM Talent Acquisition Benchmarking Report",
            "EEOC Uniform Guidelines on Employee Selection Procedures",
            "OFCCP Internet Applicant Rule (41 CFR 60-1.3)",
        ],
        burden_holder="talent_acquisition_team",
        adversary_position="Hiring managers blame recruiting for slow fills. Recruiting blames managers for slow decisions. Data resolves this tension.",
        counter_arguments=[
            "Speed-focused metrics may sacrifice quality for velocity",
            "Cost-per-hire excludes opportunity cost of unfilled positions",
            "Source attribution is complex in multi-touch candidate journeys",
            "Quality-of-hire measures lag 6-12 months after hire date",
            "Benchmarks may not reflect organization-specific role complexity",
        ],
        resolution_strategy="Implement recruiting analytics dashboard with real-time funnel tracking. Establish SLAs between recruiting and hiring managers. Review source ROI quarterly.",
        entity_scope="all_employers",
        confidence=0.85,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="SHRM/ANSI Standards; EEOC Selection Guidelines",
    ),
    DoctrineBlock(
        topic="employee_engagement_measurement",
        keywords=["engagement", "survey", "enps", "pulse", "sentiment", "retention_indicator"],
        conclusion_template=(
            "Employee engagement measurement combines annual census surveys with quarterly pulse surveys to "
            "track satisfaction, commitment, and discretionary effort. Key dimensions: manager relationship, "
            "growth opportunities, compensation fairness, organizational pride, work-life balance. eNPS "
            "(employee Net Promoter Score) provides a single-metric summary ranging from -100 to +100."
        ),
        reasoning_framework=(
            "STEP 1: Design survey instrument covering validated engagement dimensions (Gallup Q12, AON Hewitt "
            "model, or custom). STEP 2: Ensure anonymity with minimum reporting threshold (5+ responses per unit). "
            "STEP 3: Achieve target response rate (70%+ for validity). STEP 4: Analyze results by department, "
            "manager, tenure, demographic cuts. STEP 5: Identify key drivers through regression analysis (which "
            "dimensions most predict overall engagement). STEP 6: Create action plans at team level with manager "
            "ownership. STEP 7: Track action plan completion and resurvey impact. STEP 8: Correlate engagement "
            "scores with business outcomes (turnover, productivity, customer satisfaction, profitability)."
        ),
        key_factors=[
            "Response rate below 60% questions result validity",
            "Action on results is more important than the survey itself",
            "Manager quality is consistently the #1 engagement driver",
            "eNPS above 20 is considered good; above 50 is excellent",
            "Engagement correlates with turnover, productivity, and customer satisfaction",
            "Pulse surveys enable real-time tracking between annual surveys",
        ],
        primary_authority=[
            "Gallup Q12 Meta-Analysis",
            "AON Hewitt Global Engagement Database",
            "Bersin Employee Engagement Research",
            "SHRM Employee Engagement Toolkit",
        ],
        burden_holder="hr_and_management",
        adversary_position="Leadership dismisses survey results as complaints. Employees become cynical if no action follows surveys.",
        counter_arguments=[
            "Survey fatigue reduces response rates and data quality over time",
            "Self-report bias limits validity of attitudinal measures",
            "Engagement is multidimensional - single scores oversimplify",
            "High engagement without performance alignment is unproductive",
            "Remote/hybrid work requires adapted measurement approaches",
        ],
        resolution_strategy="Implement annual census + quarterly pulse cadence. Require manager action plans within 30 days of results. Track action completion and engagement trend correlation.",
        entity_scope="all_employers",
        confidence=0.83,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Gallup Q12 Research; AON Hewitt Model",
    ),
    DoctrineBlock(
        topic="title_vii_discrimination",
        keywords=["title_vii", "discrimination", "protected_class", "disparate_treatment", "disparate_impact", "eeoc"],
        conclusion_template=(
            "Title VII of the Civil Rights Act prohibits employment discrimination based on race, color, religion, "
            "sex (including pregnancy, sexual orientation, gender identity per Bostock), and national origin. "
            "Claims proceed under disparate treatment (intentional) or disparate impact (facially neutral policy "
            "with discriminatory effect) frameworks."
        ),
        reasoning_framework=(
            "STEP 1: Identify protected class and alleged adverse action. STEP 2: Apply appropriate framework - "
            "McDonnell Douglas burden-shifting for disparate treatment or Griggs/EEOC guidelines for disparate "
            "impact. STEP 3: Disparate treatment: plaintiff establishes prima facie case, employer articulates "
            "legitimate non-discriminatory reason, plaintiff shows pretext. STEP 4: Disparate impact: plaintiff "
            "shows statistically significant adverse impact (4/5ths rule), employer proves business necessity and "
            "job-relatedness, plaintiff shows less discriminatory alternative. STEP 5: Evaluate mixed-motive "
            "framework if both lawful and unlawful motivations present."
        ),
        key_factors=[
            "Bostock v. Clayton County extended sex discrimination to sexual orientation and gender identity",
            "McDonnell Douglas framework is primary burden-shifting analysis",
            "4/5ths (80%) rule is initial screen for adverse impact",
            "Employer need not prove absence of discrimination - must articulate legitimate reason",
            "Same-actor inference can rebut discrimination claim",
            "EEOC charge filing is administrative prerequisite to lawsuit",
        ],
        primary_authority=[
            "42 USC 2000e - Title VII of the Civil Rights Act of 1964",
            "Bostock v. Clayton County, 590 U.S. ___ (2020)",
            "McDonnell Douglas Corp. v. Green, 411 U.S. 792 (1973)",
            "Griggs v. Duke Power Co., 401 U.S. 424 (1971)",
        ],
        burden_holder="employee_then_employer",
        adversary_position="Employee/EEOC alleges protected class membership motivated adverse employment action.",
        counter_arguments=[
            "Employer articulates legitimate non-discriminatory reason with documentation",
            "Same decision would have been made regardless of protected class",
            "Statistical evidence may be flawed or based on inappropriate comparator groups",
            "Stray remarks without connection to decision maker may not prove discrimination",
            "After-acquired evidence limits remedies even if discrimination proven",
        ],
        resolution_strategy="Implement consistent, documented decision-making processes. Train managers on bias avoidance. Maintain contemporaneous documentation of employment decisions with business rationale.",
        entity_scope="employers_15_plus",
        confidence=0.91,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Bostock v. Clayton County; McDonnell Douglas v. Green",
    ),
    DoctrineBlock(
        topic="workplace_harassment_prevention",
        keywords=["harassment", "hostile_work_environment", "sexual_harassment", "quid_pro_quo", "faragher_ellerth"],
        conclusion_template=(
            "Workplace harassment under Title VII requires conduct that is severe or pervasive enough to create "
            "a hostile work environment. Employers can establish the Faragher-Ellerth affirmative defense by "
            "showing: (1) reasonable care to prevent and correct harassment (policy + training), and (2) employee "
            "unreasonably failed to use employer's complaint procedures."
        ),
        reasoning_framework=(
            "STEP 1: Determine if conduct is based on protected class. STEP 2: Assess severity and pervasiveness "
            "using totality of circumstances (frequency, severity, physically threatening, interference with work). "
            "STEP 3: Distinguish quid pro quo (tangible employment action by supervisor) from hostile environment. "
            "STEP 4: For supervisor harassment resulting in tangible action, employer is strictly liable. "
            "STEP 5: For supervisor harassment without tangible action, evaluate Faragher-Ellerth defense. "
            "STEP 6: For co-worker/third-party harassment, evaluate employer's knowledge and response adequacy."
        ),
        key_factors=[
            "Single incident can be severe enough to constitute harassment",
            "Faragher-Ellerth defense requires both prevention and correction elements",
            "Policy must be distributed, training must be documented",
            "Investigation must be prompt, thorough, and impartial",
            "Remedial action must be reasonably calculated to stop harassment",
            "Retaliation claims often accompany harassment complaints",
        ],
        primary_authority=[
            "Faragher v. City of Boca Raton, 524 U.S. 775 (1998)",
            "Burlington Industries v. Ellerth, 524 U.S. 742 (1998)",
            "Harris v. Forklift Systems, 510 U.S. 17 (1993)",
            "EEOC Enforcement Guidance on Harassment (2024)",
        ],
        burden_holder="employer_defense",
        adversary_position="Employee claims hostile work environment based on protected class. Employer must prove affirmative defense or show conduct was not severe/pervasive.",
        counter_arguments=[
            "Conduct may be offensive but not rise to legally actionable level",
            "Employer promptly investigated and took appropriate corrective action",
            "Employee failed to use available complaint procedures",
            "Alleged conduct was not based on protected class membership",
            "Anti-harassment policy was clear, distributed, and enforced",
        ],
        resolution_strategy="Maintain robust anti-harassment policy with multiple reporting channels. Conduct annual training for all employees, additional training for managers. Investigate complaints within 24-48 hours of receipt.",
        entity_scope="all_employers",
        confidence=0.89,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Faragher v. Boca Raton; Burlington v. Ellerth",
    ),
    DoctrineBlock(
        topic="warn_act_compliance",
        keywords=["warn_act", "layoff", "plant_closing", "mass_layoff", "60_day_notice", "reduction_in_force"],
        conclusion_template=(
            "The federal WARN Act requires 60 days advance written notice before plant closings (50+ employees) "
            "or mass layoffs (500+ employees, or 50-499 if 33%+ of workforce) at a single site. Failure to "
            "provide notice results in back pay and benefits liability for each day of violation, up to 60 days, "
            "plus $500/day civil penalty."
        ),
        reasoning_framework=(
            "STEP 1: Determine if employer has 100+ full-time employees (WARN threshold). "
            "STEP 2: Identify if action constitutes plant closing (50+ at single site) or mass layoff (500+, "
            "or 50-499 representing 33%+ of site workforce). STEP 3: Aggregate related layoffs within 90-day "
            "window (anti-evasion provision). STEP 4: Evaluate narrow exceptions: unforeseeable business "
            "circumstances, faltering company (closings only), natural disaster. STEP 5: Provide written notice "
            "to affected employees, their union representative, state dislocated worker unit, and local government. "
            "STEP 6: Review state mini-WARN requirements which may impose stricter thresholds and longer notice periods."
        ),
        key_factors=[
            "100-employee threshold counts part-timers for coverage but not for triggering events",
            "Single site of employment is key geographic unit for counting",
            "90-day aggregation prevents employers from staggering layoffs to avoid WARN",
            "Exceptions are narrow and require specific factual predicates",
            "State mini-WARN laws may have lower thresholds (CA WARN: 75 employees)",
            "Bumping chains can extend number of affected employees",
        ],
        primary_authority=[
            "29 USC 2101-2109 - Worker Adjustment and Retraining Notification Act",
            "20 CFR Part 639 - WARN regulations",
            "DOL WARN Employer's Guide",
        ],
        burden_holder="employer",
        adversary_position="Employees and government challenge adequacy of notice timing, content, or applicability of exceptions.",
        counter_arguments=[
            "Unforeseeable business circumstances exception may apply if condition was not reasonably foreseeable",
            "Faltering company exception applies when employer actively seeking capital that would avoid closing",
            "Sale of business may transfer WARN obligations to purchaser",
            "Temporary employees and part-time workers excluded from counting",
            "Voluntary departure programs may reduce mandatory WARN count",
        ],
        resolution_strategy="Implement WARN compliance checklist triggered by any headcount reduction discussion. Model employee counts with 90-day aggregation. Coordinate legal review 90+ days before planned action.",
        entity_scope="employers_100_plus",
        confidence=0.90,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="29 USC 2101; 20 CFR 639",
    ),
    DoctrineBlock(
        topic="flight_risk_assessment",
        keywords=["flight_risk", "retention", "attrition_prediction", "talent_loss", "early_warning"],
        conclusion_template=(
            "Flight risk assessment uses predictive analytics combining structural, behavioral, and sentiment "
            "indicators to identify employees likely to leave within 3-12 months. Key predictors include: "
            "time since last promotion (>24 months), compensation below band midpoint, declining engagement scores, "
            "manager change, tenure milestones (1-year, 3-year anniversary effects), and external market demand."
        ),
        reasoning_framework=(
            "STEP 1: Gather structural risk factors: tenure, compensation position, time since promotion, "
            "manager tenure, commute distance, job level. STEP 2: Assess behavioral signals: PTO pattern changes, "
            "decreased meeting attendance, reduced discretionary effort, LinkedIn profile updates. STEP 3: "
            "Incorporate sentiment data: engagement survey trends, skip-level meeting themes, exit interview "
            "patterns from similar profiles. STEP 4: Weight factors using historical turnover correlation "
            "analysis. STEP 5: Score employees on risk continuum (Critical/High/Moderate/Low). "
            "STEP 6: Cross-reference with criticality assessment (impact if person leaves). "
            "STEP 7: Generate prioritized retention intervention list. STEP 8: Track intervention "
            "effectiveness and model accuracy over time."
        ),
        key_factors=[
            "Time since promotion is strongest single predictor in most models",
            "Compensation position (compa-ratio) correlates strongly with voluntary turnover",
            "Manager relationship quality accounts for up to 70% of engagement variance",
            "Tenure cliff effects at 1, 3, and 5 years are empirically validated",
            "External market demand (job posting volume) provides context",
            "Accuracy improves with organization-specific historical calibration",
        ],
        primary_authority=[
            "Bersin/Deloitte People Analytics Research",
            "Visier Workforce Intelligence Studies",
            "Harvard Business Review Analytics Frameworks",
            "SHRM Predictive Analytics Toolkit",
        ],
        burden_holder="hr_analytics_team",
        adversary_position="Privacy concerns about monitoring employee behavior for predictive purposes. Risk of self-fulfilling prophecy if managers treat flagged employees differently.",
        counter_arguments=[
            "Models may embed historical biases in training data",
            "Individual privacy concerns with behavioral monitoring",
            "False positives waste retention resources on non-risks",
            "False negatives miss actual departures damaging credibility",
            "Manager awareness of flight risk scores may alter behavior negatively",
        ],
        resolution_strategy="Build flight risk model using historical turnover data. Validate with holdout sample. Present to managers as retention investment prioritization tool, not surveillance system.",
        entity_scope="all_employers",
        confidence=0.79,
        confidence_stratification=ConfidenceLevel.AGGRESSIVE,
        controlling_precedent="Bersin Research; Visier Analytics",
    ),
    DoctrineBlock(
        topic="organizational_design_principles",
        keywords=["org_design", "span_of_control", "organizational_structure", "restructuring", "delayering"],
        conclusion_template=(
            "Organizational design aligns structure with strategy. Key dimensions include span of control "
            "(optimal 5-9 direct reports for managers, 10-15 for supervisors), organizational layers "
            "(each layer adds communication cost and decision latency), and structural archetype selection "
            "(functional, divisional, matrix, network). Restructuring should follow the Galbraith Star Model: "
            "strategy, structure, processes, rewards, and people."
        ),
        reasoning_framework=(
            "STEP 1: Clarify strategic objectives driving design change. STEP 2: Analyze current state: spans, "
            "layers, role clarity, decision rights, information flows. STEP 3: Benchmark against peer organizations "
            "and industry norms. STEP 4: Design target state using Galbraith Star Model or McKinsey 7-S. "
            "STEP 5: Map transition plan including role changes, reporting line shifts, and RIF implications. "
            "STEP 6: Assess WARN Act and other legal requirements. STEP 7: Develop communication and change "
            "management plan. STEP 8: Implement in phases with feedback loops."
        ),
        key_factors=[
            "Span of control directly impacts management overhead cost",
            "Each additional layer reduces information fidelity by ~25%",
            "Matrix structures require explicit RACI clarity to function",
            "Restructuring fatigue reduces effectiveness of frequent changes",
            "Change management is as important as structural design",
            "Role clarity and decision rights matter more than org chart boxes",
        ],
        primary_authority=[
            "Galbraith Star Model (Designing Organizations, 2014)",
            "McKinsey 7-S Framework",
            "Mintzberg Organizational Configurations",
            "Kates & Galbraith: Designing Your Organization (Jossey-Bass)",
        ],
        burden_holder="hr_and_executive_leadership",
        adversary_position="Employees resist structural change due to uncertainty. Middle management opposes delayering that threatens their positions.",
        counter_arguments=[
            "Frequent restructuring creates change fatigue and disengagement",
            "Matrix structures increase complexity and slow decision-making",
            "Delayering may overburden remaining managers with excessive spans",
            "Structural change alone does not address cultural or process issues",
            "Cost savings from restructuring often offset by productivity loss during transition",
        ],
        resolution_strategy="Conduct thorough current-state analysis before redesign. Align structure to strategy with clear decision rights. Implement robust change management program.",
        entity_scope="all_employers",
        confidence=0.81,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Galbraith Star Model; McKinsey 7-S",
    ),
    DoctrineBlock(
        topic="learning_and_development_roi",
        keywords=["training", "development", "learning", "roi", "kirkpatrick", "upskilling", "reskilling"],
        conclusion_template=(
            "L&D effectiveness is measured using the Kirkpatrick Four-Level Model: (1) Reaction - learner "
            "satisfaction, (2) Learning - knowledge/skill acquisition, (3) Behavior - on-the-job application, "
            "(4) Results - business impact. Phillips adds Level 5: ROI calculation. Average training spend is "
            "$1,200-$1,500 per employee annually; best-in-class exceeds $2,000."
        ),
        reasoning_framework=(
            "STEP 1: Conduct training needs analysis tied to business objectives and competency gaps. "
            "STEP 2: Design learning interventions using 70-20-10 model (experience, exposure, education). "
            "STEP 3: Implement delivery through appropriate modality (instructor-led, e-learning, blended, OJT). "
            "STEP 4: Measure Level 1 (reaction surveys immediately post-training). "
            "STEP 5: Assess Level 2 (pre/post knowledge tests, skill demonstrations). "
            "STEP 6: Evaluate Level 3 (manager observation, 360 feedback 60-90 days post). "
            "STEP 7: Calculate Level 4 (business metric impact: productivity, quality, retention). "
            "STEP 8: Compute ROI (net benefits / program costs * 100) for strategic programs."
        ),
        key_factors=[
            "70-20-10 model allocates learning across experience, social, and formal channels",
            "Level 3 behavior change is where most training programs fail",
            "Manager reinforcement is the #1 predictor of training transfer",
            "Average training ROI is 353% for well-designed programs (ATD research)",
            "Microlearning and spaced repetition improve knowledge retention",
            "Reskilling costs less than external hiring for most role transitions",
        ],
        primary_authority=[
            "Kirkpatrick Four-Level Training Evaluation Model",
            "Phillips ROI Methodology",
            "ATD State of the Industry Report",
            "Bersin Learning & Development Research",
        ],
        burden_holder="learning_and_development_team",
        adversary_position="CFO questions L&D budget ROI. Business leaders see training as time away from production. Employees view mandatory training as compliance burden.",
        counter_arguments=[
            "ROI measurement for soft skills training is methodologically challenging",
            "Isolating training impact from other variables requires experimental design",
            "Self-paced e-learning completion rates average only 15-25%",
            "Training without manager reinforcement wastes 80%+ of investment",
            "Rapidly changing skill requirements may outpace training development cycles",
        ],
        resolution_strategy="Tie all L&D to business objectives with measurable outcomes. Implement manager accountability for training transfer. Measure at all 4 Kirkpatrick levels for strategic programs.",
        entity_scope="all_employers",
        confidence=0.82,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Kirkpatrick Model; ATD Research; Phillips ROI",
    ),
    DoctrineBlock(
        topic="dei_strategy_and_metrics",
        keywords=["diversity", "equity", "inclusion", "belonging", "representation", "dei_metrics"],
        conclusion_template=(
            "DEI strategy requires measurable goals across representation (demographic composition at each level), "
            "equity (pay parity, promotion rates, access to development by demographic group), inclusion (sense "
            "of belonging, psychological safety, engagement gap analysis), and accountability (leader scorecards, "
            "supplier diversity, community impact)."
        ),
        reasoning_framework=(
            "STEP 1: Establish baseline metrics: representation by level, function, and demographic group. "
            "STEP 2: Analyze equity indicators: pay equity regression results, promotion rate ratios, "
            "development investment per demographic group. STEP 3: Measure inclusion through engagement "
            "survey cuts by demographic, inclusion index scores, ERG participation. STEP 4: Set SMART goals "
            "for each dimension with executive sponsor accountability. STEP 5: Implement evidence-based "
            "interventions: structured interviewing, diverse slates (Rooney Rule), sponsorship programs, "
            "bias interrupters. STEP 6: Track progress quarterly with transparent reporting. "
            "STEP 7: Integrate DEI into talent processes (hiring, development, succession, performance)."
        ),
        key_factors=[
            "Representation without inclusion leads to revolving door turnover",
            "Pay equity and promotion equity are measurable equity indicators",
            "Structured processes reduce bias more than training alone",
            "ERGs provide community but should not replace systemic change",
            "Supplier diversity extends DEI impact beyond the workforce",
            "Legal considerations around affirmative action post-SFFA v. Harvard",
        ],
        primary_authority=[
            "EEOC Guidance on Affirmative Action",
            "OFCCP Regulatory Requirements (41 CFR 60)",
            "SHRM DEI Toolkit",
            "McKinsey Diversity Wins Research (2020, 2023)",
        ],
        burden_holder="hr_and_executive_leadership",
        adversary_position="DEI skeptics question business case. Legal landscape post-SFFA creates uncertainty around race-conscious programs. Employees may perceive DEI initiatives as unfair advantage for some groups.",
        counter_arguments=[
            "Post-SFFA legal landscape limits race-conscious employment programs",
            "Diversity training alone has limited impact on actual behavior change",
            "Representation goals may conflict with available talent pipeline demographics",
            "Inclusion measurement relies on subjective self-report data",
            "Political polarization around DEI creates reputational risk regardless of position",
        ],
        resolution_strategy="Implement process-based DEI interventions (structured hiring, diverse slates, bias interrupters) rather than preferential treatment. Measure outcomes transparently. Ensure legal review of all programs.",
        entity_scope="all_employers",
        confidence=0.76,
        confidence_stratification=ConfidenceLevel.AGGRESSIVE,
        controlling_precedent="SFFA v. Harvard; EEOC Guidance; OFCCP Requirements",
    ),
    DoctrineBlock(
        topic="hr_technology_selection",
        keywords=["hris", "hcm", "ats", "lms", "hr_technology", "implementation"],
        conclusion_template=(
            "HR technology selection requires alignment of system capabilities with organizational strategy, "
            "workforce complexity, and integration requirements. Major HCM platforms (Workday, SAP SuccessFactors, "
            "Oracle HCM, UKG, ADP, BambooHR) serve different market segments. Total cost of ownership includes "
            "license fees, implementation (1.5-3x annual license), data migration, training, and ongoing support."
        ),
        reasoning_framework=(
            "STEP 1: Document business requirements across HR domains (core HR, payroll, benefits, talent, "
            "workforce management, analytics). STEP 2: Assess organizational complexity (employee count, "
            "countries, unions, pay structures, regulatory environments). STEP 3: Evaluate vendors through "
            "structured RFP process with weighted scoring criteria. STEP 4: Conduct reference checks with "
            "similar-size organizations in same industry. STEP 5: Calculate 5-year TCO including hidden costs. "
            "STEP 6: Assess integration requirements with existing systems (ERP, payroll, SSO). "
            "STEP 7: Plan phased implementation with change management. STEP 8: Define success metrics and "
            "post-implementation review timeline."
        ),
        key_factors=[
            "Implementation costs typically 1.5-3x annual license fees",
            "Data migration is the highest-risk implementation phase",
            "Change management failures cause 70% of HCM implementation problems",
            "Integration with existing systems is critical success factor",
            "Mobile-first design essential for frontline workforce",
            "AI/ML capabilities becoming table stakes for talent modules",
        ],
        primary_authority=[
            "Gartner Magic Quadrant for Cloud HCM Suites",
            "Josh Bersin HR Technology Market Analysis",
            "Sapient Insights HR Systems Survey",
            "Sierra-Cedar HR Systems Survey",
        ],
        burden_holder="hr_and_it_leadership",
        adversary_position="Vendors oversell capabilities. Implementation timelines and budgets consistently overrun. User adoption is the ultimate success measure.",
        counter_arguments=[
            "Best-of-breed point solutions may outperform integrated suites in specific domains",
            "Cloud HCM requires ongoing subscription cost versus one-time perpetual license",
            "Customization requests increase implementation risk and upgrade complexity",
            "Vendor lock-in limits future flexibility and negotiating leverage",
            "Small organizations may not need enterprise-grade platforms",
        ],
        resolution_strategy="Conduct structured vendor evaluation with weighted criteria. Negotiate comprehensive SLA and implementation guarantees. Plan phased rollout with strong change management.",
        entity_scope="all_employers",
        confidence=0.80,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Gartner/Bersin Market Analysis",
    ),
    DoctrineBlock(
        topic="employee_relations_investigation",
        keywords=["investigation", "complaint", "workplace_misconduct", "due_process", "documentation"],
        conclusion_template=(
            "Workplace investigations must be prompt, thorough, impartial, and well-documented. The investigation "
            "process includes: complaint intake, scope definition, evidence collection, witness interviews, "
            "credibility assessment, findings of fact, and recommended corrective action. Failure to investigate "
            "or inadequate investigation eliminates employer's affirmative defense under Faragher-Ellerth."
        ),
        reasoning_framework=(
            "STEP 1: Receive and document complaint (who, what, when, where, witnesses). "
            "STEP 2: Assess immediate safety/interim measures needed (separation of parties, administrative leave). "
            "STEP 3: Select appropriate investigator (internal HR, legal, or external). "
            "STEP 4: Develop investigation plan (witness list, document requests, interview questions). "
            "STEP 5: Conduct interviews - complainant first, then witnesses, then respondent last. "
            "STEP 6: Collect and preserve documentary evidence. "
            "STEP 7: Assess credibility using objective factors (corroboration, consistency, demeanor, motive). "
            "STEP 8: Make findings of fact based on preponderance of evidence. "
            "STEP 9: Determine policy violations and appropriate corrective action. "
            "STEP 10: Communicate outcomes to parties, close file, monitor for retaliation."
        ),
        key_factors=[
            "Promptness is measured from employer's knowledge of complaint",
            "Thoroughness requires interviewing all relevant witnesses",
            "Impartiality means investigator has no stake in outcome",
            "Documentation protects employer in subsequent litigation",
            "Preponderance of evidence is appropriate standard (not beyond reasonable doubt)",
            "Anti-retaliation monitoring must continue 6-12 months post-investigation",
        ],
        primary_authority=[
            "Faragher v. City of Boca Raton, 524 U.S. 775 (1998)",
            "EEOC Enforcement Guidance on Harassment (2024)",
            "SHRM Investigation Toolkit",
            "AWI (Association of Workplace Investigators) Guiding Principles",
        ],
        burden_holder="employer",
        adversary_position="Complainant alleges inadequate investigation. Respondent alleges unfair process. Both may pursue legal claims.",
        counter_arguments=[
            "Internal investigators may lack perceived independence",
            "Respondent's rights must be balanced with complainant's need for confidentiality",
            "Union employees may have Weingarten rights during investigatory interviews",
            "Investigation documents may be discoverable in subsequent litigation",
            "Over-investigation of minor issues wastes resources and creates anxiety",
        ],
        resolution_strategy="Establish standard investigation protocol. Train investigators. Use consistent documentation templates. Consider external investigators for serious allegations.",
        entity_scope="all_employers",
        confidence=0.88,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Faragher; EEOC 2024 Guidance; AWI Principles",
    ),
    DoctrineBlock(
        topic="total_rewards_strategy",
        keywords=["total_rewards", "total_compensation", "reward_strategy", "employer_value_proposition"],
        conclusion_template=(
            "Total rewards encompasses all elements of the employee value proposition: base compensation, "
            "variable pay, benefits, well-being programs, development opportunities, and work environment. "
            "The WorldatWork Total Rewards model provides the standard framework. Effective strategy aligns "
            "reward allocation with talent strategy and employee preferences."
        ),
        reasoning_framework=(
            "STEP 1: Assess current total rewards allocation across five WorldatWork pillars. "
            "STEP 2: Survey employee preferences and value perceptions. "
            "STEP 3: Benchmark total rewards package against talent competitors. "
            "STEP 4: Align reward strategy with talent segments (differentiate investment). "
            "STEP 5: Model cost scenarios for alternative reward mixes. "
            "STEP 6: Develop communication strategy to improve reward awareness. "
            "STEP 7: Implement total rewards statements to illustrate full value. "
            "STEP 8: Review annually and adjust based on market and workforce changes."
        ),
        key_factors=[
            "Employees typically undervalue benefits by 30-50%",
            "Total rewards statements improve perceived value by 20-30%",
            "Generational preferences differ: flexibility vs. compensation vs. development",
            "Remote work has elevated well-being and flexibility as top drivers",
            "Variable pay at risk motivates differently than guaranteed compensation",
            "Development opportunities are top retention driver for high potentials",
        ],
        primary_authority=[
            "WorldatWork Total Rewards Model",
            "Mercer Total Remuneration Survey",
            "Willis Towers Watson Global Benefits Attitudes Survey",
        ],
        burden_holder="total_rewards_team",
        adversary_position="Employees focus on base pay; employer's total investment is much higher but underappreciated.",
        counter_arguments=[
            "Total rewards statements can backfire if employees feel manipulated",
            "Flexible benefits may increase administrative complexity",
            "One-size-fits-all rewards miss individual preferences",
            "Cost of providing choice (cafeteria plans) may offset perceived value gains",
            "Non-monetary rewards are hard to quantify and compare externally",
        ],
        resolution_strategy="Implement annual total rewards communication. Survey employee preferences. Differentiate rewards by talent segment. Model scenarios with finance partnership.",
        entity_scope="all_employers",
        confidence=0.84,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="WorldatWork Model; Mercer/WTW Research",
    ),
    DoctrineBlock(
        topic="workforce_planning_methodology",
        keywords=["workforce_planning", "headcount", "fte", "demand_forecasting", "supply_analysis", "gap_analysis"],
        conclusion_template=(
            "Strategic workforce planning forecasts future talent demand based on business strategy, analyzes "
            "internal talent supply using attrition and promotion models, identifies gaps, and develops "
            "strategies to close them (build, buy, borrow, bot). Planning horizon should be 1-3 years for "
            "operational and 3-5 years for strategic workforce decisions."
        ),
        reasoning_framework=(
            "STEP 1: Align workforce plan with business strategy and financial plan. "
            "STEP 2: Forecast demand by role, skill, and location using business driver analysis. "
            "STEP 3: Model internal supply using attrition rates, retirement eligibility, and promotion patterns. "
            "STEP 4: Calculate gap (demand minus projected supply). "
            "STEP 5: Develop sourcing strategy for each gap: build (develop internal talent), buy (external hire), "
            "borrow (contingent/contract), or bot (automate). STEP 6: Cost each sourcing strategy with timeline. "
            "STEP 7: Present workforce plan to leadership with scenario analysis. "
            "STEP 8: Implement and monitor quarterly against actuals."
        ),
        key_factors=[
            "Business driver analysis is more accurate than ratio-based headcount forecasting",
            "Retirement eligibility creates predictable but often unplanned supply reduction",
            "Skills-based planning is replacing job-based planning",
            "Contingent workforce provides flexibility but creates engagement and IP risks",
            "Automation potential analysis should accompany all workforce planning",
            "Scenario planning (best/base/worst) more useful than single-point forecast",
        ],
        primary_authority=[
            "SHRM Workforce Planning Toolkit",
            "Bersin Workforce Planning Maturity Model",
            "McKinsey Future of Work Research",
            "World Economic Forum Future of Jobs Report",
        ],
        burden_holder="hr_strategy_team",
        adversary_position="Finance uses simple headcount budgeting. Business leaders plan in roles, not skills. HR struggles to translate business strategy into workforce implications.",
        counter_arguments=[
            "Long-range planning accuracy decreases significantly beyond 2 years",
            "Rapid market changes can invalidate assumptions quickly",
            "Skills taxonomy maintenance requires significant ongoing investment",
            "Build strategies take 12-24 months, too slow for immediate needs",
            "Workforce analytics maturity may not support sophisticated modeling",
        ],
        resolution_strategy="Implement rolling 12-quarter workforce plan updated quarterly. Use skills adjacency analysis for build vs. buy decisions. Model three scenarios minimum.",
        entity_scope="all_employers",
        confidence=0.81,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="SHRM/Bersin Frameworks; WEF Research",
    ),
    DoctrineBlock(
        topic="employee_handbook_essentials",
        keywords=["handbook", "policy", "at_will", "employment_agreement", "workplace_rules"],
        conclusion_template=(
            "Employee handbooks serve as the employer's primary policy communication tool and provide evidence "
            "of notice for Faragher-Ellerth defense, FMLA rights notification, and at-will employment disclaimers. "
            "Essential components include at-will disclaimer, EEO policy, anti-harassment policy with complaint "
            "procedure, FMLA/ADA accommodation policies, and acknowledgment signature page."
        ),
        reasoning_framework=(
            "STEP 1: Include prominent at-will disclaimer (ideally first page and acknowledgment page). "
            "STEP 2: Draft EEO/anti-discrimination policy listing all protected classes (federal + state). "
            "STEP 3: Include comprehensive anti-harassment policy with multiple reporting channels. "
            "STEP 4: Address FMLA, ADA, and other leave policies. STEP 5: Cover compensation policies (pay "
            "periods, overtime, timekeeping). STEP 6: Define conduct expectations and progressive discipline "
            "(without creating implied contract). STEP 7: Include electronic communication and social media "
            "policies. STEP 8: Obtain signed acknowledgment for each employee. "
            "STEP 9: Review annually for legal updates."
        ),
        key_factors=[
            "At-will language must be clear and not contradicted elsewhere in handbook",
            "Disclaimer language should reserve right to modify policies at any time",
            "Anti-harassment policy is evidence element for Faragher-Ellerth defense",
            "Progressive discipline policy should include management discretion language",
            "State-specific requirements vary significantly",
            "Electronic distribution requires proof of receipt",
        ],
        primary_authority=[
            "Woolley v. Hoffmann-La Roche (NJ - handbook as implied contract)",
            "Faragher v. Boca Raton (anti-harassment policy requirement)",
            "NLRA Section 7 (protected concerted activity limits on policies)",
            "NLRB Guidance on Handbook Policies",
        ],
        burden_holder="employer",
        adversary_position="Employee claims handbook created implied contract overriding at-will status. NLRB challenges overbroad policies as chilling Section 7 rights.",
        counter_arguments=[
            "Handbook language can create enforceable implied contract in some states",
            "Overly restrictive policies may violate NLRA Section 7 rights",
            "Social media policies must allow protected concerted activity",
            "Confidentiality policies cannot prohibit discussing wages/working conditions",
            "At-will disclaimer may be undermined by contrary oral promises or practices",
        ],
        resolution_strategy="Annual legal review of handbook for compliance with federal and state law. Obtain signed acknowledgments. Use clear at-will language. Test policies against NLRB standards.",
        entity_scope="all_employers",
        confidence=0.87,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Woolley v. Hoffmann-La Roche; NLRB Handbook Guidance",
    ),
    DoctrineBlock(
        topic="hr_analytics_maturity",
        keywords=["hr_analytics", "people_analytics", "workforce_analytics", "data_driven_hr", "predictive_analytics"],
        conclusion_template=(
            "HR analytics maturity progresses through four stages: (1) Operational Reporting (headcount, turnover "
            "counts), (2) Advanced Reporting (trend analysis, segmentation, benchmarking), (3) Strategic Analytics "
            "(predictive models, causal analysis), (4) Predictive Organization (real-time dashboards, embedded "
            "analytics in manager workflows, organizational network analysis). Most organizations are at Stage 1-2."
        ),
        reasoning_framework=(
            "STEP 1: Assess current analytics maturity using Bersin model. "
            "STEP 2: Establish data governance (definitions, quality, access, privacy). "
            "STEP 3: Build foundational reporting (standardized metrics, automated dashboards). "
            "STEP 4: Develop advanced analytics (statistical analysis, segmentation, benchmarking). "
            "STEP 5: Implement predictive capabilities (turnover prediction, workforce planning models). "
            "STEP 6: Embed analytics into decision workflows (manager self-service, real-time alerts). "
            "STEP 7: Build analytics team competencies (data literacy, statistics, data visualization). "
            "STEP 8: Establish ethical guidelines for people analytics use."
        ),
        key_factors=[
            "Data quality is the #1 barrier to analytics adoption",
            "HR data literacy across the function is typically low",
            "Privacy regulations (GDPR, state laws) constrain analytics approaches",
            "Organizational network analysis reveals informal influence patterns",
            "Correlation does not imply causation - rigorous methodology matters",
            "Executive storytelling is as important as technical analysis",
        ],
        primary_authority=[
            "Bersin People Analytics Maturity Model",
            "SHRM People Analytics Toolkit",
            "Visier Workforce Intelligence Framework",
            "Harvard Business Review People Analytics Research",
        ],
        burden_holder="hr_analytics_team",
        adversary_position="CHRO wants insights yesterday. IT controls data access. Privacy officers constrain analysis. Managers distrust models.",
        counter_arguments=[
            "Advanced analytics requires significant investment in tools and talent",
            "Small organizations lack sufficient data for statistical validity",
            "Algorithm bias in predictive models can create legal liability",
            "Employee trust erodes if analytics perceived as surveillance",
            "Most impactful HR improvements don't require advanced analytics",
        ],
        resolution_strategy="Start with high-impact use cases (turnover prediction, pay equity). Ensure data quality foundation. Build incrementally with quick wins. Partner with finance for credibility.",
        entity_scope="all_employers",
        confidence=0.80,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Bersin Maturity Model; Visier Framework",
    ),
    DoctrineBlock(
        topic="shrm_competency_model",
        keywords=["shrm", "hr_competency", "hr_professional", "behavioral_competency", "hr_skills"],
        conclusion_template=(
            "The SHRM Competency Model defines 9 competencies for HR professionals across technical (HR Expertise, "
            "Business Acumen, Consultation, Critical Evaluation) and behavioral (Leadership & Navigation, Ethical "
            "Practice, Relationship Management, Communication, Global & Cultural Effectiveness) domains. "
            "This model underpins SHRM-CP and SHRM-SCP certifications."
        ),
        reasoning_framework=(
            "STEP 1: Map current HR team competencies against SHRM model. "
            "STEP 2: Assess gaps by competency domain and proficiency level. "
            "STEP 3: Create development plans aligned to priority competency gaps. "
            "STEP 4: Implement learning interventions by competency (formal learning, mentoring, stretch). "
            "STEP 5: Evaluate progress through competency assessments and certification achievement. "
            "STEP 6: Align HR hiring criteria with competency model requirements. "
            "STEP 7: Evolve model as HR function and business needs change."
        ),
        key_factors=[
            "Business Acumen is the most critical growth area for HR professionals",
            "Data literacy and analytics competency increasingly essential",
            "Ethical Practice is foundational — all other competencies depend on it",
            "Consultation skill enables HR to be strategic partner vs. order taker",
            "Certification validates baseline competency but does not replace experience",
            "Technology fluency is a cross-cutting competency becoming table stakes",
        ],
        primary_authority=[
            "SHRM Body of Competency and Knowledge (SHRM BoCK)",
            "SHRM Competency Model (2012, updated 2023)",
            "Dave Ulrich HR Competency Study (RBL Group)",
        ],
        burden_holder="hr_leadership",
        adversary_position="Business leaders view HR as administrative, not strategic. HR professionals may lack business acumen to be credible strategic partners.",
        counter_arguments=[
            "Competency models oversimplify complex professional capabilities",
            "SHRM model may not reflect all organization-specific HR requirements",
            "Certification exam performance does not predict job performance",
            "Behavioral competencies are difficult to measure objectively",
            "Model may not adequately address emerging skills (AI, remote work management)",
        ],
        resolution_strategy="Adopt SHRM model as baseline, customize for organizational context. Use for hiring, development, and succession within HR function. Prioritize Business Acumen and Analytics.",
        entity_scope="hr_function",
        confidence=0.82,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="SHRM BoCK; Ulrich HR Competency Study",
    ),
    DoctrineBlock(
        topic="workers_compensation_management",
        keywords=["workers_comp", "workplace_injury", "return_to_work", "experience_modification", "mod_rate"],
        conclusion_template=(
            "Workers compensation management requires proactive injury prevention, prompt claims reporting, "
            "effective return-to-work programs, and experience modification rate (EMR) optimization. EMR "
            "directly impacts premium costs — an EMR of 1.20 means 20% above industry average. Best-in-class "
            "employers maintain EMR below 0.80 through systematic safety and claims management."
        ),
        reasoning_framework=(
            "STEP 1: Implement safety program with hazard identification and training. "
            "STEP 2: Establish first-report-of-injury protocol (within 24 hours). "
            "STEP 3: Develop transitional duty/return-to-work program. "
            "STEP 4: Monitor claims actively with TPA/carrier partnership. "
            "STEP 5: Analyze claims data for patterns (department, shift, body part, mechanism). "
            "STEP 6: Calculate and track EMR with 3-year claims history. "
            "STEP 7: Implement root cause analysis for all recordable injuries. "
            "STEP 8: Review OSHA 300 log for accuracy and trend identification."
        ),
        key_factors=[
            "EMR is calculated using 3 years of claims data on experience rating worksheet",
            "Frequency of claims impacts EMR more than severity for small employers",
            "Return-to-work programs reduce claim duration by 30-50%",
            "First-report timeliness correlates with lower total claim costs",
            "OSHA recordkeeping requirements apply to employers with 10+ employees",
            "State workers comp laws vary significantly in benefits and procedures",
        ],
        primary_authority=[
            "State Workers Compensation Statutes",
            "NCCI Experience Rating Plan Manual",
            "OSHA Recordkeeping Standards (29 CFR 1904)",
            "BLS Survey of Occupational Injuries and Illnesses",
        ],
        burden_holder="employer_safety_and_hr",
        adversary_position="Injured employee seeks maximum benefits. Employer seeks to manage costs while maintaining duty of care.",
        counter_arguments=[
            "Aggressive claims management can damage employee relations and culture",
            "Transitional duty must accommodate employee's medical restrictions",
            "Fraud investigation must balance with good-faith claims handling",
            "OSHA citation risk if recordkeeping is incomplete or inaccurate",
            "Premium savings from EMR improvement may take 3+ years to materialize",
        ],
        resolution_strategy="Implement comprehensive safety program with leading indicators. Establish transitional duty program. Partner with TPA for proactive claims management. Track EMR quarterly.",
        entity_scope="all_employers",
        confidence=0.86,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="State WC Statutes; NCCI Rating Manual; OSHA 29 CFR 1904",
    ),
    DoctrineBlock(
        topic="remote_hybrid_work_policy",
        keywords=["remote_work", "hybrid", "telecommuting", "work_from_home", "flexible_work"],
        conclusion_template=(
            "Remote/hybrid work policies must address eligibility criteria, schedule expectations, equipment "
            "provisioning, expense reimbursement (required in some states), tax implications of multi-state "
            "work, workers compensation for home office injuries, data security, and performance management "
            "in distributed environments."
        ),
        reasoning_framework=(
            "STEP 1: Define eligibility by role (assess remote-ability based on job requirements). "
            "STEP 2: Establish schedule framework (fully remote, hybrid days, core hours). "
            "STEP 3: Address equipment and technology (employer-provided vs. BYOD, stipend). "
            "STEP 4: Resolve expense reimbursement per state law requirements (CA, IL, others mandate). "
            "STEP 5: Analyze tax nexus implications for multi-state remote employees. "
            "STEP 6: Update workers comp coverage for home office injuries. "
            "STEP 7: Implement data security measures for remote environments. "
            "STEP 8: Train managers on managing distributed teams effectively."
        ),
        key_factors=[
            "State expense reimbursement laws require payment for necessary business expenses",
            "Multi-state remote work creates tax nexus and withholding complexity",
            "Workers comp covers home office injuries during work hours in most states",
            "Data security risk increases with remote work (unsecured networks, shared devices)",
            "Performance management must shift from presence-based to output-based",
            "Manager training is critical for effective hybrid team leadership",
        ],
        primary_authority=[
            "CA Labor Code 2802 (expense reimbursement)",
            "IL Wage Payment and Collection Act (expense reimbursement)",
            "State nexus and withholding rules (vary by state)",
            "SHRM Remote Work Toolkit",
        ],
        burden_holder="employer",
        adversary_position="Employees expect full flexibility. Managers want visibility and control. Tax and compliance teams flag multi-state risks.",
        counter_arguments=[
            "Mandatory return-to-office risks losing talent to flexible competitors",
            "Remote work productivity data is mixed and context-dependent",
            "Multi-state compliance burden disproportionately affects small employers",
            "Hybrid schedules create scheduling complexity and equity concerns",
            "Cultural cohesion and mentoring are harder to maintain remotely",
        ],
        resolution_strategy="Implement role-based remote eligibility assessment. Address state compliance requirements proactively. Train managers on outcome-based performance management. Review policy annually.",
        entity_scope="all_employers",
        confidence=0.78,
        confidence_stratification=ConfidenceLevel.AGGRESSIVE,
        controlling_precedent="State expense reimbursement statutes; state nexus rules",
    ),
    DoctrineBlock(
        topic="okr_kpi_framework",
        keywords=["okr", "kpi", "objectives", "key_results", "performance_metrics", "goal_setting"],
        conclusion_template=(
            "OKRs (Objectives and Key Results) provide strategic alignment through aspirational objectives with "
            "measurable key results, while KPIs (Key Performance Indicators) track ongoing operational performance. "
            "Best practice uses OKRs for quarterly strategic priorities and KPIs for continuous business monitoring. "
            "OKR achievement targets 60-70% to encourage stretch goals."
        ),
        reasoning_framework=(
            "STEP 1: Cascade organizational strategy into department and individual OKRs. "
            "STEP 2: Each objective should be qualitative, inspirational, and time-bound. "
            "STEP 3: Each key result should be quantitative, measurable, and verifiable. "
            "STEP 4: 3-5 objectives per level with 3-5 key results each. "
            "STEP 5: Align vertically (org->team->individual) and horizontally (cross-functional). "
            "STEP 6: Track weekly progress, monthly check-ins, quarterly review. "
            "STEP 7: Score key results (0.0-1.0 scale). "
            "STEP 8: Separate OKR scores from compensation decisions (avoid sandbag incentive)."
        ),
        key_factors=[
            "OKRs should be stretch goals — 60-70% achievement is healthy",
            "Separating OKRs from compensation prevents sandbagging behavior",
            "Transparency (public OKRs) increases alignment and accountability",
            "Weekly check-ins prevent quarter-end surprises",
            "KPIs complement OKRs for operational baseline monitoring",
            "Training on OKR methodology is critical for successful adoption",
        ],
        primary_authority=[
            "John Doerr - Measure What Matters (OKR methodology)",
            "Andy Grove - High Output Management (original OKR framework)",
            "Google OKR Implementation Case Study",
            "Bersin Performance Management Research",
        ],
        burden_holder="hr_and_management",
        adversary_position="Employees treat OKRs as performance targets rather than stretch goals. Managers struggle with measurable key result definition.",
        counter_arguments=[
            "OKR adoption requires significant cultural shift from traditional goals",
            "Quarterly cadence may not align with longer project timelines",
            "Cross-functional alignment is difficult to maintain in practice",
            "Over-measuring can create bureaucracy rather than focus",
            "Some roles have difficulty defining quantifiable key results",
        ],
        resolution_strategy="Implement OKRs with proper training, transparent tracking, and separation from compensation. Start with leadership team, cascade gradually. Coach managers on writing measurable key results.",
        entity_scope="all_employers",
        confidence=0.83,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Doerr/Grove OKR Framework; Google Case Study",
    ),
    DoctrineBlock(
        topic="i9_employment_verification",
        keywords=["i9", "employment_verification", "e_verify", "work_authorization", "immigration"],
        conclusion_template=(
            "Form I-9 employment eligibility verification is required for every employee hired after November 6, 1986. "
            "Section 1 must be completed by the employee on or before the first day of employment. Section 2 must be "
            "completed by the employer within 3 business days of the hire date. I-9 errors are the most common "
            "workplace compliance violation with penalties ranging from $272-$2,507 per form."
        ),
        reasoning_framework=(
            "STEP 1: Employee completes Section 1 on or before first day of employment. "
            "STEP 2: Employer examines acceptable documents from Lists A, B, and C within 3 business days. "
            "STEP 3: Complete Section 2 with document information and certification. "
            "STEP 4: Do not specify which documents employee must present (anti-discrimination). "
            "STEP 5: Reverify expiring work authorization in Section 3 before expiration. "
            "STEP 6: Store I-9s for 3 years after hire date or 1 year after termination, whichever later. "
            "STEP 7: If using E-Verify, submit within 3 business days of hire (mandatory for federal contractors). "
            "STEP 8: Conduct periodic self-audits for I-9 compliance."
        ),
        key_factors=[
            "Over-documentation (asking for more documents than required) is discrimination",
            "Penalties range from $272-$2,507 per substantive violation per form",
            "E-Verify mandatory for federal contractors but voluntary for others in most states",
            "Remote I-9 verification permitted through authorized representatives",
            "Section 3 reverification only for expiring work authorization, not documents",
            "ICE audits (I-9 audits) require 3 business days notice to produce forms",
        ],
        primary_authority=[
            "INA Section 274A (8 USC 1324a) - Employment verification",
            "8 CFR 274a - I-9 requirements",
            "USCIS M-274 Handbook for Employers",
            "INA Section 274B - Anti-discrimination provisions",
        ],
        burden_holder="employer",
        adversary_position="ICE/HSI conducts I-9 audit and imposes penalties for technical and substantive violations.",
        counter_arguments=[
            "Good faith compliance effort may mitigate penalty amounts",
            "Voluntary self-audit demonstrates good faith",
            "Technical violations (minor errors) carry lower penalties than substantive",
            "Anti-discrimination provisions prevent over-documentation",
            "Remote verification procedures add complexity but enable compliance",
        ],
        resolution_strategy="Implement electronic I-9 system with built-in compliance checks. Train all hiring managers. Conduct annual self-audit. Use E-Verify where required or voluntarily for safe harbor.",
        entity_scope="all_employers",
        confidence=0.90,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="8 USC 1324a; 8 CFR 274a; USCIS M-274",
    ),
    DoctrineBlock(
        topic="progressive_discipline_framework",
        keywords=["discipline", "termination", "progressive_discipline", "documentation", "corrective_action"],
        conclusion_template=(
            "Progressive discipline provides a structured, documented approach to addressing performance and "
            "conduct issues: verbal warning, written warning, final written warning/PIP, and termination. "
            "Documentation at each step is critical for legal defensibility. At-will employment preserves "
            "termination discretion but consistent application reduces discrimination claims."
        ),
        reasoning_framework=(
            "STEP 1: Identify the performance gap or conduct violation with specific examples. "
            "STEP 2: Determine appropriate disciplinary level based on severity, history, and precedent. "
            "STEP 3: Deliver feedback privately with clear explanation of issue, expectation, and consequence. "
            "STEP 4: Document the interaction with specific facts, dates, and agreed next steps. "
            "STEP 5: Set measurable improvement expectations with timeline. "
            "STEP 6: Follow up on timeline and document progress or continued deficiency. "
            "STEP 7: Before termination, conduct pre-termination review (checklist: same treatment, "
            "documentation completeness, protected class consideration, retaliation risk). "
            "STEP 8: Involve HR and legal for final termination decisions."
        ),
        key_factors=[
            "At-will employers are not legally required to follow progressive discipline",
            "Consistency in application is the strongest legal defense",
            "Documentation should be specific, factual, and contemporaneous",
            "PIPs should include measurable goals and reasonable timelines (30-90 days)",
            "Certain offenses may warrant immediate termination without progressive steps",
            "Pre-termination checklist prevents disparate treatment claims",
        ],
        primary_authority=[
            "SHRM Progressive Discipline Toolkit",
            "EEOC: Employer Best Practices for Discipline",
            "Restatement of Employment Law - Termination Procedures",
        ],
        burden_holder="employer_management",
        adversary_position="Terminated employee claims discipline was pretextual and motivated by protected class status. Inconsistent application is primary evidence of pretext.",
        counter_arguments=[
            "Progressive discipline may delay necessary termination of poor performers",
            "Rigid application may prevent appropriate response to serious misconduct",
            "PIPs can be perceived as manufactured pretext for predetermined termination",
            "Union grievance procedures may override employer discipline framework",
            "Remote work complicates documentation and monitoring of improvement",
        ],
        resolution_strategy="Implement consistent progressive discipline framework with HR involvement. Document all steps contemporaneously. Conduct pre-termination checklist review. Train managers on documentation standards.",
        entity_scope="all_employers",
        confidence=0.86,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="EEOC Best Practices; Restatement of Employment Law",
    ),
    DoctrineBlock(
        topic="cobra_administration",
        keywords=["cobra", "continuation_coverage", "qualifying_event", "election_notice", "premium"],
        conclusion_template=(
            "COBRA requires employers with 20+ employees to offer continuation of group health coverage for "
            "18-36 months following qualifying events (termination, reduction in hours, divorce, death, Medicare "
            "eligibility, dependent aging out). Employers must provide election notice within 14 days of "
            "qualifying event. Premium may be up to 102% of full cost."
        ),
        reasoning_framework=(
            "STEP 1: Determine COBRA coverage obligation (20+ employees on 50% of working days). "
            "STEP 2: Identify qualifying event type and applicable coverage period. "
            "STEP 3: Provide general notice to new employees at enrollment. "
            "STEP 4: Provide election notice within 14 days of qualifying event (44 days from event total). "
            "STEP 5: Allow 60-day election period from notice date. "
            "STEP 6: First premium payment due 45 days after election. "
            "STEP 7: Subsequent premiums due on first of each month with 30-day grace period. "
            "STEP 8: Track coverage duration and termination events."
        ),
        key_factors=[
            "Employer is responsible even if TPA administers COBRA",
            "Excise tax penalty of $100/day per affected individual for noncompliance",
            "Qualifying events: termination, hours reduction, divorce, Medicare, death, dependent aging out",
            "Coverage duration: 18 months (termination/hours) or 36 months (other events)",
            "Disability extension provides 11 additional months (29 total) at 150% premium",
            "State mini-COBRA laws may apply to smaller employers",
        ],
        primary_authority=[
            "29 USC 1161-1168 - COBRA provisions (ERISA Title I, Part 6)",
            "26 USC 4980B - COBRA excise tax",
            "DOL COBRA Model Notices",
            "IRS Notice 2009-27 (COBRA subsidy guidance)",
        ],
        burden_holder="employer",
        adversary_position="Former employee claims inadequate notice or improper termination of COBRA coverage.",
        counter_arguments=[
            "Employer used compliant model notices provided by DOL",
            "Qualified beneficiary failed to elect within 60-day window",
            "Premium payment was not received within grace period",
            "Coverage properly terminated upon qualifying event cessation",
            "State mini-COBRA provides alternative compliance path for small employers",
        ],
        resolution_strategy="Use DOL model notices. Implement systematic tracking of qualifying events and notice deadlines. Audit TPA compliance quarterly. Train HR on qualifying event identification.",
        entity_scope="employers_20_plus",
        confidence=0.88,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="29 USC 1161-1168; 26 USC 4980B",
    ),
    DoctrineBlock(
        topic="age_discrimination_adea",
        keywords=["adea", "age_discrimination", "older_workers", "disparate_impact_age", "forty_plus"],
        conclusion_template=(
            "The ADEA protects employees 40 and older from age-based discrimination in employment. Unlike Title VII, "
            "the ADEA requires 'but-for' causation after Gross v. FBL Financial (mixed-motive framework does not apply). "
            "RIF/layoff decisions have heightened ADEA scrutiny - statistical analysis of age impact is essential."
        ),
        reasoning_framework=(
            "STEP 1: Verify ADEA coverage (20+ employees). STEP 2: Determine if 'but-for' causation standard "
            "is met - age must be the determinative factor, not merely a motivating factor. "
            "STEP 3: For RIF actions, analyze age distribution of selected vs. retained employees. "
            "STEP 4: Document legitimate, non-discriminatory selection criteria (performance, skills, seniority). "
            "STEP 5: Review for code words and age-related comments in decision documentation. "
            "STEP 6: If offering severance with ADEA waiver, comply with OWBPA requirements (21/45-day "
            "consideration, 7-day revocation, specific statutory language). "
            "STEP 7: Verify compliance with state age discrimination laws."
        ),
        key_factors=[
            "But-for causation is higher burden than Title VII mixed-motive",
            "OWBPA waiver requirements are strictly construed - technical noncompliance voids waiver",
            "Group termination waivers require 45-day consideration and decisional unit disclosure",
            "Statistical evidence of age impact in RIF is persuasive evidence",
            "Remarks about retirement, energy, technology skills can evidence age bias",
            "Replacement by substantially younger worker supports prima facie case",
        ],
        primary_authority=[
            "29 USC 621-634 - Age Discrimination in Employment Act",
            "29 USC 626(f) - Older Workers Benefit Protection Act (OWBPA)",
            "Gross v. FBL Financial Services, 557 U.S. 167 (2009)",
            "Oubre v. Entergy Operations, 522 U.S. 422 (1998)",
        ],
        burden_holder="employee_then_employer",
        adversary_position="Older employee claims age motivated adverse action. Employer must articulate legitimate non-age reason; employee proves but-for causation.",
        counter_arguments=[
            "But-for causation is more difficult for plaintiffs to prove than mixed-motive",
            "Legitimate performance or skills-based criteria may correlate with age without being discriminatory",
            "RIF selection criteria were applied consistently without age consideration",
            "OWBPA waiver was properly executed with all required elements",
            "Replacement employee's age is not itself proof of discrimination",
        ],
        resolution_strategy="Document age-neutral selection criteria for all employment decisions. Run adverse impact analysis before RIF. Comply strictly with OWBPA for any age waiver. Train managers on age-neutral language.",
        entity_scope="employers_20_plus",
        confidence=0.89,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Gross v. FBL Financial; Oubre v. Entergy; OWBPA",
    ),
    DoctrineBlock(
        topic="hay_group_job_evaluation",
        keywords=["hay_method", "job_evaluation", "point_factor", "know_how", "problem_solving", "accountability"],
        conclusion_template=(
            "The Hay Group Guide Chart-Profile Method evaluates jobs on three compensable factors: Know-How "
            "(breadth, depth, human relations skills), Problem Solving (thinking environment, thinking challenge), "
            "and Accountability (freedom to act, magnitude, impact). Each factor uses guide charts with numeric "
            "point values. Jobs with similar total points are grouped into the same grade regardless of function."
        ),
        reasoning_framework=(
            "STEP 1: Evaluate Know-How dimension: technical/specialized knowledge, breadth of management, "
            "and human relations skills required. STEP 2: Evaluate Problem Solving: thinking environment "
            "(how structured) and thinking challenge (how complex). Problem Solving scored as percentage "
            "of Know-How. STEP 3: Evaluate Accountability: freedom to act (supervision level), magnitude "
            "(size of area impacted), and impact type (direct vs. indirect). "
            "STEP 4: Sum factor points for total job size. STEP 5: Analyze profile (uphill = accountability "
            "dominant, flat, or downhill = know-how dominant). STEP 6: Group jobs with similar point totals "
            "into grades. STEP 7: Validate through benchmark job comparison."
        ),
        key_factors=[
            "Three factors capture universal aspects of all jobs",
            "Problem Solving is expressed as percentage of Know-How, not absolute points",
            "Profile shape reveals job character (operational vs. advisory vs. balanced)",
            "Guide charts provide standardized rating scales with step differences of ~15%",
            "Benchmark jobs calibrate the system against market data",
            "System is gender-neutral when properly applied to job content not incumbent",
        ],
        primary_authority=[
            "Hay Group Guide Chart-Profile Method (proprietary methodology)",
            "WorldatWork Job Evaluation Guidelines",
            "EEOC Guidelines on Compensation Discrimination",
        ],
        burden_holder="compensation_team",
        adversary_position="Critics argue point-factor methods are complex, subjective at evaluation stage, and may perpetuate historical biases embedded in factor definitions.",
        counter_arguments=[
            "Simpler market pricing approaches may be more practical for many organizations",
            "Guide chart application requires significant training and calibration",
            "Method was developed decades ago and may not fully capture modern knowledge work",
            "Licensing costs limit accessibility for smaller organizations",
            "Evaluator subjectivity at margin between rating levels persists",
        ],
        resolution_strategy="Use Hay evaluation for establishing internal equity hierarchy. Supplement with market pricing for external competitiveness. Train evaluation committee for consistency. Calibrate with benchmark jobs.",
        entity_scope="all_employers",
        confidence=0.84,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Hay Group Methodology; WorldatWork Standards",
    ),
    DoctrineBlock(
        topic="nlra_protected_concerted_activity",
        keywords=["nlra", "concerted_activity", "section_7", "union", "collective_bargaining", "unfair_labor_practice"],
        conclusion_template=(
            "NLRA Section 7 protects employee rights to engage in concerted activity for mutual aid or protection, "
            "regardless of union status. Protected activities include discussing wages and working conditions, "
            "collective complaints to management, and social media posts about workplace issues. Employer policies "
            "that could be reasonably construed to chill Section 7 rights are unlawful."
        ),
        reasoning_framework=(
            "STEP 1: Determine if activity is 'concerted' (involving or on behalf of multiple employees). "
            "STEP 2: Assess if purpose is 'mutual aid or protection' (related to terms and conditions of employment). "
            "STEP 3: Verify activity has not lost protection (threats, violence, disloyalty, breach of confidentiality "
            "of employer's legitimate trade secrets). STEP 4: Evaluate employer's response under Wright Line burden-shifting "
            "(employer knowledge of protected activity + anti-union animus + nexus to adverse action). "
            "STEP 5: Review employer policies for overbreadth that could chill protected activity."
        ),
        key_factors=[
            "Section 7 rights apply to ALL employees, not just union workplaces",
            "Social media posts about wages/conditions are generally protected",
            "Confidentiality policies cannot prohibit wage/condition discussions",
            "Handbook rules tested for reasonableness under Boeing framework",
            "Individual griping is not protected; must have group purpose",
            "Supervisors excluded from Section 7 protection",
        ],
        primary_authority=[
            "29 USC 157 - NLRA Section 7 rights",
            "29 USC 158 - Unfair labor practices",
            "The Boeing Company, 365 NLRB No. 154 (2017)",
            "Wright Line, 251 NLRB 1083 (1980)",
        ],
        burden_holder="employer",
        adversary_position="Employee/NLRB claims employer's policy or action interfered with Section 7 rights.",
        counter_arguments=[
            "Activity was individual complaint, not concerted",
            "Activity lost protection due to threats, violence, or disloyalty",
            "Employer policy falls within Boeing Category 1 (lawful, justified)",
            "Adverse action was motivated by legitimate business reason, not protected activity",
            "Employee's social media post disclosed trade secrets or proprietary information",
        ],
        resolution_strategy="Review all handbook policies through Boeing framework lens. Train managers that wage discussion is protected. Consult labor counsel before disciplining employees for group complaints.",
        entity_scope="all_employers",
        confidence=0.87,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="NLRA Section 7; Boeing Company; Wright Line",
    ),
    DoctrineBlock(
        topic="interview_scoring_selection",
        keywords=["interview", "structured_interview", "scoring", "selection", "behavioral_interview", "adverse_impact"],
        conclusion_template=(
            "Structured interviews with standardized questions, behavioral anchors, and consistent scoring "
            "rubrics produce the highest validity (r=0.51-0.63) and legal defensibility among selection methods. "
            "Unstructured interviews have low predictive validity (r=0.20-0.38) and create adverse impact risk. "
            "All selection procedures must be job-related and consistent with business necessity per EEOC Guidelines."
        ),
        reasoning_framework=(
            "STEP 1: Conduct job analysis to identify critical competencies and behaviors. "
            "STEP 2: Develop standardized questions targeting each competency (behavioral and situational). "
            "STEP 3: Create scoring rubric with behavioral anchors for each rating level. "
            "STEP 4: Train interviewers on structured process and unconscious bias mitigation. "
            "STEP 5: Conduct interviews with consistent questions and scoring for all candidates. "
            "STEP 6: Aggregate scores across interviewers using structured consensus or averaging. "
            "STEP 7: Monitor adverse impact at each stage using four-fifths rule. "
            "STEP 8: Document selection rationale for each hiring decision."
        ),
        key_factors=[
            "Structured interviews have 2-3x the predictive validity of unstructured",
            "Behavioral questions (past behavior) predict future performance better than hypotheticals",
            "Panel interviews reduce individual interviewer bias",
            "Interview scoring should use 5-point behaviorally anchored rating scale",
            "Adverse impact must be monitored at each selection stage",
            "Documentation of selection criteria and decisions is essential for legal defense",
        ],
        primary_authority=[
            "EEOC Uniform Guidelines on Employee Selection Procedures (29 CFR 1607)",
            "SIOP Principles for Validation and Use of Personnel Selection Procedures",
            "Schmidt & Hunter (1998) meta-analysis on selection method validity",
        ],
        burden_holder="employer",
        adversary_position="Rejected candidate claims selection process had adverse impact on protected class or was applied inconsistently.",
        counter_arguments=[
            "Selection method is job-related and consistent with business necessity",
            "Structured process ensures equal treatment of all candidates",
            "Adverse impact analysis shows no statistically significant disparity",
            "Alternative methods with less adverse impact would not serve business needs equally",
            "Individual hiring decision was based on documented, legitimate criteria",
        ],
        resolution_strategy="Implement structured interview process with job-related questions, scoring rubrics, and interviewer training. Monitor adverse impact quarterly. Document all selection decisions.",
        entity_scope="all_employers",
        confidence=0.86,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="29 CFR 1607; SIOP Principles; Griggs v. Duke Power",
    ),
    DoctrineBlock(
        topic="multi_state_employment_compliance",
        keywords=["multi_state", "state_law", "jurisdiction", "compliance", "employment_law"],
        conclusion_template=(
            "Multi-state employers must comply with the most protective applicable law, which often is state "
            "rather than federal law. Key areas of state variation include: minimum wage, overtime rules, "
            "pay frequency, final pay timing, meal/rest breaks, paid sick leave, pay transparency, "
            "non-compete enforceability, ban-the-box, marijuana, and expense reimbursement."
        ),
        reasoning_framework=(
            "STEP 1: Inventory all jurisdictions where employees are located or work. "
            "STEP 2: Map key employment law requirements by jurisdiction (50 states + DC + territories + "
            "local ordinances). STEP 3: Identify where federal law is floor and state/local law is ceiling. "
            "STEP 4: Apply most protective standard to multi-state policies where feasible. "
            "STEP 5: Create jurisdiction-specific addenda for laws requiring different treatment. "
            "STEP 6: Monitor legislative changes across all jurisdictions (300+ bills annually). "
            "STEP 7: Train local managers on jurisdiction-specific requirements. "
            "STEP 8: Implement compliance calendar with jurisdiction-specific deadlines."
        ),
        key_factors=[
            "State minimum wages range from federal $7.25 to $20+ in some jurisdictions",
            "California, NY, and other states have significantly broader protections than federal",
            "Pay transparency laws expanding rapidly (CO, CA, NY, WA, IL, others)",
            "Non-compete enforceability varies from fully enforceable to banned by state",
            "Paid sick leave mandated in 15+ states and dozens of cities",
            "Remote work adds complexity when employee works in different state than employer",
        ],
        primary_authority=[
            "Various state employment statutes",
            "Littler Mendelson State Law Compendium",
            "SHRM State Law Compliance Toolkit",
            "Jackson Lewis Employment Law Resource Center",
        ],
        burden_holder="employer",
        adversary_position="State DOL or employee alleges violation of state-specific requirement that exceeds federal floor.",
        counter_arguments=[
            "Employer's single national policy may comply with most protective standard",
            "Federal preemption may apply in certain areas (ERISA, NLRA)",
            "Good faith compliance effort may mitigate penalties in some jurisdictions",
            "State law application to out-of-state employer may face jurisdictional challenges",
            "Emerging uniform state law efforts may reduce complexity over time",
        ],
        resolution_strategy="Maintain jurisdiction-specific compliance matrix updated monthly. Apply most protective standard where feasible. Use local counsel for high-risk jurisdictions. Implement legislative monitoring service.",
        entity_scope="multi_state_employers",
        confidence=0.80,
        confidence_stratification=ConfidenceLevel.AGGRESSIVE,
        controlling_precedent="Various state employment statutes",
    ),
    DoctrineBlock(
        topic="onboarding_program_design",
        keywords=["onboarding", "new_hire", "orientation", "first_90_days", "time_to_productivity"],
        conclusion_template=(
            "Strategic onboarding extends beyond Day 1 orientation to a structured 90-day integration program "
            "covering the 4 C's: Compliance (legal/policy), Clarification (role/expectations), Culture "
            "(norms/values), and Connection (relationships/networks). Effective onboarding reduces first-year "
            "turnover by 25-50% and accelerates time-to-productivity by 34% (Brandon Hall research)."
        ),
        reasoning_framework=(
            "STEP 1: Pre-boarding (before Day 1): complete paperwork electronically, set up systems access, "
            "assign buddy, send welcome materials. STEP 2: Day 1: warm welcome, facility tour, equipment setup, "
            "meet team, begin compliance training. STEP 3: Week 1: role clarification meeting with manager, "
            "30-60-90 day plan discussion, introduction to key stakeholders. "
            "STEP 4: Month 1: complete compliance requirements (I-9, benefits enrollment, safety training), "
            "begin role-specific training, first check-in with HR. "
            "STEP 5: Month 2: deeper integration into team and cross-functional relationships, initial "
            "performance feedback. STEP 6: Month 3: 90-day review, performance expectations calibration, "
            "development planning. STEP 7: Measure program effectiveness through new hire surveys, time-to- "
            "productivity metrics, and first-year retention rates."
        ),
        key_factors=[
            "20% of turnover occurs within first 45 days",
            "Manager involvement is the single strongest predictor of onboarding success",
            "Pre-boarding reduces Day 1 administrative burden",
            "Buddy/mentor assignment improves cultural integration",
            "30-60-90 day plan provides structure and clear expectations",
            "Technology enablement (access, equipment) on Day 1 signals organizational competence",
        ],
        primary_authority=[
            "Brandon Hall Onboarding Research",
            "Talya Bauer - Onboarding New Employees (SHRM Foundation)",
            "Bersin Onboarding Frameworks",
            "Aberdeen Group Onboarding Benchmarking",
        ],
        burden_holder="hr_and_hiring_manager",
        adversary_position="New hires report feeling lost, unsupported, and unsure of expectations. Hiring managers are too busy to invest in onboarding.",
        counter_arguments=[
            "Structured onboarding takes manager time away from operational priorities",
            "Over-structured programs may feel bureaucratic to experienced hires",
            "Remote onboarding presents unique challenges for culture and connection",
            "One-size-fits-all programs miss role-specific integration needs",
            "ROI of onboarding investment is difficult to isolate from other factors",
        ],
        resolution_strategy="Implement tiered onboarding: universal foundation (4 C's) plus role-specific tracks. Require manager 30-60-90 day plan discussion. Survey new hires at 30, 60, and 90 days. Track first-year retention.",
        entity_scope="all_employers",
        confidence=0.85,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Brandon Hall Research; SHRM Foundation; Bersin",
    ),
    DoctrineBlock(
        topic="salary_transparency_laws",
        keywords=["pay_transparency", "salary_range", "wage_disclosure", "posting_requirements", "pay_range"],
        conclusion_template=(
            "Pay transparency laws requiring salary range disclosure in job postings have expanded to 10+ states "
            "and multiple cities as of 2026. Employers must include good-faith salary ranges in postings (Colorado, "
            "California, Washington, New York, Illinois, others). Non-compliance penalties range from $500-$250,000 "
            "per violation. Multi-state employers must implement consistent posting practices."
        ),
        reasoning_framework=(
            "STEP 1: Inventory all jurisdictions with pay transparency requirements. "
            "STEP 2: Determine which postings are covered (external, internal, transfers, promotions). "
            "STEP 3: Define 'good faith' salary ranges based on compensation bands and market data. "
            "STEP 4: Ensure ranges are not so broad as to be meaningless (some laws require 'reasonable' ranges). "
            "STEP 5: Update all job posting templates and ATS configurations. "
            "STEP 6: Train recruiters and hiring managers on range communication. "
            "STEP 7: Prepare for current employee inquiries about posted ranges vs. their pay. "
            "STEP 8: Audit existing compensation for internal equity alignment with posted ranges."
        ),
        key_factors=[
            "Laws vary: some require posting only, others require disclosure upon request or after interview",
            "Good faith range must reflect actual pay expectations, not extreme min/max",
            "Remote position postings may be subject to candidate's or employer's jurisdiction",
            "Existing employee pay equity concerns will surface from posted ranges",
            "Compensation band review and cleanup is prerequisite to transparency compliance",
            "Non-compliance risk includes employee complaints, agency enforcement, and private lawsuits",
        ],
        primary_authority=[
            "CO Equal Pay for Equal Work Act (SB 19-085)",
            "CA SB 1162 - Pay Transparency",
            "WA SB 5761 - Pay Range Disclosure",
            "NY Labor Law 194-b - Pay Transparency",
        ],
        burden_holder="employer",
        adversary_position="State DOL or applicant claims employer failed to disclose required salary information or posted misleading ranges.",
        counter_arguments=[
            "Salary ranges reflect good faith expectations at time of posting",
            "Ranges may legitimately vary based on experience and qualifications",
            "Multi-state employer applies most protective standard nationally",
            "Remote work jurisdiction questions remain unsettled in many states",
            "Employer has documented basis for ranges tied to compensation structure",
        ],
        resolution_strategy="Audit and formalize compensation bands before transparency compliance deadline. Post ranges in all covered jurisdictions. Prepare manager talking points for employee pay discussions.",
        entity_scope="all_employers",
        confidence=0.82,
        confidence_stratification=ConfidenceLevel.AGGRESSIVE,
        controlling_precedent="State pay transparency statutes (CO, CA, WA, NY, IL)",
    ),
    DoctrineBlock(
        topic="eeo1_reporting_requirements",
        keywords=["eeo1", "reporting", "component_1", "workforce_data", "demographics"],
        conclusion_template=(
            "The EEO-1 Component 1 report requires employers with 100+ employees (or 50+ if federal contractor) "
            "to annually report workforce demographics by job category, race/ethnicity, and sex. Accurate "
            "reporting requires proper job category mapping, self-identification data collection, and "
            "compliance with filing deadlines."
        ),
        reasoning_framework=(
            "STEP 1: Determine filing obligation (100+ employees or 50+ with federal contract). "
            "STEP 2: Select workforce snapshot date (one pay period in October-December). "
            "STEP 3: Map all positions to 10 EEO-1 job categories. "
            "STEP 4: Collect self-identification data for race/ethnicity and sex. "
            "STEP 5: Prepare separate report for each establishment with 50+ employees. "
            "STEP 6: Prepare consolidated report for headquarters. "
            "STEP 7: File electronically through EEOC filing system by deadline. "
            "STEP 8: Retain reports for audit readiness."
        ),
        key_factors=[
            "10 job categories from Officials/Managers through Service Workers",
            "7 race/ethnicity categories per revised OMB standards",
            "Self-identification is preferred method but visual identification is backup",
            "Multi-establishment employers file Type 4 (headquarters) and Type 8 (each location)",
            "Reports are confidential but may be subpoenaed in litigation",
            "Failure to file can result in compulsory process (court order to file)",
        ],
        primary_authority=[
            "42 USC 2000e-8 - EEO reporting requirements",
            "29 CFR 1602 - EEO-1 regulations",
            "OMB Directive 15 - Race/ethnicity categories",
            "EEOC Filing Instructions",
        ],
        burden_holder="employer",
        adversary_position="EEOC uses EEO-1 data for systemic discrimination investigations. Inaccurate data may trigger audit.",
        counter_arguments=[
            "Self-identification limitations may affect data accuracy",
            "Job category mapping involves judgment calls at margins",
            "Confidentiality protections limit public disclosure of report data",
            "Small establishment exception (fewer than 50) reduces filing burden",
            "Report reflects snapshot date, not annual average workforce",
        ],
        resolution_strategy="Implement automated EEO-1 preparation from HRIS data. Validate job category mappings annually. Ensure self-identification forms are current. File by deadline with quality review.",
        entity_scope="employers_100_plus",
        confidence=0.88,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="42 USC 2000e-8; 29 CFR 1602",
    ),
    DoctrineBlock(
        topic="retirement_plan_401k_administration",
        keywords=["401k", "retirement", "fiduciary", "erisa", "matching", "vesting", "safe_harbor"],
        conclusion_template=(
            "401(k) plan administration requires ERISA fiduciary compliance including prudent investment selection, "
            "reasonable fee monitoring, accurate recordkeeping, and timely contribution remittance. Safe harbor "
            "plans (3% QNEC or 4% match) avoid ADP/ACP nondiscrimination testing. Plan sponsors have fiduciary "
            "liability for investment selection and fee reasonableness."
        ),
        reasoning_framework=(
            "STEP 1: Establish plan governance committee with documented charter and fiduciary training. "
            "STEP 2: Select and monitor investment lineup using prudent process (not outcomes). "
            "STEP 3: Benchmark fees against comparable plans (Form 5500 data, industry surveys). "
            "STEP 4: Ensure timely remittance of employee contributions (DOL safe harbor: 7 business days). "
            "STEP 5: Conduct annual nondiscrimination testing (ADP/ACP) or adopt safe harbor design. "
            "STEP 6: File Form 5500 annually with required schedules and audit for 100+ participants. "
            "STEP 7: Distribute summary plan descriptions and required participant notices. "
            "STEP 8: Correct any operational errors using IRS EPCRS (SCP, VCP, or Audit CAP)."
        ),
        key_factors=[
            "Fiduciary liability extends to investment selection and fee monitoring",
            "Fee litigation has dramatically increased - document benchmarking process",
            "Safe harbor 401(k) eliminates testing burden but requires employer contributions",
            "Timely contribution remittance is strict liability - no excuses",
            "Auto-enrollment with auto-escalation dramatically increases participation",
            "SECURE 2.0 Act changes (2024-2026) expanding coverage and features",
        ],
        primary_authority=[
            "29 USC 1001-1461 - ERISA",
            "26 USC 401(k) - 401(k) plan requirements",
            "DOL Regulation 2550.404a-5 (fee disclosure)",
            "IRS Rev. Proc. 2021-30 (EPCRS)",
        ],
        burden_holder="plan_sponsor_fiduciary",
        adversary_position="Participants allege excessive fees, imprudent investments, or operational errors. DOL and IRS conduct plan audits.",
        counter_arguments=[
            "Documented prudent process demonstrates fiduciary compliance",
            "Regular fee benchmarking shows reasonable cost monitoring",
            "Investment performance evaluated relative to benchmarks over appropriate periods",
            "EPCRS self-correction available for operational errors discovered in timely manner",
            "Safe harbor design eliminates nondiscrimination testing risk",
        ],
        resolution_strategy="Establish fiduciary governance committee. Document investment review and fee benchmarking annually. Implement safe harbor design if testing risk is material. Use EPCRS promptly for any errors.",
        entity_scope="all_employers_with_plan",
        confidence=0.87,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="ERISA; IRC 401(k); DOL Reg 2550.404a-5",
    ),
]

# Build keyword index for fast doctrine lookup
_DOCTRINE_INDEX: Dict[str, List[int]] = defaultdict(list)
for _idx, _doc in enumerate(DOCTRINE_CACHE):
    for _kw in _doc.keywords:
        _DOCTRINE_INDEX[_kw].append(_idx)
