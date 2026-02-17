import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any, Union
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "ENT08"

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
    def __init__(self, engine_id: str = ENGINE_ID, max_queries: int = 100000):
        self.engine_id = engine_id
        self._queries: deque = deque(maxlen=max_queries)
        self._errors: deque = deque(maxlen=max_queries)
        self._doctrine_counter: Counter = Counter()
        self._cache_hit_counter: Counter = Counter()
        self._mode_counter: Counter = Counter()
        self._confidence_values: deque = deque(maxlen=max_queries)
        self._audit_trail_writer = AuditTrailWriter()
        self._coverage_counter: Counter = Counter()
        self._query_ids: set = set()

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._doctrine_counter[metrics.doctrine_matched] += 1
        self._cache_hit_counter[metrics.cache_hit] += 1
        self._mode_counter[metrics.mode] += 1
        self._confidence_values.append(metrics.confidence)
        self._coverage_counter[metrics.query_id] += 1
        self._query_ids.add(metrics.query_id)
        self._audit_trail_writer.write(metrics)
        logger.info(f"Recorded query: {metrics.query_id}")

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "engine_id": self.engine_id,
            "timestamp": time.time()
        }
        self._errors.append(error_entry)
        logger.error(f"Error recorded: {error_type} | {message} | Query: {query_id}")

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = [q.latency_ms for q in self._queries if q.latency_ms is not None]
        if not latencies:
            return {
                "avg": None,
                "p50": None,
                "p95": None,
                "p99": None,
                "min": None,
                "max": None
            }
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = self._percentile(latencies_sorted, 95)
        p99 = self._percentile(latencies_sorted, 99)
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

    def _percentile(self, data: List[float], percentile: float) -> float:
        if not data:
            return None
        k = (len(data) - 1) * (percentile / 100)
        f = int(k)
        c = f + 1
        if c >= len(data):
            return data[-1]
        d0 = data[f] * (c - k)
        d1 = data[c] * (k - f)
        return d0 + d1

    def get_doctrine_hit_rate(self) -> float:
        total = sum(self._doctrine_counter.values())
        if total == 0:
            return 0.0
        hits = self._doctrine_counter[True]
        return hits / total

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        queries_in_window = [q for q in self._queries if q.timestamp >= window_start]
        num_queries = len(queries_in_window)
        if num_queries == 0:
            return 0.0
        return len(errors_in_window) / num_queries

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        return sum(1 for q in self._queries if q.timestamp >= one_hour_ago)

    def get_coverage_report(self) -> Dict[str, Any]:
        total_queries = len(self._queries)
        unique_queries = len(self._query_ids)
        doctrine_hits = self._doctrine_counter[True]
        cache_hits = self._cache_hit_counter[True]
        modes = dict(self._mode_counter)
        confidence_stats = self._confidence_stats()
        return {
            "total_queries": total_queries,
            "unique_queries": unique_queries,
            "doctrine_hits": doctrine_hits,
            "cache_hits": cache_hits,
            "modes": modes,
            "confidence": confidence_stats
        }

    def _confidence_stats(self) -> Dict[str, Any]:
        values = list(self._confidence_values)
        if not values:
            return {
                "avg": None,
                "min": None,
                "max": None,
                "p50": None,
                "p95": None
            }
        avg = statistics.mean(values)
        min_val = min(values)
        max_val = max(values)
        p50 = statistics.median(values)
        p95 = self._percentile(sorted(values), 95)
        return {
            "avg": avg,
            "min": min_val,
            "max": max_val,
            "p50": p50,
            "p95": p95
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
    def __init__(self, audit_dir: Union[str, pathlib.Path] = "audit_trail"):
        self.audit_dir = pathlib.Path(audit_dir)
        self.audit_dir.mkdir(parents=True, exist_ok=True)

    def write(self, metrics: QueryMetrics):
        audit_file = self._get_audit_file(metrics.query_id)
        entry = asdict(metrics)
        entry["audit_hash"] = self._hash_entry(entry)
        with audit_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        logger.debug(f"Audit trail written for query {metrics.query_id}")

    def _get_audit_file(self, query_id: str) -> pathlib.Path:
        safe_id = hashlib.sha256(query_id.encode("utf-8")).hexdigest()
        return self.audit_dir / f"{safe_id}.jsonl"

    def _hash_entry(self, entry: Dict[str, Any]) -> str:
        entry_bytes = json.dumps(entry, sort_keys=True).encode("utf-8")
        return hashlib.sha256(entry_bytes).hexdigest()

COLLECTOR = TelemetryCollector(engine_id=ENGINE_ID)