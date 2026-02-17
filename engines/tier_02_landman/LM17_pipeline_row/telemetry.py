"""
LM17 Pipeline ROW Engine - Telemetry Module
============================================
Full query tracing, latency tracking, error domain classification,
metrics aggregation, and performance monitoring for the Pipeline ROW
intelligence engine.

Engine ID: LM17 | Port: 8517
TIE Gold Standard Telemetry Implementation
"""

from __future__ import annotations

import hashlib
import json
import statistics
import time
import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Optional

from loguru import logger
from pydantic import BaseModel, Field


# ============================================================================
# CONSTANTS
# ============================================================================

ENGINE_ID: str = "LM17"
ENGINE_NAME: str = "Pipeline ROW"
ENGINE_VERSION: str = "1.0.0"
TELEMETRY_VERSION: str = "1.0.0"
MAX_TRACE_HISTORY: int = 10_000
MAX_ERROR_HISTORY: int = 5_000
LATENCY_BUCKET_BOUNDARIES_MS: list[float] = [10, 50, 100, 200, 500, 1000, 2000, 5000, 10000]
AUDIT_LOG_DIR: Path = Path(__file__).parent / "audit_logs"
METRICS_SNAPSHOT_DIR: Path = Path(__file__).parent / "metrics_snapshots"


class ErrorDomain(str, Enum):
    """Classification of error domains for pipeline ROW queries."""
    DOCTRINE_CACHE = "doctrine_cache"
    SEMANTIC_RETRIEVAL = "semantic_retrieval"
    DEEP_ANALYSIS = "deep_analysis"
    AUTHORITY_RESOLUTION = "authority_resolution"
    VECTOR_SEARCH = "vector_search"
    INPUT_VALIDATION = "input_validation"
    CONFIDENCE_SCORING = "confidence_scoring"
    NORMALIZATION = "normalization"
    DRIFT_DETECTION = "drift_detection"
    SERIALIZATION = "serialization"
    NETWORK = "network"
    UNKNOWN = "unknown"


class QueryPhase(str, Enum):
    """Phases of query processing pipeline."""
    RECEIVED = "received"
    VALIDATED = "validated"
    NORMALIZED = "normalized"
    CACHE_LOOKUP = "cache_lookup"
    CACHE_HIT = "cache_hit"
    CACHE_MISS = "cache_miss"
    SEMANTIC_SEARCH = "semantic_search"
    DEEP_ANALYSIS = "deep_analysis"
    AUTHORITY_HARDENING = "authority_hardening"
    CONFIDENCE_SCORING = "confidence_scoring"
    FRAGILITY_SCORING = "fragility_scoring"
    RESPONSE_ASSEMBLY = "response_assembly"
    COMPLETED = "completed"
    FAILED = "failed"


class ResponseTier(str, Enum):
    """Which tier produced the final response."""
    DOCTRINE_CACHE = "doctrine_cache"
    SEMANTIC_RETRIEVAL = "semantic_retrieval"
    DEEP_ANALYSIS = "deep_analysis"


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class TraceEvent(BaseModel):
    """A single event in a query trace."""
    phase: QueryPhase
    timestamp_utc: str
    elapsed_ms: float
    details: dict[str, Any] = Field(default_factory=dict)
    error: Optional[str] = None


class QueryTrace(BaseModel):
    """Full trace of a single query through the engine."""
    trace_id: str
    query_id: str
    query_text: str
    query_hash: str
    start_time_utc: str
    end_time_utc: Optional[str] = None
    total_elapsed_ms: float = 0.0
    response_tier: Optional[ResponseTier] = None
    events: list[TraceEvent] = Field(default_factory=list)
    doctrine_topics_matched: list[str] = Field(default_factory=list)
    issue_categories: list[str] = Field(default_factory=list)
    confidence_level: Optional[str] = None
    error_domain: Optional[ErrorDomain] = None
    determinism_hash: Optional[str] = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class ErrorRecord(BaseModel):
    """Record of an error occurrence."""
    error_id: str
    timestamp_utc: str
    error_domain: ErrorDomain
    error_type: str
    error_message: str
    query_id: Optional[str] = None
    trace_id: Optional[str] = None
    stack_trace: Optional[str] = None
    recovery_action: Optional[str] = None
    resolved: bool = False


