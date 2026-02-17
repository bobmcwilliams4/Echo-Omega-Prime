import time
import json
import hashlib
import statistics
import pathlib
import dataclasses
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Union
import collections
from collections import deque, defaultdict, Counter
from loguru import logger

ENGINE_ID = "E10"

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
        self._queries = deque(maxlen=maxlen)
        self._errors = deque(maxlen=maxlen)
        self._doctrine_hits = deque(maxlen=maxlen)
        self._cache_hits = deque(maxlen=maxlen)
        self._latencies = deque(maxlen=maxlen)
        self._query_timestamps = deque(maxlen=maxlen)
        self._coverage_modes = Counter()
        self._confidence_scores = []
        self._query_ids = set()
        self._audit_trail_writer = None

    def set_audit_trail_writer(self, writer):
        self._audit_trail_writer = writer

    def record_query(self, metrics: QueryMetrics):
        if metrics.query_id in self._query_ids:
            logger.warning(f"Duplicate query_id detected: {metrics.query_id}")
            return
        self._query_ids.add(metrics.query_id)
        self._queries.append(metrics)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._cache_hits.append(metrics.cache_hit)
        self._query_timestamps.append(metrics.timestamp)
        self._coverage_modes[metrics.mode] += 1
        self._confidence_scores.append(metrics.confidence)
        if metrics.error:
            self.record_error(metrics.error, "Query error", metrics.query_id)
        if self._audit_trail_writer:
            self._audit_trail_writer.write(metrics)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "error_type": error_type,
            "message": message,
            "query_id": query_id
        }
        self._errors.append(error_entry)
        logger.error(f"Error recorded: {error_entry}")

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = list(self._latencies)
        if not latencies:
            return {
                "avg": None,
                "p50": None,
                "p95": None,
                "p99": None,
                "min": None,
                "max": None,
                "count": 0
            }
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        min_latency = min(latencies)
        max_latency = max(latencies)
        p50 = statistics.median(latencies)
        def percentile(data, perc):
            k = (len(data) - 1) * (perc / 100)
            f = int(k)
            c = min(f + 1, len(data) - 1)
            if f == c:
                return data[int(k)]
            d0 = data[f] * (c - k)
            d1 = data[c] * (k - f)
            return d0 + d1
        p95 = percentile(latencies_sorted, 95)
        p99 = percentile(latencies_sorted, 99)
        return {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_latency,
            "max": max_latency,
            "count": len(latencies)
        }

    def get_doctrine_hit_rate(self) -> float:
        hits = list(self._doctrine_hits)
        if not hits:
            return 0.0
        return sum(1 for h in hits if h) / len(hits)

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        error_count = 0
        total_count = 0
        for metrics in reversed(self._queries):
            if metrics.timestamp < window_start:
                break
            total_count += 1
            if metrics.error:
                error_count += 1
        if total_count == 0:
            return 0.0
        return error_count / total_count

    def queries_last_hour(self) -> int:
        now = time.time()
        window_start = now - 3600
        count = 0
        for ts in reversed(self._query_timestamps):
            if ts < window_start:
                break
            count += 1
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        total = sum(self._coverage_modes.values())
        if total == 0:
            return {}
        report = {}
        for mode, count in self._coverage_modes.items():
            report[mode] = {
                "count": count,
                "pct": count / total
            }
        if self._confidence_scores:
            report["confidence"] = {
                "avg": statistics.mean(self._confidence_scores),
                "min": min(self._confidence_scores),
                "max": max(self._confidence_scores)
            }
        else:
            report["confidence"] = {
                "avg": None,
                "min": None,
                "max": None
            }
        return report

    def export_jsonl(self, path: Union[str, pathlib.Path]) -> int:
        path = pathlib.Path(path)
        count = 0
        with path.open("w", encoding="utf-8") as f:
            for metrics in self._queries:
                d = dataclasses.asdict(metrics)
                f.write(json.dumps(d) + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {path}")
        return count

class AuditTrailWriter:
    def __init__(self, directory: Union[str, pathlib.Path]):
        self.directory = pathlib.Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)

    def write(self, metrics: QueryMetrics):
        record = dataclasses.asdict(metrics)
        record["audit_hash"] = self._compute_hash(record)
        filename = f"{metrics.query_id}.jsonl"
        path = self.directory / filename
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
        logger.debug(f"Audit trail written for query_id={metrics.query_id}")

    def _compute_hash(self, record: Dict[str, Any]) -> str:
        record_str = json.dumps(record, sort_keys=True)
        return hashlib.sha256(record_str.encode("utf-8")).hexdigest()

COLLECTOR = TelemetryCollector(maxlen=10000)