"""
TX12 Oil & Gas Tax Engine — Telemetry Module
Full query tracing, latency tracking, error domain classification,
and doctrine mutation auditing for the Oil & Gas Tax Intelligence Engine.

Author: ECHO OMEGA PRIME
Engine: TX12 Oil & Gas Tax
Version: 1.0.0
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

import hashlib
import json
import time
import uuid

from loguru import logger

# ==============================================================================
# TELEMETRY CONFIGURATION
# ==============================================================================

TELEMETRY_DIR = Path("O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/TX12_oil_gas_tax/telemetry_data")
TELEMETRY_DIR.mkdir(parents=True, exist_ok=True)

TRACE_LOG = TELEMETRY_DIR / "query_traces.jsonl"
ERROR_LOG = TELEMETRY_DIR / "error_traces.jsonl"
MUTATION_LOG = TELEMETRY_DIR / "doctrine_mutations.jsonl"
METRICS_LOG = TELEMETRY_DIR / "metrics_snapshots.jsonl"


# ==============================================================================
# ENUMS
# ==============================================================================

class ErrorDomain(str, Enum):
    """Classification of error origin domains."""
    DOCTRINE_MATCH = "doctrine_match"
    SEMANTIC_NORMALIZATION = "semantic_normalization"
    VECTOR_SEARCH = "vector_search"
    DEEP_ANALYSIS = "deep_analysis"
    AUTHORITY_RESOLUTION = "authority_resolution"
    CONFIDENCE_SCORING = "confidence_scoring"
    SERIALIZATION = "serialization"
    INPUT_VALIDATION = "input_validation"
    COVERAGE_MAP = "coverage_map"
    DRIFT_DETECTION = "drift_detection"
    FRAGILITY_SCORING = "fragility_scoring"
    ZONED_ANALYSIS = "zoned_analysis"
    STRATIFICATION = "stratification"
    INFRASTRUCTURE = "infrastructure"
    UNKNOWN = "unknown"


class ResponseLayer(str, Enum):
    """Which layer resolved the query."""
    DOCTRINE_CACHE = "doctrine_cache"
    SEMANTIC_RETRIEVAL = "semantic_retrieval"
    DEEP_ANALYSIS = "deep_analysis"
    STRATIFIED = "stratified"
    FALLBACK = "fallback"


class MutationType(str, Enum):
    """Types of doctrine mutations tracked."""
    BLOCK_ADDED = "block_added"
    BLOCK_MODIFIED = "block_modified"
    BLOCK_REMOVED = "block_removed"
    KEYWORD_ADDED = "keyword_added"
    KEYWORD_REMOVED = "keyword_removed"
    AUTHORITY_UPDATED = "authority_updated"
    CONFIDENCE_CHANGED = "confidence_changed"
    PRECEDENT_UPDATED = "precedent_updated"
    INTERACTION_ADDED = "interaction_added"
    INTERACTION_REMOVED = "interaction_removed"


class MutationOrigin(str, Enum):
    """Source of a doctrine mutation."""
    MANUAL = "manual"
    DRIFT_WATCHER = "drift_watcher"
    AUTO_CORRECTION = "auto_correction"
    LEGISLATIVE_UPDATE = "legislative_update"
    CASE_LAW_UPDATE = "case_law_update"
    REGULATORY_UPDATE = "regulatory_update"


# ==============================================================================
# TRACE STRUCTURES
# ==============================================================================

@dataclass
class QueryTrace:
    """Full trace of a single query execution."""
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    query_text: str = ""
    query_hash: str = ""
    mode: str = "fast"
    entity_type: Optional[str] = None
    jurisdiction: str = "US"
    tax_year: Optional[int] = None

    # Timing
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    total_latency_ms: float = 0.0

    # Layer timings
    doctrine_match_ms: float = 0.0
    semantic_retrieval_ms: float = 0.0
    deep_analysis_ms: float = 0.0
    normalization_ms: float = 0.0
    authority_resolution_ms: float = 0.0
    fragility_scoring_ms: float = 0.0
    zoned_analysis_ms: float = 0.0
    serialization_ms: float = 0.0

    # Resolution
    response_layer: ResponseLayer = ResponseLayer.FALLBACK
    doctrine_matched: bool = False
    doctrine_topic: Optional[str] = None
    match_score: int = 0
    authority_weight: int = 0
    conflict_detected: bool = False
    multi_doctrine: bool = False
    doctrines_matched_count: int = 0

    # Coverage
    coverage_triggered: int = 0
    coverage_not_triggered: int = 0
    coverage_missing: int = 0
    epistemic_gap_detected: bool = False

    # Confidence
    confidence_tier: str = "requires_review"
    confidence_stratification: Optional[str] = None

    # Errors
    errors: List[Dict[str, Any]] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    # Determinism
    determinism_hash: str = ""
    response_hash: str = ""

    def complete(self) -> None:
        """Mark trace as complete and calculate total latency."""
        self.end_time = time.time()
        self.total_latency_ms = round((self.end_time - self.start_time) * 1000, 2)

    def add_error(self, domain: ErrorDomain, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        """Record an error within this trace."""
        self.errors.append({
            "domain": domain.value,
            "message": message,
            "details": details or {},
            "timestamp": datetime.now(timezone.utc).isoformat()
        })

    def add_warning(self, message: str) -> None:
        """Record a non-fatal warning."""
        self.warnings.append(message)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize trace for JSONL storage."""
        return {
            "trace_id": self.trace_id,
            "query_text": self.query_text[:200],
            "query_hash": self.query_hash,
            "mode": self.mode,
            "entity_type": self.entity_type,
            "jurisdiction": self.jurisdiction,
            "tax_year": self.tax_year,
            "start_time": datetime.fromtimestamp(self.start_time, tz=timezone.utc).isoformat(),
            "end_time": datetime.fromtimestamp(self.end_time, tz=timezone.utc).isoformat() if self.end_time else None,
            "total_latency_ms": self.total_latency_ms,
            "layer_timings": {
                "doctrine_match_ms": self.doctrine_match_ms,
                "semantic_retrieval_ms": self.semantic_retrieval_ms,
                "deep_analysis_ms": self.deep_analysis_ms,
                "normalization_ms": self.normalization_ms,
                "authority_resolution_ms": self.authority_resolution_ms,
                "fragility_scoring_ms": self.fragility_scoring_ms,
                "zoned_analysis_ms": self.zoned_analysis_ms,
                "serialization_ms": self.serialization_ms
            },
            "response_layer": self.response_layer.value,
            "doctrine_matched": self.doctrine_matched,
            "doctrine_topic": self.doctrine_topic,
            "match_score": self.match_score,
            "authority_weight": self.authority_weight,
            "conflict_detected": self.conflict_detected,
            "multi_doctrine": self.multi_doctrine,
            "doctrines_matched_count": self.doctrines_matched_count,
            "coverage": {
                "triggered": self.coverage_triggered,
                "not_triggered": self.coverage_not_triggered,
                "missing": self.coverage_missing,
                "epistemic_gap": self.epistemic_gap_detected
            },
            "confidence_tier": self.confidence_tier,
            "confidence_stratification": self.confidence_stratification,
            "errors": self.errors,
            "warnings": self.warnings,
            "determinism_hash": self.determinism_hash,
            "response_hash": self.response_hash
        }


