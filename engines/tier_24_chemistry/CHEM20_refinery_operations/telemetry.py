import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any
import collections
from loguru import logger


ENGINE_ID = "CHEM20"


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
        self._queries: collections.deque[QueryMetrics] = collections.deque()
        # Store errors as list of dicts with timestamp and error info
        self._errors: collections.deque[Dict[str, Any]] = collections.deque()
        # Lock for thread safety if needed in future (not implemented here)
        # self._lock = threading.Lock()
        logger.debug("TelemetryCollector initialized")

    def record_query(self, metrics: QueryMetrics):
        logger.debug(f"Recording query: {metrics.query_id}")
        self._queries.append(metrics)
        # Also record error if present
        if metrics.error:
            self.record_error("QueryError", metrics.error, metrics.query_id)
        self._prune_old_data()

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        timestamp = time.time()
        error_record = {
            "timestamp": timestamp,
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
        }
        logger.debug(f"Recording error: {error_record}")
        self._errors.append(error_record)
        self._prune_old_data()

    def _prune_old_data(self):
        # Prune queries and errors older than 24 hours to limit memory usage
        now = time.time()
        cutoff = now - 24 * 3600
        while self._queries and self._queries[0].timestamp < cutoff:
            removed = self._queries.popleft()
            logger.trace(f"Pruned old query: {removed.query_id}")
        while self._errors and self._errors[0]["timestamp"] < cutoff:
            removed = self._errors.popleft()
            logger.trace(f"Pruned old error: {removed}")

    def get_latency_stats(self) -> Dict[str, Optional[float]]:
        latencies = [q.latency_ms for q in self._queries if q.latency_ms is not None]
        if not latencies:
            logger.debug("No latency data available for stats")
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
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

    @staticmethod
    def _percentile(data: List[float], percentile: float) -> float:
        if not data:
            return None
        k = (len(data)-1) * (percentile/100)
        f = int(k)
        c = f + 1
        if c >= len(data):
            return data[-1]
        d0 = data[f] * (c - k)
        d1 = data[c] * (k - f)
        return d0 + d1

    def get_doctrine_hit_rate(self) -> float:
        total = len(self._queries)
        if total == 0:
            logger.debug("No queries to calculate doctrine hit rate")
            return 0.0
        hits = sum(1 for q in self._queries if q.doctrine_matched)
        rate = hits / total
        logger.debug(f"Doctrine hit rate calculated: {rate} ({hits}/{total})")
        return rate

    def get_error_rate(self, window_hours: int) -> float:
        now = time.time()
        cutoff = now - window_hours * 3600
        total = 0
        errors = 0
        # Count queries in window
        for q in reversed(self._queries):
            if q.timestamp < cutoff:
                break
            total += 1
            if q.error:
                errors += 1
        if total == 0:
            logger.debug(f"No queries in the last {window_hours} hours to calculate error rate")
            return 0.0
        rate = errors / total
        logger.debug(f"Error rate over last {window_hours} hours: {rate} ({errors}/{total})")
        return rate

    def queries_last_hour(self) -> int:
        now = time.time()
        cutoff = now - 3600
        count = 0
        for q in reversed(self._queries):
            if q.timestamp < cutoff:
                break
            count += 1
        logger.debug(f"Queries in the last hour: {count}")
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        # Coverage report includes:
        # - total queries
        # - doctrine matched count and rate
        # - cache hit count and rate
        # - mode distribution
        # - confidence stats
        total = len(self._queries)
        if total == 0:
            logger.debug("No queries to generate coverage report")
            return {
                "total_queries": 0,
                "doctrine_matched": 0,
                "doctrine_hit_rate": 0.0,
                "cache_hits": 0,
                "cache_hit_rate": 0.0,
                "mode_distribution": {},
                "confidence_stats": {},
            }
        doctrine_matched = sum(1 for q in self._queries if q.doctrine_matched)
        cache_hits = sum(1 for q in self._queries if q.cache_hit)
        mode_counts = collections.Counter(q.mode for q in self._queries)
        confidences = [q.confidence for q in self._queries if q.confidence is not None]
        confidence_stats = {}
        if confidences:
            confidence_stats = {
                "avg": statistics.mean(confidences),
                "min": min(confidences),
                "max": max(confidences),
                "p50": statistics.median(confidences),
                "p95": self._percentile(sorted(confidences), 95),
                "p99": self._percentile(sorted(confidences), 99),
            }
        report = {
            "total_queries": total,
            "doctrine_matched": doctrine_matched,
            "doctrine_hit_rate": doctrine_matched / total,
            "cache_hits": cache_hits,
            "cache_hit_rate": cache_hits / total,
            "mode_distribution": dict(mode_counts),
            "confidence_stats": confidence_stats,
        }
        logger.debug(f"Coverage report generated: {report}")
        return report

    def export_jsonl(self, path: pathlib.Path) -> int:
        # Export all queries as JSONL to the given path
        # Returns number of records exported
        if not path.parent.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Created directory for export: {path.parent}")
        count = 0
        with path.open("w", encoding="utf-8") as f:
            for q in self._queries:
                record = asdict(q)
                # Convert timestamp to ISO8601 string for readability
                record["timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(q.timestamp))
                f.write(json.dumps(record) + "\n")
                count += 1
        logger.info(f"Exported {count} query records to {path}")
        return count


class AuditTrailWriter:
    def __init__(self, directory: pathlib.Path):
        self.directory = directory
        if not self.directory.exists():
            self.directory.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Created audit trail directory: {self.directory}")

    def write(self, metrics: QueryMetrics):
        # Write one JSONL file per query, filename is hash of query_id + timestamp
        # This avoids collisions and allows easy lookup
        timestamp_str = time.strftime("%Y%m%dT%H%M%S", time.gmtime(metrics.timestamp))
        base_str = f"{metrics.query_id}_{timestamp_str}"
        filename_hash = hashlib.sha256(base_str.encode("utf-8")).hexdigest()[:16]
        filename = f"{filename_hash}.jsonl"
        filepath = self.directory / filename
        record = asdict(metrics)
        record["timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(metrics.timestamp))
        try:
            with filepath.open("a", encoding="utf-8") as f:
                f.write(json.dumps(record) + "\n")
            logger.debug(f"Audit trail written for query {metrics.query_id} to {filepath}")
        except Exception as e:
            logger.error(f"Failed to write audit trail for query {metrics.query_id}: {e}")


COLLECTOR = TelemetryCollector()