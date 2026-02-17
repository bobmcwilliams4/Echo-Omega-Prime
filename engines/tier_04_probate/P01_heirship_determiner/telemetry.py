"""
P01 Heirship Determiner — Telemetry & Monitoring
Query tracing, latency tracking, error domains, drift detection
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from pathlib import Path
import json
from enum import Enum
from collections import defaultdict, deque
import hashlib


class ErrorDomain(str, Enum):
    """Categorize errors by domain"""
    DOCTRINE_RETRIEVAL = "doctrine_retrieval"
    CLOUD_CONNECTION = "cloud_connection"
    SEMANTIC_ANALYSIS = "semantic_analysis"
    AUTHORITY_RESOLUTION = "authority_resolution"
    VALIDATION = "validation"
    RESPONSE_GENERATION = "response_generation"
    UNKNOWN = "unknown"


class QueryZone(str, Enum):
    """Position zones for analysis"""
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"
    UNKNOWN = "UNKNOWN"


@dataclass
class QueryTrace:
    """Complete trace of a single query execution"""
    query_id: str
    timestamp: str
    query_text: str
    zone: QueryZone
    response_mode: str

    # Timing
    total_latency_ms: float
    doctrine_cache_latency_ms: float
    semantic_search_latency_ms: float
    cloud_retrieval_latency_ms: float
    response_generation_latency_ms: float

    # Cache performance
    cache_hit: bool
    doctrines_triggered: List[str]
    doctrines_missed: List[str]

    # Confidence
    final_confidence: str
    confidence_score: float

    # Response metadata
    response_length: int
    citations_count: int

    # Errors
    errors: List[Dict[str, Any]] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    # Determinism
    determinism_hash: str = ""


@dataclass
class MetricsSnapshot:
    """Point-in-time metrics snapshot"""
    timestamp: str
    queries_total: int
    queries_per_hour: float
    avg_latency_ms: float
    p95_latency_ms: float
    p99_latency_ms: float
    cache_hit_rate: float
    error_rate: float
    errors_by_domain: Dict[ErrorDomain, int]
    top_doctrines: List[tuple[str, int]]  # (doctrine_name, trigger_count)


class TelemetryCollector:
    """Centralized telemetry collection and analysis"""

    def __init__(self, audit_log_path: Optional[Path] = None):
        self.audit_log_path = audit_log_path or Path("audit_trail.jsonl")
        self.query_traces: deque = deque(maxlen=1000)  # Keep last 1000 queries in memory

        # Real-time counters
        self.total_queries = 0
        self.cache_hits = 0
        self.cache_misses = 0
        self.errors_by_domain: Dict[ErrorDomain, int] = defaultdict(int)
        self.doctrine_trigger_counts: Dict[str, int] = defaultdict(int)
        self.latency_samples: deque = deque(maxlen=1000)

        # Drift detection
        self.doctrine_coverage: Dict[str, List[str]] = defaultdict(list)  # doctrine -> [query_ids]
        self.untriggered_doctrines: set = set()

    def record_query(self, trace: QueryTrace):
        """Record a query trace"""
        self.total_queries += 1
        self.query_traces.append(trace)
        self.latency_samples.append(trace.total_latency_ms)

        # Cache metrics
        if trace.cache_hit:
            self.cache_hits += 1
        else:
            self.cache_misses += 1

        # Doctrine coverage
        for doctrine in trace.doctrines_triggered:
            self.doctrine_trigger_counts[doctrine] += 1
            self.doctrine_coverage[doctrine].append(trace.query_id)

        # Error tracking
        for error in trace.errors:
            domain = ErrorDomain(error.get('domain', 'unknown'))
            self.errors_by_domain[domain] += 1

        # Append to audit log
        self._append_to_audit_log(trace)

    def _append_to_audit_log(self, trace: QueryTrace):
        """Append trace to JSONL audit trail"""
        try:
            with self.audit_log_path.open('a', encoding='utf-8') as f:
                f.write(json.dumps(asdict(trace)) + '\n')
        except Exception:
            pass  # Silent fail for audit logging

    def get_current_metrics(self) -> MetricsSnapshot:
        """Generate current metrics snapshot"""
        now = datetime.utcnow()

        # Calculate queries per hour
        hour_ago = now - timedelta(hours=1)
        recent_queries = [
            t for t in self.query_traces
            if datetime.fromisoformat(t.timestamp) > hour_ago
        ]
        queries_per_hour = len(recent_queries)

        # Latency percentiles
        sorted_latencies = sorted(self.latency_samples)
        p95_idx = int(len(sorted_latencies) * 0.95)
        p99_idx = int(len(sorted_latencies) * 0.99)

        avg_latency = sum(sorted_latencies) / len(sorted_latencies) if sorted_latencies else 0
        p95_latency = sorted_latencies[p95_idx] if p95_idx < len(sorted_latencies) else 0
        p99_latency = sorted_latencies[p99_idx] if p99_idx < len(sorted_latencies) else 0

        # Cache hit rate
        total_cache_attempts = self.cache_hits + self.cache_misses
        cache_hit_rate = self.cache_hits / total_cache_attempts if total_cache_attempts > 0 else 0

        # Error rate
        total_errors = sum(self.errors_by_domain.values())
        error_rate = total_errors / self.total_queries if self.total_queries > 0 else 0

        # Top doctrines
        top_doctrines = sorted(
            self.doctrine_trigger_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]

        return MetricsSnapshot(
            timestamp=now.isoformat(),
            queries_total=self.total_queries,
            queries_per_hour=queries_per_hour,
            avg_latency_ms=avg_latency,
            p95_latency_ms=p95_latency,
            p99_latency_ms=p99_latency,
            cache_hit_rate=cache_hit_rate,
            error_rate=error_rate,
            errors_by_domain=dict(self.errors_by_domain),
            top_doctrines=top_doctrines
        )


class DriftWatcher:
    """Detect doctrine drift and coverage gaps"""

    def __init__(self, all_doctrine_names: List[str]):
        self.all_doctrines = set(all_doctrine_names)
        self.triggered_doctrines: set = set()
        self.query_count = 0

    def record_query(self, triggered_doctrines: List[str]):
        """Record which doctrines were triggered"""
        self.query_count += 1
        self.triggered_doctrines.update(triggered_doctrines)

    def get_coverage_report(self) -> Dict[str, Any]:
        """Generate coverage report"""
        untriggered = self.all_doctrines - self.triggered_doctrines
        coverage_pct = len(self.triggered_doctrines) / len(self.all_doctrines) * 100 if self.all_doctrines else 0

        return {
            "total_doctrines": len(self.all_doctrines),
            "triggered_doctrines": len(self.triggered_doctrines),
            "untriggered_doctrines": len(untriggered),
            "coverage_percentage": coverage_pct,
            "untriggered_list": sorted(untriggered),
            "queries_processed": self.query_count
        }

    def detect_epistemic_gaps(self) -> List[str]:
        """Identify doctrines that should have been triggered but weren't"""
        # After significant query volume, untriggered doctrines may indicate gaps
        if self.query_count < 100:
            return []  # Not enough data

        return sorted(self.all_doctrines - self.triggered_doctrines)


