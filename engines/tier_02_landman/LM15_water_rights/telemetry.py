"""
LM15 Water Rights Engine - Telemetry Module
=============================================

Full telemetry, drift watcher, metrics collection, audit trail, and
performance monitoring for the LM15 Water Rights Engine.

Author: ECHO OMEGA PRIME Build System
Engine: LM15 v2.0.0
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
    WATER_RIGHT_ANALYSIS = "water_right_analysis"
    GCD_RULE_LOOKUP = "gcd_rule_lookup"
    INJECTION_WELL_CHECK = "injection_well_check"
    COMPLIANCE_SCORING = "compliance_scoring"
    PERMIT_SEARCH = "permit_search"
    AQUIFER_SEARCH = "aquifer_search"
    OPERATOR_SEARCH = "operator_search"
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
    DEPLETION_ASSESSMENT = "depletion_assessment"
    CONVEYANCE_ANALYSIS = "conveyance_analysis"
    EXPORT_REPORT = "export_report"
    HEALTH_CHECK = "health_check"
    DOCTRINE_INTEGRITY_CHECK = "doctrine_integrity_check"


class MetricLevel(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class AuditAction(str, Enum):
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
    DOCTRINE_DRIFT_DETECTED = "doctrine_drift_detected"
    INTEGRITY_CHECK_PASSED = "integrity_check_passed"
    INTEGRITY_CHECK_FAILED = "integrity_check_failed"


# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------

@dataclass
class OperationMetric:
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
            "ts": self.timestamp,
            "duration": self.duration_ms,
            "success": self.success,
        }, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()


@dataclass
class AuditEntry:
    entry_id: str
    action: AuditAction
    timestamp: str
    actor: str
    resource_type: str
    resource_id: str
    details: dict[str, Any] = field(default_factory=dict)
    previous_state: Optional[dict[str, Any]] = None
    new_state: Optional[dict[str, Any]] = None

    def compute_hash(self) -> str:
        content = json.dumps({
            "id": self.entry_id,
            "action": self.action.value,
            "ts": self.timestamp,
            "actor": self.actor,
            "resource": self.resource_id,
        }, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()


@dataclass
class DriftEvent:
    drift_id: str
    doctrine_id: str
    field_name: str
    expected_hash: str
    actual_hash: str
    timestamp: str
    severity: MetricLevel
    description: str


@dataclass
class HealthSnapshot:
    timestamp: str
    engine_id: str
    engine_version: str
    uptime_seconds: float
    total_operations: int
    error_count: int
    error_rate: float
    avg_latency_ms: float
    p95_latency_ms: float
    p99_latency_ms: float
    doctrine_count: int
    semantic_term_count: int
    memory_usage_mb: float
    active_connections: int
    drift_events_24h: int
    status: str


# ---------------------------------------------------------------------------
# Analysis Metrics
# ---------------------------------------------------------------------------

class AnalysisMetrics:
    """Collects and computes metrics for analysis operations."""

    def __init__(self, max_history: int = 10000) -> None:
        self._lock = threading.Lock()
        self._metrics: deque[OperationMetric] = deque(maxlen=max_history)
        self._counters: dict[str, int] = defaultdict(int)
        self._latencies: dict[str, list[float]] = defaultdict(list)
        self._errors: deque[OperationMetric] = deque(maxlen=1000)
        self._start_time = time.monotonic()
        logger.info("AnalysisMetrics initialized")

    def record(self, metric: OperationMetric) -> None:
        with self._lock:
            self._metrics.append(metric)
            op = metric.operation_type.value
            self._counters[op] += 1
            self._latencies[op].append(metric.duration_ms)
            if not metric.success:
                self._errors.append(metric)
                self._counters[f"{op}_errors"] += 1
        logger.debug(f"Metric recorded: {op} {metric.duration_ms:.1f}ms success={metric.success}")

    def get_summary(self) -> dict[str, Any]:
        with self._lock:
            total = len(self._metrics)
            errors = len(self._errors)
            all_latencies = [m.duration_ms for m in self._metrics]
            return {
                "total_operations": total,
                "error_count": errors,
                "error_rate": errors / total if total > 0 else 0.0,
                "uptime_seconds": time.monotonic() - self._start_time,
                "avg_latency_ms": statistics.mean(all_latencies) if all_latencies else 0.0,
                "p50_latency_ms": statistics.median(all_latencies) if all_latencies else 0.0,
                "p95_latency_ms": self._percentile(all_latencies, 95) if all_latencies else 0.0,
                "p99_latency_ms": self._percentile(all_latencies, 99) if all_latencies else 0.0,
                "max_latency_ms": max(all_latencies) if all_latencies else 0.0,
                "operations_by_type": dict(self._counters),
            }

    def get_type_stats(self, op_type: OperationType) -> dict[str, Any]:
        with self._lock:
            key = op_type.value
            lats = self._latencies.get(key, [])
            count = self._counters.get(key, 0)
            err_count = self._counters.get(f"{key}_errors", 0)
            return {
                "operation_type": key,
                "count": count,
                "error_count": err_count,
                "error_rate": err_count / count if count > 0 else 0.0,
                "avg_latency_ms": statistics.mean(lats) if lats else 0.0,
                "p95_latency_ms": self._percentile(lats, 95) if lats else 0.0,
                "min_latency_ms": min(lats) if lats else 0.0,
                "max_latency_ms": max(lats) if lats else 0.0,
            }

    def get_recent_errors(self, count: int = 10) -> list[dict[str, Any]]:
        with self._lock:
            errors = list(self._errors)[-count:]
            return [
                {
                    "operation_id": e.operation_id,
                    "type": e.operation_type.value,
                    "timestamp": e.timestamp,
                    "error": e.error_message,
                    "metadata": e.metadata,
                }
                for e in errors
            ]

    def reset(self) -> None:
        with self._lock:
            self._metrics.clear()
            self._counters.clear()
            self._latencies.clear()
            self._errors.clear()
            self._start_time = time.monotonic()
        logger.info("AnalysisMetrics reset")

    @staticmethod
    def _percentile(data: list[float], pct: float) -> float:
        if not data:
            return 0.0
        sorted_data = sorted(data)
        idx = int(len(sorted_data) * pct / 100.0)
        idx = min(idx, len(sorted_data) - 1)
        return sorted_data[idx]


# ---------------------------------------------------------------------------
# Audit Trail
# ---------------------------------------------------------------------------

class AuditTrail:
    """Immutable, hash-chained audit trail for all engine operations."""

    def __init__(self, max_entries: int = 50000) -> None:
        self._lock = threading.Lock()
        self._entries: deque[AuditEntry] = deque(maxlen=max_entries)
        self._chain_hash: str = hashlib.sha256(b"LM15_AUDIT_GENESIS").hexdigest()
        self._entry_count: int = 0
        logger.info("AuditTrail initialized with hash chain")

    def log(self, action: AuditAction, actor: str, resource_type: str,
            resource_id: str, details: Optional[dict[str, Any]] = None,
            previous_state: Optional[dict[str, Any]] = None,
            new_state: Optional[dict[str, Any]] = None) -> AuditEntry:
        with self._lock:
            self._entry_count += 1
            entry = AuditEntry(
                entry_id=f"AUDIT-LM15-{self._entry_count:08d}",
                action=action,
                timestamp=datetime.now(timezone.utc).isoformat(),
                actor=actor,
                resource_type=resource_type,
                resource_id=resource_id,
                details=details or {},
                previous_state=previous_state,
                new_state=new_state,
            )
            entry_hash = entry.compute_hash()
            chain_input = f"{self._chain_hash}:{entry_hash}"
            self._chain_hash = hashlib.sha256(chain_input.encode()).hexdigest()
            self._entries.append(entry)
        logger.debug(f"Audit: {action.value} on {resource_type}/{resource_id} by {actor}")
        return entry

    def get_entries(self, action: Optional[AuditAction] = None,
                    resource_type: Optional[str] = None,
                    limit: int = 100) -> list[AuditEntry]:
        with self._lock:
            entries = list(self._entries)
        if action:
            entries = [e for e in entries if e.action == action]
        if resource_type:
            entries = [e for e in entries if e.resource_type == resource_type]
        return entries[-limit:]

    def get_chain_hash(self) -> str:
        with self._lock:
            return self._chain_hash

    def verify_chain(self) -> dict[str, Any]:
        with self._lock:
            chain = hashlib.sha256(b"LM15_AUDIT_GENESIS").hexdigest()
            verified = 0
            for entry in self._entries:
                entry_hash = entry.compute_hash()
                chain_input = f"{chain}:{entry_hash}"
                chain = hashlib.sha256(chain_input.encode()).hexdigest()
                verified += 1
            matches = chain == self._chain_hash
        return {
            "entries_verified": verified,
            "chain_valid": matches,
            "expected_hash": self._chain_hash,
            "computed_hash": chain,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    @property
    def entry_count(self) -> int:
        with self._lock:
            return self._entry_count

    def export_json(self) -> list[dict[str, Any]]:
        with self._lock:
            return [
                {
                    "entry_id": e.entry_id,
                    "action": e.action.value,
                    "timestamp": e.timestamp,
                    "actor": e.actor,
                    "resource_type": e.resource_type,
                    "resource_id": e.resource_id,
                    "details": e.details,
                }
                for e in self._entries
            ]


# ---------------------------------------------------------------------------
# Drift Watcher
# ---------------------------------------------------------------------------

class DriftWatcher:
    """Monitors doctrine cache for unauthorized modifications (drift)."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._baseline_hashes: dict[str, str] = {}
        self._drift_events: deque[DriftEvent] = deque(maxlen=1000)
        self._drift_count: int = 0
        self._last_check: Optional[str] = None
        logger.info("DriftWatcher initialized")

    def set_baseline(self, doctrine_id: str, content_hash: str) -> None:
        with self._lock:
            self._baseline_hashes[doctrine_id] = content_hash
        logger.debug(f"Drift baseline set: {doctrine_id} -> {content_hash[:16]}...")

    def set_baseline_from_cache(self, cache: list[Any]) -> int:
        count = 0
        for doctrine in cache:
            doc_hash = doctrine.compute_hash()
            self.set_baseline(doctrine.doctrine_id, doc_hash)
            count += 1
        logger.info(f"Drift baseline set for {count} doctrines")
        return count

    def check(self, doctrine_id: str, current_hash: str) -> Optional[DriftEvent]:
        with self._lock:
            baseline = self._baseline_hashes.get(doctrine_id)
            if baseline is None:
                return None
            if current_hash == baseline:
                return None
            self._drift_count += 1
            event = DriftEvent(
                drift_id=f"DRIFT-LM15-{self._drift_count:06d}",
                doctrine_id=doctrine_id,
                field_name="content_hash",
                expected_hash=baseline,
                actual_hash=current_hash,
                timestamp=datetime.now(timezone.utc).isoformat(),
                severity=MetricLevel.WARNING,
                description=f"Doctrine {doctrine_id} content hash changed from {baseline[:16]}... to {current_hash[:16]}...",
            )
            self._drift_events.append(event)
        logger.warning(f"DRIFT DETECTED: {event.description}")
        return event

    def check_all(self, cache: list[Any]) -> list[DriftEvent]:
        events: list[DriftEvent] = []
        for doctrine in cache:
            current_hash = doctrine.compute_hash()
            event = self.check(doctrine.doctrine_id, current_hash)
            if event:
                events.append(event)
        with self._lock:
            self._last_check = datetime.now(timezone.utc).isoformat()
        if events:
            logger.warning(f"Drift check found {len(events)} changes across {len(cache)} doctrines")
        else:
            logger.info(f"Drift check: {len(cache)} doctrines verified, no drift detected")
        return events

    def get_drift_summary(self) -> dict[str, Any]:
        with self._lock:
            return {
                "total_baselines": len(self._baseline_hashes),
                "total_drift_events": self._drift_count,
                "recent_events": [
                    {
                        "drift_id": e.drift_id,
                        "doctrine_id": e.doctrine_id,
                        "timestamp": e.timestamp,
                        "severity": e.severity.value,
                        "description": e.description,
                    }
                    for e in list(self._drift_events)[-10:]
                ],
                "last_check": self._last_check,
            }


