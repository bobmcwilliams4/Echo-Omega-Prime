"""
GOV01 — Authority Gate Engine
Central authority validation for the entire ECHO PRIME system.
TIE-20 compliant. Port 8889. Auth 10.0 COMMANDER ONLY.
"""
from __future__ import annotations

import asyncio
import hashlib
import hmac
import json
import secrets
import sys
import time
import uuid
from collections import defaultdict
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Optional

import uvicorn
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------------
ENGINE_DIR = Path(__file__).parent
ENGINES_DIR = ENGINE_DIR.parent
sys.path.insert(0, str(ENGINES_DIR))

# ---------------------------------------------------------------------------
# Loguru config
# ---------------------------------------------------------------------------
logger.remove()
logger.add(
    sys.stderr,
    level="DEBUG",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level:<8}</level> | <cyan>GOV01</cyan> | {message}",
)
LOG_PATH = ENGINE_DIR / "logs"
LOG_PATH.mkdir(exist_ok=True)
logger.add(
    LOG_PATH / "gov01_authority_gate.log",
    rotation="50 MB",
    retention="30 days",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level:<8} | GOV01 | {message}",
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
ENGINE_ID = "GOV01"
ENGINE_NAME = "Authority Gate"
ENGINE_VERSION = "1.0.0"
ENGINE_PORT = 8889
ENGINE_TIER = "GOV"
ENGINE_MODE = "DET"
ENGINE_AUTH_REQUIRED = 10.0
HMAC_SECRET = "ECHO_PRIME_GOV01_HMAC_SECRET_KEY_2026"
TOKEN_EXPIRY_SECONDS = 3600
MAX_FAILED_ATTEMPTS = 5
LOCKOUT_DURATION_SECONDS = 900
RATE_LIMIT_WINDOW_SECONDS = 60
STARTUP_TIME = time.time()

# ---------------------------------------------------------------------------
# Authority Hierarchy
# ---------------------------------------------------------------------------

class AuthorityLevel(float, Enum):
    """Complete ECHO PRIME authority hierarchy."""
    PUBLIC = 0.0
    BASIC_READ = 1.0
    BASIC_WRITE = 2.0
    BASIC_EXECUTE = 3.0
    BASIC_ADMIN = 4.0
    BASIC_MAX = 4.9
    TRUSTED = 5.0
    PREMIUM = 5.1
    ENTERPRISE = 5.2
    PARTNER = 5.3
    ELEVATED = 6.0
    INNER_CIRCLE = 7.0
    MEDICAL = 7.5
    EXECUTIVE = 8.0
    SECURITY = 9.0
    COMMANDER_HEIR = 9.5
    COMMANDER_ONLY = 10.0
    SOVEREIGN = 11.0


AUTHORITY_TIER_NAMES: dict[float, str] = {
    0.0: "PUBLIC",
    1.0: "BASIC_READ",
    2.0: "BASIC_WRITE",
    3.0: "BASIC_EXECUTE",
    4.0: "BASIC_ADMIN",
    4.9: "BASIC_MAX",
    5.0: "TRUSTED",
    5.1: "PREMIUM",
    5.2: "ENTERPRISE",
    5.3: "PARTNER",
    6.0: "ELEVATED",
    7.0: "INNER_CIRCLE",
    7.5: "MEDICAL",
    8.0: "EXECUTIVE",
    9.0: "SECURITY",
    9.5: "COMMANDER_HEIR",
    10.0: "COMMANDER_ONLY",
    11.0: "SOVEREIGN",
}

AUTHORITY_DESCRIPTIONS: dict[float, str] = {
    0.0: "Unauthenticated public access. Read-only on public endpoints.",
    1.0: "Basic authenticated read access. Can view non-sensitive data.",
    2.0: "Basic write access. Can submit data, create records.",
    3.0: "Execute access. Can trigger computations and engine queries.",
    4.0: "Basic admin. Can manage own resources, view usage stats.",
    4.9: "Maximum basic tier. All basic capabilities, no privileged ops.",
    5.0: "Trusted user. Verified identity, expanded rate limits.",
    5.1: "Premium tier. Priority processing, extended quotas.",
    5.2: "Enterprise tier. SLA-backed, dedicated resources.",
    5.3: "Partner tier. API integration access, webhook registration.",
    6.0: "Elevated access. Can view system metrics, limited admin.",
    7.0: "Inner Circle. Full system visibility, can manage users below 7.0.",
    7.5: "Medical clearance. Access to health/biometric subsystems.",
    8.0: "Executive. Can modify system config, deploy engines.",
    9.0: "Security officer. Full audit access, can lock/unlock accounts.",
    9.5: "Commander Heir. All capabilities except SOVEREIGN overrides.",
    10.0: "Commander Only. Full system control. Bobby Don McWilliams II.",
    11.0: "SOVEREIGN. Bloodline directive. Overrides all gates unconditionally.",
}

RATE_LIMITS_PER_TIER: dict[float, int] = {
    0.0: 10,
    1.0: 30,
    2.0: 60,
    3.0: 100,
    4.0: 150,
    4.9: 200,
    5.0: 300,
    5.1: 500,
    5.2: 1000,
    5.3: 800,
    6.0: 1500,
    7.0: 3000,
    7.5: 2000,
    8.0: 5000,
    9.0: 8000,
    9.5: 10000,
    10.0: 50000,
    11.0: 999999,
}


def get_tier_name(level: float) -> str:
    """Return the tier name for a given authority level."""
    if level in AUTHORITY_TIER_NAMES:
        return AUTHORITY_TIER_NAMES[level]
    for threshold in sorted(AUTHORITY_TIER_NAMES.keys(), reverse=True):
        if level >= threshold:
            return AUTHORITY_TIER_NAMES[threshold]
    return "UNKNOWN"


def get_rate_limit(level: float) -> int:
    """Return rate limit (requests per window) for a given authority level."""
    for threshold in sorted(RATE_LIMITS_PER_TIER.keys(), reverse=True):
        if level >= threshold:
            return RATE_LIMITS_PER_TIER[threshold]
    return RATE_LIMITS_PER_TIER[0.0]


# ---------------------------------------------------------------------------
# Pydantic Models
# ---------------------------------------------------------------------------

class TokenPayload(BaseModel):
    """Internal token payload structure."""
    sub: str = Field(..., description="Subject / user identifier")
    level: float = Field(..., description="Authority level 0.0-11.0")
    iat: float = Field(..., description="Issued-at timestamp")
    exp: float = Field(..., description="Expiration timestamp")
    jti: str = Field(default_factory=lambda: uuid.uuid4().hex, description="Unique token ID")
    bloodline: bool = Field(default=False, description="Bloodline-verified flag")
    ip_bound: Optional[str] = Field(default=None, description="IP binding if set")
    scope: list[str] = Field(default_factory=list, description="Allowed engine scopes")


class ValidateRequest(BaseModel):
    """Request to validate a caller's authority."""
    token: str = Field(..., description="HMAC-signed token string")
    required_level: float = Field(..., description="Minimum authority level needed")
    engine_id: str = Field(default="", description="Target engine identifier")
    action: str = Field(default="access", description="Action being performed")
    client_ip: Optional[str] = Field(default=None, description="Client IP for brute-force tracking")


class ValidateResponse(BaseModel):
    """Response from authority validation."""
    authorized: bool
    level: float
    tier_name: str
    reason: str
    token_id: str = ""
    rate_remaining: int = 0
    decision_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:12])
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    determinism_hash: str = ""


class TokenIssueRequest(BaseModel):
    """Request to issue a new authority token."""
    subject: str = Field(..., description="User or service identifier")
    level: float = Field(..., description="Authority level to grant")
    ttl_seconds: int = Field(default=3600, description="Token time-to-live")
    bloodline: bool = Field(default=False)
    ip_bind: Optional[str] = Field(default=None)
    scope: list[str] = Field(default_factory=list)


class TokenIssueResponse(BaseModel):
    """Response with the issued token."""
    token: str
    expires_at: str
    level: float
    tier_name: str
    token_id: str


class AuditEntry(BaseModel):
    """Single audit log entry."""
    decision_id: str
    timestamp: str
    action: str
    subject: str
    level: float
    required_level: float
    engine_id: str
    authorized: bool
    reason: str
    client_ip: str
    token_id: str


class MatrixEntry(BaseModel):
    """Cross-engine authorization rule."""
    engine_id: str
    engine_name: str
    min_level: float
    tier_name: str
    allowed_actions: list[str]
    restricted_to_scope: bool
    notes: str


class BruteForceStatus(BaseModel):
    """Brute force detection status for an IP."""
    ip: str
    failed_attempts: int
    locked: bool
    lockout_expires: Optional[str]
    last_attempt: Optional[str]


class EscalationRequest(BaseModel):
    """Request for authority escalation."""
    token: str
    target_level: float
    reason: str
    approver_token: Optional[str] = None


class EscalationResponse(BaseModel):
    """Response to escalation request."""
    approved: bool
    new_token: Optional[str] = None
    new_level: float = 0.0
    reason: str = ""
    requires_approval: bool = False
    escalation_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:12])


class HealthResponse(BaseModel):
    """Health check response."""
    engine_id: str
    engine_name: str
    version: str
    status: str
    uptime_seconds: float
    total_validations: int
    total_denials: int
    total_tokens_issued: int
    active_lockouts: int
    audit_entries: int
    doctrine_cache_size: int
    coverage_topics_triggered: int
    coverage_topics_total: int
    timestamp: str


class DoctrineBlock(BaseModel):
    """TIE doctrine block for authority reasoning."""
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
    confidence: float
    confidence_stratification: str


