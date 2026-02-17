import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "REG09"

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
        self._query_ids: set = set()
        self._audit_trail_writer: Optional[AuditTrailWriter] = None

    def record_query(self, metrics: QueryMetrics):
        logger.debug(f"Recording query: {metrics}")
        self._queries.append(metrics)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._query_ids.add(metrics.query_id)
        if metrics.error:
            self.record_error(error_type="query_error", message=metrics.error, query_id=metrics.query_id)
        if self._audit_trail_writer:
            self._audit_trail_writer.write(metrics)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "engine_id": ENGINE_ID
        }
        logger.error(f"Recording error: {error_entry}")
        self._errors.append(error_entry)

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = list(self._latencies)
        if not latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = latencies_sorted[int(0.95 * len(latencies_sorted)) - 1]
        p99 = latencies_sorted[int(0.99 * len(latencies_sorted)) - 1]
        min_latency = min(latencies)
        max_latency = max(latencies)
        stats = {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_latency,
            "max": max_latency
        }
        logger.info(f"Latency stats: {stats}")
        return stats

    def get_doctrine_hit_rate(self) -> float:
        hits = list(self._doctrine_hits)
        if not hits:
            return 0.0
        hit_count = sum(1 for h in hits if h)
        hit_rate = hit_count / len(hits)
        logger.info(f"Doctrine hit rate: {hit_rate}")
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        queries_in_window = [q for q in self._queries if q.timestamp >= window_start]
        if not queries_in_window:
            return 0.0
        error_rate = len(errors_in_window) / len(queries_in_window)
        logger.info(f"Error rate in last {window_hours} hours: {error_rate}")
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        window_start = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= window_start)
        logger.info(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        modes = Counter()
        confidence_bins = defaultdict(int)
        doctrine_matched_count = 0
        cache_hit_count = 0
        total = 0
        for q in self._queries:
            modes[q.mode] += 1
            bin_label = self._confidence_bin(q.confidence)
            confidence_bins[bin_label] += 1
            if q.doctrine_matched:
                doctrine_matched_count += 1
            if q.cache_hit:
                cache_hit_count += 1
            total += 1
        report = {
            "mode_distribution": dict(modes),
            "confidence_bins": dict(confidence_bins),
            "doctrine_matched": doctrine_matched_count,
            "cache_hit": cache_hit_count,
            "total_queries": total
        }
        logger.info(f"Coverage report: {report}")
        return report

    def _confidence_bin(self, confidence: float) -> str:
        if confidence >= 0.95:
            return "0.95-1.0"
        elif confidence >= 0.9:
            return "0.90-0.95"
        elif confidence >= 0.8:
            return "0.80-0.90"
        elif confidence >= 0.6:
            return "0.60-0.80"
        else:
            return "<0.60"

    def export_jsonl(self, path: str) -> int:
        p = pathlib.Path(path)
        count = 0
        with p.open("w", encoding="utf-8") as f:
            for q in self._queries:
                f.write(json.dumps(dataclasses.asdict(q)) + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {path}")
        return count

    def set_audit_trail_writer(self, writer: 'AuditTrailWriter'):
        self._audit_trail_writer = writer

class AuditTrailWriter:
    def __init__(self, path: str):
        self.path = pathlib.Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._file = self.path.open("a", encoding="utf-8")
        logger.info(f"Audit trail writer initialized at {self.path}")

    def write(self, metrics: QueryMetrics):
        entry = dataclasses.asdict(metrics)
        entry["audit_hash"] = self._hash_entry(entry)
        self._file.write(json.dumps(entry) + "\n")
        self._file.flush()
        logger.debug(f"Wrote audit trail entry for query_id={metrics.query_id}")

    def _hash_entry(self, entry: Dict[str, Any]) -> str:
        entry_copy = dict(entry)
        entry_copy.pop("audit_hash", None)
        serialized = json.dumps(entry_copy, sort_keys=True)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    def close(self):
        self._file.close()
        logger.info(f"Audit trail writer closed at {self.path}")

COLLECTOR = TelemetryCollector(maxlen=20000)