import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any, Deque
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "MECH04"

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
        self._queries: Deque[QueryMetrics] = deque(maxlen=maxlen)
        self._errors: Deque[Dict[str, Any]] = deque(maxlen=maxlen)
        self._query_by_id: Dict[str, QueryMetrics] = {}
        self._doctrine_hits: int = 0
        self._doctrine_total: int = 0
        self._error_counter: Counter = Counter()
        self._mode_counter: Counter = Counter()
        self._cache_hits: int = 0
        self._cache_total: int = 0
        self._latencies: List[float] = []
        self._coverage_by_mode: defaultdict = defaultdict(set)
        self._audit_writer = AuditTrailWriter()
        logger.info("TelemetryCollector initialized for engine {}", ENGINE_ID)

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._query_by_id[metrics.query_id] = metrics
        self._latencies.append(metrics.latency_ms)
        self._mode_counter[metrics.mode] += 1
        self._cache_total += 1
        if metrics.cache_hit:
            self._cache_hits += 1
        self._doctrine_total += 1
        if metrics.doctrine_matched:
            self._doctrine_hits += 1
        if metrics.error:
            self._error_counter[metrics.error] += 1
        self._coverage_by_mode[metrics.mode].add(metrics.query_id)
        self._audit_writer.write(metrics)
        logger.debug("Recorded query: {}", metrics)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "engine_id": ENGINE_ID,
            "error_type": error_type,
            "message": message,
            "query_id": query_id
        }
        self._errors.append(error_entry)
        self._error_counter[error_type] += 1
        logger.error("Error recorded: {}", error_entry)

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
        lat_sorted = sorted(self._latencies)
        avg = statistics.mean(self._latencies)
        p50 = statistics.median(lat_sorted)
        p95 = lat_sorted[int(0.95 * len(lat_sorted)) - 1]
        p99 = lat_sorted[int(0.99 * len(lat_sorted)) - 1]
        min_v = lat_sorted[0]
        max_v = lat_sorted[-1]
        stats_dict = {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_v,
            "max": max_v
        }
        logger.info("Latency stats: {}", stats_dict)
        return stats_dict

    def get_doctrine_hit_rate(self) -> float:
        if self._doctrine_total == 0:
            return 0.0
        hit_rate = self._doctrine_hits / self._doctrine_total
        logger.info("Doctrine hit rate: {:.2%}", hit_rate)
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        error_count = 0
        total_count = 0
        for q in self._queries:
            if q.timestamp >= window_start:
                total_count += 1
                if q.error:
                    error_count += 1
        if total_count == 0:
            return 0.0
        error_rate = error_count / total_count
        logger.info("Error rate in last {} hours: {:.2%}", window_hours, error_rate)
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= one_hour_ago)
        logger.info("Queries in last hour: {}", count)
        return count

    def get_coverage_report(self) -> dict:
        report = {}
        for mode, queries in self._coverage_by_mode.items():
            report[mode] = len(queries)
        logger.info("Coverage report: {}", report)
        return report

    def export_jsonl(self, path: str) -> int:
        p = pathlib.Path(path)
        count = 0
        with p.open("w", encoding="utf-8") as f:
            for q in self._queries:
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
        filename = self._get_filename(metrics)
        record = metrics.to_dict()
        record["audit_written_at"] = time.time()
        with open(filename, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
        logger.debug("Audit written for query_id {} to {}", metrics.query_id, filename)

    def _get_filename(self, metrics: QueryMetrics) -> str:
        date_str = time.strftime("%Y%m%d", time.localtime(metrics.timestamp))
        filename = f"{ENGINE_ID}_audit_{date_str}.jsonl"
        return str(self.base_path / filename)

COLLECTOR = TelemetryCollector()