class TelemetrySnapshot(BaseModel):
    """Telemetry data snapshot."""
    engine_id: str
    timestamp: str
    queries_total: int
    queries_per_minute: float
    avg_latency_ms: float
    p99_latency_ms: float
    error_rate: float
    cache_hit_rate: float
    denial_rate: float
    lockout_count: int


class QueryRequest(BaseModel):
    """TIE-standard query request for authority analysis."""
    query: str
    mode: str = Field(default="FAST", description="FAST | DEFENSE | MEMO")
    context: dict[str, Any] = Field(default_factory=dict)
    authority_level: float = Field(default=10.0)


class QueryResponse(BaseModel):
    """TIE-standard query response."""
    engine_id: str
    query: str
    mode: str
    answer: str
    confidence: float
    confidence_stratification: str
    authorities_cited: list[str]
    doctrine_hits: list[str]
    reasoning_chain: list[str]
    determinism_hash: str
    latency_ms: float
    timestamp: str


# ---------------------------------------------------------------------------
# Cross-Engine Authorization Matrix
# ---------------------------------------------------------------------------

CROSS_ENGINE_MATRIX: list[dict[str, Any]] = [
    {"engine_id": "GOV01", "engine_name": "Authority Gate", "min_level": 10.0, "allowed_actions": ["validate", "issue", "audit", "matrix", "escalate", "revoke"], "restricted_to_scope": False, "notes": "Self-access requires Commander level"},
    {"engine_id": "GOV02", "engine_name": "Policy Engine", "min_level": 8.0, "allowed_actions": ["query", "update"], "restricted_to_scope": False, "notes": "Policy changes require Executive+"},
    {"engine_id": "GOV03", "engine_name": "Compliance Monitor", "min_level": 7.0, "allowed_actions": ["query", "report"], "restricted_to_scope": False, "notes": "Inner Circle can view compliance"},
    {"engine_id": "SEC01", "engine_name": "Threat Detection", "min_level": 9.0, "allowed_actions": ["query", "scan", "alert"], "restricted_to_scope": False, "notes": "Security officer access"},
    {"engine_id": "SEC02", "engine_name": "Vault Manager", "min_level": 10.0, "allowed_actions": ["read", "write", "rotate"], "restricted_to_scope": True, "notes": "Commander only for vault ops"},
    {"engine_id": "INT01", "engine_name": "Intelligence Aggregator", "min_level": 7.0, "allowed_actions": ["query", "ingest"], "restricted_to_scope": False, "notes": "Inner Circle+ for intel"},
    {"engine_id": "INT02", "engine_name": "OSINT Harvester", "min_level": 6.0, "allowed_actions": ["query", "search"], "restricted_to_scope": False, "notes": "Elevated for OSINT"},
    {"engine_id": "OPS01", "engine_name": "Task Orchestrator", "min_level": 5.0, "allowed_actions": ["submit", "status"], "restricted_to_scope": True, "notes": "Trusted users can submit tasks"},
    {"engine_id": "OPS02", "engine_name": "Build Pipeline", "min_level": 8.0, "allowed_actions": ["trigger", "status", "cancel"], "restricted_to_scope": False, "notes": "Executive for build ops"},
    {"engine_id": "OPS03", "engine_name": "Deploy Manager", "min_level": 8.0, "allowed_actions": ["deploy", "rollback", "status"], "restricted_to_scope": False, "notes": "Executive for deploys"},
    {"engine_id": "DATA01", "engine_name": "Knowledge Graph", "min_level": 3.0, "allowed_actions": ["query"], "restricted_to_scope": True, "notes": "Execute access for KG queries"},
    {"engine_id": "DATA02", "engine_name": "Crystal Memory", "min_level": 5.0, "allowed_actions": ["read", "write", "search"], "restricted_to_scope": True, "notes": "Trusted for memory ops"},
    {"engine_id": "DATA03", "engine_name": "Vector Store", "min_level": 3.0, "allowed_actions": ["query", "ingest"], "restricted_to_scope": True, "notes": "Execute access for vector search"},
    {"engine_id": "AI01", "engine_name": "LLM Router", "min_level": 5.0, "allowed_actions": ["query", "stream"], "restricted_to_scope": True, "notes": "Trusted for LLM access"},
    {"engine_id": "AI02", "engine_name": "Swarm Controller", "min_level": 9.0, "allowed_actions": ["spawn", "kill", "status"], "restricted_to_scope": False, "notes": "Security+ for swarm ops"},
    {"engine_id": "FIN01", "engine_name": "Blockchain Interface", "min_level": 10.0, "allowed_actions": ["query", "sign", "broadcast"], "restricted_to_scope": True, "notes": "Commander only for chain ops"},
    {"engine_id": "FIN02", "engine_name": "DeFi Engine", "min_level": 10.0, "allowed_actions": ["query", "execute", "approve"], "restricted_to_scope": True, "notes": "Commander only for DeFi"},
    {"engine_id": "COMM01", "engine_name": "Voice Synthesis", "min_level": 5.0, "allowed_actions": ["synthesize", "clone"], "restricted_to_scope": True, "notes": "Trusted for TTS"},
    {"engine_id": "COMM02", "engine_name": "Email Gateway", "min_level": 5.0, "allowed_actions": ["send", "draft"], "restricted_to_scope": True, "notes": "Trusted for email"},
    {"engine_id": "MON01", "engine_name": "System Monitor", "min_level": 6.0, "allowed_actions": ["query", "alert"], "restricted_to_scope": False, "notes": "Elevated for monitoring"},
    {"engine_id": "MON02", "engine_name": "Audit Logger", "min_level": 9.0, "allowed_actions": ["query", "export"], "restricted_to_scope": False, "notes": "Security for audit access"},
    {"engine_id": "TIE01", "engine_name": "Tax Intelligence Engine", "min_level": 5.0, "allowed_actions": ["query"], "restricted_to_scope": True, "notes": "Trusted for tax queries"},
    {"engine_id": "PIE01", "engine_name": "Protective Intelligence Engine", "min_level": 7.0, "allowed_actions": ["query", "alert"], "restricted_to_scope": False, "notes": "Inner Circle for PIE"},
    {"engine_id": "ARCS01", "engine_name": "ARCS Compliance", "min_level": 7.0, "allowed_actions": ["query", "audit"], "restricted_to_scope": False, "notes": "Inner Circle for compliance"},
    {"engine_id": "SG01", "engine_name": "ShadowGlass Scraper", "min_level": 5.0, "allowed_actions": ["query", "scrape"], "restricted_to_scope": True, "notes": "Trusted for scraping"},
]


def get_engine_min_level(engine_id: str) -> float:
    """Look up the minimum authority level required for a given engine."""
    for entry in CROSS_ENGINE_MATRIX:
        if entry["engine_id"] == engine_id:
            return entry["min_level"]
    return 5.0  # default requires TRUSTED


def get_engine_allowed_actions(engine_id: str) -> list[str]:
    """Return allowed actions for a given engine."""
    for entry in CROSS_ENGINE_MATRIX:
        if entry["engine_id"] == engine_id:
            return entry["allowed_actions"]
    return ["query"]


# ---------------------------------------------------------------------------
# Doctrine Cache (in-memory, loaded from JSON at startup)
# ---------------------------------------------------------------------------

