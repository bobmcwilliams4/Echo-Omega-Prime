import time
import json
import hashlib
import statistics
import pathlib
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any
from collections import deque, Counter, defaultdict
from loguru import logger

ENGINE_ID = "ENT09"

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
        self.queries = deque(maxlen=maxlen)
        self.errors = deque(maxlen=maxlen)
        self.doctrine_hits = deque(maxlen=maxlen)
        self.latencies = deque(maxlen=maxlen)
        self.modes = deque(maxlen=maxlen)
        self.confidences = deque(maxlen=maxlen)
        self.timestamps = deque(maxlen=maxlen)
        self.cache_hits = deque(maxlen=maxlen)
        self.query_map = dict()
        self.error_counter = Counter()
        self.audit_writer = AuditTrailWriter()
        logger.info("TelemetryCollector initialized with maxlen={}", maxlen)

    def record_query(self, metrics: QueryMetrics):
        self.queries.append(metrics)
        self.latencies.append(metrics.latency_ms)
        self.doctrine_hits.append(metrics.doctrine_matched)
        self.modes.append(metrics.mode)
        self.confidences.append(metrics.confidence)
        self.timestamps.append(metrics.timestamp)
        self.cache_hits.append(metrics.cache_hit)
        self.query_map[metrics.query_id] = metrics
        if metrics.error:
            self.errors.append((metrics.timestamp, metrics.error, metrics.query_id))
            self.error_counter[metrics.error] += 1
        self.audit_writer.write(metrics)
        logger.debug("Recorded query: {}", metrics)

    def record_error(self, error_type: str, message: str, query_id: Optional[str] = None):
        ts = time.time()
        self.errors.append((ts, error_type, query_id))
        self.error_counter[error_type] += 1
        logger.error("Error recorded: [{}] {} (query_id={})", error_type, message, query_id)
        error_metrics = QueryMetrics(
            query_id=query_id or self._make_error_query_id(error_type, ts),
            engine_id=ENGINE_ID,
            timestamp=ts,
            latency_ms=0.0,
            cache_hit=False,
            doctrine_matched=False,
            mode="error",
            confidence=0.0,
            error=error_type
        )
        self.queries.append(error_metrics)
        self.audit_writer.write(error_metrics)

    def get_latency_stats(self) -> Dict[str, Any]:
        if not self.latencies:
            return {"avg": None, "p50": None, "p95": None, "p99": None, "min": None, "max": None}
        lat = list(self.latencies)
        avg = statistics.mean(lat)
        p50 = statistics.median(lat)
        p95 = self._percentile(lat, 95)
        p99 = self._percentile(lat, 99)
        min_ = min(lat)
        max_ = max(lat)
        logger.debug("Latency stats calculated: avg={}, p50={}, p95={}, p99={}, min={}, max={}", avg, p50, p95, p99, min_, max_)
        return {
            "avg": avg,
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "min": min_,
            "max": max_
        }

    def get_doctrine_hit_rate(self) -> float:
        if not self.doctrine_hits:
            return 0.0
        hits = sum(1 for h in self.doctrine_hits if h)
        rate = hits / len(self.doctrine_hits)
        logger.debug("Doctrine hit rate: {} ({} hits out of {})", rate, hits, len(self.doctrine_hits))
        return rate

    def get_error_rate(self, window_hours: float = 1.0) -> float:
        now = time.time()
        window_start = now - window_hours * 3600
        total = 0
        errors = 0
        for m in self.queries:
            if m.timestamp >= window_start:
                total += 1
                if m.error:
                    errors += 1
        rate = errors / total if total > 0 else 0.0
        logger.debug("Error rate in last {} hours: {} ({} errors out of {})", window_hours, rate, errors, total)
        return rate

    def queries_last_hour(self) -> int:
        now = time.time()
        window_start = now - 3600
        count = sum(1 for m in self.queries if m.timestamp >= window_start)
        logger.debug("Queries in last hour: {}", count)
        return count

    def get_coverage_report(self) -> Dict[str, Any]:
        mode_counter = Counter()
        cache_counter = Counter()
        doctrine_counter = Counter()
        for m in self.queries:
            mode_counter[m.mode] += 1
            cache_counter[m.cache_hit] += 1
            doctrine_counter[m.doctrine_matched] += 1
        report = {
            "total_queries": len(self.queries),
            "modes": dict(mode_counter),
            "cache_hits": dict(cache_counter),
            "doctrine_matched": dict(doctrine_counter),
            "confidence": {
                "avg": statistics.mean(self.confidences) if self.confidences else None,
                "min": min(self.confidences) if self.confidences else None,
                "max": max(self.confidences) if self.confidences else None,
            }
        }
        logger.debug("Coverage report: {}", report)
        return report

    def export_jsonl(self, path) -> int:
        path = pathlib.Path(path)
        count = 0
        with path.open("w", encoding="utf-8") as f:
            for m in self.queries:
                f.write(json.dumps(asdict(m)) + "\n")
                count += 1
        logger.info("Exported {} queries to {}", count, path)
        return count

    def _percentile(self, data: List[float], percentile: float) -> float:
        if not data:
            return None
        data = sorted(data)
        k = (len(data) - 1) * (percentile / 100.0)
        f = int(k)
        c = min(f + 1, len(data) - 1)
        if f == c:
            return data[int(k)]
        d0 = data[f] * (c - k)
        d1 = data[c] * (k - f)
        return d0 + d1

    def _make_error_query_id(self, error_type: str, ts: float) -> str:
        base = f"{error_type}:{ts}"
        return hashlib.sha256(base.encode()).hexdigest()[:16]

class AuditTrailWriter:
    def __init__(self, base_dir: str = "./audit_trail"):
        self.base_dir = pathlib.Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        logger.info("AuditTrailWriter initialized at {}", self.base_dir)

    def write(self, metrics: QueryMetrics):
        date_str = time.strftime("%Y-%m-%d")
        file_path = self.base_dir / f"queries_{date_str}.jsonl"
        entry = asdict(metrics)
        try:
            with file_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
            logger.debug("Wrote audit trail for query_id={}", metrics.query_id)
        except Exception as e:
            logger.exception("Failed to write audit trail: {}", e)

COLLECTOR = TelemetryCollector()