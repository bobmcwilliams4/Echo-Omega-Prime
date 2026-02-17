import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any
from collections import deque, defaultdict, Counter
from loguru import logger


ENGINE_ID = "BLD04"


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
        self._doctrine_hits: int = 0
        self._total_queries: int = 0
        self._latencies: List[float] = []
        self._error_counter: Counter = Counter()
        self._cache_hits: int = 0
        self._mode_counter: Counter = Counter()
        self._confidence_values: List[float] = []
        self._lock = None  # placeholder for thread safety if needed

    def record_query(self, metrics: QueryMetrics):
        now = time.time()
        self._queries.append(metrics)
        self._total_queries += 1
        self._latencies.append(metrics.latency_ms)
        if metrics.doctrine_matched:
            self._doctrine_hits += 1
        if metrics.cache_hit:
            self._cache_hits += 1
        self._mode_counter[metrics.mode] += 1
        self._confidence_values.append(metrics.confidence)
        if metrics.error:
            self.record_error(metrics.error, "Error recorded in query metrics", metrics.query_id)
        self._cleanup_old_entries(now)

    def record_error(self, error_type: str, message: str, query_id: Optional[str]):
        now = time.time()
        error_record = {
            "timestamp": now,
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
        }
        self._errors.append(error_record)
        self._error_counter[error_type] += 1
        self._cleanup_old_entries(now)

    def _cleanup_old_entries(self, now: float):
        cutoff = now - 3600  # 1 hour window for some metrics
        while self._queries and self._queries[0].timestamp < cutoff:
            old = self._queries.popleft()
            self._latencies.remove(old.latency_ms)
            self._total_queries -= 1
            if old.doctrine_matched:
                self._doctrine_hits -= 1
            if old.cache_hit:
                self._cache_hits -= 1
            self._mode_counter[old.mode] -= 1
            self._confidence_values.remove(old.confidence)
            if old.error:
                self._error_counter[old.error] -= 1
        while self._errors and self._errors[0]["timestamp"] < cutoff:
            old_err = self._errors.popleft()
            self._error_counter[old_err["error_type"]] -= 1

    def get_latency_stats(self) -> dict:
        if not self._latencies:
            return {"avg": 0, "p50": 0, "p95": 0, "p99": 0, "min": 0, "max": 0}
        lat_sorted = sorted(self._latencies)
        avg = statistics.mean(lat_sorted)
        p50 = lat_sorted[int(len(lat_sorted)*0.50)]
        p95 = lat_sorted[int(len(lat_sorted)*0.95)-1]
        p99 = lat_sorted[int(len(lat_sorted)*0.99)-1]
        min_v = lat_sorted[0]
        max_v = lat_sorted[-1]
        return {"avg": avg, "p50": p50, "p95": p95, "p99": p99, "min": min_v, "max": max_v}

    def get_doctrine_hit_rate(self) -> float:
        if self._total_queries == 0:
            return 0.0
        return self._doctrine_hits / self._total_queries

    def get_error_rate(self, window_hours: int) -> float:
        now = time.time()
        cutoff = now - window_hours * 3600
        error_count = 0
        query_count = 0
        for q in self._queries:
            if q.timestamp >= cutoff:
                query_count += 1
                if q.error:
                    error_count += 1
        if query_count == 0:
            return 0.0
        return error_count / query_count

    def queries_last_hour(self) -> int:
        now = time.time()
        cutoff = now - 3600
        count = 0
        for q in reversed(self._queries):
            if q.timestamp >= cutoff:
                count += 1
            else:
                break
        return count

    def get_coverage_report(self) -> dict:
        mode_distribution = dict(self._mode_counter)
        avg_confidence = statistics.mean(self._confidence_values) if self._confidence_values else 0.0
        cache_hit_rate = self._cache_hits / self._total_queries if self._total_queries else 0.0
        error_types = dict(self._error_counter)
        return {
            "total_queries": self._total_queries,
            "mode_distribution": mode_distribution,
            "average_confidence": avg_confidence,
            "cache_hit_rate": cache_hit_rate,
            "error_types_count": error_types,
            "doctrine_hit_rate": self.get_doctrine_hit_rate(),
            "latency_stats": self.get_latency_stats(),
        }

    def export_jsonl(self, path: pathlib.Path) -> int:
        count = 0
        try:
            with path.open("w", encoding="utf-8") as f:
                for q in self._queries:
                    record = asdict(q)
                    f.write(json.dumps(record) + "\n")
                    count += 1
            logger.info(f"Exported {count} telemetry records to {path}")
        except Exception as e:
            logger.error(f"Failed to export telemetry to {path}: {e}")
        return count


class AuditTrailWriter:
    def __init__(self, directory: pathlib.Path):
        self.directory = directory
        self.directory.mkdir(parents=True, exist_ok=True)

    def write(self, query_metrics: QueryMetrics):
        filename = f"{query_metrics.query_id}.jsonl"
        filepath = self.directory / filename
        try:
            with filepath.open("a", encoding="utf-8") as f:
                record = asdict(query_metrics)
                f.write(json.dumps(record) + "\n")
            logger.debug(f"Wrote audit trail for query {query_metrics.query_id} to {filepath}")
        except Exception as e:
            logger.error(f"Failed to write audit trail for query {query_metrics.query_id}: {e}")


COLLECTOR = TelemetryCollector()