"""
TX14 Crypto Tax Engine — Telemetry Module
Full query tracing, latency tracking, error domain classification,
doctrine mutation logging, and operational metrics.

Engine: TX14 Crypto Tax Intelligence Engine
Port: 8464
Author: ECHO OMEGA PRIME
"""

from __future__ import annotations

import hashlib
import json
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

from loguru import logger

# ==============================================================================
# CONSTANTS
# ==============================================================================

ENGINE_ID: str = "TX14"
ENGINE_NAME: str = "Crypto Tax Intelligence Engine"
ENGINE_VERSION: str = "1.0.0"
ENGINE_PORT: int = 8464

TELEMETRY_DIR: Path = Path("O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/TX14_crypto_tax/telemetry_data")
TELEMETRY_DIR.mkdir(parents=True, exist_ok=True)

TRACE_LOG: Path = TELEMETRY_DIR / "trace_log.jsonl"
ERROR_LOG: Path = TELEMETRY_DIR / "error_log.jsonl"
MUTATION_LOG: Path = TELEMETRY_DIR / "mutation_log.jsonl"
METRICS_LOG: Path = TELEMETRY_DIR / "metrics_snapshot.json"


# ==============================================================================
# ENUMS
# ==============================================================================

class ResponseLayer(str, Enum):
    """Which layer of the three-layer architecture produced the response."""
    DOCTRINE_CACHE = "doctrine_cache"
    SEMANTIC_RETRIEVAL = "semantic_retrieval"
    DEEP_ANALYSIS = "deep_analysis"
    STRATIFIED = "stratified"
    FALLBACK = "fallback"


class ErrorDomain(str, Enum):
    """Classification of error sources for root-cause analysis."""
    DOCTRINE_LOOKUP = "doctrine_lookup"
    SEMANTIC_SEARCH = "semantic_search"
    DEEP_ANALYSIS = "deep_analysis"
    INPUT_VALIDATION = "input_validation"
    AUTHORITY_RESOLUTION = "authority_resolution"
    CONFIDENCE_SCORING = "confidence_scoring"
    SERIALIZATION = "serialization"
    NETWORK = "network"
    DATABASE = "database"
    CONFIGURATION = "configuration"
    UNKNOWN = "unknown"


class MutationType(str, Enum):
    """Types of doctrine mutations tracked for drift detection."""
    BLOCK_ADDED = "block_added"
    BLOCK_MODIFIED = "block_modified"
    BLOCK_REMOVED = "block_removed"
    KEYWORD_UPDATED = "keyword_updated"
    AUTHORITY_CHANGED = "authority_changed"
    CONFIDENCE_ADJUSTED = "confidence_adjusted"
    CONCLUSION_REVISED = "conclusion_revised"
    REASONING_UPDATED = "reasoning_updated"


class MutationOrigin(str, Enum):
    """Who or what triggered the mutation."""
    COMMANDER_OVERRIDE = "commander_override"
    SYSTEM_AUTO = "system_auto"
    DRIFT_CORRECTION = "drift_correction"
    AUTHORITY_UPDATE = "authority_update"
    CASE_LAW_UPDATE = "case_law_update"
    LEGISLATIVE_CHANGE = "legislative_change"
    REGULATORY_CHANGE = "regulatory_change"
    QUALITY_GATE = "quality_gate"


# ==============================================================================
# TRACE DATA STRUCTURES
# ==============================================================================

@dataclass
class TraceSpan:
    """A single span within a query trace."""
    span_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    name: str = ""
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    duration_ms: Optional[float] = None
    attributes: Dict[str, Any] = field(default_factory=dict)
    status: str = "in_progress"
    error: Optional[str] = None

    def complete(self, status: str = "success", error: Optional[str] = None) -> None:
        """Mark the span as complete."""
        self.end_time = time.time()
        self.duration_ms = round((self.end_time - self.start_time) * 1000, 3)
        self.status = status
        self.error = error

    def to_dict(self) -> Dict[str, Any]:
        """Serialize for JSON logging."""
        return {
            "span_id": self.span_id,
            "name": self.name,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration_ms": self.duration_ms,
            "attributes": self.attributes,
            "status": self.status,
            "error": self.error,
        }


