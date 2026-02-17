import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any
from collections import deque, defaultdict
from loguru import logger

ENGINE_ID = "MATH15"

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
        self._lock = None  # Placeholder if threading.Lock needed later
        self._max_retention_seconds = 3600 * 24  # 24 hours retention for stats
        self._coverage_modes: Dict[str, int] = defaultdict(int)
        self._coverage_doctrine_hits: int = 0
        self._coverage_total: int = 0

    def _cleanup_old(self):
        cutoff = time.time() - self._max_retention_seconds
        while self._queries and self._queries[0].timestamp < cutoff:
            old = self._queries.popleft()
            # Adjust coverage counters accordingly
            self._coverage_modes[old.mode] -= 1
            if old.doctrine_matched:
                self._coverage_doctrine_hits -= 1
            self._coverage_total -= 1

        while self._errors and self._errors[0]['timestamp'] < cutoff:
            self._errors.popleft()

    def record_query(self, metrics: QueryMetrics):
        if metrics.engine_id != ENGINE_ID:
            logger.warning(f"Received metrics for unknown engine_id {metrics.engine_id}")
            return
        self._queries.append(metrics)
        self._coverage_modes[metrics.mode] += 1
        if metrics.doctrine_matched:
            self._coverage_doctrine_hits += 1
        self._coverage_total += 1
        self._cleanup_old()

    def record_error(self, error_type: str, message: str, query_id: Optional[str]):
        error_record = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "timestamp": time.time()
        }
        self._errors.append(error_record)
        self._cleanup_old()

    def get_latency_stats(self) -> dict:
        self._cleanup_old()
        latencies = [q.latency_ms for q in self._queries if q.latency_ms is not None]
        if not latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        latencies.sort()
        avg = statistics.mean(latencies)
        p50 = latencies[int(len(latencies)*0.50)]
        p95 = latencies[int(len(latencies)*0.95) if int(len(latencies)*0.95) < len(latencies) else -1]
        p99 = latencies[int(len(latencies)*0.99) if int(len(latencies)*0.99) < len(latencies) else -1]
        return {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": latencies[0],
            "max": latencies[-1],
        }

    def get_doctrine_hit_rate(self) -> float:
        self._cleanup_old()
        if self._coverage_total == 0:
            return 0.0
        return self._coverage_doctrine_hits / self._coverage_total

    def get_error_rate(self, window_hours: int) -> float:
        self._cleanup_old()
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self._errors if e['timestamp'] >= window_start]
        queries_in_window = [q for q in self._queries if q.timestamp >= window_start]
        if not queries_in_window:
            return 0.0
        return len(errors_in_window) / len(queries_in_window)

    def queries_last_hour(self) -> int:
        self._cleanup_old()
        cutoff = time.time() - 3600
        return sum(1 for q in self._queries if q.timestamp >= cutoff)

    def get_coverage_report(self) -> dict:
        self._cleanup_old()
        modes_total = sum(self._coverage_modes.values())
        mode_distribution = {}
        for mode, count in self._coverage_modes.items():
            mode_distribution[mode] = {
                "count": count,
                "percentage": (count / modes_total * 100) if modes_total > 0 else 0.0
            }
        return {
            "total_queries": self._coverage_total,
            "doctrine_hit_rate": self.get_doctrine_hit_rate(),
            "mode_distribution": mode_distribution,
        }

    def export_jsonl(self, path: pathlib.Path) -> int:
        self._cleanup_old()
        count = 0
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            for q in self._queries:
                record = asdict(q)
                f.write(json.dumps(record) + "\n")
                count += 1
        return count

class AuditTrailWriter:
    def __init__(self, directory: pathlib.Path):
        self.directory = directory
        self.directory.mkdir(parents=True, exist_ok=True)

    def _sanitize_filename(self, s: str) -> str:
        # Simple sanitize: hash the string to avoid filesystem issues
        h = hashlib.sha256(s.encode("utf-8")).hexdigest()
        return h

    def write(self, metrics: QueryMetrics):
        filename = f"{self._sanitize_filename(metrics.query_id)}.jsonl"
        path = self.directory / filename
        record = asdict(metrics)
        timestamp_str = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(metrics.timestamp))
        record["timestamp_iso"] = timestamp_str
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")

COLLECTOR = TelemetryCollector()