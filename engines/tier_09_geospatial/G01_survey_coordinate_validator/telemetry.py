import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any, Union
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "G01"

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
        self._latencies: deque = deque(maxlen=max_queries)
        self._query_ids: set = set()
        self._audit_writer = AuditTrailWriter()
        self._coverage_counter: Counter = Counter()
        self._mode_counter: Counter = Counter()
        self._confidence_values: deque = deque(maxlen=max_queries)
        self._cache_hits: deque = deque(maxlen=max_queries)
        self._doctrine_matched: deque = deque(maxlen=max_queries)
        self._timestamps: deque = deque(maxlen=max_queries)
        self._query_metrics: deque = deque(maxlen=max_queries)
        self._error_types: Counter = Counter()
        self._error_timestamps: deque = deque(maxlen=max_queries)

    def record_query(self, metrics: QueryMetrics):
        if metrics.query_id in self._query_ids:
            logger.warning(f"Duplicate query_id detected: {metrics.query_id}")
            return
        self._queries.append(metrics)
        self._query_ids.add(metrics.query_id)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._cache_hits.append(metrics.cache_hit)
        self._doctrine_matched.append(metrics.doctrine_matched)
        self._timestamps.append(metrics.timestamp)
        self._query_metrics.append(metrics)
        self._mode_counter[metrics.mode] += 1
        self._confidence_values.append(metrics.confidence)
        self._coverage_counter[metrics.engine_id] += 1
        self._audit_writer.write(metrics)
        if metrics.error:
            self.record_error("query_error", metrics.error, metrics.query_id)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "timestamp": time.time()
        }
        self._errors.append(error_entry)
        self._error_types[error_type] += 1
        self._error_timestamps.append(error_entry["timestamp"])
        logger.error(f"Error recorded: {error_entry}")

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = list(self._latencies)
        if not latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = latencies_sorted[int(0.95 * len(latencies_sorted)) - 1]
        p99 = latencies_sorted[int(0.99 * len(latencies_sorted)) - 1]
        min_latency = min(latencies)
        max_latency = max(latencies)
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
        return hits / total

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        error_count = sum(1 for ts in self._error_timestamps if ts >= window_start)
        query_count = sum(1 for ts in self._timestamps if ts >= window_start)
        if query_count == 0:
            return 0.0
        return error_count / query_count

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        return sum(1 for ts in self._timestamps if ts >= one_hour_ago)

    def get_coverage_report(self) -> Dict[str, Any]:
        total_queries = len(self._queries)
        mode_counts = dict(self._mode_counter)
        confidence_stats = self._get_confidence_stats()
        cache_hit_rate = self._get_cache_hit_rate()
        doctrine_hit_rate = self.get_doctrine_hit_rate()
        error_rate = self.get_error_rate(1.0)
        return {
            "engine_id": ENGINE_ID,
            "total_queries": total_queries,
            "mode_counts": mode_counts,
            "confidence_stats": confidence_stats,
            "cache_hit_rate": cache_hit_rate,
            "doctrine_hit_rate": doctrine_hit_rate,
            "error_rate_last_hour": error_rate,
            "coverage_counter": dict(self._coverage_counter)
        }

    def _get_confidence_stats(self) -> Dict[str, Any]:
        values = list(self._confidence_values)
        if not values:
            return {"avg": None, "min": None, "max": None, "p50": None}
        avg = statistics.mean(values)
        min_val = min(values)
        max_val = max(values)
        p50 = statistics.median(values)
        return {"avg": avg, "min": min_val, "max": max_val, "p50": p50}

    def _get_cache_hit_rate(self) -> float:
        total = len(self._cache_hits)
        if total == 0:
            return 0.0
        hits = sum(1 for hit in self._cache_hits if hit)
        return hits / total

    def export_jsonl(self, path: Union[str, pathlib.Path]) -> int:
        path = pathlib.Path(path)
        count = 0
        with path.open("w", encoding="utf-8") as f:
            for metrics in self._query_metrics:
                f.write(json.dumps(asdict(metrics)) + "\n")
                count += 1
        logger.info(f"Exported {count} query metrics to {path}")
        return count

class AuditTrailWriter:
    def __init__(self, base_dir: Union[str, pathlib.Path] = "audit_trail"):
        self.base_dir = pathlib.Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def write(self, metrics: QueryMetrics):
        query_hash = hashlib.sha256(metrics.query_id.encode()).hexdigest()
        filename = f"{ENGINE_ID}_{query_hash}.jsonl"
        file_path = self.base_dir / filename
        entry = asdict(metrics)
        entry["audit_timestamp"] = time.time()
        with file_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        logger.debug(f"Audit trail written for query_id={metrics.query_id}")

COLLECTOR = TelemetryCollector()