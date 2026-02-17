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

ENGINE_ID = "MATH01"

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
        self._query_id_set: set = set()
        self._doctrine_hits: int = 0
        self._doctrine_total: int = 0
        self._latencies: List[float] = []
        self._last_hour_queries: collections.deque = collections.deque()
        self._coverage_modes: collections.Counter = collections.Counter()
        self._coverage_cache: collections.Counter = collections.Counter()
        self._coverage_doctrine: collections.Counter = collections.Counter()
        self._audit_writer = AuditTrailWriter()
        self._lock = collections.Lock() if hasattr(collections, 'Lock') else None  # placeholder for thread safety

    def record_query(self, metrics: QueryMetrics):
        if self._lock:
            self._lock.acquire()
        try:
            if metrics.query_id in self._query_id_set:
                logger.warning(f"Duplicate query_id: {metrics.query_id} ignored.")
                return
            self._queries.append(metrics)
            self._query_id_set.add(metrics.query_id)
            self._latencies.append(metrics.latency_ms)
            self._coverage_modes[metrics.mode] += 1
            self._coverage_cache['hit' if metrics.cache_hit else 'miss'] += 1
            self._coverage_doctrine['matched' if metrics.doctrine_matched else 'unmatched'] += 1
            self._doctrine_total += 1
            if metrics.doctrine_matched:
                self._doctrine_hits += 1
            now = time.time()
            self._last_hour_queries.append((now, metrics.query_id))
            self._audit_writer.write(metrics)
        finally:
            if self._lock:
                self._lock.release()

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "timestamp": time.time(),
            "engine_id": ENGINE_ID
        }
        self._errors.append(error_entry)
        logger.error(f"Error recorded: {error_entry}")
        self._audit_writer.write_error(error_entry)

    def get_latency_stats(self) -> Dict[str, Any]:
        if not self._latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        latencies = sorted(self._latencies)
        avg = statistics.mean(latencies)
        min_latency = latencies[0]
        max_latency = latencies[-1]
        p50 = statistics.median(latencies)
        p95 = latencies[int(len(latencies) * 0.95) - 1] if len(latencies) > 1 else latencies[0]
        p99 = latencies[int(len(latencies) * 0.99) - 1] if len(latencies) > 1 else latencies[0]
        return {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_latency,
            "max": max_latency
        }

    def get_doctrine_hit_rate(self) -> float:
        if self._doctrine_total == 0:
            return 0.0
        return self._doctrine_hits / self._doctrine_total

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        error_count = sum(1 for e in self._errors if e['timestamp'] >= window_start)
        query_count = sum(1 for t, _ in self._last_hour_queries if t >= window_start)
        if query_count == 0:
            return 0.0
        return error_count / query_count

    def queries_last_hour(self) -> int:
        now = time.time()
        hour_ago = now - 3600
        # Remove old queries
        while self._last_hour_queries and self._last_hour_queries[0][0] < hour_ago:
            self._last_hour_queries.popleft()
        return len(self._last_hour_queries)

    def get_coverage_report(self) -> Dict[str, Any]:
        total_queries = len(self._queries)
        mode_coverage = dict(self._coverage_modes)
        cache_coverage = dict(self._coverage_cache)
        doctrine_coverage = dict(self._coverage_doctrine)
        return {
            "total_queries": total_queries,
            "mode_coverage": mode_coverage,
            "cache_coverage": cache_coverage,
            "doctrine_coverage": doctrine_coverage,
            "doctrine_hit_rate": self.get_doctrine_hit_rate()
        }

    def export_jsonl(self, path: str) -> int:
        p = pathlib.Path(path)
        count = 0
        with p.open('w', encoding='utf-8') as f:
            for q in self._queries:
                f.write(json.dumps(dataclasses.asdict(q)) + '\n')
                count += 1
            for e in self._errors:
                f.write(json.dumps(e) + '\n')
                count += 1
        logger.info(f"Exported {count} telemetry entries to {path}")
        return count

class AuditTrailWriter:
    def __init__(self, audit_dir: Optional[str] = None):
        self.audit_dir = audit_dir or "./audit_trail"
        self._ensure_dir()

    def _ensure_dir(self):
        p = pathlib.Path(self.audit_dir)
        p.mkdir(parents=True, exist_ok=True)

    def _get_file_path(self, query_id: str) -> pathlib.Path:
        # Hash query_id for filename safety
        hash_id = hashlib.sha256(query_id.encode()).hexdigest()
        return pathlib.Path(self.audit_dir) / f"{hash_id}.jsonl"

    def write(self, metrics: QueryMetrics):
        file_path = self._get_file_path(metrics.query_id)
        with file_path.open('a', encoding='utf-8') as f:
            f.write(json.dumps(dataclasses.asdict(metrics)) + '\n')
        logger.debug(f"Audit trail written for query_id: {metrics.query_id}")

    def write_error(self, error_entry: Dict[str, Any]):
        query_id = error_entry.get("query_id", "unknown")
        file_path = self._get_file_path(query_id)
        with file_path.open('a', encoding='utf-8') as f:
            f.write(json.dumps(error_entry) + '\n')
        logger.debug(f"Audit error written for query_id: {query_id}")

COLLECTOR = TelemetryCollector()