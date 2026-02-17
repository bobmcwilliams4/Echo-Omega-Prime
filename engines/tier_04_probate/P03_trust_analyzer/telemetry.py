"""
Trust Analyzer Telemetry Module
Full observability for trust analysis queries with structured logging and metrics.
"""

from typing import Optional, Dict, Any, List
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
import json
import uuid
from loguru import logger


class ErrorDomain(str, Enum):
    """Error classification domains"""
    INPUT_VALIDATION = "input_validation"
    DOCTRINE_CACHE = "doctrine_cache"
    SEMANTIC_SEARCH = "semantic_search"
    CLOUD_RETRIEVAL = "cloud_retrieval"
    AUTHORITY_CONFLICT = "authority_conflict"
    EPISTEMIC_VIOLATION = "epistemic_violation"
    INFRASTRUCTURE = "infrastructure"
    UNKNOWN = "unknown"


class ResponseLayer(str, Enum):
    """Which layer produced the response"""
    DOCTRINE_CACHE = "doctrine_cache"
    SEMANTIC_RETRIEVAL = "semantic_retrieval"
    DEEP_ANALYSIS = "deep_analysis"
    FALLBACK = "fallback"


class MutationType(str, Enum):
    """Types of doctrine mutations"""
    BLOCK_ADDED = "block_added"
    BLOCK_MODIFIED = "block_modified"
    BLOCK_DEPRECATED = "block_deprecated"
    AUTHORITY_UPDATED = "authority_updated"
    CONFIDENCE_ADJUSTED = "confidence_adjusted"


class MutationOrigin(str, Enum):
    """Source of doctrine mutation"""
    MANUAL_REVIEW = "manual_review"
    AUTOMATED_DRIFT = "automated_drift"
    AUTHORITY_CHANGE = "authority_change"
    ERROR_CORRECTION = "error_correction"


