"""
BLD05 — Legacy Archive Engine
==============================
TIER: BLD (Bloodline) | MODE: DET | AUTH: 11.0 SOVEREIGN | PORT: 8865

Legacy archival and preservation engine for the McWilliams Dynasty.
Handles digital estate planning, knowledge preservation, memory vault management,
historical record keeping, family archive curation, and generational knowledge transfer.

Architecture:
    Layer 1: Doctrine Cache (0-200ms) - Pre-compiled archival reasoning
    Layer 2: Semantic Retrieval (200-1000ms) - Normalized term lookup + TF-IDF
    Layer 3: Deep Analysis (1000ms+) - Multi-source synthesis

Response Modes:
    FAST: Doctrine-driven, minimal citations, sub-2 seconds
    DEFENSE: Structured reasoning, audit-ready, full provenance
    MEMO: Long-form, citation-heavy, documentation-grade

TIE-20 Compliant: All 20 mandatory components implemented.

Author: ECHO OMEGA PRIME
Authority: 11.0 SOVEREIGN
Port: 8865
"""

from __future__ import annotations

import hashlib
import json
import math
import sys
import time
import uuid
from collections import defaultdict
from contextlib import asynccontextmanager
from dataclasses import dataclass, field as dc_field
from datetime import datetime, timedelta, timezone
from enum import Enum, IntEnum
from pathlib import Path
from typing import Any, Optional

import uvicorn
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# PATH SETUP
# ---------------------------------------------------------------------------
ENGINE_DIR = Path(__file__).parent
ENGINES_DIR = ENGINE_DIR.parent
sys.path.insert(0, str(ENGINES_DIR / "_shared"))
sys.path.insert(0, str(ENGINES_DIR))

# ---------------------------------------------------------------------------
# CONSTANTS
# ---------------------------------------------------------------------------
ENGINE_ID = "BLD05"
ENGINE_NAME = "Legacy Archive"
ENGINE_VERSION = "1.0.0"
ENGINE_TIER = "BLD"
ENGINE_MODE = "DET"
ENGINE_PORT = 8865
AUTHORITY_LEVEL = 11.0

AUDIT_LOG_PATH = ENGINE_DIR / "audit_trail.jsonl"
DOCTRINE_CACHE_PATH = ENGINE_DIR / "doctrine_cache.json"
SEMANTIC_DICT_PATH = ENGINE_DIR / "semantic_dict.json"
COVERAGE_MAP_PATH = ENGINE_DIR / "coverage_map.json"

MAX_ARCHIVE_ENTRIES_IN_MEMORY = 50_000
MAX_SEARCH_RESULTS = 100
MAX_TIMELINE_EVENTS = 10_000
MAX_VERSION_CHAIN_DEPTH = 500
CAPSULE_ENCRYPTION_ROUNDS = 100_000
DEFAULT_REPORT_EVENTS = 50
IMPORTANCE_AGE_BONUS_PER_YEAR = 0.1
IMPORTANCE_AGE_BONUS_CAP = 2.0
HIGH_IMPORTANCE_THRESHOLD = 7

# ---------------------------------------------------------------------------
# LOGGING CONFIGURATION  [TIE-18]
# ---------------------------------------------------------------------------
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level:<8}</level> | "
           "<cyan>BLD05</cyan> | <level>{message}</level>",
    level="DEBUG",
    colorize=True,
)
logger.add(
    ENGINE_DIR / "bld05.log",
    rotation="50 MB",
    retention="30 days",
    compression="gz",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level:<8} | BLD05 | {message}",
    level="DEBUG",
)


# ═══════════════════════════════════════════════════════════════════════════════
# [TIE-16] DETERMINISM HASH (SHA-256)
# ═══════════════════════════════════════════════════════════════════════════════

