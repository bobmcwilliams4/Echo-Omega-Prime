import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any, Union
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "I03"

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
        self.queries: deque = deque(maxlen=max_queries)
        self.errors: deque = deque(maxlen=max_queries)
        self.audit_writer = AuditTrailWriter()
        self._doctrine_hits: int = 0
        self._doctrine_total: int = 0
        self._lock = None  # Placeholder for threading.Lock if needed

    def record_query(self, metrics: QueryMetrics):
        self.queries.append(metrics)
        self.audit_writer.write(metrics)
        if metrics.doctrine_matched is not None:
            self._doctrine_total += 1
            if metrics.doctrine_matched:
                self._doctrine_hits += 1
        if metrics.error:
            self.record_error('query_error', metrics.error, metrics.query_id)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "timestamp": time.time()
        }
        self.errors.append(error_entry)
        logger.error(f"Error recorded: {error_entry}")

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = [q.latency_ms for q in self.queries if q.latency_ms is not None]
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
        p50 = statistics.median(latencies_sorted)
        p95 = latencies_sorted[int(0.95 * len(latencies_sorted))-1]
        p99 = latencies_sorted[int(0.99 * len(latencies_sorted))-1]
        return {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_latency,
            "max": max_latency
        }

    def get_doctrine_hit_rate(self) -> float:
        if self._doctrine_total == 0:
            return 0.0
        return self._doctrine_hits / self._doctrine_total

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        error_count = sum(1 for e in self.errors if e["timestamp"] >= window_start)
        query_count = sum(1 for q in self.queries if q.timestamp >= window_start)
        if query_count == 0:
            return 0.0
        return error_count / query_count

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        return sum(1 for q in self.queries if q.timestamp >= one_hour_ago)

    def get_coverage_report(self) -> Dict[str, Any]:
        modes = Counter(q.mode for q in self.queries if q.mode)
        cache_hits = sum(1 for q in self.queries if q.cache_hit)
        cache_total = len(self.queries)
        confidence_values = [q.confidence for q in self.queries if q.confidence is not None]
        doctrine_hits = self._doctrine_hits
        doctrine_total = self._doctrine_total
        error_count = len(self.errors)
        coverage = {
            "mode_distribution": dict(modes),
            "cache_hit_rate": cache_hits / cache_total if cache_total else 0.0,
            "confidence_avg": statistics.mean(confidence_values) if confidence_values else None,
            "doctrine_hit_rate": doctrine_hits / doctrine_total if doctrine_total else 0.0,
            "error_count": error_count,
            "total_queries": cache_total
        }
        return coverage

    def export_jsonl(self, path: Union[str, pathlib.Path]) -> int:
        path = pathlib.Path(path)
        count = 0
        with path.open("w", encoding="utf-8") as f:
            for q in self.queries:
                f.write(json.dumps(asdict(q)) + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {path}")
        return count

class AuditTrailWriter:
    def __init__(self, audit_dir: Union[str, pathlib.Path] = "./audit_trail"):
        self.audit_dir = pathlib.Path(audit_dir)
        self.audit_dir.mkdir(parents=True, exist_ok=True)

    def write(self, metrics: QueryMetrics):
        filename = self._get_filename(metrics.query_id)
        record = asdict(metrics)
        record["audit_hash"] = self._hash_record(record)
        with open(filename, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
        logger.debug(f"Audit trail written for query_id={metrics.query_id}")

    def _get_filename(self, query_id: str) -> str:
        date_str = time.strftime("%Y%m%d")
        safe_query_id = hashlib.md5(query_id.encode()).hexdigest()
        return str(self.audit_dir / f"{ENGINE_ID}_{date_str}_{safe_query_id}.jsonl")

    def _hash_record(self, record: Dict[str, Any]) -> str:
        record_str = json.dumps(record, sort_keys=True)
        return hashlib.sha256(record_str.encode("utf-8")).hexdigest()

COLLECTOR = TelemetryCollector()