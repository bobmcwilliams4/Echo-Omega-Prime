import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict, field
from typing import Optional, List, Dict, Any
from collections import deque, defaultdict
from loguru import logger


ENGINE_ID = "CHEM09"


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
    def __init__(self):
        self._queries: deque[QueryMetrics] = deque()
        self._errors: deque[Dict[str, Any]] = deque()
        self._lock = None  # placeholder for threading.Lock() if needed
        self._max_history_seconds = 3600 * 24  # keep 24 hours of data max
        self._audit_writer = AuditTrailWriter()
        self._coverage_modes = defaultdict(int)
        self._coverage_total = 0

    def record_query(self, metrics: QueryMetrics):
        now = time.time()
        # Purge old queries beyond max history
        while self._queries and (now - self._queries[0].timestamp) > self._max_history_seconds:
            old = self._queries.popleft()
            # Adjust coverage counts
            self._coverage_modes[old.mode] -= 1
            self._coverage_total -= 1

        self._queries.append(metrics)
        self._coverage_modes[metrics.mode] += 1
        self._coverage_total += 1

        if metrics.error:
            self.record_error("query_error", metrics.error, metrics.query_id)

        try:
            self._audit_writer.write(metrics)
        except Exception as e:
            logger.error(f"Failed to write audit trail for query {metrics.query_id}: {e}")

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        now = time.time()
        error_record = {
            "timestamp": now,
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
        }
        self._errors.append(error_record)
        # Purge old errors beyond max history
        while self._errors and (now - self._errors[0]["timestamp"]) > self._max_history_seconds:
            self._errors.popleft()

    def get_latency_stats(self) -> dict:
        latencies = [q.latency_ms for q in self._queries if q.latency_ms is not None]
        if not latencies:
            return {
                "avg": None,
                "p50": None,
                "p95": None,
                "p99": None,
                "min": None,
                "max": None,
            }
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        p50 = latencies_sorted[int(len(latencies_sorted) * 0.50)]
        p95 = latencies_sorted[int(len(latencies_sorted) * 0.95) - 1]
        p99 = latencies_sorted[int(len(latencies_sorted) * 0.99) - 1]
        return {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": latencies_sorted[0],
            "max": latencies_sorted[-1],
        }

    def get_doctrine_hit_rate(self) -> float:
        if not self._queries:
            return 0.0
        hits = sum(1 for q in self._queries if q.doctrine_matched)
        return hits / len(self._queries)

    def get_error_rate(self, window_hours: int) -> float:
        now = time.time()
        window_seconds = window_hours * 3600
        queries_in_window = [q for q in self._queries if (now - q.timestamp) <= window_seconds]
        if not queries_in_window:
            return 0.0
        errors_in_window = [e for e in self._errors if (now - e["timestamp"]) <= window_seconds]
        return len(errors_in_window) / len(queries_in_window)

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = 0
        for q in reversed(self._queries):
            if q.timestamp < one_hour_ago:
                break
            count += 1
        return count

    def get_coverage_report(self) -> dict:
        if self._coverage_total == 0:
            return {}
        coverage = {}
        for mode, count in self._coverage_modes.items():
            coverage[mode] = count / self._coverage_total
        return coverage

    def export_jsonl(self, path: pathlib.Path) -> int:
        count = 0
        try:
            with path.open("w", encoding="utf-8") as f:
                for q in self._queries:
                    f.write(json.dumps(asdict(q)) + "\n")
                    count += 1
        except Exception as e:
            logger.error(f"Failed to export telemetry to {path}: {e}")
        return count


class AuditTrailWriter:
    def __init__(self, directory: Optional[pathlib.Path] = None):
        if directory is None:
            directory = pathlib.Path("./audit_trails")
        self.directory = directory
        self.directory.mkdir(parents=True, exist_ok=True)

    def write(self, metrics: QueryMetrics):
        filename = self._filename(metrics.query_id)
        filepath = self.directory / filename
        record = asdict(metrics)
        record["written_at"] = time.time()
        with filepath.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")

    def _filename(self, query_id: str) -> str:
        # Hash query_id to avoid filesystem issues and collisions
        h = hashlib.sha256(query_id.encode("utf-8")).hexdigest()
        return f"{h}.jsonl"


COLLECTOR = TelemetryCollector()