"""
BLD04 Emergency Override Engine v1.0.0
======================================
BLOODLINE tier engine for emergency override protocols, crisis management,
and break-glass procedures. Port 8884.

TIE-20 compliant: doctrine cache, semantic normalization, authority hardening,
confidence stratification, telemetry, drift watcher, coverage map, metrics,
zoned analysis, fact fragility scoring, audit trail, determinism hashing,
deep analysis mode, multi-doctrine decomposition.

Architecture:
    Three-layer response: Doctrine Cache (0-200ms) -> Semantic Retrieval -> Deep Analysis
    Response modes: FAST, DEFENSE, MEMO
    20+ doctrine blocks covering emergency override domain
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
from typing import Any, Dict, List, Optional, Tuple

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import BaseModel, Field

# ============================================================================
# PATH SETUP + CLOUD RETRIEVER IMPORT
# ============================================================================

ENGINE_DIR = Path(__file__).parent
ENGINES_DIR = ENGINE_DIR.parent
sys.path.insert(0, str(ENGINES_DIR / "_shared"))

from cloud_retriever import CognitionCloudRetriever, CloudKnowledge  # noqa: E402

# ============================================================================
# CONSTANTS
# ============================================================================

ENGINE_ID = "BLD04"
ENGINE_NAME = "Emergency Override"
ENGINE_TIER = "BLD"
ENGINE_VERSION = "1.0.0"
ENGINE_PORT = 8884
AUDIT_LOG_PATH = ENGINE_DIR / "audit_trail.jsonl"
DOCTRINE_CACHE_PATH = ENGINE_DIR / "doctrine_cache.json"
SEMANTIC_DICT_PATH = ENGINE_DIR / "semantic_dict.json"
COVERAGE_MAP_PATH = ENGINE_DIR / "coverage_map.json"

BANNED_PHRASES = [
    "i think", "probably", "maybe", "i believe", "it seems",
    "in my opinion", "arguably", "it could be", "perhaps",
    "i would say", "roughly speaking", "more or less",
]


# ============================================================================
# ENUMS
# ============================================================================

class ResponseMode(str, Enum):
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"


class ConfidenceStratification(str, Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"


class AnalysisZone(str, Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"


class LockdownLevel(str, Enum):
    NORMAL = "NORMAL"
    ELEVATED = "ELEVATED"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"
    LOCKDOWN = "LOCKDOWN"


class SeverityLevel(str, Enum):
    SEV1 = "SEV1"
    SEV2 = "SEV2"
    SEV3 = "SEV3"
    SEV4 = "SEV4"
    SEV5 = "SEV5"


class AuthorityLevel(float, Enum):
    OBSERVER = 1.0
    OPERATOR = 3.0
    ADMIN = 5.0
    ENGINEER = 7.0
    TIER_ADMIN = 9.0
    SOVEREIGN = 11.0


# ============================================================================
# PYDANTIC MODELS - REQUEST / RESPONSE
# ============================================================================

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=4000, description="The emergency override query")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response mode")
    zone: AnalysisZone = Field(default=AnalysisZone.PLANNING, description="Analysis zone")
    authority_level: float = Field(default=7.0, ge=1.0, le=11.0, description="Requester authority level")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")
    include_cloud: bool = Field(default=True, description="Include cloud knowledge retrieval")
    max_doctrines: int = Field(default=5, ge=1, le=20, description="Max doctrine blocks to return")


class DoctrineMatch(BaseModel):
    topic: str
    relevance_score: float
    conclusion: str
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    confidence: float
    confidence_stratification: ConfidenceStratification
    burden_holder: str
    adversary_position: str
    counter_arguments: List[str]
    resolution_strategy: str
    entity_scope: str


class FactFragilityScore(BaseModel):
    overall_fragility: float = Field(ge=0.0, le=1.0)
    verifiability: float = Field(ge=0.0, le=1.0)
    recharacterization_risk: float = Field(ge=0.0, le=1.0)
    testimony_dependence: float = Field(ge=0.0, le=1.0)
    authority_dependence: float = Field(ge=0.0, le=1.0)
    factors: List[str] = Field(default_factory=list)


class DriftIndicator(BaseModel):
    topic: str
    drift_detected: bool
    drift_magnitude: float = 0.0
    drift_direction: str = ""
    observation: str = ""


class DecomposedIssue(BaseModel):
    category: str
    sub_issues: List[str]
    doctrine_topics: List[str]
    interaction_edges: List[Tuple[str, str]]
    resolution_order: List[str]


class TelemetryTrace(BaseModel):
    trace_id: str
    engine_id: str = ENGINE_ID
    query_hash: str
    response_layer: str
    latency_ms: float
    doctrine_hits: int
    cloud_records: int
    timestamp: str
    zone: str
    mode: str
    authority_level: float


class QueryResponse(BaseModel):
    engine_id: str = ENGINE_ID
    engine_name: str = ENGINE_NAME
    version: str = ENGINE_VERSION
    trace_id: str
    query: str
    mode: ResponseMode
    zone: AnalysisZone
    response_layer: str
    answer: str
    doctrine_matches: List[DoctrineMatch] = Field(default_factory=list)
    fact_fragility: Optional[FactFragilityScore] = None
    drift_indicators: List[DriftIndicator] = Field(default_factory=list)
    decomposition: Optional[DecomposedIssue] = None
    cloud_knowledge_summary: str = ""
    citations: List[Dict[str, str]] = Field(default_factory=list)
    confidence: float = 0.0
    confidence_stratification: ConfidenceStratification = ConfidenceStratification.DEFENSIBLE
    determinism_hash: str = ""
    telemetry: TelemetryTrace
    disclosure_caveat: str = ""
    timestamp: str = ""


class HealthResponse(BaseModel):
    engine_id: str = ENGINE_ID
    engine_name: str = ENGINE_NAME
    version: str = ENGINE_VERSION
    tier: str = ENGINE_TIER
    port: int = ENGINE_PORT
    status: str = "operational"
    uptime_seconds: float = 0.0
    doctrine_count: int = 0
    normalization_rules: int = 0
    coverage_topics: int = 0
    queries_processed: int = 0
    avg_latency_ms: float = 0.0
    error_count: int = 0
    cloud_retriever_stats: Dict[str, Any] = Field(default_factory=dict)
    metrics: Dict[str, Any] = Field(default_factory=dict)
    timestamp: str = ""


# ============================================================================
# DOCTRINE BLOCK DATACLASS
# ============================================================================

class DoctrineBlock(BaseModel):
    topic: str
    keywords: List[str]
    conclusion_template: str
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    burden_holder: str = ""
    adversary_position: str = ""
    counter_arguments: List[str] = Field(default_factory=list)
    resolution_strategy: str = ""
    entity_scope: str = ""
    confidence: float = 0.95
    confidence_stratification: str = "DEFENSIBLE"
    controlling_precedent: str = ""


# ============================================================================
# SEMANTIC NORMALIZER
# ============================================================================

class SemanticNormalizer:
    """Normalizes emergency/crisis domain terms to canonical forms."""

    def __init__(self) -> None:
        self._rules: Dict[str, Dict[str, Any]] = {}
        self._alias_map: Dict[str, str] = {}
        self._load_rules()

    def _load_rules(self) -> None:
        if SEMANTIC_DICT_PATH.exists():
            with open(SEMANTIC_DICT_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            self._rules = data.get("normalization_rules", {})
        else:
            self._rules = self._default_rules()
        self._build_alias_map()

    def _default_rules(self) -> Dict[str, Dict[str, Any]]:
        return {
            "kill_switch": {"canonical": "kill_switch", "aliases": ["killswitch", "emergency stop", "e-stop", "panic button"]},
            "lockdown": {"canonical": "lockdown", "aliases": ["lock down", "security lockdown", "fortress mode"]},
            "severity_1": {"canonical": "SEV1", "aliases": ["sev 1", "catastrophic", "p1", "system down"]},
            "severity_2": {"canonical": "SEV2", "aliases": ["sev 2", "major", "p2"]},
            "escalation": {"canonical": "escalation", "aliases": ["escalate", "raise severity", "bump up"]},
            "containment": {"canonical": "containment", "aliases": ["contain", "isolate", "quarantine"]},
            "recovery": {"canonical": "recovery_procedure", "aliases": ["restore", "bring back", "resume"]},
            "snapshot": {"canonical": "state_snapshot", "aliases": ["system snapshot", "checkpoint", "save state"]},
            "sovereign": {"canonical": "SOVEREIGN", "aliases": ["supreme authority", "level 11", "god mode"]},
        }

    def _build_alias_map(self) -> None:
        self._alias_map.clear()
        for _key, rule in self._rules.items():
            canonical = rule.get("canonical", _key)
            for alias in rule.get("aliases", []):
                self._alias_map[alias.lower()] = canonical

    def normalize(self, text: str) -> str:
        normalized = text.lower()
        for alias, canonical in sorted(self._alias_map.items(), key=lambda x: -len(x[0])):
            if alias in normalized:
                normalized = normalized.replace(alias, canonical)
        return normalized

    def extract_terms(self, text: str) -> List[str]:
        found: List[str] = []
        lower = text.lower()
        for alias, canonical in self._alias_map.items():
            if alias in lower and canonical not in found:
                found.append(canonical)
        return found

    @property
    def rule_count(self) -> int:
        return len(self._rules)


# ============================================================================
# AUTHORITY HARDENING
# ============================================================================

class AuthorityHardener:
    """Enforces hierarchical authority levels with conflict resolution."""

    HIERARCHY: List[Dict[str, Any]] = [
        {"level": 11.0, "name": "SOVEREIGN", "weight": 1.0, "can_override": True, "can_delegate": True},
        {"level": 9.0, "name": "TIER_ADMIN", "weight": 0.85, "can_override": True, "can_delegate": True},
        {"level": 7.0, "name": "ENGINEER", "weight": 0.7, "can_override": False, "can_delegate": False},
        {"level": 5.0, "name": "ADMIN", "weight": 0.5, "can_override": False, "can_delegate": False},
        {"level": 3.0, "name": "OPERATOR", "weight": 0.3, "can_override": False, "can_delegate": False},
        {"level": 1.0, "name": "OBSERVER", "weight": 0.1, "can_override": False, "can_delegate": False},
    ]

    def validate_authority(self, requester_level: float, required_level: float) -> bool:
        return requester_level >= required_level

    def get_authority_weight(self, level: float) -> float:
        for h in self.HIERARCHY:
            if level >= h["level"]:
                return h["weight"]
        return 0.1

    def resolve_conflict(self, authorities: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not authorities:
            return {"resolved": False, "reason": "No authorities provided"}
        sorted_auth = sorted(authorities, key=lambda a: a.get("level", 0), reverse=True)
        winner = sorted_auth[0]
        return {
            "resolved": True,
            "winning_authority": winner,
            "reason": f"Authority level {winner.get('level')} supersedes lower levels",
            "all_authorities": sorted_auth,
        }

    def filter_doctrines_by_authority(self, doctrines: List[DoctrineBlock], requester_level: float) -> List[DoctrineBlock]:
        filtered: List[DoctrineBlock] = []
        for d in doctrines:
            required = 7.0
            if any(kw in d.topic for kw in ["sovereign", "kill_switch", "lockdown_full"]):
                required = 9.0
            if d.topic == "sovereign_override_authority":
                required = 11.0
            if requester_level >= required:
                filtered.append(d)
        return filtered


# ============================================================================
# DOCTRINE CACHE
# ============================================================================

class DoctrineCache:
    """In-memory doctrine cache with keyword matching. Loads from doctrine_cache.json."""

    def __init__(self) -> None:
        self._doctrines: List[DoctrineBlock] = []
        self._keyword_index: Dict[str, List[int]] = defaultdict(list)
        self._load()

    def _load(self) -> None:
        if DOCTRINE_CACHE_PATH.exists():
            with open(DOCTRINE_CACHE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            for item in data.get("doctrines", []):
                self._doctrines.append(DoctrineBlock(**item))
        if not self._doctrines:
            self._doctrines = self._build_default_doctrines()
        self._build_index()

    def _build_index(self) -> None:
        self._keyword_index.clear()
        for idx, d in enumerate(self._doctrines):
            for kw in d.keywords:
                self._keyword_index[kw.lower()].append(idx)
            self._keyword_index[d.topic.lower()].append(idx)

    def search(self, query: str, max_results: int = 5) -> List[Tuple[DoctrineBlock, float]]:
        query_lower = query.lower()
        scores: Dict[int, float] = defaultdict(float)
        query_words = set(query_lower.split())
        for word in query_words:
            for kw, indices in self._keyword_index.items():
                if word in kw or kw in word:
                    for idx in indices:
                        scores[idx] += 1.0
                elif any(w in kw for w in query_words):
                    for idx in indices:
                        scores[idx] += 0.5
        for idx, doc in enumerate(self._doctrines):
            topic_words = set(doc.topic.lower().replace("_", " ").split())
            overlap = query_words & topic_words
            if overlap:
                scores[idx] += len(overlap) * 2.0
            for kw in doc.keywords:
                if kw.lower() in query_lower:
                    scores[idx] += 3.0
        if not scores:
            return []
        max_score = max(scores.values()) if scores else 1.0
        results: List[Tuple[DoctrineBlock, float]] = []
        for idx, score in sorted(scores.items(), key=lambda x: x[1], reverse=True)[:max_results]:
            normalized_score = round(score / max_score, 3) if max_score > 0 else 0.0
            results.append((self._doctrines[idx], normalized_score))
        return results

    @property
    def count(self) -> int:
        return len(self._doctrines)

    @property
    def topics(self) -> List[str]:
        return [d.topic for d in self._doctrines]

    def _build_default_doctrines(self) -> List[DoctrineBlock]:
        """Fallback doctrines if JSON file is missing."""
        return [
            DoctrineBlock(
                topic="emergency_override_triggers",
                keywords=["override trigger", "emergency trigger", "activation criteria", "break glass", "trigger condition"],
                conclusion_template="Emergency overrides are triggered by predefined conditions including system compromise detection, cascading failures across 3+ engines, SOVEREIGN command, or automated anomaly correlation exceeding threshold. Each trigger maps to a specific response playbook with defined scope and authority requirements.",
                reasoning_framework="Trigger evaluation: (1) Identify trigger source (automated detection, manual report, SOVEREIGN command), (2) Validate trigger against false positive criteria, (3) Determine scope of override needed, (4) Map to appropriate playbook, (5) Verify authority level of initiator, (6) Execute override with full audit trail.",
                key_factors=["trigger_source", "false_positive_rate", "scope_determination", "authority_verification", "playbook_mapping"],
                primary_authority=["EMERGENCY_OVERRIDE_TRIGGER_MATRIX", "AUTOMATED_DETECTION_POLICY"],
                confidence=0.95,
                confidence_stratification="DEFENSIBLE",
            ),
            DoctrineBlock(
                topic="break_glass_procedures",
                keywords=["break glass", "emergency access", "bypass normal", "emergency procedure", "glass break"],
                conclusion_template="Break-glass procedures provide emergency access to restricted systems when normal authentication or authorization paths are unavailable. Access is time-bounded, fully audited, and automatically revoked. Requires post-event justification review within 24 hours.",
                reasoning_framework="Break-glass protocol: (1) Verify normal access path is genuinely unavailable, (2) Authenticate via secondary channel, (3) Grant time-limited access token, (4) Enable enhanced audit logging, (5) Set automatic revocation timer, (6) Require post-event justification report.",
                key_factors=["normal_path_unavailability", "secondary_authentication", "time_bound", "enhanced_audit", "justification_requirement"],
                primary_authority=["BREAK_GLASS_POLICY_v2", "EMERGENCY_ACCESS_STANDARD"],
                confidence=0.94,
                confidence_stratification="DEFENSIBLE",
            ),
        ]


# ============================================================================
# TELEMETRY
# ============================================================================

class TelemetryCollector:
    """Collects query traces, latency stats, and error domains."""

    def __init__(self) -> None:
        self._traces: List[Dict[str, Any]] = []
        self._latencies: List[float] = []
        self._error_count: int = 0
        self._query_count: int = 0
        self._layer_hits: Dict[str, int] = defaultdict(int)
        self._zone_counts: Dict[str, int] = defaultdict(int)
        self._mode_counts: Dict[str, int] = defaultdict(int)

    def record_trace(self, trace: TelemetryTrace) -> None:
        self._traces.append(trace.model_dump())
        self._latencies.append(trace.latency_ms)
        self._query_count += 1
        self._layer_hits[trace.response_layer] += 1
        self._zone_counts[trace.zone] += 1
        self._mode_counts[trace.mode] += 1
        if len(self._traces) > 1000:
            self._traces = self._traces[-500:]
            self._latencies = self._latencies[-500:]

    def record_error(self) -> None:
        self._error_count += 1

    @property
    def avg_latency(self) -> float:
        return round(sum(self._latencies) / len(self._latencies), 2) if self._latencies else 0.0

    @property
    def stats(self) -> Dict[str, Any]:
        return {
            "queries_processed": self._query_count,
            "avg_latency_ms": self.avg_latency,
            "error_count": self._error_count,
            "error_rate": round(self._error_count / max(self._query_count, 1), 4),
            "layer_hits": dict(self._layer_hits),
            "zone_distribution": dict(self._zone_counts),
            "mode_distribution": dict(self._mode_counts),
            "p50_latency": round(sorted(self._latencies)[len(self._latencies) // 2], 2) if self._latencies else 0.0,
            "p95_latency": round(sorted(self._latencies)[int(len(self._latencies) * 0.95)] if self._latencies else 0.0, 2),
        }


# ============================================================================
# DRIFT WATCHER
# ============================================================================

class DriftWatcher:
    """Detects doctrine drift over time by comparing query-response patterns."""

    def __init__(self) -> None:
        self._topic_confidence_history: Dict[str, List[float]] = defaultdict(list)
        self._topic_frequency: Dict[str, int] = defaultdict(int)
        self._drift_threshold: float = 0.15

    def record_observation(self, topic: str, confidence: float) -> None:
        self._topic_confidence_history[topic].append(confidence)
        self._topic_frequency[topic] += 1
        if len(self._topic_confidence_history[topic]) > 100:
            self._topic_confidence_history[topic] = self._topic_confidence_history[topic][-50:]

    def check_drift(self, topic: str) -> DriftIndicator:
        history = self._topic_confidence_history.get(topic, [])
        if len(history) < 5:
            return DriftIndicator(topic=topic, drift_detected=False, observation="Insufficient data for drift analysis")
        recent = history[-5:]
        early = history[:5]
        recent_avg = sum(recent) / len(recent)
        early_avg = sum(early) / len(early)
        delta = recent_avg - early_avg
        drifted = abs(delta) > self._drift_threshold
        direction = "increasing" if delta > 0 else "decreasing" if delta < 0 else "stable"
        return DriftIndicator(
            topic=topic,
            drift_detected=drifted,
            drift_magnitude=round(abs(delta), 4),
            drift_direction=direction,
            observation=f"Confidence moved from {early_avg:.3f} to {recent_avg:.3f} over {len(history)} observations",
        )

    def check_all(self) -> List[DriftIndicator]:
        return [self.check_drift(t) for t in self._topic_confidence_history]


# ============================================================================
# COVERAGE MAP
# ============================================================================

class CoverageMap:
    """Tracks triggered/missed doctrines and epistemic gap detection."""

    def __init__(self) -> None:
        self._triggered: Dict[str, int] = defaultdict(int)
        self._missed_queries: List[str] = []
        self._coverage_data: Dict[str, Any] = {}
        self._load()

    def _load(self) -> None:
        if COVERAGE_MAP_PATH.exists():
            with open(COVERAGE_MAP_PATH, "r", encoding="utf-8") as f:
                self._coverage_data = json.load(f)

    def record_hit(self, topic: str) -> None:
        self._triggered[topic] += 1

    def record_miss(self, query: str) -> None:
        self._missed_queries.append(query)
        if len(self._missed_queries) > 200:
            self._missed_queries = self._missed_queries[-100:]

    @property
    def coverage_ratio(self) -> float:
        total_topics = len(self._coverage_data.get("doctrine_coverage", []))
        triggered = len(self._triggered)
        return round(triggered / max(total_topics, 1), 3)

    @property
    def summary(self) -> Dict[str, Any]:
        return {
            "total_topics": len(self._coverage_data.get("doctrine_coverage", [])),
            "triggered_topics": len(self._triggered),
            "coverage_ratio": self.coverage_ratio,
            "top_triggered": sorted(self._triggered.items(), key=lambda x: x[1], reverse=True)[:10],
            "missed_query_count": len(self._missed_queries),
            "recent_misses": self._missed_queries[-5:],
            "epistemic_gaps": self._coverage_data.get("epistemic_gaps", []),
        }


# ============================================================================
# METRICS COLLECTOR
# ============================================================================

class MetricsCollector:
    """Collects latency stats, error rates, hit rates, queries/hour."""

    def __init__(self) -> None:
        self._start_time: float = time.monotonic()
        self._query_timestamps: List[float] = []
        self._doctrine_hit_count: int = 0
        self._cloud_hit_count: int = 0
        self._deep_analysis_count: int = 0
        self._total_queries: int = 0

    def record_query(self, doctrine_hits: int, cloud_hits: int, was_deep: bool) -> None:
        self._query_timestamps.append(time.monotonic())
        self._total_queries += 1
        self._doctrine_hit_count += doctrine_hits
        self._cloud_hit_count += cloud_hits
        if was_deep:
            self._deep_analysis_count += 1
        if len(self._query_timestamps) > 1000:
            self._query_timestamps = self._query_timestamps[-500:]

    @property
    def queries_per_hour(self) -> float:
        if not self._query_timestamps:
            return 0.0
        elapsed = time.monotonic() - self._start_time
        if elapsed < 1:
            return 0.0
        return round(self._total_queries / (elapsed / 3600), 2)

    @property
    def stats(self) -> Dict[str, Any]:
        return {
            "total_queries": self._total_queries,
            "queries_per_hour": self.queries_per_hour,
            "doctrine_hit_rate": round(self._doctrine_hit_count / max(self._total_queries, 1), 3),
            "cloud_hit_rate": round(self._cloud_hit_count / max(self._total_queries, 1), 3),
            "deep_analysis_rate": round(self._deep_analysis_count / max(self._total_queries, 1), 3),
            "uptime_seconds": round(time.monotonic() - self._start_time, 1),
        }


# ============================================================================
# AUDIT TRAIL
# ============================================================================

class AuditTrail:
    """Append-only JSONL audit trail for every query."""

    def __init__(self, path: Path = AUDIT_LOG_PATH) -> None:
        self._path = path
        self._path.parent.mkdir(parents=True, exist_ok=True)

    def log(self, trace_id: str, query: str, mode: str, zone: str, authority: float,
            doctrine_count: int, response_layer: str, confidence: float, determinism_hash: str) -> None:
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "engine_id": ENGINE_ID,
            "trace_id": trace_id,
            "query_hash": hashlib.sha256(query.encode()).hexdigest()[:16],
            "mode": mode,
            "zone": zone,
            "authority_level": authority,
            "doctrine_matches": doctrine_count,
            "response_layer": response_layer,
            "confidence": confidence,
            "determinism_hash": determinism_hash,
        }
        try:
            with open(self._path, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            logger.error(f"Audit trail write failed: {e}")


# ============================================================================
# FACT FRAGILITY SCORER
# ============================================================================

class FactFragilityScorer:
    """Scores the fragility of facts in emergency override context."""

    def score(self, doctrine_matches: List[DoctrineMatch], query: str) -> FactFragilityScore:
        if not doctrine_matches:
            return FactFragilityScore(
                overall_fragility=0.8, verifiability=0.3, recharacterization_risk=0.7,
                testimony_dependence=0.5, authority_dependence=0.8,
                factors=["No doctrine matches found; relying on general knowledge"],
            )
        avg_confidence = sum(d.confidence for d in doctrine_matches) / len(doctrine_matches)
        verifiability = avg_confidence
        authority_count = sum(len(d.primary_authority) for d in doctrine_matches)
        authority_dependence = min(1.0, authority_count / (len(doctrine_matches) * 3))
        has_adversary = sum(1 for d in doctrine_matches if d.adversary_position)
        recharacterization_risk = 1.0 - (has_adversary / max(len(doctrine_matches), 1))
        testimony_dependence = 0.3 if avg_confidence > 0.9 else 0.6
        overall = round(1.0 - (verifiability * 0.4 + (1.0 - recharacterization_risk) * 0.3 + (1.0 - testimony_dependence) * 0.3), 3)
        factors: List[str] = []
        if avg_confidence < 0.8:
            factors.append("Below-average doctrine confidence increases fragility")
        if authority_count < len(doctrine_matches) * 2:
            factors.append("Limited authority citations reduce verifiability")
        if recharacterization_risk > 0.5:
            factors.append("High recharacterization risk due to missing adversary positions")
        if not factors:
            factors.append("Strong doctrine backing with multiple authority citations")
        return FactFragilityScore(
            overall_fragility=overall,
            verifiability=round(verifiability, 3),
            recharacterization_risk=round(recharacterization_risk, 3),
            testimony_dependence=round(testimony_dependence, 3),
            authority_dependence=round(authority_dependence, 3),
            factors=factors,
        )


# ============================================================================
# MULTI-DOCTRINE DECOMPOSER
# ============================================================================

class MultiDoctrineDecomposer:
    """Decomposes complex queries into issue categories with interaction edges."""

    ISSUE_CATEGORIES = [
        "CONTAINMENT", "ESCALATION", "RECOVERY", "COMMUNICATION",
        "AUTHORITY", "DATA_PROTECTION", "MONITORING", "COMPLIANCE",
    ]

    def decompose(self, query: str, doctrine_matches: List[DoctrineMatch]) -> Optional[DecomposedIssue]:
        if len(doctrine_matches) < 2:
            return None
        topics = [d.topic for d in doctrine_matches]
        category = self._classify_category(query, topics)
        sub_issues = self._extract_sub_issues(query, doctrine_matches)
        edges = self._build_interaction_edges(topics)
        resolution_order = self._topological_sort(topics, edges)
        return DecomposedIssue(
            category=category,
            sub_issues=sub_issues,
            doctrine_topics=topics,
            interaction_edges=edges,
            resolution_order=resolution_order,
        )

    def _classify_category(self, query: str, topics: List[str]) -> str:
        q = query.lower()
        if any(w in q for w in ["contain", "isolat", "quarantin", "block"]):
            return "CONTAINMENT"
        if any(w in q for w in ["escalat", "severity", "raise", "elevat"]):
            return "ESCALATION"
        if any(w in q for w in ["recover", "restor", "bring back", "resume"]):
            return "RECOVERY"
        if any(w in q for w in ["notify", "alert", "communicat", "broadcast"]):
            return "COMMUNICATION"
        if any(w in q for w in ["authority", "privilege", "sovereign", "override"]):
            return "AUTHORITY"
        if any(w in q for w in ["data", "encrypt", "backup", "snapshot"]):
            return "DATA_PROTECTION"
        return "CONTAINMENT"

    def _extract_sub_issues(self, query: str, matches: List[DoctrineMatch]) -> List[str]:
        sub_issues: List[str] = []
        for m in matches:
            sub_issues.append(f"[{m.topic}] {m.resolution_strategy[:120]}")
        return sub_issues

    def _build_interaction_edges(self, topics: List[str]) -> List[Tuple[str, str]]:
        edges: List[Tuple[str, str]] = []
        dependency_map = {
            "full_system_kill_switch": ["system_state_snapshot", "data_protection_emergency"],
            "tier_level_shutdown": ["system_state_snapshot"],
            "lockdown_mode_escalation": ["incident_classification_severity"],
            "recovery_procedures": ["system_state_snapshot", "data_protection_emergency"],
            "emergency_communication_blast": ["incident_classification_severity"],
            "emergency_authority_elevation": ["sovereign_override_authority"],
            "automated_incident_response": ["incident_classification_severity", "system_state_snapshot"],
        }
        for src, deps in dependency_map.items():
            if src in topics:
                for dep in deps:
                    if dep in topics:
                        edges.append((dep, src))
        return edges

    def _topological_sort(self, topics: List[str], edges: List[Tuple[str, str]]) -> List[str]:
        in_degree: Dict[str, int] = {t: 0 for t in topics}
        graph: Dict[str, List[str]] = {t: [] for t in topics}
        for src, dst in edges:
            if src in graph and dst in in_degree:
                graph[src].append(dst)
                in_degree[dst] += 1
        queue = [t for t in topics if in_degree.get(t, 0) == 0]
        result: List[str] = []
        while queue:
            node = queue.pop(0)
            result.append(node)
            for neighbor in graph.get(node, []):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        for t in topics:
            if t not in result:
                result.append(t)
        return result


# ============================================================================
# ZONED ANALYSIS
# ============================================================================

class ZonedAnalyzer:
    """Ensures PLANNING / REPORTING / AUDIT zones never blur."""

    ZONE_TEMPLATES = {
        AnalysisZone.PLANNING: "PLANNING ANALYSIS: This assessment is forward-looking and should inform decision-making. {content}",
        AnalysisZone.REPORTING: "STATUS REPORT: This is a factual account of current state and recent actions. {content}",
        AnalysisZone.AUDIT: "AUDIT FINDING: This is a retrospective compliance assessment for the record. {content}",
    }

    ZONE_CAVEATS = {
        AnalysisZone.PLANNING: "This planning analysis is based on doctrine-backed emergency protocols. Actual execution may require real-time adjustment based on incident specifics.",
        AnalysisZone.REPORTING: "This report reflects system state at query time. Emergency conditions may have changed since this report was generated.",
        AnalysisZone.AUDIT: "This audit assessment is based on documented policies and procedures. Compliance verification requires review of actual execution logs.",
    }

    def apply_zone(self, content: str, zone: AnalysisZone) -> str:
        template = self.ZONE_TEMPLATES.get(zone, "{content}")
        return template.format(content=content)

    def get_caveat(self, zone: AnalysisZone) -> str:
        return self.ZONE_CAVEATS.get(zone, "")


# ============================================================================
# DEEP ANALYSIS MODE
# ============================================================================

class DeepAnalyzer:
    """Multi-source synthesis with full reasoning chain for complex queries."""

    def analyze(self, query: str, doctrine_matches: List[DoctrineMatch],
                cloud_knowledge: Optional[CloudKnowledge], zone: AnalysisZone) -> str:
        sections: List[str] = []
        sections.append(f"=== DEEP ANALYSIS: {query[:100]} ===\n")
        sections.append("1. DOCTRINE SYNTHESIS:")
        if doctrine_matches:
            for i, dm in enumerate(doctrine_matches, 1):
                sections.append(f"   {i}. [{dm.topic}] (confidence: {dm.confidence:.2f}, stratification: {dm.confidence_stratification})")
                sections.append(f"      Conclusion: {dm.conclusion[:200]}")
                sections.append(f"      Authority: {', '.join(dm.primary_authority[:3])}")
                if dm.adversary_position:
                    sections.append(f"      Counter-position: {dm.adversary_position[:150]}")
        else:
            sections.append("   No direct doctrine matches. Proceeding with general emergency framework.")
        if cloud_knowledge and cloud_knowledge.has_results:
            sections.append("\n2. CLOUD KNOWLEDGE INTEGRATION:")
            sections.append(f"   Sources queried: {', '.join(cloud_knowledge.sources_queried)}")
            sections.append(f"   Records retrieved: {cloud_knowledge.total_records}")
            if cloud_knowledge.clauses:
                sections.append(f"   Top EKM match: {cloud_knowledge.clauses[0].title}")
        else:
            sections.append("\n2. CLOUD KNOWLEDGE: Not available or no results.")
        sections.append("\n3. REASONING CHAIN:")
        if doctrine_matches:
            primary = doctrine_matches[0]
            sections.append(f"   Primary framework: {primary.reasoning_framework[:300]}")
            sections.append(f"   Key factors: {', '.join(primary.key_factors)}")
            sections.append(f"   Burden holder: {primary.burden_holder}")
            sections.append(f"   Resolution strategy: {primary.resolution_strategy}")
        sections.append("\n4. CROSS-DOCTRINE INTERACTIONS:")
        if len(doctrine_matches) > 1:
            for i in range(min(len(doctrine_matches) - 1, 3)):
                a, b = doctrine_matches[i], doctrine_matches[i + 1]
                sections.append(f"   [{a.topic}] <-> [{b.topic}]: Shared scope={a.entity_scope}")
        sections.append(f"\n5. ZONE APPLICATION: {zone.value}")
        sections.append(f"   This analysis is framed for {zone.value} purposes.")
        return "\n".join(sections)


# ============================================================================
# EPISTEMIC GUARDRAILS
# ============================================================================

def apply_epistemic_guardrails(text: str) -> str:
    """Remove banned hedging phrases that undermine authority."""
    result = text
    for phrase in BANNED_PHRASES:
        while phrase in result.lower():
            idx = result.lower().index(phrase)
            end_idx = idx + len(phrase)
            if end_idx < len(result) and result[end_idx] == " ":
                end_idx += 1
            result = result[:idx] + result[end_idx:]
    return result.strip()


def compute_determinism_hash(query: str, mode: str, zone: str, matches: List[str]) -> str:
    """SHA-256 hash for deterministic response verification."""
    payload = json.dumps({
        "engine": ENGINE_ID,
        "query": query,
        "mode": mode,
        "zone": zone,
        "doctrine_topics": sorted(matches),
    }, sort_keys=True)
    return hashlib.sha256(payload.encode()).hexdigest()


# ============================================================================
# CONFIDENCE STRATIFIER
# ============================================================================

def stratify_confidence(confidence: float, authority_count: int, has_adversary: bool) -> ConfidenceStratification:
    """Classify confidence level into stratification bands."""
    if confidence >= 0.9 and authority_count >= 2:
        return ConfidenceStratification.DEFENSIBLE
    if confidence >= 0.75 and authority_count >= 1:
        return ConfidenceStratification.AGGRESSIVE
    if confidence >= 0.5 or has_adversary:
        return ConfidenceStratification.DISCLOSURE
    return ConfidenceStratification.HIGH_RISK


# ============================================================================
# THREE-LAYER RESPONSE ENGINE
# ============================================================================

class ThreeLayerEngine:
    """
    Core response engine implementing doctrine cache -> semantic retrieval -> deep analysis.

    Layer 1: Doctrine Cache (0-200ms) - Direct keyword match against in-memory doctrines
    Layer 2: Semantic Retrieval - Cloud knowledge via CognitionCloudRetriever
    Layer 3: Deep Analysis - Multi-source synthesis for complex/ambiguous queries
    """

    def __init__(self) -> None:
        self.doctrine_cache = DoctrineCache()
        self.normalizer = SemanticNormalizer()
        self.authority_hardener = AuthorityHardener()
        self.telemetry = TelemetryCollector()
        self.drift_watcher = DriftWatcher()
        self.coverage_map = CoverageMap()
        self.metrics = MetricsCollector()
        self.audit_trail = AuditTrail()
        self.fragility_scorer = FactFragilityScorer()
        self.decomposer = MultiDoctrineDecomposer()
        self.zoned_analyzer = ZonedAnalyzer()
        self.deep_analyzer = DeepAnalyzer()
        self.cloud_retriever = CognitionCloudRetriever()
        self._start_time = time.monotonic()

    async def process_query(self, request: QueryRequest) -> QueryResponse:
        trace_id = str(uuid.uuid4())[:12]
        start = time.monotonic()
        normalized_query = self.normalizer.normalize(request.query)
        doctrine_results = self.doctrine_cache.search(normalized_query, max_results=request.max_doctrines)
        filtered_doctrines: List[DoctrineBlock] = []
        if doctrine_results:
            blocks = [d for d, _ in doctrine_results]
            filtered_doctrines = self.authority_hardener.filter_doctrines_by_authority(blocks, request.authority_level)
        doctrine_matches: List[DoctrineMatch] = []
        for block in filtered_doctrines:
            relevance = next((s for d, s in doctrine_results if d.topic == block.topic), 0.0)
            doctrine_matches.append(DoctrineMatch(
                topic=block.topic,
                relevance_score=relevance,
                conclusion=block.conclusion_template,
                reasoning_framework=block.reasoning_framework,
                key_factors=block.key_factors,
                primary_authority=block.primary_authority,
                confidence=block.confidence,
                confidence_stratification=ConfidenceStratification(block.confidence_stratification),
                burden_holder=block.burden_holder,
                adversary_position=block.adversary_position,
                counter_arguments=block.counter_arguments,
                resolution_strategy=block.resolution_strategy,
                entity_scope=block.entity_scope,
            ))
        cloud_knowledge: Optional[CloudKnowledge] = None
        response_layer = "doctrine_cache"
        if doctrine_matches:
            for dm in doctrine_matches:
                self.coverage_map.record_hit(dm.topic)
                self.drift_watcher.record_observation(dm.topic, dm.confidence)
        if not doctrine_matches or request.mode == ResponseMode.MEMO:
            if request.include_cloud:
                try:
                    cloud_knowledge = await self.cloud_retriever.retrieve_all(
                        normalized_query, category="emergency_override",
                    )
                    if cloud_knowledge and cloud_knowledge.has_results:
                        response_layer = "semantic_retrieval" if doctrine_matches else "semantic_retrieval_primary"
                except Exception as e:
                    logger.warning(f"Cloud retrieval failed: {e}")
        if (not doctrine_matches and (not cloud_knowledge or not cloud_knowledge.has_results)) or request.mode == ResponseMode.MEMO:
            response_layer = "deep_analysis"
        if not doctrine_matches and not (cloud_knowledge and cloud_knowledge.has_results):
            self.coverage_map.record_miss(request.query)
        answer = self._build_answer(request, doctrine_matches, cloud_knowledge, response_layer)
        answer = apply_epistemic_guardrails(answer)
        answer = self.zoned_analyzer.apply_zone(answer, request.zone)
        avg_confidence = sum(d.confidence for d in doctrine_matches) / len(doctrine_matches) if doctrine_matches else 0.5
        authority_count = sum(len(d.primary_authority) for d in doctrine_matches)
        has_adversary = any(d.adversary_position for d in doctrine_matches)
        strat = stratify_confidence(avg_confidence, authority_count, has_adversary)
        determinism_hash = compute_determinism_hash(
            request.query, request.mode.value, request.zone.value,
            [d.topic for d in doctrine_matches],
        )
        fragility = self.fragility_scorer.score(doctrine_matches, request.query) if request.mode != ResponseMode.FAST else None
        drift_indicators = [self.drift_watcher.check_drift(d.topic) for d in doctrine_matches] if request.mode == ResponseMode.DEFENSE else []
        decomposition = self.decomposer.decompose(request.query, doctrine_matches) if request.mode != ResponseMode.FAST else None
        latency_ms = round((time.monotonic() - start) * 1000, 2)
        trace = TelemetryTrace(
            trace_id=trace_id,
            query_hash=hashlib.sha256(request.query.encode()).hexdigest()[:16],
            response_layer=response_layer,
            latency_ms=latency_ms,
            doctrine_hits=len(doctrine_matches),
            cloud_records=cloud_knowledge.total_records if cloud_knowledge else 0,
            timestamp=datetime.now(timezone.utc).isoformat(),
            zone=request.zone.value,
            mode=request.mode.value,
            authority_level=request.authority_level,
        )
        self.telemetry.record_trace(trace)
        self.metrics.record_query(
            doctrine_hits=len(doctrine_matches),
            cloud_hits=cloud_knowledge.total_records if cloud_knowledge else 0,
            was_deep=response_layer == "deep_analysis",
        )
        self.audit_trail.log(
            trace_id=trace_id, query=request.query, mode=request.mode.value,
            zone=request.zone.value, authority=request.authority_level,
            doctrine_count=len(doctrine_matches), response_layer=response_layer,
            confidence=avg_confidence, determinism_hash=determinism_hash,
        )
        caveat = self.zoned_analyzer.get_caveat(request.zone)
        return QueryResponse(
            trace_id=trace_id,
            query=request.query,
            mode=request.mode,
            zone=request.zone,
            response_layer=response_layer,
            answer=answer,
            doctrine_matches=doctrine_matches,
            fact_fragility=fragility,
            drift_indicators=drift_indicators,
            decomposition=decomposition,
            cloud_knowledge_summary=cloud_knowledge.merged_text(2000) if cloud_knowledge else "",
            citations=cloud_knowledge.citation_list() if cloud_knowledge else [],
            confidence=round(avg_confidence, 3),
            confidence_stratification=strat,
            determinism_hash=determinism_hash,
            telemetry=trace,
            disclosure_caveat=caveat,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

    def _build_answer(self, request: QueryRequest, doctrine_matches: List[DoctrineMatch],
                      cloud_knowledge: Optional[CloudKnowledge], response_layer: str) -> str:
        if response_layer == "deep_analysis" or request.mode == ResponseMode.MEMO:
            return self.deep_analyzer.analyze(request.query, doctrine_matches, cloud_knowledge, request.zone)
        if request.mode == ResponseMode.FAST:
            return self._build_fast_answer(doctrine_matches, cloud_knowledge)
        return self._build_defense_answer(doctrine_matches, cloud_knowledge, request)

    def _build_fast_answer(self, matches: List[DoctrineMatch], cloud: Optional[CloudKnowledge]) -> str:
        parts: List[str] = []
        if matches:
            primary = matches[0]
            parts.append(primary.conclusion)
            if len(matches) > 1:
                parts.append(f"\nRelated: {', '.join(m.topic for m in matches[1:3])}")
        elif cloud and cloud.has_results:
            parts.append(cloud.merged_text(1000))
        else:
            parts.append("No matching emergency override doctrine found. Recommend consulting SOVEREIGN authority for guidance on this scenario.")
        return "\n".join(parts)

    def _build_defense_answer(self, matches: List[DoctrineMatch], cloud: Optional[CloudKnowledge],
                              request: QueryRequest) -> str:
        sections: List[str] = []
        sections.append(f"DEFENSE MODE ANALYSIS | Authority: {request.authority_level} | Zone: {request.zone.value}\n")
        if matches:
            for i, m in enumerate(matches, 1):
                sections.append(f"--- Doctrine {i}: {m.topic} (confidence: {m.confidence:.2f}, {m.confidence_stratification.value}) ---")
                sections.append(f"Conclusion: {m.conclusion}")
                sections.append(f"Authority: {', '.join(m.primary_authority)}")
                sections.append(f"Key factors: {', '.join(m.key_factors)}")
                sections.append(f"Burden: {m.burden_holder}")
                if m.adversary_position:
                    sections.append(f"Adversary position: {m.adversary_position}")
                sections.append(f"Resolution: {m.resolution_strategy}")
                sections.append("")
        if cloud and cloud.has_results:
            sections.append("--- Cloud Knowledge ---")
            sections.append(cloud.merged_text(1500))
        return "\n".join(sections)

    @property
    def health_data(self) -> Dict[str, Any]:
        return {
            "doctrine_count": self.doctrine_cache.count,
            "normalization_rules": self.normalizer.rule_count,
            "coverage": self.coverage_map.summary,
            "telemetry": self.telemetry.stats,
            "metrics": self.metrics.stats,
            "cloud_retriever": self.cloud_retriever.stats,
            "drift_warnings": [d.model_dump() for d in self.drift_watcher.check_all() if d.drift_detected],
        }


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

engine: Optional[ThreeLayerEngine] = None
app_start_time: float = 0.0


@asynccontextmanager
async def lifespan(app: FastAPI):
    global engine, app_start_time
    logger.info(f"Starting {ENGINE_NAME} engine v{ENGINE_VERSION} on port {ENGINE_PORT}")
    engine = ThreeLayerEngine()
    app_start_time = time.monotonic()
    logger.info(f"Loaded {engine.doctrine_cache.count} doctrines, {engine.normalizer.rule_count} normalization rules")
    yield
    if engine and engine.cloud_retriever:
        await engine.cloud_retriever.close()
    logger.info(f"{ENGINE_NAME} engine shut down")


app = FastAPI(
    title=f"{ENGINE_ID} {ENGINE_NAME}",
    description="BLOODLINE tier engine for emergency override protocols, crisis management, and break-glass procedures.",
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


@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Comprehensive health check endpoint."""
    assert engine is not None
    data = engine.health_data
    uptime = round(time.monotonic() - app_start_time, 1)
    return HealthResponse(
        status="operational",
        uptime_seconds=uptime,
        doctrine_count=data["doctrine_count"],
        normalization_rules=data["normalization_rules"],
        coverage_topics=data["coverage"]["total_topics"],
        queries_processed=data["telemetry"]["queries_processed"],
        avg_latency_ms=data["telemetry"]["avg_latency_ms"],
        error_count=data["telemetry"]["error_count"],
        cloud_retriever_stats=data["cloud_retriever"],
        metrics=data["metrics"],
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest) -> QueryResponse:
    """
    Primary query endpoint with three-layer response.

    Layer 1: Doctrine cache (0-200ms) - keyword match against 20+ emergency doctrine blocks
    Layer 2: Semantic retrieval - cloud knowledge via Cognition Cloud
    Layer 3: Deep analysis - multi-source synthesis for complex queries
    """
    assert engine is not None
    try:
        return await engine.process_query(request)
    except Exception as e:
        engine.telemetry.record_error()
        logger.error(f"Query processing failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/doctrines")
