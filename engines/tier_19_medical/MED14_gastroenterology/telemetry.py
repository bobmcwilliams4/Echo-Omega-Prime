import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "MED14"

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
        self._queries: deque = deque(maxlen=maxlen)
        self._errors: deque = deque(maxlen=maxlen)
        self._doctrine_hits: deque = deque(maxlen=maxlen)
        self._latencies: deque = deque(maxlen=maxlen)
        self._query_timestamps: deque = deque(maxlen=maxlen)
        self._coverage: Counter = Counter()
        self._audit_writer = AuditTrailWriter()
        self._lock = None  # Placeholder for threading.Lock if needed

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._latencies.append(metrics.latency_ms)
        self._query_timestamps.append(metrics.timestamp)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._coverage[metrics.mode] += 1
        if metrics.error:
            self.record_error(metrics.error, "Query error", metrics.query_id)
        self._audit_writer.write(metrics)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "error_type": error_type,
            "message": message,
            "query_id": query_id
        }
        self._errors.append(error_entry)
        logger.error(f"Error recorded: {error_entry}")

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = list(self._latencies)
        if not latencies:
            return {
                "avg": None, "p50": None, "p95": None, "p99": None,
                "min": None, "max": None
            }
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        min_v = min(latencies)
        max_v = max(latencies)
        p50 = statistics.median(latencies_sorted)
        p95 = latencies_sorted[int(0.95 * len(latencies_sorted))-1]
        p99 = latencies_sorted[int(0.99 * len(latencies_sorted))-1]
        return {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_v,
            "max": max_v
        }

    def get_doctrine_hit_rate(self) -> float:
        if not self._doctrine_hits:
            return 0.0
        hits = sum(1 for hit in self._doctrine_hits if hit)
        return hits / len(self._doctrine_hits)

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        total_queries = sum(1 for t in self._query_timestamps if t >= window_start)
        total_errors = sum(1 for e in self._errors if e["timestamp"] >= window_start)
        if total_queries == 0:
            return 0.0
        return total_errors / total_queries

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        return sum(1 for t in self._query_timestamps if t >= one_hour_ago)

    def get_coverage_report(self) -> Dict[str, Any]:
        total = sum(self._coverage.values())
        if total == 0:
            return {}
        report = {}
        for mode, count in self._coverage.items():
            report[mode] = {
                "count": count,
                "pct": count / total
            }
        return report

    def export_jsonl(self, path: str) -> int:
        path_obj = pathlib.Path(path)
        count = 0
        with path_obj.open("w", encoding="utf-8") as f:
            for metrics in self._queries:
                f.write(json.dumps(asdict(metrics)) + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {path}")
        return count

class AuditTrailWriter:
    def __init__(self, base_dir: Optional[str] = None):
        if base_dir is None:
            base_dir = "./audit_trail"
        self.base_dir = pathlib.Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def write(self, metrics: QueryMetrics):
        date_str = time.strftime("%Y-%m-%d", time.localtime(metrics.timestamp))
        filename = f"{ENGINE_ID}_{date_str}.jsonl"
        file_path = self.base_dir / filename
        entry = asdict(metrics)
        entry["audit_hash"] = self._hash_entry(entry)
        with file_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    def _hash_entry(self, entry: Dict[str, Any]) -> str:
        # Exclude audit_hash itself if present
        entry_copy = dict(entry)
        entry_copy.pop("audit_hash", None)
        serialized = json.dumps(entry_copy, sort_keys=True)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

COLLECTOR = TelemetryCollector()