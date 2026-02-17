import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "E12"

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
    def __init__(self, max_queries: int = 10000):
        self._queries: deque = deque(maxlen=max_queries)
        self._errors: deque = deque(maxlen=max_queries)
        self._query_index: Dict[str, QueryMetrics] = {}
        self._doctrine_hits: int = 0
        self._doctrine_total: int = 0
        self._latencies: List[float] = []
        self._error_types: Counter = Counter()
        self._audit_writer: Optional[AuditTrailWriter] = None
        self._coverage_modes: Counter = Counter()
        self._cache_hits: int = 0
        self._cache_total: int = 0

    def record_query(self, metrics: QueryMetrics):
        logger.debug(f"Recording query: {metrics.query_id}")
        self._queries.append(metrics)
        self._query_index[metrics.query_id] = metrics
        self._latencies.append(metrics.latency_ms)
        self._doctrine_total += 1
        if metrics.doctrine_matched:
            self._doctrine_hits += 1
        self._coverage_modes[metrics.mode] += 1
        self._cache_total += 1
        if metrics.cache_hit:
            self._cache_hits += 1
        if metrics.error:
            self.record_error("query_error", metrics.error, metrics.query_id)
        if self._audit_writer:
            self._audit_writer.write(metrics)
    
    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "error_type": error_type,
            "message": message,
            "query_id": query_id
        }
        logger.error(f"Error recorded: {error_entry}")
        self._errors.append(error_entry)
        self._error_types[error_type] += 1

    def get_latency_stats(self) -> Dict[str, Any]:
        if not self._latencies:
            return {
                "avg": None,
                "p50": None,
                "p95": None,
                "p99": None,
                "min": None,
                "max": None
            }
        latencies = sorted(self._latencies)
        avg = statistics.mean(latencies)
        min_latency = latencies[0]
        max_latency = latencies[-1]
        p50 = statistics.median(latencies)
        p95 = latencies[int(0.95 * len(latencies)) - 1]
        p99 = latencies[int(0.99 * len(latencies)) - 1]
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
        if self._doctrine_total == 0:
            return 0.0
        hit_rate = self._doctrine_hits / self._doctrine_total
        logger.info(f"Doctrine hit rate: {hit_rate}")
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        error_count = 0
        query_count = 0
        for q in self._queries:
            if q.timestamp >= window_start:
                query_count += 1
                if q.error:
                    error_count += 1
        if query_count == 0:
            return 0.0
        error_rate = error_count / query_count
        logger.info(f"Error rate ({window_hours}h): {error_rate}")
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= one_hour_ago)
        logger.info(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        total = sum(self._coverage_modes.values())
        report = {}
        for mode, count in self._coverage_modes.items():
            report[mode] = {
                "count": count,
                "percent": (count / total) * 100 if total else 0.0
            }
        logger.info(f"Coverage report: {report}")
        return report

    def export_jsonl(self, path: str) -> int:
        p = pathlib.Path(path)
        count = 0
        with p.open("w", encoding="utf-8") as f:
            for q in self._queries:
                f.write(json.dumps(dataclasses.asdict(q)) + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {path}")
        return count

    def set_audit_writer(self, writer: 'AuditTrailWriter'):
        self._audit_writer = writer

    def get_cache_hit_rate(self) -> float:
        if self._cache_total == 0:
            return 0.0
        return self._cache_hits / self._cache_total

    def get_error_types(self) -> Dict[str, int]:
        return dict(self._error_types)

    def get_query_by_id(self, query_id: str) -> Optional[QueryMetrics]:
        return self._query_index.get(query_id)

    def get_recent_queries(self, n: int = 100) -> List[QueryMetrics]:
        return list(self._queries)[-n:]

    def get_recent_errors(self, n: int = 100) -> List[Dict[str, Any]]:
        return list(self._errors)[-n:]

    def reset(self):
        self._queries.clear()
        self._errors.clear()
        self._query_index.clear()
        self._doctrine_hits = 0
        self._doctrine_total = 0
        self._latencies.clear()
        self._error_types.clear()
        self._coverage_modes.clear()
        self._cache_hits = 0
        self._cache_total = 0
        logger.info("TelemetryCollector reset.")

class AuditTrailWriter:
    def __init__(self, path: str):
        self.path = pathlib.Path(path)
        self._file = self.path.open("a", encoding="utf-8")
        logger.info(f"AuditTrailWriter initialized at {self.path}")

    def write(self, metrics: QueryMetrics):
        entry = dataclasses.asdict(metrics)
        entry["audit_hash"] = self._hash_query(entry)
        self._file.write(json.dumps(entry) + "\n")
        self._file.flush()
        logger.debug(f"Audit written for query {metrics.query_id}")

    def _hash_query(self, entry: Dict[str, Any]) -> str:
        relevant = {
            "query_id": entry["query_id"],
            "engine_id": entry["engine_id"],
            "timestamp": entry["timestamp"],
            "latency_ms": entry["latency_ms"],
            "cache_hit": entry["cache_hit"],
            "doctrine_matched": entry["doctrine_matched"],
            "mode": entry["mode"],
            "confidence": entry["confidence"],
            "error": entry.get("error")
        }
        raw = json.dumps(relevant, sort_keys=True)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def close(self):
        self._file.close()
        logger.info("AuditTrailWriter closed.")

    def __del__(self):
        try:
            self.close()
        except Exception:
            pass

COLLECTOR = TelemetryCollector()

# Optionally, set up an audit trail writer
# audit_writer = AuditTrailWriter("/tmp/e12_audit.jsonl")
# COLLECTOR.set_audit_writer(audit_writer)