"""
LG18 Legislative Analysis Engine - Telemetry Module
======================================================
Production telemetry, metrics collection, audit trail, and observability
for the Legislative Analysis Engine.

Components:
    - TelemetryCollector: Ring-buffer based metric collection
    - QueryTrace: Per-query trace with timing breakdowns
    - AuditTrail: Append-only JSONL audit log with SHA-256 chain
    - MetricsAggregator: Rolling window aggregation for dashboards
    - ErrorTracker: Domain-classified error tracking and alerting
    - DoctrineMutationLog: Track changes to doctrine cache
    - LegislativeMetrics: Legislative-specific counters

Port: 8408
Engine: LG18 Legislative Analysis
Version: 2.0.0
"""

from __future__ import annotations

import hashlib
import json
import math
import threading
import time
import uuid
from collections import Counter, defaultdict, deque
from dataclasses import dataclass, field as dc_field
from datetime import datetime, timezone
from enum import Enum, auto
from pathlib import Path
from typing import Any, ClassVar, Dict, List, Optional, Tuple

from loguru import logger


# ============================================================================
# ENUMS
# ============================================================================

class ResponseLayer(Enum):
    """Which processing layer produced the response."""
    DOCTRINE_CACHE = "doctrine_cache"
    SEMANTIC_SEARCH = "semantic_search"
    LEGISLATIVE_ANALYSIS = "legislative_analysis"
    DEEP_ANALYSIS = "deep_analysis"
    FALLBACK = "fallback"
    ERROR = "error"


class ErrorDomain(Enum):
    """Classification of errors by domain."""
    STATUTORY_CONSTRUCTION = "statutory_construction"
    CONGRESSIONAL_PROCEDURE = "congressional_procedure"
    REGULATORY_RULEMAKING = "regulatory_rulemaking"
    PREEMPTION = "preemption"
    DELEGATION = "delegation"
    REDISTRICTING = "redistricting"
    LOBBYING = "lobbying"
    CONSTITUTIONAL = "constitutional"
    LEGISLATIVE_PROCESS = "legislative_process"
    APPROPRIATIONS = "appropriations"
    OVERSIGHT = "oversight"
    TEXAS_LEGISLATURE = "texas_legislature"
    SEARCH = "search"
    SEMANTIC = "semantic"
    SYSTEM = "system"
    VALIDATION = "validation"
    CONFIGURATION = "configuration"
    NETWORK = "network"
    STORAGE = "storage"


class MutationType(Enum):
    """Types of doctrine mutations."""
    BLOCK_ADDED = "block_added"
    BLOCK_MODIFIED = "block_modified"
    BLOCK_DEPRECATED = "block_deprecated"
    BLOCK_REMOVED = "block_removed"
    CONFIDENCE_ADJUSTED = "confidence_adjusted"
    DRIFT_DETECTED = "drift_detected"
    STALENESS_FLAGGED = "staleness_flagged"
    AUTHORITY_UPDATED = "authority_updated"
    CITATION_ADDED = "citation_added"
    CITATION_INVALIDATED = "citation_invalidated"


class MutationOrigin(Enum):
    """Where a doctrine mutation originated."""
    DRIFT_WATCHER = "drift_watcher"
    MANUAL_UPDATE = "manual_update"
    AUTOMATED_REFRESH = "automated_refresh"
    CASE_LAW_UPDATE = "case_law_update"
    LEGISLATIVE_CHANGE = "legislative_change"
    REGULATION_CHANGE = "regulation_change"
    SCOTUS_OPINION = "scotus_opinion"
    CIRCUIT_DECISION = "circuit_decision"
    EXECUTIVE_ORDER = "executive_order"
    STATE_LEGISLATIVE_CHANGE = "state_legislative_change"
    ADMIN_OVERRIDE = "admin_override"


class CitationLookupType(Enum):
    """Types of citation lookups tracked."""
    US_CONSTITUTION = "us_constitution"
    FEDERAL_STATUTE = "federal_statute"
    STATE_STATUTE = "state_statute"
    CASE_CITATION = "case_citation"
    CFR_REGULATION = "cfr_regulation"
    EXECUTIVE_ORDER = "executive_order"
    COMMITTEE_REPORT = "committee_report"
    CRS_REPORT = "crs_report"
    PUBLIC_LAW = "public_law"
    CONGRESSIONAL_RULE = "congressional_rule"


