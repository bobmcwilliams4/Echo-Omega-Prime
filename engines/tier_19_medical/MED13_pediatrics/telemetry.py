import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict, field
from typing import List, Optional, Dict, Any
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "MED13"

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
        self._doctrine_hits = deque(maxlen=maxlen)
        self._latencies = deque(maxlen=maxlen)
        self._query_id_set = set()
        self._audit_writer = AuditTrailWriter()
        self._lock = None  # Placeholder for future threading.Lock if needed

    def record_query(self, metrics: QueryMetrics):
        if metrics.query_id in self._query_id_set:
            logger.warning(f"Duplicate query_id detected: {metrics.query_id}")
            return
        self._queries.append(metrics)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._query_id_set.add(metrics.query_id)
        if metrics.error:
            self._errors.append({
                "timestamp": metrics.timestamp,
                "error_type": metrics.error,
                "query_id": metrics.query_id
            })
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

    def get_latency_stats(self) -> Dict[str, float]:
        latencies = [m.latency_ms for m in self._queries if m.latency_ms is not None]
        if not latencies:
            return dict(avg=0, p50=0, p95=0, p99=0, min=0, max=0)
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        min_ = min(latencies)
        max_ = max(latencies)
        p50 = statistics.median(latencies)
        p95 = latencies_sorted[int(0.95 * len(latencies_sorted)) - 1]
        p99 = latencies_sorted[int(0.99 * len(latencies_sorted)) - 1]
        return dict(avg=avg, p50=p50, p95=p95, p99=p99, min=min_, max=max_)

    def get_doctrine_hit_rate(self) -> float:
        if not self._doctrine_hits:
            return 0.0
        hits = sum(1 for hit in self._doctrine_hits if hit)
        return hits / len(self._doctrine_hits)

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        queries_in_window = [q for q in self._queries if q.timestamp >= window_start]
        if not queries_in_window:
            return 0.0
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        return len(errors_in_window) / len(queries_in_window)

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        return sum(1 for q in self._queries if q.timestamp >= one_hour_ago)

    def get_coverage_report(self) -> Dict[str, Any]:
        mode_counter = Counter()
        cache_hits = 0
        doctrine_matches = 0
        confidences = []
        for q in self._queries:
            mode_counter[q.mode] += 1
            if q.cache_hit:
                cache_hits += 1
            if q.doctrine_matched:
                doctrine_matches += 1
            confidences.append(q.confidence)
        total = len(self._queries)
        avg_conf = statistics.mean(confidences) if confidences else 0.0
        return {
            "total_queries": total,
            "mode_distribution": dict(mode_counter),
            "cache_hit_rate": cache_hits / total if total else 0.0,
            "doctrine_match_rate": doctrine_matches / total if total else 0.0,
            "avg_confidence": avg_conf
        }

    def export_jsonl(self, path: str) -> int:
        path_obj = pathlib.Path(path)
        count = 0
        with path_obj.open("w", encoding="utf-8") as f:
            for q in self._queries:
                f.write(json.dumps(asdict(q)) + "\n")
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
        day = time.strftime("%Y-%m-%d", time.localtime(metrics.timestamp))
        file_path = self.base_dir / f"{ENGINE_ID}_queries_{day}.jsonl"
        entry = asdict(metrics)
        try:
            with file_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            logger.error(f"Failed to write audit trail: {e}")

COLLECTOR = TelemetryCollector()