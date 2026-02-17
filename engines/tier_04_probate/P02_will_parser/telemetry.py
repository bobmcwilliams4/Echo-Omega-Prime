"""
TELEMETRY AND OBSERVABILITY MODULE — Will Parser Intelligence Engine

Full query tracing, latency tracking, error domain classification, doctrine mutation detection.
Append-only audit trail for forensic review and compliance verification.
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
import json
import uuid
import time
from loguru import logger


# ==============================================================================
# ENUMS AND TYPES
# ==============================================================================

class ResponseLayer(str, Enum):
    """Three-layer response architecture."""
    DOCTRINE_CACHE = "doctrine_cache"
    SEMANTIC_RETRIEVAL = "semantic_retrieval"
    DEEP_ANALYSIS = "deep_analysis"


class ErrorDomain(str, Enum):
    """Error classification taxonomy."""
    PARSING = "parsing"
    DOCTRINE = "doctrine"
    CAPACITY = "capacity"
    EXECUTION = "execution"
    REVOCATION = "revocation"
    CONSTRUCTION = "construction"
    VALIDITY = "validity"
    CONFLICT = "conflict"
    STATUTE = "statute"
    SYSTEM = "system"


class MutationType(str, Enum):
    """Types of doctrine mutations."""
    ADDITION = "addition"
    MODIFICATION = "modification"
    DEPRECATION = "deprecation"
    OVERRIDE = "override"


class MutationOrigin(str, Enum):
    """Source of doctrine mutation."""
    STATUTE_CHANGE = "statute_change"
    CASE_LAW = "case_law"
    MANUAL_OVERRIDE = "manual_override"
    ERROR_CORRECTION = "error_correction"


# ==============================================================================
# TELEMETRY DATA STRUCTURES
# ==============================================================================

@dataclass
class QueryTrace:
    """Complete trace of a single query execution."""
    trace_id: str
    timestamp: str
    query: str
    normalized_query: str
    response_layer: ResponseLayer
    latency_ms: float
    doctrine_topics_matched: List[str]
    vector_search_used: bool
    cache_hit: bool
    confidence_level: str
    error: Optional[str] = None
    error_domain: Optional[ErrorDomain] = None
    statute_references: List[str] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DoctrineMutation:
    """Record of doctrine cache modification."""
    mutation_id: str
    timestamp: str
    mutation_type: MutationType
    origin: MutationOrigin
    doctrine_topic: str
    old_value: Optional[str]
    new_value: str
    authority_citation: str
    approver: str
    notes: str


@dataclass
class PerformanceMetrics:
    """Aggregated performance metrics."""
    total_queries: int
    cache_hits: int
    cache_misses: int
    avg_latency_ms: float
    p95_latency_ms: float
    p99_latency_ms: float
    error_count: int
    error_rate: float


# ==============================================================================
# TELEMETRY COLLECTOR
# ==============================================================================

class TelemetryCollector:
    """
    Centralized telemetry collection for will parser engine.
    Thread-safe, append-only audit trail.
    """

    def __init__(self, log_dir: Path):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.audit_log = self.log_dir / "audit_trail.jsonl"
        self.mutation_log = self.log_dir / "doctrine_mutations.jsonl"
        self.metrics_log = self.log_dir / "performance_metrics.jsonl"

        # In-memory metrics
        self.query_latencies: List[float] = []
        self.cache_hits = 0
        self.cache_misses = 0
        self.total_queries = 0
        self.errors_by_domain: Dict[ErrorDomain, int] = {}
        self.active_traces: Dict[str, QueryTrace] = {}

        logger.info(f"Telemetry collector initialized. Audit log: {self.audit_log}")

    def start_trace(self, query: str, normalized_query: str) -> str:
        """Begin a new query trace."""
        trace_id = str(uuid.uuid4())
        trace = QueryTrace(
            trace_id=trace_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            query=query,
            normalized_query=normalized_query,
            response_layer=ResponseLayer.DOCTRINE_CACHE,  # Default, will update
            latency_ms=0.0,
            doctrine_topics_matched=[],
            vector_search_used=False,
            cache_hit=False,
            confidence_level="UNKNOWN"
        )
        self.active_traces[trace_id] = trace
        return trace_id

    def complete_trace(
        self,
        trace_id: str,
        response_layer: ResponseLayer,
        latency_ms: float,
        doctrine_topics: List[str],
        cache_hit: bool,
        confidence_level: str,
        vector_search_used: bool = False,
        statute_refs: Optional[List[str]] = None,
        context: Optional[Dict[str, Any]] = None
    ):
        """Complete and persist a query trace."""
        if trace_id not in self.active_traces:
            logger.warning(f"Trace {trace_id} not found in active traces")
            return

        trace = self.active_traces[trace_id]
        trace.response_layer = response_layer
        trace.latency_ms = latency_ms
        trace.doctrine_topics_matched = doctrine_topics
        trace.cache_hit = cache_hit
        trace.confidence_level = confidence_level
        trace.vector_search_used = vector_search_used
        if statute_refs:
            trace.statute_references = statute_refs
        if context:
            trace.context = context

        # Update metrics
        self.total_queries += 1
        self.query_latencies.append(latency_ms)
        if len(self.query_latencies) > 1000:  # Keep last 1000
            self.query_latencies.pop(0)
        if cache_hit:
            self.cache_hits += 1
        else:
            self.cache_misses += 1

        # Persist to audit log
        self._append_audit_log(trace)

        # Remove from active traces
        del self.active_traces[trace_id]

    def log_error(
        self,
        trace_id: str,
        error_msg: str,
        error_domain: ErrorDomain
    ):
        """Log error for a query trace."""
        if trace_id in self.active_traces:
            trace = self.active_traces[trace_id]
            trace.error = error_msg
            trace.error_domain = error_domain

        # Update error metrics
        if error_domain in self.errors_by_domain:
            self.errors_by_domain[error_domain] += 1
        else:
            self.errors_by_domain[error_domain] = 1

        logger.error(f"[{error_domain.value}] {error_msg} (trace: {trace_id})")

    def record_doctrine_mutation(
        self,
        mutation_type: MutationType,
        origin: MutationOrigin,
        doctrine_topic: str,
        new_value: str,
        authority_citation: str,
        approver: str,
        notes: str = "",
        old_value: Optional[str] = None
    ):
        """Record a modification to the doctrine cache."""
        mutation = DoctrineMutation(
            mutation_id=str(uuid.uuid4()),
            timestamp=datetime.now(timezone.utc).isoformat(),
            mutation_type=mutation_type,
            origin=origin,
            doctrine_topic=doctrine_topic,
            old_value=old_value,
            new_value=new_value,
            authority_citation=authority_citation,
            approver=approver,
            notes=notes
        )

        self._append_mutation_log(mutation)
        logger.warning(f"Doctrine mutation recorded: {doctrine_topic} ({mutation_type.value})")

    def get_performance_metrics(self) -> PerformanceMetrics:
        """Calculate current performance metrics."""
        if not self.query_latencies:
            return PerformanceMetrics(
                total_queries=0,
                cache_hits=0,
                cache_misses=0,
                avg_latency_ms=0.0,
                p95_latency_ms=0.0,
                p99_latency_ms=0.0,
                error_count=0,
                error_rate=0.0
            )

        sorted_latencies = sorted(self.query_latencies)
        n = len(sorted_latencies)
        p95_idx = int(n * 0.95)
        p99_idx = int(n * 0.99)

        total_errors = sum(self.errors_by_domain.values())
        error_rate = total_errors / max(self.total_queries, 1)

        return PerformanceMetrics(
            total_queries=self.total_queries,
            cache_hits=self.cache_hits,
            cache_misses=self.cache_misses,
            avg_latency_ms=round(sum(self.query_latencies) / n, 2),
            p95_latency_ms=round(sorted_latencies[min(p95_idx, n - 1)], 2),
            p99_latency_ms=round(sorted_latencies[min(p99_idx, n - 1)], 2),
            error_count=total_errors,
            error_rate=round(error_rate, 4)
        )

    def get_error_breakdown(self) -> Dict[str, int]:
        """Get error counts by domain."""
        return {domain.value: count for domain, count in self.errors_by_domain.items()}

    def _append_audit_log(self, trace: QueryTrace):
        """Append trace to audit log (JSONL format)."""
        try:
            with open(self.audit_log, "a", encoding="utf-8") as f:
                f.write(json.dumps(asdict(trace), ensure_ascii=False) + "\n")
        except Exception as e:
            logger.error(f"Failed to write audit log: {e}")

    def _append_mutation_log(self, mutation: DoctrineMutation):
        """Append mutation to mutation log (JSONL format)."""
        try:
            with open(self.mutation_log, "a", encoding="utf-8") as f:
                f.write(json.dumps(asdict(mutation), ensure_ascii=False) + "\n")
        except Exception as e:
            logger.error(f"Failed to write mutation log: {e}")

    def health_check(self) -> Dict[str, Any]:
        """Return telemetry system health status."""
        return {
            "audit_log_exists": self.audit_log.exists(),
            "mutation_log_exists": self.mutation_log.exists(),
            "active_traces": len(self.active_traces),
            "total_queries_tracked": self.total_queries,
            "cache_hit_rate": round(self.cache_hits / max(self.total_queries, 1), 3),
            "error_domains": list(self.errors_by_domain.keys())
        }


# ==============================================================================
# GLOBAL TELEMETRY INSTANCE
# ==============================================================================

_telemetry: Optional[TelemetryCollector] = None


def get_telemetry(log_dir: Optional[Path] = None) -> TelemetryCollector:
    """Get or create global telemetry collector."""
    global _telemetry
    if _telemetry is None:
        if log_dir is None:
            log_dir = Path("O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/P02_will_parser/logs")
        _telemetry = TelemetryCollector(log_dir)
    return _telemetry


# ==============================================================================
# CONVENIENCE FUNCTIONS (match TIE pattern)
# ==============================================================================

def trace_query(query: str, normalized_query: str) -> str:
    """Start a new query trace. Returns trace_id."""
    return get_telemetry().start_trace(query, normalized_query)


def complete_trace(
    trace_id: str,
    response_layer: ResponseLayer,
    latency_ms: float,
    doctrine_topics: List[str],
    cache_hit: bool,
    confidence_level: str,
    **kwargs
):
    """Complete a query trace."""
    get_telemetry().complete_trace(
        trace_id, response_layer, latency_ms, doctrine_topics,
        cache_hit, confidence_level, **kwargs
    )


def log_error(trace_id: str, error_msg: str, error_domain: ErrorDomain):
    """Log an error for a trace."""
    get_telemetry().log_error(trace_id, error_msg, error_domain)


def record_doctrine_mutation(
    mutation_type: MutationType,
    origin: MutationOrigin,
    doctrine_topic: str,
    new_value: str,
    authority_citation: str,
    approver: str,
    **kwargs
):
    """Record a doctrine cache mutation."""
    get_telemetry().record_doctrine_mutation(
        mutation_type, origin, doctrine_topic, new_value,
        authority_citation, approver, **kwargs
    )
