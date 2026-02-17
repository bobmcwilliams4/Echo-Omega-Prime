"""
LG01 CONTRACT ANALYSIS ENGINE - Professional Telemetry & Logging
Institutional-grade observability infrastructure for contract analysis audit,
compliance verification, and operational monitoring.

Components:
    1. QueryTracer - Every contract query logged with full context
    2. ReasoningSnapshot - Reproducible clause analysis paths for audit replay
    3. DoctrineMutationLog - Immutable changelog for doctrine modifications
    4. ErrorSpine - Centralized error collection with stack traces
    5. PerformanceTelemetry - Real-time performance metrics
    6. ClauseExtractionLog - Track all clause extraction operations
    7. RiskAssessmentLog - Risk scoring audit trail
    8. ComplianceCheckLog - Regulatory compliance check history

Engine: LG01 Contract Analysis Engine
Tier: 1 (LEGAL)
Mode: DET (Deterministic)
Author: ECHO OMEGA PRIME
Authority: 11.0 SOVEREIGN
"""

import hashlib
import json
import sqlite3
import threading
import traceback
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Optional, List, Dict, Any, Callable, Tuple
from contextlib import contextmanager
import time

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

from loguru import logger

# ============================================================================
# CONFIGURATION
# ============================================================================

TELEMETRY_DIR = Path("O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/LG01/telemetry")
TELEMETRY_DIR.mkdir(parents=True, exist_ok=True)

QUERY_LOG = TELEMETRY_DIR / "query_traces.jsonl"
REASONING_LOG = TELEMETRY_DIR / "reasoning_snapshots.jsonl"
ERROR_LOG = TELEMETRY_DIR / "error_spine.jsonl"
PERFORMANCE_LOG = TELEMETRY_DIR / "performance_metrics.jsonl"
CLAUSE_EXTRACTION_LOG = TELEMETRY_DIR / "clause_extractions.jsonl"
RISK_ASSESSMENT_LOG = TELEMETRY_DIR / "risk_assessments.jsonl"
COMPLIANCE_CHECK_LOG = TELEMETRY_DIR / "compliance_checks.jsonl"

AUDIT_DB = TELEMETRY_DIR / "audit_trail.db"
MUTATION_DB = TELEMETRY_DIR / "doctrine_mutations.db"

logger.add(
    TELEMETRY_DIR / "lg01_telemetry_{time}.log",
    rotation="100 MB",
    retention="90 days",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {module}:{function}:{line} | {message}",
    serialize=True,
)


# ============================================================================
# ENUMS AND TYPES
# ============================================================================

class ResponseLayer(str, Enum):
    """Layer that produced the response."""
    DOCTRINE = "doctrine"
    SEMANTIC = "semantic"
    DEEP_ANALYSIS = "deep_analysis"
    ERROR = "error"


class MutationType(str, Enum):
    """Types of doctrine mutations."""
    ADD = "add"
    EDIT = "edit"
    DELETE = "delete"
    BULK_IMPORT = "bulk_import"


class MutationOrigin(str, Enum):
    """Origin of a doctrine mutation."""
    MANUAL = "manual"
    AI_GENERATED = "ai_generated"
    MIGRATION = "migration"
    SYSTEM = "system"


class ErrorSeverity(str, Enum):
    """Error severity classification."""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class ErrorDomain(str, Enum):
    """Domain where error originated."""
    API = "api"
    DOCTRINE_ENGINE = "doctrine_engine"
    CLAUSE_EXTRACTION = "clause_extraction"
    RISK_ASSESSMENT = "risk_assessment"
    COMPLIANCE_CHECK = "compliance_check"
    SEARCH = "search"
    SERIALIZATION = "serialization"
    DATABASE = "database"
    NETWORK = "network"
    CONTRACT_PARSING = "contract_parsing"
    UNKNOWN = "unknown"


class ClauseCategory(str, Enum):
    """Categories of extracted clauses."""
    FINANCIAL = "financial"
    OPERATIONAL = "operational"
    LEGAL = "legal"
    TERMINATION = "termination"
    IP_DATA = "ip_data"
    CHANGE_CONTROL = "change_control"
    BOILERPLATE = "boilerplate"
    CUSTOM = "custom"


class RiskLevel(str, Enum):
    """Risk assessment levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NEGLIGIBLE = "negligible"


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class QueryTrace:
    """Complete trace of a single contract analysis query."""
    trace_id: str
    timestamp: str
    query_text: str
    query_type: str
    contract_type: Optional[str]
    mode: str

    doctrine_matched: bool
    doctrine_id: Optional[str]
    doctrine_topic: Optional[str]
    confidence_score: float

    response_layer: str
    semantic_triggered: bool
    deep_analysis_triggered: bool

    latency_ms: float
    doctrine_lookup_ms: float
    semantic_lookup_ms: float
    total_tokens: int

    response_length: int
    citations_count: int
    clauses_extracted: int
    risk_scores_computed: int

    client_ip: Optional[str] = None
    user_agent: Optional[str] = None
    session_id: Optional[str] = None
    contract_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Serialize for JSON logging."""
        return asdict(self)


