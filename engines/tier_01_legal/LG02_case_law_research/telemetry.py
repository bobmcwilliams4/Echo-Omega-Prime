"""
LG02 Case Law Research Engine - Telemetry & Tracing Layer
==========================================================
Authority: 11.0 SOVEREIGN | Echo Omega Prime
Version: 2.0.0 | Port: 8392

Provides structured observability for every query through the engine.
Ring-buffer architecture prevents unbounded memory growth.
Append-only JSONL audit trail for compliance and debugging.

Architecture Position:
    QUERY INGRESS
        |
        v
    TELEMETRY START (trace_query)
        |
        v
    ENGINE PIPELINE (add_step at each stage)
        |
        v
    TELEMETRY COMPLETE (complete_trace)
        |
        v
    JSONL FLUSH (async, append-only)

Author: ECHO OMEGA PRIME
"""

from __future__ import annotations

import asyncio
import json
import time
import uuid
from collections import deque
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Deque, Dict, List, Optional, Tuple

from loguru import logger


# ============================================================================
# CONSTANTS
# ============================================================================

LOG_DIR: Path = Path("O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/LG02_case_law_research/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

TELEMETRY_LOG: Path = LOG_DIR / "telemetry.jsonl"
ERROR_LOG: Path = LOG_DIR / "errors.jsonl"
AUDIT_LOG: Path = LOG_DIR / "audit_trail.jsonl"
CITATION_LOG: Path = LOG_DIR / "citation_lookups.jsonl"
SHEPARDIZE_LOG: Path = LOG_DIR / "shepardize_ops.jsonl"

RING_BUFFER_SIZE: int = 10_000
FLUSH_BATCH_SIZE: int = 50
FLUSH_INTERVAL_SECONDS: float = 5.0


# ============================================================================
# ENUMS
# ============================================================================

class ResponseLayer(str, Enum):
    """Which engine layer produced the response."""
    DOCTRINE = "doctrine"
    SEARCH = "search"
    CITATION_ANALYSIS = "citation_analysis"
    SHEPARDIZE = "shepardize"
    PRECEDENT_CHAIN = "precedent_chain"
    DEEP_ANALYSIS = "deep_analysis"
    OPINION_PARSE = "opinion_parse"
    HEADNOTE = "headnote"
    FALLBACK = "fallback"
    ERROR = "error"


class ErrorDomain(str, Enum):
    """Classification of error source."""
    NORMALIZATION = "normalization"
    DOCTRINE_LOOKUP = "doctrine_lookup"
    SEARCH = "search"
    CITATION_PARSE = "citation_parse"
    SHEPARDIZE = "shepardize"
    PRECEDENT_CHAIN = "precedent_chain"
    OPINION_PARSE = "opinion_parse"
    HEADNOTE_EXTRACT = "headnote_extract"
    KEY_NUMBER = "key_number"
    ANALYSIS = "analysis"
    SERIALIZATION = "serialization"
    VALIDATION = "validation"
    TIMEOUT = "timeout"
    COURT_HIERARCHY = "court_hierarchy"
    JURISDICTION = "jurisdiction"
    UNKNOWN = "unknown"


class MutationType(str, Enum):
    """Type of doctrine mutation for drift tracking."""
    ADDITION = "addition"
    MODIFICATION = "modification"
    DEPRECATION = "deprecation"
    OVERRULE = "overrule"
    CIRCUIT_SPLIT = "circuit_split"
    LEGISLATIVE_CHANGE = "legislative_change"
    CERT_GRANTED = "cert_granted"


class MutationOrigin(str, Enum):
    """Where a mutation originated."""
    MANUAL = "manual"
    AUTOMATED = "automated"
    DRIFT_WATCHER = "drift_watcher"
    SHEPARDIZE_CHECK = "shepardize_check"
    SYSTEM = "system"


class CitationLookupType(str, Enum):
    """Type of citation lookup operation."""
    PARSE = "parse"
    VALIDATE = "validate"
    SHEPARDIZE = "shepardize"
    PRECEDENT_CHAIN = "precedent_chain"
    CROSS_REFERENCE = "cross_reference"


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class TelemetryStep:
    """Single step within a query trace."""
    step_name: str
    layer: ResponseLayer
    start_ms: float
    end_ms: float = 0.0
    duration_ms: float = 0.0
    success: bool = True
    detail: str = ""
    citations_found: int = 0
    doctrine_hit: bool = False
    court_level: str = ""
    jurisdiction: str = ""

    def complete(self, detail: str = "", success: bool = True) -> None:
        """Mark this step as complete."""
        self.end_ms = time.time() * 1000
        self.duration_ms = round(self.end_ms - self.start_ms, 3)
        self.detail = detail
        self.success = success

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "step_name": self.step_name,
            "layer": self.layer.value,
            "start_ms": self.start_ms,
            "end_ms": self.end_ms,
            "duration_ms": self.duration_ms,
            "success": self.success,
            "detail": self.detail,
            "citations_found": self.citations_found,
            "doctrine_hit": self.doctrine_hit,
            "court_level": self.court_level,
            "jurisdiction": self.jurisdiction,
        }


