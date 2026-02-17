import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Tuple
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "ET06"

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
        self._modes: deque = deque(maxlen=max_queries)
        self._coverage: defaultdict = defaultdict(lambda: {'count': 0, 'confidence': []})
        self._query_id_index: Dict[str, QueryMetrics] = {}
        self._audit_writer = AuditTrailWriter()
        logger.info(f"TelemetryCollector initialized for engine {ENGINE_ID}")

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._query_id_index[metrics.query_id] = metrics
        self._latencies.append(metrics.latency_ms)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._modes.append(metrics.mode)
        self._coverage[metrics.mode]['count'] += 1
        self._coverage[metrics.mode]['confidence'].append(metrics.confidence)
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
        logger.warning(f"Recorded error: {error_type} for query_id={query_id}")

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = [q.latency_ms for q in self._queries if q.latency_ms is not None]
        if not latencies:
            return {'avg': None, 'p50': None, 'p95': None, 'p99': None, 'min': None, 'max': None}
        latencies_sorted = sorted(latencies)
        stats = {
            'avg': statistics.mean(latencies),
            'p50': statistics.median(latencies),
            'p95': latencies_sorted[int(0.95 * len(latencies_sorted)) - 1],
            'p99': latencies_sorted[int(0.99 * len(latencies_sorted)) - 1],
            'min': min(latencies),
            'max': max(latencies)
        }
        logger.info(f"Latency stats: {stats}")
        return stats

    def get_doctrine_hit_rate(self) -> float:
        total = len(self._doctrine_hits)
        if total == 0:
            return 0.0
        hits = sum(1 for hit in self._doctrine_hits if hit)
        rate = hits / total
        logger.info(f"Doctrine hit rate: {rate}")
        return rate

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
        logger.info(f"Error rate in last {window_hours}h: {error_rate}")
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
            count = data['count']
            confidences = data['confidence']
            avg_conf = statistics.mean(confidences) if confidences else None
            report[mode] = {
                'count': count,
                'avg_confidence': avg_conf,
                'min_confidence': min(confidences) if confidences else None,
                'max_confidence': max(confidences) if confidences else None
            }
        logger.info(f"Coverage report: {report}")
        return report

    def export_jsonl(self, path: str) -> int:
        p = pathlib.Path(path)
        count = 0
        with p.open('w', encoding='utf-8') as f:
            for q in self._queries:
                f.write(json.dumps(dataclasses.asdict(q)) + '\n')
                count += 1
        logger.info(f"Exported {count} queries to {path}")
        return count

class AuditTrailWriter:
    def __init__(self, base_path: str = "./audit_trail"):
        self.base_path = pathlib.Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"AuditTrailWriter initialized at {self.base_path}")

    def _get_file_path(self, query_id: str) -> pathlib.Path:
        hash_digest = hashlib.sha256(query_id.encode('utf-8')).hexdigest()
        filename = f"{ENGINE_ID}_{hash_digest}.jsonl"
        return self.base_path / filename

    def write(self, metrics: QueryMetrics):
        file_path = self._get_file_path(metrics.query_id)
        with file_path.open('a', encoding='utf-8') as f:
            f.write(json.dumps(dataclasses.asdict(metrics)) + '\n')
        logger.debug(f"Wrote audit trail for query_id={metrics.query_id} to {file_path}")

COLLECTOR = TelemetryCollector()