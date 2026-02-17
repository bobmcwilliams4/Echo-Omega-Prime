import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any
from collections import deque, defaultdict, Counter
from loguru import logger


ENGINE_ID = "CHEM13"


@dataclass
class QueryMetrics:
    query_id: str
    engine_id: str
    timestamp: float
    latency_ms: float
    cache_hit: bool
    doctrine_matched: bool
    mode: str
    confidence: float
    error: Optional[str] = None


class TelemetryCollector:
    def __init__(self):
        self._queries: deque[QueryMetrics] = deque()
        self._errors: deque[Dict[str, Any]] = deque()
        self._lock = None  # Placeholder for thread safety if needed
        self._max_retention_seconds = 24 * 3600  # Retain 24 hours of data
        self._coverage_modes: Counter = Counter()
        self._coverage_confidences: List[float] = []
        self._cache_hits = 0
        self._doctrine_hits = 0
        self._total_queries = 0

    def _cleanup_old_data(self):
        cutoff = time.time() - self._max_retention_seconds
        while self._queries and self._queries[0].timestamp < cutoff:
            old = self._queries.popleft()
            self._total_queries -= 1
            if old.cache_hit:
                self._cache_hits -= 1
            if old.doctrine_matched:
                self._doctrine_hits -= 1
            self._coverage_modes[old.mode] -= 1
            try:
                self._coverage_confidences.remove(old.confidence)
            except ValueError:
                pass  # confidence might be missing if data corrupted

        while self._errors and self._errors[0]['timestamp'] < cutoff:
            self._errors.popleft()

    def record_query(self, metrics: QueryMetrics):
        if metrics.engine_id != ENGINE_ID:
            logger.warning(f"Received metrics for unknown engine_id {metrics.engine_id}")
            return
        self._cleanup_old_data()
        self._queries.append(metrics)
        self._total_queries += 1
        if metrics.cache_hit:
            self._cache_hits += 1
        if metrics.doctrine_matched:
            self._doctrine_hits += 1
        self._coverage_modes[metrics.mode] += 1
        self._coverage_confidences.append(metrics.confidence)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        self._cleanup_old_data()
        error_record = {
            "timestamp": time.time(),
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
        }
        self._errors.append(error_record)

    def get_latency_stats(self) -> Dict[str, float]:
        self._cleanup_old_data()
        latencies = [q.latency_ms for q in self._queries if q.latency_ms is not None]
        if not latencies:
            return {"avg": 0, "p50": 0, "p95": 0, "p99": 0, "min": 0, "max": 0}
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = latencies_sorted[int(len(latencies_sorted) * 0.95) - 1]
        p99 = latencies_sorted[int(len(latencies_sorted) * 0.99) - 1]
        min_latency = latencies_sorted[0]
        max_latency = latencies_sorted[-1]
        return {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_latency,
            "max": max_latency,
        }

    def get_doctrine_hit_rate(self) -> float:
        self._cleanup_old_data()
        if self._total_queries == 0:
            return 0.0
        return self._doctrine_hits / self._total_queries

    def get_error_rate(self, window_hours: int) -> float:
        self._cleanup_old_data()
        now = time.time()
        window_seconds = window_hours * 3600
        window_start = now - window_seconds
        errors_in_window = [e for e in self._errors if e['timestamp'] >= window_start]
        queries_in_window = [q for q in self._queries if q.timestamp >= window_start]
        if not queries_in_window:
            return 0.0
        return len(errors_in_window) / len(queries_in_window)

    def queries_last_hour(self) -> int:
        self._cleanup_old_data()
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= one_hour_ago)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        self._cleanup_old_data()
        mode_counts = dict(self._coverage_modes)
        total_modes = sum(mode_counts.values())
        mode_distribution = {mode: count / total_modes for mode, count in mode_counts.items()} if total_modes else {}
        avg_confidence = statistics.mean(self._coverage_confidences) if self._coverage_confidences else 0.0
        coverage = {
            "mode_distribution": mode_distribution,
            "average_confidence": avg_confidence,
            "cache_hit_rate": (self._cache_hits / self._total_queries) if self._total_queries else 0.0,
            "doctrine_hit_rate": self.get_doctrine_hit_rate(),
            "total_queries": self._total_queries,
        }
        return coverage

    def export_jsonl(self, path: pathlib.Path) -> int:
        self._cleanup_old_data()
        path.parent.mkdir(parents=True, exist_ok=True)
        count = 0
        try:
            with path.open("w", encoding="utf-8") as f:
                for q in self._queries:
                    record = asdict(q)
                    f.write(json.dumps(record) + "\n")
                    count += 1
            logger.info(f"Exported {count} telemetry records to {path}")
        except Exception as e:
            logger.error(f"Failed to export telemetry data to {path}: {e}")
        return count


class AuditTrailWriter:
    def __init__(self, directory: pathlib.Path):
        self.directory = directory
        self.directory.mkdir(parents=True, exist_ok=True)

    def _sanitize_filename(self, s: str) -> str:
        # Simple sanitizer for filenames
        return "".join(c if c.isalnum() or c in ('-', '_') else '_' for c in s)

    def write(self, query_id: str, audit_data: Dict[str, Any]) -> None:
        try:
            filename = f"{self._sanitize_filename(query_id)}.jsonl"
            path = self.directory / filename
            with path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(audit_data) + "\n")
            logger.debug(f"Wrote audit trail for query_id={query_id} to {path}")
        except Exception as e:
            logger.error(f"Failed to write audit trail for query_id={query_id}: {e}")


COLLECTOR = TelemetryCollector()