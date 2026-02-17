"""
P04 Estate Asset Mapper - Telemetry Module
Comprehensive query tracking, performance metrics, and audit logging.
"""

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path
import json
import hashlib
from enum import Enum

from loguru import logger


class QueryType(str, Enum):
    """Estate asset mapping query types."""
    INCLUSION_ANALYSIS = "inclusion_analysis"
    VALUATION = "valuation"
    DISCOUNT_APPLICABILITY = "discount_applicability"
    COMMUNITY_PROPERTY = "community_property"
    RETAINED_INTERESTS = "retained_interests"
    SPECIAL_VALUATION = "special_valuation"
    JOINT_OWNERSHIP = "joint_ownership"
    LIFE_INSURANCE = "life_insurance"
    GENERAL_GUIDANCE = "general_guidance"


class ResponseSource(str, Enum):
    """Source of response."""
    DOCTRINE_CACHE = "doctrine_cache"
    VECTOR_SEARCH = "vector_search"
    DEEP_ANALYSIS = "deep_analysis"
    HYBRID = "hybrid"


@dataclass
class QueryTelemetry:
    """Telemetry data for a single query."""
    query_id: str
    timestamp: str
    query_text: str
    query_type: QueryType
    response_mode: str
    normalized_query: str
    irc_sections_detected: List[str]
    entity_types_detected: List[str]
    property_types_detected: List[str]
    doctrine_blocks_triggered: List[str]
    response_source: ResponseSource
    latency_ms: float
    doctrine_cache_hit: bool
    vector_search_used: bool
    confidence_level: str
    disclosure_required: bool
    fact_fragility_score: float
    response_length_chars: int
    determinism_hash: str
    error_occurred: bool
    error_message: Optional[str] = None


@dataclass
class MetricsSnapshot:
    """Aggregated metrics snapshot."""
    timestamp: str
    total_queries: int
    queries_per_hour: float
    doctrine_cache_hit_rate: float
    avg_latency_ms: float
    p95_latency_ms: float
    p99_latency_ms: float
    error_rate: float
    query_type_distribution: Dict[str, int]
    response_mode_distribution: Dict[str, int]
    confidence_distribution: Dict[str, int]
    avg_fact_fragility: float
    top_triggered_doctrines: List[Dict[str, Any]]


