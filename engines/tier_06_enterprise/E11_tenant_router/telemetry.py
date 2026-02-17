import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Tuple
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "E11"

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
        self._cache_hits: deque = deque(maxlen=max_queries)
        self._query_ids: set = set()
        self._audit_writer = AuditTrailWriter()
        self._metrics_by_query: Dict[str, QueryMetrics] = {}
        self._error_counter: Counter = Counter()
        self._latency_list: List[float] = []
        self._coverage_modes: Counter = Counter()
        self._coverage_doctrine: Counter = Counter()
        self._coverage_cache: Counter = Counter()
        self._coverage_errors: Counter = Counter()
        self._coverage_confidence: List[float] = []
        self._coverage_total: int = 0

    def record_query(self, metrics: QueryMetrics):
        if metrics.query_id in self._query_ids:
            logger.warning(f"Duplicate query_id detected: {metrics.query_id}")
            return
        self._query_ids.add(metrics.query_id)
        self._queries.append(metrics)
        self._metrics_by_query[metrics.query_id] = metrics
        self._latency_list.append(metrics.latency_ms)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._cache_hits.append(metrics.cache_hit)
        self._coverage_modes[metrics.mode] += 1
        self._coverage_doctrine[metrics.doctrine_matched] += 1
        self._coverage_cache[metrics.cache_hit] += 1
        self._coverage_confidence.append(metrics.confidence)
        self._coverage_total += 1
        if metrics.error:
            self.record_error("query_error", metrics.error, metrics.query_id)
        self._audit_writer.write(metrics)
        logger.info(f"Recorded query: {metrics.query_id}")

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "timestamp": time.time(),
            "engine_id": ENGINE_ID
        }
        self._errors.append(error_entry)
        self._error_counter[error_type] += 1
        self._coverage_errors[error_type] += 1
        logger.error(f"Error recorded: {error_type} | {message} | query_id={query_id}")

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = [m.latency_ms for m in self._queries if m.latency_ms is not None]
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
        avg = statistics.mean(latencies_sorted)
        min_latency = latencies_sorted[0]
        max_latency = latencies_sorted[-1]
        p50 = statistics.median(latencies_sorted)
        p95 = latencies_sorted[int(0.95 * len(latencies_sorted)) - 1]
        p99 = latencies_sorted[int(0.99 * len(latencies_sorted)) - 1]
        return {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_latency,
            "max": max_latency
        }

    def get_doctrine_hit_rate(self) -> float:
        total = len(self._doctrine_hits)
        if total == 0:
            return 0.0
        hits = sum(1 for hit in self._doctrine_hits if hit)
        return hits / total

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        error_count = sum(1 for e in self._errors if e["timestamp"] >= window_start)
        query_count = sum(1 for m in self._queries if m.timestamp >= window_start)
        if query_count == 0:
            return 0.0
        return error_count / query_count

    def queries_last_hour(self) -> int:
        now = time.time()
        window_start = now - 3600
        return sum(1 for m in self._queries if m.timestamp >= window_start)

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {
            "total_queries": self._coverage_total,
            "mode_distribution": dict(self._coverage_modes),
            "doctrine_hit_rate": self.get_doctrine_hit_rate(),
            "cache_hit_rate": self._get_cache_hit_rate(),
            "error_distribution": dict(self._coverage_errors),
            "confidence_avg": statistics.mean(self._coverage_confidence) if self._coverage_confidence else None,
            "confidence_min": min(self._coverage_confidence) if self._coverage_confidence else None,
            "confidence_max": max(self._coverage_confidence) if self._coverage_confidence else None,
        }
        return report

    def _get_cache_hit_rate(self) -> float:
        total = len(self._cache_hits)
        if total == 0:
            return 0.0
        hits = sum(1 for hit in self._cache_hits if hit)
        return hits / total

    def export_jsonl(self, path: str) -> int:
        p = pathlib.Path(path)
        count = 0
        with p.open("w", encoding="utf-8") as f:
            for m in self._queries:
                d = dataclasses.asdict(m)
                f.write(json.dumps(d) + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {path}")
        return count

class AuditTrailWriter:
    def __init__(self, audit_dir: Optional[str] = None):
        self.audit_dir = audit_dir or "./audit_trail"
        self._ensure_dir()

    def _ensure_dir(self):
        p = pathlib.Path(self.audit_dir)
        if not p.exists():
            p.mkdir(parents=True, exist_ok=True)

    def write(self, metrics: QueryMetrics):
        filename = self._get_audit_filename(metrics)
        p = pathlib.Path(self.audit_dir) / filename
        audit_record = self._build_audit_record(metrics)
        with p.open("a", encoding="utf-8") as f:
            f.write(json.dumps(audit_record) + "\n")
        logger.debug(f"Wrote audit trail for query_id={metrics.query_id}")

    def _get_audit_filename(self, metrics: QueryMetrics) -> str:
        date_str = time.strftime("%Y%m%d", time.localtime(metrics.timestamp))
        return f"audit_{ENGINE_ID}_{date_str}.jsonl"

    def _build_audit_record(self, metrics: QueryMetrics) -> Dict[str, Any]:
        record = dataclasses.asdict(metrics)
        record["audit_hash"] = self._hash_query(record)
        record["audit_timestamp"] = time.time()
        return record

    def _hash_query(self, record: Dict[str, Any]) -> str:
        s = json.dumps(record, sort_keys=True)
        return hashlib.sha256(s.encode("utf-8")).hexdigest()

COLLECTOR = TelemetryCollector()