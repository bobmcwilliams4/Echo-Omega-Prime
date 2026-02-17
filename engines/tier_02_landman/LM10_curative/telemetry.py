"""
LM10 Curative Engine — Telemetry Module
========================================
Full query tracing, latency tracking, error domain classification,
metrics collection, and audit trail for the Curative title engine.

Engine: LM10 | Port: 8510 | Domain: title_curative
"""

from __future__ import annotations

import hashlib
import json
import statistics
import threading
import time
import uuid
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Optional

from loguru import logger
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
ENGINE_ID = "LM10"
ENGINE_NAME = "Curative"
ENGINE_VERSION = "1.0.0"
ENGINE_PORT = 8510
TELEMETRY_DIR = Path(__file__).parent / "telemetry_data"
AUDIT_TRAIL_PATH = TELEMETRY_DIR / "audit_trail.jsonl"
METRICS_SNAPSHOT_PATH = TELEMETRY_DIR / "metrics_snapshot.json"
MAX_LATENCY_SAMPLES = 10_000
MAX_ERROR_LOG_SIZE = 5_000
MAX_AUDIT_ENTRIES = 100_000


class ErrorDomain(str, Enum):
    """Classification of error domains for curative operations."""
    DOCTRINE_LOOKUP = "doctrine_lookup"
    VECTOR_SEARCH = "vector_search"
    SEMANTIC_NORMALIZATION = "semantic_normalization"
    DEEP_ANALYSIS = "deep_analysis"
    AUTHORITY_RESOLUTION = "authority_resolution"
    HEIRSHIP_ANALYSIS = "heirship_analysis"
    PROBATE_EVALUATION = "probate_evaluation"
    CORRECTION_INSTRUMENT = "correction_instrument"
    QUIET_TITLE = "quiet_title"
    TAX_SALE = "tax_sale"
    ADVERSE_POSSESSION = "adverse_possession"
    LIEN_RELEASE = "lien_release"
    ENTITY_AUTHORITY = "entity_authority"
    NAME_VARIATION = "name_variation"
    SERIALIZATION = "serialization"
    CONFIGURATION = "configuration"
    NETWORK = "network"
    UNKNOWN = "unknown"


class QueryPhase(str, Enum):
    """Phases of query processing."""
    RECEIVED = "received"
    NORMALIZED = "normalized"
    DOCTRINE_CACHE = "doctrine_cache"
    VECTOR_SEARCH = "vector_search"
    DEEP_ANALYSIS = "deep_analysis"
    AUTHORITY_HARDENING = "authority_hardening"
    CONFIDENCE_SCORING = "confidence_scoring"
    RESPONSE_ASSEMBLY = "response_assembly"
    COMPLETED = "completed"
    FAILED = "failed"


# ---------------------------------------------------------------------------
# Pydantic Models
# ---------------------------------------------------------------------------
class TraceSpan(BaseModel):
    """A single span within a query trace."""
    span_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:12])
    phase: QueryPhase
    start_time: float
    end_time: float = 0.0
    duration_ms: float = 0.0
    metadata: dict[str, Any] = Field(default_factory=dict)
    error: Optional[str] = None

    def close(self, error: Optional[str] = None) -> None:
        """Close the span and compute duration."""
        self.end_time = time.time()
        self.duration_ms = (self.end_time - self.start_time) * 1000.0
        if error:
            self.error = error


class QueryTrace(BaseModel):
    """Full trace of a single query through the engine."""
    trace_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:16])
    query_hash: str = ""
    query_text: str = ""
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    total_duration_ms: float = 0.0
    spans: list[TraceSpan] = Field(default_factory=list)
    response_mode: str = "FAST"
    issue_category: str = ""
    doctrine_hits: int = 0
    vector_hits: int = 0
    confidence_tier: str = ""
    determinism_hash: str = ""
    success: bool = True
    error_domain: Optional[str] = None
    error_message: Optional[str] = None

    def add_span(self, phase: QueryPhase, metadata: Optional[dict[str, Any]] = None) -> TraceSpan:
        """Create and add a new span."""
        span = TraceSpan(
            phase=phase,
            start_time=time.time(),
            metadata=metadata or {},
        )
        self.spans.append(span)
        return span

    def finalize(self) -> None:
        """Compute total duration and hash."""
        if self.spans:
            first_start = min(s.start_time for s in self.spans)
            last_end = max(s.end_time for s in self.spans if s.end_time > 0)
            self.total_duration_ms = (last_end - first_start) * 1000.0 if last_end > first_start else 0.0
        content = f"{self.query_text}|{self.timestamp}|{self.total_duration_ms}"
        self.determinism_hash = hashlib.sha256(content.encode()).hexdigest()


