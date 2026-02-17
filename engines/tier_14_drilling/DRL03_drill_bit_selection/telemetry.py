import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any
from collections import deque, defaultdict
from loguru import logger


ENGINE_ID = "DRL03"


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
        # Store all queries in a deque for efficient time-based pruning
        self._queries: deque[QueryMetrics] = deque()
        # Store errors as list of dicts with timestamp for time filtering
        self._errors: deque[Dict[str, Any]] = deque()
        # Doctrine coverage counts: mode -> count
        self._doctrine_counts: defaultdict[str, int] = defaultdict(int)
        self._doctrine_matched_counts: defaultdict[str, int] = defaultdict(int)
        # Cache hits count
        self._cache_hits: int = 0
        # Total queries count
        self._total_queries: int = 0

    def record_query(self, metrics: QueryMetrics):
        logger.debug(f"Recording query metrics: {metrics}")
        self._queries.append(metrics)
        self._total_queries += 1
        if metrics.cache_hit:
            self._cache_hits += 1
        if metrics.doctrine_matched:
            self._doctrine_matched_counts[metrics.mode] += 1
        self._doctrine_counts[metrics.mode] += 1
        if metrics.error:
            self.record_error(error_type="query_error", message=metrics.error, query_id=metrics.query_id)
        self._prune_old_entries()

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_record = {
            "timestamp": time.time(),
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
        }
        logger.debug(f"Recording error: {error_record}")
        self._errors.append(error_record)
        self._prune_old_entries()

    def _prune_old_entries(self):
        # Keep only last 24 hours of data for queries and errors
        now = time.time()
        cutoff = now - 24 * 3600
        while self._queries and self._queries[0].timestamp < cutoff:
            old = self._queries.popleft()
            self._total_queries -= 1
            if old.cache_hit:
                self._cache_hits -= 1
            self._doctrine_counts[old.mode] -= 1
            if old.doctrine_matched:
                self._doctrine_matched_counts[old.mode] -= 1
        while self._errors and self._errors[0]["timestamp"] < cutoff:
            self._errors.popleft()

    def get_latency_stats(self) -> Dict[str, float]:
        latencies = [q.latency_ms for q in self._queries if q.latency_ms is not None]
        if not latencies:
            logger.debug("No latency data available for stats")
            return {"avg": 0, "p50": 0, "p95": 0, "p99": 0, "min": 0, "max": 0}
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = latencies_sorted[int(len(latencies_sorted) * 0.95) - 1]
        p99 = latencies_sorted[int(len(latencies_sorted) * 0.99) - 1]
        min_latency = latencies_sorted[0]
        max_latency = latencies_sorted[-1]
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

    def get_doctrine_hit_rate(self) -> float:
        total = sum(self._doctrine_counts.values())
        matched = sum(self._doctrine_matched_counts.values())
        if total == 0:
            logger.debug("No doctrine data available for hit rate")
            return 0.0
        hit_rate = matched / total
        logger.debug(f"Doctrine hit rate computed: {hit_rate} ({matched}/{total})")
        return hit_rate

    def get_error_rate(self, window_hours: int) -> float:
        now = time.time()
        cutoff = now - window_hours * 3600
        errors_in_window = [e for e in self._errors if e["timestamp"] >= cutoff]
        queries_in_window = [q for q in self._queries if q.timestamp >= cutoff]
        total_queries = len(queries_in_window)
        total_errors = len(errors_in_window)
        if total_queries == 0:
            logger.debug("No queries in window for error rate calculation")
            return 0.0
        error_rate = total_errors / total_queries
        logger.debug(f"Error rate over last {window_hours} hours: {error_rate} ({total_errors}/{total_queries})")
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        cutoff = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= cutoff)
        logger.debug(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {}
        for mode in self._doctrine_counts.keys():
            total = self._doctrine_counts[mode]
            matched = self._doctrine_matched_counts.get(mode, 0)
            coverage = matched / total if total > 0 else 0.0
            report[mode] = {
                "total": total,
                "matched": matched,
                "coverage": coverage,
            }
        logger.debug(f"Coverage report generated: {report}")
        return report

    def export_jsonl(self, path: pathlib.Path) -> int:
        count = 0
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            for q in self._queries:
                record = asdict(q)
                f.write(json.dumps(record) + "\n")
                count += 1
        logger.info(f"Exported {count} query records to {path}")
        return count


class AuditTrailWriter:
    def __init__(self, directory: pathlib.Path):
        self.directory = directory
        self.directory.mkdir(parents=True, exist_ok=True)

    def write(self, metrics: QueryMetrics):
        filename = f"{metrics.query_id}.jsonl"
        filepath = self.directory / filename
        record = asdict(metrics)
        try:
            with filepath.open("a", encoding="utf-8") as f:
                f.write(json.dumps(record) + "\n")
            logger.debug(f"Audit trail written for query_id={metrics.query_id} at {filepath}")
        except Exception as e:
            logger.error(f"Failed to write audit trail for query_id={metrics.query_id}: {e}")


COLLECTOR = TelemetryCollector()