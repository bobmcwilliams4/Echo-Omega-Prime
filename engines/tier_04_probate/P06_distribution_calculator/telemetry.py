"""
P06_distribution_calculator - Enhanced Telemetry Module
TIE-20 Component 8: Comprehensive query tracking, performance metrics, and operational insights.
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from collections import defaultdict
from enum import Enum


class QueryType(str, Enum):
    DISTRIBUTION_CALC = "distribution_calculation"
    TESTATE = "testate_distribution"
    INTESTATE = "intestate_distribution"
    ABATEMENT = "abatement_calculation"
    TAX_APPORTIONMENT = "tax_apportionment"
    EXECUTOR_COMMISSION = "executor_commission"
    DOCTRINE_SEARCH = "doctrine_search"
    HEALTH_CHECK = "health_check"


class ErrorDomain(str, Enum):
    INPUT_VALIDATION = "input_validation"
    CALCULATION = "calculation"
    DOCTRINE_LOOKUP = "doctrine_lookup"
    EXTERNAL_API = "external_api"
    SYSTEM = "system"


@dataclass
class QueryRecord:
    """Individual query record for audit trail."""
    query_id: str
    timestamp: str
    query_type: QueryType
    estate_id: Optional[str]
    latency_ms: float
    success: bool
    error_domain: Optional[ErrorDomain]
    error_message: Optional[str]
    cache_hit: bool
    doctrines_triggered: List[str]
    confidence_level: Optional[str]


@dataclass
class PerformanceMetrics:
    """Performance metrics snapshot."""
    timestamp: str
    queries_total: int
    queries_success: int
    queries_failed: int
    avg_latency_ms: float
    p50_latency_ms: float
    p95_latency_ms: float
    p99_latency_ms: float
    cache_hit_rate: float
    error_rate: float
    queries_per_hour: float


class TelemetryEngine:
    """
    Comprehensive telemetry system for P06 distribution calculator.
    Tracks all queries, performance, errors, and doctrine usage.
    """

    def __init__(self, telemetry_dir: Path = None):
        self.telemetry_dir = telemetry_dir or Path(__file__).parent / "telemetry"
        self.telemetry_dir.mkdir(exist_ok=True)

        # In-memory metrics
        self.queries: List[QueryRecord] = []
        self.latencies: List[float] = []
        self.errors_by_domain: Dict[ErrorDomain, int] = defaultdict(int)
        self.queries_by_type: Dict[QueryType, int] = defaultdict(int)
        self.cache_hits: int = 0
        self.cache_misses: int = 0
        self.doctrine_usage: Dict[str, int] = defaultdict(int)
        self.confidence_distribution: Dict[str, int] = defaultdict(int)

        # Session tracking
        self.session_start = datetime.utcnow()
        self.last_snapshot = datetime.utcnow()

        # Load historical data if exists
        self._load_historical_metrics()

    def record_query(
        self,
        query_type: QueryType,
        estate_id: Optional[str],
        latency_ms: float,
        success: bool,
        cache_hit: bool = False,
        doctrines_triggered: List[str] = None,
        confidence_level: Optional[str] = None,
        error_domain: Optional[ErrorDomain] = None,
        error_message: Optional[str] = None
    ):
        """Record a query execution."""
        query_id = f"{query_type.value}_{datetime.utcnow().timestamp()}"

        record = QueryRecord(
            query_id=query_id,
            timestamp=datetime.utcnow().isoformat(),
            query_type=query_type,
            estate_id=estate_id,
            latency_ms=latency_ms,
            success=success,
            error_domain=error_domain,
            error_message=error_message,
            cache_hit=cache_hit,
            doctrines_triggered=doctrines_triggered or [],
            confidence_level=confidence_level
        )

        # Update in-memory metrics
        self.queries.append(record)
        self.latencies.append(latency_ms)
        self.queries_by_type[query_type] += 1

        if cache_hit:
            self.cache_hits += 1
        else:
            self.cache_misses += 1

        if not success and error_domain:
            self.errors_by_domain[error_domain] += 1

        for doctrine in (doctrines_triggered or []):
            self.doctrine_usage[doctrine] += 1

        if confidence_level:
            self.confidence_distribution[confidence_level] += 1

        # Persist to disk
        self._append_query_log(record)

    def get_current_metrics(self) -> PerformanceMetrics:
        """Get current performance metrics snapshot."""
        total_queries = len(self.queries)
        success_queries = sum(1 for q in self.queries if q.success)
        failed_queries = total_queries - success_queries

        avg_latency = sum(self.latencies) / len(self.latencies) if self.latencies else 0
        p50 = self._percentile(self.latencies, 50)
        p95 = self._percentile(self.latencies, 95)
        p99 = self._percentile(self.latencies, 99)

        cache_total = self.cache_hits + self.cache_misses
        cache_hit_rate = self.cache_hits / cache_total if cache_total > 0 else 0

        error_rate = failed_queries / total_queries if total_queries > 0 else 0

        # Queries per hour
        elapsed_hours = (datetime.utcnow() - self.session_start).total_seconds() / 3600
        qph = total_queries / elapsed_hours if elapsed_hours > 0 else 0

        return PerformanceMetrics(
            timestamp=datetime.utcnow().isoformat(),
            queries_total=total_queries,
            queries_success=success_queries,
            queries_failed=failed_queries,
            avg_latency_ms=round(avg_latency, 2),
            p50_latency_ms=round(p50, 2),
            p95_latency_ms=round(p95, 2),
            p99_latency_ms=round(p99, 2),
            cache_hit_rate=round(cache_hit_rate, 3),
            error_rate=round(error_rate, 3),
            queries_per_hour=round(qph, 2)
        )

    def get_detailed_stats(self) -> Dict[str, Any]:
        """Get detailed statistics including breakdowns."""
        metrics = self.get_current_metrics()

        return {
            "performance": asdict(metrics),
            "queries_by_type": dict(self.queries_by_type),
            "errors_by_domain": {k.value: v for k, v in self.errors_by_domain.items()},
            "top_doctrines_used": sorted(self.doctrine_usage.items(), key=lambda x: x[1], reverse=True)[:20],
            "confidence_distribution": dict(self.confidence_distribution),
            "cache_stats": {
                "hits": self.cache_hits,
                "misses": self.cache_misses,
                "hit_rate": round(self.cache_hits / (self.cache_hits + self.cache_misses), 3) if (self.cache_hits + self.cache_misses) > 0 else 0
            },
            "session_info": {
                "start_time": self.session_start.isoformat(),
                "uptime_hours": round((datetime.utcnow() - self.session_start).total_seconds() / 3600, 2),
                "total_queries": len(self.queries)
            }
        }

    def get_error_summary(self) -> Dict[str, Any]:
        """Get summary of errors encountered."""
        error_queries = [q for q in self.queries if not q.success]

        errors_by_type = defaultdict(list)
        for query in error_queries:
            errors_by_type[query.error_domain.value if query.error_domain else "UNKNOWN"].append({
                "timestamp": query.timestamp,
                "query_type": query.query_type.value,
                "error_message": query.error_message
            })

        return {
            "total_errors": len(error_queries),
            "error_rate": len(error_queries) / len(self.queries) if self.queries else 0,
            "errors_by_domain": {k.value: v for k, v in self.errors_by_domain.items()},
            "recent_errors": error_queries[-10:],  # Last 10 errors
            "errors_by_type": dict(errors_by_type)
        }

    def get_latency_distribution(self) -> Dict[str, float]:
        """Get latency percentile distribution."""
        if not self.latencies:
            return {}

        return {
            "min_ms": round(min(self.latencies), 2),
            "p10_ms": round(self._percentile(self.latencies, 10), 2),
            "p25_ms": round(self._percentile(self.latencies, 25), 2),
            "p50_ms": round(self._percentile(self.latencies, 50), 2),
            "p75_ms": round(self._percentile(self.latencies, 75), 2),
            "p90_ms": round(self._percentile(self.latencies, 90), 2),
            "p95_ms": round(self._percentile(self.latencies, 95), 2),
            "p99_ms": round(self._percentile(self.latencies, 99), 2),
            "max_ms": round(max(self.latencies), 2),
            "avg_ms": round(sum(self.latencies) / len(self.latencies), 2)
        }

    def get_doctrine_coverage(self) -> Dict[str, Any]:
        """Get doctrine usage coverage statistics."""
        total_doctrines_available = 50  # From doctrines.py
        doctrines_used = len(self.doctrine_usage)
        coverage_pct = (doctrines_used / total_doctrines_available * 100) if total_doctrines_available > 0 else 0

        return {
            "total_available": total_doctrines_available,
            "doctrines_used": doctrines_used,
            "coverage_percentage": round(coverage_pct, 2),
            "top_20_used": sorted(self.doctrine_usage.items(), key=lambda x: x[1], reverse=True)[:20],
            "usage_distribution": {
                "high_use_10plus": sum(1 for v in self.doctrine_usage.values() if v >= 10),
                "medium_use_3to9": sum(1 for v in self.doctrine_usage.values() if 3 <= v < 10),
                "low_use_1to2": sum(1 for v in self.doctrine_usage.values() if 1 <= v < 3)
            }
        }

    def generate_hourly_report(self) -> Dict[str, Any]:
        """Generate hourly performance report."""
        now = datetime.utcnow()
        hour_ago = now - timedelta(hours=1)

        recent_queries = [q for q in self.queries if datetime.fromisoformat(q.timestamp) >= hour_ago]
        recent_latencies = [q.latency_ms for q in recent_queries]
        recent_errors = [q for q in recent_queries if not q.success]

        return {
            "period": "last_1_hour",
            "start_time": hour_ago.isoformat(),
            "end_time": now.isoformat(),
            "queries_total": len(recent_queries),
            "queries_success": len(recent_queries) - len(recent_errors),
            "queries_failed": len(recent_errors),
            "avg_latency_ms": round(sum(recent_latencies) / len(recent_latencies), 2) if recent_latencies else 0,
            "p95_latency_ms": round(self._percentile(recent_latencies, 95), 2) if recent_latencies else 0,
            "error_rate": round(len(recent_errors) / len(recent_queries), 3) if recent_queries else 0,
            "queries_per_minute": round(len(recent_queries) / 60, 2)
        }

    def snapshot_to_disk(self):
        """Save current metrics snapshot to disk."""
        snapshot_path = self.telemetry_dir / f"snapshot_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"

        snapshot = {
            "timestamp": datetime.utcnow().isoformat(),
            "performance_metrics": asdict(self.get_current_metrics()),
            "detailed_stats": self.get_detailed_stats(),
            "error_summary": self.get_error_summary(),
            "latency_distribution": self.get_latency_distribution(),
            "doctrine_coverage": self.get_doctrine_coverage()
        }

        with open(snapshot_path, 'w') as f:
            json.dump(snapshot, f, indent=2, default=str)

        self.last_snapshot = datetime.utcnow()

    def _append_query_log(self, record: QueryRecord):
        """Append query record to persistent log file."""
        log_path = self.telemetry_dir / "query_log.jsonl"

        with open(log_path, 'a') as f:
            f.write(json.dumps(asdict(record), default=str) + "\n")

    def _load_historical_metrics(self):
        """Load historical metrics from disk on startup."""
        log_path = self.telemetry_dir / "query_log.jsonl"

        if not log_path.exists():
            return

        # Load last 1000 queries from historical log
        try:
            with open(log_path, 'r') as f:
                lines = f.readlines()

            for line in lines[-1000:]:  # Last 1000 queries
                record_data = json.loads(line)
                record = QueryRecord(**record_data)
                self.queries.append(record)
                self.latencies.append(record.latency_ms)

                if record.cache_hit:
                    self.cache_hits += 1
                else:
                    self.cache_misses += 1

        except Exception as e:
            # Log error but don't fail on historical data load
            pass

    def _percentile(self, data: List[float], percentile: int) -> float:
        """Calculate percentile of data."""
        if not data:
            return 0.0

        sorted_data = sorted(data)
        index = int(len(sorted_data) * percentile / 100)
        if index >= len(sorted_data):
            index = len(sorted_data) - 1

        return sorted_data[index]

    def reset_metrics(self):
        """Reset in-memory metrics (for testing or periodic cleanup)."""
        self.queries = []
        self.latencies = []
        self.errors_by_domain = defaultdict(int)
        self.queries_by_type = defaultdict(int)
        self.cache_hits = 0
        self.cache_misses = 0
        self.doctrine_usage = defaultdict(int)
        self.confidence_distribution = defaultdict(int)
        self.session_start = datetime.utcnow()
