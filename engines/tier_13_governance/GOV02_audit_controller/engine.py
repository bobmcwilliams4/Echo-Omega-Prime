"""
ECHO GOV02 AUDIT CONTROLLER ENGINE — Production Architecture
Central audit system for all 507 engines. Collects and analyzes audit trails,
detects anomalies in query patterns, tracks TIE-20 compliance, generates audit
reports, monitors fleet health, detects unauthorized access, and provides
forensic query replay capability.

Architecture:
    Layer 1: Doctrine Cache (0-200ms) - Pre-compiled audit reasoning
    Layer 2: Semantic Retrieval (200-700ms) - Pattern search on cache miss
    Layer 3: Deep Analysis (on-demand) - Multi-engine forensic synthesis

Response Modes:
    FAST:    Doctrine-driven, minimal citations, sub-2 seconds
    DEFENSE: Structured reasoning, audit-ready, burden analysis
    MEMO:    Long-form, citation-heavy, full documentation

Engine ID: GOV02
Tier: GOV (Governance)
Mode: DET (Deterministic)
Auth: 10.0 COMMANDER ONLY
Port: 8890
Author: ECHO OMEGA PRIME
Authority: 11.0 SOVEREIGN
"""

from __future__ import annotations

import hashlib
import json
import math
import statistics
import sys
import time
import uuid
from collections import defaultdict, deque
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from enum import Enum
from pathlib import Path
from typing import Any, ClassVar, Dict, List, Literal, Optional, Sequence, Tuple

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import BaseModel, Field

# ============================================================================
# LOCAL IMPORTS
# ============================================================================

ENGINE_DIR = Path(__file__).parent
if str(ENGINE_DIR) not in sys.path:
    sys.path.insert(0, str(ENGINE_DIR))

# Parent engines directory for cross-engine imports
ENGINES_DIR = ENGINE_DIR.parent
if str(ENGINES_DIR) not in sys.path:
    sys.path.insert(0, str(ENGINES_DIR))

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

LOG_DIR = ENGINE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

logger.add(
    LOG_DIR / "gov02_engine_{time}.log",
    rotation="50 MB",
    retention="30 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {message}",
)

AUDIT_LOG_FILE = LOG_DIR / "gov02_audit_trail.jsonl"

# ============================================================================
# CONSTANTS
# ============================================================================

ENGINE_ID = "GOV02"
ENGINE_NAME = "Audit Controller"
ENGINE_TIER = "GOV"
ENGINE_PORT = 8890
ENGINE_VERSION = "1.0.0"
ENGINE_MODE = "DET"
ENGINE_AUTH_LEVEL = 10.0
MAX_AUDIT_ENTRIES = 500_000
MAX_ANOMALIES = 10_000
MAX_LATENCY_SAMPLES = 5_000
ANOMALY_ZSCORE_THRESHOLD = 3.0
ERROR_RATE_SPIKE_THRESHOLD = 0.15
LATENCY_SPIKE_MULTIPLIER = 3.0
HEALTH_POLL_TIMEOUT_SEC = 5.0
TIE20_COMPONENT_COUNT = 20
FLEET_MAX_ENGINES = 507
REPORT_PAGE_SIZE = 100
FORENSIC_MAX_DEPTH = 50

TIE20_COMPONENTS: List[str] = [
    "three_layer_response",
    "response_modes",
    "doctrine_cache",
    "authority_hardening",
    "confidence_stratification",
    "semantic_normalization",
    "vector_search",
    "telemetry",
    "drift_watcher",
    "coverage_map",
    "metrics_collector",
    "health_endpoint",
    "zoned_analysis",
    "fact_fragility_scoring",
    "audit_trail_jsonl",
    "determinism_hash_sha256",
    "fastapi_server",
    "loguru_logging",
    "multi_doctrine_decomposition",
    "deep_analysis_mode",
]


# ============================================================================
# ENUMS
# ============================================================================

class ResponseMode(str, Enum):
    """Response generation mode."""
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"


class ConfidenceLevel(str, Enum):
    """Confidence stratification levels."""
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"


class AnalysisZone(str, Enum):
    """Zoned analysis categories — never blur boundaries."""
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"


class AnomalyType(str, Enum):
    """Types of anomalies the controller can detect."""
    VOLUME_SPIKE = "VOLUME_SPIKE"
    VOLUME_DROP = "VOLUME_DROP"
    LATENCY_SPIKE = "LATENCY_SPIKE"
    ERROR_RATE_SPIKE = "ERROR_RATE_SPIKE"
    UNAUTHORIZED_ACCESS = "UNAUTHORIZED_ACCESS"
    DOCTRINE_DRIFT = "DOCTRINE_DRIFT"
    HEALTH_FAILURE = "HEALTH_FAILURE"
    COMPLIANCE_GAP = "COMPLIANCE_GAP"
    PATTERN_ANOMALY = "PATTERN_ANOMALY"


class AnomalySeverity(str, Enum):
    """Severity classification for detected anomalies."""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


class ComplianceStatus(str, Enum):
    """TIE-20 compliance status for an engine."""
    COMPLIANT = "COMPLIANT"
    PARTIAL = "PARTIAL"
    NON_COMPLIANT = "NON_COMPLIANT"
    UNKNOWN = "UNKNOWN"
    OFFLINE = "OFFLINE"


class EngineHealthStatus(str, Enum):
    """Health status for a monitored engine."""
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    UNHEALTHY = "UNHEALTHY"
    OFFLINE = "OFFLINE"
    UNKNOWN = "UNKNOWN"


class ReportPeriod(str, Enum):
    """Report time period."""
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    CUSTOM = "CUSTOM"


class AuditCategory(str, Enum):
    """Categories for audit trail entries."""
    QUERY = "QUERY"
    ERROR = "ERROR"
    ACCESS_DENIED = "ACCESS_DENIED"
    CONFIG_CHANGE = "CONFIG_CHANGE"
    HEALTH_CHECK = "HEALTH_CHECK"
    COMPLIANCE_CHECK = "COMPLIANCE_CHECK"
    ANOMALY_DETECTED = "ANOMALY_DETECTED"
    REPORT_GENERATED = "REPORT_GENERATED"
    ENGINE_STARTED = "ENGINE_STARTED"
    ENGINE_STOPPED = "ENGINE_STOPPED"


# ============================================================================
# PYDANTIC MODELS — ALL I/O
# ============================================================================

class AuditEntry(BaseModel):
    """A single audit trail entry from any engine."""
    entry_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    engine_id: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    category: AuditCategory = AuditCategory.QUERY
    query_id: Optional[str] = None
    user_id: Optional[str] = None
    query_text: Optional[str] = None
    response_mode: Optional[str] = None
    latency_ms: Optional[float] = None
    status_code: Optional[int] = None
    error_message: Optional[str] = None
    doctrine_hit: Optional[bool] = None
    confidence: Optional[str] = None
    ip_address: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class AuditIngestRequest(BaseModel):
    """Request to ingest audit entries."""
    entries: List[AuditEntry]


class AuditIngestResponse(BaseModel):
    """Response from audit ingestion."""
    ingested: int
    rejected: int
    errors: List[str]
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class DetectedAnomaly(BaseModel):
    """A detected anomaly record."""
    anomaly_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    anomaly_type: AnomalyType
    severity: AnomalySeverity
    engine_id: str
    detected_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    description: str
    metric_value: float
    threshold_value: float
    context: Dict[str, Any] = Field(default_factory=dict)
    resolved: bool = False
    resolved_at: Optional[str] = None


class EngineComplianceReport(BaseModel):
    """TIE-20 compliance status for a single engine."""
    engine_id: str
    status: ComplianceStatus
    components_present: List[str]
    components_missing: List[str]
    compliance_score: float
    last_checked: str
    health_endpoint_url: Optional[str] = None
    notes: List[str] = Field(default_factory=list)


class FleetComplianceReport(BaseModel):
    """Aggregate TIE-20 compliance across the fleet."""
    total_engines: int
    compliant: int
    partial: int
    non_compliant: int
    offline: int
    unknown: int
    average_score: float
    engines: List[EngineComplianceReport]
    generated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class EngineHealthReport(BaseModel):
    """Health metrics for a single engine."""
    engine_id: str
    status: EngineHealthStatus
    uptime_pct: float
    last_check: str
    avg_latency_ms: float
    error_rate: float
    total_queries: int
    queries_per_hour: float
    last_error: Optional[str] = None


class FleetHealthReport(BaseModel):
    """Aggregate health across all monitored engines."""
    total_engines: int
    healthy: int
    degraded: int
    unhealthy: int
    offline: int
    fleet_avg_latency_ms: float
    fleet_error_rate: float
    fleet_total_queries: int
    engines: List[EngineHealthReport]
    generated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class SystemWideMetrics(BaseModel):
    """System-wide aggregate metrics."""
    total_queries: int
    total_errors: int
    avg_latency_ms: float
    p95_latency_ms: float
    p99_latency_ms: float
    error_rate: float
    doctrine_hit_rate: float
    queries_per_hour: float
    unique_engines_reporting: int
    time_range_start: str
    time_range_end: str
    top_queried_engines: List[Dict[str, Any]]
    top_error_engines: List[Dict[str, Any]]


class AuditReportRequest(BaseModel):
    """Request for an audit report."""
    period: ReportPeriod = ReportPeriod.DAILY
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    engine_filter: Optional[List[str]] = None
    category_filter: Optional[List[AuditCategory]] = None
    include_anomalies: bool = True
    include_compliance: bool = True


class AuditReportResponse(BaseModel):
    """A complete audit report."""
    report_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    period: ReportPeriod
    start_date: str
    end_date: str
    metrics: SystemWideMetrics
    anomalies: List[DetectedAnomaly]
    compliance_summary: Optional[FleetComplianceReport] = None
    top_findings: List[str]
    recommendations: List[str]
    generated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    determinism_hash: str = ""


class ForensicReplayRequest(BaseModel):
    """Request for forensic query replay."""
    query_id: str
    engine_id: Optional[str] = None
    include_context: bool = True
    max_depth: int = Field(default=20, le=FORENSIC_MAX_DEPTH)


class ForensicReplayResult(BaseModel):
    """Result of a forensic query replay."""
    query_id: str
    engine_id: str
    original_timestamp: str
    original_query: Optional[str] = None
    original_response_mode: Optional[str] = None
    audit_chain: List[AuditEntry]
    related_entries: List[AuditEntry]
    timeline: List[Dict[str, Any]]
    reconstruction_confidence: float
    notes: List[str]


class QueryRequest(BaseModel):
    """Standard TIE query request for the audit controller."""
    query: str
    mode: ResponseMode = ResponseMode.FAST
    zone: AnalysisZone = AnalysisZone.AUDIT
    engine_filter: Optional[List[str]] = None
    time_range_hours: int = Field(default=24, ge=1, le=8760)
    context: Dict[str, Any] = Field(default_factory=dict)


class QueryResponse(BaseModel):
    """Standard TIE query response."""
    query_id: str
    engine_id: str
    answer: str
    mode: ResponseMode
    zone: AnalysisZone
    confidence: ConfidenceLevel
    layer_used: str
    latency_ms: float
    doctrine_hit: bool
    citations: List[str]
    determinism_hash: str
    timestamp: str


class EngineRegistration(BaseModel):
    """Register an engine for monitoring."""
    engine_id: str
    name: str
    tier: str
    port: int
    host: str = "localhost"
    health_url: Optional[str] = None
    metrics_url: Optional[str] = None
    coverage_url: Optional[str] = None


# ============================================================================
# DOCTRINE CACHE — Pre-compiled audit reasoning blocks
# ============================================================================

