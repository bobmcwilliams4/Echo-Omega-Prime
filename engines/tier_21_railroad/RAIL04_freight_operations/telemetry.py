import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "RAIL04"

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
    def __init__(self, max_queries: int = 100000):
        self._queries: deque = deque(maxlen=max_queries)
        self._errors: deque = deque(maxlen=max_queries)
        self._query_index: Dict[str, QueryMetrics] = {}
        self._error_index: Dict[str, Dict[str, Any]] = {}
        self._doctrine_counter: Counter = Counter()
        self._cache_counter: Counter = Counter()
        self._mode_counter: Counter = Counter()
        self._confidence_values: List[float] = []
        self._coverage: Dict[str, set] = defaultdict(set)
        self._audit_writer = AuditTrailWriter()
        logger.info("TelemetryCollector initialized with max_queries={}", max_queries)

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._query_index[metrics.query_id] = metrics
        self._doctrine_counter.update([metrics.doctrine_matched])
        self._cache_counter.update([metrics.cache_hit])
        self._mode_counter.update([metrics.mode])
        self._confidence_values.append(metrics.confidence)
        self._coverage[metrics.mode].add(metrics.query_id)
        self._audit_writer.write(metrics)
        logger.debug("Recorded query: {}", metrics)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "timestamp": time.time(),
            "engine_id": ENGINE_ID
        }
        self._errors.append(error_entry)
        if query_id:
            self._error_index[query_id] = error_entry
            if query_id in self._query_index:
                self._query_index[query_id].error = error_type
        logger.error("Recorded error: {}", error_entry)

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = [q.latency_ms for q in self._queries if q.latency_ms is not None]
        if not latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = latencies_sorted[int(0.95 * len(latencies_sorted)) - 1]
        p99 = latencies_sorted[int(0.99 * len(latencies_sorted)) - 1]
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
        total = sum(self._doctrine_counter.values())
        if total == 0:
            return 0.0
        hit_rate = self._doctrine_counter[True] / total
        logger.info("Doctrine hit rate: {}", hit_rate)
        return hit_rate

    def get_error_rate(self, window_hours: int = 1) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        queries_in_window = [q for q in self._queries if q.timestamp >= window_start]
        num_errors = len(errors_in_window)
        num_queries = len(queries_in_window)
        if num_queries == 0:
            return 0.0
        error_rate = num_errors / num_queries
        logger.info("Error rate ({}h): {}", window_hours, error_rate)
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= one_hour_ago)
        logger.info("Queries last hour: {}", count)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {}
        total_queries = len(self._queries)
        for mode, queries in self._coverage.items():
            report[mode] = {
                "count": len(queries),
                "coverage_pct": (len(queries) / total_queries) * 100 if total_queries > 0 else 0
            }
        logger.info("Coverage report: {}", report)
        return report

    def export_jsonl(self, path: str) -> int:
        p = pathlib.Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        count = 0
        with p.open("w", encoding="utf-8") as f:
            for q in self._queries:
                f.write(json.dumps(q.__dict__) + "\n")
                count += 1
        logger.info("Exported {} queries to {}", count, path)
        return count

class AuditTrailWriter:
    def __init__(self, audit_dir: str = "./audit_trail"):
        self.audit_dir = pathlib.Path(audit_dir)
        self.audit_dir.mkdir(parents=True, exist_ok=True)
        logger.info("AuditTrailWriter initialized at {}", self.audit_dir)

    def _get_audit_path(self, query_id: str) -> pathlib.Path:
        hash_id = hashlib.sha256(query_id.encode("utf-8")).hexdigest()
        subdir = self.audit_dir / hash_id[:2]
        subdir.mkdir(parents=True, exist_ok=True)
        audit_path = subdir / f"{hash_id}.jsonl"
        return audit_path

    def write(self, metrics: QueryMetrics):
        audit_path = self._get_audit_path(metrics.query_id)
        with audit_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(metrics.__dict__) + "\n")
        logger.debug("Audit written for query_id {} at {}", metrics.query_id, audit_path)

COLLECTOR = TelemetryCollector()