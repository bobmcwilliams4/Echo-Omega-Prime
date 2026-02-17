"""
LM05 Chain of Title Builder - Telemetry Module
=================================================
ECHO OMEGA PRIME - Landman Intelligence Division

Performance metrics, audit trail, and deterministic hashing for
the chain of title builder engine.

Features:
- Operation timing and throughput tracking
- Chain construction metrics (links validated, gaps found, branches created)
- Search performance metrics (queries/sec, hit rates)
- Error tracking with classification
- Deterministic SHA-256 hashing for response integrity
- Audit trail for all chain operations
- Health check endpoint data
- Export to JSON for monitoring integration

Authority: Bobby Don McWilliams II (11.0 SUPREME SOVEREIGN)
"""

from __future__ import annotations

import hashlib
import json
import threading
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from loguru import logger
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

TELEMETRY_DIR = Path("O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/LM05_chain_of_title/telemetry_data")
METRICS_INTERVAL_SECONDS = 60
MAX_AUDIT_ENTRIES = 10000
MAX_ERROR_ENTRIES = 5000


# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------

class OperationMetric(BaseModel):
    """Metric for a single timed operation."""
    operation: str = Field(..., description="Operation name")
    start_time: str = Field(..., description="ISO-8601 start timestamp")
    end_time: Optional[str] = Field(default=None, description="ISO-8601 end timestamp")
    duration_ms: float = Field(default=0.0, description="Duration in milliseconds")
    success: bool = Field(default=True, description="Whether operation succeeded")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    error: Optional[str] = Field(default=None, description="Error message if failed")


class ChainMetrics(BaseModel):
    """Metrics specific to chain construction operations."""
    chains_built: int = 0
    total_links_validated: int = 0
    total_gaps_detected: int = 0
    total_branches_created: int = 0
    total_mergers_detected: int = 0
    total_wild_deeds_found: int = 0
    total_instruments_processed: int = 0
    avg_chain_depth: float = 0.0
    avg_chain_confidence: float = 0.0
    max_chain_depth: int = 0
    max_branch_factor: int = 0
    sovereign_roots_found: int = 0
    gap_cure_rate: float = 0.0
    chains_by_county: Dict[str, int] = Field(default_factory=dict)
    gaps_by_type: Dict[str, int] = Field(default_factory=dict)
    links_by_instrument_type: Dict[str, int] = Field(default_factory=dict)


class SearchMetrics(BaseModel):
    """Metrics specific to search operations."""
    total_queries: int = 0
    total_results_returned: int = 0
    avg_query_time_ms: float = 0.0
    max_query_time_ms: float = 0.0
    min_query_time_ms: float = 999999.0
    queries_per_second: float = 0.0
    cache_hit_rate: float = 0.0
    fuzzy_match_rate: float = 0.0
    soundex_match_rate: float = 0.0
    queries_by_type: Dict[str, int] = Field(default_factory=dict)
    avg_results_per_query: float = 0.0


class ErrorEntry(BaseModel):
    """A recorded error event."""
    timestamp: str = Field(..., description="ISO-8601 timestamp")
    operation: str = Field(default="", description="Operation that failed")
    error_type: str = Field(default="", description="Error classification")
    error_message: str = Field(default="", description="Error message")
    stack_trace: Optional[str] = Field(default=None, description="Stack trace")
    severity: str = Field(default="MEDIUM", description="LOW, MEDIUM, HIGH, CRITICAL")
    resolved: bool = Field(default=False, description="Whether error was resolved")
    resolution: Optional[str] = Field(default=None, description="How it was resolved")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional context")


class AuditEntry(BaseModel):
    """An audit trail entry for chain operations."""
    timestamp: str = Field(..., description="ISO-8601 timestamp")
    operation: str = Field(..., description="Operation performed")
    entity: str = Field(default="", description="Entity affected (chain ID, record ID, etc.)")
    action: str = Field(default="", description="Action taken")
    details: str = Field(default="", description="Human-readable details")
    user: str = Field(default="system", description="User or system that triggered")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional context")
    deterministic_hash: str = Field(default="", description="SHA-256 hash of entry")


