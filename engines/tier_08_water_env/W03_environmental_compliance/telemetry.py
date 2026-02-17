import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "W03"

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
    def __init__(self, engine_id: str = ENGINE_ID, maxlen: int = 10000):
        self.engine_id = engine_id
        self._queries = deque(maxlen=maxlen)
        self._errors = deque(maxlen=maxlen)
        self._query_index = {}
        self._doctrine_counter = Counter()
        self._cache_counter = Counter()
        self._mode_counter = Counter()
        self._confidence_values = []
        self._latency_values = []
        self._coverage_counter = defaultdict(int)
        self._audit_writer = AuditTrailWriter()
        logger.info(f"TelemetryCollector initialized for engine {engine_id}")

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._query_index[metrics.query_id] = metrics
        self._latency_values.append(metrics.latency_ms)
        self._doctrine_counter['matched' if metrics.doctrine_matched else 'not_matched'] += 1
        self._cache_counter['hit' if metrics.cache_hit else 'miss'] += 1
        self._mode_counter[metrics.mode] += 1
        self._confidence_values.append(metrics.confidence)
        self._coverage_counter[(metrics.mode, metrics.doctrine_matched)] += 1
        self._audit_writer.write(metrics)
        logger.debug(f"Recorded query: {metrics.query_id}")

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "engine_id": self.engine_id,
            "error_type": error_type,
            "message": message,
            "query_id": query_id
        }
        self._errors.append(error_entry)
        logger.error(f"Error recorded: {error_type} ({query_id}) - {message}")

    def get_latency_stats(self) -> Dict[str, Any]:
        values = [q.latency_ms for q in self._queries if q.latency_ms is not None]
        if not values:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        values_sorted = sorted(values)
        avg = statistics.mean(values)
        p50 = statistics.median(values)
        p95 = values_sorted[int(0.95 * len(values_sorted)) - 1]
        p99 = values_sorted[int(0.99 * len(values_sorted)) - 1]
        minv = min(values)
        maxv = max(values)
        logger.info(f"Latency stats: avg={avg}, p50={p50}, p95={p95}, p99={p99}, min={minv}, max={maxv}")
        return {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": minv,
            "max": maxv
        }

    def get_doctrine_hit_rate(self) -> float:
        total = self._doctrine_counter['matched'] + self._doctrine_counter['not_matched']
        if total == 0:
            return 0.0
        hit_rate = self._doctrine_counter['matched'] / total
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
        report = {
            "total_queries": len(self._queries),
            "modes": dict(self._mode_counter),
            "doctrine_matched": self._doctrine_counter['matched'],
            "doctrine_not_matched": self._doctrine_counter['not_matched'],
            "cache_hit": self._cache_counter['hit'],
            "cache_miss": self._cache_counter['miss'],
            "confidence_avg": statistics.mean(self._confidence_values) if self._confidence_values else None,
            "coverage_by_mode": dict(self._coverage_counter)
        }
        logger.info(f"Coverage report generated: {report}")
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

class AuditTrailWriter:
    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = base_dir or "./audit_trail"
        pathlib.Path(self.base_dir).mkdir(parents=True, exist_ok=True)
        logger.info(f"AuditTrailWriter initialized at {self.base_dir}")

    def write(self, metrics: QueryMetrics):
        filename = self._get_filename(metrics.query_id)
        path = pathlib.Path(self.base_dir) / filename
        entry = dataclass_to_dict(metrics)
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        logger.debug(f"Audit trail written for query {metrics.query_id} at {path}")

    def _get_filename(self, query_id: str) -> str:
        hashval = hashlib.sha256(query_id.encode()).hexdigest()[:8]
        return f"audit_{hashval}.jsonl"

def dataclass_to_dict(instance: Any) -> Dict[str, Any]:
    if hasattr(instance, "__dataclass_fields__"):
        result = {}
        for field_ in instance.__dataclass_fields__:
            value = getattr(instance, field_)
            if hasattr(value, "__dataclass_fields__"):
                result[field_] = dataclass_to_dict(value)
            else:
                result[field_] = value
        return result
    elif isinstance(instance, dict):
        return {k: dataclass_to_dict(v) for k, v in instance.items()}
    elif isinstance(instance, list):
        return [dataclass_to_dict(v) for v in instance]
    else:
        return instance

COLLECTOR = TelemetryCollector(engine_id=ENGINE_ID)