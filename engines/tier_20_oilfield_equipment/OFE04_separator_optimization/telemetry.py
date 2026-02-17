import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "OFE04"

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
        self.queries: deque = deque(maxlen=max_queries)
        self.errors: deque = deque(maxlen=max_queries)
        self.audit_writer: Optional[AuditTrailWriter] = None
        self._query_id_set: set = set()
        self._doctrine_counter: Counter = Counter()
        self._cache_counter: Counter = Counter()
        self._mode_counter: Counter = Counter()
        self._confidence_list: List[float] = []
        self._error_counter: Counter = Counter()
        self._coverage_counter: Counter = Counter()
        self._last_export_time: float = 0.0

    def record_query(self, metrics: QueryMetrics):
        if metrics.query_id in self._query_id_set:
            logger.warning(f"Duplicate query_id detected: {metrics.query_id}")
            return
        self.queries.append(metrics)
        self._query_id_set.add(metrics.query_id)
        self._doctrine_counter[metrics.doctrine_matched] += 1
        self._cache_counter[metrics.cache_hit] += 1
        self._mode_counter[metrics.mode] += 1
        self._confidence_list.append(metrics.confidence)
        self._coverage_counter[(metrics.mode, metrics.doctrine_matched)] += 1
        if metrics.error:
            self._error_counter[metrics.error] += 1
            self.errors.append({
                "error_type": metrics.error,
                "query_id": metrics.query_id,
                "timestamp": metrics.timestamp
            })
        if self.audit_writer:
            self.audit_writer.write(metrics)
        logger.debug(f"Recorded query: {metrics.query_id}")

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        timestamp = time.time()
        error_entry = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "timestamp": timestamp
        }
        self.errors.append(error_entry)
        self._error_counter[error_type] += 1
        logger.error(f"Error recorded: {error_type} ({query_id}) {message}")

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = [q.latency_ms for q in self.queries if q.latency_ms is not None]
        if not latencies:
            return {
                "avg": None, "p50": None, "p95": None, "p99": None,
                "min": None, "max": None
            }
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        min_latency = min(latencies_sorted)
        max_latency = max(latencies_sorted)
        p50 = statistics.median(latencies_sorted)
        p95 = latencies_sorted[int(0.95 * len(latencies_sorted))-1]
        p99 = latencies_sorted[int(0.99 * len(latencies_sorted))-1]
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
        hits = self._doctrine_counter[True]
        return hits / total

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        error_count = sum(1 for e in self.errors if e["timestamp"] >= window_start)
        query_count = sum(1 for q in self.queries if q.timestamp >= window_start)
        if query_count == 0:
            return 0.0
        return error_count / query_count

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        return sum(1 for q in self.queries if q.timestamp >= one_hour_ago)

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {
            "mode_counts": dict(self._mode_counter),
            "doctrine_matched_counts": dict(self._doctrine_counter),
            "cache_hit_counts": dict(self._cache_counter),
            "confidence_stats": self._confidence_stats(),
            "coverage_matrix": {}
        }
        for (mode, doctrine), count in self._coverage_counter.items():
            report["coverage_matrix"][f"{mode}|{doctrine}"] = count
        return report

    def _confidence_stats(self) -> Dict[str, Any]:
        if not self._confidence_list:
            return {"avg": None, "min": None, "max": None}
        return {
            "avg": statistics.mean(self._confidence_list),
            "min": min(self._confidence_list),
            "max": max(self._confidence_list)
        }

    def export_jsonl(self, path: str) -> int:
        p = pathlib.Path(path)
        exported = 0
        with p.open("a", encoding="utf-8") as f:
            for q in self.queries:
                f.write(json.dumps(asdict(q)) + "\n")
                exported += 1
        self._last_export_time = time.time()
        logger.info(f"Exported {exported} queries to {path}")
        return exported

    def set_audit_writer(self, writer: 'AuditTrailWriter'):
        self.audit_writer = writer

class AuditTrailWriter:
    def __init__(self, path: str):
        self.path = pathlib.Path(path)
        self._lock = None  # Placeholder for threading.Lock if needed

    def write(self, metrics: QueryMetrics):
        entry = asdict(metrics)
        entry["audit_hash"] = self._hash_entry(entry)
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        logger.debug(f"Audit trail written for query: {metrics.query_id}")

    def _hash_entry(self, entry: Dict[str, Any]) -> str:
        s = json.dumps(entry, sort_keys=True)
        return hashlib.sha256(s.encode("utf-8")).hexdigest()

COLLECTOR = TelemetryCollector()

# Example: Set up default audit trail writer
audit_path = pathlib.Path("ofe04_audit_trail.jsonl")
COLLECTOR.set_audit_writer(AuditTrailWriter(str(audit_path)))