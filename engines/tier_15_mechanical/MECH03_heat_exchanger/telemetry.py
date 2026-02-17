import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Union
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "MECH03"

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
    def __init__(self, max_queries: int = 10000, max_errors: int = 1000):
        self.queries: deque = deque(maxlen=max_queries)
        self.errors: deque = deque(maxlen=max_errors)
        self.query_index: Dict[str, QueryMetrics] = {}
        self.error_index: Dict[str, Dict[str, Any]] = {}
        self.audit_writer = AuditTrailWriter()
        self.latency_list: List[float] = []
        self.doctrine_hits: List[bool] = []
        self.cache_hits: List[bool] = []
        self.confidences: List[float] = []
        self.modes: Counter = Counter()
        self.coverage: Dict[str, Counter] = defaultdict(Counter)
        self.last_query_time: Optional[float] = None

    def record_query(self, metrics: QueryMetrics):
        logger.debug(f"Recording query: {metrics}")
        self.queries.append(metrics)
        self.query_index[metrics.query_id] = metrics
        self.latency_list.append(metrics.latency_ms)
        self.doctrine_hits.append(metrics.doctrine_matched)
        self.cache_hits.append(metrics.cache_hit)
        self.confidences.append(metrics.confidence)
        self.modes[metrics.mode] += 1
        self.coverage[metrics.mode]['total'] += 1
        if metrics.doctrine_matched:
            self.coverage[metrics.mode]['doctrine_matched'] += 1
        if metrics.cache_hit:
            self.coverage[metrics.mode]['cache_hit'] += 1
        if metrics.error:
            self.coverage[metrics.mode]['error'] += 1
        self.last_query_time = metrics.timestamp
        self.audit_writer.write(metrics)
    
    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "error_type": error_type,
            "message": message,
            "timestamp": time.time(),
            "query_id": query_id,
            "engine_id": ENGINE_ID
        }
        logger.error(f"Recording error: {error_entry}")
        self.errors.append(error_entry)
        error_hash = hashlib.sha256(json.dumps(error_entry, sort_keys=True).encode()).hexdigest()
        self.error_index[error_hash] = error_entry
        if query_id and query_id in self.query_index:
            self.query_index[query_id].error = error_type
        self.audit_writer.write_error(error_entry)

    def get_latency_stats(self) -> Dict[str, Union[float, None]]:
        if not self.latency_list:
            return dict(avg=None, p50=None, p95=None, p99=None, min=None, max=None)
        latencies = sorted(self.latency_list)
        avg = statistics.mean(latencies)
        min_latency = latencies[0]
        max_latency = latencies[-1]
        p50 = statistics.median(latencies)
        p95 = latencies[int(0.95 * len(latencies)) - 1]
        p99 = latencies[int(0.99 * len(latencies)) - 1]
        return dict(
            avg=avg,
            p50=p50,
            p95=p95,
            p99=p99,
            min=min_latency,
            max=max_latency
        )

    def get_doctrine_hit_rate(self) -> float:
        if not self.doctrine_hits:
            return 0.0
        return sum(self.doctrine_hits) / len(self.doctrine_hits)

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        queries_in_window = [q for q in self.queries if q.timestamp >= window_start]
        if not queries_in_window:
            return 0.0
        errors_in_window = [q for q in queries_in_window if q.error]
        return len(errors_in_window) / len(queries_in_window)

    def queries_last_hour(self) -> int:
        now = time.time()
        window_start = now - 3600
        return sum(1 for q in self.queries if q.timestamp >= window_start)

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {}
        for mode, counts in self.coverage.items():
            total = counts['total']
            doctrine_matched = counts.get('doctrine_matched', 0)
            cache_hit = counts.get('cache_hit', 0)
            error = counts.get('error', 0)
            report[mode] = {
                "total": total,
                "doctrine_matched": doctrine_matched,
                "doctrine_hit_rate": doctrine_matched / total if total else 0.0,
                "cache_hit": cache_hit,
                "cache_hit_rate": cache_hit / total if total else 0.0,
                "error": error,
                "error_rate": error / total if total else 0.0
            }
        return report

    def export_jsonl(self, path: Union[str, pathlib.Path]) -> int:
        path = pathlib.Path(path)
        logger.info(f"Exporting telemetry to {path}")
        count = 0
        with path.open('w', encoding='utf-8') as f:
            for q in self.queries:
                f.write(json.dumps(dataclasses.asdict(q)) + '\n')
                count += 1
        logger.info(f"Exported {count} queries to {path}")
        return count

class AuditTrailWriter:
    def __init__(self, audit_dir: Union[str, pathlib.Path] = "./audit_trail"):
        self.audit_dir = pathlib.Path(audit_dir)
        self.audit_dir.mkdir(parents=True, exist_ok=True)
        self.query_audit_path = self.audit_dir / "query_audit.jsonl"
        self.error_audit_path = self.audit_dir / "error_audit.jsonl"
        self._query_file = None
        self._error_file = None

    def _open_query_file(self):
        if self._query_file is None:
            self._query_file = self.query_audit_path.open('a', encoding='utf-8')
        return self._query_file

    def _open_error_file(self):
        if self._error_file is None:
            self._error_file = self.error_audit_path.open('a', encoding='utf-8')
        return self._error_file

    def write(self, metrics: QueryMetrics):
        entry = dataclasses.asdict(metrics)
        entry['audit_timestamp'] = time.time()
        f = self._open_query_file()
        f.write(json.dumps(entry) + '\n')
        f.flush()
        logger.debug(f"Wrote query audit: {entry}")

    def write_error(self, error_entry: Dict[str, Any]):
        entry = error_entry.copy()
        entry['audit_timestamp'] = time.time()
        f = self._open_error_file()
        f.write(json.dumps(entry) + '\n')
        f.flush()
        logger.debug(f"Wrote error audit: {entry}")

    def close(self):
        if self._query_file:
            self._query_file.close()
            self._query_file = None
        if self._error_file:
            self._error_file.close()
            self._error_file = None

COLLECTOR = TelemetryCollector()

# Optionally, ensure audit files are closed on shutdown
import atexit
atexit.register(lambda: COLLECTOR.audit_writer.close())