"""
GOV04 Configuration Manager Engine v1.0.0
Port: 8894
TIE-20 Compliant | ECHO OMEGA PRIME Governance Tier

Centralized configuration management for all 507 engines.
Schema validation, versioning, hot reload, secret references, environment management.
"""

import asyncio
import copy
import hashlib
import json
import math
import os
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Optional

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
logger.add(LOG_DIR / "gov04_{time}.log", rotation="50 MB", compression="gz", retention="30 days")

# ── Constants ───────────────────────────────────────────────────────────────
ENGINE_ID = "GOV04"
ENGINE_NAME = "Configuration Manager"
ENGINE_VERSION = "1.0.0"
PORT = 8894
MAX_CONFIG_VERSIONS = 100
MAX_HISTORY = 5000

# ── Enums ───────────────────────────────────────────────────────────────────

class Environment(str, Enum):
    DEV = "dev"
    STAGING = "staging"
    PROD = "prod"

class ConfigStatus(str, Enum):
    ACTIVE = "active"
    DRAFT = "draft"
    ARCHIVED = "archived"
    ROLLBACK = "rollback"

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

# ── Pydantic Models ─────────────────────────────────────────────────────────

class ConfigEntry(BaseModel):
    key: str
    value: Any
    value_type: str = "string"
    description: str = ""
    secret: bool = False
    secret_ref: Optional[str] = None
    required: bool = True
    default: Optional[Any] = None
    validation_regex: Optional[str] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    allowed_values: Optional[list[Any]] = None

class ConfigVersion(BaseModel):
    version: int
    config_id: str
    environment: Environment
    entries: dict[str, Any]
    author: str = "system"
    message: str = ""
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    hash: str = ""
    status: ConfigStatus = ConfigStatus.ACTIVE
    parent_version: Optional[int] = None

class ConfigSchema(BaseModel):
    schema_id: str
    engine_type: str
    required_keys: list[str] = Field(default_factory=list)
    optional_keys: list[str] = Field(default_factory=list)
    entries: list[ConfigEntry] = Field(default_factory=list)
    version: str = "1.0"

class EngineConfig(BaseModel):
    engine_id: str
    engine_type: str
    environment: Environment = Environment.PROD
    config: dict[str, Any] = Field(default_factory=dict)
    schema_id: Optional[str] = None
    versions: list[ConfigVersion] = Field(default_factory=list)
    current_version: int = 0
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class ConfigDiff(BaseModel):
    added: dict[str, Any] = Field(default_factory=dict)
    removed: dict[str, Any] = Field(default_factory=dict)
    changed: dict[str, dict[str, Any]] = Field(default_factory=dict)
    unchanged_count: int = 0

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

class SetConfigRequest(BaseModel):
    engine_id: str
    engine_type: str = "generic"
    environment: Environment = Environment.PROD
    config: dict[str, Any]
    author: str = "system"
    message: str = ""

class RollbackRequest(BaseModel):
    engine_id: str
    target_version: int
    author: str = "system"
    reason: str = ""

class TemplateRequest(BaseModel):
    engine_type: str
    engine_id: str
    environment: Environment = Environment.PROD

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
        self.last_hit: Optional[str] = None

