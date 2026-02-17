"""
LM01 Title Examination Engine - Telemetry Module
==================================================

Performance metrics, query tracking, audit trail, and
deterministic hashing for the title examination engine.

Provides:
- Real-time performance metrics collection
- Query execution tracking with timing
- Full audit trail of examinations
- Deterministic SHA-256 hashing for results
- Health monitoring and alerting
- Session-level metrics aggregation
- Error tracking and classification

Author: ECHO OMEGA PRIME Build System
Engine: LM01 Title Examination
"""

from __future__ import annotations

import hashlib
import json
import statistics
import time
import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

from loguru import logger


# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------

class MetricType(str, Enum):
    """Types of metrics tracked."""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    TIMER = "timer"


class OperationType(str, Enum):
    """Types of operations tracked."""
    TITLE_EXAM = "title_examination"
    CHAIN_BUILD = "chain_build"
    DEFECT_DETECT = "defect_detection"
    OPINION_GEN = "opinion_generation"
    CURATIVE_ANALYZE = "curative_analysis"
    INTEREST_CALC = "interest_calculation"
    RUN_SHEET = "run_sheet_generation"
    SEARCH = "search"
    INDEX_BUILD = "index_build"
    CHAIN_TRACE = "chain_trace"
    OWNERSHIP_CALC = "ownership_calculation"
    EXPORT = "export"


class AuditEventType(str, Enum):
    """Types of audit events."""
    EXAM_STARTED = "exam_started"
    EXAM_COMPLETED = "exam_completed"
    EXAM_FAILED = "exam_failed"
    CHAIN_BUILT = "chain_built"
    DEFECT_FOUND = "defect_found"
    OPINION_GENERATED = "opinion_generated"
    CURATIVE_IDENTIFIED = "curative_identified"
    INTEREST_CALCULATED = "interest_calculated"
    RUN_SHEET_BUILT = "run_sheet_built"
    SEARCH_EXECUTED = "search_executed"
    ERROR_OCCURRED = "error_occurred"
    CONFIG_CHANGED = "config_changed"
    ENGINE_STARTED = "engine_started"
    ENGINE_STOPPED = "engine_stopped"
    HEALTH_CHECK = "health_check"


class ErrorSeverity(str, Enum):
    """Severity of errors."""
    FATAL = "fatal"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class MetricPoint:
    """A single metric data point."""
    name: str
    metric_type: MetricType
    value: float
    timestamp: datetime = field(default_factory=datetime.utcnow)
    labels: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "type": self.metric_type.value,
            "value": self.value,
            "timestamp": self.timestamp.isoformat(),
            "labels": self.labels,
        }


@dataclass
class OperationTimer:
    """Timer for tracking operation duration."""
    operation_id: str
    operation_type: OperationType
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None

    @property
    def duration_ms(self) -> float:
        end = self.end_time or time.time()
        return (end - self.start_time) * 1000

    @property
    def is_complete(self) -> bool:
        return self.end_time is not None

    def complete(self, metadata: Optional[Dict[str, Any]] = None) -> float:
        """Mark operation as complete. Returns duration in ms."""
        self.end_time = time.time()
        if metadata:
            self.metadata.update(metadata)
        return self.duration_ms

    def fail(self, error: str) -> float:
        """Mark operation as failed. Returns duration in ms."""
        self.end_time = time.time()
        self.error = error
        return self.duration_ms

    def to_dict(self) -> Dict[str, Any]:
        return {
            "operation_id": self.operation_id,
            "operation_type": self.operation_type.value,
            "start_time": datetime.fromtimestamp(self.start_time).isoformat(),
            "end_time": datetime.fromtimestamp(self.end_time).isoformat() if self.end_time else None,
            "duration_ms": round(self.duration_ms, 2),
            "is_complete": self.is_complete,
            "error": self.error,
            "metadata": self.metadata,
        }


