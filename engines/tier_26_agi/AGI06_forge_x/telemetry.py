import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional, Any
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "AGI06"

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
        self._cache_hits: deque = deque(maxlen=maxlen)
        self._latencies: deque = deque(maxlen=maxlen)
        self._query_ids: set = set()
        self._mode_counter: Counter = Counter()
        self._confidence_values: deque = deque(maxlen=maxlen)
        self._coverage: defaultdict = defaultdict(int)
        self._audit_writer = AuditTrailWriter()
        logger.info("TelemetryCollector initialized with maxlen={}", maxlen)

    def record_query(self, metrics: QueryMetrics):
        if metrics.query_id in self._query_ids:
            logger.warning("Duplicate query_id detected: {}", metrics.query_id)
            return
        self._query_ids.add(metrics.query_id)
        self._queries.append(metrics)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._cache_hits.append(metrics.cache_hit)
        self._mode_counter[metrics.mode] += 1
        self._confidence_values.append(metrics.confidence)
        self._coverage[metrics.mode] += 1
        if metrics.error:
            self._errors.append({
                'timestamp': metrics.timestamp,
                'error_type': metrics.error,
                'query_id': metrics.query_id
            })
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

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = list(self._latencies)
        if not latencies:
            return {
                'avg': None,
                'p50': None,
                'p95': None,
                'p99': None,
                'min': None,
                'max': None
            }
        latencies_sorted = sorted(latencies)
        stats = {
            'avg': statistics.mean(latencies),
            'p50': statistics.median(latencies),
            'p95': self._percentile(latencies_sorted, 95),
            'p99': self._percentile(latencies_sorted, 99),
            'min': min(latencies),
            'max': max(latencies)
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
        queries_in_window = [q for q in self._queries if q.timestamp >= window_start]
        errors_in_window = [e for e in self._errors if e['timestamp'] >= window_start]
        total = len(queries_in_window)
        error_count = len(errors_in_window)
        error_rate = (error_count / total) if total > 0 else 0.0
        logger.debug("Error rate in last {} hours: {}", window_hours, error_rate)
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= one_hour_ago)
        logger.debug("Queries in last hour: {}", count)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        total = sum(self._mode_counter.values())
        report = {}
        for mode, count in self._mode_counter.items():
            report[mode] = {
                'count': count,
                'percent': (count / total) * 100 if total > 0 else 0.0
            }
        confidences = list(self._confidence_values)
        report['confidence'] = {
            'avg': statistics.mean(confidences) if confidences else None,
            'min': min(confidences) if confidences else None,
            'max': max(confidences) if confidences else None
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

    @staticmethod
    def _percentile(sorted_list: List[float], percentile: float) -> float:
        if not sorted_list:
            return None
        k = (len(sorted_list) - 1) * (percentile / 100)
        f = int(k)
        c = min(f + 1, len(sorted_list) - 1)
        if f == c:
            return sorted_list[int(k)]
        d0 = sorted_list[f] * (c - k)
        d1 = sorted_list[c] * (k - f)
        return d0 + d1

class AuditTrailWriter:
    def __init__(self, audit_dir: Optional[str] = None):
        if audit_dir is None:
            audit_dir = "./audit_trail"
        self.audit_dir = pathlib.Path(audit_dir)
        self.audit_dir.mkdir(parents=True, exist_ok=True)
        logger.info("AuditTrailWriter initialized at {}", self.audit_dir)

    def write(self, metrics: QueryMetrics):
        audit_entry = asdict(metrics)
        audit_entry['audit_timestamp'] = time.time()
        filename = self._get_audit_filename(metrics.query_id)
        try:
            with open(filename, 'a', encoding='utf-8') as f:
                f.write(json.dumps(audit_entry) + '\n')
            logger.debug("Wrote audit trail for query_id {} to {}", metrics.query_id, filename)
        except Exception as e:
            logger.error("Failed to write audit trail: {}", e)

    def _get_audit_filename(self, query_id: str) -> str:
        # Hash query_id to avoid filesystem issues
        h = hashlib.sha256(query_id.encode('utf-8')).hexdigest()
        filename = self.audit_dir / f"{h}.jsonl"
        return str(filename)

COLLECTOR = TelemetryCollector()