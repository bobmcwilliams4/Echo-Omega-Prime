import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict, field
from typing import List, Optional, Dict, Any, Deque
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "REG12"

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
        self.audit_writer = AuditTrailWriter()
        self.lock = None  # Placeholder for thread safety if needed

    def record_query(self, metrics: QueryMetrics):
        logger.debug(f"Recording query: {metrics}")
        self.queries.append(metrics)
        self.audit_writer.write(metrics)
        if metrics.error:
            self.record_error(metrics.error, "Query error", metrics.query_id)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "engine_id": ENGINE_ID
        }
        logger.error(f"Recording error: {error_entry}")
        self.errors.append(error_entry)
        self.audit_writer.write_error(error_entry)

    def get_latency_stats(self) -> Dict[str, Optional[float]]:
        latencies = [q.latency_ms for q in self.queries if q.latency_ms is not None]
        if not latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = self._percentile(latencies_sorted, 95)
        p99 = self._percentile(latencies_sorted, 99)
        min_latency = latencies_sorted[0]
        max_latency = latencies_sorted[-1]
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
        k = (len(data) - 1) * percentile / 100
        f = int(k)
        c = min(f + 1, len(data) - 1)
        if f == c:
            return data[int(k)]
        d0 = data[f] * (c - k)
        d1 = data[c] * (k - f)
        return d0 + d1

    def get_doctrine_hit_rate(self) -> float:
        if not self.queries:
            return 0.0
        doctrine_hits = sum(1 for q in self.queries if q.doctrine_matched)
        hit_rate = doctrine_hits / len(self.queries)
        logger.debug(f"Doctrine hit rate: {hit_rate} ({doctrine_hits}/{len(self.queries)})")
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        total_queries = sum(1 for q in self.queries if q.timestamp >= window_start)
        total_errors = sum(1 for e in self.errors if e["timestamp"] >= window_start)
        if total_queries == 0:
            return 0.0
        error_rate = total_errors / total_queries
        logger.debug(f"Error rate: {error_rate} ({total_errors}/{total_queries}) in last {window_hours}h")
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self.queries if q.timestamp >= one_hour_ago)
        logger.debug(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        total = len(self.queries)
        if total == 0:
            return {
                "total": 0,
                "cache_hits": 0,
                "cache_hit_rate": 0.0,
                "doctrine_matched": 0,
                "doctrine_hit_rate": 0.0,
                "modes": {},
                "confidence_avg": None,
                "confidence_min": None,
                "confidence_max": None
            }
        cache_hits = sum(1 for q in self.queries if q.cache_hit)
        doctrine_matched = sum(1 for q in self.queries if q.doctrine_matched)
        mode_counter = Counter(q.mode for q in self.queries)
        confidences = [q.confidence for q in self.queries if q.confidence is not None]
        confidence_avg = statistics.mean(confidences) if confidences else None
        confidence_min = min(confidences) if confidences else None
        confidence_max = max(confidences) if confidences else None
        report = {
            "total": total,
            "cache_hits": cache_hits,
            "cache_hit_rate": cache_hits / total,
            "doctrine_matched": doctrine_matched,
            "doctrine_hit_rate": doctrine_matched / total,
            "modes": dict(mode_counter),
            "confidence_avg": confidence_avg,
            "confidence_min": confidence_min,
            "confidence_max": confidence_max
        }
        logger.debug(f"Coverage report: {report}")
        return report

    def export_jsonl(self, path: str) -> int:
        p = pathlib.Path(path)
        count = 0
        with p.open("w", encoding="utf-8") as f:
            for q in self.queries:
                f.write(json.dumps(asdict(q)) + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {path}")
        return count

class AuditTrailWriter:
    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = pathlib.Path(base_dir) if base_dir else pathlib.Path("audit_trail")
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.query_file = self.base_dir / "queries.jsonl"
        self.error_file = self.base_dir / "errors.jsonl"
        self._query_fh = None
        self._error_fh = None

    def _open_query_file(self):
        if self._query_fh is None:
            self._query_fh = self.query_file.open("a", encoding="utf-8")

    def _open_error_file(self):
        if self._error_fh is None:
            self._error_fh = self.error_file.open("a", encoding="utf-8")

    def write(self, metrics: QueryMetrics):
        self._open_query_file()
        entry = asdict(metrics)
        entry["audit_id"] = self._make_audit_id(entry)
        self._query_fh.write(json.dumps(entry) + "\n")
        self._query_fh.flush()
        logger.debug(f"Wrote query audit: {entry['audit_id']}")

    def write_error(self, error_entry: Dict[str, Any]):
        self._open_error_file()
        entry = dict(error_entry)
        entry["audit_id"] = self._make_audit_id(entry)
        self._error_fh.write(json.dumps(entry) + "\n")
        self._error_fh.flush()
        logger.debug(f"Wrote error audit: {entry['audit_id']}")

    def _make_audit_id(self, entry: Dict[str, Any]) -> str:
        s = json.dumps(entry, sort_keys=True)
        return hashlib.sha256(s.encode("utf-8")).hexdigest()

    def __del__(self):
        try:
            if self._query_fh:
                self._query_fh.close()
            if self._error_fh:
                self._error_fh.close()
        except Exception:
            pass

COLLECTOR = TelemetryCollector()