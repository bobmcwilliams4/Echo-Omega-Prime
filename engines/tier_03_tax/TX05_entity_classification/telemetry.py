"""
TX05 Entity Classification Engine - Telemetry Module
Comprehensive telemetry, metrics, and monitoring for entity classification queries
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Set
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict, deque
import json
import hashlib
from loguru import logger


@dataclass
class QueryMetrics:
    """Metrics for a single query"""
    query_id: str
    timestamp: str
    query_text: str
    normalized_query: str
    entity_type: str
    issue_categories: List[str]
    response_mode: str
    cache_hit: bool
    cache_latency_ms: float
    semantic_latency_ms: float
    deep_latency_ms: float
    total_latency_ms: float
    doctrines_triggered: List[str]
    doctrines_missed: List[str]
    confidence_level: str
    error_domain: Optional[str] = None
    epistemic_flags: List[str] = field(default_factory=list)
    determinism_hash: Optional[str] = None


@dataclass
class DoctrineMetrics:
    """Metrics for doctrine block usage"""
    topic: str
    hit_count: int = 0
    miss_count: int = 0
    avg_confidence: float = 0.0
    last_triggered: Optional[str] = None
    queries_matched: List[str] = field(default_factory=list)


@dataclass
class EngineHealthMetrics:
    """Overall engine health metrics"""
    uptime_seconds: float
    total_queries: int
    queries_per_hour: float
    cache_hit_rate: float
    avg_latency_ms: float
    p95_latency_ms: float
    p99_latency_ms: float
    error_rate: float
    doctrine_coverage: float
    active_doctrines: int
    total_doctrines: int


class TelemetryCollector:
    """Comprehensive telemetry collection and analysis"""

    def __init__(self, engine_id: str, audit_trail_path: Optional[Path] = None):
        """
        Initialize telemetry collector

        Args:
            engine_id: Unique engine identifier
            audit_trail_path: Path to audit trail JSONL file
        """
        self.engine_id = engine_id
        self.audit_trail_path = audit_trail_path or Path(f"./audit_trail_{engine_id}.jsonl")
        self.start_time = datetime.now()

        # Metrics storage
        self.query_history: deque = deque(maxlen=10000)
        self.doctrine_metrics: Dict[str, DoctrineMetrics] = {}
        self.latency_samples: deque = deque(maxlen=1000)
        self.error_counts: defaultdict = defaultdict(int)
        self.hourly_query_counts: defaultdict = defaultdict(int)

        # Real-time tracking
        self.total_queries = 0
        self.total_cache_hits = 0
        self.total_errors = 0
        self.epistemic_trigger_count = 0

        logger.info(f"Telemetry collector initialized for {engine_id}")

    def record_query(self, metrics: QueryMetrics):
        """
        Record query metrics

        Args:
            metrics: Query metrics to record
        """
        self.total_queries += 1
        if metrics.cache_hit:
            self.total_cache_hits += 1
        if metrics.error_domain:
            self.total_errors += 1
            self.error_counts[metrics.error_domain] += 1
        if metrics.epistemic_flags:
            self.epistemic_trigger_count += 1

        # Update latency samples
        self.latency_samples.append(metrics.total_latency_ms)

        # Update doctrine metrics
        for doctrine_topic in metrics.doctrines_triggered:
            if doctrine_topic not in self.doctrine_metrics:
                self.doctrine_metrics[doctrine_topic] = DoctrineMetrics(topic=doctrine_topic)

            dm = self.doctrine_metrics[doctrine_topic]
            dm.hit_count += 1
            dm.last_triggered = metrics.timestamp
            dm.queries_matched.append(metrics.query_id)

        for doctrine_topic in metrics.doctrines_missed:
            if doctrine_topic not in self.doctrine_metrics:
                self.doctrine_metrics[doctrine_topic] = DoctrineMetrics(topic=doctrine_topic)
            self.doctrine_metrics[doctrine_topic].miss_count += 1

        # Update hourly query count
        hour_key = datetime.fromisoformat(metrics.timestamp).strftime("%Y-%m-%d-%H")
        self.hourly_query_counts[hour_key] += 1

        # Store in history
        self.query_history.append(metrics)

        # Append to audit trail
        self._append_audit_trail(metrics)

        logger.debug(f"Query {metrics.query_id} telemetry recorded")

    def _append_audit_trail(self, metrics: QueryMetrics):
        """
        Append query to audit trail JSONL file

        Args:
            metrics: Query metrics to append
        """
        try:
            with open(self.audit_trail_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(asdict(metrics)) + '\n')
        except Exception as e:
            logger.error(f"Failed to append to audit trail: {e}")

    def get_health_metrics(self) -> EngineHealthMetrics:
        """
        Calculate current engine health metrics

        Returns:
            Engine health metrics
        """
        uptime = (datetime.now() - self.start_time).total_seconds()

        # Calculate cache hit rate
        cache_hit_rate = (
            self.total_cache_hits / self.total_queries
            if self.total_queries > 0 else 0.0
        )

        # Calculate latency percentiles
        latencies = sorted(self.latency_samples)
        avg_latency = sum(latencies) / len(latencies) if latencies else 0.0
        p95_latency = latencies[int(len(latencies) * 0.95)] if latencies else 0.0
        p99_latency = latencies[int(len(latencies) * 0.99)] if latencies else 0.0

        # Calculate error rate
        error_rate = self.total_errors / self.total_queries if self.total_queries > 0 else 0.0

        # Calculate queries per hour
        hours_running = uptime / 3600.0 if uptime > 0 else 1.0
        queries_per_hour = self.total_queries / hours_running

        # Calculate doctrine coverage
        total_doctrines = len(self.doctrine_metrics)
        active_doctrines = sum(1 for dm in self.doctrine_metrics.values() if dm.hit_count > 0)
        doctrine_coverage = active_doctrines / total_doctrines if total_doctrines > 0 else 0.0

        return EngineHealthMetrics(
            uptime_seconds=uptime,
            total_queries=self.total_queries,
            queries_per_hour=queries_per_hour,
            cache_hit_rate=cache_hit_rate,
            avg_latency_ms=avg_latency,
            p95_latency_ms=p95_latency,
            p99_latency_ms=p99_latency,
            error_rate=error_rate,
            doctrine_coverage=doctrine_coverage,
            active_doctrines=active_doctrines,
            total_doctrines=total_doctrines
        )

    def get_doctrine_coverage_report(self) -> Dict[str, any]:
        """
        Generate doctrine coverage report

        Returns:
            Doctrine coverage statistics
        """
        triggered_doctrines = [
            dm.topic for dm in self.doctrine_metrics.values() if dm.hit_count > 0
        ]
        never_triggered = [
            dm.topic for dm in self.doctrine_metrics.values() if dm.hit_count == 0
        ]
        top_doctrines = sorted(
            self.doctrine_metrics.values(),
            key=lambda dm: dm.hit_count,
            reverse=True
        )[:10]

        return {
            'total_doctrines': len(self.doctrine_metrics),
            'triggered_doctrines_count': len(triggered_doctrines),
            'never_triggered_count': len(never_triggered),
            'coverage_percentage': (len(triggered_doctrines) / len(self.doctrine_metrics) * 100)
                if self.doctrine_metrics else 0.0,
            'top_doctrines': [
                {
                    'topic': dm.topic,
                    'hit_count': dm.hit_count,
                    'last_triggered': dm.last_triggered
                }
                for dm in top_doctrines
            ],
            'never_triggered': never_triggered[:20]  # First 20
        }

    def get_latency_report(self) -> Dict[str, any]:
        """
        Generate latency analysis report

        Returns:
            Latency statistics
        """
        latencies = sorted(self.latency_samples)
        if not latencies:
            return {'error': 'No latency samples'}

        return {
            'sample_count': len(latencies),
            'min_ms': latencies[0],
            'max_ms': latencies[-1],
            'avg_ms': sum(latencies) / len(latencies),
            'median_ms': latencies[len(latencies) // 2],
            'p50_ms': latencies[int(len(latencies) * 0.50)],
            'p75_ms': latencies[int(len(latencies) * 0.75)],
            'p90_ms': latencies[int(len(latencies) * 0.90)],
            'p95_ms': latencies[int(len(latencies) * 0.95)],
            'p99_ms': latencies[int(len(latencies) * 0.99)],
            'under_200ms_pct': sum(1 for l in latencies if l < 200) / len(latencies) * 100,
            'under_500ms_pct': sum(1 for l in latencies if l < 500) / len(latencies) * 100
        }

    def get_error_report(self) -> Dict[str, any]:
        """
        Generate error analysis report

        Returns:
            Error statistics
        """
        return {
            'total_errors': self.total_errors,
            'error_rate': self.total_errors / self.total_queries if self.total_queries > 0 else 0.0,
            'error_domains': dict(self.error_counts),
            'top_error_domain': max(self.error_counts, key=self.error_counts.get)
                if self.error_counts else None
        }

    def get_query_volume_report(self) -> Dict[str, any]:
        """
        Generate query volume analysis

        Returns:
            Query volume statistics
        """
        recent_hour = datetime.now().strftime("%Y-%m-%d-%H")
        recent_queries = self.hourly_query_counts.get(recent_hour, 0)

        hourly_avg = (
            sum(self.hourly_query_counts.values()) / len(self.hourly_query_counts)
            if self.hourly_query_counts else 0
        )

        return {
            'total_queries': self.total_queries,
            'queries_this_hour': recent_queries,
            'hourly_average': hourly_avg,
            'hourly_breakdown': dict(self.hourly_query_counts)
        }

    def calculate_determinism_hash(self, query: str, response: str) -> str:
        """
        Calculate SHA-256 determinism hash for reproducibility

        Args:
            query: Query text
            response: Response text

        Returns:
            SHA-256 hash string
        """
        combined = f"{query}|{response}"
        return hashlib.sha256(combined.encode('utf-8')).hexdigest()

    def detect_epistemic_gaps(self, triggered_doctrines: List[str], all_doctrines: List[str]) -> List[str]:
        """
        Detect epistemic gaps (doctrines that should have triggered but didn't)

        Args:
            triggered_doctrines: Doctrines that were triggered
            all_doctrines: All available doctrines

        Returns:
            List of potentially missed doctrines
        """
        missed = set(all_doctrines) - set(triggered_doctrines)
        return list(missed)

    def export_metrics(self, output_path: Path):
        """
        Export all metrics to JSON file

        Args:
            output_path: Path to output file
        """
        export_data = {
            'engine_id': self.engine_id,
            'export_timestamp': datetime.now().isoformat(),
            'health_metrics': asdict(self.get_health_metrics()),
            'doctrine_coverage': self.get_doctrine_coverage_report(),
            'latency_report': self.get_latency_report(),
            'error_report': self.get_error_report(),
            'query_volume': self.get_query_volume_report(),
            'recent_queries': [asdict(q) for q in list(self.query_history)[-100:]]
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2)

        logger.info(f"Metrics exported to {output_path}")


class DriftWatcher:
    """Monitor doctrine drift over time"""

    def __init__(self):
        self.doctrine_versions: Dict[str, List[Dict]] = defaultdict(list)
        self.drift_events: List[Dict] = []

    def record_doctrine_snapshot(self, topic: str, content_hash: str):
        """
        Record doctrine content snapshot

        Args:
            topic: Doctrine topic
            content_hash: Hash of doctrine content
        """
        self.doctrine_versions[topic].append({
            'timestamp': datetime.now().isoformat(),
            'content_hash': content_hash
        })

    def detect_drift(self, topic: str, current_hash: str) -> bool:
        """
        Detect if doctrine has drifted from original

        Args:
            topic: Doctrine topic
            current_hash: Current content hash

        Returns:
            True if drift detected
        """
        if topic not in self.doctrine_versions or not self.doctrine_versions[topic]:
            return False

        original_hash = self.doctrine_versions[topic][0]['content_hash']
        drifted = original_hash != current_hash

        if drifted:
            self.drift_events.append({
                'topic': topic,
                'timestamp': datetime.now().isoformat(),
                'original_hash': original_hash,
                'current_hash': current_hash
            })
            logger.warning(f"Doctrine drift detected for {topic}")

        return drifted

    def get_drift_report(self) -> Dict[str, any]:
        """
        Generate drift report

        Returns:
            Drift statistics
        """
        return {
            'total_doctrines_tracked': len(self.doctrine_versions),
            'drift_events': len(self.drift_events),
            'recent_drift_events': self.drift_events[-10:],
            'doctrines_with_drift': list(set(e['topic'] for e in self.drift_events))
        }