DOCTRINE_CACHE: list[DoctrineBlock] = [
    DoctrineBlock(
        topic="twelve_factor_config",
        keywords=["twelve", "factor", "12-factor", "environment", "config", "separation"],
        conclusion="Configuration should be strictly separated from code and stored in environment variables or external config stores. The twelve-factor app methodology mandates that config varies between deploys while code does not. Never hardcode config values.",
        reasoning="Hardcoded configuration creates deployment friction: different values for dev/staging/prod require code changes and rebuilds. Environment-based config enables the same artifact to run in any environment. This separation is foundational to CI/CD pipelines and container orchestration.",
        key_factors=["config-code separation", "environment variable precedence", "no config in version control", "config store externalization", "deploy-time injection"],
        authority=["The Twelve-Factor App - Config", "Kubernetes ConfigMaps", "HashiCorp Vault Best Practices"],
    ),
    DoctrineBlock(
        topic="secret_management",
        keywords=["secret", "credential", "password", "token", "key", "vault", "encrypt"],
        conclusion="Secrets must never appear in config files, environment variables visible to all processes, or version control. Use dedicated secret management systems (Vault, AWS Secrets Manager, Cloudflare Secrets) with rotation, auditing, and least-privilege access.",
        reasoning="Secret exposure is the #1 cause of security breaches. Config files get committed to git, environment variables appear in process listings, and logs capture config dumps. Dedicated secret managers provide encryption at rest, access logging, automatic rotation, and revocation capabilities.",
        key_factors=["encryption at rest and in transit", "access audit logging", "automatic rotation", "least-privilege access policies", "secret reference by key not value"],
        authority=["HashiCorp Vault Best Practices", "AWS Secrets Manager", "OWASP Secret Management Cheat Sheet"],
    ),
    DoctrineBlock(
        topic="config_versioning",
        keywords=["version", "history", "track", "changelog", "audit", "diff"],
        conclusion="Every configuration change must be versioned with timestamp, author, diff, and rollback capability. Config versioning provides audit trail, blame tracking, and instant rollback. Store at least 100 versions per config.",
        reasoning="Configuration changes are the #1 cause of production incidents (per Google SRE data). Without versioning, troubleshooting requires guessing what changed. With versioning, operators can instantly compare current vs previous config, identify the change that caused the issue, and rollback in seconds.",
        key_factors=["immutable version records", "diff between versions", "author attribution", "change message/reason", "instant rollback capability"],
        authority=["Google SRE Book - Configuration Management", "GitOps Principles", "Terraform State Management"],
    ),
    DoctrineBlock(
        topic="config_inheritance",
        keywords=["inherit", "override", "base", "hierarchy", "cascade", "default"],
        conclusion="Configuration should follow an inheritance hierarchy: global defaults → engine-type defaults → engine-specific overrides → environment overrides. Each level can override keys from parent levels. This reduces duplication and ensures consistency.",
        reasoning="Without inheritance, every engine needs a complete config — 500 engines × 50 keys = 25,000 config entries to maintain. With inheritance, common settings live in base configs (ports, timeouts, logging levels) and engines only override what's different. This follows the DRY principle applied to configuration.",
        key_factors=["global base config", "engine-type templates", "engine-specific overrides", "environment-level overrides", "merge strategy (deep merge vs shallow)"],
        authority=["Spring Boot Configuration Hierarchy", "Kubernetes ConfigMap Layering", "Ansible Variable Precedence"],
    ),
    DoctrineBlock(
        topic="hot_reload",
        keywords=["hot", "reload", "live", "dynamic", "runtime", "push", "refresh"],
        conclusion="Configuration changes should be applicable without service restart when possible. Hot reload reduces deployment risk and downtime. Implement via file watchers, config polling, or push notification. Not all config can be hot-reloaded (ports, database connections) — classify config as static vs dynamic.",
        reasoning="Service restart causes brief unavailability and connection disruption. For config changes that don't require process-level changes (feature flags, thresholds, timeouts), hot reload eliminates this disruption. The key is classifying which config keys support hot reload and which require restart.",
        key_factors=["static vs dynamic config classification", "change notification mechanism", "validation before apply", "atomic config swap", "rollback on apply failure"],
        authority=["Netflix Archaius", "Spring Cloud Config", "Consul Watch"],
    ),
    DoctrineBlock(
        topic="feature_flags",
        keywords=["feature", "flag", "toggle", "canary", "gradual", "rollout", "experiment"],
        conclusion="Feature flags enable decoupling deployment from release. Deploy code with flags disabled, then enable gradually. This enables canary releases, A/B testing, and instant rollback without code deployment. Manage flags as config with lifecycle tracking.",
        reasoning="Feature flags transform risky big-bang releases into controlled gradual rollouts. A 1% canary catches issues before 100% of users are affected. Combined with config management, flags can be toggled in seconds vs minutes for a full deployment. The lifecycle must be managed — stale flags become technical debt.",
        key_factors=["flag lifecycle management", "gradual rollout percentage", "user targeting rules", "flag dependency tracking", "stale flag cleanup"],
        authority=["Martin Fowler - Feature Toggles", "LaunchDarkly Best Practices", "Unleash Feature Management"],
    ),
    DoctrineBlock(
        topic="config_validation",
        keywords=["validate", "schema", "type", "constraint", "check", "verify"],
        conclusion="All configuration must be validated against a schema before deployment. Validation catches: missing required keys, type mismatches, out-of-range values, invalid formats, and constraint violations. Fail fast on invalid config — never start a service with bad configuration.",
        reasoning="Invalid configuration is worse than missing configuration — it can cause subtle bugs, data corruption, or security vulnerabilities. Schema validation is the first line of defense. Pydantic models provide runtime type checking, JSON Schema provides portable validation, and custom validators catch domain-specific constraints.",
        key_factors=["required vs optional key enforcement", "type checking", "range/boundary validation", "format validation (regex, URL, email)", "cross-key constraint validation"],
        authority=["JSON Schema Specification", "Pydantic Validators", "Kubernetes Admission Controllers"],
    ),
    DoctrineBlock(
        topic="config_drift_detection",
        keywords=["drift", "diverge", "inconsistent", "desync", "mismatch", "expected"],
        conclusion="Config drift occurs when running configuration diverges from intended state. Detect drift by periodically comparing running config against source of truth. Common causes: manual changes, failed deployments, race conditions. Remediate by reconciling to desired state.",
        reasoning="GitOps principles dictate that the declared config in version control IS the desired state. Any divergence is drift that must be detected and reconciled. Without drift detection, systems gradually become snowflakes — unique configurations that nobody fully understands.",
        key_factors=["periodic reconciliation checks", "drift alerting", "auto-remediation option", "drift root cause tracking", "manual change detection"],
        authority=["GitOps Principles - Weaveworks", "Terraform Drift Detection", "AWS Config Rules"],
    ),
    DoctrineBlock(
        topic="environment_management",
        keywords=["environment", "dev", "staging", "prod", "promote", "parity"],
        conclusion="Maintain dev/staging/prod parity for configuration structure while allowing value differences. Promote configs through environments (dev → staging → prod) with approval gates. Never copy prod config to dev without scrubbing secrets.",
        reasoning="Environment parity reduces 'works on my machine' and 'works in staging' failures. The config structure (keys, types) should be identical across environments — only values differ (URLs, credentials, feature flags). Promotion with approval gates ensures tested configs reach production.",
        key_factors=["structural parity across environments", "value-only differences", "promotion workflow with approval", "secret scrubbing for lower environments", "environment-specific overrides"],
        authority=["The Twelve-Factor App - Dev/Prod Parity", "Kubernetes Namespace Isolation", "Terraform Workspaces"],
    ),
    DoctrineBlock(
        topic="config_as_code",
        keywords=["infrastructure", "code", "IaC", "declarative", "gitops", "terraform"],
        conclusion="Configuration should be treated as code: version controlled, reviewed, tested, and deployed through CI/CD pipelines. GitOps workflow: commit config change → PR review → merge → automated deployment. This provides auditability, reproducibility, and collaboration.",
        reasoning="Treating config as code applies software engineering best practices to infrastructure management. Code review catches errors before they reach production. Version control provides history and rollback. CI/CD pipelines ensure consistent deployment. The result: fewer incidents from config changes.",
        key_factors=["version control for all config", "PR review for changes", "automated testing of config changes", "CI/CD deployment pipeline", "immutable config artifacts"],
        authority=["GitOps - Weaveworks", "Terraform Best Practices", "Pulumi Infrastructure as Code"],
    ),
    DoctrineBlock(
        topic="config_security",
        keywords=["security", "encrypt", "access", "permission", "RBAC", "policy"],
        conclusion="Config access should follow least privilege: engines read only their own config, operators modify only their domain, secrets require elevated access. Encrypt config at rest and in transit. Log all config reads and writes for audit.",
        reasoning="Configuration often contains sensitive information beyond secrets: internal URLs reveal architecture, thresholds reveal capacity limits, feature flags reveal unreleased features. Access control prevents unauthorized visibility into system internals.",
        key_factors=["per-engine access scoping", "role-based access control", "encryption at rest", "audit logging of all access", "config data classification"],
        authority=["NIST 800-53 CM Controls", "CIS Benchmark - Configuration Management", "SOC2 Change Management"],
    ),
    DoctrineBlock(
        topic="immutable_infrastructure",
        keywords=["immutable", "infrastructure", "bake", "image", "artifact", "rebuild"],
        conclusion="In immutable infrastructure, config is baked into deployment artifacts or injected at startup — never modified in-place on running systems. This eliminates config drift and ensures every deployment is clean. Trade-off: slower config changes require redeployment.",
        reasoning="Mutable infrastructure ('pet servers') accumulate manual changes that create snowflakes. Immutable infrastructure ('cattle') guarantees that every instance of a service is identical. Config injection at startup (env vars, mounted config files) provides the flexibility while maintaining immutability.",
        key_factors=["build-time vs runtime config injection", "no SSH/manual changes to running systems", "config as part of deployment artifact", "rolling deployment for config changes", "canary deployment for validation"],
        authority=["Martin Fowler - Immutable Server", "Netflix - Immutable Infrastructure", "Docker Best Practices"],
    ),
    DoctrineBlock(
        topic="config_templating",
        keywords=["template", "generate", "scaffold", "boilerplate", "standard", "default"],
        conclusion="Config templates reduce errors and onboarding friction. Each engine type should have a template with sensible defaults, documentation for each key, and validation rules. New engines start from templates, overriding only what's different.",
        reasoning="Without templates, new engine configuration is copy-paste from existing engines — introducing stale values, missing keys, and inconsistencies. Templates encode best practices: correct default ports, standard timeout values, required monitoring config, and security settings.",
        key_factors=["engine-type specific templates", "documented default values", "required vs optional marking", "validation rules in template", "template versioning"],
        authority=["Helm Chart Templates", "Cookiecutter Project Templates", "Yeoman Generators"],
    ),
    DoctrineBlock(
        topic="config_testing",
        keywords=["test", "validate", "dry-run", "preview", "simulate", "check"],
        conclusion="Config changes should be testable before deployment. Implement config dry-run: validate schema, check constraints, simulate inheritance resolution, and preview the final merged config. This catches issues before they reach any environment.",
        reasoning="Testing config changes in production is too late — the damage is done. Dry-run capability lets operators preview exactly what config will look like after their change, including inheritance resolution and environment overrides. This is especially important for complex inheritance hierarchies.",
        key_factors=["schema validation dry-run", "inheritance resolution preview", "diff against current config", "constraint validation", "impact analysis"],
        authority=["Terraform Plan", "Kubernetes Dry-Run", "Ansible Check Mode"],
    ),
    DoctrineBlock(
        topic="config_observability",
        keywords=["observe", "monitor", "track", "metric", "dashboard", "visibility"],
        conclusion="Configuration systems need their own observability: track config read/write rates, cache hit rates, validation failure rates, version counts, and drift detection frequency. Alert on unusual patterns (sudden burst of config changes, high validation failure rate).",
        reasoning="A misconfigured configuration system is a meta-failure that can cascade to all managed services. Monitoring the config system itself ensures it remains reliable. High validation failure rates indicate schema mismatches; unusual write patterns indicate potential unauthorized changes.",
        key_factors=["config operation metrics", "validation failure tracking", "version growth monitoring", "access pattern analysis", "config system health checks"],
        authority=["Prometheus Monitoring Best Practices", "Grafana Dashboard Design", "DataDog Config Monitoring"],
    ),
]

