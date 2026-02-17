import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Deque, Any
from collections import deque, defaultdict, Counter
from loguru import logger


ENGINE_ID = "DRL14"


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
        self._queries: Deque[QueryMetrics] = deque()
        self._errors: Deque[Dict[str, Any]] = deque()
        self._lock = None  # placeholder for threading.Lock if needed later
        self._max_retention_seconds = 3600 * 24  # keep 24 hours of data max
        self._coverage_modes: Counter = Counter()
        self._doctrine_hits = 0
        self._total_queries = 0
        self._cache_hits = 0
        self._error_counts: Counter = Counter()
        self._error_total = 0

    def _prune_old(self):
        cutoff = time.time() - self._max_retention_seconds
        while self._queries and self._queries[0].timestamp < cutoff:
            old = self._queries.popleft()
            # Adjust counters accordingly
            self._coverage_modes[old.mode] -= 1
            if old.doctrine_matched:
                self._doctrine_hits -= 1
            self._total_queries -= 1
            if old.cache_hit:
                self._cache_hits -= 1
            if old.error:
                self._error_counts[old.error] -= 1
                self._error_total -= 1
        while self._errors and self._errors[0]['timestamp'] < cutoff:
            old_err = self._errors.popleft()
            self._error_counts[old_err['error_type']] -= 1
            self._error_total -= 1

    def record_query(self, metrics: QueryMetrics):
        if metrics.engine_id != ENGINE_ID:
            logger.warning(f"Received metrics for different engine_id: {metrics.engine_id}")
            return
        self._prune_old()
        self._queries.append(metrics)
        self._coverage_modes[metrics.mode] += 1
        self._total_queries += 1
        if metrics.doctrine_matched:
            self._doctrine_hits += 1
        if metrics.cache_hit:
            self._cache_hits += 1
        if metrics.error:
            self._error_counts[metrics.error] += 1
            self._error_total += 1

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        self._prune_old()
        err = {
            "timestamp": time.time(),
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
        }
        self._errors.append(err)
        self._error_counts[error_type] += 1
        self._error_total += 1

    def get_latency_stats(self) -> Dict[str, float]:
        self._prune_old()
        latencies = [q.latency_ms for q in self._queries if q.latency_ms is not None and q.latency_ms >= 0]
        if not latencies:
            return {"avg": 0, "p50": 0, "p95": 0, "p99": 0, "min": 0, "max": 0}
        latencies.sort()
        avg = statistics.mean(latencies)
        p50 = latencies[int(len(latencies)*0.50)]
        p95 = latencies[int(len(latencies)*0.95) if int(len(latencies)*0.95) < len(latencies) else -1]
        p99 = latencies[int(len(latencies)*0.99) if int(len(latencies)*0.99) < len(latencies) else -1]
        min_v = latencies[0]
        max_v = latencies[-1]
        return {"avg": avg, "p50": p50, "p95": p95, "p99": p99, "min": min_v, "max": max_v}

    def get_doctrine_hit_rate(self) -> float:
        self._prune_old()
        if self._total_queries == 0:
            return 0.0
        return self._doctrine_hits / self._total_queries

    def get_error_rate(self, window_hours: int) -> float:
        self._prune_old()
        now = time.time()
        cutoff = now - window_hours * 3600
        total_in_window = 0
        errors_in_window = 0
        for q in self._queries:
            if q.timestamp >= cutoff:
                total_in_window += 1
                if q.error:
                    errors_in_window += 1
        if total_in_window == 0:
            return 0.0
        return errors_in_window / total_in_window

    def queries_last_hour(self) -> int:
        self._prune_old()
        now = time.time()
        cutoff = now - 3600
        count = 0
        for q in reversed(self._queries):
            if q.timestamp < cutoff:
                break
            count += 1
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        self._prune_old()
        total = sum(self._coverage_modes.values())
        if total == 0:
            return {}
        coverage = {mode: count / total for mode, count in self._coverage_modes.items()}
        report = {
            "total_queries": self._total_queries,
            "mode_coverage": coverage,
            "cache_hit_rate": self._cache_hits / self._total_queries if self._total_queries else 0.0,
            "doctrine_hit_rate": self.get_doctrine_hit_rate(),
            "error_rate": self._error_total / self._total_queries if self._total_queries else 0.0,
            "error_counts": dict(self._error_counts),
        }
        return report

    def export_jsonl(self, path: pathlib.Path) -> int:
        self._prune_old()
        count = 0
        try:
            with path.open("w", encoding="utf-8") as f:
                for q in self._queries:
                    data = asdict(q)
                    f.write(json.dumps(data) + "\n")
                    count += 1
            logger.info(f"Exported {count} telemetry records to {path}")
        except Exception as e:
            logger.error(f"Failed to export telemetry to {path}: {e}")
            raise
        return count


class AuditTrailWriter:
    def __init__(self, directory: pathlib.Path):
        self.directory = directory
        self.directory.mkdir(parents=True, exist_ok=True)
        self._file_handles: Dict[str, Any] = {}

    def _get_file_handle(self, query_id: str):
        # Use first 2 chars of query_id hash to shard files
        shard = hashlib.sha256(query_id.encode("utf-8")).hexdigest()[:2]
        filename = self.directory / f"audit_{shard}.jsonl"
        if filename not in self._file_handles:
            self._file_handles[filename] = open(filename, "a", encoding="utf-8")
        return self._file_handles[filename]

    def write(self, metrics: QueryMetrics):
        try:
            fh = self._get_file_handle(metrics.query_id)
            data = asdict(metrics)
            fh.write(json.dumps(data) + "\n")
            fh.flush()
        except Exception as e:
            logger.error(f"Failed to write audit trail for query_id={metrics.query_id}: {e}")

    def close(self):
        for fh in self._file_handles.values():
            try:
                fh.close()
            except Exception:
                pass
        self._file_handles.clear()


COLLECTOR = TelemetryCollector()