"""
LM14 Easement Analyzer Engine - Telemetry Module
====================================================
Provides comprehensive metrics collection, latency tracking, cache hit
monitoring, error rate computation, query pattern analysis, and structured
audit logging for the LM14 Easement Analyzer engine.

Components:
    - TelemetryCollector: Core metrics aggregation engine
    - MetricsBucket: Time-windowed metric storage
    - AuditLogger: Append-only JSONL audit trail
    - LatencyTracker: Per-endpoint latency histograms
    - CacheMetrics: Doctrine cache hit/miss tracking
    - QueryPatternAnalyzer: Query frequency and pattern analysis
    - telemetry_health(): Health check for telemetry subsystem

Version: 1.0.0
Engine: LM14 Easement Analyzer
"""

from __future__ import annotations

import hashlib
import json
import os
import threading
import time
from collections import Counter, defaultdict, deque
from contextlib import contextmanager
from dataclasses import dataclass, field as dc_field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Deque, Dict, Generator, List, Optional, Set, Tuple

from loguru import logger


# ============================================================================
# CONFIGURATION
# ============================================================================

ENGINE_ID = "LM14"
ENGINE_NAME = "Easement Analyzer"
ENGINE_VERSION = "1.0.0"
METRICS_PREFIX = "lm14"
MAX_BUFFER_SIZE = 500
FLUSH_INTERVAL_SEC = 30
LATENCY_WINDOW_SIZE = 1000
PATTERN_WINDOW_SIZE = 500
AUDIT_LOG_DIR = Path(__file__).parent / "audit_logs"


# ============================================================================
# METRIC TYPE ENUM
# ============================================================================

class MetricType(str, Enum):
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    TIMER = "timer"


# ============================================================================
# METRICS BUCKET - TIME-WINDOWED STORAGE
# ============================================================================

@dataclass
class MetricsBucket:
    """Stores metric values within a time window."""

    name: str
    metric_type: MetricType
    values: Deque[Tuple[float, float]] = dc_field(default_factory=lambda: deque(maxlen=LATENCY_WINDOW_SIZE))
    total: float = 0.0
    count: int = 0
    min_val: float = float("inf")
    max_val: float = float("-inf")
    _lock: threading.Lock = dc_field(default_factory=threading.Lock, repr=False)

    def record(self, value: float) -> None:
        """Record a new metric value."""
        with self._lock:
            now = time.time()
            self.values.append((now, value))
            self.total += value
            self.count += 1
            if value < self.min_val:
                self.min_val = value
            if value > self.max_val:
                self.max_val = value

    def increment(self, amount: float = 1.0) -> None:
        """Increment a counter metric."""
        with self._lock:
            self.total += amount
            self.count += 1
            now = time.time()
            self.values.append((now, amount))

    @property
    def average(self) -> float:
        if self.count == 0:
            return 0.0
        return self.total / self.count

    def percentile(self, p: float) -> float:
        """Calculate the p-th percentile from recent values."""
        with self._lock:
            if not self.values:
                return 0.0
            sorted_vals = sorted(v for _, v in self.values)
            k = max(0, min(len(sorted_vals) - 1, int(len(sorted_vals) * p / 100.0)))
            return sorted_vals[k]

    def values_since(self, since_ts: float) -> List[Tuple[float, float]]:
        """Return values recorded since a given timestamp."""
        with self._lock:
            return [(ts, v) for ts, v in self.values if ts >= since_ts]

    def reset(self) -> None:
        """Reset all values."""
        with self._lock:
            self.values.clear()
            self.total = 0.0
            self.count = 0
            self.min_val = float("inf")
            self.max_val = float("-inf")

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "name": self.name,
            "type": self.metric_type.value,
            "count": self.count,
            "total": round(self.total, 4),
            "average": round(self.average, 4),
            "min": round(self.min_val, 4) if self.min_val != float("inf") else 0.0,
            "max": round(self.max_val, 4) if self.max_val != float("-inf") else 0.0,
            "p50": round(self.percentile(50), 4),
            "p90": round(self.percentile(90), 4),
            "p99": round(self.percentile(99), 4),
            "recent_values": len(self.values),
        }


