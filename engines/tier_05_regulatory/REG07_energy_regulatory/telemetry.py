import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict, field
from typing import Optional, List, Dict, Any, Deque
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "REG07"

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
        self._doctrine_hits: int = 0
        self._doctrine_total: int = 0
        self._latencies: Deque[float] = deque(maxlen=maxlen)
        self._cache_hits: int = 0
        self._cache_total: int = 0
        self._mode_counter: Counter = Counter()
        self._confidence_scores: Deque[float] = deque(maxlen=maxlen)
        self._error_counter: Counter = Counter()
        self._query_timestamps: Deque[float] = deque(maxlen=maxlen)
        self._audit_writer = AuditTrailWriter()
        logger.debug("TelemetryCollector initialized with maxlen={}", maxlen)

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_total += 1
        if metrics.doctrine_matched:
            self._doctrine_hits += 1
        self._cache_total += 1
        if metrics.cache_hit:
            self._cache_hits += 1
        self._mode_counter[metrics.mode] += 1
        self._confidence_scores.append(metrics.confidence)
        self._query_timestamps.append(metrics.timestamp)
        if metrics.error:
            self._error_counter[metrics.error] += 1
        self._audit_writer.write(metrics)
        logger.debug("Recorded query: {}", metrics)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "engine_id": ENGINE_ID,
            "error_type": error_type,
            "message": message,
            "query_id": query_id
        }
        self._errors.append(error_entry)
        self._error_counter[error_type] += 1
        logger.error("Error recorded: {}", error_entry)

    def get_latency_stats(self) -> Dict[str, float]:
        if not self._latencies:
            return {"avg": 0, "p50": 0, "p95": 0, "p99": 0, "min": 0, "max": 0}
        latencies = sorted(self._latencies)
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = latencies[int(0.95 * len(latencies)) - 1]
        p99 = latencies[int(0.99 * len(latencies)) - 1]
        min_v = latencies[0]
        max_v = latencies[-1]
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
        if self._doctrine_total == 0:
            return 0.0
        hit_rate = self._doctrine_hits / self._doctrine_total
        logger.debug("Doctrine hit rate: {:.4f}", hit_rate)
        return hit_rate

    def get_error_rate(self, window_hours: float) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        total_queries = 0
        error_queries = 0
        for qm in self._queries:
            if qm.timestamp >= window_start:
                total_queries += 1
                if qm.error:
                    error_queries += 1
        if total_queries == 0:
            return 0.0
        error_rate = error_queries / total_queries
        logger.debug("Error rate over last {} hours: {:.4f}", window_hours, error_rate)
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = 0
        for ts in reversed(self._query_timestamps):
            if ts >= one_hour_ago:
                count += 1
            else:
                break
        logger.debug("Queries in last hour: {}", count)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        total = len(self._queries)
        if total == 0:
            return {
                "total": 0,
                "cache_hit_rate": 0.0,
                "doctrine_hit_rate": 0.0,
                "modes": {},
                "confidence_avg": 0.0,
                "confidence_min": 0.0,
                "confidence_max": 0.0
            }
        cache_hit_rate = self._cache_hits / self._cache_total if self._cache_total else 0.0
        doctrine_hit_rate = self.get_doctrine_hit_rate()
        modes = dict(self._mode_counter)
        conf_scores = list(self._confidence_scores)
        confidence_avg = statistics.mean(conf_scores)
        confidence_min = min(conf_scores)
        confidence_max = max(conf_scores)
        report = {
            "total": total,
            "cache_hit_rate": cache_hit_rate,
            "doctrine_hit_rate": doctrine_hit_rate,
            "modes": modes,
            "confidence_avg": confidence_avg,
            "confidence_min": confidence_min,
            "confidence_max": confidence_max
        }
        logger.debug("Coverage report: {}", report)
        return report

    def export_jsonl(self, path: str) -> int:
        p = pathlib.Path(path)
        count = 0
        with p.open("w", encoding="utf-8") as f:
            for qm in self._queries:
                f.write(json.dumps(asdict(qm)) + "\n")
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
        # Use hash to avoid too many files in a single directory
        h = hashlib.sha1(query_id.encode("utf-8")).hexdigest()
        subdir = self.base_dir / h[:2]
        subdir.mkdir(parents=True, exist_ok=True)
        return subdir / f"{query_id}.jsonl"

    def write(self, metrics: QueryMetrics):
        path = self._get_audit_path(metrics.query_id)
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(metrics)) + "\n")
        logger.debug("Audit trail written for query_id={}", metrics.query_id)

COLLECTOR = TelemetryCollector()