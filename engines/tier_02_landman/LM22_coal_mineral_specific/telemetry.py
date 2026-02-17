"""
LM22 Coal/Mineral Specific — Telemetry Module
Full query tracing, latency tracking, error domains, and audit trail.

Author: ECHO OMEGA PRIME
Engine: LM22 Coal/Mineral Specific
"""

import json
import time
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional
from loguru import logger


# ==============================================================================
# ENUMS
# ==============================================================================

class ResponseLayer(str, Enum):
    """Which layer handled the response."""
    DOCTRINE_CACHE = "doctrine_cache"
    SEMANTIC_RETRIEVAL = "semantic_retrieval"
    DEEP_ANALYSIS = "deep_analysis"
    ERROR_FALLBACK = "error_fallback"


class ErrorDomain(str, Enum):
    """Classification of error origin."""
    NORMALIZATION = "normalization"
    DOCTRINE_LOOKUP = "doctrine_lookup"
    SEARCH = "search"
    ANALYSIS = "analysis"
    SERIALIZATION = "serialization"
    VALIDATION = "validation"
    NETWORK = "network"
    UNKNOWN = "unknown"


class MutationType(str, Enum):
    """Type of doctrine mutation."""
    DOCTRINE_ADDED = "doctrine_added"
    DOCTRINE_MODIFIED = "doctrine_modified"
    DOCTRINE_REMOVED = "doctrine_removed"
    KEYWORD_ADDED = "keyword_added"
    CONFIDENCE_CHANGED = "confidence_changed"
    AUTHORITY_UPDATED = "authority_updated"


class MutationOrigin(str, Enum):
    """Origin of a doctrine mutation."""
    MANUAL = "manual"
    AUTOMATED = "automated"
    DRIFT_CORRECTION = "drift_correction"
    COVERAGE_GAP_FILL = "coverage_gap_fill"


# ==============================================================================
# TRACE DATA MODELS
# ==============================================================================

