"""
LM04 Mineral Interest Tracker - Telemetry Module
=================================================

Query tracing, latency tracking, error domains, conflict detection tracking.

Provides TIE Components 8 (telemetry), 9 (drift watcher), 10 (coverage map),
and 11 (metrics collector) for the Mineral Interest Tracker.

Engine: LM04 | Version: 1.0.0
Commander: Bobby Don McWilliams II | Authority: 11.0 SOVEREIGN
"""

from __future__ import annotations

import json
import time
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from loguru import logger


# ═══════════════════════════════════════════════════════════════════
# QUERY PHASES
# ═══════════════════════════════════════════════════════════════════

class QueryPhase(str, Enum):
    """Phases of query execution for mineral interest tracking."""
    RECEIVED = "RECEIVED"
    VALIDATED = "VALIDATED"
    CLASSIFIED = "CLASSIFIED"
    DOCTRINE_LOOKUP = "DOCTRINE_LOOKUP"
    INTEREST_CALCULATION = "INTEREST_CALCULATION"
    CHAIN_ANALYSIS = "CHAIN_ANALYSIS"
    CONFLICT_DETECTION = "CONFLICT_DETECTION"
    CLOUD_RETRIEVAL = "CLOUD_RETRIEVAL"
    SYNTHESIS = "SYNTHESIS"
    COMPLETE = "COMPLETE"
    ERROR = "ERROR"


# ═══════════════════════════════════════════════════════════════════
# CONFLICT TYPES
# ═══════════════════════════════════════════════════════════════════

class ConflictType(str, Enum):
    """Types of conflicts detected in mineral interest tracking."""
    INTEREST_SUM_OVER = "interest_sum_over"
    INTEREST_SUM_UNDER = "interest_sum_under"
    TEMPORAL_OVERLAP = "temporal_overlap"
    DUPLICATE_CONVEYANCE = "duplicate_conveyance"
    CIRCULAR_CHAIN = "circular_chain"
    MISSING_GRANTOR = "missing_grantor"
    EXCEEDS_GRANTOR_INTEREST = "exceeds_grantor_interest"
    CONFLICTING_EXECUTIVE_RIGHTS = "conflicting_executive_rights"
    LIFE_ESTATE_REVERSION_GAP = "life_estate_reversion_gap"
    DORMANT_MINERAL_RISK = "dormant_mineral_risk"


# ═══════════════════════════════════════════════════════════════════
# INTEREST OPERATION TYPES
# ═══════════════════════════════════════════════════════════════════

class InterestOperation(str, Enum):
    """Types of interest operations tracked."""
    DECIMAL_CONVERSION = "decimal_conversion"
    FRACTIONAL_CALCULATION = "fractional_calculation"
    NET_ACRES_CALCULATION = "net_acres_calculation"
    WI_NRI_CONVERSION = "wi_nri_conversion"
    POOLED_ALLOCATION = "pooled_allocation"
    CARRIED_INTEREST_CALCULATION = "carried_interest_calculation"
    BACK_IN_CALCULATION = "back_in_calculation"
    FARMOUT_CALCULATION = "farmout_calculation"
    REVENUE_DISTRIBUTION = "revenue_distribution"
    INTEREST_RECONCILIATION = "interest_reconciliation"


# ═══════════════════════════════════════════════════════════════════
# QUERY TRACE
# ═══════════════════════════════════════════════════════════════════

