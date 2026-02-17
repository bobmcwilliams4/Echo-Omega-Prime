import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict, field
from typing import Optional, List, Dict, Any, Deque
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "I02"

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
        self._queries: Deque[QueryMetrics] = deque(maxlen=maxlen)
        self._errors: Deque[Dict[str, Any]] = deque(maxlen=maxlen)
        self._doctrine_hits: Deque[bool] = deque(maxlen=maxlen)
        self._latencies: Deque[float] = deque(maxlen=maxlen)
        self._cache_hits: Deque[bool] = deque(maxlen=maxlen)
        self._modes: Deque[str] = deque(maxlen=maxlen)
        self._confidences: Deque[float] = deque(maxlen=maxlen)
        self._query_id_map: Dict[str, QueryMetrics] = {}
        self._audit_writer = AuditTrailWriter()
        self._error_counter = Counter()
        self._query_timestamps: Deque[float] = deque(maxlen=maxlen)
        self._doctrine_counter = Counter()
        self._lock = None  # Placeholder for threading.Lock if needed

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._query_id_map[metrics.query_id] = metrics
        self._latencies.append(metrics.latency_ms)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._cache_hits.append(metrics.cache_hit)
        self._modes.append(metrics.mode)
        self._confidences.append(metrics.confidence)
        self._query_timestamps.append(metrics.timestamp)
        self._doctrine_counter['hit' if metrics.doctrine_matched else 'miss'] += 1
        if metrics.error:
            self.record_error(metrics.error, "Query error", metrics.query_id)
        self._audit_writer.write(metrics)
        logger.debug(f"Recorded query: {metrics}")

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "engine_id": ENGINE_ID
        }
        self._errors.append(error_entry)
        self._error_counter[error_type] += 1
        logger.error(f"Error recorded: {error_entry}")

    def get_latency_stats(self) -> dict:
        latencies = list(self._latencies)
        if not latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        latencies.sort()
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = latencies[int(0.95 * len(latencies)) - 1]
        p99 = latencies[int(0.99 * len(latencies)) - 1]
        min_latency = latencies[0]
        max_latency = latencies[-1]
        stats = {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_latency,
            "max": max_latency
        }
        logger.debug(f"Latency stats: {stats}")
        return stats

    def get_doctrine_hit_rate(self) -> float:
        total = len(self._doctrine_hits)
        if total == 0:
            return 0.0
        hits = sum(self._doctrine_hits)
        hit_rate = hits / total
        logger.debug(f"Doctrine hit rate: {hit_rate} ({hits}/{total})")
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        queries_in_window = [t for t in self._query_timestamps if t >= window_start]
        error_rate = (len(errors_in_window) / len(queries_in_window)) if queries_in_window else 0.0
        logger.debug(f"Error rate in last {window_hours}h: {error_rate} ({len(errors_in_window)}/{len(queries_in_window)})")
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for t in self._query_timestamps if t >= one_hour_ago)
        logger.debug(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> dict:
        mode_counter = Counter(self._modes)
        doctrine_counter = self._doctrine_counter.copy()
        cache_hit_count = sum(self._cache_hits)
        total = len(self._queries)
        coverage = {
            "total_queries": total,
            "mode_distribution": dict(mode_counter),
            "doctrine_hits": doctrine_counter.get('hit', 0),
            "doctrine_misses": doctrine_counter.get('miss', 0),
            "cache_hits": cache_hit_count,
            "cache_misses": total - cache_hit_count,
            "avg_confidence": statistics.mean(self._confidences) if self._confidences else None
        }
        logger.debug(f"Coverage report: {coverage}")
        return coverage

    def export_jsonl(self, path: str) -> int:
        out_path = pathlib.Path(path)
        count = 0
        with out_path.open("w", encoding="utf-8") as f:
            for qm in self._queries:
                f.write(json.dumps(asdict(qm)) + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {out_path}")
        return count

class AuditTrailWriter:
    def __init__(self, directory: Optional[str] = None):
        if directory is None:
            directory = "./audit_trail"
        self.directory = pathlib.Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)

    def _get_audit_path(self, query_id: str) -> pathlib.Path:
        # Use hash to avoid filesystem issues with long IDs
        hash_id = hashlib.sha256(query_id.encode()).hexdigest()
        filename = f"{hash_id}.jsonl"
        return self.directory / filename

    def write(self, metrics: QueryMetrics):
        path = self._get_audit_path(metrics.query_id)
        data = asdict(metrics)
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(data) + "\n")
        logger.debug(f"Audit trail written for query_id={metrics.query_id} at {path}")

COLLECTOR = TelemetryCollector()