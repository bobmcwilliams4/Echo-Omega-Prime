import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any
import collections
from loguru import logger


ENGINE_ID = "DRL06"


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
        # Store all queries in memory for stats and export
        self._queries: List[QueryMetrics] = []
        # Store errors as tuples (timestamp, error_type, message, query_id)
        self._errors: List[Dict[str, Any]] = []
        # For coverage report: count of queries per mode and doctrine hits
        self._mode_counter: collections.Counter = collections.Counter()
        self._doctrine_hits: int = 0
        self._total_queries: int = 0
        # For thread safety in multi-threaded environment, consider locks if needed
        # Here we assume single-threaded or external synchronization
        logger.debug("TelemetryCollector initialized")

    def record_query(self, metrics: QueryMetrics):
        logger.debug(f"Recording query metrics: {metrics}")
        self._queries.append(metrics)
        self._total_queries += 1
        self._mode_counter[metrics.mode] += 1
        if metrics.doctrine_matched:
            self._doctrine_hits += 1
        if metrics.error:
            self.record_error("query_error", metrics.error, metrics.query_id)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        ts = time.time()
        error_record = {
            "timestamp": ts,
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
        }
        logger.debug(f"Recording error: {error_record}")
        self._errors.append(error_record)

    def get_latency_stats(self) -> dict:
        latencies = [q.latency_ms for q in self._queries if q.latency_ms is not None]
        if not latencies:
            logger.debug("No latency data available for stats")
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)
        min_lat = min(latencies)
        max_lat = max(latencies)
        stats = {"avg": avg, "p50": p50, "p95": p95, "p99": p99, "min": min_lat, "max": max_lat}
        logger.debug(f"Latency stats computed: {stats}")
        return stats

    def _percentile(self, data: List[float], percentile: float) -> float:
        size = len(data)
        if size == 0:
            return None
        data_sorted = sorted(data)
        k = (size - 1) * (percentile / 100)
        f = int(k)
        c = f + 1
        if c >= size:
            return data_sorted[-1]
        d0 = data_sorted[f] * (c - k)
        d1 = data_sorted[c] * (k - f)
        return d0 + d1

    def get_doctrine_hit_rate(self) -> float:
        if self._total_queries == 0:
            logger.debug("No queries recorded, doctrine hit rate is 0.0")
            return 0.0
        rate = self._doctrine_hits / self._total_queries
        logger.debug(f"Doctrine hit rate computed: {rate}")
        return rate

    def get_error_rate(self, window_hours: int = 1) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        queries_in_window = [q for q in self._queries if q.timestamp >= window_start]
        if not queries_in_window:
            logger.debug(f"No queries in the last {window_hours} hours, error rate is 0.0")
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

    def get_coverage_report(self) -> dict:
        if self._total_queries == 0:
            logger.debug("No queries recorded, coverage report is empty")
            return {}
        coverage = {}
        for mode, count in self._mode_counter.items():
            coverage[mode] = {
                "count": count,
                "percentage": count / self._total_queries,
            }
        coverage_report = {
            "total_queries": self._total_queries,
            "doctrine_hit_rate": self.get_doctrine_hit_rate(),
            "mode_coverage": coverage,
        }
        logger.debug(f"Coverage report generated: {coverage_report}")
        return coverage_report

    def export_jsonl(self, path: pathlib.Path) -> int:
        if not path.parent.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
        count = 0
        logger.debug(f"Exporting telemetry data to JSONL at {path}")
        with path.open("w", encoding="utf-8") as f:
            for q in self._queries:
                record = asdict(q)
                f.write(json.dumps(record) + "\n")
                count += 1
        logger.info(f"Exported {count} telemetry query records to {path}")
        return count


class AuditTrailWriter:
    def __init__(self, directory: pathlib.Path):
        self.directory = directory
        if not self.directory.exists():
            self.directory.mkdir(parents=True, exist_ok=True)
        logger.debug(f"AuditTrailWriter initialized with directory {self.directory}")

    def write(self, metrics: QueryMetrics) -> None:
        filename = f"{metrics.query_id}.jsonl"
        filepath = self.directory / filename
        record = asdict(metrics)
        logger.debug(f"Writing audit trail for query {metrics.query_id} to {filepath}")
        with filepath.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")


COLLECTOR = TelemetryCollector()