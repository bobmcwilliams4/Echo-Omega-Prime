import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict, field
from typing import Optional, List, Dict, Any, Union
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "PROD01"

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
    def __init__(self, maxlen: int = 10000):
        self._queries: deque[QueryMetrics] = deque(maxlen=maxlen)
        self._errors: deque[Dict[str, Any]] = deque(maxlen=maxlen)
        self._doctrine_counter: Counter = Counter()
        self._cache_hit_counter: Counter = Counter()
        self._mode_counter: Counter = Counter()
        self._confidence_values: List[float] = []
        self._latencies: List[float] = []
        self._query_time_index: deque[float] = deque(maxlen=maxlen)
        self._audit_writer = AuditTrailWriter()
        logger.info(f"TelemetryCollector initialized for engine {ENGINE_ID}")

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_counter[metrics.doctrine_matched] += 1
        self._cache_hit_counter[metrics.cache_hit] += 1
        self._mode_counter[metrics.mode] += 1
        self._confidence_values.append(metrics.confidence)
        self._query_time_index.append(metrics.timestamp)
        self._audit_writer.write(metrics)
        logger.debug(f"Recorded query: {metrics.query_id}")

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "timestamp": time.time(),
            "engine_id": ENGINE_ID
        }
        self._errors.append(error_entry)
        logger.error(f"Error recorded: {error_type} - {message} (query_id={query_id})")
        self._audit_writer.write_error(error_entry)

    def get_latency_stats(self) -> Dict[str, Union[float, None]]:
        latencies = [q.latency_ms for q in self._queries if q.latency_ms is not None]
        if not latencies:
            return dict(avg=None, p50=None, p95=None, p99=None, min=None, max=None)
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = latencies_sorted[int(0.95 * len(latencies_sorted))-1]
        p99 = latencies_sorted[int(0.99 * len(latencies_sorted))-1]
        min_v = min(latencies)
        max_v = max(latencies)
        logger.info(f"Latency stats calculated: avg={avg}, p50={p50}, p95={p95}, p99={p99}, min={min_v}, max={max_v}")
        return dict(avg=avg, p50=p50, p95=p95, p99=p99, min=min_v, max=max_v)

    def get_doctrine_hit_rate(self) -> float:
        total = sum(self._doctrine_counter.values())
        if total == 0:
            return 0.0
        hit_rate = self._doctrine_counter[True] / total
        logger.info(f"Doctrine hit rate: {hit_rate}")
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        error_count = sum(1 for e in self._errors if e["timestamp"] >= window_start)
        query_count = sum(1 for t in self._query_time_index if t >= window_start)
        if query_count == 0:
            return 0.0
        error_rate = error_count / query_count
        logger.info(f"Error rate over last {window_hours} hours: {error_rate}")
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for t in self._query_time_index if t >= one_hour_ago)
        logger.info(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        total = len(self._queries)
        if total == 0:
            return {
                "total_queries": 0,
                "cache_hit_rate": None,
                "doctrine_hit_rate": None,
                "mode_distribution": {},
                "confidence_avg": None,
                "confidence_min": None,
                "confidence_max": None
            }
        cache_hit_rate = self._cache_hit_counter[True] / total
        doctrine_hit_rate = self._doctrine_counter[True] / total
        mode_distribution = {k: v / total for k, v in self._mode_counter.items()}
        confidence_avg = statistics.mean(self._confidence_values) if self._confidence_values else None
        confidence_min = min(self._confidence_values) if self._confidence_values else None
        confidence_max = max(self._confidence_values) if self._confidence_values else None
        report = {
            "total_queries": total,
            "cache_hit_rate": cache_hit_rate,
            "doctrine_hit_rate": doctrine_hit_rate,
            "mode_distribution": mode_distribution,
            "confidence_avg": confidence_avg,
            "confidence_min": confidence_min,
            "confidence_max": confidence_max
        }
        logger.info(f"Coverage report generated: {report}")
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
    def __init__(self, base_dir: Union[str, pathlib.Path] = "./audit_trail"):
        self.base_dir = pathlib.Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"AuditTrailWriter initialized at {self.base_dir}")

    def _get_query_audit_path(self, query_id: str) -> pathlib.Path:
        h = hashlib.sha256(query_id.encode()).hexdigest()
        subdir = self.base_dir / h[:2]
        subdir.mkdir(parents=True, exist_ok=True)
        return subdir / f"{query_id}.jsonl"

    def write(self, metrics: QueryMetrics):
        path = self._get_query_audit_path(metrics.query_id)
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(metrics)) + "\n")
        logger.debug(f"Audit trail written for query {metrics.query_id}")

    def write_error(self, error_entry: Dict[str, Any]):
        query_id = error_entry.get("query_id", "unknown")
        path = self._get_query_audit_path(str(query_id))
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"error": error_entry}) + "\n")
        logger.debug(f"Audit trail error written for query {query_id}")

COLLECTOR = TelemetryCollector()