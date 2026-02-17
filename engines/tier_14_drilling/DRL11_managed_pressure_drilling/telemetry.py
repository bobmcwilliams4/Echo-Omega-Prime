import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict, field
from typing import List, Optional, Dict, Any, Deque
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "DRL11"

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
        self.queries: Deque[QueryMetrics] = deque(maxlen=maxlen)
        self.errors: Deque[Dict[str, Any]] = deque(maxlen=maxlen)
        self.mode_counter: Counter = Counter()
        self.doctrine_hits: int = 0
        self.doctrine_total: int = 0
        self.cache_hits: int = 0
        self.cache_total: int = 0
        self.latencies: List[float] = []
        self.coverage: Dict[str, int] = defaultdict(int)
        self.audit_writer = AuditTrailWriter()
        logger.debug("TelemetryCollector initialized with maxlen={}", maxlen)

    def record_query(self, metrics: QueryMetrics):
        self.queries.append(metrics)
        self.latencies.append(metrics.latency_ms)
        self.mode_counter[metrics.mode] += 1
        self.doctrine_total += 1
        if metrics.doctrine_matched:
            self.doctrine_hits += 1
        self.cache_total += 1
        if metrics.cache_hit:
            self.cache_hits += 1
        self.coverage[metrics.mode] += 1
        if metrics.error:
            self.record_error(metrics.error, "Query error", metrics.query_id)
        self.audit_writer.write(metrics)
        logger.info("Recorded query: {}", metrics)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "engine_id": ENGINE_ID
        }
        self.errors.append(error_entry)
        logger.error("Error recorded: {}", error_entry)

    def get_latency_stats(self) -> Dict[str, float]:
        if not self.latencies:
            return dict(avg=0, p50=0, p95=0, p99=0, min=0, max=0)
        lat_sorted = sorted(self.latencies)
        avg = statistics.mean(self.latencies)
        p50 = statistics.median(lat_sorted)
        p95 = lat_sorted[int(0.95 * len(lat_sorted)) - 1]
        p99 = lat_sorted[int(0.99 * len(lat_sorted)) - 1]
        min_ = lat_sorted[0]
        max_ = lat_sorted[-1]
        stats = dict(
            avg=avg,
            p50=p50,
            p95=p95,
            p99=p99,
            min=min_,
            max=max_
        )
        logger.debug("Latency stats computed: {}", stats)
        return stats

    def get_doctrine_hit_rate(self) -> float:
        if self.doctrine_total == 0:
            return 0.0
        hit_rate = self.doctrine_hits / self.doctrine_total
        logger.debug("Doctrine hit rate: {:.2%}", hit_rate)
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        total_queries = sum(1 for q in self.queries if q.timestamp >= window_start)
        total_errors = sum(1 for e in self.errors if e["timestamp"] >= window_start)
        if total_queries == 0:
            return 0.0
        error_rate = total_errors / total_queries
        logger.debug("Error rate in last {:.2f} hours: {:.2%}", window_hours, error_rate)
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self.queries if q.timestamp >= one_hour_ago)
        logger.debug("Queries in last hour: {}", count)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        total = sum(self.coverage.values())
        report = {
            "total": total,
            "by_mode": dict(self.coverage)
        }
        logger.debug("Coverage report: {}", report)
        return report

    def export_jsonl(self, path: str) -> int:
        output_path = pathlib.Path(path)
        count = 0
        with output_path.open("w", encoding="utf-8") as f:
            for q in self.queries:
                f.write(json.dumps(asdict(q)) + "\n")
                count += 1
        logger.info("Exported {} queries to {}", count, path)
        return count

class AuditTrailWriter:
    def __init__(self, base_dir: Optional[str] = None):
        if base_dir is None:
            base_dir = "./audit_trail"
        self.base_dir = pathlib.Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        logger.debug("AuditTrailWriter initialized at {}", self.base_dir)

    def write(self, metrics: QueryMetrics):
        date_str = time.strftime("%Y-%m-%d", time.localtime(metrics.timestamp))
        file_path = self.base_dir / f"{date_str}.jsonl"
        entry = asdict(metrics)
        entry["audit_hash"] = self._hash_entry(entry)
        with file_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        logger.debug("Wrote audit entry for query_id={} to {}", metrics.query_id, file_path)

    def _hash_entry(self, entry: Dict[str, Any]) -> str:
        data = json.dumps(entry, sort_keys=True).encode("utf-8")
        return hashlib.sha256(data).hexdigest()

COLLECTOR = TelemetryCollector()