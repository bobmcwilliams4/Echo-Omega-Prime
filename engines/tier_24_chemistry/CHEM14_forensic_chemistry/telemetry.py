import time
import json
import hashlib
import statistics
import pathlib
import dataclasses
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any
import collections
from collections import deque, Counter
from loguru import logger

ENGINE_ID = "CHEM14"

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
        self._metrics: deque = deque(maxlen=maxlen)
        self._errors: deque = deque(maxlen=maxlen)
        self._doctrine_hits: deque = deque(maxlen=maxlen)
        self._latencies: deque = deque(maxlen=maxlen)
        self._modes: Counter = Counter()
        self._confidence: deque = deque(maxlen=maxlen)
        self._cache_hits: deque = deque(maxlen=maxlen)
        self._coverage: Counter = Counter()
        self._query_timestamps: deque = deque(maxlen=maxlen)
        self._query_ids: set = set()
        self._audit_writer = AuditTrailWriter()
        logger.debug("TelemetryCollector initialized with maxlen={}", maxlen)

    def record_query(self, metrics: QueryMetrics):
        logger.debug("Recording query: {}", metrics)
        self._metrics.append(metrics)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._modes[metrics.mode] += 1
        self._confidence.append(metrics.confidence)
        self._cache_hits.append(metrics.cache_hit)
        self._coverage[metrics.mode] += 1
        self._query_timestamps.append(metrics.timestamp)
        self._query_ids.add(metrics.query_id)
        self._audit_writer.write(metrics)
        if metrics.error:
            self.record_error(metrics.error, metrics.error, metrics.query_id)

    def record_error(self, error_type: str, message: str, query_id: str):
        error_entry = {
            "timestamp": time.time(),
            "error_type": error_type,
            "message": message,
            "query_id": query_id
        }
        logger.error("Recording error: {}", error_entry)
        self._errors.append(error_entry)

    def get_latency_stats(self) -> Dict[str, Any]:
        if not self._latencies:
            logger.warning("No latency data to compute stats.")
            return {
                "avg": None,
                "p50": None,
                "p95": None,
                "p99": None,
                "min": None,
                "max": None
            }
        latencies = list(self._latencies)
        latencies.sort()
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = latencies[int(0.95 * len(latencies)) - 1]
        p99 = latencies[int(0.99 * len(latencies)) - 1]
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
        logger.debug("Latency stats computed: {}", stats)
        return stats

    def get_doctrine_hit_rate(self) -> float:
        if not self._doctrine_hits:
            logger.warning("No doctrine hit data.")
            return 0.0
        hit_rate = sum(self._doctrine_hits) / len(self._doctrine_hits)
        logger.debug("Doctrine hit rate: {}", hit_rate)
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        total = 0
        errors = 0
        for metrics in self._metrics:
            if metrics.timestamp >= window_start:
                total += 1
                if metrics.error:
                    errors += 1
        error_rate = (errors / total) if total > 0 else 0.0
        logger.debug("Error rate in last {} hours: {}", window_hours, error_rate)
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for ts in self._query_timestamps if ts >= one_hour_ago)
        logger.debug("Queries in last hour: {}", count)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        total = sum(self._coverage.values())
        report = {}
        for mode, count in self._coverage.items():
            report[mode] = {
                "count": count,
                "pct": (count / total) * 100 if total > 0 else 0.0
            }
        logger.debug("Coverage report: {}", report)
        return report

    def export_jsonl(self, path: str) -> int:
        p = pathlib.Path(path)
        count = 0
        with p.open("w", encoding="utf-8") as f:
            for metrics in self._metrics:
                f.write(json.dumps(asdict(metrics)) + "\n")
                count += 1
        logger.info("Exported {} records to {}", count, path)
        return count

class AuditTrailWriter:
    def __init__(self, base_dir: Optional[str] = None):
        if base_dir is None:
            base_dir = "./audit_trail"
        self.base_dir = pathlib.Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        logger.debug("AuditTrailWriter initialized at {}", str(self.base_dir))

    def write(self, metrics: QueryMetrics):
        audit_record = {
            "query_id": metrics.query_id,
            "engine_id": metrics.engine_id,
            "timestamp": metrics.timestamp,
            "latency_ms": metrics.latency_ms,
            "cache_hit": metrics.cache_hit,
            "doctrine_matched": metrics.doctrine_matched,
            "mode": metrics.mode,
            "confidence": metrics.confidence,
            "error": metrics.error
        }
        filename = self._get_audit_filename(metrics.query_id)
        with filename.open("a", encoding="utf-8") as f:
            f.write(json.dumps(audit_record) + "\n")
        logger.debug("Audit record written for query_id {} to {}", metrics.query_id, str(filename))

    def _get_audit_filename(self, query_id: str) -> pathlib.Path:
        # Hash the query_id to avoid filesystem issues
        h = hashlib.sha256(query_id.encode("utf-8")).hexdigest()
        filename = self.base_dir / f"{h}.jsonl"
        return filename

COLLECTOR = TelemetryCollector()