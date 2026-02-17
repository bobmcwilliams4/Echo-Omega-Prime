import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict, field
from typing import List, Optional, Dict, Any, Deque
import collections
from loguru import logger

ENGINE_ID = "RAIL03"

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
    def __init__(self):
        self._metrics: Deque[QueryMetrics] = collections.deque(maxlen=10000)
        self._errors: Deque[Dict[str, Any]] = collections.deque(maxlen=10000)
        self._audit_trail_writer = AuditTrailWriter()
        self._lock = collections.defaultdict(lambda: None)  # Dummy for future thread safety

    def record_query(self, metrics: QueryMetrics):
        logger.debug(f"Recording query: {metrics.query_id}")
        self._metrics.append(metrics)
        self._audit_trail_writer.write(metrics)
        if metrics.error:
            self.record_error(metrics.error, "Query error", metrics.query_id)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "timestamp": time.time(),
        }
        logger.error(f"Error recorded: {error_entry}")
        self._errors.append(error_entry)

    def get_latency_stats(self) -> Dict[str, float]:
        latencies = [m.latency_ms for m in self._metrics if m.latency_ms is not None]
        if not latencies:
            return {"avg": 0.0, "p50": 0.0, "p95": 0.0, "p99": 0.0, "min": 0.0, "max": 0.0}
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = latencies_sorted[int(0.95 * len(latencies_sorted)) - 1]
        p99 = latencies_sorted[int(0.99 * len(latencies_sorted)) - 1]
        min_latency = latencies_sorted[0]
        max_latency = latencies_sorted[-1]
        stats = {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_latency,
            "max": max_latency,
        }
        logger.debug(f"Latency stats: {stats}")
        return stats

    def get_doctrine_hit_rate(self) -> float:
        if not self._metrics:
            return 0.0
        doctrine_hits = sum(1 for m in self._metrics if m.doctrine_matched)
        hit_rate = doctrine_hits / len(self._metrics)
        logger.debug(f"Doctrine hit rate: {hit_rate}")
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        relevant_metrics = [m for m in self._metrics if m.timestamp >= window_start]
        if not relevant_metrics:
            return 0.0
        error_count = sum(1 for m in relevant_metrics if m.error)
        error_rate = error_count / len(relevant_metrics)
        logger.debug(f"Error rate over last {window_hours}h: {error_rate}")
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for m in self._metrics if m.timestamp >= one_hour_ago)
        logger.debug(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        total = len(self._metrics)
        if total == 0:
            return {
                "total": 0,
                "cache_hit": 0,
                "cache_hit_rate": 0.0,
                "doctrine_matched": 0,
                "doctrine_hit_rate": 0.0,
                "modes": {},
            }
        cache_hits = sum(1 for m in self._metrics if m.cache_hit)
        doctrine_hits = sum(1 for m in self._metrics if m.doctrine_matched)
        modes = collections.Counter(m.mode for m in self._metrics)
        report = {
            "total": total,
            "cache_hit": cache_hits,
            "cache_hit_rate": cache_hits / total,
            "doctrine_matched": doctrine_hits,
            "doctrine_hit_rate": doctrine_hits / total,
            "modes": dict(modes),
        }
        logger.debug(f"Coverage report: {report}")
        return report

    def export_jsonl(self, path: str) -> int:
        p = pathlib.Path(path)
        count = 0
        with p.open("w", encoding="utf-8") as f:
            for m in self._metrics:
                f.write(json.dumps(asdict(m)) + "\n")
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
        # Use first 2 chars of hash as subdirectory for sharding
        h = hashlib.sha1(query_id.encode("utf-8")).hexdigest()
        subdir = self.base_dir / h[:2]
        subdir.mkdir(parents=True, exist_ok=True)
        return subdir / f"{query_id}.jsonl"

    def write(self, metrics: QueryMetrics):
        path = self._get_audit_path(metrics.query_id)
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(metrics)) + "\n")
        logger.debug(f"Audit trail written for {metrics.query_id} at {path}")

COLLECTOR = TelemetryCollector()