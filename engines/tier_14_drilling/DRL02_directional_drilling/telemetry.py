import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any
from collections import deque, defaultdict
from loguru import logger


ENGINE_ID = "DRL02"


@dataclass
class QueryMetrics:
    query_id: str
    engine_id: str
    timestamp: float  # Unix timestamp in seconds
    latency_ms: float
    cache_hit: bool
    doctrine_matched: bool
    mode: str
    confidence: float
    error: Optional[str] = None


class TelemetryCollector:
    def __init__(self):
        # Store all query metrics in a deque for efficient append and popleft
        self._queries: deque[QueryMetrics] = deque()
        # Store errors as list of dicts with error_type, message, query_id, timestamp
        self._errors: deque[Dict[str, Any]] = deque()
        # For coverage report, track counts per mode and doctrine matched
        self._mode_counts: defaultdict[str, int] = defaultdict(int)
        self._doctrine_hits: int = 0
        self._total_queries: int = 0
        # For latency stats cache
        self._latencies: List[float] = []
        # For error rate calculation, keep timestamps of errors and queries
        self._error_timestamps: deque[float] = deque()
        self._query_timestamps: deque[float] = deque()
        # Lock for thread safety if needed (not implemented here)
        logger.debug("TelemetryCollector initialized")

    def record_query(self, metrics: QueryMetrics):
        logger.debug(f"Recording query: {metrics}")
        self._queries.append(metrics)
        self._latencies.append(metrics.latency_ms)
        self._mode_counts[metrics.mode] += 1
        self._total_queries += 1
        if metrics.doctrine_matched:
            self._doctrine_hits += 1
        self._query_timestamps.append(metrics.timestamp)
        if metrics.error:
            self.record_error("QueryError", metrics.error, metrics.query_id)
        self._cleanup_old_entries()

    def record_error(self, error_type: str, message: str, query_id: Optional[str]):
        timestamp = time.time()
        error_entry = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "timestamp": timestamp,
        }
        logger.debug(f"Recording error: {error_entry}")
        self._errors.append(error_entry)
        self._error_timestamps.append(timestamp)
        self._cleanup_old_entries()

    def _cleanup_old_entries(self):
        # Remove entries older than 24 hours to limit memory usage
        cutoff = time.time() - 24 * 3600
        while self._queries and self._queries[0].timestamp < cutoff:
            old = self._queries.popleft()
            try:
                self._latencies.remove(old.latency_ms)
            except ValueError:
                pass
            self._mode_counts[old.mode] = max(0, self._mode_counts[old.mode] - 1)
            self._total_queries = max(0, self._total_queries - 1)
            if old.doctrine_matched:
                self._doctrine_hits = max(0, self._doctrine_hits - 1)
            if self._query_timestamps and self._query_timestamps[0] < cutoff:
                self._query_timestamps.popleft()

        while self._errors and self._errors[0]["timestamp"] < cutoff:
            self._errors.popleft()
        while self._error_timestamps and self._error_timestamps[0] < cutoff:
            self._error_timestamps.popleft()

    def get_latency_stats(self) -> Dict[str, Optional[float]]:
        if not self._latencies:
            logger.debug("No latencies recorded yet")
            return {
                "avg": None,
                "p50": None,
                "p95": None,
                "p99": None,
                "min": None,
                "max": None,
            }
        sorted_latencies = sorted(self._latencies)
        avg = statistics.mean(sorted_latencies)
        p50 = self._percentile(sorted_latencies, 50)
        p95 = self._percentile(sorted_latencies, 95)
        p99 = self._percentile(sorted_latencies, 99)
        min_latency = sorted_latencies[0]
        max_latency = sorted_latencies[-1]
        stats = {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_latency,
            "max": max_latency,
        }
        logger.debug(f"Latency stats computed: {stats}")
        return stats

    def _percentile(self, data: List[float], percentile: float) -> float:
        if not data:
            return 0.0
        k = (len(data)-1) * (percentile / 100)
        f = int(k)
        c = min(f + 1, len(data) - 1)
        if f == c:
            return data[int(k)]
        d0 = data[f] * (c - k)
        d1 = data[c] * (k - f)
        return d0 + d1

    def get_doctrine_hit_rate(self) -> float:
        if self._total_queries == 0:
            logger.debug("No queries recorded for doctrine hit rate")
            return 0.0
        rate = self._doctrine_hits / self._total_queries
        logger.debug(f"Doctrine hit rate: {rate} ({self._doctrine_hits}/{self._total_queries})")
        return rate

    def get_error_rate(self, window_hours: int) -> float:
        now = time.time()
        cutoff = now - window_hours * 3600
        errors_in_window = [ts for ts in self._error_timestamps if ts >= cutoff]
        queries_in_window = [ts for ts in self._query_timestamps if ts >= cutoff]
        if not queries_in_window:
            logger.debug("No queries in window for error rate calculation")
            return 0.0
        rate = len(errors_in_window) / len(queries_in_window)
        logger.debug(f"Error rate over last {window_hours} hours: {rate} ({len(errors_in_window)}/{len(queries_in_window)})")
        return rate

    def queries_last_hour(self) -> int:
        now = time.time()
        cutoff = now - 3600
        count = sum(1 for ts in self._query_timestamps if ts >= cutoff)
        logger.debug(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        # Coverage report: distribution of modes, doctrine hit rate, error count
        mode_distribution = dict(self._mode_counts)
        doctrine_hit_rate = self.get_doctrine_hit_rate()
        error_count = len(self._errors)
        coverage = {
            "total_queries": self._total_queries,
            "mode_distribution": mode_distribution,
            "doctrine_hit_rate": doctrine_hit_rate,
            "error_count": error_count,
        }
        logger.debug(f"Coverage report generated: {coverage}")
        return coverage

    def export_jsonl(self, path: pathlib.Path) -> int:
        # Export all queries as JSONL to file at path
        # Return number of records exported
        logger.debug(f"Exporting telemetry data to {path}")
        path.parent.mkdir(parents=True, exist_ok=True)
        count = 0
        with path.open("w", encoding="utf-8") as f:
            for metric in self._queries:
                record = asdict(metric)
                json_line = json.dumps(record)
                f.write(json_line + "\n")
                count += 1
        logger.info(f"Exported {count} telemetry records to {path}")
        return count


class AuditTrailWriter:
    def __init__(self, directory: pathlib.Path):
        self.directory = directory
        self.directory.mkdir(parents=True, exist_ok=True)
        logger.debug(f"AuditTrailWriter initialized at directory {self.directory}")

    def write(self, metrics: QueryMetrics):
        # Write a single JSONL audit trail file per query
        # Filename: <query_id>.jsonl
        filename = f"{metrics.query_id}.jsonl"
        filepath = self.directory / filename
        record = asdict(metrics)
        json_line = json.dumps(record)
        logger.debug(f"Writing audit trail for query_id={metrics.query_id} to {filepath}")
        with filepath.open("w", encoding="utf-8") as f:
            f.write(json_line + "\n")


COLLECTOR = TelemetryCollector()