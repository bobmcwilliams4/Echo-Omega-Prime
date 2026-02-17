import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "OFE02"

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
    def __init__(self, max_queries: int = 100000):
        self.queries: deque = deque(maxlen=max_queries)
        self.errors: deque = deque(maxlen=max_queries)
        self._query_id_index: Dict[str, QueryMetrics] = {}
        self._error_counter: Counter = Counter()
        self._doctrine_counter: Counter = Counter()
        self._cache_counter: Counter = Counter()
        self._mode_counter: Counter = Counter()
        self._confidence_values: List[float] = []
        self._latency_values: List[float] = []
        self._coverage_counter: Counter = Counter()
        self._last_export_count: int = 0
        logger.info("TelemetryCollector initialized with max_queries={}", max_queries)

    def record_query(self, metrics: QueryMetrics):
        self.queries.append(metrics)
        self._query_id_index[metrics.query_id] = metrics
        self._latency_values.append(metrics.latency_ms)
        self._doctrine_counter[metrics.doctrine_matched] += 1
        self._cache_counter[metrics.cache_hit] += 1
        self._mode_counter[metrics.mode] += 1
        self._confidence_values.append(metrics.confidence)
        self._coverage_counter[(metrics.mode, metrics.doctrine_matched)] += 1
        if metrics.error:
            self.record_error("query_error", metrics.error, metrics.query_id)
        logger.debug("Recorded query: {}", metrics)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "error_type": error_type,
            "message": message,
            "query_id": query_id
        }
        self.errors.append(error_entry)
        self._error_counter[error_type] += 1
        logger.warning("Recorded error: {} for query_id={}", error_type, query_id)

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = [q.latency_ms for q in self.queries if q.latency_ms is not None]
        if not latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = latencies_sorted[int(0.95 * len(latencies_sorted)) - 1]
        p99 = latencies_sorted[int(0.99 * len(latencies_sorted)) - 1]
        min_latency = latencies_sorted[0]
        max_latency = latencies_sorted[-1]
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
        logger.info("Doctrine hit rate: {:.4f}", hit_rate)
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        error_count = sum(1 for e in self.errors if e["timestamp"] >= window_start)
        query_count = sum(1 for q in self.queries if q.timestamp >= window_start)
        error_rate = error_count / query_count if query_count > 0 else 0.0
        logger.info("Error rate in last {:.2f} hours: {:.4f}", window_hours, error_rate)
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self.queries if q.timestamp >= one_hour_ago)
        logger.info("Queries in last hour: {}", count)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        modes = set(q.mode for q in self.queries)
        doctrine_states = [True, False]
        report = {}
        for mode in modes:
            for doctrine in doctrine_states:
                key = (mode, doctrine)
                count = self._coverage_counter.get(key, 0)
                report[f"{mode}_doctrine_{doctrine}"] = count
        logger.info("Coverage report: {}", report)
        return report

    def export_jsonl(self, path: str) -> int:
        p = pathlib.Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        count = 0
        with p.open("w", encoding="utf-8") as f:
            for q in self.queries:
                f.write(json.dumps(asdict(q)) + "\n")
                count += 1
        self._last_export_count = count
        logger.info("Exported {} queries to {}", count, path)
        return count

class AuditTrailWriter:
    def __init__(self, audit_dir: str = "./audit_trail"):
        self.audit_dir = pathlib.Path(audit_dir)
        self.audit_dir.mkdir(parents=True, exist_ok=True)
        logger.info("AuditTrailWriter initialized at {}", self.audit_dir)

    def write(self, metrics: QueryMetrics):
        audit_file = self.audit_dir / f"{metrics.query_id}.jsonl"
        with audit_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(metrics)) + "\n")
        logger.debug("Audit trail written for query_id={}", metrics.query_id)

COLLECTOR = TelemetryCollector()
AUDIT_WRITER = AuditTrailWriter()

# Example usage for integration (not executed in module)
def _example_usage():
    q = QueryMetrics(
        query_id=hashlib.md5(str(time.time()).encode()).hexdigest(),
        engine_id=ENGINE_ID,
        timestamp=time.time(),
        latency_ms=123.4,
        cache_hit=True,
        doctrine_matched=False,
        mode="analysis",
        confidence=0.87,
        error=None
    )
    COLLECTOR.record_query(q)
    AUDIT_WRITER.write(q)
    COLLECTOR.record_error("timeout", "Query timed out", q.query_id)
    stats = COLLECTOR.get_latency_stats()
    hit_rate = COLLECTOR.get_doctrine_hit_rate()
    error_rate = COLLECTOR.get_error_rate(1.0)
    queries_hour = COLLECTOR.queries_last_hour()
    coverage = COLLECTOR.get_coverage_report()
    COLLECTOR.export_jsonl("./telemetry_export.jsonl")