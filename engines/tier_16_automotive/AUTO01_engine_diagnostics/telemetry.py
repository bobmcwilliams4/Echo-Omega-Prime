import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Tuple
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "AUTO01"

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
        self._audit_trail: deque = deque(maxlen=10000)
        self._query_id_index: Dict[str, QueryMetrics] = {}
        self._error_counter: Counter = Counter()
        self._doctrine_counter: Counter = Counter()
        self._latencies: List[float] = []
        self._cache_hits: List[bool] = []
        self._coverage_modes: Counter = Counter()
        self._coverage_confidence: List[float] = []
        self._coverage_doctrine: Counter = Counter()
        self._coverage_cache: Counter = Counter()
        self._coverage_errors: Counter = Counter()
        self._audit_writer = AuditTrailWriter()
        logger.info(f"TelemetryCollector initialized for engine {engine_id}")

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._query_id_index[metrics.query_id] = metrics
        self._latencies.append(metrics.latency_ms)
        self._cache_hits.append(metrics.cache_hit)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._coverage_modes[metrics.mode] += 1
        self._coverage_confidence.append(metrics.confidence)
        self._coverage_doctrine[metrics.doctrine_matched] += 1
        self._coverage_cache[metrics.cache_hit] += 1
        if metrics.error:
            self._coverage_errors[metrics.error] += 1
        self._audit_writer.write(metrics)
        logger.debug(f"Recorded query: {metrics.query_id}, latency: {metrics.latency_ms}ms, cache_hit: {metrics.cache_hit}, doctrine_matched: {metrics.doctrine_matched}")

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "engine_id": self.engine_id,
            "error_type": error_type,
            "message": message,
            "timestamp": time.time(),
            "query_id": query_id
        }
        self._errors.append(error_entry)
        self._error_counter[error_type] += 1
        logger.error(f"Error recorded: {error_type} - {message} (query_id={query_id})")

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = [q.latency_ms for q in self._queries if q.latency_ms is not None]
        if not latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies_sorted)
        p50 = statistics.median(latencies_sorted)
        p95 = latencies_sorted[int(0.95 * len(latencies_sorted))-1]
        p99 = latencies_sorted[int(0.99 * len(latencies_sorted))-1]
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
        total = len(self._doctrine_hits)
        if total == 0:
            return 0.0
        hits = sum(1 for hit in self._doctrine_hits if hit)
        rate = hits / total
        logger.info(f"Doctrine hit rate: {rate} ({hits}/{total})")
        return rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        queries_in_window = [q for q in self._queries if q.timestamp >= window_start]
        error_count = len(errors_in_window)
        query_count = len(queries_in_window)
        if query_count == 0:
            return 0.0
        rate = error_count / query_count
        logger.info(f"Error rate in last {window_hours}h: {rate} ({error_count}/{query_count})")
        return rate

    def queries_last_hour(self) -> int:
        now = time.time()
        hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= hour_ago)
        logger.info(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        total_queries = len(self._queries)
        if total_queries == 0:
            return {
                "total_queries": 0,
                "mode_distribution": {},
                "avg_confidence": None,
                "doctrine_matched_rate": None,
                "cache_hit_rate": None,
                "error_distribution": {},
            }
        mode_dist = dict(self._coverage_modes)
        avg_confidence = statistics.mean(self._coverage_confidence) if self._coverage_confidence else None
        doctrine_matched_rate = self._coverage_doctrine[True] / total_queries if True in self._coverage_doctrine else 0.0
        cache_hit_rate = self._coverage_cache[True] / total_queries if True in self._coverage_cache else 0.0
        error_dist = dict(self._coverage_errors)
        logger.info(f"Coverage report: total_queries={total_queries}, mode_dist={mode_dist}, avg_confidence={avg_confidence}, doctrine_matched_rate={doctrine_matched_rate}, cache_hit_rate={cache_hit_rate}, error_dist={error_dist}")
        return {
            "total_queries": total_queries,
            "mode_distribution": mode_dist,
            "avg_confidence": avg_confidence,
            "doctrine_matched_rate": doctrine_matched_rate,
            "cache_hit_rate": cache_hit_rate,
            "error_distribution": error_dist,
        }

    def export_jsonl(self, path: str) -> int:
        export_path = pathlib.Path(path)
        export_path.parent.mkdir(parents=True, exist_ok=True)
        count = 0
        with export_path.open("w", encoding="utf-8") as f:
            for q in self._queries:
                f.write(json.dumps(dataclasses.asdict(q)) + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {export_path}")
        return count

class AuditTrailWriter:
    def __init__(self, base_path: Optional[str] = None):
        self.base_path = base_path or "./audit_trail"
        self._path_obj = pathlib.Path(self.base_path)
        self._path_obj.mkdir(parents=True, exist_ok=True)
        logger.info(f"AuditTrailWriter initialized at {self.base_path}")

    def _get_audit_file(self, query_id: str) -> pathlib.Path:
        hash_digest = hashlib.sha256(query_id.encode()).hexdigest()
        filename = f"{hash_digest}.jsonl"
        return self._path_obj / filename

    def write(self, metrics: QueryMetrics):
        audit_file = self._get_audit_file(metrics.query_id)
        with audit_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(dataclasses.asdict(metrics)) + "\n")
        logger.debug(f"Audit trail written for query_id={metrics.query_id} to {audit_file}")

COLLECTOR = TelemetryCollector(engine_id=ENGINE_ID)