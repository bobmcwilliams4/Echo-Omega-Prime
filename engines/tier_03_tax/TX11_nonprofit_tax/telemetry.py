"""
TX11 Nonprofit Tax — Telemetry and Observability
Query tracing, drift detection, coverage mapping, and metrics collection.

Author: ECHO OMEGA PRIME
Engine: TX11 Nonprofit Tax
"""

from dataclasses import dataclass, field as dc_field
from datetime import datetime, timezone
from typing import Dict, List, Optional, Set
from enum import Enum
from collections import defaultdict
import json
from pathlib import Path


# =============================================================================
# ENUMS
# =============================================================================

class ResponseLayer(str, Enum):
    """Which response layer was used."""
    DOCTRINE_CACHE = "doctrine_cache"
    SEMANTIC_RETRIEVAL = "semantic_retrieval"
    DEEP_ANALYSIS = "deep_analysis"


class ErrorDomain(str, Enum):
    """Error classification domains."""
    QUERY_EXECUTION = "query_execution"
    DOCTRINE_MATCHING = "doctrine_matching"
    SEMANTIC_NORMALIZATION = "semantic_normalization"
    CLOUD_RETRIEVAL = "cloud_retrieval"
    VALIDATION = "validation"
    FORMATTING = "formatting"


class MutationType(str, Enum):
    """Types of doctrine mutations."""
    CONCLUSION_SHIFT = "conclusion_shift"
    AUTHORITY_CHANGE = "authority_change"
    FACTOR_ADDITION = "factor_addition"
    CONFIDENCE_DOWNGRADE = "confidence_downgrade"


class MutationOrigin(str, Enum):
    """Source of doctrine mutation."""
    NEW_CASE_LAW = "new_case_law"
    IRS_GUIDANCE = "irs_guidance"
    REGULATORY_CHANGE = "regulatory_change"
    STATUTORY_AMENDMENT = "statutory_amendment"
    MANUAL_CORRECTION = "manual_correction"


# =============================================================================
# DATACLASSES
# =============================================================================

@dataclass
class QueryTrace:
    """Single query trace record."""
    trace_id: str
    query: str
    mode: str
    zone: str
    start_time: datetime
    end_time: Optional[datetime] = None
    response_layer: Optional[ResponseLayer] = None
    latency_ms: float = 0.0
    doctrines_triggered: List[str] = dc_field(default_factory=list)
    success: bool = True
    error_domain: Optional[ErrorDomain] = None
    error_message: Optional[str] = None


@dataclass
class DoctrineMutation:
    """Record of doctrine change over time."""
    doctrine_topic: str
    mutation_type: MutationType
    mutation_origin: MutationOrigin
    timestamp: datetime
    old_value: str
    new_value: str
    rationale: str


@dataclass
class CoverageRecord:
    """Doctrine coverage tracking."""
    doctrine_topic: str
    trigger_count: int = 0
    first_triggered: Optional[datetime] = None
    last_triggered: Optional[datetime] = None
    avg_latency_ms: float = 0.0


# =============================================================================
# TELEMETRY ENGINE
# =============================================================================

