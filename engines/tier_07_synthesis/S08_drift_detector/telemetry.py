import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional, Any
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "S08"

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
    def __init__(self, max_queries: int = 100000, max_errors: int = 10000):
        self.queries: deque = deque(maxlen=max_queries)
        self.errors: deque = deque(maxlen=max_errors)
        self.query_counter: Counter = Counter()
        self.doctrine_counter: Counter = Counter()
        self.cache_counter: Counter = Counter()
        self.error_counter: Counter = Counter()
        self.latencies: List[float] = []
        self.coverage: defaultdict = defaultdict(set)
        self.audit_writer = AuditTrailWriter()
        logger.info("TelemetryCollector initialized.")

    def record_query(self, metrics: QueryMetrics):
        self.queries.append(metrics)
        self.latencies.append(metrics.latency_ms)
        self.query_counter[metrics.query_id] += 1
        self.doctrine_counter[metrics.doctrine_matched] += 1
        self.cache_counter[metrics.cache_hit] += 1
        if metrics.error:
            self.error_counter[metrics.error] += 1
        self.coverage[metrics.mode].add(metrics.query_id)
        self.audit_writer.write(metrics)
        logger.debug(f"Recorded query: {metrics}")

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "error_type": error_type,
            "message": message,
            "timestamp": time.time(),
            "query_id": query_id
        }
        self.errors.append(error_entry)
        self.error_counter[error_type] += 1
        logger.error(f"Recorded error: {error_entry}")

    def get_latency_stats(self) -> Dict[str, Any]:
        if not self.latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        lat_sorted = sorted(self.latencies)
        avg = statistics.mean(lat_sorted)
        p50 = statistics.median(lat_sorted)
        p95 = lat_sorted[int(len(lat_sorted) * 0.95)-1] if len(lat_sorted) > 1 else lat_sorted[0]
        p99 = lat_sorted[int(len(lat_sorted) * 0.99)-1] if len(lat_sorted) > 1 else lat_sorted[0]
        min_lat = min(lat_sorted)
        max_lat = max(lat_sorted)
        stats = {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_lat,
            "max": max_lat
        }
        logger.info(f"Latency stats: {stats}")
        return stats

    def get_doctrine_hit_rate(self) -> float:
        total = sum(self.doctrine_counter.values())
        hits = self.doctrine_counter.get(True, 0)
        rate = hits / total if total else 0.0
        logger.info(f"Doctrine hit rate: {rate}")
        return rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        total_queries = sum(1 for q in self.queries if q.timestamp >= window_start)
        total_errors = sum(1 for e in self.errors if e["timestamp"] >= window_start)
        rate = total_errors / total_queries if total_queries else 0.0
        logger.info(f"Error rate (last {window_hours}h): {rate}")
        return rate

    def queries_last_hour(self) -> int:
        now = time.time()
        window_start = now - 3600
        count = sum(1 for q in self.queries if q.timestamp >= window_start)
        logger.info(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {}
        for mode, queries in self.coverage.items():
            report[mode] = {
                "unique_queries": len(queries),
                "total_queries": sum(1 for q in self.queries if q.mode == mode)
            }
        logger.info(f"Coverage report: {report}")
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
    def __init__(self, audit_dir: str = "audit_trail"):
        self.audit_dir = pathlib.Path(audit_dir)
        self.audit_dir.mkdir(exist_ok=True)
        logger.info(f"AuditTrailWriter initialized at {self.audit_dir}")

    def _get_audit_path(self, query_id: str) -> pathlib.Path:
        hash_id = hashlib.sha256(query_id.encode()).hexdigest()
        filename = f"{hash_id}.jsonl"
        return self.audit_dir / filename

    def write(self, metrics: QueryMetrics):
        path = self._get_audit_path(metrics.query_id)
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(metrics)) + "\n")
        logger.debug(f"Wrote audit trail for query {metrics.query_id} to {path}")

COLLECTOR = TelemetryCollector()