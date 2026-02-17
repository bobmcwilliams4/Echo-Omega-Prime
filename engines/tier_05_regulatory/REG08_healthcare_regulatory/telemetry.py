import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "REG08"

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
    def __init__(self, max_queries: int = 10000, max_errors: int = 1000):
        self._queries: deque = deque(maxlen=max_queries)
        self._errors: deque = deque(maxlen=max_errors)
        self._doctrine_hits: deque = deque(maxlen=max_queries)
        self._query_ids: set = set()
        self._audit_writer = AuditTrailWriter()
        self._coverage: defaultdict = defaultdict(lambda: {"count": 0, "confidence": []})
        logger.info("TelemetryCollector initialized for engine {}", ENGINE_ID)

    def record_query(self, metrics: QueryMetrics):
        if metrics.query_id in self._query_ids:
            logger.warning("Duplicate query_id detected: {}", metrics.query_id)
            return
        self._queries.append(metrics)
        self._query_ids.add(metrics.query_id)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._coverage[metrics.mode]["count"] += 1
        self._coverage[metrics.mode]["confidence"].append(metrics.confidence)
        self._audit_writer.write(metrics)
        logger.debug("Recorded query: {}", metrics.query_id)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        err = {
            "timestamp": time.time(),
            "engine_id": ENGINE_ID,
            "error_type": error_type,
            "message": message,
            "query_id": query_id
        }
        self._errors.append(err)
        logger.error("Error recorded: {} | {}", error_type, message)

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = [q.latency_ms for q in self._queries if q.latency_ms is not None]
        if not latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = latencies_sorted[int(len(latencies_sorted) * 0.95) - 1] if len(latencies_sorted) >= 1 else None
        p99 = latencies_sorted[int(len(latencies_sorted) * 0.99) - 1] if len(latencies_sorted) >= 1 else None
        min_latency = min(latencies)
        max_latency = max(latencies)
        logger.info("Latency stats calculated: avg={}, p50={}, p95={}, p99={}, min={}, max={}", avg, p50, p95, p99, min_latency, max_latency)
        return {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_latency,
            "max": max_latency
        }

    def get_doctrine_hit_rate(self) -> float:
        total = len(self._doctrine_hits)
        if total == 0:
            return 0.0
        hits = sum(1 for hit in self._doctrine_hits if hit)
        hit_rate = hits / total
        logger.info("Doctrine hit rate: {}", hit_rate)
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        error_count = sum(1 for e in self._errors if e["timestamp"] >= window_start)
        query_count = sum(1 for q in self._queries if q.timestamp >= window_start)
        if query_count == 0:
            return 0.0
        error_rate = error_count / query_count
        logger.info("Error rate in last {} hours: {}", window_hours, error_rate)
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= one_hour_ago)
        logger.info("Queries in last hour: {}", count)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {}
        for mode, data in self._coverage.items():
            count = data["count"]
            confidences = data["confidence"]
            avg_conf = statistics.mean(confidences) if confidences else None
            min_conf = min(confidences) if confidences else None
            max_conf = max(confidences) if confidences else None
            report[mode] = {
                "count": count,
                "avg_confidence": avg_conf,
                "min_confidence": min_conf,
                "max_confidence": max_conf
            }
        logger.info("Coverage report generated")
        return report

    def export_jsonl(self, path: str) -> int:
        p = pathlib.Path(path)
        count = 0
        with p.open("w", encoding="utf-8") as f:
            for q in self._queries:
                f.write(json.dumps(asdict(q)) + "\n")
                count += 1
        logger.info("Exported {} queries to {}", count, path)
        return count

class AuditTrailWriter:
    def __init__(self, base_dir: str = "./audit_trail"):
        self.base_dir = pathlib.Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        logger.info("AuditTrailWriter initialized at {}", self.base_dir)

    def write(self, metrics: QueryMetrics):
        query_hash = hashlib.sha256(metrics.query_id.encode()).hexdigest()
        filename = f"{ENGINE_ID}_{query_hash}.jsonl"
        file_path = self.base_dir / filename
        with file_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(metrics)) + "\n")
        logger.debug("Audit trail written for query_id {}", metrics.query_id)

COLLECTOR = TelemetryCollector()