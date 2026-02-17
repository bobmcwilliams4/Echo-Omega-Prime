"""
LM13 Water Rights Analyzer - Telemetry Module
================================================

Comprehensive telemetry, metrics collection, audit trail, and performance
monitoring for the water rights analyzer engine.

Tracks analysis operations, compliance checks, search queries, error rates,
response times, and system health metrics. All telemetry is structured,
timestamped, and exportable.

Author: ECHO OMEGA PRIME Build System
Engine: LM13 v1.0.0
"""

from __future__ import annotations

import hashlib
import json
import statistics
import threading
import time
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Optional

from loguru import logger


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class OperationType(str, Enum):
    """Types of operations tracked by telemetry."""
    WATER_RIGHT_ANALYSIS = "water_right_analysis"
    GCD_RULE_LOOKUP = "gcd_rule_lookup"
    INJECTION_WELL_CHECK = "injection_well_check"
    COMPLIANCE_SCORING = "compliance_scoring"
    PERMIT_SEARCH = "permit_search"
    AQUIFER_SEARCH = "aquifer_search"
    OPERATOR_SEARCH = "operator_search"
    SPATIAL_SEARCH = "spatial_search"
    DOCTRINE_LOOKUP = "doctrine_lookup"
    SEMANTIC_SEARCH = "semantic_search"
    TERM_EXTRACTION = "term_extraction"
    RISK_ASSESSMENT = "risk_assessment"
    FRESHWATER_IDENTIFICATION = "freshwater_identification"
    TRANSPORT_ANALYSIS = "transport_analysis"
    MIT_COMPLIANCE_CHECK = "mit_compliance_check"
    SEISMICITY_REVIEW = "seismicity_review"
    PRODUCED_WATER_TRACKING = "produced_water_tracking"
    SURFACE_USE_ANALYSIS = "surface_use_analysis"
    EXPORT_REPORT = "export_report"
    HEALTH_CHECK = "health_check"


