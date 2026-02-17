import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict, field
from typing import Optional, List, Dict, Any, Union
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "I05"

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
        self.metrics: deque[QueryMetrics] = deque(maxlen=maxlen)
        self.errors: deque[Dict[str, Any]] = deque(maxlen=maxlen)
        self.lock = None  # Placeholder for thread safety if needed
        self.audit_writer = AuditTrailWriter()
        self._doctrine_hits = 0
        self._doctrine_total = 0
        self._error_counter = Counter()
        self._query_times = deque(maxlen=maxlen)
        self._coverage_counter = Counter()
        self._cache_hits = 0
        self._cache_total = 0

    def record_query(self, metrics: QueryMetrics):
        self.metrics.append(metrics)
        self._query_times.append(metrics.timestamp)
        self._doctrine_total += 1
        if metrics.doctrine_matched:
            self._doctrine_hits += 1
        if metrics.cache_hit:
            self._cache_hits += 1
        self._cache_total += 1
        if metrics.error:
            self._error_counter[metrics.error] += 1
        self._coverage_counter[metrics.mode] += 1
        self.audit_writer.write(metrics)
        logger.debug(f"Recorded query: {metrics}")

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "engine_id": ENGINE_ID,
            "timestamp": time.time()
        }
        self.errors.append(error_entry)
        self._error_counter[error_type] += 1
        logger.error(f"Error recorded: {error_entry}")

    def get_latency_stats(self) -> Dict[str, float]:
        latencies = [m.latency_ms for m in self.metrics if m.latency_ms is not None]
        if not latencies:
            return {"avg": 0.0, "p50": 0.0, "p95": 0.0, "p99": 0.0, "min": 0.0, "max": 0.0}
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
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
        if self._doctrine_total == 0:
            return 0.0
        return self._doctrine_hits / self._doctrine_total

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        total = 0
        errors = 0
        for m in self.metrics:
            if m.timestamp >= window_start:
                total += 1
                if m.error:
                    errors += 1
        if total == 0:
            return 0.0
        return errors / total

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        return sum(1 for m in self.metrics if m.timestamp >= one_hour_ago)

    def get_coverage_report(self) -> Dict[str, Any]:
        total = sum(self._coverage_counter.values())
        if total == 0:
            return {}
        report = {}
        for mode, count in self._coverage_counter.items():
            report[mode] = {
                "count": count,
                "percent": (count / total) * 100
            }
        return report

    def export_jsonl(self, path: Union[str, pathlib.Path]) -> int:
        path = pathlib.Path(path)
        count = 0
        with path.open("w", encoding="utf-8") as f:
            for m in self.metrics:
                f.write(json.dumps(asdict(m)) + "\n")
                count += 1
        logger.info(f"Exported {count} metrics to {path}")
        return count

class AuditTrailWriter:
    def __init__(self, base_path: Optional[Union[str, pathlib.Path]] = None):
        if base_path is None:
            base_path = pathlib.Path("audit_trail")
        self.base_path = pathlib.Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def _get_audit_file(self, query_id: str) -> pathlib.Path:
        # Hash query_id for filesystem safety and sharding
        h = hashlib.sha256(query_id.encode()).hexdigest()[:8]
        subdir = self.base_path / h
        subdir.mkdir(parents=True, exist_ok=True)
        return subdir / f"{query_id}.jsonl"

    def write(self, metrics: QueryMetrics):
        audit_file = self._get_audit_file(metrics.query_id)
        with audit_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(metrics)) + "\n")
        logger.debug(f"Audit trail written for query {metrics.query_id} at {audit_file}")

COLLECTOR = TelemetryCollector()