# ---------------------------------------------------------------------------
# Performance Monitor
# ---------------------------------------------------------------------------

class PerformanceMonitor:
    """Monitors engine performance and detects anomalies."""

    def __init__(self, latency_threshold_ms: float = 5000.0, error_rate_threshold: float = 0.05) -> None:
        self._latency_threshold = latency_threshold_ms
        self._error_rate_threshold = error_rate_threshold
        self._lock = threading.Lock()
        self._alerts: deque[dict[str, Any]] = deque(maxlen=500)
        self._windows: dict[str, deque[float]] = defaultdict(lambda: deque(maxlen=100))
        logger.info(f"PerformanceMonitor: latency_threshold={latency_threshold_ms}ms, error_rate_threshold={error_rate_threshold}")

    def check_latency(self, operation: str, latency_ms: float) -> Optional[dict[str, Any]]:
        with self._lock:
            self._windows[operation].append(latency_ms)
        if latency_ms > self._latency_threshold:
            alert = {
                "type": "high_latency",
                "operation": operation,
                "latency_ms": latency_ms,
                "threshold_ms": self._latency_threshold,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "level": MetricLevel.WARNING.value,
            }
            with self._lock:
                self._alerts.append(alert)
            logger.warning(f"High latency alert: {operation} took {latency_ms:.1f}ms (threshold: {self._latency_threshold}ms)")
            return alert
        return None

    def check_error_rate(self, metrics: AnalysisMetrics) -> Optional[dict[str, Any]]:
        summary = metrics.get_summary()
        error_rate = summary.get("error_rate", 0.0)
        if error_rate > self._error_rate_threshold:
            alert = {
                "type": "high_error_rate",
                "error_rate": error_rate,
                "threshold": self._error_rate_threshold,
                "total_operations": summary["total_operations"],
                "error_count": summary["error_count"],
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "level": MetricLevel.ERROR.value,
            }
            with self._lock:
                self._alerts.append(alert)
            logger.error(f"High error rate alert: {error_rate:.3f} (threshold: {self._error_rate_threshold})")
            return alert
        return None

    def get_alerts(self, limit: int = 50) -> list[dict[str, Any]]:
        with self._lock:
            return list(self._alerts)[-limit:]

    def get_operation_trends(self) -> dict[str, dict[str, float]]:
        with self._lock:
            trends: dict[str, dict[str, float]] = {}
            for op, window in self._windows.items():
                data = list(window)
                if data:
                    trends[op] = {
                        "avg_ms": statistics.mean(data),
                        "p95_ms": sorted(data)[int(len(data) * 0.95)] if len(data) >= 20 else max(data),
                        "samples": len(data),
                        "min_ms": min(data),
                        "max_ms": max(data),
                    }
            return trends


