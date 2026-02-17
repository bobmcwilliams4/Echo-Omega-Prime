import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict, field
from typing import Optional, List, Dict, Any, Deque
from collections import deque, defaultdict
from loguru import logger

ENGINE_ID = "AERO06"

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
        self.audit_writer = AuditTrailWriter()
        self._doctrine_total = 0
        self._doctrine_matched = 0
        self._latencies = deque(maxlen=maxlen)
        self._cache_hits = 0
        self._cache_total = 0
        self._modes = defaultdict(int)
        self._confidence_scores = []
        self._coverage = defaultdict(lambda: {"count": 0, "matched": 0})
        logger.info("TelemetryCollector initialized with maxlen={}", maxlen)

    def record_query(self, metrics: QueryMetrics):
        self.queries.append(metrics)
        self._latencies.append(metrics.latency_ms)
        self._cache_total += 1
        if metrics.cache_hit:
            self._cache_hits += 1
        self._doctrine_total += 1
        if metrics.doctrine_matched:
            self._doctrine_matched += 1
        self._modes[metrics.mode] += 1
        self._confidence_scores.append(metrics.confidence)
        self._coverage[metrics.mode]["count"] += 1
        if metrics.doctrine_matched:
            self._coverage[metrics.mode]["matched"] += 1
        if metrics.error:
            self.record_error(metrics.error, "Query error", metrics.query_id)
        self.audit_writer.write(metrics)
        logger.debug("Recorded query: {}", metrics)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "engine_id": ENGINE_ID,
            "timestamp": time.time()
        }
        self.errors.append(error_entry)
        logger.error("Error recorded: {}", error_entry)

    def get_latency_stats(self) -> Dict[str, float]:
        if not self._latencies:
            return {"avg": 0.0, "p50": 0.0, "p95": 0.0, "p99": 0.0, "min": 0.0, "max": 0.0}
        latencies = list(self._latencies)
        latencies.sort()
        avg = statistics.mean(latencies)
        min_v = latencies[0]
        max_v = latencies[-1]
        p50 = statistics.median(latencies)
        p95 = latencies[int(0.95 * len(latencies)) - 1]
        p99 = latencies[int(0.99 * len(latencies)) - 1]
        logger.debug("Latency stats computed")
        return {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_v,
            "max": max_v
        }

    def get_doctrine_hit_rate(self) -> float:
        if self._doctrine_total == 0:
            return 0.0
        hit_rate = self._doctrine_matched / self._doctrine_total
        logger.debug("Doctrine hit rate: {}", hit_rate)
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self.errors if e["timestamp"] >= window_start]
        queries_in_window = [q for q in self.queries if q.timestamp >= window_start]
        error_count = len(errors_in_window)
        query_count = len(queries_in_window)
        if query_count == 0:
            return 0.0
        error_rate = error_count / query_count
        logger.debug("Error rate over last {} hours: {}", window_hours, error_rate)
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self.queries if q.timestamp >= one_hour_ago)
        logger.debug("Queries in last hour: {}", count)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {}
        for mode, data in self._coverage.items():
            count = data["count"]
            matched = data["matched"]
            hit_rate = matched / count if count else 0.0
            report[mode] = {
                "total": count,
                "doctrine_matched": matched,
                "doctrine_hit_rate": hit_rate
            }
        logger.debug("Coverage report generated")
        return report

    def export_jsonl(self, path: str) -> int:
        p = pathlib.Path(path)
        count = 0
        with p.open("w", encoding="utf-8") as f:
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

    def write(self, metrics: QueryMetrics):
        date_str = time.strftime("%Y-%m-%d")
        file_path = self.base_dir / f"audit_{date_str}.jsonl"
        entry = asdict(metrics)
        entry["audit_id"] = self._generate_audit_id(metrics)
        with file_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        logger.debug("Audit entry written: {}", entry["audit_id"])

    def _generate_audit_id(self, metrics: QueryMetrics) -> str:
        base = f"{metrics.query_id}-{metrics.engine_id}-{metrics.timestamp}"
        return hashlib.sha256(base.encode()).hexdigest()

COLLECTOR = TelemetryCollector()