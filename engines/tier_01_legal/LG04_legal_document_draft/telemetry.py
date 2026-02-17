"""
LG04 Legal Document Draft Engine - Telemetry Module
=====================================================
Production telemetry, metrics collection, audit trailing, and
performance monitoring for the legal document drafting engine.

Provides:
    - Ring buffer for high-frequency event capture
    - JSONL audit trail with SHA-256 hash chain
    - Query tracing with step-level timing
    - Doctrine mutation tracking
    - Document generation metrics
    - Error domain classification
    - Periodic flush to disk

Engine ID: LG04
Version: 1.0.0
"""

from __future__ import annotations

import hashlib
import json
import threading
import time
import uuid
from collections import defaultdict, deque
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from loguru import logger
from pydantic import BaseModel, Field


# ============================================================================
# ENUMS
# ============================================================================


class ErrorDomain(str, Enum):
    """Classification of error sources within the engine."""

    DOCTRINE_CACHE = "doctrine_cache"
    SEMANTIC_NORMALIZATION = "semantic_normalization"
    VECTOR_SEARCH = "vector_search"
    DOCUMENT_ASSEMBLY = "document_assembly"
    CLAUSE_LIBRARY = "clause_library"
    TEMPLATE_ENGINE = "template_engine"
    COMPLIANCE_CHECK = "compliance_check"
    AUTHORITY_GATE = "authority_gate"
    INPUT_VALIDATION = "input_validation"
    SERIALIZATION = "serialization"
    CONFIGURATION = "configuration"
    JURISDICTION = "jurisdiction"
    VERSION_CONTROL = "version_control"
    AUDIT_TRAIL = "audit_trail"
    TELEMETRY = "telemetry"
    UNKNOWN = "unknown"


class ResponseLayer(str, Enum):
    """Which response layer produced the result."""

    SUMMARY = "summary"
    ANALYSIS = "analysis"
    DEEP_DIVE = "deep_dive"
    CACHE_HIT = "cache_hit"
    SEARCH_HIT = "search_hit"
    ASSEMBLY = "assembly"
    GENERATION = "generation"


class MutationType(str, Enum):
    """Type of doctrine mutation event."""

    ADDED = "added"
    UPDATED = "updated"
    DEPRECATED = "deprecated"
    REMOVED = "removed"
    DRIFT_DETECTED = "drift_detected"
    CONFIDENCE_ADJUSTED = "confidence_adjusted"
    CLAUSE_MODIFIED = "clause_modified"
    TEMPLATE_UPDATED = "template_updated"


class MutationOrigin(str, Enum):
    """Who or what triggered the mutation."""

    SYSTEM = "system"
    ADMIN = "admin"
    DRIFT_WATCHER = "drift_watcher"
    USER_FEEDBACK = "user_feedback"
    COMPLIANCE_UPDATE = "compliance_update"
    JURISDICTION_CHANGE = "jurisdiction_change"
    LEGISLATIVE_UPDATE = "legislative_update"
    AUTOMATED_REVIEW = "automated_review"


class DocumentMetricType(str, Enum):
    """Types of document-specific metrics."""

    GENERATION_TIME = "generation_time_ms"
    CLAUSE_COUNT = "clause_count"
    WORD_COUNT = "word_count"
    COMPLIANCE_SCORE = "compliance_score"
    TEMPLATE_MATCH = "template_match_score"
    JURISDICTION_COVERAGE = "jurisdiction_coverage"
    VERSION_COUNT = "version_count"
    ASSEMBLY_COMPLEXITY = "assembly_complexity"


# ============================================================================
# PYDANTIC MODELS
# ============================================================================


