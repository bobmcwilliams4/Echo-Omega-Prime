import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any, Tuple
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "ENRG01"

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
        self._queries: deque = deque(maxlen=max_queries)
        self._errors: deque = deque(maxlen=max_queries)
        self._query_index: Dict[str, QueryMetrics] = {}
        self._error_counter: Counter = Counter()
        self._doctrine_counter: Counter = Counter()
        self._cache_counter: Counter = Counter()
        self._mode_counter: Counter = Counter()
        self._confidence_values: List[float] = []
        self._audit_writer = AuditTrailWriter()
        self._last_export_path: Optional[pathlib.Path] = None

    def record_query(self, metrics: QueryMetrics):
        logger.debug(f"Recording query: {metrics.query_id}")
        self._queries.append(metrics)
        self._query_index[metrics.query_id] = metrics
        self._doctrine_counter[metrics.doctrine_matched] += 1
        self._cache_counter[metrics.cache_hit] += 1
        self._mode_counter[metrics.mode] += 1
        self._confidence_values.append(metrics.confidence)
        self._audit_writer.write(metrics)
        if metrics.error:
            self.record_error("query_error", metrics.error, metrics.query_id)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        timestamp = time.time()
        error_entry = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "engine_id": self.engine_id,
            "timestamp": timestamp
        }
        logger.error(f"Recording error: {error_entry}")
        self._errors.append(error_entry)
        self._error_counter[error_type] += 1
        self._audit_writer.write_error(error_entry)

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = [q.latency_ms for q in self._queries if q.latency_ms is not None]
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
        p50 = statistics.median(latencies_sorted)
        p95 = latencies_sorted[int(0.95 * len(latencies_sorted)) - 1]
        p99 = latencies_sorted[int(0.99 * len(latencies_sorted)) - 1]
        min_latency = min(latencies_sorted)
        max_latency = max(latencies_sorted)
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
        if total == 0:
            return 0.0
        hits = self._doctrine_counter.get(True, 0)
        return hits / total

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        queries_in_window = [q for q in self._queries if q.timestamp >= window_start]
        total_queries = len(queries_in_window)
        if total_queries == 0:
            return 0.0
        return len(errors_in_window) / total_queries

    def queries_last_hour(self) -> int:
        now = time.time()
        hour_ago = now - 3600
        return sum(1 for q in self._queries if q.timestamp >= hour_ago)

    def get_coverage_report(self) -> Dict[str, Any]:
        total_queries = len(self._queries)
        doctrine_hits = self._doctrine_counter.get(True, 0)
        cache_hits = self._cache_counter.get(True, 0)
        error_count = sum(1 for q in self._queries if q.error)
        mode_distribution = dict(self._mode_counter)
        confidence_stats = self._get_confidence_stats()
        return {
            "engine_id": self.engine_id,
            "total_queries": total_queries,
            "doctrine_hits": doctrine_hits,
            "doctrine_hit_rate": self.get_doctrine_hit_rate(),
            "cache_hits": cache_hits,
            "cache_hit_rate": cache_hits / total_queries if total_queries else 0.0,
            "error_count": error_count,
            "error_rate": error_count / total_queries if total_queries else 0.0,
            "mode_distribution": mode_distribution,
            "confidence_stats": confidence_stats
        }

    def _get_confidence_stats(self) -> Dict[str, Any]:
        values = self._confidence_values
        if not values:
            return {
                "avg": None,
                "min": None,
                "max": None,
                "p50": None,
                "p95": None,
                "p99": None
            }
        values_sorted = sorted(values)
        avg = statistics.mean(values)
        min_val = min(values)
        max_val = max(values)
        p50 = statistics.median(values_sorted)
        p95 = values_sorted[int(0.95 * len(values_sorted)) - 1]
        p99 = values_sorted[int(0.99 * len(values_sorted)) - 1]
        return {
            "avg": avg,
            "min": min_val,
            "max": max_val,
            "p50": p50,
            "p95": p95,
            "p99": p99
        }

    def export_jsonl(self, path: str) -> int:
        export_path = pathlib.Path(path)
        count = 0
        with export_path.open("w", encoding="utf-8") as f:
            for q in self._queries:
                f.write(json.dumps(asdict(q)) + "\n")
                count += 1
        self._last_export_path = export_path
        logger.info(f"Exported {count} queries to {export_path}")
        return count

class AuditTrailWriter:
    def __init__(self, base_path: Optional[str] = None):
        self.base_path = pathlib.Path(base_path) if base_path else pathlib.Path("./audit_trails")
        self.base_path.mkdir(parents=True, exist_ok=True)
        self._file_handles: Dict[str, Any] = {}

    def _get_file_path(self, query_id: str) -> pathlib.Path:
        hash_id = hashlib.sha256(query_id.encode()).hexdigest()[:12]
        file_name = f"{ENGINE_ID}_{hash_id}.jsonl"
        return self.base_path / file_name

    def write(self, metrics: QueryMetrics):
        file_path = self._get_file_path(metrics.query_id)
        with file_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(metrics)) + "\n")
        logger.debug(f"Audit trail written for query {metrics.query_id} at {file_path}")

    def write_error(self, error_entry: Dict[str, Any]):
        query_id = error_entry.get("query_id", "unknown")
        file_path = self._get_file_path(query_id)
        with file_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"error": error_entry}) + "\n")
        logger.debug(f"Audit error written for query {query_id} at {file_path}")

COLLECTOR = TelemetryCollector(engine_id=ENGINE_ID)