"""
LM09 Runsheet Generator — Telemetry Module
Engine ID: LM09 | Port: 8509
Full query tracing, latency tracking, error domain classification,
coverage metrics, and performance analytics for run sheet generation.
"""

from __future__ import annotations

import hashlib
import json
import statistics
import threading
import time
import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Optional

from loguru import logger


class ErrorDomain(str, Enum):
    """Classification of error domains for run sheet generation."""
    CHAIN_RECONSTRUCTION = "chain_reconstruction"
    INTEREST_COMPUTATION = "interest_computation"
    LEGAL_DESCRIPTION_PARSE = "legal_description_parse"
    INSTRUMENT_ABSTRACTION = "instrument_abstraction"
    DOCTRINE_CACHE_MISS = "doctrine_cache_miss"
    VECTOR_SEARCH_FAILURE = "vector_search_failure"
    GAP_DETECTION = "gap_detection"
    NRI_CALCULATION = "nri_calculation"
    ACREAGE_CALCULATION = "acreage_calculation"
    RESERVATION_TRACKING = "reservation_tracking"
    PROBATE_CHAIN = "probate_chain"
    INPUT_VALIDATION = "input_validation"
    SERIALIZATION = "serialization"
    TIMEOUT = "timeout"
    UNKNOWN = "unknown"


