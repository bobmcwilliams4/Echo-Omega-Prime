import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict, field
from typing import Optional, List, Dict, Any, Deque
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "RAIL06"

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
        self._coverage: Dict[str, Counter] = defaultdict(Counter)
        self._audit_writer = AuditTrailWriter()
        logger.info("TelemetryCollector initialized with maxlen={}", maxlen)

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._cache_hits.append(metrics.cache_hit)
        self._modes.append(metrics.mode)
        self._confidences.append(metrics.confidence)
        self._coverage[metrics.mode].update([
            "cache_hit" if metrics.cache_hit else "cache_miss",
            "doctrine_matched" if metrics.doctrine_matched else "doctrine_unmatched"
        ])
        self._audit_writer.write(metrics)
        logger.debug("Recorded query: {}", metrics)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "timestamp": time.time(),
            "engine_id": ENGINE_ID
        }
        self._errors.append(error_entry)
        logger.error("Error recorded: {}", error_entry)

    def get_latency_stats(self) -> dict:
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
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)
        min_v = min(latencies)
        max_v = max(latencies)
        stats = {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_v,
            "max": max_v
        }
        logger.debug("Latency stats: {}", stats)
        return stats

    def get_doctrine_hit_rate(self) -> float:
        hits = list(self._doctrine_hits)
        if not hits:
            return 0.0
        rate = sum(hits) / len(hits)
        logger.debug("Doctrine hit rate: {}", rate)
        return rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - (window_hours * 3600)
        error_count = sum(1 for e in self._errors if e["timestamp"] >= window_start)
        query_count = sum(1 for q in self._queries if q.timestamp >= window_start)
        rate = (error_count / query_count) if query_count else 0.0
        logger.debug("Error rate in last {} hours: {}", window_hours, rate)
        return rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= one_hour_ago)
        logger.debug("Queries in last hour: {}", count)
        return count

    def get_coverage_report(self) -> dict:
        report = {}
        for mode, counter in self._coverage.items():
            total = sum(counter.values())
            report[mode] = {
                "total": total,
                "cache_hit": counter.get("cache_hit", 0),
                "cache_miss": counter.get("cache_miss", 0),
                "doctrine_matched": counter.get("doctrine_matched", 0),
                "doctrine_unmatched": counter.get("doctrine_unmatched", 0)
            }
        logger.debug("Coverage report: {}", report)
        return report

    def export_jsonl(self, path) -> int:
        path = pathlib.Path(path)
        count = 0
        with path.open("w", encoding="utf-8") as f:
            for q in self._queries:
                f.write(json.dumps(asdict(q)) + "\n")
                count += 1
        logger.info("Exported {} queries to {}", count, path)
        return count

    @staticmethod
    def _percentile(data: List[float], percentile: float) -> float:
        if not data:
            return None
        data = sorted(data)
        k = (len(data) - 1) * (percentile / 100)
        f = int(k)
        c = min(f + 1, len(data) - 1)
        if f == c:
            return data[int(k)]
        d0 = data[f] * (c - k)
        d1 = data[c] * (k - f)
        return d0 + d1

class AuditTrailWriter:
    def __init__(self, base_dir: Optional[str] = None):
        if base_dir is None:
            self.base_dir = pathlib.Path("./audit_trails")
        else:
            self.base_dir = pathlib.Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        logger.info("AuditTrailWriter initialized at {}", self.base_dir)

    def write(self, metrics: QueryMetrics):
        date_str = time.strftime("%Y%m%d")
        filename = f"{ENGINE_ID}_audit_{date_str}.jsonl"
        file_path = self.base_dir / filename
        entry = asdict(metrics)
        entry["audit_id"] = self._generate_audit_id(metrics)
        with file_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        logger.debug("Wrote audit trail for query_id={} to {}", metrics.query_id, file_path)

    @staticmethod
    def _generate_audit_id(metrics: QueryMetrics) -> str:
        base = f"{metrics.query_id}|{metrics.engine_id}|{metrics.timestamp}"
        return hashlib.sha256(base.encode("utf-8")).hexdigest()

COLLECTOR = TelemetryCollector()