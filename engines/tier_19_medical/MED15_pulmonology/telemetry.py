import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any, Union
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "MED15"

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
    def __init__(self, max_queries: int = 10000, max_errors: int = 1000):
        self._queries: deque = deque(maxlen=max_queries)
        self._errors: deque = deque(maxlen=max_errors)
        self._doctrine_hits: int = 0
        self._doctrine_total: int = 0
        self._latencies: deque = deque(maxlen=max_queries)
        self._coverage: Counter = Counter()
        self._cache_hits: int = 0
        self._cache_total: int = 0
        self._audit_writer = AuditTrailWriter()
        self._query_id_set: set = set()
        logger.info("TelemetryCollector initialized for engine {}", ENGINE_ID)

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_total += 1
        if metrics.doctrine_matched:
            self._doctrine_hits += 1
        self._cache_total += 1
        if metrics.cache_hit:
            self._cache_hits += 1
        self._coverage[metrics.mode] += 1
        self._audit_writer.write(metrics)
        self._query_id_set.add(metrics.query_id)
        logger.debug("Recorded query: {}", metrics)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_record = {
            "error_type": error_type,
            "message": message,
            "timestamp": time.time(),
            "query_id": query_id,
            "engine_id": ENGINE_ID
        }
        self._errors.append(error_record)
        logger.error("Recorded error: {}", error_record)

    def get_latency_stats(self) -> Dict[str, Union[float, None]]:
        latencies = list(self._latencies)
        if not latencies:
            return dict(avg=None, p50=None, p95=None, p99=None, min=None, max=None)
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        latencies_sorted = sorted(latencies)
        n = len(latencies_sorted)
        def percentile(p):
            idx = int(p * n)
            idx = min(idx, n - 1)
            return latencies_sorted[idx]
        p95 = percentile(0.95)
        p99 = percentile(0.99)
        min_latency = latencies_sorted[0]
        max_latency = latencies_sorted[-1]
        stats = {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_latency,
            "max": max_latency
        }
        logger.info("Latency stats: {}", stats)
        return stats

    def get_doctrine_hit_rate(self) -> float:
        if self._doctrine_total == 0:
            return 0.0
        hit_rate = self._doctrine_hits / self._doctrine_total
        logger.info("Doctrine hit rate: {:.2f}", hit_rate)
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        error_count = sum(1 for e in self._errors if e["timestamp"] >= window_start)
        query_count = sum(1 for q in self._queries if q.timestamp >= window_start)
        if query_count == 0:
            return 0.0
        error_rate = error_count / query_count
        logger.info("Error rate in last {:.2f} hours: {:.4f}", window_hours, error_rate)
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= hour_ago)
        logger.info("Queries in last hour: {}", count)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        total = sum(self._coverage.values())
        report = {}
        for mode, count in self._coverage.items():
            report[mode] = {
                "count": count,
                "percent": (count / total) * 100 if total > 0 else 0.0
            }
        logger.info("Coverage report: {}", report)
        return report

    def export_jsonl(self, path: Union[str, pathlib.Path]) -> int:
        path = pathlib.Path(path)
        count = 0
        with path.open("w", encoding="utf-8") as f:
            for q in self._queries:
                f.write(json.dumps(asdict(q)) + "\n")
                count += 1
        logger.info("Exported {} queries to {}", count, str(path))
        return count

class AuditTrailWriter:
    def __init__(self, base_dir: Union[str, pathlib.Path] = "./audit_trail"):
        self.base_dir = pathlib.Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        logger.info("AuditTrailWriter initialized at {}", str(self.base_dir))

    def _get_audit_path(self, query_id: str) -> pathlib.Path:
        hash_digest = hashlib.sha256(query_id.encode()).hexdigest()
        subdir = hash_digest[:2]
        dir_path = self.base_dir / subdir
        dir_path.mkdir(exist_ok=True)
        file_path = dir_path / f"{query_id}.jsonl"
        return file_path

    def write(self, metrics: QueryMetrics):
        file_path = self._get_audit_path(metrics.query_id)
        with file_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(metrics)) + "\n")
        logger.debug("Audit trail written for query {}", metrics.query_id)

COLLECTOR = TelemetryCollector()