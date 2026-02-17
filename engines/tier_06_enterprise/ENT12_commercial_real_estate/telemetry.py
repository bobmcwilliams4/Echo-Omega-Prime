import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "ENT12"

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
        self._coverage_modes = Counter()
        self._coverage_confidences = defaultdict(list)
        self._query_ids = set()
        self._audit_writer = AuditTrailWriter()
        logger.info(f"TelemetryCollector initialized for engine {engine_id}")

    def record_query(self, metrics: QueryMetrics):
        if metrics.query_id in self._query_ids:
            logger.warning(f"Duplicate query_id detected: {metrics.query_id}")
            return
        self._queries.append(metrics)
        self._query_ids.add(metrics.query_id)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._coverage_modes[metrics.mode] += 1
        self._coverage_confidences[metrics.mode].append(metrics.confidence)
        if metrics.error:
            self.record_error("query_error", metrics.error, metrics.query_id)
        self._audit_writer.write(metrics)
        logger.debug(f"Recorded query: {metrics.query_id}")

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "engine_id": self.engine_id,
            "timestamp": time.time()
        }
        self._errors.append(error_entry)
        logger.error(f"Error recorded: {error_entry}")

    def get_latency_stats(self) -> Dict[str, Any]:
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
        min_latency = min(latencies)
        max_latency = max(latencies)
        p50 = statistics.median(latencies)
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
        logger.debug(f"Latency stats: {stats}")
        return stats

    def get_doctrine_hit_rate(self) -> float:
        hits = sum(1 for hit in self._doctrine_hits if hit)
        total = len(self._doctrine_hits)
        hit_rate = hits / total if total > 0 else 0.0
        logger.debug(f"Doctrine hit rate: {hit_rate:.4f}")
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        queries_in_window = [q for q in self._queries if q.timestamp >= window_start]
        error_count = len(errors_in_window)
        query_count = len(queries_in_window)
        error_rate = error_count / query_count if query_count > 0 else 0.0
        logger.debug(f"Error rate in last {window_hours} hours: {error_rate:.4f}")
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= one_hour_ago)
        logger.debug(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {}
        for mode, count in self._coverage_modes.items():
            confidences = self._coverage_confidences[mode]
            avg_conf = statistics.mean(confidences) if confidences else None
            min_conf = min(confidences) if confidences else None
            max_conf = max(confidences) if confidences else None
            report[mode] = {
                "count": count,
                "avg_confidence": avg_conf,
                "min_confidence": min_conf,
                "max_confidence": max_conf
            }
        logger.debug(f"Coverage report: {report}")
        return report

    def export_jsonl(self, path: str) -> int:
        export_path = pathlib.Path(path)
        export_path.parent.mkdir(parents=True, exist_ok=True)
        count = 0
        with export_path.open("w", encoding="utf-8") as f:
            for q in self._queries:
                f.write(json.dumps(asdict(q)) + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {export_path}")
        return count

class AuditTrailWriter:
    def __init__(self, audit_dir: str = "./audit_trail"):
        self.audit_dir = pathlib.Path(audit_dir)
        self.audit_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"AuditTrailWriter initialized at {self.audit_dir}")

    def _get_audit_path(self, query_id: str) -> pathlib.Path:
        hash_id = hashlib.sha256(query_id.encode()).hexdigest()[:8]
        filename = f"{ENGINE_ID}_{hash_id}_{query_id}.jsonl"
        return self.audit_dir / filename

    def write(self, metrics: QueryMetrics):
        audit_path = self._get_audit_path(metrics.query_id)
        with audit_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(metrics)) + "\n")
        logger.debug(f"Wrote audit trail for query {metrics.query_id} to {audit_path}")

COLLECTOR = TelemetryCollector(engine_id=ENGINE_ID)