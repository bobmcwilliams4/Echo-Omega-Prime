"""
LM12 GIS Integration Engine — Telemetry Module
Full query tracing, latency tracking, error domains, and operational metrics.

Author: ECHO OMEGA PRIME
Engine: LM12 GIS Integration
Port: 8512
"""

from __future__ import annotations

import hashlib
import json
import time
import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

from loguru import logger

# ==============================================================================
# LOG CONFIGURATION
# ==============================================================================

LOG_DIR = Path("O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/LM12_gis_integration/logs")
LOG_DIR.mkdir(exist_ok=True, parents=True)

logger.add(
    LOG_DIR / "gis_telemetry_{time}.log",
    rotation="50 MB",
    retention="30 days",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {name}:{function}:{line} | {message}",
)

AUDIT_LOG = LOG_DIR / "audit_trail.jsonl"
METRICS_LOG = LOG_DIR / "metrics.jsonl"


# ==============================================================================
# ERROR DOMAIN CLASSIFICATION
# ==============================================================================

class ErrorDomain(str, Enum):
    """Classified error domains for GIS operations."""
    COORDINATE_CONVERSION = "coordinate_conversion"
    LEGAL_DESCRIPTION_PARSE = "legal_description_parse"
    METES_BOUNDS_PLOT = "metes_bounds_plot"
    SURVEY_LOOKUP = "survey_lookup"
    SPACING_ANALYSIS = "spacing_analysis"
    PLAT_GENERATION = "plat_generation"
    WELL_LOCATION = "well_location"
    BOUNDARY_CALC = "boundary_calc"
    PRORATION = "proration"
    REGULATORY = "regulatory"
    DATA_SOURCE = "data_source"
    DOCTRINE_CACHE = "doctrine_cache"
    SEMANTIC_SEARCH = "semantic_search"
    DEEP_ANALYSIS = "deep_analysis"
    PROCESSING = "processing"
    SYSTEM = "system"
    NETWORK = "network"
    CONFIGURATION = "configuration"
    INPUT_VALIDATION = "input_validation"


class ResponseLayer(str, Enum):
    """Which processing layer handled the response."""
    DOCTRINE_CACHE = "doctrine_cache"
    SEMANTIC_RETRIEVAL = "semantic_retrieval"
    DEEP_ANALYSIS = "deep_analysis"
    COORDINATE_ENGINE = "coordinate_engine"
    SPATIAL_ENGINE = "spatial_engine"
    REGULATORY_ENGINE = "regulatory_engine"


class MutationType(str, Enum):
    """Types of doctrine mutations tracked."""
    DOCTRINE_ADDED = "doctrine_added"
    DOCTRINE_MODIFIED = "doctrine_modified"
    DOCTRINE_DEPRECATED = "doctrine_deprecated"
    AUTHORITY_UPDATED = "authority_updated"
    CONFIDENCE_CHANGED = "confidence_changed"
    KEYWORD_EXPANDED = "keyword_expanded"
    COUNTER_ARGUMENT_ADDED = "counter_argument_added"


class MutationOrigin(str, Enum):
    """Where doctrine mutations originate."""
    MANUAL = "manual"
    DRIFT_WATCHER = "drift_watcher"
    AUTO_UPDATE = "auto_update"
    COMMANDER_OVERRIDE = "commander_override"
    REGULATORY_CHANGE = "regulatory_change"


# ==============================================================================
# TRACE CONTEXT
# ==============================================================================

