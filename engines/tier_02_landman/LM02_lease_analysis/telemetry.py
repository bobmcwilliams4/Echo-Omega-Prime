"""
LM02 Lease Analysis Engine - Telemetry Module
Performance tracking, query metrics, audit trail, and operational monitoring.

Provides:
    - Query timing and throughput metrics
    - Lease analysis operation auditing
    - Error tracking by domain and severity
    - Search performance analytics
    - Doctrine cache hit/miss tracking
    - NRI calculation audit trail
    - Royalty computation verification logging
    - Expiration alert delivery tracking
    - Engine health monitoring

Author: ECHO OMEGA PRIME
Authority: 11.0 SOVEREIGN
Version: 1.0.0
"""

from __future__ import annotations

import hashlib
import json
import statistics
import time
import uuid
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Deque, Dict, List, Optional, Tuple

from loguru import logger

# ============================================================================
# TELEMETRY ENUMERATIONS
# ============================================================================


class QueryType(str, Enum):
    """Types of queries processed by the engine."""
    LEASE_ANALYSIS = "lease_analysis"
    TERM_ANALYSIS = "term_analysis"
    ROYALTY_CALCULATION = "royalty_calculation"
    NRI_CALCULATION = "nri_calculation"
    PUGH_ANALYSIS = "pugh_analysis"
    EXPIRATION_CHECK = "expiration_check"
    LEASE_COMPARISON = "lease_comparison"
    LEASE_SEARCH = "lease_search"
    DOCTRINE_LOOKUP = "doctrine_lookup"
    SEMANTIC_NORMALIZE = "semantic_normalize"
    LEGAL_DESC_PARSE = "legal_desc_parse"
    DEPTH_ANALYSIS = "depth_analysis"
    CLAUSE_IDENTIFICATION = "clause_identification"
    HEALTH_CHECK = "health_check"
    BATCH_ANALYSIS = "batch_analysis"


class ResponseLayer(str, Enum):
    """Response generation layer."""
    DOCTRINE_CACHE = "doctrine_cache"
    SEMANTIC_RETRIEVAL = "semantic_retrieval"
    DEEP_ANALYSIS = "deep_analysis"
    SEARCH_INDEX = "search_index"
    EXTERNAL_API = "external_api"
    COMPUTED = "computed"


class ErrorDomain(str, Enum):
    """Domain classification for errors."""
    PARSING = "parsing"
    CALCULATION = "calculation"
    SEARCH = "search"
    DOCTRINE = "doctrine"
    VALIDATION = "validation"
    INTEGRATION = "integration"
    SERIALIZATION = "serialization"
    CONFIGURATION = "configuration"
    TIMEOUT = "timeout"
    UNKNOWN = "unknown"


