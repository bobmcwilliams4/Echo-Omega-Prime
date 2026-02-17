"""
R10 - Bond Requirements Calculator Engine
ECHO OMEGA PRIME Regulatory Division
Port: 8710 | Version: 2.0.0

Calculate operator bond requirements per 16 TAC 3.78, TX NRC 91.103-104.
TIE-20 Gold Standard compliant.

Architecture:
    Layer 1: Doctrine Cache (0-200ms) - Pre-compiled bond reasoning blocks
    Layer 2: Semantic Retrieval (200-700ms) - Fallback search on cache miss
    Layer 3: Deep Analysis (on-demand) - Multi-source bond synthesis

Response Modes:
    FAST: Bond calculation, minimal citations, sub-2 seconds
    DEFENSE: Structured reasoning, audit-ready, authority-weighted
    MEMO: Long-form, citation-heavy, regulatory documentation

Author: ECHO OMEGA PRIME
Authority: 11.0 SOVEREIGN
Port: 8710
"""

import sys
import hashlib
import json
import time
import uuid
from collections import defaultdict
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, ClassVar, Dict, List, Literal, Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Path setup - local module imports
# ---------------------------------------------------------------------------
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "_shared"))

try:
    from cloud_retriever import retrieve_from_cloud
except ImportError:
    retrieve_from_cloud = None

import doctrines
import search
import semantic
import telemetry

DOCTRINE_BLOCKS = doctrines.DOCTRINE_BLOCKS
DoctrineBlock = doctrines.DoctrineBlock
IssueCategory = doctrines.IssueCategory
ConfidenceLevel = doctrines.ConfidenceLevel
TelemetryCollector = telemetry.TelemetryCollector

# ---------------------------------------------------------------------------
# Logging configuration
# ---------------------------------------------------------------------------
ENGINE_DIR = Path(__file__).resolve().parent
LOG_DIR = ENGINE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

logger.add(
    LOG_DIR / "bond_engine_{time}.log",
    rotation="50 MB",
    retention="30 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {message}",
)

AUDIT_LOG_PATH = LOG_DIR / "audit_trail.jsonl"

ENGINE_ID = "R10_bond_requirements"
ENGINE_VERSION = "2.0.0"
ENGINE_PORT = 8710


# ==========================================================================
# TIE COMPONENT 6 - SEMANTIC NORMALIZATION
# ==========================================================================

BOND_SYNONYMS: Dict[str, List[str]] = {
    "individual_bond": ["individual bond", "single well bond", "per well bond", "well bond"],
    "blanket_bond": ["blanket bond", "blanket surety", "operator blanket", "aggregate bond"],
    "letter_of_credit": ["letter of credit", "loc", "bank guarantee", "bank letter"],
    "cash_deposit": ["cash deposit", "cash bond", "cash escrow"],
    "certificate_of_deposit": ["certificate of deposit", "cd", "cd bond"],
    "surety": ["surety bond", "surety", "bond company", "bonding company"],
    "forfeiture": ["forfeiture", "bond forfeiture", "call bond", "bond claim"],
    "release": ["bond release", "release bond", "cancel bond", "bond cancellation"],
    "p5": ["p-5", "p5", "organization report", "form p-5"],
    "rrc": ["rrc", "railroad commission", "texas railroad commission", "trrc"],
    "operator": ["operator", "operator of record", "designated operator", "working interest"],
    "well_count": ["well count", "number of wells", "total wells", "wells operated"],
    "bay_estuary": ["bay", "estuary", "bay well", "estuary well", "coastal well"],
    "h2s": ["h2s", "hydrogen sulfide", "sour gas", "h2s well", "sour well"],
    "injection": ["injection", "injection well", "disposal", "saltwater disposal", "swd"],
    "inactive": ["inactive well", "inactive", "idle well", "shut-in"],
    "violation": ["violation", "compliance violation", "enforcement", "penalty"],
    "plugging": ["plugging", "plug", "p&a", "plug and abandon"],
    "financial_assurance": ["financial assurance", "financial security", "security requirement"],
    "depth": ["depth", "total depth", "td", "well depth", "feet"],
}

BOND_STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "as", "is", "was", "are", "were", "be",
    "been", "being", "have", "has", "had", "do", "does", "did", "will",
    "would", "could", "should", "may", "might", "must", "can", "what",
    "when", "where", "who", "which", "how", "why", "this", "that", "these",
    "those", "i", "me", "my", "we", "our", "you", "your",
}


def normalize_bond_query(query: str) -> str:
    """Normalize query to canonical bond terminology."""
    import re
    normalized = query.lower().strip()
    for canonical, variants in BOND_SYNONYMS.items():
        for variant in variants:
            pattern = r"\b" + re.escape(variant) + r"\b"
            normalized = re.sub(pattern, canonical, normalized)
    normalized = re.sub(r"\s+", " ", normalized)
    return normalized


def extract_bond_keywords(query: str) -> List[str]:
    """Extract meaningful keywords from a bond-related query."""
    import re
    tokens = re.findall(r"\b\w+\b", query.lower())
    keywords = [t for t in tokens if t not in BOND_STOP_WORDS and len(t) > 2]
    seen: set = set()
    unique: List[str] = []
    for kw in keywords:
        if kw not in seen:
            seen.add(kw)
            unique.append(kw)
    return unique


# ==========================================================================
# TIE COMPONENT 4 - AUTHORITY HARDENING
# ==========================================================================

AUTHORITY_WEIGHTS: Dict[str, float] = {
    "16 TAC 3.78": 1.00,
    "16 TAC 3.78(a)": 0.98,
    "16 TAC 3.78(b)": 0.97,
    "16 TAC 3.78(c)": 0.98,
    "16 TAC 3.78(d)": 0.95,
    "16 TAC 3.78(e)": 0.94,
    "16 TAC 3.78(f)": 0.96,
    "16 TAC 3.78(g)": 0.96,
    "16 TAC 3.78(h)": 0.96,
    "TX NRC 91.103": 0.99,
    "TX NRC 91.104": 0.99,
    "TX NRC 91.1041": 0.97,
    "TX NRC 89.001": 0.90,
    "TX NRC 89.011": 0.88,
    "TX NRC 89.042": 0.87,
    "TX NRC 91.142": 0.92,
    "TX NRC 91.457": 0.85,
    "Statewide Rule 78": 0.95,
    "RRC Form P-5": 0.93,
    "RRC Oil & Gas Docket": 0.80,
}


def resolve_authority_conflict(authorities: List[str]) -> str:
    """Given multiple authorities, return the one with highest weight."""
    if not authorities:
        return "16 TAC 3.78"
    best = max(authorities, key=lambda a: AUTHORITY_WEIGHTS.get(a, 0.50))
    return best


def get_authority_weight(authority: str) -> float:
    """Return the authority weight for a given citation."""
    return AUTHORITY_WEIGHTS.get(authority, 0.50)


# ==========================================================================
# TIE COMPONENT 5 - CONFIDENCE STRATIFICATION
# ==========================================================================

class ConfidenceStratification(str, Enum):
    DEFENSIBLE = "defensible"
    AGGRESSIVE = "aggressive"
    DISCLOSURE = "disclosure"
    HIGH_RISK = "high_risk"


def stratify_confidence(
    confidence: ConfidenceLevel,
    authority_weight: float,
    doctrine_hit: bool,
) -> ConfidenceStratification:
    """Determine confidence stratification based on multiple factors."""
    if confidence == ConfidenceLevel.HIGH and authority_weight >= 0.90 and doctrine_hit:
        return ConfidenceStratification.DEFENSIBLE
    if confidence == ConfidenceLevel.HIGH and authority_weight >= 0.80:
        return ConfidenceStratification.AGGRESSIVE
    if confidence == ConfidenceLevel.MEDIUM:
        return ConfidenceStratification.DISCLOSURE
    return ConfidenceStratification.HIGH_RISK


# ==========================================================================
# TIE COMPONENT 13 - ZONED ANALYSIS
# ==========================================================================

class AnalysisZone(str, Enum):
    PLANNING = "planning"
    REPORTING = "reporting"
    AUDIT = "audit"


