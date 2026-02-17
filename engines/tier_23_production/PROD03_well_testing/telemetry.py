import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any, Tuple
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "PROD03"

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
        self._queries: deque = deque(maxlen=maxlen)
        self._errors: deque = deque(maxlen=maxlen)
        self._doctrine_hits: deque = deque(maxlen=maxlen)
        self._latencies: deque = deque(maxlen=maxlen)
        self._coverage: Counter = Counter()
        self._audit_writer = AuditTrailWriter()
        self._query_ids: set = set()
        logger.info("TelemetryCollector initialized with maxlen={}", maxlen)

    def record_query(self, metrics: QueryMetrics):
        logger.debug("Recording query: {}", metrics)
        self._queries.append(metrics)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._coverage[metrics.mode] += 1
        self._query_ids.add(metrics.query_id)
        self._audit_writer.write(metrics)
        if metrics.error:
            self.record_error(metrics.error, "Query error", metrics.query_id)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "error_type": error_type,
            "message": message,
            "timestamp": time.time(),
            "query_id": query_id,
            "engine_id": ENGINE_ID
        }
        logger.warning("Recording error: {}", error_entry)
        self._errors.append(error_entry)
        self._audit_writer.write_error(error_entry)

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = list(self._latencies)
        logger.debug("Calculating latency stats for {} latencies", len(latencies))
        if not latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)
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
        logger.info("Latency stats: {}", stats)
        return stats

    def _percentile(self, data: List[float], percentile: float) -> float:
        if not data:
            return None
        data_sorted = sorted(data)
        k = (len(data_sorted) - 1) * (percentile / 100)
        f = int(k)
        c = int(k) + 1
        if c >= len(data_sorted):
            return data_sorted[-1]
        d0 = data_sorted[f]
        d1 = data_sorted[c]
        return d0 + (d1 - d0) * (k - f)

    def get_doctrine_hit_rate(self) -> float:
        total = len(self._doctrine_hits)
        hits = sum(1 for hit in self._doctrine_hits if hit)
        hit_rate = hits / total if total > 0 else 0.0
        logger.info("Doctrine hit rate: {:.3f} ({} hits / {} total)", hit_rate, hits, total)
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        queries_in_window = [q for q in self._queries if q.timestamp >= window_start]
        error_rate = len(errors_in_window) / len(queries_in_window) if queries_in_window else 0.0
        logger.info("Error rate in last {:.2f} hours: {:.3f}", window_hours, error_rate)
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        window_start = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= window_start)
        logger.info("Queries in last hour: {}", count)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        total = sum(self._coverage.values())
        report = {mode: count / total if total > 0 else 0.0 for mode, count in self._coverage.items()}
        logger.info("Coverage report: {}", report)
        return report

    def export_jsonl(self, path: str) -> int:
        p = pathlib.Path(path)
        logger.info("Exporting telemetry to JSONL: {}", p)
        count = 0
        with p.open("w", encoding="utf-8") as f:
            for q in self._queries:
                f.write(json.dumps(q.to_dict()) + "\n")
                count += 1
        logger.info("Exported {} queries to {}", count, p)
        return count

class AuditTrailWriter:
    def __init__(self, base_path: Optional[str] = None):
        self.base_path = base_path or "./audit_trail"
        self.path_obj = pathlib.Path(self.base_path)
        self.path_obj.mkdir(parents=True, exist_ok=True)
        logger.info("AuditTrailWriter initialized at {}", self.base_path)

    def _get_query_file(self, query_id: str) -> pathlib.Path:
        hash_id = hashlib.sha256(query_id.encode()).hexdigest()[:8]
        file_name = f"{ENGINE_ID}_query_{hash_id}.jsonl"
        return self.path_obj / file_name

    def write(self, metrics: QueryMetrics):
        file_path = self._get_query_file(metrics.query_id)
        logger.debug("Writing audit trail for query {} to {}", metrics.query_id, file_path)
        with file_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(metrics.to_dict()) + "\n")

    def write_error(self, error_entry: dict):
        query_id = error_entry.get("query_id", "unknown")
        file_path = self._get_query_file(query_id)
        logger.debug("Writing error audit trail for query {} to {}", query_id, file_path)
        with file_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(error_entry) + "\n")

COLLECTOR = TelemetryCollector(maxlen=10000)