@dataclass
class AuditEvent:
    """A single audit trail event."""
    event_id: str
    event_type: AuditEventType
    timestamp: datetime
    operation_id: Optional[str]
    user_id: Optional[str]
    description: str
    details: Dict[str, Any] = field(default_factory=dict)
    deterministic_hash: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type.value,
            "timestamp": self.timestamp.isoformat(),
            "operation_id": self.operation_id,
            "user_id": self.user_id,
            "description": self.description,
            "details": self.details,
            "deterministic_hash": self.deterministic_hash,
        }


@dataclass
class ErrorRecord:
    """A tracked error."""
    error_id: str
    severity: ErrorSeverity
    operation_type: Optional[OperationType]
    timestamp: datetime
    error_type: str
    message: str
    stack_trace: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)
    resolved: bool = False
    resolution: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "error_id": self.error_id,
            "severity": self.severity.value,
            "operation_type": self.operation_type.value if self.operation_type else None,
            "timestamp": self.timestamp.isoformat(),
            "error_type": self.error_type,
            "message": self.message,
            "stack_trace": self.stack_trace,
            "context": self.context,
            "resolved": self.resolved,
            "resolution": self.resolution,
        }


# ---------------------------------------------------------------------------
# Metrics Collection
# ---------------------------------------------------------------------------