@dataclass
class TraceContext:
    """Full trace context for a single query lifecycle."""
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    query_text: str = ""
    query_hash: str = ""
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    duration_ms: float = 0.0
    response_layer: Optional[ResponseLayer] = None
    doctrine_topic: Optional[str] = None
    doctrine_hit: bool = False
    error_domain: Optional[ErrorDomain] = None
    error_message: Optional[str] = None
    coordinate_system_in: Optional[str] = None
    coordinate_system_out: Optional[str] = None
    county: Optional[str] = None
    state: Optional[str] = None
    abstract_number: Optional[str] = None
    survey_name: Optional[str] = None
    section: Optional[str] = None
    township: Optional[str] = None
    range_val: Optional[str] = None
    well_api: Optional[str] = None
    confidence: float = 0.0
    token_count: int = 0
    response_mode: str = "FAST"
    steps: List[Dict[str, Any]] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_step(self, name: str, duration_ms: float, details: Optional[Dict[str, Any]] = None) -> None:
        """Record a processing step within the trace."""
        self.steps.append({
            "step": name,
            "duration_ms": round(duration_ms, 3),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "details": details or {},
        })

    def add_warning(self, warning: str) -> None:
        """Add a non-fatal warning to the trace."""
        self.warnings.append(warning)
        logger.warning(f"[{self.trace_id[:8]}] {warning}")

    def complete(self, layer: ResponseLayer, doctrine_hit: bool = False) -> None:
        """Mark the trace as complete."""
        self.end_time = time.time()
        self.duration_ms = round((self.end_time - self.start_time) * 1000, 3)
        self.response_layer = layer
        self.doctrine_hit = doctrine_hit

    def fail(self, domain: ErrorDomain, message: str) -> None:
        """Mark the trace as failed."""
        self.end_time = time.time()
        self.duration_ms = round((self.end_time - self.start_time) * 1000, 3)
        self.error_domain = domain
        self.error_message = message
        logger.error(f"[{self.trace_id[:8]}] {domain.value}: {message}")

    def to_dict(self) -> Dict[str, Any]:
        """Serialize trace to dictionary for audit logging."""
        return {
            "trace_id": self.trace_id,
            "query_hash": self.query_hash,
            "start_time": datetime.fromtimestamp(self.start_time, tz=timezone.utc).isoformat(),
            "end_time": datetime.fromtimestamp(self.end_time, tz=timezone.utc).isoformat() if self.end_time else None,
            "duration_ms": self.duration_ms,
            "response_layer": self.response_layer.value if self.response_layer else None,
            "doctrine_topic": self.doctrine_topic,
            "doctrine_hit": self.doctrine_hit,
            "error_domain": self.error_domain.value if self.error_domain else None,
            "error_message": self.error_message,
            "coordinate_system_in": self.coordinate_system_in,
            "coordinate_system_out": self.coordinate_system_out,
            "county": self.county,
            "state": self.state,
            "abstract_number": self.abstract_number,
            "survey_name": self.survey_name,
            "section": self.section,
            "well_api": self.well_api,
            "confidence": self.confidence,
            "token_count": self.token_count,
            "response_mode": self.response_mode,
            "step_count": len(self.steps),
            "steps": self.steps,
            "warnings": self.warnings,
            "metadata": self.metadata,
        }


# ==============================================================================
# MUTATION RECORD
# ==============================================================================

@dataclass
class DoctrineMutationRecord:
    """Track every change to doctrine blocks for drift detection."""
    mutation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    mutation_type: MutationType = MutationType.DOCTRINE_MODIFIED
    origin: MutationOrigin = MutationOrigin.MANUAL
    doctrine_topic: str = ""
    field_changed: str = ""
    old_value_hash: str = ""
    new_value_hash: str = ""
    reason: str = ""
    approved_by: str = "system"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "mutation_id": self.mutation_id,
            "timestamp": self.timestamp,
            "mutation_type": self.mutation_type.value,
            "origin": self.origin.value,
            "doctrine_topic": self.doctrine_topic,
            "field_changed": self.field_changed,
            "old_value_hash": self.old_value_hash,
            "new_value_hash": self.new_value_hash,
            "reason": self.reason,
            "approved_by": self.approved_by,
        }


# ==============================================================================
# METRICS COLLECTOR
# ==============================================================================

