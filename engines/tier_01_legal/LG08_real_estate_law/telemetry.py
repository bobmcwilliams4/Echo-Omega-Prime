"""
LG08 Real Estate Law Engine - Telemetry Module
=================================================
Production telemetry, metrics collection, audit trail, and observability
for the Real Estate Law Engine.

Components:
    - TelemetryCollector: Ring-buffer based metric collection
    - QueryTrace: Per-query trace with timing breakdowns
    - AuditTrail: Append-only JSONL audit log with SHA-256 chain
    - MetricsAggregator: Rolling window aggregation for dashboards
    - ErrorTracker: Domain-classified error tracking and alerting
    - DoctrineMutationLog: Track changes to doctrine cache
    - RealEstateMetrics: Property/title/deed specific counters

Port: 8398
Engine: LG08 Real Estate Law
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
    REAL_ESTATE_ANALYSIS = "real_estate_analysis"
    DEEP_ANALYSIS = "deep_analysis"
    FALLBACK = "fallback"
    ERROR = "error"


class ErrorDomain(Enum):
    """Classification of errors by domain."""
    TITLE = "title"
    DEED = "deed"
    EASEMENT = "easement"
    ZONING = "zoning"
    LANDLORD_TENANT = "landlord_tenant"
    FINANCING = "financing"
    FORECLOSURE = "foreclosure"
    TAX = "tax"
    EMINENT_DOMAIN = "eminent_domain"
    HOA = "hoa"
    MINERAL_RIGHTS = "mineral_rights"
    TRANSACTION = "transaction"
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
    STATE_COURT_OPINION = "state_court_opinion"
    CFPB_GUIDANCE = "cfpb_guidance"
    HUD_POLICY = "hud_policy"
    LOCAL_ORDINANCE = "local_ordinance"
    ADMIN_OVERRIDE = "admin_override"


class CitationLookupType(Enum):
    """Types of citation lookups tracked."""
    STATE_STATUTE = "state_statute"
    FEDERAL_STATUTE = "federal_statute"
    CASE_CITATION = "case_citation"
    REGULATION = "regulation"
    LOCAL_ORDINANCE = "local_ordinance"
    RECORDING_REFERENCE = "recording_reference"
    TITLE_STANDARD = "title_standard"
    ALTA_FORM = "alta_form"
    RESTATEMENT = "restatement"
    PROPERTY_CODE = "property_code"


class RealEstateMetricType(Enum):
    """Real estate-specific metric categories."""
    TITLE_QUERY = "title_query"
    DEED_QUERY = "deed_query"
    EASEMENT_QUERY = "easement_query"
    ZONING_QUERY = "zoning_query"
    LANDLORD_TENANT_QUERY = "landlord_tenant_query"
    FINANCING_QUERY = "financing_query"
    FORECLOSURE_QUERY = "foreclosure_query"
    TAX_QUERY = "tax_query"
    EMINENT_DOMAIN_QUERY = "eminent_domain_query"
    HOA_QUERY = "hoa_query"
    MINERAL_RIGHTS_QUERY = "mineral_rights_query"
    EXCHANGE_1031_QUERY = "exchange_1031_query"
    COMPLIANCE_CHECK = "compliance_check"
    TRANSACTION_REVIEW = "transaction_review"
    TITLE_OPINION = "title_opinion"
    TEXAS_SPECIFIC = "texas_specific"


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
    re_category: Optional[str] = None

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
    re_category: Optional[str] = None
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

    def add_step(self, step_name: str, layer: ResponseLayer, re_category: Optional[str] = None) -> TelemetryStep:
        """Add a new step to the trace."""
        step = TelemetryStep(
            step_name=step_name,
            layer=layer,
            start_time=time.monotonic(),
            re_category=re_category,
        )
        self.steps.append(step)
        return step

    def complete(self, final_layer: ResponseLayer) -> None:
        """Mark query trace complete."""
        self.end_time = time.monotonic()
        self.total_duration_ms = (self.end_time - self.start_time) * 1000.0
        self.final_layer = final_layer
        for step in self.steps:
            if step.end_time == 0.0:
                step.complete()

    def to_dict(self) -> Dict[str, Any]:
        """Serialize trace to dictionary."""
        return {
            "trace_id": self.trace_id,
            "query_hash": self.query_hash,
            "start_time": self.start_time,
            "total_duration_ms": round(self.total_duration_ms, 3),
            "final_layer": self.final_layer.value if self.final_layer else None,
            "response_mode": self.response_mode,
            "re_category": self.re_category,
            "jurisdiction": self.jurisdiction,
            "confidence_score": round(self.confidence_score, 4),
            "confidence_band": self.confidence_band,
            "doctrine_hits": self.doctrine_hits,
            "search_results": self.search_results,
            "citations_found": self.citations_found,
            "error": self.error,
            "determinism_hash": self.determinism_hash,
            "steps": [
                {
                    "step_name": s.step_name,
                    "layer": s.layer.value,
                    "duration_ms": round(s.duration_ms, 3),
                    "re_category": s.re_category,
                    "error": s.error,
                    "metadata": s.metadata,
                }
                for s in self.steps
            ],
            "step_count": len(self.steps),
        }


# ============================================================================
# DOCTRINE MUTATION RECORD
# ============================================================================

@dataclass
class DoctrineMutationRecord:
    """Record of a doctrine cache mutation."""
    mutation_id: str
    timestamp: str
    mutation_type: MutationType
    origin: MutationOrigin
    doctrine_topic: str
    description: str
    old_confidence: Optional[float] = None
    new_confidence: Optional[float] = None
    affected_blocks: int = 0
    re_category: Optional[str] = None
    triggering_authority: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Serialize mutation record."""
        return {
            "mutation_id": self.mutation_id,
            "timestamp": self.timestamp,
            "mutation_type": self.mutation_type.value,
            "origin": self.origin.value,
            "doctrine_topic": self.doctrine_topic,
            "description": self.description,
            "old_confidence": self.old_confidence,
            "new_confidence": self.new_confidence,
            "affected_blocks": self.affected_blocks,
            "re_category": self.re_category,
            "triggering_authority": self.triggering_authority,
        }


