"""
LIE Telemetry Module — Query tracing, performance monitoring, and audit logging.

Tracks all queries, routing decisions, child engine calls, doctrine hits,
and performance metrics. Provides comprehensive audit trail for legal analysis.

Commander: Bobby Don McWilliams II | Authority: 11.0 SOVEREIGN
"""

from __future__ import annotations

import hashlib
import json
import time
import uuid
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from loguru import logger


# ═══════════════════════════════════════════════════════════════════
# TELEMETRY MODELS
# ═══════════════════════════════════════════════════════════════════

class EventType(str, Enum):
    QUERY_START = "QUERY_START"
    QUERY_COMPLETE = "QUERY_COMPLETE"
    DOCTRINE_HIT = "DOCTRINE_HIT"
    CHILD_ROUTE = "CHILD_ROUTE"
    CHILD_RESPONSE = "CHILD_RESPONSE"
    CHILD_ERROR = "CHILD_ERROR"
    CLOUD_RETRIEVAL = "CLOUD_RETRIEVAL"
    CITATION_EXTRACT = "CITATION_EXTRACT"
    ERROR = "ERROR"
    WARNING = "WARNING"


@dataclass
class TelemetryEvent:
    """Single telemetry event."""
    event_id: str
    event_type: EventType
    timestamp: str
    query_id: str
    engine_id: str
    details: Dict[str, Any] = field(default_factory=dict)
    latency_ms: Optional[float] = None
    error: Optional[str] = None


@dataclass
class QueryTrace:
    """Complete trace of a single query execution."""
    query_id: str
    query_text: str
    normalized_query: str
    start_time: str
    end_time: Optional[str] = None
    total_latency_ms: Optional[float] = None
    mode: str = "FAST"
    zone: str = "PLANNING"
    confidence: str = "DEFENSIBLE"
    practice_areas: List[str] = field(default_factory=list)
    doctrines_triggered: List[str] = field(default_factory=list)
    children_routed: List[str] = field(default_factory=list)
    child_latencies: Dict[str, float] = field(default_factory=dict)
    cloud_results: int = 0
    citations_extracted: int = 0
    events: List[TelemetryEvent] = field(default_factory=list)
    sha256_hash: Optional[str] = None
    user_agent: Optional[str] = None
    client_ip: Optional[str] = None


@dataclass
class PerformanceMetrics:
    """Aggregated performance metrics."""
    total_queries: int = 0
    avg_latency_ms: float = 0.0
    p50_latency_ms: float = 0.0
    p95_latency_ms: float = 0.0
    p99_latency_ms: float = 0.0
    max_latency_ms: float = 0.0
    min_latency_ms: float = float('inf')
    doctrine_hit_rate: float = 0.0
    child_routing_rate: float = 0.0
    cloud_usage_rate: float = 0.0
    error_rate: float = 0.0
    queries_by_mode: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    queries_by_zone: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    queries_by_practice: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    errors_by_type: Dict[str, int] = field(default_factory=lambda: defaultdict(int))


# ═══════════════════════════════════════════════════════════════════
# TELEMETRY COLLECTOR
# ═══════════════════════════════════════════════════════════════════

