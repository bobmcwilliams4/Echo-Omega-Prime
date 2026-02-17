import time
import json
import hashlib
import statistics
import pathlib
import dataclasses
import typing
import collections
from loguru import logger

ENGINE_ID = "AUTO15"

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
        self._queries = collections.deque()  # store QueryMetrics
        self._errors = collections.deque()   # store (timestamp, error_type, message, query_id)
        self._lock = None  # placeholder for thread safety if needed
        self._audit_writer = AuditTrailWriter()
        self._max_retention_seconds = 24 * 3600  # keep 24 hours of data

    def _prune_old(self):
        cutoff = time.time() - self._max_retention_seconds
        while self._queries and self._queries[0].timestamp < cutoff:
            self._queries.popleft()
        while self._errors and self._errors[0][0] < cutoff:
            self._errors.popleft()

    def record_query(self, metrics: QueryMetrics):
        if metrics.engine_id != ENGINE_ID:
            logger.warning(f"record_query called with mismatched engine_id {metrics.engine_id}")
            return
        self._queries.append(metrics)
        self._audit_writer.write(metrics)
        self._prune_old()

    def record_error(self, error_type: str, message: str, query_id: str):
        ts = time.time()
        self._errors.append((ts, error_type, message, query_id))
        self._prune_old()

    def get_latency_stats(self) -> dict:
        latencies = [q.latency_ms for q in self._queries if q.error is None]
        if not latencies:
            return {"avg": 0, "p50": 0, "p95": 0, "p99": 0, "min": 0, "max": 0}
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)
        return {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min(latencies),
            "max": max(latencies),
        }

    def _percentile(self, data: typing.List[float], percentile: float) -> float:
        size = len(data)
        if size == 0:
            return 0
        sorted_data = sorted(data)
        k = (size - 1) * (percentile / 100)
        f = int(k)
        c = min(f + 1, size - 1)
        if f == c:
            return sorted_data[int(k)]
        d0 = sorted_data[f] * (c - k)
        d1 = sorted_data[c] * (k - f)
        return d0 + d1

    def get_doctrine_hit_rate(self) -> float:
        total = len(self._queries)
        if total == 0:
            return 0.0
        hits = sum(1 for q in self._queries if q.doctrine_matched)
        return hits / total

    def get_error_rate(self, window_hours: int) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        total = sum(1 for q in self._queries if q.timestamp >= window_start)
        if total == 0:
            return 0.0
        errors = sum(1 for e in self._errors if e[0] >= window_start)
        return errors / total

    def queries_last_hour(self) -> int:
        now = time.time()
        cutoff = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= cutoff)
        return count

    def get_coverage_report(self) -> dict:
        """
        Coverage report includes:
        - total queries
        - queries by mode
        - cache hit rate
        - doctrine matched rate
        - error count last 24h
        - error types count last 24h
        """
        now = time.time()
        cutoff = now - 24 * 3600
        queries_24h = [q for q in self._queries if q.timestamp >= cutoff]
        total = len(queries_24h)
        if total == 0:
            return {
                "total_queries": 0,
                "queries_by_mode": {},
                "cache_hit_rate": 0.0,
                "doctrine_matched_rate": 0.0,
                "error_count": 0,
                "error_types": {},
            }
        mode_counter = collections.Counter(q.mode for q in queries_24h)
        cache_hits = sum(1 for q in queries_24h if q.cache_hit)
        doctrine_hits = sum(1 for q in queries_24h if q.doctrine_matched)
        errors_24h = [e for e in self._errors if e[0] >= cutoff]
        error_count = len(errors_24h)
        error_types_counter = collections.Counter(e[1] for e in errors_24h)

        return {
            "total_queries": total,
            "queries_by_mode": dict(mode_counter),
            "cache_hit_rate": cache_hits / total,
            "doctrine_matched_rate": doctrine_hits / total,
            "error_count": error_count,
            "error_types": dict(error_types_counter),
        }

    def export_jsonl(self, path: typing.Union[str, pathlib.Path]) -> int:
        path = pathlib.Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        count = 0
        with path.open("w", encoding="utf-8") as f:
            for q in self._queries:
                record = dataclasses.asdict(q)
                json.dump(record, f)
                f.write("\n")
                count += 1
        return count

class AuditTrailWriter:
    def __init__(self, directory: typing.Union[str, pathlib.Path] = "audit_trail"):
        self.directory = pathlib.Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)

    def _get_filename(self, query_id: str) -> pathlib.Path:
        # Use hash of query_id to avoid filesystem issues
        h = hashlib.sha256(query_id.encode("utf-8")).hexdigest()
        return self.directory / f"{h}.jsonl"

    def write(self, metrics: QueryMetrics):
        filename = self._get_filename(metrics.query_id)
        record = dataclasses.asdict(metrics)
        try:
            with filename.open("a", encoding="utf-8") as f:
                json.dump(record, f)
                f.write("\n")
        except Exception as e:
            logger.error(f"Failed to write audit trail for query_id={metrics.query_id}: {e}")

COLLECTOR = TelemetryCollector()