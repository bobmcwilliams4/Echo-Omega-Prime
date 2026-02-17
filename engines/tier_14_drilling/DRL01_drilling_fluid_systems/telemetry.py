import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict, field
from typing import Optional, List, Dict, Any, Union
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "DRL01"

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
        self._queries: deque[QueryMetrics] = deque(maxlen=maxlen)
        self._errors: deque[Dict[str, Any]] = deque(maxlen=maxlen)
        self._doctrine_hits: deque[bool] = deque(maxlen=maxlen)
        self._latencies: deque[float] = deque(maxlen=maxlen)
        self._query_timestamps: deque[float] = deque(maxlen=maxlen)
        self._query_ids: set[str] = set()
        self._audit_writer = AuditTrailWriter()
        self._coverage_counter = Counter()
        self._mode_counter = Counter()
        self._confidence_samples = []
        self._cache_hits = deque(maxlen=maxlen)
        self._lock = None  # Placeholder for thread safety if needed

    def record_query(self, metrics: QueryMetrics):
        if metrics.query_id in self._query_ids:
            logger.warning(f"Duplicate query_id detected: {metrics.query_id}")
            return
        self._queries.append(metrics)
        self._query_ids.add(metrics.query_id)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._latencies.append(metrics.latency_ms)
        self._query_timestamps.append(metrics.timestamp)
        self._mode_counter[metrics.mode] += 1
        self._confidence_samples.append(metrics.confidence)
        self._cache_hits.append(metrics.cache_hit)
        if metrics.doctrine_matched:
            self._coverage_counter["doctrine_matched"] += 1
        else:
            self._coverage_counter["doctrine_unmatched"] += 1
        if metrics.error:
            self.record_error("query_error", metrics.error, metrics.query_id)
        self._audit_writer.write(metrics)
        logger.debug(f"Recorded query: {metrics}")

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "timestamp": time.time(),
            "engine_id": ENGINE_ID
        }
        self._errors.append(error_entry)
        logger.error(f"Error recorded: {error_entry}")

    def get_latency_stats(self) -> dict:
        if not self._latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        latencies = list(self._latencies)
        avg = statistics.mean(latencies)
        min_latency = min(latencies)
        max_latency = max(latencies)
        p50 = statistics.median(latencies)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)
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

    def _percentile(self, data: List[float], percentile: float) -> float:
        if not data:
            return None
        size = len(data)
        data_sorted = sorted(data)
        k = (size - 1) * (percentile / 100)
        f = int(k)
        c = min(f + 1, size - 1)
        if f == c:
            return data_sorted[int(k)]
        d0 = data_sorted[f] * (c - k)
        d1 = data_sorted[c] * (k - f)
        return d0 + d1

    def get_doctrine_hit_rate(self) -> float:
        if not self._doctrine_hits:
            return 0.0
        hit_rate = sum(self._doctrine_hits) / len(self._doctrine_hits)
        logger.debug(f"Doctrine hit rate: {hit_rate}")
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        queries_in_window = [t for t in self._query_timestamps if t >= window_start]
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        if not queries_in_window:
            return 0.0
        error_rate = len(errors_in_window) / len(queries_in_window)
        logger.debug(f"Error rate (last {window_hours}h): {error_rate}")
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for t in self._query_timestamps if t >= one_hour_ago)
        logger.debug(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> dict:
        total = self._coverage_counter["doctrine_matched"] + self._coverage_counter["doctrine_unmatched"]
        doctrine_coverage = (
            self._coverage_counter["doctrine_matched"] / total if total > 0 else 0.0
        )
        mode_distribution = dict(self._mode_counter)
        avg_confidence = (
            statistics.mean(self._confidence_samples) if self._confidence_samples else None
        )
        cache_hit_rate = (
            sum(self._cache_hits) / len(self._cache_hits) if self._cache_hits else 0.0
        )
        report = {
            "doctrine_coverage": doctrine_coverage,
            "mode_distribution": mode_distribution,
            "avg_confidence": avg_confidence,
            "cache_hit_rate": cache_hit_rate,
            "total_queries": total,
        }
        logger.debug(f"Coverage report: {report}")
        return report

    def export_jsonl(self, path: Union[str, pathlib.Path]) -> int:
        path = pathlib.Path(path)
        count = 0
        with path.open("w", encoding="utf-8") as f:
            for q in self._queries:
                data = asdict(q)
                f.write(json.dumps(data) + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {path}")
        return count

class AuditTrailWriter:
    def __init__(self, base_dir: Union[str, pathlib.Path] = "audit_trail"):
        self.base_dir = pathlib.Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def write(self, metrics: QueryMetrics):
        date_str = time.strftime("%Y%m%d")
        filename = f"{ENGINE_ID}_audit_{date_str}.jsonl"
        path = self.base_dir / filename
        entry = asdict(metrics)
        entry["audit_timestamp"] = time.time()
        try:
            with path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
            logger.debug(f"Audit entry written for query_id={metrics.query_id}")
        except Exception as e:
            logger.error(f"Failed to write audit entry: {e}")

COLLECTOR = TelemetryCollector()