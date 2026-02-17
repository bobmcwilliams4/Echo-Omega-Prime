import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any, Deque
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "MED09"

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

    def to_dict(self) -> dict:
        return asdict(self)

class TelemetryCollector:
    def __init__(self, maxlen: int = 10000):
        self.queries: Deque[QueryMetrics] = deque(maxlen=maxlen)
        self.errors: Deque[dict] = deque(maxlen=maxlen)
        self.latencies: Deque[float] = deque(maxlen=maxlen)
        self.doctrine_hits: Deque[bool] = deque(maxlen=maxlen)
        self.cache_hits: Deque[bool] = deque(maxlen=maxlen)
        self.confidences: Deque[float] = deque(maxlen=maxlen)
        self.modes: Deque[str] = deque(maxlen=maxlen)
        self.coverage: Counter = Counter()
        self.audit_writer = AuditTrailWriter()
        self._query_id_index: Dict[str, QueryMetrics] = {}
        self._lock = None  # For future thread safety

    def record_query(self, metrics: QueryMetrics):
        logger.debug(f"Recording query: {metrics.query_id}")
        self.queries.append(metrics)
        self.latencies.append(metrics.latency_ms)
        self.doctrine_hits.append(metrics.doctrine_matched)
        self.cache_hits.append(metrics.cache_hit)
        self.confidences.append(metrics.confidence)
        self.modes.append(metrics.mode)
        self.coverage[metrics.mode] += 1
        self._query_id_index[metrics.query_id] = metrics
        self.audit_writer.write(metrics)
        if metrics.error:
            self.record_error(metrics.error, "Error in query", metrics.query_id)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "engine_id": ENGINE_ID
        }
        logger.error(f"Error recorded: {error_entry}")
        self.errors.append(error_entry)

    def get_latency_stats(self) -> dict:
        if not self.latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        lats = list(self.latencies)
        lats.sort()
        avg = statistics.mean(lats)
        p50 = statistics.median(lats)
        p95 = lats[int(0.95 * len(lats)) - 1] if len(lats) >= 20 else lats[-1]
        p99 = lats[int(0.99 * len(lats)) - 1] if len(lats) >= 100 else lats[-1]
        min_lat = min(lats)
        max_lat = max(lats)
        return {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_lat,
            "max": max_lat
        }

    def get_doctrine_hit_rate(self) -> float:
        if not self.doctrine_hits:
            return 0.0
        hits = sum(1 for hit in self.doctrine_hits if hit)
        rate = hits / len(self.doctrine_hits)
        logger.debug(f"Doctrine hit rate: {rate:.3f}")
        return rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self.errors if e["timestamp"] >= window_start]
        queries_in_window = [q for q in self.queries if q.timestamp >= window_start]
        if not queries_in_window:
            return 0.0
        rate = len(errors_in_window) / len(queries_in_window)
        logger.debug(f"Error rate in last {window_hours}h: {rate:.3f}")
        return rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self.queries if q.timestamp >= one_hour_ago)
        logger.debug(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> dict:
        total = sum(self.coverage.values())
        report = {}
        for mode, count in self.coverage.items():
            report[mode] = {
                "count": count,
                "percent": (count / total) * 100 if total else 0.0
            }
        logger.debug(f"Coverage report: {report}")
        return report

    def export_jsonl(self, path: str) -> int:
        p = pathlib.Path(path)
        count = 0
        with p.open("w", encoding="utf-8") as f:
            for q in self.queries:
                f.write(json.dumps(q.to_dict()) + "\n")
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
        # Hash for subdir sharding
        h = hashlib.sha1(query_id.encode()).hexdigest()[:2]
        subdir = self.base_dir / h
        subdir.mkdir(parents=True, exist_ok=True)
        return subdir / f"{query_id}.jsonl"

    def write(self, metrics: QueryMetrics):
        path = self._get_audit_path(metrics.query_id)
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(metrics.to_dict()) + "\n")
        logger.debug(f"Wrote audit trail for query {metrics.query_id} to {path}")

COLLECTOR = TelemetryCollector()