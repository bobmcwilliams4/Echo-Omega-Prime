"""
BLD01 — Bloodline Authenticator Engine
=======================================
TIER: BLD (Bloodline) | MODE: DET | AUTH: 11.0 SOVEREIGN | PORT: 8893

Supreme authentication for the McWilliams Bloodline. Verifies SOVEREIGN (11.0) identity.
Multi-factor verification (knowledge/biometric/behavioral patterns). Session management
for Commander. Delegation of authority. Bloodline chain verification. Emergency lockout
and recovery. Dead man's switch. Authentication ceremony for highest-privilege operations.

TIE-20 Compliant: All 20 mandatory components implemented.
"""

from __future__ import annotations

import asyncio
import hashlib
import hmac
import json
import os
import secrets
import sys
import time
import uuid
from collections import defaultdict
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from enum import Enum, IntEnum
from pathlib import Path
from typing import Any, Optional

import uvicorn
from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field, field_validator

# ─────────────────────────────────────────────────────────────────────────────
# PATH SETUP
# ─────────────────────────────────────────────────────────────────────────────
ENGINE_DIR = Path(__file__).parent
ENGINES_DIR = ENGINE_DIR.parent
sys.path.insert(0, str(ENGINES_DIR))

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────
ENGINE_ID = "BLD01"
ENGINE_NAME = "Bloodline Authenticator"
ENGINE_VERSION = "1.0.0"
ENGINE_TIER = "BLD"
ENGINE_MODE = "DET"
ENGINE_PORT = 8893
AUTHORITY_LEVEL = 11.0

SOVEREIGN_LEVEL = 11.0
HEIR_MAX_LEVEL = 9.5
DELEGATE_MAX_LEVEL = 8.0
OPERATOR_MAX_LEVEL = 5.0
GUEST_MAX_LEVEL = 2.0

SESSION_TTL_SECONDS = 86400  # 24 hours
MAX_CONCURRENT_SESSIONS = 5
CEREMONY_TIMEOUT_SECONDS = 300  # 5 minutes for ceremony completion
DEAD_MAN_SWITCH_DEFAULT_HOURS = 72
LOCKOUT_RECOVERY_WINDOW_HOURS = 24
MAX_AUTH_ATTEMPTS = 5
AUTH_LOCKOUT_DURATION_SECONDS = 900  # 15 min lockout after max attempts
TOKEN_LENGTH = 64
CHALLENGE_EXPIRY_SECONDS = 120

HMAC_KEY = os.environ.get("BLD01_HMAC_KEY", "bld01-bloodline-hmac-key-sovereign-auth")
PEPPER = os.environ.get("BLD01_PEPPER", "mcwilliams-dynasty-pepper-2026")

AUDIT_LOG_PATH = ENGINE_DIR / "audit_trail.jsonl"
DOCTRINE_CACHE_PATH = ENGINE_DIR / "doctrine_cache.json"
SEMANTIC_DICT_PATH = ENGINE_DIR / "semantic_dict.json"
COVERAGE_MAP_PATH = ENGINE_DIR / "coverage_map.json"

# ─────────────────────────────────────────────────────────────────────────────
# LOGGING CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level:<8}</level> | "
           "<cyan>BLD01</cyan> | <level>{message}</level>",
    level="DEBUG",
    colorize=True,
)
logger.add(
    ENGINE_DIR / "bld01.log",
    rotation="50 MB",
    retention="30 days",
    compression="gz",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level:<8} | BLD01 | {message}",
    level="DEBUG",
)


# ═══════════════════════════════════════════════════════════════════════════════
# [TIE-01] THREE LAYER RESPONSE
# ═══════════════════════════════════════════════════════════════════════════════

class ResponseLayer(str, Enum):
    """Three-layer response system: doctrine cache, semantic retrieval, deep analysis."""
    DOCTRINE_CACHE = "doctrine_cache"
    SEMANTIC_RETRIEVAL = "semantic_retrieval"
    DEEP_ANALYSIS = "deep_analysis"


