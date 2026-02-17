import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict, field
from typing import List, Optional, Dict, Any, Deque
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "SYN04"

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
        self.queries: Deque[QueryMetrics] = deque(maxlen=maxlen)
        self.errors: Deque[Dict[str, Any]] = deque(maxlen=maxlen)
        self._doctrine_hits: int = 0
        self._doctrine_total: int = 0
        self._cache_hits: int = 0
        self._cache_total: int = 0
        self._latencies: List[float] = []
        self._modes: Counter = Counter()
        self._confidence_scores: List[float] = []
        self._coverage: Dict[str, int] = defaultdict(int)
        self._query_times: Deque[float] = deque(maxlen=maxlen)
        self._query_ids: set = set()
        logger.info("TelemetryCollector initialized with maxlen={}", maxlen)

    def record_query(self, metrics: QueryMetrics):
        self.queries.append(metrics)
        self._query_times.append(metrics.timestamp)
        self._query_ids.add(metrics.query_id)
        self._latencies.append(metrics.latency_ms)
        self._modes[metrics.mode] += 1
        self._confidence_scores.append(metrics.confidence)
        self._coverage[metrics.mode] += 1
        self._doctrine_total += 1
        if metrics.doctrine_matched:
            self._doctrine_hits += 1
        self._cache_total += 1
        if metrics.cache_hit:
            self._cache_hits += 1
        logger.debug("Recorded query: {}", metrics)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "error_type": error_type,
            "message": message,
            "query_id": query_id
        }
        self.errors.append(error_entry)
        logger.error("Error recorded: {} - {} (query_id={})", error_type, message, query_id)

    def get_latency_stats(self) -> Dict[str, float]:
        if not self._latencies:
            return {"avg": 0, "p50": 0, "p95": 0, "p99": 0, "min": 0, "max": 0}
        sorted_lat = sorted(self._latencies)
        avg = statistics.mean(self._latencies)
        min_v = sorted_lat[0]
        max_v = sorted_lat[-1]
        p50 = statistics.median(sorted_lat)
        def percentile(p):
            k = int(len(sorted_lat) * p / 100)
            k = min(k, len(sorted_lat) - 1)
            return sorted_lat[k]
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
        if self._doctrine_total == 0:
            return 0.0
        hit_rate = self._doctrine_hits / self._doctrine_total
        logger.debug("Doctrine hit rate: {}", hit_rate)
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        error_count = 0
        query_count = 0
        for q in self.queries:
            if q.timestamp >= window_start:
                query_count += 1
        for e in self.errors:
            if e["timestamp"] >= window_start:
                error_count += 1
        if query_count == 0:
            return 0.0
        error_rate = error_count / query_count
        logger.debug("Error rate ({}h): {}", window_hours, error_rate)
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        window_start = now - 3600
        count = 0
        for t in reversed(self._query_times):
            if t >= window_start:
                count += 1
            else:
                break
        logger.debug("Queries in last hour: {}", count)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        total = sum(self._coverage.values())
        if total == 0:
            return {"modes": {}, "total": 0}
        modes = {mode: count / total for mode, count in self._coverage.items()}
        report = {"modes": modes, "total": total}
        logger.debug("Coverage report: {}", report)
        return report

    def export_jsonl(self, path: str) -> int:
        p = pathlib.Path(path)
        count = 0
        with p.open("w", encoding="utf-8") as f:
            for q in self.queries:
                f.write(json.dumps(asdict(q)) + "\n")
                count += 1
        logger.info("Exported {} queries to {}", count, path)
        return count

class AuditTrailWriter:
    def __init__(self, directory: str):
        self.dir = pathlib.Path(directory)
        self.dir.mkdir(parents=True, exist_ok=True)
        logger.info("AuditTrailWriter initialized at {}", self.dir)

    def write(self, metrics: QueryMetrics, extra: Optional[Dict[str, Any]] = None) -> str:
        data = asdict(metrics)
        if extra:
            data.update(extra)
        jsonl = json.dumps(data)
        # Use a hash of query_id and timestamp for filename uniqueness
        base = f"{metrics.query_id}_{int(metrics.timestamp)}"
        h = hashlib.sha256(base.encode()).hexdigest()[:12]
        fname = f"{metrics.query_id}_{h}.jsonl"
        fpath = self.dir / fname
        with fpath.open("w", encoding="utf-8") as f:
            f.write(jsonl + "\n")
        logger.debug("Audit trail written: {}", fpath)
        return str(fpath)

COLLECTOR = TelemetryCollector(maxlen=10000)