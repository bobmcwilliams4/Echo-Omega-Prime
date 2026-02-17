"""
LM18 Title Insurance Engine — Telemetry
=======================================
Query tracing, performance metrics, and observability for title insurance engine.

Engine: LM18 | Port: 8518 | Domain: title_insurance
Version: 1.0.0 | TIE Gold Standard Component 8
"""

from __future__ import annotations

import json
import time
import uuid
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Optional

from loguru import logger


# ===================================================================
# Enums
# ===================================================================

class QueryPhase(str, Enum):
    """Query execution phases."""
    RECEIVED = "RECEIVED"
    NORMALIZED = "NORMALIZED"
    CACHE_LOOKUP = "CACHE_LOOKUP"
    VECTOR_SEARCH = "VECTOR_SEARCH"
    DEEP_ANALYSIS = "DEEP_ANALYSIS"
    CLOUD_RETRIEVAL = "CLOUD_RETRIEVAL"
    RESPONSE_BUILT = "RESPONSE_BUILT"
    COMPLETED = "COMPLETED"


class ErrorDomain(str, Enum):
    """Error domain categories."""
    NORMALIZATION = "NORMALIZATION"
    CACHE_MISS = "CACHE_MISS"
    VECTOR_SEARCH = "VECTOR_SEARCH"
    CLOUD_UNAVAILABLE = "CLOUD_UNAVAILABLE"
    INVALID_INPUT = "INVALID_INPUT"
    DOCTRINE_NOT_FOUND = "DOCTRINE_NOT_FOUND"
    AUTHORITY_CONFLICT = "AUTHORITY_CONFLICT"
    COVERAGE_GAP = "COVERAGE_GAP"
    RATE_CALCULATION = "RATE_CALCULATION"


# ===================================================================
# Data Classes
# ===================================================================

@dataclass
class PhaseMetric:
    """Metrics for a single query phase."""
    phase: QueryPhase
    start_time: float
    end_time: float
    duration_ms: float
    success: bool
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class QueryTrace:
    """Complete trace of a query execution."""
    trace_id: str
    query: str
    mode: str
    zone: str
    start_time: float
    end_time: Optional[float] = None
    total_duration_ms: Optional[float] = None
    phases: list[PhaseMetric] = field(default_factory=list)
    doctrines_triggered: list[str] = field(default_factory=list)
    cache_hit: bool = False
    vector_search_used: bool = False
    cloud_retrieval_used: bool = False
    error_domain: Optional[ErrorDomain] = None
    error_message: Optional[str] = None
    client_id: str = ""
    response_tokens: int = 0
    confidence_tier: str = ""

    def add_phase(self, phase: QueryPhase, duration_ms: float, success: bool = True, metadata: Optional[dict[str, Any]] = None) -> None:
        """Add phase metric to trace."""
        now = time.time()
        phase_metric = PhaseMetric(
            phase=phase,
            start_time=now - (duration_ms / 1000),
            end_time=now,
            duration_ms=duration_ms,
            success=success,
            metadata=metadata or {}
        )
        self.phases.append(phase_metric)

    def complete(self) -> None:
        """Mark trace as completed."""
        self.end_time = time.time()
        self.total_duration_ms = (self.end_time - self.start_time) * 1000

    def to_dict(self) -> dict[str, Any]:
        """Convert trace to dictionary."""
        return {
            "trace_id": self.trace_id,
            "query": self.query,
            "mode": self.mode,
            "zone": self.zone,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "total_duration_ms": self.total_duration_ms,
            "phases": [asdict(p) for p in self.phases],
            "doctrines_triggered": self.doctrines_triggered,
            "cache_hit": self.cache_hit,
            "vector_search_used": self.vector_search_used,
            "cloud_retrieval_used": self.cloud_retrieval_used,
            "error_domain": self.error_domain.value if self.error_domain else None,
            "error_message": self.error_message,
            "client_id": self.client_id,
            "response_tokens": self.response_tokens,
            "confidence_tier": self.confidence_tier,
        }


