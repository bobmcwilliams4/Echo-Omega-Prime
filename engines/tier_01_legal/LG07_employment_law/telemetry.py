"""
LG07 Employment Law Engine - Telemetry Module
================================================
Production telemetry, metrics collection, audit trail, and observability
for the Employment Law Engine.

Components:
    - TelemetryCollector: Ring-buffer based metric collection
    - QueryTrace: Per-query trace with timing breakdowns
    - AuditTrail: Append-only JSONL audit log with SHA-256 chain
    - MetricsAggregator: Rolling window aggregation for dashboards
    - ErrorTracker: Domain-classified error tracking and alerting
    - DoctrineMutationLog: Track changes to doctrine cache
    - EmploymentMetrics: Employment-law-specific counters (discrimination, wage/hour, etc.)

Port: 8397
Engine: LG07 Employment Law
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
    EMPLOYMENT_ANALYSIS = "employment_analysis"
    DEEP_ANALYSIS = "deep_analysis"
    FALLBACK = "fallback"
    ERROR = "error"


class ErrorDomain(Enum):
    """Classification of errors by employment law domain."""
    TITLE_VII = "title_vii"
    ADA = "ada"
    ADEA = "adea"
    FMLA = "fmla"
    FLSA = "flsa"
    OSHA = "osha"
    ERISA = "erisa"
    NLRA = "nlra"
    WARN_ACT = "warn_act"
    WRONGFUL_TERMINATION = "wrongful_termination"
    NON_COMPETE = "non_compete"
    HARASSMENT = "harassment"
    RETALIATION = "retaliation"
    WORKERS_COMP = "workers_comp"
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


class MutationOrigin(Enum):
    """Origin of a doctrine mutation."""
    MANUAL = "manual"
    DRIFT_WATCHER = "drift_watcher"
    AUTO_UPDATE = "auto_update"
    EXTERNAL_FEED = "external_feed"
    QUALITY_GATE = "quality_gate"
    CASE_LAW_UPDATE = "case_law_update"
    LEGISLATIVE_CHANGE = "legislative_change"
    REGULATORY_UPDATE = "regulatory_update"


class EmploymentMetricType(Enum):
    """Employment-law-specific metric categories."""
    DISCRIMINATION_QUERY = "discrimination_query"
    WAGE_HOUR_QUERY = "wage_hour_query"
    LEAVE_QUERY = "leave_query"
    SAFETY_QUERY = "safety_query"
    BENEFITS_QUERY = "benefits_query"
    LABOR_RELATIONS_QUERY = "labor_relations_query"
    TERMINATION_QUERY = "termination_query"
    HARASSMENT_QUERY = "harassment_query"
    RETALIATION_QUERY = "retaliation_query"
    NON_COMPETE_QUERY = "non_compete_query"
    WORKERS_COMP_QUERY = "workers_comp_query"
    WHISTLEBLOWER_QUERY = "whistleblower_query"
    CONTRACT_QUERY = "contract_query"
    CLASSIFICATION_QUERY = "classification_query"
    COMPLIANCE_QUERY = "compliance_query"


class CitationLookupType(Enum):
    """Types of citation lookups."""
    STATUTE = "statute"
    REGULATION = "regulation"
    CASE_LAW = "case_law"
    EEOC_GUIDANCE = "eeoc_guidance"
    DOL_OPINION = "dol_opinion"
    NLRB_DECISION = "nlrb_decision"
    OSHA_STANDARD = "osha_standard"
    CFR_SECTION = "cfr_section"
    EXECUTIVE_ORDER = "executive_order"
    STATE_STATUTE = "state_statute"


# ============================================================================
# TELEMETRY STEP
# ============================================================================

@dataclass
class TelemetryStep:
    """A single step in a query trace."""
    step_name: str
    start_time: float
    end_time: float = 0.0
    duration_ms: float = 0.0
    metadata: Dict[str, Any] = dc_field(default_factory=dict)
    success: bool = True
    error_message: str = ""

    def complete(self, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Mark this step as complete."""
        self.end_time = time.monotonic()
        self.duration_ms = (self.end_time - self.start_time) * 1000.0
        if metadata:
            self.metadata.update(metadata)

    def fail(self, error_message: str) -> None:
        """Mark this step as failed."""
        self.end_time = time.monotonic()
        self.duration_ms = (self.end_time - self.start_time) * 1000.0
        self.success = False
        self.error_message = error_message

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "step_name": self.step_name,
            "duration_ms": round(self.duration_ms, 3),
            "success": self.success,
            "error_message": self.error_message,
            "metadata": self.metadata,
        }


