"""
Contract Analysis Engine - Telemetry & Observability
Ring-buffer telemetry with async-safe collection, JSONL flush, and percentile stats.

Author: ECHO OMEGA PRIME
Authority: 11.0 SOVEREIGN
Version: 1.0.0
"""

from __future__ import annotations
import asyncio
import json
import statistics
import time
import traceback
import uuid
from collections import deque
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Deque, Tuple
from loguru import logger

# Log directory
LOG_DIR = Path("O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/lg01/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

TELEMETRY_LOG = LOG_DIR / "telemetry.jsonl"
ERROR_LOG = LOG_DIR / "errors.jsonl"
MUTATION_LOG = LOG_DIR / "mutations.jsonl"

# Enums
class ErrorDomain(str, Enum):
    """Error categorization domains."""
    DOCTRINE = "doctrine"
    SEMANTIC = "semantic"
    SEARCH = "search"
    ANALYSIS = "analysis"
    API = "api"
    VALIDATION = "validation"
    AUTHORITY = "authority"
    DRIFT = "drift"


class ResponseLayer(str, Enum):
    """Response generation layers."""
    DOCTRINE = "doctrine"
    RETRIEVAL = "retrieval"
    DEEP_ANALYSIS = "deep_analysis"
    STRATIFIED = "stratified"


class MutationType(str, Enum):
    """Types of system mutations."""
    DOCTRINE_ADD = "doctrine_add"
    DOCTRINE_UPDATE = "doctrine_update"
    DOCTRINE_DEPRECATE = "doctrine_deprecate"
    SEMANTIC_ADD = "semantic_add"
    SEMANTIC_UPDATE = "semantic_update"
    CONFIG_CHANGE = "config_change"
    AUTHORITY_UPDATE = "authority_update"


class MutationOrigin(str, Enum):
    """Source of mutations."""
    MANUAL = "manual"
    DRIFT_WATCHER = "drift_watcher"
    ADMIN_API = "admin_api"
    AUTOMATED = "automated"
    SYSTEM = "system"


# Dataclasses
@dataclass
class TelemetryStep:
    """Single step in a query trace."""
    step_name: str
    started_at: float
    completed_at: float = 0.0
    duration_ms: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None

    def complete(self, **extra_meta):
        """Mark step as complete and calculate duration."""
        self.completed_at = time.time()
        self.duration_ms = round((self.completed_at - self.started_at) * 1000, 2)
        if extra_meta:
            self.metadata.update(extra_meta)

    def fail(self, error_msg: str):
        """Mark step as failed."""
        self.error = error_msg
        self.complete()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "step_name": self.step_name,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "duration_ms": self.duration_ms,
            "metadata": self.metadata,
            "error": self.error
        }


@dataclass
class QueryTrace:
    """Complete trace of a query through the system."""
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    query_hash: str = ""
    query_text: str = ""
    started_at: float = field(default_factory=time.time)
    completed_at: float = 0.0
    total_ms: float = 0.0
    response_layer: Optional[ResponseLayer] = None
    doctrine_hit: bool = False
    semantic_matches: int = 0
    retrieval_count: int = 0
    steps: List[TelemetryStep] = field(default_factory=list)
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_step(self, name: str, **meta) -> TelemetryStep:
        """Add a new step to the trace."""
        step = TelemetryStep(step_name=name, started_at=time.time(), metadata=meta)
        self.steps.append(step)
        return step

    def complete(self, **extra_meta):
        """Mark trace as complete and calculate total duration."""
        self.completed_at = time.time()
        self.total_ms = round((self.completed_at - self.started_at) * 1000, 2)
        if extra_meta:
            self.metadata.update(extra_meta)

    def fail(self, error_msg: str):
        """Mark trace as failed."""
        self.error = error_msg
        self.complete()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "trace_id": self.trace_id,
            "query_hash": self.query_hash,
            "query_text": self.query_text,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "total_ms": self.total_ms,
            "response_layer": self.response_layer.value if self.response_layer else None,
            "doctrine_hit": self.doctrine_hit,
            "semantic_matches": self.semantic_matches,
            "retrieval_count": self.retrieval_count,
            "steps": [s.to_dict() for s in self.steps],
            "error": self.error,
            "metadata": self.metadata
        }


