import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict, field
from typing import Optional, List, Dict, Any, Deque
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "G05"

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
        self._queries: Deque[QueryMetrics] = deque(maxlen=maxlen)
        self._errors: Deque[Dict[str, Any]] = deque(maxlen=maxlen)
        self._doctrine_hits: Deque[bool] = deque(maxlen=maxlen)
        self._cache_hits: Deque[bool] = deque(maxlen=maxlen)
        self._latencies: Deque[float] = deque(maxlen=maxlen)
        self._query_times: Deque[float] = deque(maxlen=maxlen)
        self._query_ids: Deque[str] = deque(maxlen=maxlen)
        self._error_types: Counter = Counter()
        self._coverage: Dict[str, Counter] = defaultdict(Counter)
        self._audit_writer = AuditTrailWriter()
        logger.info("TelemetryCollector initialized with maxlen={}", maxlen)

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._cache_hits.append(metrics.cache_hit)
        self._latencies.append(metrics.latency_ms)
        self._query_times.append(metrics.timestamp)
        self._query_ids.append(metrics.query_id)
        self._coverage[metrics.mode][
            "total"
        ] += 1
        if metrics.doctrine_matched:
            self._coverage[metrics.mode]["doctrine_matched"] += 1
        if metrics.cache_hit:
            self._coverage[metrics.mode]["cache_hit"] += 1
        if metrics.error:
            self._coverage[metrics.mode]["error"] += 1
        self._audit_writer.write(metrics)
        logger.debug("Recorded query: {}", metrics)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "error_type": error_type,
            "message": message,
            "timestamp": time.time(),
            "query_id": query_id,
        }
        self._errors.append(error_entry)
        self._error_types[error_type] += 1
        logger.error("Recorded error: {}", error_entry)

    def get_latency_stats(self) -> Dict[str, float]:
        latencies = list(self._latencies)
        if not latencies:
            return {
                "avg": 0.0,
                "p50": 0.0,
                "p95": 0.0,
                "p99": 0.0,
                "min": 0.0,
                "max": 0.0,
            }
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = self._percentile(latencies_sorted, 95)
        p99 = self._percentile(latencies_sorted, 99)
        min_v = latencies_sorted[0]
        max_v = latencies_sorted[-1]
        stats = {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_v,
            "max": max_v,
        }
        logger.debug("Latency stats: {}", stats)
        return stats

    def _percentile(self, data: List[float], percentile: float) -> float:
        if not data:
            return 0.0
        k = (len(data) - 1) * (percentile / 100)
        f = int(k)
        c = min(f + 1, len(data) - 1)
        if f == c:
            return data[int(k)]
        d0 = data[f] * (c - k)
        d1 = data[c] * (k - f)
        return d0 + d1

    def get_doctrine_hit_rate(self) -> float:
        total = len(self._doctrine_hits)
        if total == 0:
            return 0.0
        hits = sum(self._doctrine_hits)
        rate = hits / total
        logger.debug("Doctrine hit rate: {:.3f} ({} hits / {} total)", rate, hits, total)
        return rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        queries_in_window = [t for t in self._query_times if t >= window_start]
        num_errors = len(errors_in_window)
        num_queries = len(queries_in_window)
        rate = (num_errors / num_queries) if num_queries else 0.0
        logger.debug(
            "Error rate: {:.3f} ({} errors / {} queries) in last {}h",
            rate,
            num_errors,
            num_queries,
            window_hours,
        )
        return rate

    def queries_last_hour(self) -> int:
        now = time.time()
        hour_ago = now - 3600
        count = sum(1 for t in self._query_times if t >= hour_ago)
        logger.debug("Queries in last hour: {}", count)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {}
        for mode, counters in self._coverage.items():
            total = counters.get("total", 0)
            doctrine_matched = counters.get("doctrine_matched", 0)
            cache_hit = counters.get("cache_hit", 0)
            error = counters.get("error", 0)
            report[mode] = {
                "total": total,
                "doctrine_matched": doctrine_matched,
                "cache_hit": cache_hit,
                "error": error,
                "doctrine_match_rate": (doctrine_matched / total) if total else 0.0,
                "cache_hit_rate": (cache_hit / total) if total else 0.0,
                "error_rate": (error / total) if total else 0.0,
            }
        logger.debug("Coverage report: {}", report)
        return report

    def export_jsonl(self, path: str) -> int:
        out_path = pathlib.Path(path)
        count = 0
        with out_path.open("w", encoding="utf-8") as f:
            for qm in self._queries:
                f.write(json.dumps(asdict(qm)) + "\n")
                count += 1
        logger.info("Exported {} queries to {}", count, out_path)
        return count

class AuditTrailWriter:
    def __init__(self, base_dir: Optional[str] = None):
        if base_dir is None:
            base_dir = "./audit_trail"
        self.base_dir = pathlib.Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        logger.info("AuditTrailWriter initialized at {}", self.base_dir)

    def write(self, metrics: QueryMetrics):
        query_hash = hashlib.sha256(metrics.query_id.encode()).hexdigest()
        filename = f"{metrics.engine_id}_{query_hash}.jsonl"
        filepath = self.base_dir / filename
        record = asdict(metrics)
        record["audit_timestamp"] = time.time()
        with filepath.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
        logger.debug("Wrote audit trail for query_id={} to {}", metrics.query_id, filepath)

COLLECTOR = TelemetryCollector()