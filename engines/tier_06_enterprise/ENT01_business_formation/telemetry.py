import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict, field
from typing import Optional, List, Dict, Any
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "ENT01"


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
        self.metrics: deque[QueryMetrics] = deque(maxlen=maxlen)
        self.errors: deque[Dict[str, Any]] = deque(maxlen=maxlen)
        self.audit_writer = AuditTrailWriter()
        self._doctrine_hits: int = 0
        self._doctrine_total: int = 0
        self._cache_hits: int = 0
        self._cache_total: int = 0
        self._error_counter: Counter = Counter()
        self._mode_counter: Counter = Counter()
        self._confidence_list: List[float] = []
        self._coverage_modes: set = set()
        self._coverage_doctrines: set = set()
        self._coverage_queries: set = set()

    def record_query(self, metrics: QueryMetrics):
        self.metrics.append(metrics)
        self._mode_counter[metrics.mode] += 1
        self._confidence_list.append(metrics.confidence)
        self._coverage_modes.add(metrics.mode)
        self._coverage_queries.add(metrics.query_id)
        if metrics.doctrine_matched:
            self._doctrine_hits += 1
            self._coverage_doctrines.add(metrics.query_id)
        self._doctrine_total += 1
        if metrics.cache_hit:
            self._cache_hits += 1
        self._cache_total += 1
        if metrics.error:
            self._error_counter[metrics.error] += 1
        self.audit_writer.write(metrics)
        logger.debug(f"Recorded query: {metrics}")

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "timestamp": time.time(),
            "engine_id": ENGINE_ID
        }
        self.errors.append(error_entry)
        self._error_counter[error_type] += 1
        logger.error(f"Error recorded: {error_entry}")

    def get_latency_stats(self) -> Dict[str, float]:
        latencies = [m.latency_ms for m in self.metrics if m.latency_ms is not None]
        if not latencies:
            return dict(avg=0, p50=0, p95=0, p99=0, min=0, max=0)
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        minv = latencies_sorted[0]
        maxv = latencies_sorted[-1]
        p50 = statistics.median(latencies)
        p95 = latencies_sorted[int(0.95 * len(latencies_sorted)) - 1]
        p99 = latencies_sorted[int(0.99 * len(latencies_sorted)) - 1]
        stats = dict(
            avg=avg,
            p50=p50,
            p95=p95,
            p99=p99,
            min=minv,
            max=maxv
        )
        logger.debug(f"Latency stats: {stats}")
        return stats

    def get_doctrine_hit_rate(self) -> float:
        if self._doctrine_total == 0:
            return 0.0
        hit_rate = self._doctrine_hits / self._doctrine_total
        logger.debug(f"Doctrine hit rate: {hit_rate}")
        return hit_rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        cutoff = time.time() - window_hours * 3600
        errors_in_window = [e for e in self.errors if e["timestamp"] >= cutoff]
        queries_in_window = [m for m in self.metrics if m.timestamp >= cutoff]
        if not queries_in_window:
            return 0.0
        error_rate = len(errors_in_window) / len(queries_in_window)
        logger.debug(f"Error rate in last {window_hours}h: {error_rate}")
        return error_rate

    def queries_last_hour(self) -> int:
        cutoff = time.time() - 3600
        count = sum(1 for m in self.metrics if m.timestamp >= cutoff)
        logger.debug(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {
            "modes_covered": list(self._coverage_modes),
            "doctrine_coverage_count": len(self._coverage_doctrines),
            "unique_queries": len(self._coverage_queries),
            "total_queries": len(self.metrics),
            "mode_counts": dict(self._mode_counter),
            "confidence_stats": self._confidence_stats()
        }
        logger.debug(f"Coverage report: {report}")
        return report

    def _confidence_stats(self) -> Dict[str, float]:
        if not self._confidence_list:
            return dict(avg=0, min=0, max=0)
        avg = statistics.mean(self._confidence_list)
        minv = min(self._confidence_list)
        maxv = max(self._confidence_list)
        return dict(avg=avg, min=minv, max=maxv)

    def export_jsonl(self, path: str) -> int:
        p = pathlib.Path(path)
        count = 0
        with p.open("w", encoding="utf-8") as f:
            for m in self.metrics:
                f.write(json.dumps(asdict(m)) + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {path}")
        return count


class AuditTrailWriter:
    def __init__(self, base_dir: Optional[str] = None):
        if base_dir is None:
            base_dir = "./audit_trail"
        self.base_dir = pathlib.Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def write(self, metrics: QueryMetrics):
        # Use query_id as filename, hash if too long
        query_id = metrics.query_id
        if len(query_id) > 64:
            query_id = hashlib.sha256(query_id.encode()).hexdigest()
        filename = f"{ENGINE_ID}_{query_id}.jsonl"
        path = self.base_dir / filename
        entry = asdict(metrics)
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        logger.debug(f"Audit trail written for query {metrics.query_id} at {path}")


COLLECTOR = TelemetryCollector()