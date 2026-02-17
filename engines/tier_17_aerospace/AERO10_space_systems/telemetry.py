import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "AERO10"

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
        self._queries = deque(maxlen=maxlen)
        self._errors = deque(maxlen=maxlen)
        self._doctrine_hits = deque(maxlen=maxlen)
        self._latencies = deque(maxlen=maxlen)
        self._query_times = deque(maxlen=maxlen)
        self._query_ids = set()
        self._mode_counter = Counter()
        self._confidence_scores = []
        self._coverage_data = defaultdict(list)
        self._audit_writer = AuditTrailWriter()
        logger.info("TelemetryCollector initialized with maxlen={}", maxlen)

    def record_query(self, metrics: QueryMetrics):
        if metrics.query_id in self._query_ids:
            logger.warning("Duplicate query_id detected: {}", metrics.query_id)
            return
        self._queries.append(metrics)
        self._query_ids.add(metrics.query_id)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_hits.append(metrics.doctrine_matched)
        self._query_times.append(metrics.timestamp)
        self._mode_counter[metrics.mode] += 1
        self._confidence_scores.append(metrics.confidence)
        self._coverage_data[metrics.mode].append(metrics.doctrine_matched)
        if metrics.error:
            self.record_error(metrics.error, "Query error", metrics.query_id)
        self._audit_writer.write(metrics)
        logger.debug("Recorded query: {}", metrics)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        error_entry = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "timestamp": time.time(),
        }
        self._errors.append(error_entry)
        logger.error("Error recorded: {}", error_entry)

    def get_latency_stats(self) -> Dict[str, Any]:
        if not self._latencies:
            return {
                "avg": None,
                "p50": None,
                "p95": None,
                "p99": None,
                "min": None,
                "max": None,
            }
        lats = list(self._latencies)
        lats.sort()
        avg = statistics.mean(lats)
        p50 = statistics.median(lats)
        p95 = lats[int(0.95 * len(lats)) - 1] if len(lats) >= 20 else lats[-1]
        p99 = lats[int(0.99 * len(lats)) - 1] if len(lats) >= 100 else lats[-1]
        min_lat = lats[0]
        max_lat = lats[-1]
        stats_dict = {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_lat,
            "max": max_lat,
        }
        logger.debug("Latency stats: {}", stats_dict)
        return stats_dict

    def get_doctrine_hit_rate(self) -> float:
        if not self._doctrine_hits:
            return 0.0
        rate = sum(self._doctrine_hits) / len(self._doctrine_hits)
        logger.debug("Doctrine hit rate: {:.2%}", rate)
        return rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        queries_in_window = [t for t in self._query_times if t >= window_start]
        errors_in_window = [e for e in self._errors if e["timestamp"] >= window_start]
        total = len(queries_in_window)
        error_count = len(errors_in_window)
        error_rate = (error_count / total) if total > 0 else 0.0
        logger.debug("Error rate in last {:.2f} hours: {:.2%}", window_hours, error_rate)
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = len([t for t in self._query_times if t >= one_hour_ago])
        logger.debug("Queries in last hour: {}", count)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {}
        for mode, matches in self._coverage_data.items():
            total = len(matches)
            doctrine_hits = sum(matches)
            hit_rate = doctrine_hits / total if total > 0 else 0.0
            report[mode] = {
                "total": total,
                "doctrine_hits": doctrine_hits,
                "hit_rate": hit_rate,
            }
        logger.debug("Coverage report: {}", report)
        return report

    def export_jsonl(self, path: str) -> int:
        path_obj = pathlib.Path(path)
        count = 0
        try:
            with path_obj.open("w", encoding="utf-8") as f:
                for q in self._queries:
                    f.write(json.dumps(asdict(q)) + "\n")
                    count += 1
            logger.info("Exported {} queries to {}", count, path)
        except Exception as e:
            logger.error("Failed to export JSONL: {}", e)
        return count

class AuditTrailWriter:
    def __init__(self, base_path: Optional[str] = None):
        if base_path is None:
            base_path = "./audit_trail"
        self.base_path = pathlib.Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        logger.info("AuditTrailWriter initialized at {}", self.base_path)

    def write(self, metrics: QueryMetrics):
        try:
            ts = time.strftime("%Y%m%d")
            file_path = self.base_path / f"audit_{ts}.jsonl"
            entry = asdict(metrics)
            entry["audit_hash"] = self._hash_entry(entry)
            with file_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
            logger.debug("Audit entry written for query_id={}", metrics.query_id)
        except Exception as e:
            logger.error("Failed to write audit entry: {}", e)

    def _hash_entry(self, entry: Dict[str, Any]) -> str:
        # Deterministic hash for audit trail integrity
        entry_bytes = json.dumps(entry, sort_keys=True).encode("utf-8")
        return hashlib.sha256(entry_bytes).hexdigest()

COLLECTOR = TelemetryCollector()