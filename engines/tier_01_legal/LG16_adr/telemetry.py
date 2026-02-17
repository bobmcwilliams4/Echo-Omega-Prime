"""
LG16 ADR Engine - Telemetry Module
======================================
Production telemetry, metrics collection, audit trail, and observability
for the ADR (Alternative Dispute Resolution) Engine.

Components:
    - TelemetryCollector: Ring-buffer based metric collection
    - QueryTrace: Per-query trace with timing breakdowns
    - AuditTrailWriter: Append-only JSONL audit log with SHA-256 chain
    - MetricsAggregator: Rolling window aggregation for dashboards
    - ErrorTracker: Domain-classified error tracking and alerting
    - DoctrineMutationLog: Track changes to doctrine cache
    - DriftWatcher: Monitor doctrine staleness and regulatory changes
    - ADRMetrics: ADR-specific metric types and counters

Port: 8406
Engine: LG16 ADR Engine
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
# ENUMS - RESPONSE LAYERS
# ============================================================================

class ResponseLayer(Enum):
    """Which processing layer produced the response."""
    DOCTRINE_CACHE = "doctrine_cache"
    SEMANTIC_SEARCH = "semantic_search"
    ADR_ANALYSIS = "adr_analysis"
    DEEP_ANALYSIS = "deep_analysis"
    FALLBACK = "fallback"
    ERROR = "error"


# ============================================================================
# ENUMS - ERROR DOMAINS
# ============================================================================

class ErrorDomain(Enum):
    """Classification of errors by domain."""
    ARBITRATION = "arbitration"
    MEDIATION = "mediation"
    NEGOTIATION = "negotiation"
    ENFORCEMENT = "enforcement"
    CLAUSE_DRAFTING = "clause_drafting"
    FAA = "faa"
    NY_CONVENTION = "ny_convention"
    ICSID = "icsid"
    CONSUMER = "consumer"
    EMPLOYMENT = "employment"
    SECURITIES = "securities"
    CONSTRUCTION = "construction"
    OIL_GAS = "oil_gas"
    INTERNATIONAL = "international"
    TEXAS_ADR = "texas_adr"
    SEARCH = "search"
    SEMANTIC = "semantic"
    SYSTEM = "system"
    VALIDATION = "validation"
    CONFIGURATION = "configuration"
    NETWORK = "network"
    STORAGE = "storage"


# ============================================================================
# ENUMS - MUTATION TYPES
# ============================================================================

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
    RULE_AMENDMENT = "rule_amendment"
    CASE_LAW_UPDATE = "case_law_update"


class MutationOrigin(Enum):
    """Where a doctrine mutation originated."""
    DRIFT_WATCHER = "drift_watcher"
    MANUAL_UPDATE = "manual_update"
    AUTOMATED_REFRESH = "automated_refresh"
    CASE_LAW_UPDATE = "case_law_update"
    LEGISLATIVE_CHANGE = "legislative_change"
    RULE_AMENDMENT = "rule_amendment"
    SCOTUS_DECISION = "scotus_decision"
    CIRCUIT_SPLIT = "circuit_split"
    INSTITUTIONAL_UPDATE = "institutional_update"
    AAA_RULE_CHANGE = "aaa_rule_change"
    ICC_RULE_CHANGE = "icc_rule_change"
    UNCITRAL_UPDATE = "uncitral_update"
    FINRA_RULE_CHANGE = "finra_rule_change"
    ADMIN_OVERRIDE = "admin_override"


# ============================================================================
# ENUMS - CITATION LOOKUP TYPES
# ============================================================================

class CitationLookupType(Enum):
    """Types of citation lookups tracked."""
    FEDERAL_STATUTE = "federal_statute"
    STATE_STATUTE = "state_statute"
    CASE_CITATION = "case_citation"
    CFR_REGULATION = "cfr_regulation"
    ARBITRATION_RULE = "arbitration_rule"
    TREATY = "treaty"
    MODEL_LAW = "model_law"
    INSTITUTIONAL_RULE = "institutional_rule"
    RESTATEMENT = "restatement"
    LAW_REVIEW = "law_review"


# ============================================================================
# ENUMS - ADR METRIC TYPES
# ============================================================================

class ADRMetricType(Enum):
    """ADR-specific metric categories."""
    ARBITRATION_QUERY = "arbitration_query"
    MEDIATION_QUERY = "mediation_query"
    NEGOTIATION_QUERY = "negotiation_query"
    ENFORCEMENT_QUERY = "enforcement_query"
    CLAUSE_REVIEW = "clause_review"
    PROCESS_DESIGN = "process_design"
    VACATUR_ANALYSIS = "vacatur_analysis"
    NY_CONVENTION_QUERY = "ny_convention_query"
    ICSID_QUERY = "icsid_query"
    CONSUMER_ARB_QUERY = "consumer_arb_query"
    EMPLOYMENT_ARB_QUERY = "employment_arb_query"
    SECURITIES_ARB_QUERY = "securities_arb_query"
    CONSTRUCTION_ARB_QUERY = "construction_arb_query"
    OIL_GAS_ARB_QUERY = "oil_gas_arb_query"
    TEXAS_ADR_QUERY = "texas_adr_query"
    INTERNATIONAL_ARB_QUERY = "international_arb_query"
    CLASS_ARBITRATION_QUERY = "class_arbitration_query"
    HYBRID_PROCESS_QUERY = "hybrid_process_query"
    DISPUTE_CLASSIFICATION = "dispute_classification"
    UNCONSCIONABILITY_CHECK = "unconscionability_check"
    AWARD_REVIEW = "award_review"
    RULES_SEARCH = "rules_search"


# ============================================================================
# ENUMS - DRIFT SEVERITY
# ============================================================================

class DriftSeverity(Enum):
    """Severity of doctrine drift signals."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


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
    adr_zone: Optional[str] = None

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
    adr_zone: Optional[str] = None
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

    def add_step(self, step_name: str, layer: ResponseLayer, adr_zone: Optional[str] = None) -> TelemetryStep:
        """Add a new step to the trace."""
        step = TelemetryStep(
            step_name=step_name,
            layer=layer,
            start_time=time.monotonic(),
            adr_zone=adr_zone,
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
            "adr_zone": self.adr_zone,
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
                    "adr_zone": s.adr_zone,
                    "error": s.error,
                    "metadata": s.metadata,
                }
                for s in self.steps
            ],
        }


