import time
import json
import hashlib
import statistics
import pathlib
import dataclasses
import typing
import collections
from loguru import logger


ENGINE_ID = "DRL04"


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
        self._queries: typing.List[QueryMetrics] = []
        self._errors: typing.List[dict] = []
        self._lock = collections.deque()  # placeholder for thread safety if needed
        self._audit_writer = AuditTrailWriter()
        self._coverage_modes: typing.Counter[str] = collections.Counter()
        self._coverage_confidences: typing.List[float] = []

    def record_query(self, metrics: QueryMetrics):
        logger.debug(f"Recording query metrics: {metrics}")
        self._queries.append(metrics)
        self._coverage_modes[metrics.mode] += 1
        self._coverage_confidences.append(metrics.confidence)
        if metrics.error:
            self.record_error("QueryError", metrics.error, metrics.query_id)
        self._audit_writer.write(metrics)

    def record_error(self, error_type: str, message: str, query_id: str):
        error_entry = {
            "timestamp": time.time(),
            "error_type": error_type,
            "message": message,
            "query_id": query_id,
            "engine_id": ENGINE_ID,
        }
        logger.warning(f"Recording error: {error_entry}")
        self._errors.append(error_entry)

    def get_latency_stats(self) -> dict:
        latencies = [q.latency_ms for q in self._queries if q.latency_ms is not None]
        if not latencies:
            return {"avg": 0, "p50": 0, "p95": 0, "p99": 0, "min": 0, "max": 0}
        latencies.sort()
        avg = statistics.mean(latencies)
        p50 = statistics.median(latencies)
        p95 = latencies[int(len(latencies) * 0.95) - 1]
        p99 = latencies[int(len(latencies) * 0.99) - 1]
        min_latency = latencies[0]
        max_latency = latencies[-1]
        stats = {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_latency,
            "max": max_latency,
        }
        logger.debug(f"Latency stats computed: {stats}")
        return stats

    def get_doctrine_hit_rate(self) -> float:
        if not self._queries:
            return 0.0
        hits = sum(1 for q in self._queries if q.doctrine_matched)
        rate = hits / len(self._queries)
        logger.debug(f"Doctrine hit rate: {rate} ({hits}/{len(self._queries)})")
        return rate

    def get_error_rate(self, window_hours: float) -> float:
        now = time.time()
        window_seconds = window_hours * 3600
        recent_queries = [q for q in self._queries if now - q.timestamp <= window_seconds]
        if not recent_queries:
            return 0.0
        recent_errors = [e for e in self._errors if now - e["timestamp"] <= window_seconds]
        rate = len(recent_errors) / len(recent_queries)
        logger.debug(f"Error rate over last {window_hours} hours: {rate} ({len(recent_errors)}/{len(recent_queries)})")
        return rate

    def queries_last_hour(self) -> int:
        now = time.time()
        one_hour_ago = now - 3600
        count = sum(1 for q in self._queries if q.timestamp >= one_hour_ago)
        logger.debug(f"Queries in the last hour: {count}")
        return count

    def get_coverage_report(self) -> dict:
        total = sum(self._coverage_modes.values())
        if total == 0:
            coverage = {}
        else:
            coverage = {mode: count / total for mode, count in self._coverage_modes.items()}
        avg_confidence = statistics.mean(self._coverage_confidences) if self._coverage_confidences else 0.0
        report = {
            "mode_coverage": coverage,
            "average_confidence": avg_confidence,
            "total_queries": total,
        }
        logger.debug(f"Coverage report generated: {report}")
        return report

    def export_jsonl(self, path: typing.Union[str, pathlib.Path]) -> int:
        path = pathlib.Path(path)
        count = 0
        try:
            with path.open("w", encoding="utf-8") as f:
                for q in self._queries:
                    record = dataclasses.asdict(q)
                    f.write(json.dumps(record) + "\n")
                    count += 1
            logger.info(f"Exported {count} query records to {path}")
        except Exception as e:
            logger.error(f"Failed to export telemetry data to {path}: {e}")
            raise
        return count


class AuditTrailWriter:
    def __init__(self, directory: typing.Union[str, pathlib.Path] = "audit_trail"):
        self.directory = pathlib.Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        self._file_handles: typing.Dict[str, typing.IO] = {}
        self._lock = collections.deque()  # placeholder for thread safety if needed

    def _get_file_handle(self, query_id: str) -> typing.IO:
        # Use hash of query_id to shard files to avoid too many open files
        shard = hashlib.sha256(query_id.encode("utf-8")).hexdigest()[:2]
        filename = self.directory / f"audit_{shard}.jsonl"
        if filename not in self._file_handles:
            self._file_handles[filename] = open(filename, "a", encoding="utf-8")
        return self._file_handles[filename]

    def write(self, metrics: QueryMetrics):
        try:
            fh = self._get_file_handle(metrics.query_id)
            record = dataclasses.asdict(metrics)
            fh.write(json.dumps(record) + "\n")
            fh.flush()
            logger.debug(f"Audit trail written for query_id={metrics.query_id}")
        except Exception as e:
            logger.error(f"Failed to write audit trail for query_id={metrics.query_id}: {e}")

    def close(self):
        for fh in self._file_handles.values():
            try:
                fh.close()
            except Exception as e:
                logger.warning(f"Failed to close audit trail file handle: {e}")
        self._file_handles.clear()


COLLECTOR = TelemetryCollector()