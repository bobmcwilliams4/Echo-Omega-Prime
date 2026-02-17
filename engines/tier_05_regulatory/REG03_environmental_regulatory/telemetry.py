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
        self._query_index = {}  # query_id -> QueryMetrics
        self._doctrine_hits = 0
        self._total_queries = 0
        self._cache_hits = 0
        self._latencies = []
        self._coverage_modes = collections.Counter()
        self._confidence_scores = []
        self._last_hour_queries = collections.deque()
        self._audit_writer = AuditTrailWriter()
        self._lock = None  # Placeholder for threading.Lock if needed

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._query_index[metrics.query_id] = metrics
        self._total_queries += 1
        if metrics.doctrine_matched:
            self._doctrine_hits += 1
        if metrics.cache_hit:
            self._cache_hits += 1
        self._latencies.append(metrics.latency_ms)
        self._coverage_modes[metrics.mode] += 1
        self._confidence_scores.append(metrics.confidence)
        now = time.time()
        self._last_hour_queries.append((now, metrics.query_id))
        self._purge_old_queries(now)
        self._audit_writer.write(metrics)
        logger.debug(f"Recorded query: {metrics.query_id}")

    def record_error(self, error_type: str, message: str, query_id: typing.Optional[str]):
        error_entry = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "timestamp": time.time()
        }
        self._errors.append(error_entry)
        logger.error(f"Error recorded: {error_type} - {message} (query_id={query_id})")
        if query_id and query_id in self._query_index:
            self._query_index[query_id].error = error_type

    def get_latency_stats(self) -> dict:
        if not self._latencies:
            return dict(avg=None, p50=None, p95=None, p99=None, min=None, max=None)
        lat = sorted(self._latencies)
        avg = statistics.mean(lat)
        p50 = statistics.median(lat)
        p95 = lat[int(0.95 * len(lat))-1]
        p99 = lat[int(0.99 * len(lat))-1]
        minv = lat[0]
        maxv = lat[-1]
        return {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": minv,
            "max": maxv
        }

    def get_doctrine_hit_rate(self) -> float:
        if self._total_queries == 0:
            return 0.0
        return self._doctrine_hits / self._total_queries

    def get_error_rate(self, window_hours: float) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        queries_in_window = [q for (ts, qid) in self._last_hour_queries if ts >= window_start]
        if not queries_in_window:
            return 0.0
        return len(errors_in_window) / len(queries_in_window)

    def queries_last_hour(self) -> int:
        now = time.time()
        self._purge_old_queries(now)
        return len(self._last_hour_queries)

    def get_coverage_report(self) -> dict:
        total = sum(self._coverage_modes.values())
        if total == 0:
            return {}
        report = {}
        for mode, count in self._coverage_modes.items():
            report[mode] = count / total
        avg_conf = statistics.mean(self._confidence_scores) if self._confidence_scores else None
        report["avg_confidence"] = avg_conf
        return report

    def export_jsonl(self, path: typing.Union[str, pathlib.Path]) -> int:
        path = pathlib.Path(path)
        count = 0
        with path.open("w", encoding="utf-8") as f:
            for q in self._queries:
                f.write(json.dumps(dataclasses.asdict(q)) + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {path}")
        return count

    def _purge_old_queries(self, now: float):
        hour_ago = now - 3600
        while self._last_hour_queries and self._last_hour_queries[0][0] < hour_ago:
            self._last_hour_queries.popleft()

class AuditTrailWriter:
    def __init__(self, base_dir: typing.Union[str, pathlib.Path] = "audit_trail"):
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
        fname = self._get_audit_file(metrics.query_id)
        with fname.open("a", encoding="utf-8") as f:
            f.write(json.dumps(audit_entry) + "\n")
        logger.debug(f"Audit written for query {metrics.query_id} to {fname}")

    def _get_audit_file(self, query_id: str) -> pathlib.Path:
        # Partition audit files by first 2 chars of hash for scalability
        h = hashlib.sha256(query_id.encode()).hexdigest()
        subdir = self.base_dir / h[:2]
        subdir.mkdir(parents=True, exist_ok=True)
        return subdir / f"{query_id}.jsonl"

ENGINE_ID = "REG03"

COLLECTOR = TelemetryCollector()