class PerformanceProfiler:
    """Detailed performance profiling for optimization"""

    def __init__(self):
        self.phase_timings: Dict[str, List[float]] = defaultdict(list)

    def record_phase(self, phase_name: str, duration_ms: float):
        """Record timing for a specific phase"""
        self.phase_timings[phase_name].append(duration_ms)

    def get_bottlenecks(self, threshold_ms: float = 100) -> List[tuple[str, float]]:
        """Identify performance bottlenecks"""
        bottlenecks = []
        for phase, timings in self.phase_timings.items():
            avg_time = sum(timings) / len(timings)
            if avg_time > threshold_ms:
                bottlenecks.append((phase, avg_time))
        return sorted(bottlenecks, key=lambda x: x[1], reverse=True)


def generate_determinism_hash(query: str, response: str, doctrines_used: List[str]) -> str:
    """Generate SHA-256 hash for determinism verification"""
    content = f"{query}|{response}|{'|'.join(sorted(doctrines_used))}"
    return hashlib.sha256(content.encode('utf-8')).hexdigest()


__all__ = [
    'TelemetryCollector',
    'DriftWatcher',
    'PerformanceProfiler',
    'QueryTrace',
    'MetricsSnapshot',
    'ErrorDomain',
    'QueryZone',
    'generate_determinism_hash'
]