class LegislativeMetricType(Enum):
    """Legislative-specific metric categories."""
    STATUTORY_CONSTRUCTION_QUERY = "statutory_construction_query"
    CANON_APPLICATION = "canon_application"
    CONGRESSIONAL_PROCEDURE_QUERY = "congressional_procedure_query"
    REGULATORY_RULEMAKING_QUERY = "regulatory_rulemaking_query"
    PREEMPTION_QUERY = "preemption_query"
    DELEGATION_QUERY = "delegation_query"
    DEFERENCE_QUERY = "deference_query"
    REDISTRICTING_QUERY = "redistricting_query"
    LOBBYING_QUERY = "lobbying_query"
    BILL_ANALYSIS = "bill_analysis"
    LEGISLATIVE_HISTORY_QUERY = "legislative_history_query"
    CONSTITUTIONAL_AMENDMENT_QUERY = "constitutional_amendment_query"
    TEXAS_LEGISLATURE_QUERY = "texas_legislature_query"
    APPROPRIATIONS_QUERY = "appropriations_query"
    OVERSIGHT_QUERY = "oversight_query"
    VETO_QUERY = "veto_query"


# ============================================================================
# TELEMETRY STEP
# ============================================================================

@dataclass
class TelemetryStep:
    """Single step in a query trace."""
    step_name: str
    layer: ResponseLayer
    start_time: float
    end_time: float = 0.0
    duration_ms: float = 0.0
    tokens_processed: int = 0
    metadata: Dict[str, Any] = dc_field(default_factory=dict)

    def complete(self) -> None:
        """Mark step as complete and calculate duration."""
        self.end_time = time.perf_counter()
        self.duration_ms = (self.end_time - self.start_time) * 1000


# ============================================================================
# QUERY TRACE
# ============================================================================

@dataclass
class QueryTrace:
    """Complete trace of a single query's lifecycle."""
    trace_id: str
    query_hash: str
    query_text: str
    mode: str
    start_time: float
    end_time: float = 0.0
    total_duration_ms: float = 0.0
    steps: List[TelemetryStep] = dc_field(default_factory=list)
    layer_used: ResponseLayer = ResponseLayer.FALLBACK
    confidence_score: float = 0.0
    confidence_band: str = ""
    leg_category: str = ""
    jurisdiction: Optional[str] = None
    citations_count: int = 0
    error: Optional[str] = None
    metadata: Dict[str, Any] = dc_field(default_factory=dict)

    def add_step(self, step_name: str, layer: ResponseLayer) -> TelemetryStep:
        """Add a new step to the trace."""
        step = TelemetryStep(
            step_name=step_name,
            layer=layer,
            start_time=time.perf_counter(),
        )
        self.steps.append(step)
        return step

    def complete(self, layer: ResponseLayer, confidence: float, band: str) -> None:
        """Mark the trace as complete."""
        self.end_time = time.perf_counter()
        self.total_duration_ms = (self.end_time - self.start_time) * 1000
        self.layer_used = layer
        self.confidence_score = confidence
        self.confidence_band = band

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "trace_id": self.trace_id,
            "query_hash": self.query_hash,
            "mode": self.mode,
            "total_duration_ms": round(self.total_duration_ms, 3),
            "layer_used": self.layer_used.value,
            "confidence_score": round(self.confidence_score, 4),
            "confidence_band": self.confidence_band,
            "leg_category": self.leg_category,
            "jurisdiction": self.jurisdiction,
            "citations_count": self.citations_count,
            "steps_count": len(self.steps),
            "error": self.error,
        }


# ============================================================================
# AUDIT TRAIL
# ============================================================================

