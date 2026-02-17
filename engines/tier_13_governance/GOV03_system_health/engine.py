"""
GOV03 System Health Monitor Engine v1.0.0
Port: 8893
TIE-20 Compliant | ECHO OMEGA PRIME Governance Tier

Monitors health of all engines, cloud workers, local services, and infrastructure.
Aggregates status, tracks latency, detects cascade failures, provides dashboard data.

TIE-20 Components:
  1. three_layer_response    2. response_modes       3. doctrine_cache
  4. authority_hardening     5. confidence_strat      6. semantic_normalization
  7. vector_search           8. telemetry             9. drift_watcher
 10. coverage_map           11. metrics_collector    12. health_endpoint
 13. zoned_analysis         14. fact_fragility       15. audit_trail_jsonl
 16. determinism_hash_sha256 17. fastapi_server      18. loguru_logging
 19. multi_doctrine_decomp  20. deep_analysis_mode
"""

import asyncio
import hashlib
import json
import math
import os
import sys
import time
import uuid
from collections import defaultdict, deque
from datetime import datetime, timedelta, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Optional

import httpx
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import BaseModel, Field

# ── Path Setup ──────────────────────────────────────────────────────────────
ENGINE_DIR = Path(__file__).parent
ENGINES_ROOT = ENGINE_DIR.parent
sys.path.insert(0, str(ENGINES_ROOT / "_shared"))

try:
    from cloud_retriever import CognitionCloudRetriever
    CLOUD_AVAILABLE = True
except ImportError:
    CLOUD_AVAILABLE = False

# ── Logging ─────────────────────────────────────────────────────────────────
LOG_DIR = ENGINE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)
logger.remove()
logger.add(sys.stderr, level="INFO", format="{time:HH:mm:ss} | {level:<7} | {message}")
logger.add(LOG_DIR / "gov03_{time}.log", rotation="50 MB", compression="gz", retention="30 days")

# ── Constants ───────────────────────────────────────────────────────────────
ENGINE_ID = "GOV03"
ENGINE_NAME = "System Health Monitor"
ENGINE_VERSION = "1.0.0"
PORT = 8893
HEALTH_CHECK_TIMEOUT = 5.0
DEFAULT_POLL_INTERVAL = 30
MAX_HISTORY_ENTRIES = 10000
LATENCY_WINDOW = 100
DOCTRINE_CACHE_PATH = ENGINE_DIR / "doctrine_cache.json"
SEMANTIC_DICT_PATH = ENGINE_DIR / "semantic_dict.json"
COVERAGE_MAP_PATH = ENGINE_DIR / "coverage_map.json"
CONSECUTIVE_FAILURES_DOWN = 3
FLAPPING_WINDOW_SECONDS = 600
FLAPPING_THRESHOLD = 5
FLAPPING_EXIT_SUCCESSES = 5
INCIDENT_ESCALATION_MINUTES = 30
MAX_CRASH_PER_HOUR = 3
MAINTENANCE_GRACE_MINUTES = 15
CAPACITY_FORECAST_SAMPLES = 168
CAPACITY_WARNING_DAYS = 14
RESOURCE_BUFFER_SIZE = 720

# ── Enums ───────────────────────────────────────────────────────────────────