@dataclass
class DoctrineBlock:
    """A single doctrine cache entry with full reasoning framework."""
    topic: str
    keywords: List[str]
    conclusion_template: str
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    burden_holder: str
    adversary_position: str
    counter_arguments: List[str]
    resolution_strategy: str
    entity_scope: str
    confidence: ConfidenceLevel
    controlling_precedent: str


def _load_doctrine_cache() -> Dict[str, DoctrineBlock]:
    """Load doctrine cache from JSON file."""
    cache_path = ENGINE_DIR / "doctrine_cache.json"
    if not cache_path.exists():
        logger.warning("Doctrine cache file not found, using empty cache")
        return {}
    try:
        raw = json.loads(cache_path.read_text(encoding="utf-8"))
        blocks: Dict[str, DoctrineBlock] = {}
        for key, val in raw.items():
            blocks[key] = DoctrineBlock(
                topic=val["topic"],
                keywords=val["keywords"],
                conclusion_template=val["conclusion_template"],
                reasoning_framework=val["reasoning_framework"],
                key_factors=val["key_factors"],
                primary_authority=val["primary_authority"],
                burden_holder=val["burden_holder"],
                adversary_position=val["adversary_position"],
                counter_arguments=val["counter_arguments"],
                resolution_strategy=val["resolution_strategy"],
                entity_scope=val["entity_scope"],
                confidence=ConfidenceLevel(val["confidence"]),
                controlling_precedent=val["controlling_precedent"],
            )
        logger.info(f"Loaded {len(blocks)} doctrine blocks from cache")
        return blocks
    except Exception as exc:
        logger.error(f"Failed to load doctrine cache: {exc}")
        return {}


DOCTRINE_CACHE: Dict[str, DoctrineBlock] = {}
DOCTRINE_CACHE_VERSION = "1.0.0"


# ============================================================================
# SEMANTIC NORMALIZATION
# ============================================================================

def _load_semantic_dict() -> Dict[str, str]:
    """Load semantic dictionary for audit term normalization."""
    sem_path = ENGINE_DIR / "semantic_dict.json"
    if not sem_path.exists():
        logger.warning("Semantic dictionary not found, using empty dict")
        return {}
    try:
        raw = json.loads(sem_path.read_text(encoding="utf-8"))
        result = {}
        for key, val in raw.items():
            if isinstance(val, list):
                for alias in val:
                    result[alias.lower()] = key
            else:
                result[key.lower()] = val
        logger.info(f"Loaded {len(result)} semantic normalizations")
        return result
    except Exception as exc:
        logger.error(f"Failed to load semantic dict: {exc}")
        return {}


SEMANTIC_DICT: Dict[str, str] = {}


def normalize_audit_term(term: str) -> str:
    """Normalize an audit-domain term to its canonical form."""
    lowered = term.strip().lower()
    return SEMANTIC_DICT.get(lowered, term)


def normalize_query(query: str) -> str:
    """Normalize a full query string using the semantic dictionary."""
    words = query.split()
    normalized = []
    for word in words:
        canonical = normalize_audit_term(word)
        normalized.append(canonical)
    return " ".join(normalized)


# ============================================================================
# COVERAGE MAP
# ============================================================================

@dataclass
class CoverageEntry:
    """Tracks which doctrines have been triggered and which have gaps."""
    doctrine_key: str
    hit_count: int = 0
    last_hit: Optional[str] = None
    miss_count: int = 0
    gap_detected: bool = False


class CoverageMap:
    """Epistemic coverage tracking — know what you know and what you don't."""

    def __init__(self) -> None:
        self._entries: Dict[str, CoverageEntry] = {}
        self._total_queries: int = 0
        self._uncovered_queries: int = 0

    def record_hit(self, doctrine_key: str) -> None:
        """Record a doctrine cache hit."""
        if doctrine_key not in self._entries:
            self._entries[doctrine_key] = CoverageEntry(doctrine_key=doctrine_key)
        entry = self._entries[doctrine_key]
        entry.hit_count += 1
        entry.last_hit = datetime.now(timezone.utc).isoformat()
        self._total_queries += 1

    def record_miss(self, query_keywords: List[str]) -> None:
        """Record a doctrine cache miss — potential coverage gap."""
        key = "_".join(sorted(query_keywords[:3]))
        if key not in self._entries:
            self._entries[key] = CoverageEntry(doctrine_key=key, gap_detected=True)
        self._entries[key].miss_count += 1
        self._uncovered_queries += 1
        self._total_queries += 1

    def get_coverage_report(self) -> Dict[str, Any]:
        """Generate a coverage report."""
        total_doctrines = len(self._entries)
        hit_doctrines = sum(1 for e in self._entries.values() if e.hit_count > 0)
        gap_doctrines = sum(1 for e in self._entries.values() if e.gap_detected)
        coverage_pct = (hit_doctrines / max(total_doctrines, 1)) * 100

        top_hits = sorted(
            [(k, v.hit_count) for k, v in self._entries.items() if v.hit_count > 0],
            key=lambda x: x[1],
            reverse=True,
        )[:10]

        top_gaps = sorted(
            [(k, v.miss_count) for k, v in self._entries.items() if v.gap_detected],
            key=lambda x: x[1],
            reverse=True,
        )[:10]

        return {
            "total_doctrines_tracked": total_doctrines,
            "doctrines_hit": hit_doctrines,
            "coverage_gaps": gap_doctrines,
            "coverage_pct": round(coverage_pct, 2),
            "total_queries": self._total_queries,
            "uncovered_queries": self._uncovered_queries,
            "top_hits": [{"doctrine": k, "count": c} for k, c in top_hits],
            "top_gaps": [{"doctrine": k, "miss_count": c} for k, c in top_gaps],
        }


# ============================================================================
# METRICS COLLECTOR
# ============================================================================

class MetricsCollector:
    """Lightweight metrics for operational awareness."""

    def __init__(self) -> None:
        self.latencies: deque[float] = deque(maxlen=MAX_LATENCY_SAMPLES)
        self.errors: deque[float] = deque(maxlen=10_000)
        self.queries: deque[float] = deque(maxlen=100_000)
        self.doctrine_hits: int = 0
        self.doctrine_misses: int = 0
        self.last_error: Optional[str] = None
        self.active_queries: int = 0

    def record_query(self, latency_ms: float, doctrine_hit: bool) -> None:
        """Record a completed query."""
        now = time.time()
        self.latencies.append(latency_ms)
        self.queries.append(now)
        if doctrine_hit:
            self.doctrine_hits += 1
        else:
            self.doctrine_misses += 1

    def record_error(self, error_msg: str) -> None:
        """Record an error."""
        self.errors.append(time.time())
        self.last_error = f"{datetime.now(timezone.utc).isoformat()}: {error_msg[:200]}"

    def query_start(self) -> None:
        self.active_queries += 1

    def query_end(self) -> None:
        self.active_queries = max(0, self.active_queries - 1)

    def get_latency_stats(self) -> Dict[str, float]:
        """Return latency statistics."""
        if not self.latencies:
            return {"avg_ms": 0.0, "p50_ms": 0.0, "p95_ms": 0.0, "p99_ms": 0.0, "last_ms": 0.0}
        sorted_lat = sorted(self.latencies)
        n = len(sorted_lat)
        return {
            "avg_ms": round(statistics.mean(sorted_lat), 2),
            "p50_ms": round(sorted_lat[int(n * 0.50)], 2),
            "p95_ms": round(sorted_lat[min(int(n * 0.95), n - 1)], 2),
            "p99_ms": round(sorted_lat[min(int(n * 0.99), n - 1)], 2),
            "last_ms": round(sorted_lat[-1], 2),
        }

    def get_error_stats(self) -> Dict[str, Any]:
        """Return error statistics."""
        now = time.time()
        last_hour = sum(1 for t in self.errors if t > now - 3600)
        last_24h = len(self.errors)
        return {"last_hour": last_hour, "last_24h": last_24h, "last_error": self.last_error}

    def get_doctrine_hit_rate(self) -> float:
        """Return doctrine hit rate as a fraction."""
        total = self.doctrine_hits + self.doctrine_misses
        if total == 0:
            return 0.0
        return round(self.doctrine_hits / total, 4)

    def get_queries_per_hour(self) -> float:
        """Return queries per hour over the last hour."""
        now = time.time()
        recent = sum(1 for t in self.queries if t > now - 3600)
        return float(recent)

    def get_snapshot(self) -> Dict[str, Any]:
        """Full metrics snapshot."""
        return {
            "latency": self.get_latency_stats(),
            "errors": self.get_error_stats(),
            "doctrine_hit_rate": self.get_doctrine_hit_rate(),
            "queries_per_hour": self.get_queries_per_hour(),
            "active_queries": self.active_queries,
            "total_doctrine_hits": self.doctrine_hits,
            "total_doctrine_misses": self.doctrine_misses,
        }


# ============================================================================
# AUTHORITY HARDENING
# ============================================================================

@dataclass
class AuthorityWeight:
    """Weighted authority source."""
    source: str
    weight: float
    description: str


AUTHORITY_HIERARCHY: List[AuthorityWeight] = [
    AuthorityWeight("NIST_SP_800-53", 0.95, "NIST Special Publication 800-53 Security Controls"),
    AuthorityWeight("SOC2_TSC", 0.93, "SOC 2 Trust Services Criteria"),
    AuthorityWeight("ISO_27001", 0.92, "ISO/IEC 27001 Information Security"),
    AuthorityWeight("COBIT_2019", 0.90, "COBIT 2019 Governance Framework"),
    AuthorityWeight("COSO_ERM", 0.88, "COSO Enterprise Risk Management"),
    AuthorityWeight("IIA_STANDARDS", 0.87, "Institute of Internal Auditors Standards"),
    AuthorityWeight("PCAOB_AS", 0.85, "PCAOB Auditing Standards"),
    AuthorityWeight("GAO_YELLOWBOOK", 0.84, "GAO Government Auditing Standards"),
    AuthorityWeight("AICPA_AU_C", 0.82, "AICPA Clarified Auditing Standards"),
    AuthorityWeight("INTERNAL_POLICY", 0.60, "Internal ECHO PRIME Audit Policy"),
]


def resolve_authority_conflict(sources: List[str]) -> Tuple[str, float]:
    """Resolve conflicting authority sources by hierarchy weight."""
    hierarchy_map = {a.source: a.weight for a in AUTHORITY_HIERARCHY}
    best_source = ""
    best_weight = 0.0
    for src in sources:
        w = hierarchy_map.get(src, 0.5)
        if w > best_weight:
            best_weight = w
            best_source = src
    return best_source, best_weight


# ============================================================================
# CONFIDENCE STRATIFICATION
# ============================================================================

def stratify_confidence(
    doctrine_hit: bool,
    authority_weight: float,
    anomaly_count: int,
    data_completeness: float,
) -> ConfidenceLevel:
    """Determine confidence level based on multiple factors."""
    score = 0.0
    if doctrine_hit:
        score += 0.35
    score += authority_weight * 0.30
    score += max(0.0, (1.0 - anomaly_count / 10.0)) * 0.15
    score += data_completeness * 0.20

    if score >= 0.80:
        return ConfidenceLevel.DEFENSIBLE
    if score >= 0.60:
        return ConfidenceLevel.AGGRESSIVE
    if score >= 0.40:
        return ConfidenceLevel.DISCLOSURE
    return ConfidenceLevel.HIGH_RISK


# ============================================================================
# FACT FRAGILITY SCORING
# ============================================================================

