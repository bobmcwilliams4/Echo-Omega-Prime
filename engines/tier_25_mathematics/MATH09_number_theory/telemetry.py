import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict, field
from typing import Optional, List, Dict, Any, Deque
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "MATH09"

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
        self._queries: Deque[QueryMetrics] = deque(maxlen=maxlen)
        self._errors: Deque[Dict[str, Any]] = deque(maxlen=maxlen)
        self._doctrine_hits: Counter = Counter()
        self._cache_hits: Counter = Counter()
        self._latencies: Deque[float] = deque(maxlen=maxlen)
        self._modes: Counter = Counter()
        self._confidence_scores: Deque[float] = deque(maxlen=maxlen)
        self._coverage: Dict[str, int] = defaultdict(int)
        self._audit_writer = AuditTrailWriter()
        logger.info("TelemetryCollector initialized with maxlen={}", maxlen)

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_hits[metrics.doctrine_matched] += 1
        self._cache_hits[metrics.cache_hit] += 1
        self._modes[metrics.mode] += 1
        self._confidence_scores.append(metrics.confidence)
        self._coverage[metrics.mode] += 1
        self._audit_writer.write(metrics)
        logger.debug("Recorded query: {}", metrics)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "engine_id": ENGINE_ID,
            "error_type": error_type,
            "message": message,
            "query_id": query_id
        }
        self._errors.append(error_entry)
        logger.error("Error recorded: {}", error_entry)

    def get_latency_stats(self) -> Dict[str, float]:
        latencies = list(self._latencies)
        if not latencies:
            return {"avg": 0.0, "p50": 0.0, "p95": 0.0, "p99": 0.0, "min": 0.0, "max": 0.0}
        avg = statistics.mean(latencies)
        min_v = min(latencies)
        max_v = max(latencies)
        p50 = statistics.median(latencies)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)
        stats = {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_v,
            "max": max_v
        }
        logger.debug("Latency stats computed: {}", stats)
        return stats

    def get_doctrine_hit_rate(self) -> float:
        total = sum(self._doctrine_hits.values())
        if total == 0:
            return 0.0
        hit_rate = self._doctrine_hits[True] / total
        logger.debug("Doctrine hit rate: {}", hit_rate)
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        queries_in_window = [q for q in self._queries if q.timestamp >= window_start]
        num_queries = len(queries_in_window)
        if num_queries == 0:
            return 0.0
        error_rate = len(errors_in_window) / num_queries
        logger.debug("Error rate in last {} hours: {}", window_hours, error_rate)
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= one_hour_ago)
        logger.debug("Queries in last hour: {}", count)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        total = sum(self._coverage.values())
        report = {
            "total_queries": total,
            "by_mode": dict(self._coverage)
        }
        logger.debug("Coverage report: {}", report)
        return report

    def export_jsonl(self, path: str) -> int:
        path_obj = pathlib.Path(path)
        count = 0
        with path_obj.open("w", encoding="utf-8") as f:
            for q in self._queries:
                f.write(json.dumps(asdict(q)) + "\n")
                count += 1
        logger.info("Exported {} queries to {}", count, path)
        return count

    @staticmethod
    def _percentile(data: List[float], percentile: float) -> float:
        if not data:
            return 0.0
        data_sorted = sorted(data)
        k = (len(data_sorted) - 1) * (percentile / 100)
        f = int(k)
        c = min(f + 1, len(data_sorted) - 1)
        if f == c:
            return data_sorted[int(k)]
        d0 = data_sorted[f] * (c - k)
        d1 = data_sorted[c] * (k - f)
        return d0 + d1

class AuditTrailWriter:
    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = pathlib.Path(base_dir) if base_dir else pathlib.Path("./audit_trail")
        self.base_dir.mkdir(parents=True, exist_ok=True)
        logger.info("AuditTrailWriter initialized at {}", self.base_dir)

    def write(self, metrics: QueryMetrics):
        query_hash = hashlib.sha256(metrics.query_id.encode()).hexdigest()
        filename = f"{metrics.timestamp:.0f}_{query_hash[:12]}.jsonl"
        file_path = self.base_dir / filename
        with file_path.open("w", encoding="utf-8") as f:
            json.dump(asdict(metrics), f)
            f.write("\n")
        logger.debug("Audit trail written for query_id {} at {}", metrics.query_id, file_path)

COLLECTOR = TelemetryCollector()