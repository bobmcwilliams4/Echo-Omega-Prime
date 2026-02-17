import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Any
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "AUTO03"

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
    def __init__(self):
        self._queries: deque = deque(maxlen=10000)
        self._errors: deque = deque(maxlen=5000)
        self._doctrine_hits: deque = deque(maxlen=10000)
        self._latencies: deque = deque(maxlen=10000)
        self._query_times: deque = deque(maxlen=10000)
        self._mode_counter: Counter = Counter()
        self._cache_hits: deque = deque(maxlen=10000)
        self._confidence_scores: deque = deque(maxlen=10000)
        self._coverage: defaultdict = defaultdict(lambda: {'count': 0, 'doctrine_matched': 0})
        self._audit_writer = AuditTrailWriter()
        logger.info("TelemetryCollector initialized.")

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._latencies.append(metrics.latency_ms)
        self._query_times.append(metrics.timestamp)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._mode_counter[metrics.mode] += 1
        self._cache_hits.append(metrics.cache_hit)
        self._confidence_scores.append(metrics.confidence)
        self._coverage[metrics.mode]['count'] += 1
        if metrics.doctrine_matched:
            self._coverage[metrics.mode]['doctrine_matched'] += 1
        self._audit_writer.write(metrics)
        logger.debug(f"Recorded query: {metrics}")

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "error_type": error_type,
            "message": message,
            "query_id": query_id
        }
        self._errors.append(error_entry)
        logger.error(f"Error recorded: {error_entry}")

    def get_latency_stats(self) -> Dict[str, Any]:
        if not self._latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        latencies = list(self._latencies)
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)
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
        logger.debug(f"Latency stats: {stats}")
        return stats

    def get_doctrine_hit_rate(self) -> float:
        if not self._doctrine_hits:
            return 0.0
        hit_rate = sum(self._doctrine_hits) / len(self._doctrine_hits)
        logger.debug(f"Doctrine hit rate: {hit_rate}")
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        queries_in_window = [t for t in self._query_times if t >= window_start]
        error_count = len(errors_in_window)
        query_count = len(queries_in_window)
        error_rate = error_count / query_count if query_count > 0 else 0.0
        logger.debug(f"Error rate: {error_rate} ({error_count} errors / {query_count} queries)")
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = len([t for t in self._query_times if t >= one_hour_ago])
        logger.debug(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {}
        for mode, data in self._coverage.items():
            count = data['count']
            doctrine_matched = data['doctrine_matched']
            doctrine_rate = doctrine_matched / count if count > 0 else 0.0
            report[mode] = {
                "count": count,
                "doctrine_matched": doctrine_matched,
                "doctrine_rate": doctrine_rate
            }
        logger.debug(f"Coverage report: {report}")
        return report

    def export_jsonl(self, path: str) -> int:
        path_obj = pathlib.Path(path)
        path_obj.parent.mkdir(parents=True, exist_ok=True)
        count = 0
        with path_obj.open("w", encoding="utf-8") as f:
            for metrics in self._queries:
                f.write(json.dumps(asdict(metrics)) + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {path}")
        return count

    @staticmethod
    def _percentile(data: List[float], percentile: float) -> float:
        if not data:
            return 0.0
        data_sorted = sorted(data)
        k = (len(data_sorted) - 1) * (percentile / 100.0)
        f = int(k)
        c = min(f + 1, len(data_sorted) - 1)
        if f == c:
            return data_sorted[int(k)]
        d0 = data_sorted[f] * (c - k)
        d1 = data_sorted[c] * (k - f)
        return d0 + d1

class AuditTrailWriter:
    def __init__(self, base_path: Optional[str] = None):
        self.base_path = pathlib.Path(base_path) if base_path else pathlib.Path("./audit_trail")
        self.base_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"AuditTrailWriter initialized at {self.base_path}")

    def write(self, metrics: QueryMetrics):
        date_str = time.strftime("%Y-%m-%d")
        file_path = self.base_path / f"audit_{date_str}.jsonl"
        entry = asdict(metrics)
        entry['audit_hash'] = self._compute_hash(entry)
        with file_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        logger.debug(f"Audit trail written for query_id={metrics.query_id}")

    @staticmethod
    def _compute_hash(entry: Dict[str, Any]) -> str:
        entry_bytes = json.dumps(entry, sort_keys=True).encode("utf-8")
        return hashlib.sha256(entry_bytes).hexdigest()

COLLECTOR = TelemetryCollector()