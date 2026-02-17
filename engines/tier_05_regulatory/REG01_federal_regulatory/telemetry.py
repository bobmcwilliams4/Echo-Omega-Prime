import time
import json
import hashlib
import statistics
import pathlib
import dataclasses
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
import collections
from loguru import logger

ENGINE_ID = "REG01"

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
    def __init__(self):
        self._queries: List[QueryMetrics] = []
        self._errors: List[Dict[str, Any]] = []
        self._query_index: Dict[str, QueryMetrics] = {}
        self._doctrine_hits: int = 0
        self._doctrine_total: int = 0
        self._error_types: collections.Counter = collections.Counter()
        self._audit_writer = AuditTrailWriter()
        self._lock = collections.Lock() if hasattr(collections, 'Lock') else None

    def record_query(self, metrics: QueryMetrics):
        logger.debug(f"Recording query: {metrics}")
        self._queries.append(metrics)
        self._query_index[metrics.query_id] = metrics
        self._doctrine_total += 1
        if metrics.doctrine_matched:
            self._doctrine_hits += 1
        self._audit_writer.write(metrics)
        if metrics.error:
            self.record_error(metrics.error, "Query error", metrics.query_id)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "engine_id": ENGINE_ID
        }
        logger.error(f"Recording error: {error_entry}")
        self._errors.append(error_entry)
        self._error_types[error_type] += 1

    def get_latency_stats(self) -> Dict[str, float]:
        latencies = [q.latency_ms for q in self._queries if q.latency_ms is not None]
        if not latencies:
            return {"avg": 0, "p50": 0, "p95": 0, "p99": 0, "min": 0, "max": 0}
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = latencies_sorted[int(len(latencies_sorted)*0.95)-1] if len(latencies_sorted) > 1 else latencies_sorted[0]
        p99 = latencies_sorted[int(len(latencies_sorted)*0.99)-1] if len(latencies_sorted) > 1 else latencies_sorted[0]
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
        if self._doctrine_total == 0:
            return 0.0
        hit_rate = self._doctrine_hits / self._doctrine_total
        logger.debug(f"Doctrine hit rate: {hit_rate}")
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        queries_in_window = [q for q in self._queries if q.timestamp >= window_start]
        errors_in_window = [e for e in self._errors if e['timestamp'] >= window_start]
        total_queries = len(queries_in_window)
        total_errors = len(errors_in_window)
        error_rate = (total_errors / total_queries) if total_queries > 0 else 0.0
        logger.debug(f"Error rate in last {window_hours} hours: {error_rate}")
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= one_hour_ago)
        logger.debug(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        modes = collections.Counter(q.mode for q in self._queries)
        cache_hits = sum(1 for q in self._queries if q.cache_hit)
        doctrine_hits = self._doctrine_hits
        doctrine_total = self._doctrine_total
        coverage = {
            "total_queries": len(self._queries),
            "cache_hit_rate": (cache_hits / len(self._queries)) if self._queries else 0.0,
            "doctrine_hit_rate": self.get_doctrine_hit_rate(),
            "mode_distribution": dict(modes),
            "error_types": dict(self._error_types),
            "last_hour_queries": self.queries_last_hour()
        }
        logger.debug(f"Coverage report: {coverage}")
        return coverage

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
    def __init__(self, audit_dir: Optional[str] = None):
        self.audit_dir = audit_dir or "./audit_trails"
        self._ensure_dir()

    def _ensure_dir(self):
        p = pathlib.Path(self.audit_dir)
        if not p.exists():
            p.mkdir(parents=True, exist_ok=True)

    def write(self, metrics: QueryMetrics):
        filename = self._get_filename(metrics.query_id)
        filepath = pathlib.Path(self.audit_dir) / filename
        entry = dataclasses.asdict(metrics)
        entry['audit_hash'] = self._hash_entry(entry)
        with filepath.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        logger.debug(f"Wrote audit trail for query_id={metrics.query_id} to {filepath}")

    def _get_filename(self, query_id: str) -> str:
        return f"{ENGINE_ID}_{query_id}.jsonl"

    def _hash_entry(self, entry: Dict[str, Any]) -> str:
        entry_str = json.dumps(entry, sort_keys=True)
        return hashlib.sha256(entry_str.encode("utf-8")).hexdigest()

COLLECTOR = TelemetryCollector()