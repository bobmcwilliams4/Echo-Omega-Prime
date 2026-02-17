"""
P08 Probate Procedure Engine - Telemetry and Monitoring
Full query tracing, latency tracking, error domain analysis.
"""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum
import json
from pathlib import Path
from collections import defaultdict, Counter
import time


class QueryZone(str, Enum):
    """Position zones for probate queries."""
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"
    UNKNOWN = "UNKNOWN"


class ErrorDomain(str, Enum):
    """Error categorization for probate queries."""
    CACHE_MISS = "CACHE_MISS"
    VECTOR_FAILURE = "VECTOR_FAILURE"
    PARSE_ERROR = "PARSE_ERROR"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    AUTHORITY_CONFLICT = "AUTHORITY_CONFLICT"
    EPISTEMIC_GAP = "EPISTEMIC_GAP"
    INSUFFICIENT_FACTS = "INSUFFICIENT_FACTS"
    MULTI_STATE_AMBIGUITY = "MULTI_STATE_AMBIGUITY"


@dataclass
class QueryTrace:
    """Complete trace record for single query."""
    query_id: str
    timestamp: datetime
    query_text: str
    normalized_query: str
    keywords: List[str]
    entities: Dict[str, List[str]]
    zone: QueryZone
    issue_categories: List[str]

    # Performance metrics
    total_latency_ms: float
    cache_latency_ms: float
    vector_latency_ms: Optional[float]
    synthesis_latency_ms: float

    # Cache results
    cache_hits: int
    cache_blocks_used: List[str]
    confidence_scores: Dict[str, float]

    # Vector results
    vector_used: bool
    vector_results_count: int

    # Response details
    response_mode: str
    response_length: int
    authorities_cited: List[str]
    fragility_score: float
    determinism_hash: str

    # Error tracking
    errors: List[str] = field(default_factory=list)
    error_domains: List[ErrorDomain] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    # Audit trail
    doctrine_coverage: List[str] = field(default_factory=list)
    epistemic_gaps: List[str] = field(default_factory=list)


@dataclass
class DriftObservation:
    """Record of potential doctrine drift."""
    timestamp: datetime
    query: str
    expected_doctrine: str
    observed_pattern: str
    deviation_score: float
    context: Dict[str, Any]


