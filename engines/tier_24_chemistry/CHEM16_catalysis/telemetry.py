import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict, field
from typing import Optional, List, Dict, Any, Deque
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "CHEM16"

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
        self._query_metrics: Deque[QueryMetrics] = deque(maxlen=maxlen)
        self._errors: Deque[Dict[str, Any]] = deque(maxlen=maxlen)
        self._doctrine_counter: Counter = Counter()
        self._cache_counter: Counter = Counter()
        self._mode_counter: Counter = Counter()
        self._confidence_values: List[float] = []
        self._latencies: List[float] = []
        self._coverage: Dict[str, set] = defaultdict(set)
        self._query_ids: set = set()
        self._audit_writer = AuditTrailWriter()
        logger.info("TelemetryCollector initialized with maxlen={}", maxlen)

    def record_query(self, metrics: QueryMetrics):
        logger.debug("Recording query: {}", metrics)
        self._query_metrics.append(metrics)
        self._query_ids.add(metrics.query_id)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_counter[metrics.doctrine_matched] += 1
        self._cache_counter[metrics.cache_hit] += 1
        self._mode_counter[metrics.mode] += 1
        self._confidence_values.append(metrics.confidence)
        self._coverage[metrics.mode].add(metrics.query_id)
        self._audit_writer.write(metrics)
        logger.debug("Query recorded. Current queries stored: {}", len(self._query_metrics))

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "engine_id": ENGINE_ID
        }
        self._errors.append(error_entry)
        logger.error("Error recorded: {}", error_entry)

    def get_latency_stats(self) -> dict:
        if not self._latencies:
            logger.warning("No latency data to compute stats.")
            return {
                "avg": None,
                "p50": None,
                "p95": None,
                "p99": None,
                "min": None,
                "max": None
            }
        lat_sorted = sorted(self._latencies)
        avg = statistics.mean(self._latencies)
        min_v = lat_sorted[0]
        max_v = lat_sorted[-1]
        p50 = statistics.median(lat_sorted)
        p95 = lat_sorted[int(0.95 * len(lat_sorted)) - 1]
        p99 = lat_sorted[int(0.99 * len(lat_sorted)) - 1]
        stats = {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_v,
            "max": max_v
        }
        logger.info("Latency stats computed: {}", stats)
        return stats

    def get_doctrine_hit_rate(self) -> float:
        total = self._doctrine_counter[True] + self._doctrine_counter[False]
        if total == 0:
            logger.warning("No doctrine match data.")
            return 0.0
        hit_rate = self._doctrine_counter[True] / total
        logger.info("Doctrine hit rate: {:.2%}", hit_rate)
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        total_queries = sum(1 for m in self._query_metrics if m.timestamp >= window_start)
        total_errors = sum(1 for e in self._errors if e["timestamp"] >= window_start)
        if total_queries == 0:
            logger.warning("No queries in the last {} hours.", window_hours)
            return 0.0
        error_rate = total_errors / total_queries
        logger.info("Error rate over last {} hours: {:.2%}", window_hours, error_rate)
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for m in self._query_metrics if m.timestamp >= one_hour_ago)
        logger.info("Queries in the last hour: {}", count)
        return count

    def get_coverage_report(self) -> dict:
        report = {}
        for mode, qids in self._coverage.items():
            report[mode] = len(qids)
        logger.info("Coverage report: {}", report)
        return report

    def export_jsonl(self, path: str) -> int:
        output_path = pathlib.Path(path)
        count = 0
        with output_path.open("w", encoding="utf-8") as f:
            for metrics in self._query_metrics:
                f.write(json.dumps(asdict(metrics)) + "\n")
                count += 1
        logger.info("Exported {} query metrics to {}", count, path)
        return count

class AuditTrailWriter:
    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = pathlib.Path(base_dir) if base_dir else pathlib.Path("./audit_trails")
        self.base_dir.mkdir(parents=True, exist_ok=True)
        logger.info("AuditTrailWriter initialized at {}", self.base_dir)

    def write(self, metrics: QueryMetrics):
        audit_entry = asdict(metrics)
        audit_entry["audit_id"] = self._compute_audit_id(metrics)
        audit_entry["audit_timestamp"] = time.time()
        filename = self._get_audit_filename(metrics.query_id)
        with open(filename, "a", encoding="utf-8") as f:
            f.write(json.dumps(audit_entry) + "\n")
        logger.debug("Audit trail written for query_id={} at {}", metrics.query_id, filename)

    def _compute_audit_id(self, metrics: QueryMetrics) -> str:
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

    def _get_audit_filename(self, query_id: str) -> str:
        # Use first 2 chars of query_id as subdir for sharding
        subdir = self.base_dir / query_id[:2]
        subdir.mkdir(exist_ok=True)
        filename = subdir / f"{query_id}.jsonl"
        return str(filename)

COLLECTOR = TelemetryCollector()