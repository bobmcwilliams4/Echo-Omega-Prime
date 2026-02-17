import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any
from collections import deque, defaultdict, Counter
from loguru import logger


ENGINE_ID = "AGI02"


@dataclass
class QueryMetrics:
    query_id: str
    engine_id: str
    timestamp: float
    latency_ms: float
    cache_hit: bool
    doctrine_matched: bool
    mode: str
    confidence: Optional[float]
    error: Optional[str]


class TelemetryCollector:
    def __init__(self):
        self._queries: deque[QueryMetrics] = deque()
        self._errors: deque[Dict[str, Any]] = deque()
        self._lock = None  # placeholder for thread safety if needed
        self._max_retention_seconds = 3600 * 24  # keep 24 hours of data max
        self._audit_writer = AuditTrailWriter(pathlib.Path("./audit_trail"))
        self._coverage_counter = Counter()
        self._doctrine_hits = 0
        self._total_queries = 0

    def record_query(self, metrics: QueryMetrics):
        now = time.time()
        # Clean old data
        self._cleanup_old_entries(now)
        self._queries.append(metrics)
        self._total_queries += 1
        if metrics.doctrine_matched:
            self._doctrine_hits += 1
        self._coverage_counter[metrics.mode] += 1
        try:
            self._audit_writer.write(metrics)
        except Exception as e:
            logger.error(f"Failed to write audit trail for query {metrics.query_id}: {e}")

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        now = time.time()
        self._cleanup_old_entries(now)
        error_record = {
            "timestamp": now,
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
        }
        self._errors.append(error_record)

    def get_latency_stats(self) -> Dict[str, float]:
        latencies = [q.latency_ms for q in self._queries if q.latency_ms is not None]
        if not latencies:
            return {"avg": 0, "p50": 0, "p95": 0, "p99": 0, "min": 0, "max": 0}
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        p50 = self._percentile(latencies_sorted, 50)
        p95 = self._percentile(latencies_sorted, 95)
        p99 = self._percentile(latencies_sorted, 99)
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
        if self._total_queries == 0:
            return 0.0
        return self._doctrine_hits / self._total_queries

    def get_error_rate(self, window_hours: float) -> float:
        now = time.time()
        window_seconds = window_hours * 3600
        start_time = now - window_seconds
        errors_in_window = [e for e in self._errors if e["timestamp"] >= start_time]
        queries_in_window = [q for q in self._queries if q.timestamp >= start_time]
        if not queries_in_window:
            return 0.0
        return len(errors_in_window) / len(queries_in_window)

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        return sum(1 for q in self._queries if q.timestamp >= one_hour_ago)

    def get_coverage_report(self) -> Dict[str, Any]:
        total = sum(self._coverage_counter.values())
        if total == 0:
            return {}
        coverage = {mode: count / total for mode, count in self._coverage_counter.items()}
        return {
            "total_queries": total,
            "coverage_by_mode": coverage,
            "doctrine_hit_rate": self.get_doctrine_hit_rate(),
        }

    def export_jsonl(self, path: pathlib.Path) -> int:
        count = 0
        try:
            with path.open("w", encoding="utf-8") as f:
                for q in self._queries:
                    json_line = json.dumps(asdict(q))
                    f.write(json_line + "\n")
                    count += 1
        except Exception as e:
            logger.error(f"Failed to export telemetry JSONL to {path}: {e}")
        return count

    def _cleanup_old_entries(self, now: float):
        cutoff = now - self._max_retention_seconds
        while self._queries and self._queries[0].timestamp < cutoff:
            old = self._queries.popleft()
            self._total_queries -= 1
            if old.doctrine_matched:
                self._doctrine_hits -= 1
            self._coverage_counter[old.mode] -= 1
            if self._coverage_counter[old.mode] <= 0:
                del self._coverage_counter[old.mode]
        while self._errors and self._errors[0]["timestamp"] < cutoff:
            self._errors.popleft()

    @staticmethod
    def _percentile(data: List[float], percentile: float) -> float:
        if not data:
            return 0.0
        k = (len(data)-1) * (percentile/100)
        f = int(k)
        c = min(f + 1, len(data)-1)
        if f == c:
            return data[int(k)]
        d0 = data[f] * (c - k)
        d1 = data[c] * (k - f)
        return d0 + d1


class AuditTrailWriter:
    def __init__(self, base_path: pathlib.Path):
        self.base_path = base_path
        self.base_path.mkdir(parents=True, exist_ok=True)
        self._file_handles: Dict[str, Any] = {}
        self._max_open_files = 10
        self._open_files_order: deque[str] = deque()

    def write(self, metrics: QueryMetrics):
        date_str = time.strftime("%Y-%m-%d", time.localtime(metrics.timestamp))
        file_path = self.base_path / f"audit_{date_str}.jsonl"
        if file_path not in self._file_handles:
            self._open_file(file_path)
        f = self._file_handles[file_path]
        json_line = json.dumps(asdict(metrics))
        f.write(json_line + "\n")
        f.flush()

    def _open_file(self, file_path: pathlib.Path):
        if len(self._file_handles) >= self._max_open_files:
            oldest = self._open_files_order.popleft()
            fh = self._file_handles.pop(oldest)
            try:
                fh.close()
            except Exception:
                pass
        fh = file_path.open("a", encoding="utf-8")
        self._file_handles[file_path] = fh
        self._open_files_order.append(file_path)

    def close_all(self):
        for fh in self._file_handles.values():
            try:
                fh.close()
            except Exception:
                pass
        self._file_handles.clear()
        self._open_files_order.clear()


COLLECTOR = TelemetryCollector()