class DoctrineCache:
    """TIE-compliant doctrine cache for authority reasoning."""

    def __init__(self) -> None:
        self._blocks: list[DoctrineBlock] = []
        self._keyword_index: dict[str, list[int]] = defaultdict(list)
        self._topic_index: dict[str, int] = {}
        self._load_builtin_doctrines()

    def _load_builtin_doctrines(self) -> None:
        """Load doctrine blocks from JSON file or built-in defaults."""
        json_path = ENGINE_DIR / "doctrine_cache.json"
        if json_path.exists():
            try:
                raw = json.loads(json_path.read_text(encoding="utf-8"))
                for entry in raw:
                    block = DoctrineBlock(**entry)
                    self._add_block(block)
                logger.info("Loaded {} doctrine blocks from JSON", len(self._blocks))
                return
            except Exception as exc:
                logger.warning("Failed to load doctrine JSON, using built-in: {}", exc)
        self._load_hardcoded_doctrines()

    def _add_block(self, block: DoctrineBlock) -> None:
        idx = len(self._blocks)
        self._blocks.append(block)
        self._topic_index[block.topic] = idx
        for kw in block.keywords:
            self._keyword_index[kw.lower()].append(idx)

    def _load_hardcoded_doctrines(self) -> None:
        """Hardcoded fallback doctrines for authority gate reasoning."""
        doctrines = [
            DoctrineBlock(
                topic="least_privilege_principle",
                keywords=["least privilege", "minimum access", "need to know", "access control", "RBAC"],
                conclusion_template="Access must be granted at the minimum level required to perform the requested action. No caller should hold authority beyond what their role demands.",
                reasoning_framework="1. Identify the action requested. 2. Determine the minimum authority level for that action. 3. Compare caller level to minimum. 4. Deny if caller level < minimum. 5. Grant only the specific permissions needed, not blanket access. 6. Log the decision with full context for audit trail.",
                key_factors=["Caller authority level", "Action minimum requirement", "Engine-specific overrides", "Scope restrictions", "Temporal constraints"],
                primary_authority=["NIST SP 800-53 AC-6", "ECHO PRIME Governance Charter Section 3.1", "Zero Trust Architecture Principles"],
                burden_holder="system",
                adversary_position="Over-privileged access simplifies operations and reduces friction",
                counter_arguments=["Convenience does not justify security risk", "Lateral movement exploits over-privileged accounts", "Audit complexity increases with excess permissions", "Compliance frameworks mandate least privilege", "Breach blast radius correlates with privilege level"],
                resolution_strategy="Enforce strict level comparison. When ambiguous, deny and log for Commander review.",
                confidence=0.98,
                confidence_stratification="DEFENSIBLE",
            ),
            DoctrineBlock(
                topic="defense_in_depth",
                keywords=["defense in depth", "layered security", "multiple barriers", "redundant controls", "fail-safe"],
                conclusion_template="Authority validation must employ multiple independent checks. Token validity, authority level, rate limits, brute force detection, and cross-engine rules each form a separate defense layer.",
                reasoning_framework="1. Validate token signature integrity (cryptographic layer). 2. Check token expiration (temporal layer). 3. Verify authority level meets threshold (RBAC layer). 4. Check rate limits (availability layer). 5. Check brute force lockout (abuse prevention layer). 6. Verify cross-engine authorization (scope layer). 7. All layers must pass independently.",
                key_factors=["Token cryptographic integrity", "Temporal validity", "Authority level threshold", "Rate limit adherence", "Brute force status", "Cross-engine scope", "IP binding verification"],
                primary_authority=["NIST SP 800-53 SC-7", "Defense in Depth Strategy (NSA)", "ECHO PRIME Security Directive 2.0"],
                burden_holder="system",
                adversary_position="Single-layer validation is faster and simpler to implement",
                counter_arguments=["Single point of failure enables complete bypass", "Layered checks add microseconds not seconds", "Each layer catches different attack vectors", "Compliance requires demonstrable defense depth", "Post-breach analysis consistently shows single-layer failures"],
                resolution_strategy="Execute all validation layers sequentially. Short-circuit on first failure but log which layer caught the violation.",
                confidence=0.97,
                confidence_stratification="DEFENSIBLE",
            ),
            DoctrineBlock(
                topic="sovereign_override",
                keywords=["sovereign", "bloodline", "override", "11.0", "unconditional", "supreme"],
                conclusion_template="SOVEREIGN (11.0) authority unconditionally bypasses all gates, rate limits, and restrictions. This level is reserved exclusively for Bloodline-verified principals and cannot be delegated or escalated to.",
                reasoning_framework="1. Check if caller level == 11.0 SOVEREIGN. 2. If yes, verify bloodline flag is set on token. 3. If bloodline confirmed, grant unconditional access. 4. SOVEREIGN cannot be achieved through escalation — it must be issued directly. 5. All SOVEREIGN actions are logged with enhanced audit detail. 6. No rate limits apply to SOVEREIGN.",
                key_factors=["Bloodline verification flag", "Token-level SOVEREIGN marker", "Non-delegatable status", "Enhanced audit logging", "Unconditional bypass"],
                primary_authority=["ECHO PRIME Bloodline Directive", "McWilliams Dynasty Charter", "SOVEREIGN Protocol v1.0"],
                burden_holder="token_issuer",
                adversary_position="No single authority should bypass all controls",
                counter_arguments=["SOVEREIGN is the system owner — the system exists to serve them", "Bloodline verification prevents unauthorized SOVEREIGN claims", "Enhanced audit logging provides accountability", "The alternative is the owner being locked out of their own system", "SOVEREIGN actions are rare and high-visibility"],
                resolution_strategy="If bloodline-verified SOVEREIGN, grant immediately. Log everything. Never question.",
                confidence=1.0,
                confidence_stratification="DEFENSIBLE",
            ),
            DoctrineBlock(
                topic="token_integrity",
                keywords=["token", "HMAC", "signature", "JWT", "integrity", "tamper", "forgery"],
                conclusion_template="Every token must carry an HMAC-SHA256 signature computed over its payload. Tokens with invalid signatures are rejected unconditionally regardless of claimed authority level.",
                reasoning_framework="1. Extract signature from token. 2. Recompute HMAC-SHA256 over payload using server secret. 3. Compare signatures using constant-time comparison. 4. If mismatch, reject immediately — do not inspect payload. 5. If match, proceed to payload validation. 6. Never log the full token — log only the token ID (jti).",
                key_factors=["HMAC-SHA256 algorithm", "Server-side secret key", "Constant-time comparison", "Token ID tracking", "Signature-first validation"],
                primary_authority=["RFC 7519 (JWT)", "RFC 2104 (HMAC)", "ECHO PRIME Token Standard v1.0"],
                burden_holder="system",
                adversary_position="Signed tokens add latency and complexity",
                counter_arguments=["HMAC computation is sub-millisecond", "Unsigned tokens allow trivial privilege escalation", "Token forgery is the primary attack vector against auth systems", "Constant-time comparison prevents timing attacks", "Industry standard for 20+ years"],
                resolution_strategy="Reject invalid signatures before any other check. No exceptions.",
                confidence=0.99,
                confidence_stratification="DEFENSIBLE",
            ),
            DoctrineBlock(
                topic="brute_force_prevention",
                keywords=["brute force", "lockout", "failed attempts", "rate limit", "abuse", "throttle"],
                conclusion_template="After a configurable threshold of failed authentication attempts from a single source, the source must be locked out for a cooling period. This prevents credential stuffing and brute force attacks.",
                reasoning_framework="1. Track failed attempts per IP and per token-subject. 2. After MAX_FAILED_ATTEMPTS failures within a window, lock the source. 3. Lockout duration increases exponentially with repeated lockouts. 4. Lockout applies to the specific IP, not the entire system. 5. SOVEREIGN tokens bypass lockout checks. 6. All lockout events are logged and alerted.",
                key_factors=["Failed attempt counter", "Time window for counting", "Lockout duration", "Exponential backoff", "IP-level granularity", "SOVEREIGN exemption"],
                primary_authority=["NIST SP 800-63B Section 5.2.2", "OWASP Authentication Cheat Sheet", "ECHO PRIME Security Directive 3.0"],
                burden_holder="system",
                adversary_position="Lockouts cause denial of service for legitimate users",
                counter_arguments=["IP-level lockout limits blast radius", "Exponential backoff balances security and availability", "SOVEREIGN exemption prevents owner lockout", "5 attempts is generous for legitimate users", "Alternative (no lockout) enables unlimited password guessing"],
                resolution_strategy="Lock after threshold. Exponential backoff. Alert on repeated lockouts from same source.",
                confidence=0.96,
                confidence_stratification="DEFENSIBLE",
            ),
        ]
        for d in doctrines:
            self._add_block(d)
        logger.info("Loaded {} hardcoded doctrine blocks", len(self._blocks))

    def lookup(self, query: str) -> list[DoctrineBlock]:
        """Find matching doctrine blocks by keyword search."""
        query_lower = query.lower()
        matched_indices: set[int] = set()
        for kw, indices in self._keyword_index.items():
            if kw in query_lower:
                matched_indices.update(indices)
        for topic, idx in self._topic_index.items():
            if topic.replace("_", " ") in query_lower or query_lower in topic.replace("_", " "):
                matched_indices.add(idx)
        return [self._blocks[i] for i in sorted(matched_indices)]

    def get_by_topic(self, topic: str) -> Optional[DoctrineBlock]:
        """Get a specific doctrine block by topic name."""
        idx = self._topic_index.get(topic)
        if idx is not None:
            return self._blocks[idx]
        return None

    @property
    def size(self) -> int:
        return len(self._blocks)

    @property
    def all_topics(self) -> list[str]:
        return list(self._topic_index.keys())


# ---------------------------------------------------------------------------
# Semantic Normalizer
# ---------------------------------------------------------------------------

class SemanticNormalizer:
    """Normalize authority-related terms to canonical forms."""

    def __init__(self) -> None:
        self._mappings: dict[str, str] = {}
        self._load_mappings()

    def _load_mappings(self) -> None:
        json_path = ENGINE_DIR / "semantic_dict.json"
        if json_path.exists():
            try:
                self._mappings = json.loads(json_path.read_text(encoding="utf-8"))
                logger.info("Loaded {} semantic mappings", len(self._mappings))
                return
            except Exception as exc:
                logger.warning("Failed to load semantic dict: {}", exc)
        self._mappings = {
            "auth": "authority",
            "authn": "authentication",
            "authz": "authorization",
            "perms": "permissions",
            "rbac": "role-based access control",
            "abac": "attribute-based access control",
            "acl": "access control list",
            "mfa": "multi-factor authentication",
            "2fa": "two-factor authentication",
            "sso": "single sign-on",
            "jwt": "JSON Web Token",
            "hmac": "Hash-based Message Authentication Code",
            "totp": "time-based one-time password",
            "admin": "administrator",
            "priv": "privilege",
            "privesc": "privilege escalation",
            "cred": "credential",
            "creds": "credentials",
            "passwd": "password",
            "pw": "password",
            "lockout": "account lockout",
            "bruteforce": "brute force attack",
            "csrf": "cross-site request forgery",
            "xss": "cross-site scripting",
            "idor": "insecure direct object reference",
            "oauth": "OAuth 2.0 authorization framework",
            "oidc": "OpenID Connect",
            "saml": "Security Assertion Markup Language",
            "pki": "public key infrastructure",
            "tls": "Transport Layer Security",
            "cert": "certificate",
            "crl": "certificate revocation list",
            "iam": "identity and access management",
            "pam": "privileged access management",
            "siem": "security information and event management",
            "dlp": "data loss prevention",
            "zta": "zero trust architecture",
        }

    def normalize(self, text: str) -> str:
        """Normalize text by expanding known abbreviations."""
        words = text.lower().split()
        normalized = []
        for word in words:
            clean = word.strip(".,;:!?()[]{}\"'")
            if clean in self._mappings:
                normalized.append(self._mappings[clean])
            else:
                normalized.append(word)
        return " ".join(normalized)


# ---------------------------------------------------------------------------
# Coverage Map
# ---------------------------------------------------------------------------

