"""
LM16 Wind/Solar Lease Engine - Telemetry Module
=================================================
Full query tracing, latency tracking, error domain classification,
metrics collection, and performance monitoring for the Wind/Solar
Lease Intelligence Engine.

Engine: LM16 | Port: 8516
"""

from __future__ import annotations

import hashlib
import json
import statistics
import threading
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Optional
from uuid import uuid4

from loguru import logger
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
ENGINE_ID: str = "LM16"
ENGINE_NAME: str = "Wind/Solar Lease Intelligence Engine"
ENGINE_VERSION: str = "1.0.0"
ENGINE_PORT: int = 8516

TELEMETRY_DIR: Path = Path(__file__).parent / "telemetry_data"
AUDIT_LOG_PATH: Path = TELEMETRY_DIR / "audit_trail.jsonl"
METRICS_SNAPSHOT_PATH: Path = TELEMETRY_DIR / "metrics_snapshot.json"
DRIFT_LOG_PATH: Path = TELEMETRY_DIR / "drift_observations.jsonl"

MAX_LATENCY_SAMPLES: int = 10000
MAX_ERROR_LOG_ENTRIES: int = 5000


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------
class ErrorDomain(str, Enum):
    """Classification of error domains for telemetry tracking."""
    DOCTRINE_CACHE = "doctrine_cache"
    SEMANTIC_SEARCH = "semantic_search"
    VECTOR_RETRIEVAL = "vector_retrieval"
    AUTHORITY_RESOLUTION = "authority_resolution"
    CONFIDENCE_SCORING = "confidence_scoring"
    INPUT_VALIDATION = "input_validation"
    DEEP_ANALYSIS = "deep_analysis"
    NORMALIZATION = "normalization"
    SERIALIZATION = "serialization"
    NETWORK = "network"
    UNKNOWN = "unknown"


class QueryTier(str, Enum):
    """Which response tier handled the query."""
    DOCTRINE_CACHE = "doctrine_cache"
    SEMANTIC_RETRIEVAL = "semantic_retrieval"
    DEEP_ANALYSIS = "deep_analysis"


class ResponseMode(str, Enum):
    """Response mode used for the query."""
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"


# ---------------------------------------------------------------------------
# Pydantic Models
# ---------------------------------------------------------------------------
class QueryTrace(BaseModel):
    """Complete trace of a single query through the engine."""
    trace_id: str = Field(default_factory=lambda: uuid4().hex[:16])
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    engine_id: str = ENGINE_ID
    engine_version: str = ENGINE_VERSION
    query_text: str = ""
    query_hash: str = ""
    response_mode: str = "FAST"
    tier_used: str = "doctrine_cache"
    doctrine_topics_matched: list[str] = Field(default_factory=list)
    confidence_level: str = ""
    confidence_score: float = 0.0
    latency_ms: float = 0.0
    cache_hit: bool = False
    error_domain: Optional[str] = None
    error_message: Optional[str] = None
    determinism_hash: str = ""
    zone: str = "NEGOTIATION"
    authority_count: int = 0
    fragility_score: float = 0.0
    token_estimate: int = 0

    def compute_query_hash(self) -> str:
        """Compute SHA-256 hash of the query text for deduplication."""
        self.query_hash = hashlib.sha256(self.query_text.encode()).hexdigest()[:16]
        return self.query_hash


class LatencyBucket(BaseModel):
    """Latency statistics for a specific operation type."""
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

    def record(self, latency_ms: float) -> None:
        """Record a new latency measurement."""
        self.count += 1
        self.total_ms += latency_ms
        if latency_ms < self.min_ms:
            self.min_ms = latency_ms
        if latency_ms > self.max_ms:
            self.max_ms = latency_ms
        self.samples.append(latency_ms)
        if len(self.samples) > MAX_LATENCY_SAMPLES:
            self.samples = self.samples[-MAX_LATENCY_SAMPLES:]
        self._recompute_percentiles()

    def _recompute_percentiles(self) -> None:
        """Recompute percentile statistics from samples."""
        if not self.samples:
            return
        sorted_samples = sorted(self.samples)
        n = len(sorted_samples)
        self.avg_ms = self.total_ms / self.count if self.count > 0 else 0.0
        self.p50_ms = sorted_samples[int(n * 0.50)]
        self.p95_ms = sorted_samples[min(int(n * 0.95), n - 1)]
        self.p99_ms = sorted_samples[min(int(n * 0.99), n - 1)]