# ============================================================================
# CITATION LOOKUP RECORD
# ============================================================================

@dataclass
class CitationLookupRecord:
    """Record of a citation lookup."""
    lookup_id: str
    timestamp: str
    lookup_type: CitationLookupType
    citation_text: str
    found: bool
    source: Optional[str] = None
    authority_weight: float = 0.0
    re_category: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Serialize citation lookup record."""
        return {
            "lookup_id": self.lookup_id,
            "timestamp": self.timestamp,
            "lookup_type": self.lookup_type.value,
            "citation_text": self.citation_text,
            "found": self.found,
            "source": self.source,
            "authority_weight": self.authority_weight,
            "re_category": self.re_category,
        }


# ============================================================================
# METRICS AGGREGATOR
# ============================================================================

class MetricsAggregator:
    """Rolling window metrics aggregation for dashboards."""

    def __init__(self, window_size: int = 1000) -> None:
        self._window_size: int = window_size
        self._latencies: deque[float] = deque(maxlen=window_size)
        self._layer_counts: Counter = Counter()
        self._mode_counts: Counter = Counter()
        self._re_category_counts: Counter = Counter()
        self._error_counts: Counter = Counter()
        self._confidence_scores: deque[float] = deque(maxlen=window_size)
        self._doctrine_hit_rate: deque[bool] = deque(maxlen=window_size)
        self._re_metric_counts: Counter = Counter()
        self._citation_counts: Counter = Counter()
        self._jurisdiction_counts: Counter = Counter()
        self._total_queries: int = 0
        self._total_errors: int = 0
        self._lock: threading.Lock = threading.Lock()

    def record_query(self, trace: QueryTrace) -> None:
        """Record a completed query trace into aggregations."""
        with self._lock:
            self._total_queries += 1
            self._latencies.append(trace.total_duration_ms)
            self._confidence_scores.append(trace.confidence_score)
            if trace.final_layer:
                self._layer_counts[trace.final_layer.value] += 1
            self._mode_counts[trace.response_mode] += 1
            if trace.re_category:
                self._re_category_counts[trace.re_category] += 1
            if trace.jurisdiction:
                self._jurisdiction_counts[trace.jurisdiction] += 1
            self._doctrine_hit_rate.append(trace.doctrine_hits > 0)
            if trace.error:
                self._total_errors += 1
                self._error_counts[trace.error[:50]] += 1

    def record_re_metric(self, metric_type: RealEstateMetricType) -> None:
        """Record a real estate-specific metric event."""
        with self._lock:
            self._re_metric_counts[metric_type.value] += 1

    def record_citation_lookup(self, lookup_type: CitationLookupType, found: bool) -> None:
        """Record a citation lookup event."""
        with self._lock:
            key = f"{lookup_type.value}_{'hit' if found else 'miss'}"
            self._citation_counts[key] += 1

    def get_snapshot(self) -> Dict[str, Any]:
        """Get a point-in-time metrics snapshot."""
        with self._lock:
            latencies = list(self._latencies)
            confidences = list(self._confidence_scores)
            hits = list(self._doctrine_hit_rate)

        p50 = self._percentile(latencies, 50) if latencies else 0.0
        p95 = self._percentile(latencies, 95) if latencies else 0.0
        p99 = self._percentile(latencies, 99) if latencies else 0.0
        avg_latency = sum(latencies) / len(latencies) if latencies else 0.0
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
        hit_rate = sum(1 for h in hits if h) / len(hits) if hits else 0.0

        return {
            "total_queries": self._total_queries,
            "total_errors": self._total_errors,
            "error_rate": round(self._total_errors / max(self._total_queries, 1), 4),
            "latency": {
                "p50_ms": round(p50, 3),
                "p95_ms": round(p95, 3),
                "p99_ms": round(p99, 3),
                "avg_ms": round(avg_latency, 3),
                "min_ms": round(min(latencies), 3) if latencies else 0.0,
                "max_ms": round(max(latencies), 3) if latencies else 0.0,
            },
            "confidence": {
                "avg": round(avg_confidence, 4),
                "min": round(min(confidences), 4) if confidences else 0.0,
                "max": round(max(confidences), 4) if confidences else 0.0,
            },
            "doctrine_hit_rate": round(hit_rate, 4),
            "layer_distribution": dict(self._layer_counts),
            "mode_distribution": dict(self._mode_counts),
            "re_category_distribution": dict(self._re_category_counts),
            "jurisdiction_distribution": dict(self._jurisdiction_counts),
            "re_metrics": dict(self._re_metric_counts),
            "citation_lookups": dict(self._citation_counts),
            "error_distribution": dict(self._error_counts.most_common(10)),
            "window_size": self._window_size,
            "samples_in_window": len(latencies),
        }

    @staticmethod
    def _percentile(data: List[float], pct: int) -> float:
        """Calculate percentile from sorted data."""
        if not data:
            return 0.0
        sorted_data = sorted(data)
        idx = (pct / 100.0) * (len(sorted_data) - 1)
        lower = int(math.floor(idx))
        upper = int(math.ceil(idx))
        if lower == upper:
            return sorted_data[lower]
        frac = idx - lower
        return sorted_data[lower] * (1.0 - frac) + sorted_data[upper] * frac


# ============================================================================
# AUDIT TRAIL
# ============================================================================

class AuditTrail:
    """Append-only JSONL audit log with SHA-256 hash chain."""

    def __init__(self, log_path: Path) -> None:
        self._log_path: Path = log_path
        self._log_path.parent.mkdir(parents=True, exist_ok=True)
        self._lock: threading.Lock = threading.Lock()
        self._last_hash: str = "GENESIS"
        self._entry_count: int = 0
        self._recover_chain_state()

    def _recover_chain_state(self) -> None:
        """Recover the last hash from existing audit log."""
        if not self._log_path.exists():
            return
        try:
            last_line = ""
            with open(self._log_path, "r", encoding="utf-8") as fh:
                for line in fh:
                    stripped = line.strip()
                    if stripped:
                        last_line = stripped
                        self._entry_count += 1
            if last_line:
                entry = json.loads(last_line)
                self._last_hash = entry.get("chain_hash", "GENESIS")
        except (json.JSONDecodeError, OSError) as exc:
            logger.warning(f"Audit trail recovery failed: {exc}. Starting fresh chain.")
            self._last_hash = "GENESIS"

    def append(self, event_type: str, data: Dict[str, Any]) -> str:
        """Append an audit entry and return its chain hash."""
        with self._lock:
            timestamp = datetime.now(timezone.utc).isoformat()
            entry_id = str(uuid.uuid4())
            chain_input = f"{self._last_hash}|{timestamp}|{event_type}|{json.dumps(data, sort_keys=True)}"
            chain_hash = hashlib.sha256(chain_input.encode("utf-8")).hexdigest()

            entry = {
                "entry_id": entry_id,
                "timestamp": timestamp,
                "event_type": event_type,
                "data": data,
                "prev_hash": self._last_hash,
                "chain_hash": chain_hash,
                "sequence": self._entry_count,
            }

            try:
                with open(self._log_path, "a", encoding="utf-8") as fh:
                    fh.write(json.dumps(entry, separators=(",", ":")) + "\n")
                self._last_hash = chain_hash
                self._entry_count += 1
            except OSError as exc:
                logger.error(f"Audit trail write failed: {exc}")

            return chain_hash

    def verify_chain(self, max_entries: int = 1000) -> Tuple[bool, int, int]:
        """Verify the hash chain integrity. Returns (valid, verified, total)."""
        if not self._log_path.exists():
            return True, 0, 0

        verified = 0
        total = 0
        prev_hash = "GENESIS"

        try:
            with open(self._log_path, "r", encoding="utf-8") as fh:
                for line in fh:
                    stripped = line.strip()
                    if not stripped:
                        continue
                    total += 1
                    if total > max_entries:
                        break

                    entry = json.loads(stripped)
                    stored_prev = entry.get("prev_hash", "")
                    if stored_prev != prev_hash:
                        logger.error(f"Chain break at entry {total}: expected {prev_hash}, got {stored_prev}")
                        return False, verified, total

                    chain_input = (
                        f"{entry['prev_hash']}|{entry['timestamp']}|"
                        f"{entry['event_type']}|{json.dumps(entry['data'], sort_keys=True)}"
                    )
                    computed = hashlib.sha256(chain_input.encode("utf-8")).hexdigest()
                    if computed != entry.get("chain_hash", ""):
                        logger.error(f"Hash mismatch at entry {total}")
                        return False, verified, total

                    prev_hash = entry["chain_hash"]
                    verified += 1
        except (json.JSONDecodeError, OSError) as exc:
            logger.error(f"Chain verification error: {exc}")
            return False, verified, total

        return True, verified, total

    def get_stats(self) -> Dict[str, Any]:
        """Get audit trail statistics."""
        return {
            "log_path": str(self._log_path),
            "entry_count": self._entry_count,
            "last_hash": self._last_hash[:16] + "...",
            "exists": self._log_path.exists(),
            "size_bytes": self._log_path.stat().st_size if self._log_path.exists() else 0,
        }


# ============================================================================
# ERROR TRACKER
# ============================================================================

class ErrorTracker:
    """Domain-classified error tracking with rate detection."""

    def __init__(self, window_size: int = 500) -> None:
        self._errors: deque[Dict[str, Any]] = deque(maxlen=window_size)
        self._domain_counts: Counter = Counter()
        self._total_errors: int = 0
        self._lock: threading.Lock = threading.Lock()

    def record(self, domain: ErrorDomain, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Record an error and return its ID."""
        error_id = str(uuid.uuid4())
        with self._lock:
            self._total_errors += 1
            self._domain_counts[domain.value] += 1
            self._errors.append({
                "error_id": error_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "domain": domain.value,
                "message": message,
                "context": context or {},
            })
        return error_id

    def get_recent(self, count: int = 20) -> List[Dict[str, Any]]:
        """Get recent errors."""
        with self._lock:
            return list(self._errors)[-count:]

    def get_error_rate(self, total_queries: int) -> float:
        """Calculate error rate."""
        if total_queries == 0:
            return 0.0
        return self._total_errors / total_queries

    def get_stats(self) -> Dict[str, Any]:
        """Get error tracking statistics."""
        with self._lock:
            return {
                "total_errors": self._total_errors,
                "domain_distribution": dict(self._domain_counts),
                "recent_count": len(self._errors),
                "top_domains": dict(self._domain_counts.most_common(5)),
            }


