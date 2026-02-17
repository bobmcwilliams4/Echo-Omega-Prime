import time
import json
import hashlib
import statistics
from pathlib import Path
from dataclasses import dataclass, asdict, field
from typing import List, Optional, Dict, Any, Deque
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "ENRG08"

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
        self._modes: Deque[str] = deque(maxlen=maxlen)
        self._confidences: Deque[float] = deque(maxlen=maxlen)
        self._coverage: Counter = Counter()
        self._query_timestamps: Deque[float] = deque(maxlen=maxlen)
        self._query_ids: set = set()
        self._audit_writer = AuditTrailWriter()
        logger.info("TelemetryCollector initialized.")

    def record_query(self, metrics: QueryMetrics):
        if metrics.query_id in self._query_ids:
            logger.warning(f"Duplicate query_id detected: {metrics.query_id}")
            return
        self._queries.append(metrics)
        self._query_ids.add(metrics.query_id)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._latencies.append(metrics.latency_ms)
        self._cache_hits.append(metrics.cache_hit)
        self._modes.append(metrics.mode)
        self._confidences.append(metrics.confidence)
        self._query_timestamps.append(metrics.timestamp)
        self._coverage[metrics.mode] += 1
        self._audit_writer.write(metrics)
        logger.debug(f"Recorded query: {metrics.query_id}")

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "timestamp": time.time(),
        }
        self._errors.append(error_entry)
        logger.error(f"Error recorded: {error_type} - {message} (query_id={query_id})")

    def get_latency_stats(self) -> Dict[str, float]:
        if not self._latencies:
            return {"avg": 0.0, "p50": 0.0, "p95": 0.0, "p99": 0.0, "min": 0.0, "max": 0.0}
        latencies = list(self._latencies)
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        lat_sorted = sorted(latencies)
        def percentile(p):
            k = int(len(lat_sorted) * p)
            if k >= len(lat_sorted):
                k = len(lat_sorted) - 1
            return lat_sorted[k]
        p95 = percentile(0.95)
        p99 = percentile(0.99)
        min_v = min(latencies)
        max_v = max(latencies)
        stats = {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_v,
            "max": max_v,
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
        error_count = sum(1 for e in self._errors if e["timestamp"] >= window_start)
        query_count = sum(1 for t in self._query_timestamps if t >= window_start)
        if query_count == 0:
            return 0.0
        error_rate = error_count / query_count
        logger.debug(f"Error rate over last {window_hours}h: {error_rate}")
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for t in self._query_timestamps if t >= one_hour_ago)
        logger.debug(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        total = sum(self._coverage.values())
        if total == 0:
            return {"modes": {}, "total": 0}
        modes = {mode: count / total for mode, count in self._coverage.items()}
        report = {"modes": modes, "total": total}
        logger.debug(f"Coverage report: {report}")
        return report

    def export_jsonl(self, path: str) -> int:
        path_obj = Path(path)
        count = 0
        with path_obj.open("w", encoding="utf-8") as f:
            for q in self._queries:
                f.write(json.dumps(asdict(q)) + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {path}")
        return count

class AuditTrailWriter:
    def __init__(self, base_dir: str = "./audit_trail"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"AuditTrailWriter initialized at {self.base_dir}")

    def write(self, metrics: QueryMetrics):
        date_str = time.strftime("%Y-%m-%d")
        file_path = self.base_dir / f"audit_{date_str}.jsonl"
        entry = asdict(metrics)
        entry["audit_timestamp"] = time.time()
        try:
            with file_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
            logger.debug(f"Audit entry written for query_id={metrics.query_id}")
        except Exception as e:
            logger.error(f"Failed to write audit trail: {e}")

COLLECTOR = TelemetryCollector()