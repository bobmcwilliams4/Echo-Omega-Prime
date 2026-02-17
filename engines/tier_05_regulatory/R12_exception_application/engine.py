"""
R12 — Exception Application Analyzer Engine
Port: 8712 | Version: 2.0.0
TIE-20 Compliant | ECHO OMEGA PRIME Regulatory Division

Analyzes RRC exception applications (Rule 37, Rule 38, density, flaring,
disposal, enhanced recovery, horizontal well, special field rules).
Three-layer response: doctrine cache → semantic retrieval → deep analysis.
"""

import hashlib
import json
import sys
import time
import uuid
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import uvicorn
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import BaseModel, Field

# ═══════════════════════════════════════════════════════════════════════
# PATH SETUP
# ═══════════════════════════════════════════════════════════════════════
ENGINE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ENGINE_DIR))
sys.path.insert(0, str(ENGINE_DIR.parent / "_shared"))

try:
    from cloud_retriever import CognitionCloudRetriever
    _cloud = CognitionCloudRetriever()
except ImportError:
    _cloud = None

import doctrines
import semantic
import search
import telemetry

# ═══════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════
ENGINE_ID = "R12_exception_application"
ENGINE_NAME = "Exception Application Analyzer"
ENGINE_VERSION = "2.0.0"
ENGINE_PORT = 8712

LOG_DIR = ENGINE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
AUDIT_LOG = LOG_DIR / "audit_trail.jsonl"

logger.remove()
logger.add(sys.stderr, level="INFO", format="<green>{time:HH:mm:ss}</green> | <level>{level:<7}</level> | {message}")
logger.add(LOG_DIR / "engine.log", rotation="50 MB", retention="30 days", level="DEBUG")

DOCTRINE_BLOCKS = doctrines.DOCTRINE_BLOCKS
ConfidenceLevel = doctrines.ConfidenceLevel
IssueCategory = doctrines.IssueCategory
DoctrineBlock = doctrines.DoctrineBlock
normalize_query = semantic.normalize_query
extract_keywords = semantic.extract_keywords
TelemetryCollector = telemetry.TelemetryCollector


# ═══════════════════════════════════════════════════════════════════════
# COMPONENT 2: RESPONSE MODES
# ═══════════════════════════════════════════════════════════════════════
class ResponseMode(str, Enum):
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"


# ═══════════════════════════════════════════════════════════════════════
# COMPONENT 4: AUTHORITY HARDENING
# ═══════════════════════════════════════════════════════════════════════
class AuthorityLevel(str, Enum):
    CONSTITUTIONAL = "CONSTITUTIONAL"
    STATUTORY = "STATUTORY"
    REGULATORY = "REGULATORY"
    ADMINISTRATIVE_RULE = "ADMINISTRATIVE_RULE"
    COMMISSION_ORDER = "COMMISSION_ORDER"
    FIELD_RULE = "FIELD_RULE"
    ADVISORY = "ADVISORY"
    INTERNAL_GUIDANCE = "INTERNAL_GUIDANCE"
    INDUSTRY_PRACTICE = "INDUSTRY_PRACTICE"


AUTHORITY_WEIGHTS: Dict[str, Tuple[AuthorityLevel, int]] = {
    "Texas Constitution": (AuthorityLevel.CONSTITUTIONAL, 100),
    "Texas Natural Resources Code": (AuthorityLevel.STATUTORY, 95),
    "TX NRC §85": (AuthorityLevel.STATUTORY, 95),
    "TX NRC §86": (AuthorityLevel.STATUTORY, 95),
    "TX NRC §89": (AuthorityLevel.STATUTORY, 95),
    "16 TAC §3.37": (AuthorityLevel.REGULATORY, 90),
    "16 TAC §3.38": (AuthorityLevel.REGULATORY, 90),
    "16 TAC §3.32": (AuthorityLevel.REGULATORY, 90),
    "16 TAC §3.36": (AuthorityLevel.REGULATORY, 90),
    "16 TAC §3.46": (AuthorityLevel.REGULATORY, 90),
    "16 TAC §3.40": (AuthorityLevel.REGULATORY, 90),
    "Railroad Commission of Texas": (AuthorityLevel.COMMISSION_ORDER, 80),
    "RRC Statewide Rule": (AuthorityLevel.COMMISSION_ORDER, 80),
    "RRC Final Order": (AuthorityLevel.COMMISSION_ORDER, 80),
    "RRC Examiner's Report": (AuthorityLevel.ADVISORY, 60),
    "SOAH Recommendation": (AuthorityLevel.ADVISORY, 60),
    "Industry Practice": (AuthorityLevel.INDUSTRY_PRACTICE, 30),
}


def classify_authority(citation: str) -> Tuple[AuthorityLevel, int]:
    """Classify a citation to its authority level and weight."""
    for key, (level, weight) in AUTHORITY_WEIGHTS.items():
        if key.lower() in citation.lower():
            return level, weight
    return AuthorityLevel.ADVISORY, 50


def resolve_authority_conflict(authorities: List[str]) -> Dict[str, Any]:
    """When multiple authorities conflict, higher weight controls."""
    classified = [(a, *classify_authority(a)) for a in authorities]
    classified.sort(key=lambda x: x[2], reverse=True)
    if len(classified) < 2:
        return {"conflict": False, "controlling": classified[0][0] if classified else None}
    top = classified[0]
    runner = classified[1]
    return {
        "conflict": top[2] != runner[2],
        "controlling": top[0],
        "controlling_level": top[1].value,
        "controlling_weight": top[2],
        "subordinate": runner[0],
        "subordinate_weight": runner[2],
    }


