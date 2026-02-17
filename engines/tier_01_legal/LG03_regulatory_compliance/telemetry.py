"""
LG03 REGULATORY COMPLIANCE ENGINE - TELEMETRY MODULE
Production-grade telemetry, metrics collection, and audit trail system.

Provides:
    - Query tracing with unique trace IDs
    - Latency recording per layer (doctrine, retrieval, deep analysis)
    - Error domain classification and tracking
    - Audit trail with append-only JSONL logging
    - Doctrine mutation tracking for governance
    - Risk score distribution metrics
    - Compliance gap analytics
    - Agency-level query distribution tracking

Architecture:
    All telemetry is local, deterministic, and append-only.
    No external dependencies. No probabilistic elements.
    Audit trail is tamper-evident via SHA-256 hash chain.

Author: ECHO OMEGA PRIME
Authority: 11.0 SOVEREIGN
Engine: LG03 Regulatory Compliance
Port: 8393
"""

from __future__ import annotations

import hashlib
import json
import time
import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

from loguru import logger

# ============================================================================
# CONFIGURATION
# ============================================================================

LOG_DIR = Path("O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/LG03_regulatory_compliance/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

AUDIT_LOG_PATH = LOG_DIR / "audit_trail.jsonl"
METRICS_LOG_PATH = LOG_DIR / "metrics.jsonl"
ERROR_LOG_PATH = LOG_DIR / "errors.jsonl"

logger.add(
    LOG_DIR / "lg03_telemetry_{time}.log",
    rotation="50 MB",
    retention="30 days",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {module}:{function}:{line} | {message}",
)


# ============================================================================
# ENUMS
# ============================================================================

class ErrorDomain(str, Enum):
    """Classification of error sources for targeted remediation."""
    DOCTRINE_MATCH = "doctrine_match"
    CFR_PARSE = "cfr_parse"
    RISK_SCORING = "risk_scoring"
    AGENCY_LOOKUP = "agency_lookup"
    DEADLINE_COMPUTE = "deadline_compute"
    PREEMPTION_ANALYSIS = "preemption_analysis"
    INDUSTRY_CLASSIFY = "industry_classify"
    ENFORCEMENT_LOOKUP = "enforcement_lookup"
    COMPLIANCE_GAP = "compliance_gap"
    SERIALIZATION = "serialization"
    INPUT_VALIDATION = "input_validation"
    SEMANTIC_NORMALIZE = "semantic_normalize"
    HASH_COMPUTE = "hash_compute"
    AUDIT_WRITE = "audit_write"
    SEARCH = "search"
    UNKNOWN = "unknown"


class ResponseLayer(str, Enum):
    """Which processing layer produced the response."""
    DOCTRINE = "doctrine"
    RETRIEVAL = "retrieval"
    DEEP_ANALYSIS = "deep_analysis"
    COMPLIANCE_CHECK = "compliance_check"
    GAP_ANALYSIS = "gap_analysis"
    RISK_ASSESSMENT = "risk_assessment"


class MutationType(str, Enum):
    """Type of doctrine mutation for governance tracking."""
    CREATED = "created"
    UPDATED = "updated"
    DEPRECATED = "deprecated"
    SUPERSEDED = "superseded"
    CORRECTED = "corrected"


class MutationOrigin(str, Enum):
    """Source of doctrine mutation for audit purposes."""
    FEDERAL_REGISTER = "federal_register"
    ENFORCEMENT_ACTION = "enforcement_action"
    COURT_DECISION = "court_decision"
    LEGISLATIVE_CHANGE = "legislative_change"
    AGENCY_GUIDANCE = "agency_guidance"
    MANUAL_REVIEW = "manual_review"
    SYSTEM_CORRECTION = "system_correction"


class QueryType(str, Enum):
    """Classification of incoming queries for analytics."""
    COMPLIANCE_CHECK = "compliance_check"
    RISK_ASSESSMENT = "risk_assessment"
    REGULATION_SEARCH = "regulation_search"
    DEADLINE_QUERY = "deadline_query"
    GAP_ANALYSIS = "gap_analysis"
    ENFORCEMENT_LOOKUP = "enforcement_lookup"
    PREEMPTION_CHECK = "preemption_check"
    GENERAL = "general"


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class TraceRecord:
    """Individual query trace for performance and audit tracking."""
    trace_id: str
    query_id: str
    query_type: QueryType
    started_at: float
    completed_at: Optional[float] = None
    layer: Optional[ResponseLayer] = None
    latency_ms: Optional[float] = None
    doctrine_hit: bool = False
    agency: Optional[str] = None
    cfr_title: Optional[str] = None
    risk_score: Optional[float] = None
    error: Optional[str] = None
    error_domain: Optional[ErrorDomain] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def complete(self, layer: ResponseLayer) -> None:
        """Mark trace as complete, compute latency."""
        self.completed_at = time.time()
        self.layer = layer
        self.latency_ms = round((self.completed_at - self.started_at) * 1000, 2)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize for logging."""
        return {
            "trace_id": self.trace_id,
            "query_id": self.query_id,
            "query_type": self.query_type.value,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "layer": self.layer.value if self.layer else None,
            "latency_ms": self.latency_ms,
            "doctrine_hit": self.doctrine_hit,
            "agency": self.agency,
            "cfr_title": self.cfr_title,
            "risk_score": self.risk_score,
            "error": self.error,
            "error_domain": self.error_domain.value if self.error_domain else None,
            "metadata": self.metadata,
        }


@dataclass
class AuditEntry:
    """Tamper-evident audit trail entry with hash chain."""
    entry_id: str
    timestamp: str
    action: str
    actor: str
    resource: str
    details: Dict[str, Any]
    query_id: Optional[str] = None
    determinism_hash: Optional[str] = None
    previous_hash: Optional[str] = None
    entry_hash: Optional[str] = None

    def compute_hash(self, previous_hash: str) -> str:
        """Compute SHA-256 hash for hash chain integrity."""
        self.previous_hash = previous_hash
        content = json.dumps({
            "entry_id": self.entry_id,
            "timestamp": self.timestamp,
            "action": self.action,
            "actor": self.actor,
            "resource": self.resource,
            "details": self.details,
            "query_id": self.query_id,
            "determinism_hash": self.determinism_hash,
            "previous_hash": self.previous_hash,
        }, sort_keys=True, default=str)
        self.entry_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
        return self.entry_hash

    def to_dict(self) -> Dict[str, Any]:
        """Serialize for JSONL storage."""
        return {
            "entry_id": self.entry_id,
            "timestamp": self.timestamp,
            "action": self.action,
            "actor": self.actor,
            "resource": self.resource,
            "details": self.details,
            "query_id": self.query_id,
            "determinism_hash": self.determinism_hash,
            "previous_hash": self.previous_hash,
            "entry_hash": self.entry_hash,
        }


# ============================================================================
# METRICS COLLECTOR
# ============================================================================

class MetricsCollector:
    """Production-grade metrics for LG03 operational awareness.

    Tracks latencies, error rates, doctrine hit rates, agency distribution,
    risk score distributions, and compliance gap analytics.
    No external dependencies. All in-memory with periodic flush to disk.
    """

    def __init__(self) -> None:
        self.latencies: List[float] = []
        self.errors: List[float] = []
        self.queries: List[float] = []
        self.doctrine_hits: int = 0
        self.doctrine_misses: int = 0
        self.last_error: Optional[str] = None
        self.active_queries: int = 0
        self._max_latencies: int = 500

        # Agency distribution tracking
        self.agency_query_counts: Dict[str, int] = defaultdict(int)

        # Risk score distribution
        self.risk_scores: List[float] = []
        self._max_risk_scores: int = 1000

        # Query type distribution
        self.query_type_counts: Dict[str, int] = defaultdict(int)

        # Layer distribution
        self.layer_counts: Dict[str, int] = defaultdict(int)

        # Compliance gap tracking
        self.gap_scores: List[float] = []
        self._max_gap_scores: int = 500

        # Error domain tracking
        self.error_domain_counts: Dict[str, int] = defaultdict(int)

        # CFR title query distribution
        self.cfr_title_counts: Dict[str, int] = defaultdict(int)

        # Per-hour aggregates for trend analysis
        self.hourly_query_counts: Dict[str, int] = defaultdict(int)

    def record_query(self, latency_ms: float, doctrine_hit: bool,
                     query_type: Optional[QueryType] = None,
                     layer: Optional[ResponseLayer] = None,
                     agency: Optional[str] = None,
                     cfr_title: Optional[str] = None) -> None:
        """Record a completed query with full metadata."""
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

        if query_type:
            self.query_type_counts[query_type.value] += 1

        if layer:
            self.layer_counts[layer.value] += 1

        if agency:
            self.agency_query_counts[agency.upper()] += 1

        if cfr_title:
            self.cfr_title_counts[cfr_title] += 1

        hour_key = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H")
        self.hourly_query_counts[hour_key] += 1

    def record_risk_score(self, score: float) -> None:
        """Record a computed risk score for distribution analysis."""
        self.risk_scores.append(score)
        if len(self.risk_scores) > self._max_risk_scores:
            self.risk_scores.pop(0)

    def record_gap_score(self, score: float) -> None:
        """Record a compliance gap score."""
        self.gap_scores.append(score)
        if len(self.gap_scores) > self._max_gap_scores:
            self.gap_scores.pop(0)

    def record_error(self, error_msg: str, domain: Optional[ErrorDomain] = None) -> None:
        """Record an error with domain classification."""
        self.errors.append(time.time())
        self.last_error = f"{datetime.now(timezone.utc).isoformat()}: {error_msg[:200]}"
        cutoff = time.time() - 86400
        self.errors = [t for t in self.errors if t > cutoff]

        if domain:
            self.error_domain_counts[domain.value] += 1

    def query_start(self) -> None:
        """Mark query as started."""
        self.active_queries += 1

    def query_end(self) -> None:
        """Mark query as ended."""
        self.active_queries = max(0, self.active_queries - 1)

    def get_latency_stats(self) -> Dict[str, float]:
        """Compute latency percentiles."""
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
        """Compute error rates by time window."""
        now = time.time()
        last_hour = sum(1 for t in self.errors if t > now - 3600)
        last_24h = len(self.errors)
        return {
            "last_hour": last_hour,
            "last_24h": last_24h,
            "last_error": self.last_error,
            "error_domains": dict(self.error_domain_counts),
        }

    def get_doctrine_hit_rate(self) -> float:
        """Compute doctrine cache hit rate."""
        total = self.doctrine_hits + self.doctrine_misses
        if total == 0:
            return 1.0
        return round(self.doctrine_hits / total, 4)

    def get_risk_distribution(self) -> Dict[str, Any]:
        """Compute risk score distribution stats."""
        if not self.risk_scores:
            return {"count": 0, "avg": 0.0, "min": 0.0, "max": 0.0, "high_risk_count": 0}
        return {
            "count": len(self.risk_scores),
            "avg": round(sum(self.risk_scores) / len(self.risk_scores), 2),
            "min": round(min(self.risk_scores), 2),
            "max": round(max(self.risk_scores), 2),
            "high_risk_count": sum(1 for s in self.risk_scores if s >= 500),
            "critical_risk_count": sum(1 for s in self.risk_scores if s >= 750),
        }

    def get_agency_distribution(self) -> Dict[str, int]:
        """Return query counts per agency."""
        return dict(sorted(self.agency_query_counts.items(), key=lambda x: x[1], reverse=True))

    def queries_last_hour(self) -> int:
        """Count queries in the last hour."""
        cutoff = time.time() - 3600
        return sum(1 for t in self.queries if t > cutoff)

    def get_full_metrics(self) -> Dict[str, Any]:
        """Return complete metrics snapshot."""
        return {
            "latency": self.get_latency_stats(),
            "errors": self.get_error_stats(),
            "doctrine_hit_rate": self.get_doctrine_hit_rate(),
            "active_queries": self.active_queries,
            "queries_last_hour": self.queries_last_hour(),
            "total_queries": self.doctrine_hits + self.doctrine_misses,
            "risk_distribution": self.get_risk_distribution(),
            "agency_distribution": self.get_agency_distribution(),
            "query_type_distribution": dict(self.query_type_counts),
            "layer_distribution": dict(self.layer_counts),
            "cfr_title_distribution": dict(self.cfr_title_counts),
        }


# ============================================================================
# AUDIT TRAIL MANAGER
# ============================================================================

class AuditTrailManager:
    """Append-only, hash-chained audit trail for compliance determinations.

    Every compliance determination, risk assessment, and gap analysis is
    recorded in a tamper-evident JSONL log. Hash chain ensures integrity.
    """

    def __init__(self, audit_path: Path = AUDIT_LOG_PATH) -> None:
        self.audit_path = audit_path
        self._last_hash: str = self._load_last_hash()
        self._entry_count: int = self._count_entries()

    def _load_last_hash(self) -> str:
        """Load the hash of the last audit entry for chain continuity."""
        if not self.audit_path.exists():
            return hashlib.sha256(b"LG03_GENESIS_BLOCK").hexdigest()
        last_line = ""
        try:
            with open(self.audit_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        last_line = line
            if last_line:
                entry = json.loads(last_line)
                return entry.get("entry_hash", hashlib.sha256(b"LG03_GENESIS_BLOCK").hexdigest())
        except (json.JSONDecodeError, OSError) as exc:
            logger.warning(f"Failed to load last audit hash: {exc}")
        return hashlib.sha256(b"LG03_GENESIS_BLOCK").hexdigest()

    def _count_entries(self) -> int:
        """Count existing audit entries."""
        if not self.audit_path.exists():
            return 0
        count = 0
        try:
            with open(self.audit_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        count += 1
        except OSError:
            pass
        return count

    def record(self, action: str, actor: str, resource: str,
               details: Dict[str, Any], query_id: Optional[str] = None,
               determinism_hash: Optional[str] = None) -> AuditEntry:
        """Record a new audit entry with hash chain."""
        entry = AuditEntry(
            entry_id=f"AUD-{self._entry_count + 1:08d}",
            timestamp=datetime.now(timezone.utc).isoformat(),
            action=action,
            actor=actor,
            resource=resource,
            details=details,
            query_id=query_id,
            determinism_hash=determinism_hash,
        )
        entry.compute_hash(self._last_hash)
        self._last_hash = entry.entry_hash
        self._entry_count += 1

        try:
            with open(self.audit_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry.to_dict(), default=str) + "\n")
        except OSError as exc:
            logger.error(f"Failed to write audit entry: {exc}")

        return entry

    def verify_chain(self) -> Dict[str, Any]:
        """Verify the integrity of the entire audit chain."""
        if not self.audit_path.exists():
            return {"valid": True, "entries": 0, "message": "No audit entries"}

        entries = []
        try:
            with open(self.audit_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        entries.append(json.loads(line))
        except (json.JSONDecodeError, OSError) as exc:
            return {"valid": False, "entries": 0, "error": str(exc)}

        if not entries:
            return {"valid": True, "entries": 0, "message": "Empty audit trail"}

        expected_prev = hashlib.sha256(b"LG03_GENESIS_BLOCK").hexdigest()
        broken_at: Optional[int] = None

        for idx, entry_dict in enumerate(entries):
            if entry_dict.get("previous_hash") != expected_prev:
                broken_at = idx
                break

            verify_content = json.dumps({
                "entry_id": entry_dict["entry_id"],
                "timestamp": entry_dict["timestamp"],
                "action": entry_dict["action"],
                "actor": entry_dict["actor"],
                "resource": entry_dict["resource"],
                "details": entry_dict["details"],
                "query_id": entry_dict.get("query_id"),
                "determinism_hash": entry_dict.get("determinism_hash"),
                "previous_hash": entry_dict.get("previous_hash"),
            }, sort_keys=True, default=str)
            computed = hashlib.sha256(verify_content.encode("utf-8")).hexdigest()

            if computed != entry_dict.get("entry_hash"):
                broken_at = idx
                break

            expected_prev = entry_dict["entry_hash"]

        if broken_at is not None:
            return {
                "valid": False,
                "entries": len(entries),
                "broken_at_index": broken_at,
                "broken_entry_id": entries[broken_at].get("entry_id"),
                "message": f"Hash chain broken at entry {broken_at}",
            }

        return {
            "valid": True,
            "entries": len(entries),
            "first_entry": entries[0].get("entry_id"),
            "last_entry": entries[-1].get("entry_id"),
            "last_hash": entries[-1].get("entry_hash"),
            "message": "Audit chain integrity verified",
        }

    def get_entries(self, limit: int = 50, offset: int = 0,
                    action_filter: Optional[str] = None,
                    query_id_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieve audit entries with optional filtering."""
        if not self.audit_path.exists():
            return []

        entries: List[Dict[str, Any]] = []
        try:
            with open(self.audit_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    entry = json.loads(line)
                    if action_filter and entry.get("action") != action_filter:
                        continue
                    if query_id_filter and entry.get("query_id") != query_id_filter:
                        continue
                    entries.append(entry)
        except (json.JSONDecodeError, OSError) as exc:
            logger.error(f"Failed to read audit entries: {exc}")

        return entries[offset:offset + limit]

    @property
    def entry_count(self) -> int:
        """Total number of audit entries."""
        return self._entry_count


# ============================================================================
# TELEMETRY SINGLETON
# ============================================================================

class TelemetryManager:
    """Central telemetry coordinator for LG03 engine.

    Manages metrics collection, trace recording, and audit trail.
    Singleton pattern ensures consistent state across the engine.
    """

    _instance: Optional[TelemetryManager] = None

    def __init__(self) -> None:
        self.metrics = MetricsCollector()
        self.audit = AuditTrailManager()
        self._active_traces: Dict[str, TraceRecord] = {}
        self._start_time: float = time.time()

    @classmethod
    def get_instance(cls) -> TelemetryManager:
        """Get or create the singleton instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @property
    def uptime_seconds(self) -> float:
        """Seconds since telemetry was initialized."""
        return round(time.time() - self._start_time, 2)

    def trace_query(self, query_id: str, query_type: QueryType = QueryType.GENERAL) -> str:
        """Start a new query trace. Returns trace_id."""
        trace_id = f"TRC-{uuid.uuid4().hex[:12]}"
        trace = TraceRecord(
            trace_id=trace_id,
            query_id=query_id,
            query_type=query_type,
            started_at=time.time(),
        )
        self._active_traces[trace_id] = trace
        self.metrics.query_start()
        logger.debug(f"Trace started: {trace_id} for query {query_id} type={query_type.value}")
        return trace_id

    def complete_trace(self, trace_id: str, layer: ResponseLayer,
                       doctrine_hit: bool = False,
                       agency: Optional[str] = None,
                       cfr_title: Optional[str] = None,
                       risk_score: Optional[float] = None) -> Optional[TraceRecord]:
        """Complete a query trace and record metrics."""
        trace = self._active_traces.pop(trace_id, None)
        if trace is None:
            logger.warning(f"Trace not found: {trace_id}")
            return None

        trace.complete(layer)
        trace.doctrine_hit = doctrine_hit
        trace.agency = agency
        trace.cfr_title = cfr_title
        trace.risk_score = risk_score

        self.metrics.query_end()
        self.metrics.record_query(
            latency_ms=trace.latency_ms or 0.0,
            doctrine_hit=doctrine_hit,
            query_type=trace.query_type,
            layer=layer,
            agency=agency,
            cfr_title=cfr_title,
        )

        if risk_score is not None:
            self.metrics.record_risk_score(risk_score)

        logger.info(
            f"Trace complete: {trace_id} | layer={layer.value} | "
            f"latency={trace.latency_ms}ms | doctrine_hit={doctrine_hit}"
        )

        try:
            with open(METRICS_LOG_PATH, "a", encoding="utf-8") as f:
                f.write(json.dumps(trace.to_dict(), default=str) + "\n")
        except OSError as exc:
            logger.error(f"Failed to write trace to metrics log: {exc}")

        return trace

    def log_error(self, trace_id: Optional[str], error_msg: str,
                  domain: ErrorDomain = ErrorDomain.UNKNOWN,
                  details: Optional[Dict[str, Any]] = None) -> None:
        """Log an error with domain classification."""
        self.metrics.record_error(error_msg, domain)

        if trace_id and trace_id in self._active_traces:
            self._active_traces[trace_id].error = error_msg
            self._active_traces[trace_id].error_domain = domain

        error_record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "trace_id": trace_id,
            "error": error_msg[:500],
            "domain": domain.value,
            "details": details or {},
        }
        logger.error(f"[{domain.value}] {error_msg[:200]}")

        try:
            with open(ERROR_LOG_PATH, "a", encoding="utf-8") as f:
                f.write(json.dumps(error_record, default=str) + "\n")
        except OSError:
            pass

    def record_doctrine_mutation(self, doctrine_key: str,
                                 mutation_type: MutationType,
                                 origin: MutationOrigin,
                                 details: Dict[str, Any]) -> None:
        """Record a doctrine mutation for governance tracking."""
        self.audit.record(
            action=f"doctrine_mutation:{mutation_type.value}",
            actor="LG03_ENGINE",
            resource=f"doctrine:{doctrine_key}",
            details={
                "mutation_type": mutation_type.value,
                "origin": origin.value,
                **details,
            },
        )
        logger.info(
            f"Doctrine mutation recorded: {doctrine_key} | "
            f"type={mutation_type.value} | origin={origin.value}"
        )

    def record_compliance_determination(self, query_id: str, regulation: str,
                                        determination: str, risk_score: float,
                                        determinism_hash: str,
                                        details: Dict[str, Any]) -> AuditEntry:
        """Record a compliance determination in the audit trail."""
        return self.audit.record(
            action="compliance_determination",
            actor="LG03_ENGINE",
            resource=regulation,
            details={
                "determination": determination,
                "risk_score": risk_score,
                **details,
            },
            query_id=query_id,
            determinism_hash=determinism_hash,
        )

    def record_gap_analysis(self, query_id: str, entity: str,
                            gap_score: float, gaps: List[str],
                            determinism_hash: str) -> AuditEntry:
        """Record a compliance gap analysis result."""
        self.metrics.record_gap_score(gap_score)
        return self.audit.record(
            action="gap_analysis",
            actor="LG03_ENGINE",
            resource=entity,
            details={
                "gap_score": gap_score,
                "gaps_identified": gaps,
                "gap_count": len(gaps),
            },
            query_id=query_id,
            determinism_hash=determinism_hash,
        )


# ============================================================================
# MODULE-LEVEL FUNCTIONS (convenience wrappers)
# ============================================================================

def get_telemetry() -> TelemetryManager:
    """Get the telemetry singleton."""
    return TelemetryManager.get_instance()


def trace_query(query_id: str, query_type: QueryType = QueryType.GENERAL) -> str:
    """Start a new query trace. Returns trace_id."""
    return get_telemetry().trace_query(query_id, query_type)


def complete_trace(trace_id: str, layer: ResponseLayer,
                   doctrine_hit: bool = False, **kwargs: Any) -> Optional[TraceRecord]:
    """Complete a query trace."""
    return get_telemetry().complete_trace(trace_id, layer, doctrine_hit, **kwargs)


def log_error(trace_id: Optional[str], error_msg: str,
              domain: ErrorDomain = ErrorDomain.UNKNOWN,
              details: Optional[Dict[str, Any]] = None) -> None:
    """Log an error."""
    get_telemetry().log_error(trace_id, error_msg, domain, details)


def record_doctrine_mutation(doctrine_key: str, mutation_type: MutationType,
                             origin: MutationOrigin,
                             details: Dict[str, Any]) -> None:
    """Record a doctrine mutation."""
    get_telemetry().record_doctrine_mutation(doctrine_key, mutation_type, origin, details)