# ============================================================================
# LATENCY TRACKER
# ============================================================================

class LatencyTracker:
    """Per-endpoint latency histogram tracking."""

    def __init__(self) -> None:
        self._endpoints: Dict[str, MetricsBucket] = {}
        self._lock = threading.Lock()

    def record(self, endpoint: str, latency_ms: float) -> None:
        """Record a latency observation for an endpoint."""
        with self._lock:
            if endpoint not in self._endpoints:
                self._endpoints[endpoint] = MetricsBucket(
                    name=f"{METRICS_PREFIX}.latency.{endpoint}",
                    metric_type=MetricType.HISTOGRAM,
                )
            self._endpoints[endpoint].record(latency_ms)

    @contextmanager
    def timer(self, endpoint: str) -> Generator[None, None, None]:
        """Context manager to automatically time an operation."""
        start = time.time()
        try:
            yield
        finally:
            elapsed_ms = (time.time() - start) * 1000
            self.record(endpoint, elapsed_ms)

    def get_stats(self, endpoint: str) -> Optional[Dict[str, Any]]:
        """Get latency stats for a specific endpoint."""
        with self._lock:
            bucket = self._endpoints.get(endpoint)
            if bucket:
                return bucket.to_dict()
            return None

    def get_all_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get latency stats for all endpoints."""
        with self._lock:
            return {ep: bucket.to_dict() for ep, bucket in self._endpoints.items()}

    def get_slow_endpoints(self, threshold_ms: float = 1000.0) -> List[Dict[str, Any]]:
        """Return endpoints with p90 latency above threshold."""
        slow: List[Dict[str, Any]] = []
        with self._lock:
            for ep, bucket in self._endpoints.items():
                p90 = bucket.percentile(90)
                if p90 > threshold_ms:
                    slow.append({
                        "endpoint": ep,
                        "p90_ms": round(p90, 2),
                        "p99_ms": round(bucket.percentile(99), 2),
                        "count": bucket.count,
                    })
        return sorted(slow, key=lambda x: x["p90_ms"], reverse=True)

    def reset(self) -> None:
        """Reset all latency data."""
        with self._lock:
            for bucket in self._endpoints.values():
                bucket.reset()

    def to_dict(self) -> Dict[str, Any]:
        return self.get_all_stats()


# ============================================================================
# CACHE METRICS
# ============================================================================

class CacheMetrics:
    """Track doctrine cache hit/miss rates."""

    def __init__(self) -> None:
        self._hits = MetricsBucket(
            name=f"{METRICS_PREFIX}.cache.hits",
            metric_type=MetricType.COUNTER,
        )
        self._misses = MetricsBucket(
            name=f"{METRICS_PREFIX}.cache.misses",
            metric_type=MetricType.COUNTER,
        )
        self._by_topic_hits: Dict[str, int] = Counter()
        self._by_topic_misses: Dict[str, int] = Counter()
        self._lock = threading.Lock()

    def record_hit(self, topic: str = "") -> None:
        """Record a cache hit."""
        self._hits.increment()
        if topic:
            with self._lock:
                self._by_topic_hits[topic] += 1

    def record_miss(self, topic: str = "") -> None:
        """Record a cache miss."""
        self._misses.increment()
        if topic:
            with self._lock:
                self._by_topic_misses[topic] += 1

    @property
    def hit_rate(self) -> float:
        total = self._hits.count + self._misses.count
        if total == 0:
            return 0.0
        return self._hits.count / total

    @property
    def miss_rate(self) -> float:
        return 1.0 - self.hit_rate

    def top_hits(self, n: int = 10) -> List[Tuple[str, int]]:
        """Return the N most frequently hit topics."""
        with self._lock:
            return Counter(self._by_topic_hits).most_common(n)

    def top_misses(self, n: int = 10) -> List[Tuple[str, int]]:
        """Return the N most frequently missed topics."""
        with self._lock:
            return Counter(self._by_topic_misses).most_common(n)

    def reset(self) -> None:
        """Reset all cache metrics."""
        self._hits.reset()
        self._misses.reset()
        with self._lock:
            self._by_topic_hits.clear()
            self._by_topic_misses.clear()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_hits": self._hits.count,
            "total_misses": self._misses.count,
            "hit_rate": round(self.hit_rate, 4),
            "miss_rate": round(self.miss_rate, 4),
            "top_hits": self.top_hits(10),
            "top_misses": self.top_misses(10),
        }


# ============================================================================
# QUERY PATTERN ANALYZER
# ============================================================================

class QueryPatternAnalyzer:
    """Analyze query patterns for optimization insights."""

    def __init__(self, window_size: int = PATTERN_WINDOW_SIZE) -> None:
        self._queries: Deque[Tuple[float, str, str]] = deque(maxlen=window_size)
        self._term_frequency: Dict[str, int] = Counter()
        self._type_frequency: Dict[str, int] = Counter()
        self._county_frequency: Dict[str, int] = Counter()
        self._operator_frequency: Dict[str, int] = Counter()
        self._hourly_counts: Dict[int, int] = Counter()
        self._lock = threading.Lock()

    def record_query(
        self,
        query_text: str,
        easement_type: str = "",
        county: str = "",
        pipeline_operator: str = "",
    ) -> None:
        """Record a search query for pattern analysis."""
        now = time.time()
        with self._lock:
            self._queries.append((now, query_text, easement_type))

            # Term frequency
            tokens = query_text.lower().split()
            for token in tokens:
                self._term_frequency[token] += 1

            # Filter frequency
            if easement_type:
                self._type_frequency[easement_type] += 1
            if county:
                self._county_frequency[county] += 1
            if pipeline_operator:
                self._operator_frequency[pipeline_operator] += 1

            # Hourly distribution
            hour = datetime.fromtimestamp(now, tz=timezone.utc).hour
            self._hourly_counts[hour] += 1

    def top_terms(self, n: int = 20) -> List[Tuple[str, int]]:
        """Return most frequent query terms."""
        with self._lock:
            return Counter(self._term_frequency).most_common(n)

    def top_types(self, n: int = 10) -> List[Tuple[str, int]]:
        """Return most queried easement types."""
        with self._lock:
            return Counter(self._type_frequency).most_common(n)

    def top_counties(self, n: int = 10) -> List[Tuple[str, int]]:
        """Return most queried counties."""
        with self._lock:
            return Counter(self._county_frequency).most_common(n)

    def top_operators(self, n: int = 10) -> List[Tuple[str, int]]:
        """Return most queried operators."""
        with self._lock:
            return Counter(self._operator_frequency).most_common(n)

    def hourly_distribution(self) -> Dict[int, int]:
        """Return query counts by hour of day (UTC)."""
        with self._lock:
            return dict(sorted(self._hourly_counts.items()))

    def queries_per_minute(self, window_minutes: int = 5) -> float:
        """Calculate queries per minute over a recent window."""
        cutoff = time.time() - (window_minutes * 60)
        with self._lock:
            recent = sum(1 for ts, _, _ in self._queries if ts >= cutoff)
        return recent / max(window_minutes, 1)

    def unique_queries(self) -> int:
        """Count unique query texts."""
        with self._lock:
            return len({q for _, q, _ in self._queries})

    def reset(self) -> None:
        """Reset all pattern data."""
        with self._lock:
            self._queries.clear()
            self._term_frequency.clear()
            self._type_frequency.clear()
            self._county_frequency.clear()
            self._operator_frequency.clear()
            self._hourly_counts.clear()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_queries": len(self._queries),
            "unique_queries": self.unique_queries(),
            "queries_per_minute": round(self.queries_per_minute(), 2),
            "top_terms": self.top_terms(15),
            "top_types": self.top_types(10),
            "top_counties": self.top_counties(10),
            "top_operators": self.top_operators(10),
            "hourly_distribution": self.hourly_distribution(),
        }


# ============================================================================
# ERROR TRACKER
# ============================================================================

class ErrorTracker:
    """Track error rates and patterns."""

    def __init__(self, window_size: int = 200) -> None:
        self._errors: Deque[Tuple[float, str, str, str]] = deque(maxlen=window_size)
        self._error_counts: Dict[str, int] = Counter()
        self._total_requests: int = 0
        self._total_errors: int = 0
        self._lock = threading.Lock()

    def record_request(self) -> None:
        """Record a successful request."""
        with self._lock:
            self._total_requests += 1

    def record_error(self, error_type: str, message: str, endpoint: str = "") -> None:
        """Record an error occurrence."""
        with self._lock:
            now = time.time()
            self._errors.append((now, error_type, message, endpoint))
            self._error_counts[error_type] += 1
            self._total_errors += 1
            self._total_requests += 1

    @property
    def error_rate(self) -> float:
        if self._total_requests == 0:
            return 0.0
        return self._total_errors / self._total_requests

    def recent_errors(self, n: int = 10) -> List[Dict[str, Any]]:
        """Return the N most recent errors."""
        with self._lock:
            recent = list(self._errors)[-n:]
            return [
                {
                    "timestamp": datetime.fromtimestamp(ts, tz=timezone.utc).isoformat(),
                    "type": etype,
                    "message": msg,
                    "endpoint": ep,
                }
                for ts, etype, msg, ep in reversed(recent)
            ]

    def error_distribution(self) -> Dict[str, int]:
        """Return error counts by type."""
        with self._lock:
            return dict(Counter(self._error_counts).most_common(20))

    def errors_per_minute(self, window_minutes: int = 5) -> float:
        """Calculate errors per minute over a recent window."""
        cutoff = time.time() - (window_minutes * 60)
        with self._lock:
            recent = sum(1 for ts, _, _, _ in self._errors if ts >= cutoff)
        return recent / max(window_minutes, 1)

    def reset(self) -> None:
        """Reset all error data."""
        with self._lock:
            self._errors.clear()
            self._error_counts.clear()
            self._total_requests = 0
            self._total_errors = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_requests": self._total_requests,
            "total_errors": self._total_errors,
            "error_rate": round(self.error_rate, 4),
            "errors_per_minute": round(self.errors_per_minute(), 2),
            "error_distribution": self.error_distribution(),
            "recent_errors": self.recent_errors(5),
        }


# ============================================================================
# AUDIT LOGGER - APPEND-ONLY JSONL
# ============================================================================

class AuditLogger:
    """Append-only JSON Lines audit trail for all engine operations."""

    def __init__(self, log_dir: Optional[Path] = None) -> None:
        self._log_dir = log_dir or AUDIT_LOG_DIR
        self._log_dir.mkdir(parents=True, exist_ok=True)
        self._current_file: Optional[Path] = None
        self._buffer: List[Dict[str, Any]] = []
        self._lock = threading.Lock()
        self._total_entries: int = 0
        self._rotate_if_needed()

    def _rotate_if_needed(self) -> None:
        """Rotate to a new log file if needed (daily rotation)."""
        today = datetime.now(timezone.utc).strftime("%Y%m%d")
        target = self._log_dir / f"lm14_audit_{today}.jsonl"
        if self._current_file != target:
            self.flush()
            self._current_file = target

    def log(
        self,
        action: str,
        endpoint: str = "",
        query: str = "",
        result_count: int = 0,
        latency_ms: float = 0.0,
        user_id: str = "",
        session_id: str = "",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Record an audit entry."""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "engine_id": ENGINE_ID,
            "engine_version": ENGINE_VERSION,
            "action": action,
            "endpoint": endpoint,
            "query": query,
            "result_count": result_count,
            "latency_ms": round(latency_ms, 2),
            "user_id": user_id,
            "session_id": session_id,
            "metadata": metadata or {},
        }

        with self._lock:
            self._buffer.append(entry)
            self._total_entries += 1

            if len(self._buffer) >= MAX_BUFFER_SIZE:
                self._flush_buffer()

    def log_search(
        self,
        query: str,
        filters: Dict[str, Any],
        result_count: int,
        latency_ms: float,
        session_id: str = "",
    ) -> None:
        """Log a search operation with full context."""
        self.log(
            action="search",
            endpoint="/search",
            query=query,
            result_count=result_count,
            latency_ms=latency_ms,
            session_id=session_id,
            metadata={"filters": filters},
        )

    def log_analysis(
        self,
        analysis_type: str,
        input_summary: str,
        output_summary: str,
        latency_ms: float,
        session_id: str = "",
    ) -> None:
        """Log an analysis operation."""
        self.log(
            action="analysis",
            endpoint=f"/analyze/{analysis_type}",
            query=input_summary,
            latency_ms=latency_ms,
            session_id=session_id,
            metadata={
                "analysis_type": analysis_type,
                "output_summary": output_summary,
            },
        )

    def log_error(
        self,
        error_type: str,
        message: str,
        endpoint: str = "",
        session_id: str = "",
    ) -> None:
        """Log an error event."""
        self.log(
            action="error",
            endpoint=endpoint,
            session_id=session_id,
            metadata={
                "error_type": error_type,
                "message": message,
            },
        )

    def flush(self) -> None:
        """Flush the buffer to disk."""
        with self._lock:
            self._flush_buffer()

    def _flush_buffer(self) -> None:
        """Internal flush (must be called under lock)."""
        if not self._buffer or not self._current_file:
            return

        try:
            self._rotate_if_needed()
            with open(self._current_file, "a", encoding="utf-8") as f:
                for entry in self._buffer:
                    f.write(json.dumps(entry, default=str) + "\n")
            logger.debug(f"Audit log flushed: {len(self._buffer)} entries to {self._current_file}")
            self._buffer.clear()
        except OSError as e:
            logger.error(f"Failed to flush audit log: {e}")

    @property
    def total_entries(self) -> int:
        return self._total_entries

    @property
    def buffer_size(self) -> int:
        with self._lock:
            return len(self._buffer)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_entries": self._total_entries,
            "buffer_size": self.buffer_size,
            "log_dir": str(self._log_dir),
            "current_file": str(self._current_file) if self._current_file else None,
        }


