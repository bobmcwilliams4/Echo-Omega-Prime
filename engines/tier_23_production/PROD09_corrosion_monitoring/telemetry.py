import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Union
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "PROD09"

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
        self._coverage: defaultdict = defaultdict(lambda: {"count": 0, "doctrine_matched": 0})
        self._audit_writer = AuditTrailWriter()
        self._query_counter: Counter = Counter()
        self._error_counter: Counter = Counter()
        self._last_exported_idx: int = 0
        logger.info(f"TelemetryCollector initialized for engine {ENGINE_ID}")

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._coverage[metrics.mode]["count"] += 1
        if metrics.doctrine_matched:
            self._coverage[metrics.mode]["doctrine_matched"] += 1
        self._query_counter[metrics.mode] += 1
        if metrics.error:
            self.record_error(metrics.error, "Query error", metrics.query_id)
        self._audit_writer.write(metrics)
        logger.debug(f"Recorded query: {metrics.query_id}")

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "engine_id": ENGINE_ID,
            "error_type": error_type,
            "message": message,
            "query_id": query_id
        }
        self._errors.append(error_entry)
        self._error_counter[error_type] += 1
        logger.warning(f"Error recorded: {error_type} ({message}) for query {query_id}")

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = list(self._latencies)
        if not latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = latencies_sorted[int(0.95 * len(latencies_sorted)) - 1]
        p99 = latencies_sorted[int(0.99 * len(latencies_sorted)) - 1]
        min_latency = min(latencies)
        max_latency = max(latencies)
        logger.info(f"Latency stats computed: avg={avg}, p50={p50}, p95={p95}, p99={p99}, min={min_latency}, max={max_latency}")
        return {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_latency,
            "max": max_latency
        }

    def get_doctrine_hit_rate(self) -> float:
        total = len(self._doctrine_hits)
        if total == 0:
            return 0.0
        hits = sum(1 for hit in self._doctrine_hits if hit)
        rate = hits / total
        logger.info(f"Doctrine hit rate: {rate} ({hits}/{total})")
        return rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        queries_in_window = [q for q in self._queries if q.timestamp >= window_start]
        num_queries = len(queries_in_window)
        num_errors = len(errors_in_window)
        if num_queries == 0:
            return 0.0
        error_rate = num_errors / num_queries
        logger.info(f"Error rate in last {window_hours} hours: {error_rate} ({num_errors}/{num_queries})")
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= one_hour_ago)
        logger.info(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {}
        for mode, data in self._coverage.items():
            total = data["count"]
            doctrine_matched = data["doctrine_matched"]
            hit_rate = doctrine_matched / total if total > 0 else 0.0
            report[mode] = {
                "total_queries": total,
                "doctrine_matched": doctrine_matched,
                "doctrine_hit_rate": hit_rate
            }
        logger.info(f"Coverage report generated: {report}")
        return report

    def export_jsonl(self, path: Union[str, pathlib.Path]) -> int:
        path = pathlib.Path(path)
        exported_count = 0
        with path.open("a") as f:
            for idx, metrics in enumerate(list(self._queries)[self._last_exported_idx:]):
                f.write(json.dumps(dataclasses.asdict(metrics)) + "\n")
                exported_count += 1
            self._last_exported_idx += exported_count
        logger.info(f"Exported {exported_count} queries to {path}")
        return exported_count

class AuditTrailWriter:
    def __init__(self, audit_dir: Union[str, pathlib.Path] = "./audit_trail"):
        self.audit_dir = pathlib.Path(audit_dir)
        self.audit_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"AuditTrailWriter initialized at {self.audit_dir}")

    def write(self, metrics: QueryMetrics):
        audit_file = self.audit_dir / f"{metrics.query_id}.jsonl"
        entry = dataclasses.asdict(metrics)
        entry["audit_hash"] = self._hash_entry(entry)
        with audit_file.open("a") as f:
            f.write(json.dumps(entry) + "\n")
        logger.debug(f"Audit trail written for query {metrics.query_id}")

    def _hash_entry(self, entry: Dict[str, Any]) -> str:
        entry_str = json.dumps(entry, sort_keys=True)
        return hashlib.sha256(entry_str.encode("utf-8")).hexdigest()

COLLECTOR = TelemetryCollector()