@dataclass
class ReasoningSnapshot:
    """Reproducible reasoning path for audit replay."""
    snapshot_id: str
    trace_id: str
    timestamp: str

    input_hash: str
    input_text: str
    normalized_text: str
    normalization_delta: List[str]

    doctrine_candidates: List[Dict[str, Any]]
    selected_doctrine: Optional[str]
    selection_rationale: str
    match_scores: Dict[str, float]

    reasoning_steps: List[Dict[str, str]]
    citations_used: List[Dict[str, str]]
    risk_factors_identified: List[str]

    output_hash: str
    determinism_verified: bool

    def to_dict(self) -> Dict[str, Any]:
        """Serialize for JSON logging."""
        return asdict(self)


@dataclass
class DoctrineMutationRecord:
    """Immutable record of a doctrine change."""
    mutation_id: str
    timestamp: str
    doctrine_key: str
    mutation_type: MutationType
    origin: MutationOrigin
    author: str

    before_hash: Optional[str]
    after_hash: str

    before_summary: Optional[str]
    after_summary: str
    justification: str

    approved_by: Optional[str] = None
    rollback_hash: Optional[str] = None
    regression_suite_passed: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Serialize for storage."""
        result = asdict(self)
        result["mutation_type"] = self.mutation_type.value
        result["origin"] = self.origin.value
        return result


@dataclass
class ErrorRecord:
    """Structured error record with full context."""
    error_id: str
    timestamp: str
    severity: ErrorSeverity
    domain: ErrorDomain
    message: str
    stack_trace: Optional[str]

    trace_id: Optional[str] = None
    contract_id: Optional[str] = None
    clause_type: Optional[str] = None
    input_snippet: Optional[str] = None
    resolution: Optional[str] = None
    recovered: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Serialize for logging."""
        result = asdict(self)
        result["severity"] = self.severity.value
        result["domain"] = self.domain.value
        return result


@dataclass
class ClauseExtractionRecord:
    """Record of a clause extraction operation."""
    extraction_id: str
    timestamp: str
    trace_id: str
    contract_id: Optional[str]

    clause_type: str
    clause_category: ClauseCategory
    clause_text_hash: str
    clause_length: int
    confidence: float

    extraction_method: str
    is_boilerplate: bool
    customization_score: float
    risk_flags: List[str]

    latency_ms: float

    def to_dict(self) -> Dict[str, Any]:
        """Serialize for logging."""
        result = asdict(self)
        result["clause_category"] = self.clause_category.value
        return result


@dataclass
class RiskAssessmentRecord:
    """Record of a risk assessment computation."""
    assessment_id: str
    timestamp: str
    trace_id: str
    contract_id: Optional[str]

    risk_category: str
    risk_level: RiskLevel
    risk_score: float
    risk_factors: List[str]
    mitigating_factors: List[str]

    clause_references: List[str]
    recommendation: str
    confidence: float

    latency_ms: float

    def to_dict(self) -> Dict[str, Any]:
        """Serialize for logging."""
        result = asdict(self)
        result["risk_level"] = self.risk_level.value
        return result


@dataclass
class ComplianceCheckRecord:
    """Record of a compliance check operation."""
    check_id: str
    timestamp: str
    trace_id: str
    contract_id: Optional[str]

    framework: str
    requirement: str
    status: str
    findings: List[str]
    remediation: Optional[str]
    confidence: float

    latency_ms: float

    def to_dict(self) -> Dict[str, Any]:
        """Serialize for logging."""
        return asdict(self)


