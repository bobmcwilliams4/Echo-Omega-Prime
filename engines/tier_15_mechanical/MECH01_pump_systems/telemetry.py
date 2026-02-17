import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Union
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "MECH01"

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
        self.queries: deque = deque(maxlen=max_queries)
        self.errors: deque = deque(maxlen=max_queries)
        self.audit_trail: deque = deque(maxlen=max_queries)
        self._query_id_index: Dict[str, QueryMetrics] = {}
        self._error_counter: Counter = Counter()
        self._doctrine_counter: Counter = Counter()
        self._cache_counter: Counter = Counter()
        self._mode_counter: Counter = Counter()
        self._confidence_list: List[float] = []
        self._latency_list: List[float] = []
        self._coverage_counter: Counter = Counter()
        self._last_export_count: int = 0

    def record_query(self, metrics: QueryMetrics):
        self.queries.append(metrics)
        self._query_id_index[metrics.query_id] = metrics
        self._latency_list.append(metrics.latency_ms)
        self._doctrine_counter[metrics.doctrine_matched] += 1
        self._cache_counter[metrics.cache_hit] += 1
        self._mode_counter[metrics.mode] += 1
        self._confidence_list.append(metrics.confidence)
        self._coverage_counter[(metrics.mode, metrics.doctrine_matched)] += 1
        self.audit_trail.append({
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
        if metrics.error:
            self.record_error(metrics.error, metrics.error, metrics.query_id)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "error_type": error_type,
            "message": message,
            "timestamp": time.time(),
            "query_id": query_id
        }
        self.errors.append(error_entry)
        self._error_counter[error_type] += 1
        logger.error(f"Error recorded: {error_type} | {message} | Query ID: {query_id}")

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = [q.latency_ms for q in self.queries if q.latency_ms is not None]
        if not latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies_sorted)
        min_latency = latencies_sorted[0]
        max_latency = latencies_sorted[-1]
        p50 = statistics.median(latencies_sorted)
        p95 = latencies_sorted[int(0.95 * len(latencies_sorted)) - 1]
        p99 = latencies_sorted[int(0.99 * len(latencies_sorted)) - 1]
        return {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_latency,
            "max": max_latency
        }

    def get_doctrine_hit_rate(self) -> float:
        total = sum(self._doctrine_counter.values())
        if total == 0:
            return 0.0
        hits = self._doctrine_counter[True]
        return hits / total

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        error_count = sum(1 for e in self.errors if e['timestamp'] >= window_start)
        query_count = sum(1 for q in self.queries if q.timestamp >= window_start)
        if query_count == 0:
            return 0.0
        return error_count / query_count

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        return sum(1 for q in self.queries if q.timestamp >= one_hour_ago)

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {}
        total = len(self.queries)
        report['total_queries'] = total
        report['modes'] = dict(self._mode_counter)
        report['doctrine_matched'] = dict(self._doctrine_counter)
        report['cache_hits'] = dict(self._cache_counter)
        report['coverage_by_mode_doctrine'] = dict(self._coverage_counter)
        report['confidence'] = {
            "avg": statistics.mean(self._confidence_list) if self._confidence_list else None,
            "min": min(self._confidence_list) if self._confidence_list else None,
            "max": max(self._confidence_list) if self._confidence_list else None
        }
        return report

    def export_jsonl(self, path: Union[str, pathlib.Path]) -> int:
        path = pathlib.Path(path)
        count = 0
        with path.open('a', encoding='utf-8') as f:
            for q in list(self.queries)[self._last_export_count:]:
                f.write(json.dumps({
                    "query_id": q.query_id,
                    "engine_id": q.engine_id,
                    "timestamp": q.timestamp,
                    "latency_ms": q.latency_ms,
                    "cache_hit": q.cache_hit,
                    "doctrine_matched": q.doctrine_matched,
                    "mode": q.mode,
                    "confidence": q.confidence,
                    "error": q.error
                }) + '\n')
                count += 1
        self._last_export_count += count
        logger.info(f"Exported {count} queries to {path}")
        return count

class AuditTrailWriter:
    def __init__(self, audit_path: Union[str, pathlib.Path]):
        self.audit_path = pathlib.Path(audit_path)
        self.audit_path.parent.mkdir(parents=True, exist_ok=True)
        self._last_written_query_ids: set = set()

    def write(self, metrics: QueryMetrics):
        if metrics.query_id in self._last_written_query_ids:
            return
        entry = {
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
        with self.audit_path.open('a', encoding='utf-8') as f:
            f.write(json.dumps(entry) + '\n')
        self._last_written_query_ids.add(metrics.query_id)
        logger.debug(f"Audit trail written for query {metrics.query_id}")

COLLECTOR = TelemetryCollector()