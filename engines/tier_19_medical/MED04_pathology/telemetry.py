import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Union
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "MED04"

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
        self._query_times: deque = deque(maxlen=max_queries)
        self._query_modes: Counter = Counter()
        self._coverage: defaultdict = defaultdict(set)
        self._audit_writer = AuditTrailWriter()
        logger.info("TelemetryCollector initialized for engine {}", ENGINE_ID)

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._latencies.append(metrics.latency_ms)
        self._query_times.append(metrics.timestamp)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._query_modes[metrics.mode] += 1
        self._coverage[metrics.mode].add(metrics.query_id)
        self._audit_writer.write(metrics)
        logger.debug("Recorded query: {}", metrics)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "engine_id": ENGINE_ID,
            "error_type": error_type,
            "message": message,
            "query_id": query_id
        }
        self._errors.append(error_entry)
        logger.error("Recorded error: {}", error_entry)

    def get_latency_stats(self) -> Dict[str, Union[float, None]]:
        latencies = list(self._latencies)
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
        p50 = statistics.median(latencies)
        p95 = latencies_sorted[int(len(latencies_sorted) * 0.95) - 1]
        p99 = latencies_sorted[int(len(latencies_sorted) * 0.99) - 1]
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
        logger.debug("Latency stats: {}", stats)
        return stats

    def get_doctrine_hit_rate(self) -> float:
        hits = sum(1 for hit in self._doctrine_hits if hit)
        total = len(self._doctrine_hits)
        hit_rate = hits / total if total > 0 else 0.0
        logger.debug("Doctrine hit rate: {:.2f}", hit_rate)
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        queries_in_window = [q for q in self._queries if q.timestamp >= window_start]
        error_rate = len(errors_in_window) / max(len(queries_in_window), 1)
        logger.debug("Error rate in last {:.2f} hours: {:.4f}", window_hours, error_rate)
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= one_hour_ago)
        logger.debug("Queries in last hour: {}", count)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {}
        for mode, queries in self._coverage.items():
            report[mode] = {
                "unique_queries": len(queries),
                "total_queries": self._query_modes[mode]
            }
        logger.debug("Coverage report: {}", report)
        return report

    def export_jsonl(self, path: Union[str, pathlib.Path]) -> int:
        path = pathlib.Path(path)
        count = 0
        with path.open("w", encoding="utf-8") as f:
            for q in self._queries:
                f.write(json.dumps(dataclasses.asdict(q)) + "\n")
                count += 1
        logger.info("Exported {} queries to {}", count, path)
        return count

class AuditTrailWriter:
    def __init__(self, audit_dir: Union[str, pathlib.Path] = "./audit_trail"):
        self.audit_dir = pathlib.Path(audit_dir)
        self.audit_dir.mkdir(parents=True, exist_ok=True)
        logger.info("AuditTrailWriter initialized at {}", self.audit_dir)

    def _get_audit_path(self, query_id: str) -> pathlib.Path:
        hash_id = hashlib.sha256(query_id.encode()).hexdigest()
        filename = f"{hash_id}.jsonl"
        return self.audit_dir / filename

    def write(self, metrics: QueryMetrics):
        audit_path = self._get_audit_path(metrics.query_id)
        with audit_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(dataclasses.asdict(metrics)) + "\n")
        logger.debug("Wrote audit trail for query {}", metrics.query_id)

COLLECTOR = TelemetryCollector()