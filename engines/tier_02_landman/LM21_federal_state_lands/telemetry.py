"""
LM21 Federal/State Lands Engine - Telemetry Module
=====================================================
Full query tracing, latency tracking, error domain classification,
metrics collection, drift watching, coverage mapping, and audit trail.
"""

from __future__ import annotations

import hashlib
import json
import statistics
import time
import uuid
from collections import defaultdict
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from loguru import logger
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class QueryPhase(str, Enum):
    """Phases of query processing for latency tracking."""
    NORMALIZATION = "normalization"
    CACHE_LOOKUP = "cache_lookup"
    VECTOR_SEARCH = "vector_search"
    DEEP_ANALYSIS = "deep_analysis"
    AUTHORITY_HARDENING = "authority_hardening"
    CONFIDENCE_STRATIFICATION = "confidence_stratification"
    RESPONSE_ASSEMBLY = "response_assembly"
    TOTAL = "total"


class ErrorDomain(str, Enum):
    """Classification of error domains for telemetry."""
    NORMALIZATION_ERROR = "normalization_error"
    CACHE_MISS = "cache_miss"
    SEARCH_FAILURE = "search_failure"
    AUTHORITY_CONFLICT = "authority_conflict"
    CONFIDENCE_BELOW_THRESHOLD = "confidence_below_threshold"
    DOCTRINE_DRIFT = "doctrine_drift"
    COVERAGE_GAP = "coverage_gap"
    STATUTE_PARSE_ERROR = "statute_parse_error"
    TIMEOUT = "timeout"
    INTERNAL_ERROR = "internal_error"
    VALIDATION_ERROR = "validation_error"
    RATE_LIMITED = "rate_limited"


class DriftSeverity(str, Enum):
    """Severity levels for doctrine drift detection."""
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

class QueryTrace(BaseModel):
    """Complete trace of a single query through the engine."""
    trace_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    query: str = ""
    normalized_query: str = ""
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    session_id: str = ""
    response_mode: str = "FAST"
    analysis_zone: str = "PLANNING"
    cache_hit: bool = False
    cache_topic: str = ""
    search_results_count: int = 0
    search_top_score: float = 0.0
    doctrine_topics_triggered: List[str] = Field(default_factory=list)
    confidence_level: str = ""
    confidence_score: float = 0.0
    authority_chain: List[str] = Field(default_factory=list)
    latencies_ms: Dict[str, float] = Field(default_factory=dict)
    total_latency_ms: float = 0.0
    errors: List[str] = Field(default_factory=list)
    error_domains: List[str] = Field(default_factory=list)
    determinism_hash: str = ""
    response_length: int = 0
    fragility_score: float = 0.0


class LatencyBucket(BaseModel):
    """Aggregated latency statistics for a phase."""
    phase: str
    count: int = 0
    total_ms: float = 0.0
    min_ms: float = float("inf")
    max_ms: float = 0.0
    mean_ms: float = 0.0
    median_ms: float = 0.0
    p95_ms: float = 0.0
    p99_ms: float = 0.0
    values: List[float] = Field(default_factory=list, exclude=True)

    def record(self, value_ms: float) -> None:
        """Record a latency observation."""
        self.count += 1
        self.total_ms += value_ms
        self.min_ms = min(self.min_ms, value_ms)
        self.max_ms = max(self.max_ms, value_ms)
        self.values.append(value_ms)
        self.mean_ms = self.total_ms / self.count
        if len(self.values) >= 2:
            sorted_vals = sorted(self.values)
            self.median_ms = statistics.median(sorted_vals)
            idx_95 = int(len(sorted_vals) * 0.95)
            idx_99 = int(len(sorted_vals) * 0.99)
            self.p95_ms = sorted_vals[min(idx_95, len(sorted_vals) - 1)]
            self.p99_ms = sorted_vals[min(idx_99, len(sorted_vals) - 1)]
        else:
            self.median_ms = self.mean_ms
            self.p95_ms = self.max_ms
            self.p99_ms = self.max_ms


class DriftObservation(BaseModel):
    """A single doctrine drift observation."""
    observation_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    doctrine_topic: str = ""
    drift_type: str = ""
    severity: DriftSeverity = DriftSeverity.NONE
    description: str = ""
    previous_position: str = ""
    current_position: str = ""
    authority_change: str = ""
    remediation: str = ""


