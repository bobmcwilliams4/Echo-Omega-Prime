import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any, Union
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "AERO09"

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
        self._doctrine_hits: int = 0
        self._doctrine_total: int = 0
        self._latencies: deque = deque(maxlen=max_queries)
        self._cache_hits: int = 0
        self._cache_total: int = 0
        self._mode_counter: Counter = Counter()
        self._confidence_scores: deque = deque(maxlen=max_queries)
        self._coverage_counter: Counter = Counter()
        self._query_ids: set = set()
        self._audit_writer = AuditTrailWriter()
        logger.info("TelemetryCollector initialized for ENGINE_ID={}", ENGINE_ID)

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._query_ids.add(metrics.query_id)
        self._latencies.append(metrics.latency_ms)
        self._mode_counter[metrics.mode] += 1
        self._confidence_scores.append(metrics.confidence)
        self._cache_total += 1
        if metrics.cache_hit:
            self._cache_hits += 1
        self._doctrine_total += 1
        if metrics.doctrine_matched:
            self._doctrine_hits += 1
        self._coverage_counter[metrics.mode] += 1
        self._audit_writer.write(metrics)
        logger.debug("Recorded query: {}", metrics)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "error_type": error_type,
            "message": message,
            "timestamp": time.time(),
            "query_id": query_id,
            "engine_id": ENGINE_ID
        }
        self._errors.append(error_entry)
        logger.error("Error recorded: {}", error_entry)
        self._audit_writer.write_error(error_entry)

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
        p50 = statistics.median(latencies)
        p95 = latencies_sorted[int(0.95 * len(latencies_sorted))-1]
        p99 = latencies_sorted[int(0.99 * len(latencies_sorted))-1]
        min_latency = min(latencies_sorted)
        max_latency = max(latencies_sorted)
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
        if self._doctrine_total == 0:
            return 0.0
        hit_rate = self._doctrine_hits / self._doctrine_total
        logger.info("Doctrine hit rate: {}", hit_rate)
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        error_count = sum(1 for e in self._errors if e["timestamp"] >= window_start)
        query_count = sum(1 for q in self._queries if q.timestamp >= window_start)
        if query_count == 0:
            return 0.0
        error_rate = error_count / query_count
        logger.info("Error rate ({}h): {}", window_hours, error_rate)
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= one_hour_ago)
        logger.info("Queries last hour: {}", count)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        total = sum(self._coverage_counter.values())
        report = {}
        for mode, count in self._coverage_counter.items():
            report[mode] = {
                "count": count,
                "percent": (count / total * 100) if total else 0.0
            }
        logger.info("Coverage report: {}", report)
        return report

    def export_jsonl(self, path: Union[str, pathlib.Path]) -> int:
        p = pathlib.Path(path)
        count = 0
        with p.open("w", encoding="utf-8") as f:
            for q in self._queries:
                f.write(json.dumps(asdict(q)) + "\n")
                count += 1
            for e in self._errors:
                f.write(json.dumps(e) + "\n")
                count += 1
        logger.info("Exported {} records to {}", count, str(p))
        return count

class AuditTrailWriter:
    def __init__(self, audit_dir: Union[str, pathlib.Path] = "audit_trail"):
        self.audit_dir = pathlib.Path(audit_dir)
        self.audit_dir.mkdir(parents=True, exist_ok=True)
        logger.info("AuditTrailWriter initialized at {}", str(self.audit_dir))

    def _get_audit_path(self, query_id: str) -> pathlib.Path:
        hash_id = hashlib.sha256(query_id.encode()).hexdigest()
        filename = f"{hash_id}.jsonl"
        return self.audit_dir / filename

    def write(self, metrics: QueryMetrics):
        path = self._get_audit_path(metrics.query_id)
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(metrics)) + "\n")
        logger.debug("Audit trail written for query_id={}", metrics.query_id)

    def write_error(self, error_entry: Dict[str, Any]):
        query_id = error_entry.get("query_id", "unknown")
        path = self._get_audit_path(query_id)
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(error_entry) + "\n")
        logger.debug("Audit trail error written for query_id={}", query_id)

COLLECTOR = TelemetryCollector()