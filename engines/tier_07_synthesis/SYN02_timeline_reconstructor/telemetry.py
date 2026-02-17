import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any, Tuple
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "SYN02"

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
        self._errors: deque = deque(maxlen=max_queries)
        self._doctrine_hits: deque = deque(maxlen=max_queries)
        self._cache_hits: deque = deque(maxlen=max_queries)
        self._latencies: deque = deque(maxlen=max_queries)
        self._query_times: deque = deque(maxlen=max_queries)
        self._query_ids: set = set()
        self._coverage_counter: Counter = Counter()
        self._audit_writer: Optional[AuditTrailWriter] = None

    def record_query(self, metrics: QueryMetrics):
        if metrics.query_id in self._query_ids:
            logger.warning(f"Duplicate query_id detected: {metrics.query_id}")
            return
        self._queries.append(metrics)
        self._query_ids.add(metrics.query_id)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._cache_hits.append(metrics.cache_hit)
        self._query_times.append(metrics.timestamp)
        self._coverage_counter[(metrics.mode, metrics.doctrine_matched)] += 1
        if self._audit_writer:
            self._audit_writer.write(metrics)
        logger.debug(f"Recorded query: {metrics}")

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "timestamp": time.time(),
            "engine_id": ENGINE_ID
        }
        self._errors.append(error_entry)
        logger.error(f"Error recorded: {error_entry}")

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = list(self._latencies)
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
        avg = statistics.mean(latencies)
        min_latency = min(latencies)
        max_latency = max(latencies)
        p50 = statistics.median(latencies)
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
        hits = sum(1 for hit in self._doctrine_hits if hit)
        total = len(self._doctrine_hits)
        if total == 0:
            return 0.0
        return hits / total

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        queries_in_window = [q for q in self._queries if q.timestamp >= window_start]
        error_count = len(errors_in_window)
        query_count = len(queries_in_window)
        if query_count == 0:
            return 0.0
        return error_count / query_count

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= one_hour_ago)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        report = defaultdict(lambda: {"doctrine_matched": 0, "not_matched": 0, "total": 0})
        for (mode, doctrine_matched), count in self._coverage_counter.items():
            if doctrine_matched:
                report[mode]["doctrine_matched"] += count
            else:
                report[mode]["not_matched"] += count
            report[mode]["total"] += count
        return dict(report)

    def export_jsonl(self, path: str) -> int:
        p = pathlib.Path(path)
        count = 0
        with p.open("w", encoding="utf-8") as f:
            for q in self._queries:
                f.write(json.dumps(asdict(q)) + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {path}")
        return count

    def set_audit_writer(self, writer: 'AuditTrailWriter'):
        self._audit_writer = writer

class AuditTrailWriter:
    def __init__(self, directory: str):
        self.directory = pathlib.Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        self._file_handles: Dict[str, Any] = {}

    def _get_file_handle(self, query_id: str) -> Any:
        filename = f"{query_id}.jsonl"
        path = self.directory / filename
        if filename not in self._file_handles:
            fh = path.open("a", encoding="utf-8")
            self._file_handles[filename] = fh
        return self._file_handles[filename]

    def write(self, metrics: QueryMetrics):
        fh = self._get_file_handle(metrics.query_id)
        fh.write(json.dumps(asdict(metrics)) + "\n")
        fh.flush()
        logger.debug(f"Audit trail written for query_id: {metrics.query_id}")

    def close(self):
        for fh in self._file_handles.values():
            fh.close()
        self._file_handles.clear()
        logger.info("AuditTrailWriter file handles closed.")

COLLECTOR = TelemetryCollector()