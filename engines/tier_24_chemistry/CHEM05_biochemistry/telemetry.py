import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any
import collections
from loguru import logger


ENGINE_ID = "CHEM05"


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
        self._queries: List[QueryMetrics] = []
        self._errors: collections.deque = collections.deque()
        self._error_counts: collections.Counter = collections.Counter()
        self._lock = None  # Placeholder for threading.Lock if needed in future
        self._audit_writer = AuditTrailWriter()
        logger.debug("TelemetryCollector initialized")

    def record_query(self, metrics: QueryMetrics):
        logger.debug(f"Recording query metrics: {metrics}")
        self._queries.append(metrics)
        self._audit_writer.write(metrics)
        if metrics.error:
            self.record_error(metrics.error, "Error recorded in query metrics", metrics.query_id)

    def record_error(self, error_type: str, message: str, query_id: Optional[str]):
        timestamp = time.time()
        error_record = {
            "timestamp": timestamp,
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
        }
        logger.debug(f"Recording error: {error_record}")
        self._errors.append(error_record)
        self._error_counts[error_type] += 1
        # Keep errors only for last 24 hours to limit memory
        cutoff = timestamp - 86400
        while self._errors and self._errors[0]["timestamp"] < cutoff:
            old_error = self._errors.popleft()
            self._error_counts[old_error["error_type"]] -= 1
            if self._error_counts[old_error["error_type"]] <= 0:
                del self._error_counts[old_error["error_type"]]

    def get_latency_stats(self) -> Dict[str, float]:
        latencies = [q.latency_ms for q in self._queries if q.latency_ms is not None]
        if not latencies:
            logger.debug("No latencies recorded, returning zeros")
            return {"avg": 0.0, "p50": 0.0, "p95": 0.0, "p99": 0.0, "min": 0.0, "max": 0.0}
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = self._percentile(latencies_sorted, 95)
        p99 = self._percentile(latencies_sorted, 99)
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

    def _percentile(self, data: List[float], percentile: float) -> float:
        if not data:
            return 0.0
        k = (len(data)-1) * (percentile/100)
        f = int(k)
        c = min(f+1, len(data)-1)
        if f == c:
            return data[int(k)]
        d0 = data[f] * (c - k)
        d1 = data[c] * (k - f)
        return d0 + d1

    def get_doctrine_hit_rate(self) -> float:
        total = len(self._queries)
        if total == 0:
            logger.debug("No queries recorded, doctrine hit rate is 0.0")
            return 0.0
        hits = sum(1 for q in self._queries if q.doctrine_matched)
        rate = hits / total
        logger.debug(f"Doctrine hit rate calculated: {rate} ({hits}/{total})")
        return rate

    def get_error_rate(self, window_hours: int) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        queries_in_window = [q for q in self._queries if q.timestamp >= window_start]
        if not queries_in_window:
            logger.debug(f"No queries in the last {window_hours} hours, error rate is 0.0")
            return 0.0
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        error_rate = len(errors_in_window) / len(queries_in_window)
        logger.debug(f"Error rate for last {window_hours} hours: {error_rate} ({len(errors_in_window)}/{len(queries_in_window)})")
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        cutoff = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= cutoff)
        logger.debug(f"Queries in the last hour: {count}")
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        # Coverage report includes:
        # - total queries
        # - queries per mode
        # - doctrine matched count and rate
        # - cache hit rate
        total = len(self._queries)
        if total == 0:
            logger.debug("No queries recorded, returning empty coverage report")
            return {
                "total_queries": 0,
                "queries_per_mode": {},
                "doctrine_matched_count": 0,
                "doctrine_hit_rate": 0.0,
                "cache_hit_rate": 0.0,
            }
        queries_per_mode = collections.Counter(q.mode for q in self._queries)
        doctrine_matched_count = sum(1 for q in self._queries if q.doctrine_matched)
        cache_hit_count = sum(1 for q in self._queries if q.cache_hit)
        report = {
            "total_queries": total,
            "queries_per_mode": dict(queries_per_mode),
            "doctrine_matched_count": doctrine_matched_count,
            "doctrine_hit_rate": doctrine_matched_count / total,
            "cache_hit_rate": cache_hit_count / total,
        }
        logger.debug(f"Coverage report generated: {report}")
        return report

    def export_jsonl(self, path: pathlib.Path) -> int:
        logger.debug(f"Exporting telemetry data to JSONL at {path}")
        count = 0
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            for q in self._queries:
                record = asdict(q)
                f.write(json.dumps(record) + "\n")
                count += 1
        logger.debug(f"Exported {count} query records to {path}")
        return count


class AuditTrailWriter:
    def __init__(self, directory: Optional[pathlib.Path] = None):
        if directory is None:
            directory = pathlib.Path("./audit_trail")
        self.directory = directory
        self.directory.mkdir(parents=True, exist_ok=True)
        logger.debug(f"AuditTrailWriter initialized with directory {self.directory}")

    def write(self, metrics: QueryMetrics):
        filename = f"{metrics.query_id}.jsonl"
        filepath = self.directory / filename
        record = asdict(metrics)
        try:
            with filepath.open("a", encoding="utf-8") as f:
                f.write(json.dumps(record) + "\n")
            logger.debug(f"Audit trail written for query_id {metrics.query_id} at {filepath}")
        except Exception as e:
            logger.error(f"Failed to write audit trail for query_id {metrics.query_id}: {e}")


COLLECTOR = TelemetryCollector()