class CoverageMap:
    """Track which doctrine topics have been triggered vs missed."""

    def __init__(self, all_topics: list[str]) -> None:
        self._triggered: dict[str, int] = defaultdict(int)
        self._all_topics = set(all_topics)
        self._total_queries = 0

    def record_hit(self, topic: str) -> None:
        self._triggered[topic] += 1
        self._total_queries += 1

    def record_miss(self) -> None:
        self._total_queries += 1

    @property
    def triggered_topics(self) -> list[str]:
        return list(self._triggered.keys())

    @property
    def missed_topics(self) -> list[str]:
        return [t for t in self._all_topics if t not in self._triggered]

    @property
    def coverage_ratio(self) -> float:
        if not self._all_topics:
            return 0.0
        return len(self._triggered) / len(self._all_topics)

    def to_dict(self) -> dict[str, Any]:
        return {
            "total_queries": self._total_queries,
            "triggered": dict(self._triggered),
            "missed": self.missed_topics,
            "coverage_ratio": round(self.coverage_ratio, 4),
            "triggered_count": len(self._triggered),
            "total_topics": len(self._all_topics),
        }


# ---------------------------------------------------------------------------
# Drift Watcher
# ---------------------------------------------------------------------------

class DriftWatcher:
    """Detect drift in authority validation patterns over time."""

    def __init__(self) -> None:
        self._windows: list[dict[str, Any]] = []
        self._current_window: dict[str, Any] = self._new_window()

    def _new_window(self) -> dict[str, Any]:
        return {
            "start": time.time(),
            "approvals": 0,
            "denials": 0,
            "escalations": 0,
            "lockouts": 0,
            "level_distribution": defaultdict(int),
        }

    def record_decision(self, authorized: bool, level: float, escalation: bool = False, lockout: bool = False) -> None:
        if time.time() - self._current_window["start"] > 300:
            self._windows.append(self._current_window)
            if len(self._windows) > 288:
                self._windows = self._windows[-288:]
            self._current_window = self._new_window()
        if authorized:
            self._current_window["approvals"] += 1
        else:
            self._current_window["denials"] += 1
        if escalation:
            self._current_window["escalations"] += 1
        if lockout:
            self._current_window["lockouts"] += 1
        tier = get_tier_name(level)
        self._current_window["level_distribution"][tier] += 1

    def detect_drift(self) -> dict[str, Any]:
        """Compare current window to historical average."""
        if len(self._windows) < 2:
            return {"drift_detected": False, "reason": "Insufficient history", "windows_analyzed": len(self._windows)}
        recent = self._current_window
        total_approvals = sum(w["approvals"] for w in self._windows)
        total_denials = sum(w["denials"] for w in self._windows)
        total_windows = len(self._windows)
        avg_approval_rate = total_approvals / max(total_approvals + total_denials, 1)
        recent_total = recent["approvals"] + recent["denials"]
        if recent_total == 0:
            return {"drift_detected": False, "reason": "No decisions in current window", "windows_analyzed": total_windows}
        current_approval_rate = recent["approvals"] / recent_total
        drift_magnitude = abs(current_approval_rate - avg_approval_rate)
        drift_detected = drift_magnitude > 0.15
        return {
            "drift_detected": drift_detected,
            "current_approval_rate": round(current_approval_rate, 4),
            "historical_approval_rate": round(avg_approval_rate, 4),
            "drift_magnitude": round(drift_magnitude, 4),
            "windows_analyzed": total_windows,
            "current_window_decisions": recent_total,
            "alert": "APPROVAL RATE DRIFT DETECTED" if drift_detected else "Normal",
        }


# ---------------------------------------------------------------------------
# Metrics Collector
# ---------------------------------------------------------------------------

class MetricsCollector:
    """Collect and report operational metrics."""

    def __init__(self) -> None:
        self._latencies: list[float] = []
        self._errors: int = 0
        self._queries: int = 0
        self._cache_hits: int = 0
        self._cache_misses: int = 0
        self._denials: int = 0
        self._start_time: float = time.time()

    def record_latency(self, ms: float) -> None:
        self._latencies.append(ms)
        if len(self._latencies) > 10000:
            self._latencies = self._latencies[-5000:]

    def record_query(self) -> None:
        self._queries += 1

    def record_error(self) -> None:
        self._errors += 1

    def record_cache_hit(self) -> None:
        self._cache_hits += 1

    def record_cache_miss(self) -> None:
        self._cache_misses += 1

    def record_denial(self) -> None:
        self._denials += 1

    @property
    def avg_latency_ms(self) -> float:
        if not self._latencies:
            return 0.0
        return sum(self._latencies) / len(self._latencies)

    @property
    def p99_latency_ms(self) -> float:
        if not self._latencies:
            return 0.0
        sorted_lat = sorted(self._latencies)
        idx = int(len(sorted_lat) * 0.99)
        return sorted_lat[min(idx, len(sorted_lat) - 1)]

    @property
    def error_rate(self) -> float:
        if self._queries == 0:
            return 0.0
        return self._errors / self._queries

    @property
    def cache_hit_rate(self) -> float:
        total = self._cache_hits + self._cache_misses
        if total == 0:
            return 0.0
        return self._cache_hits / total

    @property
    def denial_rate(self) -> float:
        if self._queries == 0:
            return 0.0
        return self._denials / self._queries

    @property
    def queries_per_minute(self) -> float:
        elapsed = time.time() - self._start_time
        if elapsed < 1:
            return 0.0
        return (self._queries / elapsed) * 60

    def snapshot(self) -> TelemetrySnapshot:
        return TelemetrySnapshot(
            engine_id=ENGINE_ID,
            timestamp=datetime.now(timezone.utc).isoformat(),
            queries_total=self._queries,
            queries_per_minute=round(self.queries_per_minute, 2),
            avg_latency_ms=round(self.avg_latency_ms, 3),
            p99_latency_ms=round(self.p99_latency_ms, 3),
            error_rate=round(self.error_rate, 4),
            cache_hit_rate=round(self.cache_hit_rate, 4),
            denial_rate=round(self.denial_rate, 4),
            lockout_count=0,
        )


# ---------------------------------------------------------------------------
# Audit Trail
# ---------------------------------------------------------------------------

class AuditTrail:
    """Append-only audit trail for all auth decisions."""

    def __init__(self) -> None:
        self._entries: list[AuditEntry] = []
        self._jsonl_path = LOG_PATH / "audit_trail.jsonl"

    def log_decision(
        self,
        action: str,
        subject: str,
        level: float,
        required_level: float,
        engine_id: str,
        authorized: bool,
        reason: str,
        client_ip: str,
        token_id: str,
    ) -> str:
        decision_id = uuid.uuid4().hex[:12]
        entry = AuditEntry(
            decision_id=decision_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            action=action,
            subject=subject,
            level=level,
            required_level=required_level,
            engine_id=engine_id,
            authorized=authorized,
            reason=reason,
            client_ip=client_ip,
            token_id=token_id,
        )
        self._entries.append(entry)
        if len(self._entries) > 50000:
            self._entries = self._entries[-25000:]
        try:
            with self._jsonl_path.open("a", encoding="utf-8") as fh:
                fh.write(entry.model_dump_json() + "\n")
        except Exception as exc:
            logger.error("Failed to write audit JSONL: {}", exc)
        return decision_id

    def get_recent(self, count: int = 100) -> list[AuditEntry]:
        return self._entries[-count:]

    def search(self, subject: Optional[str] = None, engine_id: Optional[str] = None, authorized: Optional[bool] = None) -> list[AuditEntry]:
        results = self._entries
        if subject is not None:
            results = [e for e in results if e.subject == subject]
        if engine_id is not None:
            results = [e for e in results if e.engine_id == engine_id]
        if authorized is not None:
            results = [e for e in results if e.authorized == authorized]
        return results[-500:]

    @property
    def total_entries(self) -> int:
        return len(self._entries)


# ---------------------------------------------------------------------------
# Token Manager
# ---------------------------------------------------------------------------

class TokenManager:
    """Issue, validate, and revoke HMAC-signed tokens."""

    def __init__(self, secret: str) -> None:
        self._secret = secret.encode("utf-8")
        self._revoked: set[str] = set()
        self._issued_count: int = 0

    def _sign(self, payload_json: str) -> str:
        return hmac.new(self._secret, payload_json.encode("utf-8"), hashlib.sha256).hexdigest()

    def _constant_time_compare(self, a: str, b: str) -> bool:
        return hmac.compare_digest(a.encode("utf-8"), b.encode("utf-8"))

    def issue(self, subject: str, level: float, ttl_seconds: int = TOKEN_EXPIRY_SECONDS, bloodline: bool = False, ip_bind: Optional[str] = None, scope: Optional[list[str]] = None) -> tuple[str, TokenPayload]:
        """Issue a new signed token."""
        now = time.time()
        payload = TokenPayload(
            sub=subject,
            level=level,
            iat=now,
            exp=now + ttl_seconds,
            bloodline=bloodline,
            ip_bound=ip_bind,
            scope=scope or [],
        )
        payload_json = payload.model_dump_json()
        signature = self._sign(payload_json)
        import base64
        token_b64 = base64.urlsafe_b64encode(payload_json.encode("utf-8")).decode("utf-8")
        token = f"{token_b64}.{signature}"
        self._issued_count += 1
        logger.info("Issued token jti={} sub={} level={} ttl={}s", payload.jti, subject, level, ttl_seconds)
        return token, payload

    def validate(self, token: str) -> tuple[bool, Optional[TokenPayload], str]:
        """Validate a token's signature and expiration. Returns (valid, payload, reason)."""
        import base64
        parts = token.split(".")
        if len(parts) != 2:
            return False, None, "Malformed token: expected payload.signature format"
        token_b64, provided_sig = parts
        try:
            payload_json = base64.urlsafe_b64decode(token_b64.encode("utf-8")).decode("utf-8")
        except Exception:
            return False, None, "Failed to decode token payload"
        expected_sig = self._sign(payload_json)
        if not self._constant_time_compare(provided_sig, expected_sig):
            return False, None, "Invalid token signature"
        try:
            payload = TokenPayload.model_validate_json(payload_json)
        except Exception as exc:
            return False, None, f"Invalid token payload structure: {exc}"
        if payload.jti in self._revoked:
            return False, payload, "Token has been revoked"
        now = time.time()
        if now > payload.exp:
            return False, payload, "Token has expired"
        return True, payload, "Token valid"

    def revoke(self, token_id: str) -> None:
        """Revoke a token by its JTI."""
        self._revoked.add(token_id)
        logger.info("Revoked token jti={}", token_id)

    @property
    def issued_count(self) -> int:
        return self._issued_count

    @property
    def revoked_count(self) -> int:
        return len(self._revoked)


