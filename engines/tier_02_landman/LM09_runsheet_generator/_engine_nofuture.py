"""
LM09 Runsheet Generator Engine
Engine ID: LM09 | Port: 8509 | Version: 1.0.0
Domain: Landman Intelligence — Automated Run Sheet / Abstract Generation

TIE-20 Gold Standard Implementation:
  1.  three_layer_response — Doctrine Cache, Semantic Retrieval, Deep Analysis
  2.  response_modes — FAST, DEFENSE, MEMO
  3.  doctrine_cache — 30+ pre-compiled expert reasoning blocks
  4.  authority_hardening — Hierarchical authority with weights
  5.  confidence_stratification — DEFENSIBLE / AGGRESSIVE / DISCLOSURE / HIGH_RISK
  6.  semantic_normalization — Run sheet term normalization
  7.  vector_search — Semantic retrieval fallback
  8.  telemetry — Full query tracing
  9.  drift_watcher — Doctrine consistency monitoring
  10. coverage_map — Triggered/missed doctrine tracking
  11. metrics_collector — Latency, error rates, hit rates
  12. health_endpoint — Comprehensive health check
  13. zoned_analysis — PLANNING / REPORTING / AUDIT zones
  14. fact_fragility_scoring — Verifiability and risk scoring
  15. audit_trail_jsonl — Forensic query logging
  16. determinism_hash_sha256 — Reproducibility hashing
  17. fastapi_server — FastAPI with CORS and typed endpoints
  18. loguru_logging — Structured logging
  19. multi_doctrine_decomposition — Issue strata and interaction DAG
  20. deep_analysis_mode — Multi-source synthesis
"""

# from __future__ import annotations  # DISABLED FOR TEST

import hashlib
import json
import os
import sys
import time
import uuid
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Optional

# ─── Cloud knowledge retrieval setup ──────────────────────────────────
from pathlib import Path as _Path
sys.path.insert(0, str(_Path(__file__).resolve().parent.parent / "_shared"))

import uvicorn
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import BaseModel, Field

# ─── Cloud knowledge retrieval import ─────────────────────────────────
try:
    from cloud_retriever import CognitionCloudRetriever, CloudKnowledge, retrieve_cloud_knowledge
    _CLOUD_AVAILABLE = True
except ImportError:
    _CLOUD_AVAILABLE = False
    logger.warning("cloud_retriever not available — running without cloud knowledge")

# ─── Local imports ────────────────────────────────────────────────────

# Ensure sibling modules are importable
ENGINE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ENGINE_DIR))
from doctrines import (
    ConfidenceLevel,
    DoctrineBlock,
    IssueCategory,
    build_doctrine_cache,
    get_all_doctrine_topics,
    get_doctrine_interaction_graph,
    get_doctrines_by_category,
)
from search import RunsheetVectorSearch, SearchDocument
from semantic import (
    InstrumentType,
    SemanticNormalizer,
)
from telemetry import (
    CoverageMap,
    DriftWatcher,
    ErrorDomain,
    MetricsCollector,
    QueryPhase,
    QueryTrace,
    TelemetryManager,
)

# ═══════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════

ENGINE_ID = "LM09"
ENGINE_NAME = "Runsheet Generator"
ENGINE_VERSION = "1.0.0"
ENGINE_PORT = 8509
ENGINE_DOMAIN = "landman_intelligence"
ENGINE_SUBDOMAIN = "title_examination"

LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR = Path(__file__).parent / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
VECTOR_DIR = Path(__file__).parent / "vectors"
VECTOR_DIR.mkdir(parents=True, exist_ok=True)

logger.remove()
logger.add(sys.stderr, level="INFO", format="<green>{time:HH:mm:ss}</green> | <level>{level:<7}</level> | <cyan>{name}</cyan> | {message}")
logger.add(LOG_DIR / "lm09_engine.log", rotation="10 MB", retention="30 days", level="DEBUG")

BANNED_PHRASES = [
    "this is not legal advice",
    "consult an attorney",
    "I am not a lawyer",
    "this is for informational purposes only",
    "you should seek professional",
]


# ═══════════════════════════════════════════════════════════════════════
# PYDANTIC MODELS
# ═══════════════════════════════════════════════════════════════════════

class ResponseMode(str, Enum):
    """Response mode for query processing."""
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"


class AnalysisZone(str, Enum):
    """Position zones that must never be blurred."""
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"


class QueryRequest(BaseModel):
    """Incoming query request."""
    query: str = Field(..., min_length=3, max_length=10000, description="The title examination or run sheet query")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response mode")
    zone: AnalysisZone = Field(default=AnalysisZone.REPORTING, description="Analysis zone")
    session_id: Optional[str] = Field(default=None, description="Session ID for tracking")
    issue_category: Optional[str] = Field(default=None, description="Specific issue category to focus on")
    county: Optional[str] = Field(default=None, description="Texas county for the examination")
    tract_description: Optional[str] = Field(default=None, description="Legal description of the tract")
    instruments: Optional[list[dict[str, Any]]] = Field(default=None, description="List of instruments for chain building")
    deep_analysis: bool = Field(default=False, description="Enable deep analysis mode")


class InstrumentEntry(BaseModel):
    """A single instrument entry for run sheet generation."""
    entry_number: int
    instrument_date: str
    recording_reference: str
    grantor: str
    grantee: str
    instrument_type: str
    legal_description: str
    consideration: Optional[str] = None
    remarks: Optional[str] = None
    reservations: Optional[list[str]] = None
    exceptions: Optional[list[str]] = None
    volume: Optional[str] = None
    page: Optional[str] = None
    clerks_file_number: Optional[str] = None


class InterestEntry(BaseModel):
    """Interest computation entry."""
    owner: str
    mineral_interest_fraction: str
    nma: float
    lease_status: str
    royalty_rate: Optional[str] = None
    nri: Optional[float] = None
    orri_burden: Optional[float] = None
    npri_burden: Optional[float] = None
    remarks: Optional[str] = None


class RunSheetOutput(BaseModel):
    """Complete run sheet output."""
    header: dict[str, Any]
    chain_of_title: list[dict[str, Any]]
    mineral_interests: list[dict[str, Any]]
    lease_summary: list[dict[str, Any]]
    encumbrances: list[dict[str, Any]]
    requirements: list[dict[str, Any]]
    interest_computation: list[dict[str, Any]]
    metadata: dict[str, Any]


class GapReport(BaseModel):
    """Gap in chain of title report."""
    gap_type: str
    description: str
    severity: str
    between_entries: list[int]
    curative_recommendation: str
    authority: str


class QueryResponse(BaseModel):
    """Query response envelope."""
    engine_id: str = ENGINE_ID
    engine_version: str = ENGINE_VERSION
    trace_id: str
    query_hash: str
    response_mode: str
    analysis_zone: str
    confidence_level: str
    confidence_score: float
    issue_category: str
    doctrine_hit: bool
    doctrine_topic: Optional[str] = None
    answer: str
    reasoning_framework: Optional[str] = None
    key_factors: Optional[list[str]] = None
    primary_authority: Optional[list[str]] = None
    counter_arguments: Optional[list[str]] = None
    resolution_strategy: Optional[str] = None
    run_sheet: Optional[dict[str, Any]] = None
    gaps_detected: Optional[list[dict[str, Any]]] = None
    interest_computation: Optional[list[dict[str, Any]]] = None
    fact_fragility: Optional[dict[str, Any]] = None
    interaction_edges: Optional[list[str]] = None
    cloud_knowledge: Optional[dict[str, Any]] = None
    cloud_citations: Optional[list[str]] = None
    determinism_hash: str
    latency_ms: float
    timestamp: str


class HealthResponse(BaseModel):
    """Health check response."""
    engine_id: str
    engine_name: str
    version: str
    status: str
    uptime_seconds: float
    doctrine_count: int
    vector_index_size: int
    total_queries: int
    error_rate: float
    cache_hit_rate: float
    last_query_time: Optional[str] = None
    timestamp: str


class NormalizeRequest(BaseModel):
    """Request for term normalization."""
    term: str
    category: Optional[str] = None


class LegalDescriptionRequest(BaseModel):
    """Request for legal description parsing."""
    description: str


class InterestComputationRequest(BaseModel):
    """Request for interest computation."""
    gross_acres: float
    mineral_chain: list[dict[str, Any]]
    lease_royalty_rate: float = 0.25
    orri_burdens: list[float] = Field(default_factory=list)
    npri_burdens: list[float] = Field(default_factory=list)


class ChainBuildRequest(BaseModel):
    """Request to build a chain of title."""
    instruments: list[dict[str, Any]]
    county: str
    tract_description: str
    effective_date: Optional[str] = None


# ═══════════════════════════════════════════════════════════════════════
# AUTHORITY HARDENING
# ═══════════════════════════════════════════════════════════════════════

AUTHORITY_HIERARCHY: list[dict[str, Any]] = [
    {"level": 1, "source": "Texas Constitution", "weight": 1.0},
    {"level": 2, "source": "Texas Property Code", "weight": 0.95},
    {"level": 3, "source": "Texas Natural Resources Code", "weight": 0.93},
    {"level": 4, "source": "Texas Estates Code", "weight": 0.92},
    {"level": 5, "source": "Texas Family Code", "weight": 0.91},
    {"level": 6, "source": "Texas Tax Code", "weight": 0.90},
    {"level": 7, "source": "Texas Supreme Court Decisions", "weight": 0.88},
    {"level": 8, "source": "Texas Courts of Appeals Decisions", "weight": 0.83},
    {"level": 9, "source": "TLTA Title Standards", "weight": 0.78},
    {"level": 10, "source": "AAPL Standards", "weight": 0.73},
    {"level": 11, "source": "Railroad Commission Rules", "weight": 0.70},
    {"level": 12, "source": "Industry Practice and Custom", "weight": 0.60},
]


def get_authority_weight(source: str) -> float:
    """Look up authority weight for a given source."""
    for entry in AUTHORITY_HIERARCHY:
        if entry["source"].lower() in source.lower() or source.lower() in entry["source"].lower():
            return entry["weight"]
    return 0.50


def rank_authorities(authorities: list[str]) -> list[dict[str, Any]]:
    """Rank a list of authorities by their hierarchy weight."""
    ranked = []
    for auth in authorities:
        weight = get_authority_weight(auth)
        ranked.append({"authority": auth, "weight": weight})
    ranked.sort(key=lambda x: x["weight"], reverse=True)
    return ranked


# ═══════════════════════════════════════════════════════════════════════
# CONFIDENCE STRATIFICATION
# ═══════════════════════════════════════════════════════════════════════

def stratify_confidence(score: float, has_controlling_precedent: bool, zone: AnalysisZone) -> ConfidenceLevel:
    """Stratify confidence into risk categories."""
    if zone == AnalysisZone.AUDIT:
        if score >= 0.90 and has_controlling_precedent:
            return ConfidenceLevel.DEFENSIBLE
        if score >= 0.75:
            return ConfidenceLevel.DISCLOSURE
        return ConfidenceLevel.HIGH_RISK
    if score >= 0.85 and has_controlling_precedent:
        return ConfidenceLevel.DEFENSIBLE
    if score >= 0.70:
        return ConfidenceLevel.AGGRESSIVE
    if score >= 0.50:
        return ConfidenceLevel.DISCLOSURE
    return ConfidenceLevel.HIGH_RISK


# ═══════════════════════════════════════════════════════════════════════
# FACT FRAGILITY SCORING
# ═══════════════════════════════════════════════════════════════════════

class FactFragilityScorer:
    """Scores the fragility of factual conclusions in title analysis."""

    def score(
        self,
        conclusion: str,
        authority_count: int,
        has_controlling_precedent: bool,
        counter_argument_count: int,
        instrument_count: int,
        gap_count: int,
    ) -> dict[str, Any]:
        """Compute fragility score for a title conclusion."""
        verifiability = min(1.0, authority_count / 4)
        if has_controlling_precedent:
            verifiability = min(1.0, verifiability + 0.2)
        recharacterization_risk = min(1.0, counter_argument_count / 5) * 0.7
        chain_completeness = 1.0 - min(1.0, gap_count / max(instrument_count, 1))
        testimony_dependence = 0.0
        testimony_terms = ["affidavit of heirship", "sworn statement", "testimony", "deposition"]
        conclusion_lower = conclusion.lower()
        for term in testimony_terms:
            if term in conclusion_lower:
                testimony_dependence += 0.25
        testimony_dependence = min(1.0, testimony_dependence)
        fragility_score = (
            (1.0 - verifiability) * 0.25
            + recharacterization_risk * 0.25
            + (1.0 - chain_completeness) * 0.30
            + testimony_dependence * 0.20
        )
        return {
            "fragility_score": round(fragility_score, 4),
            "verifiability": round(verifiability, 4),
            "recharacterization_risk": round(recharacterization_risk, 4),
            "chain_completeness": round(chain_completeness, 4),
            "testimony_dependence": round(testimony_dependence, 4),
            "risk_level": "LOW" if fragility_score < 0.3 else "MEDIUM" if fragility_score < 0.6 else "HIGH",
        }


