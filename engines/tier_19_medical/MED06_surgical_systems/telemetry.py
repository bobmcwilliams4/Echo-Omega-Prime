import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any, Union
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "MED06"

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
        self._query_ids: set = set()
        self._audit_writer = AuditTrailWriter()
        self._coverage_counter = Counter()
        self._mode_counter = Counter()
        self._confidence_values = []
        self._cache_hits = deque(maxlen=max_queries)
        logger.info("TelemetryCollector initialized with max_queries={}", max_queries)

    def record_query(self, metrics: QueryMetrics):
        logger.debug("Recording query: {}", metrics)
        self._queries.append(metrics)
        self._query_ids.add(metrics.query_id)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._cache_hits.append(metrics.cache_hit)
        self._mode_counter[metrics.mode] += 1
        self._coverage_counter[metrics.doctrine_matched] += 1
        self._confidence_values.append(metrics.confidence)
        self._audit_writer.write(metrics)
        if metrics.error:
            self.record_error("query_error", metrics.error, metrics.query_id)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "timestamp": time.time()
        }
        logger.error("Recording error: {}", error_entry)
        self._errors.append(error_entry)
        self._audit_writer.write_error(error_entry)

    def get_latency_stats(self) -> Dict[str, Union[float, None]]:
        latencies = list(self._latencies)
        if not latencies:
            logger.warning("No latency data available for stats.")
            return dict(avg=None, p50=None, p95=None, p99=None, min=None, max=None)
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = latencies_sorted[int(0.95 * len(latencies_sorted)) - 1]
        p99 = latencies_sorted[int(0.99 * len(latencies_sorted)) - 1]
        min_latency = min(latencies)
        max_latency = max(latencies)
        stats = dict(
            avg=avg,
            p50=p50,
            p95=p95,
            p99=p99,
            min=min_latency,
            max=max_latency
        )
        logger.info("Latency stats: {}", stats)
        return stats

    def get_doctrine_hit_rate(self) -> float:
        hits = sum(self._doctrine_hits)
        total = len(self._doctrine_hits)
        hit_rate = hits / total if total > 0 else 0.0
        logger.info("Doctrine hit rate: {:.2f}", hit_rate)
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        queries_in_window = [q for q in self._queries if q.timestamp >= window_start]
        error_count = len(errors_in_window)
        query_count = len(queries_in_window)
        error_rate = error_count / query_count if query_count > 0 else 0.0
        logger.info("Error rate in last {:.2f} hours: {:.2f}", window_hours, error_rate)
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= one_hour_ago)
        logger.info("Queries in last hour: {}", count)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        total_queries = len(self._queries)
        doctrine_matched = sum(q.doctrine_matched for q in self._queries)
        cache_hits = sum(q.cache_hit for q in self._queries)
        avg_confidence = statistics.mean(self._confidence_values) if self._confidence_values else None
        mode_distribution = dict(self._mode_counter)
        coverage_report = {
            "total_queries": total_queries,
            "doctrine_matched": doctrine_matched,
            "doctrine_match_rate": doctrine_matched / total_queries if total_queries > 0 else 0.0,
            "cache_hits": cache_hits,
            "cache_hit_rate": cache_hits / total_queries if total_queries > 0 else 0.0,
            "avg_confidence": avg_confidence,
            "mode_distribution": mode_distribution
        }
        logger.info("Coverage report: {}", coverage_report)
        return coverage_report

    def export_jsonl(self, path: Union[str, pathlib.Path]) -> int:
        path = pathlib.Path(path)
        logger.info("Exporting queries to JSONL at {}", path)
        count = 0
        with path.open("w", encoding="utf-8") as f:
            for q in self._queries:
                f.write(json.dumps(asdict(q)) + "\n")
                count += 1
        logger.info("Exported {} queries to {}", count, path)
        return count

class AuditTrailWriter:
    def __init__(self, base_dir: Union[str, pathlib.Path] = "audit_trails"):
        self.base_dir = pathlib.Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        logger.info("AuditTrailWriter initialized at {}", self.base_dir)

    def _get_query_file(self, query_id: str) -> pathlib.Path:
        hash_id = hashlib.sha256(query_id.encode()).hexdigest()
        filename = f"{hash_id}.jsonl"
        return self.base_dir / filename

    def write(self, metrics: QueryMetrics):
        file_path = self._get_query_file(metrics.query_id)
        logger.debug("Writing audit trail for query {} to {}", metrics.query_id, file_path)
        with file_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(metrics)) + "\n")

    def write_error(self, error_entry: Dict[str, Any]):
        query_id = error_entry.get("query_id", "unknown")
        file_path = self._get_query_file(query_id)
        logger.debug("Writing error audit trail for query {} to {}", query_id, file_path)
        with file_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(error_entry) + "\n")

COLLECTOR = TelemetryCollector()