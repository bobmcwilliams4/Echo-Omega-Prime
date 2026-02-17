import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any, Union
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "RAIL08"

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
        self.metrics: deque = deque(maxlen=max_queries)
        self.errors: deque = deque(maxlen=max_queries)
        self.audit_trail_writer = AuditTrailWriter()
        self._query_counter = Counter()
        self._doctrine_counter = Counter()
        self._cache_counter = Counter()
        self._mode_counter = Counter()
        self._confidence_values = []
        self._error_counter = Counter()
        self._coverage_counter = defaultdict(set)
        self._last_exported = 0

    def record_query(self, metrics: QueryMetrics):
        self.metrics.append(metrics)
        self._query_counter[metrics.query_id] += 1
        self._doctrine_counter[metrics.doctrine_matched] += 1
        self._cache_counter[metrics.cache_hit] += 1
        self._mode_counter[metrics.mode] += 1
        self._confidence_values.append(metrics.confidence)
        if metrics.error:
            self._error_counter[metrics.error] += 1
            self.errors.append({
                "query_id": metrics.query_id,
                "engine_id": metrics.engine_id,
                "timestamp": metrics.timestamp,
                "error": metrics.error
            })
        self._coverage_counter[metrics.mode].add(metrics.query_id)
        self.audit_trail_writer.write(metrics)

    def record_error(self, error_type: str, message: str, query_id: str):
        timestamp = time.time()
        error_record = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "engine_id": ENGINE_ID,
            "timestamp": timestamp
        }
        self.errors.append(error_record)
        self._error_counter[error_type] += 1
        logger.error(f"[{ENGINE_ID}] Error recorded: {error_type} - {message} (query_id={query_id})")

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = [m.latency_ms for m in self.metrics if m.latency_ms is not None]
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
        p95 = latencies_sorted[int(len(latencies_sorted) * 0.95)-1]
        p99 = latencies_sorted[int(len(latencies_sorted) * 0.99)-1]
        min_latency = min(latencies_sorted)
        max_latency = max(latencies_sorted)
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
        total_queries = sum(1 for m in self.metrics if m.timestamp >= window_start)
        total_errors = sum(1 for e in self.errors if e["timestamp"] >= window_start)
        if total_queries == 0:
            return 0.0
        return total_errors / total_queries

    def queries_last_hour(self) -> int:
        now = time.time()
        hour_ago = now - 3600
        return sum(1 for m in self.metrics if m.timestamp >= hour_ago)

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {}
        for mode, queries in self._coverage_counter.items():
            report[mode] = {
                "unique_queries": len(queries),
                "coverage_percent": (len(queries) / max(1, len(self.metrics))) * 100
            }
        return report

    def export_jsonl(self, path: Union[str, pathlib.Path]) -> int:
        path = pathlib.Path(path)
        exported = 0
        try:
            with path.open("a", encoding="utf-8") as f:
                for m in self.metrics:
                    f.write(json.dumps(asdict(m)) + "\n")
                    exported += 1
            self._last_exported = time.time()
            logger.info(f"[{ENGINE_ID}] Exported {exported} query metrics to {path}")
        except Exception as e:
            logger.error(f"[{ENGINE_ID}] Failed to export metrics: {e}")
        return exported

class AuditTrailWriter:
    def __init__(self, audit_dir: Union[str, pathlib.Path] = "audit_trails"):
        self.audit_dir = pathlib.Path(audit_dir)
        self.audit_dir.mkdir(parents=True, exist_ok=True)

    def write(self, metrics: QueryMetrics):
        try:
            audit_path = self._get_audit_path(metrics.query_id)
            with audit_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(asdict(metrics)) + "\n")
            logger.debug(f"[{ENGINE_ID}] Audit trail written for query_id={metrics.query_id}")
        except Exception as e:
            logger.error(f"[{ENGINE_ID}] Failed to write audit trail: {e}")

    def _get_audit_path(self, query_id: str) -> pathlib.Path:
        hash_digest = hashlib.sha256(query_id.encode()).hexdigest()[:8]
        filename = f"{ENGINE_ID}_audit_{hash_digest}.jsonl"
        return self.audit_dir / filename

COLLECTOR = TelemetryCollector()