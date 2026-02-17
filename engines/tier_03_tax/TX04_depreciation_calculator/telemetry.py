"""
TX04 Depreciation Calculator - Telemetry Module
Query tracing, latency tracking, error monitoring, and audit trail.
"""

import time
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict, field
from enum import Enum
from loguru import logger


class QueryType(str, Enum):
    """Query type classification."""
    CALCULATION = "calculation"
    RECAPTURE = "recapture"
    ELECTION = "election"
    QUALIFICATION = "qualification"
    GENERAL = "general"


class ResponseMode(str, Enum):
    """Response mode classification."""
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"


class ErrorDomain(str, Enum):
    """Error categorization."""
    INPUT_VALIDATION = "input_validation"
    DOCTRINE_CACHE = "doctrine_cache"
    VECTOR_SEARCH = "vector_search"
    CALCULATION = "calculation"
    EXTERNAL_API = "external_api"
    SYSTEM = "system"


@dataclass
class QueryMetrics:
    """Metrics for a single query."""
    query_id: str
    timestamp: str
    query_text: str
    query_type: QueryType
    response_mode: ResponseMode

    # Latency breakdown (milliseconds)
    total_latency_ms: float
    cache_latency_ms: float
    vector_search_latency_ms: float
    llm_latency_ms: float

    # Cache performance
    cache_hit: bool
    doctrines_matched: List[str]

    # Vector search (if used)
    vector_search_used: bool
    vector_results_count: int

    # Response metrics
    response_length_chars: int
    confidence_score: float

    # Determinism verification
    determinism_hash: str

    # Error tracking
    errors: List[Dict[str, str]] = field(default_factory=list)

    # Metadata
    user_agent: Optional[str] = None
    ip_address: Optional[str] = None


@dataclass
class AggregateMetrics:
    """Aggregate telemetry metrics."""
    total_queries: int = 0
    successful_queries: int = 0
    failed_queries: int = 0

    # Latency stats (milliseconds)
    avg_latency_ms: float = 0.0
    p50_latency_ms: float = 0.0
    p95_latency_ms: float = 0.0
    p99_latency_ms: float = 0.0

    # Cache performance
    cache_hit_rate: float = 0.0
    avg_doctrines_per_query: float = 0.0

    # Vector search usage
    vector_search_usage_rate: float = 0.0

    # Error rates by domain
    error_rate_by_domain: Dict[str, float] = field(default_factory=dict)

    # Query type distribution
    query_type_distribution: Dict[str, int] = field(default_factory=dict)

    # Response mode distribution
    response_mode_distribution: Dict[str, int] = field(default_factory=dict)


