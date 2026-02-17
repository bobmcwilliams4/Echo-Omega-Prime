import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Tuple
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "OFE01"

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
        self._query_index: Dict[str, QueryMetrics] = {}
        self._error_index: Dict[str, Dict[str, Any]] = {}
        self._doctrine_hits: int = 0
        self._doctrine_total: int = 0
        self._latencies: List[float] = []
        self._coverage_counter: Counter = Counter()
        self._last_export_time: float = time.time()
        self._audit_writer = AuditTrailWriter()
        logger.info("TelemetryCollector initialized for engine {}", ENGINE_ID)

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._query_index[metrics.query_id] = metrics
        self._latencies.append(metrics.latency_ms)
        self._doctrine_total += 1
        if metrics.doctrine_matched:
            self._doctrine_hits += 1
        self._coverage_counter[metrics.mode] += 1
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
        error_hash = hashlib.sha256(json.dumps(error_entry, sort_keys=True).encode()).hexdigest()
        self._error_index[error_hash] = error_entry
        logger.error("Recorded error: {}", error_entry)

    def get_latency_stats(self) -> Dict[str, Any]:
        if not self._latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        latencies = self._latencies
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = statistics.quantiles(latencies, n=100)[94]
        p99 = statistics.quantiles(latencies, n=100)[98]
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
        logger.info("Latency stats: {}", stats)
        return stats

    def get_doctrine_hit_rate(self) -> float:
        if self._doctrine_total == 0:
            return 0.0
        hit_rate = self._doctrine_hits / self._doctrine_total
        logger.info("Doctrine hit rate: {:.3f}", hit_rate)
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        queries_in_window = [q for q in self._queries if q.timestamp >= window_start]
        if not queries_in_window:
            return 0.0
        error_rate = len(errors_in_window) / len(queries_in_window)
        logger.info("Error rate in last {} hours: {:.3f}", window_hours, error_rate)
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= one_hour_ago)
        logger.info("Queries in last hour: {}", count)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        total = sum(self._coverage_counter.values())
        if total == 0:
            return {}
        coverage = {mode: count / total for mode, count in self._coverage_counter.items()}
        logger.info("Coverage report: {}", coverage)
        return coverage

    def export_jsonl(self, path: str) -> int:
        export_path = pathlib.Path(path)
        count = 0
        with export_path.open("w", encoding="utf-8") as f:
            for metrics in self._queries:
                f.write(json.dumps(dataclasses.asdict(metrics)) + "\n")
                count += 1
        logger.info("Exported {} queries to {}", count, path)
        self._last_export_time = time.time()
        return count

class AuditTrailWriter:
    def __init__(self, base_path: str = "./audit_trail"):
        self.base_path = pathlib.Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        logger.info("AuditTrailWriter initialized at {}", self.base_path)

    def _get_audit_path(self, query_id: str) -> pathlib.Path:
        filename = f"{ENGINE_ID}_{query_id}.jsonl"
        return self.base_path / filename

    def write(self, metrics: QueryMetrics):
        path = self._get_audit_path(metrics.query_id)
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(dataclasses.asdict(metrics)) + "\n")
        logger.debug("Wrote audit trail for query {}", metrics.query_id)

COLLECTOR = TelemetryCollector()