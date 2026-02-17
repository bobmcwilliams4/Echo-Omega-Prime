import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional, Any
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "MED01"

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
        self._queries: deque = deque(maxlen=maxlen)
        self._errors: deque = deque(maxlen=maxlen)
        self._doctrine_hits: deque = deque(maxlen=maxlen)
        self._latencies: deque = deque(maxlen=maxlen)
        self._cache_hits: deque = deque(maxlen=maxlen)
        self._query_modes: deque = deque(maxlen=maxlen)
        self._confidence_scores: deque = deque(maxlen=maxlen)
        self._query_timestamps: deque = deque(maxlen=maxlen)
        self._query_id_map: Dict[str, QueryMetrics] = {}
        self._error_counter: Counter = Counter()
        self._doctrine_counter: Counter = Counter()
        self._audit_writer = AuditTrailWriter()
        logger.info("TelemetryCollector initialized with maxlen={}", maxlen)

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._query_id_map[metrics.query_id] = metrics
        self._latencies.append(metrics.latency_ms)
        self._cache_hits.append(metrics.cache_hit)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._query_modes.append(metrics.mode)
        self._confidence_scores.append(metrics.confidence)
        self._query_timestamps.append(metrics.timestamp)
        self._doctrine_counter[metrics.doctrine_matched] += 1
        if metrics.error:
            self.record_error(metrics.error, "Query error", metrics.query_id)
        self._audit_writer.write(metrics)
        logger.debug("Recorded query: {}", metrics)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "error_type": error_type,
            "message": message,
            "query_id": query_id
        }
        self._errors.append(error_entry)
        self._error_counter[error_type] += 1
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
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        min_latency = latencies_sorted[0]
        max_latency = latencies_sorted[-1]
        p50 = statistics.median(latencies)
        p95 = latencies_sorted[int(0.95 * len(latencies_sorted)) - 1]
        p99 = latencies_sorted[int(0.99 * len(latencies_sorted)) - 1]
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
        total = len(self._doctrine_hits)
        if total == 0:
            return 0.0
        hits = sum(1 for hit in self._doctrine_hits if hit)
        hit_rate = hits / total
        logger.debug("Doctrine hit rate: {} ({} hits / {} total)", hit_rate, hits, total)
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        total_queries = sum(1 for t in self._query_timestamps if t >= window_start)
        total_errors = sum(1 for e in self._errors if e["timestamp"] >= window_start)
        if total_queries == 0:
            return 0.0
        error_rate = total_errors / total_queries
        logger.debug("Error rate: {} ({} errors / {} queries) in last {} hours", error_rate, total_errors, total_queries, window_hours)
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for t in self._query_timestamps if t >= one_hour_ago)
        logger.debug("Queries in last hour: {}", count)
        return count

    def get_coverage_report(self) -> dict:
        mode_counter = Counter(self._query_modes)
        cache_hit_counter = Counter(self._cache_hits)
        doctrine_counter = Counter(self._doctrine_hits)
        total = len(self._queries)
        coverage = {
            "total_queries": total,
            "mode_distribution": dict(mode_counter),
            "cache_hit_rate": cache_hit_counter.get(True, 0) / total if total else 0.0,
            "doctrine_matched_rate": doctrine_counter.get(True, 0) / total if total else 0.0,
            "confidence_avg": statistics.mean(self._confidence_scores) if self._confidence_scores else None,
            "confidence_min": min(self._confidence_scores) if self._confidence_scores else None,
            "confidence_max": max(self._confidence_scores) if self._confidence_scores else None,
            "errors_by_type": dict(self._error_counter)
        }
        logger.debug("Coverage report: {}", coverage)
        return coverage

    def export_jsonl(self, path: str) -> int:
        p = pathlib.Path(path)
        count = 0
        with p.open("w", encoding="utf-8") as f:
            for metrics in self._queries:
                f.write(json.dumps(metrics.to_dict()) + "\n")
                count += 1
        logger.info("Exported {} queries to {}", count, path)
        return count

class AuditTrailWriter:
    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = pathlib.Path(base_dir) if base_dir else pathlib.Path("./audit_trail")
        self.base_dir.mkdir(parents=True, exist_ok=True)
        logger.info("AuditTrailWriter initialized at {}", self.base_dir)

    def write(self, metrics: QueryMetrics):
        date_str = time.strftime("%Y-%m-%d", time.localtime(metrics.timestamp))
        file_path = self.base_dir / f"{ENGINE_ID}_{date_str}.jsonl"
        entry = metrics.to_dict()
        entry["audit_written_at"] = time.time()
        with file_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        logger.debug("Audit trail written for query_id {} to {}", metrics.query_id, file_path)

COLLECTOR = TelemetryCollector()