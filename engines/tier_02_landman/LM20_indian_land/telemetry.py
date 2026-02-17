"""
LM20 Indian Land Engine — Telemetry Module
Comprehensive query tracing, error logging, metrics collection, and audit trail.

Tracks:
- Query latency by layer (cache, semantic, deep)
- Doctrine hit/miss rates
- Error domains and frequencies
- Coverage gaps (queries with no good doctrine match)
- Doctrine mutations (when expert reasoning changes)

Author: ECHO OMEGA PRIME
Engine: LM20
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
import time
import json
from loguru import logger


# ==============================================================================
# ENUMS
# ==============================================================================

class ResponseLayer(str, Enum):
    """Which layer of TIE architecture handled the query."""
    DOCTRINE_CACHE = "doctrine_cache"
    SEMANTIC_RETRIEVAL = "semantic_retrieval"
    DEEP_ANALYSIS = "deep_analysis"
    CLOUD_KNOWLEDGE = "cloud_knowledge"
    FALLBACK = "fallback"


class ErrorDomain(str, Enum):
    """Error classification domains."""
    TRUST_STATUS = "trust_status"
    BIA_APPROVAL = "bia_approval"
    FRACTIONATION = "fractionation"
    SOVEREIGNTY = "sovereignty"
    ENVIRONMENTAL = "environmental"
    ROYALTY = "royalty"
    JURISDICTION = "jurisdiction"
    LEASING = "leasing"
    TITLE = "title"
    RIGHT_OF_WAY = "right_of_way"
    UNKNOWN = "unknown"


class MutationType(str, Enum):
    """Types of doctrine mutations."""
    AUTHORITY_CHANGE = "authority_change"
    CONCLUSION_REVISION = "conclusion_revision"
    NEW_PRECEDENT = "new_precedent"
    REGULATORY_UPDATE = "regulatory_update"
    CONFIDENCE_ADJUSTMENT = "confidence_adjustment"


class MutationOrigin(str, Enum):
    """Source of doctrine mutation."""
    CASE_LAW = "case_law"
    REGULATION = "regulation"
    STATUTE = "statute"
    BIA_GUIDANCE = "bia_guidance"
    SOLICITOR_OPINION = "solicitor_opinion"
    TRIBAL_CODE = "tribal_code"
    EXPERT_REVIEW = "expert_review"


# ==============================================================================
# DATACLASSES
# ==============================================================================

@dataclass
class QueryTrace:
    """Single query execution trace."""
    trace_id: str
    query: str
    response_layer: ResponseLayer
    latency_ms: float
    doctrines_considered: int
    doctrines_triggered: List[str]
    confidence_score: float
    issue_category: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    error: Optional[str] = None
    cache_hit: bool = False


@dataclass
class ErrorLog:
    """Error event log entry."""
    error_id: str
    error_domain: ErrorDomain
    error_message: str
    query_context: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    stack_trace: Optional[str] = None
    resolved: bool = False


@dataclass
class DoctrineMutation:
    """Doctrine change record."""
    mutation_id: str
    doctrine_topic: str
    mutation_type: MutationType
    mutation_origin: MutationOrigin
    old_value: str
    new_value: str
    authority_citation: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    reviewer: str = "LM20_engine"


@dataclass
class PerformanceMetrics:
    """Aggregated performance metrics."""
    total_queries: int = 0
    cache_hit_rate: float = 0.0
    avg_latency_ms: float = 0.0
    p50_latency_ms: float = 0.0
    p95_latency_ms: float = 0.0
    p99_latency_ms: float = 0.0
    error_rate: float = 0.0
    queries_per_hour: float = 0.0


@dataclass
class CoverageStats:
    """Doctrine coverage statistics."""
    total_doctrines: int = 0
    triggered_doctrines: Dict[str, int] = field(default_factory=dict)
    untriggered_doctrines: List[str] = field(default_factory=list)
    coverage_percentage: float = 0.0
    epistemic_gaps: List[str] = field(default_factory=list)


# ==============================================================================
# TELEMETRY ENGINE
# ==============================================================================

class TelemetryEngine:
    """
    Comprehensive telemetry system for LM20 engine.

    Responsibilities:
    - Trace all queries with latency breakdown
    - Log all errors with context
    - Track doctrine usage and coverage
    - Detect epistemic gaps (queries with no good answer)
    - Record doctrine mutations
    - Generate performance metrics
    """

    def __init__(self, log_dir: Path):
        """Initialize telemetry engine."""
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.audit_log = self.log_dir / "audit_trail.jsonl"
        self.error_log_file = self.log_dir / "errors.jsonl"
        self.mutation_log = self.log_dir / "doctrine_mutations.jsonl"
        self.metrics_log = self.log_dir / "metrics.jsonl"

        self.query_traces: List[QueryTrace] = []
        self.error_logs: List[ErrorLog] = []
        self.doctrine_mutations: List[DoctrineMutation] = []
        self.latencies: List[float] = []

        self.start_time = time.time()
        logger.info(f"TelemetryEngine initialized, logging to {self.log_dir}")

    def trace_query(
        self,
        trace_id: str,
        query: str,
        response_layer: ResponseLayer,
        latency_ms: float,
        doctrines_considered: int,
        doctrines_triggered: List[str],
        confidence_score: float,
        issue_category: str,
        cache_hit: bool = False,
        error: Optional[str] = None
    ):
        """Record query trace."""
        trace = QueryTrace(
            trace_id=trace_id,
            query=query,
            response_layer=response_layer,
            latency_ms=latency_ms,
            doctrines_considered=doctrines_considered,
            doctrines_triggered=doctrines_triggered,
            confidence_score=confidence_score,
            issue_category=issue_category,
            cache_hit=cache_hit,
            error=error
        )

        self.query_traces.append(trace)
        self.latencies.append(latency_ms)

        # Write to audit log
        with open(self.audit_log, 'a', encoding='utf-8') as f:
            f.write(json.dumps({
                "trace_id": trace_id,
                "query": query,
                "response_layer": response_layer.value,
                "latency_ms": latency_ms,
                "doctrines_considered": doctrines_considered,
                "doctrines_triggered": doctrines_triggered,
                "confidence_score": confidence_score,
                "issue_category": issue_category,
                "cache_hit": cache_hit,
                "error": error,
                "timestamp": trace.timestamp
            }) + '\n')

        logger.debug(f"Query trace recorded: {trace_id}, layer={response_layer.value}, latency={latency_ms:.2f}ms")

    def log_error(
        self,
        error_id: str,
        error_domain: ErrorDomain,
        error_message: str,
        query_context: str,
        stack_trace: Optional[str] = None
    ):
        """Log error event."""
        error_log = ErrorLog(
            error_id=error_id,
            error_domain=error_domain,
            error_message=error_message,
            query_context=query_context,
            stack_trace=stack_trace
        )

        self.error_logs.append(error_log)

        # Write to error log file
        with open(self.error_log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps({
                "error_id": error_id,
                "error_domain": error_domain.value,
                "error_message": error_message,
                "query_context": query_context,
                "stack_trace": stack_trace,
                "timestamp": error_log.timestamp
            }) + '\n')

        logger.error(f"Error logged: {error_id}, domain={error_domain.value}, msg={error_message}")

    def record_doctrine_mutation(
        self,
        mutation_id: str,
        doctrine_topic: str,
        mutation_type: MutationType,
        mutation_origin: MutationOrigin,
        old_value: str,
        new_value: str,
        authority_citation: str
    ):
        """Record doctrine mutation event."""
        mutation = DoctrineMutation(
            mutation_id=mutation_id,
            doctrine_topic=doctrine_topic,
            mutation_type=mutation_type,
            mutation_origin=mutation_origin,
            old_value=old_value,
            new_value=new_value,
            authority_citation=authority_citation
        )

        self.doctrine_mutations.append(mutation)

        # Write to mutation log
        with open(self.mutation_log, 'a', encoding='utf-8') as f:
            f.write(json.dumps({
                "mutation_id": mutation_id,
                "doctrine_topic": doctrine_topic,
                "mutation_type": mutation_type.value,
                "mutation_origin": mutation_origin.value,
                "old_value": old_value,
                "new_value": new_value,
                "authority_citation": authority_citation,
                "timestamp": mutation.timestamp
            }) + '\n')

        logger.warning(f"Doctrine mutation recorded: {mutation_id}, topic={doctrine_topic}, type={mutation_type.value}")

    def get_performance_metrics(self) -> PerformanceMetrics:
        """Calculate and return performance metrics."""
        total_queries = len(self.query_traces)
        if total_queries == 0:
            return PerformanceMetrics()

        cache_hits = sum(1 for t in self.query_traces if t.cache_hit)
        errors = sum(1 for t in self.query_traces if t.error is not None)

        sorted_latencies = sorted(self.latencies)
        p50_idx = int(len(sorted_latencies) * 0.50)
        p95_idx = int(len(sorted_latencies) * 0.95)
        p99_idx = int(len(sorted_latencies) * 0.99)

        elapsed_hours = (time.time() - self.start_time) / 3600

        metrics = PerformanceMetrics(
            total_queries=total_queries,
            cache_hit_rate=cache_hits / total_queries if total_queries > 0 else 0.0,
            avg_latency_ms=sum(self.latencies) / len(self.latencies) if self.latencies else 0.0,
            p50_latency_ms=sorted_latencies[p50_idx] if sorted_latencies else 0.0,
            p95_latency_ms=sorted_latencies[p95_idx] if sorted_latencies else 0.0,
            p99_latency_ms=sorted_latencies[p99_idx] if sorted_latencies else 0.0,
            error_rate=errors / total_queries if total_queries > 0 else 0.0,
            queries_per_hour=total_queries / elapsed_hours if elapsed_hours > 0 else 0.0
        )

        # Write metrics snapshot
        with open(self.metrics_log, 'a', encoding='utf-8') as f:
            f.write(json.dumps({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "total_queries": metrics.total_queries,
                "cache_hit_rate": metrics.cache_hit_rate,
                "avg_latency_ms": metrics.avg_latency_ms,
                "p95_latency_ms": metrics.p95_latency_ms,
                "error_rate": metrics.error_rate,
                "queries_per_hour": metrics.queries_per_hour
            }) + '\n')

        return metrics

    def get_coverage_stats(self, all_doctrine_topics: List[str]) -> CoverageStats:
        """Calculate doctrine coverage statistics."""
        triggered = {}
        for trace in self.query_traces:
            for topic in trace.doctrines_triggered:
                triggered[topic] = triggered.get(topic, 0) + 1

        untriggered = [topic for topic in all_doctrine_topics if topic not in triggered]

        coverage_pct = (len(triggered) / len(all_doctrine_topics)) * 100 if all_doctrine_topics else 0.0

        # Identify epistemic gaps: queries with low confidence or no doctrine match
        epistemic_gaps = []
        for trace in self.query_traces:
            if trace.confidence_score < 0.5 or len(trace.doctrines_triggered) == 0:
                epistemic_gaps.append(trace.query)

        return CoverageStats(
            total_doctrines=len(all_doctrine_topics),
            triggered_doctrines=triggered,
            untriggered_doctrines=untriggered,
            coverage_percentage=coverage_pct,
            epistemic_gaps=epistemic_gaps[:20]  # top 20
        )

    def get_error_summary(self) -> Dict[str, int]:
        """Get error counts by domain."""
        summary = {}
        for error in self.error_logs:
            domain = error.error_domain.value
            summary[domain] = summary.get(domain, 0) + 1
        return summary


# ==============================================================================
# MODULE-LEVEL TELEMETRY INSTANCE
# ==============================================================================

_telemetry: Optional[TelemetryEngine] = None


def get_telemetry() -> Optional[TelemetryEngine]:
    """Get module-level telemetry instance."""
    return _telemetry


def initialize_telemetry(log_dir: Path):
    """Initialize module-level telemetry."""
    global _telemetry
    _telemetry = TelemetryEngine(log_dir)
    logger.info("Module-level telemetry initialized")


def trace_query(
    trace_id: str,
    query: str,
    response_layer: ResponseLayer,
    latency_ms: float,
    doctrines_considered: int,
    doctrines_triggered: List[str],
    confidence_score: float,
    issue_category: str,
    cache_hit: bool = False,
    error: Optional[str] = None
):
    """Trace query via module-level telemetry."""
    if _telemetry:
        _telemetry.trace_query(
            trace_id, query, response_layer, latency_ms,
            doctrines_considered, doctrines_triggered,
            confidence_score, issue_category, cache_hit, error
        )


def complete_trace(trace_id: str):
    """Mark trace as complete (no-op for now, can extend)."""
    logger.debug(f"Trace {trace_id} complete")


def log_error(
    error_id: str,
    error_domain: ErrorDomain,
    error_message: str,
    query_context: str,
    stack_trace: Optional[str] = None
):
    """Log error via module-level telemetry."""
    if _telemetry:
        _telemetry.log_error(error_id, error_domain, error_message, query_context, stack_trace)


def record_doctrine_mutation(
    mutation_id: str,
    doctrine_topic: str,
    mutation_type: MutationType,
    mutation_origin: MutationOrigin,
    old_value: str,
    new_value: str,
    authority_citation: str
):
    """Record doctrine mutation via module-level telemetry."""
    if _telemetry:
        _telemetry.record_doctrine_mutation(
            mutation_id, doctrine_topic, mutation_type, mutation_origin,
            old_value, new_value, authority_citation
        )
