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
        self._cache_hits = 0
        self._cache_total = 0
        self._latencies = []
        self._query_times = collections.deque()
        self._coverage_modes = collections.Counter()
        self._coverage_doctrines = collections.Counter()
        self._coverage_confidences = []
        self._query_id_set = set()
        self._audit_writer = AuditTrailWriter()
        self._lock = None  # Placeholder for threading.Lock if needed

    def record_query(self, metrics: QueryMetrics):
        if metrics.query_id in self._query_id_set:
            logger.warning(f"Duplicate query_id detected: {metrics.query_id}")
            return
        self._query_id_set.add(metrics.query_id)
        self._queries.append(metrics)
        self._query_times.append(metrics.timestamp)
        self._latencies.append(metrics.latency_ms)
        if metrics.cache_hit:
            self._cache_hits += 1
        self._cache_total += 1
        if metrics.doctrine_matched:
            self._doctrine_hits += 1
        self._doctrine_total += 1
        self._coverage_modes[metrics.mode] += 1
        self._coverage_confidences.append(metrics.confidence)
        self._coverage_doctrines[metrics.doctrine_matched] += 1
        if metrics.error:
            self._errors.append({
                "error_type": metrics.error,
                "message": "",
                "query_id": metrics.query_id,
                "timestamp": metrics.timestamp
            })
        self._audit_writer.write(metrics)

    def record_error(self, error_type: str, message: str, query_id: str):
        ts = time.time()
        self._errors.append({
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "timestamp": ts
        })
        logger.error(f"Error recorded: {error_type} | {message} | Query: {query_id}")

    def get_latency_stats(self) -> dict:
        if not self._latencies:
            return {
                "avg": None, "p50": None, "p95": None, "p99": None,
                "min": None, "max": None
            }
        lat = sorted(self._latencies)
        avg = statistics.mean(lat)
        min_v = lat[0]
        max_v = lat[-1]
        p50 = lat[int(0.5 * len(lat))]
        p95 = lat[int(0.95 * len(lat)) - 1]
        p99 = lat[int(0.99 * len(lat)) - 1]
        return {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_v,
            "max": max_v
        }

    def get_doctrine_hit_rate(self) -> float:
        if self._doctrine_total == 0:
            return 0.0
        return self._doctrine_hits / self._doctrine_total

    def get_error_rate(self, window_hours: float) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        total = 0
        errors = 0
        for m in self._queries:
            if m.timestamp >= window_start:
                total += 1
                if m.error:
                    errors += 1
        if total == 0:
            return 0.0
        return errors / total

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = 0
        for ts in reversed(self._query_times):
            if ts >= one_hour_ago:
                count += 1
            else:
                break
        return count

    def get_coverage_report(self) -> dict:
        total = len(self._queries)
        if total == 0:
            return {
                "total": 0,
                "modes": {},
                "avg_confidence": None,
                "doctrine_matched": 0,
                "doctrine_unmatched": 0,
                "cache_hit": 0,
                "cache_miss": 0
            }
        avg_conf = statistics.mean(self._coverage_confidences) if self._coverage_confidences else None
        doctrine_matched = self._coverage_doctrines.get(True, 0)
        doctrine_unmatched = self._coverage_doctrines.get(False, 0)
        cache_hit = self._cache_hits
        cache_miss = self._cache_total - self._cache_hits
        return {
            "total": total,
            "modes": dict(self._coverage_modes),
            "avg_confidence": avg_conf,
            "doctrine_matched": doctrine_matched,
            "doctrine_unmatched": doctrine_unmatched,
            "cache_hit": cache_hit,
            "cache_miss": cache_miss
        }

    def export_jsonl(self, path) -> int:
        path = pathlib.Path(path)
        count = 0
        with path.open("w", encoding="utf-8") as f:
            for m in self._queries:
                d = dataclasses.asdict(m)
                f.write(json.dumps(d) + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {path}")
        return count

class AuditTrailWriter:
    def __init__(self, base_dir: typing.Optional[pathlib.Path] = None):
        if base_dir is None:
            base_dir = pathlib.Path("./audit_trail")
        self.base_dir = base_dir
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def write(self, metrics: QueryMetrics):
        day = time.strftime("%Y-%m-%d", time.localtime(metrics.timestamp))
        file_path = self.base_dir / f"audit_{day}.jsonl"
        data = dataclasses.asdict(metrics)
        try:
            with file_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(data) + "\n")
        except Exception as e:
            logger.error(f"Failed to write audit trail for {metrics.query_id}: {e}")

ENGINE_ID = "MATH02"
COLLECTOR = TelemetryCollector()