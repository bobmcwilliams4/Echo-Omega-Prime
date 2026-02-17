import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any, Union
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "CHEM18"

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
        self._doctrine_hits: deque = deque(maxlen=maxlen)
        self._latencies: deque = deque(maxlen=maxlen)
        self._audit_trail_writer = AuditTrailWriter()
        self._query_id_set: set = set()
        self._coverage_modes: Counter = Counter()
        self._coverage_confidence: defaultdict = defaultdict(list)
        self._coverage_cache_hits: Counter = Counter()
        self._coverage_doctrine: Counter = Counter()
        self._coverage_errors: Counter = Counter()
        self._coverage_total: int = 0

    def record_query(self, metrics: QueryMetrics):
        logger.debug(f"Recording query: {metrics}")
        self._queries.append(metrics)
        self._query_id_set.add(metrics.query_id)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._coverage_modes[metrics.mode] += 1
        self._coverage_confidence[metrics.mode].append(metrics.confidence)
        self._coverage_cache_hits[metrics.cache_hit] += 1
        self._coverage_doctrine[metrics.doctrine_matched] += 1
        self._coverage_total += 1
        if metrics.error:
            self._coverage_errors[metrics.error] += 1
        self._audit_trail_writer.write(metrics)
    
    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "error_type": error_type,
            "message": message,
            "timestamp": time.time(),
            "query_id": query_id,
            "engine_id": ENGINE_ID
        }
        logger.error(f"Recording error: {error_entry}")
        self._errors.append(error_entry)
        self._coverage_errors[error_type] += 1
        self._audit_trail_writer.write(error_entry)
    
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
        p50 = statistics.median(latencies)
        p95 = latencies_sorted[int(0.95 * len(latencies_sorted)) - 1]
        p99 = latencies_sorted[int(0.99 * len(latencies_sorted)) - 1]
        min_latency = min(latencies)
        max_latency = max(latencies)
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
        total = len(self._doctrine_hits)
        if total == 0:
            return 0.0
        hits = sum(1 for hit in self._doctrine_hits if hit)
        return hits / total

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [err for err in self._errors if err["timestamp"] >= window_start]
        queries_in_window = [q for q in self._queries if q.timestamp >= window_start]
        if not queries_in_window:
            return 0.0
        return len(errors_in_window) / len(queries_in_window)

    def queries_last_hour(self) -> int:
        now = time.time()
        hour_ago = now - 3600
        return sum(1 for q in self._queries if q.timestamp >= hour_ago)

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {
            "total_queries": self._coverage_total,
            "modes": dict(self._coverage_modes),
            "confidence_by_mode": {mode: {
                "avg": statistics.mean(vals) if vals else None,
                "min": min(vals) if vals else None,
                "max": max(vals) if vals else None,
                "count": len(vals)
            } for mode, vals in self._coverage_confidence.items()},
            "cache_hit_rate": self._coverage_cache_hits[True] / self._coverage_total if self._coverage_total else 0.0,
            "doctrine_hit_rate": self._coverage_doctrine[True] / self._coverage_total if self._coverage_total else 0.0,
            "error_counts": dict(self._coverage_errors),
            "error_rate": self._coverage_errors.total() / self._coverage_total if self._coverage_total else 0.0
        }
        return report

    def export_jsonl(self, path: Union[str, pathlib.Path]) -> int:
        path = pathlib.Path(path)
        count = 0
        with path.open("w", encoding="utf-8") as f:
            for q in self._queries:
                f.write(json.dumps(asdict(q)) + "\n")
                count += 1
            for err in self._errors:
                f.write(json.dumps(err) + "\n")
                count += 1
        logger.info(f"Exported {count} telemetry entries to {path}")
        return count

class AuditTrailWriter:
    def __init__(self, audit_dir: Union[str, pathlib.Path] = "audit_trail"):
        self.audit_dir = pathlib.Path(audit_dir)
        self.audit_dir.mkdir(exist_ok=True)
    
    def _get_audit_path(self, query_id: Optional[str]) -> pathlib.Path:
        if not query_id:
            query_id = hashlib.md5(str(time.time()).encode()).hexdigest()
        filename = f"{query_id}.jsonl"
        return self.audit_dir / filename

    def write(self, entry: Any):
        if isinstance(entry, QueryMetrics):
            query_id = entry.query_id
            data = asdict(entry)
        elif isinstance(entry, dict):
            query_id = entry.get("query_id", None)
            data = entry
        else:
            query_id = None
            data = entry
        path = self._get_audit_path(query_id)
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(data) + "\n")
        logger.debug(f"Wrote audit trail for query_id={query_id} to {path}")

COLLECTOR = TelemetryCollector()