"""
LG13 Environmental Law Engine - Telemetry Module
==================================================
Production telemetry, metrics collection, audit trail, and observability
for the Environmental Law Engine.

Components:
    - TelemetryCollector: Ring-buffer based metric collection
    - QueryTrace: Per-query trace with timing breakdowns
    - AuditTrail: Append-only JSONL audit log with SHA-256 chain
    - MetricsAggregator: Rolling window aggregation for dashboards
    - ErrorTracker: Domain-classified error tracking and alerting
    - DoctrineMutationLog: Track changes to doctrine cache
    - EnvironmentalMetrics: Permit/compliance/contamination-specific counters

Port: 8403
Engine: LG13 Environmental Law
Version: 1.0.0
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
    ENVIRONMENTAL_ANALYSIS = "environmental_analysis"
    DEEP_ANALYSIS = "deep_analysis"
    FALLBACK = "fallback"
    ERROR = "error"


class ErrorDomain(Enum):
    """Classification of errors by environmental domain."""
    NEPA = "nepa"
    CAA = "caa"
    CWA = "cwa"
    RCRA = "rcra"
    CERCLA = "cercla"
    TSCA = "tsca"
    ESA = "esa"
    FIFRA = "fifra"
    SDWA = "sdwa"
    OPA = "opa"
    EPCRA = "epcra"
    TCEQ = "tceq"
    RRC = "rrc"
    PERMIT = "permit"
    CONTAMINATION = "contamination"
    REMEDIATION = "remediation"
    COMPLIANCE = "compliance"
    CARBON = "carbon"
    CITIZEN_SUIT = "citizen_suit"
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
    CATEGORY_ADDED = "category_added"
    INTEGRITY_REPAIRED = "integrity_repaired"
    REGULATION_UPDATED = "regulation_updated"
    PERMIT_THRESHOLD_CHANGED = "permit_threshold_changed"


class MutationOrigin(Enum):
    """Where the mutation came from."""
    STARTUP_INIT = "startup_init"
    RUNTIME_UPDATE = "runtime_update"
    ADMIN_OVERRIDE = "admin_override"
    DRIFT_REPAIR = "drift_repair"
    AUTO_HEAL = "auto_heal"
    REGULATION_SYNC = "regulation_sync"
    EXTERNAL_FEED = "external_feed"


class AlertSeverity(Enum):
    """Alert severity levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


# ============================================================================
# QUERY TRACE
# ============================================================================

@dataclass
class QueryTrace:
    """Per-query trace object with timing breakdowns."""
    trace_id: str = dc_field(default_factory=lambda: str(uuid.uuid4()))
    query_hash: str = ""
    query_text: str = ""
    start_time: float = dc_field(default_factory=time.time)
    end_time: Optional[float] = None
    total_ms: float = 0.0
    layer_hit: ResponseLayer = ResponseLayer.FALLBACK
    doctrine_topic: str = ""
    environmental_domain: str = ""
    jurisdiction: str = ""
    permit_type: str = ""
    statute_referenced: str = ""
    confidence: float = 0.0
    token_count_in: int = 0
    token_count_out: int = 0
    response_mode: str = "HYBRID"
    analysis_layer: str = "STANDARD"
    semantic_normalized: bool = False
    normalization_mapping: Dict[str, str] = dc_field(default_factory=dict)
    search_results_count: int = 0
    doctrine_blocks_checked: int = 0
    doctrine_blocks_matched: int = 0
    error_message: Optional[str] = None
    error_domain: Optional[ErrorDomain] = None
    sub_traces: List[Dict[str, Any]] = dc_field(default_factory=list)
    metadata: Dict[str, Any] = dc_field(default_factory=dict)

    def complete(self, layer: ResponseLayer, confidence: float) -> None:
        """Finalize trace."""
        self.end_time = time.time()
        self.total_ms = (self.end_time - self.start_time) * 1000
        self.layer_hit = layer
        self.confidence = confidence

    def add_sub_trace(self, name: str, duration_ms: float, details: Optional[Dict[str, Any]] = None) -> None:
        """Add sub-trace for component timing."""
        entry: Dict[str, Any] = {"name": name, "duration_ms": round(duration_ms, 3)}
        if details:
            entry["details"] = details
        self.sub_traces.append(entry)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "trace_id": self.trace_id,
            "query_hash": self.query_hash,
            "query_text": self.query_text[:200],
            "start_time": self.start_time,
            "end_time": self.end_time,
            "total_ms": round(self.total_ms, 3),
            "layer_hit": self.layer_hit.value,
            "doctrine_topic": self.doctrine_topic,
            "environmental_domain": self.environmental_domain,
            "jurisdiction": self.jurisdiction,
            "permit_type": self.permit_type,
            "statute_referenced": self.statute_referenced,
            "confidence": round(self.confidence, 4),
            "token_count_in": self.token_count_in,
            "token_count_out": self.token_count_out,
            "response_mode": self.response_mode,
            "analysis_layer": self.analysis_layer,
            "semantic_normalized": self.semantic_normalized,
            "normalization_mapping": self.normalization_mapping,
            "search_results_count": self.search_results_count,
            "doctrine_blocks_checked": self.doctrine_blocks_checked,
            "doctrine_blocks_matched": self.doctrine_blocks_matched,
            "error_message": self.error_message,
            "error_domain": self.error_domain.value if self.error_domain else None,
            "sub_traces": self.sub_traces,
            "metadata": self.metadata,
        }


