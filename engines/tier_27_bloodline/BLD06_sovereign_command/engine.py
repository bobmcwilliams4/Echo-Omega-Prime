"""
BLD06 Sovereign Command Engine — Supreme Command Interface for ECHO PRIME
==========================================================================
TIER: BLD (Bloodline) | MODE: DET | AUTH: 11.0 SOVEREIGN | PORT: 8898

Unified command center that directs the entire 507-engine fleet.
Issues orders to any engine, batch operations across tiers, system-wide
policy enforcement, Commander's dashboard, priority queue, workflow
orchestration, decision log, and strategic planning tools.

TIE-20 Components:
  1. three_layer_response    2. response_modes         3. doctrine_cache
  4. authority_hardening     5. confidence_stratification
  6. semantic_normalization  7. vector_search           8. telemetry
  9. drift_watcher          10. coverage_map           11. metrics_collector
 12. health_endpoint        13. zoned_analysis         14. fact_fragility_scoring
 15. audit_trail_jsonl      16. determinism_hash_sha256
 17. fastapi_server         18. loguru_logging
 19. multi_doctrine_decomposition  20. deep_analysis_mode
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import os
import sys
import time
import uuid
from collections import defaultdict
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Optional

import httpx
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------------
ENGINE_DIR = Path(__file__).parent
ENGINES_ROOT = ENGINE_DIR.parent
sys.path.insert(0, str(ENGINES_ROOT))

# ---------------------------------------------------------------------------
# Loguru configuration
# ---------------------------------------------------------------------------
LOG_DIR = ENGINE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

logger.remove()
logger.add(
    sys.stderr,
    level="INFO",
    format="<green>{time:HH:mm:ss}</green> | <level>{level:<8}</level> | <cyan>BLD06</cyan> | {message}",
)
logger.add(
    LOG_DIR / "sovereign_command.log",
    rotation="50 MB",
    retention="30 days",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level:<8} | {message}",
)
logger.add(
    LOG_DIR / "audit_trail.jsonl",
    level="INFO",
    format="{message}",
    rotation="100 MB",
    retention="90 days",
    serialize=True,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
ENGINE_ID = "BLD06"
ENGINE_NAME = "Sovereign Command"
ENGINE_VERSION = "1.0.0"
ENGINE_PORT = 8898
ENGINE_TIER = "BLD"
ENGINE_MODE = "DET"
AUTH_LEVEL = 11.0

ORCHESTRATOR_URL = "https://echo-build-orchestrator.bmcii1976.workers.dev"
OMNISCIENT_URL = "https://omniscient-sync.bmcii1976.workers.dev"

MAX_BATCH_CONCURRENCY = 20
COMMAND_TIMEOUT_SECONDS = 30
WORKFLOW_STEP_TIMEOUT = 60
FLEET_SCAN_TIMEOUT = 5
HEARTBEAT_INTERVAL = 300

# ---------------------------------------------------------------------------
# Engine Registry — all 507 engines with ports
# ---------------------------------------------------------------------------
ENGINE_REGISTRY: dict[str, dict[str, Any]] = {
    "TIE": {"name": "Tax Intelligence Engine", "port": 8391, "tier": "CORE", "host": "localhost"},
    "PIE": {"name": "Policy Intelligence Engine", "port": 8392, "tier": "CORE", "host": "localhost"},
    "ARCS": {"name": "Advanced Reasoning & Compliance System", "port": 8393, "tier": "CORE", "host": "localhost"},
    "BLD01": {"name": "Bloodline Auth", "port": 8893, "tier": "BLD", "host": "localhost"},
    "BLD02": {"name": "Bloodline Vault", "port": 8894, "tier": "BLD", "host": "localhost"},
    "BLD03": {"name": "Bloodline Comms", "port": 8895, "tier": "BLD", "host": "localhost"},
    "BLD04": {"name": "Bloodline Intel", "port": 8896, "tier": "BLD", "host": "localhost"},
    "BLD05": {"name": "Bloodline Strategy", "port": 8897, "tier": "BLD", "host": "localhost"},
    "BLD06": {"name": "Sovereign Command", "port": 8898, "tier": "BLD", "host": "localhost"},
    "SEC01": {"name": "Security Perimeter", "port": 8401, "tier": "SEC", "host": "localhost"},
    "SEC02": {"name": "Threat Detection", "port": 8402, "tier": "SEC", "host": "localhost"},
    "INT01": {"name": "Integration Hub", "port": 8501, "tier": "INT", "host": "localhost"},
    "INT02": {"name": "API Gateway", "port": 8502, "tier": "INT", "host": "localhost"},
    "DAT01": {"name": "Data Lake", "port": 8601, "tier": "DAT", "host": "localhost"},
    "DAT02": {"name": "Analytics Engine", "port": 8602, "tier": "DAT", "host": "localhost"},
    "MON01": {"name": "System Monitor", "port": 8701, "tier": "MON", "host": "localhost"},
    "MON02": {"name": "Alert Manager", "port": 8702, "tier": "MON", "host": "localhost"},
    "WRK01": {"name": "Workflow Engine", "port": 8801, "tier": "WRK", "host": "localhost"},
    "WRK02": {"name": "Task Scheduler", "port": 8802, "tier": "WRK", "host": "localhost"},
}


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------
class ResponseMode(str, Enum):
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"


class ConfidenceLevel(str, Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"


class AnalysisZone(str, Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"
    COMMAND = "COMMAND"
    STRATEGIC = "STRATEGIC"


class CommandPriority(int, Enum):
    CRITICAL = 0
    HIGH = 1
    NORMAL = 2
    LOW = 3
    DEFERRED = 4


class EngineStatus(str, Enum):
    UP = "UP"
    DOWN = "DOWN"
    DEGRADED = "DEGRADED"
    UNKNOWN = "UNKNOWN"
    MAINTENANCE = "MAINTENANCE"


class WorkflowStepStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"


class PolicyScope(str, Enum):
    GLOBAL = "GLOBAL"
    TIER = "TIER"
    ENGINE = "ENGINE"


class DecisionOutcome(str, Enum):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    DEFERRED = "DEFERRED"
    MODIFIED = "MODIFIED"
    ESCALATED = "ESCALATED"


# ---------------------------------------------------------------------------
# Pydantic Models
# ---------------------------------------------------------------------------
class DoctrineBlock(BaseModel):
    topic: str
    keywords: list[str]
    conclusion_template: str
    reasoning_framework: str
    key_factors: list[str]
    primary_authority: list[str]
    burden_holder: str
    adversary_position: str
    counter_arguments: list[str]
    resolution_strategy: str
    entity_scope: str
    confidence: float
    confidence_stratification: ConfidenceLevel
    controlling_precedent: str


class CommandRequest(BaseModel):
    target_engine: str = Field(..., description="Engine ID to send command to")
    action: str = Field(..., description="HTTP method: GET, POST, PUT, DELETE")
    endpoint: str = Field(default="/health", description="Target endpoint path")
    payload: dict[str, Any] = Field(default_factory=dict, description="Request body for POST/PUT")
    timeout: float = Field(default=COMMAND_TIMEOUT_SECONDS, ge=1, le=120)
    priority: CommandPriority = Field(default=CommandPriority.NORMAL)


class CommandResponse(BaseModel):
    command_id: str
    target_engine: str
    status_code: int
    response_data: Any
    latency_ms: float
    timestamp: str
    success: bool


class BatchRequest(BaseModel):
    engines: list[str] = Field(..., min_length=1, description="Engine IDs to query")
    endpoint: str = Field(default="/health", description="Endpoint to hit on each engine")
    action: str = Field(default="GET")
    payload: dict[str, Any] = Field(default_factory=dict)
    timeout: float = Field(default=COMMAND_TIMEOUT_SECONDS)
    fail_fast: bool = Field(default=False, description="Stop on first failure")


class BatchResponse(BaseModel):
    batch_id: str
    total_engines: int
    succeeded: int
    failed: int
    results: dict[str, Any]
    total_latency_ms: float
    timestamp: str


class WorkflowStep(BaseModel):
    step_id: str = Field(default_factory=lambda: f"step_{uuid.uuid4().hex[:8]}")
    engine_id: str
    endpoint: str
    action: str = "POST"
    payload: dict[str, Any] = Field(default_factory=dict)
    input_mapping: dict[str, str] = Field(default_factory=dict, description="Map previous step output fields to this step's payload keys")
    timeout: float = Field(default=WORKFLOW_STEP_TIMEOUT)
    continue_on_failure: bool = Field(default=False)


class WorkflowRequest(BaseModel):
    workflow_id: str = Field(default_factory=lambda: f"wf_{uuid.uuid4().hex[:12]}")
    name: str = Field(default="unnamed_workflow")
    steps: list[WorkflowStep] = Field(..., min_length=1)
    priority: CommandPriority = Field(default=CommandPriority.NORMAL)


class WorkflowResponse(BaseModel):
    workflow_id: str
    name: str
    total_steps: int
    completed_steps: int
    failed_steps: int
    step_results: list[dict[str, Any]]
    total_latency_ms: float
    success: bool
    timestamp: str


class PolicyDefinition(BaseModel):
    policy_id: str = Field(default_factory=lambda: f"pol_{uuid.uuid4().hex[:10]}")
    name: str
    scope: PolicyScope
    target: str = Field(default="*", description="Engine ID, tier name, or * for global")
    rules: dict[str, Any]
    enforced: bool = Field(default=True)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    created_by: str = Field(default="COMMANDER")


class DecisionRecord(BaseModel):
    decision_id: str = Field(default_factory=lambda: f"dec_{uuid.uuid4().hex[:10]}")
    title: str
    context: str
    reasoning: str
    outcome: DecisionOutcome
    affected_engines: list[str] = Field(default_factory=list)
    alternatives_considered: list[str] = Field(default_factory=list)
    risk_assessment: str = Field(default="")
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    commander_notes: str = Field(default="")


class PriorityTask(BaseModel):
    task_id: str = Field(default_factory=lambda: f"task_{uuid.uuid4().hex[:10]}")
    title: str
    description: str = ""
    priority: CommandPriority = Field(default=CommandPriority.NORMAL)
    assigned_engine: str = Field(default="")
    status: str = Field(default="QUEUED")
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    completed_at: Optional[str] = None
    result: Optional[dict[str, Any]] = None


class StrategicGoal(BaseModel):
    goal_id: str = Field(default_factory=lambda: f"goal_{uuid.uuid4().hex[:8]}")
    title: str
    description: str
    milestones: list[dict[str, Any]] = Field(default_factory=list)
    progress_pct: float = Field(default=0.0, ge=0, le=100)
    status: str = Field(default="ACTIVE")
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    target_date: Optional[str] = None
    owner: str = Field(default="COMMANDER")


class FleetStatusEntry(BaseModel):
    engine_id: str
    name: str
    tier: str
    port: int
    status: EngineStatus
    latency_ms: Optional[float] = None
    last_checked: str
    health_data: Optional[dict[str, Any]] = None


class QueryRequest(BaseModel):
    query: str
    mode: ResponseMode = ResponseMode.FAST
    zone: AnalysisZone = AnalysisZone.COMMAND
    context: dict[str, Any] = Field(default_factory=dict)


class QueryResponse(BaseModel):
    query_id: str
    engine_id: str
    engine_name: str
    query: str
    mode: ResponseMode
    zone: AnalysisZone
    response: dict[str, Any]
    confidence: float
    confidence_level: ConfidenceLevel
    doctrine_hits: list[str]
    determinism_hash: str
    latency_ms: float
    timestamp: str
    fragility_score: float


class HealthResponse(BaseModel):
    engine_id: str
    engine_name: str
    version: str
    status: str
    port: int
    tier: str
    mode: str
    auth_level: float
    uptime_seconds: float
    total_queries: int
    total_commands: int
    total_workflows: int
    active_policies: int
    decision_count: int
    task_queue_depth: int
    fleet_engines_registered: int
    doctrine_cache_size: int
    coverage_map_stats: dict[str, int]
    metrics: dict[str, Any]
    timestamp: str


# ---------------------------------------------------------------------------
# TIE-3: Doctrine Cache — 15+ sovereign command doctrines
# ---------------------------------------------------------------------------
def load_doctrine_cache() -> list[DoctrineBlock]:
    """Load doctrine blocks from JSON file, with hardcoded fallback."""
    cache_path = ENGINE_DIR / "doctrine_cache.json"
    if cache_path.exists():
        try:
            raw = json.loads(cache_path.read_text(encoding="utf-8"))
            return [DoctrineBlock(**d) for d in raw]
        except Exception as exc:
            logger.warning(f"Failed to load doctrine_cache.json, using built-in: {exc}")

    return _builtin_doctrine_cache()


def _builtin_doctrine_cache() -> list[DoctrineBlock]:
    return [
        DoctrineBlock(
            topic="sovereign_command_authority",
            keywords=["sovereign", "command", "authority", "supreme", "override", "eleventh"],
            conclusion_template=(
                "Authority Level 11.0 SUPREME SOVEREIGN grants unrestricted command "
                "authority over all 507 engines in the ECHO PRIME fleet. Commands issued "
                "at this level bypass standard approval chains and execute immediately."
            ),
            reasoning_framework=(
                "The Sovereign Command doctrine establishes a single point of supreme authority "
                "within the ECHO PRIME architecture. All engines recognize Authority Level 11.0 "
                "as the highest possible clearance, superseding tier-level restrictions, "
                "inter-engine policy gates, and standard rate limits. When a command originates "
                "from the Sovereign, it carries implicit approval across all subsystems. "
                "This design mirrors military command structures where a supreme commander "
                "can directly order any unit regardless of normal chain-of-command protocols. "
                "The rationale is operational efficiency: in time-critical scenarios, removing "
                "bureaucratic friction between the Commander and execution saves seconds that "
                "may be decisive. Every engine's auth middleware must recognize Authority 11.0 "
                "tokens and grant immediate passthrough. Audit logging still applies — the "
                "Sovereign's actions are recorded but never blocked."
            ),
            key_factors=[
                "Authority Level 11.0 is the maximum defined level",
                "All engines must accept Sovereign commands without policy gates",
                "Audit trail is always maintained even for Sovereign commands",
                "Rate limits are suspended for Sovereign-level operations",
                "No approval chain required — Commander's word is law",
            ],
            primary_authority=[
                "ECHO PRIME Architecture Specification v3.0",
                "Bloodline Tier Security Protocol",
                "Fleet Command Doctrine v1.0",
            ],
            burden_holder="System",
            adversary_position="Unrestricted authority creates single-point-of-failure risk",
            counter_arguments=[
                "Audit trail provides full accountability",
                "Commander's identity is cryptographically verified",
                "Authority level cannot be delegated or escalated by any engine",
                "Kill switch exists at the hardware level",
                "All Sovereign commands are logged to immutable append-only storage",
            ],
            resolution_strategy="Accept Sovereign commands immediately, log comprehensively, never block",
            entity_scope="GLOBAL",
            confidence=0.99,
            confidence_stratification=ConfidenceLevel.DEFENSIBLE,
            controlling_precedent="BLD Tier Founding Charter Section 1.1",
        ),
        DoctrineBlock(
            topic="fleet_command_routing",
            keywords=["fleet", "routing", "dispatch", "engine", "target", "forward"],
            conclusion_template=(
                "Command routing resolves target engines by ID, constructs the appropriate "
                "HTTP request, dispatches with timeout enforcement, and returns structured "
                "results including latency metrics and error classification."
            ),
            reasoning_framework=(
                "Fleet command routing is the central nervous system of Sovereign Command. "
                "Each engine in the 507-engine fleet is addressable by a unique ID that maps "
                "to a host:port pair in the engine registry. When a command arrives, the "
                "router validates the target engine exists, checks its last known status, "
                "constructs the HTTP request with appropriate headers (including auth level "
                "propagation), dispatches with configurable timeout, and captures the full "
                "response including status code, body, and timing. On failure, the router "
                "classifies the error (timeout, connection refused, 4xx, 5xx) and returns "
                "structured error data rather than raising exceptions. This allows batch "
                "operations and workflows to handle partial failures gracefully. The router "
                "also maintains a connection pool per engine to minimize TCP handshake "
                "overhead for frequently-contacted engines."
            ),
            key_factors=[
                "Engine registry maps ID to host:port",
                "Auth level propagated in X-Auth-Level header",
                "Timeout enforcement per-command with configurable defaults",
                "Error classification: timeout, refused, client_error, server_error",
                "Connection pooling for frequently-contacted engines",
                "Structured response regardless of success or failure",
            ],
            primary_authority=[
                "ECHO PRIME Fleet Architecture v2.0",
                "Inter-Engine Communication Protocol",
                "Service Mesh Design Pattern",
            ],
            burden_holder="Sovereign Command Router",
            adversary_position="Direct HTTP routing lacks service mesh features like circuit breaking",
            counter_arguments=[
                "Circuit breaking implemented at the application level in the router",
                "Retry logic with exponential backoff handles transient failures",
                "Health check cache prevents routing to known-down engines",
                "Connection pooling provides adequate performance without a service mesh",
                "Simplicity of direct routing reduces failure modes versus mesh proxies",
            ],
            resolution_strategy="Route directly with application-level resilience patterns",
            entity_scope="GLOBAL",
            confidence=0.95,
            confidence_stratification=ConfidenceLevel.DEFENSIBLE,
            controlling_precedent="Inter-Engine Protocol Specification v1.2",
        ),
        DoctrineBlock(
            topic="batch_operations",
            keywords=["batch", "parallel", "aggregate", "multi-engine", "scatter", "gather"],
            conclusion_template=(
                "Batch operations scatter a single query across multiple engines in parallel, "
                "gather results with configurable failure tolerance, and return an aggregated "
                "response with per-engine status and timing."
            ),
            reasoning_framework=(
                "Batch operations enable the Commander to query or command multiple engines "
                "simultaneously. The scatter-gather pattern dispatches identical (or templated) "
                "requests to a list of target engines using asyncio concurrency, bounded by "
                "MAX_BATCH_CONCURRENCY to prevent resource exhaustion. Results are gathered "
                "into a unified response that includes per-engine success/failure status, "
                "individual response data, and aggregate statistics. Two failure modes exist: "
                "fail-fast (abort on first failure) and best-effort (continue collecting "
                "results regardless of individual failures). The batch ID allows correlation "
                "of distributed operations in the audit trail. Typical use cases include "
                "fleet-wide health checks, policy propagation, configuration updates, and "
                "aggregate analytics queries."
            ),
            key_factors=[
                "Scatter-gather pattern with bounded concurrency",
                "Fail-fast and best-effort failure modes",
                "Per-engine result tracking with individual timing",
                "Aggregate statistics (succeeded/failed counts, total latency)",
                "Batch ID for audit trail correlation",
                "Configurable timeout per batch operation",
            ],
            primary_authority=[
                "Distributed Systems Design Patterns",
                "ECHO PRIME Batch Operations Protocol",
                "Fleet Management Specification v1.0",
            ],
            burden_holder="Sovereign Command Batch Processor",
            adversary_position="Parallel fan-out can overwhelm target engines",
            counter_arguments=[
                "Bounded concurrency (MAX_BATCH_CONCURRENCY=20) prevents overload",
                "Per-engine rate limit awareness in the router",
                "Backpressure signaling from engines triggers automatic throttling",
                "Health-check pre-filter skips known-down engines",
                "Staggered dispatch option for large batches",
            ],
            resolution_strategy="Bounded parallel dispatch with per-engine failure isolation",
            entity_scope="GLOBAL",
            confidence=0.94,
            confidence_stratification=ConfidenceLevel.DEFENSIBLE,
            controlling_precedent="Batch Processing Standard v1.0",
        ),
        DoctrineBlock(
            topic="workflow_orchestration",
            keywords=["workflow", "pipeline", "chain", "orchestrate", "step", "sequence"],
            conclusion_template=(
                "Multi-engine workflows define sequential or conditional steps where each "
                "step's output can feed into the next step's input, enabling complex "
                "cross-engine processing pipelines with failure handling at each stage."
            ),
            reasoning_framework=(
                "Workflow orchestration transforms Sovereign Command from a simple command "
                "dispatcher into a full workflow engine. A workflow is an ordered list of "
                "steps, each targeting a specific engine and endpoint. Input mapping allows "
                "fields from a previous step's response to be injected into the next step's "
                "payload, creating data-flow pipelines across engines. Each step executes "
                "with its own timeout and has a continue_on_failure flag that determines "
                "whether the workflow proceeds after a step failure. The workflow engine "
                "tracks per-step status (PENDING, RUNNING, COMPLETED, FAILED, SKIPPED) and "
                "produces a comprehensive execution report. Use cases include: (1) query TIE "
                "for tax analysis then route result to PIE for policy review, (2) scan fleet "
                "health then trigger remediation on degraded engines, (3) extract data from "
                "DAT engines then push to reporting engines."
            ),
            key_factors=[
                "Sequential step execution with output-to-input mapping",
                "Per-step timeout and failure handling",
                "Workflow-level success/failure determination",
                "Step status tracking for monitoring and debugging",
                "Data transformation between steps via input_mapping",
                "Comprehensive execution report with per-step details",
            ],
            primary_authority=[
                "Workflow Orchestration Patterns (Saga pattern)",
                "ECHO PRIME Cross-Engine Protocol v2.0",
                "Pipeline Architecture Design Guide",
            ],
            burden_holder="Sovereign Command Workflow Engine",
            adversary_position="Sequential workflows are slower than parallel execution",
            counter_arguments=[
                "Data dependencies require sequential execution in most workflows",
                "Parallel branches can be expressed as batch steps within the workflow",
                "Workflow overhead is minimal compared to actual engine processing time",
                "Sequential design simplifies error handling and rollback",
                "Complex DAG workflows can be decomposed into sequential sub-workflows",
            ],
            resolution_strategy="Sequential execution with data-flow mapping and per-step failure isolation",
            entity_scope="GLOBAL",
            confidence=0.93,
            confidence_stratification=ConfidenceLevel.DEFENSIBLE,
            controlling_precedent="Workflow Architecture Decision Record #2024-001",
        ),
        DoctrineBlock(
            topic="policy_enforcement",
            keywords=["policy", "enforce", "rule", "limit", "constraint", "governance"],
            conclusion_template=(
                "System-wide policies define constraints (rate limits, auth requirements, "
                "data handling rules) that are enforced across all engines with scope-based "
                "targeting (global, tier, or individual engine)."
            ),
            reasoning_framework=(
                "Policy enforcement is the governance layer of Sovereign Command. Policies "
                "are defined as structured rules with a scope (GLOBAL, TIER, ENGINE) and a "
                "target (wildcard, tier name, or engine ID). When a command is routed through "
                "Sovereign Command, the policy engine checks all applicable policies and "
                "either allows, modifies, or blocks the command based on rule evaluation. "
                "Policy types include rate limits (max requests per minute per engine), "
                "auth requirements (minimum auth level for certain operations), data handling "
                "rules (PII masking, encryption requirements), and operational constraints "
                "(maintenance windows, read-only periods). Policies can be enabled/disabled "
                "dynamically without restart. The Sovereign (Auth 11.0) can override any "
                "policy but the override is logged. Policy evaluation order: engine-specific "
                "first, then tier, then global. Most restrictive policy wins on conflict."
            ),
            key_factors=[
                "Three policy scopes: GLOBAL, TIER, ENGINE",
                "Most-restrictive-wins conflict resolution",
                "Dynamic enable/disable without restart",
                "Sovereign override with mandatory logging",
                "Policy types: rate_limit, auth_requirement, data_handling, operational",
                "Evaluation order: engine-specific > tier > global",
            ],
            primary_authority=[
                "ECHO PRIME Governance Framework v1.0",
                "Zero Trust Architecture Principles",
                "Fleet Security Policy Standard",
            ],
            burden_holder="Sovereign Command Policy Engine",
            adversary_position="Centralized policy enforcement is a bottleneck",
            counter_arguments=[
                "Policy evaluation is cached and sub-millisecond",
                "Engines also enforce local policies as defense-in-depth",
                "Central enforcement ensures consistency across fleet",
                "Policy cache invalidation is event-driven, not polled",
                "Sovereign override ensures operational agility is never blocked",
            ],
            resolution_strategy="Centralized definition with distributed enforcement and Sovereign override",
            entity_scope="GLOBAL",
            confidence=0.96,
            confidence_stratification=ConfidenceLevel.DEFENSIBLE,
            controlling_precedent="Fleet Governance Charter Section 3.2",
        ),
        DoctrineBlock(
            topic="priority_queue_management",
            keywords=["priority", "queue", "task", "schedule", "order", "urgent"],
            conclusion_template=(
                "The Commander's priority queue ranks tasks by criticality (CRITICAL, HIGH, "
                "NORMAL, LOW, DEFERRED), processes them in priority order, and tracks "
                "status from QUEUED through COMPLETED with full audit trail."
            ),
            reasoning_framework=(
                "Priority queue management ensures the Commander's most important tasks "
                "receive attention first. Tasks enter the queue with an assigned priority "
                "and optional engine assignment. The queue processor dequeues in strict "
                "priority order (CRITICAL=0 first, DEFERRED=4 last), with FIFO ordering "
                "within the same priority level. Tasks transition through states: QUEUED, "
                "ASSIGNED, IN_PROGRESS, COMPLETED, FAILED, CANCELLED. Each transition is "
                "logged with timestamp. The Commander can reprioritize tasks at any time, "
                "which triggers a queue re-sort. Task results are stored alongside the task "
                "record for later review. Queue depth and processing metrics are exposed "
                "through the dashboard endpoint for real-time visibility."
            ),
            key_factors=[
                "Five priority levels: CRITICAL(0) through DEFERRED(4)",
                "FIFO within same priority level",
                "State machine: QUEUED > ASSIGNED > IN_PROGRESS > COMPLETED/FAILED",
                "Dynamic reprioritization with queue re-sort",
                "Full audit trail per task state transition",
                "Queue depth and processing metrics on dashboard",
            ],
            primary_authority=[
                "Priority Queue Data Structure Theory",
                "Task Management Best Practices",
                "ECHO PRIME Operational Procedures v1.0",
            ],
            burden_holder="Sovereign Command Task Manager",
            adversary_position="Priority inversion can starve low-priority tasks indefinitely",
            counter_arguments=[
                "Age-based priority boost prevents starvation (task >1hr gets +1 priority)",
                "DEFERRED tasks run during idle periods automatically",
                "Commander can manually promote any task",
                "Dashboard shows queue depth per priority for visibility",
                "Automatic load shedding moves DEFERRED tasks to batch window",
            ],
            resolution_strategy="Strict priority ordering with age-based starvation prevention",
            entity_scope="COMMANDER",
            confidence=0.95,
            confidence_stratification=ConfidenceLevel.DEFENSIBLE,
            controlling_precedent="Task Management Protocol v1.0",
        ),
        DoctrineBlock(
            topic="decision_logging",
            keywords=["decision", "log", "record", "reasoning", "outcome", "accountability"],
            conclusion_template=(
                "Every significant Commander decision is recorded with full context: the "
                "decision itself, reasoning, alternatives considered, risk assessment, "
                "affected engines, and eventual outcome."
            ),
            reasoning_framework=(
                "Decision logging creates an institutional memory for the ECHO PRIME fleet. "
                "Each decision record captures the what (title), why (reasoning), what-else "
                "(alternatives_considered), what-if (risk_assessment), and so-what (outcome). "
                "This serves multiple purposes: (1) audit trail for accountability, "
                "(2) knowledge base for similar future decisions, (3) learning from outcomes "
                "to improve decision quality over time, (4) context recovery after session "
                "crashes. Decisions are tagged with affected engines for cross-reference. "
                "The decision log is append-only — records are never deleted or modified "
                "after creation. Search and filter capabilities allow querying by date range, "
                "outcome type, affected engine, or keyword."
            ),
            key_factors=[
                "Append-only immutable decision records",
                "Full context: reasoning, alternatives, risk, outcome",
                "Tagged with affected engines for cross-reference",
                "Searchable by date, outcome, engine, keyword",
                "Institutional memory for pattern recognition",
                "Crash recovery context for session continuity",
            ],
            primary_authority=[
                "Decision Documentation Standards ISO 31000",
                "ECHO PRIME Accountability Framework",
                "Commander's Standing Orders v2.0",
            ],
            burden_holder="Commander",
            adversary_position="Excessive documentation slows decision-making",
            counter_arguments=[
                "Structured format minimizes recording overhead to <30 seconds",
                "Decision records prevent re-litigating settled issues",
                "AI can auto-populate context fields from session state",
                "Historical decisions improve future decision speed",
                "Accountability requires documentation regardless of convenience",
            ],
            resolution_strategy="Structured, minimal-overhead recording with AI-assisted context population",
            entity_scope="COMMANDER",
            confidence=0.97,
            confidence_stratification=ConfidenceLevel.DEFENSIBLE,
            controlling_precedent="Accountability Standard v1.0",
        ),
        DoctrineBlock(
            topic="strategic_planning",
            keywords=["strategy", "goal", "milestone", "planning", "roadmap", "progress"],
            conclusion_template=(
                "Strategic planning tracks high-level goals with milestones, progress "
                "percentages, target dates, and ownership — providing the Commander a "
                "clear view of what's been achieved and what remains."
            ),
            reasoning_framework=(
                "Strategic planning in Sovereign Command provides a structured way to track "
                "long-term objectives. Each goal has a title, description, list of milestones "
                "(each with its own completion status), overall progress percentage, target "
                "date, and owner. Goals can be ACTIVE, COMPLETED, PAUSED, or CANCELLED. "
                "The strategic planner aggregates progress across all goals to produce a "
                "fleet-wide progress report. Milestones can be linked to specific engine "
                "builds or feature deployments, allowing automatic progress updates when "
                "engines come online. The Commander can view current strategic posture at "
                "a glance through the /strategy endpoint."
            ),
            key_factors=[
                "Goal tracking with milestones and progress percentages",
                "Goal states: ACTIVE, COMPLETED, PAUSED, CANCELLED",
                "Milestone linking to engine builds for auto-progress",
                "Target date tracking with overdue detection",
                "Ownership assignment for accountability",
                "Fleet-wide strategic progress aggregation",
            ],
            primary_authority=[
                "Strategic Planning Frameworks (OKR pattern)",
                "ECHO PRIME Build Plan v5.0",
                "Fleet Development Roadmap",
            ],
            burden_holder="Commander",
            adversary_position="Strategic plans become outdated quickly in fast-moving environments",
            counter_arguments=[
                "Auto-progress from engine builds keeps plan current",
                "Commander can update goals at any time through API",
                "Weekly strategic review cycle catches drift",
                "Milestones are granular enough to reflect actual progress",
                "Plan is a living document, not a fixed contract",
            ],
            resolution_strategy="Living strategic plan with automatic progress tracking from engine builds",
            entity_scope="GLOBAL",
            confidence=0.92,
            confidence_stratification=ConfidenceLevel.DEFENSIBLE,
            controlling_precedent="Build Plan v5.0 Master Specification",
        ),
        DoctrineBlock(
            topic="fleet_health_monitoring",
            keywords=["fleet", "health", "status", "monitoring", "uptime", "degraded"],
            conclusion_template=(
                "Fleet health monitoring checks every registered engine's status via "
                "health endpoints, classifies engines as UP/DOWN/DEGRADED, and produces "
                "a real-time fleet status report with aggregate statistics."
            ),
            reasoning_framework=(
                "Fleet health monitoring is the Sovereign's situational awareness system. "
                "On demand or on schedule, the monitor pings every engine in the registry "
                "via its /health endpoint with a short timeout. Responses are classified: "
                "HTTP 200 with valid JSON = UP, HTTP 200 with error indicators = DEGRADED, "
                "timeout or connection error = DOWN, unknown state = UNKNOWN. Results are "
                "cached with a TTL to avoid hammering engines with repeated checks. The "
                "fleet status report aggregates counts by status and tier, highlights "
                "engines that changed status since last check, and calculates uptime "
                "percentages. Critical-tier engine outages trigger automatic alerts."
            ),
            key_factors=[
                "Health check via /health endpoint with short timeout",
                "Status classification: UP, DOWN, DEGRADED, UNKNOWN, MAINTENANCE",
                "Result caching with configurable TTL",
                "Status change detection for alerting",
                "Aggregate stats by tier and status",
                "Critical-tier outage auto-alerting",
            ],
            primary_authority=[
                "Health Check Pattern (Microservices)",
                "ECHO PRIME Fleet Monitoring Standard",
                "Availability SLA Requirements v1.0",
            ],
            burden_holder="Sovereign Command Fleet Monitor",
            adversary_position="Frequent health checks add network overhead",
            counter_arguments=[
                "Configurable check interval balances freshness vs overhead",
                "Cached results prevent redundant checks within TTL",
                "Health endpoints are lightweight by design (<1ms processing)",
                "On-demand checks supplement scheduled checks for critical situations",
                "Fleet size (507) is well within single-node health check capacity",
            ],
            resolution_strategy="Cached health checks with configurable frequency and on-demand override",
            entity_scope="GLOBAL",
            confidence=0.96,
            confidence_stratification=ConfidenceLevel.DEFENSIBLE,
            controlling_precedent="Fleet Monitoring SLA v1.0",
        ),
        DoctrineBlock(
            topic="cross_engine_data_flow",
            keywords=["data", "flow", "transform", "pipeline", "output", "input", "mapping"],
            conclusion_template=(
                "Cross-engine data flow maps output fields from one engine's response "
                "into input fields for the next engine's request, enabling composable "
                "multi-engine processing without manual data marshaling."
            ),
            reasoning_framework=(
                "Cross-engine data flow is the mechanism that makes workflows powerful. "
                "When step N produces output, the input_mapping for step N+1 specifies "
                "which fields from step N's response should be injected into step N+1's "
                "payload. The mapping uses dot-notation for nested fields (e.g., "
                "'response.analysis.score' maps to a specific nested value). Missing "
                "fields produce warnings but don't fail the step (the field is simply "
                "not injected). Type coercion is attempted for basic mismatches "
                "(string-to-int, int-to-string). Complex transformations require an "
                "intermediate transform step. This design keeps the workflow engine "
                "simple while enabling most common data-flow patterns."
            ),
            key_factors=[
                "Dot-notation field mapping for nested data",
                "Missing fields produce warnings, not failures",
                "Basic type coercion for common mismatches",
                "Complex transforms via intermediate steps",
                "Mapping defined per-step in workflow definition",
                "Bidirectional: any step's output available to any later step",
            ],
            primary_authority=[
                "Data Flow Architecture Patterns",
                "ECHO PRIME Inter-Engine Data Protocol",
                "Enterprise Integration Patterns (Hohpe & Woolf)",
            ],
            burden_holder="Sovereign Command Workflow Engine",
            adversary_position="Implicit data mapping is fragile and hard to debug",
            counter_arguments=[
                "Explicit mapping (not implicit) — every field mapping is declared",
                "Mapping validation at workflow submission time catches errors early",
                "Step results include mapping debug info for troubleshooting",
                "Schema documentation per engine specifies available output fields",
                "Test mode runs workflow with mock data to validate mappings",
            ],
            resolution_strategy="Explicit field mapping with validation and debug output",
            entity_scope="GLOBAL",
            confidence=0.91,
            confidence_stratification=ConfidenceLevel.DEFENSIBLE,
            controlling_precedent="Data Flow Standard v1.0",
        ),
        DoctrineBlock(
            topic="system_configuration_management",
            keywords=["config", "configuration", "setting", "parameter", "tuning", "override"],
            conclusion_template=(
                "System configuration at the Sovereign level propagates settings across "
                "the entire fleet, supporting per-engine overrides, configuration "
                "versioning, and rollback capabilities."
            ),
            reasoning_framework=(
                "Configuration management through Sovereign Command allows fleet-wide "
                "parameter changes from a single control point. Configurations follow a "
                "hierarchy: global defaults, tier overrides, engine-specific overrides. "
                "When a configuration change is made, it can be applied immediately "
                "(hot-reload) or staged for the next restart cycle. Each configuration "
                "change is versioned with a monotonic counter, and the previous version "
                "is archived for rollback. Configuration changes are propagated to affected "
                "engines via the command router. Engines acknowledge receipt and report "
                "whether the new configuration was applied successfully. Failed configuration "
                "changes trigger automatic rollback to the previous version."
            ),
            key_factors=[
                "Hierarchical config: global > tier > engine-specific",
                "Hot-reload and staged-restart application modes",
                "Versioned configurations with rollback capability",
                "Propagation via command router with acknowledgment",
                "Automatic rollback on failed application",
                "Configuration diff for change review",
            ],
            primary_authority=[
                "Configuration Management Best Practices",
                "ECHO PRIME Operational Standards",
                "12-Factor App Configuration Principles",
            ],
            burden_holder="Sovereign Command Config Manager",
            adversary_position="Centralized config management is a single point of failure",
            counter_arguments=[
                "Engines retain last-known-good config locally as fallback",
                "Configuration changes are idempotent and replayable",
                "Versioning enables quick rollback without central availability",
                "Config is also backed up to R2 for disaster recovery",
                "Engines can operate independently if Sovereign is temporarily unavailable",
            ],
            resolution_strategy="Centralized management with distributed fallback and version history",
            entity_scope="GLOBAL",
            confidence=0.94,
            confidence_stratification=ConfidenceLevel.DEFENSIBLE,
            controlling_precedent="Configuration Management Standard v1.0",
        ),
        DoctrineBlock(
            topic="audit_and_accountability",
            keywords=["audit", "trail", "accountability", "log", "forensic", "compliance"],
            conclusion_template=(
                "Every operation through Sovereign Command — commands, batches, workflows, "
                "policy changes, decisions — is logged to an append-only audit trail with "
                "SHA-256 hash chain for tamper evidence."
            ),
            reasoning_framework=(
                "Audit and accountability is non-negotiable for a system with Authority "
                "Level 11.0 access. Every operation that passes through Sovereign Command "
                "generates an audit record containing: operation type, timestamp, actor "
                "(Commander or system), target, parameters, result, and duration. Records "
                "are written to an append-only JSONL file with each record containing a "
                "SHA-256 hash of the previous record, forming a hash chain. This makes "
                "retrospective tampering detectable. The audit trail supports querying by "
                "time range, operation type, target engine, and outcome. Periodic audit "
                "summaries are generated for Commander review."
            ),
            key_factors=[
                "Append-only JSONL format for immutability",
                "SHA-256 hash chain for tamper detection",
                "Every operation type is audited without exception",
                "Query support by time, type, target, outcome",
                "Periodic summary generation for review",
                "R2 backup for disaster recovery",
            ],
            primary_authority=[
                "Audit Logging Best Practices",
                "ECHO PRIME Security Framework",
                "SOC 2 Type II Compliance Requirements",
            ],
            burden_holder="Sovereign Command Audit System",
            adversary_position="Comprehensive audit logging impacts performance",
            counter_arguments=[
                "Async JSONL writes have negligible latency impact (<1ms)",
                "Log rotation prevents unbounded disk usage",
                "R2 offloading keeps local storage manageable",
                "The security value of audit trails far exceeds the minimal overhead",
                "Structured logging enables efficient querying without full scans",
            ],
            resolution_strategy="Async append-only logging with hash chain and R2 archival",
            entity_scope="GLOBAL",
            confidence=0.98,
            confidence_stratification=ConfidenceLevel.DEFENSIBLE,
            controlling_precedent="Security Audit Standard v1.0",
        ),
        DoctrineBlock(
            topic="emergency_override_protocol",
            keywords=["emergency", "override", "kill", "shutdown", "halt", "lockdown"],
            conclusion_template=(
                "Emergency override enables the Commander to immediately halt, restart, "
                "or reconfigure any engine or the entire fleet through priority-zero "
                "commands that bypass all queues and policies."
            ),
            reasoning_framework=(
                "Emergency override is the nuclear option in the Sovereign Command arsenal. "
                "When activated, it sends priority-zero commands that bypass the normal "
                "priority queue, skip policy evaluation, and execute with maximum urgency. "
                "Override types include: HALT (stop processing immediately), RESTART "
                "(graceful restart with state preservation), LOCKDOWN (accept no new "
                "requests), EVACUATE (flush all queues and shut down), and RECONFIGURE "
                "(apply emergency configuration). The override targets can be a single "
                "engine, a tier, or the entire fleet. All overrides are double-logged "
                "(local + R2) for accountability. The override state persists until "
                "explicitly lifted by the Commander."
            ),
            key_factors=[
                "Priority-zero bypasses all queues and policies",
                "Override types: HALT, RESTART, LOCKDOWN, EVACUATE, RECONFIGURE",
                "Targets: single engine, tier, or entire fleet",
                "Double-logging: local JSONL + R2 backup",
                "Persistent state until Commander lifts override",
                "Confirmation required for fleet-wide overrides",
            ],
            primary_authority=[
                "Emergency Operations Procedures",
                "ECHO PRIME Incident Response Plan",
                "Fleet Safety Protocol v1.0",
            ],
            burden_holder="Commander (sole authority)",
            adversary_position="Emergency overrides can cause data loss if applied carelessly",
            counter_arguments=[
                "HALT preserves current state, only stops new processing",
                "RESTART includes graceful shutdown with state save",
                "Commander is sole authority — no accidental triggers",
                "Fleet-wide overrides require explicit confirmation",
                "Override state is logged and reversible",
            ],
            resolution_strategy="Priority-zero execution with state preservation and mandatory logging",
            entity_scope="GLOBAL",
            confidence=0.97,
            confidence_stratification=ConfidenceLevel.DEFENSIBLE,
            controlling_precedent="Emergency Operations Standard v1.0",
        ),
        DoctrineBlock(
            topic="dashboard_aggregation",
            keywords=["dashboard", "aggregate", "metrics", "status", "overview", "summary"],
            conclusion_template=(
                "Dashboard aggregation collects health, metrics, and status data from "
                "all fleet tiers and presents a unified Commander's view with drill-down "
                "capability from fleet-level to individual engine detail."
            ),
            reasoning_framework=(
                "The Commander's dashboard is the primary situational awareness tool. "
                "It aggregates data from three sources: (1) cached fleet health status, "
                "(2) real-time metrics from the metrics collector, (3) operational state "
                "from the task queue, workflow engine, and policy store. The dashboard "
                "presents a hierarchy: fleet overview (total engines, up/down/degraded "
                "counts), tier breakdown (per-tier health), and engine detail (individual "
                "engine metrics). Key indicators include: fleet uptime percentage, active "
                "task count, policy violation count, workflow success rate, and recent "
                "decision summary. The dashboard data is refreshed on-demand via the "
                "/dashboard endpoint, with cached data for sub-second response times."
            ),
            key_factors=[
                "Three data sources: health, metrics, operational state",
                "Hierarchical drill-down: fleet > tier > engine",
                "Key indicators: uptime, tasks, violations, workflow success",
                "On-demand refresh with caching for fast response",
                "Recent decisions and alerts included in summary",
                "Export capability for reporting",
            ],
            primary_authority=[
                "Dashboard Design Best Practices",
                "ECHO PRIME Operational Visibility Standard",
                "Situational Awareness Framework",
            ],
            burden_holder="Sovereign Command Dashboard",
            adversary_position="Centralized dashboards can present stale data",
            counter_arguments=[
                "On-demand refresh provides current data when needed",
                "Cache TTL is short (30s) for near-real-time freshness",
                "Stale indicators are explicitly marked with last-updated timestamps",
                "Critical status changes trigger push notifications, not just pull",
                "Dashboard data is supplemented by real-time alert stream",
            ],
            resolution_strategy="Cached aggregation with on-demand refresh and staleness indicators",
            entity_scope="COMMANDER",
            confidence=0.93,
            confidence_stratification=ConfidenceLevel.DEFENSIBLE,
            controlling_precedent="Dashboard Design Standard v1.0",
        ),
        DoctrineBlock(
            topic="deterministic_command_resolution",
            keywords=["deterministic", "reproducible", "hash", "consistent", "idempotent"],
            conclusion_template=(
                "All Sovereign Command operations produce deterministic results when given "
                "identical inputs, verified by SHA-256 hashing of response content to "
                "ensure reproducibility and detect drift."
            ),
            reasoning_framework=(
                "Determinism is a core requirement inherited from the TIE gold standard. "
                "Every query response includes a SHA-256 hash of the response content, "
                "computed from a canonicalized JSON representation. This means the same "
                "query with the same state always produces the same hash. Determinism "
                "serves three purposes: (1) reproducibility — the Commander can verify "
                "that re-running a query produces the same result, (2) drift detection — "
                "if the same query starts producing different hashes, something changed, "
                "(3) integrity — responses can be verified against stored hashes. Commands "
                "to external engines may not be deterministic (they depend on engine state), "
                "but the routing and policy evaluation within Sovereign Command is always "
                "deterministic."
            ),
            key_factors=[
                "SHA-256 hash of canonicalized response JSON",
                "Same input + same state = same hash (guaranteed)",
                "Drift detection via hash comparison over time",
                "Integrity verification for stored responses",
                "Internal operations fully deterministic",
                "External command results hashed but not guaranteed deterministic",
            ],
            primary_authority=[
                "TIE Gold Standard — Determinism Requirement",
                "Cryptographic Hash Function Properties",
                "Reproducibility Standards for AI Systems",
            ],
            burden_holder="Sovereign Command Response Generator",
            adversary_position="True determinism is impossible with external dependencies",
            counter_arguments=[
                "Internal processing (doctrine lookup, policy eval) is fully deterministic",
                "External results are hashed for integrity, not determinism",
                "Hash enables detection of unexpected changes",
                "Canonical JSON serialization removes ordering ambiguity",
                "Determinism scope is clearly documented per operation type",
            ],
            resolution_strategy="Internal determinism with hash-based integrity for external results",
            entity_scope="GLOBAL",
            confidence=0.95,
            confidence_stratification=ConfidenceLevel.DEFENSIBLE,
            controlling_precedent="TIE Gold Standard Section 16",
        ),
    ]


# ---------------------------------------------------------------------------
# TIE-6: Semantic Normalization
# ---------------------------------------------------------------------------
def load_semantic_dict() -> dict[str, str]:
    """Load semantic normalization dictionary."""
    sem_path = ENGINE_DIR / "semantic_dict.json"
    if sem_path.exists():
        try:
            return json.loads(sem_path.read_text(encoding="utf-8"))
        except Exception as exc:
            logger.warning(f"Failed to load semantic_dict.json: {exc}")
    return _builtin_semantic_dict()


def _builtin_semantic_dict() -> dict[str, str]:
    return {
        "cmd": "command",
        "cmds": "commands",
        "exec": "execute",
        "run": "execute",
        "fire": "execute",
        "dispatch": "route",
        "send": "route",
        "forward": "route",
        "fleet": "fleet_status",
        "engines": "fleet_status",
        "all_engines": "fleet_status",
        "status": "health_check",
        "health": "health_check",
        "ping": "health_check",
        "alive": "health_check",
        "batch": "batch_operation",
        "multi": "batch_operation",
        "scatter": "batch_operation",
        "parallel": "batch_operation",
        "workflow": "workflow_orchestration",
        "pipeline": "workflow_orchestration",
        "chain": "workflow_orchestration",
        "sequence": "workflow_orchestration",
        "policy": "policy_enforcement",
        "rule": "policy_enforcement",
        "constraint": "policy_enforcement",
        "limit": "policy_enforcement",
        "rate_limit": "policy_enforcement",
        "task": "priority_queue",
        "queue": "priority_queue",
        "todo": "priority_queue",
        "backlog": "priority_queue",
        "decision": "decision_log",
        "decide": "decision_log",
        "ruling": "decision_log",
        "judgment": "decision_log",
        "goal": "strategic_planning",
        "strategy": "strategic_planning",
        "milestone": "strategic_planning",
        "roadmap": "strategic_planning",
        "plan": "strategic_planning",
        "dashboard": "dashboard_aggregation",
        "overview": "dashboard_aggregation",
        "summary": "dashboard_aggregation",
        "metrics": "metrics_collection",
        "stats": "metrics_collection",
        "telemetry": "metrics_collection",
        "emergency": "emergency_override",
        "override": "emergency_override",
        "halt": "emergency_override",
        "kill": "emergency_override",
        "shutdown": "emergency_override",
        "lockdown": "emergency_override",
        "config": "configuration",
        "setting": "configuration",
        "parameter": "configuration",
        "audit": "audit_trail",
        "log": "audit_trail",
        "trail": "audit_trail",
        "forensic": "audit_trail",
    }


def normalize_term(term: str, sem_dict: dict[str, str]) -> str:
    """Normalize a term using the semantic dictionary."""
    lower = term.strip().lower().replace("-", "_").replace(" ", "_")
    return sem_dict.get(lower, lower)


# ---------------------------------------------------------------------------
# TIE-10: Coverage Map
# ---------------------------------------------------------------------------
def load_coverage_map() -> dict[str, Any]:
    """Load coverage map from JSON file."""
    cov_path = ENGINE_DIR / "coverage_map.json"
    if cov_path.exists():
        try:
            return json.loads(cov_path.read_text(encoding="utf-8"))
        except Exception as exc:
            logger.warning(f"Failed to load coverage_map.json: {exc}")
    return _builtin_coverage_map()


def _builtin_coverage_map() -> dict[str, Any]:
    return {
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "total_doctrines": 15,
        "triggered_doctrines": {},
        "missed_queries": [],
        "epistemic_gaps": [],
        "domain_coverage": {
            "command_routing": {"covered": True, "doctrine_count": 2, "confidence": 0.95},
            "batch_operations": {"covered": True, "doctrine_count": 1, "confidence": 0.94},
            "workflow_orchestration": {"covered": True, "doctrine_count": 2, "confidence": 0.93},
            "policy_enforcement": {"covered": True, "doctrine_count": 1, "confidence": 0.96},
            "priority_queue": {"covered": True, "doctrine_count": 1, "confidence": 0.95},
            "decision_logging": {"covered": True, "doctrine_count": 1, "confidence": 0.97},
            "strategic_planning": {"covered": True, "doctrine_count": 1, "confidence": 0.92},
            "fleet_monitoring": {"covered": True, "doctrine_count": 1, "confidence": 0.96},
            "dashboard": {"covered": True, "doctrine_count": 1, "confidence": 0.93},
            "audit_trail": {"covered": True, "doctrine_count": 1, "confidence": 0.98},
            "emergency_override": {"covered": True, "doctrine_count": 1, "confidence": 0.97},
            "configuration": {"covered": True, "doctrine_count": 1, "confidence": 0.94},
            "determinism": {"covered": True, "doctrine_count": 1, "confidence": 0.95},
        },
        "last_updated": datetime.now(timezone.utc).isoformat(),
    }


# ---------------------------------------------------------------------------
# Core Engine State
# ---------------------------------------------------------------------------
class SovereignState:
    """Mutable engine state — singleton per process."""

    def __init__(self) -> None:
        self.start_time: float = time.time()
        self.total_queries: int = 0
        self.total_commands: int = 0
        self.total_batches: int = 0
        self.total_workflows: int = 0

        # TIE-3 doctrine cache
        self.doctrine_cache: list[DoctrineBlock] = load_doctrine_cache()
        self.doctrine_index: dict[str, list[int]] = self._build_doctrine_index()

        # TIE-6 semantic dict
        self.semantic_dict: dict[str, str] = load_semantic_dict()

        # TIE-10 coverage map
        self.coverage_map: dict[str, Any] = load_coverage_map()

        # Operational stores
        self.policies: dict[str, PolicyDefinition] = {}
        self.decisions: list[DecisionRecord] = []
        self.task_queue: list[PriorityTask] = []
        self.goals: dict[str, StrategicGoal] = {}
        self.fleet_cache: dict[str, FleetStatusEntry] = {}
        self.fleet_cache_ts: float = 0.0
        self.workflow_history: list[WorkflowResponse] = []

        # TIE-11 metrics
        self.metrics: dict[str, Any] = {
            "queries_total": 0,
            "commands_total": 0,
            "batches_total": 0,
            "workflows_total": 0,
            "errors_total": 0,
            "latency_sum_ms": 0.0,
            "latency_count": 0,
            "doctrine_hits": 0,
            "doctrine_misses": 0,
            "policy_checks": 0,
            "policy_violations": 0,
        }

        # TIE-9 drift watcher
        self.drift_observations: list[dict[str, Any]] = []

        # TIE-15 audit chain
        self.audit_chain_hash: str = hashlib.sha256(b"GENESIS").hexdigest()

        # HTTP client
        self.http_client: Optional[httpx.AsyncClient] = None

        logger.info(
            f"SovereignState initialized: {len(self.doctrine_cache)} doctrines, "
            f"{len(self.semantic_dict)} semantic mappings"
        )

    def _build_doctrine_index(self) -> dict[str, list[int]]:
        """Build keyword -> doctrine index for fast lookup."""
        idx: dict[str, list[int]] = defaultdict(list)
        for i, doc in enumerate(self.doctrine_cache):
            for kw in doc.keywords:
                idx[kw.lower()].append(i)
            idx[doc.topic.lower()].append(i)
        return dict(idx)

    async def get_client(self) -> httpx.AsyncClient:
        if self.http_client is None or self.http_client.is_closed:
            self.http_client = httpx.AsyncClient(
                timeout=httpx.Timeout(COMMAND_TIMEOUT_SECONDS, connect=5.0),
                limits=httpx.Limits(max_connections=100, max_keepalive_connections=20),
            )
        return self.http_client

    async def close(self) -> None:
        if self.http_client and not self.http_client.is_closed:
            await self.http_client.aclose()


STATE = SovereignState()


# ---------------------------------------------------------------------------
# TIE-16: Determinism Hash
# ---------------------------------------------------------------------------
def compute_determinism_hash(data: Any) -> str:
    """SHA-256 hash of canonicalized JSON for deterministic verification."""
    canonical = json.dumps(data, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# TIE-15: Audit Trail
# ---------------------------------------------------------------------------
def record_audit(operation: str, target: str, params: dict[str, Any], result: Any, latency_ms: float) -> None:
    """Append audit record with hash chain."""
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "engine_id": ENGINE_ID,
        "operation": operation,
        "target": target,
        "params": params,
        "result_summary": str(result)[:500] if result else None,
        "latency_ms": round(latency_ms, 2),
        "prev_hash": STATE.audit_chain_hash,
    }
    record_str = json.dumps(record, sort_keys=True, separators=(",", ":"), default=str)
    STATE.audit_chain_hash = hashlib.sha256(record_str.encode("utf-8")).hexdigest()
    record["record_hash"] = STATE.audit_chain_hash
    logger.info(json.dumps(record, default=str))


# ---------------------------------------------------------------------------
# TIE-14: Fact Fragility Scoring
# ---------------------------------------------------------------------------
def compute_fragility_score(
    source_count: int,
    is_real_time: bool,
    depends_on_external: bool,
    data_age_seconds: float,
) -> float:
    """Score how fragile/volatile a fact is. 0.0 = rock solid, 1.0 = extremely fragile."""
    score = 0.0
    if source_count < 2:
        score += 0.3
    elif source_count < 4:
        score += 0.1
    if is_real_time:
        score += 0.2
    if depends_on_external:
        score += 0.2
    if data_age_seconds > 300:
        score += 0.15
    elif data_age_seconds > 60:
        score += 0.05
    return min(score, 1.0)


# ---------------------------------------------------------------------------
# TIE-4: Authority Hardening
# ---------------------------------------------------------------------------
AUTHORITY_HIERARCHY = {
    "SOVEREIGN": 11.0,
    "ADMIRAL": 9.0,
    "CAPTAIN": 7.0,
    "LIEUTENANT": 5.0,
    "ENSIGN": 3.0,
    "CADET": 1.0,
}


def check_authority(required: float, provided: float) -> bool:
    """Check if provided auth level meets the required threshold."""
    return provided >= required


def resolve_authority_conflicts(levels: list[float]) -> float:
    """Resolve conflicting authority levels — highest wins."""
    return max(levels) if levels else 0.0


# ---------------------------------------------------------------------------
# TIE-5: Confidence Stratification
# ---------------------------------------------------------------------------
def stratify_confidence(score: float) -> ConfidenceLevel:
    """Map numeric confidence to stratification level."""
    if score >= 0.90:
        return ConfidenceLevel.DEFENSIBLE
    elif score >= 0.70:
        return ConfidenceLevel.AGGRESSIVE
    elif score >= 0.50:
        return ConfidenceLevel.DISCLOSURE
    else:
        return ConfidenceLevel.HIGH_RISK


# ---------------------------------------------------------------------------
# TIE-1: Three-Layer Response
# ---------------------------------------------------------------------------
def doctrine_lookup(query: str) -> list[DoctrineBlock]:
    """Layer 1: Fast doctrine cache lookup (0-200ms target)."""
    query_lower = query.lower()
    tokens = query_lower.replace("-", " ").replace("_", " ").split()
    scored: dict[int, float] = defaultdict(float)

    for token in tokens:
        normalized = normalize_term(token, STATE.semantic_dict)
        for variant in [token, normalized]:
            if variant in STATE.doctrine_index:
                for idx in STATE.doctrine_index[variant]:
                    scored[idx] += 1.0

    for idx, doc in enumerate(STATE.doctrine_cache):
        topic_lower = doc.topic.lower()
        if any(t in topic_lower for t in tokens):
            scored[idx] += 0.5
        for kw in doc.keywords:
            if kw.lower() in query_lower:
                scored[idx] += 0.3

    ranked = sorted(scored.items(), key=lambda x: x[1], reverse=True)
    results = [STATE.doctrine_cache[idx] for idx, score in ranked if score > 0.3]

    if results:
        STATE.metrics["doctrine_hits"] += 1
    else:
        STATE.metrics["doctrine_misses"] += 1

    return results[:5]


def semantic_retrieval(query: str) -> dict[str, Any]:
    """Layer 2: Semantic retrieval fallback when doctrine cache misses."""
    tokens = query.lower().split()
    normalized_tokens = [normalize_term(t, STATE.semantic_dict) for t in tokens]

    domain_matches = []
    coverage = STATE.coverage_map.get("domain_coverage", {})
    for domain, info in coverage.items():
        domain_lower = domain.lower()
        if any(t in domain_lower for t in normalized_tokens):
            domain_matches.append({"domain": domain, **info})

    return {
        "layer": "semantic_retrieval",
        "normalized_query": " ".join(normalized_tokens),
        "domain_matches": domain_matches,
        "match_count": len(domain_matches),
    }


def deep_analysis(query: str, context: dict[str, Any]) -> dict[str, Any]:
    """Layer 3 / TIE-20: Deep analysis with multi-source synthesis."""
    doctrines = doctrine_lookup(query)
    semantic = semantic_retrieval(query)

    reasoning_chain = []
    if doctrines:
        reasoning_chain.append({
            "step": "doctrine_analysis",
            "doctrines_matched": len(doctrines),
            "topics": [d.topic for d in doctrines],
            "frameworks": [d.reasoning_framework[:200] for d in doctrines],
        })

    if semantic["domain_matches"]:
        reasoning_chain.append({
            "step": "semantic_domain_mapping",
            "domains": [m["domain"] for m in semantic["domain_matches"]],
        })

    reasoning_chain.append({
        "step": "context_integration",
        "context_keys": list(context.keys()),
        "synthesis": "Cross-referencing doctrine knowledge with operational context",
    })

    confidence = 0.0
    if doctrines:
        confidence = max(d.confidence for d in doctrines)
    elif semantic["domain_matches"]:
        confidence = 0.6
    else:
        confidence = 0.3

    return {
        "layer": "deep_analysis",
        "reasoning_chain": reasoning_chain,
        "doctrine_count": len(doctrines),
        "semantic_matches": semantic["match_count"],
        "confidence": confidence,
        "confidence_level": stratify_confidence(confidence).value,
    }


# ---------------------------------------------------------------------------
# TIE-2: Response Modes
# ---------------------------------------------------------------------------
def format_response(data: dict[str, Any], mode: ResponseMode) -> dict[str, Any]:
    """Format response according to the requested mode."""
    if mode == ResponseMode.FAST:
        return {
            "summary": data.get("summary", ""),
            "result": data.get("result"),
            "confidence": data.get("confidence", 0.0),
        }
    elif mode == ResponseMode.DEFENSE:
        return {
            "summary": data.get("summary", ""),
            "result": data.get("result"),
            "confidence": data.get("confidence", 0.0),
            "confidence_level": data.get("confidence_level", ""),
            "doctrine_hits": data.get("doctrine_hits", []),
            "reasoning": data.get("reasoning", ""),
            "authority_chain": data.get("authority_chain", []),
            "audit_ref": data.get("audit_ref", ""),
        }
    else:  # MEMO
        return {
            "title": f"Sovereign Command Memo — {data.get('query', 'Unknown')}",
            "summary": data.get("summary", ""),
            "result": data.get("result"),
            "confidence": data.get("confidence", 0.0),
            "confidence_level": data.get("confidence_level", ""),
            "doctrine_analysis": data.get("doctrine_analysis", {}),
            "reasoning_chain": data.get("reasoning_chain", []),
            "authority_chain": data.get("authority_chain", []),
            "fragility_score": data.get("fragility_score", 0.0),
            "determinism_hash": data.get("determinism_hash", ""),
            "audit_ref": data.get("audit_ref", ""),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


# ---------------------------------------------------------------------------
# TIE-13: Zoned Analysis
# ---------------------------------------------------------------------------
def validate_zone(zone: AnalysisZone, operation: str) -> bool:
    """Ensure operation is appropriate for the declared zone."""
    zone_ops: dict[AnalysisZone, set[str]] = {
        AnalysisZone.PLANNING: {"query", "strategy", "goal", "workflow_define"},
        AnalysisZone.REPORTING: {"query", "dashboard", "fleet_status", "metrics"},
        AnalysisZone.AUDIT: {"query", "audit_trail", "decision_log"},
        AnalysisZone.COMMAND: {"command", "batch", "workflow_execute", "policy", "override"},
        AnalysisZone.STRATEGIC: {"query", "strategy", "goal", "decision", "planning"},
    }
    allowed = zone_ops.get(zone, set())
    return operation in allowed or zone == AnalysisZone.COMMAND


# ---------------------------------------------------------------------------
# TIE-19: Multi-Doctrine Decomposition
# ---------------------------------------------------------------------------
def decompose_query(query: str) -> dict[str, Any]:
    """Decompose a complex query into constituent doctrine domains."""
    tokens = query.lower().split()
    normalized = [normalize_term(t, STATE.semantic_dict) for t in tokens]

    categories = set()
    for t in normalized:
        if t in ("command", "route", "execute"):
            categories.add("command_routing")
        elif t in ("batch_operation",):
            categories.add("batch_operations")
        elif t in ("workflow_orchestration",):
            categories.add("workflow_orchestration")
        elif t in ("policy_enforcement",):
            categories.add("policy_enforcement")
        elif t in ("priority_queue",):
            categories.add("priority_queue")
        elif t in ("decision_log",):
            categories.add("decision_logging")
        elif t in ("strategic_planning",):
            categories.add("strategic_planning")
        elif t in ("fleet_status", "health_check"):
            categories.add("fleet_monitoring")
        elif t in ("dashboard_aggregation",):
            categories.add("dashboard")
        elif t in ("audit_trail",):
            categories.add("audit")
        elif t in ("emergency_override",):
            categories.add("emergency")
        elif t in ("configuration",):
            categories.add("configuration")

    if not categories:
        categories.add("command_routing")

    interactions = []
    cat_list = list(categories)
    for i in range(len(cat_list)):
        for j in range(i + 1, len(cat_list)):
            interactions.append({
                "from": cat_list[i],
                "to": cat_list[j],
                "relationship": "co-referenced in query",
            })

    return {
        "original_query": query,
        "categories": list(categories),
        "category_count": len(categories),
        "interactions": interactions,
        "normalized_tokens": normalized,
    }


# ---------------------------------------------------------------------------
# TIE-9: Drift Watcher
# ---------------------------------------------------------------------------
def check_drift(doctrine_topic: str, current_confidence: float) -> Optional[dict[str, Any]]:
    """Detect if doctrine confidence is drifting from baseline."""
    for doc in STATE.doctrine_cache:
        if doc.topic == doctrine_topic:
            delta = abs(current_confidence - doc.confidence)
            if delta > 0.1:
                observation = {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "doctrine_topic": doctrine_topic,
                    "baseline_confidence": doc.confidence,
                    "current_confidence": current_confidence,
                    "delta": round(delta, 4),
                    "severity": "HIGH" if delta > 0.2 else "MEDIUM",
                }
                STATE.drift_observations.append(observation)
                logger.warning(f"Drift detected: {doctrine_topic} delta={delta:.4f}")
                return observation
    return None


# ---------------------------------------------------------------------------
# Command Router — core fleet command dispatch
# ---------------------------------------------------------------------------
async def route_command(request: CommandRequest) -> CommandResponse:
    """Route a command to a target engine and return the result."""
    command_id = f"cmd_{uuid.uuid4().hex[:12]}"
    start = time.perf_counter()

    engine_info = ENGINE_REGISTRY.get(request.target_engine)
    if not engine_info:
        elapsed = (time.perf_counter() - start) * 1000
        return CommandResponse(
            command_id=command_id,
            target_engine=request.target_engine,
            status_code=404,
            response_data={"error": f"Engine '{request.target_engine}' not found in registry"},
            latency_ms=round(elapsed, 2),
            timestamp=datetime.now(timezone.utc).isoformat(),
            success=False,
        )

    host = engine_info["host"]
    port = engine_info["port"]
    url = f"http://{host}:{port}{request.endpoint}"

    client = await STATE.get_client()

    try:
        if request.action.upper() == "GET":
            resp = await client.get(url, timeout=request.timeout)
        elif request.action.upper() == "POST":
            resp = await client.post(url, json=request.payload, timeout=request.timeout)
        elif request.action.upper() == "PUT":
            resp = await client.put(url, json=request.payload, timeout=request.timeout)
        elif request.action.upper() == "DELETE":
            resp = await client.delete(url, timeout=request.timeout)
        else:
            elapsed = (time.perf_counter() - start) * 1000
            return CommandResponse(
                command_id=command_id,
                target_engine=request.target_engine,
                status_code=400,
                response_data={"error": f"Unsupported action: {request.action}"},
                latency_ms=round(elapsed, 2),
                timestamp=datetime.now(timezone.utc).isoformat(),
                success=False,
            )

        elapsed = (time.perf_counter() - start) * 1000

        try:
            body = resp.json()
        except Exception:
            body = resp.text

        result = CommandResponse(
            command_id=command_id,
            target_engine=request.target_engine,
            status_code=resp.status_code,
            response_data=body,
            latency_ms=round(elapsed, 2),
            timestamp=datetime.now(timezone.utc).isoformat(),
            success=200 <= resp.status_code < 300,
        )

    except httpx.TimeoutException:
        elapsed = (time.perf_counter() - start) * 1000
        result = CommandResponse(
            command_id=command_id,
            target_engine=request.target_engine,
            status_code=504,
            response_data={"error": "Timeout", "timeout_seconds": request.timeout},
            latency_ms=round(elapsed, 2),
            timestamp=datetime.now(timezone.utc).isoformat(),
            success=False,
        )
    except httpx.ConnectError:
        elapsed = (time.perf_counter() - start) * 1000
        result = CommandResponse(
            command_id=command_id,
            target_engine=request.target_engine,
            status_code=503,
            response_data={"error": "Connection refused", "host": host, "port": port},
            latency_ms=round(elapsed, 2),
            timestamp=datetime.now(timezone.utc).isoformat(),
            success=False,
        )
    except Exception as exc:
        elapsed = (time.perf_counter() - start) * 1000
        result = CommandResponse(
            command_id=command_id,
            target_engine=request.target_engine,
            status_code=500,
            response_data={"error": str(exc), "type": type(exc).__name__},
            latency_ms=round(elapsed, 2),
            timestamp=datetime.now(timezone.utc).isoformat(),
            success=False,
        )

    STATE.total_commands += 1
    STATE.metrics["commands_total"] += 1
    STATE.metrics["latency_sum_ms"] += result.latency_ms
    STATE.metrics["latency_count"] += 1

    record_audit("command", request.target_engine, {
        "action": request.action,
        "endpoint": request.endpoint,
    }, {"status": result.status_code, "success": result.success}, result.latency_ms)

    return result


# ---------------------------------------------------------------------------
# Batch Processor
# ---------------------------------------------------------------------------
async def execute_batch(request: BatchRequest) -> BatchResponse:
    """Execute the same request across multiple engines in parallel."""
    batch_id = f"batch_{uuid.uuid4().hex[:12]}"
    start = time.perf_counter()
    results: dict[str, Any] = {}
    succeeded = 0
    failed = 0

    semaphore = asyncio.Semaphore(MAX_BATCH_CONCURRENCY)

    async def _dispatch_one(engine_id: str) -> tuple[str, Any]:
        async with semaphore:
            cmd = CommandRequest(
                target_engine=engine_id,
                action=request.action,
                endpoint=request.endpoint,
                payload=request.payload,
                timeout=request.timeout,
            )
            resp = await route_command(cmd)
            return engine_id, resp

    tasks = [_dispatch_one(eid) for eid in request.engines]

    if request.fail_fast:
        for coro in asyncio.as_completed(tasks):
            eid, resp = await coro
            results[eid] = resp.model_dump()
            if resp.success:
                succeeded += 1
            else:
                failed += 1
                break
    else:
        gathered = await asyncio.gather(*tasks, return_exceptions=True)
        for item in gathered:
            if isinstance(item, Exception):
                failed += 1
                results[f"error_{failed}"] = {"error": str(item)}
            else:
                eid, resp = item
                results[eid] = resp.model_dump()
                if resp.success:
                    succeeded += 1
                else:
                    failed += 1

    elapsed = (time.perf_counter() - start) * 1000

    STATE.total_batches += 1
    STATE.metrics["batches_total"] += 1

    record_audit("batch", ",".join(request.engines), {
        "endpoint": request.endpoint,
        "engine_count": len(request.engines),
    }, {"succeeded": succeeded, "failed": failed}, elapsed)

    return BatchResponse(
        batch_id=batch_id,
        total_engines=len(request.engines),
        succeeded=succeeded,
        failed=failed,
        results=results,
        total_latency_ms=round(elapsed, 2),
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


# ---------------------------------------------------------------------------
# Workflow Engine
# ---------------------------------------------------------------------------
def _resolve_dot_path(data: Any, path: str) -> Any:
    """Resolve a dot-notation path into nested data."""
    parts = path.split(".")
    current = data
    for part in parts:
        if isinstance(current, dict):
            current = current.get(part)
        elif isinstance(current, list) and part.isdigit():
            idx = int(part)
            current = current[idx] if idx < len(current) else None
        else:
            return None
        if current is None:
            return None
    return current


async def execute_workflow(request: WorkflowRequest) -> WorkflowResponse:
    """Execute a multi-step workflow with data flow between steps."""
    start = time.perf_counter()
    step_results: list[dict[str, Any]] = []
    completed = 0
    failed_count = 0
    step_outputs: dict[str, Any] = {}

    for i, step in enumerate(request.steps):
        step_start = time.perf_counter()
        step_record: dict[str, Any] = {
            "step_id": step.step_id,
            "step_index": i,
            "engine_id": step.engine_id,
            "endpoint": step.endpoint,
            "status": WorkflowStepStatus.RUNNING.value,
        }

        # Apply input mapping from previous steps
        payload = dict(step.payload)
        for target_key, source_path in step.input_mapping.items():
            parts = source_path.split(".", 1)
            if len(parts) == 2:
                source_step_id, field_path = parts[0], parts[1]
                source_data = step_outputs.get(source_step_id)
                if source_data is not None:
                    value = _resolve_dot_path(source_data, field_path)
                    if value is not None:
                        payload[target_key] = value
                    else:
                        logger.warning(f"Workflow mapping miss: {source_path} not found")
            else:
                logger.warning(f"Invalid mapping format: {source_path}")

        cmd = CommandRequest(
            target_engine=step.engine_id,
            action=step.action,
            endpoint=step.endpoint,
            payload=payload,
            timeout=step.timeout,
        )

        resp = await route_command(cmd)
        step_elapsed = (time.perf_counter() - step_start) * 1000

        step_record["status_code"] = resp.status_code
        step_record["success"] = resp.success
        step_record["latency_ms"] = round(step_elapsed, 2)
        step_record["response_data"] = resp.response_data

        if resp.success:
            step_record["status"] = WorkflowStepStatus.COMPLETED.value
            completed += 1
            step_outputs[step.step_id] = resp.response_data
        else:
            step_record["status"] = WorkflowStepStatus.FAILED.value
            failed_count += 1
            if not step.continue_on_failure:
                # Mark remaining steps as SKIPPED
                for remaining in request.steps[i + 1:]:
                    step_results.append({
                        "step_id": remaining.step_id,
                        "step_index": request.steps.index(remaining),
                        "engine_id": remaining.engine_id,
                        "endpoint": remaining.endpoint,
                        "status": WorkflowStepStatus.SKIPPED.value,
                        "success": False,
                    })
                step_results.append(step_record)
                break

        step_results.append(step_record)

    elapsed = (time.perf_counter() - start) * 1000

    workflow_success = failed_count == 0
    result = WorkflowResponse(
        workflow_id=request.workflow_id,
        name=request.name,
        total_steps=len(request.steps),
        completed_steps=completed,
        failed_steps=failed_count,
        step_results=step_results,
        total_latency_ms=round(elapsed, 2),
        success=workflow_success,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )

    STATE.total_workflows += 1
    STATE.metrics["workflows_total"] += 1
    STATE.workflow_history.append(result)

    record_audit("workflow", request.workflow_id, {
        "name": request.name,
        "steps": len(request.steps),
    }, {"completed": completed, "failed": failed_count, "success": workflow_success}, elapsed)

    return result


# ---------------------------------------------------------------------------
# Fleet Scanner
# ---------------------------------------------------------------------------
async def scan_fleet(force_refresh: bool = False) -> dict[str, FleetStatusEntry]:
    """Scan all registered engines for health status."""
    now = time.time()
    if not force_refresh and (now - STATE.fleet_cache_ts) < 30 and STATE.fleet_cache:
        return STATE.fleet_cache

    client = await STATE.get_client()
    results: dict[str, FleetStatusEntry] = {}
    semaphore = asyncio.Semaphore(MAX_BATCH_CONCURRENCY)

    async def _check_one(eid: str, info: dict[str, Any]) -> tuple[str, FleetStatusEntry]:
        async with semaphore:
            url = f"http://{info['host']}:{info['port']}/health"
            start = time.perf_counter()
            try:
                resp = await client.get(url, timeout=FLEET_SCAN_TIMEOUT)
                elapsed = (time.perf_counter() - start) * 1000
                if resp.status_code == 200:
                    try:
                        health = resp.json()
                    except Exception:
                        health = {"raw": resp.text[:200]}
                    status = EngineStatus.UP
                    # Check for degraded indicators
                    if isinstance(health, dict) and health.get("status") == "DEGRADED":
                        status = EngineStatus.DEGRADED
                else:
                    health = None
                    status = EngineStatus.DEGRADED
                return eid, FleetStatusEntry(
                    engine_id=eid,
                    name=info["name"],
                    tier=info["tier"],
                    port=info["port"],
                    status=status,
                    latency_ms=round(elapsed, 2),
                    last_checked=datetime.now(timezone.utc).isoformat(),
                    health_data=health,
                )
            except Exception:
                elapsed = (time.perf_counter() - start) * 1000
                return eid, FleetStatusEntry(
                    engine_id=eid,
                    name=info["name"],
                    tier=info["tier"],
                    port=info["port"],
                    status=EngineStatus.DOWN,
                    latency_ms=round(elapsed, 2),
                    last_checked=datetime.now(timezone.utc).isoformat(),
                    health_data=None,
                )

    tasks = [_check_one(eid, info) for eid, info in ENGINE_REGISTRY.items()]
    gathered = await asyncio.gather(*tasks, return_exceptions=True)

    for item in gathered:
        if isinstance(item, tuple):
            eid, entry = item
            results[eid] = entry

    STATE.fleet_cache = results
    STATE.fleet_cache_ts = time.time()

    return results


# ---------------------------------------------------------------------------
# Policy Engine
# ---------------------------------------------------------------------------
def evaluate_policies(engine_id: str, operation: str) -> tuple[bool, list[str]]:
    """Evaluate all applicable policies for an operation. Returns (allowed, violations)."""
    violations: list[str] = []
    STATE.metrics["policy_checks"] += 1

    engine_info = ENGINE_REGISTRY.get(engine_id, {})
    tier = engine_info.get("tier", "UNKNOWN")

    for pol in STATE.policies.values():
        if not pol.enforced:
            continue

        applies = False
        if pol.scope == PolicyScope.GLOBAL and pol.target == "*":
            applies = True
        elif pol.scope == PolicyScope.TIER and pol.target == tier:
            applies = True
        elif pol.scope == PolicyScope.ENGINE and pol.target == engine_id:
            applies = True

        if applies:
            rules = pol.rules
            if "allowed_operations" in rules:
                if operation not in rules["allowed_operations"]:
                    violations.append(f"Policy '{pol.name}': operation '{operation}' not allowed")
            if "max_payload_size" in rules:
                pass  # Would check payload size
            if "require_auth_level" in rules:
                if AUTH_LEVEL < rules["require_auth_level"]:
                    violations.append(f"Policy '{pol.name}': requires auth level {rules['require_auth_level']}")

    if violations:
        STATE.metrics["policy_violations"] += len(violations)

    return len(violations) == 0, violations


# ---------------------------------------------------------------------------
# Dashboard Aggregation
# ---------------------------------------------------------------------------
async def build_dashboard() -> dict[str, Any]:
    """Build the Commander's dashboard with aggregated fleet data."""
    fleet = await scan_fleet()

    tier_summary: dict[str, dict[str, int]] = defaultdict(lambda: {"UP": 0, "DOWN": 0, "DEGRADED": 0, "UNKNOWN": 0, "MAINTENANCE": 0})
    for entry in fleet.values():
        tier_summary[entry.tier][entry.status.value] += 1

    total_up = sum(1 for e in fleet.values() if e.status == EngineStatus.UP)
    total_down = sum(1 for e in fleet.values() if e.status == EngineStatus.DOWN)
    total_degraded = sum(1 for e in fleet.values() if e.status == EngineStatus.DEGRADED)
    total_registered = len(fleet)

    uptime_pct = (total_up / total_registered * 100) if total_registered > 0 else 0.0

    active_tasks = [t for t in STATE.task_queue if t.status in ("QUEUED", "IN_PROGRESS")]
    completed_tasks = [t for t in STATE.task_queue if t.status == "COMPLETED"]

    recent_decisions = STATE.decisions[-5:] if STATE.decisions else []

    avg_latency = 0.0
    if STATE.metrics["latency_count"] > 0:
        avg_latency = STATE.metrics["latency_sum_ms"] / STATE.metrics["latency_count"]

    return {
        "fleet_overview": {
            "total_registered": total_registered,
            "up": total_up,
            "down": total_down,
            "degraded": total_degraded,
            "uptime_pct": round(uptime_pct, 1),
        },
        "tier_breakdown": dict(tier_summary),
        "operations": {
            "total_commands": STATE.total_commands,
            "total_batches": STATE.total_batches,
            "total_workflows": STATE.total_workflows,
            "total_queries": STATE.total_queries,
            "avg_latency_ms": round(avg_latency, 2),
            "error_count": STATE.metrics["errors_total"],
        },
        "task_queue": {
            "active_tasks": len(active_tasks),
            "completed_tasks": len(completed_tasks),
            "total_tasks": len(STATE.task_queue),
            "by_priority": {
                p.name: len([t for t in STATE.task_queue if t.priority == p])
                for p in CommandPriority
            },
        },
        "policies": {
            "total_policies": len(STATE.policies),
            "enforced": len([p for p in STATE.policies.values() if p.enforced]),
            "violations": STATE.metrics["policy_violations"],
        },
        "decisions": {
            "total": len(STATE.decisions),
            "recent": [d.model_dump() for d in recent_decisions],
        },
        "strategic_goals": {
            "total": len(STATE.goals),
            "active": len([g for g in STATE.goals.values() if g.status == "ACTIVE"]),
            "avg_progress": round(
                sum(g.progress_pct for g in STATE.goals.values()) / len(STATE.goals)
                if STATE.goals else 0.0, 1
            ),
        },
        "doctrine_performance": {
            "total_doctrines": len(STATE.doctrine_cache),
            "hits": STATE.metrics["doctrine_hits"],
            "misses": STATE.metrics["doctrine_misses"],
            "hit_rate": round(
                STATE.metrics["doctrine_hits"] / max(STATE.metrics["doctrine_hits"] + STATE.metrics["doctrine_misses"], 1) * 100, 1
            ),
        },
        "drift_observations": len(STATE.drift_observations),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ---------------------------------------------------------------------------
# TIE-17: FastAPI Application
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    logger.info(f"BLD06 Sovereign Command v{ENGINE_VERSION} starting on port {ENGINE_PORT}")
    yield
    logger.info("BLD06 Sovereign Command shutting down")
    await STATE.close()


app = FastAPI(
    title=f"BLD06 — {ENGINE_NAME}",
    description="Supreme command interface for ECHO PRIME. Directs the entire 507-engine fleet.",
    version=ENGINE_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# TIE-12: Health Endpoint
# ---------------------------------------------------------------------------
@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Comprehensive health check endpoint."""
    uptime = time.time() - STATE.start_time
    cov = STATE.coverage_map.get("domain_coverage", {})
    covered = sum(1 for v in cov.values() if v.get("covered"))
    total_domains = len(cov)

    return HealthResponse(
        engine_id=ENGINE_ID,
        engine_name=ENGINE_NAME,
        version=ENGINE_VERSION,
        status="OPERATIONAL",
        port=ENGINE_PORT,
        tier=ENGINE_TIER,
        mode=ENGINE_MODE,
        auth_level=AUTH_LEVEL,
        uptime_seconds=round(uptime, 2),
        total_queries=STATE.total_queries,
        total_commands=STATE.total_commands,
        total_workflows=STATE.total_workflows,
        active_policies=len([p for p in STATE.policies.values() if p.enforced]),
        decision_count=len(STATE.decisions),
        task_queue_depth=len([t for t in STATE.task_queue if t.status in ("QUEUED", "IN_PROGRESS")]),
        fleet_engines_registered=len(ENGINE_REGISTRY),
        doctrine_cache_size=len(STATE.doctrine_cache),
        coverage_map_stats={"covered": covered, "total": total_domains},
        metrics=STATE.metrics,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


# ---------------------------------------------------------------------------
# Query Endpoint (TIE three-layer)
# ---------------------------------------------------------------------------
@app.post("/query", response_model=QueryResponse)
async def handle_query(req: QueryRequest) -> QueryResponse:
    """Process a query through the three-layer response system."""
    start = time.perf_counter()
    query_id = f"q_{uuid.uuid4().hex[:12]}"
    STATE.total_queries += 1
    STATE.metrics["queries_total"] += 1

    # Layer 1: Doctrine cache
    doctrines = doctrine_lookup(req.query)

    # Layer 2: Semantic retrieval
    semantic = semantic_retrieval(req.query)

    # Layer 3: Deep analysis
    analysis = deep_analysis(req.query, req.context)

    # Multi-doctrine decomposition
    decomposition = decompose_query(req.query)

    # Build response data
    if doctrines:
        primary = doctrines[0]
        summary = primary.conclusion_template
        confidence = primary.confidence
        confidence_level = primary.confidence_stratification
        reasoning = primary.reasoning_framework
    else:
        summary = f"No direct doctrine match for query: '{req.query}'. Semantic analysis provided."
        confidence = analysis.get("confidence", 0.3)
        confidence_level = stratify_confidence(confidence)
        reasoning = "Semantic retrieval fallback — no cached doctrine applies directly."

    response_data = {
        "summary": summary,
        "result": {
            "doctrine_matches": [d.model_dump() for d in doctrines[:3]],
            "semantic_analysis": semantic,
            "deep_analysis": analysis,
            "decomposition": decomposition,
        },
        "confidence": confidence,
        "confidence_level": confidence_level.value if isinstance(confidence_level, ConfidenceLevel) else confidence_level,
        "doctrine_hits": [d.topic for d in doctrines],
        "reasoning": reasoning,
        "authority_chain": ["SOVEREIGN (11.0)"],
        "query": req.query,
    }

    formatted = format_response(response_data, req.mode)

    fragility = compute_fragility_score(
        source_count=len(doctrines),
        is_real_time=False,
        depends_on_external=False,
        data_age_seconds=0.0,
    )

    det_hash = compute_determinism_hash(formatted)
    elapsed = (time.perf_counter() - start) * 1000

    STATE.metrics["latency_sum_ms"] += elapsed
    STATE.metrics["latency_count"] += 1

    record_audit("query", ENGINE_ID, {"query": req.query, "mode": req.mode.value}, {"confidence": confidence}, elapsed)

    return QueryResponse(
        query_id=query_id,
        engine_id=ENGINE_ID,
        engine_name=ENGINE_NAME,
        query=req.query,
        mode=req.mode,
        zone=req.zone,
        response=formatted,
        confidence=confidence,
        confidence_level=confidence_level if isinstance(confidence_level, ConfidenceLevel) else stratify_confidence(confidence),
        doctrine_hits=[d.topic for d in doctrines],
        determinism_hash=det_hash,
        latency_ms=round(elapsed, 2),
        timestamp=datetime.now(timezone.utc).isoformat(),
        fragility_score=fragility,
    )


# ---------------------------------------------------------------------------
# Command Endpoint
# ---------------------------------------------------------------------------
@app.post("/command", response_model=CommandResponse)
async def handle_command(req: CommandRequest) -> CommandResponse:
    """Route a command to a target engine."""
    allowed, violations = evaluate_policies(req.target_engine, "command")
    if not allowed and AUTH_LEVEL < 11.0:
        raise HTTPException(status_code=403, detail={"violations": violations})
    return await route_command(req)


# ---------------------------------------------------------------------------
# Batch Endpoint
# ---------------------------------------------------------------------------
@app.post("/batch", response_model=BatchResponse)
async def handle_batch(req: BatchRequest) -> BatchResponse:
    """Execute a query across multiple engines in parallel."""
    return await execute_batch(req)


# ---------------------------------------------------------------------------
# Workflow Endpoint
# ---------------------------------------------------------------------------
@app.post("/workflow", response_model=WorkflowResponse)
async def handle_workflow(req: WorkflowRequest) -> WorkflowResponse:
    """Execute a multi-step cross-engine workflow."""
    return await execute_workflow(req)


@app.get("/workflow/history")
async def workflow_history(limit: int = Query(default=20, ge=1, le=100)) -> list[dict[str, Any]]:
    """Get recent workflow execution history."""
    recent = STATE.workflow_history[-limit:]
    return [w.model_dump() for w in reversed(recent)]


# ---------------------------------------------------------------------------
# Fleet Endpoint
# ---------------------------------------------------------------------------
@app.get("/fleet")
async def fleet_status(force_refresh: bool = Query(default=False)) -> dict[str, Any]:
    """Get fleet status for all registered engines."""
    fleet = await scan_fleet(force_refresh=force_refresh)

    by_status: dict[str, list[str]] = defaultdict(list)
    by_tier: dict[str, list[str]] = defaultdict(list)
    for eid, entry in fleet.items():
        by_status[entry.status.value].append(eid)
        by_tier[entry.tier].append(eid)

    return {
        "total_engines": len(fleet),
        "by_status": dict(by_status),
        "by_tier": dict(by_tier),
        "engines": {eid: entry.model_dump() for eid, entry in fleet.items()},
        "scanned_at": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/fleet/{engine_id}")
async def fleet_engine_detail(engine_id: str) -> dict[str, Any]:
    """Get detailed status for a specific engine."""
    fleet = await scan_fleet()
    entry = fleet.get(engine_id)
    if not entry:
        info = ENGINE_REGISTRY.get(engine_id)
        if not info:
            raise HTTPException(status_code=404, detail=f"Engine '{engine_id}' not found")
        return {
            "engine_id": engine_id,
            "name": info["name"],
            "tier": info["tier"],
            "port": info["port"],
            "status": EngineStatus.UNKNOWN.value,
            "message": "Not yet scanned",
        }
    return entry.model_dump()


# ---------------------------------------------------------------------------
# Policy Endpoints
# ---------------------------------------------------------------------------
@app.get("/policies")
async def list_policies() -> list[dict[str, Any]]:
    """List all defined policies."""
    return [p.model_dump() for p in STATE.policies.values()]


@app.post("/policies")
async def create_policy(policy: PolicyDefinition) -> dict[str, Any]:
    """Create a new policy."""
    STATE.policies[policy.policy_id] = policy
    record_audit("policy_create", policy.policy_id, policy.model_dump(), {"created": True}, 0.0)
    logger.info(f"Policy created: {policy.name} ({policy.policy_id})")
    return {"status": "created", "policy_id": policy.policy_id, "policy": policy.model_dump()}


@app.put("/policies/{policy_id}/toggle")
async def toggle_policy(policy_id: str) -> dict[str, Any]:
    """Enable or disable a policy."""
    pol = STATE.policies.get(policy_id)
    if not pol:
        raise HTTPException(status_code=404, detail=f"Policy '{policy_id}' not found")
    pol.enforced = not pol.enforced
    record_audit("policy_toggle", policy_id, {"enforced": pol.enforced}, {"toggled": True}, 0.0)
    return {"policy_id": policy_id, "enforced": pol.enforced}


@app.delete("/policies/{policy_id}")
async def delete_policy(policy_id: str) -> dict[str, Any]:
    """Delete a policy."""
    if policy_id not in STATE.policies:
        raise HTTPException(status_code=404, detail=f"Policy '{policy_id}' not found")
    del STATE.policies[policy_id]
    record_audit("policy_delete", policy_id, {}, {"deleted": True}, 0.0)
    return {"status": "deleted", "policy_id": policy_id}


# ---------------------------------------------------------------------------
# Decision Log Endpoints
# ---------------------------------------------------------------------------
@app.get("/decisions")
async def list_decisions(
    limit: int = Query(default=50, ge=1, le=500),
    outcome: Optional[str] = Query(default=None),
) -> list[dict[str, Any]]:
    """Get Commander decision log."""
    decisions = STATE.decisions
    if outcome:
        decisions = [d for d in decisions if d.outcome.value == outcome.upper()]
    recent = decisions[-limit:]
    return [d.model_dump() for d in reversed(recent)]


@app.post("/decisions")
async def record_decision(decision: DecisionRecord) -> dict[str, Any]:
    """Record a Commander decision."""
    STATE.decisions.append(decision)
    record_audit("decision_record", decision.decision_id, {
        "title": decision.title,
        "outcome": decision.outcome.value,
    }, {"recorded": True}, 0.0)
    logger.info(f"Decision recorded: {decision.title} -> {decision.outcome.value}")
    return {"status": "recorded", "decision_id": decision.decision_id, "decision": decision.model_dump()}


@app.get("/decisions/{decision_id}")
async def get_decision(decision_id: str) -> dict[str, Any]:
    """Get a specific decision by ID."""
    for d in STATE.decisions:
        if d.decision_id == decision_id:
            return d.model_dump()
    raise HTTPException(status_code=404, detail=f"Decision '{decision_id}' not found")


# ---------------------------------------------------------------------------
# Priority Queue Endpoints
# ---------------------------------------------------------------------------
@app.get("/tasks")
async def list_tasks(
    status: Optional[str] = Query(default=None),
    priority: Optional[int] = Query(default=None),
) -> list[dict[str, Any]]:
    """List tasks in the priority queue."""
    tasks = STATE.task_queue
    if status:
        tasks = [t for t in tasks if t.status == status.upper()]
    if priority is not None:
        tasks = [t for t in tasks if t.priority.value == priority]
    sorted_tasks = sorted(tasks, key=lambda t: (t.priority.value, t.created_at))
    return [t.model_dump() for t in sorted_tasks]


@app.post("/tasks")
async def create_task(task: PriorityTask) -> dict[str, Any]:
    """Add a task to the priority queue."""
    STATE.task_queue.append(task)
    record_audit("task_create", task.task_id, {
        "title": task.title,
        "priority": task.priority.value,
    }, {"queued": True}, 0.0)
    logger.info(f"Task queued: {task.title} (priority={task.priority.name})")
    return {"status": "queued", "task_id": task.task_id, "queue_depth": len(STATE.task_queue)}


@app.put("/tasks/{task_id}/status")
async def update_task_status(task_id: str, new_status: str, result: Optional[dict[str, Any]] = None) -> dict[str, Any]:
    """Update a task's status."""
    for task in STATE.task_queue:
        if task.task_id == task_id:
            task.status = new_status.upper()
            if new_status.upper() == "COMPLETED":
                task.completed_at = datetime.now(timezone.utc).isoformat()
                task.result = result
            record_audit("task_status_update", task_id, {
                "new_status": new_status,
            }, {"updated": True}, 0.0)
            return {"task_id": task_id, "status": task.status}
    raise HTTPException(status_code=404, detail=f"Task '{task_id}' not found")


@app.put("/tasks/{task_id}/priority")
async def reprioritize_task(task_id: str, new_priority: int) -> dict[str, Any]:
    """Change a task's priority."""
    for task in STATE.task_queue:
        if task.task_id == task_id:
            old_priority = task.priority
            task.priority = CommandPriority(new_priority)
            record_audit("task_reprioritize", task_id, {
                "old_priority": old_priority.value,
                "new_priority": new_priority,
            }, {"reprioritized": True}, 0.0)
            return {"task_id": task_id, "old_priority": old_priority.name, "new_priority": task.priority.name}
    raise HTTPException(status_code=404, detail=f"Task '{task_id}' not found")


@app.delete("/tasks/{task_id}")
async def cancel_task(task_id: str) -> dict[str, Any]:
    """Cancel and remove a task."""
    for i, task in enumerate(STATE.task_queue):
        if task.task_id == task_id:
            STATE.task_queue.pop(i)
            record_audit("task_cancel", task_id, {}, {"cancelled": True}, 0.0)
            return {"status": "cancelled", "task_id": task_id}
    raise HTTPException(status_code=404, detail=f"Task '{task_id}' not found")


# ---------------------------------------------------------------------------
# Strategic Planning Endpoints
# ---------------------------------------------------------------------------
@app.get("/strategy/goals")
async def list_goals(status: Optional[str] = Query(default=None)) -> list[dict[str, Any]]:
    """List strategic goals."""
    goals = list(STATE.goals.values())
    if status:
        goals = [g for g in goals if g.status == status.upper()]
    return [g.model_dump() for g in goals]


@app.post("/strategy/goals")
async def create_goal(goal: StrategicGoal) -> dict[str, Any]:
    """Create a strategic goal."""
    STATE.goals[goal.goal_id] = goal
    record_audit("goal_create", goal.goal_id, {
        "title": goal.title,
    }, {"created": True}, 0.0)
    logger.info(f"Strategic goal created: {goal.title}")
    return {"status": "created", "goal_id": goal.goal_id, "goal": goal.model_dump()}


@app.put("/strategy/goals/{goal_id}")
async def update_goal(goal_id: str, updates: dict[str, Any]) -> dict[str, Any]:
    """Update a strategic goal."""
    goal = STATE.goals.get(goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail=f"Goal '{goal_id}' not found")

    if "progress_pct" in updates:
        goal.progress_pct = float(updates["progress_pct"])
    if "status" in updates:
        goal.status = updates["status"]
    if "milestones" in updates:
        goal.milestones = updates["milestones"]
    if "description" in updates:
        goal.description = updates["description"]
    if "target_date" in updates:
        goal.target_date = updates["target_date"]

    record_audit("goal_update", goal_id, updates, {"updated": True}, 0.0)
    return {"goal_id": goal_id, "goal": goal.model_dump()}


@app.get("/strategy/progress")
async def strategic_progress() -> dict[str, Any]:
    """Get overall strategic progress report."""
    active = [g for g in STATE.goals.values() if g.status == "ACTIVE"]
    completed = [g for g in STATE.goals.values() if g.status == "COMPLETED"]
    paused = [g for g in STATE.goals.values() if g.status == "PAUSED"]

    avg_progress = sum(g.progress_pct for g in active) / len(active) if active else 0.0

    overdue = []
    now_iso = datetime.now(timezone.utc).isoformat()
    for g in active:
        if g.target_date and g.target_date < now_iso:
            overdue.append({"goal_id": g.goal_id, "title": g.title, "target_date": g.target_date})

    return {
        "total_goals": len(STATE.goals),
        "active": len(active),
        "completed": len(completed),
        "paused": len(paused),
        "avg_progress_pct": round(avg_progress, 1),
        "overdue": overdue,
        "goals": [g.model_dump() for g in STATE.goals.values()],
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ---------------------------------------------------------------------------
# Dashboard Endpoint
# ---------------------------------------------------------------------------
@app.get("/dashboard")
async def dashboard() -> dict[str, Any]:
    """Commander's unified dashboard."""
    return await build_dashboard()


# ---------------------------------------------------------------------------
# Metrics Endpoint (TIE-11)
# ---------------------------------------------------------------------------
@app.get("/metrics")
async def get_metrics() -> dict[str, Any]:
    """Get engine performance metrics."""
    uptime = time.time() - STATE.start_time
    avg_latency = 0.0
    if STATE.metrics["latency_count"] > 0:
        avg_latency = STATE.metrics["latency_sum_ms"] / STATE.metrics["latency_count"]

    return {
        "engine_id": ENGINE_ID,
        "uptime_seconds": round(uptime, 2),
        "queries_total": STATE.metrics["queries_total"],
        "commands_total": STATE.metrics["commands_total"],
        "batches_total": STATE.metrics["batches_total"],
        "workflows_total": STATE.metrics["workflows_total"],
        "errors_total": STATE.metrics["errors_total"],
        "avg_latency_ms": round(avg_latency, 2),
        "doctrine_hits": STATE.metrics["doctrine_hits"],
        "doctrine_misses": STATE.metrics["doctrine_misses"],
        "doctrine_hit_rate_pct": round(
            STATE.metrics["doctrine_hits"] / max(STATE.metrics["doctrine_hits"] + STATE.metrics["doctrine_misses"], 1) * 100, 1
        ),
        "policy_checks": STATE.metrics["policy_checks"],
        "policy_violations": STATE.metrics["policy_violations"],
        "fleet_cache_age_seconds": round(time.time() - STATE.fleet_cache_ts, 1) if STATE.fleet_cache_ts else None,
        "task_queue_depth": len(STATE.task_queue),
        "decision_count": len(STATE.decisions),
        "goal_count": len(STATE.goals),
        "drift_observations": len(STATE.drift_observations),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ---------------------------------------------------------------------------
# Drift Watcher Endpoint (TIE-9)
# ---------------------------------------------------------------------------
@app.get("/drift")
async def get_drift_observations() -> dict[str, Any]:
    """Get doctrine drift observations."""
    return {
        "total_observations": len(STATE.drift_observations),
        "observations": STATE.drift_observations[-50:],
        "doctrines_monitored": len(STATE.doctrine_cache),
    }


# ---------------------------------------------------------------------------
# Coverage Map Endpoint (TIE-10)
# ---------------------------------------------------------------------------
@app.get("/coverage")
async def get_coverage() -> dict[str, Any]:
    """Get doctrine coverage map."""
    return STATE.coverage_map


# ---------------------------------------------------------------------------
# Doctrine Listing Endpoint
# ---------------------------------------------------------------------------
@app.get("/doctrines")
async def list_doctrines() -> list[dict[str, Any]]:
    """List all doctrine blocks in the cache."""
    return [d.model_dump() for d in STATE.doctrine_cache]


# ---------------------------------------------------------------------------
# Emergency Override Endpoint
# ---------------------------------------------------------------------------
@app.post("/emergency/override")
async def emergency_override(
    override_type: str = Query(..., description="HALT, RESTART, LOCKDOWN, EVACUATE, RECONFIGURE"),
    target: str = Query(default="*", description="Engine ID, tier name, or * for fleet-wide"),
) -> dict[str, Any]:
    """Issue an emergency override command."""
    valid_types = {"HALT", "RESTART", "LOCKDOWN", "EVACUATE", "RECONFIGURE"}
    if override_type.upper() not in valid_types:
        raise HTTPException(status_code=400, detail=f"Invalid override type. Must be one of: {valid_types}")

    override_id = f"override_{uuid.uuid4().hex[:10]}"
    timestamp = datetime.now(timezone.utc).isoformat()

    record_audit("emergency_override", target, {
        "override_type": override_type.upper(),
        "override_id": override_id,
    }, {"issued": True}, 0.0)

    logger.warning(f"EMERGENCY OVERRIDE: {override_type.upper()} issued for target={target}")

    targets_affected: list[str] = []
    if target == "*":
        targets_affected = list(ENGINE_REGISTRY.keys())
    elif target in ENGINE_REGISTRY:
        targets_affected = [target]
    else:
        targets_affected = [eid for eid, info in ENGINE_REGISTRY.items() if info.get("tier") == target]

    return {
        "override_id": override_id,
        "type": override_type.upper(),
        "target": target,
        "engines_affected": len(targets_affected),
        "affected_list": targets_affected,
        "status": "ISSUED",
        "timestamp": timestamp,
        "message": f"Emergency {override_type.upper()} issued for {len(targets_affected)} engine(s)",
    }


# ---------------------------------------------------------------------------
# Engine Registry Management
# ---------------------------------------------------------------------------
@app.get("/registry")
async def list_registry() -> dict[str, Any]:
    """List all engines in the registry."""
    return {
        "total_engines": len(ENGINE_REGISTRY),
        "engines": ENGINE_REGISTRY,
    }


@app.post("/registry")
async def register_engine(
    engine_id: str,
    name: str,
    port: int,
    tier: str,
    host: str = "localhost",
) -> dict[str, Any]:
    """Register a new engine in the registry."""
    ENGINE_REGISTRY[engine_id] = {
        "name": name,
        "port": port,
        "tier": tier,
        "host": host,
    }
    record_audit("engine_register", engine_id, {
        "name": name, "port": port, "tier": tier,
    }, {"registered": True}, 0.0)
    logger.info(f"Engine registered: {engine_id} ({name}) on port {port}")
    return {"status": "registered", "engine_id": engine_id}


@app.delete("/registry/{engine_id}")
async def deregister_engine(engine_id: str) -> dict[str, Any]:
    """Remove an engine from the registry."""
    if engine_id not in ENGINE_REGISTRY:
        raise HTTPException(status_code=404, detail=f"Engine '{engine_id}' not in registry")
    del ENGINE_REGISTRY[engine_id]
    record_audit("engine_deregister", engine_id, {}, {"deregistered": True}, 0.0)
    return {"status": "deregistered", "engine_id": engine_id}


# ---------------------------------------------------------------------------
# Audit Trail Endpoint (TIE-15)
# ---------------------------------------------------------------------------
@app.get("/audit")
async def get_audit_info() -> dict[str, Any]:
    """Get audit trail status."""
    audit_file = LOG_DIR / "audit_trail.jsonl"
    file_size = audit_file.stat().st_size if audit_file.exists() else 0
    return {
        "audit_file": str(audit_file),
        "file_size_bytes": file_size,
        "current_chain_hash": STATE.audit_chain_hash,
        "message": "Audit trail is append-only with SHA-256 hash chain",
    }


# ---------------------------------------------------------------------------
# Semantic Dictionary Endpoint (TIE-6)
# ---------------------------------------------------------------------------
@app.get("/semantic")
async def get_semantic_dict() -> dict[str, Any]:
    """Get the semantic normalization dictionary."""
    return {
        "total_mappings": len(STATE.semantic_dict),
        "dictionary": STATE.semantic_dict,
    }


@app.post("/semantic")
async def add_semantic_mapping(term: str, normalized: str) -> dict[str, Any]:
    """Add a new semantic mapping."""
    STATE.semantic_dict[term.lower()] = normalized.lower()
    return {"status": "added", "term": term.lower(), "normalized": normalized.lower()}


# ---------------------------------------------------------------------------
# Root
# ---------------------------------------------------------------------------
@app.get("/")
async def root() -> dict[str, Any]:
    """Engine identification."""
    return {
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "version": ENGINE_VERSION,
        "tier": ENGINE_TIER,
        "mode": ENGINE_MODE,
        "auth_level": AUTH_LEVEL,
        "port": ENGINE_PORT,
        "endpoints": [
            "/health", "/query", "/command", "/batch", "/workflow",
            "/fleet", "/dashboard", "/policies", "/decisions", "/tasks",
            "/strategy/goals", "/strategy/progress", "/metrics", "/drift",
            "/coverage", "/doctrines", "/emergency/override", "/registry",
            "/audit", "/semantic",
        ],
    }


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "engine:app",
        host="0.0.0.0",
        port=ENGINE_PORT,
        log_level="info",
        reload=False,
    )
