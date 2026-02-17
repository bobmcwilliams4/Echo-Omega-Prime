import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict, field
from typing import Optional, List, Dict, Any, Deque
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "OFE11"

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
        self._query_ids: set = set()
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
        self._query_timestamps.append(metrics.timestamp)
        self._query_ids.add(metrics.query_id)
        self._audit_writer.write(metrics)
        if metrics.error:
            self.record_error(metrics.error, "Query error", metrics.query_id)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "timestamp": time.time(),
            "engine_id": ENGINE_ID
        }
        logger.error("Recording error: {}", error_entry)
        self._errors.append(error_entry)
        self._audit_writer.write_error(error_entry)

    def get_latency_stats(self) -> Dict[str, float]:
        latencies = list(self._latencies)
        if not latencies:
            logger.warning("No latencies recorded")
            return {"avg": 0.0, "p50": 0.0, "p95": 0.0, "p99": 0.0, "min": 0.0, "max": 0.0}
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        latencies_sorted = sorted(latencies)
        def percentile(p):
            k = int(len(latencies_sorted) * p / 100)
            k = min(max(k, 0), len(latencies_sorted) - 1)
            return latencies_sorted[k]
        p95 = percentile(95)
        p99 = percentile(99)
        min_latency = latencies_sorted[0]
        max_latency = latencies_sorted[-1]
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
        hits = list(self._doctrine_hits)
        if not hits:
            logger.warning("No doctrine hits recorded")
            return 0.0
        hit_rate = sum(hits) / len(hits)
        logger.debug("Doctrine hit rate: {}", hit_rate)
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
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
            logger.warning("No queries in error rate window")
            return 0.0
        error_rate = error_count / query_count
        logger.debug("Error rate over last {} hours: {}", window_hours, error_rate)
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = 0
        for ts in self._query_timestamps:
            if ts >= one_hour_ago:
                count += 1
        logger.debug("Queries in last hour: {}", count)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        mode_counter = Counter(self._modes)
        cache_hit_counter = Counter(self._cache_hits)
        doctrine_counter = Counter(self._doctrine_hits)
        confidence_list = list(self._confidences)
        avg_confidence = statistics.mean(confidence_list) if confidence_list else 0.0
        report = {
            "total_queries": len(self._queries),
            "modes": dict(mode_counter),
            "cache_hits": dict(cache_hit_counter),
            "doctrine_matched": dict(doctrine_counter),
            "avg_confidence": avg_confidence,
            "unique_queries": len(self._query_ids)
        }
        logger.debug("Coverage report: {}", report)
        return report

    def export_jsonl(self, path: str) -> int:
        output_path = pathlib.Path(path)
        count = 0
        with output_path.open("w", encoding="utf-8") as f:
            for metrics in self._queries:
                json_line = json.dumps(asdict(metrics))
                f.write(json_line + "\n")
                count += 1
        logger.info("Exported {} queries to {}", count, path)
        return count

class AuditTrailWriter:
    def __init__(self, base_dir: Optional[str] = None):
        if base_dir is None:
            base_dir = "./audit_trail"
        self.base_dir = pathlib.Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        logger.debug("AuditTrailWriter initialized at {}", self.base_dir)

    def _get_audit_path(self, query_id: str) -> pathlib.Path:
        hash_digest = hashlib.sha256(query_id.encode("utf-8")).hexdigest()
        subdir = self.base_dir / hash_digest[:2]
        subdir.mkdir(parents=True, exist_ok=True)
        return subdir / f"{query_id}.jsonl"

    def write(self, metrics: QueryMetrics):
        path = self._get_audit_path(metrics.query_id)
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(metrics)) + "\n")
        logger.debug("Wrote audit trail for query_id={} at {}", metrics.query_id, path)

    def write_error(self, error_entry: Dict[str, Any]):
        query_id = error_entry.get("query_id") or "unknown"
        path = self._get_audit_path(query_id)
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"error": error_entry}) + "\n")
        logger.debug("Wrote error audit trail for query_id={} at {}", query_id, path)

COLLECTOR = TelemetryCollector()