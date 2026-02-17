import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any, Deque
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "MECH13"

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

    def to_dict(self) -> dict:
        return asdict(self)

class TelemetryCollector:
    def __init__(self, maxlen: int = 10000):
        self.queries: Deque[QueryMetrics] = deque(maxlen=maxlen)
        self.errors: Deque[Dict[str, Any]] = deque(maxlen=maxlen)
        self.audit_trail_writer = AuditTrailWriter()
        self._doctrine_hits = 0
        self._doctrine_total = 0
        self._lock = None  # Placeholder for threading.Lock if needed

    def record_query(self, metrics: QueryMetrics):
        logger.debug(f"Recording query: {metrics.query_id}")
        self.queries.append(metrics)
        self.audit_trail_writer.write(metrics)
        if metrics.doctrine_matched is not None:
            self._doctrine_total += 1
            if metrics.doctrine_matched:
                self._doctrine_hits += 1

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
        }
        logger.error(f"Error recorded: {error_entry}")
        self.errors.append(error_entry)

    def get_latency_stats(self) -> dict:
        latencies = [q.latency_ms for q in self.queries if q.latency_ms is not None]
        if not latencies:
            return {
                "avg": None,
                "p50": None,
                "p95": None,
                "p99": None,
                "min": None,
                "max": None
            }
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)
        min_ = min(latencies)
        max_ = max(latencies)
        return {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_,
            "max": max_
        }

    def _percentile(self, data: List[float], percentile: float) -> float:
        if not data:
            return None
        size = len(data)
        data = sorted(data)
        k = (size - 1) * (percentile / 100)
        f = int(k)
        c = min(f + 1, size - 1)
        if f == c:
            return data[int(k)]
        d0 = data[f] * (c - k)
        d1 = data[c] * (k - f)
        return d0 + d1

    def get_doctrine_hit_rate(self) -> float:
        if self._doctrine_total == 0:
            return 0.0
        return self._doctrine_hits / self._doctrine_total

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        error_count = sum(1 for e in self.errors if e["timestamp"] >= window_start)
        query_count = sum(1 for q in self.queries if q.timestamp >= window_start)
        if query_count == 0:
            return 0.0
        return error_count / query_count

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self.queries if q.timestamp >= one_hour_ago)
        return count

    def get_coverage_report(self) -> dict:
        mode_counter = Counter()
        cache_hit_counter = Counter()
        doctrine_counter = Counter()
        confidence_buckets = defaultdict(int)
        total = 0
        for q in self.queries:
            total += 1
            mode_counter[q.mode] += 1
            cache_hit_counter[q.cache_hit] += 1
            doctrine_counter[q.doctrine_matched] += 1
            bucket = self._confidence_bucket(q.confidence)
            confidence_buckets[bucket] += 1
        return {
            "total_queries": total,
            "modes": dict(mode_counter),
            "cache_hit": dict(cache_hit_counter),
            "doctrine_matched": dict(doctrine_counter),
            "confidence_buckets": dict(confidence_buckets)
        }

    def _confidence_bucket(self, confidence: float) -> str:
        if confidence is None:
            return "unknown"
        if confidence >= 0.95:
            return "0.95-1.0"
        elif confidence >= 0.90:
            return "0.90-0.95"
        elif confidence >= 0.80:
            return "0.80-0.90"
        elif confidence >= 0.70:
            return "0.70-0.80"
        else:
            return "<0.70"

    def export_jsonl(self, path: str) -> int:
        p = pathlib.Path(path)
        count = 0
        with p.open("w", encoding="utf-8") as f:
            for q in self.queries:
                f.write(json.dumps(q.to_dict()) + "\n")
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
        file_path = self.base_dir / f"{date_str}.jsonl"
        entry = metrics.to_dict()
        entry["audit_hash"] = self._hash_entry(entry)
        try:
            with file_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
            logger.debug(f"Audit entry written for query {metrics.query_id}")
        except Exception as e:
            logger.error(f"Failed to write audit entry: {e}")

    def _hash_entry(self, entry: dict) -> str:
        # Hash the JSON representation for audit integrity
        s = json.dumps(entry, sort_keys=True)
        return hashlib.sha256(s.encode("utf-8")).hexdigest()

COLLECTOR = TelemetryCollector()