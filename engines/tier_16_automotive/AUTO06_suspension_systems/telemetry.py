import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any, Union
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "AUTO06"

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
    def __init__(self, max_queries: int = 10000):
        self._queries: deque = deque(maxlen=max_queries)
        self._errors: deque = deque(maxlen=max_queries)
        self._doctrine_hits: deque = deque(maxlen=max_queries)
        self._latencies: deque = deque(maxlen=max_queries)
        self._coverage: defaultdict = defaultdict(lambda: {"count": 0, "doctrine_matched": 0})
        self._query_ids: set = set()
        self._audit_writer = AuditTrailWriter()
        logger.info(f"TelemetryCollector initialized for engine {ENGINE_ID}")

    def record_query(self, metrics: QueryMetrics):
        if metrics.query_id in self._query_ids:
            logger.warning(f"Duplicate query_id detected: {metrics.query_id}")
            return
        self._queries.append(metrics)
        self._query_ids.add(metrics.query_id)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._coverage[metrics.mode]["count"] += 1
        if metrics.doctrine_matched:
            self._coverage[metrics.mode]["doctrine_matched"] += 1
        if metrics.error:
            self.record_error(metrics.error, metrics.error, metrics.query_id)
        self._audit_writer.write(metrics)
        logger.debug(f"Recorded query: {metrics.query_id}")

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "engine_id": ENGINE_ID,
            "error_type": error_type,
            "message": message,
            "query_id": query_id
        }
        self._errors.append(error_entry)
        logger.error(f"Error recorded: {error_type} | {message} | Query: {query_id}")

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = list(self._latencies)
        if not latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        min_latency = min(latencies)
        max_latency = max(latencies)
        p50 = statistics.median(latencies)
        p95 = latencies_sorted[int(0.95 * len(latencies_sorted))-1]
        p99 = latencies_sorted[int(0.99 * len(latencies_sorted))-1]
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
        hits = sum(1 for hit in self._doctrine_hits if hit)
        total = len(self._doctrine_hits)
        rate = hits / total if total > 0 else 0.0
        logger.info(f"Doctrine hit rate: {rate:.4f}")
        return rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        error_count = sum(1 for e in self._errors if e["timestamp"] >= window_start)
        query_count = sum(1 for q in self._queries if q.timestamp >= window_start)
        rate = error_count / query_count if query_count > 0 else 0.0
        logger.info(f"Error rate in last {window_hours}h: {rate:.4f}")
        return rate

    def queries_last_hour(self) -> int:
        now = time.time()
        hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= hour_ago)
        logger.info(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {}
        for mode, stats in self._coverage.items():
            count = stats["count"]
            doctrine_matched = stats["doctrine_matched"]
            doctrine_rate = doctrine_matched / count if count > 0 else 0.0
            report[mode] = {
                "total_queries": count,
                "doctrine_matched": doctrine_matched,
                "doctrine_match_rate": doctrine_rate
            }
        logger.info(f"Coverage report: {report}")
        return report

    def export_jsonl(self, path: Union[str, pathlib.Path]) -> int:
        path = pathlib.Path(path)
        count = 0
        with path.open("w", encoding="utf-8") as f:
            for q in self._queries:
                f.write(json.dumps(asdict(q)) + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {path}")
        return count

class AuditTrailWriter:
    def __init__(self, base_dir: Optional[Union[str, pathlib.Path]] = None):
        self.base_dir = pathlib.Path(base_dir) if base_dir else pathlib.Path("./audit_trails")
        self.base_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"AuditTrailWriter initialized at {self.base_dir}")

    def _get_audit_path(self, query_id: str) -> pathlib.Path:
        hash_digest = hashlib.sha256(query_id.encode()).hexdigest()[:8]
        filename = f"{ENGINE_ID}_{hash_digest}_{query_id}.jsonl"
        return self.base_dir / filename

    def write(self, metrics: QueryMetrics):
        path = self._get_audit_path(metrics.query_id)
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(metrics)) + "\n")
        logger.debug(f"Audit trail written for query_id: {metrics.query_id}")

COLLECTOR = TelemetryCollector()