class DepreciationTelemetry:
    """Telemetry system for depreciation calculator engine."""

    def __init__(self, log_dir: Path, retention_days: int = 730):
        """
        Initialize telemetry.

        Args:
            log_dir: Directory for telemetry logs
            retention_days: Days to retain audit logs
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.audit_file = self.log_dir / "audit_trail.jsonl"
        self.metrics_file = self.log_dir / "metrics.json"

        self.retention_days = retention_days

        # In-memory metrics (last 1000 queries)
        self.recent_queries: List[QueryMetrics] = []
        self.max_recent_queries = 1000

        # Aggregate metrics
        self.aggregate = AggregateMetrics()

        # Load existing metrics if available
        self._load_metrics()

    def start_query(self, query_text: str, query_type: QueryType, response_mode: ResponseMode) -> str:
        """
        Start tracking a query.

        Args:
            query_text: Query text
            query_type: Query classification
            response_mode: Response mode

        Returns:
            Query ID for tracking
        """
        query_id = hashlib.sha256(
            f"{query_text}{time.time()}".encode()
        ).hexdigest()[:16]

        logger.info(
            f"Query started",
            query_id=query_id,
            query_type=query_type.value,
            response_mode=response_mode.value
        )

        return query_id

    def record_query(
        self,
        query_id: str,
        query_text: str,
        query_type: QueryType,
        response_mode: ResponseMode,
        total_latency_ms: float,
        cache_latency_ms: float,
        vector_search_latency_ms: float,
        llm_latency_ms: float,
        cache_hit: bool,
        doctrines_matched: List[str],
        vector_search_used: bool,
        vector_results_count: int,
        response_length_chars: int,
        confidence_score: float,
        determinism_hash: str,
        errors: Optional[List[Dict[str, str]]] = None,
        user_agent: Optional[str] = None,
        ip_address: Optional[str] = None
    ):
        """
        Record completed query metrics.

        Args:
            query_id: Unique query identifier
            query_text: Original query
            query_type: Query classification
            response_mode: Response mode used
            total_latency_ms: Total query latency
            cache_latency_ms: Cache lookup latency
            vector_search_latency_ms: Vector search latency
            llm_latency_ms: LLM processing latency
            cache_hit: Whether cache hit
            doctrines_matched: List of doctrine topics matched
            vector_search_used: Whether vector search was used
            vector_results_count: Number of vector results
            response_length_chars: Response character count
            confidence_score: Confidence score (0.0-1.0)
            determinism_hash: SHA-256 hash for determinism verification
            errors: List of errors encountered
            user_agent: User agent string
            ip_address: Client IP address
        """
        metrics = QueryMetrics(
            query_id=query_id,
            timestamp=datetime.utcnow().isoformat(),
            query_text=query_text,
            query_type=query_type,
            response_mode=response_mode,
            total_latency_ms=total_latency_ms,
            cache_latency_ms=cache_latency_ms,
            vector_search_latency_ms=vector_search_latency_ms,
            llm_latency_ms=llm_latency_ms,
            cache_hit=cache_hit,
            doctrines_matched=doctrines_matched,
            vector_search_used=vector_search_used,
            vector_results_count=vector_results_count,
            response_length_chars=response_length_chars,
            confidence_score=confidence_score,
            determinism_hash=determinism_hash,
            errors=errors or [],
            user_agent=user_agent,
            ip_address=ip_address
        )

        # Append to recent queries (circular buffer)
        self.recent_queries.append(metrics)
        if len(self.recent_queries) > self.max_recent_queries:
            self.recent_queries.pop(0)

        # Update aggregate metrics
        self._update_aggregates(metrics)

        # Write to audit trail
        self._write_audit_trail(metrics)

        # Persist metrics
        self._save_metrics()

        logger.info(
            f"Query recorded",
            query_id=query_id,
            total_latency_ms=total_latency_ms,
            cache_hit=cache_hit,
            doctrines_matched_count=len(doctrines_matched)
        )

    def record_error(
        self,
        query_id: str,
        error_domain: ErrorDomain,
        error_message: str,
        stack_trace: Optional[str] = None
    ):
        """
        Record an error.

        Args:
            query_id: Query identifier
            error_domain: Error categorization
            error_message: Error description
            stack_trace: Optional stack trace
        """
        error_record = {
            "query_id": query_id,
            "timestamp": datetime.utcnow().isoformat(),
            "domain": error_domain.value,
            "message": error_message,
            "stack_trace": stack_trace
        }

        logger.error(
            f"Error recorded",
            query_id=query_id,
            error_domain=error_domain.value,
            error_message=error_message
        )

        # Write to audit trail
        with self.audit_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"error": error_record}) + "\n")

    def get_aggregate_metrics(self) -> AggregateMetrics:
        """
        Get current aggregate metrics.

        Returns:
            Aggregate metrics object
        """
        return self.aggregate

    def get_recent_queries(self, count: int = 100) -> List[QueryMetrics]:
        """
        Get recent query metrics.

        Args:
            count: Number of recent queries to return

        Returns:
            List of recent query metrics
        """
        return self.recent_queries[-count:]

    def _update_aggregates(self, metrics: QueryMetrics):
        """Update aggregate metrics with new query."""
        self.aggregate.total_queries += 1

        if not metrics.errors:
            self.aggregate.successful_queries += 1
        else:
            self.aggregate.failed_queries += 1

        # Update latency stats (simplified - use recent queries for percentiles)
        recent_latencies = [q.total_latency_ms for q in self.recent_queries]
        if recent_latencies:
            self.aggregate.avg_latency_ms = sum(recent_latencies) / len(recent_latencies)
            sorted_latencies = sorted(recent_latencies)
            n = len(sorted_latencies)
            self.aggregate.p50_latency_ms = sorted_latencies[int(n * 0.50)]
            self.aggregate.p95_latency_ms = sorted_latencies[int(n * 0.95)] if n > 20 else sorted_latencies[-1]
            self.aggregate.p99_latency_ms = sorted_latencies[int(n * 0.99)] if n > 100 else sorted_latencies[-1]

        # Cache hit rate
        cache_hits = sum(1 for q in self.recent_queries if q.cache_hit)
        self.aggregate.cache_hit_rate = cache_hits / len(self.recent_queries) if self.recent_queries else 0.0

        # Average doctrines per query
        total_doctrines = sum(len(q.doctrines_matched) for q in self.recent_queries)
        self.aggregate.avg_doctrines_per_query = total_doctrines / len(self.recent_queries) if self.recent_queries else 0.0

        # Vector search usage rate
        vector_searches = sum(1 for q in self.recent_queries if q.vector_search_used)
        self.aggregate.vector_search_usage_rate = vector_searches / len(self.recent_queries) if self.recent_queries else 0.0

        # Query type distribution
        self.aggregate.query_type_distribution[metrics.query_type.value] = \
            self.aggregate.query_type_distribution.get(metrics.query_type.value, 0) + 1

        # Response mode distribution
        self.aggregate.response_mode_distribution[metrics.response_mode.value] = \
            self.aggregate.response_mode_distribution.get(metrics.response_mode.value, 0) + 1

    def _write_audit_trail(self, metrics: QueryMetrics):
        """Write query metrics to audit trail."""
        with self.audit_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(metrics)) + "\n")

    def _save_metrics(self):
        """Persist aggregate metrics to disk."""
        with self.metrics_file.open("w", encoding="utf-8") as f:
            json.dump(asdict(self.aggregate), f, indent=2)

    def _load_metrics(self):
        """Load existing metrics from disk."""
        if self.metrics_file.exists():
            try:
                with self.metrics_file.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.aggregate = AggregateMetrics(**data)
                logger.info(f"Loaded existing metrics: {self.aggregate.total_queries} total queries")
            except Exception as e:
                logger.warning(f"Failed to load metrics: {e}")

    def health_check(self) -> Dict[str, Any]:
        """
        Perform health check.

        Returns:
            Health status with metrics
        """
        return {
            "status": "healthy",
            "total_queries": self.aggregate.total_queries,
            "cache_hit_rate": f"{self.aggregate.cache_hit_rate * 100:.1f}%",
            "avg_latency_ms": f"{self.aggregate.avg_latency_ms:.1f}",
            "p95_latency_ms": f"{self.aggregate.p95_latency_ms:.1f}",
            "error_rate": f"{(self.aggregate.failed_queries / max(self.aggregate.total_queries, 1)) * 100:.1f}%",
            "uptime": "operational"
        }
