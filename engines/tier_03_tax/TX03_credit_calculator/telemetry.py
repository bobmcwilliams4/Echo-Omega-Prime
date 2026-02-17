"""
TX03 Credit Calculator Engine - Telemetry Module
Comprehensive query tracking, latency monitoring, and error domains
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from pathlib import Path
import json
from collections import defaultdict
from loguru import logger


@dataclass
class QueryMetric:
    """Single query telemetry record"""
    query_id: str
    timestamp: datetime
    query_text: str
    response_mode: str
    issue_category: Optional[str]
    doctrines_triggered: List[str]
    latency_ms: float
    cache_hit: bool
    error_domain: Optional[str] = None
    confidence_level: Optional[float] = None
    tokens_used: int = 0


@dataclass
class EngineMetrics:
    """Aggregate engine metrics"""
    total_queries: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    avg_latency_ms: float = 0.0
    p95_latency_ms: float = 0.0
    p99_latency_ms: float = 0.0
    error_count: int = 0
    error_rate: float = 0.0
    queries_per_hour: float = 0.0
    top_doctrines: Dict[str, int] = field(default_factory=dict)
    top_error_domains: Dict[str, int] = field(default_factory=dict)
    uptime_hours: float = 0.0


class TelemetryCollector:
    """Collect and aggregate telemetry data for credit calculator engine"""

    def __init__(self, config_path: Path, audit_trail_path: Optional[Path] = None):
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        telemetry_config = config.get('telemetry', {})
        self.enable_query_logging = telemetry_config.get('enable_query_logging', True)
        self.enable_latency_tracking = telemetry_config.get('enable_latency_tracking', True)
        self.enable_error_tracking = telemetry_config.get('enable_error_tracking', True)
        self.enable_drift_detection = telemetry_config.get('enable_drift_detection', True)

        self.audit_trail_path = audit_trail_path or Path(telemetry_config.get('audit_trail_path', 'audit_trail.jsonl'))
        self.metrics_retention_days = telemetry_config.get('metrics_retention_days', 90)

        # In-memory metrics storage
        self.query_history: List[QueryMetric] = []
        self.error_log: List[Dict[str, Any]] = []
        self.doctrine_triggers: defaultdict = defaultdict(int)
        self.latency_samples: List[float] = []
        self.start_time = datetime.utcnow()

        logger.info(f"TelemetryCollector initialized, audit trail: {self.audit_trail_path}")

    def record_query(
        self,
        query_id: str,
        query_text: str,
        response_mode: str,
        doctrines_triggered: List[str],
        latency_ms: float,
        cache_hit: bool,
        issue_category: Optional[str] = None,
        error_domain: Optional[str] = None,
        confidence_level: Optional[float] = None,
        tokens_used: int = 0
    ) -> None:
        """Record a single query execution"""
        metric = QueryMetric(
            query_id=query_id,
            timestamp=datetime.utcnow(),
            query_text=query_text,
            response_mode=response_mode,
            issue_category=issue_category,
            doctrines_triggered=doctrines_triggered,
            latency_ms=latency_ms,
            cache_hit=cache_hit,
            error_domain=error_domain,
            confidence_level=confidence_level,
            tokens_used=tokens_used
        )

        # Store in memory
        self.query_history.append(metric)

        # Track doctrine triggers
        for doctrine in doctrines_triggered:
            self.doctrine_triggers[doctrine] += 1

        # Track latency
        if self.enable_latency_tracking:
            self.latency_samples.append(latency_ms)

        # Write to audit trail (JSONL format)
        if self.enable_query_logging:
            self._write_audit_trail(metric)

        # Cleanup old metrics
        self._cleanup_old_metrics()

    def record_error(
        self,
        query_id: str,
        error_domain: str,
        error_message: str,
        stack_trace: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Record an error occurrence"""
        error_record = {
            'query_id': query_id,
            'timestamp': datetime.utcnow().isoformat(),
            'error_domain': error_domain,
            'error_message': error_message,
            'stack_trace': stack_trace,
            'metadata': metadata or {}
        }

        self.error_log.append(error_record)

        if self.enable_error_tracking:
            logger.error(f"Query {query_id} error in {error_domain}: {error_message}")

    def get_metrics(self) -> EngineMetrics:
        """Get current aggregate metrics"""
        if not self.query_history:
            return EngineMetrics()

        total_queries = len(self.query_history)
        cache_hits = sum(1 for q in self.query_history if q.cache_hit)
        cache_misses = total_queries - cache_hits
        error_count = len(self.error_log)

        # Calculate latencies
        latencies = [q.latency_ms for q in self.query_history]
        avg_latency = sum(latencies) / len(latencies) if latencies else 0.0

        # Percentiles
        sorted_latencies = sorted(latencies)
        p95_index = int(0.95 * len(sorted_latencies))
        p99_index = int(0.99 * len(sorted_latencies))
        p95_latency = sorted_latencies[p95_index] if sorted_latencies else 0.0
        p99_latency = sorted_latencies[p99_index] if sorted_latencies else 0.0

        # Error rate
        error_rate = error_count / total_queries if total_queries > 0 else 0.0

        # Queries per hour
        uptime_hours = (datetime.utcnow() - self.start_time).total_seconds() / 3600
        queries_per_hour = total_queries / uptime_hours if uptime_hours > 0 else 0.0

        # Top doctrines
        top_doctrines = dict(sorted(self.doctrine_triggers.items(), key=lambda x: x[1], reverse=True)[:10])

        # Top error domains
        error_domains = defaultdict(int)
        for error in self.error_log:
            error_domains[error['error_domain']] += 1
        top_error_domains = dict(sorted(error_domains.items(), key=lambda x: x[1], reverse=True)[:10])

        return EngineMetrics(
            total_queries=total_queries,
            cache_hits=cache_hits,
            cache_misses=cache_misses,
            avg_latency_ms=avg_latency,
            p95_latency_ms=p95_latency,
            p99_latency_ms=p99_latency,
            error_count=error_count,
            error_rate=error_rate,
            queries_per_hour=queries_per_hour,
            top_doctrines=top_doctrines,
            top_error_domains=top_error_domains,
            uptime_hours=uptime_hours
        )

    def get_metrics_dict(self) -> Dict[str, Any]:
        """Get metrics as dictionary for JSON serialization"""
        metrics = self.get_metrics()
        return asdict(metrics)

    def get_doctrine_coverage(self) -> Dict[str, Any]:
        """Get doctrine coverage statistics"""
        triggered_doctrines = set(self.doctrine_triggers.keys())
        total_doctrines = 65  # From DOCTRINE_CACHE

        return {
            'triggered_count': len(triggered_doctrines),
            'total_count': total_doctrines,
            'coverage_pct': (len(triggered_doctrines) / total_doctrines * 100) if total_doctrines > 0 else 0.0,
            'untriggered_count': total_doctrines - len(triggered_doctrines),
            'trigger_counts': dict(self.doctrine_triggers)
        }

    def get_latency_distribution(self) -> Dict[str, float]:
        """Get latency distribution percentiles"""
        if not self.latency_samples:
            return {}

        sorted_latencies = sorted(self.latency_samples)
        n = len(sorted_latencies)

        percentiles = [10, 25, 50, 75, 90, 95, 99]
        distribution = {}

        for p in percentiles:
            index = int((p / 100) * n)
            distribution[f'p{p}'] = sorted_latencies[min(index, n - 1)]

        distribution['min'] = sorted_latencies[0]
        distribution['max'] = sorted_latencies[-1]
        distribution['mean'] = sum(sorted_latencies) / n

        return distribution

    def get_error_summary(self) -> Dict[str, Any]:
        """Get error summary statistics"""
        if not self.error_log:
            return {'total_errors': 0, 'by_domain': {}, 'recent_errors': []}

        error_domains = defaultdict(int)
        for error in self.error_log:
            error_domains[error['error_domain']] += 1

        # Get recent errors (last 10)
        recent_errors = sorted(self.error_log, key=lambda x: x['timestamp'], reverse=True)[:10]

        return {
            'total_errors': len(self.error_log),
            'by_domain': dict(error_domains),
            'recent_errors': recent_errors
        }

    def get_query_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent query history"""
        recent_queries = sorted(self.query_history, key=lambda x: x.timestamp, reverse=True)[:limit]
        return [
            {
                'query_id': q.query_id,
                'timestamp': q.timestamp.isoformat(),
                'query_text': q.query_text[:100],  # Truncate for readability
                'response_mode': q.response_mode,
                'latency_ms': q.latency_ms,
                'cache_hit': q.cache_hit,
                'doctrines_count': len(q.doctrines_triggered)
            }
            for q in recent_queries
        ]

    def _write_audit_trail(self, metric: QueryMetric) -> None:
        """Write query metric to JSONL audit trail"""
        try:
            audit_record = {
                'query_id': metric.query_id,
                'timestamp': metric.timestamp.isoformat(),
                'query_text': metric.query_text,
                'response_mode': metric.response_mode,
                'issue_category': metric.issue_category,
                'doctrines_triggered': metric.doctrines_triggered,
                'latency_ms': metric.latency_ms,
                'cache_hit': metric.cache_hit,
                'error_domain': metric.error_domain,
                'confidence_level': metric.confidence_level,
                'tokens_used': metric.tokens_used
            }

            # Append to JSONL file
            with open(self.audit_trail_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(audit_record) + '\n')

        except Exception as e:
            logger.error(f"Failed to write audit trail: {e}")

    def _cleanup_old_metrics(self) -> None:
        """Remove metrics older than retention period"""
        cutoff = datetime.utcnow() - timedelta(days=self.metrics_retention_days)

        # Cleanup query history
        self.query_history = [q for q in self.query_history if q.timestamp >= cutoff]

        # Cleanup error log
        self.error_log = [e for e in self.error_log if datetime.fromisoformat(e['timestamp']) >= cutoff]

    def reset_metrics(self) -> None:
        """Reset all in-memory metrics (for testing or manual reset)"""
        self.query_history.clear()
        self.error_log.clear()
        self.doctrine_triggers.clear()
        self.latency_samples.clear()
        self.start_time = datetime.utcnow()
        logger.warning("Telemetry metrics reset")

    def export_metrics(self, output_path: Path) -> None:
        """Export current metrics to JSON file"""
        export_data = {
            'export_timestamp': datetime.utcnow().isoformat(),
            'metrics': self.get_metrics_dict(),
            'doctrine_coverage': self.get_doctrine_coverage(),
            'latency_distribution': self.get_latency_distribution(),
            'error_summary': self.get_error_summary(),
            'query_history': self.get_query_history(limit=1000)
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2)

        logger.info(f"Metrics exported to {output_path}")