class ErrorSeverity(str, Enum):
    """Error severity levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class MutationType(str, Enum):
    """Types of data mutations tracked."""
    LEASE_ADDED = "lease_added"
    LEASE_UPDATED = "lease_updated"
    LEASE_DELETED = "lease_deleted"
    INDEX_REBUILT = "index_rebuilt"
    DOCTRINE_UPDATED = "doctrine_updated"
    CONFIG_CHANGED = "config_changed"
    ALERT_GENERATED = "alert_generated"
    ALERT_ACKNOWLEDGED = "alert_acknowledged"


class MutationOrigin(str, Enum):
    """Origin of a data mutation."""
    USER_REQUEST = "user_request"
    API_CALL = "api_call"
    SCHEDULED_JOB = "scheduled_job"
    AUTO_REFRESH = "auto_refresh"
    INTEGRATION_SYNC = "integration_sync"
    ERROR_RECOVERY = "error_recovery"


# ============================================================================
# TELEMETRY DATA STRUCTURES
# ============================================================================


@dataclass
class QueryTrace:
    """Detailed trace of a single query execution."""
    trace_id: str
    query_type: QueryType
    start_time: float
    end_time: Optional[float] = None
    duration_ms: Optional[float] = None
    response_layer: Optional[ResponseLayer] = None
    input_summary: str = ""
    output_summary: str = ""
    cache_hit: bool = False
    error: Optional[str] = None
    error_domain: Optional[ErrorDomain] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def complete(self, response_layer: ResponseLayer, output_summary: str = "") -> None:
        """Mark the trace as completed."""
        self.end_time = time.monotonic()
        self.duration_ms = (self.end_time - self.start_time) * 1000
        self.response_layer = response_layer
        self.output_summary = output_summary

    def fail(self, error: str, domain: ErrorDomain = ErrorDomain.UNKNOWN) -> None:
        """Mark the trace as failed."""
        self.end_time = time.monotonic()
        self.duration_ms = (self.end_time - self.start_time) * 1000
        self.error = error
        self.error_domain = domain

    def to_dict(self) -> Dict[str, Any]:
        return {
            "trace_id": self.trace_id,
            "query_type": self.query_type.value,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration_ms": self.duration_ms,
            "response_layer": self.response_layer.value if self.response_layer else None,
            "input_summary": self.input_summary,
            "output_summary": self.output_summary,
            "cache_hit": self.cache_hit,
            "error": self.error,
            "error_domain": self.error_domain.value if self.error_domain else None,
            "metadata": self.metadata,
        }


@dataclass
class AuditEntry:
    """Audit trail entry for a lease operation."""
    entry_id: str
    timestamp: str
    mutation_type: MutationType
    mutation_origin: MutationOrigin
    entity_type: str
    entity_id: str
    description: str
    user_context: str = ""
    before_state: Optional[Dict[str, Any]] = None
    after_state: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entry_id": self.entry_id,
            "timestamp": self.timestamp,
            "mutation_type": self.mutation_type.value,
            "mutation_origin": self.mutation_origin.value,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "description": self.description,
            "user_context": self.user_context,
            "before_state": self.before_state,
            "after_state": self.after_state,
            "metadata": self.metadata,
        }


@dataclass
class ErrorRecord:
    """Record of an error occurrence."""
    error_id: str
    timestamp: str
    domain: ErrorDomain
    severity: ErrorSeverity
    message: str
    stack_trace: Optional[str] = None
    query_type: Optional[QueryType] = None
    trace_id: Optional[str] = None
    resolution: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "error_id": self.error_id,
            "timestamp": self.timestamp,
            "domain": self.domain.value,
            "severity": self.severity.value,
            "message": self.message,
            "stack_trace": self.stack_trace,
            "query_type": self.query_type.value if self.query_type else None,
            "trace_id": self.trace_id,
            "resolution": self.resolution,
            "metadata": self.metadata,
        }


# ============================================================================
# METRICS COLLECTOR
# ============================================================================


class MetricsCollector:
    """Collects and aggregates query performance metrics."""

    def __init__(self, window_size: int = 1000) -> None:
        """Initialize the metrics collector.

        Args:
            window_size: Number of recent traces to keep for percentile calculations.
        """
        self._window_size = window_size
        self._query_counts: Dict[QueryType, int] = defaultdict(int)
        self._query_errors: Dict[QueryType, int] = defaultdict(int)
        self._query_durations: Dict[QueryType, Deque[float]] = defaultdict(lambda: deque(maxlen=window_size))
        self._layer_counts: Dict[ResponseLayer, int] = defaultdict(int)
        self._cache_hits: int = 0
        self._cache_misses: int = 0
        self._total_queries: int = 0
        self._error_counts: Dict[ErrorDomain, int] = defaultdict(int)
        self._start_time: float = time.monotonic()
        self._last_reset: str = datetime.now(timezone.utc).isoformat()

    def record_query(self, trace: QueryTrace) -> None:
        """Record a completed query trace into metrics.

        Args:
            trace: The completed QueryTrace to record.
        """
        self._total_queries += 1
        self._query_counts[trace.query_type] += 1

        if trace.duration_ms is not None:
            self._query_durations[trace.query_type].append(trace.duration_ms)

        if trace.response_layer:
            self._layer_counts[trace.response_layer] += 1

        if trace.cache_hit:
            self._cache_hits += 1
        else:
            self._cache_misses += 1

        if trace.error:
            self._query_errors[trace.query_type] += 1
            if trace.error_domain:
                self._error_counts[trace.error_domain] += 1

    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics snapshot.

        Returns:
            Dictionary with all collected metrics.
        """
        uptime_seconds = time.monotonic() - self._start_time

        # Per-query-type metrics
        query_metrics: Dict[str, Any] = {}
        for qt in QueryType:
            count = self._query_counts.get(qt, 0)
            errors = self._query_errors.get(qt, 0)
            durations = list(self._query_durations.get(qt, []))

            metric: Dict[str, Any] = {
                "count": count,
                "errors": errors,
                "error_rate": round(errors / count, 4) if count > 0 else 0.0,
            }

            if durations:
                metric["avg_ms"] = round(statistics.mean(durations), 2)
                metric["p50_ms"] = round(statistics.median(durations), 2)
                metric["p95_ms"] = round(sorted(durations)[int(len(durations) * 0.95)], 2) if len(durations) >= 20 else None
                metric["p99_ms"] = round(sorted(durations)[int(len(durations) * 0.99)], 2) if len(durations) >= 100 else None
                metric["min_ms"] = round(min(durations), 2)
                metric["max_ms"] = round(max(durations), 2)

            if count > 0:
                query_metrics[qt.value] = metric

        # Overall metrics
        all_durations: List[float] = []
        for dq in self._query_durations.values():
            all_durations.extend(dq)

        overall: Dict[str, Any] = {
            "total_queries": self._total_queries,
            "queries_per_minute": round(self._total_queries / max(uptime_seconds / 60, 1), 2),
            "cache_hit_rate": round(self._cache_hits / max(self._total_queries, 1), 4),
            "overall_error_rate": round(
                sum(self._query_errors.values()) / max(self._total_queries, 1), 4
            ),
        }

        if all_durations:
            overall["avg_latency_ms"] = round(statistics.mean(all_durations), 2)
            overall["p50_latency_ms"] = round(statistics.median(all_durations), 2)
            overall["p95_latency_ms"] = (
                round(sorted(all_durations)[int(len(all_durations) * 0.95)], 2)
                if len(all_durations) >= 20 else None
            )

        return {
            "engine_id": "LM02",
            "engine_name": "Lease Analysis Engine",
            "uptime_seconds": round(uptime_seconds, 1),
            "last_reset": self._last_reset,
            "overall": overall,
            "by_query_type": query_metrics,
            "by_response_layer": {k.value: v for k, v in self._layer_counts.items()},
            "by_error_domain": {k.value: v for k, v in self._error_counts.items()},
            "cache": {
                "hits": self._cache_hits,
                "misses": self._cache_misses,
                "hit_rate": round(self._cache_hits / max(self._cache_hits + self._cache_misses, 1), 4),
            },
        }

    def reset(self) -> None:
        """Reset all metrics."""
        self._query_counts.clear()
        self._query_errors.clear()
        self._query_durations.clear()
        self._layer_counts.clear()
        self._cache_hits = 0
        self._cache_misses = 0
        self._total_queries = 0
        self._error_counts.clear()
        self._start_time = time.monotonic()
        self._last_reset = datetime.now(timezone.utc).isoformat()
        logger.info("LM02 Telemetry metrics reset")