# ============================================================================
# TELEMETRY COLLECTOR (Main Singleton)
# ============================================================================

class TelemetryCollector:
    """Central telemetry collector for the LG08 Real Estate Law Engine.

    Combines query tracing, metrics aggregation, audit trail,
    error tracking, and real estate-specific metric collection.
    """

    _instance: ClassVar[Optional["TelemetryCollector"]] = None
    _init_lock: ClassVar[threading.Lock] = threading.Lock()

    def __init__(self, log_dir: Optional[Path] = None) -> None:
        base_dir = log_dir or Path("O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/LG08_real_estate_law/logs")
        base_dir.mkdir(parents=True, exist_ok=True)

        self._log_dir: Path = base_dir
        self._metrics: MetricsAggregator = MetricsAggregator(window_size=10000)
        self._audit: AuditTrail = AuditTrail(base_dir / "audit_trail.jsonl")
        self._errors: ErrorTracker = ErrorTracker(window_size=500)
        self._active_traces: Dict[str, QueryTrace] = {}
        self._trace_history: deque[QueryTrace] = deque(maxlen=1000)
        self._mutation_log: deque[DoctrineMutationRecord] = deque(maxlen=500)
        self._citation_log: deque[CitationLookupRecord] = deque(maxlen=1000)
        self._lock: threading.Lock = threading.Lock()
        self._start_time: float = time.monotonic()
        self._boot_timestamp: str = datetime.now(timezone.utc).isoformat()

        logger.info(f"TelemetryCollector initialized | log_dir={base_dir}")

    @classmethod
    def get_instance(cls, log_dir: Optional[Path] = None) -> "TelemetryCollector":
        """Get or create the singleton instance."""
        if cls._instance is None:
            with cls._init_lock:
                if cls._instance is None:
                    cls._instance = cls(log_dir=log_dir)
        return cls._instance

    @classmethod
    def reset_instance(cls) -> None:
        """Reset the singleton (for testing)."""
        with cls._init_lock:
            cls._instance = None

    def start_trace(self, query_text: str, query_hash: str, response_mode: str = "fast") -> QueryTrace:
        """Start a new query trace."""
        trace = QueryTrace(
            trace_id=str(uuid.uuid4()),
            query_text=query_text[:200],
            query_hash=query_hash,
            start_time=time.monotonic(),
            response_mode=response_mode,
        )
        with self._lock:
            self._active_traces[trace.trace_id] = trace
        return trace

    def complete_trace(self, trace: QueryTrace, final_layer: ResponseLayer) -> None:
        """Complete a query trace and record metrics."""
        trace.complete(final_layer)
        with self._lock:
            self._active_traces.pop(trace.trace_id, None)
            self._trace_history.append(trace)
        self._metrics.record_query(trace)
        self._audit.append("query_complete", trace.to_dict())

    def record_error(self, domain: ErrorDomain, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Record an error event."""
        error_id = self._errors.record(domain, message, context)
        self._audit.append("error", {
            "error_id": error_id,
            "domain": domain.value,
            "message": message[:500],
        })
        logger.error(f"[{domain.value}] {message}")
        return error_id

    def record_doctrine_mutation(
        self,
        mutation_type: MutationType,
        origin: MutationOrigin,
        topic: str,
        description: str,
        old_confidence: Optional[float] = None,
        new_confidence: Optional[float] = None,
        affected_blocks: int = 0,
        re_category: Optional[str] = None,
        triggering_authority: Optional[str] = None,
    ) -> str:
        """Record a doctrine mutation event."""
        record = DoctrineMutationRecord(
            mutation_id=str(uuid.uuid4()),
            timestamp=datetime.now(timezone.utc).isoformat(),
            mutation_type=mutation_type,
            origin=origin,
            doctrine_topic=topic,
            description=description,
            old_confidence=old_confidence,
            new_confidence=new_confidence,
            affected_blocks=affected_blocks,
            re_category=re_category,
            triggering_authority=triggering_authority,
        )
        with self._lock:
            self._mutation_log.append(record)
        self._audit.append("doctrine_mutation", record.to_dict())
        return record.mutation_id

    def record_citation_lookup(
        self,
        lookup_type: CitationLookupType,
        citation_text: str,
        found: bool,
        source: Optional[str] = None,
        authority_weight: float = 0.0,
        re_category: Optional[str] = None,
    ) -> str:
        """Record a citation lookup event."""
        record = CitationLookupRecord(
            lookup_id=str(uuid.uuid4()),
            timestamp=datetime.now(timezone.utc).isoformat(),
            lookup_type=lookup_type,
            citation_text=citation_text[:200],
            found=found,
            source=source,
            authority_weight=authority_weight,
            re_category=re_category,
        )
        with self._lock:
            self._citation_log.append(record)
        self._metrics.record_citation_lookup(lookup_type, found)
        return record.lookup_id

    def record_re_metric(self, metric_type: RealEstateMetricType) -> None:
        """Record a real estate-specific metric event."""
        self._metrics.record_re_metric(metric_type)

    def get_health(self) -> Dict[str, Any]:
        """Get telemetry health summary."""
        uptime = time.monotonic() - self._start_time
        metrics_snap = self._metrics.get_snapshot()
        audit_stats = self._audit.get_stats()
        error_stats = self._errors.get_stats()

        return {
            "status": "healthy",
            "engine_id": "LG08",
            "engine_name": "Real Estate Law",
            "uptime_seconds": round(uptime, 2),
            "boot_timestamp": self._boot_timestamp,
            "metrics": metrics_snap,
            "audit": audit_stats,
            "errors": error_stats,
            "active_traces": len(self._active_traces),
            "trace_history_size": len(self._trace_history),
            "mutation_log_size": len(self._mutation_log),
            "citation_log_size": len(self._citation_log),
        }

    def get_recent_traces(self, count: int = 20) -> List[Dict[str, Any]]:
        """Get recent query traces."""
        with self._lock:
            recent = list(self._trace_history)[-count:]
        return [t.to_dict() for t in recent]

    def get_recent_mutations(self, count: int = 20) -> List[Dict[str, Any]]:
        """Get recent doctrine mutations."""
        with self._lock:
            recent = list(self._mutation_log)[-count:]
        return [m.to_dict() for m in recent]

    def get_recent_citations(self, count: int = 20) -> List[Dict[str, Any]]:
        """Get recent citation lookups."""
        with self._lock:
            recent = list(self._citation_log)[-count:]
        return [c.to_dict() for c in recent]

    def verify_audit_chain(self) -> Dict[str, Any]:
        """Verify the audit trail hash chain integrity."""
        valid, verified, total = self._audit.verify_chain()
        return {
            "chain_valid": valid,
            "entries_verified": verified,
            "entries_total": total,
        }


# ============================================================================
# MODULE-LEVEL CONVENIENCE FUNCTIONS
# ============================================================================

_collector: Optional[TelemetryCollector] = None


def get_telemetry(log_dir: Optional[Path] = None) -> TelemetryCollector:
    """Get the global telemetry collector instance."""
    global _collector
    if _collector is None:
        _collector = TelemetryCollector.get_instance(log_dir=log_dir)
    return _collector


def trace_query(query_text: str, query_hash: str, response_mode: str = "fast") -> QueryTrace:
    """Start tracing a query."""
    return get_telemetry().start_trace(query_text, query_hash, response_mode)


def complete_trace(trace: QueryTrace, final_layer: ResponseLayer) -> None:
    """Complete a query trace."""
    get_telemetry().complete_trace(trace, final_layer)


def log_error(domain: ErrorDomain, message: str, context: Optional[Dict[str, Any]] = None) -> str:
    """Log an error through telemetry."""
    return get_telemetry().record_error(domain, message, context)


def record_doctrine_mutation(
    mutation_type: MutationType,
    origin: MutationOrigin,
    topic: str,
    description: str,
    old_confidence: Optional[float] = None,
    new_confidence: Optional[float] = None,
    affected_blocks: int = 0,
    re_category: Optional[str] = None,
    triggering_authority: Optional[str] = None,
) -> str:
    """Record a doctrine mutation through telemetry."""
    return get_telemetry().record_doctrine_mutation(
        mutation_type=mutation_type,
        origin=origin,
        topic=topic,
        description=description,
        old_confidence=old_confidence,
        new_confidence=new_confidence,
        affected_blocks=affected_blocks,
        re_category=re_category,
        triggering_authority=triggering_authority,
    )


def record_citation_lookup(
    lookup_type: CitationLookupType,
    citation_text: str,
    found: bool,
    source: Optional[str] = None,
    authority_weight: float = 0.0,
    re_category: Optional[str] = None,
) -> str:
    """Record a citation lookup through telemetry."""
    return get_telemetry().record_citation_lookup(
        lookup_type=lookup_type,
        citation_text=citation_text,
        found=found,
        source=source,
        authority_weight=authority_weight,
        re_category=re_category,
    )