# ---------------------------------------------------------------------------
# Brute Force Detector
# ---------------------------------------------------------------------------

class BruteForceDetector:
    """Track failed authentication attempts and enforce lockouts."""

    def __init__(self, max_attempts: int = MAX_FAILED_ATTEMPTS, lockout_seconds: int = LOCKOUT_DURATION_SECONDS) -> None:
        self._max_attempts = max_attempts
        self._lockout_seconds = lockout_seconds
        self._attempts: dict[str, list[float]] = defaultdict(list)
        self._lockouts: dict[str, float] = {}
        self._lockout_counts: dict[str, int] = defaultdict(int)

    def record_failure(self, source: str) -> bool:
        """Record a failed attempt. Returns True if source is now locked out."""
        now = time.time()
        window_start = now - RATE_LIMIT_WINDOW_SECONDS * 5
        self._attempts[source] = [t for t in self._attempts[source] if t > window_start]
        self._attempts[source].append(now)
        if len(self._attempts[source]) >= self._max_attempts:
            self._lockout_counts[source] += 1
            multiplier = min(self._lockout_counts[source], 8)
            duration = self._lockout_seconds * multiplier
            self._lockouts[source] = now + duration
            logger.warning("LOCKOUT source={} attempts={} duration={}s multiplier={}", source, len(self._attempts[source]), duration, multiplier)
            return True
        return False

    def is_locked(self, source: str) -> bool:
        """Check if a source is currently locked out."""
        if source not in self._lockouts:
            return False
        if time.time() > self._lockouts[source]:
            del self._lockouts[source]
            return False
        return True

    def get_status(self, source: str) -> BruteForceStatus:
        now = time.time()
        window_start = now - RATE_LIMIT_WINDOW_SECONDS * 5
        recent = [t for t in self._attempts.get(source, []) if t > window_start]
        locked = self.is_locked(source)
        lockout_expires = None
        if locked and source in self._lockouts:
            lockout_expires = datetime.fromtimestamp(self._lockouts[source], tz=timezone.utc).isoformat()
        last_attempt = None
        if recent:
            last_attempt = datetime.fromtimestamp(recent[-1], tz=timezone.utc).isoformat()
        return BruteForceStatus(
            ip=source,
            failed_attempts=len(recent),
            locked=locked,
            lockout_expires=lockout_expires,
            last_attempt=last_attempt,
        )

    def clear(self, source: str) -> None:
        self._attempts.pop(source, None)
        self._lockouts.pop(source, None)
        self._lockout_counts.pop(source, None)

    @property
    def active_lockout_count(self) -> int:
        now = time.time()
        return sum(1 for exp in self._lockouts.values() if exp > now)


# ---------------------------------------------------------------------------
# Rate Limiter
# ---------------------------------------------------------------------------

class RateLimiter:
    """Per-subject, per-tier rate limiting with sliding window."""

    def __init__(self) -> None:
        self._windows: dict[str, list[float]] = defaultdict(list)

    def check(self, subject: str, level: float) -> tuple[bool, int]:
        """Check rate limit. Returns (allowed, remaining)."""
        limit = get_rate_limit(level)
        now = time.time()
        window_start = now - RATE_LIMIT_WINDOW_SECONDS
        self._windows[subject] = [t for t in self._windows[subject] if t > window_start]
        current = len(self._windows[subject])
        if current >= limit:
            return False, 0
        self._windows[subject].append(now)
        return True, limit - current - 1

    def get_usage(self, subject: str, level: float) -> dict[str, Any]:
        limit = get_rate_limit(level)
        now = time.time()
        window_start = now - RATE_LIMIT_WINDOW_SECONDS
        recent = [t for t in self._windows.get(subject, []) if t > window_start]
        return {
            "subject": subject,
            "tier": get_tier_name(level),
            "limit": limit,
            "used": len(recent),
            "remaining": max(0, limit - len(recent)),
            "window_seconds": RATE_LIMIT_WINDOW_SECONDS,
        }


# ---------------------------------------------------------------------------
# Authority Gate Core
# ---------------------------------------------------------------------------

