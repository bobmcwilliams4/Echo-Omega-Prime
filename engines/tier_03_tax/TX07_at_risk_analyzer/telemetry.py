"""
Telemetry module for TX07 at-risk analyzer
Comprehensive query tracing, latency tracking, doctrine coverage, and drift detection
"""

from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field, asdict
from datetime import datetime
from collections import defaultdict
from pathlib import Path
import json
from loguru import logger


@dataclass
class QueryMetrics:
    """Metrics for a single query"""
    query_id: str
    timestamp: str
    query_text: str
    response_mode: str
    total_latency_ms: float
    doctrine_cache_hit: bool
    doctrines_triggered: List[str]
    semantic_search_used: bool
    semantic_latency_ms: Optional[float]
    confidence_level: str
    entity_scope: str
    error_occurred: bool
    error_domain: Optional[str] = None


@dataclass
class DoctrineCoverage:
    """Track which doctrines are used vs. unused"""
    total_doctrines: int
    triggered_doctrines: Set[str] = field(default_factory=set)
    never_triggered: Set[str] = field(default_factory=set)
    trigger_counts: Dict[str, int] = field(default_factory=lambda: defaultdict(int))

    def record_trigger(self, doctrine: str):
        self.triggered_doctrines.add(doctrine)
        self.trigger_counts[doctrine] += 1
        if doctrine in self.never_triggered:
            self.never_triggered.remove(doctrine)

    def coverage_rate(self) -> float:
        if self.total_doctrines == 0:
            return 0.0
        return len(self.triggered_doctrines) / self.total_doctrines


