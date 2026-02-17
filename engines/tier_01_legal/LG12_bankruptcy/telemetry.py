"""
LG12 Bankruptcy Law Engine - Telemetry Module
================================================
Production telemetry, metrics collection, audit trail, and observability
for the Bankruptcy Law Engine.

Components:
    - TelemetryCollector: Ring-buffer based metric collection
    - QueryTrace: Per-query trace with timing breakdowns
    - AuditTrail: Append-only JSONL audit log with SHA-256 chain
    - MetricsAggregator: Rolling window aggregation for dashboards
    - ErrorTracker: Domain-classified error tracking and alerting
    - DoctrineMutationLog: Track changes to doctrine cache
    - BankruptcyMetrics: Chapter/means-test/discharge specific counters

Port: 8402
Engine: LG12 Bankruptcy Law
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
    BANKRUPTCY_ANALYSIS = "bankruptcy_analysis"
    DEEP_ANALYSIS = "deep_analysis"
    FALLBACK = "fallback"
    ERROR = "error"


class ErrorDomain(Enum):
    """Classification of errors by domain."""
    CHAPTER_7 = "chapter_7"
    CHAPTER_11 = "chapter_11"
    CHAPTER_13 = "chapter_13"
    CHAPTER_12 = "chapter_12"
    CHAPTER_15 = "chapter_15"
    MEANS_TEST = "means_test"
    AUTOMATIC_STAY = "automatic_stay"
    DISCHARGE = "discharge"
    EXEMPTIONS = "exemptions"
    AVOIDANCE = "avoidance"
    PREFERENCE = "preference"
    FRAUDULENT_TRANSFER = "fraudulent_transfer"
    PLAN_CONFIRMATION = "plan_confirmation"
    ADVERSARY = "adversary"
    TRUSTEE = "trustee"
    CRAMDOWN = "cramdown"
    REAFFIRMATION = "reaffirmation"
    STUDENT_LOAN = "student_loan"
    TAX_DEBT = "tax_debt"
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
    FRBP_AMENDMENT = "frbp_amendment"
    SCOTUS_OPINION = "scotus_opinion"
    CIRCUIT_SPLIT = "circuit_split"
    US_TRUSTEE_GUIDELINE = "us_trustee_guideline"
    MEDIAN_INCOME_UPDATE = "median_income_update"
    EXEMPTION_AMOUNT_UPDATE = "exemption_amount_update"
    LOCAL_RULE_CHANGE = "local_rule_change"


class CitationLookupType(Enum):
    """Types of citation lookups."""
    TITLE_11_USC = "title_11_usc"
    TITLE_28_USC = "title_28_usc"
    FRBP = "frbp"
    LOCAL_RULE = "local_rule"
    CASE_LAW = "case_law"
    CFR = "cfr"
    TREATISE = "treatise"
    US_TRUSTEE = "us_trustee"


class BankruptcyMetricType(Enum):
    """Bankruptcy-specific metric categories."""
    CHAPTER_7_QUERY = auto()
    CHAPTER_11_QUERY = auto()
    CHAPTER_13_QUERY = auto()
    CHAPTER_12_QUERY = auto()
    CHAPTER_15_QUERY = auto()
    MEANS_TEST_CALCULATION = auto()
    EXEMPTION_ANALYSIS = auto()
    DISCHARGE_DETERMINATION = auto()
    STAY_ANALYSIS = auto()
    AVOIDANCE_ACTION = auto()
    PREFERENCE_ANALYSIS = auto()
    FRAUDULENT_TRANSFER_ANALYSIS = auto()
    PLAN_CONFIRMATION_REVIEW = auto()
    CRAMDOWN_CALCULATION = auto()
    LIEN_STRIP_ANALYSIS = auto()
    ADVERSARY_ANALYSIS = auto()
    REAFFIRMATION_REVIEW = auto()
    STUDENT_LOAN_BRUNNER = auto()
    TAX_DISCHARGE_ANALYSIS = auto()
    TRUSTEE_POWER_QUERY = auto()
    TX_EXEMPTION_QUERY = auto()
    CROSS_BORDER_QUERY = auto()


# ============================================================================
# QUERY TRACE
# ============================================================================

@dataclass
class QueryTrace:
    """Per-query trace with timing breakdowns for bankruptcy analysis."""

    trace_id: str
    query_text: str
    start_time: float
    response_layer: Optional[ResponseLayer] = None
    end_time: Optional[float] = None
    normalization_ms: float = 0.0
    doctrine_lookup_ms: float = 0.0
    search_ms: float = 0.0
    analysis_ms: float = 0.0
    total_ms: float = 0.0
    tokens_in: int = 0
    tokens_out: int = 0
    doctrine_hits: int = 0
    search_results: int = 0
    confidence: float = 0.0
    chapter_type: Optional[str] = None
    bankruptcy_category: Optional[str] = None
    citations_returned: int = 0
    mode: str = "fast"
    error: Optional[str] = None
    metadata: Dict[str, Any] = dc_field(default_factory=dict)

    def finalize(self) -> None:
        """Calculate total duration and finalize trace."""
        if self.end_time is None:
            self.end_time = time.monotonic()
        self.total_ms = (self.end_time - self.start_time) * 1000.0

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "trace_id": self.trace_id,
            "query_text": self.query_text[:200],
            "start_time": self.start_time,
            "end_time": self.end_time,
            "response_layer": self.response_layer.value if self.response_layer else None,
            "normalization_ms": round(self.normalization_ms, 3),
            "doctrine_lookup_ms": round(self.doctrine_lookup_ms, 3),
            "search_ms": round(self.search_ms, 3),
            "analysis_ms": round(self.analysis_ms, 3),
            "total_ms": round(self.total_ms, 3),
            "tokens_in": self.tokens_in,
            "tokens_out": self.tokens_out,
            "doctrine_hits": self.doctrine_hits,
            "search_results": self.search_results,
            "confidence": round(self.confidence, 4),
            "chapter_type": self.chapter_type,
            "bankruptcy_category": self.bankruptcy_category,
            "citations_returned": self.citations_returned,
            "mode": self.mode,
            "error": self.error,
            "metadata": self.metadata,
        }


# ============================================================================
# AUDIT TRAIL
# ============================================================================

class AuditTrail:
    """Append-only JSONL audit log with SHA-256 hash chain for tamper detection."""

    def __init__(self, log_path: Path) -> None:
        self._log_path = log_path
        self._log_path.parent.mkdir(parents=True, exist_ok=True)
        self._last_hash: str = "GENESIS"
        self._lock = threading.Lock()
        self._entry_count: int = 0
        self._recover_last_hash()

    def _recover_last_hash(self) -> None:
        """Recover the last hash from existing log for chain continuity."""
        if not self._log_path.exists():
            return
        try:
            last_line = ""
            with self._log_path.open("r", encoding="utf-8") as fh:
                for line in fh:
                    if line.strip():
                        last_line = line.strip()
                        self._entry_count += 1
            if last_line:
                entry = json.loads(last_line)
                self._last_hash = entry.get("chain_hash", "GENESIS")
        except (json.JSONDecodeError, OSError) as exc:
            logger.warning(f"Could not recover audit hash chain: {exc}")

    def _compute_chain_hash(self, payload: str) -> str:
        """Compute the next hash in the chain."""
        combined = f"{self._last_hash}:{payload}"
        return hashlib.sha256(combined.encode("utf-8")).hexdigest()

    def append(self, event_type: str, data: Dict[str, Any]) -> str:
        """Append an audit entry and return its chain hash."""
        with self._lock:
            timestamp = datetime.now(timezone.utc).isoformat()
            entry_id = str(uuid.uuid4())
            payload_str = json.dumps(data, sort_keys=True, default=str)
            chain_hash = self._compute_chain_hash(payload_str)
            entry = {
                "entry_id": entry_id,
                "timestamp": timestamp,
                "event_type": event_type,
                "data": data,
                "chain_hash": chain_hash,
                "prev_hash": self._last_hash,
                "sequence": self._entry_count,
            }
            try:
                with self._log_path.open("a", encoding="utf-8") as fh:
                    fh.write(json.dumps(entry, default=str) + "\n")
                self._last_hash = chain_hash
                self._entry_count += 1
            except OSError as exc:
                logger.error(f"Audit trail write failed: {exc}")
            return chain_hash

    def verify_chain(self, max_entries: int = 1000) -> Tuple[bool, int, int]:
        """Verify the hash chain integrity. Returns (valid, checked, errors)."""
        if not self._log_path.exists():
            return (True, 0, 0)
        checked = 0
        errors = 0
        prev_hash = "GENESIS"
        try:
            with self._log_path.open("r", encoding="utf-8") as fh:
                for line in fh:
                    if checked >= max_entries:
                        break
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        entry = json.loads(line)
                    except json.JSONDecodeError:
                        errors += 1
                        checked += 1
                        continue
                    stored_prev = entry.get("prev_hash", "")
                    if stored_prev != prev_hash:
                        errors += 1
                    payload_str = json.dumps(entry.get("data", {}), sort_keys=True, default=str)
                    expected_hash = hashlib.sha256(
                        f"{prev_hash}:{payload_str}".encode("utf-8")
                    ).hexdigest()
                    stored_hash = entry.get("chain_hash", "")
                    if stored_hash != expected_hash:
                        errors += 1
                    prev_hash = stored_hash
                    checked += 1
        except OSError as exc:
            logger.error(f"Audit chain verification error: {exc}")
            errors += 1
        return (errors == 0, checked, errors)

    @property
    def entry_count(self) -> int:
        """Return total entries in the audit trail."""
        return self._entry_count

    @property
    def last_hash(self) -> str:
        """Return the most recent chain hash."""
        return self._last_hash


# ============================================================================
# METRICS AGGREGATOR
# ============================================================================

class MetricsAggregator:
    """Rolling-window metrics aggregation for dashboard display."""

    def __init__(self, window_size: int = 1000) -> None:
        self._window_size = window_size
        self._latencies: deque = deque(maxlen=window_size)
        self._layer_counts: Counter = Counter()
        self._error_counts: Counter = Counter()
        self._mode_counts: Counter = Counter()
        self._chapter_counts: Counter = Counter()
        self._category_counts: Counter = Counter()
        self._citation_lookup_counts: Counter = Counter()
        self._bk_metric_counts: Counter = Counter()
        self._confidence_sum: float = 0.0
        self._confidence_count: int = 0
        self._total_queries: int = 0
        self._lock = threading.Lock()

    def record_trace(self, trace: QueryTrace) -> None:
        """Record a completed query trace into aggregation."""
        with self._lock:
            self._total_queries += 1
            self._latencies.append(trace.total_ms)
            if trace.response_layer:
                self._layer_counts[trace.response_layer.value] += 1
            self._mode_counts[trace.mode] += 1
            if trace.chapter_type:
                self._chapter_counts[trace.chapter_type] += 1
            if trace.bankruptcy_category:
                self._category_counts[trace.bankruptcy_category] += 1
            if trace.error:
                self._error_counts[trace.error[:80]] += 1
            self._confidence_sum += trace.confidence
            self._confidence_count += 1

    def record_citation_lookup(self, lookup_type: CitationLookupType) -> None:
        """Record a citation lookup event."""
        with self._lock:
            self._citation_lookup_counts[lookup_type.value] += 1

    def record_bk_metric(self, metric_type: BankruptcyMetricType) -> None:
        """Record a bankruptcy-specific metric event."""
        with self._lock:
            self._bk_metric_counts[metric_type.name] += 1

    def get_summary(self) -> Dict[str, Any]:
        """Return aggregated metrics summary."""
        with self._lock:
            latencies = list(self._latencies)
            if latencies:
                sorted_lat = sorted(latencies)
                n = len(sorted_lat)
                p50 = sorted_lat[int(n * 0.50)]
                p90 = sorted_lat[int(n * 0.90)]
                p99 = sorted_lat[min(int(n * 0.99), n - 1)]
                avg_lat = sum(sorted_lat) / n
                min_lat = sorted_lat[0]
                max_lat = sorted_lat[-1]
                std_dev = math.sqrt(sum((x - avg_lat) ** 2 for x in sorted_lat) / n) if n > 1 else 0.0
            else:
                p50 = p90 = p99 = avg_lat = min_lat = max_lat = std_dev = 0.0
            avg_conf = (
                self._confidence_sum / self._confidence_count
                if self._confidence_count > 0 else 0.0
            )
            return {
                "total_queries": self._total_queries,
                "window_size": self._window_size,
                "latency": {
                    "p50_ms": round(p50, 3),
                    "p90_ms": round(p90, 3),
                    "p99_ms": round(p99, 3),
                    "avg_ms": round(avg_lat, 3),
                    "min_ms": round(min_lat, 3),
                    "max_ms": round(max_lat, 3),
                    "std_dev_ms": round(std_dev, 3),
                },
                "response_layers": dict(self._layer_counts),
                "modes": dict(self._mode_counts),
                "chapters": dict(self._chapter_counts),
                "categories": dict(self._category_counts),
                "errors": dict(self._error_counts),
                "citation_lookups": dict(self._citation_lookup_counts),
                "bankruptcy_metrics": dict(self._bk_metric_counts),
                "average_confidence": round(avg_conf, 4),
            }


# ============================================================================
# DOCTRINE MUTATION LOG
# ============================================================================

@dataclass
class DoctrineMutation:
    """A single doctrine mutation record."""

    mutation_id: str
    timestamp: str
    mutation_type: MutationType
    origin: MutationOrigin
    topic: str
    field_changed: str
    old_value: Any
    new_value: Any
    reason: str
    confidence_before: float = 0.0
    confidence_after: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "mutation_id": self.mutation_id,
            "timestamp": self.timestamp,
            "mutation_type": self.mutation_type.value,
            "origin": self.origin.value,
            "topic": self.topic,
            "field_changed": self.field_changed,
            "old_value": str(self.old_value)[:500],
            "new_value": str(self.new_value)[:500],
            "reason": self.reason,
            "confidence_before": round(self.confidence_before, 4),
            "confidence_after": round(self.confidence_after, 4),
        }


class DoctrineMutationLog:
    """Track all changes to doctrine cache blocks."""

    def __init__(self, max_entries: int = 5000) -> None:
        self._mutations: deque = deque(maxlen=max_entries)
        self._lock = threading.Lock()
        self._topic_mutation_count: Counter = Counter()

    def record(
        self,
        mutation_type: MutationType,
        origin: MutationOrigin,
        topic: str,
        field_changed: str,
        old_value: Any,
        new_value: Any,
        reason: str,
        confidence_before: float = 0.0,
        confidence_after: float = 0.0,
    ) -> DoctrineMutation:
        """Record a doctrine mutation."""
        mutation = DoctrineMutation(
            mutation_id=str(uuid.uuid4()),
            timestamp=datetime.now(timezone.utc).isoformat(),
            mutation_type=mutation_type,
            origin=origin,
            topic=topic,
            field_changed=field_changed,
            old_value=old_value,
            new_value=new_value,
            reason=reason,
            confidence_before=confidence_before,
            confidence_after=confidence_after,
        )
        with self._lock:
            self._mutations.append(mutation)
            self._topic_mutation_count[topic] += 1
        logger.info(
            f"Doctrine mutation recorded: {mutation_type.value} on "
            f"'{topic}' ({field_changed}) by {origin.value}"
        )
        return mutation

    def get_recent(self, count: int = 50) -> List[Dict[str, Any]]:
        """Return recent mutations."""
        with self._lock:
            items = list(self._mutations)[-count:]
        return [m.to_dict() for m in items]

    def get_topic_mutations(self, topic: str) -> List[Dict[str, Any]]:
        """Return all mutations for a specific topic."""
        with self._lock:
            items = [m for m in self._mutations if m.topic == topic]
        return [m.to_dict() for m in items]

    def get_stats(self) -> Dict[str, Any]:
        """Return mutation statistics."""
        with self._lock:
            type_counts: Counter = Counter()
            origin_counts: Counter = Counter()
            for m in self._mutations:
                type_counts[m.mutation_type.value] += 1
                origin_counts[m.origin.value] += 1
            return {
                "total_mutations": len(self._mutations),
                "by_type": dict(type_counts),
                "by_origin": dict(origin_counts),
                "top_mutated_topics": dict(self._topic_mutation_count.most_common(20)),
            }


# ============================================================================
# ERROR TRACKER
# ============================================================================

@dataclass
class ErrorRecord:
    """A single error occurrence."""

    error_id: str
    timestamp: str
    domain: ErrorDomain
    message: str
    trace_id: Optional[str] = None
    stack_trace: Optional[str] = None
    resolved: bool = False
    resolution: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "error_id": self.error_id,
            "timestamp": self.timestamp,
            "domain": self.domain.value,
            "message": self.message[:500],
            "trace_id": self.trace_id,
            "stack_trace": self.stack_trace[:1000] if self.stack_trace else None,
            "resolved": self.resolved,
            "resolution": self.resolution,
        }


class ErrorTracker:
    """Domain-classified error tracking with alerting thresholds."""

    def __init__(self, max_errors: int = 2000) -> None:
        self._errors: deque = deque(maxlen=max_errors)
        self._domain_counts: Counter = Counter()
        self._lock = threading.Lock()
        self._alert_thresholds: Dict[str, int] = {
            "chapter_7": 10,
            "chapter_11": 10,
            "chapter_13": 10,
            "means_test": 5,
            "discharge": 5,
            "exemptions": 5,
            "system": 3,
        }

    def record_error(
        self,
        domain: ErrorDomain,
        message: str,
        trace_id: Optional[str] = None,
        stack_trace: Optional[str] = None,
    ) -> ErrorRecord:
        """Record an error occurrence."""
        record = ErrorRecord(
            error_id=str(uuid.uuid4()),
            timestamp=datetime.now(timezone.utc).isoformat(),
            domain=domain,
            message=message,
            trace_id=trace_id,
            stack_trace=stack_trace,
        )
        with self._lock:
            self._errors.append(record)
            self._domain_counts[domain.value] += 1
            count = self._domain_counts[domain.value]
            threshold = self._alert_thresholds.get(domain.value, 20)
            if count % threshold == 0:
                logger.warning(
                    f"Error threshold reached for {domain.value}: {count} errors"
                )
        logger.error(f"[{domain.value}] {message[:200]}")
        return record

    def get_recent(self, count: int = 50) -> List[Dict[str, Any]]:
        """Return recent errors."""
        with self._lock:
            items = list(self._errors)[-count:]
        return [e.to_dict() for e in items]

    def get_stats(self) -> Dict[str, Any]:
        """Return error statistics."""
        with self._lock:
            return {
                "total_errors": len(self._errors),
                "by_domain": dict(self._domain_counts),
                "alert_thresholds": dict(self._alert_thresholds),
            }


# ============================================================================
# TELEMETRY COLLECTOR (MAIN)
# ============================================================================

class TelemetryCollector:
    """Central telemetry hub for the Bankruptcy Law Engine."""

    def __init__(
        self,
        audit_path: Path,
        ring_buffer_size: int = 10000,
    ) -> None:
        self._traces: deque = deque(maxlen=ring_buffer_size)
        self._aggregator = MetricsAggregator(window_size=ring_buffer_size)
        self._audit = AuditTrail(audit_path)
        self._mutation_log = DoctrineMutationLog()
        self._error_tracker = ErrorTracker()
        self._lock = threading.Lock()
        self._start_time = time.monotonic()
        self._startup_timestamp = datetime.now(timezone.utc).isoformat()
        logger.info("TelemetryCollector initialized for LG12 Bankruptcy Law Engine")

    def start_trace(self, query_text: str, mode: str = "fast") -> QueryTrace:
        """Begin a new query trace."""
        trace = QueryTrace(
            trace_id=str(uuid.uuid4()),
            query_text=query_text,
            start_time=time.monotonic(),
            mode=mode,
        )
        return trace

    def complete_trace(self, trace: QueryTrace) -> None:
        """Complete and record a query trace."""
        trace.finalize()
        with self._lock:
            self._traces.append(trace)
        self._aggregator.record_trace(trace)
        self._audit.append("query_completed", trace.to_dict())
        logger.debug(
            f"Trace {trace.trace_id[:8]} completed: "
            f"{trace.total_ms:.1f}ms layer={trace.response_layer}"
        )

    def log_error(
        self,
        domain: ErrorDomain,
        message: str,
        trace_id: Optional[str] = None,
        stack_trace: Optional[str] = None,
    ) -> ErrorRecord:
        """Log an error event."""
        record = self._error_tracker.record_error(domain, message, trace_id, stack_trace)
        self._audit.append("error", record.to_dict())
        return record

    def record_citation_lookup(self, lookup_type: CitationLookupType) -> None:
        """Record a citation lookup event."""
        self._aggregator.record_citation_lookup(lookup_type)

    def record_bk_metric(self, metric_type: BankruptcyMetricType) -> None:
        """Record a bankruptcy-specific metric."""
        self._aggregator.record_bk_metric(metric_type)

    def record_doctrine_mutation(
        self,
        mutation_type: MutationType,
        origin: MutationOrigin,
        topic: str,
        field_changed: str,
        old_value: Any,
        new_value: Any,
        reason: str,
        confidence_before: float = 0.0,
        confidence_after: float = 0.0,
    ) -> DoctrineMutation:
        """Record a doctrine mutation."""
        mutation = self._mutation_log.record(
            mutation_type, origin, topic, field_changed,
            old_value, new_value, reason, confidence_before, confidence_after,
        )
        self._audit.append("doctrine_mutation", mutation.to_dict())
        return mutation

    def get_metrics(self) -> Dict[str, Any]:
        """Return complete metrics summary."""
        uptime_seconds = time.monotonic() - self._start_time
        return {
            "engine_id": "LG12",
            "engine_name": "Bankruptcy Law Engine",
            "startup_time": self._startup_timestamp,
            "uptime_seconds": round(uptime_seconds, 1),
            "aggregated_metrics": self._aggregator.get_summary(),
            "mutation_stats": self._mutation_log.get_stats(),
            "error_stats": self._error_tracker.get_stats(),
            "audit_trail": {
                "entries": self._audit.entry_count,
                "last_hash": self._audit.last_hash[:16] + "...",
            },
        }

    def get_recent_traces(self, count: int = 50) -> List[Dict[str, Any]]:
        """Return recent query traces."""
        with self._lock:
            items = list(self._traces)[-count:]
        return [t.to_dict() for t in items]

    def get_recent_errors(self, count: int = 50) -> List[Dict[str, Any]]:
        """Return recent errors."""
        return self._error_tracker.get_recent(count)

    def get_recent_mutations(self, count: int = 50) -> List[Dict[str, Any]]:
        """Return recent doctrine mutations."""
        return self._mutation_log.get_recent(count)

    def verify_audit_chain(self, max_entries: int = 1000) -> Dict[str, Any]:
        """Verify the audit trail hash chain."""
        valid, checked, errors = self._audit.verify_chain(max_entries)
        return {"valid": valid, "entries_checked": checked, "errors": errors}

    @property
    def audit(self) -> AuditTrail:
        """Access the audit trail."""
        return self._audit

    @property
    def aggregator(self) -> MetricsAggregator:
        """Access the metrics aggregator."""
        return self._aggregator

    @property
    def mutation_log(self) -> DoctrineMutationLog:
        """Access the doctrine mutation log."""
        return self._mutation_log

    @property
    def error_tracker(self) -> ErrorTracker:
        """Access the error tracker."""
        return self._error_tracker


# ============================================================================
# MODULE-LEVEL SINGLETON
# ============================================================================

_TELEMETRY: Optional[TelemetryCollector] = None
_TELEMETRY_LOCK = threading.Lock()


def get_telemetry(audit_path: Optional[Path] = None) -> TelemetryCollector:
    """Get or create the module-level TelemetryCollector singleton."""
    global _TELEMETRY
    if _TELEMETRY is None:
        with _TELEMETRY_LOCK:
            if _TELEMETRY is None:
                if audit_path is None:
                    audit_path = Path(__file__).parent / "logs" / "audit_trail.jsonl"
                _TELEMETRY = TelemetryCollector(audit_path=audit_path)
    return _TELEMETRY


def trace_query(query_text: str, mode: str = "fast") -> QueryTrace:
    """Create a new query trace."""
    return get_telemetry().start_trace(query_text, mode)


def complete_trace(trace: QueryTrace) -> None:
    """Complete and record a query trace."""
    get_telemetry().complete_trace(trace)


def log_error(
    domain: ErrorDomain,
    message: str,
    trace_id: Optional[str] = None,
    stack_trace: Optional[str] = None,
) -> ErrorRecord:
    """Log an error event."""
    return get_telemetry().log_error(domain, message, trace_id, stack_trace)


def record_citation_lookup(lookup_type: CitationLookupType) -> None:
    """Record a citation lookup event."""
    get_telemetry().record_citation_lookup(lookup_type)


def record_doctrine_mutation(
    mutation_type: MutationType,
    origin: MutationOrigin,
    topic: str,
    field_changed: str,
    old_value: Any,
    new_value: Any,
    reason: str,
    confidence_before: float = 0.0,
    confidence_after: float = 0.0,
) -> DoctrineMutation:
    """Record a doctrine mutation."""
    return get_telemetry().record_doctrine_mutation(
        mutation_type, origin, topic, field_changed,
        old_value, new_value, reason, confidence_before, confidence_after,
    )


def record_bk_metric(metric_type: BankruptcyMetricType) -> None:
    """Record a bankruptcy-specific metric event."""
    get_telemetry().record_bk_metric(metric_type)
