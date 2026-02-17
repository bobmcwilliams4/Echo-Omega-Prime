import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "FRAC08"

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
        self._queries: deque = deque(maxlen=maxlen)
        self._errors: deque = deque(maxlen=maxlen)
        self._query_id_index: Dict[str, QueryMetrics] = {}
        self._doctrine_hits: int = 0
        self._doctrine_total: int = 0
        self._error_counter: Counter = Counter()
        self._mode_counter: Counter = Counter()
        self._confidence_list: List[float] = []
        self._cache_hit_counter: Counter = Counter()
        self._coverage_counter: Counter = Counter()
        self._last_exported: float = 0.0
        self._audit_writer = AuditTrailWriter()
        logger.info("TelemetryCollector initialized for engine {}", ENGINE_ID)

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._query_id_index[metrics.query_id] = metrics
        self._mode_counter[metrics.mode] += 1
        self._confidence_list.append(metrics.confidence)
        self._cache_hit_counter["hit" if metrics.cache_hit else "miss"] += 1
        self._doctrine_total += 1
        if metrics.doctrine_matched:
            self._doctrine_hits += 1
        self._coverage_counter[metrics.mode] += 1
        if metrics.error:
            self.record_error("query_error", metrics.error, metrics.query_id)
        self._audit_writer.write(metrics)
        logger.debug("Recorded query: {}", metrics)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "engine_id": ENGINE_ID,
            "timestamp": time.time()
        }
        self._errors.append(error_entry)
        self._error_counter[error_type] += 1
        logger.error("Error recorded: {} for query {}", error_type, query_id)

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = [q.latency_ms for q in self._queries if q.latency_ms is not None]
        if not latencies:
            return {
                "avg": None, "p50": None, "p95": None, "p99": None,
                "min": None, "max": None
            }
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        min_latency = min(latencies)
        max_latency = max(latencies)
        p50 = statistics.median(latencies)
        p95 = latencies_sorted[int(0.95 * len(latencies_sorted)) - 1]
        p99 = latencies_sorted[int(0.99 * len(latencies_sorted)) - 1]
        logger.info("Latency stats calculated: avg={}, p50={}, p95={}, p99={}, min={}, max={}",
                    avg, p50, p95, p99, min_latency, max_latency)
        return {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_latency,
            "max": max_latency
        }

    def get_doctrine_hit_rate(self) -> float:
        if self._doctrine_total == 0:
            return 0.0
        hit_rate = self._doctrine_hits / self._doctrine_total
        logger.info("Doctrine hit rate: {}", hit_rate)
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        total_queries = sum(1 for q in self._queries if q.timestamp >= window_start)
        total_errors = sum(1 for e in self._errors if e["timestamp"] >= window_start)
        if total_queries == 0:
            return 0.0
        error_rate = total_errors / total_queries
        logger.info("Error rate in last {} hours: {}", window_hours, error_rate)
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= one_hour_ago)
        logger.info("Queries in last hour: {}", count)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {
            "mode_distribution": dict(self._mode_counter),
            "cache_hit_distribution": dict(self._cache_hit_counter),
            "confidence_stats": self._confidence_stats(),
            "doctrine_hit_rate": self.get_doctrine_hit_rate(),
            "error_rate_last_hour": self.get_error_rate(1.0),
            "queries_last_hour": self.queries_last_hour(),
            "total_queries": len(self._queries),
            "total_errors": len(self._errors),
        }
        logger.info("Coverage report generated")
        return report

    def _confidence_stats(self) -> Dict[str, Any]:
        if not self._confidence_list:
            return {
                "avg": None,
                "min": None,
                "max": None,
                "p50": None,
                "p95": None,
                "p99": None
            }
        confidences_sorted = sorted(self._confidence_list)
        avg = statistics.mean(self._confidence_list)
        min_conf = min(self._confidence_list)
        max_conf = max(self._confidence_list)
        p50 = statistics.median(self._confidence_list)
        p95 = confidences_sorted[int(0.95 * len(confidences_sorted)) - 1]
        p99 = confidences_sorted[int(0.99 * len(confidences_sorted)) - 1]
        return {
            "avg": avg,
            "min": min_conf,
            "max": max_conf,
            "p50": p50,
            "p95": p95,
            "p99": p99
        }

    def export_jsonl(self, path: str) -> int:
        out_path = pathlib.Path(path)
        count = 0
        with out_path.open("w", encoding="utf-8") as f:
            for q in self._queries:
                record = {
                    "query_id": q.query_id,
                    "engine_id": q.engine_id,
                    "timestamp": q.timestamp,
                    "latency_ms": q.latency_ms,
                    "cache_hit": q.cache_hit,
                    "doctrine_matched": q.doctrine_matched,
                    "mode": q.mode,
                    "confidence": q.confidence,
                    "error": q.error
                }
                f.write(json.dumps(record) + "\n")
                count += 1
        self._last_exported = time.time()
        logger.info("Exported {} queries to {}", count, path)
        return count

class AuditTrailWriter:
    def __init__(self, base_dir: str = "./audit_trails"):
        self.base_dir = pathlib.Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        logger.info("AuditTrailWriter initialized at {}", self.base_dir)

    def write(self, metrics: QueryMetrics):
        audit_record = {
            "query_id": metrics.query_id,
            "engine_id": metrics.engine_id,
            "timestamp": metrics.timestamp,
            "latency_ms": metrics.latency_ms,
            "cache_hit": metrics.cache_hit,
            "doctrine_matched": metrics.doctrine_matched,
            "mode": metrics.mode,
            "confidence": metrics.confidence,
            "error": metrics.error
        }
        filename = self._audit_filename(metrics.query_id)
        file_path = self.base_dir / filename
        with file_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(audit_record) + "\n")
        logger.debug("Audit trail written for query {}", metrics.query_id)

    def _audit_filename(self, query_id: str) -> str:
        # Use a hash for filename uniqueness and privacy
        hash_id = hashlib.sha256(query_id.encode("utf-8")).hexdigest()
        return f"{hash_id}.jsonl"

COLLECTOR = TelemetryCollector()