@dataclass
class PerformanceSnapshot:
    """Point-in-time performance metrics."""
    timestamp: str
    engine_id: str = "LG01"

    queries_total: int = 0
    queries_last_hour: int = 0
    queries_last_minute: int = 0

    avg_latency_ms: float = 0.0
    p50_latency_ms: float = 0.0
    p95_latency_ms: float = 0.0
    p99_latency_ms: float = 0.0
    max_latency_ms: float = 0.0

    doctrine_hit_rate: float = 0.0
    cache_hit_rate: float = 0.0

    clauses_extracted_total: int = 0
    risk_assessments_total: int = 0
    compliance_checks_total: int = 0

    errors_last_hour: int = 0
    error_rate: float = 0.0

    cpu_percent: float = 0.0
    memory_mb: float = 0.0
    memory_percent: float = 0.0

    active_queries: int = 0
    queue_depth: int = 0

    uptime_seconds: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Serialize for logging."""
        return asdict(self)


# ============================================================================
# AUDIT DATABASE MANAGER
# ============================================================================

class AuditDatabase:
    """Thread-safe SQLite audit database for immutable query records."""

    def __init__(self, db_path: Path):
        self._db_path = db_path
        self._local = threading.local()
        self._init_lock = threading.Lock()
        self._initialized = False
        self._ensure_tables()

    def _get_conn(self) -> sqlite3.Connection:
        """Get thread-local database connection."""
        if not hasattr(self._local, "conn") or self._local.conn is None:
            self._local.conn = sqlite3.connect(
                str(self._db_path),
                timeout=30,
                check_same_thread=False,
            )
            self._local.conn.execute("PRAGMA journal_mode=WAL")
            self._local.conn.execute("PRAGMA synchronous=NORMAL")
            self._local.conn.execute("PRAGMA cache_size=-64000")
            self._local.conn.row_factory = sqlite3.Row
        return self._local.conn

    def _ensure_tables(self) -> None:
        """Create tables if they do not exist."""
        with self._init_lock:
            if self._initialized:
                return
            conn = self._get_conn()
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS query_audit (
                    trace_id TEXT PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    query_text TEXT NOT NULL,
                    query_type TEXT NOT NULL,
                    contract_type TEXT,
                    mode TEXT NOT NULL,
                    doctrine_matched INTEGER NOT NULL DEFAULT 0,
                    doctrine_id TEXT,
                    doctrine_topic TEXT,
                    confidence_score REAL NOT NULL DEFAULT 0.0,
                    response_layer TEXT NOT NULL,
                    latency_ms REAL NOT NULL DEFAULT 0.0,
                    clauses_extracted INTEGER NOT NULL DEFAULT 0,
                    risk_scores_computed INTEGER NOT NULL DEFAULT 0,
                    contract_id TEXT,
                    session_id TEXT,
                    determinism_hash TEXT
                );

                CREATE TABLE IF NOT EXISTS clause_audit (
                    extraction_id TEXT PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    trace_id TEXT NOT NULL,
                    contract_id TEXT,
                    clause_type TEXT NOT NULL,
                    clause_category TEXT NOT NULL,
                    clause_text_hash TEXT NOT NULL,
                    confidence REAL NOT NULL DEFAULT 0.0,
                    is_boilerplate INTEGER NOT NULL DEFAULT 0,
                    risk_flags TEXT,
                    FOREIGN KEY (trace_id) REFERENCES query_audit(trace_id)
                );

                CREATE TABLE IF NOT EXISTS risk_audit (
                    assessment_id TEXT PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    trace_id TEXT NOT NULL,
                    contract_id TEXT,
                    risk_category TEXT NOT NULL,
                    risk_level TEXT NOT NULL,
                    risk_score REAL NOT NULL DEFAULT 0.0,
                    risk_factors TEXT,
                    recommendation TEXT,
                    FOREIGN KEY (trace_id) REFERENCES query_audit(trace_id)
                );

                CREATE TABLE IF NOT EXISTS compliance_audit (
                    check_id TEXT PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    trace_id TEXT NOT NULL,
                    contract_id TEXT,
                    framework TEXT NOT NULL,
                    requirement TEXT NOT NULL,
                    status TEXT NOT NULL,
                    findings TEXT,
                    remediation TEXT,
                    FOREIGN KEY (trace_id) REFERENCES query_audit(trace_id)
                );

                CREATE TABLE IF NOT EXISTS error_audit (
                    error_id TEXT PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    domain TEXT NOT NULL,
                    message TEXT NOT NULL,
                    trace_id TEXT,
                    contract_id TEXT,
                    stack_trace TEXT,
                    recovered INTEGER NOT NULL DEFAULT 0
                );

                CREATE INDEX IF NOT EXISTS idx_query_timestamp ON query_audit(timestamp);
                CREATE INDEX IF NOT EXISTS idx_query_contract ON query_audit(contract_id);
                CREATE INDEX IF NOT EXISTS idx_query_doctrine ON query_audit(doctrine_id);
                CREATE INDEX IF NOT EXISTS idx_clause_trace ON clause_audit(trace_id);
                CREATE INDEX IF NOT EXISTS idx_clause_type ON clause_audit(clause_type);
                CREATE INDEX IF NOT EXISTS idx_risk_trace ON risk_audit(trace_id);
                CREATE INDEX IF NOT EXISTS idx_risk_level ON risk_audit(risk_level);
                CREATE INDEX IF NOT EXISTS idx_compliance_trace ON compliance_audit(trace_id);
                CREATE INDEX IF NOT EXISTS idx_compliance_framework ON compliance_audit(framework);
                CREATE INDEX IF NOT EXISTS idx_error_severity ON error_audit(severity);
                CREATE INDEX IF NOT EXISTS idx_error_domain ON error_audit(domain);
            """)
            conn.commit()
            self._initialized = True
            logger.info("LG01 audit database initialized at {}", self._db_path)

    def record_query(self, trace: QueryTrace, determinism_hash: Optional[str] = None) -> None:
        """Insert query audit record."""
        conn = self._get_conn()
        try:
            conn.execute(
                """INSERT OR REPLACE INTO query_audit
                   (trace_id, timestamp, query_text, query_type, contract_type, mode,
                    doctrine_matched, doctrine_id, doctrine_topic, confidence_score,
                    response_layer, latency_ms, clauses_extracted, risk_scores_computed,
                    contract_id, session_id, determinism_hash)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    trace.trace_id, trace.timestamp, trace.query_text, trace.query_type,
                    trace.contract_type, trace.mode, int(trace.doctrine_matched),
                    trace.doctrine_id, trace.doctrine_topic, trace.confidence_score,
                    trace.response_layer, trace.latency_ms, trace.clauses_extracted,
                    trace.risk_scores_computed, trace.contract_id, trace.session_id,
                    determinism_hash,
                ),
            )
            conn.commit()
        except sqlite3.Error as exc:
            logger.error("Failed to record query audit: {}", exc)

    def record_clause_extraction(self, record: ClauseExtractionRecord) -> None:
        """Insert clause extraction audit record."""
        conn = self._get_conn()
        try:
            conn.execute(
                """INSERT OR REPLACE INTO clause_audit
                   (extraction_id, timestamp, trace_id, contract_id, clause_type,
                    clause_category, clause_text_hash, confidence, is_boilerplate, risk_flags)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    record.extraction_id, record.timestamp, record.trace_id,
                    record.contract_id, record.clause_type,
                    record.clause_category.value, record.clause_text_hash,
                    record.confidence, int(record.is_boilerplate),
                    json.dumps(record.risk_flags),
                ),
            )
            conn.commit()
        except sqlite3.Error as exc:
            logger.error("Failed to record clause extraction audit: {}", exc)

    def record_risk_assessment(self, record: RiskAssessmentRecord) -> None:
        """Insert risk assessment audit record."""
        conn = self._get_conn()
        try:
            conn.execute(
                """INSERT OR REPLACE INTO risk_audit
                   (assessment_id, timestamp, trace_id, contract_id, risk_category,
                    risk_level, risk_score, risk_factors, recommendation)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    record.assessment_id, record.timestamp, record.trace_id,
                    record.contract_id, record.risk_category,
                    record.risk_level.value, record.risk_score,
                    json.dumps(record.risk_factors), record.recommendation,
                ),
            )
            conn.commit()
        except sqlite3.Error as exc:
            logger.error("Failed to record risk assessment audit: {}", exc)

    def record_compliance_check(self, record: ComplianceCheckRecord) -> None:
        """Insert compliance check audit record."""
        conn = self._get_conn()
        try:
            conn.execute(
                """INSERT OR REPLACE INTO compliance_audit
                   (check_id, timestamp, trace_id, contract_id, framework,
                    requirement, status, findings, remediation)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    record.check_id, record.timestamp, record.trace_id,
                    record.contract_id, record.framework,
                    record.requirement, record.status,
                    json.dumps(record.findings), record.remediation,
                ),
            )
            conn.commit()
        except sqlite3.Error as exc:
            logger.error("Failed to record compliance check audit: {}", exc)

    def record_error(self, record: ErrorRecord) -> None:
        """Insert error audit record."""
        conn = self._get_conn()
        try:
            conn.execute(
                """INSERT OR REPLACE INTO error_audit
                   (error_id, timestamp, severity, domain, message,
                    trace_id, contract_id, stack_trace, recovered)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    record.error_id, record.timestamp, record.severity.value,
                    record.domain.value, record.message,
                    record.trace_id, record.contract_id,
                    record.stack_trace, int(record.recovered),
                ),
            )
            conn.commit()
        except sqlite3.Error as exc:
            logger.error("Failed to record error audit: {}", exc)

    def get_query_count(self, since_hours: int = 24) -> int:
        """Get query count for the specified time window."""
        conn = self._get_conn()
        cutoff = datetime.now(timezone.utc).isoformat()
        try:
            row = conn.execute(
                "SELECT COUNT(*) as cnt FROM query_audit WHERE timestamp > ?",
                (cutoff,),
            ).fetchone()
            return row["cnt"] if row else 0
        except sqlite3.Error:
            return 0

    def get_error_count(self, since_hours: int = 1) -> int:
        """Get error count for the specified time window."""
        conn = self._get_conn()
        try:
            row = conn.execute(
                "SELECT COUNT(*) as cnt FROM error_audit WHERE severity IN ('error', 'critical')",
            ).fetchone()
            return row["cnt"] if row else 0
        except sqlite3.Error:
            return 0

    def get_recent_errors(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recent errors for dashboard display."""
        conn = self._get_conn()
        try:
            rows = conn.execute(
                "SELECT * FROM error_audit ORDER BY timestamp DESC LIMIT ?",
                (limit,),
            ).fetchall()
            return [dict(r) for r in rows]
        except sqlite3.Error:
            return []

    def get_clause_stats(self) -> Dict[str, int]:
        """Get clause extraction statistics by type."""
        conn = self._get_conn()
        try:
            rows = conn.execute(
                "SELECT clause_type, COUNT(*) as cnt FROM clause_audit GROUP BY clause_type ORDER BY cnt DESC",
            ).fetchall()
            return {r["clause_type"]: r["cnt"] for r in rows}
        except sqlite3.Error:
            return {}

    def get_risk_distribution(self) -> Dict[str, int]:
        """Get risk level distribution."""
        conn = self._get_conn()
        try:
            rows = conn.execute(
                "SELECT risk_level, COUNT(*) as cnt FROM risk_audit GROUP BY risk_level",
            ).fetchall()
            return {r["risk_level"]: r["cnt"] for r in rows}
        except sqlite3.Error:
            return {}


# ============================================================================
# MUTATION DATABASE MANAGER
# ============================================================================

class MutationDatabase:
    """Thread-safe SQLite database for doctrine mutation tracking."""

    def __init__(self, db_path: Path):
        self._db_path = db_path
        self._local = threading.local()
        self._init_lock = threading.Lock()
        self._initialized = False
        self._ensure_tables()

    def _get_conn(self) -> sqlite3.Connection:
        """Get thread-local connection."""
        if not hasattr(self._local, "conn") or self._local.conn is None:
            self._local.conn = sqlite3.connect(
                str(self._db_path), timeout=30, check_same_thread=False,
            )
            self._local.conn.execute("PRAGMA journal_mode=WAL")
            self._local.conn.row_factory = sqlite3.Row
        return self._local.conn

    def _ensure_tables(self) -> None:
        """Create mutation tracking tables."""
        with self._init_lock:
            if self._initialized:
                return
            conn = self._get_conn()
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS doctrine_mutations (
                    mutation_id TEXT PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    doctrine_key TEXT NOT NULL,
                    mutation_type TEXT NOT NULL,
                    origin TEXT NOT NULL,
                    author TEXT NOT NULL,
                    before_hash TEXT,
                    after_hash TEXT NOT NULL,
                    before_summary TEXT,
                    after_summary TEXT NOT NULL,
                    justification TEXT NOT NULL,
                    approved_by TEXT,
                    rollback_hash TEXT,
                    regression_suite_passed INTEGER NOT NULL DEFAULT 0
                );

                CREATE INDEX IF NOT EXISTS idx_mutation_doctrine ON doctrine_mutations(doctrine_key);
                CREATE INDEX IF NOT EXISTS idx_mutation_type ON doctrine_mutations(mutation_type);
                CREATE INDEX IF NOT EXISTS idx_mutation_timestamp ON doctrine_mutations(timestamp);
            """)
            conn.commit()
            self._initialized = True
            logger.info("LG01 mutation database initialized at {}", self._db_path)

    def record_mutation(self, record: DoctrineMutationRecord) -> None:
        """Insert immutable mutation record."""
        conn = self._get_conn()
        try:
            conn.execute(
                """INSERT INTO doctrine_mutations
                   (mutation_id, timestamp, doctrine_key, mutation_type, origin, author,
                    before_hash, after_hash, before_summary, after_summary, justification,
                    approved_by, rollback_hash, regression_suite_passed)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    record.mutation_id, record.timestamp, record.doctrine_key,
                    record.mutation_type.value, record.origin.value, record.author,
                    record.before_hash, record.after_hash, record.before_summary,
                    record.after_summary, record.justification, record.approved_by,
                    record.rollback_hash, int(record.regression_suite_passed),
                ),
            )
            conn.commit()
        except sqlite3.Error as exc:
            logger.error("Failed to record doctrine mutation: {}", exc)

    def get_mutation_history(self, doctrine_key: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get mutation history for a specific doctrine."""
        conn = self._get_conn()
        try:
            rows = conn.execute(
                "SELECT * FROM doctrine_mutations WHERE doctrine_key = ? ORDER BY timestamp DESC LIMIT ?",
                (doctrine_key, limit),
            ).fetchall()
            return [dict(r) for r in rows]
        except sqlite3.Error:
            return []

    def get_all_mutations(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all recent mutations across all doctrines."""
        conn = self._get_conn()
        try:
            rows = conn.execute(
                "SELECT * FROM doctrine_mutations ORDER BY timestamp DESC LIMIT ?",
                (limit,),
            ).fetchall()
            return [dict(r) for r in rows]
        except sqlite3.Error:
            return []


# ============================================================================
# TELEMETRY SINGLETON
# ============================================================================

class ContractTelemetry:
    """Central telemetry hub for the LG01 Contract Analysis Engine.

    Thread-safe singleton managing all telemetry operations including
    query tracing, performance monitoring, error tracking, and audit logging.
    """

    _instance: Optional["ContractTelemetry"] = None
    _lock = threading.Lock()

    def __new__(cls) -> "ContractTelemetry":
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self) -> None:
        if self._initialized:
            return
        self._initialized = True
        self._start_time = time.time()

        self._audit_db = AuditDatabase(AUDIT_DB)
        self._mutation_db = MutationDatabase(MUTATION_DB)

        self._latencies: List[float] = []
        self._error_timestamps: List[float] = []
        self._query_timestamps: List[float] = []
        self._max_history = 1000

        self._doctrine_hits: int = 0
        self._doctrine_misses: int = 0
        self._cache_hits: int = 0
        self._cache_misses: int = 0
        self._active_queries: int = 0
        self._total_queries: int = 0
        self._total_clauses_extracted: int = 0
        self._total_risk_assessments: int = 0
        self._total_compliance_checks: int = 0

        self._perf_lock = threading.Lock()

        logger.info("LG01 ContractTelemetry initialized. Audit DB: {}, Mutation DB: {}", AUDIT_DB, MUTATION_DB)

    @property
    def uptime_seconds(self) -> float:
        """Seconds since telemetry initialization."""
        return time.time() - self._start_time

    def query_start(self) -> None:
        """Mark a query as started."""
        with self._perf_lock:
            self._active_queries += 1

    def query_end(self) -> None:
        """Mark a query as completed."""
        with self._perf_lock:
            self._active_queries = max(0, self._active_queries - 1)

    def record_query(self, latency_ms: float, doctrine_hit: bool) -> None:
        """Record query completion metrics."""
        now = time.time()
        with self._perf_lock:
            self._latencies.append(latency_ms)
            if len(self._latencies) > self._max_history:
                self._latencies = self._latencies[-self._max_history:]
            self._query_timestamps.append(now)
            cutoff = now - 3600
            self._query_timestamps = [t for t in self._query_timestamps if t > cutoff]
            self._total_queries += 1
            if doctrine_hit:
                self._doctrine_hits += 1
            else:
                self._doctrine_misses += 1

    def record_cache_access(self, hit: bool) -> None:
        """Record cache hit/miss."""
        with self._perf_lock:
            if hit:
                self._cache_hits += 1
            else:
                self._cache_misses += 1

    def record_clause_extraction(self, count: int = 1) -> None:
        """Record clause extractions."""
        with self._perf_lock:
            self._total_clauses_extracted += count

    def record_risk_assessment(self, count: int = 1) -> None:
        """Record risk assessments."""
        with self._perf_lock:
            self._total_risk_assessments += count

    def record_compliance_check(self, count: int = 1) -> None:
        """Record compliance checks."""
        with self._perf_lock:
            self._total_compliance_checks += count

    def record_error(self, error_msg: str) -> None:
        """Record an error timestamp."""
        with self._perf_lock:
            self._error_timestamps.append(time.time())
            cutoff = time.time() - 86400
            self._error_timestamps = [t for t in self._error_timestamps if t > cutoff]

    def get_latency_stats(self) -> Dict[str, float]:
        """Get latency statistics."""
        with self._perf_lock:
            if not self._latencies:
                return {"avg_ms": 0.0, "p50_ms": 0.0, "p95_ms": 0.0, "p99_ms": 0.0, "max_ms": 0.0}
            sorted_lat = sorted(self._latencies)
            count = len(sorted_lat)
            return {
                "avg_ms": round(sum(sorted_lat) / count, 2),
                "p50_ms": round(sorted_lat[int(count * 0.50)], 2),
                "p95_ms": round(sorted_lat[min(int(count * 0.95), count - 1)], 2),
                "p99_ms": round(sorted_lat[min(int(count * 0.99), count - 1)], 2),
                "max_ms": round(sorted_lat[-1], 2),
            }

    def get_error_stats(self) -> Dict[str, Any]:
        """Get error rate statistics."""
        now = time.time()
        with self._perf_lock:
            last_hour = sum(1 for t in self._error_timestamps if t > now - 3600)
            last_24h = len(self._error_timestamps)
            return {
                "last_hour": last_hour,
                "last_24h": last_24h,
                "error_rate": round(last_hour / max(1, self.queries_last_hour), 4),
            }

    @property
    def queries_last_hour(self) -> int:
        """Queries in the last hour."""
        cutoff = time.time() - 3600
        with self._perf_lock:
            return sum(1 for t in self._query_timestamps if t > cutoff)

    @property
    def queries_last_minute(self) -> int:
        """Queries in the last minute."""
        cutoff = time.time() - 60
        with self._perf_lock:
            return sum(1 for t in self._query_timestamps if t > cutoff)

    @property
    def doctrine_hit_rate(self) -> float:
        """Doctrine cache hit rate."""
        with self._perf_lock:
            total = self._doctrine_hits + self._doctrine_misses
            if total == 0:
                return 1.0
            return round(self._doctrine_hits / total, 3)

    @property
    def cache_hit_rate(self) -> float:
        """General cache hit rate."""
        with self._perf_lock:
            total = self._cache_hits + self._cache_misses
            if total == 0:
                return 0.0
            return round(self._cache_hits / total, 3)

    def get_performance_snapshot(self) -> PerformanceSnapshot:
        """Generate complete performance snapshot."""
        latency = self.get_latency_stats()
        errors = self.get_error_stats()

        cpu_pct = 0.0
        mem_mb = 0.0
        mem_pct = 0.0
        if PSUTIL_AVAILABLE:
            try:
                process = psutil.Process()
                cpu_pct = process.cpu_percent(interval=0.1)
                mem_info = process.memory_info()
                mem_mb = round(mem_info.rss / (1024 * 1024), 2)
                mem_pct = round(process.memory_percent(), 2)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        return PerformanceSnapshot(
            timestamp=datetime.now(timezone.utc).isoformat(),
            queries_total=self._total_queries,
            queries_last_hour=self.queries_last_hour,
            queries_last_minute=self.queries_last_minute,
            avg_latency_ms=latency["avg_ms"],
            p50_latency_ms=latency["p50_ms"],
            p95_latency_ms=latency["p95_ms"],
            p99_latency_ms=latency["p99_ms"],
            max_latency_ms=latency["max_ms"],
            doctrine_hit_rate=self.doctrine_hit_rate,
            cache_hit_rate=self.cache_hit_rate,
            clauses_extracted_total=self._total_clauses_extracted,
            risk_assessments_total=self._total_risk_assessments,
            compliance_checks_total=self._total_compliance_checks,
            errors_last_hour=errors["last_hour"],
            error_rate=errors["error_rate"],
            cpu_percent=cpu_pct,
            memory_mb=mem_mb,
            memory_percent=mem_pct,
            active_queries=self._active_queries,
            uptime_seconds=self.uptime_seconds,
        )

    # --- Audit DB pass-through ---

    def audit_query(self, trace: QueryTrace, determinism_hash: Optional[str] = None) -> None:
        """Record query to audit database and JSONL log."""
        self._audit_db.record_query(trace, determinism_hash)
        _append_jsonl(QUERY_LOG, trace.to_dict())

    def audit_clause_extraction(self, record: ClauseExtractionRecord) -> None:
        """Record clause extraction to audit database and JSONL log."""
        self._audit_db.record_clause_extraction(record)
        _append_jsonl(CLAUSE_EXTRACTION_LOG, record.to_dict())

    def audit_risk_assessment(self, record: RiskAssessmentRecord) -> None:
        """Record risk assessment to audit database and JSONL log."""
        self._audit_db.record_risk_assessment(record)
        _append_jsonl(RISK_ASSESSMENT_LOG, record.to_dict())

    def audit_compliance_check(self, record: ComplianceCheckRecord) -> None:
        """Record compliance check to audit database and JSONL log."""
        self._audit_db.record_compliance_check(record)
        _append_jsonl(COMPLIANCE_CHECK_LOG, record.to_dict())

    def audit_error(self, record: ErrorRecord) -> None:
        """Record error to audit database and JSONL log."""
        self._audit_db.record_error(record)
        _append_jsonl(ERROR_LOG, record.to_dict())
        self.record_error(record.message)

    def audit_reasoning(self, snapshot: ReasoningSnapshot) -> None:
        """Record reasoning snapshot to JSONL log."""
        _append_jsonl(REASONING_LOG, snapshot.to_dict())

    def log_performance(self) -> None:
        """Write current performance snapshot to JSONL log."""
        snap = self.get_performance_snapshot()
        _append_jsonl(PERFORMANCE_LOG, snap.to_dict())

    # --- Mutation DB pass-through ---

    def record_doctrine_mutation(self, record: DoctrineMutationRecord) -> None:
        """Record a doctrine mutation to the immutable mutation log."""
        self._mutation_db.record_mutation(record)

    def get_mutation_history(self, doctrine_key: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get mutation history for a doctrine key."""
        return self._mutation_db.get_mutation_history(doctrine_key, limit)

    # --- Stats pass-through ---

    def get_clause_stats(self) -> Dict[str, int]:
        """Get clause extraction statistics."""
        return self._audit_db.get_clause_stats()

    def get_risk_distribution(self) -> Dict[str, int]:
        """Get risk level distribution."""
        return self._audit_db.get_risk_distribution()

    def get_recent_errors(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recent errors."""
        return self._audit_db.get_recent_errors(limit)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def _append_jsonl(path: Path, data: Dict[str, Any]) -> None:
    """Append a JSON line to a JSONL file. Thread-safe via atomic write."""
    try:
        line = json.dumps(data, default=str, ensure_ascii=False) + "\n"
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(line)
    except OSError as exc:
        logger.error("Failed to write JSONL {}: {}", path, exc)


def get_telemetry() -> ContractTelemetry:
    """Get the global telemetry singleton."""
    return ContractTelemetry()


def trace_query(
    query_text: str,
    query_type: str,
    mode: str,
    contract_type: Optional[str] = None,
    contract_id: Optional[str] = None,
    session_id: Optional[str] = None,
) -> str:
    """Start tracing a query. Returns trace_id."""
    trace_id = str(uuid.uuid4())
    telemetry = get_telemetry()
    telemetry.query_start()
    logger.debug("Query trace started: {} | type={} mode={}", trace_id, query_type, mode)
    return trace_id


def complete_trace(
    trace_id: str,
    query_text: str,
    query_type: str,
    mode: str,
    contract_type: Optional[str],
    doctrine_matched: bool,
    doctrine_id: Optional[str],
    doctrine_topic: Optional[str],
    confidence_score: float,
    response_layer: ResponseLayer,
    latency_ms: float,
    doctrine_lookup_ms: float,
    semantic_lookup_ms: float,
    clauses_extracted: int = 0,
    risk_scores_computed: int = 0,
    citations_count: int = 0,
    response_length: int = 0,
    total_tokens: int = 0,
    contract_id: Optional[str] = None,
    session_id: Optional[str] = None,
    determinism_hash: Optional[str] = None,
) -> None:
    """Complete a query trace and log all metrics."""
    telemetry = get_telemetry()
    telemetry.query_end()
    telemetry.record_query(latency_ms, doctrine_matched)

    trace = QueryTrace(
        trace_id=trace_id,
        timestamp=datetime.now(timezone.utc).isoformat(),
        query_text=query_text[:500],
        query_type=query_type,
        contract_type=contract_type,
        mode=mode,
        doctrine_matched=doctrine_matched,
        doctrine_id=doctrine_id,
        doctrine_topic=doctrine_topic,
        confidence_score=confidence_score,
        response_layer=response_layer.value,
        semantic_triggered=response_layer == ResponseLayer.SEMANTIC,
        deep_analysis_triggered=response_layer == ResponseLayer.DEEP_ANALYSIS,
        latency_ms=latency_ms,
        doctrine_lookup_ms=doctrine_lookup_ms,
        semantic_lookup_ms=semantic_lookup_ms,
        total_tokens=total_tokens,
        response_length=response_length,
        citations_count=citations_count,
        clauses_extracted=clauses_extracted,
        risk_scores_computed=risk_scores_computed,
        contract_id=contract_id,
        session_id=session_id,
    )
    telemetry.audit_query(trace, determinism_hash)
    logger.info(
        "Query complete: {} | layer={} latency={:.1f}ms doctrine_hit={} clauses={} risks={}",
        trace_id, response_layer.value, latency_ms, doctrine_matched,
        clauses_extracted, risk_scores_computed,
    )


def log_error(
    domain: ErrorDomain,
    message: str,
    severity: ErrorSeverity = ErrorSeverity.ERROR,
    trace_id: Optional[str] = None,
    contract_id: Optional[str] = None,
    clause_type: Optional[str] = None,
    exc: Optional[Exception] = None,
) -> str:
    """Log a structured error. Returns error_id."""
    error_id = str(uuid.uuid4())
    stack = traceback.format_exc() if exc else None

    record = ErrorRecord(
        error_id=error_id,
        timestamp=datetime.now(timezone.utc).isoformat(),
        severity=severity,
        domain=domain,
        message=message[:2000],
        stack_trace=stack,
        trace_id=trace_id,
        contract_id=contract_id,
        clause_type=clause_type,
    )

    telemetry = get_telemetry()
    telemetry.audit_error(record)

    if severity in (ErrorSeverity.ERROR, ErrorSeverity.CRITICAL):
        logger.error("LG01 Error [{}] {}: {}", domain.value, error_id, message)
    else:
        logger.warning("LG01 Warning [{}] {}: {}", domain.value, error_id, message)

    return error_id


def record_doctrine_mutation(
    doctrine_key: str,
    mutation_type: MutationType,
    origin: MutationOrigin,
    author: str,
    after_hash: str,
    after_summary: str,
    justification: str,
    before_hash: Optional[str] = None,
    before_summary: Optional[str] = None,
    approved_by: Optional[str] = None,
    regression_passed: bool = False,
) -> str:
    """Record a doctrine mutation. Returns mutation_id."""
    mutation_id = str(uuid.uuid4())
    record = DoctrineMutationRecord(
        mutation_id=mutation_id,
        timestamp=datetime.now(timezone.utc).isoformat(),
        doctrine_key=doctrine_key,
        mutation_type=mutation_type,
        origin=origin,
        author=author,
        before_hash=before_hash,
        after_hash=after_hash,
        before_summary=before_summary,
        after_summary=after_summary,
        justification=justification,
        approved_by=approved_by,
        regression_suite_passed=regression_passed,
    )

    telemetry = get_telemetry()
    telemetry.record_doctrine_mutation(record)
    logger.info("Doctrine mutation recorded: {} | key={} type={}", mutation_id, doctrine_key, mutation_type.value)
    return mutation_id
