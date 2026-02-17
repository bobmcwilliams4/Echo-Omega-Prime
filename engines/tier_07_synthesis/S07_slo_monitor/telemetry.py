import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Union
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "S07"

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
        self._doctrine_hits = 0
        self._doctrine_total = 0
        self._latencies = []
        self._query_id_set = set()
        self._coverage_modes = Counter()
        self._coverage_confidence = []
        self._coverage_cache = Counter()
        self._coverage_doctrine = Counter()
        self._coverage_errors = Counter()
        self._audit_writer = AuditTrailWriter()
        logger.info("TelemetryCollector initialized for engine_id={}", ENGINE_ID)

    def record_query(self, metrics: QueryMetrics):
        if metrics.query_id in self._query_id_set:
            logger.warning("Duplicate query_id detected: {}", metrics.query_id)
            return
        self._queries.append(metrics)
        self._query_id_set.add(metrics.query_id)
        self._latencies.append(metrics.latency_ms)
        self._coverage_modes[metrics.mode] += 1
        self._coverage_confidence.append(metrics.confidence)
        self._coverage_cache[metrics.cache_hit] += 1
        self._coverage_doctrine[metrics.doctrine_matched] += 1
        if metrics.doctrine_matched:
            self._doctrine_hits += 1
        self._doctrine_total += 1
        if metrics.error:
            self._coverage_errors[metrics.error] += 1
        self._audit_writer.write(metrics)
        logger.debug("Recorded query: {}", metrics)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "engine_id": ENGINE_ID,
            "error_type": error_type,
            "message": message,
            "query_id": query_id
        }
        self._errors.append(error_entry)
        self._coverage_errors[error_type] += 1
        logger.error("Recorded error: {}", error_entry)

    def get_latency_stats(self) -> Dict[str, Any]:
        if not self._latencies:
            return {
                "avg": None,
                "p50": None,
                "p95": None,
                "p99": None,
                "min": None,
                "max": None
            }
        latencies = sorted(self._latencies)
        avg = statistics.mean(latencies)
        min_latency = min(latencies)
        max_latency = max(latencies)
        p50 = statistics.median(latencies)
        p95 = latencies[int(0.95 * len(latencies)) - 1]
        p99 = latencies[int(0.99 * len(latencies)) - 1]
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
        logger.info("Error rate in last {:.2f} hours: {:.3f}", window_hours, error_rate)
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= one_hour_ago)
        logger.info("Queries in last hour: {}", count)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {
            "total_queries": len(self._queries),
            "modes": dict(self._coverage_modes),
            "confidence_avg": statistics.mean(self._coverage_confidence) if self._coverage_confidence else None,
            "cache_hit_rate": self._coverage_cache.get(True, 0) / max(1, sum(self._coverage_cache.values())),
            "doctrine_hit_rate": self.get_doctrine_hit_rate(),
            "errors": dict(self._coverage_errors)
        }
        logger.info("Coverage report: {}", report)
        return report

    def export_jsonl(self, path: Union[str, pathlib.Path]) -> int:
        path = pathlib.Path(path)
        count = 0
        with path.open("w", encoding="utf-8") as f:
            for q in self._queries:
                f.write(json.dumps(dataclasses.asdict(q)) + "\n")
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
        entry = dataclasses.asdict(metrics)
        with audit_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        logger.debug("Audit trail written for query_id={}", metrics.query_id)

COLLECTOR = TelemetryCollector()