@dataclass
class TraceSpan:
    """A single span within a query trace."""
    span_id: str
    operation: str
    start_time: float
    end_time: float = 0.0
    duration_ms: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None

    def complete(self, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Mark span as complete."""
        self.end_time = time.perf_counter()
        self.duration_ms = round((self.end_time - self.start_time) * 1000, 2)
        if metadata:
            self.metadata.update(metadata)


@dataclass
class QueryTrace:
    """Full trace for a single query through the engine."""
    trace_id: str
    query: str
    session_id: str
    timestamp: str
    response_layer: Optional[ResponseLayer] = None
    response_mode: Optional[str] = None
    total_latency_ms: float = 0.0
    doctrine_hit: bool = False
    doctrine_topic: Optional[str] = None
    normalization_result: Optional[str] = None
    confidence: Optional[str] = None
    spans: List[TraceSpan] = field(default_factory=list)
    error: Optional[str] = None
    error_domain: Optional[ErrorDomain] = None

    def add_span(self, operation: str) -> TraceSpan:
        """Create and add a new span to this trace."""
        span = TraceSpan(
            span_id=str(uuid.uuid4())[:8],
            operation=operation,
            start_time=time.perf_counter(),
        )
        self.spans.append(span)
        return span

    def to_dict(self) -> Dict[str, Any]:
        """Serialize trace to dictionary."""
        result = {
            "trace_id": self.trace_id,
            "query": self.query,
            "session_id": self.session_id,
            "timestamp": self.timestamp,
            "response_layer": self.response_layer.value if self.response_layer else None,
            "response_mode": self.response_mode,
            "total_latency_ms": self.total_latency_ms,
            "doctrine_hit": self.doctrine_hit,
            "doctrine_topic": self.doctrine_topic,
            "normalization_result": self.normalization_result,
            "confidence": self.confidence,
            "error": self.error,
            "error_domain": self.error_domain.value if self.error_domain else None,
            "spans": [
                {
                    "span_id": s.span_id,
                    "operation": s.operation,
                    "duration_ms": s.duration_ms,
                    "metadata": s.metadata,
                    "error": s.error,
                }
                for s in self.spans
            ],
        }
        return result


@dataclass
class DoctrineMutation:
    """Record of a doctrine change for drift tracking."""
    mutation_id: str
    timestamp: str
    mutation_type: MutationType
    origin: MutationOrigin
    doctrine_topic: str
    field_changed: str
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    reason: str = ""


# ==============================================================================
# TELEMETRY ENGINE
# ==============================================================================

class TelemetryEngine:
    """
    Central telemetry system for LM22 Coal/Mineral Specific engine.
    Tracks queries, errors, latencies, doctrine mutations, and audit trail.
    """

    def __init__(self, log_dir: Optional[Path] = None) -> None:
        self._log_dir = log_dir or Path("O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/LM22_coal_mineral_specific/logs")
        self._log_dir.mkdir(parents=True, exist_ok=True)
        self._audit_log = self._log_dir / "audit_trail.jsonl"
        self._session_id = str(uuid.uuid4())[:12]

        # Metrics accumulators
        self._query_count: int = 0
        self._error_count: int = 0
        self._doctrine_hits: int = 0
        self._doctrine_misses: int = 0
        self._latencies: List[float] = []
        self._errors: List[Dict[str, Any]] = []
        self._mutations: List[DoctrineMutation] = []
        self._active_traces: Dict[str, QueryTrace] = {}
        self._completed_traces: List[QueryTrace] = []
        self._max_completed_traces: int = 500

        # Per-layer latency tracking
        self._layer_latencies: Dict[str, List[float]] = {
            ResponseLayer.DOCTRINE_CACHE.value: [],
            ResponseLayer.SEMANTIC_RETRIEVAL.value: [],
            ResponseLayer.DEEP_ANALYSIS.value: [],
        }

        logger.info(f"Telemetry engine initialized. Session: {self._session_id}, Log dir: {self._log_dir}")

    @property
    def session_id(self) -> str:
        """Current telemetry session ID."""
        return self._session_id

    # --------------------------------------------------------------------------
    # QUERY TRACING
    # --------------------------------------------------------------------------

    def trace_query(self, query: str) -> QueryTrace:
        """Start a new query trace."""
        trace = QueryTrace(
            trace_id=str(uuid.uuid4())[:12],
            query=query,
            session_id=self._session_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        self._active_traces[trace.trace_id] = trace
        self._query_count += 1
        return trace

    def complete_trace(
        self,
        trace: QueryTrace,
        response_layer: ResponseLayer,
        doctrine_hit: bool,
        doctrine_topic: Optional[str] = None,
        confidence: Optional[str] = None,
        response_mode: Optional[str] = None,
    ) -> None:
        """Complete a query trace and record metrics."""
        total_latency = sum(s.duration_ms for s in trace.spans)
        trace.total_latency_ms = round(total_latency, 2)
        trace.response_layer = response_layer
        trace.doctrine_hit = doctrine_hit
        trace.doctrine_topic = doctrine_topic
        trace.confidence = confidence
        trace.response_mode = response_mode

        # Record metrics
        self._latencies.append(trace.total_latency_ms)
        if len(self._latencies) > 1000:
            self._latencies = self._latencies[-500:]

        if doctrine_hit:
            self._doctrine_hits += 1
        else:
            self._doctrine_misses += 1

        # Track per-layer latency
        layer_key = response_layer.value
        if layer_key in self._layer_latencies:
            self._layer_latencies[layer_key].append(trace.total_latency_ms)
            if len(self._layer_latencies[layer_key]) > 500:
                self._layer_latencies[layer_key] = self._layer_latencies[layer_key][-250:]

        # Move from active to completed
        self._active_traces.pop(trace.trace_id, None)
        self._completed_traces.append(trace)
        if len(self._completed_traces) > self._max_completed_traces:
            self._completed_traces = self._completed_traces[-250:]

        # Write audit log entry
        self._write_audit_entry(trace)

        logger.debug(
            f"Trace {trace.trace_id} complete: {response_layer.value}, "
            f"{trace.total_latency_ms}ms, hit={doctrine_hit}"
        )

    # --------------------------------------------------------------------------
    # ERROR TRACKING
    # --------------------------------------------------------------------------

    def log_error(
        self,
        error_domain: ErrorDomain,
        error_msg: str,
        trace: Optional[QueryTrace] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Log an error with domain classification."""
        self._error_count += 1
        error_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "domain": error_domain.value,
            "message": error_msg[:500],
            "trace_id": trace.trace_id if trace else None,
            "context": context or {},
        }
        self._errors.append(error_entry)
        if len(self._errors) > 500:
            self._errors = self._errors[-250:]

        if trace:
            trace.error = error_msg[:500]
            trace.error_domain = error_domain

        logger.error(f"[{error_domain.value}] {error_msg[:200]}")

    # --------------------------------------------------------------------------
    # DOCTRINE MUTATION TRACKING
    # --------------------------------------------------------------------------

    def record_doctrine_mutation(
        self,
        mutation_type: MutationType,
        origin: MutationOrigin,
        doctrine_topic: str,
        field_changed: str,
        old_value: Optional[str] = None,
        new_value: Optional[str] = None,
        reason: str = "",
    ) -> DoctrineMutation:
        """Record a doctrine mutation for drift detection."""
        mutation = DoctrineMutation(
            mutation_id=str(uuid.uuid4())[:12],
            timestamp=datetime.now(timezone.utc).isoformat(),
            mutation_type=mutation_type,
            origin=origin,
            doctrine_topic=doctrine_topic,
            field_changed=field_changed,
            old_value=old_value[:200] if old_value else None,
            new_value=new_value[:200] if new_value else None,
            reason=reason,
        )
        self._mutations.append(mutation)
        logger.info(
            f"Doctrine mutation: {mutation_type.value} on {doctrine_topic}.{field_changed} "
            f"(origin={origin.value})"
        )
        return mutation

    # --------------------------------------------------------------------------
    # METRICS
    # --------------------------------------------------------------------------

    def get_latency_stats(self) -> Dict[str, float]:
        """Calculate latency statistics."""
        if not self._latencies:
            return {"avg_ms": 0.0, "p50_ms": 0.0, "p95_ms": 0.0, "p99_ms": 0.0, "min_ms": 0.0, "max_ms": 0.0}

        sorted_lat = sorted(self._latencies)
        n = len(sorted_lat)
        return {
            "avg_ms": round(sum(sorted_lat) / n, 2),
            "p50_ms": round(sorted_lat[int(n * 0.50)], 2),
            "p95_ms": round(sorted_lat[min(int(n * 0.95), n - 1)], 2),
            "p99_ms": round(sorted_lat[min(int(n * 0.99), n - 1)], 2),
            "min_ms": round(sorted_lat[0], 2),
            "max_ms": round(sorted_lat[-1], 2),
        }

    def get_layer_latencies(self) -> Dict[str, Dict[str, float]]:
        """Get per-layer latency statistics."""
        result: Dict[str, Dict[str, float]] = {}
        for layer, latencies in self._layer_latencies.items():
            if latencies:
                sorted_lat = sorted(latencies)
                n = len(sorted_lat)
                result[layer] = {
                    "avg_ms": round(sum(sorted_lat) / n, 2),
                    "p95_ms": round(sorted_lat[min(int(n * 0.95), n - 1)], 2),
                    "count": n,
                }
            else:
                result[layer] = {"avg_ms": 0.0, "p95_ms": 0.0, "count": 0}
        return result

    def get_error_stats(self) -> Dict[str, Any]:
        """Calculate error statistics."""
        domain_counts: Dict[str, int] = {}
        for err in self._errors:
            domain = err.get("domain", "unknown")
            domain_counts[domain] = domain_counts.get(domain, 0) + 1

        return {
            "total_errors": self._error_count,
            "recent_errors": len(self._errors),
            "error_rate": round(self._error_count / max(self._query_count, 1), 4),
            "by_domain": domain_counts,
            "last_error": self._errors[-1] if self._errors else None,
        }

    def get_doctrine_hit_rate(self) -> float:
        """Calculate doctrine cache hit rate."""
        total = self._doctrine_hits + self._doctrine_misses
        if total == 0:
            return 0.0
        return round(self._doctrine_hits / total, 4)

    def get_full_metrics(self) -> Dict[str, Any]:
        """Return comprehensive telemetry metrics."""
        return {
            "session_id": self._session_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "queries": {
                "total": self._query_count,
                "active": len(self._active_traces),
                "completed": len(self._completed_traces),
            },
            "doctrine": {
                "hits": self._doctrine_hits,
                "misses": self._doctrine_misses,
                "hit_rate": self.get_doctrine_hit_rate(),
            },
            "latency": self.get_latency_stats(),
            "layer_latencies": self.get_layer_latencies(),
            "errors": self.get_error_stats(),
            "mutations": {
                "total": len(self._mutations),
                "recent": [
                    {
                        "mutation_id": m.mutation_id,
                        "type": m.mutation_type.value,
                        "topic": m.doctrine_topic,
                        "timestamp": m.timestamp,
                    }
                    for m in self._mutations[-10:]
                ],
            },
        }

    # --------------------------------------------------------------------------
    # AUDIT TRAIL
    # --------------------------------------------------------------------------

    def _write_audit_entry(self, trace: QueryTrace) -> None:
        """Append a trace to the JSONL audit trail file."""
        try:
            entry = trace.to_dict()
            with self._audit_log.open("a", encoding="utf-8") as f:
                f.write(json.dumps(entry, default=str) + "\n")
        except Exception as exc:
            logger.warning(f"Failed to write audit entry: {exc}")

    def get_audit_trail(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Read recent audit trail entries."""
        entries: List[Dict[str, Any]] = []
        try:
            if self._audit_log.exists():
                lines = self._audit_log.read_text(encoding="utf-8").strip().split("\n")
                for line in lines[-limit:]:
                    if line.strip():
                        entries.append(json.loads(line))
        except Exception as exc:
            logger.warning(f"Failed to read audit trail: {exc}")
        return entries


# ==============================================================================
# MODULE-LEVEL SINGLETON
# ==============================================================================

_telemetry: Optional[TelemetryEngine] = None


def get_telemetry() -> TelemetryEngine:
    """Get or create the singleton telemetry engine."""
    global _telemetry
    if _telemetry is None:
        _telemetry = TelemetryEngine()
    return _telemetry


def trace_query(query: str) -> QueryTrace:
    """Convenience: start a new query trace."""
    return get_telemetry().trace_query(query)


def complete_trace(
    trace: QueryTrace,
    response_layer: ResponseLayer,
    doctrine_hit: bool,
    doctrine_topic: Optional[str] = None,
    confidence: Optional[str] = None,
    response_mode: Optional[str] = None,
) -> None:
    """Convenience: complete a query trace."""
    get_telemetry().complete_trace(
        trace=trace,
        response_layer=response_layer,
        doctrine_hit=doctrine_hit,
        doctrine_topic=doctrine_topic,
        confidence=confidence,
        response_mode=response_mode,
    )


def log_error(
    error_domain: ErrorDomain,
    error_msg: str,
    trace: Optional[QueryTrace] = None,
    context: Optional[Dict[str, Any]] = None,
) -> None:
    """Convenience: log an error."""
    get_telemetry().log_error(error_domain, error_msg, trace, context)


def record_doctrine_mutation(
    mutation_type: MutationType,
    origin: MutationOrigin,
    doctrine_topic: str,
    field_changed: str,
    old_value: Optional[str] = None,
    new_value: Optional[str] = None,
    reason: str = "",
) -> DoctrineMutation:
    """Convenience: record a doctrine mutation."""
    return get_telemetry().record_doctrine_mutation(
        mutation_type=mutation_type,
        origin=origin,
        doctrine_topic=doctrine_topic,
        field_changed=field_changed,
        old_value=old_value,
        new_value=new_value,
        reason=reason,
    )