@dataclass
class ErrorTrace:
    """Detailed error trace for post-mortem analysis."""
    error_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    trace_id: Optional[str] = None
    domain: ErrorDomain = ErrorDomain.UNKNOWN
    severity: str = "medium"
    message: str = ""
    stack_trace: Optional[str] = None
    query_context: Optional[str] = None
    resolution: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        """Serialize for JSONL storage."""
        return {
            "error_id": self.error_id,
            "trace_id": self.trace_id,
            "domain": self.domain.value,
            "severity": self.severity,
            "message": self.message,
            "stack_trace": self.stack_trace,
            "query_context": self.query_context[:200] if self.query_context else None,
            "resolution": self.resolution,
            "timestamp": self.timestamp
        }


@dataclass
class DoctrineMutation:
    """Record of a doctrine cache change."""
    mutation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    mutation_type: MutationType = MutationType.BLOCK_MODIFIED
    origin: MutationOrigin = MutationOrigin.MANUAL
    doctrine_topic: str = ""
    field_changed: Optional[str] = None
    old_value_hash: Optional[str] = None
    new_value_hash: Optional[str] = None
    reason: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        """Serialize for JSONL storage."""
        return {
            "mutation_id": self.mutation_id,
            "mutation_type": self.mutation_type.value,
            "origin": self.origin.value,
            "doctrine_topic": self.doctrine_topic,
            "field_changed": self.field_changed,
            "old_value_hash": self.old_value_hash,
            "new_value_hash": self.new_value_hash,
            "reason": self.reason,
            "timestamp": self.timestamp
        }


