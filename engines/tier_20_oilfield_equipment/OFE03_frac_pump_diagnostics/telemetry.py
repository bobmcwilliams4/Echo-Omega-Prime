import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "OFE03"

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
        self._queries: deque = deque(maxlen=maxlen)
        self._errors: deque = deque(maxlen=maxlen)
        self._doctrine_hits: deque = deque(maxlen=maxlen)
        self._latencies: deque = deque(maxlen=maxlen)
        self._query_ids: set = set()
        self._audit_writer = AuditTrailWriter()
        self._coverage_counter: Counter = Counter()
        self._cache_hits: deque = deque(maxlen=maxlen)
        self._modes: deque = deque(maxlen=maxlen)
        self._confidence_scores: deque = deque(maxlen=maxlen)

    def record_query(self, metrics: QueryMetrics):
        if metrics.query_id in self._query_ids:
            logger.warning(f"Duplicate query_id detected: {metrics.query_id}")
            return
        self._queries.append(metrics)
        self._query_ids.add(metrics.query_id)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._cache_hits.append(metrics.cache_hit)
        self._modes.append(metrics.mode)
        self._confidence_scores.append(metrics.confidence)
        self._coverage_counter[metrics.mode] += 1
        self._audit_writer.write(metrics)
        logger.debug(f"Recorded query: {metrics}")

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_record = {
            "error_type": error_type,
            "message": message,
            "timestamp": time.time(),
            "query_id": query_id,
            "engine_id": ENGINE_ID
        }
        self._errors.append(error_record)
        logger.error(f"Error recorded: {error_record}")

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
        p95 = latencies_sorted[int(0.95 * len(latencies_sorted)) - 1]
        p99 = latencies_sorted[int(0.99 * len(latencies_sorted)) - 1]
        min_latency = min(latencies)
        max_latency = max(latencies)
        return {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_latency,
            "max": max_latency
        }

    def get_doctrine_hit_rate(self) -> float:
        hits = sum(1 for hit in self._doctrine_hits if hit)
        total = len(self._doctrine_hits)
        if total == 0:
            return 0.0
        return hits / total

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        error_count = sum(1 for e in self._errors if e["timestamp"] >= window_start)
        query_count = sum(1 for q in self._queries if q.timestamp >= window_start)
        if query_count == 0:
            return 0.0
        return error_count / query_count

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        return sum(1 for q in self._queries if q.timestamp >= one_hour_ago)

    def get_coverage_report(self) -> Dict[str, Any]:
        total_queries = len(self._queries)
        doctrine_hits = sum(1 for hit in self._doctrine_hits if hit)
        cache_hits = sum(1 for hit in self._cache_hits if hit)
        modes = Counter(self._modes)
        confidences = list(self._confidence_scores)
        avg_confidence = statistics.mean(confidences) if confidences else None
        report = {
            "total_queries": total_queries,
            "doctrine_hits": doctrine_hits,
            "doctrine_hit_rate": self.get_doctrine_hit_rate(),
            "cache_hits": cache_hits,
            "cache_hit_rate": cache_hits / total_queries if total_queries else 0.0,
            "mode_distribution": dict(modes),
            "avg_confidence": avg_confidence,
            "coverage_by_mode": dict(self._coverage_counter)
        }
        return report

    def export_jsonl(self, path: str) -> int:
        p = pathlib.Path(path)
        count = 0
        with p.open("w") as f:
            for q in self._queries:
                f.write(json.dumps(dataclasses.asdict(q)) + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {path}")
        return count

class AuditTrailWriter:
    def __init__(self, base_path: str = "./audit_trail"):
        self.base_path = pathlib.Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

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
        filename = self._get_filename(metrics.query_id)
        with open(filename, "a") as f:
            f.write(json.dumps(audit_record) + "\n")
        logger.debug(f"Wrote audit trail for query_id={metrics.query_id} to {filename}")

    def _get_filename(self, query_id: str) -> str:
        hash_digest = hashlib.sha256(query_id.encode()).hexdigest()
        subdir = self.base_path / hash_digest[:2]
        subdir.mkdir(exist_ok=True)
        filename = subdir / f"{hash_digest}.jsonl"
        return str(filename)

COLLECTOR = TelemetryCollector()