import time
import json
import hashlib
import statistics
import pathlib
import dataclasses
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Union
import collections
from loguru import logger

ENGINE_ID = "MED12"

@dataclass
class QueryMetrics:
    query_id: str
    engine_id: str = ENGINE_ID
    timestamp: float = field(default_factory=lambda: time.time())
    latency_ms: float = 0.0
    cache_hit: bool = False
    doctrine_matched: bool = False
    mode: str = ""
    confidence: float = 0.0
    error: Optional[str] = None

class TelemetryCollector:
    def __init__(self):
        self._queries: List[QueryMetrics] = []
        self._errors: List[Dict[str, Any]] = []
        self._doctrine_hits: int = 0
        self._doctrine_total: int = 0
        self._latencies: List[float] = []
        self._query_times: List[float] = []
        self._query_id_index: Dict[str, QueryMetrics] = {}
        self._coverage_modes: collections.Counter = collections.Counter()
        self._audit_writer = AuditTrailWriter()
        logger.info("TelemetryCollector initialized for engine {}", ENGINE_ID)

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._query_id_index[metrics.query_id] = metrics
        self._latencies.append(metrics.latency_ms)
        self._query_times.append(metrics.timestamp)
        self._coverage_modes[metrics.mode] += 1
        self._doctrine_total += 1
        if metrics.doctrine_matched:
            self._doctrine_hits += 1
        if metrics.error:
            self.record_error("query_error", metrics.error, metrics.query_id)
        self._audit_writer.write(metrics)
        logger.debug("Recorded query: {}", metrics)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_record = {
            "timestamp": time.time(),
            "error_type": error_type,
            "message": message,
            "query_id": query_id
        }
        self._errors.append(error_record)
        logger.error("Error recorded: {}", error_record)

    def get_latency_stats(self) -> Dict[str, float]:
        if not self._latencies:
            return {"avg": 0.0, "p50": 0.0, "p95": 0.0, "p99": 0.0, "min": 0.0, "max": 0.0}
        latencies = sorted(self._latencies)
        avg = statistics.mean(latencies)
        min_latency = latencies[0]
        max_latency = latencies[-1]
        p50 = statistics.median(latencies)
        p95 = latencies[int(0.95 * len(latencies)) - 1]
        p99 = latencies[int(0.99 * len(latencies)) - 1]
        stats = {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_latency,
            "max": max_latency
        }
        logger.info("Latency stats: {}", stats)
        return stats

    def get_doctrine_hit_rate(self) -> float:
        if self._doctrine_total == 0:
            return 0.0
        hit_rate = self._doctrine_hits / self._doctrine_total
        logger.info("Doctrine hit rate: {}", hit_rate)
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        total_queries = sum(1 for t in self._query_times if t >= window_start)
        total_errors = sum(1 for e in self._errors if e["timestamp"] >= window_start)
        if total_queries == 0:
            return 0.0
        error_rate = total_errors / total_queries
        logger.info("Error rate ({}h): {}", window_hours, error_rate)
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for t in self._query_times if t >= one_hour_ago)
        logger.info("Queries in last hour: {}", count)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        total = sum(self._coverage_modes.values())
        report = {}
        for mode, count in self._coverage_modes.items():
            report[mode] = {
                "count": count,
                "percent": (count / total * 100) if total > 0 else 0.0
            }
        logger.info("Coverage report: {}", report)
        return report

    def export_jsonl(self, path: Union[str, pathlib.Path]) -> int:
        path = pathlib.Path(path)
        count = 0
        with path.open("w", encoding="utf-8") as f:
            for metrics in self._queries:
                f.write(json.dumps(dataclasses.asdict(metrics)) + "\n")
                count += 1
        logger.info("Exported {} queries to {}", count, str(path))
        return count

class AuditTrailWriter:
    def __init__(self, base_dir: Union[str, pathlib.Path] = "audit_trail"):
        self.base_dir = pathlib.Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        logger.info("AuditTrailWriter initialized at {}", str(self.base_dir))

    def _get_audit_path(self, query_id: str) -> pathlib.Path:
        hash_digest = hashlib.sha256(query_id.encode()).hexdigest()
        subdir = hash_digest[:2]
        dir_path = self.base_dir / subdir
        dir_path.mkdir(exist_ok=True)
        file_path = dir_path / f"{query_id}.jsonl"
        return file_path

    def write(self, metrics: QueryMetrics):
        file_path = self._get_audit_path(metrics.query_id)
        with file_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(dataclasses.asdict(metrics)) + "\n")
        logger.debug("Audit trail written for query_id {}", metrics.query_id)

COLLECTOR = TelemetryCollector()