ZONE_DESCRIPTIONS: Dict[AnalysisZone, str] = {
    AnalysisZone.PLANNING: (
        "Forward-looking analysis for operators planning bond requirements. "
        "May include estimates, recommendations, and cost optimization strategies."
    ),
    AnalysisZone.REPORTING: (
        "Current-state reporting of bond amounts, compliance status, and regulatory "
        "obligations. Factual, no speculation."
    ),
    AnalysisZone.AUDIT: (
        "Audit-grade analysis with full authority chain, burden allocation, and "
        "defensibility assessment. Every statement must trace to statute or rule."
    ),
}


def detect_analysis_zone(query: str) -> AnalysisZone:
    """Detect appropriate analysis zone from query context."""
    query_lower = query.lower()
    audit_signals = ["audit", "compliance review", "enforcement", "penalty", "forfeiture", "inspection"]
    planning_signals = ["plan", "should i", "recommend", "optimize", "strategy", "what if", "how much would"]
    if any(signal in query_lower for signal in audit_signals):
        return AnalysisZone.AUDIT
    if any(signal in query_lower for signal in planning_signals):
        return AnalysisZone.PLANNING
    return AnalysisZone.REPORTING


# ==========================================================================
# TIE COMPONENT 14 - FACT FRAGILITY SCORING
# ==========================================================================

@dataclass
class FragilityScore:
    """Score indicating how fragile / vulnerable a factual assertion is."""
    verifiability: float = 1.0
    recharacterization_risk: float = 0.0
    testimony_dependence: float = 0.0
    regulatory_change_risk: float = 0.0
    overall: float = 1.0

    def compute_overall(self) -> float:
        self.overall = (
            self.verifiability * 0.40
            + (1.0 - self.recharacterization_risk) * 0.25
            + (1.0 - self.testimony_dependence) * 0.15
            + (1.0 - self.regulatory_change_risk) * 0.20
        )
        return self.overall


def score_bond_fragility(topic: str) -> FragilityScore:
    """Score fact fragility for bond-related assertions."""
    fs = FragilityScore()
    high_verifiability_topics = [
        "individual_well_bond_calculation", "blanket_bond_tiers",
        "letter_of_credit_alternative", "cash_deposit_alternative",
        "certificate_of_deposit_alternative",
    ]
    medium_topics = [
        "bond_increase_triggers", "bond_release_criteria",
        "operator_qualification_requirements",
    ]
    low_topics = [
        "bond_forfeiture_process", "inactive_well_bond_increase",
    ]
    if topic in high_verifiability_topics:
        fs.verifiability = 0.95
        fs.recharacterization_risk = 0.05
        fs.testimony_dependence = 0.0
        fs.regulatory_change_risk = 0.15
    elif topic in medium_topics:
        fs.verifiability = 0.80
        fs.recharacterization_risk = 0.15
        fs.testimony_dependence = 0.10
        fs.regulatory_change_risk = 0.25
    elif topic in low_topics:
        fs.verifiability = 0.65
        fs.recharacterization_risk = 0.25
        fs.testimony_dependence = 0.20
        fs.regulatory_change_risk = 0.30
    else:
        fs.verifiability = 0.70
        fs.recharacterization_risk = 0.20
        fs.testimony_dependence = 0.15
        fs.regulatory_change_risk = 0.20
    fs.compute_overall()
    return fs


# ==========================================================================
# EPISTEMIC GUARDRAILS (BANNED PHRASES)
# ==========================================================================

BANNED_PHRASES: List[str] = [
    "you definitely don't need a bond",
    "no bond is required",
    "the rrc won't check",
    "bonds are optional",
    "you can skip the bond",
    "everyone knows",
    "it's always",
    "it's never",
    "guaranteed to be approved",
    "the commission always accepts",
    "no operator has ever been denied",
    "bonds are just a formality",
    "just file the p-5 and you're done",
    "no penalty for late bonding",
    "the amount is negotiable",
    "you can bond for less than the schedule",
]


def apply_epistemic_guardrails(text: str) -> str:
    """Strip or flag banned phrases that compromise epistemic integrity."""
    text_lower = text.lower()
    for phrase in BANNED_PHRASES:
        if phrase in text_lower:
            logger.warning(f"Epistemic guardrail triggered: '{phrase}' found in output")
            text = text.replace(phrase, "[REDACTED - epistemic guardrail]")
            text = text.replace(phrase.capitalize(), "[REDACTED - epistemic guardrail]")
    return text


def check_guardrail_violations(text: str) -> List[str]:
    """Return list of banned phrases found in text."""
    violations: List[str] = []
    text_lower = text.lower()
    for phrase in BANNED_PHRASES:
        if phrase in text_lower:
            violations.append(phrase)
    return violations


# ==========================================================================
# TIE COMPONENT 9 - DRIFT WATCHER
# ==========================================================================

class DriftWatcher:
    """Monitor for doctrine drift over time."""

    def __init__(self) -> None:
        self.observations: List[Dict[str, Any]] = []
        self.baseline_doctrine_count: int = len(DOCTRINE_BLOCKS)
        self.baseline_timestamp: str = datetime.now(timezone.utc).isoformat()

    def observe(self, query: str, matched_topic: Optional[str], confidence: str) -> None:
        """Record an observation for drift analysis."""
        self.observations.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "query_hash": hashlib.sha256(query.encode()).hexdigest()[:12],
            "matched_topic": matched_topic,
            "confidence": confidence,
        })
        if len(self.observations) > 5000:
            self.observations = self.observations[-5000:]

    def get_drift_report(self) -> Dict[str, Any]:
        """Generate drift analysis report."""
        if not self.observations:
            return {
                "status": "no_data",
                "baseline_doctrines": self.baseline_doctrine_count,
                "observation_count": 0,
            }
        total = len(self.observations)
        misses = sum(1 for o in self.observations if o["matched_topic"] is None)
        miss_rate = misses / total if total > 0 else 0.0
        topic_counts: Dict[str, int] = defaultdict(int)
        for obs in self.observations:
            if obs["matched_topic"]:
                topic_counts[obs["matched_topic"]] += 1
        top_topics = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        confidence_dist: Dict[str, int] = defaultdict(int)
        for obs in self.observations:
            confidence_dist[obs["confidence"]] += 1
        return {
            "status": "active",
            "baseline_doctrines": self.baseline_doctrine_count,
            "current_doctrines": len(DOCTRINE_BLOCKS),
            "observation_count": total,
            "miss_rate": round(miss_rate, 4),
            "drift_detected": miss_rate > 0.30,
            "top_topics": top_topics,
            "confidence_distribution": dict(confidence_dist),
            "baseline_timestamp": self.baseline_timestamp,
            "latest_observation": self.observations[-1]["timestamp"] if self.observations else None,
        }


# ==========================================================================
# TIE COMPONENT 10 - COVERAGE MAP
# ==========================================================================

class CoverageMap:
    """Track triggered versus missed doctrines for epistemic gap detection."""

    def __init__(self) -> None:
        self.triggered: Dict[str, int] = defaultdict(int)
        self.queries_without_match: int = 0
        self.total_queries: int = 0
        self.gap_queries: List[str] = []

    def record_hit(self, topic: str) -> None:
        """Record a doctrine cache hit."""
        self.triggered[topic] += 1
        self.total_queries += 1

    def record_miss(self, query_snippet: str) -> None:
        """Record a doctrine cache miss."""
        self.queries_without_match += 1
        self.total_queries += 1
        self.gap_queries.append(query_snippet[:200])
        if len(self.gap_queries) > 500:
            self.gap_queries = self.gap_queries[-500:]

    def get_coverage_report(self) -> Dict[str, Any]:
        """Generate coverage report with gap analysis."""
        all_topics = {b.topic for b in DOCTRINE_BLOCKS}
        triggered_topics = set(self.triggered.keys())
        untriggered = all_topics - triggered_topics
        coverage_pct = len(triggered_topics) / len(all_topics) * 100 if all_topics else 0.0
        return {
            "total_doctrines": len(all_topics),
            "triggered_doctrines": len(triggered_topics),
            "untriggered_doctrines": len(untriggered),
            "coverage_percentage": round(coverage_pct, 2),
            "total_queries": self.total_queries,
            "miss_count": self.queries_without_match,
            "miss_rate": round(self.queries_without_match / max(self.total_queries, 1), 4),
            "triggered_topics": dict(self.triggered),
            "untriggered_topics": list(untriggered),
            "recent_gap_queries": self.gap_queries[-20:],
        }


