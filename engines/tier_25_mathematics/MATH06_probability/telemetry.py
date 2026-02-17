import time
import json
import hashlib
import statistics
import pathlib
import dataclasses
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any, Union
import collections
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "MATH06"

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
        self._modes = deque(maxlen=maxlen)
        self._confidences = deque(maxlen=maxlen)
        self._query_id_index = {}
        self._coverage_counter = Counter()
        self._audit_writer = AuditTrailWriter()
        self._lock = None  # Placeholder for thread safety if needed

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._cache_hits.append(metrics.cache_hit)
        self._modes.append(metrics.mode)
        self._confidences.append(metrics.confidence)
        self._query_id_index[metrics.query_id] = metrics
        self._coverage_counter[metrics.mode] += 1
        if metrics.error:
            self.record_error(metrics.error, "Query error", metrics.query_id)
        self._audit_writer.write(metrics)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "engine_id": ENGINE_ID
        }
        self._errors.append(error_entry)
        logger.error(f"Error recorded: {error_entry}")

    def get_latency_stats(self) -> Dict[str, float]:
        latencies = list(self._latencies)
        if not latencies:
            return {
                "avg": 0.0,
                "p50": 0.0,
                "p95": 0.0,
                "p99": 0.0,
                "min": 0.0,
                "max": 0.0
            }
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        min_v = latencies_sorted[0]
        max_v = latencies_sorted[-1]
        p50 = self._percentile(latencies_sorted, 50)
        p95 = self._percentile(latencies_sorted, 95)
        p99 = self._percentile(latencies_sorted, 99)
        return {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_v,
            "max": max_v
        }

    def _percentile(self, data: List[float], percentile: float) -> float:
        if not data:
            return 0.0
        k = (len(data)-1) * (percentile/100)
        f = int(k)
        c = min(f+1, len(data)-1)
        if f == c:
            return data[int(k)]
        d0 = data[f] * (c-k)
        d1 = data[c] * (k-f)
        return d0 + d1

    def get_doctrine_hit_rate(self) -> float:
        hits = list(self._doctrine_hits)
        if not hits:
            return 0.0
        return sum(hits) / len(hits)

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_sec = window_hours * 3600
        errors_in_window = [e for e in self._errors if now - e["timestamp"] <= window_sec]
        queries_in_window = [q for q in self._queries if now - q.timestamp <= window_sec]
        n_queries = len(queries_in_window)
        n_errors = len(errors_in_window)
        if n_queries == 0:
            return 0.0
        return n_errors / n_queries

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        return sum(1 for q in self._queries if q.timestamp >= one_hour_ago)

    def get_coverage_report(self) -> Dict[str, Any]:
        total = sum(self._coverage_counter.values())
        report = {}
        for mode, count in self._coverage_counter.items():
            report[mode] = {
                "count": count,
                "ratio": count / total if total > 0 else 0.0
            }
        return {
            "total_queries": total,
            "modes": report
        }

    def export_jsonl(self, path: Union[str, pathlib.Path]) -> int:
        path = pathlib.Path(path)
        count = 0
        with path.open("w", encoding="utf-8") as f:
            for q in self._queries:
                f.write(json.dumps(asdict(q)) + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {path}")
        return count

class AuditTrailWriter:
    def __init__(self, base_dir: Union[str, pathlib.Path] = "./audit_trail"):
        self.base_dir = pathlib.Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def write(self, metrics: QueryMetrics):
        audit_record = self._build_audit_record(metrics)
        filename = self._get_audit_filename(metrics.query_id)
        with open(filename, "a", encoding="utf-8") as f:
            f.write(json.dumps(audit_record) + "\n")
        logger.debug(f"Audit trail written for query_id={metrics.query_id}")

    def _build_audit_record(self, metrics: QueryMetrics) -> Dict[str, Any]:
        record = asdict(metrics)
        record["audit_timestamp"] = time.time()
        record["hash"] = self._hash_query(metrics)
        return record

    def _get_audit_filename(self, query_id: str) -> str:
        # Use first 2 chars of query_id as subdir for sharding
        subdir = self.base_dir / query_id[:2]
        subdir.mkdir(exist_ok=True)
        return str(subdir / f"{query_id}.jsonl")

    def _hash_query(self, metrics: QueryMetrics) -> str:
        m = hashlib.sha256()
        m.update(metrics.query_id.encode("utf-8"))
        m.update(str(metrics.timestamp).encode("utf-8"))
        m.update(str(metrics.latency_ms).encode("utf-8"))
        m.update(str(metrics.cache_hit).encode("utf-8"))
        m.update(str(metrics.doctrine_matched).encode("utf-8"))
        m.update(metrics.mode.encode("utf-8"))
        m.update(str(metrics.confidence).encode("utf-8"))
        if metrics.error:
            m.update(metrics.error.encode("utf-8"))
        return m.hexdigest()

COLLECTOR = TelemetryCollector()