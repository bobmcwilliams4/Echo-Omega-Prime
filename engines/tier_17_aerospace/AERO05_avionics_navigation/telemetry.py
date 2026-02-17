import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Tuple
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "AERO05"

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
        self.metrics: deque = deque(maxlen=maxlen)
        self.errors: deque = deque(maxlen=maxlen)
        self.query_index: Dict[str, QueryMetrics] = {}
        self.error_counter: Counter = Counter()
        self.doctrine_counter: Counter = Counter()
        self.cache_counter: Counter = Counter()
        self.mode_counter: Counter = Counter()
        self.confidence_values: List[float] = []
        self.latency_values: List[float] = []
        self.last_query_times: deque = deque(maxlen=1000)
        self.coverage: Dict[str, Counter] = defaultdict(Counter)
        self.audit_writer = AuditTrailWriter()
        logger.info("TelemetryCollector initialized for ENGINE_ID={}", ENGINE_ID)

    def record_query(self, metrics: QueryMetrics):
        logger.debug("Recording query: {}", metrics)
        self.metrics.append(metrics)
        self.query_index[metrics.query_id] = metrics
        self.latency_values.append(metrics.latency_ms)
        self.cache_counter[metrics.cache_hit] += 1
        self.doctrine_counter[metrics.doctrine_matched] += 1
        self.mode_counter[metrics.mode] += 1
        self.confidence_values.append(metrics.confidence)
        self.last_query_times.append(metrics.timestamp)
        self.coverage[metrics.mode][metrics.doctrine_matched] += 1
        if metrics.error:
            self.record_error(error_type="query_error", message=metrics.error, query_id=metrics.query_id)
        self.audit_writer.write(metrics)
        logger.info("Query recorded: query_id={}", metrics.query_id)

    def record_error(self, error_type: str, message: str, query_id: Optional[str]):
        error_entry = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "timestamp": time.time(),
            "engine_id": ENGINE_ID
        }
        self.errors.append(error_entry)
        self.error_counter[error_type] += 1
        logger.error("Error recorded: {}", error_entry)
        self.audit_writer.write_error(error_entry)

    def get_latency_stats(self) -> Dict[str, Any]:
        if not self.latency_values:
            logger.warning("No latency values to compute stats.")
            return {}
        values = self.latency_values
        stats = {
            "avg": statistics.mean(values),
            "p50": statistics.median(values),
            "p95": statistics.quantiles(values, n=100)[94],
            "p99": statistics.quantiles(values, n=100)[98],
            "min": min(values),
            "max": max(values),
        }
        logger.debug("Latency stats computed: {}", stats)
        return stats

    def get_doctrine_hit_rate(self) -> float:
        total = sum(self.doctrine_counter.values())
        hits = self.doctrine_counter[True]
        hit_rate = hits / total if total > 0 else 0.0
        logger.debug("Doctrine hit rate: {} ({} hits / {} total)", hit_rate, hits, total)
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        error_count = 0
        query_count = 0
        for m in self.metrics:
            if m.timestamp >= window_start:
                query_count += 1
                if m.error:
                    error_count += 1
        error_rate = error_count / query_count if query_count > 0 else 0.0
        logger.debug("Error rate for last {} hours: {} ({} errors / {} queries)", window_hours, error_rate, error_count, query_count)
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for t in self.last_query_times if t >= one_hour_ago)
        logger.debug("Queries in last hour: {}", count)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {}
        for mode, doctrine_counts in self.coverage.items():
            total = sum(doctrine_counts.values())
            matched = doctrine_counts[True]
            unmatched = doctrine_counts[False]
            report[mode] = {
                "total": total,
                "matched": matched,
                "unmatched": unmatched,
                "match_rate": matched / total if total > 0 else 0.0
            }
        logger.debug("Coverage report: {}", report)
        return report

    def export_jsonl(self, path: str) -> int:
        p = pathlib.Path(path)
        count = 0
        with p.open("w") as f:
            for m in self.metrics:
                f.write(json.dumps(dataclass_to_dict(m)) + "\n")
                count += 1
        logger.info("Exported {} query metrics to {}", count, path)
        return count

def dataclass_to_dict(obj):
    if hasattr(obj, "__dataclass_fields__"):
        return {k: dataclass_to_dict(v) for k, v in obj.__dict__.items()}
    elif isinstance(obj, (list, tuple)):
        return [dataclass_to_dict(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: dataclass_to_dict(v) for k, v in obj.items()}
    else:
        return obj

class AuditTrailWriter:
    def __init__(self, base_path: str = "./audit_trail"):
        self.base_path = pathlib.Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        logger.info("AuditTrailWriter initialized at {}", self.base_path)

    def _get_query_path(self, query_id: str) -> pathlib.Path:
        hash_id = hashlib.sha256(query_id.encode()).hexdigest()
        subdir = hash_id[:2]
        dir_path = self.base_path / subdir
        dir_path.mkdir(exist_ok=True)
        file_path = dir_path / f"{hash_id}.jsonl"
        return file_path

    def write(self, metrics: QueryMetrics):
        file_path = self._get_query_path(metrics.query_id)
        with file_path.open("a") as f:
            f.write(json.dumps(dataclass_to_dict(metrics)) + "\n")
        logger.debug("Audit trail written for query_id={}", metrics.query_id)

    def write_error(self, error_entry: Dict[str, Any]):
        query_id = error_entry.get("query_id", "unknown")
        file_path = self._get_query_path(query_id)
        with file_path.open("a") as f:
            f.write(json.dumps(error_entry) + "\n")
        logger.debug("Audit trail error written for query_id={}", query_id)

COLLECTOR = TelemetryCollector()