class CoverageEntry(BaseModel):
    """Coverage tracking for a single doctrine topic."""
    topic: str
    hit_count: int = 0
    miss_count: int = 0
    last_hit: str = ""
    last_miss: str = ""
    coverage_ratio: float = 0.0
    epistemic_gap: bool = False
    gap_description: str = ""


class MetricsSnapshot(BaseModel):
    """Point-in-time metrics snapshot."""
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    total_queries: int = 0
    cache_hit_rate: float = 0.0
    error_rate: float = 0.0
    avg_latency_ms: float = 0.0
    queries_per_minute: float = 0.0
    top_error_domains: Dict[str, int] = Field(default_factory=dict)
    top_doctrine_topics: Dict[str, int] = Field(default_factory=dict)
    confidence_distribution: Dict[str, int] = Field(default_factory=dict)
    coverage_gaps: List[str] = Field(default_factory=list)
    drift_alerts: int = 0
    uptime_seconds: float = 0.0


# ---------------------------------------------------------------------------
# Telemetry Collector
# ---------------------------------------------------------------------------

class TelemetryCollector:
    """
    Central telemetry system for the LM21 engine.
    Collects traces, computes latency statistics, detects drift,
    tracks coverage, and writes audit trails.
    """

    def __init__(self, data_dir: Optional[Path] = None) -> None:
        self._data_dir = data_dir or Path("data")
        self._data_dir.mkdir(parents=True, exist_ok=True)
        self._traces: List[QueryTrace] = []
        self._latency_buckets: Dict[str, LatencyBucket] = {
            phase.value: LatencyBucket(phase=phase.value)
            for phase in QueryPhase
        }
        self._error_counts: Dict[str, int] = defaultdict(int)
        self._doctrine_hits: Dict[str, int] = defaultdict(int)
        self._doctrine_misses: Dict[str, int] = defaultdict(int)
        self._confidence_counts: Dict[str, int] = defaultdict(int)
        self._drift_observations: List[DriftObservation] = []
        self._coverage: Dict[str, CoverageEntry] = {}
        self._total_queries: int = 0
        self._total_cache_hits: int = 0
        self._total_errors: int = 0
        self._start_time: float = time.time()
        self._audit_path = self._data_dir / "lm21_audit.jsonl"
        self._telemetry_path = self._data_dir / "lm21_telemetry.jsonl"
        logger.info("TelemetryCollector initialized")

    def start_trace(self, query: str, session_id: str = "") -> QueryTrace:
        """Begin a new query trace."""
        trace = QueryTrace(
            query=query,
            session_id=session_id,
        )
        return trace

    def record_phase_latency(
        self, trace: QueryTrace, phase: QueryPhase, latency_ms: float
    ) -> None:
        """Record latency for a specific processing phase."""
        trace.latencies_ms[phase.value] = round(latency_ms, 3)
        self._latency_buckets[phase.value].record(latency_ms)

    def record_cache_hit(self, trace: QueryTrace, topic: str) -> None:
        """Record a doctrine cache hit."""
        trace.cache_hit = True
        trace.cache_topic = topic
        self._total_cache_hits += 1

    def record_cache_miss(self, trace: QueryTrace) -> None:
        """Record a doctrine cache miss."""
        trace.cache_hit = False

    def record_search_results(
        self, trace: QueryTrace, count: int, top_score: float
    ) -> None:
        """Record vector search results."""
        trace.search_results_count = count
        trace.search_top_score = top_score

    def record_doctrine_trigger(self, trace: QueryTrace, topic: str) -> None:
        """Record that a doctrine topic was triggered."""
        trace.doctrine_topics_triggered.append(topic)
        self._doctrine_hits[topic] = self._doctrine_hits.get(topic, 0) + 1
        if topic not in self._coverage:
            self._coverage[topic] = CoverageEntry(topic=topic)
        entry = self._coverage[topic]
        entry.hit_count += 1
        entry.last_hit = datetime.now(timezone.utc).isoformat()
        entry.coverage_ratio = entry.hit_count / max(
            entry.hit_count + entry.miss_count, 1
        )

    def record_doctrine_miss(self, topic: str) -> None:
        """Record that a doctrine topic was expected but not triggered."""
        self._doctrine_misses[topic] = self._doctrine_misses.get(topic, 0) + 1
        if topic not in self._coverage:
            self._coverage[topic] = CoverageEntry(topic=topic)
        entry = self._coverage[topic]
        entry.miss_count += 1
        entry.last_miss = datetime.now(timezone.utc).isoformat()
        entry.coverage_ratio = entry.hit_count / max(
            entry.hit_count + entry.miss_count, 1
        )

    def record_confidence(
        self, trace: QueryTrace, level: str, score: float
    ) -> None:
        """Record confidence level and score."""
        trace.confidence_level = level
        trace.confidence_score = score
        self._confidence_counts[level] = self._confidence_counts.get(level, 0) + 1

    def record_error(
        self, trace: QueryTrace, error: str, domain: ErrorDomain
    ) -> None:
        """Record an error in the trace."""
        trace.errors.append(error)
        trace.error_domains.append(domain.value)
        self._error_counts[domain.value] = self._error_counts.get(domain.value, 0) + 1
        self._total_errors += 1

    def record_authority_chain(
        self, trace: QueryTrace, authorities: List[str]
    ) -> None:
        """Record the authority chain used in the response."""
        trace.authority_chain = authorities

    def record_fragility(self, trace: QueryTrace, score: float) -> None:
        """Record the fact fragility score."""
        trace.fragility_score = score

    def finalize_trace(self, trace: QueryTrace, response_text: str) -> None:
        """Finalize a trace with response data and write to audit trail."""
        trace.total_latency_ms = sum(trace.latencies_ms.values())
        self._latency_buckets[QueryPhase.TOTAL.value].record(
            trace.total_latency_ms
        )
        trace.response_length = len(response_text)
        trace.determinism_hash = hashlib.sha256(
            response_text.encode("utf-8")
        ).hexdigest()
        self._total_queries += 1
        self._traces.append(trace)
        self._write_audit_entry(trace)
        self._write_telemetry_entry(trace)
        logger.debug(
            f"Trace finalized | id={trace.trace_id[:8]} | "
            f"latency={trace.total_latency_ms:.1f}ms | "
            f"cache_hit={trace.cache_hit} | "
            f"confidence={trace.confidence_level}"
        )

    def observe_drift(
        self,
        topic: str,
        drift_type: str,
        severity: DriftSeverity,
        description: str,
        previous_position: str = "",
        current_position: str = "",
        authority_change: str = "",
        remediation: str = "",
    ) -> DriftObservation:
        """Record a doctrine drift observation."""
        obs = DriftObservation(
            doctrine_topic=topic,
            drift_type=drift_type,
            severity=severity,
            description=description,
            previous_position=previous_position,
            current_position=current_position,
            authority_change=authority_change,
            remediation=remediation,
        )
        self._drift_observations.append(obs)
        logger.warning(
            f"Drift observed | topic={topic} | severity={severity.value} | "
            f"{description}"
        )
        return obs

    def flag_epistemic_gap(self, topic: str, description: str) -> None:
        """Flag an epistemic gap in coverage."""
        if topic not in self._coverage:
            self._coverage[topic] = CoverageEntry(topic=topic)
        entry = self._coverage[topic]
        entry.epistemic_gap = True
        entry.gap_description = description
        logger.warning(f"Epistemic gap flagged | topic={topic} | {description}")

    def get_metrics_snapshot(self) -> MetricsSnapshot:
        """Generate a point-in-time metrics snapshot."""
        uptime = time.time() - self._start_time
        qpm = (self._total_queries / max(uptime, 1)) * 60

        avg_latency = 0.0
        total_bucket = self._latency_buckets.get(QueryPhase.TOTAL.value)
        if total_bucket and total_bucket.count > 0:
            avg_latency = total_bucket.mean_ms

        cache_hit_rate = (
            self._total_cache_hits / max(self._total_queries, 1)
        )
        error_rate = self._total_errors / max(self._total_queries, 1)

        top_errors = dict(
            sorted(
                self._error_counts.items(), key=lambda x: x[1], reverse=True
            )[:10]
        )
        top_doctrines = dict(
            sorted(
                self._doctrine_hits.items(), key=lambda x: x[1], reverse=True
            )[:10]
        )
        coverage_gaps = [
            topic
            for topic, entry in self._coverage.items()
            if entry.epistemic_gap or entry.coverage_ratio < 0.1
        ]

        return MetricsSnapshot(
            total_queries=self._total_queries,
            cache_hit_rate=round(cache_hit_rate, 4),
            error_rate=round(error_rate, 4),
            avg_latency_ms=round(avg_latency, 2),
            queries_per_minute=round(qpm, 2),
            top_error_domains=top_errors,
            top_doctrine_topics=top_doctrines,
            confidence_distribution=dict(self._confidence_counts),
            coverage_gaps=coverage_gaps,
            drift_alerts=len(self._drift_observations),
            uptime_seconds=round(uptime, 1),
        )

    def get_latency_report(self) -> Dict[str, Dict[str, float]]:
        """Return latency statistics for all phases."""
        report: Dict[str, Dict[str, float]] = {}
        for phase, bucket in self._latency_buckets.items():
            if bucket.count > 0:
                report[phase] = {
                    "count": bucket.count,
                    "min_ms": round(bucket.min_ms, 3),
                    "max_ms": round(bucket.max_ms, 3),
                    "mean_ms": round(bucket.mean_ms, 3),
                    "median_ms": round(bucket.median_ms, 3),
                    "p95_ms": round(bucket.p95_ms, 3),
                    "p99_ms": round(bucket.p99_ms, 3),
                }
        return report

    def get_coverage_report(self) -> Dict[str, Dict[str, Any]]:
        """Return coverage report for all tracked doctrine topics."""
        report: Dict[str, Dict[str, Any]] = {}
        for topic, entry in self._coverage.items():
            report[topic] = {
                "hit_count": entry.hit_count,
                "miss_count": entry.miss_count,
                "coverage_ratio": round(entry.coverage_ratio, 4),
                "epistemic_gap": entry.epistemic_gap,
                "gap_description": entry.gap_description,
                "last_hit": entry.last_hit,
                "last_miss": entry.last_miss,
            }
        return report

    def get_drift_report(self) -> List[Dict[str, Any]]:
        """Return all drift observations."""
        return [obs.model_dump() for obs in self._drift_observations]

    def get_recent_traces(self, count: int = 20) -> List[Dict[str, Any]]:
        """Return the most recent query traces."""
        recent = self._traces[-count:]
        return [
            {
                "trace_id": t.trace_id,
                "query": t.query[:100],
                "timestamp": t.timestamp,
                "cache_hit": t.cache_hit,
                "confidence_level": t.confidence_level,
                "total_latency_ms": t.total_latency_ms,
                "errors": t.errors,
                "doctrines_triggered": t.doctrine_topics_triggered,
            }
            for t in reversed(recent)
        ]

    def _write_audit_entry(self, trace: QueryTrace) -> None:
        """Append trace to JSONL audit trail."""
        entry = {
            "trace_id": trace.trace_id,
            "timestamp": trace.timestamp,
            "query": trace.query,
            "cache_hit": trace.cache_hit,
            "cache_topic": trace.cache_topic,
            "confidence_level": trace.confidence_level,
            "confidence_score": trace.confidence_score,
            "total_latency_ms": trace.total_latency_ms,
            "determinism_hash": trace.determinism_hash,
            "errors": trace.errors,
            "doctrines": trace.doctrine_topics_triggered,
            "authority_chain": trace.authority_chain,
            "fragility_score": trace.fragility_score,
        }
        with self._audit_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    def _write_telemetry_entry(self, trace: QueryTrace) -> None:
        """Append telemetry data to JSONL file."""
        entry = {
            "trace_id": trace.trace_id,
            "timestamp": trace.timestamp,
            "latencies_ms": trace.latencies_ms,
            "total_latency_ms": trace.total_latency_ms,
            "cache_hit": trace.cache_hit,
            "search_results_count": trace.search_results_count,
            "response_length": trace.response_length,
            "error_domains": trace.error_domains,
        }
        with self._telemetry_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    def reset_metrics(self) -> None:
        """Reset all counters and metrics (keep drift observations)."""
        self._traces.clear()
        for bucket in self._latency_buckets.values():
            bucket.count = 0
            bucket.total_ms = 0.0
            bucket.min_ms = float("inf")
            bucket.max_ms = 0.0
            bucket.mean_ms = 0.0
            bucket.median_ms = 0.0
            bucket.p95_ms = 0.0
            bucket.p99_ms = 0.0
            bucket.values.clear()
        self._error_counts.clear()
        self._doctrine_hits.clear()
        self._confidence_counts.clear()
        self._total_queries = 0
        self._total_cache_hits = 0
        self._total_errors = 0
        self._start_time = time.time()
        logger.info("Telemetry metrics reset")


