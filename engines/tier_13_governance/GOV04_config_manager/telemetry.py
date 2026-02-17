import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "GOV04"

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
    def __init__(self, max_queries: int = 10000, max_errors: int = 1000):
        self._queries: deque = deque(maxlen=max_queries)
        self._errors: deque = deque(maxlen=max_errors)
        self._doctrine_hits: deque = deque(maxlen=max_queries)
        self._latencies: deque = deque(maxlen=max_queries)
        self._query_ids: set = set()
        self._audit_writer = AuditTrailWriter()
        self._coverage_counter: Counter = Counter()
        self._mode_counter: Counter = Counter()
        self._confidence_values: deque = deque(maxlen=max_queries)
        self._cache_hits: deque = deque(maxlen=max_queries)
        logger.info("TelemetryCollector initialized with max_queries={}, max_errors={}", max_queries, max_errors)

    def record_query(self, metrics: QueryMetrics):
        if metrics.query_id in self._query_ids:
            logger.warning("Duplicate query_id detected: {}", metrics.query_id)
            return
        self._queries.append(metrics)
        self._query_ids.add(metrics.query_id)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._mode_counter[metrics.mode] += 1
        self._confidence_values.append(metrics.confidence)
        self._cache_hits.append(metrics.cache_hit)
        self._coverage_counter[(metrics.mode, metrics.doctrine_matched)] += 1
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
        logger.error("Recorded error: {}", error_entry)

    def get_latency_stats(self) -> Dict[str, Any]:
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
        min_latency = min(latencies)
        max_latency = max(latencies)
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
        logger.info("Latency stats: {}", stats)
        return stats

    def get_doctrine_hit_rate(self) -> float:
        hits = sum(self._doctrine_hits)
        total = len(self._doctrine_hits)
        hit_rate = hits / total if total > 0 else 0.0
        logger.info("Doctrine hit rate: {} ({} hits / {} total)", hit_rate, hits, total)
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        queries_in_window = [q for q in self._queries if q.timestamp >= window_start]
        error_count = len(errors_in_window)
        query_count = len(queries_in_window)
        error_rate = error_count / query_count if query_count > 0 else 0.0
        logger.info("Error rate: {} ({} errors / {} queries) in last {} hours", error_rate, error_count, query_count, window_hours)
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= one_hour_ago)
        logger.info("Queries in last hour: {}", count)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {}
        total_queries = len(self._queries)
        for mode in self._mode_counter:
            doctrine_true = self._coverage_counter.get((mode, True), 0)
            doctrine_false = self._coverage_counter.get((mode, False), 0)
            mode_count = self._mode_counter[mode]
            doctrine_rate = doctrine_true / mode_count if mode_count > 0 else 0.0
            report[mode] = {
                "total": mode_count,
                "doctrine_matched": doctrine_true,
                "doctrine_not_matched": doctrine_false,
                "doctrine_match_rate": doctrine_rate
            }
        avg_confidence = statistics.mean(self._confidence_values) if self._confidence_values else None
        cache_hit_rate = sum(self._cache_hits) / len(self._cache_hits) if self._cache_hits else 0.0
        report["overall"] = {
            "total_queries": total_queries,
            "avg_confidence": avg_confidence,
            "cache_hit_rate": cache_hit_rate
        }
        logger.info("Coverage report: {}", report)
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
    def __init__(self, audit_dir: str = "./audit_trails"):
        self.audit_dir = pathlib.Path(audit_dir)
        self.audit_dir.mkdir(parents=True, exist_ok=True)
        logger.info("AuditTrailWriter initialized at {}", self.audit_dir)

    def _get_audit_path(self, query_id: str) -> pathlib.Path:
        hash_id = hashlib.sha256(query_id.encode()).hexdigest()[:16]
        filename = f"{ENGINE_ID}_{hash_id}.jsonl"
        return self.audit_dir / filename

    def write(self, metrics: QueryMetrics):
        path = self._get_audit_path(metrics.query_id)
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(metrics)) + "\n")
        logger.debug("Audit trail written for query_id: {} at {}", metrics.query_id, path)

COLLECTOR = TelemetryCollector()