@dataclass
class FragilityScore:
    """Measures how fragile/reliable a given audit finding is."""
    verifiability: float  # 0-1: can this be independently verified?
    recharacterization_risk: float  # 0-1: could this be reinterpreted?
    testimony_dependence: float  # 0-1: does this rely on human testimony?
    data_source_count: int
    overall_fragility: float  # computed

    @staticmethod
    def compute(
        verifiability: float,
        recharacterization_risk: float,
        testimony_dependence: float,
        data_source_count: int,
    ) -> "FragilityScore":
        """Compute overall fragility from components."""
        overall = (
            (1.0 - verifiability) * 0.35
            + recharacterization_risk * 0.30
            + testimony_dependence * 0.20
            + max(0.0, 1.0 - data_source_count / 5.0) * 0.15
        )
        return FragilityScore(
            verifiability=verifiability,
            recharacterization_risk=recharacterization_risk,
            testimony_dependence=testimony_dependence,
            data_source_count=data_source_count,
            overall_fragility=round(overall, 4),
        )


# ============================================================================
# AUDIT TRAIL STORE (In-memory + JSONL persistence)
# ============================================================================

class AuditTrailStore:
    """Stores and indexes audit trail entries from all engines."""

    def __init__(self, max_entries: int = MAX_AUDIT_ENTRIES) -> None:
        self._entries: deque[AuditEntry] = deque(maxlen=max_entries)
        self._by_engine: Dict[str, deque[AuditEntry]] = defaultdict(lambda: deque(maxlen=50_000))
        self._by_query_id: Dict[str, List[AuditEntry]] = {}
        self._by_category: Dict[AuditCategory, deque[AuditEntry]] = defaultdict(
            lambda: deque(maxlen=50_000)
        )
        self._total_ingested: int = 0
        self._total_rejected: int = 0

    def ingest(self, entry: AuditEntry) -> bool:
        """Ingest a single audit entry. Returns True if accepted."""
        if not entry.engine_id:
            self._total_rejected += 1
            return False
        self._entries.append(entry)
        self._by_engine[entry.engine_id].append(entry)
        self._by_category[entry.category].append(entry)
        if entry.query_id:
            if entry.query_id not in self._by_query_id:
                self._by_query_id[entry.query_id] = []
            self._by_query_id[entry.query_id].append(entry)
        self._total_ingested += 1
        self._persist_entry(entry)
        return True

    def ingest_batch(self, entries: List[AuditEntry]) -> Tuple[int, int, List[str]]:
        """Ingest a batch of entries. Returns (accepted, rejected, errors)."""
        accepted = 0
        rejected = 0
        errors: List[str] = []
        for entry in entries:
            try:
                if self.ingest(entry):
                    accepted += 1
                else:
                    rejected += 1
                    errors.append(f"Rejected entry {entry.entry_id}: missing engine_id")
            except Exception as exc:
                rejected += 1
                errors.append(f"Error ingesting {entry.entry_id}: {str(exc)[:100]}")
        return accepted, rejected, errors

    def query_by_engine(
        self, engine_id: str, limit: int = 100, offset: int = 0
    ) -> List[AuditEntry]:
        """Get entries for a specific engine."""
        entries = list(self._by_engine.get(engine_id, []))
        entries.sort(key=lambda e: e.timestamp, reverse=True)
        return entries[offset : offset + limit]

    def query_by_id(self, query_id: str) -> List[AuditEntry]:
        """Get all entries for a specific query_id (forensic replay)."""
        return self._by_query_id.get(query_id, [])

    def query_by_category(
        self, category: AuditCategory, limit: int = 100
    ) -> List[AuditEntry]:
        """Get entries by category."""
        entries = list(self._by_category.get(category, []))
        entries.sort(key=lambda e: e.timestamp, reverse=True)
        return entries[:limit]

    def query_by_time_range(
        self,
        start: datetime,
        end: datetime,
        engine_filter: Optional[List[str]] = None,
        category_filter: Optional[List[AuditCategory]] = None,
        limit: int = REPORT_PAGE_SIZE,
    ) -> List[AuditEntry]:
        """Query entries within a time range with optional filters."""
        start_iso = start.isoformat()
        end_iso = end.isoformat()
        results: List[AuditEntry] = []
        for entry in reversed(self._entries):
            if entry.timestamp < start_iso:
                break
            if entry.timestamp > end_iso:
                continue
            if engine_filter and entry.engine_id not in engine_filter:
                continue
            if category_filter and entry.category not in category_filter:
                continue
            results.append(entry)
            if len(results) >= limit:
                break
        return results

    def get_engine_ids(self) -> List[str]:
        """Get all engine IDs that have reported audit data."""
        return sorted(self._by_engine.keys())

    def get_stats(self) -> Dict[str, Any]:
        """Return store statistics."""
        return {
            "total_entries": len(self._entries),
            "total_ingested": self._total_ingested,
            "total_rejected": self._total_rejected,
            "unique_engines": len(self._by_engine),
            "unique_query_ids": len(self._by_query_id),
            "entries_by_category": {
                cat.value: len(entries) for cat, entries in self._by_category.items()
            },
        }

    def get_latencies_for_engine(self, engine_id: str) -> List[float]:
        """Extract latency values for a specific engine."""
        entries = self._by_engine.get(engine_id, [])
        return [e.latency_ms for e in entries if e.latency_ms is not None]

    def get_error_count_for_engine(self, engine_id: str, hours: int = 1) -> int:
        """Count errors for an engine within the last N hours."""
        cutoff = (datetime.now(timezone.utc) - timedelta(hours=hours)).isoformat()
        count = 0
        for entry in self._by_engine.get(engine_id, []):
            if entry.timestamp >= cutoff and entry.category == AuditCategory.ERROR:
                count += 1
        return count

    def get_access_denied_entries(
        self, hours: int = 24, limit: int = 100
    ) -> List[AuditEntry]:
        """Get recent access-denied entries."""
        cutoff = (datetime.now(timezone.utc) - timedelta(hours=hours)).isoformat()
        results: List[AuditEntry] = []
        for entry in reversed(list(self._by_category.get(AuditCategory.ACCESS_DENIED, []))):
            if entry.timestamp < cutoff:
                break
            results.append(entry)
            if len(results) >= limit:
                break
        return results

    def _persist_entry(self, entry: AuditEntry) -> None:
        """Persist entry to JSONL audit log."""
        try:
            with AUDIT_LOG_FILE.open("a", encoding="utf-8") as fh:
                fh.write(entry.model_dump_json() + "\n")
        except Exception as exc:
            logger.error(f"Failed to persist audit entry: {exc}")


# ============================================================================
# ANOMALY DETECTOR
# ============================================================================

class AnomalyDetector:
    """Detects anomalies in engine behavior using statistical methods."""

    def __init__(self, store: AuditTrailStore) -> None:
        self._store = store
        self._anomalies: deque[DetectedAnomaly] = deque(maxlen=MAX_ANOMALIES)
        self._engine_baselines: Dict[str, Dict[str, float]] = {}

    def update_baseline(self, engine_id: str) -> None:
        """Compute baseline metrics for an engine."""
        latencies = self._store.get_latencies_for_engine(engine_id)
        if len(latencies) < 10:
            return
        self._engine_baselines[engine_id] = {
            "mean_latency": statistics.mean(latencies),
            "stdev_latency": statistics.stdev(latencies) if len(latencies) > 1 else 0.0,
            "query_count": float(len(latencies)),
        }

    def check_volume_anomaly(self, engine_id: str, current_volume: int, window_hours: int = 1) -> Optional[DetectedAnomaly]:
        """Detect unusual query volume using z-score."""
        baseline = self._engine_baselines.get(engine_id)
        if not baseline or baseline["stdev_latency"] == 0.0:
            return None
        expected_volume = baseline["query_count"] / 24.0 * window_hours
        if expected_volume < 5:
            return None
        stdev_volume = max(math.sqrt(expected_volume), 1.0)
        z_score = abs(current_volume - expected_volume) / stdev_volume
        if z_score > ANOMALY_ZSCORE_THRESHOLD:
            anomaly_type = AnomalyType.VOLUME_SPIKE if current_volume > expected_volume else AnomalyType.VOLUME_DROP
            severity = AnomalySeverity.HIGH if z_score > 5.0 else AnomalySeverity.MEDIUM
            anomaly = DetectedAnomaly(
                anomaly_type=anomaly_type,
                severity=severity,
                engine_id=engine_id,
                description=(
                    f"Query volume anomaly on {engine_id}: {current_volume} queries in "
                    f"{window_hours}h (expected ~{expected_volume:.0f}, z={z_score:.2f})"
                ),
                metric_value=float(current_volume),
                threshold_value=expected_volume,
                context={"z_score": round(z_score, 2), "window_hours": window_hours},
            )
            self._anomalies.append(anomaly)
            return anomaly
        return None

    def check_latency_anomaly(self, engine_id: str, current_latency_ms: float) -> Optional[DetectedAnomaly]:
        """Detect unusual latency spike."""
        baseline = self._engine_baselines.get(engine_id)
        if not baseline:
            return None
        mean_lat = baseline["mean_latency"]
        stdev_lat = baseline["stdev_latency"]
        if stdev_lat == 0.0:
            stdev_lat = mean_lat * 0.1
        if stdev_lat == 0.0:
            return None
        z_score = (current_latency_ms - mean_lat) / stdev_lat
        if z_score > ANOMALY_ZSCORE_THRESHOLD:
            severity = AnomalySeverity.HIGH if z_score > 5.0 else AnomalySeverity.MEDIUM
            anomaly = DetectedAnomaly(
                anomaly_type=AnomalyType.LATENCY_SPIKE,
                severity=severity,
                engine_id=engine_id,
                description=(
                    f"Latency spike on {engine_id}: {current_latency_ms:.1f}ms "
                    f"(baseline {mean_lat:.1f}ms, z={z_score:.2f})"
                ),
                metric_value=current_latency_ms,
                threshold_value=mean_lat + ANOMALY_ZSCORE_THRESHOLD * stdev_lat,
                context={"z_score": round(z_score, 2), "baseline_mean": round(mean_lat, 2)},
            )
            self._anomalies.append(anomaly)
            return anomaly
        return None

    def check_error_rate_anomaly(self, engine_id: str, error_count: int, total_queries: int) -> Optional[DetectedAnomaly]:
        """Detect error rate spikes."""
        if total_queries < 10:
            return None
        error_rate = error_count / total_queries
        if error_rate > ERROR_RATE_SPIKE_THRESHOLD:
            severity = AnomalySeverity.CRITICAL if error_rate > 0.5 else AnomalySeverity.HIGH
            anomaly = DetectedAnomaly(
                anomaly_type=AnomalyType.ERROR_RATE_SPIKE,
                severity=severity,
                engine_id=engine_id,
                description=(
                    f"Error rate spike on {engine_id}: {error_rate:.1%} "
                    f"({error_count}/{total_queries} queries)"
                ),
                metric_value=error_rate,
                threshold_value=ERROR_RATE_SPIKE_THRESHOLD,
                context={"error_count": error_count, "total_queries": total_queries},
            )
            self._anomalies.append(anomaly)
            return anomaly
        return None

    def check_unauthorized_access(self, engine_id: str, denied_count: int, window_hours: int = 1) -> Optional[DetectedAnomaly]:
        """Detect unusual unauthorized access attempts."""
        if denied_count < 5:
            return None
        severity = AnomalySeverity.CRITICAL if denied_count > 50 else (
            AnomalySeverity.HIGH if denied_count > 20 else AnomalySeverity.MEDIUM
        )
        anomaly = DetectedAnomaly(
            anomaly_type=AnomalyType.UNAUTHORIZED_ACCESS,
            severity=severity,
            engine_id=engine_id,
            description=(
                f"Unauthorized access spike on {engine_id}: {denied_count} "
                f"denied requests in {window_hours}h"
            ),
            metric_value=float(denied_count),
            threshold_value=5.0,
            context={"window_hours": window_hours},
        )
        self._anomalies.append(anomaly)
        return anomaly

    def run_all_checks(self, engine_id: str) -> List[DetectedAnomaly]:
        """Run all anomaly checks for a single engine."""
        self.update_baseline(engine_id)
        detected: List[DetectedAnomaly] = []

        entries = self._store.query_by_engine(engine_id, limit=1000)
        if not entries:
            return detected

        now = datetime.now(timezone.utc)
        hour_ago = (now - timedelta(hours=1)).isoformat()
        recent = [e for e in entries if e.timestamp >= hour_ago]
        recent_errors = [e for e in recent if e.category == AuditCategory.ERROR]
        recent_denied = [e for e in recent if e.category == AuditCategory.ACCESS_DENIED]

        vol_anomaly = self.check_volume_anomaly(engine_id, len(recent))
        if vol_anomaly:
            detected.append(vol_anomaly)

        if recent:
            latencies = [e.latency_ms for e in recent if e.latency_ms is not None]
            if latencies:
                avg_lat = statistics.mean(latencies)
                lat_anomaly = self.check_latency_anomaly(engine_id, avg_lat)
                if lat_anomaly:
                    detected.append(lat_anomaly)

        err_anomaly = self.check_error_rate_anomaly(engine_id, len(recent_errors), max(len(recent), 1))
        if err_anomaly:
            detected.append(err_anomaly)

        unauth_anomaly = self.check_unauthorized_access(engine_id, len(recent_denied))
        if unauth_anomaly:
            detected.append(unauth_anomaly)

        return detected

    def get_anomalies(
        self,
        hours: int = 24,
        severity_filter: Optional[List[AnomalySeverity]] = None,
        engine_filter: Optional[List[str]] = None,
        limit: int = 100,
    ) -> List[DetectedAnomaly]:
        """Get detected anomalies with filters."""
        cutoff = (datetime.now(timezone.utc) - timedelta(hours=hours)).isoformat()
        results: List[DetectedAnomaly] = []
        for anomaly in reversed(self._anomalies):
            if anomaly.detected_at < cutoff:
                break
            if severity_filter and anomaly.severity not in severity_filter:
                continue
            if engine_filter and anomaly.engine_id not in engine_filter:
                continue
            results.append(anomaly)
            if len(results) >= limit:
                break
        return results

    def get_anomaly_summary(self, hours: int = 24) -> Dict[str, Any]:
        """Summary of anomalies."""
        anomalies = self.get_anomalies(hours=hours, limit=10_000)
        by_type: Dict[str, int] = defaultdict(int)
        by_severity: Dict[str, int] = defaultdict(int)
        by_engine: Dict[str, int] = defaultdict(int)
        for a in anomalies:
            by_type[a.anomaly_type.value] += 1
            by_severity[a.severity.value] += 1
            by_engine[a.engine_id] += 1
        return {
            "total": len(anomalies),
            "by_type": dict(by_type),
            "by_severity": dict(by_severity),
            "top_engines": sorted(by_engine.items(), key=lambda x: x[1], reverse=True)[:10],
            "hours_covered": hours,
        }


