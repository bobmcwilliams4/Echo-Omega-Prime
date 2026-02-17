import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "MATH07"

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
        self._queries: deque = deque(maxlen=maxlen)
        self._errors: deque = deque(maxlen=maxlen)
        self._query_index: Dict[str, QueryMetrics] = {}
        self._doctrine_counter: Counter = Counter()
        self._cache_counter: Counter = Counter()
        self._mode_counter: Counter = Counter()
        self._error_counter: Counter = Counter()
        self._coverage_data: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
            "count": 0,
            "confidence_sum": 0.0,
            "doctrine_matched": 0,
            "cache_hit": 0
        })
        self._audit_writer = AuditTrailWriter()
        logger.info("TelemetryCollector initialized with maxlen={}", maxlen)

    def record_query(self, metrics: QueryMetrics):
        logger.debug("Recording query: {}", metrics)
        self._queries.append(metrics)
        self._query_index[metrics.query_id] = metrics
        self._doctrine_counter[metrics.doctrine_matched] += 1
        self._cache_counter[metrics.cache_hit] += 1
        self._mode_counter[metrics.mode] += 1
        if metrics.error:
            self._error_counter[metrics.error] += 1
            self._errors.append({
                "timestamp": metrics.timestamp,
                "error": metrics.error,
                "query_id": metrics.query_id
            })
        self._coverage_data[metrics.mode]["count"] += 1
        self._coverage_data[metrics.mode]["confidence_sum"] += metrics.confidence
        self._coverage_data[metrics.mode]["doctrine_matched"] += int(metrics.doctrine_matched)
        self._coverage_data[metrics.mode]["cache_hit"] += int(metrics.cache_hit)
        self._audit_writer.write(metrics)
        logger.info("Query recorded: {}", metrics.query_id)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        timestamp = time.time()
        logger.error("Error recorded: {} - {} (query_id={})", error_type, message, query_id)
        self._error_counter[error_type] += 1
        self._errors.append({
            "timestamp": timestamp,
            "error": error_type,
            "message": message,
            "query_id": query_id
        })
        if query_id and query_id in self._query_index:
            self._query_index[query_id].error = error_type
        self._audit_writer.write_error(error_type, message, query_id, timestamp)

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = [q.latency_ms for q in self._queries if q.latency_ms is not None]
        logger.debug("Calculating latency stats for {} queries", len(latencies))
        if not latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        min_latency = latencies_sorted[0]
        max_latency = latencies_sorted[-1]
        p50 = statistics.median(latencies_sorted)
        p95 = latencies_sorted[int(0.95 * len(latencies_sorted)) - 1]
        p99 = latencies_sorted[int(0.99 * len(latencies_sorted)) - 1]
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
        total = sum(self._doctrine_counter.values())
        hits = self._doctrine_counter.get(True, 0)
        hit_rate = hits / total if total > 0 else 0.0
        logger.info("Doctrine hit rate: {} ({} hits / {} total)", hit_rate, hits, total)
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        queries_in_window = [q for q in self._queries if q.timestamp >= window_start]
        error_rate = len(errors_in_window) / len(queries_in_window) if queries_in_window else 0.0
        logger.info("Error rate in last {} hours: {} ({} errors / {} queries)", window_hours, error_rate, len(errors_in_window), len(queries_in_window))
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= hour_ago)
        logger.info("Queries in last hour: {}", count)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {}
        logger.debug("Generating coverage report")
        for mode, data in self._coverage_data.items():
            count = data["count"]
            avg_confidence = data["confidence_sum"] / count if count > 0 else 0.0
            doctrine_hit_rate = data["doctrine_matched"] / count if count > 0 else 0.0
            cache_hit_rate = data["cache_hit"] / count if count > 0 else 0.0
            report[mode] = {
                "count": count,
                "avg_confidence": avg_confidence,
                "doctrine_hit_rate": doctrine_hit_rate,
                "cache_hit_rate": cache_hit_rate
            }
        logger.info("Coverage report: {}", report)
        return report

    def export_jsonl(self, path: str) -> int:
        logger.info("Exporting telemetry to JSONL: {}", path)
        p = pathlib.Path(path)
        count = 0
        with p.open("w", encoding="utf-8") as f:
            for q in self._queries:
                f.write(json.dumps(dataclass_to_dict(q)) + "\n")
                count += 1
        logger.info("Exported {} queries to {}", count, path)
        return count

def dataclass_to_dict(obj):
    if isinstance(obj, QueryMetrics):
        return {
            "query_id": obj.query_id,
            "engine_id": obj.engine_id,
            "timestamp": obj.timestamp,
            "latency_ms": obj.latency_ms,
            "cache_hit": obj.cache_hit,
            "doctrine_matched": obj.doctrine_matched,
            "mode": obj.mode,
            "confidence": obj.confidence,
            "error": obj.error
        }
    elif isinstance(obj, dict):
        return obj
    else:
        return dict(obj)

class AuditTrailWriter:
    def __init__(self, audit_dir: str = "./audit_trail"):
        self.audit_dir = pathlib.Path(audit_dir)
        self.audit_dir.mkdir(exist_ok=True)
        logger.info("AuditTrailWriter initialized at {}", self.audit_dir)

    def write(self, metrics: QueryMetrics):
        filename = self._get_audit_filename(metrics.query_id)
        logger.debug("Writing audit trail for query_id={}", metrics.query_id)
        with open(filename, "a", encoding="utf-8") as f:
            f.write(json.dumps(dataclass_to_dict(metrics)) + "\n")

    def write_error(self, error_type: str, message: str, query_id: Optional[str], timestamp: float):
        filename = self._get_audit_filename(query_id or "unknown")
        logger.debug("Writing error audit trail for query_id={}", query_id)
        error_record = {
            "timestamp": timestamp,
            "error": error_type,
            "message": message,
            "query_id": query_id
        }
        with open(filename, "a", encoding="utf-8") as f:
            f.write(json.dumps(error_record) + "\n")

    def _get_audit_filename(self, query_id: str) -> str:
        hash_id = hashlib.sha256(query_id.encode("utf-8")).hexdigest()[:16]
        filename = self.audit_dir / f"{hash_id}.jsonl"
        return str(filename)

COLLECTOR = TelemetryCollector(maxlen=10000)