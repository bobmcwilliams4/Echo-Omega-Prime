import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any, Union
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "ET07"

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
        self._query_index: Dict[str, QueryMetrics] = {}
        self._doctrine_hits: int = 0
        self._total_queries: int = 0
        self._error_counter: Counter = Counter()
        self._audit_writer = AuditTrailWriter()
        logger.info(f"TelemetryCollector initialized for engine {ENGINE_ID}")

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._query_index[metrics.query_id] = metrics
        self._total_queries += 1
        if metrics.doctrine_matched:
            self._doctrine_hits += 1
        self._audit_writer.write(metrics)
        logger.debug(f"Recorded query: {metrics.query_id} (latency: {metrics.latency_ms}ms)")

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "engine_id": ENGINE_ID,
            "error_type": error_type,
            "message": message,
            "query_id": query_id
        }
        self._errors.append(error_entry)
        self._error_counter[error_type] += 1
        logger.error(f"Error recorded: {error_type} ({message}) for query {query_id}")

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = [q.latency_ms for q in self._queries if q.latency_ms is not None]
        if not latencies:
            return {
                "avg": None,
                "p50": None,
                "p95": None,
                "p99": None,
                "min": None,
                "max": None
            }
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        min_latency = min(latencies)
        max_latency = max(latencies)
        p50 = statistics.median(latencies_sorted)
        p95 = self._percentile(latencies_sorted, 95)
        p99 = self._percentile(latencies_sorted, 99)
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

    def _percentile(self, data: List[float], percentile: float) -> float:
        if not data:
            return None
        k = (len(data) - 1) * (percentile / 100)
        f = int(k)
        c = f + 1
        if c >= len(data):
            return data[-1]
        d0 = data[f] * (c - k)
        d1 = data[c] * (k - f)
        return d0 + d1

    def get_doctrine_hit_rate(self) -> float:
        if self._total_queries == 0:
            return 0.0
        hit_rate = self._doctrine_hits / self._total_queries
        logger.info(f"Doctrine hit rate: {hit_rate:.4f}")
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        queries_in_window = [q for q in self._queries if q.timestamp >= window_start]
        num_queries = len(queries_in_window)
        num_errors = len(errors_in_window)
        error_rate = (num_errors / num_queries) if num_queries > 0 else 0.0
        logger.info(f"Error rate in last {window_hours}h: {error_rate:.4f}")
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= hour_ago)
        logger.info(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        modes = Counter()
        cache_hits = 0
        doctrine_hits = 0
        confidences = []
        errors = 0
        for q in self._queries:
            modes[q.mode] += 1
            if q.cache_hit:
                cache_hits += 1
            if q.doctrine_matched:
                doctrine_hits += 1
            confidences.append(q.confidence)
            if q.error:
                errors += 1
        total = len(self._queries)
        report = {
            "total_queries": total,
            "mode_distribution": dict(modes),
            "cache_hit_rate": (cache_hits / total) if total else 0.0,
            "doctrine_hit_rate": (doctrine_hits / total) if total else 0.0,
            "avg_confidence": statistics.mean(confidences) if confidences else None,
            "error_count": errors
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
    def __init__(self, audit_dir: Union[str, pathlib.Path] = "audit_trail"):
        self.audit_dir = pathlib.Path(audit_dir)
        self.audit_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"AuditTrailWriter initialized at {self.audit_dir}")

    def write(self, metrics: QueryMetrics):
        filename = self._get_filename(metrics.query_id)
        record = asdict(metrics)
        record["audit_timestamp"] = time.time()
        with open(filename, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
        logger.debug(f"Audit trail written for query {metrics.query_id}")

    def _get_filename(self, query_id: str) -> pathlib.Path:
        hash_digest = hashlib.sha256(query_id.encode()).hexdigest()[:16]
        filename = f"{ENGINE_ID}_{hash_digest}.jsonl"
        return self.audit_dir / filename

COLLECTOR = TelemetryCollector()