"""
LM06 Right of Way Engine - Telemetry & Metrics Collection
==========================================================
Comprehensive telemetry for query tracking, latency monitoring, error analysis,
cache hit rates, and performance metrics.

Tracks: Query latency, doctrine cache hits/misses, semantic normalization stats,
search performance, error rates by category, usage patterns.
"""

from __future__ import annotations

import time
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Deque, Dict, List, Optional, Set

from loguru import logger
from pydantic import BaseModel


# ============================================================================
# ENUMS
# ============================================================================

class QueryPhase(str, Enum):
    """Query execution phases for latency tracking."""
    NORMALIZATION = "normalization"
    DOCTRINE_CACHE = "doctrine_cache"
    SEMANTIC_SEARCH = "semantic_search"
    VECTOR_SEARCH = "vector_search"
    CLOUD_RETRIEVAL = "cloud_retrieval"
    DEEP_ANALYSIS = "deep_analysis"
    RESPONSE_FORMATTING = "response_formatting"


class ErrorDomain(str, Enum):
    """Error categorization domains."""
    VALIDATION = "validation"
    NORMALIZATION = "normalization"
    DOCTRINE_LOOKUP = "doctrine_lookup"
    SEARCH = "search"
    CLOUD_RETRIEVAL = "cloud_retrieval"
    RESPONSE_GENERATION = "response_generation"
    SYSTEM = "system"


# ============================================================================
# DATACLASSES
# ============================================================================

@dataclass
class QueryMetrics:
    """Metrics for a single query."""
    query_id: str
    query_text: str
    timestamp: datetime
    response_mode: str
    total_latency_ms: float
    phase_latencies: Dict[QueryPhase, float] = field(default_factory=dict)
    doctrine_hits: int = 0
    doctrine_misses: int = 0
    search_results: int = 0
    cloud_calls: int = 0
    error: Optional[str] = None
    error_domain: Optional[ErrorDomain] = None


@dataclass
class TelemetryCollector:
    """
    Telemetry data collector with rolling windows and aggregation.

    Tracks:
    - Per-query metrics (last 1000 queries)
    - Aggregated stats (hourly, daily)
    - Error tracking by domain
    - Cache hit rates
    - Latency percentiles
    """
    # Recent queries (rolling window of last 1000)
    recent_queries: Deque[QueryMetrics] = field(default_factory=lambda: deque(maxlen=1000))

    # Counters
    total_queries: int = 0
    total_errors: int = 0
    doctrine_cache_hits: int = 0
    doctrine_cache_misses: int = 0
    cloud_retrieval_calls: int = 0

    # Latency tracking by phase (sum for averaging)
    phase_latency_sums: Dict[QueryPhase, float] = field(default_factory=dict)
    phase_query_counts: Dict[QueryPhase, int] = field(default_factory=dict)

    # Error tracking by domain
    errors_by_domain: Dict[ErrorDomain, int] = field(default_factory=dict)

    # Response mode usage
    mode_usage: Dict[str, int] = field(default_factory=dict)

    # Hourly stats (last 24 hours)
    hourly_query_counts: Deque[int] = field(default_factory=lambda: deque([0] * 24, maxlen=24))
    current_hour: int = field(default_factory=lambda: datetime.now(timezone.utc).hour)

    # Start time
    start_time: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class TelemetrySnapshot(BaseModel):
    """Snapshot of current telemetry state."""
    total_queries: int
    total_errors: int
    error_rate: float
    uptime_seconds: float
    queries_per_hour: float
    avg_latency_ms: float
    p50_latency_ms: float
    p95_latency_ms: float
    p99_latency_ms: float
    cache_hit_rate: float
    cloud_retrieval_rate: float
    errors_by_domain: Dict[str, int]
    mode_usage: Dict[str, int]
    recent_errors: List[str]


class DashboardData(BaseModel):
    """Dashboard-ready telemetry data."""
    snapshot: TelemetrySnapshot
    phase_latencies: Dict[str, float]
    hourly_query_counts: List[int]
    top_errors: List[Dict[str, Any]]


# ============================================================================
# TELEMETRY FUNCTIONS
# ============================================================================

_TELEMETRY: Optional[TelemetryCollector] = None


def get_telemetry() -> TelemetryCollector:
    """Get singleton telemetry collector."""
    global _TELEMETRY
    if _TELEMETRY is None:
        _TELEMETRY = TelemetryCollector()
        logger.info("Initialized telemetry collector")
    return _TELEMETRY


