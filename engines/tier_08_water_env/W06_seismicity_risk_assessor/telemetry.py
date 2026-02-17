import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "W06"

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
        self._queries = deque(maxlen=maxlen)
        self._errors = deque(maxlen=maxlen)
        self._doctrine_hits = deque(maxlen=maxlen)
        self._latencies = deque(maxlen=maxlen)
        self._modes = deque(maxlen=maxlen)
        self._confidences = deque(maxlen=maxlen)
        self._query_times = deque(maxlen=maxlen)
        self._query_ids = set()
        self._audit_trail_writer = AuditTrailWriter()
        self._mode_counter = Counter()
        self._doctrine_counter = Counter()
        self._cache_counter = Counter()
        self._coverage_by_mode = defaultdict(int)
        self._coverage_by_doctrine = defaultdict(int)
        self._coverage_by_cache = defaultdict(int)
        self._coverage_by_confidence = defaultdict(list)
        self._all_metrics = []
        logger.info("TelemetryCollector initialized with maxlen={}", maxlen)

    def record_query(self, metrics: QueryMetrics):
        if metrics.query_id in self._query_ids:
            logger.warning("Duplicate query_id detected: {}", metrics.query_id)
            return
        self._queries.append(metrics)
        self._query_ids.add(metrics.query_id)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._modes.append(metrics.mode)
        self._confidences.append(metrics.confidence)
        self._query_times.append(metrics.timestamp)
        self._mode_counter[metrics.mode] += 1
        self._doctrine_counter[metrics.doctrine_matched] += 1
        self._cache_counter[metrics.cache_hit] += 1
        self._coverage_by_mode[metrics.mode] += 1
        self._coverage_by_doctrine[metrics.doctrine_matched] += 1
        self._coverage_by_cache[metrics.cache_hit] += 1
        self._coverage_by_confidence[metrics.mode].append(metrics.confidence)
        self._all_metrics.append(metrics)
        self._audit_trail_writer.write(metrics)
        logger.debug("Recorded query: {}", metrics)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "error_type": error_type,
            "message": message,
            "query_id": query_id
        }
        self._errors.append(error_entry)
        logger.error("Error recorded: {}", error_entry)

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = list(self._latencies)
        if not latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
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
        logger.debug("Latency stats: {}", stats)
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
        total = len(self._doctrine_hits)
        if total == 0:
            return 0.0
        hits = sum(1 for hit in self._doctrine_hits if hit)
        rate = hits / total
        logger.debug("Doctrine hit rate: {:.2f}", rate)
        return rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        queries_in_window = [t for t in self._query_times if t >= window_start]
        num_queries = len(queries_in_window)
        if num_queries == 0:
            return 0.0
        error_rate = len(errors_in_window) / num_queries
        logger.debug("Error rate in last {:.2f} hours: {:.4f}", window_hours, error_rate)
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for t in self._query_times if t >= one_hour_ago)
        logger.debug("Queries in last hour: {}", count)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {
            "total_queries": len(self._queries),
            "by_mode": dict(self._coverage_by_mode),
            "by_doctrine": {str(k): v for k, v in self._coverage_by_doctrine.items()},
            "by_cache": {str(k): v for k, v in self._coverage_by_cache.items()},
            "confidence_by_mode": {
                mode: {
                    "avg": statistics.mean(vals) if vals else None,
                    "min": min(vals) if vals else None,
                    "max": max(vals) if vals else None
                }
                for mode, vals in self._coverage_by_confidence.items()
            }
        }
        logger.debug("Coverage report: {}", report)
        return report

    def export_jsonl(self, path: str) -> int:
        p = pathlib.Path(path)
        count = 0
        with p.open("w", encoding="utf-8") as f:
            for metrics in self._all_metrics:
                f.write(json.dumps(asdict(metrics)) + "\n")
                count += 1
        logger.info("Exported {} telemetry records to {}", count, path)
        return count

class AuditTrailWriter:
    def __init__(self, audit_dir: str = "./audit_trails"):
        self._dir = pathlib.Path(audit_dir)
        self._dir.mkdir(parents=True, exist_ok=True)
        logger.info("AuditTrailWriter initialized at {}", audit_dir)

    def write(self, metrics: QueryMetrics):
        audit_entry = asdict(metrics)
        audit_entry["audit_timestamp"] = time.time()
        fname = self._get_audit_filename(metrics.query_id)
        with open(fname, "a", encoding="utf-8") as f:
            f.write(json.dumps(audit_entry) + "\n")
        logger.debug("Wrote audit trail for query_id {} to {}", metrics.query_id, fname)

    def _get_audit_filename(self, query_id: str) -> str:
        # Use a hash to avoid filename issues
        h = hashlib.sha256(query_id.encode("utf-8")).hexdigest()
        fname = self._dir / f"audit_{h}.jsonl"
        return str(fname)

COLLECTOR = TelemetryCollector()