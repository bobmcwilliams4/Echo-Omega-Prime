"""
R11 Penalty Calculator — TIE-20 Gold Standard Engine
=====================================================

Regulatory penalty calculation, assessment, and mitigation analysis for
oil & gas violations under 16 TAC Chapter 3, TCEQ enforcement, EPA civil
penalties, and OSHA citations. Computes penalty ranges with gravity adjustments,
compliance history multipliers, cooperation credits, and economic benefit recovery.

Engine ID: R11
Port: 8711
Domain: regulatory_penalty_calculation
Version: 2.0.0
TIE Components: 20/20

Authority Hierarchy:
  16 TAC §3.107 (RRC Penalties): weight 10
  TX Nat. Res. Code §81.0531: weight 9
  40 CFR §19.4 (EPA Civil Penalties): weight 9
  29 CFR §1903.15 (OSHA Citations): weight 8
  TCEQ Penalty Policy (RG-253): weight 7
  EPA Penalty Policy Guidance: weight 6
  Case Law Precedent: weight 5

ECHO OMEGA PRIME — Commander Bobby Don McWilliams II
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import sys
import time
import uuid
from collections import defaultdict
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import uvicorn
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import BaseModel, Field

# ═══════════════════════════════════════════════════════════════════════════════
# PATH SETUP
# ═══════════════════════════════════════════════════════════════════════════════
ENGINE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ENGINE_DIR))
sys.path.insert(0, str(ENGINE_DIR.parent / "_shared"))

import doctrines
import telemetry as telem_mod
from doctrines import DOCTRINE_BLOCKS

try:
    from semantic import normalize_query, extract_keywords
except ImportError:
    def normalize_query(q: str) -> str: return q.lower().strip()
    def extract_keywords(q: str) -> List[str]: return q.lower().split()

try:
    from search import search_penalty_precedents, calculate_relevance_score
except ImportError:
    async def search_penalty_precedents(*a, **kw): return []
    def calculate_relevance_score(q, d): return 0.0

try:
    from cloud_retriever import CognitionCloudRetriever
except ImportError:
    CognitionCloudRetriever = None

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
ENGINE_ID = "R11"
ENGINE_NAME = "Penalty Calculator"
ENGINE_VERSION = "2.0.0"
ENGINE_PORT = 8711
ENGINE_DOMAIN = "regulatory_penalty_calculation"

CONFIG_PATH = ENGINE_DIR / "config.json"
AUDIT_LOG_DIR = ENGINE_DIR / "logs"
AUDIT_LOG_DIR.mkdir(parents=True, exist_ok=True)

_config: Dict[str, Any] = {}
if CONFIG_PATH.exists():
    with open(CONFIG_PATH, "r", encoding="utf-8") as _f:
        _config = json.load(_f)

# ═══════════════════════════════════════════════════════════════════════════════
# LOGGING (TIE-18)
# ═══════════════════════════════════════════════════════════════════════════════
logger.remove()
logger.add(sys.stderr, format="<green>{time:HH:mm:ss}</green> | <level>{level:<8}</level> | <cyan>R11</cyan> | {message}", level="INFO")
logger.add(AUDIT_LOG_DIR / "r11_engine.log", rotation="10 MB", retention="30 days", level="DEBUG")

# ═══════════════════════════════════════════════════════════════════════════════
# BANNED PHRASES — Epistemic Guardrails
# ═══════════════════════════════════════════════════════════════════════════════
BANNED_PHRASES = [
    "exact penalty will be", "guaranteed fine of", "definitely assessed at",
    "no penalty possible", "impossible to be fined", "always dismissed",
    "zero chance of enforcement", "100% penalty reduction", "guaranteed waiver",
]

# ═══════════════════════════════════════════════════════════════════════════════
# PYDANTIC MODELS (TIE-17)
# ═══════════════════════════════════════════════════════════════════════════════


class ViolationType(str, Enum):
    UNPLUGGED_WELL = "unplugged_well"
    POLLUTION = "pollution"
    UNAUTHORIZED_DISPOSAL = "unauthorized_disposal"
    FAILURE_TO_FILE = "failure_to_file"
    OPERATING_WITHOUT_PERMIT = "operating_without_permit"
    FAILURE_TO_PLUG = "failure_to_plug"
    BOND_VIOLATION = "bond_violation"
    SPACING_VIOLATION = "spacing_violation"
    FLARING_VIOLATION = "flaring_violation"
    H2S_VIOLATION = "h2s_violation"
    OVERPRODUCTION = "overproduction"
    INJECTION_VIOLATION = "injection_violation"


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=5000)
    mode: str = Field(default="FAST", description="FAST | DEFENSE | MEMO")
    zone: str = Field(default="REPORTING", description="PLANNING | REPORTING | AUDIT")
    include_cloud: bool = Field(default=True)
    trace_id: Optional[str] = None


class PenaltyRequest(BaseModel):
    violation_type: str = Field(..., description="Type of violation")
    days_in_violation: int = Field(1, ge=1, description="Days violation persisted")
    prior_violations: int = Field(0, ge=0, description="Number of prior violations")
    environmental_harm: bool = Field(False)
    public_health_risk: bool = Field(False)
    cooperation: bool = Field(True)
    self_reported: bool = Field(False)
    economic_benefit: float = Field(0.0, ge=0.0, description="Economic benefit gained from violation")
    ability_to_pay: Optional[str] = Field(None, description="small_operator | mid_size | major")
    mode: str = Field(default="FAST")
    zone: str = Field(default="REPORTING")


class AuthorityCitation(BaseModel):
    authority: str
    weight: int
    level: str


class FactFragilityScore(BaseModel):
    claim: str
    verifiability: float
    recharacterization_risk: float
    testimony_dependence: float
    overall_fragility: float
    warning: Optional[str] = None


class PenaltyResponse(BaseModel):
    engine_id: str = ENGINE_ID
    engine_version: str = ENGINE_VERSION
    query_id: str
    trace_id: str
    timestamp: str
    # Penalty calculation
    violation_type: str
    base_penalty: float
    gravity_adjustment: float
    history_multiplier: float
    cooperation_credit: float
    self_report_credit: float
    ability_to_pay_adjustment: float
    economic_benefit_recovery: float
    per_day_penalty: float
    total_penalty: float
    penalty_range_min: float
    penalty_range_max: float
    statutory_maximum: float
    # Authority
    primary_authority: str
    authorities: List[AuthorityCitation] = []
    confidence: float
    confidence_zone: str
    # Analysis
    response_mode: str
    analysis_zone: str
    layer_used: str
    latency_ms: float
    # Doctrine
    doctrine_matches: List[Dict[str, Any]] = []
    issue_categories: List[str] = []
    strata: Dict[str, List[str]] = {}
    # Mitigation & recommendations
    mitigation_options: List[str] = []
    aggravating_factors: List[str] = []
    enforcement_actions: List[str] = []
    reasoning: str = ""
    recommendation: str = ""
    # Epistemic
    epistemic_warnings: List[str] = []
    disclosure_caveat: Optional[str] = None
    fact_fragility: List[FactFragilityScore] = []
    # Determinism
    determinism_hash: str = ""


class HealthResponse(BaseModel):
    engine_id: str
    engine_name: str
    version: str
    status: str
    uptime_seconds: float
    doctrine_count: int
    port: int
    domain: str
    cloud_available: bool
    total_queries: int
    error_rate: float
    avg_latency_ms: float
    coverage_pct: float
    guardrails_active: bool


# ═══════════════════════════════════════════════════════════════════════════════
# TIE-4: AUTHORITY HARDENING
# ═══════════════════════════════════════════════════════════════════════════════

class AuthorityLevel(str, Enum):
    STATUTORY = "STATUTORY"
    REGULATORY = "REGULATORY"
    AGENCY_POLICY = "AGENCY_POLICY"
    CASE_LAW = "CASE_LAW"
    GUIDANCE = "GUIDANCE"


AUTHORITY_WEIGHTS = {
    "16 TAC §3.107": ("REGULATORY", 10),
    "TX Natural Resources Code §81.0531": ("STATUTORY", 9),
    "TX Natural Resources Code §85.381": ("STATUTORY", 9),
    "40 CFR Part 19": ("REGULATORY", 9),
    "29 CFR §1903.15": ("REGULATORY", 8),
    "TCEQ Penalty Policy RG-253": ("AGENCY_POLICY", 7),
    "EPA Civil Penalty Policy": ("AGENCY_POLICY", 6),
    "RRC Enforcement Guidelines": ("GUIDANCE", 5),
}


def classify_authority(citation: str) -> Tuple[str, int]:
    if citation in AUTHORITY_WEIGHTS:
        return AUTHORITY_WEIGHTS[citation]
    cl = citation.lower()
    if "tac" in cl or "cfr" in cl:
        return ("REGULATORY", 8)
    elif "code" in cl:
        return ("STATUTORY", 9)
    elif "policy" in cl:
        return ("AGENCY_POLICY", 6)
    elif "v." in cl:
        return ("CASE_LAW", 5)
    return ("GUIDANCE", 4)


def build_citations(authorities: List[str]) -> List[AuthorityCitation]:
    result = []
    for auth in authorities:
        level, weight = classify_authority(auth)
        result.append(AuthorityCitation(authority=auth, weight=weight, level=level))
    return sorted(result, key=lambda c: c.weight, reverse=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TIE-5: CONFIDENCE STRATIFICATION
# ═══════════════════════════════════════════════════════════════════════════════

def stratify_confidence(score: float) -> str:
    if score >= 0.90: return "DEFENSIBLE"
    if score >= 0.70: return "AGGRESSIVE"
    if score >= 0.50: return "DISCLOSURE"
    return "HIGH_RISK"


def compute_penalty_confidence(
    has_clear_statute: bool,
    has_precedent: bool,
    fact_certainty: float,
    regulatory_ambiguity: bool,
) -> float:
    base = 0.5
    if has_clear_statute: base += 0.25
    if has_precedent: base += 0.15
    base += fact_certainty * 0.1
    if regulatory_ambiguity: base -= 0.15
    return min(1.0, max(0.0, base))


# ═══════════════════════════════════════════════════════════════════════════════
# TIE-13: ZONED ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════

class AnalysisZone(str, Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"


ZONE_PREFIX = {"PLANNING": "PLANNING ADVISORY: ", "REPORTING": "PENALTY REPORT: ", "AUDIT": "AUDIT FINDING: "}


def validate_zone(zone: str) -> AnalysisZone:
    try:
        return AnalysisZone(zone.upper())
    except ValueError:
        return AnalysisZone.REPORTING


# ═══════════════════════════════════════════════════════════════════════════════
# TIE-14: FACT FRAGILITY
# ═══════════════════════════════════════════════════════════════════════════════

def score_fragility(claim: str, documentary: bool, testimony: bool, ambiguous: bool) -> FactFragilityScore:
    v = 0.9 if documentary else 0.4
    r = 0.6 if ambiguous else 0.2
    t = 0.7 if testimony else 0.1
    overall = (1.0 - v) * 0.35 + r * 0.35 + t * 0.30
    warning = None
    if overall > 0.6:
        warning = "HIGH FRAGILITY: Penalty calculation inputs may be challenged."
    return FactFragilityScore(claim=claim, verifiability=round(v, 3), recharacterization_risk=round(r, 3),
                              testimony_dependence=round(t, 3), overall_fragility=round(overall, 3), warning=warning)


# ═══════════════════════════════════════════════════════════════════════════════
# TIE-16: DETERMINISM HASH
# ═══════════════════════════════════════════════════════════════════════════════

def compute_hash(violation_type: str, days: int, prior: int, env_harm: bool, coop: bool, mode: str) -> str:
    content = json.dumps({"v": violation_type, "d": days, "p": prior, "e": env_harm, "c": coop, "m": mode, "ver": ENGINE_VERSION}, sort_keys=True)
    return hashlib.sha256(content.encode()).hexdigest()


# ═══════════════════════════════════════════════════════════════════════════════
# TIE-9: DRIFT WATCHER
# ═══════════════════════════════════════════════════════════════════════════════

class DriftWatcher:
    def __init__(self, topics: List[str]):
        self.all_topics = set(topics)
        self.triggered: Dict[str, int] = defaultdict(int)
        self.misses = 0
        self.total = 0

    def hit(self, topic: str):
        self.triggered[topic] += 1
        self.total += 1

    def miss(self):
        self.misses += 1
        self.total += 1

    def report(self) -> Dict:
        never = sorted(self.all_topics - set(self.triggered))
        cov = 1.0 - (len(never) / len(self.all_topics)) if self.all_topics else 0
        return {"coverage_pct": round(cov * 100, 1), "never_triggered": never, "miss_rate": round(self.misses / max(self.total, 1), 4),
                "top": sorted(self.triggered.items(), key=lambda x: x[1], reverse=True)[:10]}


# ═══════════════════════════════════════════════════════════════════════════════
# TIE-10: COVERAGE MAP
# ═══════════════════════════════════════════════════════════════════════════════

class CoverageMap:
    def __init__(self, blocks):
        self.blocks = {b.topic: b for b in blocks}
        self.triggered: Dict[str, int] = defaultdict(int)
        self.gaps: List[str] = []

    def trigger(self, topic: str):
        self.triggered[topic] += 1

    def gap(self, query: str):
        if len(self.gaps) < 500:
            self.gaps.append(query)

    def report(self) -> Dict:
        total = len(self.blocks)
        covered = len(self.triggered)
        return {"total": total, "covered": covered, "pct": round(covered / max(total, 1) * 100, 1), "gaps": len(self.gaps), "recent_gaps": self.gaps[-5:]}


# ═══════════════════════════════════════════════════════════════════════════════
# PENALTY CALCULATION ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

# Base penalty per violation type per day (16 TAC §3.107 framework)
PENALTY_BASES: Dict[str, float] = {
    "unplugged_well": 1000.0, "pollution": 5000.0, "unauthorized_disposal": 10000.0,
    "failure_to_file": 500.0, "operating_without_permit": 2500.0, "failure_to_plug": 1000.0,
    "bond_violation": 1500.0, "spacing_violation": 2000.0, "flaring_violation": 3000.0,
    "h2s_violation": 7500.0, "overproduction": 1500.0, "injection_violation": 5000.0,
}

# Statutory maximum per day per violation
STATUTORY_MAX_PER_DAY: Dict[str, float] = {
    "rrc": 10000.0,   # 16 TAC §3.107
    "tceq": 25000.0,  # TX Water Code §7.102
    "epa": 101439.0,  # 40 CFR Part 19 (2024 adjusted)
    "osha": 16131.0,  # OSHA max per serious violation (2024 adjusted)
}

GRAVITY_FACTORS = {
    "environmental_harm": 1.5, "public_health": 2.0,
    "willful": 3.0, "repeat_offender": 2.0,
    "death_or_injury": 5.0, "aquifer_contamination": 4.0,
}

MITIGATION_FACTORS = {
    "cooperation": 0.75, "self_report": 0.50,
    "immediate_correction": 0.60, "first_offense": 0.85,
    "good_faith": 0.80, "small_operator": 0.70,
    "financial_hardship": 0.65, "voluntary_disclosure": 0.50,
}


def calculate_penalty(req: PenaltyRequest) -> Dict[str, Any]:
    """
    Core penalty calculation with all TIE-20 adjustments.

    Formula: total = (base * gravity * history * cooperation * self_report * ability) * days + econ_benefit
    Capped at statutory maximum.
    """
    vtype = req.violation_type.lower().replace(" ", "_")
    base = PENALTY_BASES.get(vtype, 1000.0)

    # Gravity adjustment
    gravity = 1.0
    aggravating: List[str] = []
    if req.environmental_harm:
        gravity *= GRAVITY_FACTORS["environmental_harm"]
        aggravating.append("Environmental harm (1.5x)")
    if req.public_health_risk:
        gravity *= GRAVITY_FACTORS["public_health"]
        aggravating.append("Public health risk (2.0x)")

    # History multiplier (25% increase per prior violation, capped at 3x)
    history = min(3.0, 1.0 + (req.prior_violations * 0.25))
    if req.prior_violations > 0:
        aggravating.append(f"Prior violations: {req.prior_violations} ({history:.2f}x)")

    # Cooperation credit
    coop = MITIGATION_FACTORS["cooperation"] if req.cooperation else 1.0
    mitigation: List[str] = []
    if req.cooperation:
        mitigation.append("Cooperation with investigation (-25%)")

    # Self-report credit
    self_report = MITIGATION_FACTORS["self_report"] if req.self_reported else 1.0
    if req.self_reported:
        mitigation.append("Self-reported violation (-50%)")

    # Ability to pay
    atp = 1.0
    if req.ability_to_pay == "small_operator":
        atp = MITIGATION_FACTORS["small_operator"]
        mitigation.append("Small operator adjustment (-30%)")
    elif req.ability_to_pay == "financial_hardship":
        atp = MITIGATION_FACTORS["financial_hardship"]
        mitigation.append("Financial hardship (-35%)")

    # Per-day penalty
    per_day = base * gravity * history * coop * self_report * atp

    # Total with days
    subtotal = per_day * req.days_in_violation

    # Add economic benefit recovery
    total = subtotal + req.economic_benefit

    # Statutory maximum
    stat_max = STATUTORY_MAX_PER_DAY.get("rrc", 10000.0) * req.days_in_violation
    total = min(total, stat_max)

    # Range estimation (50%-150% of calculated, within statutory limits)
    range_min = max(base * 0.5, total * 0.5)
    range_max = min(total * 1.5, stat_max)

    # Enforcement actions based on severity
    enforcement = ["Notice_of_Violation"]
    if total > 50000:
        enforcement = ["Administrative_Penalty", "Compliance_Order", "Permit_Suspension"]
    elif total > 10000:
        enforcement = ["Administrative_Penalty", "Compliance_Order"]
    elif total > 5000:
        enforcement = ["Notice_of_Violation", "Administrative_Penalty"]

    if req.prior_violations >= 3:
        mitigation.append("WARNING: Repeat offender status may trigger enhanced enforcement")
        if "Permit_Suspension" not in enforcement:
            enforcement.append("Permit_Suspension")

    return {
        "base": base, "gravity": gravity, "history": history, "coop": coop,
        "self_report": self_report, "atp": atp, "per_day": round(per_day, 2),
        "total": round(total, 2), "range_min": round(range_min, 2), "range_max": round(range_max, 2),
        "stat_max": stat_max, "mitigation": mitigation, "aggravating": aggravating,
        "enforcement": enforcement, "econ_benefit": req.economic_benefit,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# EPISTEMIC GUARDRAILS
# ═══════════════════════════════════════════════════════════════════════════════

def apply_guardrails(text: str, confidence: float) -> Tuple[str, List[str], Optional[str]]:
    warnings: List[str] = []
    disclosure = None
    for phrase in BANNED_PHRASES:
        if phrase.lower() in text.lower():
            text = text.replace(phrase, "[EPISTEMIC OVERRIDE]")
            warnings.append(f"Removed: '{phrase}'")
    if confidence < 0.5:
        disclosure = ("DISCLOSURE: Penalty estimates involve significant discretion. Actual penalties depend on "
                      "agency interpretation, settlement negotiations, and specific facts. Consult regulatory counsel.")
    return text, warnings, disclosure


# ═══════════════════════════════════════════════════════════════════════════════
# RESPONSE BUILDERS (TIE-2: FAST/DEFENSE/MEMO)
# ═══════════════════════════════════════════════════════════════════════════════

def build_summary(calc: Dict, req: PenaltyRequest, zone: AnalysisZone, confidence: float) -> str:
    prefix = ZONE_PREFIX.get(zone.value, "")
    conf_zone = stratify_confidence(confidence)

    if req.mode == "FAST":
        return (
            f"{prefix}Violation: {req.violation_type}. "
            f"Estimated penalty: ${calc['total']:,.2f} (range: ${calc['range_min']:,.2f}-${calc['range_max']:,.2f}). "
            f"Confidence: {confidence:.0%} ({conf_zone}). "
            f"Primary authority: 16 TAC §3.107."
        )
    elif req.mode == "DEFENSE":
        lines = [
            f"{prefix}PENALTY ASSESSMENT — {req.violation_type}",
            f"Confidence: {confidence:.0%} ({conf_zone})",
            "",
            f"BASE PENALTY: ${calc['base']:,.2f}/day",
            f"GRAVITY ADJUSTMENT: {calc['gravity']:.2f}x",
            f"HISTORY MULTIPLIER: {calc['history']:.2f}x (prior violations: {req.prior_violations})",
            f"COOPERATION CREDIT: {calc['coop']:.2f}x",
            f"SELF-REPORT CREDIT: {calc['self_report']:.2f}x",
            f"ABILITY-TO-PAY: {calc['atp']:.2f}x",
            f"DAYS IN VIOLATION: {req.days_in_violation}",
            f"ECONOMIC BENEFIT: ${calc['econ_benefit']:,.2f}",
            "",
            f"PER-DAY PENALTY: ${calc['per_day']:,.2f}",
            f"TOTAL PENALTY: ${calc['total']:,.2f}",
            f"RANGE: ${calc['range_min']:,.2f} — ${calc['range_max']:,.2f}",
            f"STATUTORY MAX: ${calc['stat_max']:,.2f}",
            "",
            "AUTHORITIES:",
            "  [REGULATORY W:10] 16 TAC §3.107 — RRC Administrative Penalties",
            "  [STATUTORY W:9] TX Nat. Res. Code §81.0531 — Penalty Authority",
            "",
            "MITIGATING FACTORS:",
        ]
        for m in calc["mitigation"]:
            lines.append(f"  - {m}")
        if calc["aggravating"]:
            lines.append("\nAGGRAVATING FACTORS:")
            for a in calc["aggravating"]:
                lines.append(f"  - {a}")
        return "\n".join(lines)
    else:  # MEMO
        lines = [
            "=" * 60,
            "PENALTY CALCULATION MEMORANDUM",
            f"Engine: {ENGINE_ID} {ENGINE_NAME} v{ENGINE_VERSION}",
            f"Date: {datetime.utcnow().strftime('%Y-%m-%d')}",
            "=" * 60,
            "",
            "I. VIOLATION IDENTIFICATION",
            f"   Type: {req.violation_type}",
            f"   Duration: {req.days_in_violation} days",
            f"   Prior Violations: {req.prior_violations}",
            f"   Environmental Harm: {'Yes' if req.environmental_harm else 'No'}",
            f"   Public Health Risk: {'Yes' if req.public_health_risk else 'No'}",
            "",
            "II. PENALTY CALCULATION",
            f"   Base Rate: ${calc['base']:,.2f} per day",
            f"   Gravity Adjustment: {calc['gravity']:.2f}x",
            f"   History Multiplier: {calc['history']:.2f}x",
            f"   Cooperation Credit: {calc['coop']:.2f}x",
            f"   Self-Report Credit: {calc['self_report']:.2f}x",
            f"   Ability-to-Pay: {calc['atp']:.2f}x",
            f"   Per-Day Adjusted: ${calc['per_day']:,.2f}",
            f"   Subtotal ({req.days_in_violation} days): ${calc['per_day'] * req.days_in_violation:,.2f}",
            f"   Economic Benefit Recovery: ${calc['econ_benefit']:,.2f}",
            f"   TOTAL: ${calc['total']:,.2f}",
            "",
            "III. RANGE ANALYSIS",
            f"   Minimum: ${calc['range_min']:,.2f}",
            f"   Calculated: ${calc['total']:,.2f}",
            f"   Maximum: ${calc['range_max']:,.2f}",
            f"   Statutory Cap: ${calc['stat_max']:,.2f}",
            "",
            "IV. APPLICABLE AUTHORITIES",
            "   - 16 TAC §3.107 — Administrative penalties up to $10,000/day/violation",
            "   - TX Natural Resources Code §81.0531 — Penalty authority and procedures",
            "   - TX Natural Resources Code §85.381 — Additional penalty provisions",
            "   - RRC Enforcement Guidelines — Agency discretion framework",
            "",
            "V. MITIGATING FACTORS",
        ]
        for m in calc["mitigation"]:
            lines.append(f"   - {m}")
        lines.append("")
        lines.append("VI. AGGRAVATING FACTORS")
        for a in calc["aggravating"]:
            lines.append(f"   - {a}")
        if not calc["aggravating"]:
            lines.append("   None identified")
        lines.append("")
        lines.append("VII. ENFORCEMENT ACTIONS")
        for e in calc["enforcement"]:
            lines.append(f"   - {e}")
        lines.append("")
        lines.append("VIII. RECOMMENDATION")
        if req.cooperation:
            lines.append("   Operator cooperation noted. Settlement at lower end of range may be appropriate.")
        else:
            lines.append("   Non-cooperation warrants full calculated penalty. Consider enhanced enforcement.")
        lines.append("=" * 60)
        return "\n".join(lines)


def build_recommendation(calc: Dict, conf_zone: str, zone: AnalysisZone) -> str:
    if conf_zone == "DEFENSIBLE":
        if zone == AnalysisZone.PLANNING:
            return f"Penalty of ${calc['total']:,.2f} is well-supported. Budget for this amount and implement corrective actions immediately."
        return f"Penalty calculation is defensible under 16 TAC §3.107. Range: ${calc['range_min']:,.2f}-${calc['range_max']:,.2f}."
    elif conf_zone == "AGGRESSIVE":
        return f"Penalty estimate of ${calc['total']:,.2f} is supportable but may face challenge. Consider settlement at ${calc['range_min']:,.2f}."
    elif conf_zone == "DISCLOSURE":
        return "DISCLOSURE: Significant discretion involved. Actual penalty depends on agency negotiation and specific facts."
    return "HIGH RISK: Novel penalty scenario. Do not rely on this estimate without regulatory counsel review."


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN ENGINE CLASS (TIE-1: Three-Layer Response)
# ═══════════════════════════════════════════════════════════════════════════════

class PenaltyCalculatorEngine:
    def __init__(self):
        self.start_time = time.time()
        self.doctrines = DOCTRINE_BLOCKS
        self.doctrine_index = {d.topic: d for d in self.doctrines}
        self.telemetry = telem_mod.TelemetryCollector()
        self.drift = DriftWatcher([d.topic for d in self.doctrines])
        self.coverage = CoverageMap(self.doctrines)
        self.cloud = None
        if CognitionCloudRetriever is not None:
            try:
                self.cloud = CognitionCloudRetriever()
            except Exception:
                pass
        self.query_count = 0
        self.error_count = 0
        self.latencies: List[float] = []
        logger.info(f"{ENGINE_ID} initialized — {len(self.doctrines)} doctrines")

    # Layer 1: Doctrine Cache
    def doctrine_lookup(self, query: str, limit: int = 5) -> List:
        keywords = extract_keywords(query)
        query_lower = query.lower()
        scored = []
        for d in self.doctrines:
            score = 0.0
            for kw in keywords:
                if kw in [k.lower() for k in d.keywords]:
                    score += 2.0
            if d.topic.lower().replace("_", " ") in query_lower:
                score += 3.0
            elif any(w in query_lower for w in d.topic.lower().split("_")):
                score += 1.5
            if score > 0:
                scored.append((score, d))
        scored.sort(key=lambda x: x[0], reverse=True)
        results = [d for _, d in scored[:limit]]
        for r in results:
            self.drift.hit(r.topic)
            self.coverage.trigger(r.topic)
        if not results:
            self.drift.miss()
            self.coverage.gap(query)
        return results

    # Layer 2: Semantic Retrieval
    async def semantic_search(self, query: str, limit: int = 5) -> List:
        normalized = normalize_query(query)
        terms = set(normalized.split())
        scored = []
        for d in self.doctrines:
            doc_terms = set(d.topic.lower().replace("_", " ").split())
            doc_terms.update(k.lower() for k in d.keywords)
            overlap = len(terms & doc_terms) / max(len(terms), 1)
            if overlap > 0.1:
                scored.append((overlap, d))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [d for _, d in scored[:limit]]

    # Layer 3: Deep Analysis
    async def deep_analysis(self, query: str, matched, zone: AnalysisZone) -> Dict:
        chain = [f"Deep analysis: {query[:200]}", f"Zone: {zone.value}", f"Matched: {len(matched)} doctrines"]
        authorities = []
        for d in matched:
            chain.append(f"  {d.topic}: conf={d.confidence}")
            for a in d.primary_authority:
                level, weight = classify_authority(a)
                authorities.append((a, level, weight))
        authorities.sort(key=lambda x: x[2], reverse=True)
        return {"chain": chain, "authorities": authorities[:10]}

    # Main query handler
    async def query(self, req: QueryRequest) -> Dict:
        start = time.time()
        self.query_count += 1
        zone = validate_zone(req.zone)
        normalized = normalize_query(req.query)

        # Layer 1
        layer = "DOCTRINE_CACHE"
        matched = self.doctrine_lookup(normalized)
        # Layer 2 fallback
        if not matched:
            layer = "SEMANTIC_RETRIEVAL"
            matched = await self.semantic_search(normalized)
        # Layer 3 fallback
        deep = None
        if not matched or req.mode == "MEMO":
            layer = "DEEP_ANALYSIS" if not matched else layer
            if not matched:
                matched = self.doctrines[:3]
            deep = await self.deep_analysis(req.query, matched, zone)

        conf = compute_penalty_confidence(True, len(matched) > 0, 0.8, False)
        latency = (time.time() - start) * 1000
        self.latencies.append(latency)
        return {"matched": matched, "layer": layer, "confidence": conf, "zone": zone, "deep": deep, "latency": latency}

    # Penalty calculation with TIE wrapping
    async def calculate(self, req: PenaltyRequest) -> PenaltyResponse:
        start = time.time()
        self.query_count += 1
        qid = hashlib.sha256(f"{req.violation_type}{time.time()}".encode()).hexdigest()[:16]
        tid = str(uuid.uuid4())[:12]
        zone = validate_zone(req.zone)

        # Calculate penalty
        calc = calculate_penalty(req)

        # Doctrine lookup
        matched = self.doctrine_lookup(req.violation_type)
        layer = "DOCTRINE_CACHE" if matched else "PENALTY_FORMULA"

        # Confidence
        conf = compute_penalty_confidence(True, len(matched) > 0, 0.8 if req.days_in_violation > 0 else 0.5, False)
        conf_zone = stratify_confidence(conf)

        # Decomposition
        categories = list(set(d.issue_category.value for d in matched)) if matched else ["penalty"]
        strata = {"primary": [m.topic for m in matched[:3]], "secondary": [m.topic for m in matched[3:6]]}

        # Doctrine matches
        doc_matches = [{"topic": d.topic, "confidence": d.confidence, "keywords": d.keywords[:5]} for d in matched[:5]]

        # Summary & recommendation
        summary = build_summary(calc, req, zone, conf)
        recommendation = build_recommendation(calc, conf_zone, zone)

        # Epistemic guardrails
        summary, warnings, disclosure = apply_guardrails(summary, conf)

        # Fact fragility
        fragility = [score_fragility(f"Violation duration: {req.days_in_violation} days", True, False, False)]
        if req.environmental_harm:
            fragility.append(score_fragility("Environmental harm assessment", False, True, True))

        # Determinism hash
        det_hash = compute_hash(req.violation_type, req.days_in_violation, req.prior_violations,
                                req.environmental_harm, req.cooperation, req.mode)

        latency = (time.time() - start) * 1000
        self.latencies.append(latency)

        return PenaltyResponse(
            query_id=qid, trace_id=tid, timestamp=datetime.utcnow().isoformat(),
            violation_type=req.violation_type, base_penalty=calc["base"],
            gravity_adjustment=calc["gravity"], history_multiplier=calc["history"],
            cooperation_credit=calc["coop"], self_report_credit=calc["self_report"],
            ability_to_pay_adjustment=calc["atp"], economic_benefit_recovery=calc["econ_benefit"],
            per_day_penalty=calc["per_day"], total_penalty=calc["total"],
            penalty_range_min=calc["range_min"], penalty_range_max=calc["range_max"],
            statutory_maximum=calc["stat_max"],
            primary_authority="16 TAC §3.107",
            authorities=build_citations(["16 TAC §3.107", "TX Natural Resources Code §81.0531", "RRC Enforcement Guidelines"]),
            confidence=round(conf, 4), confidence_zone=conf_zone,
            response_mode=req.mode, analysis_zone=zone.value, layer_used=layer,
            latency_ms=round(latency, 2),
            doctrine_matches=doc_matches, issue_categories=categories, strata=strata,
            mitigation_options=calc["mitigation"], aggravating_factors=calc["aggravating"],
            enforcement_actions=calc["enforcement"],
            reasoning=summary, recommendation=recommendation,
            epistemic_warnings=warnings, disclosure_caveat=disclosure,
            fact_fragility=fragility, determinism_hash=det_hash,
        )


# ═══════════════════════════════════════════════════════════════════════════════
# FASTAPI APPLICATION (TIE-17)
# ═══════════════════════════════════════════════════════════════════════════════

engine: Optional[PenaltyCalculatorEngine] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global engine
    logger.info(f"Starting {ENGINE_ID} {ENGINE_NAME} v{ENGINE_VERSION}")
    engine = PenaltyCalculatorEngine()
    yield
    logger.info(f"{ENGINE_ID} shutting down")


app = FastAPI(title=f"ECHO OMEGA PRIME — {ENGINE_ID} {ENGINE_NAME}", version=ENGINE_VERSION, lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


@app.post("/query")
async def handle_query(request: QueryRequest):
    if not engine: raise HTTPException(503, "Not initialized")
    return await engine.query(request)


@app.post("/calculate", response_model=PenaltyResponse)
async def handle_calculate(request: PenaltyRequest):
    if not engine: raise HTTPException(503, "Not initialized")
    return await engine.calculate(request)


@app.get("/health", response_model=HealthResponse)
async def health():
    if not engine: raise HTTPException(503, "Not initialized")
    drift = engine.drift.report()
    avg_lat = sum(engine.latencies) / max(len(engine.latencies), 1)
    return HealthResponse(
        engine_id=ENGINE_ID, engine_name=ENGINE_NAME, version=ENGINE_VERSION, status="healthy",
        uptime_seconds=round(time.time() - engine.start_time, 1), doctrine_count=len(engine.doctrines),
        port=ENGINE_PORT, domain=ENGINE_DOMAIN, cloud_available=engine.cloud is not None,
        total_queries=engine.query_count, error_rate=round(engine.error_count / max(engine.query_count, 1), 4),
        avg_latency_ms=round(avg_lat, 2), coverage_pct=drift["coverage_pct"], guardrails_active=True)


@app.get("/metrics")
async def metrics():
    if not engine: raise HTTPException(503, "Not initialized")
    avg_lat = sum(engine.latencies) / max(len(engine.latencies), 1)
    return {"engine_id": ENGINE_ID, "queries": engine.query_count, "errors": engine.error_count,
            "avg_latency_ms": round(avg_lat, 2), "coverage": engine.coverage.report()}


@app.get("/drift")
async def drift():
    if not engine: raise HTTPException(503, "Not initialized")
    return engine.drift.report()


@app.get("/coverage")
async def coverage():
    if not engine: raise HTTPException(503, "Not initialized")
    return engine.coverage.report()


@app.get("/penalty-tiers")
async def penalty_tiers():
    return {"bases": PENALTY_BASES, "statutory_max": STATUTORY_MAX_PER_DAY,
            "gravity": GRAVITY_FACTORS, "mitigation": MITIGATION_FACTORS}


@app.get("/authorities")
async def authorities():
    return {"hierarchy": AUTHORITY_WEIGHTS, "resolution": "Higher weight controls"}


@app.get("/guardrails")
async def guardrails():
    return {"banned": BANNED_PHRASES, "active": True}


@app.get("/doctrines")
async def list_doctrines(limit: int = 50):
    if not engine: raise HTTPException(503, "Not initialized")
    return {"total": len(engine.doctrines), "doctrines": [
        {"topic": d.topic, "confidence": d.confidence, "keywords": d.keywords[:5]} for d in engine.doctrines[:limit]]}


if __name__ == "__main__":
    logger.info(f"Launching {ENGINE_ID} on port {ENGINE_PORT}")
    uvicorn.run("engine:app", host="0.0.0.0", port=ENGINE_PORT, log_level="info")