class LatencyBucket(BaseModel):
    """Latency distribution bucket."""
    lower_bound_ms: float
    upper_bound_ms: float
    count: int = 0


class MetricsSnapshot(BaseModel):
    """Point-in-time metrics snapshot."""
    engine_id: str = ENGINE_ID
    engine_name: str = ENGINE_NAME
    engine_version: str = ENGINE_VERSION
    snapshot_time_utc: str
    uptime_seconds: float
    total_queries: int = 0
    successful_queries: int = 0
    failed_queries: int = 0
    error_rate: float = 0.0
    cache_hits: int = 0
    cache_misses: int = 0
    cache_hit_rate: float = 0.0
    semantic_retrievals: int = 0
    deep_analyses: int = 0
    avg_latency_ms: float = 0.0
    p50_latency_ms: float = 0.0
    p95_latency_ms: float = 0.0
    p99_latency_ms: float = 0.0
    min_latency_ms: float = 0.0
    max_latency_ms: float = 0.0
    queries_per_minute: float = 0.0
    latency_buckets: list[LatencyBucket] = Field(default_factory=list)
    error_counts_by_domain: dict[str, int] = Field(default_factory=dict)
    top_doctrine_topics: list[dict[str, Any]] = Field(default_factory=list)
    top_issue_categories: list[dict[str, Any]] = Field(default_factory=list)
    active_traces: int = 0


class HealthTelemetry(BaseModel):
    """Telemetry component of health check response."""
    status: str = "operational"
    total_queries_processed: int = 0
    error_rate_percent: float = 0.0
    avg_response_ms: float = 0.0
    cache_hit_rate_percent: float = 0.0
    uptime_seconds: float = 0.0
    active_traces: int = 0
    last_error: Optional[str] = None
    last_error_time: Optional[str] = None


# ============================================================================
# TRACE CONTEXT MANAGER
# ============================================================================