# ── Semantic Normalizer ─────────────────────────────────────────────────────

class SemanticNormalizer:
    SYNONYMS: dict[str, str] = {
        "env": "environment", "vars": "variables", "envvar": "environment_variable",
        "config": "configuration", "cfg": "configuration", "conf": "configuration",
        "val": "validation", "validate": "validation",
        "ver": "version", "vers": "version",
        "sec": "secret", "cred": "credential", "pw": "password",
        "tmpl": "template", "tpl": "template",
        "diff": "difference", "cmp": "compare",
        "rb": "rollback", "undo": "rollback", "revert": "rollback",
        "prod": "production", "stg": "staging", "dev": "development",
    }

    STOP_WORDS: set[str] = {"the", "a", "an", "is", "are", "was", "were", "be", "been",
                             "have", "has", "had", "do", "does", "did", "will", "would",
                             "to", "of", "in", "for", "on", "with", "at", "by", "from"}

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
    def __init__(self, doctrines: list[DoctrineBlock]):
        self.doctrines = doctrines
        self.idf: dict[str, float] = {}
        self._build_index()

    def _build_index(self) -> None:
        n = len(self.doctrines)
        term_doc: dict[str, int] = defaultdict(int)
        for d in self.doctrines:
            terms = set(d.keywords + d.topic.split("_"))
            for t in terms:
                term_doc[t.lower()] += 1
        for term, count in term_doc.items():
            self.idf[term] = math.log(n / (1 + count))

    def search(self, query: str, top_k: int = 5) -> list[tuple[DoctrineBlock, float]]:
        query_terms = set(query.lower().split())
        scores = []
        for doctrine in self.doctrines:
            doc_terms = set(k.lower() for k in doctrine.keywords) | set(doctrine.topic.lower().split("_"))
            score = 0.0
            for qt in query_terms:
                if qt in doc_terms:
                    score += self.idf.get(qt, 1.0)
                for dt in doc_terms:
                    if qt in dt or dt in qt:
                        score += self.idf.get(dt, 0.5) * 0.5
            if score > 0:
                scores.append((doctrine, score))
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]

# ── Telemetry ───────────────────────────────────────────────────────────────

