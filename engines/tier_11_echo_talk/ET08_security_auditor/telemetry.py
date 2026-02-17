import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "ET08"

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
        self._queries = deque(maxlen=max_queries)
        self._errors = deque(maxlen=max_queries)
        self._doctrine_hits = deque(maxlen=max_queries)
        self._latencies = deque(maxlen=max_queries)
        self._query_ids = set()
        self._audit_trail_writer = AuditTrailWriter()
        logger.info(f"TelemetryCollector initialized for engine_id={engine_id}")

    def record_query(self, metrics: QueryMetrics):
        if metrics.query_id in self._query_ids:
            logger.warning(f"Duplicate query_id detected: {metrics.query_id}")
            return
        self._queries.append(metrics)
        self._query_ids.add(metrics.query_id)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_hits.append(metrics.doctrine_matched)
        if metrics.error:
            self.record_error("query_error", metrics.error, metrics.query_id)
        self._audit_trail_writer.write(metrics)
        logger.debug(f"Recorded query: {metrics.query_id}")

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        timestamp = time.time()
        error_record = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "timestamp": timestamp,
            "engine_id": self.engine_id
        }
        self._errors.append(error_record)
        logger.error(f"Error recorded: {error_type} for query_id={query_id}: {message}")

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
        hits = list(self._doctrine_hits)
        if not hits:
            return 0.0
        hit_count = sum(1 for hit in hits if hit)
        rate = hit_count / len(hits)
        logger.info(f"Doctrine hit rate: {rate:.4f}")
        return rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        queries_in_window = [q for q in self._queries if q.timestamp >= window_start]
        error_count = len(errors_in_window)
        query_count = len(queries_in_window)
        if query_count == 0:
            return 0.0
        rate = error_count / query_count
        logger.info(f"Error rate in last {window_hours}h: {rate:.4f}")
        return rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= one_hour_ago)
        logger.info(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        modes = Counter()
        confidence_buckets = defaultdict(int)
        doctrine_hits = 0
        total = 0
        for q in self._queries:
            modes[q.mode] += 1
            bucket = int(q.confidence * 10)
            confidence_buckets[bucket] += 1
            if q.doctrine_matched:
                doctrine_hits += 1
            total += 1
        coverage = {
            "total_queries": total,
            "modes": dict(modes),
            "confidence_distribution": dict(confidence_buckets),
            "doctrine_matched": doctrine_hits,
            "doctrine_hit_rate": doctrine_hits / total if total else 0.0
        }
        logger.info(f"Coverage report: {coverage}")
        return coverage

    def export_jsonl(self, path: str) -> int:
        p = pathlib.Path(path)
        count = 0
        with p.open("w", encoding="utf-8") as f:
            for q in self._queries:
                f.write(json.dumps(asdict(q)) + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {path}")
        return count

class AuditTrailWriter:
    def __init__(self, base_path: str = "./audit_trails"):
        self.base_path = pathlib.Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"AuditTrailWriter initialized at {self.base_path}")

    def write(self, metrics: QueryMetrics):
        filename = self._filename_for_query(metrics)
        path = self.base_path / filename
        record = asdict(metrics)
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
        logger.debug(f"Audit trail written for query_id={metrics.query_id} at {path}")

    def _filename_for_query(self, metrics: QueryMetrics) -> str:
        date_str = time.strftime("%Y%m%d", time.localtime(metrics.timestamp))
        hash_id = hashlib.sha256(metrics.query_id.encode()).hexdigest()[:8]
        filename = f"{ENGINE_ID}_{date_str}_{hash_id}.jsonl"
        return filename

COLLECTOR = TelemetryCollector(engine_id=ENGINE_ID)