class ServiceStatus(str, Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"
    CIRCUIT_OPEN = "circuit_open"

class AlertSeverity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

class ServiceType(str, Enum):
    ENGINE = "engine"
    WORKER = "worker"
    LOCAL_SERVICE = "local_service"
    CLOUD_WORKER = "cloud_worker"
    DATABASE = "database"
    QUEUE = "queue"

class ResponseMode(str, Enum):
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"

class AnalysisZone(str, Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"

class ConfidenceLevel(str, Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"

class IncidentStage(str, Enum):
    DETECTED = "DETECTED"
    CLASSIFIED = "CLASSIFIED"
    NOTIFIED = "NOTIFIED"
    MITIGATING = "MITIGATING"
    RESOLVED = "RESOLVED"
    REVIEWED = "REVIEWED"

class RemediationTier(str, Enum):
    TIER1_SINGLE_RESTART = "TIER1_SINGLE_RESTART"
    TIER2_CASCADE_RESTART = "TIER2_CASCADE_RESTART"
    TIER3_SYSTEM_RESTART = "TIER3_SYSTEM_RESTART"

# ── Pydantic Models ─────────────────────────────────────────────────────────

class ServiceDefinition(BaseModel):
    service_id: str
    name: str
    service_type: ServiceType
    url: str
    port: Optional[int] = None
    health_path: str = "/health"
    dependencies: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    expected_latency_ms: float = 500.0
    critical: bool = False

class HealthCheckResult(BaseModel):
    service_id: str
    status: ServiceStatus
    latency_ms: float
    timestamp: str
    response_code: Optional[int] = None
    details: dict[str, Any] = Field(default_factory=dict)
    error: Optional[str] = None

class ServiceRecord(BaseModel):
    definition: ServiceDefinition
    current_status: ServiceStatus = ServiceStatus.UNKNOWN
    last_check: Optional[str] = None
    last_healthy: Optional[str] = None
    consecutive_failures: int = 0
    circuit_breaker_open: bool = False
    circuit_breaker_opened_at: Optional[str] = None
    uptime_checks: int = 0
    uptime_successes: int = 0
    latency_history: list[float] = Field(default_factory=list)
    error_history: list[str] = Field(default_factory=list)

class AlertRecord(BaseModel):
    alert_id: str
    severity: AlertSeverity
    service_id: str
    message: str
    timestamp: str
    acknowledged: bool = False
    resolved: bool = False
    resolved_at: Optional[str] = None

class SystemSnapshot(BaseModel):
    timestamp: str
    total_services: int
    healthy: int
    degraded: int
    unhealthy: int
    unknown: int
    circuit_open: int
    avg_latency_ms: float
    active_alerts: int
    uptime_pct: float

class QueryRequest(BaseModel):
    query: str
    mode: ResponseMode = ResponseMode.FAST
    zone: AnalysisZone = AnalysisZone.REPORTING
    include_cloud: bool = True

class QueryResponse(BaseModel):
    engine_id: str = ENGINE_ID
    query: str
    mode: ResponseMode
    zone: AnalysisZone
    response: dict[str, Any]
    confidence: ConfidenceLevel
    determinism_hash: str
    latency_ms: float
    timestamp: str
    sources: list[str] = Field(default_factory=list)

class RegisterRequest(BaseModel):
    service_id: str
    name: str
    service_type: ServiceType
    url: str
    port: Optional[int] = None
    health_path: str = "/health"
    dependencies: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    expected_latency_ms: float = 500.0
    critical: bool = False

class IncidentRecord(BaseModel):
    incident_id: str = Field(default_factory=lambda: f"INC-{uuid.uuid4().hex[:8].upper()}")
    service_id: str
    stage: IncidentStage = IncidentStage.DETECTED
    severity: AlertSeverity = AlertSeverity.HIGH
    failure_mode: str = "unknown"
    description: str = ""
    detected_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    classified_at: Optional[str] = None
    resolved_at: Optional[str] = None
    recommended_action: str = ""
    remediation_tier: Optional[RemediationTier] = None
    auto_approved: bool = False
    escalated: bool = False
    notes: list[str] = Field(default_factory=list)

class MaintenanceWindow(BaseModel):
    window_id: str = Field(default_factory=lambda: f"MW-{uuid.uuid4().hex[:8].upper()}")
    service_id: str
    start_time: str
    duration_minutes: int
    reason: str
    declared_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    active: bool = False
    completed: bool = False

class CapacityForecast(BaseModel):
    service_id: str
    metric_name: str
    current_value: float
    slope_per_hour: float
    r_squared: float
    threshold_value: float
    projected_exhaustion: Optional[str] = None
    days_until_exhaustion: Optional[float] = None
    trend_direction: str = "stable"

# ── Doctrine Cache ──────────────────────────────────────────────────────────

class DoctrineBlock:
    def __init__(self, topic: str, keywords: list[str], conclusion: str,
                 reasoning: str, key_factors: list[str], authority: list[str],
                 confidence: ConfidenceLevel = ConfidenceLevel.DEFENSIBLE):
        self.topic = topic
        self.keywords = keywords
        self.conclusion = conclusion
        self.reasoning = reasoning
        self.key_factors = key_factors
        self.authority = authority
        self.confidence = confidence
        self.hit_count = 0
        self.last_hit = None

DOCTRINE_CACHE: list[DoctrineBlock] = [
    DoctrineBlock(
        topic="health_check_patterns",
        keywords=["health", "check", "probe", "liveness", "readiness"],
        conclusion="Health checks should distinguish between liveness (process alive) and readiness (can serve traffic). Kubernetes-style probes provide the gold standard: liveness prevents zombie processes, readiness prevents premature traffic routing.",
        reasoning="A service can be alive but not ready (still warming caches, loading models, connecting to databases). Conflating the two leads to either premature traffic (crashes) or unnecessary restarts (liveness killing slow starters). Separate endpoints allow orchestrators to make nuanced decisions.",
        key_factors=["liveness vs readiness separation", "startup probe for slow initializers", "dependency health inclusion", "degraded vs down distinction", "health check caching to prevent thundering herd"],
        authority=["Kubernetes Health Check Best Practices", "Google SRE Book Ch.6", "AWS Well-Architected Reliability Pillar"],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),
    DoctrineBlock(
        topic="circuit_breaker_pattern",
        keywords=["circuit", "breaker", "failfast", "cascade", "failure"],
        conclusion="Circuit breakers prevent cascade failures by failing fast when a downstream service is unhealthy. The three states (CLOSED, OPEN, HALF-OPEN) provide automatic recovery without manual intervention. Threshold should be 5 consecutive failures or 50% error rate in a 60-second window.",
        reasoning="Without circuit breakers, a single failing service can exhaust connection pools, thread pools, and memory across all upstream callers. The pattern bounds failure impact: OPEN state returns instant errors (no resource consumption), HALF-OPEN allows periodic probes to detect recovery. Hystrix popularized the pattern; Resilience4j and Polly provide modern implementations.",
        key_factors=["failure threshold configuration", "half-open probe interval", "fallback response strategy", "per-service circuit isolation", "monitoring circuit state transitions"],
        authority=["Martin Fowler - Circuit Breaker", "Netflix Hystrix", "Microsoft - Circuit Breaker Pattern", "Release It! by Michael Nygard"],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),
    DoctrineBlock(
        topic="golden_signals",
        keywords=["golden", "signals", "latency", "traffic", "errors", "saturation", "SRE"],
        conclusion="Google's four golden signals — latency, traffic, errors, saturation — provide the minimum viable monitoring for any service. Latency should track P50/P95/P99 separately; error rate should distinguish client (4xx) from server (5xx) errors; saturation should measure against known limits.",
        reasoning="The golden signals were distilled from decades of Google SRE experience as the minimum set of metrics that, if monitored correctly, will catch virtually all production issues. USE method (Utilization, Saturation, Errors) and RED method (Rate, Errors, Duration) are complementary but golden signals remain the foundation for system health monitoring.",
        key_factors=["latency percentile tracking not averages", "traffic baseline for anomaly detection", "error budget calculation", "saturation capacity limits", "correlation across signals"],
        authority=["Google SRE Book Ch.6 - Monitoring Distributed Systems", "Brendan Gregg - USE Method", "Tom Wilkie - RED Method"],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),
    DoctrineBlock(
        topic="distributed_systems_observability",
        keywords=["observability", "tracing", "metrics", "logs", "three", "pillars"],
        conclusion="The three pillars of observability — metrics, logs, traces — serve distinct purposes. Metrics for alerting and dashboards (aggregated, cheap to store), logs for debugging specific events (detailed, expensive), traces for understanding request flow across services (correlated, moderate cost).",
        reasoning="Observability is not monitoring — monitoring tells you WHEN something is wrong, observability tells you WHY. Structured logging with correlation IDs enables log aggregation. Distributed tracing with OpenTelemetry provides end-to-end request visibility. Metrics with Prometheus-style labels enable flexible querying.",
        key_factors=["correlation ID propagation", "structured log format", "trace sampling strategy", "metric cardinality management", "alert-metric-log-trace linkage"],
        authority=["Distributed Systems Observability by Cindy Sridharan", "OpenTelemetry Specification", "Prometheus Best Practices"],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),
    DoctrineBlock(
        topic="error_budgets",
        keywords=["error", "budget", "SLO", "SLA", "reliability", "objective"],
        conclusion="Error budgets quantify acceptable unreliability. A 99.9% SLO allows 43.8 minutes of downtime per month. When budget is exhausted, freeze deployments and focus on reliability. This creates a natural balance between feature velocity and stability.",
        reasoning="Without error budgets, reliability is a qualitative judgment ('is it reliable enough?'). SLOs make it quantitative. The budget approach creates alignment: product teams want to ship fast (spend budget), reliability teams want stability (save budget). The budget is the negotiation mechanism.",
        key_factors=["SLO definition per service tier", "budget consumption tracking", "deployment freeze triggers", "burn rate alerting", "multi-window burn rate"],
        authority=["Google SRE Workbook - Implementing SLOs", "The Art of SLOs - Google Cloud", "Sloth SLO Generator"],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),
    DoctrineBlock(
        topic="alert_fatigue_prevention",
        keywords=["alert", "fatigue", "noise", "actionable", "paging", "oncall"],
        conclusion="Alert fatigue is the #1 killer of incident response effectiveness. Every alert must be actionable, urgent, and require human judgment. Automate everything that can be automated. Target: every page should result in a human taking a meaningful action.",
        reasoning="PagerDuty research shows teams with >100 alerts/week have 3x slower MTTR than teams with <20. Non-actionable alerts train on-call engineers to ignore pages. The remedy: ruthlessly eliminate informational alerts (use dashboards instead), deduplicate related alerts, and implement alert routing based on service ownership.",
        key_factors=["actionability requirement for every alert", "alert deduplication and grouping", "severity level discipline", "alert review and pruning cadence", "escalation path clarity"],
        authority=["PagerDuty Incident Response Guide", "Google SRE Book Ch.11 - Being On-Call", "Rob Ewaschuk - My Philosophy on Alerting"],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),
    DoctrineBlock(
        topic="capacity_planning",
        keywords=["capacity", "planning", "scaling", "resource", "forecast", "growth"],
        conclusion="Capacity planning requires three inputs: current utilization, growth rate, and lead time for new capacity. Plan for 18 months ahead with quarterly reviews. Reserve 30% headroom for unexpected spikes. Organic growth is predictable; viral growth is not — maintain burst capacity.",
        reasoning="Undercapacity causes outages; overcapacity wastes money. The sweet spot requires understanding both organic growth (linear, predictable from historical data) and inorganic events (launches, marketing campaigns, viral moments). Cloud autoscaling helps but has latency — pre-scaling for known events is essential.",
        key_factors=["utilization baseline measurement", "growth rate extrapolation", "seasonal pattern recognition", "burst capacity reserves", "cost optimization vs reliability tradeoff"],
        authority=["Google SRE Book Ch.18 - Software Engineering in SRE", "AWS Well-Architected Cost Optimization", "Capacity Planning by John Allspaw"],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),
    DoctrineBlock(
        topic="dependency_management",
        keywords=["dependency", "coupling", "cascade", "blast", "radius", "isolation"],
        conclusion="Service dependencies create failure propagation paths. Map all dependencies (sync and async), identify critical paths, and ensure no single dependency failure can take down the entire system. Use timeouts, retries with backoff, and circuit breakers on every cross-service call.",
        reasoning="Distributed systems fail in distributed ways. A dependency graph reveals the blast radius of any single service failure. Critical path analysis identifies which dependencies must be highly available vs which can be degraded gracefully. Async dependencies (via queues) are inherently more resilient than sync (HTTP/RPC).",
        key_factors=["dependency graph visualization", "critical path identification", "sync vs async dependency classification", "timeout and retry configuration", "graceful degradation strategies"],
        authority=["Release It! by Michael Nygard", "Building Microservices by Sam Newman", "Netflix Chaos Engineering"],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),
    DoctrineBlock(
        topic="incident_classification",
        keywords=["incident", "severity", "classification", "SEV", "priority", "triage"],
        conclusion="Incident severity should be based on user impact, not root cause. SEV1: widespread user-facing outage. SEV2: significant degradation or partial outage. SEV3: minor impact, workaround available. SEV4: no user impact, internal only. Auto-classify based on golden signals thresholds.",
        reasoning="Consistent severity classification enables appropriate response. Over-classifying (everything is SEV1) causes fatigue; under-classifying causes slow response. The key insight: classify by impact FIRST, investigate cause AFTER. This ensures appropriate urgency regardless of whether the cause is 'trivial'.",
        key_factors=["user impact as primary classifier", "automatic severity from metrics thresholds", "escalation criteria per severity", "communication cadence per severity", "post-incident review threshold"],
        authority=["PagerDuty Incident Response", "Atlassian Incident Management", "Google SRE Book Ch.14"],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),
    DoctrineBlock(
        topic="chaos_engineering",
        keywords=["chaos", "engineering", "resilience", "failure", "injection", "gameday"],
        conclusion="Chaos engineering proactively injects failures to verify system resilience. Start with steady-state hypothesis, inject failure, observe. Begin with known failure modes (network partition, service crash), graduate to novel ones (clock skew, disk full). Always have a kill switch.",
        reasoning="Systems are too complex to reason about theoretically. The only way to verify resilience is to test it in production (or production-like environments). Netflix's Chaos Monkey philosophy: if your system can't handle a single instance failure, you'll discover it at 3 AM on a Saturday.",
        key_factors=["steady-state hypothesis definition", "blast radius containment", "kill switch mechanism", "gradual scope expansion", "failure mode catalog"],
        authority=["Chaos Engineering by Casey Rosenthal", "Netflix Chaos Monkey", "Gremlin - Chaos Engineering Platform"],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),
    DoctrineBlock(
        topic="service_mesh_monitoring",
        keywords=["service", "mesh", "sidecar", "proxy", "istio", "envoy", "traffic"],
        conclusion="Service meshes provide infrastructure-level observability without application code changes. Sidecar proxies capture all inter-service traffic, enabling automatic latency tracking, error rate monitoring, and traffic visualization. Essential for systems with 50+ microservices.",
        reasoning="As service count grows, instrumenting each service individually becomes unsustainable. Service meshes (Istio, Linkerd) inject sidecar proxies that transparently capture traffic metrics. This provides a consistent observability baseline while allowing services to add custom metrics on top.",
        key_factors=["sidecar resource overhead", "mTLS certificate rotation", "traffic policy enforcement", "canary traffic routing", "distributed tracing integration"],
        authority=["Istio Documentation", "Linkerd Best Practices", "CNCF Service Mesh Interface"],
        confidence=ConfidenceLevel.AGGRESSIVE
    ),
    DoctrineBlock(
        topic="runbook_automation",
        keywords=["runbook", "automation", "remediation", "self-healing", "auto-remediate"],
        conclusion="Every alert should have a runbook. Every runbook that can be automated, should be. Self-healing systems reduce MTTR from minutes to seconds. Start with the most common incidents: restart crashed services, clear full disks, rotate expired certificates.",
        reasoning="Human responders add latency (wake up, context switch, diagnose, act). Automated remediation removes this latency for known failure modes. The hierarchy: auto-remediate (best), runbook-guided (good), tribal knowledge (bad), no runbook (worst). Track remediation automation percentage as a key SRE metric.",
        key_factors=["runbook coverage percentage", "automation candidates by frequency", "safety checks before auto-remediation", "audit trail for automated actions", "human escalation triggers"],
        authority=["Google SRE Book Ch.12 - Effective Troubleshooting", "PagerDuty Runbook Automation", "Shoreline.io Auto-Remediation"],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),
    DoctrineBlock(
        topic="monitoring_antipatterns",
        keywords=["antipattern", "monitoring", "bad", "practice", "mistake", "wrong"],
        conclusion="Common monitoring antipatterns: (1) monitoring for monitoring's sake without actionable alerts, (2) relying on averages instead of percentiles, (3) dashboard sprawl without hierarchy, (4) alert-per-metric instead of symptom-based alerting, (5) ignoring seasonality in baselines.",
        reasoning="Bad monitoring is worse than no monitoring — it creates false confidence. Teams that monitor CPU but not user-facing errors miss real incidents. Teams that alert on every metric spike create noise that masks real signals. The fix: start from user experience, work backward to infrastructure.",
        key_factors=["symptom-based over cause-based alerting", "percentile over average metrics", "dashboard hierarchy (overview → detail)", "alert hygiene reviews", "user-centric monitoring"],
        authority=["Monitoring and Observability by James Turnbull", "Google SRE Workbook", "Charity Majors - Observability Engineering"],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),
    DoctrineBlock(
        topic="sre_toil_reduction",
        keywords=["toil", "manual", "repetitive", "automation", "SRE", "operational"],
        conclusion="Toil is manual, repetitive, automatable work that scales linearly with service growth. SRE teams should spend no more than 50% of time on toil; the rest on engineering that reduces future toil. Track toil hours and automate the highest-frequency tasks first.",
        reasoning="Toil is the enemy of scalability. If operating 10 services requires 10 hours/week of manual work, operating 100 services will require 100 hours — unsustainable. The SRE model: invest engineering time to automate toil, creating leverage that enables managing more services with the same team size.",
        key_factors=["toil measurement and tracking", "automation ROI calculation", "50% toil budget enforcement", "toil categorization (provisioning, deployment, monitoring, incident response)", "automation prioritization by frequency × time"],
        authority=["Google SRE Book Ch.5 - Eliminating Toil", "The SRE Workbook", "SRE at Scale - LinkedIn Engineering"],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),
    DoctrineBlock(
        topic="graceful_degradation",
        keywords=["graceful", "degradation", "fallback", "partial", "availability", "shed"],
        conclusion="Systems should degrade gracefully rather than fail completely. Implement load shedding (reject excess traffic), feature flags (disable non-critical features), and fallback responses (serve cached/stale data). Users prefer slow over unavailable.",
        reasoning="Binary availability (up or down) is a false dichotomy. Real systems have a spectrum of functionality that can be selectively disabled under pressure. E-commerce example: disable recommendations (nice-to-have) to preserve checkout (critical). This requires pre-planning which features are shed first.",
        key_factors=["feature criticality classification", "load shedding thresholds", "fallback response strategies", "cache serving during outages", "feature flag integration"],
        authority=["AWS Avoiding Overload", "Netflix Zuul Load Shedding", "Envoy Proxy Rate Limiting"],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),
    DoctrineBlock(
        topic="post_incident_review",
        keywords=["postmortem", "PIR", "retrospective", "blameless", "review", "RCA"],
        conclusion="Post-incident reviews must be blameless, focused on systemic improvements, and result in tracked action items. The goal is not to find WHO caused the incident but WHAT system allowed the incident to happen. Every SEV1/SEV2 should have a PIR within 5 business days.",
        reasoning="Blame-focused reviews cause engineers to hide information, reducing organizational learning. Blameless reviews create psychological safety that encourages full disclosure. The most valuable PIRs identify systemic weaknesses (missing monitoring, inadequate testing, unclear ownership) rather than individual mistakes.",
        key_factors=["blameless culture enforcement", "timeline reconstruction accuracy", "contributing factor analysis", "action item tracking to completion", "pattern detection across PIRs"],
        authority=["Etsy - Blameless Postmortems", "Google SRE Book Ch.15 - Postmortem Culture", "John Allspaw - Blameless Post-Mortems"],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),
    DoctrineBlock(
        topic="multi_region_health",
        keywords=["multi-region", "geo", "failover", "DR", "disaster", "recovery"],
        conclusion="Multi-region health monitoring must account for network partitions between regions, independent failure domains, and cross-region replication lag. Health checks should run from each region to detect regional issues. Failover decisions should be automated with human override capability.",
        reasoning="Regional failures (cloud provider outages, natural disasters, network issues) require cross-region resilience. But multi-region adds complexity: data consistency, DNS failover latency, and split-brain scenarios. Health monitoring must detect regional degradation fast enough to trigger failover before users notice.",
        key_factors=["cross-region health probing", "replication lag monitoring", "DNS failover TTL management", "split-brain detection", "regional traffic routing"],
        authority=["AWS Multi-Region Best Practices", "Google Cloud Disaster Recovery", "Azure Traffic Manager"],
        confidence=ConfidenceLevel.AGGRESSIVE
    ),
    DoctrineBlock(
        topic="container_health",
        keywords=["container", "docker", "kubernetes", "pod", "OOM", "restart"],
        conclusion="Container health monitoring extends beyond process liveness. Track: OOM kills (memory limits too tight), restart loops (CrashLoopBackOff), evictions (node pressure), image pull failures, and resource quota exhaustion. Kubernetes events are a critical but often overlooked signal source.",
        reasoning="Containers add abstraction layers that can mask issues. A pod restarting every 5 minutes might maintain 99% uptime by metrics but indicates a serious underlying issue. Container-specific metrics (restart count, resource requests vs limits, scheduling delays) are essential for understanding container health.",
        key_factors=["OOM kill detection and alerting", "restart loop detection", "resource request/limit tuning", "eviction monitoring", "scheduling delay tracking"],
        authority=["Kubernetes Production Best Practices", "Docker Health Check Documentation", "Prometheus Kubernetes Monitoring"],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),
    DoctrineBlock(
        topic="database_health_monitoring",
        keywords=["database", "DB", "query", "connection", "pool", "replication", "lag"],
        conclusion="Database health monitoring must track: connection pool utilization, query latency percentiles, replication lag, lock contention, table bloat, and storage growth rate. A database at 80% connection pool is an emergency — at 100% the entire application stops.",
        reasoning="Databases are typically the hardest component to scale and the most impactful when they fail. Connection pool exhaustion is the most common database-related outage cause. Replication lag causes stale reads. Lock contention causes cascading slowdowns. Proactive monitoring of these metrics prevents outages.",
        key_factors=["connection pool utilization alerting at 70%", "slow query log analysis", "replication lag thresholds", "lock wait timeout monitoring", "storage growth rate projection"],
        authority=["Percona Database Performance Blog", "PostgreSQL Monitoring Best Practices", "AWS RDS Performance Insights"],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),
    DoctrineBlock(
        topic="synthetic_monitoring",
        keywords=["synthetic", "monitoring", "canary", "probe", "user", "journey"],
        conclusion="Synthetic monitoring simulates real user journeys to detect issues before users report them. Run critical user flows (login, checkout, search) every 1-5 minutes from multiple locations. Synthetic checks catch issues that infrastructure metrics miss: broken deploys, third-party failures, CDN issues.",
        reasoning="Infrastructure metrics can be green while the user experience is broken (bad deploy, JS error, third-party script failure). Synthetic monitoring fills this gap by executing actual user flows. Combined with real user monitoring (RUM), it provides complete visibility.",
        key_factors=["critical user journey identification", "multi-location probing", "screenshot comparison for UI changes", "API contract validation", "SSL certificate expiry monitoring"],
        authority=["Datadog Synthetic Monitoring", "New Relic Synthetics", "Google Web Vitals"],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),
    DoctrineBlock(
        topic="cost_monitoring",
        keywords=["cost", "spending", "cloud", "billing", "budget", "optimization"],
        conclusion="Cloud cost monitoring is a health signal — unexpected cost spikes often indicate runaway processes, misconfigured autoscaling, or data pipeline issues. Set budget alerts at 80% and 100% of expected spend. Tag all resources for cost attribution.",
        reasoning="Cloud spending correlates with system behavior. A 10x cost spike usually means something is wrong (infinite loop, misconfigured autoscaler, data amplification). Cost anomaly detection catches issues that traditional monitoring misses because it operates on a different dimension of system behavior.",
        key_factors=["resource tagging for attribution", "budget alert thresholds", "cost anomaly detection", "reserved capacity optimization", "right-sizing recommendations"],
        authority=["AWS Cost Explorer", "GCP Cost Management", "FinOps Foundation"],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),
    DoctrineBlock(
        topic="log_aggregation_health",
        keywords=["log", "aggregation", "pipeline", "ingestion", "volume", "retention"],
        conclusion="Log pipeline health is meta-monitoring: monitoring your monitoring. Track log ingestion rate, parsing errors, storage utilization, and query latency. A broken log pipeline means you're flying blind during the next incident. Alert on ingestion drops > 20% from baseline.",
        reasoning="Log pipelines fail silently — services keep running, but troubleshooting capability disappears. Common failure modes: agent crash, pipeline throttling, storage full, parser misconfiguration. The worst time to discover broken logging is during an active incident.",
        key_factors=["ingestion rate baseline", "parsing error rate", "storage growth projection", "query latency tracking", "pipeline lag monitoring"],
        authority=["Elasticsearch Operations Best Practices", "Splunk Admin Guide", "Grafana Loki Best Practices"],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),
    DoctrineBlock(
        topic="security_health_signals",
        keywords=["security", "auth", "certificate", "SSL", "TLS", "vulnerability"],
        conclusion="Security health signals include: SSL certificate expiry (alert at 30, 14, 7 days), authentication failure rate spikes, API key rotation status, dependency vulnerability count, and WAF block rate. A sudden spike in auth failures may indicate a credential stuffing attack.",
        reasoning="Security incidents manifest as health anomalies before they cause outages. Monitoring security signals alongside operational health provides early warning of attacks and misconfigurations. Certificate expiry is the most preventable outage cause yet remains one of the most common.",
        key_factors=["certificate expiry tracking", "auth failure rate anomaly detection", "API key age monitoring", "dependency CVE scanning", "WAF rule effectiveness"],
        authority=["NIST Cybersecurity Framework", "OWASP Monitoring Cheatsheet", "CIS Controls v8"],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),
    DoctrineBlock(
        topic="sla_compliance_monitoring",
        keywords=["SLA", "compliance", "uptime", "availability", "contractual", "penalty"],
        conclusion="SLA compliance monitoring must track availability from the customer's perspective, not internal metrics. Use external synthetic monitoring as the source of truth. Track burn rate: if the SLA allows 4.38 minutes of downtime per month (99.99%), consuming 50% of budget in week 1 requires immediate action.",
        reasoning="Internal metrics often overstate availability because they miss edge cases (DNS issues, CDN failures, regional outages). SLA compliance should be measured as close to the customer as possible. Multi-window burn rate alerting catches both sudden outages and slow degradation.",
        key_factors=["external measurement as truth source", "burn rate calculation and alerting", "SLA tiering by customer segment", "penalty calculation automation", "proactive customer communication"],
        authority=["Google SRE Workbook - SLOs", "AWS Service Level Agreements", "Datadog SLO Tracking"],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),
    DoctrineBlock(
        topic="network_health_monitoring",
        keywords=["network", "DNS", "latency", "packet", "loss", "bandwidth", "connectivity"],
        conclusion="Network health monitoring should track: DNS resolution time, inter-service latency, packet loss rate, bandwidth utilization, and connection establishment time. Network issues are the most common yet hardest to diagnose cause of distributed system failures.",
        reasoning="Network failures are often partial — affecting some connections but not others, some regions but not others, some protocols but not others. This makes them hard to detect with simple health checks. Continuous network monitoring with baselining catches subtle degradation before it causes visible impact.",
        key_factors=["DNS resolution monitoring", "inter-AZ latency tracking", "packet loss detection", "bandwidth utilization alerting", "TCP retransmission rate"],
        authority=["Cloudflare Network Intelligence", "AWS VPC Flow Logs", "LinkedIn Netperf"],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),
]

# ── File-Based Doctrine Loader ──────────────────────────────────────────────

def _load_file_doctrines() -> list[DoctrineBlock]:
    """Load additional doctrine blocks from doctrine_cache.json."""
    if not DOCTRINE_CACHE_PATH.exists():
        logger.warning(f"doctrine_cache.json not found at {DOCTRINE_CACHE_PATH}")
        return []
    try:
        data = json.loads(DOCTRINE_CACHE_PATH.read_text(encoding="utf-8"))
        blocks = []
        for d in data.get("doctrines", []):
            blocks.append(DoctrineBlock(
                topic=d["topic"],
                keywords=d["keywords"],
                conclusion=d.get("conclusion_template", ""),
                reasoning=d.get("reasoning_framework", ""),
                key_factors=d.get("key_factors", []),
                authority=d.get("primary_authority", []),
                confidence=ConfidenceLevel(d.get("confidence_stratification", "DEFENSIBLE")),
            ))
        logger.info(f"Loaded {len(blocks)} doctrine blocks from doctrine_cache.json")
        return blocks
    except Exception as exc:
        logger.error(f"Failed to load doctrine_cache.json: {exc}")
        return []

FILE_DOCTRINES: list[DoctrineBlock] = _load_file_doctrines()
ALL_DOCTRINES: list[DoctrineBlock] = DOCTRINE_CACHE + FILE_DOCTRINES

# ── File-Based Semantic Dict Loader ─────────────────────────────────────────

def _load_semantic_dict() -> dict[str, Any]:
    """Load semantic normalization rules from semantic_dict.json."""
    if not SEMANTIC_DICT_PATH.exists():
        logger.warning(f"semantic_dict.json not found at {SEMANTIC_DICT_PATH}")
        return {}
    try:
        data = json.loads(SEMANTIC_DICT_PATH.read_text(encoding="utf-8"))
        logger.info(f"Loaded semantic_dict.json with {len(data.get('normalization_rules', {}))} rule sets")
        return data
    except Exception as exc:
        logger.error(f"Failed to load semantic_dict.json: {exc}")
        return {}

SEMANTIC_DICT_DATA: dict[str, Any] = _load_semantic_dict()

# ── Flapping Detector ──────────────────────────────────────────────────────

class FlappingDetector:
    """Detects engines that oscillate rapidly between health states."""

    def __init__(self) -> None:
        self._state_changes: dict[str, deque[float]] = defaultdict(lambda: deque(maxlen=50))
        self._flapping: dict[str, bool] = {}
        self._consecutive_stable: dict[str, int] = defaultdict(int)

    def record_state_change(self, service_id: str) -> None:
        self._state_changes[service_id].append(time.time())
        self._consecutive_stable[service_id] = 0

    def record_stable_check(self, service_id: str) -> None:
        if self._flapping.get(service_id, False):
            self._consecutive_stable[service_id] += 1
            if self._consecutive_stable[service_id] >= FLAPPING_EXIT_SUCCESSES:
                self._flapping[service_id] = False
                logger.info(f"Service {service_id} exited FLAPPING state")

    def is_flapping(self, service_id: str) -> bool:
        cutoff = time.time() - FLAPPING_WINDOW_SECONDS
        recent = [t for t in self._state_changes.get(service_id, []) if t >= cutoff]
        if len(recent) >= FLAPPING_THRESHOLD:
            self._flapping[service_id] = True
            return True
        return self._flapping.get(service_id, False)

    def changes_in_window(self, service_id: str) -> int:
        cutoff = time.time() - FLAPPING_WINDOW_SECONDS
        return len([t for t in self._state_changes.get(service_id, []) if t >= cutoff])

# ── Incident Manager ──────────────────────────────────────────────────────

class IncidentManager:
    """Full lifecycle incident tracking from detection to resolution."""

    def __init__(self) -> None:
        self._active: dict[str, IncidentRecord] = {}
        self._resolved: deque[IncidentRecord] = deque(maxlen=5000)
        self._crash_history: dict[str, deque[float]] = defaultdict(lambda: deque(maxlen=100))

    def create_incident(self, service_id: str, failure_mode: str, description: str,
                        severity: AlertSeverity = AlertSeverity.HIGH) -> IncidentRecord:
        incident = IncidentRecord(
            service_id=service_id, failure_mode=failure_mode,
            description=description, severity=severity,
            stage=IncidentStage.CLASSIFIED,
            classified_at=datetime.now(timezone.utc).isoformat(),
        )
        self._active[incident.incident_id] = incident
        self._crash_history[service_id].append(time.time())
        logger.error(f"Incident {incident.incident_id}: {service_id} - {failure_mode}")
        return incident

    def resolve_incident(self, incident_id: str, note: str = "") -> bool:
        inc = self._active.pop(incident_id, None)
        if not inc:
            return False
        inc.stage = IncidentStage.RESOLVED
        inc.resolved_at = datetime.now(timezone.utc).isoformat()
        if note:
            inc.notes.append(f"[{datetime.now(timezone.utc).isoformat()}] {note}")
        self._resolved.append(inc)
        return True

    def recommend_remediation(self, service_id: str) -> tuple[RemediationTier, bool]:
        hour_ago = time.time() - 3600
        recent = [t for t in self._crash_history.get(service_id, []) if t >= hour_ago]
        if len(recent) >= MAX_CRASH_PER_HOUR:
            return RemediationTier.TIER2_CASCADE_RESTART, False
        return RemediationTier.TIER1_SINGLE_RESTART, True

    def get_active(self) -> list[IncidentRecord]:
        return list(self._active.values())

    def get_incident(self, incident_id: str) -> Optional[IncidentRecord]:
        return self._active.get(incident_id) or next(
            (i for i in self._resolved if i.incident_id == incident_id), None)

    def check_escalation(self) -> list[IncidentRecord]:
        escalated = []
        now = datetime.now(timezone.utc)
        for inc in self._active.values():
            if inc.escalated:
                continue
            detected = datetime.fromisoformat(inc.detected_at)
            if (now - detected).total_seconds() > INCIDENT_ESCALATION_MINUTES * 60:
                inc.escalated = True
                if inc.severity == AlertSeverity.MEDIUM:
                    inc.severity = AlertSeverity.HIGH
                elif inc.severity == AlertSeverity.HIGH:
                    inc.severity = AlertSeverity.CRITICAL
                inc.notes.append(f"[{now.isoformat()}] Auto-escalated")
                escalated.append(inc)
        return escalated

# ── Maintenance Manager ────────────────────────────────────────────────────

class MaintenanceManager:
    """Manages planned maintenance windows and SLA exclusions."""

    def __init__(self) -> None:
        self._windows: dict[str, MaintenanceWindow] = {}
        self._by_service: dict[str, list[str]] = defaultdict(list)

    def declare_window(self, service_id: str, start_time: str,
                       duration_minutes: int, reason: str) -> MaintenanceWindow:
        window = MaintenanceWindow(
            service_id=service_id, start_time=start_time,
            duration_minutes=duration_minutes, reason=reason,
        )
        self._windows[window.window_id] = window
        self._by_service[service_id].append(window.window_id)
        logger.info(f"Maintenance window {window.window_id} for {service_id}: {reason}")
        return window

    def is_in_maintenance(self, service_id: str) -> bool:
        now = datetime.now(timezone.utc)
        for wid in self._by_service.get(service_id, []):
            w = self._windows.get(wid)
            if not w or w.completed:
                continue
            try:
                start = datetime.fromisoformat(w.start_time)
                end = start + timedelta(minutes=w.duration_minutes + MAINTENANCE_GRACE_MINUTES)
                if start <= now <= end:
                    w.active = True
                    return True
                if now > end:
                    w.completed = True
                    w.active = False
            except (ValueError, TypeError):
                continue
        return False

    def active_windows(self) -> list[MaintenanceWindow]:
        return [w for w in self._windows.values() if w.active and not w.completed]

    def all_windows(self, service_id: Optional[str] = None) -> list[MaintenanceWindow]:
        if service_id:
            return [self._windows[wid] for wid in self._by_service.get(service_id, [])
                    if wid in self._windows]
        return list(self._windows.values())

# ── Capacity Forecaster ────────────────────────────────────────────────────

class CapacityForecaster:
    """Linear regression on resource time series to project exhaustion dates."""

    def __init__(self) -> None:
        self._series: dict[str, dict[str, deque[tuple[float, float]]]] = defaultdict(
            lambda: defaultdict(lambda: deque(maxlen=RESOURCE_BUFFER_SIZE)))

    def record(self, service_id: str, metric: str, value: float) -> None:
        self._series[service_id][metric].append((time.time(), value))

    def forecast(self, service_id: str, metric: str,
                 threshold: float) -> Optional[CapacityForecast]:
        data = list(self._series.get(service_id, {}).get(metric, []))
        if len(data) < 10:
            return None
        recent = data[-CAPACITY_FORECAST_SAMPLES:]
        n = len(recent)
        xs = [t for t, _ in recent]
        ys = [v for _, v in recent]
        x_base = xs[0]
        xs_norm = [(x - x_base) / 3600.0 for x in xs]
        sum_x = sum(xs_norm)
        sum_y = sum(ys)
        sum_xy = sum(x * y for x, y in zip(xs_norm, ys))
        sum_x2 = sum(x * x for x in xs_norm)
        denom = n * sum_x2 - sum_x * sum_x
        if abs(denom) < 1e-10:
            return None
        slope = (n * sum_xy - sum_x * sum_y) / denom
        intercept = (sum_y - slope * sum_x) / n
        y_mean = sum_y / n
        ss_tot = sum((y - y_mean) ** 2 for y in ys)
        ss_res = sum((y - (slope * x + intercept)) ** 2 for x, y in zip(xs_norm, ys))
        r_squared = 1.0 - (ss_res / ss_tot) if ss_tot > 0 else 0.0
        current_value = ys[-1]
        trend = "increasing" if slope > 0.01 else "decreasing" if slope < -0.01 else "stable"
        projected_exhaustion = None
        days_until = None
        if slope > 0.001 and current_value < threshold:
            hours_until = (threshold - intercept) / slope
            if hours_until > 0:
                days_until = round(hours_until / 24.0, 2)
                exhaust_time = datetime.now(timezone.utc) + timedelta(hours=hours_until)
                projected_exhaustion = exhaust_time.isoformat()
        return CapacityForecast(
            service_id=service_id, metric_name=metric,
            current_value=round(current_value, 2), slope_per_hour=round(slope, 4),
            r_squared=round(r_squared, 4), threshold_value=threshold,
            projected_exhaustion=projected_exhaustion,
            days_until_exhaustion=days_until, trend_direction=trend,
        )

# ── Uptime Tracker ─────────────────────────────────────────────────────────

class UptimeTracker:
    """Tracks per-service uptime across rolling 24h, 7d, 30d windows."""

    def __init__(self) -> None:
        self._checks: dict[str, deque[tuple[float, bool]]] = defaultdict(
            lambda: deque(maxlen=100000))

    def record_check(self, service_id: str, success: bool) -> None:
        self._checks[service_id].append((time.time(), success))

    def calculate_uptime(self, service_id: str, window_seconds: int) -> float:
        cutoff = time.time() - window_seconds
        checks = [(t, s) for t, s in self._checks.get(service_id, []) if t >= cutoff]
        if not checks:
            return 100.0
        successes = sum(1 for _, s in checks if s)
        return round((successes / len(checks)) * 100.0, 4)

# ── Semantic Normalizer ─────────────────────────────────────────────────────

class SemanticNormalizer:
    SYNONYMS: dict[str, str] = {
        "healthcheck": "health_check", "health-check": "health_check",
        "uptime": "availability", "downtime": "unavailability",
        "latency": "response_time", "response time": "response_time",
        "circuit-breaker": "circuit_breaker", "circuitbreaker": "circuit_breaker",
        "failover": "failover", "fail-over": "failover",
        "p50": "percentile_50", "p95": "percentile_95", "p99": "percentile_99",
        "mttr": "mean_time_to_recovery", "mttf": "mean_time_to_failure",
        "mttd": "mean_time_to_detect", "mtbf": "mean_time_between_failures",
        "sla": "service_level_agreement", "slo": "service_level_objective",
        "sli": "service_level_indicator", "error budget": "error_budget",
        "oncall": "on_call", "on-call": "on_call", "pagerduty": "paging_system",
        "k8s": "kubernetes", "aws": "amazon_web_services", "gcp": "google_cloud",
        "cf": "cloudflare", "cdn": "content_delivery_network",
    }

    # Merge file-based status/metric/severity terms into the synonym map
    _file_rules = SEMANTIC_DICT_DATA.get("normalization_rules", {})
    for _rule_set in _file_rules.values():
        if isinstance(_rule_set, dict):
            for _raw, _canonical in _rule_set.items():
                if isinstance(_canonical, str):
                    SYNONYMS[_raw] = _canonical

    ABBREVIATIONS: dict[str, str] = SEMANTIC_DICT_DATA.get("abbreviation_expansion", {})

    STOP_WORDS: set[str] = {"the", "a", "an", "is", "are", "was", "were", "be", "been",
                             "being", "have", "has", "had", "do", "does", "did", "will",
                             "would", "could", "should", "may", "might", "shall", "can",
                             "to", "of", "in", "for", "on", "with", "at", "by", "from",
                             "as", "into", "about", "between", "through", "after", "before"}

    def normalize(self, text: str) -> str:
        text = text.lower().strip()
        for syn, canonical in self.SYNONYMS.items():
            text = text.replace(syn, canonical)
        tokens = text.split()
        tokens = [t for t in tokens if t not in self.STOP_WORDS]
        return " ".join(tokens)

    def extract_keywords(self, text: str) -> list[str]:
        normalized = self.normalize(text)
        return [t for t in normalized.split() if len(t) > 2]

# ── Vector Search ───────────────────────────────────────────────────────────

class VectorSearchEngine:
    """TF-IDF-style vector search over doctrine blocks."""

    def __init__(self, doctrines: list[DoctrineBlock]):
        self.doctrines = doctrines
        self.idf: dict[str, float] = {}
        self._build_index()

    def _build_index(self) -> None:
        doc_count = len(self.doctrines)
        term_doc_count: dict[str, int] = defaultdict(int)
        for d in self.doctrines:
            terms = set(d.keywords + d.topic.split("_"))
            for term in terms:
                term_doc_count[term.lower()] += 1
        for term, count in term_doc_count.items():
            self.idf[term] = math.log(doc_count / (1 + count))

    def search(self, query: str, top_k: int = 5) -> list[tuple[DoctrineBlock, float]]:
        query_terms = set(query.lower().split())
        scores: list[tuple[DoctrineBlock, float]] = []
        for doctrine in self.doctrines:
            doc_terms = set(k.lower() for k in doctrine.keywords) | set(doctrine.topic.lower().split("_"))
            score = 0.0
            for term in query_terms:
                if term in doc_terms:
                    score += self.idf.get(term, 1.0)
                for doc_term in doc_terms:
                    if term in doc_term or doc_term in term:
                        score += self.idf.get(doc_term, 0.5) * 0.5
            if score > 0:
                scores.append((doctrine, score))
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]

# ── Telemetry ───────────────────────────────────────────────────────────────

class TelemetryCollector:
    def __init__(self):
        self.query_count: int = 0
        self.total_latency_ms: float = 0.0
        self.error_count: int = 0
        self.cache_hits: int = 0
        self.cache_misses: int = 0
        self.health_checks_performed: int = 0
        self.alerts_fired: int = 0
        self.circuit_breaker_trips: int = 0
        self.start_time: float = time.time()
        self.latencies: list[float] = []
        self.hourly_counts: dict[int, int] = defaultdict(int)

    def record_query(self, latency_ms: float, cache_hit: bool) -> None:
        self.query_count += 1
        self.total_latency_ms += latency_ms
        self.latencies.append(latency_ms)
        if len(self.latencies) > LATENCY_WINDOW:
            self.latencies = self.latencies[-LATENCY_WINDOW:]
        if cache_hit:
            self.cache_hits += 1
        else:
            self.cache_misses += 1
        hour = datetime.now(timezone.utc).hour
        self.hourly_counts[hour] += 1

    def record_error(self) -> None:
        self.error_count += 1

    def record_health_check(self) -> None:
        self.health_checks_performed += 1

    def record_alert(self) -> None:
        self.alerts_fired += 1

    def record_circuit_trip(self) -> None:
        self.circuit_breaker_trips += 1

    def get_stats(self) -> dict[str, Any]:
        uptime = time.time() - self.start_time
        avg_lat = self.total_latency_ms / max(self.query_count, 1)
        p50 = sorted(self.latencies)[len(self.latencies) // 2] if self.latencies else 0
        p95 = sorted(self.latencies)[int(len(self.latencies) * 0.95)] if len(self.latencies) > 1 else 0
        p99 = sorted(self.latencies)[int(len(self.latencies) * 0.99)] if len(self.latencies) > 1 else 0
        return {
            "uptime_seconds": round(uptime, 1),
            "total_queries": self.query_count,
            "avg_latency_ms": round(avg_lat, 2),
            "p50_latency_ms": round(p50, 2),
            "p95_latency_ms": round(p95, 2),
            "p99_latency_ms": round(p99, 2),
            "error_count": self.error_count,
            "error_rate": round(self.error_count / max(self.query_count, 1), 4),
            "cache_hit_rate": round(self.cache_hits / max(self.cache_hits + self.cache_misses, 1), 4),
            "health_checks_performed": self.health_checks_performed,
            "alerts_fired": self.alerts_fired,
            "circuit_breaker_trips": self.circuit_breaker_trips,
            "queries_per_hour": dict(self.hourly_counts),
        }

# ── Drift Watcher ───────────────────────────────────────────────────────────

class DriftWatcher:
    def __init__(self, alpha: float = 0.1, threshold: float = 2.0):
        self.alpha = alpha
        self.threshold = threshold
        self.ema: dict[str, float] = {}
        self.ema_var: dict[str, float] = {}
        self.drift_events: list[dict[str, Any]] = []

    def observe(self, metric_name: str, value: float) -> Optional[dict[str, Any]]:
        if metric_name not in self.ema:
            self.ema[metric_name] = value
            self.ema_var[metric_name] = 0.0
            return None
        old_ema = self.ema[metric_name]
        self.ema[metric_name] = self.alpha * value + (1 - self.alpha) * old_ema
        diff = abs(value - old_ema)
        self.ema_var[metric_name] = self.alpha * diff + (1 - self.alpha) * self.ema_var[metric_name]
        std = max(self.ema_var[metric_name], 0.001)
        z_score = diff / std
        if z_score > self.threshold:
            event = {
                "metric": metric_name,
                "value": value,
                "expected": round(old_ema, 4),
                "z_score": round(z_score, 2),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            self.drift_events.append(event)
            if len(self.drift_events) > 1000:
                self.drift_events = self.drift_events[-500:]
            return event
        return None

# ── Coverage Map ────────────────────────────────────────────────────────────

class CoverageMap:
    def __init__(self):
        self.triggered: dict[str, int] = defaultdict(int)
        self.missed: list[str] = []
        self.gap_queries: list[str] = []

    def record_hit(self, topic: str) -> None:
        self.triggered[topic] += 1

    def record_miss(self, query: str) -> None:
        self.missed.append(query)
        self.gap_queries.append(query)
        if len(self.missed) > 500:
            self.missed = self.missed[-250:]
        if len(self.gap_queries) > 500:
            self.gap_queries = self.gap_queries[-250:]

    def get_coverage(self) -> dict[str, Any]:
        total_topics = len(DOCTRINE_CACHE)
        covered = len(self.triggered)
        return {
            "total_doctrine_topics": total_topics,
            "covered_topics": covered,
            "coverage_pct": round(covered / max(total_topics, 1) * 100, 1),
            "top_triggered": dict(sorted(self.triggered.items(), key=lambda x: x[1], reverse=True)[:10]),
            "recent_gaps": self.gap_queries[-10:],
            "total_misses": len(self.missed),
        }

# ── Metrics Collector ───────────────────────────────────────────────────────

class MetricsCollector:
    def __init__(self):
        self.counters: dict[str, int] = defaultdict(int)
        self.gauges: dict[str, float] = {}
        self.histograms: dict[str, list[float]] = defaultdict(list)

    def increment(self, name: str, value: int = 1) -> None:
        self.counters[name] += value

    def set_gauge(self, name: str, value: float) -> None:
        self.gauges[name] = value

    def observe_histogram(self, name: str, value: float) -> None:
        self.histograms[name].append(value)
        if len(self.histograms[name]) > 1000:
            self.histograms[name] = self.histograms[name][-500:]

    def get_all(self) -> dict[str, Any]:
        result: dict[str, Any] = {"counters": dict(self.counters), "gauges": dict(self.gauges), "histograms": {}}
        for name, values in self.histograms.items():
            if values:
                s = sorted(values)
                result["histograms"][name] = {
                    "count": len(s), "min": round(s[0], 2), "max": round(s[-1], 2),
                    "avg": round(sum(s) / len(s), 2),
                    "p50": round(s[len(s) // 2], 2),
                    "p95": round(s[int(len(s) * 0.95)], 2) if len(s) > 1 else round(s[0], 2),
                }
        return result

# ── Audit Trail ─────────────────────────────────────────────────────────────

class AuditTrail:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.last_hash: str = "0" * 64

    def log(self, event_type: str, data: dict[str, Any]) -> str:
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "data": data,
            "prev_hash": self.last_hash,
        }
        entry_json = json.dumps(entry, separators=(",", ":"), sort_keys=True)
        entry_hash = hashlib.sha256(entry_json.encode()).hexdigest()
        entry["hash"] = entry_hash
        self.last_hash = entry_hash
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, separators=(",", ":")) + "\n")
        return entry_hash

# ── Fact Fragility Scorer ───────────────────────────────────────────────────

class FactFragilityScorer:
    SOURCE_WEIGHTS: dict[str, float] = {
        "automated_probe": 0.1, "synthetic_monitor": 0.15,
        "real_user_monitoring": 0.2, "log_analysis": 0.3,
        "manual_observation": 0.5, "anecdotal": 0.8, "unknown": 0.9,
    }

    def score(self, source_type: str, corroboration_count: int, recency_hours: float) -> dict[str, Any]:
        base = self.SOURCE_WEIGHTS.get(source_type, 0.7)
        corroboration_factor = max(0.1, 1.0 - (corroboration_count * 0.15))
        recency_factor = min(1.0, recency_hours / 24.0) * 0.3
        fragility = min(1.0, base * corroboration_factor + recency_factor)
        return {
            "fragility_score": round(fragility, 3),
            "source_type": source_type,
            "corroboration_count": corroboration_count,
            "recency_hours": recency_hours,
            "assessment": "reliable" if fragility < 0.3 else "moderate" if fragility < 0.6 else "fragile",
        }

# ── Zoned Analyzer ──────────────────────────────────────────────────────────

class ZonedAnalyzer:
    def __init__(self):
        self.zone_history: list[dict[str, Any]] = []

    def analyze(self, query: str, zone: AnalysisZone, data: dict[str, Any]) -> dict[str, Any]:
        result: dict[str, Any] = {"zone": zone.value, "query": query}
        if zone == AnalysisZone.PLANNING:
            result["focus"] = "Forward-looking capacity and reliability planning"
            result["recommendations"] = self._planning_analysis(data)
        elif zone == AnalysisZone.REPORTING:
            result["focus"] = "Current state reporting and dashboards"
            result["summary"] = self._reporting_analysis(data)
        elif zone == AnalysisZone.AUDIT:
            result["focus"] = "Historical compliance and forensic review"
            result["audit_findings"] = self._audit_analysis(data)
        self.zone_history.append({"zone": zone.value, "timestamp": datetime.now(timezone.utc).isoformat()})
        if len(self.zone_history) > 500:
            self.zone_history = self.zone_history[-250:]
        return result

    def _planning_analysis(self, data: dict[str, Any]) -> list[str]:
        recs = []
        if data.get("unhealthy_count", 0) > 0:
            recs.append(f"Address {data['unhealthy_count']} unhealthy services before capacity expansion")
        if data.get("avg_latency_ms", 0) > 500:
            recs.append("Investigate high average latency — consider caching or CDN optimization")
        if data.get("circuit_open_count", 0) > 0:
            recs.append(f"{data['circuit_open_count']} circuit breakers open — resolve upstream dependencies")
        if data.get("uptime_pct", 100) < 99.9:
            recs.append(f"Uptime at {data.get('uptime_pct', 0):.2f}% — below 99.9% target, prioritize reliability")
        if not recs:
            recs.append("System healthy — consider expanding monitoring coverage or load testing")
        return recs

    def _reporting_analysis(self, data: dict[str, Any]) -> dict[str, Any]:
        return {
            "total_services": data.get("total_services", 0),
            "healthy_pct": round(data.get("healthy_count", 0) / max(data.get("total_services", 1), 1) * 100, 1),
            "avg_latency_ms": round(data.get("avg_latency_ms", 0), 2),
            "active_alerts": data.get("active_alerts", 0),
            "uptime_pct": round(data.get("uptime_pct", 100), 3),
        }

    def _audit_analysis(self, data: dict[str, Any]) -> list[str]:
        findings = []
        if data.get("error_count", 0) > 10:
            findings.append(f"High error count ({data['error_count']}) — review error patterns")
        if data.get("unacknowledged_alerts", 0) > 0:
            findings.append(f"{data['unacknowledged_alerts']} unacknowledged alerts — review alert handling")
        if data.get("services_without_health_check", 0) > 0:
            findings.append(f"{data['services_without_health_check']} services lack health checks")
        if not findings:
            findings.append("No audit concerns detected")
        return findings

# ── Multi-Doctrine Decomposer ──────────────────────────────────────────────

class MultiDoctrineDecomposer:
    ISSUE_CATEGORIES: list[str] = [
        "availability", "latency", "error_rate", "saturation",
        "security", "compliance", "cost", "capacity",
        "dependency", "configuration", "deployment", "incident",
    ]

    INTERACTION_EDGES: list[tuple[str, str, str]] = [
        ("availability", "error_rate", "availability_drops_increase_errors"),
        ("latency", "saturation", "high_saturation_increases_latency"),
        ("dependency", "availability", "dependency_failure_reduces_availability"),
        ("deployment", "error_rate", "bad_deploy_increases_errors"),
        ("configuration", "security", "misconfiguration_creates_vulnerabilities"),
        ("capacity", "latency", "insufficient_capacity_increases_latency"),
        ("incident", "availability", "incidents_reduce_availability"),
        ("security", "compliance", "security_gaps_affect_compliance"),
        ("cost", "capacity", "cost_constraints_limit_capacity"),
        ("saturation", "availability", "oversaturation_causes_outage"),
    ]

    def decompose(self, query: str) -> dict[str, Any]:
        normalizer = SemanticNormalizer()
        keywords = normalizer.extract_keywords(query)
        relevant_categories = []
        for cat in self.ISSUE_CATEGORIES:
            cat_terms = set(cat.split("_"))
            if cat_terms & set(keywords):
                relevant_categories.append(cat)
        if not relevant_categories:
            relevant_categories = ["availability", "latency", "error_rate"]
        relevant_edges = [
            {"from": e[0], "to": e[1], "relationship": e[2]}
            for e in self.INTERACTION_EDGES
            if e[0] in relevant_categories or e[1] in relevant_categories
        ]
        return {
            "query": query,
            "categories": relevant_categories,
            "interaction_edges": relevant_edges,
            "decomposition_depth": len(relevant_categories),
        }

# ── Deep Analyzer ───────────────────────────────────────────────────────────

class DeepAnalyzer:
    def __init__(self, vector_search: VectorSearchEngine, fragility: FactFragilityScorer):
        self.vector_search = vector_search
        self.fragility = fragility

    def analyze(self, query: str, system_data: dict[str, Any]) -> dict[str, Any]:
        search_results = self.vector_search.search(query, top_k=5)
        sources = []
        reasoning_chain = []
        for doctrine, score in search_results:
            sources.append({
                "topic": doctrine.topic,
                "relevance_score": round(score, 3),
                "confidence": doctrine.confidence.value,
                "conclusion": doctrine.conclusion,
            })
            reasoning_chain.append(f"[{doctrine.topic}] {doctrine.reasoning[:200]}...")
        fragility_assessment = self.fragility.score(
            source_type="automated_probe",
            corroboration_count=len(sources),
            recency_hours=0.1,
        )
        return {
            "query": query,
            "sources": sources,
            "reasoning_chain": reasoning_chain,
            "fragility": fragility_assessment,
            "system_context": {
                "total_services": system_data.get("total_services", 0),
                "healthy": system_data.get("healthy", 0),
                "active_alerts": system_data.get("active_alerts", 0),
            },
            "synthesis": self._synthesize(query, sources, system_data),
        }

    def _synthesize(self, query: str, sources: list[dict], system_data: dict) -> str:
        if not sources:
            return f"No doctrine coverage for query: {query}. Consider expanding monitoring doctrine."
        top = sources[0]
        health_summary = f"System has {system_data.get('total_services', 0)} services, " \
                         f"{system_data.get('healthy', 0)} healthy, " \
                         f"{system_data.get('active_alerts', 0)} active alerts."
        return f"Based on {top['topic']} doctrine ({top['confidence']} confidence): " \
               f"{top['conclusion']} {health_summary}"

# ── Response Formatter ──────────────────────────────────────────────────────

class ResponseFormatter:
    def format(self, data: dict[str, Any], mode: ResponseMode) -> dict[str, Any]:
        if mode == ResponseMode.FAST:
            return {
                "summary": data.get("synthesis", data.get("summary", "")),
                "status": data.get("status", "unknown"),
                "key_metrics": {k: v for k, v in data.items() if k in ("healthy", "unhealthy", "avg_latency_ms", "active_alerts")},
            }
        elif mode == ResponseMode.DEFENSE:
            return {
                "summary": data.get("synthesis", ""),
                "sources": data.get("sources", []),
                "reasoning_chain": data.get("reasoning_chain", []),
                "fragility": data.get("fragility", {}),
                "confidence": data.get("confidence", "UNKNOWN"),
                "audit_hash": data.get("audit_hash", ""),
            }
        else:  # MEMO
            return {
                "full_analysis": data,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "engine": ENGINE_ID,
                "version": ENGINE_VERSION,
                "disclaimer": "This analysis is based on automated monitoring data and doctrine cache. "
                              "Human review recommended for critical decisions.",
            }

# ── Circuit Breaker ─────────────────────────────────────────────────────────

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, recovery_timeout: float = 60.0,
                 half_open_max_calls: int = 3):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_max_calls = half_open_max_calls

    def should_open(self, record: ServiceRecord) -> bool:
        return record.consecutive_failures >= self.failure_threshold

    def should_half_open(self, record: ServiceRecord) -> bool:
        if not record.circuit_breaker_open or not record.circuit_breaker_opened_at:
            return False
        opened_at = datetime.fromisoformat(record.circuit_breaker_opened_at)
        elapsed = (datetime.now(timezone.utc) - opened_at).total_seconds()
        return elapsed >= self.recovery_timeout

    def trip(self, record: ServiceRecord) -> None:
        record.circuit_breaker_open = True
        record.circuit_breaker_opened_at = datetime.now(timezone.utc).isoformat()
        record.current_status = ServiceStatus.CIRCUIT_OPEN

    def reset(self, record: ServiceRecord) -> None:
        record.circuit_breaker_open = False
        record.circuit_breaker_opened_at = None
        record.consecutive_failures = 0

# ── Authority Hardening ─────────────────────────────────────────────────────

class AuthorityHardening:
    LEVELS: dict[str, float] = {
        "public": 0.0, "basic": 1.0, "standard": 3.0, "elevated": 5.0,
        "admin": 7.0, "system": 9.0, "sovereign": 11.0,
    }

    def check_access(self, required_level: str, provided_level: str) -> bool:
        req = self.LEVELS.get(required_level, 11.0)
        prov = self.LEVELS.get(provided_level, 0.0)
        return prov >= req

    def classify_query(self, query: str) -> str:
        sensitive_terms = {"delete", "purge", "override", "force", "reset", "kill", "shutdown"}
        admin_terms = {"configure", "register", "unregister", "threshold", "policy"}
        query_lower = query.lower()
        if any(t in query_lower for t in sensitive_terms):
            return "admin"
        if any(t in query_lower for t in admin_terms):
            return "elevated"
        return "public"

# ── Health Monitor Core ─────────────────────────────────────────────────────

class HealthMonitor:
    def __init__(self):
        self.services: dict[str, ServiceRecord] = {}
        self.alerts: list[AlertRecord] = []
        self.snapshots: list[SystemSnapshot] = []
        self.circuit_breaker = CircuitBreaker()
        self.telemetry = TelemetryCollector()
        self.drift_watcher = DriftWatcher()
        self.coverage_map = CoverageMap()
        self.metrics = MetricsCollector()
        self.normalizer = SemanticNormalizer()
        self.vector_search = VectorSearchEngine(ALL_DOCTRINES)
        self.fragility_scorer = FactFragilityScorer()
        self.deep_analyzer = DeepAnalyzer(self.vector_search, self.fragility_scorer)
        self.zoned_analyzer = ZonedAnalyzer()
        self.decomposer = MultiDoctrineDecomposer()
        self.response_formatter = ResponseFormatter()
        self.authority = AuthorityHardening()
        self.audit_trail = AuditTrail(LOG_DIR / "audit_trail.jsonl")
        self.flapping_detector = FlappingDetector()
        self.incident_manager = IncidentManager()
        self.maintenance_manager = MaintenanceManager()
        self.capacity_forecaster = CapacityForecaster()
        self.uptime_tracker = UptimeTracker()
        self.http_client: Optional[httpx.AsyncClient] = None
        self._alert_counter: int = 0
        self._polling_active: bool = False
        self._poll_task: Optional[asyncio.Task[None]] = None
        self._load_default_services()
        logger.info(f"HealthMonitor initialized: {len(ALL_DOCTRINES)} total doctrines "
                    f"({len(DOCTRINE_CACHE)} inline + {len(FILE_DOCTRINES)} from file)")

    def _load_default_services(self) -> None:
        defaults = [
            ServiceDefinition(service_id="TIE", name="Tax Intelligence Engine", service_type=ServiceType.ENGINE,
                              url="http://localhost:8391", port=8391, critical=True, tags=["backbone", "tax"]),
            ServiceDefinition(service_id="PIE", name="Policy Intelligence Engine", service_type=ServiceType.ENGINE,
                              url="http://localhost:8392", port=8392, critical=True, tags=["backbone", "policy"]),
            ServiceDefinition(service_id="ARCS", name="ARCS Engine", service_type=ServiceType.ENGINE,
                              url="http://localhost:8393", port=8393, critical=True, tags=["backbone"]),
            ServiceDefinition(service_id="EKM", name="EKM Query Engine", service_type=ServiceType.CLOUD_WORKER,
                              url="https://ekm-query-engine.bmcii1976.workers.dev", tags=["cloud", "knowledge"]),
            ServiceDefinition(service_id="GRAPH", name="Graph Query Engine", service_type=ServiceType.CLOUD_WORKER,
                              url="https://graph-query-engine.bmcii1976.workers.dev", tags=["cloud", "graph"]),
            ServiceDefinition(service_id="CRYSTAL", name="Crystal Memory Engine", service_type=ServiceType.CLOUD_WORKER,
                              url="https://crystal-memory-engine.bmcii1976.workers.dev", tags=["cloud", "memory"]),
            ServiceDefinition(service_id="SWARM", name="Swarm Brain", service_type=ServiceType.CLOUD_WORKER,
                              url="https://echo-swarm-brain.bmcii1976.workers.dev", tags=["cloud", "swarm"]),
            ServiceDefinition(service_id="SHARED_BRAIN", name="Echo Shared Brain", service_type=ServiceType.CLOUD_WORKER,
                              url="https://echo-shared-brain.bmcii1976.workers.dev", tags=["cloud", "brain"]),
            ServiceDefinition(service_id="MEMORY_PRIME", name="Echo Memory Prime", service_type=ServiceType.CLOUD_WORKER,
                              url="https://echo-memory-prime.bmcii1976.workers.dev", tags=["cloud", "memory"]),
            ServiceDefinition(service_id="KNOWLEDGE_FORGE", name="Knowledge Forge", service_type=ServiceType.CLOUD_WORKER,
                              url="https://echo-knowledge-forge.bmcii1976.workers.dev", tags=["cloud", "knowledge"]),
            ServiceDefinition(service_id="SHADOWGLASS", name="ShadowGlass v8", service_type=ServiceType.CLOUD_WORKER,
                              url="https://shadowglass-v8-warpspeed.bmcii1976.workers.dev", tags=["cloud", "scraping"]),
            ServiceDefinition(service_id="ORCHESTRATOR", name="Build Orchestrator", service_type=ServiceType.CLOUD_WORKER,
                              url="https://echo-build-orchestrator.bmcii1976.workers.dev", tags=["cloud", "orchestrator"]),
            ServiceDefinition(service_id="OMNISCIENT", name="Omniscient Sync", service_type=ServiceType.CLOUD_WORKER,
                              url="https://omniscient-sync.bmcii1976.workers.dev", tags=["cloud", "sync"]),
            ServiceDefinition(service_id="BREE", name="Bree Chat", service_type=ServiceType.CLOUD_WORKER,
                              url="https://bree-chat.bmcii1976.workers.dev", tags=["cloud", "chat"]),
            ServiceDefinition(service_id="SENTINEL_MEM", name="Sentinel Memory", service_type=ServiceType.CLOUD_WORKER,
                              url="https://echo-sentinel-memory.bmcii1976.workers.dev", tags=["cloud", "memory"]),
            ServiceDefinition(service_id="CLAUDFARE", name="Claudfare Terminal", service_type=ServiceType.LOCAL_SERVICE,
                              url="http://localhost:8451", port=8451, tags=["local", "terminal"]),
            ServiceDefinition(service_id="AI_ORCH", name="Multi-AI Orchestrator", service_type=ServiceType.LOCAL_SERVICE,
                              url="http://localhost:3032", port=3032, tags=["local", "ai"]),
            ServiceDefinition(service_id="GS343", name="GS343 Error Healer", service_type=ServiceType.LOCAL_SERVICE,
                              url="http://localhost:5003", port=5003, tags=["local", "healing"]),
        ]
        for svc in defaults:
            self.services[svc.service_id] = ServiceRecord(definition=svc)

    async def get_http_client(self) -> httpx.AsyncClient:
        if self.http_client is None or self.http_client.is_closed:
            self.http_client = httpx.AsyncClient(timeout=HEALTH_CHECK_TIMEOUT, follow_redirects=True)
        return self.http_client

    async def check_service(self, service_id: str) -> HealthCheckResult:
        record = self.services.get(service_id)
        if not record:
            return HealthCheckResult(
                service_id=service_id, status=ServiceStatus.UNKNOWN,
                latency_ms=0, timestamp=datetime.now(timezone.utc).isoformat(),
                error="Service not registered",
            )
        if record.circuit_breaker_open:
            if self.circuit_breaker.should_half_open(record):
                logger.info(f"Circuit breaker half-open for {service_id}, attempting probe")
            else:
                return HealthCheckResult(
                    service_id=service_id, status=ServiceStatus.CIRCUIT_OPEN,
                    latency_ms=0, timestamp=datetime.now(timezone.utc).isoformat(),
                    error="Circuit breaker open",
                )
        # Check maintenance window -- skip health check if in maintenance
        if self.maintenance_manager.is_in_maintenance(service_id):
            prev = record.current_status
            record.current_status = ServiceStatus.DEGRADED  # Mark as degraded during maintenance
            record.last_check = datetime.now(timezone.utc).isoformat()
            if prev != ServiceStatus.DEGRADED:
                self.flapping_detector.record_state_change(service_id)
            return HealthCheckResult(
                service_id=service_id, status=ServiceStatus.DEGRADED,
                latency_ms=0, timestamp=datetime.now(timezone.utc).isoformat(),
                details={"maintenance": True},
            )

        url = f"{record.definition.url}{record.definition.health_path}"
        start = time.monotonic()
        prev_status = record.current_status
        try:
            client = await self.get_http_client()
            resp = await client.get(url)
            latency = (time.monotonic() - start) * 1000
            self.telemetry.record_health_check()
            self.metrics.observe_histogram(f"health_check_latency_{service_id}", latency)
            now = datetime.now(timezone.utc).isoformat()
            record.uptime_checks += 1
            record.last_check = now
            if resp.status_code == 200:
                record.current_status = ServiceStatus.HEALTHY
                record.last_healthy = now
                record.consecutive_failures = 0
                record.uptime_successes += 1
                self.uptime_tracker.record_check(service_id, True)
                self.flapping_detector.record_stable_check(service_id)
                if record.circuit_breaker_open:
                    self.circuit_breaker.reset(record)
                    logger.info(f"Circuit breaker reset for {service_id}")
                record.latency_history.append(latency)
                if len(record.latency_history) > LATENCY_WINDOW:
                    record.latency_history = record.latency_history[-LATENCY_WINDOW:]
                # Record capacity data
                self.capacity_forecaster.record(service_id, "latency_ms", latency)
                details = {}
                try:
                    details = resp.json()
                except Exception:
                    pass
                self.drift_watcher.observe(f"latency_{service_id}", latency)
                if prev_status != ServiceStatus.HEALTHY:
                    self.flapping_detector.record_state_change(service_id)
                    self.audit_trail.log("status_change", {
                        "service_id": service_id, "from": prev_status.value,
                        "to": "healthy"})
                return HealthCheckResult(
                    service_id=service_id, status=ServiceStatus.HEALTHY,
                    latency_ms=round(latency, 2), timestamp=now,
                    response_code=resp.status_code, details=details,
                )
            else:
                record.consecutive_failures += 1
                status = ServiceStatus.DEGRADED if resp.status_code < 500 else ServiceStatus.UNHEALTHY
                record.current_status = status
                self.uptime_tracker.record_check(service_id, False)
                if prev_status != status:
                    self.flapping_detector.record_state_change(service_id)
                if self.circuit_breaker.should_open(record):
                    self.circuit_breaker.trip(record)
                    self.telemetry.record_circuit_trip()
                    self._fire_alert(service_id, AlertSeverity.HIGH,
                                     f"Circuit breaker opened for {service_id} after {record.consecutive_failures} failures")
                # Create incident on consecutive failures
                if record.consecutive_failures >= CONSECUTIVE_FAILURES_DOWN:
                    active_incs = [i for i in self.incident_manager.get_active()
                                   if i.service_id == service_id]
                    if not active_incs:
                        inc = self.incident_manager.create_incident(
                            service_id, "http_error",
                            f"Service {service_id} failing: HTTP {resp.status_code}",
                            AlertSeverity.HIGH)
                        tier, auto = self.incident_manager.recommend_remediation(service_id)
                        inc.remediation_tier = tier
                        inc.auto_approved = auto
                return HealthCheckResult(
                    service_id=service_id, status=status,
                    latency_ms=round(latency, 2), timestamp=now,
                    response_code=resp.status_code, error=f"HTTP {resp.status_code}",
                )
        except Exception as e:
            latency = (time.monotonic() - start) * 1000
            now = datetime.now(timezone.utc).isoformat()
            record.uptime_checks += 1
            record.consecutive_failures += 1
            record.current_status = ServiceStatus.UNHEALTHY
            record.last_check = now
            self.uptime_tracker.record_check(service_id, False)
            record.error_history.append(str(e))
            if len(record.error_history) > 50:
                record.error_history = record.error_history[-25:]
            if prev_status != ServiceStatus.UNHEALTHY:
                self.flapping_detector.record_state_change(service_id)
            if self.circuit_breaker.should_open(record):
                self.circuit_breaker.trip(record)
                self.telemetry.record_circuit_trip()
                self._fire_alert(service_id, AlertSeverity.HIGH,
                                 f"Circuit breaker opened for {service_id}: {e}")
            # Create incident on consecutive failures
            if record.consecutive_failures >= CONSECUTIVE_FAILURES_DOWN:
                active_incs = [i for i in self.incident_manager.get_active()
                               if i.service_id == service_id]
                if not active_incs:
                    failure_mode = "connection_refused" if "refused" in str(e).lower() else (
                        "timeout" if "timeout" in str(e).lower() else "exception")
                    inc = self.incident_manager.create_incident(
                        service_id, failure_mode,
                        f"Service {service_id} DOWN: {e}", AlertSeverity.HIGH)
                    tier, auto = self.incident_manager.recommend_remediation(service_id)
                    inc.remediation_tier = tier
                    inc.auto_approved = auto
            return HealthCheckResult(
                service_id=service_id, status=ServiceStatus.UNHEALTHY,
                latency_ms=round(latency, 2), timestamp=now,
                error=str(e),
            )

    async def check_all(self) -> list[HealthCheckResult]:
        tasks = [self.check_service(sid) for sid in self.services]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        valid_results = []
        for r in results:
            if isinstance(r, HealthCheckResult):
                valid_results.append(r)
            elif isinstance(r, Exception):
                logger.error(f"Health check exception: {r}")
        return valid_results

    def get_snapshot(self) -> SystemSnapshot:
        now = datetime.now(timezone.utc).isoformat()
        statuses = [r.current_status for r in self.services.values()]
        healthy = sum(1 for s in statuses if s == ServiceStatus.HEALTHY)
        degraded = sum(1 for s in statuses if s == ServiceStatus.DEGRADED)
        unhealthy = sum(1 for s in statuses if s == ServiceStatus.UNHEALTHY)
        unknown = sum(1 for s in statuses if s == ServiceStatus.UNKNOWN)
        circuit_open = sum(1 for s in statuses if s == ServiceStatus.CIRCUIT_OPEN)
        all_latencies = []
        for r in self.services.values():
            if r.latency_history:
                all_latencies.extend(r.latency_history[-10:])
        avg_lat = sum(all_latencies) / max(len(all_latencies), 1) if all_latencies else 0
        active_alerts = sum(1 for a in self.alerts if not a.resolved)
        total_checks = sum(r.uptime_checks for r in self.services.values())
        total_successes = sum(r.uptime_successes for r in self.services.values())
        uptime_pct = (total_successes / max(total_checks, 1)) * 100
        snapshot = SystemSnapshot(
            timestamp=now, total_services=len(self.services),
            healthy=healthy, degraded=degraded, unhealthy=unhealthy,
            unknown=unknown, circuit_open=circuit_open,
            avg_latency_ms=round(avg_lat, 2),
            active_alerts=active_alerts, uptime_pct=round(uptime_pct, 3),
        )
        self.snapshots.append(snapshot)
        if len(self.snapshots) > MAX_HISTORY_ENTRIES:
            self.snapshots = self.snapshots[-MAX_HISTORY_ENTRIES // 2:]
        return snapshot

    def _fire_alert(self, service_id: str, severity: AlertSeverity, message: str) -> AlertRecord:
        self._alert_counter += 1
        alert = AlertRecord(
            alert_id=f"ALERT-{self._alert_counter:06d}",
            severity=severity, service_id=service_id,
            message=message, timestamp=datetime.now(timezone.utc).isoformat(),
        )
        self.alerts.append(alert)
        if len(self.alerts) > MAX_HISTORY_ENTRIES:
            self.alerts = self.alerts[-MAX_HISTORY_ENTRIES // 2:]
        self.telemetry.record_alert()
        self.audit_trail.log("alert_fired", {"alert_id": alert.alert_id, "severity": severity.value,
                                              "service_id": service_id, "message": message})
        logger.warning(f"ALERT [{severity.value}] {service_id}: {message}")
        return alert

    def register_service(self, defn: ServiceDefinition) -> ServiceRecord:
        record = ServiceRecord(definition=defn)
        self.services[defn.service_id] = record
        self.audit_trail.log("service_registered", {"service_id": defn.service_id, "name": defn.name})
        logger.info(f"Registered service: {defn.service_id} ({defn.name}) at {defn.url}")
        return record

    def unregister_service(self, service_id: str) -> bool:
        if service_id in self.services:
            del self.services[service_id]
            self.audit_trail.log("service_unregistered", {"service_id": service_id})
            return True
        return False

    def get_dependency_graph(self) -> dict[str, Any]:
        nodes = []
        edges = []
        for sid, record in self.services.items():
            nodes.append({
                "id": sid, "name": record.definition.name,
                "status": record.current_status.value,
                "type": record.definition.service_type.value,
            })
            for dep in record.definition.dependencies:
                edges.append({"from": sid, "to": dep, "type": "depends_on"})
        return {"nodes": nodes, "edges": edges, "total_nodes": len(nodes), "total_edges": len(edges)}

    def detect_cascade_risks(self) -> list[dict[str, Any]]:
        risks = []
        for sid, record in self.services.items():
            if record.current_status in (ServiceStatus.UNHEALTHY, ServiceStatus.CIRCUIT_OPEN):
                dependents = [
                    s for s, r in self.services.items()
                    if sid in r.definition.dependencies
                ]
                if dependents:
                    risks.append({
                        "failing_service": sid,
                        "status": record.current_status.value,
                        "at_risk_services": dependents,
                        "blast_radius": len(dependents),
                        "critical": record.definition.critical,
                    })
        risks.sort(key=lambda x: x["blast_radius"], reverse=True)
        return risks

    async def query(self, request: QueryRequest) -> QueryResponse:
        start = time.monotonic()
        # Step 1: Normalize query
        normalized = self.normalizer.normalize(request.query)
        keywords = self.normalizer.extract_keywords(request.query)
        # Step 2: Doctrine cache lookup
        cache_results = self.vector_search.search(normalized, top_k=3)
        cache_hit = len(cache_results) > 0
        if cache_hit:
            for doctrine, _ in cache_results:
                doctrine.hit_count += 1
                doctrine.last_hit = datetime.now(timezone.utc).isoformat()
                self.coverage_map.record_hit(doctrine.topic)
        else:
            self.coverage_map.record_miss(request.query)
        # Step 3: System state
        snapshot = self.get_snapshot()
        system_data = {
            "total_services": snapshot.total_services,
            "healthy": snapshot.healthy,
            "unhealthy": snapshot.unhealthy,
            "degraded": snapshot.degraded,
            "avg_latency_ms": snapshot.avg_latency_ms,
            "active_alerts": snapshot.active_alerts,
            "uptime_pct": snapshot.uptime_pct,
            "healthy_count": snapshot.healthy,
            "unhealthy_count": snapshot.unhealthy,
            "circuit_open_count": snapshot.circuit_open,
        }
        # Step 4: Deep analysis
        analysis = self.deep_analyzer.analyze(request.query, system_data)
        # Step 5: Zone analysis
        zoned = self.zoned_analyzer.analyze(request.query, request.zone, system_data)
        # Step 6: Decomposition
        decomposition = self.decomposer.decompose(request.query)
        # Step 7: Determine confidence
        confidence = ConfidenceLevel.DEFENSIBLE
        if not cache_hit:
            confidence = ConfidenceLevel.AGGRESSIVE
        if snapshot.unknown > snapshot.total_services * 0.3:
            confidence = ConfidenceLevel.DISCLOSURE
        # Step 8: Format response
        combined = {**analysis, **zoned, "decomposition": decomposition, "snapshot": snapshot.model_dump(),
                    "confidence": confidence.value}
        formatted = self.response_formatter.format(combined, request.mode)
        # Step 9: Determinism hash
        hash_input = json.dumps({"query": request.query, "mode": request.mode.value,
                                  "snapshot": snapshot.model_dump()}, sort_keys=True, default=str)
        det_hash = hashlib.sha256(hash_input.encode()).hexdigest()
        # Step 10: Audit
        latency_ms = (time.monotonic() - start) * 1000
        self.audit_trail.log("query", {"query": request.query, "mode": request.mode.value,
                                        "latency_ms": round(latency_ms, 2), "confidence": confidence.value})
        self.telemetry.record_query(latency_ms, cache_hit)
        sources = [d.topic for d, _ in cache_results]
        return QueryResponse(
            query=request.query, mode=request.mode, zone=request.zone,
            response=formatted, confidence=confidence,
            determinism_hash=det_hash, latency_ms=round(latency_ms, 2),
            timestamp=datetime.now(timezone.utc).isoformat(), sources=sources,
        )

    # ── Background Polling ─────────────────────────────────────────────────

    async def _poll_loop(self) -> None:
        """Background health polling loop."""
        logger.info("Background health polling started")
        while self._polling_active:
            try:
                await self.check_all()
                self.incident_manager.check_escalation()
            except Exception as exc:
                logger.error(f"Poll cycle error: {exc}")
                self.telemetry.record_error()
            await asyncio.sleep(DEFAULT_POLL_INTERVAL)

    async def start_polling(self) -> None:
        """Start the background polling loop."""
        self._polling_active = True
        self._poll_task = asyncio.create_task(self._poll_loop())
        logger.info("Health polling started")

    async def stop_polling(self) -> None:
        """Stop the background polling loop."""
        self._polling_active = False
        if self._poll_task:
            self._poll_task.cancel()
            try:
                await self._poll_task
            except asyncio.CancelledError:
                pass
        logger.info("Health polling stopped")

    async def close(self) -> None:
        await self.stop_polling()
        if self.http_client and not self.http_client.is_closed:
            await self.http_client.aclose()

    # ── Uptime via UptimeTracker ───────────────────────────────────────────

    def get_service_uptime(self, service_id: str) -> dict[str, float]:
        return {
            "24h": self.uptime_tracker.calculate_uptime(service_id, 86400),
            "7d": self.uptime_tracker.calculate_uptime(service_id, 604800),
            "30d": self.uptime_tracker.calculate_uptime(service_id, 2592000),
        }

    # ── Capacity Forecasting ───────────────────────────────────────────────

    def get_capacity_forecast(self, service_id: str, metric: str = "latency_ms",
                              threshold: float = 2000.0) -> Optional[CapacityForecast]:
        return self.capacity_forecaster.forecast(service_id, metric, threshold)

# ── Determinism Hash Helper ─────────────────────────────────────────────────

def compute_determinism_hash(data: Any) -> str:
    raw = json.dumps(data, sort_keys=True, default=str)
    return hashlib.sha256(raw.encode()).hexdigest()

# ── FastAPI Application ─────────────────────────────────────────────────────

monitor = HealthMonitor()

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"GOV03 System Health Monitor v{ENGINE_VERSION} starting on port {PORT}")
    logger.info(f"Monitoring {len(monitor.services)} services, "
                f"{len(ALL_DOCTRINES)} doctrines loaded")
    await monitor.start_polling()
    yield
    await monitor.close()
    logger.info("GOV03 shutting down")

app = FastAPI(
    title=f"GOV03 - {ENGINE_NAME}",
    version=ENGINE_VERSION,
    description="System Health Monitor for ECHO OMEGA PRIME",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Endpoints ───────────────────────────────────────────────────────────────

@app.get("/health")
async def health_endpoint():
    snapshot = monitor.get_snapshot()
    return {
        "status": "healthy",
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "version": ENGINE_VERSION,
        "port": PORT,
        "monitored_services": snapshot.total_services,
        "healthy_services": snapshot.healthy,
        "degraded_services": snapshot.degraded,
        "unhealthy_services": snapshot.unhealthy,
        "circuit_open": snapshot.circuit_open,
        "avg_latency_ms": snapshot.avg_latency_ms,
        "active_alerts": snapshot.active_alerts,
        "uptime_pct": snapshot.uptime_pct,
        "active_incidents": len(monitor.incident_manager.get_active()),
        "active_maintenance": len(monitor.maintenance_manager.active_windows()),
        "polling_active": monitor._polling_active,
        "telemetry": monitor.telemetry.get_stats(),
        "doctrine_topics": len(ALL_DOCTRINES),
        "inline_doctrines": len(DOCTRINE_CACHE),
        "file_doctrines": len(FILE_DOCTRINES),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "components": {
            "doctrine_cache": "healthy",
            "semantic_normalizer": "healthy",
            "vector_search": "healthy",
            "telemetry": "healthy",
            "drift_watcher": "healthy",
            "coverage_map": "healthy",
            "metrics_collector": "healthy",
            "audit_trail": "healthy",
            "circuit_breaker": "healthy",
            "flapping_detector": "healthy",
            "incident_manager": "healthy",
            "maintenance_manager": "healthy",
            "capacity_forecaster": "healthy",
            "uptime_tracker": "healthy",
            "authority_hardening": "healthy",
            "zoned_analyzer": "healthy",
            "fact_fragility": "healthy",
            "deep_analyzer": "healthy",
            "multi_doctrine_decomposer": "healthy",
            "response_formatter": "healthy",
        },
    }

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    return await monitor.query(request)

@app.get("/check/{service_id}")
async def check_service(service_id: str):
    return await monitor.check_service(service_id)

@app.post("/check-all")
async def check_all_services():
    results = await monitor.check_all()
    return {"results": [r.model_dump() for r in results], "total": len(results),
            "timestamp": datetime.now(timezone.utc).isoformat()}

@app.get("/snapshot")
async def get_snapshot():
    return monitor.get_snapshot().model_dump()

@app.get("/services")
async def list_services(status: Optional[str] = None, tag: Optional[str] = None):
    services = []
    for sid, record in monitor.services.items():
        if status and record.current_status.value != status:
            continue
        if tag and tag not in record.definition.tags:
            continue
        uptime = (record.uptime_successes / max(record.uptime_checks, 1)) * 100
        lat_hist = record.latency_history[-10:] if record.latency_history else []
        avg_lat = sum(lat_hist) / max(len(lat_hist), 1) if lat_hist else 0
        services.append({
            "service_id": sid,
            "name": record.definition.name,
            "type": record.definition.service_type.value,
            "status": record.current_status.value,
            "url": record.definition.url,
            "port": record.definition.port,
            "last_check": record.last_check,
            "last_healthy": record.last_healthy,
            "consecutive_failures": record.consecutive_failures,
            "circuit_breaker_open": record.circuit_breaker_open,
            "uptime_pct": round(uptime, 3),
            "avg_latency_ms": round(avg_lat, 2),
            "tags": record.definition.tags,
            "critical": record.definition.critical,
        })
    return {"services": services, "total": len(services)}

@app.get("/service/{service_id}")
async def get_service_detail(service_id: str):
    record = monitor.services.get(service_id)
    if not record:
        raise HTTPException(status_code=404, detail=f"Service {service_id} not found")
    uptime = (record.uptime_successes / max(record.uptime_checks, 1)) * 100
    lat = record.latency_history
    return {
        "service_id": service_id,
        "definition": record.definition.model_dump(),
        "current_status": record.current_status.value,
        "last_check": record.last_check,
        "last_healthy": record.last_healthy,
        "consecutive_failures": record.consecutive_failures,
        "circuit_breaker": {
            "open": record.circuit_breaker_open,
            "opened_at": record.circuit_breaker_opened_at,
        },
        "uptime": {"checks": record.uptime_checks, "successes": record.uptime_successes, "pct": round(uptime, 3)},
        "latency": {
            "recent": lat[-20:] if lat else [],
            "avg": round(sum(lat) / max(len(lat), 1), 2) if lat else 0,
            "p50": round(sorted(lat)[len(lat) // 2], 2) if lat else 0,
            "p95": round(sorted(lat)[int(len(lat) * 0.95)], 2) if len(lat) > 1 else 0,
            "p99": round(sorted(lat)[int(len(lat) * 0.99)], 2) if len(lat) > 1 else 0,
        },
        "recent_errors": record.error_history[-10:],
    }

@app.post("/register")
async def register_service(request: RegisterRequest):
    defn = ServiceDefinition(**request.model_dump())
    record = monitor.register_service(defn)
    return {"status": "registered", "service_id": defn.service_id, "name": defn.name}

@app.delete("/service/{service_id}")
async def unregister_service(service_id: str):
    if monitor.unregister_service(service_id):
        return {"status": "unregistered", "service_id": service_id}
    raise HTTPException(status_code=404, detail=f"Service {service_id} not found")

@app.get("/alerts")
async def get_alerts(active_only: bool = True, severity: Optional[str] = None):
    alerts = monitor.alerts
    if active_only:
        alerts = [a for a in alerts if not a.resolved]
    if severity:
        alerts = [a for a in alerts if a.severity.value == severity]
    return {"alerts": [a.model_dump() for a in alerts[-50:]], "total": len(alerts)}

@app.post("/alerts/{alert_id}/acknowledge")
async def acknowledge_alert(alert_id: str):
    for alert in monitor.alerts:
        if alert.alert_id == alert_id:
            alert.acknowledged = True
            monitor.audit_trail.log("alert_acknowledged", {"alert_id": alert_id})
            return {"status": "acknowledged", "alert_id": alert_id}
    raise HTTPException(status_code=404, detail=f"Alert {alert_id} not found")

@app.post("/alerts/{alert_id}/resolve")
async def resolve_alert(alert_id: str):
    for alert in monitor.alerts:
        if alert.alert_id == alert_id:
            alert.resolved = True
            alert.resolved_at = datetime.now(timezone.utc).isoformat()
            monitor.audit_trail.log("alert_resolved", {"alert_id": alert_id})
            return {"status": "resolved", "alert_id": alert_id}
    raise HTTPException(status_code=404, detail=f"Alert {alert_id} not found")

@app.get("/dependency-graph")
async def dependency_graph():
    return monitor.get_dependency_graph()

@app.get("/cascade-risks")
async def cascade_risks():
    risks = monitor.detect_cascade_risks()
    return {"risks": risks, "total": len(risks)}

@app.get("/telemetry")
async def get_telemetry():
    return monitor.telemetry.get_stats()

@app.get("/metrics")
async def get_metrics():
    return monitor.metrics.get_all()

@app.get("/drift")
async def get_drift():
    return {"events": monitor.drift_watcher.drift_events[-50:],
            "total": len(monitor.drift_watcher.drift_events)}

@app.get("/coverage")
async def get_coverage():
    return monitor.coverage_map.get_coverage()

@app.get("/audit")
async def get_audit(limit: int = Query(default=50, le=200)):
    trail_path = LOG_DIR / "audit_trail.jsonl"
    if not trail_path.exists():
        return {"entries": [], "total": 0}
    lines = trail_path.read_text(encoding="utf-8").strip().split("\n")
    entries = []
    for line in lines[-limit:]:
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return {"entries": entries, "total": len(lines)}

@app.get("/zones/history")
async def zone_history():
    return {"history": monitor.zoned_analyzer.zone_history[-50:]}

@app.post("/analyze")
async def deep_analyze(request: QueryRequest):
    snapshot = monitor.get_snapshot()
    system_data = snapshot.model_dump()
    analysis = monitor.deep_analyzer.analyze(request.query, system_data)
    return analysis

@app.get("/search/doctrine")
async def search_doctrine(q: str = Query(...), top_k: int = Query(default=5, le=20)):
    results = monitor.vector_search.search(q, top_k=top_k)
    return {
        "query": q,
        "results": [{"topic": d.topic, "score": round(s, 3), "conclusion": d.conclusion,
                      "confidence": d.confidence.value, "keywords": d.keywords} for d, s in results],
        "total": len(results),
    }

@app.post("/normalize")
async def normalize_text(text: str = Query(...)):
    normalized = monitor.normalizer.normalize(text)
    keywords = monitor.normalizer.extract_keywords(text)
    return {"original": text, "normalized": normalized, "keywords": keywords}

@app.get("/fragility")
async def compute_fragility(source_type: str = "automated_probe", corroboration: int = 1, recency_hours: float = 1.0):
    return monitor.fragility_scorer.score(source_type, corroboration, recency_hours)

@app.get("/history")
async def get_history(limit: int = Query(default=50, le=500)):
    return {"snapshots": [s.model_dump() for s in monitor.snapshots[-limit:]],
            "total": len(monitor.snapshots)}

@app.get("/recommendations")
async def get_recommendations():
    recs = []
    snapshot = monitor.get_snapshot()
    if snapshot.unhealthy > 0:
        unhealthy_services = [sid for sid, r in monitor.services.items()
                              if r.current_status == ServiceStatus.UNHEALTHY]
        recs.append({
            "priority": "HIGH",
            "action": "Investigate unhealthy services",
            "services": unhealthy_services,
            "detail": f"{snapshot.unhealthy} services are unhealthy and may need restart or investigation",
        })
    if snapshot.circuit_open > 0:
        circuit_services = [sid for sid, r in monitor.services.items()
                            if r.current_status == ServiceStatus.CIRCUIT_OPEN]
        recs.append({
            "priority": "HIGH",
            "action": "Review circuit-broken services",
            "services": circuit_services,
            "detail": "Circuit breakers indicate persistent downstream failures",
        })
    if snapshot.avg_latency_ms > 1000:
        recs.append({
            "priority": "MEDIUM",
            "action": "Investigate high latency",
            "detail": f"Average latency is {snapshot.avg_latency_ms:.0f}ms — above 1000ms threshold",
        })
    if snapshot.uptime_pct < 99.0:
        recs.append({
            "priority": "MEDIUM",
            "action": "Improve system reliability",
            "detail": f"Overall uptime is {snapshot.uptime_pct:.2f}% — below 99% target",
        })
    if not recs:
        recs.append({"priority": "INFO", "action": "System healthy", "detail": "No immediate actions needed"})
    return {"recommendations": recs, "snapshot": snapshot.model_dump()}

# ── Incident Endpoints ─────────────────────────────────────────────────────

@app.get("/incidents")
async def get_incidents():
    active = monitor.incident_manager.get_active()
    return {"incidents": [i.model_dump() for i in active], "total": len(active)}

@app.get("/incidents/{incident_id}")
async def get_incident(incident_id: str):
    inc = monitor.incident_manager.get_incident(incident_id)
    if not inc:
        raise HTTPException(status_code=404, detail=f"Incident {incident_id} not found")
    return inc.model_dump()

@app.post("/incidents/{incident_id}/resolve")
async def resolve_incident(incident_id: str, note: str = ""):
    success = monitor.incident_manager.resolve_incident(incident_id, note)
    if not success:
        raise HTTPException(status_code=404, detail=f"Incident {incident_id} not found")
    monitor.audit_trail.log("incident_resolved", {"incident_id": incident_id, "note": note})
    return {"status": "resolved", "incident_id": incident_id}

# ── Maintenance Endpoints ──────────────────────────────────────────────────

@app.post("/maintenance")
async def declare_maintenance(service_id: str, start_time: str,
                              duration_minutes: int, reason: str):
    window = monitor.maintenance_manager.declare_window(
        service_id, start_time, duration_minutes, reason)
    monitor.audit_trail.log("maintenance_declared", {
        "window_id": window.window_id, "service_id": service_id,
        "duration": duration_minutes, "reason": reason})
    return {"status": "declared", "window": window.model_dump()}

@app.get("/maintenance")
async def list_maintenance(service_id: Optional[str] = None):
    windows = monitor.maintenance_manager.all_windows(service_id)
    return {"windows": [w.model_dump() for w in windows], "total": len(windows)}

# ── Capacity Forecast Endpoints ────────────────────────────────────────────

@app.get("/capacity/{service_id}")
async def get_capacity(service_id: str, metric: str = "latency_ms",
                       threshold: float = 2000.0):
    forecast = monitor.get_capacity_forecast(service_id, metric, threshold)
    if not forecast:
        return {"service_id": service_id, "metric": metric,
                "forecast": None, "reason": "insufficient data"}
    return {"service_id": service_id, "forecast": forecast.model_dump()}

# ── Uptime Endpoints ───────────────────────────────────────────────────────

@app.get("/uptime/{service_id}")
async def get_uptime(service_id: str):
    if service_id not in monitor.services:
        raise HTTPException(status_code=404, detail=f"Service {service_id} not found")
    uptimes = monitor.get_service_uptime(service_id)
    return {"service_id": service_id, "uptime": uptimes}

@app.get("/sla")
async def sla_overview():
    results = []
    for sid, record in monitor.services.items():
        uptimes = monitor.get_service_uptime(sid)
        results.append({
            "service_id": sid, "name": record.definition.name,
            "uptime_24h": uptimes["24h"], "uptime_7d": uptimes["7d"],
            "uptime_30d": uptimes["30d"],
            "critical": record.definition.critical,
        })
    results.sort(key=lambda x: x["uptime_24h"])
    return {"sla_status": results, "total": len(results)}

# ── Flapping Detection Endpoint ────────────────────────────────────────────

@app.get("/flapping")
async def get_flapping():
    flapping_services = []
    for sid in monitor.services:
        if monitor.flapping_detector.is_flapping(sid):
            flapping_services.append({
                "service_id": sid,
                "state_changes": monitor.flapping_detector.changes_in_window(sid),
            })
    return {"flapping": flapping_services, "total": len(flapping_services)}

# ── Dashboard Endpoint ─────────────────────────────────────────────────────

@app.get("/dashboard")
async def dashboard():
    snapshot = monitor.get_snapshot()
    active_alerts = [a for a in monitor.alerts if not a.resolved]
    alert_by_sev: dict[str, int] = defaultdict(int)
    for a in active_alerts:
        alert_by_sev[a.severity.value] += 1
    flapping_count = sum(1 for sid in monitor.services
                         if monitor.flapping_detector.is_flapping(sid))
    active_incidents = monitor.incident_manager.get_active()
    active_maint = monitor.maintenance_manager.active_windows()
    cascade_risks = monitor.detect_cascade_risks()
    # Worst uptime services
    worst_uptime = []
    for sid in monitor.services:
        u24 = monitor.uptime_tracker.calculate_uptime(sid, 86400)
        worst_uptime.append({"service_id": sid, "uptime_24h": u24})
    worst_uptime.sort(key=lambda x: x["uptime_24h"])
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "snapshot": snapshot.model_dump(),
        "alerts_by_severity": dict(alert_by_sev),
        "total_active_alerts": len(active_alerts),
        "flapping_count": flapping_count,
        "active_incidents": len(active_incidents),
        "active_maintenance": len(active_maint),
        "cascade_risks": len(cascade_risks),
        "worst_uptime": worst_uptime[:10],
        "polling_active": monitor._polling_active,
        "doctrines_loaded": len(ALL_DOCTRINES),
    }

# ── Poll Trigger Endpoint ──────────────────────────────────────────────────

@app.post("/poll")
async def trigger_poll():
    results = await monitor.check_all()
    return {"status": "poll_complete", "services_checked": len(results)}

# ── Main ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting {ENGINE_ID} - {ENGINE_NAME} v{ENGINE_VERSION} on port {PORT}")
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")