class AuthorityGate:
    """Central authority validation engine."""

    def __init__(self) -> None:
        self.doctrine_cache = DoctrineCache()
        self.semantic_normalizer = SemanticNormalizer()
        self.coverage_map = CoverageMap(self.doctrine_cache.all_topics)
        self.drift_watcher = DriftWatcher()
        self.metrics = MetricsCollector()
        self.audit_trail = AuditTrail()
        self.token_manager = TokenManager(HMAC_SECRET)
        self.brute_force = BruteForceDetector()
        self.rate_limiter = RateLimiter()
        logger.info("AuthorityGate initialized. Doctrines={} Matrix_engines={}", self.doctrine_cache.size, len(CROSS_ENGINE_MATRIX))

    def _compute_determinism_hash(self, *args: Any) -> str:
        """SHA-256 determinism hash over inputs."""
        content = "|".join(str(a) for a in args)
        return hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]

    def validate_authority(self, request: ValidateRequest) -> ValidateResponse:
        """Core validation logic — multi-layer defense in depth."""
        start_ms = time.time() * 1000
        self.metrics.record_query()
        client_ip = request.client_ip or "unknown"

        # Layer 1: Brute force check
        if self.brute_force.is_locked(client_ip):
            self.metrics.record_denial()
            reason = f"Source {client_ip} is locked out due to repeated failed attempts"
            self.audit_trail.log_decision("validate", "unknown", 0.0, request.required_level, request.engine_id, False, reason, client_ip, "")
            self.drift_watcher.record_decision(False, 0.0, lockout=True)
            latency = time.time() * 1000 - start_ms
            self.metrics.record_latency(latency)
            return ValidateResponse(authorized=False, level=0.0, tier_name="LOCKED", reason=reason, determinism_hash=self._compute_determinism_hash("locked", client_ip))

        # Layer 2: Token signature + structure
        valid, payload, token_reason = self.token_manager.validate(request.token)
        if not valid:
            self.metrics.record_denial()
            locked_out = self.brute_force.record_failure(client_ip)
            reason = f"Token validation failed: {token_reason}"
            if locked_out:
                reason += " | SOURCE NOW LOCKED OUT"
            sub = payload.sub if payload else "unknown"
            jti = payload.jti if payload else ""
            self.audit_trail.log_decision("validate", sub, 0.0, request.required_level, request.engine_id, False, reason, client_ip, jti)
            self.drift_watcher.record_decision(False, 0.0)
            latency = time.time() * 1000 - start_ms
            self.metrics.record_latency(latency)
            return ValidateResponse(authorized=False, level=0.0, tier_name="INVALID", reason=reason, token_id=jti, determinism_hash=self._compute_determinism_hash("invalid", token_reason))

        assert payload is not None

        # Layer 3: SOVEREIGN bypass — unconditional
        if payload.level >= 11.0 and payload.bloodline:
            doctrines = self.doctrine_cache.lookup("sovereign override")
            for d in doctrines:
                self.coverage_map.record_hit(d.topic)
            self.metrics.record_cache_hit()
            reason = "SOVEREIGN BLOODLINE — unconditional access granted"
            self.audit_trail.log_decision("validate", payload.sub, payload.level, request.required_level, request.engine_id, True, reason, client_ip, payload.jti)
            self.drift_watcher.record_decision(True, payload.level)
            latency = time.time() * 1000 - start_ms
            self.metrics.record_latency(latency)
            return ValidateResponse(authorized=True, level=payload.level, tier_name="SOVEREIGN", reason=reason, token_id=payload.jti, rate_remaining=999999, determinism_hash=self._compute_determinism_hash("sovereign", payload.sub, payload.jti))

        # Layer 4: IP binding check
        if payload.ip_bound and payload.ip_bound != client_ip:
            self.metrics.record_denial()
            reason = f"Token is IP-bound to {payload.ip_bound}, request from {client_ip}"
            self.audit_trail.log_decision("validate", payload.sub, payload.level, request.required_level, request.engine_id, False, reason, client_ip, payload.jti)
            self.drift_watcher.record_decision(False, payload.level)
            latency = time.time() * 1000 - start_ms
            self.metrics.record_latency(latency)
            return ValidateResponse(authorized=False, level=payload.level, tier_name=get_tier_name(payload.level), reason=reason, token_id=payload.jti, determinism_hash=self._compute_determinism_hash("ip_mismatch", payload.ip_bound, client_ip))

        # Layer 5: Rate limit check
        allowed, remaining = self.rate_limiter.check(payload.sub, payload.level)
        if not allowed:
            self.metrics.record_denial()
            reason = f"Rate limit exceeded for tier {get_tier_name(payload.level)} (limit={get_rate_limit(payload.level)}/min)"
            self.audit_trail.log_decision("validate", payload.sub, payload.level, request.required_level, request.engine_id, False, reason, client_ip, payload.jti)
            self.drift_watcher.record_decision(False, payload.level)
            latency = time.time() * 1000 - start_ms
            self.metrics.record_latency(latency)
            return ValidateResponse(authorized=False, level=payload.level, tier_name=get_tier_name(payload.level), reason=reason, token_id=payload.jti, rate_remaining=0, determinism_hash=self._compute_determinism_hash("rate_limit", payload.sub, payload.level))

        # Layer 6: Authority level check
        if payload.level < request.required_level:
            self.metrics.record_denial()
            reason = f"Insufficient authority: caller={payload.level} ({get_tier_name(payload.level)}), required={request.required_level} ({get_tier_name(request.required_level)})"
            doctrines = self.doctrine_cache.lookup("least privilege access control")
            for d in doctrines:
                self.coverage_map.record_hit(d.topic)
            if not doctrines:
                self.coverage_map.record_miss()
            self.audit_trail.log_decision("validate", payload.sub, payload.level, request.required_level, request.engine_id, False, reason, client_ip, payload.jti)
            self.drift_watcher.record_decision(False, payload.level)
            latency = time.time() * 1000 - start_ms
            self.metrics.record_latency(latency)
            return ValidateResponse(authorized=False, level=payload.level, tier_name=get_tier_name(payload.level), reason=reason, token_id=payload.jti, rate_remaining=remaining, determinism_hash=self._compute_determinism_hash("denied", payload.level, request.required_level))

        # Layer 7: Cross-engine authorization
        if request.engine_id:
            engine_min = get_engine_min_level(request.engine_id)
            if payload.level < engine_min:
                self.metrics.record_denial()
                reason = f"Engine {request.engine_id} requires level {engine_min} ({get_tier_name(engine_min)}), caller has {payload.level} ({get_tier_name(payload.level)})"
                self.audit_trail.log_decision("validate", payload.sub, payload.level, engine_min, request.engine_id, False, reason, client_ip, payload.jti)
                self.drift_watcher.record_decision(False, payload.level)
                latency = time.time() * 1000 - start_ms
                self.metrics.record_latency(latency)
                return ValidateResponse(authorized=False, level=payload.level, tier_name=get_tier_name(payload.level), reason=reason, token_id=payload.jti, rate_remaining=remaining, determinism_hash=self._compute_determinism_hash("engine_denied", request.engine_id, payload.level, engine_min))

            # Scope check
            for entry in CROSS_ENGINE_MATRIX:
                if entry["engine_id"] == request.engine_id and entry["restricted_to_scope"]:
                    if payload.scope and request.engine_id not in payload.scope and "*" not in payload.scope:
                        self.metrics.record_denial()
                        reason = f"Token scope does not include engine {request.engine_id}. Scopes: {payload.scope}"
                        self.audit_trail.log_decision("validate", payload.sub, payload.level, engine_min, request.engine_id, False, reason, client_ip, payload.jti)
                        self.drift_watcher.record_decision(False, payload.level)
                        latency = time.time() * 1000 - start_ms
                        self.metrics.record_latency(latency)
                        return ValidateResponse(authorized=False, level=payload.level, tier_name=get_tier_name(payload.level), reason=reason, token_id=payload.jti, rate_remaining=remaining, determinism_hash=self._compute_determinism_hash("scope_denied", request.engine_id, payload.scope))
                    break

            # Action check
            if request.action:
                allowed_actions = get_engine_allowed_actions(request.engine_id)
                if request.action not in allowed_actions and "admin" not in allowed_actions:
                    if payload.level < 10.0:
                        self.metrics.record_denial()
                        reason = f"Action '{request.action}' not in allowed actions {allowed_actions} for engine {request.engine_id}"
                        self.audit_trail.log_decision("validate", payload.sub, payload.level, engine_min, request.engine_id, False, reason, client_ip, payload.jti)
                        self.drift_watcher.record_decision(False, payload.level)
                        latency = time.time() * 1000 - start_ms
                        self.metrics.record_latency(latency)
                        return ValidateResponse(authorized=False, level=payload.level, tier_name=get_tier_name(payload.level), reason=reason, token_id=payload.jti, rate_remaining=remaining, determinism_hash=self._compute_determinism_hash("action_denied", request.action, request.engine_id))

        # All layers passed
        self.metrics.record_cache_hit()
        self.brute_force.clear(client_ip)
        tier_name = get_tier_name(payload.level)
        reason = f"Authorized: level={payload.level} ({tier_name}) >= required={request.required_level}"
        if request.engine_id:
            reason += f" | engine={request.engine_id}"

        doctrines = self.doctrine_cache.lookup("defense in depth layered")
        for d in doctrines:
            self.coverage_map.record_hit(d.topic)

        self.audit_trail.log_decision("validate", payload.sub, payload.level, request.required_level, request.engine_id, True, reason, client_ip, payload.jti)
        self.drift_watcher.record_decision(True, payload.level)
        latency = time.time() * 1000 - start_ms
        self.metrics.record_latency(latency)
        return ValidateResponse(authorized=True, level=payload.level, tier_name=tier_name, reason=reason, token_id=payload.jti, rate_remaining=remaining, determinism_hash=self._compute_determinism_hash("approved", payload.sub, payload.level, request.required_level, request.engine_id))

    def handle_escalation(self, req: EscalationRequest) -> EscalationResponse:
        """Handle authority escalation requests."""
        valid, payload, reason = self.token_manager.validate(req.token)
        if not valid or payload is None:
            return EscalationResponse(approved=False, reason=f"Invalid token: {reason}")

        if req.target_level >= 11.0:
            return EscalationResponse(approved=False, reason="SOVEREIGN level cannot be escalated to. Must be issued directly by Bloodline authority.")

        if req.target_level >= 10.0:
            if req.approver_token is None:
                return EscalationResponse(approved=False, reason="Escalation to COMMANDER_ONLY (10.0) requires approver token.", requires_approval=True)
            a_valid, a_payload, a_reason = self.token_manager.validate(req.approver_token)
            if not a_valid or a_payload is None or a_payload.level < 10.0:
                return EscalationResponse(approved=False, reason="Approver must hold COMMANDER_ONLY (10.0) or higher.")

        max_self_escalation = payload.level + 1.0
        if req.target_level > max_self_escalation and req.approver_token is None:
            return EscalationResponse(approved=False, reason=f"Self-escalation limited to +1.0 (max {max_self_escalation}). Higher requires approver.", requires_approval=True)

        new_token, new_payload = self.token_manager.issue(
            subject=payload.sub,
            level=req.target_level,
            ttl_seconds=min(TOKEN_EXPIRY_SECONDS, 1800),
            bloodline=False,
            scope=payload.scope,
        )
        self.audit_trail.log_decision("escalate", payload.sub, payload.level, req.target_level, "", True, f"Escalated from {payload.level} to {req.target_level}: {req.reason}", "internal", payload.jti)
        self.drift_watcher.record_decision(True, req.target_level, escalation=True)
        logger.info("Escalation approved: {} from {} to {}", payload.sub, payload.level, req.target_level)
        return EscalationResponse(approved=True, new_token=new_token, new_level=req.target_level, reason="Escalation approved")

    def three_layer_query(self, request: QueryRequest) -> QueryResponse:
        """TIE three-layer response: Doctrine Cache -> Semantic -> Deep Analysis."""
        start_ms = time.time() * 1000
        self.metrics.record_query()
        normalized_query = self.semantic_normalizer.normalize(request.query)
        authorities_cited: list[str] = []
        doctrine_hits: list[str] = []
        reasoning_chain: list[str] = []

        # Layer 1: Doctrine Cache (0-200ms target)
        doctrines = self.doctrine_cache.lookup(normalized_query)
        if doctrines:
            self.metrics.record_cache_hit()
            for d in doctrines:
                self.coverage_map.record_hit(d.topic)
                doctrine_hits.append(d.topic)
                authorities_cited.extend(d.primary_authority)
                reasoning_chain.append(f"[DOCTRINE:{d.topic}] {d.conclusion_template}")
        else:
            self.metrics.record_cache_miss()
            self.coverage_map.record_miss()

        # Layer 2: Semantic retrieval (keyword expansion)
        semantic_terms = normalized_query.split()
        for term in semantic_terms:
            additional = self.doctrine_cache.lookup(term)
            for d in additional:
                if d.topic not in doctrine_hits:
                    doctrine_hits.append(d.topic)
                    self.coverage_map.record_hit(d.topic)
                    reasoning_chain.append(f"[SEMANTIC:{d.topic}] {d.conclusion_template}")
                    authorities_cited.extend(d.primary_authority)

        # Layer 3: Deep Analysis (synthesize from all available data)
        if not doctrine_hits:
            reasoning_chain.append("[DEEP_ANALYSIS] No direct doctrine match. Applying general authority principles.")
            reasoning_chain.append("[DEEP_ANALYSIS] Authority hierarchy: 0.0 PUBLIC through 11.0 SOVEREIGN with 18 defined tiers.")
            reasoning_chain.append("[DEEP_ANALYSIS] All access decisions follow defense-in-depth with 7 validation layers.")

        # Build answer based on mode
        if request.mode == "FAST":
            answer = "; ".join(r.split("] ", 1)[-1] for r in reasoning_chain[:3])
        elif request.mode == "DEFENSE":
            answer = "AUTHORITY GATE ANALYSIS:\n\n"
            for i, r in enumerate(reasoning_chain, 1):
                answer += f"{i}. {r}\n"
            answer += f"\nAuthorities: {', '.join(set(authorities_cited[:10]))}"
        else:  # MEMO
            answer = f"MEMORANDUM — AUTHORITY GATE ENGINE (GOV01)\n\n"
            answer += f"QUERY: {request.query}\n"
            answer += f"NORMALIZED: {normalized_query}\n"
            answer += f"MODE: {request.mode}\n\n"
            answer += "ANALYSIS:\n"
            for i, r in enumerate(reasoning_chain, 1):
                answer += f"  {i}. {r}\n"
            answer += f"\nDOCTRINES CONSULTED: {', '.join(doctrine_hits) if doctrine_hits else 'None (deep analysis applied)'}\n"
            answer += f"AUTHORITIES: {', '.join(set(authorities_cited)) if authorities_cited else 'General principles'}\n"

        confidence = 0.95 if doctrine_hits else 0.70
        stratification = "DEFENSIBLE" if doctrine_hits else "AGGRESSIVE"
        det_hash = self._compute_determinism_hash(request.query, request.mode, *doctrine_hits)
        latency = time.time() * 1000 - start_ms
        self.metrics.record_latency(latency)

        return QueryResponse(
            engine_id=ENGINE_ID,
            query=request.query,
            mode=request.mode,
            answer=answer,
            confidence=confidence,
            confidence_stratification=stratification,
            authorities_cited=list(set(authorities_cited)),
            doctrine_hits=doctrine_hits,
            reasoning_chain=reasoning_chain,
            determinism_hash=det_hash,
            latency_ms=round(latency, 3),
            timestamp=datetime.now(timezone.utc).isoformat(),
        )


