"""
TX08 Passive Activity Loss - Telemetry and Metrics
Query tracing, latency tracking, coverage analysis
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
from datetime import datetime
from pathlib import Path
import json
import hashlib
from collections import defaultdict
from loguru import logger


@dataclass
class QueryTrace:
    """Single query execution trace."""
    query_id: str
    query_text: str
    timestamp: datetime
    response_mode: str
    latency_ms: float
    doctrines_triggered: List[str]
    doctrines_missed: List[str]
    confidence_level: str
    issue_categories: List[str]
    vector_search_used: bool
    error_occurred: bool
    error_message: Optional[str] = None


@dataclass
class DoctrineUsageStats:
    """Usage statistics for a single doctrine block."""
    topic: str
    hit_count: int = 0
    miss_count: int = 0
    last_hit: Optional[datetime] = None
    avg_confidence: float = 0.0
    queries_matched: List[str] = field(default_factory=list)


@dataclass
class CoverageReport:
    """Doctrine coverage and gap analysis."""
    total_doctrines: int
    triggered_doctrines: Set[str]
    never_triggered: Set[str]
    coverage_percentage: float
    top_doctrines: List[tuple]  # (topic, hit_count)
    gap_areas: List[str]


class PassiveActivityTelemetry:
    """Telemetry collector for passive activity engine."""

    def __init__(self, audit_trail_path: Optional[Path] = None):
        self.audit_trail_path = audit_trail_path or Path(__file__).parent / "audit_trail.jsonl"
        self.metrics: Dict[str, any] = {
            "total_queries": 0,
            "queries_by_mode": defaultdict(int),
            "queries_by_category": defaultdict(int),
            "avg_latency_ms": 0.0,
            "vector_search_rate": 0.0,
            "error_rate": 0.0
        }
        self.doctrine_stats: Dict[str, DoctrineUsageStats] = {}
        self.query_traces: List[QueryTrace] = []
        self.drift_observations: List[Dict] = []

    def record_query(self, trace: QueryTrace) -> None:
        """Record a query execution trace."""
        self.query_traces.append(trace)
        self.metrics["total_queries"] += 1
        self.metrics["queries_by_mode"][trace.response_mode] += 1

        for category in trace.issue_categories:
            self.metrics["queries_by_category"][category] += 1

        # Update doctrine usage stats
        for doctrine in trace.doctrines_triggered:
            if doctrine not in self.doctrine_stats:
                self.doctrine_stats[doctrine] = DoctrineUsageStats(topic=doctrine)
            stats = self.doctrine_stats[doctrine]
            stats.hit_count += 1
            stats.last_hit = trace.timestamp
            stats.queries_matched.append(trace.query_text[:100])

        for doctrine in trace.doctrines_missed:
            if doctrine not in self.doctrine_stats:
                self.doctrine_stats[doctrine] = DoctrineUsageStats(topic=doctrine)
            self.doctrine_stats[doctrine].miss_count += 1

        # Update aggregate metrics
        self._update_aggregate_metrics()

        # Append to audit trail
        self._append_audit_trail(trace)

        logger.info(
            f"Query recorded: {trace.query_id} | Mode: {trace.response_mode} | "
            f"Latency: {trace.latency_ms:.1f}ms | Doctrines: {len(trace.doctrines_triggered)}"
        )

    def _update_aggregate_metrics(self) -> None:
        """Update aggregate metrics from query traces."""
        if not self.query_traces:
            return

        total = len(self.query_traces)

        # Average latency
        total_latency = sum(t.latency_ms for t in self.query_traces)
        self.metrics["avg_latency_ms"] = total_latency / total

        # Vector search rate
        vector_count = sum(1 for t in self.query_traces if t.vector_search_used)
        self.metrics["vector_search_rate"] = vector_count / total

        # Error rate
        error_count = sum(1 for t in self.query_traces if t.error_occurred)
        self.metrics["error_rate"] = error_count / total

    def _append_audit_trail(self, trace: QueryTrace) -> None:
        """Append query trace to JSONL audit trail."""
        try:
            audit_entry = {
                "query_id": trace.query_id,
                "timestamp": trace.timestamp.isoformat(),
                "query_text": trace.query_text,
                "response_mode": trace.response_mode,
                "latency_ms": trace.latency_ms,
                "doctrines_triggered": trace.doctrines_triggered,
                "confidence_level": trace.confidence_level,
                "issue_categories": trace.issue_categories,
                "vector_search_used": trace.vector_search_used,
                "error_occurred": trace.error_occurred,
                "error_message": trace.error_message
            }

            with open(self.audit_trail_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(audit_entry) + "\n")
        except Exception as e:
            logger.error(f"Failed to append audit trail: {e}")

    def get_coverage_report(self, all_doctrine_topics: List[str]) -> CoverageReport:
        """
        Generate doctrine coverage report.

        Args:
            all_doctrine_topics: Complete list of doctrine topics in engine

        Returns:
            Coverage report with gap analysis
        """
        triggered = {topic for topic, stats in self.doctrine_stats.items() if stats.hit_count > 0}
        never_triggered = set(all_doctrine_topics) - triggered

        coverage_pct = (len(triggered) / len(all_doctrine_topics) * 100) if all_doctrine_topics else 0.0

        # Top doctrines by hit count
        top_doctrines = sorted(
            [(topic, stats.hit_count) for topic, stats in self.doctrine_stats.items()],
            key=lambda x: x[1],
            reverse=True
        )[:10]

        # Gap areas (never triggered doctrines)
        gap_areas = list(never_triggered)

        report = CoverageReport(
            total_doctrines=len(all_doctrine_topics),
            triggered_doctrines=triggered,
            never_triggered=never_triggered,
            coverage_percentage=coverage_pct,
            top_doctrines=top_doctrines,
            gap_areas=gap_areas
        )

        logger.info(f"Coverage: {coverage_pct:.1f}% ({len(triggered)}/{len(all_doctrine_topics)} doctrines)")

        return report

    def detect_drift(self, query: str, expected_doctrines: List[str], actual_doctrines: List[str]) -> Optional[Dict]:
        """
        Detect doctrine drift (expected vs. actual matches).

        Args:
            query: Query text
            expected_doctrines: Expected doctrine matches
            actual_doctrines: Actual doctrine matches

        Returns:
            Drift observation if detected, None otherwise
        """
        expected_set = set(expected_doctrines)
        actual_set = set(actual_doctrines)

        missing = expected_set - actual_set
        unexpected = actual_set - expected_set

        if missing or unexpected:
            drift = {
                "timestamp": datetime.utcnow().isoformat(),
                "query": query[:200],
                "query_hash": hashlib.sha256(query.encode()).hexdigest()[:16],
                "missing_doctrines": list(missing),
                "unexpected_doctrines": list(unexpected),
                "drift_severity": "HIGH" if len(missing) > 2 else "MEDIUM" if missing else "LOW"
            }

            self.drift_observations.append(drift)
            logger.warning(f"Doctrine drift detected: {drift['drift_severity']} | Missing: {missing} | Unexpected: {unexpected}")
            return drift

        return None

    def get_metrics_summary(self) -> Dict[str, any]:
        """Get current metrics summary."""
        return {
            "total_queries": self.metrics["total_queries"],
            "avg_latency_ms": round(self.metrics["avg_latency_ms"], 2),
            "vector_search_rate": round(self.metrics["vector_search_rate"] * 100, 1),
            "error_rate": round(self.metrics["error_rate"] * 100, 2),
            "queries_by_mode": dict(self.metrics["queries_by_mode"]),
            "queries_by_category": dict(self.metrics["queries_by_category"]),
            "doctrine_hit_count": sum(stats.hit_count for stats in self.doctrine_stats.values()),
            "unique_doctrines_used": len([s for s in self.doctrine_stats.values() if s.hit_count > 0])
        }

    def export_telemetry_report(self, output_path: Path) -> None:
        """Export full telemetry report to JSON."""
        report = {
            "generated_at": datetime.utcnow().isoformat(),
            "metrics": self.get_metrics_summary(),
            "doctrine_stats": {
                topic: {
                    "hit_count": stats.hit_count,
                    "miss_count": stats.miss_count,
                    "last_hit": stats.last_hit.isoformat() if stats.last_hit else None,
                    "sample_queries": stats.queries_matched[:5]
                }
                for topic, stats in self.doctrine_stats.items()
            },
            "drift_observations": self.drift_observations[-50:],  # Last 50
            "recent_queries": [
                {
                    "query_id": t.query_id,
                    "timestamp": t.timestamp.isoformat(),
                    "mode": t.response_mode,
                    "latency_ms": t.latency_ms,
                    "doctrines": len(t.doctrines_triggered)
                }
                for t in self.query_traces[-100:]  # Last 100 queries
            ]
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        logger.info(f"Telemetry report exported: {output_path}")

    def get_latency_percentiles(self) -> Dict[str, float]:
        """Calculate latency percentiles."""
        if not self.query_traces:
            return {}

        latencies = sorted(t.latency_ms for t in self.query_traces)
        n = len(latencies)

        return {
            "p50": latencies[int(n * 0.5)],
            "p90": latencies[int(n * 0.9)],
            "p95": latencies[int(n * 0.95)],
            "p99": latencies[int(n * 0.99)] if n > 100 else latencies[-1],
            "min": latencies[0],
            "max": latencies[-1]
        }

    def get_doctrine_hit_rate(self, topic: str) -> float:
        """Get hit rate for a specific doctrine topic."""
        if topic not in self.doctrine_stats:
            return 0.0

        stats = self.doctrine_stats[topic]
        total = stats.hit_count + stats.miss_count
        return (stats.hit_count / total * 100) if total > 0 else 0.0

    def reset_metrics(self) -> None:
        """Reset all metrics (use cautiously)."""
        self.metrics = {
            "total_queries": 0,
            "queries_by_mode": defaultdict(int),
            "queries_by_category": defaultdict(int),
            "avg_latency_ms": 0.0,
            "vector_search_rate": 0.0,
            "error_rate": 0.0
        }
        self.doctrine_stats = {}
        self.query_traces = []
        self.drift_observations = []
        logger.warning("Telemetry metrics reset")
