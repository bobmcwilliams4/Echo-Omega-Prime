"""
LG09 Criminal Law Engine - Telemetry Module
=============================================
Performance telemetry, metrics collection, and operational monitoring
for the Criminal Law TIE-20 engine.

Features:
    - Query tracing with full lifecycle tracking
    - Latency histograms and percentile calculations
    - Doctrine cache hit/miss monitoring
    - Error domain classification and tracking
    - Mutation logging for doctrine changes
    - Resource utilization monitoring
    - Exportable metrics snapshots

Author: ECHO OMEGA PRIME
Engine: LG09 Criminal Law
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
from typing import Any, ClassVar, Dict, List, Optional, Tuple

from loguru import logger
from pydantic import BaseModel, Field


# =============================================================================
# ENUMS
# =============================================================================

class ResponseLayer(str, Enum):
    """Which analysis layer handled the query."""
    QUICK = "quick"
    STANDARD = "standard"
    DEEP = "deep"
    CACHE_HIT = "cache_hit"
    FALLBACK = "fallback"


class ErrorDomain(str, Enum):
    """Classification of error domains for tracking."""
    DOCTRINE_LOOKUP = "doctrine_lookup"
    SEMANTIC_NORMALIZATION = "semantic_normalization"
    VECTOR_SEARCH = "vector_search"
    CONFIDENCE_SCORING = "confidence_scoring"
    RESPONSE_GENERATION = "response_generation"
    INPUT_VALIDATION = "input_validation"
    SERIALIZATION = "serialization"
    JURISDICTION_RESOLUTION = "jurisdiction_resolution"
    CITATION_VERIFICATION = "citation_verification"
    AUDIT_TRAIL = "audit_trail"
    CONFIGURATION = "configuration"
    HEALTH_CHECK = "health_check"
    UNKNOWN = "unknown"


class MutationType(str, Enum):
    """Types of doctrine mutations."""
    DOCTRINE_ADDED = "doctrine_added"
    DOCTRINE_UPDATED = "doctrine_updated"
    DOCTRINE_DEPRECATED = "doctrine_deprecated"
    DOCTRINE_REMOVED = "doctrine_removed"
    CITATION_ADDED = "citation_added"
    CITATION_UPDATED = "citation_updated"
    COVERAGE_EXPANDED = "coverage_expanded"
    CONFIDENCE_ADJUSTED = "confidence_adjusted"
    SEMANTIC_MAPPING_ADDED = "semantic_mapping_added"


class MutationOrigin(str, Enum):
    """Origin of a doctrine mutation."""
    SYSTEM_INIT = "system_init"
    ADMIN_OVERRIDE = "admin_override"
    DRIFT_CORRECTION = "drift_correction"
    AUTO_UPDATE = "auto_update"
    USER_FEEDBACK = "user_feedback"
    QUALITY_GATE = "quality_gate"
    EXTERNAL_SYNC = "external_sync"


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class QueryTrace:
    """Full lifecycle trace for a single query."""
    trace_id: str
    query_text: str
    started_at: float
    completed_at: Optional[float] = None
    response_layer: Optional[ResponseLayer] = None
    doctrine_keys_hit: list = field(default_factory=list)
    doctrine_keys_missed: list = field(default_factory=list)
    semantic_normalizations: int = 0
    vector_searches_performed: int = 0
    vector_results_count: int = 0
    confidence_score: float = 0.0
    response_mode: str = "DET"
    jurisdiction: str = "unknown"
    error: Optional[str] = None
    metadata: dict = field(default_factory=dict)

    @property
    def latency_ms(self) -> float:
        if self.completed_at is None:
            return (time.time() - self.started_at) * 1000
        return (self.completed_at - self.started_at) * 1000

    @property
    def is_complete(self) -> bool:
        return self.completed_at is not None

    @property
    def is_error(self) -> bool:
        return self.error is not None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "trace_id": self.trace_id,
            "query_text": self.query_text[:200],
            "started_at": datetime.fromtimestamp(self.started_at, tz=timezone.utc).isoformat(),
            "completed_at": datetime.fromtimestamp(self.completed_at, tz=timezone.utc).isoformat() if self.completed_at else None,
            "latency_ms": round(self.latency_ms, 2),
            "response_layer": self.response_layer.value if self.response_layer else None,
            "doctrine_hits": len(self.doctrine_keys_hit),
            "doctrine_misses": len(self.doctrine_keys_missed),
            "semantic_normalizations": self.semantic_normalizations,
            "vector_searches": self.vector_searches_performed,
            "vector_results": self.vector_results_count,
            "confidence_score": round(self.confidence_score, 4),
            "response_mode": self.response_mode,
            "jurisdiction": self.jurisdiction,
            "error": self.error,
            "metadata": self.metadata,
        }


@dataclass
class DoctrineMutation:
    """Record of a doctrine change."""
    mutation_id: str
    timestamp: float
    mutation_type: MutationType
    origin: MutationOrigin
    doctrine_key: str
    old_hash: Optional[str]
    new_hash: str
    description: str
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "mutation_id": self.mutation_id,
            "timestamp": datetime.fromtimestamp(self.timestamp, tz=timezone.utc).isoformat(),
            "mutation_type": self.mutation_type.value,
            "origin": self.origin.value,
            "doctrine_key": self.doctrine_key,
            "old_hash": self.old_hash,
            "new_hash": self.new_hash,
            "description": self.description,
            "metadata": self.metadata,
        }


# =============================================================================
# LATENCY HISTOGRAM
# =============================================================================

class LatencyHistogram:
    """Track latency distribution with configurable buckets."""

    DEFAULT_BUCKETS: ClassVar[List[float]] = [
        5.0, 10.0, 25.0, 50.0, 100.0, 250.0, 500.0,
        1000.0, 2500.0, 5000.0, 10000.0, 30000.0,
    ]

    def __init__(self, buckets: Optional[List[float]] = None, max_samples: int = 10000):
        self._buckets = sorted(buckets or self.DEFAULT_BUCKETS)
        self._counts: Dict[str, int] = {}
        for b in self._buckets:
            self._counts[f"le_{b}"] = 0
        self._counts["le_inf"] = 0
        self._samples: deque = deque(maxlen=max_samples)
        self._total_count: int = 0
        self._total_sum: float = 0.0
        self._lock = threading.Lock()

    def observe(self, value_ms: float) -> None:
        with self._lock:
            self._samples.append(value_ms)
            self._total_count += 1
            self._total_sum += value_ms
            for b in self._buckets:
                if value_ms <= b:
                    self._counts[f"le_{b}"] += 1
            self._counts["le_inf"] += 1

    def percentile(self, p: float) -> float:
        with self._lock:
            if not self._samples:
                return 0.0
            sorted_samples = sorted(self._samples)
            idx = int(len(sorted_samples) * p / 100.0)
            idx = min(idx, len(sorted_samples) - 1)
            return sorted_samples[idx]

    def mean(self) -> float:
        with self._lock:
            if self._total_count == 0:
                return 0.0
            return self._total_sum / self._total_count

    def stddev(self) -> float:
        with self._lock:
            if len(self._samples) < 2:
                return 0.0
            return statistics.stdev(self._samples)

    def summary(self) -> Dict[str, Any]:
        with self._lock:
            return {
                "count": self._total_count,
                "sum_ms": round(self._total_sum, 2),
                "mean_ms": round(self.mean(), 2),
                "stddev_ms": round(self.stddev(), 2) if len(self._samples) >= 2 else 0.0,
                "p50_ms": round(self.percentile(50), 2),
                "p90_ms": round(self.percentile(90), 2),
                "p95_ms": round(self.percentile(95), 2),
                "p99_ms": round(self.percentile(99), 2),
                "min_ms": round(min(self._samples), 2) if self._samples else 0.0,
                "max_ms": round(max(self._samples), 2) if self._samples else 0.0,
                "buckets": dict(self._counts),
            }


# =============================================================================
# ERROR TRACKER
# =============================================================================

class ErrorTracker:
    """Track errors by domain with rate calculation."""

    def __init__(self, window_seconds: int = 3600, max_errors: int = 5000):
        self._errors: deque = deque(maxlen=max_errors)
        self._domain_counts: Dict[str, int] = defaultdict(int)
        self._window = window_seconds
        self._lock = threading.Lock()

    def record(self, domain: ErrorDomain, message: str, trace_id: Optional[str] = None) -> None:
        now = time.time()
        entry = {
            "timestamp": now,
            "domain": domain.value,
            "message": message[:500],
            "trace_id": trace_id,
        }
        with self._lock:
            self._errors.append(entry)
            self._domain_counts[domain.value] += 1

    def errors_in_window(self, window_seconds: Optional[int] = None) -> int:
        window = window_seconds or self._window
        cutoff = time.time() - window
        with self._lock:
            return sum(1 for e in self._errors if e["timestamp"] > cutoff)

    def error_rate_per_minute(self, window_seconds: int = 300) -> float:
        count = self.errors_in_window(window_seconds)
        minutes = window_seconds / 60.0
        return round(count / minutes, 4) if minutes > 0 else 0.0

    def errors_by_domain(self, window_seconds: Optional[int] = None) -> Dict[str, int]:
        window = window_seconds or self._window
        cutoff = time.time() - window
        counts: Dict[str, int] = defaultdict(int)
        with self._lock:
            for e in self._errors:
                if e["timestamp"] > cutoff:
                    counts[e["domain"]] += 1
        return dict(counts)

    def recent_errors(self, limit: int = 20) -> List[Dict[str, Any]]:
        with self._lock:
            recent = list(self._errors)[-limit:]
        result = []
        for e in reversed(recent):
            result.append({
                "timestamp": datetime.fromtimestamp(e["timestamp"], tz=timezone.utc).isoformat(),
                "domain": e["domain"],
                "message": e["message"],
                "trace_id": e["trace_id"],
            })
        return result

    def summary(self) -> Dict[str, Any]:
        return {
            "total_errors": sum(self._domain_counts.values()),
            "errors_last_hour": self.errors_in_window(3600),
            "errors_last_5min": self.errors_in_window(300),
            "error_rate_per_min": self.error_rate_per_minute(),
            "by_domain": self.errors_by_domain(),
            "recent": self.recent_errors(5),
        }


# =============================================================================
# MUTATION LOG
# =============================================================================

class MutationLog:
    """Append-only log of doctrine mutations."""

    def __init__(self, max_entries: int = 10000):
        self._mutations: deque = deque(maxlen=max_entries)
        self._lock = threading.Lock()

    def record(
        self,
        mutation_type: MutationType,
        origin: MutationOrigin,
        doctrine_key: str,
        new_hash: str,
        description: str,
        old_hash: Optional[str] = None,
        metadata: Optional[Dict] = None,
    ) -> DoctrineMutation:
        mutation = DoctrineMutation(
            mutation_id=str(uuid.uuid4()),
            timestamp=time.time(),
            mutation_type=mutation_type,
            origin=origin,
            doctrine_key=doctrine_key,
            old_hash=old_hash,
            new_hash=new_hash,
            description=description,
            metadata=metadata or {},
        )
        with self._lock:
            self._mutations.append(mutation)
        logger.info(
            f"Doctrine mutation: {mutation_type.value} on {doctrine_key} "
            f"by {origin.value} — {description[:100]}"
        )
        return mutation

    def recent(self, limit: int = 20) -> List[Dict[str, Any]]:
        with self._lock:
            entries = list(self._mutations)[-limit:]
        return [m.to_dict() for m in reversed(entries)]

    def mutations_for_key(self, doctrine_key: str) -> List[Dict[str, Any]]:
        with self._lock:
            matches = [m for m in self._mutations if m.doctrine_key == doctrine_key]
        return [m.to_dict() for m in matches]

    def mutation_count_by_type(self) -> Dict[str, int]:
        counts: Dict[str, int] = defaultdict(int)
        with self._lock:
            for m in self._mutations:
                counts[m.mutation_type.value] += 1
        return dict(counts)

    def summary(self) -> Dict[str, Any]:
        with self._lock:
            total = len(self._mutations)
        return {
            "total_mutations": total,
            "by_type": self.mutation_count_by_type(),
            "recent": self.recent(5),
        }


# =============================================================================
# THROUGHPUT TRACKER
# =============================================================================

class ThroughputTracker:
    """Track queries per second / minute with sliding window."""

    def __init__(self, window_seconds: int = 60, max_timestamps: int = 50000):
        self._timestamps: deque = deque(maxlen=max_timestamps)
        self._window = window_seconds
        self._lock = threading.Lock()

    def record(self) -> None:
        with self._lock:
            self._timestamps.append(time.time())

    def queries_in_window(self, window_seconds: Optional[int] = None) -> int:
        window = window_seconds or self._window
        cutoff = time.time() - window
        with self._lock:
            return sum(1 for t in self._timestamps if t > cutoff)

    def qps(self) -> float:
        count = self.queries_in_window(60)
        return round(count / 60.0, 4)

    def qpm(self) -> float:
        return float(self.queries_in_window(60))

    def summary(self) -> Dict[str, Any]:
        return {
            "queries_last_minute": self.queries_in_window(60),
            "queries_last_5min": self.queries_in_window(300),
            "queries_last_hour": self.queries_in_window(3600),
            "qps": self.qps(),
            "qpm": self.qpm(),
        }


# =============================================================================
# DOCTRINE CACHE METRICS
# =============================================================================

class DoctrineCacheMetrics:
    """Track doctrine cache performance."""

    def __init__(self):
        self._hits: int = 0
        self._misses: int = 0
        self._hit_keys: Dict[str, int] = defaultdict(int)
        self._miss_keys: Dict[str, int] = defaultdict(int)
        self._lock = threading.Lock()

    def record_hit(self, key: str) -> None:
        with self._lock:
            self._hits += 1
            self._hit_keys[key] += 1

    def record_miss(self, key: str) -> None:
        with self._lock:
            self._misses += 1
            self._miss_keys[key] += 1

    @property
    def hit_rate(self) -> float:
        total = self._hits + self._misses
        if total == 0:
            return 0.0
        return round(self._hits / total, 4)

    def top_hits(self, limit: int = 10) -> List[Tuple[str, int]]:
        with self._lock:
            sorted_keys = sorted(self._hit_keys.items(), key=lambda x: x[1], reverse=True)
        return sorted_keys[:limit]

    def top_misses(self, limit: int = 10) -> List[Tuple[str, int]]:
        with self._lock:
            sorted_keys = sorted(self._miss_keys.items(), key=lambda x: x[1], reverse=True)
        return sorted_keys[:limit]

    def summary(self) -> Dict[str, Any]:
        return {
            "hits": self._hits,
            "misses": self._misses,
            "hit_rate": self.hit_rate,
            "total_lookups": self._hits + self._misses,
            "top_hits": [{"key": k, "count": v} for k, v in self.top_hits(5)],
            "top_misses": [{"key": k, "count": v} for k, v in self.top_misses(5)],
        }


# =============================================================================
# JURISDICTION METRICS
# =============================================================================

class JurisdictionMetrics:
    """Track query distribution across jurisdictions."""

    def __init__(self):
        self._counts: Dict[str, int] = defaultdict(int)
        self._latencies: Dict[str, List[float]] = defaultdict(list)
        self._lock = threading.Lock()

    def record(self, jurisdiction: str, latency_ms: float) -> None:
        with self._lock:
            self._counts[jurisdiction] += 1
            self._latencies[jurisdiction].append(latency_ms)
            if len(self._latencies[jurisdiction]) > 1000:
                self._latencies[jurisdiction] = self._latencies[jurisdiction][-500:]

    def summary(self) -> Dict[str, Any]:
        result = {}
        with self._lock:
            for j, count in self._counts.items():
                lats = self._latencies.get(j, [])
                avg_lat = sum(lats) / len(lats) if lats else 0.0
                result[j] = {
                    "query_count": count,
                    "avg_latency_ms": round(avg_lat, 2),
                }
        return result


# =============================================================================
# CONFIDENCE DISTRIBUTION TRACKER
# =============================================================================

class ConfidenceDistribution:
    """Track distribution of confidence scores across queries."""

    BUCKETS: ClassVar[List[str]] = [
        "SPECULATIVE_0_40",
        "LOW_40_60",
        "MODERATE_60_80",
        "HIGH_80_95",
        "DEFINITIVE_95_100",
    ]

    def __init__(self):
        self._counts: Dict[str, int] = {b: 0 for b in self.BUCKETS}
        self._scores: deque = deque(maxlen=5000)
        self._lock = threading.Lock()

    def record(self, score: float) -> None:
        with self._lock:
            self._scores.append(score)
            if score >= 0.95:
                self._counts["DEFINITIVE_95_100"] += 1
            elif score >= 0.80:
                self._counts["HIGH_80_95"] += 1
            elif score >= 0.60:
                self._counts["MODERATE_60_80"] += 1
            elif score >= 0.40:
                self._counts["LOW_40_60"] += 1
            else:
                self._counts["SPECULATIVE_0_40"] += 1

    def mean_confidence(self) -> float:
        with self._lock:
            if not self._scores:
                return 0.0
            return round(sum(self._scores) / len(self._scores), 4)

    def summary(self) -> Dict[str, Any]:
        total = sum(self._counts.values())
        return {
            "distribution": dict(self._counts),
            "total_scored": total,
            "mean_confidence": self.mean_confidence(),
        }


# =============================================================================
# RESPONSE MODE TRACKER
# =============================================================================

class ResponseModeTracker:
    """Track usage of response modes (DET, EF, HYBRID)."""

    def __init__(self):
        self._counts: Dict[str, int] = defaultdict(int)
        self._latencies: Dict[str, List[float]] = defaultdict(list)
        self._lock = threading.Lock()

    def record(self, mode: str, latency_ms: float) -> None:
        with self._lock:
            self._counts[mode] += 1
            self._latencies[mode].append(latency_ms)
            if len(self._latencies[mode]) > 1000:
                self._latencies[mode] = self._latencies[mode][-500:]

    def summary(self) -> Dict[str, Any]:
        result = {}
        with self._lock:
            for mode, count in self._counts.items():
                lats = self._latencies.get(mode, [])
                avg_lat = sum(lats) / len(lats) if lats else 0.0
                result[mode] = {
                    "count": count,
                    "avg_latency_ms": round(avg_lat, 2),
                }
        return result


# =============================================================================
# MAIN TELEMETRY ENGINE
# =============================================================================

class TelemetryEngine:
    """
    Central telemetry coordinator for LG09 Criminal Law Engine.

    Aggregates all sub-trackers and provides unified metrics export.
    Thread-safe, lock-free reads where possible.
    """

    def __init__(self, engine_id: str = "LG09", log_dir: Optional[Path] = None):
        self.engine_id = engine_id
        self.log_dir = log_dir or Path("O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/LG09_criminal_law/logs")
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Sub-trackers
        self.latency = LatencyHistogram()
        self.errors = ErrorTracker()
        self.mutations = MutationLog()
        self.throughput = ThroughputTracker()
        self.doctrine_cache = DoctrineCacheMetrics()
        self.jurisdictions = JurisdictionMetrics()
        self.confidence = ConfidenceDistribution()
        self.response_modes = ResponseModeTracker()

        # Active traces
        self._active_traces: Dict[str, QueryTrace] = {}
        self._completed_traces: deque = deque(maxlen=1000)
        self._trace_lock = threading.Lock()

        # Boot timestamp
        self._boot_time = time.time()

        logger.info(f"Telemetry engine initialized for {engine_id}")

    # -------------------------------------------------------------------------
    # TRACE MANAGEMENT
    # -------------------------------------------------------------------------

    def trace_query(self, query_text: str, response_mode: str = "DET", jurisdiction: str = "unknown") -> str:
        """Start a new query trace. Returns trace_id."""
        trace_id = str(uuid.uuid4())
        trace = QueryTrace(
            trace_id=trace_id,
            query_text=query_text,
            started_at=time.time(),
            response_mode=response_mode,
            jurisdiction=jurisdiction,
        )
        with self._trace_lock:
            self._active_traces[trace_id] = trace
        self.throughput.record()
        logger.debug(f"Trace started: {trace_id} mode={response_mode} jurisdiction={jurisdiction}")
        return trace_id

    def complete_trace(
        self,
        trace_id: str,
        response_layer: ResponseLayer,
        confidence_score: float = 0.0,
        error: Optional[str] = None,
    ) -> Optional[QueryTrace]:
        """Complete a query trace and record metrics."""
        with self._trace_lock:
            trace = self._active_traces.pop(trace_id, None)
        if trace is None:
            logger.warning(f"Attempted to complete unknown trace: {trace_id}")
            return None

        trace.completed_at = time.time()
        trace.response_layer = response_layer
        trace.confidence_score = confidence_score
        trace.error = error

        # Record to sub-trackers
        latency = trace.latency_ms
        self.latency.observe(latency)
        self.response_modes.record(trace.response_mode, latency)
        self.jurisdictions.record(trace.jurisdiction, latency)
        self.confidence.record(confidence_score)

        if error:
            self.errors.record(ErrorDomain.RESPONSE_GENERATION, error, trace_id)

        with self._trace_lock:
            self._completed_traces.append(trace)

        logger.debug(
            f"Trace completed: {trace_id} layer={response_layer.value} "
            f"latency={latency:.1f}ms confidence={confidence_score:.3f}"
        )
        return trace

    def get_active_trace(self, trace_id: str) -> Optional[QueryTrace]:
        """Get an in-progress trace."""
        with self._trace_lock:
            return self._active_traces.get(trace_id)

    def record_doctrine_hit(self, trace_id: str, key: str) -> None:
        """Record a doctrine cache hit for a trace."""
        with self._trace_lock:
            trace = self._active_traces.get(trace_id)
            if trace:
                trace.doctrine_keys_hit.append(key)
        self.doctrine_cache.record_hit(key)

    def record_doctrine_miss(self, trace_id: str, key: str) -> None:
        """Record a doctrine cache miss for a trace."""
        with self._trace_lock:
            trace = self._active_traces.get(trace_id)
            if trace:
                trace.doctrine_keys_missed.append(key)
        self.doctrine_cache.record_miss(key)

    def record_semantic_normalization(self, trace_id: str) -> None:
        """Increment semantic normalization counter for a trace."""
        with self._trace_lock:
            trace = self._active_traces.get(trace_id)
            if trace:
                trace.semantic_normalizations += 1

    def record_vector_search(self, trace_id: str, results_count: int) -> None:
        """Record a vector search operation for a trace."""
        with self._trace_lock:
            trace = self._active_traces.get(trace_id)
            if trace:
                trace.vector_searches_performed += 1
                trace.vector_results_count += results_count

    # -------------------------------------------------------------------------
    # ERROR LOGGING
    # -------------------------------------------------------------------------

    def log_error(self, domain: ErrorDomain, message: str, trace_id: Optional[str] = None) -> None:
        """Log an error to the error tracker."""
        self.errors.record(domain, message, trace_id)
        logger.error(f"[{domain.value}] {message} (trace={trace_id})")

    # -------------------------------------------------------------------------
    # MUTATION RECORDING
    # -------------------------------------------------------------------------

    def record_doctrine_mutation(
        self,
        mutation_type: MutationType,
        origin: MutationOrigin,
        doctrine_key: str,
        new_hash: str,
        description: str,
        old_hash: Optional[str] = None,
        metadata: Optional[Dict] = None,
    ) -> DoctrineMutation:
        """Record a doctrine mutation event."""
        return self.mutations.record(
            mutation_type=mutation_type,
            origin=origin,
            doctrine_key=doctrine_key,
            new_hash=new_hash,
            description=description,
            old_hash=old_hash,
            metadata=metadata,
        )

    # -------------------------------------------------------------------------
    # METRICS EXPORT
    # -------------------------------------------------------------------------

    def get_full_metrics(self) -> Dict[str, Any]:
        """Export complete metrics snapshot."""
        uptime = time.time() - self._boot_time
        with self._trace_lock:
            active_count = len(self._active_traces)
            completed_count = len(self._completed_traces)

        return {
            "engine_id": self.engine_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "uptime_seconds": round(uptime, 1),
            "active_traces": active_count,
            "completed_traces_in_buffer": completed_count,
            "latency": self.latency.summary(),
            "throughput": self.throughput.summary(),
            "errors": self.errors.summary(),
            "doctrine_cache": self.doctrine_cache.summary(),
            "mutations": self.mutations.summary(),
            "jurisdictions": self.jurisdictions.summary(),
            "confidence": self.confidence.summary(),
            "response_modes": self.response_modes.summary(),
        }

    def get_health_metrics(self) -> Dict[str, Any]:
        """Lightweight health metrics for /health endpoint."""
        uptime = time.time() - self._boot_time
        return {
            "engine_id": self.engine_id,
            "status": "healthy",
            "uptime_seconds": round(uptime, 1),
            "active_queries": len(self._active_traces),
            "error_rate_per_min": self.errors.error_rate_per_minute(),
            "qps": self.throughput.qps(),
            "doctrine_hit_rate": self.doctrine_cache.hit_rate,
            "mean_latency_ms": round(self.latency.mean(), 2),
            "p95_latency_ms": round(self.latency.percentile(95), 2),
            "mean_confidence": self.confidence.mean_confidence(),
        }

    def recent_traces(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recently completed traces."""
        with self._trace_lock:
            traces = list(self._completed_traces)[-limit:]
        return [t.to_dict() for t in reversed(traces)]

    # -------------------------------------------------------------------------
    # PERSISTENCE
    # -------------------------------------------------------------------------

    def export_snapshot(self) -> Path:
        """Export full metrics snapshot to JSON file."""
        snapshot = self.get_full_metrics()
        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        filepath = self.log_dir / f"telemetry_snapshot_{ts}.json"
        filepath.write_text(json.dumps(snapshot, indent=2, default=str), encoding="utf-8")
        logger.info(f"Telemetry snapshot exported: {filepath}")
        return filepath

    def export_traces(self, limit: int = 100) -> Path:
        """Export recent traces to JSONL file."""
        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        filepath = self.log_dir / f"traces_{ts}.jsonl"
        traces = self.recent_traces(limit)
        lines = [json.dumps(t, default=str) for t in traces]
        filepath.write_text("\n".join(lines), encoding="utf-8")
        logger.info(f"Exported {len(traces)} traces to {filepath}")
        return filepath