class TelemetryCollector:
    """
    Centralized telemetry collector for LIE engine.

    Tracks all query events, maintains audit trail, and calculates
    performance metrics.
    """

    def __init__(self, engine_id: str = "LIE", log_dir: Optional[Path] = None):
        self.engine_id = engine_id
        self.active_traces: Dict[str, QueryTrace] = {}
        self.completed_traces: List[QueryTrace] = []
        self.all_latencies: List[float] = []
        self.log_dir = log_dir or Path(__file__).parent / "logs"
        self.log_dir.mkdir(exist_ok=True)
        self.audit_log_path = self.log_dir / "audit_trail.jsonl"

        logger.info(f"Telemetry collector initialized for {engine_id}")
        logger.info(f"Audit log: {self.audit_log_path}")

    def start_query(
        self,
        query: str,
        normalized_query: str,
        mode: str,
        zone: str,
        confidence: str,
        user_agent: Optional[str] = None,
        client_ip: Optional[str] = None,
    ) -> str:
        """
        Start tracking a new query.

        Args:
            query: Original query text
            normalized_query: Normalized query
            mode: Response mode (FAST, DEFENSE, MEMO)
            zone: Analysis zone (PLANNING, REPORTING, AUDIT, LITIGATION)
            confidence: Confidence level
            user_agent: Optional user agent string
            client_ip: Optional client IP

        Returns:
            Unique query ID
        """
        query_id = str(uuid.uuid4())
        start_time = datetime.now(timezone.utc).isoformat()

        trace = QueryTrace(
            query_id=query_id,
            query_text=query,
            normalized_query=normalized_query,
            start_time=start_time,
            mode=mode,
            zone=zone,
            confidence=confidence,
            user_agent=user_agent,
            client_ip=client_ip,
        )

        self.active_traces[query_id] = trace

        # Log start event
        event = TelemetryEvent(
            event_id=str(uuid.uuid4()),
            event_type=EventType.QUERY_START,
            timestamp=start_time,
            query_id=query_id,
            engine_id=self.engine_id,
            details={
                "query": query,
                "normalized_query": normalized_query,
                "mode": mode,
                "zone": zone,
                "confidence": confidence,
            },
        )

        trace.events.append(event)

        logger.info(f"Query started: {query_id[:8]}... | mode={mode} zone={zone}")

        return query_id

    def record_doctrine_hit(
        self,
        query_id: str,
        doctrine_topic: str,
        keywords_matched: List[str],
    ):
        """Record a doctrine cache hit."""
        if query_id not in self.active_traces:
            logger.warning(f"Query {query_id[:8]} not found in active traces")
            return

        trace = self.active_traces[query_id]
        trace.doctrines_triggered.append(doctrine_topic)

        event = TelemetryEvent(
            event_id=str(uuid.uuid4()),
            event_type=EventType.DOCTRINE_HIT,
            timestamp=datetime.now(timezone.utc).isoformat(),
            query_id=query_id,
            engine_id=self.engine_id,
            details={
                "doctrine_topic": doctrine_topic,
                "keywords_matched": keywords_matched,
            },
        )

        trace.events.append(event)

    def record_child_route(
        self,
        query_id: str,
        child_id: str,
        child_name: str,
        practice_areas: List[str],
    ):
        """Record routing to a child engine."""
        if query_id not in self.active_traces:
            logger.warning(f"Query {query_id[:8]} not found in active traces")
            return

        trace = self.active_traces[query_id]
        trace.children_routed.append(child_id)

        event = TelemetryEvent(
            event_id=str(uuid.uuid4()),
            event_type=EventType.CHILD_ROUTE,
            timestamp=datetime.now(timezone.utc).isoformat(),
            query_id=query_id,
            engine_id=self.engine_id,
            details={
                "child_id": child_id,
                "child_name": child_name,
                "practice_areas": practice_areas,
            },
        )

        trace.events.append(event)

    def record_child_response(
        self,
        query_id: str,
        child_id: str,
        latency_ms: float,
        confidence: str,
        sources_count: int,
    ):
        """Record successful child engine response."""
        if query_id not in self.active_traces:
            logger.warning(f"Query {query_id[:8]} not found in active traces")
            return

        trace = self.active_traces[query_id]
        trace.child_latencies[child_id] = latency_ms

        event = TelemetryEvent(
            event_id=str(uuid.uuid4()),
            event_type=EventType.CHILD_RESPONSE,
            timestamp=datetime.now(timezone.utc).isoformat(),
            query_id=query_id,
            engine_id=self.engine_id,
            details={
                "child_id": child_id,
                "confidence": confidence,
                "sources_count": sources_count,
            },
            latency_ms=latency_ms,
        )

        trace.events.append(event)

    def record_child_error(
        self,
        query_id: str,
        child_id: str,
        error_msg: str,
    ):
        """Record child engine error."""
        if query_id not in self.active_traces:
            logger.warning(f"Query {query_id[:8]} not found in active traces")
            return

        trace = self.active_traces[query_id]

        event = TelemetryEvent(
            event_id=str(uuid.uuid4()),
            event_type=EventType.CHILD_ERROR,
            timestamp=datetime.now(timezone.utc).isoformat(),
            query_id=query_id,
            engine_id=self.engine_id,
            details={
                "child_id": child_id,
            },
            error=error_msg,
        )

        trace.events.append(event)

    def record_cloud_retrieval(
        self,
        query_id: str,
        results_count: int,
        latency_ms: float,
    ):
        """Record cloud knowledge retrieval."""
        if query_id not in self.active_traces:
            logger.warning(f"Query {query_id[:8]} not found in active traces")
            return

        trace = self.active_traces[query_id]
        trace.cloud_results = results_count

        event = TelemetryEvent(
            event_id=str(uuid.uuid4()),
            event_type=EventType.CLOUD_RETRIEVAL,
            timestamp=datetime.now(timezone.utc).isoformat(),
            query_id=query_id,
            engine_id=self.engine_id,
            details={
                "results_count": results_count,
            },
            latency_ms=latency_ms,
        )

        trace.events.append(event)

    def record_citations(
        self,
        query_id: str,
        citations: List[str],
    ):
        """Record extracted citations."""
        if query_id not in self.active_traces:
            logger.warning(f"Query {query_id[:8]} not found in active traces")
            return

        trace = self.active_traces[query_id]
        trace.citations_extracted = len(citations)

        event = TelemetryEvent(
            event_id=str(uuid.uuid4()),
            event_type=EventType.CITATION_EXTRACT,
            timestamp=datetime.now(timezone.utc).isoformat(),
            query_id=query_id,
            engine_id=self.engine_id,
            details={
                "citations": citations,
                "count": len(citations),
            },
        )

        trace.events.append(event)

    def complete_query(
        self,
        query_id: str,
        practice_areas: List[str],
        sha256_hash: str,
    ):
        """
        Mark query as complete and calculate final metrics.

        Args:
            query_id: Query ID
            practice_areas: List of practice areas queried
            sha256_hash: Determinism hash
        """
        if query_id not in self.active_traces:
            logger.warning(f"Query {query_id[:8]} not found in active traces")
            return

        trace = self.active_traces[query_id]
        end_time = datetime.now(timezone.utc).isoformat()
        trace.end_time = end_time
        trace.practice_areas = practice_areas
        trace.sha256_hash = sha256_hash

        # Calculate total latency
        start_dt = datetime.fromisoformat(trace.start_time)
        end_dt = datetime.fromisoformat(end_time)
        total_latency = (end_dt - start_dt).total_seconds() * 1000
        trace.total_latency_ms = round(total_latency, 2)

        # Log completion event
        event = TelemetryEvent(
            event_id=str(uuid.uuid4()),
            event_type=EventType.QUERY_COMPLETE,
            timestamp=end_time,
            query_id=query_id,
            engine_id=self.engine_id,
            details={
                "practice_areas": practice_areas,
                "doctrines_triggered": len(trace.doctrines_triggered),
                "children_routed": len(trace.children_routed),
                "cloud_results": trace.cloud_results,
                "citations": trace.citations_extracted,
            },
            latency_ms=trace.total_latency_ms,
        )

        trace.events.append(event)

        # Move to completed traces
        self.completed_traces.append(trace)
        self.all_latencies.append(trace.total_latency_ms)
        del self.active_traces[query_id]

        # Write to audit log
        self._write_audit_log(trace)

        logger.info(
            f"Query completed: {query_id[:8]}... | "
            f"latency={trace.total_latency_ms:.2f}ms | "
            f"doctrines={len(trace.doctrines_triggered)} | "
            f"children={len(trace.children_routed)}"
        )

    def record_error(
        self,
        query_id: Optional[str],
        error_type: str,
        error_msg: str,
        details: Optional[Dict[str, Any]] = None,
    ):
        """Record an error event."""
        event = TelemetryEvent(
            event_id=str(uuid.uuid4()),
            event_type=EventType.ERROR,
            timestamp=datetime.now(timezone.utc).isoformat(),
            query_id=query_id or "UNKNOWN",
            engine_id=self.engine_id,
            details={
                "error_type": error_type,
                **(details or {}),
            },
            error=error_msg,
        )

        if query_id and query_id in self.active_traces:
            self.active_traces[query_id].events.append(event)

        logger.error(f"Error recorded: {error_type} | {error_msg}")

    def _write_audit_log(self, trace: QueryTrace):
        """Write query trace to audit log (JSONL format)."""
        try:
            with open(self.audit_log_path, "a", encoding="utf-8") as f:
                trace_dict = asdict(trace)
                json_line = json.dumps(trace_dict, ensure_ascii=False)
                f.write(json_line + "\n")
        except Exception as e:
            logger.error(f"Failed to write audit log: {e}")

    def get_performance_metrics(self) -> PerformanceMetrics:
        """
        Calculate aggregated performance metrics.

        Returns:
            PerformanceMetrics object
        """
        metrics = PerformanceMetrics()

        if not self.completed_traces:
            return metrics

        metrics.total_queries = len(self.completed_traces)

        # Latency metrics
        if self.all_latencies:
            sorted_latencies = sorted(self.all_latencies)
            metrics.avg_latency_ms = round(sum(self.all_latencies) / len(self.all_latencies), 2)
            metrics.min_latency_ms = round(sorted_latencies[0], 2)
            metrics.max_latency_ms = round(sorted_latencies[-1], 2)

            # Percentiles
            p50_idx = int(len(sorted_latencies) * 0.50)
            p95_idx = int(len(sorted_latencies) * 0.95)
            p99_idx = int(len(sorted_latencies) * 0.99)

            metrics.p50_latency_ms = round(sorted_latencies[p50_idx], 2)
            metrics.p95_latency_ms = round(sorted_latencies[p95_idx], 2)
            metrics.p99_latency_ms = round(sorted_latencies[p99_idx], 2)

        # Doctrine hit rate
        queries_with_doctrines = sum(1 for t in self.completed_traces if t.doctrines_triggered)
        metrics.doctrine_hit_rate = round(queries_with_doctrines / metrics.total_queries, 3)

        # Child routing rate
        queries_with_children = sum(1 for t in self.completed_traces if t.children_routed)
        metrics.child_routing_rate = round(queries_with_children / metrics.total_queries, 3)

        # Cloud usage rate
        queries_with_cloud = sum(1 for t in self.completed_traces if t.cloud_results > 0)
        metrics.cloud_usage_rate = round(queries_with_cloud / metrics.total_queries, 3)

        # Error rate
        error_events = sum(1 for t in self.completed_traces for e in t.events if e.event_type == EventType.ERROR)
        metrics.error_rate = round(error_events / metrics.total_queries, 3) if metrics.total_queries > 0 else 0.0

        # Breakdown by mode, zone, practice
        for trace in self.completed_traces:
            metrics.queries_by_mode[trace.mode] += 1
            metrics.queries_by_zone[trace.zone] += 1
            for practice in trace.practice_areas:
                metrics.queries_by_practice[practice] += 1

        return metrics

    def get_trace(self, query_id: str) -> Optional[QueryTrace]:
        """Retrieve a specific query trace."""
        if query_id in self.active_traces:
            return self.active_traces[query_id]

        for trace in self.completed_traces:
            if trace.query_id == query_id:
                return trace

        return None

    def get_recent_traces(self, limit: int = 10) -> List[QueryTrace]:
        """Get the N most recent completed traces."""
        return self.completed_traces[-limit:]

    def clear_completed_traces(self):
        """Clear completed traces (keep audit log)."""
        count = len(self.completed_traces)
        self.completed_traces.clear()
        self.all_latencies.clear()
        logger.info(f"Cleared {count} completed traces")

    def export_metrics(self, output_path: Path):
        """Export performance metrics to JSON file."""
        metrics = self.get_performance_metrics()
        metrics_dict = asdict(metrics)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(metrics_dict, f, indent=2, ensure_ascii=False)

        logger.info(f"Metrics exported to {output_path}")


