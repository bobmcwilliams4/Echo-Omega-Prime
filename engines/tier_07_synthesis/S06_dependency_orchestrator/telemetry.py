import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "S06"

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
        self._errors: deque = deque(maxlen=5000)
        self._audit_trail: deque = deque(maxlen=10000)
        self._doctrine_hits: deque = deque(maxlen=10000)
        self._cache_hits: deque = deque(maxlen=10000)
        self._latencies: deque = deque(maxlen=10000)
        self._coverage: defaultdict = defaultdict(lambda: {'count': 0, 'doctrine_matched': 0})
        self._query_ids: set = set()
        self._last_export_time: float = time.time()
        logger.info(f"TelemetryCollector initialized for engine_id={engine_id}")

    def record_query(self, metrics: QueryMetrics):
        logger.debug(f"Recording query: {metrics}")
        self._queries.append(metrics)
        self._audit_trail.append(metrics)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._cache_hits.append(metrics.cache_hit)
        self._coverage[metrics.mode]['count'] += 1
        if metrics.doctrine_matched:
            self._coverage[metrics.mode]['doctrine_matched'] += 1
        self._query_ids.add(metrics.query_id)
        if metrics.error:
            self.record_error(metrics.error, "QueryError", metrics.query_id)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            'timestamp': time.time(),
            'engine_id': self.engine_id,
            'error_type': error_type,
            'message': message,
            'query_id': query_id
        }
        logger.error(f"Recording error: {error_entry}")
        self._errors.append(error_entry)

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = list(self._latencies)
        if not latencies:
            logger.warning("No latencies recorded.")
            return {
                'avg': None, 'p50': None, 'p95': None, 'p99': None,
                'min': None, 'max': None
            }
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = latencies_sorted[int(0.95 * len(latencies_sorted)) - 1]
        p99 = latencies_sorted[int(0.99 * len(latencies_sorted)) - 1]
        min_latency = latencies_sorted[0]
        max_latency = latencies_sorted[-1]
        stats = {
            'avg': avg,
            'p50': p50,
            'p95': p95,
            'p99': p99,
            'min': min_latency,
            'max': max_latency
        }
        logger.info(f"Latency stats: {stats}")
        return stats

    def get_doctrine_hit_rate(self) -> float:
        hits = list(self._doctrine_hits)
        if not hits:
            logger.warning("No doctrine hits recorded.")
            return 0.0
        hit_rate = sum(hits) / len(hits)
        logger.info(f"Doctrine hit rate: {hit_rate}")
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        error_count = sum(1 for e in self._errors if e['timestamp'] >= window_start)
        query_count = sum(1 for q in self._queries if q.timestamp >= window_start)
        if query_count == 0:
            logger.warning("No queries in error rate window.")
            return 0.0
        error_rate = error_count / query_count
        logger.info(f"Error rate (window_hours={window_hours}): {error_rate}")
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= one_hour_ago)
        logger.info(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {}
        for mode, data in self._coverage.items():
            total = data['count']
            doctrine_matched = data['doctrine_matched']
            doctrine_rate = doctrine_matched / total if total > 0 else 0.0
            report[mode] = {
                'total_queries': total,
                'doctrine_matched': doctrine_matched,
                'doctrine_rate': doctrine_rate
            }
        logger.info(f"Coverage report: {report}")
        return report

    def export_jsonl(self, path: str) -> int:
        export_path = pathlib.Path(path)
        export_path.parent.mkdir(parents=True, exist_ok=True)
        count = 0
        with export_path.open('a', encoding='utf-8') as f:
            for metrics in self._audit_trail:
                f.write(json.dumps(dataclasses.asdict(metrics)) + '\n')
                count += 1
        logger.info(f"Exported {count} queries to {path}")
        self._audit_trail.clear()
        self._last_export_time = time.time()
        return count

class AuditTrailWriter:
    def __init__(self, path: str):
        self.path = pathlib.Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._buffer: deque = deque(maxlen=10000)
        logger.info(f"AuditTrailWriter initialized at {self.path}")

    def write(self, metrics: QueryMetrics):
        entry = dataclasses.asdict(metrics)
        self._buffer.append(entry)
        logger.debug(f"Audit trail buffered: {entry}")

    def flush(self):
        count = 0
        with self.path.open('a', encoding='utf-8') as f:
            while self._buffer:
                entry = self._buffer.popleft()
                f.write(json.dumps(entry) + '\n')
                count += 1
        logger.info(f"Flushed {count} audit trail entries to {self.path}")
        return count

COLLECTOR = TelemetryCollector(engine_id=ENGINE_ID)