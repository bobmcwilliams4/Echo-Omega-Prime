import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "S01"

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
    def __init__(self, maxlen=10000):
        self.queries: deque[QueryMetrics] = deque(maxlen=maxlen)
        self.errors: deque[Dict[str, Any]] = deque(maxlen=maxlen)
        self.latencies: deque[float] = deque(maxlen=maxlen)
        self.doctrine_matches: deque[bool] = deque(maxlen=maxlen)
        self.cache_hits: deque[bool] = deque(maxlen=maxlen)
        self.confidences: deque[float] = deque(maxlen=maxlen)
        self.modes: deque[str] = deque(maxlen=maxlen)
        self.timestamps: deque[float] = deque(maxlen=maxlen)
        self.query_id_set: set = set()
        self.audit_writer = AuditTrailWriter()
        self._query_id_to_metrics: Dict[str, QueryMetrics] = {}
        self._coverage_counter: Counter = Counter()
        self._last_exported_index = 0

    def record_query(self, metrics: QueryMetrics):
        logger.debug(f"Recording query: {metrics}")
        self.queries.append(metrics)
        self.latencies.append(metrics.latency_ms)
        self.doctrine_matches.append(metrics.doctrine_matched)
        self.cache_hits.append(metrics.cache_hit)
        self.confidences.append(metrics.confidence)
        self.modes.append(metrics.mode)
        self.timestamps.append(metrics.timestamp)
        self.query_id_set.add(metrics.query_id)
        self._query_id_to_metrics[metrics.query_id] = metrics
        self._coverage_counter[metrics.mode] += 1
        self.audit_writer.write(metrics)
        if metrics.error:
            self.record_error(metrics.error, "Query error", metrics.query_id)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "engine_id": ENGINE_ID
        }
        logger.error(f"Recording error: {error_entry}")
        self.errors.append(error_entry)

    def get_latency_stats(self) -> dict:
        if not self.latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        latencies = list(self.latencies)
        latencies.sort()
        avg = statistics.mean(latencies)
        min_latency = latencies[0]
        max_latency = latencies[-1]
        p50 = statistics.median(latencies)
        p95 = latencies[int(0.95 * len(latencies)) - 1]
        p99 = latencies[int(0.99 * len(latencies)) - 1]
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
        if not self.doctrine_matches:
            return 0.0
        hit_rate = sum(self.doctrine_matches) / len(self.doctrine_matches)
        logger.debug(f"Doctrine hit rate: {hit_rate}")
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self.errors if e["timestamp"] >= window_start]
        queries_in_window = [q for q in self.queries if q.timestamp >= window_start]
        error_count = len(errors_in_window)
        query_count = len(queries_in_window)
        if query_count == 0:
            return 0.0
        error_rate = error_count / query_count
        logger.debug(f"Error rate in last {window_hours}h: {error_rate} ({error_count}/{query_count})")
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self.queries if q.timestamp >= one_hour_ago)
        logger.debug(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> dict:
        total = sum(self._coverage_counter.values())
        report = {}
        for mode, count in self._coverage_counter.items():
            report[mode] = {
                "count": count,
                "percent": (count / total * 100) if total > 0 else 0.0
            }
        logger.debug(f"Coverage report: {report}")
        return report

    def export_jsonl(self, path: str) -> int:
        path_obj = pathlib.Path(path)
        path_obj.parent.mkdir(parents=True, exist_ok=True)
        count = 0
        with path_obj.open("a", encoding="utf-8") as f:
            for i, metrics in enumerate(list(self.queries)[self._last_exported_index:]):
                f.write(json.dumps(asdict(metrics)) + "\n")
                count += 1
            self._last_exported_index += count
        logger.info(f"Exported {count} queries to {path}")
        return count

class AuditTrailWriter:
    def __init__(self, base_path: Optional[str] = None):
        if base_path is None:
            base_path = "./audit_trail"
        self.base_path = pathlib.Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        self._open_files: Dict[str, Any] = {}

    def _get_audit_path(self, query_id: str) -> pathlib.Path:
        h = hashlib.sha1(query_id.encode("utf-8")).hexdigest()
        subdir = self.base_path / h[:2]
        subdir.mkdir(parents=True, exist_ok=True)
        return subdir / f"{query_id}.jsonl"

    def write(self, metrics: QueryMetrics):
        path = self._get_audit_path(metrics.query_id)
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(metrics)) + "\n")
        logger.debug(f"Wrote audit trail for query {metrics.query_id} to {path}")

COLLECTOR = TelemetryCollector()