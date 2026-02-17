import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Union
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "ENRG10"

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
        self._coverage: Dict[str, set] = defaultdict(set)
        self._last_exported: float = 0.0

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._query_index[metrics.query_id] = metrics
        self._doctrine_counter.update([metrics.doctrine_matched])
        self._cache_counter.update([metrics.cache_hit])
        self._mode_counter.update([metrics.mode])
        self._confidence_values.append(metrics.confidence)
        self._coverage[metrics.mode].add(metrics.query_id)
        logger.info(f"Recorded query {metrics.query_id} (latency={metrics.latency_ms}ms, cache_hit={metrics.cache_hit}, doctrine_matched={metrics.doctrine_matched}, confidence={metrics.confidence})")

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "error_type": error_type,
            "message": message,
            "query_id": query_id
        }
        self._errors.append(error_entry)
        self._error_types.update([error_type])
        logger.error(f"Error recorded: {error_type} for query {query_id}: {message}")

    def get_latency_stats(self) -> Dict[str, Union[float, None]]:
        latencies = [q.latency_ms for q in self._queries if q.latency_ms is not None]
        if not latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = latencies_sorted[int(0.95 * len(latencies_sorted)) - 1]
        p99 = latencies_sorted[int(0.99 * len(latencies_sorted)) - 1]
        min_latency = latencies_sorted[0]
        max_latency = latencies_sorted[-1]
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
        hits = self._doctrine_counter[True]
        return hits / total if total > 0 else 0.0

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        error_count = sum(1 for e in self._errors if e["timestamp"] >= window_start)
        query_count = sum(1 for q in self._queries if q.timestamp >= window_start)
        return error_count / query_count if query_count > 0 else 0.0

    def queries_last_hour(self) -> int:
        now = time.time()
        window_start = now - 3600
        return sum(1 for q in self._queries if q.timestamp >= window_start)

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {}
        for mode, queries in self._coverage.items():
            report[mode] = {
                "unique_queries": len(queries),
                "total_queries": sum(1 for q in self._queries if q.mode == mode)
            }
        return report

    def export_jsonl(self, path: Union[str, pathlib.Path]) -> int:
        path = pathlib.Path(path)
        count = 0
        with path.open("a", encoding="utf-8") as f:
            for q in self._queries:
                d = {
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
                f.write(json.dumps(d) + "\n")
                count += 1
        self._last_exported = time.time()
        logger.info(f"Exported {count} queries to {path}")
        return count

    def get_error_details(self) -> List[Dict[str, Any]]:
        return list(self._errors)

    def get_mode_distribution(self) -> Dict[str, int]:
        return dict(self._mode_counter)

    def get_cache_hit_rate(self) -> float:
        total = sum(self._cache_counter.values())
        hits = self._cache_counter[True]
        return hits / total if total > 0 else 0.0

    def get_confidence_stats(self) -> Dict[str, Union[float, None]]:
        values = self._confidence_values
        if not values:
            return {"avg": None, "min": None, "max": None}
        return {
            "avg": statistics.mean(values),
            "min": min(values),
            "max": max(values)
        }

    def get_last_exported(self) -> float:
        return self._last_exported

    def get_query_by_id(self, query_id: str) -> Optional[QueryMetrics]:
        return self._query_index.get(query_id)

class AuditTrailWriter:
    def __init__(self, audit_path: Union[str, pathlib.Path]):
        self.audit_path = pathlib.Path(audit_path)
        self.audit_path.parent.mkdir(parents=True, exist_ok=True)

    def write(self, query_metrics: QueryMetrics, extra: Optional[Dict[str, Any]] = None):
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
        if extra:
            entry.update(extra)
        with self.audit_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        logger.debug(f"Audit trail written for query {query_metrics.query_id}")

COLLECTOR = TelemetryCollector()