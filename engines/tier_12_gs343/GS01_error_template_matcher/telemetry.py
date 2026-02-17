import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict, field
from typing import Optional, List, Dict, Any
from collections import deque, defaultdict
from loguru import logger

ENGINE_ID = "GS01"

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
        self._queries: deque = deque(maxlen=maxlen)
        self._errors: deque = deque(maxlen=maxlen)
        self._doctrine_hits: deque = deque(maxlen=maxlen)
        self._latencies: deque = deque(maxlen=maxlen)
        self._query_times: deque = deque(maxlen=maxlen)
        self._query_by_id: Dict[str, QueryMetrics] = {}
        self._audit_writer = AuditTrailWriter()
        logger.info("TelemetryCollector initialized with maxlen={}", maxlen)

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._query_by_id[metrics.query_id] = metrics
        self._latencies.append(metrics.latency_ms)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._query_times.append(metrics.timestamp)
        self._audit_writer.write(metrics)
        logger.debug("Recorded query: {}", metrics)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
        }
        self._errors.append(error_entry)
        logger.error("Error recorded: {}", error_entry)

    def get_latency_stats(self) -> dict:
        latencies = list(self._latencies)
        if not latencies:
            return {
                "avg": None,
                "p50": None,
                "p95": None,
                "p99": None,
                "min": None,
                "max": None,
            }
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)
        min_latency = min(latencies)
        max_latency = max(latencies)
        stats = {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_latency,
            "max": max_latency,
        }
        logger.debug("Latency stats: {}", stats)
        return stats

    def _percentile(self, data: List[float], percentile: float) -> float:
        if not data:
            return None
        k = (len(data) - 1) * (percentile / 100)
        f = int(k)
        c = min(f + 1, len(data) - 1)
        if f == c:
            return sorted(data)[int(k)]
        d0 = sorted(data)[f] * (c - k)
        d1 = sorted(data)[c] * (k - f)
        return d0 + d1

    def get_doctrine_hit_rate(self) -> float:
        if not self._doctrine_hits:
            return 0.0
        hit_rate = sum(self._doctrine_hits) / len(self._doctrine_hits)
        logger.debug("Doctrine hit rate: {}", hit_rate)
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        queries_in_window = [t for t in self._query_times if t >= window_start]
        error_count = len(errors_in_window)
        query_count = len(queries_in_window)
        if query_count == 0:
            logger.debug("No queries in window for error rate calculation.")
            return 0.0
        error_rate = error_count / query_count
        logger.debug("Error rate in last {} hours: {}", window_hours, error_rate)
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for t in self._query_times if t >= one_hour_ago)
        logger.debug("Queries in last hour: {}", count)
        return count

    def get_coverage_report(self) -> dict:
        total = len(self._queries)
        doctrine_matched = sum(1 for q in self._queries if q.doctrine_matched)
        cache_hits = sum(1 for q in self._queries if q.cache_hit)
        modes = defaultdict(int)
        confidences = []
        for q in self._queries:
            modes[q.mode] += 1
            confidences.append(q.confidence)
        avg_confidence = statistics.mean(confidences) if confidences else None
        report = {
            "total_queries": total,
            "doctrine_matched": doctrine_matched,
            "doctrine_coverage": doctrine_matched / total if total else 0.0,
            "cache_hits": cache_hits,
            "cache_hit_rate": cache_hits / total if total else 0.0,
            "modes": dict(modes),
            "avg_confidence": avg_confidence,
        }
        logger.debug("Coverage report: {}", report)
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
    def __init__(self, base_dir: Optional[str] = None):
        if base_dir is None:
            base_dir = "./audit_trail"
        self.base_dir = pathlib.Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        logger.info("AuditTrailWriter initialized at {}", self.base_dir)

    def write(self, metrics: QueryMetrics):
        date_str = time.strftime("%Y%m%d")
        file_path = self.base_dir / f"audit_{ENGINE_ID}_{date_str}.jsonl"
        record = metrics.to_dict()
        with file_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
        logger.debug("Wrote audit trail for query_id={} to {}", metrics.query_id, file_path)

COLLECTOR = TelemetryCollector()