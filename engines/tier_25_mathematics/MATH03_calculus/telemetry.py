import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "MATH03"

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
    def __init__(self, max_queries: int = 10000):
        self._queries: deque = deque(maxlen=max_queries)
        self._errors: deque = deque(maxlen=max_queries)
        self._doctrine_hits: deque = deque(maxlen=max_queries)
        self._latencies: deque = deque(maxlen=max_queries)
        self._modes: Counter = Counter()
        self._confidence_scores: deque = deque(maxlen=max_queries)
        self._cache_hits: deque = deque(maxlen=max_queries)
        self._query_timestamps: deque = deque(maxlen=max_queries)
        self._query_ids: set = set()
        self._audit_writer = AuditTrailWriter()
        logger.info("TelemetryCollector initialized with max_queries={}", max_queries)

    def record_query(self, metrics: QueryMetrics):
        logger.debug("Recording query: {}", metrics)
        self._queries.append(metrics)
        self._query_ids.add(metrics.query_id)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._modes[metrics.mode] += 1
        self._confidence_scores.append(metrics.confidence)
        self._cache_hits.append(metrics.cache_hit)
        self._query_timestamps.append(metrics.timestamp)
        if metrics.error:
            self.record_error(metrics.error, "Query error", metrics.query_id)
        self._audit_writer.write(metrics)
        logger.info("Query recorded: {}", metrics.query_id)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "timestamp": time.time(),
        }
        self._errors.append(error_entry)
        logger.warning("Error recorded: {} for query_id={}", error_type, query_id)

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = list(self._latencies)
        if not latencies:
            logger.debug("No latencies recorded.")
            return {
                "avg": None,
                "p50": None,
                "p95": None,
                "p99": None,
                "min": None,
                "max": None,
            }
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = latencies_sorted[int(0.95 * len(latencies_sorted)) - 1]
        p99 = latencies_sorted[int(0.99 * len(latencies_sorted)) - 1]
        min_latency = min(latencies)
        max_latency = max(latencies)
        logger.debug("Latency stats calculated.")
        return {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_latency,
            "max": max_latency,
        }

    def get_doctrine_hit_rate(self) -> float:
        hits = sum(1 for hit in self._doctrine_hits if hit)
        total = len(self._doctrine_hits)
        if total == 0:
            logger.debug("No doctrine hits recorded.")
            return 0.0
        hit_rate = hits / total
        logger.debug("Doctrine hit rate: {:.2f}", hit_rate)
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        queries_in_window = [q for q in self._queries if q.timestamp >= window_start]
        num_errors = len(errors_in_window)
        num_queries = len(queries_in_window)
        if num_queries == 0:
            logger.debug("No queries in window for error rate.")
            return 0.0
        error_rate = num_errors / num_queries
        logger.debug("Error rate in last {:.2f} hours: {:.4f}", window_hours, error_rate)
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        window_start = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= window_start)
        logger.debug("Queries in last hour: {}", count)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        mode_counts = dict(self._modes)
        total_queries = len(self._queries)
        doctrine_hit_rate = self.get_doctrine_hit_rate()
        error_rate = self.get_error_rate(window_hours=24)
        avg_confidence = statistics.mean(self._confidence_scores) if self._confidence_scores else None
        cache_hit_rate = sum(1 for hit in self._cache_hits if hit) / len(self._cache_hits) if self._cache_hits else 0.0
        report = {
            "engine_id": ENGINE_ID,
            "total_queries": total_queries,
            "mode_counts": mode_counts,
            "doctrine_hit_rate": doctrine_hit_rate,
            "error_rate_24h": error_rate,
            "avg_confidence": avg_confidence,
            "cache_hit_rate": cache_hit_rate,
        }
        logger.info("Coverage report generated.")
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
    def __init__(self, base_path: Optional[str] = None):
        self.base_path = base_path or "./audit_trails"
        self._ensure_dir()
        logger.info("AuditTrailWriter initialized at {}", self.base_path)

    def _ensure_dir(self):
        p = pathlib.Path(self.base_path)
        p.mkdir(parents=True, exist_ok=True)

    def write(self, metrics: QueryMetrics):
        filename = self._get_filename(metrics.query_id)
        p = pathlib.Path(self.base_path) / filename
        with p.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(metrics)) + "\n")
        logger.debug("Audit trail written for query_id={}", metrics.query_id)

    def _get_filename(self, query_id: str) -> str:
        hash_id = hashlib.sha256(query_id.encode("utf-8")).hexdigest()[:16]
        return f"{ENGINE_ID}_{hash_id}.jsonl"

COLLECTOR = TelemetryCollector()