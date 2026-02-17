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
        self._lock = collections.deque(maxlen=100000)
        self._query_id_index = set()
        self._doctrine_hits = 0
        self._total_queries = 0
        self._latencies = []
        self._doctrine_matched = []
        self._cache_hits = []
        self._confidence_scores = []
        self._error_types = collections.Counter()
        self._query_timestamps = []
        self._query_modes = collections.Counter()
        self._coverage_modes = collections.defaultdict(int)
        self._audit_writer = AuditTrailWriter()
        logger.info("TelemetryCollector initialized.")

    def record_query(self, metrics: QueryMetrics):
        if metrics.query_id in self._query_id_index:
            logger.warning(f"Duplicate query_id detected: {metrics.query_id}")
            return
        self._queries.append(metrics)
        self._query_id_index.add(metrics.query_id)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_matched.append(metrics.doctrine_matched)
        self._cache_hits.append(metrics.cache_hit)
        self._confidence_scores.append(metrics.confidence)
        self._query_timestamps.append(metrics.timestamp)
        self._query_modes[metrics.mode] += 1
        self._coverage_modes[metrics.mode] += 1
        self._total_queries += 1
        if metrics.doctrine_matched:
            self._doctrine_hits += 1
        if metrics.error:
            self._errors.append({
                "timestamp": metrics.timestamp,
                "query_id": metrics.query_id,
                "error": metrics.error
            })
            self._error_types[metrics.error] += 1
        self._audit_writer.write(metrics)
        logger.debug(f"Recorded query: {metrics.query_id}")

    def record_error(self, error_type: str, message: str, query_id: typing.Optional[str] = None):
        err_entry = {
            "timestamp": time.time(),
            "error_type": error_type,
            "message": message,
            "query_id": query_id
        }
        self._errors.append(err_entry)
        self._error_types[error_type] += 1
        logger.error(f"Error recorded: {error_type} for query_id={query_id}: {message}")

    def get_latency_stats(self) -> dict:
        if not self._latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        lat = sorted(self._latencies)
        avg = statistics.mean(lat)
        p50 = statistics.median(lat)
        p95 = lat[int(0.95 * len(lat)) - 1]
        p99 = lat[int(0.99 * len(lat)) - 1]
        min_v = lat[0]
        max_v = lat[-1]
        stats = {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_v,
            "max": max_v
        }
        logger.debug(f"Latency stats: {stats}")
        return stats

    def get_doctrine_hit_rate(self) -> float:
        if self._total_queries == 0:
            return 0.0
        hit_rate = self._doctrine_hits / self._total_queries
        logger.debug(f"Doctrine hit rate: {hit_rate}")
        return hit_rate

    def get_error_rate(self, window_hours: float) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        relevant_queries = [ts for ts in self._query_timestamps if ts >= window_start]
        relevant_errors = [err for err in self._errors if err["timestamp"] >= window_start]
        num_queries = len(relevant_queries)
        num_errors = len(relevant_errors)
        if num_queries == 0:
            return 0.0
        error_rate = num_errors / num_queries
        logger.debug(f"Error rate over last {window_hours}h: {error_rate}")
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for ts in self._query_timestamps if ts >= one_hour_ago)
        logger.debug(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> dict:
        total = self._total_queries
        if total == 0:
            return {}
        mode_counts = dict(self._coverage_modes)
        coverage = {mode: count / total for mode, count in mode_counts.items()}
        avg_confidence = statistics.mean(self._confidence_scores) if self._confidence_scores else None
        report = {
            "total_queries": total,
            "coverage_by_mode": coverage,
            "avg_confidence": avg_confidence,
            "cache_hit_rate": sum(self._cache_hits) / total if total else 0.0,
            "doctrine_hit_rate": self.get_doctrine_hit_rate()
        }
        logger.debug(f"Coverage report: {report}")
        return report

    def export_jsonl(self, path: typing.Union[str, pathlib.Path]) -> int:
        path = pathlib.Path(path)
        count = 0
        with path.open("w", encoding="utf-8") as f:
            for qm in self._queries:
                f.write(json.dumps(dataclasses.asdict(qm)) + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {path}")
        return count

class AuditTrailWriter:
    def __init__(self, base_dir: typing.Optional[typing.Union[str, pathlib.Path]] = None):
        if base_dir is None:
            base_dir = pathlib.Path("audit_trails")
        else:
            base_dir = pathlib.Path(base_dir)
        self.base_dir = base_dir
        self.base_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"AuditTrailWriter initialized at {self.base_dir}")

    def write(self, metrics: QueryMetrics):
        date_str = time.strftime("%Y-%m-%d", time.localtime(metrics.timestamp))
        file_path = self.base_dir / f"audit_{date_str}.jsonl"
        entry = dataclasses.asdict(metrics)
        with file_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        logger.debug(f"Audit trail written for query_id={metrics.query_id}")

ENGINE_ID = "CHEM10"
COLLECTOR = TelemetryCollector()