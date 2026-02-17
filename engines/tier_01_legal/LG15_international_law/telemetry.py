"""
LG15 International Law Engine - Telemetry Module
===================================================
Counters, ring buffer, audit trail (JSONL with SHA-256 hash chain),
metrics aggregation, error tracking, doctrine mutation log, drift watcher.

Engine: LG15 International Law
Version: 2.0.0
"""

from __future__ import annotations

import hashlib
import json
import math
import statistics
import threading
import time
from collections import defaultdict, deque
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Optional

from loguru import logger

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

_ENGINE_ID = "LG15"
_ENGINE_NAME = "International Law Engine"
_ENGINE_VERSION = "2.0.0"
_MAX_RING_BUFFER = 2000
_MAX_ERROR_BUFFER = 500
_MAX_MUTATION_LOG = 1000
_DRIFT_STALENESS_HOURS = 168  # 7 days
_METRICS_RETENTION_HOURS = 168


# ---------------------------------------------------------------------------
# QueryTrace dataclass
# ---------------------------------------------------------------------------

@dataclass
class QueryTrace:
    """Trace record for a single query execution."""

    trace_id: str
    query_text: str
    query_hash: str
    category: str
    response_mode: str
    confidence: float
    latency_ms: float
    cache_hit: bool
    doctrine_blocks_used: int
    search_results_count: int
    zone: str
    error: str | None
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# ---------------------------------------------------------------------------
# TelemetryCollector
# ---------------------------------------------------------------------------

class TelemetryCollector:
    """Central telemetry hub: counters, ring buffer, latency tracking."""

    def __init__(self, telemetry_dir: Path | None = None) -> None:
        self._lock = threading.Lock()

        # Counters
        self._total_queries: int = 0
        self._cache_hits: int = 0
        self._cache_misses: int = 0
        self._errors: int = 0
        self._by_category: dict[str, int] = defaultdict(int)
        self._by_mode: dict[str, int] = defaultdict(int)
        self._by_zone: dict[str, int] = defaultdict(int)
        self._by_confidence: dict[str, int] = defaultdict(int)

        # Latencies
        self._latencies: deque[float] = deque(maxlen=10000)

        # Ring buffer of recent traces
        self._ring: deque[QueryTrace] = deque(maxlen=_MAX_RING_BUFFER)

        # Telemetry directory
        self._dir = telemetry_dir or Path("telemetry_data")
        self._dir.mkdir(parents=True, exist_ok=True)

        self._started_at = datetime.utcnow().isoformat()
        logger.info("TelemetryCollector initialised, dir={}", self._dir)

    # -- recording ----------------------------------------------------------

    def record_query(self, trace: QueryTrace) -> None:
        """Record a completed query trace."""
        with self._lock:
            self._total_queries += 1
            if trace.cache_hit:
                self._cache_hits += 1
            else:
                self._cache_misses += 1
            if trace.error:
                self._errors += 1
            self._by_category[trace.category] += 1
            self._by_mode[trace.response_mode] += 1
            self._by_zone[trace.zone] += 1

            conf_band = self._confidence_band(trace.confidence)
            self._by_confidence[conf_band] += 1

            self._latencies.append(trace.latency_ms)
            self._ring.append(trace)

    def record_cache_hit(self) -> None:
        with self._lock:
            self._cache_hits += 1

    def record_error(self) -> None:
        with self._lock:
            self._errors += 1

    @staticmethod
    def _confidence_band(conf: float) -> str:
        if conf >= 0.85:
            return "HIGH"
        if conf >= 0.65:
            return "MEDIUM"
        if conf >= 0.40:
            return "LOW"
        return "INSUFFICIENT"

    # -- retrieval ----------------------------------------------------------

    def get_counters(self) -> dict[str, Any]:
        with self._lock:
            return {
                "total_queries": self._total_queries,
                "cache_hits": self._cache_hits,
                "cache_misses": self._cache_misses,
                "cache_hit_rate": round(self._cache_hits / max(self._total_queries, 1), 4),
                "errors": self._errors,
                "error_rate": round(self._errors / max(self._total_queries, 1), 4),
                "started_at": self._started_at,
            }

    def get_category_distribution(self) -> dict[str, int]:
        with self._lock:
            return dict(self._by_category)

    def get_mode_distribution(self) -> dict[str, int]:
        with self._lock:
            return dict(self._by_mode)

    def get_zone_distribution(self) -> dict[str, int]:
        with self._lock:
            return dict(self._by_zone)

    def get_confidence_distribution(self) -> dict[str, int]:
        with self._lock:
            return dict(self._by_confidence)

    def get_recent_traces(self, n: int = 50) -> list[dict[str, Any]]:
        with self._lock:
            traces = list(self._ring)[-n:]
        return [t.to_dict() for t in traces]

    def get_latency_stats(self) -> dict[str, float]:
        with self._lock:
            lats = list(self._latencies)
        if not lats:
            return {"count": 0, "mean": 0.0, "p50": 0.0, "p90": 0.0, "p95": 0.0, "p99": 0.0, "min": 0.0, "max": 0.0}
        lats_sorted = sorted(lats)
        n = len(lats_sorted)
        return {
            "count": n,
            "mean": round(statistics.mean(lats_sorted), 2),
            "p50": round(lats_sorted[int(n * 0.50)], 2),
            "p90": round(lats_sorted[min(int(n * 0.90), n - 1)], 2),
            "p95": round(lats_sorted[min(int(n * 0.95), n - 1)], 2),
            "p99": round(lats_sorted[min(int(n * 0.99), n - 1)], 2),
            "min": round(lats_sorted[0], 2),
            "max": round(lats_sorted[-1], 2),
        }

    def get_full_snapshot(self) -> dict[str, Any]:
        return {
            "engine_id": _ENGINE_ID,
            "engine_name": _ENGINE_NAME,
            "version": _ENGINE_VERSION,
            "counters": self.get_counters(),
            "latency": self.get_latency_stats(),
            "by_category": self.get_category_distribution(),
            "by_mode": self.get_mode_distribution(),
            "by_zone": self.get_zone_distribution(),
            "by_confidence": self.get_confidence_distribution(),
            "recent_traces_count": len(self._ring),
            "snapshot_at": datetime.utcnow().isoformat(),
        }

    def reset(self) -> None:
        """Reset all counters (used in testing)."""
        with self._lock:
            self._total_queries = 0
            self._cache_hits = 0
            self._cache_misses = 0
            self._errors = 0
            self._by_category.clear()
            self._by_mode.clear()
            self._by_zone.clear()
            self._by_confidence.clear()
            self._latencies.clear()
            self._ring.clear()
            self._started_at = datetime.utcnow().isoformat()
        logger.info("TelemetryCollector reset")


