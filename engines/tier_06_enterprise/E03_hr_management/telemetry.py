import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Union
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "E03"

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
        self._doctrine_hits: deque = deque(maxlen=max_queries)
        self._audit_trail: deque = deque(maxlen=max_queries)
        self._query_id_set: set = set()
        self._error_counter: Counter = Counter()
        self._coverage_counter: Counter = Counter()
        self._mode_counter: Counter = Counter()
        self._confidence_list: List[float] = []
        self._last_exported_index: int = 0

    def record_query(self, metrics: QueryMetrics):
        logger.debug(f"Recording query: {metrics}")
        if metrics.query_id in self._query_id_set:
            logger.warning(f"Duplicate query_id detected: {metrics.query_id}")
            return
        self._queries.append(metrics)
        self._query_id_set.add(metrics.query_id)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._mode_counter[metrics.mode] += 1
        self._coverage_counter['total'] += 1
        if metrics.doctrine_matched:
            self._coverage_counter['doctrine_matched'] += 1
        self._confidence_list.append(metrics.confidence)
        if metrics.error:
            self.record_error(error_type=metrics.error, message="Query error", query_id=metrics.query_id)
        self._audit_trail.append({
            "query_id": metrics.query_id,
            "engine_id": metrics.engine_id,
            "timestamp": metrics.timestamp,
            "latency_ms": metrics.latency_ms,
            "cache_hit": metrics.cache_hit,
            "doctrine_matched": metrics.doctrine_matched,
            "mode": metrics.mode,
            "confidence": metrics.confidence,
            "error": metrics.error
        })

    def record_error(self, error_type: str, message: str, query_id: str):
        logger.error(f"Recording error: {error_type} for query {query_id}: {message}")
        error_entry = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "timestamp": time.time()
        }
        self._errors.append(error_entry)
        self._error_counter[error_type] += 1

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = [q.latency_ms for q in self._queries if q.latency_ms is not None]
        if not latencies:
            return {
                "avg": None,
                "p50": None,
                "p95": None,
                "p99": None,
                "min": None,
                "max": None
            }
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies_sorted)
        p95 = latencies_sorted[int(0.95 * len(latencies_sorted)) - 1]
        p99 = latencies_sorted[int(0.99 * len(latencies_sorted)) - 1]
        min_latency = min(latencies_sorted)
        max_latency = max(latencies_sorted)
        logger.info(f"Latency stats: avg={avg}, p50={p50}, p95={p95}, p99={p99}, min={min_latency}, max={max_latency}")
        return {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_latency,
            "max": max_latency
        }

    def get_doctrine_hit_rate(self) -> float:
        total = len(self._doctrine_hits)
        if total == 0:
            return 0.0
        hits = sum(1 for hit in self._doctrine_hits if hit)
        hit_rate = hits / total
        logger.info(f"Doctrine hit rate: {hit_rate:.4f}")
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        queries_in_window = [q for q in self._queries if q.timestamp >= window_start]
        if not queries_in_window:
            return 0.0
        error_rate = len(errors_in_window) / len(queries_in_window)
        logger.info(f"Error rate in last {window_hours} hours: {error_rate:.4f}")
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= hour_ago)
        logger.info(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        total = self._coverage_counter['total']
        doctrine_matched = self._coverage_counter.get('doctrine_matched', 0)
        coverage = doctrine_matched / total if total > 0 else 0.0
        mode_distribution = dict(self._mode_counter)
        confidence_avg = statistics.mean(self._confidence_list) if self._confidence_list else None
        report = {
            "total_queries": total,
            "doctrine_matched": doctrine_matched,
            "coverage": coverage,
            "mode_distribution": mode_distribution,
            "confidence_avg": confidence_avg
        }
        logger.info(f"Coverage report: {report}")
        return report

    def export_jsonl(self, path: Union[str, pathlib.Path]) -> int:
        path = pathlib.Path(path)
        logger.info(f"Exporting telemetry to {path}")
        exported_count = 0
        with path.open("a", encoding="utf-8") as f:
            for idx, entry in enumerate(list(self._audit_trail)[self._last_exported_index:]):
                f.write(json.dumps(entry) + "\n")
                exported_count += 1
            self._last_exported_index += exported_count
        logger.success(f"Exported {exported_count} telemetry entries to {path}")
        return exported_count

class AuditTrailWriter:
    def __init__(self, path: Union[str, pathlib.Path]):
        self.path = pathlib.Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = None  # Placeholder for threading.Lock if needed

    def write(self, query_metrics: QueryMetrics):
        entry = {
            "query_id": query_metrics.query_id,
            "engine_id": query_metrics.engine_id,
            "timestamp": query_metrics.timestamp,
            "latency_ms": query_metrics.latency_ms,
            "cache_hit": query_metrics.cache_hit,
            "doctrine_matched": query_metrics.doctrine_matched,
            "mode": query_metrics.mode,
            "confidence": query_metrics.confidence,
            "error": query_metrics.error
        }
        logger.debug(f"Writing audit trail entry: {entry}")
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

COLLECTOR = TelemetryCollector()

# Example usage (commented out):
# metrics = QueryMetrics(
#     query_id="abc123",
#     engine_id=ENGINE_ID,
#     timestamp=time.time(),
#     latency_ms=120.5,
#     cache_hit=True,
#     doctrine_matched=False,
#     mode="search",
#     confidence=0.92,
#     error=None
# )
# COLLECTOR.record_query(metrics)
# COLLECTOR.record_error("Timeout", "Query timed out", metrics.query_id)
# stats = COLLECTOR.get_latency_stats()
# hit_rate = COLLECTOR.get_doctrine_hit_rate()
# error_rate = COLLECTOR.get_error_rate(1.0)
# coverage = COLLECTOR.get_coverage_report()
# COLLECTOR.export_jsonl("telemetry_export.jsonl")
# writer = AuditTrailWriter("audit_trail.jsonl")
# writer.write(metrics)