# ============================================================================
# AUDIT TRAIL WRITER
# ============================================================================

class AuditTrailWriter:
    """Append-only JSONL audit log with SHA-256 hash chain."""

    def __init__(self, log_path: Path) -> None:
        self._log_path = log_path
        self._lock = threading.Lock()
        self._last_hash: str = "0" * 64
        self._entry_count: int = 0
        log_path.parent.mkdir(parents=True, exist_ok=True)
        self._recover_chain_state()
        logger.info(f"AuditTrailWriter initialized at {log_path} | entries={self._entry_count}")

    def _recover_chain_state(self) -> None:
        """Recover hash chain state from existing log file."""
        if not self._log_path.exists():
            return
        try:
            with open(self._log_path, "r", encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        entry = json.loads(line)
                        if "hash" in entry:
                            self._last_hash = entry["hash"]
                        self._entry_count += 1
                    except json.JSONDecodeError:
                        logger.warning(f"Skipping malformed audit entry at line {self._entry_count}")
        except OSError as exc:
            logger.warning(f"Failed to recover audit chain state: {exc}")

    def append(self, event_type: str, data: Dict[str, Any]) -> str:
        """Append an audit entry and return its hash."""
        with self._lock:
            entry = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "event_type": event_type,
                "engine_id": "LG16",
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

    def get_recent_entries(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get the most recent audit entries."""
        entries: List[Dict[str, Any]] = []
        if not self._log_path.exists():
            return entries
        try:
            with open(self._log_path, "r", encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if line:
                        try:
                            entries.append(json.loads(line))
                        except json.JSONDecodeError:
                            continue
        except OSError as exc:
            logger.warning(f"Failed to read audit entries: {exc}")
        return entries[-limit:]

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
        self._zone_counts: Counter = Counter()
        self._confidence_histogram: Counter = Counter()
        self._error_counts: Counter = Counter()
        self._citation_counts: Counter = Counter()
        self._adr_metric_counts: Counter = Counter()
        self._institution_counts: Counter = Counter()
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
            if trace.adr_zone:
                self._zone_counts[trace.adr_zone] += 1

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

    def record_adr_metric(self, metric_type: ADRMetricType) -> None:
        """Record an ADR-specific metric."""
        with self._lock:
            self._adr_metric_counts[metric_type.value] += 1

    def record_citation_lookup(self, citation_type: CitationLookupType) -> None:
        """Record a citation lookup."""
        with self._lock:
            self._citation_counts[citation_type.value] += 1

    def record_institution_query(self, institution: str) -> None:
        """Record a query related to a specific institution."""
        with self._lock:
            self._institution_counts[institution] += 1

    def get_summary(self) -> Dict[str, Any]:
        """Get aggregated metrics summary."""
        with self._lock:
            latency_list = list(self._latencies)
            if latency_list:
                sorted_lat = sorted(latency_list)
                avg_latency = sum(latency_list) / len(latency_list)
                p50 = sorted_lat[len(sorted_lat) // 2]
                p95 = sorted_lat[int(len(sorted_lat) * 0.95)] if len(sorted_lat) >= 20 else max(sorted_lat)
                p99 = sorted_lat[int(len(sorted_lat) * 0.99)] if len(sorted_lat) >= 100 else max(sorted_lat)
                min_lat = sorted_lat[0]
                max_lat = sorted_lat[-1]
            else:
                avg_latency = p50 = p95 = p99 = min_lat = max_lat = 0.0

            return {
                "total_queries": self._total_queries,
                "total_errors": self._total_errors,
                "error_rate": round(self._total_errors / max(self._total_queries, 1), 4),
                "latency_ms": {
                    "avg": round(avg_latency, 2),
                    "p50": round(p50, 2),
                    "p95": round(p95, 2),
                    "p99": round(p99, 2),
                    "min": round(min_lat, 2),
                    "max": round(max_lat, 2),
                },
                "layer_distribution": dict(self._layer_counts),
                "mode_distribution": dict(self._mode_counts),
                "zone_distribution": dict(self._zone_counts),
                "confidence_distribution": dict(self._confidence_histogram),
                "adr_metrics": dict(self._adr_metric_counts),
                "citation_lookups": dict(self._citation_counts),
                "institution_queries": dict(self._institution_counts),
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
        self._severity_counts: Counter = Counter()
        self._lock = threading.Lock()

    def record_error(
        self,
        domain: ErrorDomain,
        error_msg: str,
        severity: str = "MEDIUM",
        context: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Record an error with domain classification."""
        with self._lock:
            entry = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "domain": domain.value,
                "severity": severity,
                "error": error_msg,
                "context": context or {},
            }
            self._errors.append(entry)
            self._domain_counts[domain.value] += 1
            self._severity_counts[severity] += 1
            logger.error(f"[{domain.value}][{severity}] {error_msg}")

    def get_errors_by_domain(self, domain: ErrorDomain, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recent errors for a specific domain."""
        with self._lock:
            domain_errors = [e for e in self._errors if e["domain"] == domain.value]
            return domain_errors[-limit:]

    def get_summary(self) -> Dict[str, Any]:
        """Get error summary."""
        with self._lock:
            return {
                "total_errors": sum(self._domain_counts.values()),
                "by_domain": dict(self._domain_counts),
                "by_severity": dict(self._severity_counts),
                "recent_errors": list(self._errors)[-10:],
            }


# ============================================================================
# DOCTRINE MUTATION LOG
# ============================================================================

class DoctrineMutationLog:
    """Track mutations to the doctrine cache."""

    def __init__(self) -> None:
        self._mutations: deque = deque(maxlen=500)
        self._type_counts: Counter = Counter()
        self._origin_counts: Counter = Counter()
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
            self._type_counts[mutation_type.value] += 1
            self._origin_counts[origin.value] += 1
            logger.info(f"Doctrine mutation: {mutation_type.value} on {topic} from {origin.value}")

    def get_mutations(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent mutations."""
        with self._lock:
            return list(self._mutations)[-limit:]

    def get_mutation_stats(self) -> Dict[str, Any]:
        """Get mutation statistics."""
        with self._lock:
            return {
                "total_mutations": sum(self._type_counts.values()),
                "by_type": dict(self._type_counts),
                "by_origin": dict(self._origin_counts),
            }


# ============================================================================
# DRIFT WATCHER
# ============================================================================

class DriftWatcher:
    """Monitor doctrine staleness and track regulatory/case law changes."""

    def __init__(self, registry_path: Path) -> None:
        self._registry_path = registry_path
        self._signals: deque = deque(maxlen=200)
        self._lock = threading.Lock()
        self._staleness_thresholds: Dict[str, int] = {
            "case_law": 365,
            "statute": 730,
            "rule_amendment": 180,
            "guidance": 365,
            "model_law": 1095,
        }
        self._load_registry()
        logger.info(f"DriftWatcher initialized | registry={registry_path}")

    def _load_registry(self) -> None:
        """Load existing drift signals from registry."""
        if self._registry_path.exists():
            try:
                with open(self._registry_path, "r", encoding="utf-8") as fh:
                    data = json.load(fh)
                    for signal in data.get("signals", []):
                        self._signals.append(signal)
            except (json.JSONDecodeError, OSError) as exc:
                logger.warning(f"Failed to load drift registry: {exc}")

    def _save_registry(self) -> None:
        """Save drift signals to registry."""
        try:
            self._registry_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self._registry_path, "w", encoding="utf-8") as fh:
                json.dump({
                    "signals": list(self._signals),
                    "last_check": datetime.now(timezone.utc).isoformat(),
                    "engine_id": "LG16",
                }, fh, indent=2)
        except OSError as exc:
            logger.error(f"Failed to save drift registry: {exc}")

    def record_signal(
        self,
        signal_type: str,
        topic: str,
        description: str,
        severity: DriftSeverity,
        source: Optional[str] = None,
        confidence_impact: float = 0.0,
    ) -> Dict[str, Any]:
        """Record a doctrine drift signal."""
        with self._lock:
            signal = {
                "signal_id": str(uuid.uuid4()),
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "signal_type": signal_type,
                "topic": topic,
                "description": description,
                "severity": severity.value,
                "source": source,
                "confidence_impact": confidence_impact,
                "resolved": False,
            }
            self._signals.append(signal)
            self._save_registry()
            logger.warning(f"Drift signal [{severity.value}]: {topic} - {description}")
            return signal

    def resolve_signal(self, signal_id: str, resolution: str) -> bool:
        """Mark a drift signal as resolved."""
        with self._lock:
            for signal in self._signals:
                if signal.get("signal_id") == signal_id:
                    signal["resolved"] = True
                    signal["resolution"] = resolution
                    signal["resolved_at"] = datetime.now(timezone.utc).isoformat()
                    self._save_registry()
                    logger.info(f"Drift signal {signal_id} resolved: {resolution}")
                    return True
            return False

    def check_staleness(self, topic: str, last_updated: str, source_type: str) -> Optional[Dict[str, Any]]:
        """Check if a doctrine topic is stale based on last update time."""
        threshold = self._staleness_thresholds.get(source_type, 365)
        try:
            last_dt = datetime.fromisoformat(last_updated.replace("Z", "+00:00"))
            age_days = (datetime.now(timezone.utc) - last_dt).days
            if age_days > threshold:
                severity = DriftSeverity.HIGH if age_days > threshold * 2 else DriftSeverity.MEDIUM
                return self.record_signal(
                    signal_type="staleness",
                    topic=topic,
                    description=f"Doctrine {topic} last updated {age_days} days ago (threshold: {threshold})",
                    severity=severity,
                    confidence_impact=-0.1 if severity == DriftSeverity.MEDIUM else -0.2,
                )
        except (ValueError, TypeError) as exc:
            logger.warning(f"Could not parse date for staleness check: {exc}")
        return None

    def get_active_signals(self) -> List[Dict[str, Any]]:
        """Get unresolved drift signals."""
        with self._lock:
            return [s for s in self._signals if not s.get("resolved", False)]

    def get_all_signals(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get all drift signals."""
        with self._lock:
            return list(self._signals)[-limit:]

    def get_drift_summary(self) -> Dict[str, Any]:
        """Get drift summary statistics."""
        with self._lock:
            active = [s for s in self._signals if not s.get("resolved", False)]
            severity_counts: Counter = Counter()
            type_counts: Counter = Counter()
            for s in active:
                severity_counts[s.get("severity", "unknown")] += 1
                type_counts[s.get("signal_type", "unknown")] += 1
            return {
                "total_signals": len(self._signals),
                "active_signals": len(active),
                "resolved_signals": len(self._signals) - len(active),
                "by_severity": dict(severity_counts),
                "by_type": dict(type_counts),
            }


# ============================================================================
# TELEMETRY COLLECTOR
# ============================================================================

class TelemetryCollector:
    """Central telemetry collector for the ADR engine."""

    def __init__(self, log_dir: Path, drift_registry_path: Optional[Path] = None) -> None:
        self._log_dir = log_dir
        log_dir.mkdir(parents=True, exist_ok=True)

        self._metrics = MetricsAggregator()
        self._audit = AuditTrailWriter(log_dir / "audit_trail.jsonl")
        self._errors = ErrorTracker()
        self._mutations = DoctrineMutationLog()
        self._drift_watcher = DriftWatcher(
            drift_registry_path or (log_dir / "doctrine_drift_registry.json")
        )

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

    def record_error(self, domain: ErrorDomain, error_msg: str, severity: str = "MEDIUM", context: Optional[Dict[str, Any]] = None) -> None:
        """Record an error."""
        self._errors.record_error(domain, error_msg, severity, context)
        self._audit.append("error", {"domain": domain.value, "severity": severity, "error": error_msg, "context": context or {}})

    def record_adr_metric(self, metric_type: ADRMetricType) -> None:
        """Record an ADR-specific metric."""
        self._metrics.record_adr_metric(metric_type)

    def record_citation_lookup(self, citation_type: CitationLookupType) -> None:
        """Record a citation lookup."""
        self._metrics.record_citation_lookup(citation_type)

    def record_institution_query(self, institution: str) -> None:
        """Record a query related to a specific institution."""
        self._metrics.record_institution_query(institution)

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

    def record_drift_signal(
        self,
        signal_type: str,
        topic: str,
        description: str,
        severity: DriftSeverity,
        source: Optional[str] = None,
        confidence_impact: float = 0.0,
    ) -> Dict[str, Any]:
        """Record a drift signal through the drift watcher."""
        signal = self._drift_watcher.record_signal(signal_type, topic, description, severity, source, confidence_impact)
        self._audit.append("drift_signal", signal)
        return signal

    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get full metrics summary."""
        return {
            "query_metrics": self._metrics.get_summary(),
            "error_summary": self._errors.get_summary(),
            "audit_entries": self._audit.entry_count,
            "active_traces": len(self._active_traces),
            "recent_mutations": self._mutations.get_mutations(10),
            "mutation_stats": self._mutations.get_mutation_stats(),
            "drift_summary": self._drift_watcher.get_drift_summary(),
        }

    @property
    def audit(self) -> AuditTrailWriter:
        """Access the audit trail writer."""
        return self._audit

    @property
    def drift_watcher(self) -> DriftWatcher:
        """Access the drift watcher."""
        return self._drift_watcher


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


def log_error(domain: ErrorDomain, error_msg: str, severity: str = "MEDIUM", context: Optional[Dict[str, Any]] = None) -> None:
    """Log an error via the global telemetry collector."""
    telemetry = get_telemetry()
    telemetry.record_error(domain, error_msg, severity, context)


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


def record_drift_signal(
    signal_type: str,
    topic: str,
    description: str,
    severity: DriftSeverity,
    source: Optional[str] = None,
    confidence_impact: float = 0.0,
) -> Dict[str, Any]:
    """Record a drift signal via the global telemetry collector."""
    telemetry = get_telemetry()
    return telemetry.record_drift_signal(signal_type, topic, description, severity, source, confidence_impact)
