import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict, field
from typing import List, Optional, Dict, Any, Deque
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "G04"

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
        self._errors: Deque[dict] = deque(maxlen=maxlen)
        self._doctrine_hits: Deque[bool] = deque(maxlen=maxlen)
        self._latencies: Deque[float] = deque(maxlen=maxlen)
        self._query_timestamps: Deque[float] = deque(maxlen=maxlen)
        self._audit_writer = AuditTrailWriter()
        self._mode_counter: Counter = Counter()
        self._cache_hits: Deque[bool] = deque(maxlen=maxlen)
        self._confidence_scores: Deque[float] = deque(maxlen=maxlen)
        self._coverage_by_mode: defaultdict = defaultdict(int)

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._query_timestamps.append(metrics.timestamp)
        self._mode_counter[metrics.mode] += 1
        self._cache_hits.append(metrics.cache_hit)
        self._confidence_scores.append(metrics.confidence)
        self._coverage_by_mode[metrics.mode] += 1
        self._audit_writer.write(metrics)
        if metrics.error:
            self.record_error(metrics.error, "Query error", metrics.query_id)
        logger.debug(f"Recorded query: {metrics}")

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "timestamp": time.time(),
        }
        self._errors.append(error_entry)
        logger.error(f"Error recorded: {error_entry}")

    def get_latency_stats(self) -> dict:
        if not self._latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        lats = list(self._latencies)
        lats.sort()
        avg = statistics.mean(lats)
        p50 = statistics.median(lats)
        p95 = lats[int(0.95 * len(lats)) - 1] if len(lats) >= 20 else lats[-1]
        p99 = lats[int(0.99 * len(lats)) - 1] if len(lats) >= 100 else lats[-1]
        min_v = min(lats)
        max_v = max(lats)
        stats_dict = {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_v,
            "max": max_v,
        }
        logger.debug(f"Latency stats: {stats_dict}")
        return stats_dict

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
        logger.debug(f"Error rate in last {window_hours}h: {error_rate}")
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for t in self._query_timestamps if t >= one_hour_ago)
        logger.debug(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> dict:
        total = len(self._queries)
        if total == 0:
            return {
                "total": 0,
                "by_mode": {},
                "cache_hit_rate": None,
                "avg_confidence": None,
            }
        by_mode = dict(self._mode_counter)
        cache_hit_rate = sum(self._cache_hits) / len(self._cache_hits) if self._cache_hits else None
        avg_confidence = statistics.mean(self._confidence_scores) if self._confidence_scores else None
        report = {
            "total": total,
            "by_mode": by_mode,
            "cache_hit_rate": cache_hit_rate,
            "avg_confidence": avg_confidence,
        }
        logger.debug(f"Coverage report: {report}")
        return report

    def export_jsonl(self, path) -> int:
        path = pathlib.Path(path)
        count = 0
        with path.open("w", encoding="utf-8") as f:
            for q in self._queries:
                f.write(json.dumps(asdict(q)) + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {path}")
        return count

class AuditTrailWriter:
    def __init__(self, base_path: Optional[str] = None):
        self.base_path = pathlib.Path(base_path) if base_path else pathlib.Path("./audit_trail")
        self.base_path.mkdir(parents=True, exist_ok=True)

    def write(self, metrics: QueryMetrics):
        audit_entry = asdict(metrics)
        audit_entry["audit_timestamp"] = time.time()
        filename = self._get_audit_filename(metrics)
        with open(filename, "a", encoding="utf-8") as f:
            f.write(json.dumps(audit_entry) + "\n")
        logger.debug(f"Wrote audit trail for query {metrics.query_id} to {filename}")

    def _get_audit_filename(self, metrics: QueryMetrics) -> str:
        date_str = time.strftime("%Y%m%d")
        hash_id = hashlib.sha1(metrics.query_id.encode()).hexdigest()[:8]
        filename = f"{date_str}_{metrics.engine_id}_{hash_id}.jsonl"
        return str(self.base_path / filename)

COLLECTOR = TelemetryCollector()