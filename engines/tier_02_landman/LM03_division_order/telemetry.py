"""
LM03 Division Order Engine - Telemetry Module
===============================================

Performance metrics, query tracking, audit trail, deterministic hashing,
drift detection, and health monitoring for the division order engine.

Provides:
- Real-time performance metrics collection per operation type
- Query execution tracking with sub-millisecond timing
- Full audit trail of all division order operations
- Deterministic SHA-256 hashing for interest calculations
- Drift detection for decimal interest totals
- Session-level metrics aggregation
- Error tracking and classification with severity levels
- Health monitoring with component-level status

Author: ECHO OMEGA PRIME Build System
Engine: LM03 Division Order
"""

from __future__ import annotations

import hashlib
import json
import statistics
import time
import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

from loguru import logger


# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------

class MetricType(str, Enum):
    """Types of metrics tracked by the telemetry system."""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    TIMER = "timer"


class OperationType(str, Enum):
    """Types of operations tracked in the division order engine."""
    INTEREST_CALC = "interest_calculation"
    DECIMAL_CONVERT = "decimal_conversion"
    CHAIN_TRACE = "chain_trace"
    PAY_DECK_BUILD = "pay_deck_build"
    REVENUE_DISTRIBUTE = "revenue_distribution"
    SUSPENSE_ANALYZE = "suspense_analysis"
    RATIFICATION_CHECK = "ratification_check"
    POOLING_ALLOCATE = "pooling_allocation"
    DUHIG_APPLY = "duhig_application"
    JOA_PARSE = "joa_parse"
    DOCTRINE_SEARCH = "doctrine_search"
    SEMANTIC_LOOKUP = "semantic_lookup"
    DIVISION_ORDER_GEN = "division_order_generation"
    TITLE_OPINION_GEN = "title_opinion_generation"
    OWNERSHIP_CHANGE = "ownership_change"
    ESCHEAT_CHECK = "escheat_check"
    HEALTH_CHECK = "health_check"
    ENGINE_QUERY = "engine_query"
    EXPORT = "export"


class AuditEventType(str, Enum):
    """Types of audit events logged."""
    INTEREST_CALCULATED = "interest_calculated"
    DECIMAL_CONVERTED = "decimal_converted"
    CHAIN_TRACED = "chain_traced"
    PAY_DECK_BUILT = "pay_deck_built"
    REVENUE_DISTRIBUTED = "revenue_distributed"
    SUSPENSE_PLACED = "suspense_placed"
    SUSPENSE_RELEASED = "suspense_released"
    RATIFICATION_SENT = "ratification_sent"
    RATIFICATION_RECEIVED = "ratification_received"
    POOLING_ALLOCATED = "pooling_allocated"
    DUHIG_APPLIED = "duhig_applied"
    OWNERSHIP_CHANGED = "ownership_changed"
    ESCHEAT_FLAGGED = "escheat_flagged"
    DIVISION_ORDER_GENERATED = "division_order_generated"
    TITLE_OPINION_GENERATED = "title_opinion_generated"
    DOCTRINE_SEARCHED = "doctrine_searched"
    ERROR_OCCURRED = "error_occurred"
    CONFIG_CHANGED = "config_changed"
    ENGINE_STARTED = "engine_started"
    ENGINE_STOPPED = "engine_stopped"
    HEALTH_CHECKED = "health_checked"
    DRIFT_DETECTED = "drift_detected"


class ErrorSeverity(str, Enum):
    """Severity classification for errors."""
    FATAL = "fatal"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class DriftType(str, Enum):
    """Types of drift detected in the engine."""
    INTEREST_TOTAL_DRIFT = "interest_total_drift"
    DECIMAL_PRECISION_DRIFT = "decimal_precision_drift"
    DOCTRINE_COVERAGE_DRIFT = "doctrine_coverage_drift"
    RESPONSE_TIME_DRIFT = "response_time_drift"
    ERROR_RATE_DRIFT = "error_rate_drift"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class MetricPoint:
    """A single metric data point with labels."""
    name: str
    metric_type: MetricType
    value: float
    timestamp: datetime = field(default_factory=datetime.utcnow)
    labels: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "name": self.name,
            "type": self.metric_type.value,
            "value": self.value,
            "timestamp": self.timestamp.isoformat(),
            "labels": self.labels,
        }