@dataclass
class TraceContext:
    """Context manager for tracing a query through the engine."""
    query_text: str
    query_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    _start_time: float = field(default=0.0, init=False)
    _events: list[TraceEvent] = field(default_factory=list, init=False)
    _phase_start: float = field(default=0.0, init=False)
    _collector: Optional[MetricsCollector] = field(default=None, init=False)

    def bind_collector(self, collector: MetricsCollector) -> TraceContext:
        """Bind a metrics collector to this trace context."""
        self._collector = collector
        return self

    def start(self) -> TraceContext:
        """Start the trace."""
        self._start_time = time.perf_counter()
        self._phase_start = self._start_time
        self.add_event(QueryPhase.RECEIVED)
        logger.debug(
            "Trace started | trace_id={} query_id={} query={}",
            self.trace_id, self.query_id, self.query_text[:80]
        )
        return self

    def add_event(
        self,
        phase: QueryPhase,
        details: Optional[dict[str, Any]] = None,
        error: Optional[str] = None,
    ) -> TraceEvent:
        """Record a phase event in the trace."""
        now = time.perf_counter()
        elapsed = (now - self._phase_start) * 1000.0
        self._phase_start = now
        event = TraceEvent(
            phase=phase,
            timestamp_utc=datetime.now(timezone.utc).isoformat(),
            elapsed_ms=round(elapsed, 3),
            details=details or {},
            error=error,
        )
        self._events.append(event)
        if error:
            logger.warning(
                "Trace event error | trace_id={} phase={} error={}",
                self.trace_id, phase.value, error,
            )
        else:
            logger.trace(
                "Trace event | trace_id={} phase={} elapsed_ms={:.1f}",
                self.trace_id, phase.value, elapsed,
            )
        return event

    def complete(
        self,
        response_tier: ResponseTier,
        doctrine_topics: Optional[list[str]] = None,
        issue_categories: Optional[list[str]] = None,
        confidence_level: Optional[str] = None,
        determinism_hash: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> QueryTrace:
        """Complete the trace and return the full query trace record."""
        total_elapsed = (time.perf_counter() - self._start_time) * 1000.0
        self.add_event(QueryPhase.COMPLETED, {"response_tier": response_tier.value})
        query_hash = hashlib.sha256(self.query_text.encode()).hexdigest()[:16]
        trace = QueryTrace(
            trace_id=self.trace_id,
            query_id=self.query_id,
            query_text=self.query_text,
            query_hash=query_hash,
            start_time_utc=self._events[0].timestamp_utc if self._events else "",
            end_time_utc=datetime.now(timezone.utc).isoformat(),
            total_elapsed_ms=round(total_elapsed, 3),
            response_tier=response_tier,
            events=list(self._events),
            doctrine_topics_matched=doctrine_topics or [],
            issue_categories=issue_categories or [],
            confidence_level=confidence_level,
            determinism_hash=determinism_hash,
            metadata=metadata or {},
        )
        if self._collector:
            self._collector.record_trace(trace)
        logger.info(
            "Trace completed | trace_id={} tier={} elapsed_ms={:.1f} doctrines={} confidence={}",
            self.trace_id, response_tier.value, total_elapsed,
            len(doctrine_topics or []), confidence_level,
        )
        return trace

    def fail(self, error_domain: ErrorDomain, error_message: str) -> QueryTrace:
        """Record a failed trace."""
        total_elapsed = (time.perf_counter() - self._start_time) * 1000.0
        self.add_event(QueryPhase.FAILED, {"error_domain": error_domain.value}, error=error_message)
        query_hash = hashlib.sha256(self.query_text.encode()).hexdigest()[:16]
        trace = QueryTrace(
            trace_id=self.trace_id,
            query_id=self.query_id,
            query_text=self.query_text,
            query_hash=query_hash,
            start_time_utc=self._events[0].timestamp_utc if self._events else "",
            end_time_utc=datetime.now(timezone.utc).isoformat(),
            total_elapsed_ms=round(total_elapsed, 3),
            events=list(self._events),
            error_domain=error_domain,
        )
        if self._collector:
            self._collector.record_trace(trace)
            self._collector.record_error(
                error_domain=error_domain,
                error_type="query_failure",
                error_message=error_message,
                query_id=self.query_id,
                trace_id=self.trace_id,
            )
        logger.error(
            "Trace failed | trace_id={} domain={} error={} elapsed_ms={:.1f}",
            self.trace_id, error_domain.value, error_message, total_elapsed,
        )
        return trace


# ============================================================================
# METRICS COLLECTOR
# ============================================================================

class MetricsCollector:
    """
    Central metrics collection and aggregation for the Pipeline ROW engine.
    Tracks latencies, error rates, cache performance, doctrine coverage,
    and provides real-time performance snapshots.
    """

    def __init__(self) -> None:
        self._start_time: float = time.time()
        self._traces: list[QueryTrace] = []
        self._errors: list[ErrorRecord] = []
        self._latencies: list[float] = []
        self._cache_hits: int = 0
        self._cache_misses: int = 0
        self._semantic_retrievals: int = 0
        self._deep_analyses: int = 0
        self._total_queries: int = 0
        self._successful_queries: int = 0
        self._failed_queries: int = 0
        self._doctrine_topic_counts: defaultdict[str, int] = defaultdict(int)
        self._issue_category_counts: defaultdict[str, int] = defaultdict(int)
        self._error_domain_counts: defaultdict[str, int] = defaultdict(int)
        self._latency_buckets: list[LatencyBucket] = self._init_buckets()
        self._last_error: Optional[ErrorRecord] = None
        self._active_traces: int = 0

        AUDIT_LOG_DIR.mkdir(parents=True, exist_ok=True)
        METRICS_SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
        logger.info("MetricsCollector initialized for {} v{}", ENGINE_NAME, ENGINE_VERSION)

    def _init_buckets(self) -> list[LatencyBucket]:
        """Initialize latency distribution buckets."""
        buckets: list[LatencyBucket] = []
        prev = 0.0
        for boundary in LATENCY_BUCKET_BOUNDARIES_MS:
            buckets.append(LatencyBucket(lower_bound_ms=prev, upper_bound_ms=boundary))
            prev = boundary
        buckets.append(LatencyBucket(lower_bound_ms=prev, upper_bound_ms=float("inf")))
        return buckets

    def create_trace(self, query_text: str, query_id: Optional[str] = None) -> TraceContext:
        """Create a new trace context bound to this collector."""
        self._active_traces += 1
        ctx = TraceContext(
            query_text=query_text,
            query_id=query_id or str(uuid.uuid4()),
        )
        ctx.bind_collector(self)
        return ctx.start()

    def record_trace(self, trace: QueryTrace) -> None:
        """Record a completed or failed trace."""
        self._active_traces = max(0, self._active_traces - 1)
        self._total_queries += 1

        if trace.error_domain:
            self._failed_queries += 1
        else:
            self._successful_queries += 1
            self._latencies.append(trace.total_elapsed_ms)
            self._assign_latency_bucket(trace.total_elapsed_ms)

            if trace.response_tier == ResponseTier.DOCTRINE_CACHE:
                self._cache_hits += 1
            elif trace.response_tier == ResponseTier.SEMANTIC_RETRIEVAL:
                self._cache_misses += 1
                self._semantic_retrievals += 1
            elif trace.response_tier == ResponseTier.DEEP_ANALYSIS:
                self._cache_misses += 1
                self._deep_analyses += 1

        for topic in trace.doctrine_topics_matched:
            self._doctrine_topic_counts[topic] += 1
        for cat in trace.issue_categories:
            self._issue_category_counts[cat] += 1

        if len(self._traces) >= MAX_TRACE_HISTORY:
            self._traces = self._traces[-(MAX_TRACE_HISTORY // 2):]
        self._traces.append(trace)

        self._write_audit_record(trace)

    def _assign_latency_bucket(self, latency_ms: float) -> None:
        """Assign a latency value to the appropriate bucket."""
        for bucket in self._latency_buckets:
            if bucket.lower_bound_ms <= latency_ms < bucket.upper_bound_ms:
                bucket.count += 1
                return
        if self._latency_buckets:
            self._latency_buckets[-1].count += 1

    def record_error(
        self,
        error_domain: ErrorDomain,
        error_type: str,
        error_message: str,
        query_id: Optional[str] = None,
        trace_id: Optional[str] = None,
        stack_trace: Optional[str] = None,
        recovery_action: Optional[str] = None,
    ) -> ErrorRecord:
        """Record an error occurrence."""
        record = ErrorRecord(
            error_id=str(uuid.uuid4()),
            timestamp_utc=datetime.now(timezone.utc).isoformat(),
            error_domain=error_domain,
            error_type=error_type,
            error_message=error_message,
            query_id=query_id,
            trace_id=trace_id,
            stack_trace=stack_trace,
            recovery_action=recovery_action,
        )
        self._error_domain_counts[error_domain.value] += 1
        self._last_error = record

        if len(self._errors) >= MAX_ERROR_HISTORY:
            self._errors = self._errors[-(MAX_ERROR_HISTORY // 2):]
        self._errors.append(record)

        logger.error(
            "Error recorded | domain={} type={} msg={}",
            error_domain.value, error_type, error_message[:200],
        )
        return record

    def get_snapshot(self) -> MetricsSnapshot:
        """Generate a point-in-time metrics snapshot."""
        uptime = time.time() - self._start_time
        avg_lat = statistics.mean(self._latencies) if self._latencies else 0.0
        p50 = self._percentile(50) if self._latencies else 0.0
        p95 = self._percentile(95) if self._latencies else 0.0
        p99 = self._percentile(99) if self._latencies else 0.0
        min_lat = min(self._latencies) if self._latencies else 0.0
        max_lat = max(self._latencies) if self._latencies else 0.0
        error_rate = (self._failed_queries / self._total_queries * 100.0) if self._total_queries > 0 else 0.0
        cache_total = self._cache_hits + self._cache_misses
        cache_hit_rate = (self._cache_hits / cache_total * 100.0) if cache_total > 0 else 0.0
        qpm = (self._total_queries / uptime * 60.0) if uptime > 0 else 0.0

        top_doctrines = sorted(
            [{"topic": k, "count": v} for k, v in self._doctrine_topic_counts.items()],
            key=lambda x: x["count"], reverse=True,
        )[:20]
        top_categories = sorted(
            [{"category": k, "count": v} for k, v in self._issue_category_counts.items()],
            key=lambda x: x["count"], reverse=True,
        )[:12]

        return MetricsSnapshot(
            snapshot_time_utc=datetime.now(timezone.utc).isoformat(),
            uptime_seconds=round(uptime, 1),
            total_queries=self._total_queries,
            successful_queries=self._successful_queries,
            failed_queries=self._failed_queries,
            error_rate=round(error_rate, 2),
            cache_hits=self._cache_hits,
            cache_misses=self._cache_misses,
            cache_hit_rate=round(cache_hit_rate, 2),
            semantic_retrievals=self._semantic_retrievals,
            deep_analyses=self._deep_analyses,
            avg_latency_ms=round(avg_lat, 2),
            p50_latency_ms=round(p50, 2),
            p95_latency_ms=round(p95, 2),
            p99_latency_ms=round(p99, 2),
            min_latency_ms=round(min_lat, 2),
            max_latency_ms=round(max_lat, 2),
            queries_per_minute=round(qpm, 2),
            latency_buckets=list(self._latency_buckets),
            error_counts_by_domain=dict(self._error_domain_counts),
            top_doctrine_topics=top_doctrines,
            top_issue_categories=top_categories,
            active_traces=self._active_traces,
        )

    def get_health_telemetry(self) -> HealthTelemetry:
        """Generate telemetry data for health check response."""
        snap = self.get_snapshot()
        status = "operational"
        if snap.error_rate > 50.0:
            status = "degraded"
        elif snap.error_rate > 80.0:
            status = "critical"
        return HealthTelemetry(
            status=status,
            total_queries_processed=snap.total_queries,
            error_rate_percent=snap.error_rate,
            avg_response_ms=snap.avg_latency_ms,
            cache_hit_rate_percent=snap.cache_hit_rate,
            uptime_seconds=snap.uptime_seconds,
            active_traces=snap.active_traces,
            last_error=self._last_error.error_message if self._last_error else None,
            last_error_time=self._last_error.timestamp_utc if self._last_error else None,
        )

    def save_snapshot(self) -> Path:
        """Save a metrics snapshot to disk."""
        snap = self.get_snapshot()
        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        path = METRICS_SNAPSHOT_DIR / f"metrics_{ts}.json"
        path.write_text(json.dumps(snap.model_dump(), indent=2, default=str), encoding="utf-8")
        logger.info("Metrics snapshot saved to {}", path)
        return path

    def _percentile(self, pct: float) -> float:
        """Calculate a percentile from latency data."""
        if not self._latencies:
            return 0.0
        sorted_lat = sorted(self._latencies)
        idx = int(len(sorted_lat) * pct / 100.0)
        idx = min(idx, len(sorted_lat) - 1)
        return sorted_lat[idx]

    def _write_audit_record(self, trace: QueryTrace) -> None:
        """Append a trace record to the JSONL audit log."""
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        audit_path = AUDIT_LOG_DIR / f"audit_{today}.jsonl"
        record = {
            "trace_id": trace.trace_id,
            "query_id": trace.query_id,
            "query_hash": trace.query_hash,
            "timestamp": trace.start_time_utc,
            "elapsed_ms": trace.total_elapsed_ms,
            "tier": trace.response_tier.value if trace.response_tier else "failed",
            "doctrines": trace.doctrine_topics_matched,
            "categories": trace.issue_categories,
            "confidence": trace.confidence_level,
            "error_domain": trace.error_domain.value if trace.error_domain else None,
            "determinism_hash": trace.determinism_hash,
        }
        with audit_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, default=str) + "\n")

    def get_recent_traces(self, limit: int = 50) -> list[QueryTrace]:
        """Return the most recent query traces."""
        return self._traces[-limit:]

    def get_recent_errors(self, limit: int = 50) -> list[ErrorRecord]:
        """Return the most recent error records."""
        return self._errors[-limit:]

    def reset(self) -> None:
        """Reset all metrics (for testing)."""
        self.__init__()  # type: ignore[misc]
        logger.warning("MetricsCollector reset — all metrics cleared")