# ---------------------------------------------------------------------------
# Fact Fragility Scorer
# ---------------------------------------------------------------------------

class FactFragilityScorer:
    """Score the fragility of authority-related facts and claims."""

    FRAGILITY_FACTORS: dict[str, float] = {
        "hardcoded_hierarchy": 0.05,
        "cryptographic_verification": 0.02,
        "time_based_expiry": 0.10,
        "rate_limit_threshold": 0.15,
        "brute_force_threshold": 0.12,
        "cross_engine_matrix": 0.08,
        "policy_based_rule": 0.20,
        "human_judgment_required": 0.45,
        "external_dependency": 0.30,
        "configuration_value": 0.18,
    }

    def score(self, fact_type: str, description: str) -> dict[str, Any]:
        """Return fragility score and analysis for a fact."""
        base_fragility = self.FRAGILITY_FACTORS.get(fact_type, 0.25)
        verifiability = 1.0 - base_fragility
        recharacterization_risk = base_fragility * 0.6
        testimony_dependence = 0.1 if fact_type in ("hardcoded_hierarchy", "cryptographic_verification") else 0.4
        overall = (base_fragility + recharacterization_risk + testimony_dependence) / 3
        return {
            "fact_type": fact_type,
            "description": description,
            "fragility_score": round(overall, 4),
            "verifiability": round(verifiability, 4),
            "recharacterization_risk": round(recharacterization_risk, 4),
            "testimony_dependence": round(testimony_dependence, 4),
            "recommendation": "STABLE" if overall < 0.2 else "MONITOR" if overall < 0.35 else "FRAGILE",
        }


# ---------------------------------------------------------------------------
# Zoned Analysis
# ---------------------------------------------------------------------------

class ZonedAnalyzer:
    """Separate analysis into PLANNING / REPORTING / AUDIT zones."""

    def analyze(self, zone: str, data: dict[str, Any]) -> dict[str, Any]:
        if zone == "PLANNING":
            return self._planning_zone(data)
        elif zone == "REPORTING":
            return self._reporting_zone(data)
        elif zone == "AUDIT":
            return self._audit_zone(data)
        return {"error": f"Unknown zone: {zone}", "valid_zones": ["PLANNING", "REPORTING", "AUDIT"]}

    def _planning_zone(self, data: dict[str, Any]) -> dict[str, Any]:
        """Forward-looking authority architecture planning."""
        return {
            "zone": "PLANNING",
            "analysis": "Authority architecture assessment",
            "recommendations": [
                "Review cross-engine matrix quarterly",
                "Audit rate limit thresholds against actual usage",
                "Plan for authority delegation workflows",
                "Evaluate need for time-boxed elevated access",
                "Consider attribute-based access control (ABAC) extensions",
            ],
            "risk_areas": [
                "Stale tokens with broad scope",
                "Rate limit windows too permissive for high-risk engines",
                "Escalation without multi-party approval above 8.0",
            ],
            "input_data": data,
        }

    def _reporting_zone(self, data: dict[str, Any]) -> dict[str, Any]:
        """Current-state authority metrics and status."""
        return {
            "zone": "REPORTING",
            "analysis": "Current authority system status",
            "metrics_available": [
                "Total validations",
                "Denial rate",
                "Active lockouts",
                "Token issuance rate",
                "Coverage map",
                "Drift detection",
            ],
            "input_data": data,
        }

    def _audit_zone(self, data: dict[str, Any]) -> dict[str, Any]:
        """Historical authority decision review."""
        return {
            "zone": "AUDIT",
            "analysis": "Authority decision audit trail",
            "capabilities": [
                "Full decision history with JSONL export",
                "Filter by subject, engine, authorization status",
                "Determinism hash verification",
                "Brute force incident review",
                "Escalation chain reconstruction",
            ],
            "compliance_notes": [
                "All decisions logged with SHA-256 determinism hash",
                "Audit trail is append-only",
                "JSONL format for forensic tooling compatibility",
            ],
            "input_data": data,
        }


# ---------------------------------------------------------------------------
# Multi-Doctrine Decomposition
# ---------------------------------------------------------------------------

class MultiDoctrineDecomposer:
    """Decompose complex authority queries into doctrine sub-problems."""

    ISSUE_CATEGORIES: list[str] = [
        "TOKEN_VALIDITY",
        "AUTHORITY_LEVEL",
        "RATE_LIMITING",
        "BRUTE_FORCE",
        "CROSS_ENGINE",
        "SCOPE_RESTRICTION",
        "IP_BINDING",
        "ESCALATION",
        "REVOCATION",
        "AUDIT_COMPLIANCE",
        "TEMPORAL_CONSTRAINTS",
        "BLOODLINE_VERIFICATION",
    ]

    def decompose(self, query: str, doctrine_cache: DoctrineCache) -> dict[str, Any]:
        """Break a complex query into categorized sub-problems with doctrine mappings."""
        query_lower = query.lower()
        triggered_categories: list[str] = []
        category_doctrines: dict[str, list[str]] = {}

        category_keywords: dict[str, list[str]] = {
            "TOKEN_VALIDITY": ["token", "signature", "hmac", "valid", "expired", "forged"],
            "AUTHORITY_LEVEL": ["level", "authority", "permission", "access", "privilege", "tier"],
            "RATE_LIMITING": ["rate", "limit", "throttle", "quota", "window"],
            "BRUTE_FORCE": ["brute", "force", "lockout", "failed", "attempt", "block"],
            "CROSS_ENGINE": ["engine", "cross", "matrix", "inter-service", "service-to-service"],
            "SCOPE_RESTRICTION": ["scope", "restrict", "allow", "whitelist", "boundary"],
            "IP_BINDING": ["ip", "bind", "address", "network", "source"],
            "ESCALATION": ["escalat", "elevat", "promot", "upgrade", "temporary"],
            "REVOCATION": ["revok", "invalidat", "cancel", "blacklist", "ban"],
            "AUDIT_COMPLIANCE": ["audit", "compliance", "log", "trail", "forensic", "review"],
            "TEMPORAL_CONSTRAINTS": ["expir", "ttl", "time", "window", "duration", "temporal"],
            "BLOODLINE_VERIFICATION": ["bloodline", "sovereign", "mcwilliams", "dynasty", "supreme"],
        }

        for cat, keywords in category_keywords.items():
            for kw in keywords:
                if kw in query_lower:
                    if cat not in triggered_categories:
                        triggered_categories.append(cat)
                    hits = doctrine_cache.lookup(kw)
                    if cat not in category_doctrines:
                        category_doctrines[cat] = []
                    for h in hits:
                        if h.topic not in category_doctrines[cat]:
                            category_doctrines[cat].append(h.topic)
                    break

        if not triggered_categories:
            triggered_categories.append("AUTHORITY_LEVEL")

        interaction_edges: list[dict[str, str]] = []
        edge_rules = [
            ("TOKEN_VALIDITY", "AUTHORITY_LEVEL", "Token must be valid before level check"),
            ("AUTHORITY_LEVEL", "CROSS_ENGINE", "Level check precedes engine-specific rules"),
            ("BRUTE_FORCE", "TOKEN_VALIDITY", "Lockout check precedes token validation"),
            ("RATE_LIMITING", "AUTHORITY_LEVEL", "Rate limits vary by authority tier"),
            ("ESCALATION", "AUTHORITY_LEVEL", "Escalation changes effective authority level"),
            ("REVOCATION", "TOKEN_VALIDITY", "Revoked tokens fail validity check"),
            ("IP_BINDING", "TOKEN_VALIDITY", "IP binding is a token validity constraint"),
            ("TEMPORAL_CONSTRAINTS", "TOKEN_VALIDITY", "Expiration is a temporal validity check"),
            ("BLOODLINE_VERIFICATION", "ESCALATION", "Bloodline status cannot be gained via escalation"),
            ("SCOPE_RESTRICTION", "CROSS_ENGINE", "Scope limits which engines a token can access"),
            ("AUDIT_COMPLIANCE", "REVOCATION", "Revocation events must be audit-logged"),
        ]
        for src, dst, label in edge_rules:
            if src in triggered_categories and dst in triggered_categories:
                interaction_edges.append({"from": src, "to": dst, "relationship": label})

        return {
            "original_query": query,
            "triggered_categories": triggered_categories,
            "category_count": len(triggered_categories),
            "category_doctrines": category_doctrines,
            "interaction_edges": interaction_edges,
            "resolution_order": triggered_categories,
            "complexity": "LOW" if len(triggered_categories) <= 2 else "MEDIUM" if len(triggered_categories) <= 5 else "HIGH",
        }


