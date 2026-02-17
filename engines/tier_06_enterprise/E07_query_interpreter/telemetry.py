import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional, Any
from collections import deque, defaultdict, Counter
from loguru import logger

ENGINE_ID = "E07"

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
        self._queries: deque = deque(maxlen=maxlen)
        self._errors: deque = deque(maxlen=maxlen)
        self._doctrine_hits: deque = deque(maxlen=maxlen)
        self._latencies: deque = deque(maxlen=maxlen)
        self._query_time_index: deque = deque(maxlen=maxlen)
        self._coverage_modes: Counter = Counter()
        self._audit_writer = AuditTrailWriter()
        logger.info("TelemetryCollector initialized with maxlen={}", maxlen)

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._query_time_index.append(metrics.timestamp)
        self._coverage_modes[metrics.mode] += 1
        if metrics.error:
            self._errors.append({
                "timestamp": metrics.timestamp,
                "error": metrics.error,
                "query_id": metrics.query_id
            })
        self._audit_writer.write(metrics)
        logger.debug("Recorded query: {}", metrics)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "error_type": error_type,
            "message": message,
            "query_id": query_id
        }
        self._errors.append(error_entry)
        logger.error("Error recorded: {}", error_entry)

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = list(self._latencies)
        if not latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        min_v = min(latencies)
        max_v = max(latencies)
        p50 = statistics.median(latencies)
        p95 = latencies_sorted[int(0.95 * len(latencies_sorted)) - 1]
        p99 = latencies_sorted[int(0.99 * len(latencies_sorted)) - 1]
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
        if not self._doctrine_hits:
            return 0.0
        hit_count = sum(1 for hit in self._doctrine_hits if hit)
        rate = hit_count / len(self._doctrine_hits)
        logger.debug("Doctrine hit rate: {:.2%}", rate)
        return rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        queries_in_window = [t for t in self._query_time_index if t >= window_start]
        errors_in_window = [e for e in self._errors if e.get("timestamp", 0) >= window_start]
        if not queries_in_window:
            return 0.0
        rate = len(errors_in_window) / len(queries_in_window)
        logger.debug("Error rate in last {:.2f}h: {:.2%}", window_hours, rate)
        return rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for t in self._query_time_index if t >= one_hour_ago)
        logger.debug("Queries in last hour: {}", count)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        total = sum(self._coverage_modes.values())
        report = {}
        for mode, count in self._coverage_modes.items():
            report[mode] = {
                "count": count,
                "rate": count / total if total else 0.0
            }
        logger.debug("Coverage report: {}", report)
        return report

    def export_jsonl(self, path: str) -> int:
        path_obj = pathlib.Path(path)
        count = 0
        with path_obj.open("w", encoding="utf-8") as f:
            for metrics in self._queries:
                f.write(json.dumps(asdict(metrics)) + "\n")
                count += 1
        logger.info("Exported {} queries to {}", count, path)
        return count

class AuditTrailWriter:
    def __init__(self, base_path: Optional[str] = None):
        self.base_path = pathlib.Path(base_path) if base_path else pathlib.Path("./audit_trail")
        self.base_path.mkdir(parents=True, exist_ok=True)
        logger.info("AuditTrailWriter initialized at {}", self.base_path)

    def write(self, metrics: QueryMetrics):
        date_str = time.strftime("%Y-%m-%d")
        file_path = self.base_path / f"audit_{date_str}.jsonl"
        entry = asdict(metrics)
        with file_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        logger.debug("Audit trail written for query_id={}", metrics.query_id)

COLLECTOR = TelemetryCollector()