@dataclass
class QueryTrace:
    """Complete trace of a single query execution"""
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    query_text: str = ""
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None
    latency_ms: Optional[float] = None

    # Query metadata
    response_mode: str = "FAST"
    position_zone: Optional[str] = None
    confidence_stratum: Optional[str] = None

    # Execution path
    layer_used: Optional[ResponseLayer] = None
    doctrines_triggered: List[str] = field(default_factory=list)
    semantic_terms: List[str] = field(default_factory=list)

    # Results
    success: bool = False
    error_domain: Optional[ErrorDomain] = None
    error_message: Optional[str] = None

    # Performance
    cache_hit: bool = False
    cloud_retrieval_ms: Optional[float] = None
    total_tokens: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dict"""
        return {
            "trace_id": self.trace_id,
            "query_text": self.query_text,
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "latency_ms": self.latency_ms,
            "response_mode": self.response_mode,
            "position_zone": self.position_zone,
            "confidence_stratum": self.confidence_stratum,
            "layer_used": self.layer_used.value if self.layer_used else None,
            "doctrines_triggered": self.doctrines_triggered,
            "semantic_terms": self.semantic_terms,
            "success": self.success,
            "error_domain": self.error_domain.value if self.error_domain else None,
            "error_message": self.error_message,
            "cache_hit": self.cache_hit,
            "cloud_retrieval_ms": self.cloud_retrieval_ms,
            "total_tokens": self.total_tokens
        }


class TelemetrySystem:
    """
    Centralized telemetry for trust analyzer engine.
    Handles query tracing, metrics collection, audit logging.
    """

    def __init__(self, log_dir: Path):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.audit_log = self.log_dir / "audit_trail.jsonl"
        self.metrics_log = self.log_dir / "metrics.jsonl"
        self.drift_log = self.log_dir / "doctrine_drift.jsonl"

        # In-memory trace storage (last 1000 queries)
        self._active_traces: Dict[str, QueryTrace] = {}
        self._completed_traces: List[QueryTrace] = []
        self._max_traces = 1000

        # Metrics accumulators
        self.total_queries = 0
        self.total_errors = 0
        self.cache_hits = 0
        self.cache_misses = 0
        self.latencies: List[float] = []

        logger.info(f"Telemetry initialized: {log_dir}")

    def start_trace(self, query_text: str, response_mode: str = "FAST") -> str:
        """Begin tracing a new query"""
        trace = QueryTrace(
            query_text=query_text,
            response_mode=response_mode
        )
        self._active_traces[trace.trace_id] = trace

        logger.debug(f"Trace started: {trace.trace_id} | Mode: {response_mode}")
        return trace.trace_id

    def complete_trace(
        self,
        trace_id: str,
        success: bool = True,
        layer_used: Optional[ResponseLayer] = None,
        doctrines_triggered: Optional[List[str]] = None,
        error_domain: Optional[ErrorDomain] = None,
        error_message: Optional[str] = None,
        cache_hit: bool = False,
        cloud_retrieval_ms: Optional[float] = None
    ):
        """Complete a query trace with results"""
        if trace_id not in self._active_traces:
            logger.warning(f"Trace not found: {trace_id}")
            return

        trace = self._active_traces.pop(trace_id)
        trace.completed_at = datetime.now(timezone.utc)
        trace.latency_ms = (trace.completed_at - trace.started_at).total_seconds() * 1000
        trace.success = success
        trace.layer_used = layer_used
        trace.doctrines_triggered = doctrines_triggered or []
        trace.error_domain = error_domain
        trace.error_message = error_message
        trace.cache_hit = cache_hit
        trace.cloud_retrieval_ms = cloud_retrieval_ms

        # Update metrics
        self.total_queries += 1
        if not success:
            self.total_errors += 1
        if cache_hit:
            self.cache_hits += 1
        else:
            self.cache_misses += 1

        if trace.latency_ms:
            self.latencies.append(trace.latency_ms)
            if len(self.latencies) > 1000:
                self.latencies.pop(0)

        # Store completed trace
        self._completed_traces.append(trace)
        if len(self._completed_traces) > self._max_traces:
            self._completed_traces.pop(0)

        # Write to audit log
        self._write_audit(trace)

        logger.info(
            f"Trace complete: {trace_id} | "
            f"Success: {success} | "
            f"Latency: {trace.latency_ms:.1f}ms | "
            f"Layer: {layer_used.value if layer_used else 'N/A'}"
        )

    def log_error(
        self,
        trace_id: Optional[str],
        error_domain: ErrorDomain,
        error_message: str,
        context: Optional[Dict[str, Any]] = None
    ):
        """Log an error with context"""
        error_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "trace_id": trace_id,
            "error_domain": error_domain.value,
            "error_message": error_message,
            "context": context or {}
        }

        with open(self.log_dir / "errors.jsonl", "a") as f:
            f.write(json.dumps(error_entry) + "\n")

        logger.error(
            f"Error logged: {error_domain.value} | "
            f"Trace: {trace_id} | "
            f"Message: {error_message}"
        )

    def record_doctrine_mutation(
        self,
        mutation_type: MutationType,
        mutation_origin: MutationOrigin,
        doctrine_topic: str,
        details: Dict[str, Any]
    ):
        """Record changes to doctrine blocks"""
        mutation_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "mutation_type": mutation_type.value,
            "mutation_origin": mutation_origin.value,
            "doctrine_topic": doctrine_topic,
            "details": details
        }

        with open(self.drift_log, "a") as f:
            f.write(json.dumps(mutation_entry) + "\n")

        logger.warning(
            f"Doctrine mutation: {mutation_type.value} | "
            f"Topic: {doctrine_topic} | "
            f"Origin: {mutation_origin.value}"
        )

    def get_metrics_snapshot(self) -> Dict[str, Any]:
        """Return current performance metrics"""
        cache_total = self.cache_hits + self.cache_misses
        cache_hit_rate = self.cache_hits / cache_total if cache_total > 0 else 0.0

        latencies_sorted = sorted(self.latencies) if self.latencies else [0.0]
        p50 = latencies_sorted[len(latencies_sorted) // 2]
        p95 = latencies_sorted[int(len(latencies_sorted) * 0.95)]
        p99 = latencies_sorted[int(len(latencies_sorted) * 0.99)]

        error_rate = self.total_errors / self.total_queries if self.total_queries > 0 else 0.0

        return {
            "total_queries": self.total_queries,
            "total_errors": self.total_errors,
            "error_rate": round(error_rate, 4),
            "cache_hit_rate": round(cache_hit_rate, 4),
            "latency_p50_ms": round(p50, 1),
            "latency_p95_ms": round(p95, 1),
            "latency_p99_ms": round(p99, 1),
            "active_traces": len(self._active_traces)
        }

    def _write_audit(self, trace: QueryTrace):
        """Write completed trace to audit log"""
        with open(self.audit_log, "a") as f:
            f.write(json.dumps(trace.to_dict()) + "\n")


# Global telemetry instance
_telemetry: Optional[TelemetrySystem] = None


def init_telemetry(log_dir: Path) -> TelemetrySystem:
    """Initialize global telemetry system"""
    global _telemetry
    _telemetry = TelemetrySystem(log_dir)
    return _telemetry


def get_telemetry() -> TelemetrySystem:
    """Get global telemetry instance"""
    if _telemetry is None:
        raise RuntimeError("Telemetry not initialized. Call init_telemetry() first.")
    return _telemetry


# Convenience functions
def trace_query(query_text: str, response_mode: str = "FAST") -> str:
    """Start a new query trace"""
    return get_telemetry().start_trace(query_text, response_mode)


def complete_trace(
    trace_id: str,
    success: bool = True,
    layer_used: Optional[ResponseLayer] = None,
    doctrines_triggered: Optional[List[str]] = None,
    cache_hit: bool = False,
    **kwargs
):
    """Complete a query trace"""
    get_telemetry().complete_trace(
        trace_id=trace_id,
        success=success,
        layer_used=layer_used,
        doctrines_triggered=doctrines_triggered,
        cache_hit=cache_hit,
        **kwargs
    )


def log_error(
    trace_id: Optional[str],
    error_domain: ErrorDomain,
    error_message: str,
    context: Optional[Dict[str, Any]] = None
):
    """Log an error"""
    get_telemetry().log_error(trace_id, error_domain, error_message, context)


def record_doctrine_mutation(
    mutation_type: MutationType,
    mutation_origin: MutationOrigin,
    doctrine_topic: str,
    details: Dict[str, Any]
):
    """Record doctrine changes"""
    get_telemetry().record_doctrine_mutation(
        mutation_type, mutation_origin, doctrine_topic, details
    )
