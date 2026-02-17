import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any, Tuple
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "FRAC10"

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
    def __init__(self, max_queries: int = 10000, max_errors: int = 5000):
        self.queries: deque = deque(maxlen=max_queries)
        self.errors: deque = deque(maxlen=max_errors)
        self.query_index: Dict[str, QueryMetrics] = {}
        self.doctrine_counter: Counter = Counter()
        self.cache_counter: Counter = Counter()
        self.mode_counter: Counter = Counter()
        self.confidence_hist: List[float] = []
        self.latency_hist: List[float] = []
        self.coverage_counter: Counter = Counter()
        self.audit_writer = AuditTrailWriter()
        logger.info(f"TelemetryCollector initialized for engine {ENGINE_ID}")

    def record_query(self, metrics: QueryMetrics):
        self.queries.append(metrics)
        self.query_index[metrics.query_id] = metrics
        self.doctrine_counter[metrics.doctrine_matched] += 1
        self.cache_counter[metrics.cache_hit] += 1
        self.mode_counter[metrics.mode] += 1
        self.confidence_hist.append(metrics.confidence)
        self.latency_hist.append(metrics.latency_ms)
        self.coverage_counter[(metrics.mode, metrics.doctrine_matched)] += 1
        self.audit_writer.write(metrics)
        logger.debug(f"Recorded query: {metrics.query_id}")

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "error_type": error_type,
            "message": message,
            "timestamp": time.time(),
            "query_id": query_id,
            "engine_id": ENGINE_ID
        }
        self.errors.append(error_entry)
        logger.warning(f"Error recorded: {error_type} for query {query_id}")

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = [q.latency_ms for q in self.queries if q.latency_ms is not None]
        if not latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = latencies_sorted[int(0.95 * len(latencies_sorted)) - 1]
        p99 = latencies_sorted[int(0.99 * len(latencies_sorted)) - 1]
        min_latency = min(latencies)
        max_latency = max(latencies)
        logger.info(f"Latency stats computed: avg={avg}, p50={p50}, p95={p95}, p99={p99}, min={min_latency}, max={max_latency}")
        return {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_latency,
            "max": max_latency
        }

    def get_doctrine_hit_rate(self) -> float:
        total = sum(self.doctrine_counter.values())
        hits = self.doctrine_counter.get(True, 0)
        hit_rate = hits / total if total > 0 else 0.0
        logger.info(f"Doctrine hit rate: {hit_rate} ({hits}/{total})")
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        error_count = sum(1 for e in self.errors if e["timestamp"] >= window_start)
        query_count = sum(1 for q in self.queries if q.timestamp >= window_start)
        error_rate = error_count / query_count if query_count > 0 else 0.0
        logger.info(f"Error rate in last {window_hours}h: {error_rate} ({error_count}/{query_count})")
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self.queries if q.timestamp >= one_hour_ago)
        logger.info(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {}
        total_queries = len(self.queries)
        for (mode, doctrine_matched), count in self.coverage_counter.items():
            key = f"{mode}|{'doctrine' if doctrine_matched else 'no_doctrine'}"
            report[key] = {
                "count": count,
                "percent": (count / total_queries) * 100 if total_queries > 0 else 0.0
            }
        logger.info(f"Coverage report generated: {report}")
        return report

    def export_jsonl(self, path: str) -> int:
        p = pathlib.Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        count = 0
        with p.open("w", encoding="utf-8") as f:
            for q in self.queries:
                f.write(json.dumps(asdict(q)) + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {path}")
        return count

class AuditTrailWriter:
    def __init__(self, base_path: Optional[str] = None):
        self.base_path = base_path or "./audit_trail"
        pathlib.Path(self.base_path).mkdir(parents=True, exist_ok=True)
        logger.info(f"AuditTrailWriter initialized at {self.base_path}")

    def write(self, metrics: QueryMetrics):
        filename = self._filename_for_query(metrics.query_id)
        path = pathlib.Path(self.base_path) / filename
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(metrics)) + "\n")
        logger.debug(f"Audit trail written for query {metrics.query_id} at {path}")

    def _filename_for_query(self, query_id: str) -> str:
        h = hashlib.sha256(query_id.encode()).hexdigest()[:12]
        return f"{ENGINE_ID}_{h}.jsonl"

COLLECTOR = TelemetryCollector()