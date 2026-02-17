"""
LG05 LITIGATION RISK ENGINE - Professional Telemetry & Logging
Institutional-grade observability infrastructure for litigation risk assessment
audit, compliance verification, and operational monitoring.

Components:
    1. QueryTracer - Every litigation query logged with full context
    2. ReasoningSnapshot - Reproducible risk assessment paths for audit replay
    3. DoctrineMutationLog - Immutable changelog for doctrine modifications
    4. ErrorSpine - Centralized error collection with stack traces
    5. PerformanceTelemetry - Real-time performance metrics
    6. RiskAssessmentLog - Risk scoring audit trail
    7. DamagesEstimationLog - Damages calculation audit trail
    8. JurisdictionAnalysisLog - Jurisdiction assessment history

Engine: LG05 Litigation Risk Engine
Tier: 1 (LEGAL)
Mode: DET (Deterministic)
Port: 8395
Author: ECHO OMEGA PRIME
Authority: 5.0
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

TELEMETRY_DIR = Path("O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/LG05_litigation_risk/telemetry")
TELEMETRY_DIR.mkdir(parents=True, exist_ok=True)

QUERY_LOG = TELEMETRY_DIR / "query_traces.jsonl"
REASONING_LOG = TELEMETRY_DIR / "reasoning_snapshots.jsonl"
ERROR_LOG = TELEMETRY_DIR / "error_spine.jsonl"
PERFORMANCE_LOG = TELEMETRY_DIR / "performance_metrics.jsonl"
RISK_ASSESSMENT_LOG = TELEMETRY_DIR / "risk_assessments.jsonl"
DAMAGES_ESTIMATION_LOG = TELEMETRY_DIR / "damages_estimations.jsonl"
JURISDICTION_LOG = TELEMETRY_DIR / "jurisdiction_analyses.jsonl"

AUDIT_DB = TELEMETRY_DIR / "audit_trail.db"
MUTATION_DB = TELEMETRY_DIR / "doctrine_mutations.db"

logger.add(
    TELEMETRY_DIR / "lg05_telemetry_{time}.log",
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
    DEEP = "deep"
    FALLBACK = "fallback"


class ErrorDomain(str, Enum):
    """Domain where error originated."""
    DOCTRINE_MATCH = "doctrine_match"
    SEMANTIC_SEARCH = "semantic_search"
    RISK_SCORING = "risk_scoring"
    DAMAGES_CALC = "damages_calc"
    JURISDICTION = "jurisdiction"
    SETTLEMENT = "settlement"
    PRECEDENT = "precedent"
    INPUT_VALIDATION = "input_validation"
    AUTHORITY_GATE = "authority_gate"
    SERIALIZATION = "serialization"
    DATABASE = "database"
    UNKNOWN = "unknown"


class MutationType(str, Enum):
    """Type of doctrine mutation."""
    ADD = "add"
    MODIFY = "modify"
    DEPRECATE = "deprecate"
    REWEIGHT = "reweight"
    MERGE = "merge"


class MutationOrigin(str, Enum):
    """Origin of the mutation."""
    MANUAL = "manual"
    SYSTEM = "system"
    DRIFT_CORRECTION = "drift_correction"
    AUTHORITY_UPDATE = "authority_update"
    CASE_LAW_UPDATE = "case_law_update"


class RiskLevel(str, Enum):
    """Risk level classification for telemetry."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NEGLIGIBLE = "negligible"


class LitigationCategory(str, Enum):
    """Litigation category for telemetry classification."""
    CONTRACT = "contract"
    TORT = "tort"
    EMPLOYMENT = "employment"
    SECURITIES = "securities"
    ANTITRUST = "antitrust"
    IP = "intellectual_property"
    ENVIRONMENTAL = "environmental"
    PRODUCTS_LIABILITY = "products_liability"
    INSURANCE = "insurance"
    REGULATORY = "regulatory"
    GENERAL = "general"


# ============================================================================
# DATA RECORDS
# ============================================================================