# ═══════════════════════════════════════════════════════════════════════
# COMPONENT 5: CONFIDENCE STRATIFICATION
# ═══════════════════════════════════════════════════════════════════════
class ConfidenceStratification(str, Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"


def stratify_confidence(score: float) -> ConfidenceStratification:
    if score >= 0.90:
        return ConfidenceStratification.DEFENSIBLE
    if score >= 0.70:
        return ConfidenceStratification.AGGRESSIVE
    if score >= 0.50:
        return ConfidenceStratification.DISCLOSURE
    return ConfidenceStratification.HIGH_RISK


# ═══════════════════════════════════════════════════════════════════════
# COMPONENT 13: ZONED ANALYSIS
# ═══════════════════════════════════════════════════════════════════════
class AnalysisZone(str, Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"


ZONE_INSTRUCTIONS = {
    AnalysisZone.PLANNING: "Forward-looking: identify requirements, timelines, strategic options for exception filing",
    AnalysisZone.REPORTING: "Factual summary: current application status, compliance position, regulatory posture",
    AnalysisZone.AUDIT: "Retrospective: verify procedures followed, identify deficiencies, document compliance gaps",
}


# ═══════════════════════════════════════════════════════════════════════
# COMPONENT 14: FACT FRAGILITY SCORING
# ═══════════════════════════════════════════════════════════════════════
@dataclass
class FragilityScore:
    verifiability: float
    recharacterization_risk: float
    testimony_dependence: float
    overall: float
    narrative: str


def score_fact_fragility(
    verifiability: float = 0.8,
    recharacterization_risk: float = 0.3,
    testimony_dependence: float = 0.2,
) -> FragilityScore:
    overall = (verifiability * 0.4) + ((1.0 - recharacterization_risk) * 0.35) + ((1.0 - testimony_dependence) * 0.25)
    if overall >= 0.80:
        narrative = "Fact pattern is robust — verifiable through official RRC records and technical data."
    elif overall >= 0.60:
        narrative = "Fact pattern has moderate support — some elements depend on engineering judgment."
    else:
        narrative = "Fact pattern is fragile — relies on testimony, subjective judgments, or contested data."
    return FragilityScore(
        verifiability=verifiability,
        recharacterization_risk=recharacterization_risk,
        testimony_dependence=testimony_dependence,
        overall=round(overall, 3),
        narrative=narrative,
    )


# ═══════════════════════════════════════════════════════════════════════
# COMPONENT 16: DETERMINISM HASH
# ═══════════════════════════════════════════════════════════════════════
def compute_determinism_hash(query: str, matched_topics: List[str], confidence: float) -> str:
    deterministic = json.dumps(
        {"query": query.strip().lower(), "topics": sorted(matched_topics), "confidence": round(confidence, 3)},
        sort_keys=True,
    )
    return hashlib.sha256(deterministic.encode("utf-8")).hexdigest()[:16]


# ═══════════════════════════════════════════════════════════════════════
# BANNED PHRASES — EPISTEMIC GUARDRAILS
# ═══════════════════════════════════════════════════════════════════════
BANNED_PHRASES = [
    "guaranteed approval",
    "certain to be granted",
    "100% success",
    "will definitely be approved",
    "no risk of denial",
    "always granted",
    "never denied",
    "rubber stamp",
    "automatic approval",
    "risk-free application",
    "no possibility of protest",
    "guaranteed outcome",
]


def apply_epistemic_guardrails(text: str) -> str:
    result = text
    for phrase in BANNED_PHRASES:
        if phrase.lower() in result.lower():
            result = result.replace(phrase, f"[REDACTED: overconfident claim]")
    return result


# ═══════════════════════════════════════════════════════════════════════
# COMPONENT 9: DRIFT WATCHER
# ═══════════════════════════════════════════════════════════════════════
class DriftWatcher:
    def __init__(self) -> None:
        self.baseline_hashes: Dict[str, str] = {}
        self.drift_events: List[Dict[str, Any]] = []
        self.topic_last_triggered: Dict[str, str] = {}

    def register_baseline(self, topic: str, content_hash: str) -> None:
        self.baseline_hashes[topic] = content_hash

    def record_trigger(self, topic: str) -> None:
        self.topic_last_triggered[topic] = datetime.now(timezone.utc).isoformat()

    def check_drift(self, topic: str, current_hash: str) -> Optional[Dict[str, Any]]:
        baseline = self.baseline_hashes.get(topic)
        if baseline and baseline != current_hash:
            event = {
                "topic": topic,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "baseline_hash": baseline,
                "current_hash": current_hash,
                "drifted": True,
            }
            self.drift_events.append(event)
            logger.warning(f"Doctrine drift detected: {topic}")
            return event
        return None

    def get_stale_doctrines(self, max_age_days: int = 30) -> List[str]:
        cutoff = datetime.now(timezone.utc).isoformat()
        stale = []
        for topic in self.baseline_hashes:
            if topic not in self.topic_last_triggered:
                stale.append(topic)
        return stale

    def get_drift_report(self) -> Dict[str, Any]:
        return {
            "total_baselines": len(self.baseline_hashes),
            "drift_events": len(self.drift_events),
            "stale_doctrines": self.get_stale_doctrines(),
            "recent_drifts": self.drift_events[-10:] if self.drift_events else [],
        }


# ═══════════════════════════════════════════════════════════════════════
# COMPONENT 10: COVERAGE MAP
# ═══════════════════════════════════════════════════════════════════════
class CoverageMap:
    def __init__(self) -> None:
        self.triggered: Dict[str, int] = {}
        self.missed_queries: List[Dict[str, Any]] = []

    def record_hit(self, topic: str) -> None:
        self.triggered[topic] = self.triggered.get(topic, 0) + 1

    def record_miss(self, query: str, keywords: List[str]) -> None:
        self.missed_queries.append({
            "query": query[:200],
            "keywords": keywords,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        if len(self.missed_queries) > 500:
            self.missed_queries = self.missed_queries[-250:]

    def get_coverage_report(self) -> Dict[str, Any]:
        total_doctrines = len(DOCTRINE_BLOCKS)
        triggered_count = len(self.triggered)
        return {
            "total_doctrines": total_doctrines,
            "triggered_count": triggered_count,
            "coverage_pct": round(triggered_count / max(total_doctrines, 1) * 100, 1),
            "top_topics": sorted(self.triggered.items(), key=lambda x: x[1], reverse=True)[:20],
            "missed_queries": len(self.missed_queries),
            "recent_misses": self.missed_queries[-5:],
            "epistemic_gaps": [m["query"] for m in self.missed_queries[-5:]],
        }


# ═══════════════════════════════════════════════════════════════════════
# COMPONENT 11: METRICS COLLECTOR
# ═══════════════════════════════════════════════════════════════════════
class MetricsCollector:
    def __init__(self) -> None:
        self.total_queries: int = 0
        self.cache_hits: int = 0
        self.cache_misses: int = 0
        self.semantic_retrievals: int = 0
        self.deep_analyses: int = 0
        self.errors: int = 0
        self.latencies: List[float] = []
        self.start_time: float = time.time()

    def record_query(self, latency_ms: float, layer: str) -> None:
        self.total_queries += 1
        self.latencies.append(latency_ms)
        if len(self.latencies) > 10000:
            self.latencies = self.latencies[-5000:]
        if layer == "doctrine_cache":
            self.cache_hits += 1
        elif layer == "semantic_retrieval":
            self.semantic_retrievals += 1
            self.cache_misses += 1
        else:
            self.deep_analyses += 1
            self.cache_misses += 1

    def record_error(self) -> None:
        self.errors += 1

    @property
    def avg_latency(self) -> float:
        return sum(self.latencies) / len(self.latencies) if self.latencies else 0.0

    @property
    def p95_latency(self) -> float:
        if not self.latencies:
            return 0.0
        s = sorted(self.latencies)
        return s[int(len(s) * 0.95)]

    @property
    def cache_hit_rate(self) -> float:
        total = self.cache_hits + self.cache_misses
        return self.cache_hits / total if total > 0 else 0.0

    @property
    def uptime_seconds(self) -> float:
        return time.time() - self.start_time

    @property
    def queries_per_hour(self) -> float:
        hours = self.uptime_seconds / 3600
        return self.total_queries / hours if hours > 0 else 0.0


# ═══════════════════════════════════════════════════════════════════════
# COMPONENT 15: AUDIT TRAIL
# ═══════════════════════════════════════════════════════════════════════
class AuditTrail:
    def __init__(self, path: Path) -> None:
        self.path = path

    def log_query(self, entry: Dict[str, Any]) -> None:
        try:
            with open(self.path, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            logger.error(f"Audit trail write failed: {e}")


# ═══════════════════════════════════════════════════════════════════════
# GLOBAL INSTANCES
# ═══════════════════════════════════════════════════════════════════════
_metrics = MetricsCollector()
_drift = DriftWatcher()
_coverage = CoverageMap()
_audit = AuditTrail(AUDIT_LOG)
_telemetry = TelemetryCollector()
_start_time = time.time()

# Register baselines for all doctrine blocks
for _block in DOCTRINE_BLOCKS:
    _h = hashlib.sha256(f"{_block.topic}|{_block.reasoning_framework}".encode()).hexdigest()[:16]
    _drift.register_baseline(_block.topic, _h)


# ═══════════════════════════════════════════════════════════════════════
# PYDANTIC MODELS
# ═══════════════════════════════════════════════════════════════════════
class ExceptionType(str, Enum):
    RULE_37 = "rule_37"
    RULE_38 = "rule_38"
    DENSITY = "density"
    FLARING = "flaring"
    DISPOSAL = "disposal"
    ENHANCED_RECOVERY = "enhanced_recovery"
    HORIZONTAL_WELL = "horizontal_well"
    SPECIAL_FIELD_RULE = "special_field_rule"
    SALTWATER_DISPOSAL = "saltwater_disposal"
    COMMINGLING = "commingling"
    UNITIZATION = "unitization"


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=3, description="Exception application question")
    mode: ResponseMode = Field(default=ResponseMode.FAST)
    zone: AnalysisZone = Field(default=AnalysisZone.PLANNING)
    exception_type: Optional[ExceptionType] = None
    field_name: Optional[str] = None
    county: Optional[str] = None
    include_authorities: bool = Field(default=True)
    deep_analysis: bool = Field(default=False)


class ExceptionApplicationRequest(BaseModel):
    exception_type: ExceptionType
    field_name: Optional[str] = None
    county: Optional[str] = None
    current_rule: Optional[str] = None
    requested_exception: str = Field(..., description="What exception is requested")
    justification: str = Field(..., description="Good cause justification")
    no_injury_claimed: bool = Field(False)
    voluntary_pooling: bool = Field(False)
    offset_consent: bool = Field(False)
    well_count: int = Field(1, ge=1)
    acreage: Optional[float] = None
    mode: ResponseMode = Field(default=ResponseMode.FAST)
    zone: AnalysisZone = Field(default=AnalysisZone.PLANNING)


class AuthorityCitation(BaseModel):
    citation: str
    level: str
    weight: int
    relevance: str


class AnalysisResult(BaseModel):
    query_id: str
    engine_id: str = ENGINE_ID
    engine_version: str = ENGINE_VERSION
    timestamp: str
    query: str
    mode: str
    zone: str
    response_layer: str
    exception_type: Optional[str] = None
    conclusion: str
    reasoning: str
    key_factors: List[str]
    good_cause_elements: List[str]
    burden_of_proof: str
    hearing_required: bool
    protest_rights: str
    authorities_cited: List[AuthorityCitation]
    success_likelihood: str
    success_score: float
    recommendations: List[str]
    confidence: float
    confidence_stratification: str
    fact_fragility: Optional[Dict[str, Any]] = None
    determinism_hash: str
    latency_ms: float
    disclosure_caveat: Optional[str] = None
    zoned_analysis: Optional[Dict[str, Any]] = None
    coverage_snapshot: Optional[Dict[str, Any]] = None


class HealthResponse(BaseModel):
    engine_id: str
    engine_name: str
    version: str
    status: str
    uptime_seconds: float
    doctrine_count: int
    queries_served: int
    cache_hit_rate: float
    avg_latency_ms: float
    exception_types: List[str]
    port: int


class MetricsResponse(BaseModel):
    total_queries: int
    cache_hits: int
    cache_misses: int
    semantic_retrievals: int
    deep_analyses: int
    avg_latency_ms: float
    p95_latency_ms: float
    errors: int
    uptime_seconds: float
    queries_per_hour: float


# ═══════════════════════════════════════════════════════════════════════
# EXCEPTION FRAMEWORKS — DOMAIN KNOWLEDGE
# ═══════════════════════════════════════════════════════════════════════
EXCEPTION_FRAMEWORKS: Dict[str, Dict[str, Any]] = {
    "rule_37": {
        "cite": "16 TAC §3.37",
        "statute": "TX NRC §85.2021",
        "burden": "Applicant must prove exception will prevent waste or protect correlative rights, and no undue injury to other operators",
        "hearing": True,
        "notice_days": 15,
        "protest_window_days": 15,
        "elements": [
            "Demonstrate necessity for exception (small tract, irregular shape, drainage)",
            "Show no undue injury to offset operators or their correlative rights",
            "Prove waste prevention or economic necessity",
            "Provide technical justification (geological, engineering data)",
            "Show compliance with density requirements or justify density exception",
        ],
        "success_factors": {
            "no_injury_claimed": 20,
            "voluntary_pooling": 15,
            "offset_consent": 25,
            "small_tract": 15,
            "engineering_data": 10,
            "detailed_justification": 10,
        },
        "typical_success_rate": 0.72,
    },
    "rule_38": {
        "cite": "16 TAC §3.38",
        "statute": "TX NRC §86.088",
        "burden": "Applicant must show good cause for density exception, proving additional well will recover additional reserves",
        "hearing": True,
        "notice_days": 15,
        "protest_window_days": 15,
        "elements": [
            "Geologic or engineering justification for additional well",
            "Proof of additional recoverable reserves",
            "No drainage from offset tracts",
            "Economic analysis demonstrating viability",
            "Reservoir data supporting density increase",
        ],
        "success_factors": {
            "engineering_data": 20,
            "reserve_proof": 25,
            "no_drainage": 15,
            "economic_analysis": 15,
            "offset_consent": 20,
        },
        "typical_success_rate": 0.65,
    },
    "flaring": {
        "cite": "16 TAC §3.32",
        "statute": "TX NRC §85.045",
        "burden": "Show no feasible alternative to flaring and flaring is temporary",
        "hearing": False,
        "notice_days": 0,
        "protest_window_days": 0,
        "elements": [
            "Demonstrate lack of pipeline access or connection delays",
            "Show temporary nature of flaring with estimated end date",
            "Prove economic infeasibility of alternatives (compression, storage)",
            "Environmental impact assessment and minimization efforts",
            "Volume and composition of gas being flared",
        ],
        "success_factors": {
            "no_pipeline": 25,
            "temporary_nature": 20,
            "economic_infeasibility": 15,
            "environmental_mitigation": 15,
            "detailed_justification": 10,
        },
        "typical_success_rate": 0.80,
    },
    "disposal": {
        "cite": "16 TAC §3.46",
        "statute": "TX NRC §89.001",
        "burden": "Applicant must demonstrate disposal well will not endanger fresh water and is geologically sound",
        "hearing": True,
        "notice_days": 15,
        "protest_window_days": 15,
        "elements": [
            "Geologic survey of disposal zone and confining formations",
            "Mechanical integrity test results",
            "Fresh water protection plan",
            "Area of review (AOR) analysis",
            "Surface casing protection demonstration",
        ],
        "success_factors": {
            "geologic_data": 25,
            "mit_passed": 20,
            "fw_protection": 20,
            "aor_clean": 15,
            "detailed_justification": 10,
        },
        "typical_success_rate": 0.75,
    },
    "enhanced_recovery": {
        "cite": "16 TAC §3.46",
        "statute": "TX NRC §89.001",
        "burden": "Applicant must prove injection operations will increase recovery and protect fresh water",
        "hearing": True,
        "notice_days": 15,
        "protest_window_days": 15,
        "elements": [
            "Reservoir engineering study showing enhanced recovery potential",
            "Injection rate and pressure calculations",
            "Mechanical integrity of injection well(s)",
            "Fresh water protection measures",
            "Monitoring plan for injection operations",
        ],
        "success_factors": {
            "engineering_study": 25,
            "mit_passed": 20,
            "monitoring_plan": 15,
            "fw_protection": 15,
            "offset_notification": 10,
        },
        "typical_success_rate": 0.70,
    },
    "horizontal_well": {
        "cite": "16 TAC §3.37 & §3.86",
        "statute": "TX NRC §85.2021",
        "burden": "Applicant must demonstrate horizontal well path does not violate spacing or drainage protections",
        "hearing": True,
        "notice_days": 15,
        "protest_window_days": 15,
        "elements": [
            "Horizontal well path survey (proposed lateral path)",
            "Spacing from lease lines along entire lateral",
            "Take point analysis for production allocation",
            "No drainage of offset tracts by lateral extension",
            "Compliance with field rule spacing or exception request",
        ],
        "success_factors": {
            "survey_data": 20,
            "spacing_compliance": 20,
            "take_point_analysis": 15,
            "no_drainage": 15,
            "offset_consent": 20,
        },
        "typical_success_rate": 0.68,
    },
    "special_field_rule": {
        "cite": "16 TAC §3.37 (Field-Specific)",
        "statute": "TX NRC §86.088",
        "burden": "Applicant must show field conditions warrant departure from statewide rules",
        "hearing": True,
        "notice_days": 21,
        "protest_window_days": 21,
        "elements": [
            "Field-specific geological characteristics",
            "Production history supporting rule modification",
            "Reservoir engineering data",
            "Impact analysis on existing operators",
            "Proposed rule parameters with technical justification",
        ],
        "success_factors": {
            "geologic_data": 25,
            "production_history": 20,
            "engineering_data": 20,
            "operator_support": 15,
            "detailed_justification": 10,
        },
        "typical_success_rate": 0.55,
    },
    "saltwater_disposal": {
        "cite": "16 TAC §3.9 & §3.46",
        "statute": "TX NRC §89.001",
        "burden": "Demonstrate safe disposal without endangering usable-quality groundwater",
        "hearing": True,
        "notice_days": 15,
        "protest_window_days": 15,
        "elements": [
            "Disposal well construction and completion details",
            "Injection zone characterization",
            "Area of review for underground sources of drinking water",
            "Seismicity risk assessment (post-2014 requirement)",
            "Monitoring and reporting plan",
        ],
        "success_factors": {
            "well_construction": 20,
            "zone_characterization": 20,
            "seismicity_assessment": 20,
            "monitoring_plan": 15,
            "aor_clean": 15,
        },
        "typical_success_rate": 0.72,
    },
    "commingling": {
        "cite": "16 TAC §3.10",
        "statute": "TX NRC §85.042",
        "burden": "Prove commingling will not adversely affect waste prevention or correlative rights",
        "hearing": False,
        "notice_days": 15,
        "protest_window_days": 15,
        "elements": [
            "Identify zones to be commingled",
            "Production data from each zone",
            "Engineering justification for commingling",
            "Allocation method for production from commingled zones",
            "Impact on offset operators",
        ],
        "success_factors": {
            "zone_data": 20,
            "production_data": 20,
            "allocation_method": 20,
            "engineering_justification": 15,
            "no_adverse_impact": 15,
        },
        "typical_success_rate": 0.78,
    },
    "unitization": {
        "cite": "16 TAC §3.40",
        "statute": "TX NRC §101.001",
        "burden": "Demonstrate unitization will prevent waste and protect correlative rights of all interest owners",
        "hearing": True,
        "notice_days": 21,
        "protest_window_days": 21,
        "elements": [
            "Unit plan of development",
            "Participation formula for all interest owners",
            "Engineering and geological justification",
            "Evidence of good faith effort to obtain voluntary agreement",
            "Financial security for unit operations",
        ],
        "success_factors": {
            "voluntary_agreement_pct": 25,
            "engineering_justification": 20,
            "unit_plan": 20,
            "participation_formula": 15,
            "financial_security": 10,
        },
        "typical_success_rate": 0.60,
    },
}


# ═══════════════════════════════════════════════════════════════════════
# COMPONENT 6: SEMANTIC NORMALIZATION
# ═══════════════════════════════════════════════════════════════════════
EXCEPTION_TERM_MAP: Dict[str, str] = {
    "rule 37": "spacing_exception",
    "r37": "spacing_exception",
    "spacing exception": "spacing_exception",
    "location exception": "spacing_exception",
    "rule 38": "density_exception",
    "r38": "density_exception",
    "density exception": "density_exception",
    "flare exception": "flaring_exception",
    "flaring permit": "flaring_exception",
    "gas flaring": "flaring_exception",
    "venting": "flaring_exception",
    "swd": "saltwater_disposal",
    "disposal well": "saltwater_disposal",
    "injection well": "disposal_injection",
    "eor": "enhanced_recovery",
    "enhanced oil recovery": "enhanced_recovery",
    "waterflood": "enhanced_recovery",
    "co2 flood": "enhanced_recovery",
    "horizontal": "horizontal_well",
    "lateral": "horizontal_well",
    "hz well": "horizontal_well",
    "special field rule": "special_field_rule",
    "sfr": "special_field_rule",
    "commingling": "commingling",
    "commingle": "commingling",
    "unitization": "unitization",
    "unit plan": "unitization",
    "good cause": "good_cause_showing",
    "no injury": "no_injury_exception",
    "soah": "hearing_procedure",
    "state office": "hearing_procedure",
    "administrative hearing": "hearing_procedure",
    "protest": "protest_procedure",
    "offset protest": "protest_procedure",
}


def normalize_exception_terms(text: str) -> Tuple[str, List[str]]:
    """Normalize exception-specific terms."""
    lower = text.lower().strip()
    matched = []
    for raw, canonical in EXCEPTION_TERM_MAP.items():
        if raw in lower:
            matched.append(canonical)
    return lower, list(set(matched))


# ═══════════════════════════════════════════════════════════════════════
# COMPONENT 19: MULTI-DOCTRINE DECOMPOSITION
# ═══════════════════════════════════════════════════════════════════════
INTERACTION_EDGES = [
    ("spacing_exception", "density_exception", "Spacing and density exceptions often filed together"),
    ("spacing_exception", "horizontal_well", "Horizontal wells frequently need spacing exceptions"),
    ("density_exception", "enhanced_recovery", "Enhanced recovery may require additional density"),
    ("flaring_exception", "disposal_injection", "Flaring alternative may involve disposal wells"),
    ("saltwater_disposal", "enhanced_recovery", "SWD wells may convert to injection wells"),
    ("unitization", "enhanced_recovery", "Unit operations often involve enhanced recovery"),
    ("commingling", "density_exception", "Commingling may affect density calculations"),
    ("spacing_exception", "special_field_rule", "Field rules may modify spacing requirements"),
]


def decompose_exception_query(query: str, matched_terms: List[str]) -> Dict[str, Any]:
    """Multi-doctrine decomposition for exception queries."""
    primary_categories = matched_terms[:3] if matched_terms else ["general_exception"]
    related_edges = [
        edge for edge in INTERACTION_EDGES
        if any(cat in (edge[0], edge[1]) for cat in primary_categories)
    ]
    strata = []
    for cat in primary_categories:
        strata.append({
            "category": cat,
            "depth": "primary",
            "interactions": [e[2] for e in related_edges if cat in (e[0], e[1])],
        })
    return {
        "primary_categories": primary_categories,
        "interaction_edges": [(e[0], e[1], e[2]) for e in related_edges],
        "strata": strata,
        "complexity": "multi_doctrine" if len(primary_categories) > 1 else "single_doctrine",
    }


# ═══════════════════════════════════════════════════════════════════════
# COMPONENT 1: THREE-LAYER RESPONSE ENGINE
# ═══════════════════════════════════════════════════════════════════════
def doctrine_cache_lookup(query: str, keywords: List[str]) -> List:
    """Layer 1: Doctrine cache lookup (0-200ms target)."""
    matched = []
    query_lower = query.lower()
    for block in DOCTRINE_BLOCKS:
        score = 0
        for kw in block.keywords:
            if kw.lower() in query_lower:
                score += 2
        for kw in keywords:
            if kw.lower() in " ".join(block.keywords).lower():
                score += 1
        if score > 0:
            matched.append((block, score))
    matched.sort(key=lambda x: x[1], reverse=True)
    return [m[0] for m in matched[:5]]


def semantic_retrieval(query: str) -> List[Dict[str, Any]]:
    """Layer 2: Semantic retrieval (200-2000ms target)."""
    try:
        results = search.search_exception_patterns(query) if hasattr(search, "search_exception_patterns") else []
        return results
    except Exception as e:
        logger.warning(f"Semantic retrieval error: {e}")
        return []


def deep_analysis(
    query: str,
    mode: ResponseMode,
    zone: AnalysisZone,
    exception_type: Optional[str],
    matched_terms: List[str],
) -> Dict[str, Any]:
    """Layer 3 / Component 20: Deep analysis with multi-source synthesis."""
    framework = EXCEPTION_FRAMEWORKS.get(exception_type, EXCEPTION_FRAMEWORKS.get("rule_37", {}))
    decomposition = decompose_exception_query(query, matched_terms)

    reasoning_chain = [
        f"1. Exception type identified: {exception_type or 'general'}",
        f"2. Governing authority: {framework.get('cite', 'N/A')} / {framework.get('statute', 'N/A')}",
        f"3. Burden of proof: {framework.get('burden', 'N/A')}",
        f"4. Hearing required: {'Yes' if framework.get('hearing') else 'No'}",
        f"5. Decomposition complexity: {decomposition.get('complexity', 'unknown')}",
    ]

    if decomposition.get("interaction_edges"):
        reasoning_chain.append(f"6. Cross-doctrine interactions: {len(decomposition['interaction_edges'])} edges")

    adversarial_review = [
        "Offset operators may protest — verify notice requirements",
        "Commission examiner may request additional technical data",
        "Timing: filing delays can affect exception validity",
        "Alternative: consider voluntary pooling to avoid contested hearing",
    ]

    return {
        "reasoning_chain": reasoning_chain,
        "decomposition": decomposition,
        "adversarial_review": adversarial_review,
        "framework": framework,
        "depth": "deep_analysis",
    }


# ═══════════════════════════════════════════════════════════════════════
# MAIN QUERY HANDLER
# ═══════════════════════════════════════════════════════════════════════
def calculate_success_likelihood(
    exception_type: str,
    no_injury: bool = False,
    voluntary_pooling: bool = False,
    offset_consent: bool = False,
    justification_length: int = 0,
    acreage: Optional[float] = None,
) -> Tuple[float, str]:
    """Calculate success likelihood score and label."""
    framework = EXCEPTION_FRAMEWORKS.get(exception_type, {})
    base_rate = framework.get("typical_success_rate", 0.50)
    score = base_rate * 100
    factors = framework.get("success_factors", {})

    if no_injury and "no_injury_claimed" in factors:
        score += factors["no_injury_claimed"]
    if voluntary_pooling and "voluntary_pooling" in factors:
        score += factors["voluntary_pooling"]
    if offset_consent and "offset_consent" in factors:
        score += factors["offset_consent"]
    if justification_length > 500 and "detailed_justification" in factors:
        score += factors["detailed_justification"]
    if acreage and acreage < 40 and "small_tract" in factors:
        score += factors["small_tract"]

    score = min(score, 95)  # Never claim >95%

    if score >= 80:
        label = f"High ({score:.0f}%)"
    elif score >= 60:
        label = f"Moderate ({score:.0f}%)"
    elif score >= 40:
        label = f"Low-Moderate ({score:.0f}%)"
    else:
        label = f"Low ({score:.0f}%)"

    return score / 100, label


def process_query(request: QueryRequest) -> AnalysisResult:
    """Main query handler with three-layer response."""
    start = time.time()
    query_id = str(uuid.uuid4())
    logger.info(f"[{query_id}] Query: {request.query[:100]}")

    # Component 6: Semantic normalization
    normalized, sem_keywords = normalize_query(request.query)
    _, exception_terms = normalize_exception_terms(request.query)
    all_keywords = list(set(sem_keywords + exception_terms))

    # Detect exception type from query
    exc_type = request.exception_type.value if request.exception_type else None
    if not exc_type:
        for term in exception_terms:
            if term == "spacing_exception":
                exc_type = "rule_37"
                break
            elif term == "density_exception":
                exc_type = "rule_38"
                break
            elif term == "flaring_exception":
                exc_type = "flaring"
                break
            elif term == "saltwater_disposal":
                exc_type = "saltwater_disposal"
                break
            elif term == "enhanced_recovery":
                exc_type = "enhanced_recovery"
                break
            elif term == "horizontal_well":
                exc_type = "horizontal_well"
                break
        if not exc_type:
            exc_type = "rule_37"

    framework = EXCEPTION_FRAMEWORKS.get(exc_type, EXCEPTION_FRAMEWORKS["rule_37"])

    # Layer 1: Doctrine cache
    matched_doctrines = doctrine_cache_lookup(request.query, all_keywords)
    if matched_doctrines:
        layer = "doctrine_cache"
        primary = matched_doctrines[0]
        conclusion_parts = primary.conclusion_template if isinstance(primary.conclusion_template, list) else [primary.conclusion_template]
        conclusion = " ".join(conclusion_parts)
        reasoning = primary.reasoning_framework
        key_factors = primary.key_factors[:6]
        auth_list = primary.primary_authority
        conf_score = 0.85

        for topic_block in matched_doctrines:
            _coverage.record_hit(topic_block.topic)
            _drift.record_trigger(topic_block.topic)
    else:
        # Layer 2: Semantic retrieval
        sem_results = semantic_retrieval(request.query)
        if sem_results:
            layer = "semantic_retrieval"
            conclusion = f"Based on regulatory knowledge base: exception application under {framework['cite']} — {framework['burden']}."
            reasoning = f"Semantic retrieval matched {len(sem_results)} relevant provisions for {exc_type} exception."
            key_factors = framework["elements"][:5]
            auth_list = [framework["cite"], framework.get("statute", "")]
            conf_score = 0.70
        else:
            # Layer 3: Deep analysis
            layer = "deep_analysis"
            analysis = deep_analysis(request.query, request.mode, request.zone, exc_type, exception_terms)
            conclusion = f"Deep analysis of {exc_type} exception application. {framework['burden']}."
            reasoning = "\n".join(analysis["reasoning_chain"])
            key_factors = framework["elements"]
            auth_list = [framework["cite"], framework.get("statute", "")]
            conf_score = 0.55
            _coverage.record_miss(request.query, all_keywords)

    # Authority hardening
    authorities = []
    for cite in auth_list:
        if cite:
            level, weight = classify_authority(cite)
            authorities.append(AuthorityCitation(
                citation=cite, level=level.value, weight=weight,
                relevance="Primary exception authority",
            ))

    # Confidence stratification
    strat = stratify_confidence(conf_score)

    # Success likelihood
    success_score, success_label = calculate_success_likelihood(exc_type)

    # Fact fragility
    fragility = score_fact_fragility(
        verifiability=0.85 if layer == "doctrine_cache" else 0.60,
        recharacterization_risk=0.20,
        testimony_dependence=0.15 if layer == "doctrine_cache" else 0.40,
    )

    # Determinism hash
    matched_topics = [b.topic for b in matched_doctrines] if matched_doctrines else [exc_type]
    det_hash = compute_determinism_hash(request.query, matched_topics, conf_score)

    # Build mode-specific summary
    conclusion = apply_epistemic_guardrails(conclusion)
    if request.mode == ResponseMode.DEFENSE:
        conclusion = f"AUDIT-READY ANALYSIS: {conclusion}\nAuthority: {framework['cite']}. Burden: {framework['burden']}."
    elif request.mode == ResponseMode.MEMO:
        conclusion = (
            f"MEMORANDUM — {exc_type.upper()} EXCEPTION APPLICATION\n"
            f"Authority: {framework['cite']} / {framework.get('statute', 'N/A')}\n"
            f"Burden: {framework['burden']}\n"
            f"Hearing Required: {'Yes' if framework['hearing'] else 'No'}\n"
            f"Typical Success Rate: {framework.get('typical_success_rate', 'N/A')}\n\n"
            f"{conclusion}"
        )

    # Zoned analysis
    zone_output = {
        "zone": request.zone.value,
        "instruction": ZONE_INSTRUCTIONS[request.zone],
        "conclusion_in_zone": conclusion[:300],
    }

    # Recommendations
    recommendations = [
        f"File application with RRC under {framework['cite']}",
        "Prepare detailed technical justification with engineering data",
    ]
    if framework.get("hearing"):
        recommendations.append("Prepare for SOAH hearing — retain expert witnesses")
        recommendations.append(f"Notify offset operators {framework.get('notice_days', 15)} days before hearing")
    recommendations.append("Conduct offset operator outreach before filing")
    recommendations.append("Submit engineering reports and reservoir studies")
    if exc_type in ("rule_37", "horizontal_well"):
        recommendations.append("Consider voluntary pooling to reduce opposition")

    latency = (time.time() - start) * 1000
    _metrics.record_query(latency, layer)

    # Audit trail
    _audit.log_query({
        "query_id": query_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "query": request.query[:200],
        "exception_type": exc_type,
        "mode": request.mode.value,
        "zone": request.zone.value,
        "layer": layer,
        "confidence": conf_score,
        "stratification": strat.value,
        "latency_ms": round(latency, 2),
    })

    # Disclosure caveat
    disclosure = None
    if strat in (ConfidenceStratification.DISCLOSURE, ConfidenceStratification.HIGH_RISK):
        disclosure = (
            "This analysis involves significant uncertainty. Exception application outcomes depend on "
            "RRC examiner discretion, hearing testimony, and current regulatory posture. Retain qualified "
            "oil and gas attorney before filing."
        )

    return AnalysisResult(
        query_id=query_id,
        timestamp=datetime.now(timezone.utc).isoformat(),
        query=request.query,
        mode=request.mode.value,
        zone=request.zone.value,
        response_layer=layer,
        exception_type=exc_type,
        conclusion=conclusion,
        reasoning=reasoning,
        key_factors=key_factors,
        good_cause_elements=framework["elements"],
        burden_of_proof=framework["burden"],
        hearing_required=framework.get("hearing", True),
        protest_rights=f"Offset operators may protest within {framework.get('protest_window_days', 15)} days of notice. Protest triggers contested case hearing at SOAH.",
        authorities_cited=authorities,
        success_likelihood=success_label,
        success_score=round(success_score, 3),
        recommendations=recommendations,
        confidence=round(conf_score, 3),
        confidence_stratification=strat.value,
        fact_fragility={
            "verifiability": fragility.verifiability,
            "recharacterization_risk": fragility.recharacterization_risk,
            "testimony_dependence": fragility.testimony_dependence,
            "overall": fragility.overall,
            "narrative": fragility.narrative,
        },
        determinism_hash=det_hash,
        latency_ms=round(latency, 2),
        disclosure_caveat=disclosure,
        zoned_analysis=zone_output,
        coverage_snapshot=_coverage.get_coverage_report(),
    )


def process_application(request: ExceptionApplicationRequest) -> AnalysisResult:
    """Specialized handler for structured exception application analysis."""
    exc_type = request.exception_type.value
    query_text = (
        f"Analyze {exc_type} exception application for {request.field_name or 'unknown field'} "
        f"in {request.county or 'Texas'}. Requested: {request.requested_exception}. "
        f"Justification: {request.justification}"
    )

    # Use process_query for base analysis
    base_request = QueryRequest(
        query=query_text,
        mode=request.mode,
        zone=request.zone,
        exception_type=request.exception_type,
        field_name=request.field_name,
        county=request.county,
        deep_analysis=True,
    )
    result = process_query(base_request)

    # Recalculate success with application-specific factors
    success_score, success_label = calculate_success_likelihood(
        exc_type,
        no_injury=request.no_injury_claimed,
        voluntary_pooling=request.voluntary_pooling,
        offset_consent=request.offset_consent,
        justification_length=len(request.justification),
        acreage=request.acreage,
    )
    result.success_score = round(success_score, 3)
    result.success_likelihood = success_label

    return result


# ═══════════════════════════════════════════════════════════════════════
# COMPONENT 17: FASTAPI SERVER
# ═══════════════════════════════════════════════════════════════════════
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"{ENGINE_NAME} v{ENGINE_VERSION} starting on port {ENGINE_PORT}")
    logger.info(f"Doctrine cache: {len(DOCTRINE_BLOCKS)} blocks")
    logger.info(f"Exception frameworks: {len(EXCEPTION_FRAMEWORKS)} types")
    yield
    logger.info(f"{ENGINE_NAME} shutting down")


app = FastAPI(
    title=f"ECHO {ENGINE_ID} — {ENGINE_NAME}",
    version=ENGINE_VERSION,
    description="RRC exception application analysis with TIE-20 architecture",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/query", response_model=AnalysisResult)
async def query_endpoint(request: QueryRequest):
    try:
        return process_query(request)
    except Exception as e:
        logger.error(f"Query error: {e}")
        _metrics.record_error()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze", response_model=AnalysisResult)
async def analyze_application(request: ExceptionApplicationRequest):
    try:
        return process_application(request)
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        _metrics.record_error()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(
        engine_id=ENGINE_ID,
        engine_name=ENGINE_NAME,
        version=ENGINE_VERSION,
        status="operational",
        uptime_seconds=round(time.time() - _start_time, 2),
        doctrine_count=len(DOCTRINE_BLOCKS),
        queries_served=_metrics.total_queries,
        cache_hit_rate=round(_metrics.cache_hit_rate, 3),
        avg_latency_ms=round(_metrics.avg_latency, 2),
        exception_types=list(EXCEPTION_FRAMEWORKS.keys()),
        port=ENGINE_PORT,
    )


@app.get("/metrics", response_model=MetricsResponse)
async def metrics():
    return MetricsResponse(
        total_queries=_metrics.total_queries,
        cache_hits=_metrics.cache_hits,
        cache_misses=_metrics.cache_misses,
        semantic_retrievals=_metrics.semantic_retrievals,
        deep_analyses=_metrics.deep_analyses,
        avg_latency_ms=round(_metrics.avg_latency, 2),
        p95_latency_ms=round(_metrics.p95_latency, 2),
        errors=_metrics.errors,
        uptime_seconds=round(_metrics.uptime_seconds, 2),
        queries_per_hour=round(_metrics.queries_per_hour, 2),
    )


@app.get("/drift")
async def drift_report():
    return _drift.get_drift_report()


@app.get("/coverage")
async def coverage_report():
    return _coverage.get_coverage_report()


@app.get("/frameworks")
async def list_frameworks():
    return {
        k: {
            "cite": v["cite"],
            "hearing": v["hearing"],
            "typical_success_rate": v.get("typical_success_rate"),
            "elements_count": len(v["elements"]),
        }
        for k, v in EXCEPTION_FRAMEWORKS.items()
    }


@app.get("/doctrines")
async def list_doctrines():
    return {
        "total": len(DOCTRINE_BLOCKS),
        "topics": [b.topic for b in DOCTRINE_BLOCKS],
    }


@app.get("/authorities")
async def list_authorities():
    return {k: {"level": v[0].value, "weight": v[1]} for k, v in AUTHORITY_WEIGHTS.items()}


@app.get("/guardrails")
async def list_guardrails():
    return {"banned_phrases": BANNED_PHRASES, "count": len(BANNED_PHRASES)}


@app.get("/audit-trail")
async def get_audit_trail(limit: int = Query(default=50, le=500)):
    try:
        if AUDIT_LOG.exists():
            lines = AUDIT_LOG.read_text(encoding="utf-8").strip().split("\n")
            entries = [json.loads(line) for line in lines[-limit:]]
            return {"entries": entries, "total": len(lines)}
    except Exception as e:
        logger.error(f"Audit trail read error: {e}")
    return {"entries": [], "total": 0}


if __name__ == "__main__":
    logger.info(f"Launching {ENGINE_NAME} on port {ENGINE_PORT}")
    uvicorn.run(app, host="0.0.0.0", port=ENGINE_PORT)