@dataclass
class QueryTrace:
    """Full trace of a single query through the engine."""
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    query: str = ""
    normalized_query: str = ""
    mode: str = "fast"
    jurisdiction: str = "federal"
    start_time: float = field(default_factory=lambda: time.time() * 1000)
    end_time: float = 0.0
    total_ms: float = 0.0
    steps: List[TelemetryStep] = field(default_factory=list)
    response_layer: ResponseLayer = ResponseLayer.FALLBACK
    doctrine_hit: bool = False
    citations_returned: int = 0
    confidence: float = 0.0
    determinism_hash: str = ""
    error: Optional[str] = None
    court_level: str = ""
    shepardize_performed: bool = False
    precedent_chain_depth: int = 0

    def add_step(
        self,
        step_name: str,
        layer: ResponseLayer,
    ) -> TelemetryStep:
        """Start a new telemetry step within this trace."""
        step = TelemetryStep(
            step_name=step_name,
            layer=layer,
            start_ms=time.time() * 1000,
        )
        self.steps.append(step)
        return step

    def complete(
        self,
        response_layer: ResponseLayer,
        doctrine_hit: bool = False,
        citations_returned: int = 0,
        confidence: float = 0.0,
        determinism_hash: str = "",
    ) -> None:
        """Mark this trace as complete."""
        self.end_time = time.time() * 1000
        self.total_ms = round(self.end_time - self.start_time, 3)
        self.response_layer = response_layer
        self.doctrine_hit = doctrine_hit
        self.citations_returned = citations_returned
        self.confidence = confidence
        self.determinism_hash = determinism_hash

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the entire trace."""
        return {
            "trace_id": self.trace_id,
            "query": self.query[:200],
            "normalized_query": self.normalized_query[:200],
            "mode": self.mode,
            "jurisdiction": self.jurisdiction,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "total_ms": self.total_ms,
            "steps": [s.to_dict() for s in self.steps],
            "response_layer": self.response_layer.value,
            "doctrine_hit": self.doctrine_hit,
            "citations_returned": self.citations_returned,
            "confidence": self.confidence,
            "determinism_hash": self.determinism_hash,
            "error": self.error,
            "court_level": self.court_level,
            "shepardize_performed": self.shepardize_performed,
            "precedent_chain_depth": self.precedent_chain_depth,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


@dataclass
class DoctrineMutation:
    """Record of a change to the doctrine cache."""
    mutation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    mutation_type: MutationType = MutationType.ADDITION
    origin: MutationOrigin = MutationOrigin.MANUAL
    doctrine_key: str = ""
    old_value_hash: str = ""
    new_value_hash: str = ""
    reason: str = ""
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    related_citation: str = ""
    court_level: str = ""
    approved_by: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "mutation_id": self.mutation_id,
            "mutation_type": self.mutation_type.value,
            "origin": self.origin.value,
            "doctrine_key": self.doctrine_key,
            "old_value_hash": self.old_value_hash,
            "new_value_hash": self.new_value_hash,
            "reason": self.reason,
            "timestamp": self.timestamp,
            "related_citation": self.related_citation,
            "court_level": self.court_level,
            "approved_by": self.approved_by,
        }


@dataclass
class CitationLookupRecord:
    """Record of a citation lookup operation."""
    lookup_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    lookup_type: CitationLookupType = CitationLookupType.PARSE
    citation_input: str = ""
    parsed_successfully: bool = False
    court_identified: str = ""
    reporter_identified: str = ""
    year_extracted: int = 0
    treatment_signal: str = ""
    chain_depth: int = 0
    latency_ms: float = 0.0
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "lookup_id": self.lookup_id,
            "lookup_type": self.lookup_type.value,
            "citation_input": self.citation_input[:300],
            "parsed_successfully": self.parsed_successfully,
            "court_identified": self.court_identified,
            "reporter_identified": self.reporter_identified,
            "year_extracted": self.year_extracted,
            "treatment_signal": self.treatment_signal,
            "chain_depth": self.chain_depth,
            "latency_ms": self.latency_ms,
            "timestamp": self.timestamp,
            "error": self.error,
        }


# ============================================================================
# TELEMETRY COLLECTOR — Ring Buffer + Async Flush
# ============================================================================

class TelemetryCollector:
    """
    High-performance telemetry collector with ring buffer architecture.

    Features:
        - Fixed-size ring buffer (default 10K entries)
        - Async flush to JSONL files
        - Citation-specific tracking
        - Shepardize operation logging
        - Error correlation across domains
        - Latency percentile calculation (p50, p95, p99)
    """

    def __init__(
        self,
        buffer_size: int = RING_BUFFER_SIZE,
        flush_batch: int = FLUSH_BATCH_SIZE,
        flush_interval: float = FLUSH_INTERVAL_SECONDS,
    ) -> None:
        self._buffer: Deque[Dict[str, Any]] = deque(maxlen=buffer_size)
        self._error_buffer: Deque[Dict[str, Any]] = deque(maxlen=buffer_size)
        self._mutation_buffer: Deque[Dict[str, Any]] = deque(maxlen=1000)
        self._citation_buffer: Deque[Dict[str, Any]] = deque(maxlen=5000)
        self._flush_batch = flush_batch
        self._flush_interval = flush_interval
        self._flush_task: Optional[asyncio.Task] = None
        self._total_traces: int = 0
        self._total_errors: int = 0
        self._total_mutations: int = 0
        self._total_citations: int = 0
        self._total_shepardize: int = 0
        self._latencies: Deque[float] = deque(maxlen=1000)
        self._layer_counts: Dict[str, int] = {}
        self._error_domain_counts: Dict[str, int] = {}
        self._court_level_counts: Dict[str, int] = {}
        self._jurisdiction_counts: Dict[str, int] = {}
        self._citation_type_counts: Dict[str, int] = {}
        self._treatment_counts: Dict[str, int] = {}
        self._start_time: float = time.time()

    def start_background_flush(self) -> None:
        """Start the background flush task."""
        if self._flush_task is None or self._flush_task.done():
            self._flush_task = asyncio.create_task(self._flush_loop())
            logger.info("Telemetry background flush started")

    async def _flush_loop(self) -> None:
        """Continuously flush buffer to disk."""
        while True:
            try:
                await asyncio.sleep(self._flush_interval)
                await self._flush_to_disk()
            except asyncio.CancelledError:
                await self._flush_to_disk()
                break
            except Exception as exc:
                logger.error(f"Telemetry flush error: {exc}")

    async def _flush_to_disk(self) -> None:
        """Write buffered entries to JSONL files."""
        entries_flushed = 0

        # Flush trace buffer
        batch: List[str] = []
        while self._buffer and len(batch) < self._flush_batch:
            entry = self._buffer.popleft()
            batch.append(json.dumps(entry, default=str))

        if batch:
            try:
                with open(TELEMETRY_LOG, "a", encoding="utf-8") as fh:
                    fh.write("\n".join(batch) + "\n")
                entries_flushed += len(batch)
            except OSError as exc:
                logger.error(f"Failed to write telemetry log: {exc}")

        # Flush error buffer
        error_batch: List[str] = []
        while self._error_buffer and len(error_batch) < self._flush_batch:
            entry = self._error_buffer.popleft()
            error_batch.append(json.dumps(entry, default=str))

        if error_batch:
            try:
                with open(ERROR_LOG, "a", encoding="utf-8") as fh:
                    fh.write("\n".join(error_batch) + "\n")
                entries_flushed += len(error_batch)
            except OSError as exc:
                logger.error(f"Failed to write error log: {exc}")

        # Flush citation buffer
        citation_batch: List[str] = []
        while self._citation_buffer and len(citation_batch) < self._flush_batch:
            entry = self._citation_buffer.popleft()
            citation_batch.append(json.dumps(entry, default=str))

        if citation_batch:
            try:
                with open(CITATION_LOG, "a", encoding="utf-8") as fh:
                    fh.write("\n".join(citation_batch) + "\n")
                entries_flushed += len(citation_batch)
            except OSError as exc:
                logger.error(f"Failed to write citation log: {exc}")

        if entries_flushed > 0:
            logger.debug(f"Flushed {entries_flushed} telemetry entries to disk")

    def record_trace(self, trace: QueryTrace) -> None:
        """Record a completed query trace."""
        self._total_traces += 1
        self._latencies.append(trace.total_ms)
        layer_key = trace.response_layer.value
        self._layer_counts[layer_key] = self._layer_counts.get(layer_key, 0) + 1

        if trace.court_level:
            self._court_level_counts[trace.court_level] = (
                self._court_level_counts.get(trace.court_level, 0) + 1
            )

        if trace.jurisdiction:
            self._jurisdiction_counts[trace.jurisdiction] = (
                self._jurisdiction_counts.get(trace.jurisdiction, 0) + 1
            )

        if trace.shepardize_performed:
            self._total_shepardize += 1

        self._buffer.append(trace.to_dict())

    def record_error(
        self,
        domain: ErrorDomain,
        error_msg: str,
        trace_id: str = "",
        query: str = "",
        citation: str = "",
    ) -> None:
        """Record an error event."""
        self._total_errors += 1
        domain_key = domain.value
        self._error_domain_counts[domain_key] = (
            self._error_domain_counts.get(domain_key, 0) + 1
        )

        entry = {
            "error_id": str(uuid.uuid4()),
            "domain": domain_key,
            "message": error_msg[:500],
            "trace_id": trace_id,
            "query": query[:200],
            "citation": citation[:300],
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self._error_buffer.append(entry)

    def record_mutation(self, mutation: DoctrineMutation) -> None:
        """Record a doctrine mutation event."""
        self._total_mutations += 1
        self._mutation_buffer.append(mutation.to_dict())

    def record_citation_lookup(self, record: CitationLookupRecord) -> None:
        """Record a citation lookup event."""
        self._total_citations += 1
        lookup_key = record.lookup_type.value
        self._citation_type_counts[lookup_key] = (
            self._citation_type_counts.get(lookup_key, 0) + 1
        )

        if record.treatment_signal:
            self._treatment_counts[record.treatment_signal] = (
                self._treatment_counts.get(record.treatment_signal, 0) + 1
            )

        self._citation_buffer.append(record.to_dict())

    def get_latency_percentiles(self) -> Dict[str, float]:
        """Calculate latency percentiles from recent data."""
        if not self._latencies:
            return {"p50": 0.0, "p75": 0.0, "p90": 0.0, "p95": 0.0, "p99": 0.0, "avg": 0.0}

        sorted_lat = sorted(self._latencies)
        n = len(sorted_lat)

        def percentile(p: float) -> float:
            idx = int(n * p)
            return round(sorted_lat[min(idx, n - 1)], 2)

        return {
            "p50": percentile(0.50),
            "p75": percentile(0.75),
            "p90": percentile(0.90),
            "p95": percentile(0.95),
            "p99": percentile(0.99),
            "avg": round(sum(sorted_lat) / n, 2),
        }

    def get_stats(self) -> Dict[str, Any]:
        """Get comprehensive telemetry statistics."""
        uptime_seconds = time.time() - self._start_time
        return {
            "total_traces": self._total_traces,
            "total_errors": self._total_errors,
            "total_mutations": self._total_mutations,
            "total_citation_lookups": self._total_citations,
            "total_shepardize_ops": self._total_shepardize,
            "error_rate": round(
                self._total_errors / max(self._total_traces, 1), 4
            ),
            "latency_percentiles": self.get_latency_percentiles(),
            "layer_distribution": dict(self._layer_counts),
            "error_domain_distribution": dict(self._error_domain_counts),
            "court_level_distribution": dict(self._court_level_counts),
            "jurisdiction_distribution": dict(self._jurisdiction_counts),
            "citation_type_distribution": dict(self._citation_type_counts),
            "treatment_distribution": dict(self._treatment_counts),
            "buffer_usage": {
                "trace_buffer": len(self._buffer),
                "error_buffer": len(self._error_buffer),
                "citation_buffer": len(self._citation_buffer),
                "mutation_buffer": len(self._mutation_buffer),
            },
            "uptime_seconds": round(uptime_seconds, 1),
            "traces_per_minute": round(
                self._total_traces / max(uptime_seconds / 60, 0.01), 2
            ),
        }

    def get_recent_traces(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get the most recent traces."""
        traces = list(self._buffer)
        return traces[-limit:]

    def get_recent_errors(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get the most recent errors."""
        errors = list(self._error_buffer)
        return errors[-limit:]

    def get_recent_citations(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get the most recent citation lookups."""
        citations = list(self._citation_buffer)
        return citations[-limit:]

    def get_recent_mutations(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get the most recent doctrine mutations."""
        mutations = list(self._mutation_buffer)
        return mutations[-limit:]


# ============================================================================
# SINGLETON INSTANCE
# ============================================================================

_telemetry_instance: Optional[TelemetryCollector] = None


def get_telemetry() -> TelemetryCollector:
    """Get the global telemetry collector instance."""
    global _telemetry_instance
    if _telemetry_instance is None:
        _telemetry_instance = TelemetryCollector()
    return _telemetry_instance


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def trace_query(
    query: str,
    normalized_query: str = "",
    mode: str = "fast",
    jurisdiction: str = "federal",
) -> QueryTrace:
    """Create and register a new query trace."""
    trace = QueryTrace(
        query=query,
        normalized_query=normalized_query or query,
        mode=mode,
        jurisdiction=jurisdiction,
    )
    logger.debug(f"Trace started: {trace.trace_id} | query={query[:80]}")
    return trace


def complete_trace(
    trace: QueryTrace,
    response_layer: ResponseLayer,
    doctrine_hit: bool = False,
    citations_returned: int = 0,
    confidence: float = 0.0,
    determinism_hash: str = "",
) -> None:
    """Complete a trace and record it to the collector."""
    trace.complete(
        response_layer=response_layer,
        doctrine_hit=doctrine_hit,
        citations_returned=citations_returned,
        confidence=confidence,
        determinism_hash=determinism_hash,
    )
    get_telemetry().record_trace(trace)
    logger.debug(
        f"Trace complete: {trace.trace_id} | "
        f"layer={response_layer.value} | "
        f"ms={trace.total_ms} | "
        f"citations={citations_returned}"
    )


def log_error(
    domain: ErrorDomain,
    error_msg: str,
    trace_id: str = "",
    query: str = "",
    citation: str = "",
) -> None:
    """Log an error to the telemetry system."""
    get_telemetry().record_error(
        domain=domain,
        error_msg=error_msg,
        trace_id=trace_id,
        query=query,
        citation=citation,
    )
    logger.error(f"[{domain.value}] {error_msg[:200]}")


def record_doctrine_mutation(
    mutation_type: MutationType,
    origin: MutationOrigin,
    doctrine_key: str,
    reason: str,
    old_hash: str = "",
    new_hash: str = "",
    related_citation: str = "",
    court_level: str = "",
) -> None:
    """Record a doctrine mutation."""
    mutation = DoctrineMutation(
        mutation_type=mutation_type,
        origin=origin,
        doctrine_key=doctrine_key,
        old_value_hash=old_hash,
        new_value_hash=new_hash,
        reason=reason,
        related_citation=related_citation,
        court_level=court_level,
    )
    get_telemetry().record_mutation(mutation)
    logger.info(
        f"Doctrine mutation: {mutation_type.value} on {doctrine_key} "
        f"({origin.value}): {reason[:100]}"
    )


def record_citation_lookup(
    lookup_type: CitationLookupType,
    citation_input: str,
    parsed_ok: bool = False,
    court: str = "",
    reporter: str = "",
    year: int = 0,
    treatment: str = "",
    chain_depth: int = 0,
    latency_ms: float = 0.0,
    error: Optional[str] = None,
) -> None:
    """Record a citation lookup operation."""
    record = CitationLookupRecord(
        lookup_type=lookup_type,
        citation_input=citation_input,
        parsed_successfully=parsed_ok,
        court_identified=court,
        reporter_identified=reporter,
        year_extracted=year,
        treatment_signal=treatment,
        chain_depth=chain_depth,
        latency_ms=latency_ms,
        error=error,
    )
    get_telemetry().record_citation_lookup(record)