# ============================================================================
# AUDIT TRAIL - Append-only JSONL with SHA-256 chain
# ============================================================================

class AuditTrail:
    """Append-only JSONL audit log with SHA-256 hash chain for tamper detection."""

    def __init__(self, log_path: Path, max_size_mb: int = 500) -> None:
        self._log_path = log_path
        self._max_size_bytes = max_size_mb * 1024 * 1024
        self._last_hash: str = "GENESIS"
        self._entry_count: int = 0
        self._lock = threading.Lock()
        self._log_path.parent.mkdir(parents=True, exist_ok=True)
        self._recover_chain_state()

    def _recover_chain_state(self) -> None:
        """Recover last hash from existing log file."""
        if not self._log_path.exists():
            return
        last_line = ""
        try:
            with self._log_path.open("r", encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if line:
                        last_line = line
                        self._entry_count += 1
            if last_line:
                record = json.loads(last_line)
                self._last_hash = record.get("chain_hash", self._last_hash)
        except (json.JSONDecodeError, OSError) as exc:
            logger.warning(f"Audit chain recovery partial: {exc}")

    def _compute_chain_hash(self, payload: str) -> str:
        """Compute next hash in the chain."""
        data = f"{self._last_hash}:{payload}"
        return hashlib.sha256(data.encode("utf-8")).hexdigest()

    def _rotate_if_needed(self) -> None:
        """Rotate log if it exceeds max size."""
        if not self._log_path.exists():
            return
        size = self._log_path.stat().st_size
        if size > self._max_size_bytes:
            archive_name = self._log_path.stem + f"_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}" + self._log_path.suffix
            archive_path = self._log_path.parent / archive_name
            self._log_path.rename(archive_path)
            self._entry_count = 0
            logger.info(f"Audit log rotated to {archive_path}")

    def record(self, event_type: str, details: Dict[str, Any], severity: AlertSeverity = AlertSeverity.INFO) -> str:
        """Append audit record with chained hash."""
        with self._lock:
            self._rotate_if_needed()
            timestamp = datetime.now(timezone.utc).isoformat()
            entry_id = str(uuid.uuid4())
            payload = json.dumps({"t": timestamp, "e": event_type, "d": details}, sort_keys=True)
            chain_hash = self._compute_chain_hash(payload)
            record = {
                "entry_id": entry_id,
                "timestamp": timestamp,
                "event_type": event_type,
                "severity": severity.value,
                "details": details,
                "chain_hash": chain_hash,
                "entry_number": self._entry_count,
            }
            line = json.dumps(record, separators=(",", ":"))
            with self._log_path.open("a", encoding="utf-8") as fh:
                fh.write(line + "\n")
            self._last_hash = chain_hash
            self._entry_count += 1
            return entry_id

    def verify_chain(self, max_entries: int = 10000) -> Tuple[bool, int, Optional[str]]:
        """Verify the hash chain integrity."""
        if not self._log_path.exists():
            return True, 0, None
        prev_hash = "GENESIS"
        count = 0
        try:
            with self._log_path.open("r", encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    if count >= max_entries:
                        break
                    record = json.loads(line)
                    stored_hash = record.get("chain_hash", "")
                    payload = json.dumps({
                        "t": record["timestamp"],
                        "e": record["event_type"],
                        "d": record["details"],
                    }, sort_keys=True)
                    expected_hash = hashlib.sha256(f"{prev_hash}:{payload}".encode("utf-8")).hexdigest()
                    if expected_hash != stored_hash:
                        return False, count, f"Chain break at entry {count}: expected {expected_hash[:16]}... got {stored_hash[:16]}..."
                    prev_hash = stored_hash
                    count += 1
        except (json.JSONDecodeError, OSError) as exc:
            return False, count, f"Parse error at entry {count}: {exc}"
        return True, count, None

    @property
    def entry_count(self) -> int:
        """Return the number of entries."""
        return self._entry_count

    @property
    def last_hash(self) -> str:
        """Return the last hash in the chain."""
        return self._last_hash


# ============================================================================
# METRICS AGGREGATOR
# ============================================================================

class MetricsAggregator:
    """Rolling-window metrics aggregation for dashboards."""

    def __init__(self, window_size: int = 1000, retention_hours: int = 168) -> None:
        self._window_size = window_size
        self._retention_seconds = retention_hours * 3600
        self._latencies: deque[float] = deque(maxlen=window_size)
        self._timestamps: deque[float] = deque(maxlen=window_size)
        self._layers: Counter = Counter()
        self._domains: Counter = Counter()
        self._statutes: Counter = Counter()
        self._permit_types: Counter = Counter()
        self._jurisdictions: Counter = Counter()
        self._confidence_buckets: Counter = Counter()
        self._error_count: int = 0
        self._total_queries: int = 0
        self._lock = threading.Lock()

    def record_trace(self, trace: QueryTrace) -> None:
        """Record a completed trace."""
        with self._lock:
            now = time.time()
            self._latencies.append(trace.total_ms)
            self._timestamps.append(now)
            self._layers[trace.layer_hit.value] += 1
            if trace.environmental_domain:
                self._domains[trace.environmental_domain] += 1
            if trace.statute_referenced:
                self._statutes[trace.statute_referenced] += 1
            if trace.permit_type:
                self._permit_types[trace.permit_type] += 1
            if trace.jurisdiction:
                self._jurisdictions[trace.jurisdiction] += 1
            if trace.confidence >= 0.85:
                self._confidence_buckets["high"] += 1
            elif trace.confidence >= 0.65:
                self._confidence_buckets["medium"] += 1
            elif trace.confidence >= 0.40:
                self._confidence_buckets["low"] += 1
            else:
                self._confidence_buckets["uncertain"] += 1
            if trace.error_message:
                self._error_count += 1
            self._total_queries += 1

    def get_stats(self) -> Dict[str, Any]:
        """Get aggregated statistics."""
        with self._lock:
            lats = list(self._latencies)
            if lats:
                sorted_lats = sorted(lats)
                n = len(sorted_lats)
                p50 = sorted_lats[int(n * 0.50)]
                p90 = sorted_lats[int(min(n * 0.90, n - 1))]
                p99 = sorted_lats[int(min(n * 0.99, n - 1))]
                avg_latency = sum(sorted_lats) / n
                min_latency = sorted_lats[0]
                max_latency = sorted_lats[-1]
                std_dev = math.sqrt(sum((x - avg_latency) ** 2 for x in sorted_lats) / n) if n > 1 else 0.0
            else:
                p50 = p90 = p99 = avg_latency = min_latency = max_latency = std_dev = 0.0
            now = time.time()
            recent_1m = sum(1 for t in self._timestamps if now - t < 60)
            recent_5m = sum(1 for t in self._timestamps if now - t < 300)
            recent_1h = sum(1 for t in self._timestamps if now - t < 3600)
            return {
                "total_queries": self._total_queries,
                "error_count": self._error_count,
                "error_rate": round(self._error_count / max(self._total_queries, 1), 4),
                "latency_ms": {
                    "avg": round(avg_latency, 2),
                    "p50": round(p50, 2),
                    "p90": round(p90, 2),
                    "p99": round(p99, 2),
                    "min": round(min_latency, 2),
                    "max": round(max_latency, 2),
                    "std_dev": round(std_dev, 2),
                },
                "throughput": {
                    "last_1m": recent_1m,
                    "last_5m": recent_5m,
                    "last_1h": recent_1h,
                },
                "layer_distribution": dict(self._layers),
                "environmental_domain_distribution": dict(self._domains.most_common(20)),
                "statute_distribution": dict(self._statutes.most_common(15)),
                "permit_type_distribution": dict(self._permit_types.most_common(10)),
                "jurisdiction_distribution": dict(self._jurisdictions.most_common(10)),
                "confidence_distribution": dict(self._confidence_buckets),
            }

    def reset(self) -> None:
        """Reset all metrics."""
        with self._lock:
            self._latencies.clear()
            self._timestamps.clear()
            self._layers.clear()
            self._domains.clear()
            self._statutes.clear()
            self._permit_types.clear()
            self._jurisdictions.clear()
            self._confidence_buckets.clear()
            self._error_count = 0
            self._total_queries = 0


# ============================================================================
# ERROR TRACKER
# ============================================================================

class ErrorTracker:
    """Domain-classified error tracking with trending and alerting."""

    def __init__(self, max_recent: int = 200) -> None:
        self._recent: deque[Dict[str, Any]] = deque(maxlen=max_recent)
        self._domain_counts: Counter = Counter()
        self._total: int = 0
        self._lock = threading.Lock()

    def record_error(self, domain: ErrorDomain, message: str, trace_id: str = "", details: Optional[Dict[str, Any]] = None) -> None:
        """Record an error event."""
        with self._lock:
            entry = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "domain": domain.value,
                "message": message[:500],
                "trace_id": trace_id,
                "details": details or {},
            }
            self._recent.append(entry)
            self._domain_counts[domain.value] += 1
            self._total += 1
            logger.error(f"[{domain.value}] {message[:200]} (trace={trace_id[:12]})")

    def get_summary(self) -> Dict[str, Any]:
        """Get error tracking summary."""
        with self._lock:
            return {
                "total_errors": self._total,
                "by_domain": dict(self._domain_counts.most_common(20)),
                "recent_errors": list(self._recent)[-10:],
            }

    def get_trending(self, window_seconds: int = 300) -> List[Tuple[str, int]]:
        """Get errors trending in the last N seconds."""
        with self._lock:
            cutoff_str = datetime.now(timezone.utc).isoformat()
            cutoff_ts = time.time() - window_seconds
            trending: Counter = Counter()
            for entry in self._recent:
                try:
                    ts = datetime.fromisoformat(entry["timestamp"]).timestamp()
                    if ts > cutoff_ts:
                        trending[entry["domain"]] += 1
                except (ValueError, KeyError):
                    continue
            return trending.most_common(10)


# ============================================================================
# DOCTRINE MUTATION LOG
# ============================================================================

@dataclass
class DoctrineMutation:
    """A single doctrine mutation event."""
    mutation_id: str = dc_field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = dc_field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    mutation_type: MutationType = MutationType.BLOCK_ADDED
    origin: MutationOrigin = MutationOrigin.STARTUP_INIT
    topic: str = ""
    category: str = ""
    previous_hash: str = ""
    new_hash: str = ""
    description: str = ""
    regulation_affected: str = ""
    metadata: Dict[str, Any] = dc_field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "mutation_id": self.mutation_id,
            "timestamp": self.timestamp,
            "mutation_type": self.mutation_type.value,
            "origin": self.origin.value,
            "topic": self.topic,
            "category": self.category,
            "previous_hash": self.previous_hash,
            "new_hash": self.new_hash,
            "description": self.description,
            "regulation_affected": self.regulation_affected,
            "metadata": self.metadata,
        }


