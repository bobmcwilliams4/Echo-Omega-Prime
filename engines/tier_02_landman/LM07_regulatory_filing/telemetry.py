"""
LM07 Regulatory Filing Engine - Telemetry Module
=================================================
Full query tracing, latency tracking, error domain classification,
metrics collection, and audit trail for oil & gas regulatory filing queries.
"""

from __future__ import annotations

import hashlib
import json
import statistics
import time
import threading
from collections import defaultdict, deque
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Optional
from uuid import uuid4

from loguru import logger


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
ENGINE_ID = "LM07"
ENGINE_NAME = "Regulatory Filing Engine"
TELEMETRY_VERSION = "1.0.0"
MAX_RECENT_QUERIES = 5000
MAX_ERROR_LOG = 2000
AUDIT_ROTATION_BYTES = 10 * 1024 * 1024  # 10 MB
LATENCY_BUCKETS_MS = [5, 10, 25, 50, 100, 250, 500, 1000, 2500, 5000, 10000]


class ErrorDomain(str, Enum):
    """Classification of error domains in regulatory filing analysis."""
    FORM_PARSE = "form_parse"
    JURISDICTION_MISMATCH = "jurisdiction_mismatch"
    AUTHORITY_CONFLICT = "authority_conflict"
    RULE_INTERPRETATION = "rule_interpretation"
    DEADLINE_CALCULATION = "deadline_calculation"
    FEE_COMPUTATION = "fee_computation"
    PERMIT_VALIDATION = "permit_validation"
    COMPLIANCE_CHECK = "compliance_check"
    PRODUCTION_REPORTING = "production_reporting"
    ENVIRONMENTAL = "environmental"
    PLUGGING_ABANDONMENT = "plugging_abandonment"
    SPACING_DENSITY = "spacing_density"
    FLARING_CURTAILMENT = "flaring_curtailment"
    H2S_SAFETY = "h2s_safety"
    OPERATOR_TRANSFER = "operator_transfer"
    INJECTION_DISPOSAL = "injection_disposal"
    PRORATION_ALLOWABLE = "proration_allowable"
    FEDERAL_LEASE = "federal_lease"
    DOCTRINE_MISS = "doctrine_miss"
    SEMANTIC_FAILURE = "semantic_failure"
    VECTOR_SEARCH_FAILURE = "vector_search_failure"
    CONFIGURATION = "configuration"
    TIMEOUT = "timeout"
    UNKNOWN = "unknown"


class QueryTier(str, Enum):
    """Which tier resolved the query."""
    DOCTRINE_CACHE = "doctrine_cache"
    SEMANTIC_RETRIEVAL = "semantic_retrieval"
    DEEP_ANALYSIS = "deep_analysis"
    FALLBACK = "fallback"


class QueryPhase(str, Enum):
    """Phases of query processing for trace instrumentation."""
    NORMALIZATION = "normalization"
    DOCTRINE_CACHE = "doctrine_cache"
    VECTOR_SEARCH = "vector_search"
    DEEP_ANALYSIS = "deep_analysis"


