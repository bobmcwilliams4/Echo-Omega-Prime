"""
LG14 Healthcare Law Engine - Telemetry Module
=================================================
Production telemetry, metrics collection, audit trail, and observability
for the Healthcare Law Engine.

Components:
    - TelemetryCollector: Ring-buffer based metric collection
    - QueryTrace: Per-query trace with timing breakdowns
    - AuditTrail: Append-only JSONL audit log with SHA-256 chain
    - MetricsAggregator: Rolling window aggregation for dashboards
    - ErrorTracker: Domain-classified error tracking and alerting
    - DoctrineMutationLog: Track changes to doctrine cache
    - HealthcareMetrics: Healthcare-specific counters

Port: 8404
Engine: LG14 Healthcare Law
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
    HEALTHCARE_ANALYSIS = "healthcare_analysis"
    DEEP_ANALYSIS = "deep_analysis"
    FALLBACK = "fallback"
    ERROR = "error"


class ErrorDomain(Enum):
    """Classification of errors by domain."""
    HIPAA = "hipaa"
    FRAUD_ABUSE = "fraud_abuse"
    MALPRACTICE = "malpractice"
    FDA = "fda"
    EMTALA = "emtala"
    ACA = "aca"
    TELEMEDICINE = "telemedicine"
    CLINICAL_TRIALS = "clinical_trials"
    PARITY = "parity"
    INTEROPERABILITY = "interoperability"
    PHARMACY = "pharmacy"
    PUBLIC_HEALTH = "public_health"
    TAX_EXEMPT = "tax_exempt"
    LICENSING = "licensing"
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
    HHS_GUIDANCE = "hhs_guidance"
    CMS_POLICY = "cms_policy"
    OIG_OPINION = "oig_opinion"
    FDA_GUIDANCE = "fda_guidance"
    OCR_ENFORCEMENT = "ocr_enforcement"
    ADMIN_OVERRIDE = "admin_override"


class CitationLookupType(Enum):
    """Types of citation lookups tracked."""
    FEDERAL_STATUTE = "federal_statute"
    STATE_STATUTE = "state_statute"
    CASE_CITATION = "case_citation"
    CFR_REGULATION = "cfr_regulation"
    CMS_MANUAL = "cms_manual"
    OIG_ADVISORY = "oig_advisory"
    FDA_GUIDANCE = "fda_guidance"
    RESTATEMENT = "restatement"
    IRC_SECTION = "irc_section"


class HealthcareMetricType(Enum):
    """Healthcare-specific metric categories."""
    HIPAA_QUERY = "hipaa_query"
    FRAUD_ABUSE_QUERY = "fraud_abuse_query"
    MALPRACTICE_QUERY = "malpractice_query"
    FDA_QUERY = "fda_query"
    EMTALA_QUERY = "emtala_query"
    ACA_QUERY = "aca_query"
    TELEMEDICINE_QUERY = "telemedicine_query"
    CLINICAL_TRIALS_QUERY = "clinical_trials_query"
    PARITY_QUERY = "parity_query"
    INTEROPERABILITY_QUERY = "interoperability_query"
    PHARMACY_QUERY = "pharmacy_query"
    PUBLIC_HEALTH_QUERY = "public_health_query"
    TAX_EXEMPT_QUERY = "tax_exempt_query"
    LICENSING_QUERY = "licensing_query"
    COMPLIANCE_CHECK = "compliance_check"
    REGULATORY_REVIEW = "regulatory_review"


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
    metadata: Dict[str, Any] = dc_field(default_factory=dict)
    error: Optional[str] = None
    hc_category: Optional[str] = None

    def complete(self) -> None:
        """Mark step complete and calculate duration."""
        self.end_time = time.monotonic()
        self.duration_ms = (self.end_time - self.start_time) * 1000.0


# ============================================================================
# QUERY TRACE
# ============================================================================

@dataclass
class QueryTrace:
    """Full trace of a single query through the engine."""
    trace_id: str
    query_text: str
    query_hash: str
    start_time: float
    end_time: float = 0.0
    total_duration_ms: float = 0.0
    steps: List[TelemetryStep] = dc_field(default_factory=list)
    final_layer: Optional[ResponseLayer] = None
    response_mode: str = "fast"
    hc_category: Optional[str] = None
    confidence_score: float = 0.0
    confidence_band: str = "HIGH_RISK"
    doctrine_hits: int = 0
    search_results: int = 0
    citations_found: int = 0
    error: Optional[str] = None
    determinism_hash: Optional[str] = None
    authority_level: float = 5.0
    client_ip: Optional[str] = None
    user_agent: Optional[str] = None
    jurisdiction: Optional[str] = None

    def add_step(self, step_name: str, layer: ResponseLayer, hc_category: Optional[str] = None) -> TelemetryStep:
        """Add a new step to the trace."""
        step = TelemetryStep(
            step_name=step_name,
            layer=layer,
            start_time=time.monotonic(),
            hc_category=hc_category,
        )
        self.steps.append(step)
        return step

    def complete(self) -> None:
        """Mark the trace as complete."""
        self.end_time = time.monotonic()
        self.total_duration_ms = (self.end_time - self.start_time) * 1000.0

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "trace_id": self.trace_id,
            "query_hash": self.query_hash,
            "total_duration_ms": round(self.total_duration_ms, 3),
            "final_layer": self.final_layer.value if self.final_layer else None,
            "response_mode": self.response_mode,
            "hc_category": self.hc_category,
            "confidence_score": round(self.confidence_score, 4),
            "confidence_band": self.confidence_band,
            "doctrine_hits": self.doctrine_hits,
            "search_results": self.search_results,
            "citations_found": self.citations_found,
            "error": self.error,
            "determinism_hash": self.determinism_hash,
            "jurisdiction": self.jurisdiction,
            "steps": [
                {
                    "step_name": s.step_name,
                    "layer": s.layer.value,
                    "duration_ms": round(s.duration_ms, 3),
                    "hc_category": s.hc_category,
                    "error": s.error,
                    "metadata": s.metadata,
                }
                for s in self.steps
            ],
        }


# ============================================================================
# AUDIT TRAIL
# ============================================================================

class AuditTrail:
    """Append-only JSONL audit log with SHA-256 hash chain."""

    def __init__(self, log_path: Path) -> None:
        self._log_path = log_path
        self._lock = threading.Lock()
        self._last_hash: str = "0" * 64
        self._entry_count: int = 0
        log_path.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"AuditTrail initialized at {log_path}")

    def append(self, event_type: str, data: Dict[str, Any]) -> str:
        """Append an audit entry and return its hash."""
        with self._lock:
            entry = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "event_type": event_type,
                "data": data,
                "sequence": self._entry_count,
                "prev_hash": self._last_hash,
            }
            entry_json = json.dumps(entry, sort_keys=True)
            entry_hash = hashlib.sha256(entry_json.encode("utf-8")).hexdigest()
            entry["hash"] = entry_hash

            try:
                with open(self._log_path, "a", encoding="utf-8") as fh:
                    fh.write(json.dumps(entry) + "\n")
            except OSError as exc:
                logger.error(f"Failed to write audit entry: {exc}")

            self._last_hash = entry_hash
            self._entry_count += 1
            return entry_hash

    def verify_chain(self) -> Dict[str, Any]:
        """Verify the integrity of the audit chain."""
        if not self._log_path.exists():
            return {"valid": True, "entries": 0, "message": "No audit entries found"}

        prev_hash = "0" * 64
        entry_count = 0
        broken_at: Optional[int] = None

        try:
            with open(self._log_path, "r", encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    entry = json.loads(line)
                    if entry.get("prev_hash") != prev_hash:
                        broken_at = entry_count
                        break
                    entry_copy = {k: v for k, v in entry.items() if k != "hash"}
                    computed = hashlib.sha256(json.dumps(entry_copy, sort_keys=True).encode("utf-8")).hexdigest()
                    if computed != entry.get("hash"):
                        broken_at = entry_count
                        break
                    prev_hash = entry["hash"]
                    entry_count += 1
        except (json.JSONDecodeError, OSError) as exc:
            return {"valid": False, "entries": entry_count, "error": str(exc)}

        return {
            "valid": broken_at is None,
            "entries": entry_count,
            "broken_at": broken_at,
            "last_hash": prev_hash,
        }

    @property
    def entry_count(self) -> int:
        """Return the number of audit entries."""
        return self._entry_count


# ============================================================================
# METRICS AGGREGATOR
# ============================================================================

class MetricsAggregator:
    """Rolling window metrics aggregation."""

    def __init__(self, window_size: int = 10000) -> None:
        self._window_size = window_size
        self._lock = threading.Lock()
        self._latencies: deque = deque(maxlen=window_size)
        self._layer_counts: Counter = Counter()
        self._mode_counts: Counter = Counter()
        self._category_counts: Counter = Counter()
        self._confidence_histogram: Counter = Counter()
        self._error_counts: Counter = Counter()
        self._citation_counts: Counter = Counter()
        self._hc_metric_counts: Counter = Counter()
        self._total_queries: int = 0
        self._total_errors: int = 0

    def record_query(self, trace: QueryTrace) -> None:
        """Record a completed query trace."""
        with self._lock:
            self._total_queries += 1
            self._latencies.append(trace.total_duration_ms)
            if trace.final_layer:
                self._layer_counts[trace.final_layer.value] += 1
            self._mode_counts[trace.response_mode] += 1
            if trace.hc_category:
                self._category_counts[trace.hc_category] += 1

            if trace.confidence_score >= 0.85:
                self._confidence_histogram["DEFENSIBLE"] += 1
            elif trace.confidence_score >= 0.65:
                self._confidence_histogram["SUPPORTABLE"] += 1
            elif trace.confidence_score >= 0.50:
                self._confidence_histogram["DISCLOSURE"] += 1
            else:
                self._confidence_histogram["HIGH_RISK"] += 1

            if trace.error:
                self._total_errors += 1
                self._error_counts[trace.error[:50]] += 1

    def record_hc_metric(self, metric_type: HealthcareMetricType) -> None:
        """Record a healthcare-specific metric."""
        with self._lock:
            self._hc_metric_counts[metric_type.value] += 1

    def record_citation_lookup(self, citation_type: CitationLookupType) -> None:
        """Record a citation lookup."""
        with self._lock:
            self._citation_counts[citation_type.value] += 1

    def get_summary(self) -> Dict[str, Any]:
        """Get aggregated metrics summary."""
        with self._lock:
            latency_list = list(self._latencies)
            if latency_list:
                avg_latency = sum(latency_list) / len(latency_list)
                p50 = sorted(latency_list)[len(latency_list) // 2]
                p95 = sorted(latency_list)[int(len(latency_list) * 0.95)] if len(latency_list) >= 20 else max(latency_list)
                p99 = sorted(latency_list)[int(len(latency_list) * 0.99)] if len(latency_list) >= 100 else max(latency_list)
            else:
                avg_latency = p50 = p95 = p99 = 0.0

            return {
                "total_queries": self._total_queries,
                "total_errors": self._total_errors,
                "error_rate": round(self._total_errors / max(self._total_queries, 1), 4),
                "latency_ms": {
                    "avg": round(avg_latency, 2),
                    "p50": round(p50, 2),
                    "p95": round(p95, 2),
                    "p99": round(p99, 2),
                },
                "layer_distribution": dict(self._layer_counts),
                "mode_distribution": dict(self._mode_counts),
                "category_distribution": dict(self._category_counts),
                "confidence_distribution": dict(self._confidence_histogram),
                "hc_metrics": dict(self._hc_metric_counts),
                "citation_lookups": dict(self._citation_counts),
                "top_errors": dict(self._error_counts.most_common(10)),
            }


# ============================================================================
# ERROR TRACKER
# ============================================================================

class ErrorTracker:
    """Domain-classified error tracking."""

    def __init__(self) -> None:
        self._errors: deque = deque(maxlen=1000)
        self._domain_counts: Counter = Counter()
        self._lock = threading.Lock()

    def record_error(self, domain: ErrorDomain, error_msg: str, context: Optional[Dict[str, Any]] = None) -> None:
        """Record an error with domain classification."""
        with self._lock:
            entry = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "domain": domain.value,
                "error": error_msg,
                "context": context or {},
            }
            self._errors.append(entry)
            self._domain_counts[domain.value] += 1
            logger.error(f"[{domain.value}] {error_msg}")

    def get_summary(self) -> Dict[str, Any]:
        """Get error summary."""
        with self._lock:
            return {
                "total_errors": sum(self._domain_counts.values()),
                "by_domain": dict(self._domain_counts),
                "recent_errors": list(self._errors)[-10:],
            }


# ============================================================================
# DOCTRINE MUTATION LOG
# ============================================================================

class DoctrineMutationLog:
    """Track mutations to the doctrine cache."""

    def __init__(self) -> None:
        self._mutations: deque = deque(maxlen=500)
        self._lock = threading.Lock()

    def record_mutation(
        self,
        mutation_type: MutationType,
        origin: MutationOrigin,
        topic: str,
        details: Dict[str, Any],
    ) -> None:
        """Record a doctrine mutation."""
        with self._lock:
            entry = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "mutation_type": mutation_type.value,
                "origin": origin.value,
                "topic": topic,
                "details": details,
            }
            self._mutations.append(entry)
            logger.info(f"Doctrine mutation: {mutation_type.value} on {topic} from {origin.value}")

    def get_mutations(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent mutations."""
        with self._lock:
            return list(self._mutations)[-limit:]


