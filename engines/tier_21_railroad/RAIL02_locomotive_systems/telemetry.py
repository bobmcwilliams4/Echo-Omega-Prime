import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any, Union
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "RAIL02"

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
        self._doctrine_counter: Counter = Counter()
        self._cache_counter: Counter = Counter()
        self._mode_counter: Counter = Counter()
        self._confidence_values: List[float] = []
        self._error_types: Counter = Counter()
        self._audit_writer = AuditTrailWriter()
        logger.info(f"TelemetryCollector initialized for engine {ENGINE_ID}")

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._query_index[metrics.query_id] = metrics
        self._doctrine_counter[metrics.doctrine_matched] += 1
        self._cache_counter[metrics.cache_hit] += 1
        self._mode_counter[metrics.mode] += 1
        if metrics.confidence is not None:
            self._confidence_values.append(metrics.confidence)
        if metrics.error:
            self.record_error(error_type=metrics.error, message="Query error", query_id=metrics.query_id)
        self._audit_writer.write(metrics)
        logger.debug(f"Recorded query: {metrics.query_id}")

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "engine_id": ENGINE_ID,
            "error_type": error_type,
            "message": message,
            "query_id": query_id
        }
        self._errors.append(error_entry)
        self._error_types[error_type] += 1
        logger.warning(f"Recorded error: {error_type} for query {query_id}")

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = [q.latency_ms for q in self._queries if q.latency_ms is not None]
        if not latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = latencies_sorted[int(0.95 * len(latencies_sorted))-1]
        p99 = latencies_sorted[int(0.99 * len(latencies_sorted))-1]
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
        logger.info(f"Latency stats: {stats}")
        return stats

    def get_doctrine_hit_rate(self) -> float:
        total = sum(self._doctrine_counter.values())
        hits = self._doctrine_counter.get(True, 0)
        rate = hits / total if total > 0 else 0.0
        logger.info(f"Doctrine hit rate: {rate:.4f}")
        return rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        queries_in_window = [q for q in self._queries if q.timestamp >= window_start]
        error_rate = len(errors_in_window) / len(queries_in_window) if queries_in_window else 0.0
        logger.info(f"Error rate in last {window_hours} hours: {error_rate:.4f}")
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= hour_ago)
        logger.info(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        total = len(self._queries)
        doctrine_hits = self._doctrine_counter.get(True, 0)
        cache_hits = self._cache_counter.get(True, 0)
        modes = dict(self._mode_counter)
        avg_confidence = statistics.mean(self._confidence_values) if self._confidence_values else None
        coverage = {
            "total_queries": total,
            "doctrine_hits": doctrine_hits,
            "cache_hits": cache_hits,
            "modes": modes,
            "avg_confidence": avg_confidence,
            "error_types": dict(self._error_types)
        }
        logger.info(f"Coverage report: {coverage}")
        return coverage

    def export_jsonl(self, path: Union[str, pathlib.Path]) -> int:
        p = pathlib.Path(path)
        count = 0
        with p.open("w", encoding="utf-8") as f:
            for q in self._queries:
                f.write(json.dumps(asdict(q)) + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {p}")
        return count

class AuditTrailWriter:
    def __init__(self, audit_dir: Union[str, pathlib.Path] = "audit_trail"):
        self.audit_dir = pathlib.Path(audit_dir)
        self.audit_dir.mkdir(exist_ok=True)
        logger.info(f"AuditTrailWriter initialized at {self.audit_dir}")

    def write(self, metrics: QueryMetrics):
        filename = self._get_audit_filename(metrics.query_id)
        entry = asdict(metrics)
        with open(filename, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        logger.debug(f"Wrote audit trail for query {metrics.query_id} to {filename}")

    def _get_audit_filename(self, query_id: str) -> str:
        hash_id = hashlib.sha256(query_id.encode()).hexdigest()[:8]
        filename = self.audit_dir / f"{ENGINE_ID}_audit_{hash_id}.jsonl"
        return str(filename)

COLLECTOR = TelemetryCollector()