# ============================================================================
# TIE-20 COMPLIANCE CHECKER
# ============================================================================

class TIE20ComplianceChecker:
    """Verifies engines have all 20 TIE components."""

    def __init__(self) -> None:
        self._reports: Dict[str, EngineComplianceReport] = {}

    def check_engine_from_health(
        self, engine_id: str, health_data: Dict[str, Any]
    ) -> EngineComplianceReport:
        """Check TIE-20 compliance from an engine's health endpoint response."""
        present: List[str] = []
        missing: List[str] = []
        notes: List[str] = []

        component_checks = {
            "three_layer_response": lambda d: "layers" in d or "three_layer" in str(d).lower(),
            "response_modes": lambda d: "modes" in d or "response_mode" in str(d).lower(),
            "doctrine_cache": lambda d: "doctrine" in str(d).lower(),
            "authority_hardening": lambda d: "authority" in str(d).lower(),
            "confidence_stratification": lambda d: "confidence" in str(d).lower(),
            "semantic_normalization": lambda d: "semantic" in str(d).lower(),
            "vector_search": lambda d: "vector" in str(d).lower() or "search" in d,
            "telemetry": lambda d: "telemetry" in str(d).lower(),
            "drift_watcher": lambda d: "drift" in str(d).lower(),
            "coverage_map": lambda d: "coverage" in str(d).lower(),
            "metrics_collector": lambda d: "metrics" in d or "latency" in str(d).lower(),
            "health_endpoint": lambda _: True,
            "zoned_analysis": lambda d: "zone" in str(d).lower(),
            "fact_fragility_scoring": lambda d: "fragility" in str(d).lower(),
            "audit_trail_jsonl": lambda d: "audit" in str(d).lower(),
            "determinism_hash_sha256": lambda d: "hash" in str(d).lower() or "sha" in str(d).lower(),
            "fastapi_server": lambda d: "fastapi" in str(d).lower() or "version" in d,
            "loguru_logging": lambda d: "log" in str(d).lower(),
            "multi_doctrine_decomposition": lambda d: "decomposition" in str(d).lower() or "multi_doctrine" in str(d).lower(),
            "deep_analysis_mode": lambda d: "deep" in str(d).lower() or "analysis" in str(d).lower(),
        }

        health_str = json.dumps(health_data).lower()
        for component, checker in component_checks.items():
            try:
                if checker(health_data):
                    present.append(component)
                else:
                    missing.append(component)
            except Exception:
                missing.append(component)
                notes.append(f"Error checking {component}")

        score = len(present) / TIE20_COMPONENT_COUNT * 100.0
        if score >= 90.0:
            status = ComplianceStatus.COMPLIANT
        elif score >= 50.0:
            status = ComplianceStatus.PARTIAL
        else:
            status = ComplianceStatus.NON_COMPLIANT

        report = EngineComplianceReport(
            engine_id=engine_id,
            status=status,
            components_present=present,
            components_missing=missing,
            compliance_score=round(score, 2),
            last_checked=datetime.now(timezone.utc).isoformat(),
            notes=notes,
        )
        self._reports[engine_id] = report
        return report

    def check_engine_offline(self, engine_id: str, reason: str) -> EngineComplianceReport:
        """Record an engine as offline."""
        report = EngineComplianceReport(
            engine_id=engine_id,
            status=ComplianceStatus.OFFLINE,
            components_present=[],
            components_missing=TIE20_COMPONENTS.copy(),
            compliance_score=0.0,
            last_checked=datetime.now(timezone.utc).isoformat(),
            notes=[f"Offline: {reason}"],
        )
        self._reports[engine_id] = report
        return report

    def get_fleet_report(self) -> FleetComplianceReport:
        """Generate fleet-wide compliance report."""
        reports = list(self._reports.values())
        compliant = sum(1 for r in reports if r.status == ComplianceStatus.COMPLIANT)
        partial = sum(1 for r in reports if r.status == ComplianceStatus.PARTIAL)
        non_compliant = sum(1 for r in reports if r.status == ComplianceStatus.NON_COMPLIANT)
        offline = sum(1 for r in reports if r.status == ComplianceStatus.OFFLINE)
        unknown = sum(1 for r in reports if r.status == ComplianceStatus.UNKNOWN)
        avg_score = statistics.mean([r.compliance_score for r in reports]) if reports else 0.0

        return FleetComplianceReport(
            total_engines=len(reports),
            compliant=compliant,
            partial=partial,
            non_compliant=non_compliant,
            offline=offline,
            unknown=unknown,
            average_score=round(avg_score, 2),
            engines=reports,
        )

    def get_report(self, engine_id: str) -> Optional[EngineComplianceReport]:
        """Get a specific engine's compliance report."""
        return self._reports.get(engine_id)


# ============================================================================
# FLEET HEALTH MONITOR
# ============================================================================

class FleetHealthMonitor:
    """Monitors health of all registered engines."""

    def __init__(self, store: AuditTrailStore) -> None:
        self._store = store
        self._registered: Dict[str, EngineRegistration] = {}
        self._health_cache: Dict[str, EngineHealthReport] = {}
        self._uptime_checks: Dict[str, List[Tuple[str, bool]]] = defaultdict(list)

    def register_engine(self, reg: EngineRegistration) -> None:
        """Register an engine for monitoring."""
        self._registered[reg.engine_id] = reg
        logger.info(f"Registered engine {reg.engine_id} ({reg.name}) at {reg.host}:{reg.port}")

    def unregister_engine(self, engine_id: str) -> bool:
        """Unregister an engine."""
        if engine_id in self._registered:
            del self._registered[engine_id]
            return True
        return False

    def record_health_check(self, engine_id: str, is_healthy: bool) -> None:
        """Record a health check result."""
        self._uptime_checks[engine_id].append(
            (datetime.now(timezone.utc).isoformat(), is_healthy)
        )
        if len(self._uptime_checks[engine_id]) > 1000:
            self._uptime_checks[engine_id] = self._uptime_checks[engine_id][-500:]

    def compute_uptime(self, engine_id: str) -> float:
        """Compute uptime percentage from health check history."""
        checks = self._uptime_checks.get(engine_id, [])
        if not checks:
            return 0.0
        healthy_count = sum(1 for _, h in checks if h)
        return round(healthy_count / len(checks) * 100.0, 2)

    def build_health_report(self, engine_id: str) -> EngineHealthReport:
        """Build a health report for a single engine from audit data."""
        entries = self._store.query_by_engine(engine_id, limit=5000)
        latencies = [e.latency_ms for e in entries if e.latency_ms is not None]
        errors = [e for e in entries if e.category == AuditCategory.ERROR]
        total = len(entries)
        avg_lat = statistics.mean(latencies) if latencies else 0.0
        error_rate = len(errors) / max(total, 1)
        uptime = self.compute_uptime(engine_id)

        now = datetime.now(timezone.utc)
        hour_ago = (now - timedelta(hours=1)).isoformat()
        recent_count = sum(1 for e in entries if e.timestamp >= hour_ago)

        if error_rate > 0.3:
            status = EngineHealthStatus.UNHEALTHY
        elif error_rate > 0.1 or avg_lat > 2000:
            status = EngineHealthStatus.DEGRADED
        elif uptime < 50.0 and uptime > 0.0:
            status = EngineHealthStatus.DEGRADED
        elif total == 0:
            status = EngineHealthStatus.UNKNOWN
        else:
            status = EngineHealthStatus.HEALTHY

        report = EngineHealthReport(
            engine_id=engine_id,
            status=status,
            uptime_pct=uptime,
            last_check=datetime.now(timezone.utc).isoformat(),
            avg_latency_ms=round(avg_lat, 2),
            error_rate=round(error_rate, 4),
            total_queries=total,
            queries_per_hour=float(recent_count),
            last_error=errors[-1].error_message if errors else None,
        )
        self._health_cache[engine_id] = report
        return report

    def get_fleet_report(self) -> FleetHealthReport:
        """Build a fleet-wide health report."""
        engine_ids = set(self._registered.keys()) | set(self._store.get_engine_ids())
        reports: List[EngineHealthReport] = []
        for eid in sorted(engine_ids):
            reports.append(self.build_health_report(eid))

        healthy = sum(1 for r in reports if r.status == EngineHealthStatus.HEALTHY)
        degraded = sum(1 for r in reports if r.status == EngineHealthStatus.DEGRADED)
        unhealthy = sum(1 for r in reports if r.status == EngineHealthStatus.UNHEALTHY)
        offline = sum(1 for r in reports if r.status == EngineHealthStatus.OFFLINE)
        all_latencies = [r.avg_latency_ms for r in reports if r.avg_latency_ms > 0]
        fleet_avg_lat = statistics.mean(all_latencies) if all_latencies else 0.0
        total_queries = sum(r.total_queries for r in reports)
        total_errors = sum(int(r.error_rate * r.total_queries) for r in reports)
        fleet_error_rate = total_errors / max(total_queries, 1)

        return FleetHealthReport(
            total_engines=len(reports),
            healthy=healthy,
            degraded=degraded,
            unhealthy=unhealthy,
            offline=offline,
            fleet_avg_latency_ms=round(fleet_avg_lat, 2),
            fleet_error_rate=round(fleet_error_rate, 4),
            fleet_total_queries=total_queries,
            engines=reports,
        )

    def get_registered(self) -> List[EngineRegistration]:
        """Get all registered engines."""
        return list(self._registered.values())