# ---------------------------------------------------------------------------
# Main Telemetry Facade
# ---------------------------------------------------------------------------

class WaterRightsTelemetry:
    """Unified telemetry interface for the LM15 Water Rights Engine."""

    def __init__(self, engine_id: str = "LM15", engine_version: str = "2.0.0") -> None:
        self.engine_id = engine_id
        self.engine_version = engine_version
        self.metrics = AnalysisMetrics()
        self.audit = AuditTrail()
        self.drift_watcher = DriftWatcher()
        self.performance = PerformanceMonitor()
        self._start_time = time.monotonic()
        self._operation_counter = 0
        self._lock = threading.Lock()
        self.audit.log(AuditAction.ENGINE_STARTED, "system", "engine", engine_id,
                       {"version": engine_version, "timestamp": datetime.now(timezone.utc).isoformat()})
        logger.info(f"WaterRightsTelemetry initialized for {engine_id} v{engine_version}")

    def record_operation(self, operation_type: OperationType, duration_ms: float,
                         success: bool, input_size: int = 0, output_size: int = 0,
                         error_message: str = "", metadata: Optional[dict[str, Any]] = None) -> str:
        with self._lock:
            self._operation_counter += 1
            op_id = f"OP-LM15-{self._operation_counter:08d}"
        metric = OperationMetric(
            operation_id=op_id,
            operation_type=operation_type,
            timestamp=datetime.now(timezone.utc).isoformat(),
            duration_ms=duration_ms,
            success=success,
            input_size=input_size,
            output_size=output_size,
            error_message=error_message,
            metadata=metadata or {},
        )
        self.metrics.record(metric)
        self.performance.check_latency(operation_type.value, duration_ms)
        if not success:
            self.audit.log(AuditAction.ERROR_OCCURRED, "system", "operation", op_id,
                           {"type": operation_type.value, "error": error_message})
        return op_id

    def log_audit(self, action: AuditAction, actor: str, resource_type: str,
                  resource_id: str, details: Optional[dict[str, Any]] = None) -> AuditEntry:
        return self.audit.log(action, actor, resource_type, resource_id, details)

    def check_doctrine_drift(self, cache: list[Any]) -> list[Any]:
        return self.drift_watcher.check_all(cache)

    def set_doctrine_baseline(self, cache: list[Any]) -> int:
        return self.drift_watcher.set_baseline_from_cache(cache)

    def get_health(self) -> HealthSnapshot:
        summary = self.metrics.get_summary()
        drift_summary = self.drift_watcher.get_drift_summary()
        uptime = time.monotonic() - self._start_time
        error_rate = summary.get("error_rate", 0.0)
        status = "healthy"
        if error_rate > 0.1:
            status = "degraded"
        elif error_rate > 0.25:
            status = "unhealthy"
        return HealthSnapshot(
            timestamp=datetime.now(timezone.utc).isoformat(),
            engine_id=self.engine_id,
            engine_version=self.engine_version,
            uptime_seconds=uptime,
            total_operations=summary["total_operations"],
            error_count=summary["error_count"],
            error_rate=error_rate,
            avg_latency_ms=summary["avg_latency_ms"],
            p95_latency_ms=summary["p95_latency_ms"],
            p99_latency_ms=summary["p99_latency_ms"],
            doctrine_count=drift_summary["total_baselines"],
            semantic_term_count=0,
            memory_usage_mb=0.0,
            active_connections=0,
            drift_events_24h=drift_summary["total_drift_events"],
            status=status,
        )

    def export_telemetry(self) -> dict[str, Any]:
        return {
            "engine_id": self.engine_id,
            "engine_version": self.engine_version,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "metrics_summary": self.metrics.get_summary(),
            "audit_chain_hash": self.audit.get_chain_hash(),
            "audit_entry_count": self.audit.entry_count,
            "drift_summary": self.drift_watcher.get_drift_summary(),
            "performance_alerts": self.performance.get_alerts(20),
            "performance_trends": self.performance.get_operation_trends(),
            "recent_errors": self.metrics.get_recent_errors(10),
        }

    def shutdown(self) -> None:
        self.audit.log(AuditAction.ENGINE_STOPPED, "system", "engine", self.engine_id,
                       {"uptime_seconds": time.monotonic() - self._start_time})
        logger.info(f"WaterRightsTelemetry shutdown for {self.engine_id}")
