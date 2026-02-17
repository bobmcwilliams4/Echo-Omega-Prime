import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any
from collections import deque, defaultdict
from loguru import logger


ENGINE_ID = "DRL09"


@dataclass
class QueryMetrics:
    query_id: str
    engine_id: str
    timestamp: float
    latency_ms: float
    cache_hit: bool
    doctrine_matched: bool
    mode: Optional[str]
    confidence: Optional[float]
    error: Optional[str]


class TelemetryCollector:
    def __init__(self):
        # Store all queries in a deque for time-based queries (last hour)
        self._queries: deque[QueryMetrics] = deque()
        # Store errors keyed by error_type for error rate calculations
        self._errors: deque[Dict[str, Any]] = deque()
        # For coverage report: counts of doctrine matched vs total
        self._doctrine_hits = 0
        self._total_queries = 0
        # Latencies for stats
        self._latencies: List[float] = []
        # Cache hits count
        self._cache_hits = 0
        # Mode counts for coverage report
        self._mode_counts: Dict[str, int] = defaultdict(int)
        # Confidence values for coverage report
        self._confidences: List[float] = []
        # Lock for thread safety (if needed in future)
        # from threading import Lock
        # self._lock = Lock()

    def record_query(self, metrics: QueryMetrics):
        now = time.time()
        # Append query metrics
        self._queries.append(metrics)
        self._total_queries += 1
        self._latencies.append(metrics.latency_ms)
        if metrics.cache_hit:
            self._cache_hits += 1
        if metrics.doctrine_matched:
            self._doctrine_hits += 1
        if metrics.mode:
            self._mode_counts[metrics.mode] += 1
        if metrics.confidence is not None:
            self._confidences.append(metrics.confidence)
        # Clean old queries beyond 1 hour for memory efficiency
        cutoff = now - 3600
        while self._queries and self._queries[0].timestamp < cutoff:
            old = self._queries.popleft()
            self._total_queries -= 1
            self._latencies.remove(old.latency_ms)
            if old.cache_hit:
                self._cache_hits -= 1
            if old.doctrine_matched:
                self._doctrine_hits -= 1
            if old.mode:
                self._mode_counts[old.mode] -= 1
                if self._mode_counts[old.mode] <= 0:
                    del self._mode_counts[old.mode]
            if old.confidence is not None:
                try:
                    self._confidences.remove(old.confidence)
                except ValueError:
                    pass

    def record_error(self, error_type: str, message: str, query_id: Optional[str]):
        now = time.time()
        self._errors.append({
            "timestamp": now,
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
        })
        # Clean errors older than 24 hours to keep memory bounded
        cutoff = now - 86400
        while self._errors and self._errors[0]["timestamp"] < cutoff:
            self._errors.popleft()

    def get_latency_stats(self) -> Dict[str, Optional[float]]:
        if not self._latencies:
            return {
                "avg": None,
                "p50": None,
                "p95": None,
                "p99": None,
                "min": None,
                "max": None,
            }
        lat_sorted = sorted(self._latencies)
        avg = statistics.mean(lat_sorted)
        p50 = lat_sorted[int(len(lat_sorted)*0.5)]
        p95 = lat_sorted[int(len(lat_sorted)*0.95)-1]
        p99 = lat_sorted[int(len(lat_sorted)*0.99)-1]
        return {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": lat_sorted[0],
            "max": lat_sorted[-1],
        }

    def get_doctrine_hit_rate(self) -> float:
        if self._total_queries == 0:
            return 0.0
        return self._doctrine_hits / self._total_queries

    def get_error_rate(self, window_hours: int) -> float:
        now = time.time()
        cutoff = now - window_hours * 3600
        total = 0
        errors = 0
        # Count queries and errors in the window
        for q in self._queries:
            if q.timestamp >= cutoff:
                total += 1
        for e in self._errors:
            if e["timestamp"] >= cutoff:
                errors += 1
        if total == 0:
            return 0.0
        return errors / total

    def queries_last_hour(self) -> int:
        now = time.time()
        cutoff = now - 3600
        count = 0
        for q in self._queries:
            if q.timestamp >= cutoff:
                count += 1
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        # Coverage report includes:
        # - doctrine hit rate
        # - cache hit rate
        # - mode distribution
        # - confidence stats (avg, min, max)
        doctrine_hit_rate = self.get_doctrine_hit_rate()
        cache_hit_rate = self._cache_hits / self._total_queries if self._total_queries > 0 else 0.0
        mode_distribution = dict(self._mode_counts)
        confidence_stats = {}
        if self._confidences:
            confidence_stats["avg"] = statistics.mean(self._confidences)
            confidence_stats["min"] = min(self._confidences)
            confidence_stats["max"] = max(self._confidences)
        else:
            confidence_stats = {"avg": None, "min": None, "max": None}
        return {
            "doctrine_hit_rate": doctrine_hit_rate,
            "cache_hit_rate": cache_hit_rate,
            "mode_distribution": mode_distribution,
            "confidence_stats": confidence_stats,
            "total_queries": self._total_queries,
        }

    def export_jsonl(self, path: pathlib.Path) -> int:
        # Export all stored queries as JSONL to the given path
        count = 0
        try:
            with path.open("w", encoding="utf-8") as f:
                for q in self._queries:
                    # Convert dataclass to dict and serialize
                    d = asdict(q)
                    json_line = json.dumps(d)
                    f.write(json_line + "\n")
                    count += 1
            logger.info(f"Exported {count} queries to {path}")
        except Exception as e:
            logger.error(f"Failed to export JSONL to {path}: {e}")
        return count


class AuditTrailWriter:
    def __init__(self, directory: pathlib.Path):
        self.directory = directory
        self.directory.mkdir(parents=True, exist_ok=True)

    def write(self, metrics: QueryMetrics):
        # Write one JSONL line per query in a file named by date
        dt = time.gmtime(metrics.timestamp)
        filename = time.strftime("audit_%Y-%m-%d.jsonl", dt)
        path = self.directory / filename
        try:
            with path.open("a", encoding="utf-8") as f:
                d = asdict(metrics)
                json_line = json.dumps(d)
                f.write(json_line + "\n")
        except Exception as e:
            logger.error(f"Failed to write audit trail for query {metrics.query_id}: {e}")


COLLECTOR = TelemetryCollector()