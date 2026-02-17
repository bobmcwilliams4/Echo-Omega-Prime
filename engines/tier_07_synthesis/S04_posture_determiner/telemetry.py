import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict, field
from typing import List, Optional, Dict, Any, Deque
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "S04"


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
        self.queries: Deque[QueryMetrics] = deque(maxlen=maxlen)
        self.errors: Deque[Dict[str, Any]] = deque(maxlen=maxlen)
        self.latencies: Deque[float] = deque(maxlen=maxlen)
        self.doctrine_hits: Deque[bool] = deque(maxlen=maxlen)
        self.cache_hits: Deque[bool] = deque(maxlen=maxlen)
        self.modes: Deque[str] = deque(maxlen=maxlen)
        self.confidences: Deque[float] = deque(maxlen=maxlen)
        self.coverage: Counter = Counter()
        self.audit_writer = AuditTrailWriter()
        self._query_id_set = set()
        logger.info("TelemetryCollector initialized for engine {}", ENGINE_ID)

    def record_query(self, metrics: QueryMetrics):
        if metrics.query_id in self._query_id_set:
            logger.warning("Duplicate query_id detected: {}", metrics.query_id)
            return
        self._query_id_set.add(metrics.query_id)
        self.queries.append(metrics)
        self.latencies.append(metrics.latency_ms)
        self.doctrine_hits.append(metrics.doctrine_matched)
        self.cache_hits.append(metrics.cache_hit)
        self.modes.append(metrics.mode)
        self.confidences.append(metrics.confidence)
        self.coverage[metrics.mode] += 1
        if metrics.error:
            self.errors.append({
                "timestamp": metrics.timestamp,
                "query_id": metrics.query_id,
                "error": metrics.error,
                "engine_id": metrics.engine_id,
            })
        self.audit_writer.write(metrics)
        logger.debug("Recorded query: {}", metrics.query_id)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "engine_id": ENGINE_ID,
        }
        self.errors.append(error_entry)
        logger.error("Error recorded: {} | Query: {} | Msg: {}", error_type, query_id, message)

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = list(self.latencies)
        if not latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = latencies_sorted[int(0.95 * len(latencies_sorted)) - 1]
        p99 = latencies_sorted[int(0.99 * len(latencies_sorted)) - 1]
        min_v = latencies_sorted[0]
        max_v = latencies_sorted[-1]
        return {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_v,
            "max": max_v,
        }

    def get_doctrine_hit_rate(self) -> float:
        hits = list(self.doctrine_hits)
        if not hits:
            return 0.0
        hit_rate = sum(hits) / len(hits)
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        queries_in_window = [q for q in self.queries if q.timestamp >= window_start]
        errors_in_window = [e for e in self.errors if e["timestamp"] >= window_start]
        total = len(queries_in_window)
        if total == 0:
            return 0.0
        error_rate = len(errors_in_window) / total
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self.queries if q.timestamp >= one_hour_ago)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        total = sum(self.coverage.values())
        if total == 0:
            return {}
        report = {}
        for mode, count in self.coverage.items():
            report[mode] = {
                "count": count,
                "pct": 100.0 * count / total
            }
        return report

    def export_jsonl(self, path: str) -> int:
        path_obj = pathlib.Path(path)
        count = 0
        with path_obj.open("w", encoding="utf-8") as f:
            for q in self.queries:
                f.write(json.dumps(asdict(q)) + "\n")
                count += 1
        logger.info("Exported {} queries to {}", count, path)
        return count


class AuditTrailWriter:
    def __init__(self, base_dir: Optional[str] = None):
        if base_dir is None:
            base_dir = "./audit_trail"
        self.base_dir = pathlib.Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        logger.info("AuditTrailWriter initialized at {}", self.base_dir)

    def _get_audit_path(self, query_id: str) -> pathlib.Path:
        # Use first 2 chars of hash for sharding
        h = hashlib.sha256(query_id.encode()).hexdigest()
        shard = h[:2]
        dir_path = self.base_dir / shard
        dir_path.mkdir(parents=True, exist_ok=True)
        return dir_path / f"{query_id}.jsonl"

    def write(self, metrics: QueryMetrics):
        path = self._get_audit_path(metrics.query_id)
        entry = asdict(metrics)
        entry["audit_timestamp"] = time.time()
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        logger.debug("Audit written for query {}", metrics.query_id)


COLLECTOR = TelemetryCollector()