"""
LM11 Lease Negotiation Engine — Telemetry Module
Full query tracing, latency tracking, error domain classification, and operational metrics.

Author: ECHO OMEGA PRIME
Engine: LM11 Lease Negotiation
Version: 1.0.0
"""

from __future__ import annotations

import hashlib
import json
import time
import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

from loguru import logger

# ==============================================================================
# CONSTANTS
# ==============================================================================

ENGINE_ID = "LM11"
ENGINE_NAME = "Lease Negotiation Engine"
TELEMETRY_VERSION = "1.0.0"
MAX_TRACE_HISTORY = 500
MAX_ERROR_HISTORY = 200
MAX_LATENCY_SAMPLES = 1000
AUDIT_FLUSH_THRESHOLD = 50

LOG_DIR = Path("O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/LM11_lease_negotiation/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

AUDIT_LOG_PATH = LOG_DIR / "audit_trail.jsonl"
TELEMETRY_LOG_PATH = LOG_DIR / "telemetry.jsonl"
ERROR_LOG_PATH = LOG_DIR / "errors.jsonl"


# ==============================================================================
# ERROR DOMAIN CLASSIFICATION
# ==============================================================================

class ErrorDomain(str, Enum):
    """Classifies errors by operational domain for routing and analysis."""
    DOCTRINE_LOOKUP = "doctrine_lookup"
    SEMANTIC_NORMALIZATION = "semantic_normalization"
    VECTOR_SEARCH = "vector_search"
    DEEP_ANALYSIS = "deep_analysis"
    INPUT_VALIDATION = "input_validation"
    SERIALIZATION = "serialization"
    AUTHORITY_RESOLUTION = "authority_resolution"
    CONFIDENCE_SCORING = "confidence_scoring"
    FRAGILITY_ASSESSMENT = "fragility_assessment"
    COVERAGE_GAP = "coverage_gap"
    DRIFT_DETECTION = "drift_detection"
    AUDIT_TRAIL = "audit_trail"
    HEALTH_CHECK = "health_check"
    NETWORK_IO = "network_io"
    LEASE_CLAUSE_PARSE = "lease_clause_parse"
    ROYALTY_CALCULATION = "royalty_calculation"
    NEGOTIATION_STRATEGY = "negotiation_strategy"
    TERM_ANALYSIS = "term_analysis"
    UNKNOWN = "unknown"


class ResponseLayer(str, Enum):
    """Which response layer produced the result."""
    DOCTRINE_CACHE = "doctrine_cache"
    SEMANTIC_RETRIEVAL = "semantic_retrieval"
    DEEP_ANALYSIS = "deep_analysis"
    FALLBACK = "fallback"


class MutationType(str, Enum):
    """Type of doctrine mutation detected."""
    CONTENT_UPDATE = "content_update"
    AUTHORITY_SHIFT = "authority_shift"
    CONFIDENCE_CHANGE = "confidence_change"
    NEW_PRECEDENT = "new_precedent"
    DEPRECATION = "deprecation"
    SCOPE_EXPANSION = "scope_expansion"
    SCOPE_CONTRACTION = "scope_contraction"


class MutationOrigin(str, Enum):
    """Where the mutation was triggered from."""
    DRIFT_WATCHER = "drift_watcher"
    MANUAL_UPDATE = "manual_update"
    PRECEDENT_IMPORT = "precedent_import"
    AUTO_CORRECTION = "auto_correction"
    LEGISLATIVE_UPDATE = "legislative_update"


# ==============================================================================
# TRACE DATA STRUCTURES
# ==============================================================================

@dataclass
class TraceSpan:
    """A single span within a query trace."""
    span_id: str
    operation: str
    start_time: float
    end_time: Optional[float] = None
    duration_ms: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    layer: Optional[ResponseLayer] = None

    def complete(self, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Mark span as complete and calculate duration."""
        self.end_time = time.time()
        self.duration_ms = (self.end_time - self.start_time) * 1000
        if metadata:
            self.metadata.update(metadata)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize span to dictionary."""
        return {
            "span_id": self.span_id,
            "operation": self.operation,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration_ms": self.duration_ms,
            "metadata": self.metadata,
            "error": self.error,
            "layer": self.layer.value if self.layer else None,
        }


@dataclass
class QueryTrace:
    """Complete trace of a single query through the engine."""
    trace_id: str
    query_text: str
    start_time: float
    engine_id: str = ENGINE_ID
    session_id: Optional[str] = None
    response_mode: Optional[str] = None
    analysis_zone: Optional[str] = None
    spans: List[TraceSpan] = field(default_factory=list)
    end_time: Optional[float] = None
    total_duration_ms: Optional[float] = None
    final_layer: Optional[ResponseLayer] = None
    doctrine_hit: bool = False
    doctrine_topic: Optional[str] = None
    confidence_level: Optional[str] = None
    error: Optional[str] = None
    determinism_hash: Optional[str] = None

    def add_span(self, operation: str, layer: Optional[ResponseLayer] = None) -> TraceSpan:
        """Create and add a new span to this trace."""
        span = TraceSpan(
            span_id=str(uuid.uuid4())[:8],
            operation=operation,
            start_time=time.time(),
            layer=layer,
        )
        self.spans.append(span)
        return span

    def complete(
        self,
        final_layer: ResponseLayer,
        doctrine_hit: bool = False,
        doctrine_topic: Optional[str] = None,
        confidence_level: Optional[str] = None,
        determinism_hash: Optional[str] = None,
    ) -> None:
        """Mark trace as complete."""
        self.end_time = time.time()
        self.total_duration_ms = (self.end_time - self.start_time) * 1000
        self.final_layer = final_layer
        self.doctrine_hit = doctrine_hit
        self.doctrine_topic = doctrine_topic
        self.confidence_level = confidence_level
        self.determinism_hash = determinism_hash

    def to_dict(self) -> Dict[str, Any]:
        """Serialize trace to dictionary."""
        return {
            "trace_id": self.trace_id,
            "engine_id": self.engine_id,
            "query_text": self.query_text[:200],
            "session_id": self.session_id,
            "response_mode": self.response_mode,
            "analysis_zone": self.analysis_zone,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "total_duration_ms": self.total_duration_ms,
            "final_layer": self.final_layer.value if self.final_layer else None,
            "doctrine_hit": self.doctrine_hit,
            "doctrine_topic": self.doctrine_topic,
            "confidence_level": self.confidence_level,
            "determinism_hash": self.determinism_hash,
            "span_count": len(self.spans),
            "spans": [s.to_dict() for s in self.spans],
            "error": self.error,
        }


@dataclass
class ErrorRecord:
    """Structured error record for analysis."""
    error_id: str
    timestamp: float
    domain: ErrorDomain
    message: str
    trace_id: Optional[str] = None
    stack_trace: Optional[str] = None
    query_context: Optional[str] = None
    resolution: Optional[str] = None
    severity: str = "ERROR"

    def to_dict(self) -> Dict[str, Any]:
        """Serialize error record."""
        return {
            "error_id": self.error_id,
            "timestamp": self.timestamp,
            "domain": self.domain.value,
            "message": self.message,
            "trace_id": self.trace_id,
            "stack_trace": self.stack_trace,
            "query_context": self.query_context[:200] if self.query_context else None,
            "resolution": self.resolution,
            "severity": self.severity,
        }


@dataclass
class DoctrineMutationRecord:
    """Record of a doctrine content mutation."""
    mutation_id: str
    timestamp: float
    topic: str
    mutation_type: MutationType
    origin: MutationOrigin
    before_hash: Optional[str] = None
    after_hash: Optional[str] = None
    description: str = ""
    approved_by: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Serialize mutation record."""
        return {
            "mutation_id": self.mutation_id,
            "timestamp": self.timestamp,
            "topic": self.topic,
            "mutation_type": self.mutation_type.value,
            "origin": self.origin.value,
            "before_hash": self.before_hash,
            "after_hash": self.after_hash,
            "description": self.description,
            "approved_by": self.approved_by,
        }


# ==============================================================================
# TELEMETRY COLLECTOR
# ==============================================================================

class TelemetryCollector:
    """
    Central telemetry collector for the LM11 Lease Negotiation Engine.

    Responsibilities:
    - Trace every query from ingestion through response
    - Track latency distributions per response layer
    - Classify and record errors by domain
    - Monitor doctrine cache hit/miss rates
    - Record doctrine mutations for drift analysis
    - Persist audit trail to JSONL
    - Expose operational metrics for health endpoint
    """

    def __init__(self) -> None:
        self._traces: List[QueryTrace] = []
        self._errors: List[ErrorRecord] = []
        self._mutations: List[DoctrineMutationRecord] = []
        self._latencies: Dict[str, List[float]] = defaultdict(list)
        self._error_counts: Dict[str, int] = defaultdict(int)
        self._query_count: int = 0
        self._doctrine_hits: int = 0
        self._doctrine_misses: int = 0
        self._layer_counts: Dict[str, int] = defaultdict(int)
        self._pending_audit: List[Dict[str, Any]] = []
        self._start_time: float = time.time()
        self._last_flush: float = time.time()
        logger.info(f"TelemetryCollector initialized for {ENGINE_ID}")

    # --------------------------------------------------------------------------
    # TRACE MANAGEMENT
    # --------------------------------------------------------------------------

    def start_trace(
        self,
        query_text: str,
        session_id: Optional[str] = None,
        response_mode: Optional[str] = None,
        analysis_zone: Optional[str] = None,
    ) -> QueryTrace:
        """Begin tracing a new query."""
        trace = QueryTrace(
            trace_id=str(uuid.uuid4()),
            query_text=query_text,
            start_time=time.time(),
            session_id=session_id,
            response_mode=response_mode,
            analysis_zone=analysis_zone,
        )
        self._traces.append(trace)
        if len(self._traces) > MAX_TRACE_HISTORY:
            self._traces = self._traces[-MAX_TRACE_HISTORY:]
        self._query_count += 1
        logger.debug(f"Trace started: {trace.trace_id} | query='{query_text[:80]}'")
        return trace

    def complete_trace(
        self,
        trace: QueryTrace,
        final_layer: ResponseLayer,
        doctrine_hit: bool = False,
        doctrine_topic: Optional[str] = None,
        confidence_level: Optional[str] = None,
        determinism_hash: Optional[str] = None,
    ) -> None:
        """Complete a query trace and record metrics."""
        trace.complete(
            final_layer=final_layer,
            doctrine_hit=doctrine_hit,
            doctrine_topic=doctrine_topic,
            confidence_level=confidence_level,
            determinism_hash=determinism_hash,
        )
        if trace.total_duration_ms is not None:
            layer_key = final_layer.value
            self._latencies[layer_key].append(trace.total_duration_ms)
            if len(self._latencies[layer_key]) > MAX_LATENCY_SAMPLES:
                self._latencies[layer_key] = self._latencies[layer_key][-MAX_LATENCY_SAMPLES:]
            self._layer_counts[layer_key] = self._layer_counts.get(layer_key, 0) + 1

        if doctrine_hit:
            self._doctrine_hits += 1
        else:
            self._doctrine_misses += 1

        audit_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "engine_id": ENGINE_ID,
            "trace_id": trace.trace_id,
            "query": trace.query_text[:200],
            "response_mode": trace.response_mode,
            "analysis_zone": trace.analysis_zone,
            "layer": final_layer.value,
            "duration_ms": trace.total_duration_ms,
            "doctrine_hit": doctrine_hit,
            "doctrine_topic": doctrine_topic,
            "confidence": confidence_level,
            "hash": determinism_hash,
        }
        self._pending_audit.append(audit_entry)
        if len(self._pending_audit) >= AUDIT_FLUSH_THRESHOLD:
            self._flush_audit()

        logger.info(
            f"Trace complete: {trace.trace_id} | "
            f"layer={final_layer.value} | "
            f"duration={trace.total_duration_ms:.1f}ms | "
            f"hit={doctrine_hit}"
        )

    # --------------------------------------------------------------------------
    # ERROR RECORDING
    # --------------------------------------------------------------------------

    def log_error(
        self,
        domain: ErrorDomain,
        message: str,
        trace_id: Optional[str] = None,
        stack_trace: Optional[str] = None,
        query_context: Optional[str] = None,
        severity: str = "ERROR",
    ) -> ErrorRecord:
        """Record a structured error."""
        record = ErrorRecord(
            error_id=str(uuid.uuid4())[:12],
            timestamp=time.time(),
            domain=domain,
            message=message,
            trace_id=trace_id,
            stack_trace=stack_trace,
            query_context=query_context,
            severity=severity,
        )
        self._errors.append(record)
        if len(self._errors) > MAX_ERROR_HISTORY:
            self._errors = self._errors[-MAX_ERROR_HISTORY:]
        self._error_counts[domain.value] += 1
        logger.error(f"[{domain.value}] {message} (trace={trace_id})")
        self._write_error_log(record)
        return record

    def _write_error_log(self, record: ErrorRecord) -> None:
        """Append error record to error log file."""
        try:
            with open(ERROR_LOG_PATH, "a", encoding="utf-8") as f:
                f.write(json.dumps(record.to_dict()) + "\n")
        except Exception as exc:
            logger.warning(f"Failed to write error log: {exc}")

    # --------------------------------------------------------------------------
    # DOCTRINE MUTATION TRACKING
    # --------------------------------------------------------------------------

    def record_doctrine_mutation(
        self,
        topic: str,
        mutation_type: MutationType,
        origin: MutationOrigin,
        description: str = "",
        before_hash: Optional[str] = None,
        after_hash: Optional[str] = None,
        approved_by: Optional[str] = None,
    ) -> DoctrineMutationRecord:
        """Record a doctrine content mutation for drift analysis."""
        record = DoctrineMutationRecord(
            mutation_id=str(uuid.uuid4())[:12],
            timestamp=time.time(),
            topic=topic,
            mutation_type=mutation_type,
            origin=origin,
            before_hash=before_hash,
            after_hash=after_hash,
            description=description,
            approved_by=approved_by,
        )
        self._mutations.append(record)
        logger.info(
            f"Doctrine mutation: {topic} | type={mutation_type.value} | "
            f"origin={origin.value}"
        )
        return record

    # --------------------------------------------------------------------------
    # AUDIT TRAIL PERSISTENCE
    # --------------------------------------------------------------------------

    def _flush_audit(self) -> None:
        """Flush pending audit entries to JSONL file."""
        if not self._pending_audit:
            return
        try:
            with open(AUDIT_LOG_PATH, "a", encoding="utf-8") as f:
                for entry in self._pending_audit:
                    f.write(json.dumps(entry) + "\n")
            flushed_count = len(self._pending_audit)
            self._pending_audit.clear()
            self._last_flush = time.time()
            logger.debug(f"Flushed {flushed_count} audit entries to {AUDIT_LOG_PATH}")
        except Exception as exc:
            logger.error(f"Failed to flush audit trail: {exc}")

    def flush(self) -> None:
        """Public flush for graceful shutdown."""
        self._flush_audit()

    # --------------------------------------------------------------------------
    # METRICS AND REPORTING
    # --------------------------------------------------------------------------

    def get_metrics(self) -> Dict[str, Any]:
        """Return current operational metrics."""
        uptime_seconds = time.time() - self._start_time
        total_hit_miss = self._doctrine_hits + self._doctrine_misses
        hit_rate = (self._doctrine_hits / total_hit_miss * 100) if total_hit_miss > 0 else 0.0

        latency_stats = {}
        for layer_name, samples in self._latencies.items():
            if samples:
                sorted_samples = sorted(samples)
                latency_stats[layer_name] = {
                    "count": len(sorted_samples),
                    "mean_ms": sum(sorted_samples) / len(sorted_samples),
                    "min_ms": sorted_samples[0],
                    "max_ms": sorted_samples[-1],
                    "p50_ms": sorted_samples[len(sorted_samples) // 2],
                    "p95_ms": sorted_samples[int(len(sorted_samples) * 0.95)],
                    "p99_ms": sorted_samples[int(len(sorted_samples) * 0.99)],
                }

        return {
            "engine_id": ENGINE_ID,
            "engine_name": ENGINE_NAME,
            "telemetry_version": TELEMETRY_VERSION,
            "uptime_seconds": round(uptime_seconds, 1),
            "total_queries": self._query_count,
            "queries_per_hour": round(self._query_count / max(uptime_seconds / 3600, 0.001), 2),
            "doctrine_hits": self._doctrine_hits,
            "doctrine_misses": self._doctrine_misses,
            "doctrine_hit_rate_pct": round(hit_rate, 2),
            "layer_distribution": dict(self._layer_counts),
            "latency_stats": latency_stats,
            "error_counts_by_domain": dict(self._error_counts),
            "total_errors": sum(self._error_counts.values()),
            "mutation_count": len(self._mutations),
            "pending_audit_entries": len(self._pending_audit),
            "last_flush_time": datetime.fromtimestamp(self._last_flush, tz=timezone.utc).isoformat(),
        }

    def get_recent_traces(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Return recent query traces."""
        recent = self._traces[-limit:] if self._traces else []
        return [t.to_dict() for t in reversed(recent)]

    def get_recent_errors(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Return recent error records."""
        recent = self._errors[-limit:] if self._errors else []
        return [e.to_dict() for e in reversed(recent)]

    def get_mutation_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Return doctrine mutation history."""
        recent = self._mutations[-limit:] if self._mutations else []
        return [m.to_dict() for m in reversed(recent)]

    def get_error_rate(self, window_seconds: int = 3600) -> float:
        """Calculate error rate over a time window."""
        cutoff = time.time() - window_seconds
        recent_errors = sum(1 for e in self._errors if e.timestamp > cutoff)
        recent_queries = sum(1 for t in self._traces if t.start_time > cutoff)
        if recent_queries == 0:
            return 0.0
        return round(recent_errors / recent_queries * 100, 2)

    def compute_determinism_hash(self, content: str) -> str:
        """Compute SHA-256 determinism hash for a response."""
        return hashlib.sha256(content.encode("utf-8")).hexdigest()


# ==============================================================================
# MODULE-LEVEL SINGLETON
# ==============================================================================

_telemetry_instance: Optional[TelemetryCollector] = None


def get_telemetry() -> TelemetryCollector:
    """Get or create the global telemetry collector."""
    global _telemetry_instance
    if _telemetry_instance is None:
        _telemetry_instance = TelemetryCollector()
    return _telemetry_instance


def trace_query(
    query_text: str,
    session_id: Optional[str] = None,
    response_mode: Optional[str] = None,
    analysis_zone: Optional[str] = None,
) -> QueryTrace:
    """Convenience: start a new query trace."""
    return get_telemetry().start_trace(query_text, session_id, response_mode, analysis_zone)


def complete_trace(
    trace: QueryTrace,
    final_layer: ResponseLayer,
    doctrine_hit: bool = False,
    doctrine_topic: Optional[str] = None,
    confidence_level: Optional[str] = None,
    determinism_hash: Optional[str] = None,
) -> None:
    """Convenience: complete a query trace."""
    get_telemetry().complete_trace(
        trace, final_layer, doctrine_hit, doctrine_topic, confidence_level, determinism_hash
    )


def log_error(
    domain: ErrorDomain,
    message: str,
    trace_id: Optional[str] = None,
    stack_trace: Optional[str] = None,
    query_context: Optional[str] = None,
    severity: str = "ERROR",
) -> ErrorRecord:
    """Convenience: log an error."""
    return get_telemetry().log_error(domain, message, trace_id, stack_trace, query_context, severity)


def record_doctrine_mutation(
    topic: str,
    mutation_type: MutationType,
    origin: MutationOrigin,
    description: str = "",
    before_hash: Optional[str] = None,
    after_hash: Optional[str] = None,
    approved_by: Optional[str] = None,
) -> DoctrineMutationRecord:
    """Convenience: record a doctrine mutation."""
    return get_telemetry().record_doctrine_mutation(
        topic, mutation_type, origin, description, before_hash, after_hash, approved_by
    )
