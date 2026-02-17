import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any
from collections import deque, defaultdict
from loguru import logger


ENGINE_ID = "CHEM06"


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
        # Store QueryMetrics objects
        self._queries: deque[QueryMetrics] = deque()
        # Store errors as tuples: (timestamp, error_type, message, query_id)
        self._errors: deque = deque()
        # For coverage report: count doctrine matches and total queries by mode
        self._doctrine_hits = 0
        self._total_queries = 0
        self._mode_counts = defaultdict(int)
        self._doctrine_mode_counts = defaultdict(int)
        # Lock for thread safety if needed (not implemented here)
        logger.debug("TelemetryCollector initialized")

    def record_query(self, metrics: QueryMetrics):
        if metrics.engine_id != ENGINE_ID:
            logger.warning(f"Ignoring query for engine {metrics.engine_id}, expected {ENGINE_ID}")
            return
        self._queries.append(metrics)
        self._total_queries += 1
        self._mode_counts[metrics.mode] += 1
        if metrics.doctrine_matched:
            self._doctrine_hits += 1
            self._doctrine_mode_counts[metrics.mode] += 1
        logger.debug(f"Recorded query {metrics.query_id} at {metrics.timestamp}")

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        now = time.time()
        self._errors.append((now, error_type, message, query_id))
        logger.error(f"Recorded error {error_type} for query {query_id}: {message}")

    def get_latency_stats(self) -> Dict[str, Optional[float]]:
        latencies = [q.latency_ms for q in self._queries if q.latency_ms is not None]
        if not latencies:
            logger.debug("No latencies recorded yet")
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = latencies_sorted[int(len(latencies_sorted) * 0.95) - 1]
        p99 = latencies_sorted[int(len(latencies_sorted) * 0.99) - 1]
        min_latency = latencies_sorted[0]
        max_latency = latencies_sorted[-1]
        stats = {"avg": avg, "p50": p50, "p95": p95, "p99": p99, "min": min_latency, "max": max_latency}
        logger.debug(f"Latency stats computed: {stats}")
        return stats

    def get_doctrine_hit_rate(self) -> float:
        if self._total_queries == 0:
            logger.debug("No queries recorded for doctrine hit rate")
            return 0.0
        rate = self._doctrine_hits / self._total_queries
        logger.debug(f"Doctrine hit rate: {rate:.4f}")
        return rate

    def get_error_rate(self, window_hours: float) -> float:
        now = time.time()
        window_seconds = window_hours * 3600
        window_start = now - window_seconds
        errors_in_window = [e for e in self._errors if e[0] >= window_start]
        queries_in_window = [q for q in self._queries if q.timestamp >= window_start]
        if not queries_in_window:
            logger.debug("No queries in window for error rate calculation")
            return 0.0
        rate = len(errors_in_window) / len(queries_in_window)
        logger.debug(f"Error rate over last {window_hours}h: {rate:.4f}")
        return rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= one_hour_ago)
        logger.debug(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {}
        total = self._total_queries
        doctrine = self._doctrine_hits
        report["total_queries"] = total
        report["doctrine_hits"] = doctrine
        report["doctrine_hit_rate"] = (doctrine / total) if total > 0 else 0.0
        mode_coverage = {}
        for mode, count in self._mode_counts.items():
            hits = self._doctrine_mode_counts.get(mode, 0)
            mode_coverage[mode] = {
                "queries": count,
                "doctrine_hits": hits,
                "hit_rate": (hits / count) if count > 0 else 0.0,
            }
        report["mode_coverage"] = mode_coverage
        logger.debug(f"Coverage report generated: {report}")
        return report

    def export_jsonl(self, path: pathlib.Path) -> int:
        count = 0
        try:
            with path.open("w", encoding="utf-8") as f:
                for q in self._queries:
                    record = asdict(q)
                    f.write(json.dumps(record) + "\n")
                    count += 1
            logger.info(f"Exported {count} query records to {path}")
        except Exception as e:
            logger.error(f"Failed to export telemetry to {path}: {e}")
            raise
        return count


class AuditTrailWriter:
    def __init__(self, directory: pathlib.Path):
        self.directory = directory
        self.directory.mkdir(parents=True, exist_ok=True)
        logger.debug(f"AuditTrailWriter initialized at {self.directory}")

    def _sanitize_filename(self, name: str) -> str:
        # Simple sanitization for filenames
        safe = "".join(c if c.isalnum() or c in "-_." else "_" for c in name)
        return safe

    def write(self, metrics: QueryMetrics) -> None:
        # Write a JSONL file per query with audit trail info
        filename = f"{self._sanitize_filename(metrics.query_id)}.jsonl"
        filepath = self.directory / filename
        record = asdict(metrics)
        try:
            with filepath.open("w", encoding="utf-8") as f:
                json.dump(record, f)
                f.write("\n")
            logger.debug(f"Audit trail written for query {metrics.query_id} at {filepath}")
        except Exception as e:
            logger.error(f"Failed to write audit trail for query {metrics.query_id}: {e}")
            raise


COLLECTOR = TelemetryCollector()