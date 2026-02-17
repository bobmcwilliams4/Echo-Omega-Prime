import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Union
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "PRB08"

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
        self.audit_trail: deque = deque(maxlen=maxlen)
        self.query_counter: Counter = Counter()
        self.doctrine_counter: Counter = Counter()
        self.error_counter: Counter = Counter()
        self.latencies: deque = deque(maxlen=maxlen)
        self.coverage: defaultdict = defaultdict(list)
        self.last_export_time = time.time()
        self.lock = None  # Placeholder for thread safety if needed

    def record_query(self, metrics: QueryMetrics):
        self.metrics.append(metrics)
        self.latencies.append(metrics.latency_ms)
        self.query_counter[metrics.query_id] += 1
        self.doctrine_counter['matched' if metrics.doctrine_matched else 'unmatched'] += 1
        self.coverage[metrics.mode].append(metrics.query_id)
        self.audit_trail.append({
            "query_id": metrics.query_id,
            "engine_id": metrics.engine_id,
            "timestamp": metrics.timestamp,
            "latency_ms": metrics.latency_ms,
            "cache_hit": metrics.cache_hit,
            "doctrine_matched": metrics.doctrine_matched,
            "mode": metrics.mode,
            "confidence": metrics.confidence,
            "error": metrics.error
        })
        logger.debug(f"Recorded query: {metrics}")

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "timestamp": time.time()
        }
        self.errors.append(error_entry)
        self.error_counter[error_type] += 1
        logger.error(f"Recorded error: {error_entry}")

    def get_latency_stats(self) -> Dict[str, Union[float, None]]:
        latencies = list(self.latencies)
        if not latencies:
            return dict(avg=None, p50=None, p95=None, p99=None, min=None, max=None)
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = statistics.quantiles(latencies, n=100)[94] if len(latencies) >= 100 else statistics.median(latencies)
        p99 = statistics.quantiles(latencies, n=100)[98] if len(latencies) >= 100 else statistics.median(latencies)
        min_latency = min(latencies)
        max_latency = max(latencies)
        return dict(avg=avg, p50=p50, p95=p95, p99=p99, min=min_latency, max=max_latency)

    def get_doctrine_hit_rate(self) -> float:
        matched = self.doctrine_counter['matched']
        total = matched + self.doctrine_counter['unmatched']
        if total == 0:
            return 0.0
        return matched / total

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        relevant_errors = [e for e in self.errors if e['timestamp'] >= window_start]
        relevant_queries = [m for m in self.metrics if m.timestamp >= window_start]
        num_errors = len(relevant_errors)
        num_queries = len(relevant_queries)
        if num_queries == 0:
            return 0.0
        return num_errors / num_queries

    def queries_last_hour(self) -> int:
        now = time.time()
        window_start = now - 3600
        return sum(1 for m in self.metrics if m.timestamp >= window_start)

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {}
        for mode, queries in self.coverage.items():
            report[mode] = {
                "count": len(queries),
                "unique_queries": len(set(queries))
            }
        return report

    def export_jsonl(self, path: Union[str, pathlib.Path]) -> int:
        path = pathlib.Path(path)
        count = 0
        with path.open("a", encoding="utf-8") as f:
            for entry in self.audit_trail:
                f.write(json.dumps(entry) + "\n")
                count += 1
        logger.info(f"Exported {count} audit trail entries to {path}")
        self.audit_trail.clear()
        self.last_export_time = time.time()
        return count

class AuditTrailWriter:
    def __init__(self, path: Union[str, pathlib.Path]):
        self.path = pathlib.Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def write(self, query_metrics: QueryMetrics):
        entry = {
            "query_id": query_metrics.query_id,
            "engine_id": query_metrics.engine_id,
            "timestamp": query_metrics.timestamp,
            "latency_ms": query_metrics.latency_ms,
            "cache_hit": query_metrics.cache_hit,
            "doctrine_matched": query_metrics.doctrine_matched,
            "mode": query_metrics.mode,
            "confidence": query_metrics.confidence,
            "error": query_metrics.error
        }
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        logger.debug(f"Wrote audit trail entry to {self.path}: {entry}")

COLLECTOR = TelemetryCollector(maxlen=20000)