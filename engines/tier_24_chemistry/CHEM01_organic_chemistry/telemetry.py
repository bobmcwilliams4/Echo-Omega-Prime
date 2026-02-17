import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional, Any
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "CHEM01"

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
        self._queries: deque = deque(maxlen=maxlen)
        self._errors: deque = deque(maxlen=maxlen)
        self._doctrine_counter: Counter = Counter()
        self._cache_counter: Counter = Counter()
        self._mode_counter: Counter = Counter()
        self._confidence_values: List[float] = []
        self._latencies: List[float] = []
        self._coverage: defaultdict = defaultdict(set)
        self._query_times: deque = deque(maxlen=maxlen)
        self._query_id_map: Dict[str, QueryMetrics] = {}
        self._audit_writer = AuditTrailWriter()
        logger.info("TelemetryCollector initialized with maxlen={}", maxlen)

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._query_id_map[metrics.query_id] = metrics
        self._latencies.append(metrics.latency_ms)
        self._doctrine_counter[metrics.doctrine_matched] += 1
        self._cache_counter[metrics.cache_hit] += 1
        self._mode_counter[metrics.mode] += 1
        self._confidence_values.append(metrics.confidence)
        self._query_times.append(metrics.timestamp)
        self._coverage[metrics.mode].add(metrics.query_id)
        self._audit_writer.write(metrics)
        logger.debug("Recorded query: {}", metrics)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "error_type": error_type,
            "message": message,
            "query_id": query_id
        }
        self._errors.append(error_entry)
        logger.error("Recorded error: {}", error_entry)

    def get_latency_stats(self) -> Dict[str, Any]:
        if not self._latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        lat_sorted = sorted(self._latencies)
        avg = statistics.mean(lat_sorted)
        min_v = lat_sorted[0]
        max_v = lat_sorted[-1]
        p50 = statistics.median(lat_sorted)
        def percentile(p):
            k = (len(lat_sorted)-1) * (p/100)
            f = int(k)
            c = min(f+1, len(lat_sorted)-1)
            if f == c:
                return lat_sorted[int(k)]
            d0 = lat_sorted[f] * (c-k)
            d1 = lat_sorted[c] * (k-f)
            return d0 + d1
        p95 = percentile(95)
        p99 = percentile(99)
        stats = {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_v,
            "max": max_v
        }
        logger.debug("Latency stats: {}", stats)
        return stats

    def get_doctrine_hit_rate(self) -> float:
        total = sum(self._doctrine_counter.values())
        if total == 0:
            return 0.0
        hit_rate = self._doctrine_counter[True] / total
        logger.debug("Doctrine hit rate: {}", hit_rate)
        return hit_rate

    def get_error_rate(self, window_hours: float) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        queries_in_window = [q for q in self._queries if q.timestamp >= window_start]
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        total = len(queries_in_window)
        if total == 0:
            return 0.0
        error_rate = len(errors_in_window) / total
        logger.debug("Error rate in last {} hours: {}", window_hours, error_rate)
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for t in self._query_times if t >= one_hour_ago)
        logger.debug("Queries in last hour: {}", count)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {}
        for mode, qids in self._coverage.items():
            report[mode] = len(qids)
        logger.debug("Coverage report: {}", report)
        return report

    def export_jsonl(self, path: str) -> int:
        out_path = pathlib.Path(path)
        count = 0
        with out_path.open("w", encoding="utf-8") as f:
            for qm in self._queries:
                f.write(json.dumps(asdict(qm)) + "\n")
                count += 1
        logger.info("Exported {} queries to {}", count, path)
        return count

class AuditTrailWriter:
    def __init__(self, base_dir: Optional[str] = None):
        if base_dir is None:
            base_dir = "./audit_trail"
        self.base_dir = pathlib.Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        logger.info("AuditTrailWriter initialized at {}", self.base_dir)

    def write(self, metrics: QueryMetrics):
        ts = time.strftime("%Y%m%d")
        day_dir = self.base_dir / ts
        day_dir.mkdir(exist_ok=True)
        fname = day_dir / f"{metrics.query_id}.jsonl"
        entry = asdict(metrics)
        with fname.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        logger.debug("Wrote audit trail for query_id={} to {}", metrics.query_id, fname)

COLLECTOR = TelemetryCollector()