"""
P07 Fiduciary Duty Engine - Telemetry and Monitoring
Comprehensive performance tracking, metrics, and observability
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Dict, List, Optional, Any
from collections import defaultdict, deque
from pathlib import Path
import json
import hashlib
from enum import Enum


class QueryLayer(Enum):
    """Query processing layers"""
    DOCTRINE_CACHE = "doctrine_cache"
    SEMANTIC_RETRIEVAL = "semantic_retrieval"
    DEEP_ANALYSIS = "deep_analysis"


class IssueCategory(Enum):
    """Fiduciary duty issue categories"""
    EXECUTOR_DUTIES = "executor_duties"
    TRUSTEE_DUTIES = "trustee_duties"
    GUARDIAN_DUTIES = "guardian_duties"
    BREACH_ANALYSIS = "breach_analysis"
    SURCHARGE_LIABILITY = "surcharge_liability"
    REMOVAL_GROUNDS = "removal_grounds"
    SELF_DEALING = "self_dealing"
    CONFLICT_INTEREST = "conflict_interest"
    INVESTMENT_PRUDENCE = "investment_prudence"
    ACCOUNTING_DISCLOSURE = "accounting_disclosure"
    CORPORATE_FIDUCIARY = "corporate_fiduciary"
    EXCULPATORY_CLAUSES = "exculpatory_clauses"


@dataclass
class QueryMetrics:
    """Metrics for a single query"""
    query_id: str
    timestamp: str
    query_text: str
    query_hash: str
    layer_used: str
    response_mode: str
    issue_categories: List[str]
    doctrines_triggered: List[str]
    confidence_level: str
    total_latency_ms: float
    cache_latency_ms: float
    retrieval_latency_ms: float
    analysis_latency_ms: float
    response_length: int
    citations_count: int
    cache_hit: bool
    error: Optional[str] = None
    user_context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DriftObservation:
    """Doctrine drift observation"""
    timestamp: str
    doctrine_topic: str
    query_text: str
    expected_conclusion: str
    actual_conclusion: str
    deviation_score: float
    triggering_factors: List[str]


@dataclass
class CoverageGap:
    """Epistemic coverage gap"""
    timestamp: str
    query_text: str
    issue_categories: List[str]
    missing_doctrines: List[str]
    fallback_used: str
    confidence_impact: str


class FiduciaryTelemetry:
    """Comprehensive telemetry system for fiduciary duty engine"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.engine_id = config.get("engine_id", "P07_fiduciary_duty")

        # Metrics storage
        self.query_history: deque = deque(maxlen=10000)
        self.doctrine_hit_counts: Dict[str, int] = defaultdict(int)
        self.category_counts: Dict[str, int] = defaultdict(int)
        self.layer_usage: Dict[str, int] = defaultdict(int)
        self.error_counts: Dict[str, int] = defaultdict(int)

        # Performance tracking
        self.latency_buckets: Dict[str, List[float]] = {
            "doctrine_cache": [],
            "semantic_retrieval": [],
            "deep_analysis": []
        }

        # Drift and coverage tracking
        self.drift_observations: List[DriftObservation] = []
        self.coverage_gaps: List[CoverageGap] = []

        # Audit trail
        self.audit_log_path = Path(f"O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/{self.engine_id}/audit_trail.jsonl")
        self.audit_log_path.parent.mkdir(parents=True, exist_ok=True)

        # Session tracking
        self.session_start = datetime.utcnow()
        self.total_queries = 0
        self.total_errors = 0

    def record_query(self, metrics: QueryMetrics) -> None:
        """Record query metrics"""
        self.query_history.append(metrics)
        self.total_queries += 1

        # Update counters
        self.layer_usage[metrics.layer_used] += 1
        for category in metrics.issue_categories:
            self.category_counts[category] += 1
        for doctrine in metrics.doctrines_triggered:
            self.doctrine_hit_counts[doctrine] += 1

        # Track latencies
        layer_key = metrics.layer_used.lower().replace(" ", "_")
        if layer_key in self.latency_buckets:
            self.latency_buckets[layer_key].append(metrics.total_latency_ms)

        # Track errors
        if metrics.error:
            self.error_counts[metrics.error] += 1
            self.total_errors += 1

        # Write to audit trail
        self._append_audit_log(metrics)

    def record_drift(self, observation: DriftObservation) -> None:
        """Record doctrine drift observation"""
        self.drift_observations.append(observation)

        # Write to separate drift log
        drift_log_path = Path(f"O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/{self.engine_id}/drift_observations.jsonl")
        with drift_log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(observation)) + "\n")

    def record_coverage_gap(self, gap: CoverageGap) -> None:
        """Record epistemic coverage gap"""
        self.coverage_gaps.append(gap)

        # Write to coverage gap log
        gap_log_path = Path(f"O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/{self.engine_id}/coverage_gaps.jsonl")
        with gap_log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(gap)) + "\n")

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics"""
        return {
            "session_duration_seconds": (datetime.utcnow() - self.session_start).total_seconds(),
            "total_queries": self.total_queries,
            "total_errors": self.total_errors,
            "error_rate": self.total_errors / max(self.total_queries, 1),
            "queries_per_minute": self._calculate_qpm(),
            "layer_distribution": dict(self.layer_usage),
            "category_distribution": dict(self.category_counts),
            "average_latencies": self._calculate_avg_latencies(),
            "p95_latencies": self._calculate_p95_latencies(),
            "p99_latencies": self._calculate_p99_latencies(),
            "cache_hit_rate": self._calculate_cache_hit_rate(),
            "top_doctrines": self._get_top_doctrines(10),
            "top_categories": self._get_top_categories(10),
            "recent_errors": self._get_recent_errors(5)
        }

    def get_doctrine_coverage(self) -> Dict[str, Any]:
        """Get doctrine coverage statistics"""
        total_doctrines = len(self.config.get("doctrine_topics", []))
        triggered_doctrines = len(self.doctrine_hit_counts)

        return {
            "total_doctrines": total_doctrines,
            "triggered_doctrines": triggered_doctrines,
            "coverage_percentage": (triggered_doctrines / max(total_doctrines, 1)) * 100,
            "untriggered_doctrines": self._get_untriggered_doctrines(),
            "doctrine_hit_distribution": dict(self.doctrine_hit_counts),
            "coverage_gaps_count": len(self.coverage_gaps),
            "recent_gaps": [asdict(g) for g in self.coverage_gaps[-5:]]
        }

    def get_drift_analysis(self) -> Dict[str, Any]:
        """Get doctrine drift analysis"""
        if not self.drift_observations:
            return {
                "total_observations": 0,
                "average_deviation": 0.0,
                "high_risk_drifts": []
            }

        deviations = [obs.deviation_score for obs in self.drift_observations]
        high_risk = [obs for obs in self.drift_observations if obs.deviation_score > 0.5]

        return {
            "total_observations": len(self.drift_observations),
            "average_deviation": sum(deviations) / len(deviations),
            "max_deviation": max(deviations),
            "high_risk_drifts": [asdict(obs) for obs in high_risk[-5:]],
            "affected_doctrines": list(set(obs.doctrine_topic for obs in self.drift_observations))
        }

    def get_health_status(self) -> Dict[str, Any]:
        """Get overall engine health status"""
        metrics = self.get_performance_metrics()
        coverage = self.get_doctrine_coverage()
        drift = self.get_drift_analysis()

        # Determine health score (0-100)
        health_score = 100

        # Penalize for errors
        if metrics["error_rate"] > 0.05:
            health_score -= 20
        elif metrics["error_rate"] > 0.01:
            health_score -= 10

        # Penalize for low coverage
        if coverage["coverage_percentage"] < 50:
            health_score -= 15
        elif coverage["coverage_percentage"] < 75:
            health_score -= 5

        # Penalize for high drift
        if drift["average_deviation"] > 0.3:
            health_score -= 15
        elif drift["average_deviation"] > 0.1:
            health_score -= 5

        # Penalize for slow performance
        avg_latency = metrics["average_latencies"].get("total", 0)
        if avg_latency > 5000:
            health_score -= 10
        elif avg_latency > 2000:
            health_score -= 5

        health_status = "HEALTHY"
        if health_score < 60:
            health_status = "DEGRADED"
        if health_score < 40:
            health_status = "CRITICAL"

        return {
            "status": health_status,
            "health_score": max(health_score, 0),
            "metrics_summary": metrics,
            "coverage_summary": coverage,
            "drift_summary": drift,
            "recommendations": self._generate_recommendations(metrics, coverage, drift)
        }

    def generate_determinism_hash(self, query: str, response: str) -> str:
        """Generate SHA-256 hash for query/response determinism tracking"""
        combined = f"{query}||{response}"
        return hashlib.sha256(combined.encode()).hexdigest()

    def _append_audit_log(self, metrics: QueryMetrics) -> None:
        """Append query to audit trail"""
        try:
            with self.audit_log_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(asdict(metrics)) + "\n")
        except Exception as e:
            print(f"Failed to write audit log: {e}")

    def _calculate_qpm(self) -> float:
        """Calculate queries per minute"""
        duration_minutes = (datetime.utcnow() - self.session_start).total_seconds() / 60
        return self.total_queries / max(duration_minutes, 0.1)

    def _calculate_avg_latencies(self) -> Dict[str, float]:
        """Calculate average latencies by layer"""
        averages = {}
        for layer, latencies in self.latency_buckets.items():
            if latencies:
                averages[layer] = sum(latencies) / len(latencies)
            else:
                averages[layer] = 0.0

        # Calculate total average
        all_latencies = [m.total_latency_ms for m in self.query_history if m.total_latency_ms]
        averages["total"] = sum(all_latencies) / len(all_latencies) if all_latencies else 0.0

        return averages

    def _calculate_p95_latencies(self) -> Dict[str, float]:
        """Calculate 95th percentile latencies"""
        percentiles = {}
        for layer, latencies in self.latency_buckets.items():
            if latencies:
                sorted_latencies = sorted(latencies)
                p95_index = int(len(sorted_latencies) * 0.95)
                percentiles[layer] = sorted_latencies[p95_index] if p95_index < len(sorted_latencies) else sorted_latencies[-1]
            else:
                percentiles[layer] = 0.0
        return percentiles

    def _calculate_p99_latencies(self) -> Dict[str, float]:
        """Calculate 99th percentile latencies"""
        percentiles = {}
        for layer, latencies in self.latency_buckets.items():
            if latencies:
                sorted_latencies = sorted(latencies)
                p99_index = int(len(sorted_latencies) * 0.99)
                percentiles[layer] = sorted_latencies[p99_index] if p99_index < len(sorted_latencies) else sorted_latencies[-1]
            else:
                percentiles[layer] = 0.0
        return percentiles

    def _calculate_cache_hit_rate(self) -> float:
        """Calculate doctrine cache hit rate"""
        if not self.query_history:
            return 0.0
        cache_hits = sum(1 for m in self.query_history if m.cache_hit)
        return cache_hits / len(self.query_history)

    def _get_top_doctrines(self, n: int) -> List[Dict[str, Any]]:
        """Get top N most-triggered doctrines"""
        sorted_doctrines = sorted(
            self.doctrine_hit_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return [{"doctrine": d, "count": c} for d, c in sorted_doctrines[:n]]

    def _get_top_categories(self, n: int) -> List[Dict[str, Any]]:
        """Get top N most-queried categories"""
        sorted_categories = sorted(
            self.category_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return [{"category": c, "count": cnt} for c, cnt in sorted_categories[:n]]

    def _get_recent_errors(self, n: int) -> List[Dict[str, Any]]:
        """Get recent errors"""
        error_queries = [m for m in self.query_history if m.error][-n:]
        return [
            {
                "timestamp": m.timestamp,
                "query": m.query_text[:100],
                "error": m.error
            }
            for m in error_queries
        ]

    def _get_untriggered_doctrines(self) -> List[str]:
        """Get list of doctrines never triggered"""
        all_doctrines = set(self.config.get("doctrine_topics", []))
        triggered = set(self.doctrine_hit_counts.keys())
        return list(all_doctrines - triggered)

    def _generate_recommendations(
        self,
        metrics: Dict[str, Any],
        coverage: Dict[str, Any],
        drift: Dict[str, Any]
    ) -> List[str]:
        """Generate operational recommendations based on metrics"""
        recommendations = []

        # Error rate recommendations
        if metrics["error_rate"] > 0.05:
            recommendations.append("HIGH ERROR RATE: Investigate recent errors and implement fixes")

        # Coverage recommendations
        if coverage["coverage_percentage"] < 75:
            recommendations.append(
                f"LOW DOCTRINE COVERAGE ({coverage['coverage_percentage']:.1f}%): "
                f"Review and expand untriggered doctrines"
            )

        # Performance recommendations
        avg_latency = metrics["average_latencies"].get("total", 0)
        if avg_latency > 2000:
            recommendations.append(
                f"HIGH LATENCY ({avg_latency:.0f}ms avg): "
                "Optimize doctrine cache or semantic retrieval performance"
            )

        # Drift recommendations
        if drift["average_deviation"] > 0.2:
            recommendations.append(
                f"DOCTRINE DRIFT DETECTED ({drift['average_deviation']:.2f} avg deviation): "
                "Review and update affected doctrines"
            )

        # Coverage gap recommendations
        if len(self.coverage_gaps) > 10:
            recommendations.append(
                f"EPISTEMIC GAPS DETECTED ({len(self.coverage_gaps)} gaps): "
                "Add doctrines for frequently-missed topics"
            )

        if not recommendations:
            recommendations.append("All metrics within healthy ranges")

        return recommendations

    def export_metrics(self, filepath: Path) -> None:
        """Export all metrics to JSON file"""
        export_data = {
            "engine_id": self.engine_id,
            "export_timestamp": datetime.utcnow().isoformat(),
            "session_start": self.session_start.isoformat(),
            "performance": self.get_performance_metrics(),
            "coverage": self.get_doctrine_coverage(),
            "drift": self.get_drift_analysis(),
            "health": self.get_health_status()
        }

        with filepath.open("w", encoding="utf-8") as f:
            json.dump(export_data, f, indent=2)
