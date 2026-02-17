import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any, Union
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "MECH15"

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
    def __init__(self, engine_id: str = ENGINE_ID, maxlen: int = 10000):
        self.engine_id = engine_id
        self._queries = deque(maxlen=maxlen)
        self._errors = deque(maxlen=maxlen)
        self._audit_trail = []
        self._query_counter = Counter()
        self._doctrine_hits = 0
        self._total_queries = 0
        self._latencies = []
        self._cache_hits = 0
        self._coverage_modes = defaultdict(int)
        self._confidence_scores = []
        self._error_types = Counter()
        self._last_export_path = None

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._query_counter[metrics.query_id] += 1
        self._total_queries += 1
        self._latencies.append(metrics.latency_ms)
        self._cache_hits += int(metrics.cache_hit)
        self._doctrine_hits += int(metrics.doctrine_matched)
        self._coverage_modes[metrics.mode] += 1
        self._confidence_scores.append(metrics.confidence)
        if metrics.error:
            self.record_error("query_error", metrics.error, metrics.query_id)
        logger.debug(f"Recorded query: {metrics}")

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "timestamp": time.time(),
            "engine_id": self.engine_id
        }
        self._errors.append(error_entry)
        self._error_types[error_type] += 1
        logger.error(f"Error recorded: {error_entry}")

    def get_latency_stats(self) -> Dict[str, Union[float, None]]:
        latencies = [m.latency_ms for m in self._queries if m.latency_ms is not None]
        if not latencies:
            return dict(avg=None, p50=None, p95=None, p99=None, min=None, max=None)
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = latencies_sorted[int(len(latencies_sorted) * 0.95) - 1]
        p99 = latencies_sorted[int(len(latencies_sorted) * 0.99) - 1]
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

    def get_doctrine_hit_rate(self) -> float:
        if self._total_queries == 0:
            return 0.0
        return self._doctrine_hits / self._total_queries

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        queries_in_window = [m for m in self._queries if m.timestamp >= window_start]
        total_queries = len(queries_in_window)
        if total_queries == 0:
            return 0.0
        return len(errors_in_window) / total_queries

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for m in self._queries if m.timestamp >= one_hour_ago)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {
            "total_queries": self._total_queries,
            "cache_hit_rate": self._cache_hits / self._total_queries if self._total_queries else 0.0,
            "doctrine_hit_rate": self.get_doctrine_hit_rate(),
            "mode_distribution": dict(self._coverage_modes),
            "confidence_avg": statistics.mean(self._confidence_scores) if self._confidence_scores else None,
            "confidence_min": min(self._confidence_scores) if self._confidence_scores else None,
            "confidence_max": max(self._confidence_scores) if self._confidence_scores else None,
            "error_types": dict(self._error_types),
            "latency_stats": self.get_latency_stats(),
        }
        return report

    def export_jsonl(self, path: Union[str, pathlib.Path]) -> int:
        path = pathlib.Path(path)
        count = 0
        with path.open('w', encoding='utf-8') as f:
            for m in self._queries:
                f.write(json.dumps(asdict(m)) + '\n')
                count += 1
        self._last_export_path = str(path)
        logger.info(f"Exported {count} queries to {path}")
        return count

    def audit_trail(self) -> List[Dict[str, Any]]:
        return [asdict(m) for m in self._queries]

    def get_last_export_path(self) -> Optional[str]:
        return self._last_export_path

class AuditTrailWriter:
    def __init__(self, audit_dir: Union[str, pathlib.Path]):
        self.audit_dir = pathlib.Path(audit_dir)
        self.audit_dir.mkdir(parents=True, exist_ok=True)

    def write(self, metrics: QueryMetrics):
        filename = f"{metrics.query_id}_{int(metrics.timestamp)}.jsonl"
        path = self.audit_dir / filename
        with path.open('w', encoding='utf-8') as f:
            f.write(json.dumps(asdict(metrics)) + '\n')
        logger.info(f"Audit trail written: {path}")

COLLECTOR = TelemetryCollector(engine_id=ENGINE_ID)