class ResponseMode(str, Enum):
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------
@dataclass
class QueryTrace:
    """Full trace of a single query through the engine."""
    trace_id: str = field(default_factory=lambda: uuid4().hex[:16])
    query_id: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    query_text: str = ""
    query_hash: str = ""
    normalized_query: str = ""
    response_mode: str = "FAST"
    mode: str = "FAST"
    tier_resolved: str = "doctrine_cache"
    doctrine_topics_hit: list[str] = field(default_factory=list)
    doctrine_topics_missed: list[str] = field(default_factory=list)
    jurisdiction: str = ""
    form_types: list[str] = field(default_factory=list)
    statewide_rules: list[str] = field(default_factory=list)
    confidence_level: str = ""
    confidence_score: float = 0.0
    latency_ms: float = 0.0
    cache_hit: bool = False
    vector_fallback: bool = False
    deep_analysis: bool = False
    vector_score: float = 0.0
    error_domain: Optional[str] = None
    error_message: Optional[str] = None
    determinism_hash: str = ""
    tokens_input: int = 0
    tokens_output: int = 0
    client_ip: str = ""
    user_agent: str = ""
    _phase_start: float = field(default=0.0, repr=False)
    _phases: list[str] = field(default_factory=list, repr=False)

    def __post_init__(self):
        if self.query_id and not self.trace_id:
            self.trace_id = self.query_id
        if not self.query_id:
            self.query_id = self.trace_id
        if self.mode and not self.response_mode:
            self.response_mode = self.mode

    def start_phase(self, phase) -> None:
        """Record entering a processing phase."""
        self._phase_start = time.time()
        phase_name = phase.value if hasattr(phase, 'value') else str(phase)
        self._phases.append(phase_name)

    def end_phase(self, phase) -> None:
        """Record completing a processing phase."""
        elapsed = (time.time() - self._phase_start) * 1000 if self._phase_start else 0.0
        self.latency_ms += elapsed
        self._phase_start = 0.0

    def enter_phase(self, phase) -> None:
        """Alias for start_phase."""
        self.start_phase(phase)

    def to_audit_line(self) -> str:
        """Serialize to JSONL for audit trail."""
        return json.dumps(asdict(self), default=str)


@dataclass
class LatencyStats:
    """Aggregated latency statistics."""
    count: int = 0
    total_ms: float = 0.0
    min_ms: float = float("inf")
    max_ms: float = 0.0
    mean_ms: float = 0.0
    median_ms: float = 0.0
    p95_ms: float = 0.0
    p99_ms: float = 0.0
    stddev_ms: float = 0.0
    values: list[float] = field(default_factory=list)

    def record(self, latency_ms: float) -> None:
        self.count += 1
        self.total_ms += latency_ms
        if latency_ms < self.min_ms:
            self.min_ms = latency_ms
        if latency_ms > self.max_ms:
            self.max_ms = latency_ms
        self.values.append(latency_ms)
        if len(self.values) > MAX_RECENT_QUERIES:
            self.values = self.values[-MAX_RECENT_QUERIES:]
        self._recalculate()

    def _recalculate(self) -> None:
        if not self.values:
            return
        self.mean_ms = statistics.mean(self.values)
        self.median_ms = statistics.median(self.values)
        sorted_vals = sorted(self.values)
        n = len(sorted_vals)
        self.p95_ms = sorted_vals[int(n * 0.95)] if n > 1 else sorted_vals[0]
        self.p99_ms = sorted_vals[int(n * 0.99)] if n > 1 else sorted_vals[0]
        self.stddev_ms = statistics.stdev(self.values) if n > 1 else 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "count": self.count,
            "total_ms": round(self.total_ms, 2),
            "min_ms": round(self.min_ms, 2) if self.min_ms != float("inf") else 0.0,
            "max_ms": round(self.max_ms, 2),
            "mean_ms": round(self.mean_ms, 2),
            "median_ms": round(self.median_ms, 2),
            "p95_ms": round(self.p95_ms, 2),
            "p99_ms": round(self.p99_ms, 2),
            "stddev_ms": round(self.stddev_ms, 2),
        }


@dataclass
class ErrorRecord:
    """Record of an error occurrence."""
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    error_domain: str = ErrorDomain.UNKNOWN.value
    error_message: str = ""
    trace_id: str = ""
    query_snippet: str = ""
    resolved: bool = False
    resolution: str = ""