# ==========================================================================
# TIE COMPONENT 11 - METRICS COLLECTOR
# ==========================================================================

class MetricsCollector:
    """Lightweight operational metrics for bond engine."""

    def __init__(self) -> None:
        self.latencies: List[float] = []
        self.errors: List[float] = []
        self.queries: List[float] = []
        self.doctrine_hits: int = 0
        self.doctrine_misses: int = 0
        self.last_error: Optional[str] = None
        self.active_queries: int = 0
        self._max_latencies: int = 200

    def record_query(self, latency_ms: float, doctrine_hit: bool) -> None:
        """Record a completed query with latency and cache hit info."""
        now = time.time()
        self.latencies.append(latency_ms)
        if len(self.latencies) > self._max_latencies:
            self.latencies.pop(0)
        self.queries.append(now)
        cutoff = now - 3600
        self.queries = [t for t in self.queries if t > cutoff]
        if doctrine_hit:
            self.doctrine_hits += 1
        else:
            self.doctrine_misses += 1

    def record_error(self, error_msg: str) -> None:
        """Record an error occurrence."""
        self.errors.append(time.time())
        self.last_error = f"{datetime.now(timezone.utc).isoformat()}: {error_msg[:200]}"
        cutoff = time.time() - 86400
        self.errors = [t for t in self.errors if t > cutoff]

    def get_metrics(self) -> Dict[str, Any]:
        """Return current metrics snapshot."""
        now = time.time()
        queries_last_hour = len([t for t in self.queries if t > now - 3600])
        avg_latency = sum(self.latencies) / len(self.latencies) if self.latencies else 0.0
        p50 = sorted(self.latencies)[len(self.latencies) // 2] if self.latencies else 0.0
        p95_idx = int(len(self.latencies) * 0.95)
        p95 = sorted(self.latencies)[min(p95_idx, len(self.latencies) - 1)] if self.latencies else 0.0
        total_doctrine = self.doctrine_hits + self.doctrine_misses
        hit_rate = self.doctrine_hits / total_doctrine if total_doctrine > 0 else 0.0
        return {
            "queries_last_hour": queries_last_hour,
            "total_queries": self.doctrine_hits + self.doctrine_misses,
            "avg_latency_ms": round(avg_latency, 2),
            "p50_latency_ms": round(p50, 2),
            "p95_latency_ms": round(p95, 2),
            "doctrine_hit_rate": round(hit_rate, 4),
            "doctrine_hits": self.doctrine_hits,
            "doctrine_misses": self.doctrine_misses,
            "errors_last_24h": len(self.errors),
            "last_error": self.last_error,
            "active_queries": self.active_queries,
        }


# ==========================================================================
# TIE COMPONENT 15 - AUDIT TRAIL (JSONL)
# ==========================================================================

class AuditTrail:
    """Append-only JSONL audit trail for every query processed."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.entries: List[Dict[str, Any]] = []

    def log_query(
        self,
        query_id: str,
        query_text: str,
        response_mode: str,
        zone: str,
        matched_topics: List[str],
        confidence: str,
        stratification: str,
        authority: str,
        latency_ms: float,
        determinism_hash: str,
    ) -> None:
        """Append an audit entry for a processed query."""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "query_id": query_id,
            "engine": ENGINE_ID,
            "version": ENGINE_VERSION,
            "query_hash": hashlib.sha256(query_text.encode()).hexdigest()[:16],
            "response_mode": response_mode,
            "zone": zone,
            "matched_topics": matched_topics,
            "confidence": confidence,
            "stratification": stratification,
            "primary_authority": authority,
            "latency_ms": round(latency_ms, 2),
            "determinism_hash": determinism_hash,
        }
        self.entries.append(entry)
        if len(self.entries) > 10000:
            self.entries = self.entries[-10000:]
        try:
            with open(self.path, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
        except OSError as exc:
            logger.error(f"Audit trail write error: {exc}")

    def get_recent(self, count: int = 50) -> List[Dict[str, Any]]:
        """Return last N audit entries."""
        return self.entries[-count:]


# ==========================================================================
# ENUMS AND MODELS
# ==========================================================================

class BondType(str, Enum):
    INDIVIDUAL = "individual"
    BLANKET = "blanket"
    LETTER_OF_CREDIT = "letter_of_credit"
    CASH_DEPOSIT = "cash_deposit"
    CERTIFICATE_OF_DEPOSIT = "certificate_of_deposit"


class WellCategory(str, Enum):
    OIL = "oil"
    GAS = "gas"
    INJECTION = "injection"
    BAY_ESTUARY = "bay_estuary"
    H2S = "h2s"


class ResponseMode(str, Enum):
    FAST = "fast"
    DEFENSE = "defense"
    MEMO = "memo"


# ==========================================================================
# PYDANTIC MODELS
# ==========================================================================

class QueryRequest(BaseModel):
    """General bond query request."""
    query: str = Field(..., min_length=3, description="Natural language bond question")
    mode: ResponseMode = Field(ResponseMode.FAST, description="Response mode")
    zone: Optional[AnalysisZone] = Field(None, description="Analysis zone override")
    include_authorities: bool = Field(True, description="Include authority citations")
    include_fragility: bool = Field(False, description="Include fact fragility scores")


class BondRequest(BaseModel):
    """Structured bond calculation request."""
    well_count: int = Field(..., ge=1, description="Number of wells")
    well_depths: Optional[List[int]] = Field(None, description="Individual well depths in feet")
    well_categories: Optional[List[WellCategory]] = Field(None, description="Per-well categories")
    bay_estuary_count: int = Field(0, ge=0, description="Bay/estuary wells count")
    h2s_count: int = Field(0, ge=0, description="H2S wells count")
    injection_count: int = Field(0, ge=0, description="Injection wells count")
    operator_name: Optional[str] = Field(None, description="Operator name for P-5 reference")
    bond_type_preference: Optional[BondType] = Field(None, description="Preferred bond type")
    mode: ResponseMode = Field(ResponseMode.FAST, description="Response mode")
    include_alternatives: bool = Field(True, description="Include alternative security options")

    class Config:
        use_enum_values = True


class BondLineItem(BaseModel):
    """Individual well bond line item."""
    well_number: int
    depth_feet: int
    category: str
    base_amount: float
    multiplier: float
    bond_amount: float
    regulatory_cite: str


class BondCalculation(BaseModel):
    """Single bond type calculation result."""
    bond_type: str
    total_amount: float
    per_well_amount: Optional[float] = None
    well_count_applicable: int
    regulatory_cite: str
    calculation_method: str
    authority_weight: float
    alternatives: List[Dict[str, Any]]

    class Config:
        use_enum_values = True


class BondResponse(BaseModel):
    """Full bond calculation response."""
    query_id: str
    well_count: int
    total_bond_required: float
    recommended_bond_type: str
    individual_well_bonds: Optional[List[BondLineItem]] = None
    individual_total: Optional[float] = None
    blanket_bond_option: Optional[BondCalculation] = None
    alternative_securities: List[Dict[str, Any]]
    primary_authority: str
    authority_weight: float
    confidence: str
    confidence_stratification: str
    zone: str
    reasoning: str
    disclosure_caveat: Optional[str] = None
    fragility: Optional[Dict[str, Any]] = None
    determinism_hash: str
    telemetry: Dict[str, Any]

    class Config:
        use_enum_values = True


class QueryResponse(BaseModel):
    """General query response."""
    query_id: str
    query: str
    normalized_query: str
    matched_doctrines: List[Dict[str, Any]]
    answer: str
    mode: str
    zone: str
    primary_authority: str
    authority_weight: float
    confidence: str
    confidence_stratification: str
    disclosure_caveat: Optional[str] = None
    fragility: Optional[Dict[str, Any]] = None
    determinism_hash: str
    telemetry: Dict[str, Any]


# ==========================================================================
# BOND AMOUNT TABLES - 16 TAC 3.78
# ==========================================================================

INDIVIDUAL_BOND_AMOUNTS: Dict[tuple, float] = {
    (0, 2000): 2_000.00,
    (2001, 4000): 4_000.00,
    (4001, 6000): 6_000.00,
    (6001, 10000): 10_000.00,
    (10001, 999_999): 25_000.00,
}

BLANKET_BOND_TABLE: List[tuple] = [
    (1, 10, 25_000.00),
    (11, 25, 50_000.00),
    (26, 100, 125_000.00),
    (101, 250, 250_000.00),
    (251, 999_999, 250_000.00),
]

CATEGORY_MULTIPLIERS: Dict[WellCategory, float] = {
    WellCategory.OIL: 1.0,
    WellCategory.GAS: 1.0,
    WellCategory.INJECTION: 2.0,
    WellCategory.BAY_ESTUARY: 2.0,
    WellCategory.H2S: 1.5,
}

CATEGORY_CITES: Dict[WellCategory, str] = {
    WellCategory.OIL: "16 TAC 3.78(a)",
    WellCategory.GAS: "16 TAC 3.78(a)",
    WellCategory.INJECTION: "16 TAC 3.78(b)",
    WellCategory.BAY_ESTUARY: "16 TAC 3.78(b)",
    WellCategory.H2S: "16 TAC 3.78(b)",
}

SPECIAL_WELL_SURCHARGE = 5_000.00
OVER_250_PER_WELL = 2_500.00


# ==========================================================================
# BOND DOMAIN KNOWLEDGE
# ==========================================================================

BOND_DOMAIN_KNOWLEDGE: Dict[str, str] = {
    "p5_organization_report": (
        "Every operator in Texas must file a Form P-5 (Organization Report) with the "
        "Railroad Commission before commencing operations. The P-5 establishes the "
        "operator's identity, financial responsibility, and bonding status. An operator "
        "cannot obtain a drilling permit (Form W-1) without an active P-5 and current "
        "bond on file. The P-5 must be renewed annually and updated within 30 days of "
        "any material change in organization."
    ),
    "financial_assurance_requirements": (
        "Texas requires operators to maintain continuous financial assurance for all "
        "wells operated. Financial assurance may take the form of: (1) surety bond, "
        "(2) cash deposit, (3) letter of credit, or (4) certificate of deposit. The "
        "RRC may require additional financial assurance if the operator has compliance "
        "issues, excessive inactive wells, or environmental violations. Financial "
        "assurance must remain in effect until all wells are properly plugged and "
        "abandoned and sites restored."
    ),
    "bond_increase_triggers": (
        "The RRC may increase bond requirements when: (1) the operator accumulates "
        "violations or enforcement actions; (2) the operator has a high ratio of "
        "inactive to active wells (greater than 10%); (3) the operator fails to "
        "timely plug wells on the inactive well list; (4) environmental contamination "
        "is identified at operator sites; (5) the operator's P-5 status is "
        "jeopardized. Bond increases are determined by RRC staff and may be appealed "
        "through the administrative hearing process under TX NRC 91.142."
    ),
    "bond_release_criteria": (
        "Bond release requires: (1) all wells properly plugged per Statewide Rule 14; "
        "(2) all surface equipment removed; (3) site restored to pre-drilling condition; "
        "(4) all RRC reports current (production, H-1, H-10); (5) no pending enforcement "
        "actions; (6) Form W-3A (plugging record) filed and approved; (7) RRC field "
        "inspection passed. Partial release may be granted as individual wells are plugged. "
        "Full release typically takes 6-18 months after final well plugged."
    ),
    "forfeiture_process": (
        "Bond forfeiture occurs when: (1) the operator fails to plug wells within the "
        "timeframe ordered by the RRC; (2) the operator becomes insolvent or ceases "
        "operations without properly abandoning wells; (3) the operator's P-5 is revoked "
        "and wells remain unplugged. Upon forfeiture, the surety is liable for the full "
        "bond amount. If the bond is insufficient to cover plugging costs, the RRC may "
        "access the Oil Field Cleanup Fund (OFCUF) under TX NRC 91.457 for remaining costs. "
        "Average plugging cost per well is $8-15/ft, often exceeding bond amounts."
    ),
    "inactive_well_bonding": (
        "Operators with wells on the RRC's inactive well list face additional bonding "
        "requirements. Wells inactive for more than 12 months must be reported on the "
        "annual H-15 filing. Operators must either: (1) plug inactive wells, (2) restore "
        "them to production, (3) obtain an extension by demonstrating future utility, or "
        "(4) post additional financial assurance. The RRC may require an individual bond "
        "for each inactive well beyond the blanket bond threshold. Per TX NRC 89.011, "
        "operators with excessive inactive wells may face higher total bond requirements."
    ),
    "alternative_security_details": (
        "Letters of credit must be irrevocable, issued by a Texas-licensed bank or "
        "federally-insured institution, payable to the Railroad Commission, and must "
        "contain an auto-renewal clause with 60-day advance notice of cancellation. "
        "Cash deposits are held in the State Treasury and earn no interest for the "
        "operator. Certificates of deposit must be assigned to the RRC and maintained "
        "at federally-insured institutions. The RRC does not accept personal guarantees, "
        "real property liens, or insurance policies as bond alternatives."
    ),
    "multi_state_operator_bonding": (
        "Operators working across multiple states must maintain separate bonding in each "
        "jurisdiction. Texas bonds do not satisfy New Mexico, Oklahoma, or federal "
        "requirements. Federal leases on Texas lands require separate BLM bonds per "
        "43 CFR 3104. Operators should evaluate blanket vs. individual bonding in each "
        "jurisdiction independently based on well counts and depth profiles."
    ),
}


# ==========================================================================
# TIE COMPONENT 19 - MULTI-DOCTRINE DECOMPOSITION
# ==========================================================================

ISSUE_CATEGORY_STRATA: Dict[str, List[str]] = {
    "bond_calculation": [
        "individual_well_bond_calculation",
        "blanket_bond_tiers",
        "depth_based_bond_amounts",
        "special_well_surcharges",
        "bond_cost_optimization",
    ],
    "bond_types": [
        "surety_bond_mechanics",
        "letter_of_credit_alternative",
        "cash_deposit_alternative",
        "certificate_of_deposit_alternative",
        "bond_type_comparison",
    ],
    "alternative_security": [
        "letter_of_credit_alternative",
        "cash_deposit_alternative",
        "certificate_of_deposit_alternative",
    ],
    "operator_requirements": [
        "p5_organization_report",
        "operator_qualification_requirements",
        "bond_filing_requirements",
        "annual_renewal_requirements",
    ],
    "bond_release": [
        "bond_release_criteria",
        "partial_release_process",
        "surface_restoration_requirements",
        "final_release_timeline",
    ],
    "bond_forfeiture": [
        "bond_forfeiture_process",
        "surety_liability",
        "ofcuf_fund_access",
        "plugging_cost_recovery",
    ],
}

DOCTRINE_INTERACTION_EDGES: List[tuple] = [
    ("individual_well_bond_calculation", "blanket_bond_tiers", "comparison"),
    ("blanket_bond_tiers", "bond_cost_optimization", "optimization"),
    ("bond_increase_triggers", "inactive_well_bonding", "escalation"),
    ("bond_forfeiture_process", "bond_release_criteria", "lifecycle"),
    ("p5_organization_report", "operator_qualification_requirements", "prerequisite"),
    ("letter_of_credit_alternative", "bond_type_comparison", "substitution"),
    ("cash_deposit_alternative", "bond_type_comparison", "substitution"),
    ("certificate_of_deposit_alternative", "bond_type_comparison", "substitution"),
    ("individual_well_bond_calculation", "special_well_surcharges", "modifier"),
    ("bond_increase_triggers", "bond_forfeiture_process", "escalation"),
    ("inactive_well_bonding", "bond_release_criteria", "lifecycle"),
    ("operator_qualification_requirements", "bond_filing_requirements", "prerequisite"),
]


def decompose_issue(query: str) -> Dict[str, Any]:
    """Decompose a query into issue categories and relevant strata."""
    normalized = normalize_bond_query(query)
    keywords = extract_bond_keywords(normalized)
    matched_categories: Dict[str, float] = {}
    for cat_key, strata_topics in ISSUE_CATEGORY_STRATA.items():
        score = 0.0
        for topic in strata_topics:
            topic_words = topic.replace("_", " ").split()
            overlap = len(set(keywords) & set(topic_words))
            if overlap > 0:
                score += overlap / len(topic_words)
        if score > 0:
            matched_categories[cat_key] = score
    relevant_edges = []
    all_matched_topics: set = set()
    for cat_key in matched_categories:
        all_matched_topics.update(ISSUE_CATEGORY_STRATA.get(cat_key, []))
    for src, dst, rel in DOCTRINE_INTERACTION_EDGES:
        if src in all_matched_topics or dst in all_matched_topics:
            relevant_edges.append({"source": src, "target": dst, "relationship": rel})
    return {
        "categories": matched_categories,
        "strata": {k: ISSUE_CATEGORY_STRATA[k] for k in matched_categories},
        "interaction_edges": relevant_edges,
        "keyword_count": len(keywords),
    }


# ==========================================================================
# CORE BOND CALCULATION FUNCTIONS
# ==========================================================================

def calculate_individual_bond(depth_feet: int, category: WellCategory) -> Dict[str, Any]:
    """Calculate individual well bond amount with full detail."""
    base_amount = 2_000.00
    cite = "16 TAC 3.78(a)"
    for (min_depth, max_depth), amount in INDIVIDUAL_BOND_AMOUNTS.items():
        if min_depth <= depth_feet <= max_depth:
            base_amount = amount
            break
    multiplier = CATEGORY_MULTIPLIERS.get(category, 1.0)
    category_cite = CATEGORY_CITES.get(category, cite)
    final_amount = base_amount * multiplier
    return {
        "base_amount": base_amount,
        "multiplier": multiplier,
        "final_amount": final_amount,
        "depth_feet": depth_feet,
        "category": category.value if isinstance(category, WellCategory) else category,
        "regulatory_cite": category_cite,
    }


def calculate_blanket_bond(well_count: int, special_well_count: int = 0) -> Dict[str, Any]:
    """Calculate blanket bond amount with full detail."""
    base_amount = 25_000.00
    tier_desc = "1-10 wells"
    for min_wells, max_wells, amount in BLANKET_BOND_TABLE:
        if min_wells <= well_count <= max_wells:
            base_amount = amount
            tier_desc = f"{min_wells}-{max_wells} wells"
            break
    overage = 0.0
    if well_count > 250:
        overage = (well_count - 250) * OVER_250_PER_WELL
        base_amount += overage
    surcharge = special_well_count * SPECIAL_WELL_SURCHARGE
    total = base_amount + surcharge
    return {
        "base_amount": base_amount - overage,
        "overage_amount": overage,
        "special_well_surcharge": surcharge,
        "special_well_count": special_well_count,
        "total_amount": total,
        "well_count": well_count,
        "tier": tier_desc,
        "regulatory_cite": "16 TAC 3.78(c)",
    }


def calculate_alternative_securities(amount: float) -> List[Dict[str, Any]]:
    """Calculate alternative security options for a given bond amount."""
    return [
        {
            "type": "Surety Bond",
            "amount": amount,
            "annual_premium_estimate": round(amount * 0.015, 2),
            "premium_range": "1-3% of bond amount annually",
            "issuer_requirements": "Licensed surety company authorized in Texas",
            "regulatory_cite": "16 TAC 3.78(a)-(c)",
            "advantages": "No capital outlay beyond premium; most common form",
            "disadvantages": "Annual premium cost; surety may decline renewal",
        },
        {
            "type": "Letter of Credit",
            "amount": amount,
            "annual_fee_estimate": round(amount * 0.02, 2),
            "fee_range": "1-3% of face value annually",
            "issuer_requirements": "Texas-licensed bank or federally-insured institution",
            "requirements": "Irrevocable, auto-renewal, 60-day cancellation notice",
            "regulatory_cite": "16 TAC 3.78(f)",
            "advantages": "No premium to third party; may be cheaper than surety",
            "disadvantages": "Reduces bank credit capacity; annual renewal burden",
        },
        {
            "type": "Cash Deposit",
            "amount": amount,
            "held_by": "State Treasury via Railroad Commission",
            "interest": "None - operator earns no interest on deposit",
            "regulatory_cite": "16 TAC 3.78(g)",
            "advantages": "No annual fees; no third-party dependency",
            "disadvantages": "Full capital outlay; no interest earned; ties up cash",
        },
        {
            "type": "Certificate of Deposit",
            "amount": amount,
            "requirements": "Assigned to RRC, federally insured institution",
            "interest": "Operator may retain interest if CD terms permit",
            "regulatory_cite": "16 TAC 3.78(h)",
            "advantages": "May earn interest; relatively safe",
            "disadvantages": "Capital tied up; must maintain at qualifying institution",
        },
    ]


# ==========================================================================
# DOCTRINE CACHE LOOKUP (TIE COMPONENT 1 - LAYER 1)
# ==========================================================================

def doctrine_cache_lookup(query: str) -> Optional[DoctrineBlock]:
    """Layer 1: Fast doctrine cache lookup (target <200ms)."""
    normalized = normalize_bond_query(query)
    keywords = set(extract_bond_keywords(normalized))
    if not keywords:
        return None
    best_match: Optional[DoctrineBlock] = None
    best_score = 0.0
    for block in DOCTRINE_BLOCKS:
        block_keywords = set(kw.lower() for kw in block.keywords)
        overlap = len(keywords & block_keywords)
        if overlap > 0:
            score = overlap / max(len(block_keywords), 1)
            topic_words = set(block.topic.lower().replace("_", " ").split())
            topic_overlap = len(keywords & topic_words)
            score += topic_overlap * 0.3
            if block.confidence == ConfidenceLevel.HIGH:
                score *= 1.2
            elif block.confidence == ConfidenceLevel.MEDIUM:
                score *= 1.0
            elif block.confidence == ConfidenceLevel.LOW:
                score *= 0.8
            if score > best_score:
                best_score = score
                best_match = block
    if best_score < 0.15:
        return None
    return best_match


# ==========================================================================
# VECTOR SEARCH FALLBACK (TIE COMPONENT 7 - LAYER 2)
# ==========================================================================

def vector_search_fallback(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """Layer 2: Semantic vector search fallback when doctrine cache misses."""
    results = search.vector_search_fallback(query, top_k=top_k)
    domain_results = []
    normalized = normalize_bond_query(query)
    keywords = extract_bond_keywords(normalized)
    for key, knowledge in BOND_DOMAIN_KNOWLEDGE.items():
        knowledge_lower = knowledge.lower()
        overlap = sum(1 for kw in keywords if kw in knowledge_lower)
        if overlap > 0:
            score = overlap / max(len(keywords), 1)
            domain_results.append({
                "topic": key,
                "category": "domain_knowledge",
                "score": score,
                "source": "bond_domain_knowledge",
                "snippet": knowledge[:300],
            })
    combined = results + domain_results
    combined.sort(key=lambda x: x.get("score", 0), reverse=True)
    return combined[:top_k]


# ==========================================================================
# DEEP ANALYSIS (TIE COMPONENT 20 - LAYER 3)
# ==========================================================================

def deep_analysis(query: str, zone: AnalysisZone) -> Dict[str, Any]:
    """Layer 3: Deep multi-source analysis for complex bond questions."""
    decomposition = decompose_issue(query)
    doctrine_match = doctrine_cache_lookup(query)
    search_results = vector_search_fallback(query, top_k=8)
    normalized = normalize_bond_query(query)
    keywords = extract_bond_keywords(normalized)
    relevant_knowledge: List[Dict[str, str]] = []
    for key, text in BOND_DOMAIN_KNOWLEDGE.items():
        text_lower = text.lower()
        if any(kw in text_lower for kw in keywords):
            relevant_knowledge.append({"topic": key, "content": text})
    all_authorities: List[str] = []
    if doctrine_match:
        all_authorities.extend(doctrine_match.primary_authority)
    for result in search_results:
        if "regulatory_cite" in result:
            all_authorities.append(result["regulatory_cite"])
    primary_authority = resolve_authority_conflict(all_authorities) if all_authorities else "16 TAC 3.78"
    reasoning_chain: List[str] = []
    reasoning_chain.append(f"Query decomposed into {len(decomposition['categories'])} issue categories.")
    if doctrine_match:
        reasoning_chain.append(f"Doctrine cache hit: '{doctrine_match.topic}' with confidence {doctrine_match.confidence.value}.")
        reasoning_chain.extend(doctrine_match.conclusion_template)
    if search_results:
        reasoning_chain.append(f"Semantic search returned {len(search_results)} relevant results.")
    if relevant_knowledge:
        reasoning_chain.append(f"Domain knowledge matched {len(relevant_knowledge)} knowledge blocks.")
        for rk in relevant_knowledge[:3]:
            reasoning_chain.append(f"  - {rk['topic']}: {rk['content'][:150]}...")
    if zone == AnalysisZone.AUDIT:
        reasoning_chain.append(f"AUDIT ZONE: Primary authority is {primary_authority} (weight {get_authority_weight(primary_authority):.2f}).")
        reasoning_chain.append("All assertions must trace to statutory or regulatory authority.")
    elif zone == AnalysisZone.PLANNING:
        reasoning_chain.append("PLANNING ZONE: Analysis includes forward-looking recommendations.")
    fragility = score_bond_fragility(doctrine_match.topic if doctrine_match else "unknown")
    confidence = ConfidenceLevel.HIGH if doctrine_match else ConfidenceLevel.MEDIUM
    auth_weight = get_authority_weight(primary_authority)
    strat = stratify_confidence(confidence, auth_weight, doctrine_match is not None)
    return {
        "decomposition": decomposition,
        "doctrine_match": {
            "topic": doctrine_match.topic,
            "category": doctrine_match.category.value,
            "confidence": doctrine_match.confidence.value,
        } if doctrine_match else None,
        "search_results_count": len(search_results),
        "domain_knowledge_count": len(relevant_knowledge),
        "reasoning_chain": reasoning_chain,
        "primary_authority": primary_authority,
        "authority_weight": auth_weight,
        "confidence": confidence.value,
        "stratification": strat.value,
        "fragility": {
            "verifiability": fragility.verifiability,
            "recharacterization_risk": fragility.recharacterization_risk,
            "testimony_dependence": fragility.testimony_dependence,
            "regulatory_change_risk": fragility.regulatory_change_risk,
            "overall": fragility.overall,
        },
        "zone": zone.value,
    }


# ==========================================================================
# TIE COMPONENT 16 - DETERMINISM HASH (SHA-256)
# ==========================================================================

def compute_determinism_hash(data: Dict[str, Any]) -> str:
    """Compute SHA-256 determinism hash for reproducibility."""
    canonical = json.dumps(data, sort_keys=True, default=str)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


# ==========================================================================
# TIE COMPONENT 1 - THREE LAYER RESPONSE (bond calculation)
# ==========================================================================

def three_layer_bond_response(
    request: BondRequest,
    metrics: MetricsCollector,
    drift: DriftWatcher,
    coverage: CoverageMap,
    audit: AuditTrail,
) -> BondResponse:
    """Full three-layer response for structured bond calculation."""
    start_time = time.time()
    query_id = str(uuid.uuid4())[:12]
    zone = AnalysisZone.REPORTING

    # --- Layer 1: Calculate individual bonds ---
    individual_items: List[BondLineItem] = []
    total_individual = 0.0
    for i in range(request.well_count):
        depth = request.well_depths[i] if request.well_depths and i < len(request.well_depths) else 5000
        cat_val = request.well_categories[i] if request.well_categories and i < len(request.well_categories) else WellCategory.OIL
        if isinstance(cat_val, str):
            cat_val = WellCategory(cat_val)
        calc = calculate_individual_bond(depth, cat_val)
        item = BondLineItem(
            well_number=i + 1,
            depth_feet=depth,
            category=calc["category"],
            base_amount=calc["base_amount"],
            multiplier=calc["multiplier"],
            bond_amount=calc["final_amount"],
            regulatory_cite=calc["regulatory_cite"],
        )
        individual_items.append(item)
        total_individual += calc["final_amount"]

    # --- Layer 1: Calculate blanket bond ---
    special_count = request.bay_estuary_count + request.h2s_count + request.injection_count
    blanket_calc = calculate_blanket_bond(request.well_count, special_count)
    blanket_total = blanket_calc["total_amount"]

    # --- Determine recommendation ---
    if blanket_total < total_individual:
        recommended_type = BondType.BLANKET
        recommended_amount = blanket_total
        savings = total_individual - blanket_total
        reasoning = (
            f"Blanket bond recommended for {request.well_count} wells. "
            f"Blanket: ${blanket_total:,.2f} vs Individual total: ${total_individual:,.2f}. "
            f"Savings of ${savings:,.2f} with blanket bond. "
            f"Blanket tier: {blanket_calc['tier']}."
        )
    else:
        recommended_type = BondType.INDIVIDUAL
        recommended_amount = total_individual
        reasoning = (
            f"Individual bonds recommended for {request.well_count} wells. "
            f"Individual total: ${total_individual:,.2f} vs Blanket: ${blanket_total:,.2f}. "
            f"Individual bonding is more economical for this well configuration."
        )
    if special_count > 0:
        reasoning += (
            f" Includes {special_count} special wells "
            f"(bay/estuary: {request.bay_estuary_count}, H2S: {request.h2s_count}, "
            f"injection: {request.injection_count}) with surcharge of "
            f"${blanket_calc['special_well_surcharge']:,.2f}."
        )

    # Override with preference if provided
    if request.bond_type_preference:
        pref = BondType(request.bond_type_preference)
        if pref in (BondType.INDIVIDUAL, BondType.BLANKET):
            recommended_type = pref
            recommended_amount = total_individual if pref == BondType.INDIVIDUAL else blanket_total
            reasoning += f" Operator preference override to {pref.value} bond."

    # --- Alternative securities ---
    alternatives = calculate_alternative_securities(recommended_amount) if request.include_alternatives else []

    # --- Build blanket calculation model ---
    blanket_model = BondCalculation(
        bond_type=BondType.BLANKET.value,
        total_amount=blanket_total,
        per_well_amount=round(blanket_total / max(request.well_count, 1), 2),
        well_count_applicable=request.well_count,
        regulatory_cite="16 TAC 3.78(c)",
        calculation_method=(
            f"Base: ${blanket_calc['base_amount']:,.2f} for {blanket_calc['tier']} tier. "
            f"Overage: ${blanket_calc['overage_amount']:,.2f}. "
            f"Special surcharge: ${blanket_calc['special_well_surcharge']:,.2f}."
        ),
        authority_weight=get_authority_weight("16 TAC 3.78(c)"),
        alternatives=alternatives,
    )

    # --- Confidence & stratification ---
    primary_authority = "16 TAC 3.78"
    auth_weight = get_authority_weight(primary_authority)
    confidence = ConfidenceLevel.HIGH
    strat = stratify_confidence(confidence, auth_weight, True)
    disclosure_caveat = (
        "Bond amounts are based on 16 TAC 3.78 schedules as of the engine build date. "
        "The RRC may impose additional bonding requirements based on operator compliance "
        "history, inactive well counts, or environmental conditions. Verify current "
        "requirements with the RRC Financial Assurance Section before filing."
    )

    # --- Determinism hash ---
    hash_data = {
        "well_count": request.well_count,
        "special_count": special_count,
        "individual_total": total_individual,
        "blanket_total": blanket_total,
        "recommended": recommended_type.value,
    }
    det_hash = compute_determinism_hash(hash_data)

    # --- Telemetry ---
    elapsed = time.time() - start_time
    latency_ms = elapsed * 1000
    metrics.record_query(latency_ms, True)
    drift.observe(f"calculate:{request.well_count}wells", "bond_calculation", confidence.value)
    coverage.record_hit("bond_calculation")

    # --- Audit ---
    audit.log_query(
        query_id=query_id,
        query_text=f"calculate: {request.well_count} wells, {special_count} special",
        response_mode=request.mode if isinstance(request.mode, str) else request.mode.value,
        zone=zone.value,
        matched_topics=["individual_well_bond_calculation", "blanket_bond_tiers"],
        confidence=confidence.value,
        stratification=strat.value,
        authority=primary_authority,
        latency_ms=latency_ms,
        determinism_hash=det_hash,
    )

    reasoning = apply_epistemic_guardrails(reasoning)

    return BondResponse(
        query_id=query_id,
        well_count=request.well_count,
        total_bond_required=recommended_amount,
        recommended_bond_type=recommended_type.value,
        individual_well_bonds=individual_items,
        individual_total=total_individual,
        blanket_bond_option=blanket_model,
        alternative_securities=alternatives,
        primary_authority=primary_authority,
        authority_weight=auth_weight,
        confidence=confidence.value,
        confidence_stratification=strat.value,
        zone=zone.value,
        reasoning=reasoning,
        disclosure_caveat=disclosure_caveat,
        determinism_hash=det_hash,
        telemetry={"latency_ms": round(latency_ms, 2), "layer": "doctrine_cache"},
    )


# ==========================================================================
# TIE COMPONENT 1 - THREE LAYER RESPONSE (general query)
# ==========================================================================

def three_layer_query_response(
    request: QueryRequest,
    metrics: MetricsCollector,
    drift: DriftWatcher,
    coverage: CoverageMap,
    audit: AuditTrail,
) -> QueryResponse:
    """Full three-layer response for natural language bond queries."""
    start_time = time.time()
    query_id = str(uuid.uuid4())[:12]
    zone = request.zone if request.zone else detect_analysis_zone(request.query)
    mode = request.mode if isinstance(request.mode, str) else request.mode.value
    normalized = normalize_bond_query(request.query)

    # --- Layer 1: Doctrine cache ---
    doctrine_match = doctrine_cache_lookup(request.query)
    matched_doctrines: List[Dict[str, Any]] = []
    answer_parts: List[str] = []
    doctrine_hit = doctrine_match is not None

    if doctrine_match:
        coverage.record_hit(doctrine_match.topic)
        matched_doctrines.append({
            "topic": doctrine_match.topic,
            "category": doctrine_match.category.value,
            "confidence": doctrine_match.confidence.value,
            "stratification": doctrine_match.confidence_stratification,
            "layer": "doctrine_cache",
        })
        answer_parts.extend(doctrine_match.conclusion_template)
        if mode in ("defense", "memo"):
            answer_parts.append("")
            answer_parts.append(f"Reasoning Framework: {doctrine_match.reasoning_framework.strip()}")
            answer_parts.append("")
            answer_parts.append(f"Key Factors: {', '.join(doctrine_match.key_factors)}")
            answer_parts.append(f"Primary Authority: {', '.join(doctrine_match.primary_authority)}")
    else:
        coverage.record_miss(request.query[:200])

    # --- Layer 2: Semantic retrieval fallback ---
    if not doctrine_hit or mode in ("defense", "memo"):
        search_results = vector_search_fallback(request.query, top_k=5)
        for result in search_results:
            if result.get("source") == "bond_domain_knowledge":
                matched_doctrines.append({
                    "topic": result["topic"],
                    "category": "domain_knowledge",
                    "score": result.get("score", 0),
                    "layer": "semantic_retrieval",
                })
                if not doctrine_hit:
                    answer_parts.append(result.get("snippet", "")[:500])
            elif result.get("topic"):
                matched_doctrines.append({
                    "topic": result["topic"],
                    "category": result.get("category", "unknown"),
                    "score": result.get("score", 0),
                    "layer": "semantic_retrieval",
                })

    # --- Layer 3: Deep analysis for DEFENSE/MEMO ---
    if mode in ("defense", "memo"):
        analysis = deep_analysis(request.query, zone)
        if analysis["reasoning_chain"]:
            answer_parts.append("")
            answer_parts.append("--- Deep Analysis ---")
            for step in analysis["reasoning_chain"]:
                answer_parts.append(f"  {step}")

    if not answer_parts:
        answer_parts.append(
            "No specific doctrine matched this query. The bond requirements engine "
            "covers: individual bond calculation, blanket bond tiers, alternative "
            "securities, operator requirements, bond release, and bond forfeiture. "
            "Please refine your query or use the /calculate endpoint for structured "
            "bond calculations."
        )

    # --- Confidence & authority ---
    all_authorities: List[str] = []
    if doctrine_match:
        all_authorities.extend(doctrine_match.primary_authority)
    primary_authority = resolve_authority_conflict(all_authorities) if all_authorities else "16 TAC 3.78"
    auth_weight = get_authority_weight(primary_authority)
    confidence = doctrine_match.confidence if doctrine_match else ConfidenceLevel.MEDIUM
    strat = stratify_confidence(confidence, auth_weight, doctrine_hit)

    # --- Fragility ---
    fragility_data = None
    if request.include_fragility:
        frag = score_bond_fragility(doctrine_match.topic if doctrine_match else "unknown")
        fragility_data = {
            "verifiability": frag.verifiability,
            "recharacterization_risk": frag.recharacterization_risk,
            "testimony_dependence": frag.testimony_dependence,
            "regulatory_change_risk": frag.regulatory_change_risk,
            "overall": frag.overall,
        }

    # --- Disclosure caveat ---
    disclosure_caveat = None
    if strat in (ConfidenceStratification.DISCLOSURE, ConfidenceStratification.HIGH_RISK):
        disclosure_caveat = (
            "This response involves areas where regulatory interpretation may vary. "
            "Bond requirements may change based on operator compliance history and "
            "RRC discretion. Consult the RRC Financial Assurance Section for definitive guidance."
        )

    # --- Determinism hash ---
    hash_data = {
        "query": normalized,
        "matched_topics": [d["topic"] for d in matched_doctrines],
        "confidence": confidence.value,
    }
    det_hash = compute_determinism_hash(hash_data)

    # --- Finalize answer ---
    answer = "\n".join(answer_parts)
    answer = apply_epistemic_guardrails(answer)

    # --- Telemetry ---
    elapsed = time.time() - start_time
    latency_ms = elapsed * 1000
    metrics.record_query(latency_ms, doctrine_hit)
    drift.observe(
        request.query,
        doctrine_match.topic if doctrine_match else None,
        confidence.value,
    )

    # --- Audit ---
    audit.log_query(
        query_id=query_id,
        query_text=request.query,
        response_mode=mode,
        zone=zone.value if isinstance(zone, AnalysisZone) else zone,
        matched_topics=[d["topic"] for d in matched_doctrines],
        confidence=confidence.value,
        stratification=strat.value,
        authority=primary_authority,
        latency_ms=latency_ms,
        determinism_hash=det_hash,
    )

    return QueryResponse(
        query_id=query_id,
        query=request.query,
        normalized_query=normalized,
        matched_doctrines=matched_doctrines,
        answer=answer,
        mode=mode,
        zone=zone.value if isinstance(zone, AnalysisZone) else zone,
        primary_authority=primary_authority,
        authority_weight=auth_weight,
        confidence=confidence.value,
        confidence_stratification=strat.value,
        disclosure_caveat=disclosure_caveat,
        fragility=fragility_data,
        determinism_hash=det_hash,
        telemetry={"latency_ms": round(latency_ms, 2), "doctrine_hit": doctrine_hit},
    )


# ==========================================================================
# TIE COMPONENT 17 - FASTAPI SERVER
# ==========================================================================

# Singleton instances
_metrics = MetricsCollector()
_drift = DriftWatcher()
_coverage = CoverageMap()
_audit = AuditTrail(AUDIT_LOG_PATH)
_telemetry_collector = TelemetryCollector()


@asynccontextmanager
async def lifespan(application: FastAPI):
    """Application lifespan: startup and shutdown."""
    logger.info(
        f"R10 Bond Requirements Calculator v{ENGINE_VERSION} starting on port {ENGINE_PORT}"
    )
    logger.info(f"Loaded {len(DOCTRINE_BLOCKS)} doctrine blocks")
    logger.info(f"Authority weights configured for {len(AUTHORITY_WEIGHTS)} citations")
    logger.info(f"Domain knowledge blocks: {len(BOND_DOMAIN_KNOWLEDGE)}")
    logger.info(f"Banned phrases (epistemic guardrails): {len(BANNED_PHRASES)}")
    yield
    logger.info("R10 Bond Requirements Calculator shutting down")


app = FastAPI(
    title="R10 - Bond Requirements Calculator",
    version=ENGINE_VERSION,
    description=(
        "Calculate operator bond requirements per 16 TAC 3.78, TX NRC 91.103-104. "
        "TIE-20 Gold Standard compliant engine with doctrine cache, semantic retrieval, "
        "deep analysis, authority hardening, and epistemic guardrails."
    ),
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================================================
# TIE COMPONENT 12 - HEALTH ENDPOINT
# ==========================================================================

@app.get("/health")
async def health():
    """Comprehensive health check endpoint."""
    return {
        "status": "operational",
        "engine": ENGINE_ID,
        "version": ENGINE_VERSION,
        "port": ENGINE_PORT,
        "doctrine_blocks": len(DOCTRINE_BLOCKS),
        "authority_weights": len(AUTHORITY_WEIGHTS),
        "domain_knowledge_blocks": len(BOND_DOMAIN_KNOWLEDGE),
        "banned_phrases": len(BANNED_PHRASES),
        "issue_categories": len(ISSUE_CATEGORY_STRATA),
        "interaction_edges": len(DOCTRINE_INTERACTION_EDGES),
        "cloud_retriever_available": retrieve_from_cloud is not None,
        "metrics": _metrics.get_metrics(),
        "uptime_queries": _metrics.doctrine_hits + _metrics.doctrine_misses,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ==========================================================================
# MAIN ENDPOINTS
# ==========================================================================

@app.post("/calculate", response_model=BondResponse)
async def calculate_bond(request: BondRequest):
    """Structured bond calculation endpoint."""
    try:
        return three_layer_bond_response(request, _metrics, _drift, _coverage, _audit)
    except Exception as exc:
        _metrics.record_error(str(exc))
        logger.error(f"Bond calculation error: {exc}")
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/query", response_model=QueryResponse)
async def query_bond(request: QueryRequest):
    """Natural language bond query endpoint."""
    try:
        return three_layer_query_response(request, _metrics, _drift, _coverage, _audit)
    except Exception as exc:
        _metrics.record_error(str(exc))
        logger.error(f"Query error: {exc}")
        raise HTTPException(status_code=500, detail=str(exc))


# ==========================================================================
# TIE COMPONENT 11 - METRICS ENDPOINT
# ==========================================================================

@app.get("/metrics")
async def metrics():
    """Return operational metrics."""
    return _metrics.get_metrics()


# ==========================================================================
# TIE COMPONENT 9 - DRIFT ENDPOINT
# ==========================================================================

@app.get("/drift")
async def drift_report():
    """Return doctrine drift analysis."""
    return _drift.get_drift_report()


# ==========================================================================
# TIE COMPONENT 10 - COVERAGE ENDPOINT
# ==========================================================================

@app.get("/coverage")
async def coverage_report():
    """Return doctrine coverage map."""
    return _coverage.get_coverage_report()


# ==========================================================================
# DOCTRINE LISTING ENDPOINT
# ==========================================================================

@app.get("/doctrines")
async def list_doctrines():
    """List all doctrine blocks with metadata."""
    return {
        "count": len(DOCTRINE_BLOCKS),
        "doctrines": [
            {
                "topic": b.topic,
                "category": b.category.value,
                "keywords": b.keywords,
                "confidence": b.confidence.value,
                "stratification": b.confidence_stratification,
                "authority": b.primary_authority,
            }
            for b in DOCTRINE_BLOCKS
        ],
    }


# ==========================================================================
# AUTHORITY LISTING ENDPOINT
# ==========================================================================

@app.get("/authorities")
async def list_authorities():
    """List all authority weights and conflict resolution rules."""
    return {
        "count": len(AUTHORITY_WEIGHTS),
        "authorities": [
            {"citation": k, "weight": v}
            for k, v in sorted(AUTHORITY_WEIGHTS.items(), key=lambda x: x[1], reverse=True)
        ],
        "conflict_resolution": "Highest weight wins; ties broken by specificity",
    }


# ==========================================================================
# GUARDRAILS ENDPOINT
# ==========================================================================

@app.get("/guardrails")
async def list_guardrails():
    """List epistemic guardrails (banned phrases)."""
    return {
        "count": len(BANNED_PHRASES),
        "banned_phrases": BANNED_PHRASES,
        "policy": "Any output containing banned phrases is redacted before delivery",
    }


# ==========================================================================
# TIE COMPONENT 15 - AUDIT TRAIL ENDPOINT
# ==========================================================================

@app.get("/audit-trail")
async def get_audit_trail(count: int = 50):
    """Return recent audit trail entries."""
    entries = _audit.get_recent(count)
    return {
        "count": len(entries),
        "entries": entries,
    }


# ==========================================================================
# DOMAIN KNOWLEDGE ENDPOINT
# ==========================================================================

@app.get("/knowledge")
async def list_knowledge():
    """List all domain knowledge blocks."""
    return {
        "count": len(BOND_DOMAIN_KNOWLEDGE),
        "blocks": [
            {"topic": k, "content": v, "length": len(v)}
            for k, v in BOND_DOMAIN_KNOWLEDGE.items()
        ],
    }


# ==========================================================================
# ISSUE DECOMPOSITION ENDPOINT
# ==========================================================================

@app.post("/decompose")
async def decompose_endpoint(request: QueryRequest):
    """Decompose a query into issue categories and strata."""
    return decompose_issue(request.query)


# ==========================================================================
# FRAGILITY SCORING ENDPOINT
# ==========================================================================

@app.get("/fragility/{topic}")
async def fragility_endpoint(topic: str):
    """Get fact fragility score for a given topic."""
    score = score_bond_fragility(topic)
    return {
        "topic": topic,
        "verifiability": score.verifiability,
        "recharacterization_risk": score.recharacterization_risk,
        "testimony_dependence": score.testimony_dependence,
        "regulatory_change_risk": score.regulatory_change_risk,
        "overall": score.overall,
    }


# ==========================================================================
# ZONE INFO ENDPOINT
# ==========================================================================

@app.get("/zones")
async def list_zones():
    """List analysis zones and their descriptions."""
    return {
        "zones": [
            {"zone": z.value, "description": ZONE_DESCRIPTIONS[z]}
            for z in AnalysisZone
        ],
    }


# ==========================================================================
# BOND TABLES ENDPOINT (reference data)
# ==========================================================================

@app.get("/tables")
async def bond_tables():
    """Return bond amount reference tables."""
    return {
        "individual_bond_amounts": [
            {"min_depth": k[0], "max_depth": k[1], "amount": v}
            for k, v in INDIVIDUAL_BOND_AMOUNTS.items()
        ],
        "blanket_bond_tiers": [
            {"min_wells": t[0], "max_wells": t[1], "amount": t[2]}
            for t in BLANKET_BOND_TABLE
        ],
        "category_multipliers": {k.value: v for k, v in CATEGORY_MULTIPLIERS.items()},
        "special_well_surcharge": SPECIAL_WELL_SURCHARGE,
        "over_250_per_well": OVER_250_PER_WELL,
        "regulatory_cite": "16 TAC 3.78",
    }


# ==========================================================================
# ENTRYPOINT
# ==========================================================================

if __name__ == "__main__":
    import uvicorn

    logger.info(
        f"R10 Bond Requirements Calculator v{ENGINE_VERSION} launching on port {ENGINE_PORT}"
    )
    uvicorn.run(app, host="0.0.0.0", port=ENGINE_PORT)