def record_query(
    query_id: str,
    query_text: str,
    response_mode: str,
    total_latency_ms: float,
    phase_latencies: Dict[QueryPhase, float],
    doctrine_hits: int = 0,
    doctrine_misses: int = 0,
    search_results: int = 0,
    cloud_calls: int = 0,
    error: Optional[str] = None,
    error_domain: Optional[ErrorDomain] = None,
) -> None:
    """
    Record metrics for a completed query.

    Args:
        query_id: Unique query identifier
        query_text: Original query text
        response_mode: Response mode used (fast/defense/memo)
        total_latency_ms: Total query latency in milliseconds
        phase_latencies: Latency breakdown by phase
        doctrine_hits: Number of doctrine cache hits
        doctrine_misses: Number of doctrine cache misses
        search_results: Number of search results returned
        cloud_calls: Number of cloud retrieval calls
        error: Error message if query failed
        error_domain: Error categorization domain
    """
    telemetry = get_telemetry()

    # Create metrics record
    metrics = QueryMetrics(
        query_id=query_id,
        query_text=query_text,
        timestamp=datetime.now(timezone.utc),
        response_mode=response_mode,
        total_latency_ms=total_latency_ms,
        phase_latencies=phase_latencies,
        doctrine_hits=doctrine_hits,
        doctrine_misses=doctrine_misses,
        search_results=search_results,
        cloud_calls=cloud_calls,
        error=error,
        error_domain=error_domain,
    )

    # Add to recent queries
    telemetry.recent_queries.append(metrics)

    # Update counters
    telemetry.total_queries += 1

    if error:
        telemetry.total_errors += 1
        if error_domain:
            telemetry.errors_by_domain[error_domain] = telemetry.errors_by_domain.get(error_domain, 0) + 1

    telemetry.doctrine_cache_hits += doctrine_hits
    telemetry.doctrine_cache_misses += doctrine_misses
    telemetry.cloud_retrieval_calls += cloud_calls

    # Update mode usage
    telemetry.mode_usage[response_mode] = telemetry.mode_usage.get(response_mode, 0) + 1

    # Update phase latencies
    for phase, latency in phase_latencies.items():
        telemetry.phase_latency_sums[phase] = telemetry.phase_latency_sums.get(phase, 0.0) + latency
        telemetry.phase_query_counts[phase] = telemetry.phase_query_counts.get(phase, 0) + 1

    # Update hourly counts
    current_hour = datetime.now(timezone.utc).hour
    if current_hour != telemetry.current_hour:
        # New hour, rotate hourly counts
        telemetry.current_hour = current_hour
        telemetry.hourly_query_counts.append(0)
    telemetry.hourly_query_counts[-1] += 1


def get_snapshot() -> TelemetrySnapshot:
    """Get current telemetry snapshot."""
    telemetry = get_telemetry()

    # Calculate uptime
    uptime_seconds = (datetime.now(timezone.utc) - telemetry.start_time).total_seconds()

    # Calculate error rate
    error_rate = telemetry.total_errors / max(telemetry.total_queries, 1)

    # Calculate queries per hour
    queries_per_hour = (telemetry.total_queries / max(uptime_seconds / 3600, 0.01))

    # Calculate latency percentiles
    latencies = [q.total_latency_ms for q in telemetry.recent_queries if q.error is None]
    if latencies:
        latencies_sorted = sorted(latencies)
        p50_idx = int(len(latencies_sorted) * 0.50)
        p95_idx = int(len(latencies_sorted) * 0.95)
        p99_idx = int(len(latencies_sorted) * 0.99)

        p50_latency = latencies_sorted[p50_idx] if p50_idx < len(latencies_sorted) else 0.0
        p95_latency = latencies_sorted[p95_idx] if p95_idx < len(latencies_sorted) else 0.0
        p99_latency = latencies_sorted[p99_idx] if p99_idx < len(latencies_sorted) else 0.0
        avg_latency = sum(latencies) / len(latencies)
    else:
        p50_latency = p95_latency = p99_latency = avg_latency = 0.0

    # Calculate cache hit rate
    total_cache_accesses = telemetry.doctrine_cache_hits + telemetry.doctrine_cache_misses
    cache_hit_rate = telemetry.doctrine_cache_hits / max(total_cache_accesses, 1)

    # Calculate cloud retrieval rate
    cloud_retrieval_rate = telemetry.cloud_retrieval_calls / max(telemetry.total_queries, 1)

    # Recent errors (last 10)
    recent_errors = [
        q.error for q in list(telemetry.recent_queries)[-10:]
        if q.error is not None
    ]

    return TelemetrySnapshot(
        total_queries=telemetry.total_queries,
        total_errors=telemetry.total_errors,
        error_rate=error_rate,
        uptime_seconds=uptime_seconds,
        queries_per_hour=queries_per_hour,
        avg_latency_ms=avg_latency,
        p50_latency_ms=p50_latency,
        p95_latency_ms=p95_latency,
        p99_latency_ms=p99_latency,
        cache_hit_rate=cache_hit_rate,
        cloud_retrieval_rate=cloud_retrieval_rate,
        errors_by_domain={k.value: v for k, v in telemetry.errors_by_domain.items()},
        mode_usage=telemetry.mode_usage,
        recent_errors=recent_errors,
    )


