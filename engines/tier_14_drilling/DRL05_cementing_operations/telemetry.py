import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Tuple
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "DRL05"

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
    def __init__(self, engine_id: str = ENGINE_ID, max_queries: int = 10000):
        self.engine_id = engine_id
        self._queries: deque = deque(maxlen=max_queries)
        self._errors: deque = deque(maxlen=max_queries)
        self._doctrine_hits: deque = deque(maxlen=max_queries)
        self._latencies: deque = deque(maxlen=max_queries)
        self._modes: Counter = Counter()
        self._confidence_scores: deque = deque(maxlen=max_queries)
        self._coverage: defaultdict = defaultdict(set)
        self._query_ids: set = set()
        self._audit_writer = AuditTrailWriter()
        logger.info(f"TelemetryCollector initialized for engine_id={self.engine_id}")

    def record_query(self, metrics: QueryMetrics):
        logger.debug(f"Recording query: {metrics}")
        self._queries.append(metrics)
        self._query_ids.add(metrics.query_id)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._modes[metrics.mode] += 1
        self._confidence_scores.append(metrics.confidence)
        self._coverage[metrics.mode].add(metrics.query_id)
        self._audit_writer.write(metrics)
        if metrics.error:
            self.record_error(error_type="query_error", message=metrics.error, query_id=metrics.query_id)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "timestamp": time.time(),
            "engine_id": self.engine_id,
            "error_type": error_type,
            "message": message,
            "query_id": query_id
        }
        logger.error(f"Recording error: {error_entry}")
        self._errors.append(error_entry)
        self._audit_writer.write(error_entry)

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = list(self._latencies)
        if not latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)
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

    def _percentile(self, data: List[float], percentile: float) -> float:
        if not data:
            return None
        data_sorted = sorted(data)
        k = (len(data_sorted) - 1) * (percentile / 100)
        f = int(k)
        c = f + 1
        if c >= len(data_sorted):
            return data_sorted[-1]
        d0 = data_sorted[f] * (c - k)
        d1 = data_sorted[c] * (k - f)
        return d0 + d1

    def get_doctrine_hit_rate(self) -> float:
        hits = sum(1 for hit in self._doctrine_hits if hit)
        total = len(self._doctrine_hits)
        rate = hits / total if total > 0 else 0.0
        logger.info(f"Doctrine hit rate: {rate} ({hits}/{total})")
        return rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        error_count = sum(1 for e in self._errors if e["timestamp"] >= window_start)
        query_count = sum(1 for q in self._queries if q.timestamp >= window_start)
        rate = error_count / query_count if query_count > 0 else 0.0
        logger.info(f"Error rate in last {window_hours} hours: {rate} ({error_count}/{query_count})")
        return rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= one_hour_ago)
        logger.info(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {}
        for mode, ids in self._coverage.items():
            report[mode] = {
                "unique_queries": len(ids),
                "coverage_percent": (len(ids) / len(self._query_ids) * 100) if self._query_ids else 0.0
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
            for e in self._errors:
                f.write(json.dumps(e) + "\n")
                count += 1
        logger.info(f"Exported {count} records to {path}")
        return count

class AuditTrailWriter:
    def __init__(self, audit_dir: str = "./audit_trail"):
        self.audit_dir = pathlib.Path(audit_dir)
        self.audit_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"AuditTrailWriter initialized at {self.audit_dir}")

    def write(self, entry: Any):
        if isinstance(entry, QueryMetrics):
            record = dataclasses.asdict(entry)
            filename = self._get_filename(entry.query_id)
        elif isinstance(entry, dict) and "error_type" in entry:
            record = entry
            filename = self._get_filename(entry.get("query_id", "error"))
        else:
            logger.warning(f"Unknown entry type for audit: {entry}")
            return
        with open(filename, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
        logger.debug(f"Wrote audit entry to {filename}")

    def _get_filename(self, query_id: str) -> str:
        if not query_id:
            query_id = "unknown"
        hash_id = hashlib.md5(query_id.encode()).hexdigest()
        filename = self.audit_dir / f"{hash_id}.jsonl"
        return str(filename)

COLLECTOR = TelemetryCollector(engine_id=ENGINE_ID)