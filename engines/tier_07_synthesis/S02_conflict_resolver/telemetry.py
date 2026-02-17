import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict, field
from typing import List, Optional, Dict, Any, Deque
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "S02"

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
        self._doctrine_counts = Counter()
        self._cache_hits = 0
        self._cache_total = 0
        self._lock = None  # Placeholder for threading.Lock if needed

    def record_query(self, metrics: QueryMetrics):
        self.queries.append(metrics)
        self.audit_writer.write(metrics)
        if metrics.doctrine_matched:
            self._doctrine_counts['matched'] += 1
        else:
            self._doctrine_counts['missed'] += 1
        if metrics.cache_hit:
            self._cache_hits += 1
        self._cache_total += 1

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "engine_id": ENGINE_ID
        }
        self.errors.append(error_entry)
        logger.error(f"[{ENGINE_ID}] Error ({error_type}): {message} (query_id={query_id})")
        self.audit_writer.write_error(error_entry)

    def get_latency_stats(self) -> Dict[str, float]:
        latencies = [q.latency_ms for q in self.queries if q.latency_ms is not None]
        if not latencies:
            return {"avg": 0, "p50": 0, "p95": 0, "p99": 0, "min": 0, "max": 0}
        latencies.sort()
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = latencies[int(0.95 * len(latencies)) - 1]
        p99 = latencies[int(0.99 * len(latencies)) - 1]
        min_v = latencies[0]
        max_v = latencies[-1]
        return {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_v,
            "max": max_v
        }

    def get_doctrine_hit_rate(self) -> float:
        total = self._doctrine_counts['matched'] + self._doctrine_counts['missed']
        if total == 0:
            return 0.0
        return self._doctrine_counts['matched'] / total

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        queries_in_window = [q for q in self.queries if q.timestamp >= window_start]
        errors_in_window = [e for e in self.errors if e['timestamp'] >= window_start]
        total = len(queries_in_window)
        if total == 0:
            return 0.0
        return len(errors_in_window) / total

    def queries_last_hour(self) -> int:
        now = time.time()
        window_start = now - 3600
        return sum(1 for q in self.queries if q.timestamp >= window_start)

    def get_coverage_report(self) -> Dict[str, Any]:
        mode_counter = Counter(q.mode for q in self.queries)
        doctrine_matched = sum(1 for q in self.queries if q.doctrine_matched)
        doctrine_total = len(self.queries)
        cache_hits = self._cache_hits
        cache_total = self._cache_total
        avg_confidence = statistics.mean([q.confidence for q in self.queries if q.confidence is not None]) if self.queries else 0.0
        return {
            "total_queries": doctrine_total,
            "doctrine_matched": doctrine_matched,
            "doctrine_coverage": doctrine_matched / doctrine_total if doctrine_total else 0.0,
            "cache_hit_rate": cache_hits / cache_total if cache_total else 0.0,
            "mode_distribution": dict(mode_counter),
            "avg_confidence": avg_confidence
        }

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
    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = pathlib.Path(base_dir) if base_dir else pathlib.Path("audit_trail")
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.query_audit_path = self.base_dir / "queries.jsonl"
        self.error_audit_path = self.base_dir / "errors.jsonl"
        self._query_file = None
        self._error_file = None

    def write(self, metrics: QueryMetrics):
        entry = asdict(metrics)
        entry['audit_timestamp'] = time.time()
        line = json.dumps(entry)
        with self.query_audit_path.open("a", encoding="utf-8") as f:
            f.write(line + "\n")

    def write_error(self, error_entry: Dict[str, Any]):
        error_entry = dict(error_entry)
        error_entry['audit_timestamp'] = time.time()
        line = json.dumps(error_entry)
        with self.error_audit_path.open("a", encoding="utf-8") as f:
            f.write(line + "\n")

COLLECTOR = TelemetryCollector()