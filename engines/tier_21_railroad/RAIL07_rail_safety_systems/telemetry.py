import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict, field
from typing import Optional, List, Dict, Any, Deque
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "RAIL07"

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
        self._queries: Deque[QueryMetrics] = deque(maxlen=maxlen)
        self._errors: Deque[Dict[str, Any]] = deque(maxlen=maxlen)
        self._doctrine_hits: int = 0
        self._doctrine_total: int = 0
        self._latencies: Deque[float] = deque(maxlen=maxlen)
        self._mode_counter: Counter = Counter()
        self._cache_hits: int = 0
        self._cache_total: int = 0
        self._coverage_by_mode: Dict[str, int] = defaultdict(int)
        self._coverage_total: int = 0
        self._audit_writer = AuditTrailWriter()
        logger.info("TelemetryCollector initialized with maxlen={}", maxlen)

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_total += 1
        if metrics.doctrine_matched:
            self._doctrine_hits += 1
        self._mode_counter[metrics.mode] += 1
        self._coverage_by_mode[metrics.mode] += 1
        self._coverage_total += 1
        self._cache_total += 1
        if metrics.cache_hit:
            self._cache_hits += 1
        if metrics.error:
            self.record_error(metrics.error, "Query error", metrics.query_id)
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
        logger.error("Error recorded: {}", error_entry)

    def get_latency_stats(self) -> Dict[str, float]:
        if not self._latencies:
            return {"avg": 0, "p50": 0, "p95": 0, "p99": 0, "min": 0, "max": 0}
        latencies = sorted(self._latencies)
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = latencies[int(0.95 * len(latencies)) - 1]
        p99 = latencies[int(0.99 * len(latencies)) - 1]
        min_latency = latencies[0]
        max_latency = latencies[-1]
        stats = {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_latency,
            "max": max_latency
        }
        logger.debug("Latency stats: {}", stats)
        return stats

    def get_doctrine_hit_rate(self) -> float:
        if self._doctrine_total == 0:
            return 0.0
        rate = self._doctrine_hits / self._doctrine_total
        logger.debug("Doctrine hit rate: {}", rate)
        return rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        queries_in_window = [q for q in self._queries if q.timestamp >= window_start]
        error_count = len(errors_in_window)
        query_count = len(queries_in_window)
        if query_count == 0:
            return 0.0
        rate = error_count / query_count
        logger.debug("Error rate ({}h): {}", window_hours, rate)
        return rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= one_hour_ago)
        logger.debug("Queries last hour: {}", count)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {
            "total_queries": self._coverage_total,
            "by_mode": dict(self._coverage_by_mode),
            "cache_hit_rate": (self._cache_hits / self._cache_total) if self._cache_total else 0.0,
            "doctrine_hit_rate": self.get_doctrine_hit_rate(),
            "error_rate_1h": self.get_error_rate(1.0)
        }
        logger.debug("Coverage report: {}", report)
        return report

    def export_jsonl(self, path: str) -> int:
        p = pathlib.Path(path)
        count = 0
        with p.open("w", encoding="utf-8") as f:
            for q in self._queries:
                f.write(json.dumps(asdict(q)) + "\n")
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
        file_path = self.base_path / f"audit_{ENGINE_ID}_{date_str}.jsonl"
        entry = asdict(metrics)
        entry["audit_timestamp"] = time.time()
        with file_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        logger.debug("Audit written for query_id={}", metrics.query_id)

COLLECTOR = TelemetryCollector()