import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any, Deque
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "PROD06"

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
        self.queries: Deque[QueryMetrics] = deque(maxlen=maxlen)
        self.errors: Deque[Dict[str, Any]] = deque(maxlen=maxlen)
        self.audit_trail_path: Optional[pathlib.Path] = None
        self.audit_writer: Optional['AuditTrailWriter'] = None
        self._doctrine_counter: Counter = Counter()
        self._cache_counter: Counter = Counter()
        self._mode_counter: Counter = Counter()
        self._last_exported_idx = 0
        logger.info("TelemetryCollector initialized with maxlen={}", maxlen)

    def record_query(self, metrics: QueryMetrics):
        self.queries.append(metrics)
        self._doctrine_counter[metrics.doctrine_matched] += 1
        self._cache_counter[metrics.cache_hit] += 1
        self._mode_counter[metrics.mode] += 1
        if metrics.error:
            self.record_error("query_error", metrics.error, metrics.query_id)
        if self.audit_writer:
            self.audit_writer.write(metrics)
        logger.debug("Recorded query: {}", metrics)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "timestamp": time.time()
        }
        self.errors.append(error_entry)
        logger.warning("Recorded error: {}", error_entry)

    def get_latency_stats(self) -> Dict[str, float]:
        latencies = [q.latency_ms for q in self.queries if q.latency_ms is not None]
        if not latencies:
            logger.info("No latency data available for stats.")
            return {"avg": 0, "p50": 0, "p95": 0, "p99": 0, "min": 0, "max": 0}
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = latencies_sorted[int(0.95 * len(latencies_sorted)) - 1]
        p99 = latencies_sorted[int(0.99 * len(latencies_sorted)) - 1]
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
        logger.debug("Latency stats: {}", stats)
        return stats

    def get_doctrine_hit_rate(self) -> float:
        total = sum(self._doctrine_counter.values())
        if total == 0:
            logger.info("No queries to compute doctrine hit rate.")
            return 0.0
        hit_rate = self._doctrine_counter[True] / total
        logger.debug("Doctrine hit rate: {:.3f}", hit_rate)
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        total_queries = sum(1 for q in self.queries if q.timestamp >= window_start)
        total_errors = sum(1 for e in self.errors if e["timestamp"] >= window_start)
        if total_queries == 0:
            logger.info("No queries in window to compute error rate.")
            return 0.0
        error_rate = total_errors / total_queries
        logger.debug("Error rate in last {} hours: {:.3f}", window_hours, error_rate)
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self.queries if q.timestamp >= one_hour_ago)
        logger.debug("Queries in last hour: {}", count)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        total = len(self.queries)
        if total == 0:
            logger.info("No queries for coverage report.")
            return {
                "total": 0,
                "cache_hit_rate": 0.0,
                "doctrine_hit_rate": 0.0,
                "mode_distribution": {},
                "confidence_avg": 0.0
            }
        cache_hit_rate = self._cache_counter[True] / total
        doctrine_hit_rate = self._doctrine_counter[True] / total
        mode_distribution = {mode: count / total for mode, count in self._mode_counter.items()}
        confidence_values = [q.confidence for q in self.queries if q.confidence is not None]
        confidence_avg = statistics.mean(confidence_values) if confidence_values else 0.0
        report = {
            "total": total,
            "cache_hit_rate": cache_hit_rate,
            "doctrine_hit_rate": doctrine_hit_rate,
            "mode_distribution": mode_distribution,
            "confidence_avg": confidence_avg
        }
        logger.debug("Coverage report: {}", report)
        return report

    def export_jsonl(self, path: str) -> int:
        export_path = pathlib.Path(path)
        export_path.parent.mkdir(parents=True, exist_ok=True)
        count = 0
        with export_path.open("a", encoding="utf-8") as f:
            for idx, q in enumerate(list(self.queries)[self._last_exported_idx:]):
                f.write(json.dumps(asdict(q)) + "\n")
                count += 1
            self._last_exported_idx += count
        logger.info("Exported {} queries to {}", count, export_path)
        return count

    def set_audit_trail(self, path: str):
        self.audit_trail_path = pathlib.Path(path)
        self.audit_writer = AuditTrailWriter(self.audit_trail_path)
        logger.info("Audit trail writer set to {}", self.audit_trail_path)

class AuditTrailWriter:
    def __init__(self, path: pathlib.Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        logger.info("AuditTrailWriter initialized at {}", self.path)

    def write(self, metrics: QueryMetrics):
        entry = asdict(metrics)
        entry["audit_id"] = self._compute_audit_id(entry)
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        logger.debug("Wrote audit trail entry: {}", entry["audit_id"])

    def _compute_audit_id(self, entry: Dict[str, Any]) -> str:
        m = hashlib.sha256()
        m.update((entry["query_id"] + str(entry["timestamp"]) + ENGINE_ID).encode())
        return m.hexdigest()

COLLECTOR = TelemetryCollector()