# ============================================================================
# TELEMETRY COLLECTOR - MAIN CLASS
# ============================================================================

class TelemetryCollector:
    """
    Core telemetry aggregation engine for LM14.
    Combines latency tracking, cache metrics, error rates,
    query patterns, and audit logging into a unified collector.
    """

    def __init__(self, audit_log_dir: Optional[Path] = None) -> None:
        self.latency = LatencyTracker()
        self.cache = CacheMetrics()
        self.errors = ErrorTracker()
        self.patterns = QueryPatternAnalyzer()
        self.audit = AuditLogger(log_dir=audit_log_dir)

        self._start_time = time.time()
        self._custom_metrics: Dict[str, MetricsBucket] = {}
        self._lock = threading.Lock()

        logger.info(f"LM14 Telemetry Collector initialized at {datetime.now(timezone.utc).isoformat()}")

    @property
    def uptime_seconds(self) -> float:
        return time.time() - self._start_time

    def record_request(
        self,
        endpoint: str,
        latency_ms: float,
        query: str = "",
        result_count: int = 0,
        easement_type: str = "",
        county: str = "",
        pipeline_operator: str = "",
        session_id: str = "",
        error: Optional[str] = None,
    ) -> None:
        """Record a complete request cycle with all metrics."""
        # Latency
        self.latency.record(endpoint, latency_ms)

        # Error or success
        if error:
            self.errors.record_error(error, f"Error on {endpoint}", endpoint)
            self.audit.log_error(error, f"Error on {endpoint}", endpoint, session_id)
        else:
            self.errors.record_request()

        # Query patterns
        if query:
            self.patterns.record_query(query, easement_type, county, pipeline_operator)

        # Audit
        self.audit.log(
            action="request",
            endpoint=endpoint,
            query=query,
            result_count=result_count,
            latency_ms=latency_ms,
            session_id=session_id,
        )

    def record_cache_access(self, topic: str, hit: bool) -> None:
        """Record a doctrine cache access."""
        if hit:
            self.cache.record_hit(topic)
        else:
            self.cache.record_miss(topic)

    def record_custom_metric(self, name: str, value: float) -> None:
        """Record a custom metric value."""
        with self._lock:
            if name not in self._custom_metrics:
                self._custom_metrics[name] = MetricsBucket(
                    name=f"{METRICS_PREFIX}.custom.{name}",
                    metric_type=MetricType.GAUGE,
                )
            self._custom_metrics[name].record(value)

    @contextmanager
    def timer(self, endpoint: str) -> Generator[None, None, None]:
        """Context manager to time an operation and record latency."""
        start = time.time()
        try:
            yield
        finally:
            elapsed_ms = (time.time() - start) * 1000
            self.latency.record(endpoint, elapsed_ms)

    def flush(self) -> None:
        """Flush all buffers."""
        self.audit.flush()

    def reset(self) -> None:
        """Reset all telemetry data."""
        self.latency.reset()
        self.cache.reset()
        self.errors.reset()
        self.patterns.reset()
        with self._lock:
            for bucket in self._custom_metrics.values():
                bucket.reset()
        logger.info("LM14 Telemetry Collector reset")

    def get_dashboard(self) -> Dict[str, Any]:
        """Return a comprehensive telemetry dashboard."""
        custom_metrics = {}
        with self._lock:
            for name, bucket in self._custom_metrics.items():
                custom_metrics[name] = bucket.to_dict()

        return {
            "engine_id": ENGINE_ID,
            "engine_name": ENGINE_NAME,
            "engine_version": ENGINE_VERSION,
            "uptime_seconds": round(self.uptime_seconds, 1),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "latency": self.latency.to_dict(),
            "cache": self.cache.to_dict(),
            "errors": self.errors.to_dict(),
            "patterns": self.patterns.to_dict(),
            "audit": self.audit.to_dict(),
            "custom_metrics": custom_metrics,
            "slow_endpoints": self.latency.get_slow_endpoints(),
        }

    def get_summary(self) -> Dict[str, Any]:
        """Return a compact telemetry summary for health checks."""
        return {
            "engine_id": ENGINE_ID,
            "uptime_seconds": round(self.uptime_seconds, 1),
            "total_requests": self.errors._total_requests,
            "total_errors": self.errors._total_errors,
            "error_rate": round(self.errors.error_rate, 4),
            "cache_hit_rate": round(self.cache.hit_rate, 4),
            "queries_per_minute": round(self.patterns.queries_per_minute(), 2),
            "audit_entries": self.audit.total_entries,
        }

    def to_dict(self) -> Dict[str, Any]:
        """Alias for get_dashboard."""
        return self.get_dashboard()


# ============================================================================
# MODULE-LEVEL SINGLETON
# ============================================================================

_TELEMETRY: Optional[TelemetryCollector] = None


def get_telemetry() -> TelemetryCollector:
    """Return the global telemetry collector, creating if necessary."""
    global _TELEMETRY
    if _TELEMETRY is None:
        _TELEMETRY = TelemetryCollector()
    return _TELEMETRY


def telemetry_health() -> Dict[str, Any]:
    """Return telemetry subsystem health."""
    return get_telemetry().get_summary()


def telemetry_dashboard() -> Dict[str, Any]:
    """Return the full telemetry dashboard."""
    return get_telemetry().get_dashboard()


def reset_telemetry() -> None:
    """Reset all telemetry data."""
    get_telemetry().reset()