@dataclass
class ErrorRecord:
    """Structured error record."""
    error_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    domain: ErrorDomain = ErrorDomain.API
    message: str = ""
    trace_id: Optional[str] = None
    stack_trace: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "error_id": self.error_id,
            "timestamp": self.timestamp,
            "domain": self.domain.value,
            "message": self.message,
            "trace_id": self.trace_id,
            "stack_trace": self.stack_trace,
            "metadata": self.metadata
        }


@dataclass
class MutationRecord:
    """Record of a doctrine/config mutation for audit."""
    mutation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    mutation_type: MutationType = MutationType.DOCTRINE_ADD
    origin: MutationOrigin = MutationOrigin.MANUAL
    target: str = ""
    description: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "mutation_id": self.mutation_id,
            "timestamp": self.timestamp,
            "mutation_type": self.mutation_type.value,
            "origin": self.origin.value,
            "target": self.target,
            "description": self.description,
            "metadata": self.metadata
        }


class TelemetryCollector:
    """
    Ring-buffer telemetry with async-safe JSONL flush.
    - 10,000 trace ring buffer
    - 1,000 error ring buffer
    - 500 mutation ring buffer
    - Async lock for concurrent access
    - JSONL flush to disk
    - Percentile computation (p50, p95, p99)
    """

    TRACE_BUFFER_SIZE = 10_000
    ERROR_BUFFER_SIZE = 1_000
    MUTATION_BUFFER_SIZE = 500

    def __init__(self):
        self._traces: Deque[QueryTrace] = deque(maxlen=self.TRACE_BUFFER_SIZE)
        self._errors: Deque[ErrorRecord] = deque(maxlen=self.ERROR_BUFFER_SIZE)
        self._mutations: Deque[MutationRecord] = deque(maxlen=self.MUTATION_BUFFER_SIZE)
        self._lock = asyncio.Lock()
        self._started_at = time.time()
        self._total_queries = 0
        self._total_errors = 0
        self._doctrine_hits = 0

        logger.info(f"TelemetryCollector initialized | buffers: traces={self.TRACE_BUFFER_SIZE}, errors={self.ERROR_BUFFER_SIZE}, mutations={self.MUTATION_BUFFER_SIZE}")

    async def trace_query(self, query_hash: str, query_text: str = "") -> QueryTrace:
        """Start a new query trace."""
        trace = QueryTrace(query_hash=query_hash, query_text=query_text)
        async with self._lock:
            self._traces.append(trace)
            self._total_queries += 1
        logger.debug(f"Started trace {trace.trace_id} | query_hash={query_hash}")
        return trace

    async def add_step(self, trace: QueryTrace, step_name: str, **meta) -> TelemetryStep:
        """Add a step to an existing trace."""
        step = trace.add_step(step_name, **meta)
        logger.debug(f"Added step '{step_name}' to trace {trace.trace_id}")
        return step

    async def complete_trace(self, trace: QueryTrace, **extra_meta):
        """Mark trace as complete."""
        trace.complete(**extra_meta)
        if trace.doctrine_hit:
            async with self._lock:
                self._doctrine_hits += 1
        logger.info(f"Completed trace {trace.trace_id} | duration={trace.total_ms}ms | layer={trace.response_layer} | doctrine_hit={trace.doctrine_hit}")

    async def fail_trace(self, trace: QueryTrace, error_msg: str):
        """Mark trace as failed."""
        trace.fail(error_msg)
        async with self._lock:
            self._total_errors += 1
        logger.error(f"Failed trace {trace.trace_id} | error={error_msg}")

    async def log_error(self, domain: ErrorDomain, message: str, trace_id: Optional[str] = None, stack_trace: Optional[str] = None, **meta):
        """Log a structured error."""
        error = ErrorRecord(
            domain=domain,
            message=message,
            trace_id=trace_id,
            stack_trace=stack_trace,
            metadata=meta
        )
        async with self._lock:
            self._errors.append(error)
            self._total_errors += 1
        logger.error(f"Error logged | domain={domain.value} | error_id={error.error_id} | message={message}")
        return error

    async def record_mutation(self, mutation_type: MutationType, origin: MutationOrigin, target: str, description: str, **meta):
        """Record a doctrine/config mutation."""
        mutation = MutationRecord(
            mutation_type=mutation_type,
            origin=origin,
            target=target,
            description=description,
            metadata=meta
        )
        async with self._lock:
            self._mutations.append(mutation)
        logger.info(f"Mutation recorded | type={mutation_type.value} | origin={origin.value} | target={target} | mutation_id={mutation.mutation_id}")
        return mutation

    async def flush_to_disk(self):
        """Flush all buffers to JSONL files."""
        async with self._lock:
            trace_count = len(self._traces)
            error_count = len(self._errors)
            mutation_count = len(self._mutations)

            # Flush traces
            if trace_count > 0:
                with open(TELEMETRY_LOG, "a", encoding="utf-8") as f:
                    for trace in self._traces:
                        f.write(json.dumps(trace.to_dict()) + "\n")

            # Flush errors
            if error_count > 0:
                with open(ERROR_LOG, "a", encoding="utf-8") as f:
                    for error in self._errors:
                        f.write(json.dumps(error.to_dict()) + "\n")

            # Flush mutations
            if mutation_count > 0:
                with open(MUTATION_LOG, "a", encoding="utf-8") as f:
                    for mutation in self._mutations:
                        f.write(json.dumps(mutation.to_dict()) + "\n")

        logger.info(f"Flushed to disk | traces={trace_count}, errors={error_count}, mutations={mutation_count}")

    async def get_stats(self) -> Dict[str, Any]:
        """Get telemetry statistics with percentiles."""
        async with self._lock:
            traces = list(self._traces)
            errors = list(self._errors)
            mutations = list(self._mutations)

        # Calculate latency percentiles
        latencies = [t.total_ms for t in traces if t.total_ms > 0]
        p50 = statistics.median(latencies) if latencies else 0.0
        p95 = statistics.quantiles(latencies, n=20)[18] if len(latencies) >= 20 else (max(latencies) if latencies else 0.0)
        p99 = statistics.quantiles(latencies, n=100)[98] if len(latencies) >= 100 else (max(latencies) if latencies else 0.0)

        # Layer breakdown
        layer_counts = {}
        for trace in traces:
            if trace.response_layer:
                layer = trace.response_layer.value
                layer_counts[layer] = layer_counts.get(layer, 0) + 1

        # Error domain breakdown
        error_domains = {}
        for error in errors:
            domain = error.domain.value
            error_domains[domain] = error_domains.get(domain, 0) + 1

        uptime = time.time() - self._started_at

        return {
            "uptime_seconds": round(uptime, 2),
            "total_queries": self._total_queries,
            "total_errors": self._total_errors,
            "doctrine_hits": self._doctrine_hits,
            "buffer_counts": {
                "traces": len(traces),
                "errors": len(errors),
                "mutations": len(mutations)
            },
            "latency_percentiles": {
                "p50": round(p50, 2),
                "p95": round(p95, 2),
                "p99": round(p99, 2)
            },
            "layer_distribution": layer_counts,
            "error_domains": error_domains,
            "doctrine_hit_rate": round(self._doctrine_hits / self._total_queries * 100, 2) if self._total_queries > 0 else 0.0,
            "error_rate": round(self._total_errors / self._total_queries * 100, 2) if self._total_queries > 0 else 0.0
        }

    async def get_recent_traces(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent traces."""
        async with self._lock:
            traces = list(self._traces)[-limit:]
        return [t.to_dict() for t in traces]

    async def get_recent_errors(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent errors."""
        async with self._lock:
            errors = list(self._errors)[-limit:]
        return [e.to_dict() for e in errors]

    async def get_recent_mutations(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent mutations."""
        async with self._lock:
            mutations = list(self._mutations)[-limit:]
        return [m.to_dict() for m in mutations]

    def get_uptime(self) -> float:
        """Get system uptime in seconds."""
        return time.time() - self._started_at

    def get_error_rate(self) -> float:
        """Get error rate as percentage."""
        if self._total_queries == 0:
            return 0.0
        return round(self._total_errors / self._total_queries * 100, 2)

    def get_doctrine_hit_rate(self) -> float:
        """Get doctrine hit rate as percentage."""
        if self._total_queries == 0:
            return 0.0
        return round(self._doctrine_hits / self._total_queries * 100, 2)


# Global singleton
_telemetry_instance: Optional[TelemetryCollector] = None


def get_telemetry() -> TelemetryCollector:
    """Get or create the global telemetry collector singleton."""
    global _telemetry_instance
    if _telemetry_instance is None:
        _telemetry_instance = TelemetryCollector()
        logger.info("Global TelemetryCollector instance created")
    return _telemetry_instance


# Convenience functions
async def trace_query(query_hash: str, query_text: str = "") -> QueryTrace:
    """Start a new query trace (convenience wrapper)."""
    collector = get_telemetry()
    return await collector.trace_query(query_hash, query_text)


async def complete_trace(trace: QueryTrace, **extra_meta):
    """Complete a trace (convenience wrapper)."""
    collector = get_telemetry()
    await collector.complete_trace(trace, **extra_meta)


async def fail_trace(trace: QueryTrace, error_msg: str):
    """Fail a trace (convenience wrapper)."""
    collector = get_telemetry()
    await collector.fail_trace(trace, error_msg)


async def log_error(domain: ErrorDomain, message: str, trace_id: Optional[str] = None, stack_trace: Optional[str] = None, **meta):
    """Log an error (convenience wrapper)."""
    collector = get_telemetry()
    return await collector.log_error(domain, message, trace_id, stack_trace, **meta)


async def record_doctrine_mutation(mutation_type: MutationType, origin: MutationOrigin, target: str, description: str, **meta):
    """Record a doctrine mutation (convenience wrapper)."""
    collector = get_telemetry()
    return await collector.record_mutation(mutation_type, origin, target, description, **meta)


async def flush_loop():
    """Auto-flush telemetry to disk every 60 seconds."""
    collector = get_telemetry()
    logger.info("Telemetry flush loop started (interval=60s)")
    while True:
        try:
            await asyncio.sleep(60)
            await collector.flush_to_disk()
        except asyncio.CancelledError:
            logger.info("Flush loop cancelled, performing final flush")
            await collector.flush_to_disk()
            break
        except Exception as e:
            logger.error(f"Flush loop error: {e}")
            await log_error(
                ErrorDomain.API,
                f"Flush loop error: {str(e)}",
                stack_trace=traceback.format_exc()
            )


async def get_stats() -> Dict[str, Any]:
    """Get telemetry stats (convenience wrapper)."""
    collector = get_telemetry()
    return await collector.get_stats()


async def shutdown_telemetry():
    """Gracefully shut down telemetry system."""
    collector = get_telemetry()
    logger.info("Shutting down telemetry system")
    await collector.flush_to_disk()
    logger.info("Telemetry shutdown complete")


if __name__ == "__main__":
    # Test telemetry system
    async def test_telemetry():
        logger.info("=== Testing LG01 Telemetry System ===")

        # Start a trace
        trace = await trace_query("test_query_hash", "What is consideration in contract law?")

        # Add steps
        step1 = await get_telemetry().add_step(trace, "doctrine_lookup", topic="consideration")
        await asyncio.sleep(0.01)
        step1.complete(matched=True)

        step2 = await get_telemetry().add_step(trace, "semantic_search", terms=["consideration", "contract"])
        await asyncio.sleep(0.02)
        step2.complete(results=5)

        trace.doctrine_hit = True
        trace.response_layer = ResponseLayer.DOCTRINE
        trace.semantic_matches = 5

        await complete_trace(trace, confidence=0.95)

        # Log an error
        await log_error(
            ErrorDomain.SEARCH,
            "Test error message",
            trace_id=trace.trace_id,
            query="test query"
        )

        # Record a mutation
        await record_doctrine_mutation(
            MutationType.DOCTRINE_ADD,
            MutationOrigin.MANUAL,
            "consideration_doctrine",
            "Added new consideration doctrine"
        )

        # Get stats
        stats = await get_stats()
        logger.info(f"Stats: {json.dumps(stats, indent=2)}")

        # Flush to disk
        await get_telemetry().flush_to_disk()

        logger.info("=== Telemetry Test Complete ===")

    asyncio.run(test_telemetry())
