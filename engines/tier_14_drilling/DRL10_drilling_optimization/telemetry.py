import time
import json
import hashlib
import statistics
import pathlib
import dataclasses
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any
from collections import deque, defaultdict
from loguru import logger

ENGINE_ID = "DRL10"

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
        self._queries: deque[QueryMetrics] = deque(maxlen=maxlen)
        self._errors: deque[dict] = deque(maxlen=maxlen)
        self._doctrine_hits: deque[bool] = deque(maxlen=maxlen)
        self._cache_hits: deque[bool] = deque(maxlen=maxlen)
        self._latencies: deque[float] = deque(maxlen=maxlen)
        self._coverage_modes: defaultdict[str, int] = defaultdict(int)
        self._query_timestamps: deque[float] = deque(maxlen=maxlen)
        self._query_ids: set[str] = set()
        self._audit_writer = AuditTrailWriter()
        logger.debug("TelemetryCollector initialized with maxlen={}", maxlen)

    def record_query(self, metrics: QueryMetrics):
        if metrics.query_id in self._query_ids:
            logger.warning("Duplicate query_id detected: {}", metrics.query_id)
            return
        self._queries.append(metrics)
        self._query_ids.add(metrics.query_id)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._cache_hits.append(metrics.cache_hit)
        self._latencies.append(metrics.latency_ms)
        self._coverage_modes[metrics.mode] += 1
        self._query_timestamps.append(metrics.timestamp)
        self._audit_writer.write(metrics)
        logger.info("Recorded query: {}", metrics.query_id)
        if metrics.error:
            self.record_error("query_error", metrics.error, metrics.query_id)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "engine_id": ENGINE_ID,
            "error_type": error_type,
            "message": message,
            "query_id": query_id
        }
        self._errors.append(error_entry)
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
        stats = {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_v,
            "max": max_v
        }
        logger.debug("Latency stats: {}", stats)
        return stats

    def _percentile(self, data: List[float], percentile: float) -> float:
        if not data:
            return None
        data_sorted = sorted(data)
        k = (len(data_sorted) - 1) * (percentile / 100)
        f = int(k)
        c = min(f + 1, len(data_sorted) - 1)
        if f == c:
            return data_sorted[int(k)]
        d0 = data_sorted[f] * (c - k)
        d1 = data_sorted[c] * (k - f)
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
        error_count = sum(1 for e in self._errors if e["timestamp"] >= window_start)
        query_count = sum(1 for t in self._query_timestamps if t >= window_start)
        rate = (error_count / query_count) if query_count > 0 else 0.0
        logger.debug("Error rate in last {} hours: {}", window_hours, rate)
        return rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for t in self._query_timestamps if t >= one_hour_ago)
        logger.debug("Queries in last hour: {}", count)
        return count

    def get_coverage_report(self) -> dict:
        total = sum(self._coverage_modes.values())
        report = {}
        for mode, count in self._coverage_modes.items():
            report[mode] = {
                "count": count,
                "percent": (count / total) * 100 if total > 0 else 0.0
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
    def __init__(self, base_dir: str = "audit_trail"):
        self.base_dir = pathlib.Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        logger.debug("AuditTrailWriter initialized at {}", self.base_dir)

    def write(self, metrics: QueryMetrics):
        date_str = time.strftime("%Y-%m-%d", time.localtime(metrics.timestamp))
        file_path = self.base_dir / f"{date_str}.jsonl"
        entry = asdict(metrics)
        entry["audit_id"] = self._make_audit_id(metrics)
        try:
            with file_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
            logger.debug("Wrote audit trail for query_id {} to {}", metrics.query_id, file_path)
        except Exception as e:
            logger.error("Failed to write audit trail: {}", str(e))

    def _make_audit_id(self, metrics: QueryMetrics) -> str:
        base = f"{metrics.query_id}:{metrics.engine_id}:{metrics.timestamp}"
        return hashlib.sha256(base.encode("utf-8")).hexdigest()

COLLECTOR = TelemetryCollector()