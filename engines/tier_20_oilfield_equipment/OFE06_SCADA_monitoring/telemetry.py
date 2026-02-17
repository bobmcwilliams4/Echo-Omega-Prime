import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any, Deque
import collections
from loguru import logger

ENGINE_ID = "OFE06"

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
    def __init__(self, engine_id: str):
        self.engine_id = engine_id
        self._queries: Deque[QueryMetrics] = collections.deque(maxlen=10000)
        self._errors: Deque[Dict[str, Any]] = collections.deque(maxlen=5000)
        self._doctrine_hits: Deque[bool] = collections.deque(maxlen=10000)
        self._latencies: Deque[float] = collections.deque(maxlen=10000)
        self._cache_hits: Deque[bool] = collections.deque(maxlen=10000)
        self._modes: Deque[str] = collections.deque(maxlen=10000)
        self._confidences: Deque[float] = collections.deque(maxlen=10000)
        self._query_timestamps: Deque[float] = collections.deque(maxlen=10000)
        self._audit_writer = AuditTrailWriter()
        logger.info(f"TelemetryCollector initialized for engine {engine_id}")

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._latencies.append(metrics.latency_ms)
        self._cache_hits.append(metrics.cache_hit)
        self._modes.append(metrics.mode)
        self._confidences.append(metrics.confidence)
        self._query_timestamps.append(metrics.timestamp)
        self._audit_writer.write(metrics)
        logger.debug(f"Recorded query: {metrics.query_id}")

    def record_error(self, error_type: str, message: str, query_id: Optional[str]):
        error_entry = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "timestamp": time.time(),
            "engine_id": self.engine_id
        }
        self._errors.append(error_entry)
        logger.error(f"Error recorded: {error_type} for query {query_id}: {message}")

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = list(self._latencies)
        if not latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies_sorted)
        p95 = latencies_sorted[int(len(latencies_sorted) * 0.95) - 1] if len(latencies_sorted) >= 1 else None
        p99 = latencies_sorted[int(len(latencies_sorted) * 0.99) - 1] if len(latencies_sorted) >= 1 else None
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
        logger.debug(f"Latency stats: {stats}")
        return stats

    def get_doctrine_hit_rate(self) -> float:
        hits = list(self._doctrine_hits)
        if not hits:
            return 0.0
        hit_rate = sum(hits) / len(hits)
        logger.debug(f"Doctrine hit rate: {hit_rate}")
        return hit_rate

    def get_error_rate(self, window_hours: float) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        queries_in_window = [t for t in self._query_timestamps if t >= window_start]
        error_rate = (len(errors_in_window) / len(queries_in_window)) if queries_in_window else 0.0
        logger.debug(f"Error rate in last {window_hours}h: {error_rate}")
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for t in self._query_timestamps if t >= one_hour_ago)
        logger.debug(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        mode_counts = collections.Counter(self._modes)
        doctrine_hits = sum(self._doctrine_hits)
        total = len(self._doctrine_hits)
        cache_hits = sum(self._cache_hits)
        confidences = list(self._confidences)
        avg_confidence = statistics.mean(confidences) if confidences else None
        report = {
            "total_queries": len(self._queries),
            "mode_counts": dict(mode_counts),
            "doctrine_hit_count": doctrine_hits,
            "doctrine_hit_rate": (doctrine_hits / total) if total else 0.0,
            "cache_hit_count": cache_hits,
            "cache_hit_rate": (cache_hits / total) if total else 0.0,
            "avg_confidence": avg_confidence
        }
        logger.debug(f"Coverage report: {report}")
        return report

    def export_jsonl(self, path: str) -> int:
        out_path = pathlib.Path(path)
        count = 0
        with out_path.open("w", encoding="utf-8") as f:
            for q in self._queries:
                f.write(json.dumps(asdict(q)) + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {out_path}")
        return count

class AuditTrailWriter:
    def __init__(self, base_dir: Optional[str] = None):
        if base_dir is None:
            base_dir = "./audit_trail"
        self.base_dir = pathlib.Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"AuditTrailWriter initialized at {self.base_dir}")

    def _get_audit_file(self, query_id: str) -> pathlib.Path:
        hash_digest = hashlib.sha256(query_id.encode()).hexdigest()
        subdir = self.base_dir / hash_digest[:2]
        subdir.mkdir(parents=True, exist_ok=True)
        file_path = subdir / f"{query_id}.jsonl"
        return file_path

    def write(self, metrics: QueryMetrics):
        file_path = self._get_audit_file(metrics.query_id)
        with file_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(metrics)) + "\n")
        logger.debug(f"Wrote audit trail for query {metrics.query_id} to {file_path}")

COLLECTOR = TelemetryCollector(ENGINE_ID)