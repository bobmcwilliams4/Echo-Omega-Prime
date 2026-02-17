"""
R04 Violation Detector — Telemetry Module

Comprehensive query tracing, latency tracking, error domain monitoring,
and metrics collection for the violation detection engine.
"""

from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

from loguru import logger


class ErrorDomain(str, Enum):
    """Error classification domains."""
    INPUT_VALIDATION = "input_validation"
    DOCTRINE_CACHE_MISS = "doctrine_cache_miss"
    CLOUD_RETRIEVAL_TIMEOUT = "cloud_retrieval_timeout"
    PENALTY_CALCULATION_ERROR = "penalty_calculation_error"
    COMPLIANCE_ASSESSMENT_ERROR = "compliance_assessment_error"
    UNKNOWN = "unknown"


@dataclass
class QueryTrace:
    """Single query execution trace."""
    query_id: str
    query_text: str
    response_mode: str
    start_time: float
    end_time: Optional[float] = None
    latency_ms: Optional[float] = None
    doctrines_triggered: List[str] = field(default_factory=list)
    cloud_calls: int = 0
    cache_hits: int = 0
    errors: List[str] = field(default_factory=list)
    error_domain: Optional[ErrorDomain] = None
    confidence: Optional[float] = None
    violation_type: Optional[str] = None
    penalty_range: Optional[str] = None


@dataclass
class MetricsSnapshot:
    """Aggregated metrics snapshot."""
    timestamp: str
    total_queries: int
    avg_latency_ms: float
    p95_latency_ms: float
    p99_latency_ms: float
    error_rate: float
    cache_hit_rate: float
    cloud_call_rate: float
    queries_per_minute: float
    top_violations: List[tuple]  # (violation_type, count)
    top_authorities: List[tuple]  # (authority, count)