# ---------------------------------------------------------------------------
# Metrics Collector
# ---------------------------------------------------------------------------
class MetricsCollector:
    """Centralized metrics collection for LM07 Regulatory Filing Engine."""

    def __init__(self, audit_dir: Optional[Path] = None) -> None:
        self._lock = threading.Lock()
        self._start_time = time.time()
        self._total_queries = 0
        self._successful_queries = 0
        self._failed_queries = 0
        self._cache_hits = 0
        self._cache_misses = 0
        self._tier_counts: dict[str, int] = defaultdict(int)
        self._mode_counts: dict[str, int] = defaultdict(int)
        self._jurisdiction_counts: dict[str, int] = defaultdict(int)
        self._form_type_counts: dict[str, int] = defaultdict(int)
        self._rule_counts: dict[str, int] = defaultdict(int)
        self._doctrine_hit_counts: dict[str, int] = defaultdict(int)
        self._doctrine_miss_counts: dict[str, int] = defaultdict(int)
        self._error_domain_counts: dict[str, int] = defaultdict(int)
        self._confidence_distribution: dict[str, int] = defaultdict(int)
        self._latency_overall = LatencyStats()
        self._latency_by_tier: dict[str, LatencyStats] = defaultdict(LatencyStats)
        self._latency_by_mode: dict[str, LatencyStats] = defaultdict(LatencyStats)
        self._latency_histogram: dict[str, int] = {f"<={b}ms": 0 for b in LATENCY_BUCKETS_MS}
        self._latency_histogram[f">{LATENCY_BUCKETS_MS[-1]}ms"] = 0
        self._recent_traces: deque[QueryTrace] = deque(maxlen=MAX_RECENT_QUERIES)
        self._recent_errors: deque[ErrorRecord] = deque(maxlen=MAX_ERROR_LOG)
        self._queries_per_minute: deque[float] = deque(maxlen=3600)

        # Audit trail
        self._audit_dir = audit_dir or Path("O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/LM07_regulatory_filing/audit")
        self._audit_dir.mkdir(parents=True, exist_ok=True)
        self._audit_file = self._audit_dir / f"audit_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.jsonl"
        self._audit_bytes_written = 0

        logger.info(
            "LM07 MetricsCollector initialized | audit_dir={} | audit_file={}",
            self._audit_dir, self._audit_file.name,
        )

    def record_query(self, trace: QueryTrace) -> None:
        """Record a completed query trace."""
        with self._lock:
            self._total_queries += 1
            self._queries_per_minute.append(time.time())

            if trace.error_domain:
                self._failed_queries += 1
                self._error_domain_counts[trace.error_domain] += 1
                self._recent_errors.append(ErrorRecord(
                    error_domain=trace.error_domain,
                    error_message=trace.error_message or "",
                    trace_id=trace.trace_id,
                    query_snippet=trace.query_text[:120],
                ))
            else:
                self._successful_queries += 1

            if trace.cache_hit:
                self._cache_hits += 1
            else:
                self._cache_misses += 1

            self._tier_counts[trace.tier_resolved] += 1
            self._mode_counts[trace.response_mode] += 1

            if trace.jurisdiction:
                self._jurisdiction_counts[trace.jurisdiction] += 1

            for ft in trace.form_types:
                self._form_type_counts[ft] += 1

            for sr in trace.statewide_rules:
                self._rule_counts[sr] += 1

            for dt in trace.doctrine_topics_hit:
                self._doctrine_hit_counts[dt] += 1

            for dm in trace.doctrine_topics_missed:
                self._doctrine_miss_counts[dm] += 1

            if trace.confidence_level:
                self._confidence_distribution[trace.confidence_level] += 1

            # Latency tracking
            self._latency_overall.record(trace.latency_ms)
            self._latency_by_tier[trace.tier_resolved].record(trace.latency_ms)
            self._latency_by_mode[trace.response_mode].record(trace.latency_ms)
            self._bucket_latency(trace.latency_ms)

            self._recent_traces.append(trace)

        # Audit trail (outside lock to avoid I/O blocking)
        self._write_audit(trace)

    def _bucket_latency(self, latency_ms: float) -> None:
        for bucket in LATENCY_BUCKETS_MS:
            if latency_ms <= bucket:
                self._latency_histogram[f"<={bucket}ms"] += 1
                return
        self._latency_histogram[f">{LATENCY_BUCKETS_MS[-1]}ms"] += 1

    def _write_audit(self, trace: QueryTrace) -> None:
        try:
            line = trace.to_audit_line() + "\n"
            line_bytes = line.encode("utf-8")
            if self._audit_bytes_written + len(line_bytes) > AUDIT_ROTATION_BYTES:
                self._audit_file = self._audit_dir / f"audit_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.jsonl"
                self._audit_bytes_written = 0
                logger.info("Audit log rotated to {}", self._audit_file.name)
            with open(self._audit_file, "a", encoding="utf-8") as f:
                f.write(line)
            self._audit_bytes_written += len(line_bytes)
        except Exception as exc:
            logger.error("Failed to write audit trail: {}", exc)

    def record_error(self, domain: ErrorDomain, message: str, trace_id: str = "", query: str = "") -> None:
        """Record a standalone error."""
        with self._lock:
            self._error_domain_counts[domain.value] += 1
            self._recent_errors.append(ErrorRecord(
                error_domain=domain.value,
                error_message=message,
                trace_id=trace_id,
                query_snippet=query[:120],
            ))

    def get_queries_per_minute(self) -> float:
        """Current query rate per minute."""
        now = time.time()
        with self._lock:
            recent = [t for t in self._queries_per_minute if now - t < 60]
            return float(len(recent))

    def get_queries_per_hour(self) -> float:
        """Current query rate per hour."""
        now = time.time()
        with self._lock:
            recent = [t for t in self._queries_per_minute if now - t < 3600]
            return float(len(recent))

    def get_uptime_seconds(self) -> float:
        return time.time() - self._start_time

    def get_cache_hit_rate(self) -> float:
        total = self._cache_hits + self._cache_misses
        return (self._cache_hits / total * 100) if total > 0 else 0.0

    def get_error_rate(self) -> float:
        if self._total_queries == 0:
            return 0.0
        return self._failed_queries / self._total_queries * 100

    def get_success_rate(self) -> float:
        if self._total_queries == 0:
            return 100.0
        return self._successful_queries / self._total_queries * 100

    def get_summary(self) -> dict[str, Any]:
        """Summary dict consumed by engine.get_health() and /metrics endpoint."""
        with self._lock:
            total = self._total_queries
            cache_total = self._cache_hits + self._cache_misses
            last_time: str | None = None
            if self._recent_traces:
                last_time = self._recent_traces[-1].timestamp if hasattr(self._recent_traces[-1], 'timestamp') else None
            return {
                "total_queries": total,
                "cache_hit_rate": round((self._cache_hits / cache_total * 100) if cache_total > 0 else 0.0, 2),
                "avg_latency_ms": round(self._latency_overall.mean_ms, 2) if self._latency_overall.count > 0 else 0.0,
                "error_rate": round((self._failed_queries / total * 100) if total > 0 else 0.0, 2),
                "last_query_time": last_time,
            }

    def get_top_doctrines(self, n: int = 10) -> list[tuple[str, int]]:
        with self._lock:
            return sorted(self._doctrine_hit_counts.items(), key=lambda x: x[1], reverse=True)[:n]

    def get_missed_doctrines(self, n: int = 10) -> list[tuple[str, int]]:
        with self._lock:
            return sorted(self._doctrine_miss_counts.items(), key=lambda x: x[1], reverse=True)[:n]

    def get_top_error_domains(self, n: int = 10) -> list[tuple[str, int]]:
        with self._lock:
            return sorted(self._error_domain_counts.items(), key=lambda x: x[1], reverse=True)[:n]

    def get_form_type_distribution(self) -> dict[str, int]:
        with self._lock:
            return dict(self._form_type_counts)

    def get_jurisdiction_distribution(self) -> dict[str, int]:
        with self._lock:
            return dict(self._jurisdiction_counts)

    def get_rule_distribution(self) -> dict[str, int]:
        with self._lock:
            return dict(self._rule_counts)

    def get_metrics_snapshot(self) -> dict[str, Any]:
        """Full metrics snapshot for health endpoint and monitoring."""
        with self._lock:
            uptime = self.get_uptime_seconds()
            return {
                "engine_id": ENGINE_ID,
                "engine_name": ENGINE_NAME,
                "telemetry_version": TELEMETRY_VERSION,
                "uptime_seconds": round(uptime, 1),
                "uptime_human": f"{int(uptime // 3600)}h {int((uptime % 3600) // 60)}m {int(uptime % 60)}s",
                "queries": {
                    "total": self._total_queries,
                    "successful": self._successful_queries,
                    "failed": self._failed_queries,
                    "success_rate_pct": round(self.get_success_rate(), 2),
                    "error_rate_pct": round(self.get_error_rate(), 2),
                    "per_minute": round(self.get_queries_per_minute(), 1),
                    "per_hour": round(self.get_queries_per_hour(), 1),
                },
                "cache": {
                    "hits": self._cache_hits,
                    "misses": self._cache_misses,
                    "hit_rate_pct": round(self.get_cache_hit_rate(), 2),
                },
                "latency": {
                    "overall": self._latency_overall.to_dict(),
                    "by_tier": {k: v.to_dict() for k, v in self._latency_by_tier.items()},
                    "by_mode": {k: v.to_dict() for k, v in self._latency_by_mode.items()},
                    "histogram": dict(self._latency_histogram),
                },
                "tiers": dict(self._tier_counts),
                "modes": dict(self._mode_counts),
                "jurisdictions": dict(self._jurisdiction_counts),
                "form_types": dict(self._form_type_counts),
                "statewide_rules": dict(self._rule_counts),
                "confidence_distribution": dict(self._confidence_distribution),
                "doctrine_coverage": {
                    "top_hits": self.get_top_doctrines(15),
                    "top_misses": self.get_missed_doctrines(15),
                },
                "errors": {
                    "by_domain": dict(self._error_domain_counts),
                    "recent_count": len(self._recent_errors),
                    "recent": [asdict(e) for e in list(self._recent_errors)[-10:]],
                },
                "audit": {
                    "current_file": str(self._audit_file.name),
                    "bytes_written": self._audit_bytes_written,
                    "directory": str(self._audit_dir),
                },
            }

    def get_recent_traces(self, n: int = 20) -> list[dict[str, Any]]:
        """Return most recent query traces."""
        with self._lock:
            return [asdict(t) for t in list(self._recent_traces)[-n:]]

    def reset(self) -> None:
        """Reset all metrics (for testing)."""
        with self._lock:
            self.__init__(audit_dir=self._audit_dir)
            logger.warning("LM07 MetricsCollector reset")


