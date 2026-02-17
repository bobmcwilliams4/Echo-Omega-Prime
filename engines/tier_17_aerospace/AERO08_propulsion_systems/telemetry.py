import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Union
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "AERO08"

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
        self._queries: deque = deque(maxlen=100000)
        self._errors: deque = deque(maxlen=10000)
        self._doctrine_hits: deque = deque(maxlen=100000)
        self._latencies: deque = deque(maxlen=100000)
        self._query_modes: Counter = Counter()
        self._confidence_scores: deque = deque(maxlen=100000)
        self._coverage: defaultdict = defaultdict(set)
        self._audit_writer = AuditTrailWriter()
        logger.info(f"TelemetryCollector initialized for engine: {engine_id}")

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._query_modes[metrics.mode] += 1
        self._confidence_scores.append(metrics.confidence)
        self._coverage[metrics.mode].add(metrics.query_id)
        if metrics.error:
            self.record_error(metrics.error, "Query error", metrics.query_id)
        self._audit_writer.write(metrics)
        logger.debug(f"Recorded query: {metrics.query_id}")

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "engine_id": self.engine_id,
            "timestamp": time.time()
        }
        self._errors.append(error_entry)
        logger.warning(f"Recorded error: {error_type} for query_id: {query_id}")

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = list(self._latencies)
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
        min_latency = min(latencies)
        max_latency = max(latencies)
        p50 = self._percentile(latencies_sorted, 50)
        p95 = self._percentile(latencies_sorted, 95)
        p99 = self._percentile(latencies_sorted, 99)
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

    def _percentile(self, data: List[float], percentile: float) -> float:
        if not data:
            return None
        k = (len(data)-1) * (percentile/100)
        f = int(k)
        c = min(f+1, len(data)-1)
        if f == c:
            return data[int(k)]
        d0 = data[f] * (c-k)
        d1 = data[c] * (k-f)
        return d0 + d1

    def get_doctrine_hit_rate(self) -> float:
        hits = list(self._doctrine_hits)
        if not hits:
            return 0.0
        hit_count = sum(1 for h in hits if h)
        rate = hit_count / len(hits)
        logger.info(f"Doctrine hit rate: {rate}")
        return rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        queries_in_window = [q for q in self._queries if q.timestamp >= window_start]
        error_count = len(errors_in_window)
        query_count = len(queries_in_window)
        rate = (error_count / query_count) if query_count > 0 else 0.0
        logger.info(f"Error rate over last {window_hours} hours: {rate}")
        return rate

    def queries_last_hour(self) -> int:
        now = time.time()
        window_start = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= window_start)
        logger.info(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {}
        for mode, queries in self._coverage.items():
            report[mode] = {
                "unique_queries": len(queries),
                "total_queries": self._query_modes[mode]
            }
        logger.info(f"Coverage report: {report}")
        return report

    def export_jsonl(self, path: Union[str, pathlib.Path]) -> int:
        path = pathlib.Path(path)
        count = 0
        with path.open("w", encoding="utf-8") as f:
            for q in self._queries:
                f.write(json.dumps(dataclasses.asdict(q)) + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {path}")
        return count

class AuditTrailWriter:
    def __init__(self, audit_dir: Union[str, pathlib.Path] = "audit_trail"):
        self.audit_dir = pathlib.Path(audit_dir)
        self.audit_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"AuditTrailWriter initialized at {self.audit_dir}")

    def write(self, metrics: QueryMetrics):
        audit_path = self._get_audit_path(metrics)
        with audit_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(dataclasses.asdict(metrics)) + "\n")
        logger.debug(f"Audit trail written for query_id: {metrics.query_id}")

    def _get_audit_path(self, metrics: QueryMetrics) -> pathlib.Path:
        date_str = time.strftime("%Y-%m-%d", time.localtime(metrics.timestamp))
        filename = f"audit_{metrics.engine_id}_{date_str}.jsonl"
        return self.audit_dir / filename

COLLECTOR = TelemetryCollector(engine_id=ENGINE_ID)