import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any, Tuple
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "MED10"

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
        self.max_queries = max_queries
        self.queries: deque = deque(maxlen=max_queries)
        self.errors: deque = deque(maxlen=max_queries)
        self.doctrine_hits: deque = deque(maxlen=max_queries)
        self.audit_writer = AuditTrailWriter()
        self.query_counter = Counter()
        self.error_counter = Counter()
        self.coverage_counter = defaultdict(lambda: {"matched": 0, "total": 0})
        self.latency_values: deque = deque(maxlen=max_queries)
        self.last_hour_window = 3600  # seconds

    def record_query(self, metrics: QueryMetrics):
        self.queries.append(metrics)
        self.latency_values.append(metrics.latency_ms)
        self.query_counter[metrics.mode] += 1
        self.doctrine_hits.append(metrics.doctrine_matched)
        self.coverage_counter[metrics.mode]["total"] += 1
        if metrics.doctrine_matched:
            self.coverage_counter[metrics.mode]["matched"] += 1
        self.audit_writer.write(metrics)
        if metrics.error:
            self.record_error("query_error", metrics.error, metrics.query_id)

    def record_error(self, error_type: str, message: str, query_id: str):
        error_record = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "timestamp": time.time(),
            "engine_id": ENGINE_ID
        }
        self.errors.append(error_record)
        self.error_counter[error_type] += 1
        self.audit_writer.write_error(error_record)

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = [q.latency_ms for q in self.queries if q.latency_ms is not None]
        if not latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        min_latency = latencies_sorted[0]
        max_latency = latencies_sorted[-1]
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
        total = len(self.doctrine_hits)
        if total == 0:
            return 0.0
        hits = sum(1 for hit in self.doctrine_hits if hit)
        return hits / total

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_seconds = window_hours * 3600
        queries_in_window = [q for q in self.queries if now - q.timestamp <= window_seconds]
        errors_in_window = [e for e in self.errors if now - e["timestamp"] <= window_seconds]
        num_queries = len(queries_in_window)
        num_errors = len(errors_in_window)
        if num_queries == 0:
            return 0.0
        return num_errors / num_queries

    def queries_last_hour(self) -> int:
        now = time.time()
        return sum(1 for q in self.queries if now - q.timestamp <= self.last_hour_window)

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {}
        for mode, counts in self.coverage_counter.items():
            total = counts["total"]
            matched = counts["matched"]
            coverage = matched / total if total > 0 else 0.0
            report[mode] = {
                "total": total,
                "matched": matched,
                "coverage": coverage
            }
        return report

    def export_jsonl(self, path: str) -> int:
        p = pathlib.Path(path)
        count = 0
        with p.open("w", encoding="utf-8") as f:
            for q in self.queries:
                f.write(json.dumps(asdict(q)) + "\n")
                count += 1
            for e in self.errors:
                f.write(json.dumps(e) + "\n")
                count += 1
        logger.info(f"Exported {count} records to {path}")
        return count

class AuditTrailWriter:
    def __init__(self, audit_dir: Optional[str] = None):
        self.audit_dir = audit_dir or "./audit_trail"
        self.audit_path = pathlib.Path(self.audit_dir)
        self.audit_path.mkdir(exist_ok=True)
        self.query_log_path = self.audit_path / "queries.jsonl"
        self.error_log_path = self.audit_path / "errors.jsonl"
        self._query_fp = None
        self._error_fp = None
        self._open_files()

    def _open_files(self):
        self._query_fp = self.query_log_path.open("a", encoding="utf-8")
        self._error_fp = self.error_log_path.open("a", encoding="utf-8")

    def write(self, metrics: QueryMetrics):
        record = asdict(metrics)
        self._query_fp.write(json.dumps(record) + "\n")
        self._query_fp.flush()

    def write_error(self, error_record: Dict[str, Any]):
        self._error_fp.write(json.dumps(error_record) + "\n")
        self._error_fp.flush()

    def close(self):
        if self._query_fp:
            self._query_fp.close()
        if self._error_fp:
            self._error_fp.close()

    def __del__(self):
        self.close()

COLLECTOR = TelemetryCollector()