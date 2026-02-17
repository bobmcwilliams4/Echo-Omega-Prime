import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Union
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "G02"

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
        self._query_id_index: Dict[str, QueryMetrics] = {}
        self._error_counter: Counter = Counter()
        self._coverage_counter: Counter = Counter()
        self._audit_writer: Optional['AuditTrailWriter'] = None

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._query_id_index[metrics.query_id] = metrics
        self._latencies.append(metrics.latency_ms)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._coverage_counter[metrics.mode] += 1
        if metrics.error:
            self.record_error(metrics.error, str(metrics.error), metrics.query_id)
        if self._audit_writer:
            self._audit_writer.write(metrics)

    def record_error(self, error_type: str, message: str, query_id: str):
        error_record = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "timestamp": time.time()
        }
        self._errors.append(error_record)
        self._error_counter[error_type] += 1

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = [q.latency_ms for q in self._queries if q.latency_ms is not None]
        if not latencies:
            return {
                "avg": None, "p50": None, "p95": None, "p99": None,
                "min": None, "max": None
            }
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        min_latency = latencies_sorted[0]
        max_latency = latencies_sorted[-1]
        p50 = statistics.median(latencies_sorted)
        p95 = latencies_sorted[int(0.95 * len(latencies_sorted)) - 1]
        p99 = latencies_sorted[int(0.99 * len(latencies_sorted)) - 1]
        return {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_latency,
            "max": max_latency
        }

    def get_doctrine_hit_rate(self) -> float:
        total = len(self._doctrine_hits)
        if total == 0:
            return 0.0
        hits = sum(1 for hit in self._doctrine_hits if hit)
        return hits / total

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        queries_in_window = [q for q in self._queries if q.timestamp >= window_start]
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        total_queries = len(queries_in_window)
        total_errors = len(errors_in_window)
        if total_queries == 0:
            return 0.0
        return total_errors / total_queries

    def queries_last_hour(self) -> int:
        now = time.time()
        hour_ago = now - 3600
        return sum(1 for q in self._queries if q.timestamp >= hour_ago)

    def get_coverage_report(self) -> Dict[str, Any]:
        total = sum(self._coverage_counter.values())
        if total == 0:
            return {}
        report = {}
        for mode, count in self._coverage_counter.items():
            report[mode] = {
                "count": count,
                "rate": count / total
            }
        return report

    def export_jsonl(self, path: Union[str, pathlib.Path]) -> int:
        path = pathlib.Path(path)
        count = 0
        with path.open("w", encoding="utf-8") as f:
            for q in self._queries:
                f.write(json.dumps(dataclasses.asdict(q)) + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {path}")
        return count

    def set_audit_writer(self, writer: 'AuditTrailWriter'):
        self._audit_writer = writer

class AuditTrailWriter:
    def __init__(self, directory: Union[str, pathlib.Path]):
        self.directory = pathlib.Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        self._open_files: Dict[str, Any] = {}

    def _get_file(self, query_id: str) -> pathlib.Path:
        hash_id = hashlib.sha256(query_id.encode()).hexdigest()[:8]
        filename = f"audit_{hash_id}.jsonl"
        return self.directory / filename

    def write(self, metrics: QueryMetrics):
        file_path = self._get_file(metrics.query_id)
        with file_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(dataclasses.asdict(metrics)) + "\n")
        logger.debug(f"Audit trail written for query_id={metrics.query_id}")

COLLECTOR = TelemetryCollector(max_queries=10000)