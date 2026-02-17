import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "SYN05"

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
    def __init__(self, max_queries: int = 100000):
        self._queries: deque = deque(maxlen=max_queries)
        self._errors: deque = deque(maxlen=max_queries)
        self._doctrine_hits: deque = deque(maxlen=max_queries)
        self._latencies: deque = deque(maxlen=max_queries)
        self._modes: Counter = Counter()
        self._confidence_scores: deque = deque(maxlen=max_queries)
        self._cache_hits: deque = deque(maxlen=max_queries)
        self._query_ids: set = set()
        self._audit_trail_writer = AuditTrailWriter()
        self._coverage_data: defaultdict = defaultdict(list)
        logger.info(f"TelemetryCollector initialized for engine {ENGINE_ID}")

    def record_query(self, metrics: QueryMetrics):
        logger.debug(f"Recording query: {metrics.query_id}")
        self._queries.append(metrics)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._modes[metrics.mode] += 1
        self._confidence_scores.append(metrics.confidence)
        self._cache_hits.append(metrics.cache_hit)
        self._query_ids.add(metrics.query_id)
        self._coverage_data[metrics.mode].append(metrics.doctrine_matched)
        self._audit_trail_writer.write(metrics)
        if metrics.error:
            self.record_error("query_error", metrics.error, metrics.query_id)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_record = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "timestamp": time.time(),
            "engine_id": ENGINE_ID
        }
        logger.error(f"Recording error: {error_record}")
        self._errors.append(error_record)

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = list(self._latencies)
        if not latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = statistics.quantiles(latencies, n=100)[94]
        p99 = statistics.quantiles(latencies, n=100)[98]
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
        logger.info(f"Latency stats: {stats}")
        return stats

    def get_doctrine_hit_rate(self) -> float:
        hits = list(self._doctrine_hits)
        if not hits:
            return 0.0
        rate = sum(hits) / len(hits)
        logger.info(f"Doctrine hit rate: {rate}")
        return rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        queries_in_window = [q for q in self._queries if q.timestamp >= window_start]
        if not queries_in_window:
            return 0.0
        rate = len(errors_in_window) / len(queries_in_window)
        logger.info(f"Error rate in last {window_hours} hours: {rate}")
        return rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= one_hour_ago)
        logger.info(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {}
        for mode, doctrine_matches in self._coverage_data.items():
            total = len(doctrine_matches)
            matched = sum(doctrine_matches)
            report[mode] = {
                "total": total,
                "matched": matched,
                "coverage": matched / total if total else 0.0
            }
        logger.info(f"Coverage report: {report}")
        return report

    def export_jsonl(self, path: str) -> int:
        p = pathlib.Path(path)
        count = 0
        with p.open("w", encoding="utf-8") as f:
            for q in self._queries:
                f.write(json.dumps(dataclass_to_dict(q)) + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {path}")
        return count

def dataclass_to_dict(instance):
    if hasattr(instance, "__dataclass_fields__"):
        return {k: dataclass_to_dict(v) for k, v in instance.__dict__.items()}
    elif isinstance(instance, (list, tuple)):
        return [dataclass_to_dict(i) for i in instance]
    elif isinstance(instance, dict):
        return {k: dataclass_to_dict(v) for k, v in instance.items()}
    else:
        return instance

class AuditTrailWriter:
    def __init__(self, audit_dir: Optional[str] = None):
        if audit_dir is None:
            audit_dir = "./audit_trail"
        self.audit_dir = pathlib.Path(audit_dir)
        self.audit_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"AuditTrailWriter initialized at {self.audit_dir}")

    def write(self, metrics: QueryMetrics):
        filename = self._get_filename(metrics.query_id)
        record = dataclass_to_dict(metrics)
        record["audit_timestamp"] = time.time()
        with open(filename, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
        logger.debug(f"Wrote audit trail for query {metrics.query_id} to {filename}")

    def _get_filename(self, query_id: str) -> str:
        hash_digest = hashlib.sha256(query_id.encode()).hexdigest()
        filename = self.audit_dir / f"{hash_digest}.jsonl"
        return str(filename)

COLLECTOR = TelemetryCollector()