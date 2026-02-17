import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any, Union
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "MECH07"

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
    def __init__(self, maxlen: int = 100_000):
        self._queries = deque(maxlen=maxlen)
        self._errors = deque(maxlen=maxlen)
        self._doctrine_hits = deque(maxlen=maxlen)
        self._latencies = deque(maxlen=maxlen)
        self._coverage = defaultdict(lambda: {'count': 0, 'doctrine_matched': 0, 'cache_hit': 0})
        self._query_id_set = set()
        self._query_modes = Counter()
        self._query_confidences = []
        self._audit_writer = AuditTrailWriter()
        logger.info("TelemetryCollector initialized with maxlen={}", maxlen)

    def record_query(self, metrics: QueryMetrics):
        if metrics.query_id in self._query_id_set:
            logger.warning("Duplicate query_id detected: {}", metrics.query_id)
            return
        self._queries.append(metrics)
        self._query_id_set.add(metrics.query_id)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._query_modes[metrics.mode] += 1
        self._query_confidences.append(metrics.confidence)
        self._coverage[metrics.mode]['count'] += 1
        if metrics.doctrine_matched:
            self._coverage[metrics.mode]['doctrine_matched'] += 1
        if metrics.cache_hit:
            self._coverage[metrics.mode]['cache_hit'] += 1
        if metrics.error:
            self._errors.append({
                'timestamp': metrics.timestamp,
                'query_id': metrics.query_id,
                'error': metrics.error,
                'engine_id': metrics.engine_id
            })
        self._audit_writer.write(metrics)
        logger.debug("Recorded query: {}", metrics)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        ts = time.time()
        error_entry = {
            'timestamp': ts,
            'error_type': error_type,
            'message': message,
            'query_id': query_id,
            'engine_id': ENGINE_ID
        }
        self._errors.append(error_entry)
        logger.error("Error recorded: {}", error_entry)

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = list(self._latencies)
        if not latencies:
            return {'avg': None, 'p50': None, 'p95': None, 'p99': None, 'min': None, 'max': None}
        lat_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = lat_sorted[int(0.95 * len(lat_sorted)) - 1]
        p99 = lat_sorted[int(0.99 * len(lat_sorted)) - 1]
        min_v = lat_sorted[0]
        max_v = lat_sorted[-1]
        stats = {
            'avg': avg,
            'p50': p50,
            'p95': p95,
            'p99': p99,
            'min': min_v,
            'max': max_v
        }
        logger.debug("Latency stats: {}", stats)
        return stats

    def get_doctrine_hit_rate(self) -> float:
        if not self._doctrine_hits:
            return 0.0
        hit_rate = sum(self._doctrine_hits) / len(self._doctrine_hits)
        logger.debug("Doctrine hit rate: {}", hit_rate)
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        error_count = 0
        query_count = 0
        for q in self._queries:
            if q.timestamp >= window_start:
                query_count += 1
                if q.error:
                    error_count += 1
        if query_count == 0:
            return 0.0
        error_rate = error_count / query_count
        logger.debug("Error rate in last {} hours: {}", window_hours, error_rate)
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= one_hour_ago)
        logger.debug("Queries in last hour: {}", count)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {}
        for mode, stats in self._coverage.items():
            count = stats['count']
            doctrine_matched = stats['doctrine_matched']
            cache_hit = stats['cache_hit']
            report[mode] = {
                'count': count,
                'doctrine_matched': doctrine_matched,
                'cache_hit': cache_hit,
                'doctrine_match_rate': doctrine_matched / count if count else 0.0,
                'cache_hit_rate': cache_hit / count if count else 0.0
            }
        logger.debug("Coverage report: {}", report)
        return report

    def export_jsonl(self, path: Union[str, pathlib.Path]) -> int:
        path = pathlib.Path(path)
        count = 0
        with path.open('w', encoding='utf-8') as f:
            for q in self._queries:
                d = asdict(q)
                f.write(json.dumps(d) + '\n')
                count += 1
        logger.info("Exported {} queries to {}", count, path)
        return count

class AuditTrailWriter:
    def __init__(self, audit_dir: Union[str, pathlib.Path] = "./audit_trail"):
        self.audit_dir = pathlib.Path(audit_dir)
        self.audit_dir.mkdir(parents=True, exist_ok=True)
        logger.info("AuditTrailWriter initialized at {}", self.audit_dir)

    def _get_audit_path(self, query_id: str) -> pathlib.Path:
        h = hashlib.sha1(query_id.encode('utf-8')).hexdigest()
        subdir = self.audit_dir / h[:2]
        subdir.mkdir(parents=True, exist_ok=True)
        return subdir / f"{query_id}.jsonl"

    def write(self, metrics: QueryMetrics):
        path = self._get_audit_path(metrics.query_id)
        with path.open('a', encoding='utf-8') as f:
            f.write(json.dumps(asdict(metrics)) + '\n')
        logger.debug("Audit written for query_id {} at {}", metrics.query_id, path)

COLLECTOR = TelemetryCollector()