class TelemetryStep(BaseModel):
    """A single step within a query trace."""

    step_name: str
    start_time: float
    end_time: float = 0.0
    duration_ms: float = 0.0
    metadata: Dict[str, Any] = Field(default_factory=dict)
    error: Optional[str] = None
    layer: Optional[ResponseLayer] = None

    def complete(self, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Mark step as complete with timing."""
        self.end_time = time.time()
        self.duration_ms = (self.end_time - self.start_time) * 1000.0
        if metadata:
            self.metadata.update(metadata)


class QueryTrace(BaseModel):
    """Full trace of a single query through the engine."""

    trace_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    query_text: str = ""
    query_hash: str = ""
    document_type: str = ""
    jurisdiction: str = ""
    response_mode: str = "EF"
    authority_level: float = 0.0
    start_time: float = Field(default_factory=time.time)
    end_time: float = 0.0
    total_duration_ms: float = 0.0
    steps: List[TelemetryStep] = Field(default_factory=list)
    result_layer: Optional[ResponseLayer] = None
    confidence: float = 0.0
    doctrine_hits: int = 0
    clause_count: int = 0
    error: Optional[str] = None
    determinism_hash: str = ""

    def add_step(self, step_name: str, layer: Optional[ResponseLayer] = None) -> TelemetryStep:
        """Start a new trace step."""
        step = TelemetryStep(step_name=step_name, start_time=time.time(), layer=layer)
        self.steps.append(step)
        return step

    def complete(self, result_layer: Optional[ResponseLayer] = None, confidence: float = 0.0) -> None:
        """Finalize the trace."""
        self.end_time = time.time()
        self.total_duration_ms = (self.end_time - self.start_time) * 1000.0
        if result_layer:
            self.result_layer = result_layer
        self.confidence = confidence


class AuditEntry(BaseModel):
    """Single audit trail entry for JSONL logging."""

    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    event_type: str
    trace_id: str = ""
    engine_id: str = "LG04"
    query_hash: str = ""
    document_type: str = ""
    jurisdiction: str = ""
    response_mode: str = ""
    authority_level: float = 0.0
    confidence: float = 0.0
    duration_ms: float = 0.0
    clause_count: int = 0
    error: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    entry_hash: str = ""
    previous_hash: str = ""


class DoctrineMutationRecord(BaseModel):
    """Record of a doctrine mutation event."""

    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    mutation_type: MutationType
    origin: MutationOrigin
    doctrine_id: str
    topic: str = ""
    old_value_hash: str = ""
    new_value_hash: str = ""
    reason: str = ""
    metadata: Dict[str, Any] = Field(default_factory=dict)


class DocumentGenerationRecord(BaseModel):
    """Record of a document generation event."""

    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    trace_id: str
    document_type: str
    jurisdiction: str = ""
    clause_count: int = 0
    word_count: int = 0
    generation_time_ms: float = 0.0
    compliance_score: float = 0.0
    template_used: str = ""
    version: int = 1
    determinism_hash: str = ""


class EngineMetrics(BaseModel):
    """Aggregated engine-level metrics snapshot."""

    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    engine_id: str = "LG04"
    total_queries: int = 0
    total_documents: int = 0
    total_clauses_generated: int = 0
    total_errors: int = 0
    avg_latency_ms: float = 0.0
    p95_latency_ms: float = 0.0
    p99_latency_ms: float = 0.0
    cache_hit_rate: float = 0.0
    avg_confidence: float = 0.0
    avg_compliance_score: float = 0.0
    documents_by_type: Dict[str, int] = Field(default_factory=dict)
    errors_by_domain: Dict[str, int] = Field(default_factory=dict)
    uptime_seconds: float = 0.0


# ============================================================================
# TELEMETRY COLLECTOR - CORE
# ============================================================================


class TelemetryCollector:
    """
    High-performance telemetry collector with ring buffer, audit trail,
    and metrics aggregation for the LG04 Legal Document Draft engine.
    """

    def __init__(
        self,
        engine_id: str = "LG04",
        ring_buffer_size: int = 10000,
        flush_batch_size: int = 50,
        flush_interval: float = 5.0,
        log_dir: Optional[Path] = None,
    ) -> None:
        self.engine_id = engine_id
        self.ring_buffer_size = ring_buffer_size
        self.flush_batch_size = flush_batch_size
        self.flush_interval = flush_interval
        self.log_dir = log_dir or Path("O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/LG04_legal_document_draft/logs")
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self._traces: deque[QueryTrace] = deque(maxlen=ring_buffer_size)
        self._audit_buffer: deque[AuditEntry] = deque(maxlen=ring_buffer_size)
        self._mutation_log: deque[DoctrineMutationRecord] = deque(maxlen=5000)
        self._document_log: deque[DocumentGenerationRecord] = deque(maxlen=5000)
        self._error_counts: Dict[str, int] = defaultdict(int)
        self._latencies: deque[float] = deque(maxlen=10000)
        self._confidence_scores: deque[float] = deque(maxlen=10000)
        self._compliance_scores: deque[float] = deque(maxlen=10000)
        self._documents_by_type: Dict[str, int] = defaultdict(int)
        self._clauses_generated: int = 0
        self._total_queries: int = 0
        self._total_documents: int = 0
        self._total_errors: int = 0
        self._cache_hits: int = 0
        self._cache_misses: int = 0
        self._start_time: float = time.time()
        self._last_audit_hash: str = "GENESIS"

        self._lock = threading.Lock()
        self._audit_file = self.log_dir / "audit_trail.jsonl"
        self._metrics_file = self.log_dir / "metrics.jsonl"
        self._mutation_file = self.log_dir / "doctrine_mutations.jsonl"
        self._document_file = self.log_dir / "document_generations.jsonl"

        self._flush_thread: Optional[threading.Thread] = None
        self._running = False

        logger.info(
            "TelemetryCollector initialized | engine={} buffer_size={} flush_interval={}s",
            engine_id,
            ring_buffer_size,
            flush_interval,
        )

    def start(self) -> None:
        """Start the background flush thread."""
        if self._running:
            return
        self._running = True
        self._flush_thread = threading.Thread(target=self._flush_loop, daemon=True, name="lg04-telemetry-flush")
        self._flush_thread.start()
        logger.info("Telemetry flush thread started")

    def stop(self) -> None:
        """Stop the background flush thread and flush remaining data."""
        self._running = False
        if self._flush_thread and self._flush_thread.is_alive():
            self._flush_thread.join(timeout=10.0)
        self._flush_all()
        logger.info("Telemetry collector stopped, final flush complete")

    def _flush_loop(self) -> None:
        """Background loop that periodically flushes telemetry data to disk."""
        while self._running:
            time.sleep(self.flush_interval)
            try:
                self._flush_all()
            except Exception as exc:
                logger.error("Telemetry flush error: {}", str(exc))

    def _flush_all(self) -> None:
        """Flush all buffered data to disk."""
        with self._lock:
            self._flush_audit_buffer()
            self._flush_metrics_snapshot()

    def _flush_audit_buffer(self) -> None:
        """Write buffered audit entries to JSONL file."""
        if not self._audit_buffer:
            return
        entries_to_write: List[AuditEntry] = []
        batch_count = 0
        while self._audit_buffer and batch_count < self.flush_batch_size:
            entries_to_write.append(self._audit_buffer.popleft())
            batch_count += 1

        try:
            with open(self._audit_file, "a", encoding="utf-8") as fh:
                for entry in entries_to_write:
                    fh.write(entry.model_dump_json() + "\n")
        except OSError as exc:
            logger.error("Failed to write audit trail: {}", str(exc))

    def _flush_metrics_snapshot(self) -> None:
        """Write a metrics snapshot to the metrics JSONL file."""
        metrics = self.get_metrics_snapshot()
        try:
            with open(self._metrics_file, "a", encoding="utf-8") as fh:
                fh.write(metrics.model_dump_json() + "\n")
        except OSError as exc:
            logger.error("Failed to write metrics snapshot: {}", str(exc))

    # ========================================================================
    # TRACE MANAGEMENT
    # ========================================================================

    def start_trace(
        self,
        query_text: str,
        document_type: str = "",
        jurisdiction: str = "",
        response_mode: str = "EF",
        authority_level: float = 0.0,
    ) -> QueryTrace:
        """Begin a new query trace."""
        query_hash = hashlib.sha256(query_text.encode("utf-8")).hexdigest()[:16]
        trace = QueryTrace(
            query_text=query_text,
            query_hash=query_hash,
            document_type=document_type,
            jurisdiction=jurisdiction,
            response_mode=response_mode,
            authority_level=authority_level,
        )
        with self._lock:
            self._traces.append(trace)
            self._total_queries += 1
        logger.debug("Trace started | id={} type={} jurisdiction={}", trace.trace_id[:8], document_type, jurisdiction)
        return trace

    def complete_trace(
        self,
        trace: QueryTrace,
        result_layer: Optional[ResponseLayer] = None,
        confidence: float = 0.0,
        clause_count: int = 0,
        determinism_hash: str = "",
        was_cache_hit: bool = False,
    ) -> None:
        """Finalize a query trace and record metrics."""
        trace.complete(result_layer=result_layer, confidence=confidence)
        trace.clause_count = clause_count
        trace.determinism_hash = determinism_hash

        with self._lock:
            self._latencies.append(trace.total_duration_ms)
            self._confidence_scores.append(confidence)
            if was_cache_hit:
                self._cache_hits += 1
            else:
                self._cache_misses += 1

        audit_entry = self._create_audit_entry(
            event_type="query_complete",
            trace=trace,
        )
        self._enqueue_audit(audit_entry)

        logger.info(
            "Trace complete | id={} duration={:.1f}ms confidence={:.2f} clauses={} layer={}",
            trace.trace_id[:8],
            trace.total_duration_ms,
            confidence,
            clause_count,
            result_layer.value if result_layer else "none",
        )

    # ========================================================================
    # ERROR TRACKING
    # ========================================================================

    def log_error(
        self,
        error_domain: ErrorDomain,
        error_message: str,
        trace_id: str = "",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Record an error event."""
        with self._lock:
            self._error_counts[error_domain.value] += 1
            self._total_errors += 1

        audit_entry = AuditEntry(
            event_type="error",
            trace_id=trace_id,
            engine_id=self.engine_id,
            error=f"[{error_domain.value}] {error_message}",
            metadata=metadata or {},
        )
        self._enqueue_audit(audit_entry)
        logger.error("Engine error | domain={} msg={} trace={}", error_domain.value, error_message, trace_id[:8])

    # ========================================================================
    # DOCTRINE MUTATION TRACKING
    # ========================================================================

    def record_doctrine_mutation(
        self,
        mutation_type: MutationType,
        origin: MutationOrigin,
        doctrine_id: str,
        topic: str = "",
        old_value: str = "",
        new_value: str = "",
        reason: str = "",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> DoctrineMutationRecord:
        """Record a doctrine cache mutation."""
        old_hash = hashlib.sha256(old_value.encode("utf-8")).hexdigest()[:16] if old_value else ""
        new_hash = hashlib.sha256(new_value.encode("utf-8")).hexdigest()[:16] if new_value else ""

        record = DoctrineMutationRecord(
            mutation_type=mutation_type,
            origin=origin,
            doctrine_id=doctrine_id,
            topic=topic,
            old_value_hash=old_hash,
            new_value_hash=new_hash,
            reason=reason,
            metadata=metadata or {},
        )

        with self._lock:
            self._mutation_log.append(record)

        try:
            with open(self._mutation_file, "a", encoding="utf-8") as fh:
                fh.write(record.model_dump_json() + "\n")
        except OSError:
            pass

        logger.info(
            "Doctrine mutation | type={} origin={} id={} topic={}",
            mutation_type.value,
            origin.value,
            doctrine_id,
            topic,
        )
        return record

    # ========================================================================
    # DOCUMENT GENERATION TRACKING
    # ========================================================================

    def record_document_generation(
        self,
        trace_id: str,
        document_type: str,
        jurisdiction: str = "",
        clause_count: int = 0,
        word_count: int = 0,
        generation_time_ms: float = 0.0,
        compliance_score: float = 0.0,
        template_used: str = "",
        version: int = 1,
        determinism_hash: str = "",
    ) -> DocumentGenerationRecord:
        """Record a document generation event."""
        record = DocumentGenerationRecord(
            trace_id=trace_id,
            document_type=document_type,
            jurisdiction=jurisdiction,
            clause_count=clause_count,
            word_count=word_count,
            generation_time_ms=generation_time_ms,
            compliance_score=compliance_score,
            template_used=template_used,
            version=version,
            determinism_hash=determinism_hash,
        )

        with self._lock:
            self._document_log.append(record)
            self._total_documents += 1
            self._documents_by_type[document_type] += 1
            self._clauses_generated += clause_count
            if compliance_score > 0:
                self._compliance_scores.append(compliance_score)

        try:
            with open(self._document_file, "a", encoding="utf-8") as fh:
                fh.write(record.model_dump_json() + "\n")
        except OSError:
            pass

        logger.info(
            "Document generated | type={} jurisdiction={} clauses={} words={} compliance={:.2f}",
            document_type,
            jurisdiction,
            clause_count,
            word_count,
            compliance_score,
        )
        return record

    # ========================================================================
    # AUDIT TRAIL
    # ========================================================================

    def _create_audit_entry(
        self,
        event_type: str,
        trace: Optional[QueryTrace] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> AuditEntry:
        """Create an audit entry with hash chain integrity."""
        entry = AuditEntry(
            event_type=event_type,
            trace_id=trace.trace_id if trace else "",
            engine_id=self.engine_id,
            query_hash=trace.query_hash if trace else "",
            document_type=trace.document_type if trace else "",
            jurisdiction=trace.jurisdiction if trace else "",
            response_mode=trace.response_mode if trace else "",
            authority_level=trace.authority_level if trace else 0.0,
            confidence=trace.confidence if trace else 0.0,
            duration_ms=trace.total_duration_ms if trace else 0.0,
            clause_count=trace.clause_count if trace else 0,
            error=trace.error if trace else None,
            metadata=metadata or {},
            previous_hash=self._last_audit_hash,
        )

        entry_content = f"{entry.timestamp}|{entry.event_type}|{entry.trace_id}|{entry.previous_hash}"
        entry.entry_hash = hashlib.sha256(entry_content.encode("utf-8")).hexdigest()
        self._last_audit_hash = entry.entry_hash

        return entry

    def _enqueue_audit(self, entry: AuditEntry) -> None:
        """Add an audit entry to the buffer."""
        with self._lock:
            self._audit_buffer.append(entry)

    def record_audit_event(
        self,
        event_type: str,
        trace_id: str = "",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> AuditEntry:
        """Record a standalone audit event (not tied to a trace)."""
        entry = AuditEntry(
            event_type=event_type,
            trace_id=trace_id,
            engine_id=self.engine_id,
            metadata=metadata or {},
            previous_hash=self._last_audit_hash,
        )
        entry_content = f"{entry.timestamp}|{entry.event_type}|{entry.trace_id}|{entry.previous_hash}"
        entry.entry_hash = hashlib.sha256(entry_content.encode("utf-8")).hexdigest()
        self._last_audit_hash = entry.entry_hash
        self._enqueue_audit(entry)
        return entry

    # ========================================================================
    # METRICS AGGREGATION
    # ========================================================================

    def get_metrics_snapshot(self) -> EngineMetrics:
        """Generate a point-in-time metrics snapshot."""
        with self._lock:
            latencies_list = list(self._latencies)
            confidence_list = list(self._confidence_scores)
            compliance_list = list(self._compliance_scores)

        avg_latency = sum(latencies_list) / len(latencies_list) if latencies_list else 0.0
        p95_latency = self._percentile(latencies_list, 0.95) if latencies_list else 0.0
        p99_latency = self._percentile(latencies_list, 0.99) if latencies_list else 0.0
        avg_confidence = sum(confidence_list) / len(confidence_list) if confidence_list else 0.0
        avg_compliance = sum(compliance_list) / len(compliance_list) if compliance_list else 0.0

        total_cache_ops = self._cache_hits + self._cache_misses
        cache_hit_rate = self._cache_hits / total_cache_ops if total_cache_ops > 0 else 0.0

        return EngineMetrics(
            engine_id=self.engine_id,
            total_queries=self._total_queries,
            total_documents=self._total_documents,
            total_clauses_generated=self._clauses_generated,
            total_errors=self._total_errors,
            avg_latency_ms=round(avg_latency, 2),
            p95_latency_ms=round(p95_latency, 2),
            p99_latency_ms=round(p99_latency, 2),
            cache_hit_rate=round(cache_hit_rate, 4),
            avg_confidence=round(avg_confidence, 4),
            avg_compliance_score=round(avg_compliance, 4),
            documents_by_type=dict(self._documents_by_type),
            errors_by_domain=dict(self._error_counts),
            uptime_seconds=round(time.time() - self._start_time, 2),
        )

    def get_recent_traces(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Return the most recent query traces."""
        with self._lock:
            traces = list(self._traces)
        recent = traces[-limit:] if len(traces) > limit else traces
        return [t.model_dump() for t in reversed(recent)]

    def get_recent_mutations(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Return the most recent doctrine mutations."""
        with self._lock:
            mutations = list(self._mutation_log)
        recent = mutations[-limit:] if len(mutations) > limit else mutations
        return [m.model_dump() for m in reversed(recent)]

    def get_recent_documents(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Return the most recent document generation records."""
        with self._lock:
            docs = list(self._document_log)
        recent = docs[-limit:] if len(docs) > limit else docs
        return [d.model_dump() for d in reversed(recent)]

    def get_error_summary(self) -> Dict[str, Any]:
        """Return error counts by domain."""
        with self._lock:
            return {
                "total_errors": self._total_errors,
                "by_domain": dict(self._error_counts),
            }

    # ========================================================================
    # UTILITY
    # ========================================================================

    @staticmethod
    def _percentile(data: List[float], pct: float) -> float:
        """Calculate percentile value from a list."""
        if not data:
            return 0.0
        sorted_data = sorted(data)
        idx = int(len(sorted_data) * pct)
        idx = min(idx, len(sorted_data) - 1)
        return sorted_data[idx]

    def verify_audit_chain(self) -> Tuple[bool, int, int]:
        """Verify the integrity of the audit trail hash chain on disk."""
        if not self._audit_file.exists():
            return True, 0, 0

        valid_count = 0
        invalid_count = 0
        previous_hash = "GENESIS"

        try:
            with open(self._audit_file, "r", encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        entry_data = json.loads(line)
                        stored_prev = entry_data.get("previous_hash", "")
                        if stored_prev == previous_hash:
                            valid_count += 1
                        else:
                            invalid_count += 1
                        previous_hash = entry_data.get("entry_hash", previous_hash)
                    except json.JSONDecodeError:
                        invalid_count += 1
        except OSError:
            return False, 0, 0

        is_valid = invalid_count == 0
        return is_valid, valid_count, invalid_count


# ============================================================================
# MODULE-LEVEL SINGLETON
# ============================================================================

_telemetry_instance: Optional[TelemetryCollector] = None
_telemetry_lock = threading.Lock()


def get_telemetry(
    engine_id: str = "LG04",
    ring_buffer_size: int = 10000,
    flush_batch_size: int = 50,
    flush_interval: float = 5.0,
    log_dir: Optional[Path] = None,
) -> TelemetryCollector:
    """Get or create the singleton TelemetryCollector instance."""
    global _telemetry_instance
    with _telemetry_lock:
        if _telemetry_instance is None:
            _telemetry_instance = TelemetryCollector(
                engine_id=engine_id,
                ring_buffer_size=ring_buffer_size,
                flush_batch_size=flush_batch_size,
                flush_interval=flush_interval,
                log_dir=log_dir,
            )
            _telemetry_instance.start()
        return _telemetry_instance


def trace_query(
    query_text: str,
    document_type: str = "",
    jurisdiction: str = "",
    response_mode: str = "EF",
    authority_level: float = 0.0,
) -> QueryTrace:
    """Convenience function to start a query trace."""
    collector = get_telemetry()
    return collector.start_trace(
        query_text=query_text,
        document_type=document_type,
        jurisdiction=jurisdiction,
        response_mode=response_mode,
        authority_level=authority_level,
    )


def complete_trace(
    trace: QueryTrace,
    result_layer: Optional[ResponseLayer] = None,
    confidence: float = 0.0,
    clause_count: int = 0,
    determinism_hash: str = "",
    was_cache_hit: bool = False,
) -> None:
    """Convenience function to complete a query trace."""
    collector = get_telemetry()
    collector.complete_trace(
        trace=trace,
        result_layer=result_layer,
        confidence=confidence,
        clause_count=clause_count,
        determinism_hash=determinism_hash,
        was_cache_hit=was_cache_hit,
    )


def log_error(
    error_domain: ErrorDomain,
    error_message: str,
    trace_id: str = "",
    metadata: Optional[Dict[str, Any]] = None,
) -> None:
    """Convenience function to log an error."""
    collector = get_telemetry()
    collector.log_error(
        error_domain=error_domain,
        error_message=error_message,
        trace_id=trace_id,
        metadata=metadata,
    )


def record_doctrine_mutation(
    mutation_type: MutationType,
    origin: MutationOrigin,
    doctrine_id: str,
    topic: str = "",
    old_value: str = "",
    new_value: str = "",
    reason: str = "",
    metadata: Optional[Dict[str, Any]] = None,
) -> DoctrineMutationRecord:
    """Convenience function to record a doctrine mutation."""
    collector = get_telemetry()
    return collector.record_doctrine_mutation(
        mutation_type=mutation_type,
        origin=origin,
        doctrine_id=doctrine_id,
        topic=topic,
        old_value=old_value,
        new_value=new_value,
        reason=reason,
        metadata=metadata,
    )


def record_document_generation(
    trace_id: str,
    document_type: str,
    jurisdiction: str = "",
    clause_count: int = 0,
    word_count: int = 0,
    generation_time_ms: float = 0.0,
    compliance_score: float = 0.0,
    template_used: str = "",
    version: int = 1,
    determinism_hash: str = "",
) -> DocumentGenerationRecord:
    """Convenience function to record a document generation."""
    collector = get_telemetry()
    return collector.record_document_generation(
        trace_id=trace_id,
        document_type=document_type,
        jurisdiction=jurisdiction,
        clause_count=clause_count,
        word_count=word_count,
        generation_time_ms=generation_time_ms,
        compliance_score=compliance_score,
        template_used=template_used,
        version=version,
        determinism_hash=determinism_hash,
    )