# ---------------------------------------------------------------------------
# AuditTrailWriter (append-only JSONL with SHA-256 hash chain)
# ---------------------------------------------------------------------------

class AuditTrailWriter:
    """Append-only JSONL audit log with cryptographic hash chain."""

    def __init__(self, log_path: Path | None = None) -> None:
        self._path = log_path or Path("telemetry_data") / "audit_trail.jsonl"
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._prev_hash: str = "GENESIS"
        self._seq: int = 0
        self._recover_chain()
        logger.info("AuditTrailWriter initialised at {}, seq={}", self._path, self._seq)

    def _recover_chain(self) -> None:
        """On startup, read last line to recover previous hash and sequence."""
        if not self._path.exists():
            return
        try:
            last_line = ""
            with self._path.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        last_line = line
            if last_line:
                record = json.loads(last_line)
                self._prev_hash = record.get("hash", "GENESIS")
                self._seq = record.get("seq", 0)
        except (json.JSONDecodeError, OSError) as exc:
            logger.warning("Could not recover audit chain: {}", exc)

    def _compute_hash(self, payload: str) -> str:
        content = f"{self._prev_hash}::{payload}"
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def write_entry(
        self,
        event_type: str,
        actor: str,
        detail: dict[str, Any],
        query_hash: str = "",
    ) -> dict[str, Any]:
        """Write a single audit entry, returning the record written."""
        with self._lock:
            self._seq += 1
            timestamp = datetime.utcnow().isoformat()
            payload = json.dumps({
                "seq": self._seq,
                "event_type": event_type,
                "actor": actor,
                "detail": detail,
                "query_hash": query_hash,
                "timestamp": timestamp,
                "prev_hash": self._prev_hash,
            }, sort_keys=True, separators=(",", ":"))

            current_hash = self._compute_hash(payload)
            record = {
                "seq": self._seq,
                "event_type": event_type,
                "actor": actor,
                "detail": detail,
                "query_hash": query_hash,
                "timestamp": timestamp,
                "prev_hash": self._prev_hash,
                "hash": current_hash,
            }
            self._prev_hash = current_hash

            try:
                with self._path.open("a", encoding="utf-8") as f:
                    f.write(json.dumps(record, separators=(",", ":")) + "\n")
            except OSError as exc:
                logger.error("Failed to write audit entry: {}", exc)

            return record

    def verify_chain(self, max_entries: int = 10000) -> dict[str, Any]:
        """Verify the integrity of the hash chain."""
        if not self._path.exists():
            return {"valid": True, "entries_checked": 0, "message": "No audit trail file found"}

        prev_hash = "GENESIS"
        entries_checked = 0
        broken_at: int | None = None

        try:
            with self._path.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    entries_checked += 1
                    if entries_checked > max_entries:
                        break
                    try:
                        record = json.loads(line)
                    except json.JSONDecodeError:
                        broken_at = entries_checked
                        break

                    stored_prev = record.get("prev_hash", "")
                    if stored_prev != prev_hash:
                        broken_at = entries_checked
                        break

                    check_payload = json.dumps({
                        "seq": record["seq"],
                        "event_type": record["event_type"],
                        "actor": record["actor"],
                        "detail": record["detail"],
                        "query_hash": record.get("query_hash", ""),
                        "timestamp": record["timestamp"],
                        "prev_hash": record["prev_hash"],
                    }, sort_keys=True, separators=(",", ":"))
                    expected_hash = hashlib.sha256(f"{prev_hash}::{check_payload}".encode()).hexdigest()

                    if record.get("hash") != expected_hash:
                        broken_at = entries_checked
                        break

                    prev_hash = record["hash"]
        except OSError as exc:
            return {"valid": False, "entries_checked": entries_checked, "error": str(exc)}

        if broken_at is not None:
            return {"valid": False, "entries_checked": entries_checked, "broken_at_seq": broken_at}
        return {"valid": True, "entries_checked": entries_checked, "last_hash": prev_hash}

    def get_recent_entries(self, n: int = 50) -> list[dict[str, Any]]:
        """Read the last N entries from the audit trail."""
        if not self._path.exists():
            return []
        entries: deque[dict[str, Any]] = deque(maxlen=n)
        try:
            with self._path.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            entries.append(json.loads(line))
                        except json.JSONDecodeError:
                            pass
        except OSError:
            pass
        return list(entries)

    @property
    def sequence_number(self) -> int:
        return self._seq

    @property
    def current_hash(self) -> str:
        return self._prev_hash


