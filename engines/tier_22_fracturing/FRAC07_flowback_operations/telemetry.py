import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "FRAC07"

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
        self._queries: deque = deque(maxlen=10000)
        self._errors: deque = deque(maxlen=5000)
        self._doctrine_hits: deque = deque(maxlen=10000)
        self._query_ids: set = set()
        self._audit_trail_writer = AuditTrailWriter()
        self._coverage: defaultdict = defaultdict(set)
        logger.info(f"TelemetryCollector initialized for engine {engine_id}")

    def record_query(self, metrics: QueryMetrics):
        if metrics.query_id in self._query_ids:
            logger.warning(f"Duplicate query_id detected: {metrics.query_id}")
            return
        self._queries.append(metrics)
        self._query_ids.add(metrics.query_id)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._coverage[metrics.mode].add(metrics.query_id)
        self._audit_trail_writer.write(metrics)
        logger.debug(f"Recorded query: {metrics.query_id}")

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "timestamp": time.time(),
            "engine_id": self.engine_id
        }
        self._errors.append(error_entry)
        logger.error(f"Error recorded: {error_type} - {message} (query_id={query_id})")

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = [q.latency_ms for q in self._queries if q.latency_ms is not None]
        if not latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = statistics.quantiles(latencies, n=100)[94] if len(latencies) >= 20 else None
        p99 = statistics.quantiles(latencies, n=100)[98] if len(latencies) >= 100 else None
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
        logger.debug(f"Latency stats: {stats}")
        return stats

    def get_doctrine_hit_rate(self) -> float:
        total = len(self._doctrine_hits)
        if total == 0:
            return 0.0
        hits = sum(1 for hit in self._doctrine_hits if hit)
        hit_rate = hits / total
        logger.debug(f"Doctrine hit rate: {hit_rate:.3f}")
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_seconds = window_hours * 3600
        errors_in_window = [e for e in self._errors if now - e["timestamp"] <= window_seconds]
        queries_in_window = [q for q in self._queries if now - q.timestamp <= window_seconds]
        num_queries = len(queries_in_window)
        num_errors = len(errors_in_window)
        if num_queries == 0:
            return 0.0
        error_rate = num_errors / num_queries
        logger.debug(f"Error rate in last {window_hours}h: {error_rate:.3f}")
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= one_hour_ago)
        logger.debug(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {}
        for mode, query_ids in self._coverage.items():
            report[mode] = {
                "unique_queries": len(query_ids),
                "coverage_percent": (len(query_ids) / max(1, len(self._queries))) * 100
            }
        logger.debug(f"Coverage report: {report}")
        return report

    def export_jsonl(self, path: str) -> int:
        p = pathlib.Path(path)
        count = 0
        with p.open("w", encoding="utf-8") as f:
            for q in self._queries:
                f.write(json.dumps(dataclasses.asdict(q)) + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {path}")
        return count

class AuditTrailWriter:
    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = base_dir or "./audit_trail"
        self._ensure_dir()
        logger.info(f"AuditTrailWriter initialized at {self.base_dir}")

    def _ensure_dir(self):
        p = pathlib.Path(self.base_dir)
        p.mkdir(parents=True, exist_ok=True)

    def write(self, metrics: QueryMetrics):
        filename = self._get_filename(metrics.query_id)
        data = dataclasses.asdict(metrics)
        data["audit_hash"] = self._hash_query(data)
        p = pathlib.Path(self.base_dir) / filename
        with p.open("w", encoding="utf-8") as f:
            f.write(json.dumps(data) + "\n")
        logger.debug(f"Wrote audit trail for query_id: {metrics.query_id}")

    def _get_filename(self, query_id: str) -> str:
        safe_id = hashlib.sha256(query_id.encode()).hexdigest()[:16]
        return f"{safe_id}.jsonl"

    def _hash_query(self, data: Dict[str, Any]) -> str:
        s = json.dumps(data, sort_keys=True)
        return hashlib.sha256(s.encode()).hexdigest()

COLLECTOR = TelemetryCollector(engine_id=ENGINE_ID)