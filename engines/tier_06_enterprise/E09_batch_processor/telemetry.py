import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional, Any
from collections import deque, defaultdict, Counter
from loguru import logger

ENGINE_ID = "E09"

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
        self._errors: deque[Dict[str, Any]] = deque(maxlen=maxlen)
        self._doctrine_hits: deque[bool] = deque(maxlen=maxlen)
        self._latencies: deque[float] = deque(maxlen=maxlen)
        self._cache_hits: deque[bool] = deque(maxlen=maxlen)
        self._query_times: deque[float] = deque(maxlen=maxlen)
        self._query_ids: set[str] = set()
        self._audit_writer = AuditTrailWriter()
        self._error_counter: Counter = Counter()
        logger.info("TelemetryCollector initialized with maxlen={}", maxlen)

    def record_query(self, metrics: QueryMetrics):
        logger.debug("Recording query: {}", metrics)
        self._queries.append(metrics)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._cache_hits.append(metrics.cache_hit)
        self._query_times.append(metrics.timestamp)
        self._query_ids.add(metrics.query_id)
        if metrics.error:
            self.record_error(metrics.error, "Error in QueryMetrics", metrics.query_id)
        self._audit_writer.write(metrics)
        logger.debug("Query recorded. Total queries stored: {}", len(self._queries))

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "engine_id": ENGINE_ID
        }
        logger.error("Recording error: {}", error_entry)
        self._errors.append(error_entry)
        self._error_counter[error_type] += 1

    def get_latency_stats(self) -> Dict[str, float]:
        latencies = list(self._latencies)
        if not latencies:
            logger.warning("No latencies recorded.")
            return {"avg": 0.0, "p50": 0.0, "p95": 0.0, "p99": 0.0, "min": 0.0, "max": 0.0}
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
            "max": max_latency
        }
        logger.info("Latency stats computed: {}", stats)
        return stats

    def get_doctrine_hit_rate(self) -> float:
        hits = list(self._doctrine_hits)
        if not hits:
            logger.warning("No doctrine hit data.")
            return 0.0
        hit_rate = sum(hits) / len(hits)
        logger.info("Doctrine hit rate: {:.2%}", hit_rate)
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        queries_in_window = [t for t in self._query_times if t >= window_start]
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        total = len(queries_in_window)
        error_count = len(errors_in_window)
        if total == 0:
            logger.warning("No queries in error rate window.")
            return 0.0
        error_rate = error_count / total
        logger.info("Error rate over last {:.2f} hours: {:.2%}", window_hours, error_rate)
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for t in self._query_times if t >= one_hour_ago)
        logger.info("Queries in last hour: {}", count)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        modes = Counter()
        confidences = []
        cache_hits = 0
        doctrine_hits = 0
        total = 0
        for q in self._queries:
            modes[q.mode] += 1
            confidences.append(q.confidence)
            if q.cache_hit:
                cache_hits += 1
            if q.doctrine_matched:
                doctrine_hits += 1
            total += 1
        avg_conf = statistics.mean(confidences) if confidences else 0.0
        coverage = {
            "total_queries": total,
            "modes": dict(modes),
            "avg_confidence": avg_conf,
            "cache_hit_rate": cache_hits / total if total else 0.0,
            "doctrine_hit_rate": doctrine_hits / total if total else 0.0
        }
        logger.info("Coverage report: {}", coverage)
        return coverage

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

    @staticmethod
    def _percentile(data: List[float], percentile: float) -> float:
        if not data:
            return 0.0
        data = sorted(data)
        k = (len(data)-1) * (percentile/100)
        f = int(k)
        c = min(f+1, len(data)-1)
        if f == c:
            return data[int(k)]
        d0 = data[f] * (c-k)
        d1 = data[c] * (k-f)
        return d0 + d1

class AuditTrailWriter:
    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = pathlib.Path(base_dir) if base_dir else pathlib.Path("./audit_trail")
        self.base_dir.mkdir(parents=True, exist_ok=True)
        logger.info("AuditTrailWriter initialized at {}", self.base_dir)

    def write(self, metrics: QueryMetrics):
        query_hash = self._hash_query_id(metrics.query_id)
        date_str = time.strftime("%Y-%m-%d", time.localtime(metrics.timestamp))
        dir_path = self.base_dir / date_str
        dir_path.mkdir(parents=True, exist_ok=True)
        file_path = dir_path / f"{query_hash}.jsonl"
        with file_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(metrics)) + "\n")
        logger.debug("Audit trail written for query_id={} at {}", metrics.query_id, file_path)

    @staticmethod
    def _hash_query_id(query_id: str) -> str:
        return hashlib.sha256(query_id.encode("utf-8")).hexdigest()[:16]

COLLECTOR = TelemetryCollector()