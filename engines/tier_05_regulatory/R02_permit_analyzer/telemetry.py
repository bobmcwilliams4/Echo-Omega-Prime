"""
R02 Permit Analyzer - Telemetry Module
Production-grade tracing, metrics, and observability.

Author: ECHO OMEGA PRIME
Authority: 11.0 SOVEREIGN
"""

from typing import Dict, List, Optional, Any, ClassVar
from datetime import datetime, timezone
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import time
import uuid
from loguru import logger

# ==============================================================================
# TELEMETRY ENUMS
# ==============================================================================

class ErrorDomain(Enum):
    """Error classification for structured debugging."""
    INPUT_VALIDATION = "input_validation"
    DOCTRINE_RETRIEVAL = "doctrine_retrieval"
    SEMANTIC_PROCESSING = "semantic_processing"
    AUTHORITY_CONFLICT = "authority_conflict"
    CONFIGURATION = "configuration"
    EXTERNAL_DEPENDENCY = "external_dependency"
    INTERNAL_LOGIC = "internal_logic"
    UNKNOWN = "unknown"


class ResponseLayer(Enum):
    """Three-layer response architecture tracking."""
    DOCTRINE_CACHE = "doctrine_cache"
    SEMANTIC_RETRIEVAL = "semantic_retrieval"
    DEEP_ANALYSIS = "deep_analysis"


class MutationType(Enum):
    """Doctrine mutation classification."""
    AUTHORITY_OVERRIDE = "authority_override"
    CONFIDENCE_ADJUSTMENT = "confidence_adjustment"
    CONFLICT_RESOLUTION = "conflict_resolution"
    ZONE_CORRECTION = "zone_correction"


class MutationOrigin(Enum):
    """Source of doctrine mutations."""
    MANUAL_OVERRIDE = "manual_override"
    AUTOMATED_HARDENING = "automated_hardening"
    EPISTEMIC_CORRECTION = "epistemic_correction"
    COVERAGE_GAP_FILL = "coverage_gap_fill"


# ==============================================================================
# TELEMETRY DATA STRUCTURES
# ==============================================================================

@dataclass
class QueryTrace:
    """
    Complete trace for a single permit analysis query.
    Captures timing, layer selection, doctrine paths, and outcomes.
    """
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    query_text: str = ""
    normalized_query: str = ""
    permit_types_detected: List[str] = field(default_factory=list)

    # Timing breakdown
    total_latency_ms: float = 0.0
    normalization_ms: float = 0.0
    doctrine_lookup_ms: float = 0.0
    semantic_search_ms: Optional[float] = None
    synthesis_ms: Optional[float] = None

    # Layer selection
    response_layer: Optional[ResponseLayer] = None
    doctrine_cache_hit: bool = False
    doctrines_triggered: List[str] = field(default_factory=list)

    # Confidence and authority
    final_confidence: float = 0.0
    confidence_stratification: str = ""
    authority_sources: List[str] = field(default_factory=list)
    authority_conflicts: List[str] = field(default_factory=list)

    # Epistemic tracking
    fact_fragility_score: float = 0.0
    disclosure_triggered: bool = False
    coverage_gaps: List[str] = field(default_factory=list)

    # Error handling
    errors: List[str] = field(default_factory=list)
    error_domain: Optional[ErrorDomain] = None

    # Response metadata
    response_mode: str = "FAST"
    response_length: int = 0
    determinism_hash: str = ""

    def complete(self) -> Dict[str, Any]:
        """Mark trace complete and return serializable dict."""
        self.total_latency_ms = sum(filter(None, [
            self.normalization_ms,
            self.doctrine_lookup_ms,
            self.semantic_search_ms or 0.0,
            self.synthesis_ms or 0.0
        ]))

        return {
            "trace_id": self.trace_id,
            "timestamp": self.timestamp.isoformat(),
            "query_text": self.query_text,
            "normalized_query": self.normalized_query,
            "permit_types_detected": self.permit_types_detected,
            "total_latency_ms": round(self.total_latency_ms, 2),
            "normalization_ms": round(self.normalization_ms, 2),
            "doctrine_lookup_ms": round(self.doctrine_lookup_ms, 2),
            "semantic_search_ms": round(self.semantic_search_ms, 2) if self.semantic_search_ms else None,
            "synthesis_ms": round(self.synthesis_ms, 2) if self.synthesis_ms else None,
            "response_layer": self.response_layer.value if self.response_layer else None,
            "doctrine_cache_hit": self.doctrine_cache_hit,
            "doctrines_triggered": self.doctrines_triggered,
            "final_confidence": round(self.final_confidence, 3),
            "confidence_stratification": self.confidence_stratification,
            "authority_sources": self.authority_sources,
            "authority_conflicts": self.authority_conflicts,
            "fact_fragility_score": round(self.fact_fragility_score, 3),
            "disclosure_triggered": self.disclosure_triggered,
            "coverage_gaps": self.coverage_gaps,
            "errors": self.errors,
            "error_domain": self.error_domain.value if self.error_domain else None,
            "response_mode": self.response_mode,
            "response_length": self.response_length,
            "determinism_hash": self.determinism_hash
        }


