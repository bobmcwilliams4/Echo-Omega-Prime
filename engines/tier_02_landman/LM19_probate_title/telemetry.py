"""
LM19 Probate Title Engine — Telemetry
======================================
Query tracing, metrics collection, and performance monitoring.
Full audit trail for probate title opinions.
"""

from __future__ import annotations

import json
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Optional

from loguru import logger


class QueryPhase(str, Enum):
    """Query execution phases."""
    NORMALIZATION = "NORMALIZATION"
    CACHE_LOOKUP = "CACHE_LOOKUP"
    VECTOR_SEARCH = "VECTOR_SEARCH"
    CLOUD_RETRIEVAL = "CLOUD_RETRIEVAL"
    DOCTRINE_SELECTION = "DOCTRINE_SELECTION"
    RESPONSE_GENERATION = "RESPONSE_GENERATION"
    TOTAL = "TOTAL"


class ErrorDomain(str, Enum):
    """Error domains for categorization."""
    INPUT_VALIDATION = "INPUT_VALIDATION"
    CACHE_MISS = "CACHE_MISS"
    SEARCH_FAILURE = "SEARCH_FAILURE"
    CLOUD_UNAVAILABLE = "CLOUD_UNAVAILABLE"
    AUTHORITY_CONFLICT = "AUTHORITY_CONFLICT"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"
    AMBIGUOUS_QUERY = "AMBIGUOUS_QUERY"
    SYSTEM_ERROR = "SYSTEM_ERROR"


