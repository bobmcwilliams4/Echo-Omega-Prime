"""
TX13 Real Estate Tax Engine - Telemetry Module
Full query tracing, latency tracking, error domains, and audit trail.

Author: ECHO OMEGA PRIME
Engine: TX13 Real Estate Tax
Port: 8463
"""

from __future__ import annotations

import hashlib
import json
import time
import uuid
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

from loguru import logger
from pydantic import BaseModel, Field


# =============================================================================
# CONSTANTS
# =============================================================================

ENGINE_ID: str = "TX13"
ENGINE_NAME: str = "Real Estate Tax Intelligence Engine"
ENGINE_VERSION: str = "1.0.0"
ENGINE_PORT: int = 8463

LOG_DIR: Path = Path("O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/TX13_real_estate_tax/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

AUDIT_LOG_PATH: Path = LOG_DIR / "audit_trail.jsonl"
TELEMETRY_LOG_PATH: Path = LOG_DIR / "telemetry.jsonl"
ERROR_LOG_PATH: Path = LOG_DIR / "errors.jsonl"

logger.add(
    LOG_DIR / "tx13_telemetry_{time}.log",
    rotation="50 MB",
    retention="30 days",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {module}:{function}:{line} | {message}",
)


# =============================================================================
# ENUMS
# =============================================================================

class ResponseLayer(str, Enum):
    """Which layer handled the query."""
    DOCTRINE_CACHE = "doctrine_cache"
    SEMANTIC_RETRIEVAL = "semantic_retrieval"
    DEEP_ANALYSIS = "deep_analysis"
    ERROR_FALLBACK = "error_fallback"


class ErrorDomain(str, Enum):
    """Classification of error domains for tracking."""
    DOCTRINE_LOOKUP = "doctrine_lookup"
    SEMANTIC_SEARCH = "semantic_search"
    DEEP_ANALYSIS = "deep_analysis"
    INPUT_VALIDATION = "input_validation"
    SERIALIZATION = "serialization"
    AUTHORITY_RESOLUTION = "authority_resolution"
    CONFIDENCE_SCORING = "confidence_scoring"
    DEPRECIATION_CALC = "depreciation_calc"
    EXCHANGE_TIMING = "exchange_timing"
    PASSIVE_ACTIVITY = "passive_activity"
    REIT_COMPLIANCE = "reit_compliance"
    INSTALLMENT_CALC = "installment_calc"
    UNKNOWN = "unknown"


class MutationType(str, Enum):
    """Types of doctrine mutations tracked."""
    DOCTRINE_ADDED = "doctrine_added"
    DOCTRINE_MODIFIED = "doctrine_modified"
    DOCTRINE_DEPRECATED = "doctrine_deprecated"
    AUTHORITY_WEIGHT_CHANGED = "authority_weight_changed"
    CONFIDENCE_OVERRIDE = "confidence_override"
    KEYWORD_EXPANSION = "keyword_expansion"
    REASONING_UPDATE = "reasoning_update"


class MutationOrigin(str, Enum):
    """Where a mutation originated."""
    SYSTEM_UPDATE = "system_update"
    COMMANDER_OVERRIDE = "commander_override"
    DRIFT_DETECTION = "drift_detection"
    COVERAGE_GAP_FILL = "coverage_gap_fill"
    LEGISLATIVE_CHANGE = "legislative_change"
    CASE_LAW_UPDATE = "case_law_update"


# =============================================================================
# PYDANTIC MODELS
# =============================================================================

class TraceRecord(BaseModel):
    """A single query trace record."""
    trace_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    engine_id: str = ENGINE_ID
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    query_text: str = ""
    normalized_query: str = ""
    response_mode: str = "FAST"
    layer_hit: ResponseLayer = ResponseLayer.DOCTRINE_CACHE
    doctrine_topic: Optional[str] = None
    latency_ms: float = 0.0
    confidence: Optional[str] = None
    error: Optional[str] = None
    error_domain: Optional[ErrorDomain] = None
    determinism_hash: Optional[str] = None
    irc_sections_referenced: List[str] = Field(default_factory=list)
    authority_chain: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class AuditEntry(BaseModel):
    """An entry in the append-only audit trail."""
    audit_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    engine_id: str = ENGINE_ID
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    event_type: str = "query"
    trace_id: Optional[str] = None
    query_text: str = ""
    response_summary: str = ""
    doctrine_topic: Optional[str] = None
    layer_hit: Optional[str] = None
    latency_ms: float = 0.0
    confidence: Optional[str] = None
    determinism_hash: Optional[str] = None
    client_ip: Optional[str] = None
    user_agent: Optional[str] = None


class DoctrineMutationRecord(BaseModel):
    """Record of any change to doctrine content."""
    mutation_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    engine_id: str = ENGINE_ID
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    mutation_type: MutationType
    origin: MutationOrigin
    doctrine_topic: str
    field_changed: str
    old_value_hash: Optional[str] = None
    new_value_hash: Optional[str] = None
    reason: str = ""


class TelemetrySnapshot(BaseModel):
    """Point-in-time telemetry snapshot."""
    engine_id: str = ENGINE_ID
    engine_name: str = ENGINE_NAME
    engine_version: str = ENGINE_VERSION
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    uptime_seconds: float = 0.0
    total_queries: int = 0
    total_errors: int = 0
    error_rate: float = 0.0
    avg_latency_ms: float = 0.0
    p50_latency_ms: float = 0.0
    p95_latency_ms: float = 0.0
    p99_latency_ms: float = 0.0
    doctrine_hit_rate: float = 0.0
    doctrine_hits: int = 0
    doctrine_misses: int = 0
    active_traces: int = 0
    queries_per_minute: float = 0.0
    layer_distribution: Dict[str, int] = Field(default_factory=dict)
    top_doctrines: List[Dict[str, Any]] = Field(default_factory=list)
    recent_errors: List[Dict[str, Any]] = Field(default_factory=list)


# =============================================================================
# TELEMETRY ENGINE
# =============================================================================

class RealEstateTelemetry:
    """
    Full telemetry system for the TX13 Real Estate Tax Engine.

    Tracks query traces, latencies, error domains, doctrine hit rates,
    and maintains an append-only audit trail for forensic review.
    """

    def __init__(self) -> None:
        self._start_time: float = time.time()
        self._traces: Dict[str, TraceRecord] = {}
        self._completed_traces: List[TraceRecord] = []
        self._max_completed: int = 1000
        self._latencies: List[float] = []
        self._max_latencies: int = 500
        self._errors: List[Dict[str, Any]] = []
        self._max_errors: int = 200
        self._query_timestamps: List[float] = []
        self._doctrine_hits: int = 0
        self._doctrine_misses: int = 0
        self._total_queries: int = 0
        self._total_errors: int = 0
        self._layer_counts: Dict[str, int] = {
            ResponseLayer.DOCTRINE_CACHE.value: 0,
            ResponseLayer.SEMANTIC_RETRIEVAL.value: 0,
            ResponseLayer.DEEP_ANALYSIS.value: 0,
            ResponseLayer.ERROR_FALLBACK.value: 0,
        }
        self._doctrine_usage: Dict[str, int] = {}
        self._mutations: List[DoctrineMutationRecord] = []
        logger.info("TX13 Telemetry initialized | engine={} version={}", ENGINE_ID, ENGINE_VERSION)

    # -------------------------------------------------------------------------
    # TRACE LIFECYCLE
    # -------------------------------------------------------------------------

    def start_trace(self, query_text: str, response_mode: str = "FAST") -> str:
        """Begin a new query trace. Returns the trace_id."""
        trace = TraceRecord(
            query_text=query_text,
            response_mode=response_mode,
        )
        self._traces[trace.trace_id] = trace
        self._total_queries += 1
        self._query_timestamps.append(time.time())
        self._prune_query_timestamps()
        logger.debug("Trace started | trace_id={} mode={}", trace.trace_id, response_mode)
        return trace.trace_id

    def complete_trace(
        self,
        trace_id: str,
        layer_hit: ResponseLayer,
        doctrine_topic: Optional[str] = None,
        confidence: Optional[str] = None,
        determinism_hash: Optional[str] = None,
        irc_sections: Optional[List[str]] = None,
        authority_chain: Optional[List[str]] = None,
        error: Optional[str] = None,
        error_domain: Optional[ErrorDomain] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Optional[TraceRecord]:
        """Complete a trace with results."""
        trace = self._traces.pop(trace_id, None)
        if trace is None:
            logger.warning("Trace not found for completion | trace_id={}", trace_id)
            return None

        now = time.time()
        start_ts = datetime.fromisoformat(trace.timestamp).timestamp()
        latency_ms = (now - start_ts) * 1000.0

        trace.layer_hit = layer_hit
        trace.doctrine_topic = doctrine_topic
        trace.latency_ms = round(latency_ms, 2)
        trace.confidence = confidence
        trace.determinism_hash = determinism_hash
        trace.error = error
        trace.error_domain = error_domain
        if irc_sections:
            trace.irc_sections_referenced = irc_sections
        if authority_chain:
            trace.authority_chain = authority_chain
        if metadata:
            trace.metadata = metadata

        self._record_latency(trace.latency_ms)
        self._layer_counts[layer_hit.value] = self._layer_counts.get(layer_hit.value, 0) + 1

        if doctrine_topic:
            self._doctrine_hits += 1
            self._doctrine_usage[doctrine_topic] = self._doctrine_usage.get(doctrine_topic, 0) + 1
        else:
            self._doctrine_misses += 1

        if error:
            self._record_error(trace_id, error, error_domain)

        self._completed_traces.append(trace)
        if len(self._completed_traces) > self._max_completed:
            self._completed_traces = self._completed_traces[-self._max_completed:]

        self._write_audit_entry(trace)

        logger.info(
            "Trace completed | trace_id={} layer={} doctrine={} latency={:.1f}ms confidence={}",
            trace_id, layer_hit.value, doctrine_topic, latency_ms, confidence,
        )
        return trace

    # -------------------------------------------------------------------------
    # ERROR TRACKING
    # -------------------------------------------------------------------------

    def log_error(
        self,
        error_msg: str,
        error_domain: ErrorDomain = ErrorDomain.UNKNOWN,
        trace_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Log an error with domain classification."""
        self._total_errors += 1
        error_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "error": error_msg[:500],
            "domain": error_domain.value,
            "trace_id": trace_id,
            "context": context or {},
        }
        self._errors.append(error_entry)
        if len(self._errors) > self._max_errors:
            self._errors = self._errors[-self._max_errors:]

        self._write_error_log(error_entry)
        logger.error("TX13 Error | domain={} msg={}", error_domain.value, error_msg[:200])

    # -------------------------------------------------------------------------
    # DOCTRINE MUTATION TRACKING
    # -------------------------------------------------------------------------

    def record_doctrine_mutation(
        self,
        mutation_type: MutationType,
        origin: MutationOrigin,
        doctrine_topic: str,
        field_changed: str,
        old_value: Optional[str] = None,
        new_value: Optional[str] = None,
        reason: str = "",
    ) -> DoctrineMutationRecord:
        """Record a change to doctrine content for drift detection."""
        record = DoctrineMutationRecord(
            mutation_type=mutation_type,
            origin=origin,
            doctrine_topic=doctrine_topic,
            field_changed=field_changed,
            old_value_hash=hashlib.sha256(old_value.encode()).hexdigest()[:16] if old_value else None,
            new_value_hash=hashlib.sha256(new_value.encode()).hexdigest()[:16] if new_value else None,
            reason=reason,
        )
        self._mutations.append(record)
        logger.info(
            "Doctrine mutation | type={} topic={} field={} origin={}",
            mutation_type.value, doctrine_topic, field_changed, origin.value,
        )
        return record

    # -------------------------------------------------------------------------
    # METRICS / SNAPSHOT
    # -------------------------------------------------------------------------

    def get_snapshot(self) -> TelemetrySnapshot:
        """Get a point-in-time telemetry snapshot."""
        now = time.time()
        uptime = now - self._start_time
        error_rate = (self._total_errors / self._total_queries * 100.0) if self._total_queries > 0 else 0.0
        hit_rate = (
            self._doctrine_hits / (self._doctrine_hits + self._doctrine_misses) * 100.0
            if (self._doctrine_hits + self._doctrine_misses) > 0
            else 0.0
        )
        qpm = self._calculate_queries_per_minute()

        latency_stats = self._calculate_latency_percentiles()

        top_doctrines = sorted(
            self._doctrine_usage.items(), key=lambda x: x[1], reverse=True
        )[:10]

        return TelemetrySnapshot(
            uptime_seconds=round(uptime, 1),
            total_queries=self._total_queries,
            total_errors=self._total_errors,
            error_rate=round(error_rate, 2),
            avg_latency_ms=latency_stats["avg"],
            p50_latency_ms=latency_stats["p50"],
            p95_latency_ms=latency_stats["p95"],
            p99_latency_ms=latency_stats["p99"],
            doctrine_hit_rate=round(hit_rate, 2),
            doctrine_hits=self._doctrine_hits,
            doctrine_misses=self._doctrine_misses,
            active_traces=len(self._traces),
            queries_per_minute=round(qpm, 2),
            layer_distribution=dict(self._layer_counts),
            top_doctrines=[{"topic": t, "count": c} for t, c in top_doctrines],
            recent_errors=self._errors[-5:] if self._errors else [],
        )

    def get_doctrine_hit_rate(self) -> float:
        """Return doctrine cache hit rate as a percentage."""
        total = self._doctrine_hits + self._doctrine_misses
        if total == 0:
            return 0.0
        return round(self._doctrine_hits / total * 100.0, 2)

    def get_latency_stats(self) -> Dict[str, float]:
        """Return latency statistics."""
        stats = self._calculate_latency_percentiles()
        return {
            "avg_ms": stats["avg"],
            "p50_ms": stats["p50"],
            "p95_ms": stats["p95"],
            "p99_ms": stats["p99"],
            "last_ms": round(self._latencies[-1], 2) if self._latencies else 0.0,
        }

    def get_error_stats(self) -> Dict[str, Any]:
        """Return error statistics."""
        now = time.time()
        recent = [e for e in self._errors if _parse_ts(e.get("timestamp", "")) > now - 3600]
        return {
            "total": self._total_errors,
            "last_hour": len(recent),
            "last_error": self._errors[-1] if self._errors else None,
            "error_rate_pct": round(
                self._total_errors / max(self._total_queries, 1) * 100, 2
            ),
        }

    # -------------------------------------------------------------------------
    # INTERNAL HELPERS
    # -------------------------------------------------------------------------

    def _record_latency(self, latency_ms: float) -> None:
        self._latencies.append(latency_ms)
        if len(self._latencies) > self._max_latencies:
            self._latencies = self._latencies[-self._max_latencies:]

    def _record_error(
        self, trace_id: Optional[str], error_msg: str, domain: Optional[ErrorDomain]
    ) -> None:
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "trace_id": trace_id,
            "error": error_msg[:500],
            "domain": domain.value if domain else "unknown",
        }
        self._errors.append(entry)
        if len(self._errors) > self._max_errors:
            self._errors = self._errors[-self._max_errors:]

    def _calculate_latency_percentiles(self) -> Dict[str, float]:
        if not self._latencies:
            return {"avg": 0.0, "p50": 0.0, "p95": 0.0, "p99": 0.0}
        sorted_l = sorted(self._latencies)
        n = len(sorted_l)
        return {
            "avg": round(sum(sorted_l) / n, 2),
            "p50": round(sorted_l[int(n * 0.50)], 2),
            "p95": round(sorted_l[min(int(n * 0.95), n - 1)], 2),
            "p99": round(sorted_l[min(int(n * 0.99), n - 1)], 2),
        }

    def _calculate_queries_per_minute(self) -> float:
        now = time.time()
        recent = [t for t in self._query_timestamps if t > now - 60]
        return float(len(recent))

    def _prune_query_timestamps(self) -> None:
        cutoff = time.time() - 3600
        self._query_timestamps = [t for t in self._query_timestamps if t > cutoff]

    def _write_audit_entry(self, trace: TraceRecord) -> None:
        entry = AuditEntry(
            trace_id=trace.trace_id,
            query_text=trace.query_text[:500],
            response_summary=f"layer={trace.layer_hit.value} doctrine={trace.doctrine_topic}",
            doctrine_topic=trace.doctrine_topic,
            layer_hit=trace.layer_hit.value,
            latency_ms=trace.latency_ms,
            confidence=trace.confidence,
            determinism_hash=trace.determinism_hash,
        )
        try:
            with open(AUDIT_LOG_PATH, "a", encoding="utf-8") as f:
                f.write(entry.model_dump_json() + "\n")
        except OSError as e:
            logger.warning("Failed to write audit entry | error={}", str(e))

    def _write_error_log(self, error_entry: Dict[str, Any]) -> None:
        try:
            with open(ERROR_LOG_PATH, "a", encoding="utf-8") as f:
                f.write(json.dumps(error_entry, default=str) + "\n")
        except OSError as e:
            logger.warning("Failed to write error log | error={}", str(e))


# =============================================================================
# HELPERS
# =============================================================================

def _parse_ts(iso_str: str) -> float:
    """Parse ISO timestamp to epoch seconds, return 0.0 on failure."""
    try:
        return datetime.fromisoformat(iso_str).timestamp()
    except (ValueError, TypeError):
        return 0.0


# =============================================================================
# SINGLETON
# =============================================================================

_telemetry_instance: Optional[RealEstateTelemetry] = None


def get_telemetry() -> RealEstateTelemetry:
    """Get or create the singleton telemetry instance."""
    global _telemetry_instance
    if _telemetry_instance is None:
        _telemetry_instance = RealEstateTelemetry()
    return _telemetry_instance


def trace_query(query_text: str, response_mode: str = "FAST") -> str:
    """Convenience: start a trace and return trace_id."""
    return get_telemetry().start_trace(query_text, response_mode)


def complete_trace(
    trace_id: str,
    layer_hit: ResponseLayer,
    doctrine_topic: Optional[str] = None,
    confidence: Optional[str] = None,
    determinism_hash: Optional[str] = None,
    irc_sections: Optional[List[str]] = None,
    authority_chain: Optional[List[str]] = None,
    error: Optional[str] = None,
    error_domain: Optional[ErrorDomain] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> Optional[TraceRecord]:
    """Convenience: complete a trace."""
    return get_telemetry().complete_trace(
        trace_id=trace_id,
        layer_hit=layer_hit,
        doctrine_topic=doctrine_topic,
        confidence=confidence,
        determinism_hash=determinism_hash,
        irc_sections=irc_sections,
        authority_chain=authority_chain,
        error=error,
        error_domain=error_domain,
        metadata=metadata,
    )


def log_error(
    error_msg: str,
    error_domain: ErrorDomain = ErrorDomain.UNKNOWN,
    trace_id: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
) -> None:
    """Convenience: log an error."""
    get_telemetry().log_error(error_msg, error_domain, trace_id, context)


def record_doctrine_mutation(
    mutation_type: MutationType,
    origin: MutationOrigin,
    doctrine_topic: str,
    field_changed: str,
    old_value: Optional[str] = None,
    new_value: Optional[str] = None,
    reason: str = "",
) -> DoctrineMutationRecord:
    """Convenience: record a doctrine mutation."""
    return get_telemetry().record_doctrine_mutation(
        mutation_type=mutation_type,
        origin=origin,
        doctrine_topic=doctrine_topic,
        field_changed=field_changed,
        old_value=old_value,
        new_value=new_value,
        reason=reason,
    )
