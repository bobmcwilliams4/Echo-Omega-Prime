import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Union
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "ET04"

@dataclass
class QueryMetrics:
    query_id: str
    engine_id: str = ENGINE_ID
    timestamp: float = field(default_factory=time.time)
    latency_ms: float = 0.0
    cache_hit: bool = False
    doctrine_matched: bool = False
    mode: str = "default"
    confidence: float = 0.0
    error: Optional[str] = None

class TelemetryCollector:
    def __init__(self, max_queries: int = 100000):
        self.max_queries = max_queries
        self._queries: deque = deque(maxlen=max_queries)
        self._errors: deque = deque(maxlen=max_queries)
        self._doctrine_hits: deque = deque(maxlen=max_queries)
        self._latencies: deque = deque(maxlen=max_queries)
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
        if metrics.error:
            self.record_error("query_error", metrics.error, metrics.query_id)
        self._audit_writer.write(metrics)
        logger.debug(f"Recorded query: {metrics.query_id}")

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "timestamp": time.time()
        }
        self._errors.append(error_entry)
        logger.error(f"Error recorded: {error_entry}")

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = [m.latency_ms for m in self._queries if m.latency_ms is not None]
        if not latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        latencies_sorted = sorted(latencies)
        stats = {
            "avg": statistics.mean(latencies),
            "p50": statistics.median(latencies),
            "p95": latencies_sorted[int(0.95 * len(latencies_sorted)) - 1],
            "p99": latencies_sorted[int(0.99 * len(latencies_sorted)) - 1],
            "min": min(latencies),
            "max": max(latencies)
        }
        logger.info(f"Latency stats: {stats}")
        return stats

    def get_doctrine_hit_rate(self) -> float:
        total = len(self._doctrine_hits)
        if total == 0:
            return 0.0
        hits = sum(1 for hit in self._doctrine_hits if hit)
        hit_rate = hits / total
        logger.info(f"Doctrine hit rate: {hit_rate:.4f}")
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        queries_in_window = [m for m in self._queries if m.timestamp >= window_start]
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        total_queries = len(queries_in_window)
        total_errors = len(errors_in_window)
        if total_queries == 0:
            return 0.0
        error_rate = total_errors / total_queries
        logger.info(f"Error rate in last {window_hours} hours: {error_rate:.4f}")
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for m in self._queries if m.timestamp >= one_hour_ago)
        logger.info(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        modes = Counter(m.mode for m in self._queries)
        doctrine_hits = sum(1 for m in self._queries if m.doctrine_matched)
        cache_hits = sum(1 for m in self._queries if m.cache_hit)
        total = len(self._queries)
        coverage = {
            "total_queries": total,
            "modes": dict(modes),
            "doctrine_matched": doctrine_hits,
            "cache_hit": cache_hits,
            "doctrine_match_rate": doctrine_hits / total if total else 0.0,
            "cache_hit_rate": cache_hits / total if total else 0.0,
        }
        logger.info(f"Coverage report: {coverage}")
        return coverage

    def export_jsonl(self, path: Union[str, pathlib.Path]) -> int:
        path = pathlib.Path(path)
        count = 0
        with path.open("w", encoding="utf-8") as f:
            for m in self._queries:
                f.write(json.dumps(dataclasses.asdict(m)) + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {path}")
        return count

class AuditTrailWriter:
    def __init__(self, base_dir: Union[str, pathlib.Path] = "./audit_trail"):
        self.base_dir = pathlib.Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
        logger.info(f"AuditTrailWriter initialized at {self.base_dir}")

    def _get_query_audit_path(self, query_id: str) -> pathlib.Path:
        hash_digest = hashlib.sha256(query_id.encode()).hexdigest()
        subdir = hash_digest[:2]
        dir_path = self.base_dir / subdir
        dir_path.mkdir(exist_ok=True)
        audit_path = dir_path / f"{query_id}.jsonl"
        return audit_path

    def write(self, metrics: QueryMetrics):
        audit_path = self._get_query_audit_path(metrics.query_id)
        with audit_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(dataclasses.asdict(metrics)) + "\n")
        logger.debug(f"Audit trail written for query: {metrics.query_id}")

COLLECTOR = TelemetryCollector()