# ═══════════════════════════════════════════════════════════════════════
# DETERMINISM HASH
# ═══════════════════════════════════════════════════════════════════════

def compute_determinism_hash(query: str, answer: str, doctrine_topic: Optional[str], confidence: float) -> str:
    """Generate SHA-256 determinism hash for reproducibility."""
    payload = json.dumps({
        "query": query.strip().lower(),
        "answer": answer.strip(),
        "doctrine_topic": doctrine_topic,
        "confidence": round(confidence, 4),
        "engine_id": ENGINE_ID,
        "engine_version": ENGINE_VERSION,
    }, sort_keys=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


# ═══════════════════════════════════════════════════════════════════════
# EPISTEMIC GUARDRAILS
# ═══════════════════════════════════════════════════════════════════════

def apply_epistemic_guardrails(text: str) -> str:
    """Remove banned phrases and add appropriate disclosure caveats."""
    result = text
    for phrase in BANNED_PHRASES:
        result = result.replace(phrase, "")
        result = result.replace(phrase.title(), "")
        result = result.replace(phrase.upper(), "")
    return result.strip()


def add_disclosure_caveat(confidence_level: ConfidenceLevel, zone: AnalysisZone) -> Optional[str]:
    """Generate appropriate disclosure caveat based on confidence and zone."""
    if confidence_level == ConfidenceLevel.HIGH_RISK:
        return (
            "DISCLOSURE: This analysis involves significant uncertainty. Key factual predicates "
            "remain unverified. Additional instruments or curative action may alter the conclusion. "
            "Independent verification of all chain links is recommended before relying on this analysis."
        )
    if confidence_level == ConfidenceLevel.DISCLOSURE:
        return (
            "DISCLOSURE: This analysis contains elements of interpretation where reasonable title "
            "examiners may reach different conclusions. The identified authorities support the stated "
            "position, but alternative interpretations exist as noted in the counter-arguments."
        )
    if confidence_level == ConfidenceLevel.AGGRESSIVE and zone == AnalysisZone.AUDIT:
        return (
            "NOTE: This position, while supported by authority, takes an aggressive interpretation "
            "that may not withstand challenge. Consider the counter-arguments when assessing risk."
        )
    return None


# ═══════════════════════════════════════════════════════════════════════
# MULTI-DOCTRINE DECOMPOSITION
# ═══════════════════════════════════════════════════════════════════════

class MultiDoctrineDecomposer:
    """Decomposes complex queries into multiple doctrine interactions."""

    def __init__(self, doctrine_cache: dict[str, DoctrineBlock]) -> None:
        self._cache = doctrine_cache
        self._interaction_graph = get_doctrine_interaction_graph()

    def decompose(self, query: str, primary_topic: str) -> dict[str, Any]:
        """Decompose a query into issue strata and interaction paths."""
        primary = self._cache.get(primary_topic)
        if not primary:
            return {"primary": None, "related": [], "interaction_path": []}
        related_topics = self._interaction_graph.get(primary_topic, [])
        related_doctrines = []
        for edge_topic in related_topics:
            edge_doctrine = self._cache.get(edge_topic)
            if edge_doctrine:
                relevance = self._compute_relevance(query, edge_doctrine)
                related_doctrines.append({
                    "topic": edge_topic,
                    "relevance": round(relevance, 4),
                    "issue_category": edge_doctrine.issue_category.value,
                    "confidence": edge_doctrine.confidence,
                })
        related_doctrines.sort(key=lambda x: x["relevance"], reverse=True)
        issue_strata = self._build_issue_strata(primary, related_doctrines)
        return {
            "primary_topic": primary_topic,
            "primary_category": primary.issue_category.value,
            "related_doctrines": related_doctrines,
            "issue_strata": issue_strata,
            "interaction_depth": len(related_doctrines),
            "composite_confidence": self._compute_composite_confidence(primary, related_doctrines),
        }

    def _compute_relevance(self, query: str, doctrine: DoctrineBlock) -> float:
        """Compute relevance of a doctrine to the query."""
        query_lower = query.lower()
        keyword_matches = sum(1 for kw in doctrine.keywords if kw.lower() in query_lower)
        return min(1.0, keyword_matches / max(len(doctrine.keywords), 1))

    def _build_issue_strata(self, primary: DoctrineBlock, related: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Build issue strata showing layered analysis requirements."""
        strata = [
            {
                "layer": 0,
                "topic": primary.topic,
                "category": primary.issue_category.value,
                "description": "Primary analysis layer",
            }
        ]
        for i, rel in enumerate(related[:5]):
            strata.append({
                "layer": i + 1,
                "topic": rel["topic"],
                "category": rel["issue_category"],
                "description": f"Related analysis — {rel['topic']}",
            })
        return strata

    def _compute_composite_confidence(self, primary: DoctrineBlock, related: list[dict[str, Any]]) -> float:
        """Compute composite confidence across all applicable doctrines."""
        if not related:
            return primary.confidence
        weights = [1.0]
        confidences = [primary.confidence]
        for rel in related[:3]:
            weights.append(rel["relevance"])
            confidences.append(rel["confidence"])
        total_weight = sum(weights)
        weighted_sum = sum(w * c for w, c in zip(weights, confidences))
        return round(weighted_sum / total_weight, 4) if total_weight > 0 else primary.confidence


# ═══════════════════════════════════════════════════════════════════════
# CHAIN OF TITLE BUILDER
# ═══════════════════════════════════════════════════════════════════════

class ChainOfTitleBuilder:
    """Builds and validates chains of title from instrument lists."""

    def __init__(self, normalizer: SemanticNormalizer) -> None:
        self._normalizer = normalizer

    def build_chain(self, instruments: list[dict[str, Any]]) -> dict[str, Any]:
        """Build a chain of title from a list of instruments."""
        sorted_instruments = sorted(instruments, key=lambda x: x.get("date", "1900-01-01"))
        chain: list[dict[str, Any]] = []
        for i, inst in enumerate(sorted_instruments):
            entry = {
                "entry_number": i + 1,
                "date": inst.get("date", "Unknown"),
                "recording_ref": inst.get("recording_ref", inst.get("volume_page", "Unknown")),
                "grantor": self._normalizer.normalize_party_name(inst.get("grantor", "Unknown")),
                "grantee": self._normalizer.normalize_party_name(inst.get("grantee", "Unknown")),
                "instrument_type": self._normalizer.normalize_instrument_type(inst.get("type", "Unknown")).normalized,
                "legal_description": inst.get("legal_description", ""),
                "consideration": inst.get("consideration", ""),
                "remarks": inst.get("remarks", ""),
                "reservations": inst.get("reservations", []),
                "exceptions": inst.get("exceptions", []),
            }
            chain.append(entry)
        return {
            "chain": chain,
            "instrument_count": len(chain),
            "date_range": {
                "earliest": chain[0]["date"] if chain else None,
                "latest": chain[-1]["date"] if chain else None,
            },
        }

    def detect_gaps(self, chain: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Detect gaps in the chain of title."""
        gaps: list[dict[str, Any]] = []
        for i in range(len(chain) - 1):
            current_grantee = chain[i]["grantee"].lower().strip()
            next_grantor = chain[i + 1]["grantor"].lower().strip()
            if current_grantee != next_grantor:
                name_sim = self._name_similarity(current_grantee, next_grantor)
                if name_sim < 0.8:
                    gap = {
                        "gap_type": self._classify_gap(current_grantee, next_grantor),
                        "description": f"Grantee of entry {chain[i]['entry_number']} ({chain[i]['grantee']}) "
                                       f"does not match grantor of entry {chain[i+1]['entry_number']} ({chain[i+1]['grantor']})",
                        "severity": "HIGH" if name_sim < 0.3 else "MEDIUM",
                        "between_entries": [chain[i]["entry_number"], chain[i + 1]["entry_number"]],
                        "name_similarity": round(name_sim, 4),
                        "curative_recommendation": self._recommend_curative(current_grantee, next_grantor, name_sim),
                    }
                    gaps.append(gap)
        return gaps

    def _name_similarity(self, name1: str, name2: str) -> float:
        """Compute simple name similarity ratio."""
        if name1 == name2:
            return 1.0
        words1 = set(name1.split())
        words2 = set(name2.split())
        if not words1 or not words2:
            return 0.0
        common = words1 & words2
        return len(common) / max(len(words1), len(words2))

    def _classify_gap(self, grantee: str, grantor: str) -> str:
        """Classify the type of gap."""
        grantee_words = set(grantee.split())
        grantor_words = set(grantor.split())
        common = grantee_words & grantor_words
        if len(common) >= 1 and len(common) < max(len(grantee_words), len(grantor_words)):
            return "NAME_VARIANCE"
        entity_indicators = {"llc", "inc", "corp", "lp", "ltd", "co"}
        if grantee_words & entity_indicators or grantor_words & entity_indicators:
            return "ENTITY_SUCCESSION"
        estate_indicators = {"estate", "heirs", "heir", "deceased", "trust"}
        if grantor_words & estate_indicators:
            return "PROBATE_GAP"
        return "UNRECORDED_CONVEYANCE"

    def _recommend_curative(self, grantee: str, grantor: str, similarity: float) -> str:
        """Recommend curative action for a gap."""
        gap_type = self._classify_gap(grantee, grantor)
        recommendations = {
            "NAME_VARIANCE": "Obtain affidavit of identity confirming the named parties are the same person. "
                            "Alternatively, obtain a correction deed or quitclaim deed.",
            "ENTITY_SUCCESSION": "Obtain evidence of entity succession — merger documents, certificate of name "
                                "change, or articles of dissolution. File corporate resolution confirming authority.",
            "PROBATE_GAP": "Obtain affidavit of heirship, muniment of title, or determination of heirship from "
                          "probate court. All heirs must be identified and accounted for.",
            "UNRECORDED_CONVEYANCE": "Obtain and record the missing conveyance. If unavailable, a quitclaim deed "
                                    "from the missing grantor or a quiet title action may be necessary.",
        }
        return recommendations.get(gap_type, "Conduct further investigation to resolve the gap in chain of title.")


# ═══════════════════════════════════════════════════════════════════════
# INTEREST CALCULATOR
# ═══════════════════════════════════════════════════════════════════════

class InterestCalculator:
    """Computes NMA, NRI, and decimal interests from chain data."""

    def compute_nma(self, gross_acres: float, mineral_interest_fraction: float) -> float:
        """Compute Net Mineral Acres."""
        return round(gross_acres * mineral_interest_fraction, 6)

    def compute_nri(
        self,
        working_interest: float,
        lease_royalty_rate: float,
        orri_burdens: list[float],
        npri_burdens: list[float],
    ) -> float:
        """Compute Net Revenue Interest."""
        lessor_royalty = lease_royalty_rate
        total_orri = sum(orri_burdens)
        total_npri = sum(npri_burdens)
        nri = working_interest * (1.0 - lessor_royalty) - total_orri
        effective_royalty = lessor_royalty - total_npri
        if effective_royalty < 0:
            effective_royalty = 0.0
        return round(max(0.0, nri), 6)

    def compute_decimal_interest(
        self,
        tract_nma: float,
        unit_total_nma: float,
        tract_nri: float,
    ) -> float:
        """Compute decimal interest for unit participation."""
        if unit_total_nma == 0:
            return 0.0
        participation_factor = tract_nma / unit_total_nma
        return round(participation_factor * tract_nri, 6)

    def trace_mineral_ownership(self, chain: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Trace mineral ownership through a chain of conveyances."""
        ownership: dict[str, float] = {}
        history: list[dict[str, Any]] = []
        for entry in chain:
            grantor = entry.get("grantor", "Unknown")
            grantee = entry.get("grantee", "Unknown")
            inst_type = entry.get("instrument_type", "").upper()
            if not ownership:
                ownership[grantee] = 1.0
                history.append({
                    "entry": entry.get("entry_number", 0),
                    "action": "Initial ownership established",
                    "ownership_after": dict(ownership),
                })
                continue
            if "MINERAL_DEED" in inst_type or "MINERAL" in entry.get("remarks", "").upper():
                fraction = self._extract_fraction(entry.get("remarks", ""), entry.get("consideration", ""))
                grantor_share = ownership.get(grantor, 0.0)
                conveyed = grantor_share * fraction
                ownership[grantor] = round(grantor_share - conveyed, 8)
                ownership[grantee] = round(ownership.get(grantee, 0.0) + conveyed, 8)
                if ownership[grantor] <= 0.0:
                    del ownership[grantor]
            elif "ROYALTY_DEED" in inst_type or "ROYALTY" in inst_type:
                history.append({
                    "entry": entry.get("entry_number", 0),
                    "action": "Royalty interest conveyed — tracked separately",
                    "ownership_after": dict(ownership),
                })
                continue
            elif "WARRANTY_DEED" in inst_type or "DEED" in inst_type:
                grantor_share = ownership.get(grantor, 0.0)
                reservations = entry.get("reservations", [])
                reserved_fraction = 0.0
                for res in reservations:
                    reserved_fraction += self._extract_fraction(res, "")
                conveyed = grantor_share * (1.0 - reserved_fraction)
                reserved = grantor_share * reserved_fraction
                if grantor in ownership:
                    del ownership[grantor]
                if reserved > 0:
                    ownership[grantor] = round(reserved, 8)
                ownership[grantee] = round(ownership.get(grantee, 0.0) + conveyed, 8)
            elif "LEASE" in inst_type or "OGL" in inst_type:
                history.append({
                    "entry": entry.get("entry_number", 0),
                    "action": "Lease recorded — affects leasehold interest",
                    "ownership_after": dict(ownership),
                })
                continue
            elif "ASSIGNMENT" in inst_type:
                history.append({
                    "entry": entry.get("entry_number", 0),
                    "action": "Assignment recorded — affects working interest",
                    "ownership_after": dict(ownership),
                })
                continue
            else:
                grantor_share = ownership.get(grantor, 0.0)
                if grantor_share > 0:
                    ownership[grantee] = round(ownership.get(grantee, 0.0) + grantor_share, 8)
                    del ownership[grantor]
            ownership = {k: v for k, v in ownership.items() if v > 0.0001}
            history.append({
                "entry": entry.get("entry_number", 0),
                "action": f"{inst_type} from {grantor} to {grantee}",
                "ownership_after": dict(ownership),
            })
        return history

    def _extract_fraction(self, text: str, consideration: str) -> float:
        """Extract a fractional interest from text."""
        import re
        patterns = [
            r"(\d+)/(\d+)",
            r"(\d+(?:\.\d+)?)\s*%",
            r"undivided\s+(\d+(?:\.\d+)?)",
        ]
        combined = f"{text} {consideration}"
        for pattern in patterns:
            match = re.search(pattern, combined, re.IGNORECASE)
            if match:
                groups = match.groups()
                if len(groups) == 2:
                    num, den = float(groups[0]), float(groups[1])
                    if den > 0 and num / den <= 1.0:
                        return num / den
                elif len(groups) == 1:
                    val = float(groups[0])
                    if val > 1:
                        return val / 100.0
                    return val
        return 0.5


# ═══════════════════════════════════════════════════════════════════════
# RUN SHEET FORMATTER
# ═══════════════════════════════════════════════════════════════════════

class RunSheetFormatter:
    """Formats chain of title data into standard run sheet format."""

    def format_header(
        self,
        county: str,
        state: str,
        tract_description: str,
        effective_date: str,
        prepared_by: str = "LM09 Runsheet Generator Engine",
        scope: str = "Full chain of title examination",
    ) -> dict[str, Any]:
        """Format the run sheet header block."""
        return {
            "county": county,
            "state": state,
            "tract_description": tract_description,
            "effective_date": effective_date,
            "prepared_by": prepared_by,
            "scope_of_examination": scope,
            "engine_id": ENGINE_ID,
            "engine_version": ENGINE_VERSION,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    def format_chain_entry(self, entry: dict[str, Any]) -> dict[str, Any]:
        """Format a single chain of title entry."""
        return {
            "entry_no": entry.get("entry_number", 0),
            "date": entry.get("date", ""),
            "recording_ref": entry.get("recording_ref", ""),
            "grantor": entry.get("grantor", ""),
            "grantee": entry.get("grantee", ""),
            "type": entry.get("instrument_type", ""),
            "legal_description": entry.get("legal_description", ""),
            "consideration": entry.get("consideration", ""),
            "remarks": entry.get("remarks", ""),
        }

    def format_requirement(self, gap: dict[str, Any], req_number: int) -> dict[str, Any]:
        """Format a title requirement from a gap."""
        return {
            "requirement_no": req_number,
            "type": gap.get("gap_type", "UNKNOWN"),
            "severity": gap.get("severity", "MEDIUM"),
            "description": gap.get("description", ""),
            "curative_action": gap.get("curative_recommendation", ""),
            "between_entries": gap.get("between_entries", []),
            "status": "OPEN",
        }

    def generate_full_runsheet(
        self,
        header: dict[str, Any],
        chain: list[dict[str, Any]],
        gaps: list[dict[str, Any]],
        ownership_history: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Generate a complete run sheet document."""
        formatted_chain = [self.format_chain_entry(e) for e in chain]
        requirements = [self.format_requirement(g, i + 1) for i, g in enumerate(gaps)]
        current_ownership = ownership_history[-1]["ownership_after"] if ownership_history else {}
        interest_summary = [
            {"owner": owner, "mineral_fraction": round(fraction, 6)}
            for owner, fraction in sorted(current_ownership.items(), key=lambda x: x[1], reverse=True)
        ]
        return {
            "header": header,
            "chain_of_title": formatted_chain,
            "mineral_interests": interest_summary,
            "lease_summary": [],
            "encumbrances": [],
            "requirements": requirements,
            "interest_computation": interest_summary,
            "ownership_trace": ownership_history,
            "summary": {
                "total_instruments": len(chain),
                "total_gaps": len(gaps),
                "total_requirements": len(requirements),
                "current_owners": len(current_ownership),
                "gap_severity_breakdown": {
                    "HIGH": sum(1 for g in gaps if g.get("severity") == "HIGH"),
                    "MEDIUM": sum(1 for g in gaps if g.get("severity") == "MEDIUM"),
                    "LOW": sum(1 for g in gaps if g.get("severity") == "LOW"),
                },
            },
        }


# ═══════════════════════════════════════════════════════════════════════
# THREE-LAYER RESPONSE ENGINE
# ═══════════════════════════════════════════════════════════════════════

class ThreeLayerResponseEngine:
    """
    Layer 1: Doctrine Cache (0-200ms) — pre-compiled expert reasoning
    Layer 2: Semantic Retrieval — vector search fallback
    Layer 3: Deep Analysis — multi-source synthesis
    """

    def __init__(
        self,
        doctrine_cache: dict[str, DoctrineBlock],
        vector_search: RunsheetVectorSearch,
        normalizer: SemanticNormalizer,
        telemetry: TelemetryManager,
        chain_builder: ChainOfTitleBuilder,
        interest_calculator: InterestCalculator,
        formatter: RunSheetFormatter,
        fragility_scorer: FactFragilityScorer,
        decomposer: MultiDoctrineDecomposer,
    ) -> None:
        self._doctrine_cache = doctrine_cache
        self._vector_search = vector_search
        self._normalizer = normalizer
        self._telemetry = telemetry
        self._chain_builder = chain_builder
        self._interest_calculator = interest_calculator
        self._formatter = formatter
        self._fragility_scorer = fragility_scorer
        self._decomposer = decomposer
        logger.info("ThreeLayerResponseEngine initialized with {} doctrines", len(doctrine_cache))

    def process_query(self, request: QueryRequest) -> QueryResponse:
        """Process a query through the three-layer response system."""
        session_id = request.session_id or str(uuid.uuid4())
        trace = self._telemetry.start_query(
            query_text=request.query,
            session_id=session_id,
            response_mode=request.mode.value,
            issue_category=request.issue_category or "UNKNOWN",
        )

        # Retrieve cloud knowledge (sync-safe: use new thread event loop)
        cloud_data = {}
        cloud_citations = []
        if _CLOUD_AVAILABLE:
            try:
                import asyncio
                try:
                    loop = asyncio.get_running_loop()
                except RuntimeError:
                    loop = None
                if loop and loop.is_running():
                    # Already in async context — skip cloud retrieval to avoid deadlock
                    logger.debug("Skipping cloud retrieval in async context")
                else:
                    cloud = asyncio.run(retrieve_cloud_knowledge(request.query, category="runsheet"))
                    cloud_data = {
                        "records": len(cloud.clauses) + len(cloud.graph_nodes) + len(cloud.crystals),
                        "merged_context": cloud.merged_text(3000),
                        "sources_succeeded": cloud.sources_succeeded,
                        "retrieval_time_ms": cloud.retrieval_time_ms,
                    }
                    cloud_citations = cloud.citation_list()
            except Exception as e:
                logger.warning(f"Cloud retrieval failed: {e}")

        try:
            trace.enter_phase(QueryPhase.VALIDATED)
            doctrine_result = self._layer1_doctrine_cache(request.query, trace)
            if doctrine_result and request.mode == ResponseMode.FAST and not request.deep_analysis:
                return self._build_response(request, trace, doctrine_result, session_id, cloud_data, cloud_citations)
            if not doctrine_result:
                trace.enter_phase(QueryPhase.SEMANTIC_SEARCH)
                trace.vector_fallback = True
                semantic_result = self._layer2_semantic_search(request.query, trace)
                if semantic_result and request.mode == ResponseMode.FAST:
                    return self._build_response(request, trace, semantic_result, session_id, cloud_data, cloud_citations)
                doctrine_result = semantic_result
            if request.deep_analysis or request.mode in (ResponseMode.DEFENSE, ResponseMode.MEMO):
                trace.enter_phase(QueryPhase.DEEP_ANALYSIS)
                trace.deep_analysis = True
                deep_result = self._layer3_deep_analysis(request, doctrine_result, trace)
                return self._build_response(request, trace, deep_result, session_id, cloud_data, cloud_citations)
            if doctrine_result:
                return self._build_response(request, trace, doctrine_result, session_id, cloud_data, cloud_citations)
            return self._build_fallback_response(request, trace, session_id, cloud_data, cloud_citations)
        except Exception as exc:
            logger.error("Query processing error: {}", exc)
            trace.fail(ErrorDomain.UNKNOWN, str(exc))
            self._telemetry.end_query(trace)
            raise HTTPException(status_code=500, detail=f"Query processing error: {exc}") from exc

    def _layer1_doctrine_cache(self, query: str, trace: QueryTrace) -> Optional[dict[str, Any]]:
        """Layer 1: Search doctrine cache for matching pre-compiled reasoning."""
        trace.enter_phase(QueryPhase.DOCTRINE_LOOKUP)
        query_lower = query.lower()
        best_match: Optional[tuple[str, DoctrineBlock, int]] = None
        best_score = 0
        for topic, doctrine in self._doctrine_cache.items():
            score = sum(1 for kw in doctrine.keywords if kw.lower() in query_lower)
            if score > best_score:
                best_score = score
                best_match = (topic, doctrine, score)
        if best_match and best_match[2] >= 2:
            topic, doctrine, score = best_match
            trace.doctrine_hit = True
            trace.doctrine_topic = topic
            logger.info("Doctrine cache hit: topic={} score={}", topic, score)
            return {
                "source": "doctrine_cache",
                "topic": topic,
                "doctrine": doctrine,
                "match_score": score,
            }
        logger.debug("Doctrine cache miss for query")
        return None

    def _layer2_semantic_search(self, query: str, trace: QueryTrace) -> Optional[dict[str, Any]]:
        """Layer 2: Semantic vector search fallback."""
        results = self._vector_search.search(query, top_k=5, min_score=0.05)
        if results:
            top = results[0]
            matched_topic = None
            for topic, doctrine in self._doctrine_cache.items():
                if top.category.lower() in topic.lower() or topic.lower() in top.title.lower():
                    matched_topic = topic
                    break
            if matched_topic:
                trace.doctrine_topic = matched_topic
                return {
                    "source": "semantic_search",
                    "topic": matched_topic,
                    "doctrine": self._doctrine_cache[matched_topic],
                    "search_results": results[:3],
                    "match_score": top.relevance_score,
                }
            return {
                "source": "semantic_search",
                "topic": None,
                "doctrine": None,
                "search_results": results[:3],
                "match_score": top.relevance_score,
            }
        return None

    def _layer3_deep_analysis(
        self,
        request: QueryRequest,
        prior_result: Optional[dict[str, Any]],
        trace: QueryTrace,
    ) -> dict[str, Any]:
        """Layer 3: Deep analysis with multi-source synthesis."""
        result: dict[str, Any] = prior_result or {"source": "deep_analysis", "doctrine": None, "topic": None}
        result["source"] = "deep_analysis"
        if request.instruments:
            trace.enter_phase(QueryPhase.CHAIN_BUILD)
            chain_data = self._chain_builder.build_chain(request.instruments)
            trace.instruments_processed = chain_data["instrument_count"]
            trace.enter_phase(QueryPhase.GAP_CHECK)
            gaps = self._chain_builder.detect_gaps(chain_data["chain"])
            trace.gaps_detected = len(gaps)
            ownership = self._interest_calculator.trace_mineral_ownership(chain_data["chain"])
            trace.enter_phase(QueryPhase.FORMAT_OUTPUT)
            header = self._formatter.format_header(
                county=request.county or "Unknown",
                state="Texas",
                tract_description=request.tract_description or "See instruments",
                effective_date=datetime.now(timezone.utc).strftime("%m/%d/%Y"),
            )
            run_sheet = self._formatter.generate_full_runsheet(
                header=header,
                chain=chain_data["chain"],
                gaps=gaps,
                ownership_history=ownership,
            )
            result["run_sheet"] = run_sheet
            result["gaps"] = gaps
            result["ownership_history"] = ownership
        if result.get("topic"):
            decomposition = self._decomposer.decompose(request.query, result["topic"])
            result["decomposition"] = decomposition
        return result

    def _build_response(
        self,
        request: QueryRequest,
        trace: QueryTrace,
        result: dict[str, Any],
        session_id: str,
        cloud_data: dict[str, Any] = None,
        cloud_citations: list[str] = None,
    ) -> QueryResponse:
        """Build the final query response."""
        doctrine: Optional[DoctrineBlock] = result.get("doctrine")
        topic = result.get("topic")
        if doctrine:
            answer = self._format_answer(doctrine, request.mode, request.zone)
            confidence_score = doctrine.confidence
            has_precedent = bool(doctrine.controlling_precedent)
            confidence_level = stratify_confidence(confidence_score, has_precedent, request.zone)
            issue_category = doctrine.issue_category.value
            reasoning = doctrine.reasoning_framework if request.mode != ResponseMode.FAST else None
            key_factors = doctrine.key_factors
            authorities = doctrine.primary_authority
            counter_args = doctrine.counter_arguments if request.mode in (ResponseMode.DEFENSE, ResponseMode.MEMO) else None
            resolution = doctrine.resolution_strategy
            interaction_edges = doctrine.interaction_edges
        else:
            answer = self._format_generic_answer(request.query, result)
            confidence_score = 0.50
            confidence_level = ConfidenceLevel.DISCLOSURE
            issue_category = request.issue_category or "UNKNOWN"
            reasoning = None
            key_factors = None
            authorities = None
            counter_args = None
            resolution = None
            interaction_edges = None
        answer = apply_epistemic_guardrails(answer)
        caveat = add_disclosure_caveat(confidence_level, request.zone)
        if caveat:
            answer = f"{answer}\n\n{caveat}"
        determinism_hash = compute_determinism_hash(request.query, answer, topic, confidence_score)
        trace.complete(determinism_hash=determinism_hash)
        trace.result_size_bytes = len(answer.encode("utf-8"))
        trace.confidence_level = confidence_level.value
        trace.issue_category = issue_category
        fragility = None
        if doctrine:
            fragility = self._fragility_scorer.score(
                conclusion=answer,
                authority_count=len(doctrine.primary_authority),
                has_controlling_precedent=bool(doctrine.controlling_precedent),
                counter_argument_count=len(doctrine.counter_arguments),
                instrument_count=trace.instruments_processed,
                gap_count=trace.gaps_detected,
            )
        self._telemetry.end_query(trace, doctrine_topic=topic, determinism_hash=determinism_hash)
        return QueryResponse(
            trace_id=trace.trace_id,
            query_hash=trace.query_hash,
            response_mode=request.mode.value,
            analysis_zone=request.zone.value,
            confidence_level=confidence_level.value,
            confidence_score=confidence_score,
            issue_category=issue_category,
            doctrine_hit=trace.doctrine_hit,
            doctrine_topic=topic,
            answer=answer,
            reasoning_framework=reasoning,
            key_factors=key_factors,
            primary_authority=authorities,
            counter_arguments=counter_args,
            resolution_strategy=resolution,
            run_sheet=result.get("run_sheet"),
            gaps_detected=result.get("gaps"),
            interest_computation=result.get("ownership_history"),
            fact_fragility=fragility,
            interaction_edges=interaction_edges,
            cloud_knowledge=cloud_data or {},
            cloud_citations=cloud_citations or [],
            determinism_hash=determinism_hash,
            latency_ms=round(trace.total_duration_ms or 0, 2),
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

    def _build_fallback_response(
        self,
        request: QueryRequest,
        trace: QueryTrace,
        session_id: str,
        cloud_data: dict[str, Any] = None,
        cloud_citations: list[str] = None,
    ) -> QueryResponse:
        """Build a fallback response when no doctrine matches."""
        answer = (
            f"The query regarding '{request.query[:100]}...' does not match a specific pre-compiled doctrine "
            f"in the LM09 Runsheet Generator engine. This may involve a specialized or novel title examination "
            f"scenario. The engine covers {len(self._doctrine_cache)} doctrine topics across chain of title, "
            f"interest computation, legal description, lease analysis, mineral rights, probate/heirship, "
            f"reservations/exceptions, gap detection, run sheet formatting, and title standards. "
            f"Consider refining the query to target one of these areas specifically."
        )
        answer = apply_epistemic_guardrails(answer)
        determinism_hash = compute_determinism_hash(request.query, answer, None, 0.30)
        trace.complete(determinism_hash=determinism_hash)
        self._telemetry.end_query(trace)
        return QueryResponse(
            trace_id=trace.trace_id,
            query_hash=trace.query_hash,
            response_mode=request.mode.value,
            analysis_zone=request.zone.value,
            confidence_level=ConfidenceLevel.HIGH_RISK.value,
            confidence_score=0.30,
            issue_category=request.issue_category or "UNKNOWN",
            doctrine_hit=False,
            doctrine_topic=None,
            answer=answer,
            cloud_knowledge=cloud_data or {},
            cloud_citations=cloud_citations or [],
            determinism_hash=determinism_hash,
            latency_ms=round(trace.total_duration_ms or 0, 2),
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

    def _format_answer(self, doctrine: DoctrineBlock, mode: ResponseMode, zone: AnalysisZone) -> str:
        """Format the answer based on response mode."""
        if mode == ResponseMode.FAST:
            return doctrine.conclusion_template
        if mode == ResponseMode.DEFENSE:
            sections = [
                f"TOPIC: {doctrine.topic}",
                f"\nCONCLUSION:\n{doctrine.conclusion_template}",
                f"\nANALYSIS FRAMEWORK:\n{doctrine.reasoning_framework}",
                f"\nKEY FACTORS:\n" + "\n".join(f"  - {f}" for f in doctrine.key_factors),
                f"\nPRIMARY AUTHORITY:\n" + "\n".join(f"  - {a}" for a in doctrine.primary_authority),
                f"\nCONTROLLING PRECEDENT: {doctrine.controlling_precedent}",
                f"\nCOUNTER-ARGUMENTS:\n" + "\n".join(f"  - {c}" for c in doctrine.counter_arguments),
                f"\nRESOLUTION STRATEGY:\n{doctrine.resolution_strategy}",
                f"\nCONFIDENCE: {doctrine.confidence} ({doctrine.confidence_stratification.value})",
            ]
            return "\n".join(sections)
        if mode == ResponseMode.MEMO:
            sections = [
                "=" * 60,
                f"MEMORANDUM — {doctrine.topic}",
                "=" * 60,
                f"\nISSUE CATEGORY: {doctrine.issue_category.value}",
                f"CONFIDENCE LEVEL: {doctrine.confidence_stratification.value} ({doctrine.confidence})",
                f"BURDEN OF PROOF: {doctrine.burden_holder}",
                f"ADVERSE PARTY POSITION: {doctrine.adversary_position}",
                f"\n{'─' * 40}\nCONCLUSION\n{'─' * 40}\n{doctrine.conclusion_template}",
                f"\n{'─' * 40}\nANALYSIS\n{'─' * 40}\n{doctrine.reasoning_framework}",
                f"\n{'─' * 40}\nKEY FACTORS\n{'─' * 40}",
                "\n".join(f"  {i+1}. {f}" for i, f in enumerate(doctrine.key_factors)),
                f"\n{'─' * 40}\nAUTHORITIES\n{'─' * 40}",
                "\n".join(f"  [{i+1}] {a}" for i, a in enumerate(doctrine.primary_authority)),
                f"\n  CONTROLLING: {doctrine.controlling_precedent}",
                f"\n{'─' * 40}\nCOUNTER-ARGUMENTS\n{'─' * 40}",
                "\n".join(f"  {i+1}. {c}" for i, c in enumerate(doctrine.counter_arguments)),
                f"\n{'─' * 40}\nRESOLUTION STRATEGY\n{'─' * 40}\n{doctrine.resolution_strategy}",
                f"\n{'─' * 40}\nRELATED DOCTRINES\n{'─' * 40}",
                "\n".join(f"  - {e}" for e in doctrine.interaction_edges) if doctrine.interaction_edges else "  None",
                f"\n{'─' * 40}\nSCOPE\n{'─' * 40}\n  Entity scope: {doctrine.entity_scope}",
                f"\n{'=' * 60}",
                f"Generated by {ENGINE_ID} {ENGINE_NAME} v{ENGINE_VERSION}",
                f"{'=' * 60}",
            ]
            return "\n".join(sections)
        return doctrine.conclusion_template

    def _format_generic_answer(self, query: str, result: dict[str, Any]) -> str:
        """Format a generic answer when no doctrine matched directly."""
        parts = [f"Analysis of query: {query[:200]}"]
        if result.get("search_results"):
            parts.append("\nRelated topics found via semantic search:")
            for sr in result["search_results"][:3]:
                parts.append(f"  - {sr.title} (relevance: {sr.relevance_score})")
        if result.get("run_sheet"):
            parts.append("\nRun sheet generated from provided instruments.")
        return "\n".join(parts)


# ═══════════════════════════════════════════════════════════════════════
# VECTOR INDEX SEED DATA
# ═══════════════════════════════════════════════════════════════════════

def seed_vector_index(vector_search: RunsheetVectorSearch, doctrines: dict[str, DoctrineBlock]) -> None:
    """Seed the vector index with doctrine-derived documents."""
    docs = []
    for topic, doctrine in doctrines.items():
        content = f"{doctrine.conclusion_template}\n\n{doctrine.reasoning_framework}"
        docs.append(SearchDocument(
            doc_id=f"doctrine_{topic}",
            title=doctrine.topic,
            content=content,
            category=doctrine.issue_category.value,
            keywords=doctrine.keywords,
            authority_weight=doctrine.confidence,
        ))
    vector_search.add_documents(docs)
    logger.info("Seeded vector index with {} doctrine documents", len(docs))


# ═══════════════════════════════════════════════════════════════════════
# FASTAPI APPLICATION
# ═══════════════════════════════════════════════════════════════════════

doctrine_cache: dict[str, DoctrineBlock] = {}
normalizer: Optional[SemanticNormalizer] = None
vector_search: Optional[RunsheetVectorSearch] = None
telemetry_mgr: Optional[TelemetryManager] = None
response_engine: Optional[ThreeLayerResponseEngine] = None
chain_builder: Optional[ChainOfTitleBuilder] = None
interest_calc: Optional[InterestCalculator] = None
formatter: Optional[RunSheetFormatter] = None
fragility_scorer: Optional[FactFragilityScorer] = None
decomposer: Optional[MultiDoctrineDecomposer] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and tear down engine components."""
    global doctrine_cache, normalizer, vector_search, telemetry_mgr
    global response_engine, chain_builder, interest_calc, formatter
    global fragility_scorer, decomposer

    logger.info("LM09 Runsheet Generator Engine starting on port {}", ENGINE_PORT)

    doctrine_cache = build_doctrine_cache()
    logger.info("Loaded {} doctrines", len(doctrine_cache))

    normalizer = SemanticNormalizer()
    vector_search = RunsheetVectorSearch(index_path=VECTOR_DIR / "lm09_runsheet.db")
    seed_vector_index(vector_search, doctrine_cache)

    all_topics = get_all_doctrine_topics()
    telemetry_mgr = TelemetryManager(
        engine_id=ENGINE_ID,
        doctrine_topics=all_topics,
        audit_log_path=LOG_DIR / "lm09_audit.jsonl",
    )

    chain_builder = ChainOfTitleBuilder(normalizer)
    interest_calc = InterestCalculator()
    formatter = RunSheetFormatter()
    fragility_scorer = FactFragilityScorer()
    decomposer = MultiDoctrineDecomposer(doctrine_cache)

    response_engine = ThreeLayerResponseEngine(
        doctrine_cache=doctrine_cache,
        vector_search=vector_search,
        normalizer=normalizer,
        telemetry=telemetry_mgr,
        chain_builder=chain_builder,
        interest_calculator=interest_calc,
        formatter=formatter,
        fragility_scorer=fragility_scorer,
        decomposer=decomposer,
    )

    logger.info("LM09 engine fully initialized — {} doctrines, vector index seeded", len(doctrine_cache))
    yield
    logger.info("LM09 engine shutting down")
    if _CLOUD_AVAILABLE:
        try:
            retriever = CognitionCloudRetriever()
            await retriever.close()
            logger.info("Cloud retriever client closed")
        except Exception as e:
            logger.warning(f"Failed to close cloud retriever: {e}")


# When running as __main__, skip lifespan on the module-level app — the __main__
# block creates its own fresh app with lifespan + fresh routes.  Having TWO apps
# with the same lifespan in the same process causes ASGI middleware stack corruption
# (TCP connects but HTTP never processes).
app = FastAPI(
    title=f"{ENGINE_ID} {ENGINE_NAME}",
    version=ENGINE_VERSION,
    description="Automated run sheet and abstract generation for oil & gas title examination",
    lifespan=lifespan if __name__ != "__main__" else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── ENDPOINTS ────────────────────────────────────────────────────────

@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Comprehensive health check endpoint."""
    metrics = telemetry_mgr.metrics.get_comprehensive_metrics() if telemetry_mgr else {}
    hit_rates = telemetry_mgr.metrics.get_hit_rates() if telemetry_mgr else {}
    error_rates = telemetry_mgr.metrics.get_error_rates() if telemetry_mgr else {}
    return HealthResponse(
        engine_id=ENGINE_ID,
        engine_name=ENGINE_NAME,
        version=ENGINE_VERSION,
        status="HEALTHY",
        uptime_seconds=telemetry_mgr.metrics.get_uptime_seconds() if telemetry_mgr else 0,
        doctrine_count=len(doctrine_cache),
        vector_index_size=vector_search.get_index_stats()["total_documents"] if vector_search else 0,
        total_queries=error_rates.get("total_queries", 0),
        error_rate=error_rates.get("error_rate", 0.0),
        cache_hit_rate=hit_rates.get("hit_rate", 0.0),
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest) -> QueryResponse:
    """Process a title examination or run sheet query through the three-layer engine."""
    if not response_engine:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    return response_engine.process_query(request)


@app.post("/chain/build")
async def build_chain(request: ChainBuildRequest) -> dict[str, Any]:
    """Build a chain of title from instruments."""
    if not chain_builder or not interest_calc or not formatter:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    chain_data = chain_builder.build_chain(request.instruments)
    gaps = chain_builder.detect_gaps(chain_data["chain"])
    ownership = interest_calc.trace_mineral_ownership(chain_data["chain"])
    header = formatter.format_header(
        county=request.county,
        state="Texas",
        tract_description=request.tract_description,
        effective_date=request.effective_date or datetime.now(timezone.utc).strftime("%m/%d/%Y"),
    )
    run_sheet = formatter.generate_full_runsheet(
        header=header,
        chain=chain_data["chain"],
        gaps=gaps,
        ownership_history=ownership,
    )
    return run_sheet


@app.post("/chain/gaps")
async def detect_chain_gaps(instruments: list[dict[str, Any]]) -> dict[str, Any]:
    """Detect gaps in a chain of title."""
    if not chain_builder:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    chain_data = chain_builder.build_chain(instruments)
    gaps = chain_builder.detect_gaps(chain_data["chain"])
    return {
        "instrument_count": len(chain_data["chain"]),
        "gaps_detected": len(gaps),
        "gaps": gaps,
    }


@app.post("/interest/compute")
async def compute_interest(request: InterestComputationRequest) -> dict[str, Any]:
    """Compute NMA, NRI, and decimal interests."""
    if not interest_calc:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    results = []
    for entry in request.mineral_chain:
        owner = entry.get("owner", "Unknown")
        fraction = entry.get("mineral_fraction", 1.0)
        nma = interest_calc.compute_nma(request.gross_acres, fraction)
        nri = interest_calc.compute_nri(
            working_interest=1.0,
            lease_royalty_rate=request.lease_royalty_rate,
            orri_burdens=request.orri_burdens,
            npri_burdens=request.npri_burdens,
        )
        results.append({
            "owner": owner,
            "mineral_fraction": fraction,
            "nma": nma,
            "nri": round(nri * fraction, 6),
            "decimal_interest": round(nri * fraction, 6),
        })
    return {
        "gross_acres": request.gross_acres,
        "lease_royalty_rate": request.lease_royalty_rate,
        "total_orri_burden": sum(request.orri_burdens),
        "total_npri_burden": sum(request.npri_burdens),
        "interest_allocation": results,
        "total_nma": round(sum(r["nma"] for r in results), 6),
        "total_decimal": round(sum(r["decimal_interest"] for r in results), 6),
    }


@app.post("/normalize")
async def normalize_term(request: NormalizeRequest) -> dict[str, Any]:
    """Normalize a title examination term."""
    if not normalizer:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    if request.category == "instrument":
        result = normalizer.normalize_instrument_type(request.term)
    elif request.category == "legal":
        result = normalizer.normalize_legal_term(request.term)
    elif request.category == "party":
        result = normalizer.normalize_party_designation(request.term)
    elif request.category == "curative":
        result = normalizer.normalize_curative_term(request.term)
    else:
        result = normalizer.normalize_any(request.term)
    return {
        "original": result.original,
        "normalized": result.normalized,
        "category": result.category,
        "confidence": result.confidence,
        "match_type": result.match_type,
    }


@app.post("/legal-description/parse")
async def parse_legal_description(request: LegalDescriptionRequest) -> dict[str, Any]:
    """Parse a legal description into structured components."""
    if not normalizer:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    return normalizer.extract_legal_description_components(request.description)


@app.get("/doctrines")
async def list_doctrines(
    category: Optional[str] = Query(default=None, description="Filter by issue category"),
) -> dict[str, Any]:
    """List all available doctrines."""
    if category:
        try:
            cat = IssueCategory(category)
            filtered = get_doctrines_by_category(cat)
            return {
                "category": category,
                "count": len(filtered),
                "doctrines": [
                    {"topic": d.topic, "confidence": d.confidence, "keywords": d.keywords}
                    for d in filtered
                ],
            }
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid category: {category}")
    return {
        "total": len(doctrine_cache),
        "categories": {cat.value: 0 for cat in IssueCategory},
        "doctrines": [
            {
                "topic_key": key,
                "topic": d.topic,
                "category": d.issue_category.value,
                "confidence": d.confidence,
                "keywords": d.keywords,
            }
            for key, d in doctrine_cache.items()
        ],
    }


@app.get("/doctrines/{topic_key}")
async def get_doctrine_detail(topic_key: str) -> dict[str, Any]:
    """Get detailed information about a specific doctrine."""
    doctrine = doctrine_cache.get(topic_key)
    if not doctrine:
        raise HTTPException(status_code=404, detail=f"Doctrine not found: {topic_key}")
    return {
        "topic_key": topic_key,
        "topic": doctrine.topic,
        "issue_category": doctrine.issue_category.value,
        "keywords": doctrine.keywords,
        "conclusion_template": doctrine.conclusion_template,
        "reasoning_framework": doctrine.reasoning_framework,
        "key_factors": doctrine.key_factors,
        "primary_authority": doctrine.primary_authority,
        "controlling_precedent": doctrine.controlling_precedent,
        "burden_holder": doctrine.burden_holder,
        "adversary_position": doctrine.adversary_position,
        "counter_arguments": doctrine.counter_arguments,
        "resolution_strategy": doctrine.resolution_strategy,
        "entity_scope": doctrine.entity_scope,
        "confidence": doctrine.confidence,
        "confidence_stratification": doctrine.confidence_stratification.value,
        "interaction_edges": doctrine.interaction_edges,
    }


@app.get("/doctrines/graph/interactions")
async def get_interaction_graph() -> dict[str, Any]:
    """Get the doctrine interaction graph."""
    graph = get_doctrine_interaction_graph()
    return {
        "total_doctrines": len(graph),
        "total_edges": sum(len(edges) for edges in graph.values()),
        "graph": graph,
    }


@app.get("/telemetry")
async def get_telemetry() -> dict[str, Any]:
    """Get comprehensive telemetry data."""
    if not telemetry_mgr:
        raise HTTPException(status_code=503, detail="Telemetry not initialized")
    return telemetry_mgr.get_full_telemetry()


@app.get("/telemetry/metrics")
async def get_metrics() -> dict[str, Any]:
    """Get performance metrics."""
    if not telemetry_mgr:
        raise HTTPException(status_code=503, detail="Telemetry not initialized")
    return telemetry_mgr.metrics.get_comprehensive_metrics()


@app.get("/telemetry/drift")
async def get_drift_report() -> dict[str, Any]:
    """Get doctrine drift analysis report."""
    if not telemetry_mgr:
        raise HTTPException(status_code=503, detail="Telemetry not initialized")
    return telemetry_mgr.drift_watcher.get_drift_report()


@app.get("/telemetry/coverage")
async def get_coverage_report() -> dict[str, Any]:
    """Get doctrine coverage report."""
    if not telemetry_mgr:
        raise HTTPException(status_code=503, detail="Telemetry not initialized")
    return telemetry_mgr.coverage_map.get_coverage_report()


@app.get("/search")
async def search_knowledge(
    q: str = Query(..., min_length=2, description="Search query"),
    top_k: int = Query(default=10, ge=1, le=50),
    category: Optional[str] = Query(default=None),
) -> dict[str, Any]:
    """Search the vector knowledge base."""
    if not vector_search:
        raise HTTPException(status_code=503, detail="Vector search not initialized")
    results = vector_search.search(q, top_k=top_k, category_filter=category)
    return {
        "query": q,
        "results_count": len(results),
        "results": [
            {
                "doc_id": r.doc_id,
                "title": r.title,
                "snippet": r.content_snippet,
                "category": r.category,
                "relevance": r.relevance_score,
                "combined_score": r.combined_score,
                "matched_keywords": r.matched_keywords,
            }
            for r in results
        ],
    }


@app.get("/authority")
async def get_authority_hierarchy() -> dict[str, Any]:
    """Get the authority hierarchy for Texas title examination."""
    return {
        "hierarchy": AUTHORITY_HIERARCHY,
        "total_levels": len(AUTHORITY_HIERARCHY),
    }


@app.get("/instrument-types")
async def get_instrument_types() -> dict[str, Any]:
    """Get all recognized instrument types and their aliases."""
    type_aliases: dict[str, list[str]] = {}
    for alias, inst_type in INSTRUMENT_ALIASES.items():
        key = inst_type.value
        if key not in type_aliases:
            type_aliases[key] = []
        type_aliases[key].append(alias)
    return {
        "total_types": len(InstrumentType),
        "types": [
            {"type": t.value, "aliases": type_aliases.get(t.value, [])}
            for t in InstrumentType
        ],
    }


# Import INSTRUMENT_ALIASES from semantic module for the endpoint above
from semantic import INSTRUMENT_ALIASES


@app.get("/")
async def root() -> dict[str, Any]:
    """Engine information endpoint."""
    return {
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "version": ENGINE_VERSION,
        "port": ENGINE_PORT,
        "domain": ENGINE_DOMAIN,
        "subdomain": ENGINE_SUBDOMAIN,
        "status": "OPERATIONAL",
        "doctrine_count": len(doctrine_cache),
        "endpoints": [
            "GET  /health",
            "POST /query",
            "POST /chain/build",
            "POST /chain/gaps",
            "POST /interest/compute",
            "POST /normalize",
            "POST /legal-description/parse",
            "GET  /doctrines",
            "GET  /doctrines/{topic_key}",
            "GET  /doctrines/graph/interactions",
            "GET  /telemetry",
            "GET  /telemetry/metrics",
            "GET  /telemetry/drift",
            "GET  /telemetry/coverage",
            "GET  /search",
            "GET  /authority",
            "GET  /instrument-types",
        ],
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ═══════════════════════════════════════════════════════════════════════
# ACREAGE CALCULATOR
# ═══════════════════════════════════════════════════════════════════════

class AcreageCalculator:
    """Computes acreage from legal descriptions and survey data."""

    STANDARD_SECTION_ACRES = 640.0
    STANDARD_QUARTER_ACRES = 160.0
    STANDARD_HALF_ACRES = 320.0
    VARAS_PER_FOOT = 1.0 / (100.0 / 36.0)
    FEET_PER_VARA = 100.0 / 36.0
    ACRES_PER_LABOR = 177.1
    ACRES_PER_LEAGUE = 4428.4
    SQUARE_FEET_PER_ACRE = 43560.0

    def compute_aliquot_acreage(
        self,
        parent_acres: float,
        aliquot_parts: list[str],
    ) -> float:
        """Compute acreage from aliquot part descriptions."""
        result = parent_acres
        for part in aliquot_parts:
            part_lower = part.lower().strip()
            if "1/4" in part_lower or "quarter" in part_lower:
                result = result / 4.0
            elif "1/2" in part_lower or "half" in part_lower:
                result = result / 2.0
            elif "1/3" in part_lower or "third" in part_lower:
                result = result / 3.0
            elif "3/4" in part_lower:
                result = result * 3.0 / 4.0
            elif "2/3" in part_lower:
                result = result * 2.0 / 3.0
        return round(result, 4)

    def varas_to_feet(self, varas: float) -> float:
        """Convert Texas varas to feet."""
        return round(varas * self.FEET_PER_VARA, 4)

    def feet_to_varas(self, feet: float) -> float:
        """Convert feet to Texas varas."""
        return round(feet * self.VARAS_PER_FOOT, 4)

    def compute_rectangular_acreage(self, length_ft: float, width_ft: float) -> float:
        """Compute acreage from rectangular dimensions in feet."""
        return round((length_ft * width_ft) / self.SQUARE_FEET_PER_ACRE, 4)

    def compute_metes_and_bounds_area(self, calls: list[dict[str, float]]) -> float:
        """
        Compute area from metes and bounds calls using the Shoelace formula.
        Each call has 'x' and 'y' coordinates (or 'easting' and 'northing').
        """
        if len(calls) < 3:
            return 0.0
        n = len(calls)
        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            xi = calls[i].get("x", calls[i].get("easting", 0.0))
            yi = calls[i].get("y", calls[i].get("northing", 0.0))
            xj = calls[j].get("x", calls[j].get("easting", 0.0))
            yj = calls[j].get("y", calls[j].get("northing", 0.0))
            area += xi * yj
            area -= xj * yi
        area = abs(area) / 2.0
        return round(area / self.SQUARE_FEET_PER_ACRE, 4)

    def validate_closure(self, calls: list[dict[str, float]], tolerance_ft: float = 1.0) -> dict[str, Any]:
        """Validate metes and bounds closure."""
        if len(calls) < 3:
            return {"closed": False, "error_ft": float("inf"), "message": "Insufficient calls"}
        first = calls[0]
        last = calls[-1]
        x1 = first.get("x", first.get("easting", 0.0))
        y1 = first.get("y", first.get("northing", 0.0))
        x2 = last.get("x", last.get("easting", 0.0))
        y2 = last.get("y", last.get("northing", 0.0))
        import math
        error = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return {
            "closed": error <= tolerance_ft,
            "error_ft": round(error, 4),
            "tolerance_ft": tolerance_ft,
            "message": "Closure within tolerance" if error <= tolerance_ft else f"Closure error of {round(error, 4)} ft exceeds tolerance",
        }

    def texas_section_acreage_lookup(self, abstract_number: str, county: str) -> dict[str, Any]:
        """
        Look up actual Texas section acreage. In production this would query GLO.
        Returns standard section as default with note about verification needed.
        """
        return {
            "abstract_number": abstract_number,
            "county": county,
            "standard_acreage": self.STANDARD_SECTION_ACRES,
            "verified": False,
            "note": "Acreage should be verified against GLO records. Texas sections are not uniformly 640 acres.",
            "source": "Standard estimate — GLO verification recommended",
        }


# ═══════════════════════════════════════════════════════════════════════
# LEASE STATUS ANALYZER
# ═══════════════════════════════════════════════════════════════════════

class LeaseStatusAnalyzer:
    """Analyzes oil and gas lease status for run sheet purposes."""

    def analyze_lease_status(self, lease: dict[str, Any]) -> dict[str, Any]:
        """Determine current lease status from lease terms."""
        effective_date = lease.get("effective_date", "")
        primary_term_years = lease.get("primary_term_years", 3)
        producing = lease.get("producing", False)
        shut_in = lease.get("shut_in", False)
        operations_ongoing = lease.get("operations_ongoing", False)
        released = lease.get("released", False)
        if released:
            return {
                "status": "RELEASED",
                "description": "Lease has been released by lessee",
                "burden_on_minerals": False,
                "primary_term_expired": True,
            }
        primary_expired = self._check_primary_term(effective_date, primary_term_years)
        if not primary_expired:
            return {
                "status": "PRIMARY_TERM",
                "description": f"Lease is within primary term ({primary_term_years} years from {effective_date})",
                "burden_on_minerals": True,
                "primary_term_expired": False,
                "expiration_date": self._compute_expiration(effective_date, primary_term_years),
            }
        if producing:
            return {
                "status": "HBP",
                "description": "Lease is held by production in secondary term",
                "burden_on_minerals": True,
                "primary_term_expired": True,
            }
        if shut_in:
            shut_in_paid = lease.get("shut_in_royalty_paid", False)
            if shut_in_paid:
                return {
                    "status": "SHUT_IN",
                    "description": "Lease maintained by shut-in royalty payments",
                    "burden_on_minerals": True,
                    "primary_term_expired": True,
                    "warning": "Verify shut-in provisions and payment compliance",
                }
            return {
                "status": "SHUT_IN_UNPAID",
                "description": "Well shut-in but royalty payment status unverified",
                "burden_on_minerals": True,
                "primary_term_expired": True,
                "warning": "HIGH RISK — verify shut-in royalty compliance or lease may have terminated",
            }
        if operations_ongoing:
            return {
                "status": "OPERATIONS",
                "description": "Lease maintained by continuous drilling operations",
                "burden_on_minerals": True,
                "primary_term_expired": True,
                "warning": "Verify operations clause compliance",
            }
        return {
            "status": "EXPIRED",
            "description": f"Primary term expired with no production, shut-in, or operations maintaining the lease",
            "burden_on_minerals": False,
            "primary_term_expired": True,
        }

    def _check_primary_term(self, effective_date: str, term_years: int) -> bool:
        """Check if primary term has expired."""
        if not effective_date:
            return True
        try:
            from datetime import datetime as dt
            for fmt in ("%m/%d/%Y", "%Y-%m-%d", "%m-%d-%Y"):
                try:
                    start = dt.strptime(effective_date, fmt)
                    expiration = start.replace(year=start.year + term_years)
                    return dt.now() > expiration
                except ValueError:
                    continue
            return True
        except Exception:
            return True

    def _compute_expiration(self, effective_date: str, term_years: int) -> str:
        """Compute the primary term expiration date."""
        try:
            from datetime import datetime as dt
            for fmt in ("%m/%d/%Y", "%Y-%m-%d", "%m-%d-%Y"):
                try:
                    start = dt.strptime(effective_date, fmt)
                    expiration = start.replace(year=start.year + term_years)
                    return expiration.strftime("%m/%d/%Y")
                except ValueError:
                    continue
            return "UNKNOWN"
        except Exception:
            return "UNKNOWN"

    def check_pugh_clause(self, lease: dict[str, Any], unit_tracts: list[dict[str, Any]]) -> dict[str, Any]:
        """Analyze Pugh clause effect on lease status."""
        has_horizontal_pugh = lease.get("horizontal_pugh", False)
        has_vertical_pugh = lease.get("vertical_pugh", False)
        if not has_horizontal_pugh and not has_vertical_pugh:
            return {
                "pugh_clause": False,
                "effect": "No Pugh clause — entire lease maintained by any production",
            }
        results: dict[str, Any] = {
            "pugh_clause": True,
            "horizontal_pugh": has_horizontal_pugh,
            "vertical_pugh": has_vertical_pugh,
            "effects": [],
        }
        if has_horizontal_pugh:
            producing_tracts = [t for t in unit_tracts if t.get("producing", False)]
            non_producing = [t for t in unit_tracts if not t.get("producing", False)]
            results["effects"].append({
                "type": "HORIZONTAL",
                "producing_tracts": len(producing_tracts),
                "released_tracts": len(non_producing),
                "description": f"Horizontal Pugh releases {len(non_producing)} non-producing tract(s) from the lease",
            })
        if has_vertical_pugh:
            producing_depth = lease.get("producing_depth", "all")
            results["effects"].append({
                "type": "VERTICAL",
                "producing_depth": producing_depth,
                "description": f"Vertical Pugh releases all depths not included in the producing unit",
            })
        return results

    def analyze_top_lease_risk(self, lease: dict[str, Any]) -> dict[str, Any]:
        """Assess the risk of a top lease filing."""
        status = self.analyze_lease_status(lease)
        risk_level = "LOW"
        if status["status"] == "EXPIRED":
            risk_level = "CONFIRMED_EXPIRED"
        elif status["status"] in ("SHUT_IN", "SHUT_IN_UNPAID"):
            risk_level = "HIGH"
        elif status["status"] == "OPERATIONS":
            risk_level = "MEDIUM"
        elif status["status"] == "HBP":
            cessation_risk = lease.get("production_declining", False)
            risk_level = "MEDIUM" if cessation_risk else "LOW"
        elif status["status"] == "PRIMARY_TERM":
            risk_level = "LOW"
        return {
            "current_lease_status": status["status"],
            "top_lease_risk": risk_level,
            "description": f"Top lease risk is {risk_level} based on current lease status of {status['status']}",
            "recommendation": self._top_lease_recommendation(risk_level),
        }

    def _top_lease_recommendation(self, risk_level: str) -> str:
        """Generate top lease recommendation based on risk level."""
        recommendations = {
            "LOW": "Current lease appears secure. Top lease filing is speculative.",
            "MEDIUM": "Lease maintenance has potential vulnerabilities. Monitor production and operations closely.",
            "HIGH": "Lease may be at risk of termination. Verify all savings clause compliance. Consider top lease position.",
            "CONFIRMED_EXPIRED": "Lease has expired. Minerals are available for new leasing. File new lease directly.",
        }
        return recommendations.get(risk_level, "Assess lease status carefully before making leasing decisions.")


# ═══════════════════════════════════════════════════════════════════════
# DUHIG RULE ANALYZER
# ═══════════════════════════════════════════════════════════════════════

class DuhigAnalyzer:
    """Analyzes the application of the Duhig rule in mineral conveyances."""

    def analyze_duhig(
        self,
        grantor_mineral_ownership: float,
        conveyed_fraction: float,
        reserved_fraction: float,
        outstanding_interests: list[dict[str, Any]],
        is_warranty_deed: bool,
    ) -> dict[str, Any]:
        """
        Analyze whether the Duhig rule applies and its effect.

        The Duhig rule: When a warranty deed grantor conveys minerals but reserves
        a fraction, and outstanding prior conveyances exist such that the grantor
        cannot fulfill both the conveyance and the reservation, the warranty estops
        the grantor — the reservation is eliminated or reduced.
        """
        if not is_warranty_deed:
            return {
                "duhig_applies": False,
                "reason": "Duhig rule applies only to warranty deeds. This instrument is not a warranty deed.",
                "grantor_ownership_after": grantor_mineral_ownership - conveyed_fraction,
            }
        total_outstanding = sum(i.get("fraction", 0.0) for i in outstanding_interests)
        available = grantor_mineral_ownership - total_outstanding
        needed = conveyed_fraction + reserved_fraction
        if available >= needed:
            return {
                "duhig_applies": False,
                "reason": "Grantor owns sufficient mineral interest to satisfy both the conveyance and reservation.",
                "grantor_owns": grantor_mineral_ownership,
                "outstanding": total_outstanding,
                "available": available,
                "conveyed": conveyed_fraction,
                "reserved": reserved_fraction,
                "needed": needed,
                "grantee_receives": conveyed_fraction,
                "grantor_retains": reserved_fraction,
            }
        shortfall = needed - available
        grantor_reservation_after_duhig = max(0.0, reserved_fraction - shortfall)
        grantee_receives = available - grantor_reservation_after_duhig
        return {
            "duhig_applies": True,
            "reason": (
                f"Grantor owns {grantor_mineral_ownership} mineral interest with {total_outstanding} outstanding. "
                f"Available interest ({available}) is insufficient to satisfy both conveyance ({conveyed_fraction}) "
                f"and reservation ({reserved_fraction}). Under Duhig, the warranty estops the grantor's reservation."
            ),
            "grantor_owns": grantor_mineral_ownership,
            "outstanding": total_outstanding,
            "available": round(available, 8),
            "conveyed": conveyed_fraction,
            "reserved_attempted": reserved_fraction,
            "shortfall": round(shortfall, 8),
            "duhig_effect": {
                "grantor_reservation_reduced_to": round(grantor_reservation_after_duhig, 8),
                "grantee_receives": round(grantee_receives, 8),
                "reduction_amount": round(reserved_fraction - grantor_reservation_after_duhig, 8),
            },
            "authority": "Duhig v. Peavy-Moore Lumber Co., 135 Tex. 503 (1940)",
            "warning": "Duhig analysis is fact-intensive. Verify all fractional interests in the chain.",
        }


# ═══════════════════════════════════════════════════════════════════════
# RUN SHEET REPORT GENERATOR
# ═══════════════════════════════════════════════════════════════════════

class RunSheetReportGenerator:
    """Generates formatted text reports from run sheet data."""

    def generate_text_report(self, run_sheet: dict[str, Any]) -> str:
        """Generate a full text run sheet report."""
        lines: list[str] = []
        header = run_sheet.get("header", {})
        lines.append("=" * 80)
        lines.append("RUN SHEET / ABSTRACT OF TITLE")
        lines.append("=" * 80)
        lines.append(f"County: {header.get('county', 'Unknown')}, {header.get('state', 'Texas')}")
        lines.append(f"Tract: {header.get('tract_description', 'See instruments')}")
        lines.append(f"Effective Date: {header.get('effective_date', 'N/A')}")
        lines.append(f"Prepared By: {header.get('prepared_by', 'LM09 Engine')}")
        lines.append(f"Scope: {header.get('scope_of_examination', 'Full chain')}")
        lines.append(f"Generated: {header.get('generated_at', 'N/A')}")
        lines.append("-" * 80)
        chain = run_sheet.get("chain_of_title", [])
        if chain:
            lines.append("")
            lines.append("CHAIN OF TITLE")
            lines.append("-" * 80)
            for entry in chain:
                lines.append(f"Entry {entry.get('entry_no', '?'):>3} | {entry.get('date', 'N/A'):<12} | {entry.get('recording_ref', 'N/A'):<20}")
                lines.append(f"         Grantor:  {entry.get('grantor', 'N/A')}")
                lines.append(f"         Grantee:  {entry.get('grantee', 'N/A')}")
                lines.append(f"         Type:     {entry.get('type', 'N/A')}")
                lines.append(f"         Desc:     {entry.get('legal_description', 'N/A')[:80]}")
                if entry.get("consideration"):
                    lines.append(f"         Consid:   {entry['consideration']}")
                if entry.get("remarks"):
                    lines.append(f"         Remarks:  {entry['remarks']}")
                lines.append("")
        interests = run_sheet.get("mineral_interests", [])
        if interests:
            lines.append("")
            lines.append("MINERAL INTEREST SUMMARY")
            lines.append("-" * 80)
            lines.append(f"{'Owner':<40} {'Mineral Fraction':>18}")
            lines.append("-" * 60)
            for mi in interests:
                owner = mi.get("owner", "Unknown")
                fraction = mi.get("mineral_fraction", 0.0)
                lines.append(f"{owner:<40} {fraction:>18.6f}")
        requirements = run_sheet.get("requirements", [])
        if requirements:
            lines.append("")
            lines.append("TITLE REQUIREMENTS")
            lines.append("-" * 80)
            for req in requirements:
                lines.append(f"Req #{req.get('requirement_no', '?')}: [{req.get('severity', 'MEDIUM')}] {req.get('type', 'UNKNOWN')}")
                lines.append(f"  Description: {req.get('description', 'N/A')}")
                lines.append(f"  Curative:    {req.get('curative_action', 'N/A')}")
                lines.append(f"  Status:      {req.get('status', 'OPEN')}")
                lines.append("")
        summary = run_sheet.get("summary", {})
        if summary:
            lines.append("")
            lines.append("SUMMARY")
            lines.append("-" * 80)
            lines.append(f"Total Instruments:   {summary.get('total_instruments', 0)}")
            lines.append(f"Total Gaps:          {summary.get('total_gaps', 0)}")
            lines.append(f"Total Requirements:  {summary.get('total_requirements', 0)}")
            lines.append(f"Current Owners:      {summary.get('current_owners', 0)}")
            severity = summary.get("gap_severity_breakdown", {})
            lines.append(f"Gap Severity:        HIGH={severity.get('HIGH', 0)} MEDIUM={severity.get('MEDIUM', 0)} LOW={severity.get('LOW', 0)}")
        lines.append("")
        lines.append("=" * 80)
        lines.append(f"Generated by {ENGINE_ID} {ENGINE_NAME} v{ENGINE_VERSION}")
        lines.append("=" * 80)
        return "\n".join(lines)

    def generate_interest_report(self, computation: list[dict[str, Any]], gross_acres: float) -> str:
        """Generate a formatted interest computation report."""
        lines: list[str] = []
        lines.append("=" * 80)
        lines.append("INTEREST COMPUTATION REPORT")
        lines.append("=" * 80)
        lines.append(f"Gross Acres: {gross_acres}")
        lines.append("")
        lines.append(f"{'Owner':<35} {'MI Fraction':>12} {'NMA':>10} {'NRI':>10}")
        lines.append("-" * 70)
        total_nma = 0.0
        for entry in computation:
            owner = entry.get("owner", "Unknown")[:35]
            fraction = entry.get("mineral_fraction", 0.0)
            nma = entry.get("nma", 0.0)
            nri = entry.get("decimal_interest", entry.get("nri", 0.0))
            lines.append(f"{owner:<35} {fraction:>12.6f} {nma:>10.4f} {nri:>10.6f}")
            total_nma += nma
        lines.append("-" * 70)
        lines.append(f"{'TOTALS':<35} {'':>12} {total_nma:>10.4f}")
        lines.append("=" * 80)
        return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════
# ADDITIONAL API ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════

acreage_calc = AcreageCalculator()
lease_analyzer = LeaseStatusAnalyzer()
duhig_analyzer = DuhigAnalyzer()
report_generator = RunSheetReportGenerator()


@app.post("/acreage/aliquot")
async def compute_aliquot_acreage(
    parent_acres: float = Query(..., description="Parent tract acreage"),
    parts: list[str] = Query(..., description="Aliquot part descriptions"),
) -> dict[str, Any]:
    """Compute acreage from aliquot part descriptions."""
    result = acreage_calc.compute_aliquot_acreage(parent_acres, parts)
    return {
        "parent_acres": parent_acres,
        "aliquot_parts": parts,
        "computed_acres": result,
    }


@app.post("/acreage/rectangular")
async def compute_rectangular_acreage(length_ft: float, width_ft: float) -> dict[str, Any]:
    """Compute acreage from rectangular dimensions."""
    return {
        "length_ft": length_ft,
        "width_ft": width_ft,
        "acres": acreage_calc.compute_rectangular_acreage(length_ft, width_ft),
    }


@app.post("/acreage/metes-bounds")
async def compute_metes_bounds_area(calls: list[dict[str, float]]) -> dict[str, Any]:
    """Compute area and validate closure for metes and bounds description."""
    area = acreage_calc.compute_metes_and_bounds_area(calls)
    closure = acreage_calc.validate_closure(calls)
    return {
        "computed_acres": area,
        "closure": closure,
        "call_count": len(calls),
    }


@app.post("/lease/status")
async def analyze_lease_status(lease: dict[str, Any]) -> dict[str, Any]:
    """Analyze current oil and gas lease status."""
    return lease_analyzer.analyze_lease_status(lease)


@app.post("/lease/pugh")
async def analyze_pugh_clause(lease: dict[str, Any], unit_tracts: list[dict[str, Any]]) -> dict[str, Any]:
    """Analyze Pugh clause effect on lease status."""
    return lease_analyzer.check_pugh_clause(lease, unit_tracts)


@app.post("/lease/top-lease-risk")
async def assess_top_lease_risk(lease: dict[str, Any]) -> dict[str, Any]:
    """Assess risk of top lease filing based on current lease status."""
    return lease_analyzer.analyze_top_lease_risk(lease)


@app.post("/duhig/analyze")
async def analyze_duhig_rule(
    grantor_mineral_ownership: float,
    conveyed_fraction: float,
    reserved_fraction: float,
    outstanding_interests: list[dict[str, Any]],
    is_warranty_deed: bool = True,
) -> dict[str, Any]:
    """Analyze Duhig rule application in a mineral conveyance."""
    return duhig_analyzer.analyze_duhig(
        grantor_mineral_ownership=grantor_mineral_ownership,
        conveyed_fraction=conveyed_fraction,
        reserved_fraction=reserved_fraction,
        outstanding_interests=outstanding_interests,
        is_warranty_deed=is_warranty_deed,
    )


@app.post("/report/text")
async def generate_text_report(run_sheet: dict[str, Any]) -> dict[str, str]:
    """Generate a formatted text run sheet report."""
    return {"report": report_generator.generate_text_report(run_sheet)}


@app.post("/report/interest")
async def generate_interest_report(
    computation: list[dict[str, Any]],
    gross_acres: float,
) -> dict[str, str]:
    """Generate a formatted interest computation report."""
    return {"report": report_generator.generate_interest_report(computation, gross_acres)}


@app.get("/convert/varas-to-feet")
async def convert_varas_to_feet(varas: float) -> dict[str, float]:
    """Convert Texas varas to feet."""
    return {"varas": varas, "feet": acreage_calc.varas_to_feet(varas)}


@app.get("/convert/feet-to-varas")
async def convert_feet_to_varas(feet: float) -> dict[str, float]:
    """Convert feet to Texas varas."""
    return {"feet": feet, "varas": acreage_calc.feet_to_varas(feet)}


@app.get("/section/lookup")
async def lookup_section_acreage(abstract_number: str, county: str) -> dict[str, Any]:
    """Look up Texas section acreage by abstract number and county."""
    return acreage_calc.texas_section_acreage_lookup(abstract_number, county)


# ═══════════════════════════════════════════════════════════════════════
# BATCH PROCESSING ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════

class BatchQueryRequest(BaseModel):
    """Batch query request for processing multiple queries."""
    queries: list[QueryRequest] = Field(..., max_length=50)
    parallel: bool = Field(default=False, description="Process in parallel (not yet supported)")


class BatchNormalizeRequest(BaseModel):
    """Batch normalization request."""
    terms: list[str]
    category: Optional[str] = None


@app.post("/batch/query")
async def batch_query(request: BatchQueryRequest) -> dict[str, Any]:
    """Process multiple queries in batch."""
    if not response_engine:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    results = []
    for q in request.queries:
        try:
            result = response_engine.process_query(q)
            results.append({"status": "success", "response": result.model_dump()})
        except Exception as exc:
            results.append({"status": "error", "error": str(exc)})
    return {
        "total": len(request.queries),
        "succeeded": sum(1 for r in results if r["status"] == "success"),
        "failed": sum(1 for r in results if r["status"] == "error"),
        "results": results,
    }


@app.post("/batch/normalize")
async def batch_normalize(request: BatchNormalizeRequest) -> dict[str, Any]:
    """Normalize multiple terms in batch."""
    if not normalizer:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    results = []
    for term in request.terms:
        if request.category == "instrument":
            result = normalizer.normalize_instrument_type(term)
        elif request.category == "legal":
            result = normalizer.normalize_legal_term(term)
        elif request.category == "party":
            result = normalizer.normalize_party_designation(term)
        elif request.category == "curative":
            result = normalizer.normalize_curative_term(term)
        else:
            result = normalizer.normalize_any(term)
        results.append({
            "original": result.original,
            "normalized": result.normalized,
            "category": result.category,
            "confidence": result.confidence,
        })
    return {"total": len(request.terms), "results": results}


# ═══════════════════════════════════════════════════════════════════════
# TEXAS COUNTY REFERENCE DATA
# ═══════════════════════════════════════════════════════════════════════

PERMIAN_BASIN_COUNTIES: list[str] = [
    "Andrews", "Borden", "Crane", "Crockett", "Dawson", "Ector", "Gaines",
    "Garza", "Glasscock", "Howard", "Irion", "Lea", "Loving", "Martin",
    "Midland", "Mitchell", "Nolan", "Pecos", "Reagan", "Reeves", "Scurry",
    "Sterling", "Stonewall", "Terrell", "Terry", "Upton", "Val Verde",
    "Ward", "Winkler", "Yoakum",
]

EAGLE_FORD_COUNTIES: list[str] = [
    "Atascosa", "Bee", "DeWitt", "Dimmit", "Frio", "Gonzales", "Karnes",
    "La Salle", "Lavaca", "Live Oak", "McMullen", "Maverick", "Webb",
    "Wilson", "Zavala",
]

HAYNESVILLE_COUNTIES: list[str] = [
    "Cass", "Harrison", "Marion", "Panola", "Rusk", "Shelby",
]


@app.get("/counties/permian-basin")
async def get_permian_basin_counties() -> dict[str, Any]:
    """Get list of Permian Basin counties."""
    return {"play": "Permian Basin", "counties": PERMIAN_BASIN_COUNTIES, "count": len(PERMIAN_BASIN_COUNTIES)}


@app.get("/counties/eagle-ford")
async def get_eagle_ford_counties() -> dict[str, Any]:
    """Get list of Eagle Ford counties."""
    return {"play": "Eagle Ford", "counties": EAGLE_FORD_COUNTIES, "count": len(EAGLE_FORD_COUNTIES)}


@app.get("/counties/haynesville")
async def get_haynesville_counties() -> dict[str, Any]:
    """Get list of Haynesville counties."""
    return {"play": "Haynesville", "counties": HAYNESVILLE_COUNTIES, "count": len(HAYNESVILLE_COUNTIES)}


# ═══════════════════════════════════════════════════════════════════════
# INTEREST FRACTION PARSER
# ═══════════════════════════════════════════════════════════════════════

class FractionParser:
    """Parses fractional interest expressions from instrument text."""

    def parse(self, text: str) -> dict[str, Any]:
        """Parse fractional interest expressions from text."""
        import re
        results: list[dict[str, Any]] = []
        fraction_pattern = re.compile(r"(\d+)\s*/\s*(\d+)")
        for match in fraction_pattern.finditer(text):
            num = int(match.group(1))
            den = int(match.group(2))
            if den > 0 and num <= den:
                results.append({
                    "text": match.group(0),
                    "numerator": num,
                    "denominator": den,
                    "decimal": round(num / den, 8),
                    "position": match.start(),
                })
        percent_pattern = re.compile(r"(\d+(?:\.\d+)?)\s*%")
        for match in percent_pattern.finditer(text):
            val = float(match.group(1))
            if 0 < val <= 100:
                results.append({
                    "text": match.group(0),
                    "percentage": val,
                    "decimal": round(val / 100, 8),
                    "position": match.start(),
                })
        decimal_pattern = re.compile(r"(?:^|\s)(\d+\.\d{4,8})(?:\s|$)")
        for match in decimal_pattern.finditer(text):
            val = float(match.group(1))
            if 0 < val < 1:
                results.append({
                    "text": match.group(1),
                    "decimal": round(val, 8),
                    "position": match.start(),
                })
        word_fractions = {
            "one-half": 0.5, "one half": 0.5,
            "one-fourth": 0.25, "one fourth": 0.25, "one-quarter": 0.25,
            "one-eighth": 0.125, "one eighth": 0.125,
            "one-sixteenth": 0.0625, "one sixteenth": 0.0625,
            "three-fourths": 0.75, "three fourths": 0.75,
            "three-sixteenths": 0.1875, "three sixteenths": 0.1875,
            "one-third": 0.333333, "one third": 0.333333,
            "two-thirds": 0.666667, "two thirds": 0.666667,
        }
        text_lower = text.lower()
        for word, decimal in word_fractions.items():
            idx = text_lower.find(word)
            if idx >= 0:
                results.append({
                    "text": word,
                    "decimal": decimal,
                    "position": idx,
                    "type": "word_fraction",
                })
        results.sort(key=lambda x: x["position"])
        return {
            "input_text": text[:200],
            "fractions_found": len(results),
            "fractions": results,
        }


fraction_parser = FractionParser()


@app.post("/fraction/parse")
async def parse_fractions(text: str) -> dict[str, Any]:
    """Parse fractional interest expressions from instrument text."""
    return fraction_parser.parse(text)


# ═══════════════════════════════════════════════════════════════════════
# TITLE REQUIREMENT TRACKER
# ═══════════════════════════════════════════════════════════════════════

class TitleRequirementTracker:
    """Tracks and manages title examination requirements (curative items)."""

    def __init__(self) -> None:
        self._requirements: list[dict[str, Any]] = []
        self._next_id = 1

    def add_requirement(
        self,
        req_type: str,
        description: str,
        severity: str,
        curative_action: str,
        related_entries: Optional[list[int]] = None,
        authority: Optional[str] = None,
        deadline: Optional[str] = None,
    ) -> dict[str, Any]:
        """Add a new title requirement."""
        req = {
            "id": self._next_id,
            "type": req_type,
            "description": description,
            "severity": severity,
            "curative_action": curative_action,
            "related_entries": related_entries or [],
            "authority": authority or "",
            "deadline": deadline,
            "status": "OPEN",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "resolved_at": None,
            "resolution_notes": None,
        }
        self._requirements.append(req)
        self._next_id += 1
        logger.info("Title requirement #{} added: {} [{}]", req["id"], req_type, severity)
        return req

    def resolve_requirement(self, req_id: int, resolution_notes: str) -> Optional[dict[str, Any]]:
        """Mark a requirement as resolved."""
        for req in self._requirements:
            if req["id"] == req_id:
                req["status"] = "RESOLVED"
                req["resolved_at"] = datetime.now(timezone.utc).isoformat()
                req["resolution_notes"] = resolution_notes
                logger.info("Title requirement #{} resolved", req_id)
                return req
        return None

    def waive_requirement(self, req_id: int, waiver_reason: str) -> Optional[dict[str, Any]]:
        """Waive a requirement with documented reason."""
        for req in self._requirements:
            if req["id"] == req_id:
                req["status"] = "WAIVED"
                req["resolved_at"] = datetime.now(timezone.utc).isoformat()
                req["resolution_notes"] = f"WAIVED: {waiver_reason}"
                logger.info("Title requirement #{} waived: {}", req_id, waiver_reason)
                return req
        return None

    def get_open_requirements(self) -> list[dict[str, Any]]:
        """Get all open (unresolved) requirements."""
        return [r for r in self._requirements if r["status"] == "OPEN"]

    def get_all_requirements(self) -> list[dict[str, Any]]:
        """Get all requirements."""
        return list(self._requirements)

    def get_summary(self) -> dict[str, Any]:
        """Get requirements summary."""
        open_reqs = [r for r in self._requirements if r["status"] == "OPEN"]
        resolved = [r for r in self._requirements if r["status"] == "RESOLVED"]
        waived = [r for r in self._requirements if r["status"] == "WAIVED"]
        severity_counts: dict[str, int] = {}
        for r in open_reqs:
            sev = r.get("severity", "MEDIUM")
            severity_counts[sev] = severity_counts.get(sev, 0) + 1
        return {
            "total": len(self._requirements),
            "open": len(open_reqs),
            "resolved": len(resolved),
            "waived": len(waived),
            "open_by_severity": severity_counts,
            "has_high_severity_open": severity_counts.get("HIGH", 0) > 0,
        }

    def generate_curative_checklist(self) -> list[dict[str, Any]]:
        """Generate a curative action checklist from open requirements."""
        checklist = []
        open_reqs = sorted(self.get_open_requirements(), key=lambda r: {"HIGH": 0, "MEDIUM": 1, "LOW": 2}.get(r["severity"], 3))
        for i, req in enumerate(open_reqs):
            checklist.append({
                "item_number": i + 1,
                "requirement_id": req["id"],
                "severity": req["severity"],
                "type": req["type"],
                "curative_action": req["curative_action"],
                "related_entries": req["related_entries"],
                "authority": req["authority"],
                "deadline": req["deadline"],
                "completed": False,
            })
        return checklist


requirement_tracker = TitleRequirementTracker()


@app.post("/requirements/add")
async def add_title_requirement(
    req_type: str,
    description: str,
    severity: str = "MEDIUM",
    curative_action: str = "",
    related_entries: Optional[list[int]] = None,
    authority: Optional[str] = None,
) -> dict[str, Any]:
    """Add a title requirement."""
    return requirement_tracker.add_requirement(
        req_type=req_type,
        description=description,
        severity=severity,
        curative_action=curative_action,
        related_entries=related_entries,
        authority=authority,
    )


@app.post("/requirements/{req_id}/resolve")
async def resolve_requirement(req_id: int, notes: str) -> dict[str, Any]:
    """Resolve a title requirement."""
    result = requirement_tracker.resolve_requirement(req_id, notes)
    if not result:
        raise HTTPException(status_code=404, detail=f"Requirement {req_id} not found")
    return result


@app.get("/requirements")
async def list_requirements(status: Optional[str] = None) -> dict[str, Any]:
    """List title requirements."""
    if status == "open":
        reqs = requirement_tracker.get_open_requirements()
    else:
        reqs = requirement_tracker.get_all_requirements()
    return {"requirements": reqs, "summary": requirement_tracker.get_summary()}


@app.get("/requirements/checklist")
async def get_curative_checklist() -> dict[str, Any]:
    """Generate a curative action checklist."""
    return {"checklist": requirement_tracker.generate_curative_checklist()}


# ═══════════════════════════════════════════════════════════════════════
# INSTRUMENT TYPE CLASSIFIER
# ═══════════════════════════════════════════════════════════════════════

class InstrumentClassifier:
    """Classifies instrument types from instrument text or metadata."""

    CLASSIFICATION_PATTERNS: list[tuple[str, str, list[str]]] = [
        ("WARRANTY_DEED", "WARRANTY_DEED", ["general warranty deed", "gwd", "warranty deed", "grant bargain and sell"]),
        ("SPECIAL_WARRANTY_DEED", "SPECIAL_WARRANTY_DEED", ["special warranty deed", "swd", "grant bargain sell by way of"]),
        ("QUITCLAIM_DEED", "QUITCLAIM_DEED", ["quitclaim", "quit claim", "remise release"]),
        ("MINERAL_DEED", "MINERAL_DEED", ["mineral deed", "mineral conveyance", "conveys all minerals"]),
        ("ROYALTY_DEED", "ROYALTY_DEED", ["royalty deed", "royalty conveyance", "npri", "royalty interest"]),
        ("OIL_GAS_LEASE", "OIL_GAS_LEASE", ["oil and gas lease", "oil gas lease", "ogl", "mineral lease", "lease and let"]),
        ("ASSIGNMENT", "ASSIGNMENT", ["assignment of", "assigns transfers", "assign all right"]),
        ("RELEASE", "RELEASE", ["release of", "releases and discharges", "full release"]),
        ("AFFIDAVIT_OF_HEIRSHIP", "AFFIDAVIT_OF_HEIRSHIP", ["affidavit of heirship", "heirship affidavit"]),
        ("PROBATE", "PROBATE", ["order admitting will", "muniment of title", "letters testamentary"]),
        ("CORRECTION_DEED", "CORRECTION_DEED", ["correction deed", "corrective deed", "deed of correction"]),
        ("RATIFICATION", "RATIFICATION", ["ratification", "ratify and confirm"]),
        ("DESIGNATION_OF_POOLED_UNIT", "DESIGNATION_OF_POOLED_UNIT", ["designation of pooled unit", "dpu", "unit designation"]),
        ("RIGHT_OF_WAY", "RIGHT_OF_WAY", ["right of way", "right-of-way", "pipeline easement"]),
        ("EASEMENT", "EASEMENT", ["easement", "grant of easement"]),
        ("DEED_OF_TRUST", "DEED_OF_TRUST", ["deed of trust", "mortgage", "security instrument"]),
    ]

    def classify(self, text: str) -> dict[str, Any]:
        """Classify an instrument type from text."""
        text_lower = text.lower()
        matches: list[dict[str, Any]] = []
        for type_name, canonical, patterns in self.CLASSIFICATION_PATTERNS:
            score = 0
            matched_patterns = []
            for pattern in patterns:
                if pattern in text_lower:
                    score += 1
                    matched_patterns.append(pattern)
            if score > 0:
                matches.append({
                    "type": type_name,
                    "canonical": canonical,
                    "score": score,
                    "matched_patterns": matched_patterns,
                })
        matches.sort(key=lambda x: x["score"], reverse=True)
        if matches:
            best = matches[0]
            return {
                "classified_type": best["type"],
                "confidence": min(1.0, best["score"] / 2.0),
                "matched_patterns": best["matched_patterns"],
                "alternatives": [m["type"] for m in matches[1:3]],
            }
        return {
            "classified_type": "UNKNOWN",
            "confidence": 0.0,
            "matched_patterns": [],
            "alternatives": [],
        }


instrument_classifier = InstrumentClassifier()


@app.post("/instrument/classify")
async def classify_instrument(text: str) -> dict[str, Any]:
    """Classify an instrument type from instrument text."""
    return instrument_classifier.classify(text)


# ═══════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # ── LM09 FIX: assign lifespan to module-level app at runtime ──────
    # The module-level `app` was created with lifespan=None (guarded above)
    # to prevent ASGI state from interfering.  Now inject the lifespan
    # back into the app's router before running uvicorn, so there's only
    # ONE FastAPI app in the process (not two competing instances).
    app.router.lifespan_context = lifespan
    logger.info(
        "Starting {} {} on port {} ({} routes)",
        ENGINE_ID, ENGINE_NAME, ENGINE_PORT, len(app.routes),
    )
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=ENGINE_PORT,
        reload=False,
        log_level="info",
    )
