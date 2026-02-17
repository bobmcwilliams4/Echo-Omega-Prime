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
        self._doctrine_hits = 0
        self._doctrine_total = 0
        self._latencies = []
        self._cache_hits = 0
        self._cache_total = 0
        self._query_id_set = set()
        self._mode_counter = collections.Counter()
        self._confidence_samples = []
        self._coverage_modes = collections.defaultdict(int)
        self._audit_writer = AuditTrailWriter()
        self._lock = None  # Placeholder for thread safety if needed

    def record_query(self, metrics: QueryMetrics):
        if metrics.query_id in self._query_id_set:
            logger.warning(f"Duplicate query_id: {metrics.query_id}")
            return
        self._queries.append(metrics)
        self._query_id_set.add(metrics.query_id)
        self._latencies.append(metrics.latency_ms)
        self._mode_counter[metrics.mode] += 1
        self._confidence_samples.append(metrics.confidence)
        self._coverage_modes[metrics.mode] += 1
        self._cache_total += 1
        if metrics.cache_hit:
            self._cache_hits += 1
        self._doctrine_total += 1
        if metrics.doctrine_matched:
            self._doctrine_hits += 1
        if metrics.error:
            self.record_error(metrics.error, "QueryError", metrics.query_id)
        self._audit_writer.write(metrics)

    def record_error(self, error_type: str, message: str, query_id: typing.Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "error_type": error_type,
            "message": message,
            "query_id": query_id
        }
        self._errors.append(error_entry)
        logger.error(f"Error recorded: {error_entry}")

    def get_latency_stats(self) -> dict:
        if not self._latencies:
            return {
                "avg": None, "p50": None, "p95": None, "p99": None,
                "min": None, "max": None
            }
        lat_sorted = sorted(self._latencies)
        avg = statistics.mean(lat_sorted)
        min_val = lat_sorted[0]
        max_val = lat_sorted[-1]
        p50 = self._percentile(lat_sorted, 50)
        p95 = self._percentile(lat_sorted, 95)
        p99 = self._percentile(lat_sorted, 99)
        return {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_val,
            "max": max_val
        }

    def _percentile(self, data, percentile):
        if not data:
            return None
        k = (len(data)-1) * (percentile/100)
        f = int(k)
        c = min(f+1, len(data)-1)
        if f == c:
            return data[int(k)]
        d0 = data[f] * (c-k)
        d1 = data[c] * (k-f)
        return d0 + d1

    def get_doctrine_hit_rate(self) -> float:
        if self._doctrine_total == 0:
            return 0.0
        return self._doctrine_hits / self._doctrine_total

    def get_error_rate(self, window_hours: float) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        queries_in_window = [q for q in self._queries if q.timestamp >= window_start]
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        total = len(queries_in_window)
        if total == 0:
            return 0.0
        return len(errors_in_window) / total

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        return sum(1 for q in self._queries if q.timestamp >= one_hour_ago)

    def get_coverage_report(self) -> dict:
        total = len(self._queries)
        if total == 0:
            return {
                "total": 0,
                "modes": {},
                "confidence": {
                    "avg": None,
                    "min": None,
                    "max": None,
                    "p50": None,
                    "p95": None
                }
            }
        mode_dist = dict(self._mode_counter)
        conf_sorted = sorted(self._confidence_samples)
        conf_avg = statistics.mean(conf_sorted)
        conf_min = conf_sorted[0]
        conf_max = conf_sorted[-1]
        conf_p50 = self._percentile(conf_sorted, 50)
        conf_p95 = self._percentile(conf_sorted, 95)
        return {
            "total": total,
            "modes": mode_dist,
            "confidence": {
                "avg": conf_avg,
                "min": conf_min,
                "max": conf_max,
                "p50": conf_p50,
                "p95": conf_p95
            }
        }

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
    def __init__(self, directory: typing.Union[str, pathlib.Path] = "./audit_trail"):
        self.directory = pathlib.Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)

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
        filename = self.directory / f"{metrics.query_id}.jsonl"
        try:
            with filename.open("a", encoding="utf-8") as f:
                f.write(json.dumps(audit_entry) + "\n")
        except Exception as e:
            logger.error(f"Failed to write audit trail for {metrics.query_id}: {e}")

ENGINE_ID = "DRL12"
COLLECTOR = TelemetryCollector()