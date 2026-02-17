import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Union
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "OFE13"

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
    def __init__(self, engine_id: str = ENGINE_ID, max_queries: int = 10000, max_errors: int = 1000):
        self.engine_id = engine_id
        self._queries: deque = deque(maxlen=max_queries)
        self._errors: deque = deque(maxlen=max_errors)
        self._query_counter: Counter = Counter()
        self._doctrine_counter: Counter = Counter()
        self._cache_counter: Counter = Counter()
        self._mode_counter: Counter = Counter()
        self._confidence_values: List[float] = []
        self._coverage_data: Dict[str, set] = defaultdict(set)
        self._audit_writer = AuditTrailWriter()
        logger.info(f"TelemetryCollector initialized for engine_id={engine_id}")

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._query_counter['total'] += 1
        self._doctrine_counter['matched' if metrics.doctrine_matched else 'unmatched'] += 1
        self._cache_counter['hit' if metrics.cache_hit else 'miss'] += 1
        self._mode_counter[metrics.mode] += 1
        self._confidence_values.append(metrics.confidence)
        self._coverage_data[metrics.mode].add(metrics.query_id)
        self._audit_writer.write(metrics)
        logger.debug(f"Recorded query: {metrics.query_id}")

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "timestamp": time.time(),
            "engine_id": self.engine_id
        }
        self._errors.append(error_entry)
        self._query_counter['errors'] += 1
        logger.warning(f"Error recorded: {error_type} for query {query_id}")

    def get_latency_stats(self) -> Dict[str, Union[float, None]]:
        latencies = [q.latency_ms for q in self._queries if q.latency_ms is not None]
        if not latencies:
            return dict(avg=None, p50=None, p95=None, p99=None, min=None, max=None)
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        min_latency = min(latencies)
        max_latency = max(latencies)
        p50 = statistics.median(latencies)
        p95 = latencies_sorted[int(len(latencies_sorted) * 0.95) - 1] if len(latencies_sorted) >= 1 else None
        p99 = latencies_sorted[int(len(latencies_sorted) * 0.99) - 1] if len(latencies_sorted) >= 1 else None
        return dict(
            avg=avg,
            p50=p50,
            p95=p95,
            p99=p99,
            min=min_latency,
            max=max_latency
        )

    def get_doctrine_hit_rate(self) -> float:
        matched = self._doctrine_counter['matched']
        total = matched + self._doctrine_counter['unmatched']
        if total == 0:
            return 0.0
        return matched / total

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        error_count = sum(1 for e in self._errors if e['timestamp'] >= window_start)
        query_count = sum(1 for q in self._queries if q.timestamp >= window_start)
        if query_count == 0:
            return 0.0
        return error_count / query_count

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        return sum(1 for q in self._queries if q.timestamp >= one_hour_ago)

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {}
        for mode, queries in self._coverage_data.items():
            report[mode] = {
                "unique_queries": len(queries),
                "coverage": len(queries) / max(1, self._mode_counter[mode])
            }
        report['total_modes'] = len(self._coverage_data)
        report['total_queries'] = self._query_counter['total']
        return report

    def export_jsonl(self, path: Union[str, pathlib.Path]) -> int:
        path = pathlib.Path(path)
        count = 0
        with path.open("w", encoding="utf-8") as f:
            for q in self._queries:
                f.write(json.dumps(dataclasses.asdict(q)) + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {path}")
        return count

class AuditTrailWriter:
    def __init__(self, base_path: Union[str, pathlib.Path] = "audit_trail"):
        self.base_path = pathlib.Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"AuditTrailWriter initialized at {self.base_path}")

    def write(self, metrics: QueryMetrics):
        filename = self._get_filename(metrics)
        entry = dataclasses.asdict(metrics)
        with open(filename, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        logger.debug(f"Wrote audit trail for query {metrics.query_id} to {filename}")

    def _get_filename(self, metrics: QueryMetrics) -> str:
        date_str = time.strftime("%Y%m%d", time.localtime(metrics.timestamp))
        hash_id = hashlib.sha256(metrics.query_id.encode()).hexdigest()[:8]
        filename = f"{self.base_path}/audit_{metrics.engine_id}_{date_str}_{hash_id}.jsonl"
        return filename

COLLECTOR = TelemetryCollector(engine_id=ENGINE_ID)