class TelemetryCollector:
    """Violation detection engine telemetry system."""

    def __init__(self, engine_id: str = "R04_violation_detector"):
        self.engine_id = engine_id
        self.active_traces: Dict[str, QueryTrace] = {}
        self.completed_traces: List[QueryTrace] = []
        self.start_time = time.time()

        # Metrics counters
        self.total_queries = 0
        self.total_errors = 0
        self.total_cache_hits = 0
        self.total_cloud_calls = 0
        self.violation_counts: Dict[str, int] = {}
        self.authority_counts: Dict[str, int] = {}
        self.latencies: List[float] = []

        # Audit trail
        self.audit_log_path = Path(f"./logs/audit_trail_{engine_id}.jsonl")
        self.audit_log_path.parent.mkdir(parents=True, exist_ok=True)

        logger.info(f"Telemetry collector initialized for {engine_id}")

    def start_trace(
        self,
        query_text: str,
        response_mode: str = "FAST"
    ) -> str:
        """
        Begin query trace.

        Returns:
            query_id for correlation
        """
        query_id = self._generate_query_id(query_text)

        trace = QueryTrace(
            query_id=query_id,
            query_text=query_text,
            response_mode=response_mode,
            start_time=time.time()
        )

        self.active_traces[query_id] = trace
        self.total_queries += 1

        logger.debug(f"Started trace {query_id[:8]}: {query_text[:50]}")

        return query_id

    def end_trace(
        self,
        query_id: str,
        doctrines_triggered: Optional[List[str]] = None,
        cloud_calls: int = 0,
        cache_hits: int = 0,
        confidence: Optional[float] = None,
        violation_type: Optional[str] = None,
        penalty_range: Optional[str] = None,
        error: Optional[str] = None,
        error_domain: Optional[ErrorDomain] = None
    ):
        """Complete query trace with results."""
        if query_id not in self.active_traces:
            logger.warning(f"Trace {query_id[:8]} not found in active traces")
            return

        trace = self.active_traces.pop(query_id)
        trace.end_time = time.time()
        trace.latency_ms = (trace.end_time - trace.start_time) * 1000

        if doctrines_triggered:
            trace.doctrines_triggered = doctrines_triggered

        trace.cloud_calls = cloud_calls
        trace.cache_hits = cache_hits
        trace.confidence = confidence
        trace.violation_type = violation_type
        trace.penalty_range = penalty_range

        if error:
            trace.errors.append(error)
            trace.error_domain = error_domain or ErrorDomain.UNKNOWN
            self.total_errors += 1

        # Update metrics
        self.latencies.append(trace.latency_ms)
        self.total_cache_hits += cache_hits
        self.total_cloud_calls += cloud_calls

        if violation_type:
            self.violation_counts[violation_type] = self.violation_counts.get(violation_type, 0) + 1

        self.completed_traces.append(trace)

        # Audit trail
        self._write_audit_log(trace)

        logger.debug(f"Completed trace {query_id[:8]}: {trace.latency_ms:.1f}ms")

    def record_error(
        self,
        query_id: str,
        error: str,
        error_domain: ErrorDomain = ErrorDomain.UNKNOWN
    ):
        """Record error during query execution."""
        if query_id in self.active_traces:
            self.active_traces[query_id].errors.append(error)
            self.active_traces[query_id].error_domain = error_domain

        self.total_errors += 1
        logger.error(f"Error in {query_id[:8]} ({error_domain}): {error}")

    def get_metrics_snapshot(self) -> MetricsSnapshot:
        """Generate current metrics snapshot."""
        if not self.latencies:
            return MetricsSnapshot(
                timestamp=datetime.utcnow().isoformat(),
                total_queries=0,
                avg_latency_ms=0.0,
                p95_latency_ms=0.0,
                p99_latency_ms=0.0,
                error_rate=0.0,
                cache_hit_rate=0.0,
                cloud_call_rate=0.0,
                queries_per_minute=0.0,
                top_violations=[],
                top_authorities=[]
            )

        sorted_latencies = sorted(self.latencies)
        p95_idx = int(len(sorted_latencies) * 0.95)
        p99_idx = int(len(sorted_latencies) * 0.99)

        elapsed_minutes = (time.time() - self.start_time) / 60.0
        queries_per_minute = self.total_queries / elapsed_minutes if elapsed_minutes > 0 else 0.0

        error_rate = self.total_errors / self.total_queries if self.total_queries > 0 else 0.0
        cache_hit_rate = self.total_cache_hits / self.total_queries if self.total_queries > 0 else 0.0
        cloud_call_rate = self.total_cloud_calls / self.total_queries if self.total_queries > 0 else 0.0

        top_violations = sorted(
            self.violation_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]

        top_authorities = sorted(
            self.authority_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]

        return MetricsSnapshot(
            timestamp=datetime.utcnow().isoformat(),
            total_queries=self.total_queries,
            avg_latency_ms=sum(self.latencies) / len(self.latencies),
            p95_latency_ms=sorted_latencies[p95_idx] if p95_idx < len(sorted_latencies) else 0.0,
            p99_latency_ms=sorted_latencies[p99_idx] if p99_idx < len(sorted_latencies) else 0.0,
            error_rate=error_rate,
            cache_hit_rate=cache_hit_rate,
            cloud_call_rate=cloud_call_rate,
            queries_per_minute=queries_per_minute,
            top_violations=top_violations,
            top_authorities=top_authorities
        )

    def _generate_query_id(self, query_text: str) -> str:
        """Generate deterministic query ID."""
        timestamp = str(time.time())
        content = f"{query_text}|{timestamp}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def _write_audit_log(self, trace: QueryTrace):
        """Append trace to audit log (JSONL format)."""
        try:
            import json

            log_entry = {
                "query_id": trace.query_id,
                "timestamp": datetime.utcnow().isoformat(),
                "query_text": trace.query_text,
                "response_mode": trace.response_mode,
                "latency_ms": trace.latency_ms,
                "doctrines_triggered": trace.doctrines_triggered,
                "cloud_calls": trace.cloud_calls,
                "cache_hits": trace.cache_hits,
                "confidence": trace.confidence,
                "violation_type": trace.violation_type,
                "penalty_range": trace.penalty_range,
                "errors": trace.errors,
                "error_domain": trace.error_domain.value if trace.error_domain else None
            }

            with open(self.audit_log_path, "a") as f:
                f.write(json.dumps(log_entry) + "\n")

        except Exception as e:
            logger.warning(f"Failed to write audit log: {e}")

    def get_recent_traces(self, limit: int = 10) -> List[QueryTrace]:
        """Return most recent completed traces."""
        return self.completed_traces[-limit:]

    def reset_metrics(self):
        """Reset all metrics counters (for testing or periodic reset)."""
        self.total_queries = 0
        self.total_errors = 0
        self.total_cache_hits = 0
        self.total_cloud_calls = 0
        self.violation_counts.clear()
        self.authority_counts.clear()
        self.latencies.clear()
        self.completed_traces.clear()
        self.start_time = time.time()
        logger.info("Telemetry metrics reset")
