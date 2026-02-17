import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Union
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "RAIL01"

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
    def __init__(self, engine_id: str):
        self.engine_id = engine_id
        self._queries: deque = deque(maxlen=10000)
        self._errors: deque = deque(maxlen=10000)
        self._doctrine_hits: deque = deque(maxlen=10000)
        self._latencies: deque = deque(maxlen=10000)
        self._cache_hits: deque = deque(maxlen=10000)
        self._coverage: defaultdict = defaultdict(lambda: {'count': 0, 'doctrine_matched': 0, 'cache_hit': 0, 'errors': 0})
        self._audit_writer = AuditTrailWriter()
        self._query_counter: Counter = Counter()
        self._error_counter: Counter = Counter()
        self._last_query_time: deque = deque(maxlen=10000)
        self._query_metrics_by_id: Dict[str, QueryMetrics] = {}
        logger.info(f"TelemetryCollector initialized for engine_id={engine_id}")

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._latencies.append(metrics.latency_ms)
        self._cache_hits.append(metrics.cache_hit)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._last_query_time.append(metrics.timestamp)
        self._coverage[metrics.mode]['count'] += 1
        if metrics.doctrine_matched:
            self._coverage[metrics.mode]['doctrine_matched'] += 1
        if metrics.cache_hit:
            self._coverage[metrics.mode]['cache_hit'] += 1
        if metrics.error:
            self._coverage[metrics.mode]['errors'] += 1
        self._query_counter[metrics.mode] += 1
        self._query_metrics_by_id[metrics.query_id] = metrics
        self._audit_writer.write(metrics)
        logger.debug(f"Recorded query: {metrics}")

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "error_type": error_type,
            "message": message,
            "timestamp": time.time(),
            "engine_id": self.engine_id,
            "query_id": query_id
        }
        self._errors.append(error_entry)
        self._error_counter[error_type] += 1
        logger.error(f"Recorded error: {error_entry}")

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
        total = len(self._doctrine_hits)
        if total == 0:
            return 0.0
        hits = sum(1 for hit in self._doctrine_hits if hit)
        hit_rate = hits / total
        logger.debug(f"Doctrine hit rate: {hit_rate} ({hits}/{total})")
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_seconds = window_hours * 3600
        errors_in_window = [e for e in self._errors if now - e["timestamp"] <= window_seconds]
        queries_in_window = [q for q in self._queries if now - q.timestamp <= window_seconds]
        total_queries = len(queries_in_window)
        total_errors = len(errors_in_window)
        if total_queries == 0:
            return 0.0
        error_rate = total_errors / total_queries
        logger.debug(f"Error rate: {error_rate} ({total_errors}/{total_queries}) in last {window_hours} hours")
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= one_hour_ago)
        logger.debug(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {}
        for mode, stats in self._coverage.items():
            count = stats['count']
            doctrine_matched = stats['doctrine_matched']
            cache_hit = stats['cache_hit']
            errors = stats['errors']
            doctrine_rate = doctrine_matched / count if count else 0.0
            cache_rate = cache_hit / count if count else 0.0
            error_rate = errors / count if count else 0.0
            report[mode] = {
                "count": count,
                "doctrine_matched": doctrine_matched,
                "cache_hit": cache_hit,
                "errors": errors,
                "doctrine_rate": doctrine_rate,
                "cache_rate": cache_rate,
                "error_rate": error_rate
            }
        logger.debug(f"Coverage report: {report}")
        return report

    def export_jsonl(self, path: Union[str, pathlib.Path]) -> int:
        path = pathlib.Path(path)
        count = 0
        with path.open('w', encoding='utf-8') as f:
            for metrics in self._queries:
                data = {
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
                f.write(json.dumps(data) + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {path}")
        return count

class AuditTrailWriter:
    def __init__(self, audit_dir: Optional[Union[str, pathlib.Path]] = None):
        if audit_dir is None:
            audit_dir = pathlib.Path("./audit_trail")
        self.audit_dir = pathlib.Path(audit_dir)
        self.audit_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"AuditTrailWriter initialized at {self.audit_dir}")

    def write(self, metrics: QueryMetrics):
        filename = self._get_filename(metrics)
        filepath = self.audit_dir / filename
        data = {
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
        with filepath.open('a', encoding='utf-8') as f:
            f.write(json.dumps(data) + "\n")
        logger.debug(f"Wrote audit trail for query_id={metrics.query_id} to {filepath}")

    def _get_filename(self, metrics: QueryMetrics) -> str:
        date_str = time.strftime("%Y%m%d", time.localtime(metrics.timestamp))
        hash_id = hashlib.sha256(metrics.query_id.encode()).hexdigest()[:8]
        filename = f"{date_str}_{metrics.engine_id}_{hash_id}.jsonl"
        return filename

COLLECTOR = TelemetryCollector(engine_id=ENGINE_ID)