import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "SYN08"

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
    def __init__(self, maxlen=10000):
        self.queries = deque(maxlen=maxlen)
        self.errors = deque(maxlen=maxlen)
        self.audit_trail = []
        self.lock = None  # Placeholder for thread safety if needed
        self._latencies = deque(maxlen=maxlen)
        self._doctrine_matches = deque(maxlen=maxlen)
        self._cache_hits = deque(maxlen=maxlen)
        self._modes = deque(maxlen=maxlen)
        self._confidences = deque(maxlen=maxlen)
        self._query_timestamps = deque(maxlen=maxlen)
        self._query_ids = set()
        self._error_types = deque(maxlen=maxlen)
        self._error_timestamps = deque(maxlen=maxlen)
        self._doctrine_counter = Counter()
        self._mode_counter = Counter()
        self._coverage = defaultdict(set)  # mode -> set of query_ids

    def record_query(self, metrics: QueryMetrics):
        logger.debug(f"Recording query: {metrics}")
        self.queries.append(metrics)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_matches.append(metrics.doctrine_matched)
        self._cache_hits.append(metrics.cache_hit)
        self._modes.append(metrics.mode)
        self._confidences.append(metrics.confidence)
        self._query_timestamps.append(metrics.timestamp)
        self._query_ids.add(metrics.query_id)
        self._doctrine_counter[metrics.doctrine_matched] += 1
        self._mode_counter[metrics.mode] += 1
        self._coverage[metrics.mode].add(metrics.query_id)
        if metrics.error:
            self.record_error(metrics.error, "Query error", metrics.query_id)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "error_type": error_type,
            "message": message,
            "query_id": query_id
        }
        logger.error(f"Recording error: {error_entry}")
        self.errors.append(error_entry)
        self._error_types.append(error_type)
        self._error_timestamps.append(error_entry["timestamp"])

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = list(self._latencies)
        if not latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)
        min_v = min(latencies)
        max_v = max(latencies)
        logger.debug(f"Latency stats: avg={avg}, p50={p50}, p95={p95}, p99={p99}, min={min_v}, max={max_v}")
        return {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_v,
            "max": max_v
        }

    def _percentile(self, data: List[float], percentile: float) -> float:
        if not data:
            return None
        data = sorted(data)
        k = (len(data) - 1) * (percentile / 100)
        f = int(k)
        c = min(f + 1, len(data) - 1)
        if f == c:
            return data[int(k)]
        d0 = data[f] * (c - k)
        d1 = data[c] * (k - f)
        return d0 + d1

    def get_doctrine_hit_rate(self) -> float:
        total = len(self._doctrine_matches)
        if total == 0:
            return 0.0
        hits = sum(1 for m in self._doctrine_matches if m)
        hit_rate = hits / total
        logger.debug(f"Doctrine hit rate: {hit_rate} ({hits}/{total})")
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        error_count = sum(1 for t in self._error_timestamps if t >= window_start)
        query_count = sum(1 for t in self._query_timestamps if t >= window_start)
        if query_count == 0:
            return 0.0
        error_rate = error_count / query_count
        logger.debug(f"Error rate in last {window_hours}h: {error_rate} ({error_count}/{query_count})")
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for t in self._query_timestamps if t >= one_hour_ago)
        logger.debug(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {}
        for mode, query_ids in self._coverage.items():
            report[mode] = {
                "unique_queries": len(query_ids),
                "total_queries": self._mode_counter[mode]
            }
        logger.debug(f"Coverage report: {report}")
        return report

    def export_jsonl(self, path: str) -> int:
        p = pathlib.Path(path)
        count = 0
        with p.open("w", encoding="utf-8") as f:
            for q in self.queries:
                f.write(json.dumps(asdict(q)) + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {path}")
        return count

class AuditTrailWriter:
    def __init__(self, base_path: str = "./audit_trail"):
        self.base_path = pathlib.Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def write(self, query_metrics: QueryMetrics, extra: Optional[Dict[str, Any]] = None) -> str:
        data = asdict(query_metrics)
        if extra:
            data.update(extra)
        # Hash query_id for filename safety
        qid_hash = hashlib.sha256(query_metrics.query_id.encode()).hexdigest()[:16]
        ts = int(query_metrics.timestamp)
        filename = f"{ENGINE_ID}_{qid_hash}_{ts}.jsonl"
        path = self.base_path / filename
        with path.open("w", encoding="utf-8") as f:
            f.write(json.dumps(data) + "\n")
        logger.info(f"Wrote audit trail: {path}")
        return str(path)

COLLECTOR = TelemetryCollector()
AUDIT_TRAIL_WRITER = AuditTrailWriter()