class MetricsCollector:
    """
    Lightweight metrics for GIS engine operational awareness.
    Tracks latencies, error rates, doctrine hit rates, coordinate conversions,
    and spatial operation performance.
    """

    def __init__(self, window_hours: int = 24) -> None:
        self.window_seconds: int = window_hours * 3600
        self.latencies: List[float] = []
        self.errors: List[float] = []
        self.queries: List[float] = []
        self.doctrine_hits: int = 0
        self.doctrine_misses: int = 0
        self.last_error: Optional[str] = None
        self.active_queries: int = 0
        self._max_latencies: int = 500
        self.coordinate_conversions: int = 0
        self.legal_desc_parses: int = 0
        self.spacing_analyses: int = 0
        self.boundary_calcs: int = 0
        self.plat_generations: int = 0
        self.well_plots: int = 0
        self.proration_calcs: int = 0
        self.error_by_domain: Dict[str, int] = defaultdict(int)
        self.queries_by_mode: Dict[str, int] = defaultdict(int)
        self.queries_by_county: Dict[str, int] = defaultdict(int)
        self.queries_by_state: Dict[str, int] = defaultdict(int)
        self.layer_distribution: Dict[str, int] = defaultdict(int)
        self._start_time: float = time.time()

    def record_query(self, latency_ms: float, doctrine_hit: bool, mode: str = "FAST") -> None:
        """Record a completed query with latency and cache hit status."""
        now = time.time()
        self.latencies.append(latency_ms)
        if len(self.latencies) > self._max_latencies:
            self.latencies = self.latencies[-self._max_latencies:]
        self.queries.append(now)
        cutoff = now - self.window_seconds
        self.queries = [t for t in self.queries if t > cutoff]
        if doctrine_hit:
            self.doctrine_hits += 1
        else:
            self.doctrine_misses += 1
        self.queries_by_mode[mode] = self.queries_by_mode.get(mode, 0) + 1

    def record_error(self, error_msg: str, domain: Optional[ErrorDomain] = None) -> None:
        """Record an error occurrence with domain classification."""
        self.errors.append(time.time())
        self.last_error = f"{datetime.now(timezone.utc).isoformat()}: {error_msg[:200]}"
        cutoff = time.time() - self.window_seconds
        self.errors = [t for t in self.errors if t > cutoff]
        if domain:
            self.error_by_domain[domain.value] = self.error_by_domain.get(domain.value, 0) + 1

    def record_coordinate_conversion(self) -> None:
        self.coordinate_conversions += 1

    def record_legal_desc_parse(self) -> None:
        self.legal_desc_parses += 1

    def record_spacing_analysis(self) -> None:
        self.spacing_analyses += 1

    def record_boundary_calc(self) -> None:
        self.boundary_calcs += 1

    def record_plat_generation(self) -> None:
        self.plat_generations += 1

    def record_well_plot(self) -> None:
        self.well_plots += 1

    def record_proration_calc(self) -> None:
        self.proration_calcs += 1

    def record_county_query(self, county: str) -> None:
        self.queries_by_county[county] = self.queries_by_county.get(county, 0) + 1

    def record_state_query(self, state: str) -> None:
        self.queries_by_state[state] = self.queries_by_state.get(state, 0) + 1

    def record_layer(self, layer: ResponseLayer) -> None:
        self.layer_distribution[layer.value] = self.layer_distribution.get(layer.value, 0) + 1

    def query_start(self) -> None:
        self.active_queries += 1

    def query_end(self) -> None:
        self.active_queries = max(0, self.active_queries - 1)

    def get_latency_stats(self) -> Dict[str, float]:
        if not self.latencies:
            return {"avg_ms": 0.0, "p50_ms": 0.0, "p95_ms": 0.0, "p99_ms": 0.0, "min_ms": 0.0, "max_ms": 0.0, "last_ms": 0.0}
        sorted_lat = sorted(self.latencies)
        n = len(sorted_lat)
        return {
            "avg_ms": round(sum(self.latencies) / n, 2),
            "p50_ms": round(sorted_lat[int(n * 0.50)], 2),
            "p95_ms": round(sorted_lat[min(int(n * 0.95), n - 1)], 2),
            "p99_ms": round(sorted_lat[min(int(n * 0.99), n - 1)], 2),
            "min_ms": round(sorted_lat[0], 2),
            "max_ms": round(sorted_lat[-1], 2),
            "last_ms": round(self.latencies[-1], 2),
        }

    def get_error_stats(self) -> Dict[str, Any]:
        now = time.time()
        last_hour = sum(1 for t in self.errors if t > now - 3600)
        return {
            "last_hour": last_hour,
            "last_24h": len(self.errors),
            "last_error": self.last_error,
            "by_domain": dict(self.error_by_domain),
        }

    def get_doctrine_hit_rate(self) -> float:
        total = self.doctrine_hits + self.doctrine_misses
        if total == 0:
            return 0.0
        return round(self.doctrine_hits / total, 4)

    def get_queries_per_hour(self) -> float:
        if not self.queries:
            return 0.0
        now = time.time()
        hour_queries = sum(1 for t in self.queries if t > now - 3600)
        return round(hour_queries, 1)

    def get_uptime_seconds(self) -> float:
        return round(time.time() - self._start_time, 1)

    def get_operation_counts(self) -> Dict[str, int]:
        return {
            "coordinate_conversions": self.coordinate_conversions,
            "legal_desc_parses": self.legal_desc_parses,
            "spacing_analyses": self.spacing_analyses,
            "boundary_calcs": self.boundary_calcs,
            "plat_generations": self.plat_generations,
            "well_plots": self.well_plots,
            "proration_calcs": self.proration_calcs,
        }

    def get_full_metrics(self) -> Dict[str, Any]:
        total_queries = self.doctrine_hits + self.doctrine_misses
        return {
            "uptime_seconds": self.get_uptime_seconds(),
            "total_queries": total_queries,
            "active_queries": self.active_queries,
            "queries_per_hour": self.get_queries_per_hour(),
            "doctrine_hit_rate": self.get_doctrine_hit_rate(),
            "latency": self.get_latency_stats(),
            "errors": self.get_error_stats(),
            "operations": self.get_operation_counts(),
            "queries_by_mode": dict(self.queries_by_mode),
            "queries_by_county": dict(self.queries_by_county),
            "queries_by_state": dict(self.queries_by_state),
            "layer_distribution": dict(self.layer_distribution),
        }


