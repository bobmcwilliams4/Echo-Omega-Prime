import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any, Union
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "CHEM12"

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
    def __init__(self, engine_id: str, maxlen: int = 10000):
        self.engine_id = engine_id
        self.metrics: deque = deque(maxlen=maxlen)
        self.errors: deque = deque(maxlen=maxlen)
        self.audit_trail_writer = AuditTrailWriter()
        self._query_counter = Counter()
        self._doctrine_counter = Counter()
        self._error_counter = Counter()
        self._coverage_counter = defaultdict(set)
        self._last_hour_queries = deque()
        self._lock = None  # Placeholder for threading.Lock if needed

    def record_query(self, metrics: QueryMetrics):
        self.metrics.append(metrics)
        self._query_counter['total'] += 1
        if metrics.doctrine_matched:
            self._doctrine_counter['matched'] += 1
        else:
            self._doctrine_counter['unmatched'] += 1
        if metrics.error:
            self._error_counter[metrics.error] += 1
        self._coverage_counter[metrics.mode].add(metrics.query_id)
        now = time.time()
        self._last_hour_queries.append((now, metrics.query_id))
        self._prune_last_hour_queries(now)
        self.audit_trail_writer.write(metrics)
        logger.debug(f"Recorded query: {metrics}")

    def record_error(self, error_type: str, message: str, query_id: str):
        error_entry = {
            "timestamp": time.time(),
            "engine_id": self.engine_id,
            "error_type": error_type,
            "message": message,
            "query_id": query_id
        }
        self.errors.append(error_entry)
        self._error_counter[error_type] += 1
        logger.error(f"Error recorded: {error_entry}")

    def get_latency_stats(self) -> Dict[str, Union[float, None]]:
        latencies = [m.latency_ms for m in self.metrics if m.latency_ms is not None]
        if not latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = latencies_sorted[int(0.95 * len(latencies_sorted)) - 1]
        p99 = latencies_sorted[int(0.99 * len(latencies_sorted)) - 1]
        min_latency = min(latencies)
        max_latency = max(latencies)
        logger.info(f"Latency stats: avg={avg}, p50={p50}, p95={p95}, p99={p99}, min={min_latency}, max={max_latency}")
        return {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_latency,
            "max": max_latency
        }

    def get_doctrine_hit_rate(self) -> float:
        total = self._doctrine_counter['matched'] + self._doctrine_counter['unmatched']
        if total == 0:
            return 0.0
        hit_rate = self._doctrine_counter['matched'] / total
        logger.info(f"Doctrine hit rate: {hit_rate}")
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        error_count = sum(1 for e in self.errors if e["timestamp"] >= window_start)
        query_count = sum(1 for t, _ in self._last_hour_queries if t >= window_start)
        if query_count == 0:
            return 0.0
        error_rate = error_count / query_count
        logger.info(f"Error rate (last {window_hours}h): {error_rate}")
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        self._prune_last_hour_queries(now)
        count = len(self._last_hour_queries)
        logger.info(f"Queries last hour: {count}")
        return count

    def _prune_last_hour_queries(self, now: float):
        one_hour_ago = now - 3600
        while self._last_hour_queries and self._last_hour_queries[0][0] < one_hour_ago:
            self._last_hour_queries.popleft()

    def get_coverage_report(self) -> Dict[str, Any]:
        coverage = {}
        for mode, query_ids in self._coverage_counter.items():
            coverage[mode] = len(query_ids)
        total_queries = self._query_counter['total']
        coverage_percent = {mode: (count / total_queries if total_queries else 0.0) for mode, count in coverage.items()}
        logger.info(f"Coverage report: {coverage_percent}")
        return {
            "coverage_count": coverage,
            "coverage_percent": coverage_percent,
            "total_queries": total_queries
        }

    def export_jsonl(self, path: Union[str, pathlib.Path]) -> int:
        path = pathlib.Path(path)
        count = 0
        with path.open('w', encoding='utf-8') as f:
            for metric in self.metrics:
                f.write(json.dumps(asdict(metric)) + '\n')
                count += 1
        logger.info(f"Exported {count} metrics to {path}")
        return count

class AuditTrailWriter:
    def __init__(self, base_dir: Union[str, pathlib.Path] = "audit_trail"):
        self.base_dir = pathlib.Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def write(self, metrics: QueryMetrics):
        query_hash = hashlib.sha256(metrics.query_id.encode()).hexdigest()
        filename = f"{metrics.engine_id}_{query_hash}.jsonl"
        filepath = self.base_dir / filename
        entry = asdict(metrics)
        with filepath.open('a', encoding='utf-8') as f:
            f.write(json.dumps(entry) + '\n')
        logger.debug(f"Audit trail written for query_id={metrics.query_id} at {filepath}")

COLLECTOR = TelemetryCollector(engine_id=ENGINE_ID)