class QueryPhase(str, Enum):
    """Phases within a single query lifecycle."""
    RECEIVED = "received"
    VALIDATED = "validated"
    DOCTRINE_LOOKUP = "doctrine_lookup"
    SEMANTIC_SEARCH = "semantic_search"
    DEEP_ANALYSIS = "deep_analysis"
    CHAIN_BUILD = "chain_build"
    INTEREST_CALC = "interest_calc"
    GAP_CHECK = "gap_check"
    FORMAT_OUTPUT = "format_output"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class PhaseTimestamp:
    """Records a phase transition with timing."""
    phase: QueryPhase
    entered_at: float
    exited_at: Optional[float] = None
    duration_ms: Optional[float] = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class QueryTrace:
    """Full trace of a single query through the engine."""
    trace_id: str
    query_text: str
    query_hash: str
    session_id: str
    started_at: float
    completed_at: Optional[float] = None
    total_duration_ms: Optional[float] = None
    response_mode: str = "FAST"
    issue_category: str = "UNKNOWN"
    confidence_level: str = "DEFENSIBLE"
    doctrine_hit: bool = False
    doctrine_topic: Optional[str] = None
    vector_fallback: bool = False
    deep_analysis: bool = False
    phases: list[PhaseTimestamp] = field(default_factory=list)
    errors: list[dict[str, Any]] = field(default_factory=list)
    instruments_processed: int = 0
    tracts_analyzed: int = 0
    gaps_detected: int = 0
    determinism_hash: Optional[str] = None
    result_size_bytes: int = 0

    def enter_phase(self, phase: QueryPhase, metadata: Optional[dict[str, Any]] = None) -> None:
        """Record entering a new phase."""
        if self.phases:
            prev = self.phases[-1]
            if prev.exited_at is None:
                prev.exited_at = time.time()
                prev.duration_ms = (prev.exited_at - prev.entered_at) * 1000
        self.phases.append(PhaseTimestamp(
            phase=phase,
            entered_at=time.time(),
            metadata=metadata or {},
        ))

    def complete(self, determinism_hash: Optional[str] = None) -> None:
        """Mark query as completed."""
        self.completed_at = time.time()
        self.total_duration_ms = (self.completed_at - self.started_at) * 1000
        self.determinism_hash = determinism_hash
        if self.phases:
            last = self.phases[-1]
            if last.exited_at is None:
                last.exited_at = self.completed_at
                last.duration_ms = (last.exited_at - last.entered_at) * 1000
        self.enter_phase(QueryPhase.COMPLETED)

    def fail(self, error_domain: ErrorDomain, error_msg: str) -> None:
        """Mark query as failed."""
        self.completed_at = time.time()
        self.total_duration_ms = (self.completed_at - self.started_at) * 1000
        self.errors.append({
            "domain": error_domain.value,
            "message": error_msg,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        self.enter_phase(QueryPhase.FAILED, {"error_domain": error_domain.value})

    def to_dict(self) -> dict[str, Any]:
        """Serialize the trace to a dictionary."""
        return {
            "trace_id": self.trace_id,
            "query_hash": self.query_hash,
            "session_id": self.session_id,
            "started_at": datetime.fromtimestamp(self.started_at, tz=timezone.utc).isoformat(),
            "completed_at": datetime.fromtimestamp(self.completed_at, tz=timezone.utc).isoformat() if self.completed_at else None,
            "total_duration_ms": round(self.total_duration_ms, 2) if self.total_duration_ms else None,
            "response_mode": self.response_mode,
            "issue_category": self.issue_category,
            "confidence_level": self.confidence_level,
            "doctrine_hit": self.doctrine_hit,
            "doctrine_topic": self.doctrine_topic,
            "vector_fallback": self.vector_fallback,
            "deep_analysis": self.deep_analysis,
            "instruments_processed": self.instruments_processed,
            "tracts_analyzed": self.tracts_analyzed,
            "gaps_detected": self.gaps_detected,
            "determinism_hash": self.determinism_hash,
            "result_size_bytes": self.result_size_bytes,
            "phase_count": len(self.phases),
            "phases": [
                {
                    "phase": p.phase.value,
                    "duration_ms": round(p.duration_ms, 2) if p.duration_ms else None,
                    "metadata": p.metadata,
                }
                for p in self.phases
            ],
            "errors": self.errors,
        }


class MetricsCollector:
    """Collects and aggregates engine performance metrics."""

    def __init__(self, engine_id: str = "LM09", audit_log_path: Optional[Path] = None) -> None:
        self.engine_id = engine_id
        self.audit_log_path = audit_log_path or Path("logs/lm09_audit.jsonl")
        self.audit_log_path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._traces: list[QueryTrace] = []
        self._active_traces: dict[str, QueryTrace] = {}
        self._start_time = time.time()
        self._total_queries = 0
        self._total_errors = 0
        self._doctrine_hits = 0
        self._doctrine_misses = 0
        self._vector_fallbacks = 0
        self._deep_analyses = 0
        self._latencies_ms: list[float] = []
        self._errors_by_domain: dict[str, int] = defaultdict(int)
        self._queries_by_category: dict[str, int] = defaultdict(int)
        self._queries_by_mode: dict[str, int] = defaultdict(int)
        self._instruments_total = 0
        self._tracts_total = 0
        self._gaps_total = 0
        self._hourly_counts: dict[str, int] = defaultdict(int)
        logger.info("MetricsCollector initialized for engine {}", engine_id)

    def start_trace(
        self,
        query_text: str,
        session_id: str,
        response_mode: str = "FAST",
        issue_category: str = "UNKNOWN",
    ) -> QueryTrace:
        """Begin tracing a new query."""
        query_hash = hashlib.sha256(query_text.encode()).hexdigest()[:16]
        trace = QueryTrace(
            trace_id=str(uuid.uuid4()),
            query_text=query_text[:500],
            query_hash=query_hash,
            session_id=session_id,
            started_at=time.time(),
            response_mode=response_mode,
            issue_category=issue_category,
        )
        trace.enter_phase(QueryPhase.RECEIVED)
        with self._lock:
            self._active_traces[trace.trace_id] = trace
        logger.debug("Trace started: {} hash={}", trace.trace_id, query_hash)
        return trace

    def complete_trace(self, trace: QueryTrace) -> None:
        """Finalize a trace and record metrics."""
        with self._lock:
            self._active_traces.pop(trace.trace_id, None)
            self._traces.append(trace)
            self._total_queries += 1
            if trace.total_duration_ms is not None:
                self._latencies_ms.append(trace.total_duration_ms)
            if trace.doctrine_hit:
                self._doctrine_hits += 1
            else:
                self._doctrine_misses += 1
            if trace.vector_fallback:
                self._vector_fallbacks += 1
            if trace.deep_analysis:
                self._deep_analyses += 1
            if trace.errors:
                self._total_errors += 1
                for err in trace.errors:
                    self._errors_by_domain[err.get("domain", "unknown")] += 1
            self._queries_by_category[trace.issue_category] += 1
            self._queries_by_mode[trace.response_mode] += 1
            self._instruments_total += trace.instruments_processed
            self._tracts_total += trace.tracts_analyzed
            self._gaps_total += trace.gaps_detected
            hour_key = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H")
            self._hourly_counts[hour_key] += 1
        self._write_audit_log(trace)
        logger.debug(
            "Trace completed: {} duration={}ms doctrine_hit={}",
            trace.trace_id,
            round(trace.total_duration_ms or 0, 2),
            trace.doctrine_hit,
        )

    def _write_audit_log(self, trace: QueryTrace) -> None:
        """Append trace to JSONL audit log."""
        try:
            with self.audit_log_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(trace.to_dict(), default=str) + "\n")
        except OSError as exc:
            logger.error("Failed to write audit log: {}", exc)

    def get_latency_stats(self) -> dict[str, float]:
        """Calculate latency statistics."""
        with self._lock:
            if not self._latencies_ms:
                return {"count": 0, "mean_ms": 0.0, "median_ms": 0.0, "p95_ms": 0.0, "p99_ms": 0.0, "max_ms": 0.0, "min_ms": 0.0}
            sorted_lats = sorted(self._latencies_ms)
            n = len(sorted_lats)
            p95_idx = min(int(n * 0.95), n - 1)
            p99_idx = min(int(n * 0.99), n - 1)
            return {
                "count": n,
                "mean_ms": round(statistics.mean(sorted_lats), 2),
                "median_ms": round(statistics.median(sorted_lats), 2),
                "p95_ms": round(sorted_lats[p95_idx], 2),
                "p99_ms": round(sorted_lats[p99_idx], 2),
                "max_ms": round(max(sorted_lats), 2),
                "min_ms": round(min(sorted_lats), 2),
            }

    def get_hit_rates(self) -> dict[str, Any]:
        """Get doctrine cache hit rates."""
        with self._lock:
            total = self._doctrine_hits + self._doctrine_misses
            return {
                "total_lookups": total,
                "hits": self._doctrine_hits,
                "misses": self._doctrine_misses,
                "hit_rate": round(self._doctrine_hits / total, 4) if total > 0 else 0.0,
                "vector_fallbacks": self._vector_fallbacks,
                "deep_analyses": self._deep_analyses,
            }

    def get_error_rates(self) -> dict[str, Any]:
        """Get error rates by domain."""
        with self._lock:
            return {
                "total_queries": self._total_queries,
                "total_errors": self._total_errors,
                "error_rate": round(self._total_errors / self._total_queries, 4) if self._total_queries > 0 else 0.0,
                "errors_by_domain": dict(self._errors_by_domain),
            }

    def get_queries_per_hour(self) -> dict[str, int]:
        """Get hourly query counts."""
        with self._lock:
            return dict(self._hourly_counts)

    def get_category_distribution(self) -> dict[str, int]:
        """Get query distribution by issue category."""
        with self._lock:
            return dict(self._queries_by_category)

    def get_mode_distribution(self) -> dict[str, int]:
        """Get query distribution by response mode."""
        with self._lock:
            return dict(self._queries_by_mode)

    def get_domain_metrics(self) -> dict[str, Any]:
        """Get run sheet domain-specific metrics."""
        with self._lock:
            return {
                "total_instruments_processed": self._instruments_total,
                "total_tracts_analyzed": self._tracts_total,
                "total_gaps_detected": self._gaps_total,
                "avg_instruments_per_query": round(self._instruments_total / self._total_queries, 2) if self._total_queries > 0 else 0.0,
                "avg_tracts_per_query": round(self._tracts_total / self._total_queries, 2) if self._total_queries > 0 else 0.0,
                "gap_detection_rate": round(self._gaps_total / self._total_queries, 4) if self._total_queries > 0 else 0.0,
            }

    def get_uptime_seconds(self) -> float:
        """Get engine uptime in seconds."""
        return round(time.time() - self._start_time, 2)

    def get_comprehensive_metrics(self) -> dict[str, Any]:
        """Return all metrics in a single payload."""
        return {
            "engine_id": self.engine_id,
            "uptime_seconds": self.get_uptime_seconds(),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "latency": self.get_latency_stats(),
            "hit_rates": self.get_hit_rates(),
            "error_rates": self.get_error_rates(),
            "queries_per_hour": self.get_queries_per_hour(),
            "category_distribution": self.get_category_distribution(),
            "mode_distribution": self.get_mode_distribution(),
            "domain_metrics": self.get_domain_metrics(),
            "active_traces": len(self._active_traces),
            "total_completed_traces": len(self._traces),
        }

    def reset(self) -> None:
        """Reset all collected metrics."""
        with self._lock:
            self._traces.clear()
            self._active_traces.clear()
            self._total_queries = 0
            self._total_errors = 0
            self._doctrine_hits = 0
            self._doctrine_misses = 0
            self._vector_fallbacks = 0
            self._deep_analyses = 0
            self._latencies_ms.clear()
            self._errors_by_domain.clear()
            self._queries_by_category.clear()
            self._queries_by_mode.clear()
            self._instruments_total = 0
            self._tracts_total = 0
            self._gaps_total = 0
            self._hourly_counts.clear()
            self._start_time = time.time()
        logger.info("MetricsCollector reset for engine {}", self.engine_id)


class DriftWatcher:
    """Monitors doctrine drift over time by tracking response consistency."""

    def __init__(self, window_size: int = 100) -> None:
        self.window_size = window_size
        self._lock = threading.Lock()
        self._response_hashes: dict[str, list[str]] = defaultdict(list)
        self._drift_alerts: list[dict[str, Any]] = []
        logger.info("DriftWatcher initialized with window_size={}", window_size)

    def record_response(self, doctrine_topic: str, determinism_hash: str) -> Optional[dict[str, Any]]:
        """Record a response hash and check for drift."""
        with self._lock:
            hashes = self._response_hashes[doctrine_topic]
            hashes.append(determinism_hash)
            if len(hashes) > self.window_size:
                hashes.pop(0)
            if len(hashes) >= 10:
                unique_count = len(set(hashes[-10:]))
                drift_ratio = unique_count / 10
                if drift_ratio > 0.3:
                    alert = {
                        "doctrine_topic": doctrine_topic,
                        "drift_ratio": round(drift_ratio, 4),
                        "unique_hashes_in_window": unique_count,
                        "window_size": 10,
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "severity": "HIGH" if drift_ratio > 0.6 else "MEDIUM",
                    }
                    self._drift_alerts.append(alert)
                    logger.warning("Doctrine drift detected: topic={} ratio={}", doctrine_topic, drift_ratio)
                    return alert
        return None

    def get_drift_report(self) -> dict[str, Any]:
        """Generate a drift analysis report."""
        with self._lock:
            topic_stats = {}
            for topic, hashes in self._response_hashes.items():
                unique = len(set(hashes))
                total = len(hashes)
                topic_stats[topic] = {
                    "total_responses": total,
                    "unique_hashes": unique,
                    "consistency_ratio": round(1.0 - (unique / total), 4) if total > 0 else 1.0,
                }
            return {
                "total_topics_tracked": len(self._response_hashes),
                "total_drift_alerts": len(self._drift_alerts),
                "recent_alerts": self._drift_alerts[-10:],
                "topic_consistency": topic_stats,
            }


class CoverageMap:
    """Tracks which doctrines have been triggered and which have gaps."""

    def __init__(self, all_doctrine_topics: list[str]) -> None:
        self._lock = threading.Lock()
        self._all_topics = set(all_doctrine_topics)
        self._triggered: dict[str, int] = defaultdict(int)
        self._missed_queries: list[dict[str, Any]] = []
        logger.info("CoverageMap initialized with {} doctrine topics", len(all_doctrine_topics))

    def record_hit(self, topic: str) -> None:
        """Record that a doctrine topic was triggered."""
        with self._lock:
            self._triggered[topic] += 1

    def record_miss(self, query_text: str, attempted_category: str) -> None:
        """Record a query that failed to match any doctrine."""
        with self._lock:
            self._missed_queries.append({
                "query_hash": hashlib.sha256(query_text.encode()).hexdigest()[:16],
                "attempted_category": attempted_category,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            if len(self._missed_queries) > 500:
                self._missed_queries = self._missed_queries[-250:]

    def get_coverage_report(self) -> dict[str, Any]:
        """Generate a coverage analysis report."""
        with self._lock:
            triggered_topics = set(self._triggered.keys())
            untriggered = self._all_topics - triggered_topics
            total = len(self._all_topics)
            covered = len(triggered_topics)
            return {
                "total_doctrines": total,
                "triggered_doctrines": covered,
                "untriggered_doctrines": len(untriggered),
                "coverage_ratio": round(covered / total, 4) if total > 0 else 0.0,
                "untriggered_topics": sorted(untriggered),
                "top_triggered": sorted(self._triggered.items(), key=lambda x: x[1], reverse=True)[:15],
                "total_misses": len(self._missed_queries),
                "recent_misses": self._missed_queries[-10:],
                "epistemic_gaps": sorted(untriggered)[:20],
            }


class TelemetryManager:
    """Central telemetry coordinator for the LM09 engine."""

    def __init__(
        self,
        engine_id: str = "LM09",
        doctrine_topics: Optional[list[str]] = None,
        audit_log_path: Optional[Path] = None,
    ) -> None:
        self.engine_id = engine_id
        self.metrics = MetricsCollector(engine_id=engine_id, audit_log_path=audit_log_path)
        self.drift_watcher = DriftWatcher(window_size=100)
        self.coverage_map = CoverageMap(all_doctrine_topics=doctrine_topics or [])
        logger.info("TelemetryManager initialized for engine {} with {} doctrine topics", engine_id, len(doctrine_topics or []))

    def start_query(
        self,
        query_text: str,
        session_id: str,
        response_mode: str = "FAST",
        issue_category: str = "UNKNOWN",
    ) -> QueryTrace:
        """Begin telemetry for a new query."""
        return self.metrics.start_trace(
            query_text=query_text,
            session_id=session_id,
            response_mode=response_mode,
            issue_category=issue_category,
        )

    def end_query(
        self,
        trace: QueryTrace,
        doctrine_topic: Optional[str] = None,
        determinism_hash: Optional[str] = None,
    ) -> None:
        """Complete telemetry for a query and run drift/coverage checks."""
        self.metrics.complete_trace(trace)
        if doctrine_topic and determinism_hash:
            self.drift_watcher.record_response(doctrine_topic, determinism_hash)
            self.coverage_map.record_hit(doctrine_topic)
        elif not trace.doctrine_hit:
            self.coverage_map.record_miss(trace.query_text, trace.issue_category)

    def get_full_telemetry(self) -> dict[str, Any]:
        """Return complete telemetry snapshot."""
        return {
            "engine_id": self.engine_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "metrics": self.metrics.get_comprehensive_metrics(),
            "drift_report": self.drift_watcher.get_drift_report(),
            "coverage_report": self.coverage_map.get_coverage_report(),
        }