class MetricLevel(str, Enum):
    """Metric severity/importance level."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class AuditAction(str, Enum):
    """Types of auditable actions."""
    RECORD_CREATED = "record_created"
    RECORD_UPDATED = "record_updated"
    RECORD_DELETED = "record_deleted"
    SEARCH_EXECUTED = "search_executed"
    ANALYSIS_COMPLETED = "analysis_completed"
    COMPLIANCE_SCORED = "compliance_scored"
    RISK_FLAGGED = "risk_flagged"
    PERMIT_EXPIRY_ALERT = "permit_expiry_alert"
    MIT_OVERDUE_ALERT = "mit_overdue_alert"
    VIOLATION_DETECTED = "violation_detected"
    CONFIG_CHANGED = "config_changed"
    EXPORT_GENERATED = "export_generated"
    ENGINE_STARTED = "engine_started"
    ENGINE_STOPPED = "engine_stopped"
    ERROR_OCCURRED = "error_occurred"


# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------

@dataclass
class OperationMetric:
    """Single operation metric recording."""
    operation_id: str
    operation_type: OperationType
    timestamp: str
    duration_ms: float
    success: bool
    input_size: int = 0
    output_size: int = 0
    error_message: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def compute_hash(self) -> str:
        content = json.dumps({
            "id": self.operation_id,
            "type": self.operation_type.value,
            "timestamp": self.timestamp,
            "success": self.success,
        }, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()


@dataclass
class AuditEntry:
    """Single audit trail entry."""
    audit_id: str
    timestamp: str
    action: AuditAction
    actor: str
    resource_type: str
    resource_id: str
    details: str
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    ip_address: str = ""
    session_id: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def compute_hash(self) -> str:
        content = json.dumps({
            "id": self.audit_id,
            "action": self.action.value,
            "timestamp": self.timestamp,
            "resource": self.resource_id,
            "details": self.details,
        }, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()


@dataclass
class HealthStatus:
    """Engine health status snapshot."""
    timestamp: str
    engine_id: str = "LM13"
    engine_name: str = "Water Rights Analyzer"
    version: str = "1.0.0"
    status: str = "healthy"
    uptime_seconds: float = 0.0
    total_operations: int = 0
    total_errors: int = 0
    error_rate: float = 0.0
    avg_response_time_ms: float = 0.0
    p95_response_time_ms: float = 0.0
    p99_response_time_ms: float = 0.0
    records_indexed: int = 0
    doctrines_loaded: int = 0
    terms_loaded: int = 0
    memory_usage_mb: float = 0.0
    active_analyses: int = 0
    last_error: str = ""
    warnings: list[str] = field(default_factory=list)

    def is_healthy(self) -> bool:
        return self.status == "healthy" and self.error_rate < 0.1

    def to_dict(self) -> dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "engine_id": self.engine_id,
            "engine_name": self.engine_name,
            "version": self.version,
            "status": self.status,
            "uptime_seconds": self.uptime_seconds,
            "total_operations": self.total_operations,
            "total_errors": self.total_errors,
            "error_rate": round(self.error_rate, 4),
            "avg_response_time_ms": round(self.avg_response_time_ms, 2),
            "p95_response_time_ms": round(self.p95_response_time_ms, 2),
            "p99_response_time_ms": round(self.p99_response_time_ms, 2),
            "records_indexed": self.records_indexed,
            "doctrines_loaded": self.doctrines_loaded,
            "terms_loaded": self.terms_loaded,
            "memory_usage_mb": round(self.memory_usage_mb, 2),
            "active_analyses": self.active_analyses,
            "is_healthy": self.is_healthy(),
            "warnings": self.warnings,
        }


@dataclass
class AnalysisMetrics:
    """Aggregated metrics for analysis operations."""
    total_analyses: int = 0
    successful_analyses: int = 0
    failed_analyses: int = 0
    avg_duration_ms: float = 0.0
    min_duration_ms: float = 0.0
    max_duration_ms: float = 0.0
    p50_duration_ms: float = 0.0
    p95_duration_ms: float = 0.0
    p99_duration_ms: float = 0.0
    total_records_processed: int = 0
    total_compliance_checks: int = 0
    total_risk_flags: int = 0
    total_permits_analyzed: int = 0
    total_searches: int = 0
    operations_by_type: dict[str, int] = field(default_factory=dict)
    errors_by_type: dict[str, int] = field(default_factory=dict)
    avg_compliance_score: float = 0.0
    analysis_period_start: str = ""
    analysis_period_end: str = ""

    def error_rate(self) -> float:
        if self.total_analyses == 0:
            return 0.0
        return self.failed_analyses / self.total_analyses

    def success_rate(self) -> float:
        if self.total_analyses == 0:
            return 0.0
        return self.successful_analyses / self.total_analyses

    def to_dict(self) -> dict[str, Any]:
        return {
            "total_analyses": self.total_analyses,
            "successful": self.successful_analyses,
            "failed": self.failed_analyses,
            "success_rate": round(self.success_rate(), 4),
            "error_rate": round(self.error_rate(), 4),
            "avg_duration_ms": round(self.avg_duration_ms, 2),
            "p50_duration_ms": round(self.p50_duration_ms, 2),
            "p95_duration_ms": round(self.p95_duration_ms, 2),
            "p99_duration_ms": round(self.p99_duration_ms, 2),
            "total_records_processed": self.total_records_processed,
            "total_compliance_checks": self.total_compliance_checks,
            "total_risk_flags": self.total_risk_flags,
            "total_permits_analyzed": self.total_permits_analyzed,
            "total_searches": self.total_searches,
            "operations_by_type": self.operations_by_type,
            "errors_by_type": self.errors_by_type,
            "period": f"{self.analysis_period_start} to {self.analysis_period_end}",
        }


# ---------------------------------------------------------------------------
# Performance Monitor
# ---------------------------------------------------------------------------

class PerformanceMonitor:
    """Tracks operation performance metrics with sliding window."""

    def __init__(self, window_size: int = 1000) -> None:
        self._window_size = window_size
        self._durations: deque[float] = deque(maxlen=window_size)
        self._operation_counts: dict[str, int] = defaultdict(int)
        self._error_counts: dict[str, int] = defaultdict(int)
        self._active_operations: int = 0
        self._lock = threading.Lock()
        logger.info("PerformanceMonitor initialized (window_size={})", window_size)

    def record_operation(
        self,
        operation_type: OperationType,
        duration_ms: float,
        success: bool,
        error_type: str = "",
    ) -> None:
        """Record a completed operation."""
        with self._lock:
            self._durations.append(duration_ms)
            self._operation_counts[operation_type.value] += 1
            if not success and error_type:
                self._error_counts[error_type] += 1

    def start_operation(self) -> None:
        """Mark an operation as started."""
        with self._lock:
            self._active_operations += 1

    def end_operation(self) -> None:
        """Mark an operation as ended."""
        with self._lock:
            self._active_operations = max(0, self._active_operations - 1)

    def get_percentile(self, percentile: float) -> float:
        """Calculate a percentile from the duration window."""
        with self._lock:
            if not self._durations:
                return 0.0
            sorted_durations = sorted(self._durations)
            idx = int(len(sorted_durations) * percentile / 100.0)
            idx = min(idx, len(sorted_durations) - 1)
            return sorted_durations[idx]

    def get_average(self) -> float:
        """Get average duration from the window."""
        with self._lock:
            if not self._durations:
                return 0.0
            return statistics.mean(self._durations)

    def get_min(self) -> float:
        with self._lock:
            return min(self._durations) if self._durations else 0.0

    def get_max(self) -> float:
        with self._lock:
            return max(self._durations) if self._durations else 0.0

    def get_total_operations(self) -> int:
        with self._lock:
            return sum(self._operation_counts.values())

    def get_total_errors(self) -> int:
        with self._lock:
            return sum(self._error_counts.values())

    def get_active_operations(self) -> int:
        with self._lock:
            return self._active_operations

    def get_operation_counts(self) -> dict[str, int]:
        with self._lock:
            return dict(self._operation_counts)

    def get_error_counts(self) -> dict[str, int]:
        with self._lock:
            return dict(self._error_counts)

    def get_summary(self) -> dict[str, Any]:
        """Get complete performance summary."""
        return {
            "total_operations": self.get_total_operations(),
            "total_errors": self.get_total_errors(),
            "active_operations": self.get_active_operations(),
            "avg_duration_ms": round(self.get_average(), 2),
            "min_duration_ms": round(self.get_min(), 2),
            "max_duration_ms": round(self.get_max(), 2),
            "p50_duration_ms": round(self.get_percentile(50), 2),
            "p95_duration_ms": round(self.get_percentile(95), 2),
            "p99_duration_ms": round(self.get_percentile(99), 2),
            "window_size": self._window_size,
            "window_fill": len(self._durations),
            "operations_by_type": self.get_operation_counts(),
            "errors_by_type": self.get_error_counts(),
        }


# ---------------------------------------------------------------------------
# Compliance Tracker
# ---------------------------------------------------------------------------

class ComplianceTracker:
    """Tracks compliance scores and violations across analyzed records."""

    def __init__(self) -> None:
        self._scores: dict[str, float] = {}
        self._violations: dict[str, list[dict[str, Any]]] = defaultdict(list)
        self._risk_flags: dict[str, list[str]] = defaultdict(list)
        self._mit_status: dict[str, dict[str, Any]] = {}
        self._permit_expirations: dict[str, str] = {}
        self._lock = threading.Lock()
        logger.info("ComplianceTracker initialized")

    def record_score(self, record_id: str, score: float) -> None:
        """Record a compliance score for a record."""
        with self._lock:
            self._scores[record_id] = score
            if score < 40.0:
                logger.warning("CRITICAL compliance score for {}: {:.1f}", record_id, score)
            elif score < 60.0:
                logger.warning("HIGH risk compliance score for {}: {:.1f}", record_id, score)

    def record_violation(
        self,
        record_id: str,
        violation_type: str,
        description: str,
        severity: str = "moderate",
        date_detected: Optional[str] = None,
    ) -> None:
        """Record a compliance violation."""
        with self._lock:
            entry = {
                "type": violation_type,
                "description": description,
                "severity": severity,
                "date_detected": date_detected or datetime.now(timezone.utc).isoformat(),
            }
            self._violations[record_id].append(entry)
            logger.warning(
                "Violation recorded for {}: {} ({})", record_id, violation_type, severity
            )

    def flag_risk(self, record_id: str, risk_description: str) -> None:
        """Flag a compliance risk for a record."""
        with self._lock:
            self._risk_flags[record_id].append(risk_description)
            logger.info("Risk flagged for {}: {}", record_id, risk_description)

    def record_mit_status(
        self,
        well_id: str,
        last_test_date: str,
        result: str,
        next_due: str,
    ) -> None:
        """Record mechanical integrity test status."""
        with self._lock:
            self._mit_status[well_id] = {
                "last_test_date": last_test_date,
                "result": result,
                "next_due": next_due,
                "recorded_at": datetime.now(timezone.utc).isoformat(),
            }

    def record_permit_expiration(self, permit_id: str, expiration_date: str) -> None:
        """Track permit expiration for alerting."""
        with self._lock:
            self._permit_expirations[permit_id] = expiration_date

    def get_score(self, record_id: str) -> Optional[float]:
        with self._lock:
            return self._scores.get(record_id)

    def get_violations(self, record_id: str) -> list[dict[str, Any]]:
        with self._lock:
            return list(self._violations.get(record_id, []))

    def get_risk_flags(self, record_id: str) -> list[str]:
        with self._lock:
            return list(self._risk_flags.get(record_id, []))

    def get_all_violations(self) -> dict[str, list[dict[str, Any]]]:
        with self._lock:
            return dict(self._violations)

    def get_critical_records(self, threshold: float = 40.0) -> list[tuple[str, float]]:
        """Get records with compliance scores below threshold."""
        with self._lock:
            return [
                (rid, score)
                for rid, score in self._scores.items()
                if score < threshold
            ]

    def get_mit_overdue(self) -> list[tuple[str, dict[str, Any]]]:
        """Get wells with overdue MIT."""
        with self._lock:
            overdue: list[tuple[str, dict[str, Any]]] = []
            for well_id, status in self._mit_status.items():
                if status.get("result") == "overdue" or status.get("result") == "failed":
                    overdue.append((well_id, status))
            return overdue

    def get_summary(self) -> dict[str, Any]:
        """Get compliance tracking summary."""
        with self._lock:
            scores = list(self._scores.values())
            return {
                "total_scored": len(self._scores),
                "avg_score": round(statistics.mean(scores), 2) if scores else 0.0,
                "min_score": round(min(scores), 2) if scores else 0.0,
                "max_score": round(max(scores), 2) if scores else 0.0,
                "critical_count": sum(1 for s in scores if s < 40.0),
                "high_risk_count": sum(1 for s in scores if 40.0 <= s < 60.0),
                "moderate_risk_count": sum(1 for s in scores if 60.0 <= s < 80.0),
                "low_risk_count": sum(1 for s in scores if s >= 80.0),
                "total_violations": sum(len(v) for v in self._violations.values()),
                "records_with_violations": len(self._violations),
                "total_risk_flags": sum(len(f) for f in self._risk_flags.values()),
                "mit_tracked": len(self._mit_status),
                "mit_overdue": len(self.get_mit_overdue()),
                "permits_tracked": len(self._permit_expirations),
            }


# ---------------------------------------------------------------------------
# Audit Trail
# ---------------------------------------------------------------------------

class AuditTrail:
    """Append-only audit trail for all engine operations."""

    def __init__(self, max_entries: int = 100000) -> None:
        self._entries: deque[AuditEntry] = deque(maxlen=max_entries)
        self._hash_chain: list[str] = []
        self._counter: int = 0
        self._lock = threading.Lock()
        logger.info("AuditTrail initialized (max_entries={})", max_entries)

    def log(
        self,
        action: AuditAction,
        actor: str,
        resource_type: str,
        resource_id: str,
        details: str,
        old_value: Optional[str] = None,
        new_value: Optional[str] = None,
        session_id: str = "",
        metadata: Optional[dict[str, Any]] = None,
    ) -> str:
        """Record an audit entry. Returns audit_id."""
        with self._lock:
            self._counter += 1
            timestamp = datetime.now(timezone.utc).isoformat()
            audit_id = f"AUD-{self._counter:08d}"

            entry = AuditEntry(
                audit_id=audit_id,
                timestamp=timestamp,
                action=action,
                actor=actor,
                resource_type=resource_type,
                resource_id=resource_id,
                details=details,
                old_value=old_value,
                new_value=new_value,
                session_id=session_id,
                metadata=metadata or {},
            )

            # Compute hash chain for tamper detection
            entry_hash = entry.compute_hash()
            prev_hash = self._hash_chain[-1] if self._hash_chain else "GENESIS"
            chain_hash = hashlib.sha256(
                f"{prev_hash}|{entry_hash}".encode()
            ).hexdigest()
            self._hash_chain.append(chain_hash)

            self._entries.append(entry)
            logger.debug(
                "Audit: {} {} {} on {} ({})",
                action.value, actor, details[:60], resource_id, audit_id,
            )
            return audit_id

    def query(
        self,
        action: Optional[AuditAction] = None,
        actor: Optional[str] = None,
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        since: Optional[str] = None,
        limit: int = 100,
    ) -> list[AuditEntry]:
        """Query audit entries with optional filters."""
        with self._lock:
            results: list[AuditEntry] = []
            for entry in reversed(self._entries):
                if action and entry.action != action:
                    continue
                if actor and entry.actor != actor:
                    continue
                if resource_type and entry.resource_type != resource_type:
                    continue
                if resource_id and entry.resource_id != resource_id:
                    continue
                if since and entry.timestamp < since:
                    continue
                results.append(entry)
                if len(results) >= limit:
                    break
            return results

    def get_recent(self, limit: int = 50) -> list[AuditEntry]:
        """Get the most recent audit entries."""
        with self._lock:
            return list(reversed(list(self._entries)))[:limit]

    def verify_chain_integrity(self) -> bool:
        """Verify the hash chain has not been tampered with."""
        with self._lock:
            if not self._hash_chain:
                return True
            entries_list = list(self._entries)
            prev_hash = "GENESIS"
            for i, entry in enumerate(entries_list):
                if i >= len(self._hash_chain):
                    break
                entry_hash = entry.compute_hash()
                expected = hashlib.sha256(
                    f"{prev_hash}|{entry_hash}".encode()
                ).hexdigest()
                if expected != self._hash_chain[i]:
                    logger.error("Hash chain integrity failure at index {}", i)
                    return False
                prev_hash = self._hash_chain[i]
            return True

    def export(self, output_path: Path) -> int:
        """Export audit trail to JSON file."""
        with self._lock:
            export_data = {
                "exported_at": datetime.now(timezone.utc).isoformat(),
                "total_entries": len(self._entries),
                "chain_intact": self.verify_chain_integrity(),
                "entries": [
                    {
                        "audit_id": e.audit_id,
                        "timestamp": e.timestamp,
                        "action": e.action.value,
                        "actor": e.actor,
                        "resource_type": e.resource_type,
                        "resource_id": e.resource_id,
                        "details": e.details,
                        "session_id": e.session_id,
                    }
                    for e in self._entries
                ],
            }
            output_path.write_text(json.dumps(export_data, indent=2))
            logger.info("Exported {} audit entries to {}", len(self._entries), output_path)
            return len(self._entries)

    def get_statistics(self) -> dict[str, Any]:
        """Get audit trail statistics."""
        with self._lock:
            action_counts: dict[str, int] = defaultdict(int)
            actor_counts: dict[str, int] = defaultdict(int)
            for entry in self._entries:
                action_counts[entry.action.value] += 1
                actor_counts[entry.actor] += 1
            return {
                "total_entries": len(self._entries),
                "chain_length": len(self._hash_chain),
                "chain_intact": self.verify_chain_integrity(),
                "action_counts": dict(action_counts),
                "actor_counts": dict(actor_counts),
            }


# ---------------------------------------------------------------------------
# Master Telemetry
# ---------------------------------------------------------------------------

class WaterRightsTelemetry:
    """Master telemetry system for LM13 engine."""

    def __init__(self) -> None:
        self.performance = PerformanceMonitor(window_size=5000)
        self.compliance = ComplianceTracker()
        self.audit = AuditTrail(max_entries=100000)
        self._start_time = time.monotonic()
        self._operation_log: deque[OperationMetric] = deque(maxlen=10000)
        self._counter = 0
        self._lock = threading.Lock()
        logger.info("WaterRightsTelemetry system initialized")

        # Log engine start
        self.audit.log(
            action=AuditAction.ENGINE_STARTED,
            actor="system",
            resource_type="engine",
            resource_id="LM13",
            details="Water Rights Analyzer Engine started",
        )

    def record_operation(
        self,
        operation_type: OperationType,
        duration_ms: float,
        success: bool,
        input_size: int = 0,
        output_size: int = 0,
        error_message: str = "",
        metadata: Optional[dict[str, Any]] = None,
    ) -> str:
        """Record a completed operation. Returns operation_id."""
        with self._lock:
            self._counter += 1
            operation_id = f"OP-{self._counter:08d}"

        timestamp = datetime.now(timezone.utc).isoformat()
        metric = OperationMetric(
            operation_id=operation_id,
            operation_type=operation_type,
            timestamp=timestamp,
            duration_ms=duration_ms,
            success=success,
            input_size=input_size,
            output_size=output_size,
            error_message=error_message,
            metadata=metadata or {},
        )

        with self._lock:
            self._operation_log.append(metric)

        # Update performance monitor
        self.performance.record_operation(
            operation_type=operation_type,
            duration_ms=duration_ms,
            success=success,
            error_type=error_message[:50] if not success else "",
        )

        # Audit trail
        self.audit.log(
            action=AuditAction.ANALYSIS_COMPLETED if success else AuditAction.ERROR_OCCURRED,
            actor="engine",
            resource_type=operation_type.value,
            resource_id=operation_id,
            details=f"{'Success' if success else 'Failed'}: {operation_type.value} in {duration_ms:.1f}ms",
            metadata=metadata,
        )

        if not success:
            logger.warning(
                "Operation failed: {} ({}) - {}",
                operation_type.value, operation_id, error_message,
            )
        else:
            logger.debug(
                "Operation completed: {} ({}) in {:.1f}ms",
                operation_type.value, operation_id, duration_ms,
            )

        return operation_id

    def get_health(
        self,
        records_indexed: int = 0,
        doctrines_loaded: int = 0,
        terms_loaded: int = 0,
    ) -> HealthStatus:
        """Get current engine health status."""
        total_ops = self.performance.get_total_operations()
        total_errors = self.performance.get_total_errors()
        error_rate = total_errors / max(total_ops, 1)
        uptime = time.monotonic() - self._start_time

        warnings: list[str] = []
        status = "healthy"
        if error_rate > 0.1:
            status = "degraded"
            warnings.append(f"High error rate: {error_rate:.1%}")
        if error_rate > 0.25:
            status = "unhealthy"
        avg_response = self.performance.get_average()
        if avg_response > 5000:
            warnings.append(f"Slow average response time: {avg_response:.0f}ms")
            if status == "healthy":
                status = "degraded"

        last_error = ""
        with self._lock:
            for metric in reversed(self._operation_log):
                if not metric.success:
                    last_error = metric.error_message
                    break

        return HealthStatus(
            timestamp=datetime.now(timezone.utc).isoformat(),
            status=status,
            uptime_seconds=uptime,
            total_operations=total_ops,
            total_errors=total_errors,
            error_rate=error_rate,
            avg_response_time_ms=avg_response,
            p95_response_time_ms=self.performance.get_percentile(95),
            p99_response_time_ms=self.performance.get_percentile(99),
            records_indexed=records_indexed,
            doctrines_loaded=doctrines_loaded,
            terms_loaded=terms_loaded,
            active_analyses=self.performance.get_active_operations(),
            last_error=last_error,
            warnings=warnings,
        )

    def get_metrics(self) -> AnalysisMetrics:
        """Get aggregated analysis metrics."""
        with self._lock:
            operations = list(self._operation_log)

        if not operations:
            return AnalysisMetrics()

        durations = [op.duration_ms for op in operations]
        successful = [op for op in operations if op.success]
        failed = [op for op in operations if not op.success]

        ops_by_type: dict[str, int] = defaultdict(int)
        errors_by_type: dict[str, int] = defaultdict(int)
        for op in operations:
            ops_by_type[op.operation_type.value] += 1
            if not op.success:
                errors_by_type[op.operation_type.value] += 1

        sorted_durations = sorted(durations)
        p50_idx = int(len(sorted_durations) * 0.50)
        p95_idx = int(len(sorted_durations) * 0.95)
        p99_idx = int(len(sorted_durations) * 0.99)

        return AnalysisMetrics(
            total_analyses=len(operations),
            successful_analyses=len(successful),
            failed_analyses=len(failed),
            avg_duration_ms=statistics.mean(durations),
            min_duration_ms=min(durations),
            max_duration_ms=max(durations),
            p50_duration_ms=sorted_durations[min(p50_idx, len(sorted_durations) - 1)],
            p95_duration_ms=sorted_durations[min(p95_idx, len(sorted_durations) - 1)],
            p99_duration_ms=sorted_durations[min(p99_idx, len(sorted_durations) - 1)],
            total_records_processed=sum(op.input_size for op in operations),
            total_compliance_checks=ops_by_type.get(OperationType.COMPLIANCE_SCORING.value, 0),
            total_risk_flags=ops_by_type.get(OperationType.RISK_ASSESSMENT.value, 0),
            total_permits_analyzed=ops_by_type.get(OperationType.WATER_RIGHT_ANALYSIS.value, 0),
            total_searches=sum(
                v for k, v in ops_by_type.items()
                if "search" in k.lower()
            ),
            operations_by_type=dict(ops_by_type),
            errors_by_type=dict(errors_by_type),
            analysis_period_start=operations[0].timestamp if operations else "",
            analysis_period_end=operations[-1].timestamp if operations else "",
        )

    def get_recent_operations(self, limit: int = 50) -> list[OperationMetric]:
        """Get the most recent operations."""
        with self._lock:
            return list(reversed(list(self._operation_log)))[:limit]

    def export_telemetry(self, output_path: Path) -> dict[str, int]:
        """Export complete telemetry data to JSON file."""
        health = self.get_health()
        metrics = self.get_metrics()
        performance = self.performance.get_summary()
        compliance = self.compliance.get_summary()
        audit_stats = self.audit.get_statistics()

        export_data = {
            "exported_at": datetime.now(timezone.utc).isoformat(),
            "engine_id": "LM13",
            "health": health.to_dict(),
            "metrics": metrics.to_dict(),
            "performance": performance,
            "compliance": compliance,
            "audit": audit_stats,
            "recent_operations": [
                {
                    "id": op.operation_id,
                    "type": op.operation_type.value,
                    "timestamp": op.timestamp,
                    "duration_ms": round(op.duration_ms, 2),
                    "success": op.success,
                    "error": op.error_message,
                }
                for op in self.get_recent_operations(100)
            ],
        }

        output_path.write_text(json.dumps(export_data, indent=2))
        logger.info("Telemetry exported to {}", output_path)
        return {
            "operations": len(self._operation_log),
            "audit_entries": len(self.audit._entries),
            "compliance_records": len(self.compliance._scores),
        }

    def reset(self) -> None:
        """Reset all telemetry counters (for testing)."""
        with self._lock:
            self._operation_log.clear()
            self._counter = 0
        self.performance = PerformanceMonitor(window_size=5000)
        self.compliance = ComplianceTracker()
        self.audit = AuditTrail(max_entries=100000)
        self._start_time = time.monotonic()
        logger.info("Telemetry system reset")
