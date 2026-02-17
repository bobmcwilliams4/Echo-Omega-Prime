"""
LM08 Due Diligence Engine - Telemetry Module
==============================================
Full query tracing, latency tracking, error domain classification,
metrics collection, drift watching, and coverage mapping.
"""

from __future__ import annotations

import hashlib
import json
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

from loguru import logger


class ErrorDomain(str, Enum):
    """Classification of error domains for telemetry."""
    DOCTRINE_MISS = "doctrine_miss"
    AUTHORITY_CONFLICT = "authority_conflict"
    SEMANTIC_AMBIGUITY = "semantic_ambiguity"
    VECTOR_SEARCH_FAIL = "vector_search_fail"
    CONFIDENCE_LOW = "confidence_low"
    INPUT_VALIDATION = "input_validation"
    TIMEOUT = "timeout"
    INTERNAL = "internal"
    DRIFT_DETECTED = "drift_detected"
    FRAGILITY_HIGH = "fragility_high"


class QueryPhase(str, Enum):
    """Phases of query processing."""
    RECEIVED = "received"
    NORMALIZED = "normalized"
    DOCTRINE_LOOKUP = "doctrine_lookup"
    VECTOR_SEARCH = "vector_search"
    DEEP_ANALYSIS = "deep_analysis"
    AUTHORITY_RESOLUTION = "authority_resolution"
    CONFIDENCE_SCORING = "confidence_scoring"
    RESPONSE_GENERATION = "response_generation"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class QueryTrace:
    """Full trace of a single query through the engine."""
    trace_id: str
    query_text: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    phases: List[Dict[str, Any]] = field(default_factory=list)
    total_latency_ms: float = 0.0
    doctrine_hits: List[str] = field(default_factory=list)
    doctrine_misses: List[str] = field(default_factory=list)
    errors: List[Dict[str, str]] = field(default_factory=list)
    response_mode: str = "FAST"
    confidence_level: str = "DEFENSIBLE"
    determinism_hash: str = ""
    issue_categories: List[str] = field(default_factory=list)

    def add_phase(self, phase: QueryPhase, latency_ms: float, details: Optional[Dict] = None) -> None:
        """Record a processing phase."""
        self.phases.append({
            "phase": phase.value,
            "latency_ms": round(latency_ms, 3),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "details": details or {},
        })
        self.total_latency_ms += latency_ms

    def add_error(self, domain: ErrorDomain, message: str, context: Optional[str] = None) -> None:
        """Record an error during processing."""
        self.errors.append({
            "domain": domain.value,
            "message": message,
            "context": context or "",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

    def finalize(self) -> None:
        """Compute determinism hash and mark complete."""
        raw = f"{self.query_text}|{self.response_mode}|{self.confidence_level}|{len(self.doctrine_hits)}"
        self.determinism_hash = hashlib.sha256(raw.encode()).hexdigest()


@dataclass
class LatencyBucket:
    """Latency distribution bucket."""
    label: str
    min_ms: float
    max_ms: float
    count: int = 0

    def matches(self, latency_ms: float) -> bool:
        return self.min_ms <= latency_ms < self.max_ms


class MetricsCollector:
    """Collects and aggregates engine performance metrics."""

    def __init__(self) -> None:
        self._query_count: int = 0
        self._error_count: int = 0
        self._total_latency_ms: float = 0.0
        self._min_latency_ms: float = float("inf")
        self._max_latency_ms: float = 0.0
        self._doctrine_hit_count: int = 0
        self._doctrine_miss_count: int = 0
        self._mode_counts: Dict[str, int] = defaultdict(int)
        self._confidence_counts: Dict[str, int] = defaultdict(int)
        self._error_domain_counts: Dict[str, int] = defaultdict(int)
        self._category_counts: Dict[str, int] = defaultdict(int)
        self._hourly_queries: Dict[str, int] = defaultdict(int)
        self._latency_buckets: List[LatencyBucket] = [
            LatencyBucket("fast", 0, 50),
            LatencyBucket("normal", 50, 200),
            LatencyBucket("slow", 200, 1000),
            LatencyBucket("very_slow", 1000, 5000),
            LatencyBucket("timeout", 5000, float("inf")),
        ]
        self._start_time = time.time()
        logger.info("MetricsCollector initialized")

    def record_query(self, trace: QueryTrace) -> None:
        """Record metrics from a completed query trace."""
        self._query_count += 1
        self._total_latency_ms += trace.total_latency_ms

        if trace.total_latency_ms < self._min_latency_ms:
            self._min_latency_ms = trace.total_latency_ms
        if trace.total_latency_ms > self._max_latency_ms:
            self._max_latency_ms = trace.total_latency_ms

        self._doctrine_hit_count += len(trace.doctrine_hits)
        self._doctrine_miss_count += len(trace.doctrine_misses)
        self._mode_counts[trace.response_mode] += 1
        self._confidence_counts[trace.confidence_level] += 1

        for error in trace.errors:
            self._error_count += 1
            self._error_domain_counts[error["domain"]] += 1

        for cat in trace.issue_categories:
            self._category_counts[cat] += 1

        hour_key = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H")
        self._hourly_queries[hour_key] += 1

        for bucket in self._latency_buckets:
            if bucket.matches(trace.total_latency_ms):
                bucket.count += 1
                break

    def get_metrics(self) -> Dict[str, Any]:
        """Return comprehensive metrics snapshot."""
        uptime_seconds = time.time() - self._start_time
        avg_latency = (self._total_latency_ms / self._query_count) if self._query_count > 0 else 0.0
        hit_rate = (self._doctrine_hit_count / max(self._doctrine_hit_count + self._doctrine_miss_count, 1))
        error_rate = (self._error_count / max(self._query_count, 1))
        qph = (self._query_count / max(uptime_seconds / 3600, 0.001))

        return {
            "engine_id": "LM08",
            "engine_name": "Due Diligence",
            "uptime_seconds": round(uptime_seconds, 1),
            "total_queries": self._query_count,
            "total_errors": self._error_count,
            "error_rate": round(error_rate, 4),
            "queries_per_hour": round(qph, 2),
            "latency": {
                "average_ms": round(avg_latency, 2),
                "min_ms": round(self._min_latency_ms, 2) if self._min_latency_ms != float("inf") else 0,
                "max_ms": round(self._max_latency_ms, 2),
                "distribution": {b.label: b.count for b in self._latency_buckets},
            },
            "doctrine": {
                "hits": self._doctrine_hit_count,
                "misses": self._doctrine_miss_count,
                "hit_rate": round(hit_rate, 4),
            },
            "response_modes": dict(self._mode_counts),
            "confidence_levels": dict(self._confidence_counts),
            "error_domains": dict(self._error_domain_counts),
            "issue_categories": dict(self._category_counts),
            "hourly_queries": dict(self._hourly_queries),
        }


class DriftWatcher:
    """Monitors for doctrine drift over time."""

    def __init__(self, drift_threshold: float = 0.15) -> None:
        self._baseline_hashes: Dict[str, str] = {}
        self._drift_events: List[Dict[str, Any]] = []
        self._check_count: int = 0
        self._drift_threshold = drift_threshold
        logger.info("DriftWatcher initialized | threshold={}", drift_threshold)

    def set_baseline(self, doctrine_id: str, content_hash: str) -> None:
        """Set a baseline hash for a doctrine block."""
        self._baseline_hashes[doctrine_id] = content_hash

    def check_drift(self, doctrine_id: str, current_hash: str) -> Optional[Dict[str, Any]]:
        """Check if a doctrine has drifted from baseline."""
        self._check_count += 1
        baseline = self._baseline_hashes.get(doctrine_id)
        if baseline is None:
            self.set_baseline(doctrine_id, current_hash)
            return None

        if baseline != current_hash:
            event = {
                "doctrine_id": doctrine_id,
                "baseline_hash": baseline[:16],
                "current_hash": current_hash[:16],
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "severity": "WARNING",
            }
            self._drift_events.append(event)
            logger.warning("Doctrine drift detected | doctrine={} | baseline={} | current={}",
                           doctrine_id, baseline[:16], current_hash[:16])
            return event
        return None

    def get_drift_report(self) -> Dict[str, Any]:
        """Return drift monitoring report."""
        return {
            "total_checks": self._check_count,
            "total_drifts": len(self._drift_events),
            "drift_rate": round(len(self._drift_events) / max(self._check_count, 1), 4),
            "baseline_count": len(self._baseline_hashes),
            "recent_drifts": self._drift_events[-10:],
        }


class CoverageMap:
    """Tracks which doctrines have been triggered and identifies gaps."""

    def __init__(self) -> None:
        self._registered_doctrines: Dict[str, Dict[str, Any]] = {}
        self._trigger_counts: Dict[str, int] = defaultdict(int)
        self._last_triggered: Dict[str, str] = {}
        self._gap_queries: List[Dict[str, str]] = []
        logger.info("CoverageMap initialized")

    def register_doctrine(self, doctrine_id: str, topic: str, domain: str) -> None:
        """Register a doctrine block for coverage tracking."""
        self._registered_doctrines[doctrine_id] = {
            "topic": topic,
            "domain": domain,
            "registered_at": datetime.now(timezone.utc).isoformat(),
        }

    def record_trigger(self, doctrine_id: str) -> None:
        """Record that a doctrine was triggered by a query."""
        self._trigger_counts[doctrine_id] += 1
        self._last_triggered[doctrine_id] = datetime.now(timezone.utc).isoformat()

    def record_gap(self, query_text: str, attempted_domain: str) -> None:
        """Record a query that found no matching doctrine (epistemic gap)."""
        self._gap_queries.append({
            "query": query_text[:200],
            "domain": attempted_domain,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

    def get_coverage_report(self) -> Dict[str, Any]:
        """Return coverage analysis."""
        total = len(self._registered_doctrines)
        triggered = sum(1 for d in self._registered_doctrines if self._trigger_counts.get(d, 0) > 0)
        untriggered = [
            {"id": d, "topic": info["topic"], "domain": info["domain"]}
            for d, info in self._registered_doctrines.items()
            if self._trigger_counts.get(d, 0) == 0
        ]
        hot_doctrines = sorted(
            [(d, c) for d, c in self._trigger_counts.items()],
            key=lambda x: x[1],
            reverse=True,
        )[:10]

        return {
            "total_doctrines": total,
            "triggered": triggered,
            "untriggered_count": total - triggered,
            "coverage_pct": round(triggered / max(total, 1) * 100, 1),
            "untriggered_doctrines": untriggered[:20],
            "hot_doctrines": [{"id": d, "count": c} for d, c in hot_doctrines],
            "epistemic_gaps": len(self._gap_queries),
            "recent_gaps": self._gap_queries[-10:],
        }


class AuditTrail:
    """Append-only JSONL audit trail for forensic review."""

    def __init__(self, log_dir: Path) -> None:
        self._log_dir = log_dir
        self._log_dir.mkdir(parents=True, exist_ok=True)
        self._log_file = self._log_dir / "audit_trail.jsonl"
        self._entry_count = 0
        logger.info("AuditTrail initialized | path={}", self._log_file)

    def log_query(self, trace: QueryTrace) -> None:
        """Append a query trace to the audit trail."""
        entry = {
            "type": "query",
            "trace_id": trace.trace_id,
            "timestamp": trace.timestamp,
            "query_text": trace.query_text[:500],
            "response_mode": trace.response_mode,
            "confidence_level": trace.confidence_level,
            "total_latency_ms": trace.total_latency_ms,
            "doctrine_hits": len(trace.doctrine_hits),
            "doctrine_misses": len(trace.doctrine_misses),
            "errors": len(trace.errors),
            "determinism_hash": trace.determinism_hash,
            "issue_categories": trace.issue_categories,
        }
        self._write_entry(entry)

    def log_event(self, event_type: str, details: Dict[str, Any]) -> None:
        """Log a generic event to the audit trail."""
        entry = {
            "type": event_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "details": details,
        }
        self._write_entry(entry)

    def _write_entry(self, entry: Dict[str, Any]) -> None:
        """Write a single entry to the JSONL file."""
        try:
            with self._log_file.open("a", encoding="utf-8") as f:
                f.write(json.dumps(entry, default=str) + "\n")
            self._entry_count += 1
        except Exception as e:
            logger.error("Failed to write audit entry: {}", e)

    def get_stats(self) -> Dict[str, Any]:
        """Return audit trail statistics."""
        file_size = self._log_file.stat().st_size if self._log_file.exists() else 0
        return {
            "log_file": str(self._log_file),
            "entry_count": self._entry_count,
            "file_size_bytes": file_size,
            "file_size_mb": round(file_size / (1024 * 1024), 2),
        }


class DueDiligenceTelemetry:
    """Unified telemetry facade for the Due Diligence engine."""

    def __init__(self, log_dir: Optional[Path] = None) -> None:
        if log_dir is None:
            log_dir = Path("O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/LM08_due_diligence/logs")
        self.metrics = MetricsCollector()
        self.drift = DriftWatcher()
        self.coverage = CoverageMap()
        self.audit = AuditTrail(log_dir)
        logger.info("DueDiligenceTelemetry fully initialized")

    def record_query(self, trace: QueryTrace) -> None:
        """Record a completed query across all telemetry systems."""
        trace.finalize()
        self.metrics.record_query(trace)
        self.audit.log_query(trace)
        for hit in trace.doctrine_hits:
            self.coverage.record_trigger(hit)

    def get_full_report(self) -> Dict[str, Any]:
        """Return comprehensive telemetry report."""
        return {
            "engine_id": "LM08",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "metrics": self.metrics.get_metrics(),
            "drift": self.drift.get_drift_report(),
            "coverage": self.coverage.get_coverage_report(),
            "audit": self.audit.get_stats(),
        }