class MetricsSnapshot(BaseModel):
    """Point-in-time snapshot of engine metrics."""
    engine_id: str = ENGINE_ID
    engine_version: str = ENGINE_VERSION
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    uptime_seconds: float = 0.0
    total_queries: int = 0
    successful_queries: int = 0
    failed_queries: int = 0
    error_rate: float = 0.0
    cache_hit_rate: float = 0.0
    queries_per_minute: float = 0.0
    avg_latency_ms: float = 0.0
    p95_latency_ms: float = 0.0
    p99_latency_ms: float = 0.0
    tier_distribution: dict[str, int] = Field(default_factory=dict)
    mode_distribution: dict[str, int] = Field(default_factory=dict)
    error_domain_counts: dict[str, int] = Field(default_factory=dict)
    doctrine_hit_counts: dict[str, int] = Field(default_factory=dict)
    zone_distribution: dict[str, int] = Field(default_factory=dict)
    confidence_distribution: dict[str, int] = Field(default_factory=dict)


class DriftObservation(BaseModel):
    """Record of detected doctrine drift."""
    observation_id: str = Field(default_factory=lambda: uuid4().hex[:12])
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    doctrine_topic: str = ""
    drift_type: str = ""
    description: str = ""
    severity: str = "LOW"
    previous_confidence: float = 0.0
    current_confidence: float = 0.0
    delta: float = 0.0
    recommended_action: str = ""


