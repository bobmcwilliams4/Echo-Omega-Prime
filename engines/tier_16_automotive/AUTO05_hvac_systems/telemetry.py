import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict, field
from typing import List, Optional, Dict, Any, Deque
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "AUTO05"

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
        self.latencies: Deque[float] = deque(maxlen=maxlen)
        self.doctrine_matches: Deque[bool] = deque(maxlen=maxlen)
        self.cache_hits: Deque[bool] = deque(maxlen=maxlen)
        self.modes: Deque[str] = deque(maxlen=maxlen)
        self.confidences: Deque[float] = deque(maxlen=maxlen)
        self.audit_writer = AuditTrailWriter()
        self._query_id_set = set()
        self._lock = None  # Placeholder for threading.Lock if needed

    def record_query(self, metrics: QueryMetrics):
        if metrics.query_id in self._query_id_set:
            logger.warning(f"Duplicate query_id detected: {metrics.query_id}")
            return
        self.queries.append(metrics)
        self.latencies.append(metrics.latency_ms)
        self.doctrine_matches.append(metrics.doctrine_matched)
        self.cache_hits.append(metrics.cache_hit)
        self.modes.append(metrics.mode)
        self.confidences.append(metrics.confidence)
        self._query_id_set.add(metrics.query_id)
        self.audit_writer.write(metrics)
        logger.debug(f"Recorded query: {metrics}")

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "engine_id": ENGINE_ID,
            "error_type": error_type,
            "message": message,
            "query_id": query_id
        }
        self.errors.append(error_entry)
        logger.error(f"Error recorded: {error_entry}")

    def get_latency_stats(self) -> Dict[str, float]:
        latencies = list(self.latencies)
        if not latencies:
            return {"avg": 0, "p50": 0, "p95": 0, "p99": 0, "min": 0, "max": 0}
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)
        min_v = min(latencies)
        max_v = max(latencies)
        logger.info(f"Latency stats: avg={avg}, p50={p50}, p95={p95}, p99={p99}, min={min_v}, max={max_v}")
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
            return 0.0
        size = len(data)
        data_sorted = sorted(data)
        k = (size - 1) * (percentile / 100)
        f = int(k)
        c = min(f + 1, size - 1)
        if f == c:
            return data_sorted[int(k)]
        d0 = data_sorted[f] * (c - k)
        d1 = data_sorted[c] * (k - f)
        return d0 + d1

    def get_doctrine_hit_rate(self) -> float:
        matches = list(self.doctrine_matches)
        if not matches:
            return 0.0
        hit_rate = sum(matches) / len(matches)
        logger.info(f"Doctrine hit rate: {hit_rate}")
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        error_count = sum(1 for e in self.errors if e["timestamp"] >= window_start)
        query_count = sum(1 for q in self.queries if q.timestamp >= window_start)
        if query_count == 0:
            return 0.0
        error_rate = error_count / query_count
        logger.info(f"Error rate in last {window_hours}h: {error_rate}")
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self.queries if q.timestamp >= one_hour_ago)
        logger.info(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        modes = list(self.modes)
        mode_counts = Counter(modes)
        doctrine_matches = list(self.doctrine_matches)
        cache_hits = list(self.cache_hits)
        confidences = list(self.confidences)
        total = len(modes)
        report = {
            "total_queries": total,
            "mode_distribution": dict(mode_counts),
            "doctrine_matched": sum(doctrine_matches),
            "doctrine_miss": total - sum(doctrine_matches),
            "cache_hits": sum(cache_hits),
            "cache_misses": total - sum(cache_hits),
            "avg_confidence": statistics.mean(confidences) if confidences else 0.0,
            "min_confidence": min(confidences) if confidences else 0.0,
            "max_confidence": max(confidences) if confidences else 0.0,
        }
        logger.info(f"Coverage report: {report}")
        return report

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
    def __init__(self, audit_dir: Optional[str] = None):
        self.audit_dir = pathlib.Path(audit_dir or "./audit_trail")
        self.audit_dir.mkdir(parents=True, exist_ok=True)

    def write(self, metrics: QueryMetrics):
        ts = int(metrics.timestamp)
        query_hash = hashlib.sha256(metrics.query_id.encode()).hexdigest()[:16]
        filename = f"{ts}_{metrics.engine_id}_{query_hash}.jsonl"
        path = self.audit_dir / filename
        try:
            with path.open("w", encoding="utf-8") as f:
                f.write(json.dumps(asdict(metrics)) + "\n")
            logger.debug(f"Audit trail written: {path}")
        except Exception as e:
            logger.error(f"Failed to write audit trail: {e}")

COLLECTOR = TelemetryCollector()