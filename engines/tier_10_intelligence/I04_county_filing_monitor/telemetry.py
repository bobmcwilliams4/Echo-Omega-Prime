import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Tuple
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "I04"

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
        self._latencies: deque = deque(maxlen=10000)
        self._audit_trail: List[Dict[str, Any]] = []
        self._query_counter: Counter = Counter()
        self._error_counter: Counter = Counter()
        self._coverage_counter: Counter = Counter()
        self._last_export_time = time.time()
        logger.info(f"TelemetryCollector initialized for engine {engine_id}")

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._query_counter[metrics.mode] += 1
        self._coverage_counter[metrics.doctrine_matched] += 1
        if metrics.error:
            self.record_error("query_error", metrics.error, metrics.query_id)
        logger.debug(f"Recorded query: {metrics.query_id}, latency: {metrics.latency_ms}ms, doctrine_matched: {metrics.doctrine_matched}")

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "timestamp": time.time()
        }
        self._errors.append(error_entry)
        self._error_counter[error_type] += 1
        logger.error(f"Error recorded: {error_type} for query {query_id}: {message}")

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = list(self._latencies)
        if not latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = latencies_sorted[int(0.95 * len(latencies_sorted)) - 1]
        p99 = latencies_sorted[int(0.99 * len(latencies_sorted)) - 1]
        min_latency = min(latencies)
        max_latency = max(latencies)
        logger.info(f"Latency stats: avg={avg}, p50={p50}, p95={p95}, p99={p99}, min={min_latency}, max={max_latency}")
        return {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_latency,
            "max": max_latency
        }

    def get_doctrine_hit_rate(self) -> float:
        hits = sum(1 for hit in self._doctrine_hits if hit)
        total = len(self._doctrine_hits)
        hit_rate = hits / total if total > 0 else 0.0
        logger.info(f"Doctrine hit rate: {hit_rate:.3f} ({hits}/{total})")
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        error_count = sum(1 for e in self._errors if e["timestamp"] >= window_start)
        query_count = sum(1 for q in self._queries if q.timestamp >= window_start)
        error_rate = error_count / query_count if query_count > 0 else 0.0
        logger.info(f"Error rate in last {window_hours}h: {error_rate:.3f} ({error_count}/{query_count})")
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= one_hour_ago)
        logger.info(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        total = sum(self._coverage_counter.values())
        doctrine_matched = self._coverage_counter[True]
        not_matched = self._coverage_counter[False]
        coverage = doctrine_matched / total if total > 0 else 0.0
        report = {
            "total_queries": total,
            "doctrine_matched": doctrine_matched,
            "not_matched": not_matched,
            "coverage": coverage
        }
        logger.info(f"Coverage report: {report}")
        return report

    def export_jsonl(self, path: str) -> int:
        export_path = pathlib.Path(path)
        export_path.parent.mkdir(parents=True, exist_ok=True)
        count = 0
        with export_path.open("a", encoding="utf-8") as f:
            for q in self._queries:
                f.write(json.dumps(q.__dict__) + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {export_path}")
        self._last_export_time = time.time()
        return count

class AuditTrailWriter:
    def __init__(self, audit_dir: str):
        self.audit_dir = pathlib.Path(audit_dir)
        self.audit_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"AuditTrailWriter initialized at {self.audit_dir}")

    def write(self, query_metrics: QueryMetrics):
        audit_entry = {
            "query_id": query_metrics.query_id,
            "engine_id": query_metrics.engine_id,
            "timestamp": query_metrics.timestamp,
            "latency_ms": query_metrics.latency_ms,
            "cache_hit": query_metrics.cache_hit,
            "doctrine_matched": query_metrics.doctrine_matched,
            "mode": query_metrics.mode,
            "confidence": query_metrics.confidence,
            "error": query_metrics.error
        }
        filename = f"{query_metrics.query_id}_{int(query_metrics.timestamp)}.jsonl"
        audit_path = self.audit_dir / filename
        with audit_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(audit_entry) + "\n")
        logger.debug(f"Audit trail written for query {query_metrics.query_id} at {audit_path}")

COLLECTOR = TelemetryCollector(engine_id=ENGINE_ID)