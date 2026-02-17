import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any, Tuple
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "AUTO14"

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
        self._errors: deque = deque(maxlen=10000)
        self._audit_trail_writer = AuditTrailWriter()
        self._query_counter: Counter = Counter()
        self._doctrine_counter: Counter = Counter()
        self._cache_hit_counter: Counter = Counter()
        self._mode_counter: Counter = Counter()
        self._confidence_values: List[float] = []
        self._latency_values: List[float] = []
        self._error_types: Counter = Counter()
        self._coverage: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._query_counter[metrics.engine_id] += 1
        self._doctrine_counter[metrics.doctrine_matched] += 1
        self._cache_hit_counter[metrics.cache_hit] += 1
        self._mode_counter[metrics.mode] += 1
        self._confidence_values.append(metrics.confidence)
        self._latency_values.append(metrics.latency_ms)
        if metrics.error:
            self.record_error(metrics.error, "Query error", metrics.query_id)
        self._coverage[metrics.mode]['total'] += 1
        if metrics.doctrine_matched:
            self._coverage[metrics.mode]['doctrine_matched'] += 1
        self._audit_trail_writer.write(metrics)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_record = {
            "timestamp": time.time(),
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "engine_id": ENGINE_ID
        }
        self._errors.append(error_record)
        self._error_types[error_type] += 1
        logger.error(f"Error recorded: {error_type} - {message} (query_id={query_id})")

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = [q.latency_ms for q in self._queries if q.latency_ms is not None]
        if not latencies:
            return {
                "avg": None,
                "p50": None,
                "p95": None,
                "p99": None,
                "min": None,
                "max": None
            }
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies_sorted)
        p50 = statistics.median(latencies_sorted)
        p95 = latencies_sorted[int(0.95 * len(latencies_sorted)) - 1]
        p99 = latencies_sorted[int(0.99 * len(latencies_sorted)) - 1]
        min_latency = latencies_sorted[0]
        max_latency = latencies_sorted[-1]
        return {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_latency,
            "max": max_latency
        }

    def get_doctrine_hit_rate(self) -> float:
        total = self._doctrine_counter[True] + self._doctrine_counter[False]
        if total == 0:
            return 0.0
        return self._doctrine_counter[True] / total

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        error_count = sum(1 for e in self._errors if e["timestamp"] >= window_start)
        query_count = sum(1 for q in self._queries if q.timestamp >= window_start)
        if query_count == 0:
            return 0.0
        return error_count / query_count

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        return sum(1 for q in self._queries if q.timestamp >= one_hour_ago)

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {}
        for mode, stats in self._coverage.items():
            total = stats['total']
            doctrine_matched = stats['doctrine_matched']
            doctrine_rate = doctrine_matched / total if total else 0.0
            report[mode] = {
                "total_queries": total,
                "doctrine_matched": doctrine_matched,
                "doctrine_rate": doctrine_rate
            }
        return report

    def export_jsonl(self, path: str) -> int:
        p = pathlib.Path(path)
        count = 0
        with p.open('w', encoding='utf-8') as f:
            for q in self._queries:
                f.write(json.dumps(asdict(q)) + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {path}")
        return count

class AuditTrailWriter:
    def __init__(self, audit_path: Optional[str] = None):
        self._audit_path = audit_path or f"./audit_trail_{ENGINE_ID}.jsonl"
        self._file = None
        self._open_file()

    def _open_file(self):
        p = pathlib.Path(self._audit_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        self._file = p.open('a', encoding='utf-8')

    def write(self, metrics: QueryMetrics):
        record = asdict(metrics)
        record['audit_hash'] = self._hash_record(record)
        self._file.write(json.dumps(record) + "\n")
        self._file.flush()

    def _hash_record(self, record: Dict[str, Any]) -> str:
        record_bytes = json.dumps(record, sort_keys=True).encode('utf-8')
        return hashlib.sha256(record_bytes).hexdigest()

    def close(self):
        if self._file:
            self._file.close()
            self._file = None

COLLECTOR = TelemetryCollector()