@dataclass
class QueryTrace:
    """Full trace of a single query through the engine."""
    trace_id: str = field(default_factory=lambda: uuid.uuid4().hex)
    query_id: str = ""
    engine_id: str = ENGINE_ID
    engine_version: str = ENGINE_VERSION
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    question_hash: str = ""
    response_layer: Optional[str] = None
    doctrine_topic: Optional[str] = None
    doctrine_hit: bool = False
    total_latency_ms: Optional[float] = None
    spans: List[TraceSpan] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    error_domain: Optional[str] = None
    error_message: Optional[str] = None

    def add_span(self, name: str, **attributes: Any) -> TraceSpan:
        """Create and register a new span."""
        span = TraceSpan(name=name, attributes=attributes)
        self.spans.append(span)
        return span

    def complete(self, layer: ResponseLayer, doctrine_hit: bool, doctrine_topic: Optional[str] = None) -> None:
        """Finalize the trace with results."""
        self.response_layer = layer.value
        self.doctrine_hit = doctrine_hit
        self.doctrine_topic = doctrine_topic
        if self.spans:
            first_start = min(s.start_time for s in self.spans)
            last_end = max(s.end_time or time.time() for s in self.spans)
            self.total_latency_ms = round((last_end - first_start) * 1000, 3)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the full trace."""
        return {
            "trace_id": self.trace_id,
            "query_id": self.query_id,
            "engine_id": self.engine_id,
            "engine_version": self.engine_version,
            "timestamp": self.timestamp,
            "question_hash": self.question_hash,
            "response_layer": self.response_layer,
            "doctrine_topic": self.doctrine_topic,
            "doctrine_hit": self.doctrine_hit,
            "total_latency_ms": self.total_latency_ms,
            "spans": [s.to_dict() for s in self.spans],
            "metadata": self.metadata,
            "error_domain": self.error_domain,
            "error_message": self.error_message,
        }


# ==============================================================================
# DOCTRINE MUTATION RECORD
# ==============================================================================

@dataclass
class DoctrineMutation:
    """Record of a change to doctrine content for drift tracking."""
    mutation_id: str = field(default_factory=lambda: uuid.uuid4().hex[:16])
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    engine_id: str = ENGINE_ID
    mutation_type: str = ""
    origin: str = ""
    doctrine_topic: str = ""
    field_changed: str = ""
    old_value_hash: Optional[str] = None
    new_value_hash: Optional[str] = None
    description: str = ""
    approved_by: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Serialize for logging."""
        return {
            "mutation_id": self.mutation_id,
            "timestamp": self.timestamp,
            "engine_id": self.engine_id,
            "mutation_type": self.mutation_type,
            "origin": self.origin,
            "doctrine_topic": self.doctrine_topic,
            "field_changed": self.field_changed,
            "old_value_hash": self.old_value_hash,
            "new_value_hash": self.new_value_hash,
            "description": self.description,
            "approved_by": self.approved_by,
        }


# ==============================================================================
# TELEMETRY COLLECTOR
# ==============================================================================