class ThreeLayerResponse:
    """Implements the three-layer response pattern for authentication queries.

    Layer 1 (0-200ms): Doctrine Cache — pre-compiled authentication principles
    Layer 2 (200-1000ms): Semantic Retrieval — normalized term lookup + vector search
    Layer 3 (1000ms+): Deep Analysis — full multi-factor reasoning chain
    """

    def __init__(self, doctrine_cache: dict[str, Any], semantic_dict: dict[str, Any]) -> None:
        self._doctrine_cache = doctrine_cache
        self._semantic_dict = semantic_dict
        self._query_count = 0
        self._layer_hits: dict[str, int] = defaultdict(int)

    def resolve(self, query: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        """Resolve a query through the three-layer system."""
        self._query_count += 1
        start_time = time.monotonic()
        normalized = self._normalize_query(query)

        # Layer 1: Doctrine Cache
        cache_result = self._check_doctrine_cache(normalized)
        if cache_result is not None:
            elapsed_ms = (time.monotonic() - start_time) * 1000
            self._layer_hits["doctrine_cache"] += 1
            logger.debug(f"Doctrine cache hit for '{query}' in {elapsed_ms:.1f}ms")
            return {
                "layer": ResponseLayer.DOCTRINE_CACHE.value,
                "result": cache_result,
                "elapsed_ms": round(elapsed_ms, 2),
                "normalized_query": normalized,
                "confidence": cache_result.get("confidence", 0.95),
            }

        # Layer 2: Semantic Retrieval
        semantic_result = self._semantic_retrieval(normalized, context)
        if semantic_result is not None:
            elapsed_ms = (time.monotonic() - start_time) * 1000
            self._layer_hits["semantic_retrieval"] += 1
            logger.debug(f"Semantic retrieval hit for '{query}' in {elapsed_ms:.1f}ms")
            return {
                "layer": ResponseLayer.SEMANTIC_RETRIEVAL.value,
                "result": semantic_result,
                "elapsed_ms": round(elapsed_ms, 2),
                "normalized_query": normalized,
                "confidence": semantic_result.get("confidence", 0.80),
            }

        # Layer 3: Deep Analysis
        deep_result = self._deep_analysis(normalized, context or {})
        elapsed_ms = (time.monotonic() - start_time) * 1000
        self._layer_hits["deep_analysis"] += 1
        logger.debug(f"Deep analysis for '{query}' in {elapsed_ms:.1f}ms")
        return {
            "layer": ResponseLayer.DEEP_ANALYSIS.value,
            "result": deep_result,
            "elapsed_ms": round(elapsed_ms, 2),
            "normalized_query": normalized,
            "confidence": deep_result.get("confidence", 0.70),
        }

    def _normalize_query(self, query: str) -> str:
        """Normalize query using semantic dictionary."""
        normalized = query.lower().strip()
        for original, replacement in self._semantic_dict.get("normalizations", {}).items():
            normalized = normalized.replace(original.lower(), replacement.lower())
        return normalized

    def _check_doctrine_cache(self, normalized: str) -> dict[str, Any] | None:
        """Check doctrine cache for pre-compiled answers."""
        entries = self._doctrine_cache.get("doctrines", [])
        for entry in entries:
            keywords = [kw.lower() for kw in entry.get("keywords", [])]
            if any(kw in normalized for kw in keywords):
                return {
                    "topic": entry.get("topic", "unknown"),
                    "conclusion": entry.get("conclusion_template", ""),
                    "reasoning": entry.get("reasoning_framework", ""),
                    "authority": entry.get("primary_authority", []),
                    "confidence": entry.get("confidence", 0.95),
                    "stratification": entry.get("confidence_stratification", "DEFENSIBLE"),
                }
        return None

    def _semantic_retrieval(self, normalized: str, context: dict[str, Any] | None) -> dict[str, Any] | None:
        """Semantic retrieval using normalized terms and synonym expansion."""
        synonyms = self._semantic_dict.get("synonyms", {})
        expanded_terms: list[str] = [normalized]
        for term, syns in synonyms.items():
            if term.lower() in normalized:
                expanded_terms.extend([s.lower() for s in syns])

        entries = self._doctrine_cache.get("doctrines", [])
        best_match: dict[str, Any] | None = None
        best_score = 0

        for entry in entries:
            keywords = [kw.lower() for kw in entry.get("keywords", [])]
            score = sum(1 for et in expanded_terms for kw in keywords if kw in et or et in kw)
            if score > best_score:
                best_score = score
                best_match = {
                    "topic": entry.get("topic", "unknown"),
                    "conclusion": entry.get("conclusion_template", ""),
                    "reasoning": entry.get("reasoning_framework", ""),
                    "authority": entry.get("primary_authority", []),
                    "confidence": min(0.85, 0.5 + score * 0.1),
                    "stratification": entry.get("confidence_stratification", "AGGRESSIVE"),
                    "match_score": score,
                }

        if best_match and best_score >= 2:
            return best_match
        return None

    def _deep_analysis(self, normalized: str, context: dict[str, Any]) -> dict[str, Any]:
        """Full deep analysis with multi-source synthesis."""
        analysis_steps = [
            "identify_authentication_context",
            "evaluate_threat_model",
            "assess_identity_claims",
            "verify_authority_chain",
            "compute_risk_score",
            "generate_recommendation",
        ]
        reasoning_chain: list[str] = []
        for step_name in analysis_steps:
            reasoning_chain.append(f"[{step_name}] Evaluating '{normalized}' in auth context")

        return {
            "topic": "deep_analysis",
            "conclusion": f"Deep analysis of authentication query: {normalized}",
            "reasoning": " -> ".join(analysis_steps),
            "reasoning_chain": reasoning_chain,
            "authority": ["BLD01 Sovereign Auth Protocol"],
            "confidence": 0.70,
            "stratification": "AGGRESSIVE",
            "context_used": list(context.keys()) if context else [],
        }

    def get_stats(self) -> dict[str, Any]:
        """Return three-layer resolution statistics."""
        return {
            "total_queries": self._query_count,
            "layer_hits": dict(self._layer_hits),
            "cache_hit_rate": (
                self._layer_hits.get("doctrine_cache", 0) / max(self._query_count, 1)
            ),
        }


# ═══════════════════════════════════════════════════════════════════════════════
# [TIE-02] RESPONSE MODES
# ═══════════════════════════════════════════════════════════════════════════════

class ResponseMode(str, Enum):
    """Response formatting modes."""
    FAST = "FAST"        # Concise, minimal output
    DEFENSE = "DEFENSE"  # Audit-ready, full citations
    MEMO = "MEMO"        # Full documentation with reasoning chain


class ResponseFormatter:
    """Formats responses according to the selected mode."""

    @staticmethod
    def format(raw: dict[str, Any], mode: ResponseMode) -> dict[str, Any]:
        """Format a raw response according to mode."""
        if mode == ResponseMode.FAST:
            return {
                "mode": "FAST",
                "result": raw.get("result", {}).get("conclusion", ""),
                "confidence": raw.get("confidence", 0.0),
                "layer": raw.get("layer", "unknown"),
            }
        elif mode == ResponseMode.DEFENSE:
            result = raw.get("result", {})
            return {
                "mode": "DEFENSE",
                "result": result.get("conclusion", ""),
                "reasoning": result.get("reasoning", ""),
                "authority": result.get("authority", []),
                "confidence": raw.get("confidence", 0.0),
                "stratification": result.get("stratification", "UNKNOWN"),
                "layer": raw.get("layer", "unknown"),
                "elapsed_ms": raw.get("elapsed_ms", 0.0),
                "audit_trail": {
                    "engine": ENGINE_ID,
                    "version": ENGINE_VERSION,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "normalized_query": raw.get("normalized_query", ""),
                },
            }
        else:  # MEMO
            result = raw.get("result", {})
            return {
                "mode": "MEMO",
                "title": f"BLD01 Authentication Analysis — {result.get('topic', 'General')}",
                "result": result.get("conclusion", ""),
                "full_reasoning": result.get("reasoning", ""),
                "reasoning_chain": result.get("reasoning_chain", []),
                "authority_citations": result.get("authority", []),
                "confidence": raw.get("confidence", 0.0),
                "stratification": result.get("stratification", "UNKNOWN"),
                "layer": raw.get("layer", "unknown"),
                "elapsed_ms": raw.get("elapsed_ms", 0.0),
                "context_used": result.get("context_used", []),
                "metadata": {
                    "engine": ENGINE_ID,
                    "version": ENGINE_VERSION,
                    "mode": ENGINE_MODE,
                    "tier": ENGINE_TIER,
                    "authority_level": AUTHORITY_LEVEL,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                },
            }


# ═══════════════════════════════════════════════════════════════════════════════
# [TIE-03] DOCTRINE CACHE
# ═══════════════════════════════════════════════════════════════════════════════

def load_doctrine_cache() -> dict[str, Any]:
    """Load the doctrine cache from disk."""
    if DOCTRINE_CACHE_PATH.exists():
        with DOCTRINE_CACHE_PATH.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
            logger.info(f"Loaded doctrine cache: {len(data.get('doctrines', []))} entries")
            return data
    logger.warning("Doctrine cache not found, using empty cache")
    return {"doctrines": []}


# ═══════════════════════════════════════════════════════════════════════════════
# [TIE-04] AUTHORITY HARDENING
# ═══════════════════════════════════════════════════════════════════════════════

class AuthorityLevel(IntEnum):
    """Hierarchical authority levels for the Bloodline system."""
    GUEST = 1
    OBSERVER = 2
    OPERATOR = 3
    TRUSTED_OPERATOR = 4
    SENIOR_OPERATOR = 5
    LIEUTENANT = 6
    CAPTAIN = 7
    COMMANDER_DELEGATE = 8
    HEIR = 9
    HEIR_APPARENT = 10
    SOVEREIGN = 11


AUTHORITY_WEIGHTS: dict[int, float] = {
    1: 0.05,   # GUEST
    2: 0.10,   # OBSERVER
    3: 0.20,   # OPERATOR
    4: 0.30,   # TRUSTED_OPERATOR
    5: 0.40,   # SENIOR_OPERATOR
    6: 0.55,   # LIEUTENANT
    7: 0.70,   # CAPTAIN
    8: 0.80,   # COMMANDER_DELEGATE
    9: 0.90,   # HEIR
    10: 0.95,  # HEIR_APPARENT
    11: 1.00,  # SOVEREIGN
}

AUTHORITY_CAPABILITIES: dict[int, list[str]] = {
    1: ["view_public"],
    2: ["view_public", "view_logs"],
    3: ["view_public", "view_logs", "execute_basic"],
    4: ["view_public", "view_logs", "execute_basic", "execute_advanced"],
    5: ["view_public", "view_logs", "execute_basic", "execute_advanced", "manage_sessions"],
    6: ["view_public", "view_logs", "execute_basic", "execute_advanced", "manage_sessions", "delegate_low"],
    7: ["view_public", "view_logs", "execute_basic", "execute_advanced", "manage_sessions", "delegate_low", "delegate_mid"],
    8: ["view_public", "view_logs", "execute_basic", "execute_advanced", "manage_sessions", "delegate_low", "delegate_mid", "manage_delegates"],
    9: ["view_public", "view_logs", "execute_basic", "execute_advanced", "manage_sessions", "delegate_low", "delegate_mid", "manage_delegates", "succession_view"],
    10: ["view_public", "view_logs", "execute_basic", "execute_advanced", "manage_sessions", "delegate_low", "delegate_mid", "manage_delegates", "succession_view", "succession_manage"],
    11: ["*"],  # SOVEREIGN — all capabilities
}


class AuthorityHardening:
    """Enforces hierarchical authority with conflict resolution."""

    @staticmethod
    def check_capability(level: int, capability: str) -> bool:
        """Check if an authority level grants a specific capability."""
        caps = AUTHORITY_CAPABILITIES.get(level, [])
        return "*" in caps or capability in caps

    @staticmethod
    def resolve_conflict(level_a: int, level_b: int) -> int:
        """Higher authority always wins. Equal levels require SOVEREIGN tiebreak."""
        if level_a == level_b:
            logger.warning(f"Authority conflict at level {level_a}, escalating to SOVEREIGN")
            return AuthorityLevel.SOVEREIGN
        return max(level_a, level_b)

    @staticmethod
    def get_weight(level: int) -> float:
        """Get the trust weight for an authority level."""
        return AUTHORITY_WEIGHTS.get(level, 0.0)

    @staticmethod
    def can_delegate(delegator_level: int, target_level: int) -> bool:
        """A delegator can only grant levels strictly below their own."""
        return delegator_level > target_level and target_level <= DELEGATE_MAX_LEVEL

    @staticmethod
    def validate_chain(chain: list[int]) -> bool:
        """Validate an authority delegation chain (each link strictly descending)."""
        for i in range(len(chain) - 1):
            if chain[i] <= chain[i + 1]:
                return False
        return True


# ═══════════════════════════════════════════════════════════════════════════════
# [TIE-05] CONFIDENCE STRATIFICATION
# ═══════════════════════════════════════════════════════════════════════════════

class ConfidenceLevel(str, Enum):
    """Confidence stratification for authentication decisions."""
    DEFENSIBLE = "DEFENSIBLE"        # High confidence, audit-proof
    AGGRESSIVE = "AGGRESSIVE"        # Reasonable confidence, some assumptions
    DISCLOSURE = "DISCLOSURE"        # Moderate confidence, caveats required
    HIGH_RISK = "HIGH_RISK"          # Low confidence, manual review needed
    CEREMONY_REQUIRED = "CEREMONY_REQUIRED"  # Requires full auth ceremony


class ConfidenceStratifier:
    """Assigns confidence stratification to authentication decisions."""

    THRESHOLDS = {
        ConfidenceLevel.DEFENSIBLE: 0.90,
        ConfidenceLevel.AGGRESSIVE: 0.75,
        ConfidenceLevel.DISCLOSURE: 0.55,
        ConfidenceLevel.HIGH_RISK: 0.30,
        ConfidenceLevel.CEREMONY_REQUIRED: 0.0,
    }

    @classmethod
    def stratify(cls, confidence: float) -> ConfidenceLevel:
        """Map a confidence score to a stratification level."""
        for level, threshold in cls.THRESHOLDS.items():
            if confidence >= threshold:
                return level
        return ConfidenceLevel.CEREMONY_REQUIRED

    @classmethod
    def requires_ceremony(cls, confidence: float, operation_level: int) -> bool:
        """Determine if an operation requires full authentication ceremony."""
        if operation_level >= AuthorityLevel.HEIR:
            return True
        stratum = cls.stratify(confidence)
        return stratum in (ConfidenceLevel.HIGH_RISK, ConfidenceLevel.CEREMONY_REQUIRED)

    @classmethod
    def get_action_guidance(cls, level: ConfidenceLevel) -> str:
        """Return recommended action for each confidence level."""
        guidance = {
            ConfidenceLevel.DEFENSIBLE: "Proceed. Authentication is audit-proof with full evidence chain.",
            ConfidenceLevel.AGGRESSIVE: "Proceed with logging. Authentication factors are strong but not exhaustive.",
            ConfidenceLevel.DISCLOSURE: "Proceed with enhanced monitoring. Some verification gaps exist.",
            ConfidenceLevel.HIGH_RISK: "Require additional factors. Confidence below operational threshold.",
            ConfidenceLevel.CEREMONY_REQUIRED: "Initiate full authentication ceremony. Identity not sufficiently established.",
        }
        return guidance.get(level, "Unknown confidence level.")


# ═══════════════════════════════════════════════════════════════════════════════
# [TIE-06] SEMANTIC NORMALIZATION
# ═══════════════════════════════════════════════════════════════════════════════

def load_semantic_dict() -> dict[str, Any]:
    """Load semantic dictionary from disk."""
    if SEMANTIC_DICT_PATH.exists():
        with SEMANTIC_DICT_PATH.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
            logger.info(f"Loaded semantic dict: {len(data.get('normalizations', {}))} norms, "
                        f"{len(data.get('synonyms', {}))} synonym groups")
            return data
    logger.warning("Semantic dict not found, using empty dict")
    return {"normalizations": {}, "synonyms": {}}


class SemanticNormalizer:
    """Domain-specific term normalization for authentication contexts."""

    def __init__(self, semantic_dict: dict[str, Any]) -> None:
        self._normalizations = semantic_dict.get("normalizations", {})
        self._synonyms = semantic_dict.get("synonyms", {})
        self._abbreviations = semantic_dict.get("abbreviations", {})

    def normalize(self, text: str) -> str:
        """Normalize authentication-domain text to canonical forms."""
        result = text.lower().strip()
        for original, replacement in self._normalizations.items():
            result = result.replace(original.lower(), replacement.lower())
        return result

    def expand_synonyms(self, term: str) -> list[str]:
        """Expand a term to all known synonyms."""
        lower_term = term.lower()
        expansions = [lower_term]
        for key, syns in self._synonyms.items():
            if key.lower() == lower_term or lower_term in [s.lower() for s in syns]:
                expansions.extend([s.lower() for s in syns])
                expansions.append(key.lower())
        return list(set(expansions))

    def resolve_abbreviation(self, abbr: str) -> str:
        """Resolve an abbreviation to its full form."""
        return self._abbreviations.get(abbr.upper(), abbr)


# ═══════════════════════════════════════════════════════════════════════════════
# [TIE-07] VECTOR SEARCH (Simplified in-memory for BLD tier)
# ═══════════════════════════════════════════════════════════════════════════════

class VectorSearchEngine:
    """In-memory vector search for authentication doctrine retrieval.

    Uses term-frequency scoring as a lightweight alternative to full
    embedding-based search. Suitable for the BLD tier where the doctrine
    corpus is bounded and domain-specific.
    """

    def __init__(self, doctrines: list[dict[str, Any]]) -> None:
        self._doctrines = doctrines
        self._index: dict[str, list[int]] = defaultdict(list)
        self._build_index()

    def _build_index(self) -> None:
        """Build inverted index from doctrine keywords and topics."""
        for idx, doctrine in enumerate(self._doctrines):
            topic_tokens = doctrine.get("topic", "").lower().split()
            for token in topic_tokens:
                self._index[token].append(idx)
            for kw in doctrine.get("keywords", []):
                for token in kw.lower().split():
                    self._index[token].append(idx)

    def search(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        """Search doctrines by query string, returning top-k matches."""
        tokens = query.lower().split()
        scores: dict[int, float] = defaultdict(float)
        for token in tokens:
            for idx in self._index.get(token, []):
                scores[idx] += 1.0

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        results: list[dict[str, Any]] = []
        for idx, score in ranked:
            d = self._doctrines[idx].copy()
            d["search_score"] = score
            results.append(d)
        return results


# ═══════════════════════════════════════════════════════════════════════════════
# [TIE-08] TELEMETRY
# ═══════════════════════════════════════════════════════════════════════════════

class TelemetryCollector:
    """Full query tracing, latency tracking, error domain classification."""

    def __init__(self) -> None:
        self._traces: list[dict[str, Any]] = []
        self._latencies: list[float] = []
        self._errors: list[dict[str, Any]] = []
        self._auth_events: list[dict[str, Any]] = []
        self._start_time = time.monotonic()

    def trace_query(self, query_id: str, endpoint: str, latency_ms: float,
                    status_code: int, auth_level: int | None = None) -> None:
        """Record a query trace."""
        trace = {
            "query_id": query_id,
            "endpoint": endpoint,
            "latency_ms": round(latency_ms, 2),
            "status_code": status_code,
            "auth_level": auth_level,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self._traces.append(trace)
        self._latencies.append(latency_ms)

    def trace_auth_event(self, event_type: str, identity: str, success: bool,
                         level: int | None = None, details: str = "") -> None:
        """Record an authentication event for security audit."""
        event = {
            "event_type": event_type,
            "identity": identity,
            "success": success,
            "level": level,
            "details": details,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self._auth_events.append(event)
        logger.info(f"Auth event: {event_type} | identity={identity} | success={success} | level={level}")

    def trace_error(self, error_type: str, message: str, domain: str = "auth") -> None:
        """Record an error with domain classification."""
        err = {
            "error_type": error_type,
            "message": message,
            "domain": domain,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self._errors.append(err)
        logger.error(f"Error [{domain}]: {error_type} — {message}")

    def get_stats(self) -> dict[str, Any]:
        """Return comprehensive telemetry statistics."""
        uptime = time.monotonic() - self._start_time
        total_queries = len(self._traces)
        total_errors = len(self._errors)
        avg_latency = sum(self._latencies) / max(len(self._latencies), 1)
        p95_latency = sorted(self._latencies)[int(len(self._latencies) * 0.95)] if self._latencies else 0.0
        p99_latency = sorted(self._latencies)[int(len(self._latencies) * 0.99)] if self._latencies else 0.0

        return {
            "uptime_seconds": round(uptime, 2),
            "total_queries": total_queries,
            "total_errors": total_errors,
            "error_rate": round(total_errors / max(total_queries, 1), 4),
            "avg_latency_ms": round(avg_latency, 2),
            "p95_latency_ms": round(p95_latency, 2),
            "p99_latency_ms": round(p99_latency, 2),
            "queries_per_minute": round(total_queries / max(uptime / 60, 1), 2),
            "auth_events": len(self._auth_events),
            "auth_success_rate": round(
                sum(1 for e in self._auth_events if e["success"]) / max(len(self._auth_events), 1), 4
            ),
            "recent_traces": self._traces[-10:],
            "recent_errors": self._errors[-10:],
            "recent_auth_events": self._auth_events[-10:],
        }


# ═══════════════════════════════════════════════════════════════════════════════
# [TIE-09] DRIFT WATCHER
# ═══════════════════════════════════════════════════════════════════════════════

class DriftWatcher:
    """Detect doctrine drift over time in authentication patterns.

    Monitors the distribution of authentication methods, confidence levels,
    and authority delegations to detect systematic shifts that could indicate
    policy erosion or credential compromise.
    """

    def __init__(self) -> None:
        self._baseline: dict[str, float] = {}
        self._current: dict[str, float] = defaultdict(float)
        self._observations: int = 0
        self._drift_alerts: list[dict[str, Any]] = []
        self._drift_threshold = 0.15  # 15% deviation triggers alert

    def set_baseline(self, baseline: dict[str, float]) -> None:
        """Set the baseline distribution for drift detection."""
        self._baseline = baseline.copy()
        logger.info(f"Drift baseline set with {len(baseline)} metrics")

    def observe(self, metric: str, value: float) -> None:
        """Record an observation for drift analysis."""
        self._observations += 1
        # Exponential moving average
        alpha = 0.1
        self._current[metric] = (1 - alpha) * self._current.get(metric, value) + alpha * value

    def check_drift(self) -> list[dict[str, Any]]:
        """Check for drift against baseline."""
        alerts: list[dict[str, Any]] = []
        for metric, baseline_val in self._baseline.items():
            current_val = self._current.get(metric, baseline_val)
            if baseline_val == 0:
                continue
            deviation = abs(current_val - baseline_val) / baseline_val
            if deviation > self._drift_threshold:
                alert = {
                    "metric": metric,
                    "baseline": round(baseline_val, 4),
                    "current": round(current_val, 4),
                    "deviation_pct": round(deviation * 100, 2),
                    "severity": "HIGH" if deviation > 0.30 else "MEDIUM",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
                alerts.append(alert)
                self._drift_alerts.append(alert)
                logger.warning(f"Drift detected: {metric} deviated {deviation*100:.1f}% from baseline")
        return alerts

    def get_status(self) -> dict[str, Any]:
        """Get drift watcher status."""
        return {
            "observations": self._observations,
            "baseline_metrics": len(self._baseline),
            "current_metrics": dict(self._current),
            "total_alerts": len(self._drift_alerts),
            "recent_alerts": self._drift_alerts[-5:],
        }


# ═══════════════════════════════════════════════════════════════════════════════
# [TIE-10] COVERAGE MAP
# ═══════════════════════════════════════════════════════════════════════════════

class CoverageMap:
    """Track triggered/missed doctrines, epistemic gap detection."""

    def __init__(self, coverage_data: dict[str, Any]) -> None:
        self._topics = coverage_data.get("topics", {})
        self._triggered: dict[str, int] = defaultdict(int)
        self._missed: dict[str, int] = defaultdict(int)
        self._gaps: list[str] = []

    def record_hit(self, topic: str) -> None:
        """Record a doctrine cache hit for a topic."""
        self._triggered[topic] += 1

    def record_miss(self, query: str) -> None:
        """Record a doctrine cache miss."""
        self._missed[query] += 1
        if self._missed[query] >= 3 and query not in self._gaps:
            self._gaps.append(query)
            logger.warning(f"Epistemic gap detected: '{query}' missed {self._missed[query]} times")

    def get_coverage(self) -> dict[str, Any]:
        """Get coverage statistics."""
        total_topics = len(self._topics)
        triggered_count = len(self._triggered)
        coverage_pct = round(triggered_count / max(total_topics, 1) * 100, 2)
        return {
            "total_topics": total_topics,
            "triggered_topics": triggered_count,
            "coverage_pct": coverage_pct,
            "top_triggered": dict(sorted(self._triggered.items(), key=lambda x: x[1], reverse=True)[:10]),
            "top_missed": dict(sorted(self._missed.items(), key=lambda x: x[1], reverse=True)[:10]),
            "epistemic_gaps": self._gaps,
            "gap_count": len(self._gaps),
        }

    def load_from_file(self) -> None:
        """Reload coverage map from disk."""
        if COVERAGE_MAP_PATH.exists():
            with COVERAGE_MAP_PATH.open("r", encoding="utf-8") as fh:
                data = json.load(fh)
                self._topics = data.get("topics", {})
                logger.info(f"Coverage map loaded: {len(self._topics)} topics")


# ═══════════════════════════════════════════════════════════════════════════════
# [TIE-11] METRICS COLLECTOR
# ═══════════════════════════════════════════════════════════════════════════════

class MetricsCollector:
    """Latency stats, error rates, hit rates, queries/hour."""

    def __init__(self) -> None:
        self._request_count = 0
        self._error_count = 0
        self._latencies: list[float] = []
        self._cache_hits = 0
        self._cache_misses = 0
        self._auth_successes = 0
        self._auth_failures = 0
        self._start_time = time.monotonic()
        self._endpoint_counts: dict[str, int] = defaultdict(int)
        self._hourly_buckets: dict[str, int] = defaultdict(int)

    def record_request(self, endpoint: str, latency_ms: float, is_error: bool = False) -> None:
        """Record a request metric."""
        self._request_count += 1
        self._latencies.append(latency_ms)
        self._endpoint_counts[endpoint] += 1
        hour_key = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H")
        self._hourly_buckets[hour_key] += 1
        if is_error:
            self._error_count += 1

    def record_cache_event(self, hit: bool) -> None:
        """Record a doctrine cache hit or miss."""
        if hit:
            self._cache_hits += 1
        else:
            self._cache_misses += 1

    def record_auth_event(self, success: bool) -> None:
        """Record authentication success or failure."""
        if success:
            self._auth_successes += 1
        else:
            self._auth_failures += 1

    def get_metrics(self) -> dict[str, Any]:
        """Return comprehensive metrics."""
        uptime = time.monotonic() - self._start_time
        sorted_latencies = sorted(self._latencies) if self._latencies else [0.0]
        return {
            "uptime_seconds": round(uptime, 2),
            "total_requests": self._request_count,
            "total_errors": self._error_count,
            "error_rate": round(self._error_count / max(self._request_count, 1), 4),
            "requests_per_hour": round(self._request_count / max(uptime / 3600, 0.001), 2),
            "latency": {
                "avg_ms": round(sum(self._latencies) / max(len(self._latencies), 1), 2),
                "min_ms": round(min(sorted_latencies), 2),
                "max_ms": round(max(sorted_latencies), 2),
                "p50_ms": round(sorted_latencies[len(sorted_latencies) // 2], 2),
                "p95_ms": round(sorted_latencies[int(len(sorted_latencies) * 0.95)], 2),
                "p99_ms": round(sorted_latencies[int(len(sorted_latencies) * 0.99)], 2),
            },
            "cache": {
                "hits": self._cache_hits,
                "misses": self._cache_misses,
                "hit_rate": round(self._cache_hits / max(self._cache_hits + self._cache_misses, 1), 4),
            },
            "auth": {
                "successes": self._auth_successes,
                "failures": self._auth_failures,
                "success_rate": round(self._auth_successes / max(self._auth_successes + self._auth_failures, 1), 4),
            },
            "endpoints": dict(self._endpoint_counts),
            "hourly_traffic": dict(list(self._hourly_buckets.items())[-24:]),
        }


# ═══════════════════════════════════════════════════════════════════════════════
# [TIE-12] HEALTH ENDPOINT (implemented in FastAPI routes below)
# ═══════════════════════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════════════════════
# [TIE-13] ZONED ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════

class AnalysisZone(str, Enum):
    """Analysis zones for authentication operations — never blur these."""
    PLANNING = "PLANNING"      # Pre-auth: evaluating identity claims
    REPORTING = "REPORTING"    # Post-auth: generating audit reports
    AUDIT = "AUDIT"            # Review: examining authentication history


class ZonedAnalyzer:
    """Enforces strict zone separation in authentication analysis.

    PLANNING zone: Evaluate whether to authenticate, what factors to require.
    REPORTING zone: Document what happened, session state, authority used.
    AUDIT zone: Review historical patterns, detect anomalies, compliance checks.

    Mixing zones (e.g., making auth decisions during an audit) is prohibited.
    """

    def __init__(self) -> None:
        self._active_zone: AnalysisZone | None = None
        self._zone_history: list[dict[str, Any]] = []

    def enter_zone(self, zone: AnalysisZone, context: str = "") -> None:
        """Enter an analysis zone."""
        if self._active_zone is not None:
            logger.warning(f"Zone transition: {self._active_zone.value} -> {zone.value}")
        self._active_zone = zone
        self._zone_history.append({
            "zone": zone.value,
            "action": "enter",
            "context": context,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

    def exit_zone(self) -> None:
        """Exit the current analysis zone."""
        if self._active_zone:
            self._zone_history.append({
                "zone": self._active_zone.value,
                "action": "exit",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
        self._active_zone = None

    def assert_zone(self, expected: AnalysisZone) -> None:
        """Assert we are in the expected zone. Raises if not."""
        if self._active_zone != expected:
            raise ValueError(
                f"Zone violation: expected {expected.value}, "
                f"currently in {self._active_zone.value if self._active_zone else 'NONE'}"
            )

    def get_history(self) -> list[dict[str, Any]]:
        """Return zone transition history."""
        return self._zone_history[-50:]


# ═══════════════════════════════════════════════════════════════════════════════
# [TIE-14] FACT FRAGILITY SCORING
# ═══════════════════════════════════════════════════════════════════════════════

class FactFragilityScorer:
    """Score the fragility of authentication claims.

    Evaluates how easily an authentication factor could be:
    - Forged (verifiability)
    - Recharacterized (recharacterization_risk)
    - Dependent on testimony (testimony_dependence)
    """

    @staticmethod
    def score_factor(factor_type: str, evidence_strength: float,
                     independent_corroboration: bool) -> dict[str, Any]:
        """Score the fragility of a single authentication factor."""
        base_fragility = {
            "knowledge": 0.35,       # Security questions — phishable
            "biometric": 0.10,       # Hard to forge, low fragility
            "behavioral": 0.20,      # Typing patterns — moderate
            "device": 0.25,          # Device fingerprint — clonable
            "location": 0.30,        # IP/geo — spoofable
            "temporal": 0.40,        # Time-based — predictable
            "ceremony": 0.05,        # Multi-step — very robust
        }

        fragility = base_fragility.get(factor_type, 0.50)
        if independent_corroboration:
            fragility *= 0.6  # Independent verification reduces fragility
        fragility *= (1.0 - evidence_strength * 0.5)  # Strong evidence reduces fragility

        verifiability = 1.0 - fragility
        recharacterization_risk = fragility * 0.7
        testimony_dependence = fragility * 0.5 if factor_type in ("knowledge", "temporal") else fragility * 0.2

        return {
            "factor_type": factor_type,
            "fragility_score": round(fragility, 4),
            "verifiability": round(verifiability, 4),
            "recharacterization_risk": round(recharacterization_risk, 4),
            "testimony_dependence": round(testimony_dependence, 4),
            "independent_corroboration": independent_corroboration,
            "evidence_strength": evidence_strength,
            "recommendation": (
                "STRONG" if fragility < 0.15 else
                "ADEQUATE" if fragility < 0.30 else
                "WEAK" if fragility < 0.45 else
                "FRAGILE"
            ),
        }

    @staticmethod
    def composite_fragility(factor_scores: list[dict[str, Any]]) -> dict[str, Any]:
        """Compute composite fragility from multiple factor scores."""
        if not factor_scores:
            return {"composite_fragility": 1.0, "recommendation": "NO_FACTORS"}

        # Multi-factor authentication reduces composite fragility multiplicatively
        composite = 1.0
        for score in factor_scores:
            composite *= score["fragility_score"]

        avg_verifiability = sum(s["verifiability"] for s in factor_scores) / len(factor_scores)
        max_rechar_risk = max(s["recharacterization_risk"] for s in factor_scores)

        return {
            "composite_fragility": round(composite, 6),
            "avg_verifiability": round(avg_verifiability, 4),
            "max_recharacterization_risk": round(max_rechar_risk, 4),
            "factor_count": len(factor_scores),
            "recommendation": (
                "FORTRESS" if composite < 0.001 else
                "STRONG" if composite < 0.01 else
                "ADEQUATE" if composite < 0.05 else
                "NEEDS_IMPROVEMENT"
            ),
        }


# ═══════════════════════════════════════════════════════════════════════════════
# [TIE-15] AUDIT TRAIL (JSONL)
# ═══════════════════════════════════════════════════════════════════════════════

class AuditTrail:
    """Append-only JSONL audit trail for forensic review."""

    def __init__(self, log_path: Path) -> None:
        self._log_path = log_path
        self._log_path.parent.mkdir(parents=True, exist_ok=True)
        self._entry_count = 0

    def log(self, event_type: str, data: dict[str, Any]) -> str:
        """Append an audit entry. Returns the entry ID."""
        entry_id = str(uuid.uuid4())
        entry = {
            "id": entry_id,
            "event_type": event_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "engine": ENGINE_ID,
            "data": data,
        }
        # Compute integrity hash over the entry
        entry_json = json.dumps(entry, sort_keys=True, separators=(",", ":"))
        entry["integrity_hash"] = hashlib.sha256(entry_json.encode()).hexdigest()

        with self._log_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry, separators=(",", ":")) + "\n")

        self._entry_count += 1
        return entry_id

    def query(self, event_type: str | None = None, limit: int = 50) -> list[dict[str, Any]]:
        """Query the audit trail (most recent first)."""
        if not self._log_path.exists():
            return []
        entries: list[dict[str, Any]] = []
        with self._log_path.open("r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                entry = json.loads(line)
                if event_type is None or entry.get("event_type") == event_type:
                    entries.append(entry)
        return entries[-limit:]

    def get_stats(self) -> dict[str, Any]:
        """Return audit trail statistics."""
        size_bytes = self._log_path.stat().st_size if self._log_path.exists() else 0
        return {
            "log_path": str(self._log_path),
            "entries_this_session": self._entry_count,
            "file_size_bytes": size_bytes,
            "file_size_mb": round(size_bytes / (1024 * 1024), 2),
        }


# ═══════════════════════════════════════════════════════════════════════════════
# [TIE-16] DETERMINISM HASH (SHA-256)
# ═══════════════════════════════════════════════════════════════════════════════

def compute_determinism_hash(data: dict[str, Any]) -> str:
    """Compute SHA-256 determinism hash for reproducibility.

    Given the same input data, this always produces the same hash,
    enabling verification that authentication decisions are reproducible.
    """
    canonical = json.dumps(data, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


# ═══════════════════════════════════════════════════════════════════════════════
# [TIE-19] MULTI-DOCTRINE DECOMPOSITION
# ═══════════════════════════════════════════════════════════════════════════════

class AuthIssueCategory(str, Enum):
    """Issue categories for multi-doctrine decomposition."""
    IDENTITY_VERIFICATION = "identity_verification"
    SESSION_MANAGEMENT = "session_management"
    AUTHORITY_DELEGATION = "authority_delegation"
    SUCCESSION_PLANNING = "succession_planning"
    EMERGENCY_PROTOCOL = "emergency_protocol"
    CEREMONY_PROTOCOL = "ceremony_protocol"
    BEHAVIORAL_ANALYSIS = "behavioral_analysis"
    DEVICE_TRUST = "device_trust"
    TEMPORAL_ANALYSIS = "temporal_analysis"
    THREAT_ASSESSMENT = "threat_assessment"


class MultiDoctrineDecomposer:
    """Decompose complex authentication queries into issue categories,
    strata, and an interaction DAG."""

    INTERACTION_EDGES: list[tuple[str, str, str]] = [
        ("identity_verification", "session_management", "identity must be verified before session creation"),
        ("identity_verification", "authority_delegation", "identity determines maximum delegable authority"),
        ("authority_delegation", "session_management", "delegated sessions have scoped permissions"),
        ("succession_planning", "emergency_protocol", "succession activates on dead man's switch"),
        ("ceremony_protocol", "identity_verification", "ceremony is the highest form of identity verification"),
        ("behavioral_analysis", "identity_verification", "behavioral patterns supplement identity verification"),
        ("device_trust", "session_management", "device trust affects session security level"),
        ("temporal_analysis", "threat_assessment", "unusual timing patterns indicate potential threats"),
        ("threat_assessment", "emergency_protocol", "high threat level triggers emergency protocol"),
        ("identity_verification", "ceremony_protocol", "low-confidence identity triggers ceremony requirement"),
    ]

    def decompose(self, query: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        """Decompose a query into issue categories with interaction DAG."""
        categories_detected: list[str] = []
        query_lower = query.lower()

        category_keywords: dict[str, list[str]] = {
            AuthIssueCategory.IDENTITY_VERIFICATION.value: ["identity", "verify", "authenticate", "who", "prove"],
            AuthIssueCategory.SESSION_MANAGEMENT.value: ["session", "token", "login", "logout", "timeout"],
            AuthIssueCategory.AUTHORITY_DELEGATION.value: ["delegate", "grant", "permission", "authorize", "scope"],
            AuthIssueCategory.SUCCESSION_PLANNING.value: ["heir", "successor", "inheritance", "bloodline", "dynasty"],
            AuthIssueCategory.EMERGENCY_PROTOCOL.value: ["emergency", "lockout", "panic", "revoke", "freeze"],
            AuthIssueCategory.CEREMONY_PROTOCOL.value: ["ceremony", "ritual", "sovereign", "supreme", "multi-step"],
            AuthIssueCategory.BEHAVIORAL_ANALYSIS.value: ["behavior", "pattern", "typing", "cadence", "habit"],
            AuthIssueCategory.DEVICE_TRUST.value: ["device", "fingerprint", "hardware", "machine", "trusted"],
            AuthIssueCategory.TEMPORAL_ANALYSIS.value: ["time", "schedule", "when", "hour", "pattern"],
            AuthIssueCategory.THREAT_ASSESSMENT.value: ["threat", "attack", "breach", "compromise", "suspicious"],
        }

        for category, keywords in category_keywords.items():
            if any(kw in query_lower for kw in keywords):
                categories_detected.append(category)

        if not categories_detected:
            categories_detected = [AuthIssueCategory.IDENTITY_VERIFICATION.value]

        # Build relevant edges
        relevant_edges = [
            {"from": src, "to": dst, "reason": reason}
            for src, dst, reason in self.INTERACTION_EDGES
            if src in categories_detected or dst in categories_detected
        ]

        return {
            "query": query,
            "categories_detected": categories_detected,
            "category_count": len(categories_detected),
            "interaction_dag": relevant_edges,
            "interaction_edge_count": len(relevant_edges),
            "resolution_order": self._topological_sort(categories_detected, relevant_edges),
        }

    @staticmethod
    def _topological_sort(categories: list[str], edges: list[dict[str, str]]) -> list[str]:
        """Topological sort of categories based on interaction edges."""
        in_degree: dict[str, int] = {c: 0 for c in categories}
        adj: dict[str, list[str]] = {c: [] for c in categories}

        for edge in edges:
            src, dst = edge["from"], edge["to"]
            if src in adj and dst in in_degree:
                adj[src].append(dst)
                in_degree[dst] += 1

        queue = [c for c in categories if in_degree[c] == 0]
        order: list[str] = []
        while queue:
            node = queue.pop(0)
            order.append(node)
            for neighbor in adj.get(node, []):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        # Add any remaining (cyclic) nodes
        for c in categories:
            if c not in order:
                order.append(c)
        return order


# ═══════════════════════════════════════════════════════════════════════════════
# [TIE-20] DEEP ANALYSIS MODE
# ═══════════════════════════════════════════════════════════════════════════════

class DeepAnalyzer:
    """Multi-source synthesis with full reasoning chain for auth queries."""

    def __init__(self, doctrine_cache: dict[str, Any], semantic_dict: dict[str, Any]) -> None:
        self._doctrine_cache = doctrine_cache
        self._semantic_dict = semantic_dict
        self._decomposer = MultiDoctrineDecomposer()
        self._fragility_scorer = FactFragilityScorer()

    def analyze(self, query: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        """Perform deep multi-source analysis."""
        start = time.monotonic()
        context = context or {}

        # Step 1: Decompose
        decomposition = self._decomposer.decompose(query, context)

        # Step 2: Gather doctrine evidence for each category
        evidence: dict[str, list[dict[str, Any]]] = {}
        for category in decomposition["categories_detected"]:
            evidence[category] = self._gather_evidence(category)

        # Step 3: Synthesize reasoning chain
        reasoning_chain = self._build_reasoning_chain(decomposition, evidence, context)

        # Step 4: Score fragility of the overall analysis
        factor_scores = []
        for cat in decomposition["categories_detected"]:
            factor_scores.append(
                self._fragility_scorer.score_factor(
                    factor_type="knowledge",
                    evidence_strength=0.8 if evidence.get(cat) else 0.3,
                    independent_corroboration=len(evidence.get(cat, [])) > 1,
                )
            )
        composite = self._fragility_scorer.composite_fragility(factor_scores)

        elapsed_ms = (time.monotonic() - start) * 1000
        return {
            "query": query,
            "decomposition": decomposition,
            "evidence": {k: len(v) for k, v in evidence.items()},
            "reasoning_chain": reasoning_chain,
            "fragility": composite,
            "confidence": round(1.0 - composite["composite_fragility"], 4),
            "elapsed_ms": round(elapsed_ms, 2),
            "determinism_hash": compute_determinism_hash({
                "query": query,
                "categories": decomposition["categories_detected"],
                "evidence_counts": {k: len(v) for k, v in evidence.items()},
            }),
        }

    def _gather_evidence(self, category: str) -> list[dict[str, Any]]:
        """Gather doctrine evidence for a specific category."""
        results: list[dict[str, Any]] = []
        for doctrine in self._doctrine_cache.get("doctrines", []):
            keywords = [kw.lower() for kw in doctrine.get("keywords", [])]
            if any(category.replace("_", " ") in kw or kw in category for kw in keywords):
                results.append(doctrine)
        return results

    def _build_reasoning_chain(self, decomposition: dict[str, Any],
                                evidence: dict[str, list[dict[str, Any]]],
                                context: dict[str, Any]) -> list[dict[str, Any]]:
        """Build a step-by-step reasoning chain."""
        chain: list[dict[str, Any]] = []
        for step_num, category in enumerate(decomposition["resolution_order"], 1):
            ev = evidence.get(category, [])
            chain.append({
                "step": step_num,
                "category": category,
                "action": f"Analyze {category.replace('_', ' ')}",
                "evidence_count": len(ev),
                "evidence_topics": [e.get("topic", "unknown") for e in ev[:3]],
                "conclusion": (
                    f"Doctrine evidence supports {category} analysis with {len(ev)} sources"
                    if ev else
                    f"No direct doctrine evidence for {category}; using deep reasoning"
                ),
            })
        return chain


# ═══════════════════════════════════════════════════════════════════════════════
# CORE AUTHENTICATION MODELS (Pydantic)
# ═══════════════════════════════════════════════════════════════════════════════

class BloodlineIdentity(BaseModel):
    """The immutable identity record of a bloodline member."""
    identity_id: str = Field(description="Unique identity identifier")
    full_name: str = Field(description="Full legal name")
    dob: str = Field(description="Date of birth (MM/DD/YYYY)")
    location: str = Field(description="Primary location")
    authority_level: float = Field(ge=0.0, le=11.0, description="Authority level")
    role: str = Field(description="Dynasty role")
    bloodline_position: str = Field(description="Position in bloodline chain")
    registered_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    knowledge_hash: str = Field(default="", description="SHA-256 of knowledge challenge answers")
    device_fingerprints: list[str] = Field(default_factory=list)
    behavioral_hash: str = Field(default="", description="Behavioral pattern hash")
    is_active: bool = Field(default=True)


class AuthCredentials(BaseModel):
    """Authentication credentials submitted for verification."""
    identity_id: str = Field(description="Claimed identity")
    knowledge_response: str = Field(default="", description="Security question answer")
    device_fingerprint: str = Field(default="", description="Device fingerprint hash")
    behavioral_sample: str = Field(default="", description="Behavioral pattern sample")
    ceremony_token: str = Field(default="", description="Active ceremony token if in ceremony flow")


class SessionToken(BaseModel):
    """An active authentication session."""
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    identity_id: str
    authority_level: float
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    expires_at: str
    is_revoked: bool = Field(default=False)
    device_fingerprint: str = Field(default="")
    auth_factors_used: list[str] = Field(default_factory=list)
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    scope: list[str] = Field(default_factory=lambda: ["*"])


class DelegationToken(BaseModel):
    """Authority delegation from Commander to a delegate."""
    delegation_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    delegator_id: str = Field(description="Who granted this delegation")
    delegate_id: str = Field(description="Who receives the delegation")
    max_level: float = Field(ge=0.0, le=11.0)
    scope: list[str] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    expires_at: str
    is_revoked: bool = Field(default=False)
    reason: str = Field(default="")


class CeremonyState(BaseModel):
    """State of an authentication ceremony (multi-step verification)."""
    ceremony_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    identity_id: str
    steps_completed: list[str] = Field(default_factory=list)
    steps_required: list[str] = Field(default_factory=list)
    challenge_token: str = Field(default="")
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    expires_at: str
    is_complete: bool = Field(default=False)
    confidence_accumulated: float = Field(default=0.0)


class DeadManSwitchConfig(BaseModel):
    """Configuration for the dead man's switch."""
    is_armed: bool = Field(default=True)
    timeout_hours: int = Field(default=DEAD_MAN_SWITCH_DEFAULT_HOURS)
    last_heartbeat: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    succession_triggered: bool = Field(default=False)
    designated_heir_id: str = Field(default="")
    alert_contacts: list[str] = Field(default_factory=list)


class AuthenticateRequest(BaseModel):
    """Request body for /authenticate."""
    identity_id: str
    knowledge_response: str = ""
    device_fingerprint: str = ""
    behavioral_sample: str = ""
    requested_level: float = Field(default=0.0, ge=0.0, le=11.0)


class DelegateRequest(BaseModel):
    """Request body for /delegate."""
    delegator_session_id: str = Field(description="Active session of the delegator")
    delegate_id: str = Field(description="Identity to delegate to")
    max_level: float = Field(ge=0.0, le=11.0)
    duration_hours: int = Field(default=24, ge=1, le=720)
    scope: list[str] = Field(default_factory=lambda: ["execute_basic"])
    reason: str = Field(default="")


class BloodlineVerifyRequest(BaseModel):
    """Request body for /verify-bloodline."""
    identity_id: str
    challenge_type: str = Field(default="knowledge", description="knowledge|ceremony|behavioral")
    challenge_response: str = Field(default="")
    ceremony_token: str = Field(default="")


class LockoutRequest(BaseModel):
    """Request body for /lockout."""
    commander_session_id: str = Field(description="Must be SOVEREIGN session")
    reason: str = Field(default="Emergency lockout initiated by SOVEREIGN")
    preserve_emergency_recovery: bool = Field(default=True)


class HeartbeatRequest(BaseModel):
    """Request body for dead man's switch heartbeat."""
    commander_session_id: str
    message: str = Field(default="alive")


class QueryRequest(BaseModel):
    """Request body for the three-layer query endpoint."""
    query: str
    mode: ResponseMode = Field(default=ResponseMode.FAST)
    context: dict[str, Any] = Field(default_factory=dict)


# ═══════════════════════════════════════════════════════════════════════════════
# BLOODLINE AUTHENTICATOR CORE
# ═══════════════════════════════════════════════════════════════════════════════

class BloodlineAuthenticator:
    """Supreme authentication engine for the McWilliams Dynasty.

    Manages identity verification, session control, authority delegation,
    bloodline chain verification, emergency lockout, dead man's switch,
    and authentication ceremonies for SOVEREIGN operations.
    """

    def __init__(self) -> None:
        # Identity registry
        self._identities: dict[str, BloodlineIdentity] = {}
        # Active sessions
        self._sessions: dict[str, SessionToken] = {}
        # Delegations
        self._delegations: dict[str, DelegationToken] = {}
        # Active ceremonies
        self._ceremonies: dict[str, CeremonyState] = {}
        # Dead man's switch
        self._dead_man_switch = DeadManSwitchConfig()
        # Failed attempts tracker
        self._failed_attempts: dict[str, list[float]] = defaultdict(list)
        # Lockout state
        self._global_lockout = False
        self._lockout_reason = ""
        self._emergency_recovery_sessions: set[str] = set()

        # Register the Commander (SOVEREIGN)
        self._register_commander()

    def _register_commander(self) -> None:
        """Register the Commander's immutable identity."""
        commander_knowledge = "McWilliams-Midland-1976-SOVEREIGN"
        knowledge_hash = self._hash_secret(commander_knowledge)

        commander = BloodlineIdentity(
            identity_id="CMDR-001",
            full_name="Bobby Don McWilliams II",
            dob="05/14/1976",
            location="Midland, TX",
            authority_level=SOVEREIGN_LEVEL,
            role="SOVEREIGN COMMANDER",
            bloodline_position="PATRIARCH",
            knowledge_hash=knowledge_hash,
            device_fingerprints=[],
            behavioral_hash="",
            is_active=True,
        )
        self._identities[commander.identity_id] = commander
        logger.info(f"Commander registered: {commander.full_name} | Level {commander.authority_level}")

        # Register heir placeholder (can be updated by Commander)
        heir = BloodlineIdentity(
            identity_id="HEIR-001",
            full_name="Designated Heir",
            dob="",
            location="Midland, TX",
            authority_level=HEIR_MAX_LEVEL,
            role="HEIR APPARENT",
            bloodline_position="FIRST_IN_LINE",
            knowledge_hash="",
            device_fingerprints=[],
            behavioral_hash="",
            is_active=False,
        )
        self._identities[heir.identity_id] = heir
        self._dead_man_switch.designated_heir_id = heir.identity_id

    @staticmethod
    def _hash_secret(secret: str) -> str:
        """Hash a secret with HMAC-SHA256 and pepper."""
        return hmac.new(
            HMAC_KEY.encode("utf-8"),
            (secret + PEPPER).encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

    @staticmethod
    def _generate_token(length: int = TOKEN_LENGTH) -> str:
        """Generate a cryptographically secure random token."""
        return secrets.token_urlsafe(length)

    def _check_lockout(self, identity_id: str) -> tuple[bool, str]:
        """Check if an identity is locked out due to failed attempts."""
        if self._global_lockout:
            return True, f"Global lockout active: {self._lockout_reason}"

        attempts = self._failed_attempts.get(identity_id, [])
        # Clean old attempts
        cutoff = time.time() - AUTH_LOCKOUT_DURATION_SECONDS
        self._failed_attempts[identity_id] = [t for t in attempts if t > cutoff]
        attempts = self._failed_attempts[identity_id]

        if len(attempts) >= MAX_AUTH_ATTEMPTS:
            return True, f"Identity locked out: {len(attempts)} failed attempts in last {AUTH_LOCKOUT_DURATION_SECONDS}s"
        return False, ""

    def _record_failed_attempt(self, identity_id: str) -> int:
        """Record a failed authentication attempt. Returns current count."""
        self._failed_attempts[identity_id].append(time.time())
        count = len(self._failed_attempts[identity_id])
        logger.warning(f"Failed auth attempt #{count} for {identity_id}")
        return count

    def _clean_expired_sessions(self) -> int:
        """Remove expired sessions. Returns count of cleaned sessions."""
        now = datetime.now(timezone.utc)
        expired: list[str] = []
        for sid, session in self._sessions.items():
            exp = datetime.fromisoformat(session.expires_at)
            if exp < now:
                expired.append(sid)
        for sid in expired:
            del self._sessions[sid]
        if expired:
            logger.info(f"Cleaned {len(expired)} expired sessions")
        return len(expired)

    def _count_active_sessions(self, identity_id: str) -> int:
        """Count active (non-expired, non-revoked) sessions for an identity."""
        self._clean_expired_sessions()
        return sum(
            1 for s in self._sessions.values()
            if s.identity_id == identity_id and not s.is_revoked
        )

    # ─── AUTHENTICATE ─────────────────────────────────────────────────────

    def authenticate(self, request: AuthenticateRequest) -> dict[str, Any]:
        """Authenticate an identity and create a session.

        Multi-factor verification:
        1. Knowledge challenge (security question hash match)
        2. Device fingerprint match
        3. Behavioral pattern match
        """
        identity_id = request.identity_id
        logger.info(f"Authentication request for {identity_id}")

        # Check lockout
        is_locked, reason = self._check_lockout(identity_id)
        if is_locked:
            return {"success": False, "error": reason, "locked_out": True}

        # Lookup identity
        identity = self._identities.get(identity_id)
        if identity is None:
            self._record_failed_attempt(identity_id)
            return {"success": False, "error": "Identity not found", "locked_out": False}

        if not identity.is_active:
            return {"success": False, "error": "Identity is deactivated", "locked_out": False}

        # Check max concurrent sessions
        active_count = self._count_active_sessions(identity_id)
        if active_count >= MAX_CONCURRENT_SESSIONS:
            return {"success": False, "error": f"Max concurrent sessions ({MAX_CONCURRENT_SESSIONS}) reached"}

        # Multi-factor verification
        factors_verified: list[str] = []
        confidence = 0.0

        # Factor 1: Knowledge challenge
        if request.knowledge_response:
            expected_hash = identity.knowledge_hash
            provided_hash = self._hash_secret(request.knowledge_response)
            if hmac.compare_digest(expected_hash, provided_hash):
                factors_verified.append("knowledge")
                confidence += 0.40
                logger.debug(f"Knowledge factor verified for {identity_id}")
            else:
                self._record_failed_attempt(identity_id)
                return {"success": False, "error": "Knowledge challenge failed", "locked_out": False}

        # Factor 2: Device fingerprint
        if request.device_fingerprint:
            if request.device_fingerprint in identity.device_fingerprints:
                factors_verified.append("device")
                confidence += 0.25
                logger.debug(f"Device factor verified for {identity_id}")
            elif not identity.device_fingerprints:
                # First device registration
                identity.device_fingerprints.append(request.device_fingerprint)
                factors_verified.append("device_new")
                confidence += 0.15
                logger.info(f"New device registered for {identity_id}")
            else:
                factors_verified.append("device_unknown")
                confidence += 0.05

        # Factor 3: Behavioral pattern
        if request.behavioral_sample:
            if identity.behavioral_hash:
                provided_hash = self._hash_secret(request.behavioral_sample)
                if hmac.compare_digest(identity.behavioral_hash, provided_hash):
                    factors_verified.append("behavioral")
                    confidence += 0.20
                    logger.debug(f"Behavioral factor verified for {identity_id}")
                else:
                    factors_verified.append("behavioral_mismatch")
                    confidence += 0.05
            else:
                # First behavioral sample — store it
                identity.behavioral_hash = self._hash_secret(request.behavioral_sample)
                factors_verified.append("behavioral_new")
                confidence += 0.10

        # Base confidence for known identity
        if not factors_verified:
            confidence = 0.10  # Identity exists but no factors provided

        # SOVEREIGN requires ceremony for operations above level 9
        requested_level = request.requested_level or identity.authority_level
        if requested_level > 9.0 and confidence < 0.90:
            return {
                "success": False,
                "error": "SOVEREIGN operations require authentication ceremony",
                "ceremony_required": True,
                "confidence": round(confidence, 4),
                "factors_verified": factors_verified,
            }

        # Check if requested level is allowed
        if requested_level > identity.authority_level:
            return {
                "success": False,
                "error": f"Requested level {requested_level} exceeds max authority {identity.authority_level}",
            }

        # Determine granted level based on confidence
        granted_level = min(
            requested_level,
            identity.authority_level * min(confidence / 0.8, 1.0),
        )

        # Create session
        expires_at = (datetime.now(timezone.utc) + timedelta(seconds=SESSION_TTL_SECONDS)).isoformat()
        session = SessionToken(
            identity_id=identity_id,
            authority_level=round(granted_level, 1),
            expires_at=expires_at,
            device_fingerprint=request.device_fingerprint,
            auth_factors_used=factors_verified,
            confidence=round(confidence, 4),
        )
        self._sessions[session.session_id] = session

        logger.info(
            f"Session created: {session.session_id} | identity={identity_id} | "
            f"level={granted_level:.1f} | factors={factors_verified} | confidence={confidence:.4f}"
        )

        return {
            "success": True,
            "session_id": session.session_id,
            "identity_id": identity_id,
            "authority_level": round(granted_level, 1),
            "factors_verified": factors_verified,
            "confidence": round(confidence, 4),
            "expires_at": expires_at,
            "stratification": ConfidenceStratifier.stratify(confidence).value,
        }

    # ─── VALIDATE SESSION ─────────────────────────────────────────────────

    def validate_session(self, session_id: str) -> dict[str, Any]:
        """Validate an existing session."""
        session = self._sessions.get(session_id)
        if session is None:
            return {"valid": False, "error": "Session not found"}
        if session.is_revoked:
            return {"valid": False, "error": "Session has been revoked"}

        expires = datetime.fromisoformat(session.expires_at)
        if expires < datetime.now(timezone.utc):
            return {"valid": False, "error": "Session has expired"}

        return {
            "valid": True,
            "session_id": session_id,
            "identity_id": session.identity_id,
            "authority_level": session.authority_level,
            "confidence": session.confidence,
            "auth_factors": session.auth_factors_used,
            "expires_at": session.expires_at,
            "scope": session.scope,
        }

    # ─── REVOKE SESSION ───────────────────────────────────────────────────

    def revoke_session(self, session_id: str, revoker_session_id: str) -> dict[str, Any]:
        """Revoke a session. Revoker must have manage_sessions capability."""
        revoker_session = self._sessions.get(revoker_session_id)
        if revoker_session is None:
            return {"success": False, "error": "Revoker session not found"}

        revoker_level = int(revoker_session.authority_level)
        if not AuthorityHardening.check_capability(revoker_level, "manage_sessions"):
            return {"success": False, "error": "Insufficient authority to revoke sessions"}

        target_session = self._sessions.get(session_id)
        if target_session is None:
            return {"success": False, "error": "Target session not found"}

        if target_session.authority_level > revoker_session.authority_level:
            return {"success": False, "error": "Cannot revoke a higher-authority session"}

        target_session.is_revoked = True
        logger.info(f"Session {session_id} revoked by {revoker_session_id}")
        return {"success": True, "revoked_session_id": session_id}

    # ─── DELEGATE AUTHORITY ───────────────────────────────────────────────

    def delegate(self, request: DelegateRequest) -> dict[str, Any]:
        """Delegate authority from one identity to another."""
        # Validate delegator session
        delegator_session = self._sessions.get(request.delegator_session_id)
        if delegator_session is None:
            return {"success": False, "error": "Delegator session not found"}
        if delegator_session.is_revoked:
            return {"success": False, "error": "Delegator session is revoked"}

        delegator_level = int(delegator_session.authority_level)

        # Check delegation capability
        if not AuthorityHardening.check_capability(delegator_level, "delegate_low"):
            return {"success": False, "error": "Insufficient authority to delegate"}

        # Check delegation rules
        if not AuthorityHardening.can_delegate(delegator_level, int(request.max_level)):
            return {
                "success": False,
                "error": f"Cannot delegate level {request.max_level} (your level: {delegator_level}, "
                         f"max delegable: {DELEGATE_MAX_LEVEL})",
            }

        # Verify delegate exists
        delegate_identity = self._identities.get(request.delegate_id)
        if delegate_identity is None:
            return {"success": False, "error": f"Delegate identity {request.delegate_id} not found"}

        # Create delegation
        expires_at = (datetime.now(timezone.utc) + timedelta(hours=request.duration_hours)).isoformat()
        delegation = DelegationToken(
            delegator_id=delegator_session.identity_id,
            delegate_id=request.delegate_id,
            max_level=request.max_level,
            scope=request.scope,
            expires_at=expires_at,
            reason=request.reason,
        )
        self._delegations[delegation.delegation_id] = delegation

        logger.info(
            f"Delegation created: {delegation.delegation_id} | "
            f"from={delegator_session.identity_id} to={request.delegate_id} | "
            f"level={request.max_level} | scope={request.scope}"
        )

        return {
            "success": True,
            "delegation_id": delegation.delegation_id,
            "delegator_id": delegator_session.identity_id,
            "delegate_id": request.delegate_id,
            "max_level": request.max_level,
            "scope": request.scope,
            "expires_at": expires_at,
        }

    # ─── VERIFY BLOODLINE ────────────────────────────────────────────────

    def verify_bloodline(self, request: BloodlineVerifyRequest) -> dict[str, Any]:
        """Verify bloodline membership and authenticate via challenge."""
        identity = self._identities.get(request.identity_id)
        if identity is None:
            return {"verified": False, "error": "Identity not in bloodline registry"}

        if not identity.is_active:
            return {"verified": False, "error": "Bloodline member is deactivated"}

        if request.challenge_type == "knowledge":
            if not request.challenge_response:
                return {
                    "verified": False,
                    "challenge_issued": True,
                    "message": "Provide your knowledge challenge response",
                }
            provided_hash = self._hash_secret(request.challenge_response)
            if hmac.compare_digest(identity.knowledge_hash, provided_hash):
                return {
                    "verified": True,
                    "identity_id": identity.identity_id,
                    "full_name": identity.full_name,
                    "authority_level": identity.authority_level,
                    "bloodline_position": identity.bloodline_position,
                    "role": identity.role,
                }
            else:
                self._record_failed_attempt(request.identity_id)
                return {"verified": False, "error": "Knowledge challenge failed"}

        elif request.challenge_type == "ceremony":
            return self._initiate_ceremony(request.identity_id)

        elif request.challenge_type == "behavioral":
            if identity.behavioral_hash and request.challenge_response:
                provided_hash = self._hash_secret(request.challenge_response)
                match = hmac.compare_digest(identity.behavioral_hash, provided_hash)
                return {
                    "verified": match,
                    "identity_id": identity.identity_id,
                    "challenge_type": "behavioral",
                    "confidence": 0.85 if match else 0.10,
                }
            return {"verified": False, "error": "No behavioral baseline established"}

        return {"verified": False, "error": f"Unknown challenge type: {request.challenge_type}"}

    # ─── CEREMONY PROTOCOL ───────────────────────────────────────────────

    def _initiate_ceremony(self, identity_id: str) -> dict[str, Any]:
        """Initiate a multi-step authentication ceremony for SOVEREIGN operations."""
        identity = self._identities.get(identity_id)
        if identity is None:
            return {"success": False, "error": "Identity not found"}

        steps_required = [
            "confirm_identity",
            "verify_knowledge",
            "verify_bloodline_position",
            "authorize_sovereign_action",
        ]
        if identity.authority_level >= SOVEREIGN_LEVEL:
            steps_required.append("sovereign_confirmation")

        expires_at = (datetime.now(timezone.utc) + timedelta(seconds=CEREMONY_TIMEOUT_SECONDS)).isoformat()
        challenge_token = self._generate_token(32)

        ceremony = CeremonyState(
            identity_id=identity_id,
            steps_required=steps_required,
            challenge_token=challenge_token,
            expires_at=expires_at,
        )
        self._ceremonies[ceremony.ceremony_id] = ceremony

        logger.info(f"Ceremony initiated: {ceremony.ceremony_id} for {identity_id} | steps={len(steps_required)}")

        return {
            "ceremony_initiated": True,
            "ceremony_id": ceremony.ceremony_id,
            "challenge_token": challenge_token,
            "steps_required": steps_required,
            "steps_completed": [],
            "expires_at": expires_at,
            "timeout_seconds": CEREMONY_TIMEOUT_SECONDS,
        }

    def advance_ceremony(self, ceremony_id: str, step: str,
                          response: str, challenge_token: str) -> dict[str, Any]:
        """Advance a ceremony by completing a step."""
        ceremony = self._ceremonies.get(ceremony_id)
        if ceremony is None:
            return {"success": False, "error": "Ceremony not found"}

        # Check expiry
        expires = datetime.fromisoformat(ceremony.expires_at)
        if expires < datetime.now(timezone.utc):
            del self._ceremonies[ceremony_id]
            return {"success": False, "error": "Ceremony expired"}

        # Validate challenge token
        if not hmac.compare_digest(ceremony.challenge_token, challenge_token):
            return {"success": False, "error": "Invalid challenge token"}

        # Check step is next required
        remaining = [s for s in ceremony.steps_required if s not in ceremony.steps_completed]
        if not remaining:
            return {"success": False, "error": "Ceremony already complete"}
        if step != remaining[0]:
            return {"success": False, "error": f"Expected step '{remaining[0]}', got '{step}'"}

        # Verify step response
        verified = self._verify_ceremony_step(ceremony.identity_id, step, response)
        if not verified:
            self._record_failed_attempt(ceremony.identity_id)
            return {"success": False, "error": f"Ceremony step '{step}' verification failed"}

        ceremony.steps_completed.append(step)
        ceremony.confidence_accumulated += 1.0 / len(ceremony.steps_required)

        # Check if ceremony is complete
        if set(ceremony.steps_completed) == set(ceremony.steps_required):
            ceremony.is_complete = True
            # Create SOVEREIGN session
            identity = self._identities[ceremony.identity_id]
            expires_at = (datetime.now(timezone.utc) + timedelta(seconds=SESSION_TTL_SECONDS)).isoformat()
            session = SessionToken(
                identity_id=ceremony.identity_id,
                authority_level=identity.authority_level,
                expires_at=expires_at,
                auth_factors_used=["ceremony_full"],
                confidence=ceremony.confidence_accumulated,
                scope=["*"],
            )
            self._sessions[session.session_id] = session
            del self._ceremonies[ceremony_id]

            logger.info(f"Ceremony complete: {ceremony_id} | SOVEREIGN session {session.session_id} created")
            return {
                "success": True,
                "ceremony_complete": True,
                "session_id": session.session_id,
                "authority_level": identity.authority_level,
                "confidence": round(ceremony.confidence_accumulated, 4),
            }

        # Issue new challenge token for next step
        new_token = self._generate_token(32)
        ceremony.challenge_token = new_token

        return {
            "success": True,
            "ceremony_complete": False,
            "step_completed": step,
            "steps_remaining": [s for s in ceremony.steps_required if s not in ceremony.steps_completed],
            "challenge_token": new_token,
            "confidence_accumulated": round(ceremony.confidence_accumulated, 4),
        }

    def _verify_ceremony_step(self, identity_id: str, step: str, response: str) -> bool:
        """Verify a single ceremony step."""
        identity = self._identities.get(identity_id)
        if identity is None:
            return False

        if step == "confirm_identity":
            # Must provide full name
            return response.lower().strip() == identity.full_name.lower().strip()

        elif step == "verify_knowledge":
            # Must pass knowledge challenge
            provided_hash = self._hash_secret(response)
            return hmac.compare_digest(identity.knowledge_hash, provided_hash)

        elif step == "verify_bloodline_position":
            # Must state correct bloodline position
            return response.upper().strip() == identity.bloodline_position.upper().strip()

        elif step == "authorize_sovereign_action":
            # Must provide the authorization phrase
            expected = f"I, {identity.full_name}, authorize this SOVEREIGN action"
            return response.strip().lower() == expected.lower()

        elif step == "sovereign_confirmation":
            # Final confirmation — must match DOB
            return response.strip() == identity.dob

        return False

    # ─── EMERGENCY LOCKOUT ───────────────────────────────────────────────

    def emergency_lockout(self, request: LockoutRequest) -> dict[str, Any]:
        """Activate emergency lockout — revoke ALL sessions except emergency recovery."""
        # Validate commander session
        cmd_session = self._sessions.get(request.commander_session_id)
        if cmd_session is None:
            return {"success": False, "error": "Commander session not found"}
        if cmd_session.authority_level < SOVEREIGN_LEVEL:
            return {"success": False, "error": "Only SOVEREIGN can initiate emergency lockout"}

        # Revoke all sessions
        revoked_count = 0
        for sid, session in self._sessions.items():
            if sid == request.commander_session_id and request.preserve_emergency_recovery:
                self._emergency_recovery_sessions.add(sid)
                continue
            if not session.is_revoked:
                session.is_revoked = True
                revoked_count += 1

        # Revoke all delegations
        delegation_revoked = 0
        for delegation in self._delegations.values():
            if not delegation.is_revoked:
                delegation.is_revoked = True
                delegation_revoked += 1

        # Invalidate all ceremonies
        ceremony_count = len(self._ceremonies)
        self._ceremonies.clear()

        # Set global lockout
        self._global_lockout = True
        self._lockout_reason = request.reason

        logger.critical(
            f"EMERGENCY LOCKOUT ACTIVATED | reason={request.reason} | "
            f"sessions_revoked={revoked_count} | delegations_revoked={delegation_revoked} | "
            f"ceremonies_cancelled={ceremony_count}"
        )

        return {
            "success": True,
            "lockout_active": True,
            "reason": request.reason,
            "sessions_revoked": revoked_count,
            "delegations_revoked": delegation_revoked,
            "ceremonies_cancelled": ceremony_count,
            "emergency_recovery_preserved": request.preserve_emergency_recovery,
            "recovery_session_id": request.commander_session_id if request.preserve_emergency_recovery else None,
        }

    def lift_lockout(self, commander_session_id: str) -> dict[str, Any]:
        """Lift emergency lockout. Only callable from emergency recovery session."""
        if commander_session_id not in self._emergency_recovery_sessions:
            return {"success": False, "error": "Only emergency recovery sessions can lift lockout"}

        self._global_lockout = False
        self._lockout_reason = ""
        self._emergency_recovery_sessions.clear()
        logger.info("Emergency lockout lifted")
        return {"success": True, "lockout_lifted": True}

    # ─── DEAD MAN'S SWITCH ───────────────────────────────────────────────

    def dead_man_heartbeat(self, request: HeartbeatRequest) -> dict[str, Any]:
        """Record a heartbeat from the Commander for the dead man's switch."""
        session = self._sessions.get(request.commander_session_id)
        if session is None:
            return {"success": False, "error": "Session not found"}
        if session.identity_id != "CMDR-001":
            return {"success": False, "error": "Dead man's switch heartbeat requires Commander identity"}

        self._dead_man_switch.last_heartbeat = datetime.now(timezone.utc).isoformat()
        self._dead_man_switch.succession_triggered = False

        logger.debug(f"Dead man's switch heartbeat received: {request.message}")

        hours_remaining = self._dead_man_switch.timeout_hours
        return {
            "success": True,
            "last_heartbeat": self._dead_man_switch.last_heartbeat,
            "timeout_hours": hours_remaining,
            "switch_armed": self._dead_man_switch.is_armed,
            "succession_triggered": False,
        }

    def check_dead_man_switch(self) -> dict[str, Any]:
        """Check if the dead man's switch has been triggered."""
        if not self._dead_man_switch.is_armed:
            return {"armed": False, "triggered": False}

        last_hb = datetime.fromisoformat(self._dead_man_switch.last_heartbeat)
        elapsed_hours = (datetime.now(timezone.utc) - last_hb).total_seconds() / 3600
        timeout = self._dead_man_switch.timeout_hours

        if elapsed_hours >= timeout and not self._dead_man_switch.succession_triggered:
            self._dead_man_switch.succession_triggered = True
            self._trigger_succession()
            logger.critical(
                f"DEAD MAN'S SWITCH TRIGGERED | elapsed={elapsed_hours:.1f}h | timeout={timeout}h"
            )

        return {
            "armed": self._dead_man_switch.is_armed,
            "triggered": self._dead_man_switch.succession_triggered,
            "last_heartbeat": self._dead_man_switch.last_heartbeat,
            "elapsed_hours": round(elapsed_hours, 2),
            "timeout_hours": timeout,
            "hours_remaining": round(max(timeout - elapsed_hours, 0), 2),
            "designated_heir": self._dead_man_switch.designated_heir_id,
        }

    def _trigger_succession(self) -> None:
        """Trigger the succession protocol when dead man's switch fires."""
        heir_id = self._dead_man_switch.designated_heir_id
        heir = self._identities.get(heir_id)
        if heir is None:
            logger.error(f"Succession failed: heir {heir_id} not found")
            return

        # Activate heir
        heir.is_active = True
        logger.critical(f"SUCCESSION PROTOCOL ACTIVATED | heir={heir.full_name} | level={heir.authority_level}")

    # ─── IDENTITY MANAGEMENT ─────────────────────────────────────────────

    def register_identity(self, identity: BloodlineIdentity, registrar_session_id: str) -> dict[str, Any]:
        """Register a new identity in the bloodline registry."""
        registrar = self._sessions.get(registrar_session_id)
        if registrar is None:
            return {"success": False, "error": "Registrar session not found"}
        if registrar.authority_level < AuthorityLevel.COMMANDER_DELEGATE:
            return {"success": False, "error": "Insufficient authority to register identities"}
        if identity.authority_level >= registrar.authority_level:
            return {"success": False, "error": "Cannot register identity at or above your own level"}

        if identity.knowledge_hash:
            identity.knowledge_hash = self._hash_secret(identity.knowledge_hash)

        self._identities[identity.identity_id] = identity
        logger.info(f"Identity registered: {identity.identity_id} | {identity.full_name} | level={identity.authority_level}")
        return {
            "success": True,
            "identity_id": identity.identity_id,
            "full_name": identity.full_name,
            "authority_level": identity.authority_level,
        }

    def list_identities(self, session_id: str) -> dict[str, Any]:
        """List all registered identities (requires manage_sessions capability)."""
        session = self._sessions.get(session_id)
        if session is None:
            return {"success": False, "error": "Session not found"}
        level = int(session.authority_level)
        if not AuthorityHardening.check_capability(level, "manage_sessions"):
            return {"success": False, "error": "Insufficient authority"}

        identities = []
        for ident in self._identities.values():
            identities.append({
                "identity_id": ident.identity_id,
                "full_name": ident.full_name,
                "authority_level": ident.authority_level,
                "role": ident.role,
                "bloodline_position": ident.bloodline_position,
                "is_active": ident.is_active,
            })
        return {"success": True, "identities": identities, "count": len(identities)}

    # ─── STATUS ───────────────────────────────────────────────────────────

    def get_status(self) -> dict[str, Any]:
        """Get comprehensive authenticator status."""
        self._clean_expired_sessions()
        active_sessions = sum(1 for s in self._sessions.values() if not s.is_revoked)
        active_delegations = sum(1 for d in self._delegations.values() if not d.is_revoked)

        return {
            "engine_id": ENGINE_ID,
            "engine_name": ENGINE_NAME,
            "version": ENGINE_VERSION,
            "authority_level": AUTHORITY_LEVEL,
            "identities_registered": len(self._identities),
            "active_sessions": active_sessions,
            "total_sessions": len(self._sessions),
            "active_delegations": active_delegations,
            "active_ceremonies": len(self._ceremonies),
            "global_lockout": self._global_lockout,
            "dead_man_switch": {
                "armed": self._dead_man_switch.is_armed,
                "triggered": self._dead_man_switch.succession_triggered,
                "last_heartbeat": self._dead_man_switch.last_heartbeat,
            },
        }


# ═══════════════════════════════════════════════════════════════════════════════
# FASTAPI APPLICATION [TIE-17]
# ═══════════════════════════════════════════════════════════════════════════════

# Global instances
doctrine_cache_data: dict[str, Any] = {}
semantic_dict_data: dict[str, Any] = {}
coverage_map_data: dict[str, Any] = {}

three_layer: ThreeLayerResponse | None = None
authenticator: BloodlineAuthenticator | None = None
telemetry: TelemetryCollector | None = None
drift_watcher: DriftWatcher | None = None
coverage_map: CoverageMap | None = None
metrics: MetricsCollector | None = None
audit_trail: AuditTrail | None = None
zoned_analyzer: ZonedAnalyzer | None = None
vector_search: VectorSearchEngine | None = None
deep_analyzer: DeepAnalyzer | None = None
normalizer: SemanticNormalizer | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: initialize all TIE components on startup."""
    global doctrine_cache_data, semantic_dict_data, coverage_map_data
    global three_layer, authenticator, telemetry, drift_watcher
    global coverage_map, metrics, audit_trail, zoned_analyzer
    global vector_search, deep_analyzer, normalizer

    logger.info(f"Starting {ENGINE_NAME} v{ENGINE_VERSION} on port {ENGINE_PORT}")

    # Load data files
    doctrine_cache_data = load_doctrine_cache()
    semantic_dict_data = load_semantic_dict()

    if COVERAGE_MAP_PATH.exists():
        with COVERAGE_MAP_PATH.open("r", encoding="utf-8") as fh:
            coverage_map_data = json.load(fh)
    else:
        coverage_map_data = {"topics": {}}

    # Initialize TIE components
    three_layer = ThreeLayerResponse(doctrine_cache_data, semantic_dict_data)
    authenticator = BloodlineAuthenticator()
    telemetry = TelemetryCollector()
    drift_watcher = DriftWatcher()
    coverage_map = CoverageMap(coverage_map_data)
    metrics = MetricsCollector()
    audit_trail = AuditTrail(AUDIT_LOG_PATH)
    zoned_analyzer = ZonedAnalyzer()
    vector_search = VectorSearchEngine(doctrine_cache_data.get("doctrines", []))
    deep_analyzer = DeepAnalyzer(doctrine_cache_data, semantic_dict_data)
    normalizer = SemanticNormalizer(semantic_dict_data)

    # Set drift baseline
    drift_watcher.set_baseline({
        "auth_success_rate": 0.85,
        "avg_confidence": 0.75,
        "ceremony_rate": 0.05,
        "delegation_rate": 0.10,
        "lockout_rate": 0.01,
    })

    logger.info(f"{ENGINE_NAME} initialized — {len(doctrine_cache_data.get('doctrines', []))} doctrines loaded")

    yield

    logger.info(f"{ENGINE_NAME} shutting down")


app = FastAPI(
    title=f"BLD01 — {ENGINE_NAME}",
    description="Supreme authentication for the McWilliams Bloodline",
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


# ═══════════════════════════════════════════════════════════════════════════════
# MIDDLEWARE — Request tracking
# ═══════════════════════════════════════════════════════════════════════════════

@app.middleware("http")
async def tracking_middleware(request: Request, call_next):
    """Track every request for telemetry and audit."""
    start = time.monotonic()
    query_id = str(uuid.uuid4())
    request.state.query_id = query_id

    response: Response = await call_next(request)

    latency_ms = (time.monotonic() - start) * 1000
    endpoint = request.url.path
    is_error = response.status_code >= 400

    if metrics:
        metrics.record_request(endpoint, latency_ms, is_error)
    if telemetry:
        telemetry.trace_query(query_id, endpoint, latency_ms, response.status_code)

    return response


# ═══════════════════════════════════════════════════════════════════════════════
# [TIE-12] HEALTH ENDPOINT
# ═══════════════════════════════════════════════════════════════════════════════

@app.get("/health")
async def health_check() -> dict[str, Any]:
    """Comprehensive health check endpoint."""
    auth_status = authenticator.get_status() if authenticator else {}
    tlr_stats = three_layer.get_stats() if three_layer else {}
    telemetry_stats = telemetry.get_stats() if telemetry else {}
    metrics_data = metrics.get_metrics() if metrics else {}
    drift_status = drift_watcher.get_status() if drift_watcher else {}
    coverage_data = coverage_map.get_coverage() if coverage_map else {}
    audit_stats = audit_trail.get_stats() if audit_trail else {}

    return {
        "status": "healthy",
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "version": ENGINE_VERSION,
        "tier": ENGINE_TIER,
        "mode": ENGINE_MODE,
        "port": ENGINE_PORT,
        "authority_level": AUTHORITY_LEVEL,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "authenticator": auth_status,
        "three_layer": tlr_stats,
        "telemetry": telemetry_stats,
        "metrics": metrics_data,
        "drift": drift_status,
        "coverage": coverage_data,
        "audit": audit_stats,
        "determinism_hash": compute_determinism_hash({
            "engine": ENGINE_ID,
            "version": ENGINE_VERSION,
            "status": "healthy",
        }),
    }


# ═══════════════════════════════════════════════════════════════════════════════
# AUTHENTICATION ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@app.post("/authenticate")
async def authenticate_endpoint(request: AuthenticateRequest) -> dict[str, Any]:
    """Authenticate an identity and create a session."""
    start = time.monotonic()

    result = authenticator.authenticate(request)

    latency_ms = (time.monotonic() - start) * 1000
    success = result.get("success", False)

    # Telemetry
    telemetry.trace_auth_event(
        event_type="authenticate",
        identity=request.identity_id,
        success=success,
        level=result.get("authority_level"),
    )
    metrics.record_auth_event(success)

    # Drift observation
    drift_watcher.observe("auth_success_rate", 1.0 if success else 0.0)
    if success:
        drift_watcher.observe("avg_confidence", result.get("confidence", 0.0))

    # Audit trail
    audit_trail.log("authenticate", {
        "identity_id": request.identity_id,
        "success": success,
        "authority_level": result.get("authority_level"),
        "factors": result.get("factors_verified", []),
        "confidence": result.get("confidence"),
        "latency_ms": round(latency_ms, 2),
    })

    result["determinism_hash"] = compute_determinism_hash({
        "identity_id": request.identity_id,
        "success": success,
        "authority_level": result.get("authority_level"),
    })
    return result


@app.post("/authenticate/validate")
async def validate_session_endpoint(session_id: str) -> dict[str, Any]:
    """Validate an existing session."""
    result = authenticator.validate_session(session_id)
    audit_trail.log("validate_session", {"session_id": session_id, "valid": result.get("valid", False)})
    return result


@app.post("/authenticate/revoke")
async def revoke_session_endpoint(session_id: str, revoker_session_id: str) -> dict[str, Any]:
    """Revoke a session."""
    result = authenticator.revoke_session(session_id, revoker_session_id)
    audit_trail.log("revoke_session", {
        "session_id": session_id,
        "revoker_session_id": revoker_session_id,
        "success": result.get("success", False),
    })
    return result


# ═══════════════════════════════════════════════════════════════════════════════
# DELEGATION ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@app.post("/delegate")
async def delegate_endpoint(request: DelegateRequest) -> dict[str, Any]:
    """Delegate authority to another identity."""
    result = authenticator.delegate(request)
    success = result.get("success", False)

    telemetry.trace_auth_event(
        event_type="delegate",
        identity=request.delegate_id,
        success=success,
        level=result.get("max_level"),
    )
    drift_watcher.observe("delegation_rate", 1.0 if success else 0.0)

    audit_trail.log("delegate", {
        "delegator_session_id": request.delegator_session_id,
        "delegate_id": request.delegate_id,
        "max_level": request.max_level,
        "scope": request.scope,
        "success": success,
    })

    return result


# ═══════════════════════════════════════════════════════════════════════════════
# BLOODLINE VERIFICATION ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@app.post("/verify-bloodline")
async def verify_bloodline_endpoint(request: BloodlineVerifyRequest) -> dict[str, Any]:
    """Verify bloodline membership and authenticate."""
    result = authenticator.verify_bloodline(request)
    verified = result.get("verified", False)

    telemetry.trace_auth_event(
        event_type="verify_bloodline",
        identity=request.identity_id,
        success=verified,
    )

    audit_trail.log("verify_bloodline", {
        "identity_id": request.identity_id,
        "challenge_type": request.challenge_type,
        "verified": verified,
    })

    return result


# ═══════════════════════════════════════════════════════════════════════════════
# CEREMONY ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@app.post("/ceremony/initiate")
async def initiate_ceremony_endpoint(identity_id: str) -> dict[str, Any]:
    """Initiate an authentication ceremony for SOVEREIGN operations."""
    result = authenticator._initiate_ceremony(identity_id)
    drift_watcher.observe("ceremony_rate", 1.0)

    audit_trail.log("ceremony_initiate", {
        "identity_id": identity_id,
        "ceremony_id": result.get("ceremony_id"),
        "initiated": result.get("ceremony_initiated", False),
    })

    return result


@app.post("/ceremony/advance")
async def advance_ceremony_endpoint(
    ceremony_id: str,
    step: str,
    response: str,
    challenge_token: str,
) -> dict[str, Any]:
    """Advance a ceremony by completing a step."""
    result = authenticator.advance_ceremony(ceremony_id, step, response, challenge_token)
    success = result.get("success", False)

    audit_trail.log("ceremony_advance", {
        "ceremony_id": ceremony_id,
        "step": step,
        "success": success,
        "ceremony_complete": result.get("ceremony_complete", False),
    })

    return result


# ═══════════════════════════════════════════════════════════════════════════════
# EMERGENCY ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@app.post("/lockout")
async def lockout_endpoint(request: LockoutRequest) -> dict[str, Any]:
    """Activate emergency lockout."""
    result = authenticator.emergency_lockout(request)
    drift_watcher.observe("lockout_rate", 1.0 if result.get("success") else 0.0)

    audit_trail.log("emergency_lockout", {
        "reason": request.reason,
        "success": result.get("success", False),
        "sessions_revoked": result.get("sessions_revoked", 0),
    })

    return result


@app.post("/lockout/lift")
async def lift_lockout_endpoint(commander_session_id: str) -> dict[str, Any]:
    """Lift emergency lockout."""
    result = authenticator.lift_lockout(commander_session_id)
    audit_trail.log("lift_lockout", {"success": result.get("success", False)})
    return result


# ═══════════════════════════════════════════════════════════════════════════════
# DEAD MAN'S SWITCH ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@app.post("/dead-man-switch/heartbeat")
async def dead_man_heartbeat_endpoint(request: HeartbeatRequest) -> dict[str, Any]:
    """Record a Commander heartbeat for the dead man's switch."""
    result = authenticator.dead_man_heartbeat(request)

    audit_trail.log("dead_man_heartbeat", {
        "session_id": request.commander_session_id,
        "message": request.message,
        "success": result.get("success", False),
    })

    return result


@app.get("/dead-man-switch/status")
async def dead_man_status_endpoint() -> dict[str, Any]:
    """Check dead man's switch status."""
    return authenticator.check_dead_man_switch()


# ═══════════════════════════════════════════════════════════════════════════════
# IDENTITY MANAGEMENT ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@app.post("/identity/register")
async def register_identity_endpoint(
    identity: BloodlineIdentity,
    registrar_session_id: str,
) -> dict[str, Any]:
    """Register a new identity in the bloodline registry."""
    result = authenticator.register_identity(identity, registrar_session_id)

    audit_trail.log("register_identity", {
        "identity_id": identity.identity_id,
        "full_name": identity.full_name,
        "authority_level": identity.authority_level,
        "registrar_session_id": registrar_session_id,
        "success": result.get("success", False),
    })

    return result


@app.get("/identity/list")
async def list_identities_endpoint(session_id: str) -> dict[str, Any]:
    """List all registered identities."""
    return authenticator.list_identities(session_id)


# ═══════════════════════════════════════════════════════════════════════════════
# THREE-LAYER QUERY ENDPOINT
# ═══════════════════════════════════════════════════════════════════════════════

@app.post("/query")
async def query_endpoint(request: QueryRequest) -> dict[str, Any]:
    """Query the three-layer response system for authentication knowledge."""
    raw = three_layer.resolve(request.query, request.context)

    # Record coverage
    result = raw.get("result", {})
    topic = result.get("topic", "")
    if raw["layer"] == ResponseLayer.DOCTRINE_CACHE.value:
        coverage_map.record_hit(topic)
        metrics.record_cache_event(hit=True)
    else:
        coverage_map.record_miss(request.query)
        metrics.record_cache_event(hit=False)

    formatted = ResponseFormatter.format(raw, request.mode)
    formatted["determinism_hash"] = compute_determinism_hash({
        "query": request.query,
        "layer": raw["layer"],
        "topic": topic,
    })

    audit_trail.log("query", {
        "query": request.query,
        "mode": request.mode.value,
        "layer": raw["layer"],
        "confidence": raw.get("confidence", 0.0),
    })

    return formatted


# ═══════════════════════════════════════════════════════════════════════════════
# DEEP ANALYSIS ENDPOINT
# ═══════════════════════════════════════════════════════════════════════════════

@app.post("/analyze")
async def deep_analysis_endpoint(query: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
    """Perform deep multi-source analysis on an authentication query."""
    result = deep_analyzer.analyze(query, context)

    audit_trail.log("deep_analysis", {
        "query": query,
        "categories": result["decomposition"]["categories_detected"],
        "confidence": result["confidence"],
    })

    return result


# ═══════════════════════════════════════════════════════════════════════════════
# VECTOR SEARCH ENDPOINT
# ═══════════════════════════════════════════════════════════════════════════════

@app.get("/search")
async def vector_search_endpoint(query: str, top_k: int = 5) -> dict[str, Any]:
    """Search authentication doctrines using vector search."""
    results = vector_search.search(query, top_k)
    return {
        "query": query,
        "results": results,
        "count": len(results),
    }


# ═══════════════════════════════════════════════════════════════════════════════
# DRIFT / COVERAGE / METRICS ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@app.get("/drift")
async def drift_endpoint() -> dict[str, Any]:
    """Check for doctrine drift."""
    alerts = drift_watcher.check_drift()
    status = drift_watcher.get_status()
    return {"alerts": alerts, "status": status}


@app.get("/coverage")
async def coverage_endpoint() -> dict[str, Any]:
    """Get doctrine coverage statistics."""
    return coverage_map.get_coverage()


@app.get("/metrics")
async def metrics_endpoint() -> dict[str, Any]:
    """Get comprehensive metrics."""
    return metrics.get_metrics()


@app.get("/telemetry")
async def telemetry_endpoint() -> dict[str, Any]:
    """Get telemetry data."""
    return telemetry.get_stats()


# ═══════════════════════════════════════════════════════════════════════════════
# AUDIT TRAIL ENDPOINT
# ═══════════════════════════════════════════════════════════════════════════════

@app.get("/audit")
async def audit_endpoint(event_type: str | None = None, limit: int = 50) -> dict[str, Any]:
    """Query the audit trail."""
    entries = audit_trail.query(event_type, limit)
    return {
        "entries": entries,
        "count": len(entries),
        "stats": audit_trail.get_stats(),
    }


# ═══════════════════════════════════════════════════════════════════════════════
# AUTHORITY INFO ENDPOINT
# ═══════════════════════════════════════════════════════════════════════════════

@app.get("/authority")
async def authority_endpoint() -> dict[str, Any]:
    """Get authority level information and capability matrix."""
    levels = []
    for level in AuthorityLevel:
        levels.append({
            "level": level.value,
            "name": level.name,
            "weight": AUTHORITY_WEIGHTS.get(level.value, 0.0),
            "capabilities": AUTHORITY_CAPABILITIES.get(level.value, []),
        })
    return {
        "levels": levels,
        "sovereign_level": SOVEREIGN_LEVEL,
        "heir_max_level": HEIR_MAX_LEVEL,
        "delegate_max_level": DELEGATE_MAX_LEVEL,
        "operator_max_level": OPERATOR_MAX_LEVEL,
        "guest_max_level": GUEST_MAX_LEVEL,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# FRAGILITY ANALYSIS ENDPOINT
# ═══════════════════════════════════════════════════════════════════════════════

@app.post("/fragility")
async def fragility_endpoint(
    factor_type: str = "knowledge",
    evidence_strength: float = 0.7,
    independent_corroboration: bool = False,
) -> dict[str, Any]:
    """Score the fragility of an authentication factor."""
    scorer = FactFragilityScorer()
    return scorer.score_factor(factor_type, evidence_strength, independent_corroboration)


# ═══════════════════════════════════════════════════════════════════════════════
# ZONE ANALYSIS ENDPOINT
# ═══════════════════════════════════════════════════════════════════════════════

@app.get("/zones/history")
async def zones_history_endpoint() -> dict[str, Any]:
    """Get zone transition history."""
    return {
        "history": zoned_analyzer.get_history(),
        "active_zone": zoned_analyzer._active_zone.value if zoned_analyzer._active_zone else None,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# SEMANTIC NORMALIZATION ENDPOINT
# ═══════════════════════════════════════════════════════════════════════════════

@app.get("/normalize")
async def normalize_endpoint(text: str) -> dict[str, Any]:
    """Normalize authentication-domain text."""
    normalized = normalizer.normalize(text)
    return {
        "original": text,
        "normalized": normalized,
        "synonyms": normalizer.expand_synonyms(text),
    }


# ═══════════════════════════════════════════════════════════════════════════════
# STATUS / ROOT
# ═══════════════════════════════════════════════════════════════════════════════

@app.get("/")
async def root() -> dict[str, Any]:
    """Engine identification."""
    return {
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "version": ENGINE_VERSION,
        "tier": ENGINE_TIER,
        "mode": ENGINE_MODE,
        "port": ENGINE_PORT,
        "authority_level": AUTHORITY_LEVEL,
        "status": "operational",
        "endpoints": [
            "/health", "/authenticate", "/authenticate/validate", "/authenticate/revoke",
            "/delegate", "/verify-bloodline", "/ceremony/initiate", "/ceremony/advance",
            "/lockout", "/lockout/lift", "/dead-man-switch/heartbeat", "/dead-man-switch/status",
            "/identity/register", "/identity/list", "/query", "/analyze", "/search",
            "/drift", "/coverage", "/metrics", "/telemetry", "/audit",
            "/authority", "/fragility", "/zones/history", "/normalize",
        ],
    }


# ═══════════════════════════════════════════════════════════════════════════════
# [TIE-18] LOGURU LOGGING — Already configured at module top
# ═══════════════════════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    logger.info(f"Launching {ENGINE_NAME} v{ENGINE_VERSION} on port {ENGINE_PORT}")
    uvicorn.run(
        "engine:app",
        host="0.0.0.0",
        port=ENGINE_PORT,
        log_level="info",
        reload=False,
    )
