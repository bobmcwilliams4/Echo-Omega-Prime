import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict, field
from typing import Optional, List, Dict, Any, Deque
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "ENT04"

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
        self._timestamps: Deque[float] = deque(maxlen=maxlen)
        self._query_ids: set = set()
        self._coverage_counter: Counter = Counter()
        self._audit_writer = AuditTrailWriter()
        logger.debug("TelemetryCollector initialized with maxlen={}", maxlen)

    def record_query(self, metrics: QueryMetrics):
        logger.debug("Recording query: {}", metrics)
        self._queries.append(metrics)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._latencies.append(metrics.latency_ms)
        self._cache_hits.append(metrics.cache_hit)
        self._modes.append(metrics.mode)
        self._confidences.append(metrics.confidence)
        self._timestamps.append(metrics.timestamp)
        self._query_ids.add(metrics.query_id)
        self._coverage_counter[metrics.mode] += 1
        self._audit_writer.write(metrics)
        if metrics.error:
            self.record_error(metrics.error, "Query error", metrics.query_id)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "engine_id": ENGINE_ID
        }
        logger.error("Recording error: {}", error_entry)
        self._errors.append(error_entry)
        self._audit_writer.write_error(error_entry)

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = list(self._latencies)
        logger.debug("Computing latency stats for {} entries", len(latencies))
        if not latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = latencies_sorted[int(0.95 * len(latencies_sorted)) - 1]
        p99 = latencies_sorted[int(0.99 * len(latencies_sorted)) - 1]
        min_latency = min(latencies)
        max_latency = max(latencies)
        stats = {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_latency,
            "max": max_latency
        }
        logger.debug("Latency stats: {}", stats)
        return stats

    def get_doctrine_hit_rate(self) -> float:
        total = len(self._doctrine_hits)
        hits = sum(self._doctrine_hits)
        logger.debug("Doctrine hit rate: {}/{}", hits, total)
        if total == 0:
            return 0.0
        return hits / total

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        error_count = sum(1 for e in self._errors if e["timestamp"] >= window_start)
        query_count = sum(1 for t in self._timestamps if t >= window_start)
        logger.debug("Error rate in last {} hours: {}/{}", window_hours, error_count, query_count)
        if query_count == 0:
            return 0.0
        return error_count / query_count

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for t in self._timestamps if t >= one_hour_ago)
        logger.debug("Queries in last hour: {}", count)
        return count

    def get_coverage_report(self) -> Dict[str, int]:
        logger.debug("Coverage report: {}", dict(self._coverage_counter))
        return dict(self._coverage_counter)

    def export_jsonl(self, path: str) -> int:
        path_obj = pathlib.Path(path)
        count = 0
        logger.info("Exporting telemetry to {}", path)
        with path_obj.open("w", encoding="utf-8") as f:
            for qm in self._queries:
                f.write(json.dumps(asdict(qm)) + "\n")
                count += 1
        logger.info("Exported {} telemetry records to {}", count, path)
        return count

class AuditTrailWriter:
    def __init__(self, base_dir: Optional[str] = None):
        if base_dir is None:
            base_dir = "./audit_trail"
        self.base_dir = pathlib.Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        logger.debug("AuditTrailWriter initialized at {}", self.base_dir)

    def _get_audit_path(self, query_id: str) -> pathlib.Path:
        # Use first 2 chars of hash as subdirectory for sharding
        h = hashlib.sha256(query_id.encode()).hexdigest()
        subdir = self.base_dir / h[:2]
        subdir.mkdir(parents=True, exist_ok=True)
        return subdir / f"{query_id}.jsonl"

    def write(self, metrics: QueryMetrics):
        path = self._get_audit_path(metrics.query_id)
        logger.debug("Writing audit trail for query_id={} to {}", metrics.query_id, path)
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(metrics)) + "\n")

    def write_error(self, error_entry: Dict[str, Any]):
        query_id = error_entry.get("query_id", "unknown")
        path = self._get_audit_path(query_id)
        logger.debug("Writing error audit trail for query_id={} to {}", query_id, path)
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"error": error_entry}) + "\n")

COLLECTOR = TelemetryCollector()