# ==============================================================================
# TELEMETRY SINGLETON
# ==============================================================================

_telemetry_instance: Optional[MetricsCollector] = None


def get_telemetry() -> MetricsCollector:
    """Get or create the singleton telemetry instance."""
    global _telemetry_instance
    if _telemetry_instance is None:
        _telemetry_instance = MetricsCollector(window_hours=24)
    return _telemetry_instance


def trace_query(query_text: str, mode: str = "FAST") -> TraceContext:
    """Create a new trace context for a query."""
    ctx = TraceContext(
        query_text=query_text,
        query_hash=hashlib.sha256(query_text.encode()).hexdigest()[:16],
        response_mode=mode,
    )
    get_telemetry().query_start()
    logger.info(f"[TRACE:{ctx.trace_id[:8]}] Query started | mode={mode} | hash={ctx.query_hash}")
    return ctx


def complete_trace(ctx: TraceContext) -> None:
    """Complete a trace and record metrics."""
    telemetry = get_telemetry()
    telemetry.query_end()
    telemetry.record_query(ctx.duration_ms, ctx.doctrine_hit, ctx.response_mode)
    if ctx.response_layer:
        telemetry.record_layer(ctx.response_layer)
    if ctx.county:
        telemetry.record_county_query(ctx.county)
    if ctx.state:
        telemetry.record_state_query(ctx.state)
    _write_audit_record(ctx)
    logger.info(
        f"[TRACE:{ctx.trace_id[:8]}] Complete | "
        f"layer={ctx.response_layer.value if ctx.response_layer else 'none'} | "
        f"hit={ctx.doctrine_hit} | "
        f"duration={ctx.duration_ms}ms | "
        f"confidence={ctx.confidence}"
    )


def log_error(ctx: TraceContext, domain: ErrorDomain, message: str) -> None:
    """Log an error within a trace context."""
    ctx.fail(domain, message)
    telemetry = get_telemetry()
    telemetry.record_error(message, domain)
    telemetry.query_end()
    _write_audit_record(ctx)


