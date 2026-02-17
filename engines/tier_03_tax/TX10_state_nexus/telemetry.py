"""
TX10 State Nexus Engine - Telemetry and Metrics
Full query tracing, latency tracking, error domain monitoring
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from enum import Enum
from collections import defaultdict
from pathlib import Path
import json
import time


class QueryPhase(str, Enum):
    NORMALIZATION = "normalization"
    DOCTRINE_CACHE = "doctrine_cache"
    SEMANTIC_SEARCH = "semantic_search"
    VECTOR_SEARCH = "vector_search"
    DEEP_ANALYSIS = "deep_analysis"
    RESPONSE_GENERATION = "response_generation"


class ErrorDomain(str, Enum):
    INPUT_VALIDATION = "input_validation"
    DOCTRINE_MATCHING = "doctrine_matching"
    SEARCH_FAILURE = "search_failure"
    ANALYSIS_ERROR = "analysis_error"
    RESPONSE_GENERATION = "response_generation"
    CLOUD_RETRIEVAL = "cloud_retrieval"
    CONFIGURATION = "configuration"


@dataclass
class QueryTrace:
    """Complete trace of a single query execution"""
    query_id: str
    query_text: str
    timestamp: str
    mode: str
    phases: List[Dict[str, Any]] = field(default_factory=list)
    total_latency_ms: float = 0.0
    doctrines_triggered: List[str] = field(default_factory=list)
    doctrines_missed: List[str] = field(default_factory=list)
    confidence_level: Optional[str] = None
    error_domain: Optional[str] = None
    error_message: Optional[str] = None
    response_length: int = 0
    cache_hit: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class PhaseMetrics:
    """Metrics for a single query phase"""
    phase: str
    start_time: float
    end_time: float
    latency_ms: float
    success: bool
    details: Dict[str, Any] = field(default_factory=dict)


class MetricsCollector:
    """Collect and analyze telemetry data"""

    def __init__(self, audit_trail_path: Optional[Path] = None):
        self.audit_trail_path = audit_trail_path
        self.query_traces: List[QueryTrace] = []
        self.phase_stats: Dict[str, List[float]] = defaultdict(list)
        self.error_counts: Dict[str, int] = defaultdict(int)
        self.doctrine_hit_counts: Dict[str, int] = defaultdict(int)
        self.doctrine_miss_counts: Dict[str, int] = defaultdict(int)
        self.start_time = datetime.now()

    def start_query(self, query_id: str, query_text: str, mode: str) -> QueryTrace:
        """Start tracking a new query"""
        trace = QueryTrace(
            query_id=query_id,
            query_text=query_text,
            timestamp=datetime.now().isoformat(),
            mode=mode
        )
        return trace

    def record_phase(
        self,
        trace: QueryTrace,
        phase: QueryPhase,
        start_time: float,
        end_time: float,
        success: bool,
        details: Optional[Dict[str, Any]] = None
    ):
        """Record metrics for a query phase"""
        latency_ms = (end_time - start_time) * 1000

        phase_metric = PhaseMetrics(
            phase=phase.value,
            start_time=start_time,
            end_time=end_time,
            latency_ms=latency_ms,
            success=success,
            details=details or {}
        )

        trace.phases.append(asdict(phase_metric))
        self.phase_stats[phase.value].append(latency_ms)

    def complete_query(
        self,
        trace: QueryTrace,
        total_latency_ms: float,
        doctrines_triggered: List[str],
        doctrines_missed: List[str],
        confidence_level: Optional[str] = None,
        error_domain: Optional[ErrorDomain] = None,
        error_message: Optional[str] = None,
        response_length: int = 0,
        cache_hit: bool = False
    ):
        """Complete query trace and update aggregate stats"""
        trace.total_latency_ms = total_latency_ms
        trace.doctrines_triggered = doctrines_triggered
        trace.doctrines_missed = doctrines_missed
        trace.confidence_level = confidence_level
        trace.error_domain = error_domain.value if error_domain else None
        trace.error_message = error_message
        trace.response_length = response_length
        trace.cache_hit = cache_hit

        # Update aggregate stats
        for doctrine in doctrines_triggered:
            self.doctrine_hit_counts[doctrine] += 1

        for doctrine in doctrines_missed:
            self.doctrine_miss_counts[doctrine] += 1

        if error_domain:
            self.error_counts[error_domain.value] += 1

        # Store trace
        self.query_traces.append(trace)

        # Write to audit trail
        if self.audit_trail_path:
            self._write_audit_trail(trace)

    def _write_audit_trail(self, trace: QueryTrace):
        """Append trace to JSONL audit trail"""
        try:
            with open(self.audit_trail_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(trace.to_dict()) + '\n')
        except Exception as e:
            # Silently fail audit trail writes (telemetry should not break engine)
            pass

    def get_summary_stats(self) -> Dict[str, Any]:
        """Get summary statistics"""
        total_queries = len(self.query_traces)
        if total_queries == 0:
            return {"error": "No queries recorded"}

        successful_queries = sum(1 for t in self.query_traces if not t.error_domain)
        error_rate = (total_queries - successful_queries) / total_queries

        latencies = [t.total_latency_ms for t in self.query_traces]
        avg_latency = sum(latencies) / len(latencies)
        p50_latency = sorted(latencies)[len(latencies) // 2]
        p95_latency = sorted(latencies)[int(len(latencies) * 0.95)]
        p99_latency = sorted(latencies)[int(len(latencies) * 0.99)]

        cache_hits = sum(1 for t in self.query_traces if t.cache_hit)
        cache_hit_rate = cache_hits / total_queries if total_queries > 0 else 0

        # Phase breakdown
        phase_stats = {}
        for phase, latencies in self.phase_stats.items():
            if latencies:
                phase_stats[phase] = {
                    "count": len(latencies),
                    "avg_ms": sum(latencies) / len(latencies),
                    "p95_ms": sorted(latencies)[int(len(latencies) * 0.95)],
                    "total_ms": sum(latencies)
                }

        # Top triggered doctrines
        top_doctrines = sorted(
            self.doctrine_hit_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]

        # Top missed doctrines (potential gaps)
        top_missed = sorted(
            self.doctrine_miss_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]

        # Error breakdown
        error_breakdown = dict(self.error_counts)

        uptime = (datetime.now() - self.start_time).total_seconds()

        return {
            "summary": {
                "total_queries": total_queries,
                "successful_queries": successful_queries,
                "error_rate": round(error_rate, 4),
                "cache_hit_rate": round(cache_hit_rate, 4),
                "uptime_seconds": round(uptime, 2)
            },
            "latency": {
                "avg_ms": round(avg_latency, 2),
                "p50_ms": round(p50_latency, 2),
                "p95_ms": round(p95_latency, 2),
                "p99_ms": round(p99_latency, 2)
            },
            "phase_breakdown": phase_stats,
            "top_doctrines_triggered": [
                {"doctrine": d, "count": c} for d, c in top_doctrines
            ],
            "top_doctrines_missed": [
                {"doctrine": d, "count": c} for d, c in top_missed
            ],
            "error_breakdown": error_breakdown
        }

    def get_recent_traces(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get most recent query traces"""
        recent = self.query_traces[-limit:]
        return [trace.to_dict() for trace in recent]

    def get_error_traces(self, error_domain: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get traces that resulted in errors"""
        error_traces = [t for t in self.query_traces if t.error_domain]

        if error_domain:
            error_traces = [t for t in error_traces if t.error_domain == error_domain]

        return [trace.to_dict() for trace in error_traces]

    def get_slow_queries(self, threshold_ms: float = 2000) -> List[Dict[str, Any]]:
        """Get queries that exceeded latency threshold"""
        slow = [t for t in self.query_traces if t.total_latency_ms > threshold_ms]
        slow.sort(key=lambda t: t.total_latency_ms, reverse=True)
        return [trace.to_dict() for trace in slow]

    def get_doctrine_coverage(self) -> Dict[str, Any]:
        """Analyze doctrine cache coverage"""
        total_triggered = sum(self.doctrine_hit_counts.values())
        total_missed = sum(self.doctrine_miss_counts.values())
        total_attempts = total_triggered + total_missed

        coverage_rate = total_triggered / total_attempts if total_attempts > 0 else 0

        return {
            "total_triggered": total_triggered,
            "total_missed": total_missed,
            "coverage_rate": round(coverage_rate, 4),
            "unique_doctrines_triggered": len(self.doctrine_hit_counts),
            "unique_doctrines_missed": len(self.doctrine_miss_counts),
            "hit_counts": dict(self.doctrine_hit_counts),
            "miss_counts": dict(self.doctrine_miss_counts)
        }

    def get_confidence_distribution(self) -> Dict[str, int]:
        """Get distribution of confidence levels"""
        distribution = defaultdict(int)
        for trace in self.query_traces:
            if trace.confidence_level:
                distribution[trace.confidence_level] += 1
        return dict(distribution)

    def reset_metrics(self):
        """Reset all collected metrics"""
        self.query_traces.clear()
        self.phase_stats.clear()
        self.error_counts.clear()
        self.doctrine_hit_counts.clear()
        self.doctrine_miss_counts.clear()
        self.start_time = datetime.now()


class DriftWatcher:
    """Monitor doctrine drift over time"""

    def __init__(self):
        self.baseline_stats: Optional[Dict[str, Any]] = None
        self.snapshots: List[Dict[str, Any]] = []

    def set_baseline(self, metrics: MetricsCollector):
        """Set baseline statistics for drift comparison"""
        self.baseline_stats = {
            "timestamp": datetime.now().isoformat(),
            "doctrine_hit_counts": dict(metrics.doctrine_hit_counts),
            "doctrine_miss_counts": dict(metrics.doctrine_miss_counts),
            "error_counts": dict(metrics.error_counts),
            "total_queries": len(metrics.query_traces)
        }

    def take_snapshot(self, metrics: MetricsCollector):
        """Take snapshot for drift analysis"""
        snapshot = {
            "timestamp": datetime.now().isoformat(),
            "doctrine_hit_counts": dict(metrics.doctrine_hit_counts),
            "doctrine_miss_counts": dict(metrics.doctrine_miss_counts),
            "error_counts": dict(metrics.error_counts),
            "total_queries": len(metrics.query_traces)
        }
        self.snapshots.append(snapshot)

    def detect_drift(self, threshold: float = 0.15) -> Dict[str, Any]:
        """Detect significant drift from baseline"""
        if not self.baseline_stats or not self.snapshots:
            return {"error": "Insufficient data for drift detection"}

        latest = self.snapshots[-1]
        drift_detected = False
        drift_details = []

        # Compare doctrine hit rates
        baseline_total = self.baseline_stats["total_queries"]
        latest_total = latest["total_queries"]

        if baseline_total == 0 or latest_total == 0:
            return {"error": "Insufficient queries for comparison"}

        for doctrine in set(list(self.baseline_stats["doctrine_hit_counts"].keys()) +
                           list(latest["doctrine_hit_counts"].keys())):
            baseline_rate = self.baseline_stats["doctrine_hit_counts"].get(doctrine, 0) / baseline_total
            latest_rate = latest["doctrine_hit_counts"].get(doctrine, 0) / latest_total
            drift = abs(latest_rate - baseline_rate)

            if drift > threshold:
                drift_detected = True
                drift_details.append({
                    "doctrine": doctrine,
                    "baseline_rate": round(baseline_rate, 4),
                    "latest_rate": round(latest_rate, 4),
                    "drift": round(drift, 4)
                })

        return {
            "drift_detected": drift_detected,
            "threshold": threshold,
            "drift_details": drift_details,
            "baseline_timestamp": self.baseline_stats["timestamp"],
            "latest_timestamp": latest["timestamp"]
        }


class CoverageMapper:
    """Track triggered and missed doctrines for epistemic gap detection"""

    def __init__(self, all_doctrine_topics: List[str]):
        self.all_doctrine_topics = set(all_doctrine_topics)
        self.triggered_topics: set = set()
        self.missed_topics: set = set()
        self.query_patterns: Dict[str, List[str]] = defaultdict(list)

    def record_query(self, query: str, triggered: List[str], missed: List[str]):
        """Record which doctrines were triggered/missed for a query"""
        self.triggered_topics.update(triggered)
        self.missed_topics.update(missed)

        # Track query patterns
        for topic in triggered:
            self.query_patterns[topic].append(query)

    def get_coverage_report(self) -> Dict[str, Any]:
        """Generate coverage report identifying epistemic gaps"""
        never_triggered = self.all_doctrine_topics - self.triggered_topics
        coverage_rate = len(self.triggered_topics) / len(self.all_doctrine_topics) if self.all_doctrine_topics else 0

        return {
            "total_doctrines": len(self.all_doctrine_topics),
            "triggered_doctrines": len(self.triggered_topics),
            "never_triggered": len(never_triggered),
            "coverage_rate": round(coverage_rate, 4),
            "never_triggered_topics": list(never_triggered),
            "triggered_topics": list(self.triggered_topics),
            "query_patterns": {k: v[:5] for k, v in self.query_patterns.items()}  # Sample queries per doctrine
        }