# ============================================================================
# QUERY TRACE
# ============================================================================

@dataclass
class QueryTrace:
    """Full trace of a single query through the engine."""
    trace_id: str
    query_text: str
    start_time: float
    end_time: float = 0.0
    total_duration_ms: float = 0.0
    response_layer: ResponseLayer = ResponseLayer.DOCTRINE_CACHE
    steps: List[TelemetryStep] = dc_field(default_factory=list)
    doctrine_hits: int = 0
    search_results: int = 0
    confidence: float = 0.0
    employment_domain: str = ""
    response_mode: str = "FAST"
    determinism_hash: str = ""
    error: Optional[str] = None
    cached: bool = False
    multi_doctrine: bool = False
    doctrines_used: List[str] = dc_field(default_factory=list)
    jurisdiction: str = "federal"
    statutes_referenced: List[str] = dc_field(default_factory=list)

    def begin_step(self, step_name: str) -> TelemetryStep:
        """Start a new telemetry step."""
        step = TelemetryStep(step_name=step_name, start_time=time.monotonic())
        self.steps.append(step)
        return step

    def complete(self) -> None:
        """Finalize the trace."""
        self.end_time = time.monotonic()
        self.total_duration_ms = (self.end_time - self.start_time) * 1000.0

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "trace_id": self.trace_id,
            "query_text": self.query_text[:500],
            "total_duration_ms": round(self.total_duration_ms, 3),
            "response_layer": self.response_layer.value,
            "steps": [s.to_dict() for s in self.steps],
            "doctrine_hits": self.doctrine_hits,
            "search_results": self.search_results,
            "confidence": round(self.confidence, 4),
            "employment_domain": self.employment_domain,
            "response_mode": self.response_mode,
            "determinism_hash": self.determinism_hash,
            "error": self.error,
            "cached": self.cached,
            "multi_doctrine": self.multi_doctrine,
            "doctrines_used": self.doctrines_used,
            "jurisdiction": self.jurisdiction,
            "statutes_referenced": self.statutes_referenced,
        }


# ============================================================================
# ERROR RECORD
# ============================================================================

@dataclass
class ErrorRecord:
    """A single error event."""
    error_id: str
    timestamp: str
    domain: ErrorDomain
    message: str
    stack_trace: str = ""
    query_context: str = ""
    severity: str = "MEDIUM"
    resolved: bool = False
    resolution: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "error_id": self.error_id,
            "timestamp": self.timestamp,
            "domain": self.domain.value,
            "message": self.message,
            "stack_trace": self.stack_trace[:2000],
            "query_context": self.query_context[:500],
            "severity": self.severity,
            "resolved": self.resolved,
            "resolution": self.resolution,
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
    topic: str
    before_hash: str
    after_hash: str
    description: str
    confidence_delta: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "mutation_id": self.mutation_id,
            "timestamp": self.timestamp,
            "mutation_type": self.mutation_type.value,
            "origin": self.origin.value,
            "topic": self.topic,
            "before_hash": self.before_hash,
            "after_hash": self.after_hash,
            "description": self.description,
            "confidence_delta": round(self.confidence_delta, 4),
        }


# ============================================================================
# CITATION LOOKUP RECORD
# ============================================================================

@dataclass
class CitationLookupRecord:
    """Record of a citation lookup event."""
    lookup_id: str
    timestamp: str
    lookup_type: CitationLookupType
    citation: str
    found: bool
    source: str
    latency_ms: float

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "lookup_id": self.lookup_id,
            "timestamp": self.timestamp,
            "lookup_type": self.lookup_type.value,
            "citation": self.citation,
            "found": self.found,
            "source": self.source,
            "latency_ms": round(self.latency_ms, 3),
        }


# ============================================================================
# ENGINE METRICS
# ============================================================================

