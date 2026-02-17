"""
R05 TELEMETRY MODULE

Comprehensive query tracing, performance monitoring, and error tracking.
Full audit trail for regulatory compliance analysis.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
import uuid
import time
from loguru import logger


class ErrorDomain(str, Enum):
    """Error classification domains."""
    QUERY_PROCESSING = "query_processing"
    DOCTRINE_MATCHING = "doctrine_matching"
    VECTOR_SEARCH = "vector_search"
    RESPONSE_GENERATION = "response_generation"
    VALIDATION = "validation"
    EXTERNAL_API = "external_api"
    DATABASE = "database"
    UNKNOWN = "unknown"


class ResponseLayer(str, Enum):
    """Response generation layers."""
    DOCTRINE_CACHE = "doctrine"
    VECTOR_RETRIEVAL = "retrieval"
    DEEP_ANALYSIS = "deep_analysis"


class MutationType(str, Enum):
    """Types of doctrine mutations."""
    ADDITION = "addition"
    MODIFICATION = "modification"
    DEPRECATION = "deprecation"
    AUTHORITY_CHANGE = "authority_change"


class MutationOrigin(str, Enum):
    """Origin of doctrine mutation."""
    REGULATORY_UPDATE = "regulatory_update"
    COURT_DECISION = "court_decision"
    ERROR_CORRECTION = "error_correction"
    REFINEMENT = "refinement"


@dataclass
class QueryTrace:
    """Complete trace of a single query execution."""
    trace_id: str
    start_time: float
    end_time: Optional[float] = None
    query_text: str = ""
    normalized_text: str = ""
    keywords: List[str] = field(default_factory=list)
    response_layer: Optional[ResponseLayer] = None
    doctrine_matches: List[str] = field(default_factory=list)
    vector_results_count: int = 0
    errors: List[Dict[str, Any]] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def latency_ms(self) -> float:
        """Calculate query latency in milliseconds."""
        if self.end_time is None:
            return (time.time() - self.start_time) * 1000
        return (self.end_time - self.start_time) * 1000

    def to_dict(self) -> Dict[str, Any]:
        """Serialize trace to dictionary."""
        return {
            "trace_id": self.trace_id,
            "start_time": datetime.fromtimestamp(self.start_time, tz=timezone.utc).isoformat(),
            "end_time": datetime.fromtimestamp(self.end_time, tz=timezone.utc).isoformat() if self.end_time else None,
            "latency_ms": round(self.latency_ms, 2),
            "query_text": self.query_text,
            "normalized_text": self.normalized_text,
            "keywords": self.keywords,
            "response_layer": self.response_layer.value if self.response_layer else None,
            "doctrine_matches": self.doctrine_matches,
            "vector_results_count": self.vector_results_count,
            "errors": self.errors,
            "warnings": self.warnings,
            "metadata": self.metadata
        }


@dataclass
class DoctrineMutation:
    """Record of a doctrine change over time."""
    mutation_id: str
    timestamp: datetime
    doctrine_topic: str
    mutation_type: MutationType
    origin: MutationOrigin
    description: str
    authority_before: Optional[str] = None
    authority_after: Optional[str] = None
    confidence_before: Optional[float] = None
    confidence_after: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class TelemetryCollector:
    """Central telemetry collector for R05 engine."""

    def __init__(self):
        self.active_traces: Dict[str, QueryTrace] = {}
        self.completed_traces: List[QueryTrace] = []
        self.mutations: List[DoctrineMutation] = []
        self._max_completed = 1000  # Keep last 1000 completed traces in memory

    def start_trace(self, query_text: str) -> str:
        """Start a new query trace."""
        trace_id = str(uuid.uuid4())
        trace = QueryTrace(
            trace_id=trace_id,
            start_time=time.time(),
            query_text=query_text
        )
        self.active_traces[trace_id] = trace
        logger.info(f"[{trace_id}] Trace started")
        return trace_id

    def update_trace(
        self,
        trace_id: str,
        normalized_text: Optional[str] = None,
        keywords: Optional[List[str]] = None,
        response_layer: Optional[ResponseLayer] = None,
        doctrine_matches: Optional[List[str]] = None,
        vector_results_count: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Update trace with processing details."""
        if trace_id not in self.active_traces:
            logger.warning(f"[{trace_id}] Trace not found for update")
            return

        trace = self.active_traces[trace_id]

        if normalized_text is not None:
            trace.normalized_text = normalized_text
        if keywords is not None:
            trace.keywords = keywords
        if response_layer is not None:
            trace.response_layer = response_layer
        if doctrine_matches is not None:
            trace.doctrine_matches = doctrine_matches
        if vector_results_count is not None:
            trace.vector_results_count = vector_results_count
        if metadata is not None:
            trace.metadata.update(metadata)

    def add_error(self, trace_id: str, domain: ErrorDomain, message: str, details: Optional[Dict[str, Any]] = None):
        """Add error to trace."""
        if trace_id not in self.active_traces:
            logger.warning(f"[{trace_id}] Trace not found for error")
            return

        error_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "domain": domain.value,
            "message": message,
            "details": details or {}
        }

        self.active_traces[trace_id].errors.append(error_entry)
        logger.error(f"[{trace_id}] {domain.value}: {message}")

    def add_warning(self, trace_id: str, warning: str):
        """Add warning to trace."""
        if trace_id not in self.active_traces:
            return

        self.active_traces[trace_id].warnings.append(warning)
        logger.warning(f"[{trace_id}] {warning}")

    def complete_trace(self, trace_id: str) -> Optional[QueryTrace]:
        """Complete a trace and move to completed list."""
        if trace_id not in self.active_traces:
            logger.warning(f"[{trace_id}] Trace not found for completion")
            return None

        trace = self.active_traces.pop(trace_id)
        trace.end_time = time.time()

        self.completed_traces.append(trace)

        # Prune old completed traces
        if len(self.completed_traces) > self._max_completed:
            self.completed_traces = self.completed_traces[-self._max_completed:]

        logger.info(f"[{trace_id}] Trace completed: {trace.latency_ms:.2f}ms")

        return trace

    def record_mutation(
        self,
        doctrine_topic: str,
        mutation_type: MutationType,
        origin: MutationOrigin,
        description: str,
        **kwargs
    ):
        """Record a doctrine mutation."""
        mutation = DoctrineMutation(
            mutation_id=str(uuid.uuid4()),
            timestamp=datetime.now(timezone.utc),
            doctrine_topic=doctrine_topic,
            mutation_type=mutation_type,
            origin=origin,
            description=description,
            **kwargs
        )

        self.mutations.append(mutation)
        logger.info(f"Mutation recorded: {doctrine_topic} - {mutation_type.value}")

    def get_trace_summary(self) -> Dict[str, Any]:
        """Get summary statistics of all traces."""
        if not self.completed_traces:
            return {
                "total_traces": 0,
                "avg_latency_ms": 0.0,
                "error_rate": 0.0
            }

        latencies = [t.latency_ms for t in self.completed_traces]
        errors = [t for t in self.completed_traces if t.errors]

        return {
            "total_traces": len(self.completed_traces),
            "active_traces": len(self.active_traces),
            "avg_latency_ms": round(sum(latencies) / len(latencies), 2),
            "min_latency_ms": round(min(latencies), 2),
            "max_latency_ms": round(max(latencies), 2),
            "error_count": len(errors),
            "error_rate": round(len(errors) / len(self.completed_traces), 3),
            "mutations_recorded": len(self.mutations)
        }


# Global telemetry instance
_telemetry = TelemetryCollector()


def get_telemetry() -> TelemetryCollector:
    """Get global telemetry instance."""
    return _telemetry


def trace_query(query_text: str) -> str:
    """Start tracing a query."""
    return _telemetry.start_trace(query_text)


def update_trace(trace_id: str, **kwargs):
    """Update trace with processing details."""
    _telemetry.update_trace(trace_id, **kwargs)


def complete_trace(trace_id: str) -> Optional[QueryTrace]:
    """Complete a trace."""
    return _telemetry.complete_trace(trace_id)


def log_error(trace_id: str, domain: ErrorDomain, message: str, details: Optional[Dict[str, Any]] = None):
    """Log error to trace."""
    _telemetry.add_error(trace_id, domain, message, details)


def record_doctrine_mutation(
    doctrine_topic: str,
    mutation_type: MutationType,
    origin: MutationOrigin,
    description: str,
    **kwargs
):
    """Record a doctrine mutation."""
    _telemetry.record_mutation(doctrine_topic, mutation_type, origin, description, **kwargs)