@dataclass
class OperationTimer:
    """Timer for tracking individual operation duration."""
    operation_id: str
    operation_type: OperationType
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None

    @property
    def duration_ms(self) -> float:
        """Return duration in milliseconds."""
        end = self.end_time or time.time()
        return (end - self.start_time) * 1000

    @property
    def is_complete(self) -> bool:
        """Check if the operation has completed."""
        return self.end_time is not None

    def complete(self, metadata: Optional[Dict[str, Any]] = None) -> float:
        """Mark operation as complete. Returns duration in ms."""
        self.end_time = time.time()
        if metadata:
            self.metadata.update(metadata)
        duration = self.duration_ms
        logger.debug(
            "Operation {op_type} completed in {dur:.2f}ms",
            op_type=self.operation_type.value,
            dur=duration,
        )
        return duration

    def fail(self, error: str) -> float:
        """Mark operation as failed. Returns duration in ms."""
        self.end_time = time.time()
        self.error = error
        duration = self.duration_ms
        logger.warning(
            "Operation {op_type} failed in {dur:.2f}ms: {err}",
            op_type=self.operation_type.value,
            dur=duration,
            err=error,
        )
        return duration

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
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
    """A single immutable audit trail event."""
    event_id: str
    event_type: AuditEventType
    timestamp: datetime
    operation_id: Optional[str]
    user_id: Optional[str]
    description: str
    details: Dict[str, Any] = field(default_factory=dict)
    deterministic_hash: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
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
    """A tracked error with context and resolution status."""
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
        """Serialize to dictionary."""
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

    def resolve(self, resolution: str) -> None:
        """Mark the error as resolved."""
        self.resolved = True
        self.resolution = resolution
        logger.info(
            "Error {eid} resolved: {res}",
            eid=self.error_id,
            res=resolution,
        )


@dataclass
class DriftObservation:
    """A single drift detection observation."""
    observation_id: str
    drift_type: DriftType
    timestamp: datetime
    expected_value: float
    actual_value: float
    deviation: float
    threshold: float
    is_violation: bool
    context: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "observation_id": self.observation_id,
            "drift_type": self.drift_type.value,
            "timestamp": self.timestamp.isoformat(),
            "expected_value": self.expected_value,
            "actual_value": self.actual_value,
            "deviation": self.deviation,
            "threshold": self.threshold,
            "is_violation": self.is_violation,
            "context": self.context,
        }


# ---------------------------------------------------------------------------
# Hashing Functions
# ---------------------------------------------------------------------------