@dataclass
class QueryTrace:
    """Complete trace of a litigation risk query."""
    trace_id: str
    query_text: str
    query_hash: str
    litigation_type: str
    jurisdiction: str
    response_mode: str
    response_layer: str
    doctrine_keys_matched: List[str]
    risk_score: float
    confidence: float
    latency_ms: float
    timestamp: str
    session_id: str
    determinism_hash: str
    authority_level: float
    error: Optional[str] = None
    warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)


@dataclass
class ReasoningSnapshot:
    """Snapshot of the reasoning path for audit replay."""
    snapshot_id: str
    trace_id: str
    step_number: int
    step_name: str
    input_state: Dict[str, Any]
    output_state: Dict[str, Any]
    duration_ms: float
    doctrine_applied: Optional[str]
    confidence_delta: float
    timestamp: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)


@dataclass
class DoctrineMutation:
    """Record of a doctrine modification."""
    mutation_id: str
    doctrine_key: str
    mutation_type: str
    origin: str
    before_hash: str
    after_hash: str
    justification: str
    approved_by: str
    timestamp: str
    rollback_possible: bool = True

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)


@dataclass
class ErrorRecord:
    """Structured error record."""
    error_id: str
    domain: str
    severity: str
    message: str
    stack_trace: str
    trace_id: Optional[str]
    query_context: Optional[str]
    resolution: Optional[str]
    timestamp: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)


@dataclass
class RiskAssessmentRecord:
    """Record of a risk assessment calculation."""
    assessment_id: str
    trace_id: str
    litigation_type: str
    case_merit_score: float
    damages_exposure_score: float
    jurisdiction_risk_score: float
    discovery_cost_score: float
    settlement_pressure_score: float
    regulatory_escalation_score: float
    composite_risk_score: float
    risk_level: str
    confidence: float
    factors_evaluated: int
    timestamp: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)


@dataclass
class DamagesEstimationRecord:
    """Record of a damages estimation calculation."""
    estimation_id: str
    trace_id: str
    litigation_type: str
    compensatory_low: float
    compensatory_high: float
    consequential_low: float
    consequential_high: float
    punitive_low: float
    punitive_high: float
    statutory_low: float
    statutory_high: float
    attorneys_fees_estimate: float
    total_exposure_low: float
    total_exposure_high: float
    methodology: str
    timestamp: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)


@dataclass
class JurisdictionAnalysisRecord:
    """Record of a jurisdiction analysis."""
    analysis_id: str
    trace_id: str
    jurisdiction: str
    venue_favorability: float
    judge_profile_available: bool
    jury_tendency_score: float
    local_rules_impact: float
    overall_favorability: float
    recommended_venue: Optional[str]
    timestamp: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)


# ============================================================================
# JSONL WRITER (Thread-Safe)
# ============================================================================

class JSONLWriter:
    """Thread-safe JSONL file writer with rotation."""

    def __init__(self, file_path: Path, max_size_mb: int = 100) -> None:
        self._path = file_path
        self._max_bytes = max_size_mb * 1024 * 1024
        self._lock = threading.Lock()
        self._write_count = 0

    def write(self, record: Dict[str, Any]) -> None:
        """Write a record to the JSONL file."""
        with self._lock:
            self._rotate_if_needed()
            try:
                line = json.dumps(record, default=str, separators=(",", ":"))
                with open(self._path, "a", encoding="utf-8") as fh:
                    fh.write(line + "\n")
                self._write_count += 1
            except Exception as exc:
                logger.error(f"JSONL write failed for {self._path.name}: {exc}")

    def _rotate_if_needed(self) -> None:
        """Rotate log file if it exceeds max size."""
        if self._path.exists() and self._path.stat().st_size > self._max_bytes:
            ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
            rotated = self._path.with_suffix(f".{ts}.jsonl")
            try:
                self._path.rename(rotated)
                logger.info(f"Rotated {self._path.name} -> {rotated.name}")
            except OSError as exc:
                logger.warning(f"Rotation failed for {self._path.name}: {exc}")

    @property
    def write_count(self) -> int:
        """Total records written since initialization."""
        return self._write_count

    def read_recent(self, count: int = 50) -> List[Dict[str, Any]]:
        """Read the most recent N records."""
        records: List[Dict[str, Any]] = []
        if not self._path.exists():
            return records
        try:
            with open(self._path, "r", encoding="utf-8") as fh:
                lines = fh.readlines()
            for line in lines[-count:]:
                stripped = line.strip()
                if stripped:
                    records.append(json.loads(stripped))
        except Exception as exc:
            logger.error(f"JSONL read failed for {self._path.name}: {exc}")
        return records