class HealthReport(BaseModel):
    """Engine health report for monitoring."""
    engine_id: str = ENGINE_ID
    engine_name: str = ENGINE_NAME
    engine_version: str = ENGINE_VERSION
    port: int = ENGINE_PORT
    status: str = "healthy"
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    uptime_seconds: float = 0.0
    total_queries: int = 0
    error_rate: float = 0.0
    cache_hit_rate: float = 0.0
    avg_latency_ms: float = 0.0
    doctrine_count: int = 0
    active_zones: list[str] = Field(default_factory=list)
    last_query_time: Optional[str] = None
    memory_usage_mb: float = 0.0
    warnings: list[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Telemetry Collector
# ---------------------------------------------------------------------------
class TelemetryCollector:
    """
    Central telemetry collection and reporting system for LM16.
    Thread-safe with lock-protected mutation of all counters and logs.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._start_time: float = time.time()
        self._total_queries: int = 0
        self._successful_queries: int = 0
        self._failed_queries: int = 0
        self._cache_hits: int = 0
        self._cache_misses: int = 0

        self._tier_counts: dict[str, int] = defaultdict(int)
        self._mode_counts: dict[str, int] = defaultdict(int)
        self._error_domain_counts: dict[str, int] = defaultdict(int)
        self._doctrine_hit_counts: dict[str, int] = defaultdict(int)
        self._zone_counts: dict[str, int] = defaultdict(int)
        self._confidence_counts: dict[str, int] = defaultdict(int)

        self._latency_buckets: dict[str, LatencyBucket] = {
            "total": LatencyBucket(operation="total"),
            "doctrine_cache": LatencyBucket(operation="doctrine_cache"),
            "semantic_retrieval": LatencyBucket(operation="semantic_retrieval"),
            "deep_analysis": LatencyBucket(operation="deep_analysis"),
            "normalization": LatencyBucket(operation="normalization"),
            "authority_resolution": LatencyBucket(operation="authority_resolution"),
        }

        self._recent_traces: list[QueryTrace] = []
        self._max_recent_traces: int = 500
        self._error_log: list[dict[str, Any]] = []
        self._drift_observations: list[DriftObservation] = []

        TELEMETRY_DIR.mkdir(parents=True, exist_ok=True)
        logger.info(
            "TelemetryCollector initialized for {engine} v{version}",
            engine=ENGINE_ID,
            version=ENGINE_VERSION,
        )

    @property
    def uptime_seconds(self) -> float:
        """Current engine uptime in seconds."""
        return time.time() - self._start_time

    def record_query(self, trace: QueryTrace) -> None:
        """Record a completed query trace with all metrics."""
        with self._lock:
            self._total_queries += 1
            if trace.error_domain:
                self._failed_queries += 1
                self._error_domain_counts[trace.error_domain] += 1
                self._error_log.append({
                    "trace_id": trace.trace_id,
                    "timestamp": trace.timestamp,
                    "error_domain": trace.error_domain,
                    "error_message": trace.error_message or "",
                    "query_hash": trace.query_hash,
                })
                if len(self._error_log) > MAX_ERROR_LOG_ENTRIES:
                    self._error_log = self._error_log[-MAX_ERROR_LOG_ENTRIES:]
            else:
                self._successful_queries += 1

            if trace.cache_hit:
                self._cache_hits += 1
            else:
                self._cache_misses += 1

            self._tier_counts[trace.tier_used] += 1
            self._mode_counts[trace.response_mode] += 1
            self._zone_counts[trace.zone] += 1
            if trace.confidence_level:
                self._confidence_counts[trace.confidence_level] += 1

            for topic in trace.doctrine_topics_matched:
                self._doctrine_hit_counts[topic] += 1

            if trace.latency_ms > 0:
                self._latency_buckets["total"].record(trace.latency_ms)
                tier_key = trace.tier_used
                if tier_key in self._latency_buckets:
                    self._latency_buckets[tier_key].record(trace.latency_ms)

            self._recent_traces.append(trace)
            if len(self._recent_traces) > self._max_recent_traces:
                self._recent_traces = self._recent_traces[-self._max_recent_traces:]

        self._append_audit_log(trace)

    def record_latency(self, operation: str, latency_ms: float) -> None:
        """Record a latency measurement for a specific operation."""
        with self._lock:
            if operation not in self._latency_buckets:
                self._latency_buckets[operation] = LatencyBucket(operation=operation)
            self._latency_buckets[operation].record(latency_ms)

    def record_drift(self, observation: DriftObservation) -> None:
        """Record a doctrine drift observation."""
        with self._lock:
            self._drift_observations.append(observation)
        self._append_drift_log(observation)
        logger.warning(
            "Doctrine drift detected: {topic} - {drift_type} (severity={severity})",
            topic=observation.doctrine_topic,
            drift_type=observation.drift_type,
            severity=observation.severity,
        )

    def get_metrics_snapshot(self) -> MetricsSnapshot:
        """Generate a point-in-time metrics snapshot."""
        with self._lock:
            uptime = self.uptime_seconds
            total = self._total_queries
            error_rate = (
                self._failed_queries / total if total > 0 else 0.0
            )
            cache_total = self._cache_hits + self._cache_misses
            cache_hit_rate = (
                self._cache_hits / cache_total if cache_total > 0 else 0.0
            )
            qpm = total / (uptime / 60.0) if uptime > 60 else 0.0

            total_bucket = self._latency_buckets.get("total", LatencyBucket(operation="total"))

            return MetricsSnapshot(
                uptime_seconds=round(uptime, 2),
                total_queries=total,
                successful_queries=self._successful_queries,
                failed_queries=self._failed_queries,
                error_rate=round(error_rate, 4),
                cache_hit_rate=round(cache_hit_rate, 4),
                queries_per_minute=round(qpm, 2),
                avg_latency_ms=round(total_bucket.avg_ms, 2),
                p95_latency_ms=round(total_bucket.p95_ms, 2),
                p99_latency_ms=round(total_bucket.p99_ms, 2),
                tier_distribution=dict(self._tier_counts),
                mode_distribution=dict(self._mode_counts),
                error_domain_counts=dict(self._error_domain_counts),
                doctrine_hit_counts=dict(self._doctrine_hit_counts),
                zone_distribution=dict(self._zone_counts),
                confidence_distribution=dict(self._confidence_counts),
            )

    def get_health_report(self, doctrine_count: int = 0) -> HealthReport:
        """Generate an engine health report."""
        metrics = self.get_metrics_snapshot()
        warnings: list[str] = []

        if metrics.error_rate > 0.10:
            warnings.append(f"High error rate: {metrics.error_rate:.1%}")
        if metrics.avg_latency_ms > 5000:
            warnings.append(f"High avg latency: {metrics.avg_latency_ms:.0f}ms")
        if metrics.cache_hit_rate < 0.20 and metrics.total_queries > 50:
            warnings.append(f"Low cache hit rate: {metrics.cache_hit_rate:.1%}")

        status = "healthy"
        if len(warnings) >= 2:
            status = "degraded"
        if metrics.error_rate > 0.50:
            status = "unhealthy"

        import psutil
        process = psutil.Process()
        memory_mb = process.memory_info().rss / (1024 * 1024)

        return HealthReport(
            status=status,
            uptime_seconds=metrics.uptime_seconds,
            total_queries=metrics.total_queries,
            error_rate=metrics.error_rate,
            cache_hit_rate=metrics.cache_hit_rate,
            avg_latency_ms=metrics.avg_latency_ms,
            doctrine_count=doctrine_count,
            active_zones=list(metrics.zone_distribution.keys()),
            last_query_time=(
                self._recent_traces[-1].timestamp if self._recent_traces else None
            ),
            memory_usage_mb=round(memory_mb, 2),
            warnings=warnings,
        )

    def get_recent_traces(self, limit: int = 50) -> list[QueryTrace]:
        """Return the most recent query traces."""
        with self._lock:
            return list(self._recent_traces[-limit:])

    def get_error_log(self, limit: int = 100) -> list[dict[str, Any]]:
        """Return recent error log entries."""
        with self._lock:
            return list(self._error_log[-limit:])

    def get_drift_observations(self, limit: int = 50) -> list[DriftObservation]:
        """Return recent drift observations."""
        with self._lock:
            return list(self._drift_observations[-limit:])

    def get_doctrine_coverage(self, all_topics: list[str]) -> dict[str, Any]:
        """Compute doctrine coverage statistics."""
        with self._lock:
            triggered = set(self._doctrine_hit_counts.keys())
            all_set = set(all_topics)
            missed = all_set - triggered
            coverage = len(triggered) / len(all_set) if all_set else 0.0

            return {
                "total_doctrines": len(all_set),
                "triggered_doctrines": len(triggered),
                "missed_doctrines": len(missed),
                "coverage_ratio": round(coverage, 4),
                "triggered_list": sorted(triggered),
                "missed_list": sorted(missed),
                "hit_counts": dict(self._doctrine_hit_counts),
            }

    def export_metrics(self) -> None:
        """Export current metrics snapshot to disk."""
        snapshot = self.get_metrics_snapshot()
        METRICS_SNAPSHOT_PATH.write_text(
            snapshot.model_dump_json(indent=2), encoding="utf-8"
        )
        logger.debug("Metrics snapshot exported to {path}", path=METRICS_SNAPSHOT_PATH)

    def _append_audit_log(self, trace: QueryTrace) -> None:
        """Append a query trace to the JSONL audit log."""
        try:
            with AUDIT_LOG_PATH.open("a", encoding="utf-8") as f:
                f.write(trace.model_dump_json() + "\n")
        except Exception as exc:
            logger.error("Failed to write audit log: {err}", err=str(exc))

    def _append_drift_log(self, observation: DriftObservation) -> None:
        """Append a drift observation to the JSONL drift log."""
        try:
            with DRIFT_LOG_PATH.open("a", encoding="utf-8") as f:
                f.write(observation.model_dump_json() + "\n")
        except Exception as exc:
            logger.error("Failed to write drift log: {err}", err=str(exc))


# ---------------------------------------------------------------------------
# Timer Context Manager
# ---------------------------------------------------------------------------
class LatencyTimer:
    """Context manager for timing operations and recording to telemetry."""

    def __init__(self, collector: TelemetryCollector, operation: str) -> None:
        self.collector = collector
        self.operation = operation
        self._start: float = 0.0
        self.elapsed_ms: float = 0.0

    def __enter__(self) -> "LatencyTimer":
        self._start = time.perf_counter()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.elapsed_ms = (time.perf_counter() - self._start) * 1000
        self.collector.record_latency(self.operation, self.elapsed_ms)


# ---------------------------------------------------------------------------
# Module-level singleton
# ---------------------------------------------------------------------------
_collector: Optional[TelemetryCollector] = None
_collector_lock = threading.Lock()


def get_collector() -> TelemetryCollector:
    """Get or create the module-level telemetry collector singleton."""
    global _collector
    if _collector is None:
        with _collector_lock:
            if _collector is None:
                _collector = TelemetryCollector()
    return _collector


def reset_collector() -> TelemetryCollector:
    """Reset the telemetry collector (for testing)."""
    global _collector
    with _collector_lock:
        _collector = TelemetryCollector()
    return _collector
