import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "PRB05"

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
        self._query_index: Dict[str, QueryMetrics] = {}
        self._doctrine_counter: Counter = Counter()
        self._cache_counter: Counter = Counter()
        self._mode_counter: Counter = Counter()
        self._confidence_list: List[float] = []
        self._coverage_modes: set = set()
        self._coverage_doctrines: set = set()
        self._coverage_queries: set = set()
        self._latencies: List[float] = []
        self._error_types: Counter = Counter()
        self._audit_writer = AuditTrailWriter()
        logger.info("TelemetryCollector initialized for engine_id={}", ENGINE_ID)

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._query_index[metrics.query_id] = metrics
        self._latencies.append(metrics.latency_ms)
        self._doctrine_counter[metrics.doctrine_matched] += 1
        self._cache_counter[metrics.cache_hit] += 1
        self._mode_counter[metrics.mode] += 1
        self._confidence_list.append(metrics.confidence)
        self._coverage_modes.add(metrics.mode)
        self._coverage_queries.add(metrics.query_id)
        if metrics.doctrine_matched:
            self._coverage_doctrines.add(metrics.query_id)
        if metrics.error:
            self.record_error(metrics.error, "Query error", metrics.query_id)
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
        self._error_types[error_type] += 1
        logger.error("Recorded error: {}", error_entry)

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = [q.latency_ms for q in self._queries if q.latency_ms is not None]
        if not latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies_sorted)
        min_lat = min(latencies_sorted)
        max_lat = max(latencies_sorted)
        p50 = statistics.median(latencies_sorted)
        p95 = latencies_sorted[int(0.95 * len(latencies_sorted))-1]
        p99 = latencies_sorted[int(0.99 * len(latencies_sorted))-1]
        stats = {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_lat,
            "max": max_lat
        }
        logger.info("Latency stats: {}", stats)
        return stats

    def get_doctrine_hit_rate(self) -> float:
        total = sum(self._doctrine_counter.values())
        hits = self._doctrine_counter.get(True, 0)
        hit_rate = hits / total if total > 0 else 0.0
        logger.info("Doctrine hit rate: {}", hit_rate)
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        queries_in_window = [q for q in self._queries if q.timestamp >= window_start]
        error_rate = len(errors_in_window) / len(queries_in_window) if queries_in_window else 0.0
        logger.info("Error rate ({}h): {}", window_hours, error_rate)
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
            "unique_modes": list(self._coverage_modes),
            "doctrine_matched_count": len(self._coverage_doctrines),
            "unique_queries": len(self._coverage_queries),
            "mode_distribution": dict(self._mode_counter),
            "cache_hit_distribution": dict(self._cache_counter),
            "confidence_avg": statistics.mean(self._confidence_list) if self._confidence_list else None,
            "confidence_min": min(self._confidence_list) if self._confidence_list else None,
            "confidence_max": max(self._confidence_list) if self._confidence_list else None
        }
        logger.info("Coverage report: {}", report)
        return report

    def export_jsonl(self, path: str) -> int:
        p = pathlib.Path(path)
        count = 0
        with p.open("w", encoding="utf-8") as f:
            for q in self._queries:
                f.write(json.dumps(dataclasses.asdict(q)) + "\n")
                count += 1
        logger.info("Exported {} queries to {}", count, path)
        return count

class AuditTrailWriter:
    def __init__(self, audit_dir: str = "./audit_trail"):
        self.audit_dir = pathlib.Path(audit_dir)
        self.audit_dir.mkdir(parents=True, exist_ok=True)
        logger.info("AuditTrailWriter initialized at {}", self.audit_dir)

    def write(self, metrics: QueryMetrics):
        filename = self._get_filename(metrics.query_id)
        audit_entry = {
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
        with open(filename, "a", encoding="utf-8") as f:
            f.write(json.dumps(audit_entry) + "\n")
        logger.debug("Audit trail written for query_id={}", metrics.query_id)

    def _get_filename(self, query_id: str) -> str:
        hash_id = hashlib.sha256(query_id.encode("utf-8")).hexdigest()[:16]
        filename = self.audit_dir / f"{hash_id}.jsonl"
        return str(filename)

COLLECTOR = TelemetryCollector()