class EngineMetrics:
    """Aggregate metrics for the employment law engine."""

    def __init__(self) -> None:
        """Initialize all metric counters."""
        self._lock = threading.Lock()
        self.total_queries: int = 0
        self.total_errors: int = 0
        self.total_cache_hits: int = 0
        self.total_cache_misses: int = 0
        self.total_search_queries: int = 0
        self.total_deep_analyses: int = 0
        self.total_multi_doctrine: int = 0
        self.total_doctrine_lookups: int = 0
        self.total_citation_lookups: int = 0
        self.queries_by_mode: Counter = Counter()
        self.queries_by_domain: Counter = Counter()
        self.queries_by_layer: Counter = Counter()
        self.errors_by_domain: Counter = Counter()
        self.employment_metrics: Counter = Counter()
        self.jurisdiction_counts: Counter = Counter()
        self.statute_references: Counter = Counter()
        self._latencies: deque = deque(maxlen=10000)
        self._layer_latencies: Dict[str, deque] = defaultdict(lambda: deque(maxlen=5000))
        self._start_time: float = time.monotonic()
        self._last_reset: str = datetime.now(timezone.utc).isoformat()

    def record_query(self, trace: QueryTrace) -> None:
        """Record metrics from a completed query trace."""
        with self._lock:
            self.total_queries += 1
            self._latencies.append(trace.total_duration_ms)
            self._layer_latencies[trace.response_layer.value].append(trace.total_duration_ms)
            self.queries_by_mode[trace.response_mode] += 1
            self.queries_by_layer[trace.response_layer.value] += 1
            if trace.employment_domain:
                self.queries_by_domain[trace.employment_domain] += 1
            if trace.jurisdiction:
                self.jurisdiction_counts[trace.jurisdiction] += 1
            for statute in trace.statutes_referenced:
                self.statute_references[statute] += 1
            if trace.cached:
                self.total_cache_hits += 1
            else:
                self.total_cache_misses += 1
            if trace.multi_doctrine:
                self.total_multi_doctrine += 1
            self.total_doctrine_lookups += trace.doctrine_hits
            if trace.response_layer == ResponseLayer.DEEP_ANALYSIS:
                self.total_deep_analyses += 1
            if trace.search_results > 0:
                self.total_search_queries += 1
            if trace.error:
                self.total_errors += 1

    def record_error(self, domain: ErrorDomain) -> None:
        """Record an error event."""
        with self._lock:
            self.total_errors += 1
            self.errors_by_domain[domain.value] += 1

    def record_employment_metric(self, metric_type: EmploymentMetricType) -> None:
        """Record an employment-law-specific metric."""
        with self._lock:
            self.employment_metrics[metric_type.value] += 1

    def record_citation_lookup(self) -> None:
        """Increment citation lookup counter."""
        with self._lock:
            self.total_citation_lookups += 1

    def get_latency_stats(self) -> Dict[str, float]:
        """Compute latency statistics from ring buffer."""
        with self._lock:
            if not self._latencies:
                return {"p50": 0.0, "p90": 0.0, "p99": 0.0, "mean": 0.0, "min": 0.0, "max": 0.0}
            sorted_lat = sorted(self._latencies)
            n = len(sorted_lat)
            return {
                "p50": round(sorted_lat[int(n * 0.50)], 3),
                "p90": round(sorted_lat[min(int(n * 0.90), n - 1)], 3),
                "p99": round(sorted_lat[min(int(n * 0.99), n - 1)], 3),
                "mean": round(sum(sorted_lat) / n, 3),
                "min": round(sorted_lat[0], 3),
                "max": round(sorted_lat[-1], 3),
            }

    def get_layer_latency_stats(self) -> Dict[str, Dict[str, float]]:
        """Compute latency statistics per response layer."""
        with self._lock:
            stats: Dict[str, Dict[str, float]] = {}
            for layer, latencies in self._layer_latencies.items():
                if not latencies:
                    stats[layer] = {"p50": 0.0, "p90": 0.0, "mean": 0.0, "count": 0}
                    continue
                sorted_lat = sorted(latencies)
                n = len(sorted_lat)
                stats[layer] = {
                    "p50": round(sorted_lat[int(n * 0.50)], 3),
                    "p90": round(sorted_lat[min(int(n * 0.90), n - 1)], 3),
                    "mean": round(sum(sorted_lat) / n, 3),
                    "count": n,
                }
            return stats

    def get_cache_hit_rate(self) -> float:
        """Compute cache hit rate."""
        total = self.total_cache_hits + self.total_cache_misses
        if total == 0:
            return 0.0
        return round(self.total_cache_hits / total, 4)

    def get_error_rate(self) -> float:
        """Compute error rate."""
        if self.total_queries == 0:
            return 0.0
        return round(self.total_errors / self.total_queries, 4)

    def get_uptime_seconds(self) -> float:
        """Get engine uptime in seconds."""
        return round(time.monotonic() - self._start_time, 2)

    def get_queries_per_second(self) -> float:
        """Compute average QPS."""
        uptime = self.get_uptime_seconds()
        if uptime == 0:
            return 0.0
        return round(self.total_queries / uptime, 4)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize all metrics to dictionary."""
        latency = self.get_latency_stats()
        return {
            "total_queries": self.total_queries,
            "total_errors": self.total_errors,
            "error_rate": self.get_error_rate(),
            "total_cache_hits": self.total_cache_hits,
            "total_cache_misses": self.total_cache_misses,
            "cache_hit_rate": self.get_cache_hit_rate(),
            "total_search_queries": self.total_search_queries,
            "total_deep_analyses": self.total_deep_analyses,
            "total_multi_doctrine": self.total_multi_doctrine,
            "total_doctrine_lookups": self.total_doctrine_lookups,
            "total_citation_lookups": self.total_citation_lookups,
            "latency": latency,
            "layer_latency": self.get_layer_latency_stats(),
            "queries_by_mode": dict(self.queries_by_mode),
            "queries_by_domain": dict(self.queries_by_domain),
            "queries_by_layer": dict(self.queries_by_layer),
            "errors_by_domain": dict(self.errors_by_domain),
            "employment_metrics": dict(self.employment_metrics),
            "jurisdiction_counts": dict(self.jurisdiction_counts),
            "statute_references": dict(self.statute_references.most_common(20)),
            "uptime_seconds": self.get_uptime_seconds(),
            "queries_per_second": self.get_queries_per_second(),
            "last_reset": self._last_reset,
        }

    def reset(self) -> None:
        """Reset all counters."""
        with self._lock:
            self.total_queries = 0
            self.total_errors = 0
            self.total_cache_hits = 0
            self.total_cache_misses = 0
            self.total_search_queries = 0
            self.total_deep_analyses = 0
            self.total_multi_doctrine = 0
            self.total_doctrine_lookups = 0
            self.total_citation_lookups = 0
            self.queries_by_mode.clear()
            self.queries_by_domain.clear()
            self.queries_by_layer.clear()
            self.errors_by_domain.clear()
            self.employment_metrics.clear()
            self.jurisdiction_counts.clear()
            self.statute_references.clear()
            self._latencies.clear()
            self._layer_latencies.clear()
            self._start_time = time.monotonic()
            self._last_reset = datetime.now(timezone.utc).isoformat()


# ============================================================================
# PERFORMANCE TRACKER
# ============================================================================

class PerformanceTracker:
    """Tracks per-endpoint and per-operation performance."""

    def __init__(self, window_size: int = 1000) -> None:
        """Initialize with configurable window size."""
        self._lock = threading.Lock()
        self._window_size = window_size
        self._endpoint_latencies: Dict[str, deque] = defaultdict(
            lambda: deque(maxlen=window_size)
        )
        self._operation_counts: Counter = Counter()
        self._slow_queries: deque = deque(maxlen=100)
        self._slow_threshold_ms: float = 5000.0

    def record_endpoint(self, endpoint: str, latency_ms: float) -> None:
        """Record a latency measurement for an endpoint."""
        with self._lock:
            self._endpoint_latencies[endpoint].append(latency_ms)
            self._operation_counts[endpoint] += 1
            if latency_ms > self._slow_threshold_ms:
                self._slow_queries.append({
                    "endpoint": endpoint,
                    "latency_ms": round(latency_ms, 3),
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })

    def get_endpoint_stats(self, endpoint: str) -> Dict[str, float]:
        """Get performance statistics for a specific endpoint."""
        with self._lock:
            latencies = self._endpoint_latencies.get(endpoint)
            if not latencies:
                return {"count": 0, "p50": 0.0, "p90": 0.0, "p99": 0.0, "mean": 0.0}
            sorted_lat = sorted(latencies)
            n = len(sorted_lat)
            return {
                "count": n,
                "p50": round(sorted_lat[int(n * 0.50)], 3),
                "p90": round(sorted_lat[min(int(n * 0.90), n - 1)], 3),
                "p99": round(sorted_lat[min(int(n * 0.99), n - 1)], 3),
                "mean": round(sum(sorted_lat) / n, 3),
            }

    def get_all_stats(self) -> Dict[str, Any]:
        """Get all endpoint statistics."""
        with self._lock:
            stats: Dict[str, Any] = {}
            for endpoint in self._endpoint_latencies:
                stats[endpoint] = self.get_endpoint_stats(endpoint)
            stats["_slow_queries_count"] = len(self._slow_queries)
            stats["_slow_queries_recent"] = list(self._slow_queries)[-10:]
            stats["_operation_counts"] = dict(self._operation_counts)
            return stats

    def get_slow_queries(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent slow queries."""
        with self._lock:
            return list(self._slow_queries)[-limit:]

    def set_slow_threshold(self, threshold_ms: float) -> None:
        """Set the slow query threshold."""
        self._slow_threshold_ms = threshold_ms


