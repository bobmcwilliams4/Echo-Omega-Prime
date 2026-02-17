import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any
from collections import deque, defaultdict, Counter
from loguru import logger


ENGINE_ID = "AUTO12"


@dataclass
class QueryMetrics:
    query_id: str
    engine_id: str
    timestamp: float
    latency_ms: float
    cache_hit: bool
    doctrine_matched: bool
    mode: str
    confidence: Optional[float] = None
    error: Optional[str] = None


class TelemetryCollector:
    def __init__(self):
        # Store all queries as deque for efficient append and pops from left
        self._queries: deque[QueryMetrics] = deque()
        # Store errors as list of dicts with timestamp, error_type, message, query_id
        self._errors: deque[Dict[str, Any]] = deque()
        # For coverage report: count of queries per mode and doctrine matched
        self._mode_counter: Counter = Counter()
        self._doctrine_hits: int = 0
        self._total_queries: int = 0
        # Cache hit count
        self._cache_hits: int = 0
        # Lock for thread safety if needed (not implemented here)
        # self._lock = threading.Lock()

    def record_query(self, metrics: QueryMetrics):
        # Append query metrics
        self._queries.append(metrics)
        self._total_queries += 1
        if metrics.doctrine_matched:
            self._doctrine_hits += 1
        if metrics.cache_hit:
            self._cache_hits += 1
        self._mode_counter[metrics.mode] += 1

        # Clean up old queries and errors beyond 24 hours to keep memory bounded
        cutoff = time.time() - 24 * 3600
        while self._queries and self._queries[0].timestamp < cutoff:
            old = self._queries.popleft()
            self._total_queries -= 1
            if old.doctrine_matched:
                self._doctrine_hits -= 1
            if old.cache_hit:
                self._cache_hits -= 1
            self._mode_counter[old.mode] -= 1
            if self._mode_counter[old.mode] == 0:
                del self._mode_counter[old.mode]

        while self._errors and self._errors[0]['timestamp'] < cutoff:
            self._errors.popleft()

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
        }
        self._errors.append(error_entry)

    def get_latency_stats(self) -> Dict[str, Optional[float]]:
        latencies = [q.latency_ms for q in self._queries if q.latency_ms is not None]
        if not latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        p50 = latencies_sorted[int(len(latencies_sorted) * 0.50)]
        p95 = latencies_sorted[int(len(latencies_sorted) * 0.95) - 1]
        p99 = latencies_sorted[int(len(latencies_sorted) * 0.99) - 1]
        min_latency = latencies_sorted[0]
        max_latency = latencies_sorted[-1]
        return {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_latency,
            "max": max_latency,
        }

    def get_doctrine_hit_rate(self) -> float:
        if self._total_queries == 0:
            return 0.0
        return self._doctrine_hits / self._total_queries

    def get_error_rate(self, window_hours: int) -> float:
        now = time.time()
        cutoff = now - window_hours * 3600
        errors_in_window = [e for e in self._errors if e['timestamp'] >= cutoff]
        queries_in_window = [q for q in self._queries if q.timestamp >= cutoff]
        total_queries = len(queries_in_window)
        if total_queries == 0:
            return 0.0
        return len(errors_in_window) / total_queries

    def queries_last_hour(self) -> int:
        now = time.time()
        cutoff = now - 3600
        count = 0
        for q in reversed(self._queries):
            if q.timestamp >= cutoff:
                count += 1
            else:
                break
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        # Report coverage by mode and doctrine matched ratio per mode
        report = {}
        total = sum(self._mode_counter.values())
        for mode, count in self._mode_counter.items():
            doctrine_hits_mode = sum(
                1 for q in self._queries if q.mode == mode and q.doctrine_matched
            )
            coverage = doctrine_hits_mode / count if count > 0 else 0.0
            report[mode] = {
                "queries": count,
                "doctrine_hit_rate": coverage,
            }
        report["total_queries"] = total
        report["overall_doctrine_hit_rate"] = self.get_doctrine_hit_rate()
        report["cache_hit_rate"] = self._cache_hits / total if total > 0 else 0.0
        return report

    def export_jsonl(self, path: pathlib.Path) -> int:
        # Export all queries as JSONL to the given path
        count = 0
        try:
            with path.open("w", encoding="utf-8") as f:
                for q in self._queries:
                    obj = asdict(q)
                    f.write(json.dumps(obj) + "\n")
                    count += 1
            logger.info(f"Exported {count} telemetry records to {path}")
        except Exception as e:
            logger.error(f"Failed to export telemetry to {path}: {e}")
        return count


class AuditTrailWriter:
    def __init__(self, directory: pathlib.Path):
        self.directory = directory
        self.directory.mkdir(parents=True, exist_ok=True)

    def write(self, metrics: QueryMetrics):
        # Write one JSONL file per query with filename hash of query_id + timestamp
        try:
            filename_hash = hashlib.sha256(
                (metrics.query_id + str(metrics.timestamp)).encode("utf-8")
            ).hexdigest()
            filename = f"{filename_hash}.jsonl"
            filepath = self.directory / filename
            with filepath.open("w", encoding="utf-8") as f:
                f.write(json.dumps(asdict(metrics)) + "\n")
            logger.debug(f"Audit trail written for query_id={metrics.query_id} to {filepath}")
        except Exception as e:
            logger.error(f"Failed to write audit trail for query_id={metrics.query_id}: {e}")


COLLECTOR = TelemetryCollector()