import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any
from collections import deque, defaultdict, Counter
from loguru import logger


ENGINE_ID = "AGI03"


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
        self._queries: List[QueryMetrics] = []
        self._errors: deque = deque()
        self._error_counter: Counter = Counter()
        self._latencies: List[float] = []
        self._doctrine_hits: int = 0
        self._total_queries: int = 0
        self._query_timestamps: deque = deque()
        self._lock = None  # placeholder if threading.Lock needed
        self._mode_counter: Counter = Counter()
        self._confidence_values: List[float] = []
        self._cache_hits: int = 0
        self._query_id_set: set = set()

    def record_query(self, metrics: QueryMetrics):
        if metrics.query_id in self._query_id_set:
            logger.warning(f"Duplicate query_id detected: {metrics.query_id}")
            return
        self._query_id_set.add(metrics.query_id)
        self._queries.append(metrics)
        self._total_queries += 1
        self._latencies.append(metrics.latency_ms)
        if metrics.doctrine_matched:
            self._doctrine_hits += 1
        if metrics.cache_hit:
            self._cache_hits += 1
        self._mode_counter[metrics.mode] += 1
        if metrics.confidence is not None:
            self._confidence_values.append(metrics.confidence)
        self._query_timestamps.append(metrics.timestamp)
        if metrics.error:
            self.record_error(metrics.error, f"Error in query {metrics.query_id}", metrics.query_id)
        self._cleanup_old_entries()

    def record_error(self, error_type: str, message: str, query_id: Optional[str]):
        now = time.time()
        error_entry = {
            "timestamp": now,
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
        }
        self._errors.append(error_entry)
        self._error_counter[error_type] += 1
        self._cleanup_old_entries()

    def _cleanup_old_entries(self):
        cutoff = time.time() - 3600
        while self._query_timestamps and self._query_timestamps[0] < cutoff:
            old_ts = self._query_timestamps.popleft()
        while self._errors and self._errors[0]["timestamp"] < cutoff:
            old_error = self._errors.popleft()

    def get_latency_stats(self) -> Dict[str, float]:
        if not self._latencies:
            return {"avg": 0, "p50": 0, "p95": 0, "p99": 0, "min": 0, "max": 0}
        lat_sorted = sorted(self._latencies)
        avg = statistics.mean(self._latencies)
        p50 = lat_sorted[int(len(lat_sorted) * 0.5)]
        p95 = lat_sorted[int(len(lat_sorted) * 0.95) - 1]
        p99 = lat_sorted[int(len(lat_sorted) * 0.99) - 1]
        return {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": lat_sorted[0],
            "max": lat_sorted[-1],
        }

    def get_doctrine_hit_rate(self) -> float:
        if self._total_queries == 0:
            return 0.0
        return self._doctrine_hits / self._total_queries

    def get_error_rate(self, window_hours: int) -> float:
        now = time.time()
        cutoff = now - window_hours * 3600
        error_count = sum(1 for e in self._errors if e["timestamp"] >= cutoff)
        query_count = sum(1 for q in self._queries if q.timestamp >= cutoff)
        if query_count == 0:
            return 0.0
        return error_count / query_count

    def queries_last_hour(self) -> int:
        cutoff = time.time() - 3600
        count = sum(1 for q in self._queries if q.timestamp >= cutoff)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        modes = dict(self._mode_counter)
        avg_confidence = statistics.mean(self._confidence_values) if self._confidence_values else None
        cache_hit_rate = self._cache_hits / self._total_queries if self._total_queries else 0.0
        doctrine_hit_rate = self.get_doctrine_hit_rate()
        error_rate_1h = self.get_error_rate(1)
        latency_stats = self.get_latency_stats()
        coverage = {
            "total_queries": self._total_queries,
            "modes": modes,
            "avg_confidence": avg_confidence,
            "cache_hit_rate": cache_hit_rate,
            "doctrine_hit_rate": doctrine_hit_rate,
            "error_rate_1h": error_rate_1h,
            "latency_stats": latency_stats,
        }
        return coverage

    def export_jsonl(self, path: pathlib.Path) -> int:
        count = 0
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            for metric in self._queries:
                data = asdict(metric)
                json_line = json.dumps(data)
                f.write(json_line + "\n")
                count += 1
        return count


class AuditTrailWriter:
    def __init__(self, directory: pathlib.Path):
        self.directory = directory
        self.directory.mkdir(parents=True, exist_ok=True)

    def write(self, metrics: QueryMetrics):
        filename = f"{metrics.query_id}.jsonl"
        filepath = self.directory / filename
        data = asdict(metrics)
        json_line = json.dumps(data)
        try:
            with filepath.open("a", encoding="utf-8") as f:
                f.write(json_line + "\n")
        except Exception as e:
            logger.error(f"Failed to write audit trail for {metrics.query_id}: {e}")


COLLECTOR = TelemetryCollector()