# ---------------------------------------------------------------------------
# MetricsAggregator
# ---------------------------------------------------------------------------

class MetricsAggregator:
    """Aggregates latency percentiles and category distributions over time windows."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._windows: dict[str, deque[tuple[float, float]]] = defaultdict(lambda: deque(maxlen=50000))
        self._category_counts: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
        logger.info("MetricsAggregator initialised")

    def record_latency(self, category: str, latency_ms: float) -> None:
        ts = time.time()
        with self._lock:
            self._windows[category].append((ts, latency_ms))

    def record_category_event(self, window_name: str, category: str) -> None:
        with self._lock:
            self._category_counts[window_name][category] += 1

    def get_latency_percentiles(
        self,
        category: str,
        window_seconds: float = 3600.0,
        percentiles: list[float] | None = None,
    ) -> dict[str, float]:
        """Compute latency percentiles for a category within a time window."""
        if percentiles is None:
            percentiles = [0.50, 0.90, 0.95, 0.99]
        cutoff = time.time() - window_seconds
        with self._lock:
            values = [v for ts, v in self._windows.get(category, []) if ts >= cutoff]

        if not values:
            return {f"p{int(p*100)}": 0.0 for p in percentiles}

        values.sort()
        n = len(values)
        result: dict[str, float] = {"count": float(n), "mean": round(statistics.mean(values), 2)}
        for p in percentiles:
            idx = min(int(n * p), n - 1)
            result[f"p{int(p*100)}"] = round(values[idx], 2)
        return result

    def get_category_distribution(self, window_name: str) -> dict[str, int]:
        with self._lock:
            return dict(self._category_counts.get(window_name, {}))

    def get_all_category_distributions(self) -> dict[str, dict[str, int]]:
        with self._lock:
            return {w: dict(cats) for w, cats in self._category_counts.items()}

    def prune_old_data(self, max_age_seconds: float = _METRICS_RETENTION_HOURS * 3600) -> int:
        """Remove data older than max_age_seconds. Returns count removed."""
        cutoff = time.time() - max_age_seconds
        removed = 0
        with self._lock:
            for category in list(self._windows.keys()):
                dq = self._windows[category]
                before = len(dq)
                while dq and dq[0][0] < cutoff:
                    dq.popleft()
                removed += before - len(dq)
                if not dq:
                    del self._windows[category]
        return removed


# ---------------------------------------------------------------------------
# ErrorTracker
# ---------------------------------------------------------------------------

class ErrorSeverity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


@dataclass
class ErrorRecord:
    error_id: str
    error_type: str
    message: str
    severity: ErrorSeverity
    category: str
    query_hash: str
    stack_trace: str
    resolution: str
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    resolved: bool = False

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["severity"] = self.severity.value
        return d


class ErrorTracker:
    """Track errors with severity, frequency, and resolution."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._errors: deque[ErrorRecord] = deque(maxlen=_MAX_ERROR_BUFFER)
        self._type_counts: dict[str, int] = defaultdict(int)
        self._severity_counts: dict[str, int] = defaultdict(int)
        self._total: int = 0
        logger.info("ErrorTracker initialised")

    def record_error(self, error: ErrorRecord) -> None:
        with self._lock:
            self._errors.append(error)
            self._type_counts[error.error_type] += 1
            self._severity_counts[error.severity.value] += 1
            self._total += 1
        if error.severity in (ErrorSeverity.CRITICAL, ErrorSeverity.HIGH):
            logger.error("ErrorTracker [{severity}] {error_type}: {message}", severity=error.severity.value, error_type=error.error_type, message=error.message)
        else:
            logger.warning("ErrorTracker [{severity}] {error_type}: {message}", severity=error.severity.value, error_type=error.error_type, message=error.message)

    def get_recent_errors(self, n: int = 20, severity_filter: ErrorSeverity | None = None) -> list[dict[str, Any]]:
        with self._lock:
            errors = list(self._errors)
        if severity_filter:
            errors = [e for e in errors if e.severity == severity_filter]
        return [e.to_dict() for e in errors[-n:]]

    def get_error_stats(self) -> dict[str, Any]:
        with self._lock:
            return {
                "total_errors": self._total,
                "by_type": dict(self._type_counts),
                "by_severity": dict(self._severity_counts),
                "recent_count": len(self._errors),
            }

    def get_recurring_errors(self, min_count: int = 3) -> list[dict[str, Any]]:
        with self._lock:
            return [
                {"error_type": t, "count": c}
                for t, c in self._type_counts.items()
                if c >= min_count
            ]

    def mark_resolved(self, error_id: str, resolution: str) -> bool:
        with self._lock:
            for e in self._errors:
                if e.error_id == error_id:
                    e.resolved = True
                    e.resolution = resolution
                    return True
        return False


