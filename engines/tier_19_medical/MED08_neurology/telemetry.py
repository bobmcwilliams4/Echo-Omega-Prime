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
        self._query_index = collections.deque(maxlen=10000)
        self._doctrine_hits = 0
        self._doctrine_total = 0
        self._lock = None  # For future thread safety if needed
        self._audit_writer = AuditTrailWriter()
        self._engine_id = ENGINE_ID

    def record_query(self, metrics: QueryMetrics):
        logger.debug(f"Recording query: {metrics}")
        self._queries.append(metrics)
        self._query_index.append((metrics.timestamp, metrics.query_id))
        if metrics.doctrine_matched:
            self._doctrine_hits += 1
        self._doctrine_total += 1
        self._audit_writer.write(metrics)
        if metrics.error:
            self.record_error(metrics.error, "Query error", metrics.query_id)

    def record_error(self, error_type: str, message: str, query_id: typing.Optional[str] = None):
        error_record = {
            "timestamp": time.time(),
            "engine_id": self._engine_id,
            "error_type": error_type,
            "message": message,
            "query_id": query_id
        }
        logger.error(f"Recording error: {error_record}")
        self._errors.append(error_record)
        self._audit_writer.write_error(error_record)

    def get_latency_stats(self) -> dict:
        latencies = [q.latency_ms for q in self._queries if q.latency_ms is not None]
        if not latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = latencies_sorted[int(0.95 * len(latencies_sorted))-1]
        p99 = latencies_sorted[int(0.99 * len(latencies_sorted))-1]
        min_ = min(latencies)
        max_ = max(latencies)
        return {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_,
            "max": max_
        }

    def get_doctrine_hit_rate(self) -> float:
        if self._doctrine_total == 0:
            return 0.0
        return self._doctrine_hits / self._doctrine_total

    def get_error_rate(self, window_hours: float) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        total_queries = sum(1 for q in self._queries if q.timestamp >= window_start)
        total_errors = sum(1 for e in self._errors if e["timestamp"] >= window_start)
        if total_queries == 0:
            return 0.0
        return total_errors / total_queries

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        return sum(1 for q in self._queries if q.timestamp >= one_hour_ago)

    def get_coverage_report(self) -> dict:
        mode_counts = collections.Counter(q.mode for q in self._queries if q.mode)
        cache_hits = sum(1 for q in self._queries if q.cache_hit)
        total = len(self._queries)
        doctrine_hits = self._doctrine_hits
        doctrine_total = self._doctrine_total
        coverage = {
            "total_queries": total,
            "cache_hit_rate": cache_hits / total if total else 0.0,
            "doctrine_hit_rate": doctrine_hits / doctrine_total if doctrine_total else 0.0,
            "mode_distribution": dict(mode_counts),
            "error_count": len(self._errors)
        }
        return coverage

    def export_jsonl(self, path: typing.Union[str, pathlib.Path]) -> int:
        path = pathlib.Path(path)
        count = 0
        with path.open("w", encoding="utf-8") as f:
            for q in self._queries:
                f.write(json.dumps(dataclasses.asdict(q)) + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {path}")
        return count

class AuditTrailWriter:
    def __init__(self, base_dir: typing.Union[str, pathlib.Path] = "./audit_trail"):
        self.base_dir = pathlib.Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.query_file = self.base_dir / "queries.jsonl"
        self.error_file = self.base_dir / "errors.jsonl"
        self._query_fh = self.query_file.open("a", encoding="utf-8")
        self._error_fh = self.error_file.open("a", encoding="utf-8")

    def write(self, metrics: QueryMetrics):
        record = dataclasses.asdict(metrics)
        record["audit_hash"] = self._hash_record(record)
        self._query_fh.write(json.dumps(record) + "\n")
        self._query_fh.flush()

    def write_error(self, error_record: dict):
        error_record = dict(error_record)
        error_record["audit_hash"] = self._hash_record(error_record)
        self._error_fh.write(json.dumps(error_record) + "\n")
        self._error_fh.flush()

    def _hash_record(self, record: dict) -> str:
        s = json.dumps(record, sort_keys=True)
        return hashlib.sha256(s.encode("utf-8")).hexdigest()

    def close(self):
        self._query_fh.close()
        self._error_fh.close()

ENGINE_ID = "MED08"

COLLECTOR = TelemetryCollector()