# ============================================================================
# TELEMETRY COLLECTOR
# ============================================================================

class TelemetryCollector:
    """Central telemetry collector for the healthcare law engine."""

    def __init__(self, log_dir: Path) -> None:
        self._log_dir = log_dir
        log_dir.mkdir(parents=True, exist_ok=True)

        self._metrics = MetricsAggregator()
        self._audit = AuditTrail(log_dir / "audit_trail.jsonl")
        self._errors = ErrorTracker()
        self._mutations = DoctrineMutationLog()

        self._active_traces: Dict[str, QueryTrace] = {}
        self._lock = threading.Lock()

        logger.info(f"TelemetryCollector initialized | log_dir={log_dir}")

    def start_trace(self, query: str, query_hash: str, response_mode: str = "fast") -> QueryTrace:
        """Start a new query trace."""
        trace_id = str(uuid.uuid4())
        trace = QueryTrace(
            trace_id=trace_id,
            query_text=query[:200],
            query_hash=query_hash,
            start_time=time.monotonic(),
            response_mode=response_mode,
        )
        with self._lock:
            self._active_traces[trace_id] = trace
        return trace

    def complete_trace(self, trace: QueryTrace) -> None:
        """Complete a trace and record metrics."""
        trace.complete()
        self._metrics.record_query(trace)
        self._audit.append("query_completed", trace.to_dict())
        with self._lock:
            self._active_traces.pop(trace.trace_id, None)

    def record_error(self, domain: ErrorDomain, error_msg: str, context: Optional[Dict[str, Any]] = None) -> None:
        """Record an error."""
        self._errors.record_error(domain, error_msg, context)
        self._audit.append("error", {"domain": domain.value, "error": error_msg, "context": context or {}})

    def record_hc_metric(self, metric_type: HealthcareMetricType) -> None:
        """Record a healthcare-specific metric."""
        self._metrics.record_hc_metric(metric_type)

    def record_citation_lookup(self, citation_type: CitationLookupType) -> None:
        """Record a citation lookup."""
        self._metrics.record_citation_lookup(citation_type)

    def record_doctrine_mutation(
        self,
        mutation_type: MutationType,
        origin: MutationOrigin,
        topic: str,
        details: Dict[str, Any],
    ) -> None:
        """Record a doctrine mutation."""
        self._mutations.record_mutation(mutation_type, origin, topic, details)
        self._audit.append("doctrine_mutation", {
            "mutation_type": mutation_type.value,
            "origin": origin.value,
            "topic": topic,
        })

    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get full metrics summary."""
        return {
            "query_metrics": self._metrics.get_summary(),
            "error_summary": self._errors.get_summary(),
            "audit_entries": self._audit.entry_count,
            "active_traces": len(self._active_traces),
            "recent_mutations": self._mutations.get_mutations(10),
        }


# ============================================================================
# MODULE-LEVEL FUNCTIONS
# ============================================================================

_TELEMETRY_INSTANCE: Optional[TelemetryCollector] = None


def get_telemetry(log_dir: Optional[Path] = None) -> TelemetryCollector:
    """Get or create the telemetry collector."""
    global _TELEMETRY_INSTANCE
    if _TELEMETRY_INSTANCE is None:
        if log_dir is None:
            log_dir = Path(__file__).parent / "logs"
        _TELEMETRY_INSTANCE = TelemetryCollector(log_dir)
    return _TELEMETRY_INSTANCE


def trace_query(query: str, query_hash: str, response_mode: str = "fast") -> QueryTrace:
    """Start a new query trace via the global telemetry collector."""
    telemetry = get_telemetry()
    return telemetry.start_trace(query, query_hash, response_mode)


def complete_trace(trace: QueryTrace) -> None:
    """Complete a trace via the global telemetry collector."""
    telemetry = get_telemetry()
    telemetry.complete_trace(trace)


def log_error(domain: ErrorDomain, error_msg: str, context: Optional[Dict[str, Any]] = None) -> None:
    """Log an error via the global telemetry collector."""
    telemetry = get_telemetry()
    telemetry.record_error(domain, error_msg, context)


def record_citation_lookup(citation_type: CitationLookupType) -> None:
    """Record a citation lookup via the global telemetry collector."""
    telemetry = get_telemetry()
    telemetry.record_citation_lookup(citation_type)


def record_doctrine_mutation(
    mutation_type: MutationType,
    origin: MutationOrigin,
    topic: str,
    details: Optional[Dict[str, Any]] = None,
) -> None:
    """Record a doctrine mutation via the global telemetry collector."""
    telemetry = get_telemetry()
    telemetry.record_doctrine_mutation(mutation_type, origin, topic, details or {})