# ---------------------------------------------------------------------------
# Compatibility Layer — names expected by engine.py
# ---------------------------------------------------------------------------

class AuditEntry(BaseModel):
    """Audit trail entry for a completed query."""
    timestamp: str = ""
    query_id: str = ""
    query_text: str = ""
    mode: str = ""
    doctrines_triggered: List[str] = Field(default_factory=list)
    confidence: float = 0.0
    determinism_hash: str = ""


# Aliases for names imported by engine.py but not otherwise used
CoverageGap = CoverageEntry
DriftEvent = DriftObservation
MetricSnapshot = MetricsSnapshot


class FederalLandsTelemetry:
    """
    Engine-facing telemetry interface that wraps TelemetryCollector and adds
    the start_query / record_phase / complete_query / log_audit / flush /
    get_stats / get_coverage_map API expected by engine.py.
    """

    def __init__(self, data_dir_or_path: Optional[str] = None) -> None:
        data_dir = Path(data_dir_or_path).parent if data_dir_or_path else None
        self._collector = TelemetryCollector(data_dir=data_dir)
        self._active_traces: Dict[str, QueryTrace] = {}
        self._audit_entries: List[AuditEntry] = []
        self._audit_path = (
            (data_dir or Path("data")) / "lm21_audit_entries.jsonl"
        )
        self._audit_path.parent.mkdir(parents=True, exist_ok=True)

    # -- query lifecycle -----------------------------------------------------

    def start_query(self, analysis_id: str) -> None:
        """Begin tracking a new query by analysis_id."""
        trace = self._collector.start_trace(query=analysis_id, session_id=analysis_id)
        self._active_traces[analysis_id] = trace

    def record_phase(
        self, analysis_id: str, phase: QueryPhase, elapsed_seconds: float
    ) -> None:
        """Record latency for a processing phase (seconds -> ms)."""
        trace = self._active_traces.get(analysis_id)
        if trace:
            self._collector.record_phase_latency(trace, phase, elapsed_seconds * 1000)

    def record_cache_hit(self, analysis_id: str) -> None:
        """Record a doctrine cache hit for the given query."""
        trace = self._active_traces.get(analysis_id)
        if trace:
            self._collector.record_cache_hit(trace, "")

    def record_cache_miss(self, analysis_id: str) -> None:
        """Record a doctrine cache miss for the given query."""
        trace = self._active_traces.get(analysis_id)
        if trace:
            self._collector.record_cache_miss(trace)

    def complete_query(self, analysis_id: str, *, success: bool = True) -> None:
        """Mark a query complete and finalize its trace."""
        trace = self._active_traces.pop(analysis_id, None)
        if trace:
            if not success:
                self._collector.record_error(
                    trace, "query_failed", ErrorDomain.INTERNAL_ERROR
                )
            self._collector.finalize_trace(trace, trace.query)

    def log_audit(self, entry: AuditEntry) -> None:
        """Persist an audit entry to disk."""
        self._audit_entries.append(entry)
        with self._audit_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry.model_dump()) + "\n")

    def flush(self) -> None:
        """Flush any pending data (no-op — writes are immediate)."""
        pass

    # -- reporting -----------------------------------------------------------

    def get_stats(self) -> Dict[str, Any]:
        """Return a stats dict suitable for /health and /metrics endpoints."""
        snapshot = self._collector.get_metrics_snapshot()
        return {
            "total_queries": snapshot.total_queries,
            "cache_hit_rate": snapshot.cache_hit_rate,
            "error_rate": snapshot.error_rate,
            "avg_latency_ms": snapshot.avg_latency_ms,
            "queries_per_minute": snapshot.queries_per_minute,
            "uptime_seconds": snapshot.uptime_seconds,
            "drift_alerts": snapshot.drift_alerts,
            "coverage_gaps": snapshot.coverage_gaps,
            "top_error_domains": snapshot.top_error_domains,
            "top_doctrine_topics": snapshot.top_doctrine_topics,
            "confidence_distribution": snapshot.confidence_distribution,
        }

    def get_coverage_map(self) -> Dict[str, Dict[str, Any]]:
        """Return per-doctrine coverage data."""
        return self._collector.get_coverage_report()
