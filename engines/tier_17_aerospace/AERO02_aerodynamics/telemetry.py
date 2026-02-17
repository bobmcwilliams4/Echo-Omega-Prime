import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict, field
from typing import List, Optional, Dict, Any, Deque
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "AERO02"

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
        self._queries: Deque[QueryMetrics] = deque(maxlen=maxlen)
        self._errors: Deque[Dict[str, Any]] = deque(maxlen=maxlen)
        self._doctrine_hits: Deque[bool] = deque(maxlen=maxlen)
        self._latencies: Deque[float] = deque(maxlen=maxlen)
        self._cache_hits: Deque[bool] = deque(maxlen=maxlen)
        self._modes: Deque[str] = deque(maxlen=maxlen)
        self._confidences: Deque[float] = deque(maxlen=maxlen)
        self._query_timestamps: Deque[float] = deque(maxlen=maxlen)
        self._error_timestamps: Deque[float] = deque(maxlen=maxlen)
        self._coverage_counter: Counter = Counter()
        self._audit_writer = AuditTrailWriter()
        self._lock = None  # Placeholder for threading.Lock if needed

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._cache_hits.append(metrics.cache_hit)
        self._modes.append(metrics.mode)
        self._confidences.append(metrics.confidence)
        self._query_timestamps.append(metrics.timestamp)
        if metrics.error:
            self.record_error(metrics.error, "Query error", metrics.query_id)
        self._coverage_counter[metrics.mode] += 1
        self._audit_writer.write(metrics)
        logger.debug(f"Recorded query: {metrics}")

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        err = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "timestamp": time.time()
        }
        self._errors.append(err)
        self._error_timestamps.append(err["timestamp"])
        logger.error(f"Error recorded: {err}")

    def get_latency_stats(self) -> Dict[str, Optional[float]]:
        if not self._latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        lat_sorted = sorted(self._latencies)
        n = len(lat_sorted)
        avg = statistics.mean(lat_sorted)
        p50 = lat_sorted[int(0.5 * n) - 1]
        p95 = lat_sorted[int(0.95 * n) - 1]
        p99 = lat_sorted[int(0.99 * n) - 1]
        minv = lat_sorted[0]
        maxv = lat_sorted[-1]
        return {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": minv,
            "max": maxv
        }

    def get_doctrine_hit_rate(self) -> Optional[float]:
        if not self._doctrine_hits:
            return None
        hit_count = sum(self._doctrine_hits)
        total = len(self._doctrine_hits)
        return hit_count / total if total else None

    def get_error_rate(self, window_hours: float = 1.0) -> Optional[float]:
        now = time.time()
        window_start = now - window_hours * 3600
        query_count = sum(1 for t in self._query_timestamps if t >= window_start)
        error_count = sum(1 for t in self._error_timestamps if t >= window_start)
        if query_count == 0:
            return None
        return error_count / query_count

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        return sum(1 for t in self._query_timestamps if t >= one_hour_ago)

    def get_coverage_report(self) -> Dict[str, Any]:
        total = sum(self._coverage_counter.values())
        if total == 0:
            return {"total": 0, "by_mode": {}, "coverage": {}}
        by_mode = dict(self._coverage_counter)
        coverage = {mode: count / total for mode, count in by_mode.items()}
        return {
            "total": total,
            "by_mode": by_mode,
            "coverage": coverage
        }

    def export_jsonl(self, path: str) -> int:
        p = pathlib.Path(path)
        count = 0
        with p.open("w", encoding="utf-8") as f:
            for q in self._queries:
                f.write(json.dumps(asdict(q)) + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {path}")
        return count

class AuditTrailWriter:
    def __init__(self, base_dir: Optional[str] = None):
        if base_dir is None:
            base_dir = "./audit_trail"
        self.base_dir = pathlib.Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _get_audit_path(self, query_id: str) -> pathlib.Path:
        h = hashlib.sha256(query_id.encode("utf-8")).hexdigest()
        subdir = self.base_dir / h[:2]
        subdir.mkdir(parents=True, exist_ok=True)
        return subdir / f"{query_id}.jsonl"

    def write(self, metrics: QueryMetrics):
        path = self._get_audit_path(metrics.query_id)
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(metrics)) + "\n")
        logger.debug(f"Wrote audit trail for query_id={metrics.query_id} to {path}")

COLLECTOR = TelemetryCollector()