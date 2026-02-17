import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional, Any, Deque
from collections import deque, defaultdict, Counter
from loguru import logger

ENGINE_ID = "BLD05"

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
    def __init__(self, maxlen: int = 100_000):
        self.metrics: Deque[QueryMetrics] = deque(maxlen=maxlen)
        self.errors: Deque[Dict[str, Any]] = deque(maxlen=maxlen)
        self.latencies: Deque[float] = deque(maxlen=maxlen)
        self.doctrine_matches: Deque[bool] = deque(maxlen=maxlen)
        self.cache_hits: Deque[bool] = deque(maxlen=maxlen)
        self.confidences: Deque[float] = deque(maxlen=maxlen)
        self.modes: Deque[str] = deque(maxlen=maxlen)
        self.timestamps: Deque[float] = deque(maxlen=maxlen)
        self.query_ids: Deque[str] = deque(maxlen=maxlen)
        self._audit_writer = AuditTrailWriter()
        self._error_counter = Counter()
        self._doctrine_total = 0
        self._doctrine_matched = 0

    def record_query(self, metrics: QueryMetrics):
        self.metrics.append(metrics)
        self.latencies.append(metrics.latency_ms)
        self.doctrine_matches.append(metrics.doctrine_matched)
        self.cache_hits.append(metrics.cache_hit)
        self.confidences.append(metrics.confidence)
        self.modes.append(metrics.mode)
        self.timestamps.append(metrics.timestamp)
        self.query_ids.append(metrics.query_id)
        self._doctrine_total += 1
        if metrics.doctrine_matched:
            self._doctrine_matched += 1
        self._audit_writer.write(metrics)
        if metrics.error:
            self.record_error(metrics.error, "Query error", metrics.query_id)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_event = {
            "timestamp": time.time(),
            "engine_id": ENGINE_ID,
            "error_type": error_type,
            "message": message,
            "query_id": query_id
        }
        self.errors.append(error_event)
        self._error_counter[error_type] += 1
        logger.error(f"Error recorded: {error_event}")

    def get_latency_stats(self) -> Dict[str, float]:
        if not self.latencies:
            return {"avg": 0, "p50": 0, "p95": 0, "p99": 0, "min": 0, "max": 0}
        data = list(self.latencies)
        data.sort()
        avg = statistics.mean(data)
        min_v = data[0]
        max_v = data[-1]
        p50 = statistics.median(data)
        p95 = data[int(0.95 * len(data)) - 1]
        p99 = data[int(0.99 * len(data)) - 1]
        return {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_v,
            "max": max_v
        }

    def get_doctrine_hit_rate(self) -> float:
        if self._doctrine_total == 0:
            return 0.0
        return self._doctrine_matched / self._doctrine_total

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - (window_hours * 3600)
        total_queries = 0
        error_count = 0
        for m in self.metrics:
            if m.timestamp >= window_start:
                total_queries += 1
                if m.error:
                    error_count += 1
        if total_queries == 0:
            return 0.0
        return error_count / total_queries

    def queries_last_hour(self) -> int:
        now = time.time()
        window_start = now - 3600
        count = 0
        for m in self.metrics:
            if m.timestamp >= window_start:
                count += 1
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        mode_counter = Counter(self.modes)
        cache_counter = Counter(self.cache_hits)
        doctrine_counter = Counter(self.doctrine_matches)
        confidence_list = list(self.confidences)
        report = {
            "total_queries": len(self.metrics),
            "modes": dict(mode_counter),
            "cache_hits": dict(cache_counter),
            "doctrine_matches": dict(doctrine_counter),
            "confidence_avg": statistics.mean(confidence_list) if confidence_list else 0.0,
            "confidence_min": min(confidence_list) if confidence_list else 0.0,
            "confidence_max": max(confidence_list) if confidence_list else 0.0,
            "unique_query_ids": len(set(self.query_ids)),
        }
        return report

    def export_jsonl(self, path: str) -> int:
        output_path = pathlib.Path(path)
        count = 0
        with output_path.open("w", encoding="utf-8") as f:
            for m in self.metrics:
                f.write(json.dumps(asdict(m)) + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {output_path}")
        return count

class AuditTrailWriter:
    def __init__(self, base_dir: str = "./telemetry_audit"):
        self.base_dir = pathlib.Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _get_audit_path(self, query_id: str) -> pathlib.Path:
        # Use hash to avoid too many files in one dir
        h = hashlib.sha1(query_id.encode()).hexdigest()[:2]
        dir_path = self.base_dir / h
        dir_path.mkdir(parents=True, exist_ok=True)
        return dir_path / f"{query_id}.jsonl"

    def write(self, metrics: QueryMetrics):
        path = self._get_audit_path(metrics.query_id)
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(metrics)) + "\n")
        logger.debug(f"Audit trail written for query_id={metrics.query_id}")

COLLECTOR = TelemetryCollector()