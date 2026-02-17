import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "RAIL05"

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
    def __init__(self, maxlen:int=10000):
        self._queries = deque(maxlen=maxlen)
        self._errors = deque(maxlen=maxlen)
        self._doctrine_matches = deque(maxlen=maxlen)
        self._cache_hits = deque(maxlen=maxlen)
        self._latencies = deque(maxlen=maxlen)
        self._modes = deque(maxlen=maxlen)
        self._confidences = deque(maxlen=maxlen)
        self._query_ids = set()
        self._coverage = defaultdict(lambda: {"count":0, "doctrine_matched":0, "cache_hit":0, "errors":0})
        self._audit_writer = AuditTrailWriter()
        logger.info("TelemetryCollector initialized.")

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._query_ids.add(metrics.query_id)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_matches.append(metrics.doctrine_matched)
        self._cache_hits.append(metrics.cache_hit)
        self._modes.append(metrics.mode)
        self._confidences.append(metrics.confidence)
        self._coverage[metrics.mode]["count"] += 1
        if metrics.doctrine_matched:
            self._coverage[metrics.mode]["doctrine_matched"] += 1
        if metrics.cache_hit:
            self._coverage[metrics.mode]["cache_hit"] += 1
        if metrics.error:
            self._coverage[metrics.mode]["errors"] += 1
        self._audit_writer.write(metrics)
        logger.debug(f"Recorded query: {metrics.query_id}")

    def record_error(self, error_type: str, message: str, query_id: Optional[str]=None):
        timestamp = time.time()
        error_entry = {
            "error_type": error_type,
            "message": message,
            "timestamp": timestamp,
            "query_id": query_id,
            "engine_id": ENGINE_ID
        }
        self._errors.append(error_entry)
        logger.error(f"Error recorded: {error_type} for query {query_id}: {message}")
        if query_id:
            for q in self._queries:
                if q.query_id == query_id:
                    q.error = error_type
                    self._coverage[q.mode]["errors"] += 1
                    break

    def get_latency_stats(self) -> Dict[str, Any]:
        latencies = list(self._latencies)
        if not latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        avg = statistics.mean(latencies)
        min_latency = min(latencies)
        max_latency = max(latencies)
        p50 = statistics.median(latencies)
        p95 = statistics.quantiles(latencies, n=100)[94]
        p99 = statistics.quantiles(latencies, n=100)[98]
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

    def get_doctrine_hit_rate(self) -> float:
        matches = list(self._doctrine_matches)
        if not matches:
            return 0.0
        hit_rate = sum(matches) / len(matches)
        logger.info(f"Doctrine hit rate: {hit_rate}")
        return hit_rate

    def get_error_rate(self, window_hours: float=1.0) -> float:
        now = time.time()
        window_start = now - window_hours*3600
        relevant_queries = [q for q in self._queries if q.timestamp >= window_start]
        relevant_errors = [q for q in relevant_queries if q.error]
        if not relevant_queries:
            return 0.0
        error_rate = len(relevant_errors) / len(relevant_queries)
        logger.info(f"Error rate in last {window_hours} hours: {error_rate}")
        return error_rate

    def queries_last_hour(self) -> int:
        now = time.time()
        cutoff = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= cutoff)
        logger.info(f"Queries in last hour: {count}")
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        report = {}
        for mode, stats in self._coverage.items():
            total = stats["count"]
            doctrine_hits = stats["doctrine_matched"]
            cache_hits = stats["cache_hit"]
            errors = stats["errors"]
            report[mode] = {
                "total": total,
                "doctrine_hit_rate": doctrine_hits/total if total else 0.0,
                "cache_hit_rate": cache_hits/total if total else 0.0,
                "error_rate": errors/total if total else 0.0
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
        logger.info(f"Exported {count} queries to {path}")
        return count

class AuditTrailWriter:
    def __init__(self, base_dir:str="audit_trail"):
        self.base_dir = pathlib.Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
        logger.info(f"AuditTrailWriter initialized at {self.base_dir}")

    def write(self, metrics: QueryMetrics):
        filename = self._filename_for_query(metrics.query_id)
        record = dataclasses.asdict(metrics)
        record["audit_hash"] = self._hash_record(record)
        record["audit_timestamp"] = time.time()
        with open(filename, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
        logger.debug(f"Audit trail written for query {metrics.query_id}")

    def _filename_for_query(self, query_id: str) -> str:
        h = hashlib.sha256(query_id.encode()).hexdigest()
        subdir = self.base_dir / h[:2]
        subdir.mkdir(exist_ok=True)
        return str(subdir / f"{h}.jsonl")

    def _hash_record(self, record: Dict[str, Any]) -> str:
        record_str = json.dumps(record, sort_keys=True)
        return hashlib.sha256(record_str.encode()).hexdigest()

COLLECTOR = TelemetryCollector()