# ==============================================================================
# TELEMETRY COLLECTOR
# ==============================================================================

class TelemetryCollector:
    """Central telemetry collection and persistence for TX12 Oil & Gas Tax Engine.

    Responsibilities:
        - Create and manage query traces
        - Persist traces to JSONL audit files
        - Track error domains and frequencies
        - Record doctrine mutations
        - Generate metrics snapshots
    """

    def __init__(self) -> None:
        """Initialize telemetry collector with empty state."""
        self._traces: List[QueryTrace] = []
        self._errors: List[ErrorTrace] = []
        self._mutations: List[DoctrineMutation] = []
        self._max_in_memory: int = 500
        self._total_traces: int = 0
        self._total_errors: int = 0
        self._total_mutations: int = 0
        self._start_time: float = time.time()
        self._error_domain_counts: Dict[str, int] = {}
        self._layer_counts: Dict[str, int] = {}
        logger.info("TX12 TelemetryCollector initialized")

    def create_trace(self, query_text: str, mode: str = "fast",
                     entity_type: Optional[str] = None,
                     jurisdiction: str = "US",
                     tax_year: Optional[int] = None) -> QueryTrace:
        """Create a new query trace."""
        trace = QueryTrace(
            query_text=query_text,
            query_hash=hashlib.sha256(query_text.encode()).hexdigest()[:16],
            mode=mode,
            entity_type=entity_type,
            jurisdiction=jurisdiction,
            tax_year=tax_year
        )
        return trace

    def complete_trace(self, trace: QueryTrace) -> None:
        """Complete and persist a query trace."""
        trace.complete()

        # Track layer resolution counts
        layer_key = trace.response_layer.value
        self._layer_counts[layer_key] = self._layer_counts.get(layer_key, 0) + 1

        # Persist to file
        self._persist_trace(trace)

        # Keep in memory (bounded)
        self._traces.append(trace)
        if len(self._traces) > self._max_in_memory:
            self._traces.pop(0)
        self._total_traces += 1

        logger.info(
            f"Trace complete: {trace.trace_id} | "
            f"layer={trace.response_layer.value} | "
            f"latency={trace.total_latency_ms}ms | "
            f"doctrine={trace.doctrine_topic or 'none'}"
        )

    def log_error(self, domain: ErrorDomain, message: str,
                  trace_id: Optional[str] = None,
                  severity: str = "medium",
                  stack_trace: Optional[str] = None,
                  query_context: Optional[str] = None) -> ErrorTrace:
        """Log an error with full context."""
        error = ErrorTrace(
            trace_id=trace_id,
            domain=domain,
            severity=severity,
            message=message,
            stack_trace=stack_trace,
            query_context=query_context
        )

        # Track domain counts
        domain_key = domain.value
        self._error_domain_counts[domain_key] = self._error_domain_counts.get(domain_key, 0) + 1

        # Persist
        self._persist_error(error)

        # Keep in memory (bounded)
        self._errors.append(error)
        if len(self._errors) > self._max_in_memory:
            self._errors.pop(0)
        self._total_errors += 1

        logger.error(f"TX12 Error [{domain.value}]: {message}")
        return error

    def record_doctrine_mutation(self, mutation_type: MutationType,
                                  origin: MutationOrigin,
                                  doctrine_topic: str,
                                  reason: str,
                                  field_changed: Optional[str] = None,
                                  old_value: Optional[str] = None,
                                  new_value: Optional[str] = None) -> DoctrineMutation:
        """Record a doctrine cache mutation for audit trail."""
        mutation = DoctrineMutation(
            mutation_type=mutation_type,
            origin=origin,
            doctrine_topic=doctrine_topic,
            field_changed=field_changed,
            old_value_hash=hashlib.sha256(old_value.encode()).hexdigest()[:16] if old_value else None,
            new_value_hash=hashlib.sha256(new_value.encode()).hexdigest()[:16] if new_value else None,
            reason=reason
        )

        # Persist
        self._persist_mutation(mutation)

        self._mutations.append(mutation)
        if len(self._mutations) > self._max_in_memory:
            self._mutations.pop(0)
        self._total_mutations += 1

        logger.info(f"Doctrine mutation: {mutation_type.value} on {doctrine_topic} ({reason})")
        return mutation

    def get_metrics_snapshot(self) -> Dict[str, Any]:
        """Generate a comprehensive metrics snapshot."""
        uptime = time.time() - self._start_time
        recent_traces = [t for t in self._traces if t.end_time and t.end_time > time.time() - 3600]
        recent_latencies = [t.total_latency_ms for t in recent_traces]

        latency_stats = {}
        if recent_latencies:
            sorted_lat = sorted(recent_latencies)
            latency_stats = {
                "avg_ms": round(sum(recent_latencies) / len(recent_latencies), 2),
                "p50_ms": round(sorted_lat[len(sorted_lat) // 2], 2),
                "p95_ms": round(sorted_lat[int(len(sorted_lat) * 0.95)], 2),
                "p99_ms": round(sorted_lat[int(len(sorted_lat) * 0.99)], 2),
                "min_ms": round(sorted_lat[0], 2),
                "max_ms": round(sorted_lat[-1], 2)
            }
        else:
            latency_stats = {"avg_ms": 0.0, "p50_ms": 0.0, "p95_ms": 0.0,
                             "p99_ms": 0.0, "min_ms": 0.0, "max_ms": 0.0}

        doctrine_hits = sum(1 for t in recent_traces if t.doctrine_matched)
        doctrine_total = len(recent_traces)
        hit_rate = round(doctrine_hits / doctrine_total, 3) if doctrine_total > 0 else 1.0

        snapshot = {
            "engine": "TX12_oil_gas_tax",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "uptime_seconds": round(uptime, 1),
            "totals": {
                "traces": self._total_traces,
                "errors": self._total_errors,
                "mutations": self._total_mutations
            },
            "last_hour": {
                "queries": len(recent_traces),
                "latency": latency_stats,
                "doctrine_hit_rate": hit_rate,
                "errors": sum(1 for e in self._errors
                              if e.timestamp > datetime.fromtimestamp(
                                  time.time() - 3600, tz=timezone.utc).isoformat())
            },
            "error_domains": dict(self._error_domain_counts),
            "layer_distribution": dict(self._layer_counts),
            "multi_doctrine_rate": round(
                sum(1 for t in recent_traces if t.multi_doctrine) / max(len(recent_traces), 1), 3
            ),
            "conflict_rate": round(
                sum(1 for t in recent_traces if t.conflict_detected) / max(len(recent_traces), 1), 3
            ),
            "epistemic_gap_rate": round(
                sum(1 for t in recent_traces if t.epistemic_gap_detected) / max(len(recent_traces), 1), 3
            )
        }

        # Persist snapshot
        self._persist_metrics_snapshot(snapshot)
        return snapshot

    def get_recent_errors(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recent errors for health endpoint."""
        return [e.to_dict() for e in self._errors[-limit:]]

    def get_error_domain_summary(self) -> Dict[str, int]:
        """Get error counts by domain."""
        return dict(self._error_domain_counts)

    # --------------------------------------------------------------------------
    # PERSISTENCE
    # --------------------------------------------------------------------------

    def _persist_trace(self, trace: QueryTrace) -> None:
        """Append trace to JSONL file."""
        try:
            with TRACE_LOG.open("a", encoding="utf-8") as f:
                f.write(json.dumps(trace.to_dict(), default=str) + "\n")
        except Exception as exc:
            logger.error(f"Failed to persist trace: {exc}")

    def _persist_error(self, error: ErrorTrace) -> None:
        """Append error trace to JSONL file."""
        try:
            with ERROR_LOG.open("a", encoding="utf-8") as f:
                f.write(json.dumps(error.to_dict(), default=str) + "\n")
        except Exception as exc:
            logger.error(f"Failed to persist error trace: {exc}")

    def _persist_mutation(self, mutation: DoctrineMutation) -> None:
        """Append mutation record to JSONL file."""
        try:
            with MUTATION_LOG.open("a", encoding="utf-8") as f:
                f.write(json.dumps(mutation.to_dict(), default=str) + "\n")
        except Exception as exc:
            logger.error(f"Failed to persist mutation record: {exc}")

    def _persist_metrics_snapshot(self, snapshot: Dict[str, Any]) -> None:
        """Append metrics snapshot to JSONL file."""
        try:
            with METRICS_LOG.open("a", encoding="utf-8") as f:
                f.write(json.dumps(snapshot, default=str) + "\n")
        except Exception as exc:
            logger.error(f"Failed to persist metrics snapshot: {exc}")


# ==============================================================================
# MODULE-LEVEL SINGLETON
# ==============================================================================

_telemetry: Optional[TelemetryCollector] = None


def get_telemetry() -> TelemetryCollector:
    """Get or create the global telemetry collector."""
    global _telemetry
    if _telemetry is None:
        _telemetry = TelemetryCollector()
    return _telemetry


def trace_query(query_text: str, mode: str = "fast",
                entity_type: Optional[str] = None,
                jurisdiction: str = "US",
                tax_year: Optional[int] = None) -> QueryTrace:
    """Convenience: create a new trace via the global collector."""
    return get_telemetry().create_trace(query_text, mode, entity_type, jurisdiction, tax_year)


def complete_trace(trace: QueryTrace) -> None:
    """Convenience: complete a trace via the global collector."""
    get_telemetry().complete_trace(trace)


def log_error(domain: ErrorDomain, message: str,
              trace_id: Optional[str] = None,
              severity: str = "medium",
              stack_trace: Optional[str] = None,
              query_context: Optional[str] = None) -> ErrorTrace:
    """Convenience: log an error via the global collector."""
    return get_telemetry().log_error(domain, message, trace_id, severity, stack_trace, query_context)


def record_doctrine_mutation(mutation_type: MutationType,
                              origin: MutationOrigin,
                              doctrine_topic: str,
                              reason: str,
                              field_changed: Optional[str] = None,
                              old_value: Optional[str] = None,
                              new_value: Optional[str] = None) -> DoctrineMutation:
    """Convenience: record a doctrine mutation via the global collector."""
    return get_telemetry().record_doctrine_mutation(
        mutation_type, origin, doctrine_topic, reason,
        field_changed, old_value, new_value
    )