@dataclass
class TelemetryCollector:
    """Comprehensive telemetry for at-risk engine"""
    engine_id: str = "TX07_at_risk_analyzer"
    start_time: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    # Query metrics
    total_queries: int = 0
    queries: List[QueryMetrics] = field(default_factory=list)

    # Latency tracking
    latencies_ms: List[float] = field(default_factory=list)
    doctrine_cache_hits: int = 0
    doctrine_cache_misses: int = 0
    semantic_searches: int = 0

    # Confidence distribution
    confidence_distribution: Dict[str, int] = field(default_factory=lambda: defaultdict(int))

    # Response mode usage
    response_mode_counts: Dict[str, int] = field(default_factory=lambda: defaultdict(int))

    # Error tracking
    errors: List[Dict] = field(default_factory=list)
    error_rate: float = 0.0

    # Doctrine coverage
    doctrine_coverage: Optional[DoctrineCoverage] = None

    # Drift detection
    drift_observations: List[Dict] = field(default_factory=list)

    def record_query(self, metrics: QueryMetrics):
        """Record a query and update aggregate metrics"""
        self.total_queries += 1
        self.queries.append(metrics)
        self.latencies_ms.append(metrics.total_latency_ms)

        if metrics.doctrine_cache_hit:
            self.doctrine_cache_hits += 1
        else:
            self.doctrine_cache_misses += 1

        if metrics.semantic_search_used:
            self.semantic_searches += 1

        self.confidence_distribution[metrics.confidence_level] += 1
        self.response_mode_counts[metrics.response_mode] += 1

        if metrics.error_occurred:
            self.errors.append({
                "query_id": metrics.query_id,
                "error_domain": metrics.error_domain,
                "timestamp": metrics.timestamp
            })

        # Update error rate
        self.error_rate = len(self.errors) / self.total_queries if self.total_queries > 0 else 0.0

        # Update doctrine coverage
        if self.doctrine_coverage:
            for doctrine in metrics.doctrines_triggered:
                self.doctrine_coverage.record_trigger(doctrine)

    def get_latency_stats(self) -> Dict[str, float]:
        """Compute latency statistics"""
        if not self.latencies_ms:
            return {"avg": 0.0, "p50": 0.0, "p95": 0.0, "p99": 0.0}

        sorted_latencies = sorted(self.latencies_ms)
        n = len(sorted_latencies)

        return {
            "avg": sum(sorted_latencies) / n,
            "p50": sorted_latencies[int(n * 0.5)],
            "p95": sorted_latencies[int(n * 0.95)] if n > 1 else sorted_latencies[0],
            "p99": sorted_latencies[int(n * 0.99)] if n > 1 else sorted_latencies[0],
            "min": sorted_latencies[0],
            "max": sorted_latencies[-1]
        }

    def get_cache_hit_rate(self) -> float:
        """Calculate doctrine cache hit rate"""
        total = self.doctrine_cache_hits + self.doctrine_cache_misses
        if total == 0:
            return 0.0
        return self.doctrine_cache_hits / total

    def detect_epistemic_drift(self, query: str, response: str) -> Optional[Dict]:
        """
        Detect potential epistemic drift in responses
        Flags responses that may have drifted from authoritative guidance
        """
        drift_indicators = {
            "overconfidence": ["guaranteed", "always", "never", "certain", "definitely"],
            "speculation": ["might", "could", "possibly", "perhaps", "probably"],
            "missing_authority": len([w for w in response.split() if w.startswith("§")]) == 0,
            "excessive_hedging": response.lower().count("may") > 5,
        }

        drift_score = 0
        flags = []

        for indicator_type, patterns in drift_indicators.items():
            if indicator_type == "missing_authority":
                if patterns:  # missing_authority is a boolean
                    drift_score += 2
                    flags.append("no_statutory_citations")
            elif indicator_type == "excessive_hedging":
                if patterns:  # excessive_hedging is a boolean
                    drift_score += 1
                    flags.append("excessive_hedging")
            else:
                for pattern in patterns:
                    if pattern in response.lower():
                        drift_score += 1
                        flags.append(f"{indicator_type}:{pattern}")

        if drift_score >= 3:
            drift_observation = {
                "timestamp": datetime.utcnow().isoformat(),
                "query": query[:200],
                "drift_score": drift_score,
                "flags": flags,
                "response_snippet": response[:300]
            }
            self.drift_observations.append(drift_observation)
            return drift_observation

        return None

    def export_metrics(self) -> Dict:
        """Export all telemetry as JSON-serializable dict"""
        return {
            "engine_id": self.engine_id,
            "start_time": self.start_time,
            "current_time": datetime.utcnow().isoformat(),
            "total_queries": self.total_queries,
            "latency_stats": self.get_latency_stats(),
            "cache_hit_rate": self.get_cache_hit_rate(),
            "semantic_search_usage": self.semantic_searches,
            "confidence_distribution": dict(self.confidence_distribution),
            "response_mode_usage": dict(self.response_mode_counts),
            "error_rate": self.error_rate,
            "error_count": len(self.errors),
            "doctrine_coverage": {
                "coverage_rate": self.doctrine_coverage.coverage_rate() if self.doctrine_coverage else 0.0,
                "triggered_count": len(self.doctrine_coverage.triggered_doctrines) if self.doctrine_coverage else 0,
                "never_triggered_count": len(self.doctrine_coverage.never_triggered) if self.doctrine_coverage else 0,
            } if self.doctrine_coverage else {},
            "drift_observations_count": len(self.drift_observations),
        }

    def save_audit_trail(self, output_dir: Path):
        """Save detailed audit trail to JSONL file"""
        output_dir.mkdir(parents=True, exist_ok=True)
        audit_file = output_dir / f"audit_trail_{datetime.utcnow().strftime('%Y%m%d')}.jsonl"

        with open(audit_file, 'a', encoding='utf-8') as f:
            for query_metrics in self.queries:
                f.write(json.dumps(asdict(query_metrics)) + '\n')

        logger.info(f"Audit trail saved to {audit_file}")


class DriftWatcher:
    """Monitor for doctrine drift over time"""

    def __init__(self, baseline_file: Optional[Path] = None):
        self.baseline_file = baseline_file
        self.baseline_responses: Dict[str, str] = {}
        if baseline_file and baseline_file.exists():
            self._load_baseline()

    def _load_baseline(self):
        """Load baseline responses from file"""
        with open(self.baseline_file, 'r', encoding='utf-8') as f:
            self.baseline_responses = json.load(f)

    def compare_to_baseline(self, query: str, current_response: str) -> Optional[Dict]:
        """Compare current response to baseline for drift detection"""
        baseline = self.baseline_responses.get(query)
        if not baseline:
            return None

        # Simple diff metrics
        baseline_length = len(baseline)
        current_length = len(current_response)
        length_diff_pct = abs(current_length - baseline_length) / baseline_length * 100

        # Authority citation changes
        baseline_cites = set([w for w in baseline.split() if w.startswith("§")])
        current_cites = set([w for w in current_response.split() if w.startswith("§")])
        citation_drift = len(baseline_cites.symmetric_difference(current_cites))

        if length_diff_pct > 20 or citation_drift > 2:
            return {
                "query": query,
                "length_diff_pct": length_diff_pct,
                "citation_drift_count": citation_drift,
                "baseline_citations": list(baseline_cites),
                "current_citations": list(current_cites),
            }

        return None