# ============================================================================
# TELEMETRY MANAGER
# ============================================================================


class TelemetryManager:
    """Central telemetry manager for the LM02 engine.

    Coordinates trace recording, audit logging, error tracking, and metrics collection.
    """

    def __init__(
        self,
        max_traces: int = 5000,
        max_audit_entries: int = 10000,
        max_errors: int = 2000,
    ) -> None:
        """Initialize the telemetry manager.

        Args:
            max_traces: Maximum number of recent traces to retain.
            max_audit_entries: Maximum number of audit entries to retain.
            max_errors: Maximum number of error records to retain.
        """
        self._traces: Deque[QueryTrace] = deque(maxlen=max_traces)
        self._audit_log: Deque[AuditEntry] = deque(maxlen=max_audit_entries)
        self._errors: Deque[ErrorRecord] = deque(maxlen=max_errors)
        self._metrics = MetricsCollector()
        self._active_traces: Dict[str, QueryTrace] = {}
        self._engine_start_time: float = time.monotonic()
        self._engine_start_iso: str = datetime.now(timezone.utc).isoformat()

        logger.info("LM02 TelemetryManager initialized")

    def start_trace(
        self,
        query_type: QueryType,
        input_summary: str = "",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Start a new query trace.

        Args:
            query_type: The type of query being executed.
            input_summary: Brief description of the input.
            metadata: Additional metadata to attach.

        Returns:
            The trace_id for completing or failing the trace later.
        """
        trace_id = uuid.uuid4().hex[:16]
        trace = QueryTrace(
            trace_id=trace_id,
            query_type=query_type,
            start_time=time.monotonic(),
            input_summary=input_summary,
            metadata=metadata or {},
        )
        self._active_traces[trace_id] = trace
        return trace_id

    def complete_trace(
        self,
        trace_id: str,
        response_layer: ResponseLayer,
        output_summary: str = "",
        cache_hit: bool = False,
    ) -> Optional[QueryTrace]:
        """Complete an active trace successfully.

        Args:
            trace_id: The trace ID from start_trace.
            response_layer: The response layer that served the result.
            output_summary: Brief description of the output.
            cache_hit: Whether the result came from cache.

        Returns:
            The completed QueryTrace, or None if trace not found.
        """
        trace = self._active_traces.pop(trace_id, None)
        if trace is None:
            logger.warning(f"Trace {trace_id} not found in active traces")
            return None

        trace.complete(response_layer, output_summary)
        trace.cache_hit = cache_hit
        self._traces.append(trace)
        self._metrics.record_query(trace)

        logger.debug(
            f"Trace {trace_id} completed: {trace.query_type.value} "
            f"in {trace.duration_ms:.1f}ms via {response_layer.value}"
        )
        return trace

    def fail_trace(
        self,
        trace_id: str,
        error: str,
        domain: ErrorDomain = ErrorDomain.UNKNOWN,
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
    ) -> Optional[QueryTrace]:
        """Fail an active trace with an error.

        Args:
            trace_id: The trace ID from start_trace.
            error: Error message.
            domain: Error domain classification.
            severity: Error severity level.

        Returns:
            The failed QueryTrace, or None if trace not found.
        """
        trace = self._active_traces.pop(trace_id, None)
        if trace is None:
            logger.warning(f"Trace {trace_id} not found in active traces")
            return None

        trace.fail(error, domain)
        self._traces.append(trace)
        self._metrics.record_query(trace)

        # Also record in error log
        self._record_error(error, domain, severity, trace.query_type, trace_id)

        logger.error(
            f"Trace {trace_id} FAILED: {trace.query_type.value} - "
            f"[{domain.value}/{severity.value}] {error}"
        )
        return trace

    def record_audit(
        self,
        mutation_type: MutationType,
        mutation_origin: MutationOrigin,
        entity_type: str,
        entity_id: str,
        description: str,
        user_context: str = "",
        before_state: Optional[Dict[str, Any]] = None,
        after_state: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Record an audit trail entry.

        Args:
            mutation_type: Type of mutation.
            mutation_origin: Origin of the mutation.
            entity_type: Type of entity affected (e.g., "lease", "index", "config").
            entity_id: ID of the entity affected.
            description: Human-readable description of the change.
            user_context: User or session context.
            before_state: State before the change.
            after_state: State after the change.
            metadata: Additional metadata.

        Returns:
            The audit entry ID.
        """
        entry_id = uuid.uuid4().hex[:16]
        entry = AuditEntry(
            entry_id=entry_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            mutation_type=mutation_type,
            mutation_origin=mutation_origin,
            entity_type=entity_type,
            entity_id=entity_id,
            description=description,
            user_context=user_context,
            before_state=before_state,
            after_state=after_state,
            metadata=metadata or {},
        )
        self._audit_log.append(entry)

        logger.info(f"Audit [{mutation_type.value}]: {entity_type}/{entity_id} — {description}")
        return entry_id

    def _record_error(
        self,
        message: str,
        domain: ErrorDomain,
        severity: ErrorSeverity,
        query_type: Optional[QueryType] = None,
        trace_id: Optional[str] = None,
        stack_trace: Optional[str] = None,
    ) -> str:
        """Record an error occurrence.

        Args:
            message: Error message.
            domain: Error domain.
            severity: Error severity.
            query_type: Related query type.
            trace_id: Related trace ID.
            stack_trace: Stack trace if available.

        Returns:
            The error record ID.
        """
        error_id = uuid.uuid4().hex[:16]
        record = ErrorRecord(
            error_id=error_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            domain=domain,
            severity=severity,
            message=message,
            stack_trace=stack_trace,
            query_type=query_type,
            trace_id=trace_id,
        )
        self._errors.append(record)
        return error_id

    def log_error(
        self,
        message: str,
        domain: ErrorDomain = ErrorDomain.UNKNOWN,
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
        query_type: Optional[QueryType] = None,
        stack_trace: Optional[str] = None,
    ) -> str:
        """Log an error outside of a trace context.

        Args:
            message: Error message.
            domain: Error domain.
            severity: Error severity.
            query_type: Related query type.
            stack_trace: Stack trace if available.

        Returns:
            The error record ID.
        """
        error_id = self._record_error(message, domain, severity, query_type, stack_trace=stack_trace)
        logger.error(f"Error [{domain.value}/{severity.value}]: {message}")
        return error_id

    def record_doctrine_mutation(
        self,
        doctrine_key: str,
        mutation: str,
        origin: MutationOrigin = MutationOrigin.USER_REQUEST,
    ) -> str:
        """Record a doctrine cache mutation.

        Args:
            doctrine_key: The doctrine key that was mutated.
            mutation: Description of the mutation.
            origin: Origin of the mutation.

        Returns:
            The audit entry ID.
        """
        return self.record_audit(
            mutation_type=MutationType.DOCTRINE_UPDATED,
            mutation_origin=origin,
            entity_type="doctrine",
            entity_id=doctrine_key,
            description=mutation,
        )

    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics.

        Returns:
            Dictionary with all metrics.
        """
        return self._metrics.get_metrics()

    def get_recent_traces(self, limit: int = 50, query_type: Optional[QueryType] = None) -> List[Dict[str, Any]]:
        """Get recent query traces.

        Args:
            limit: Maximum number of traces to return.
            query_type: Optional filter by query type.

        Returns:
            List of trace dictionaries.
        """
        traces = list(self._traces)
        if query_type:
            traces = [t for t in traces if t.query_type == query_type]
        traces = traces[-limit:]
        return [t.to_dict() for t in reversed(traces)]

    def get_recent_errors(self, limit: int = 50, domain: Optional[ErrorDomain] = None) -> List[Dict[str, Any]]:
        """Get recent error records.

        Args:
            limit: Maximum number of errors to return.
            domain: Optional filter by error domain.

        Returns:
            List of error record dictionaries.
        """
        errors = list(self._errors)
        if domain:
            errors = [e for e in errors if e.domain == domain]
        errors = errors[-limit:]
        return [e.to_dict() for e in reversed(errors)]

    def get_audit_log(
        self,
        limit: int = 100,
        entity_type: Optional[str] = None,
        mutation_type: Optional[MutationType] = None,
    ) -> List[Dict[str, Any]]:
        """Get audit log entries.

        Args:
            limit: Maximum number of entries to return.
            entity_type: Optional filter by entity type.
            mutation_type: Optional filter by mutation type.

        Returns:
            List of audit entry dictionaries.
        """
        entries = list(self._audit_log)
        if entity_type:
            entries = [e for e in entries if e.entity_type == entity_type]
        if mutation_type:
            entries = [e for e in entries if e.mutation_type == mutation_type]
        entries = entries[-limit:]
        return [e.to_dict() for e in reversed(entries)]

    def get_health(self) -> Dict[str, Any]:
        """Get engine health status.

        Returns:
            Dictionary with health metrics.
        """
        uptime = time.monotonic() - self._engine_start_time
        metrics = self._metrics.get_metrics()

        # Determine health status
        error_rate = metrics.get("overall", {}).get("overall_error_rate", 0.0)
        active_traces = len(self._active_traces)

        if error_rate > 0.2 or active_traces > 100:
            status = "degraded"
        elif error_rate > 0.05:
            status = "warning"
        else:
            status = "healthy"

        return {
            "engine_id": "LM02",
            "engine_name": "Lease Analysis Engine",
            "status": status,
            "uptime_seconds": round(uptime, 1),
            "start_time": self._engine_start_iso,
            "total_queries": self._metrics._total_queries,
            "active_traces": active_traces,
            "error_rate": error_rate,
            "cache_hit_rate": metrics.get("cache", {}).get("hit_rate", 0.0),
            "recent_errors": len([e for e in self._errors if (
                datetime.now(timezone.utc) - datetime.fromisoformat(e.timestamp)
            ).total_seconds() < 300]),
            "trace_buffer_usage": f"{len(self._traces)}/{self._traces.maxlen}",
            "audit_buffer_usage": f"{len(self._audit_log)}/{self._audit_log.maxlen}",
            "error_buffer_usage": f"{len(self._errors)}/{self._errors.maxlen}",
        }

    def export_telemetry(self) -> Dict[str, Any]:
        """Export all telemetry data for persistence.

        Returns:
            Dictionary with all telemetry data.
        """
        return {
            "engine_id": "LM02",
            "export_time": datetime.now(timezone.utc).isoformat(),
            "health": self.get_health(),
            "metrics": self.get_metrics(),
            "recent_traces": self.get_recent_traces(limit=100),
            "recent_errors": self.get_recent_errors(limit=100),
            "audit_log": self.get_audit_log(limit=200),
        }


# ============================================================================
# MODULE-LEVEL TELEMETRY INSTANCE
# ============================================================================

_TELEMETRY = TelemetryManager()


def get_telemetry() -> TelemetryManager:
    """Get the module-level TelemetryManager instance."""
    return _TELEMETRY


def trace_query(
    query_type: QueryType,
    input_summary: str = "",
    metadata: Optional[Dict[str, Any]] = None,
) -> str:
    """Start a query trace using the module-level telemetry manager.

    Args:
        query_type: Type of query.
        input_summary: Brief description of input.
        metadata: Additional metadata.

    Returns:
        The trace_id.
    """
    return _TELEMETRY.start_trace(query_type, input_summary, metadata)


def complete_trace(
    trace_id: str,
    response_layer: ResponseLayer,
    output_summary: str = "",
    cache_hit: bool = False,
) -> Optional[QueryTrace]:
    """Complete a trace using the module-level telemetry manager.

    Args:
        trace_id: The trace ID from trace_query.
        response_layer: The response layer.
        output_summary: Brief output description.
        cache_hit: Whether result was from cache.

    Returns:
        The completed QueryTrace.
    """
    return _TELEMETRY.complete_trace(trace_id, response_layer, output_summary, cache_hit)


def fail_trace(
    trace_id: str,
    error: str,
    domain: ErrorDomain = ErrorDomain.UNKNOWN,
    severity: ErrorSeverity = ErrorSeverity.MEDIUM,
) -> Optional[QueryTrace]:
    """Fail a trace using the module-level telemetry manager."""
    return _TELEMETRY.fail_trace(trace_id, error, domain, severity)


def log_error(
    message: str,
    domain: ErrorDomain = ErrorDomain.UNKNOWN,
    severity: ErrorSeverity = ErrorSeverity.MEDIUM,
    query_type: Optional[QueryType] = None,
) -> str:
    """Log an error using the module-level telemetry manager."""
    return _TELEMETRY.log_error(message, domain, severity, query_type)


def record_doctrine_mutation(
    doctrine_key: str,
    mutation: str,
    origin: MutationOrigin = MutationOrigin.USER_REQUEST,
) -> str:
    """Record a doctrine mutation using the module-level telemetry manager."""
    return _TELEMETRY.record_doctrine_mutation(doctrine_key, mutation, origin)
