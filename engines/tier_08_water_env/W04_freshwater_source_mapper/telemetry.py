import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any, Union
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "W04"

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
        self._queries: deque = deque(maxlen=10000)
        self._errors: deque = deque(maxlen=5000)
        self._doctrine_hits: deque = deque(maxlen=10000)
        self._latencies: deque = deque(maxlen=10000)
        self._coverage: defaultdict = defaultdict(lambda: {"count": 0, "confidence": []})
        self._query_ids: set = set()
        self._audit_writer = AuditTrailWriter()
        logger.info("TelemetryCollector initialized.")

    def record_query(self, metrics: QueryMetrics):
        if metrics.query_id in self._query_ids:
            logger.warning(f"Duplicate query_id detected: {metrics.query_id}")
            return
        self._query_ids.add(metrics.query_id)
        self._queries.append(metrics)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._coverage[metrics.mode]["count"] += 1
        self._coverage[metrics.mode]["confidence"].append(metrics.confidence)
        self._audit_writer.write(metrics)
        logger.debug(f"Recorded query: {metrics.query_id}")

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        err = {
            "error_type": error_type,
            "message": message,
            "timestamp": time.time(),
            "query_id": query_id
        }
        self._errors.append(err)
        logger.error(f"Error recorded: {error_type} for query {query_id}")

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
        hits = list(self._doctrine_hits)
        if not hits:
            return 0.0
        hit_rate = sum(hits) / len(hits)
        logger.debug(f"Doctrine hit rate: {hit_rate}")
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        error_count = sum(1 for e in self._errors if e["timestamp"] >= window_start)
        query_count = sum(1 for q in self._queries if q.timestamp >= window_start)
        if query_count == 0:
            return 0.0
        error_rate = error_count / query_count
        logger.debug(f"Error rate in last {window_hours} hours: {error_rate}")
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= one_hour_ago)
        logger.debug(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {}
        for mode, data in self._coverage.items():
            count = data["count"]
            confidences = data["confidence"]
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
    def __init__(self, audit_dir: Optional[Union[str, pathlib.Path]] = None):
        if audit_dir is None:
            audit_dir = pathlib.Path("./audit_trail")
        else:
            audit_dir = pathlib.Path(audit_dir)
        self.audit_dir = audit_dir
        self.audit_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"AuditTrailWriter initialized at {self.audit_dir}")

    def write(self, metrics: QueryMetrics):
        filename = self._get_filename(metrics.query_id)
        path = self.audit_dir / filename
        record = asdict(metrics)
        record["audit_hash"] = self._hash_record(record)
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
        logger.debug(f"Wrote audit trail for query {metrics.query_id} to {path}")

    def _get_filename(self, query_id: str) -> str:
        hash_id = hashlib.sha256(query_id.encode()).hexdigest()[:8]
        return f"{ENGINE_ID}_query_{hash_id}.jsonl"

    def _hash_record(self, record: Dict[str, Any]) -> str:
        record_str = json.dumps(record, sort_keys=True)
        return hashlib.sha256(record_str.encode()).hexdigest()

COLLECTOR = TelemetryCollector()