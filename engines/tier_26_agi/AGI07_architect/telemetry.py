import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any
from collections import deque, defaultdict
from loguru import logger


ENGINE_ID = "AGI07"


@dataclass
class QueryMetrics:
    query_id: str
    engine_id: str
    timestamp: float
    latency_ms: float
    cache_hit: bool
    doctrine_matched: bool
    mode: str
    confidence: Optional[float]
    error: Optional[str]


class TelemetryCollector:
    def __init__(self):
        # Store QueryMetrics objects
        self._queries: deque[QueryMetrics] = deque()
        # Store errors as tuples: (timestamp, error_type, message, query_id)
        self._errors: deque = deque()
        # For coverage report: count doctrine matches per mode
        self._doctrine_counts: Dict[str, int] = defaultdict(int)
        self._doctrine_total: int = 0
        # For cache hit rate and other stats
        self._cache_hits: int = 0
        self._total_queries: int = 0
        # Lock for thread safety if needed (not implemented here)
        # For latency stats cache
        self._latencies: List[float] = []
        # For audit trail writer
        self.audit_writer = AuditTrailWriter()

    def record_query(self, metrics: QueryMetrics):
        logger.debug(f"Recording query metrics: {metrics}")
        self._queries.append(metrics)
        self._latencies.append(metrics.latency_ms)
        self._total_queries += 1
        if metrics.cache_hit:
            self._cache_hits += 1
        if metrics.doctrine_matched:
            self._doctrine_counts[metrics.mode] += 1
            self._doctrine_total += 1
        # Clean old data beyond 24 hours for memory management
        self._cleanup_old_data()
        # Write audit trail
        self.audit_writer.write(metrics)

    def record_error(self, error_type: str, message: str, query_id: Optional[str]):
        timestamp = time.time()
        logger.error(f"Recording error: type={error_type}, message={message}, query_id={query_id}")
        self._errors.append((timestamp, error_type, message, query_id))
        self._cleanup_old_data()

    def _cleanup_old_data(self):
        # Remove queries and errors older than 24 hours
        cutoff = time.time() - 86400  # 24 hours
        while self._queries and self._queries[0].timestamp < cutoff:
            old = self._queries.popleft()
            self._latencies.pop(0)
            self._total_queries -= 1
            if old.cache_hit:
                self._cache_hits -= 1
            if old.doctrine_matched:
                self._doctrine_counts[old.mode] -= 1
                self._doctrine_total -= 1
        while self._errors and self._errors[0][0] < cutoff:
            self._errors.popleft()

    def get_latency_stats(self) -> Dict[str, float]:
        latencies = self._latencies
        if not latencies:
            return {"avg": 0, "p50": 0, "p95": 0, "p99": 0, "min": 0, "max": 0}
        lat_sorted = sorted(latencies)
        avg = statistics.mean(lat_sorted)
        p50 = lat_sorted[int(len(lat_sorted)*0.50)]
        p95 = lat_sorted[int(len(lat_sorted)*0.95)-1]
        p99 = lat_sorted[int(len(lat_sorted)*0.99)-1]
        min_lat = lat_sorted[0]
        max_lat = lat_sorted[-1]
        stats = {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_lat,
            "max": max_lat,
        }
        logger.debug(f"Latency stats computed: {stats}")
        return stats

    def get_doctrine_hit_rate(self) -> float:
        if self._total_queries == 0:
            return 0.0
        rate = self._doctrine_total / self._total_queries
        logger.debug(f"Doctrine hit rate: {rate} ({self._doctrine_total}/{self._total_queries})")
        return rate

    def get_error_rate(self, window_hours: int) -> float:
        now = time.time()
        cutoff = now - window_hours * 3600
        error_count = sum(1 for e in self._errors if e[0] >= cutoff)
        query_count = sum(1 for q in self._queries if q.timestamp >= cutoff)
        if query_count == 0:
            return 0.0
        rate = error_count / query_count
        logger.debug(f"Error rate over last {window_hours} hours: {rate} ({error_count}/{query_count})")
        return rate

    def queries_last_hour(self) -> int:
        now = time.time()
        cutoff = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= cutoff)
        logger.debug(f"Queries in the last hour: {count}")
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        # Coverage report: doctrine matches per mode and total queries per mode
        mode_counts = defaultdict(int)
        mode_doctrine = defaultdict(int)
        for q in self._queries:
            mode_counts[q.mode] += 1
            if q.doctrine_matched:
                mode_doctrine[q.mode] += 1
        report = {}
        for mode in mode_counts:
            total = mode_counts[mode]
            matched = mode_doctrine.get(mode, 0)
            coverage = matched / total if total > 0 else 0.0
            report[mode] = {
                "total_queries": total,
                "doctrine_matched": matched,
                "coverage": coverage,
            }
        logger.debug(f"Coverage report generated: {report}")
        return report

    def export_jsonl(self, path: pathlib.Path) -> int:
        count = 0
        try:
            with path.open("w", encoding="utf-8") as f:
                for q in self._queries:
                    line = json.dumps(asdict(q))
                    f.write(line + "\n")
                    count += 1
            logger.info(f"Exported {count} telemetry records to {path}")
        except Exception as e:
            logger.error(f"Failed to export telemetry to {path}: {e}")
        return count


class AuditTrailWriter:
    def __init__(self, directory: Optional[pathlib.Path] = None):
        if directory is None:
            directory = pathlib.Path("./audit_trail")
        self.directory = directory
        self.directory.mkdir(parents=True, exist_ok=True)
        self._file_handles: Dict[str, Any] = {}

    def _get_file_handle(self, query_id: str):
        # Use first 2 chars of query_id as subdirectory for sharding
        shard = query_id[:2]
        shard_dir = self.directory / shard
        shard_dir.mkdir(parents=True, exist_ok=True)
        file_path = shard_dir / f"{query_id}.jsonl"
        if file_path not in self._file_handles:
            self._file_handles[file_path] = open(file_path, "a", encoding="utf-8")
        return self._file_handles[file_path]

    def write(self, metrics: QueryMetrics):
        try:
            fh = self._get_file_handle(metrics.query_id)
            line = json.dumps(asdict(metrics))
            fh.write(line + "\n")
            fh.flush()
            logger.debug(f"Audit trail written for query_id={metrics.query_id}")
        except Exception as e:
            logger.error(f"Failed to write audit trail for query_id={metrics.query_id}: {e}")

    def close_all(self):
        for fh in self._file_handles.values():
            try:
                fh.close()
            except Exception:
                pass
        self._file_handles.clear()


COLLECTOR = TelemetryCollector()