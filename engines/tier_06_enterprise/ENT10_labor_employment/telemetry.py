import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any, Union
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "ENT10"

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
        self._doctrine_hits: deque = deque(maxlen=maxlen)
        self._latencies: deque = deque(maxlen=maxlen)
        self._query_id_map: Dict[str, QueryMetrics] = {}
        self._audit_writer = AuditTrailWriter()
        self._coverage_counter: Counter = Counter()
        self._mode_counter: Counter = Counter()
        self._confidence_values: deque = deque(maxlen=maxlen)
        self._cache_hits: deque = deque(maxlen=maxlen)
        self._doctrine_matched: deque = deque(maxlen=maxlen)
        self._error_types: Counter = Counter()
        self._error_timestamps: deque = deque(maxlen=maxlen)
        self._last_exported_idx: int = 0

    def record_query(self, metrics: QueryMetrics):
        logger.debug(f"Recording query: {metrics.query_id}")
        self._queries.append(metrics)
        self._query_id_map[metrics.query_id] = metrics
        self._latencies.append(metrics.latency_ms)
        self._cache_hits.append(metrics.cache_hit)
        self._doctrine_matched.append(metrics.doctrine_matched)
        self._mode_counter[metrics.mode] += 1
        self._confidence_values.append(metrics.confidence)
        self._coverage_counter['total'] += 1
        if metrics.doctrine_matched:
            self._coverage_counter['doctrine_matched'] += 1
        if metrics.cache_hit:
            self._coverage_counter['cache_hit'] += 1
        if metrics.error:
            self.record_error('query_error', metrics.error, metrics.query_id)
        self._audit_writer.write(metrics)
        logger.info(f"Query recorded: {metrics.query_id}")

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
        self._error_timestamps.append(error_entry["timestamp"])
        logger.error(f"Error recorded: {error_type} for query {query_id}: {message}")

    def get_latency_stats(self) -> Dict[str, Union[float, None]]:
        latencies = list(self._latencies)
        if not latencies:
            return dict(avg=None, p50=None, p95=None, p99=None, min=None, max=None)
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        min_latency = min(latencies)
        max_latency = max(latencies)
        p50 = statistics.median(latencies)
        p95 = latencies_sorted[int(len(latencies_sorted) * 0.95) - 1]
        p99 = latencies_sorted[int(len(latencies_sorted) * 0.99) - 1]
        logger.debug(f"Latency stats: avg={avg}, p50={p50}, p95={p95}, p99={p99}, min={min_latency}, max={max_latency}")
        return dict(avg=avg, p50=p50, p95=p95, p99=p99, min=min_latency, max=max_latency)

    def get_doctrine_hit_rate(self) -> float:
        total = len(self._doctrine_matched)
        if total == 0:
            return 0.0
        hits = sum(1 for matched in self._doctrine_matched if matched)
        hit_rate = hits / total
        logger.debug(f"Doctrine hit rate: {hit_rate} ({hits}/{total})")
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [ts for ts in self._error_timestamps if ts >= window_start]
        queries_in_window = [q for q in self._queries if q.timestamp >= window_start]
        num_queries = len(queries_in_window)
        num_errors = len(errors_in_window)
        if num_queries == 0:
            return 0.0
        error_rate = num_errors / num_queries
        logger.debug(f"Error rate (last {window_hours}h): {error_rate} ({num_errors}/{num_queries})")
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= one_hour_ago)
        logger.debug(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        total = self._coverage_counter['total']
        doctrine_matched = self._coverage_counter['doctrine_matched']
        cache_hit = self._coverage_counter['cache_hit']
        doctrine_rate = doctrine_matched / total if total else 0.0
        cache_hit_rate = cache_hit / total if total else 0.0
        mode_stats = dict(self._mode_counter)
        confidence_stats = {
            "avg": statistics.mean(self._confidence_values) if self._confidence_values else None,
            "min": min(self._confidence_values) if self._confidence_values else None,
            "max": max(self._confidence_values) if self._confidence_values else None,
            "p50": statistics.median(self._confidence_values) if self._confidence_values else None
        }
        report = {
            "total_queries": total,
            "doctrine_matched": doctrine_matched,
            "cache_hit": cache_hit,
            "doctrine_rate": doctrine_rate,
            "cache_hit_rate": cache_hit_rate,
            "mode_stats": mode_stats,
            "confidence_stats": confidence_stats,
            "error_types": dict(self._error_types)
        }
        logger.debug(f"Coverage report: {report}")
        return report

    def export_jsonl(self, path: Union[str, pathlib.Path]) -> int:
        path = pathlib.Path(path)
        count = 0
        with path.open("a", encoding="utf-8") as f:
            for idx, q in enumerate(list(self._queries)[self._last_exported_idx:]):
                f.write(json.dumps(asdict(q)) + "\n")
                count += 1
            self._last_exported_idx += count
        logger.info(f"Exported {count} queries to {path}")
        return count

class AuditTrailWriter:
    def __init__(self, base_path: Optional[Union[str, pathlib.Path]] = None):
        if base_path is None:
            base_path = pathlib.Path("./audit_trails")
        self.base_path = pathlib.Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def _get_audit_path(self, query_id: str) -> pathlib.Path:
        hash_digest = hashlib.sha256(query_id.encode()).hexdigest()
        subdir = hash_digest[:2]
        dir_path = self.base_path / subdir
        dir_path.mkdir(parents=True, exist_ok=True)
        file_path = dir_path / f"{query_id}.jsonl"
        return file_path

    def write(self, metrics: QueryMetrics):
        path = self._get_audit_path(metrics.query_id)
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(metrics)) + "\n")
        logger.debug(f"Audit trail written for query {metrics.query_id} at {path}")

COLLECTOR = TelemetryCollector()