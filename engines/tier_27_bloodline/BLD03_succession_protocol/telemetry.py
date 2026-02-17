import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict, field
from typing import Optional, List, Dict, Any, Deque
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "BLD03"

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
        self._queries: Deque[QueryMetrics] = deque(maxlen=maxlen)
        self._errors: Deque[dict] = deque(maxlen=maxlen)
        self._doctrine_hits: int = 0
        self._doctrine_total: int = 0
        self._latencies: Deque[float] = deque(maxlen=maxlen)
        self._cache_hits: int = 0
        self._cache_total: int = 0
        self._mode_counter: Counter = Counter()
        self._confidence_values: Deque[float] = deque(maxlen=maxlen)
        self._coverage_modes: Counter = Counter()
        self._coverage_doctrines: Counter = Counter()
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
        self._latencies.append(metrics.latency_ms)
        self._query_timestamps.append(metrics.timestamp)
        self._mode_counter[metrics.mode] += 1
        self._confidence_values.append(metrics.confidence)
        self._coverage_modes[metrics.mode] += 1
        if metrics.doctrine_matched:
            self._doctrine_hits += 1
            self._coverage_doctrines["matched"] += 1
        else:
            self._coverage_doctrines["unmatched"] += 1
        self._doctrine_total += 1
        if metrics.cache_hit:
            self._cache_hits += 1
        self._cache_total += 1
        if metrics.error:
            self.record_error(metrics.error, "Error in query", metrics.query_id)
        self._audit_writer.write(metrics)
        logger.debug(f"Recorded query: {metrics.query_id}")

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "engine_id": ENGINE_ID
        }
        self._errors.append(error_entry)
        logger.error(f"Error recorded: {error_type} - {message} (query_id={query_id})")

    def get_latency_stats(self) -> dict:
        if not self._latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        latencies = list(self._latencies)
        latencies.sort()
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
        logger.debug(f"Latency stats: {stats}")
        return stats

    def get_doctrine_hit_rate(self) -> float:
        if self._doctrine_total == 0:
            return 0.0
        hit_rate = self._doctrine_hits / self._doctrine_total
        logger.debug(f"Doctrine hit rate: {hit_rate}")
        return hit_rate

    def get_error_rate(self, window_hours: float) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        total_queries = sum(1 for ts in self._query_timestamps if ts >= window_start)
        total_errors = sum(1 for err in self._errors if err["timestamp"] >= window_start)
        if total_queries == 0:
            return 0.0
        error_rate = total_errors / total_queries
        logger.debug(f"Error rate (last {window_hours}h): {error_rate}")
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for ts in self._query_timestamps if ts >= one_hour_ago)
        logger.debug(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> dict:
        total = len(self._queries)
        if total == 0:
            return {
                "total": 0,
                "modes": {},
                "doctrine_matched": 0,
                "doctrine_unmatched": 0,
                "cache_hit": 0,
                "cache_miss": 0,
                "avg_confidence": None
            }
        modes = dict(self._coverage_modes)
        doctrine_matched = self._coverage_doctrines["matched"]
        doctrine_unmatched = self._coverage_doctrines["unmatched"]
        cache_hit = self._cache_hits
        cache_miss = self._cache_total - self._cache_hits
        avg_confidence = statistics.mean(self._confidence_values) if self._confidence_values else None
        report = {
            "total": total,
            "modes": modes,
            "doctrine_matched": doctrine_matched,
            "doctrine_unmatched": doctrine_unmatched,
            "cache_hit": cache_hit,
            "cache_miss": cache_miss,
            "avg_confidence": avg_confidence
        }
        logger.debug(f"Coverage report: {report}")
        return report

    def export_jsonl(self, path: str) -> int:
        p = pathlib.Path(path)
        count = 0
        with p.open("w", encoding="utf-8") as f:
            for qm in self._queries:
                json_line = json.dumps(qm.to_dict(), ensure_ascii=False)
                f.write(json_line + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {path}")
        return count

class AuditTrailWriter:
    def __init__(self, base_dir: Optional[str] = None):
        if base_dir is None:
            base_dir = "./bld03_audit_trail"
        self.base_dir = pathlib.Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"AuditTrailWriter initialized at {self.base_dir}")

    def _get_audit_path(self, query_id: str) -> pathlib.Path:
        # Use SHA1 hash of query_id to avoid filesystem issues
        h = hashlib.sha1(query_id.encode("utf-8")).hexdigest()
        subdir = self.base_dir / h[:2]
        subdir.mkdir(parents=True, exist_ok=True)
        return subdir / f"{h}.jsonl"

    def write(self, metrics: QueryMetrics):
        path = self._get_audit_path(metrics.query_id)
        with path.open("a", encoding="utf-8") as f:
            json_line = json.dumps(metrics.to_dict(), ensure_ascii=False)
            f.write(json_line + "\n")
        logger.debug(f"Audit trail written for query_id={metrics.query_id} at {path}")

COLLECTOR = TelemetryCollector()