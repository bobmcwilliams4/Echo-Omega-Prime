import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional, Any
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "AUTO07"

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
        self._queries: deque[QueryMetrics] = deque(maxlen=maxlen)
        self._errors: deque[Dict[str, Any]] = deque(maxlen=maxlen)
        self._doctrine_hits: deque[bool] = deque(maxlen=maxlen)
        self._latencies: deque[float] = deque(maxlen=maxlen)
        self._query_ids: set[str] = set()
        self._mode_counter: Counter = Counter()
        self._cache_hits: deque[bool] = deque(maxlen=maxlen)
        self._confidence_scores: deque[float] = deque(maxlen=maxlen)
        self._coverage_by_mode: defaultdict[str, int] = defaultdict(int)
        self._coverage_by_doctrine: defaultdict[bool, int] = defaultdict(int)
        self._last_exported_index: int = 0

    def record_query(self, metrics: QueryMetrics):
        if metrics.query_id in self._query_ids:
            logger.warning(f"Duplicate query_id detected: {metrics.query_id}")
            return
        self._queries.append(metrics)
        self._query_ids.add(metrics.query_id)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._mode_counter[metrics.mode] += 1
        self._cache_hits.append(metrics.cache_hit)
        self._confidence_scores.append(metrics.confidence)
        self._coverage_by_mode[metrics.mode] += 1
        self._coverage_by_doctrine[metrics.doctrine_matched] += 1
        logger.debug(f"Recorded query: {metrics}")

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
        }
        self._errors.append(error_entry)
        logger.error(f"Error recorded: {error_entry}")

    def get_latency_stats(self) -> Dict[str, float]:
        if not self._latencies:
            return dict(avg=0, p50=0, p95=0, p99=0, min=0, max=0)
        latencies = list(self._latencies)
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = statistics.quantiles(latencies, n=100)[94] if len(latencies) >= 20 else max(latencies)
        p99 = statistics.quantiles(latencies, n=100)[98] if len(latencies) >= 100 else max(latencies)
        min_latency = min(latencies)
        max_latency = max(latencies)
        return {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_latency,
            "max": max_latency,
        }

    def get_doctrine_hit_rate(self) -> float:
        if not self._doctrine_hits:
            return 0.0
        hits = sum(1 for hit in self._doctrine_hits if hit)
        return hits / len(self._doctrine_hits)

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        queries_in_window = [q for q in self._queries if q.timestamp >= window_start]
        if not queries_in_window:
            return 0.0
        return len(errors_in_window) / len(queries_in_window)

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        return sum(1 for q in self._queries if q.timestamp >= one_hour_ago)

    def get_coverage_report(self) -> Dict[str, Any]:
        total = len(self._queries)
        doctrine_true = sum(1 for q in self._queries if q.doctrine_matched)
        doctrine_false = total - doctrine_true
        mode_counts = dict(self._mode_counter)
        cache_hits = sum(1 for hit in self._cache_hits if hit)
        cache_misses = len(self._cache_hits) - cache_hits
        avg_confidence = statistics.mean(self._confidence_scores) if self._confidence_scores else 0.0
        return {
            "total_queries": total,
            "doctrine_matched": doctrine_true,
            "doctrine_not_matched": doctrine_false,
            "mode_counts": mode_counts,
            "cache_hits": cache_hits,
            "cache_misses": cache_misses,
            "avg_confidence": avg_confidence,
        }

    def export_jsonl(self, path: str) -> int:
        export_path = pathlib.Path(path)
        export_path.parent.mkdir(parents=True, exist_ok=True)
        count = 0
        with export_path.open("a", encoding="utf-8") as f:
            for i, q in enumerate(list(self._queries)[self._last_exported_index:]):
                f.write(json.dumps(asdict(q)) + "\n")
                count += 1
            self._last_exported_index = len(self._queries)
        logger.info(f"Exported {count} queries to {path}")
        return count

class AuditTrailWriter:
    def __init__(self, audit_dir: str = "./audit_trail"):
        self.audit_dir = pathlib.Path(audit_dir)
        self.audit_dir.mkdir(parents=True, exist_ok=True)

    def write(self, query_metrics: QueryMetrics, extra: Optional[Dict[str, Any]] = None) -> pathlib.Path:
        record = asdict(query_metrics)
        if extra:
            record.update(extra)
        record["audit_timestamp"] = time.time()
        record_str = json.dumps(record, sort_keys=True)
        record_hash = hashlib.sha256(record_str.encode("utf-8")).hexdigest()
        filename = f"{query_metrics.query_id}_{record_hash[:8]}.jsonl"
        file_path = self.audit_dir / filename
        with file_path.open("a", encoding="utf-8") as f:
            f.write(record_str + "\n")
        logger.info(f"Audit trail written: {file_path}")
        return file_path

COLLECTOR = TelemetryCollector()
AUDIT_TRAIL_WRITER = AuditTrailWriter()