class EstateTelemetryCollector:
    """
    Comprehensive telemetry collector for estate asset mapper engine.
    Tracks queries, performance, doctrine usage, and generates audit trail.
    """

    def __init__(
        self,
        telemetry_file: Path,
        metrics_file: Path,
        audit_trail_file: Path,
        drift_log_file: Path
    ):
        self.telemetry_file = telemetry_file
        self.metrics_file = metrics_file
        self.audit_trail_file = audit_trail_file
        self.drift_log_file = drift_log_file

        # Ensure parent directories exist
        for file_path in [telemetry_file, metrics_file, audit_trail_file, drift_log_file]:
            file_path.parent.mkdir(parents=True, exist_ok=True)

        # In-memory metrics
        self.query_history: List[QueryTelemetry] = []
        self.latency_history: List[float] = []
        self.doctrine_usage_counts: Dict[str, int] = {}
        self.start_time = datetime.now()

    def log_query(
        self,
        query_id: str,
        query_text: str,
        query_type: QueryType,
        response_mode: str,
        normalized_query: str,
        irc_sections: List[str],
        entity_types: List[str],
        property_types: List[str],
        doctrine_blocks: List[str],
        response_source: ResponseSource,
        latency_ms: float,
        cache_hit: bool,
        vector_used: bool,
        confidence: str,
        disclosure: bool,
        fragility: float,
        response_length: int,
        determinism_hash: str,
        error: bool = False,
        error_msg: Optional[str] = None
    ) -> None:
        """Log query telemetry."""
        telemetry = QueryTelemetry(
            query_id=query_id,
            timestamp=datetime.now().isoformat(),
            query_text=query_text,
            query_type=query_type,
            response_mode=response_mode,
            normalized_query=normalized_query,
            irc_sections_detected=irc_sections,
            entity_types_detected=entity_types,
            property_types_detected=property_types,
            doctrine_blocks_triggered=doctrine_blocks,
            response_source=response_source,
            latency_ms=latency_ms,
            doctrine_cache_hit=cache_hit,
            vector_search_used=vector_used,
            confidence_level=confidence,
            disclosure_required=disclosure,
            fact_fragility_score=fragility,
            response_length_chars=response_length,
            determinism_hash=determinism_hash,
            error_occurred=error,
            error_message=error_msg
        )

        # Append to history
        self.query_history.append(telemetry)
        self.latency_history.append(latency_ms)

        # Update doctrine usage counts
        for doctrine in doctrine_blocks:
            self.doctrine_usage_counts[doctrine] = self.doctrine_usage_counts.get(doctrine, 0) + 1

        # Write to JSONL file
        with open(self.telemetry_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(asdict(telemetry)) + '\n')

        logger.info(
            f"Query logged: {query_id} | Type: {query_type.value} | "
            f"Latency: {latency_ms:.1f}ms | Cache: {cache_hit} | "
            f"Confidence: {confidence}"
        )

    def log_audit_entry(
        self,
        query_id: str,
        query_text: str,
        response_text: str,
        doctrine_blocks: List[str],
        authorities_cited: List[str],
        confidence: str,
        disclosure: bool
    ) -> None:
        """Log audit trail entry for forensic review."""
        audit_entry = {
            "query_id": query_id,
            "timestamp": datetime.now().isoformat(),
            "query": query_text,
            "response": response_text,
            "doctrine_blocks": doctrine_blocks,
            "authorities_cited": authorities_cited,
            "confidence_level": confidence,
            "disclosure_required": disclosure
        }

        with open(self.audit_trail_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(audit_entry) + '\n')

    def log_drift_observation(
        self,
        doctrine_topic: str,
        observed_change: str,
        source: str,
        impact: str
    ) -> None:
        """Log potential doctrine drift observation."""
        drift_entry = {
            "timestamp": datetime.now().isoformat(),
            "doctrine_topic": doctrine_topic,
            "observed_change": observed_change,
            "source": source,
            "impact_assessment": impact
        }

        with open(self.drift_log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(drift_entry) + '\n')

        logger.warning(f"Doctrine drift observed: {doctrine_topic} | {observed_change}")

    def generate_metrics_snapshot(self) -> MetricsSnapshot:
        """Generate current metrics snapshot."""
        if not self.query_history:
            return MetricsSnapshot(
                timestamp=datetime.now().isoformat(),
                total_queries=0,
                queries_per_hour=0.0,
                doctrine_cache_hit_rate=0.0,
                avg_latency_ms=0.0,
                p95_latency_ms=0.0,
                p99_latency_ms=0.0,
                error_rate=0.0,
                query_type_distribution={},
                response_mode_distribution={},
                confidence_distribution={},
                avg_fact_fragility=0.0,
                top_triggered_doctrines=[]
            )

        # Calculate metrics
        total_queries = len(self.query_history)
        elapsed_hours = (datetime.now() - self.start_time).total_seconds() / 3600
        queries_per_hour = total_queries / elapsed_hours if elapsed_hours > 0 else 0

        cache_hits = sum(1 for q in self.query_history if q.doctrine_cache_hit)
        cache_hit_rate = cache_hits / total_queries if total_queries > 0 else 0

        avg_latency = sum(self.latency_history) / len(self.latency_history)
        sorted_latencies = sorted(self.latency_history)
        p95_idx = int(len(sorted_latencies) * 0.95)
        p99_idx = int(len(sorted_latencies) * 0.99)
        p95_latency = sorted_latencies[p95_idx] if p95_idx < len(sorted_latencies) else 0
        p99_latency = sorted_latencies[p99_idx] if p99_idx < len(sorted_latencies) else 0

        errors = sum(1 for q in self.query_history if q.error_occurred)
        error_rate = errors / total_queries if total_queries > 0 else 0

        # Query type distribution
        query_type_dist = {}
        for q in self.query_history:
            query_type_dist[q.query_type.value] = query_type_dist.get(q.query_type.value, 0) + 1

        # Response mode distribution
        response_mode_dist = {}
        for q in self.query_history:
            response_mode_dist[q.response_mode] = response_mode_dist.get(q.response_mode, 0) + 1

        # Confidence distribution
        confidence_dist = {}
        for q in self.query_history:
            confidence_dist[q.confidence_level] = confidence_dist.get(q.confidence_level, 0) + 1

        # Average fact fragility
        avg_fragility = sum(q.fact_fragility_score for q in self.query_history) / total_queries

        # Top triggered doctrines
        top_doctrines = [
            {"doctrine": k, "count": v}
            for k, v in sorted(self.doctrine_usage_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        ]

        snapshot = MetricsSnapshot(
            timestamp=datetime.now().isoformat(),
            total_queries=total_queries,
            queries_per_hour=queries_per_hour,
            doctrine_cache_hit_rate=cache_hit_rate,
            avg_latency_ms=avg_latency,
            p95_latency_ms=p95_latency,
            p99_latency_ms=p99_latency,
            error_rate=error_rate,
            query_type_distribution=query_type_dist,
            response_mode_distribution=response_mode_dist,
            confidence_distribution=confidence_dist,
            avg_fact_fragility=avg_fragility,
            top_triggered_doctrines=top_doctrines
        )

        # Write snapshot to metrics file
        with open(self.metrics_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(snapshot), f, indent=2)

        return snapshot

    def get_doctrine_coverage_report(self) -> Dict[str, Any]:
        """Generate doctrine coverage report (triggered vs. missed)."""
        # This would compare doctrine_usage_counts against total doctrine blocks
        # For now, return usage summary
        return {
            "timestamp": datetime.now().isoformat(),
            "total_doctrines_available": 50,  # Update based on actual count
            "doctrines_triggered": len(self.doctrine_usage_counts),
            "usage_distribution": self.doctrine_usage_counts,
            "coverage_percentage": (len(self.doctrine_usage_counts) / 50) * 100
        }

    def compute_determinism_hash(self, query: str, response: str) -> str:
        """Compute SHA-256 determinism hash for query-response pair."""
        combined = f"{query}|||{response}"
        return hashlib.sha256(combined.encode('utf-8')).hexdigest()


# ═══════════════════════════════════════════════════════════════════════════
# MODULE-LEVEL SINGLETON
# ═══════════════════════════════════════════════════════════════════════════

_telemetry_instance = None


def get_telemetry_collector(
    telemetry_file: Optional[Path] = None,
    metrics_file: Optional[Path] = None,
    audit_trail_file: Optional[Path] = None,
    drift_log_file: Optional[Path] = None
) -> EstateTelemetryCollector:
    """Get singleton telemetry collector instance."""
    global _telemetry_instance

    if _telemetry_instance is None:
        # Default paths if not provided
        base_dir = Path(__file__).parent
        telemetry_file = telemetry_file or base_dir / "telemetry.jsonl"
        metrics_file = metrics_file or base_dir / "metrics.json"
        audit_trail_file = audit_trail_file or base_dir / "audit_trail.jsonl"
        drift_log_file = drift_log_file or base_dir / "drift.jsonl"

        _telemetry_instance = EstateTelemetryCollector(
            telemetry_file=telemetry_file,
            metrics_file=metrics_file,
            audit_trail_file=audit_trail_file,
            drift_log_file=drift_log_file
        )

    return _telemetry_instance
