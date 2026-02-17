import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict, field
from typing import Optional, List, Dict, Any, Deque
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "AUTO04"

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

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

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
        self._query_ids: set = set()
        self._audit_writer = AuditTrailWriter()
        logger.debug("TelemetryCollector initialized with maxlen={}", maxlen)

    def record_query(self, metrics: QueryMetrics):
        if metrics.query_id in self._query_ids:
            logger.warning("Duplicate query_id detected: {}", metrics.query_id)
            return
        self._queries.append(metrics)
        self._query_ids.add(metrics.query_id)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._latencies.append(metrics.latency_ms)
        self._cache_hits.append(metrics.cache_hit)
        self._modes.append(metrics.mode)
        self._confidences.append(metrics.confidence)
        self._query_timestamps.append(metrics.timestamp)
        self._audit_writer.write(metrics)
        logger.info("Recorded query: {}", metrics.query_id)
        if metrics.error:
            self.record_error(metrics.error, "Query error", metrics.query_id)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "engine_id": ENGINE_ID,
            "error_type": error_type,
            "message": message,
            "query_id": query_id
        }
        self._errors.append(error_entry)
        logger.error("Recorded error: {} for query_id={}", error_type, query_id)

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = list(self._latencies)
        if not latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        latencies.sort()
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = latencies[int(0.95 * len(latencies)) - 1]
        p99 = latencies[int(0.99 * len(latencies)) - 1]
        min_latency = latencies[0]
        max_latency = latencies[-1]
        stats = {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_latency,
            "max": max_latency
        }
        logger.debug("Latency stats computed: {}", stats)
        return stats

    def get_doctrine_hit_rate(self) -> float:
        hits = list(self._doctrine_hits)
        if not hits:
            return 0.0
        rate = sum(hits) / len(hits)
        logger.debug("Doctrine hit rate: {:.3f}", rate)
        return rate

    def get_error_rate(self, window_hours: float) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        error_count = 0
        query_count = 0
        for metrics in self._queries:
            if metrics.timestamp >= window_start:
                query_count += 1
                if metrics.error:
                    error_count += 1
        if query_count == 0:
            return 0.0
        rate = error_count / query_count
        logger.debug("Error rate over last {:.2f} hours: {:.3f}", window_hours, rate)
        return rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for ts in self._query_timestamps if ts >= one_hour_ago)
        logger.debug("Queries in last hour: {}", count)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        mode_counter = Counter(self._modes)
        cache_hit_counter = Counter(self._cache_hits)
        doctrine_counter = Counter(self._doctrine_hits)
        confidence_values = list(self._confidences)
        coverage = {
            "total_queries": len(self._queries),
            "modes": dict(mode_counter),
            "cache_hits": dict(cache_hit_counter),
            "doctrine_matched": dict(doctrine_counter),
            "confidence_avg": statistics.mean(confidence_values) if confidence_values else None,
            "confidence_min": min(confidence_values) if confidence_values else None,
            "confidence_max": max(confidence_values) if confidence_values else None,
        }
        logger.debug("Coverage report: {}", coverage)
        return coverage

    def export_jsonl(self, path: str) -> int:
        path_obj = pathlib.Path(path)
        count = 0
        with path_obj.open("w", encoding="utf-8") as f:
            for metrics in self._queries:
                f.write(json.dumps(metrics.to_dict(), ensure_ascii=False) + "\n")
                count += 1
        logger.info("Exported {} queries to {}", count, path)
        return count

class AuditTrailWriter:
    def __init__(self, base_path: Optional[str] = None):
        if base_path is None:
            base_path = "./audit_trail"
        self.base_path = pathlib.Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        logger.debug("AuditTrailWriter initialized at {}", self.base_path)

    def _get_audit_path(self, query_id: str) -> pathlib.Path:
        hash_digest = hashlib.sha256(query_id.encode("utf-8")).hexdigest()
        subdir = self.base_path / hash_digest[:2]
        subdir.mkdir(parents=True, exist_ok=True)
        filename = f"{query_id}.jsonl"
        return subdir / filename

    def write(self, metrics: QueryMetrics):
        path = self._get_audit_path(metrics.query_id)
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(metrics.to_dict(), ensure_ascii=False) + "\n")
        logger.debug("Wrote audit trail for query_id={} at {}", metrics.query_id, path)

COLLECTOR = TelemetryCollector()