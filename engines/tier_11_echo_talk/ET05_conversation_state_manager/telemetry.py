import time
import json
import hashlib
import statistics
import pathlib
import dataclasses
import typing
import collections
from loguru import logger

@dataclasses.dataclass
class QueryMetrics:
    query_id: str
    engine_id: str
    timestamp: float
    latency_ms: float
    cache_hit: bool
    doctrine_matched: bool
    mode: str
    confidence: float
    error: typing.Optional[str] = None

class TelemetryCollector:
    def __init__(self):
        self._queries = []
        self._errors = []
        self._query_by_id = {}
        self._doctrine_matches = 0
        self._total_queries = 0
        self._cache_hits = 0
        self._latencies = []
        self._lock = collections.defaultdict(lambda: None)
        self._audit_writer = AuditTrailWriter()
        self._engine_id = ENGINE_ID

    def record_query(self, metrics: QueryMetrics):
        logger.debug(f"Recording query: {metrics}")
        self._queries.append(metrics)
        self._query_by_id[metrics.query_id] = metrics
        self._total_queries += 1
        self._latencies.append(metrics.latency_ms)
        if metrics.cache_hit:
            self._cache_hits += 1
        if metrics.doctrine_matched:
            self._doctrine_matches += 1
        self._audit_writer.write(metrics)
        if metrics.error:
            self.record_error(metrics.error, "Query error", metrics.query_id)

    def record_error(self, error_type: str, message: str, query_id: typing.Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "engine_id": self._engine_id
        }
        logger.error(f"Error recorded: {error_entry}")
        self._errors.append(error_entry)

    def get_latency_stats(self) -> dict:
        if not self._latencies:
            return {
                "avg": None,
                "p50": None,
                "p95": None,
                "p99": None,
                "min": None,
                "max": None
            }
        sorted_latencies = sorted(self._latencies)
        avg = statistics.mean(sorted_latencies)
        p50 = statistics.median(sorted_latencies)
        p95 = sorted_latencies[int(0.95 * len(sorted_latencies)) - 1]
        p99 = sorted_latencies[int(0.99 * len(sorted_latencies)) - 1]
        min_latency = sorted_latencies[0]
        max_latency = sorted_latencies[-1]
        stats = {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_latency,
            "max": max_latency
        }
        logger.debug(f"Latency stats: {stats}")
        return stats

    def get_doctrine_hit_rate(self) -> float:
        if self._total_queries == 0:
            return 0.0
        hit_rate = self._doctrine_matches / self._total_queries
        logger.debug(f"Doctrine hit rate: {hit_rate}")
        return hit_rate

    def get_error_rate(self, window_hours: float) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        queries_in_window = [q for q in self._queries if q.timestamp >= window_start]
        error_rate = (len(errors_in_window) / len(queries_in_window)) if queries_in_window else 0.0
        logger.debug(f"Error rate in last {window_hours} hours: {error_rate}")
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= one_hour_ago)
        logger.debug(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> dict:
        mode_counter = collections.Counter()
        doctrine_counter = collections.Counter()
        cache_counter = collections.Counter()
        for q in self._queries:
            mode_counter[q.mode] += 1
            doctrine_counter[q.doctrine_matched] += 1
            cache_counter[q.cache_hit] += 1
        report = {
            "total_queries": self._total_queries,
            "by_mode": dict(mode_counter),
            "doctrine_matched": doctrine_counter.get(True, 0),
            "doctrine_not_matched": doctrine_counter.get(False, 0),
            "cache_hits": cache_counter.get(True, 0),
            "cache_misses": cache_counter.get(False, 0),
        }
        logger.debug(f"Coverage report: {report}")
        return report

    def export_jsonl(self, path: typing.Union[str, pathlib.Path]) -> int:
        path = pathlib.Path(path)
        count = 0
        with path.open("w", encoding="utf-8") as f:
            for q in self._queries:
                d = dataclasses.asdict(q)
                f.write(json.dumps(d) + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {path}")
        return count

class AuditTrailWriter:
    def __init__(self, base_dir: typing.Union[str, pathlib.Path] = "./audit_trail"):
        self.base_dir = pathlib.Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def write(self, metrics: QueryMetrics):
        audit_entry = {
            "query_id": metrics.query_id,
            "engine_id": metrics.engine_id,
            "timestamp": metrics.timestamp,
            "latency_ms": metrics.latency_ms,
            "cache_hit": metrics.cache_hit,
            "doctrine_matched": metrics.doctrine_matched,
            "mode": metrics.mode,
            "confidence": metrics.confidence,
            "error": metrics.error
        }
        # Use a hash of query_id for filename safety
        filename = hashlib.sha256(metrics.query_id.encode()).hexdigest() + ".jsonl"
        file_path = self.base_dir / filename
        with file_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(audit_entry) + "\n")
        logger.debug(f"Wrote audit trail for query_id={metrics.query_id} to {file_path}")

ENGINE_ID = "ET05"
COLLECTOR = TelemetryCollector()