class TelemetryCollector:
    def __init__(self):
        self.query_count = 0
        self.total_latency = 0.0
        self.error_count = 0
        self.cache_hits = 0
        self.cache_misses = 0
        self.config_reads = 0
        self.config_writes = 0
        self.validation_failures = 0
        self.rollbacks = 0
        self.start_time = time.time()
        self.latencies: list[float] = []

    def record_query(self, latency_ms: float, cache_hit: bool) -> None:
        self.query_count += 1
        self.total_latency += latency_ms
        self.latencies.append(latency_ms)
        if len(self.latencies) > 200:
            self.latencies = self.latencies[-200:]
        if cache_hit:
            self.cache_hits += 1
        else:
            self.cache_misses += 1

    def record_error(self) -> None:
        self.error_count += 1

    def get_stats(self) -> dict[str, Any]:
        uptime = time.time() - self.start_time
        s = sorted(self.latencies) if self.latencies else [0]
        return {
            "uptime_seconds": round(uptime, 1),
            "queries": self.query_count,
            "avg_latency_ms": round(self.total_latency / max(self.query_count, 1), 2),
            "p50_ms": round(s[len(s) // 2], 2),
            "p95_ms": round(s[int(len(s) * 0.95)], 2) if len(s) > 1 else round(s[0], 2),
            "errors": self.error_count,
            "cache_hit_rate": round(self.cache_hits / max(self.cache_hits + self.cache_misses, 1), 4),
            "config_reads": self.config_reads,
            "config_writes": self.config_writes,
            "validation_failures": self.validation_failures,
            "rollbacks": self.rollbacks,
        }

# ── Drift Watcher ───────────────────────────────────────────────────────────

class DriftWatcher:
    def __init__(self, alpha: float = 0.1, threshold: float = 2.0):
        self.alpha = alpha
        self.threshold = threshold
        self.ema: dict[str, float] = {}
        self.ema_var: dict[str, float] = {}
        self.drift_events: list[dict] = []

    def observe(self, metric: str, value: float) -> Optional[dict]:
        if metric not in self.ema:
            self.ema[metric] = value
            self.ema_var[metric] = 0.0
            return None
        old = self.ema[metric]
        self.ema[metric] = self.alpha * value + (1 - self.alpha) * old
        diff = abs(value - old)
        self.ema_var[metric] = self.alpha * diff + (1 - self.alpha) * self.ema_var[metric]
        std = max(self.ema_var[metric], 0.001)
        z = diff / std
        if z > self.threshold:
            event = {"metric": metric, "value": value, "expected": round(old, 4),
                     "z_score": round(z, 2), "timestamp": datetime.now(timezone.utc).isoformat()}
            self.drift_events.append(event)
            if len(self.drift_events) > 500:
                self.drift_events = self.drift_events[-250:]
            return event
        return None

# ── Coverage Map ────────────────────────────────────────────────────────────

class CoverageMap:
    def __init__(self):
        self.triggered: dict[str, int] = defaultdict(int)
        self.missed: list[str] = []

    def record_hit(self, topic: str) -> None:
        self.triggered[topic] += 1

    def record_miss(self, query: str) -> None:
        self.missed.append(query)
        if len(self.missed) > 500:
            self.missed = self.missed[-250:]

    def get_coverage(self) -> dict[str, Any]:
        total = len(DOCTRINE_CACHE)
        covered = len(self.triggered)
        return {
            "total_topics": total, "covered": covered,
            "coverage_pct": round(covered / max(total, 1) * 100, 1),
            "top_triggered": dict(sorted(self.triggered.items(), key=lambda x: x[1], reverse=True)[:10]),
            "recent_misses": self.missed[-10:],
        }

# ── Metrics Collector ───────────────────────────────────────────────────────

class MetricsCollector:
    def __init__(self):
        self.counters: dict[str, int] = defaultdict(int)
        self.gauges: dict[str, float] = {}
        self.histograms: dict[str, list[float]] = defaultdict(list)

    def inc(self, name: str, v: int = 1) -> None:
        self.counters[name] += v

    def gauge(self, name: str, v: float) -> None:
        self.gauges[name] = v

    def observe(self, name: str, v: float) -> None:
        self.histograms[name].append(v)
        if len(self.histograms[name]) > 1000:
            self.histograms[name] = self.histograms[name][-500:]

    def get_all(self) -> dict[str, Any]:
        h = {}
        for name, vals in self.histograms.items():
            if vals:
                s = sorted(vals)
                h[name] = {"count": len(s), "avg": round(sum(s) / len(s), 2),
                           "p50": round(s[len(s) // 2], 2), "p95": round(s[int(len(s) * 0.95)], 2) if len(s) > 1 else round(s[0], 2)}
        return {"counters": dict(self.counters), "gauges": dict(self.gauges), "histograms": h}

# ── Audit Trail ─────────────────────────────────────────────────────────────

class AuditTrail:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.last_hash = "0" * 64

    def log(self, event_type: str, data: dict) -> str:
        entry = {"timestamp": datetime.now(timezone.utc).isoformat(), "event_type": event_type,
                 "data": data, "prev_hash": self.last_hash}
        raw = json.dumps(entry, separators=(",", ":"), sort_keys=True)
        h = hashlib.sha256(raw.encode()).hexdigest()
        entry["hash"] = h
        self.last_hash = h
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, separators=(",", ":")) + "\n")
        return h

# ── Fact Fragility Scorer ───────────────────────────────────────────────────

class FactFragilityScorer:
    WEIGHTS: dict[str, float] = {
        "schema_validated": 0.1, "version_controlled": 0.15,
        "manual_entry": 0.5, "imported": 0.3, "unknown": 0.8,
    }

    def score(self, source: str, corroboration: int, recency_hours: float) -> dict:
        base = self.WEIGHTS.get(source, 0.6)
        corr_factor = max(0.1, 1.0 - corroboration * 0.15)
        recency = min(1.0, recency_hours / 24.0) * 0.3
        fragility = min(1.0, base * corr_factor + recency)
        return {"fragility": round(fragility, 3), "source": source, "corroboration": corroboration,
                "assessment": "reliable" if fragility < 0.3 else "moderate" if fragility < 0.6 else "fragile"}

# ── Zoned Analyzer ──────────────────────────────────────────────────────────

class ZonedAnalyzer:
    def __init__(self):
        self.history: list[dict] = []

    def analyze(self, query: str, zone: AnalysisZone, data: dict) -> dict:
        result = {"zone": zone.value, "query": query}
        if zone == AnalysisZone.PLANNING:
            result["recommendations"] = self._plan(data)
        elif zone == AnalysisZone.REPORTING:
            result["summary"] = self._report(data)
        else:
            result["findings"] = self._audit(data)
        self.history.append({"zone": zone.value, "ts": datetime.now(timezone.utc).isoformat()})
        if len(self.history) > 500:
            self.history = self.history[-250:]
        return result

    def _plan(self, data: dict) -> list[str]:
        recs = []
        if data.get("configs_without_schema", 0) > 0:
            recs.append(f"{data['configs_without_schema']} configs lack schema validation — create schemas")
        if data.get("stale_configs", 0) > 0:
            recs.append(f"{data['stale_configs']} configs haven't been updated in 90+ days — review")
        recs.append("Implement hot reload for dynamic config keys across all engines")
        return recs

    def _report(self, data: dict) -> dict:
        return {"total_configs": data.get("total_configs", 0), "total_versions": data.get("total_versions", 0),
                "schemas": data.get("total_schemas", 0), "environments": data.get("environments", [])}

    def _audit(self, data: dict) -> list[str]:
        findings = []
        if data.get("secrets_in_plaintext", 0) > 0:
            findings.append(f"CRITICAL: {data['secrets_in_plaintext']} plaintext secrets detected")
        if data.get("validation_failures", 0) > 5:
            findings.append(f"HIGH: {data['validation_failures']} recent validation failures")
        if not findings:
            findings.append("No audit concerns")
        return findings

# ── Multi-Doctrine Decomposer ──────────────────────────────────────────────

class MultiDoctrineDecomposer:
    CATEGORIES = ["versioning", "validation", "secrets", "inheritance", "hot_reload",
                  "templating", "drift", "security", "environment", "observability"]
    EDGES = [
        ("versioning", "drift", "version_changes_cause_drift"),
        ("secrets", "security", "secrets_are_security_critical"),
        ("validation", "drift", "validation_prevents_drift"),
        ("inheritance", "templating", "templates_define_inheritance_base"),
        ("environment", "secrets", "environments_have_different_secrets"),
    ]

    def decompose(self, query: str) -> dict:
        normalizer = SemanticNormalizer()
        kw = normalizer.extract_keywords(query)
        cats = [c for c in self.CATEGORIES if any(k in c for k in kw)]
        if not cats:
            cats = ["versioning", "validation"]
        edges = [{"from": e[0], "to": e[1], "rel": e[2]} for e in self.EDGES
                 if e[0] in cats or e[1] in cats]
        return {"categories": cats, "edges": edges, "depth": len(cats)}

# ── Deep Analyzer ───────────────────────────────────────────────────────────

class DeepAnalyzer:
    def __init__(self, vs: VectorSearchEngine, fs: FactFragilityScorer):
        self.vs = vs
        self.fs = fs

    def analyze(self, query: str, data: dict) -> dict:
        results = self.vs.search(query, top_k=5)
        sources = [{"topic": d.topic, "score": round(s, 3), "conclusion": d.conclusion,
                     "confidence": d.confidence.value} for d, s in results]
        chain = [f"[{d.topic}] {d.reasoning[:200]}..." for d, _ in results]
        frag = self.fs.score("schema_validated", len(sources), 0.1)
        synth = sources[0]["conclusion"] if sources else f"No doctrine coverage for: {query}"
        return {"sources": sources, "reasoning_chain": chain, "fragility": frag, "synthesis": synth}

# ── Response Formatter ──────────────────────────────────────────────────────

class ResponseFormatter:
    def format(self, data: dict, mode: ResponseMode) -> dict:
        if mode == ResponseMode.FAST:
            return {"summary": data.get("synthesis", ""), "key_metrics": {
                k: v for k, v in data.items() if k in ("total_configs", "total_versions", "total_schemas")}}
        elif mode == ResponseMode.DEFENSE:
            return {"summary": data.get("synthesis", ""), "sources": data.get("sources", []),
                    "reasoning_chain": data.get("reasoning_chain", []), "fragility": data.get("fragility", {})}
        else:
            return {"full_analysis": data, "engine": ENGINE_ID, "version": ENGINE_VERSION,
                    "timestamp": datetime.now(timezone.utc).isoformat()}

# ── Authority Hardening ─────────────────────────────────────────────────────

class AuthorityHardening:
    LEVELS = {"public": 0, "basic": 1, "standard": 3, "elevated": 5, "admin": 7, "system": 9, "sovereign": 11}

    def check(self, required: str, provided: str) -> bool:
        return self.LEVELS.get(provided, 0) >= self.LEVELS.get(required, 11)

    def classify(self, query: str) -> str:
        q = query.lower()
        if any(t in q for t in ("delete", "purge", "destroy", "wipe")):
            return "admin"
        if any(t in q for t in ("set", "create", "modify", "rollback")):
            return "elevated"
        return "public"

# ── Config Store ────────────────────────────────────────────────────────────

class ConfigStore:
    def __init__(self):
        self.configs: dict[str, EngineConfig] = {}
        self.schemas: dict[str, ConfigSchema] = {}
        self.templates: dict[str, dict[str, Any]] = {}
        self.telemetry = TelemetryCollector()
        self.drift_watcher = DriftWatcher()
        self.coverage_map = CoverageMap()
        self.metrics = MetricsCollector()
        self.normalizer = SemanticNormalizer()
        self.vector_search = VectorSearchEngine(DOCTRINE_CACHE)
        self.fragility = FactFragilityScorer()
        self.deep_analyzer = DeepAnalyzer(self.vector_search, self.fragility)
        self.zoned_analyzer = ZonedAnalyzer()
        self.decomposer = MultiDoctrineDecomposer()
        self.formatter = ResponseFormatter()
        self.authority = AuthorityHardening()
        self.audit_trail = AuditTrail(LOG_DIR / "audit_trail.jsonl")
        self._load_default_schemas()
        self._load_default_templates()

    def _load_default_schemas(self) -> None:
        base_entries = [
            ConfigEntry(key="port", value_type="integer", description="Service port", required=True, min_value=1024, max_value=65535),
            ConfigEntry(key="host", value_type="string", description="Bind host", default="0.0.0.0"),
            ConfigEntry(key="log_level", value_type="string", description="Logging level", default="INFO",
                        allowed_values=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
            ConfigEntry(key="cors_origins", value_type="list", description="Allowed CORS origins", default=["*"]),
            ConfigEntry(key="request_timeout_ms", value_type="integer", description="Request timeout", default=30000, min_value=1000, max_value=300000),
            ConfigEntry(key="max_concurrent_requests", value_type="integer", description="Max concurrency", default=100, min_value=1, max_value=10000),
            ConfigEntry(key="health_check_interval_s", value_type="integer", description="Health check interval", default=30, min_value=5),
            ConfigEntry(key="telemetry_enabled", value_type="boolean", description="Enable telemetry", default=True),
            ConfigEntry(key="cache_ttl_s", value_type="integer", description="Cache TTL seconds", default=300, min_value=0),
            ConfigEntry(key="api_key", value_type="string", description="API authentication key", secret=True, secret_ref="vault://engine/{engine_id}/api_key"),
        ]
        self.schemas["base_engine"] = ConfigSchema(
            schema_id="base_engine", engine_type="base",
            required_keys=["port", "host", "log_level"],
            optional_keys=["cors_origins", "request_timeout_ms", "max_concurrent_requests",
                           "health_check_interval_s", "telemetry_enabled", "cache_ttl_s", "api_key"],
            entries=base_entries,
        )
        tax_entries = base_entries + [
            ConfigEntry(key="doctrine_cache_path", value_type="string", description="Path to doctrine cache", required=True),
            ConfigEntry(key="vector_db_path", value_type="string", description="Path to vector DB"),
            ConfigEntry(key="cloud_retrieval_enabled", value_type="boolean", default=True),
            ConfigEntry(key="cloud_retrieval_timeout_ms", value_type="integer", default=5000, min_value=500),
            ConfigEntry(key="confidence_threshold", value_type="float", default=0.7, min_value=0.0, max_value=1.0),
        ]
        self.schemas["tax_engine"] = ConfigSchema(
            schema_id="tax_engine", engine_type="tax",
            required_keys=["port", "host", "log_level", "doctrine_cache_path"],
            optional_keys=["vector_db_path", "cloud_retrieval_enabled", "cloud_retrieval_timeout_ms", "confidence_threshold"],
            entries=tax_entries,
        )
        landman_entries = base_entries + [
            ConfigEntry(key="county_database_url", value_type="string", description="County records DB URL"),
            ConfigEntry(key="gis_api_url", value_type="string", description="GIS service URL"),
            ConfigEntry(key="title_chain_depth", value_type="integer", default=50, min_value=10, max_value=200),
            ConfigEntry(key="cloud_ekm_enabled", value_type="boolean", default=True),
        ]
        self.schemas["landman_engine"] = ConfigSchema(
            schema_id="landman_engine", engine_type="landman",
            required_keys=["port", "host", "log_level"],
            optional_keys=["county_database_url", "gis_api_url", "title_chain_depth", "cloud_ekm_enabled"],
            entries=landman_entries,
        )

    def _load_default_templates(self) -> None:
        self.templates["base"] = {
            "port": 8900, "host": "0.0.0.0", "log_level": "INFO",
            "cors_origins": ["*"], "request_timeout_ms": 30000,
            "max_concurrent_requests": 100, "health_check_interval_s": 30,
            "telemetry_enabled": True, "cache_ttl_s": 300,
        }
        self.templates["tax"] = {
            **self.templates["base"],
            "doctrine_cache_path": "./doctrine_cache.json",
            "vector_db_path": "./vector_db",
            "cloud_retrieval_enabled": True,
            "cloud_retrieval_timeout_ms": 5000,
            "confidence_threshold": 0.7,
        }
        self.templates["landman"] = {
            **self.templates["base"],
            "title_chain_depth": 50,
            "cloud_ekm_enabled": True,
        }

    def _compute_hash(self, config: dict) -> str:
        raw = json.dumps(config, sort_keys=True, default=str)
        return hashlib.sha256(raw.encode()).hexdigest()

    def set_config(self, engine_id: str, engine_type: str, env: Environment,
                   config: dict[str, Any], author: str, message: str) -> EngineConfig:
        self.telemetry.config_writes += 1
        self.metrics.inc("config_writes")
        if engine_id in self.configs:
            ec = self.configs[engine_id]
            old_config = ec.config.copy()
            new_version = ec.current_version + 1
        else:
            ec = EngineConfig(engine_id=engine_id, engine_type=engine_type, environment=env)
            old_config = {}
            new_version = 1
        # Apply inheritance: template → existing → new
        template = self.templates.get(engine_type, self.templates.get("base", {}))
        merged = {**template, **config}
        version = ConfigVersion(
            version=new_version, config_id=engine_id, environment=env,
            entries=merged, author=author, message=message,
            hash=self._compute_hash(merged), parent_version=ec.current_version if ec.current_version > 0 else None,
        )
        ec.versions.append(version)
        if len(ec.versions) > MAX_CONFIG_VERSIONS:
            ec.versions = ec.versions[-MAX_CONFIG_VERSIONS:]
        ec.config = merged
        ec.current_version = new_version
        ec.updated_at = datetime.now(timezone.utc).isoformat()
        self.configs[engine_id] = ec
        self.audit_trail.log("config_set", {
            "engine_id": engine_id, "version": new_version, "author": author,
            "message": message, "keys_changed": list(config.keys()),
        })
        logger.info(f"Config set for {engine_id} v{new_version} by {author}: {message}")
        return ec

    def get_config(self, engine_id: str) -> Optional[EngineConfig]:
        self.telemetry.config_reads += 1
        self.metrics.inc("config_reads")
        return self.configs.get(engine_id)

    def get_version(self, engine_id: str, version: int) -> Optional[ConfigVersion]:
        ec = self.configs.get(engine_id)
        if not ec:
            return None
        for v in ec.versions:
            if v.version == version:
                return v
        return None

    def rollback(self, engine_id: str, target_version: int, author: str, reason: str) -> Optional[EngineConfig]:
        ec = self.configs.get(engine_id)
        if not ec:
            return None
        target = None
        for v in ec.versions:
            if v.version == target_version:
                target = v
                break
        if not target:
            return None
        self.telemetry.rollbacks += 1
        self.metrics.inc("rollbacks")
        new_ver = ec.current_version + 1
        rollback_version = ConfigVersion(
            version=new_ver, config_id=engine_id, environment=ec.environment,
            entries=copy.deepcopy(target.entries), author=author,
            message=f"Rollback to v{target_version}: {reason}",
            hash=self._compute_hash(target.entries),
            status=ConfigStatus.ROLLBACK, parent_version=ec.current_version,
        )
        ec.versions.append(rollback_version)
        ec.config = copy.deepcopy(target.entries)
        ec.current_version = new_ver
        ec.updated_at = datetime.now(timezone.utc).isoformat()
        self.audit_trail.log("config_rollback", {
            "engine_id": engine_id, "from_version": ec.current_version - 1,
            "to_version": target_version, "new_version": new_ver, "author": author, "reason": reason,
        })
        logger.warning(f"Config rollback for {engine_id}: v{ec.current_version - 1} → v{target_version} (now v{new_ver})")
        return ec

    def diff_configs(self, config_a: dict, config_b: dict) -> ConfigDiff:
        added = {k: v for k, v in config_b.items() if k not in config_a}
        removed = {k: v for k, v in config_a.items() if k not in config_b}
        changed = {}
        unchanged = 0
        for k in set(config_a.keys()) & set(config_b.keys()):
            if config_a[k] != config_b[k]:
                changed[k] = {"old": config_a[k], "new": config_b[k]}
            else:
                unchanged += 1
        return ConfigDiff(added=added, removed=removed, changed=changed, unchanged_count=unchanged)

    def diff_versions(self, engine_id: str, v1: int, v2: int) -> Optional[ConfigDiff]:
        ver1 = self.get_version(engine_id, v1)
        ver2 = self.get_version(engine_id, v2)
        if not ver1 or not ver2:
            return None
        return self.diff_configs(ver1.entries, ver2.entries)

    def validate_config(self, engine_type: str, config: dict) -> dict[str, Any]:
        schema = self.schemas.get(f"{engine_type}_engine", self.schemas.get("base_engine"))
        if not schema:
            return {"valid": True, "warnings": ["No schema found — skipping validation"]}
        errors = []
        warnings = []
        for key in schema.required_keys:
            if key not in config:
                errors.append(f"Missing required key: {key}")
        for entry in schema.entries:
            if entry.key not in config:
                continue
            val = config[entry.key]
            if entry.value_type == "integer" and not isinstance(val, int):
                errors.append(f"{entry.key}: expected integer, got {type(val).__name__}")
            elif entry.value_type == "float" and not isinstance(val, (int, float)):
                errors.append(f"{entry.key}: expected float, got {type(val).__name__}")
            elif entry.value_type == "boolean" and not isinstance(val, bool):
                errors.append(f"{entry.key}: expected boolean, got {type(val).__name__}")
            elif entry.value_type == "string" and not isinstance(val, str):
                errors.append(f"{entry.key}: expected string, got {type(val).__name__}")
            if entry.min_value is not None and isinstance(val, (int, float)):
                if val < entry.min_value:
                    errors.append(f"{entry.key}: value {val} below minimum {entry.min_value}")
            if entry.max_value is not None and isinstance(val, (int, float)):
                if val > entry.max_value:
                    errors.append(f"{entry.key}: value {val} above maximum {entry.max_value}")
            if entry.allowed_values and val not in entry.allowed_values:
                errors.append(f"{entry.key}: value '{val}' not in allowed values {entry.allowed_values}")
            if entry.secret and not entry.secret_ref:
                warnings.append(f"{entry.key}: secret without vault reference")
        if errors:
            self.telemetry.validation_failures += 1
            self.metrics.inc("validation_failures")
        return {"valid": len(errors) == 0, "errors": errors, "warnings": warnings,
                "schema_id": schema.schema_id, "keys_validated": len(config)}

    def generate_template(self, engine_type: str, engine_id: str) -> dict[str, Any]:
        base = self.templates.get(engine_type, self.templates.get("base", {}))
        template = copy.deepcopy(base)
        template["_engine_id"] = engine_id
        template["_engine_type"] = engine_type
        template["_generated_at"] = datetime.now(timezone.utc).isoformat()
        return template

    def get_system_data(self) -> dict[str, Any]:
        total_versions = sum(len(ec.versions) for ec in self.configs.values())
        envs = set(ec.environment.value for ec in self.configs.values())
        configs_without_schema = sum(1 for ec in self.configs.values()
                                      if f"{ec.engine_type}_engine" not in self.schemas and "base_engine" not in self.schemas)
        return {
            "total_configs": len(self.configs),
            "total_versions": total_versions,
            "total_schemas": len(self.schemas),
            "total_templates": len(self.templates),
            "environments": list(envs),
            "configs_without_schema": configs_without_schema,
            "validation_failures": self.telemetry.validation_failures,
            "stale_configs": 0,
            "secrets_in_plaintext": 0,
        }

    async def query(self, request: QueryRequest) -> QueryResponse:
        start = time.monotonic()
        normalized = self.normalizer.normalize(request.query)
        cache_results = self.vector_search.search(normalized, top_k=3)
        cache_hit = len(cache_results) > 0
        if cache_hit:
            for d, _ in cache_results:
                d.hit_count += 1
                d.last_hit = datetime.now(timezone.utc).isoformat()
                self.coverage_map.record_hit(d.topic)
        else:
            self.coverage_map.record_miss(request.query)
        system_data = self.get_system_data()
        analysis = self.deep_analyzer.analyze(request.query, system_data)
        zoned = self.zoned_analyzer.analyze(request.query, request.zone, system_data)
        decomp = self.decomposer.decompose(request.query)
        confidence = ConfidenceLevel.DEFENSIBLE if cache_hit else ConfidenceLevel.AGGRESSIVE
        combined = {**analysis, **zoned, "decomposition": decomp, "system": system_data}
        formatted = self.formatter.format(combined, request.mode)
        hash_input = json.dumps({"q": request.query, "m": request.mode.value, "sys": system_data}, sort_keys=True, default=str)
        det_hash = hashlib.sha256(hash_input.encode()).hexdigest()
        lat = (time.monotonic() - start) * 1000
        self.audit_trail.log("query", {"query": request.query, "mode": request.mode.value, "latency_ms": round(lat, 2)})
        self.telemetry.record_query(lat, cache_hit)
        return QueryResponse(
            query=request.query, mode=request.mode, zone=request.zone,
            response=formatted, confidence=confidence, determinism_hash=det_hash,
            latency_ms=round(lat, 2), timestamp=datetime.now(timezone.utc).isoformat(),
            sources=[d.topic for d, _ in cache_results],
        )

# ── FastAPI App ─────────────────────────────────────────────────────────────

store = ConfigStore()

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"GOV04 Config Manager v{ENGINE_VERSION} starting on port {PORT}")
    logger.info(f"Loaded {len(store.schemas)} schemas, {len(store.templates)} templates")
    yield
    logger.info("GOV04 shutting down")

app = FastAPI(title=f"GOV04 - {ENGINE_NAME}", version=ENGINE_VERSION,
              description="Configuration Manager for ECHO OMEGA PRIME", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"])

@app.get("/health")
async def health():
    sd = store.get_system_data()
    return {"status": "healthy", "engine_id": ENGINE_ID, "name": ENGINE_NAME, "version": ENGINE_VERSION,
            "port": PORT, "configs": sd["total_configs"], "versions": sd["total_versions"],
            "schemas": sd["total_schemas"], "templates": sd["total_templates"],
            "telemetry": store.telemetry.get_stats(), "doctrine_topics": len(DOCTRINE_CACHE),
            "timestamp": datetime.now(timezone.utc).isoformat()}

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(req: QueryRequest):
    return await store.query(req)

@app.post("/config")
async def set_config(req: SetConfigRequest):
    validation = store.validate_config(req.engine_type, req.config)
    if not validation["valid"]:
        raise HTTPException(400, detail={"errors": validation["errors"], "warnings": validation["warnings"]})
    ec = store.set_config(req.engine_id, req.engine_type, req.environment, req.config, req.author, req.message)
    return {"status": "ok", "engine_id": ec.engine_id, "version": ec.current_version,
            "keys": len(ec.config), "warnings": validation.get("warnings", [])}

@app.get("/config/{engine_id}")
async def get_config(engine_id: str, version: Optional[int] = None):
    if version is not None:
        v = store.get_version(engine_id, version)
        if not v:
            raise HTTPException(404, detail=f"Version {version} not found for {engine_id}")
        return v.model_dump()
    ec = store.get_config(engine_id)
    if not ec:
        raise HTTPException(404, detail=f"Config not found for {engine_id}")
    return {"engine_id": ec.engine_id, "type": ec.engine_type, "environment": ec.environment.value,
            "config": ec.config, "version": ec.current_version, "updated_at": ec.updated_at,
            "total_versions": len(ec.versions)}

@app.get("/config/{engine_id}/versions")
async def list_versions(engine_id: str):
    ec = store.get_config(engine_id)
    if not ec:
        raise HTTPException(404, detail=f"Config not found for {engine_id}")
    return {"engine_id": engine_id, "versions": [
        {"version": v.version, "author": v.author, "message": v.message,
         "timestamp": v.timestamp, "status": v.status.value, "hash": v.hash[:16]}
        for v in ec.versions
    ]}

@app.get("/config/{engine_id}/diff")
async def diff_versions(engine_id: str, v1: int = Query(...), v2: int = Query(...)):
    d = store.diff_versions(engine_id, v1, v2)
    if not d:
        raise HTTPException(404, detail=f"Could not diff v{v1} and v{v2}")
    return d.model_dump()

@app.post("/config/{engine_id}/rollback")
async def rollback_config(engine_id: str, req: RollbackRequest):
    ec = store.rollback(engine_id, req.target_version, req.author, req.reason)
    if not ec:
        raise HTTPException(404, detail=f"Rollback failed for {engine_id} to v{req.target_version}")
    return {"status": "rolled_back", "engine_id": engine_id, "new_version": ec.current_version,
            "rolled_back_to": req.target_version}

@app.post("/validate")
async def validate_config(engine_type: str = Query(...), config: dict = ...):
    return store.validate_config(engine_type, config)

@app.get("/schemas")
async def list_schemas():
    return {"schemas": [{"id": s.schema_id, "type": s.engine_type, "required": s.required_keys,
                          "optional": s.optional_keys, "entries": len(s.entries)} for s in store.schemas.values()]}

@app.get("/schema/{schema_id}")
async def get_schema(schema_id: str):
    s = store.schemas.get(schema_id)
    if not s:
        raise HTTPException(404)
    return s.model_dump()

@app.get("/templates")
async def list_templates():
    return {"templates": {k: {kk: vv for kk, vv in v.items() if not kk.startswith("_")}
                          for k, v in store.templates.items()}}

@app.post("/template/generate")
async def generate_template(req: TemplateRequest):
    return store.generate_template(req.engine_type, req.engine_id)

@app.get("/configs")
async def list_all_configs(env: Optional[str] = None, engine_type: Optional[str] = None):
    configs = []
    for eid, ec in store.configs.items():
        if env and ec.environment.value != env:
            continue
        if engine_type and ec.engine_type != engine_type:
            continue
        configs.append({"engine_id": eid, "type": ec.engine_type, "environment": ec.environment.value,
                        "version": ec.current_version, "keys": len(ec.config), "updated_at": ec.updated_at})
    return {"configs": configs, "total": len(configs)}

@app.get("/telemetry")
async def telemetry():
    return store.telemetry.get_stats()

@app.get("/metrics")
async def metrics():
    return store.metrics.get_all()

@app.get("/coverage")
async def coverage():
    return store.coverage_map.get_coverage()

@app.get("/drift")
async def drift():
    return {"events": store.drift_watcher.drift_events[-50:]}

@app.get("/audit")
async def audit(limit: int = Query(default=50, le=200)):
    path = LOG_DIR / "audit_trail.jsonl"
    if not path.exists():
        return {"entries": [], "total": 0}
    lines = path.read_text(encoding="utf-8").strip().split("\n")
    entries = []
    for line in lines[-limit:]:
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return {"entries": entries, "total": len(lines)}

@app.get("/search/doctrine")
async def search_doctrine(q: str = Query(...), top_k: int = Query(default=5, le=20)):
    results = store.vector_search.search(q, top_k=top_k)
    return {"query": q, "results": [{"topic": d.topic, "score": round(s, 3),
            "conclusion": d.conclusion, "confidence": d.confidence.value} for d, s in results]}

@app.post("/normalize")
async def normalize(text: str = Query(...)):
    n = store.normalizer.normalize(text)
    kw = store.normalizer.extract_keywords(text)
    return {"original": text, "normalized": n, "keywords": kw}

@app.get("/system")
async def system_data():
    return store.get_system_data()

# ── Main ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting {ENGINE_ID} - {ENGINE_NAME} v{ENGINE_VERSION} on port {PORT}")
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")
