import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Union
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "MECH06"

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
        self._coverage: Dict[str, Dict[str, Any]] = defaultdict(lambda: {"count": 0, "doctrine_matched": 0, "cache_hit": 0})
        logger.info("TelemetryCollector initialized for engine: {}", ENGINE_ID)

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._query_index[metrics.query_id] = metrics
        self._doctrine_counter[metrics.doctrine_matched] += 1
        self._cache_hit_counter[metrics.cache_hit] += 1
        self._mode_counter[metrics.mode] += 1
        if metrics.confidence is not None:
            self._confidence_values.append(metrics.confidence)
        self._coverage[metrics.mode]["count"] += 1
        if metrics.doctrine_matched:
            self._coverage[metrics.mode]["doctrine_matched"] += 1
        if metrics.cache_hit:
            self._coverage[metrics.mode]["cache_hit"] += 1
        logger.debug("Recorded query: {}", metrics)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "timestamp": time.time(),
        }
        self._errors.append(error_entry)
        self._error_counter[error_type] += 1
        logger.error("Recorded error: {} | Query ID: {}", error_type, query_id)

        if query_id and query_id in self._query_index:
            self._query_index[query_id].error = error_type

    def get_latency_stats(self) -> Dict[str, Union[float, None]]:
        latencies = [q.latency_ms for q in self._queries if q.latency_ms is not None]
        if not latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = latencies_sorted[int(len(latencies_sorted) * 0.95)-1] if len(latencies_sorted) >= 1 else None
        p99 = latencies_sorted[int(len(latencies_sorted) * 0.99)-1] if len(latencies_sorted) >= 1 else None
        min_latency = min(latencies)
        max_latency = max(latencies)
        logger.info("Latency stats computed: avg={}, p50={}, p95={}, p99={}, min={}, max={}", avg, p50, p95, p99, min_latency, max_latency)
        return {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_latency,
            "max": max_latency,
        }

    def get_doctrine_hit_rate(self) -> float:
        total = sum(self._doctrine_counter.values())
        hits = self._doctrine_counter.get(True, 0)
        hit_rate = hits / total if total > 0 else 0.0
        logger.info("Doctrine hit rate: {}", hit_rate)
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        error_count = sum(1 for e in self._errors if e["timestamp"] >= window_start)
        query_count = sum(1 for q in self._queries if q.timestamp >= window_start)
        error_rate = error_count / query_count if query_count > 0 else 0.0
        logger.info("Error rate over {} hours: {}", window_hours, error_rate)
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= one_hour_ago)
        logger.info("Queries in last hour: {}", count)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {}
        for mode, stats in self._coverage.items():
            count = stats["count"]
            doctrine_matched = stats["doctrine_matched"]
            cache_hit = stats["cache_hit"]
            doctrine_rate = doctrine_matched / count if count > 0 else 0.0
            cache_rate = cache_hit / count if count > 0 else 0.0
            report[mode] = {
                "count": count,
                "doctrine_matched": doctrine_matched,
                "cache_hit": cache_hit,
                "doctrine_rate": doctrine_rate,
                "cache_rate": cache_rate,
            }
        logger.info("Coverage report generated: {}", report)
        return report

    def export_jsonl(self, path: Union[str, pathlib.Path]) -> int:
        p = pathlib.Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        count = 0
        with p.open("w", encoding="utf-8") as f:
            for q in self._queries:
                f.write(json.dumps(dataclasses.asdict(q)) + "\n")
                count += 1
        logger.info("Exported {} queries to {}", count, path)
        return count

class AuditTrailWriter:
    def __init__(self, audit_dir: Union[str, pathlib.Path]):
        self.audit_dir = pathlib.Path(audit_dir)
        self.audit_dir.mkdir(parents=True, exist_ok=True)
        logger.info("AuditTrailWriter initialized at {}", self.audit_dir)

    def write(self, query_metrics: QueryMetrics):
        audit_file = self.audit_dir / f"{query_metrics.query_id}.jsonl"
        with audit_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(dataclasses.asdict(query_metrics)) + "\n")
        logger.debug("Audit trail written for query_id: {}", query_metrics.query_id)

COLLECTOR = TelemetryCollector()

# Example usage (commented out):
# metrics = QueryMetrics(
#     query_id="abc123",
#     engine_id=ENGINE_ID,
#     timestamp=time.time(),
#     latency_ms=120.5,
#     cache_hit=True,
#     doctrine_matched=False,
#     mode="bearing_analysis",
#     confidence=0.92,
#     error=None
# )
# COLLECTOR.record_query(metrics)
# COLLECTOR.record_error("Timeout", "Query timed out", query_id="abc123")
# stats = COLLECTOR.get_latency_stats()
# hit_rate = COLLECTOR.get_doctrine_hit_rate()
# error_rate = COLLECTOR.get_error_rate(1.0)
# coverage = COLLECTOR.get_coverage_report()
# COLLECTOR.export_jsonl("telemetry_export.jsonl")
# audit_writer = AuditTrailWriter("audit_trails")
# audit_writer.write(metrics)