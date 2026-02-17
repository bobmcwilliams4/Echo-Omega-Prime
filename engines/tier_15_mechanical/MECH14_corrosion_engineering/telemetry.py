import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict, field
from typing import Optional, List, Dict, Any, Union
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "MECH14"

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
        self._modes: deque = deque(maxlen=maxlen)
        self._confidences: deque = deque(maxlen=maxlen)
        self._timestamps: deque = deque(maxlen=maxlen)
        self._query_id_set = set()
        self._error_counter = Counter()
        self._audit_writer = AuditTrailWriter()
        self._coverage_counter = Counter()
        self._doctrine_matched_counter = Counter()
        self._cache_hit_counter = Counter()
        self._lock = None  # Placeholder for thread safety if needed

    def record_query(self, metrics: QueryMetrics):
        if metrics.query_id in self._query_id_set:
            logger.warning(f"Duplicate query_id detected: {metrics.query_id}")
            return
        self._query_id_set.add(metrics.query_id)
        self._queries.append(metrics)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._cache_hits.append(metrics.cache_hit)
        self._modes.append(metrics.mode)
        self._confidences.append(metrics.confidence)
        self._timestamps.append(metrics.timestamp)
        self._coverage_counter[metrics.mode] += 1
        self._doctrine_matched_counter[metrics.doctrine_matched] += 1
        self._cache_hit_counter[metrics.cache_hit] += 1
        if metrics.error:
            self.record_error(metrics.error, "Query error", metrics.query_id)
        self._audit_writer.write(metrics)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "engine_id": ENGINE_ID
        }
        self._errors.append(error_entry)
        self._error_counter[error_type] += 1
        logger.error(f"[{ENGINE_ID}] Error recorded: {error_type} | {message} | Query: {query_id}")

    def get_latency_stats(self) -> Dict[str, Union[float, None]]:
        latencies = list(self._latencies)
        if not latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = latencies_sorted[int(0.95 * len(latencies_sorted))-1]
        p99 = latencies_sorted[int(0.99 * len(latencies_sorted))-1]
        min_latency = min(latencies)
        max_latency = max(latencies)
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
        if not queries_in_window:
            return 0.0
        return len(errors_in_window) / len(queries_in_window)

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        return sum(1 for q in self._queries if q.timestamp >= one_hour_ago)

    def get_coverage_report(self) -> Dict[str, Any]:
        total = len(self._queries)
        mode_counts = dict(self._coverage_counter)
        doctrine_true = self._doctrine_matched_counter.get(True, 0)
        doctrine_false = self._doctrine_matched_counter.get(False, 0)
        cache_true = self._cache_hit_counter.get(True, 0)
        cache_false = self._cache_hit_counter.get(False, 0)
        return {
            "total_queries": total,
            "mode_counts": mode_counts,
            "doctrine_matched": {
                "true": doctrine_true,
                "false": doctrine_false
            },
            "cache_hit": {
                "true": cache_true,
                "false": cache_false
            }
        }

    def export_jsonl(self, path: Union[str, pathlib.Path]) -> int:
        path = pathlib.Path(path)
        count = 0
        with path.open("w", encoding="utf-8") as f:
            for q in self._queries:
                f.write(json.dumps(asdict(q)) + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {path}")
        return count

class AuditTrailWriter:
    def __init__(self, base_dir: Union[str, pathlib.Path] = "./audit_trail"):
        self.base_dir = pathlib.Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def write(self, metrics: QueryMetrics):
        day = time.strftime("%Y-%m-%d", time.localtime(metrics.timestamp))
        audit_path = self.base_dir / f"mech14_audit_{day}.jsonl"
        record = asdict(metrics)
        record["audit_hash"] = self._compute_hash(record)
        with audit_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
        logger.debug(f"Audit record written for query_id={metrics.query_id}")

    def _compute_hash(self, record: Dict[str, Any]) -> str:
        record_copy = dict(record)
        record_copy.pop("audit_hash", None)
        record_bytes = json.dumps(record_copy, sort_keys=True).encode("utf-8")
        return hashlib.sha256(record_bytes).hexdigest()

COLLECTOR = TelemetryCollector()