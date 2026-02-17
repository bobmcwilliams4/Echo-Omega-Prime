"""
TX01 IRC Parser Engine - Telemetry Module
Comprehensive query tracking, latency monitoring, and audit trail
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
import json
import hashlib
from collections import defaultdict
from loguru import logger


@dataclass
class QueryTelemetry:
    """Telemetry data for a single query"""
    query_id: str
    timestamp: str
    query_text: str
    response_mode: str
    analysis_zone: str
    doctrines_triggered: List[str] = field(default_factory=list)
    cache_hit: bool = False
    latency_ms: float = 0.0
    citations_extracted: List[str] = field(default_factory=list)
    cross_references_found: List[str] = field(default_factory=list)
    confidence_level: Optional[str] = None
    error: Optional[str] = None
    response_length: int = 0
    determinism_hash: Optional[str] = None


@dataclass
class MetricsSnapshot:
    """Aggregated metrics snapshot"""
    timestamp: str
    total_queries: int
    cache_hit_rate: float
    avg_latency_ms: float
    error_rate: float
    doctrines_by_frequency: Dict[str, int]
    queries_per_mode: Dict[str, int]
    queries_per_zone: Dict[str, int]


class TelemetryCollector:
    """Collect and analyze telemetry data"""

    def __init__(self, engine_id: str, audit_dir: Optional[Path] = None):
        self.engine_id = engine_id
        self.audit_dir = audit_dir or Path(__file__).parent / "audit_logs"
        self.audit_dir.mkdir(exist_ok=True)

        self.query_log_path = self.audit_dir / f"{engine_id}_queries.jsonl"
        self.metrics_log_path = self.audit_dir / f"{engine_id}_metrics.jsonl"

        # In-memory metrics
        self.queries_processed = 0
        self.total_latency_ms = 0.0
        self.cache_hits = 0
        self.errors = 0
        self.doctrine_frequency = defaultdict(int)
        self.mode_frequency = defaultdict(int)
        self.zone_frequency = defaultdict(int)
        self.recent_queries: List[QueryTelemetry] = []
        self.max_recent = 100

        logger.info(f"Telemetry collector initialized for {engine_id}")

    def log_query(self, telemetry: QueryTelemetry) -> None:
        """Log query telemetry to JSONL audit trail"""
        # Update in-memory metrics
        self.queries_processed += 1
        self.total_latency_ms += telemetry.latency_ms

        if telemetry.cache_hit:
            self.cache_hits += 1

        if telemetry.error:
            self.errors += 1

        for doctrine in telemetry.doctrines_triggered:
            self.doctrine_frequency[doctrine] += 1

        self.mode_frequency[telemetry.response_mode] += 1
        self.zone_frequency[telemetry.analysis_zone] += 1

        # Add to recent queries
        self.recent_queries.append(telemetry)
        if len(self.recent_queries) > self.max_recent:
            self.recent_queries.pop(0)

        # Write to audit log
        try:
            with open(self.query_log_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(asdict(telemetry)) + '\n')
        except Exception as e:
            logger.error(f"Failed to write query telemetry: {e}")

    def generate_metrics_snapshot(self) -> MetricsSnapshot:
        """Generate current metrics snapshot"""
        snapshot = MetricsSnapshot(
            timestamp=datetime.utcnow().isoformat(),
            total_queries=self.queries_processed,
            cache_hit_rate=self.cache_hits / self.queries_processed if self.queries_processed > 0 else 0.0,
            avg_latency_ms=self.total_latency_ms / self.queries_processed if self.queries_processed > 0 else 0.0,
            error_rate=self.errors / self.queries_processed if self.queries_processed > 0 else 0.0,
            doctrines_by_frequency=dict(self.doctrine_frequency),
            queries_per_mode=dict(self.mode_frequency),
            queries_per_zone=dict(self.zone_frequency)
        )

        # Write snapshot to metrics log
        try:
            with open(self.metrics_log_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(asdict(snapshot)) + '\n')
        except Exception as e:
            logger.error(f"Failed to write metrics snapshot: {e}")

        return snapshot

    def get_doctrine_coverage(self, total_doctrines: int) -> Dict[str, Any]:
        """Calculate doctrine coverage statistics"""
        triggered = len(self.doctrine_frequency)
        missed = total_doctrines - triggered

        return {
            "total_doctrines": total_doctrines,
            "triggered_doctrines": triggered,
            "missed_doctrines": missed,
            "coverage_rate": triggered / total_doctrines if total_doctrines > 0 else 0.0,
            "top_doctrines": sorted(
                self.doctrine_frequency.items(),
                key=lambda x: x[1],
                reverse=True
            )[:10]
        }

    def get_latency_stats(self) -> Dict[str, float]:
        """Calculate latency statistics from recent queries"""
        if not self.recent_queries:
            return {"min": 0.0, "max": 0.0, "avg": 0.0, "p50": 0.0, "p95": 0.0, "p99": 0.0}

        latencies = sorted([q.latency_ms for q in self.recent_queries])
        n = len(latencies)

        return {
            "min": latencies[0],
            "max": latencies[-1],
            "avg": sum(latencies) / n,
            "p50": latencies[int(n * 0.50)],
            "p95": latencies[int(n * 0.95)] if n > 20 else latencies[-1],
            "p99": latencies[int(n * 0.99)] if n > 100 else latencies[-1]
        }

    def get_error_domains(self) -> Dict[str, int]:
        """Categorize errors by domain"""
        error_domains = defaultdict(int)

        for query in self.recent_queries:
            if query.error:
                # Simple error categorization
                if "parse" in query.error.lower():
                    error_domains["parsing"] += 1
                elif "citation" in query.error.lower():
                    error_domains["citation"] += 1
                elif "doctrine" in query.error.lower():
                    error_domains["doctrine"] += 1
                elif "timeout" in query.error.lower():
                    error_domains["timeout"] += 1
                else:
                    error_domains["other"] += 1

        return dict(error_domains)

    def detect_drift(self, baseline_metrics: Optional[MetricsSnapshot] = None) -> Dict[str, Any]:
        """Detect drift in doctrine usage or performance"""
        current = self.generate_metrics_snapshot()

        if not baseline_metrics:
            return {"drift_detected": False, "message": "No baseline for comparison"}

        drift_signals = {}

        # Latency drift
        latency_change = (current.avg_latency_ms - baseline_metrics.avg_latency_ms) / baseline_metrics.avg_latency_ms if baseline_metrics.avg_latency_ms > 0 else 0
        if abs(latency_change) > 0.2:  # 20% change
            drift_signals["latency"] = {
                "baseline": baseline_metrics.avg_latency_ms,
                "current": current.avg_latency_ms,
                "change_pct": latency_change * 100
            }

        # Error rate drift
        error_change = current.error_rate - baseline_metrics.error_rate
        if abs(error_change) > 0.05:  # 5 percentage points
            drift_signals["error_rate"] = {
                "baseline": baseline_metrics.error_rate,
                "current": current.error_rate,
                "change": error_change
            }

        # Doctrine usage drift (new doctrines heavily used or old ones unused)
        baseline_doctrines = set(baseline_metrics.doctrines_by_frequency.keys())
        current_doctrines = set(current.doctrines_by_frequency.keys())

        new_doctrines = current_doctrines - baseline_doctrines
        disappeared_doctrines = baseline_doctrines - current_doctrines

        if new_doctrines or disappeared_doctrines:
            drift_signals["doctrine_usage"] = {
                "new_doctrines": list(new_doctrines),
                "disappeared_doctrines": list(disappeared_doctrines)
            }

        return {
            "drift_detected": len(drift_signals) > 0,
            "signals": drift_signals,
            "timestamp": current.timestamp
        }

    def compute_determinism_hash(self, query: str, response: str) -> str:
        """Compute SHA-256 hash for determinism verification"""
        combined = f"{query}||{response}"
        return hashlib.sha256(combined.encode('utf-8')).hexdigest()

    def get_health_status(self) -> Dict[str, Any]:
        """Generate health status report"""
        snapshot = self.generate_metrics_snapshot()
        latency_stats = self.get_latency_stats()
        error_domains = self.get_error_domains()

        health_score = 100.0
        issues = []

        # Deduct for high error rate
        if snapshot.error_rate > 0.05:
            health_score -= 20
            issues.append(f"High error rate: {snapshot.error_rate:.2%}")

        # Deduct for high latency
        if latency_stats["p95"] > 500:
            health_score -= 15
            issues.append(f"High P95 latency: {latency_stats['p95']:.0f}ms")

        # Deduct for low cache hit rate
        if snapshot.cache_hit_rate < 0.3:
            health_score -= 10
            issues.append(f"Low cache hit rate: {snapshot.cache_hit_rate:.2%}")

        return {
            "health_score": max(0, health_score),
            "status": "healthy" if health_score >= 80 else "degraded" if health_score >= 50 else "unhealthy",
            "total_queries": snapshot.total_queries,
            "cache_hit_rate": snapshot.cache_hit_rate,
            "avg_latency_ms": snapshot.avg_latency_ms,
            "error_rate": snapshot.error_rate,
            "latency_stats": latency_stats,
            "error_domains": error_domains,
            "issues": issues,
            "timestamp": snapshot.timestamp
        }


class DriftWatcher:
    """Monitor doctrine drift over time"""

    def __init__(self, telemetry: TelemetryCollector, check_interval_hours: int = 24):
        self.telemetry = telemetry
        self.check_interval_hours = check_interval_hours
        self.baseline_snapshot: Optional[MetricsSnapshot] = None
        self.last_check: Optional[datetime] = None

    def set_baseline(self) -> None:
        """Set current metrics as baseline for drift detection"""
        self.baseline_snapshot = self.telemetry.generate_metrics_snapshot()
        self.last_check = datetime.utcnow()
        logger.info(f"Drift baseline set at {self.baseline_snapshot.timestamp}")

    def check_drift(self) -> Dict[str, Any]:
        """Check for drift against baseline"""
        if not self.baseline_snapshot:
            self.set_baseline()
            return {"message": "Baseline set, no drift to report yet"}

        return self.telemetry.detect_drift(self.baseline_snapshot)

    def should_check(self) -> bool:
        """Determine if drift check is due"""
        if not self.last_check:
            return True

        hours_since_check = (datetime.utcnow() - self.last_check).total_seconds() / 3600
        return hours_since_check >= self.check_interval_hours