class TelemetryCollector:
    """Central telemetry collection for the TX14 Crypto Tax Engine.

    Responsibilities:
    - Query trace creation and finalization
    - Error logging with domain classification
    - Doctrine mutation tracking
    - Latency and throughput metrics
    - Periodic metrics snapshots
    """

    def __init__(self) -> None:
        self._traces: List[QueryTrace] = []
        self._errors: List[Dict[str, Any]] = []
        self._mutations: List[DoctrineMutation] = []
        self._latencies: List[float] = []
        self._doctrine_hits: int = 0
        self._doctrine_misses: int = 0
        self._query_timestamps: List[float] = []
        self._error_timestamps: List[float] = []
        self._active_queries: int = 0
        self._total_queries: int = 0
        self._start_time: float = time.time()
        self._max_trace_buffer: int = 500
        self._max_latency_buffer: int = 200
        logger.info(f"TelemetryCollector initialized for {ENGINE_ID} v{ENGINE_VERSION}")

    def create_trace(self, query_id: str, question: str) -> QueryTrace:
        """Create a new query trace."""
        trace = QueryTrace(
            query_id=query_id,
            question_hash=hashlib.sha256(question.encode()).hexdigest()[:16],
        )
        self._traces.append(trace)
        if len(self._traces) > self._max_trace_buffer:
            self._flush_traces()
        self._active_queries += 1
        self._total_queries += 1
        self._query_timestamps.append(time.time())
        return trace

    def complete_trace(self, trace: QueryTrace, layer: ResponseLayer, doctrine_hit: bool,
                       doctrine_topic: Optional[str] = None) -> None:
        """Finalize a query trace and record metrics."""
        trace.complete(layer, doctrine_hit, doctrine_topic)
        self._active_queries = max(0, self._active_queries - 1)
        if trace.total_latency_ms is not None:
            self._latencies.append(trace.total_latency_ms)
            if len(self._latencies) > self._max_latency_buffer:
                self._latencies = self._latencies[-self._max_latency_buffer:]
        if doctrine_hit:
            self._doctrine_hits += 1
        else:
            self._doctrine_misses += 1
        self._persist_trace(trace)

    def log_error(self, domain: ErrorDomain, message: str, trace_id: Optional[str] = None,
                  details: Optional[Dict[str, Any]] = None) -> None:
        """Log an error with domain classification."""
        error_record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "engine_id": ENGINE_ID,
            "error_domain": domain.value,
            "message": message[:500],
            "trace_id": trace_id,
            "details": details or {},
        }
        self._errors.append(error_record)
        self._error_timestamps.append(time.time())
        logger.error(f"[{domain.value}] {message[:200]}")
        self._persist_error(error_record)

    def record_doctrine_mutation(self, mutation_type: MutationType, origin: MutationOrigin,
                                 doctrine_topic: str, field_changed: str, description: str,
                                 old_value: Optional[str] = None, new_value: Optional[str] = None,
                                 approved_by: Optional[str] = None) -> DoctrineMutation:
        """Record a change to doctrine content."""
        mutation = DoctrineMutation(
            mutation_type=mutation_type.value,
            origin=origin.value,
            doctrine_topic=doctrine_topic,
            field_changed=field_changed,
            old_value_hash=hashlib.sha256(old_value.encode()).hexdigest()[:16] if old_value else None,
            new_value_hash=hashlib.sha256(new_value.encode()).hexdigest()[:16] if new_value else None,
            description=description,
            approved_by=approved_by,
        )
        self._mutations.append(mutation)
        logger.info(f"Doctrine mutation recorded: {mutation_type.value} on {doctrine_topic}")
        self._persist_mutation(mutation)
        return mutation

    def get_latency_stats(self) -> Dict[str, float]:
        """Calculate latency statistics from recent queries."""
        if not self._latencies:
            return {"avg_ms": 0.0, "p50_ms": 0.0, "p95_ms": 0.0, "p99_ms": 0.0, "min_ms": 0.0, "max_ms": 0.0}
        sorted_lat = sorted(self._latencies)
        n = len(sorted_lat)
        return {
            "avg_ms": round(sum(sorted_lat) / n, 3),
            "p50_ms": round(sorted_lat[int(n * 0.50)], 3),
            "p95_ms": round(sorted_lat[min(int(n * 0.95), n - 1)], 3),
            "p99_ms": round(sorted_lat[min(int(n * 0.99), n - 1)], 3),
            "min_ms": round(sorted_lat[0], 3),
            "max_ms": round(sorted_lat[-1], 3),
        }

    def get_throughput_stats(self) -> Dict[str, Any]:
        """Calculate queries per hour and error rates."""
        now = time.time()
        hour_ago = now - 3600
        queries_last_hour = sum(1 for t in self._query_timestamps if t > hour_ago)
        errors_last_hour = sum(1 for t in self._error_timestamps if t > hour_ago)
        # Prune old timestamps
        self._query_timestamps = [t for t in self._query_timestamps if t > hour_ago]
        self._error_timestamps = [t for t in self._error_timestamps if t > now - 86400]
        return {
            "total_queries": self._total_queries,
            "queries_last_hour": queries_last_hour,
            "errors_last_hour": errors_last_hour,
            "errors_last_24h": len(self._error_timestamps),
            "active_queries": self._active_queries,
            "uptime_seconds": round(now - self._start_time, 1),
        }

    def get_doctrine_stats(self) -> Dict[str, Any]:
        """Get doctrine cache hit/miss statistics."""
        total = self._doctrine_hits + self._doctrine_misses
        return {
            "total_lookups": total,
            "hits": self._doctrine_hits,
            "misses": self._doctrine_misses,
            "hit_rate": round(self._doctrine_hits / total, 4) if total > 0 else 1.0,
        }

    def get_full_metrics(self) -> Dict[str, Any]:
        """Get comprehensive metrics snapshot."""
        return {
            "engine_id": ENGINE_ID,
            "engine_version": ENGINE_VERSION,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "latency": self.get_latency_stats(),
            "throughput": self.get_throughput_stats(),
            "doctrine": self.get_doctrine_stats(),
            "mutations_count": len(self._mutations),
            "trace_buffer_size": len(self._traces),
        }

    def snapshot_metrics(self) -> None:
        """Persist current metrics to disk."""
        metrics = self.get_full_metrics()
        try:
            METRICS_LOG.write_text(json.dumps(metrics, indent=2))
            logger.debug(f"Metrics snapshot saved: {self._total_queries} total queries")
        except Exception as exc:
            logger.warning(f"Failed to save metrics snapshot: {exc}")

    def _persist_trace(self, trace: QueryTrace) -> None:
        """Append trace to JSONL log."""
        try:
            with TRACE_LOG.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(trace.to_dict()) + "\n")
        except Exception as exc:
            logger.warning(f"Failed to persist trace: {exc}")

    def _persist_error(self, error_record: Dict[str, Any]) -> None:
        """Append error to JSONL log."""
        try:
            with ERROR_LOG.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(error_record) + "\n")
        except Exception as exc:
            logger.warning(f"Failed to persist error: {exc}")

    def _persist_mutation(self, mutation: DoctrineMutation) -> None:
        """Append mutation to JSONL log."""
        try:
            with MUTATION_LOG.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(mutation.to_dict()) + "\n")
        except Exception as exc:
            logger.warning(f"Failed to persist mutation: {exc}")

    def _flush_traces(self) -> None:
        """Flush old traces from the in-memory buffer."""
        if len(self._traces) > self._max_trace_buffer:
            self._traces = self._traces[-100:]
            logger.debug("Trace buffer flushed to last 100 entries")