# ═══════════════════════════════════════════════════════════════════
# DRIFT WATCHER (detects changes in query patterns)
# ═══════════════════════════════════════════════════════════════════

class DriftWatcher:
    """
    Monitors for drift in query patterns, doctrine coverage, and routing behavior.
    """

    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self.recent_queries: List[str] = []
        self.recent_doctrines: List[Set[str]] = []
        self.recent_practices: List[Set[str]] = []

    def observe_query(
        self,
        query: str,
        doctrines_triggered: List[str],
        practice_areas: List[str],
    ):
        """Observe a query and track for drift."""
        self.recent_queries.append(query)
        self.recent_doctrines.append(set(doctrines_triggered))
        self.recent_practices.append(set(practice_areas))

        # Maintain window size
        if len(self.recent_queries) > self.window_size:
            self.recent_queries.pop(0)
            self.recent_doctrines.pop(0)
            self.recent_practices.pop(0)

    def detect_drift(self) -> Dict[str, Any]:
        """
        Detect drift in recent query patterns.

        Returns:
            Dictionary with drift analysis
        """
        if len(self.recent_queries) < self.window_size:
            return {"status": "INSUFFICIENT_DATA", "observed": len(self.recent_queries)}

        # Analyze doctrine diversity
        all_doctrines = set()
        for doc_set in self.recent_doctrines:
            all_doctrines.update(doc_set)

        doctrine_diversity = len(all_doctrines)

        # Analyze practice area diversity
        all_practices = set()
        for prac_set in self.recent_practices:
            all_practices.update(prac_set)

        practice_diversity = len(all_practices)

        # Calculate average doctrines per query
        avg_doctrines = sum(len(d) for d in self.recent_doctrines) / len(self.recent_doctrines)

        # Calculate average practices per query
        avg_practices = sum(len(p) for p in self.recent_practices) / len(self.recent_practices)

        return {
            "status": "ANALYZED",
            "window_size": len(self.recent_queries),
            "doctrine_diversity": doctrine_diversity,
            "practice_diversity": practice_diversity,
            "avg_doctrines_per_query": round(avg_doctrines, 2),
            "avg_practices_per_query": round(avg_practices, 2),
        }