# ---------------------------------------------------------------------------
# DoctrineMutationLog
# ---------------------------------------------------------------------------

@dataclass
class MutationRecord:
    mutation_id: str
    doctrine_block_id: str
    field_changed: str
    old_value_hash: str
    new_value_hash: str
    reason: str
    actor: str
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class DoctrineMutationLog:
    """Track all modifications to doctrine blocks."""

    def __init__(self, log_path: Path | None = None) -> None:
        self._path = log_path or Path("telemetry_data") / "doctrine_mutations.jsonl"
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._recent: deque[MutationRecord] = deque(maxlen=_MAX_MUTATION_LOG)
        self._count: int = 0
        logger.info("DoctrineMutationLog initialised at {}", self._path)

    def log_mutation(self, mutation: MutationRecord) -> None:
        with self._lock:
            self._recent.append(mutation)
            self._count += 1
            try:
                with self._path.open("a", encoding="utf-8") as f:
                    f.write(json.dumps(mutation.to_dict(), separators=(",", ":")) + "\n")
            except OSError as exc:
                logger.error("Failed to write mutation log: {}", exc)

    def get_recent_mutations(self, n: int = 50) -> list[dict[str, Any]]:
        with self._lock:
            return [m.to_dict() for m in list(self._recent)[-n:]]

    def get_mutations_for_block(self, block_id: str, n: int = 20) -> list[dict[str, Any]]:
        with self._lock:
            matching = [m for m in self._recent if m.doctrine_block_id == block_id]
        return [m.to_dict() for m in matching[-n:]]

    @property
    def total_mutations(self) -> int:
        return self._count


# ---------------------------------------------------------------------------
# DriftWatcher
# ---------------------------------------------------------------------------

@dataclass
class DriftRecord:
    block_id: str
    topic: str
    last_verified: str
    staleness_hours: float
    drift_detected: bool
    drift_type: str
    confidence_delta: float
    recommendation: str