class TelemetryEngine:
    """Comprehensive telemetry system for TX11 engine."""

    def __init__(self, log_dir: Path):
        self.log_dir = log_dir
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # In-memory stores
        self.active_traces: Dict[str, QueryTrace] = {}
        self.completed_traces: List[QueryTrace] = []
        self.coverage_map: Dict[str, CoverageRecord] = defaultdict(
            lambda: CoverageRecord(doctrine_topic="")
        )
        self.mutations: List[DoctrineMutation] = []
        self.errors: List[QueryTrace] = []

        # Metrics
        self.total_queries: int = 0
        self.queries_by_layer: Dict[str, int] = defaultdict(int)
        self.queries_by_mode: Dict[str, int] = defaultdict(int)
        self.queries_by_zone: Dict[str, int] = defaultdict(int)
        self.total_latency_ms: float = 0.0

    def trace_query(self, trace_id: str, query: str, mode: str, zone: str):
        """Start a new query trace."""
        trace = QueryTrace(
            trace_id=trace_id,
            query=query,
            mode=mode,
            zone=zone,
            start_time=datetime.now(timezone.utc),
        )
        self.active_traces[trace_id] = trace
        self.total_queries += 1
        self.queries_by_mode[mode] += 1
        self.queries_by_zone[zone] += 1

    def complete_trace(
        self,
        trace_id: str,
        response_layer: ResponseLayer,
        latency_ms: float,
        success: bool = True,
        doctrines_triggered: Optional[List[str]] = None,
    ):
        """Complete an active query trace."""
        if trace_id not in self.active_traces:
            return

        trace = self.active_traces.pop(trace_id)
        trace.end_time = datetime.now(timezone.utc)
        trace.response_layer = response_layer
        trace.latency_ms = latency_ms
        trace.success = success
        if doctrines_triggered:
            trace.doctrines_triggered = doctrines_triggered

        self.completed_traces.append(trace)
        self.queries_by_layer[response_layer.value] += 1
        self.total_latency_ms += latency_ms

        # Update coverage map
        if doctrines_triggered:
            for topic in doctrines_triggered:
                record = self.coverage_map[topic]
                record.doctrine_topic = topic
                record.trigger_count += 1
                if record.first_triggered is None:
                    record.first_triggered = trace.start_time
                record.last_triggered = trace.end_time

                # Update average latency
                if record.trigger_count == 1:
                    record.avg_latency_ms = latency_ms
                else:
                    record.avg_latency_ms = (
                        record.avg_latency_ms * (record.trigger_count - 1) + latency_ms
                    ) / record.trigger_count

    def log_error(self, trace_id: str, error_domain: ErrorDomain, error_message: str):
        """Log an error for a query trace."""
        if trace_id in self.active_traces:
            trace = self.active_traces[trace_id]
            trace.success = False
            trace.error_domain = error_domain
            trace.error_message = error_message
            self.errors.append(trace)

    def record_mutation(
        self,
        doctrine_topic: str,
        mutation_type: MutationType,
        mutation_origin: MutationOrigin,
        old_value: str,
        new_value: str,
        rationale: str,
    ):
        """Record a doctrine mutation for drift detection."""
        mutation = DoctrineMutation(
            doctrine_topic=doctrine_topic,
            mutation_type=mutation_type,
            mutation_origin=mutation_origin,
            timestamp=datetime.now(timezone.utc),
            old_value=old_value,
            new_value=new_value,
            rationale=rationale,
        )
        self.mutations.append(mutation)

        # Write to drift log
        drift_log = self.log_dir / "doctrine_drift.jsonl"
        try:
            with drift_log.open("a", encoding="utf-8") as f:
                f.write(json.dumps({
                    "doctrine_topic": mutation.doctrine_topic,
                    "mutation_type": mutation.mutation_type.value,
                    "mutation_origin": mutation.mutation_origin.value,
                    "timestamp": mutation.timestamp.isoformat(),
                    "old_value": mutation.old_value,
                    "new_value": mutation.new_value,
                    "rationale": mutation.rationale,
                }) + "\n")
        except Exception:
            pass

    def get_coverage_stats(self) -> Dict[str, any]:
        """Get coverage statistics."""
        total_doctrines = len(self.coverage_map)
        triggered_doctrines = sum(1 for r in self.coverage_map.values() if r.trigger_count > 0)
        coverage_pct = (triggered_doctrines / total_doctrines * 100) if total_doctrines > 0 else 0.0

        untriggered = [topic for topic, record in self.coverage_map.items() if record.trigger_count == 0]
        top_triggered = sorted(
            self.coverage_map.items(),
            key=lambda x: x[1].trigger_count,
            reverse=True
        )[:10]

        return {
            "total_doctrines": total_doctrines,
            "triggered_doctrines": triggered_doctrines,
            "coverage_percentage": coverage_pct,
            "untriggered_topics": untriggered,
            "top_triggered": [
                {
                    "topic": topic,
                    "trigger_count": record.trigger_count,
                    "avg_latency_ms": record.avg_latency_ms,
                }
                for topic, record in top_triggered
            ],
        }

    def get_drift_summary(self) -> Dict[str, any]:
        """Get doctrine drift summary."""
        mutations_by_type = defaultdict(int)
        mutations_by_origin = defaultdict(int)

        for mutation in self.mutations:
            mutations_by_type[mutation.mutation_type.value] += 1
            mutations_by_origin[mutation.mutation_origin.value] += 1

        return {
            "total_mutations": len(self.mutations),
            "mutations_by_type": dict(mutations_by_type),
            "mutations_by_origin": dict(mutations_by_origin),
            "recent_mutations": [
                {
                    "doctrine_topic": m.doctrine_topic,
                    "mutation_type": m.mutation_type.value,
                    "timestamp": m.timestamp.isoformat(),
                    "rationale": m.rationale,
                }
                for m in self.mutations[-10:]
            ],
        }

    def get_error_summary(self) -> Dict[str, any]:
        """Get error summary."""
        errors_by_domain = defaultdict(int)
        for error in self.errors:
            if error.error_domain:
                errors_by_domain[error.error_domain.value] += 1

        error_rate = len(self.errors) / self.total_queries if self.total_queries > 0 else 0.0

        return {
            "total_errors": len(self.errors),
            "error_rate": error_rate,
            "errors_by_domain": dict(errors_by_domain),
            "recent_errors": [
                {
                    "trace_id": e.trace_id,
                    "error_domain": e.error_domain.value if e.error_domain else None,
                    "error_message": e.error_message,
                    "timestamp": e.start_time.isoformat(),
                }
                for e in self.errors[-10:]
            ],
        }

    def get_performance_metrics(self) -> Dict[str, any]:
        """Get performance metrics."""
        avg_latency = (
            self.total_latency_ms / len(self.completed_traces)
            if self.completed_traces else 0.0
        )

        latencies_by_layer = defaultdict(list)
        for trace in self.completed_traces:
            if trace.response_layer:
                latencies_by_layer[trace.response_layer.value].append(trace.latency_ms)

        avg_by_layer = {
            layer: sum(latencies) / len(latencies) if latencies else 0.0
            for layer, latencies in latencies_by_layer.items()
        }

        return {
            "total_queries": self.total_queries,
            "completed_queries": len(self.completed_traces),
            "avg_latency_ms": avg_latency,
            "queries_by_layer": dict(self.queries_by_layer),
            "queries_by_mode": dict(self.queries_by_mode),
            "queries_by_zone": dict(self.queries_by_zone),
            "avg_latency_by_layer": avg_by_layer,
        }

    def get_triggered_doctrines(self) -> List[str]:
        """Get list of triggered doctrine topics."""
        return [topic for topic, record in self.coverage_map.items() if record.trigger_count > 0]

    def get_top_doctrines(self, limit: int = 10) -> List[Dict[str, any]]:
        """Get top triggered doctrines."""
        top = sorted(
            self.coverage_map.items(),
            key=lambda x: x[1].trigger_count,
            reverse=True
        )[:limit]

        return [
            {
                "topic": topic,
                "trigger_count": record.trigger_count,
                "avg_latency_ms": record.avg_latency_ms,
                "first_triggered": record.first_triggered.isoformat() if record.first_triggered else None,
                "last_triggered": record.last_triggered.isoformat() if record.last_triggered else None,
            }
            for topic, record in top
        ]

    def get_avg_latency(self) -> float:
        """Get average query latency."""
        if not self.completed_traces:
            return 0.0
        return self.total_latency_ms / len(self.completed_traces)


