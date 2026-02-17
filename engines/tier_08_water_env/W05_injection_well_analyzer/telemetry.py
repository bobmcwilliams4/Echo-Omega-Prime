import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict, field
from typing import Optional, List, Dict, Any
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "W05"

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
        self._queries: deque = deque(maxlen=maxlen)
        self._errors: deque = deque(maxlen=maxlen)
        self._doctrine_hits: deque = deque(maxlen=maxlen)
        self._latencies: deque = deque(maxlen=maxlen)
        self._cache_hits: deque = deque(maxlen=maxlen)
        self._coverage_modes: Counter = Counter()
        self._coverage_confidences: List[float] = []
        self._query_timestamps: deque = deque(maxlen=maxlen)
        self._query_ids: set = set()
        self._audit_writer = AuditTrailWriter()
        logger.debug("TelemetryCollector initialized with maxlen={}", maxlen)

    def record_query(self, metrics: QueryMetrics):
        if metrics.query_id in self._query_ids:
            logger.warning("Duplicate query_id detected: {}", metrics.query_id)
            return
        self._query_ids.add(metrics.query_id)
        self._queries.append(metrics)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._cache_hits.append(metrics.cache_hit)
        self._coverage_modes[metrics.mode] += 1
        self._coverage_confidences.append(metrics.confidence)
        self._query_timestamps.append(metrics.timestamp)
        if metrics.error:
            self.record_error(metrics.error, "Error in query", metrics.query_id)
        self._audit_writer.write(metrics)
        logger.debug("Recorded query: {}", metrics.query_id)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "engine_id": ENGINE_ID,
            "error_type": error_type,
            "message": message,
            "query_id": query_id
        }
        self._errors.append(error_entry)
        logger.error("Error recorded: {} | {} | {}", error_type, message, query_id)

    def get_latency_stats(self) -> Dict[str, Any]:
        if not self._latencies:
            logger.info("No latency data available.")
            return dict(avg=None, p50=None, p95=None, p99=None, min=None, max=None)
        latencies = list(self._latencies)
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        latencies_sorted = sorted(latencies)
        def percentile(p):
            k = (len(latencies_sorted)-1) * (p/100)
            f = int(k)
            c = min(f+1, len(latencies_sorted)-1)
            if f == c:
                return latencies_sorted[int(k)]
            return latencies_sorted[f] + (latencies_sorted[c] - latencies_sorted[f]) * (k-f)
        stats = {
            "avg": avg,
            "p50": p50,
            "p95": percentile(95),
            "p99": percentile(99),
            "min": min(latencies),
            "max": max(latencies)
        }
        logger.debug("Latency stats computed: {}", stats)
        return stats

    def get_doctrine_hit_rate(self) -> float:
        if not self._doctrine_hits:
            logger.info("No doctrine hit data available.")
            return 0.0
        hits = sum(1 for hit in self._doctrine_hits if hit)
        rate = hits / len(self._doctrine_hits)
        logger.debug("Doctrine hit rate: {:.3f}", rate)
        return rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        queries_in_window = [t for t in self._query_timestamps if t >= window_start]
        error_rate = (len(errors_in_window) / len(queries_in_window)) if queries_in_window else 0.0
        logger.debug("Error rate in last {} hours: {:.3f}", window_hours, error_rate)
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for t in self._query_timestamps if t >= one_hour_ago)
        logger.debug("Queries in last hour: {}", count)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        total = sum(self._coverage_modes.values())
        if not total:
            logger.info("No coverage data available.")
            return {
                "modes": {},
                "avg_confidence": None,
                "min_confidence": None,
                "max_confidence": None
            }
        modes = {mode: count/total for mode, count in self._coverage_modes.items()}
        avg_conf = statistics.mean(self._coverage_confidences) if self._coverage_confidences else None
        min_conf = min(self._coverage_confidences) if self._coverage_confidences else None
        max_conf = max(self._coverage_confidences) if self._coverage_confidences else None
        report = {
            "modes": modes,
            "avg_confidence": avg_conf,
            "min_confidence": min_conf,
            "max_confidence": max_conf
        }
        logger.debug("Coverage report: {}", report)
        return report

    def export_jsonl(self, path: str) -> int:
        path_obj = pathlib.Path(path)
        count = 0
        with path_obj.open("w", encoding="utf-8") as f:
            for metrics in self._queries:
                obj = asdict(metrics)
                json.dump(obj, f)
                f.write("\n")
                count += 1
        logger.info("Exported {} queries to {}", count, path)
        return count

class AuditTrailWriter:
    def __init__(self, base_dir: str = "./audit_trail"):
        self.base_dir = pathlib.Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        logger.debug("AuditTrailWriter initialized at {}", self.base_dir)

    def _get_audit_path(self, query_id: str) -> pathlib.Path:
        hash_id = hashlib.sha1(query_id.encode("utf-8")).hexdigest()
        subdir = self.base_dir / hash_id[:2]
        subdir.mkdir(parents=True, exist_ok=True)
        return subdir / f"{hash_id}.jsonl"

    def write(self, metrics: QueryMetrics):
        path = self._get_audit_path(metrics.query_id)
        with path.open("a", encoding="utf-8") as f:
            json.dump(asdict(metrics), f)
            f.write("\n")
        logger.debug("Audit written for query_id: {} at {}", metrics.query_id, path)

COLLECTOR = TelemetryCollector()