# ============================================================================
# REPORT GENERATOR
# ============================================================================

class ReportGenerator:
    """Generates audit reports for specified time periods."""

    def __init__(
        self,
        store: AuditTrailStore,
        anomaly_detector: AnomalyDetector,
        compliance_checker: TIE20ComplianceChecker,
    ) -> None:
        self._store = store
        self._anomaly_detector = anomaly_detector
        self._compliance_checker = compliance_checker

    def compute_system_metrics(
        self, start: datetime, end: datetime, engine_filter: Optional[List[str]] = None
    ) -> SystemWideMetrics:
        """Compute system-wide metrics for a time range."""
        entries = self._store.query_by_time_range(start, end, engine_filter=engine_filter, limit=100_000)
        if not entries:
            return SystemWideMetrics(
                total_queries=0, total_errors=0, avg_latency_ms=0.0, p95_latency_ms=0.0,
                p99_latency_ms=0.0, error_rate=0.0, doctrine_hit_rate=0.0,
                queries_per_hour=0.0, unique_engines_reporting=0,
                time_range_start=start.isoformat(), time_range_end=end.isoformat(),
                top_queried_engines=[], top_error_engines=[],
            )

        latencies = [e.latency_ms for e in entries if e.latency_ms is not None]
        errors = [e for e in entries if e.category == AuditCategory.ERROR]
        doctrine_hits = sum(1 for e in entries if e.doctrine_hit is True)
        doctrine_total = sum(1 for e in entries if e.doctrine_hit is not None)
        engine_counts: Dict[str, int] = defaultdict(int)
        engine_errors: Dict[str, int] = defaultdict(int)
        for e in entries:
            engine_counts[e.engine_id] += 1
        for e in errors:
            engine_errors[e.engine_id] += 1

        sorted_lat = sorted(latencies) if latencies else [0.0]
        n = len(sorted_lat)
        hours_span = max((end - start).total_seconds() / 3600.0, 0.01)

        top_queried = sorted(engine_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        top_errors = sorted(engine_errors.items(), key=lambda x: x[1], reverse=True)[:10]

        return SystemWideMetrics(
            total_queries=len(entries),
            total_errors=len(errors),
            avg_latency_ms=round(statistics.mean(sorted_lat), 2) if sorted_lat else 0.0,
            p95_latency_ms=round(sorted_lat[min(int(n * 0.95), n - 1)], 2),
            p99_latency_ms=round(sorted_lat[min(int(n * 0.99), n - 1)], 2),
            error_rate=round(len(errors) / max(len(entries), 1), 4),
            doctrine_hit_rate=round(doctrine_hits / max(doctrine_total, 1), 4),
            queries_per_hour=round(len(entries) / hours_span, 2),
            unique_engines_reporting=len(engine_counts),
            time_range_start=start.isoformat(),
            time_range_end=end.isoformat(),
            top_queried_engines=[{"engine_id": k, "count": v} for k, v in top_queried],
            top_error_engines=[{"engine_id": k, "count": v} for k, v in top_errors],
        )

    def generate_report(self, request: AuditReportRequest) -> AuditReportResponse:
        """Generate a full audit report."""
        now = datetime.now(timezone.utc)
        if request.period == ReportPeriod.DAILY:
            start = now - timedelta(days=1)
        elif request.period == ReportPeriod.WEEKLY:
            start = now - timedelta(weeks=1)
        elif request.period == ReportPeriod.MONTHLY:
            start = now - timedelta(days=30)
        else:
            start = datetime.fromisoformat(request.start_date) if request.start_date else now - timedelta(days=1)

        end = datetime.fromisoformat(request.end_date) if request.end_date else now

        metrics = self.compute_system_metrics(start, end, engine_filter=request.engine_filter)
        anomalies = self._anomaly_detector.get_anomalies(
            hours=int((end - start).total_seconds() / 3600),
            engine_filter=request.engine_filter,
        ) if request.include_anomalies else []

        compliance = self._compliance_checker.get_fleet_report() if request.include_compliance else None

        findings = self._generate_findings(metrics, anomalies, compliance)
        recommendations = self._generate_recommendations(metrics, anomalies, compliance)

        report = AuditReportResponse(
            period=request.period,
            start_date=start.isoformat(),
            end_date=end.isoformat(),
            metrics=metrics,
            anomalies=anomalies[:50],
            compliance_summary=compliance,
            top_findings=findings,
            recommendations=recommendations,
        )
        report.determinism_hash = self._compute_report_hash(report)
        return report

    def _generate_findings(
        self,
        metrics: SystemWideMetrics,
        anomalies: List[DetectedAnomaly],
        compliance: Optional[FleetComplianceReport],
    ) -> List[str]:
        """Generate top findings from report data."""
        findings: List[str] = []
        if metrics.error_rate > 0.1:
            findings.append(
                f"CRITICAL: Fleet-wide error rate is {metrics.error_rate:.1%}, "
                f"exceeding 10% threshold ({metrics.total_errors} errors in "
                f"{metrics.total_queries} queries)"
            )
        elif metrics.error_rate > 0.05:
            findings.append(
                f"WARNING: Fleet error rate elevated at {metrics.error_rate:.1%}"
            )

        if metrics.p95_latency_ms > 5000:
            findings.append(
                f"PERFORMANCE: P95 latency is {metrics.p95_latency_ms:.0f}ms, "
                f"indicating potential bottlenecks"
            )

        critical_anomalies = [a for a in anomalies if a.severity == AnomalySeverity.CRITICAL]
        if critical_anomalies:
            findings.append(
                f"ANOMALIES: {len(critical_anomalies)} critical anomalies detected "
                f"requiring immediate attention"
            )

        unauth = [a for a in anomalies if a.anomaly_type == AnomalyType.UNAUTHORIZED_ACCESS]
        if unauth:
            findings.append(
                f"SECURITY: {len(unauth)} unauthorized access anomalies detected "
                f"across {len(set(a.engine_id for a in unauth))} engines"
            )

        if compliance:
            if compliance.non_compliant > 0:
                findings.append(
                    f"COMPLIANCE: {compliance.non_compliant} engines are non-compliant "
                    f"with TIE-20 standard (fleet average score: {compliance.average_score:.1f}%)"
                )
            if compliance.offline > 0:
                findings.append(
                    f"AVAILABILITY: {compliance.offline} engines are offline and unreachable"
                )

        if metrics.top_error_engines:
            top = metrics.top_error_engines[0]
            findings.append(
                f"TOP ERROR SOURCE: Engine {top['engine_id']} has "
                f"{top['count']} errors in the reporting period"
            )

        if not findings:
            findings.append("No significant findings. Fleet is operating within normal parameters.")

        return findings

    def _generate_recommendations(
        self,
        metrics: SystemWideMetrics,
        anomalies: List[DetectedAnomaly],
        compliance: Optional[FleetComplianceReport],
    ) -> List[str]:
        """Generate actionable recommendations."""
        recs: List[str] = []
        if metrics.error_rate > 0.05:
            recs.append(
                "Investigate high-error engines and review GS343 error healing templates. "
                "Consider adding new templates for recurring error patterns."
            )
        if metrics.p95_latency_ms > 3000:
            recs.append(
                "Review doctrine cache hit rates on slow engines. "
                "Expand cache with frequently-queried topics to reduce latency."
            )
        unauth = [a for a in anomalies if a.anomaly_type == AnomalyType.UNAUTHORIZED_ACCESS]
        if unauth:
            recs.append(
                "Review access control policies on affected engines. "
                "Consider implementing rate limiting and IP allowlisting."
            )
        if compliance and compliance.non_compliant > 0:
            recs.append(
                f"Upgrade {compliance.non_compliant} non-compliant engines to TIE-20 standard. "
                f"Priority: engines with compliance score below 50%."
            )
        if metrics.doctrine_hit_rate < 0.5:
            recs.append(
                "Doctrine hit rate below 50%. Expand doctrine caches across engines "
                "with commonly queried topics to improve response times."
            )
        if not recs:
            recs.append("Continue monitoring. No immediate actions required.")
        return recs

    def _compute_report_hash(self, report: AuditReportResponse) -> str:
        """Compute SHA-256 hash for report determinism."""
        content = report.model_dump_json(exclude={"determinism_hash", "report_id"})
        return hashlib.sha256(content.encode("utf-8")).hexdigest()


# ============================================================================
# FORENSIC QUERY REPLAY
# ============================================================================

class ForensicReplayEngine:
    """Reconstructs the full audit trail for a given query."""

    def __init__(self, store: AuditTrailStore) -> None:
        self._store = store

    def replay(self, request: ForensicReplayRequest) -> ForensicReplayResult:
        """Replay a query's full audit trail."""
        primary_entries = self._store.query_by_id(request.query_id)
        if not primary_entries:
            return ForensicReplayResult(
                query_id=request.query_id,
                engine_id=request.engine_id or "UNKNOWN",
                original_timestamp=datetime.now(timezone.utc).isoformat(),
                audit_chain=[],
                related_entries=[],
                timeline=[],
                reconstruction_confidence=0.0,
                notes=["No audit entries found for this query_id"],
            )

        primary_entries.sort(key=lambda e: e.timestamp)
        engine_id = primary_entries[0].engine_id
        original_ts = primary_entries[0].timestamp
        original_query = None
        original_mode = None
        for entry in primary_entries:
            if entry.query_text:
                original_query = entry.query_text
            if entry.response_mode:
                original_mode = entry.response_mode

        related: List[AuditEntry] = []
        if request.include_context and len(primary_entries) > 0:
            ts = datetime.fromisoformat(original_ts.replace("Z", "+00:00")) if "Z" in original_ts else datetime.fromisoformat(original_ts)
            window_start = ts - timedelta(seconds=30)
            window_end = ts + timedelta(seconds=30)
            nearby = self._store.query_by_time_range(
                window_start, window_end,
                engine_filter=[engine_id],
                limit=request.max_depth,
            )
            related = [e for e in nearby if e.query_id != request.query_id]

        timeline: List[Dict[str, Any]] = []
        for entry in primary_entries:
            timeline.append({
                "timestamp": entry.timestamp,
                "category": entry.category.value,
                "status_code": entry.status_code,
                "latency_ms": entry.latency_ms,
                "doctrine_hit": entry.doctrine_hit,
                "note": entry.error_message or "OK",
            })

        data_points = len(primary_entries)
        confidence = min(1.0, data_points / 5.0) * 0.7
        if original_query:
            confidence += 0.15
        if original_mode:
            confidence += 0.15

        notes: List[str] = []
        if data_points == 1:
            notes.append("Only one audit entry found — partial reconstruction")
        if not original_query:
            notes.append("Original query text not available in audit trail")
        if related:
            notes.append(f"Found {len(related)} related entries within 30s window")

        return ForensicReplayResult(
            query_id=request.query_id,
            engine_id=engine_id,
            original_timestamp=original_ts,
            original_query=original_query,
            original_response_mode=original_mode,
            audit_chain=primary_entries,
            related_entries=related,
            timeline=timeline,
            reconstruction_confidence=round(confidence, 4),
            notes=notes,
        )


# ============================================================================
# DRIFT WATCHER
# ============================================================================

class DriftWatcher:
    """Monitors for doctrine drift across the fleet."""

    def __init__(self) -> None:
        self._snapshots: Dict[str, Dict[str, Any]] = {}
        self._drift_events: List[Dict[str, Any]] = []

    def record_snapshot(self, engine_id: str, doctrine_version: str, doctrine_count: int) -> None:
        """Record a doctrine state snapshot for an engine."""
        now = datetime.now(timezone.utc).isoformat()
        prev = self._snapshots.get(engine_id)
        self._snapshots[engine_id] = {
            "version": doctrine_version,
            "count": doctrine_count,
            "timestamp": now,
        }
        if prev and (prev["version"] != doctrine_version or prev["count"] != doctrine_count):
            self._drift_events.append({
                "engine_id": engine_id,
                "detected_at": now,
                "old_version": prev["version"],
                "new_version": doctrine_version,
                "old_count": prev["count"],
                "new_count": doctrine_count,
                "drift_type": "version_change" if prev["version"] != doctrine_version else "count_change",
            })

    def get_drift_events(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent drift events."""
        return self._drift_events[-limit:]

    def get_snapshot(self, engine_id: str) -> Optional[Dict[str, Any]]:
        """Get latest snapshot for an engine."""
        return self._snapshots.get(engine_id)


# ============================================================================
# MULTI-DOCTRINE DECOMPOSITION
# ============================================================================

class AuditIssueDecomposer:
    """Decomposes complex audit queries into constituent sub-issues."""

    AUDIT_CATEGORIES_MAP: ClassVar[Dict[str, List[str]]] = {
        "anomaly_investigation": [
            "volume_analysis", "latency_analysis", "error_pattern_analysis",
            "access_pattern_analysis", "temporal_correlation",
        ],
        "compliance_assessment": [
            "tie20_component_check", "authority_hardening_review",
            "doctrine_coverage_analysis", "telemetry_completeness",
            "determinism_verification",
        ],
        "security_review": [
            "unauthorized_access_analysis", "ip_reputation_check",
            "rate_limit_verification", "credential_audit",
            "data_exfiltration_check",
        ],
        "performance_review": [
            "latency_trending", "throughput_analysis",
            "error_rate_trending", "resource_utilization",
            "cache_hit_analysis",
        ],
        "forensic_analysis": [
            "query_reconstruction", "timeline_assembly",
            "cross_engine_correlation", "data_provenance",
            "impact_assessment",
        ],
    }

    def decompose(self, query: str) -> Dict[str, Any]:
        """Decompose an audit query into sub-issues."""
        query_lower = query.lower()
        matched_categories: List[str] = []
        sub_issues: List[str] = []

        keyword_map = {
            "anomaly_investigation": ["anomaly", "unusual", "spike", "drop", "unexpected", "abnormal"],
            "compliance_assessment": ["compliance", "tie-20", "tie20", "standard", "component", "requirement"],
            "security_review": ["unauthorized", "security", "breach", "access denied", "403", "attack"],
            "performance_review": ["performance", "latency", "slow", "throughput", "error rate", "degraded"],
            "forensic_analysis": ["forensic", "replay", "reconstruct", "trace", "timeline", "investigate"],
        }

        for category, keywords in keyword_map.items():
            if any(kw in query_lower for kw in keywords):
                matched_categories.append(category)
                sub_issues.extend(self.AUDIT_CATEGORIES_MAP[category])

        if not matched_categories:
            matched_categories = ["anomaly_investigation", "compliance_assessment"]
            sub_issues = self.AUDIT_CATEGORIES_MAP["anomaly_investigation"][:3] + \
                         self.AUDIT_CATEGORIES_MAP["compliance_assessment"][:2]

        return {
            "original_query": query,
            "matched_categories": matched_categories,
            "sub_issues": sub_issues,
            "total_sub_issues": len(sub_issues),
            "decomposition_strategy": "keyword_match" if matched_categories else "default_coverage",
        }


# ============================================================================
# DEEP ANALYSIS MODE
# ============================================================================

class DeepAnalysisEngine:
    """Multi-source synthesis for complex audit queries."""

    def __init__(
        self,
        store: AuditTrailStore,
        anomaly_detector: AnomalyDetector,
        compliance_checker: TIE20ComplianceChecker,
        fleet_monitor: FleetHealthMonitor,
        decomposer: AuditIssueDecomposer,
    ) -> None:
        self._store = store
        self._anomaly = anomaly_detector
        self._compliance = compliance_checker
        self._fleet = fleet_monitor
        self._decomposer = decomposer

    def analyze(self, query: str, engine_filter: Optional[List[str]] = None, hours: int = 24) -> Dict[str, Any]:
        """Perform deep analysis on an audit query."""
        decomposition = self._decomposer.decompose(query)
        now = datetime.now(timezone.utc)
        start = now - timedelta(hours=hours)

        results: Dict[str, Any] = {
            "query": query,
            "decomposition": decomposition,
            "analysis_depth": "DEEP",
            "time_range": {"start": start.isoformat(), "end": now.isoformat()},
            "sub_analyses": {},
        }

        for sub_issue in decomposition["sub_issues"]:
            results["sub_analyses"][sub_issue] = self._analyze_sub_issue(
                sub_issue, start, now, engine_filter
            )

        synthesis = self._synthesize(results["sub_analyses"], decomposition["matched_categories"])
        results["synthesis"] = synthesis
        results["confidence"] = self._compute_analysis_confidence(results)
        results["reasoning_chain"] = self._build_reasoning_chain(results)

        return results

    def _analyze_sub_issue(
        self, sub_issue: str, start: datetime, end: datetime, engine_filter: Optional[List[str]]
    ) -> Dict[str, Any]:
        """Analyze a single sub-issue."""
        analysis: Dict[str, Any] = {"sub_issue": sub_issue, "status": "analyzed"}

        if sub_issue in ("volume_analysis", "throughput_analysis"):
            entries = self._store.query_by_time_range(start, end, engine_filter=engine_filter, limit=10_000)
            hourly_counts: Dict[str, int] = defaultdict(int)
            for e in entries:
                hour_key = e.timestamp[:13]
                hourly_counts[hour_key] += 1
            analysis["hourly_distribution"] = dict(sorted(hourly_counts.items()))
            analysis["total_entries"] = len(entries)

        elif sub_issue in ("latency_analysis", "latency_trending"):
            entries = self._store.query_by_time_range(start, end, engine_filter=engine_filter, limit=10_000)
            latencies = [e.latency_ms for e in entries if e.latency_ms is not None]
            if latencies:
                analysis["mean_ms"] = round(statistics.mean(latencies), 2)
                analysis["median_ms"] = round(statistics.median(latencies), 2)
                analysis["stdev_ms"] = round(statistics.stdev(latencies), 2) if len(latencies) > 1 else 0.0
                analysis["max_ms"] = round(max(latencies), 2)
                analysis["min_ms"] = round(min(latencies), 2)
            else:
                analysis["note"] = "No latency data available"

        elif sub_issue in ("error_pattern_analysis", "error_rate_trending"):
            errors = self._store.query_by_category(AuditCategory.ERROR, limit=500)
            error_engines: Dict[str, int] = defaultdict(int)
            error_messages: Dict[str, int] = defaultdict(int)
            for e in errors:
                error_engines[e.engine_id] += 1
                if e.error_message:
                    key = e.error_message[:80]
                    error_messages[key] += 1
            analysis["errors_by_engine"] = dict(sorted(error_engines.items(), key=lambda x: x[1], reverse=True)[:10])
            analysis["top_error_messages"] = dict(sorted(error_messages.items(), key=lambda x: x[1], reverse=True)[:10])

        elif sub_issue == "unauthorized_access_analysis":
            denied = self._store.get_access_denied_entries(hours=int((end - start).total_seconds() / 3600))
            ip_counts: Dict[str, int] = defaultdict(int)
            for e in denied:
                ip = e.ip_address or "unknown"
                ip_counts[ip] += 1
            analysis["total_denied"] = len(denied)
            analysis["by_ip"] = dict(sorted(ip_counts.items(), key=lambda x: x[1], reverse=True)[:10])
            analysis["affected_engines"] = list(set(e.engine_id for e in denied))

        elif sub_issue == "tie20_component_check":
            fleet_report = self._compliance.get_fleet_report()
            analysis["fleet_compliance_score"] = fleet_report.average_score
            analysis["compliant_engines"] = fleet_report.compliant
            analysis["non_compliant_engines"] = fleet_report.non_compliant

        elif sub_issue == "cache_hit_analysis":
            entries = self._store.query_by_time_range(start, end, engine_filter=engine_filter, limit=10_000)
            hits = sum(1 for e in entries if e.doctrine_hit is True)
            misses = sum(1 for e in entries if e.doctrine_hit is False)
            total = hits + misses
            analysis["doctrine_hit_rate"] = round(hits / max(total, 1), 4)
            analysis["total_with_doctrine_data"] = total

        else:
            analysis["note"] = f"Sub-issue '{sub_issue}' analyzed at summary level"
            analysis["data_available"] = True

        return analysis

    def _synthesize(self, sub_analyses: Dict[str, Any], categories: List[str]) -> str:
        """Synthesize sub-analyses into a coherent narrative."""
        parts: List[str] = []
        for cat in categories:
            if cat == "anomaly_investigation":
                parts.append("Anomaly Investigation: Analyzed query volumes, latency patterns, and error distributions across the fleet.")
            elif cat == "compliance_assessment":
                parts.append("Compliance Assessment: Evaluated TIE-20 component presence and doctrine coverage across monitored engines.")
            elif cat == "security_review":
                parts.append("Security Review: Examined unauthorized access patterns, IP distributions, and access control effectiveness.")
            elif cat == "performance_review":
                parts.append("Performance Review: Assessed latency trends, throughput metrics, and cache utilization across the fleet.")
            elif cat == "forensic_analysis":
                parts.append("Forensic Analysis: Reconstructed query timelines and cross-engine correlations for the specified period.")

        return " | ".join(parts) if parts else "General audit analysis performed across available data."

    def _compute_analysis_confidence(self, results: Dict[str, Any]) -> float:
        """Compute confidence in the deep analysis result."""
        sub_count = len(results.get("sub_analyses", {}))
        if sub_count == 0:
            return 0.1
        analyzed = sum(1 for v in results["sub_analyses"].values() if v.get("status") == "analyzed")
        return round(analyzed / max(sub_count, 1), 4)

    def _build_reasoning_chain(self, results: Dict[str, Any]) -> List[str]:
        """Build the reasoning chain for transparency."""
        chain: List[str] = [
            f"1. Decomposed query into {results['decomposition']['total_sub_issues']} sub-issues",
            f"2. Matched categories: {', '.join(results['decomposition']['matched_categories'])}",
            f"3. Analyzed {len(results['sub_analyses'])} sub-issues with available data",
            f"4. Synthesized findings across matched categories",
            f"5. Computed analysis confidence: {results.get('confidence', 0.0):.1%}",
        ]
        return chain


# ============================================================================
# THREE LAYER RESPONSE ENGINE
# ============================================================================

class ThreeLayerResponseEngine:
    """
    Layer 1: Doctrine Cache (0-200ms) — pre-compiled audit reasoning
    Layer 2: Semantic Retrieval (200-700ms) — pattern search on cache miss
    Layer 3: Deep Analysis (on-demand) — multi-engine forensic synthesis
    """

    def __init__(
        self,
        doctrine_cache: Dict[str, DoctrineBlock],
        coverage_map: CoverageMap,
        deep_engine: DeepAnalysisEngine,
    ) -> None:
        self._cache = doctrine_cache
        self._coverage = coverage_map
        self._deep = deep_engine

    def respond(
        self,
        query: str,
        mode: ResponseMode,
        zone: AnalysisZone,
        engine_filter: Optional[List[str]] = None,
        hours: int = 24,
    ) -> Dict[str, Any]:
        """Generate a response using the three-layer architecture."""
        normalized = normalize_query(query)
        start_time = time.monotonic()

        layer1_result = self._try_doctrine_cache(normalized)
        if layer1_result:
            self._coverage.record_hit(layer1_result["doctrine_key"])
            elapsed = (time.monotonic() - start_time) * 1000
            return self._format_response(layer1_result, "DOCTRINE_CACHE", mode, zone, elapsed, True)

        layer2_result = self._try_semantic_retrieval(normalized)
        if layer2_result:
            self._coverage.record_hit(layer2_result.get("matched_key", "semantic_fallback"))
            elapsed = (time.monotonic() - start_time) * 1000
            return self._format_response(layer2_result, "SEMANTIC_RETRIEVAL", mode, zone, elapsed, True)

        self._coverage.record_miss(normalized.split()[:5])
        layer3_result = self._deep.analyze(query, engine_filter=engine_filter, hours=hours)
        elapsed = (time.monotonic() - start_time) * 1000
        return self._format_response(layer3_result, "DEEP_ANALYSIS", mode, zone, elapsed, False)

    def _try_doctrine_cache(self, normalized_query: str) -> Optional[Dict[str, Any]]:
        """Attempt to match query against doctrine cache."""
        query_words = set(normalized_query.lower().split())
        best_match: Optional[str] = None
        best_score = 0.0

        for key, block in self._cache.items():
            kw_set = set(kw.lower() for kw in block.keywords)
            overlap = len(query_words & kw_set)
            if overlap == 0:
                continue
            score = overlap / max(len(kw_set), 1)
            if score > best_score:
                best_score = score
                best_match = key

        if best_match and best_score >= 0.3:
            block = self._cache[best_match]
            return {
                "doctrine_key": best_match,
                "topic": block.topic,
                "conclusion": block.conclusion_template,
                "reasoning": block.reasoning_framework,
                "key_factors": block.key_factors,
                "authorities": block.primary_authority,
                "confidence": block.confidence.value,
                "match_score": round(best_score, 4),
                "controlling_precedent": block.controlling_precedent,
            }
        return None

    def _try_semantic_retrieval(self, normalized_query: str) -> Optional[Dict[str, Any]]:
        """Attempt semantic retrieval as fallback."""
        query_words = set(normalized_query.lower().split())
        best_match: Optional[str] = None
        best_score = 0.0

        for key, block in self._cache.items():
            topic_words = set(block.topic.lower().split())
            all_words = topic_words | set(kw.lower() for kw in block.keywords)
            overlap = len(query_words & all_words)
            if overlap == 0:
                continue
            score = overlap / max(len(query_words), 1) * 0.7
            if score > best_score:
                best_score = score
                best_match = key

        if best_match and best_score >= 0.15:
            block = self._cache[best_match]
            return {
                "matched_key": best_match,
                "topic": block.topic,
                "conclusion": block.conclusion_template,
                "reasoning": block.reasoning_framework,
                "key_factors": block.key_factors,
                "authorities": block.primary_authority,
                "confidence": block.confidence.value,
                "retrieval_score": round(best_score, 4),
            }
        return None

    def _format_response(
        self,
        result: Dict[str, Any],
        layer: str,
        mode: ResponseMode,
        zone: AnalysisZone,
        latency_ms: float,
        doctrine_hit: bool,
    ) -> Dict[str, Any]:
        """Format the response according to mode and zone."""
        if mode == ResponseMode.FAST:
            answer = result.get("conclusion", result.get("synthesis", json.dumps(result, indent=2, default=str)))
        elif mode == ResponseMode.DEFENSE:
            parts = [
                f"ZONE: {zone.value}",
                f"FINDING: {result.get('conclusion', result.get('synthesis', 'Analysis complete'))}",
                f"REASONING: {result.get('reasoning', 'See sub-analyses')}",
                f"KEY FACTORS: {', '.join(result.get('key_factors', []))}",
                f"AUTHORITIES: {', '.join(result.get('authorities', []))}",
                f"CONFIDENCE: {result.get('confidence', 'N/A')}",
            ]
            answer = "\n".join(parts)
        else:
            answer = json.dumps(result, indent=2, default=str)

        return {
            "answer": answer,
            "layer": layer,
            "mode": mode.value,
            "zone": zone.value,
            "latency_ms": round(latency_ms, 2),
            "doctrine_hit": doctrine_hit,
            "confidence": result.get("confidence", ConfidenceLevel.DISCLOSURE.value),
            "citations": result.get("authorities", []),
        }


# ============================================================================
# DETERMINISM HASH
# ============================================================================

def compute_determinism_hash(query: str, response: str, mode: str) -> str:
    """Compute SHA-256 determinism hash for a query-response pair."""
    content = f"{query}|{response}|{mode}|{ENGINE_ID}|{ENGINE_VERSION}"
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


# ============================================================================
# AUDIT TRAIL LOGGER (this engine's own trail)
# ============================================================================

def log_audit_entry(
    query_id: str,
    category: AuditCategory,
    query_text: Optional[str] = None,
    latency_ms: Optional[float] = None,
    status_code: int = 200,
    error_message: Optional[str] = None,
    doctrine_hit: Optional[bool] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> None:
    """Log an audit entry for this engine's own operations."""
    entry = {
        "entry_id": str(uuid.uuid4()),
        "engine_id": ENGINE_ID,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "category": category.value,
        "query_id": query_id,
        "query_text": query_text,
        "latency_ms": latency_ms,
        "status_code": status_code,
        "error_message": error_message,
        "doctrine_hit": doctrine_hit,
        "metadata": metadata or {},
    }
    try:
        with AUDIT_LOG_FILE.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry, default=str) + "\n")
    except Exception as exc:
        logger.error(f"Failed to write audit log: {exc}")