@dataclass
class QueryTrace:
    """Trace of a single query execution."""
    query_id: str
    timestamp: str
    query_text: str
    mode: str
    zone: str
    phase_timings: dict[str, float] = field(default_factory=dict)
    doctrines_triggered: list[str] = field(default_factory=list)
    cache_hit: bool = False
    vector_search_used: bool = False
    cloud_retrieval_used: bool = False
    confidence_tier: str = ""
    response_length: int = 0
    error_domain: Optional[str] = None
    error_message: Optional[str] = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert trace to dictionary."""
        return {
            "query_id": self.query_id,
            "timestamp": self.timestamp,
            "query_text": self.query_text,
            "mode": self.mode,
            "zone": self.zone,
            "phase_timings": self.phase_timings,
            "doctrines_triggered": self.doctrines_triggered,
            "cache_hit": self.cache_hit,
            "vector_search_used": self.vector_search_used,
            "cloud_retrieval_used": self.cloud_retrieval_used,
            "confidence_tier": self.confidence_tier,
            "response_length": self.response_length,
            "error_domain": self.error_domain,
            "error_message": self.error_message,
            "metadata": self.metadata,
        }


class TelemetryCollector:
    """Telemetry collector for probate engine."""

    def __init__(self, audit_log_path: Optional[Path] = None) -> None:
        """
        Initialize telemetry collector.

        Args:
            audit_log_path: Path to JSONL audit log file
        """
        self.audit_log_path = audit_log_path
        self.traces: list[QueryTrace] = []
        self.metrics: dict[str, Any] = {
            "total_queries": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "vector_searches": 0,
            "cloud_retrievals": 0,
            "errors": 0,
            "error_by_domain": defaultdict(int),
            "avg_latency_ms": 0.0,
            "doctrine_hit_counts": defaultdict(int),
            "queries_by_mode": defaultdict(int),
            "queries_by_zone": defaultdict(int),
            "confidence_distribution": defaultdict(int),
        }
        self.start_time = time.time()

    def start_trace(self, query_id: str, query_text: str, mode: str, zone: str) -> QueryTrace:
        """
        Start a new query trace.

        Args:
            query_id: Unique query ID
            query_text: Query text
            mode: Response mode
            zone: Analysis zone

        Returns:
            QueryTrace object
        """
        trace = QueryTrace(
            query_id=query_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            query_text=query_text,
            mode=mode,
            zone=zone
        )
        return trace

    def record_phase(self, trace: QueryTrace, phase: QueryPhase, duration_ms: float) -> None:
        """
        Record phase timing.

        Args:
            trace: QueryTrace object
            phase: Query phase
            duration_ms: Duration in milliseconds
        """
        trace.phase_timings[phase.value] = duration_ms

    def record_doctrine_trigger(self, trace: QueryTrace, doctrine_topic: str) -> None:
        """
        Record doctrine triggered.

        Args:
            trace: QueryTrace object
            doctrine_topic: Doctrine topic
        """
        if doctrine_topic not in trace.doctrines_triggered:
            trace.doctrines_triggered.append(doctrine_topic)
            self.metrics["doctrine_hit_counts"][doctrine_topic] += 1

    def record_cache_hit(self, trace: QueryTrace, hit: bool) -> None:
        """
        Record cache hit/miss.

        Args:
            trace: QueryTrace object
            hit: True if cache hit, False if miss
        """
        trace.cache_hit = hit
        if hit:
            self.metrics["cache_hits"] += 1
        else:
            self.metrics["cache_misses"] += 1

    def record_vector_search(self, trace: QueryTrace) -> None:
        """
        Record vector search usage.

        Args:
            trace: QueryTrace object
        """
        trace.vector_search_used = True
        self.metrics["vector_searches"] += 1

    def record_cloud_retrieval(self, trace: QueryTrace) -> None:
        """
        Record cloud retrieval usage.

        Args:
            trace: QueryTrace object
        """
        trace.cloud_retrieval_used = True
        self.metrics["cloud_retrievals"] += 1

    def record_error(self, trace: QueryTrace, error_domain: ErrorDomain, error_message: str) -> None:
        """
        Record error.

        Args:
            trace: QueryTrace object
            error_domain: Error domain
            error_message: Error message
        """
        trace.error_domain = error_domain.value
        trace.error_message = error_message
        self.metrics["errors"] += 1
        self.metrics["error_by_domain"][error_domain.value] += 1

    def complete_trace(self, trace: QueryTrace, confidence_tier: str, response_length: int) -> None:
        """
        Complete trace and persist to audit log.

        Args:
            trace: QueryTrace object
            confidence_tier: Confidence tier
            response_length: Response length in characters
        """
        trace.confidence_tier = confidence_tier
        trace.response_length = response_length

        # Update metrics
        self.metrics["total_queries"] += 1
        self.metrics["queries_by_mode"][trace.mode] += 1
        self.metrics["queries_by_zone"][trace.zone] += 1
        self.metrics["confidence_distribution"][confidence_tier] += 1

        # Calculate average latency
        total_latency = trace.phase_timings.get(QueryPhase.TOTAL.value, 0)
        total_queries = self.metrics["total_queries"]
        current_avg = self.metrics["avg_latency_ms"]
        self.metrics["avg_latency_ms"] = ((current_avg * (total_queries - 1)) + total_latency) / total_queries

        # Add to traces
        self.traces.append(trace)

        # Persist to audit log
        if self.audit_log_path:
            self._append_audit_log(trace)

        logger.debug(
            f"Query trace completed: {trace.query_id} | "
            f"Latency: {total_latency:.1f}ms | "
            f"Doctrines: {len(trace.doctrines_triggered)} | "
            f"Confidence: {confidence_tier}"
        )

    def _append_audit_log(self, trace: QueryTrace) -> None:
        """
        Append trace to JSONL audit log.

        Args:
            trace: QueryTrace object
        """
        try:
            with open(self.audit_log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(trace.to_dict()) + "\n")
        except Exception as e:
            logger.error(f"Failed to write audit log: {e}")

    def get_metrics(self) -> dict[str, Any]:
        """
        Get current metrics.

        Returns:
            Metrics dictionary
        """
        uptime_seconds = time.time() - self.start_time
        return {
            **self.metrics,
            "uptime_seconds": uptime_seconds,
            "uptime_hours": uptime_seconds / 3600,
            "queries_per_hour": (self.metrics["total_queries"] / uptime_seconds * 3600) if uptime_seconds > 0 else 0,
            "cache_hit_rate": (self.metrics["cache_hits"] / max(1, self.metrics["total_queries"])),
            "error_rate": (self.metrics["errors"] / max(1, self.metrics["total_queries"])),
        }

    def get_doctrine_coverage(self) -> dict[str, Any]:
        """
        Get doctrine coverage statistics.

        Returns:
            Doctrine coverage dictionary
        """
        total_doctrines_available = len(self.metrics["doctrine_hit_counts"])
        total_doctrines_triggered = sum(1 for count in self.metrics["doctrine_hit_counts"].values() if count > 0)

        # Top triggered doctrines
        top_doctrines = sorted(
            self.metrics["doctrine_hit_counts"].items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]

        return {
            "total_doctrines_available": total_doctrines_available,
            "total_doctrines_triggered": total_doctrines_triggered,
            "coverage_percentage": (total_doctrines_triggered / max(1, total_doctrines_available) * 100),
            "top_triggered_doctrines": [{"topic": topic, "count": count} for topic, count in top_doctrines],
        }

    def get_recent_traces(self, limit: int = 10) -> list[dict[str, Any]]:
        """
        Get recent query traces.

        Args:
            limit: Number of traces to return

        Returns:
            List of trace dictionaries
        """
        return [trace.to_dict() for trace in self.traces[-limit:]]

    def reset_metrics(self) -> None:
        """Reset all metrics."""
        self.metrics = {
            "total_queries": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "vector_searches": 0,
            "cloud_retrievals": 0,
            "errors": 0,
            "error_by_domain": defaultdict(int),
            "avg_latency_ms": 0.0,
            "doctrine_hit_counts": defaultdict(int),
            "queries_by_mode": defaultdict(int),
            "queries_by_zone": defaultdict(int),
            "confidence_distribution": defaultdict(int),
        }
        self.traces = []
        self.start_time = time.time()
        logger.info("Telemetry metrics reset")


# Global telemetry collector
_TELEMETRY_COLLECTOR: Optional[TelemetryCollector] = None


def get_telemetry_collector() -> TelemetryCollector:
    """Get global telemetry collector instance."""
    global _TELEMETRY_COLLECTOR
    if _TELEMETRY_COLLECTOR is None:
        # Default audit log path
        audit_log_path = Path(__file__).parent / "logs" / "audit_trail.jsonl"
        audit_log_path.parent.mkdir(parents=True, exist_ok=True)
        _TELEMETRY_COLLECTOR = TelemetryCollector(audit_log_path=audit_log_path)
    return _TELEMETRY_COLLECTOR
