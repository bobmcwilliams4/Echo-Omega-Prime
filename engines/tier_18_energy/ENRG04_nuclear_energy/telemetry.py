import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any, Union
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "ENRG04"

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
        self._doctrine_hits: deque = deque(maxlen=max_queries)
        self._latencies: deque = deque(maxlen=max_queries)
        self._modes: Counter = Counter()
        self._confidence: deque = deque(maxlen=max_queries)
        self._cache_hits: deque = deque(maxlen=max_queries)
        self._query_ids: set = set()
        self._audit_writer = AuditTrailWriter()
        self._coverage: defaultdict = defaultdict(set)
        logger.info("TelemetryCollector initialized with max_queries={}", max_queries)

    def record_query(self, metrics: QueryMetrics):
        if metrics.query_id in self._query_ids:
            logger.warning("Duplicate query_id detected: {}", metrics.query_id)
            return
        self._queries.append(metrics)
        self._query_ids.add(metrics.query_id)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._modes[metrics.mode] += 1
        self._confidence.append(metrics.confidence)
        self._cache_hits.append(metrics.cache_hit)
        self._coverage[metrics.mode].add(metrics.query_id)
        self._audit_writer.write(metrics)
        logger.debug("Recorded query: {}", metrics.query_id)

    def record_error(self, error_type: str, message: str, query_id: str):
        error_record = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "timestamp": time.time(),
            "engine_id": ENGINE_ID
        }
        self._errors.append(error_record)
        logger.error("Error recorded: {} for query {}", error_type, query_id)

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
        p50 = statistics.median(latencies)
        p95 = self._percentile(latencies_sorted, 95)
        p99 = self._percentile(latencies_sorted, 99)
        min_latency = min(latencies)
        max_latency = max(latencies)
        logger.info("Latency stats calculated")
        return {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_latency,
            "max": max_latency
        }

    def _percentile(self, data: List[float], percentile: float) -> float:
        if not data:
            return None
        k = (len(data) - 1) * (percentile / 100)
        f = int(k)
        c = min(f + 1, len(data) - 1)
        if f == c:
            return data[int(k)]
        return data[f] + (data[c] - data[f]) * (k - f)

    def get_doctrine_hit_rate(self) -> float:
        total = len(self._doctrine_hits)
        if total == 0:
            return 0.0
        hits = sum(1 for hit in self._doctrine_hits if hit)
        hit_rate = hits / total
        logger.info("Doctrine hit rate calculated: {}", hit_rate)
        return hit_rate

    def get_error_rate(self, window_hours: float) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        queries_in_window = [q for q in self._queries if q.timestamp >= window_start]
        num_queries = len(queries_in_window)
        num_errors = len(errors_in_window)
        if num_queries == 0:
            return 0.0
        error_rate = num_errors / num_queries
        logger.info("Error rate for last {} hours: {}", window_hours, error_rate)
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= one_hour_ago)
        logger.info("Queries in last hour: {}", count)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {}
        for mode, query_ids in self._coverage.items():
            report[mode] = {
                "queries": len(query_ids),
                "unique_queries": len(set(query_ids))
            }
        logger.info("Coverage report generated")
        return report

    def export_jsonl(self, path: Union[str, pathlib.Path]) -> int:
        path = pathlib.Path(path)
        count = 0
        with path.open("w", encoding="utf-8") as f:
            for q in self._queries:
                f.write(json.dumps(asdict(q)) + "\n")
                count += 1
        logger.info("Exported {} queries to {}", count, path)
        return count

class AuditTrailWriter:
    def __init__(self, base_path: Optional[pathlib.Path] = None):
        if base_path is None:
            base_path = pathlib.Path("./audit_trail")
        self.base_path = base_path
        self.base_path.mkdir(parents=True, exist_ok=True)
        logger.info("AuditTrailWriter initialized at {}", self.base_path)

    def write(self, metrics: QueryMetrics):
        filename = self._get_filename(metrics)
        filepath = self.base_path / filename
        record = asdict(metrics)
        record["audit_hash"] = self._hash_record(record)
        with filepath.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
        logger.debug("Audit trail written for query {}", metrics.query_id)

    def _get_filename(self, metrics: QueryMetrics) -> str:
        date_str = time.strftime("%Y-%m-%d", time.localtime(metrics.timestamp))
        return f"{ENGINE_ID}_{date_str}_audit.jsonl"

    def _hash_record(self, record: Dict[str, Any]) -> str:
        record_str = json.dumps(record, sort_keys=True)
        return hashlib.sha256(record_str.encode("utf-8")).hexdigest()

COLLECTOR = TelemetryCollector()