class ErrorRecord(BaseModel):
    """Structured error record for telemetry."""
    error_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:12])
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    domain: ErrorDomain = ErrorDomain.UNKNOWN
    message: str = ""
    stack_trace: str = ""
    query_hash: str = ""
    trace_id: str = ""
    resolved: bool = False
    resolution: str = ""


class LatencyBucket(BaseModel):
    """Latency statistics for a specific operation."""
    operation: str
    count: int = 0
    total_ms: float = 0.0
    min_ms: float = float("inf")
    max_ms: float = 0.0
    avg_ms: float = 0.0
    p50_ms: float = 0.0
    p95_ms: float = 0.0
    p99_ms: float = 0.0
    samples: list[float] = Field(default_factory=list)

    def record(self, duration_ms: float) -> None:
        """Record a latency sample."""
        self.count += 1
        self.total_ms += duration_ms
        if duration_ms < self.min_ms:
            self.min_ms = duration_ms
        if duration_ms > self.max_ms:
            self.max_ms = duration_ms
        self.samples.append(duration_ms)
        if len(self.samples) > MAX_LATENCY_SAMPLES:
            self.samples = self.samples[-MAX_LATENCY_SAMPLES:]
        self._recalculate()

    def _recalculate(self) -> None:
        """Recalculate percentile statistics."""
        if not self.samples:
            return
        self.avg_ms = self.total_ms / self.count
        sorted_samples = sorted(self.samples)
        n = len(sorted_samples)
        self.p50_ms = sorted_samples[int(n * 0.50)]
        self.p95_ms = sorted_samples[int(n * 0.95)] if n >= 20 else sorted_samples[-1]
        self.p99_ms = sorted_samples[int(n * 0.99)] if n >= 100 else sorted_samples[-1]


class MetricsSnapshot(BaseModel):
    """Point-in-time metrics snapshot."""
    engine_id: str = ENGINE_ID
    engine_name: str = ENGINE_NAME
    engine_version: str = ENGINE_VERSION
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    uptime_seconds: float = 0.0
    total_queries: int = 0
    successful_queries: int = 0
    failed_queries: int = 0
    error_rate: float = 0.0
    queries_per_minute: float = 0.0
    doctrine_cache_hits: int = 0
    doctrine_cache_misses: int = 0
    cache_hit_rate: float = 0.0
    vector_search_count: int = 0
    deep_analysis_count: int = 0
    latency_buckets: dict[str, Any] = Field(default_factory=dict)
    error_counts_by_domain: dict[str, int] = Field(default_factory=dict)
    queries_by_category: dict[str, int] = Field(default_factory=dict)
    queries_by_mode: dict[str, int] = Field(default_factory=dict)
    confidence_distribution: dict[str, int] = Field(default_factory=dict)
    active_traces: int = 0


class AuditEntry(BaseModel):
    """Audit trail entry for compliance and forensic review."""
    entry_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:16])
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    event_type: str = ""
    trace_id: str = ""
    query_hash: str = ""
    query_summary: str = ""
    response_mode: str = ""
    issue_category: str = ""
    confidence_tier: str = ""
    doctrine_topics_triggered: list[str] = Field(default_factory=list)
    authority_sources_cited: list[str] = Field(default_factory=list)
    duration_ms: float = 0.0
    determinism_hash: str = ""
    client_ip: str = ""
    user_agent: str = ""


