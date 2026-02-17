import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Tuple
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "MECH10"

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
    def __init__(self, engine_id: str = ENGINE_ID, max_queries: int = 10000):
        self.engine_id = engine_id
        self._queries: deque = deque(maxlen=max_queries)
        self._errors: deque = deque(maxlen=max_queries)
        self._doctrine_hits: deque = deque(maxlen=max_queries)
        self._latencies: deque = deque(maxlen=max_queries)
        self._coverage: defaultdict = defaultdict(lambda: {"count": 0, "doctrine_matched": 0, "cache_hit": 0})
        self._audit_writer = AuditTrailWriter()
        logger.info(f"TelemetryCollector initialized for engine {engine_id}")

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._coverage[metrics.mode]["count"] += 1
        if metrics.doctrine_matched:
            self._coverage[metrics.mode]["doctrine_matched"] += 1
        if metrics.cache_hit:
            self._coverage[metrics.mode]["cache_hit"] += 1
        self._audit_writer.write(metrics)
        logger.debug(f"Recorded query: {metrics.query_id}")

    def record_error(self, error_type: str, message: str, query_id: str):
        error_entry = {
            "timestamp": time.time(),
            "engine_id": self.engine_id,
            "error_type": error_type,
            "message": message,
            "query_id": query_id
        }
        self._errors.append(error_entry)
        logger.error(f"Error recorded: {error_type} for query {query_id}: {message}")

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = list(self._latencies)
        if not latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        min_latency = latencies_sorted[0]
        max_latency = latencies_sorted[-1]
        p50 = statistics.median(latencies_sorted)
        p95 = latencies_sorted[int(0.95 * len(latencies_sorted)) - 1]
        p99 = latencies_sorted[int(0.99 * len(latencies_sorted)) - 1]
        stats = {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_latency,
            "max": max_latency
        }
        logger.info(f"Latency stats: {stats}")
        return stats

    def get_doctrine_hit_rate(self) -> float:
        doctrine_hits = list(self._doctrine_hits)
        if not doctrine_hits:
            return 0.0
        hit_rate = sum(doctrine_hits) / len(doctrine_hits)
        logger.info(f"Doctrine hit rate: {hit_rate:.4f}")
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        error_count = sum(1 for e in self._errors if e["timestamp"] >= window_start)
        query_count = sum(1 for q in self._queries if q.timestamp >= window_start)
        if query_count == 0:
            return 0.0
        error_rate = error_count / query_count
        logger.info(f"Error rate for last {window_hours}h: {error_rate:.4f}")
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= one_hour_ago)
        logger.info(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {}
        for mode, stats in self._coverage.items():
            total = stats["count"]
            doctrine_matched = stats["doctrine_matched"]
            cache_hit = stats["cache_hit"]
            report[mode] = {
                "total": total,
                "doctrine_matched": doctrine_matched,
                "doctrine_match_rate": doctrine_matched / total if total > 0 else 0.0,
                "cache_hit": cache_hit,
                "cache_hit_rate": cache_hit / total if total > 0 else 0.0
            }
        logger.info(f"Coverage report: {report}")
        return report

    def export_jsonl(self, path: str) -> int:
        p = pathlib.Path(path)
        count = 0
        with p.open("w", encoding="utf-8") as f:
            for q in self._queries:
                f.write(json.dumps(dataclass_to_dict(q)) + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {path}")
        return count

def dataclass_to_dict(instance):
    if hasattr(instance, "__dataclass_fields__"):
        return {k: getattr(instance, k) for k in instance.__dataclass_fields__}
    return instance

class AuditTrailWriter:
    def __init__(self, base_path: str = "./audit_trail"):
        self.base_path = pathlib.Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"AuditTrailWriter initialized at {self.base_path}")

    def write(self, metrics: QueryMetrics):
        date_str = time.strftime("%Y-%m-%d")
        file_path = self.base_path / f"{ENGINE_ID}_audit_{date_str}.jsonl"
        entry = dataclass_to_dict(metrics)
        with file_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        logger.debug(f"Audit trail written for query {metrics.query_id}")

COLLECTOR = TelemetryCollector(engine_id=ENGINE_ID)