import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any, Union
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "PRB04"

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
        self.metrics: deque = deque(maxlen=maxlen)
        self.errors: deque = deque(maxlen=maxlen)
        self.query_id_index: Dict[str, QueryMetrics] = {}
        self.doctrine_hits: int = 0
        self.doctrine_total: int = 0
        self.latency_list: List[float] = []
        self.error_counter: Counter = Counter()
        self.mode_counter: Counter = Counter()
        self.cache_hit_counter: Counter = Counter()
        self.confidence_list: List[float] = []
        self.coverage_counter: Counter = Counter()
        self.last_hour_queries: deque = deque(maxlen=10000)
        self.audit_writer: Optional[AuditTrailWriter] = None

    def record_query(self, metrics: QueryMetrics):
        self.metrics.append(metrics)
        self.query_id_index[metrics.query_id] = metrics
        self.latency_list.append(metrics.latency_ms)
        self.mode_counter[metrics.mode] += 1
        self.cache_hit_counter[metrics.cache_hit] += 1
        self.confidence_list.append(metrics.confidence)
        self.coverage_counter[metrics.mode] += 1
        self.doctrine_total += 1
        if metrics.doctrine_matched:
            self.doctrine_hits += 1
        now = time.time()
        self.last_hour_queries.append((now, metrics.query_id))
        if metrics.error:
            self.record_error("query_error", metrics.error, metrics.query_id)
        if self.audit_writer:
            self.audit_writer.write(metrics)
        logger.debug(f"Recorded query: {metrics.query_id}")

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        err = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "timestamp": time.time()
        }
        self.errors.append(err)
        self.error_counter[error_type] += 1
        logger.error(f"Error recorded: {error_type} - {message} (query_id={query_id})")

    def get_latency_stats(self) -> Dict[str, Any]:
        if not self.latency_list:
            return {
                "avg": None,
                "p50": None,
                "p95": None,
                "p99": None,
                "min": None,
                "max": None
            }
        latencies = sorted(self.latency_list)
        avg = statistics.mean(latencies)
        min_val = latencies[0]
        max_val = latencies[-1]
        p50 = statistics.median(latencies)
        p95 = latencies[int(0.95 * len(latencies)) - 1]
        p99 = latencies[int(0.99 * len(latencies)) - 1]
        return {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_val,
            "max": max_val
        }

    def get_doctrine_hit_rate(self) -> float:
        if self.doctrine_total == 0:
            return 0.0
        return self.doctrine_hits / self.doctrine_total

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        error_count = 0
        query_count = 0
        for ts, qid in self.last_hour_queries:
            if ts >= window_start:
                query_count += 1
                metrics = self.query_id_index.get(qid)
                if metrics and metrics.error:
                    error_count += 1
        if query_count == 0:
            return 0.0
        return error_count / query_count

    def queries_last_hour(self) -> int:
        now = time.time()
        window_start = now - 3600
        return sum(1 for ts, _ in self.last_hour_queries if ts >= window_start)

    def get_coverage_report(self) -> Dict[str, Any]:
        total = sum(self.coverage_counter.values())
        report = {}
        for mode, count in self.coverage_counter.items():
            report[mode] = {
                "count": count,
                "percent": (count / total) * 100 if total else 0
            }
        return report

    def export_jsonl(self, path: Union[str, pathlib.Path]) -> int:
        p = pathlib.Path(path)
        count = 0
        with p.open("w", encoding="utf-8") as f:
            for metrics in self.metrics:
                f.write(json.dumps(asdict(metrics)) + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {str(p)}")
        return count

    def set_audit_writer(self, writer: 'AuditTrailWriter'):
        self.audit_writer = writer

class AuditTrailWriter:
    def __init__(self, path: Union[str, pathlib.Path]):
        self.path = pathlib.Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.file = self.path.open("a", encoding="utf-8")
        self.lock = None  # Placeholder for future thread safety

    def write(self, metrics: QueryMetrics):
        entry = asdict(metrics)
        entry["audit_hash"] = self._hash_entry(entry)
        self.file.write(json.dumps(entry) + "\n")
        self.file.flush()
        logger.debug(f"Audit written for query_id={metrics.query_id}")

    def _hash_entry(self, entry: Dict[str, Any]) -> str:
        s = json.dumps(entry, sort_keys=True)
        return hashlib.sha256(s.encode("utf-8")).hexdigest()

    def close(self):
        self.file.close()

COLLECTOR = TelemetryCollector(maxlen=10000)