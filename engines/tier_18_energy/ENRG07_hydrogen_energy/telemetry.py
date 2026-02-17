import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict, field
from typing import Optional, List, Dict, Any, Deque
from collections import deque, Counter
from loguru import logger

ENGINE_ID = "ENRG07"

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
        self._doctrine_matches: Deque[bool] = deque(maxlen=maxlen)
        self._cache_hits: Deque[bool] = deque(maxlen=maxlen)
        self._latencies: Deque[float] = deque(maxlen=maxlen)
        self._query_times: Deque[float] = deque(maxlen=maxlen)
        self._query_ids: Deque[str] = deque(maxlen=maxlen)
        self._modes: Deque[str] = deque(maxlen=maxlen)
        self._confidences: Deque[float] = deque(maxlen=maxlen)
        self._coverage_counter: Counter = Counter()
        self._audit_writer = AuditTrailWriter()
        logger.info("TelemetryCollector initialized with maxlen={}", maxlen)

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_matches.append(metrics.doctrine_matched)
        self._cache_hits.append(metrics.cache_hit)
        self._query_times.append(metrics.timestamp)
        self._query_ids.append(metrics.query_id)
        self._modes.append(metrics.mode)
        self._confidences.append(metrics.confidence)
        self._coverage_counter[metrics.mode] += 1
        if metrics.error:
            self.record_error(metrics.error, "Recorded via QueryMetrics", metrics.query_id)
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

    def get_latency_stats(self) -> Dict[str, float]:
        latencies = list(self._latencies)
        if not latencies:
            return {"avg": 0, "p50": 0, "p95": 0, "p99": 0, "min": 0, "max": 0}
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = latencies_sorted[int(0.95 * len(latencies_sorted)) - 1]
        p99 = latencies_sorted[int(0.99 * len(latencies_sorted)) - 1]
        min_latency = latencies_sorted[0]
        max_latency = latencies_sorted[-1]
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

    def get_doctrine_hit_rate(self) -> float:
        matches = list(self._doctrine_matches)
        if not matches:
            return 0.0
        hit_rate = sum(matches) / len(matches)
        logger.debug("Doctrine hit rate: {}", hit_rate)
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        error_count = sum(1 for e in self._errors if e["timestamp"] >= window_start)
        query_count = sum(1 for t in self._query_times if t >= window_start)
        error_rate = (error_count / query_count) if query_count > 0 else 0.0
        logger.debug("Error rate in last {} hours: {}", window_hours, error_rate)
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for t in self._query_times if t >= one_hour_ago)
        logger.debug("Queries in last hour: {}", count)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        total = sum(self._coverage_counter.values())
        report = {
            "total": total,
            "by_mode": {},
            "confidence": {}
        }
        for mode, count in self._coverage_counter.items():
            report["by_mode"][mode] = count
        confidences_by_mode = {}
        for mode in set(self._modes):
            indices = [i for i, m in enumerate(self._modes) if m == mode]
            confidences = [self._confidences[i] for i in indices]
            if confidences:
                confidences_by_mode[mode] = {
                    "avg": statistics.mean(confidences),
                    "min": min(confidences),
                    "max": max(confidences)
                }
        report["confidence"] = confidences_by_mode
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
            base_dir = "./audit_trails"
        self.base_dir = pathlib.Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        logger.info("AuditTrailWriter initialized at {}", self.base_dir)

    def write(self, metrics: QueryMetrics):
        date_str = time.strftime("%Y%m%d")
        filename = f"{ENGINE_ID}_audit_{date_str}.jsonl"
        path = self.base_dir / filename
        entry = asdict(metrics)
        entry["audit_hash"] = self._hash_entry(entry)
        try:
            with path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
            logger.debug("Wrote audit trail for query_id={}", metrics.query_id)
        except Exception as e:
            logger.exception("Failed to write audit trail: {}", e)

    def _hash_entry(self, entry: Dict[str, Any]) -> str:
        # Hash all fields except audit_hash itself
        entry_copy = dict(entry)
        entry_copy.pop("audit_hash", None)
        entry_json = json.dumps(entry_copy, sort_keys=True)
        return hashlib.sha256(entry_json.encode("utf-8")).hexdigest()

COLLECTOR = TelemetryCollector()