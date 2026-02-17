import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any, Union
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "BLD06"

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
        self.queries: deque[QueryMetrics] = deque(maxlen=maxlen)
        self.errors: deque[Dict[str, Any]] = deque(maxlen=maxlen)
        self.audit_writer = AuditTrailWriter()
        self._doctrine_total = 0
        self._doctrine_hits = 0
        self._latencies = deque(maxlen=maxlen)
        self._cache_hits = 0
        self._cache_total = 0
        self._modes = Counter()
        self._confidences = deque(maxlen=maxlen)
        self._error_types = Counter()
        self._query_timestamps = deque(maxlen=maxlen)
        self._coverage_modes = defaultdict(int)
        self._coverage_errors = defaultdict(int)
        self._coverage_cache = defaultdict(int)
        self._coverage_doctrine = defaultdict(int)

    def record_query(self, metrics: QueryMetrics):
        self.queries.append(metrics)
        self._latencies.append(metrics.latency_ms)
        self._confidences.append(metrics.confidence)
        self._modes[metrics.mode] += 1
        self._query_timestamps.append(metrics.timestamp)
        self._coverage_modes[metrics.mode] += 1
        if metrics.cache_hit:
            self._cache_hits += 1
            self._coverage_cache[metrics.mode] += 1
        self._cache_total += 1
        if metrics.doctrine_matched:
            self._doctrine_hits += 1
            self._coverage_doctrine[metrics.mode] += 1
        self._doctrine_total += 1
        if metrics.error:
            self._coverage_errors[metrics.error] += 1
        self.audit_writer.write(metrics)
        logger.debug(f"Recorded query: {metrics}")

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "timestamp": time.time()
        }
        self.errors.append(error_entry)
        self._error_types[error_type] += 1
        self._coverage_errors[error_type] += 1
        logger.error(f"Error recorded: {error_entry}")

    def get_latency_stats(self) -> Dict[str, Union[float, None]]:
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
        total_queries = 0
        error_queries = 0
        for q in self.queries:
            if q.timestamp >= window_start:
                total_queries += 1
                if q.error:
                    error_queries += 1
        if total_queries == 0:
            return 0.0
        return error_queries / total_queries

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        return sum(1 for t in self._query_timestamps if t >= one_hour_ago)

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {
            "modes": dict(self._coverage_modes),
            "cache_hits_by_mode": dict(self._coverage_cache),
            "doctrine_hits_by_mode": dict(self._coverage_doctrine),
            "errors_by_type": dict(self._coverage_errors),
            "total_queries": len(self.queries),
            "total_errors": sum(self._coverage_errors.values()),
            "cache_hit_rate": self._cache_hits / self._cache_total if self._cache_total else 0.0,
            "doctrine_hit_rate": self.get_doctrine_hit_rate(),
            "latency_stats": self.get_latency_stats(),
            "confidence_stats": self._get_confidence_stats()
        }
        return report

    def _get_confidence_stats(self) -> Dict[str, Union[float, None]]:
        confidences = list(self._confidences)
        if not confidences:
            return {"avg": None, "min": None, "max": None}
        avg = statistics.mean(confidences)
        min_conf = min(confidences)
        max_conf = max(confidences)
        return {"avg": avg, "min": min_conf, "max": max_conf}

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
    def __init__(self, base_dir: Union[str, pathlib.Path] = "./audit_trail"):
        self.base_dir = pathlib.Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def write(self, metrics: QueryMetrics):
        # Use a hash of query_id for filename to avoid issues with special chars
        query_hash = hashlib.sha256(metrics.query_id.encode("utf-8")).hexdigest()
        filename = f"{metrics.engine_id}_{query_hash}.jsonl"
        file_path = self.base_dir / filename
        entry = asdict(metrics)
        entry["audit_timestamp"] = time.time()
        with file_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        logger.debug(f"Audit trail written for query {metrics.query_id} at {file_path}")

COLLECTOR = TelemetryCollector()