class HealthStatus(BaseModel):
    """Health check status for the engine."""
    status: str = Field(default="unknown", description="healthy, degraded, unhealthy, unknown")
    uptime_seconds: float = Field(default=0.0, description="Engine uptime")
    last_check: str = Field(default="", description="Last health check timestamp")
    components: Dict[str, str] = Field(default_factory=dict, description="Component statuses")
    metrics_summary: Dict[str, Any] = Field(default_factory=dict, description="Key metrics")
    errors_last_hour: int = Field(default=0, description="Errors in the last hour")
    version: str = Field(default="1.0.0", description="Engine version")
    engine_id: str = Field(default="LM05", description="Engine identifier")


class TelemetrySummary(BaseModel):
    """Complete telemetry summary for export."""
    engine_id: str = "LM05"
    engine_name: str = "Chain of Title Builder"
    version: str = "1.0.0"
    generated_at: str = ""
    uptime_seconds: float = 0.0
    chain_metrics: ChainMetrics = Field(default_factory=ChainMetrics)
    search_metrics: SearchMetrics = Field(default_factory=SearchMetrics)
    operation_counts: Dict[str, int] = Field(default_factory=dict)
    operation_avg_times: Dict[str, float] = Field(default_factory=dict)
    error_counts: Dict[str, int] = Field(default_factory=dict)
    total_errors: int = 0
    total_operations: int = 0
    health: HealthStatus = Field(default_factory=HealthStatus)
    deterministic_hash: str = ""


# ---------------------------------------------------------------------------
# Timer context manager
# ---------------------------------------------------------------------------

class OperationTimer:
    """Context manager for timing operations."""

    def __init__(self, telemetry: ChainOfTitleTelemetry, operation: str,
                 metadata: Optional[Dict[str, Any]] = None) -> None:
        self._telemetry = telemetry
        self._operation = operation
        self._metadata = metadata or {}
        self._start: float = 0.0
        self._metric: Optional[OperationMetric] = None

    def __enter__(self) -> OperationTimer:
        self._start = time.perf_counter()
        self._metric = OperationMetric(
            operation=self._operation,
            start_time=datetime.now(timezone.utc).isoformat(),
            metadata=self._metadata,
        )
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        elapsed_ms = (time.perf_counter() - self._start) * 1000
        if self._metric:
            self._metric.end_time = datetime.now(timezone.utc).isoformat()
            self._metric.duration_ms = round(elapsed_ms, 3)
            self._metric.success = exc_type is None
            if exc_val:
                self._metric.error = str(exc_val)
            self._telemetry.record_operation(self._metric)

    def set_metadata(self, key: str, value: Any) -> None:
        """Add metadata to the operation metric."""
        self._metadata[key] = value
        if self._metric:
            self._metric.metadata[key] = value


# ---------------------------------------------------------------------------
# Telemetry manager
# ---------------------------------------------------------------------------

