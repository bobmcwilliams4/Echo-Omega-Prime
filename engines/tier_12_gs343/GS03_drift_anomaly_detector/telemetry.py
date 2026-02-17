import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any, Deque
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "GS03"

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

    def to_dict(self) -> dict:
        return asdict(self)

class TelemetryCollector:
    def __init__(self, maxlen: int = 10000):
        self.queries: Deque[QueryMetrics] = deque(maxlen=maxlen)
        self.errors: Deque[dict] = deque(maxlen=maxlen)
        self.latencies: Deque[float] = deque(maxlen=maxlen)
        self.doctrine_matches: Deque[bool] = deque(maxlen=maxlen)
        self.cache_hits: Deque[bool] = deque(maxlen=maxlen)
        self.modes: Deque[str] = deque(maxlen=maxlen)
        self.confidences: Deque[float] = deque(maxlen=maxlen)
        self.query_timestamps: Deque[float] = deque(maxlen=maxlen)
        self.error_timestamps: Deque[float] = deque(maxlen=maxlen)
        self.coverage_counter: Counter = Counter()
        self.audit_writer = AuditTrailWriter()
        logger.info("TelemetryCollector initialized with maxlen={}", maxlen)

    def record_query(self, metrics: QueryMetrics):
        self.queries.append(metrics)
        self.latencies.append(metrics.latency_ms)
        self.doctrine_matches.append(metrics.doctrine_matched)
        self.cache_hits.append(metrics.cache_hit)
        self.modes.append(metrics.mode)
        self.confidences.append(metrics.confidence)
        self.query_timestamps.append(metrics.timestamp)
        self.coverage_counter[metrics.mode] += 1
        if metrics.error:
            self.record_error(metrics.error, "Error from QueryMetrics", metrics.query_id)
        self.audit_writer.write(metrics)
        logger.debug("Recorded query: {}", metrics)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_event = {
            "timestamp": time.time(),
            "error_type": error_type,
            "message": message,
            "query_id": query_id
        }
        self.errors.append(error_event)
        self.error_timestamps.append(error_event["timestamp"])
        logger.warning("Recorded error: {}", error_event)

    def get_latency_stats(self) -> dict:
        latencies = list(self.latencies)
        if not latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
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
        logger.debug("Latency stats: {}", stats)
        return stats

    def _percentile(self, data: List[float], percentile: float) -> float:
        if not data:
            return None
        data = sorted(data)
        k = (len(data) - 1) * (percentile / 100)
        f = int(k)
        c = f + 1
        if c >= len(data):
            return data[-1]
        d0 = data[f] * (c - k)
        d1 = data[c] * (k - f)
        return d0 + d1

    def get_doctrine_hit_rate(self) -> float:
        matches = list(self.doctrine_matches)
        if not matches:
            return 0.0
        hit_rate = sum(matches) / len(matches)
        logger.debug("Doctrine hit rate: {}", hit_rate)
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        error_count = sum(1 for t in self.error_timestamps if t >= window_start)
        query_count = sum(1 for t in self.query_timestamps if t >= window_start)
        if query_count == 0:
            return 0.0
        error_rate = error_count / query_count
        logger.debug("Error rate ({}h): {}", window_hours, error_rate)
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for t in self.query_timestamps if t >= one_hour_ago)
        logger.debug("Queries in last hour: {}", count)
        return count

    def get_coverage_report(self) -> dict:
        total = sum(self.coverage_counter.values())
        if total == 0:
            return {}
        report = {mode: count / total for mode, count in self.coverage_counter.items()}
        logger.debug("Coverage report: {}", report)
        return report

    def export_jsonl(self, path: str) -> int:
        p = pathlib.Path(path)
        count = 0
        with p.open("w", encoding="utf-8") as f:
            for q in self.queries:
                f.write(json.dumps(q.to_dict(), ensure_ascii=False) + "\n")
                count += 1
        logger.info("Exported {} queries to {}", count, path)
        return count

class AuditTrailWriter:
    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = pathlib.Path(base_dir) if base_dir else pathlib.Path("./audit_trail")
        self.base_dir.mkdir(parents=True, exist_ok=True)
        logger.info("AuditTrailWriter initialized at {}", self.base_dir)

    def write(self, metrics: QueryMetrics):
        date_str = time.strftime("%Y-%m-%d")
        file_path = self.base_dir / f"{ENGINE_ID}_audit_{date_str}.jsonl"
        record = metrics.to_dict()
        record["audit_hash"] = self._hash_record(record)
        with file_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
        logger.debug("Wrote audit trail for query_id={}", metrics.query_id)

    def _hash_record(self, record: dict) -> str:
        # Deterministic hash for audit
        record_bytes = json.dumps(record, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(record_bytes).hexdigest()

COLLECTOR = TelemetryCollector()