# ============================================================================
# METRICS AGGREGATOR
# ============================================================================

class MetricsAggregator:
    """Rolling window aggregation for dashboard metrics."""

    def __init__(self, window_minutes: int = 60) -> None:
        """Initialize with a rolling window size."""
        self._lock = threading.Lock()
        self._window_minutes = window_minutes
        self._minute_buckets: Dict[str, Dict[str, float]] = {}
        self._current_minute: str = ""

    def _get_minute_key(self) -> str:
        """Get the current minute key."""
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M")

    def _prune_old_buckets(self) -> None:
        """Remove buckets older than the window."""
        now = datetime.now(timezone.utc)
        cutoff_keys: List[str] = []
        for key in self._minute_buckets:
            try:
                bucket_time = datetime.fromisoformat(key + ":00+00:00")
                age_minutes = (now - bucket_time).total_seconds() / 60.0
                if age_minutes > self._window_minutes:
                    cutoff_keys.append(key)
            except (ValueError, TypeError):
                cutoff_keys.append(key)
        for key in cutoff_keys:
            del self._minute_buckets[key]

    def record(self, metric_name: str, value: float) -> None:
        """Record a metric value into the current minute bucket."""
        with self._lock:
            minute_key = self._get_minute_key()
            if minute_key not in self._minute_buckets:
                self._prune_old_buckets()
                self._minute_buckets[minute_key] = {}
            bucket = self._minute_buckets[minute_key]
            count_key = f"{metric_name}_count"
            sum_key = f"{metric_name}_sum"
            bucket[count_key] = bucket.get(count_key, 0.0) + 1.0
            bucket[sum_key] = bucket.get(sum_key, 0.0) + value

    def get_window_average(self, metric_name: str) -> float:
        """Get the average value across the rolling window."""
        with self._lock:
            total_sum = 0.0
            total_count = 0.0
            sum_key = f"{metric_name}_sum"
            count_key = f"{metric_name}_count"
            for bucket in self._minute_buckets.values():
                total_sum += bucket.get(sum_key, 0.0)
                total_count += bucket.get(count_key, 0.0)
            if total_count == 0:
                return 0.0
            return round(total_sum / total_count, 4)

    def get_window_total(self, metric_name: str) -> float:
        """Get the total value across the rolling window."""
        with self._lock:
            total = 0.0
            sum_key = f"{metric_name}_sum"
            for bucket in self._minute_buckets.values():
                total += bucket.get(sum_key, 0.0)
            return round(total, 4)

    def get_window_count(self, metric_name: str) -> int:
        """Get the count of events across the rolling window."""
        with self._lock:
            total = 0.0
            count_key = f"{metric_name}_count"
            for bucket in self._minute_buckets.values():
                total += bucket.get(count_key, 0.0)
            return int(total)

    def get_summary(self) -> Dict[str, Any]:
        """Get summary of all metrics in the window."""
        with self._lock:
            all_metrics: set = set()
            for bucket in self._minute_buckets.values():
                for key in bucket:
                    if key.endswith("_count"):
                        all_metrics.add(key.replace("_count", ""))
            summary: Dict[str, Any] = {
                "window_minutes": self._window_minutes,
                "active_buckets": len(self._minute_buckets),
            }
            for metric in sorted(all_metrics):
                summary[metric] = {
                    "count": self.get_window_count(metric),
                    "total": self.get_window_total(metric),
                    "average": self.get_window_average(metric),
                }
            return summary


