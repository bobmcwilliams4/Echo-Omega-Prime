"""
Telemetry Module
R03 Compliance Checker Engine

Performance tracking, metrics collection, and operational monitoring
"""

import time
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict, field
from datetime import datetime
from pathlib import Path
from collections import defaultdict, deque
import hashlib


@dataclass
class QueryTrace:
    """Single query execution trace."""
    query_id: str
    timestamp: str
    query_text: str
    normalized_query: str
    compliance_zone: str
    query_intent: str

    # Execution path
    cache_hit: bool
    doctrine_topic: Optional[str]
    semantic_search_used: bool
    deep_analysis_triggered: bool

    # Timing
    total_latency_ms: float
    cache_lookup_ms: float
    semantic_search_ms: float
    deep_analysis_ms: float

    # Results
    response_mode: str
    confidence: float
    confidence_strata: str
    authorities_cited: List[str]

    # Quality
    word_count: int
    citation_count: int

    # Errors
    error_occurred: bool
    error_message: Optional[str] = None


@dataclass
class MetricsSnapshot:
    """Point-in-time metrics snapshot."""
    timestamp: str
    uptime_seconds: float

    # Query volume
    total_queries: int
    queries_last_hour: int
    queries_last_day: int

    # Performance
    avg_latency_ms: float
    p50_latency_ms: float
    p95_latency_ms: float
    p99_latency_ms: float

    # Cache effectiveness
    cache_hit_rate: float
    cache_hits: int
    cache_misses: int

    # Doctrine coverage
    doctrines_triggered: int
    unique_doctrines_used: int
    total_doctrines: int

    # Error tracking
    error_rate: float
    total_errors: int
    errors_last_hour: int

    # Response modes
    fast_mode_pct: float
    defense_mode_pct: float
    memo_mode_pct: float

    # Confidence distribution
    defensible_pct: float
    aggressive_pct: float
    disclosure_pct: float
    high_risk_pct: float


