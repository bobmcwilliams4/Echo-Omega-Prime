import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any, Tuple
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "MECH11"

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
    def __init__(self, max_queries: int = 10000):
        self._queries: deque = deque(maxlen=max_queries)
        self._errors: deque = deque(maxlen=max_queries)
        self._query_id_index: Dict[str, QueryMetrics] = {}
        self._error_counter: Counter = Counter()
        self._doctrine_hits: int = 0
        self._doctrine_total: int = 0
        self._latencies: List[float] = []
        self._coverage_modes: Counter = Counter()
        self._coverage_cache_hit: Counter = Counter()
        self._coverage_doctrine: Counter = Counter()
        self._coverage_confidence: List[float] = []
        self._audit_writer = AuditTrailWriter()
        logger.info("TelemetryCollector initialized for engine '{}'", ENGINE_ID)

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._query_id_index[metrics.query_id] = metrics
        self._latencies.append(metrics.latency_ms)
        self._coverage_modes[metrics.mode] += 1
        self._coverage_cache_hit[str(metrics.cache_hit)] += 1
        self._coverage_doctrine[str(metrics.doctrine_matched)] += 1
        self._coverage_confidence.append(metrics.confidence)
        self._doctrine_total += 1
        if metrics.doctrine_matched:
            self._doctrine_hits += 1
        if metrics.error:
            self.record_error(metrics.error, metrics.error, metrics.query_id)
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
        self._error_counter[error_type] += 1
        logger.warning("Error recorded: {} - {}", error_type, message)

    def get_latency_stats(self) -> Dict[str, Any]:
        if not self._latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        latencies_sorted = sorted(self._latencies)
        avg = statistics.mean(self._latencies)
        p50 = statistics.median(latencies_sorted)
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
        queries_in_window = [q for q in self._queries if q.timestamp >= window_start]
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        total_queries = len(queries_in_window)
        total_errors = len(errors_in_window)
        error_rate = (total_errors / total_queries) if total_queries > 0 else 0.0
        logger.info("Error rate in last {:.2f} hours: {:.4f}", window_hours, error_rate)
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= hour_ago)
        logger.info("Queries in last hour: {}", count)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {
            "mode_distribution": dict(self._coverage_modes),
            "cache_hit_distribution": dict(self._coverage_cache_hit),
            "doctrine_matched_distribution": dict(self._coverage_doctrine),
            "confidence_stats": self._confidence_stats(),
            "total_queries": len(self._queries),
            "total_errors": len(self._errors),
            "doctrine_hit_rate": self.get_doctrine_hit_rate(),
            "error_rate_last_hour": self.get_error_rate(1.0),
            "latency_stats": self.get_latency_stats()
        }
        logger.info("Coverage report generated")
        return report

    def _confidence_stats(self) -> Dict[str, Any]:
        if not self._coverage_confidence:
            return {"avg": None, "min": None, "max": None, "p50": None, "p95": None}
        confidences_sorted = sorted(self._coverage_confidence)
        avg = statistics.mean(self._coverage_confidence)
        min_conf = confidences_sorted[0]
        max_conf = confidences_sorted[-1]
        p50 = statistics.median(confidences_sorted)
        p95 = confidences_sorted[int(0.95 * len(confidences_sorted)) - 1]
        stats = {
            "avg": avg,
            "min": min_conf,
            "max": max_conf,
            "p50": p50,
            "p95": p95
        }
        return stats

    def export_jsonl(self, path: str) -> int:
        p = pathlib.Path(path)
        count = 0
        with p.open("w", encoding="utf-8") as f:
            for q in self._queries:
                f.write(json.dumps(asdict(q)) + "\n")
                count += 1
        logger.info("Exported {} queries to {}", count, path)
        return count

class AuditTrailWriter:
    def __init__(self, base_path: Optional[str] = None):
        self.base_path = base_path or "./audit_trails"
        self._ensure_dir(self.base_path)
        logger.info("AuditTrailWriter initialized at '{}'", self.base_path)

    def _ensure_dir(self, path: str):
        p = pathlib.Path(path)
        if not p.exists():
            p.mkdir(parents=True, exist_ok=True)

    def _get_audit_path(self, query_id: str) -> pathlib.Path:
        hash_id = hashlib.sha256(query_id.encode()).hexdigest()[:8]
        filename = f"{ENGINE_ID}_{hash_id}_{query_id}.jsonl"
        return pathlib.Path(self.base_path) / filename

    def write(self, metrics: QueryMetrics):
        audit_path = self._get_audit_path(metrics.query_id)
        with audit_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(metrics)) + "\n")
        logger.debug("Audit trail written for query_id '{}'", metrics.query_id)

COLLECTOR = TelemetryCollector()