# =============================================================================
# MODULE-LEVEL SINGLETON
# =============================================================================

_telemetry_instance: Optional[TelemetryEngine] = None
_init_lock = threading.Lock()


def get_telemetry(engine_id: str = "LG09", log_dir: Optional[Path] = None) -> TelemetryEngine:
    """Get or create the singleton telemetry engine."""
    global _telemetry_instance
    if _telemetry_instance is None:
        with _init_lock:
            if _telemetry_instance is None:
                _telemetry_instance = TelemetryEngine(engine_id=engine_id, log_dir=log_dir)
    return _telemetry_instance


def trace_query(query_text: str, response_mode: str = "DET", jurisdiction: str = "unknown") -> str:
    """Convenience: start a query trace."""
    return get_telemetry().trace_query(query_text, response_mode, jurisdiction)


def complete_trace(
    trace_id: str,
    response_layer: ResponseLayer,
    confidence_score: float = 0.0,
    error: Optional[str] = None,
) -> Optional[QueryTrace]:
    """Convenience: complete a query trace."""
    return get_telemetry().complete_trace(trace_id, response_layer, confidence_score, error)


def log_error(domain: ErrorDomain, message: str, trace_id: Optional[str] = None) -> None:
    """Convenience: log an error."""
    get_telemetry().log_error(domain, message, trace_id)


def record_doctrine_mutation(
    mutation_type: MutationType,
    origin: MutationOrigin,
    doctrine_key: str,
    new_hash: str,
    description: str,
    old_hash: Optional[str] = None,
    metadata: Optional[Dict] = None,
) -> DoctrineMutation:
    """Convenience: record a doctrine mutation."""
    return get_telemetry().record_doctrine_mutation(
        mutation_type, origin, doctrine_key, new_hash, description, old_hash, metadata
    )
