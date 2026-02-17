import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any
from collections import deque, defaultdict
from loguru import logger


ENGINE_ID = "CHEM04"


@dataclass
class QueryMetrics:
    query_id: str
    engine_id: str
    timestamp: float  # epoch seconds
    latency_ms: float
    cache_hit: bool
    doctrine_matched: bool
    mode: str
    confidence: Optional[float] = None
    error: Optional[str] = None


class TelemetryCollector:
    def __init__(self):
        # Store all queries in a deque with maxlen to prevent memory explosion
        self._queries: deque[QueryMetrics] = deque(maxlen=100_000)
        # Store errors as list of dicts with timestamp for time window queries
        self._errors: deque[Dict[str, Any]] = deque(maxlen=10_000)
        # For coverage report: count of queries per mode and doctrine matched
        self._mode_counter: defaultdict[str, int] = defaultdict(int)
        self._doctrine_counter: int = 0
        self._total_queries: int = 0
        # For cache hit rate
        self._cache_hit_counter: int = 0
        # For latency stats cache
        self._latencies: List[float] = []
        # Locking is omitted for simplicity, assume single-threaded or external sync

    def record_query(self, metrics: QueryMetrics):
        if metrics.engine_id != ENGINE_ID:
            logger.warning(f"Received metrics for unknown engine_id: {metrics.engine_id}")
            return
        self._queries.append(metrics)
        self._total_queries += 1
        if metrics.cache_hit:
            self._cache_hit_counter += 1
        if metrics.doctrine_matched:
            self._doctrine_counter += 1
        self._mode_counter[metrics.mode] += 1
        self._latencies.append(metrics.latency_ms)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_record = {
            "timestamp": time.time(),
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "engine_id": ENGINE_ID,
        }
        self._errors.append(error_record)
        logger.error(f"Error recorded: {error_record}")

    def get_latency_stats(self) -> Dict[str, Optional[float]]:
        if not self._latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        lat_sorted = sorted(self._latencies)
        avg = statistics.mean(lat_sorted)
        p50 = lat_sorted[int(len(lat_sorted)*0.50)]
        p95 = lat_sorted[int(len(lat_sorted)*0.95)-1]
        p99 = lat_sorted[int(len(lat_sorted)*0.99)-1]
        min_lat = lat_sorted[0]
        max_lat = lat_sorted[-1]
        return {"avg": avg, "p50": p50, "p95": p95, "p99": p99, "min": min_lat, "max": max_lat}

    def get_doctrine_hit_rate(self) -> float:
        if self._total_queries == 0:
            return 0.0
        return self._doctrine_counter / self._total_queries

    def get_error_rate(self, window_hours: int) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        queries_in_window = [q for q in self._queries if q.timestamp >= window_start]
        if not queries_in_window:
            return 0.0
        return len(errors_in_window) / len(queries_in_window)

    def queries_last_hour(self) -> int:
        now = time.time()
        hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= hour_ago)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        # Coverage report includes mode distribution, doctrine hit rate, cache hit rate
        mode_distribution = {}
        total_modes = sum(self._mode_counter.values())
        for mode, count in self._mode_counter.items():
            mode_distribution[mode] = count / total_modes if total_modes > 0 else 0.0
        cache_hit_rate = self._cache_hit_counter / self._total_queries if self._total_queries > 0 else 0.0
        doctrine_hit_rate = self.get_doctrine_hit_rate()
        latency_stats = self.get_latency_stats()
        return {
            "total_queries": self._total_queries,
            "mode_distribution": mode_distribution,
            "doctrine_hit_rate": doctrine_hit_rate,
            "cache_hit_rate": cache_hit_rate,
            "latency_stats": latency_stats,
            "error_count": len(self._errors),
        }

    def export_jsonl(self, path: pathlib.Path) -> int:
        # Export all queries to a JSONL file, one query per line
        count = 0
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("w", encoding="utf-8") as f:
                for q in self._queries:
                    record = asdict(q)
                    f.write(json.dumps(record) + "\n")
                    count += 1
            logger.info(f"Exported {count} query metrics to {path}")
        except Exception as e:
            logger.error(f"Failed to export telemetry to {path}: {e}")
        return count


class AuditTrailWriter:
    def __init__(self, directory: pathlib.Path):
        self.directory = directory
        self.directory.mkdir(parents=True, exist_ok=True)

    def write(self, query_metrics: QueryMetrics):
        # Write a JSONL file per query, filename is hash of query_id + timestamp
        try:
            base_str = f"{query_metrics.query_id}_{query_metrics.timestamp}"
            filename_hash = hashlib.sha256(base_str.encode("utf-8")).hexdigest()
            filename = f"{filename_hash}.jsonl"
            path = self.directory / filename
            with path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(asdict(query_metrics)) + "\n")
            logger.debug(f"Audit trail written for query_id={query_metrics.query_id} at {path}")
        except Exception as e:
            logger.error(f"Failed to write audit trail for query_id={query_metrics.query_id}: {e}")


COLLECTOR = TelemetryCollector()