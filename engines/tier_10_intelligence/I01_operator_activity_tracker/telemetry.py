import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any, Tuple
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "I01"

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
        self._queries: deque = deque(maxlen=max_queries)
        self._errors: deque = deque(maxlen=max_queries)
        self._doctrine_hits: deque = deque(maxlen=max_queries)
        self._latencies: deque = deque(maxlen=max_queries)
        self._query_ids: set = set()
        self._mode_counter: Counter = Counter()
        self._confidence_values: deque = deque(maxlen=max_queries)
        self._cache_hits: deque = deque(maxlen=max_queries)
        self._coverage: defaultdict = defaultdict(lambda: {'matched': 0, 'total': 0})
        self._audit_writer = AuditTrailWriter()
        logger.info("TelemetryCollector initialized for ENGINE_ID={}".format(ENGINE_ID))

    def record_query(self, metrics: QueryMetrics):
        if metrics.query_id in self._query_ids:
            logger.warning(f"Duplicate query_id detected: {metrics.query_id}")
            return
        self._queries.append(metrics)
        self._query_ids.add(metrics.query_id)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._mode_counter[metrics.mode] += 1
        self._confidence_values.append(metrics.confidence)
        self._cache_hits.append(metrics.cache_hit)
        self._coverage[metrics.mode]['total'] += 1
        if metrics.doctrine_matched:
            self._coverage[metrics.mode]['matched'] += 1
        self._audit_writer.write(metrics)
        logger.debug(f"Recorded query: {metrics.query_id}")

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            'timestamp': time.time(),
            'error_type': error_type,
            'message': message,
            'query_id': query_id
        }
        self._errors.append(error_entry)
        logger.error(f"Error recorded: {error_type} - {message} (query_id={query_id})")

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = list(self._latencies)
        if not latencies:
            return {'avg': None, 'p50': None, 'p95': None, 'p99': None, 'min': None, 'max': None}
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        latencies_sorted = sorted(latencies)
        n = len(latencies_sorted)
        def percentile(p):
            idx = int(p * n)
            idx = min(idx, n - 1)
            return latencies_sorted[idx]
        p95 = percentile(0.95)
        p99 = percentile(0.99)
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
        errors_in_window = [e for e in self._errors if e['timestamp'] >= window_start]
        queries_in_window = [q for q in self._queries if q.timestamp >= window_start]
        total_queries = len(queries_in_window)
        total_errors = len(errors_in_window)
        if total_queries == 0:
            return 0.0
        error_rate = total_errors / total_queries
        logger.info(f"Error rate in last {window_hours} hours: {error_rate:.4f}")
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= hour_ago)
        logger.info(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {}
        for mode, data in self._coverage.items():
            total = data['total']
            matched = data['matched']
            coverage = matched / total if total > 0 else 0.0
            report[mode] = {
                'total': total,
                'matched': matched,
                'coverage': coverage
            }
        logger.info(f"Coverage report: {report}")
        return report

    def export_jsonl(self, path: str) -> int:
        p = pathlib.Path(path)
        count = 0
        with p.open('w', encoding='utf-8') as f:
            for q in self._queries:
                f.write(json.dumps(asdict(q)) + '\n')
                count += 1
        logger.info(f"Exported {count} queries to {path}")
        return count

class AuditTrailWriter:
    def __init__(self, base_dir: str = "./audit_trails"):
        self.base_dir = pathlib.Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"AuditTrailWriter initialized at {self.base_dir}")

    def write(self, metrics: QueryMetrics):
        query_hash = hashlib.sha256(metrics.query_id.encode()).hexdigest()
        filename = f"{ENGINE_ID}_{query_hash}.jsonl"
        file_path = self.base_dir / filename
        with file_path.open('a', encoding='utf-8') as f:
            f.write(json.dumps(asdict(metrics)) + '\n')
        logger.debug(f"Audit trail written for query_id={metrics.query_id}")

COLLECTOR = TelemetryCollector()