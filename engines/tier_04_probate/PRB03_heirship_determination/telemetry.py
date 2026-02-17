import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict, field
from typing import Optional, List, Dict, Any, Deque
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "PRB03"

@dataclass
class QueryMetrics:
    query_id: str
    engine_id: str
    timestamp: float
    latency_ms: float
    cache_hit: bool
    doctrine_matched: bool
    mode: str
    confidence: Optional[float]
    error: Optional[str] = None

class TelemetryCollector:
    def __init__(self, maxlen: int = 10000):
        self._queries: Deque[QueryMetrics] = deque(maxlen=maxlen)
        self._errors: Deque[Dict[str, Any]] = deque(maxlen=maxlen)
        self._doctrine_hits: int = 0
        self._doctrine_total: int = 0
        self._cache_hits: int = 0
        self._cache_total: int = 0
        self._latencies: Deque[float] = deque(maxlen=maxlen)
        self._modes: Counter = Counter()
        self._confidence: List[float] = []
        self._coverage: Dict[str, Counter] = defaultdict(Counter)
        self._query_timestamps: Deque[float] = deque(maxlen=maxlen)
        self._query_ids: set = set()
        self._audit_writer = AuditTrailWriter()
        logger.debug("TelemetryCollector initialized with maxlen={}", maxlen)

    def record_query(self, metrics: QueryMetrics):
        logger.debug("Recording query: {}", metrics)
        self._queries.append(metrics)
        self._query_timestamps.append(metrics.timestamp)
        self._query_ids.add(metrics.query_id)
        self._latencies.append(metrics.latency_ms)
        self._modes[metrics.mode] += 1
        if metrics.confidence is not None:
            self._confidence.append(metrics.confidence)
        if metrics.doctrine_matched:
            self._doctrine_hits += 1
        self._doctrine_total += 1
        if metrics.cache_hit:
            self._cache_hits += 1
        self._cache_total += 1
        self._coverage[metrics.mode]['total'] += 1
        if metrics.doctrine_matched:
            self._coverage[metrics.mode]['doctrine_matched'] += 1
        if metrics.error:
            self.record_error(metrics.error, "Query error", metrics.query_id)
        self._audit_writer.write(metrics)
        logger.debug("Query recorded. Total queries: {}", len(self._queries))

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "engine_id": ENGINE_ID
        }
        self._errors.append(error_entry)
        logger.error("Error recorded: {}", error_entry)

    def get_latency_stats(self) -> Dict[str, Any]:
        if not self._latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        lat = sorted(self._latencies)
        avg = statistics.mean(lat)
        min_v = lat[0]
        max_v = lat[-1]
        p50 = lat[int(0.5 * len(lat))]
        p95 = lat[int(0.95 * len(lat)) - 1]
        p99 = lat[int(0.99 * len(lat)) - 1]
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
        if self._doctrine_total == 0:
            return 0.0
        hit_rate = self._doctrine_hits / self._doctrine_total
        logger.debug("Doctrine hit rate: {}/{} = {}", self._doctrine_hits, self._doctrine_total, hit_rate)
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        queries_in_window = [t for t in self._query_timestamps if t >= window_start]
        if not queries_in_window:
            return 0.0
        error_rate = len(errors_in_window) / len(queries_in_window)
        logger.debug("Error rate in last {}h: {}/{} = {}", window_hours, len(errors_in_window), len(queries_in_window), error_rate)
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for t in self._query_timestamps if t >= one_hour_ago)
        logger.debug("Queries in last hour: {}", count)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {}
        for mode, counts in self._coverage.items():
            total = counts['total']
            doctrine_matched = counts.get('doctrine_matched', 0)
            doctrine_rate = doctrine_matched / total if total else 0.0
            report[mode] = {
                "total": total,
                "doctrine_matched": doctrine_matched,
                "doctrine_rate": doctrine_rate
            }
        logger.debug("Coverage report: {}", report)
        return report

    def export_jsonl(self, path: str) -> int:
        p = pathlib.Path(path)
        count = 0
        with p.open("w", encoding="utf-8") as f:
            for q in self._queries:
                f.write(json.dumps(asdict(q)) + "\n")
                count += 1
        logger.info("Exported {} queries to {}", count, path)
        return count

class AuditTrailWriter:
    def __init__(self, base_dir: Optional[str] = None):
        if base_dir is None:
            base_dir = "./audit_trail"
        self.base_dir = pathlib.Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        logger.debug("AuditTrailWriter initialized at {}", self.base_dir)

    def _get_audit_path(self, query_id: str) -> pathlib.Path:
        h = hashlib.sha1(query_id.encode("utf-8")).hexdigest()[:8]
        subdir = self.base_dir / h
        subdir.mkdir(parents=True, exist_ok=True)
        return subdir / f"{query_id}.jsonl"

    def write(self, metrics: QueryMetrics):
        path = self._get_audit_path(metrics.query_id)
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(metrics)) + "\n")
        logger.debug("Audit trail written for query_id={} at {}", metrics.query_id, path)

COLLECTOR = TelemetryCollector()