"""
LG11 Immigration Law Engine — Telemetry Module
Captures query traces, performance metrics, and audit events.

Architecture:
    QueryTrace: Per-query lifecycle tracking
    TelemetryStep: Individual analysis step within a trace
    TelemetryCollector: Ring-buffer aggregator with JSONL flush

Author: ECHO OMEGA PRIME
Engine: LG11 Immigration Law
Authority: 11.0 SOVEREIGN
"""

from __future__ import annotations

import json
import time
import uuid
import hashlib
import threading
from collections import deque
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

from loguru import logger


# =============================================================================
# TELEMETRY ENUMS
# =============================================================================

class ResponseLayer(str, Enum):
    """Which processing layer handled the query."""
    DOCTRINE = "doctrine"
    RETRIEVAL = "retrieval"
    DEEP_ANALYSIS = "deep_analysis"
    STRATIFIED = "stratified"
    ERROR = "error"


class ErrorDomain(str, Enum):
    """Classification of error source."""
    PARSING = "parsing"
    DOCTRINE_LOOKUP = "doctrine_lookup"
    VECTOR_SEARCH = "vector_search"
    ANALYSIS = "analysis"
    SERIALIZATION = "serialization"
    NETWORK = "network"
    TIMEOUT = "timeout"
    VALIDATION = "validation"
    UNKNOWN = "unknown"


class MutationType(str, Enum):
    """Type of doctrine mutation event."""
    ADDED = "added"
    UPDATED = "updated"
    REMOVED = "removed"
    STALE_FLAGGED = "stale_flagged"
    CONFIDENCE_ADJUSTED = "confidence_adjusted"


class MutationOrigin(str, Enum):
    """Source that triggered doctrine mutation."""
    MANUAL = "manual"
    DRIFT_WATCHER = "drift_watcher"
    AUTO_UPDATE = "auto_update"
    COVERAGE_GAP = "coverage_gap"
    EXTERNAL_FEED = "external_feed"


# =============================================================================
# TELEMETRY STEP — Individual analysis step within a query trace
# =============================================================================

