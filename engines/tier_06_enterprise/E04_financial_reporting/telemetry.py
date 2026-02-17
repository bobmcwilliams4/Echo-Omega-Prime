import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict, field
from typing import Optional, List, Dict, Any, Union
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "E04"

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
        self._doctrine_matches: deque = deque(maxlen=maxlen)
        self._cache_hits: deque = deque(maxlen=maxlen)
        self._latencies: deque = deque(maxlen=maxlen)
        self._query_times: deque = deque(maxlen=maxlen)
        self._query_modes: Counter = Counter()
        self._confidence_scores: deque = deque(maxlen=maxlen)
        self._coverage: defaultdict = defaultdict(lambda: {'count': 0, 'errors': 0})
        self._audit_writer = AuditTrailWriter()
        logger.info("TelemetryCollector initialized with maxlen={}", maxlen)

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_matches.append(metrics.doctrine_matched)
        self._cache_hits.append(metrics.cache_hit)
        self._query_times.append(metrics.timestamp)
        self._query_modes[metrics.mode] += 1
        self._confidence_scores.append(metrics.confidence)
        self._coverage[metrics.mode]['count'] += 1
        if metrics.error:
            self._coverage[metrics.mode]['errors'] += 1
        self._audit_writer.write(metrics)
        logger.debug("Recorded query: {}", metrics)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_event = {
            'timestamp': time.time(),
            'error_type': error_type,
            'message': message,
            'query_id': query_id
        }
        self._errors.append(error_event)
        logger.error("Error recorded: {}", error_event)

    def get_latency_stats(self) -> Dict[str, Union[float, None]]:
        latencies = list(self._latencies)
        if not latencies:
            return {'avg': None, 'p50': None, 'p95': None, 'p99': None, 'min': None, 'max': None}
        latencies.sort()
        avg = statistics.mean(latencies)
        min_latency = latencies[0]
        max_latency = latencies[-1]
        p50 = statistics.median(latencies)
        p95 = latencies[int(0.95 * len(latencies)) - 1]
        p99 = latencies[int(0.99 * len(latencies)) - 1]
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
        hit_rate = sum(1 for m in matches if m) / len(matches)
        logger.debug("Doctrine hit rate: {:.2%}", hit_rate)
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        total = 0
        errors = 0
        for q in self._queries:
            if q.timestamp >= window_start:
                total += 1
                if q.error:
                    errors += 1
        if total == 0:
            return 0.0
        error_rate = errors / total
        logger.debug("Error rate in last {:.2f}h: {:.2%}", window_hours, error_rate)
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for t in self._query_times if t >= one_hour_ago)
        logger.debug("Queries in last hour: {}", count)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {}
        for mode, data in self._coverage.items():
            total = data['count']
            errors = data['errors']
            error_rate = errors / total if total > 0 else 0.0
            report[mode] = {
                'total': total,
                'errors': errors,
                'error_rate': error_rate
            }
        logger.debug("Coverage report: {}", report)
        return report

    def export_jsonl(self, path: Union[str, pathlib.Path]) -> int:
        path = pathlib.Path(path)
        count = 0
        with path.open('w', encoding='utf-8') as f:
            for q in self._queries:
                f.write(json.dumps(asdict(q)) + '\n')
                count += 1
        logger.info("Exported {} queries to {}", count, path)
        return count

class AuditTrailWriter:
    def __init__(self, base_dir: Union[str, pathlib.Path] = "./audit_trail"):
        self.base_dir = pathlib.Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        logger.info("AuditTrailWriter initialized at {}", self.base_dir)

    def write(self, metrics: QueryMetrics):
        date_str = time.strftime("%Y-%m-%d", time.localtime(metrics.timestamp))
        file_path = self.base_dir / f"audit_{date_str}.jsonl"
        entry = asdict(metrics)
        entry['audit_hash'] = self._hash_entry(entry)
        with file_path.open('a', encoding='utf-8') as f:
            f.write(json.dumps(entry) + '\n')
        logger.debug("Audit trail written for query_id {} to {}", metrics.query_id, file_path)

    def _hash_entry(self, entry: dict) -> str:
        # Exclude audit_hash itself to avoid recursion
        entry_copy = dict(entry)
        entry_copy.pop('audit_hash', None)
        entry_bytes = json.dumps(entry_copy, sort_keys=True).encode('utf-8')
        return hashlib.sha256(entry_bytes).hexdigest()

COLLECTOR = TelemetryCollector()