# ═══════════════════════════════════════════════════════════════════
# COVERAGE MAP (tracks which doctrines are triggered)
# ═══════════════════════════════════════════════════════════════════

class CoverageMap:
    """
    Tracks doctrine and practice area coverage to identify gaps.
    """

    def __init__(self, all_doctrines: Set[str], all_practices: Set[str]):
        self.all_doctrines = all_doctrines
        self.all_practices = all_practices
        self.triggered_doctrines: Dict[str, int] = defaultdict(int)
        self.triggered_practices: Dict[str, int] = defaultdict(int)

    def record_trigger(self, doctrines: List[str], practices: List[str]):
        """Record triggered doctrines and practices."""
        for doctrine in doctrines:
            self.triggered_doctrines[doctrine] += 1

        for practice in practices:
            self.triggered_practices[practice] += 1

    def get_coverage_report(self) -> Dict[str, Any]:
        """
        Generate coverage report.

        Returns:
            Dictionary with coverage statistics
        """
        untriggered_doctrines = self.all_doctrines - set(self.triggered_doctrines.keys())
        untriggered_practices = self.all_practices - set(self.triggered_practices.keys())

        doctrine_coverage_rate = len(self.triggered_doctrines) / len(self.all_doctrines) if self.all_doctrines else 0.0
        practice_coverage_rate = len(self.triggered_practices) / len(self.all_practices) if self.all_practices else 0.0

        return {
            "doctrine_coverage": {
                "total": len(self.all_doctrines),
                "triggered": len(self.triggered_doctrines),
                "untriggered": len(untriggered_doctrines),
                "coverage_rate": round(doctrine_coverage_rate, 3),
                "untriggered_list": sorted(untriggered_doctrines),
                "most_triggered": sorted(self.triggered_doctrines.items(), key=lambda x: x[1], reverse=True)[:10],
            },
            "practice_coverage": {
                "total": len(self.all_practices),
                "triggered": len(self.triggered_practices),
                "untriggered": len(untriggered_practices),
                "coverage_rate": round(practice_coverage_rate, 3),
                "untriggered_list": sorted(untriggered_practices),
                "most_triggered": sorted(self.triggered_practices.items(), key=lambda x: x[1], reverse=True)[:10],
            },
        }


# ═══════════════════════════════════════════════════════════════════
# LOGGING
# ═══════════════════════════════════════════════════════════════════

logger.info("LIE telemetry module loaded")