def get_phase_latencies() -> Dict[str, float]:
    """Get average latency by query phase."""
    telemetry = get_telemetry()

    phase_avgs = {}
    for phase, total_latency in telemetry.phase_latency_sums.items():
        count = telemetry.phase_query_counts.get(phase, 1)
        phase_avgs[phase.value] = total_latency / count

    return phase_avgs


def telemetry_dashboard() -> DashboardData:
    """Get comprehensive dashboard data."""
    telemetry = get_telemetry()
    snapshot = get_snapshot()
    phase_latencies = get_phase_latencies()

    # Top errors (by domain, sorted by count)
    top_errors = [
        {"domain": domain.value, "count": count}
        for domain, count in sorted(
            telemetry.errors_by_domain.items(),
            key=lambda x: x[1],
            reverse=True
        )
    ]

    return DashboardData(
        snapshot=snapshot,
        phase_latencies=phase_latencies,
        hourly_query_counts=list(telemetry.hourly_query_counts),
        top_errors=top_errors,
    )


def telemetry_health() -> Dict[str, Any]:
    """Get telemetry system health."""
    telemetry = get_telemetry()
    snapshot = get_snapshot()

    return {
        "status": "healthy" if snapshot.error_rate < 0.05 else "degraded" if snapshot.error_rate < 0.15 else "critical",
        "total_queries": telemetry.total_queries,
        "error_rate": snapshot.error_rate,
        "avg_latency_ms": snapshot.avg_latency_ms,
        "cache_hit_rate": snapshot.cache_hit_rate,
        "uptime_hours": snapshot.uptime_seconds / 3600,
    }


def reset_telemetry() -> None:
    """Reset telemetry (for testing/debugging only)."""
    global _TELEMETRY
    _TELEMETRY = TelemetryCollector()
    logger.warning("Telemetry reset (all metrics cleared)")


# ============================================================================
# CONTEXT MANAGER FOR LATENCY TRACKING
# ============================================================================

class PhaseTimer:
    """Context manager for tracking phase latency."""

    def __init__(self, phase: QueryPhase, phase_latencies: Dict[QueryPhase, float]):
        self.phase = phase
        self.phase_latencies = phase_latencies
        self.start_time = 0.0

    def __enter__(self):
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed_ms = (time.perf_counter() - self.start_time) * 1000
        self.phase_latencies[self.phase] = elapsed_ms


# ============================================================================
# EXPORT FOR TESTING
# ============================================================================

if __name__ == "__main__":
    # Test telemetry
    print("=== Telemetry Test ===\n")

    # Record some test queries
    for i in range(10):
        record_query(
            query_id=f"Q{i+1:03d}",
            query_text=f"test query {i+1}",
            response_mode="fast" if i % 2 == 0 else "defense",
            total_latency_ms=50.0 + i * 10,
            phase_latencies={
                QueryPhase.NORMALIZATION: 5.0 + i,
                QueryPhase.DOCTRINE_CACHE: 20.0 + i * 2,
                QueryPhase.RESPONSE_FORMATTING: 10.0 + i,
            },
            doctrine_hits=3 if i % 3 != 0 else 0,
            doctrine_misses=0 if i % 3 != 0 else 2,
            cloud_calls=1 if i % 5 == 0 else 0,
            error="test error" if i == 7 else None,
            error_domain=ErrorDomain.SEARCH if i == 7 else None,
        )

    # Get snapshot
    snapshot = get_snapshot()
    print(f"Total queries: {snapshot.total_queries}")
    print(f"Error rate: {snapshot.error_rate:.2%}")
    print(f"Avg latency: {snapshot.avg_latency_ms:.2f} ms")
    print(f"P95 latency: {snapshot.p95_latency_ms:.2f} ms")
    print(f"Cache hit rate: {snapshot.cache_hit_rate:.2%}")
    print(f"\nMode usage: {snapshot.mode_usage}")
    print(f"Errors by domain: {snapshot.errors_by_domain}")

    # Get dashboard
    dashboard = telemetry_dashboard()
    print(f"\nPhase latencies:")
    for phase, latency in dashboard.phase_latencies.items():
        print(f"  {phase}: {latency:.2f} ms")
