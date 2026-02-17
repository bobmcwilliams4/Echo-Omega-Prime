import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any, Deque
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "AUTO13"

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

    def to_dict(self) -> dict:
        return asdict(self)

class TelemetryCollector:
    def __init__(self, maxlen: int = 10000):
        self.queries: Deque[QueryMetrics] = deque(maxlen=maxlen)
        self.errors: Deque[dict] = deque(maxlen=maxlen)
        self.audit_writer = AuditTrailWriter()
        self._doctrine_counter = Counter()
        self._cache_counter = Counter()
        self._mode_counter = Counter()
        self._confidence_values = []
        self._latency_values = []
        self._query_times = deque(maxlen=maxlen)
        self._error_times = deque(maxlen=maxlen)
        self._query_id_map = {}
        logger.info("TelemetryCollector initialized with maxlen={}", maxlen)

    def record_query(self, metrics: QueryMetrics):
        self.queries.append(metrics)
        self._query_id_map[metrics.query_id] = metrics
        self._latency_values.append(metrics.latency_ms)
        self._doctrine_counter[metrics.doctrine_matched] += 1
        self._cache_counter[metrics.cache_hit] += 1
        self._mode_counter[metrics.mode] += 1
        self._confidence_values.append(metrics.confidence)
        self._query_times.append(metrics.timestamp)
        if metrics.error:
            self.record_error(metrics.error, "Query error", metrics.query_id)
        self.audit_writer.write(metrics)
        logger.debug("Recorded query: {}", metrics)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_record = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "timestamp": time.time(),
            "engine_id": ENGINE_ID
        }
        self.errors.append(error_record)
        self._error_times.append(error_record["timestamp"])
        logger.warning("Error recorded: {}", error_record)

    def get_latency_stats(self) -> dict:
        if not self._latency_values:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        values = sorted(self._latency_values)
        avg = statistics.mean(values)
        min_v = values[0]
        max_v = values[-1]
        p50 = statistics.median(values)
        p95 = values[int(0.95 * len(values)) - 1]
        p99 = values[int(0.99 * len(values)) - 1]
        stats = {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_v,
            "max": max_v
        }
        logger.debug("Latency stats calculated: {}", stats)
        return stats

    def get_doctrine_hit_rate(self) -> float:
        total = self._doctrine_counter[True] + self._doctrine_counter[False]
        if total == 0:
            return 0.0
        hit_rate = self._doctrine_counter[True] / total
        logger.debug("Doctrine hit rate: {}", hit_rate)
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [t for t in self._error_times if t >= window_start]
        queries_in_window = [t for t in self._query_times if t >= window_start]
        if not queries_in_window:
            return 0.0
        error_rate = len(errors_in_window) / len(queries_in_window)
        logger.debug("Error rate in last {} hours: {}", window_hours, error_rate)
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        window_start = now - 3600
        count = sum(1 for t in self._query_times if t >= window_start)
        logger.debug("Queries in last hour: {}", count)
        return count

    def get_coverage_report(self) -> dict:
        total = len(self.queries)
        if total == 0:
            return {
                "total_queries": 0,
                "cache_hit_rate": None,
                "doctrine_hit_rate": None,
                "mode_distribution": {},
                "confidence_avg": None,
                "confidence_min": None,
                "confidence_max": None
            }
        cache_hit_rate = self._cache_counter[True] / total
        doctrine_hit_rate = self._doctrine_counter[True] / total
        mode_distribution = dict(self._mode_counter)
        confidence_avg = statistics.mean(self._confidence_values)
        confidence_min = min(self._confidence_values)
        confidence_max = max(self._confidence_values)
        report = {
            "total_queries": total,
            "cache_hit_rate": cache_hit_rate,
            "doctrine_hit_rate": doctrine_hit_rate,
            "mode_distribution": mode_distribution,
            "confidence_avg": confidence_avg,
            "confidence_min": confidence_min,
            "confidence_max": confidence_max
        }
        logger.debug("Coverage report: {}", report)
        return report

    def export_jsonl(self, path: str) -> int:
        path_obj = pathlib.Path(path)
        count = 0
        with path_obj.open("w", encoding="utf-8") as f:
            for q in self.queries:
                f.write(json.dumps(q.to_dict()) + "\n")
                count += 1
        logger.info("Exported {} queries to {}", count, path)
        return count

class AuditTrailWriter:
    def __init__(self, base_path: Optional[str] = None):
        if base_path is None:
            base_path = "./audit_trail"
        self.base_path = pathlib.Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        logger.info("AuditTrailWriter initialized at {}", self.base_path)

    def write(self, metrics: QueryMetrics):
        date_str = time.strftime("%Y-%m-%d")
        file_path = self.base_path / f"audit_{date_str}.jsonl"
        record = metrics.to_dict()
        record["audit_hash"] = self._hash_record(record)
        with file_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
        logger.debug("Audit trail written for query_id={}", metrics.query_id)

    def _hash_record(self, record: dict) -> str:
        record_bytes = json.dumps(record, sort_keys=True).encode("utf-8")
        return hashlib.sha256(record_bytes).hexdigest()

COLLECTOR = TelemetryCollector()