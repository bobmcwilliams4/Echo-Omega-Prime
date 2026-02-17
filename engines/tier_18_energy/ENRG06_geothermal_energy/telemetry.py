import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "ENRG06"

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
        self._query_times: deque = deque(maxlen=max_queries)
        self._query_modes: Counter = Counter()
        self._coverage: defaultdict = defaultdict(lambda: {'count': 0, 'confidence_sum': 0.0})
        self._audit_writer = AuditTrailWriter()
        logger.info(f"TelemetryCollector initialized for engine {ENGINE_ID}")

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._query_times.append(metrics.timestamp)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._query_modes[metrics.mode] += 1
        self._coverage[metrics.mode]['count'] += 1
        self._coverage[metrics.mode]['confidence_sum'] += metrics.confidence
        self._audit_writer.write(metrics)
        logger.debug(f"Recorded query: {metrics.query_id}")

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            'error_type': error_type,
            'message': message,
            'query_id': query_id,
            'timestamp': time.time()
        }
        self._errors.append(error_entry)
        logger.error(f"Error recorded: {error_type} for query {query_id}: {message}")

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = [q.latency_ms for q in self._queries if q.latency_ms is not None]
        if not latencies:
            return {'avg': None, 'p50': None, 'p95': None, 'p99': None, 'min': None, 'max': None}
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = latencies_sorted[int(0.95 * len(latencies_sorted)) - 1]
        p99 = latencies_sorted[int(0.99 * len(latencies_sorted)) - 1]
        min_latency = min(latencies)
        max_latency = max(latencies)
        logger.info(f"Latency stats computed: avg={avg}, p50={p50}, p95={p95}, p99={p99}, min={min_latency}, max={max_latency}")
        return {
            'avg': avg,
            'p50': p50,
            'p95': p95,
            'p99': p99,
            'min': min_latency,
            'max': max_latency
        }

    def get_doctrine_hit_rate(self) -> float:
        total = len(self._doctrine_hits)
        if total == 0:
            return 0.0
        hits = sum(1 for hit in self._doctrine_hits if hit)
        hit_rate = hits / total
        logger.info(f"Doctrine hit rate: {hit_rate} ({hits}/{total})")
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self._errors if e['timestamp'] >= window_start]
        queries_in_window = [q for q in self._queries if q.timestamp >= window_start]
        num_queries = len(queries_in_window)
        num_errors = len(errors_in_window)
        if num_queries == 0:
            return 0.0
        error_rate = num_errors / num_queries
        logger.info(f"Error rate in last {window_hours} hours: {error_rate} ({num_errors}/{num_queries})")
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for t in self._query_times if t >= one_hour_ago)
        logger.info(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {}
        for mode, data in self._coverage.items():
            count = data['count']
            confidence_sum = data['confidence_sum']
            avg_confidence = confidence_sum / count if count > 0 else 0.0
            report[mode] = {
                'count': count,
                'avg_confidence': avg_confidence
            }
        logger.info(f"Coverage report generated: {report}")
        return report

    def export_jsonl(self, path: str) -> int:
        p = pathlib.Path(path)
        exported = 0
        with p.open('w', encoding='utf-8') as f:
            for q in self._queries:
                f.write(json.dumps(asdict(q)) + '\n')
                exported += 1
        logger.info(f"Exported {exported} queries to {path}")
        return exported

class AuditTrailWriter:
    def __init__(self, audit_dir: str = "./audit_trail"):
        self.audit_dir = pathlib.Path(audit_dir)
        self.audit_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"AuditTrailWriter initialized at {self.audit_dir}")

    def write(self, metrics: QueryMetrics):
        audit_path = self.audit_dir / f"{metrics.query_id}.jsonl"
        with audit_path.open('a', encoding='utf-8') as f:
            f.write(json.dumps(asdict(metrics)) + '\n')
        logger.debug(f"Audit trail written for query {metrics.query_id}")

COLLECTOR = TelemetryCollector()