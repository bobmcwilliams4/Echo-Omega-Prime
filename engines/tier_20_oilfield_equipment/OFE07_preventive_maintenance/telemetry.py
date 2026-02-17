import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "OFE07"

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
    def __init__(self, max_queries: int = 10000, max_errors: int = 1000):
        self._queries: deque = deque(maxlen=max_queries)
        self._errors: deque = deque(maxlen=max_errors)
        self._query_index: Dict[str, QueryMetrics] = {}
        self._error_counter: Counter = Counter()
        self._doctrine_counter: Counter = Counter()
        self._cache_hit_counter: Counter = Counter()
        self._mode_counter: Counter = Counter()
        self._confidence_values: List[float] = []
        self._audit_writer = AuditTrailWriter()
        logger.info("TelemetryCollector initialized for engine {}", ENGINE_ID)

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._query_index[metrics.query_id] = metrics
        self._doctrine_counter[metrics.doctrine_matched] += 1
        self._cache_hit_counter[metrics.cache_hit] += 1
        self._mode_counter[metrics.mode] += 1
        self._confidence_values.append(metrics.confidence)
        if metrics.error:
            self.record_error(metrics.error, metrics.error, metrics.query_id)
        self._audit_writer.write(metrics)
        logger.debug("Recorded query: {}", metrics)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "error_type": error_type,
            "message": message,
            "timestamp": time.time(),
            "query_id": query_id,
            "engine_id": ENGINE_ID
        }
        self._errors.append(error_entry)
        self._error_counter[error_type] += 1
        logger.warning("Recorded error: {} for query_id {}", error_type, query_id)

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = [q.latency_ms for q in self._queries if q.latency_ms is not None]
        if not latencies:
            return {
                "avg": None, "p50": None, "p95": None, "p99": None,
                "min": None, "max": None
            }
        latencies_sorted = sorted(latencies)
        stats = {
            "avg": statistics.mean(latencies),
            "p50": statistics.median(latencies),
            "p95": latencies_sorted[int(0.95 * len(latencies_sorted)) - 1],
            "p99": latencies_sorted[int(0.99 * len(latencies_sorted)) - 1],
            "min": min(latencies),
            "max": max(latencies)
        }
        logger.info("Latency stats: {}", stats)
        return stats

    def get_doctrine_hit_rate(self) -> float:
        total = sum(self._doctrine_counter.values())
        hits = self._doctrine_counter.get(True, 0)
        hit_rate = hits / total if total > 0 else 0.0
        logger.info("Doctrine hit rate: {:.2%}", hit_rate)
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        queries_in_window = [q for q in self._queries if q.timestamp >= window_start]
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        query_count = len(queries_in_window)
        error_count = len(errors_in_window)
        error_rate = error_count / query_count if query_count > 0 else 0.0
        logger.info("Error rate in last {:.2f} hours: {:.2%}", window_hours, error_rate)
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= one_hour_ago)
        logger.info("Queries in last hour: {}", count)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        total_queries = len(self._queries)
        doctrine_hits = self._doctrine_counter.get(True, 0)
        cache_hits = self._cache_hit_counter.get(True, 0)
        modes = dict(self._mode_counter)
        avg_confidence = statistics.mean(self._confidence_values) if self._confidence_values else None
        report = {
            "total_queries": total_queries,
            "doctrine_hits": doctrine_hits,
            "doctrine_hit_rate": self.get_doctrine_hit_rate(),
            "cache_hits": cache_hits,
            "cache_hit_rate": cache_hits / total_queries if total_queries > 0 else 0.0,
            "modes": modes,
            "avg_confidence": avg_confidence,
            "error_count": len(self._errors),
            "error_types": dict(self._error_counter)
        }
        logger.info("Coverage report: {}", report)
        return report

    def export_jsonl(self, path: str) -> int:
        p = pathlib.Path(path)
        count = 0
        with p.open("w", encoding="utf-8") as f:
            for q in self._queries:
                f.write(json.dumps(dataclass_to_dict(q)) + "\n")
                count += 1
        logger.info("Exported {} queries to {}", count, path)
        return count

class AuditTrailWriter:
    def __init__(self, base_path: Optional[str] = None):
        self.base_path = base_path or "./audit_trail"
        pathlib.Path(self.base_path).mkdir(parents=True, exist_ok=True)
        logger.info("AuditTrailWriter initialized at {}", self.base_path)

    def write(self, metrics: QueryMetrics):
        filename = self._get_filename(metrics)
        filepath = pathlib.Path(self.base_path) / filename
        entry = dataclass_to_dict(metrics)
        with filepath.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        logger.debug("Audit trail written for query_id {} to {}", metrics.query_id, filepath)

    def _get_filename(self, metrics: QueryMetrics) -> str:
        date_str = time.strftime("%Y%m%d", time.localtime(metrics.timestamp))
        return f"{ENGINE_ID}_audit_{date_str}.jsonl"

def dataclass_to_dict(obj):
    if hasattr(obj, "__dataclass_fields__"):
        return {k: dataclass_to_dict(v) for k, v in obj.__dict__.items()}
    elif isinstance(obj, (list, tuple)):
        return [dataclass_to_dict(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: dataclass_to_dict(v) for k, v in obj.items()}
    else:
        return obj

COLLECTOR = TelemetryCollector()