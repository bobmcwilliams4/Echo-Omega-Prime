import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "I07"

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
    def __init__(self, engine_id: str):
        self.engine_id = engine_id
        self._queries: deque = deque()
        self._errors: deque = deque()
        self._doctrine_hits: deque = deque()
        self._audit_writer = AuditTrailWriter()
        self._query_id_set = set()
        self._metrics_by_query_id = {}
        self._error_counter = Counter()
        self._lock = None  # Placeholder for threading.Lock if needed

    def record_query(self, metrics: QueryMetrics):
        if metrics.query_id in self._query_id_set:
            logger.warning(f"Duplicate query_id detected: {metrics.query_id}")
            return
        self._queries.append(metrics)
        self._query_id_set.add(metrics.query_id)
        self._metrics_by_query_id[metrics.query_id] = metrics
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._audit_writer.write(metrics)
        logger.info(f"Recorded query: {metrics.query_id}")

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "engine_id": self.engine_id,
            "error_type": error_type,
            "message": message,
            "query_id": query_id
        }
        self._errors.append(error_entry)
        self._error_counter[error_type] += 1
        logger.error(f"Error recorded: {error_type} - {message} (query_id={query_id})")

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = [q.latency_ms for q in self._queries if q.latency_ms is not None]
        if not latencies:
            return {
                "avg": None,
                "p50": None,
                "p95": None,
                "p99": None,
                "min": None,
                "max": None
            }
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        lat_sorted = sorted(latencies)
        p95 = lat_sorted[int(0.95 * len(lat_sorted)) - 1]
        p99 = lat_sorted[int(0.99 * len(lat_sorted)) - 1]
        min_lat = min(latencies)
        max_lat = max(latencies)
        return {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_lat,
            "max": max_lat
        }

    def get_doctrine_hit_rate(self) -> float:
        total = len(self._doctrine_hits)
        if total == 0:
            return 0.0
        hits = sum(1 for hit in self._doctrine_hits if hit)
        return hits / total

    def get_error_rate(self, window_hours: float) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        queries_in_window = [q for q in self._queries if q.timestamp >= window_start]
        num_queries = len(queries_in_window)
        num_errors = len(errors_in_window)
        if num_queries == 0:
            return 0.0
        return num_errors / num_queries

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        return sum(1 for q in self._queries if q.timestamp >= one_hour_ago)

    def get_coverage_report(self) -> Dict[str, Any]:
        modes = Counter()
        cache_hits = Counter()
        doctrine_matches = Counter()
        confidences = []
        errors = Counter()
        for q in self._queries:
            modes[q.mode] += 1
            cache_hits[q.cache_hit] += 1
            doctrine_matches[q.doctrine_matched] += 1
            confidences.append(q.confidence)
            if q.error:
                errors[q.error] += 1
        total = len(self._queries)
        report = {
            "total_queries": total,
            "mode_distribution": dict(modes),
            "cache_hit_distribution": dict(cache_hits),
            "doctrine_match_distribution": dict(doctrine_matches),
            "confidence_stats": {
                "avg": statistics.mean(confidences) if confidences else None,
                "min": min(confidences) if confidences else None,
                "max": max(confidences) if confidences else None,
                "p50": statistics.median(confidences) if confidences else None
            },
            "error_distribution": dict(errors)
        }
        return report

    def export_jsonl(self, path: str) -> int:
        p = pathlib.Path(path)
        count = 0
        with p.open("w", encoding="utf-8") as f:
            for q in self._queries:
                f.write(json.dumps(dataclasses.asdict(q)) + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {path}")
        return count

class AuditTrailWriter:
    def __init__(self, audit_dir: str = "./audit_trail"):
        self.audit_dir = pathlib.Path(audit_dir)
        self.audit_dir.mkdir(parents=True, exist_ok=True)

    def _get_audit_path(self, query_id: str) -> pathlib.Path:
        hash_id = hashlib.sha256(query_id.encode("utf-8")).hexdigest()
        file_name = f"{hash_id}.jsonl"
        return self.audit_dir / file_name

    def write(self, metrics: QueryMetrics):
        path = self._get_audit_path(metrics.query_id)
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(dataclasses.asdict(metrics)) + "\n")
        logger.debug(f"Audit trail written for query_id: {metrics.query_id}")

COLLECTOR = TelemetryCollector(engine_id=ENGINE_ID)