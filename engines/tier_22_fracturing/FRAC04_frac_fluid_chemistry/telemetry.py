import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional, Any
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "FRAC04"

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
        self._doctrine_matches = deque(maxlen=maxlen)
        self._latencies = deque(maxlen=maxlen)
        self._cache_hits = deque(maxlen=maxlen)
        self._modes = deque(maxlen=maxlen)
        self._confidences = deque(maxlen=maxlen)
        self._coverage = defaultdict(set)  # mode -> set of query_ids
        self._query_timestamps = deque(maxlen=maxlen)
        self._query_ids = set()
        self._audit_writer = AuditTrailWriter()
        logger.info("TelemetryCollector initialized with maxlen={}", maxlen)

    def record_query(self, metrics: QueryMetrics):
        logger.debug("Recording query: {}", metrics)
        self._queries.append(metrics)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_matches.append(metrics.doctrine_matched)
        self._cache_hits.append(metrics.cache_hit)
        self._modes.append(metrics.mode)
        self._confidences.append(metrics.confidence)
        self._query_timestamps.append(metrics.timestamp)
        self._query_ids.add(metrics.query_id)
        self._coverage[metrics.mode].add(metrics.query_id)
        if metrics.error:
            self.record_error(metrics.error, "Error in query", metrics.query_id)
        self._audit_writer.write(metrics)
        logger.debug("Query recorded: {}", metrics.query_id)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "timestamp": time.time()
        }
        self._errors.append(error_entry)
        logger.warning("Error recorded: {} - {}", error_type, message)

    def get_latency_stats(self) -> Dict[str, Any]:
        if not self._latencies:
            logger.info("No latencies recorded yet.")
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        latencies = list(self._latencies)
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

    def _percentile(self, data: List[float], percentile: float) -> float:
        if not data:
            return None
        data = sorted(data)
        k = (len(data)-1) * (percentile/100)
        f = int(k)
        c = min(f+1, len(data)-1)
        if f == c:
            return data[int(k)]
        d0 = data[f] * (c-k)
        d1 = data[c] * (k-f)
        return d0 + d1

    def get_doctrine_hit_rate(self) -> float:
        if not self._doctrine_matches:
            logger.info("No doctrine matches recorded yet.")
            return 0.0
        hits = sum(1 for matched in self._doctrine_matches if matched)
        rate = hits / len(self._doctrine_matches)
        logger.debug("Doctrine hit rate: {}", rate)
        return rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        queries_in_window = [t for t in self._query_timestamps if t >= window_start]
        error_rate = (len(errors_in_window) / len(queries_in_window)) if queries_in_window else 0.0
        logger.debug("Error rate ({}h): {}", window_hours, error_rate)
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for t in self._query_timestamps if t >= one_hour_ago)
        logger.debug("Queries in last hour: {}", count)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {}
        for mode, queries in self._coverage.items():
            report[mode] = len(queries)
        logger.debug("Coverage report: {}", report)
        return report

    def export_jsonl(self, path: str) -> int:
        p = pathlib.Path(path)
        count = 0
        with p.open("w", encoding="utf-8") as f:
            for metrics in self._queries:
                obj = asdict(metrics)
                f.write(json.dumps(obj) + "\n")
                count += 1
        logger.info("Exported {} queries to {}", count, path)
        return count

class AuditTrailWriter:
    def __init__(self, base_dir: Optional[str] = None):
        if base_dir is None:
            base_dir = "./audit_trail"
        self.base_dir = pathlib.Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        logger.info("AuditTrailWriter initialized at {}", self.base_dir)

    def write(self, metrics: QueryMetrics):
        ts = int(metrics.timestamp)
        date_str = time.strftime("%Y-%m-%d", time.gmtime(ts))
        file_path = self.base_dir / f"{date_str}_audit.jsonl"
        entry = asdict(metrics)
        entry["audit_id"] = self._make_audit_id(metrics)
        with file_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        logger.debug("Wrote audit trail for query_id={} to {}", metrics.query_id, file_path)

    def _make_audit_id(self, metrics: QueryMetrics) -> str:
        base = f"{metrics.query_id}:{metrics.timestamp}:{metrics.engine_id}"
        return hashlib.sha256(base.encode("utf-8")).hexdigest()

COLLECTOR = TelemetryCollector()