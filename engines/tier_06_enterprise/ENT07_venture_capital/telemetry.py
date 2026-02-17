import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict, field
from typing import Optional, List, Dict, Any
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "ENT07"

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
        self._queries = deque(maxlen=maxlen)
        self._errors = deque(maxlen=maxlen)
        self._lock = None  # Placeholder for future threading.Lock if needed
        self._doctrine_counter = Counter()
        self._cache_counter = Counter()
        self._mode_counter = Counter()
        self._confidence_values = []
        self._coverage_keys = set()
        self._audit_writer = AuditTrailWriter()
        logger.info("TelemetryCollector initialized with maxlen={}", maxlen)

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._doctrine_counter[metrics.doctrine_matched] += 1
        self._cache_counter[metrics.cache_hit] += 1
        self._mode_counter[metrics.mode] += 1
        self._confidence_values.append(metrics.confidence)
        self._coverage_keys.add(metrics.mode)
        self._audit_writer.write(metrics)
        logger.debug("Recorded query: {}", metrics)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
        }
        self._errors.append(error_entry)
        logger.error("Error recorded: {}", error_entry)

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = [q.latency_ms for q in self._queries if q.latency_ms is not None]
        if not latencies:
            logger.warning("No latency data available.")
            return {
                "avg": None, "p50": None, "p95": None, "p99": None,
                "min": None, "max": None
            }
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies_sorted)
        p95 = self._percentile(latencies_sorted, 95)
        p99 = self._percentile(latencies_sorted, 99)
        min_v = latencies_sorted[0]
        max_v = latencies_sorted[-1]
        stats = {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_v,
            "max": max_v
        }
        logger.debug("Latency stats: {}", stats)
        return stats

    def get_doctrine_hit_rate(self) -> float:
        total = sum(self._doctrine_counter.values())
        if total == 0:
            logger.warning("No doctrine data to compute hit rate.")
            return 0.0
        hit_rate = self._doctrine_counter[True] / total
        logger.debug("Doctrine hit rate: {}", hit_rate)
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        total_queries = sum(1 for q in self._queries if q.timestamp >= window_start)
        total_errors = sum(1 for e in self._errors if e["timestamp"] >= window_start)
        if total_queries == 0:
            logger.warning("No queries in the last {} hours.", window_hours)
            return 0.0
        error_rate = total_errors / total_queries
        logger.debug("Error rate (window_hours={}): {}", window_hours, error_rate)
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= one_hour_ago)
        logger.debug("Queries in the last hour: {}", count)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        mode_counts = dict(self._mode_counter)
        total = sum(mode_counts.values())
        coverage = {mode: count / total if total else 0.0 for mode, count in mode_counts.items()}
        avg_confidence = statistics.mean(self._confidence_values) if self._confidence_values else None
        report = {
            "mode_coverage": coverage,
            "avg_confidence": avg_confidence,
            "total_modes": len(self._coverage_keys),
            "modes": list(self._coverage_keys)
        }
        logger.debug("Coverage report: {}", report)
        return report

    def export_jsonl(self, path: str) -> int:
        path_obj = pathlib.Path(path)
        count = 0
        with path_obj.open("w", encoding="utf-8") as f:
            for q in self._queries:
                f.write(json.dumps(asdict(q)) + "\n")
                count += 1
        logger.info("Exported {} queries to {}", count, path)
        return count

    @staticmethod
    def _percentile(sorted_list: List[float], percentile: float) -> float:
        if not sorted_list:
            return None
        k = (len(sorted_list) - 1) * percentile / 100
        f = int(k)
        c = min(f + 1, len(sorted_list) - 1)
        if f == c:
            return sorted_list[int(k)]
        d0 = sorted_list[f] * (c - k)
        d1 = sorted_list[c] * (k - f)
        return d0 + d1

class AuditTrailWriter:
    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = pathlib.Path(base_dir) if base_dir else pathlib.Path("./audit_trail")
        self.base_dir.mkdir(parents=True, exist_ok=True)
        logger.info("AuditTrailWriter initialized at {}", self.base_dir)

    def write(self, metrics: QueryMetrics):
        date_str = time.strftime("%Y-%m-%d")
        file_path = self.base_dir / f"{ENGINE_ID}_audit_{date_str}.jsonl"
        entry = asdict(metrics)
        entry["audit_hash"] = self._hash_entry(entry)
        with file_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        logger.debug("Audit trail written for query_id={}", metrics.query_id)

    @staticmethod
    def _hash_entry(entry: Dict[str, Any]) -> str:
        # Remove audit_hash if present to avoid recursion
        entry = dict(entry)
        entry.pop("audit_hash", None)
        entry_bytes = json.dumps(entry, sort_keys=True).encode("utf-8")
        return hashlib.sha256(entry_bytes).hexdigest()

COLLECTOR = TelemetryCollector()