@dataclass
class EngineMetrics:
    """Aggregate engine performance metrics."""
    total_queries: int = 0
    successful_queries: int = 0
    failed_queries: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    vector_searches: int = 0
    cloud_retrievals: int = 0
    total_duration_ms: float = 0.0
    avg_duration_ms: float = 0.0
    min_duration_ms: float = float('inf')
    max_duration_ms: float = 0.0
    errors_by_domain: dict[str, int] = field(default_factory=lambda: defaultdict(int))
    queries_by_mode: dict[str, int] = field(default_factory=lambda: defaultdict(int))
    queries_by_zone: dict[str, int] = field(default_factory=lambda: defaultdict(int))
    doctrines_triggered_count: dict[str, int] = field(default_factory=lambda: defaultdict(int))

    def update_from_trace(self, trace: QueryTrace) -> None:
        """Update metrics from a completed trace."""
        self.total_queries += 1

        if trace.error_domain:
            self.failed_queries += 1
            self.errors_by_domain[trace.error_domain.value] += 1
        else:
            self.successful_queries += 1

        if trace.cache_hit:
            self.cache_hits += 1
        else:
            self.cache_misses += 1

        if trace.vector_search_used:
            self.vector_searches += 1

        if trace.cloud_retrieval_used:
            self.cloud_retrievals += 1

        if trace.total_duration_ms:
            self.total_duration_ms += trace.total_duration_ms
            self.avg_duration_ms = self.total_duration_ms / self.total_queries
            self.min_duration_ms = min(self.min_duration_ms, trace.total_duration_ms)
            self.max_duration_ms = max(self.max_duration_ms, trace.total_duration_ms)

        self.queries_by_mode[trace.mode] += 1
        self.queries_by_zone[trace.zone] += 1

        for doctrine in trace.doctrines_triggered:
            self.doctrines_triggered_count[doctrine] += 1

    def get_cache_hit_rate(self) -> float:
        """Calculate cache hit rate."""
        total = self.cache_hits + self.cache_misses
        return (self.cache_hits / total * 100) if total > 0 else 0.0

    def get_success_rate(self) -> float:
        """Calculate query success rate."""
        return (self.successful_queries / self.total_queries * 100) if self.total_queries > 0 else 0.0

    def to_dict(self) -> dict[str, Any]:
        """Convert metrics to dictionary."""
        return {
            "total_queries": self.total_queries,
            "successful_queries": self.successful_queries,
            "failed_queries": self.failed_queries,
            "success_rate": round(self.get_success_rate(), 2),
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "cache_hit_rate": round(self.get_cache_hit_rate(), 2),
            "vector_searches": self.vector_searches,
            "cloud_retrievals": self.cloud_retrievals,
            "total_duration_ms": round(self.total_duration_ms, 2),
            "avg_duration_ms": round(self.avg_duration_ms, 2),
            "min_duration_ms": round(self.min_duration_ms, 2),
            "max_duration_ms": round(self.max_duration_ms, 2),
            "errors_by_domain": dict(self.errors_by_domain),
            "queries_by_mode": dict(self.queries_by_mode),
            "queries_by_zone": dict(self.queries_by_zone),
            "top_doctrines": dict(sorted(self.doctrines_triggered_count.items(), key=lambda x: x[1], reverse=True)[:10]),
        }


# ===================================================================
# Telemetry Collector
# ===================================================================

