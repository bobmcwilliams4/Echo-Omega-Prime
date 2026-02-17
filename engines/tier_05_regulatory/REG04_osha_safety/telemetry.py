import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Any
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "REG04"

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
        self._queries: deque = deque(maxlen=10000)
        self._errors: deque = deque(maxlen=5000)
        self._doctrine_matches: deque = deque(maxlen=10000)
        self._latencies: deque = deque(maxlen=10000)
        self._cache_hits: deque = deque(maxlen=10000)
        self._query_modes: deque = deque(maxlen=10000)
        self._confidences: deque = deque(maxlen=10000)
        self._query_timestamps: deque = deque(maxlen=10000)
        self._coverage_counter: Counter = Counter()
        self._audit_writer = AuditTrailWriter()
        self._query_id_map = {}
        logger.info(f"TelemetryCollector initialized for engine_id={engine_id}")

    def record_query(self, metrics: QueryMetrics):
        logger.debug(f"Recording query: {metrics}")
        self._queries.append(metrics)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_matches.append(metrics.doctrine_matched)
        self._cache_hits.append(metrics.cache_hit)
        self._query_modes.append(metrics.mode)
        self._confidences.append(metrics.confidence)
        self._query_timestamps.append(metrics.timestamp)
        self._coverage_counter[metrics.mode] += 1
        self._query_id_map[metrics.query_id] = metrics
        self._audit_writer.write(metrics)
        if metrics.error:
            self.record_error(metrics.error, "Query error", metrics.query_id)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "engine_id": self.engine_id,
            "error_type": error_type,
            "message": message,
            "query_id": query_id
        }
        logger.error(f"Recording error: {error_entry}")
        self._errors.append(error_entry)
        self._audit_writer.write_error(error_entry)

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = list(self._latencies)
        if not latencies:
            logger.warning("No latencies recorded yet.")
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
        matches = list(self._doctrine_matches)
        if not matches:
            logger.warning("No doctrine matches recorded yet.")
            return 0.0
        hit_rate = sum(1 for m in matches if m) / len(matches)
        logger.debug(f"Doctrine hit rate: {hit_rate}")
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        queries_in_window = [q for q in self._queries if q.timestamp >= window_start]
        error_count = len(errors_in_window)
        query_count = len(queries_in_window)
        logger.debug(f"Errors in window: {error_count}, Queries in window: {query_count}")
        if query_count == 0:
            return 0.0
        error_rate = error_count / query_count
        logger.debug(f"Error rate (last {window_hours}h): {error_rate}")
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= one_hour_ago)
        logger.debug(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        total = sum(self._coverage_counter.values())
        report = {}
        for mode, count in self._coverage_counter.items():
            report[mode] = {
                "count": count,
                "percent": (count / total) * 100 if total else 0.0
            }
        logger.debug(f"Coverage report: {report}")
        return report

    def export_jsonl(self, path: str) -> int:
        path_obj = pathlib.Path(path)
        count = 0
        try:
            with path_obj.open("w", encoding="utf-8") as f:
                for q in self._queries:
                    f.write(json.dumps(asdict(q)) + "\n")
                    count += 1
            logger.info(f"Exported {count} queries to {path}")
        except Exception as e:
            logger.error(f"Failed to export queries: {e}")
        return count

class AuditTrailWriter:
    def __init__(self, base_path: Optional[str] = None):
        if base_path is None:
            self.base_path = pathlib.Path("./audit_trail")
        else:
            self.base_path = pathlib.Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"AuditTrailWriter initialized at {self.base_path}")

    def _get_query_file(self, query_id: str) -> pathlib.Path:
        h = hashlib.sha256(query_id.encode()).hexdigest()[:8]
        filename = f"{query_id}_{h}.jsonl"
        return self.base_path / filename

    def write(self, metrics: QueryMetrics):
        path = self._get_query_file(metrics.query_id)
        try:
            with path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(asdict(metrics)) + "\n")
            logger.debug(f"Wrote audit trail for query_id={metrics.query_id}")
        except Exception as e:
            logger.error(f"Failed to write audit trail for {metrics.query_id}: {e}")

    def write_error(self, error_entry: Dict[str, Any]):
        query_id = error_entry.get("query_id", "unknown")
        path = self._get_query_file(query_id)
        try:
            with path.open("a", encoding="utf-8") as f:
                f.write(json.dumps({"error": error_entry}) + "\n")
            logger.debug(f"Wrote error audit for query_id={query_id}")
        except Exception as e:
            logger.error(f"Failed to write error audit for {query_id}: {e}")

COLLECTOR = TelemetryCollector(engine_id=ENGINE_ID)