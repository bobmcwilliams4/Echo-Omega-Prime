import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "ENRG09"

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
        self._cache_hits: deque = deque(maxlen=10000)
        self._latencies: deque = deque(maxlen=10000)
        self._coverage: defaultdict = defaultdict(lambda: {'count': 0, 'confidence_sum': 0.0})
        self._audit_writer = AuditTrailWriter()
        logger.info(f"TelemetryCollector initialized for engine {engine_id}")

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._cache_hits.append(metrics.cache_hit)
        self._coverage[metrics.mode]['count'] += 1
        self._coverage[metrics.mode]['confidence_sum'] += metrics.confidence
        if metrics.error:
            self.record_error(error_type="query_error", message=metrics.error, query_id=metrics.query_id)
        self._audit_writer.write(metrics)
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
        logger.warning(f"Recorded error: {error_type} for query {query_id}")

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
        logger.info(f"Latency stats computed: avg={avg}, p50={p50}, p95={p95}, p99={p99}, min={min_latency}, max={max_latency}")
        return {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_latency,
            "max": max_latency
        }

    def get_doctrine_hit_rate(self) -> float:
        hits = list(self._doctrine_hits)
        if not hits:
            return 0.0
        hit_count = sum(1 for h in hits if h)
        rate = hit_count / len(hits)
        logger.info(f"Doctrine hit rate: {rate}")
        return rate

    def get_error_rate(self, window_hours: float) -> float:
        now = time.time()
        window_seconds = window_hours * 3600
        errors_in_window = [e for e in self._errors if now - e['timestamp'] <= window_seconds]
        queries_in_window = [q for q in self._queries if now - q.timestamp <= window_seconds]
        if not queries_in_window:
            return 0.0
        error_rate = len(errors_in_window) / len(queries_in_window)
        logger.info(f"Error rate in last {window_hours} hours: {error_rate}")
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= one_hour_ago)
        logger.info(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {}
        for mode, data in self._coverage.items():
            count = data['count']
            avg_confidence = data['confidence_sum'] / count if count > 0 else 0.0
            report[mode] = {
                "count": count,
                "avg_confidence": avg_confidence
            }
        logger.info(f"Coverage report generated: {report}")
        return report

    def export_jsonl(self, path: str) -> int:
        p = pathlib.Path(path)
        exported = 0
        with p.open("w", encoding="utf-8") as f:
            for q in self._queries:
                f.write(json.dumps(asdict(q)) + "\n")
                exported += 1
        logger.info(f"Exported {exported} queries to {path}")
        return exported

class AuditTrailWriter:
    def __init__(self, audit_dir: Optional[str] = None):
        if audit_dir is None:
            audit_dir = "./audit_trail"
        self.audit_dir = pathlib.Path(audit_dir)
        self.audit_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"AuditTrailWriter initialized at {self.audit_dir}")

    def write(self, metrics: QueryMetrics):
        filename = self._filename_for_query(metrics.query_id)
        filepath = self.audit_dir / filename
        audit_entry = {
            "query_id": metrics.query_id,
            "engine_id": metrics.engine_id,
            "timestamp": metrics.timestamp,
            "latency_ms": metrics.latency_ms,
            "cache_hit": metrics.cache_hit,
            "doctrine_matched": metrics.doctrine_matched,
            "mode": metrics.mode,
            "confidence": metrics.confidence,
            "error": metrics.error
        }
        with filepath.open("a", encoding="utf-8") as f:
            f.write(json.dumps(audit_entry) + "\n")
        logger.debug(f"Wrote audit trail for query {metrics.query_id} to {filepath}")

    def _filename_for_query(self, query_id: str) -> str:
        hash_digest = hashlib.sha256(query_id.encode()).hexdigest()[:8]
        filename = f"audit_{hash_digest}.jsonl"
        return filename

COLLECTOR = TelemetryCollector(engine_id=ENGINE_ID)