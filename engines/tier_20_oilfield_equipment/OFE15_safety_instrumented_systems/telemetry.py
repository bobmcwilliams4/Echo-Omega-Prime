import time
import json
import hashlib
import statistics
import pathlib
import dataclasses
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
import collections
from collections import deque, defaultdict
from loguru import logger

ENGINE_ID = "OFE15"

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
        self.queries: deque = deque(maxlen=maxlen)
        self.errors: deque = deque(maxlen=maxlen)
        self._doctrine_hits: int = 0
        self._doctrine_total: int = 0
        self._latencies: deque = deque(maxlen=maxlen)
        self._query_id_map: Dict[str, QueryMetrics] = {}
        self._audit_writer = AuditTrailWriter()
        self._coverage_mode_counter: Dict[str, int] = defaultdict(int)
        self._cache_hits: int = 0
        self._cache_total: int = 0

    def record_query(self, metrics: QueryMetrics):
        self.queries.append(metrics)
        self._query_id_map[metrics.query_id] = metrics
        self._latencies.append(metrics.latency_ms)
        self._doctrine_total += 1
        if metrics.doctrine_matched:
            self._doctrine_hits += 1
        self._coverage_mode_counter[metrics.mode] += 1
        self._cache_total += 1
        if metrics.cache_hit:
            self._cache_hits += 1
        self._audit_writer.write(metrics)
        if metrics.error:
            self.record_error(metrics.error, "Query error", metrics.query_id)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "error_type": error_type,
            "message": message,
            "query_id": query_id
        }
        self.errors.append(error_entry)
        logger.error(f"Error recorded: {error_entry}")

    def get_latency_stats(self) -> dict:
        latencies = list(self._latencies)
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
        lat_sorted = sorted(latencies)
        def percentile(p):
            k = int(round(p * len(lat_sorted) + 0.5)) - 1
            k = max(0, min(k, len(lat_sorted) - 1))
            return lat_sorted[k]
        return {
            "avg": avg,
            "p50": p50,
            "p95": percentile(0.95),
            "p99": percentile(0.99),
            "min": min(latencies),
            "max": max(latencies)
        }

    def get_doctrine_hit_rate(self) -> float:
        if self._doctrine_total == 0:
            return 0.0
        return self._doctrine_hits / self._doctrine_total

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self.errors if e["timestamp"] >= window_start]
        queries_in_window = [q for q in self.queries if q.timestamp >= window_start]
        num_queries = len(queries_in_window)
        if num_queries == 0:
            return 0.0
        return len(errors_in_window) / num_queries

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        return sum(1 for q in self.queries if q.timestamp >= one_hour_ago)

    def get_coverage_report(self) -> dict:
        total = sum(self._coverage_mode_counter.values())
        report = {}
        for mode, count in self._coverage_mode_counter.items():
            report[mode] = {
                "count": count,
                "fraction": count / total if total else 0.0
            }
        report["total"] = total
        report["cache_hit_rate"] = self._cache_hits / self._cache_total if self._cache_total else 0.0
        report["doctrine_hit_rate"] = self.get_doctrine_hit_rate()
        return report

    def export_jsonl(self, path: Any) -> int:
        path = pathlib.Path(path)
        count = 0
        with path.open("w", encoding="utf-8") as f:
            for q in self.queries:
                f.write(json.dumps(dataclasses.asdict(q)) + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {path}")
        return count

class AuditTrailWriter:
    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = pathlib.Path(base_dir) if base_dir else pathlib.Path("audit_trail")
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def write(self, metrics: QueryMetrics):
        # Write a JSONL file per query
        query_hash = hashlib.sha256(metrics.query_id.encode()).hexdigest()[:16]
        fname = f"{metrics.timestamp:.0f}_{query_hash}.jsonl"
        path = self.base_dir / fname
        with path.open("w", encoding="utf-8") as f:
            f.write(json.dumps(dataclasses.asdict(metrics)) + "\n")
        logger.debug(f"Audit trail written: {path}")

COLLECTOR = TelemetryCollector()