class TelemetryCollector:
    """Collect and analyze probate procedure engine telemetry."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.enabled = config.get("telemetry_enabled", True)
        self.audit_enabled = config.get("audit_trail_enabled", True)

        # Storage paths
        self.base_path = Path(__file__).parent / "telemetry_data"
        self.base_path.mkdir(exist_ok=True)
        self.audit_path = self.base_path / "audit_trail.jsonl"
        self.drift_path = self.base_path / "drift_observations.jsonl"

        # In-memory metrics
        self.query_count = 0
        self.cache_hit_count = 0
        self.cache_miss_count = 0
        self.error_counts: Counter = Counter()
        self.latency_samples: List[float] = []
        self.zone_distribution: Counter = Counter()
        self.issue_category_distribution: Counter = Counter()

        # Drift detection
        self.drift_observations: List[DriftObservation] = []

    def record_query(self, trace: QueryTrace) -> None:
        """Record query trace for analysis."""
        if not self.enabled:
            return

        self.query_count += 1
        self.latency_samples.append(trace.total_latency_ms)
        self.zone_distribution[trace.zone.value] += 1

        for category in trace.issue_categories:
            self.issue_category_distribution[category] += 1

        if trace.cache_hits > 0:
            self.cache_hit_count += 1
        else:
            self.cache_miss_count += 1

        for error_domain in trace.error_domains:
            self.error_counts[error_domain.value] += 1

        # Write to audit trail
        if self.audit_enabled:
            self._append_audit_trail(trace)

    def record_drift(self, observation: DriftObservation) -> None:
        """Record potential doctrine drift observation."""
        self.drift_observations.append(observation)
        self._append_drift_log(observation)

    def get_metrics(self) -> Dict[str, Any]:
        """Retrieve current metrics snapshot."""
        cache_hit_rate = (
            self.cache_hit_count / self.query_count
            if self.query_count > 0 else 0.0
        )

        avg_latency = (
            sum(self.latency_samples) / len(self.latency_samples)
            if self.latency_samples else 0.0
        )

        p95_latency = (
            sorted(self.latency_samples)[int(len(self.latency_samples) * 0.95)]
            if len(self.latency_samples) > 20 else avg_latency
        )

        return {
            "query_count": self.query_count,
            "cache_hit_rate": round(cache_hit_rate, 3),
            "cache_hits": self.cache_hit_count,
            "cache_misses": self.cache_miss_count,
            "avg_latency_ms": round(avg_latency, 2),
            "p95_latency_ms": round(p95_latency, 2),
            "error_counts": dict(self.error_counts),
            "zone_distribution": dict(self.zone_distribution),
            "issue_categories": dict(self.issue_category_distribution.most_common(10)),
            "drift_observations": len(self.drift_observations),
        }

    def get_coverage_map(self) -> Dict[str, Any]:
        """Generate doctrine coverage map from audit trail."""
        if not self.audit_path.exists():
            return {"total_queries": 0, "doctrine_usage": {}}

        doctrine_usage: Counter = Counter()
        total_queries = 0

        with open(self.audit_path, 'r') as f:
            for line in f:
                try:
                    trace_data = json.loads(line)
                    total_queries += 1
                    for block in trace_data.get("cache_blocks_used", []):
                        doctrine_usage[block] += 1
                except json.JSONDecodeError:
                    continue

        return {
            "total_queries": total_queries,
            "doctrine_usage": dict(doctrine_usage.most_common()),
            "unique_doctrines_triggered": len(doctrine_usage),
        }

    def _append_audit_trail(self, trace: QueryTrace) -> None:
        """Append query trace to audit trail."""
        try:
            with open(self.audit_path, 'a') as f:
                trace_dict = asdict(trace)
                # Convert datetime and enums to strings
                trace_dict['timestamp'] = trace.timestamp.isoformat()
                trace_dict['zone'] = trace.zone.value
                trace_dict['error_domains'] = [e.value for e in trace.error_domains]
                f.write(json.dumps(trace_dict) + '\n')
        except Exception:
            # Don't fail on telemetry errors
            pass

    def _append_drift_log(self, observation: DriftObservation) -> None:
        """Append drift observation to drift log."""
        try:
            with open(self.drift_path, 'a') as f:
                obs_dict = {
                    'timestamp': observation.timestamp.isoformat(),
                    'query': observation.query,
                    'expected_doctrine': observation.expected_doctrine,
                    'observed_pattern': observation.observed_pattern,
                    'deviation_score': observation.deviation_score,
                    'context': observation.context,
                }
                f.write(json.dumps(obs_dict) + '\n')
        except Exception:
            pass


class PerformanceTracker:
    """Track performance metrics for optimization."""

    def __init__(self):
        self.timers: Dict[str, float] = {}
        self.start_time: Optional[float] = None

    def start(self, name: str = "main") -> None:
        """Start named timer."""
        self.timers[f"{name}_start"] = time.perf_counter()

    def stop(self, name: str = "main") -> float:
        """Stop named timer and return elapsed milliseconds."""
        start_key = f"{name}_start"
        if start_key not in self.timers:
            return 0.0

        elapsed = (time.perf_counter() - self.timers[start_key]) * 1000
        self.timers[f"{name}_elapsed"] = elapsed
        return elapsed

    def get_elapsed(self, name: str = "main") -> float:
        """Get elapsed time for named timer."""
        return self.timers.get(f"{name}_elapsed", 0.0)

    def get_all_timings(self) -> Dict[str, float]:
        """Get all elapsed timings."""
        return {
            k.replace("_elapsed", ""): v
            for k, v in self.timers.items()
            if k.endswith("_elapsed")
        }


class DriftWatcher:
    """Monitor for doctrine drift over time."""

    def __init__(self, collector: TelemetryCollector):
        self.collector = collector
        self.baseline_patterns: Dict[str, List[str]] = {}

    def record_pattern(self, doctrine: str, response_pattern: str) -> None:
        """Record response pattern for doctrine."""
        if doctrine not in self.baseline_patterns:
            self.baseline_patterns[doctrine] = []
        self.baseline_patterns[doctrine].append(response_pattern)

    def detect_drift(
        self,
        doctrine: str,
        current_response: str,
        threshold: float = 0.3
    ) -> Optional[DriftObservation]:
        """
        Detect if current response drifts from baseline patterns.

        Args:
            doctrine: Doctrine topic
            current_response: Current response text
            threshold: Deviation threshold for drift detection

        Returns:
            DriftObservation if drift detected, None otherwise
        """
        if doctrine not in self.baseline_patterns:
            # No baseline yet, record this as first pattern
            self.record_pattern(doctrine, current_response)
            return None

        # Simple similarity check (could be enhanced with embedding distance)
        baseline = self.baseline_patterns[doctrine][-1]  # Most recent
        deviation = self._calculate_deviation(baseline, current_response)

        if deviation > threshold:
            observation = DriftObservation(
                timestamp=datetime.utcnow(),
                query=current_response[:200],
                expected_doctrine=doctrine,
                observed_pattern=current_response[:500],
                deviation_score=deviation,
                context={"baseline_length": len(baseline), "current_length": len(current_response)}
            )
            self.collector.record_drift(observation)
            return observation

        return None

    def _calculate_deviation(self, baseline: str, current: str) -> float:
        """Calculate simple deviation score between texts."""
        # Simple length-based deviation (could enhance with Levenshtein, embeddings)
        if not baseline:
            return 1.0

        length_ratio = abs(len(current) - len(baseline)) / len(baseline)
        # Normalize to 0-1 range
        return min(length_ratio, 1.0)
