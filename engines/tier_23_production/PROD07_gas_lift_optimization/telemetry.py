import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional, Any, Union
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "PROD07"

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
        self.metrics: deque = deque(maxlen=maxlen)
        self.errors: deque = deque(maxlen=maxlen)
        self.audit_trail: deque = deque(maxlen=maxlen)
        self.query_counter: Counter = Counter()
        self.doctrine_counter: Counter = Counter()
        self.cache_hit_counter: Counter = Counter()
        self.error_counter: Counter = Counter()
        self.latency_list: List[float] = []
        self.coverage_modes: Counter = Counter()
        self.coverage_confidence: List[float] = []
        self.coverage_doctrine: Counter = Counter()
        self.coverage_cache: Counter = Counter()
        self.coverage_errors: Counter = Counter()
        self.query_times: deque = deque(maxlen=maxlen)
        logger.info("TelemetryCollector initialized.")

    def record_query(self, metrics: QueryMetrics):
        self.metrics.append(metrics)
        self.query_counter[metrics.query_id] += 1
        self.latency_list.append(metrics.latency_ms)
        self.coverage_modes[metrics.mode] += 1
        self.coverage_confidence.append(metrics.confidence)
        self.coverage_doctrine[metrics.doctrine_matched] += 1
        self.coverage_cache[metrics.cache_hit] += 1
        self.query_times.append(metrics.timestamp)
        if metrics.error:
            self.coverage_errors[metrics.error] += 1
            self.record_error(metrics.error, "Query error", metrics.query_id)
        logger.debug(f"Recorded query: {metrics}")

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "timestamp": time.time(),
            "engine_id": ENGINE_ID
        }
        self.errors.append(error_entry)
        self.error_counter[error_type] += 1
        logger.warning(f"Recorded error: {error_entry}")

    def get_latency_stats(self) -> Dict[str, Any]:
        if not self.latency_list:
            return {
                "avg": None,
                "p50": None,
                "p95": None,
                "p99": None,
                "min": None,
                "max": None
            }
        latencies = self.latency_list
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = statistics.quantiles(latencies, n=100)[94] if len(latencies) > 1 else p50
        p99 = statistics.quantiles(latencies, n=100)[98] if len(latencies) > 1 else p50
        min_latency = min(latencies)
        max_latency = max(latencies)
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
        total = sum(self.coverage_doctrine.values())
        if total == 0:
            return 0.0
        hit_rate = self.coverage_doctrine[True] / total
        logger.info(f"Doctrine hit rate: {hit_rate}")
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        error_count = 0
        query_count = 0
        for m in self.metrics:
            if m.timestamp >= window_start:
                query_count += 1
                if m.error:
                    error_count += 1
        if query_count == 0:
            return 0.0
        error_rate = error_count / query_count
        logger.info(f"Error rate in last {window_hours} hours: {error_rate}")
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for t in self.query_times if t >= one_hour_ago)
        logger.info(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        total_queries = len(self.metrics)
        doctrine_hits = self.coverage_doctrine[True]
        cache_hits = self.coverage_cache[True]
        error_count = sum(1 for m in self.metrics if m.error)
        mode_distribution = dict(self.coverage_modes)
        avg_confidence = statistics.mean(self.coverage_confidence) if self.coverage_confidence else None
        report = {
            "total_queries": total_queries,
            "doctrine_hits": doctrine_hits,
            "cache_hits": cache_hits,
            "error_count": error_count,
            "mode_distribution": mode_distribution,
            "avg_confidence": avg_confidence,
            "doctrine_hit_rate": self.get_doctrine_hit_rate(),
            "error_rate_last_hour": self.get_error_rate(1.0),
            "queries_last_hour": self.queries_last_hour(),
        }
        logger.info(f"Coverage report: {report}")
        return report

    def export_jsonl(self, path: Union[str, pathlib.Path]) -> int:
        path = pathlib.Path(path)
        count = 0
        with path.open("w", encoding="utf-8") as f:
            for m in self.metrics:
                f.write(json.dumps(asdict(m)) + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {path}")
        return count

class AuditTrailWriter:
    def __init__(self, audit_path: Union[str, pathlib.Path]):
        self.audit_path = pathlib.Path(audit_path)
        self.audit_path.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"AuditTrailWriter initialized at {self.audit_path}")

    def write(self, query_metrics: QueryMetrics, extra: Optional[Dict[str, Any]] = None):
        audit_entry = asdict(query_metrics)
        if extra:
            audit_entry.update(extra)
        audit_entry["audit_hash"] = hashlib.sha256(json.dumps(audit_entry, sort_keys=True).encode("utf-8")).hexdigest()
        with self.audit_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(audit_entry) + "\n")
        logger.debug(f"Wrote audit entry: {audit_entry}")

COLLECTOR = TelemetryCollector(maxlen=20000)

# Example usage (commented out for module use):
# metrics = QueryMetrics(
#     query_id="q123",
#     engine_id=ENGINE_ID,
#     timestamp=time.time(),
#     latency_ms=120.5,
#     cache_hit=True,
#     doctrine_matched=False,
#     mode="auto",
#     confidence=0.92,
#     error=None
# )
# COLLECTOR.record_query(metrics)
# COLLECTOR.record_error("Timeout", "Query timed out", "q123")
# stats = COLLECTOR.get_latency_stats()
# coverage = COLLECTOR.get_coverage_report()
# COLLECTOR.export_jsonl("telemetry_export.jsonl")
# audit_writer = AuditTrailWriter("audit_trail.jsonl")
# audit_writer.write(metrics, extra={"user": "operator1"})