# ---------------------------------------------------------------------------
# Telemetry Collector
# ---------------------------------------------------------------------------
class TelemetryCollector:
    """
    Central telemetry collector for the LM10 Curative Engine.

    Manages query traces, latency buckets, error records, metrics snapshots,
    and the append-only audit trail.
    """

    def __init__(self, telemetry_dir: Optional[Path] = None) -> None:
        self._start_time = time.time()
        self._lock = threading.Lock()
        self._telemetry_dir = telemetry_dir or TELEMETRY_DIR
        self._telemetry_dir.mkdir(parents=True, exist_ok=True)
        self._audit_path = self._telemetry_dir / "audit_trail.jsonl"
        self._metrics_path = self._telemetry_dir / "metrics_snapshot.json"

        # Counters
        self._total_queries = 0
        self._successful_queries = 0
        self._failed_queries = 0
        self._doctrine_cache_hits = 0
        self._doctrine_cache_misses = 0
        self._vector_search_count = 0
        self._deep_analysis_count = 0

        # Breakdown counters
        self._queries_by_category: dict[str, int] = defaultdict(int)
        self._queries_by_mode: dict[str, int] = defaultdict(int)
        self._confidence_distribution: dict[str, int] = defaultdict(int)
        self._error_counts_by_domain: dict[str, int] = defaultdict(int)

        # Latency tracking
        self._latency_buckets: dict[str, LatencyBucket] = {}

        # Active traces
        self._active_traces: dict[str, QueryTrace] = {}

        # Recent completed traces (ring buffer)
        self._completed_traces: deque[QueryTrace] = deque(maxlen=1000)

        # Error log
        self._errors: deque[ErrorRecord] = deque(maxlen=MAX_ERROR_LOG_SIZE)

        # Query timestamps for rate calculation
        self._query_timestamps: deque[float] = deque(maxlen=10_000)

        # Audit entry count
        self._audit_entry_count = 0

        logger.info(
            "TelemetryCollector initialized | engine={} | dir={}",
            ENGINE_ID,
            self._telemetry_dir,
        )

    # --- Trace lifecycle ---

    def start_trace(
        self,
        query_text: str,
        response_mode: str = "FAST",
        issue_category: str = "",
    ) -> QueryTrace:
        """Begin a new query trace."""
        query_hash = hashlib.sha256(query_text.encode()).hexdigest()[:16]
        trace = QueryTrace(
            query_hash=query_hash,
            query_text=query_text[:500],
            response_mode=response_mode,
            issue_category=issue_category,
        )
        with self._lock:
            self._active_traces[trace.trace_id] = trace
            self._total_queries += 1
            self._query_timestamps.append(time.time())
            self._queries_by_mode[response_mode] = self._queries_by_mode.get(response_mode, 0) + 1
            if issue_category:
                self._queries_by_category[issue_category] = self._queries_by_category.get(issue_category, 0) + 1
        logger.debug("Trace started | trace_id={} | hash={}", trace.trace_id, query_hash)
        return trace

    def complete_trace(
        self,
        trace: QueryTrace,
        confidence_tier: str = "",
        doctrine_hits: int = 0,
        vector_hits: int = 0,
    ) -> None:
        """Complete a trace successfully."""
        trace.success = True
        trace.confidence_tier = confidence_tier
        trace.doctrine_hits = doctrine_hits
        trace.vector_hits = vector_hits
        trace.finalize()

        with self._lock:
            self._successful_queries += 1
            self._doctrine_cache_hits += doctrine_hits
            if vector_hits > 0:
                self._vector_search_count += 1
            if confidence_tier:
                self._confidence_distribution[confidence_tier] = (
                    self._confidence_distribution.get(confidence_tier, 0) + 1
                )
            self._active_traces.pop(trace.trace_id, None)
            self._completed_traces.append(trace)

        self._record_latency("total_query", trace.total_duration_ms)
        for span in trace.spans:
            if span.duration_ms > 0:
                self._record_latency(span.phase.value, span.duration_ms)

        self._write_audit_entry(trace)
        logger.debug(
            "Trace completed | trace_id={} | duration_ms={:.1f} | tier={}",
            trace.trace_id,
            trace.total_duration_ms,
            confidence_tier,
        )

    def fail_trace(
        self,
        trace: QueryTrace,
        error_domain: ErrorDomain,
        error_message: str,
        stack_trace: str = "",
    ) -> None:
        """Mark a trace as failed."""
        trace.success = False
        trace.error_domain = error_domain.value
        trace.error_message = error_message
        trace.finalize()

        error_record = ErrorRecord(
            domain=error_domain,
            message=error_message,
            stack_trace=stack_trace,
            query_hash=trace.query_hash,
            trace_id=trace.trace_id,
        )

        with self._lock:
            self._failed_queries += 1
            self._error_counts_by_domain[error_domain.value] = (
                self._error_counts_by_domain.get(error_domain.value, 0) + 1
            )
            self._errors.append(error_record)
            self._active_traces.pop(trace.trace_id, None)
            self._completed_traces.append(trace)

        self._record_latency("failed_query", trace.total_duration_ms)
        self._write_audit_entry(trace)
        logger.warning(
            "Trace failed | trace_id={} | domain={} | error={}",
            trace.trace_id,
            error_domain.value,
            error_message[:200],
        )

    # --- Metrics ---

    def record_doctrine_miss(self) -> None:
        """Record a doctrine cache miss."""
        with self._lock:
            self._doctrine_cache_misses += 1

    def record_deep_analysis(self) -> None:
        """Record a deep analysis invocation."""
        with self._lock:
            self._deep_analysis_count += 1

    def _record_latency(self, operation: str, duration_ms: float) -> None:
        """Record a latency sample for an operation."""
        with self._lock:
            if operation not in self._latency_buckets:
                self._latency_buckets[operation] = LatencyBucket(operation=operation)
            self._latency_buckets[operation].record(duration_ms)

    def get_metrics_snapshot(self) -> MetricsSnapshot:
        """Generate a point-in-time metrics snapshot."""
        with self._lock:
            uptime = time.time() - self._start_time
            total = self._total_queries
            error_rate = self._failed_queries / total if total > 0 else 0.0

            now = time.time()
            recent_queries = sum(1 for t in self._query_timestamps if now - t < 60.0)

            cache_total = self._doctrine_cache_hits + self._doctrine_cache_misses
            cache_hit_rate = self._doctrine_cache_hits / cache_total if cache_total > 0 else 0.0

            latency_data = {}
            for key, bucket in self._latency_buckets.items():
                latency_data[key] = {
                    "count": bucket.count,
                    "avg_ms": round(bucket.avg_ms, 2),
                    "p50_ms": round(bucket.p50_ms, 2),
                    "p95_ms": round(bucket.p95_ms, 2),
                    "p99_ms": round(bucket.p99_ms, 2),
                    "min_ms": round(bucket.min_ms, 2) if bucket.min_ms != float("inf") else 0.0,
                    "max_ms": round(bucket.max_ms, 2),
                }

            return MetricsSnapshot(
                uptime_seconds=round(uptime, 1),
                total_queries=total,
                successful_queries=self._successful_queries,
                failed_queries=self._failed_queries,
                error_rate=round(error_rate, 4),
                queries_per_minute=round(recent_queries, 1),
                doctrine_cache_hits=self._doctrine_cache_hits,
                doctrine_cache_misses=self._doctrine_cache_misses,
                cache_hit_rate=round(cache_hit_rate, 4),
                vector_search_count=self._vector_search_count,
                deep_analysis_count=self._deep_analysis_count,
                latency_buckets=latency_data,
                error_counts_by_domain=dict(self._error_counts_by_domain),
                queries_by_category=dict(self._queries_by_category),
                queries_by_mode=dict(self._queries_by_mode),
                confidence_distribution=dict(self._confidence_distribution),
                active_traces=len(self._active_traces),
            )

    def save_metrics_snapshot(self) -> Path:
        """Save current metrics to disk."""
        snapshot = self.get_metrics_snapshot()
        self._metrics_path.write_text(snapshot.model_dump_json(indent=2), encoding="utf-8")
        logger.debug("Metrics snapshot saved to {}", self._metrics_path)
        return self._metrics_path

    # --- Audit trail ---

    def _write_audit_entry(self, trace: QueryTrace) -> None:
        """Append an audit entry to the JSONL audit trail."""
        entry = AuditEntry(
            event_type="query_complete" if trace.success else "query_failed",
            trace_id=trace.trace_id,
            query_hash=trace.query_hash,
            query_summary=trace.query_text[:120],
            response_mode=trace.response_mode,
            issue_category=trace.issue_category,
            confidence_tier=trace.confidence_tier,
            doctrine_topics_triggered=[
                s.metadata.get("topic", "")
                for s in trace.spans
                if s.metadata.get("topic")
            ],
            duration_ms=round(trace.total_duration_ms, 2),
            determinism_hash=trace.determinism_hash,
        )
        try:
            with self._audit_path.open("a", encoding="utf-8") as f:
                f.write(entry.model_dump_json() + "\n")
            with self._lock:
                self._audit_entry_count += 1
        except Exception as exc:
            logger.error("Failed to write audit entry: {}", exc)

    def get_recent_audit_entries(self, count: int = 50) -> list[dict[str, Any]]:
        """Read the most recent audit entries."""
        entries: list[dict[str, Any]] = []
        if not self._audit_path.exists():
            return entries
        try:
            lines = self._audit_path.read_text(encoding="utf-8").strip().split("\n")
            for line in lines[-count:]:
                if line.strip():
                    entries.append(json.loads(line))
        except Exception as exc:
            logger.error("Failed to read audit trail: {}", exc)
        return entries

    # --- Error reporting ---

    def get_recent_errors(self, count: int = 20) -> list[dict[str, Any]]:
        """Get recent error records."""
        with self._lock:
            recent = list(self._errors)[-count:]
        return [e.model_dump() for e in recent]

    def get_error_summary(self) -> dict[str, Any]:
        """Get error summary by domain."""
        with self._lock:
            return {
                "total_errors": self._failed_queries,
                "by_domain": dict(self._error_counts_by_domain),
                "recent_count": len(self._errors),
            }

    # --- Health ---

    def get_health(self) -> dict[str, Any]:
        """Get telemetry subsystem health."""
        snapshot = self.get_metrics_snapshot()
        healthy = snapshot.error_rate < 0.15
        return {
            "status": "healthy" if healthy else "degraded",
            "engine_id": ENGINE_ID,
            "engine_name": ENGINE_NAME,
            "version": ENGINE_VERSION,
            "uptime_seconds": snapshot.uptime_seconds,
            "total_queries": snapshot.total_queries,
            "error_rate": snapshot.error_rate,
            "cache_hit_rate": snapshot.cache_hit_rate,
            "queries_per_minute": snapshot.queries_per_minute,
            "active_traces": snapshot.active_traces,
            "audit_entries_written": self._audit_entry_count,
        }

    # --- Cleanup ---

    def rotate_audit_trail(self, max_entries: int = MAX_AUDIT_ENTRIES) -> int:
        """Rotate audit trail if it exceeds max entries."""
        if not self._audit_path.exists():
            return 0
        try:
            lines = self._audit_path.read_text(encoding="utf-8").strip().split("\n")
            if len(lines) <= max_entries:
                return 0
            keep = lines[-max_entries:]
            archive_path = self._telemetry_dir / f"audit_trail_archive_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.jsonl"
            archive_path.write_text("\n".join(lines[:-max_entries]) + "\n", encoding="utf-8")
            self._audit_path.write_text("\n".join(keep) + "\n", encoding="utf-8")
            rotated = len(lines) - max_entries
            logger.info("Rotated {} audit entries to {}", rotated, archive_path)
            return rotated
        except Exception as exc:
            logger.error("Audit trail rotation failed: {}", exc)
            return 0


# ---------------------------------------------------------------------------
# Module-level singleton
# ---------------------------------------------------------------------------
_collector: Optional[TelemetryCollector] = None


def get_telemetry_collector(telemetry_dir: Optional[Path] = None) -> TelemetryCollector:
    """Get or create the singleton telemetry collector."""
    global _collector
    if _collector is None:
        _collector = TelemetryCollector(telemetry_dir=telemetry_dir)
    return _collector


def reset_telemetry_collector() -> None:
    """Reset the singleton (for testing)."""
    global _collector
    _collector = None