# ============================================================================
# AUDIT TRAIL
# ============================================================================

class AuditTrail:
    """Append-only JSONL audit log with SHA-256 hash chain for tamper evidence."""

    def __init__(self, log_dir: Path) -> None:
        """Initialize audit trail with log directory."""
        self._log_dir = log_dir
        self._log_dir.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._chain_hash: str = hashlib.sha256(b"LG07_EMPLOYMENT_GENESIS").hexdigest()
        self._sequence: int = 0
        self._query_log = self._log_dir / "query_traces.jsonl"
        self._error_log = self._log_dir / "error_spine.jsonl"
        self._mutation_log = self._log_dir / "doctrine_mutations.jsonl"
        self._citation_log = self._log_dir / "citation_lookups.jsonl"
        self._performance_log = self._log_dir / "performance_metrics.jsonl"
        logger.info("AuditTrail initialized at {}", self._log_dir)

    def _next_chain_hash(self, data: str) -> str:
        """Compute next hash in chain."""
        combined = f"{self._chain_hash}:{data}"
        new_hash = hashlib.sha256(combined.encode("utf-8")).hexdigest()
        self._chain_hash = new_hash
        self._sequence += 1
        return new_hash

    def _write_line(self, path: Path, record: Dict[str, Any]) -> None:
        """Write a single JSONL line with chain hash."""
        with self._lock:
            record["_seq"] = self._sequence
            record["_chain_hash"] = self._next_chain_hash(json.dumps(record, sort_keys=True))
            record["_timestamp"] = datetime.now(timezone.utc).isoformat()
            line = json.dumps(record, default=str) + "\n"
            with open(path, "a", encoding="utf-8") as f:
                f.write(line)

    def log_query(self, trace: QueryTrace) -> None:
        """Log a completed query trace."""
        self._write_line(self._query_log, trace.to_dict())

    def log_error(self, error: ErrorRecord) -> None:
        """Log an error event."""
        self._write_line(self._error_log, error.to_dict())

    def log_mutation(self, mutation: DoctrineMutationRecord) -> None:
        """Log a doctrine mutation."""
        self._write_line(self._mutation_log, mutation.to_dict())

    def log_citation(self, lookup: CitationLookupRecord) -> None:
        """Log a citation lookup."""
        self._write_line(self._citation_log, lookup.to_dict())

    def log_performance(self, metrics: Dict[str, Any]) -> None:
        """Log periodic performance snapshot."""
        self._write_line(self._performance_log, metrics)

    def get_chain_state(self) -> Dict[str, Any]:
        """Get current chain state."""
        return {
            "chain_hash": self._chain_hash,
            "sequence": self._sequence,
            "log_dir": str(self._log_dir),
        }

    def verify_chain(self, log_file: str) -> Dict[str, Any]:
        """Verify the hash chain of a log file."""
        path = self._log_dir / log_file
        if not path.exists():
            return {"valid": False, "error": "File not found", "records": 0}
        records = 0
        valid = True
        last_error = ""
        prev_hash = hashlib.sha256(b"LG07_EMPLOYMENT_GENESIS").hexdigest()
        with open(path, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                try:
                    record = json.loads(line.strip())
                    stored_hash = record.pop("_chain_hash", "")
                    seq = record.pop("_seq", -1)
                    data_str = json.dumps(record, sort_keys=True)
                    expected = hashlib.sha256(f"{prev_hash}:{data_str}".encode()).hexdigest()
                    if stored_hash != expected:
                        valid = False
                        last_error = f"Line {line_num}: hash mismatch"
                        break
                    prev_hash = stored_hash
                    records += 1
                except (json.JSONDecodeError, KeyError) as e:
                    valid = False
                    last_error = f"Line {line_num}: {e}"
                    break
        return {"valid": valid, "records": records, "last_error": last_error}


# ============================================================================
# ERROR TRACKER
# ============================================================================

class ErrorTracker:
    """Domain-classified error tracking with alerting thresholds."""

    def __init__(self, max_history: int = 1000) -> None:
        """Initialize error tracker."""
        self._lock = threading.Lock()
        self._errors: deque = deque(maxlen=max_history)
        self._domain_counts: Counter = Counter()
        self._severity_counts: Counter = Counter()
        self._recent_window_seconds: float = 300.0
        self._alert_threshold: int = 10

    def record(self, domain: ErrorDomain, message: str, severity: str = "MEDIUM",
               stack_trace: str = "", query_context: str = "") -> ErrorRecord:
        """Record a new error."""
        error = ErrorRecord(
            error_id=str(uuid.uuid4()),
            timestamp=datetime.now(timezone.utc).isoformat(),
            domain=domain,
            message=message,
            stack_trace=stack_trace,
            query_context=query_context,
            severity=severity,
        )
        with self._lock:
            self._errors.append(error)
            self._domain_counts[domain.value] += 1
            self._severity_counts[severity] += 1
        logger.error("Error [{}][{}]: {}", domain.value, severity, message)
        return error

    def get_recent(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get most recent errors."""
        with self._lock:
            return [e.to_dict() for e in list(self._errors)[-limit:]]

    def get_domain_counts(self) -> Dict[str, int]:
        """Get error counts by domain."""
        with self._lock:
            return dict(self._domain_counts)

    def get_severity_counts(self) -> Dict[str, int]:
        """Get error counts by severity."""
        with self._lock:
            return dict(self._severity_counts)

    def is_alerting(self) -> bool:
        """Check if error rate exceeds alert threshold in recent window."""
        with self._lock:
            now = datetime.now(timezone.utc)
            recent_count = 0
            for error in reversed(self._errors):
                try:
                    error_time = datetime.fromisoformat(error.timestamp)
                    age = (now - error_time).total_seconds()
                    if age <= self._recent_window_seconds:
                        recent_count += 1
                    else:
                        break
                except (ValueError, TypeError):
                    continue
            return recent_count >= self._alert_threshold

    def get_stats(self) -> Dict[str, Any]:
        """Get error tracker statistics."""
        return {
            "total_errors": len(self._errors),
            "domain_counts": self.get_domain_counts(),
            "severity_counts": self.get_severity_counts(),
            "is_alerting": self.is_alerting(),
            "alert_threshold": self._alert_threshold,
            "recent_window_seconds": self._recent_window_seconds,
        }


# ============================================================================
# DOCTRINE MUTATION LOG
# ============================================================================

class DoctrineMutationLog:
    """Track and audit all doctrine cache mutations."""

    def __init__(self, audit_trail: AuditTrail) -> None:
        """Initialize mutation log."""
        self._audit = audit_trail
        self._lock = threading.Lock()
        self._mutations: deque = deque(maxlen=500)

    def record(self, mutation_type: MutationType, origin: MutationOrigin,
               topic: str, before_hash: str, after_hash: str,
               description: str, confidence_delta: float = 0.0) -> DoctrineMutationRecord:
        """Record a doctrine mutation."""
        mutation = DoctrineMutationRecord(
            mutation_id=str(uuid.uuid4()),
            timestamp=datetime.now(timezone.utc).isoformat(),
            mutation_type=mutation_type,
            origin=origin,
            topic=topic,
            before_hash=before_hash,
            after_hash=after_hash,
            description=description,
            confidence_delta=confidence_delta,
        )
        with self._lock:
            self._mutations.append(mutation)
        self._audit.log_mutation(mutation)
        logger.info("Doctrine mutation [{}]: {} - {}", mutation_type.value, topic, description)
        return mutation

    def get_recent(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recent mutations."""
        with self._lock:
            return [m.to_dict() for m in list(self._mutations)[-limit:]]

    def get_mutations_for_topic(self, topic: str) -> List[Dict[str, Any]]:
        """Get all mutations for a specific topic."""
        with self._lock:
            return [m.to_dict() for m in self._mutations if m.topic == topic]


# ============================================================================
# TELEMETRY COLLECTOR (SINGLETON)
# ============================================================================

class TelemetryCollector:
    """Main telemetry collector combining all sub-components."""

    _instance: ClassVar[Optional[TelemetryCollector]] = None
    _lock: ClassVar[threading.Lock] = threading.Lock()

    def __init__(self, log_dir: Optional[Path] = None) -> None:
        """Initialize all telemetry components."""
        if log_dir is None:
            log_dir = Path("O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/LG07_employment_law/telemetry")
        self.log_dir = log_dir
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.metrics = EngineMetrics()
        self.performance = PerformanceTracker(window_size=5000)
        self.aggregator = MetricsAggregator(window_minutes=60)
        self.audit = AuditTrail(log_dir)
        self.errors = ErrorTracker(max_history=2000)
        self.mutations = DoctrineMutationLog(self.audit)
        self.engine_id = "LG07"
        self.engine_name = "Employment Law Engine"
        self.engine_version = "1.0.0"
        self._boot_time = datetime.now(timezone.utc).isoformat()
        logger.info("TelemetryCollector initialized for LG07 Employment Law Engine")

    @classmethod
    def get_instance(cls, log_dir: Optional[Path] = None) -> TelemetryCollector:
        """Get or create the singleton instance."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls(log_dir=log_dir)
        return cls._instance

    @classmethod
    def reset_instance(cls) -> None:
        """Reset the singleton for testing."""
        with cls._lock:
            cls._instance = None

    def trace_query(self, query_text: str, response_mode: str = "FAST") -> QueryTrace:
        """Start a new query trace."""
        trace = QueryTrace(
            trace_id=str(uuid.uuid4()),
            query_text=query_text,
            start_time=time.monotonic(),
            response_mode=response_mode,
        )
        return trace

    def complete_trace(self, trace: QueryTrace) -> None:
        """Complete and record a query trace."""
        trace.complete()
        self.metrics.record_query(trace)
        self.aggregator.record("query_latency", trace.total_duration_ms)
        self.aggregator.record("query_count", 1)
        if trace.error:
            self.aggregator.record("error_count", 1)
        self.audit.log_query(trace)

    def log_error(self, domain: ErrorDomain, message: str, severity: str = "MEDIUM",
                  stack_trace: str = "", query_context: str = "") -> ErrorRecord:
        """Log an error event through all channels."""
        error = self.errors.record(domain, message, severity, stack_trace, query_context)
        self.metrics.record_error(domain)
        self.audit.log_error(error)
        self.aggregator.record("error_count", 1)
        return error

    def record_doctrine_mutation(self, mutation_type: MutationType, origin: MutationOrigin,
                                  topic: str, before_hash: str, after_hash: str,
                                  description: str, confidence_delta: float = 0.0) -> DoctrineMutationRecord:
        """Record a doctrine mutation."""
        return self.mutations.record(
            mutation_type, origin, topic, before_hash, after_hash, description, confidence_delta
        )

    def record_citation_lookup(self, lookup_type: CitationLookupType, citation: str,
                                found: bool, source: str, latency_ms: float) -> CitationLookupRecord:
        """Record a citation lookup."""
        record = CitationLookupRecord(
            lookup_id=str(uuid.uuid4()),
            timestamp=datetime.now(timezone.utc).isoformat(),
            lookup_type=lookup_type,
            citation=citation,
            found=found,
            source=source,
            latency_ms=latency_ms,
        )
        self.metrics.record_citation_lookup()
        self.audit.log_citation(record)
        return record

    def record_employment_metric(self, metric_type: EmploymentMetricType) -> None:
        """Record an employment-law-specific metric."""
        self.metrics.record_employment_metric(metric_type)
        self.aggregator.record(f"emp_{metric_type.value}", 1)

    def get_health(self) -> Dict[str, Any]:
        """Get comprehensive health status."""
        return {
            "engine_id": self.engine_id,
            "engine_name": self.engine_name,
            "engine_version": self.engine_version,
            "boot_time": self._boot_time,
            "metrics": self.metrics.to_dict(),
            "errors": self.errors.get_stats(),
            "audit_chain": self.audit.get_chain_state(),
            "is_alerting": self.errors.is_alerting(),
        }

    def snapshot_performance(self) -> None:
        """Take a periodic performance snapshot and log it."""
        snapshot = {
            "metrics": self.metrics.to_dict(),
            "aggregator": self.aggregator.get_summary(),
            "performance": self.performance.get_all_stats(),
        }
        self.audit.log_performance(snapshot)
        logger.debug("Performance snapshot recorded for LG07")


# ============================================================================
# MODULE-LEVEL CONVENIENCE FUNCTIONS
# ============================================================================

def get_telemetry(log_dir: Optional[Path] = None) -> TelemetryCollector:
    """Get the global TelemetryCollector instance."""
    return TelemetryCollector.get_instance(log_dir=log_dir)


def trace_query(query_text: str, response_mode: str = "FAST") -> QueryTrace:
    """Start a new query trace using the global collector."""
    return get_telemetry().trace_query(query_text, response_mode)


def complete_trace(trace: QueryTrace) -> None:
    """Complete a query trace using the global collector."""
    get_telemetry().complete_trace(trace)


def log_error(domain: ErrorDomain, message: str, severity: str = "MEDIUM",
              stack_trace: str = "", query_context: str = "") -> ErrorRecord:
    """Log an error through the global collector."""
    return get_telemetry().log_error(domain, message, severity, stack_trace, query_context)


def record_doctrine_mutation(mutation_type: MutationType, origin: MutationOrigin,
                              topic: str, before_hash: str, after_hash: str,
                              description: str, confidence_delta: float = 0.0) -> DoctrineMutationRecord:
    """Record a doctrine mutation through the global collector."""
    return get_telemetry().record_doctrine_mutation(
        mutation_type, origin, topic, before_hash, after_hash, description, confidence_delta
    )


def record_citation_lookup(lookup_type: CitationLookupType, citation: str,
                            found: bool, source: str, latency_ms: float) -> CitationLookupRecord:
    """Record a citation lookup through the global collector."""
    return get_telemetry().record_citation_lookup(lookup_type, citation, found, source, latency_ms)
