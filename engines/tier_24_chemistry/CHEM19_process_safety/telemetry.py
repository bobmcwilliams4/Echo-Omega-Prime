import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any, Union
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "CHEM19"

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
        self._doctrine_hits: int = 0
        self._doctrine_total: int = 0
        self._latencies: List[float] = []
        self._query_counter: Counter = Counter()
        self._error_counter: Counter = Counter()
        self._coverage_modes: Counter = Counter()
        self._coverage_confidence: List[float] = []
        self._audit_writer: Optional[AuditTrailWriter] = None

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._latencies.append(metrics.latency_ms)
        self._query_counter[metrics.query_id] += 1
        self._coverage_modes[metrics.mode] += 1
        self._coverage_confidence.append(metrics.confidence)
        self._doctrine_total += 1
        if metrics.doctrine_matched:
            self._doctrine_hits += 1
        if metrics.error:
            self.record_error("query_error", metrics.error, metrics.query_id)
        if self._audit_writer:
            self._audit_writer.write(metrics)
        logger.debug(f"Recorded query: {metrics}")

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
        logger.error(f"Error recorded: {error_entry}")

    def get_latency_stats(self) -> Dict[str, Union[float, None]]:
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
        min_latency = latencies_sorted[0]
        max_latency = latencies_sorted[-1]
        p50 = statistics.median(latencies_sorted)
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
        if self._doctrine_total == 0:
            return 0.0
        return self._doctrine_hits / self._doctrine_total

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
        hour_ago = now - 3600
        return sum(1 for q in self._queries if q.timestamp >= hour_ago)

    def get_coverage_report(self) -> Dict[str, Any]:
        total_queries = len(self._queries)
        mode_counts = dict(self._coverage_modes)
        avg_confidence = statistics.mean(self._coverage_confidence) if self._coverage_confidence else None
        min_confidence = min(self._coverage_confidence) if self._coverage_confidence else None
        max_confidence = max(self._coverage_confidence) if self._coverage_confidence else None
        return {
            "total_queries": total_queries,
            "mode_counts": mode_counts,
            "avg_confidence": avg_confidence,
            "min_confidence": min_confidence,
            "max_confidence": max_confidence
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

    def set_audit_writer(self, writer: 'AuditTrailWriter'):
        self._audit_writer = writer

class AuditTrailWriter:
    def __init__(self, audit_path: Union[str, pathlib.Path]):
        self.audit_path = pathlib.Path(audit_path)
        self._ensure_path()

    def _ensure_path(self):
        if not self.audit_path.parent.exists():
            self.audit_path.parent.mkdir(parents=True, exist_ok=True)

    def write(self, metrics: QueryMetrics):
        entry = asdict(metrics)
        entry["audit_hash"] = self._hash_entry(entry)
        with self.audit_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        logger.debug(f"Audit trail written for query_id={metrics.query_id}")

    def _hash_entry(self, entry: Dict[str, Any]) -> str:
        entry_str = json.dumps(entry, sort_keys=True)
        return hashlib.sha256(entry_str.encode("utf-8")).hexdigest()

COLLECTOR = TelemetryCollector(max_queries=20000)