# ==============================================================================
# TELEMETRY MANAGER
# ==============================================================================

class TelemetryManager:
    """
    Centralized telemetry for permit analyzer engine.
    Tracks queries, errors, doctrine mutations, and performance metrics.
    """

    def __init__(self, audit_log_path: Path):
        self.audit_log_path = audit_log_path
        self.audit_log_path.parent.mkdir(parents=True, exist_ok=True)

        # In-memory trace storage (last 100 queries)
        self.recent_traces: List[QueryTrace] = []
        self._max_traces = 100

        # Metrics aggregation
        self.total_queries: int = 0
        self.doctrine_cache_hits: int = 0
        self.doctrine_cache_misses: int = 0
        self.errors_by_domain: Dict[ErrorDomain, int] = {}
        self.latencies: List[float] = []
        self._max_latencies = 1000

        # Doctrine mutation tracking
        self.mutation_log: List[Dict[str, Any]] = []

        logger.info(f"Telemetry initialized: {audit_log_path}")

    def start_trace(self, query_text: str, response_mode: str = "FAST") -> QueryTrace:
        """Begin a new query trace."""
        trace = QueryTrace(
            query_text=query_text,
            response_mode=response_mode
        )
        return trace

    def complete_trace(self, trace: QueryTrace):
        """Finalize trace, write to audit log, update metrics."""
        trace_data = trace.complete()

        # Write to JSONL audit log
        import json
        with open(self.audit_log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(trace_data) + "\n")

        # Update in-memory traces
        self.recent_traces.append(trace)
        if len(self.recent_traces) > self._max_traces:
            self.recent_traces.pop(0)

        # Update metrics
        self.total_queries += 1
        if trace.doctrine_cache_hit:
            self.doctrine_cache_hits += 1
        else:
            self.doctrine_cache_misses += 1

        if trace.error_domain:
            self.errors_by_domain[trace.error_domain] = \
                self.errors_by_domain.get(trace.error_domain, 0) + 1

        self.latencies.append(trace.total_latency_ms)
        if len(self.latencies) > self._max_latencies:
            self.latencies.pop(0)

        logger.info(
            f"Query complete: {trace.trace_id} | "
            f"{trace.total_latency_ms:.1f}ms | "
            f"Layer: {trace.response_layer.value if trace.response_layer else 'None'} | "
            f"Confidence: {trace.final_confidence:.2f}"
        )

    def log_error(
        self,
        trace_id: str,
        error_msg: str,
        error_domain: ErrorDomain,
        context: Optional[Dict[str, Any]] = None
    ):
        """Log structured error with domain classification."""
        import json
        error_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "trace_id": trace_id,
            "error_domain": error_domain.value,
            "error_msg": error_msg,
            "context": context or {}
        }

        with open(self.audit_log_path.parent / "errors.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(error_data) + "\n")

        logger.error(f"[{error_domain.value}] {error_msg} | Trace: {trace_id}")

    def record_doctrine_mutation(
        self,
        doctrine_topic: str,
        mutation_type: MutationType,
        mutation_origin: MutationOrigin,
        old_value: Any,
        new_value: Any,
        reasoning: str
    ):
        """Record doctrine cache mutations for audit trail."""
        mutation_record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "doctrine_topic": doctrine_topic,
            "mutation_type": mutation_type.value,
            "mutation_origin": mutation_origin.value,
            "old_value": str(old_value),
            "new_value": str(new_value),
            "reasoning": reasoning
        }

        self.mutation_log.append(mutation_record)

        import json
        with open(self.audit_log_path.parent / "doctrine_mutations.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(mutation_record) + "\n")

        logger.warning(
            f"Doctrine mutation: {doctrine_topic} | "
            f"{mutation_type.value} | Origin: {mutation_origin.value}"
        )

    def get_metrics_summary(self) -> Dict[str, Any]:
        """Return current performance metrics."""
        cache_hit_rate = (
            self.doctrine_cache_hits / self.total_queries
            if self.total_queries > 0 else 0.0
        )

        avg_latency = sum(self.latencies) / len(self.latencies) if self.latencies else 0.0
        p50 = sorted(self.latencies)[len(self.latencies) // 2] if self.latencies else 0.0
        p95 = sorted(self.latencies)[int(len(self.latencies) * 0.95)] if self.latencies else 0.0

        return {
            "total_queries": self.total_queries,
            "doctrine_cache_hit_rate": round(cache_hit_rate, 3),
            "doctrine_cache_hits": self.doctrine_cache_hits,
            "doctrine_cache_misses": self.doctrine_cache_misses,
            "avg_latency_ms": round(avg_latency, 2),
            "p50_latency_ms": round(p50, 2),
            "p95_latency_ms": round(p95, 2),
            "errors_by_domain": {k.value: v for k, v in self.errors_by_domain.items()},
            "total_errors": sum(self.errors_by_domain.values()),
            "recent_mutations": len(self.mutation_log)
        }


# ==============================================================================
# GLOBAL TELEMETRY INSTANCE
# ==============================================================================

_telemetry_instance: Optional[TelemetryManager] = None


def initialize_telemetry(audit_log_path: Path) -> TelemetryManager:
    """Initialize global telemetry manager."""
    global _telemetry_instance
    _telemetry_instance = TelemetryManager(audit_log_path)
    return _telemetry_instance


def get_telemetry() -> TelemetryManager:
    """Get global telemetry instance."""
    if _telemetry_instance is None:
        raise RuntimeError("Telemetry not initialized. Call initialize_telemetry() first.")
    return _telemetry_instance


# ==============================================================================
# CONVENIENCE FUNCTIONS
# ==============================================================================

def trace_query(query_text: str, response_mode: str = "FAST") -> QueryTrace:
    """Start a new query trace."""
    return get_telemetry().start_trace(query_text, response_mode)


def complete_trace(trace: QueryTrace):
    """Complete and persist a query trace."""
    get_telemetry().complete_trace(trace)


def log_error(
    trace_id: str,
    error_msg: str,
    error_domain: ErrorDomain,
    context: Optional[Dict[str, Any]] = None
):
    """Log structured error."""
    get_telemetry().log_error(trace_id, error_msg, error_domain, context)


def record_doctrine_mutation(
    doctrine_topic: str,
    mutation_type: MutationType,
    mutation_origin: MutationOrigin,
    old_value: Any,
    new_value: Any,
    reasoning: str
):
    """Record doctrine mutation."""
    get_telemetry().record_doctrine_mutation(
        doctrine_topic, mutation_type, mutation_origin,
        old_value, new_value, reasoning
    )
