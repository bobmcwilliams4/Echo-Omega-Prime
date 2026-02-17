"""
TX09 AMT CALCULATOR — TELEMETRY MODULE
Query tracing, error tracking, and performance monitoring.

Author: ECHO OMEGA PRIME
Version: 1.0.0
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from enum import Enum
import uuid
import time
import json
from pathlib import Path
from collections import defaultdict


# ============================================================================
# ENUMS
# ============================================================================

class ErrorDomain(str, Enum):
    """Error domain classification."""
    ENGINE = "engine"
    DOCTRINE = "doctrine"
    RETRIEVAL = "retrieval"
    CALCULATION = "calculation"
    VALIDATION = "validation"
    EXTERNAL = "external"


class ResponseLayer(str, Enum):
    """Response layer that handled the query."""
    DOCTRINE = "doctrine"
    RETRIEVAL = "retrieval"
    DEEP_ANALYSIS = "deep_analysis"


class QueryComplexity(str, Enum):
    """Query complexity classification."""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"


# ============================================================================
# DATACLASSES
# ============================================================================

@dataclass
class QueryTrace:
    """Trace record for a single query."""
    trace_id: str
    query_id: str
    query_text: str
    start_time: float
    end_time: Optional[float] = None
    latency_ms: Optional[float] = None
    response_layer: Optional[ResponseLayer] = None
    success: bool = False
    error_domain: Optional[ErrorDomain] = None
    error_message: Optional[str] = None
    doctrine_matches: int = 0
    retrieval_hits: int = 0
    calculation_performed: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ErrorEvent:
    """Error event record."""
    error_id: str
    trace_id: str
    timestamp: str
    domain: ErrorDomain
    message: str
    stack_trace: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PerformanceMetrics:
    """Performance metrics snapshot."""
    timestamp: str
    total_queries: int
    successful_queries: int
    failed_queries: int
    avg_latency_ms: float
    p95_latency_ms: float
    p99_latency_ms: float
    doctrine_hit_rate: float
    error_rate: float
    queries_by_layer: Dict[str, int]
    errors_by_domain: Dict[str, int]


# ============================================================================
# TELEMETRY COLLECTOR
# ============================================================================

class TelemetryCollector:
    """
    Centralized telemetry collection for AMT engine.

    Tracks:
    - Query traces
    - Error events
    - Performance metrics
    - Doctrine coverage
    - Calculation statistics
    """

    def __init__(self, log_dir: Path = None):
        if log_dir is None:
            log_dir = Path("O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/TX09_amt_calculator/logs")
        self.log_dir = log_dir
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # In-memory storage
        self.traces: Dict[str, QueryTrace] = {}
        self.errors: List[ErrorEvent] = []
        self.latencies: List[float] = []
        self.layer_counts: Dict[str, int] = defaultdict(int)
        self.error_counts: Dict[str, int] = defaultdict(int)

        # Counters
        self.total_queries = 0
        self.successful_queries = 0
        self.failed_queries = 0
        self.doctrine_hits = 0
        self.doctrine_misses = 0

        # Paths
        self.trace_log = self.log_dir / "traces.jsonl"
        self.error_log = self.log_dir / "errors.jsonl"
        self.metrics_log = self.log_dir / "metrics.jsonl"

    def start_trace(self, query_id: str, query_text: str) -> str:
        """
        Start a new query trace.

        Args:
            query_id: Unique query identifier
            query_text: Query text

        Returns:
            Trace ID
        """
        trace_id = str(uuid.uuid4())
        trace = QueryTrace(
            trace_id=trace_id,
            query_id=query_id,
            query_text=query_text,
            start_time=time.time()
        )
        self.traces[trace_id] = trace
        self.total_queries += 1
        return trace_id

    def complete_trace(self, trace_id: str, success: bool, latency_ms: float,
                      response_layer: Optional[ResponseLayer] = None,
                      metadata: Optional[Dict[str, Any]] = None):
        """
        Complete a query trace.

        Args:
            trace_id: Trace identifier
            success: Whether query succeeded
            latency_ms: Query latency in milliseconds
            response_layer: Which layer handled the response
            metadata: Additional metadata
        """
        if trace_id not in self.traces:
            return

        trace = self.traces[trace_id]
        trace.end_time = time.time()
        trace.latency_ms = latency_ms
        trace.success = success
        trace.response_layer = response_layer

        if metadata:
            trace.metadata.update(metadata)

        # Update counters
        if success:
            self.successful_queries += 1
        else:
            self.failed_queries += 1

        if response_layer:
            self.layer_counts[response_layer.value] += 1

        self.latencies.append(latency_ms)

        # Keep last 1000 latencies
        if len(self.latencies) > 1000:
            self.latencies = self.latencies[-1000:]

        # Write to log
        self._write_trace(trace)

    def log_error(self, trace_id: str, domain: ErrorDomain, message: str,
                 stack_trace: Optional[str] = None,
                 context: Optional[Dict[str, Any]] = None):
        """
        Log an error event.

        Args:
            trace_id: Associated trace ID
            domain: Error domain
            message: Error message
            stack_trace: Optional stack trace
            context: Additional context
        """
        error_id = str(uuid.uuid4())
        error = ErrorEvent(
            error_id=error_id,
            trace_id=trace_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            domain=domain,
            message=message,
            stack_trace=stack_trace,
            context=context or {}
        )

        self.errors.append(error)
        self.error_counts[domain.value] += 1

        # Keep last 100 errors
        if len(self.errors) > 100:
            self.errors = self.errors[-100:]

        # Write to log
        self._write_error(error)

        # Update trace if exists
        if trace_id in self.traces:
            self.traces[trace_id].error_domain = domain
            self.traces[trace_id].error_message = message

    def record_doctrine_hit(self, trace_id: str, matches: int):
        """Record doctrine cache hit."""
        if trace_id in self.traces:
            self.traces[trace_id].doctrine_matches = matches
        self.doctrine_hits += 1

    def record_doctrine_miss(self, trace_id: str):
        """Record doctrine cache miss."""
        self.doctrine_misses += 1

    def record_retrieval(self, trace_id: str, hits: int):
        """Record retrieval results."""
        if trace_id in self.traces:
            self.traces[trace_id].retrieval_hits = hits

    def record_calculation(self, trace_id: str):
        """Record that AMT calculation was performed."""
        if trace_id in self.traces:
            self.traces[trace_id].calculation_performed = True

    def get_metrics(self) -> PerformanceMetrics:
        """
        Get current performance metrics snapshot.

        Returns:
            PerformanceMetrics instance
        """
        # Calculate latency percentiles
        if self.latencies:
            sorted_lat = sorted(self.latencies)
            avg_lat = sum(self.latencies) / len(self.latencies)
            p95_idx = int(len(sorted_lat) * 0.95)
            p99_idx = int(len(sorted_lat) * 0.99)
            p95_lat = sorted_lat[min(p95_idx, len(sorted_lat) - 1)]
            p99_lat = sorted_lat[min(p99_idx, len(sorted_lat) - 1)]
        else:
            avg_lat = p95_lat = p99_lat = 0.0

        # Calculate hit rate
        total_doctrine_queries = self.doctrine_hits + self.doctrine_misses
        hit_rate = (self.doctrine_hits / total_doctrine_queries) if total_doctrine_queries > 0 else 0.0

        # Calculate error rate
        error_rate = (self.failed_queries / self.total_queries) if self.total_queries > 0 else 0.0

        return PerformanceMetrics(
            timestamp=datetime.now(timezone.utc).isoformat(),
            total_queries=self.total_queries,
            successful_queries=self.successful_queries,
            failed_queries=self.failed_queries,
            avg_latency_ms=round(avg_lat, 2),
            p95_latency_ms=round(p95_lat, 2),
            p99_latency_ms=round(p99_lat, 2),
            doctrine_hit_rate=round(hit_rate, 3),
            error_rate=round(error_rate, 3),
            queries_by_layer=dict(self.layer_counts),
            errors_by_domain=dict(self.error_counts)
        )

    def _write_trace(self, trace: QueryTrace):
        """Write trace to JSONL log."""
        trace_dict = {
            "trace_id": trace.trace_id,
            "query_id": trace.query_id,
            "query_text": trace.query_text,
            "start_time": trace.start_time,
            "end_time": trace.end_time,
            "latency_ms": trace.latency_ms,
            "response_layer": trace.response_layer.value if trace.response_layer else None,
            "success": trace.success,
            "error_domain": trace.error_domain.value if trace.error_domain else None,
            "error_message": trace.error_message,
            "doctrine_matches": trace.doctrine_matches,
            "retrieval_hits": trace.retrieval_hits,
            "calculation_performed": trace.calculation_performed,
            "metadata": trace.metadata
        }

        with self.trace_log.open("a") as f:
            f.write(json.dumps(trace_dict) + "\n")

    def _write_error(self, error: ErrorEvent):
        """Write error to JSONL log."""
        error_dict = {
            "error_id": error.error_id,
            "trace_id": error.trace_id,
            "timestamp": error.timestamp,
            "domain": error.domain.value,
            "message": error.message,
            "stack_trace": error.stack_trace,
            "context": error.context
        }

        with self.error_log.open("a") as f:
            f.write(json.dumps(error_dict) + "\n")

    def write_metrics_snapshot(self):
        """Write current metrics snapshot to log."""
        metrics = self.get_metrics()
        metrics_dict = {
            "timestamp": metrics.timestamp,
            "total_queries": metrics.total_queries,
            "successful_queries": metrics.successful_queries,
            "failed_queries": metrics.failed_queries,
            "avg_latency_ms": metrics.avg_latency_ms,
            "p95_latency_ms": metrics.p95_latency_ms,
            "p99_latency_ms": metrics.p99_latency_ms,
            "doctrine_hit_rate": metrics.doctrine_hit_rate,
            "error_rate": metrics.error_rate,
            "queries_by_layer": metrics.queries_by_layer,
            "errors_by_domain": metrics.errors_by_domain
        }

        with self.metrics_log.open("a") as f:
            f.write(json.dumps(metrics_dict) + "\n")

    def reset_metrics(self):
        """Reset all metrics (for testing or periodic reset)."""
        self.traces.clear()
        self.errors.clear()
        self.latencies.clear()
        self.layer_counts.clear()
        self.error_counts.clear()
        self.total_queries = 0
        self.successful_queries = 0
        self.failed_queries = 0
        self.doctrine_hits = 0
        self.doctrine_misses = 0


# ============================================================================
# GLOBAL TELEMETRY INSTANCE
# ============================================================================

_telemetry: Optional[TelemetryCollector] = None


def get_telemetry() -> TelemetryCollector:
    """Get global telemetry collector instance."""
    global _telemetry
    if _telemetry is None:
        _telemetry = TelemetryCollector()
    return _telemetry


def trace_query(query_id: str, query_text: str) -> str:
    """Start tracing a query."""
    return get_telemetry().start_trace(query_id, query_text)


def complete_trace(trace_id: str, success: bool, latency_ms: float,
                  response_layer: Optional[ResponseLayer] = None,
                  metadata: Optional[Dict[str, Any]] = None):
    """Complete a query trace."""
    get_telemetry().complete_trace(trace_id, success, latency_ms, response_layer, metadata)


def log_error(trace_id: str, domain: ErrorDomain, message: str,
             stack_trace: Optional[str] = None,
             context: Optional[Dict[str, Any]] = None):
    """Log an error."""
    get_telemetry().log_error(trace_id, domain, message, stack_trace, context)


def record_doctrine_hit(trace_id: str, matches: int):
    """Record doctrine cache hit."""
    get_telemetry().record_doctrine_hit(trace_id, matches)


def record_doctrine_miss(trace_id: str):
    """Record doctrine cache miss."""
    get_telemetry().record_doctrine_miss(trace_id)


def record_retrieval(trace_id: str, hits: int):
    """Record retrieval results."""
    get_telemetry().record_retrieval(trace_id, hits)


def record_calculation(trace_id: str):
    """Record AMT calculation."""
    get_telemetry().record_calculation(trace_id)


# ============================================================================
# ANALYSIS UTILITIES
# ============================================================================

def analyze_trace_log(log_path: Path, hours: int = 24) -> Dict[str, Any]:
    """
    Analyze trace log for the last N hours.

    Args:
        log_path: Path to trace log file
        hours: Number of hours to analyze

    Returns:
        Analysis summary
    """
    if not log_path.exists():
        return {"error": "Log file not found"}

    cutoff = time.time() - (hours * 3600)
    traces = []

    with log_path.open("r") as f:
        for line in f:
            try:
                trace = json.loads(line)
                if trace.get("start_time", 0) >= cutoff:
                    traces.append(trace)
            except json.JSONDecodeError:
                continue

    if not traces:
        return {"traces": 0, "message": "No traces in specified time window"}

    # Calculate statistics
    latencies = [t["latency_ms"] for t in traces if t.get("latency_ms")]
    successes = sum(1 for t in traces if t.get("success"))
    failures = len(traces) - successes

    layers = defaultdict(int)
    for t in traces:
        if t.get("response_layer"):
            layers[t["response_layer"]] += 1

    return {
        "time_window_hours": hours,
        "total_traces": len(traces),
        "successful": successes,
        "failed": failures,
        "success_rate": round(successes / len(traces), 3) if traces else 0,
        "avg_latency_ms": round(sum(latencies) / len(latencies), 2) if latencies else 0,
        "max_latency_ms": round(max(latencies), 2) if latencies else 0,
        "min_latency_ms": round(min(latencies), 2) if latencies else 0,
        "layers": dict(layers)
    }


def analyze_error_log(log_path: Path, hours: int = 24) -> Dict[str, Any]:
    """
    Analyze error log for the last N hours.

    Args:
        log_path: Path to error log file
        hours: Number of hours to analyze

    Returns:
        Error analysis summary
    """
    if not log_path.exists():
        return {"error": "Log file not found"}

    cutoff_time = datetime.now(timezone.utc).timestamp() - (hours * 3600)
    errors = []

    with log_path.open("r") as f:
        for line in f:
            try:
                error = json.loads(line)
                error_time = datetime.fromisoformat(error["timestamp"]).timestamp()
                if error_time >= cutoff_time:
                    errors.append(error)
            except (json.JSONDecodeError, KeyError, ValueError):
                continue

    if not errors:
        return {"errors": 0, "message": "No errors in specified time window"}

    # Group by domain
    by_domain = defaultdict(int)
    for e in errors:
        by_domain[e.get("domain", "unknown")] += 1

    # Group by message (top 5)
    by_message = defaultdict(int)
    for e in errors:
        msg = e.get("message", "")[:50]  # First 50 chars
        by_message[msg] += 1

    top_messages = sorted(by_message.items(), key=lambda x: x[1], reverse=True)[:5]

    return {
        "time_window_hours": hours,
        "total_errors": len(errors),
        "by_domain": dict(by_domain),
        "top_messages": [{"message": msg, "count": count} for msg, count in top_messages]
    }
