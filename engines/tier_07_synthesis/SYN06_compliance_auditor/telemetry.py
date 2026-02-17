import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "SYN06"

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
        self._queries = deque(maxlen=maxlen)
        self._errors = deque(maxlen=maxlen)
        self._doctrine_matches = deque(maxlen=maxlen)
        self._latencies = deque(maxlen=maxlen)
        self._cache_hits = deque(maxlen=maxlen)
        self._query_times = deque(maxlen=maxlen)
        self._query_ids = set()
        self._mode_counter = Counter()
        self._confidence_scores = []
        self._coverage_map = defaultdict(lambda: {'count': 0, 'doctrine_matched': 0})
        self._audit_writer = AuditTrailWriter()
        logger.info("TelemetryCollector initialized with maxlen={}", maxlen)

    def record_query(self, metrics: QueryMetrics):
        if metrics.query_id in self._query_ids:
            logger.warning("Duplicate query_id detected: {}", metrics.query_id)
            return
        self._queries.append(metrics)
        self._query_ids.add(metrics.query_id)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_matches.append(metrics.doctrine_matched)
        self._cache_hits.append(metrics.cache_hit)
        self._query_times.append(metrics.timestamp)
        self._mode_counter[metrics.mode] += 1
        self._confidence_scores.append(metrics.confidence)
        self._coverage_map[metrics.mode]['count'] += 1
        if metrics.doctrine_matched:
            self._coverage_map[metrics.mode]['doctrine_matched'] += 1
        if metrics.error:
            self.record_error(metrics.error, "Query error", metrics.query_id)
        self._audit_writer.write(metrics)
        logger.debug("Recorded query: {}", metrics)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            'timestamp': time.time(),
            'error_type': error_type,
            'message': message,
            'query_id': query_id
        }
        self._errors.append(error_entry)
        logger.error("Error recorded: {}", error_entry)

    def get_latency_stats(self) -> Dict[str, float]:
        latencies = list(self._latencies)
        if not latencies:
            return {'avg': 0.0, 'p50': 0.0, 'p95': 0.0, 'p99': 0.0, 'min': 0.0, 'max': 0.0}
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
        logger.debug("Latency stats: {}", stats)
        return stats

    def get_doctrine_hit_rate(self) -> float:
        matches = list(self._doctrine_matches)
        if not matches:
            return 0.0
        hit_rate = sum(matches) / len(matches)
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
        error_rate = (error_count / query_count) if query_count else 0.0
        logger.debug("Error rate (window_hours={}): {}", window_hours, error_rate)
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = 0
        for t in reversed(self._query_times):
            if t >= one_hour_ago:
                count += 1
            else:
                break
        logger.debug("Queries in last hour: {}", count)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {}
        for mode, data in self._coverage_map.items():
            count = data['count']
            doctrine_matched = data['doctrine_matched']
            hit_rate = (doctrine_matched / count) if count else 0.0
            report[mode] = {
                'queries': count,
                'doctrine_matched': doctrine_matched,
                'doctrine_hit_rate': hit_rate
            }
        logger.debug("Coverage report: {}", report)
        return report

    def export_jsonl(self, path: str) -> int:
        p = pathlib.Path(path)
        count = 0
        with p.open('w', encoding='utf-8') as f:
            for q in self._queries:
                f.write(json.dumps(asdict(q)) + '\n')
                count += 1
        logger.info("Exported {} queries to {}", count, path)
        return count

class AuditTrailWriter:
    def __init__(self, base_dir: str = "audit_trail"):
        self.base_dir = pathlib.Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        logger.info("AuditTrailWriter initialized at {}", self.base_dir)

    def write(self, metrics: QueryMetrics):
        audit_entry = asdict(metrics)
        audit_entry['audit_timestamp'] = time.time()
        filename = self._get_filename(metrics)
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(json.dumps(audit_entry) + '\n')
        logger.debug("Wrote audit trail for query_id={} to {}", metrics.query_id, filename)

    def _get_filename(self, metrics: QueryMetrics) -> str:
        date_str = time.strftime('%Y%m%d', time.localtime(metrics.timestamp))
        file_hash = hashlib.sha256(metrics.query_id.encode()).hexdigest()[:8]
        filename = f"{metrics.engine_id}_{date_str}_{file_hash}.jsonl"
        return str(self.base_dir / filename)

COLLECTOR = TelemetryCollector()