class TelemetryCollector:
    """
    Collect and track engine performance metrics.

    Implements TIE-20 component: comprehensive query tracing and metrics.
    """

    def __init__(self, config: Dict):
        self.config = config
        self.start_time = time.time()

        # Query traces (keep last 1000)
        self.traces: deque = deque(maxlen=1000)

        # Metrics counters
        self.total_queries = 0
        self.cache_hits = 0
        self.cache_misses = 0
        self.total_errors = 0

        # Latency tracking (milliseconds)
        self.latencies: deque = deque(maxlen=1000)

        # Doctrine usage tracking
        self.doctrine_usage: Dict[str, int] = defaultdict(int)

        # Response mode tracking
        self.response_mode_counts: Dict[str, int] = defaultdict(int)

        # Confidence stratification tracking
        self.confidence_strata_counts: Dict[str, int] = defaultdict(int)

        # Compliance zone tracking
        self.compliance_zone_counts: Dict[str, int] = defaultdict(int)

        # Hourly query tracking
        self.hourly_queries: deque = deque(maxlen=60)  # Last 60 minutes
        self.daily_queries: deque = deque(maxlen=24)   # Last 24 hours

        # Audit trail file
        self.audit_trail_path = Path(config.get("telemetry", {}).get(
            "audit_trail_path",
            "O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/R03_compliance_checker/audit_trail.jsonl"
        ))
        self.audit_trail_path.parent.mkdir(parents=True, exist_ok=True)

    def start_query(self, query_text: str, normalized_query: str, compliance_zone: str, query_intent: str) -> str:
        """
        Start tracking a new query.

        Returns:
            query_id for this trace
        """
        timestamp = datetime.utcnow().isoformat()
        query_id = hashlib.sha256(f"{timestamp}:{query_text}".encode()).hexdigest()[:16]

        # Store initial trace data (will be completed later)
        trace_data = {
            "query_id": query_id,
            "timestamp": timestamp,
            "query_text": query_text,
            "normalized_query": normalized_query,
            "compliance_zone": compliance_zone,
            "query_intent": query_intent,
            "start_time": time.time(),
        }

        # Store in temporary dict for completion later
        if not hasattr(self, '_active_traces'):
            self._active_traces = {}
        self._active_traces[query_id] = trace_data

        self.total_queries += 1
        self.compliance_zone_counts[compliance_zone] += 1

        return query_id

    def complete_query(
        self,
        query_id: str,
        cache_hit: bool,
        doctrine_topic: Optional[str],
        semantic_search_used: bool,
        deep_analysis_triggered: bool,
        response_mode: str,
        confidence: float,
        confidence_strata: str,
        authorities_cited: List[str],
        response_text: str,
        error_occurred: bool = False,
        error_message: Optional[str] = None,
        **timings
    ):
        """
        Complete a query trace with final results.

        Args:
            query_id: Query identifier from start_query
            cache_hit: Whether doctrine cache was hit
            doctrine_topic: Topic of doctrine used (if cache hit)
            semantic_search_used: Whether semantic search was invoked
            deep_analysis_triggered: Whether deep analysis was performed
            response_mode: FAST, DEFENSE, or MEMO
            confidence: Confidence score (0.0-1.0)
            confidence_strata: DEFENSIBLE, AGGRESSIVE, DISCLOSURE, HIGH_RISK
            authorities_cited: List of authorities cited in response
            response_text: Full response text
            error_occurred: Whether an error occurred
            error_message: Error message if error occurred
            **timings: Timing measurements (cache_lookup_ms, semantic_search_ms, etc.)
        """
        if not hasattr(self, '_active_traces') or query_id not in self._active_traces:
            return

        trace_data = self._active_traces.pop(query_id)
        start_time = trace_data.pop("start_time")
        total_latency = (time.time() - start_time) * 1000  # Convert to ms

        # Count words and citations
        word_count = len(response_text.split())
        citation_count = len(authorities_cited)

        # Create complete trace
        trace = QueryTrace(
            **trace_data,
            cache_hit=cache_hit,
            doctrine_topic=doctrine_topic,
            semantic_search_used=semantic_search_used,
            deep_analysis_triggered=deep_analysis_triggered,
            total_latency_ms=total_latency,
            cache_lookup_ms=timings.get("cache_lookup_ms", 0.0),
            semantic_search_ms=timings.get("semantic_search_ms", 0.0),
            deep_analysis_ms=timings.get("deep_analysis_ms", 0.0),
            response_mode=response_mode,
            confidence=confidence,
            confidence_strata=confidence_strata,
            authorities_cited=authorities_cited,
            word_count=word_count,
            citation_count=citation_count,
            error_occurred=error_occurred,
            error_message=error_message,
        )

        # Store trace
        self.traces.append(trace)
        self.latencies.append(total_latency)

        # Update counters
        if cache_hit:
            self.cache_hits += 1
            if doctrine_topic:
                self.doctrine_usage[doctrine_topic] += 1
        else:
            self.cache_misses += 1

        self.response_mode_counts[response_mode] += 1
        self.confidence_strata_counts[confidence_strata] += 1

        if error_occurred:
            self.total_errors += 1

        # Write to audit trail
        if self.config.get("telemetry", {}).get("trace_queries", True):
            self._write_audit_trail(trace)

    def _write_audit_trail(self, trace: QueryTrace):
        """Write query trace to audit trail file (JSONL format)."""
        try:
            with open(self.audit_trail_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(asdict(trace)) + '\n')
        except Exception:
            # Silently fail - don't disrupt engine operation
            pass

    def get_metrics_snapshot(self) -> MetricsSnapshot:
        """
        Get current metrics snapshot.

        Returns:
            MetricsSnapshot with all current metrics
        """
        uptime = time.time() - self.start_time

        # Calculate latency percentiles
        sorted_latencies = sorted(self.latencies) if self.latencies else [0.0]
        n = len(sorted_latencies)
        p50_idx = int(n * 0.50)
        p95_idx = int(n * 0.95)
        p99_idx = int(n * 0.99)

        p50_latency = sorted_latencies[p50_idx] if n > 0 else 0.0
        p95_latency = sorted_latencies[p95_idx] if n > 0 else 0.0
        p99_latency = sorted_latencies[p99_idx] if n > 0 else 0.0
        avg_latency = sum(sorted_latencies) / n if n > 0 else 0.0

        # Cache hit rate
        total_cache_queries = self.cache_hits + self.cache_misses
        cache_hit_rate = self.cache_hits / total_cache_queries if total_cache_queries > 0 else 0.0

        # Error rate
        error_rate = self.total_errors / self.total_queries if self.total_queries > 0 else 0.0

        # Response mode percentages
        total_responses = sum(self.response_mode_counts.values())
        fast_pct = (self.response_mode_counts.get("FAST", 0) / total_responses * 100) if total_responses > 0 else 0.0
        defense_pct = (self.response_mode_counts.get("DEFENSE", 0) / total_responses * 100) if total_responses > 0 else 0.0
        memo_pct = (self.response_mode_counts.get("MEMO", 0) / total_responses * 100) if total_responses > 0 else 0.0

        # Confidence distribution
        total_conf_counts = sum(self.confidence_strata_counts.values())
        defensible_pct = (self.confidence_strata_counts.get("DEFENSIBLE", 0) / total_conf_counts * 100) if total_conf_counts > 0 else 0.0
        aggressive_pct = (self.confidence_strata_counts.get("AGGRESSIVE", 0) / total_conf_counts * 100) if total_conf_counts > 0 else 0.0
        disclosure_pct = (self.confidence_strata_counts.get("DISCLOSURE", 0) / total_conf_counts * 100) if total_conf_counts > 0 else 0.0
        high_risk_pct = (self.confidence_strata_counts.get("HIGH_RISK", 0) / total_conf_counts * 100) if total_conf_counts > 0 else 0.0

        return MetricsSnapshot(
            timestamp=datetime.utcnow().isoformat(),
            uptime_seconds=uptime,
            total_queries=self.total_queries,
            queries_last_hour=0,  # TODO: Implement hourly tracking
            queries_last_day=0,   # TODO: Implement daily tracking
            avg_latency_ms=avg_latency,
            p50_latency_ms=p50_latency,
            p95_latency_ms=p95_latency,
            p99_latency_ms=p99_latency,
            cache_hit_rate=cache_hit_rate,
            cache_hits=self.cache_hits,
            cache_misses=self.cache_misses,
            doctrines_triggered=sum(self.doctrine_usage.values()),
            unique_doctrines_used=len(self.doctrine_usage),
            total_doctrines=self.config.get("doctrine_topics", 52),
            error_rate=error_rate,
            total_errors=self.total_errors,
            errors_last_hour=0,  # TODO: Implement hourly error tracking
            fast_mode_pct=fast_pct,
            defense_mode_pct=defense_pct,
            memo_mode_pct=memo_pct,
            defensible_pct=defensible_pct,
            aggressive_pct=aggressive_pct,
            disclosure_pct=disclosure_pct,
            high_risk_pct=high_risk_pct,
        )

    def get_doctrine_coverage_stats(self) -> Dict[str, Any]:
        """
        Get doctrine coverage statistics.

        Returns:
            Dictionary with doctrine usage statistics
        """
        total_triggers = sum(self.doctrine_usage.values())

        # Sort doctrines by usage
        sorted_doctrines = sorted(
            self.doctrine_usage.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return {
            "total_doctrines": self.config.get("doctrine_topics", 52),
            "doctrines_used": len(self.doctrine_usage),
            "doctrines_unused": self.config.get("doctrine_topics", 52) - len(self.doctrine_usage),
            "coverage_percentage": (len(self.doctrine_usage) / self.config.get("doctrine_topics", 52)) * 100,
            "total_triggers": total_triggers,
            "top_10_doctrines": sorted_doctrines[:10],
            "least_used_doctrines": sorted_doctrines[-10:] if len(sorted_doctrines) > 10 else [],
        }

    def get_compliance_zone_distribution(self) -> Dict[str, int]:
        """Get distribution of queries across compliance zones."""
        return dict(self.compliance_zone_counts)

    def get_recent_errors(self, limit: int = 10) -> List[Dict]:
        """
        Get recent error traces.

        Args:
            limit: Maximum number of errors to return

        Returns:
            List of error trace dictionaries
        """
        error_traces = [
            {
                "query_id": t.query_id,
                "timestamp": t.timestamp,
                "query_text": t.query_text,
                "error_message": t.error_message,
                "compliance_zone": t.compliance_zone,
            }
            for t in reversed(self.traces)
            if t.error_occurred
        ]
        return error_traces[:limit]

    def reset_metrics(self):
        """Reset all metrics (for testing or scheduled resets)."""
        self.traces.clear()
        self.latencies.clear()
        self.total_queries = 0
        self.cache_hits = 0
        self.cache_misses = 0
        self.total_errors = 0
        self.doctrine_usage.clear()
        self.response_mode_counts.clear()
        self.confidence_strata_counts.clear()
        self.compliance_zone_counts.clear()
        self.start_time = time.time()


def get_telemetry_collector(config: Dict) -> TelemetryCollector:
    """Factory function to create telemetry collector instance."""
    return TelemetryCollector(config)