async def list_doctrines() -> Dict[str, Any]:
    """List all available doctrine topics."""
    assert engine is not None
    return {
        "engine_id": ENGINE_ID,
        "doctrine_count": engine.doctrine_cache.count,
        "topics": engine.doctrine_cache.topics,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/coverage")
async def get_coverage() -> Dict[str, Any]:
    """Get doctrine coverage map."""
    assert engine is not None
    return {
        "engine_id": ENGINE_ID,
        **engine.coverage_map.summary,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/metrics")
async def get_metrics() -> Dict[str, Any]:
    """Get engine performance metrics."""
    assert engine is not None
    return {
        "engine_id": ENGINE_ID,
        "telemetry": engine.telemetry.stats,
        "metrics": engine.metrics.stats,
        "cloud_retriever": engine.cloud_retriever.stats,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/drift")
async def get_drift() -> Dict[str, Any]:
    """Get doctrine drift analysis."""
    assert engine is not None
    all_drift = engine.drift_watcher.check_all()
    return {
        "engine_id": ENGINE_ID,
        "total_topics_tracked": len(all_drift),
        "drift_detected": [d.model_dump() for d in all_drift if d.drift_detected],
        "stable": [d.model_dump() for d in all_drift if not d.drift_detected],
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/normalize")
async def normalize_text(text: str) -> Dict[str, Any]:
    """Normalize emergency domain terms to canonical forms."""
    assert engine is not None
    return {
        "engine_id": ENGINE_ID,
        "original": text,
        "normalized": engine.normalizer.normalize(text),
        "extracted_terms": engine.normalizer.extract_terms(text),
    }


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    logger.add(
        ENGINE_DIR / "engine.log",
        rotation="50 MB",
        retention="7 days",
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    )
    uvicorn.run(
        "engine:app",
        host="0.0.0.0",
        port=ENGINE_PORT,
        log_level="info",
        reload=False,
    )
