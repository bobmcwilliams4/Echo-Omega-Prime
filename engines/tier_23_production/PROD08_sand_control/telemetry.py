import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any, Tuple
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "PROD08"

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
        self._query_times: deque = deque(maxlen=max_queries)
        self._query_ids: set = set()
        self._coverage: Counter = Counter()
        self._audit_writer = AuditTrailWriter()
        logger.info("TelemetryCollector initialized for engine_id={}", ENGINE_ID)

    def record_query(self, metrics: QueryMetrics):
        if metrics.query_id in self._query_ids:
            logger.warning("Duplicate query_id detected: {}", metrics.query_id)
            return
        self._queries.append(metrics)
        self._query_ids.add(metrics.query_id)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._query_times.append(metrics.timestamp)
        self._coverage[(metrics.mode, metrics.cache_hit, metrics.doctrine_matched)] += 1
        self._audit_writer.write(metrics)
        logger.debug("Recorded query: {}", metrics.query_id)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "engine_id": ENGINE_ID,
            "error_type": error_type,
            "message": message,
            "query_id": query_id
        }
        self._errors.append(error_entry)
        logger.error("Error recorded: {} - {}", error_type, message)

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
        min_ = min(latencies)
        max_ = max(latencies)
        p50 = statistics.median(latencies)
        p95 = latencies_sorted[int(0.95 * len(latencies_sorted))-1]
        p99 = latencies_sorted[int(0.99 * len(latencies_sorted))-1]
        return {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_,
            "max": max_
        }

    def get_doctrine_hit_rate(self) -> float:
        hits = sum(1 for hit in self._doctrine_hits if hit)
        total = len(self._doctrine_hits)
        if total == 0:
            return 0.0
        return hits / total

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        cutoff = now - window_hours * 3600
        error_count = sum(1 for e in self._errors if e["timestamp"] >= cutoff)
        query_count = sum(1 for t in self._query_times if t >= cutoff)
        if query_count == 0:
            return 0.0
        return error_count / query_count

    def queries_last_hour(self) -> int:
        now = time.time()
        cutoff = now - 3600
        return sum(1 for t in self._query_times if t >= cutoff)

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {}
        total = sum(self._coverage.values())
        for key, count in self._coverage.items():
            mode, cache_hit, doctrine_matched = key
            label = f"{mode}|cache:{cache_hit}|doctrine:{doctrine_matched}"
            report[label] = {
                "count": count,
                "percent": (count / total * 100) if total else 0.0
            }
        return report

    def export_jsonl(self, path: str) -> int:
        p = pathlib.Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        count = 0
        with p.open("w", encoding="utf-8") as f:
            for qm in self._queries:
                f.write(json.dumps(asdict(qm)) + "\n")
                count += 1
        logger.info("Exported {} queries to {}", count, path)
        return count

class AuditTrailWriter:
    def __init__(self, base_path: str = "./audit_trail"):
        self.base_path = pathlib.Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        logger.info("AuditTrailWriter initialized at {}", self.base_path)

    def write(self, metrics: QueryMetrics):
        audit_path = self._get_audit_path(metrics.query_id)
        entry = {
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
        with audit_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        logger.debug("Audit trail written for query_id={}", metrics.query_id)

    def _get_audit_path(self, query_id: str) -> pathlib.Path:
        hash_digest = hashlib.sha256(query_id.encode()).hexdigest()
        subdir = self.base_path / hash_digest[:2]
        subdir.mkdir(parents=True, exist_ok=True)
        filename = f"{hash_digest}.jsonl"
        return subdir / filename

COLLECTOR = TelemetryCollector()