import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any
from collections import deque, defaultdict
from loguru import logger


ENGINE_ID = "CHEM15"


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
        # Store all queries in a deque for time-based queries (timestamp ascending)
        self._queries: deque[QueryMetrics] = deque()
        # Store errors separately for error rate calculations
        self._errors: deque[Dict[str, Any]] = deque()
        # For coverage report: count doctrine matched vs total per mode
        self._doctrine_counts: Dict[str, Dict[str, int]] = defaultdict(lambda: {"matched": 0, "total": 0})
        # For latency stats cache to avoid recalculating if no new data
        self._latency_cache = None
        self._latency_cache_timestamp = 0
        # For thread safety if needed in future (not implemented here)
        logger.debug("TelemetryCollector initialized")

    def record_query(self, metrics: QueryMetrics):
        logger.debug(f"Recording query metrics: {metrics}")
        self._queries.append(metrics)
        # Update doctrine counts
        mode_stats = self._doctrine_counts[metrics.mode]
        mode_stats["total"] += 1
        if metrics.doctrine_matched:
            mode_stats["matched"] += 1
        # Invalidate latency cache
        self._latency_cache = None

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
        }
        logger.debug(f"Recording error: {error_entry}")
        self._errors.append(error_entry)

    def get_latency_stats(self) -> dict:
        now = time.time()
        # Cache latency stats for 10 seconds to reduce computation
        if self._latency_cache and now - self._latency_cache_timestamp < 10:
            logger.debug("Returning cached latency stats")
            return self._latency_cache

        latencies = [q.latency_ms for q in self._queries if q.latency_ms is not None]
        if not latencies:
            stats = {"avg": 0, "p50": 0, "p95": 0, "p99": 0, "min": 0, "max": 0}
            self._latency_cache = stats
            self._latency_cache_timestamp = now
            logger.debug("No latency data available")
            return stats

        latencies_sorted = sorted(latencies)
        stats = {
            "avg": statistics.mean(latencies),
            "p50": latencies_sorted[int(0.50 * (len(latencies_sorted)-1))],
            "p95": latencies_sorted[int(0.95 * (len(latencies_sorted)-1))],
            "p99": latencies_sorted[int(0.99 * (len(latencies_sorted)-1))],
            "min": latencies_sorted[0],
            "max": latencies_sorted[-1],
        }
        self._latency_cache = stats
        self._latency_cache_timestamp = now
        logger.debug(f"Calculated latency stats: {stats}")
        return stats

    def get_doctrine_hit_rate(self) -> float:
        total = 0
        matched = 0
        for mode, counts in self._doctrine_counts.items():
            total += counts["total"]
            matched += counts["matched"]
        hit_rate = (matched / total) if total > 0 else 0.0
        logger.debug(f"Doctrine hit rate calculated: {hit_rate} ({matched}/{total})")
        return hit_rate

    def get_error_rate(self, window_hours: float) -> float:
        now = time.time()
        window_seconds = window_hours * 3600
        # Count queries and errors in the window
        queries_in_window = 0
        errors_in_window = 0

        # Queries are stored in ascending timestamp order, so we can iterate from right to left
        for q in reversed(self._queries):
            if now - q.timestamp > window_seconds:
                break
            queries_in_window += 1

        for e in reversed(self._errors):
            if now - e["timestamp"] > window_seconds:
                break
            errors_in_window += 1

        error_rate = (errors_in_window / queries_in_window) if queries_in_window > 0 else 0.0
        logger.debug(f"Error rate over last {window_hours} hours: {error_rate} ({errors_in_window}/{queries_in_window})")
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = 0
        for q in reversed(self._queries):
            if q.timestamp < one_hour_ago:
                break
            count += 1
        logger.debug(f"Queries in the last hour: {count}")
        return count

    def get_coverage_report(self) -> dict:
        report = {}
        for mode, counts in self._doctrine_counts.items():
            total = counts["total"]
            matched = counts["matched"]
            coverage = (matched / total) if total > 0 else 0.0
            report[mode] = {
                "total_queries": total,
                "doctrine_matched": matched,
                "coverage": coverage,
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
        logger.debug(f"AuditTrailWriter initialized with directory: {directory}")

    def write(self, metrics: QueryMetrics):
        # Filename: <query_id>.jsonl
        filename = f"{metrics.query_id}.jsonl"
        filepath = self.directory / filename
        record = asdict(metrics)
        try:
            with filepath.open("a", encoding="utf-8") as f:
                f.write(json.dumps(record) + "\n")
            logger.debug(f"Wrote audit trail for query_id={metrics.query_id} to {filepath}")
        except Exception as e:
            logger.error(f"Failed to write audit trail for query_id={metrics.query_id}: {e}")
            raise


COLLECTOR = TelemetryCollector()