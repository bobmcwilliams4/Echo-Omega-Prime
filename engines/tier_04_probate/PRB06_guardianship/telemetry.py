import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict, field
from typing import Optional, List, Dict, Any, Union
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "PRB06"

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
    def __init__(self, maxlen: int = 10000):
        self._queries = deque(maxlen=maxlen)
        self._errors = deque(maxlen=maxlen)
        self._latencies = deque(maxlen=maxlen)
        self._doctrine_matches = deque(maxlen=maxlen)
        self._cache_hits = deque(maxlen=maxlen)
        self._modes = deque(maxlen=maxlen)
        self._confidences = deque(maxlen=maxlen)
        self._query_id_set = set()
        self._audit_writer = AuditTrailWriter()
        self._query_time_index = deque(maxlen=maxlen)
        self._coverage_counter = Counter()
        self._error_types = Counter()
        self._query_metrics_map = {}
        logger.debug("TelemetryCollector initialized with maxlen={}", maxlen)

    def record_query(self, metrics: QueryMetrics):
        if metrics.query_id in self._query_id_set:
            logger.warning("Duplicate query_id detected: {}", metrics.query_id)
            return
        self._queries.append(metrics)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_matches.append(metrics.doctrine_matched)
        self._cache_hits.append(metrics.cache_hit)
        self._modes.append(metrics.mode)
        self._confidences.append(metrics.confidence)
        self._query_id_set.add(metrics.query_id)
        self._query_time_index.append((metrics.timestamp, metrics.query_id))
        self._coverage_counter[metrics.mode] += 1
        self._query_metrics_map[metrics.query_id] = metrics
        if metrics.error:
            self.record_error(metrics.error, "Error in query", metrics.query_id)
        self._audit_writer.write(metrics)
        logger.info("Recorded query: {}", metrics.query_id)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        ts = time.time()
        error_entry = {
            "timestamp": ts,
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "engine_id": ENGINE_ID
        }
        self._errors.append(error_entry)
        self._error_types[error_type] += 1
        logger.error("Error recorded: {} - {}", error_type, message)

    def get_latency_stats(self) -> dict:
        if not self._latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        latencies = list(self._latencies)
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)
        min_v = min(latencies)
        max_v = max(latencies)
        logger.debug("Latency stats calculated")
        return {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_v,
            "max": max_v
        }

    def get_doctrine_hit_rate(self) -> float:
        if not self._doctrine_matches:
            return 0.0
        hit_rate = sum(self._doctrine_matches) / len(self._doctrine_matches)
        logger.debug("Doctrine hit rate: {}", hit_rate)
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        n_errors = sum(1 for e in self._errors if e["timestamp"] >= window_start)
        n_queries = sum(1 for t, _ in self._query_time_index if t >= window_start)
        error_rate = (n_errors / n_queries) if n_queries > 0 else 0.0
        logger.debug("Error rate over {} hours: {}", window_hours, error_rate)
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for t, _ in self._query_time_index if t >= one_hour_ago)
        logger.debug("Queries in last hour: {}", count)
        return count

    def get_coverage_report(self) -> dict:
        total = sum(self._coverage_counter.values())
        report = {}
        for mode, count in self._coverage_counter.items():
            report[mode] = {
                "count": count,
                "fraction": count / total if total > 0 else 0.0
            }
        logger.debug("Coverage report generated")
        return report

    def export_jsonl(self, path: Union[str, pathlib.Path]) -> int:
        path = pathlib.Path(path)
        count = 0
        with path.open("w", encoding="utf-8") as f:
            for metrics in self._queries:
                f.write(json.dumps(asdict(metrics)) + "\n")
                count += 1
        logger.info("Exported {} queries to {}", count, str(path))
        return count

    @staticmethod
    def _percentile(data: List[float], percentile: float) -> float:
        if not data:
            return None
        size = len(data)
        data_sorted = sorted(data)
        k = (size - 1) * (percentile / 100)
        f = int(k)
        c = f + 1
        if c >= size:
            return data_sorted[-1]
        d0 = data_sorted[f] * (c - k)
        d1 = data_sorted[c] * (k - f)
        return d0 + d1

class AuditTrailWriter:
    def __init__(self, base_dir: Union[str, pathlib.Path] = "./audit_trail"):
        self.base_dir = pathlib.Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        logger.debug("AuditTrailWriter initialized at {}", str(self.base_dir))

    def write(self, metrics: QueryMetrics):
        date_str = time.strftime("%Y-%m-%d")
        filename = f"{ENGINE_ID}_audit_{date_str}.jsonl"
        path = self.base_dir / filename
        entry = asdict(metrics)
        entry["audit_hash"] = self._hash_entry(entry)
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        logger.debug("Audit entry written for query_id {}", metrics.query_id)

    @staticmethod
    def _hash_entry(entry: dict) -> str:
        m = hashlib.sha256()
        s = json.dumps(entry, sort_keys=True, default=str)
        m.update(s.encode("utf-8"))
        return m.hexdigest()

COLLECTOR = TelemetryCollector()