def record_doctrine_mutation(
    mutation_type: MutationType,
    origin: MutationOrigin,
    topic: str,
    field_changed: str,
    old_value: str,
    new_value: str,
    reason: str,
) -> DoctrineMutationRecord:
    """Record a doctrine mutation for drift tracking."""
    record = DoctrineMutationRecord(
        mutation_type=mutation_type,
        origin=origin,
        doctrine_topic=topic,
        field_changed=field_changed,
        old_value_hash=hashlib.sha256(old_value.encode()).hexdigest()[:16],
        new_value_hash=hashlib.sha256(new_value.encode()).hexdigest()[:16],
        reason=reason,
    )
    _write_mutation_record(record)
    logger.info(
        f"[MUTATION:{record.mutation_id[:8]}] {mutation_type.value} on '{topic}.{field_changed}' "
        f"by {origin.value}: {reason}"
    )
    return record


# ==============================================================================
# AUDIT TRAIL I/O
# ==============================================================================

def _write_audit_record(ctx: TraceContext) -> None:
    """Append trace record to JSONL audit trail."""
    try:
        with AUDIT_LOG.open("a", encoding="utf-8") as f:
            f.write(json.dumps(ctx.to_dict(), default=str) + "\n")
    except Exception as e:
        logger.error(f"Failed to write audit record: {e}")


def _write_mutation_record(record: DoctrineMutationRecord) -> None:
    """Append mutation record to metrics log."""
    try:
        with METRICS_LOG.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record.to_dict(), default=str) + "\n")
    except Exception as e:
        logger.error(f"Failed to write mutation record: {e}")


