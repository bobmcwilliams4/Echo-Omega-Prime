import time
import json
import hashlib
import statistics
import pathlib
import dataclasses
import typing
import collections
from loguru import logger

ENGINE_ID = "FRAC01"

@dataclasses.dataclass
class QueryMetrics:
    query_id: str
    engine_id: str
    timestamp: float
    latency_ms: float
    cache_hit: bool
    doctrine_matched: bool
    mode: str
    confidence: float
    error: typing.Optional[str] = None

class TelemetryCollector:
    def __init__(self):
        self._queries = collections.deque(maxlen=10000)
        self._errors = collections.deque(maxlen=10000)
        self._doctrine_hits = collections.deque(maxlen=10000)
        self._latencies = collections.deque(maxlen=10000)
        self._query_ids = set()
        self._audit_writer = AuditTrailWriter()
        logger.info(f"TelemetryCollector initialized for engine {ENGINE_ID}")

    def record_query(self, metrics: QueryMetrics):
        self._queries.append(metrics)
        self._query_ids.add(metrics.query_id)
        self._latencies.append(metrics.latency_ms)
        self._doctrine_hits.append(metrics.doctrine_matched)
        if metrics.error:
            self.record_error("query_error", metrics.error, metrics.query_id)
        self._audit_writer.write(metrics)
        logger.debug(f"Recorded query: {metrics.query_id}")

    def record_error(self, error_type: str, message: str, query_id: typing.Optional[str] = None):
        error_entry = {
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "timestamp": time.time()
        }
        self._errors.append(error_entry)
        logger.warning(f"Error recorded: {error_type} ({query_id}): {message}")

    def get_latency_stats(self) -> dict:
        latencies = list(self._latencies)
        if not latencies:
            return {
                "avg": None,
                "p50": None,
                "p95": None,
                "p99": None,
                "min": None,
                "max": None
            }
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)
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

    def _percentile(self, data, percentile):
        if not data:
            return None
        data_sorted = sorted(data)
        k = (len(data_sorted) - 1) * (percentile / 100)
        f = int(k)
        c = f + 1
        if c >= len(data_sorted):
            return data_sorted[f]
        d0 = data_sorted[f] * (c - k)
        d1 = data_sorted[c] * (k - f)
        return d0 + d1

    def get_doctrine_hit_rate(self) -> float:
        hits = list(self._doctrine_hits)
        if not hits:
            return 0.0
        return sum(hits) / len(hits)

    def get_error_rate(self, window_hours: float) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        relevant_queries = [q for q in self._queries if q.timestamp >= window_start]
        relevant_errors = [e for e in self._errors if e["timestamp"] >= window_start]
        num_queries = len(relevant_queries)
        num_errors = len(relevant_errors)
        if num_queries == 0:
            return 0.0
        return num_errors / num_queries

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        return sum(1 for q in self._queries if q.timestamp >= one_hour_ago)

    def get_coverage_report(self) -> dict:
        total = len(self._queries)
        doctrine_matched = sum(1 for q in self._queries if q.doctrine_matched)
        cache_hits = sum(1 for q in self._queries if q.cache_hit)
        modes = collections.Counter(q.mode for q in self._queries)
        confidences = [q.confidence for q in self._queries if q.confidence is not None]
        avg_confidence = statistics.mean(confidences) if confidences else None
        return {
            "total_queries": total,
            "doctrine_matched": doctrine_matched,
            "doctrine_match_rate": doctrine_matched / total if total else 0.0,
            "cache_hits": cache_hits,
            "cache_hit_rate": cache_hits / total if total else 0.0,
            "mode_distribution": dict(modes),
            "avg_confidence": avg_confidence
        }

    def export_jsonl(self, path: typing.Union[str, pathlib.Path]) -> int:
        path = pathlib.Path(path)
        count = 0
        with path.open("w", encoding="utf-8") as f:
            for q in self._queries:
                f.write(json.dumps(dataclasses.asdict(q)) + "\n")
                count += 1
        logger.info(f"Exported {count} queries to {path}")
        return count

class AuditTrailWriter:
    def __init__(self, audit_dir: typing.Optional[pathlib.Path] = None):
        if audit_dir is None:
            audit_dir = pathlib.Path("./audit_trail")
        self.audit_dir = audit_dir
        self.audit_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"AuditTrailWriter initialized at {self.audit_dir}")

    def write(self, metrics: QueryMetrics):
        audit_path = self._get_audit_path(metrics.query_id)
        audit_entry = dataclasses.asdict(metrics)
        audit_entry["audit_hash"] = self._hash_entry(audit_entry)
        with audit_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(audit_entry) + "\n")
        logger.debug(f"Audit written for query {metrics.query_id}")

    def _get_audit_path(self, query_id: str) -> pathlib.Path:
        date_str = time.strftime("%Y-%m-%d")
        subdir = self.audit_dir / date_str
        subdir.mkdir(parents=True, exist_ok=True)
        filename = f"{ENGINE_ID}_{query_id}.jsonl"
        return subdir / filename

    def _hash_entry(self, entry: dict) -> str:
        entry_json = json.dumps(entry, sort_keys=True)
        return hashlib.sha256(entry_json.encode("utf-8")).hexdigest()

COLLECTOR = TelemetryCollector()