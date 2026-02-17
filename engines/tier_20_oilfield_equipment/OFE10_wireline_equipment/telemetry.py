import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any, Union
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "OFE10"

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
    def __init__(self, engine_id: str = ENGINE_ID, maxlen: int = 10000):
        self.engine_id = engine_id
        self.metrics: deque = deque(maxlen=maxlen)
        self.errors: deque = deque(maxlen=maxlen)
        self._latencies: List[float] = []
        self._doctrine_hits: List[bool] = []
        self._cache_hits: List[bool] = []
        self._modes: Counter = Counter()
        self._confidence: List[float] = []
        self._coverage: Dict[str, int] = defaultdict(int)
        self._query_ids: set = set()
        self._audit_writer: Optional[AuditTrailWriter] = None

    def record_query(self, metrics: QueryMetrics):
        self.metrics.append(metrics)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._cache_hits.append(metrics.cache_hit)
        self._modes[metrics.mode] += 1
        self._confidence.append(metrics.confidence)
        self._coverage[metrics.mode] += 1
        self._query_ids.add(metrics.query_id)
        if self._audit_writer:
            self._audit_writer.write(metrics)
        logger.debug(f"Recorded query: {metrics}")

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_record = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "engine_id": self.engine_id,
            "timestamp": time.time()
        }
        self.errors.append(error_record)
        logger.error(f"Error recorded: {error_record}")

    def get_latency_stats(self) -> Dict[str, Union[float, None]]:
        if not self._latencies:
            return dict(avg=None, p50=None, p95=None, p99=None, min=None, max=None)
        latencies = sorted(self._latencies)
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = latencies[int(0.95 * len(latencies)) - 1]
        p99 = latencies[int(0.99 * len(latencies)) - 1]
        min_latency = min(latencies)
        max_latency = max(latencies)
        return {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_latency,
            "max": max_latency
        }

    def get_doctrine_hit_rate(self) -> float:
        if not self._doctrine_hits:
            return 0.0
        hits = sum(self._doctrine_hits)
        total = len(self._doctrine_hits)
        return hits / total

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        relevant_queries = [m for m in self.metrics if m.timestamp >= window_start]
        relevant_errors = [e for e in self.errors if e["timestamp"] >= window_start]
        num_queries = len(relevant_queries)
        num_errors = len(relevant_errors)
        if num_queries == 0:
            return 0.0
        return num_errors / num_queries

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for m in self.metrics if m.timestamp >= one_hour_ago)
        return count

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
        with path.open("w", encoding="utf-8") as f:
            for m in self.metrics:
                f.write(json.dumps(asdict(m)) + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {path}")
        return count

    def set_audit_writer(self, writer: 'AuditTrailWriter'):
        self._audit_writer = writer

class AuditTrailWriter:
    def __init__(self, path: Union[str, pathlib.Path]):
        self.path = pathlib.Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._file = self.path.open("a", encoding="utf-8")

    def write(self, metrics: QueryMetrics):
        record = asdict(metrics)
        record["audit_hash"] = self._hash_record(record)
        self._file.write(json.dumps(record) + "\n")
        self._file.flush()
        logger.debug(f"Audit trail written for query_id={metrics.query_id}")

    def _hash_record(self, record: Dict[str, Any]) -> str:
        record_str = json.dumps(record, sort_keys=True)
        return hashlib.sha256(record_str.encode("utf-8")).hexdigest()

    def close(self):
        self._file.close()

COLLECTOR = TelemetryCollector(engine_id=ENGINE_ID)

# Example: set up audit trail writer
# audit_writer = AuditTrailWriter("/tmp/ofe10_audit_trail.jsonl")
# COLLECTOR.set_audit_writer(audit_writer)

# Example usage:
# metrics = QueryMetrics(
#     query_id="Q12345",
#     engine_id=ENGINE_ID,
#     timestamp=time.time(),
#     latency_ms=123.4,
#     cache_hit=True,
#     doctrine_matched=False,
#     mode="wireline",
#     confidence=0.92,
#     error=None
# )
# COLLECTOR.record_query(metrics)
# COLLECTOR.record_error("Timeout", "Query timed out", "Q12345")
# stats = COLLECTOR.get_latency_stats()
# hit_rate = COLLECTOR.get_doctrine_hit_rate()
# error_rate = COLLECTOR.get_error_rate(1.0)
# coverage = COLLECTOR.get_coverage_report()
# COLLECTOR.export_jsonl("/tmp/ofe10_telemetry.jsonl")