# =============================================================================
# MODULE-LEVEL SINGLETON
# =============================================================================

_TELEMETRY: Optional[TelemetryEngine] = None


def get_telemetry() -> TelemetryEngine:
    """Get or create the singleton telemetry engine."""
    global _TELEMETRY
    if _TELEMETRY is None:
        from pathlib import Path
        log_dir = Path("O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/TX11_nonprofit_tax/logs")
        _TELEMETRY = TelemetryEngine(log_dir)
    return _TELEMETRY


def trace_query(trace_id: str, query: str, mode: str, zone: str):
    """Module-level trace query function."""
    telemetry = get_telemetry()
    telemetry.trace_query(trace_id, query, mode, zone)


def complete_trace(
    trace_id: str,
    response_layer: ResponseLayer,
    latency_ms: float,
    success: bool = True,
    doctrines_triggered: Optional[List[str]] = None,
):
    """Module-level complete trace function."""
    telemetry = get_telemetry()
    telemetry.complete_trace(trace_id, response_layer, latency_ms, success, doctrines_triggered)


def log_error(trace_id: str, error_domain: ErrorDomain, error_message: str):
    """Module-level log error function."""
    telemetry = get_telemetry()
    telemetry.log_error(trace_id, error_domain, error_message)


def record_doctrine_mutation(
    doctrine_topic: str,
    mutation_type: MutationType,
    mutation_origin: MutationOrigin,
    old_value: str,
    new_value: str,
    rationale: str,
):
    """Module-level record mutation function."""
    telemetry = get_telemetry()
    telemetry.record_mutation(doctrine_topic, mutation_type, mutation_origin, old_value, new_value, rationale)
