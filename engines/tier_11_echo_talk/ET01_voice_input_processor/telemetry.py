import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional, Any
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "ET01"

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
        self._doctrine_hits = deque(maxlen=maxlen)
        self._cache_hits = deque(maxlen=maxlen)
        self._latencies = deque(maxlen=maxlen)
        self._modes = deque(maxlen=maxlen)
        self._confidences = deque(maxlen=maxlen)
        self._query_ids = set()
        self._query_metrics_map = {}
        self._audit_writer = AuditTrailWriter()
        logger.info("TelemetryCollector initialized with maxlen={}", maxlen)

    def record_query(self, metrics: QueryMetrics):
        if metrics.query_id in self._query_ids:
            logger.warning("Duplicate query_id detected: {}", metrics.query_id)
            return
        self._queries.append(metrics)
        self._query_ids.add(metrics.query_id)
        self._query_metrics_map[metrics.query_id] = metrics
        self._latencies.append(metrics.latency_ms)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._cache_hits.append(metrics.cache_hit)
        self._modes.append(metrics.mode)
        self._confidences.append(metrics.confidence)
        if metrics.error:
            self._errors.append((metrics.timestamp, metrics.error, metrics.query_id))
        self._audit_writer.write(metrics)
        logger.debug("Recorded query: {}", metrics)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        timestamp = time.time()
        self._errors.append((timestamp, error_type, query_id))
        logger.error("Error recorded: type={}, message={}, query_id={}", error_type, message, query_id)

    def get_latency_stats(self) -> Dict[str, Any]:
        if not self._latencies:
            return dict(avg=None, p50=None, p95=None, p99=None, min=None, max=None)
        latencies = list(self._latencies)
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = statistics.quantiles(latencies, n=100)[94] if len(latencies) >= 20 else max(latencies)
        p99 = statistics.quantiles(latencies, n=100)[98] if len(latencies) >= 100 else max(latencies)
        min_latency = min(latencies)
        max_latency = max(latencies)
        logger.debug("Latency stats computed")
        return {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_latency,
            "max": max_latency
        }

    def get_doctrine_hit_rate(self) -> float:
        if not self._doctrine_hits:
            return 0.0
        hits = sum(1 for hit in self._doctrine_hits if hit)
        rate = hits / len(self._doctrine_hits)
        logger.debug("Doctrine hit rate: {}", rate)
        return rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        error_count = sum(1 for ts, _, _ in self._errors if ts >= window_start)
        query_count = sum(1 for q in self._queries if q.timestamp >= window_start)
        rate = (error_count / query_count) if query_count > 0 else 0.0
        logger.debug("Error rate for last {} hours: {}", window_hours, rate)
        return rate

    def queries_last_hour(self) -> int:
        now = time.time()
        hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= hour_ago)
        logger.debug("Queries in last hour: {}", count)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        mode_counter = Counter(self._modes)
        doctrine_hits = sum(1 for hit in self._doctrine_hits if hit)
        cache_hits = sum(1 for hit in self._cache_hits if hit)
        total = len(self._queries)
        avg_conf = statistics.mean(self._confidences) if self._confidences else None
        report = {
            "total_queries": total,
            "by_mode": dict(mode_counter),
            "doctrine_hit_rate": self.get_doctrine_hit_rate(),
            "cache_hit_rate": (cache_hits / total) if total else 0.0,
            "avg_confidence": avg_conf
        }
        logger.debug("Coverage report generated: {}", report)
        return report

    def export_jsonl(self, path: str) -> int:
        output_path = pathlib.Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        count = 0
        with output_path.open("w", encoding="utf-8") as f:
            for q in self._queries:
                f.write(json.dumps(asdict(q)) + "\n")
                count += 1
        logger.info("Exported {} queries to {}", count, path)
        return count

class AuditTrailWriter:
    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = pathlib.Path(base_dir) if base_dir else pathlib.Path("./audit_trail")
        self.base_dir.mkdir(parents=True, exist_ok=True)
        logger.info("AuditTrailWriter initialized at {}", self.base_dir)

    def write(self, metrics: QueryMetrics):
        date_str = time.strftime("%Y-%m-%d", time.localtime(metrics.timestamp))
        file_path = self.base_dir / f"{date_str}.jsonl"
        record = asdict(metrics)
        try:
            with file_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(record) + "\n")
            logger.debug("Audit trail written for query_id={}", metrics.query_id)
        except Exception as e:
            logger.error("Failed to write audit trail: {}", e)

COLLECTOR = TelemetryCollector()