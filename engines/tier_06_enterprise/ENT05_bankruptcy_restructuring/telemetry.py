import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional, Any
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "ENT05"

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
    def __init__(self):
        self._queries: deque = deque(maxlen=10000)
        self._errors: deque = deque(maxlen=10000)
        self._doctrine_hits: deque = deque(maxlen=10000)
        self._cache_hits: deque = deque(maxlen=10000)
        self._latencies: deque = deque(maxlen=10000)
        self._modes: deque = deque(maxlen=10000)
        self._confidences: deque = deque(maxlen=10000)
        self._query_map: Dict[str, QueryMetrics] = {}
        self._audit_writer = AuditTrailWriter()
        logger.info("TelemetryCollector initialized.")

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._query_map[metrics.query_id] = metrics
        self._latencies.append(metrics.latency_ms)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._cache_hits.append(metrics.cache_hit)
        self._modes.append(metrics.mode)
        self._confidences.append(metrics.confidence)
        if metrics.error:
            self._errors.append((metrics.timestamp, metrics.error, metrics.query_id))
        self._audit_writer.write(metrics)
        logger.debug(f"Recorded query: {metrics.query_id}")

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        ts = time.time()
        self._errors.append((ts, error_type, query_id))
        logger.error(f"Error recorded: {error_type} - {message} (query_id={query_id})")

    def get_latency_stats(self) -> dict:
        if not self._latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        lat = list(self._latencies)
        avg = statistics.mean(lat)
        p50 = statistics.median(lat)
        p95 = self._percentile(lat, 95)
        p99 = self._percentile(lat, 99)
        min_v = min(lat)
        max_v = max(lat)
        logger.debug(f"Latency stats: avg={avg}, p50={p50}, p95={p95}, p99={p99}, min={min_v}, max={max_v}")
        return {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_v,
            "max": max_v
        }

    def _percentile(self, data: List[float], percentile: float) -> float:
        if not data:
            return None
        size = len(data)
        return sorted(data)[int(size * percentile / 100)]

    def get_doctrine_hit_rate(self) -> float:
        if not self._doctrine_hits:
            return 0.0
        hit_count = sum(1 for hit in self._doctrine_hits if hit)
        rate = hit_count / len(self._doctrine_hits)
        logger.debug(f"Doctrine hit rate: {rate}")
        return rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        total = 0
        errors = 0
        for q in self._queries:
            if q.timestamp >= window_start:
                total += 1
                if q.error:
                    errors += 1
        if total == 0:
            return 0.0
        rate = errors / total
        logger.debug(f"Error rate in last {window_hours}h: {rate}")
        return rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= one_hour_ago)
        logger.debug(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> dict:
        total = len(self._queries)
        if total == 0:
            return {
                "total": 0,
                "cache_hit": 0,
                "cache_hit_rate": 0.0,
                "doctrine_matched": 0,
                "doctrine_hit_rate": 0.0,
                "modes": {},
                "confidence_avg": None
            }
        cache_hit_count = sum(1 for q in self._queries if q.cache_hit)
        doctrine_count = sum(1 for q in self._queries if q.doctrine_matched)
        mode_counter = Counter(q.mode for q in self._queries)
        confidence_avg = statistics.mean(q.confidence for q in self._queries)
        report = {
            "total": total,
            "cache_hit": cache_hit_count,
            "cache_hit_rate": cache_hit_count / total,
            "doctrine_matched": doctrine_count,
            "doctrine_hit_rate": doctrine_count / total,
            "modes": dict(mode_counter),
            "confidence_avg": confidence_avg
        }
        logger.debug(f"Coverage report: {report}")
        return report

    def export_jsonl(self, path: str) -> int:
        p = pathlib.Path(path)
        count = 0
        with p.open("w", encoding="utf-8") as f:
            for q in self._queries:
                f.write(json.dumps(asdict(q)) + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {path}")
        return count

class AuditTrailWriter:
    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = pathlib.Path(base_dir) if base_dir else pathlib.Path("./audit_trail")
        self.base_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"AuditTrailWriter initialized at {self.base_dir}")

    def write(self, metrics: QueryMetrics):
        filename = self._get_audit_filename(metrics.query_id)
        record = asdict(metrics)
        with open(filename, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
        logger.debug(f"Wrote audit trail for query {metrics.query_id}")

    def _get_audit_filename(self, query_id: str) -> str:
        # Hash query_id to avoid filesystem issues and sharding
        h = hashlib.sha1(query_id.encode("utf-8")).hexdigest()
        shard = h[:2]
        dir_path = self.base_dir / shard
        dir_path.mkdir(parents=True, exist_ok=True)
        filename = dir_path / f"{h}.jsonl"
        return str(filename)

COLLECTOR = TelemetryCollector()