@dataclass
class TelemetryStep:
    """Single step in a query trace."""
    step_name: str
    layer: ResponseLayer
    started_at: float = field(default_factory=time.time)
    completed_at: Optional[float] = None
    duration_ms: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None

    def complete(self, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Mark this step as completed."""
        self.completed_at = time.time()
        self.duration_ms = round((self.completed_at - self.started_at) * 1000, 3)
        if metadata:
            self.metadata.update(metadata)

    def fail(self, error: str) -> None:
        """Mark this step as failed."""
        self.completed_at = time.time()
        self.duration_ms = round((self.completed_at - self.started_at) * 1000, 3)
        self.error = error

    def to_dict(self) -> Dict[str, Any]:
        """Serialize for JSONL output."""
        result = {
            "step_name": self.step_name,
            "layer": self.layer.value,
            "started_at": self.started_at,
            "duration_ms": self.duration_ms,
        }
        if self.metadata:
            result["metadata"] = self.metadata
        if self.error:
            result["error"] = self.error
        return result


# =============================================================================
# QUERY TRACE — Full lifecycle of a single query
# =============================================================================

@dataclass
class QueryTrace:
    """Complete trace of a single query from receipt to response."""
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    query_id: str = ""
    query_text: str = ""
    mode: str = "fast"
    started_at: float = field(default_factory=time.time)
    completed_at: Optional[float] = None
    total_duration_ms: Optional[float] = None
    steps: List[TelemetryStep] = field(default_factory=list)
    response_layer: ResponseLayer = ResponseLayer.DOCTRINE
    doctrine_hit: bool = False
    confidence_band: str = ""
    cache_hit: bool = False
    error: Optional[str] = None
    response_hash: Optional[str] = None
    citations_count: int = 0
    zone: str = ""

    def add_step(self, step_name: str, layer: ResponseLayer) -> TelemetryStep:
        """Create and add a new telemetry step."""
        step = TelemetryStep(step_name=step_name, layer=layer)
        self.steps.append(step)
        return step

    def complete(self, response_hash: Optional[str] = None) -> None:
        """Mark the entire trace as completed."""
        self.completed_at = time.time()
        self.total_duration_ms = round((self.completed_at - self.started_at) * 1000, 3)
        if response_hash:
            self.response_hash = response_hash

    def fail(self, error: str) -> None:
        """Mark the trace as failed."""
        self.completed_at = time.time()
        self.total_duration_ms = round((self.completed_at - self.started_at) * 1000, 3)
        self.error = error

    def to_dict(self) -> Dict[str, Any]:
        """Serialize for JSONL audit trail."""
        return {
            "trace_id": self.trace_id,
            "query_id": self.query_id,
            "query_text": self.query_text[:200],
            "mode": self.mode,
            "started_at": self.started_at,
            "total_duration_ms": self.total_duration_ms,
            "response_layer": self.response_layer.value,
            "doctrine_hit": self.doctrine_hit,
            "confidence_band": self.confidence_band,
            "cache_hit": self.cache_hit,
            "citations_count": self.citations_count,
            "zone": self.zone,
            "steps": [s.to_dict() for s in self.steps],
            "error": self.error,
            "response_hash": self.response_hash,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


# =============================================================================
# DOCTRINE MUTATION EVENT — Tracks changes to doctrine blocks
# =============================================================================

@dataclass
class DoctrineMutationEvent:
    """Records a change to doctrine blocks for audit purposes."""
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    doctrine_topic: str = ""
    mutation_type: MutationType = MutationType.UPDATED
    origin: MutationOrigin = MutationOrigin.MANUAL
    previous_hash: Optional[str] = None
    new_hash: Optional[str] = None
    description: str = ""
    confidence_before: Optional[float] = None
    confidence_after: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        """Serialize for JSONL output."""
        return {
            "event_id": self.event_id,
            "timestamp": self.timestamp,
            "doctrine_topic": self.doctrine_topic,
            "mutation_type": self.mutation_type.value,
            "origin": self.origin.value,
            "previous_hash": self.previous_hash,
            "new_hash": self.new_hash,
            "description": self.description,
            "confidence_before": self.confidence_before,
            "confidence_after": self.confidence_after,
        }


# =============================================================================
# TELEMETRY COLLECTOR — Ring-buffer aggregator with JSONL flush
# =============================================================================

class TelemetryCollector:
    """
    Collects and manages query traces with ring-buffer storage.
    Thread-safe. Flushes to JSONL on demand or at capacity thresholds.
    """

    MAX_TRACES = 10_000
    FLUSH_THRESHOLD = 1_000

    def __init__(self, log_dir: Optional[Path] = None):
        self._traces: deque[QueryTrace] = deque(maxlen=self.MAX_TRACES)
        self._mutations: deque[DoctrineMutationEvent] = deque(maxlen=5_000)
        self._lock = threading.Lock()
        self._total_queries: int = 0
        self._total_errors: int = 0
        self._total_doctrine_hits: int = 0
        self._total_doctrine_misses: int = 0
        self._started_at: float = time.time()

        self._log_dir = log_dir or Path("O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/lg11/logs")
        self._log_dir.mkdir(parents=True, exist_ok=True)
        self._trace_file = self._log_dir / "telemetry_traces.jsonl"
        self._mutation_file = self._log_dir / "doctrine_mutations.jsonl"

        logger.info(
            "TelemetryCollector initialized | max_traces={} | log_dir={}",
            self.MAX_TRACES, self._log_dir
        )

    def start_trace(self, query_id: str, query_text: str, mode: str) -> QueryTrace:
        """Begin a new query trace."""
        trace = QueryTrace(query_id=query_id, query_text=query_text, mode=mode)
        return trace

    def complete_trace(self, trace: QueryTrace) -> None:
        """Finalize and store a completed trace."""
        with self._lock:
            self._traces.append(trace)
            self._total_queries += 1
            if trace.doctrine_hit:
                self._total_doctrine_hits += 1
            else:
                self._total_doctrine_misses += 1
            if trace.error:
                self._total_errors += 1

        if len(self._traces) >= self.FLUSH_THRESHOLD and len(self._traces) % self.FLUSH_THRESHOLD == 0:
            self._flush_traces()

    def log_error(self, query_id: str, error_domain: ErrorDomain, error_msg: str) -> None:
        """Record an error event outside of a trace."""
        with self._lock:
            self._total_errors += 1
        logger.error("Telemetry error | query={} | domain={} | error={}", query_id, error_domain.value, error_msg)

    def record_doctrine_mutation(
        self,
        topic: str,
        mutation_type: MutationType,
        origin: MutationOrigin,
        description: str,
        previous_hash: Optional[str] = None,
        new_hash: Optional[str] = None,
        confidence_before: Optional[float] = None,
        confidence_after: Optional[float] = None,
    ) -> None:
        """Record a doctrine mutation event."""
        event = DoctrineMutationEvent(
            doctrine_topic=topic,
            mutation_type=mutation_type,
            origin=origin,
            description=description,
            previous_hash=previous_hash,
            new_hash=new_hash,
            confidence_before=confidence_before,
            confidence_after=confidence_after,
        )
        with self._lock:
            self._mutations.append(event)
        self._flush_mutation(event)

    def get_stats(self) -> Dict[str, Any]:
        """Return aggregated telemetry statistics."""
        with self._lock:
            uptime = time.time() - self._started_at
            total_hits = self._total_doctrine_hits
            total_misses = self._total_doctrine_misses
            total_q = self._total_queries
            total_e = self._total_errors

        hit_rate = round(total_hits / max(total_q, 1), 4)
        error_rate = round(total_e / max(total_q, 1), 4)

        latencies = [t.total_duration_ms for t in self._traces if t.total_duration_ms is not None]
        if latencies:
            sorted_lat = sorted(latencies)
            p50_idx = int(len(sorted_lat) * 0.50)
            p95_idx = int(len(sorted_lat) * 0.95)
            p99_idx = int(len(sorted_lat) * 0.99)
            latency_stats = {
                "p50_ms": round(sorted_lat[min(p50_idx, len(sorted_lat) - 1)], 2),
                "p95_ms": round(sorted_lat[min(p95_idx, len(sorted_lat) - 1)], 2),
                "p99_ms": round(sorted_lat[min(p99_idx, len(sorted_lat) - 1)], 2),
                "avg_ms": round(sum(latencies) / len(latencies), 2),
                "min_ms": round(min(latencies), 2),
                "max_ms": round(max(latencies), 2),
            }
        else:
            latency_stats = {"p50_ms": 0.0, "p95_ms": 0.0, "p99_ms": 0.0, "avg_ms": 0.0, "min_ms": 0.0, "max_ms": 0.0}

        return {
            "uptime_seconds": round(uptime, 1),
            "total_queries": total_q,
            "total_errors": total_e,
            "error_rate": error_rate,
            "doctrine_hit_rate": hit_rate,
            "doctrine_hits": total_hits,
            "doctrine_misses": total_misses,
            "traces_buffered": len(self._traces),
            "mutations_recorded": len(self._mutations),
            "latency": latency_stats,
        }

    def get_recent_traces(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Return the most recent traces."""
        with self._lock:
            recent = list(self._traces)[-limit:]
        return [t.to_dict() for t in recent]

    def _flush_traces(self) -> None:
        """Flush buffered traces to JSONL file."""
        with self._lock:
            pending = list(self._traces)
        if not pending:
            return
        try:
            with open(self._trace_file, "a", encoding="utf-8") as f:
                for trace in pending[-self.FLUSH_THRESHOLD:]:
                    f.write(json.dumps(trace.to_dict(), default=str) + "\n")
            logger.debug("Flushed {} traces to {}", min(len(pending), self.FLUSH_THRESHOLD), self._trace_file)
        except Exception as exc:
            logger.error("Failed to flush traces: {}", exc)

    def _flush_mutation(self, event: DoctrineMutationEvent) -> None:
        """Append a single mutation event to the mutation log."""
        try:
            with open(self._mutation_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(event.to_dict(), default=str) + "\n")
        except Exception as exc:
            logger.error("Failed to flush mutation: {}", exc)

    def flush_all(self) -> None:
        """Force flush all buffered data."""
        self._flush_traces()
        logger.info("Full telemetry flush completed | traces={}", len(self._traces))


# =============================================================================
# MODULE-LEVEL SINGLETON AND ACCESS FUNCTIONS
# =============================================================================

_collector: Optional[TelemetryCollector] = None


def get_telemetry() -> TelemetryCollector:
    """Get or create the singleton TelemetryCollector."""
    global _collector
    if _collector is None:
        _collector = TelemetryCollector()
    return _collector


def trace_query(query_id: str, query_text: str, mode: str) -> QueryTrace:
    """Start a new query trace via the global collector."""
    return get_telemetry().start_trace(query_id, query_text, mode)


def complete_trace(trace: QueryTrace) -> None:
    """Complete and store a query trace via the global collector."""
    get_telemetry().complete_trace(trace)


def log_error(query_id: str, error_domain: ErrorDomain, error_msg: str) -> None:
    """Log an error via the global collector."""
    get_telemetry().log_error(query_id, error_domain, error_msg)


def record_doctrine_mutation(
    topic: str,
    mutation_type: MutationType,
    origin: MutationOrigin,
    description: str,
    **kwargs: Any,
) -> None:
    """Record a doctrine mutation via the global collector."""
    get_telemetry().record_doctrine_mutation(topic, mutation_type, origin, description, **kwargs)
