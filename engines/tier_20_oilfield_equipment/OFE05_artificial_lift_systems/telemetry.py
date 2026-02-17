import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict, field
from typing import List, Optional, Dict, Any, Deque
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "OFE05"

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
        self.audit_writer = AuditTrailWriter()
        self._doctrine_hits = 0
        self._doctrine_total = 0
        self._lock = None  # Placeholder for future threading.Lock if needed

    def record_query(self, metrics: QueryMetrics):
        logger.debug(f"Recording query: {metrics}")
        self.queries.append(metrics)
        self._doctrine_total += 1
        if metrics.doctrine_matched:
            self._doctrine_hits += 1
        self.audit_writer.write(metrics)
        if metrics.error:
            self.record_error(metrics.error, "Query error", metrics.query_id)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "engine_id": ENGINE_ID,
            "error_type": error_type,
            "message": message,
            "query_id": query_id
        }
        logger.error(f"Error recorded: {error_entry}")
        self.errors.append(error_entry)

    def get_latency_stats(self) -> Dict[str, float]:
        latencies = [q.latency_ms for q in self.queries if q.latency_ms is not None]
        if not latencies:
            return dict(avg=0, p50=0, p95=0, p99=0, min=0, max=0)
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)
        min_v = min(latencies)
        max_v = max(latencies)
        logger.info(f"Latency stats: avg={avg}, p50={p50}, p95={p95}, p99={p99}, min={min_v}, max={max_v}")
        return dict(avg=avg, p50=p50, p95=p95, p99=p99, min=min_v, max=max_v)

    def _percentile(self, data: List[float], percentile: float) -> float:
        if not data:
            return 0.0
        k = (len(data) - 1) * (percentile / 100)
        f = int(k)
        c = min(f + 1, len(data) - 1)
        if f == c:
            return sorted(data)[int(k)]
        d0 = sorted(data)[f] * (c - k)
        d1 = sorted(data)[c] * (k - f)
        return d0 + d1

    def get_doctrine_hit_rate(self) -> float:
        if self._doctrine_total == 0:
            return 0.0
        rate = self._doctrine_hits / self._doctrine_total
        logger.info(f"Doctrine hit rate: {rate}")
        return rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        error_count = sum(1 for e in self.errors if e["timestamp"] >= window_start)
        query_count = sum(1 for q in self.queries if q.timestamp >= window_start)
        if query_count == 0:
            return 0.0
        rate = error_count / query_count
        logger.info(f"Error rate in last {window_hours} hours: {rate}")
        return rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self.queries if q.timestamp >= one_hour_ago)
        logger.info(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        modes = Counter(q.mode for q in self.queries)
        cache_hits = sum(1 for q in self.queries if q.cache_hit)
        total = len(self.queries)
        doctrine_matched = sum(1 for q in self.queries if q.doctrine_matched)
        coverage = {
            "total_queries": total,
            "cache_hit_rate": cache_hits / total if total else 0.0,
            "doctrine_matched_rate": doctrine_matched / total if total else 0.0,
            "mode_distribution": dict(modes)
        }
        logger.info(f"Coverage report: {coverage}")
        return coverage

    def export_jsonl(self, path: str) -> int:
        path_obj = pathlib.Path(path)
        count = 0
        with path_obj.open("w", encoding="utf-8") as f:
            for q in self.queries:
                f.write(json.dumps(asdict(q)) + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {path}")
        return count

class AuditTrailWriter:
    def __init__(self, base_path: Optional[str] = None):
        if base_path is None:
            base_path = "./audit_trail"
        self.base_path = pathlib.Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def write(self, metrics: QueryMetrics):
        date_str = time.strftime("%Y-%m-%d")
        file_path = self.base_path / f"queries_{date_str}.jsonl"
        entry = asdict(metrics)
        entry["audit_hash"] = self._hash_entry(entry)
        with file_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        logger.debug(f"Audit trail written for query_id={metrics.query_id}")

    def _hash_entry(self, entry: Dict[str, Any]) -> str:
        entry_str = json.dumps(entry, sort_keys=True)
        return hashlib.sha256(entry_str.encode("utf-8")).hexdigest()

COLLECTOR = TelemetryCollector()