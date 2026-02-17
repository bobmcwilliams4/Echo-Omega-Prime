import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any
from collections import deque, defaultdict, Counter
from loguru import logger


ENGINE_ID = "CHEM07"


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
        # Store all queries in a deque for time-based queries, capped at 100_000 for memory safety
        self._queries: deque[QueryMetrics] = deque(maxlen=100_000)
        # Store errors as tuples (timestamp, error_type, message, query_id)
        self._errors: deque = deque(maxlen=50_000)
        # Counters for doctrine hits and total queries
        self._doctrine_hits = 0
        self._total_queries = 0
        # Latencies for stats
        self._latencies: List[float] = []
        # Mode counts for coverage report
        self._mode_counter: Counter = Counter()
        # Cache hits count
        self._cache_hits = 0
        # Lock for thread safety if needed (not implemented here)
        logger.debug("TelemetryCollector initialized.")

    def record_query(self, metrics: QueryMetrics):
        logger.debug(f"Recording query: {metrics.query_id}")
        self._queries.append(metrics)
        self._total_queries += 1
        if metrics.doctrine_matched:
            self._doctrine_hits += 1
        self._latencies.append(metrics.latency_ms)
        self._mode_counter[metrics.mode] += 1
        if metrics.cache_hit:
            self._cache_hits += 1
        if metrics.error:
            self.record_error("query_error", metrics.error, metrics.query_id)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        timestamp = time.time()
        logger.warning(f"Recording error: {error_type} for query {query_id}: {message}")
        self._errors.append((timestamp, error_type, message, query_id))

    def get_latency_stats(self) -> Dict[str, float]:
        if not self._latencies:
            logger.debug("No latency data available for stats.")
            return {"avg": 0.0, "p50": 0.0, "p95": 0.0, "p99": 0.0, "min": 0.0, "max": 0.0}
        lat_sorted = sorted(self._latencies)
        avg = statistics.mean(lat_sorted)
        p50 = lat_sorted[int(len(lat_sorted) * 0.50)]
        p95 = lat_sorted[int(len(lat_sorted) * 0.95) - 1]
        p99 = lat_sorted[int(len(lat_sorted) * 0.99) - 1]
        min_lat = lat_sorted[0]
        max_lat = lat_sorted[-1]
        stats = {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_lat,
            "max": max_lat,
        }
        logger.debug(f"Latency stats computed: {stats}")
        return stats

    def get_doctrine_hit_rate(self) -> float:
        if self._total_queries == 0:
            logger.debug("No queries recorded, doctrine hit rate is 0.0")
            return 0.0
        rate = self._doctrine_hits / self._total_queries
        logger.debug(f"Doctrine hit rate: {rate:.4f}")
        return rate

    def get_error_rate(self, window_hours: int) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self._errors if e[0] >= window_start]
        queries_in_window = [q for q in self._queries if q.timestamp >= window_start]
        if not queries_in_window:
            logger.debug(f"No queries in last {window_hours} hours, error rate is 0.0")
            return 0.0
        rate = len(errors_in_window) / len(queries_in_window)
        logger.debug(f"Error rate over last {window_hours} hours: {rate:.4f}")
        return rate

    def queries_last_hour(self) -> int:
        now = time.time()
        hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= hour_ago)
        logger.debug(f"Queries in the last hour: {count}")
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        total = self._total_queries if self._total_queries > 0 else 1
        coverage = {
            "total_queries": self._total_queries,
            "doctrine_hit_rate": self.get_doctrine_hit_rate(),
            "cache_hit_rate": self._cache_hits / total,
            "mode_distribution": dict(self._mode_counter),
            "error_count": len(self._errors),
            "error_rate_1h": self.get_error_rate(1),
            "error_rate_24h": self.get_error_rate(24),
            "latency_stats": self.get_latency_stats(),
        }
        logger.debug(f"Coverage report generated: {coverage}")
        return coverage

    def export_jsonl(self, path: pathlib.Path) -> int:
        logger.info(f"Exporting telemetry data to JSONL file at {path}")
        count = 0
        try:
            with path.open("w", encoding="utf-8") as f:
                for query in self._queries:
                    record = asdict(query)
                    f.write(json.dumps(record) + "\n")
                    count += 1
            logger.info(f"Exported {count} records to {path}")
        except Exception as e:
            logger.error(f"Failed to export telemetry data: {e}")
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
            logger.debug(f"Audit trail written for query {metrics.query_id} at {filepath}")
        except Exception as e:
            logger.error(f"Failed to write audit trail for query {metrics.query_id}: {e}")
            raise


COLLECTOR = TelemetryCollector()