class AuditTrail:
    """Append-only JSONL audit log with SHA-256 hash chain."""

    def __init__(self, log_path: Path) -> None:
        self._log_path = log_path
        self._log_path.parent.mkdir(parents=True, exist_ok=True)
        self._last_hash: str = "0" * 64
        self._entry_count: int = 0
        self._lock = threading.Lock()
        logger.info("AuditTrail initialized at {}", self._log_path)

    def log_entry(self, entry: Dict[str, Any]) -> str:
        """Append an audit entry with SHA-256 chain link."""
        with self._lock:
            entry["_audit_seq"] = self._entry_count
            entry["_audit_timestamp"] = datetime.now(timezone.utc).isoformat()
            entry["_audit_prev_hash"] = self._last_hash
            entry_json = json.dumps(entry, sort_keys=True, default=str)
            entry_hash = hashlib.sha256(entry_json.encode("utf-8")).hexdigest()
            entry["_audit_hash"] = entry_hash
            try:
                with open(self._log_path, "a", encoding="utf-8") as f:
                    f.write(json.dumps(entry, default=str) + "\n")
            except OSError as exc:
                logger.error("Failed to write audit entry: {}", exc)
                return ""
            self._last_hash = entry_hash
            self._entry_count += 1
            return entry_hash

    def get_stats(self) -> Dict[str, Any]:
        """Return audit trail statistics."""
        return {
            "log_path": str(self._log_path),
            "entry_count": self._entry_count,
            "last_hash": self._last_hash[:16],
        }

    def verify_chain(self) -> Dict[str, Any]:
        """Verify the integrity of the audit chain."""
        if not self._log_path.exists():
            return {"valid": True, "entries_checked": 0, "issues": []}
        issues: List[str] = []
        entries_checked = 0
        prev_hash = "0" * 64
        try:
            with open(self._log_path, "r", encoding="utf-8") as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        entry = json.loads(line)
                    except json.JSONDecodeError:
                        issues.append(f"Line {line_num}: invalid JSON")
                        continue
                    recorded_prev = entry.get("_audit_prev_hash", "")
                    if recorded_prev != prev_hash:
                        issues.append(f"Line {line_num}: chain break (expected {prev_hash[:16]}, got {recorded_prev[:16]})")
                    recorded_hash = entry.pop("_audit_hash", "")
                    verify_json = json.dumps(entry, sort_keys=True, default=str)
                    computed_hash = hashlib.sha256(verify_json.encode("utf-8")).hexdigest()
                    entry["_audit_hash"] = recorded_hash
                    prev_hash = recorded_hash
                    entries_checked += 1
        except OSError as exc:
            issues.append(f"Failed to read audit log: {exc}")
        return {
            "valid": len(issues) == 0,
            "entries_checked": entries_checked,
            "issues": issues,
        }


# ============================================================================
# METRICS AGGREGATOR
# ============================================================================

