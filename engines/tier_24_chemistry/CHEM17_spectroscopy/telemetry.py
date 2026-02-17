import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any, Union
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "CHEM17"

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
        self._coverage: defaultdict = defaultdict(lambda: {"count": 0, "doctrine_matched": 0})
        self._query_ids: set = set()
        self._audit_writer: Optional[AuditTrailWriter] = None

    def record_query(self, metrics: QueryMetrics):
        logger.debug(f"Recording query: {metrics.query_id}")
        self._queries.append(metrics)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._coverage[metrics.mode]["count"] += 1
        if metrics.doctrine_matched:
            self._coverage[metrics.mode]["doctrine_matched"] += 1
        self._query_ids.add(metrics.query_id)
        if self._audit_writer:
            self._audit_writer.write(metrics)
        if metrics.error:
            self.record_error("query_error", metrics.error, metrics.query_id)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "timestamp": time.time()
        }
        logger.error(f"Recording error: {error_entry}")
        self._errors.append(error_entry)
        if self._audit_writer:
            self._audit_writer.write_error(error_entry)

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = list(self._latencies)
        if not latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        min_latency = min(latencies)
        max_latency = max(latencies)
        p50 = statistics.median(latencies)
        p95 = latencies_sorted[int(len(latencies_sorted) * 0.95) - 1] if len(latencies_sorted) > 1 else latencies_sorted[0]
        p99 = latencies_sorted[int(len(latencies_sorted) * 0.99) - 1] if len(latencies_sorted) > 1 else latencies_sorted[0]
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
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        queries_in_window = [q for q in self._queries if q.timestamp >= window_start]
        total_queries = len(queries_in_window)
        if total_queries == 0:
            return 0.0
        return len(errors_in_window) / total_queries

    def queries_last_hour(self) -> int:
        now = time.time()
        window_start = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= window_start)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {}
        for mode, stats in self._coverage.items():
            count = stats["count"]
            doctrine_matched = stats["doctrine_matched"]
            hit_rate = doctrine_matched / count if count > 0 else 0.0
            report[mode] = {
                "count": count,
                "doctrine_matched": doctrine_matched,
                "doctrine_hit_rate": hit_rate
            }
        return report

    def export_jsonl(self, path: Union[str, pathlib.Path]) -> int:
        path = pathlib.Path(path)
        count = 0
        with path.open("w", encoding="utf-8") as f:
            for q in self._queries:
                f.write(json.dumps(asdict(q)) + "\n")
                count += 1
            for e in self._errors:
                f.write(json.dumps(e) + "\n")
                count += 1
        logger.info(f"Exported {count} telemetry records to {path}")
        return count

    def set_audit_writer(self, writer: 'AuditTrailWriter'):
        self._audit_writer = writer

class AuditTrailWriter:
    def __init__(self, path: Union[str, pathlib.Path]):
        self.path = pathlib.Path(path)
        self._file = self.path.open("a", encoding="utf-8")
        self._written_query_ids: set = set()

    def write(self, metrics: QueryMetrics):
        if metrics.query_id in self._written_query_ids:
            logger.debug(f"Query {metrics.query_id} already written to audit trail.")
            return
        record = asdict(metrics)
        record["audit_hash"] = self._hash_record(record)
        self._file.write(json.dumps(record) + "\n")
        self._file.flush()
        self._written_query_ids.add(metrics.query_id)
        logger.debug(f"Wrote audit trail for query {metrics.query_id}")

    def write_error(self, error_entry: Dict[str, Any]):
        error_entry["audit_hash"] = self._hash_record(error_entry)
        self._file.write(json.dumps(error_entry) + "\n")
        self._file.flush()
        logger.debug(f"Wrote audit trail for error {error_entry.get('query_id')}")

    def _hash_record(self, record: Dict[str, Any]) -> str:
        record_str = json.dumps(record, sort_keys=True)
        return hashlib.sha256(record_str.encode("utf-8")).hexdigest()

    def close(self):
        self._file.close()

COLLECTOR = TelemetryCollector(maxlen=10000)