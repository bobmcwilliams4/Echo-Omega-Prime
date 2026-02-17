import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "GS04"

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
        self.queries: deque = deque(maxlen=max_queries)
        self.errors: deque = deque(maxlen=max_queries)
        self.doctrine_hits: deque = deque(maxlen=max_queries)
        self.audit_writer = AuditTrailWriter()
        self.query_counter: Counter = Counter()
        self.error_counter: Counter = Counter()
        self.coverage: defaultdict = defaultdict(set)
        logger.info(f"TelemetryCollector initialized for engine {ENGINE_ID}")

    def record_query(self, metrics: QueryMetrics):
        self.queries.append(metrics)
        self.doctrine_hits.append(metrics.doctrine_matched)
        self.query_counter[metrics.mode] += 1
        self.coverage[metrics.mode].add(metrics.query_id)
        self.audit_writer.write(metrics)
        logger.debug(f"Recorded query: {metrics.query_id}, latency: {metrics.latency_ms} ms")

    def record_error(self, error_type: str, message: str, query_id: str):
        error_record = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "timestamp": time.time(),
            "engine_id": ENGINE_ID
        }
        self.errors.append(error_record)
        self.error_counter[error_type] += 1
        logger.warning(f"Error recorded: {error_type} for query {query_id}: {message}")

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = [q.latency_ms for q in self.queries if q.latency_ms is not None]
        if not latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = latencies_sorted[int(len(latencies_sorted) * 0.95) - 1]
        p99 = latencies_sorted[int(len(latencies_sorted) * 0.99) - 1]
        min_latency = min(latencies)
        max_latency = max(latencies)
        logger.info(f"Latency stats: avg={avg}, p50={p50}, p95={p95}, p99={p99}, min={min_latency}, max={max_latency}")
        return {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_latency,
            "max": max_latency
        }

    def get_doctrine_hit_rate(self) -> float:
        total = len(self.doctrine_hits)
        if total == 0:
            return 0.0
        hits = sum(1 for hit in self.doctrine_hits if hit)
        hit_rate = hits / total
        logger.info(f"Doctrine hit rate: {hit_rate:.3f} ({hits}/{total})")
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        error_count = sum(1 for e in self.errors if e["timestamp"] >= window_start)
        query_count = sum(1 for q in self.queries if q.timestamp >= window_start)
        if query_count == 0:
            return 0.0
        error_rate = error_count / query_count
        logger.info(f"Error rate over last {window_hours} hour(s): {error_rate:.3f} ({error_count}/{query_count})")
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self.queries if q.timestamp >= one_hour_ago)
        logger.info(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {}
        for mode, queries in self.coverage.items():
            report[mode] = {
                "unique_queries": len(queries),
                "total_queries": self.query_counter[mode]
            }
        logger.info(f"Coverage report generated: {report}")
        return report

    def export_jsonl(self, path: str) -> int:
        output_path = pathlib.Path(path)
        count = 0
        with output_path.open("w", encoding="utf-8") as f:
            for q in self.queries:
                f.write(json.dumps(asdict(q)) + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {output_path}")
        return count

class AuditTrailWriter:
    def __init__(self, base_dir: str = "audit_trail"):
        self.base_dir = pathlib.Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"AuditTrailWriter initialized at {self.base_dir}")

    def write(self, metrics: QueryMetrics):
        query_hash = hashlib.sha256(metrics.query_id.encode()).hexdigest()
        filename = f"{ENGINE_ID}_{query_hash}.jsonl"
        file_path = self.base_dir / filename
        with file_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(metrics)) + "\n")
        logger.debug(f"Audit trail written for query {metrics.query_id} at {file_path}")

COLLECTOR = TelemetryCollector()