class MetricsAggregator:
    """Rolling window metrics aggregation."""

    def __init__(self, window_size: int = 1000) -> None:
        self._window_size = window_size
        self._latencies: deque = deque(maxlen=window_size)
        self._layer_counts: Counter = Counter()
        self._mode_counts: Counter = Counter()
        self._category_counts: Counter = Counter()
        self._confidence_scores: deque = deque(maxlen=window_size)
        self._error_count: int = 0
        self._total_queries: int = 0
        self._citation_counts: deque = deque(maxlen=window_size)
        self._legislative_metrics: Counter = Counter()
        self._lock = threading.Lock()

    def record_query(self, trace: QueryTrace) -> None:
        """Record metrics from a completed query trace."""
        with self._lock:
            self._total_queries += 1
            self._latencies.append(trace.total_duration_ms)
            self._layer_counts[trace.layer_used.value] += 1
            self._mode_counts[trace.mode] += 1
            if trace.leg_category:
                self._category_counts[trace.leg_category] += 1
            self._confidence_scores.append(trace.confidence_score)
            self._citation_counts.append(trace.citations_count)
            if trace.error:
                self._error_count += 1

    def record_legislative_metric(self, metric_type: LegislativeMetricType) -> None:
        """Record a legislative-specific metric."""
        with self._lock:
            self._legislative_metrics[metric_type.value] += 1

    def get_summary(self) -> Dict[str, Any]:
        """Return aggregated metrics summary."""
        with self._lock:
            latencies = list(self._latencies)
            confidences = list(self._confidence_scores)
            citations = list(self._citation_counts)

        avg_latency = sum(latencies) / max(len(latencies), 1)
        p50_latency = sorted(latencies)[len(latencies) // 2] if latencies else 0
        p95_idx = int(len(latencies) * 0.95)
        p95_latency = sorted(latencies)[min(p95_idx, len(latencies) - 1)] if latencies else 0
        p99_idx = int(len(latencies) * 0.99)
        p99_latency = sorted(latencies)[min(p99_idx, len(latencies) - 1)] if latencies else 0

        avg_confidence = sum(confidences) / max(len(confidences), 1)
        avg_citations = sum(citations) / max(len(citations), 1)

        return {
            "total_queries": self._total_queries,
            "error_count": self._error_count,
            "error_rate": round(self._error_count / max(self._total_queries, 1), 4),
            "latency": {
                "avg_ms": round(avg_latency, 3),
                "p50_ms": round(p50_latency, 3),
                "p95_ms": round(p95_latency, 3),
                "p99_ms": round(p99_latency, 3),
            },
            "avg_confidence": round(avg_confidence, 4),
            "avg_citations": round(avg_citations, 2),
            "layer_distribution": dict(self._layer_counts),
            "mode_distribution": dict(self._mode_counts),
            "category_distribution": dict(self._category_counts.most_common(15)),
            "legislative_metrics": dict(self._legislative_metrics),
        }


# ============================================================================
# ERROR TRACKER
# ============================================================================

class ErrorTracker:
    """Domain-classified error tracking."""

    def __init__(self, max_errors: int = 500) -> None:
        self._errors: deque = deque(maxlen=max_errors)
        self._domain_counts: Counter = Counter()
        self._lock = threading.Lock()

    def log_error(
        self,
        domain: ErrorDomain,
        message: str,
        trace_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Log an error with domain classification."""
        error_id = str(uuid.uuid4())[:12]
        with self._lock:
            error_entry = {
                "error_id": error_id,
                "domain": domain.value,
                "message": message,
                "trace_id": trace_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "metadata": metadata or {},
            }
            self._errors.append(error_entry)
            self._domain_counts[domain.value] += 1
        logger.error(
            "Error [{}] domain={} trace={}: {}",
            error_id,
            domain.value,
            trace_id or "none",
            message,
        )
        return error_id

    def get_recent_errors(self, count: int = 20) -> List[Dict[str, Any]]:
        """Return the most recent errors."""
        with self._lock:
            return list(self._errors)[-count:]

    def get_error_summary(self) -> Dict[str, Any]:
        """Return error summary by domain."""
        with self._lock:
            return {
                "total_errors": sum(self._domain_counts.values()),
                "by_domain": dict(self._domain_counts.most_common()),
            }


# ============================================================================
# DOCTRINE MUTATION LOG
# ============================================================================

class DoctrineMutationLog:
    """Track mutations to the doctrine cache."""

    def __init__(self) -> None:
        self._mutations: List[Dict[str, Any]] = []
        self._lock = threading.Lock()

    def log_mutation(
        self,
        mutation_type: MutationType,
        origin: MutationOrigin,
        topic: str,
        description: str,
        old_value: Optional[Any] = None,
        new_value: Optional[Any] = None,
    ) -> str:
        """Log a doctrine mutation."""
        mutation_id = str(uuid.uuid4())[:12]
        with self._lock:
            self._mutations.append({
                "mutation_id": mutation_id,
                "type": mutation_type.value,
                "origin": origin.value,
                "topic": topic,
                "description": description,
                "old_value": str(old_value) if old_value is not None else None,
                "new_value": str(new_value) if new_value is not None else None,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
        logger.info(
            "Doctrine mutation [{}]: {} on '{}' from {}: {}",
            mutation_id,
            mutation_type.value,
            topic,
            origin.value,
            description,
        )
        return mutation_id

    def get_mutations(self, count: int = 50) -> List[Dict[str, Any]]:
        """Return recent mutations."""
        with self._lock:
            return list(self._mutations[-count:])

    def get_mutation_stats(self) -> Dict[str, Any]:
        """Return mutation statistics."""
        with self._lock:
            type_counts = Counter(m["type"] for m in self._mutations)
            origin_counts = Counter(m["origin"] for m in self._mutations)
            return {
                "total_mutations": len(self._mutations),
                "by_type": dict(type_counts),
                "by_origin": dict(origin_counts),
            }


# ============================================================================
# TELEMETRY COLLECTOR - MAIN ORCHESTRATOR
# ============================================================================

class TelemetryCollector:
    """Main telemetry orchestrator combining all components."""

    def __init__(self, log_dir: Path, ring_buffer_size: int = 10000) -> None:
        self._log_dir = log_dir
        self._log_dir.mkdir(parents=True, exist_ok=True)
        self._audit = AuditTrail(log_dir / "audit_trail.jsonl")
        self._metrics = MetricsAggregator(window_size=ring_buffer_size)
        self._errors = ErrorTracker(max_errors=500)
        self._mutations = DoctrineMutationLog()
        self._active_traces: Dict[str, QueryTrace] = {}
        self._completed_traces: deque = deque(maxlen=ring_buffer_size)
        self._lock = threading.Lock()
        self._start_time = time.time()
        logger.info("TelemetryCollector initialized in {}", log_dir)

    def start_trace(self, query: str, query_hash: str, mode: str) -> QueryTrace:
        """Start a new query trace."""
        trace = QueryTrace(
            trace_id=str(uuid.uuid4())[:12],
            query_hash=query_hash,
            query_text=query[:200],
            mode=mode,
            start_time=time.perf_counter(),
        )
        with self._lock:
            self._active_traces[trace.trace_id] = trace
        return trace

    def complete_trace(self, trace: QueryTrace) -> None:
        """Complete a trace and record metrics."""
        with self._lock:
            self._active_traces.pop(trace.trace_id, None)
            self._completed_traces.append(trace)
        self._metrics.record_query(trace)
        self._audit.log_entry({
            "event": "query_completed",
            "trace_id": trace.trace_id,
            "query_hash": trace.query_hash,
            "mode": trace.mode,
            "duration_ms": round(trace.total_duration_ms, 3),
            "layer": trace.layer_used.value,
            "confidence": round(trace.confidence_score, 4),
            "band": trace.confidence_band,
            "category": trace.leg_category,
            "jurisdiction": trace.jurisdiction,
            "citations": trace.citations_count,
            "error": trace.error,
        })

    def log_error(
        self,
        domain: ErrorDomain,
        message: str,
        trace_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Log an error through the telemetry system."""
        error_id = self._errors.log_error(domain, message, trace_id, metadata)
        self._audit.log_entry({
            "event": "error",
            "error_id": error_id,
            "domain": domain.value,
            "message": message,
            "trace_id": trace_id,
        })
        return error_id

    def record_citation_lookup(self, lookup_type: CitationLookupType, citation: str) -> None:
        """Record a citation lookup event."""
        self._audit.log_entry({
            "event": "citation_lookup",
            "type": lookup_type.value,
            "citation": citation,
        })

    def record_doctrine_mutation(
        self,
        mutation_type: MutationType,
        origin: MutationOrigin,
        topic: str,
        description: str,
        old_value: Optional[Any] = None,
        new_value: Optional[Any] = None,
    ) -> str:
        """Record a doctrine mutation."""
        mutation_id = self._mutations.log_mutation(
            mutation_type, origin, topic, description, old_value, new_value
        )
        self._audit.log_entry({
            "event": "doctrine_mutation",
            "mutation_id": mutation_id,
            "type": mutation_type.value,
            "origin": origin.value,
            "topic": topic,
            "description": description,
        })
        return mutation_id

    def record_legislative_metric(self, metric_type: LegislativeMetricType) -> None:
        """Record a legislative-specific metric."""
        self._metrics.record_legislative_metric(metric_type)

    def get_health(self) -> Dict[str, Any]:
        """Return telemetry system health."""
        uptime = time.time() - self._start_time
        with self._lock:
            active_count = len(self._active_traces)
            completed_count = len(self._completed_traces)
        return {
            "status": "healthy",
            "uptime_seconds": round(uptime, 1),
            "active_traces": active_count,
            "completed_traces": completed_count,
            "metrics": self._metrics.get_summary(),
            "errors": self._errors.get_error_summary(),
            "mutations": self._mutations.get_mutation_stats(),
            "audit": self._audit.get_stats(),
        }


# ============================================================================
# MODULE-LEVEL SINGLETON
# ============================================================================

_TELEMETRY: Optional[TelemetryCollector] = None


def get_telemetry(log_dir: Optional[Path] = None) -> TelemetryCollector:
    """Return the singleton telemetry collector."""
    global _TELEMETRY
    if _TELEMETRY is None:
        if log_dir is None:
            log_dir = Path(__file__).parent / "logs"
        _TELEMETRY = TelemetryCollector(log_dir)
    return _TELEMETRY


def trace_query(query: str, query_hash: str, mode: str) -> QueryTrace:
    """Start a new query trace via the singleton collector."""
    return get_telemetry().start_trace(query, query_hash, mode)


def complete_trace(trace: QueryTrace) -> None:
    """Complete a query trace via the singleton collector."""
    get_telemetry().complete_trace(trace)


def log_error(
    domain: ErrorDomain,
    message: str,
    trace_id: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> str:
    """Log an error via the singleton collector."""
    return get_telemetry().log_error(domain, message, trace_id, metadata)


def record_citation_lookup(lookup_type: CitationLookupType, citation: str) -> None:
    """Record a citation lookup via the singleton collector."""
    get_telemetry().record_citation_lookup(lookup_type, citation)


def record_doctrine_mutation(
    mutation_type: MutationType,
    origin: MutationOrigin,
    topic: str,
    description: str,
    old_value: Optional[Any] = None,
    new_value: Optional[Any] = None,
) -> str:
    """Record a doctrine mutation via the singleton collector."""
    return get_telemetry().record_doctrine_mutation(
        mutation_type, origin, topic, description, old_value, new_value
    )