def read_audit_trail(limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
    """Read audit trail records with pagination."""
    records: List[Dict[str, Any]] = []
    if not AUDIT_LOG.exists():
        return records
    try:
        with AUDIT_LOG.open("r", encoding="utf-8") as f:
            lines = f.readlines()
        target_lines = lines[-(offset + limit): len(lines) - offset if offset > 0 else len(lines)]
        for line in target_lines:
            line = line.strip()
            if line:
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    except Exception as e:
        logger.error(f"Failed to read audit trail: {e}")
    return records


def read_mutation_log(limit: int = 100) -> List[Dict[str, Any]]:
    """Read mutation log records."""
    records: List[Dict[str, Any]] = []
    if not METRICS_LOG.exists():
        return records
    try:
        with METRICS_LOG.open("r", encoding="utf-8") as f:
            lines = f.readlines()
        for line in lines[-limit:]:
            line = line.strip()
            if line:
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    except Exception as e:
        logger.error(f"Failed to read mutation log: {e}")
    return records


def get_audit_summary() -> Dict[str, Any]:
    """Generate summary statistics from the audit trail."""
    records = read_audit_trail(limit=1000)
    if not records:
        return {"total_records": 0, "summary": "No audit records found"}
    total = len(records)
    errors = sum(1 for r in records if r.get("error_domain"))
    layers = defaultdict(int)
    domains = defaultdict(int)
    for r in records:
        layer = r.get("response_layer")
        if layer:
            layers[layer] += 1
        err_domain = r.get("error_domain")
        if err_domain:
            domains[err_domain] += 1
    durations = [r.get("duration_ms", 0) for r in records if r.get("duration_ms")]
    avg_duration = round(sum(durations) / len(durations), 2) if durations else 0.0
    return {
        "total_records": total,
        "error_count": errors,
        "error_rate": round(errors / total, 4) if total > 0 else 0.0,
        "avg_duration_ms": avg_duration,
        "layer_distribution": dict(layers),
        "error_domains": dict(domains),
    }


# ==============================================================================
# QUERY PHASE ENUM — required by engine.py three_layer_response
# ==============================================================================

class QueryPhase(str, Enum):
    """Processing phases within a query lifecycle."""
    NORMALIZATION = "normalization"
    CACHE_LOOKUP = "cache_lookup"
    VECTOR_SEARCH = "vector_search"
    DEEP_ANALYSIS = "deep_analysis"
    FORMATTING = "formatting"
    GUARDRAILS = "guardrails"


# ==============================================================================
# QUERY TRACE — lightweight trace used by engine.py
# ==============================================================================

@dataclass
class QueryTrace:
    """Lightweight query trace for the engine's three-layer pipeline."""
    query_id: str = ""
    query: str = ""
    mode: str = "FAST"
    zone: str = "REPORTING"
    cache_hit: bool = False
    phases: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    end_time: Optional[float] = None
    _active_phase: Optional[str] = field(default=None, repr=False)
    _phase_start: float = field(default=0.0, repr=False)

    def start_phase(self, phase: QueryPhase) -> None:
        """Begin timing a processing phase."""
        self._active_phase = phase.value
        self._phase_start = time.time()

    def end_phase(self, phase: QueryPhase) -> None:
        """End timing a processing phase and record duration."""
        elapsed_ms = (time.time() - self._phase_start) * 1000
        self.phases[phase.value] = {
            "duration_ms": round(elapsed_ms, 3),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self._active_phase = None


# ==============================================================================
# TELEMETRY MANAGER — required by engine.py
# ==============================================================================

class TelemetryManager:
    """
    Manages telemetry lifecycle for an engine.
    Wraps the MetricsCollector and provides trace logging.
    """

    def __init__(self, engine_id: str = "LM12", log_dir: Optional[Path] = None) -> None:
        self.engine_id = engine_id
        self.log_dir = log_dir or LOG_DIR
        self.collector = get_telemetry()
        self._traces: List[Dict[str, Any]] = []
        logger.info(f"TelemetryManager initialized for engine {engine_id}")

    def log_trace(self, trace: QueryTrace) -> None:
        """Log a completed query trace to the audit trail."""
        record = {
            "query_id": trace.query_id,
            "engine_id": self.engine_id,
            "mode": trace.mode,
            "zone": trace.zone,
            "cache_hit": trace.cache_hit,
            "phases": trace.phases,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self._traces.append(record)
        # Also append to JSONL audit log
        try:
            audit_path = self.log_dir / "audit_trail.jsonl"
            with audit_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(record, default=str) + "\n")
        except Exception as e:
            logger.error(f"Failed to write trace to audit log: {e}")


# ==============================================================================
# COVERAGE MAP — tracks which doctrines are triggered vs missed
# ==============================================================================

class CoverageMap:
    """
    Tracks doctrine coverage: which topics have been triggered by queries
    and which remain untouched (epistemic gaps).
    """

    def __init__(self) -> None:
        self._registered: Dict[str, int] = {}
        self._triggered: Dict[str, int] = {}

    def register_topic(self, topic: str) -> None:
        """Register a doctrine topic as available."""
        self._registered[topic] = self._registered.get(topic, 0)

    def mark_triggered(self, topic: str) -> None:
        """Mark a doctrine topic as triggered by a query."""
        self._triggered[topic] = self._triggered.get(topic, 0) + 1

    def get_report(self) -> Dict[str, Any]:
        """Return coverage statistics."""
        total_registered = len(self._registered)
        total_triggered = len(self._triggered)
        never_triggered = [t for t in self._registered if t not in self._triggered]
        return {
            "total_registered": total_registered,
            "total_triggered": total_triggered,
            "coverage_pct": round(total_triggered / total_registered * 100, 1) if total_registered > 0 else 0.0,
            "never_triggered": never_triggered,
            "trigger_counts": dict(self._triggered),
        }


# ==============================================================================
# DRIFT WATCHER — monitors doctrine consistency over time
# ==============================================================================

class DriftWatcher:
    """
    Monitors doctrine cache for drift — when doctrines produce
    inconsistent results or when external authority changes.
    """

    def __init__(self) -> None:
        self._baselines: Dict[str, str] = {}
        self._drift_events: List[Dict[str, Any]] = []

    def set_baseline(self, topic: str, hash_value: str) -> None:
        """Set the baseline hash for a doctrine topic."""
        self._baselines[topic] = hash_value

    def check_drift(self, topic: str, current_hash: str) -> bool:
        """Check if a doctrine has drifted from its baseline. Returns True if drifted."""
        baseline = self._baselines.get(topic)
        if baseline is None:
            self._baselines[topic] = current_hash
            return False
        if baseline != current_hash:
            self._drift_events.append({
                "topic": topic,
                "baseline_hash": baseline,
                "current_hash": current_hash,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            return True
        return False

    def get_drift_report(self) -> Dict[str, Any]:
        """Return drift detection report."""
        return {
            "total_baselines": len(self._baselines),
            "drift_events": len(self._drift_events),
            "events": self._drift_events[-20:],
        }