class DriftWatcher:
    """Monitor doctrine blocks for staleness and content drift."""

    def __init__(self, staleness_threshold_hours: float = _DRIFT_STALENESS_HOURS) -> None:
        self._threshold = staleness_threshold_hours
        self._lock = threading.Lock()
        self._block_timestamps: dict[str, str] = {}
        self._block_hashes: dict[str, str] = {}
        self._drift_records: deque[DriftRecord] = deque(maxlen=500)
        logger.info("DriftWatcher initialised, staleness_threshold={}h", self._threshold)

    def register_block(self, block_id: str, content_hash: str, timestamp: str | None = None) -> None:
        ts = timestamp or datetime.utcnow().isoformat()
        with self._lock:
            self._block_timestamps[block_id] = ts
            self._block_hashes[block_id] = content_hash

    def check_staleness(self, block_id: str) -> dict[str, Any]:
        with self._lock:
            ts_str = self._block_timestamps.get(block_id)
        if ts_str is None:
            return {"block_id": block_id, "status": "UNKNOWN", "staleness_hours": -1}

        try:
            last_ts = datetime.fromisoformat(ts_str)
        except ValueError:
            return {"block_id": block_id, "status": "INVALID_TIMESTAMP", "staleness_hours": -1}

        age_hours = (datetime.utcnow() - last_ts).total_seconds() / 3600.0
        stale = age_hours > self._threshold
        return {
            "block_id": block_id,
            "last_verified": ts_str,
            "staleness_hours": round(age_hours, 2),
            "stale": stale,
            "status": "STALE" if stale else "FRESH",
            "threshold_hours": self._threshold,
        }

    def check_drift(self, block_id: str, current_hash: str, topic: str = "") -> DriftRecord:
        with self._lock:
            prev_hash = self._block_hashes.get(block_id, "")
            ts_str = self._block_timestamps.get(block_id, datetime.utcnow().isoformat())

        try:
            last_ts = datetime.fromisoformat(ts_str)
            age_hours = (datetime.utcnow() - last_ts).total_seconds() / 3600.0
        except ValueError:
            age_hours = 0.0

        drift_detected = prev_hash != "" and prev_hash != current_hash
        stale = age_hours > self._threshold

        if drift_detected:
            drift_type = "CONTENT_CHANGED"
            recommendation = f"Block {block_id} content hash changed. Review for accuracy and update verification timestamp."
            confidence_delta = -0.10
        elif stale:
            drift_type = "STALE"
            recommendation = f"Block {block_id} last verified {age_hours:.0f}h ago (threshold {self._threshold}h). Re-verify against current law."
            confidence_delta = -0.05 * (age_hours / self._threshold)
        else:
            drift_type = "NONE"
            recommendation = "No drift detected."
            confidence_delta = 0.0

        record = DriftRecord(
            block_id=block_id,
            topic=topic,
            last_verified=ts_str,
            staleness_hours=round(age_hours, 2),
            drift_detected=drift_detected or stale,
            drift_type=drift_type,
            confidence_delta=round(confidence_delta, 4),
            recommendation=recommendation,
        )

        with self._lock:
            self._drift_records.append(record)
            if drift_detected:
                self._block_hashes[block_id] = current_hash
                self._block_timestamps[block_id] = datetime.utcnow().isoformat()

        return record

    def get_all_stale_blocks(self) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        with self._lock:
            block_ids = list(self._block_timestamps.keys())
        for bid in block_ids:
            status = self.check_staleness(bid)
            if status.get("stale", False):
                results.append(status)
        return results

    def get_drift_summary(self) -> dict[str, Any]:
        with self._lock:
            records = list(self._drift_records)
        total = len(records)
        drifted = sum(1 for r in records if r.drift_detected)
        stale_count = sum(1 for r in records if r.drift_type == "STALE")
        changed_count = sum(1 for r in records if r.drift_type == "CONTENT_CHANGED")
        return {
            "total_checks": total,
            "drift_detected": drifted,
            "stale_blocks": stale_count,
            "content_changed": changed_count,
            "monitored_blocks": len(self._block_timestamps),
            "threshold_hours": self._threshold,
        }

    def refresh_block(self, block_id: str, content_hash: str) -> None:
        """Mark a block as freshly verified."""
        with self._lock:
            self._block_timestamps[block_id] = datetime.utcnow().isoformat()
            self._block_hashes[block_id] = content_hash
        logger.debug("DriftWatcher: refreshed block {}", block_id)

    def get_recent_drift_records(self, n: int = 30) -> list[dict[str, Any]]:
        with self._lock:
            records = list(self._drift_records)[-n:]
        return [
            {
                "block_id": r.block_id,
                "topic": r.topic,
                "last_verified": r.last_verified,
                "staleness_hours": r.staleness_hours,
                "drift_detected": r.drift_detected,
                "drift_type": r.drift_type,
                "confidence_delta": r.confidence_delta,
                "recommendation": r.recommendation,
            }
            for r in records
        ]