def compute_deterministic_hash(data: Dict[str, Any]) -> str:
    """Compute a deterministic SHA-256 hash of structured data.

    Sorts keys recursively to ensure identical hashes for identical data
    regardless of insertion order.

    Args:
        data: Dictionary of data to hash.

    Returns:
        SHA-256 hex digest string.
    """
    canonical = json.dumps(data, sort_keys=True, default=str, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def compute_interest_hash(
    owner_name: str,
    interest_type: str,
    decimal_interest: str,
    well_name: str,
    effective_date: str,
) -> str:
    """Compute a deterministic hash for an interest record.

    This hash uniquely identifies a specific interest position for
    a given owner in a given well as of a given date.

    Args:
        owner_name: Owner name (normalized).
        interest_type: Interest type code (WI, RI, ORRI, etc.).
        decimal_interest: Decimal interest as string.
        well_name: Well or unit name.
        effective_date: Effective date as ISO string.

    Returns:
        SHA-256 hex digest string.
    """
    components = [
        owner_name.strip().upper(),
        interest_type.strip().upper(),
        decimal_interest.strip(),
        well_name.strip().upper(),
        effective_date.strip(),
    ]
    hash_input = "|".join(components)
    return hashlib.sha256(hash_input.encode("utf-8")).hexdigest()


def compute_pay_deck_hash(pay_deck_entries: List[Dict[str, Any]]) -> str:
    """Compute a deterministic hash for an entire pay deck.

    Args:
        pay_deck_entries: List of pay deck entry dictionaries.

    Returns:
        SHA-256 hex digest string.
    """
    sorted_entries = sorted(
        pay_deck_entries,
        key=lambda e: (e.get("owner_name", ""), e.get("interest_type", "")),
    )
    canonical = json.dumps(sorted_entries, sort_keys=True, default=str, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def compute_chain_hash(chain_events: List[Dict[str, Any]]) -> str:
    """Compute a hash-chain over sequential audit events.

    Each event's hash includes the hash of the previous event,
    creating a tamper-evident chain.

    Args:
        chain_events: List of event dictionaries in chronological order.

    Returns:
        Final chain hash (hex digest).
    """
    prev_hash = "0" * 64
    for event in chain_events:
        event_data = json.dumps(event, sort_keys=True, default=str, separators=(",", ":"))
        combined = prev_hash + event_data
        prev_hash = hashlib.sha256(combined.encode("utf-8")).hexdigest()
    return prev_hash


# ---------------------------------------------------------------------------
# Main Telemetry Class
# ---------------------------------------------------------------------------

class DivisionOrderTelemetry:
    """Comprehensive telemetry system for the LM03 Division Order Engine.

    Tracks metrics, operations, audit events, errors, and drift observations.
    Provides health monitoring and reporting capabilities.
    """

    def __init__(self, engine_id: str = "LM03", enabled: bool = True) -> None:
        """Initialize the telemetry system.

        Args:
            engine_id: The engine identifier.
            enabled: Whether telemetry collection is active.
        """
        self._engine_id = engine_id
        self._enabled = enabled
        self._start_time = datetime.utcnow()
        self._metrics: List[MetricPoint] = []
        self._active_operations: Dict[str, OperationTimer] = {}
        self._completed_operations: List[OperationTimer] = []
        self._audit_trail: List[AuditEvent] = []
        self._errors: List[ErrorRecord] = []
        self._drift_observations: List[DriftObservation] = []
        self._operation_counts: Dict[str, int] = defaultdict(int)
        self._operation_durations: Dict[str, List[float]] = defaultdict(list)
        self._total_queries: int = 0
        self._total_errors: int = 0
        self._session_id = uuid.uuid4().hex[:12]
        logger.info(
            "DivisionOrderTelemetry initialized | engine={eid} session={sid}",
            eid=engine_id,
            sid=self._session_id,
        )

    # -- Operation Tracking --------------------------------------------------

    def start_operation(
        self,
        operation_type: OperationType,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Start tracking a new operation.

        Args:
            operation_type: The type of operation being performed.
            metadata: Optional metadata about the operation.

        Returns:
            The generated operation_id.
        """
        operation_id = f"{self._engine_id}-{operation_type.value}-{uuid.uuid4().hex[:8]}"
        timer = OperationTimer(
            operation_id=operation_id,
            operation_type=operation_type,
            metadata=metadata or {},
        )
        self._active_operations[operation_id] = timer
        self._operation_counts[operation_type.value] += 1
        self._total_queries += 1
        logger.debug("Started operation {oid} type={otype}", oid=operation_id, otype=operation_type.value)
        return operation_id

    def complete_operation(
        self,
        operation_id: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> float:
        """Mark an operation as successfully completed.

        Args:
            operation_id: The operation ID returned from start_operation.
            metadata: Optional additional metadata.

        Returns:
            Duration in milliseconds.
        """
        timer = self._active_operations.pop(operation_id, None)
        if timer is None:
            logger.warning("Attempted to complete unknown operation {oid}", oid=operation_id)
            return 0.0
        duration = timer.complete(metadata)
        self._completed_operations.append(timer)
        self._operation_durations[timer.operation_type.value].append(duration)
        self._record_metric(
            f"operation_duration_{timer.operation_type.value}",
            MetricType.TIMER,
            duration,
        )
        return duration

    def fail_operation(self, operation_id: str, error: str) -> float:
        """Mark an operation as failed.

        Args:
            operation_id: The operation ID.
            error: Description of the error.

        Returns:
            Duration in milliseconds.
        """
        timer = self._active_operations.pop(operation_id, None)
        if timer is None:
            logger.warning("Attempted to fail unknown operation {oid}", oid=operation_id)
            return 0.0
        duration = timer.fail(error)
        self._completed_operations.append(timer)
        self._total_errors += 1
        self._record_metric(
            f"operation_error_{timer.operation_type.value}",
            MetricType.COUNTER,
            1.0,
        )
        return duration

    # -- Audit Trail ----------------------------------------------------------

    def record_audit_event(
        self,
        event_type: AuditEventType,
        description: str,
        operation_id: Optional[str] = None,
        user_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Record an immutable audit trail event.

        Args:
            event_type: The type of audit event.
            description: Human-readable description.
            operation_id: Optional associated operation ID.
            user_id: Optional user identifier.
            details: Optional additional detail dictionary.

        Returns:
            The generated event_id.
        """
        event_id = f"AUD-{uuid.uuid4().hex[:10]}"
        event_details = details or {}
        det_hash = compute_deterministic_hash({
            "event_id": event_id,
            "event_type": event_type.value,
            "description": description,
            "details": event_details,
        })
        event = AuditEvent(
            event_id=event_id,
            event_type=event_type,
            timestamp=datetime.utcnow(),
            operation_id=operation_id,
            user_id=user_id,
            description=description,
            details=event_details,
            deterministic_hash=det_hash,
        )
        self._audit_trail.append(event)
        logger.debug(
            "Audit event recorded: {etype} | {desc}",
            etype=event_type.value,
            desc=description[:80],
        )
        return event_id

    # -- Error Tracking -------------------------------------------------------

    def record_error(
        self,
        severity: ErrorSeverity,
        error_type: str,
        message: str,
        operation_type: Optional[OperationType] = None,
        stack_trace: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Record a tracked error.

        Args:
            severity: Error severity level.
            error_type: Classification of the error (e.g., ValueError).
            message: Human-readable error message.
            operation_type: Optional operation type where error occurred.
            stack_trace: Optional stack trace string.
            context: Optional contextual data.

        Returns:
            The generated error_id.
        """
        error_id = f"ERR-{uuid.uuid4().hex[:10]}"
        record = ErrorRecord(
            error_id=error_id,
            severity=severity,
            operation_type=operation_type,
            timestamp=datetime.utcnow(),
            error_type=error_type,
            message=message,
            stack_trace=stack_trace,
            context=context or {},
        )
        self._errors.append(record)
        self._total_errors += 1
        self._record_metric("error_count", MetricType.COUNTER, 1.0, {"severity": severity.value})
        log_func = logger.error if severity in (ErrorSeverity.FATAL, ErrorSeverity.ERROR) else logger.warning
        log_func(
            "Error [{sev}] {etype}: {msg}",
            sev=severity.value,
            etype=error_type,
            msg=message[:120],
        )
        return error_id

    # -- Drift Detection ------------------------------------------------------

    def record_drift(
        self,
        drift_type: DriftType,
        expected_value: float,
        actual_value: float,
        threshold: float,
        context: Optional[Dict[str, Any]] = None,
    ) -> Optional[str]:
        """Check for and record drift observations.

        Args:
            drift_type: The type of drift being measured.
            expected_value: The expected or baseline value.
            actual_value: The measured value.
            threshold: The acceptable deviation threshold.
            context: Optional additional context.

        Returns:
            Observation ID if drift is recorded, None if within tolerance.
        """
        deviation = abs(actual_value - expected_value)
        is_violation = deviation > threshold
        observation_id = f"DRF-{uuid.uuid4().hex[:10]}"
        observation = DriftObservation(
            observation_id=observation_id,
            drift_type=drift_type,
            timestamp=datetime.utcnow(),
            expected_value=expected_value,
            actual_value=actual_value,
            deviation=deviation,
            threshold=threshold,
            is_violation=is_violation,
            context=context or {},
        )
        self._drift_observations.append(observation)
        if is_violation:
            logger.warning(
                "DRIFT VIOLATION [{dtype}]: expected={exp}, actual={act}, deviation={dev}, threshold={thr}",
                dtype=drift_type.value,
                exp=expected_value,
                act=actual_value,
                dev=deviation,
                thr=threshold,
            )
            self.record_audit_event(
                AuditEventType.DRIFT_DETECTED,
                f"Drift violation: {drift_type.value} deviation={deviation:.8f} exceeds threshold={threshold:.8f}",
                details=observation.to_dict(),
            )
        return observation_id

    # -- Metrics Recording ----------------------------------------------------

    def _record_metric(
        self,
        name: str,
        metric_type: MetricType,
        value: float,
        labels: Optional[Dict[str, str]] = None,
    ) -> None:
        """Internal method to record a metric data point.

        Args:
            name: Metric name.
            metric_type: Type of metric.
            value: Metric value.
            labels: Optional label dictionary.
        """
        if not self._enabled:
            return
        point = MetricPoint(
            name=name,
            metric_type=metric_type,
            value=value,
            labels=labels or {},
        )
        self._metrics.append(point)

    def record_interest_calculation(
        self,
        owner_name: str,
        interest_type: str,
        decimal_value: str,
        well_name: str,
        duration_ms: float,
    ) -> None:
        """Record telemetry for an interest calculation.

        Args:
            owner_name: The owner name.
            interest_type: Interest type code.
            decimal_value: Computed decimal interest.
            well_name: Well or unit name.
            duration_ms: Calculation duration in ms.
        """
        self._record_metric(
            "interest_calculation",
            MetricType.TIMER,
            duration_ms,
            {"interest_type": interest_type, "well": well_name},
        )
        self.record_audit_event(
            AuditEventType.INTEREST_CALCULATED,
            f"Calculated {interest_type} for {owner_name} in {well_name}: {decimal_value}",
            details={
                "owner": owner_name,
                "type": interest_type,
                "decimal": decimal_value,
                "well": well_name,
                "duration_ms": round(duration_ms, 2),
            },
        )

    # -- Health Check ---------------------------------------------------------

    def health_check(self) -> Dict[str, Any]:
        """Return comprehensive telemetry health status.

        Returns:
            Dictionary with health metrics.
        """
        uptime = (datetime.utcnow() - self._start_time).total_seconds()
        error_rate = self._total_errors / max(self._total_queries, 1)
        avg_durations: Dict[str, float] = {}
        for op_type, durations in self._operation_durations.items():
            if durations:
                avg_durations[op_type] = round(statistics.mean(durations), 2)

        recent_errors = [
            e.to_dict() for e in self._errors[-5:]
        ]
        recent_drift = [
            d.to_dict() for d in self._drift_observations[-5:] if d.is_violation
        ]

        return {
            "status": "healthy" if error_rate < 0.10 else "degraded",
            "engine_id": self._engine_id,
            "session_id": self._session_id,
            "uptime_seconds": round(uptime, 1),
            "total_queries": self._total_queries,
            "total_errors": self._total_errors,
            "error_rate": round(error_rate, 4),
            "active_operations": len(self._active_operations),
            "completed_operations": len(self._completed_operations),
            "audit_trail_size": len(self._audit_trail),
            "drift_violations": sum(1 for d in self._drift_observations if d.is_violation),
            "operation_counts": dict(self._operation_counts),
            "avg_duration_ms": avg_durations,
            "recent_errors": recent_errors,
            "recent_drift_violations": recent_drift,
            "metrics_collected": len(self._metrics),
        }

    # -- Reporting ------------------------------------------------------------

    def get_session_summary(self) -> Dict[str, Any]:
        """Generate a session summary report.

        Returns:
            Dictionary with session-level aggregated metrics.
        """
        uptime = (datetime.utcnow() - self._start_time).total_seconds()
        all_durations = []
        for durations in self._operation_durations.values():
            all_durations.extend(durations)

        p50 = 0.0
        p95 = 0.0
        p99 = 0.0
        if all_durations:
            sorted_dur = sorted(all_durations)
            p50 = sorted_dur[int(len(sorted_dur) * 0.50)]
            p95 = sorted_dur[min(int(len(sorted_dur) * 0.95), len(sorted_dur) - 1)]
            p99 = sorted_dur[min(int(len(sorted_dur) * 0.99), len(sorted_dur) - 1)]

        return {
            "engine_id": self._engine_id,
            "session_id": self._session_id,
            "uptime_seconds": round(uptime, 1),
            "total_operations": self._total_queries,
            "total_errors": self._total_errors,
            "error_rate": round(self._total_errors / max(self._total_queries, 1), 4),
            "operations_per_minute": round(self._total_queries / max(uptime / 60.0, 0.01), 2),
            "latency_p50_ms": round(p50, 2),
            "latency_p95_ms": round(p95, 2),
            "latency_p99_ms": round(p99, 2),
            "operation_breakdown": dict(self._operation_counts),
            "drift_violations_total": sum(1 for d in self._drift_observations if d.is_violation),
            "audit_events_total": len(self._audit_trail),
        }

    def get_audit_trail(
        self,
        event_type: Optional[AuditEventType] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        """Retrieve audit trail events with optional filtering.

        Args:
            event_type: Optional filter by event type.
            limit: Maximum number of events to return.
            offset: Number of events to skip.

        Returns:
            List of audit event dictionaries.
        """
        filtered = self._audit_trail
        if event_type is not None:
            filtered = [e for e in filtered if e.event_type == event_type]
        page = filtered[offset:offset + limit]
        return [e.to_dict() for e in page]

    def get_errors(
        self,
        severity: Optional[ErrorSeverity] = None,
        resolved: Optional[bool] = None,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """Retrieve error records with optional filtering.

        Args:
            severity: Optional filter by severity.
            resolved: Optional filter by resolution status.
            limit: Maximum number of errors to return.

        Returns:
            List of error record dictionaries.
        """
        filtered = self._errors
        if severity is not None:
            filtered = [e for e in filtered if e.severity == severity]
        if resolved is not None:
            filtered = [e for e in filtered if e.resolved == resolved]
        return [e.to_dict() for e in filtered[-limit:]]

    def get_drift_observations(
        self,
        violations_only: bool = False,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """Retrieve drift observations.

        Args:
            violations_only: If True, only return violations.
            limit: Maximum number to return.

        Returns:
            List of drift observation dictionaries.
        """
        filtered = self._drift_observations
        if violations_only:
            filtered = [d for d in filtered if d.is_violation]
        return [d.to_dict() for d in filtered[-limit:]]

    def reset_session(self) -> None:
        """Reset all session metrics for a fresh start."""
        self._metrics.clear()
        self._active_operations.clear()
        self._completed_operations.clear()
        self._audit_trail.clear()
        self._errors.clear()
        self._drift_observations.clear()
        self._operation_counts.clear()
        self._operation_durations.clear()
        self._total_queries = 0
        self._total_errors = 0
        self._start_time = datetime.utcnow()
        self._session_id = uuid.uuid4().hex[:12]
        logger.info("Telemetry session reset | new session={sid}", sid=self._session_id)
