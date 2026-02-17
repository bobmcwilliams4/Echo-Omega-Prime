import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any, Union
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "SYN07"

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
        self._query_index: Dict[str, QueryMetrics] = {}
        self._doctrine_counter: Counter = Counter()
        self._cache_counter: Counter = Counter()
        self._mode_counter: Counter = Counter()
        self._confidence_list: List[float] = []
        self._latency_list: List[float] = []
        self._error_counter: Counter = Counter()
        self._coverage_counter: Counter = Counter()
        self._audit_writer = AuditTrailWriter()
        logger.info(f"TelemetryCollector initialized for engine {ENGINE_ID}")

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._query_index[metrics.query_id] = metrics
        self._latency_list.append(metrics.latency_ms)
        self._doctrine_counter[metrics.doctrine_matched] += 1
        self._cache_counter[metrics.cache_hit] += 1
        self._mode_counter[metrics.mode] += 1
        self._confidence_list.append(metrics.confidence)
        if metrics.error:
            self._error_counter[metrics.error] += 1
        self._coverage_counter[metrics.doctrine_matched] += 1
        self._audit_writer.write(metrics)
        logger.debug(f"Recorded query: {metrics.query_id}")

    def record_error(self, error_type: str, message: str, query_id: Optional[str]):
        error_entry = {
            "timestamp": time.time(),
            "engine_id": ENGINE_ID,
            "error_type": error_type,
            "message": message,
            "query_id": query_id
        }
        self._errors.append(error_entry)
        self._error_counter[error_type] += 1
        logger.error(f"Error recorded: {error_type} for query {query_id}: {message}")

    def get_latency_stats(self) -> Dict[str, Union[float, None]]:
        latencies = [m.latency_ms for m in self._queries if m.latency_ms is not None]
        if not latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies_sorted)
        p50 = statistics.median(latencies_sorted)
        p95 = latencies_sorted[int(0.95 * len(latencies_sorted)) - 1]
        p99 = latencies_sorted[int(0.99 * len(latencies_sorted)) - 1]
        min_latency = min(latencies_sorted)
        max_latency = max(latencies_sorted)
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
        total = sum(self._doctrine_counter.values())
        hits = self._doctrine_counter.get(True, 0)
        hit_rate = hits / total if total > 0 else 0.0
        logger.info(f"Doctrine hit rate: {hit_rate}")
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        error_count = sum(1 for e in self._errors if e["timestamp"] >= window_start)
        query_count = sum(1 for q in self._queries if q.timestamp >= window_start)
        error_rate = error_count / query_count if query_count > 0 else 0.0
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
        doctrine_hits = self._coverage_counter.get(True, 0)
        doctrine_misses = self._coverage_counter.get(False, 0)
        mode_distribution = dict(self._mode_counter)
        cache_distribution = dict(self._cache_counter)
        confidence_stats = {
            "avg": statistics.mean(self._confidence_list) if self._confidence_list else None,
            "min": min(self._confidence_list) if self._confidence_list else None,
            "max": max(self._confidence_list) if self._confidence_list else None,
            "p50": statistics.median(self._confidence_list) if self._confidence_list else None,
        }
        report = {
            "total_queries": total,
            "doctrine_hits": doctrine_hits,
            "doctrine_misses": doctrine_misses,
            "doctrine_hit_rate": doctrine_hits / total if total > 0 else 0.0,
            "mode_distribution": mode_distribution,
            "cache_distribution": cache_distribution,
            "confidence_stats": confidence_stats,
            "error_types": dict(self._error_counter)
        }
        logger.info(f"Coverage report generated: {report}")
        return report

    def export_jsonl(self, path: Union[str, pathlib.Path]) -> int:
        path = pathlib.Path(path)
        count = 0
        with path.open("w", encoding="utf-8") as f:
            for metrics in self._queries:
                f.write(json.dumps(asdict(metrics)) + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {path}")
        return count

class AuditTrailWriter:
    def __init__(self, base_path: Union[str, pathlib.Path] = "./audit_trail"):
        self.base_path = pathlib.Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"AuditTrailWriter initialized at {self.base_path}")

    def _get_audit_path(self, query_id: str) -> pathlib.Path:
        hash_digest = hashlib.sha256(query_id.encode()).hexdigest()
        subdir = hash_digest[:2]
        audit_dir = self.base_path / subdir
        audit_dir.mkdir(parents=True, exist_ok=True)
        audit_path = audit_dir / f"{query_id}.jsonl"
        return audit_path

    def write(self, metrics: QueryMetrics):
        audit_path = self._get_audit_path(metrics.query_id)
        with audit_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(metrics)) + "\n")
        logger.debug(f"Audit trail written for query {metrics.query_id} at {audit_path}")

COLLECTOR = TelemetryCollector()