@dataclass
class QueryTrace:
    """Full trace of a single mineral interest query execution."""
    trace_id: str
    query_text: str
    session_id: str
    response_mode: str
    start_time: float = field(default_factory=time.monotonic)
    phases: List[Dict[str, Any]] = field(default_factory=list)
    current_phase: QueryPhase = QueryPhase.RECEIVED
    interest_types_analyzed: List[str] = field(default_factory=list)
    doctrines_matched: List[str] = field(default_factory=list)
    cloud_sources: List[str] = field(default_factory=list)
    operations_performed: List[str] = field(default_factory=list)
    conflicts_detected: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    vector_fallback: bool = False
    cache_hit: bool = False
    interests_calculated: int = 0
    chains_analyzed: int = 0

    def enter_phase(self, phase: QueryPhase) -> None:
        """Enter a new query phase."""
        elapsed = (time.monotonic() - self.start_time) * 1000
        self.phases.append({
            "phase": phase.value,
            "entered_at_ms": round(elapsed, 2),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        self.current_phase = phase
        logger.debug(f"Query {self.trace_id[:8]} entered {phase.value} at {elapsed:.2f}ms")

    def record_error(self, error: str) -> None:
        """Record an error during query execution."""
        self.errors.append(error)
        self.enter_phase(QueryPhase.ERROR)
        logger.error(f"Query {self.trace_id[:8]} error: {error}")

    def record_conflict(self, conflict_type: ConflictType, details: str) -> None:
        """Record a conflict detected during analysis."""
        conflict_entry = f"{conflict_type.value}: {details}"
        self.conflicts_detected.append(conflict_entry)
        logger.warning(f"Query {self.trace_id[:8]} conflict: {conflict_entry}")

    def record_operation(self, operation: InterestOperation) -> None:
        """Record an interest operation performed."""
        self.operations_performed.append(operation.value)

    @property
    def total_latency_ms(self) -> float:
        """Total latency since query start."""
        return round((time.monotonic() - self.start_time) * 1000, 2)

    def to_dict(self) -> Dict[str, Any]:
        """Convert trace to dictionary for logging/export."""
        return {
            "trace_id": self.trace_id,
            "query": self.query_text[:200],
            "session_id": self.session_id,
            "mode": self.response_mode,
            "total_latency_ms": self.total_latency_ms,
            "phases": self.phases,
            "interest_types": self.interest_types_analyzed,
            "doctrines_matched": self.doctrines_matched,
            "cloud_sources": self.cloud_sources,
            "operations": self.operations_performed,
            "conflicts": self.conflicts_detected,
            "errors": self.errors,
            "vector_fallback": self.vector_fallback,
            "cache_hit": self.cache_hit,
            "interests_calculated": self.interests_calculated,
            "chains_analyzed": self.chains_analyzed,
        }


# ═══════════════════════════════════════════════════════════════════
# TIE COMPONENT 8: TELEMETRY COLLECTOR
# ═══════════════════════════════════════════════════════════════════

class TelemetryCollector:
    """Collects and aggregates mineral interest query performance telemetry."""

    def __init__(self, max_traces: int = 2000) -> None:
        self._traces: List[Dict[str, Any]] = []
        self._max_traces = max_traces
        self._total_queries = 0
        self._total_latency_ms = 0.0
        self._error_count = 0
        self._cache_hits = 0
        self._vector_fallbacks = 0
        self._interest_type_counter: Counter = Counter()
        self._operation_counter: Counter = Counter()
        self._doctrine_counter: Counter = Counter()
        self._conflict_counter: Counter = Counter()
        self._hourly_counts: Dict[str, int] = defaultdict(int)
        self._total_interests_calculated = 0
        self._total_chains_analyzed = 0
        self._total_conflicts_detected = 0

    def record_trace(self, trace: QueryTrace) -> None:
        """Record a completed query trace."""
        trace_dict = trace.to_dict()
        self._traces.append(trace_dict)
        if len(self._traces) > self._max_traces:
            self._traces = self._traces[-self._max_traces // 2:]

        self._total_queries += 1
        self._total_latency_ms += trace.total_latency_ms
        if trace.errors:
            self._error_count += 1
        if trace.cache_hit:
            self._cache_hits += 1
        if trace.vector_fallback:
            self._vector_fallbacks += 1

        for int_type in trace.interest_types_analyzed:
            self._interest_type_counter[int_type] += 1
        for op in trace.operations_performed:
            self._operation_counter[op] += 1
        for doc in trace.doctrines_matched:
            self._doctrine_counter[doc] += 1
        for conflict in trace.conflicts_detected:
            conflict_type = conflict.split(":")[0]
            self._conflict_counter[conflict_type] += 1

        self._total_interests_calculated += trace.interests_calculated
        self._total_chains_analyzed += trace.chains_analyzed
        self._total_conflicts_detected += len(trace.conflicts_detected)

        hour_key = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H")
        self._hourly_counts[hour_key] += 1

        logger.info(f"Recorded trace {trace.trace_id[:8]}: {trace.total_latency_ms}ms, "
                   f"{len(trace.conflicts_detected)} conflicts")

    def start_query(self, query_text: str, session_id: str, response_mode: str, trace_id: str) -> QueryTrace:
        """Start a new query trace."""
        return QueryTrace(
            trace_id=trace_id,
            query_text=query_text,
            session_id=session_id,
            response_mode=response_mode,
        )

    def summary(self) -> Dict[str, Any]:
        """Generate telemetry summary."""
        avg_latency = round(self._total_latency_ms / max(self._total_queries, 1), 2)
        return {
            "total_queries": self._total_queries,
            "avg_latency_ms": avg_latency,
            "error_count": self._error_count,
            "error_rate": round(self._error_count / max(self._total_queries, 1), 4),
            "cache_hit_rate": round(self._cache_hits / max(self._total_queries, 1), 4),
            "vector_fallback_rate": round(self._vector_fallbacks / max(self._total_queries, 1), 4),
            "total_interests_calculated": self._total_interests_calculated,
            "total_chains_analyzed": self._total_chains_analyzed,
            "total_conflicts_detected": self._total_conflicts_detected,
            "avg_interests_per_query": round(self._total_interests_calculated / max(self._total_queries, 1), 2),
            "avg_conflicts_per_query": round(self._total_conflicts_detected / max(self._total_queries, 1), 2),
            "top_interest_types": self._interest_type_counter.most_common(10),
            "top_operations": self._operation_counter.most_common(10),
            "top_doctrines": self._doctrine_counter.most_common(10),
            "top_conflicts": self._conflict_counter.most_common(10),
            "recent_traces": len(self._traces),
        }

    def recent_traces(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent query traces."""
        return self._traces[-limit:]

    def hourly_throughput(self) -> Dict[str, int]:
        """Get hourly query counts."""
        return dict(sorted(self._hourly_counts.items())[-24:])

    def conflict_report(self) -> Dict[str, Any]:
        """Generate conflict detection report."""
        return {
            "total_conflicts": self._total_conflicts_detected,
            "queries_with_conflicts": sum(1 for t in self._traces if t.get("conflicts")),
            "conflict_rate": round(
                sum(1 for t in self._traces if t.get("conflicts")) / max(len(self._traces), 1), 4
            ),
            "conflict_breakdown": dict(self._conflict_counter.most_common()),
            "recent_conflicts": [
                {"trace_id": t["trace_id"], "conflicts": t["conflicts"]}
                for t in self._traces[-20:]
                if t.get("conflicts")
            ],
        }


# ═══════════════════════════════════════════════════════════════════
# TIE COMPONENT 9: DRIFT WATCHER
# ═══════════════════════════════════════════════════════════════════

class DriftWatcher:
    """Detects doctrine drift — when query patterns diverge from doctrine coverage."""

    def __init__(self) -> None:
        self._unmatched_queries: List[Dict[str, Any]] = []
        self._drift_alerts: List[Dict[str, Any]] = []
        self._interest_type_gaps: Counter = Counter()

    def record_unmatched(self, query: str, interest_types: List[str]) -> None:
        """Record a query that didn't match any doctrines."""
        self._unmatched_queries.append({
            "query": query[:200],
            "interest_types": interest_types,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        if len(self._unmatched_queries) > 500:
            self._unmatched_queries = self._unmatched_queries[-250:]

        for int_type in interest_types:
            self._interest_type_gaps[int_type] += 1

        # Alert if too many unmatched queries
        if len(self._unmatched_queries) % 50 == 0:
            self._drift_alerts.append({
                "alert": f"Doctrine coverage gap: {len(self._unmatched_queries)} unmatched queries",
                "top_unmatched_interest_types": self._interest_type_gaps.most_common(5),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            logger.warning(f"Drift alert: {len(self._unmatched_queries)} unmatched queries")

    def get_drift_report(self) -> Dict[str, Any]:
        """Generate drift detection report."""
        return {
            "unmatched_count": len(self._unmatched_queries),
            "recent_unmatched": self._unmatched_queries[-10:],
            "interest_type_gaps": dict(self._interest_type_gaps.most_common()),
            "alerts": self._drift_alerts[-5:],
        }


# ═══════════════════════════════════════════════════════════════════
# TIE COMPONENT 10: COVERAGE MAP
# ═══════════════════════════════════════════════════════════════════

class CoverageMap:
    """Tracks which doctrines have been triggered and identifies gaps."""

    def __init__(self, all_topics: Set[str]) -> None:
        self._all_topics = all_topics
        self._triggered: Set[str] = set()
        self._trigger_counts: Counter = Counter()

    def record_trigger(self, topic: str) -> None:
        """Record a doctrine trigger."""
        self._triggered.add(topic)
        self._trigger_counts[topic] += 1

    def get_coverage(self) -> Dict[str, Any]:
        """Generate coverage report."""
        untriggered = self._all_topics - self._triggered
        return {
            "total_doctrines": len(self._all_topics),
            "triggered": len(self._triggered),
            "untriggered": len(untriggered),
            "coverage_pct": round(len(self._triggered) / max(len(self._all_topics), 1) * 100, 1),
            "untriggered_topics": sorted(untriggered),
            "most_triggered": self._trigger_counts.most_common(10),
            "least_triggered": self._trigger_counts.most_common()[-10:] if self._trigger_counts else [],
        }


# ═══════════════════════════════════════════════════════════════════
# TIE COMPONENT 11: METRICS COLLECTOR
# ═══════════════════════════════════════════════════════════════════

class MetricsCollector:
    """Collects detailed performance metrics for mineral interest operations."""

    def __init__(self) -> None:
        self._operation_latencies: Dict[str, List[float]] = defaultdict(list)
        self._interest_type_latencies: Dict[str, List[float]] = defaultdict(list)
        self._conflict_detection_latencies: List[float] = []
        self._chain_analysis_latencies: List[float] = []
        self._calculation_errors: Counter = Counter()

    def record_operation_latency(self, operation: InterestOperation, latency_ms: float) -> None:
        """Record latency for a specific operation."""
        self._operation_latencies[operation.value].append(latency_ms)

    def record_interest_type_latency(self, interest_type: str, latency_ms: float) -> None:
        """Record latency for analyzing a specific interest type."""
        self._interest_type_latencies[interest_type].append(latency_ms)

    def record_conflict_detection_latency(self, latency_ms: float) -> None:
        """Record latency for conflict detection."""
        self._conflict_detection_latencies.append(latency_ms)

    def record_chain_analysis_latency(self, latency_ms: float) -> None:
        """Record latency for chain analysis."""
        self._chain_analysis_latencies.append(latency_ms)

    def record_calculation_error(self, error_type: str) -> None:
        """Record a calculation error."""
        self._calculation_errors[error_type] += 1

    def get_metrics(self) -> Dict[str, Any]:
        """Generate metrics report."""
        def avg(values: List[float]) -> float:
            return round(sum(values) / len(values), 2) if values else 0.0

        return {
            "operation_avg_latencies": {
                op: avg(lats) for op, lats in self._operation_latencies.items()
            },
            "interest_type_avg_latencies": {
                it: avg(lats) for it, lats in self._interest_type_latencies.items()
            },
            "conflict_detection_avg_ms": avg(self._conflict_detection_latencies),
            "chain_analysis_avg_ms": avg(self._chain_analysis_latencies),
            "calculation_errors": dict(self._calculation_errors),
            "total_operations": sum(len(lats) for lats in self._operation_latencies.values()),
            "total_conflicts_checked": len(self._conflict_detection_latencies),
            "total_chains_analyzed": len(self._chain_analysis_latencies),
        }


# ═══════════════════════════════════════════════════════════════════
# AUDIT TRAIL
# ═══════════════════════════════════════════════════════════════════

class AuditTrail:
    """JSONL audit trail for all mineral interest operations."""

    def __init__(self, audit_path: Optional[Path] = None) -> None:
        self._audit_path = audit_path or Path("lm04_audit_trail.jsonl")
        self._ensure_audit_file()

    def _ensure_audit_file(self) -> None:
        """Ensure audit file exists."""
        if not self._audit_path.exists():
            self._audit_path.touch()
            logger.info(f"Created audit trail: {self._audit_path}")

    def log_event(self, event_type: str, details: Dict[str, Any]) -> None:
        """Log an audit event."""
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "details": details,
        }
        with self._audit_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event) + "\n")

    def log_query(self, trace: QueryTrace) -> None:
        """Log a completed query."""
        self.log_event("QUERY", trace.to_dict())

    def log_conflict(self, conflict_type: ConflictType, details: Dict[str, Any]) -> None:
        """Log a detected conflict."""
        self.log_event(f"CONFLICT_{conflict_type.value.upper()}", details)

    def log_calculation(self, operation: InterestOperation, details: Dict[str, Any]) -> None:
        """Log an interest calculation."""
        self.log_event(f"CALCULATION_{operation.value.upper()}", details)


logger.info("LM04 telemetry module loaded")