class DoctrineMutationLog:
    """Track all mutations to the doctrine cache."""

    def __init__(self, max_entries: int = 5000) -> None:
        self._entries: deque[DoctrineMutation] = deque(maxlen=max_entries)
        self._lock = threading.Lock()
        self._type_counts: Counter = Counter()
        self._origin_counts: Counter = Counter()
        self._regulation_counts: Counter = Counter()

    def record(
        self,
        mutation_type: MutationType,
        origin: MutationOrigin,
        topic: str,
        category: str = "",
        previous_hash: str = "",
        new_hash: str = "",
        description: str = "",
        regulation_affected: str = "",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> DoctrineMutation:
        """Record a doctrine mutation."""
        mutation = DoctrineMutation(
            mutation_type=mutation_type,
            origin=origin,
            topic=topic,
            category=category,
            previous_hash=previous_hash,
            new_hash=new_hash,
            description=description,
            regulation_affected=regulation_affected,
            metadata=metadata or {},
        )
        with self._lock:
            self._entries.append(mutation)
            self._type_counts[mutation_type.value] += 1
            self._origin_counts[origin.value] += 1
            if regulation_affected:
                self._regulation_counts[regulation_affected] += 1
        logger.info(f"Doctrine mutation: {mutation_type.value} on {topic} via {origin.value} (reg={regulation_affected})")
        return mutation

    def get_recent(self, n: int = 50) -> List[Dict[str, Any]]:
        """Get recent mutations."""
        with self._lock:
            return [m.to_dict() for m in list(self._entries)[-n:]]

    def get_summary(self) -> Dict[str, Any]:
        """Get mutation log summary."""
        with self._lock:
            return {
                "total_mutations": len(self._entries),
                "by_type": dict(self._type_counts.most_common()),
                "by_origin": dict(self._origin_counts.most_common()),
                "by_regulation": dict(self._regulation_counts.most_common(10)),
                "recent": [m.to_dict() for m in list(self._entries)[-5:]],
            }


# ============================================================================
# ENVIRONMENTAL METRICS - Domain-specific counters
# ============================================================================

class EnvironmentalMetrics:
    """Environmental law domain-specific metric counters."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self.nepa_queries: int = 0
        self.caa_queries: int = 0
        self.cwa_queries: int = 0
        self.rcra_queries: int = 0
        self.cercla_queries: int = 0
        self.tsca_queries: int = 0
        self.esa_queries: int = 0
        self.fifra_queries: int = 0
        self.sdwa_queries: int = 0
        self.opa_queries: int = 0
        self.tceq_queries: int = 0
        self.rrc_queries: int = 0
        self.permit_queries: int = 0
        self.citizen_suit_queries: int = 0
        self.carbon_credit_queries: int = 0
        self.environmental_justice_queries: int = 0
        self.permian_basin_queries: int = 0
        self.phase_i_esa_queries: int = 0
        self.phase_ii_esa_queries: int = 0
        self.brownfield_queries: int = 0
        self.toxic_tort_queries: int = 0
        self.compliance_checks: int = 0
        self.penalty_assessments: int = 0
        self.remediation_analyses: int = 0
        self._statute_hits: Counter = Counter()
        self._contaminant_hits: Counter = Counter()

    def record_statute_query(self, statute: str) -> None:
        """Record a statute-specific query."""
        with self._lock:
            attr_name = f"{statute.lower()}_queries"
            if hasattr(self, attr_name):
                setattr(self, attr_name, getattr(self, attr_name) + 1)
            self._statute_hits[statute] += 1

    def record_contaminant(self, contaminant: str) -> None:
        """Record contaminant type referenced."""
        with self._lock:
            self._contaminant_hits[contaminant] += 1

    def record_permit_query(self) -> None:
        """Record permit-related query."""
        with self._lock:
            self.permit_queries += 1

    def record_compliance_check(self) -> None:
        """Record compliance check."""
        with self._lock:
            self.compliance_checks += 1

    def record_penalty_assessment(self) -> None:
        """Record penalty assessment query."""
        with self._lock:
            self.penalty_assessments += 1

    def record_remediation_analysis(self) -> None:
        """Record remediation analysis query."""
        with self._lock:
            self.remediation_analyses += 1

    def get_stats(self) -> Dict[str, Any]:
        """Get domain-specific stats."""
        with self._lock:
            return {
                "statute_queries": {
                    "nepa": self.nepa_queries,
                    "caa": self.caa_queries,
                    "cwa": self.cwa_queries,
                    "rcra": self.rcra_queries,
                    "cercla": self.cercla_queries,
                    "tsca": self.tsca_queries,
                    "esa": self.esa_queries,
                    "fifra": self.fifra_queries,
                    "sdwa": self.sdwa_queries,
                    "opa": self.opa_queries,
                    "tceq": self.tceq_queries,
                    "rrc": self.rrc_queries,
                },
                "category_queries": {
                    "permits": self.permit_queries,
                    "citizen_suits": self.citizen_suit_queries,
                    "carbon_credits": self.carbon_credit_queries,
                    "environmental_justice": self.environmental_justice_queries,
                    "permian_basin": self.permian_basin_queries,
                    "phase_i_esa": self.phase_i_esa_queries,
                    "phase_ii_esa": self.phase_ii_esa_queries,
                    "brownfield": self.brownfield_queries,
                    "toxic_tort": self.toxic_tort_queries,
                },
                "operations": {
                    "compliance_checks": self.compliance_checks,
                    "penalty_assessments": self.penalty_assessments,
                    "remediation_analyses": self.remediation_analyses,
                },
                "top_statutes": dict(self._statute_hits.most_common(15)),
                "top_contaminants": dict(self._contaminant_hits.most_common(10)),
            }


# ============================================================================
# TELEMETRY COLLECTOR (Main entry point)
# ============================================================================

class TelemetryCollector:
    """Main telemetry coordinator for the Environmental Law Engine."""

    def __init__(
        self,
        audit_log_path: Optional[Path] = None,
        metrics_retention_hours: int = 168,
        max_audit_size_mb: int = 500,
    ) -> None:
        log_dir = Path("O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/LG13_environmental_law/logs")
        log_dir.mkdir(parents=True, exist_ok=True)
        self.audit = AuditTrail(
            log_path=audit_log_path or (log_dir / "audit_trail.jsonl"),
            max_size_mb=max_audit_size_mb,
        )
        self.metrics = MetricsAggregator(window_size=1000, retention_hours=metrics_retention_hours)
        self.errors = ErrorTracker(max_recent=200)
        self.mutations = DoctrineMutationLog(max_entries=5000)
        self.env_metrics = EnvironmentalMetrics()
        self._active_traces: Dict[str, QueryTrace] = {}
        self._lock = threading.Lock()
        self._boot_time = time.time()
        logger.info("LG13 Environmental Law Telemetry initialized")

    def start_trace(
        self,
        query_text: str,
        query_hash: str = "",
        response_mode: str = "HYBRID",
        analysis_layer: str = "STANDARD",
        jurisdiction: str = "",
    ) -> QueryTrace:
        """Begin tracing a query."""
        trace = QueryTrace(
            query_text=query_text,
            query_hash=query_hash or hashlib.sha256(query_text.encode("utf-8")).hexdigest()[:16],
            response_mode=response_mode,
            analysis_layer=analysis_layer,
            jurisdiction=jurisdiction,
        )
        with self._lock:
            self._active_traces[trace.trace_id] = trace
        return trace

    def complete_trace(self, trace: QueryTrace) -> None:
        """Complete a trace and record all metrics."""
        with self._lock:
            self._active_traces.pop(trace.trace_id, None)
        self.metrics.record_trace(trace)
        self.audit.record(
            event_type="query_complete",
            details=trace.to_dict(),
            severity=AlertSeverity.ERROR if trace.error_message else AlertSeverity.INFO,
        )
        if trace.error_message and trace.error_domain:
            self.errors.record_error(
                domain=trace.error_domain,
                message=trace.error_message,
                trace_id=trace.trace_id,
            )

    def log_error(self, domain: ErrorDomain, message: str, trace_id: str = "", details: Optional[Dict[str, Any]] = None) -> None:
        """Log an error."""
        self.errors.record_error(domain=domain, message=message, trace_id=trace_id, details=details)
        self.audit.record(
            event_type="error",
            details={"domain": domain.value, "message": message, "trace_id": trace_id, **(details or {})},
            severity=AlertSeverity.ERROR,
        )

    def record_doctrine_mutation(
        self,
        mutation_type: MutationType,
        origin: MutationOrigin,
        topic: str,
        category: str = "",
        previous_hash: str = "",
        new_hash: str = "",
        description: str = "",
        regulation_affected: str = "",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> DoctrineMutation:
        """Record a doctrine mutation."""
        mutation = self.mutations.record(
            mutation_type=mutation_type,
            origin=origin,
            topic=topic,
            category=category,
            previous_hash=previous_hash,
            new_hash=new_hash,
            description=description,
            regulation_affected=regulation_affected,
            metadata=metadata,
        )
        self.audit.record(
            event_type="doctrine_mutation",
            details=mutation.to_dict(),
            severity=AlertSeverity.WARNING,
        )
        return mutation

    def get_health(self) -> Dict[str, Any]:
        """Get full telemetry health report."""
        return {
            "engine_id": "LG13",
            "engine_name": "Environmental Law Engine",
            "uptime_seconds": round(time.time() - self._boot_time, 1),
            "metrics": self.metrics.get_stats(),
            "errors": self.errors.get_summary(),
            "mutations": self.mutations.get_summary(),
            "environmental_metrics": self.env_metrics.get_stats(),
            "audit": {
                "entry_count": self.audit.entry_count,
                "last_hash": self.audit.last_hash[:16] + "...",
            },
            "active_traces": len(self._active_traces),
        }


# ============================================================================
# MODULE-LEVEL SINGLETON
# ============================================================================

_telemetry: Optional[TelemetryCollector] = None
_telemetry_lock = threading.Lock()


def get_telemetry() -> TelemetryCollector:
    """Get or create the global telemetry collector."""
    global _telemetry
    if _telemetry is None:
        with _telemetry_lock:
            if _telemetry is None:
                _telemetry = TelemetryCollector()
    return _telemetry


def trace_query(
    query_text: str,
    query_hash: str = "",
    response_mode: str = "HYBRID",
    analysis_layer: str = "STANDARD",
    jurisdiction: str = "",
) -> QueryTrace:
    """Convenience: start a query trace."""
    return get_telemetry().start_trace(
        query_text=query_text,
        query_hash=query_hash,
        response_mode=response_mode,
        analysis_layer=analysis_layer,
        jurisdiction=jurisdiction,
    )


def complete_trace(trace: QueryTrace) -> None:
    """Convenience: complete a query trace."""
    get_telemetry().complete_trace(trace)


def log_error(domain: ErrorDomain, message: str, trace_id: str = "", details: Optional[Dict[str, Any]] = None) -> None:
    """Convenience: log an error."""
    get_telemetry().log_error(domain=domain, message=message, trace_id=trace_id, details=details)


def record_doctrine_mutation(
    mutation_type: MutationType,
    origin: MutationOrigin,
    topic: str,
    category: str = "",
    previous_hash: str = "",
    new_hash: str = "",
    description: str = "",
    regulation_affected: str = "",
    metadata: Optional[Dict[str, Any]] = None,
) -> DoctrineMutation:
    """Convenience: record a doctrine mutation."""
    return get_telemetry().record_doctrine_mutation(
        mutation_type=mutation_type,
        origin=origin,
        topic=topic,
        category=category,
        previous_hash=previous_hash,
        new_hash=new_hash,
        description=description,
        regulation_affected=regulation_affected,
        metadata=metadata,
    )
