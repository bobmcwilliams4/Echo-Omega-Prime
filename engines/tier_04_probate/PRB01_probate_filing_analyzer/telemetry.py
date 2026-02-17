import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Union
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "PRB01"


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

    def to_dict(self) -> Dict[str, Any]:
        return {
            "query_id": self.query_id,
            "engine_id": self.engine_id,
            "timestamp": self.timestamp,
            "latency_ms": self.latency_ms,
            "cache_hit": self.cache_hit,
            "doctrine_matched": self.doctrine_matched,
            "mode": self.mode,
            "confidence": self.confidence,
            "error": self.error,
        }


class TelemetryCollector:
    def __init__(self, engine_id: str = ENGINE_ID, max_queries: int = 10000):
        self.engine_id = engine_id
        self._queries: deque = deque(maxlen=max_queries)
        self._errors: deque = deque(maxlen=max_queries)
        self._query_index: Dict[str, QueryMetrics] = {}
        self._error_index: Dict[str, Dict[str, Any]] = {}
        self._doctrine_hits: int = 0
        self._doctrine_total: int = 0
        self._latencies: List[float] = []
        self._coverage_counter: Counter = Counter()
        self._audit_writer = AuditTrailWriter()
        logger.info(f"TelemetryCollector initialized for engine {engine_id}")

    def record_query(self, metrics: QueryMetrics):
        logger.debug(f"Recording query: {metrics.query_id}")
        self._queries.append(metrics)
        self._query_index[metrics.query_id] = metrics
        self._latencies.append(metrics.latency_ms)
        self._doctrine_total += 1
        if metrics.doctrine_matched:
            self._doctrine_hits += 1
        self._coverage_counter[metrics.mode] += 1
        self._audit_writer.write(metrics)
        if metrics.error:
            self.record_error("query_error", metrics.error, metrics.query_id)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        timestamp = time.time()
        error_record = {
            "error_type": error_type,
            "message": message,
            "timestamp": timestamp,
            "query_id": query_id,
            "engine_id": self.engine_id,
        }
        logger.error(f"Error recorded: {error_record}")
        self._errors.append(error_record)
        if query_id:
            self._error_index[query_id] = error_record
        self._audit_writer.write_error(error_record)

    def get_latency_stats(self) -> Dict[str, Union[float, None]]:
        latencies = [q.latency_ms for q in self._queries if q.latency_ms is not None]
        if not latencies:
            return {
                "avg": None,
                "p50": None,
                "p95": None,
                "p99": None,
                "min": None,
                "max": None,
            }
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies_sorted)
        p50 = statistics.median(latencies_sorted)
        p95 = latencies_sorted[int(0.95 * len(latencies_sorted)) - 1]
        p99 = latencies_sorted[int(0.99 * len(latencies_sorted)) - 1]
        min_latency = latencies_sorted[0]
        max_latency = latencies_sorted[-1]
        logger.info(f"Latency stats: avg={avg}, p50={p50}, p95={p95}, p99={p99}, min={min_latency}, max={max_latency}")
        return {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_latency,
            "max": max_latency,
        }

    def get_doctrine_hit_rate(self) -> float:
        if self._doctrine_total == 0:
            return 0.0
        hit_rate = self._doctrine_hits / self._doctrine_total
        logger.info(f"Doctrine hit rate: {hit_rate}")
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        error_count = sum(1 for e in self._errors if e["timestamp"] >= window_start)
        query_count = sum(1 for q in self._queries if q.timestamp >= window_start)
        if query_count == 0:
            return 0.0
        error_rate = error_count / query_count
        logger.info(f"Error rate in last {window_hours} hours: {error_rate}")
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= one_hour_ago)
        logger.info(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        total = sum(self._coverage_counter.values())
        report = {}
        for mode, count in self._coverage_counter.items():
            report[mode] = {
                "count": count,
                "percent": (count / total) * 100 if total > 0 else 0.0
            }
        logger.info(f"Coverage report: {report}")
        return report

    def export_jsonl(self, path: Union[str, pathlib.Path]) -> int:
        path = pathlib.Path(path)
        count = 0
        with path.open("w", encoding="utf-8") as f:
            for q in self._queries:
                f.write(json.dumps(q.to_dict()) + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {path}")
        return count


class AuditTrailWriter:
    def __init__(self, base_dir: Union[str, pathlib.Path] = "./audit_trail"):
        self.base_dir = pathlib.Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
        self._query_audit_path = self.base_dir / "queries.jsonl"
        self._error_audit_path = self.base_dir / "errors.jsonl"
        self._query_audit_file = self._query_audit_path.open("a", encoding="utf-8")
        self._error_audit_file = self._error_audit_path.open("a", encoding="utf-8")
        logger.info(f"AuditTrailWriter initialized at {self.base_dir}")

    def write(self, metrics: QueryMetrics):
        record = metrics.to_dict()
        self._query_audit_file.write(json.dumps(record) + "\n")
        self._query_audit_file.flush()
        logger.debug(f"Audit trail written for query {metrics.query_id}")

    def write_error(self, error_record: Dict[str, Any]):
        self._error_audit_file.write(json.dumps(error_record) + "\n")
        self._error_audit_file.flush()
        logger.debug(f"Audit trail written for error {error_record.get('query_id')}")

    def close(self):
        self._query_audit_file.close()
        self._error_audit_file.close()


COLLECTOR = TelemetryCollector(engine_id=ENGINE_ID)