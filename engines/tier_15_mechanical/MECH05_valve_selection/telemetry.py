import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "MECH05"

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
        self._query_counter: Counter = Counter()
        self._doctrine_counter: Counter = Counter()
        self._error_counter: Counter = Counter()
        self._latencies: List[float] = []
        self._cache_hits: Counter = Counter()
        self._audit_writer = AuditTrailWriter()
        logger.info(f"TelemetryCollector initialized for engine {ENGINE_ID}")

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._query_counter[metrics.mode] += 1
        self._doctrine_counter["matched" if metrics.doctrine_matched else "unmatched"] += 1
        self._latencies.append(metrics.latency_ms)
        self._cache_hits["hit" if metrics.cache_hit else "miss"] += 1
        if metrics.error:
            self._error_counter[metrics.error] += 1
            self._errors.append({
                "error_type": metrics.error,
                "query_id": metrics.query_id,
                "timestamp": metrics.timestamp
            })
        self._audit_writer.write(metrics)
        logger.debug(f"Recorded query: {metrics.query_id}")

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        timestamp = time.time()
        error_record = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "timestamp": timestamp
        }
        self._errors.append(error_record)
        self._error_counter[error_type] += 1
        logger.error(f"Error recorded: {error_type} for query {query_id}")

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = [q.latency_ms for q in self._queries if q.latency_ms is not None]
        if not latencies:
            return dict(avg=None, p50=None, p95=None, p99=None, min=None, max=None)
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        min_latency = min(latencies)
        max_latency = max(latencies)
        p50 = statistics.median(latencies)
        def percentile(p):
            idx = int(len(latencies_sorted) * p)
            idx = min(idx, len(latencies_sorted)-1)
            return latencies_sorted[idx]
        p95 = percentile(0.95)
        p99 = percentile(0.99)
        stats = dict(
            avg=avg,
            p50=p50,
            p95=p95,
            p99=p99,
            min=min_latency,
            max=max_latency
        )
        logger.info(f"Latency stats: {stats}")
        return stats

    def get_doctrine_hit_rate(self) -> float:
        matched = self._doctrine_counter["matched"]
        total = matched + self._doctrine_counter["unmatched"]
        hit_rate = matched / total if total > 0 else 0.0
        logger.info(f"Doctrine hit rate: {hit_rate}")
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        total_queries = sum(1 for q in self._queries if q.timestamp >= window_start)
        total_errors = sum(1 for e in self._errors if e["timestamp"] >= window_start)
        error_rate = total_errors / total_queries if total_queries > 0 else 0.0
        logger.info(f"Error rate in last {window_hours} hours: {error_rate}")
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= one_hour_ago)
        logger.info(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        modes = Counter(q.mode for q in self._queries)
        cache_hits = self._cache_hits.copy()
        doctrine = self._doctrine_counter.copy()
        errors = self._error_counter.copy()
        report = {
            "engine_id": ENGINE_ID,
            "total_queries": len(self._queries),
            "modes": dict(modes),
            "cache_hits": dict(cache_hits),
            "doctrine": dict(doctrine),
            "errors": dict(errors),
            "last_query_time": self._queries[-1].timestamp if self._queries else None
        }
        logger.info(f"Coverage report: {report}")
        return report

    def export_jsonl(self, path: str) -> int:
        p = pathlib.Path(path)
        count = 0
        with p.open("w", encoding="utf-8") as f:
            for q in self._queries:
                f.write(json.dumps(asdict(q)) + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {path}")
        return count

class AuditTrailWriter:
    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = base_dir or "./audit_trail"
        self._ensure_dir()
        logger.info(f"AuditTrailWriter initialized at {self.base_dir}")

    def _ensure_dir(self):
        p = pathlib.Path(self.base_dir)
        p.mkdir(parents=True, exist_ok=True)

    def write(self, metrics: QueryMetrics):
        filename = self._get_filename(metrics.query_id)
        record = asdict(metrics)
        record["audit_hash"] = self._hash_record(record)
        with open(filename, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
        logger.debug(f"Audit trail written for query {metrics.query_id}")

    def _get_filename(self, query_id: str) -> str:
        date_str = time.strftime("%Y%m%d")
        fname = f"{ENGINE_ID}_{date_str}_audit.jsonl"
        return str(pathlib.Path(self.base_dir) / fname)

    def _hash_record(self, record: Dict[str, Any]) -> str:
        record_str = json.dumps(record, sort_keys=True)
        return hashlib.sha256(record_str.encode("utf-8")).hexdigest()

COLLECTOR = TelemetryCollector()