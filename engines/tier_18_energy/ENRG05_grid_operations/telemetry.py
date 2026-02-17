import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Any, Deque
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "ENRG05"

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
        self._doctrine_hits: Deque[bool] = deque(maxlen=maxlen)
        self._latencies: Deque[float] = deque(maxlen=maxlen)
        self._cache_hits: Deque[bool] = deque(maxlen=maxlen)
        self._query_timestamps: Deque[float] = deque(maxlen=maxlen)
        self._coverage_modes: Counter = Counter()
        self._coverage_confidence: List[float] = []
        self._audit_writer = AuditTrailWriter()
        logger.info("TelemetryCollector initialized.")

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._latencies.append(metrics.latency_ms)
        self._cache_hits.append(metrics.cache_hit)
        self._query_timestamps.append(metrics.timestamp)
        self._coverage_modes[metrics.mode] += 1
        self._coverage_confidence.append(metrics.confidence)
        self._audit_writer.write(metrics)
        logger.debug(f"Recorded query: {metrics.query_id}")

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "timestamp": time.time()
        }
        self._errors.append(error_entry)
        logger.error(f"Error recorded: {error_type} - {message} (query_id={query_id})")

    def get_latency_stats(self) -> Dict[str, float]:
        latencies = list(self._latencies)
        if not latencies:
            return {"avg": 0.0, "p50": 0.0, "p95": 0.0, "p99": 0.0, "min": 0.0, "max": 0.0}
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)
        min_v = min(latencies)
        max_v = max(latencies)
        logger.info(f"Latency stats calculated: avg={avg}, p50={p50}, p95={p95}, p99={p99}, min={min_v}, max={max_v}")
        return {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_v,
            "max": max_v
        }

    def _percentile(self, data: List[float], percentile: float) -> float:
        if not data:
            return 0.0
        data = sorted(data)
        k = (len(data) - 1) * (percentile / 100)
        f = int(k)
        c = min(f + 1, len(data) - 1)
        if f == c:
            return data[int(k)]
        d0 = data[f] * (c - k)
        d1 = data[c] * (k - f)
        return d0 + d1

    def get_doctrine_hit_rate(self) -> float:
        total = len(self._doctrine_hits)
        if total == 0:
            return 0.0
        hits = sum(1 for hit in self._doctrine_hits if hit)
        rate = hits / total
        logger.info(f"Doctrine hit rate: {rate} ({hits}/{total})")
        return rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        queries_in_window = [t for t in self._query_timestamps if t >= window_start]
        n_errors = len(errors_in_window)
        n_queries = len(queries_in_window)
        if n_queries == 0:
            return 0.0
        rate = n_errors / n_queries
        logger.info(f"Error rate in last {window_hours}h: {rate} ({n_errors}/{n_queries})")
        return rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for t in self._query_timestamps if t >= one_hour_ago)
        logger.info(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        total = len(self._queries)
        mode_counts = dict(self._coverage_modes)
        avg_conf = statistics.mean(self._coverage_confidence) if self._coverage_confidence else 0.0
        report = {
            "total_queries": total,
            "mode_distribution": mode_counts,
            "avg_confidence": avg_conf
        }
        logger.info(f"Coverage report generated: {report}")
        return report

    def export_jsonl(self, path: str) -> int:
        path_obj = pathlib.Path(path)
        count = 0
        with path_obj.open("w", encoding="utf-8") as f:
            for q in self._queries:
                f.write(json.dumps(asdict(q)) + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {path}")
        return count

class AuditTrailWriter:
    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = pathlib.Path(base_dir) if base_dir else pathlib.Path("audit_trails")
        self.base_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"AuditTrailWriter initialized at {self.base_dir}")

    def write(self, metrics: QueryMetrics):
        fname = self._get_audit_filename(metrics)
        path = self.base_dir / fname
        entry = asdict(metrics)
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        logger.debug(f"Audit trail written for query_id={metrics.query_id}")

    def _get_audit_filename(self, metrics: QueryMetrics) -> str:
        date_str = time.strftime("%Y%m%d", time.localtime(metrics.timestamp))
        short_id = hashlib.sha1(metrics.query_id.encode()).hexdigest()[:8]
        fname = f"{ENGINE_ID}_audit_{date_str}_{short_id}.jsonl"
        return fname

COLLECTOR = TelemetryCollector()