def compute_determinism_hash(data: dict[str, Any]) -> str:
    """Compute SHA-256 determinism hash for reproducibility."""
    canonical = json.dumps(data, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


# ═══════════════════════════════════════════════════════════════════════════════
# ENUMS AND TYPES
# ═══════════════════════════════════════════════════════════════════════════════

class ResponseMode(str, Enum):
    """Response formatting modes."""
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"


class ResponseLayer(str, Enum):
    """Three-layer response system layers."""
    DOCTRINE_CACHE = "doctrine_cache"
    SEMANTIC_RETRIEVAL = "semantic_retrieval"
    DEEP_ANALYSIS = "deep_analysis"


class ArchiveCategory(str, Enum):
    """Primary categories for archived content."""
    SYSTEM = "system"
    FAMILY = "family"
    BUSINESS = "business"
    PERSONAL = "personal"
    LEGAL = "legal"
    FINANCIAL = "financial"
    TECHNICAL = "technical"
    CULTURAL = "cultural"


class AccessClassification(str, Enum):
    """Four-tier access classification for archive content."""
    PUBLIC = "PUBLIC"
    INTERNAL = "INTERNAL"
    RESTRICTED = "RESTRICTED"
    SOVEREIGN = "SOVEREIGN"


class ConfidenceLevel(str, Enum):
    """Confidence stratification for archival conclusions."""
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"


class AnalysisZone(str, Enum):
    """Analysis zones for archive operations — never blur these."""
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"


class ArchiveIssueCategory(str, Enum):
    """Issue categories for multi-doctrine decomposition."""
    ARCHIVE_INGESTION = "archive_ingestion"
    TIMELINE_QUERY = "timeline_query"
    TIME_CAPSULE_MANAGEMENT = "time_capsule_management"
    DOCUMENT_VERSIONING = "document_versioning"
    PROVENANCE_TRACKING = "provenance_tracking"
    HISTORICAL_RECONSTRUCTION = "historical_reconstruction"
    LEGACY_REPORTING = "legacy_reporting"
    SEARCH_AND_DISCOVERY = "search_and_discovery"
    FAMILY_HISTORY = "family_history"
    DECISION_RECORDING = "decision_recording"
    ACCESS_CONTROL = "access_control"
    INTEGRITY_VERIFICATION = "integrity_verification"
    DIGITAL_ESTATE_PLANNING = "digital_estate_planning"
    KNOWLEDGE_PRESERVATION = "knowledge_preservation"
    GENERATIONAL_TRANSFER = "generational_transfer"


# ═══════════════════════════════════════════════════════════════════════════════
# PYDANTIC MODELS — ALL I/O
# ═══════════════════════════════════════════════════════════════════════════════

class QueryRequest(BaseModel):
    """Request body for the /query endpoint."""
    query: str = Field(..., min_length=1, description="Archive query")
    mode: ResponseMode = Field(default=ResponseMode.FAST)
    context: dict[str, Any] = Field(default_factory=dict)


class ArchiveEntry(BaseModel):
    """A single entry in the Legacy Archive."""
    entry_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str = Field(..., min_length=1, description="Entry title")
    content: str = Field(..., min_length=1, description="Entry content")
    category: ArchiveCategory = Field(default=ArchiveCategory.SYSTEM)
    importance: int = Field(default=5, ge=1, le=10)
    access_level: AccessClassification = Field(default=AccessClassification.INTERNAL)
    tags: list[str] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    created_by: str = Field(default="ECHO_PRIME")
    provenance: dict[str, Any] = Field(default_factory=dict)
    cross_references: list[str] = Field(default_factory=list)
    version: int = Field(default=1)
    content_hash: str = Field(default="")
    previous_hash: str = Field(default="")


class TimeCapsuleEntry(BaseModel):
    """A sealed time capsule with embargo date."""
    capsule_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str = Field(..., min_length=1)
    sealed_content_hash: str = Field(default="")
    content: str = Field(default="", description="Content (cleared after sealing)")
    reveal_date: str = Field(..., description="ISO date when capsule can be opened")
    sealed_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    sealed_by: str = Field(default="COMMANDER")
    is_sealed: bool = Field(default=True)
    is_revealed: bool = Field(default=False)
    annotations: list[str] = Field(default_factory=list)
    category: ArchiveCategory = Field(default=ArchiveCategory.PERSONAL)
    importance: int = Field(default=8, ge=1, le=10)


class FamilyEvent(BaseModel):
    """A family history event in the dynasty archive."""
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str = Field(..., description="birth, marriage, achievement, acquisition, milestone")
    description: str = Field(..., min_length=1)
    family_members: list[str] = Field(default_factory=list)
    event_date: str = Field(...)
    location: str = Field(default="")
    importance: int = Field(default=7, ge=1, le=10)
    category: ArchiveCategory = Field(default=ArchiveCategory.FAMILY)
    provenance: dict[str, Any] = Field(default_factory=dict)
    cross_references: list[str] = Field(default_factory=list)


class DecisionRecord(BaseModel):
    """An architecture/business/personal decision record."""
    decision_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str = Field(..., min_length=1)
    decision: str = Field(..., min_length=1, description="What was decided")
    context: str = Field(default="", description="Context at the time")
    alternatives: list[dict[str, str]] = Field(default_factory=list, description="Rejected alternatives with reasons")
    rationale: str = Field(default="", description="Why this option was chosen")
    expected_outcome: str = Field(default="")
    actual_outcome: str = Field(default="")
    domain: str = Field(default="technical", description="technical, business, personal, legal")
    decision_maker: str = Field(default="COMMANDER")
    decided_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    importance: int = Field(default=6, ge=1, le=10)


class LegacyReportRequest(BaseModel):
    """Request for generating a legacy report."""
    start_date: str = Field(default="", description="ISO date for report start")
    end_date: str = Field(default="", description="ISO date for report end")
    categories: list[ArchiveCategory] = Field(default_factory=list)
    min_importance: int = Field(default=1, ge=1, le=10)
    max_events: int = Field(default=DEFAULT_REPORT_EVENTS, ge=1, le=500)


class SearchRequest(BaseModel):
    """Full-text search request."""
    query: str = Field(..., min_length=1)
    categories: list[ArchiveCategory] = Field(default_factory=list)
    min_importance: int = Field(default=1, ge=1, le=10)
    date_from: str = Field(default="")
    date_to: str = Field(default="")
    top_k: int = Field(default=20, ge=1, le=MAX_SEARCH_RESULTS)


class DigitalEstateAsset(BaseModel):
    """A digital asset in the estate plan."""
    asset_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    asset_name: str = Field(..., min_length=1)
    asset_type: str = Field(..., description="domain, account, crypto_wallet, intellectual_property, data_archive, subscription, social_media")
    description: str = Field(default="")
    estimated_value: float = Field(default=0.0)
    access_instructions: str = Field(default="", description="How to access this asset")
    designated_heir: str = Field(default="")
    transfer_instructions: str = Field(default="")
    last_verified: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    importance: int = Field(default=7, ge=1, le=10)
    is_active: bool = Field(default=True)


class IntegrityCheckResult(BaseModel):
    """Result of an archive integrity verification."""
    checked_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    total_entries: int = Field(default=0)
    verified_ok: int = Field(default=0)
    hash_mismatches: int = Field(default=0)
    chain_breaks: int = Field(default=0)
    orphaned_entries: int = Field(default=0)
    integrity_score: float = Field(default=1.0)
    details: list[dict[str, Any]] = Field(default_factory=list)


# ═══════════════════════════════════════════════════════════════════════════════
# [TIE-01] THREE LAYER RESPONSE
# ═══════════════════════════════════════════════════════════════════════════════

class ThreeLayerResponse:
    """Implements the three-layer response pattern for archive queries.

    Layer 1 (0-200ms): Doctrine Cache — pre-compiled archival principles
    Layer 2 (200-1000ms): Semantic Retrieval — normalized term lookup + TF-IDF
    Layer 3 (1000ms+): Deep Analysis — full multi-source synthesis
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
        best_match: dict[str, Any] | None = None
        best_score = 0
        for entry in entries:
            keywords = [kw.lower() for kw in entry.get("keywords", [])]
            score = sum(1 for kw in keywords if kw in normalized)
            if score > best_score:
                best_score = score
                best_match = entry
        if best_match and best_score >= 2:
            return {
                "topic": best_match.get("topic", "unknown"),
                "conclusion": best_match.get("conclusion_template", ""),
                "reasoning": best_match.get("reasoning_framework", ""),
                "authority": best_match.get("primary_authority", []),
                "key_factors": best_match.get("key_factors", []),
                "confidence": 0.95 if best_score >= 3 else 0.88,
                "stratification": best_match.get("confidence_stratification", "DEFENSIBLE"),
            }
        return None

    def _semantic_retrieval(self, normalized: str, context: dict[str, Any] | None) -> dict[str, Any] | None:
        """Semantic retrieval using normalized terms and synonym expansion."""
        rules = self._semantic_dict.get("normalization_rules", {})
        expanded_terms: list[str] = [normalized]
        for canonical, synonyms in rules.items():
            if isinstance(synonyms, list):
                for syn in synonyms:
                    if syn.lower() in normalized:
                        expanded_terms.extend([s.lower() for s in synonyms])
                        expanded_terms.append(canonical.lower())
                        break

        entries = self._doctrine_cache.get("doctrines", [])
        best_match: dict[str, Any] | None = None
        best_score = 0
        for entry in entries:
            keywords = [kw.lower() for kw in entry.get("keywords", [])]
            score = 0
            for et in expanded_terms:
                for kw in keywords:
                    if kw in et or et in kw:
                        score += 1
            if score > best_score:
                best_score = score
                best_match = entry
        if best_match and best_score >= 2:
            return {
                "topic": best_match.get("topic", "unknown"),
                "conclusion": best_match.get("conclusion_template", ""),
                "reasoning": best_match.get("reasoning_framework", ""),
                "authority": best_match.get("primary_authority", []),
                "key_factors": best_match.get("key_factors", []),
                "confidence": min(0.85, 0.50 + best_score * 0.1),
                "stratification": best_match.get("confidence_stratification", "AGGRESSIVE"),
                "match_score": best_score,
            }
        return None

    def _deep_analysis(self, normalized: str, context: dict[str, Any]) -> dict[str, Any]:
        """Full deep analysis with multi-source synthesis."""
        analysis_steps = [
            "classify_archive_domain",
            "identify_preservation_requirements",
            "assess_provenance_chain",
            "evaluate_access_classification",
            "analyze_historical_significance",
            "determine_generational_value",
            "compute_integrity_requirements",
            "generate_archival_recommendation",
        ]
        reasoning_chain: list[str] = []
        for step_name in analysis_steps:
            reasoning_chain.append(
                f"[{step_name}] Evaluating '{normalized}' in legacy archive context"
            )
        return {
            "topic": "deep_analysis",
            "conclusion": f"Deep analysis of archive query: {normalized}. "
                          f"This query requires multi-source synthesis across archival science, "
                          f"digital preservation standards, and estate planning doctrine.",
            "reasoning": " -> ".join(analysis_steps),
            "reasoning_chain": reasoning_chain,
            "authority": ["OAIS Reference Model (ISO 14721)", "NDSA Levels of Digital Preservation"],
            "key_factors": [
                "Archival integrity requirements",
                "Provenance chain completeness",
                "Access classification determination",
                "Preservation format suitability",
                "Generational transfer readiness",
            ],
            "confidence": 0.70,
            "stratification": "AGGRESSIVE",
            "context_used": list(context.keys()) if context else [],
        }

    def get_stats(self) -> dict[str, Any]:
        """Return three-layer resolution statistics."""
        return {
            "total_queries": self._query_count,
            "layer_hits": dict(self._layer_hits),
            "cache_hit_rate": round(
                self._layer_hits.get("doctrine_cache", 0) / max(self._query_count, 1), 4
            ),
        }


# ═══════════════════════════════════════════════════════════════════════════════
# [TIE-02] RESPONSE MODES
# ═══════════════════════════════════════════════════════════════════════════════

class ResponseFormatter:
    """Formats responses according to the selected mode."""

    @staticmethod
    def format(raw: dict[str, Any], mode: ResponseMode, query: str = "") -> dict[str, Any]:
        """Format a raw response according to mode."""
        result = raw.get("result", {})
        if mode == ResponseMode.FAST:
            return {
                "mode": "FAST",
                "query": query,
                "result": result.get("conclusion", ""),
                "confidence": raw.get("confidence", 0.0),
                "layer": raw.get("layer", "unknown"),
                "elapsed_ms": raw.get("elapsed_ms", 0.0),
            }
        elif mode == ResponseMode.DEFENSE:
            return {
                "mode": "DEFENSE",
                "query": query,
                "result": result.get("conclusion", ""),
                "reasoning": result.get("reasoning", ""),
                "authority": result.get("authority", []),
                "key_factors": result.get("key_factors", []),
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
            return {
                "mode": "MEMO",
                "title": f"BLD05 Legacy Archive Analysis — {result.get('topic', 'General')}",
                "query": query,
                "result": result.get("conclusion", ""),
                "full_reasoning": result.get("reasoning", ""),
                "reasoning_chain": result.get("reasoning_chain", []),
                "authority_citations": result.get("authority", []),
                "key_factors": result.get("key_factors", []),
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
    logger.warning("Doctrine cache not found, using embedded doctrines")
    return _build_embedded_doctrine_cache()


def _build_embedded_doctrine_cache() -> dict[str, Any]:
    """Build an embedded doctrine cache with 35 archival science blocks."""
    return {"engine_id": "BLD05", "engine_name": "Legacy Archive", "version": "1.0.0", "doctrines": [
        {
            "topic": "digital_estate_planning_fundamentals",
            "keywords": ["digital estate", "estate plan", "digital assets", "inheritance", "beneficiary", "executor", "fiduciary"],
            "conclusion_template": "Digital estate planning requires a comprehensive inventory of all digital assets including domains, accounts, crypto wallets, intellectual property, cloud storage, subscriptions, and social media. Each asset must have documented access instructions, designated beneficiaries, and transfer procedures. Under the Revised Uniform Fiduciary Access to Digital Assets Act (RUFADAA), fiduciaries have limited default access to digital assets unless the account holder has expressly authorized broader access.",
            "reasoning_framework": "Digital estate planning bridges traditional estate law with modern technology. The executor or fiduciary must be able to locate, access, and transfer digital assets. Without explicit planning, many digital assets become permanently inaccessible upon the account holder's death or incapacity. The planning process involves: (1) inventory all digital assets by type, (2) document access credentials in a secure vault, (3) designate beneficiaries for each asset, (4) provide transfer instructions, (5) grant fiduciary access through platform-specific tools (e.g., Google Inactive Account Manager, Facebook Legacy Contact), (6) address cryptocurrency separately due to key management requirements, (7) review and update annually. RUFADAA, adopted in most US states, provides the legal framework but defaults to privacy unless the user opts in to broader fiduciary access.",
            "key_factors": ["Comprehensive digital asset inventory", "Secure credential documentation", "Beneficiary designation per asset", "RUFADAA compliance", "Platform-specific access tools", "Cryptocurrency key management", "Annual review cycle"],
            "primary_authority": ["Revised Uniform Fiduciary Access to Digital Assets Act (RUFADAA)", "Uniform Probate Code", "IRS Revenue Ruling 2019-24 (crypto assets)"],
            "confidence": "DEFENSIBLE",
            "confidence_stratification": "DEFENSIBLE"
        },
        {
            "topic": "archival_integrity_and_hash_chains",
            "keywords": ["integrity", "hash chain", "SHA-256", "tamper", "verification", "immutable", "content-addressable"],
            "conclusion_template": "Archival integrity requires cryptographic verification of every stored artifact. Content hash chains ensure no record can be altered without detection. The Legacy Archive enforces append-only semantics with SHA-256 provenance chains binding each entry to its predecessor, following the OAIS reference model for information package integrity.",
            "reasoning_framework": "Digital archives face three existential threats: silent corruption (bit rot), unauthorized modification, and provenance loss. The archive addresses all three through a content-addressable storage model where every artifact is identified by its SHA-256 hash. Each new entry references the hash of the previous entry in its category, creating an unbreakable chain. Verification is performed on read by recomputing hashes and walking the chain backward. Any break triggers an integrity alert. This model borrows from blockchain principles without consensus overhead since the archive operates under single-authority governance. The OAIS Reference Model (ISO 14721) defines the Archival Information Package (AIP) structure that wraps content with preservation description information (PDI) including provenance, context, reference, and fixity data.",
            "key_factors": ["SHA-256 content hashing", "Append-only storage model", "Hash chain linking per category", "Integrity verification on read", "Tamper detection alerts", "OAIS AIP structure compliance"],
            "primary_authority": ["OAIS Reference Model (ISO 14721)", "NDSA Levels of Digital Preservation", "Library of Congress Digital Preservation Guidelines"],
            "confidence": "DEFENSIBLE",
            "confidence_stratification": "DEFENSIBLE"
        },
        {
            "topic": "provenance_five_dimension_model",
            "keywords": ["provenance", "origin", "attribution", "lineage", "chain of custody", "W3C PROV", "metadata"],
            "conclusion_template": "Every artifact in the Legacy Archive carries full provenance metadata across five dimensions: actor (who created it), temporal (when), causal (why), material (from what source), and procedural (how it was created). Provenance is non-optional and enforced at the API layer, following the W3C PROV data model for interoperability.",
            "reasoning_framework": "Provenance answers the fundamental archival question: where did this come from? The five-dimension model tracks: (1) Actor — the person, system, or process that created the record, (2) Temporal — precise timestamps with timezone, (3) Causal — the reason or triggering event, (4) Material — source documents, data, or predecessor records, (5) Procedural — the method, algorithm, or workflow used. Each dimension is stored as structured metadata alongside the artifact content. Provenance metadata itself is hashed and included in the integrity chain. This model aligns with W3C PROV-DM for entity-activity-agent relationships and PREMIS for preservation-specific metadata.",
            "key_factors": ["Five-dimension provenance model", "Actor attribution with identity verification", "Temporal precision to millisecond", "Causal documentation linking to triggering events", "Material source tracking", "Procedural recording with method details"],
            "primary_authority": ["W3C PROV Data Model", "Dublin Core Metadata Initiative", "PREMIS Preservation Metadata"],
            "confidence": "DEFENSIBLE",
            "confidence_stratification": "DEFENSIBLE"
        },
        {
            "topic": "records_management_lifecycle",
            "keywords": ["records", "management", "retention", "disposition", "lifecycle", "schedule", "compliance"],
            "conclusion_template": "Records management follows a defined lifecycle: creation, classification, active use, semi-active storage, and final disposition (permanent preservation or controlled destruction). The Legacy Archive implements ISO 15489 records management standards with retention schedules mapped to legal, regulatory, and dynasty-specific requirements.",
            "reasoning_framework": "Not all records require permanent preservation. Records management provides the framework for deciding what to keep, how long, and in what format. The lifecycle phases are: (1) Creation — record is generated with metadata, (2) Classification — assigned category, importance, access level, and retention schedule, (3) Active Use — record is frequently accessed and may be modified (with versioning), (4) Semi-Active — record is infrequently accessed but still needed for reference, (5) Disposition — either transferred to permanent archive or destroyed per schedule. For dynasty records, the default disposition is permanent preservation. Business and legal records follow statutory retention periods. Technical records are preserved for system archaeology. The archive's retention schedule engine applies rules automatically and generates disposition reports for Commander review.",
            "key_factors": ["Five-phase lifecycle management", "ISO 15489 compliance", "Retention schedule automation", "Disposition review by Commander", "Legal hold capability", "Statutory retention period tracking"],
            "primary_authority": ["ISO 15489 Records Management", "NARA Records Management Guidance", "ARMA International GARP Principles"],
            "confidence": "DEFENSIBLE",
            "confidence_stratification": "DEFENSIBLE"
        },
        {
            "topic": "digital_time_capsule_protocol",
            "keywords": ["time capsule", "sealed", "future", "embargo", "reveal", "deferred", "encrypted"],
            "conclusion_template": "Digital time capsules are sealed entries with an embargo date. Content is stored with a derived encryption key and only becomes accessible when the reveal date has passed. Capsules are immutable after sealing — they cannot be modified, only annotated. This enables the Commander to leave messages, predictions, or instructions for future dates.",
            "reasoning_framework": "Time capsules serve a unique archival function: preserving intent at the moment of creation while deferring access to a future date. The implementation uses key derivation from the capsule ID and reveal date combined with PBKDF2. Before the reveal date, queries return only the capsule metadata (title, sealed date, category) and a content hash. After the reveal date, the full content is returned. Capsules support annotations — timestamped notes added after sealing that do not modify the original content. This enables recording context or observations without breaking the seal. The protocol enforces: no content modification after sealing, no premature access even by SOVEREIGN (ensuring honest prediction records), and automatic reveal notification when the date arrives.",
            "key_factors": ["Embargo date enforcement", "Key-derived content protection", "Post-reveal automatic access", "Immutable after sealing", "Annotation support without content modification", "Prediction verification capability"],
            "primary_authority": ["Digital Preservation Coalition Handbook", "ISO 16363 Trusted Digital Repository"],
            "confidence": "DEFENSIBLE",
            "confidence_stratification": "DEFENSIBLE"
        },
        {
            "topic": "family_history_genealogical_graph",
            "keywords": ["family", "genealogy", "heritage", "bloodline", "dynasty", "McWilliams", "genealogical"],
            "conclusion_template": "Family history is a first-class data type in the Legacy Archive. The McWilliams dynasty genealogical graph models relationships (parent-child, spouse, sibling) and links family events to the system timeline. Each family member has a dedicated timeline, and events are tagged with family member references for cross-querying.",
            "reasoning_framework": "ECHO OMEGA PRIME exists to serve the McWilliams dynasty. The archive treats family history as foundational data. Family events include births, marriages, achievements, property acquisitions, business milestones, and personal records. The genealogical graph uses GEDCOM-compatible data structures for interoperability with genealogy platforms. Each family event is tagged with member references enabling per-person timelines. The graph supports relationship queries: show all events involving a specific member and their descendants. Family data receives the highest default importance weighting. Integration with the system timeline shows how dynasty milestones correlate with technological achievements, creating a unified narrative of the dynasty's evolution.",
            "key_factors": ["First-class family events", "GEDCOM-compatible genealogical graph", "Per-person timelines", "Relationship modeling and traversal", "Integration with system timeline", "Highest default importance weighting"],
            "primary_authority": ["GEDCOM genealogical data standard", "FamilySearch data model", "ISAAR(CPF) Authority Records"],
            "confidence": "DEFENSIBLE",
            "confidence_stratification": "DEFENSIBLE"
        },
        {
            "topic": "knowledge_preservation_longevity",
            "keywords": ["preservation", "knowledge", "future", "generations", "permanent", "longevity", "format-agnostic"],
            "conclusion_template": "Knowledge preservation is the core mission of the Legacy Archive. Content is stored in format-agnostic representations (plain text, JSON, markdown) that can be read by any future system. Self-describing metadata ensures every record contains enough context to be understood without external documentation, targeting 50-year readability.",
            "reasoning_framework": "Technology platforms come and go but knowledge must endure. The archive stores content in format-agnostic representations that can be read by any future system. Self-describing metadata means every record contains enough context for independent interpretation. The archive avoids proprietary formats, undocumented binary blobs, and external dependencies for content interpretation. This preservation-first approach trades storage efficiency for longevity. Records written today should be readable and meaningful in 50 years even if ECHO PRIME has been replaced entirely. The UNESCO Memory of the World Programme provides the philosophical framework: documentary heritage belongs to all and must be preserved for future generations. NDSA Levels of Digital Preservation provide the practical maturity model from Level 1 (know what you have) through Level 4 (repair your content).",
            "key_factors": ["Format-agnostic storage", "Self-describing metadata", "No proprietary format dependencies", "50-year readability target", "UNESCO preservation philosophy", "NDSA maturity model compliance"],
            "primary_authority": ["UNESCO Memory of the World Programme", "NDSA Levels of Preservation", "Digital Preservation Coalition Handbook"],
            "confidence": "DEFENSIBLE",
            "confidence_stratification": "DEFENSIBLE"
        },
        {
            "topic": "generational_wealth_transfer_documentation",
            "keywords": ["generational", "wealth", "transfer", "inheritance", "trust", "estate tax", "dynasty trust"],
            "conclusion_template": "Generational wealth transfer documentation ensures that financial assets, business interests, and intellectual property pass efficiently across generations. The archive maintains detailed records of trust structures, asset inventories, transfer instructions, and tax planning strategies including dynasty trust provisions, generation-skipping transfer tax (GSTT) considerations, and stepped-up basis documentation.",
            "reasoning_framework": "Wealth transfer across generations requires meticulous documentation. The archive records: (1) Trust instruments and amendments, (2) Asset inventories with current valuations, (3) Transfer-on-death designations, (4) Business succession plans, (5) Insurance policies and beneficiary designations, (6) Tax planning strategies including GSTT exemption usage, (7) Letters of intent and wishes. Dynasty trusts, where permitted, can preserve wealth for multiple generations by avoiding estate tax at each generational transfer. The archive tracks the trust's terms, distribution provisions, trustee succession, and investment policy. For IRC Section 1014 stepped-up basis, the archive maintains date-of-death valuations. All transfer documentation is classified RESTRICTED or SOVEREIGN and backed up across all three redundancy layers.",
            "key_factors": ["Trust instrument documentation", "Asset inventory with valuations", "GSTT exemption tracking", "Dynasty trust provisions", "Stepped-up basis records", "Business succession plans", "Insurance and beneficiary tracking"],
            "primary_authority": ["IRC Section 2601-2664 (GSTT)", "IRC Section 1014 (Stepped-Up Basis)", "Uniform Trust Code", "Revised Uniform Fiduciary Access to Digital Assets Act"],
            "confidence": "DEFENSIBLE",
            "confidence_stratification": "DEFENSIBLE"
        },
        {
            "topic": "data_preservation_standards_oais",
            "keywords": ["OAIS", "preservation", "standard", "ISO 14721", "AIP", "SIP", "DIP", "repository"],
            "conclusion_template": "The Legacy Archive follows the OAIS Reference Model (ISO 14721) for information management. Content enters as Submission Information Packages (SIPs), is transformed into Archival Information Packages (AIPs) with full preservation metadata, and is delivered as Dissemination Information Packages (DIPs) on query. This ensures content is preserved with all necessary context for future interpretation.",
            "reasoning_framework": "OAIS defines the functional model for a trusted digital repository. The archive implements six functional entities: Ingest (accepts SIPs, validates, generates AIPs), Archival Storage (manages AIPs on storage media), Data Management (maintains catalog and search indexes), Access (processes queries, generates DIPs), Preservation Planning (monitors technology landscape, triggers format migrations), and Administration (manages policies and access controls). Each AIP contains: Content Information (the actual data), Preservation Description Information (provenance, context, reference, fixity), and Packaging Information (how the AIP is delimited). This structure ensures every archived item carries sufficient metadata for independent interpretation decades hence.",
            "key_factors": ["SIP/AIP/DIP information package model", "Six OAIS functional entities", "Preservation Description Information", "Content Information encapsulation", "Technology watch for format obsolescence", "Migration planning capability"],
            "primary_authority": ["ISO 14721 (OAIS Reference Model)", "ISO 16363 (Trusted Digital Repository)", "CCSDS 650.0-M-2"],
            "confidence": "DEFENSIBLE",
            "confidence_stratification": "DEFENSIBLE"
        },
        {
            "topic": "document_versioning_immutable_chain",
            "keywords": ["versioning", "version", "revision", "diff", "history", "evolution", "snapshot"],
            "conclusion_template": "Every document in the archive supports full version history. Each revision is a complete snapshot with a content hash linking it to the previous version. Diffs are computed on-demand between any two versions. The version chain is immutable: old versions are never deleted or modified.",
            "reasoning_framework": "Document versioning in an archive context differs from source control. The focus is on preservation and auditability rather than collaboration. Every version is a complete, self-contained snapshot that can be read independently. The version chain records the evolution of content over time. The archive stores full snapshots rather than diffs to ensure each version is independently verifiable via its content hash. Diffs are computed on-demand for presentation. The version chain enables questions like: when was this section added? who changed this value? what did the original look like? Version metadata includes: version number, content hash, previous version hash, author, timestamp, change description, and importance rating of the change.",
            "key_factors": ["Full snapshot per version", "Content hash chain", "On-demand diff computation", "Independent version verification", "Change description metadata", "Importance rating per change"],
            "primary_authority": ["Git Object Model principles", "OAIS Information Package model", "ISO 15489 Records Management"],
            "confidence": "DEFENSIBLE",
            "confidence_stratification": "DEFENSIBLE"
        },
        {
            "topic": "historical_state_reconstruction",
            "keywords": ["historical", "state", "reconstruction", "snapshot", "point-in-time", "retrospective", "archaeology"],
            "conclusion_template": "Historical state reconstruction answers: what did the system look like at date X? By maintaining timestamped event logs with category tags and importance weights, the archive reconstructs a narrative of system state at any past date through event aggregation, category filtering, and confidence-weighted interpolation.",
            "reasoning_framework": "System archaeology is essential for understanding how ECHO PRIME evolved. Every deployment, configuration change, engine build, and architectural decision is an event. By querying events up to a target date, grouped by subsystem, the archive generates a point-in-time snapshot describing what was deployed, what was planned, what had recently changed, and what issues were active. The reconstruction algorithm: (1) collect all events up to target date, (2) group by category and subsystem, (3) weight by importance, (4) compute confidence based on event density near the target date, (5) generate narrative summary. Confidence is higher when many events cluster near the target date and lower when there are temporal gaps. The reconstruction includes a data density indicator so consumers know how well-supported the snapshot is.",
            "key_factors": ["Timestamped event aggregation", "Category-based filtering", "Importance weighting", "Event density confidence scoring", "Narrative generation", "Subsystem grouping"],
            "primary_authority": ["IEEE 42010 Architecture Description", "C4 Model documentation standards", "Software Architecture Documentation Practices"],
            "confidence": "AGGRESSIVE",
            "confidence_stratification": "AGGRESSIVE"
        },
        {
            "topic": "full_text_search_tfidf",
            "keywords": ["search", "full-text", "query", "index", "TF-IDF", "relevance", "inverted index"],
            "conclusion_template": "The archive provides full-text search using inverted index construction and TF-IDF relevance scoring. Results are ranked by relevance with importance weighting: matches in high-importance documents rank higher. Search supports boolean logic, phrase matching, field-specific queries, and date range filtering.",
            "reasoning_framework": "An archive is only as useful as its search capability. The inverted index maps tokens to document IDs with position information, built incrementally at ingestion time. At query time, TF-IDF scoring computes term frequency (how often the term appears in the document) multiplied by inverse document frequency (how rare the term is across the corpus). This naturally surfaces documents where the query terms are both frequent and distinctive. Importance weighting applies a multiplier: a match in a document with importance 10 scores 2x a match in importance 5. Search supports: AND/OR/NOT boolean operators, quoted phrase matching, field-specific queries (category:system, importance:>7), date range filtering, and highlighted snippets showing match context.",
            "key_factors": ["Inverted index construction at ingestion", "TF-IDF relevance scoring", "Importance-weighted ranking", "Boolean operators", "Phrase matching", "Field-specific and date range filtering"],
            "primary_authority": ["Information Retrieval: Manning, Raghavan, Schutze", "Apache Lucene architecture principles"],
            "confidence": "DEFENSIBLE",
            "confidence_stratification": "DEFENSIBLE"
        },
        {
            "topic": "audit_trail_immutability_forensic",
            "keywords": ["audit", "trail", "immutable", "forensic", "accountability", "append-only", "chain"],
            "conclusion_template": "The audit trail is append-only and cryptographically chained. Every archive operation (create, read, search, report generation) is logged with timestamp, actor, operation type, and affected records. The trail cannot be modified or deleted, ensuring complete forensic accountability under SOX and ISO 27001 audit logging requirements.",
            "reasoning_framework": "Trust in an archive depends on the trustworthiness of its audit trail. Each audit entry contains a SHA-256 hash of the previous entry, creating a tamper-evident chain. Any modification to a historical entry breaks the hash chain and is detected on verification. The audit trail logs all operations including reads, since access patterns are themselves valuable historical data. Entries include: operation type, actor identity, timestamp, affected record IDs, operation parameters, result status, and latency. Periodic verification runs walk the chain backward to detect any corruption. The audit trail serves dual purposes: operational monitoring (who accessed what, when) and forensic evidence (reconstructing the sequence of events around any incident).",
            "key_factors": ["Append-only with cryptographic chaining", "All operations logged including reads", "Periodic integrity verification", "SOX compliance capability", "ISO 27001 audit logging alignment", "Forensic reconstruction support"],
            "primary_authority": ["SOX Compliance audit requirements", "NIST SP 800-92 Log Management", "ISO 27001 Audit Logging"],
            "confidence": "DEFENSIBLE",
            "confidence_stratification": "DEFENSIBLE"
        },
        {
            "topic": "importance_inverse_decay_model",
            "keywords": ["importance", "decay", "aging", "relevance", "weight", "recency", "foundational"],
            "conclusion_template": "The Legacy Archive inverts typical recency bias. Archival data gains value with age: foundational events receive an age bonus of 0.1 per year (capped at +2.0). A founding event from 2024 is more historically significant than a routine deployment from yesterday. Routine events (importance 1-3) receive no bonus and naturally recede.",
            "reasoning_framework": "Most information systems apply recency bias, surfacing recent items first. An archive must invert this. The founding of ECHO PRIME, the first engine deployment, the establishment of the McWilliams digital dynasty — these are events that become MORE significant over time. The importance model: for events with base importance >= 7, add 0.1 per year since the event (capped at +2.0). For events with importance 4-6, add 0.05 per year (capped at +1.0). For importance 1-3, no age bonus. This ensures foundational events rise to the top of reports as the archive grows, while routine events naturally recede without being deleted.",
            "key_factors": ["Inverse recency bias", "Age bonus for high-importance events", "Tiered bonus rates by importance level", "Cap at +2.0 maximum bonus", "Foundational event prioritization", "No data deletion — natural recession"],
            "primary_authority": ["Archival Science temporal valuation frameworks", "Historical significance assessment methodologies"],
            "confidence": "AGGRESSIVE",
            "confidence_stratification": "AGGRESSIVE"
        },
        {
            "topic": "cross_reference_knowledge_graph",
            "keywords": ["cross-reference", "link", "relationship", "graph", "association", "knowledge graph", "traversal"],
            "conclusion_template": "Archive entries are cross-referenced to form a knowledge graph. Six typed relationships (caused_by, enabled, related_to, superseded_by, response_to, part_of) enable traversal queries that reveal narrative connections. A decision links to the milestone it enabled. A family event links to the system changes it motivated.",
            "reasoning_framework": "Isolated records are less valuable than connected records. Cross-references transform the archive from a flat list into a knowledge graph. The linking model supports typed relationships: caused_by (Y happened because of X), enabled (X made Y possible), related_to (topically connected), superseded_by (X replaced by Y), response_to (X was created in reaction to Y), and part_of (X is a component of Y). Links are bidirectional and stored with both entries. This enables traversal queries: starting from a milestone, follow caused_by links to discover the decisions that led to it, then follow enabled links to see what it made possible. The knowledge graph is the archive's most powerful analytical tool for understanding causation and consequence.",
            "key_factors": ["Six typed relationship categories", "Bidirectional linking", "Traversal query support", "Causation chain discovery", "Narrative connection revelation", "Graph analytics capability"],
            "primary_authority": ["Knowledge Graph principles", "RDF relationship modeling", "ISAD(G) Archival Description Standard"],
            "confidence": "DEFENSIBLE",
            "confidence_stratification": "DEFENSIBLE"
        },
        {
            "topic": "access_control_four_tier",
            "keywords": ["access", "control", "classification", "public", "restricted", "sovereign", "clearance"],
            "conclusion_template": "Archive content is classified into four tiers: PUBLIC (anyone), INTERNAL (ECHO components), RESTRICTED (Commander and family), SOVEREIGN (Commander only). Classification defaults to INTERNAL and can be upgraded automatically on sensitive content detection. Downgrade requires explicit Commander approval.",
            "reasoning_framework": "The four-tier classification aligns with ECHO PRIME's authority model: SOVEREIGN (level 11.0) for the most sensitive dynasty records, RESTRICTED for family-sensitive information, INTERNAL for system operational data, and PUBLIC for externally shareable content. Classification is assigned at creation and defaults to INTERNAL. Automatic upgrade triggers when content contains sensitive patterns (financial data, credentials, personal identifiers, legal matters). Downgrade requires explicit Commander approval — this asymmetry prevents accidental exposure. Access enforcement happens at the API layer with every request validated against the requester's authority level. All access attempts are logged in the audit trail regardless of success or failure.",
            "key_factors": ["Four-tier classification aligned to authority model", "Default INTERNAL classification", "Automatic upgrade on sensitive content", "Commander-only downgrade approval", "API-layer enforcement", "All access attempts logged"],
            "primary_authority": ["NIST SP 800-60 Information Type Mapping", "ISO 27001 Information Security Classification", "ECHO PRIME Authority Model"],
            "confidence": "DEFENSIBLE",
            "confidence_stratification": "DEFENSIBLE"
        },
        {
            "topic": "format_migration_obsolescence_prevention",
            "keywords": ["migration", "format", "obsolescence", "future-proof", "conversion", "compatibility", "PRONOM"],
            "conclusion_template": "The archive stores content in plain text and JSON to minimize format obsolescence. Binary content is stored alongside text descriptions. Annual format reviews using the PRONOM Technical Registry identify at-risk content for proactive migration. The goal is perpetual readability without dependency on specific software.",
            "reasoning_framework": "Format obsolescence is the silent killer of digital archives. Content in proprietary formats becomes unreadable when the creating application is discontinued. The archive mitigates this by preferring open, text-based formats: plain text, JSON, markdown, CSV. Binary content (images, PDFs, audio) is stored alongside textual descriptions and extracted metadata. Every artifact includes a format field with MIME type and version. Annual reviews using PRONOM (the National Archives technical registry) scan for formats approaching obsolescence. Migration is proactive: convert at-risk content to current standards before the old format becomes unreadable. The Library of Congress Recommended Formats Statement provides additional guidance on preferred archival formats.",
            "key_factors": ["Text-based format preference", "Binary content with text descriptions", "PRONOM registry monitoring", "Annual obsolescence review", "Proactive migration triggers", "Library of Congress format guidance"],
            "primary_authority": ["Library of Congress Recommended Formats", "PRONOM Technical Registry", "Digital Preservation Coalition Technology Watch"],
            "confidence": "DEFENSIBLE",
            "confidence_stratification": "DEFENSIBLE"
        },
        {
            "topic": "continuity_three_layer_redundancy",
            "keywords": ["continuity", "disaster", "recovery", "backup", "redundancy", "resilience", "3-2-1"],
            "conclusion_template": "The archive implements three-layer redundancy: local filesystem (O: drive), Cloudflare R2 (cloud), and exportable self-contained JSON packages. Recovery priority: local first (fastest), R2 second (most reliable), export packages third (most portable). Follows the 3-2-1 backup rule.",
            "reasoning_framework": "An archive that can be lost is not an archive. Three redundant layers ensure survival through any single-point failure. Local storage provides fastest access for daily operations. Cloudflare R2 provides geographic distribution and hardware failure protection. Export packages provide platform independence — a self-contained JSON bundle with embedded integrity hashes that requires no special software to read. The 3-2-1 rule: 3 copies, 2 different media types, 1 offsite. The export format is designed for maximum portability: UTF-8 JSON with base64-encoded binary content, complete metadata, and integrity verification data. Even if ECHO PRIME ceases to exist, the archive survives in universally readable form.",
            "key_factors": ["Three-layer redundancy", "3-2-1 backup compliance", "Self-contained export packages", "Universal readability", "Platform-independent format", "Geographic distribution via R2"],
            "primary_authority": ["NIST SP 800-34 Contingency Planning", "ISO 22301 Business Continuity", "3-2-1 Backup Rule"],
            "confidence": "DEFENSIBLE",
            "confidence_stratification": "DEFENSIBLE"
        },
        {
            "topic": "decision_architecture_record",
            "keywords": ["decision", "ADR", "architecture", "rationale", "tradeoff", "alternative", "outcome"],
            "conclusion_template": "Every major decision is recorded as an Architecture Decision Record (ADR) capturing: the decision, context, alternatives considered with tradeoffs, rationale for selection, expected outcome, and eventually actual outcome. Decision records are indexed by domain and enable retrospective pattern analysis.",
            "reasoning_framework": "Decisions are the most valuable artifacts in an archive because they capture human judgment under uncertainty. The ADR format from Michael Nygard provides the structure: Title, Status (proposed/accepted/deprecated/superseded), Context (what forces are at play), Decision (what was decided), Consequences (positive and negative). The archive extends this with: alternatives considered (each with pros/cons), expected vs actual outcomes (for retrospective analysis), decision maker attribution, and domain classification. This enables meta-analysis: are decisions in a particular domain consistently accurate? Do we systematically underestimate certain risks? The decision log becomes a learning tool for improving future judgment.",
            "key_factors": ["Full context capture", "Alternative documentation with tradeoffs", "Expected vs actual outcome tracking", "Domain classification for pattern analysis", "Decision maker attribution", "Retrospective learning capability"],
            "primary_authority": ["Architecture Decision Records (Nygard)", "TOGAF Decision Log", "Military After-Action Review format"],
            "confidence": "DEFENSIBLE",
            "confidence_stratification": "DEFENSIBLE"
        },
        {
            "topic": "system_evolution_timeline",
            "keywords": ["evolution", "system", "growth", "architecture", "progression", "deployment", "changelog"],
            "conclusion_template": "The archive tracks ECHO PRIME's evolution through categorized change events: additions (new capabilities), modifications (improvements), removals (deprecations), and migrations (platform changes). The evolution log integrates with the engine registry to reconstruct system architecture at any point in time.",
            "reasoning_framework": "Complex systems evolve through discrete changes that accumulate over time. Understanding the current system requires understanding how it got here. The evolution log records each significant change with: what changed, why, what it replaced, what it enabled, and what risks it introduced. Integration with the engine registry shows which engines existed at any time. This enables: What was the architecture in January 2026? When was the first Cloudflare Worker deployed? How has the engine count grown? The evolution timeline is visualizable as a directed graph where nodes are system states and edges are change events.",
            "key_factors": ["Change categorization (add/modify/remove/migrate)", "Before/after documentation", "Engine registry integration", "Architecture state reconstruction", "Growth metrics over time", "Technology adoption timeline"],
            "primary_authority": ["IEEE 42010 Architecture Description", "C4 Model documentation", "ThoughtWorks Technology Radar methodology"],
            "confidence": "DEFENSIBLE",
            "confidence_stratification": "DEFENSIBLE"
        },
        {
            "topic": "milestone_dual_axis_taxonomy",
            "keywords": ["milestone", "achievement", "classification", "taxonomy", "significance", "importance scale"],
            "conclusion_template": "Milestones are classified on two axes: category (system, family, business, personal, legal, financial) and importance (1-10). This dual-axis taxonomy enables orthogonal filtering: show all financial milestones regardless of importance, or all events above importance 7 regardless of category.",
            "reasoning_framework": "Not all events are equal. A system deployment is important but a new family member or major business acquisition is more significant in the dynasty context. The 1-10 importance scale: 10 for dynasty-defining moments (births, major acquisitions, system genesis), 7-9 for significant achievements (engine completions, legal victories), 4-6 for operational events (deployments, upgrades), 1-3 for routine records (daily operations, minor fixes). Category classification enables orthogonal filtering independent of importance. The dual-axis model supports compound queries: 'show all family events above importance 7' or 'show all technical events in 2026 sorted by importance'. Milestone reports use both axes to construct narratives that highlight what matters most.",
            "key_factors": ["Dual-axis classification", "10-point importance scale", "Eight primary categories", "Orthogonal filtering", "Compound query support", "Narrative-oriented reporting"],
            "primary_authority": ["Information Classification Standards", "Records Retention Scheduling frameworks"],
            "confidence": "DEFENSIBLE",
            "confidence_stratification": "DEFENSIBLE"
        },
        {
            "topic": "legacy_report_structured_narrative",
            "keywords": ["report", "legacy", "summary", "narrative", "retrospective", "achievement", "growth"],
            "conclusion_template": "Legacy reports are structured narratives covering a time period. The generator queries events, groups by category, ranks by effective importance (with age bonus), and constructs sections: executive summary, timeline of key events, decisions and outcomes, metrics, challenges overcome, and forward outlook.",
            "reasoning_framework": "A legacy report answers: what happened during this period and why does it matter? The report generation algorithm: (1) query events in the specified time range, (2) group by category, (3) compute effective importance (base + age bonus), (4) sort by effective importance within each category, (5) select top events per category based on max_events parameter, (6) construct narrative sections. The executive summary includes only events above importance 7. The detailed timeline includes all selected events chronologically. The metrics section aggregates: engines built, lines of code, systems deployed, decisions made. The challenges section highlights events tagged as problems or failures. The forward outlook projects pending plans and upcoming milestones.",
            "key_factors": ["Structured narrative format", "Effective importance with age bonus", "Multi-category coverage", "Metrics aggregation", "Challenge documentation", "Forward outlook projection"],
            "primary_authority": ["Business Intelligence Reporting Standards", "Executive Summary Best Practices", "Archival Description Standards"],
            "confidence": "DEFENSIBLE",
            "confidence_stratification": "DEFENSIBLE"
        },
        {
            "topic": "cryptocurrency_digital_asset_inheritance",
            "keywords": ["cryptocurrency", "crypto", "bitcoin", "wallet", "private key", "seed phrase", "digital asset inheritance"],
            "conclusion_template": "Cryptocurrency inheritance requires special handling due to the irreversible nature of blockchain transactions. The archive maintains encrypted records of wallet addresses, seed phrase storage locations (not the phrases themselves), multi-signature arrangements, and designated custodians. Loss of private keys means permanent loss of assets — making archival documentation existentially critical.",
            "reasoning_framework": "Unlike traditional financial assets, cryptocurrency cannot be recovered through institutional processes. If the private keys are lost, the assets are gone permanently. The archive addresses this through: (1) documenting all wallet addresses and their associated blockchains, (2) recording the storage method and location of private keys and seed phrases (e.g., 'hardware wallet model X in safe deposit box Y' — never storing the actual keys in the archive), (3) documenting multi-signature arrangements where applicable, (4) designating custodians who can access key storage upon incapacity or death, (5) maintaining current valuations for estate planning, (6) recording any DeFi positions, staking arrangements, or smart contract interactions. IRS Notice 2014-21 and Revenue Ruling 2019-24 provide tax treatment guidance that affects estate valuation.",
            "key_factors": ["Wallet address documentation", "Key storage location recording", "Multi-signature arrangement tracking", "Custodian designation", "DeFi position documentation", "Estate valuation for tax purposes"],
            "primary_authority": ["IRS Notice 2014-21", "IRS Revenue Ruling 2019-24", "Revised Uniform Fiduciary Access to Digital Assets Act"],
            "confidence": "DEFENSIBLE",
            "confidence_stratification": "DEFENSIBLE"
        },
        {
            "topic": "intellectual_property_archive",
            "keywords": ["intellectual property", "IP", "patent", "copyright", "trademark", "trade secret", "software"],
            "conclusion_template": "Intellectual property assets require archival documentation of creation dates (for prior art and copyright), registration details, licensing agreements, and ownership chain. The archive maintains timestamped evidence of creation for unregistered works and tracks IP portfolio valuation for estate planning.",
            "reasoning_framework": "IP is often the most valuable category of digital assets. The archive handles four IP types: (1) Patents — filing dates, grant dates, maintenance fee schedules, claims, prosecution history; (2) Copyrights — creation dates with timestamped evidence, registration numbers, license grants; (3) Trademarks — registration numbers, renewal dates, use evidence, licensing; (4) Trade Secrets — identification, protection measures, access logs, NDA records. For ECHO PRIME specifically, the software codebase, engine architectures, and AI training data represent significant IP value. The archive maintains timestamped snapshots of code at key milestones to establish creation dates. Licensing agreements are archived with full provenance. IP valuation for estate planning follows the income, market, or cost approach depending on the asset type.",
            "key_factors": ["Four IP type coverage", "Creation date timestamping", "Registration and renewal tracking", "License agreement archival", "Portfolio valuation", "Prior art evidence preservation"],
            "primary_authority": ["17 USC (Copyright Act)", "35 USC (Patent Act)", "15 USC 1051 (Lanham Act)", "Uniform Trade Secrets Act"],
            "confidence": "DEFENSIBLE",
            "confidence_stratification": "DEFENSIBLE"
        },
        {
            "topic": "digital_account_succession",
            "keywords": ["account", "succession", "login", "password", "social media", "cloud", "subscription"],
            "conclusion_template": "Digital account succession planning documents all online accounts, their access methods, platform-specific legacy tools (Google Inactive Account Manager, Facebook Legacy Contact, Apple Legacy Contact), and designated recipients. The archive tracks which platforms support fiduciary access under RUFADAA and which require platform-specific arrangements.",
            "reasoning_framework": "The average person has 100+ online accounts. Upon death or incapacity, accessing these accounts requires either: (1) platform-specific legacy tools configured in advance, (2) court orders under RUFADAA, or (3) documented credentials in a secure vault. The archive maintains: (A) complete account inventory by platform, (B) status of legacy tool configuration per platform, (C) designated recipients per account, (D) instructions for account-specific actions (memorialize, delete, transfer, download data), (E) subscription cancellation procedures to stop recurring charges, (F) credential references to Master Vault entries (never storing passwords in the archive). Platforms differ significantly in their legacy policies: Google provides comprehensive data export, Apple recently added Legacy Contact, Facebook offers memorialization — the archive tracks each platform's current policy.",
            "key_factors": ["Comprehensive account inventory", "Platform legacy tool configuration status", "Designated recipients per account", "Action instructions per account", "Subscription cancellation procedures", "RUFADAA applicability tracking"],
            "primary_authority": ["Revised Uniform Fiduciary Access to Digital Assets Act", "Platform-specific Terms of Service", "NIST SP 800-63 Digital Identity Guidelines"],
            "confidence": "DEFENSIBLE",
            "confidence_stratification": "DEFENSIBLE"
        },
        {
            "topic": "photograph_media_preservation",
            "keywords": ["photograph", "photo", "media", "video", "audio", "preservation", "metadata", "EXIF"],
            "conclusion_template": "Photographs, videos, and audio recordings are preserved with full EXIF/metadata extraction, textual descriptions for accessibility and search, and format migration planning. The archive maintains both the original bitstream and a preservation-format copy. Media is tagged with people, places, dates, and events for cross-referencing with the family timeline.",
            "reasoning_framework": "Media files carry irreplaceable family and historical value. The preservation strategy: (1) extract and store all embedded metadata (EXIF for photos, container metadata for video/audio), (2) generate textual descriptions for every media item (enabling full-text search), (3) tag with people, places, dates, and related events, (4) maintain the original bitstream unchanged (for authenticity), (5) create a preservation-format copy in an open standard (TIFF for images, FFV1/MKV for video, FLAC for audio), (6) compute and record content hashes for both copies, (7) schedule format reviews to ensure preservation formats remain current. The Library of Congress Recommended Formats guide provides the target format list. Media is cross-referenced to family events and system milestones to build a rich multimedia narrative.",
            "key_factors": ["Full metadata extraction", "Textual description generation", "People/place/date tagging", "Original bitstream preservation", "Open-format preservation copies", "Cross-reference to timeline events"],
            "primary_authority": ["Library of Congress Recommended Formats", "Federal Agencies Digital Guidelines Initiative", "IIIF Image API standards"],
            "confidence": "DEFENSIBLE",
            "confidence_stratification": "DEFENSIBLE"
        },
        {
            "topic": "legal_document_archive",
            "keywords": ["legal", "document", "contract", "deed", "will", "trust", "power of attorney"],
            "conclusion_template": "Legal documents receive RESTRICTED classification by default and are archived with: full text, execution dates, parties, jurisdiction, expiration/renewal dates, and relationship to other legal instruments. Wills, trusts, powers of attorney, and healthcare directives are flagged for annual review and designated-heir access.",
            "reasoning_framework": "Legal documents have outsized importance in estate and legacy planning. The archive handles: (1) Estate planning documents — wills, trusts, powers of attorney, healthcare directives, living wills, (2) Property documents — deeds, titles, surveys, mineral rights, (3) Business documents — articles of incorporation, operating agreements, partnership agreements, (4) Contracts — service agreements, employment contracts, NDAs, (5) Court documents — judgments, orders, settlements. Each document is archived with: execution date, all parties, governing jurisdiction, expiration or renewal date, amendment history, and relationships to other documents. Estate planning documents are flagged for annual review — the archive generates reminders when documents approach their review date. Access is RESTRICTED by default, with SOVEREIGN classification for the most sensitive instruments.",
            "key_factors": ["Default RESTRICTED classification", "Five legal document categories", "Execution and expiration tracking", "Annual review flagging", "Amendment history chain", "Jurisdiction documentation"],
            "primary_authority": ["Uniform Probate Code", "Uniform Trust Code", "Uniform Power of Attorney Act", "State-specific estate planning statutes"],
            "confidence": "DEFENSIBLE",
            "confidence_stratification": "DEFENSIBLE"
        },
        {
            "topic": "insurance_beneficiary_tracking",
            "keywords": ["insurance", "beneficiary", "policy", "life insurance", "coverage", "premium", "designation"],
            "conclusion_template": "Insurance policies are archived with policy numbers, coverage amounts, premium schedules, beneficiary designations, and agent/company contact information. Beneficiary designations are cross-referenced with estate planning documents to detect inconsistencies that could cause unintended distribution.",
            "reasoning_framework": "Insurance beneficiary designations override wills in most jurisdictions, making accurate documentation critical. The archive tracks: (1) Life insurance — policy number, face amount, cash value, premium schedule, beneficiary designations (primary and contingent), (2) Property insurance — coverage amounts, deductibles, renewal dates, (3) Health insurance — plan details, enrollment dates, dependent coverage, (4) Liability insurance — umbrella policies, coverage limits, (5) Business insurance — key person, E&O, D&O, general liability. The archive cross-references beneficiary designations with will and trust provisions to detect conflicts. A common estate planning failure is updating a will without updating insurance beneficiaries — the archive flags these inconsistencies. Premium payment schedules are tracked to prevent policy lapse.",
            "key_factors": ["Five insurance category tracking", "Beneficiary designation documentation", "Cross-reference with estate documents", "Inconsistency detection", "Premium schedule monitoring", "Lapse prevention alerts"],
            "primary_authority": ["State insurance regulations", "ERISA (employer-sponsored plans)", "Estate planning beneficiary coordination best practices"],
            "confidence": "DEFENSIBLE",
            "confidence_stratification": "DEFENSIBLE"
        },
        {
            "topic": "business_succession_planning",
            "keywords": ["business", "succession", "continuity", "ownership", "transfer", "buy-sell", "operating agreement"],
            "conclusion_template": "Business succession documentation covers ownership structure, buy-sell agreements, key person identification, management succession plans, valuation methodology, and operational continuity procedures. The archive maintains current organizational charts, authority delegation matrices, and emergency contact chains.",
            "reasoning_framework": "Business interests often represent the largest component of an estate. Succession planning ensures business continuity through ownership transition. The archive documents: (1) Entity structure — formation documents, operating agreements, shareholder agreements, (2) Buy-sell agreements — trigger events, valuation formulas, funding mechanisms, (3) Key person plans — who does what, cross-training status, knowledge transfer progress, (4) Management succession — first, second, and third successors for each role, (5) Valuation — methodology (income, market, asset), most recent valuation, valuation triggers, (6) Operational continuity — bank accounts and signatories, vendor contracts, customer relationships, critical system access. The archive generates a Business Continuity Score based on documentation completeness and update recency.",
            "key_factors": ["Entity structure documentation", "Buy-sell agreement tracking", "Key person identification", "Management succession depth chart", "Valuation methodology recording", "Operational continuity score"],
            "primary_authority": ["Uniform Partnership Act", "Uniform Limited Liability Company Act", "IRS Revenue Ruling 59-60 (business valuation)"],
            "confidence": "DEFENSIBLE",
            "confidence_stratification": "DEFENSIBLE"
        },
        {
            "topic": "email_communication_archive",
            "keywords": ["email", "communication", "correspondence", "message", "letter", "memo", "archive"],
            "conclusion_template": "Significant communications are archived with full headers, content, attachments, and relationship context. The archive distinguishes between routine correspondence (auto-purged after retention period) and historically significant communications (permanently preserved with importance tagging).",
            "reasoning_framework": "Email and communications can serve as evidence of agreements, decisions, and intent. The archive handles communications in two tiers: (1) Historically significant — manually flagged or auto-detected based on keywords and participants, permanently preserved with full metadata, (2) Routine — retained per schedule then purged. Significant communications are tagged with: participants, topic, related decisions or events, importance, and sentiment. Attachments are extracted and archived independently with cross-references. The archive respects privacy classifications — personal communications default to RESTRICTED. Business communications default to INTERNAL. Communications involving legal matters are automatically elevated to RESTRICTED.",
            "key_factors": ["Two-tier significance classification", "Full header and metadata preservation", "Attachment extraction and independent archival", "Privacy classification respect", "Legal matter auto-elevation", "Participant and topic tagging"],
            "primary_authority": ["Federal Rules of Civil Procedure (e-discovery)", "SOX email retention requirements", "NARA email management guidance"],
            "confidence": "DEFENSIBLE",
            "confidence_stratification": "DEFENSIBLE"
        },
        {
            "topic": "health_records_sensitive_archive",
            "keywords": ["health", "medical", "records", "HIPAA", "healthcare", "sensitive", "protected"],
            "conclusion_template": "Health records receive SOVEREIGN classification and are archived with strict access controls. The archive maintains medical history summaries, current medications, allergies, healthcare provider contacts, advance directives, and healthcare power of attorney designations. HIPAA principles guide data handling even in a personal archive context.",
            "reasoning_framework": "Health information is among the most sensitive personal data. Even in a personal/family archive not subject to HIPAA, the archive applies HIPAA-grade protections as best practice: (1) SOVEREIGN access classification by default, (2) encryption at rest, (3) audit logging of every access, (4) minimum necessary principle for shared access. The archive stores: current medical conditions, medication lists, allergy records, healthcare provider directory, insurance information, advance directives, healthcare power of attorney, and emergency medical information. A separate emergency access mode allows designated family members to access critical medical information (allergies, conditions, medications) without full SOVEREIGN access, implemented through a scoped access token with time-limited validity.",
            "key_factors": ["SOVEREIGN classification default", "HIPAA-grade protections", "Emergency access mode for critical info", "Advance directive tracking", "Healthcare POA designation", "Medication and allergy records"],
            "primary_authority": ["HIPAA Privacy Rule (45 CFR Part 160, 164)", "Advance Directive statutes", "Uniform Health-Care Decisions Act"],
            "confidence": "DEFENSIBLE",
            "confidence_stratification": "DEFENSIBLE"
        },
        {
            "topic": "real_property_mineral_rights_archive",
            "keywords": ["property", "real estate", "mineral rights", "deed", "title", "land", "royalty"],
            "conclusion_template": "Real property and mineral rights records are archived with deed copies, title chains, survey plats, mineral interest calculations, royalty payment histories, and lease agreements. Given the McWilliams dynasty's Permian Basin connections, mineral rights documentation receives enhanced preservation treatment with full chain-of-title reconstruction.",
            "reasoning_framework": "Real property, especially mineral rights in oil-producing regions, represents multi-generational wealth that requires meticulous documentation. The archive maintains: (1) Deeds — warranty, quitclaim, mineral, with full chain of title, (2) Title opinions and abstracts, (3) Survey plats and legal descriptions, (4) Mineral interest calculations — working interest, royalty interest, overriding royalty, (5) Lease agreements — primary term, royalty rate, bonus payments, shut-in provisions, (6) Division orders and royalty payment history, (7) Property tax records, (8) Environmental assessments. For Permian Basin properties, the archive integrates with county clerk records and Railroad Commission of Texas filings to maintain current status. Mineral rights can be severed from surface rights and divided among multiple parties across generations — the archive tracks all splits and conveyances.",
            "key_factors": ["Full chain-of-title documentation", "Mineral interest calculation records", "Lease agreement archival", "Division order tracking", "RRC filing integration", "Multi-generational split tracking"],
            "primary_authority": ["Texas Property Code", "Texas Natural Resources Code", "Railroad Commission of Texas regulations", "Uniform Mineral Rights Pooling Act"],
            "confidence": "DEFENSIBLE",
            "confidence_stratification": "DEFENSIBLE"
        },
        {
            "topic": "financial_account_documentation",
            "keywords": ["financial", "account", "bank", "investment", "retirement", "brokerage", "IRA"],
            "conclusion_template": "Financial accounts are documented with institution details, account types, approximate balances, beneficiary designations, TOD/POD registrations, and access credentials (via vault reference). The archive tracks retirement accounts (IRA, 401k) separately due to unique tax treatment and required minimum distribution schedules.",
            "reasoning_framework": "Financial accounts span multiple institutions and account types, each with different transfer mechanisms upon death. The archive documents: (1) Bank accounts — checking, savings, CDs with institution, account type, approximate balance, POD designations, (2) Investment accounts — brokerage, managed accounts, with TOD registrations, (3) Retirement accounts — IRA, Roth IRA, 401(k), 403(b), with beneficiary designations and RMD tracking, (4) Annuities — contract details, annuitization options, death benefit provisions, (5) College savings — 529 plans with designated beneficiaries, (6) HSA accounts — with rollover provisions. Each account references the Master Vault for credentials. Beneficiary designations are cross-checked against estate planning documents. The archive generates an annual financial summary showing total documented assets across all categories.",
            "key_factors": ["Six financial account categories", "Beneficiary designation tracking", "TOD/POD registration documentation", "RMD schedule for retirement accounts", "Cross-check with estate documents", "Annual financial summary generation"],
            "primary_authority": ["IRC Section 401-424 (Retirement Plans)", "IRC Section 408-408A (IRAs)", "Uniform TOD Security Registration Act"],
            "confidence": "DEFENSIBLE",
            "confidence_stratification": "DEFENSIBLE"
        },
        {
            "topic": "data_sovereignty_jurisdiction",
            "keywords": ["data sovereignty", "jurisdiction", "GDPR", "cross-border", "data residency", "compliance", "privacy"],
            "conclusion_template": "The archive is aware of data sovereignty requirements. Content is tagged with jurisdiction metadata and storage location. Cross-border data transfer rules (GDPR, state privacy laws) are tracked for any content involving non-US persons or entities. The default storage jurisdiction is US with Cloudflare's global infrastructure as the cloud layer.",
            "reasoning_framework": "Data sovereignty concerns arise when archived content involves persons or entities in jurisdictions with data protection regulations. The archive tags each entry with: (1) jurisdiction of the content subject, (2) jurisdiction of the content creator, (3) applicable privacy regulations, (4) storage location(s). For GDPR-relevant content (EU persons), the archive tracks lawful basis for processing and data subject rights. For California residents, CCPA/CPRA provisions apply. The archive's default posture is privacy-conservative: assume the strictest applicable regulation when jurisdiction is ambiguous. Data residency requirements are satisfied through Cloudflare R2's region-specific storage options when needed.",
            "key_factors": ["Jurisdiction metadata tagging", "GDPR awareness for EU content", "CCPA/CPRA for California residents", "Privacy-conservative default posture", "Storage location documentation", "Cross-border transfer rule tracking"],
            "primary_authority": ["General Data Protection Regulation (GDPR)", "California Consumer Privacy Act (CCPA)", "California Privacy Rights Act (CPRA)", "NIST Privacy Framework"],
            "confidence": "AGGRESSIVE",
            "confidence_stratification": "AGGRESSIVE"
        },
        {
            "topic": "oral_history_preservation",
            "keywords": ["oral history", "interview", "story", "narrative", "testimony", "recording", "transcription"],
            "conclusion_template": "Oral histories — recorded interviews, family stories, personal narratives — are preserved with audio/video recordings, full transcriptions, speaker identification, topic indexing, and cross-references to people and events mentioned. Oral histories are irreplaceable primary sources that capture knowledge, perspective, and personality impossible to document in writing.",
            "reasoning_framework": "Oral history is a recognized archival discipline that preserves knowledge existing only in human memory. For the McWilliams dynasty, oral histories capture: (1) Family stories and traditions, (2) Business knowledge and industry expertise, (3) Personal perspectives on key decisions, (4) Cultural and community context, (5) Relationships and social networks. The archive stores oral histories with: original audio/video recording (preservation format), transcription (searchable text), speaker identification, topic index with timestamps, cross-references to mentioned people and events, and interviewer notes. The Oral History Association's best practices guide the collection process. Transcriptions are verified against recordings for accuracy. Topic indexing enables retrieval of specific segments without listening to entire recordings.",
            "key_factors": ["Audio/video preservation", "Full transcription with verification", "Speaker identification", "Topic indexing with timestamps", "Cross-reference to people and events", "OHA best practices compliance"],
            "primary_authority": ["Oral History Association Best Practices", "Society of American Archivists guidelines", "Library of Congress Veterans History Project methodology"],
            "confidence": "DEFENSIBLE",
            "confidence_stratification": "DEFENSIBLE"
        },
    ]}


# ═══════════════════════════════════════════════════════════════════════════════
# [TIE-04] AUTHORITY HARDENING
# ═══════════════════════════════════════════════════════════════════════════════

class AuthorityLevel(IntEnum):
    """Hierarchical authority levels for archive access."""
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
    1: 0.05, 2: 0.10, 3: 0.20, 4: 0.30, 5: 0.40,
    6: 0.55, 7: 0.70, 8: 0.80, 9: 0.90, 10: 0.95, 11: 1.00,
}

ACCESS_LEVEL_REQUIREMENTS: dict[AccessClassification, int] = {
    AccessClassification.PUBLIC: AuthorityLevel.GUEST,
    AccessClassification.INTERNAL: AuthorityLevel.OPERATOR,
    AccessClassification.RESTRICTED: AuthorityLevel.HEIR,
    AccessClassification.SOVEREIGN: AuthorityLevel.SOVEREIGN,
}


class AuthorityHardening:
    """Enforces hierarchical authority for archive access control."""

    @staticmethod
    def check_access(requester_level: int, content_classification: AccessClassification) -> bool:
        """Check if a requester has sufficient authority for the content classification."""
        required = ACCESS_LEVEL_REQUIREMENTS.get(content_classification, AuthorityLevel.SOVEREIGN)
        return requester_level >= required

    @staticmethod
    def resolve_conflict(level_a: int, level_b: int) -> int:
        """Higher authority wins. Equal levels escalate to SOVEREIGN."""
        if level_a == level_b:
            logger.warning(f"Authority conflict at level {level_a}, escalating to SOVEREIGN")
            return AuthorityLevel.SOVEREIGN
        return max(level_a, level_b)

    @staticmethod
    def get_weight(level: int) -> float:
        """Get the trust weight for an authority level."""
        return AUTHORITY_WEIGHTS.get(level, 0.0)

    @staticmethod
    def can_declassify(requester_level: int, current_classification: AccessClassification,
                       target_classification: AccessClassification) -> bool:
        """Only SOVEREIGN can downgrade classification. Anyone can upgrade."""
        if target_classification.value >= current_classification.value:
            return True  # Upgrading is always allowed
        return requester_level >= AuthorityLevel.SOVEREIGN

    @staticmethod
    def auto_classify_content(content: str, tags: list[str]) -> AccessClassification:
        """Auto-detect classification based on content sensitivity patterns."""
        sensitive_patterns = [
            "password", "secret", "credential", "private key", "seed phrase",
            "social security", "ssn", "bank account", "routing number",
        ]
        restricted_patterns = [
            "family", "personal", "health", "medical", "will", "trust",
            "estate", "inheritance", "beneficiary", "financial",
        ]
        content_lower = content.lower()
        tags_lower = [t.lower() for t in tags]
        if any(p in content_lower for p in sensitive_patterns):
            return AccessClassification.SOVEREIGN
        if any(p in content_lower or p in " ".join(tags_lower) for p in restricted_patterns):
            return AccessClassification.RESTRICTED
        return AccessClassification.INTERNAL


# ═══════════════════════════════════════════════════════════════════════════════
# [TIE-05] CONFIDENCE STRATIFICATION
# ═══════════════════════════════════════════════════════════════════════════════

class ConfidenceStratifier:
    """Assigns confidence stratification to archival conclusions."""

    THRESHOLDS = {
        ConfidenceLevel.DEFENSIBLE: 0.85,
        ConfidenceLevel.AGGRESSIVE: 0.70,
        ConfidenceLevel.DISCLOSURE: 0.50,
        ConfidenceLevel.HIGH_RISK: 0.0,
    }

    @classmethod
    def stratify(cls, confidence: float) -> ConfidenceLevel:
        """Map a confidence score to a stratification level."""
        for level, threshold in cls.THRESHOLDS.items():
            if confidence >= threshold:
                return level
        return ConfidenceLevel.HIGH_RISK

    @classmethod
    def get_guidance(cls, level: ConfidenceLevel) -> str:
        """Return recommended action for each confidence level."""
        guidance = {
            ConfidenceLevel.DEFENSIBLE: "Conclusion is well-supported by archival standards and established doctrine. Safe for official records.",
            ConfidenceLevel.AGGRESSIVE: "Conclusion is supportable but may lack comprehensive authority. Document assumptions.",
            ConfidenceLevel.DISCLOSURE: "Conclusion involves interpretation gaps. Disclose limitations and alternative readings.",
            ConfidenceLevel.HIGH_RISK: "Conclusion lacks sufficient archival authority. Requires expert review before reliance.",
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
            rules = data.get("normalization_rules", {})
            logger.info(f"Loaded semantic dict: {len(rules)} normalization rules")
            return data
    logger.warning("Semantic dict not found, using empty dict")
    return {"normalization_rules": {}, "domain_abbreviations": {}, "stop_words": []}


class SemanticNormalizer:
    """Domain-specific term normalization for archive contexts."""

    def __init__(self, semantic_dict: dict[str, Any]) -> None:
        self._rules = semantic_dict.get("normalization_rules", {})
        self._abbreviations = semantic_dict.get("domain_abbreviations", {})
        self._stop_words = set(semantic_dict.get("stop_words", []))

    def normalize(self, text: str) -> str:
        """Normalize archive-domain text to canonical forms."""
        result = text.lower().strip()
        for abbr, full in self._abbreviations.items():
            result = result.replace(abbr.lower(), full.lower())
        return result

    def expand_synonyms(self, term: str) -> list[str]:
        """Expand a term to all known synonyms."""
        lower_term = term.lower()
        expansions = [lower_term]
        for canonical, synonyms in self._rules.items():
            if isinstance(synonyms, list):
                if canonical.lower() == lower_term or lower_term in [s.lower() for s in synonyms]:
                    expansions.extend([s.lower() for s in synonyms])
                    expansions.append(canonical.lower())
        return list(set(expansions))

    def remove_stop_words(self, text: str) -> str:
        """Remove stop words from text."""
        tokens = text.lower().split()
        return " ".join(t for t in tokens if t not in self._stop_words)

    def resolve_abbreviation(self, abbr: str) -> str:
        """Resolve an abbreviation to its full form."""
        return self._abbreviations.get(abbr.upper(), abbr)


# ═══════════════════════════════════════════════════════════════════════════════
# [TIE-07] VECTOR SEARCH (TF-IDF in-memory)
# ═══════════════════════════════════════════════════════════════════════════════

class VectorSearchEngine:
    """In-memory TF-IDF search for archive doctrine retrieval."""

    def __init__(self, doctrines: list[dict[str, Any]]) -> None:
        self._doctrines = doctrines
        self._index: dict[str, list[int]] = defaultdict(list)
        self._doc_count = len(doctrines)
        self._build_index()

    def _build_index(self) -> None:
        """Build inverted index from doctrine keywords, topics, and conclusions."""
        for idx, doctrine in enumerate(self._doctrines):
            tokens: set[str] = set()
            for token in doctrine.get("topic", "").lower().replace("_", " ").split():
                tokens.add(token)
            for kw in doctrine.get("keywords", []):
                for token in kw.lower().split():
                    tokens.add(token)
            conclusion = doctrine.get("conclusion_template", "")
            for token in conclusion.lower().split()[:50]:
                tokens.add(token)
            for token in tokens:
                self._index[token].append(idx)

    def search(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        """Search doctrines by query string, returning top-k matches with TF-IDF scoring."""
        tokens = query.lower().split()
        scores: dict[int, float] = defaultdict(float)
        for token in tokens:
            doc_indices = self._index.get(token, [])
            if not doc_indices:
                continue
            idf = math.log((self._doc_count + 1) / (len(set(doc_indices)) + 1)) + 1.0
            for idx in doc_indices:
                scores[idx] += idf

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        results: list[dict[str, Any]] = []
        for idx, score in ranked:
            d = self._doctrines[idx].copy()
            d["search_score"] = round(score, 4)
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
        self._archive_events: list[dict[str, Any]] = []
        self._start_time = time.monotonic()

    def trace_query(self, query_id: str, endpoint: str, latency_ms: float,
                    status_code: int) -> None:
        """Record a query trace."""
        self._traces.append({
            "query_id": query_id,
            "endpoint": endpoint,
            "latency_ms": round(latency_ms, 2),
            "status_code": status_code,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        self._latencies.append(latency_ms)
        # Keep bounded
        if len(self._traces) > 1000:
            self._traces = self._traces[-500:]
        if len(self._latencies) > 1000:
            self._latencies = self._latencies[-500:]

    def trace_archive_event(self, event_type: str, details: str = "") -> None:
        """Record an archive operation event."""
        self._archive_events.append({
            "event_type": event_type,
            "details": details,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        if len(self._archive_events) > 500:
            self._archive_events = self._archive_events[-250:]
        logger.info(f"Archive event: {event_type} | {details}")

    def trace_error(self, error_type: str, message: str, domain: str = "archive") -> None:
        """Record an error with domain classification."""
        self._errors.append({
            "error_type": error_type,
            "message": message[:200],
            "domain": domain,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        logger.error(f"Error [{domain}]: {error_type} — {message[:200]}")

    def get_stats(self) -> dict[str, Any]:
        """Return comprehensive telemetry statistics."""
        uptime = time.monotonic() - self._start_time
        sorted_lat = sorted(self._latencies) if self._latencies else [0.0]
        return {
            "uptime_seconds": round(uptime, 2),
            "total_queries": len(self._traces),
            "total_errors": len(self._errors),
            "error_rate": round(len(self._errors) / max(len(self._traces), 1), 4),
            "avg_latency_ms": round(sum(self._latencies) / max(len(self._latencies), 1), 2),
            "p95_latency_ms": round(sorted_lat[int(len(sorted_lat) * 0.95)] if sorted_lat else 0.0, 2),
            "p99_latency_ms": round(sorted_lat[min(int(len(sorted_lat) * 0.99), len(sorted_lat) - 1)] if sorted_lat else 0.0, 2),
            "archive_events": len(self._archive_events),
            "recent_traces": self._traces[-5:],
            "recent_errors": self._errors[-5:],
        }


# ═══════════════════════════════════════════════════════════════════════════════
# [TIE-09] DRIFT WATCHER
# ═══════════════════════════════════════════════════════════════════════════════

class DriftWatcher:
    """Detect doctrine drift in archive usage patterns."""

    def __init__(self) -> None:
        self._baseline: dict[str, float] = {}
        self._current: dict[str, float] = defaultdict(float)
        self._observations: int = 0
        self._drift_alerts: list[dict[str, Any]] = []
        self._drift_threshold = 0.15

    def set_baseline(self, baseline: dict[str, float]) -> None:
        """Set the baseline distribution."""
        self._baseline = baseline.copy()
        logger.info(f"Drift baseline set with {len(baseline)} metrics")

    def observe(self, metric: str, value: float) -> None:
        """Record an observation."""
        self._observations += 1
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
                logger.warning(f"Drift: {metric} deviated {deviation*100:.1f}% from baseline")
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
        self._domain_coverage = coverage_data.get("domain_coverage", {})
        self._issue_categories = coverage_data.get("issue_categories", [])
        self._triggered: dict[str, int] = defaultdict(int)
        self._missed: dict[str, int] = defaultdict(int)
        self._gaps: list[str] = []

    def record_hit(self, topic: str) -> None:
        """Record a doctrine cache hit."""
        self._triggered[topic] += 1

    def record_miss(self, query: str) -> None:
        """Record a doctrine cache miss."""
        self._missed[query] += 1
        if self._missed[query] >= 3 and query not in self._gaps:
            self._gaps.append(query)
            logger.warning(f"Epistemic gap: '{query}' missed {self._missed[query]} times")

    def get_coverage(self) -> dict[str, Any]:
        """Get coverage statistics."""
        total_domains = len(self._domain_coverage)
        triggered_count = len(self._triggered)
        return {
            "total_domains": total_domains,
            "issue_categories": len(self._issue_categories),
            "triggered_topics": triggered_count,
            "top_triggered": dict(sorted(self._triggered.items(), key=lambda x: x[1], reverse=True)[:10]),
            "top_missed": dict(sorted(self._missed.items(), key=lambda x: x[1], reverse=True)[:10]),
            "epistemic_gaps": self._gaps[:20],
            "gap_count": len(self._gaps),
        }


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
        self._start_time = time.monotonic()
        self._endpoint_counts: dict[str, int] = defaultdict(int)
        self._hourly_buckets: dict[str, int] = defaultdict(int)
        self._archive_ops: dict[str, int] = defaultdict(int)

    def record_request(self, endpoint: str, latency_ms: float, is_error: bool = False) -> None:
        """Record a request metric."""
        self._request_count += 1
        self._latencies.append(latency_ms)
        if len(self._latencies) > 2000:
            self._latencies = self._latencies[-1000:]
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

    def record_archive_op(self, op_type: str) -> None:
        """Record an archive operation type."""
        self._archive_ops[op_type] += 1

    def get_metrics(self) -> dict[str, Any]:
        """Return comprehensive metrics."""
        uptime = time.monotonic() - self._start_time
        sorted_lat = sorted(self._latencies) if self._latencies else [0.0]
        return {
            "uptime_seconds": round(uptime, 2),
            "total_requests": self._request_count,
            "total_errors": self._error_count,
            "error_rate": round(self._error_count / max(self._request_count, 1), 4),
            "requests_per_hour": round(self._request_count / max(uptime / 3600, 0.001), 2),
            "latency": {
                "avg_ms": round(sum(self._latencies) / max(len(self._latencies), 1), 2),
                "p50_ms": round(sorted_lat[len(sorted_lat) // 2], 2),
                "p95_ms": round(sorted_lat[int(len(sorted_lat) * 0.95)], 2),
                "p99_ms": round(sorted_lat[min(int(len(sorted_lat) * 0.99), len(sorted_lat) - 1)], 2),
            },
            "cache": {
                "hits": self._cache_hits,
                "misses": self._cache_misses,
                "hit_rate": round(self._cache_hits / max(self._cache_hits + self._cache_misses, 1), 4),
            },
            "archive_operations": dict(self._archive_ops),
            "endpoints": dict(self._endpoint_counts),
            "hourly_traffic": dict(list(self._hourly_buckets.items())[-24:]),
        }


# ═══════════════════════════════════════════════════════════════════════════════
# [TIE-13] ZONED ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════

class ZonedAnalyzer:
    """Enforces strict zone separation in archive analysis.

    PLANNING: Evaluating what to archive, how to classify, preservation strategy.
    REPORTING: Generating reports, timelines, legacy narratives from archived data.
    AUDIT: Reviewing integrity, access patterns, compliance, completeness.
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
            "zone": zone.value, "action": "enter", "context": context,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

    def exit_zone(self) -> None:
        """Exit the current analysis zone."""
        if self._active_zone:
            self._zone_history.append({
                "zone": self._active_zone.value, "action": "exit",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
        self._active_zone = None

    def get_history(self) -> list[dict[str, Any]]:
        """Return zone transition history."""
        return self._zone_history[-50:]


# ═══════════════════════════════════════════════════════════════════════════════
# [TIE-14] FACT FRAGILITY SCORING
# ═══════════════════════════════════════════════════════════════════════════════

class FactFragilityScorer:
    """Score the fragility of archival assertions.

    Evaluates how well-supported an archival claim is:
    - Verifiability: can the claim be independently verified?
    - Recharacterization risk: could the same facts support a different conclusion?
    - Testimony dependence: does the claim rely on a single source?
    """

    BASE_FRAGILITY: dict[str, float] = {
        "primary_source": 0.10,
        "secondary_source": 0.25,
        "oral_testimony": 0.40,
        "inference": 0.50,
        "estimation": 0.60,
        "hearsay": 0.75,
        "undocumented": 0.90,
    }

    @classmethod
    def score(cls, source_type: str, corroboration_count: int,
              has_physical_evidence: bool) -> dict[str, Any]:
        """Score the fragility of an archival assertion."""
        fragility = cls.BASE_FRAGILITY.get(source_type, 0.50)
        if corroboration_count > 0:
            fragility *= max(0.3, 1.0 - corroboration_count * 0.15)
        if has_physical_evidence:
            fragility *= 0.5

        verifiability = 1.0 - fragility
        recharacterization_risk = fragility * 0.6
        testimony_dependence = fragility * 0.8 if source_type in ("oral_testimony", "hearsay") else fragility * 0.3

        return {
            "source_type": source_type,
            "fragility_score": round(fragility, 4),
            "verifiability": round(verifiability, 4),
            "recharacterization_risk": round(recharacterization_risk, 4),
            "testimony_dependence": round(testimony_dependence, 4),
            "corroboration_count": corroboration_count,
            "has_physical_evidence": has_physical_evidence,
            "tier": (
                "ROCK_SOLID" if fragility < 0.10 else
                "STRONG" if fragility < 0.25 else
                "ADEQUATE" if fragility < 0.45 else
                "FRAGILE" if fragility < 0.70 else
                "UNRELIABLE"
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
        self._last_hash = "0" * 64

    def log(self, event_type: str, data: dict[str, Any]) -> str:
        """Append an audit entry with hash chain. Returns entry ID."""
        entry_id = str(uuid.uuid4())
        entry = {
            "id": entry_id,
            "event_type": event_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "engine": ENGINE_ID,
            "previous_hash": self._last_hash,
            "data": data,
        }
        entry_json = json.dumps(entry, sort_keys=True, separators=(",", ":"))
        entry_hash = hashlib.sha256(entry_json.encode()).hexdigest()
        entry["integrity_hash"] = entry_hash
        self._last_hash = entry_hash

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
                try:
                    entry = json.loads(line)
                    if event_type is None or entry.get("event_type") == event_type:
                        entries.append(entry)
                except json.JSONDecodeError:
                    continue
        return entries[-limit:]

    def get_stats(self) -> dict[str, Any]:
        """Return audit trail statistics."""
        size_bytes = self._log_path.stat().st_size if self._log_path.exists() else 0
        return {
            "log_path": str(self._log_path),
            "entries_this_session": self._entry_count,
            "file_size_bytes": size_bytes,
            "file_size_mb": round(size_bytes / (1024 * 1024), 2),
            "last_hash": self._last_hash[:16] + "...",
        }


# ═══════════════════════════════════════════════════════════════════════════════
# [TIE-19] MULTI-DOCTRINE DECOMPOSITION
# ═══════════════════════════════════════════════════════════════════════════════

class MultiDoctrineDecomposer:
    """Decompose complex archive queries into issue categories and interaction DAG."""

    INTERACTION_EDGES: list[tuple[str, str, str]] = [
        ("archive_ingestion", "provenance_tracking", "ingestion requires provenance metadata"),
        ("archive_ingestion", "integrity_verification", "ingestion triggers integrity hash computation"),
        ("timeline_query", "historical_reconstruction", "timeline enables point-in-time reconstruction"),
        ("time_capsule_management", "access_control", "capsules require access control enforcement"),
        ("document_versioning", "integrity_verification", "versioning requires hash chain verification"),
        ("legacy_reporting", "timeline_query", "reports depend on timeline data"),
        ("legacy_reporting", "search_and_discovery", "reports use search to gather events"),
        ("search_and_discovery", "archive_ingestion", "search indexes content at ingestion"),
        ("family_history", "timeline_query", "family events integrate with system timeline"),
        ("decision_recording", "provenance_tracking", "decisions require full provenance"),
        ("decision_recording", "archive_ingestion", "recording triggers archival ingestion"),
        ("historical_reconstruction", "search_and_discovery", "reconstruction uses search"),
        ("access_control", "integrity_verification", "access control enforced by integrity checks"),
        ("digital_estate_planning", "access_control", "estate plans require restricted access"),
        ("digital_estate_planning", "generational_transfer", "estate planning enables transfer"),
        ("knowledge_preservation", "archive_ingestion", "preservation requires proper ingestion"),
        ("generational_transfer", "family_history", "transfer documentation links to family records"),
    ]

    CATEGORY_KEYWORDS: dict[str, list[str]] = {
        ArchiveIssueCategory.ARCHIVE_INGESTION.value: ["ingest", "store", "add", "create", "upload", "import"],
        ArchiveIssueCategory.TIMELINE_QUERY.value: ["timeline", "when", "chronology", "date", "history", "sequence"],
        ArchiveIssueCategory.TIME_CAPSULE_MANAGEMENT.value: ["capsule", "sealed", "embargo", "reveal", "future", "deferred"],
        ArchiveIssueCategory.DOCUMENT_VERSIONING.value: ["version", "revision", "diff", "change", "update", "amendment"],
        ArchiveIssueCategory.PROVENANCE_TRACKING.value: ["provenance", "origin", "source", "who created", "lineage", "attribution"],
        ArchiveIssueCategory.HISTORICAL_RECONSTRUCTION.value: ["reconstruct", "point-in-time", "snapshot", "state at", "archaeology"],
        ArchiveIssueCategory.LEGACY_REPORTING.value: ["report", "summary", "narrative", "retrospective", "achievements"],
        ArchiveIssueCategory.SEARCH_AND_DISCOVERY.value: ["search", "find", "lookup", "query", "discover", "retrieve"],
        ArchiveIssueCategory.FAMILY_HISTORY.value: ["family", "genealogy", "McWilliams", "bloodline", "dynasty", "heritage"],
        ArchiveIssueCategory.DECISION_RECORDING.value: ["decision", "chose", "rationale", "alternative", "tradeoff", "ADR"],
        ArchiveIssueCategory.ACCESS_CONTROL.value: ["access", "classification", "restricted", "sovereign", "clearance", "permission"],
        ArchiveIssueCategory.INTEGRITY_VERIFICATION.value: ["integrity", "verify", "hash", "tamper", "corrupt", "validate"],
        ArchiveIssueCategory.DIGITAL_ESTATE_PLANNING.value: ["estate", "digital asset", "inheritance", "beneficiary", "executor", "RUFADAA"],
        ArchiveIssueCategory.KNOWLEDGE_PRESERVATION.value: ["preserve", "knowledge", "longevity", "future-proof", "format", "OAIS"],
        ArchiveIssueCategory.GENERATIONAL_TRANSFER.value: ["generational", "transfer", "wealth", "trust", "dynasty trust", "heir"],
    }

    def decompose(self, query: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        """Decompose a query into issue categories with interaction DAG."""
        query_lower = query.lower()
        categories_detected: list[str] = []
        for category, keywords in self.CATEGORY_KEYWORDS.items():
            if any(kw in query_lower for kw in keywords):
                categories_detected.append(category)
        if not categories_detected:
            categories_detected = [ArchiveIssueCategory.SEARCH_AND_DISCOVERY.value]

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
        for c in categories:
            if c not in order:
                order.append(c)
        return order


# ═══════════════════════════════════════════════════════════════════════════════
# [TIE-20] DEEP ANALYSIS MODE
# ═══════════════════════════════════════════════════════════════════════════════

class DeepAnalyzer:
    """Multi-source synthesis with full reasoning chain for archive queries."""

    def __init__(self, doctrine_cache: dict[str, Any], semantic_dict: dict[str, Any]) -> None:
        self._doctrine_cache = doctrine_cache
        self._semantic_dict = semantic_dict
        self._decomposer = MultiDoctrineDecomposer()
        self._fragility_scorer = FactFragilityScorer()

    def analyze(self, query: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        """Perform deep multi-source analysis."""
        start = time.monotonic()
        context = context or {}
        decomposition = self._decomposer.decompose(query, context)

        evidence: dict[str, list[dict[str, Any]]] = {}
        for category in decomposition["categories_detected"]:
            evidence[category] = self._gather_evidence(category)

        reasoning_chain = self._build_reasoning_chain(decomposition, evidence)
        factor_scores = [
            self._fragility_scorer.score(
                source_type="primary_source" if evidence.get(cat) else "inference",
                corroboration_count=len(evidence.get(cat, [])),
                has_physical_evidence=bool(evidence.get(cat)),
            )
            for cat in decomposition["categories_detected"]
        ]
        avg_fragility = sum(s["fragility_score"] for s in factor_scores) / max(len(factor_scores), 1)
        confidence = round(1.0 - avg_fragility, 4)

        elapsed_ms = (time.monotonic() - start) * 1000
        return {
            "query": query,
            "decomposition": decomposition,
            "evidence_counts": {k: len(v) for k, v in evidence.items()},
            "reasoning_chain": reasoning_chain,
            "fragility_scores": factor_scores,
            "confidence": confidence,
            "stratification": ConfidenceStratifier.stratify(confidence).value,
            "elapsed_ms": round(elapsed_ms, 2),
            "determinism_hash": compute_determinism_hash({
                "query": query,
                "categories": decomposition["categories_detected"],
                "evidence_counts": {k: len(v) for k, v in evidence.items()},
            }),
        }

    def _gather_evidence(self, category: str) -> list[dict[str, Any]]:
        """Gather doctrine evidence for a category."""
        results: list[dict[str, Any]] = []
        category_tokens = set(category.replace("_", " ").split())
        for doctrine in self._doctrine_cache.get("doctrines", []):
            keywords = set(kw.lower() for kw in doctrine.get("keywords", []))
            if category_tokens & keywords:
                results.append(doctrine)
        return results

    def _build_reasoning_chain(self, decomposition: dict[str, Any],
                                evidence: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
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
                    f"Doctrine evidence supports {category} with {len(ev)} sources"
                    if ev else
                    f"No direct doctrine for {category}; applying general archival principles"
                ),
            })
        return chain


# ═══════════════════════════════════════════════════════════════════════════════
# LEGACY ARCHIVE CORE ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

class LegacyArchiveEngine:
    """Core engine for the Legacy Archive system.

    Manages archive entries, time capsules, family events, decision records,
    digital estate assets, versioning, search, and integrity verification.
    """

    def __init__(self) -> None:
        self._entries: dict[str, ArchiveEntry] = {}
        self._capsules: dict[str, TimeCapsuleEntry] = {}
        self._family_events: dict[str, FamilyEvent] = {}
        self._decisions: dict[str, DecisionRecord] = {}
        self._digital_assets: dict[str, DigitalEstateAsset] = {}
        self._version_chains: dict[str, list[str]] = defaultdict(list)
        self._search_index: dict[str, list[str]] = defaultdict(list)
        self._category_chains: dict[str, str] = {}
        self._total_ingested = 0

    # ─── ARCHIVE ENTRY OPERATIONS ────────────────────────────────────────

    def ingest_entry(self, entry: ArchiveEntry) -> dict[str, Any]:
        """Ingest a new archive entry with hash chain and indexing."""
        content_hash = hashlib.sha256(entry.content.encode("utf-8")).hexdigest()
        entry.content_hash = content_hash
        cat_key = entry.category.value
        entry.previous_hash = self._category_chains.get(cat_key, "0" * 64)
        self._category_chains[cat_key] = content_hash

        auto_class = AuthorityHardening.auto_classify_content(entry.content, entry.tags)
        if auto_class.value > entry.access_level.value:
            entry.access_level = auto_class

        self._entries[entry.entry_id] = entry
        self._index_entry(entry)
        self._total_ingested += 1

        logger.info(f"Ingested entry: {entry.entry_id} | {entry.title} | {entry.category.value} | importance={entry.importance}")
        return {
            "entry_id": entry.entry_id,
            "content_hash": content_hash,
            "access_level": entry.access_level.value,
            "category": entry.category.value,
            "importance": entry.importance,
            "indexed_tokens": len(entry.content.split()),
        }

    def _index_entry(self, entry: ArchiveEntry) -> None:
        """Add entry to the search index."""
        tokens = set()
        for token in entry.title.lower().split():
            tokens.add(token)
        for token in entry.content.lower().split():
            tokens.add(token)
        for tag in entry.tags:
            tokens.add(tag.lower())
        for token in tokens:
            self._search_index[token].append(entry.entry_id)

    def get_entry(self, entry_id: str) -> dict[str, Any] | None:
        """Retrieve an archive entry by ID."""
        entry = self._entries.get(entry_id)
        if entry is None:
            return None
        return entry.model_dump()

    def search_entries(self, request: SearchRequest) -> list[dict[str, Any]]:
        """Full-text search across archive entries."""
        query_tokens = request.query.lower().split()
        scores: dict[str, float] = defaultdict(float)
        total_entries = max(len(self._entries), 1)

        for token in query_tokens:
            entry_ids = self._search_index.get(token, [])
            if not entry_ids:
                continue
            idf = math.log(total_entries / (len(set(entry_ids)) + 1)) + 1.0
            for eid in entry_ids:
                scores[eid] += idf

        # Apply importance weighting
        for eid, score in list(scores.items()):
            entry = self._entries.get(eid)
            if entry is None:
                continue
            if request.categories and entry.category not in request.categories:
                del scores[eid]
                continue
            if entry.importance < request.min_importance:
                del scores[eid]
                continue
            scores[eid] = score * (1.0 + entry.importance * 0.1)

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:request.top_k]
        results: list[dict[str, Any]] = []
        for eid, score in ranked:
            entry = self._entries.get(eid)
            if entry:
                d = entry.model_dump()
                d["search_score"] = round(score, 4)
                results.append(d)
        return results

    # ─── TIME CAPSULE OPERATIONS ─────────────────────────────────────────

    def seal_capsule(self, capsule: TimeCapsuleEntry) -> dict[str, Any]:
        """Seal a time capsule with content hash."""
        content_hash = hashlib.sha256(capsule.content.encode("utf-8")).hexdigest()
        capsule.sealed_content_hash = content_hash
        capsule.is_sealed = True
        self._capsules[capsule.capsule_id] = capsule
        logger.info(f"Sealed capsule: {capsule.capsule_id} | reveal={capsule.reveal_date}")
        return {
            "capsule_id": capsule.capsule_id,
            "sealed_at": capsule.sealed_at,
            "reveal_date": capsule.reveal_date,
            "content_hash": content_hash,
            "status": "SEALED",
        }

    def check_capsule(self, capsule_id: str) -> dict[str, Any]:
        """Check capsule status and reveal if date has passed."""
        capsule = self._capsules.get(capsule_id)
        if capsule is None:
            return {"error": "Capsule not found", "capsule_id": capsule_id}
        now = datetime.now(timezone.utc)
        try:
            reveal = datetime.fromisoformat(capsule.reveal_date.replace("Z", "+00:00"))
        except ValueError:
            reveal = now + timedelta(days=36500)  # far future if unparseable

        if now >= reveal:
            capsule.is_revealed = True
            return {
                "capsule_id": capsule.capsule_id,
                "title": capsule.title,
                "content": capsule.content,
                "sealed_at": capsule.sealed_at,
                "reveal_date": capsule.reveal_date,
                "status": "REVEALED",
                "content_hash": capsule.sealed_content_hash,
                "annotations": capsule.annotations,
            }
        else:
            days_remaining = (reveal - now).days
            return {
                "capsule_id": capsule.capsule_id,
                "title": capsule.title,
                "sealed_at": capsule.sealed_at,
                "reveal_date": capsule.reveal_date,
                "status": "SEALED",
                "days_remaining": days_remaining,
                "content_hash": capsule.sealed_content_hash,
                "annotations": capsule.annotations,
            }

    # ─── FAMILY EVENTS ───────────────────────────────────────────────────

    def record_family_event(self, event: FamilyEvent) -> dict[str, Any]:
        """Record a family history event."""
        self._family_events[event.event_id] = event
        logger.info(f"Family event: {event.event_id} | {event.event_type} | {event.description[:80]}")
        return {"event_id": event.event_id, "event_type": event.event_type, "recorded": True}

    def get_family_timeline(self, member: str = "") -> list[dict[str, Any]]:
        """Get family event timeline, optionally filtered by member."""
        events = list(self._family_events.values())
        if member:
            events = [e for e in events if member.lower() in [m.lower() for m in e.family_members]]
        events.sort(key=lambda e: e.event_date)
        return [e.model_dump() for e in events[:MAX_TIMELINE_EVENTS]]

    # ─── DECISION RECORDS ────────────────────────────────────────────────

    def record_decision(self, decision: DecisionRecord) -> dict[str, Any]:
        """Record an architecture/business/personal decision."""
        self._decisions[decision.decision_id] = decision
        logger.info(f"Decision recorded: {decision.decision_id} | {decision.title}")
        return {"decision_id": decision.decision_id, "title": decision.title, "recorded": True}

    def get_decisions(self, domain: str = "", min_importance: int = 1) -> list[dict[str, Any]]:
        """List decision records, optionally filtered."""
        decisions = list(self._decisions.values())
        if domain:
            decisions = [d for d in decisions if d.domain.lower() == domain.lower()]
        decisions = [d for d in decisions if d.importance >= min_importance]
        decisions.sort(key=lambda d: d.decided_at, reverse=True)
        return [d.model_dump() for d in decisions[:100]]

    # ─── DIGITAL ESTATE ──────────────────────────────────────────────────

    def register_digital_asset(self, asset: DigitalEstateAsset) -> dict[str, Any]:
        """Register a digital asset in the estate plan."""
        self._digital_assets[asset.asset_id] = asset
        logger.info(f"Digital asset registered: {asset.asset_id} | {asset.asset_name} | {asset.asset_type}")
        return {"asset_id": asset.asset_id, "asset_name": asset.asset_name, "registered": True}

    def get_estate_inventory(self) -> dict[str, Any]:
        """Get the complete digital estate inventory."""
        assets = list(self._digital_assets.values())
        total_value = sum(a.estimated_value for a in assets)
        by_type: dict[str, int] = defaultdict(int)
        for a in assets:
            by_type[a.asset_type] += 1
        return {
            "total_assets": len(assets),
            "total_estimated_value": round(total_value, 2),
            "by_type": dict(by_type),
            "assets": [a.model_dump() for a in assets],
        }

    # ─── INTEGRITY VERIFICATION ──────────────────────────────────────────

    def verify_integrity(self) -> IntegrityCheckResult:
        """Run full integrity verification on the archive."""
        total = len(self._entries)
        verified = 0
        mismatches = 0
        chain_breaks = 0

        for entry in self._entries.values():
            computed = hashlib.sha256(entry.content.encode("utf-8")).hexdigest()
            if computed == entry.content_hash:
                verified += 1
            else:
                mismatches += 1

        integrity_score = verified / max(total, 1)
        return IntegrityCheckResult(
            total_entries=total,
            verified_ok=verified,
            hash_mismatches=mismatches,
            chain_breaks=chain_breaks,
            integrity_score=round(integrity_score, 4),
        )

    # ─── LEGACY REPORT GENERATION ────────────────────────────────────────

    def generate_legacy_report(self, request: LegacyReportRequest) -> dict[str, Any]:
        """Generate a structured legacy report for a time period."""
        all_events: list[dict[str, Any]] = []

        for entry in self._entries.values():
            if request.categories and entry.category not in request.categories:
                continue
            if entry.importance < request.min_importance:
                continue
            effective_importance = self._compute_effective_importance(entry.importance, entry.created_at)
            all_events.append({
                "type": "archive_entry",
                "id": entry.entry_id,
                "title": entry.title,
                "category": entry.category.value,
                "importance": entry.importance,
                "effective_importance": effective_importance,
                "date": entry.created_at,
            })

        for event in self._family_events.values():
            if request.categories and event.category not in request.categories:
                continue
            effective_importance = self._compute_effective_importance(event.importance, event.event_date)
            all_events.append({
                "type": "family_event",
                "id": event.event_id,
                "title": f"{event.event_type}: {event.description[:80]}",
                "category": event.category.value,
                "importance": event.importance,
                "effective_importance": effective_importance,
                "date": event.event_date,
            })

        for dec in self._decisions.values():
            effective_importance = self._compute_effective_importance(dec.importance, dec.decided_at)
            all_events.append({
                "type": "decision",
                "id": dec.decision_id,
                "title": dec.title,
                "category": dec.domain,
                "importance": dec.importance,
                "effective_importance": effective_importance,
                "date": dec.decided_at,
            })

        all_events.sort(key=lambda e: e["effective_importance"], reverse=True)
        selected = all_events[:request.max_events]

        executive_summary = [e for e in selected if e["importance"] >= HIGH_IMPORTANCE_THRESHOLD]

        return {
            "report_generated_at": datetime.now(timezone.utc).isoformat(),
            "total_events_considered": len(all_events),
            "events_selected": len(selected),
            "executive_summary": executive_summary[:10],
            "detailed_timeline": sorted(selected, key=lambda e: e["date"]),
            "metrics": {
                "archive_entries": len(self._entries),
                "family_events": len(self._family_events),
                "decisions": len(self._decisions),
                "digital_assets": len(self._digital_assets),
                "time_capsules": len(self._capsules),
            },
        }

    @staticmethod
    def _compute_effective_importance(base_importance: int, date_str: str) -> float:
        """Compute effective importance with age bonus for high-importance events."""
        try:
            event_date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            now = datetime.now(timezone.utc)
            years_old = (now - event_date).days / 365.25
        except (ValueError, TypeError):
            years_old = 0.0

        if base_importance >= HIGH_IMPORTANCE_THRESHOLD:
            bonus = min(years_old * IMPORTANCE_AGE_BONUS_PER_YEAR, IMPORTANCE_AGE_BONUS_CAP)
        elif base_importance >= 4:
            bonus = min(years_old * 0.05, 1.0)
        else:
            bonus = 0.0
        return round(base_importance + bonus, 2)

    def get_status(self) -> dict[str, Any]:
        """Get archive engine status."""
        return {
            "total_entries": len(self._entries),
            "total_capsules": len(self._capsules),
            "total_family_events": len(self._family_events),
            "total_decisions": len(self._decisions),
            "total_digital_assets": len(self._digital_assets),
            "total_ingested": self._total_ingested,
            "index_tokens": len(self._search_index),
            "category_chains": len(self._category_chains),
        }


# ═══════════════════════════════════════════════════════════════════════════════
# [TIE-17] FASTAPI SERVER — LIFESPAN, APP, MIDDLEWARE
# ═══════════════════════════════════════════════════════════════════════════════

# Module-level references (initialized in lifespan)
three_layer: ThreeLayerResponse | None = None
archive_engine: LegacyArchiveEngine | None = None
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
async def lifespan(application: FastAPI):
    """Initialize all engine components on startup."""
    global three_layer, archive_engine, telemetry, drift_watcher, coverage_map
    global metrics, audit_trail, zoned_analyzer, vector_search, deep_analyzer, normalizer

    logger.info(f"Starting {ENGINE_NAME} v{ENGINE_VERSION} on port {ENGINE_PORT}")

    doctrine_cache_data = load_doctrine_cache()
    semantic_dict_data = load_semantic_dict()
    coverage_map_data: dict[str, Any] = {}
    if COVERAGE_MAP_PATH.exists():
        with COVERAGE_MAP_PATH.open("r", encoding="utf-8") as fh:
            coverage_map_data = json.load(fh)

    three_layer = ThreeLayerResponse(doctrine_cache_data, semantic_dict_data)
    archive_engine = LegacyArchiveEngine()
    telemetry = TelemetryCollector()
    drift_watcher = DriftWatcher()
    coverage_map = CoverageMap(coverage_map_data)
    metrics = MetricsCollector()
    audit_trail = AuditTrail(AUDIT_LOG_PATH)
    zoned_analyzer = ZonedAnalyzer()
    vector_search = VectorSearchEngine(doctrine_cache_data.get("doctrines", []))
    deep_analyzer = DeepAnalyzer(doctrine_cache_data, semantic_dict_data)
    normalizer = SemanticNormalizer(semantic_dict_data)

    drift_watcher.set_baseline({
        "cache_hit_rate": 0.60,
        "avg_importance": 6.0,
        "ingestion_rate": 0.5,
        "search_rate": 0.3,
    })

    logger.info(f"{ENGINE_NAME} initialized — {len(doctrine_cache_data.get('doctrines', []))} doctrines")
    yield
    logger.info(f"{ENGINE_NAME} shutting down")


app = FastAPI(
    title=f"BLD05 — {ENGINE_NAME}",
    description="Legacy archival and preservation for the McWilliams Dynasty",
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


@app.middleware("http")
async def tracking_middleware(request: Request, call_next):
    """Track every request for telemetry."""
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
        "archive": archive_engine.get_status() if archive_engine else {},
        "three_layer": three_layer.get_stats() if three_layer else {},
        "telemetry": telemetry.get_stats() if telemetry else {},
        "metrics": metrics.get_metrics() if metrics else {},
        "drift": drift_watcher.get_status() if drift_watcher else {},
        "coverage": coverage_map.get_coverage() if coverage_map else {},
        "audit": audit_trail.get_stats() if audit_trail else {},
        "determinism_hash": compute_determinism_hash({
            "engine": ENGINE_ID, "version": ENGINE_VERSION, "status": "healthy",
        }),
    }


# ═══════════════════════════════════════════════════════════════════════════════
# QUERY ENDPOINT (Three-Layer Response)
# ═══════════════════════════════════════════════════════════════════════════════

@app.post("/query")
async def query_endpoint(request: QueryRequest) -> dict[str, Any]:
    """Query the three-layer response system for archival knowledge."""
    raw = three_layer.resolve(request.query, request.context)
    result = raw.get("result", {})
    topic = result.get("topic", "")

    if raw["layer"] == ResponseLayer.DOCTRINE_CACHE.value:
        coverage_map.record_hit(topic)
        metrics.record_cache_event(hit=True)
    else:
        coverage_map.record_miss(request.query)
        metrics.record_cache_event(hit=False)

    formatted = ResponseFormatter.format(raw, request.mode, request.query)
    formatted["determinism_hash"] = compute_determinism_hash({
        "query": request.query, "layer": raw["layer"], "topic": topic,
    })

    audit_trail.log("query", {
        "query": request.query, "mode": request.mode.value,
        "layer": raw["layer"], "confidence": raw.get("confidence", 0.0),
    })
    return formatted


# ═══════════════════════════════════════════════════════════════════════════════
# ARCHIVE ENTRY ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@app.post("/archive/ingest")
async def ingest_endpoint(entry: ArchiveEntry) -> dict[str, Any]:
    """Ingest a new entry into the archive."""
    result = archive_engine.ingest_entry(entry)
    metrics.record_archive_op("ingest")
    drift_watcher.observe("ingestion_rate", 1.0)
    drift_watcher.observe("avg_importance", float(entry.importance))
    telemetry.trace_archive_event("ingest", f"{entry.entry_id} | {entry.title}")
    audit_trail.log("ingest", {"entry_id": entry.entry_id, "title": entry.title, "category": entry.category.value})
    return result


@app.get("/archive/entry/{entry_id}")
async def get_entry_endpoint(entry_id: str) -> dict[str, Any]:
    """Retrieve an archive entry by ID."""
    result = archive_engine.get_entry(entry_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Entry {entry_id} not found")
    audit_trail.log("read", {"entry_id": entry_id})
    return result


@app.post("/archive/search")
async def search_endpoint(request: SearchRequest) -> dict[str, Any]:
    """Full-text search across archive entries."""
    results = archive_engine.search_entries(request)
    metrics.record_archive_op("search")
    drift_watcher.observe("search_rate", 1.0)
    audit_trail.log("search", {"query": request.query, "results": len(results)})
    return {"query": request.query, "results": results, "count": len(results)}


# ═══════════════════════════════════════════════════════════════════════════════
# TIME CAPSULE ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@app.post("/capsule/seal")
async def seal_capsule_endpoint(capsule: TimeCapsuleEntry) -> dict[str, Any]:
    """Seal a new time capsule."""
    result = archive_engine.seal_capsule(capsule)
    metrics.record_archive_op("seal_capsule")
    telemetry.trace_archive_event("seal_capsule", capsule.capsule_id)
    audit_trail.log("seal_capsule", {"capsule_id": capsule.capsule_id, "reveal_date": capsule.reveal_date})
    return result


@app.get("/capsule/{capsule_id}")
async def check_capsule_endpoint(capsule_id: str) -> dict[str, Any]:
    """Check capsule status and reveal if embargo has passed."""
    result = archive_engine.check_capsule(capsule_id)
    audit_trail.log("check_capsule", {"capsule_id": capsule_id, "status": result.get("status")})
    return result


# ═══════════════════════════════════════════════════════════════════════════════
# FAMILY HISTORY ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@app.post("/family/event")
async def record_family_event_endpoint(event: FamilyEvent) -> dict[str, Any]:
    """Record a family history event."""
    result = archive_engine.record_family_event(event)
    metrics.record_archive_op("family_event")
    telemetry.trace_archive_event("family_event", f"{event.event_type}: {event.description[:60]}")
    audit_trail.log("family_event", {"event_id": event.event_id, "type": event.event_type})
    return result


@app.get("/family/timeline")
async def family_timeline_endpoint(member: str = "") -> dict[str, Any]:
    """Get family event timeline."""
    events = archive_engine.get_family_timeline(member)
    return {"member_filter": member or "ALL", "events": events, "count": len(events)}


# ═══════════════════════════════════════════════════════════════════════════════
# DECISION RECORD ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@app.post("/decision/record")
async def record_decision_endpoint(decision: DecisionRecord) -> dict[str, Any]:
    """Record a decision."""
    result = archive_engine.record_decision(decision)
    metrics.record_archive_op("decision")
    telemetry.trace_archive_event("decision", decision.title)
    audit_trail.log("decision", {"decision_id": decision.decision_id, "title": decision.title})
    return result


@app.get("/decision/list")
async def list_decisions_endpoint(domain: str = "", min_importance: int = 1) -> dict[str, Any]:
    """List decision records."""
    decisions = archive_engine.get_decisions(domain, min_importance)
    return {"domain_filter": domain or "ALL", "decisions": decisions, "count": len(decisions)}


# ═══════════════════════════════════════════════════════════════════════════════
# DIGITAL ESTATE ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@app.post("/estate/register")
async def register_asset_endpoint(asset: DigitalEstateAsset) -> dict[str, Any]:
    """Register a digital asset in the estate plan."""
    result = archive_engine.register_digital_asset(asset)
    metrics.record_archive_op("estate_register")
    telemetry.trace_archive_event("estate_register", f"{asset.asset_name} ({asset.asset_type})")
    audit_trail.log("estate_register", {"asset_id": asset.asset_id, "name": asset.asset_name, "type": asset.asset_type})
    return result


@app.get("/estate/inventory")
async def estate_inventory_endpoint() -> dict[str, Any]:
    """Get complete digital estate inventory."""
    return archive_engine.get_estate_inventory()


# ═══════════════════════════════════════════════════════════════════════════════
# INTEGRITY / REPORT / ANALYSIS ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@app.get("/integrity/verify")
async def integrity_verify_endpoint() -> dict[str, Any]:
    """Run full integrity verification."""
    result = archive_engine.verify_integrity()
    metrics.record_archive_op("integrity_verify")
    audit_trail.log("integrity_verify", {"score": result.integrity_score, "mismatches": result.hash_mismatches})
    return result.model_dump()


@app.post("/report/generate")
async def generate_report_endpoint(request: LegacyReportRequest) -> dict[str, Any]:
    """Generate a legacy report for a time period."""
    result = archive_engine.generate_legacy_report(request)
    metrics.record_archive_op("report")
    audit_trail.log("report", {"events_selected": result["events_selected"]})
    return result


@app.post("/analyze")
async def deep_analysis_endpoint(query: str = "", context: dict[str, Any] | None = None) -> dict[str, Any]:
    """Deep multi-source analysis on an archival query."""
    if not query:
        raise HTTPException(status_code=400, detail="Query parameter required")
    result = deep_analyzer.analyze(query, context)
    audit_trail.log("deep_analysis", {"query": query, "confidence": result["confidence"]})
    return result


# ═══════════════════════════════════════════════════════════════════════════════
# VECTOR SEARCH / NORMALIZE / DRIFT / COVERAGE / METRICS / TELEMETRY / AUDIT
# ═══════════════════════════════════════════════════════════════════════════════

@app.get("/search/doctrine")
async def doctrine_search_endpoint(query: str, top_k: int = 5) -> dict[str, Any]:
    """Search archive doctrines using TF-IDF vector search."""
    results = vector_search.search(query, top_k)
    return {"query": query, "results": results, "count": len(results)}


@app.get("/normalize")
async def normalize_endpoint(text: str) -> dict[str, Any]:
    """Normalize archive-domain text."""
    return {
        "original": text,
        "normalized": normalizer.normalize(text),
        "synonyms": normalizer.expand_synonyms(text),
        "without_stop_words": normalizer.remove_stop_words(text),
    }


@app.get("/drift")
async def drift_endpoint() -> dict[str, Any]:
    """Check for doctrine drift."""
    return {"alerts": drift_watcher.check_drift(), "status": drift_watcher.get_status()}


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


@app.get("/audit")
async def audit_endpoint(event_type: str | None = None, limit: int = 50) -> dict[str, Any]:
    """Query the audit trail."""
    entries = audit_trail.query(event_type, limit)
    return {"entries": entries, "count": len(entries), "stats": audit_trail.get_stats()}


@app.get("/zones/history")
async def zones_history_endpoint() -> dict[str, Any]:
    """Get zone transition history."""
    return {
        "history": zoned_analyzer.get_history(),
        "active_zone": zoned_analyzer._active_zone.value if zoned_analyzer._active_zone else None,
    }


@app.post("/fragility")
async def fragility_endpoint(
    source_type: str = "primary_source",
    corroboration_count: int = 0,
    has_physical_evidence: bool = False,
) -> dict[str, Any]:
    """Score the fragility of an archival assertion."""
    return FactFragilityScorer.score(source_type, corroboration_count, has_physical_evidence)


# ═══════════════════════════════════════════════════════════════════════════════
# ROOT / STATUS
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
            "/health", "/query", "/archive/ingest", "/archive/entry/{id}", "/archive/search",
            "/capsule/seal", "/capsule/{id}", "/family/event", "/family/timeline",
            "/decision/record", "/decision/list", "/estate/register", "/estate/inventory",
            "/integrity/verify", "/report/generate", "/analyze", "/search/doctrine",
            "/normalize", "/drift", "/coverage", "/metrics", "/telemetry",
            "/audit", "/zones/history", "/fragility",
        ],
    }


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
