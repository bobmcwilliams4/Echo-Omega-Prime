"""
P05 Creditor Claim Engine - Telemetry Module
Comprehensive query tracing, latency tracking, error domains for creditor claim analysis
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict, deque
from dataclasses import dataclass, field, asdict
import json
from enum import Enum
from loguru import logger
import hashlib


class ClaimCategory(str, Enum):
    """Creditor claim categories"""
    SECURED = "SECURED_CLAIMS"
    UNSECURED = "UNSECURED_CLAIMS"
    PRIORITY = "PRIORITY_CLAIMS"
    ADMINISTRATION = "ADMINISTRATION_EXPENSES"
    FUNERAL = "FUNERAL_EXPENSES"
    LAST_ILLNESS = "LAST_ILLNESS"
    FAMILY_ALLOWANCE = "FAMILY_ALLOWANCE"
    EXEMPT_PROPERTY = "EXEMPT_PROPERTY"
    MATURED = "MATURED_CLAIMS"
    CONTINGENT = "CONTINGENT_CLAIMS"
    FEDERAL_TAX = "FEDERAL_TAX"
    HOMESTEAD = "HOMESTEAD"
    REJECTED = "REJECTED_CLAIMS"


class QueryZone(str, Enum):
    """Analysis zones for creditor claims"""
    CLASSIFICATION = "claim_classification"
    PRIORITY = "priority_determination"
    SOL = "statute_of_limitations"
    EXEMPTIONS = "exempt_property_analysis"
    PROCEDURES = "filing_procedures"
    SECURED_RIGHTS = "secured_creditor_rights"


class ErrorDomain(str, Enum):
    """Creditor claim error domains"""
    MISSING_NOTICE = "missing_notice_to_creditors"
    LATE_FILING = "late_claim_filing"
    INSUFFICIENT_DETAIL = "insufficient_claim_detail"
    IMPROPER_VERIFICATION = "improper_verification"
    EXEMPTION_CONFLICT = "exemption_claim_conflict"
    PRIORITY_AMBIGUITY = "priority_classification_ambiguity"
    SECURED_ELECTION = "secured_creditor_election_error"
    CONTINGENT_VALUATION = "contingent_claim_valuation"


@dataclass
class QueryMetrics:
    """Metrics for a single creditor claim query"""
    query_id: str
    timestamp: datetime
    query_text: str
    claim_category: Optional[ClaimCategory]
    zone: QueryZone
    mode: str

    # Timing
    total_latency_ms: float
    cache_latency_ms: float
    semantic_latency_ms: float
    deep_analysis_latency_ms: float

    # Results
    cache_hit: bool
    doctrines_triggered: List[str]
    confidence_level: str
    response_length: int

    # Quality
    authority_sources: int
    citations_count: int
    fact_fragility_score: float
    epistemic_warnings: int

    # Errors
    errors: List[str] = field(default_factory=list)
    error_domain: Optional[ErrorDomain] = None

    # Hash
    determinism_hash: str = ""


@dataclass
class DoctrineCoverage:
    """Track which doctrines are being used"""
    doctrine_id: str
    topic: str
    trigger_count: int = 0
    last_triggered: Optional[datetime] = None
    avg_confidence: float = 0.0
    queries_list: List[str] = field(default_factory=list)


@dataclass
class PerformanceSnapshot:
    """Performance metrics snapshot"""
    timestamp: datetime
    queries_last_hour: int
    avg_latency_ms: float
    cache_hit_rate: float
    error_rate: float

    # By category
    secured_claims_count: int
    unsecured_claims_count: int
    priority_claims_count: int
    exemption_queries_count: int

    # By zone
    classification_queries: int
    priority_queries: int
    sol_queries: int
    procedure_queries: int

    # Quality
    avg_confidence: float
    avg_authority_sources: float
    epistemic_warning_rate: float


class CreditorClaimTelemetry:
    """Comprehensive telemetry for creditor claim analysis engine"""

    def __init__(self, engine_id: str = "P05_creditor_claim"):
        self.engine_id = engine_id
        self.queries: deque = deque(maxlen=10000)
        self.doctrine_coverage: Dict[str, DoctrineCoverage] = {}
        self.error_log: deque = deque(maxlen=1000)
        self.performance_snapshots: deque = deque(maxlen=288)  # 24 hours at 5-min intervals

        # Real-time counters
        self.total_queries = 0
        self.cache_hits = 0
        self.cache_misses = 0
        self.errors_total = 0

        # Category counters
        self.category_counts: Dict[str, int] = defaultdict(int)
        self.zone_counts: Dict[str, int] = defaultdict(int)
        self.error_domain_counts: Dict[str, int] = defaultdict(int)

        # Latency tracking
        self.latencies: deque = deque(maxlen=1000)

        # Audit trail
        self.audit_path = Path("O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/P05_creditor_claim/audit_trail.jsonl")
        self.audit_path.parent.mkdir(parents=True, exist_ok=True)

        logger.info(f"Creditor claim telemetry initialized for {engine_id}")

    def record_query(self, metrics: QueryMetrics) -> None:
        """Record a query with full metrics"""
        self.queries.append(metrics)
        self.total_queries += 1

        if metrics.cache_hit:
            self.cache_hits += 1
        else:
            self.cache_misses += 1

        if metrics.errors:
            self.errors_total += len(metrics.errors)
            if metrics.error_domain:
                self.error_domain_counts[metrics.error_domain.value] += 1

        if metrics.claim_category:
            self.category_counts[metrics.claim_category.value] += 1

        self.zone_counts[metrics.zone.value] += 1
        self.latencies.append(metrics.total_latency_ms)

        # Update doctrine coverage
        for doctrine_id in metrics.doctrines_triggered:
            if doctrine_id not in self.doctrine_coverage:
                self.doctrine_coverage[doctrine_id] = DoctrineCoverage(
                    doctrine_id=doctrine_id,
                    topic=doctrine_id.replace("_", " ").title()
                )

            cov = self.doctrine_coverage[doctrine_id]
            cov.trigger_count += 1
            cov.last_triggered = metrics.timestamp
            cov.queries_list.append(metrics.query_id)

            # Update rolling average confidence
            if cov.trigger_count == 1:
                cov.avg_confidence = self._confidence_to_float(metrics.confidence_level)
            else:
                current_conf = self._confidence_to_float(metrics.confidence_level)
                cov.avg_confidence = (cov.avg_confidence * (cov.trigger_count - 1) + current_conf) / cov.trigger_count

        # Audit trail (append-only)
        self._append_audit(metrics)

        logger.debug(
            f"Query recorded: {metrics.query_id} | "
            f"Category: {metrics.claim_category} | "
            f"Zone: {metrics.zone} | "
            f"Latency: {metrics.total_latency_ms:.1f}ms | "
            f"Cache: {'HIT' if metrics.cache_hit else 'MISS'}"
        )

    def record_error(self, error_msg: str, error_domain: ErrorDomain, context: Dict[str, Any]) -> None:
        """Record an error with domain classification"""
        error_record = {
            "timestamp": datetime.now().isoformat(),
            "error": error_msg,
            "domain": error_domain.value,
            "context": context
        }
        self.error_log.append(error_record)
        self.error_domain_counts[error_domain.value] += 1

        logger.warning(f"Error recorded: {error_domain.value} - {error_msg}")

    def snapshot_performance(self) -> PerformanceSnapshot:
        """Create a performance snapshot"""
        now = datetime.now()
        hour_ago = now - timedelta(hours=1)

        recent_queries = [q for q in self.queries if q.timestamp >= hour_ago]

        snapshot = PerformanceSnapshot(
            timestamp=now,
            queries_last_hour=len(recent_queries),
            avg_latency_ms=sum(self.latencies) / len(self.latencies) if self.latencies else 0.0,
            cache_hit_rate=self.cache_hits / max(self.total_queries, 1),
            error_rate=self.errors_total / max(self.total_queries, 1),
            secured_claims_count=self.category_counts[ClaimCategory.SECURED.value],
            unsecured_claims_count=self.category_counts[ClaimCategory.UNSECURED.value],
            priority_claims_count=self.category_counts[ClaimCategory.PRIORITY.value],
            exemption_queries_count=self.category_counts[ClaimCategory.EXEMPT_PROPERTY.value],
            classification_queries=self.zone_counts[QueryZone.CLASSIFICATION.value],
            priority_queries=self.zone_counts[QueryZone.PRIORITY.value],
            sol_queries=self.zone_counts[QueryZone.SOL.value],
            procedure_queries=self.zone_counts[QueryZone.PROCEDURES.value],
            avg_confidence=sum(self._confidence_to_float(q.confidence_level) for q in recent_queries) / max(len(recent_queries), 1),
            avg_authority_sources=sum(q.authority_sources for q in recent_queries) / max(len(recent_queries), 1),
            epistemic_warning_rate=sum(q.epistemic_warnings for q in recent_queries) / max(len(recent_queries), 1)
        )

        self.performance_snapshots.append(snapshot)
        return snapshot

    def get_doctrine_coverage_report(self) -> Dict[str, Any]:
        """Generate doctrine coverage report"""
        total_doctrines = len(self.doctrine_coverage)
        triggered_doctrines = sum(1 for cov in self.doctrine_coverage.values() if cov.trigger_count > 0)

        top_doctrines = sorted(
            self.doctrine_coverage.values(),
            key=lambda x: x.trigger_count,
            reverse=True
        )[:10]

        unused_doctrines = [
            cov.doctrine_id for cov in self.doctrine_coverage.values()
            if cov.trigger_count == 0
        ]

        return {
            "total_doctrines": total_doctrines,
            "triggered_doctrines": triggered_doctrines,
            "coverage_rate": triggered_doctrines / max(total_doctrines, 1),
            "top_10_doctrines": [
                {
                    "doctrine_id": cov.doctrine_id,
                    "topic": cov.topic,
                    "trigger_count": cov.trigger_count,
                    "avg_confidence": round(cov.avg_confidence, 3),
                    "last_triggered": cov.last_triggered.isoformat() if cov.last_triggered else None
                }
                for cov in top_doctrines
            ],
            "unused_doctrines": unused_doctrines[:20],
            "unused_count": len(unused_doctrines)
        }

    def get_error_analysis(self) -> Dict[str, Any]:
        """Analyze error patterns"""
        if not self.error_log:
            return {"total_errors": 0, "domains": {}}

        domain_breakdown = {
            domain: count
            for domain, count in self.error_domain_counts.items()
        }

        recent_errors = list(self.error_log)[-10:]

        return {
            "total_errors": len(self.error_log),
            "error_rate": self.errors_total / max(self.total_queries, 1),
            "domain_breakdown": domain_breakdown,
            "most_common_domain": max(domain_breakdown.items(), key=lambda x: x[1])[0] if domain_breakdown else None,
            "recent_errors": recent_errors
        }

    def get_health_metrics(self) -> Dict[str, Any]:
        """Get comprehensive health metrics"""
        snapshot = self.snapshot_performance()
        coverage = self.get_doctrine_coverage_report()
        errors = self.get_error_analysis()

        return {
            "engine_id": self.engine_id,
            "timestamp": datetime.now().isoformat(),
            "status": self._determine_health_status(snapshot, errors),
            "performance": asdict(snapshot),
            "doctrine_coverage": coverage,
            "error_analysis": errors,
            "total_queries": self.total_queries,
            "cache_hit_rate": self.cache_hits / max(self.total_queries, 1),
            "avg_latency_ms": sum(self.latencies) / len(self.latencies) if self.latencies else 0.0
        }

    def _append_audit(self, metrics: QueryMetrics) -> None:
        """Append query to audit trail (JSONL)"""
        try:
            with self.audit_path.open("a", encoding="utf-8") as f:
                audit_record = {
                    "query_id": metrics.query_id,
                    "timestamp": metrics.timestamp.isoformat(),
                    "query_text": metrics.query_text,
                    "claim_category": metrics.claim_category.value if metrics.claim_category else None,
                    "zone": metrics.zone.value,
                    "mode": metrics.mode,
                    "latency_ms": metrics.total_latency_ms,
                    "cache_hit": metrics.cache_hit,
                    "doctrines": metrics.doctrines_triggered,
                    "confidence": metrics.confidence_level,
                    "hash": metrics.determinism_hash
                }
                f.write(json.dumps(audit_record) + "\n")
        except Exception as e:
            logger.error(f"Failed to append audit trail: {e}")

    def _confidence_to_float(self, confidence_level: str) -> float:
        """Convert confidence level to float for averaging"""
        mapping = {
            "DEFENSIBLE": 0.95,
            "AGGRESSIVE": 0.75,
            "DISCLOSURE": 0.60,
            "HIGH_RISK": 0.40
        }
        return mapping.get(confidence_level, 0.5)

    def _determine_health_status(self, snapshot: PerformanceSnapshot, errors: Dict[str, Any]) -> str:
        """Determine overall health status"""
        if errors["error_rate"] > 0.15:
            return "CRITICAL"
        if snapshot.avg_latency_ms > 500:
            return "DEGRADED"
        if snapshot.cache_hit_rate < 0.5:
            return "WARNING"
        return "HEALTHY"


def create_query_id(query_text: str, timestamp: datetime) -> str:
    """Generate deterministic query ID"""
    content = f"{query_text}_{timestamp.isoformat()}"
    return hashlib.sha256(content.encode()).hexdigest()[:16]
