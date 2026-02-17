import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Union
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "CHEM03"

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
    def __init__(self, engine_id: str = ENGINE_ID, maxlen: int = 10000):
        self.engine_id = engine_id
        self._queries = deque(maxlen=maxlen)
        self._errors = deque(maxlen=maxlen)
        self._query_index = {}
        self._doctrine_counter = Counter()
        self._cache_counter = Counter()
        self._mode_counter = Counter()
        self._confidence_values = []
        self._error_types = Counter()
        self._audit_writer = AuditTrailWriter()
        self._coverage_counter = defaultdict(lambda: {'matched': 0, 'total': 0})

    def record_query(self, metrics: QueryMetrics):
        logger.debug(f"Recording query: {metrics}")
        self._queries.append(metrics)
        self._query_index[metrics.query_id] = metrics
        self._doctrine_counter[metrics.doctrine_matched] += 1
        self._cache_counter[metrics.cache_hit] += 1
        self._mode_counter[metrics.mode] += 1
        self._confidence_values.append(metrics.confidence)
        self._coverage_counter[metrics.mode]['total'] += 1
        if metrics.doctrine_matched:
            self._coverage_counter[metrics.mode]['matched'] += 1
        if metrics.error:
            self.record_error("query_error", metrics.error, metrics.query_id)
        self._audit_writer.write(metrics)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        timestamp = time.time()
        error_record = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "timestamp": timestamp,
            "engine_id": self.engine_id
        }
        logger.error(f"Recording error: {error_record}")
        self._errors.append(error_record)
        self._error_types[error_type] += 1

    def get_latency_stats(self) -> Dict[str, Union[float, None]]:
        latencies = [q.latency_ms for q in self._queries if q.latency_ms is not None]
        if not latencies:
            return {k: None for k in ['avg', 'p50', 'p95', 'p99', 'min', 'max']}
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        min_latency = min(latencies)
        max_latency = max(latencies)
        p50 = statistics.median(latencies)
        p95 = latencies_sorted[int(len(latencies_sorted) * 0.95) - 1]
        p99 = latencies_sorted[int(len(latencies_sorted) * 0.99) - 1]
        return {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_latency,
            "max": max_latency
        }

    def get_doctrine_hit_rate(self) -> float:
        total = sum(self._doctrine_counter.values())
        if total == 0:
            return 0.0
        matched = self._doctrine_counter[True]
        return matched / total

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self._errors if e['timestamp'] >= window_start]
        queries_in_window = [q for q in self._queries if q.timestamp >= window_start]
        num_queries = len(queries_in_window)
        if num_queries == 0:
            return 0.0
        return len(errors_in_window) / num_queries

    def queries_last_hour(self) -> int:
        now = time.time()
        window_start = now - 3600
        return sum(1 for q in self._queries if q.timestamp >= window_start)

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {}
        for mode, counts in self._coverage_counter.items():
            total = counts['total']
            matched = counts['matched']
            hit_rate = matched / total if total > 0 else 0.0
            report[mode] = {
                "total": total,
                "matched": matched,
                "hit_rate": hit_rate
            }
        confidence_stats = {}
        if self._confidence_values:
            confidence_stats = {
                "avg": statistics.mean(self._confidence_values),
                "min": min(self._confidence_values),
                "max": max(self._confidence_values),
                "p50": statistics.median(self._confidence_values)
            }
        report['confidence_stats'] = confidence_stats
        report['error_types'] = dict(self._error_types)
        return report

    def export_jsonl(self, path: Union[str, pathlib.Path]) -> int:
        path = pathlib.Path(path)
        count = 0
        with path.open('w', encoding='utf-8') as f:
            for q in self._queries:
                f.write(json.dumps(dataclasses.asdict(q)) + '\n')
                count += 1
        logger.info(f"Exported {count} queries to {path}")
        return count

class AuditTrailWriter:
    def __init__(self, base_dir: Union[str, pathlib.Path] = "./audit_trail"):
        self.base_dir = pathlib.Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _get_audit_path(self, query_id: str) -> pathlib.Path:
        hash_id = hashlib.sha256(query_id.encode()).hexdigest()
        subdir = hash_id[:2]
        dir_path = self.base_dir / subdir
        dir_path.mkdir(parents=True, exist_ok=True)
        filename = f"{query_id}.jsonl"
        return dir_path / filename

    def write(self, metrics: QueryMetrics):
        path = self._get_audit_path(metrics.query_id)
        record = dataclasses.asdict(metrics)
        with path.open('a', encoding='utf-8') as f:
            f.write(json.dumps(record) + '\n')
        logger.debug(f"Wrote audit trail for query {metrics.query_id} to {path}")

COLLECTOR = TelemetryCollector(engine_id=ENGINE_ID)