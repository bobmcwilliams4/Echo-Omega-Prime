import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict, field
from typing import Optional, List, Dict, Any
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "MECH08"

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
    def __init__(self, maxlen=10000):
        self.queries = deque(maxlen=maxlen)
        self.errors = deque(maxlen=maxlen)
        self.latencies = deque(maxlen=maxlen)
        self.doctrine_matches = deque(maxlen=maxlen)
        self.cache_hits = deque(maxlen=maxlen)
        self.confidences = deque(maxlen=maxlen)
        self.modes = deque(maxlen=maxlen)
        self.coverage = defaultdict(lambda: {"count": 0, "doctrine_matched": 0})
        self.audit_writer = AuditTrailWriter()
        self.query_id_set = set()
        logger.info("TelemetryCollector initialized with maxlen={}", maxlen)

    def record_query(self, metrics: QueryMetrics):
        self.queries.append(metrics)
        self.latencies.append(metrics.latency_ms)
        self.doctrine_matches.append(metrics.doctrine_matched)
        self.cache_hits.append(metrics.cache_hit)
        self.confidences.append(metrics.confidence)
        self.modes.append(metrics.mode)
        self.coverage[metrics.mode]["count"] += 1
        if metrics.doctrine_matched:
            self.coverage[metrics.mode]["doctrine_matched"] += 1
        self.query_id_set.add(metrics.query_id)
        self.audit_writer.write(metrics)
        logger.debug("Recorded query: {}", metrics)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "error_type": error_type,
            "message": message,
            "query_id": query_id
        }
        self.errors.append(error_entry)
        logger.error("Error recorded: {}", error_entry)

    def get_latency_stats(self) -> Dict[str, Any]:
        if not self.latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        lat = list(self.latencies)
        lat.sort()
        avg = statistics.mean(lat)
        p50 = statistics.median(lat)
        p95 = lat[int(0.95 * len(lat)) - 1]
        p99 = lat[int(0.99 * len(lat)) - 1]
        min_v = lat[0]
        max_v = lat[-1]
        stats = {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_v,
            "max": max_v
        }
        logger.debug("Latency stats: {}", stats)
        return stats

    def get_doctrine_hit_rate(self) -> float:
        if not self.doctrine_matches:
            return 0.0
        hit_rate = sum(self.doctrine_matches) / len(self.doctrine_matches)
        logger.debug("Doctrine hit rate: {}", hit_rate)
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self.errors if e["timestamp"] >= window_start]
        queries_in_window = [q for q in self.queries if q.timestamp >= window_start]
        error_rate = len(errors_in_window) / max(1, len(queries_in_window))
        logger.debug("Error rate ({}h window): {}", window_hours, error_rate)
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self.queries if q.timestamp >= one_hour_ago)
        logger.debug("Queries in last hour: {}", count)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {}
        for mode, stats in self.coverage.items():
            total = stats["count"]
            doctrine = stats["doctrine_matched"]
            report[mode] = {
                "count": total,
                "doctrine_matched": doctrine,
                "doctrine_rate": doctrine / total if total else 0.0
            }
        logger.debug("Coverage report: {}", report)
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
    def __init__(self, base_dir="audit_trail"):
        self.base_dir = pathlib.Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        logger.info("AuditTrailWriter initialized at {}", self.base_dir)

    def write(self, metrics: QueryMetrics):
        # Use hash of query_id for filename
        query_hash = hashlib.sha256(metrics.query_id.encode()).hexdigest()
        fname = f"{metrics.engine_id}_{query_hash}.jsonl"
        path = self.base_dir / fname
        data = asdict(metrics)
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(data) + "\n")
        logger.debug("Audit trail written for query_id {}: {}", metrics.query_id, path)

COLLECTOR = TelemetryCollector()