# ============================================================================
# AUDIT DATABASE
# ============================================================================

class AuditDatabase:
    """SQLite-backed audit trail for litigation risk assessments."""

    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path
        self._lock = threading.Lock()
        self._init_db()

    def _init_db(self) -> None:
        """Initialize the audit database schema."""
        with self._get_conn() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS audit_trail (
                    id TEXT PRIMARY KEY,
                    trace_id TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    event_data TEXT NOT NULL,
                    determinism_hash TEXT NOT NULL,
                    authority_level REAL NOT NULL,
                    timestamp TEXT NOT NULL,
                    session_id TEXT
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_audit_trace ON audit_trail(trace_id)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_audit_type ON audit_trail(event_type)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_audit_ts ON audit_trail(timestamp)
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS doctrine_mutations (
                    id TEXT PRIMARY KEY,
                    doctrine_key TEXT NOT NULL,
                    mutation_type TEXT NOT NULL,
                    origin TEXT NOT NULL,
                    before_hash TEXT NOT NULL,
                    after_hash TEXT NOT NULL,
                    justification TEXT NOT NULL,
                    approved_by TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    rollback_possible INTEGER DEFAULT 1
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_mutation_key ON doctrine_mutations(doctrine_key)
            """)
            conn.commit()

    @contextmanager
    def _get_conn(self):
        """Get a database connection with proper cleanup."""
        conn = sqlite3.connect(str(self._db_path), timeout=10)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        try:
            yield conn
        finally:
            conn.close()

    def record_event(
        self,
        trace_id: str,
        event_type: str,
        event_data: Dict[str, Any],
        determinism_hash: str,
        authority_level: float,
        session_id: Optional[str] = None,
    ) -> str:
        """Record an audit event."""
        event_id = str(uuid.uuid4())
        ts = datetime.now(timezone.utc).isoformat()
        with self._lock:
            try:
                with self._get_conn() as conn:
                    conn.execute(
                        """INSERT INTO audit_trail
                        (id, trace_id, event_type, event_data, determinism_hash,
                         authority_level, timestamp, session_id)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                        (
                            event_id,
                            trace_id,
                            event_type,
                            json.dumps(event_data, default=str),
                            determinism_hash,
                            authority_level,
                            ts,
                            session_id,
                        ),
                    )
                    conn.commit()
            except Exception as exc:
                logger.error(f"Audit record failed: {exc}")
        return event_id

    def record_mutation(self, mutation: DoctrineMutation) -> None:
        """Record a doctrine mutation."""
        with self._lock:
            try:
                with self._get_conn() as conn:
                    conn.execute(
                        """INSERT INTO doctrine_mutations
                        (id, doctrine_key, mutation_type, origin, before_hash,
                         after_hash, justification, approved_by, timestamp, rollback_possible)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (
                            mutation.mutation_id,
                            mutation.doctrine_key,
                            mutation.mutation_type,
                            mutation.origin,
                            mutation.before_hash,
                            mutation.after_hash,
                            mutation.justification,
                            mutation.approved_by,
                            mutation.timestamp,
                            1 if mutation.rollback_possible else 0,
                        ),
                    )
                    conn.commit()
            except Exception as exc:
                logger.error(f"Mutation record failed: {exc}")

    def get_audit_trail(
        self,
        trace_id: Optional[str] = None,
        event_type: Optional[str] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """Retrieve audit trail records."""
        conditions: List[str] = []
        params: List[Any] = []
        if trace_id:
            conditions.append("trace_id = ?")
            params.append(trace_id)
        if event_type:
            conditions.append("event_type = ?")
            params.append(event_type)
        where_clause = " AND ".join(conditions) if conditions else "1=1"
        params.append(limit)
        records: List[Dict[str, Any]] = []
        try:
            with self._get_conn() as conn:
                cursor = conn.execute(
                    f"""SELECT id, trace_id, event_type, event_data,
                    determinism_hash, authority_level, timestamp, session_id
                    FROM audit_trail WHERE {where_clause}
                    ORDER BY timestamp DESC LIMIT ?""",
                    params,
                )
                for row in cursor.fetchall():
                    records.append({
                        "id": row[0],
                        "trace_id": row[1],
                        "event_type": row[2],
                        "event_data": json.loads(row[3]),
                        "determinism_hash": row[4],
                        "authority_level": row[5],
                        "timestamp": row[6],
                        "session_id": row[7],
                    })
        except Exception as exc:
            logger.error(f"Audit trail query failed: {exc}")
        return records

    def get_mutation_history(
        self, doctrine_key: Optional[str] = None, limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Retrieve doctrine mutation history."""
        records: List[Dict[str, Any]] = []
        try:
            with self._get_conn() as conn:
                if doctrine_key:
                    cursor = conn.execute(
                        """SELECT * FROM doctrine_mutations
                        WHERE doctrine_key = ? ORDER BY timestamp DESC LIMIT ?""",
                        (doctrine_key, limit),
                    )
                else:
                    cursor = conn.execute(
                        """SELECT * FROM doctrine_mutations
                        ORDER BY timestamp DESC LIMIT ?""",
                        (limit,),
                    )
                for row in cursor.fetchall():
                    records.append({
                        "id": row[0],
                        "doctrine_key": row[1],
                        "mutation_type": row[2],
                        "origin": row[3],
                        "before_hash": row[4],
                        "after_hash": row[5],
                        "justification": row[6],
                        "approved_by": row[7],
                        "timestamp": row[8],
                        "rollback_possible": bool(row[9]),
                    })
        except Exception as exc:
            logger.error(f"Mutation history query failed: {exc}")
        return records

    def count_events(self) -> int:
        """Count total audit events."""
        try:
            with self._get_conn() as conn:
                cursor = conn.execute("SELECT COUNT(*) FROM audit_trail")
                row = cursor.fetchone()
                return row[0] if row else 0
        except Exception:
            return 0


# ============================================================================
# PERFORMANCE TELEMETRY
# ============================================================================

class PerformanceTelemetry:
    """Real-time performance metrics collection."""

    def __init__(self) -> None:
        self._latencies: List[float] = []
        self._query_timestamps: List[float] = []
        self._error_timestamps: List[float] = []
        self._layer_counts: Dict[str, int] = {
            "doctrine": 0,
            "semantic": 0,
            "deep": 0,
            "fallback": 0,
        }
        self._litigation_type_counts: Dict[str, int] = {}
        self._lock = threading.Lock()
        self._max_samples = 500

    def record_query(
        self,
        latency_ms: float,
        layer: str,
        litigation_type: str,
    ) -> None:
        """Record a completed query."""
        with self._lock:
            now = time.time()
            self._latencies.append(latency_ms)
            if len(self._latencies) > self._max_samples:
                self._latencies.pop(0)
            self._query_timestamps.append(now)
            cutoff = now - 3600
            self._query_timestamps = [t for t in self._query_timestamps if t > cutoff]
            if layer in self._layer_counts:
                self._layer_counts[layer] += 1
            self._litigation_type_counts[litigation_type] = (
                self._litigation_type_counts.get(litigation_type, 0) + 1
            )

    def record_error(self) -> None:
        """Record an error occurrence."""
        with self._lock:
            now = time.time()
            self._error_timestamps.append(now)
            cutoff = now - 86400
            self._error_timestamps = [t for t in self._error_timestamps if t > cutoff]

    def get_latency_stats(self) -> Dict[str, float]:
        """Get latency statistics."""
        with self._lock:
            if not self._latencies:
                return {"avg_ms": 0.0, "p50_ms": 0.0, "p95_ms": 0.0, "p99_ms": 0.0, "max_ms": 0.0}
            sorted_lat = sorted(self._latencies)
            n = len(sorted_lat)
            return {
                "avg_ms": round(sum(sorted_lat) / n, 2),
                "p50_ms": round(sorted_lat[n // 2], 2),
                "p95_ms": round(sorted_lat[min(int(n * 0.95), n - 1)], 2),
                "p99_ms": round(sorted_lat[min(int(n * 0.99), n - 1)], 2),
                "max_ms": round(sorted_lat[-1], 2),
            }

    def get_throughput(self) -> Dict[str, float]:
        """Get throughput metrics."""
        with self._lock:
            now = time.time()
            last_minute = sum(1 for t in self._query_timestamps if t > now - 60)
            last_hour = len(self._query_timestamps)
            errors_24h = len(self._error_timestamps)
            total_queries = sum(self._layer_counts.values())
            error_rate = errors_24h / max(total_queries, 1)
            return {
                "queries_per_minute": round(last_minute, 1),
                "queries_per_hour": last_hour,
                "total_queries": total_queries,
                "errors_24h": errors_24h,
                "error_rate": round(error_rate, 4),
            }

    def get_layer_distribution(self) -> Dict[str, Any]:
        """Get response layer distribution."""
        with self._lock:
            total = sum(self._layer_counts.values())
            if total == 0:
                return {"total": 0, "layers": self._layer_counts.copy()}
            percentages = {
                k: round(v / total * 100, 1) for k, v in self._layer_counts.items()
            }
            return {
                "total": total,
                "layers": self._layer_counts.copy(),
                "percentages": percentages,
            }

    def get_litigation_type_distribution(self) -> Dict[str, int]:
        """Get litigation type distribution."""
        with self._lock:
            return self._litigation_type_counts.copy()

    def get_system_metrics(self) -> Dict[str, Any]:
        """Get system-level metrics."""
        metrics: Dict[str, Any] = {"psutil_available": PSUTIL_AVAILABLE}
        if PSUTIL_AVAILABLE:
            try:
                metrics["cpu_percent"] = psutil.cpu_percent(interval=0.1)
                mem = psutil.virtual_memory()
                metrics["memory_percent"] = mem.percent
                metrics["memory_available_mb"] = round(mem.available / 1024 / 1024, 1)
            except Exception:
                metrics["cpu_percent"] = -1.0
                metrics["memory_percent"] = -1.0
        return metrics

    def get_full_report(self) -> Dict[str, Any]:
        """Get comprehensive performance report."""
        return {
            "latency": self.get_latency_stats(),
            "throughput": self.get_throughput(),
            "layer_distribution": self.get_layer_distribution(),
            "litigation_types": self.get_litigation_type_distribution(),
            "system": self.get_system_metrics(),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


# ============================================================================
# SINGLETON TELEMETRY MANAGER
# ============================================================================

class TelemetryManager:
    """Central telemetry manager singleton."""

    _instance: Optional["TelemetryManager"] = None
    _lock = threading.Lock()

    def __init__(self) -> None:
        self.query_writer = JSONLWriter(QUERY_LOG)
        self.reasoning_writer = JSONLWriter(REASONING_LOG)
        self.error_writer = JSONLWriter(ERROR_LOG)
        self.performance_writer = JSONLWriter(PERFORMANCE_LOG)
        self.risk_writer = JSONLWriter(RISK_ASSESSMENT_LOG)
        self.damages_writer = JSONLWriter(DAMAGES_ESTIMATION_LOG)
        self.jurisdiction_writer = JSONLWriter(JURISDICTION_LOG)
        self.audit_db = AuditDatabase(AUDIT_DB)
        self.performance = PerformanceTelemetry()
        self._session_id = str(uuid.uuid4())
        self._start_time = time.time()
        logger.info(f"TelemetryManager initialized | session={self._session_id}")

    @classmethod
    def get_instance(cls) -> "TelemetryManager":
        """Get or create the singleton instance."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    @property
    def session_id(self) -> str:
        """Current session identifier."""
        return self._session_id

    @property
    def uptime_seconds(self) -> float:
        """Seconds since initialization."""
        return time.time() - self._start_time


# ============================================================================
# MODULE-LEVEL CONVENIENCE FUNCTIONS
# ============================================================================

def get_telemetry() -> TelemetryManager:
    """Get the telemetry manager singleton."""
    return TelemetryManager.get_instance()


def trace_query(
    query_text: str,
    litigation_type: str,
    jurisdiction: str,
    response_mode: str,
    authority_level: float,
) -> Tuple[str, float]:
    """Start tracing a query. Returns (trace_id, start_time)."""
    trace_id = str(uuid.uuid4())
    start_time = time.time()
    logger.info(
        f"Query trace started | trace={trace_id} | type={litigation_type} | "
        f"jurisdiction={jurisdiction} | mode={response_mode}"
    )
    return trace_id, start_time


def complete_trace(
    trace_id: str,
    start_time: float,
    query_text: str,
    litigation_type: str,
    jurisdiction: str,
    response_mode: str,
    response_layer: str,
    doctrine_keys: List[str],
    risk_score: float,
    confidence: float,
    determinism_hash: str,
    authority_level: float,
    error: Optional[str] = None,
    warnings: Optional[List[str]] = None,
) -> QueryTrace:
    """Complete a query trace and persist it."""
    latency_ms = (time.time() - start_time) * 1000
    tm = get_telemetry()

    query_hash = hashlib.sha256(query_text.encode("utf-8")).hexdigest()[:16]
    trace = QueryTrace(
        trace_id=trace_id,
        query_text=query_text[:500],
        query_hash=query_hash,
        litigation_type=litigation_type,
        jurisdiction=jurisdiction,
        response_mode=response_mode,
        response_layer=response_layer,
        doctrine_keys_matched=doctrine_keys,
        risk_score=risk_score,
        confidence=confidence,
        latency_ms=round(latency_ms, 2),
        timestamp=datetime.now(timezone.utc).isoformat(),
        session_id=tm.session_id,
        determinism_hash=determinism_hash,
        authority_level=authority_level,
        error=error,
        warnings=warnings or [],
    )

    tm.query_writer.write(trace.to_dict())
    tm.performance.record_query(latency_ms, response_layer, litigation_type)
    if error:
        tm.performance.record_error()

    tm.audit_db.record_event(
        trace_id=trace_id,
        event_type="query_complete",
        event_data=trace.to_dict(),
        determinism_hash=determinism_hash,
        authority_level=authority_level,
        session_id=tm.session_id,
    )

    logger.info(
        f"Query trace complete | trace={trace_id} | latency={latency_ms:.1f}ms | "
        f"layer={response_layer} | risk={risk_score:.2f} | confidence={confidence:.2f}"
    )
    return trace


def log_error(
    domain: ErrorDomain,
    message: str,
    trace_id: Optional[str] = None,
    query_context: Optional[str] = None,
    severity: str = "HIGH",
    exc: Optional[Exception] = None,
) -> str:
    """Log an error with full context."""
    error_id = str(uuid.uuid4())
    stack_trace = traceback.format_exc() if exc else ""

    record = ErrorRecord(
        error_id=error_id,
        domain=domain.value,
        severity=severity,
        message=message[:1000],
        stack_trace=stack_trace[:2000],
        trace_id=trace_id,
        query_context=query_context[:500] if query_context else None,
        resolution=None,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )

    tm = get_telemetry()
    tm.error_writer.write(record.to_dict())
    tm.performance.record_error()

    logger.error(
        f"Error logged | id={error_id} | domain={domain.value} | "
        f"severity={severity} | trace={trace_id} | msg={message[:200]}"
    )
    return error_id


def record_risk_assessment(
    trace_id: str,
    litigation_type: str,
    merit_score: float,
    damages_score: float,
    jurisdiction_score: float,
    discovery_score: float,
    settlement_score: float,
    regulatory_score: float,
    composite_score: float,
    risk_level: str,
    confidence: float,
    factors_evaluated: int,
) -> str:
    """Record a risk assessment for audit."""
    assessment_id = str(uuid.uuid4())
    record = RiskAssessmentRecord(
        assessment_id=assessment_id,
        trace_id=trace_id,
        litigation_type=litigation_type,
        case_merit_score=merit_score,
        damages_exposure_score=damages_score,
        jurisdiction_risk_score=jurisdiction_score,
        discovery_cost_score=discovery_score,
        settlement_pressure_score=settlement_score,
        regulatory_escalation_score=regulatory_score,
        composite_risk_score=composite_score,
        risk_level=risk_level,
        confidence=confidence,
        factors_evaluated=factors_evaluated,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )

    tm = get_telemetry()
    tm.risk_writer.write(record.to_dict())
    return assessment_id


def record_damages_estimation(
    trace_id: str,
    litigation_type: str,
    compensatory: Tuple[float, float],
    consequential: Tuple[float, float],
    punitive: Tuple[float, float],
    statutory: Tuple[float, float],
    attorneys_fees: float,
    total_low: float,
    total_high: float,
    methodology: str,
) -> str:
    """Record a damages estimation for audit."""
    estimation_id = str(uuid.uuid4())
    record = DamagesEstimationRecord(
        estimation_id=estimation_id,
        trace_id=trace_id,
        litigation_type=litigation_type,
        compensatory_low=compensatory[0],
        compensatory_high=compensatory[1],
        consequential_low=consequential[0],
        consequential_high=consequential[1],
        punitive_low=punitive[0],
        punitive_high=punitive[1],
        statutory_low=statutory[0],
        statutory_high=statutory[1],
        attorneys_fees_estimate=attorneys_fees,
        total_exposure_low=total_low,
        total_exposure_high=total_high,
        methodology=methodology,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )

    tm = get_telemetry()
    tm.damages_writer.write(record.to_dict())
    return estimation_id


def record_jurisdiction_analysis(
    trace_id: str,
    jurisdiction: str,
    venue_favorability: float,
    judge_profile_available: bool,
    jury_tendency: float,
    local_rules_impact: float,
    overall_favorability: float,
    recommended_venue: Optional[str] = None,
) -> str:
    """Record a jurisdiction analysis for audit."""
    analysis_id = str(uuid.uuid4())
    record = JurisdictionAnalysisRecord(
        analysis_id=analysis_id,
        trace_id=trace_id,
        jurisdiction=jurisdiction,
        venue_favorability=venue_favorability,
        judge_profile_available=judge_profile_available,
        jury_tendency_score=jury_tendency,
        local_rules_impact=local_rules_impact,
        overall_favorability=overall_favorability,
        recommended_venue=recommended_venue,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )

    tm = get_telemetry()
    tm.jurisdiction_writer.write(record.to_dict())
    return analysis_id


def record_doctrine_mutation(
    doctrine_key: str,
    mutation_type: MutationType,
    origin: MutationOrigin,
    before_hash: str,
    after_hash: str,
    justification: str,
    approved_by: str = "SYSTEM",
) -> str:
    """Record a doctrine mutation."""
    mutation_id = str(uuid.uuid4())
    mutation = DoctrineMutation(
        mutation_id=mutation_id,
        doctrine_key=doctrine_key,
        mutation_type=mutation_type.value,
        origin=origin.value,
        before_hash=before_hash,
        after_hash=after_hash,
        justification=justification,
        approved_by=approved_by,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )

    tm = get_telemetry()
    tm.audit_db.record_mutation(mutation)
    logger.info(
        f"Doctrine mutation | key={doctrine_key} | type={mutation_type.value} | "
        f"origin={origin.value}"
    )
    return mutation_id


def record_reasoning_step(
    trace_id: str,
    step_number: int,
    step_name: str,
    input_state: Dict[str, Any],
    output_state: Dict[str, Any],
    duration_ms: float,
    doctrine_applied: Optional[str] = None,
    confidence_delta: float = 0.0,
) -> str:
    """Record a reasoning step for audit replay."""
    snapshot_id = str(uuid.uuid4())
    snapshot = ReasoningSnapshot(
        snapshot_id=snapshot_id,
        trace_id=trace_id,
        step_number=step_number,
        step_name=step_name,
        input_state=input_state,
        output_state=output_state,
        duration_ms=round(duration_ms, 2),
        doctrine_applied=doctrine_applied,
        confidence_delta=confidence_delta,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )

    tm = get_telemetry()
    tm.reasoning_writer.write(snapshot.to_dict())
    return snapshot_id