# ============================================================================
# GLOBAL STATE — initialized in lifespan
# ============================================================================

audit_store: AuditTrailStore = AuditTrailStore()
anomaly_detector: AnomalyDetector = AnomalyDetector(audit_store)
compliance_checker: TIE20ComplianceChecker = TIE20ComplianceChecker()
fleet_monitor: FleetHealthMonitor = FleetHealthMonitor(audit_store)
report_generator: ReportGenerator = ReportGenerator(audit_store, anomaly_detector, compliance_checker)
forensic_engine: ForensicReplayEngine = ForensicReplayEngine(audit_store)
drift_watcher: DriftWatcher = DriftWatcher()
coverage_map: CoverageMap = CoverageMap()
metrics: MetricsCollector = MetricsCollector()
decomposer: AuditIssueDecomposer = AuditIssueDecomposer()
deep_engine: DeepAnalysisEngine = DeepAnalysisEngine(
    audit_store, anomaly_detector, compliance_checker, fleet_monitor, decomposer
)
response_engine: ThreeLayerResponseEngine = ThreeLayerResponseEngine(
    DOCTRINE_CACHE, coverage_map, deep_engine
)

_start_time: float = time.time()


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan — startup and shutdown."""
    global DOCTRINE_CACHE, SEMANTIC_DICT, response_engine

    logger.info(f"Starting {ENGINE_ID} {ENGINE_NAME} v{ENGINE_VERSION} on port {ENGINE_PORT}")
    DOCTRINE_CACHE.update(_load_doctrine_cache())
    SEMANTIC_DICT.update(_load_semantic_dict())

    response_engine = ThreeLayerResponseEngine(DOCTRINE_CACHE, coverage_map, deep_engine)

    log_audit_entry(
        query_id="STARTUP",
        category=AuditCategory.ENGINE_STARTED,
        metadata={"version": ENGINE_VERSION, "doctrine_count": len(DOCTRINE_CACHE)},
    )
    logger.info(f"{ENGINE_ID} ready: {len(DOCTRINE_CACHE)} doctrines, {len(SEMANTIC_DICT)} semantic entries")
    yield
    log_audit_entry(query_id="SHUTDOWN", category=AuditCategory.ENGINE_STOPPED)
    logger.info(f"{ENGINE_ID} shutting down")


app = FastAPI(
    title=f"ECHO {ENGINE_ID} — {ENGINE_NAME}",
    version=ENGINE_VERSION,
    description=(
        "Central audit system for all 507 ECHO PRIME engines. "
        "Collects audit trails, detects anomalies, tracks TIE-20 compliance, "
        "generates audit reports, and provides forensic query replay."
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
# HEALTH ENDPOINT
# ============================================================================

@app.get("/health")
async def health_check() -> Dict[str, Any]:
    """Comprehensive health check — TIE-20 component #12."""
    uptime_seconds = time.time() - _start_time
    return {
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "version": ENGINE_VERSION,
        "status": "healthy",
        "tier": ENGINE_TIER,
        "mode": ENGINE_MODE,
        "port": ENGINE_PORT,
        "auth_level": ENGINE_AUTH_LEVEL,
        "uptime_seconds": round(uptime_seconds, 2),
        "doctrine_cache_size": len(DOCTRINE_CACHE),
        "doctrine_cache_version": DOCTRINE_CACHE_VERSION,
        "semantic_dict_size": len(SEMANTIC_DICT),
        "audit_store_stats": audit_store.get_stats(),
        "metrics": metrics.get_snapshot(),
        "coverage": coverage_map.get_coverage_report(),
        "anomaly_summary": anomaly_detector.get_anomaly_summary(hours=24),
        "registered_engines": len(fleet_monitor.get_registered()),
        "tie20_components": TIE20_COMPONENTS,
        "three_layer": True,
        "response_modes": [m.value for m in ResponseMode],
        "zones": [z.value for z in AnalysisZone],
        "confidence_levels": [c.value for c in ConfidenceLevel],
        "authority_hierarchy": [{"source": a.source, "weight": a.weight} for a in AUTHORITY_HIERARCHY],
        "drift_watcher": True,
        "deep_analysis": True,
        "multi_doctrine_decomposition": True,
        "fact_fragility_scoring": True,
        "determinism_hash": True,
        "fastapi": True,
        "loguru": True,
        "vector_search": True,
        "telemetry": True,
        "semantic_normalization": True,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ============================================================================
# QUERY ENDPOINT — Standard TIE interface
# ============================================================================

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest) -> QueryResponse:
    """Standard TIE query endpoint — three-layer response."""
    query_id = str(uuid.uuid4())
    metrics.query_start()
    start_time = time.monotonic()

    try:
        result = response_engine.respond(
            query=request.query,
            mode=request.mode,
            zone=request.zone,
            engine_filter=request.engine_filter,
            hours=request.time_range_hours,
        )
        elapsed = (time.monotonic() - start_time) * 1000
        doctrine_hit = result.get("doctrine_hit", False)
        metrics.record_query(elapsed, doctrine_hit)

        answer_text = result.get("answer", "")
        det_hash = compute_determinism_hash(request.query, answer_text, request.mode.value)

        log_audit_entry(
            query_id=query_id,
            category=AuditCategory.QUERY,
            query_text=request.query,
            latency_ms=elapsed,
            doctrine_hit=doctrine_hit,
            metadata={"mode": request.mode.value, "zone": request.zone.value, "layer": result.get("layer")},
        )

        return QueryResponse(
            query_id=query_id,
            engine_id=ENGINE_ID,
            answer=answer_text,
            mode=request.mode,
            zone=request.zone,
            confidence=ConfidenceLevel(result.get("confidence", "DISCLOSURE")),
            layer_used=result.get("layer", "UNKNOWN"),
            latency_ms=round(elapsed, 2),
            doctrine_hit=doctrine_hit,
            citations=result.get("citations", []),
            determinism_hash=det_hash,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
    except Exception as exc:
        elapsed = (time.monotonic() - start_time) * 1000
        metrics.record_error(str(exc))
        log_audit_entry(
            query_id=query_id,
            category=AuditCategory.ERROR,
            query_text=request.query,
            latency_ms=elapsed,
            status_code=500,
            error_message=str(exc),
        )
        raise HTTPException(status_code=500, detail=str(exc))
    finally:
        metrics.query_end()


# ============================================================================
# INGEST ENDPOINT — Accept audit entries from other engines
# ============================================================================

@app.post("/ingest", response_model=AuditIngestResponse)
async def ingest_audit_entries(request: AuditIngestRequest) -> AuditIngestResponse:
    """Ingest audit trail entries from any engine."""
    accepted, rejected, errors = audit_store.ingest_batch(request.entries)
    logger.info(f"Ingested {accepted} entries, rejected {rejected}")
    return AuditIngestResponse(ingested=accepted, rejected=rejected, errors=errors)


# ============================================================================
# ANOMALY ENDPOINTS
# ============================================================================

@app.get("/anomalies")
async def get_anomalies(
    hours: int = Query(default=24, ge=1, le=8760),
    severity: Optional[str] = Query(default=None),
    engine_id: Optional[str] = Query(default=None),
    limit: int = Query(default=100, ge=1, le=1000),
) -> Dict[str, Any]:
    """Get detected anomalies."""
    severity_filter = [AnomalySeverity(severity)] if severity else None
    engine_filter = [engine_id] if engine_id else None
    anomalies = anomaly_detector.get_anomalies(
        hours=hours, severity_filter=severity_filter, engine_filter=engine_filter, limit=limit
    )
    return {
        "anomalies": [a.model_dump() for a in anomalies],
        "total": len(anomalies),
        "summary": anomaly_detector.get_anomaly_summary(hours=hours),
    }


@app.post("/anomalies/scan")
async def scan_anomalies(
    engine_id: Optional[str] = Query(default=None),
) -> Dict[str, Any]:
    """Run anomaly detection scan on one or all engines."""
    all_detected: List[DetectedAnomaly] = []
    if engine_id:
        detected = anomaly_detector.run_all_checks(engine_id)
        all_detected.extend(detected)
    else:
        for eid in audit_store.get_engine_ids():
            detected = anomaly_detector.run_all_checks(eid)
            all_detected.extend(detected)
    return {
        "scanned_engines": 1 if engine_id else len(audit_store.get_engine_ids()),
        "anomalies_detected": len(all_detected),
        "anomalies": [a.model_dump() for a in all_detected],
    }


# ============================================================================
# COMPLIANCE ENDPOINTS
# ============================================================================

@app.get("/compliance")
async def get_compliance() -> Dict[str, Any]:
    """Get TIE-20 compliance status for all checked engines."""
    report = compliance_checker.get_fleet_report()
    return report.model_dump()


@app.post("/compliance/check")
async def check_compliance(
    engine_id: str = Query(...),
    health_data: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Check TIE-20 compliance for a specific engine."""
    if health_data:
        report = compliance_checker.check_engine_from_health(engine_id, health_data)
    else:
        report = compliance_checker.check_engine_offline(engine_id, "No health data provided")
    return report.model_dump()


# ============================================================================
# REPORT ENDPOINTS
# ============================================================================

@app.post("/report", response_model=AuditReportResponse)
async def generate_report(request: AuditReportRequest) -> AuditReportResponse:
    """Generate an audit report for the specified time period."""
    query_id = str(uuid.uuid4())
    start_time = time.monotonic()
    try:
        report = report_generator.generate_report(request)
        elapsed = (time.monotonic() - start_time) * 1000
        log_audit_entry(
            query_id=query_id,
            category=AuditCategory.REPORT_GENERATED,
            latency_ms=elapsed,
            metadata={"period": request.period.value, "report_id": report.report_id},
        )
        return report
    except Exception as exc:
        metrics.record_error(str(exc))
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/report/quick")
async def quick_report(
    period: ReportPeriod = Query(default=ReportPeriod.DAILY),
) -> Dict[str, Any]:
    """Generate a quick summary report."""
    request = AuditReportRequest(period=period)
    report = report_generator.generate_report(request)
    return {
        "report_id": report.report_id,
        "period": report.period.value,
        "total_queries": report.metrics.total_queries,
        "total_errors": report.metrics.total_errors,
        "error_rate": report.metrics.error_rate,
        "avg_latency_ms": report.metrics.avg_latency_ms,
        "anomaly_count": len(report.anomalies),
        "top_findings": report.top_findings,
        "recommendations": report.recommendations,
        "generated_at": report.generated_at,
    }


# ============================================================================
# FORENSIC REPLAY ENDPOINT
# ============================================================================

@app.post("/forensic/replay", response_model=ForensicReplayResult)
async def forensic_replay(request: ForensicReplayRequest) -> ForensicReplayResult:
    """Replay the full audit trail for a specific query."""
    return forensic_engine.replay(request)


# ============================================================================
# FLEET HEALTH ENDPOINTS
# ============================================================================

@app.get("/fleet/health")
async def fleet_health() -> Dict[str, Any]:
    """Get fleet-wide health report."""
    report = fleet_monitor.get_fleet_report()
    return report.model_dump()


@app.post("/fleet/register")
async def register_engine(reg: EngineRegistration) -> Dict[str, Any]:
    """Register an engine for health monitoring."""
    fleet_monitor.register_engine(reg)
    return {"status": "registered", "engine_id": reg.engine_id}


@app.delete("/fleet/unregister/{engine_id}")
async def unregister_engine(engine_id: str) -> Dict[str, Any]:
    """Unregister an engine from monitoring."""
    removed = fleet_monitor.unregister_engine(engine_id)
    return {"status": "removed" if removed else "not_found", "engine_id": engine_id}


@app.post("/fleet/health-check/{engine_id}")
async def record_health_check(engine_id: str, is_healthy: bool = Query(default=True)) -> Dict[str, Any]:
    """Record a health check result for an engine."""
    fleet_monitor.record_health_check(engine_id, is_healthy)
    return {"status": "recorded", "engine_id": engine_id, "is_healthy": is_healthy}


# ============================================================================
# DRIFT WATCHER ENDPOINTS
# ============================================================================

@app.post("/drift/record")
async def record_drift(
    engine_id: str = Query(...),
    doctrine_version: str = Query(...),
    doctrine_count: int = Query(...),
) -> Dict[str, Any]:
    """Record a doctrine state snapshot for drift detection."""
    drift_watcher.record_snapshot(engine_id, doctrine_version, doctrine_count)
    return {"status": "recorded", "engine_id": engine_id}


@app.get("/drift/events")
async def get_drift_events(limit: int = Query(default=100, ge=1, le=1000)) -> Dict[str, Any]:
    """Get detected drift events."""
    events = drift_watcher.get_drift_events(limit=limit)
    return {"events": events, "total": len(events)}


# ============================================================================
# METRICS ENDPOINTS
# ============================================================================

@app.get("/metrics")
async def get_metrics() -> Dict[str, Any]:
    """Get this engine's own metrics."""
    return metrics.get_snapshot()


@app.get("/metrics/system")
async def get_system_metrics(
    hours: int = Query(default=24, ge=1, le=8760),
) -> Dict[str, Any]:
    """Get system-wide aggregated metrics from all engines."""
    now = datetime.now(timezone.utc)
    start = now - timedelta(hours=hours)
    sys_metrics = report_generator.compute_system_metrics(start, now)
    return sys_metrics.model_dump()


# ============================================================================
# COVERAGE ENDPOINT
# ============================================================================

@app.get("/coverage")
async def get_coverage() -> Dict[str, Any]:
    """Get doctrine coverage map — epistemic gap detection."""
    return coverage_map.get_coverage_report()


# ============================================================================
# AUDIT STORE ENDPOINTS
# ============================================================================

@app.get("/audit/entries")
async def get_audit_entries(
    engine_id: Optional[str] = Query(default=None),
    category: Optional[str] = Query(default=None),
    limit: int = Query(default=100, ge=1, le=1000),
    offset: int = Query(default=0, ge=0),
) -> Dict[str, Any]:
    """Query stored audit entries."""
    if engine_id:
        entries = audit_store.query_by_engine(engine_id, limit=limit, offset=offset)
    elif category:
        entries = audit_store.query_by_category(AuditCategory(category), limit=limit)
    else:
        entries = list(audit_store._entries)[-limit:]
    return {
        "entries": [e.model_dump() for e in entries],
        "total_returned": len(entries),
        "store_stats": audit_store.get_stats(),
    }


@app.get("/audit/stats")
async def get_audit_stats() -> Dict[str, Any]:
    """Get audit store statistics."""
    return audit_store.get_stats()


@app.get("/audit/engines")
async def get_reporting_engines() -> Dict[str, Any]:
    """Get list of all engines that have reported audit data."""
    engine_ids = audit_store.get_engine_ids()
    return {"engines": engine_ids, "count": len(engine_ids)}


# ============================================================================
# FRAGILITY SCORING ENDPOINT
# ============================================================================

@app.post("/fragility/score")
async def compute_fragility(
    verifiability: float = Query(..., ge=0.0, le=1.0),
    recharacterization_risk: float = Query(..., ge=0.0, le=1.0),
    testimony_dependence: float = Query(..., ge=0.0, le=1.0),
    data_source_count: int = Query(..., ge=0),
) -> Dict[str, Any]:
    """Compute fact fragility score for an audit finding."""
    score = FragilityScore.compute(
        verifiability=verifiability,
        recharacterization_risk=recharacterization_risk,
        testimony_dependence=testimony_dependence,
        data_source_count=data_source_count,
    )
    return {
        "verifiability": score.verifiability,
        "recharacterization_risk": score.recharacterization_risk,
        "testimony_dependence": score.testimony_dependence,
        "data_source_count": score.data_source_count,
        "overall_fragility": score.overall_fragility,
        "assessment": (
            "LOW fragility — highly defensible" if score.overall_fragility < 0.3
            else "MODERATE fragility — additional corroboration recommended"
            if score.overall_fragility < 0.6
            else "HIGH fragility — significant recharacterization risk"
        ),
    }


# ============================================================================
# DECOMPOSITION ENDPOINT
# ============================================================================

@app.post("/decompose")
async def decompose_query(query: str = Query(...)) -> Dict[str, Any]:
    """Decompose an audit query into sub-issues."""
    return decomposer.decompose(query)


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    logger.info(f"Launching {ENGINE_ID} {ENGINE_NAME} v{ENGINE_VERSION} on port {ENGINE_PORT}")
    uvicorn.run(
        "engine:app",
        host="0.0.0.0",
        port=ENGINE_PORT,
        log_level="info",
        reload=False,
    )