# ==============================================================================
# SINGLETON INSTANCE
# ==============================================================================

_telemetry: Optional[TelemetryCollector] = None


def get_telemetry() -> TelemetryCollector:
    """Get or create the global telemetry collector."""
    global _telemetry
    if _telemetry is None:
        _telemetry = TelemetryCollector()
    return _telemetry


def trace_query(query_id: str, question: str) -> QueryTrace:
    """Convenience: create a new query trace."""
    return get_telemetry().create_trace(query_id, question)


def complete_trace(trace: QueryTrace, layer: ResponseLayer, doctrine_hit: bool,
                   doctrine_topic: Optional[str] = None) -> None:
    """Convenience: complete a query trace."""
    get_telemetry().complete_trace(trace, layer, doctrine_hit, doctrine_topic)


def log_error(domain: ErrorDomain, message: str, trace_id: Optional[str] = None,
              details: Optional[Dict[str, Any]] = None) -> None:
    """Convenience: log an error."""
    get_telemetry().log_error(domain, message, trace_id, details)


def record_doctrine_mutation(mutation_type: MutationType, origin: MutationOrigin,
                             doctrine_topic: str, field_changed: str, description: str,
                             old_value: Optional[str] = None, new_value: Optional[str] = None,
                             approved_by: Optional[str] = None) -> DoctrineMutation:
    """Convenience: record a doctrine mutation."""
    return get_telemetry().record_doctrine_mutation(
        mutation_type, origin, doctrine_topic, field_changed, description,
        old_value, new_value, approved_by
    )