class ChainOfTitleTelemetry:
    """Telemetry system for the LM05 Chain of Title Builder engine.

    Tracks performance metrics, maintains audit trail, records errors,
    and generates deterministic hashes for response integrity.
    """

    def __init__(self) -> None:
        self._start_time = time.time()
        self._lock = threading.Lock()

        self._chain_metrics = ChainMetrics()
        self._search_metrics = SearchMetrics()

        self._operation_times: Dict[str, List[float]] = defaultdict(list)
        self._operation_counts: Dict[str, int] = defaultdict(int)

        self._errors: List[ErrorEntry] = []
        self._audit_trail: List[AuditEntry] = []
        self._recent_operations: List[OperationMetric] = []

        self._error_counts: Dict[str, int] = defaultdict(int)

        self._component_status: Dict[str, str] = {
            "doctrine_cache": "unknown",
            "semantic_dictionary": "unknown",
            "search_engine": "unknown",
            "chain_builder": "unknown",
            "gap_detector": "unknown",
            "telemetry": "healthy",
        }

        TELEMETRY_DIR.mkdir(parents=True, exist_ok=True)
        logger.info("ChainOfTitleTelemetry initialized")

    # -- operation tracking --

    def record_operation(self, metric: OperationMetric) -> None:
        """Record a completed operation metric."""
        with self._lock:
            self._operation_counts[metric.operation] += 1
            self._operation_times[metric.operation].append(metric.duration_ms)

            if len(self._operation_times[metric.operation]) > 1000:
                self._operation_times[metric.operation] = self._operation_times[metric.operation][-500:]

            self._recent_operations.append(metric)
            if len(self._recent_operations) > 500:
                self._recent_operations = self._recent_operations[-250:]

            if not metric.success and metric.error:
                self.record_error(
                    operation=metric.operation,
                    error_type="OPERATION_FAILURE",
                    error_message=metric.error,
                    severity="MEDIUM",
                    metadata=metric.metadata,
                )

    def time_operation(self, operation: str,
                       metadata: Optional[Dict[str, Any]] = None) -> OperationTimer:
        """Create a timer context manager for an operation."""
        return OperationTimer(self, operation, metadata)

    # -- chain metrics --

    def record_chain_built(self, chain_id: str, depth: int, confidence: float,
                           county: str = "", links: int = 0, branches: int = 0,
                           gaps: int = 0, mergers: int = 0) -> None:
        """Record metrics for a completed chain construction."""
        with self._lock:
            m = self._chain_metrics
            m.chains_built += 1
            m.total_links_validated += links
            m.total_branches_created += branches
            m.total_gaps_detected += gaps
            m.total_mergers_detected += mergers

            if depth > m.max_chain_depth:
                m.max_chain_depth = depth
            if branches > m.max_branch_factor:
                m.max_branch_factor = branches

            total_depth = m.avg_chain_depth * (m.chains_built - 1) + depth
            m.avg_chain_depth = total_depth / m.chains_built

            total_conf = m.avg_chain_confidence * (m.chains_built - 1) + confidence
            m.avg_chain_confidence = total_conf / m.chains_built

            if county:
                m.chains_by_county[county] = m.chains_by_county.get(county, 0) + 1

        self.audit("chain_built", chain_id, "BUILD",
                   f"Chain built: depth={depth}, confidence={confidence:.3f}, "
                   f"links={links}, gaps={gaps}, branches={branches}")

    def record_gap_detected(self, gap_type: str, chain_id: str = "", severity: str = "MEDIUM") -> None:
        """Record a detected gap in the chain."""
        with self._lock:
            self._chain_metrics.total_gaps_detected += 1
            self._chain_metrics.gaps_by_type[gap_type] = \
                self._chain_metrics.gaps_by_type.get(gap_type, 0) + 1

        self.audit("gap_detected", chain_id, "DETECT",
                   f"Gap detected: type={gap_type}, severity={severity}")

    def record_wild_deed(self, record_id: str = "", chain_id: str = "") -> None:
        """Record a wild deed detection."""
        with self._lock:
            self._chain_metrics.total_wild_deeds_found += 1

        self.audit("wild_deed_found", record_id, "DETECT",
                   f"Wild deed detected in chain {chain_id}")

    def record_sovereign_root(self, patent_info: str = "") -> None:
        """Record a sovereign root found."""
        with self._lock:
            self._chain_metrics.sovereign_roots_found += 1

        self.audit("sovereign_root_found", patent_info, "DETECT",
                   f"Sovereign root identified: {patent_info}")

    def record_instrument_processed(self, instrument_type: str) -> None:
        """Record an instrument being processed into the chain."""
        with self._lock:
            self._chain_metrics.total_instruments_processed += 1
            self._chain_metrics.links_by_instrument_type[instrument_type] = \
                self._chain_metrics.links_by_instrument_type.get(instrument_type, 0) + 1

    # -- search metrics --

    def record_search(self, query_type: str, result_count: int, duration_ms: float,
                      fuzzy_used: bool = False, soundex_used: bool = False) -> None:
        """Record a search operation."""
        with self._lock:
            m = self._search_metrics
            m.total_queries += 1
            m.total_results_returned += result_count
            m.avg_results_per_query = m.total_results_returned / m.total_queries

            total_time = m.avg_query_time_ms * (m.total_queries - 1) + duration_ms
            m.avg_query_time_ms = total_time / m.total_queries

            if duration_ms > m.max_query_time_ms:
                m.max_query_time_ms = duration_ms
            if duration_ms < m.min_query_time_ms:
                m.min_query_time_ms = duration_ms

            elapsed_total = time.time() - self._start_time
            if elapsed_total > 0:
                m.queries_per_second = m.total_queries / elapsed_total

            m.queries_by_type[query_type] = m.queries_by_type.get(query_type, 0) + 1

            if fuzzy_used:
                total_fuzzy = m.fuzzy_match_rate * (m.total_queries - 1) + 1.0
                m.fuzzy_match_rate = total_fuzzy / m.total_queries
            if soundex_used:
                total_soundex = m.soundex_match_rate * (m.total_queries - 1) + 1.0
                m.soundex_match_rate = total_soundex / m.total_queries

    # -- error tracking --

    def record_error(self, operation: str, error_type: str, error_message: str,
                     severity: str = "MEDIUM", stack_trace: Optional[str] = None,
                     metadata: Optional[Dict[str, Any]] = None) -> None:
        """Record an error event."""
        entry = ErrorEntry(
            timestamp=datetime.now(timezone.utc).isoformat(),
            operation=operation,
            error_type=error_type,
            error_message=error_message,
            stack_trace=stack_trace,
            severity=severity,
            metadata=metadata or {},
        )

        with self._lock:
            self._errors.append(entry)
            if len(self._errors) > MAX_ERROR_ENTRIES:
                self._errors = self._errors[-MAX_ERROR_ENTRIES // 2:]
            self._error_counts[error_type] = self._error_counts.get(error_type, 0) + 1

        log_msg = f"[{severity}] {operation}: {error_type} - {error_message}"
        if severity in ("CRITICAL", "HIGH"):
            logger.error(log_msg)
        elif severity == "MEDIUM":
            logger.warning(log_msg)
        else:
            logger.info(log_msg)

    def resolve_error(self, error_index: int, resolution: str) -> bool:
        """Mark an error as resolved."""
        with self._lock:
            if 0 <= error_index < len(self._errors):
                self._errors[error_index].resolved = True
                self._errors[error_index].resolution = resolution
                return True
        return False

    # -- audit trail --

    def audit(self, operation: str, entity: str, action: str,
              details: str, user: str = "system",
              metadata: Optional[Dict[str, Any]] = None) -> str:
        """Add an entry to the audit trail. Returns the hash."""
        entry = AuditEntry(
            timestamp=datetime.now(timezone.utc).isoformat(),
            operation=operation,
            entity=entity,
            action=action,
            details=details,
            user=user,
            metadata=metadata or {},
        )

        hash_content = f"{entry.timestamp}|{entry.operation}|{entry.entity}|{entry.action}|{entry.details}"
        entry.deterministic_hash = hashlib.sha256(hash_content.encode("utf-8")).hexdigest()

        with self._lock:
            self._audit_trail.append(entry)
            if len(self._audit_trail) > MAX_AUDIT_ENTRIES:
                self._audit_trail = self._audit_trail[-MAX_AUDIT_ENTRIES // 2:]

        return entry.deterministic_hash

    # -- component status --

    def set_component_status(self, component: str, status: str) -> None:
        """Set the health status of a component."""
        with self._lock:
            self._component_status[component] = status

    # -- deterministic hashing --

    def compute_response_hash(self, response_data: Any) -> str:
        """Compute a deterministic SHA-256 hash for a response."""
        if isinstance(response_data, BaseModel):
            content = response_data.model_dump_json(exclude_none=True)
        elif isinstance(response_data, dict):
            content = json.dumps(response_data, sort_keys=True, default=str)
        elif isinstance(response_data, str):
            content = response_data
        else:
            content = str(response_data)

        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def compute_chain_hash(self, chain_data: Dict[str, Any]) -> str:
        """Compute a deterministic hash for an entire chain of title."""
        hasher = hashlib.sha256()

        links = chain_data.get("links", [])
        for link in sorted(links, key=lambda x: x.get("recording_date", "")):
            link_str = json.dumps(link, sort_keys=True, default=str)
            hasher.update(link_str.encode("utf-8"))

        hasher.update(json.dumps(chain_data.get("metadata", {}), sort_keys=True, default=str).encode("utf-8"))
        return hasher.hexdigest()

    # -- health check --

    def health_check(self) -> HealthStatus:
        """Perform a health check and return status."""
        with self._lock:
            uptime = time.time() - self._start_time
            now = datetime.now(timezone.utc)

            errors_last_hour = 0
            one_hour_ago = now.timestamp() - 3600
            for error in reversed(self._errors):
                try:
                    error_ts = datetime.fromisoformat(error.timestamp.replace("Z", "+00:00")).timestamp()
                    if error_ts >= one_hour_ago:
                        errors_last_hour += 1
                    else:
                        break
                except (ValueError, TypeError):
                    continue

            all_healthy = all(s == "healthy" for s in self._component_status.values())
            any_unhealthy = any(s == "unhealthy" for s in self._component_status.values())

            if any_unhealthy:
                overall_status = "unhealthy"
            elif not all_healthy:
                overall_status = "degraded"
            elif errors_last_hour > 10:
                overall_status = "degraded"
            else:
                overall_status = "healthy"

            total_ops = sum(self._operation_counts.values())
            total_errors = sum(self._error_counts.values())
            error_rate = total_errors / max(1, total_ops)

            return HealthStatus(
                status=overall_status,
                uptime_seconds=round(uptime, 1),
                last_check=now.isoformat(),
                components=dict(self._component_status),
                metrics_summary={
                    "total_operations": total_ops,
                    "total_errors": total_errors,
                    "error_rate": round(error_rate, 4),
                    "chains_built": self._chain_metrics.chains_built,
                    "total_queries": self._search_metrics.total_queries,
                    "avg_query_time_ms": round(self._search_metrics.avg_query_time_ms, 2),
                    "instruments_processed": self._chain_metrics.total_instruments_processed,
                },
                errors_last_hour=errors_last_hour,
                version="1.0.0",
                engine_id="LM05",
            )

    # -- summary and export --

    def get_summary(self) -> TelemetrySummary:
        """Generate a complete telemetry summary."""
        with self._lock:
            uptime = time.time() - self._start_time

            avg_times: Dict[str, float] = {}
            for op, times in self._operation_times.items():
                if times:
                    avg_times[op] = round(sum(times) / len(times), 3)

            summary = TelemetrySummary(
                generated_at=datetime.now(timezone.utc).isoformat(),
                uptime_seconds=round(uptime, 1),
                chain_metrics=self._chain_metrics.model_copy(deep=True),
                search_metrics=self._search_metrics.model_copy(deep=True),
                operation_counts=dict(self._operation_counts),
                operation_avg_times=avg_times,
                error_counts=dict(self._error_counts),
                total_errors=sum(self._error_counts.values()),
                total_operations=sum(self._operation_counts.values()),
                health=self.health_check(),
            )
            summary.deterministic_hash = self.compute_response_hash(summary)
            return summary

    def export_json(self, path: Optional[Path] = None) -> Path:
        """Export telemetry data to JSON file."""
        if path is None:
            timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
            path = TELEMETRY_DIR / f"telemetry_{timestamp}.json"

        summary = self.get_summary()
        data = {
            "summary": summary.model_dump(),
            "recent_errors": [e.model_dump() for e in self._errors[-50:]],
            "recent_audit": [a.model_dump() for a in self._audit_trail[-100:]],
            "recent_operations": [o.model_dump() for o in self._recent_operations[-50:]],
        }

        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
        logger.info(f"Telemetry exported to {path}")
        return path

    def get_chain_metrics(self) -> ChainMetrics:
        """Return chain construction metrics."""
        with self._lock:
            return self._chain_metrics.model_copy(deep=True)

    def get_search_metrics(self) -> SearchMetrics:
        """Return search metrics."""
        with self._lock:
            return self._search_metrics.model_copy(deep=True)

    def get_errors(self, severity: Optional[str] = None,
                   limit: int = 50) -> List[ErrorEntry]:
        """Get recent errors, optionally filtered by severity."""
        with self._lock:
            if severity:
                filtered = [e for e in self._errors if e.severity == severity.upper()]
            else:
                filtered = list(self._errors)
            return filtered[-limit:]

    def get_audit_trail(self, operation: Optional[str] = None,
                        limit: int = 100) -> List[AuditEntry]:
        """Get recent audit entries, optionally filtered by operation."""
        with self._lock:
            if operation:
                filtered = [a for a in self._audit_trail if a.operation == operation]
            else:
                filtered = list(self._audit_trail)
            return filtered[-limit:]

    def reset(self) -> None:
        """Reset all telemetry data (for testing)."""
        with self._lock:
            self._start_time = time.time()
            self._chain_metrics = ChainMetrics()
            self._search_metrics = SearchMetrics()
            self._operation_times.clear()
            self._operation_counts.clear()
            self._errors.clear()
            self._audit_trail.clear()
            self._recent_operations.clear()
            self._error_counts.clear()
        logger.info("Telemetry data reset")

    # -- batch recording helpers --

    def record_link_validated(self, link_id: str, instrument_type: str,
                              strength: str, confidence: float) -> None:
        """Record a link being validated in the chain."""
        with self._lock:
            self._chain_metrics.total_links_validated += 1
        self.audit(
            "link_validated", link_id, "VALIDATE",
            f"Link validated: type={instrument_type}, strength={strength}, "
            f"confidence={confidence:.3f}"
        )

    def record_branch_created(self, branch_id: str, parent_owner: str,
                               branch_count: int) -> None:
        """Record a chain branch being created."""
        with self._lock:
            self._chain_metrics.total_branches_created += 1
            if branch_count > self._chain_metrics.max_branch_factor:
                self._chain_metrics.max_branch_factor = branch_count
        self.audit(
            "branch_created", branch_id, "CREATE",
            f"Branch created from {parent_owner}: {branch_count} sub-branches"
        )

    def record_merger_detected(self, target_owner: str, merged_fractions: int) -> None:
        """Record an interest merger being detected."""
        with self._lock:
            self._chain_metrics.total_mergers_detected += 1
        self.audit(
            "merger_detected", target_owner, "DETECT",
            f"Merger: {merged_fractions} fractional interests consolidated"
        )

    def record_duhig_detected(self, link_id: str, overconveyance: str) -> None:
        """Record a Duhig rule issue being detected."""
        self.audit(
            "duhig_detected", link_id, "DETECT",
            f"Duhig rule applicable: overconveyance of {overconveyance}"
        )
        self.record_error(
            operation="chain_validation",
            error_type="DUHIG_OVERCONVEYANCE",
            error_message=f"Link {link_id}: mineral overconveyance under Duhig rule ({overconveyance})",
            severity="HIGH",
            metadata={"link_id": link_id, "overconveyance": overconveyance},
        )

    def record_after_acquired_title(self, link_id: str, grantor: str) -> None:
        """Record an after-acquired title scenario being detected."""
        self.audit(
            "after_acquired_title", link_id, "DETECT",
            f"After-acquired title may apply: {grantor} conveyed without ownership"
        )

    def record_gap_cured(self, gap_id: str, cure_instrument: str) -> None:
        """Record a gap being cured by a curative instrument."""
        with self._lock:
            if self._chain_metrics.total_gaps_detected > 0:
                cured = sum(1 for _ in []) + 1  # increment
                self._chain_metrics.gap_cure_rate = cured / self._chain_metrics.total_gaps_detected
        self.audit(
            "gap_cured", gap_id, "CURE",
            f"Gap cured by instrument: {cure_instrument}"
        )

    # -- aggregation and reporting --

    def get_operation_percentiles(self, operation: str) -> Dict[str, float]:
        """Calculate percentile timings for an operation."""
        with self._lock:
            times = sorted(self._operation_times.get(operation, []))

        if not times:
            return {"p50": 0.0, "p90": 0.0, "p95": 0.0, "p99": 0.0, "count": 0}

        def percentile(data: List[float], p: float) -> float:
            idx = int(len(data) * p / 100.0)
            idx = min(idx, len(data) - 1)
            return data[idx]

        return {
            "p50": round(percentile(times, 50), 3),
            "p90": round(percentile(times, 90), 3),
            "p95": round(percentile(times, 95), 3),
            "p99": round(percentile(times, 99), 3),
            "count": len(times),
            "min": round(times[0], 3),
            "max": round(times[-1], 3),
            "mean": round(sum(times) / len(times), 3),
        }

    def get_error_rate(self) -> float:
        """Calculate the overall error rate."""
        with self._lock:
            total_ops = sum(self._operation_counts.values())
            total_errors = sum(self._error_counts.values())
        if total_ops == 0:
            return 0.0
        return total_errors / total_ops

    def get_throughput(self) -> Dict[str, float]:
        """Calculate operations per second throughput."""
        elapsed = time.time() - self._start_time
        if elapsed <= 0:
            return {"ops_per_second": 0.0, "elapsed_seconds": 0.0}

        with self._lock:
            total_ops = sum(self._operation_counts.values())

        return {
            "ops_per_second": round(total_ops / elapsed, 2),
            "elapsed_seconds": round(elapsed, 1),
            "total_operations": total_ops,
        }

    def get_recent_operations(self, limit: int = 20) -> List[OperationMetric]:
        """Get the most recent operations."""
        with self._lock:
            return list(self._recent_operations[-limit:])

    def get_error_summary(self) -> Dict[str, Any]:
        """Get a summary of all errors by type and severity."""
        with self._lock:
            by_type: Dict[str, int] = dict(self._error_counts)
            by_severity: Dict[str, int] = defaultdict(int)
            unresolved = 0
            for error in self._errors:
                by_severity[error.severity] += 1
                if not error.resolved:
                    unresolved += 1

        return {
            "total_errors": sum(by_type.values()),
            "unresolved": unresolved,
            "by_type": by_type,
            "by_severity": dict(by_severity),
            "error_rate": self.get_error_rate(),
        }

    def get_audit_summary(self) -> Dict[str, Any]:
        """Get a summary of the audit trail."""
        with self._lock:
            by_operation: Dict[str, int] = defaultdict(int)
            by_action: Dict[str, int] = defaultdict(int)
            for entry in self._audit_trail:
                by_operation[entry.operation] += 1
                by_action[entry.action] += 1

        return {
            "total_entries": len(self._audit_trail),
            "by_operation": dict(by_operation),
            "by_action": dict(by_action),
        }