class TelemetryCollector:
    """Centralized telemetry collection for title insurance engine."""

    def __init__(self, engine_id: str = "LM18", flush_interval_seconds: int = 60, max_buffer_size: int = 10000):
        """
        Initialize telemetry collector.

        Args:
            engine_id: Engine identifier
            flush_interval_seconds: How often to flush traces to disk
            max_buffer_size: Max traces to buffer before forcing flush
        """
        self.engine_id = engine_id
        self.flush_interval_seconds = flush_interval_seconds
        self.max_buffer_size = max_buffer_size

        self.traces: list[QueryTrace] = []
        self.metrics = EngineMetrics()
        self.last_flush_time = time.time()

        logger.info(f"TelemetryCollector initialized: engine={engine_id}, flush_interval={flush_interval_seconds}s")

    def start_trace(self, query: str, mode: str, zone: str, client_id: str = "") -> QueryTrace:
        """
        Start a new query trace.

        Args:
            query: Query text
            mode: Response mode (FAST, DEFENSE, MEMO)
            zone: Analysis zone (PLANNING, REPORTING, AUDIT)
            client_id: Optional client identifier

        Returns:
            QueryTrace object to track this query
        """
        trace = QueryTrace(
            trace_id=str(uuid.uuid4()),
            query=query,
            mode=mode,
            zone=zone,
            start_time=time.time(),
            client_id=client_id
        )

        trace.add_phase(QueryPhase.RECEIVED, 0.0)
        logger.debug(f"Started trace {trace.trace_id} for query: {query[:50]}")
        return trace

    def complete_trace(self, trace: QueryTrace) -> None:
        """
        Complete a trace and update metrics.

        Args:
            trace: Completed QueryTrace
        """
        trace.complete()
        trace.add_phase(QueryPhase.COMPLETED, 0.0)

        self.traces.append(trace)
        self.metrics.update_from_trace(trace)

        logger.debug(f"Completed trace {trace.trace_id}: {trace.total_duration_ms:.2f}ms, success={trace.error_domain is None}")

        # Auto-flush if buffer full or interval exceeded
        if len(self.traces) >= self.max_buffer_size or (time.time() - self.last_flush_time) >= self.flush_interval_seconds:
            self.flush()

    def record_error(self, trace: QueryTrace, error_domain: ErrorDomain, error_message: str) -> None:
        """
        Record error in trace.

        Args:
            trace: QueryTrace to update
            error_domain: Error domain category
            error_message: Error description
        """
        trace.error_domain = error_domain
        trace.error_message = error_message
        logger.warning(f"Error in trace {trace.trace_id}: {error_domain.value} - {error_message}")

    def flush(self, output_path: Optional[Path] = None) -> None:
        """
        Flush traces to disk.

        Args:
            output_path: Optional custom output path
        """
        if not self.traces:
            return

        if output_path is None:
            output_path = Path(__file__).parent / "logs" / "traces.jsonl"

        output_path.parent.mkdir(parents=True, exist_ok=True)

        with output_path.open("a", encoding="utf-8") as f:
            for trace in self.traces:
                f.write(json.dumps(trace.to_dict()) + "\n")

        logger.info(f"Flushed {len(self.traces)} traces to {output_path}")
        self.traces.clear()
        self.last_flush_time = time.time()

    def get_metrics(self) -> dict[str, Any]:
        """Get current engine metrics."""
        return self.metrics.to_dict()

    def reset_metrics(self) -> None:
        """Reset metrics to zero."""
        self.metrics = EngineMetrics()
        logger.info("Metrics reset")

    def get_recent_traces(self, count: int = 10) -> list[dict[str, Any]]:
        """Get most recent traces."""
        return [trace.to_dict() for trace in self.traces[-count:]]

    def get_error_summary(self) -> dict[str, Any]:
        """Get summary of errors."""
        return {
            "total_errors": self.metrics.failed_queries,
            "error_rate": round((self.metrics.failed_queries / self.metrics.total_queries * 100) if self.metrics.total_queries > 0 else 0.0, 2),
            "errors_by_domain": dict(self.metrics.errors_by_domain),
        }


# ===================================================================
# Global Telemetry Collector
# ===================================================================

_TELEMETRY_COLLECTOR: Optional[TelemetryCollector] = None


def get_telemetry_collector(engine_id: str = "LM18") -> TelemetryCollector:
    """Get global telemetry collector instance (singleton)."""
    global _TELEMETRY_COLLECTOR
    if _TELEMETRY_COLLECTOR is None:
        _TELEMETRY_COLLECTOR = TelemetryCollector(engine_id=engine_id)
    return _TELEMETRY_COLLECTOR


def start_trace(query: str, mode: str, zone: str, client_id: str = "") -> QueryTrace:
    """Start a new query trace using global collector."""
    collector = get_telemetry_collector()
    return collector.start_trace(query, mode, zone, client_id)


def complete_trace(trace: QueryTrace) -> None:
    """Complete a trace using global collector."""
    collector = get_telemetry_collector()
    collector.complete_trace(trace)


def record_error(trace: QueryTrace, error_domain: ErrorDomain, error_message: str) -> None:
    """Record error in trace using global collector."""
    collector = get_telemetry_collector()
    collector.record_error(trace, error_domain, error_message)
