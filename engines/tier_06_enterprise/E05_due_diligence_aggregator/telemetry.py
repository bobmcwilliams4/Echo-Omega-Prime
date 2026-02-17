import time
import json
import hashlib
import statistics
import pathlib
import dataclasses
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Union
import collections
from loguru import logger

ENGINE_ID = "E05"

@dataclass
class QueryMetrics:
    query_id: str
    engine_id: str = ENGINE_ID
    timestamp: float = field(default_factory=lambda: time.time())
    latency_ms: float = 0.0
    cache_hit: bool = False
    doctrine_matched: bool = False
    mode: str = "default"
    confidence: float = 0.0
    error: Optional[str] = None

class TelemetryCollector:
    def __init__(self):
        self._queries = []
        self._errors = []
        self._doctrine_hits = 0
        self._doctrine_total = 0
        self._latencies = []
        self._query_times = collections.deque()
        self._coverage = collections.Counter()
        self._lock = None  # Placeholder for threading.Lock if needed

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._latencies.append(metrics.latency_ms)
        self._query_times.append(metrics.timestamp)
        self._doctrine_total += 1
        if metrics.doctrine_matched:
            self._doctrine_hits += 1
        self._coverage[metrics.mode] += 1
        logger.info(f"Query recorded: {metrics.query_id} latency={metrics.latency_ms}ms cache_hit={metrics.cache_hit} doctrine_matched={metrics.doctrine_matched} mode={metrics.mode} confidence={metrics.confidence} error={metrics.error}")

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_record = {
            "timestamp": time.time(),
            "error_type": error_type,
            "message": message,
            "query_id": query_id
        }
        self._errors.append(error_record)
        logger.error(f"Error recorded: {error_type} for query_id={query_id}: {message}")

    def get_latency_stats(self) -> Dict[str, Union[float, None]]:
        if not self._latencies:
            return dict(avg=None, p50=None, p95=None, p99=None, min=None, max=None)
        latencies = sorted(self._latencies)
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = latencies[int(0.95 * len(latencies)) - 1]
        p99 = latencies[int(0.99 * len(latencies)) - 1]
        min_latency = latencies[0]
        max_latency = latencies[-1]
        return dict(
            avg=avg,
            p50=p50,
            p95=p95,
            p99=p99,
            min=min_latency,
            max=max_latency
        )

    def get_doctrine_hit_rate(self) -> float:
        if self._doctrine_total == 0:
            return 0.0
        return self._doctrine_hits / self._doctrine_total

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        error_count = sum(1 for e in self._errors if e["timestamp"] >= window_start)
        query_count = sum(1 for q in self._queries if q.timestamp >= window_start)
        if query_count == 0:
            return 0.0
        return error_count / query_count

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        return sum(1 for q in self._queries if q.timestamp >= one_hour_ago)

    def get_coverage_report(self) -> Dict[str, Any]:
        total = sum(self._coverage.values())
        report = {}
        for mode, count in self._coverage.items():
            report[mode] = {
                "count": count,
                "percent": (count / total) * 100 if total else 0.0
            }
        return report

    def export_jsonl(self, path: Union[str, pathlib.Path]) -> int:
        path = pathlib.Path(path)
        count = 0
        with path.open("a", encoding="utf-8") as f:
            for metrics in self._queries:
                f.write(json.dumps(dataclasses.asdict(metrics)) + "\n")
                count += 1
        logger.info(f"Exported {count} query metrics to {path}")
        return count

class AuditTrailWriter:
    def __init__(self, audit_dir: Union[str, pathlib.Path]):
        self.audit_dir = pathlib.Path(audit_dir)
        self.audit_dir.mkdir(parents=True, exist_ok=True)

    def write(self, query_id: str, data: Dict[str, Any]):
        filename = self._get_filename(query_id)
        with open(filename, "a", encoding="utf-8") as f:
            f.write(json.dumps(data) + "\n")
        logger.debug(f"Audit trail written for query_id={query_id} to {filename}")

    def _get_filename(self, query_id: str) -> str:
        hash_id = hashlib.sha256(query_id.encode()).hexdigest()
        return str(self.audit_dir / f"{hash_id}.jsonl")

COLLECTOR = TelemetryCollector()