import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional, Any, Deque
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "AUTO02"


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
        self.doctrine_hits: int = 0
        self.doctrine_total: int = 0
        self.cache_hits: int = 0
        self.cache_total: int = 0
        self.mode_counter: Counter = Counter()
        self.confidences: List[float] = []
        self.coverage: Dict[str, int] = defaultdict(int)
        self.audit_writer = AuditTrailWriter()
        logger.info("TelemetryCollector initialized for ENGINE_ID={}", ENGINE_ID)

    def record_query(self, metrics: QueryMetrics):
        self.queries.append(metrics)
        if metrics.doctrine_matched:
            self.doctrine_hits += 1
        self.doctrine_total += 1
        if metrics.cache_hit:
            self.cache_hits += 1
        self.cache_total += 1
        self.mode_counter[metrics.mode] += 1
        self.confidences.append(metrics.confidence)
        self.coverage[metrics.mode] += 1
        self.audit_writer.write(metrics)
        logger.debug("Recorded query: {}", metrics)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "engine_id": ENGINE_ID
        }
        self.errors.append(error_entry)
        logger.error("Error recorded: {}", error_entry)

    def get_latency_stats(self) -> Dict[str, float]:
        latencies = [q.latency_ms for q in self.queries if q.latency_ms is not None]
        if not latencies:
            return {"avg": 0, "p50": 0, "p95": 0, "p99": 0, "min": 0, "max": 0}
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = latencies_sorted[int(0.95 * len(latencies_sorted)) - 1]
        p99 = latencies_sorted[int(0.99 * len(latencies_sorted)) - 1]
        min_v = min(latencies)
        max_v = max(latencies)
        logger.info("Latency stats computed: avg={}, p50={}, p95={}, p99={}, min={}, max={}", avg, p50, p95, p99, min_v, max_v)
        return {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_v,
            "max": max_v
        }

    def get_doctrine_hit_rate(self) -> float:
        if self.doctrine_total == 0:
            return 0.0
        rate = self.doctrine_hits / self.doctrine_total
        logger.info("Doctrine hit rate: {}", rate)
        return rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self.errors if e["timestamp"] >= window_start]
        queries_in_window = [q for q in self.queries if q.timestamp >= window_start]
        if not queries_in_window:
            return 0.0
        rate = len(errors_in_window) / len(queries_in_window)
        logger.info("Error rate in last {} hours: {}", window_hours, rate)
        return rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self.queries if q.timestamp >= one_hour_ago)
        logger.info("Queries in last hour: {}", count)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {
            "total_queries": len(self.queries),
            "modes": dict(self.mode_counter),
            "avg_confidence": statistics.mean(self.confidences) if self.confidences else 0,
            "min_confidence": min(self.confidences) if self.confidences else 0,
            "max_confidence": max(self.confidences) if self.confidences else 0,
            "doctrine_hit_rate": self.get_doctrine_hit_rate(),
            "cache_hit_rate": (self.cache_hits / self.cache_total) if self.cache_total else 0,
        }
        logger.info("Coverage report generated: {}", report)
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
            base_dir = "./audit_trails"
        self.base_dir = pathlib.Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        logger.info("AuditTrailWriter initialized at {}", self.base_dir)

    def write(self, metrics: QueryMetrics):
        audit_entry = asdict(metrics)
        audit_entry["audit_timestamp"] = time.time()
        file_name = self._get_audit_file_name(metrics.query_id)
        file_path = self.base_dir / file_name
        with file_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(audit_entry) + "\n")
        logger.debug("Audit trail written for query_id={} at {}", metrics.query_id, file_path)

    def _get_audit_file_name(self, query_id: str) -> str:
        # Use a hash of the query_id to avoid file system issues
        h = hashlib.sha1(query_id.encode("utf-8")).hexdigest()
        return f"audit_{h[:8]}.jsonl"


COLLECTOR = TelemetryCollector()