class ExamMetrics:
    """
    Real-time metrics collection for title examination operations.
    Tracks counters, gauges, histograms, and timers.
    """

    def __init__(self) -> None:
        self._counters: Dict[str, float] = defaultdict(float)
        self._gauges: Dict[str, float] = {}
        self._histograms: Dict[str, List[float]] = defaultdict(list)
        self._timers: Dict[str, List[float]] = defaultdict(list)
        self._active_operations: Dict[str, OperationTimer] = {}
        self._operation_history: List[OperationTimer] = []
        self._created_at: datetime = datetime.utcnow()

    def increment(self, name: str, value: float = 1.0, labels: Optional[Dict[str, str]] = None) -> None:
        """Increment a counter metric."""
        key = self._make_key(name, labels)
        self._counters[key] += value

    def set_gauge(self, name: str, value: float, labels: Optional[Dict[str, str]] = None) -> None:
        """Set a gauge metric."""
        key = self._make_key(name, labels)
        self._gauges[key] = value

    def observe(self, name: str, value: float, labels: Optional[Dict[str, str]] = None) -> None:
        """Add an observation to a histogram metric."""
        key = self._make_key(name, labels)
        self._histograms[key].append(value)

    def start_timer(
        self,
        operation_type: OperationType,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Start a timer for an operation. Returns operation_id."""
        op_id = str(uuid.uuid4())[:12]
        timer = OperationTimer(
            operation_id=op_id,
            operation_type=operation_type,
            metadata=metadata or {},
        )
        self._active_operations[op_id] = timer
        self.increment(f"operations.started.{operation_type.value}")
        return op_id

    def stop_timer(
        self,
        operation_id: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Optional[float]:
        """Stop a timer. Returns duration in ms."""
        timer = self._active_operations.pop(operation_id, None)
        if not timer:
            logger.warning(f"No active timer found for operation {operation_id}")
            return None

        duration = timer.complete(metadata)
        self._operation_history.append(timer)
        self._timers[timer.operation_type.value].append(duration)
        self.increment(f"operations.completed.{timer.operation_type.value}")
        self.observe(f"operation.duration.{timer.operation_type.value}", duration)
        return duration

    def fail_timer(self, operation_id: str, error: str) -> Optional[float]:
        """Mark a timed operation as failed. Returns duration in ms."""
        timer = self._active_operations.pop(operation_id, None)
        if not timer:
            return None

        duration = timer.fail(error)
        self._operation_history.append(timer)
        self.increment(f"operations.failed.{timer.operation_type.value}")
        self.observe(f"operation.duration.{timer.operation_type.value}", duration)
        return duration

    def _make_key(self, name: str, labels: Optional[Dict[str, str]] = None) -> str:
        if not labels:
            return name
        label_str = ",".join(f"{k}={v}" for k, v in sorted(labels.items()))
        return f"{name}{{{label_str}}}"

    def get_counter(self, name: str) -> float:
        return self._counters.get(name, 0.0)

    def get_gauge(self, name: str) -> Optional[float]:
        return self._gauges.get(name)

    def get_histogram_stats(self, name: str) -> Dict[str, float]:
        """Get statistical summary of a histogram."""
        values = self._histograms.get(name, [])
        if not values:
            return {"count": 0, "min": 0, "max": 0, "mean": 0, "median": 0, "p95": 0, "p99": 0}

        sorted_values = sorted(values)
        count = len(sorted_values)

        return {
            "count": count,
            "min": sorted_values[0],
            "max": sorted_values[-1],
            "mean": statistics.mean(sorted_values),
            "median": statistics.median(sorted_values),
            "p95": sorted_values[int(count * 0.95)] if count > 1 else sorted_values[0],
            "p99": sorted_values[int(count * 0.99)] if count > 1 else sorted_values[0],
            "stdev": statistics.stdev(sorted_values) if count > 1 else 0,
        }

    def get_operation_stats(self, operation_type: Optional[OperationType] = None) -> Dict[str, Any]:
        """Get operation statistics, optionally filtered by type."""
        ops = self._operation_history
        if operation_type:
            ops = [o for o in ops if o.operation_type == operation_type]

        if not ops:
            return {
                "total": 0,
                "completed": 0,
                "failed": 0,
                "avg_duration_ms": 0,
                "max_duration_ms": 0,
                "min_duration_ms": 0,
            }

        completed = [o for o in ops if o.is_complete and not o.error]
        failed = [o for o in ops if o.error]
        durations = [o.duration_ms for o in ops if o.is_complete]

        return {
            "total": len(ops),
            "completed": len(completed),
            "failed": len(failed),
            "active": len(self._active_operations),
            "avg_duration_ms": round(statistics.mean(durations), 2) if durations else 0,
            "max_duration_ms": round(max(durations), 2) if durations else 0,
            "min_duration_ms": round(min(durations), 2) if durations else 0,
            "median_duration_ms": round(statistics.median(durations), 2) if durations else 0,
            "error_rate": round(len(failed) / len(ops), 4) if ops else 0,
        }

    def get_all_counters(self) -> Dict[str, float]:
        return dict(self._counters)

    def get_all_gauges(self) -> Dict[str, float]:
        return dict(self._gauges)

    def summary(self) -> Dict[str, Any]:
        """Get complete metrics summary."""
        uptime = (datetime.utcnow() - self._created_at).total_seconds()

        operation_summary: Dict[str, Any] = {}
        for op_type in OperationType:
            stats = self.get_operation_stats(op_type)
            if stats["total"] > 0:
                operation_summary[op_type.value] = stats

        return {
            "uptime_seconds": round(uptime, 2),
            "counters": dict(self._counters),
            "gauges": dict(self._gauges),
            "operations": operation_summary,
            "active_operations": len(self._active_operations),
            "total_history": len(self._operation_history),
        }

    def reset(self) -> None:
        """Reset all metrics."""
        self._counters.clear()
        self._gauges.clear()
        self._histograms.clear()
        self._timers.clear()
        self._operation_history.clear()
        logger.info("Metrics reset")


# ---------------------------------------------------------------------------
# Query Tracker
# ---------------------------------------------------------------------------

class QueryTracker:
    """
    Tracks search queries for analysis and optimization.
    Records query patterns, execution times, and result counts.
    """

    def __init__(self, max_history: int = 10000) -> None:
        self._history: List[Dict[str, Any]] = []
        self._max_history = max_history
        self._query_counts: Dict[str, int] = defaultdict(int)
        self._slow_queries: List[Dict[str, Any]] = []
        self._slow_threshold_ms: float = 500.0

    def track(
        self,
        query_id: str,
        query_params: Dict[str, Any],
        result_count: int,
        duration_ms: float,
        search_fields: List[str],
    ) -> None:
        """Track a completed query."""
        entry = {
            "query_id": query_id,
            "timestamp": datetime.utcnow().isoformat(),
            "params": query_params,
            "result_count": result_count,
            "duration_ms": round(duration_ms, 2),
            "search_fields": search_fields,
        }

        self._history.append(entry)
        if len(self._history) > self._max_history:
            self._history = self._history[-self._max_history:]

        fields_key = ",".join(sorted(search_fields))
        self._query_counts[fields_key] += 1

        if duration_ms > self._slow_threshold_ms:
            self._slow_queries.append(entry)
            if len(self._slow_queries) > 100:
                self._slow_queries = self._slow_queries[-100:]
            logger.warning(
                f"Slow query detected: {duration_ms:.2f}ms "
                f"(threshold: {self._slow_threshold_ms}ms)"
            )

    def get_recent(self, count: int = 20) -> List[Dict[str, Any]]:
        """Get most recent queries."""
        return self._history[-count:]

    def get_slow_queries(self) -> List[Dict[str, Any]]:
        """Get slow queries above threshold."""
        return list(self._slow_queries)

    def get_popular_patterns(self, top_n: int = 10) -> List[Tuple[str, int]]:
        """Get most popular query field combinations."""
        sorted_patterns = sorted(
            self._query_counts.items(),
            key=lambda x: x[1],
            reverse=True,
        )
        return sorted_patterns[:top_n]

    def get_stats(self) -> Dict[str, Any]:
        """Get query tracker statistics."""
        if not self._history:
            return {
                "total_queries": 0,
                "avg_duration_ms": 0,
                "avg_results": 0,
                "slow_queries": 0,
            }

        durations = [q["duration_ms"] for q in self._history]
        result_counts = [q["result_count"] for q in self._history]

        return {
            "total_queries": len(self._history),
            "avg_duration_ms": round(statistics.mean(durations), 2),
            "median_duration_ms": round(statistics.median(durations), 2),
            "max_duration_ms": round(max(durations), 2),
            "avg_results": round(statistics.mean(result_counts), 1),
            "slow_queries": len(self._slow_queries),
            "popular_patterns": self.get_popular_patterns(5),
        }

    def set_slow_threshold(self, threshold_ms: float) -> None:
        """Set the slow query threshold in milliseconds."""
        self._slow_threshold_ms = threshold_ms
        logger.info(f"Slow query threshold set to {threshold_ms}ms")


# ---------------------------------------------------------------------------
# Audit Trail
# ---------------------------------------------------------------------------

class AuditTrail:
    """
    Immutable audit trail for title examination operations.
    Each event is hashed and chained for tamper detection.
    """

    def __init__(self) -> None:
        self._events: List[AuditEvent] = []
        self._chain_hash: str = "0" * 64
        self._event_counts: Dict[str, int] = defaultdict(int)

    def record(
        self,
        event_type: AuditEventType,
        description: str,
        operation_id: Optional[str] = None,
        user_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> AuditEvent:
        """Record an audit event. Returns the created event."""
        event = AuditEvent(
            event_id=str(uuid.uuid4())[:12],
            event_type=event_type,
            timestamp=datetime.utcnow(),
            operation_id=operation_id,
            user_id=user_id,
            description=description,
            details=details or {},
        )

        event.deterministic_hash = self._compute_event_hash(event)
        self._chain_hash = self._chain_event(event)
        self._events.append(event)
        self._event_counts[event_type.value] += 1

        logger.debug(
            f"Audit: [{event_type.value}] {description} "
            f"(hash: {event.deterministic_hash[:12]})"
        )

        return event

    def _compute_event_hash(self, event: AuditEvent) -> str:
        """Compute deterministic hash for an event."""
        hash_input = json.dumps({
            "event_id": event.event_id,
            "event_type": event.event_type.value,
            "timestamp": event.timestamp.isoformat(),
            "operation_id": event.operation_id,
            "user_id": event.user_id,
            "description": event.description,
            "details": event.details,
        }, sort_keys=True, default=str)
        return hashlib.sha256(hash_input.encode()).hexdigest()

    def _chain_event(self, event: AuditEvent) -> str:
        """Chain the event hash with the previous chain hash."""
        chain_input = f"{self._chain_hash}:{event.deterministic_hash}"
        return hashlib.sha256(chain_input.encode()).hexdigest()

    def verify_chain_integrity(self) -> Tuple[bool, Optional[str]]:
        """
        Verify the integrity of the entire audit chain.
        Returns (is_valid, error_message).
        """
        if not self._events:
            return (True, None)

        current_chain = "0" * 64

        for i, event in enumerate(self._events):
            expected_hash = self._compute_event_hash(event)
            if event.deterministic_hash != expected_hash:
                return (False, f"Event {i} hash mismatch: expected {expected_hash[:16]}, "
                               f"got {event.deterministic_hash[:16]}")

            chain_input = f"{current_chain}:{event.deterministic_hash}"
            current_chain = hashlib.sha256(chain_input.encode()).hexdigest()

        if current_chain != self._chain_hash:
            return (False, f"Chain hash mismatch: expected {current_chain[:16]}, "
                           f"got {self._chain_hash[:16]}")

        return (True, None)

    def get_events(
        self,
        event_type: Optional[AuditEventType] = None,
        operation_id: Optional[str] = None,
        since: Optional[datetime] = None,
        limit: int = 100,
    ) -> List[AuditEvent]:
        """Query audit events with optional filters."""
        results = self._events

        if event_type:
            results = [e for e in results if e.event_type == event_type]

        if operation_id:
            results = [e for e in results if e.operation_id == operation_id]

        if since:
            results = [e for e in results if e.timestamp >= since]

        return results[-limit:]

    def get_recent(self, count: int = 20) -> List[AuditEvent]:
        """Get most recent audit events."""
        return self._events[-count:]

    @property
    def chain_hash(self) -> str:
        """Current chain hash."""
        return self._chain_hash

    @property
    def event_count(self) -> int:
        """Total number of audit events."""
        return len(self._events)

    def get_stats(self) -> Dict[str, Any]:
        """Get audit trail statistics."""
        is_valid, error = self.verify_chain_integrity()
        return {
            "total_events": len(self._events),
            "event_counts": dict(self._event_counts),
            "chain_hash": self._chain_hash[:16] + "...",
            "chain_integrity": is_valid,
            "integrity_error": error,
            "oldest_event": self._events[0].timestamp.isoformat() if self._events else None,
            "newest_event": self._events[-1].timestamp.isoformat() if self._events else None,
        }

    def export_json(self, indent: int = 2) -> str:
        """Export full audit trail as JSON."""
        return json.dumps({
            "events": [e.to_dict() for e in self._events],
            "chain_hash": self._chain_hash,
            "event_count": len(self._events),
            "integrity_verified": self.verify_chain_integrity()[0],
        }, indent=indent, default=str)


# ---------------------------------------------------------------------------
# Error Tracker
# ---------------------------------------------------------------------------

class ErrorTracker:
    """
    Tracks and classifies errors for debugging and improvement.
    """

    def __init__(self, max_errors: int = 5000) -> None:
        self._errors: List[ErrorRecord] = []
        self._max_errors = max_errors
        self._by_type: Dict[str, int] = defaultdict(int)
        self._by_severity: Dict[str, int] = defaultdict(int)
        self._by_operation: Dict[str, int] = defaultdict(int)

    def record_error(
        self,
        severity: ErrorSeverity,
        error_type: str,
        message: str,
        operation_type: Optional[OperationType] = None,
        stack_trace: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> ErrorRecord:
        """Record an error."""
        error = ErrorRecord(
            error_id=str(uuid.uuid4())[:12],
            severity=severity,
            operation_type=operation_type,
            timestamp=datetime.utcnow(),
            error_type=error_type,
            message=message,
            stack_trace=stack_trace,
            context=context or {},
        )

        self._errors.append(error)
        if len(self._errors) > self._max_errors:
            self._errors = self._errors[-self._max_errors:]

        self._by_type[error_type] += 1
        self._by_severity[severity.value] += 1
        if operation_type:
            self._by_operation[operation_type.value] += 1

        if severity in (ErrorSeverity.FATAL, ErrorSeverity.ERROR):
            logger.error(f"[{error_type}] {message}")
        elif severity == ErrorSeverity.WARNING:
            logger.warning(f"[{error_type}] {message}")

        return error

    def resolve_error(self, error_id: str, resolution: str) -> bool:
        """Mark an error as resolved."""
        for error in reversed(self._errors):
            if error.error_id == error_id:
                error.resolved = True
                error.resolution = resolution
                return True
        return False

    def get_unresolved(self, severity: Optional[ErrorSeverity] = None) -> List[ErrorRecord]:
        """Get unresolved errors."""
        results = [e for e in self._errors if not e.resolved]
        if severity:
            results = [e for e in results if e.severity == severity]
        return results

    def get_recent(self, count: int = 20) -> List[ErrorRecord]:
        """Get most recent errors."""
        return self._errors[-count:]

    def get_stats(self) -> Dict[str, Any]:
        """Get error statistics."""
        return {
            "total_errors": len(self._errors),
            "unresolved": len([e for e in self._errors if not e.resolved]),
            "by_type": dict(self._by_type),
            "by_severity": dict(self._by_severity),
            "by_operation": dict(self._by_operation),
        }


# ---------------------------------------------------------------------------
# Deterministic Hashing
# ---------------------------------------------------------------------------

def compute_deterministic_hash(data: Any) -> str:
    """
    Compute a deterministic SHA-256 hash of any JSON-serializable data.
    Ensures consistent ordering for reproducible results.
    """
    serialized = json.dumps(data, sort_keys=True, default=str, ensure_ascii=True)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def compute_chain_hash(instruments: List[Dict[str, Any]]) -> str:
    """
    Compute a deterministic hash of a chain of title.
    Hash is stable regardless of field ordering within instruments.
    """
    hasher = hashlib.sha256()
    for inst in instruments:
        inst_hash = compute_deterministic_hash(inst)
        hasher.update(inst_hash.encode())
    return hasher.hexdigest()


def compute_opinion_hash(opinion_data: Dict[str, Any]) -> str:
    """Compute deterministic hash of a title opinion."""
    return compute_deterministic_hash(opinion_data)


# ---------------------------------------------------------------------------
# Main Telemetry Class
# ---------------------------------------------------------------------------

class TitleExamTelemetry:
    """
    Central telemetry system for the title examination engine.
    Aggregates metrics, query tracking, audit trail, and error tracking.
    """

    def __init__(self) -> None:
        self.metrics = ExamMetrics()
        self.queries = QueryTracker()
        self.audit = AuditTrail()
        self.errors = ErrorTracker()
        self._session_id: str = str(uuid.uuid4())[:12]
        self._started_at: datetime = datetime.utcnow()
        self._engine_version: str = "1.0.0"

        self.audit.record(
            AuditEventType.ENGINE_STARTED,
            f"Title Examination Engine telemetry started (session: {self._session_id})",
            details={"session_id": self._session_id, "version": self._engine_version},
        )

    @property
    def session_id(self) -> str:
        return self._session_id

    def start_operation(
        self,
        operation_type: OperationType,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Start tracking an operation. Returns operation_id."""
        op_id = self.metrics.start_timer(operation_type, metadata)

        self.audit.record(
            AuditEventType.EXAM_STARTED,
            f"Operation {operation_type.value} started",
            operation_id=op_id,
            details=metadata or {},
        )

        return op_id

    def complete_operation(
        self,
        operation_id: str,
        result_summary: Optional[Dict[str, Any]] = None,
    ) -> Optional[float]:
        """Complete an operation. Returns duration in ms."""
        duration = self.metrics.stop_timer(operation_id, result_summary)

        if duration is not None:
            self.audit.record(
                AuditEventType.EXAM_COMPLETED,
                f"Operation completed in {duration:.2f}ms",
                operation_id=operation_id,
                details=result_summary or {},
            )

        return duration

    def fail_operation(
        self,
        operation_id: str,
        error: str,
        error_type: str = "OperationError",
        severity: ErrorSeverity = ErrorSeverity.ERROR,
    ) -> Optional[float]:
        """Fail an operation. Returns duration in ms."""
        duration = self.metrics.fail_timer(operation_id, error)

        self.errors.record_error(
            severity=severity,
            error_type=error_type,
            message=error,
            context={"operation_id": operation_id},
        )

        self.audit.record(
            AuditEventType.EXAM_FAILED,
            f"Operation failed: {error}",
            operation_id=operation_id,
            details={"error": error, "error_type": error_type},
        )

        return duration

    def track_search(
        self,
        query_id: str,
        query_params: Dict[str, Any],
        result_count: int,
        duration_ms: float,
        search_fields: List[str],
    ) -> None:
        """Track a search query execution."""
        self.queries.track(query_id, query_params, result_count, duration_ms, search_fields)
        self.metrics.increment("search.total")
        self.metrics.observe("search.duration_ms", duration_ms)
        self.metrics.observe("search.result_count", float(result_count))

        self.audit.record(
            AuditEventType.SEARCH_EXECUTED,
            f"Search returned {result_count} results in {duration_ms:.2f}ms",
            details={"query_id": query_id, "result_count": result_count},
        )

    def track_defect(
        self,
        defect_category: str,
        severity: str,
        operation_id: Optional[str] = None,
    ) -> None:
        """Track a defect detection."""
        self.metrics.increment(f"defects.{severity}")
        self.metrics.increment(f"defects.category.{defect_category}")

        self.audit.record(
            AuditEventType.DEFECT_FOUND,
            f"Defect detected: {defect_category} ({severity})",
            operation_id=operation_id,
            details={"category": defect_category, "severity": severity},
        )

    def track_opinion(
        self,
        opinion_type: str,
        title_quality: str,
        operation_id: Optional[str] = None,
    ) -> None:
        """Track a title opinion generation."""
        self.metrics.increment(f"opinions.{opinion_type}")
        self.metrics.increment(f"opinions.quality.{title_quality}")

        self.audit.record(
            AuditEventType.OPINION_GENERATED,
            f"Title opinion generated: {opinion_type} ({title_quality})",
            operation_id=operation_id,
            details={"opinion_type": opinion_type, "title_quality": title_quality},
        )

    def health_check(self) -> Dict[str, Any]:
        """Return comprehensive health status."""
        uptime = (datetime.utcnow() - self._started_at).total_seconds()
        chain_valid, chain_error = self.audit.verify_chain_integrity()

        return {
            "status": "healthy",
            "session_id": self._session_id,
            "engine_version": self._engine_version,
            "uptime_seconds": round(uptime, 2),
            "metrics_summary": {
                "total_operations": sum(
                    self.metrics.get_counter(f"operations.started.{op.value}")
                    for op in OperationType
                ),
                "total_searches": self.metrics.get_counter("search.total"),
                "active_operations": len(self.metrics._active_operations),
            },
            "query_stats": self.queries.get_stats(),
            "audit": {
                "total_events": self.audit.event_count,
                "chain_integrity": chain_valid,
                "chain_error": chain_error,
            },
            "errors": {
                "total": len(self.errors._errors),
                "unresolved": len(self.errors.get_unresolved()),
            },
        }

    def summary(self) -> Dict[str, Any]:
        """Get full telemetry summary."""
        return {
            "session_id": self._session_id,
            "engine_version": self._engine_version,
            "started_at": self._started_at.isoformat(),
            "metrics": self.metrics.summary(),
            "queries": self.queries.get_stats(),
            "audit": self.audit.get_stats(),
            "errors": self.errors.get_stats(),
            "health": self.health_check(),
        }

    def export_json(self, indent: int = 2) -> str:
        """Export full telemetry as JSON."""
        return json.dumps(self.summary(), indent=indent, default=str)
