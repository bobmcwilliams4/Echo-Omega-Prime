"""
LMIE Telemetry Module — Query tracing, latency tracking, error domains.

Provides TIE Components 8 (telemetry), 9 (drift watcher), 10 (coverage map),
and 11 (metrics collector) for the Landman Intelligence Engine.

Commander: Bobby Don McWilliams II | Authority: 11.0 SOVEREIGN
"""

from __future__ import annotations

import json
import time
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from loguru import logger


# ═══════════════════════════════════════════════════════════════════
# QUERY PHASES
# ═══════════════════════════════════════════════════════════════════

class QueryPhase(str, Enum):
    RECEIVED = "RECEIVED"
    VALIDATED = "VALIDATED"
    CLASSIFIED = "CLASSIFIED"
    DOCTRINE_LOOKUP = "DOCTRINE_LOOKUP"
    CLOUD_RETRIEVAL = "CLOUD_RETRIEVAL"
    CHILD_ROUTING = "CHILD_ROUTING"
    SYNTHESIS = "SYNTHESIS"
    COMPLETE = "COMPLETE"
    ERROR = "ERROR"


# ═══════════════════════════════════════════════════════════════════
# QUERY TRACE
# ═══════════════════════════════════════════════════════════════════

@dataclass
class QueryTrace:
    """Full trace of a single query execution."""
    trace_id: str
    query_text: str
    session_id: str
    response_mode: str
    start_time: float = field(default_factory=time.monotonic)
    phases: List[Dict[str, Any]] = field(default_factory=list)
    current_phase: QueryPhase = QueryPhase.RECEIVED
    categories_detected: List[str] = field(default_factory=list)
    engines_routed: List[str] = field(default_factory=list)
    doctrines_matched: List[str] = field(default_factory=list)
    cloud_sources: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    vector_fallback: bool = False
    cache_hit: bool = False

    def enter_phase(self, phase: QueryPhase) -> None:
        elapsed = (time.monotonic() - self.start_time) * 1000
        self.phases.append({
            "phase": phase.value,
            "entered_at_ms": round(elapsed, 2),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        self.current_phase = phase

    def record_error(self, error: str) -> None:
        self.errors.append(error)
        self.enter_phase(QueryPhase.ERROR)

    @property
    def total_latency_ms(self) -> float:
        return round((time.monotonic() - self.start_time) * 1000, 2)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "trace_id": self.trace_id,
            "query": self.query_text[:200],
            "session_id": self.session_id,
            "mode": self.response_mode,
            "total_latency_ms": self.total_latency_ms,
            "phases": self.phases,
            "categories": self.categories_detected,
            "engines_routed": self.engines_routed,
            "doctrines_matched": self.doctrines_matched,
            "cloud_sources": self.cloud_sources,
            "errors": self.errors,
            "vector_fallback": self.vector_fallback,
            "cache_hit": self.cache_hit,
        }


# ═══════════════════════════════════════════════════════════════════
# TIE COMPONENT 8: TELEMETRY COLLECTOR
# ═══════════════════════════════════════════════════════════════════

class TelemetryCollector:
    """Collects and aggregates query performance telemetry."""

    def __init__(self, max_traces: int = 2000) -> None:
        self._traces: List[Dict[str, Any]] = []
        self._max_traces = max_traces
        self._total_queries = 0
        self._total_latency_ms = 0.0
        self._error_count = 0
        self._cache_hits = 0
        self._vector_fallbacks = 0
        self._category_counter: Counter = Counter()
        self._engine_counter: Counter = Counter()
        self._doctrine_counter: Counter = Counter()
        self._hourly_counts: Dict[str, int] = defaultdict(int)

    def record_trace(self, trace: QueryTrace) -> None:
        trace_dict = trace.to_dict()
        self._traces.append(trace_dict)
        if len(self._traces) > self._max_traces:
            self._traces = self._traces[-self._max_traces // 2:]

        self._total_queries += 1
        self._total_latency_ms += trace.total_latency_ms
        if trace.errors:
            self._error_count += 1
        if trace.cache_hit:
            self._cache_hits += 1
        if trace.vector_fallback:
            self._vector_fallbacks += 1

        for cat in trace.categories_detected:
            self._category_counter[cat] += 1
        for eng in trace.engines_routed:
            self._engine_counter[eng] += 1
        for doc in trace.doctrines_matched:
            self._doctrine_counter[doc] += 1

        hour_key = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H")
        self._hourly_counts[hour_key] += 1

    def start_query(self, query_text: str, session_id: str, response_mode: str, trace_id: str) -> QueryTrace:
        return QueryTrace(
            trace_id=trace_id,
            query_text=query_text,
            session_id=session_id,
            response_mode=response_mode,
        )

    def summary(self) -> Dict[str, Any]:
        avg_latency = round(self._total_latency_ms / max(self._total_queries, 1), 2)
        return {
            "total_queries": self._total_queries,
            "avg_latency_ms": avg_latency,
            "error_count": self._error_count,
            "error_rate": round(self._error_count / max(self._total_queries, 1), 4),
            "cache_hit_rate": round(self._cache_hits / max(self._total_queries, 1), 4),
            "vector_fallback_rate": round(self._vector_fallbacks / max(self._total_queries, 1), 4),
            "top_categories": self._category_counter.most_common(10),
            "top_engines": self._engine_counter.most_common(10),
            "top_doctrines": self._doctrine_counter.most_common(10),
            "recent_traces": len(self._traces),
        }

    def recent_traces(self, limit: int = 50) -> List[Dict[str, Any]]:
        return self._traces[-limit:]

    def hourly_throughput(self) -> Dict[str, int]:
        return dict(sorted(self._hourly_counts.items())[-24:])


# ═══════════════════════════════════════════════════════════════════
# TIE COMPONENT 9: DRIFT WATCHER
# ═══════════════════════════════════════════════════════════════════

class DriftWatcher:
    """Detects doctrine drift — when query patterns diverge from doctrine coverage."""

    def __init__(self) -> None:
        self._unmatched_queries: List[Dict[str, Any]] = []
        self._drift_alerts: List[Dict[str, Any]] = []

    def record_unmatched(self, query: str, categories: List[str]) -> None:
        self._unmatched_queries.append({
            "query": query[:200],
            "categories": categories,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        if len(self._unmatched_queries) > 500:
            self._unmatched_queries = self._unmatched_queries[-250:]

        # Alert if too many unmatched queries
        if len(self._unmatched_queries) % 50 == 0:
            self._drift_alerts.append({
                "alert": f"Doctrine coverage gap: {len(self._unmatched_queries)} unmatched queries",
                "top_unmatched_categories": Counter(
                    cat for q in self._unmatched_queries[-50:] for cat in q["categories"]
                ).most_common(5),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })

    def get_drift_report(self) -> Dict[str, Any]:
        return {
            "unmatched_count": len(self._unmatched_queries),
            "recent_unmatched": self._unmatched_queries[-10:],
            "alerts": self._drift_alerts[-5:],
        }


# ═══════════════════════════════════════════════════════════════════
# TIE COMPONENT 10: COVERAGE MAP
# ═══════════════════════════════════════════════════════════════════

class CoverageMap:
    """Tracks which doctrines have been triggered and identifies gaps."""

    def __init__(self, all_topics: Set[str]) -> None:
        self._all_topics = all_topics
        self._triggered: Set[str] = set()
        self._trigger_counts: Counter = Counter()

    def record_trigger(self, topic: str) -> None:
        self._triggered.add(topic)
        self._trigger_counts[topic] += 1

    def get_coverage(self) -> Dict[str, Any]:
        untriggered = self._all_topics - self._triggered
        return {
            "total_doctrines": len(self._all_topics),
            "triggered": len(self._triggered),
            "untriggered": len(untriggered),
            "coverage_pct": round(len(self._triggered) / max(len(self._all_topics), 1) * 100, 1),
            "untriggered_topics": sorted(untriggered),
            "most_triggered": self._trigger_counts.most_common(10),
            "least_triggered": self._trigger_counts.most_common()[-10:] if self._trigger_counts else [],
        }


logger.info("LMIE telemetry module loaded")