# ---------------------------------------------------------------------------
# Timing context manager
# ---------------------------------------------------------------------------
class QueryTimer:
    """Context manager for timing query execution."""

    def __init__(self) -> None:
        self.start_time: float = 0.0
        self.end_time: float = 0.0
        self.elapsed_ms: float = 0.0

    def __enter__(self) -> "QueryTimer":
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, *args: Any) -> None:
        self.end_time = time.perf_counter()
        self.elapsed_ms = (self.end_time - self.start_time) * 1000


# ---------------------------------------------------------------------------
# Determinism hashing
# ---------------------------------------------------------------------------
def compute_determinism_hash(
    query: str,
    response: str,
    doctrines_hit: list[str],
    confidence: str,
    jurisdiction: str,
) -> str:
    """Compute SHA-256 determinism hash for reproducibility verification."""
    payload = json.dumps(
        {
            "query": query,
            "response_prefix": response[:500] if response else "",
            "doctrines_hit": sorted(doctrines_hit),
            "confidence": confidence,
            "jurisdiction": jurisdiction,
            "engine_id": ENGINE_ID,
        },
        sort_keys=True,
        ensure_ascii=True,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# Coverage map tracker
# ---------------------------------------------------------------------------
class CoverageMap:
    """Track triggered vs missed doctrines for epistemic gap detection."""

    def __init__(self, topics: list[str] | None = None) -> None:
        self._lock = threading.Lock()
        self._triggered: dict[str, int] = defaultdict(int)
        self._missed: dict[str, int] = defaultdict(int)
        self._all_topics: set[str] = set()
        self._never_triggered: set[str] = set()
        if topics:
            self.register_topics(topics)

    def register_topics(self, topics: list[str]) -> None:
        """Register all available doctrine topics."""
        with self._lock:
            self._all_topics.update(topics)
            self._never_triggered = self._all_topics - set(self._triggered.keys())

    def record_hit(self, topic: str) -> None:
        with self._lock:
            self._triggered[topic] += 1
            self._never_triggered.discard(topic)

    def record_miss(self, topic: str) -> None:
        with self._lock:
            self._missed[topic] += 1

    def get_coverage_report(self) -> dict[str, Any]:
        with self._lock:
            total = len(self._all_topics) if self._all_topics else 1
            triggered_count = len(self._triggered)
            return {
                "total_registered_topics": len(self._all_topics),
                "triggered_topics": triggered_count,
                "coverage_pct": round(triggered_count / total * 100, 1),
                "never_triggered": sorted(self._never_triggered),
                "most_triggered": sorted(
                    self._triggered.items(), key=lambda x: x[1], reverse=True
                )[:15],
                "most_missed": sorted(
                    self._missed.items(), key=lambda x: x[1], reverse=True
                )[:15],
                "epistemic_gaps": sorted(self._never_triggered)[:20],
            }


# ---------------------------------------------------------------------------
# Drift watcher
# ---------------------------------------------------------------------------
class DriftWatcher:
    """Detect doctrine confidence drift over time."""

    def __init__(self, window_size: int = 100) -> None:
        self._lock = threading.Lock()
        self._window_size = window_size
        self._confidence_history: deque[tuple[str, float]] = deque(maxlen=window_size * 10)
        self._topic_confidence: dict[str, deque[float]] = defaultdict(lambda: deque(maxlen=window_size))

    def record(self, topic: str, confidence: float) -> None:
        with self._lock:
            ts = datetime.now(timezone.utc).isoformat()
            self._confidence_history.append((ts, confidence))
            self._topic_confidence[topic].append(confidence)

    def detect_drift(self, threshold: float = 0.1) -> list[dict[str, Any]]:
        """Detect topics where confidence is drifting significantly."""
        drifts = []
        with self._lock:
            for topic, scores in self._topic_confidence.items():
                if len(scores) < 10:
                    continue
                scores_list = list(scores)
                first_half = scores_list[: len(scores_list) // 2]
                second_half = scores_list[len(scores_list) // 2:]
                mean_first = statistics.mean(first_half)
                mean_second = statistics.mean(second_half)
                drift = mean_second - mean_first
                if abs(drift) > threshold:
                    drifts.append({
                        "topic": topic,
                        "drift_magnitude": round(drift, 4),
                        "direction": "INCREASING" if drift > 0 else "DECREASING",
                        "first_half_mean": round(mean_first, 4),
                        "second_half_mean": round(mean_second, 4),
                        "sample_count": len(scores_list),
                    })
        return sorted(drifts, key=lambda x: abs(x["drift_magnitude"]), reverse=True)

    def get_overall_trend(self) -> dict[str, Any]:
        with self._lock:
            if len(self._confidence_history) < 2:
                return {"trend": "INSUFFICIENT_DATA", "samples": len(self._confidence_history)}
            scores = [s for _, s in self._confidence_history]
            first_quarter = scores[: len(scores) // 4] if len(scores) >= 4 else scores[:1]
            last_quarter = scores[-(len(scores) // 4):] if len(scores) >= 4 else scores[-1:]
            mean_early = statistics.mean(first_quarter)
            mean_late = statistics.mean(last_quarter)
            return {
                "trend": "STABLE" if abs(mean_late - mean_early) < 0.05 else (
                    "IMPROVING" if mean_late > mean_early else "DEGRADING"
                ),
                "early_mean": round(mean_early, 4),
                "late_mean": round(mean_late, 4),
                "total_samples": len(scores),
                "overall_mean": round(statistics.mean(scores), 4),
                "overall_stddev": round(statistics.stdev(scores), 4) if len(scores) > 1 else 0.0,
            }


# ---------------------------------------------------------------------------
# Module-level singleton
# ---------------------------------------------------------------------------
_collector: Optional[MetricsCollector] = None
_coverage: Optional[CoverageMap] = None
_drift: Optional[DriftWatcher] = None


def get_collector() -> MetricsCollector:
    global _collector
    if _collector is None:
        _collector = MetricsCollector()
    return _collector


def get_coverage_map() -> CoverageMap:
    global _coverage
    if _coverage is None:
        _coverage = CoverageMap()
    return _coverage


def get_drift_watcher() -> DriftWatcher:
    global _drift
    if _drift is None:
        _drift = DriftWatcher()
    return _drift
