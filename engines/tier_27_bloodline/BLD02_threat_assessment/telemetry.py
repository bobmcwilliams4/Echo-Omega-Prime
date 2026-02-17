import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any
from collections import deque, defaultdict
from loguru import logger


ENGINE_ID = "BLD02"


@dataclass
class QueryMetrics:
    query_id: str
    engine_id: str
    timestamp: float
    latency_ms: float
    cache_hit: bool
    doctrine_matched: bool
    mode: str
    confidence: Optional[float] = None
    error: Optional[str] = None


class TelemetryCollector:
    def __init__(self):
        # Store all queries in a deque for time-based queries, maxlen to limit memory usage
        self._queries: deque[QueryMetrics] = deque(maxlen=100_000)
        # Error records: list of tuples (timestamp, error_type, message, query_id)
        self._errors: deque[Dict[str, Any]] = deque(maxlen=50_000)
        # For coverage report: count queries by mode and doctrine_matched
        self._mode_counts: defaultdict[str, int] = defaultdict(int)
        self._doctrine_hits: int = 0
        self._total_queries: int = 0
        # Cache hit counts
        self._cache_hits: int = 0
        # Locking is not implemented here; assumed single-threaded or external synchronization

    def record_query(self, metrics: QueryMetrics):
        logger.debug(f"Recording query metrics: {metrics}")
        self._queries.append(metrics)
        self._total_queries += 1
        if metrics.cache_hit:
            self._cache_hits += 1
        if metrics.doctrine_matched:
            self._doctrine_hits += 1
        self._mode_counts[metrics.mode] += 1
        if metrics.error:
            self.record_error(metrics.error, "Error recorded in query metrics", metrics.query_id)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        timestamp = time.time()
        error_record = {
            "timestamp": timestamp,
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
        }
        logger.warning(f"Recording error: {error_record}")
        self._errors.append(error_record)

    def get_latency_stats(self) -> Dict[str, float]:
        latencies = [q.latency_ms for q in self._queries if q.latency_ms is not None]
        if not latencies:
            logger.debug("No latency data available for stats")
            return {"avg": 0.0, "p50": 0.0, "p95": 0.0, "p99": 0.0, "min": 0.0, "max": 0.0}
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)
        min_latency = min(latencies)
        max_latency = max(latencies)
        stats = {"avg": avg, "p50": p50, "p95": p95, "p99": p99, "min": min_latency, "max": max_latency}
        logger.debug(f"Latency stats computed: {stats}")
        return stats

    def _percentile(self, data: List[float], percentile: float) -> float:
        size = len(data)
        if size == 0:
            return 0.0
        sorted_data = sorted(data)
        k = (size - 1) * (percentile / 100)
        f = int(k)
        c = f + 1
        if c >= size:
            return sorted_data[f]
        d0 = sorted_data[f] * (c - k)
        d1 = sorted_data[c] * (k - f)
        return d0 + d1

    def get_doctrine_hit_rate(self) -> float:
        if self._total_queries == 0:
            logger.debug("No queries recorded, doctrine hit rate is 0.0")
            return 0.0
        rate = self._doctrine_hits / self._total_queries
        logger.debug(f"Doctrine hit rate computed: {rate}")
        return rate

    def get_error_rate(self, window_hours: float) -> float:
        now = time.time()
        window_seconds = window_hours * 3600
        start_time = now - window_seconds
        errors_in_window = [e for e in self._errors if e["timestamp"] >= start_time]
        queries_in_window = [q for q in self._queries if q.timestamp >= start_time]
        if not queries_in_window:
            logger.debug("No queries in window, error rate is 0.0")
            return 0.0
        rate = len(errors_in_window) / len(queries_in_window)
        logger.debug(f"Error rate over last {window_hours} hours: {rate}")
        return rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= one_hour_ago)
        logger.debug(f"Queries in the last hour: {count}")
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {
            "total_queries": self._total_queries,
            "cache_hit_rate": (self._cache_hits / self._total_queries) if self._total_queries > 0 else 0.0,
            "doctrine_hit_rate": self.get_doctrine_hit_rate(),
            "mode_distribution": dict(self._mode_counts),
            "error_count": len(self._errors),
        }
        logger.debug(f"Coverage report generated: {report}")
        return report

    def export_jsonl(self, path: pathlib.Path) -> int:
        count = 0
        try:
            with path.open("w", encoding="utf-8") as f:
                for q in self._queries:
                    record = asdict(q)
                    f.write(json.dumps(record) + "\n")
                    count += 1
            logger.info(f"Exported {count} query records to {path}")
        except Exception as e:
            logger.error(f"Failed to export telemetry data to {path}: {e}")
            raise
        return count


class AuditTrailWriter:
    def __init__(self, directory: pathlib.Path):
        self.directory = directory
        self.directory.mkdir(parents=True, exist_ok=True)
        logger.debug(f"AuditTrailWriter initialized at directory: {self.directory}")

    def write(self, metrics: QueryMetrics) -> None:
        filename = f"{metrics.query_id}.jsonl"
        filepath = self.directory / filename
        record = asdict(metrics)
        try:
            with filepath.open("a", encoding="utf-8") as f:
                f.write(json.dumps(record) + "\n")
            logger.debug(f"Audit trail written for query_id {metrics.query_id} at {filepath}")
        except Exception as e:
            logger.error(f"Failed to write audit trail for query_id {metrics.query_id}: {e}")
            raise


COLLECTOR = TelemetryCollector()