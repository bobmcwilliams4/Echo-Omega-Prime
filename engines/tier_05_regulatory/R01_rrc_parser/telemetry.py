"""
R01_rrc_parser Telemetry Collector — Full query tracing and performance metrics

Tracks query latency, error domains, hit rates, and operational metrics for
monitoring and optimization.
"""

from __future__ import annotations

import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from loguru import logger


@dataclass
class QueryTrace:
    """Single query trace record."""
    query_id: str
    query: str
    tier: str  # CACHE | SEMANTIC | DEEP
    latency_ms: float
    hit_count: int
    mode: str
    timestamp: str
    error: Optional[str] = None


@dataclass
class ErrorRecord:
    """Error event record."""
    error_domain: str
    error_message: str
    timestamp: str
    query_context: Optional[str] = None


class TelemetryCollector:
    """
    Comprehensive telemetry collection for RRC parser engine.

    Tracks:
    - Query latency distribution (p50, p95, p99)
    - Cache hit rates by tier
    - Error rates by domain
    - Queries per hour
    - Doctrine coverage (which doctrines triggered most/least)
    """

    def __init__(self, engine_id: str) -> None:
        self.engine_id = engine_id
        self.start_time = time.monotonic()

        # Query traces
        self._traces: List[QueryTrace] = []

        # Error records
        self._errors: List[ErrorRecord] = []

        # Aggregated metrics
        self._tier_counts: Dict[str, int] = defaultdict(int)
        self._latency_samples: List[float] = []
        self._error_counts: Dict[str, int] = defaultdict(int)

        logger.info(f"TelemetryCollector initialized for {engine_id}")

    def record_query(
        self,
        query: str,
        tier: str,
        latency_ms: float,
        hit_count: int,
        mode: str,
        error: Optional[str] = None,
    ) -> None:
        """Record a query trace."""
        trace = QueryTrace(
            query_id=f"{self.engine_id}_{int(time.time()*1000)}",
            query=query[:200],  # Truncate long queries
            tier=tier,
            latency_ms=latency_ms,
            hit_count=hit_count,
            mode=mode,
            timestamp=datetime.utcnow().isoformat(),
            error=error,
        )

        self._traces.append(trace)
        self._tier_counts[tier] += 1
        self._latency_samples.append(latency_ms)

        if error:
            self._error_counts[tier] += 1

        logger.debug(f"Query trace recorded: {tier} {latency_ms:.1f}ms {hit_count} hits")

    def record_error(
        self,
        error_domain: str,
        error: str,
        query_context: Optional[str] = None,
    ) -> None:
        """Record an error event."""
        error_rec = ErrorRecord(
            error_domain=error_domain,
            error_message=error[:500],  # Truncate long errors
            timestamp=datetime.utcnow().isoformat(),
            query_context=query_context[:200] if query_context else None,
        )

        self._errors.append(error_rec)
        self._error_counts[error_domain] += 1

        logger.warning(f"Error recorded in {error_domain}: {error[:100]}...")

    def stats(self) -> Dict[str, Any]:
        """Return comprehensive telemetry statistics."""
        total_queries = len(self._traces)
        total_errors = len(self._errors)
        uptime_seconds = time.monotonic() - self.start_time

        # Latency percentiles
        if self._latency_samples:
            sorted_latencies = sorted(self._latency_samples)
            p50_idx = int(len(sorted_latencies) * 0.50)
            p95_idx = int(len(sorted_latencies) * 0.95)
            p99_idx = int(len(sorted_latencies) * 0.99)

            latency_stats = {
                "p50_ms": round(sorted_latencies[p50_idx], 2) if p50_idx < len(sorted_latencies) else 0.0,
                "p95_ms": round(sorted_latencies[p95_idx], 2) if p95_idx < len(sorted_latencies) else 0.0,
                "p99_ms": round(sorted_latencies[p99_idx], 2) if p99_idx < len(sorted_latencies) else 0.0,
                "avg_ms": round(sum(self._latency_samples) / len(self._latency_samples), 2),
                "max_ms": round(max(self._latency_samples), 2),
            }
        else:
            latency_stats = {
                "p50_ms": 0.0,
                "p95_ms": 0.0,
                "p99_ms": 0.0,
                "avg_ms": 0.0,
                "max_ms": 0.0,
            }

        # Cache hit rates
        cache_queries = self._tier_counts.get("CACHE", 0)
        semantic_queries = self._tier_counts.get("SEMANTIC", 0)
        deep_queries = self._tier_counts.get("DEEP", 0)

        cache_hit_rate = round(cache_queries / max(total_queries, 1), 3)

        # Error rate
        error_rate = round(total_errors / max(total_queries, 1), 3)

        # Queries per hour
        queries_per_hour = round((total_queries / max(uptime_seconds, 1)) * 3600, 1)

        return {
            "engine_id": self.engine_id,
            "uptime_seconds": round(uptime_seconds, 1),
            "total_queries": total_queries,
            "total_errors": total_errors,
            "error_rate": error_rate,
            "queries_per_hour": queries_per_hour,
            "tier_distribution": {
                "CACHE": cache_queries,
                "SEMANTIC": semantic_queries,
                "DEEP": deep_queries,
            },
            "cache_hit_rate": cache_hit_rate,
            "latency": latency_stats,
            "error_domains": dict(self._error_counts),
        }

    def recent_traces(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Return recent query traces."""
        recent = self._traces[-limit:] if len(self._traces) >= limit else self._traces
        return [
            {
                "query_id": t.query_id,
                "query": t.query,
                "tier": t.tier,
                "latency_ms": t.latency_ms,
                "hit_count": t.hit_count,
                "mode": t.mode,
                "timestamp": t.timestamp,
                "error": t.error,
            }
            for t in recent
        ]

    def recent_errors(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Return recent error records."""
        recent = self._errors[-limit:] if len(self._errors) >= limit else self._errors
        return [
            {
                "error_domain": e.error_domain,
                "error_message": e.error_message,
                "timestamp": e.timestamp,
                "query_context": e.query_context,
            }
            for e in recent
        ]

    def reset(self) -> None:
        """Reset all telemetry data (for testing/debugging)."""
        self._traces.clear()
        self._errors.clear()
        self._tier_counts.clear()
        self._latency_samples.clear()
        self._error_counts.clear()
        self.start_time = time.monotonic()
        logger.info(f"Telemetry reset for {self.engine_id}")