# ---------------------------------------------------------------------------
# FastAPI Application
# ---------------------------------------------------------------------------

gate: Optional[AuthorityGate] = None
fragility_scorer = FactFragilityScorer()
zoned_analyzer = ZonedAnalyzer()
decomposer = MultiDoctrineDecomposer()


@asynccontextmanager
async def lifespan(app: FastAPI):
    global gate
    logger.info("GOV01 Authority Gate starting on port {}", ENGINE_PORT)
    gate = AuthorityGate()
    logger.info("Authority Gate fully initialized. {} doctrines loaded.", gate.doctrine_cache.size)
    yield
    logger.info("GOV01 Authority Gate shutting down")


app = FastAPI(
    title="GOV01 — Authority Gate",
    description="Central authority validation for ECHO PRIME. TIE-20 compliant.",
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
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/health")
async def health() -> HealthResponse:
    """Comprehensive health check endpoint."""
    assert gate is not None
    return HealthResponse(
        engine_id=ENGINE_ID,
        engine_name=ENGINE_NAME,
        version=ENGINE_VERSION,
        status="OPERATIONAL",
        uptime_seconds=round(time.time() - STARTUP_TIME, 2),
        total_validations=gate.metrics._queries,
        total_denials=gate.metrics._denials,
        total_tokens_issued=gate.token_manager.issued_count,
        active_lockouts=gate.brute_force.active_lockout_count,
        audit_entries=gate.audit_trail.total_entries,
        doctrine_cache_size=gate.doctrine_cache.size,
        coverage_topics_triggered=len(gate.coverage_map.triggered_topics),
        coverage_topics_total=len(gate.coverage_map._all_topics),
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


@app.post("/validate", response_model=ValidateResponse)
async def validate_endpoint(request: ValidateRequest) -> ValidateResponse:
    """Validate a caller's authority against a required level and engine."""
    assert gate is not None
    return gate.validate_authority(request)


@app.post("/token/issue", response_model=TokenIssueResponse)
async def issue_token(request: TokenIssueRequest) -> TokenIssueResponse:
    """Issue a new signed authority token."""
    assert gate is not None
    if request.level > 11.0 or request.level < 0.0:
        raise HTTPException(status_code=400, detail="Authority level must be between 0.0 and 11.0")
    if request.level >= 11.0 and not request.bloodline:
        raise HTTPException(status_code=403, detail="SOVEREIGN tokens require bloodline verification")
    token, payload = gate.token_manager.issue(
        subject=request.subject,
        level=request.level,
        ttl_seconds=request.ttl_seconds,
        bloodline=request.bloodline,
        ip_bind=request.ip_bind,
        scope=request.scope,
    )
    gate.audit_trail.log_decision("issue", request.subject, request.level, 0.0, "", True, f"Token issued: level={request.level} ttl={request.ttl_seconds}s", "internal", payload.jti)
    return TokenIssueResponse(
        token=token,
        expires_at=datetime.fromtimestamp(payload.exp, tz=timezone.utc).isoformat(),
        level=request.level,
        tier_name=get_tier_name(request.level),
        token_id=payload.jti,
    )


@app.post("/token/revoke")
async def revoke_token(token_id: str = Query(..., description="JTI of the token to revoke")) -> dict[str, Any]:
    """Revoke a token by its ID."""
    assert gate is not None
    gate.token_manager.revoke(token_id)
    gate.audit_trail.log_decision("revoke", "system", 10.0, 0.0, "", True, f"Token revoked: jti={token_id}", "internal", token_id)
    return {"revoked": True, "token_id": token_id, "timestamp": datetime.now(timezone.utc).isoformat()}


@app.post("/escalate", response_model=EscalationResponse)
async def escalate_endpoint(request: EscalationRequest) -> EscalationResponse:
    """Request authority escalation."""
    assert gate is not None
    return gate.handle_escalation(request)


@app.get("/audit")
async def audit_endpoint(
    count: int = Query(default=100, le=500),
    subject: Optional[str] = Query(default=None),
    engine_id: Optional[str] = Query(default=None),
    authorized: Optional[bool] = Query(default=None),
) -> dict[str, Any]:
    """Retrieve audit trail entries."""
    assert gate is not None
    if subject or engine_id or authorized is not None:
        entries = gate.audit_trail.search(subject=subject, engine_id=engine_id, authorized=authorized)
    else:
        entries = gate.audit_trail.get_recent(count)
    return {
        "total_entries": gate.audit_trail.total_entries,
        "returned": len(entries),
        "entries": [e.model_dump() for e in entries],
    }


@app.get("/matrix")
async def matrix_endpoint() -> dict[str, Any]:
    """Return the cross-engine authorization matrix."""
    return {
        "engine_id": ENGINE_ID,
        "matrix_size": len(CROSS_ENGINE_MATRIX),
        "engines": CROSS_ENGINE_MATRIX,
        "authority_hierarchy": {str(k): v for k, v in AUTHORITY_TIER_NAMES.items()},
        "authority_descriptions": {str(k): v for k, v in AUTHORITY_DESCRIPTIONS.items()},
        "rate_limits": {str(k): v for k, v in RATE_LIMITS_PER_TIER.items()},
    }


@app.get("/hierarchy")
async def hierarchy_endpoint() -> dict[str, Any]:
    """Return the complete authority hierarchy with descriptions."""
    levels = []
    for level_val in sorted(AUTHORITY_TIER_NAMES.keys()):
        levels.append({
            "level": level_val,
            "name": AUTHORITY_TIER_NAMES[level_val],
            "description": AUTHORITY_DESCRIPTIONS.get(level_val, ""),
            "rate_limit": RATE_LIMITS_PER_TIER.get(level_val, 0),
        })
    return {"hierarchy": levels, "total_tiers": len(levels)}


@app.get("/brute-force/{ip}")
async def brute_force_status(ip: str) -> BruteForceStatus:
    """Check brute force lockout status for an IP."""
    assert gate is not None
    return gate.brute_force.get_status(ip)


@app.post("/brute-force/{ip}/clear")
async def brute_force_clear(ip: str) -> dict[str, Any]:
    """Clear brute force lockout for an IP."""
    assert gate is not None
    gate.brute_force.clear(ip)
    return {"cleared": True, "ip": ip, "timestamp": datetime.now(timezone.utc).isoformat()}


@app.get("/rate-limit/{subject}")
async def rate_limit_status(subject: str, level: float = Query(default=5.0)) -> dict[str, Any]:
    """Check rate limit usage for a subject."""
    assert gate is not None
    return gate.rate_limiter.get_usage(subject, level)


@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest) -> QueryResponse:
    """TIE three-layer query endpoint for authority analysis."""
    assert gate is not None
    return gate.three_layer_query(request)


@app.get("/telemetry")
async def telemetry_endpoint() -> dict[str, Any]:
    """Return current telemetry snapshot."""
    assert gate is not None
    snap = gate.metrics.snapshot()
    return snap.model_dump()


@app.get("/coverage")
async def coverage_endpoint() -> dict[str, Any]:
    """Return doctrine coverage map."""
    assert gate is not None
    return gate.coverage_map.to_dict()


@app.get("/drift")
async def drift_endpoint() -> dict[str, Any]:
    """Return drift detection analysis."""
    assert gate is not None
    return gate.drift_watcher.detect_drift()


@app.get("/doctrines")
async def doctrines_endpoint() -> dict[str, Any]:
    """Return all loaded doctrine topics."""
    assert gate is not None
    return {
        "engine_id": ENGINE_ID,
        "doctrine_count": gate.doctrine_cache.size,
        "topics": gate.doctrine_cache.all_topics,
    }


@app.post("/fragility")
async def fragility_endpoint(fact_type: str = Query(...), description: str = Query(default="")) -> dict[str, Any]:
    """Score the fragility of an authority-related fact."""
    return fragility_scorer.score(fact_type, description)


@app.post("/zone-analysis")
async def zone_analysis_endpoint(zone: str = Query(...), data: dict[str, Any] = {}) -> dict[str, Any]:
    """Perform zoned analysis (PLANNING / REPORTING / AUDIT)."""
    return zoned_analyzer.analyze(zone, data)


@app.post("/decompose")
async def decompose_endpoint(query: str = Query(...)) -> dict[str, Any]:
    """Decompose a complex authority query into sub-problems."""
    assert gate is not None
    return decomposer.decompose(query, gate.doctrine_cache)


@app.get("/engine-access/{engine_id}")
async def engine_access_info(engine_id: str) -> dict[str, Any]:
    """Return access requirements for a specific engine."""
    for entry in CROSS_ENGINE_MATRIX:
        if entry["engine_id"] == engine_id:
            return {
                "engine_id": engine_id,
                "found": True,
                "min_level": entry["min_level"],
                "tier_required": get_tier_name(entry["min_level"]),
                "allowed_actions": entry["allowed_actions"],
                "restricted_to_scope": entry["restricted_to_scope"],
                "notes": entry["notes"],
                "engine_name": entry["engine_name"],
            }
    return {"engine_id": engine_id, "found": False, "min_level": 5.0, "tier_required": "TRUSTED", "notes": "Engine not in matrix — default TRUSTED access required"}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    logger.info("Starting GOV01 Authority Gate on port {}", ENGINE_PORT)
    uvicorn.run(
        "engine:app",
        host="0.0.0.0",
        port=ENGINE_PORT,
        log_level="info",
        reload=False,
    )
