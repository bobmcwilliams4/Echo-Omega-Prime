"""
LG10 FAMILY LAW ENGINE — Telemetry Module
Production telemetry with query tracing, performance metrics, and JSONL flush.

Ring buffer: 10,000 traces max.
JSONL flush to disk for audit and performance analysis.

Author: ECHO OMEGA PRIME
Authority: 11.0 SOVEREIGN
Engine: LG10 (Family Law) | Tier 1 | Auth 5
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Optional, List, Dict, Any
import hashlib
import json
import threading
import time
import uuid

from loguru import logger


# ============================================================================
# TELEMETRY ENUMS
# ============================================================================

class ErrorDomain(str, Enum):
    """Domain classification for errors."""
    DOCTRINE_CACHE = "doctrine_cache"
    VECTOR_SEARCH = "vector_search"
    DEEP_ANALYSIS = "deep_analysis"
    NORMALIZATION = "normalization"
    FRAGILITY = "fragility"
    COVERAGE = "coverage"
    DRIFT = "drift"
    AUDIT = "audit"
    SERIALIZATION = "serialization"
    FASTAPI = "fastapi"
    CUSTODY = "custody"
    SUPPORT = "support"
    PROPERTY = "property"
    JURISDICTION = "jurisdiction"
    ENFORCEMENT = "enforcement"


class ResponseLayer(str, Enum):
    """Which processing layer handled the query."""
    DOCTRINE = "doctrine"
    RETRIEVAL = "retrieval"
    DEEP_ANALYSIS = "deep_analysis"
    STRATIFIED = "stratified"
    MULTI_DOCTRINE = "multi_doctrine"


class MutationType(str, Enum):
    """Type of doctrine mutation event."""
    BLOCK_ADDED = "block_added"
    BLOCK_UPDATED = "block_updated"
    BLOCK_REMOVED = "block_removed"
    CONFIDENCE_ADJUSTED = "confidence_adjusted"
    DRIFT_DETECTED = "drift_detected"
    COVERAGE_GAP = "coverage_gap"
    STALE_FLAGGED = "stale_flagged"


class MutationOrigin(str, Enum):
    """Origin of a doctrine mutation."""
    ADMIN = "admin"
    DRIFT_WATCHER = "drift_watcher"
    COVERAGE_MAP = "coverage_map"
    AUTO_CALIBRATION = "auto_calibration"
    STARTUP = "startup"
    RUNTIME = "runtime"


# ============================================================================
# TELEMETRY DATA STRUCTURES
# ============================================================================

@dataclass
class TelemetryStep:
    """A single step in query processing."""
    step_name: str
    layer: ResponseLayer
    start_ms: float
    end_ms: float
    success: bool
    details: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None

    @property
    def duration_ms(self) -> float:
        return round(self.end_ms - self.start_ms, 3)

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "step": self.step_name,
            "layer": self.layer.value,
            "duration_ms": self.duration_ms,
            "success": self.success,
        }
        if self.details:
            result["details"] = self.details
        if self.error:
            result["error"] = self.error
        return result


@dataclass
class QueryTrace:
    """Complete trace of a single query through the engine."""
    trace_id: str
    query_id: str
    query_text: str
    start_time: float
    end_time: Optional[float] = None
    steps: List[TelemetryStep] = field(default_factory=list)
    response_layer: Optional[ResponseLayer] = None
    doctrine_hit: bool = False
    cache_hit: bool = False
    confidence: Optional[float] = None
    error: Optional[str] = None
    mode: str = "fast"
    zone: Optional[str] = None
    determinism_hash: Optional[str] = None
    citations_count: int = 0

    @property
    def total_ms(self) -> float:
        if self.end_time is None:
            return round((time.time() * 1000) - self.start_time, 3)
        return round(self.end_time - self.start_time, 3)

    @property
    def is_complete(self) -> bool:
        return self.end_time is not None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "trace_id": self.trace_id,
            "query_id": self.query_id,
            "query_text": self.query_text[:200],
            "total_ms": self.total_ms,
            "response_layer": self.response_layer.value if self.response_layer else None,
            "doctrine_hit": self.doctrine_hit,
            "cache_hit": self.cache_hit,
            "confidence": self.confidence,
            "mode": self.mode,
            "zone": self.zone,
            "citations_count": self.citations_count,
            "determinism_hash": self.determinism_hash,
            "steps": [s.to_dict() for s in self.steps],
            "error": self.error,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def to_audit_record(self) -> Dict[str, Any]:
        """Minimal audit record for JSONL flush."""
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "query_id": self.query_id,
            "query_text": self.query_text[:300],
            "response_hash": self.determinism_hash or "",
            "confidence": self.confidence,
            "citations_count": self.citations_count,
            "latency_ms": self.total_ms,
            "mode": self.mode,
            "zone": self.zone or "",
            "cache_hit": self.cache_hit,
            "doctrine_hit": self.doctrine_hit,
            "response_layer": self.response_layer.value if self.response_layer else "",
            "error": self.error,
        }


@dataclass
class DoctrineMutation:
    """Record of a change to doctrine cache."""
    mutation_id: str
    mutation_type: MutationType
    origin: MutationOrigin
    topic_key: str
    description: str
    timestamp: str
    previous_state: Optional[Dict[str, Any]] = None
    new_state: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "mutation_id": self.mutation_id,
            "type": self.mutation_type.value,
            "origin": self.origin.value,
            "topic_key": self.topic_key,
            "description": self.description,
            "timestamp": self.timestamp,
        }


# ============================================================================
# TELEMETRY COLLECTOR — Ring buffer + JSONL flush
# ============================================================================

class TelemetryCollector:
    """
    Production telemetry collector for the LG10 Family Law engine.

    Features:
        - Ring buffer (configurable, default 10K traces)
        - Thread-safe operations
        - JSONL flush to disk
        - Error tracking by domain
        - Doctrine mutation log
        - Performance statistics
    """

    def __init__(self, buffer_size: int = 10_000, log_dir: Optional[Path] = None):
        self._buffer_size = buffer_size
        self._traces: List[QueryTrace] = []
        self._errors: List[Dict[str, Any]] = []
        self._mutations: List[DoctrineMutation] = []
        self._lock = threading.Lock()
        self._log_dir = log_dir or Path("O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/lg10/logs")
        self._log_dir.mkdir(parents=True, exist_ok=True)
        self._telemetry_file = self._log_dir / "telemetry.jsonl"
        self._mutation_file = self._log_dir / "mutations.jsonl"
        self._total_queries = 0
        self._total_errors = 0
        self._start_time = time.time()
        logger.info(f"TelemetryCollector initialized | buffer={buffer_size} | dir={self._log_dir}")

    def trace_query(self, query_id: str, query_text: str, mode: str = "fast") -> QueryTrace:
        """Start a new query trace."""
        trace = QueryTrace(
            trace_id=str(uuid.uuid4()),
            query_id=query_id,
            query_text=query_text,
            start_time=time.time() * 1000,
            mode=mode,
        )
        return trace

    def add_step(self, trace: QueryTrace, step_name: str, layer: ResponseLayer,
                 success: bool, duration_ms: float, details: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None) -> None:
        """Add a processing step to a trace."""
        now = time.time() * 1000
        step = TelemetryStep(
            step_name=step_name,
            layer=layer,
            start_ms=now - duration_ms,
            end_ms=now,
            success=success,
            details=details or {},
            error=error,
        )
        trace.steps.append(step)

    def complete_trace(self, trace: QueryTrace) -> None:
        """Complete a trace and add to ring buffer."""
        trace.end_time = time.time() * 1000
        with self._lock:
            self._traces.append(trace)
            self._total_queries += 1
            if len(self._traces) > self._buffer_size:
                self._traces.pop(0)
        self._flush_trace(trace)

    def log_error(self, domain: ErrorDomain, error_msg: str,
                  query_id: Optional[str] = None, details: Optional[Dict[str, Any]] = None) -> None:
        """Log an error with domain classification."""
        error_record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "domain": domain.value,
            "error": error_msg[:500],
            "query_id": query_id,
            "details": details or {},
        }
        with self._lock:
            self._errors.append(error_record)
            self._total_errors += 1
            if len(self._errors) > 1000:
                self._errors.pop(0)
        logger.error(f"[{domain.value}] {error_msg[:200]}")

    def record_doctrine_mutation(self, mutation_type: MutationType, origin: MutationOrigin,
                                  topic_key: str, description: str,
                                  previous_state: Optional[Dict[str, Any]] = None,
                                  new_state: Optional[Dict[str, Any]] = None) -> None:
        """Record a doctrine mutation event."""
        mutation = DoctrineMutation(
            mutation_id=str(uuid.uuid4()),
            mutation_type=mutation_type,
            origin=origin,
            topic_key=topic_key,
            description=description,
            timestamp=datetime.now(timezone.utc).isoformat(),
            previous_state=previous_state,
            new_state=new_state,
        )
        with self._lock:
            self._mutations.append(mutation)
            if len(self._mutations) > 5000:
                self._mutations.pop(0)
        self._flush_mutation(mutation)
        logger.info(f"Doctrine mutation: {mutation_type.value} | {topic_key} | {description[:80]}")

    def get_stats(self) -> Dict[str, Any]:
        """Get telemetry statistics."""
        with self._lock:
            traces = list(self._traces)
            errors = list(self._errors)

        completed = [t for t in traces if t.is_complete]
        latencies = [t.total_ms for t in completed]
        cache_hits = sum(1 for t in completed if t.cache_hit)
        doctrine_hits = sum(1 for t in completed if t.doctrine_hit)

        latency_stats = {}
        if latencies:
            sorted_lat = sorted(latencies)
            latency_stats = {
                "avg_ms": round(sum(latencies) / len(latencies), 2),
                "p50_ms": round(sorted_lat[len(sorted_lat) // 2], 2),
                "p95_ms": round(sorted_lat[int(len(sorted_lat) * 0.95)], 2),
                "p99_ms": round(sorted_lat[int(len(sorted_lat) * 0.99)], 2),
                "min_ms": round(sorted_lat[0], 2),
                "max_ms": round(sorted_lat[-1], 2),
            }

        uptime = time.time() - self._start_time
        return {
            "total_queries": self._total_queries,
            "total_errors": self._total_errors,
            "buffer_size": len(traces),
            "buffer_capacity": self._buffer_size,
            "cache_hit_rate": round(cache_hits / max(len(completed), 1), 4),
            "doctrine_hit_rate": round(doctrine_hits / max(len(completed), 1), 4),
            "latency": latency_stats,
            "errors_last_hour": sum(1 for e in errors if self._is_recent(e.get("timestamp", ""), 3600)),
            "mutations_count": len(self._mutations),
            "uptime_seconds": round(uptime, 1),
        }

    def get_recent_traces(self, count: int = 20) -> List[Dict[str, Any]]:
        """Get most recent traces."""
        with self._lock:
            recent = self._traces[-count:]
        return [t.to_dict() for t in reversed(recent)]

    def get_recent_errors(self, count: int = 20) -> List[Dict[str, Any]]:
        """Get most recent errors."""
        with self._lock:
            recent = self._errors[-count:]
        return list(reversed(recent))

    def _flush_trace(self, trace: QueryTrace) -> None:
        """Append trace to JSONL file."""
        try:
            record = trace.to_audit_record()
            with open(self._telemetry_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(record, default=str) + "\n")
        except Exception as e:
            logger.warning(f"Telemetry flush failed: {e}")

    def _flush_mutation(self, mutation: DoctrineMutation) -> None:
        """Append mutation to JSONL file."""
        try:
            with open(self._mutation_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(mutation.to_dict(), default=str) + "\n")
        except Exception as e:
            logger.warning(f"Mutation flush failed: {e}")

    @staticmethod
    def _is_recent(timestamp_str: str, window_seconds: int) -> bool:
        """Check if an ISO timestamp is within the given window."""
        try:
            ts = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
            now = datetime.now(timezone.utc)
            return (now - ts).total_seconds() < window_seconds
        except (ValueError, TypeError):
            return False


# ============================================================================
# MODULE-LEVEL SINGLETON
# ============================================================================

_telemetry: Optional[TelemetryCollector] = None


def get_telemetry() -> TelemetryCollector:
    """Get or create the global telemetry collector."""
    global _telemetry
    if _telemetry is None:
        _telemetry = TelemetryCollector()
    return _telemetry


def trace_query(query_id: str, query_text: str, mode: str = "fast") -> QueryTrace:
    """Convenience: start a trace on the global collector."""
    return get_telemetry().trace_query(query_id, query_text, mode)


def complete_trace(trace: QueryTrace) -> None:
    """Convenience: complete a trace on the global collector."""
    get_telemetry().complete_trace(trace)


def log_error(domain: ErrorDomain, error_msg: str,
              query_id: Optional[str] = None, details: Optional[Dict[str, Any]] = None) -> None:
    """Convenience: log an error on the global collector."""
    get_telemetry().log_error(domain, error_msg, query_id, details)


def record_doctrine_mutation(mutation_type: MutationType, origin: MutationOrigin,
                              topic_key: str, description: str,
                              previous_state: Optional[Dict[str, Any]] = None,
                              new_state: Optional[Dict[str, Any]] = None) -> None:
    """Convenience: record a doctrine mutation on the global collector."""
    get_telemetry().record_doctrine_mutation(
        mutation_type, origin, topic_key, description, previous_state, new_state
    )
