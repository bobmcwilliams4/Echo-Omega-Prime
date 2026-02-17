import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any, Union
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "AERO04"

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
        self._queries = deque(maxlen=max_queries)
        self._errors = deque(maxlen=max_errors)
        self._query_index = {}
        self._error_index = {}
        self._doctrine_hits = 0
        self._doctrine_total = 0
        self._cache_hits = 0
        self._cache_total = 0
        self._coverage_counter = Counter()
        self._mode_counter = Counter()
        self._confidence_values = []
        self._latency_values = []
        self._last_hour_queries = deque()
        self._audit_writer = AuditTrailWriter()
        logger.info("TelemetryCollector initialized for ENGINE_ID={}", ENGINE_ID)

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._query_index[metrics.query_id] = metrics
        self._latency_values.append(metrics.latency_ms)
        self._confidence_values.append(metrics.confidence)
        self._mode_counter[metrics.mode] += 1
        self._coverage_counter['total'] += 1
        if metrics.doctrine_matched:
            self._doctrine_hits += 1
        self._doctrine_total += 1
        if metrics.cache_hit:
            self._cache_hits += 1
        self._cache_total += 1
        if metrics.error:
            self.record_error(metrics.error, metrics.error, metrics.query_id)
        now = time.time()
        self._last_hour_queries.append((now, metrics.query_id))
        self._cleanup_last_hour(now)
        self._audit_writer.write(metrics)
        logger.debug("Recorded query: {}", metrics)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "error_type": error_type,
            "message": message,
            "timestamp": time.time(),
            "query_id": query_id,
            "engine_id": ENGINE_ID
        }
        self._errors.append(error_entry)
        self._error_index[hashlib.md5(json.dumps(error_entry, sort_keys=True).encode()).hexdigest()] = error_entry
        self._coverage_counter['errors'] += 1
        logger.error("Recorded error: {}", error_entry)

    def get_latency_stats(self) -> Dict[str, Any]:
        if not self._latency_values:
            return {
                "avg": None,
                "p50": None,
                "p95": None,
                "p99": None,
                "min": None,
                "max": None
            }
        latencies = sorted(self._latency_values)
        avg = statistics.mean(latencies)
        min_latency = min(latencies)
        max_latency = max(latencies)
        p50 = statistics.median(latencies)
        p95 = latencies[int(len(latencies) * 0.95) - 1] if len(latencies) >= 20 else max_latency
        p99 = latencies[int(len(latencies) * 0.99) - 1] if len(latencies) >= 100 else max_latency
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
        error_count = 0
        query_count = 0
        for q in self._queries:
            if q.timestamp >= window_start:
                query_count += 1
                if q.error:
                    error_count += 1
        if query_count == 0:
            return 0.0
        error_rate = error_count / query_count
        logger.info("Error rate in last {:.2f} hours: {:.2f}", window_hours, error_rate)
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        self._cleanup_last_hour(now)
        count = len(self._last_hour_queries)
        logger.info("Queries in last hour: {}", count)
        return count

    def _cleanup_last_hour(self, now: float):
        cutoff = now - 3600
        while self._last_hour_queries and self._last_hour_queries[0][0] < cutoff:
            self._last_hour_queries.popleft()

    def get_coverage_report(self) -> Dict[str, Any]:
        total = self._coverage_counter['total']
        errors = self._coverage_counter['errors']
        modes = dict(self._mode_counter)
        cache_hit_rate = self._cache_hits / self._cache_total if self._cache_total else 0.0
        doctrine_hit_rate = self.get_doctrine_hit_rate()
        avg_confidence = statistics.mean(self._confidence_values) if self._confidence_values else None
        report = {
            "total_queries": total,
            "total_errors": errors,
            "mode_distribution": modes,
            "cache_hit_rate": cache_hit_rate,
            "doctrine_hit_rate": doctrine_hit_rate,
            "avg_confidence": avg_confidence,
            "latency_stats": self.get_latency_stats()
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
        logger.info("Exported {} queries to {}", count, path)
        return count

class AuditTrailWriter:
    def __init__(self, audit_dir: Union[str, pathlib.Path] = "audit_trail"):
        self.audit_dir = pathlib.Path(audit_dir)
        self.audit_dir.mkdir(exist_ok=True)
        logger.info("AuditTrailWriter initialized at {}", self.audit_dir)

    def write(self, metrics: QueryMetrics):
        audit_path = self.audit_dir / f"{metrics.query_id}.jsonl"
        with audit_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(metrics)) + "\n")
        logger.debug("Audit trail written for query_id={}", metrics.query_id)

COLLECTOR = TelemetryCollector()