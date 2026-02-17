import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional, Any, Deque
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "MATH04"

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
        self._queries: Deque[QueryMetrics] = deque(maxlen=maxlen)
        self._errors: Deque[Dict[str, Any]] = deque(maxlen=maxlen)
        self._doctrine_counter: Counter = Counter()
        self._cache_counter: Counter = Counter()
        self._mode_counter: Counter = Counter()
        self._coverage: Dict[str, set] = defaultdict(set)
        self._latencies: Deque[float] = deque(maxlen=maxlen)
        self._audit_writer = AuditTrailWriter()
        self._lock = None  # Placeholder for future thread safety

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_counter[metrics.doctrine_matched] += 1
        self._cache_counter[metrics.cache_hit] += 1
        self._mode_counter[metrics.mode] += 1
        self._coverage[metrics.mode].add(metrics.query_id)
        if metrics.error:
            self.record_error(metrics.error, "QueryError", metrics.query_id)
        self._audit_writer.write(metrics)
        logger.debug(f"Recorded query: {metrics}")

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        err = {
            "timestamp": time.time(),
            "error_type": error_type,
            "message": message,
            "query_id": query_id
        }
        self._errors.append(err)
        logger.error(f"Error recorded: {err}")

    def get_latency_stats(self) -> Dict[str, float]:
        latencies = list(self._latencies)
        if not latencies:
            return dict(avg=0, p50=0, p95=0, p99=0, min=0, max=0)
        latencies.sort()
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = latencies[int(0.95 * len(latencies)) - 1]
        p99 = latencies[int(0.99 * len(latencies)) - 1]
        min_latency = latencies[0]
        max_latency = latencies[-1]
        stats = dict(
            avg=avg,
            p50=p50,
            p95=p95,
            p99=p99,
            min=min_latency,
            max=max_latency
        )
        logger.debug(f"Latency stats: {stats}")
        return stats

    def get_doctrine_hit_rate(self) -> float:
        total = sum(self._doctrine_counter.values())
        if total == 0:
            return 0.0
        hit_rate = self._doctrine_counter[True] / total
        logger.debug(f"Doctrine hit rate: {hit_rate}")
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        queries_in_window = [q for q in self._queries if q.timestamp >= window_start]
        n_queries = len(queries_in_window)
        n_errors = len(errors_in_window)
        if n_queries == 0:
            return 0.0
        error_rate = n_errors / n_queries
        logger.debug(f"Error rate in last {window_hours}h: {error_rate}")
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= one_hour_ago)
        logger.debug(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {}
        for mode, queries in self._coverage.items():
            report[mode] = len(queries)
        logger.debug(f"Coverage report: {report}")
        return report

    def export_jsonl(self, path: str) -> int:
        path_obj = pathlib.Path(path)
        n = 0
        with path_obj.open("w", encoding="utf-8") as f:
            for q in self._queries:
                f.write(json.dumps(asdict(q)) + "\n")
                n += 1
        logger.info(f"Exported {n} queries to {path}")
        return n

class AuditTrailWriter:
    def __init__(self, base_dir: Optional[str] = None):
        if base_dir is None:
            base_dir = "./audit_trail"
        self.base_dir = pathlib.Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def write(self, metrics: QueryMetrics):
        date_str = time.strftime("%Y-%m-%d", time.localtime(metrics.timestamp))
        file_path = self.base_dir / f"{date_str}.jsonl"
        record = asdict(metrics)
        record["audit_hash"] = self._hash_record(record)
        with file_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
        logger.debug(f"Audit written for query_id={metrics.query_id}")

    def _hash_record(self, record: Dict[str, Any]) -> str:
        rec_copy = dict(record)
        rec_copy.pop("audit_hash", None)
        rec_bytes = json.dumps(rec_copy, sort_keys=True).encode("utf-8")
        return hashlib.sha256(rec_bytes).hexdigest()

COLLECTOR = TelemetryCollector()