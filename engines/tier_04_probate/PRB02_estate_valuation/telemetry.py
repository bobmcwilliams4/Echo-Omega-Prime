import time
import json
import hashlib
import statistics
import pathlib
import dataclasses
import typing
import collections
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from loguru import logger

ENGINE_ID = "PRB02"

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
    def __init__(self):
        self._queries: List[QueryMetrics] = []
        self._errors: List[Dict[str, Any]] = []
        self._query_index: Dict[str, QueryMetrics] = {}
        self._audit_writer = AuditTrailWriter()
        self._lock = collections.deque(maxlen=0)  # Placeholder for thread safety if needed

    def record_query(self, metrics: QueryMetrics):
        logger.debug(f"Recording query: {metrics}")
        self._queries.append(metrics)
        self._query_index[metrics.query_id] = metrics
        self._audit_writer.write(metrics)
        if metrics.error:
            self.record_error(
                error_type=metrics.error,
                message=f"Error in query {metrics.query_id}",
                query_id=metrics.query_id
            )

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "engine_id": ENGINE_ID,
            "error_type": error_type,
            "message": message,
            "query_id": query_id
        }
        logger.error(f"Recording error: {error_entry}")
        self._errors.append(error_entry)

    def get_latency_stats(self) -> Dict[str, float]:
        latencies = [q.latency_ms for q in self._queries if q.latency_ms is not None]
        if not latencies:
            return {"avg": 0, "p50": 0, "p95": 0, "p99": 0, "min": 0, "max": 0}
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
        logger.debug(f"Latency stats: {stats}")
        return stats

    def get_doctrine_hit_rate(self) -> float:
        if not self._queries:
            return 0.0
        doctrine_hits = sum(1 for q in self._queries if q.doctrine_matched)
        hit_rate = doctrine_hits / len(self._queries)
        logger.debug(f"Doctrine hit rate: {hit_rate}")
        return hit_rate

    def get_error_rate(self, window_hours: float) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        queries_in_window = [q for q in self._queries if q.timestamp >= window_start]
        error_rate = (len(errors_in_window) / len(queries_in_window)) if queries_in_window else 0.0
        logger.debug(f"Error rate in last {window_hours} hours: {error_rate}")
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= one_hour_ago)
        logger.debug(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        total = len(self._queries)
        if total == 0:
            return {
                "total": 0,
                "cache_hits": 0,
                "cache_hit_rate": 0.0,
                "doctrine_matched": 0,
                "doctrine_hit_rate": 0.0,
                "modes": {},
                "confidence_avg": 0.0,
                "errors": 0
            }
        cache_hits = sum(1 for q in self._queries if q.cache_hit)
        doctrine_matched = sum(1 for q in self._queries if q.doctrine_matched)
        modes = collections.Counter(q.mode for q in self._queries)
        confidences = [q.confidence for q in self._queries if q.confidence is not None]
        errors = sum(1 for q in self._queries if q.error)
        report = {
            "total": total,
            "cache_hits": cache_hits,
            "cache_hit_rate": cache_hits / total,
            "doctrine_matched": doctrine_matched,
            "doctrine_hit_rate": doctrine_matched / total,
            "modes": dict(modes),
            "confidence_avg": statistics.mean(confidences) if confidences else 0.0,
            "errors": errors
        }
        logger.debug(f"Coverage report: {report}")
        return report

    def export_jsonl(self, path: typing.Union[str, pathlib.Path]) -> int:
        path = pathlib.Path(path)
        count = 0
        with path.open("w", encoding="utf-8") as f:
            for q in self._queries:
                f.write(json.dumps(dataclasses.asdict(q)) + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {path}")
        return count

class AuditTrailWriter:
    def __init__(self, base_dir: typing.Union[str, pathlib.Path] = "audit_trail"):
        self.base_dir = pathlib.Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def write(self, metrics: QueryMetrics):
        # Use the query_id as filename, hashed to avoid filesystem issues
        query_hash = hashlib.sha256(metrics.query_id.encode()).hexdigest()
        filename = f"{metrics.engine_id}_{query_hash}.jsonl"
        file_path = self.base_dir / filename
        record = dataclasses.asdict(metrics)
        with file_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
        logger.debug(f"Wrote audit trail for query {metrics.query_id} to {file_path}")

COLLECTOR = TelemetryCollector()