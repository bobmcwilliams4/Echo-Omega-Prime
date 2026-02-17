import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any, Union
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "CHEM02"

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
    def __init__(self, engine_id: str, max_queries: int = 10000):
        self.engine_id = engine_id
        self._queries = deque(maxlen=max_queries)
        self._errors = deque(maxlen=max_queries)
        self._doctrine_hits = 0
        self._doctrine_total = 0
        self._latencies = []
        self._query_counter = Counter()
        self._error_counter = Counter()
        self._coverage_modes = Counter()
        self._coverage_confidences = []
        self._audit_writer = AuditTrailWriter()
        logger.info(f"TelemetryCollector initialized for engine {engine_id}")

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._query_counter[metrics.mode] += 1
        self._coverage_modes[metrics.mode] += 1
        self._coverage_confidences.append(metrics.confidence)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_total += 1
        if metrics.doctrine_matched:
            self._doctrine_hits += 1
        if metrics.error:
            self.record_error(metrics.error, "Query error", metrics.query_id)
        self._audit_writer.write(metrics)
        logger.debug(f"Recorded query: {metrics}")

    def record_error(self, error_type: str, message: str, query_id: str):
        error_record = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "timestamp": time.time(),
            "engine_id": self.engine_id
        }
        self._errors.append(error_record)
        self._error_counter[error_type] += 1
        logger.warning(f"Recorded error: {error_record}")

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = self._latencies
        if not latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        sorted_latencies = sorted(latencies)
        avg = statistics.mean(latencies)
        min_latency = min(latencies)
        max_latency = max(latencies)
        p50 = statistics.median(sorted_latencies)
        p95 = sorted_latencies[int(0.95 * len(sorted_latencies)) - 1]
        p99 = sorted_latencies[int(0.99 * len(sorted_latencies)) - 1]
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
        if self._doctrine_total == 0:
            return 0.0
        hit_rate = self._doctrine_hits / self._doctrine_total
        logger.info(f"Doctrine hit rate: {hit_rate}")
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        error_count = 0
        query_count = 0
        for q in self._queries:
            if q.timestamp >= window_start:
                query_count += 1
                if q.error:
                    error_count += 1
        if query_count == 0:
            return 0.0
        error_rate = error_count / query_count
        logger.info(f"Error rate in last {window_hours} hours: {error_rate}")
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= hour_ago)
        logger.info(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {
            "mode_distribution": dict(self._coverage_modes),
            "confidence_avg": statistics.mean(self._coverage_confidences) if self._coverage_confidences else None,
            "confidence_min": min(self._coverage_confidences) if self._coverage_confidences else None,
            "confidence_max": max(self._coverage_confidences) if self._coverage_confidences else None,
            "total_queries": len(self._queries),
            "doctrine_hit_rate": self.get_doctrine_hit_rate(),
            "error_rate_last_hour": self.get_error_rate(1.0)
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
    def __init__(self, base_dir: Union[str, pathlib.Path] = "audit_trails"):
        self.base_dir = pathlib.Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"AuditTrailWriter initialized at {self.base_dir}")

    def _get_audit_path(self, query_id: str) -> pathlib.Path:
        hash_id = hashlib.sha256(query_id.encode()).hexdigest()
        subdir = self.base_dir / hash_id[:2]
        subdir.mkdir(parents=True, exist_ok=True)
        path = subdir / f"{hash_id}.jsonl"
        return path

    def write(self, metrics: QueryMetrics):
        path = self._get_audit_path(metrics.query_id)
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(metrics)) + "\n")
        logger.debug(f"Wrote audit trail for query_id={metrics.query_id} at {path}")

COLLECTOR = TelemetryCollector(engine_id=ENGINE_ID)