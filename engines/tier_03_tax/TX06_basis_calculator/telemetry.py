"""
TX06 Basis Calculator - Telemetry Module
Performance tracking, audit trail, and drift detection
"""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path
import json
import hashlib
from collections import defaultdict
from loguru import logger


@dataclass
class QueryMetrics:
    """Metrics for a single query"""
    query_id: str
    timestamp: datetime
    query_text: str
    basis_type: str
    entity_type: str
    response_mode: str

    # Performance
    total_latency_ms: float
    cache_hit: bool
    cache_latency_ms: float
    vector_search_latency_ms: float
    deep_analysis_latency_ms: float

    # Quality
    doctrines_triggered: List[str]
    confidence_level: str
    determinism_hash: str

    # Errors
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


@dataclass
class DriftObservation:
    """Doctrine drift observation"""
    timestamp: datetime
    doctrine_topic: str
    query_text: str
    expected_conclusion: str
    actual_conclusion: str
    deviation_score: float
    irc_sections: List[str]


class TelemetryCollector:
    """Collect and analyze engine telemetry"""

    def __init__(self, engine_id: str = "TX06_basis_calculator"):
        self.engine_id = engine_id
        self.log_dir = Path(__file__).parent / "logs"
        self.log_dir.mkdir(exist_ok=True)

        self.audit_trail_path = self.log_dir / "audit_trail.jsonl"
        self.metrics_path = self.log_dir / "metrics.json"
        self.drift_path = self.log_dir / "drift_observations.jsonl"

        self.session_metrics: List[QueryMetrics] = []
        self.drift_observations: List[DriftObservation] = []

        # In-memory counters
        self.doctrine_hit_counts: Dict[str, int] = defaultdict(int)
        self.doctrine_miss_counts: Dict[str, int] = defaultdict(int)
        self.error_counts: Dict[str, int] = defaultdict(int)
        self.total_queries = 0
        self.cache_hits = 0

    def record_query(self, metrics: QueryMetrics) -> None:
        """Record query metrics"""
        self.session_metrics.append(metrics)
        self.total_queries += 1

        if metrics.cache_hit:
            self.cache_hits += 1

        # Update doctrine counters
        for doctrine in metrics.doctrines_triggered:
            self.doctrine_hit_counts[doctrine] += 1

        # Track errors
        for error in metrics.errors:
            self.error_counts[error] += 1

        # Append to audit trail
        self._append_audit_trail(metrics)

    def _append_audit_trail(self, metrics: QueryMetrics) -> None:
        """Append query to audit trail (JSONL)"""
        try:
            with open(self.audit_trail_path, 'a', encoding='utf-8') as f:
                record = asdict(metrics)
                record['timestamp'] = metrics.timestamp.isoformat()
                f.write(json.dumps(record) + '\n')
        except Exception as e:
            logger.error(f"Failed to write audit trail: {e}")

    def record_drift(self, observation: DriftObservation) -> None:
        """Record doctrine drift observation"""
        self.drift_observations.append(observation)

        try:
            with open(self.drift_path, 'a', encoding='utf-8') as f:
                record = asdict(observation)
                record['timestamp'] = observation.timestamp.isoformat()
                f.write(json.dumps(record) + '\n')
        except Exception as e:
            logger.error(f"Failed to write drift observation: {e}")

    def get_performance_stats(self) -> Dict[str, Any]:
        """Calculate performance statistics"""
        if not self.session_metrics:
            return {}

        latencies = [m.total_latency_ms for m in self.session_metrics]
        cache_latencies = [
            m.cache_latency_ms
            for m in self.session_metrics
            if m.cache_hit
        ]

        return {
            "total_queries": self.total_queries,
            "cache_hit_rate": self.cache_hits / max(self.total_queries, 1),
            "avg_latency_ms": sum(latencies) / len(latencies),
            "p50_latency_ms": self._percentile(latencies, 50),
            "p95_latency_ms": self._percentile(latencies, 95),
            "p99_latency_ms": self._percentile(latencies, 99),
            "avg_cache_latency_ms": (
                sum(cache_latencies) / len(cache_latencies)
                if cache_latencies else 0
            ),
            "error_rate": sum(self.error_counts.values()) / max(self.total_queries, 1),
        }

    def get_coverage_map(self) -> Dict[str, Any]:
        """Generate doctrine coverage map"""
        total_hits = sum(self.doctrine_hit_counts.values())

        coverage = {
            "total_doctrines_available": len(self.doctrine_hit_counts) + len(self.doctrine_miss_counts),
            "doctrines_triggered": len(self.doctrine_hit_counts),
            "coverage_percentage": (
                len(self.doctrine_hit_counts) /
                max(len(self.doctrine_hit_counts) + len(self.doctrine_miss_counts), 1) * 100
            ),
            "doctrine_hits": dict(self.doctrine_hit_counts),
            "top_doctrines": sorted(
                self.doctrine_hit_counts.items(),
                key=lambda x: x[1],
                reverse=True
            )[:10],
            "unused_doctrines": list(self.doctrine_miss_counts.keys()),
        }

        return coverage

    def get_drift_summary(self) -> Dict[str, Any]:
        """Summarize doctrine drift observations"""
        if not self.drift_observations:
            return {"drift_detected": False}

        drift_by_doctrine = defaultdict(list)
        for obs in self.drift_observations:
            drift_by_doctrine[obs.doctrine_topic].append(obs.deviation_score)

        return {
            "drift_detected": True,
            "total_observations": len(self.drift_observations),
            "affected_doctrines": len(drift_by_doctrine),
            "avg_deviation_score": sum(
                obs.deviation_score for obs in self.drift_observations
            ) / len(self.drift_observations),
            "drift_by_doctrine": {
                topic: {
                    "count": len(scores),
                    "avg_deviation": sum(scores) / len(scores),
                    "max_deviation": max(scores)
                }
                for topic, scores in drift_by_doctrine.items()
            },
        }

    def get_error_breakdown(self) -> Dict[str, int]:
        """Get error counts by type"""
        return dict(self.error_counts)

    def export_metrics(self) -> None:
        """Export metrics to JSON file"""
        metrics = {
            "engine_id": self.engine_id,
            "export_timestamp": datetime.now().isoformat(),
            "performance": self.get_performance_stats(),
            "coverage": self.get_coverage_map(),
            "drift": self.get_drift_summary(),
            "errors": self.get_error_breakdown(),
        }

        try:
            with open(self.metrics_path, 'w', encoding='utf-8') as f:
                json.dump(metrics, f, indent=2)
            logger.info(f"Metrics exported to {self.metrics_path}")
        except Exception as e:
            logger.error(f"Failed to export metrics: {e}")

    @staticmethod
    def _percentile(data: List[float], percentile: int) -> float:
        """Calculate percentile"""
        if not data:
            return 0.0
        sorted_data = sorted(data)
        index = int(len(sorted_data) * percentile / 100)
        return sorted_data[min(index, len(sorted_data) - 1)]

    def generate_determinism_hash(
        self,
        query: str,
        response: str,
        doctrines_used: List[str]
    ) -> str:
        """Generate SHA-256 hash for response determinism verification"""
        content = f"{query}|{response}|{','.join(sorted(doctrines_used))}"
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def verify_determinism(
        self,
        query: str,
        response: str,
        doctrines_used: List[str],
        expected_hash: str
    ) -> bool:
        """Verify response determinism against expected hash"""
        actual_hash = self.generate_determinism_hash(query, response, doctrines_used)
        return actual_hash == expected_hash

    def get_health_metrics(self) -> Dict[str, Any]:
        """Health check metrics for monitoring"""
        perf = self.get_performance_stats()
        coverage = self.get_coverage_map()
        drift = self.get_drift_summary()

        # Determine health status
        health_score = 100.0
        issues = []

        # Performance degradation
        if perf.get("avg_latency_ms", 0) > 1000:
            health_score -= 20
            issues.append("High latency detected")

        # Low cache hit rate
        if perf.get("cache_hit_rate", 0) < 0.5:
            health_score -= 15
            issues.append("Low cache hit rate")

        # High error rate
        if perf.get("error_rate", 0) > 0.05:
            health_score -= 25
            issues.append("Elevated error rate")

        # Drift detected
        if drift.get("drift_detected"):
            health_score -= 20
            issues.append("Doctrine drift detected")

        # Low coverage
        if coverage.get("coverage_percentage", 0) < 30:
            health_score -= 10
            issues.append("Low doctrine coverage")

        return {
            "health_score": max(health_score, 0),
            "status": "healthy" if health_score >= 80 else "degraded" if health_score >= 50 else "unhealthy",
            "issues": issues,
            "performance": perf,
            "coverage_pct": coverage.get("coverage_percentage", 0),
            "drift_observations": drift.get("total_observations", 0),
        }
