import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional, Any, Deque
import collections
from loguru import logger

ENGINE_ID = "MECH12"

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
    def __init__(self):
        self._queries: Deque[QueryMetrics] = collections.deque(maxlen=10000)
        self._errors: Deque[Dict[str, Any]] = collections.deque(maxlen=2000)
        self._doctrine_hits: int = 0
        self._total_queries: int = 0
        self._cache_hits: int = 0
        self._latencies: List[float] = []
        self._mode_counter: collections.Counter = collections.Counter()
        self._confidence_scores: List[float] = []
        self._coverage: Dict[str, set] = collections.defaultdict(set)
        self._audit_writer = AuditTrailWriter()
        self._query_id_set: set = set()

    def record_query(self, metrics: QueryMetrics):
        if metrics.query_id in self._query_id_set:
            logger.warning(f"Duplicate query_id detected: {metrics.query_id}")
            return
        self._query_id_set.add(metrics.query_id)
        self._queries.append(metrics)
        self._total_queries += 1
        if metrics.cache_hit:
            self._cache_hits += 1
        if metrics.doctrine_matched:
            self._doctrine_hits += 1
        self._latencies.append(metrics.latency_ms)
        self._mode_counter[metrics.mode] += 1
        self._confidence_scores.append(metrics.confidence)
        self._coverage[metrics.mode].add(metrics.query_id)
        self._audit_writer.write(metrics)
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
        self._errors.append(error_entry)
        logger.error(f"Error recorded: {error_entry}")

    def get_latency_stats(self) -> Dict[str, float]:
        if not self._latencies:
            return {"avg": 0, "p50": 0, "p95": 0, "p99": 0, "min": 0, "max": 0}
        lats = sorted(self._latencies)
        avg = statistics.mean(lats)
        min_ = lats[0]
        max_ = lats[-1]
        p50 = lats[int(0.5 * len(lats))]
        p95 = lats[int(0.95 * len(lats)) - 1]
        p99 = lats[int(0.99 * len(lats)) - 1]
        return {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_,
            "max": max_
        }

    def get_doctrine_hit_rate(self) -> float:
        if self._total_queries == 0:
            return 0.0
        return self._doctrine_hits / self._total_queries

    def get_error_rate(self, window_hours: float) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        queries_in_window = [q for q in self._queries if q.timestamp >= window_start]
        if not queries_in_window:
            return 0.0
        return len(errors_in_window) / len(queries_in_window)

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        return sum(1 for q in self._queries if q.timestamp >= one_hour_ago)

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {}
        for mode, queries in self._coverage.items():
            report[mode] = {
                "unique_queries": len(queries),
                "total_queries": self._mode_counter[mode]
            }
        if self._confidence_scores:
            report["confidence"] = {
                "avg": statistics.mean(self._confidence_scores),
                "min": min(self._confidence_scores),
                "max": max(self._confidence_scores)
            }
        else:
            report["confidence"] = {"avg": 0, "min": 0, "max": 0}
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
        if base_dir is None:
            base_dir = "./audit_trails"
        self.base_dir = pathlib.Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def write(self, metrics: QueryMetrics):
        date_str = time.strftime("%Y-%m-%d", time.localtime(metrics.timestamp))
        file_path = self.base_dir / f"audit_{date_str}.jsonl"
        entry = asdict(metrics)
        entry["audit_hash"] = self._hash_entry(entry)
        try:
            with file_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            logger.error(f"Failed to write audit trail: {e}")

    def _hash_entry(self, entry: Dict[str, Any]) -> str:
        entry_str = json.dumps(entry, sort_keys=True)
        return hashlib.sha256(entry_str.encode("utf-8")).hexdigest()

COLLECTOR = TelemetryCollector()