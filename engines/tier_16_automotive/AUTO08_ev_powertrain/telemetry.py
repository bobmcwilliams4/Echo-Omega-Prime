import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Union
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "AUTO08"

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
        self._query_ids: set = set()
        self._modes: Counter = Counter()
        self._confidence_scores: deque = deque(maxlen=maxlen)
        self._coverage: defaultdict = defaultdict(lambda: {'count': 0, 'doctrine_matched': 0})
        logger.info("TelemetryCollector initialized with maxlen={}", maxlen)

    def record_query(self, metrics: QueryMetrics):
        if metrics.query_id in self._query_ids:
            logger.warning("Duplicate query_id detected: {}", metrics.query_id)
            return
        self._queries.append(metrics)
        self._query_ids.add(metrics.query_id)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._modes[metrics.mode] += 1
        self._confidence_scores.append(metrics.confidence)
        self._coverage[metrics.mode]['count'] += 1
        if metrics.doctrine_matched:
            self._coverage[metrics.mode]['doctrine_matched'] += 1
        logger.debug("Recorded query: {}", metrics)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            'timestamp': time.time(),
            'error_type': error_type,
            'message': message,
            'query_id': query_id
        }
        self._errors.append(error_entry)
        logger.error("Recorded error: {}", error_entry)

    def get_latency_stats(self) -> Dict[str, Union[float, None]]:
        latencies = list(self._latencies)
        if not latencies:
            return dict(avg=None, p50=None, p95=None, p99=None, min=None, max=None)
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = latencies_sorted[int(len(latencies_sorted) * 0.95) - 1]
        p99 = latencies_sorted[int(len(latencies_sorted) * 0.99) - 1]
        min_latency = min(latencies)
        max_latency = max(latencies)
        stats = dict(
            avg=avg,
            p50=p50,
            p95=p95,
            p99=p99,
            min=min_latency,
            max=max_latency
        )
        logger.info("Latency stats: {}", stats)
        return stats

    def get_doctrine_hit_rate(self) -> float:
        hits = sum(1 for hit in self._doctrine_hits if hit)
        total = len(self._doctrine_hits)
        rate = hits / total if total else 0.0
        logger.info("Doctrine hit rate: {:.3f}", rate)
        return rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self._errors if e['timestamp'] >= window_start]
        queries_in_window = [q for q in self._queries if q.timestamp >= window_start]
        error_count = len(errors_in_window)
        query_count = len(queries_in_window)
        rate = error_count / query_count if query_count else 0.0
        logger.info("Error rate in last {} hours: {:.3f}", window_hours, rate)
        return rate

    def queries_last_hour(self) -> int:
        now = time.time()
        window_start = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= window_start)
        logger.info("Queries in last hour: {}", count)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {}
        for mode, data in self._coverage.items():
            total = data['count']
            doctrine_matched = data['doctrine_matched']
            hit_rate = doctrine_matched / total if total else 0.0
            report[mode] = {
                'total': total,
                'doctrine_matched': doctrine_matched,
                'hit_rate': hit_rate
            }
        logger.info("Coverage report: {}", report)
        return report

    def export_jsonl(self, path: Union[str, pathlib.Path]) -> int:
        p = pathlib.Path(path)
        count = 0
        with p.open('w', encoding='utf-8') as f:
            for q in self._queries:
                f.write(json.dumps(dataclasses.asdict(q)) + '\n')
                count += 1
        logger.info("Exported {} queries to {}", count, path)
        return count

class AuditTrailWriter:
    def __init__(self, audit_path: Union[str, pathlib.Path]):
        self.audit_path = pathlib.Path(audit_path)
        self.audit_path.parent.mkdir(parents=True, exist_ok=True)
        logger.info("AuditTrailWriter initialized at {}", self.audit_path)

    def write(self, query_metrics: QueryMetrics, extra: Optional[Dict[str, Any]] = None):
        entry = dataclasses.asdict(query_metrics)
        if extra:
            entry.update(extra)
        entry['audit_hash'] = self._hash_entry(entry)
        with self.audit_path.open('a', encoding='utf-8') as f:
            f.write(json.dumps(entry) + '\n')
        logger.debug("Audit trail written for query_id={}", query_metrics.query_id)

    def _hash_entry(self, entry: Dict[str, Any]) -> str:
        raw = json.dumps(entry, sort_keys=True)
        return hashlib.sha256(raw.encode('utf-8')).hexdigest()

COLLECTOR = TelemetryCollector(maxlen=10000)